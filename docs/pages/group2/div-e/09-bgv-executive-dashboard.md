# 09 — Group BGV Executive Dashboard

- **URL:** `/group/hr/bgv/executive/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group BGV Executive (Role 49, G3)

---

## 1. Purpose

The Group BGV Executive Dashboard is the operational workstation for BGV Executives who handle the day-to-day processing of individual background verification cases across the group. While the BGV Manager (Role 48) sets strategy and monitors compliance rates, the BGV Executive handles the actual mechanics: initiating verification requests with external agencies, following up on pending responses, uploading agency reports, requesting document re-submissions from staff, and updating case statuses as verification components are cleared or failed.

In a large group with 3,000+ staff and a mandatory 3-year renewal cycle, a single BGV Executive might manage 60–100 active cases at any time. This dashboard is designed to maximise processing efficiency by surfacing the most time-sensitive cases first. The page defaults to sorting by "Days Outstanding" so the executive immediately sees which cases are at risk of breaching the 45-day target completion SLA. Cases that have been with an agency for more than 7 days without an update are surfaced as a "follow-up due" queue, prompting the executive to contact the agency proactively.

Document management is a frequent friction point in BGV processing. Staff often submit incomplete or unclear identity documents, address proofs, or experience certificates. The executive uses this dashboard to flag a case as "Documents Pending from Staff," which sends an automated notification to the staff member with a specific list of what is required and a 5-day re-submission deadline. The dashboard tracks how many cases are blocked at this stage, allowing the BGV Manager to identify systemic issues (e.g., a branch where staff onboarding is not collecting documents properly).

BGV Executives do not have visibility into other executives' assigned cases, salary information, appraisal records, or any HR data outside the BGV domain. Their access is tightly scoped to their own verification queue, ensuring data minimisation consistent with privacy best practices.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group BGV Executive | G3 | Own assigned cases only | Primary role; scoped to assigned queue |
| Group BGV Manager | G3 | Full read + can reassign cases | Supervisory access |
| Group HR Manager | G3 | Read-only on BGV data | Monitoring only |
| Group HR Director | G3 | Read-only on BGV data | Receives escalations |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → Background Verification → Executive Dashboard
```

### 3.2 Page Header
- **Title:** `My BGV Processing Queue`
- **Subtitle:** `[N] Assigned Cases · [N] Completed This Week · [N] Follow-ups Due`
- **Role Badge:** `Group BGV Executive`
- **Right-side controls:** `Log Agency Update` (quick action) · `Escalate to Manager` · `Export My Cases`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any assigned case has failed verification component | "[N] of your assigned cases have a FAILED verification component. Update manager immediately." | Red |
| Agency no response > 7 days | "[N] case(s) have had no agency response for more than 7 days. Follow-up required today." | Red |
| Documents pending from staff > 5 days | "[N] staff member(s) have not re-submitted requested documents for more than 5 days. Escalate." | Amber |
| Cases approaching 45-day SLA (< 5 days remaining) | "[N] case(s) will breach the 45-day target completion SLA within 5 days." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| My Assigned Cases | Total cases currently assigned to this executive | Blue | Full queue table |
| Initiated Today | Cases for which initiation was submitted today | Blue | Filtered list |
| Agency Follow-up Due | Cases with agency pending > 7 days without update | Red if > 0, Green if 0 | Filtered table |
| Documents Pending from Staff | Cases blocked awaiting document re-submission | Amber if > 0 | Filtered table |
| Completed This Week | Cases marked Complete in current calendar week | Green | Completed log |
| Escalation Required | Cases flagged for manager escalation by the executive | Red if > 0 | Filtered table |

---

## 5. Main Table — My BGV Processing Queue

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff Name | Text (link to case detail) | Yes | Yes (text search) |
| Branch | Text | Yes | Yes (multi-select) |
| Case ID | Text (e.g., BGV-2026-0312) | Yes | No |
| Verification Type(s) | Multi-badge (Police / Education / Employer / Identity / Address) | No | Yes (checkbox) |
| Agency | Text | Yes | Yes (text) |
| Days Outstanding | Integer (colour: Green <21, Amber 21–40, Red >40) | Yes | Yes (> N) |
| Last Update | Date-time | Yes | Yes (date range) |
| Staff Documents Status | Badge (Complete / Pending Re-submission / Incomplete) | Yes | Yes |
| Case Status | Badge (Initiated / In Progress / Agency Follow-up / Docs Pending / Completed / Failed) | Yes | Yes |
| Actions | Log Update / Request Docs / Complete / Escalate / View | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Case Status | Checkbox | Initiated / In Progress / Agency Follow-up / Docs Pending / Completed / Failed |
| Verification Type | Checkbox | Police / Education / Previous Employer / Identity / Address |
| Days Outstanding | Range input | > N days |
| Branch | Multi-select dropdown | All branches (executive may serve multiple) |
| Documents Status | Checkbox | Complete / Pending / Incomplete |

### 5.2 Search
- Full-text: Staff name, Case ID, agency name
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `bgv-case-detail` — View Full Case Detail
- **Trigger:** Click on staff name
- **Width:** 720px
- Shows: Staff name, branch, role, join date, Case ID, all verification components with individual status, agency name and contact, all log entries in chronological order, document uploads list, days outstanding, SLA status, escalation history

### 6.2 Drawer: `bgv-log-update` — Log Agency Update
- **Trigger:** Actions → Log Update or "Log Agency Update" header button
- **Width:** 480px
- **Fields:**
  - Case ID / Staff Name (required, searchable from own queue)
  - Verification Component (required, dropdown: Police / Education / Employer / Identity / Address)
  - Update Type (required, radio: Agency Acknowledged / In Process / Result Received / Clarification Requested)
  - Agency Reference / Tracking ID (optional, text)
  - Update Notes (required, textarea, min 30 chars)
  - Document Upload (optional, PDF/image; agency report)
  - Updated Expected Completion Date (optional, date picker)

### 6.3 Drawer: `bgv-request-docs` — Request Document Re-submission from Staff
- **Trigger:** Actions → Request Docs
- **Width:** 480px
- **Fields:**
  - Staff Name (read-only)
  - Documents Required (checkboxes: Aadhaar / PAN / Passport / Previous Employer Letter / Education Certificates / Address Proof / Passport Photo)
  - Additional Document Description (optional, text)
  - Re-submission Deadline (required, date picker; default 5 days)
  - Message to Staff (required, textarea; sent via platform notification + email)

### 6.4 Modal: Mark Case as Completed
- Confirmation: "You are marking BGV as Completed for [Staff Name]. Ensure all verification components are cleared. Once marked Complete, the BGV Manager will be notified and the record will be locked."
- Final status dropdown: Cleared / Conditional (minor discrepancy noted) / Failed
- Buttons: Mark Complete · Cancel

---

## 7. Charts

### 7.1 My Case Status Breakdown (Donut Chart)
- Segments: Initiated / In Progress / Agency Follow-up / Docs Pending / Completed / Failed
- Scoped to this executive's assigned cases only
- Quick visual of how the workload is distributed across stages

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Update logged | "Agency update logged for [Staff Name] — Case [ID]." | Success | 3s |
| Document request sent | "Document re-submission request sent to [Staff Name]. Deadline: [Date]." | Success | 4s |
| Case marked complete | "BGV marked as [Cleared / Conditional / Failed] for [Staff Name]. BGV Manager notified." | Success | 5s |
| Escalation submitted | "Case [ID] escalated to BGV Manager. They have been notified." | Warning | 5s |
| Validation error | "Please complete all required fields before submitting." | Error | 5s |
| Agency update with no notes | "Agency notes are required for all update log entries." | Error | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No cases assigned | "No Cases Assigned" | "No background verification cases have been assigned to you yet. Contact the BGV Manager." | — |
| All cases completed | "Queue Clear" | "All your assigned cases have been completed. Great work." | View Completed Log |
| No follow-ups due | "No Follow-ups Due" | "All agency cases have been updated within the last 7 days." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Skeleton: 6 KPI shimmer + table skeleton (10 rows) |
| Case detail drawer open | Drawer spinner; log entries load progressively |
| Log update form submit | Button spinner + form disabled |
| Document request submit | Button spinner; notification dispatch indicator |

---

## 11. Role-Based UI Visibility

| Element | BGV Executive (G3 — own cases) | BGV Manager (G3) | HR Manager (G3) | HR Director (G3) |
|---|---|---|---|---|
| KPI Summary Bar | Visible (own data only) | Visible (all executives aggregate) | Read-only on manager page | Read-only on director page |
| Processing Queue Table | Visible (own cases) | Full view on manager page | Read-only on manager page | Read-only |
| Log Update Button | Visible | Visible (can log on any case) | Not on this page | Not on this page |
| Request Docs Button | Visible | Visible | Not on this page | Not on this page |
| Mark Complete Button | Visible | Visible | Not on this page | Not on this page |
| Escalate Button | Visible | Not applicable | Not applicable | Not applicable |
| Other executives' queues | Never shown (scoped) | Visible on manager page | Not on this page | Not on this page |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/bgv/executive/kpis/` | JWT (G3 — scoped) | Exec-scoped KPI values |
| GET | `/api/v1/hr/bgv/executive/queue/` | JWT (G3 — scoped) | Paginated list of assigned cases |
| GET | `/api/v1/hr/bgv/executive/queue/{id}/` | JWT (G3 — scoped) | Full case detail |
| POST | `/api/v1/hr/bgv/executive/queue/{id}/log-update/` | JWT (G3 — scoped) | Log an agency update |
| POST | `/api/v1/hr/bgv/executive/queue/{id}/request-docs/` | JWT (G3 — scoped) | Send doc re-submission request to staff |
| POST | `/api/v1/hr/bgv/executive/queue/{id}/complete/` | JWT (G3 — scoped) | Mark case as completed (Cleared/Conditional/Failed) |
| POST | `/api/v1/hr/bgv/executive/queue/{id}/escalate/` | JWT (G3 — scoped) | Escalate case to BGV Manager |
| GET | `/api/v1/hr/bgv/executive/charts/status-breakdown/` | JWT (G3 — scoped) | Exec-scoped case status donut data |
| GET | `/api/v1/hr/bgv/executive/export/` | JWT (G3 — scoped) | Export of own case log |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/hr/bgv/executive/kpis/` | `#kpi-bar` | `innerHTML` |
| Load processing queue | `load` | GET `/api/v1/hr/bgv/executive/queue/` | `#queue-table` | `innerHTML` |
| Open case detail drawer | `click` on staff name | GET `/api/v1/hr/bgv/executive/queue/{id}/` | `#case-drawer` | `innerHTML` |
| Submit log update form | `click` on Submit Update | POST `/api/v1/hr/bgv/executive/queue/{id}/log-update/` | `#case-log` | `innerHTML` |
| Submit doc request | `click` on Send Request | POST `/api/v1/hr/bgv/executive/queue/{id}/request-docs/` | `#doc-request-result` | `innerHTML` |
| Filter by case status | `change` on status filter | GET `/api/v1/hr/bgv/executive/queue/?status=...` | `#queue-table` | `innerHTML` |
| Paginate queue table | `click` on page control | GET `/api/v1/hr/bgv/executive/queue/?page=N` | `#queue-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
