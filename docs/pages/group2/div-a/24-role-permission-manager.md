# 24 — Role & Permission Manager

> **URL:** `/group/gov/roles/`
> **File:** `24-role-permission-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Chairman G5 · MD G5 (full) · CEO G4 (view only)

---

## 1. Purpose

RBAC (Role-Based Access Control) configuration for the institution group. Defines what each
role can see and do within the EduForge platform. System roles (standard Division A–P roles)
come pre-configured. Chairman/MD can create custom roles for group-specific needs and adjust
permissions at the feature level.

This page shows the full permission matrix — Roles × Features — with toggle controls.

---

## 2. Role Access

| Role | Access | Notes |
|---|---|---|
| Chairman | Full — create custom roles, edit all permissions | |
| MD | Full — create, edit | Co-owner |
| CEO | View only — see permission matrix but no changes | |
| Others | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Role & Permission Manager
```

### 3.2 Page Header
```
Role & Permission Manager                              [+ Create Custom Role]  [Export Matrix ↓]
[N] system roles · [N] custom roles                   (Chairman/MD only)
```

---

## 4. Roles Table

**Search:** Role name. Debounce 300ms.

**Filters:** Division · Level (G0–G5) · Type (System/Custom).

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Role Name | Text | ✅ | |
| Division | Badge | ✅ | A–P |
| Level | Badge | ✅ | G0–G5 |
| Type | Badge | ✅ | System · Custom |
| User Count | Number | ✅ | How many users currently have this role |
| Permissions | Number | ✅ | Count of enabled permissions |
| Last Modified | Date | ✅ | |
| Modified By | Text | ❌ | |
| Actions | — | ❌ | View Permissions · Edit (custom only) · Clone · Delete (custom only) |

**Default sort:** Division · Level ascending.

**Pagination:** 25/page (system has ~126 roles — needs pagination).

**Row actions:**
| Action | Notes |
|---|---|
| View Permissions | Opens `role-permission-matrix` drawer — full permission list |
| Edit | Custom roles only — opens edit drawer |
| Clone | Creates a copy of this role as a new custom role |
| Delete | Custom roles only with 0 users — confirm modal |

---

## 5. Permission Matrix View (Alternative View)

**[Permission Matrix] button** in page header — toggles to matrix view.

**Display:** Large table — Roles as columns, Permissions as rows.

**Rows grouped by module:** Branch · Academic · Finance · HR · Compliance · Communications · IT · Reports.

**Cell:** Checkbox — checked = role has this permission. Greyed out for System roles.

**Scrollable:** Horizontal scroll (many roles) and vertical scroll (many permissions).

**Column sticky:** Role name column sticky on left.

**Export:** Matrix as CSV.

---

## 6. Permission Modules & Permissions

### Module: Branch Management
- View branch list
- Create branch
- Edit branch
- Activate/deactivate branch
- Delete branch
- View branch detail (all tabs)
- Edit branch config

### Module: Academic
- View exam schedules
- Approve/reject exam schedules
- Create curriculum content
- View academic performance
- Manage academic calendar
- View/edit topper lists

### Module: Finance
- View fee summary
- View fee details by branch
- Edit fee structure
- View financial reports
- Export financial data

### Module: HR & Staff
- View staff list
- Create user accounts
- Edit user accounts
- Suspend/delete users
- View BGV status
- Update BGV status
- View POCSO training status

### Module: Compliance
- View compliance overview
- Update compliance status
- Upload compliance evidence
- View audit log

### Module: Communications
- Compose circulars
- Send circulars
- View circulars
- Compose announcements
- Approve announcements
- View announcements
- Manage calendar

### Module: IT & Settings
- View group settings
- Edit group settings
- Manage feature toggles
- View role permissions
- Edit role permissions

### Module: Reports
- View governance reports
- Build/schedule reports
- Export reports
- View audit log
- Export audit log

---

## 7. Drawers & Modals

### 7.1 Drawer: `role-permission-matrix` — View Role Permissions
- **Trigger:** Roles table → [View Permissions]
- **Width:** 640px
- **Content:** Full permission list for this role, grouped by module
- **For System roles:** All permissions read-only (cannot change)
- **For Custom roles:** Editable checkboxes (Chairman/MD only)
- **Save Changes button:** Appears only if changes made (custom role, Chairman/MD)

### 7.2 Drawer: `custom-role-create` / `custom-role-edit`
- **Trigger:** [+ Create Custom Role] or Edit on custom role
- **Width:** 640px
- **Tabs:** Profile · Permissions

#### Tab: Profile
| Field | Type | Required | Validation |
|---|---|---|---|
| Role Name | Text | ✅ | Min 3, max 80 chars · Unique in group |
| Division | Select | ✅ | A–P |
| Base Role | Select | ❌ | Start from an existing role's permissions |
| Description | Textarea | ❌ | Max 200 chars |
| Access Level | Select | ✅ | G0–G5 |

#### Tab: Permissions
- Module sections with checkbox groups (same as Permission Matrix)
- "Select All" checkbox per module
- Permission count shown: "X of Y permissions enabled"
- Warning: "Higher level permissions may expose sensitive data"

**Submit:** "Create Role" / "Save Changes" — disabled until Profile tab complete.

### 7.3 Modal: `role-delete-confirm`
- **Width:** 380px
- **Prerequisite check:** If role has users → "Cannot delete: [N] users have this role. Reassign them first."
- **If 0 users:** "Delete custom role [Name]? This cannot be undone."
- **Buttons:** [Delete] + [Cancel]

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Custom role created | "Custom role [Name] created" | Success | 4s |
| Role permissions updated | "Permissions updated for [Role]" | Success | 4s |
| Role deleted | "Custom role [Name] deleted" | Warning | 6s |
| Role cloned | "Role cloned as [Name] (Custom)" | Info | 4s |
| System role edit attempt | "System roles cannot be modified" | Warning | 4s |
| Delete blocked (has users) | "Reassign [N] users before deleting this role" | Error | Manual |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No custom roles | "No custom roles" | "All roles are system defaults. Create a custom role for group-specific needs." | [+ Create Custom Role] |
| No search results | "No roles match" | "Try different search terms" | [Clear Search] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: table (10 rows) |
| Matrix view switch | Full matrix skeleton |
| Role permissions drawer | Spinner in drawer |
| Permission save | Spinner in Save button |

---

## 11. Role-Based UI Visibility

| Element | Chairman G5 | MD G5 | CEO G4 |
|---|---|---|---|
| [+ Create Custom Role] | ✅ | ✅ | ❌ |
| Edit permissions (custom role) | ✅ | ✅ | ❌ |
| Edit permissions (system role) | ❌ (read-only) | ❌ | ❌ |
| Delete custom role | ✅ | ✅ | ❌ |
| Clone role | ✅ | ✅ | ❌ |
| View permission matrix | ✅ | ✅ | ✅ (read) |
| [Export Matrix] | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/roles/` | JWT (G5/G4) | All roles list |
| POST | `/api/v1/group/{id}/roles/` | JWT (G5) | Create custom role |
| GET | `/api/v1/group/{id}/roles/{rid}/` | JWT (G5/G4) | Role + permissions detail |
| PUT | `/api/v1/group/{id}/roles/{rid}/` | JWT (G5) | Update custom role |
| DELETE | `/api/v1/group/{id}/roles/{rid}/` | JWT (G5) | Delete custom role |
| POST | `/api/v1/group/{id}/roles/{rid}/clone/` | JWT (G5) | Clone role |
| PUT | `/api/v1/group/{id}/roles/{rid}/permissions/` | JWT (G5) | Update permissions |
| GET | `/api/v1/group/{id}/roles/matrix/` | JWT (G5/G4) | Full matrix data |
| GET | `/api/v1/group/{id}/roles/matrix/export/` | JWT | Export matrix CSV |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search roles | `input delay:300ms` | GET `.../roles/?q=` | `#roles-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../roles/?division=&level=&type=` | `#roles-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../roles/?sort=&dir=` | `#roles-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../roles/?page=` | `#roles-table-section` | `innerHTML` |
| Switch to matrix view | `click` | GET `.../roles/matrix/` | `#roles-content-area` | `innerHTML` |
| Open role permissions drawer | `click` | GET `.../roles/{rid}/` | `#drawer-body` | `innerHTML` |
| Save custom role permissions | `click` | PUT `.../roles/{rid}/permissions/` | `#permission-section` | `innerHTML` |
| Create custom role (drawer open) | `click` | GET `.../roles/new/` | `#drawer-body` | `innerHTML` |
| Clone role | `click` | POST `.../roles/{rid}/clone/` | `#roles-table-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
