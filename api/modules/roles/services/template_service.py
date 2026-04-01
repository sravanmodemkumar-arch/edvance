"""Role template service — seeds pre-built roles when a tenant is provisioned."""
from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from api.modules.roles.models.role import Role, RoleGroup
from api.modules.roles.permissions import PERMISSION_MAP

# Maps institution type → list of (code, display_name, group, hierarchy_level)
_SCHOOL_ROLES = [
    ("MANAGEMENT",      "Management",       RoleGroup.SCHOOL, 10),
    ("PRINCIPAL",       "Principal",        RoleGroup.SCHOOL, 20),
    ("VICE_PRINCIPAL",  "Vice Principal",   RoleGroup.SCHOOL, 25),
    ("HOD",             "Head of Dept",     RoleGroup.SCHOOL, 30),
    ("EXAM_CELL_HEAD",  "Exam Cell Head",   RoleGroup.SCHOOL, 30),
    ("CLASS_TEACHER",   "Class Teacher",    RoleGroup.SCHOOL, 40),
    ("SUBJECT_TEACHER", "Subject Teacher",  RoleGroup.SCHOOL, 40),
    ("LIBRARIAN",       "Librarian",        RoleGroup.SCHOOL, 45),
    ("ACCOUNTANT",      "Accountant",       RoleGroup.SCHOOL, 45),
    ("COUNSELLOR",      "Counsellor",       RoleGroup.SCHOOL, 45),
    ("NURSE",           "Nurse",            RoleGroup.SCHOOL, 45),
    ("HOSTEL_WARDEN",   "Hostel Warden",    RoleGroup.SCHOOL, 45),
    ("GATE_STAFF",      "Gate Staff",       RoleGroup.SCHOOL, 50),
]

_COACHING_ROLES = [
    ("OWNER",            "Owner",            RoleGroup.COACHING, 20),
    ("CENTER_DIRECTOR",  "Center Director",  RoleGroup.COACHING, 30),
    ("ACADEMIC_HEAD",    "Academic Head",    RoleGroup.COACHING, 30),
    ("BATCH_COORDINATOR","Batch Coordinator",RoleGroup.COACHING, 40),
    ("FACULTY",          "Faculty",          RoleGroup.COACHING, 40),
    ("ACCOUNTANT",       "Accountant",       RoleGroup.COACHING, 45),
]

_COLLEGE_ROLES = [
    ("MANAGEMENT",      "Management",       RoleGroup.COLLEGE, 10),
    ("PRINCIPAL",       "Principal",        RoleGroup.COLLEGE, 20),
    ("DEAN",            "Dean",             RoleGroup.COLLEGE, 25),
    ("HOD",             "Head of Dept",     RoleGroup.COLLEGE, 30),
    ("PROFESSOR",       "Professor",        RoleGroup.COLLEGE, 40),
    ("LAB_INCHARGE",    "Lab Incharge",     RoleGroup.COLLEGE, 40),
    ("LIBRARIAN",       "Librarian",        RoleGroup.COLLEGE, 45),
    ("ACCOUNTANT",      "Accountant",       RoleGroup.COLLEGE, 45),
    ("HOSTEL_WARDEN",   "Hostel Warden",    RoleGroup.COLLEGE, 45),
]

_SHARED_ROLES = [
    ("STUDENT",         "Student",          RoleGroup.STUDENT,  80),
    ("PARENT",          "Parent",           RoleGroup.PARENT,   80),
]

_TEMPLATES = {
    "SCHOOL":   _SCHOOL_ROLES + _SHARED_ROLES,
    "COLLEGE":  _COLLEGE_ROLES + _SHARED_ROLES,
    "COACHING": _COACHING_ROLES + _SHARED_ROLES,
    "GROUP":    [("GROUP_ADMIN", "Group Admin", RoleGroup.GROUP, 5)],
}


class RoleTemplateService:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def apply_template(self, tenant_id: int, institution_type: str) -> None:
        """Seed all system roles for this institution type. Idempotent."""
        rows = _TEMPLATES.get(institution_type.upper(), _SHARED_ROLES)
        for code, name, group, level in rows:
            role = Role(
                tenant_id=tenant_id,
                name=name,
                code=code,
                role_group=group,
                hierarchy_level=level,
                is_system=True,
                is_active=True,
                permissions=list(PERMISSION_MAP.get(code, set())),
            )
            self._s.add(role)
        await self._s.flush()
