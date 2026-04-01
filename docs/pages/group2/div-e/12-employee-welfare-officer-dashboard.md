# 12 — Group Employee Welfare Officer Dashboard

- **URL:** `/group/hr/welfare/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Employee Welfare Officer (Role 52, G3)

---

## 1. Purpose

The Group Employee Welfare Officer Dashboard manages all staff welfare programs, grievance resolution, medical insurance administration, and welfare events across the group's branch network. This role exists exclusively in large-group configurations — in smaller groups, welfare responsibilities are absorbed by the HR Manager. For large groups, however, the volume and diversity of welfare needs — spanning thousands of staff across 20–50 branches — requires a dedicated officer who can ensure that each staff member's welfare concerns are heard, tracked, and resolved within defined SLAs.

The grievance management function is the most operationally critical element of this dashboard. A grievance is any formal complaint raised by a staff member about their working conditions, treatment by management, salary discrepancies, physical environment, or interpersonal conflict. Unresolved grievances that fester become morale crises, union actions, or legal disputes. The welfare officer ensures every grievance has an assigned owner, a resolution timeline (SLA), and a documented outcome. The dashboard surfaces grievances approaching their SLA due date in amber and those past-due in red.

Medical insurance administration is the second major function. Most school groups provide group medical insurance coverage to permanent staff and their families. When a staff member files a claim, the welfare officer tracks it through the insurance process: from first notification to documentation to insurer submission to settlement. The dashboard shows claims currently in process, those rejected (requiring re-submission or escalation to the insurer), and those settled. The welfare officer also maintains the list of staff who are newly eligible for insurance (after probation completion) and ensures they are enrolled within the required timeframe.

The welfare events calendar allows the officer to plan and track morale-building initiatives across branches: sports days, cultural programs, awards ceremonies, health check-up camps, and counselling sessions. These are not mere amenities — they are measurable staff retention investments. The satisfaction survey tracking KPI monitors whether the annual staff satisfaction survey has been distributed and completed across all branches, providing the HR Director with data to inform policy decisions.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Employee Welfare Officer | G3 | Full read + write | Primary role; large-group only |
| Group HR Director | G3 | Full read + override | Receives escalation on high-priority grievances |
| Group HR Manager | G3 | Full read + grievance initiation | Can log grievances; welfare officer manages |
| Branch Principal | Branch-level | Can view own branch grievances only | Separate branch-scoped view |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → Employee Welfare
```

### 3.2 Page Header
- **Title:** `Group Employee Welfare Officer Dashboard`
- **Subtitle:** `[N] Active Grievances · [N] Insurance Claims in Process · AY [current academic year]`
- **Role Badge:** `Group Employee Welfare Officer`
- **Right-side controls:** `+ New Grievance` · `+ Log Insurance Claim` · `+ Welfare Event` · `Export Welfare Report`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any grievance of type "Harassment" pending > 3 days | "Harassment grievance from [Staff Name] at [Branch] has been pending for [N] days. Immediate attention required." | Red |
| Medical emergency reported | "Medical emergency reported for [Staff Name] at [Branch]. Contact HR Director and insurance provider immediately." | Red |
| Grievance SLA breached | "[N] grievance(s) have exceeded their SLA due date. Escalation to HR Director triggered." | Amber |
| Insurance enrollment pending for newly confirmed staff | "[N] staff member(s) who completed probation have not been enrolled in group insurance." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Grievances | Total open grievances group-wide | Red if > 10, Amber 1–10, Green 0 | Full grievances table |
| Grievances Resolved This Month | Formally closed grievances in current calendar month | Green | Resolved log |
| Insurance Claims in Process | Active insurance claims not yet settled | Blue | Insurance claims list |
| Welfare Events This Month | Welfare events scheduled or completed in current month | Blue | Events calendar |
| Satisfaction Survey Pending | Branches where annual survey has not been distributed or completed | Amber if > 0 | Survey tracker |
| Medical Emergencies Reported | Medical emergency incidents logged (current AY) | Red if > 0 | Emergency log |

---

## 5. Main Table — Active Grievances

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Grievance ID | Text (e.g., GRV-2026-0127) | Yes | No |
| Staff Name | Text (link to grievance detail) | Yes | Yes (text search) |
| Branch | Text | Yes | Yes (multi-select) |
| Grievance Type | Badge (Medical / Salary / Work Environment / Harassment / Interpersonal / Other) | Yes | Yes |
| Filed Date | Date | Yes | Yes (date range) |
| Assigned To | Text (welfare officer or delegate) | Yes | Yes |
| Status | Badge (Filed / Under Review / Mediation / Resolved / Escalated / Closed) | Yes | Yes |
| Priority | Badge (Low / Medium / High / Critical) | Yes | Yes |
| SLA Due Date | Date (red if past, amber if < 3 days, green otherwise) | Yes | Yes |
| Days Open | Integer | Yes | Yes (> N) |
| Actions | View / Update / Escalate / Close | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Grievance Type | Checkbox | Medical / Salary / Work Environment / Harassment / Interpersonal / Other |
| Status | Checkbox | Filed / Under Review / Mediation / Resolved / Escalated / Closed |
| Priority | Checkbox | Low / Medium / High / Critical |
| Branch | Multi-select dropdown | All configured branches |
| SLA Status | Radio | All / SLA Breached / SLA Due Within 3 Days / Within SLA |

### 5.2 Search
- Full-text: Staff name, Grievance ID, branch name
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `grievance-create` — Log New Grievance
- **Trigger:** `+ New Grievance` button
- **Width:** 560px
- **Fields:**
  - Staff Name (required, searchable dropdown from Staff Directory)
  - Branch (required, auto-filled from staff record)
  - Grievance Type (required, dropdown: Medical / Salary / Work Environment / Harassment / Interpersonal / Other)
  - Priority (required, radio: Low / Medium / High / Critical)
  - Grievance Description (required, textarea, min 80 chars; encrypted at rest for Harassment type)
  - Confidential (checkbox; if checked, description visible only to Welfare Officer and HR Director)
  - Filing Mode (required, radio: Staff Self-Filed / Filed on Behalf of Staff / Anonymous)
  - Assigned To (required, dropdown: Welfare Officer / HR Manager / Branch HR Contact)
  - SLA Days (required, integer; default by type: Harassment = 3, Medical = 2, Other = 7)
  - Supporting Documents (optional, PDF/images, max 3 files)

### 6.2 Drawer: `grievance-detail` — View Grievance Detail
- **Trigger:** Click on Staff Name or Grievance ID
- **Width:** 720px
- Shows: Full grievance description, timeline of all status updates with timestamps and notes, assigned owner history, documents attached, staff's acknowledgement of resolution (if resolved), escalation history

### 6.3 Drawer: `grievance-update` — Update Grievance Status
- **Trigger:** Actions → Update
- **Width:** 480px
- **Fields:**
  - New Status (required, dropdown)
  - Update Notes (required, textarea, min 40 chars)
  - Resolution Summary (required if Status = Resolved; textarea)
  - Staff Acknowledgement Received (checkbox; required for Resolved status)
  - Next Action Date (optional, date picker)

### 6.4 Drawer: `insurance-claim-log` — Log Insurance Claim
- **Trigger:** `+ Log Insurance Claim` button
- **Width:** 480px
- **Fields:**
  - Staff Name (required, searchable dropdown)
  - Insurance Policy Number (required, text; auto-filled from insurance record)
  - Claim Type (required, dropdown: Hospitalisation / OPD / Accident / Critical Illness / Maternity / Other)
  - Claim Amount (₹, required)
  - Hospital / Provider Name (required, text)
  - Date of Treatment (required, date picker)
  - Documents Submitted (checkbox list: Discharge Summary / Bills / Prescriptions / Lab Reports / TPA Form)
  - Status (required, dropdown: Documents Collected / Submitted to Insurer / Under Review / Approved / Rejected / Settled)

### 6.5 Modal: Close Grievance
- Confirmation: "You are closing Grievance [GRV-ID] for [Staff Name]. Ensure the resolution summary is complete and the staff member has acknowledged the resolution. This action is final."
- Buttons: Confirm Close · Cancel

---

## 7. Charts

### 7.1 Grievance Types Distribution (Donut Chart)
- Segments: Medical / Salary / Work Environment / Harassment / Interpersonal / Other
- Current AY data
- Helps identify systemic issues (e.g., cluster of Salary grievances may indicate payroll errors)

### 7.2 Grievance Resolution Trend (Line Chart)
- X-axis: Months in current AY
- Series 1: Grievances filed (blue line)
- Series 2: Grievances resolved (green line)
- Convergence of lines indicates healthy resolution velocity

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Grievance logged | "Grievance [GRV-ID] registered. Assigned to [Name]. SLA due: [Date]." | Success | 5s |
| Harassment grievance logged | "Harassment grievance registered. HR Director notified immediately." | Warning | 6s |
| Grievance status updated | "Grievance [GRV-ID] status updated to [Status]." | Success | 3s |
| Grievance closed | "Grievance [GRV-ID] closed. Resolution recorded in [Staff Name]'s welfare record." | Success | 4s |
| Insurance claim logged | "Insurance claim logged for [Staff Name]. TPA reference required within 5 days." | Success | 4s |
| SLA breach auto-escalated | "SLA breach for Grievance [GRV-ID] has been escalated to the HR Director." | Warning | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No active grievances | "No Active Grievances" | "All staff grievances have been resolved. This reflects well on the group's work environment." | View Resolved Log |
| No insurance claims | "No Active Insurance Claims" | "There are no insurance claims currently in process." | + Log Insurance Claim |
| No welfare events this month | "No Events This Month" | "No welfare events are scheduled for the current month. Consider planning one." | + Welfare Event |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full skeleton: 6 KPI shimmer + table skeleton (10 rows) |
| Grievance detail drawer open | Drawer spinner; timeline entries load progressively |
| Grievance create form submit | Button spinner + form disabled |
| Charts load | Shimmer overlay on each chart panel |

---

## 11. Role-Based UI Visibility

| Element | Welfare Officer (G3) | HR Director (G3) | HR Manager (G3) | Branch Principal |
|---|---|---|---|---|
| KPI Summary Bar | Visible (all 6) | Visible (all 6) | Visible (grievances + claims) | Visible (branch grievances only) |
| Active Grievances Table | Visible (all branches) | Visible (all) | Visible (all, read-only) | Visible (own branch only) |
| Grievance Description (Confidential) | Visible | Visible | Hidden | Hidden |
| + New Grievance Button | Visible | Visible | Visible | Visible (branch scope) |
| Insurance Claim Drawer | Visible | Visible | Hidden | Hidden |
| + Welfare Event Button | Visible | Hidden | Hidden | Hidden |
| Close Grievance Button | Visible | Visible | Hidden | Hidden |
| Charts | Visible | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/welfare/kpis/` | JWT (G3) | All 6 KPI values |
| GET | `/api/v1/hr/welfare/grievances/` | JWT (G3) | Paginated active grievances table |
| POST | `/api/v1/hr/welfare/grievances/` | JWT (G3) | Log a new grievance |
| GET | `/api/v1/hr/welfare/grievances/{id}/` | JWT (G3) | Grievance detail with full timeline |
| PATCH | `/api/v1/hr/welfare/grievances/{id}/` | JWT (G3) | Update grievance status and notes |
| POST | `/api/v1/hr/welfare/grievances/{id}/close/` | JWT (G3) | Close and archive grievance |
| GET | `/api/v1/hr/welfare/insurance-claims/` | JWT (G3) | List of insurance claims |
| POST | `/api/v1/hr/welfare/insurance-claims/` | JWT (G3) | Log a new insurance claim |
| GET | `/api/v1/hr/welfare/charts/grievance-types/` | JWT (G3) | Grievance distribution donut data |
| GET | `/api/v1/hr/welfare/charts/resolution-trend/` | JWT (G3) | Monthly filed vs. resolved line chart data |
| GET | `/api/v1/hr/welfare/export/` | JWT (G3) | Async welfare report export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/hr/welfare/kpis/` | `#kpi-bar` | `innerHTML` |
| Load grievances table | `load` | GET `/api/v1/hr/welfare/grievances/` | `#grievances-table` | `innerHTML` |
| Open grievance detail drawer | `click` on Grievance ID | GET `/api/v1/hr/welfare/grievances/{id}/` | `#grievance-drawer` | `innerHTML` |
| Filter by grievance type | `change` on type filter | GET `/api/v1/hr/welfare/grievances/?type=...` | `#grievances-table` | `innerHTML` |
| Filter by SLA status | `change` on SLA filter | GET `/api/v1/hr/welfare/grievances/?sla=...` | `#grievances-table` | `innerHTML` |
| Submit new grievance | `click` on Submit | POST `/api/v1/hr/welfare/grievances/` | `#grievances-table` | `innerHTML` |
| Submit grievance status update | `click` on Save Update | PATCH `/api/v1/hr/welfare/grievances/{id}/` | `#grievance-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
