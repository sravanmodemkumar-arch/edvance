"""Platform permission map — hardcoded for all system roles.

Permission format: "{module}:{action}:{scope}"
Stored in JWT scopes[] at login — zero DB queries per request.

Scopes:  own | class | dept | institution | group | platform
Actions: view | create | edit | delete | approve | export | bulk | publish
Modules: attendance | marks | timetable | fee | library | hostel | transport |
         homework | syllabus | exam | results | admission | staff | students |
         parents | announcements | notifications | documents | compliance |
         reports | settings | roles | billing | live_classes | ai | whatsapp
"""
from __future__ import annotations

# ─── Scope constants ──────────────────────────────────────────────────────────
OWN = "own"
CLASS = "class"
DEPT = "dept"
INSTITUTION = "institution"
GROUP = "group"
PLATFORM = "platform"

# ─── Action constants ─────────────────────────────────────────────────────────
VIEW = "view"
CREATE = "create"
EDIT = "edit"
DELETE = "delete"
APPROVE = "approve"
EXPORT = "export"
BULK = "bulk"
PUBLISH = "publish"

# ─── Module constants ─────────────────────────────────────────────────────────
MOD_ALL = "*"


def _p(module: str, action: str, scope: str) -> str:
    return f"{module}:{action}:{scope}"


def _all_actions(module: str, scope: str) -> list[str]:
    return [_p(module, a, scope) for a in (VIEW, CREATE, EDIT, EXPORT, BULK)]


# ─── System role → permission set ────────────────────────────────────────────
PERMISSION_MAP: dict[str, set[str]] = {

    # ── Platform ──────────────────────────────────────────────────────────────
    "PLATFORM_ADMIN": {f"*:*:{PLATFORM}"},

    # ── Institution group ─────────────────────────────────────────────────────
    "GROUP_ADMIN": {
        _p("*", VIEW, GROUP), _p("*", EXPORT, GROUP), _p("*", BULK, GROUP),
        _p("announcements", CREATE, GROUP), _p("announcements", PUBLISH, GROUP),
        _p("reports", VIEW, GROUP), _p("reports", EXPORT, GROUP),
        _p("compliance", VIEW, GROUP),
    },

    # ── School ────────────────────────────────────────────────────────────────
    "MANAGEMENT": {
        _p("*", VIEW, INSTITUTION), _p("*", EXPORT, INSTITUTION),
        _p("fee", APPROVE, INSTITUTION), _p("staff", APPROVE, INSTITUTION),
        _p("billing", VIEW, INSTITUTION), _p("settings", EDIT, INSTITUTION),
        _p("compliance", VIEW, INSTITUTION), _p("reports", VIEW, INSTITUTION),
    },
    "PRINCIPAL": {
        _p("*", VIEW, INSTITUTION), _p("*", CREATE, INSTITUTION),
        _p("*", EDIT, INSTITUTION), _p("*", EXPORT, INSTITUTION),
        _p("*", APPROVE, INSTITUTION), _p("*", BULK, INSTITUTION),
        _p("results", PUBLISH, INSTITUTION),
        _p("roles", CREATE, INSTITUTION), _p("roles", EDIT, INSTITUTION),
        _p("announcements", PUBLISH, INSTITUTION),
    },
    "VICE_PRINCIPAL": {
        _p("students", VIEW, INSTITUTION), _p("attendance", VIEW, INSTITUTION),
        _p("marks", VIEW, INSTITUTION), _p("homework", VIEW, INSTITUTION),
        _p("compliance", VIEW, INSTITUTION), _p("exam", VIEW, INSTITUTION),
        _p("announcements", CREATE, INSTITUTION),
        _p("students", EDIT, INSTITUTION),  # with Principal approval
    },
    "HOD": {
        _p("attendance", VIEW, DEPT), _p("attendance", APPROVE, DEPT),
        _p("marks", VIEW, DEPT), _p("marks", APPROVE, DEPT),
        _p("staff", VIEW, DEPT), _p("students", VIEW, DEPT),
        _p("timetable", VIEW, DEPT), _p("homework", VIEW, DEPT),
        _p("announcements", CREATE, DEPT),
        _p("roles", CREATE, DEPT),   # assign subject teachers to own dept
    },
    "EXAM_CELL_HEAD": {
        _p("exam", VIEW, INSTITUTION), _p("exam", CREATE, INSTITUTION),
        _p("exam", EDIT, INSTITUTION), _p("exam", APPROVE, INSTITUTION),
        _p("exam", PUBLISH, INSTITUTION), _p("exam", BULK, INSTITUTION),
        _p("results", VIEW, INSTITUTION), _p("results", PUBLISH, INSTITUTION),
        _p("students", VIEW, INSTITUTION),
    },
    "CLASS_TEACHER": {
        _p("attendance", CREATE, CLASS), _p("attendance", VIEW, CLASS),
        _p("attendance", EDIT, CLASS),   # 24-hour correction window
        _p("marks", CREATE, CLASS), _p("marks", VIEW, CLASS),
        _p("homework", CREATE, CLASS), _p("homework", VIEW, CLASS),
        _p("students", VIEW, CLASS), _p("parents", VIEW, CLASS),
        _p("announcements", CREATE, CLASS),
    },
    "SUBJECT_TEACHER": {
        _p("attendance", CREATE, CLASS), _p("attendance", VIEW, CLASS),
        _p("marks", CREATE, OWN), _p("marks", VIEW, OWN),
        _p("homework", CREATE, CLASS), _p("homework", VIEW, CLASS),
        _p("syllabus", CREATE, OWN), _p("syllabus", EDIT, OWN),
        _p("students", VIEW, CLASS),
    },
    "LIBRARIAN": {
        _p("library", VIEW, INSTITUTION), _p("library", CREATE, INSTITUTION),
        _p("library", EDIT, INSTITUTION), _p("library", EXPORT, INSTITUTION),
    },
    "ACCOUNTANT": {
        _p("fee", VIEW, INSTITUTION), _p("fee", CREATE, INSTITUTION),
        _p("fee", EXPORT, INSTITUTION), _p("fee", BULK, INSTITUTION),
        _p("staff", VIEW, INSTITUTION),   # payroll view only
        _p("reports", VIEW, INSTITUTION), _p("reports", EXPORT, INSTITUTION),
    },
    "COUNSELLOR": {
        _p("students", VIEW, INSTITUTION),
        _p("compliance", CREATE, INSTITUTION),  # welfare records
        _p("parents", VIEW, INSTITUTION),
        _p("announcements", VIEW, INSTITUTION),
    },
    "HOSTEL_WARDEN": {
        _p("hostel", VIEW, INSTITUTION), _p("hostel", CREATE, INSTITUTION),
        _p("hostel", EDIT, INSTITUTION),
        _p("students", VIEW, INSTITUTION),
        _p("attendance", CREATE, INSTITUTION),  # hostel attendance
        _p("announcements", CREATE, INSTITUTION),
    },
    "NURSE": {
        _p("compliance", CREATE, INSTITUTION),  # medical records
        _p("students", VIEW, INSTITUTION),
    },
    "GATE_STAFF": {
        _p("students", VIEW, INSTITUTION),   # exit verification
        _p("parents", VIEW, INSTITUTION),    # photo verification
    },

    # ── Coaching ──────────────────────────────────────────────────────────────
    "OWNER": {
        _p("*", VIEW, INSTITUTION), _p("*", CREATE, INSTITUTION),
        _p("*", EDIT, INSTITUTION), _p("*", EXPORT, INSTITUTION),
        _p("*", APPROVE, INSTITUTION), _p("*", BULK, INSTITUTION),
    },
    "CENTER_DIRECTOR": {
        _p("students", VIEW, INSTITUTION), _p("staff", VIEW, INSTITUTION),
        _p("attendance", VIEW, INSTITUTION), _p("marks", VIEW, INSTITUTION),
        _p("fee", VIEW, INSTITUTION), _p("timetable", VIEW, INSTITUTION),
        _p("reports", VIEW, INSTITUTION),
    },
    "ACADEMIC_HEAD": {
        _p("exam", VIEW, INSTITUTION), _p("exam", CREATE, INSTITUTION),
        _p("exam", EDIT, INSTITUTION), _p("exam", PUBLISH, INSTITUTION),
        _p("syllabus", VIEW, INSTITUTION), _p("syllabus", EDIT, INSTITUTION),
        _p("staff", VIEW, INSTITUTION), _p("roles", CREATE, DEPT),
    },
    "BATCH_COORDINATOR": {
        _p("attendance", CREATE, CLASS), _p("attendance", VIEW, CLASS),
        _p("timetable", VIEW, CLASS), _p("timetable", EDIT, CLASS),
        _p("announcements", CREATE, CLASS),
        _p("students", VIEW, CLASS),
    },
    "FACULTY": {
        _p("attendance", CREATE, CLASS), _p("attendance", VIEW, CLASS),
        _p("marks", CREATE, OWN), _p("marks", VIEW, OWN),
        _p("homework", CREATE, CLASS), _p("homework", VIEW, CLASS),
        _p("students", VIEW, CLASS),
    },

    # ── Students / Parents ────────────────────────────────────────────────────
    "STUDENT": {
        _p("attendance", VIEW, OWN), _p("marks", VIEW, OWN),
        _p("timetable", VIEW, OWN), _p("homework", VIEW, OWN),
        _p("results", VIEW, OWN), _p("syllabus", VIEW, OWN),
        _p("fee", VIEW, OWN), _p("library", VIEW, OWN),
        _p("announcements", VIEW, INSTITUTION),
        _p("documents", VIEW, OWN),
    },
    "PARENT": {
        _p("attendance", VIEW, OWN),  # own child
        _p("marks", VIEW, OWN), _p("fee", VIEW, OWN),
        _p("timetable", VIEW, OWN), _p("homework", VIEW, OWN),
        _p("announcements", VIEW, INSTITUTION),
        _p("documents", VIEW, OWN),
    },

    # ── External ──────────────────────────────────────────────────────────────
    "B2B_PARTNER": {_p("*", VIEW, OWN)},   # scoped to API key grants
    "TSP_ADMIN": {
        _p("exam", CREATE, INSTITUTION), _p("exam", EDIT, INSTITUTION),
        _p("exam", PUBLISH, INSTITUTION),
        _p("results", VIEW, INSTITUTION),
    },
}


def get_permissions(roles: list[str]) -> set[str]:
    """Return union of all permissions for the given role names."""
    perms: set[str] = set()
    for role in roles:
        perms |= PERMISSION_MAP.get(role.upper(), set())
    return perms


def has_permission(perms: set[str], module: str, action: str, scope: str) -> bool:
    """Check if a permission set grants module:action:scope.

    Supports wildcard '*' in any dimension.
    """
    candidates = [
        f"{module}:{action}:{scope}",
        f"{module}:{action}:*",
        f"{module}:*:{scope}",
        f"*:{action}:{scope}",
        f"{module}:*:*",
        f"*:*:{scope}",
        f"*:{action}:*",
        f"*:*:*",
        # Platform admin shorthand
        f"*:*:{PLATFORM}",
    ]
    return any(c in perms for c in candidates)
