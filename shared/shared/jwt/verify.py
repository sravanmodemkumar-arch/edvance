"""JWT verification — shared across all 7 services."""
from jose import JWTError, jwt
from fastapi import HTTPException, status
from shared.schemas.token_schema import TokenPayload
from shared.exceptions.auth_exceptions import InvalidTokenError
import os

ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")


def verify_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(
            sub=payload["sub"],
            role=payload["role"],
            inst=payload.get("inst"),
            exp=payload["exp"],
        )
    except JWTError:
        raise InvalidTokenError()


def verify_token_optional(token: str | None) -> TokenPayload | None:
    if not token:
        return None
    return verify_token(token)
