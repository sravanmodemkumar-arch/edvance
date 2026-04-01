"""Authenticated profile and account-ops endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from shared.schemas.token_schema import TokenPayload
from api.core.database import get_db
from api.core.dependencies import get_current_user
from api.modules.auth.schemas.ops_schema import ChangePasswordRequest, ChangePhoneRequest
from api.modules.auth.services.password_service import PasswordService
from api.modules.auth.repositories.user_repo import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
async def me(
    current_user: TokenPayload = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = UserRepository(db)
    user = await repo.get_by_uid(current_user.sub)
    if user is None:
        from shared.exceptions.auth_exceptions import InvalidTokenError
        raise InvalidTokenError()
    return {
        "uid": user.uid,
        "full_name": user.full_name,
        "email": user.email,
        "mobile": user.mobile,
        "roles": current_user.roles,
        "tenant_id": current_user.tenant_id,
        "institution_type": current_user.institution_type,
    }


@router.patch("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    body: ChangePasswordRequest,
    current_user: TokenPayload = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = PasswordService(db)
    await svc.change_password(current_user.sub, body.current_password, body.new_password)
    return {"detail": "Password changed successfully."}


@router.patch("/change-phone", status_code=status.HTTP_200_OK)
async def change_phone(
    body: ChangePhoneRequest,
    current_user: TokenPayload = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """OTP for CHANGE_PHONE must already be verified before calling this."""
    from shared.utils.phone import normalize_mobile
    repo = UserRepository(db)
    user = await repo.get_by_uid(current_user.sub)
    if user is None:
        from shared.exceptions.auth_exceptions import InvalidTokenError
        raise InvalidTokenError()
    await repo.update_mobile(user.id, normalize_mobile(body.new_mobile))
    return {"detail": "Mobile number updated."}
