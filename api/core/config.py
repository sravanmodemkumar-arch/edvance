"""Central config — reads from environment variables / .env file."""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "dev"
    debug: bool = True
    platform_domain: str = "localhost"
    cors_origins: str = "http://localhost:8080"

    # Deployment target: cloudflare | hybrid | aws
    infra_provider: str = "hybrid"

    # ── Database ──────────────────────────────────────────────────────────────
    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 10

    # ── JWT ───────────────────────────────────────────────────────────────────
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_expire_minutes: int = 30
    jwt_refresh_expire_days: int = 7

    # ── AWS ───────────────────────────────────────────────────────────────────
    aws_region: str = "ap-south-1"

    # ── Cloudflare ────────────────────────────────────────────────────────────
    cf_account_id: str = ""
    cf_api_token: str = ""

    # ── Storage (R2 = Phase 1+2, S3 = Phase 3) ───────────────────────────────
    cdn_url: str = ""
    r2_bucket_name: str = ""
    r2_exam_bucket: str = ""
    r2_account_id: str = ""
    r2_access_key: str = ""
    r2_secret_key: str = ""

    # ── Queues ────────────────────────────────────────────────────────────────
    sqs_cdn_queue_url: str = ""
    sqs_exam_queue_url: str = ""
    sqs_notification_queue_url: str = ""
    cf_cdn_queue_id: str = ""
    cf_exam_queue_id: str = ""
    cf_notification_queue_id: str = ""

    # ── Celery ────────────────────────────────────────────────────────────────
    celery_broker_url: str = ""        # auto-built from database_url if empty
    celery_result_backend: str = ""

    # ── Firebase (FCM push) ───────────────────────────────────────────────────
    firebase_credentials_path: str = ""

    # ── WhatsApp ──────────────────────────────────────────────────────────────
    whatsapp_provider: str = "gupshup"  # gupshup | waba
    whatsapp_api_key: str = ""
    whatsapp_app_id: str = ""

    # ── SMS (MSG91) ───────────────────────────────────────────────────────────
    msg91_auth_key: str = ""
    msg91_sender_id: str = "EDVANC"

    # ── Payments (Razorpay) ───────────────────────────────────────────────────
    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    razorpay_webhook_secret: str = ""

    model_config = {"env_file": ".env", "case_sensitive": False}


@lru_cache
def get_settings() -> Settings:
    return Settings()
