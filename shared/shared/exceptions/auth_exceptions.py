"""Auth-related HTTP exceptions."""
from fastapi import HTTPException, status


class InvalidTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidCredentialsError(HTTPException):
    """Wrong password OR user not found in tenant — same message (no enumeration)."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class AccountLockedError(HTTPException):
    def __init__(self, minutes: int = 15):
        super().__init__(
            status_code=status.HTTP_423_LOCKED,
            detail=f"Account locked. Try again in {minutes} minutes.",
        )


class AccountDisabledError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled. Contact your institution admin.",
        )


class OTPExpiredError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_410_GONE,
            detail="OTP has expired. Please request a new one.",
        )


class OTPInvalidError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP.",
        )


class InsufficientPermissionsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


class NotFoundError(HTTPException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
        )


class RateLimitError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )
