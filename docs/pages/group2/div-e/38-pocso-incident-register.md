# 38 — POCSO Incident Register

- **URL:** `/group/hr/pocso/incidents/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group POCSO Coordinator (Role 50, G3)

---

## 1. Purpose

The POCSO Incident Register is the most sensitive and confidential page in the EduForge platform. It maintains the formal register of all POCSO-related incidents reported across all branches of the group. A POCSO incident is any incident involving a child (student) that may constitute an offence under the Protection of Children from Sexual Offences Act, 2012 — including sexual harassment, inappropriate physical contact, verbal or emotional abuse, or any other conduct by a staff member toward a student that violates the Act. The existence of this register, and the rigorous process of managing it, is both a legal obligation and a fundamental institutional safeguarding commitment.

Access to this page is strictly limited to the POCSO Coordinator and the HR Director. No other role — including branch principals, HR Managers, or senior group staff — can view, list, or search this register. Branch staff who witness or receive a complaint submit an incident report through a separate, restricted submission form (not this page); they do not have access to the register itself. The register is the post-submission management and investigation tool for the two designated role-holders only.

The escalation chain upon incident registration is mandatory and non-negotiable. Upon an incident being logged and acknowledged by the POCSO Coordinator: (1) HR Director is notified immediately within the system; (2) CEO/Chairman is notified through a separate formal communication process outside EduForge (email/phone); (3) Group POCSO Reporting Officer (Legal) is notified; (4) If the incident meets the threshold under the POCSO Act, the National Commission for Protection of Child Rights (NCPCR) must be notified within 24 hours of first knowledge, and this notification is logged in the register. Sexual offences carry an additional mandatory requirement: an FIR must be filed with the local police station. The EduForge system logs the FIR number, date filed, and police station, but does not remove the institution's obligation to act — the system is a documentation tool, not a substitute for legal compliance.

Each incident case progresses through a lifecycle: Reported (initial submission received) → POCSO Coordinator Acknowledged → Investigation Opened (internal, led by the Internal Complaints Committee) → NCPCR Reported (if applicable) → Resolved. Incidents are never deleted from this register — resolution simply moves the case to a Closed state with outcome documented. Every action taken is logged with timestamp and the name of the person who took the action.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group POCSO Coordinator | G3 | Full CRUD + Case Management | Primary case manager |
| Group HR Director | G3 | Full Read + Acknowledgement + Approve Escalation | Co-authority on all cases |
| Group HR Manager | G3 | No Access | Explicitly excluded |
| Group Training & Development Manager | G2 | No Access | Explicitly excluded |
| Group BGV Manager | G3 | No Access | Explicitly excluded |
| All Branch Roles | Any | No Access — submit only | Submission via restricted form, not this register |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > POCSO Compliance > POCSO Incident Register`

### 3.2 Page Header
- **Title:** POCSO Incident Register
- **Subtitle:** Confidential — Restricted to POCSO Coordinator and HR Director only
- **Confidentiality Banner (permanent, non-dismissible):** "This register is confidential. Access is logged. Unauthorised disclosure is a serious breach of policy and law."
- **Actions (top-right):**
  - `+ Log New Incident` (primary button — POCSO Coordinator only)
  - `Export Register` (secondary — password-protected export, requires 2FA confirmation)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Critical incident (sexual offence) not acknowledged within 2 hours | "CRITICAL: A Critical severity incident has not been acknowledged within 2 hours. Immediate action required." | Red — non-dismissible |
| NCPCR notification due (> 20 hours since first knowledge — 4-hour buffer before 24h deadline) | "URGENT: NCPCR notification deadline is in less than 4 hours for Case [ID]. File notification immediately." | Red — non-dismissible |
| Investigation open > 30 days without status update | "OVERDUE: Case [ID] has been in Investigation for more than 30 days without a status update." | Amber — dismissible |
| FIR not filed for Critical case > 24 hours | "LEGAL ALERT: FIR has not been filed for Critical Case [ID] within the required timeframe." | Red — non-dismissible |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Cases | Total open cases (all non-closed statuses) | Red if any Critical, Amber if > 0, Green if 0 | No drill-down |
| Pending Acknowledgement | Cases reported but not yet acknowledged by Coordinator | Red if > 0 (especially if > 2h old) | Filters to unacknowledged |
| Investigation Open | Cases currently in investigation stage | Amber if > 0 | Filters to investigation stage |
| NCPCR Reported | Count of cases where NCPCR notification filed | Blue (informational) | Filters to NCPCR reported |
| Resolved This Year | Cases closed in current calendar year | Green | Filters to resolved |
| Critical (Sexual Offence) Active | Count of Critical severity cases currently open | Red if > 0, Green if 0 | Filters to Critical severity |

---

## 5. Main Table — POCSO Incident Cases

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Case ID | Text (e.g., POCSO-2026-001) | No | No |
| Branch | Badge | Yes | Yes — dropdown |
| Incident Type | Badge (Sexual Harassment / Physical Harm / Verbal Abuse / Child Safety Violation / Other) | No | Yes — multi-select |
| Severity | Badge (Critical / Serious / Moderate) | No | Yes — dropdown |
| Reported Date | Date + time | Yes | Yes — date range |
| Status | Badge (Reported / Acknowledged / Investigation / NCPCR Reported / Resolved) | No | Yes — multi-select |
| NCPCR Reported | Icon (Y / N) | No | Yes — Yes/No |
| FIR Filed | Icon (Y / N / N/A) | No | Yes — Yes/No/NA |
| Actions | Icon buttons (View / Update Stage / Escalate) | No | No |

### 5.1 Filters
- **Severity:** Critical / Serious / Moderate
- **Status:** multi-select
- **Branch:** dropdown
- **NCPCR Reported:** Yes / No
- **Reported Date Range:** date picker
- **Has FIR:** Yes / No / N/A

### 5.2 Search
Search by Case ID only (no free-text name search — privacy protection). Debounced `hx-get` on keyup (400 ms).

### 5.3 Pagination
Server-side, 10 rows per page (deliberately smaller — this is a sensitive register not intended for bulk scanning). Shows `Showing X–Y of Z cases`.

---

## 6. Drawers

### 6.1 Log New Incident
**Trigger:** `+ Log New Incident` button (POCSO Coordinator only)
**Fields:**
- Branch (dropdown, required)
- Incident Date and Time
- Incident Type (dropdown, required)
- Severity Assessment (radio: Critical / Serious / Moderate — with definitions shown)
- Incident Description (textarea, required — minimum 100 characters)
- Alleged Staff Member (searchable dropdown — note: name is logged but NOT shown in the main table publicly)
- Victim Details (age range only — e.g., "Under 10 / 10–14 / 14–18" — full details stored securely, not shown in table)
- Initial Evidence (file upload — accepts PDF, JPG, PNG)
- Escalation Checklist (checkboxes, auto-checked but require manual confirmation):
  - HR Director notified
  - CEO/Chairman notified
  - Group Legal/POCSO Officer notified
  - NCPCR notification required? (auto-flags Critical)
- Submit → Case created in Reported status, all escalation notifications triggered

### 6.2 View Full Case
**Trigger:** Row click or eye icon (both POCSO Coordinator and HR Director)
**Displays:** Full case details (all fields from logging), complete audit trail of every action taken with timestamps, uploaded evidence files, escalation log (who was notified, when, response), NCPCR filing reference if applicable, FIR details if applicable, ICC investigation notes, outcome summary.

### 6.3 Update Case Stage
**Trigger:** Update Stage button (POCSO Coordinator only)
**Fields:** New Stage (dropdown), Stage Notes (textarea, required), Any new documents to upload, NCPCR Reference Number (if moving to NCPCR Reported stage), FIR Number and Police Station (if applicable).

### 6.4 Delete Confirmation
Not available — POCSO incidents are permanent records and cannot be deleted. Closure is the only terminal state, and closed cases remain in the register indefinitely.

---

## 7. Charts

**Incidents by Severity (Donut Chart)**
- Segments: Critical (red), Serious (orange), Moderate (amber)
- Date range selector for reporting period
- Displayed at bottom of page — below the table, not prominently positioned (sensitive data should not be dashboard-like)

**Incident Trend by Month (Bar Chart)**
- X-axis: Month (last 12 months)
- Y-axis: Count of incidents reported
- Low counts expected — any spike is a serious signal

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Incident logged | "Case [ID] created. Escalation notifications sent. Acknowledge case immediately." | Warning | Non-dismissible until acknowledged |
| Case acknowledged | "Case [ID] acknowledged. Investigation stage can now be opened." | Success | 5s |
| Stage updated | "Case [ID] moved to [Stage]." | Info | 4s |
| NCPCR notification logged | "NCPCR notification filed for Case [ID]. Reference: [Ref Number]." | Success | 5s |
| FIR details logged | "FIR details recorded for Case [ID]." | Success | 5s |
| Export requested | "Register export initiated. You will be prompted for 2FA confirmation." | Warning | 6s |

---

## 9. Empty States

- **No cases on record:** "No POCSO incidents have been reported. This register will remain here to document any future cases."
- **No results match filters:** "No cases match the selected filters."

---

## 10. Loader States

- Table skeleton: 5 rows with shimmer.
- KPI cards: shimmer on load.
- Case detail drawer: spinner while full case record and audit trail loads.
- Charts: placeholder with "Loading…" text.

---

## 11. Role-Based UI Visibility

| Element | POCSO Coordinator (G3) | HR Director (G3) | All Others |
|---|---|---|---|
| Page access | Full | Full | Access Denied — 403 |
| Log New Incident button | Visible + enabled | Hidden | N/A |
| Update Case Stage | Visible + enabled | Hidden | N/A |
| View Full Case | Visible | Visible | N/A |
| Export Register | Visible (with 2FA) | Visible (with 2FA) | N/A |
| NCPCR/FIR log fields | Visible | Visible | N/A |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/pocso/incidents/` | JWT G3 POCSO/HR Director | List incident cases (restricted) |
| POST | `/api/v1/hr/pocso/incidents/` | JWT G3 POCSO Coordinator | Log new incident |
| GET | `/api/v1/hr/pocso/incidents/{id}/` | JWT G3 POCSO/HR Director | View full case details |
| PATCH | `/api/v1/hr/pocso/incidents/{id}/stage/` | JWT G3 POCSO Coordinator | Update case stage |
| POST | `/api/v1/hr/pocso/incidents/{id}/acknowledge/` | JWT G3 POCSO Coordinator | Acknowledge reported case |
| GET | `/api/v1/hr/pocso/incidents/kpis/` | JWT G3 POCSO/HR Director | KPI summary data |
| GET | `/api/v1/hr/pocso/incidents/charts/severity/` | JWT G3 POCSO/HR Director | Severity donut chart |
| GET | `/api/v1/hr/pocso/incidents/charts/trend/` | JWT G3 POCSO/HR Director | Monthly trend chart |
| GET | `/api/v1/hr/pocso/incidents/export/` | JWT G3 POCSO/HR Director + 2FA | Export register (password-protected) |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search by case ID | keyup changed delay:400ms | GET `/api/v1/hr/pocso/incidents/?case_id={val}` | `#incidents-table-body` | innerHTML |
| Filter change | change | GET `/api/v1/hr/pocso/incidents/?{params}` | `#incidents-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/pocso/incidents/?page={n}` | `#incidents-table-body` | innerHTML |
| Open log incident drawer | click | GET `/api/v1/hr/pocso/incidents/new/` | `#drawer-container` | innerHTML |
| Open view drawer | click | GET `/api/v1/hr/pocso/incidents/{id}/` | `#drawer-container` | innerHTML |
| Submit log form | submit | POST `/api/v1/hr/pocso/incidents/` | `#incidents-table-body` | innerHTML |
| Submit stage update | submit | PATCH `/api/v1/hr/pocso/incidents/{id}/stage/` | `#incidents-table-body` | innerHTML |
| Refresh KPI bar | htmx:afterRequest | GET `/api/v1/hr/pocso/incidents/kpis/` | `#kpi-bar` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
