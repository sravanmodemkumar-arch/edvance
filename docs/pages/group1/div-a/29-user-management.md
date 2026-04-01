# div-a-29 — User Management

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Platform staff users (internal) | ~20–50 |
| Institution admin users | ~4,000 (2 per institution avg) |
| Roles (platform staff) | exec / superadmin / ops / finance / compliance / security / content / oncall |
| Roles (institution) | institution_admin / institution_billing / institution_teacher |
| 2FA required roles | exec / superadmin / finance / compliance / security |
| SSO providers | Optional (Google Workspace, Azure AD) |
| Session timeout | 8h default |

**Why this matters:** User Management is the access control plane. A misconfigured role grants an ops engineer access to financial data. An orphaned account from a churned institution becomes a security risk. This page manages the complete lifecycle of every platform and institution user.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | User Management |
| Route | `/exec/users/` |
| Django view | `UserManagementView` |
| Template | `exec/user_management.html` |
| Priority | P1 |
| Nav group | Settings |
| Required role | `superadmin`, `ops` |
| 2FA required | Creating / editing / deactivating users |
| HTMX poll | None (on-demand) |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: User Management                     [+ Invite User] [Export Users]  │
├──────────┬──────────┬──────────┬──────────┬──────────────────────────────── ┤
│  Total   │  Active  │  Staff   │  Inst    │  Pending                        │
│  Users   │  Users   │  Users   │  Admins  │  Invites                        │
│  4,082   │  3,940   │   42     │  4,040   │    18                           │
├──────────┴──────────┴──────────┴──────────┴──────────────────────────────── ┤
│ TABS: [All Users] [Staff] [Institution Admins] [Pending Invites] [Sessions] │
├──────────────────────────────────────────────────────────────────────────────┤
│ [🔍 Search by name, email, role...]                                          │
│ [Role ▾] [Institution ▾] [Status ▾] [2FA ▾] [Last Login ▾]                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ [☐] [Bulk: Deactivate / Reset 2FA]  Showing 1–25 / 4,082  Sort: [Name ▾]  │
├──────────────────────────────────────────────────────────────────────────────┤
│ ☐ │ Name   │ Email          │ Role     │ Institution │ 2FA │ Last Login │ ⋯ │
│   │ Rahul K│ rahul@abc.in   │ Inst Admin│ ABC Coaching│  ✓  │ 2h ago    │   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Total Users | All users (staff + institution) | — |
| 2 | Active Users | Status = Active | — |
| 3 | Staff Users | Platform staff accounts | — |
| 4 | Institution Admins | Institution-level admin accounts | — |
| 5 | Pending Invites | Invite links not yet accepted | > 20 = amber |

---

### 4.2 Tab Bar

Tabs: All Users · Staff · Institution Admins · Pending Invites · Sessions
**Count badge on Pending Invites:** `ml-1.5 bg-[#F59E0B] text-black text-xs px-1.5 rounded-full`

---

### 4.3 Search & Filter Bar

**Search:** debounced 400ms on name, email, phone
**Filters:**
| Filter | Options |
|---|---|
| Role | Multi-select: all roles |
| Institution | Searchable dropdown |
| Status | Active / Inactive / Suspended / Pending |
| 2FA | Enabled / Disabled |
| Last Login | Any / Today / 7d / 30d / Never |

---

### 4.4 User Table

`id="user-table"` · `hx-get="?part=user_table"` on load

**Row click:** opens User Detail Drawer (§5.1)

#### Column Specifications

| Column | Sort | Width | Detail |
|---|---|---|---|
| ☐ | — | 40px | Checkbox |
| Name | ✓ | 160px | Full name |
| Email | ✓ | 200px | Email · `font-mono text-sm` |
| Role | ✓ | 130px | Role badge |
| Institution | ✓ | 180px | Name (for inst admins) or "Platform" (for staff) |
| 2FA | ✓ | 50px | ✓ green / ✗ red |
| Last Login | ✓ | 110px | Relative time or "Never" |
| Status | ✓ | 100px | Active/Inactive/Suspended badge |
| Actions ⋯ | — | 48px | View / Edit / Reset 2FA / Deactivate / Impersonate |

**Role badge colours:**
- superadmin: `bg-[#2E1065] text-[#A78BFA]`
- exec: `bg-[#1E3A5F] text-[#60A5FA]`
- ops: `bg-[#064E3B] text-[#34D399]`
- finance: `bg-[#451A03] text-[#FCD34D]`
- institution_admin: `bg-[#1E293B] text-[#94A3B8]`

**Inactive users:** `opacity-60`
**Suspended users:** row tint `bg-[#1A0A0A]`

**Pagination:** 25/page

---

### 4.5 Tab: Pending Invites

`id="tab-invites"` · `hx-get="?part=pending_invites"`

| Column | Detail |
|---|---|
| Invited email | Email |
| Role | Role badge |
| Institution | Name (or Platform) |
| Invited by | Username |
| Invited at | Timestamp |
| Expires at | Datetime · red if < 24h |
| Status | Pending / Expired |
| Actions ⋯ | Resend / Revoke |

---

### 4.6 Tab: Sessions

`id="tab-sessions"` · `hx-get="?part=active_sessions"`

**Purpose:** Active user sessions. Useful for security: see who is logged in from where.

| Column | Detail |
|---|---|
| User | Name + role |
| IP Address | `font-mono` |
| Location | City, State (GeoIP) |
| Device | Browser + OS |
| Started | Datetime |
| Last active | Relative time |
| Actions ⋯ | Terminate session |

**[Terminate All Sessions]** button · mass logout · requires 2FA

---

## 5. Drawers

### 5.1 User Detail Drawer (560 px)

`id="user-drawer"` · `body.drawer-open`

**Header:** User avatar (initial) + Name + Role badge + Status badge · `[×]`

**Tab bar (3 tabs):** Profile · Activity · Sessions

**Tab A — Profile:**
```
Full name    Rahul Kumar
Email        rahul@abc.in           [Copy]
Phone        +91 98765 43210        [Copy]
Role         Institution Admin
Institution  ABC Coaching Centre
Status       Active
2FA          Enabled ✓
Created      01 Jan 2024
Last login   2 hours ago
```

**Edit mode:** [Edit ✎] → inline form fields editable
Editable fields: name · phone · role (restricted by current user's permissions)

**Section — Danger actions (role: superadmin only):**
[Reset 2FA] [Suspend Account] [Delete Account]

**Tab B — Activity (last 30 days):**
- Logins: count + last 5 login timestamps + IP
- Actions taken: count (from audit log)
- Pages visited: top 5
- Mini chart: daily activity (bar, 30 days)

**Tab C — Sessions:**
Active sessions for this user (same columns as §4.6)
[Terminate All This User's Sessions] button

**Footer:** [Save Changes] [Suspend] [Close]

---

## 6. Modals

### 6.1 Invite User Modal (560 px)

**2FA required.**

| Field | Type | Validation |
|---|---|---|
| Email | Email input | Required · uniqueness check |
| Full name | Text | Required |
| Role | Select | Restricted by current user's role |
| Institution | Searchable dropdown | Required if role = institution_admin |
| Phone | Tel | Optional |
| Send invite email | Checkbox | Default: On |
| Expiry | Select | 24h / 48h / 7d | Default: 48h |

**Role selection restriction:** A `ops` user can only invite up to `ops` role. Only `superadmin` can invite `superadmin` or `exec`.

**Footer:** [Cancel] [Send Invitation]

---

### 6.2 Deactivate User Modal (480 px)

**2FA required.**
"Deactivate {Name}?"
- Reason: required text
- Terminate active sessions: checkbox (default: On)
- Revoke API keys (if any): checkbox

**Footer:** [Cancel] [Deactivate Account]

---

### 6.3 Reset 2FA Modal (480 px)

**2FA required.**
"Reset 2FA for {Name}?"
"This will require {Name} to set up 2FA again on their next login."
- Reason: required
- Notify user by email: checkbox

**Footer:** [Cancel] [Reset 2FA]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/users_kpi.html` | Page load |
| `?part=user_table` | `exec/partials/user_table.html` | Load · search · filter · tab · page |
| `?part=pending_invites` | `exec/partials/pending_invites.html` | Tab click |
| `?part=active_sessions` | `exec/partials/user_sessions.html` | Tab click |
| `?part=user_drawer&id={id}` | `exec/partials/user_drawer.html` | Row click |

**Django view dispatch:**
```python
class UserManagementView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.manage_users"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/users_kpi.html",
                "user_table": "exec/partials/user_table.html",
                "pending_invites": "exec/partials/pending_invites.html",
                "active_sessions": "exec/partials/user_sessions.html",
                "user_drawer": "exec/partials/user_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/user_management.html", ctx)

    def post(self, request):
        part = request.GET.get("part", "")
        handlers = {
            "invite_user": self._handle_invite,
            "deactivate_user": self._handle_deactivate,
            "reset_2fa": self._handle_reset_2fa,
            "terminate_session": self._handle_terminate_session,
        }
        if part in handlers:
            return handlers[part](request)
        return HttpResponseNotAllowed(["GET"])
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 200 ms | > 500 ms |
| User table (25 rows) | < 400 ms | > 1 s |
| User drawer | < 250 ms | > 700 ms |
| Full page initial load | < 1 s | > 2.5 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| User with no 2FA (role requiring it) | Red `✗` badge + alert icon in 2FA column + warning in drawer |
| Churned institution admin still active | Amber badge "Institution suspended/churned — review access" in drawer |
| Invite expired | Status = Expired · [Resend] option creates new invite |
| Deactivate own account | Error "You cannot deactivate your own account" |
| Only superadmin in system | Cannot deactivate last superadmin · error "At least one superadmin required" |
| Impersonate: acts as institution admin | Full audit log entry "Impersonated by {user}" + session banner for impersonating user |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `N` | Invite user |
| `F` | Focus search |
| `1`–`5` | Switch tabs |
| `↑` / `↓` | Navigate rows |
| `Enter` | Open user drawer |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/user_management.html` | Full page shell |
| `exec/partials/users_kpi.html` | KPI strip |
| `exec/partials/user_table.html` | User table + pagination |
| `exec/partials/pending_invites.html` | Pending invites table |
| `exec/partials/user_sessions.html` | Active sessions table |
| `exec/partials/user_drawer.html` | User detail drawer |
| `exec/partials/invite_user_modal.html` | Invite modal |
| `exec/partials/deactivate_user_modal.html` | Deactivate modal |
| `exec/partials/reset_2fa_modal.html` | Reset 2FA modal |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `TabBar` | §4.2 |
| `SearchInput` | §4.3 |
| `FilterBar` | §4.3 |
| `UserTable` | §4.4 |
| `RoleBadge` | §4.4 |
| `TwoFAIndicator` | §4.4 |
| `PendingInvitesTable` | §4.5 |
| `SessionsTable` | §4.6 |
| `DrawerPanel` | §5.1 |
| `UserActivityChart` | §5.1 Tab B |
| `ModalDialog` | §6.1–6.3 |
| `PaginationStrip` | §4.4 |
