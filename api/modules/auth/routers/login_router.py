"""Login, logout, token refresh endpoints."""
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_db
from api.modules.auth.schemas.auth_schema import (
    LoginRequest, LoginResponse, LogoutRequest, RefreshRequest,
)
from api.modules.auth.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Authenticate user. Returns access token + sets refresh cookie."""
    svc = AuthService(db)
    return await svc.login(body.identifier, body.password, body.tenant_slug, request, response)


@router.post("/refresh", response_model=LoginResponse)
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Rotate refresh token and issue new access token. Token from cookie."""
    svc = AuthService(db)
    return await svc.refresh(request, response)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    body: LogoutRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Revoke session. Pass all_devices=true to logout everywhere."""
    svc = AuthService(db)
    await svc.logout(request, response, body.all_devices)
