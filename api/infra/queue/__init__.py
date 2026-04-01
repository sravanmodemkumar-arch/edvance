"""Queue factory — CF Queues (Phase 1) or SQS (Phase 2+) via INFRA_PROVIDER."""
from functools import lru_cache
from api.infra.provider import InfraProvider, get_provider
from api.infra.queue.base import QueueBackend, QueueMessage, EnqueueResult

__all__ = ["get_queue", "QueueMessage", "EnqueueResult"]


@lru_cache
def get_queue() -> QueueBackend:
    from api.core.config import get_settings
    s = get_settings()

    if get_provider() in (InfraProvider.HYBRID, InfraProvider.AWS):
        from api.infra.queue.sqs_backend import SQSBackend
        return SQSBackend(
            region=s.aws_region,
            queue_url_map={
                "cdn": s.sqs_cdn_queue_url,
                "exam": s.sqs_exam_queue_url,
                "notification": s.sqs_notification_queue_url,
            },
        )

    from api.infra.queue.cf_queue import CFQueueBackend
    return CFQueueBackend(
        account_id=s.cf_account_id,
        api_token=s.cf_api_token,
        queue_id_map={
            "cdn": s.cf_cdn_queue_id,
            "exam": s.cf_exam_queue_id,
            "notification": s.cf_notification_queue_id,
        },
    )
