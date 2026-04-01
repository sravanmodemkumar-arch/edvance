# div-a-30 — Role & Permissions

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Platform roles | 8 (exec / superadmin / ops / finance / compliance / security / content / oncall) |
| Institution roles | 3 (institution_admin / institution_billing / institution_teacher) |
| Permissions total | ~120 discrete permissions |
| Permission groups | ~15 groups |
| Custom role support | Yes (for institution-level custom roles) |

**Why this matters:** Role & Permissions is the authorisation matrix. A finance user who can accidentally access compliance data is a DPDPA violation. A support engineer who can mark invoices as paid is a financial risk. This page manages the complete permission map — who can see and do what.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Role & Permissions |
| Route | `/exec/roles/` |
| Django view | `RolesPermissionsView` |
| Template | `exec/roles_permissions.html` |
| Priority | P2 |
| Nav group | Settings |
| Required role | `superadmin` only |
| 2FA required | All role edits |
| HTMX poll | None |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Role & Permissions                           [+ New Custom Role]    │
├──────────────────────────────────────────────────────────────────────────────┤
│ TABS: [Platform Roles] [Institution Roles] [Permission Matrix] [Audit]      │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: PLATFORM ROLES                                                          │
│ Role cards (8 roles) with user count + key permissions + [Edit]             │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 Tab: Platform Roles

`id="tab-platform-roles"` · `hx-get="?part=platform_roles"`

**Role cards grid:** `grid grid-cols-4 gap-4 p-4`

Each role card `bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-5`:
```
┌───────────────────────────────────┐
│ 🔑 superadmin              2 users│
│                                   │
│ Full platform access               │
│ All permissions                   │
│                                   │
│ Key permissions:                  │
│ ✓ Manage platform settings        │
│ ✓ Create/delete users             │
│ ✓ View all financial data         │
│ ✓ Access audit logs               │
│ [+ 116 more]                      │
│                                   │
│ [Edit Role] [View Users]          │
└───────────────────────────────────┘
```

**System roles** (exec, superadmin): edit button visible but limited — cannot remove core permissions
**Custom roles:** fully editable

**[Edit Role]:** opens Role Edit Drawer (§5.1) · 2FA required

---

### 4.2 Tab: Institution Roles

`id="tab-inst-roles"` · `hx-get="?part=institution_roles"`

Same layout as §4.1 but for 3 institution roles:
- institution_admin: full institution access
- institution_billing: billing + invoices only
- institution_teacher: exam creation + student management

**Custom institution roles:** institutions can define their own roles (up to 5 custom roles per institution). Platform ops can see and override these.

---

### 4.3 Tab: Permission Matrix

`id="tab-matrix"` · `hx-get="?part=permission_matrix"`

**Full permissions matrix table:**
- **Rows:** Permissions (grouped by domain: Dashboard / Exams / Students / Billing / Users / Settings / Compliance / Security)
- **Columns:** Roles (8 platform roles + 3 institution roles)
- **Cell:** ✓ `text-[#34D399]` or ✗ `text-[#EF4444]` or `—` (N/A)

**Domain group headers:** sticky rows `bg-[#070C18] text-[#6366F1] text-xs uppercase font-semibold`

**Permissions sample by domain:**

*Dashboard:*
- view_exec_dashboard · view_analytics · export_reports

*Exams:*
- view_exams · create_exams · cancel_exams · publish_results · revise_answer_key

*Billing:*
- view_billing · mark_invoice_paid · write_off_invoice · generate_invoice

*Users:*
- view_users · invite_users · deactivate_users · reset_2fa

*Settings:*
- manage_platform_settings · manage_api_keys · manage_feature_flags

*Compliance:*
- view_audit_log · view_compliance · view_security_events · export_audit_log

**[Edit Matrix]:** toggleable edit mode — turn any cell ✓/✗ by clicking (2FA required to save)

**[Export Matrix]:** download as XLSX

---

### 4.4 Tab: Audit (Role Changes)

`id="tab-role-audit"` · `hx-get="?part=role_audit"`

**Purpose:** History of all role and permission changes.

| Column | Detail |
|---|---|
| Timestamp | Datetime |
| Changed by | Username |
| Change type | Role created / Permission added / Permission removed / Role assigned to user |
| Target | Role name or User |
| Before | Previous state |
| After | New state |
| Reason | Text |

**Pagination:** 25/page · sort by timestamp desc

---

## 5. Drawers

### 5.1 Role Edit Drawer (720 px)

`id="role-drawer"` · `w-[720px]` · `body.drawer-open`
**2FA required to save.**

**Header:** Role name + badge + "Edit Role" · `[×]`

**Section A — Role Metadata:**
- Role name: text (editable for custom roles, read-only for system roles)
- Description: textarea
- Colour: colour picker (for badge display)
- Icon: icon picker (emoji or SVG)

**Section B — Permissions Checklist:**
Grouped by domain with expandable sections:
```
▼ Dashboard (3/3 permissions)
   ☑ view_exec_dashboard
   ☑ view_analytics
   ☑ export_reports

▼ Exams (4/6 permissions)
   ☑ view_exams
   ☑ create_exams
   ☑ cancel_exams
   ☐ revise_answer_key  ← locked for this role
   ☑ publish_results
   ☐ bulk_export_results
```
- Locked permissions (system role core): shown with lock icon, not toggleable
- `accent-[#6366F1]` for checkboxes

**Section C — Users with this role:**
Mini table: Name · Email · Last login (5 rows + "View all N →" link)

**Footer:** [Discard] [Save Role Changes] (2FA enforced)

---

## 6. Modals

### 6.1 New Custom Role Modal (560 px)

**2FA required.**
| Field | Type |
|---|---|
| Role name | Text |
| Type | Platform role / Institution role |
| Description | Textarea |
| Base on | Select existing role to copy permissions from |

**After creating:** opens Role Edit Drawer for the new role immediately

**Footer:** [Cancel] [Create Role]

---

### 6.2 Confirm Permission Change Modal (480 px)

Triggered when editing permissions in matrix.
"Change {N} permissions for {Role}?"
| Field | Type |
|---|---|
| Summary | List of changes |
| Reason | Required text |
| 2FA code | OTP |
**Footer:** [Cancel] [Confirm Changes]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=platform_roles` | `exec/partials/platform_roles.html` | Tab click |
| `?part=institution_roles` | `exec/partials/institution_roles.html` | Tab click |
| `?part=permission_matrix` | `exec/partials/permission_matrix.html` | Tab click |
| `?part=role_audit` | `exec/partials/role_audit.html` | Tab click |
| `?part=role_drawer&id={id}` | `exec/partials/role_drawer.html` | Edit button click |

**Django view dispatch:**
```python
class RolesPermissionsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.manage_roles"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "platform_roles": "exec/partials/platform_roles.html",
                "institution_roles": "exec/partials/institution_roles.html",
                "permission_matrix": "exec/partials/permission_matrix.html",
                "role_audit": "exec/partials/role_audit.html",
                "role_drawer": "exec/partials/role_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/roles_permissions.html", ctx)

    def post(self, request):
        if not request.session.get("2fa_verified"):
            return JsonResponse({"error": "2FA required"}, status=403)
        part = request.GET.get("part", "")
        handlers = {
            "save_role": self._handle_save_role,
            "create_role": self._handle_create_role,
        }
        if part in handlers:
            return handlers[part](request)
        return HttpResponseNotAllowed(["GET"])
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| Platform roles tab | < 300 ms | > 800 ms |
| Permission matrix (120 rows × 11 cols) | < 600 ms | > 1.5 s |
| Role drawer | < 300 ms | > 800 ms |
| Full page initial load | < 800 ms | > 2 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Remove last permission from exec role | Error: "exec role must retain view_exec_dashboard permission" |
| Assign same permission to two conflicting roles | Warning: "This may create unexpected access overlap" (informational only) |
| Delete custom role with users | Error: "Cannot delete — 3 users have this role. Reassign first." |
| Permission matrix: unsaved changes | Toast "Unsaved changes — click Save or Discard" if navigating away |
| Role with 0 users | Card shows "0 users" in grey; still editable |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`4` | Switch tabs |
| `N` | New custom role |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/roles_permissions.html` | Full page shell |
| `exec/partials/platform_roles.html` | Platform role cards |
| `exec/partials/institution_roles.html` | Institution role cards |
| `exec/partials/permission_matrix.html` | Full permission matrix |
| `exec/partials/role_audit.html` | Role change audit log |
| `exec/partials/role_drawer.html` | Role edit drawer |
| `exec/partials/new_role_modal.html` | New custom role modal |
| `exec/partials/perm_change_confirm_modal.html` | Permission change confirmation |

---

## 12. Component References

| Component | Used in |
|---|---|
| `RoleCard` | §4.1, §4.2 |
| `TabBar` | §4.1–4.4 |
| `PermissionMatrix` | §4.3 |
| `PermissionCheckbox` | §4.3 + §5.1 |
| `RoleAuditTable` | §4.4 |
| `DrawerPanel` | §5.1 |
| `PermissionsChecklist` | §5.1 Section B |
| `ModalDialog` | §6.1–6.2 |
| `PaginationStrip` | §4.4 |
