"""Celery app — broker switches by INFRA_PROVIDER.

Phase 1 (cloudflare/VPS): PostgreSQL broker — no Redis, no SQS needed.
Phase 2+ (hybrid/aws):    SQS broker via celery[sqs].

On Lambda: workers run via SQS EventSourceMapping, not Celery.
Celery is used only on VPS (Phase 1) and ECS worker tasks (Phase 2+).
"""
from celery import Celery
from api.core.config import get_settings


def _make_celery() -> Celery:
    s = get_settings()

    if s.infra_provider in ("hybrid", "aws") and s.celery_broker_url:
        broker = s.celery_broker_url
        backend = s.celery_result_backend or s.celery_broker_url
    else:
        # Phase 1: use PostgreSQL as broker (celery[sqlalchemy])
        pg_url = (
            s.database_url
            .replace("postgresql+asyncpg://", "postgresql://")
            .replace("postgres://", "postgresql://")
        )
        broker = f"db+{pg_url}"
        backend = f"db+{pg_url}"

    app = Celery("edvance", broker=broker, backend=backend)
    app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="Asia/Kolkata",
        enable_utc=True,
        task_track_started=True,
        worker_prefetch_multiplier=1,       # fair dispatch
        task_acks_late=True,                # ack after completion, not on receive
    )
    app.autodiscover_tasks(["api.workers"])
    return app


celery_app = _make_celery()
