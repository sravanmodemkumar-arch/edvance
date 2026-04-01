"""Storage backend ABC — upload, delete, presigned URLs, public URL."""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class UploadResult:
    key: str
    url: str      # public CDN URL
    size: int     # bytes uploaded


class StorageBackend(ABC):
    @abstractmethod
    async def upload(self, key: str, data: bytes, content_type: str) -> UploadResult:
        """Upload bytes, return result with CDN URL."""

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Permanently delete object."""

    @abstractmethod
    def presigned_put(self, key: str, content_type: str, expires_in: int = 3600) -> str:
        """Presigned PUT URL for direct browser → storage upload (bypass API)."""

    @abstractmethod
    def presigned_get(self, key: str, expires_in: int = 3600) -> str:
        """Presigned GET URL for time-limited private download."""

    @abstractmethod
    def public_url(self, key: str) -> str:
        """Permanent public CDN URL (for CDN-cached assets)."""
