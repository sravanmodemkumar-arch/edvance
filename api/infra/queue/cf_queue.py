"""Cloudflare Queues HTTP backend — Phase 1 (VPS + CF Tunnel).

CF Queues uses REST API (no native Celery broker).
Messages are consumed by CF Workers or webhook receivers.
Docs: https://developers.cloudflare.com/queues/reference/rest-api/
"""
import json
import httpx
from api.infra.queue.base import QueueBackend, QueueMessage, EnqueueResult


class CFQueueBackend(QueueBackend):
    def __init__(
        self,
        account_id: str,
        api_token: str,
        queue_id_map: dict[str, str],
    ) -> None:
        self._base = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/queues"
        self._headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
        self._ids = queue_id_map  # logical_name -> CF queue_id

    def _queue_id(self, name: str) -> str:
        qid = self._ids.get(name)
        if not qid:
            raise ValueError(f"No CF Queue ID for: {name}")
        return qid

    async def enqueue(self, message: QueueMessage) -> EnqueueResult:
        qid = self._queue_id(message.queue_name)
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base}/{qid}/messages",
                headers=self._headers,
                json={"messages": [{"body": json.dumps(message.body)}]},
            )
            resp.raise_for_status()
        return EnqueueResult(message_id=qid, queue_name=message.queue_name)

    async def enqueue_batch(self, messages: list[QueueMessage]) -> list[EnqueueResult]:
        if not messages:
            return []
        qid = self._queue_id(messages[0].queue_name)
        batch = [{"body": json.dumps(m.body)} for m in messages[:100]]  # CF max 100
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self._base}/{qid}/messages",
                headers=self._headers,
                json={"messages": batch},
            )
            resp.raise_for_status()
        return [EnqueueResult(message_id=qid, queue_name=m.queue_name) for m in messages]
