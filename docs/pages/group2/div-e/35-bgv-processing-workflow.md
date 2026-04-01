# 35 — BGV Processing Workflow

- **URL:** `/group/hr/bgv/processing/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group BGV Executive (Role 49, G3)

---

## 1. Purpose

The BGV Processing Workflow is the day-to-day operational task queue for BGV Executives. Where the BGV Registry (page 34) is the master register viewed by the BGV Manager, this page is the working surface for BGV Executives — it shows only cases assigned to the logged-in executive and presents them in a task-oriented, priority-sorted format optimised for efficient case processing. Each case represents one staff member's background verification that needs to be actively progressed.

The processing lifecycle for each case follows a defined path. The BGV Executive receives a case assignment, contacts the staff member to collect the required documents (government ID, degree certificates, previous employer contact details, address proof), logs document receipt, submits the case to the appropriate verification agency, monitors the agency for a response, updates the case with the outcome once received, uploads the agency's formal report as a PDF attachment, and marks the case as Complete. For Police Verification specifically, the executive either visits the local police station, assists the staff member with the online portal submission, or arranges for the official letter to be sent — the process varies by state. For Educational Qualification Verification, the executive contacts the university registrar's office or uses an integrated verification API if available for that institution. For Previous Employment Verification, the executive makes direct calls to the previous employer's HR department or sends an official verification letter.

Cases where the agency has not responded within 7 days are automatically flagged as Overdue and escalated to the BGV Manager's attention. This is critical because delays in BGV completion can hold up a new joiner's full onboarding, affect their access rights, or — in the most serious cases — allow a person with an adverse record to remain in student contact while verification is still pending. Cases that arrive back with an adverse finding (any component flagged) must be escalated immediately to the BGV Manager — the executive does not resolve flagged cases; they document and escalate.

The executive can handle multiple parallel cases simultaneously. The page shows a prioritised queue: Emergency (new joiners who have already started vs. those whose day-30 deadline is approaching), High (overdue agency responses), and Standard. Each case card or row shows exactly where in the workflow the case stands and what the next action is, reducing cognitive load and minimising the chance of a case stalling due to forgotten follow-up.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group BGV Executive | G3 | Full access to assigned cases | Cannot see other executives' cases |
| Group BGV Manager | G3 | Full view of all executives' queues | Oversight and reassignment |
| Group HR Director | G3 | Read Only (escalated/flagged cases) | Reviews adverse outcomes |
| Group HR Manager | G3 | Read Only | General oversight |
| Group Performance Review Officer | G1 | No Access | Not applicable |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > Background Verification > BGV Processing Workflow`

### 3.2 Page Header
- **Title:** BGV Processing Workflow
- **Subtitle:** My open BGV cases — [Executive Name shown dynamically]
- **Actions (top-right):**
  - `Export My Case Report` (secondary button)
  - View Selector: `My Cases` / `All Cases` (BGV Manager only sees both options)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Agency response overdue > 7 days | "OVERDUE: [N] case(s) have not received an agency response in more than 7 days. Escalation to BGV Manager triggered." | Amber — dismissible |
| Documents pending from staff > 3 days | "REMINDER: [N] staff member(s) have not submitted their verification documents after 3 days of request." | Amber — dismissible |
| Flagged outcome received | "ACTION REQUIRED: A flagged BGV outcome has been received for [Staff Name]. Escalate to BGV Manager immediately." | Red — non-dismissible |
| No open cases | "You have no open BGV cases. Check with your BGV Manager for new assignments." | Green — auto-dismiss 10s |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| My Open Cases | Count of all active cases assigned to this executive | Amber if > 15, Green if ≤ 15 | No drill-down |
| Cases Initiated Today | Count of cases where document collection started today | Blue | Filters to today's initiated |
| Agency Response Overdue (>7 days) | Count where submitted to agency > 7 days ago with no response | Red if > 0, Green if 0 | Filters to overdue |
| Documents Pending from Staff | Count where awaiting document submission from staff | Amber if > 0 | Filters to this stage |
| Completed This Week | Count completed in current calendar week | Green | Filters to completed this week |
| Success Rate (Clear vs Flagged %) | (Clear outcomes / Total completed) × 100 | Green ≥ 95%, Amber 90–94%, Red < 90% | No drill-down |

---

## 5. Main Table — My BGV Cases

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Case ID | Text (auto-generated, e.g., BGV-2026-042) | No | No |
| Staff Name | Text + avatar | Yes | No |
| Branch | Badge | Yes | Yes — dropdown |
| Verification Type | Badge (Police / Education / Employment / Address / Criminal) | No | Yes — multi-select |
| Agency | Text | No | Yes — dropdown |
| Submitted Date | Date | Yes | Yes — date range |
| Days Outstanding | Integer with colour (green ≤ 3, amber 4–7, red > 7) | Yes | Yes — range |
| Last Status Update | Date + brief text | Yes | No |
| My Notes | Truncated text (expand in drawer) | No | No |
| Actions | Icon buttons (View / Update / Upload / Escalate) | No | No |

### 5.1 Filters
- **Verification Type:** multi-select
- **Stage:** Document Collection / Submitted to Agency / Agency Response Received / Completed / Escalated
- **Agency:** dropdown
- **Days Outstanding:** range (0–3 / 4–7 / 7+)
- **Priority:** Emergency / High / Standard

### 5.2 Search
Free-text search on Staff Name and Case ID. Debounced `hx-get` on keyup (400 ms).

### 5.3 Pagination
Server-side, 20 rows per page. Shows `Showing X–Y of Z cases`.

---

## 6. Drawers

### 6.1 Create
Not applicable — BGV Executive does not create cases. Cases are assigned by the BGV Manager through the BGV Registry (page 34).

### 6.2 View Case Details
**Trigger:** Row click or eye icon
**Displays:** Staff profile (name, branch, role, join date), verification type, agency name and contact details, full document checklist with received/pending status per document, agency submission confirmation (date, reference number), all status update history with timestamps, uploaded documents list (agency reports, staff documents), escalation history if any, next action prompt.

### 6.3 Update Status
**Trigger:** Update icon or Update Status button in view drawer
**Fields:**
- Stage (dropdown: Document Collection / Documents Received / Submitted to Agency / Response Received / Complete)
- Agency Reference Number (text, required when submitting to agency)
- Outcome (dropdown: Clear / Flagged / Pending — enabled only when stage = Response Received)
- Status Notes (textarea)
- Upload Documents (file upload — accepts PDF, JPG, PNG — max 10 MB per file)
- If Outcome = Flagged: mandatory "Escalate to BGV Manager" confirmation checkbox

### 6.4 Escalate to BGV Manager
**Trigger:** Escalate icon or escalate action in update drawer
**Fields:**
- Escalation Reason (dropdown: Agency Overdue / Adverse Finding / Document Dispute / Other)
- Escalation Notes (textarea, required)
- Confirm Escalate button → sends in-app notification to BGV Manager and logs escalation in case audit trail

---

## 7. Charts

**My Case Stage Distribution (Donut Chart)**
- Segments: Document Collection (grey), Submitted to Agency (blue), Response Received (teal), Completed (green), Overdue (red), Escalated (amber)
- Quick visual summary of workload stage distribution

**Daily Case Activity (Bar Chart — last 14 days)**
- X-axis: Date
- Y-axis: Count
- Bars: Cases Progressed (blue), Cases Completed (green), Escalations (red)

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Status updated | "BGV case [ID] status updated to [Stage]." | Success | 4s |
| Document uploaded | "Document uploaded for case [ID]." | Success | 3s |
| Outcome recorded (Clear) | "BGV outcome recorded as Clear for [Staff Name]." | Success | 4s |
| Outcome recorded (Flagged) | "Flagged outcome recorded for [Staff Name]. Escalation sent to BGV Manager." | Warning | 6s |
| Escalation submitted | "Case [ID] escalated to BGV Manager. Reference logged." | Info | 5s |
| File upload error | "Upload failed. File must be PDF, JPG, or PNG and under 10 MB." | Error | 6s |

---

## 9. Empty States

- **No open cases:** "You have no open BGV cases. Contact your BGV Manager for new case assignments."
- **No results match filters:** "No cases match the selected filters. Try adjusting stage or type filters."
- **All cases completed:** "All your assigned cases are complete. Well done."

---

## 10. Loader States

- Table skeleton: 6 rows with shimmer on initial load.
- KPI cards: shimmer rectangles.
- Case detail drawer: spinner while full case data and document list loads.
- Chart area: placeholder with "Loading chart…" label.

---

## 11. Role-Based UI Visibility

| Element | BGV Executive (G3) | BGV Manager (G3) | HR Director (G3) |
|---|---|---|---|
| View own cases only | Enforced — My Cases default | Can toggle to All Cases | Flagged cases only |
| Update Status button | Visible + enabled | Visible (all cases) | Hidden |
| Upload document | Visible + enabled | Visible | Hidden |
| Escalate button | Visible + enabled | Hidden (manager receives) | Hidden |
| Export case report | Visible (own cases) | Visible (all cases) | Hidden |
| View case details | Visible | Visible | Visible (flagged) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/bgv/processing/` | JWT G3 | List BGV cases (filtered to executive or all for manager) |
| GET | `/api/v1/hr/bgv/processing/{id}/` | JWT G3 | View full case details |
| PATCH | `/api/v1/hr/bgv/processing/{id}/status/` | JWT G3 BGV Executive | Update case stage and status |
| POST | `/api/v1/hr/bgv/processing/{id}/upload/` | JWT G3 BGV Executive | Upload agency report or staff document |
| POST | `/api/v1/hr/bgv/processing/{id}/escalate/` | JWT G3 BGV Executive | Escalate case to BGV Manager |
| GET | `/api/v1/hr/bgv/processing/kpis/` | JWT G3 | KPI summary (scoped to executive) |
| GET | `/api/v1/hr/bgv/processing/charts/stage/` | JWT G3 | Stage distribution donut data |
| GET | `/api/v1/hr/bgv/processing/charts/activity/` | JWT G3 | Daily activity chart data |
| GET | `/api/v1/hr/bgv/processing/export/` | JWT G3 | Export case report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search case by staff name | keyup changed delay:400ms | GET `/api/v1/hr/bgv/processing/?q={val}` | `#cases-table-body` | innerHTML |
| Filter change | change | GET `/api/v1/hr/bgv/processing/?{params}` | `#cases-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/bgv/processing/?page={n}` | `#cases-table-body` | innerHTML |
| Open view drawer | click | GET `/api/v1/hr/bgv/processing/{id}/` | `#drawer-container` | innerHTML |
| Submit status update | submit | PATCH `/api/v1/hr/bgv/processing/{id}/status/` | `#cases-table-body` | innerHTML |
| File upload | change | POST `/api/v1/hr/bgv/processing/{id}/upload/` | `#upload-status-{id}` | innerHTML |
| Submit escalation | submit | POST `/api/v1/hr/bgv/processing/{id}/escalate/` | `#cases-table-body` | innerHTML |
| Refresh KPI bar | htmx:afterRequest | GET `/api/v1/hr/bgv/processing/kpis/` | `#kpi-bar` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
