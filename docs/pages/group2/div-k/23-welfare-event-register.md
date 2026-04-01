# 23 — Welfare Event Register

> **URL:** `/group/welfare/events/register/`
> **File:** `23-welfare-event-register.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Welfare Events Coordinator (Role 95, G3) — primary owner

---

## 1. Purpose

Master register of all welfare events across all branches, organised by severity classification. A welfare event is any incident affecting student or staff wellbeing that requires formal logging, a structured response, and documented closure.

**Severity Classification:**

| Severity | Label | Definition | Resolution SLA | Escalation |
|---|---|---|---|---|
| 1 | Minor | Resolved same day with no external involvement: scraped knee, minor peer conflict, homesickness episode, minor food complaint | Same day | Branch Welfare Officer |
| 2 | Moderate | 48-hour resolution window; parent must be notified: bullying report, minor injury, illness requiring hospitalisation, student run-away attempt found within campus | 48 hours | Branch Principal |
| 3 | Serious | 7-day investigation; COO notified; may involve police or hospital: serious injury, major bullying with physical harm, serious food poisoning, student run-away found outside campus, fire or flood | 7 days | Group COO — auto-notified within 15 minutes of logging |
| 4 | Critical | Immediate Group Chairman escalation; NCPCR mandatory reporting; police FIR may be required: suicide attempt, sexual abuse, serious assault, student death, mass food poisoning | Immediate | Group Chairman + COO + Child Protection Officer + Branch Principal — auto-notified within 5 minutes; NCPCR reporting ticket auto-created |

Every event must be logged on the day it occurs. Branch staff log events at the branch level; the Group Welfare Events Coordinator monitors all events across branches from this consolidated view.

Scale: 200–2,000 events per year across all branches. The overwhelming majority are Severity 1–2. Severity 3–4 events are rare but are the highest-priority records in the system and require immediate, audit-ready documentation.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Welfare Events Coordinator | G3 | Full read + create + status update + close + export | Primary owner; all branches |
| Branch Welfare Officer | Branch | Create + edit own branch events; read own branch only | Cannot close events; cannot view other branches |
| Branch Principal | Branch | Read own branch all severities; receive auto-notifications for S2–S4 | No create; no edit |
| Group COO | G4 | Read all; receive auto-notification for S3–S4 | No create; no edit |
| Group Chairman / CEO | G5 | Read all (dashboard summary + S3–S4 list); receive auto-notification for S4 | No create; no edit |
| Child Protection Officer | G3 | Read all S3–S4; receive auto-notification for S4 | No create; no edit |
| All other roles | — | No access | — |

> **Access enforcement:** `@require_role('welfare_coordinator', 'branch_welfare_officer', 'branch_principal', 'coo', 'chairman', 'child_protection_officer')` with branch-scoped querysets applied for Branch Welfare Officer and Branch Principal.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Events  ›  Welfare Event Register
```

### 3.2 Page Header
- **Title:** `Welfare Event Register`
- **Subtitle:** `[N] Open Events · [N] This Month · SLA Compliance [X]% · Last updated [timestamp]`
- **Right controls:** `+ Log New Event` (Welfare Coordinator + Branch Welfare Officer) · `Advanced Filters` · `Export CSV` (Welfare Coordinator only)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Any Severity 4 event open | "CRITICAL: [N] Severity 4 event(s) are open. Immediate attention and escalation required." | Red (persistent; cannot dismiss) |
| Severity 3 event open > 7 days | "[N] Severity 3 events are past their 7-day resolution SLA. Escalation to COO triggered." | Red |
| Severity 2 event open > 48 hours | "[N] Severity 2 events have breached their 48-hour SLA. Review immediately." | Amber |
| Branch with zero events for > 30 days | "[N] branches have logged zero welfare events in the past 30 days. Under-reporting is flagged." | Amber |
| NCPCR ticket auto-created | "An NCPCR mandatory report ticket has been auto-created for Event [ID]. Complete it within the NCPCR statutory deadline." | Red |

---

## 4. KPI Summary Bar

Eight cards in a responsive 4×2 grid. All metrics reflect the currently selected Branch and Date Range filters; default is all branches, current academic year.

| # | Card | Metric | Colour Rule |
|---|---|---|---|
| 1 | Open Severity 3–4 | Count of events at Severity 3 or 4 with status ≠ Closed | Red if > 0 · Green = 0 |
| 2 | All Open Events | Count of events with status = Open or Under Review | Red > 20 · Yellow 5–20 · Green < 5 |
| 3 | Total This Month | Count of events logged in current calendar month | Blue always |
| 4 | Avg Resolution Days | Mean days from log date to Closed date (closed events only, current year) | Green ≤ 1.5 · Yellow 1.5–3 · Red > 3 |
| 5 | SLA Compliance % | (Events resolved within SLA / Total resolved events) × 100 | Green ≥ 90% · Yellow 70–89% · Red < 70% |
| 6 | Under-Reporting Flags | Count of branches with zero events for > 30 days | Red > 3 · Yellow 1–3 · Green = 0 |
| 7 | S1 / S2 Breakdown | Two-segment mini bar: Severity 1 count vs Severity 2 count (current month) | Visual only |
| 8 | Events by Type | Mini donut: top 5 event types (current month) | Visual only |

---

## 5. Main Table — Welfare Event Register

### 5.1 Search
Full-text search on: Event ID, branch name, event type, reported-by name. Debounce 300 ms, minimum 2 characters.

### 5.2 Advanced Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Severity | Checkbox | 1 — Minor · 2 — Moderate · 3 — Serious · 4 — Critical |
| Date Range | Date picker | From – To (event log date) |
| Event Type | Multi-select | Bullying · Injury · Illness · Run-away · Food Complaint · Fire / Flood · Conflict · Abuse · Other |
| Status | Checkbox | Open · Under Review · Resolved · Closed |
| Hostel vs Day Scholar | Radio | All · Hostel Only · Day Scholar Only |
| SLA Status | Radio | All · Within SLA · SLA Breached |
| Reported By Role | Multi-select | All roles |

### 5.3 Table Columns

| Column | Sortable | Notes |
|---|---|---|
| Event ID | ✅ | System-generated (e.g., WEL-2026-00341) |
| Date | ✅ | DD-MMM-YYYY; time shown on hover |
| Branch | ✅ | |
| Hostel / Day | ✅ | Hostel (blue) / Day Scholar (grey) badge |
| Event Type | ✅ | Text tag |
| Severity | ✅ | 1 (grey) · 2 (amber) · 3 (orange) · 4 (red — bold) colour badge |
| Persons Affected | ✅ | Integer count |
| Reported By | ✅ | Role name |
| Current Status | ✅ | Open (blue) · Under Review (purple) · Resolved (green) · Closed (dark grey) badge |
| SLA Status | ✅ | Within SLA (green) · Breached (red) · N/A (grey) badge |
| Last Update | ✅ | Relative time ("3 hours ago") with absolute timestamp on hover |
| Actions | ❌ | View · Update · Close (role-gated) |

**Default sort:** Severity descending (4 → 1), then Date descending within same severity.
**Pagination:** Server-side · 25 rows/page.
**Row highlight:** Severity 4 rows have a persistent red left border; Severity 3 rows have an orange left border.

---

## 6. Drawers / Modals

### 6.1 Drawer — `event-detail` (720px, right side)

Triggered by **View** in Actions column.

**Header:** Event ID · Severity badge · Status badge · Branch

**Tabs:**

#### Tab 1 — Overview
| Field | Notes |
|---|---|
| Event ID | Read-only |
| Log Date / Time | Read-only |
| Branch | Read-only |
| Hostel / Day Scholar | Read-only |
| Event Type | Read-only |
| Severity | Read-only badge with label |
| Persons Affected | Count (integer) |
| Persons Affected — Details | Names / roles / age groups (free text) |
| Reported By — Name | |
| Reported By — Role | |
| Description | Full free-text description of the event |
| Immediate Actions Taken | Free text — what was done within the first hour |
| Escalation Triggered | Yes / No; if Yes, list of notified parties with timestamps |

#### Tab 2 — Timeline
Chronological event log from creation to current status.

| Column | Notes |
|---|---|
| Timestamp | DD-MMM-YYYY HH:MM |
| Actor | Name + Role |
| Action | Created / Status Changed / Note Added / Severity Changed / Notified [party] |
| Detail | Free-text note or change description |

New entries are appended at the top (most recent first). Immutable — entries cannot be edited or deleted.

#### Tab 3 — Response Log
Free-text response notes added by Welfare Coordinator or Branch Welfare Officer. Each note shows: author, timestamp, note text, and whether it was shared with the branch principal.

**Footer:** `+ Add Response Note` (Welfare Coordinator + Branch Welfare Officer) — inline textarea form.

#### Tab 4 — Escalation
Shows all escalation records for this event:
- Auto-escalations (S3/S4 notifications with delivery confirmation timestamps)
- Manual escalations added by the coordinator
- NCPCR ticket status (S4 only)

| Column | Notes |
|---|---|
| Escalation Type | Auto / Manual |
| Escalated To | Role name + person name |
| Triggered At | Timestamp |
| Delivery Confirmed | Yes / Pending |
| NCPCR Ticket ID | If applicable; link to ticket |

**Footer:** `+ Manual Escalation` (Welfare Coordinator only)

#### Tab 5 — Related Welfare Events
List of other welfare events from the same branch in the past 90 days involving the same persons affected or the same event type. Allows the Coordinator to identify patterns.

| Column | Notes |
|---|---|
| Event ID | Link to that event's detail drawer |
| Date | |
| Event Type | |
| Severity | Badge |
| Status | Badge |

If no related events: *"No related events found for this branch in the past 90 days."*

#### Tab 6 — Closure
Shown as editable only when Status = Resolved or Coordinator initiates closure.
| Field | Type | Validation |
|---|---|---|
| Resolution Date | Date picker | Required |
| Resolution Summary | Textarea (max 2,000 chars) | Required |
| Root Cause | Single-select: Negligence / Infrastructure Gap / Staffing Issue / Student Behaviour / External Factor / Unknown / Other | Required |
| Lessons Learned | Textarea (max 1,000 chars) | Optional |
| Follow-up Actions | Textarea — list of any ongoing actions post-closure | Optional |
| Closed By | Read-only (logged-in user) | Auto |

**Footer:** `Cancel` · `Close Event` (Welfare Coordinator only)

---

### 6.2 Drawer — `new-event` (640px, right side)

Triggered by **+ Log New Event** button.

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select (auto-set for Branch Welfare Officer) | Required |
| Event Date | Date picker (defaults to today) | Required; not future |
| Event Time | Time picker | Required |
| Hostel / Day Scholar | Radio: Hostel · Day Scholar · Both | Required |
| Severity | Radio: 1 (Minor) · 2 (Moderate) · 3 (Serious) · 4 (Critical) | Required |
| Event Type | Single-select | Required |
| Persons Affected — Count | Number input | Required; min 1 |
| Persons Affected — Details | Textarea (max 500 chars) — names/roles/classes | Optional but recommended |
| Description | Textarea (max 3,000 chars) | Required |
| Immediate Actions Taken | Textarea (max 1,000 chars) | Required |
| Reported By — Name | Text input (auto-filled if logged-in user) | Required |
| Reported By — Role | Single-select | Required |
| Escalation Triggered | Toggle: Yes / No | Required |
| Escalated To | Multi-select (shown if Escalation = Yes): Branch Principal / Group COO / Police / Hospital / Parents | Required if Escalation = Yes |

> **Severity selector UI:** Each severity level is a clickable card (not a plain radio) with: the severity number, label, and a 2-line description of what qualifies. Makes it harder to mis-classify.

> **Severity 3 warning:** On selecting Severity 3, an inline amber banner appears: *"Logging a Severity 3 event will automatically notify the Group COO within 15 minutes of saving."*

> **Severity 4 warning:** On selecting Severity 4, a red inline alert appears: *"CRITICAL: Saving this event will immediately notify the Group Chairman, COO, Child Protection Officer, and Branch Principal. An NCPCR reporting ticket will be auto-created. Ensure all details are accurate."*

**Footer:** `Cancel` · `Log Event`

**Validation:**
- Description: required; min 50 characters
- Immediate Actions Taken: required; min 20 characters
- Severity 2+: parent notification checkbox shown and must be acknowledged
- Severity 4: confirmation checkbox required: *"I confirm this event meets Severity 4 criteria and I understand the automatic escalation that will occur."*

---

### 6.3 Drawer — `update-event` (520px, right side)

Triggered by **Update** in Actions column. Available to Welfare Coordinator and Branch Welfare Officer (own branch).

| Field | Type | Validation |
|---|---|---|
| Current Status | Read-only badge | |
| New Status | Single-select: Open · Under Review · Resolved | Required; cannot set to Closed via this drawer |
| Severity Change | Toggle: No change · Change severity (with justification) | Optional |
| New Severity | Radio (shown if severity change selected) | Required if toggled |
| Severity Change Reason | Textarea (max 500 chars) | Required if severity changed |
| Response Note | Textarea (max 2,000 chars) — what has been done since last update | Required |
| Parent Notified | Radio: Yes · No · N/A | Required for S2+ |
| Parent Notification Date | Date picker | Required if Parent Notified = Yes |
| Next Step Planned | Textarea (max 500 chars) | Optional |

**Footer:** `Cancel` · `Save Update`

**Behaviour:** On save, a new entry is appended to the Timeline tab. If severity was changed, an auto-notification is triggered for the newly applicable escalation audience.

---

### 6.4 Modal — `close-event` (440px, centred)

Triggered by **Close** in Actions column. Welfare Coordinator only.

| Field | Type | Validation |
|---|---|---|
| Event ID | Read-only | |
| Current Status | Read-only badge | |
| Resolution Date | Date picker | Required |
| Resolution Summary | Textarea (max 2,000 chars) | Required |
| Root Cause | Single-select | Required |
| Lessons Learned | Textarea (max 1,000 chars) | Optional |
| Follow-up Actions Required | Toggle: Yes / No | Required |
| Follow-up Actions | Textarea | Required if Yes |
| Confirm Closure | Checkbox: "I confirm this event has been fully resolved and is ready to close." | Required |

**Footer:** `Cancel` · `Close Event`

**Behaviour:** Status updated to Closed; closure timestamp recorded; Branch Welfare Officer receives notification; event is moved to the archived view (still searchable with Status = Closed filter).

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Event logged | "Welfare event [ID] logged successfully." | Success |
| Severity 3 event logged | "Severity 3 event logged. Group COO will be notified within 15 minutes." | Warning |
| Severity 4 event logged | "CRITICAL event logged. Chairman, COO, CPO, and Branch Principal have been notified. NCPCR ticket created." | Warning (prominent, auto-dismisses after 10 s) |
| Event updated | "Event [ID] updated. Timeline entry added." | Success |
| Severity changed | "Event severity changed to [N]. Escalation notifications triggered." | Warning |
| Event closed | "Event [ID] has been closed." | Success |
| Response note added | "Response note added to event [ID]." | Success |
| Manual escalation sent | "Escalation notification sent to [Role]." | Success |
| SLA breach alert | "SLA breached for Event [ID]. Auto-escalation triggered." | Warning |
| Validation error | "Please complete all required fields before saving." | Error |
| Severity 4 confirmation missing | "Please confirm that this event meets Severity 4 criteria before logging." | Error |
| Export triggered | "Export is being prepared." | Info |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No events for current filters | "No welfare events match the current filters." | "Try adjusting or clearing your filters." | `Clear Filters` button |
| No open events | "No open welfare events." | "All logged events have been resolved or closed." | — |
| No events this month | "No events logged this month." | "Events will appear here once logged by branch welfare officers." | `+ Log New Event` |
| Timeline tab — no entries | "No timeline entries yet." | — | — |
| Related events tab — none found | "No related events found for this branch in the past 90 days." | — | — |
| Escalation tab — no escalations | "No escalations recorded for this event." | — | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 8 KPI cards + table (10 grey rows × 12 columns) |
| Filter / search apply | Table body spinner overlay; KPI cards refresh after table resolves |
| Drawer open | Drawer skeleton: tab bar + 6 grey field blocks |
| Timeline tab load | Chronological skeleton: 5 grey timeline entries |
| Escalation auto-notification dispatch | Status indicator: "Notifying [role]…" with spinner in escalation tab; resolves to delivery timestamp |
| Close event modal submit | Spinner in modal footer + "Processing closure…" label; button disabled |
| Export generation | Button spinner + "Preparing export…" |
| Severity 4 auto-escalation | Full-width progress bar below new-event drawer footer: "Notifying Chairman · COO · CPO · Principal · Creating NCPCR Ticket" with step indicators |

---

## 10. Role-Based UI Visibility

| UI Element | Welfare Coordinator | Branch Welfare Officer | Branch Principal | COO | Chairman | CPO |
|---|---|---|---|---|---|---|
| Full cross-branch event list | ✅ | Own branch only | Own branch only | ✅ (read) | ✅ (S3–S4 + summary) | ✅ (S3–S4) |
| + Log New Event button | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Update button | ✅ | ✅ (own branch) | ❌ | ❌ | ❌ | ❌ |
| Close button | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Closure tab (in drawer) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Response Log — add note | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Escalation tab | ✅ | View only | View only | View only | View only | View only |
| Manual escalation button | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Under-reporting flags | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Export CSV | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| KPI bar — full detail | ✅ | Own branch | Own branch | ✅ | ✅ (S3–S4 counts) | S3–S4 counts |
| Alert banners — all | ✅ | Own branch banners | Own branch banners | S3–S4 | S4 only | S3–S4 |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/welfare/events/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/events/` | List events (paginated, filtered, role-scoped) | JWT + role check |
| POST | `/api/v1/group/{group_id}/welfare/events/` | Log new welfare event | Welfare Coordinator / Branch Welfare Officer |
| GET | `/api/v1/group/{group_id}/welfare/events/{event_id}/` | Retrieve event detail | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/welfare/events/{event_id}/` | Update event status / severity / notes | Welfare Coordinator / Branch Welfare Officer |
| POST | `/api/v1/group/{group_id}/welfare/events/{event_id}/close/` | Close event (record resolution) | Welfare Coordinator |
| POST | `/api/v1/group/{group_id}/welfare/events/{event_id}/notes/` | Add response note to timeline | Welfare Coordinator / Branch Welfare Officer |
| POST | `/api/v1/group/{group_id}/welfare/events/{event_id}/escalate/` | Manual escalation — notify additional parties | Welfare Coordinator |
| GET | `/api/v1/group/{group_id}/welfare/events/{event_id}/timeline/` | Full immutable timeline for event | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/events/{event_id}/related/` | Related events (same branch, 90-day window) | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/events/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/events/alerts/` | Active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/events/export/` | Export CSV | Welfare Coordinator |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Filter by branch ID(s) |
| `severity` | int[] | 1, 2, 3, 4 |
| `date_from` | date | Start of date range |
| `date_to` | date | End of date range |
| `event_type` | str[] | Event type slugs |
| `status` | str[] | `open`, `under_review`, `resolved`, `closed` |
| `hostel_only` | bool | Filter to hostel events only |
| `day_scholar_only` | bool | Filter to day scholar events only |
| `sla_breached` | bool | Filter to SLA-breached events |
| `reported_by_role` | str[] | Role slugs |
| `page` | int | Page number |
| `page_size` | int | Default 25, max 100 |
| `search` | str | Event ID, branch, event type |
| `sort_by` | str | Column name; prefix `-` for descending |

**Automatic escalation logic (server-side, not HTMX):**
- Severity 3 POST: Django signal triggers async task → sends notification to Group COO within 15 minutes via internal notification + email
- Severity 4 POST: Django signal triggers immediate synchronous notifications to Chairman + COO + Child Protection Officer + Branch Principal; NCPCR ticket record auto-created; all delivery timestamps logged to escalation table

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search input | `hx-get="/api/.../events/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#events-table-body"` `hx-include="#filter-form"` | Table body replaced on search |
| Filter apply | `hx-get="/api/.../events/"` `hx-trigger="change"` `hx-target="#events-table-body"` `hx-include="#filter-form"` | Table + KPI bar refreshed |
| Pagination | `hx-get="/api/.../events/?page={n}"` `hx-target="#events-table-body"` `hx-push-url="true"` | Page swap |
| Event detail drawer open | `hx-get="/api/.../events/{event_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in from right; Overview tab default |
| Drawer tab switch | `hx-get="/api/.../events/{event_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content swapped |
| Timeline tab load | `hx-get="/api/.../events/{event_id}/timeline/"` `hx-target="#timeline-content"` `hx-trigger="click[tab='timeline']"` | Timeline loaded on tab click |
| Related events tab load | `hx-get="/api/.../events/{event_id}/related/"` `hx-target="#related-content"` `hx-trigger="click[tab='related']"` | Related events list loaded |
| Add response note | `hx-post="/api/.../events/{event_id}/notes/"` `hx-target="#response-log-list"` `hx-swap="beforeend"` | Note appended to response log |
| New event form submit | `hx-post="/api/.../events/"` `hx-target="#events-table-body"` `hx-on::after-request="closeDrawer(); fireToast();"` | Row prepended; drawer closes; toast fires |
| Severity 3 selection | `hx-trigger="change"` `hx-target="#severity-warning-banner"` | Amber warning partial swapped in |
| Severity 4 selection | `hx-trigger="change"` `hx-target="#severity-warning-banner"` | Red critical alert partial swapped in; confirmation checkbox revealed |
| Update event submit | `hx-patch="/api/.../events/{event_id}/"` `hx-target="#event-row-{event_id}"` `hx-swap="outerHTML"` | Row updated; drawer closes; toast |
| Close event modal submit | `hx-post="/api/.../events/{event_id}/close/"` `hx-target="#event-row-{event_id}"` `hx-swap="outerHTML"` | Row status updated to Closed badge; modal closes |
| Manual escalation submit | `hx-post="/api/.../events/{event_id}/escalate/"` `hx-target="#escalation-list"` `hx-swap="beforeend"` | Escalation entry appended; toast fires |
| KPI bar refresh | `hx-get="/api/.../events/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |
| Alert banner load | `hx-get="/api/.../events/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Conditional banner display |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
