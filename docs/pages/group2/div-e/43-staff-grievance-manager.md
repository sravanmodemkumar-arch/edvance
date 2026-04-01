# 43 — Staff Grievance Manager

- **URL:** `/group/hr/welfare/grievances/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Employee Welfare Officer (Role 52, G3)

---

## 1. Purpose

The Staff Grievance Manager handles formal staff complaints that have been escalated from branch level to Group HR. A grievance is a written, formal complaint submitted by a staff member about a specific workplace issue — as distinguished from an informal concern or verbal complaint. Grievances escalated to Group HR are those which branch-level resolution failed or was not attempted within the prescribed window. This page is the operational hub for the Group Employee Welfare Officer to receive, assign, investigate, and close escalated grievances.

Grievance types recognised in the system are: Salary Related (incorrect pay, deduction disputes, arrears not credited), Working Condition (unsafe physical environment, equipment failure, inadequate facilities), Attendance and Leave Policy (wrongful leave denial, attendance record discrepancy, leave encashment dispute), Promotion Dispute (overlooked for promotion, non-transparent appraisal process), Interpersonal Conflict (harassment between peers, hostile work environment that does not rise to POSH threshold), and Harassment (non-POCSO, non-POSH — general bullying, intimidation). Grievances that involve sexual harassment are routed to the POSH Compliance process (page 46) and are excluded from this tracker.

The prescribed resolution process is: Staff member files grievance with branch → Branch Principal acknowledges within 48 hours → If unresolved in 7 calendar days → Auto-escalated to Group HR Welfare Officer → Welfare Officer assigns to self or HR Manager for investigation → Investigation period → Resolution communicated in writing → Grievance closed. Group HR SLA is 15 working days from date of escalation. Grievances unresolved beyond 15 days are flagged as SLA Breached and reported to the HR Director. Persistent unresolved cases escalated to the Labour Commissioner represent institutional risk and are highlighted in red.

This page is P0 because failure to address escalated grievances within SLA creates legal exposure and can result in labour tribunal complaints. The Welfare Officer must monitor SLA breach risk daily. Volume, resolution time, and repeat grievances from the same branch are leading indicators of management problems at branch level. All grievance records are permanently stored and cannot be deleted — only closed or escalated further.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Employee Welfare Officer | G3 | Full CRUD + Assign + Close + Escalate | Primary operator |
| Group HR Director | G3 | Full read + Escalate to external body | Oversight; receives escalations |
| Group HR Manager | G3 | Read + Add Resolution Note | Assigned as investigation handler |
| Branch Principal | G3 | Read-only (own branch grievances) | Row-level filter enforced |
| Group Performance Review Officer | G1 | Read-only | Contextual — sees grievances that touch appraisals |
| All other roles | — | No access | Page not rendered |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › Employee Welfare › Grievance Manager
```

### 3.2 Page Header

- **Title:** Staff Grievance Manager
- **Subtitle:** Manage escalated staff grievances — SLA: 15 working days
- **Primary CTA:** `+ Log Grievance` (manual entry by Welfare Officer on behalf of staff)
- **Secondary CTA:** `Export` (CSV/PDF)
- **Header badge:** Count of active grievances with SLA < 3 days remaining shown in red

### 3.3 Alert Banner (conditional)

- **Red:** `[N] grievances have breached the 15-working-day SLA. Immediate action required.` Action: `View Overdue`
- **Amber:** `[N] grievances have less than 3 working days remaining on SLA.` Action: `View At-Risk`
- **Red (escalation risk):** `[N] grievances flagged for potential Labour Commissioner escalation.` Action: `Review`
- **Green:** All grievances within SLA and no overdue — shown when no active alerts

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Grievances | Count of all open grievances (status ≠ Closed) | Blue always | Filter table to open records |
| SLA Breached (Overdue) | Count where working days since escalation > 15 and status ≠ Closed | Red if > 0, else green | Filter to breached rows |
| Resolved This Month | Count closed in current calendar month | Green always | Filter to month's closures |
| Average Resolution Time | Avg(closed_date − escalation_date) in working days for last 30 days | Green if ≤ 10 days, amber 11–15, red > 15 | No drill-down |
| Escalations to HR Director | Count escalated beyond Welfare Officer in last 30 days | Amber if > 0, else grey | Filter to escalated rows |
| Filed This Week | Count of grievances with filed_date in current ISO week | Blue always | Filter to this week |

---

## 5. Main Table — Grievances Register

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Grievance ID | Text (auto, e.g., GRV-2526-0087) | No | No |
| Staff Name | Text | Yes (A–Z) | Yes — text search |
| Branch | Text | Yes | Yes — dropdown |
| Type | Badge (colour-coded by grievance type) | No | Yes — checkbox group |
| Filed Date | Date | Yes | Yes — date range |
| SLA Deadline | Date + countdown chip | Yes | Yes — overdue toggle |
| Assigned To | Text (staff name or "Unassigned") | Yes | Yes — dropdown |
| Status | Badge (New / Under Investigation / Pending Staff Response / Resolved / Closed / Escalated) | No | Yes — checkbox group |
| Priority | Badge (Low / Medium / High / Critical) | Yes | Yes — dropdown |
| Actions | Icon buttons: View / Assign / Add Note / Close / Escalate | No | No |

### 5.1 Filters

- **Branch:** Multi-select dropdown
- **Grievance Type:** Checkboxes — all 6 types
- **Status:** Checkboxes — New, Under Investigation, Pending Staff Response, Resolved, Closed, Escalated
- **Priority:** Checkboxes — Low, Medium, High, Critical
- **SLA Status:** Toggle — Breached / At Risk (≤ 3 days) / Within SLA / All
- **Assigned To:** Dropdown of HR staff
- **Filed Date Range:** From / To date picker
- **Reset Filters** button

### 5.2 Search

Search bar queries: Grievance ID, Staff Name. Minimum 2 characters; 400 ms debounce.

### 5.3 Pagination

Server-side. Default 20 rows. Options: 10 / 20 / 50. "Showing X–Y of Z grievances."

---

## 6. Drawers

### 6.1 Log Grievance (Create)

Triggered by `+ Log Grievance`. Manual entry for Welfare Officer.

**Fields:**
- Staff Name (searchable dropdown from staff directory)
- Branch (auto-filled from staff profile)
- Designation (auto-filled)
- Grievance Type (dropdown — 6 types)
- Priority (dropdown: Low / Medium / High / Critical)
- Filed Date (date picker — defaults to today)
- Subject (text input, max 150 characters)
- Grievance Description (textarea, minimum 100 characters)
- Branch-Level Acknowledgement Date (date picker)
- Branch Resolution Attempted: Yes / No
- If No: reason (textarea)
- Escalation Date to Group HR (date — defaults to today)
- Supporting Document Upload (PDF/image, optional, max 5 MB)
- Assign To (dropdown of HR staff — defaults to Welfare Officer)

**Validation:** Description minimum 100 characters; filed date ≤ today; if branch resolution attempted = Yes, acknowledgement date required.

**Submit:** `Log Grievance` → POST `/api/hr/welfare/grievances/` → Table refresh

### 6.2 View Grievance

Full side drawer with complete grievance details.

**Displays:**
- Grievance ID, Staff profile snippet (name, branch, role, photo thumbnail)
- Filed date, Escalation date, SLA deadline with countdown
- Full grievance description
- Branch action history (acknowledgement, resolution attempt)
- All resolution notes (chronological thread)
- Current status and assigned handler
- Uploaded documents (signed URLs, opens in new tab)
- Audit log: all status changes with timestamp and actor

### 6.3 Assign Handler

Triggered by Assign icon.

**Fields:**
- Grievance ID (locked)
- Current assignee (read-only)
- New Assignee (searchable dropdown — HR staff)
- Assignment Note (textarea, optional)
- Notify Assignee: checkbox (triggers in-app notification)

**Submit:** `Assign` → PATCH `/api/hr/welfare/grievances/{id}/assign/`

### 6.4 Add Resolution Note

Triggered by Note icon. Appends to resolution thread.

**Fields:**
- Grievance ID (locked)
- Note Type (dropdown: Investigation Update / Staff Communication / Management Response / Document Request / Internal Note)
- Note Content (textarea, minimum 50 characters)
- Status Update (dropdown — can change grievance status from this drawer)
- Upload Evidence (optional, PDF/image, max 5 MB)
- Visible to Staff: checkbox (if checked, staff can view note via branch portal)

**Submit:** `Add Note` → POST `/api/hr/welfare/grievances/{id}/notes/`

### 6.5 Close Grievance

**Fields:**
- Grievance ID (locked)
- Resolution Summary (textarea, minimum 100 characters)
- Resolution Type (dropdown: Resolved in Favour of Staff / Resolved in Favour of Management / Mutual Resolution / Withdrawn by Staff / No Merit Found)
- Date Resolved (date picker)
- Resolution Communication Method (dropdown: Email / Letter / In-Person Meeting)
- Staff Acknowledged Resolution: Yes / No
- Upload Resolution Letter (PDF, required)

**Submit:** `Close Grievance` → PATCH `/api/hr/welfare/grievances/{id}/close/`

### 6.6 Escalate

Available to Welfare Officer and HR Director.

**Fields:**
- Grievance ID (locked)
- Escalate To (dropdown: HR Director / Grievance Redressal Committee / Labour Commissioner / Management Board)
- Escalation Reason (textarea, minimum 100 characters)
- Escalation Date (auto-set to today)
- Upload Escalation Document (PDF, optional)

**Submit:** `Escalate` → PATCH `/api/hr/welfare/grievances/{id}/escalate/`

---

## 7. Charts

No dedicated charts section on this page. Grievance volume trends and SLA performance charts are visible on the HR Analytics Dashboard (page 47) and the Employee Welfare Officer Dashboard (page 12).

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| Grievance logged | Success | "Grievance GRV-XXXX logged and assigned to [name]." |
| Handler assigned | Success | "Grievance GRV-XXXX assigned to [name]." |
| Note added | Success | "Resolution note added to GRV-XXXX." |
| Grievance closed | Success | "GRV-XXXX closed. Resolution recorded." |
| Grievance escalated | Warning | "GRV-XXXX escalated to [recipient]. SLA clock continues." |
| SLA breach detected | Warning | "GRV-XXXX has breached the 15-working-day SLA." |
| Form validation error | Error | "Please complete all required fields before submitting." |
| Server error | Error | "Failed to save. Please retry or contact support." |

---

## 9. Empty States

**No grievances in table:**
> Icon: handshake / peace symbol
> "No grievances have been escalated to Group HR."
> "All branch-level issues appear to be resolved at source."

**Filtered results return nothing:**
> Icon: magnifying glass
> "No grievances match your current filters."
> CTA: `Reset Filters`

---

## 10. Loader States

- Page load: Skeleton table (6 rows × 10 columns), skeleton KPI cards
- Drawer open: Spinner in drawer while fetching grievance detail
- Note thread load: Inline spinner inside thread section
- Table refresh after action: Skeleton overlay on table body only
- KPI cards: Individual shimmer while metrics recalculate

---

## 11. Role-Based UI Visibility

| UI Element | Welfare Officer | HR Director | HR Manager | Branch Principal |
|---|---|---|---|---|
| `+ Log Grievance` button | Visible | Visible | Hidden | Hidden |
| Assign Handler action | Visible | Visible | Hidden | Hidden |
| Add Resolution Note | Visible | Visible | Visible | Hidden |
| Close Grievance action | Visible | Visible | Hidden | Hidden |
| Escalate action | Visible | Visible | Hidden | Hidden |
| Export button | Visible | Visible | Hidden | Hidden |
| All branches in table | Yes | Yes | Yes | Own branch only |
| Delete (soft) | Hidden | Hidden | Hidden | Hidden — no deletion allowed |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/welfare/grievances/` | Paginated list with filters |
| POST | `/api/hr/welfare/grievances/` | Create new grievance record |
| GET | `/api/hr/welfare/grievances/{id}/` | Single grievance detail |
| PATCH | `/api/hr/welfare/grievances/{id}/assign/` | Assign/reassign handler |
| POST | `/api/hr/welfare/grievances/{id}/notes/` | Add resolution note |
| PATCH | `/api/hr/welfare/grievances/{id}/close/` | Close grievance |
| PATCH | `/api/hr/welfare/grievances/{id}/escalate/` | Escalate grievance |
| GET | `/api/hr/welfare/grievances/kpis/` | KPI summary bar data |
| GET | `/api/hr/welfare/grievances/{id}/audit-log/` | Audit trail for a grievance |

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| Table initial load | `hx-get` triggered on page render | Fetches paginated grievance list |
| Filter/search change | `hx-get` with `hx-trigger="change"` and `hx-include` | Submits all active filters, swaps `#table-body` |
| Search input | `hx-trigger="keyup changed delay:400ms"` | Debounced search on Grievance ID / Staff Name |
| Pagination click | `hx-get` on page buttons | Fetches page N, swaps table body |
| Drawer open | `hx-get` on action icon + `hx-target="#drawer"` | Loads drawer content for specific grievance |
| Log grievance form | `hx-post` + `hx-target="#table-body"` | Posts form, gets updated table on 201 |
| Add note form | `hx-post` + `hx-target="#note-thread-{id}"` | Appends new note to thread in-place |
| Assign / Close / Escalate | `hx-patch` + `hx-target="#row-{id}"` | Updates single row without full table reload |
| Toast notification | `hx-swap-oob` on `#toast-container` | Out-of-band injection of toast message |
| KPI refresh | `hx-get` on `#kpi-bar` after mutations | Reloads KPI values after status changes |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
