"""FastAPI dependency shortcuts — DB session, current user, tenant."""
from typing import Annotated
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from shared.jwt.verify import verify_token, TokenPayload
from shared.exceptions.auth_exceptions import InvalidTokenError
from api.core.database import get_db


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> TokenPayload:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return verify_token(authorization.removeprefix("Bearer ").strip())
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc


async def get_current_user_optional(
    authorization: Annotated[str | None, Header()] = None,
) -> TokenPayload | None:
    if not authorization:
        return None
    try:
        return await get_current_user(authorization)
    except HTTPException:
        return None


# Type aliases — use these in router signatures
DB = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[TokenPayload, Depends(get_current_user)]
OptionalUser = Annotated[TokenPayload | None, Depends(get_current_user_optional)]
