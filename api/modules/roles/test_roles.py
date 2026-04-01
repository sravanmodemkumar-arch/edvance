"""Module 03 RBAC tests — permission map, hierarchy, delegation, templates."""
from __future__ import annotations
import pytest
from pydantic import ValidationError
from unittest.mock import AsyncMock, MagicMock, patch

from api.modules.roles.permissions import (
    PERMISSION_MAP, get_permissions, has_permission,
    VIEW, CREATE, EDIT, DELETE, APPROVE, EXPORT, BULK, PUBLISH,
    OWN, CLASS, DEPT, INSTITUTION, GROUP, PLATFORM,
)
from api.modules.roles.schemas.role_schema import CustomRoleCreate, DelegationCreate
from api.modules.roles.services.rbac_service import RBACService, _HIERARCHY


# ─── Permission map coverage ──────────────────────────────────────────────────

class TestPermissionMap:
    def test_all_11_role_groups_present(self):
        expected = {
            "PLATFORM_ADMIN", "GROUP_ADMIN", "MANAGEMENT", "PRINCIPAL",
            "VICE_PRINCIPAL", "HOD", "EXAM_CELL_HEAD", "CLASS_TEACHER",
            "SUBJECT_TEACHER", "LIBRARIAN", "ACCOUNTANT", "COUNSELLOR",
            "HOSTEL_WARDEN", "NURSE", "GATE_STAFF",
            "OWNER", "CENTER_DIRECTOR", "ACADEMIC_HEAD", "BATCH_COORDINATOR", "FACULTY",
            "STUDENT", "PARENT", "B2B_PARTNER", "TSP_ADMIN",
        }
        for role in expected:
            assert role in PERMISSION_MAP, f"Missing role: {role}"

    def test_platform_admin_is_wildcard(self):
        perms = PERMISSION_MAP["PLATFORM_ADMIN"]
        assert "*:*:platform" in perms

    def test_student_cannot_create_attendance(self):
        perms = get_permissions(["STUDENT"])
        assert not has_permission(perms, "attendance", CREATE, CLASS)

    def test_class_teacher_can_create_attendance_for_class(self):
        perms = get_permissions(["CLASS_TEACHER"])
        assert has_permission(perms, "attendance", CREATE, CLASS)

    def test_class_teacher_cannot_export_institution(self):
        perms = get_permissions(["CLASS_TEACHER"])
        assert not has_permission(perms, "attendance", EXPORT, INSTITUTION)

    def test_principal_can_do_everything_at_institution(self):
        perms = get_permissions(["PRINCIPAL"])
        for action in (VIEW, CREATE, EDIT, APPROVE, EXPORT, BULK):
            assert has_permission(perms, "attendance", action, INSTITUTION), \
                f"Principal should have attendance:{action}:institution"

    def test_multi_role_union(self):
        perms = get_permissions(["SUBJECT_TEACHER", "ACCOUNTANT"])
        # Subject teacher perm
        assert has_permission(perms, "marks", CREATE, OWN)
        # Accountant perm
        assert has_permission(perms, "fee", EXPORT, INSTITUTION)

    def test_parent_cannot_see_other_students(self):
        perms = get_permissions(["PARENT"])
        assert not has_permission(perms, "students", VIEW, CLASS)
        assert has_permission(perms, "attendance", VIEW, OWN)


# ─── Wildcard expansion ────────────────────────────────────────────────────────

class TestWildcardExpansion:
    def test_wildcard_module_matches_any(self):
        perms = {"*:view:institution"}
        assert has_permission(perms, "fee", VIEW, INSTITUTION)
        assert has_permission(perms, "attendance", VIEW, INSTITUTION)

    def test_wildcard_all_matches_specific(self):
        perms = {"*:*:platform"}
        assert has_permission(perms, "fee", DELETE, INSTITUTION)
        assert has_permission(perms, "anything", CREATE, OWN)

    def test_no_permission_correctly_denied(self):
        perms: set[str] = set()
        assert not has_permission(perms, "fee", CREATE, INSTITUTION)


# ─── Role hierarchy ───────────────────────────────────────────────────────────

class TestRoleHierarchy:
    def test_principal_above_hod(self):
        assert _HIERARCHY["PRINCIPAL"] < _HIERARCHY["HOD"]

    def test_hod_above_subject_teacher(self):
        assert _HIERARCHY["HOD"] < _HIERARCHY["SUBJECT_TEACHER"]

    def test_student_has_high_number(self):
        assert _HIERARCHY["STUDENT"] > _HIERARCHY["PRINCIPAL"]

    @pytest.mark.asyncio
    async def test_hod_cannot_assign_principal(self):
        from fastapi import HTTPException
        mock_session = AsyncMock()
        svc = RBACService(mock_session)

        with pytest.raises(HTTPException) as exc_info:
            await svc.assign_role(
                tenant_id=1, target_user_id=99, role_code="PRINCIPAL",
                assigner_user_id=10, assigner_roles=["HOD"],
            )
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_principal_can_assign_subject_teacher(self):
        from fastapi import HTTPException
        mock_session = AsyncMock()
        svc = RBACService(mock_session)

        mock_role = MagicMock()
        mock_role.id = 5

        with patch.object(svc._role_repo, "get_by_code", return_value=mock_role), \
             patch.object(svc._assign_repo, "assign", new_callable=AsyncMock), \
             patch.object(svc._role_repo, "log_change", new_callable=AsyncMock):
            # Should not raise
            await svc.assign_role(
                tenant_id=1, target_user_id=50, role_code="SUBJECT_TEACHER",
                assigner_user_id=10, assigner_roles=["PRINCIPAL"],
            )


# ─── Custom role schema validation ────────────────────────────────────────────

class TestCustomRoleSchema:
    def test_valid_role_code(self):
        r = CustomRoleCreate(
            name="Senior Librarian", code="SENIOR_LIBRARIAN",
            role_group="SCHOOL", hierarchy_level=44,
            permissions=["library:view:institution", "library:create:institution"],
        )
        assert r.code == "SENIOR_LIBRARIAN"

    def test_invalid_code_lowercase(self):
        with pytest.raises(ValidationError):
            CustomRoleCreate(
                name="Test", code="senior_lib",
                role_group="SCHOOL", hierarchy_level=44,
                permissions=["library:view:institution"],
            )

    def test_invalid_permission_format(self):
        with pytest.raises(ValidationError):
            CustomRoleCreate(
                name="Test", code="TEST_ROLE",
                role_group="SCHOOL", hierarchy_level=44,
                permissions=["invalid-format"],
            )


# ─── Delegation validation ────────────────────────────────────────────────────

class TestDelegation:
    @pytest.mark.asyncio
    async def test_cannot_delegate_permission_not_held(self):
        from fastapi import HTTPException
        mock_session = AsyncMock()
        svc = DelegationService(mock_session)

        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)

        with pytest.raises(HTTPException) as exc_info:
            await svc.create_delegation(
                tenant_id=1, delegator_user_id=1,
                delegator_roles=["ACCOUNTANT"],  # accountant has no attendance:create
                delegate_user_id=2,
                permissions_to_delegate=["attendance:create:institution"],
                starts_at=now, ends_at=now + timedelta(days=1),
            )
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_ends_before_starts_rejected(self):
        from fastapi import HTTPException
        mock_session = AsyncMock()
        svc = DelegationService(mock_session)

        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)

        with pytest.raises(HTTPException) as exc_info:
            await svc.create_delegation(
                tenant_id=1, delegator_user_id=1,
                delegator_roles=["PRINCIPAL"],
                delegate_user_id=2,
                permissions_to_delegate=["attendance:view:institution"],
                starts_at=now + timedelta(days=1),
                ends_at=now,
            )
        assert exc_info.value.status_code == 422


# ─── Lazy import fix ─────────────────────────────────────────────────────────

def test_delegation_service_importable():
    from api.modules.roles.services.delegation_service import DelegationService
    assert DelegationService is not None


from api.modules.roles.services.delegation_service import DelegationService
