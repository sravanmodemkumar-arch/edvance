"""JWT creation — access tokens only. Refresh tokens are opaque UUIDs."""
from __future__ import annotations
import hashlib
import os
import uuid
from datetime import datetime, timedelta, timezone

from jose import jwt

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES", "15"))


def create_access_token(
    *,
    user_id: str,
    tenant_id: str,
    institution_type: str,
    roles: list[str],
    scopes: list[str],
    session_id: str,
) -> str:
    """Return signed JWT access token (15 min TTL)."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "institution_type": institution_type,
        "roles": roles,
        "scopes": scopes,
        "session_id": session_id,
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def generate_refresh_token() -> tuple[str, str]:
    """Return (raw_token, sha256_hash).

    raw_token  → sent to client as HttpOnly cookie
    sha256_hash → stored in sessions table (never store raw)
    """
    raw = str(uuid.uuid4())
    hashed = hashlib.sha256(raw.encode()).hexdigest()
    return raw, hashed
