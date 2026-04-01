"""AWS SQS queue backend — Phase 2 (hybrid) and Phase 3 (full AWS)."""
import json
import boto3
from api.infra.queue.base import QueueBackend, QueueMessage, EnqueueResult


class SQSBackend(QueueBackend):
    def __init__(self, region: str, queue_url_map: dict[str, str]) -> None:
        self._client = boto3.client("sqs", region_name=region)
        self._urls = queue_url_map  # logical_name -> SQS URL

    def _url(self, queue_name: str) -> str:
        url = self._urls.get(queue_name)
        if not url:
            raise ValueError(f"No SQS URL for queue: {queue_name}")
        return url

    async def enqueue(self, message: QueueMessage) -> EnqueueResult:
        resp = self._client.send_message(
            QueueUrl=self._url(message.queue_name),
            MessageBody=json.dumps(message.body),
            DelaySeconds=message.delay_seconds,
        )
        return EnqueueResult(message_id=resp["MessageId"], queue_name=message.queue_name)

    async def enqueue_batch(self, messages: list[QueueMessage]) -> list[EnqueueResult]:
        if not messages:
            return []
        entries = [
            {"Id": str(i), "MessageBody": json.dumps(m.body), "DelaySeconds": m.delay_seconds}
            for i, m in enumerate(messages[:10])  # SQS max 10 per batch
        ]
        resp = self._client.send_message_batch(
            QueueUrl=self._url(messages[0].queue_name), Entries=entries
        )
        return [
            EnqueueResult(message_id=r["MessageId"], queue_name=messages[0].queue_name)
            for r in resp.get("Successful", [])
        ]
