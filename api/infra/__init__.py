"""Infrastructure abstraction — storage, queue, provider detection.

INFRA_PROVIDER=cloudflare  → R2 storage + CF Queues  (Phase 1 VPS)
INFRA_PROVIDER=hybrid      → R2 storage + SQS         (Phase 2)
INFRA_PROVIDER=aws         → S3 storage + SQS         (Phase 3)
"""
from api.infra.provider import InfraProvider, get_provider
from api.infra.storage import get_storage
from api.infra.queue import get_queue

__all__ = ["InfraProvider", "get_provider", "get_storage", "get_queue"]
