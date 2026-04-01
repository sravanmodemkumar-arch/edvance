"""Infrastructure provider detection.

Set INFRA_PROVIDER in .env to switch deployment target:
  cloudflare  — Phase 1: VPS + CF Tunnel + R2 + CF Queues
  hybrid      — Phase 2: Lambda + ECS + R2 + SQS  (default)
  aws         — Phase 3: Lambda + ECS + S3 + SQS
"""
from enum import StrEnum
from functools import lru_cache
import os


class InfraProvider(StrEnum):
    CLOUDFLARE = "cloudflare"
    HYBRID = "hybrid"
    AWS = "aws"


@lru_cache
def get_provider() -> InfraProvider:
    raw = os.getenv("INFRA_PROVIDER", "hybrid").lower().strip()
    try:
        return InfraProvider(raw)
    except ValueError:
        return InfraProvider.HYBRID
