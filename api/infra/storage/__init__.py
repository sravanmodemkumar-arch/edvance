"""Storage factory — R2 (Phase 1+2) or S3 (Phase 3) via INFRA_PROVIDER."""
from functools import lru_cache
from api.infra.provider import InfraProvider, get_provider
from api.infra.storage.base import StorageBackend


@lru_cache
def get_storage() -> StorageBackend:
    from api.core.config import get_settings
    s = get_settings()

    if get_provider() == InfraProvider.AWS:
        from api.infra.storage.s3_backend import S3Backend
        return S3Backend(bucket=s.r2_bucket_name, region=s.aws_region, cdn_url=s.cdn_url)

    from api.infra.storage.r2_backend import R2Backend
    return R2Backend(
        account_id=s.r2_account_id,
        bucket=s.r2_bucket_name,
        access_key=s.r2_access_key,
        secret_key=s.r2_secret_key,
        cdn_url=s.cdn_url,
    )


@lru_cache
def get_exam_storage() -> StorageBackend:
    """Separate bucket for exam papers (stricter access control)."""
    from api.core.config import get_settings
    s = get_settings()

    if get_provider() == InfraProvider.AWS:
        from api.infra.storage.s3_backend import S3Backend
        return S3Backend(bucket=s.r2_exam_bucket, region=s.aws_region)

    from api.infra.storage.r2_backend import R2Backend
    return R2Backend(
        account_id=s.r2_account_id,
        bucket=s.r2_exam_bucket,
        access_key=s.r2_access_key,
        secret_key=s.r2_secret_key,
    )
