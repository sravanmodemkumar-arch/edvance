# 20 — Emergency Incident Register

> **URL:** `/group/health/incidents/`
> **File:** `20-emergency-incident-register.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Emergency Response Officer (primary) · Group Medical Coordinator (co-view for medical and transport incidents)

---

## 1. Purpose

Authoritative record of all emergency incidents across every branch of the group. Covered incident types include: Medical Emergency (cardiac arrest, anaphylaxis, serious injury, mass illness), Fire, Natural Disaster (earthquake, flood, cyclone, lightning strike), Road Accident (on-campus vehicle accident or bus accident), Missing Student, Campus Security Breach, and Other / Mass Casualty Events.

Each incident is tracked across its full lifecycle: initial report → active response → containment → resolution → post-incident review. Severity levels range from 1 (Minor) to 5 (Mass Casualty), with Severity 4 and 5 incidents triggering automatic escalation notifications to Group CEO, COO, and Chairman.

Live / Active incidents are surfaced with a permanent red banner and HTMX auto-refresh every 2 minutes so the Emergency Response Officer can monitor real-time progress without page reloads. Post-incident reviews must be completed within 7 days of incident closure to satisfy regulatory and governance requirements.

Scale: 10–100 incidents per academic year across the group.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Emergency Response Officer | G3 | Full CRUD — create, update, log responses, close, escalate | Primary owner |
| Group Medical Coordinator | G3 | Create + view + update: Medical Emergency + Transport type incidents | Co-owner for medical/transport type only |
| CEO / COO | Group | View all incidents + receive escalations + close incidents | Oversight; cannot create |
| Group Chairman | Group | View Severity 4 and 5 incidents only | Governance oversight |
| Branch Principal | Branch | Create incident for own branch (via branch portal) | Cannot view group-wide list; no close or escalate |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('emergency_response_officer', 'medical_coordinator', 'ceo', 'coo', 'chairman', 'branch_principal')`. Incident type scope for Medical Coordinator: `incident.type in ['medical_emergency', 'transport']`. Branch Principal scoped to `incident.branch == request.user.branch`. Chairman scoped to `incident.severity >= 4`. Severity 4–5 auto-escalation to CEO/COO/Chairman triggered server-side on create.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Emergency Incident Register
```

### 3.2 Page Header
- **Title:** `Emergency Incident Register`
- **Subtitle:** `[N] Total This AY · [N] Active · [N] Critical (last 30 days) · [N] Reviews Pending`
- **Right controls:** `+ Report Incident` (Emergency Response Officer + Medical Coordinator) · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity | Dismissable |
|---|---|---|---|
| One or more ACTIVE incidents (status = Active) | "🔴 ACTIVE INCIDENT: [N] incident(s) are currently active. Live monitoring in progress." | Red — full-width permanent banner | No — remains until all active incidents closed |
| Incident not reviewed within 7 days of closure | "[N] closed incident(s) have not had a post-incident review completed within 7 days. Immediate review required." | Red | No |
| Critical incident (Severity 4–5) with no post-incident report | "CRITICAL: [N] Severity 4–5 incident(s) have no post-incident review documented." | Red | No |
| Multiple incidents at the same branch this month (≥ 3) | "SYSTEMIC ISSUE FLAG: [Branch] has had [N] incidents this month. A systemic safety review is recommended." | Amber | Yes |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Incidents This AY | All incidents regardless of status | Blue always |
| Open / Active Incidents | Status = Active or Contained | Red > 0 · Green = 0 |
| Critical Incidents (last 30 days) | Severity 4 or 5 in last 30 days | Red > 0 · Green = 0 |
| Incidents by Type | Mini horizontal bar chart: Medical / Fire / Natural Disaster / Transport / Missing / Security / Other | Blue always |
| Average Response Time (minutes) | Mean minutes from `incident_reported_time` to first response log entry across all closed incidents | Green < 10 min · Yellow 10–30 min · Red > 30 min |
| Post-Incident Reviews Pending | Closed incidents where post-incident review not yet completed | Red > 0 · Green = 0 |

---

## 5. Main Table — Emergency Incident Register

**Search:** Incident ID, branch name. 300ms debounce, minimum 2 characters.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Type | Checkbox | Medical Emergency / Fire / Natural Disaster / Transport / Missing Student / Security Breach / Other |
| Severity | Checkbox | 1 — Minor / 2 — Moderate / 3 — Serious / 4 — Critical / 5 — Mass Casualty |
| Status | Checkbox | Active / Contained / Resolved / Under Review |
| Date Range | Date range picker | Incident date range |
| Has Students Affected | Radio | All / Yes (students affected) / No |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Incident ID | ✅ | Auto-generated format `INC-YYYY-NNNN`; click → `incident-detail` drawer |
| Date | ✅ | Date of incident |
| Time | ❌ | Time of incident |
| Branch | ✅ | |
| Type | ✅ | Colour-coded badge |
| Severity | ✅ | 1–5 badge: 1 grey / 2 yellow / 3 orange / 4 red / 5 dark red with pulse animation |
| Students Affected | ✅ | Count; red if > 0 |
| Staff Affected | ✅ | Count |
| Response Time (mins) | ✅ | Minutes from report to first response log; blank if Active; red if > 30 min |
| Status | ✅ | Active (red pulsing) / Contained (orange) / Resolved (green) / Under Review (blue) badge |
| Post-Incident Review | ✅ | Pending / Complete / Not Required — badge; red if Pending + > 7 days since closure |
| Actions | ❌ | View · Update · Close · Escalate |

**Active incident rows:** Highlighted with red left border and auto-refresh every 2 minutes via HTMX polling on `#incident-table-body`.

**Default sort:** Status (Active first, then Contained, then Under Review, then Resolved), then Date descending, then Severity descending.
**Pagination:** Server-side · 25 records per page.

---

## 6. Drawers / Modals

### 6.1 Drawer — `incident-detail` (720px, right side)

Triggered by Incident ID link or **View** action.

**Tabs:**

#### Tab 1 — Initial Report

| Field | Notes |
|---|---|
| Incident ID | Auto-generated |
| Reported By | Name + role |
| Date / Time Discovered | When the incident was first observed on campus |
| Date / Time Reported to Group | When the Emergency Response Officer / Medical Coordinator was notified |
| Branch | |
| Location Within Campus | Specific area: classroom, corridor, sports ground, hostel block, bus bay, etc. |
| Type | |
| Initial Severity Assessment | 1–5 with description |
| Immediate Description | Full narrative of what was observed |
| First Actions Taken | What was done immediately: called ambulance, activated fire alarm, isolated area, etc. |
| Who Was Informed First | Name, role, time |

#### Tab 2 — Response Log

Chronological log of all actions taken after initial report. Each entry:

| Field | Notes |
|---|---|
| Timestamp | Date and time |
| Action Taken | Description of response action |
| By Whom | Name + role (dropdown of key incident roles) |
| Outcome | What resulted from this action |

Add new log entry via **+ Add Response Entry** button → opens `response-log-add` drawer without closing the incident detail drawer. New entries appended in real-time via HTMX.

#### Tab 3 — Impact

| Field | Notes |
|---|---|
| Students Affected — List | Table: Name · Student ID · Class · Nature of injury/impact (free text) |
| Staff Affected — List | Name · Role · Nature of impact |
| Property Damage | Brief description + estimated value (₹) |
| External Agencies Involved | Table: Agency (Ambulance / Fire Brigade / Police / Hospital) · Contact Name · Contact Number · Time Notified · Arrival Time |
| Hospitalised Count | Number |
| Hospitals Involved | Hospital names + patient allocation |

#### Tab 4 — Post-Incident Review

| Field | Notes |
|---|---|
| Root Cause Analysis | Free text (5-WHY format recommended; prompts displayed) |
| Contributing Factors | Multi-row: factor description (e.g., delayed staff response, inadequate training, blocked exit) |
| Immediate Corrective Actions Taken | What was done to prevent recurrence immediately |
| Systemic Changes Recommended | Policy, infrastructure, training changes recommended |
| Timeline for Implementation | Target date for each systemic change |
| Reviewed By | Name + role |
| Review Date | Date review was completed |
| Approved By | Emergency Response Officer / COO |
| Approval Date | |

Post-incident review is locked for editing after it is marked approved. Approved reviews are surfaced in the Compliance Report (Page 24).

#### Tab 5 — Documents

| Document Type | Notes |
|---|---|
| Incident Photos | Multiple images; JPG/PNG, max 10 MB each |
| FIR Copy | If police case (accident, missing student, security breach) |
| Medical Reports | Treating doctor notes, hospital discharge summaries |
| Ambulance / Fire Brigade Report | Official report from external agency |
| Insurance Notification | Copy of claim notification if insurance claim filed |
| Post-Incident Review Report | Final approved review document PDF |

Each document: upload date, uploaded by, download link.

---

### 6.2 Drawer — `incident-create` (680px, right side)

Triggered by **+ Report Incident**. Branch Principal version accessible via branch portal with same fields but pre-filled branch.

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select (Emergency Response Officer can select any; Medical Coordinator any; Branch Principal own branch only) | Required |
| Incident Type | Single-select: Medical Emergency / Fire / Natural Disaster / Transport / Missing Student / Security Breach / Other | Required |
| Severity | Radio: 1 — Minor / 2 — Moderate / 3 — Serious / 4 — Critical / 5 — Mass Casualty | Required |
| Date | Date picker | Required; cannot be future date |
| Time | Time picker | Required |
| Location Within Campus | Text input | Required |
| Description | Textarea (max 2,000 chars) | Required |
| Immediate Action Taken | Textarea (max 1,000 chars) | Required |
| Who Was Notified Immediately | Text input (name + role) | Required |
| Students Affected (count) | Number input | Required; can be 0 |
| Staff Affected (count) | Number input | Required; can be 0 |
| SOP Followed | Single-select (links to SOP library; filtered by incident type) | Optional |

**Severity 4–5 auto-escalation notice:** When Severity 4 or 5 selected, a yellow notice appears: "Selecting Severity 4 or 5 will automatically notify the Group CEO, COO, and Chairman via portal notification and WhatsApp immediately upon submitting this report."

**Footer:** `Cancel` · `Report Incident`

---

### 6.3 Drawer — `response-log-add` (480px, right side)

Triggered by **+ Add Response Entry** in the Response Log tab. Opens as a secondary drawer panel without closing the incident detail drawer.

| Field | Type | Validation |
|---|---|---|
| Incident ID | Read-only | |
| Timestamp | Date-time picker (default: now) | Required |
| Action Taken | Textarea (max 500 chars) | Required |
| By Whom | Dropdown: roles relevant to incident response (Emergency Response Officer, Medical Officer, Fire Brigade, Police, Principal, First Responder, etc.) + free text override | Required |
| Outcome | Textarea (max 300 chars) | Required |

**Footer:** `Cancel` · `Add Entry`

On submit: new entry appended to Response Log tab timeline via HTMX without full drawer reload.

---

### 6.4 Modal — `close-incident` (500px, centred)

Triggered by **Close** action for incidents with status = Active or Contained.

| Field | Type | Validation |
|---|---|---|
| Incident ID | Read-only | |
| Resolution Date / Time | Date-time picker | Required |
| Final Status | Radio: Resolved / Under Review | Required |
| Resolution Summary | Textarea (max 1,000 chars) | Required |
| All Affected Students Accounted For | Radio: Yes / No | Required |
| Explanation if No | Textarea | Required if answer = No |
| Post-Incident Review Required | Radio: Yes / No | Required |
| Schedule Review Date | Date picker | Required if Post-Incident Review = Yes; must be within 7 days |

**Footer:** `Cancel` · `Close Incident`

On close with Review Required = Yes: incident status set to Under Review; review due date alert scheduled. On close with Review Required = No: status set to Resolved immediately.

---

### 6.5 Modal — `escalate-incident` (440px, centred)

Triggered by **Escalate** action.

| Field | Type | Validation |
|---|---|---|
| Incident ID | Read-only | |
| Escalate To | Multi-checkbox: Group CEO / Group COO / Group Chairman | Required; at least one |
| Reason for Escalation | Textarea (max 500 chars) | Required |
| Urgency | Radio: Immediate (within 5 min) / High (within 30 min) / Normal | Required |
| Notify Via | Checkbox: Portal Notification (checked; cannot deselect) / WhatsApp / Email | Required |
| Escalation Message | Textarea (max 300 chars, pre-filled with incident summary) | Required |

**Footer:** `Cancel` · `Escalate Now`

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Incident reported | "Incident [INC-ID] reported at [Branch]. Emergency Response Officer and relevant team notified." | Warning (6s) |
| Severity 4–5 auto-escalation | "CRITICAL: Severity [N] incident reported. CEO, COO, and Chairman have been notified automatically." | Error (persistent until dismissed) |
| Response entry logged | "Response entry added to Incident [INC-ID]." | Success (3s) |
| Incident status updated | "Incident [INC-ID] status updated to [Status]." | Info (4s) |
| Incident closed | "Incident [INC-ID] closed. Post-incident review [scheduled for / not required]." | Success (5s) |
| Incident escalated | "Incident [INC-ID] escalated to [Recipients]. They have been notified via [channels]." | Warning (6s) |
| Escalation failed | "Escalation failed to send. Retry or contact IT support." | Error (5s) |
| Post-incident review saved | "Post-incident review saved for Incident [INC-ID]." | Success (4s) |
| Post-incident review approved | "Post-incident review for [INC-ID] approved." | Success (4s) |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No incidents this AY | "No incidents recorded this academic year." | "Incidents will appear here once reported. Use '+ Report Incident' if an event has occurred." | `+ Report Incident` |
| No open incidents | "No active or open incidents." | "All incidents are resolved. Well done." | — |
| No results for filters | "No incidents match your current filters." | "Try adjusting the type, severity, status, or date range filters." | `Clear Filters` |
| Response log — no entries yet | "No response log entries yet." | "Add the first response entry to begin tracking this incident's response timeline." | `+ Add Response Entry` |
| Impact tab — no affected students | "No students listed as affected." | "Update this section once the full impact is assessed." | — |
| Post-incident review — not started | "Post-incident review not yet started." | "Complete the review within 7 days of incident closure." | — |
| Documents tab — no documents | "No documents uploaded for this incident." | "Attach incident photos, FIR copy, or medical reports." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 6 KPI cards (one with mini chart placeholder) + incident table (5 grey rows × 12 columns) |
| HTMX auto-refresh (every 2 min) | Active incident rows only refresh silently; table position preserved; spinner indicator on bottom-right of table |
| Filter apply | Table body inline spinner overlay |
| Search debounce | Table body inline spinner while request in-flight |
| Incident detail drawer open | Drawer skeleton: tab bar (5 tabs) + content blocks |
| Response log tab load | Timeline skeleton (4 grey event rows) |
| Impact tab load | Two-section skeleton: affected persons table + external agencies table |
| Post-incident review tab load | Form skeleton (8 grey input rows) |
| Documents tab load | File list skeleton (3 grey rows) |
| Incident create submit | Submit button spinner; form fields disabled |
| Response log add submit | Mini spinner on Add Entry button; form stays open |
| Close modal submit | Modal footer spinner + "Closing incident…" |
| Escalate modal submit | Modal footer spinner + "Sending escalation notifications…" |

---

## 10. Role-Based UI Visibility

| UI Element | Emergency Response Officer | Medical Coordinator | CEO / COO | Chairman | Branch Principal |
|---|---|---|---|---|---|
| Full incident list (all branches) | ✅ | Medical + Transport types | ✅ | Severity 4–5 only | Own branch only (branch portal) |
| + Report Incident button | ✅ | ✅ (own types) | ❌ | ❌ | ✅ (own branch — branch portal) |
| Update action | ✅ | Own types | ❌ | ❌ | ❌ |
| Close action | ✅ | ❌ | ✅ | ❌ | ❌ |
| Escalate action | ✅ | ❌ | ❌ | ❌ | ❌ |
| Response log — add entry | ✅ | ✅ (own types) | ❌ | ❌ | ❌ |
| Impact tab — edit | ✅ | ✅ (own types) | ❌ | ❌ | ❌ |
| Post-incident review — edit | ✅ | ✅ (own types) | ❌ | ❌ | ❌ |
| Post-incident review — approve | ✅ | ❌ | ✅ (COO) | ❌ | ❌ |
| Documents tab — upload | ✅ | ✅ | ❌ | ❌ | ❌ |
| Documents tab — view | ✅ | ✅ | ✅ | ✅ (Sev 4–5) | Own branch |
| KPI bar — all 6 cards | ✅ | ✅ | ✅ | Severity 4–5 counts only | ❌ |
| Alert banners — Active Incident | ✅ | ✅ | ✅ | ✅ | ❌ |
| Alert banners — review pending | ✅ | ✅ | ✅ | ❌ | ❌ |
| Export | ✅ | ❌ | ✅ | ❌ | ❌ |
| Auto-refresh (2 min) on Active incidents | ✅ | ✅ | ✅ | ❌ | ❌ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/incidents/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/incidents/` | List all incidents (paginated, filtered, role-scoped) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/incidents/` | Report new incident | Emergency Response Officer / Medical Coordinator / Branch Principal |
| GET | `/api/v1/group/{group_id}/health/incidents/{incident_id}/` | Retrieve full incident detail | JWT + role check + type scope |
| PATCH | `/api/v1/group/{group_id}/health/incidents/{incident_id}/` | Update incident fields | Emergency Response Officer / Medical Coordinator (own types) |
| GET | `/api/v1/group/{group_id}/health/incidents/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/incidents/alerts/` | Active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/incidents/active/` | Active incidents only (for auto-refresh polling) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/incidents/{incident_id}/response-log/` | Add response log entry | Emergency Response Officer / Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/incidents/{incident_id}/response-log/` | List all response log entries | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/incidents/{incident_id}/close/` | Close incident | Emergency Response Officer / CEO / COO |
| POST | `/api/v1/group/{group_id}/health/incidents/{incident_id}/escalate/` | Escalate incident | Emergency Response Officer |
| GET | `/api/v1/group/{group_id}/health/incidents/{incident_id}/impact/` | Retrieve impact details | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/incidents/{incident_id}/impact/` | Update impact details | Emergency Response Officer / Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/incidents/{incident_id}/post-incident-review/` | Retrieve post-incident review | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/incidents/{incident_id}/post-incident-review/` | Update post-incident review | Emergency Response Officer / Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/incidents/{incident_id}/post-incident-review/approve/` | Approve post-incident review | Emergency Response Officer / COO |
| POST | `/api/v1/group/{group_id}/health/incidents/{incident_id}/documents/` | Upload document | Emergency Response Officer / Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/incidents/{incident_id}/documents/{doc_id}/` | Download document | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/incidents/export/` | Export incident register | Emergency Response Officer / CEO / COO |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `search` | str | Incident ID or branch name |
| `branch` | int[] | Branch filter |
| `type` | str[] | `medical`, `fire`, `natural_disaster`, `transport`, `missing_student`, `security`, `other` |
| `severity` | int[] | 1, 2, 3, 4, 5 |
| `status` | str[] | `active`, `contained`, `resolved`, `under_review` |
| `date_from` | date | Incident date range start |
| `date_to` | date | Incident date range end |
| `has_students_affected` | bool | Filter to incidents with students affected |
| `page` | int | Page number |
| `page_size` | int | Default 25; max 100 |
| `ordering` | str | e.g. `-severity`, `-date`, `status` |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Active incidents auto-refresh (every 2 min) | `hx-get="/api/.../incidents/active/"` `hx-trigger="every 2m"` `hx-target="#active-incidents-rows"` `hx-swap="outerHTML"` | Only active incident rows refreshed silently; table position preserved |
| Alert banner load | `hx-get="/api/.../incidents/alerts/"` `hx-trigger="load, every 2m"` `hx-target="#alert-banner"` `hx-swap="outerHTML"` | Permanent red banner persists until no active incidents |
| KPI bar load | `hx-get="/api/.../incidents/kpi/"` `hx-trigger="load"` `hx-target="#kpi-bar"` | On page load |
| KPI bar refresh post-action | Triggered via `hx-swap-oob="true"` on incident update/close responses | Out-of-band swap updates KPI without reload |
| Search debounce | `hx-get="/api/.../incidents/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#incidents-table-body"` `hx-include="#filter-form"` | Table rows replaced |
| Filter apply | `hx-get="/api/.../incidents/"` `hx-trigger="change"` `hx-target="#incidents-table-body"` `hx-include="#filter-form"` | Table rows replaced |
| Pagination | `hx-get="/api/.../incidents/?page={n}"` `hx-target="#incidents-table-body"` `hx-push-url="true"` | Page swap |
| Incident detail drawer open | `hx-get="/api/.../incidents/{incident_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Initial Report tab default |
| Drawer tab switch | `hx-get="/api/.../incidents/{incident_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` `hx-trigger="click"` | Lazy load on first click |
| Response log tab load | `hx-get="/api/.../incidents/{incident_id}/response-log/"` `hx-target="#response-log-content"` `hx-trigger="click[tab='response_log'] once"` | Loaded once on first click |
| Response log add (no full reload) | `hx-post="/api/.../incidents/{incident_id}/response-log/"` `hx-target="#response-log-list"` `hx-swap="beforeend"` `hx-on::after-request="clearForm();"` | New entry appended; response log drawer stays open |
| Impact tab load | `hx-get="/api/.../incidents/{incident_id}/impact/"` `hx-target="#impact-content"` `hx-trigger="click[tab='impact'] once"` | Loaded once |
| Post-incident review tab load | `hx-get="/api/.../incidents/{incident_id}/post-incident-review/"` `hx-target="#review-content"` `hx-trigger="click[tab='review'] once"` | Loaded once |
| Documents tab load | `hx-get="/api/.../incidents/{incident_id}/documents/"` `hx-target="#documents-content"` `hx-trigger="click[tab='documents'] once"` | Loaded once |
| Incident create submit | `hx-post="/api/.../incidents/"` `hx-target="#incidents-table-body"` `hx-on::after-request="closeDrawer(); fireToast(); refreshAlertBanner();"` | New row prepended; alert banner refreshed; severity 4–5 triggers escalation toast |
| Close incident modal submit | `hx-post="/api/.../incidents/{incident_id}/close/"` `hx-target="#incident-row-{incident_id}"` `hx-swap="outerHTML"` `hx-on::after-request="closeModal(); fireToast(); refreshKPI(); refreshAlertBanner();"` | Row status updated; KPI and alert banner refreshed |
| Escalate modal submit | `hx-post="/api/.../incidents/{incident_id}/escalate/"` `hx-target="#escalate-status-{incident_id}"` `hx-on::after-request="closeModal(); fireToast();"` | Escalation recorded; modal closed |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
