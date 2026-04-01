# 41 — Show-Cause Notice Manager

- **URL:** `/group/hr/disciplinary/show-cause/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Disciplinary Committee Head (Role 51, G3)

---

## 1. Purpose

The Show-Cause Notice Manager is the operational page for drafting, issuing, tracking delivery, and recording responses to Show-Cause Notices (SCN) — the formal first step in the staff disciplinary process. A Show-Cause Notice is a legal instrument issued to a staff member that formally notifies them of the alleged conduct or misconduct and requires them to explain, in writing, why disciplinary action should not be taken against them. The SCN is a cornerstone of the principles of natural justice: every staff member must be given an opportunity to be heard before any adverse disciplinary action is taken. Skipping this step — or issuing a defective SCN — can render the entire disciplinary process legally challengeable.

For a Show-Cause Notice to be legally sound it must meet several requirements. It must be issued in writing, on official group letterhead, clearly stating the allegation in specific and factual terms (not vague or generic language). It must specify a reasonable response period — typically 7 working days, though this can be extended to 14 days for complex cases. It must be served to the staff member personally with their signature of receipt, or if personal service is refused or not possible, sent via registered post to their residential address, with the tracking number and proof of posting recorded in this system. The staff member's response must be received in writing, and the response — whether satisfactory or not — must be documented in the case file before the next disciplinary step is taken.

This page manages the full SCN lifecycle, from drafting to delivery to response. The Disciplinary Committee Head drafts the SCN text using a structured template (which can be customised per case), previews it as a formatted PDF on group letterhead, and issues it. Once issued, the system tracks the response deadline — a countdown timer is displayed for each active SCN. When the response is received, it is recorded and the Disciplinary Committee Head reviews it: if satisfactory, the case can be closed with a warning; if unsatisfactory or no response is received within the deadline, the page prompts the next step — scheduling a formal disciplinary hearing.

The page is tightly integrated with the Disciplinary Case Register (page 40): every SCN on this page is linked to a case ID. Creating an SCN on this page automatically updates the parent case stage to "SCN Issued". Recording a response updates the stage to "Response Received". Proceeding to a hearing updates the stage to "Hearing Scheduled". This bidirectional linkage ensures the Case Register always reflects the current state without manual double-entry.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Disciplinary Committee Head | G3 | Full CRUD + Draft + Issue + Record Response | Primary owner |
| Group HR Director | G3 | Full Read + Review | Oversight; receives copy of all SCNs |
| Group HR Manager | G3 | Read + Add response notes | Operational support |
| Group POCSO Coordinator | G3 | Read (POCSO-linked SCNs only) | Coordination for POCSO cases |
| Branch Principal | Branch G3 | Read (own branch SCNs only) | Receives notification of SCN issuance |
| Group Performance Review Officer | G1 | No Access | Not applicable |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > Disciplinary > Show-Cause Notice Manager`

### 3.2 Page Header
- **Title:** Show-Cause Notice Manager
- **Subtitle:** Draft, issue, and track Show-Cause Notices for all disciplinary cases
- **Actions (top-right):**
  - `+ Draft New SCN` (primary button)
  - `Export SCN Register` (secondary button)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| SCN response deadline passed with no response filed | "DEFAULT: SCN [ID] response deadline has passed with no response received for [Staff Name]. Proceed to hearing or apply default." | Amber — dismissible |
| SCN response deadline within 24 hours | "REMINDER: Response deadline for SCN [ID] ([Staff Name]) is in less than 24 hours." | Amber — dismissible |
| SCN delivery not confirmed > 3 days after issue | "WARNING: SCN [ID] delivery has not been confirmed for [Staff Name] after 3 days. Check delivery method." | Amber — dismissible |
| All SCNs have received responses | "All active Show-Cause Notices have received staff responses. Review and proceed." | Green — auto-dismiss 10s |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| SCNs Issued This Month | Count issued in current month | Blue always | Filters to current month |
| Awaiting Response | Count with status = Issued, response deadline not passed | Amber if > 0 | Filters to awaiting |
| Response Received (Satisfactory) | Count marked Satisfactory | Green | Filters to satisfactory responses |
| Response Received (Unsatisfactory/Proceeding to Hearing) | Count marked Unsatisfactory | Amber if > 0 | Filters to unsatisfactory |
| No Response (Defaulted) | Count where deadline passed with no response | Red if > 0 | Filters to defaulted |
| SCNs Closed | Count where SCN led to case closure with warning | Green | Filters to closed |

---

## 5. Main Table — Show-Cause Notices

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| SCN ID | Text (e.g., SCN-2026-001) | No | No |
| Case ID | Text (linked to Disciplinary Case Register) | No | No |
| Staff Name | Text + avatar | Yes | No |
| Branch | Badge | Yes | Yes — dropdown |
| Issue Date | Date | Yes | Yes — date range |
| Response Due Date | Date with countdown highlight | Yes | Yes — date range |
| Response Status | Badge (Awaiting / Received — Satisfactory / Received — Unsatisfactory / Defaulted / N/A) | No | Yes — multi-select |
| Outcome | Badge (Pending / Warning — Case Closed / Proceeding to Hearing / Closed) | No | Yes — dropdown |
| Actions | Icon buttons (View / Mark Delivered / Record Response / Proceed) | No | No |

### 5.1 Filters
- **Response Status:** multi-select
- **Outcome:** dropdown
- **Branch:** multi-select
- **Issue Date Range:** date picker
- **Deadline Status:** Within 24h / Overdue / Not yet due

### 5.2 Search
Free-text search on SCN ID, Case ID, and Staff Name. Debounced `hx-get` on keyup (400 ms).

### 5.3 Pagination
Server-side, 20 rows per page. Shows `Showing X–Y of Z notices`.

---

## 6. Drawers

### 6.1 Draft SCN
**Trigger:** `+ Draft New SCN` button
**Fields:**
- Linked Case ID (searchable dropdown — must be an existing open case in Case Opened stage)
- Staff Member (auto-populated from case, read-only)
- Branch (auto-populated)
- SCN Date (defaults to today, editable)
- Allegation Type (dropdown: Misconduct / Attendance / Financial Irregularity / POCSO-related / Other)
- SCN Body (rich text editor with template pre-loaded — includes: To, Subject, allegation statement, response instructions, deadline, signatory block)
- Response Deadline (date picker, default = 7 working days from SCN date, editable up to 14 days with reason)
- Response Method Required (radio: Written / Email / In-person to HR)
- Save as Draft button (does not issue — saves for review)
- Preview PDF button (renders SCN as formatted PDF on group letterhead in overlay)
- Issue SCN button (final — issues the notice and changes case stage to SCN Issued)

### 6.2 View Full SCN
**Trigger:** Row click or eye icon
**Displays:** Full SCN text with formatting, issue date, delivery status, response due date, response deadline countdown, any response received (full text), Committee Head's assessment of response (Satisfactory / Unsatisfactory), outcome decision, audit trail of all actions.

### 6.3 Mark Delivered
**Trigger:** Mark Delivered button (available after SCN issued)
**Fields:**
- Delivery Method (radio: Personal Service / Registered Post / Email with Read Receipt)
- Delivery Date and Time
- Received By (staff member's name — auto-filled from case; editable if received by representative)
- Proof of Delivery (file upload — signed acknowledgement scan, postal tracking screenshot, email read receipt screenshot)
- Confirm → records delivery confirmation in case file

### 6.4 Record Response
**Trigger:** Record Response button (available after SCN delivered)
**Fields:**
- Response Receipt Date
- Response Method (how received: Written letter / Email / In-person verbal — not recommended)
- Response Summary (textarea — Committee Head's summary of staff's explanation)
- Upload Staff Response Document (file upload — the staff member's written response letter, PDF/DOC/JPG)
- Assessment (radio: Satisfactory — close case with warning / Unsatisfactory or No Response — proceed to hearing)
- If Satisfactory: Warning Letter to be issued? (toggle), Warning Notes
- If Unsatisfactory: Hearing Date (date picker), Hearing Room / Mode
- Submit → updates case stage, triggers next step notifications

---

## 7. Charts

**SCN Response Outcome Distribution (Donut Chart)**
- Segments: Satisfactory — Closed (green), Unsatisfactory — Hearing Proceeding (amber), Defaulted — No Response (red), Awaiting Response (grey)
- Date range selector for reporting period

**Monthly SCN Volume (Bar Chart — last 12 months)**
- X-axis: Month
- Y-axis: Count of SCNs issued
- Useful for spotting spikes in disciplinary activity (e.g., post-appraisal period, post-audit)

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| SCN saved as draft | "SCN draft saved for [Staff Name]. Not yet issued." | Info | 4s |
| SCN issued | "Show-Cause Notice [ID] issued for [Staff Name]. Case stage updated. HR Director notified." | Success | 5s |
| Delivery confirmed | "Delivery confirmed for SCN [ID]. Delivery date: [Date]." | Success | 4s |
| Response recorded (Satisfactory) | "Response for SCN [ID] recorded as Satisfactory. Case can be closed with warning." | Success | 5s |
| Response recorded (Unsatisfactory) | "Response for SCN [ID] recorded as Unsatisfactory. Proceed to schedule hearing." | Warning | 5s |
| Response defaulted | "No response received for SCN [ID]. Default status applied. Proceed to hearing." | Warning | 5s |
| Export triggered | "SCN register export started." | Info | 4s |

---

## 9. Empty States

- **No SCNs issued:** "No Show-Cause Notices have been issued. Click '+ Draft New SCN' to begin."
- **No results match filters:** "No Show-Cause Notices match the selected filters."
- **All responses received:** "All issued SCNs have received staff responses. No notices are awaiting response."

---

## 10. Loader States

- Table skeleton: 6 rows with shimmer on initial load.
- KPI cards: shimmer rectangles.
- SCN view drawer: spinner while full SCN text and response data loads.
- PDF preview overlay: loading spinner while letterhead and SCN text renders.
- Chart area: placeholder with "Loading chart…" text.

---

## 11. Role-Based UI Visibility

| Element | Disciplinary Committee Head (G3) | HR Director (G3) | HR Manager (G3) |
|---|---|---|---|
| Draft / Issue SCN button | Visible + enabled | Hidden | Hidden |
| Mark Delivered button | Visible + enabled | Hidden | Hidden |
| Record Response button | Visible + enabled | Hidden | Hidden |
| Preview PDF | Visible | Visible | Visible |
| View full SCN | Visible (all) | Visible (all) | Visible |
| Export SCN Register | Visible | Visible | Visible |
| Proceed to Hearing button | Visible + enabled | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/disciplinary/show-cause/` | JWT G3 | List all SCNs (paginated) |
| POST | `/api/v1/hr/disciplinary/show-cause/` | JWT G3 Disc. Head | Draft and issue new SCN |
| GET | `/api/v1/hr/disciplinary/show-cause/{id}/` | JWT G3 | View full SCN details |
| PATCH | `/api/v1/hr/disciplinary/show-cause/{id}/` | JWT G3 Disc. Head | Update SCN draft (pre-issue only) |
| POST | `/api/v1/hr/disciplinary/show-cause/{id}/deliver/` | JWT G3 Disc. Head | Record delivery confirmation |
| POST | `/api/v1/hr/disciplinary/show-cause/{id}/response/` | JWT G3 Disc. Head | Record staff response and assessment |
| GET | `/api/v1/hr/disciplinary/show-cause/{id}/preview/` | JWT G3 | Render SCN as PDF (preview) |
| GET | `/api/v1/hr/disciplinary/show-cause/kpis/` | JWT G3 | KPI summary data |
| GET | `/api/v1/hr/disciplinary/show-cause/charts/outcomes/` | JWT G3 | Response outcome donut chart data |
| GET | `/api/v1/hr/disciplinary/show-cause/charts/volume/` | JWT G3 | Monthly volume bar chart data |
| GET | `/api/v1/hr/disciplinary/show-cause/export/` | JWT G3 | Export SCN register |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search SCN ID or staff | keyup changed delay:400ms | GET `/api/v1/hr/disciplinary/show-cause/?q={val}` | `#scn-table-body` | innerHTML |
| Filter change | change | GET `/api/v1/hr/disciplinary/show-cause/?{params}` | `#scn-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/disciplinary/show-cause/?page={n}` | `#scn-table-body` | innerHTML |
| Open draft SCN drawer | click | GET `/api/v1/hr/disciplinary/show-cause/new/` | `#drawer-container` | innerHTML |
| Open view drawer | click | GET `/api/v1/hr/disciplinary/show-cause/{id}/` | `#drawer-container` | innerHTML |
| Preview SCN as PDF | click | GET `/api/v1/hr/disciplinary/show-cause/{id}/preview/` | `#pdf-preview-overlay` | innerHTML |
| Submit issue SCN form | submit | POST `/api/v1/hr/disciplinary/show-cause/` | `#scn-table-body` | innerHTML |
| Submit delivery confirmation | submit | POST `/api/v1/hr/disciplinary/show-cause/{id}/deliver/` | `#scn-table-body` | innerHTML |
| Submit response record | submit | POST `/api/v1/hr/disciplinary/show-cause/{id}/response/` | `#scn-table-body` | innerHTML |
| Refresh KPI bar | htmx:afterRequest | GET `/api/v1/hr/disciplinary/show-cause/kpis/` | `#kpi-bar` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
