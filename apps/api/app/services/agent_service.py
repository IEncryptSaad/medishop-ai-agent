from __future__ import annotations

import re
from collections.abc import Iterable
from hashlib import sha256

from app.contracts.agent import (
    AgentChatRequest,
    AgentChatResponse,
    AgentRecommendation,
    AgentSource,
)
from app.repositories.conversation_repository import conversation_repository
from app.repositories.knowledge_repository import KnowledgeEntry, KnowledgeRepository
from app.repositories.product_repository import ProductRepository

MEDICAL_DISCLAIMER = (
    "This is general health information and not a diagnosis or substitute for "
    "professional medical advice."
)
ESCALATION = (
    "Please contact a licensed healthcare professional for diagnosis or medication decisions, "
    "and seek emergency care for severe or urgent symptoms."
)


class AgentService:
    def __init__(
        self,
        products: ProductRepository | None = None,
        knowledge: KnowledgeRepository | None = None,
        conversations=conversation_repository,
    ) -> None:
        self.products = products or ProductRepository()
        self.knowledge = knowledge or KnowledgeRepository()
        self.conversations = conversations

    def chat(self, payload: AgentChatRequest) -> AgentChatResponse:
        intent = self.classify_intent(payload.message)
        self.conversations.add_message(payload.session_id, "user", payload.message)

        product_results = self._matching_products(payload.message, intent)
        knowledge_results = self.knowledge.search(payload.message)
        recommendations = self._product_recommendations(product_results, intent)
        sources = self._sources(knowledge_results)
        response = self._response_for_intent(
            intent, payload.message, product_results, knowledge_results
        )

        conversation = self.conversations.add_message(payload.session_id, "assistant", response)
        return AgentChatResponse(
            response=response,
            sources=sources,
            recommendations=recommendations,
            conversation_id=conversation.id,
        )

    @staticmethod
    def classify_intent(message: str) -> str:
        text = message.lower()
        tokens = set(re.findall(r"\b[\w']+\b", text))
        greeting_tokens = {word.strip(".,?!") for word in text.split()}
        is_greeting = (
            text.strip() in {"hi", "hello", "hey", "help"}
            or text.startswith(("hi ", "hello ", "hey "))
            or "what can you do" in text
        )
        if tokens & {"appointment", "book", "schedule", "consult", "pharmacist"}:
            return "appointment_booking"

        support_tokens = {
            "ticket",
            "refund",
            "damaged",
            "leaked",
            "missing",
            "order",
            "shipping",
            "support",
            "delivery",
            "return",
        }
        late_context_tokens = {"delivery", "order", "package", "shipment", "shipping"}
        is_late_support_issue = "late" in tokens and bool(tokens & late_context_tokens)
        is_delayed_shipment_issue = bool(tokens & {"delayed", "delay"}) and bool(
            tokens & {"shipment", "shipping", "delivery", "order", "package"}
        )
        if tokens & support_tokens or is_late_support_issue or is_delayed_shipment_issue:
            return "support_request"

        if tokens & {
            "symptom",
            "diagnose",
            "medication",
            "medicine",
            "dose",
            "pain",
            "fever",
            "cold",
            "cough",
            "rash",
            "allergy",
            "emergency",
            "nausea",
        }:
            return "medical_faq"
        if tokens & {
            "product",
            "recommend",
            "moisturizer",
            "sunscreen",
            "spray",
            "skin",
            "spf",
            "ceramide",
            "saline",
        }:
            return "product_question"
        if is_greeting or greeting_tokens & {"help"}:
            return "greeting_help"
        return "general"

    @staticmethod
    def _health_related(message: str) -> bool:
        return AgentService.classify_intent(message) == "medical_faq"

    def _matching_products(self, message: str, intent: str):
        if intent not in {"product_question", "medical_faq"}:
            return []

        from app.contracts.products import ProductSearchRequest

        in_stock_only = intent == "product_question"
        product_results, _ = self.products.search(
            ProductSearchRequest(query=message, in_stock_only=in_stock_only, page_size=3)
        )
        return product_results

    @staticmethod
    def _product_recommendations(
        product_results: Iterable, intent: str
    ) -> list[AgentRecommendation]:
        recommendations: list[AgentRecommendation] = []
        for product in product_results:
            stock_note = (
                "currently in stock"
                if product.stock_quantity > 0
                else "listed in the demo catalog"
            )
            reason = (
                f"Matches your question and is {stock_note}."
                if intent == "product_question"
                else f"May be relevant supportive-care context and is {stock_note}."
            )
            recommendations.append(
                AgentRecommendation(
                    id=product.id,
                    type="product",
                    title=product.name,
                    reason=reason,
                    metadata={
                        "sku": product.sku,
                        "price": str(product.price),
                        "stock_quantity": product.stock_quantity,
                    },
                )
            )
        return recommendations

    @staticmethod
    def _sources(knowledge_results: list[KnowledgeEntry]) -> list[AgentSource]:
        return [
            AgentSource(
                title=entry.title,
                source_type=entry.source_type,
                uri=entry.uri,
                score=max(0.1, 0.95 - index * 0.1),
                metadata=entry.metadata,
            )
            for index, entry in enumerate(knowledge_results)
        ]

    def _response_for_intent(
        self,
        intent: str,
        message: str,
        product_results: list,
        knowledge_results: list[KnowledgeEntry],
    ) -> str:
        variant = self._variant(message, 3)
        product_text = self._format_products(product_results)
        source_text = self._format_sources(knowledge_results)

        if intent == "product_question":
            openings = [
                "Here are the best demo-catalog matches I found.",
                "I found a few catalog options that fit your question.",
                "Based on the local MediShop catalog, these are good starting points.",
            ]
            response = openings[variant]
            if product_text:
                response += f" {product_text}"
            else:
                response += (
                    " I did not find an exact in-stock match, so broadening the search may help."
                )
            if source_text:
                response += f" I also found guidance from {source_text}."
            return response

        if intent == "appointment_booking":
            prompts = [
                "I can help prepare an appointment request with a pharmacist or care professional.",
                "For booking, I would collect the appointment type, preferred time window, "
                "and a short note for the clinician.",
                "A pharmacist consultation is a good demo workflow when you want product "
                "compatibility or safe-use guidance.",
            ]
            return (
                f"{prompts[variant]} Please share your preferred date/time, timezone, "
                "and what you want to discuss; "
                "I can then route you to the appointment form with those details."
            )

        if intent == "support_request":
            prompts = [
                "I can help triage this order issue for the support queue.",
                "That sounds like something support should track in a ticket.",
                "I can summarize the problem so the support team has the right details."
            ]
            return (
                f"{prompts[variant]} Please include the order number, affected item, "
                "photos if something arrived damaged, "
                "and whether you prefer a replacement, refund, or status update."
            )

        if intent == "medical_faq":
            openings = [
                "I can share general wellness information, but I cannot diagnose symptoms.",
                "For a demo-safe answer, I can explain general self-care considerations only.",
                "I can provide non-diagnostic information from the knowledge base."
            ]
            response = openings[variant]
            if source_text:
                response += f" Relevant knowledge-base topics include {source_text}."
            if product_text:
                response += f" Product context: {product_text}"
            response += f" {MEDICAL_DISCLAIMER} {ESCALATION}"
            return response

        if intent == "greeting_help":
            return (
                "Hi! I can help with product recommendations, appointment booking prep, "
                "order/support issues, and general non-diagnostic medical information. "
                "Try asking about sensitive-skin products, "
                "booking a pharmacist consult, or a damaged order."
            )

        return (
            "I can help with MediShop products, appointments, support tickets, or general "
            "health information. Tell me what you are trying to do and I will use the demo "
            "catalog and knowledge base where relevant."
        )

    @staticmethod
    def _variant(message: str, count: int) -> int:
        digest = sha256(message.strip().lower().encode("utf-8")).hexdigest()
        return int(digest[:8], 16) % count

    @staticmethod
    def _format_products(product_results: list) -> str:
        if not product_results:
            return ""
        chunks = []
        for product in product_results:
            stock = "in stock" if product.stock_quantity > 0 else "out of stock in this demo"
            chunks.append(f"{product.name} ({product.sku}, ${product.price}, {stock})")
        return "Recommended products: " + "; ".join(chunks) + "."

    @staticmethod
    def _format_sources(knowledge_results: list[KnowledgeEntry]) -> str:
        if not knowledge_results:
            return ""
        return ", ".join(entry.title for entry in knowledge_results)
