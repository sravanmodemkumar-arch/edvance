# 19 — Security Incident Register

> **URL:** `/group/welfare/security/incidents/`
> **File:** `19-security-incident-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group CCTV & Security Head (Role 93, G3)

---

## 1. Purpose

Register of all security incidents across all branches — unauthorized entry, theft, vandalism, physical altercation at gate, trespassing, suspicious activity, intruder detection, equipment tampering, fire alarm activation (non-drill), and any incident involving CCTV tampering. Each incident must be logged with full detail, CCTV footage reference (timestamp and camera ID), guard on duty, immediate action taken, and resolution status.

Serious incidents involving outsiders, weapons, or any direct threat to student safety must be escalated to Group COO within 1 hour of occurrence, and a police complaint filed if required. The Security Head reviews all incidents, identifies patterns (repeated incidents at the same branch indicate a systemic security gap), and submits the monthly security report to Group COO.

Scale: 5–100 incidents per month across all branches.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group CCTV & Security Head | G3 | Full — view, log, update, escalate, close incidents, export | Primary owner |
| Group COO | G4 | View — all incidents; receive escalations; read-only except can add resolution notes on escalated items | No create/delete |
| Branch Security Supervisor | G2 | View own branch incidents; log new incidents for own branch; update own branch incidents (status + notes) | Cannot escalate or close without G3 review |
| Branch Principal | G2 | View own branch incidents summary only — count by severity and type; no individual records | Read-only summary |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('cctv_security_head', 'branch_security_supervisor')` with branch-scope filter for G2.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Security  ›  Security Incident Register
```

### 3.2 Page Header
```
Security Incident Register                  [+ Log New Incident]  [Export Register ↓]  [Monthly Report ↓]
[Group Name] — Group CCTV & Security Head · Last refreshed: [timestamp]
[N] Open Incidents  ·  [N] Critical/High Open  ·  [N] Escalated to COO  ·  [N] Police-Reported This Month
```

### 3.3 Alert Banner (conditional — critical open items requiring same-day action)

| Condition | Banner Text | Severity |
|---|---|---|
| Critical incident open > 1 hour without COO escalation | "Critical incident [ID] at [Branch] has been open for [N] hours without COO escalation. Escalate immediately." | Red |
| Critical incident open > 24 hours unresolved | "Critical incident [ID] at [Branch] has been unresolved for [N] hours. Immediate review required." | Red |
| Incident requires police report but not yet filed | "Incident [ID] at [Branch] is rated High/Critical and involves an outsider. Police complaint may be required. Review status." | Red |
| Branch with 3+ incidents in current month (pattern) | "[Branch] has logged [N] incidents this month — possible systemic security gap. Investigate and escalate." | Amber |
| Incident with CCTV reference that is now overdue for footage download | "CCTV footage for Incident [ID] is referenced to [Camera ID] at [timestamp]. Footage may be overwritten if not downloaded — DVR retention period is [N] days." | Amber |

Max 5 alerts visible. Alert links route to the specific incident record. "View all escalations → COO Escalation Log" shown below alerts.

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open Incidents | Total open incidents across all branches (status: Open + Investigated) | Green = 0 · Yellow 1–5 · Red > 5 | → Main table filtered to status Open/Investigated |
| Critical / High Severity Open | Open incidents rated Critical or High | Green = 0 · Yellow 1–2 · Red > 2 | → Main table filtered to severity Critical + High, status Open |
| Police-Reported This Month | Incidents with Police Reported = Yes in current calendar month | Blue always (informational) | → Main table filtered to police_reported=Yes and current month |
| Avg Resolution Days | Mean days from incident logged to status Closed, for closed incidents this month | Green < 3d · Yellow 3–7d · Red > 7d | → Main table filtered to status Closed |
| Branches with Repeat Incidents (3+ / month) | Branches that have 3 or more incidents logged in the current month | Green = 0 · Yellow 1–2 · Red > 2 | → Section 5.2 |
| COO Escalated Open | Incidents currently escalated to COO and not yet resolved | Green = 0 · Yellow 1–2 · Red > 2 | → Main table filtered to coo_escalated=True, status Open |
| Incidents This Month | Total incidents logged in the current calendar month, all branches | Blue always (informational) | → Main table filtered to current month |
| CCTV Evidence Attached | % of incidents this month that have at least one CCTV reference recorded | Green ≥ 80% · Yellow 60–79% · Red < 60% | → Main table filtered to cctv_reference=empty |

**HTMX:** `hx-trigger="every 3m"` → Open Incidents, Critical/High Open, and COO Escalated Open auto-refresh.

---

## 5. Sections

### 5.1 Incident Register Table (Primary Table)

> Complete log of all security incidents across all branches.

**Search:** Incident ID, branch name, incident type, persons involved. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Date Range | Date range picker | Default: Last 30 days; max range 365 days |
| Incident Type | Checkbox | Unauthorized Entry / Theft / Vandalism / Physical Altercation / Trespassing / Suspicious Activity / Intruder Detection / Equipment Tampering / Fire Alarm (Non-drill) / CCTV Tampering / Other |
| Severity | Checkbox | Low / Medium / High / Critical |
| Police Reported | Radio | All · Yes · No |
| Status | Checkbox | Open / Investigated / Resolved / Closed |
| COO Escalated | Toggle | Show only COO-escalated incidents |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Incident ID | ✅ | System-generated (e.g., INC-2026-0047); link → `incident-detail` drawer |
| Date/Time | ✅ | Datetime of incident occurrence |
| Branch | ✅ | Branch name |
| Area | ✅ | Gate / Hostel / Parking / Corridor / Campus / Admin Block |
| Incident Type | ✅ | Type badge |
| Severity | ✅ | Badge: Critical (Dark Red) · High (Red) · Medium (Orange) · Low (Grey) |
| Guard On Duty | ✅ | Guard name |
| Persons Involved | ❌ | Brief description (e.g., "External male, 1 student") |
| CCTV Reference | ❌ | Camera ID + timestamp if provided; "—" if none; ⚠ icon if present but footage near retention limit |
| Police Reported | ✅ | Yes (Red badge) / No (Grey) |
| Status | ✅ | Open (Red) · Investigated (Amber) · Resolved (Blue) · Closed (Green) |
| Actions | ❌ | View · Update Status · Escalate to COO |

**Default sort:** Severity (Critical first, then High, then Medium, then Low), then Date/Time descending.
**Pagination:** Server-side · 25/page.

---

### 5.2 Branch Incident Heatmap

> Branch-level incident count and pattern summary for the current month.

**Display:** Table with conditional row highlighting.

**Columns:**
| Column | Notes |
|---|---|
| Branch | Branch name |
| Incidents This Month | Total count; Red background if ≥ 3 (pattern flag) |
| Critical / High | Count of high-severity incidents; Red if > 0 |
| Police Reported | Count with police complaint filed |
| Open Incidents | Current open count; Red if > 0 |
| Avg Resolution Days | Mean days to close; Red if > 7 |
| Pattern Flag | Badge: Repeat Incident Pattern (Red) · Elevated (Amber) · Normal (Green) |
| Actions | View Incidents · Investigate Pattern |

**Default sort:** Pattern Flag (Repeat first), then Incidents This Month descending.
**Pagination:** Server-side · 25/page.

---

## 6. Drawers / Modals

### 6.1 Drawer: `incident-detail`
- **Trigger:** Incident ID link in Section 5.1 table
- **Width:** 700px
- **Tabs:** Overview · CCTV Evidence · Action Log · Resolution

**Overview tab:**
| Field | Notes |
|---|---|
| Incident ID | Read-only |
| Status | Badge |
| Branch | Read-only |
| Date & Time of Incident | Read-only |
| Date & Time Logged | Read-only (may differ from occurrence time) |
| Area | Gate / Hostel / Parking / Corridor / Campus / Admin Block |
| Incident Type | Type badge |
| Severity | Severity badge |
| Incident Description | Full narrative; read-only |
| Persons Involved | Names/descriptions of individuals involved |
| Guard On Duty | Guard name · Shift · Contact |
| Additional Guards / Staff Responding | List |
| Immediate Action Taken | Narrative of response at time of incident |
| Police Reported | Yes / No |
| Police Station | If reported |
| FIR Number | If available |
| COO Escalated | Yes / No · Escalation timestamp if Yes |
| Logged By | User name + role + timestamp |
| Last Updated By | User name + role + timestamp |

**CCTV Evidence tab:**
- List of all CCTV references attached to this incident:
  - Camera ID · Area Type · Location Description · Footage Timestamp (start–end) · Footage Status (Available / Overwritten / Downloaded / Requested)
- [+ Add CCTV Reference] button (G3 only)
- [Mark Footage Downloaded] toggle per reference
- Note: "Footage retention on this DVR: [N] days. Footage may be overwritten on [calculated date]." Warning if < 7 days remaining.

**Action Log tab:**
- Chronological timeline of all actions taken on this incident:
  - Date/Time · Action Type (Status Change / Note Added / Escalated / CCTV Reference Added / Police Report Filed / Footage Downloaded) · Performed By · Note text
- [+ Add Note] button — opens inline textarea with submit
- Paginated if > 20 entries

**Resolution tab:**
| Field | Notes |
|---|---|
| Root Cause Analysis | Textarea; filled when resolving |
| Corrective Actions Taken | Textarea; what was done to prevent recurrence |
| Follow-up Required | Toggle |
| Follow-up Details | Textarea; conditional on Follow-up = ON |
| Resolution Date | Date of resolution |
| Resolved By | User name |
| Final Outcome | Select: Perpetrator Identified / Police Action / Dismissed (no evidence) / Process Improvement / Other |
| Closure Approved By | G3 user name and date (required before status = Closed) |

**Footer actions (G3):**
- [Update Status] → opens `update-status` drawer
- [Escalate to COO] → opens `escalate-to-coo` modal
- [Close Incident] → confirm dialog with required closure summary

---

### 6.2 Drawer: `new-incident`
- **Trigger:** [+ Log New Incident] button in page header
- **Width:** 620px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Searchable dropdown | Required |
| Date of Incident | Date picker | Required; cannot be future date |
| Time of Incident | Time picker | Required |
| Area | Select | Gate / Hostel / Parking / Corridor / Campus / Admin Block / Other · Required |
| Incident Type | Select | Full list as per filters · Required |
| Severity | Radio | Low / Medium / High / Critical · Required |
| Incident Description | Textarea · max 1000 chars | Required · min 50 chars |
| Persons Involved | Textarea · max 400 chars | Required · e.g., "Unknown male, approx. 30s / Student Name [class]" |
| Guard On Duty | Searchable dropdown (guards assigned to this branch and shift) | Required |
| Additional Responders | Text · max 200 chars | Optional |
| Immediate Action Taken | Textarea · max 600 chars | Required · min 30 chars |
| CCTV Reference — Camera ID | Searchable (cameras at selected branch) | Optional; add multiple |
| CCTV Reference — Footage Timestamp Start | Datetime picker | Conditional: required if Camera ID provided |
| CCTV Reference — Footage Timestamp End | Datetime picker | Conditional: required if Camera ID provided |
| Police Reported | Toggle | Default: OFF |
| Police Station | Text · max 100 chars | Required if Police Reported = ON |
| FIR Number | Text · max 50 chars | Optional |
| Initial Status | Radio | Open (default) / Investigated | Required |
| Linked Visitor Entry | Searchable (visitor log entries) | Optional; if incident involved a visitor |

**Auto-escalation prompt:** After saving, if Severity is Critical or High and involves persons from outside the campus: system shows a prompt: "This incident may require COO escalation within 1 hour per policy. Escalate now?" with [Escalate Now] and [Later] buttons.

**Validation:**
- Incident Description and Immediate Action Taken both require minimum character counts.
- CCTV Footage Timestamp End must be after Start.
- Cannot log an incident dated more than 7 days in the past without a mandatory "Reason for Delayed Logging" field appearing.

**Footer:** [Cancel] [Log Incident →]

---

### 6.3 Drawer: `update-status`
- **Trigger:** "Update Status" action in table row or incident-detail drawer footer
- **Width:** 440px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Incident ID | Read-only pre-filled | — |
| Current Status | Read-only pre-filled | — |
| New Status | Select | Open / Investigated / Resolved / Closed · Required; cannot go backward |
| Severity Update | Radio | Keep existing / Change to: Low / Medium / High / Critical | Optional; requires justification if changed |
| Status Update Note | Textarea · max 600 chars | Required · min 30 chars |
| Root Cause (required for Resolved) | Textarea · max 500 chars | Required if new status = Resolved |
| Corrective Actions (required for Resolved) | Textarea · max 500 chars | Required if new status = Resolved |
| Closure Confirmation (required for Closed) | Checkbox | "I confirm all actions have been completed and the incident is fully resolved" · Required for Closed |

**Validation:**
- Status can only advance forward (Open → Investigated → Resolved → Closed).
- Closed status requires the confirmation checkbox.
- Resolved status requires both Root Cause and Corrective Actions.

**Footer:** [Cancel] [Save Status Update →]

---

### 6.4 Modal: `escalate-to-coo`
- **Trigger:** "Escalate to COO" action in table row or incident-detail drawer footer
- **Width:** 400px
- **Type:** Modal (not slide-in drawer) — requires explicit focus; overlay behind

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Incident ID | Read-only pre-filled | — |
| Branch | Read-only pre-filled | — |
| Severity | Read-only pre-filled | — |
| Escalation Reason | Textarea · max 500 chars | Required · min 30 chars |
| COO Notification Message | Textarea · max 600 chars | Required; pre-populated with template: "Incident [ID] at [Branch] on [date]. Type: [type]. Severity: [severity]. Immediate attention required." — editable |
| Police Template Required | Checkbox | "Generate police complaint template" — if checked, a formatted complaint draft is generated and available for download |
| Escalation Timestamp | Read-only | Current date/time auto-set |

**COO auto-notification:** On confirmation, system sends: (a) portal notification to all G4 COO users in the group, (b) email to COO using registered email, (c) SMS to COO mobile if configured.

**Police template:** If "Generate police complaint template" is checked, a formatted PDF template is generated on submit, downloadable from the incident-detail CCTV Evidence tab.

**Footer:** [Cancel] [Confirm Escalation →]

**On submit:** POST to escalation endpoint · `incident-detail` drawer refreshes · incident row badge updated to "COO Escalated" · toast warning displayed · KPI "COO Escalated Open" increments.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Incident logged | "Security incident [ID] logged at [Branch]. Severity: [Level]." | Success | 4s |
| Critical incident — escalation prompt | "Incident [ID] is Critical severity. COO escalation recommended within 1 hour." | Warning | 8s (persistent) |
| Status updated | "Incident [ID] status updated to [New Status]." | Success | 4s |
| Incident closed | "Incident [ID] closed. Resolution recorded." | Success | 4s |
| Escalated to COO | "Incident [ID] escalated to Group COO. COO notified by portal, email, and SMS." | Warning | 6s |
| CCTV reference added | "CCTV reference added to Incident [ID] — Camera [ID], footage [start–end]." | Success | 4s |
| Footage download marked | "CCTV footage for Incident [ID] marked as downloaded and secured." | Info | 4s |
| Police template generated | "Police complaint template for Incident [ID] generated. Download from incident record." | Info | 5s |
| Export ready | "Security register export is being prepared. Download will begin shortly." | Info | 4s |
| Monthly report ready | "Monthly security report generated. Download ready." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No incidents logged | "No Security Incidents Recorded" | "No security incidents have been logged for the selected period and branch." | [+ Log New Incident] |
| No open incidents | "No Open Incidents" | "All security incidents across all branches are resolved or closed." | — |
| No critical/high incidents | "No High-Severity Incidents" | "There are no Critical or High severity open incidents across any branch." | — |
| No COO-escalated incidents | "No COO Escalations Open" | "No incidents are currently escalated to the Group COO." | — |
| Search returns no results | "No Incidents Found" | "No incidents match your search terms or applied filters." | [Clear Filters] |
| No repeat incident branches | "No Repeat Incident Pattern Detected" | "No branch has logged 3 or more incidents this month." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + incident table (15 rows × 11 columns) + branch heatmap table + alerts |
| Table filter/search | Inline skeleton rows (8 rows × 11 columns) |
| KPI auto-refresh | Shimmer on Open Incidents, Critical/High Open, COO Escalated Open card values |
| Incident detail drawer open | 700px drawer skeleton with 4-tab bar; each tab loads lazily on first click |
| CCTV Evidence tab | List skeleton (3 rows with camera + timestamp placeholders) |
| Action Log tab | Timeline skeleton (5 entries with date + text placeholders) |
| New incident form open | 620px drawer with 18 field skeletons |
| Update status drawer | 440px drawer with 7 field skeletons |
| Escalate to COO modal | 400px modal with 5 field skeletons |
| Branch heatmap panel | Table skeleton (10 rows × 7 columns) |

---

## 10. Role-Based UI Visibility

| Element | CCTV & Security Head G3 | Group COO G4 | Branch Security Supervisor G2 | Branch Principal G2 |
|---|---|---|---|---|
| View All Branches Register | ✅ | ✅ (read-only) | Own branch only | Own branch summary only |
| Log New Incident | ✅ | ❌ | ✅ (own branch) | ❌ |
| Update Incident Status | ✅ | ❌ (add resolution note only on escalated) | ✅ (own branch; Open → Investigated only) | ❌ |
| Escalate to COO | ✅ | ❌ | ❌ | ❌ |
| Close Incident | ✅ | ❌ | ❌ | ❌ |
| Add CCTV Reference | ✅ | ❌ | ✅ (own branch) | ❌ |
| Generate Police Template | ✅ | ❌ | ❌ | ❌ |
| View Persons Involved Detail | ✅ | ✅ | ✅ (own branch) | ❌ |
| Export Register | ✅ | ✅ | ✅ (own branch) | ❌ |
| Generate Monthly Report | ✅ | ✅ | ❌ | ❌ |
| View Branch Heatmap | ✅ | ✅ (read-only) | ✅ (own branch row) | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/security/incidents/` | JWT (G3+) | Incident register table; params: `branch_id`, `date_from`, `date_to`, `incident_type`, `severity`, `police_reported`, `status`, `coo_escalated`, `q`, `page` |
| GET | `/api/v1/group/{group_id}/welfare/security/incidents/kpi-cards/` | JWT (G3+) | KPI auto-refresh payload |
| GET | `/api/v1/group/{group_id}/welfare/security/incidents/branch-heatmap/` | JWT (G3+) | Branch incident pattern heatmap table |
| GET | `/api/v1/group/{group_id}/welfare/security/incidents/{incident_id}/` | JWT (G3+) | Single incident detail drawer payload |
| POST | `/api/v1/group/{group_id}/welfare/security/incidents/` | JWT (G3, G2-branch) | Log new security incident |
| PATCH | `/api/v1/group/{group_id}/welfare/security/incidents/{incident_id}/status/` | JWT (G3, G2-branch) | Update incident status + notes |
| POST | `/api/v1/group/{group_id}/welfare/security/incidents/{incident_id}/escalate/` | JWT (G3) | Escalate incident to COO |
| POST | `/api/v1/group/{group_id}/welfare/security/incidents/{incident_id}/cctv-reference/` | JWT (G3, G2-branch) | Add CCTV footage reference |
| PATCH | `/api/v1/group/{group_id}/welfare/security/incidents/{incident_id}/cctv-reference/{ref_id}/` | JWT (G3) | Mark footage as downloaded |
| POST | `/api/v1/group/{group_id}/welfare/security/incidents/{incident_id}/notes/` | JWT (G3+) | Add action log note |
| GET | `/api/v1/group/{group_id}/welfare/security/incidents/export/` | JWT (G3+) | Async export of incident register (CSV/XLSX) |
| GET | `/api/v1/group/{group_id}/welfare/security/incidents/monthly-report/` | JWT (G3+) | Generate monthly security report PDF |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 3m` | GET `.../incidents/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Incident table search | `input delay:300ms` | GET `.../incidents/?q={val}` | `#incident-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../incidents/?{filters}` | `#incident-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../incidents/?page={n}` | `#incident-table-section` | `innerHTML` |
| Open incident detail drawer | `click` on Incident ID | GET `.../incidents/{id}/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch (lazy) | `click` on tab | GET `.../incidents/{id}/?tab={name}` | `#drawer-tab-content` | `innerHTML` |
| Add action note (inline) | `click` submit | POST `.../incidents/{id}/notes/` | `#action-log-list` | `beforeend` |
| Update status submit | `click` | PATCH `.../incidents/{id}/status/` | `#incident-row-{id}` | `outerHTML` |
| Escalate to COO confirm | `click` | POST `.../incidents/{id}/escalate/` | `#incident-row-{id}` | `outerHTML` |
| Add CCTV reference | `click` | POST `.../incidents/{id}/cctv-reference/` | `#cctv-reference-list` | `beforeend` |
| Mark footage downloaded | `change` | PATCH `.../incidents/{id}/cctv-reference/{ref_id}/` | `#cctv-ref-row-{ref_id}` | `outerHTML` |
| Branch heatmap load | `load` | GET `.../incidents/branch-heatmap/` | `#branch-heatmap` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
