"""Role and assignment schemas."""
from __future__ import annotations
import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from api.modules.roles.models.role import RoleGroup

_CODE_RE = re.compile(r"^[A-Z][A-Z0-9_]{1,38}[A-Z0-9]$")
_PERM_RE = re.compile(r"^[\w\*]+:[\w\*]+:[\w\*]+$")


class RoleOut(BaseModel):
    id: int
    name: str
    code: str
    role_group: RoleGroup
    hierarchy_level: int
    is_system: bool
    is_active: bool
    permissions: list[str] | None
    description: str | None

    model_config = {"from_attributes": True}


class CustomRoleCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    code: str = Field(..., description="UPPER_SNAKE_CASE e.g. SENIOR_LIBRARIAN")
    role_group: RoleGroup
    hierarchy_level: int = Field(..., ge=10, le=90)
    permissions: list[str] = Field(..., min_length=1)
    description: str | None = None

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not _CODE_RE.match(v):
            raise ValueError("Code must be UPPER_SNAKE_CASE, 3-40 chars")
        return v

    @field_validator("permissions")
    @classmethod
    def validate_perms(cls, v: list[str]) -> list[str]:
        for p in v:
            if not _PERM_RE.match(p):
                raise ValueError(f"Invalid permission format '{p}'. Use module:action:scope")
        return v


class AssignRoleRequest(BaseModel):
    target_user_id: int
    role_code: str
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    scope_context: dict | None = None
    reason: str | None = None


class RevokeRoleRequest(BaseModel):
    assignment_id: int
    target_user_id: int
    role_code: str
    reason: str | None = None


class DelegationCreate(BaseModel):
    delegate_user_id: int
    permissions: list[str] = Field(..., min_length=1)
    starts_at: datetime
    ends_at: datetime
    reason: str | None = None

    @field_validator("permissions")
    @classmethod
    def validate_perms(cls, v: list[str]) -> list[str]:
        for p in v:
            if not _PERM_RE.match(p):
                raise ValueError(f"Invalid permission format: {p}")
        return v


class AcknowledgeRequest(BaseModel):
    assignment_id: int
