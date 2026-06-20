from __future__ import annotations

from app.contracts.agent import (
    AgentChatRequest,
    AgentChatResponse,
    AgentRecommendation,
    AgentSource,
)
from app.repositories.conversation_repository import conversation_repository
from app.repositories.knowledge_repository import KnowledgeRepository
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
        sources: list[AgentSource] = []
        recommendations: list[AgentRecommendation] = []
        response = self._response_for_intent(intent)

        if intent in {"product_question", "medical_faq"}:
            from app.contracts.products import ProductSearchRequest

            product_results, _ = self.products.search(
                ProductSearchRequest(query=payload.message, in_stock_only=True, page_size=3)
            )
            for product in product_results:
                recommendations.append(
                    AgentRecommendation(
                        id=product.id,
                        type="product",
                        title=product.name,
                        reason="Matches your question and is currently in stock.",
                        metadata={"sku": product.sku, "price": str(product.price)},
                    )
                )
            if recommendations:
                names = ", ".join(r.title for r in recommendations)
                response += f" Relevant products include: {names}."

        for index, entry in enumerate(self.knowledge.search(payload.message)):
            sources.append(
                AgentSource(
                    title=entry.title,
                    source_type=entry.source_type,
                    uri=entry.uri,
                    score=max(0.1, 0.95 - index * 0.1),
                    metadata=entry.metadata,
                )
            )

        if intent == "medical_faq":
            response += f" {MEDICAL_DISCLAIMER} {ESCALATION}"
        elif self._health_related(payload.message):
            response += f" {MEDICAL_DISCLAIMER}"

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
        if any(w in text for w in ["appointment", "book", "schedule", "consultation"]):
            return "appointment_booking"
        if any(w in text for w in ["ticket", "refund", "damaged", "order", "shipping", "support"]):
            return "support_request"
        if any(
            w in text
            for w in [
                "symptom",
                "diagnose",
                "medication",
                "medicine",
                "pain",
                "fever",
                "cold",
                "rash",
                "emergency",
            ]
        ):
            return "medical_faq"
        if any(w in text for w in ["product", "moisturizer", "sunscreen", "spray", "skin", "spf"]):
            return "product_question"
        return "general"

    @staticmethod
    def _health_related(message: str) -> bool:
        return AgentService.classify_intent(message) == "medical_faq"

    @staticmethod
    def _response_for_intent(intent: str) -> str:
        return {
            "product_question": "I can help compare products using the local catalog.",
            "appointment_booking": (
                "I can help you prepare to book an appointment with a pharmacist "
                "or care professional."
            ),
            "support_request": (
                "I can help route this support request and recommend opening a ticket "
                "if follow-up is needed."
            ),
            "medical_faq": "I can share general wellness information from the knowledge base.",
            "general": "How can I help with MediShop products, appointments, or support today?",
        }[intent]
