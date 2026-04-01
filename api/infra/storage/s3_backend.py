"""AWS S3 storage backend — Phase 3 (full AWS) or fallback.

Identical interface to R2Backend. Swap by changing INFRA_PROVIDER=aws.
"""
import boto3
from botocore.client import Config
from api.infra.storage.base import StorageBackend, UploadResult


class S3Backend(StorageBackend):
    def __init__(
        self,
        bucket: str,
        region: str,
        cdn_url: str = "",
    ) -> None:
        self._bucket = bucket
        self._cdn_url = cdn_url.rstrip("/")
        self._client = boto3.client(
            "s3",
            region_name=region,
            config=Config(signature_version="s3v4"),
        )

    async def upload(self, key: str, data: bytes, content_type: str) -> UploadResult:
        self._client.put_object(
            Bucket=self._bucket, Key=key, Body=data, ContentType=content_type
        )
        return UploadResult(key=key, url=self.public_url(key), size=len(data))

    async def delete(self, key: str) -> None:
        self._client.delete_object(Bucket=self._bucket, Key=key)

    def presigned_put(self, key: str, content_type: str, expires_in: int = 3600) -> str:
        return self._client.generate_presigned_url(
            "put_object",
            Params={"Bucket": self._bucket, "Key": key, "ContentType": content_type},
            ExpiresIn=expires_in,
        )

    def presigned_get(self, key: str, expires_in: int = 3600) -> str:
        return self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=expires_in,
        )

    def public_url(self, key: str) -> str:
        if self._cdn_url:
            return f"{self._cdn_url}/{key}"
        return f"https://{self._bucket}.s3.amazonaws.com/{key}"
