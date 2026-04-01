"""OTP and password-reset endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_db
from api.modules.auth.schemas.auth_schema import LoginResponse
from api.modules.auth.schemas.ops_schema import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    SendOTPRequest,
    VerifyOTPRequest,
)
from api.modules.auth.services.otp_service import OTPService
from api.modules.auth.services.password_service import PasswordService
from api.modules.auth.repositories.user_repo import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/otp/send", status_code=status.HTTP_202_ACCEPTED)
async def send_otp(body: SendOTPRequest, db: AsyncSession = Depends(get_db)):
    """Send OTP. Used for forgot-password, account-delete, phone-change, etc."""
    user_repo = UserRepository(db)
    user = (
        await user_repo.get_by_email(body.identifier)
        if "@" in body.identifier
        else await user_repo.get_by_mobile(body.identifier)
    )
    if user is None:
        # Return 202 even if not found — no user enumeration
        return {"detail": "If the account exists, OTP has been sent."}
    svc = OTPService(db)
    await svc.send_otp(user.id, body.identifier, body.purpose)
    return {"detail": "If the account exists, OTP has been sent."}


@router.post("/otp/verify", status_code=status.HTTP_200_OK)
async def verify_otp(body: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user = (
        await user_repo.get_by_email(body.identifier)
        if "@" in body.identifier
        else await user_repo.get_by_mobile(body.identifier)
    )
    if user is None:
        from shared.exceptions.auth_exceptions import OTPInvalidError
        raise OTPInvalidError()
    svc = OTPService(db)
    await svc.verify_otp(user.id, body.purpose, body.otp)
    return {"verified": True}


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(body: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    """Step 1: trigger OTP to mobile/email. Step 2: /otp/verify. Step 3: /reset-password."""
    user_repo = UserRepository(db)
    user = (
        await user_repo.get_by_email(body.identifier)
        if "@" in body.identifier
        else await user_repo.get_by_mobile(body.identifier)
    )
    if user is None:
        return {"detail": "If the account exists, OTP has been sent."}
    svc = OTPService(db)
    from api.modules.auth.models.otp import OTPPurpose
    await svc.send_otp(user.id, body.identifier, OTPPurpose.FORGOT_PASSWORD)
    return {"detail": "If the account exists, OTP has been sent."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(body: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    """After OTP verified, use the reset_token issued by /otp/verify to set new password."""
    svc = PasswordService(db)
    await svc.reset_password(body.reset_token, body.new_password)
    return {"detail": "Password updated. Please log in again."}
