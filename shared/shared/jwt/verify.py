"""JWT verification — shared across all services."""
from __future__ import annotations
import os

from jose import JWTError, jwt

from shared.exceptions.auth_exceptions import InvalidTokenError
from shared.schemas.token_schema import TokenPayload

ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")


def verify_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(
            sub=payload["sub"],
            tenant_id=payload["tenant_id"],
            institution_type=payload["institution_type"],
            roles=payload["roles"],
            scopes=payload.get("scopes", []),
            session_id=payload["session_id"],
            exp=payload["exp"],
        )
    except (JWTError, KeyError):
        raise InvalidTokenError()


def verify_token_optional(token: str | None) -> TokenPayload | None:
    if not token:
        return None
    return verify_token(token)
