"""Token payload schema — shared across all services for JWT decoding."""
from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str        # user_id
    role: str       # student | staff | admin | platform_admin
    inst: int | None = None  # institution_id (None for platform users)
    exp: int


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
