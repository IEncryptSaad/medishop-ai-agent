from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass
class ConversationMessage:
    sender_type: str
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class ConversationRecord:
    id: str
    session_id: str
    messages: list[ConversationMessage] = field(default_factory=list)


class ConversationRepository:
    def __init__(self) -> None:
        self._by_session: dict[str, ConversationRecord] = {}

    def get_or_create(self, session_id: str) -> ConversationRecord:
        if session_id not in self._by_session:
            self._by_session[session_id] = ConversationRecord(
                id=str(uuid4()), session_id=session_id
            )
        return self._by_session[session_id]

    def add_message(self, session_id: str, sender_type: str, content: str) -> ConversationRecord:
        conversation = self.get_or_create(session_id)
        conversation.messages.append(ConversationMessage(sender_type=sender_type, content=content))
        return conversation


conversation_repository = ConversationRepository()
