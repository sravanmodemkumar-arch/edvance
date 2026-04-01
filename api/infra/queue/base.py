"""Queue backend ABC — enqueue single and batch messages."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class QueueMessage:
    body: dict[str, Any]
    queue_name: str           # logical name: cdn | exam | notification
    delay_seconds: int = 0
    deduplication_id: str | None = None


@dataclass
class EnqueueResult:
    message_id: str
    queue_name: str
    success: bool = True


class QueueBackend(ABC):
    @abstractmethod
    async def enqueue(self, message: QueueMessage) -> EnqueueResult:
        """Send one message to the named queue."""

    @abstractmethod
    async def enqueue_batch(self, messages: list[QueueMessage]) -> list[EnqueueResult]:
        """Send up to provider batch limit (SQS=10, CF=100)."""
