# 07 — Group Staff Transfer Coordinator Dashboard

- **URL:** `/group/hr/transfers/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Staff Transfer Coordinator (Role 47, G3)

---

## 1. Purpose

The Group Staff Transfer Coordinator Dashboard manages all inter-branch staff transfers within the group's school network. Inter-branch transfers are a sensitive HR operation because they directly affect branch-level staffing strength, teaching continuity, and staff morale. A critical policy rule enforced by this system is that no branch can self-initiate a teacher transfer — all inter-branch moves must be approved and coordinated exclusively by Group HR. This prevents branches from dumping underperforming staff on sister branches, circumventing performance management protocols, or creating invisible gaps in teaching coverage.

The coordinator's primary responsibility is to evaluate transfer requests, assess their operational impact on both the originating and receiving branches, and route them through the appropriate approval chain. Each transfer request undergoes an automated vacancy impact check: if approving the transfer would reduce the originating branch below 90% of its sanctioned strength in a critical subject or role, the system flags it as "Vacancy Risk" and requires the HR Director's sign-off before proceeding. This check prevents transfers from inadvertently creating teaching coverage crises mid-academic year.

Transfers fall into several categories that drive the urgency and approval pathway: Routine Transfers (scheduled, low urgency), Emergency Transfers (welfare-based or disciplinary, fast-tracked with 24-hour turnaround), and Administrative Transfers (group-initiated, e.g., a newly opened branch requiring experienced staff). Each category has its own SLA. The dashboard surface SLA breaches prominently so the coordinator can escalate before a transfer request is left in limbo.

The coordinator also maintains the record of completed transfers for the current academic year, which feeds into the HR Director's turnover analysis and the Group Accounts team's salary allocation adjustments. Staff remain linked to their original branch in the payroll system until the coordinator marks the transfer as "Executed," which triggers the branch reassignment across all dependent systems.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Staff Transfer Coordinator | G3 | Full read + write on transfer requests | Primary role |
| Group HR Director | G3 | Full read + final approval authority | Approves high-impact transfers |
| Group HR Manager | G3 | Full read | Monitors pipeline; no approval authority |
| Branch Principal | Branch-level | Can submit transfer requests; cannot view other branches' transfers | Request initiation only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → Staff Transfers
```

### 3.2 Page Header
- **Title:** `Group Staff Transfer Coordinator Dashboard`
- **Subtitle:** `[N] Pending Requests · [N] Executed This AY · AY [current academic year]`
- **Role Badge:** `Group Staff Transfer Coordinator`
- **Right-side controls:** `+ New Transfer Request` · `Transfer History` · `Export Transfer Log`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Transfer request pending > 5 days without action | "[N] transfer request(s) have exceeded the 5-day review SLA. Action required." | Red |
| Emergency transfer request received | "Emergency transfer request received for [Staff Name] at [Branch]. Requires 24-hour resolution." | Red |
| Vacancy Risk flag on pending transfer | "[N] pending transfer(s) are flagged for Vacancy Risk. HR Director sign-off required." | Amber |
| Transfer approved but not executed > 7 days | "[N] approved transfer(s) have not been marked Executed for more than 7 days." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Pending Transfer Requests | Requests awaiting coordinator review | Red if > 5, Amber 1–5, Green 0 | Filtered table (Pending status) |
| Approved (Execution Pending) | Transfers approved but not yet executed in the system | Amber if > 0 | Filtered table (Approved status) |
| Completed This AY | Fully executed transfers in current academic year | Blue | Transfer history |
| Transfers Blocked — Vacancy Risk | Requests flagged and blocked due to vacancy impact | Red if > 0 | Filtered table (Blocked status) |
| Emergency Transfers | Active emergency transfer requests | Red if > 0 | Filtered table (Emergency type) |
| Declined Requests | Requests declined in current AY | Blue (informational) | Transfer history (Declined) |

---

## 5. Main Table — Transfer Requests

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Request ID | Text (e.g., TRF-2026-0041) | Yes | No |
| Staff Name | Text (link to staff profile) | Yes | Yes (text search) |
| From Branch | Text | Yes | Yes (multi-select) |
| To Branch | Text | Yes | Yes (multi-select) |
| Role | Text | Yes | Yes |
| Transfer Type | Badge (Routine / Emergency / Administrative) | Yes | Yes |
| Reason | Short text summary | No | No |
| Requested By | Text (Principal name or self-request) | Yes | No |
| Requested Date | Date | Yes | Yes (date range) |
| Status | Badge (Pending / Under Review / Approved / Blocked / Executed / Declined) | Yes | Yes |
| Vacancy Impact | Badge (None / Low / High — Vacancy Risk) | Yes | Yes |
| Actions | Review / Approve / Decline / Execute | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Status | Checkbox | Pending / Under Review / Approved / Blocked / Executed / Declined |
| Transfer Type | Checkbox | Routine / Emergency / Administrative |
| Vacancy Impact | Checkbox | None / Low / High — Vacancy Risk |
| From / To Branch | Multi-select dropdown | All configured branches |
| Requested Date | Date range picker | Any range |

### 5.2 Search
- Full-text: Staff name, Request ID, branch names
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `transfer-create` — Create Transfer Request
- **Trigger:** `+ New Transfer Request` button
- **Width:** 560px
- **Fields:**
  - Staff Name (required, searchable dropdown from Staff Directory)
  - From Branch (required, auto-filled from staff record; editable)
  - To Branch (required, dropdown; cannot equal From Branch)
  - Transfer Type (required, radio: Routine / Emergency / Administrative)
  - Effective Date (required, date picker; must be > 14 days in future for Routine; any date for Emergency)
  - Reason Category (required, dropdown: Professional Development / Workload Rebalancing / Staff Request / Administrative Requirement / Disciplinary / Welfare / Other)
  - Detailed Reason (required, textarea, min 80 chars)
  - Supporting Documents (file upload, optional; PDF/images, max 5 files, 10MB each)
- **Validation:** To Branch ≠ From Branch; effective date rules by type; system auto-runs vacancy impact check on submission

### 6.2 Drawer: `transfer-review` — Review Transfer Request
- **Trigger:** Actions → Review
- **Width:** 720px
- Shows: Full request details, staff profile summary (role, join date, current branch tenure), Vacancy Impact Analysis panel (staffing strength at From Branch before/after, From Branch's sanctioned vs. actual post-transfer), To Branch current strength, Coordinator Notes textarea, Recommend Approve / Recommend Decline / Flag Vacancy Risk buttons

### 6.3 Drawer: `transfer-execute` — Mark Transfer as Executed
- **Trigger:** Actions → Execute (only for Approved status)
- **Width:** 400px
- **Fields:**
  - Actual Transfer Date (required, date picker)
  - Relieving Order Reference (required, text)
  - Joining Report at New Branch (required, text — reference number)
  - Notes (optional textarea)
- On submit: Updates staff branch in system, triggers salary branch reallocation notification to Finance

### 6.4 Modal: Decline Transfer Request
- Confirmation: "You are declining the transfer request for [Staff Name] from [Branch A] to [Branch B]. Reason must be provided. The requesting branch will be notified."
- Fields: Decline Reason (required, textarea, min 50 chars)
- Buttons: Confirm Decline · Cancel

---

## 7. Charts

### 7.1 Transfer Activity by Month (Bar Chart)
- **X-axis:** Months in current academic year
- **Series 1:** Requests received (blue)
- **Series 2:** Requests executed (green)
- **Series 3:** Requests declined (red)

### 7.2 Transfer Flow by Branch (Sankey / Table Heat Map)
- Shows which branches are the highest sources and recipients of transfers
- Rendered as a heat-map table (From Branch rows × To Branch columns; cell value = count)
- Highlights branches that are consistently losing staff (likely management or culture issues)

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Transfer request created | "Transfer request [TRF-ID] submitted. Vacancy impact check in progress." | Success | 4s |
| Transfer approved | "Transfer approved. Executing branch notified." | Success | 4s |
| Transfer declined | "Transfer request declined. Requesting branch notified." | Info | 4s |
| Transfer executed | "Transfer executed. Staff record updated to [New Branch]. Finance notified." | Success | 5s |
| Vacancy Risk auto-flagged | "Vacancy Risk detected. Request has been flagged. HR Director approval required." | Warning | 6s |
| Export triggered | "Transfer log export is being prepared." | Info | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No pending requests | "No Pending Transfers" | "All transfer requests have been reviewed. Nothing requires action." | View Transfer History |
| No transfers this AY | "No Transfers This Academic Year" | "No inter-branch transfers have been processed in the current academic year." | + New Transfer Request |
| No emergency transfers | "No Emergency Transfers" | "No emergency transfer requests are active." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full skeleton: 6 KPI shimmer + table skeleton (10 rows) |
| Transfer review drawer open | Drawer spinner; vacancy impact analysis panel loads separately |
| Transfer create form submit | Button spinner + vacancy impact check running indicator |
| Execute form submit | Button spinner + "Updating staff records…" indicator |

---

## 11. Role-Based UI Visibility

| Element | Transfer Coordinator (G3) | HR Director (G3) | HR Manager (G3) | Branch Principal |
|---|---|---|---|---|
| KPI Summary Bar | Visible (all 6) | Visible (all 6) | Visible (all 6) | Hidden |
| Transfer Requests Table | Visible + full actions | Visible + approval action | Visible (read-only) | Hidden (separate branch view) |
| + New Transfer Request | Visible | Visible | Hidden | Visible (branch-scoped only) |
| Vacancy Impact Analysis | Visible | Visible | Visible (read-only) | Hidden |
| Decline Button | Visible | Visible | Hidden | Hidden |
| Execute Button | Visible | Hidden (Director doesn't execute) | Hidden | Hidden |
| Transfer Flow Heat Map | Visible | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/transfers/kpis/` | JWT (G3) | All 6 KPI card values |
| GET | `/api/v1/hr/transfers/` | JWT (G3) | Paginated transfer requests table |
| POST | `/api/v1/hr/transfers/` | JWT (G3) | Create new transfer request + trigger vacancy check |
| GET | `/api/v1/hr/transfers/{id}/` | JWT (G3) | Transfer request detail for review drawer |
| POST | `/api/v1/hr/transfers/{id}/approve/` | JWT (G3) | Approve transfer (coordinator recommends; Director confirms) |
| POST | `/api/v1/hr/transfers/{id}/decline/` | JWT (G3) | Decline with reason |
| POST | `/api/v1/hr/transfers/{id}/execute/` | JWT (G3) | Mark transfer as executed; update staff record |
| GET | `/api/v1/hr/transfers/charts/activity/` | JWT (G3) | Monthly transfer activity bar chart data |
| GET | `/api/v1/hr/transfers/charts/flow/` | JWT (G3) | Branch-to-branch transfer flow heat map data |
| GET | `/api/v1/hr/transfers/export/` | JWT (G3) | Async export of transfer log |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/hr/transfers/kpis/` | `#kpi-bar` | `innerHTML` |
| Load transfers table | `load` | GET `/api/v1/hr/transfers/` | `#transfers-table` | `innerHTML` |
| Open transfer review drawer | `click` on Request ID | GET `/api/v1/hr/transfers/{id}/` | `#review-drawer` | `innerHTML` |
| Filter by status | `change` on status filter | GET `/api/v1/hr/transfers/?status=...` | `#transfers-table` | `innerHTML` |
| Submit create form | `click` on Submit | POST `/api/v1/hr/transfers/` | `#transfers-table` | `innerHTML` |
| Submit execute form | `click` on Confirm Execute | POST `/api/v1/hr/transfers/{id}/execute/` | `#transfer-row-{id}` | `outerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/hr/transfers/?page=N` | `#transfers-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
