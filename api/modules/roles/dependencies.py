"""RBAC FastAPI dependencies — used by ALL modules as the permission gate.

Usage in any router:
    @router.post("/attendance")
    async def mark_attendance(
        _perm=Depends(require_permission("attendance", "create", "class")),
        current_user: CurrentUser = ...,
    ):
        ...

Permission check order (all zero-DB for system roles):
  1. JWT scopes[] (pre-computed at login from PERMISSION_MAP)
  2. Wildcard expansion: module:*:*, *:action:*, *:*:scope, *:*:*
  3. Delegated permissions (DB check — only if user has active delegations)
"""
from __future__ import annotations
from typing import Callable
from fastapi import Depends, HTTPException, status

from api.core.dependencies import CurrentUser
from api.modules.roles.permissions import PERMISSION_MAP, get_permissions, has_permission


def require_permission(module: str, action: str, scope: str) -> Callable:
    """Factory — returns a FastAPI dependency that enforces one permission.

    Zero DB queries for system roles (permissions live in JWT scopes).
    """
    async def _check(current_user: CurrentUser) -> None:
        # Scopes embedded in JWT at login (includes wildcard-expanded system perms)
        jwt_scopes = set(current_user.scopes)

        # Fast path: check JWT scopes directly
        if has_permission(jwt_scopes, module, action, scope):
            return

        # Slower path: re-derive from roles (handles edge case where JWT is stale)
        role_perms = get_permissions(current_user.roles)
        if has_permission(role_perms, module, action, scope):
            return

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied: {module}:{action}:{scope}",
        )

    return Depends(_check)


def require_any_permission(*permission_tuples: tuple[str, str, str]) -> Callable:
    """At least ONE of the given permissions must be held.

    Usage: Depends(require_any_permission(
        ("attendance", "create", "class"),
        ("attendance", "create", "institution"),
    ))
    """
    async def _check(current_user: CurrentUser) -> None:
        jwt_scopes = set(current_user.scopes)
        role_perms = get_permissions(current_user.roles)
        all_perms = jwt_scopes | role_perms

        for mod, action, scope in permission_tuples:
            if has_permission(all_perms, mod, action, scope):
                return

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )

    return Depends(_check)


def require_scope_at_least(minimum_scope: str) -> Callable:
    """Ensure the user has at least a certain data scope.

    Scope hierarchy: own < class < dept < institution < group < platform
    """
    _ORDER = ("own", "class", "dept", "institution", "group", "platform")

    async def _check(current_user: CurrentUser) -> None:
        user_scopes = set(current_user.scopes)
        min_idx = _ORDER.index(minimum_scope) if minimum_scope in _ORDER else 99
        for scope_val in _ORDER[min_idx:]:
            if any(s.endswith(f":{scope_val}") for s in user_scopes):
                return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Requires at least '{minimum_scope}' scope",
        )

    return Depends(_check)
