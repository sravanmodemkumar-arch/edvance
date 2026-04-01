# 02 — MD Dashboard

> **URL:** `/group/gov/md/`
> **File:** `02-md-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Managing Director (G5) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Managing Director. The MD is responsible for:
- Provisioning principal and admin user accounts across all branches
- Onboarding new branches step-by-step
- Tracking policy acknowledgement from all principals
- Monitoring full staff structure across branches

This dashboard surfaces the MD's daily work queue: pending user creation requests, new branch
onboarding stages, policy compliance gaps, and staff provisioning alerts.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group MD | G5 | Full — all sections, all actions | Exclusive dashboard |
| Group Chairman | G5 | — | Has own dashboard `/group/gov/chairman/` |
| All others | G4/G3/G1 | — | Redirected to their own dashboards |

> **Access enforcement:** Django view decorator `@require_role('md')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  MD Dashboard
```

### 3.2 Page Header
```
Managing Director — [MD Name]                          [+ Provision User]  [View All Staff →]
[Group Name] · Last login: [date time]
```

---

## 4. KPI Summary Bar (5 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Provisioned Users | `1,247 accounts` · +23 this week | Info (always blue) | → User Provisioning page 23 |
| Active Principals | `48 / 50` · 2 vacancies flagged | Green = 100% · Yellow = 1–2 vacant · Red = 3+ | → User Provisioning page 23 |
| Branches in Onboarding | `2 branches` in pipeline | Info | → Branch Onboarding page 11 |
| Policy Acknowledgement | `91%` of principals acknowledged latest | Green ≥100% · Yellow 80–99% · Red <80% | → Policy Management page 19 |
| Pending User Requests | `7 pending` requests from branches | Badge — red if >5 | → User Provisioning page 23 |

---

## 5. Sections

### 5.1 Principal Accounts Status

> All branch principals' account health — the MD's primary responsibility.

**Search:** By principal name, branch name, email, phone. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches in group |
| Account Status | Multi-select | Active · Inactive · Pending Invite · Locked |
| Last Login | Select | Today · This Week · This Month · Never |
| BGV Status | Multi-select | Verified · Pending · Expired · Not Started |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Principal Name | Text | ✅ | |
| Branch | Text + link | ✅ | Opens Branch Detail page 10 |
| Mobile / Email | Text | ❌ | Masked: `98***** / r***@` |
| Account Status | Badge | ✅ | Active (green) · Pending (yellow) · Locked (red) |
| Last Login | Date + relative | ✅ | "3 days ago" — red if >30 days |
| BGV Status | Badge | ✅ | Verified · Pending · Expired |
| Policy Acknowledged | Yes/No badge | ✅ | Red if No and policy is 0–30 days old |
| Actions | — | ❌ | Edit · Reset Password · Suspend · View History |

**Default sort:** Last Login ascending (longest inactive first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

**Row actions:**
| Action | Modal/Drawer | Notes |
|---|---|---|
| Edit | `user-edit` drawer 560px | Role, branch, status change |
| Reset Password | Confirm modal 400px | Sends OTP reset to principal's mobile |
| Suspend | `user-suspend-confirm` modal 400px | Required reason field |
| View History | `user-history-detail` drawer 480px | Login history, role changes, actions taken |

---

### 5.2 Staff Provisioning Pending Queue

> Requests from branch principals/HR to create new user accounts.

**Display:** Table (max 10 rows). "View all in User Provisioning →" link.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Requested By | Text | ✅ | Branch principal name |
| Branch | Text | ✅ | |
| Role Requested | Badge | ✅ | E.g. "Branch Accountant", "Hostel Warden" |
| User Name | Text | ❌ | Name of person to be provisioned |
| Purpose / Notes | Text (truncated) | ❌ | |
| Days Pending | Number | ✅ | Red badge if >3 days |
| Actions | — | ❌ | [Approve & Create] [Reject] [View Details] |

**Approve & Create:** Opens `user-create` drawer pre-filled with requested role + branch. MD can
modify before submitting.

**Reject:** 400px modal — required reason (communicated back to requesting branch).

---

### 5.3 Branch Onboarding Pipeline (mini Kanban)

> Compact view of branches currently being onboarded. Full view → page 11.

**Display:** Horizontal scroll Kanban — stages as columns, branch cards within each stage.

**Stages:**
```
Applied → Legal → Infrastructure → Staff Hiring → System Setup → Training → Soft Launch → Live
```

**Branch card fields:** Branch name · Expected go-live date · Current stage completion % · Blocker count (red badge if >0) · Assigned Coordinator.

**Click card:** Opens Branch Onboarding Pipeline (page 11) filtered to that branch.

**"View Full Pipeline →"** link to page 11.

---

### 5.4 Policy Acknowledgement Tracker

> Which branch principals have acknowledged the latest group policies.

**Display:** Table — one row per policy (latest version only).

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Policy Name | Text | ✅ | |
| Category | Badge | ✅ | Academic · HR · Finance · Safety |
| Version | Text | ❌ | e.g. "v3.1" |
| Published | Date | ✅ | |
| Acknowledged | Progress `42 / 50` | ✅ | Shows count + progress bar |
| % | Number + bar | ✅ | Colour-coded |
| Pending Principals | Number | ✅ | Click → drill-down list |
| Actions | — | ❌ | [Send Reminder] [View Details] |

**Send Reminder action:** `hx-post` — sends WhatsApp reminder to all non-acknowledging principals
for that policy. Toast: "Reminder sent to [N] principals."

**Click "Pending Principals" count:** Opens 480px drawer listing non-acknowledging principals with
name, branch, last login, and individual [Send Reminder] per row.

---

### 5.5 Staff Structure Overview (read-only aggregate)

> Cross-branch staff headcount snapshot. Full detail → page 32.

**Display:** 3-column summary cards.

| Card | Metric |
|---|---|
| Total Sanctioned | Group-wide sanctioned positions |
| Total Filled | Filled positions — % of sanctioned |
| Vacancies | Open positions by type (Teaching / Non-Teaching / Hostel / Transport) |

**"View Full Staff Report →"** link to page 32.

---

## 6. Drawers & Modals

### 6.1 Drawer: `user-create` — Provision New User
- **Trigger:** [+ Provision User] header button or Approve & Create in pending queue
- **Width:** 560px
- **Tabs:** Profile · Role · Branch · Invite

#### Tab: Profile
| Field | Type | Required | Validation |
|---|---|---|---|
| Full Name | Text | ✅ | Min 3 chars, max 100 |
| Mobile Number | Tel | ✅ | 10-digit Indian mobile, unique across group |
| Email | Email | ✅ | Valid email, unique |
| Designation | Text | ✅ | Free text, max 80 chars |
| Date of Joining | Date | ✅ | Cannot be future date |
| Employee ID | Text | ❌ | Alphanumeric, unique per branch |

#### Tab: Role
| Field | Type | Required | Validation |
|---|---|---|---|
| Role | Dropdown | ✅ | All Division A–P roles for group level |
| Access Level | Auto-populated | — | Based on role selected |
| Start Date | Date | ✅ | ≥ Date of Joining |

#### Tab: Branch
| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Multi-select or Single | ✅ | Depends on role (group-level = all branches) |
| Primary Branch | Select | Conditional | If multi-branch role |

#### Tab: Invite
| Field | Type | Required | Validation |
|---|---|---|---|
| Invite via | Radio | ✅ | WhatsApp OTP · Email OTP |
| Preview invite message | Read-only | — | Shows message that will be sent |

**Submit button:** "Create Account & Send Invite" — disabled until all required fields valid.
**Server error summary** at top of drawer on validation failure.

### 6.2 Drawer: `user-edit` — Edit User
- **Width:** 560px
- **Tabs:** Profile · Role · Branch · History
- **History tab:** Role change log, login history (last 20 logins), branch changes — read-only

### 6.3 Modal: `user-suspend-confirm`
- **Width:** 400px
- **Fields:** Warning message · Reason (required, min 20 chars) · Suspension end date (optional)
- **Buttons:** [Suspend Account] (danger) + [Cancel]
- **On confirm:** Account suspended, WhatsApp message sent to user, audit log entry created

### 6.4 Modal: `password-reset-confirm`
- **Width:** 380px
- **Content:** "Send OTP reset to [Name]'s mobile [98*****]?"
- **Buttons:** [Send Reset] + [Cancel]

### 6.5 Drawer: `policy-reminder-detail`
- **Width:** 480px
- **Tab:** Pending Principals — table of non-acknowledging principals with branch, last login, [Send Reminder ↻]
- **Bulk:** [Send All Reminders] button at top

---

## 7. Charts

### 7.1 User Growth Trend
- **Type:** Line chart
- **Data:** Monthly new users provisioned (last 12 months)
- **X-axis:** Months
- **Y-axis:** Count
- **Tooltip:** Month · New users: N · Total cumulative: N
- **Export:** PNG

### 7.2 Policy Acknowledgement Donut
- **Type:** Doughnut
- **Data:** Acknowledged vs Pending per latest policy
- **Colours:** Green (acknowledged) · Red (pending)
- **Centre text:** "X of Y principals"
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| User created | "Account created and invite sent to [Name]" | Success | 4s |
| User updated | "[Name]'s account updated" | Success | 4s |
| User suspended | "[Name]'s account suspended" | Warning | 6s |
| Password reset sent | "OTP reset sent to [Name]'s mobile" | Info | 4s |
| Policy reminder sent | "Reminder sent to [N] principals" | Success | 4s |
| Create error (duplicate mobile) | "Mobile number already registered. Use Edit to update." | Error | Manual |
| Create error (server) | "Failed to create account. Try again." | Error | Manual |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No pending user requests | "No provisioning requests" | "Branch principals haven't submitted any user creation requests" | — |
| No principals found (search) | "No principals match your search" | "Try a different name or branch" | [Clear Search] |
| No active onboarding | "No branches in pipeline" | "All branches are live. Add a new branch to begin onboarding." | [+ Start Onboarding] |
| All policies acknowledged | "All principals are up to date" | "Every principal has acknowledged the latest policies" | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 5 KPI cards + table rows (8 skeleton) + Kanban cards |
| Principal table filter/search | Inline skeleton rows |
| Pending queue load | Inline skeleton rows |
| User create submit | Spinner in submit button + drawer blocked |
| Policy reminder send | Spinner + "Sending…" text in button |

---

## 11. Role-Based UI Visibility

| Element | MD G5 | Others |
|---|---|---|
| Page | ✅ | ❌ Redirected |
| [+ Provision User] header button | ✅ | N/A |
| [Approve & Create] in queue | ✅ | N/A |
| [Reject] in queue | ✅ | N/A |
| Edit / Suspend / Reset on principals table | ✅ | N/A |
| [Send Reminder] on policy table | ✅ | N/A |
| Export options | ✅ | N/A |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/md/dashboard/` | JWT (G5) | Full dashboard data |
| GET | `/api/v1/group/{id}/users/?role=principal` | JWT (G5) | Principal accounts list |
| GET | `/api/v1/group/{id}/users/requests/` | JWT (G5) | Pending provisioning requests |
| POST | `/api/v1/group/{id}/users/` | JWT (G5) | Create new user account |
| PUT | `/api/v1/group/{id}/users/{user_id}/` | JWT (G5) | Update user |
| POST | `/api/v1/group/{id}/users/{user_id}/suspend/` | JWT (G5) | Suspend user |
| POST | `/api/v1/group/{id}/users/{user_id}/reset-password/` | JWT (G5) | Trigger OTP reset |
| POST | `/api/v1/group/{id}/users/requests/{req_id}/approve/` | JWT (G5) | Approve provisioning request |
| POST | `/api/v1/group/{id}/users/requests/{req_id}/reject/` | JWT (G5) | Reject with reason |
| GET | `/api/v1/group/{id}/policies/?latest=true` | JWT (G5) | Policy acknowledgement status |
| POST | `/api/v1/group/{id}/policies/{policy_id}/remind/` | JWT (G5) | Send acknowledgement reminder |
| GET | `/api/v1/group/{id}/users/growth-trend/` | JWT (G5) | Monthly user provisioning trend |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Principal search | `input delay:300ms` | GET `.../users/?q={val}&role=principal` | `#principal-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../users/?filters={…}` | `#principal-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../users/?page={n}` | `#principal-table-section` | `innerHTML` |
| Open user-create drawer | `click` | GET `.../users/create-form/` | `#drawer-body` | `innerHTML` |
| Submit user-create form | `submit` | POST `.../users/` | `#drawer-body` | `innerHTML` |
| Approve request | `click` | POST `.../requests/{id}/approve/` | `#pending-queue` | `innerHTML` |
| Send policy reminder | `click` | POST `.../policies/{id}/remind/` | `#policy-row-{id}` | `outerHTML` |
| KPI stats auto-refresh | `every 5m` | GET `.../md/dashboard/stats/` | `#md-stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
