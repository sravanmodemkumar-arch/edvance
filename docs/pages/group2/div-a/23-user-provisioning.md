# 23 — User Provisioning

> **URL:** `/group/gov/users/`
> **File:** `23-user-provisioning.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 · MD G5 (full) · CEO G4 (view only)

---

## 1. Purpose

Central management of all user accounts across all branches in the institution group. The MD
creates, edits, suspends, and deletes accounts for all group-level and branch-level staff.
CEO can view (for operational awareness) but cannot modify accounts.

This page covers: Group-level staff (Chairman, MD, CEO, President, VP, Secretary, Advisor) AND
branch-level staff (Principals, Vice Principals, Teachers, Admin, Hostel Wardens, etc.).

BGV status is tracked per user — mandatory for all staff with access to the platform and
physical access to minors (POCSO compliance).

---

## 2. Role Access

| Role | Access | Notes |
|---|---|---|
| Chairman | Full — all users, all actions | |
| MD | Full — all users, all actions | Primary owner |
| CEO | View only — no create/edit/delete | Operational awareness |
| Others | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  User Provisioning
```

### 3.2 Page Header
```
User Provisioning                                      [+ Create User]  [Import CSV]  [Export ↓]
[N] total users · [N] active · [N] pending BGV        (Chairman/MD only)
```

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Users | N |
| Active | N |
| Inactive / Suspended | N |
| Pending Invite | N |
| BGV Pending | N (red if >0) |
| BGV Expired | N (red if >0) |

---

## 4. Users Table

**Search:** Name, mobile, email (masked). Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches + "Group-level" |
| Role | Multi-select | All roles (grouped by Division A–P) |
| Level | Multi-select | G0 · G1 · G2 · G3 · G4 · G5 |
| Status | Multi-select | Active · Suspended · Pending Invite · Locked |
| BGV Status | Multi-select | Verified · Pending · Expired · Not Started |
| POCSO Trained | Select | All · Yes · No |
| Last Login | Select | Today · This Week · >30 days · Never |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Row select |
| Name | Text | ✅ | |
| Role | Badge | ✅ | Colour-coded by Division |
| Level | Badge | ✅ | G0–G5 |
| Branch | Text | ✅ | "Group-level" for HQ staff |
| Mobile | Text | ❌ | Masked: 98***** |
| Email | Text | ❌ | Masked: r***@domain |
| Status | Badge | ✅ | Active · Suspended · Pending · Locked |
| BGV Status | Badge | ✅ | Verified · Pending · Expired · N/A |
| POCSO | Badge | ✅ | Trained · Not Trained |
| Last Login | Date + relative | ✅ | Red if >30 days |
| Created | Date | ✅ | |
| Actions | — | ❌ | View · Edit · Reset Password · Suspend · Delete |

**Default sort:** Created descending (newest first).

**Pagination:** Server-side · Default 25/page.

**Bulk actions (Chairman/MD):**
- Suspend Selected
- Reset Password Selected (sends OTP reset to each)
- Export Selected CSV
- Assign BGV Reminder

---

## 5. Drawers & Modals

### 5.1 Drawer: `user-create`
- **Trigger:** [+ Create User] header button
- **Width:** 560px
- **Tabs:** Profile · Role · Branch · Invite

#### Tab: Profile
| Field | Type | Required | Validation |
|---|---|---|---|
| Full Name | Text | ✅ | Min 3, max 100 |
| Mobile | Tel | ✅ | 10-digit Indian mobile, unique across platform |
| Email | Email | ✅ | Valid email, unique across platform |
| Designation | Text | ✅ | Max 80 chars |
| Date of Birth | Date | ❌ | Must be adult (>18) |
| Gender | Select | ❌ | Male · Female · Other · Prefer not to say |
| Employee ID | Text | ❌ | Alphanumeric, unique per branch |
| Date of Joining | Date | ✅ | Cannot be future date |

#### Tab: Role
| Field | Type | Required | Validation |
|---|---|---|---|
| Division | Select | ✅ | A (Governance) · B (Academic) · C (Admissions) · … · P (Audit) |
| Role | Select | ✅ | Populated from selected Division roles |
| Access Level | Read-only | — | Auto-populated from role: G0–G5 |

#### Tab: Branch
| Field | Type | Required | Validation |
|---|---|---|---|
| Scope | Radio | ✅ | Group-level (all branches) · Branch-specific |
| Branch | Multi-select | Conditional | Required if Branch-specific |
| Primary Branch | Select | Conditional | Required if multiple branches |

#### Tab: Invite
| Field | Type | Required | Validation |
|---|---|---|---|
| Invite Method | Radio | ✅ | WhatsApp OTP · Email OTP · Both |
| Invite Preview | Read-only | — | Shows message that will be sent |
| Send Invite Now | Toggle | ✅ | Default On — can delay invite |

**Submit:** "Create Account & Send Invite" — disabled until all required tabs valid.
Tabs show red dot if incomplete.

### 5.2 Drawer: `user-edit`
- **Width:** 560px
- **Tabs:** Profile · Role · Branch · History
- Pre-filled from user data

#### History Tab (extra in edit)
- Login history: Last 20 logins (date, time, IP, device type)
- Role change log: Who changed what role when and why
- Actions taken: Approvals, circulars sent, etc. (last 10)
- All read-only

### 5.3 Drawer: `user-history-detail`
- **Trigger:** View row action
- **Width:** 480px
- **Same as History tab in user-edit but standalone**

### 5.4 Modal: `user-suspend-confirm`
- **Width:** 400px
- **Fields:**
  - Warning: "This will immediately prevent [Name] from accessing the platform"
  - Reason (required, min 20 chars)
  - Suspension End Date (optional — auto-reactivates on this date)
  - Notify user? (toggle, default on — sends WhatsApp message)
- **Buttons:** [Suspend Account] (danger) + [Cancel]

### 5.5 Modal: `password-reset-confirm`
- **Width:** 380px
- **Content:** "Send OTP password reset to [Name]'s mobile [98*****]?"
- **Buttons:** [Send Reset OTP] + [Cancel]
- **On confirm:** OTP sent via WhatsApp → user logs in with OTP → sets no password (OTP-only system)

### 5.6 Modal: `user-delete-confirm`
- **Width:** 420px
- **Prerequisites:** Cannot delete active user — must suspend first
- **Fields:** Reason (required, min 30 chars) · "Delete" typed confirmation
- **Warning:** "User's audit log entries are retained permanently. Login history is retained for 7 years per DPDP Act."
- **Buttons:** [Delete Account] (danger, enabled only when "Delete" typed) + [Cancel]

### 5.7 Modal: `import-csv`
- **Width:** 480px
- **Fields:** File upload (CSV only, max 500 rows) · [Download Template CSV] link
- **Preview:** After upload, shows first 10 rows with column mapping
- **Validation errors shown:** Duplicate mobile, invalid role, etc.
- **Buttons:** [Import [N] Users] + [Cancel]

---

## 6. Charts

### 6.1 Users by Division (Donut)
- **Type:** Doughnut chart
- **Data:** User count per division (A–P)
- **Colours:** One colour per division
- **Export:** PNG

### 6.2 BGV Status Distribution (Donut)
- **Type:** Doughnut
- **Data:** Verified · Pending · Expired · Not Started
- **Colours:** Green · Yellow · Red · Grey
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| User created | "Account created for [Name]. Invite sent via [channel]." | Success | 4s |
| User updated | "[Name]'s account updated" | Success | 4s |
| User suspended | "[Name]'s account suspended. User notified." | Warning | 6s |
| User reactivated | "[Name]'s account reactivated. User notified." | Success | 4s |
| Password reset sent | "OTP reset sent to [Name]'s mobile" | Info | 4s |
| User deleted | "[Name]'s account deleted. Audit data retained." | Warning | 6s |
| Duplicate mobile | "Mobile number already registered to another account" | Error | Manual |
| CSV import success | "[N] users imported successfully. [M] errors — download error report." | Success | Manual |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No users | "No users provisioned" | "Create the first user account for this group" | [+ Create User] |
| No results (search/filter) | "No users match" | "Try different search terms or clear your filters" | [Clear Filters] |
| No BGV issues | "BGV compliance looks good" | "All users have valid BGV records" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) |
| Table filter/search/sort | Inline skeleton rows |
| User create drawer | Spinner in drawer |
| User create submit | Full-page overlay "Creating account…" |
| CSV import | Progress bar in modal |
| BGV status refresh | Shimmer on BGV column |

---

## 10. Role-Based UI Visibility

| Element | Chairman/MD G5 | CEO G4 |
|---|---|---|
| [+ Create User] | ✅ | ❌ |
| [Import CSV] | ✅ | ❌ |
| [Export] | ✅ | ✅ |
| Edit row action | ✅ | ❌ |
| Suspend row action | ✅ | ❌ |
| Delete row action | ✅ (Chairman) | ❌ |
| Reset Password | ✅ | ❌ |
| Mobile/Email (unmasked) | Chairman only | ❌ |
| Bulk actions | ✅ | ❌ |
| BGV Status column | ✅ | ✅ (read) |
| History tab | ✅ | ✅ (read) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/users/` | JWT (G5/G4) | User list (paginated, filtered) |
| POST | `/api/v1/group/{id}/users/` | JWT (G5) | Create user |
| GET | `/api/v1/group/{id}/users/{uid}/` | JWT (G5) | User detail |
| PUT | `/api/v1/group/{id}/users/{uid}/` | JWT (G5) | Update user |
| DELETE | `/api/v1/group/{id}/users/{uid}/` | JWT (G5 Chairman) | Delete user |
| POST | `/api/v1/group/{id}/users/{uid}/suspend/` | JWT (G5) | Suspend |
| POST | `/api/v1/group/{id}/users/{uid}/reactivate/` | JWT (G5) | Reactivate |
| POST | `/api/v1/group/{id}/users/{uid}/reset-password/` | JWT (G5) | OTP reset |
| GET | `/api/v1/group/{id}/users/{uid}/history/` | JWT (G5) | Login + action history |
| POST | `/api/v1/group/{id}/users/import/` | JWT (G5) | CSV import |
| GET | `/api/v1/group/{id}/users/export/?format=csv` | JWT (G5/G4) | Export |
| GET | `/api/v1/group/{id}/users/stats/` | JWT | Summary stats |

---

## HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search users | `input delay:300ms` | GET `.../users/?q=` | `#users-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../users/?role=&branch=&status=&bgv=` | `#users-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../users/?sort=&dir=` | `#users-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../users/?page=` | `#users-table-section` | `innerHTML` |
| Open user create drawer | `click` | GET `.../users/new/` | `#drawer-body` | `innerHTML` |
| Open user edit drawer | `click` | GET `.../users/{uid}/edit/` | `#drawer-body` | `innerHTML` |
| Edit drawer tab switch | `click` | GET `.../users/{uid}/edit/?tab=profile\|role\|branch\|history` | `#user-drawer-tab` | `innerHTML` |
| Suspend user (confirm modal) | `click` | POST `.../users/{uid}/suspend/` | `#user-row-{uid}` | `outerHTML` |
| Bulk suspend | `click` | POST `.../users/bulk-suspend/` | `#users-table-section` | `innerHTML` |
| Bulk password reset | `click` | POST `.../users/bulk-reset-password/` | `#bulk-action-result` | `innerHTML` |
| CSV import upload | `change` | POST `.../users/import/` | `#import-result` | `innerHTML` |
| BGV reminder send | `click` | POST `.../users/{uid}/bgv-reminder/` | `#user-row-{uid}-bgv` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
