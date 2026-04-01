# 06 — Welfare Events Dashboard

> **URL:** `/group/welfare/events/`
> **File:** `06-welfare-events-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Welfare Events Coordinator (Role 95, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Welfare Events Coordinator. Command centre for tracking and managing welfare events across all branches with four-tier severity classification. A welfare event is any incident or situation that affects the physical, emotional, or social wellbeing of students or staff — ranging from minor same-day incidents to critical events requiring national regulatory reporting and immediate escalation to the Group Chairman.

The Group Welfare Events Coordinator ensures every branch logs all welfare incidents in real time, monitors unresolved events for SLA compliance, enforces severity-appropriate escalation pathways (Severity 3–4 events must reach the Group COO within 2 hours of occurrence and the Chairman within 4 hours), and compiles the monthly welfare digest for the Chairman. The role also acts as the system owner for welfare event classification, ensuring branches do not under-report or miscategorise incidents. Severity 4 events — suicide attempts, serious physical or sexual abuse, police involvement, NCPCR-reportable incidents — trigger an automatic persistent alert that cannot be dismissed until the event is closed. Under-reporting is treated as a systemic failure: branches that have logged zero events for a sustained period are flagged as potentially under-reporting.

Severity Classification:
- Severity 1 (Grey): Minor — first aid administered, minor interpersonal conflict, resolved same day with no escalation
- Severity 2 (Yellow): Moderate — parent notification required, counsellor involvement, 48-hour resolution expected
- Severity 3 (Orange): Serious — police or hospital involvement, COO notification mandatory within 2 hours, 7-day investigation
- Severity 4 (Red): Critical — suicide attempt, severe abuse (physical/sexual), police FIR, NCPCR mandatory reporting, immediate Group Chairman escalation

Scale: 20–50 branches · 200–2,000 welfare events/year · real-time Severity 3–4 alert system · monthly welfare digest to Chairman.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Welfare Events Coordinator | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group COO | G4 | View — Severity 3–4 events and escalation tracker | Read-only |
| Group Chairman / CEO | G5 / G4 | View — Severity 4 events and monthly digest | Not this URL |
| Branch Welfare Officer | G2 | View — own branch events, can log new events | Branch-scoped, not this URL |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('welfare_events_coordinator')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Welfare Events Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]               [Export Monthly Digest ↓]  [Settings ⚙]
[Group Name] — Group Welfare Events Coordinator · Last login: [date time]
AY [current academic year]  ·  [N] Branches  ·  [N] Open Events  ·  [N] Severity 3–4 Active
```

### 3.3 Alert Banner (conditional — critical items requiring immediate action)

| Condition | Banner Text | Severity |
|---|---|---|
| Active Severity 4 event | "CRITICAL: Severity 4 welfare event [ID] is active at [Branch]. Chairman and COO must be notified immediately. [View Event →]" | Red — persistent, cannot be dismissed until event is closed |
| Severity 3 event open > 7 days | "Severity 3 event [ID] at [Branch] has been open for [N] days, exceeding the 7-day investigation window." | Red |
| Severity 3 event not escalated within 2 hours | "Severity 3 event [ID] at [Branch] was not escalated to COO within the 2-hour window. Compliance breach." | Red |
| Severity 2 event open > 48 hours | "Severity 2 event [ID] at [Branch] has been open for [N] hours. Parent notification and counsellor involvement required." | Amber |
| Branch with zero events logged this month | "[Branch] has logged zero welfare events this month. Possible under-reporting — conduct review." | Amber |

Multiple Red alerts stack vertically. Severity 4 banner always appears first and cannot be collapsed. "View all welfare events → Event Audit Log" always shown below alerts.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open Severity 3–4 Events | Active Severity 3 or 4 events not yet resolved | Green = 0 · Red if any — highest priority card on dashboard | → Section 5.1 |
| All Open Events | Total active welfare events across all branches, all severities | Green = 0 · Yellow 1–20 · Red > 20 | → Section 5.2 |
| Events This Month | Total welfare events logged this calendar month, all branches | Blue always (informational) | → Section 5.2 |
| Severity 4 Events This Year | Cumulative count of Severity 4 events in current AY | Blue always — warrants review if > 0 | → Section 5.2 |
| Escalation Compliance % | Severity 3–4 events that were escalated within the 2-hour window / total Severity 3–4 | Green = 100% · Red if any breach | → Section 5.2 |
| Branches with Zero Events This Month | Branches that have logged no welfare events in current calendar month | Informational — Amber if any branch zero and month > 7 days in | → Section 5.2 |
| Events Resolved Within SLA % | Events closed within the severity-appropriate SLA (S1: same day / S2: 48h / S3: 7d) this AY | Green ≥ 90% · Yellow 70–89% · Red < 70% | → Section 5.2 |
| Average Resolution Time | Mean days from event logging to resolution closure, this AY, all severities | Green < 3 days · Yellow 3–7 days · Red > 7 days | → Section 5.4 |

**HTMX:** `hx-trigger="every 2m"` → Open Severity 3–4 Events and All Open Events auto-refresh.

---

## 5. Sections

### 5.1 Live Event Monitor

> Real-time view of all active Severity 3 and Severity 4 events requiring immediate coordinator attention. Refreshes every 2 minutes.

**Display:** Card-based layout — one card per active Severity 3/4 event, sorted by severity then time elapsed.

**Card content:**
- Severity badge (large — Orange for S3, Red for S4)
- Event ID · Branch · Date and time logged
- Event type / category
- Brief description (first 150 chars)
- Hours/days open · Escalation status (Escalated ✅ / Not Escalated ❌ with time since event)
- Persons affected count
- [View Full Event →] button

- Severity 4 cards have a pulsing red border
- "No active Severity 3–4 events" → shows green "All Clear" state

**Auto-refresh:** `hx-trigger="every 2m"` — new Severity 3/4 events appear immediately.

---

### 5.2 All Events Table

> Complete event list across all branches, all severities, with full filtering.

**Search:** Event ID, branch, event type, description keyword. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Severity | Checkbox | Severity 1 / 2 / 3 / 4 |
| Status | Checkbox | Open / Under Investigation / Resolved / Closed |
| SLA Status | Radio | All / Within SLA / Overdue |
| Escalation | Radio | All / Escalated / Not Escalated / Not Required |
| Date Range | Date picker | From / To |
| Event Type | Multi-select | Medical / Physical Conflict / Emotional / Abuse / Self-Harm / Accident / Natural Disaster / Other |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Event ID | ✅ | System-generated; link → `event-detail` drawer |
| Date & Time | ✅ | Logged date and time |
| Branch | ✅ | |
| Event Type | ✅ | Badge |
| Severity | ✅ | Colour-coded pill: S1 Grey · S2 Yellow · S3 Orange · S4 Red |
| Persons Affected | ✅ | Count |
| Status | ✅ | Open / Under Investigation / Resolved / Closed |
| Escalated | ✅ | ✅ Within Window / ⚠ Late / ❌ Not Done / — Not Required |
| SLA | ✅ | Within SLA ✅ / Overdue ❌ |
| Days Open | ✅ | Red if > SLA threshold for severity level |
| Actions | ❌ | View · Update · Escalate |

**Default sort:** Severity descending (S4 first), then Days Open descending.
**Pagination:** Server-side · 25/page.

---

### 5.3 Severity Distribution Chart

> Two charts: group-wide severity distribution (donut) and per-branch event count (heatmap-style bar).

**Chart 1 — Donut Chart (group-wide):**
- Segments: S1 (Grey) · S2 (Yellow) · S3 (Orange) · S4 (Red)
- Centre label: Total events this month
- Legend: S1: [N] events · S2: [N] events · S3: [N] events · S4: [N] events
- Click segment → filters Section 5.2 table to that severity

**Chart 2 — Horizontal Bar Chart (branch event counts):**
- X-axis: Event count this month
- Y-axis: Branch names (sorted by count descending)
- Bars colour-coded by most severe open event at that branch
- Tooltip: Branch · S1 count · S2 count · S3 count · S4 count · Total
- Click branch bar → `event-detail` drawer filtered to that branch; alternatively, branch row in Section 5.2

---

### 5.4 Monthly Trend

> Line chart showing welfare event volume by severity for the past 12 months.

**Chart type:** Multi-series line chart.

- X-axis: Last 12 months (abbreviated month-year)
- Y-axis: Event count (0 to max + 10% headroom)
- Series: S1 (Grey line) · S2 (Yellow line) · S3 (Orange line) · S4 (Red line, dashed)
- Tooltip: Month · S1 count · S2 count · S3 count · S4 count · Total
- Click month point → inline panel shows events for that month (summary count table)
- Trend annotation: Arrow icon if current month is up/down vs previous month by > 20%

---

### 5.5 Quick Actions

| Action | Target |
|---|---|
| Report Event | Opens `event-report` drawer (new event creation) |
| Export Monthly Digest | Download PDF/XLSX — all events for selected month with severity breakdown |
| View SLA Report | Download CSV — all events with SLA compliance status, current AY |
| Escalate to COO | Opens escalation confirmation for selected Severity 3/4 event |
| View Under-Reporting Branches | Navigates to Section 5.2 filtered: zero events, current month |

---

## 6. Drawers / Modals

### 6.1 Drawer: `event-detail`
- **Trigger:** Event ID link in Section 5.2 table or "View Full Event →" in Section 5.1 monitor
- **Width:** 680px
- **Tabs:** Event · Timeline · Escalation · Resolution · Related Events

**Event tab:**
| Field | Notes |
|---|---|
| Event ID | System-generated |
| Branch | |
| Date & Time Logged | |
| Severity | Colour badge (S1–S4) |
| Event Type | Category |
| Event Description | Full text |
| Location on Campus | |
| Persons Affected | Count and list (Name · Type: Student/Staff · Class/Role) |
| Immediate Action Taken | Documented response |
| Police / Hospital Involved | Yes/No; FIR number / hospital name if applicable |
| Logged By | Name · Role · Date/Time |
| Attachments | Files — view/download only |

**Timeline tab:**
- Chronological log: Date/Time · Event type (Logged / Escalated / Update Added / Status Changed / Resolved) · Actor · Note

**Escalation tab:**
- Required escalation (by severity): COO within 2h (S3/S4) / Chairman within 4h (S4)
- Actual escalation: ✅ Done at [time] by [name] / ❌ Not done (N/A for S1/S2)
- Escalation notes
- COO response / acknowledgment (if received)

**Resolution tab:**
- Resolution notes (editable by Coordinator)
- Root cause (select: Individual Behaviour / System / Environment / Medical / External / Unknown)
- Corrective action taken
- Preventive measure recommended
- Resolution date picker
- [Mark Resolved] button
- [Close Event] button (available only when resolution is complete)

**Related Events tab:**
- Other welfare events at the same branch in last 90 days: Event ID · Severity · Type · Date · Status
- Events involving the same persons (if applicable): Event ID · Date · Branch · Type

---

### 6.2 Drawer: `event-report`
- **Trigger:** "Report Event" quick action or "Log Incident" from branch
- **Width:** 600px
- **Mode:** Create new welfare event

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Select | Required |
| Event Date & Time | DateTime | Required; cannot be future |
| Severity | Radio | S1 / S2 / S3 / S4 — required; with severity guide tooltip |
| Event Type | Select | Medical / Physical Conflict / Emotional / Abuse / Self-Harm / Accident / Natural Disaster / Other |
| Event Description | Textarea | Required; min 100 chars |
| Location on Campus | Text | Required |
| Persons Affected Count | Number | Required; min 1 |
| Persons Affected (list) | Repeating row | Name · Type (Student/Staff) · Class/Role — add at least 1 |
| Immediate Action Taken | Textarea | Required; min 50 chars |
| Police Involved | Toggle | If Yes: FIR number appears |
| FIR Number | Text | Required if Police Involved = Yes |
| Hospital Involved | Toggle | If Yes: Hospital name + admission status |
| Hospital Name | Text | Required if Hospital Involved = Yes |
| NCPCR Reporting Required | Toggle | Auto-suggested for S4; user confirms |
| Attachments | File upload | Max 5 files · 10MB each |
| Escalation Status | Radio | Escalated to COO / Not Yet / Not Required — required for S3/S4 |

**Validation:** Branch, date/time, severity, type, description, location, immediate action, persons affected all required · FIR and hospital fields conditional · Escalation status mandatory for S3/S4.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event reported | "Welfare event [ID] (Severity [N]) logged at [Branch]." | Success | 4s |
| Severity 3/4 event escalated | "Event [ID] escalated to Group COO. Notification sent." | Warning | 6s |
| Severity 4 Chairman notified | "Group Chairman has been notified of Severity 4 event [ID] at [Branch]." | Warning | 8s |
| Event status updated | "Event [ID] status updated to [Status]." | Success | 4s |
| Event resolved | "Welfare event [ID] resolved and closed." | Success | 5s |
| Monthly digest exported | "Monthly welfare digest for [Month] export prepared. Download ready." | Info | 4s |
| SLA report exported | "SLA compliance report export prepared. Download ready." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No active Severity 3–4 events | "All Clear — No Critical Events" | "No Severity 3 or 4 welfare events are currently active." | — |
| No open events at all | "No Open Welfare Events" | "All welfare events across all branches are resolved or closed." | — |
| No events this month | "No Events Logged This Month" | "No welfare events have been logged for this month yet. Ensure branches are reporting." | [Report Event] |
| Search returns no results | "No Events Found" | "No welfare events match your current search or filters." | [Clear Filters] |
| No events in AY | "No Welfare Events Recorded This Year" | "No welfare events have been recorded for this academic year. Verify branch reporting is active." | [Report Event] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + S3/S4 monitor cards + all events table + donut chart + bar chart + line chart + alerts |
| S3/S4 monitor auto-refresh | Card skeleton (3 cards) — replaces section content while fetching |
| All events table filter/search | Inline skeleton rows (8 rows) |
| KPI auto-refresh | Shimmer on individual card values; labels preserved |
| Donut chart load | Circle skeleton with animated rotation |
| Branch bar chart load | Horizontal bar skeleton (10 rows) |
| Monthly trend chart load | Chart area skeleton with animated gradient |
| Event detail drawer open | 680px drawer skeleton; tabs load lazily |
| Event report drawer open | 600px form skeleton |

---

## 10. Role-Based UI Visibility

| Element | Welfare Events Coordinator G3 | Group COO G4 | Chairman / CEO G5 | Branch Welfare Officer G2 |
|---|---|---|---|---|
| View All Branches Events | ✅ | S3/S4 only | S4 only | Own branch only |
| Report New Event | ✅ | ❌ | ❌ | ✅ (own branch) |
| Update Event Status | ✅ | ❌ | ❌ | ✅ (own branch, S1/S2 only) |
| Escalate to COO | ✅ | ❌ | ❌ | ❌ |
| Escalate to Chairman | ✅ | ✅ | ❌ | ❌ |
| Mark Resolved | ✅ | ❌ | ❌ | ✅ (S1/S2 own branch) |
| Close Event | ✅ | ❌ | ❌ | ❌ |
| View Persons Affected List | ✅ | ✅ (S3/S4) | ✅ (S4) | Own branch only |
| Export Monthly Digest | ✅ | ✅ | ✅ | ❌ |
| Change Severity Classification | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/events/dashboard/` | JWT (G3+) | Full dashboard data payload |
| GET | `/api/v1/group/{group_id}/welfare/events/kpi-cards/` | JWT (G3+) | KPI auto-refresh values |
| GET | `/api/v1/group/{group_id}/welfare/events/live/` | JWT (G3+) | Active S3/S4 events for live monitor; refreshes every 2m |
| GET | `/api/v1/group/{group_id}/welfare/events/` | JWT (G3+) | All events list; params: `branch_id`, `severity`, `status`, `sla_status`, `escalated`, `type`, `from_date`, `to_date`, `page` |
| POST | `/api/v1/group/{group_id}/welfare/events/` | JWT (G3) | Report new welfare event |
| GET | `/api/v1/group/{group_id}/welfare/events/{event_id}/` | JWT (G3+) | Single event detail with all tabs data |
| PATCH | `/api/v1/group/{group_id}/welfare/events/{event_id}/` | JWT (G3) | Update event details or status |
| POST | `/api/v1/group/{group_id}/welfare/events/{event_id}/escalate/` | JWT (G3+) | Escalate to COO or Chairman; body: `level` (coo/chairman), `note` |
| POST | `/api/v1/group/{group_id}/welfare/events/{event_id}/resolve/` | JWT (G3) | Mark resolved; body: `resolution_notes`, `root_cause`, `corrective_action` |
| GET | `/api/v1/group/{group_id}/welfare/events/severity-distribution/` | JWT (G3+) | Donut chart and branch bar data |
| GET | `/api/v1/group/{group_id}/welfare/events/monthly-trend/` | JWT (G3+) | 12-month severity trend data |
| GET | `/api/v1/group/{group_id}/welfare/events/export/digest/` | JWT (G3+) | Async monthly digest export; params: `month`, `year`, `format` |
| GET | `/api/v1/group/{group_id}/welfare/events/export/sla-report/` | JWT (G3+) | Async SLA compliance report export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 2m` | GET `.../events/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| S3/S4 live monitor refresh | `every 2m` | GET `.../events/live/` | `#live-monitor-section` | `innerHTML` |
| All events table search | `input delay:300ms` | GET `.../events/?q={val}` | `#events-table-body` | `innerHTML` |
| All events filter | `click` | GET `.../events/?{filters}` | `#events-section` | `innerHTML` |
| All events pagination | `click` | GET `.../events/?page={n}` | `#events-section` | `innerHTML` |
| Open event detail drawer | `click` on event ID | GET `.../events/{id}/` | `#drawer-body` | `innerHTML` |
| Open event report drawer | `click` Report Event | GET `.../events/report-form/` | `#drawer-body` | `innerHTML` |
| Submit new event | `click` Save | POST `.../events/` | `#events-section` | `innerHTML` |
| Update event status | `click` Save | PATCH `.../events/{id}/` | `#event-row-{id}` | `outerHTML` |
| Escalate event | `click` Escalate | POST `.../events/{id}/escalate/` | `#event-row-{id}` | `outerHTML` |
| Severity chart load | `load` | GET `.../events/severity-distribution/` | `#severity-chart-section` | `innerHTML` |
| Monthly trend chart load | `load` | GET `.../events/monthly-trend/` | `#trend-chart-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
