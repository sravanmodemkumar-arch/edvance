# 14 — Role & Permission Matrix

- **URL:** `/group/it/users/permissions/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4) — Primary owner; IT Director (Role 53, G4) for approvals

---

## 1. Purpose

The Role & Permission Matrix is the "permissions constitution" for the entire EduForge group deployment. Every role that exists on the platform — from the Group Chairman's read-only dashboard observer role to the Branch Exam Controller's exam-creation rights — has its full permission set defined on this page. Any change made here propagates to every user who holds that role across every branch in the group.

The page operates as a two-pane configuration surface. The left pane presents the complete role hierarchy in a collapsible tree: Group Roles → Branch Roles → Staff Roles → Student Roles → Parent Roles. The right pane shows the permission matrix for the currently selected role — a grid of Modules (Admissions, Exams, Finance, HR, IT, Transport, Library, Hostel, etc.) crossed against Actions (View / Create / Edit / Delete / Export / Approve) with checkboxes at each intersection.

Governance is the defining feature of this page. Permission changes are not instant: every edit creates a new Draft version of the role's permission set. The IT Admin can iterate on the draft and then submit it for approval. The IT Director (G4) must approve the draft before it becomes the Active version. Until approval, the old Active version remains in force. This two-step process prevents accidental privilege escalation from reaching production immediately. All versions are retained indefinitely for compliance auditing.

The page is read-heavy — most visits are lookups to verify what a role can and cannot do, not edits. The matrix is therefore presented in a read-optimised view by default, with an explicit "Edit Permissions" button that switches the right pane into edit mode.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + create Draft versions + submit for approval | Cannot self-approve; must submit to IT Director |
| Group IT Director | G4 | Full read + approve/reject permission change requests | Can also edit and self-approve if no conflict of interest |
| Group Cybersecurity Officer | G1 | Read-only (entire matrix) | Security audit purpose |
| Group Data Privacy Officer | G1 | Read-only (entire matrix) | DPDP compliance review |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → User Management → Role & Permission Matrix
```

### 3.2 Page Header
- **Title:** `Role & Permission Matrix`
- **Subtitle:** `[N] Roles Defined · [N] Pending Approval · Last change: [date]`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `+ Add Role` · `View Pending Approvals ([N])` · `Export Matrix`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Draft permission sets awaiting IT Director approval > 48h | "[N] permission set changes have been awaiting approval for more than 48 hours." | Amber |
| Active roles with no users assigned | "[N] active roles have zero users assigned. Consider archiving unused roles." | Info (Blue) |
| Roles with pending approval that conflict (same module) | "Conflicting permission changes detected in pending drafts. Review before approving." | Red |

---

## 4. KPI Summary Bar

No numeric KPI cards on this page. The header subtitle line provides the essential counts. The two-pane layout uses the full width for the role tree and permission matrix.

---

## 5. Main Table — Role List (Left Pane)

The left pane is a collapsible tree list, not a traditional paginated table.

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Role Name | Text (click to load right pane) | No | Indented by hierarchy level |
| Access Level | Badge (G0–G5) | No | Shown inline |
| Users Assigned | Number | No | Live count |
| Last Modified | Date | No | Of the Active version |
| Version | Text (e.g., v3) | No | Current active version number |
| Status | Badge (Active / Draft / Pending Approval / Archived) | No | |
| Actions | Edit / View History / Archive | No | Edit opens right pane in edit mode |

### 5.1 Role Tree Structure
```
▼ Group Roles (G1–G5)
    ├── Group IT Admin
    ├── Group IT Director
    ├── Group HR Director
    └── ... (all group-level roles)
▼ Branch Roles
    ├── Branch Principal
    ├── Branch Vice Principal
    └── ... (all branch-level roles)
▼ Staff Roles
    ├── Teaching Staff
    ├── Non-Teaching Staff
    └── ...
▼ Student Roles
    └── Student
▼ Parent Roles
    └── Parent / Guardian
```

### 5.2 Search (Left Pane)
- Text search filters the role tree in real-time
- Highlights matching role name; collapses non-matching branches

---

## 6. Drawers

### 6.1 Right Pane: Permission Matrix (Read View)
- **Trigger:** Click any role in the left tree
- **Width:** Fills remaining page width (approx. 65–70% of viewport)
- **Content:**
  - Role name, access level badge, description
  - Version indicator: "Active: v[N] · Approved [date] by [IT Director name]"
  - Permission grid:

| Module | View | Create | Edit | Delete | Export | Approve |
|---|---|---|---|---|---|---|
| Admissions | ✓ | ✓ | ✓ | — | ✓ | — |
| Examinations | ✓ | — | — | — | ✓ | — |
| Finance | ✓ | — | — | — | — | — |
| HR & Staff | ✓ | — | — | — | — | — |
| IT & Technology | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ... | | | | | | |

  - Checkmarks rendered as green tick icons; dashes rendered as grey dash icons
  - Bottom: `Edit Permissions` button (visible to G4 IT Admin/Director only)

### 6.2 Right Pane: Permission Matrix (Edit Mode)
- **Trigger:** `Edit Permissions` button in read view
- **Width:** Same (right pane inline edit)
- **Content:** Same grid but checkboxes replace icons; all cells editable
- **Module rows:** Admissions / Examinations / Finance / HR & Staff / IT & Technology / Transport / Library / Hostel / Reports & Analytics / System Settings / Notifications / Student Records / Parent Portal / Communications
- **Actions per module:** View / Create / Edit / Delete / Export / Approve
- **Validation:** At least View must be enabled if any other action is enabled
- **Bottom controls:** Save as Draft · Cancel
- **On Save Draft:** New version created with status "Draft"; right pane switches back to read view showing new draft version

### 6.3 Drawer: `permission-history` — View Version History
- **Trigger:** Actions → View History (left pane)
- **Width:** 480px
- **Content:** Chronological list of all versions for the selected role:
  - Version number, status (Active/Archived), created by, approved by (if approved), approval date
  - Click any version to view its full permission grid in a nested read-only view
  - Active version is highlighted with a green "Current" badge

### 6.4 Modal: Submit for Approval
- **Trigger:** `Submit for Approval` button visible when a Draft version exists
- **Type:** Centered modal (480px)
- **Content:** "You are submitting permission changes for [Role Name] (Draft v[N]) for IT Director approval. Changes will not take effect until approved. Summary of changes: [diff list showing which module/action checkboxes changed]."
- **Fields:**
  - Change Summary / Justification (required, textarea, min 20 characters)
  - Urgency (radio: Standard / Urgent)
- **Buttons:** Submit for Approval · Cancel

### 6.5 Modal: Add New Role
- **Trigger:** `+ Add Role` button
- **Type:** Drawer 480px
- **Fields:**
  - Role Name (required, text, unique)
  - Role Category (required, dropdown: Group / Branch / Staff / Student / Parent)
  - Access Level (required, dropdown: G0–G5)
  - Description (required, textarea)
  - Base Template (optional, dropdown: "Copy permissions from existing role" — pre-fills the matrix)
- **On submit:** Role created with empty or copied permission set as Draft v1; IT Director approval required before it becomes Active

---

## 7. Charts

No charts on this page. The permission matrix grid itself is the primary visualisation. Version history provides a timeline view inline within the history drawer.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Draft saved | "Permission changes for [Role Name] saved as Draft v[N]. Submit for approval to apply." | Info | 5s |
| Submitted for approval | "Permission changes for [Role Name] submitted for IT Director approval." | Success | 4s |
| Role approved (IT Director action) | "Permission set v[N] for [Role Name] approved and now Active. [N] users affected." | Success | 5s |
| Role rejected (IT Director action) | "Permission set v[N] for [Role Name] rejected. Review rejection notes." | Warning | 5s |
| New role created | "New role '[Role Name]' created as Draft. Submit permissions for IT Director approval." | Success | 4s |
| Role archived | "Role '[Role Name]' archived. Users previously assigned this role must be reassigned." | Warning | 5s |
| Export triggered | "Permission matrix export is being prepared." | Info | 3s |
| Submit for approval failed | Error: `Could not submit draft. Review and correct the permission set before resubmitting.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No role selected in left pane | "Select a Role" | "Click a role from the list on the left to view its permission matrix." | — (instructional) |
| No roles defined at all | "No Roles Configured" | "No EduForge roles have been defined yet. Add the first role to begin configuring permissions." | + Add Role |
| Version history drawer — only one version | "No Previous Versions" | "This role has only one version. Version history will appear here when changes are made." | — |
| Role has zero users assigned | "No Users Assigned" | "No users are currently assigned to this role. Users are assigned via the Account Manager." | Go to Account Manager |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Left pane: role tree skeleton (collapsed nodes, shimmering); Right pane: instructional placeholder |
| Role click (loading permission matrix) | Right pane full-width skeleton: module rows with checkbox shimmer |
| Edit mode save (draft creation) | Save button spinner; right pane reloads with new version indicator |
| Submit for approval | Modal submit button spinner; left pane role row status badge updates |
| Version history drawer open | Drawer skeleton; version rows load progressively |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | Cybersecurity Officer (G1) | Data Privacy Officer (G1) |
|---|---|---|---|---|
| Left pane — full role tree | Visible | Visible | Visible | Visible |
| Right pane — read view | Visible | Visible | Visible | Visible |
| Edit Permissions button | Visible | Visible | Hidden | Hidden |
| + Add Role button | Visible | Visible | Hidden | Hidden |
| Submit for Approval button | Visible (IT Admin creates draft) | Visible | Hidden | Hidden |
| Approve / Reject (in approval modal) | Hidden (cannot self-approve) | Visible | Hidden | Hidden |
| Archive Role action | Visible | Visible | Hidden | Hidden |
| Export Matrix | Visible | Visible | Visible | Hidden |
| View Version History | Visible | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/permissions/roles/` | JWT (G1+) | Role tree with metadata |
| POST | `/api/v1/it/permissions/roles/` | JWT (G4) | Create a new role |
| GET | `/api/v1/it/permissions/roles/{id}/` | JWT (G1+) | Role details + active permission set |
| GET | `/api/v1/it/permissions/roles/{id}/versions/` | JWT (G1+) | All versions for a role |
| POST | `/api/v1/it/permissions/roles/{id}/draft/` | JWT (G4) | Save permission changes as a new draft |
| POST | `/api/v1/it/permissions/roles/{id}/submit/` | JWT (G4 — IT Admin) | Submit draft for IT Director approval |
| POST | `/api/v1/it/permissions/roles/{id}/approve/` | JWT (G4 — IT Director) | Approve pending draft; makes it Active |
| POST | `/api/v1/it/permissions/roles/{id}/reject/` | JWT (G4 — IT Director) | Reject pending draft with notes |
| PATCH | `/api/v1/it/permissions/roles/{id}/archive/` | JWT (G4) | Archive a role |
| GET | `/api/v1/it/permissions/matrix/export/` | JWT (G3+) | Export full permission matrix as CSV/XLSX |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load role tree | `load` | GET `/api/v1/it/permissions/roles/` | `#role-tree` | `innerHTML` |
| Select role (load matrix) | `click` on role row | GET `/api/v1/it/permissions/roles/{id}/` | `#permission-matrix-pane` | `innerHTML` |
| Search roles in left pane | `input` (200ms debounce) | GET `/api/v1/it/permissions/roles/?q=...` | `#role-tree` | `innerHTML` |
| Switch to edit mode | `click` on Edit Permissions | — (client-side toggle, no HTTP) | `#permission-matrix-pane` | replaces icons with checkboxes |
| Save draft | `click` on Save as Draft | POST `/api/v1/it/permissions/roles/{id}/draft/` | `#permission-matrix-pane` | `innerHTML` |
| Submit for approval | `click` on Submit for Approval | POST `/api/v1/it/permissions/roles/{id}/submit/` | `#role-tree` + `#approval-banner` | `innerHTML` |
| Open version history drawer | `click` on View History | GET `/api/v1/it/permissions/roles/{id}/versions/` | `#permission-drawer` | `innerHTML` |
| Approve permission change | `click` on Approve | POST `/api/v1/it/permissions/roles/{id}/approve/` | `#permission-matrix-pane` + `#role-tree` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
