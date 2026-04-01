"""Token payload schema — shared across all services for JWT decoding."""
from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str                          # "usr_abc123"
    tenant_id: str                    # "sch_0501"
    institution_type: str             # SCHOOL | COACHING | HOSTEL | PLATFORM
    roles: list[str]                  # ["TEACHER", "COORDINATOR"]
    scopes: list[str]                 # ["read:students", "write:attendance"]
    session_id: str                   # opaque session reference
    exp: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 900             # seconds (15 min)
