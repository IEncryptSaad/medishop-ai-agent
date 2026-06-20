from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class KnowledgeEntry:
    title: str
    content: str
    source_type: str = "knowledge_document"
    uri: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


DEMO_KNOWLEDGE = [
    KnowledgeEntry(
        title="Sensitive Skin Care Guide",
        uri="kb://sensitive-skin-care",
        content=(
            "For sensitive skin, choose fragrance-free products, patch test new skincare, "
            "and consider moisturizers with ceramides."
        ),
        metadata={"topic": "skincare"},
    ),
    KnowledgeEntry(
        title="When to Seek Urgent Care",
        uri="kb://urgent-care",
        content=(
            "Emergency symptoms such as trouble breathing, chest pain, severe allergic reaction, "
            "fainting, or sudden weakness need immediate medical attention."
        ),
        metadata={"topic": "safety"},
    ),
    KnowledgeEntry(
        title="Common Cold Self-Care",
        uri="kb://cold-self-care",
        content=(
            "Rest, fluids, saline spray, and humidified air can support comfort during a "
            "common cold. Ask a clinician before combining medicines."
        ),
        metadata={"topic": "medical_faq"},
    ),
]


class KnowledgeRepository:
    def search(self, query: str, limit: int = 3) -> list[KnowledgeEntry]:
        words = {word.strip(".,?!").lower() for word in query.split() if len(word) > 2}
        scored: list[tuple[int, KnowledgeEntry]] = []
        for entry in DEMO_KNOWLEDGE:
            haystack = f"{entry.title} {entry.content}".lower()
            score = sum(1 for word in words if word in haystack)
            if score:
                scored.append((score, entry))
        return [
            entry for _, entry in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]
        ]
