# [20] — Compliance Calendar & Unified Deadlines

> **URL:** `/group/legal/compliance-calendar/`
> **File:** `n-20-compliance-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Compliance Manager (Role 109, G1) — master deadline calendar aggregating all compliance obligations group-wide

---

## 1. Purpose

The Compliance Calendar & Unified Deadlines page is the master scheduling view for the entire Division N compliance function. It aggregates every deadline from every sub-module — affiliation renewals (N-02), RTI response deadlines (N-03), regulatory filing due dates (N-04), POCSO NCPCR reporting windows (N-05), DPDP breach notification windows (N-06), staff contract expiries (N-07), vendor agreement expiries (N-10), inspection deficiency response deadlines (N-11), consent withdrawal deadlines (N-12), insurance policy expiries (N-13), statutory return due dates (N-14), and policy review dates (N-15) — into a single, unified calendar.

The Group Compliance Manager uses this as the daily operational calendar: what is due today, what is due this week, what is overdue. The RTI Officer, DPO, POCSO Officer, and other roles each see a filtered view showing only deadlines relevant to their function. The Chairman/CEO sees a high-level summary.

Deadlines can be viewed in three modes: (1) Monthly calendar grid with colour-coded event badges; (2) Upcoming list view sorted by urgency; (3) Overdue items list — the most critical view. The calendar supports ICS export (iCalendar format) for import into Google Calendar, Outlook, or any calendar application, enabling role-based automated reminders.

Scale: 5–50 branches · 200–2,000 compliance deadline events per year group-wide · Aggregated from 15+ source modules

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | |
| Group Compliance Manager | 109 | G1 | Full Calendar — All Deadline Types | Primary user |
| Group RTI Officer | 110 | G1 | RTI deadlines only | Filtered view |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | |
| Group POCSO Reporting Officer | 112 | G1 | POCSO deadlines only | Filtered view |
| Group Data Privacy Officer | 113 | G1 | DPDP/Consent deadlines only | Filtered view |
| Group Contract Administrator | 127 | G3 | Contracts/Vendor expiry deadlines | Filtered view |
| Group Legal Dispute Coordinator | 128 | G1 | Litigation response/hearing deadlines | Filtered view |
| Group Insurance Coordinator | 129 | G1 | Insurance renewal deadlines | Filtered view |

> **Access enforcement:** `@require_role(min_level=G1, division='N')` with deadline_type scoping per role. G4/G5 full calendar.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Compliance Calendar
```

### 3.2 Page Header
```
Compliance Calendar                             [Export ICS]  [Export PDF]
Group Compliance Manager — [Name]
[Group Name] · [N] Items Due This Week · [N] Overdue · Today: [date]
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any critical deadline today | "CRITICAL: [N] compliance deadline(s) are due TODAY." | Critical (red, sticky) |
| Any POCSO/DPDP 24h/72h deadline active | "Active statutory notification window: [type] — [X] hours remaining." | Critical (red, sticky) |
| Overdue items > 5 | "[N] compliance deadline(s) are overdue across [N] branches." | High (amber) |
| Items due this week > 10 | "[N] compliance items due this week. Review the calendar." | Medium (yellow) |

---

## 4. KPI Summary Bar (8 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Overdue Items | Count | COUNT WHERE due_date < TODAY AND status != completed | Red > 0, Green = 0 | `#kpi-overdue` |
| 2 | Due Today | Count | COUNT WHERE due_date = TODAY | Red > 0, Green = 0 | `#kpi-due-today` |
| 3 | Due This Week | Count | COUNT WHERE due_date BETWEEN TODAY AND TODAY+7 | Amber > 5, Blue ≤ 5 | `#kpi-due-week` |
| 4 | Due This Month | Count | COUNT WHERE due_date within current month AND status != completed | Blue | `#kpi-due-month` |
| 5 | Completed On Time (This Month) | Count | COUNT WHERE completed_date <= due_date within current month | Green | `#kpi-completed-month` |
| 6 | Compliance Score (Timeliness) | % | on_time_completions / total_due × 100 (rolling 90 days) | Green ≥ 90%, Amber 70–89%, Red < 70% | `#kpi-timeliness` |
| 7 | Active Critical Windows | Count | POCSO 24h + DPDP 72h windows currently open | Red > 0, Green = 0 | `#kpi-critical-windows` |
| 8 | Next Upcoming (Days) | Integer | Days until next compliance deadline | Green > 7, Amber 3–7, Red ≤ 3 | `#kpi-next-deadline` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/compliance-calendar/kpis/"` with `hx-trigger="load, every 60s"` (1-minute refresh for this critical page).

---

## 5. Sections

### 5.1 Monthly Calendar View (Default)

A full-month grid calendar. Each day cell contains event badges for compliance deadlines.

**Event badge format:** `[Category icon] [Branch/Entity] · [Deadline type]`

**Event colour coding:**
- 🔴 Red: Overdue + POCSO/DPDP critical (today and past)
- 🟠 Orange: Due today
- 🟡 Amber: Due in 1–7 days
- 🔵 Blue: Due in 8–30 days
- 🟢 Green: Completed/submitted

**Month navigation:** Prev/Next month buttons. "Today" button returns to current month.

**Category toggle filters** (above calendar):
`[Affiliation]` `[RTI]` `[POCSO]` `[DPDP]` `[Contracts]` `[Filings]` `[Insurance]` `[Returns]` `[Inspections]` `[Policies]` — each toggleable on/off. Active filters persist in URL.

**Branch filter:** Show all branches or filter to specific branch.

**Clicking an event badge:** Opens mini-detail drawer for that specific deadline.

---

### 5.2 Upcoming Deadlines List View

Scrollable list of all upcoming compliance deadlines sorted by due date.

**Search:** Deadline type, branch, source module. Debounced 350ms.

**Filters:**
- Deadline Type: `All` + individual types (Affiliation / RTI / POCSO / DPDP / Contract / Filing / Insurance / Return / Inspection / Policy)
- Time Window: `Today` · `This Week` · `Next 14 Days` · `Next 30 Days` · `Next 90 Days`
- Branch: dropdown
- Status: `All` · `Pending` · `Completed` · `Overdue`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Due Date | Date + Time (if applicable) | Yes | Red = today/overdue, amber < 7d |
| Days Left | Badge | Yes | Negative = overdue |
| Deadline Type | Badge + icon | Yes | Colour by category |
| Description | Text | Yes | e.g., "Staff contract expiry — Physics Teacher, Branch XYZ" |
| Branch / Entity | Text | Yes | |
| Source Module | Link | No | "→ N-07 Staff Contracts" |
| Status | Badge | Yes | Pending / Completed / Overdue |
| Actions | Button | No | [View] (opens source module record) |

**Default sort:** Due Date ASC (most urgent first)
**Pagination:** Server-side · Default 50/page

---

### 5.3 Overdue Items List (Priority Tab)

Same columns as Upcoming List but filtered to status = Overdue only. This is the most action-oriented tab — everything here needs immediate attention.

**Sorted by:** Days Overdue DESC (longest overdue first)

**Each row has:** Deadline type badge · Description · Branch · Days Overdue (red badge) · Source Module link

**Batch action:** Select multiple items → "Send Reminder to Responsible Officers" (Role 109, G4+)

---

## 6. Drawers & Modals

### 6.1 Drawer: `deadline-detail` (560px, right-slide)
Mini-drawer opening when clicking any calendar event or list row.

- **Header:** Category badge + Deadline date
- **Body:**
  - Deadline type, Description, Branch, Responsible role
  - Due date + days remaining (or days overdue)
  - Current status
  - Regulatory basis (e.g., "RTI Act 2005 s.7(1) — 30 day response window")
  - Source module with link button
- **Footer:** "Open in [Module Name] →" button

### 6.2 Modal: `export-ics` (480px)
Export compliance deadlines as ICS calendar file (importable to Google Calendar, Outlook).

| Field | Type | Notes |
|---|---|---|
| Date Range | Date range picker | Default: next 6 months |
| Deadline Types | Multi-checkbox | All selected by default |
| Branch Filter | Select | All or specific |
| Include Overdue | Toggle | Yes/No |

**Footer:** Cancel · Export ICS
**ICS format:** Each deadline becomes a calendar event with: title = deadline description, date = due date, reminder = 7 days before, category = compliance type, location = branch name.

### 6.3 Modal: `export-calendar-pdf` (480px)
Export calendar as PDF — monthly view or list view.

| Field | Type | Notes |
|---|---|---|
| View | Select | Monthly Grid / Upcoming List / Overdue Only |
| Date Range | Date range picker | |
| Deadline Types | Multi-checkbox | |
| Format | Fixed PDF | |

**Footer:** Cancel · Export PDF

### 6.4 Modal: `send-reminders` (520px)
Batch send compliance reminders to responsible officers.

| Field | Type | Notes |
|---|---|---|
| Selected Items | Display | Pre-filled from selection |
| Reminder Method | Select | Platform notification / WhatsApp / Email |
| Message | Textarea | Template pre-filled with item details |
| CC | Text | Optional: CC to Compliance Manager |

**Footer:** Cancel · Send Reminders

---

## 7. Charts

### 7.1 Compliance Deadline Trend — Monthly Bar Chart

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Compliance Deadlines — Completed vs Overdue (Last 6 Months)" |
| Data | Per month: count completed on time vs overdue |
| X-axis | Month |
| Y-axis | Count |
| Colour | On-time = `#22C55E`, Overdue = `#EF4444` |
| Tooltip | "[Month]: [N] on time · [N] overdue" |
| API endpoint | `GET /api/v1/group/{id}/legal/compliance-calendar/monthly-trend/` |
| HTMX | `hx-get` on load → `hx-target="#chart-monthly-trend"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Deadlines by Type — Donut (Upcoming 30 Days)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Upcoming Deadlines by Type — Next 30 Days" |
| Data | Count per deadline type in next 30 days |
| Colour | Each type a distinct colour (matching category colours) |
| Tooltip | "[Type]: [N] deadlines due in next 30 days" |
| API endpoint | `GET /api/v1/group/{id}/legal/compliance-calendar/deadlines-by-type/?window=30` |
| HTMX | `hx-get` on load → `hx-target="#chart-by-type"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Calendar loaded | "Compliance calendar loaded — [N] items in view." | Info | 2s |
| Deadline today alert | "CRITICAL: [N] compliance deadline(s) due TODAY." | Error | Sticky (dismiss required) |
| ICS export ready | "Calendar ICS file ready. Import to your calendar app." | Success | 8s |
| PDF export triggered | "Generating compliance calendar PDF…" | Info | 3s |
| PDF export ready | "Calendar PDF ready. Click to download." | Success | 6s |
| Reminders sent | "Compliance reminders sent to [N] responsible officers." | Success | 4s |
| Month navigation | "Showing [Month Year] — [N] compliance deadlines." | Info | 2s |
| Auto-refresh | "Calendar refreshed." | Info | 2s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| Calendar month has no deadlines | `calendar-check` | "Clear Month" | "No compliance deadlines in [Month Year]." | — |
| No overdue items | `check-circle` | "No Overdue Items" | "All compliance deadlines are on track." | View Upcoming |
| Filter returns no results | `search` | "No Matching Deadlines" | "No compliance items match the selected filters." | Clear Filters |
| No items in next 30 days | `calendar` | "Clean Calendar Ahead" | "No compliance deadlines in the next 30 days." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 8 KPI shimmer cards + calendar grid shimmer |
| Calendar month change | Month grid shimmer while loading new data |
| Upcoming list load | 10-row shimmer skeleton |
| Overdue tab switch | 5-row shimmer skeleton |
| KPI auto-refresh (every 60s) | Shimmer pulse on card values only |
| Charts | Grey canvas + centred spinner per chart |
| Deadline detail drawer | Slide-in skeleton |
| Export operations | Toast with "Generating…" indicator |
| Bulk reminder send | Button spinner + disabled state |

---

## 11. Role-Based UI Visibility

| Element | Compliance Mgr (109) | RTI Officer (110) | POCSO Officer (112) | DPO (113) | Contract Admin (127) | CEO/Chairman |
|---|---|---|---|---|---|---|
| Full calendar (all types) | Visible | RTI events only | POCSO events only | DPDP events only | Contract events only | Full |
| Category toggle filters | All visible + toggleable | RTI only | POCSO only | DPDP only | Contracts only | All |
| Upcoming list (all types) | Full | RTI items | POCSO items | DPDP items | Contract items | Full |
| Overdue list | Full | RTI overdue | POCSO overdue | DPDP overdue | Contract overdue | Full |
| [Send Reminders] button | Visible | Not visible | Not visible | Not visible | Not visible | Visible |
| [Export ICS] | Visible (all types) | Visible (RTI only) | Visible (POCSO only) | Visible (DPDP only) | Visible (contracts) | Visible |
| [Export PDF] | Visible | Visible | Visible | Visible | Visible | Visible |
| Both charts | Full | Not visible | Not visible | Not visible | Not visible | Full |
| Critical window alerts | All | POCSO if relevant | POCSO always | DPDP always | Not visible | All |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/compliance-calendar/` | G1+ (type-scoped) | All calendar events (paginated) |
| GET | `/api/v1/group/{id}/legal/compliance-calendar/monthly/` | G1+ | Events for a specific month (calendar grid) |
| GET | `/api/v1/group/{id}/legal/compliance-calendar/upcoming/` | G1+ | Upcoming deadlines list |
| GET | `/api/v1/group/{id}/legal/compliance-calendar/overdue/` | G1+ | Overdue items list |
| GET | `/api/v1/group/{id}/legal/compliance-calendar/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/legal/compliance-calendar/monthly-trend/` | G1+ | Trend chart data |
| GET | `/api/v1/group/{id}/legal/compliance-calendar/deadlines-by-type/` | G1+ | Donut chart data |
| POST | `/api/v1/group/{id}/legal/compliance-calendar/export-ics/` | G1+ | Generate ICS file |
| POST | `/api/v1/group/{id}/legal/compliance-calendar/export-pdf/` | G1+ | Generate PDF |
| POST | `/api/v1/group/{id}/legal/compliance-calendar/send-reminders/` | Role 109, G4+ | Batch send reminders |
| GET | `/api/v1/group/{id}/legal/compliance-calendar/{event_id}/` | G1+ | Single deadline event detail |

### Query Parameters for Calendar Events

| Parameter | Type | Description |
|---|---|---|
| `deadline_type` | string (multi) | affiliation / rti / pocso / dpdp / contracts / filings / insurance / returns / inspections / policies / litigation |
| `branch_id` | integer | Filter to specific branch |
| `status` | string | pending / completed / overdue |
| `month` | string | YYYY-MM — for monthly calendar view |
| `window_days` | integer | For upcoming list: days ahead (default 30, max 365) |
| `q` | string | Search description, branch |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 / 50 / 100; default 50 |
| `sort` | string | due_date / deadline_type / branch |
| `order` | string | asc / desc |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + auto-refresh | `<div id="kpi-bar">` | GET `.../compliance-calendar/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 60s"` (60s interval) |
| Calendar month load | Calendar container | GET `.../compliance-calendar/monthly/?month={YYYY-MM}` | `#calendar-grid` | `innerHTML` | `hx-trigger="load"` |
| Month navigation | Prev/Next buttons | GET `.../compliance-calendar/monthly/?month={prev/next}` | `#calendar-grid` | `innerHTML` | `hx-trigger="click"` |
| Category toggle | Category toggle chips | GET `.../compliance-calendar/monthly/?types={active_types}` | `#calendar-grid` | `innerHTML` | `hx-trigger="click"` |
| Branch filter | Branch dropdown | GET `.../compliance-calendar/monthly/?branch_id={id}` | `#calendar-grid` | `innerHTML` | `hx-trigger="change"` |
| Upcoming list load | `<div id="upcoming-list">` | GET `.../compliance-calendar/upcoming/?window_days=30` | `#upcoming-list` | `innerHTML` | `hx-trigger="load"` |
| Upcoming search | Search input | GET `.../upcoming/?q={v}` | `#upcoming-list` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| Upcoming time filter | Time window chips | GET `.../upcoming/?window_days={N}` | `#upcoming-list` | `innerHTML` | `hx-trigger="click"` |
| Switch to overdue tab | Overdue tab click | GET `.../compliance-calendar/overdue/` | `#calendar-list-content` | `innerHTML` | `hx-trigger="click"` |
| Deadline detail drawer | Event badge / row click | GET `.../compliance-calendar/{event_id}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Export ICS modal | [Export ICS] button | GET `/htmx/legal/compliance-calendar/ics-form/` | `#modal-container` | `innerHTML` | Opens modal |
| Submit ICS export | ICS form | POST `.../export-ics/` | `#export-toast` | `innerHTML` | File download triggered |
| Send reminders modal | [Send Reminders] | GET `/htmx/legal/compliance-calendar/remind-form/` | `#modal-container` | `innerHTML` | Pre-fills selected items |
| Submit reminders | Reminder form | POST `.../send-reminders/` | `#remind-toast` | `innerHTML` | Toast confirmation |
| Charts load | Both chart containers | GET chart endpoints | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination controls | GET with `?page={n}` | `#upcoming-list` | `innerHTML` | Replaces list only |

---

## 14. Cross-Module Integration Notes

This page is a **read-only aggregation layer** — it pulls deadline data from:

| Source Module | Deadline Types Pulled |
|---|---|
| N-02 Affiliation Tracker | Affiliation expiry dates; renewal milestones |
| N-03 RTI Manager | RTI response deadlines; appeal deadlines |
| N-04 Regulatory Filings | Filing due dates (AISHE, UDISE+, etc.) |
| N-05 POCSO Registry | 24h NCPCR reporting windows for open incidents |
| N-06 Data Privacy | 72h CERT-In/DPB breach notification windows; DSR 30-day deadlines |
| N-07 Staff Contracts | Contract expiry dates (60-day lead time) |
| N-09 Litigation Register | Court hearing dates; response filing deadlines |
| N-10 Vendor Agreements | Vendor contract expiry dates (60-day lead time) |
| N-11 Inspection Tracker | Deficiency response deadlines; follow-up inspection dates |
| N-12 Consent Management | Consent withdrawal 30-day deadlines |
| N-13 Insurance Registry | Policy expiry dates (60-day lead time) |
| N-14 Statutory Returns | All annual/monthly/quarterly statutory return due dates |
| N-15 Policy Repository | Policy review due dates |

All deadline data is pulled via the unified `ComplianceDeadline` model which is populated by background tasks from each sub-module. No direct writes to deadlines are made from this page — all updates happen in the source module.

**Background tasks:**
- `sync_compliance_deadlines`: Celery task running every 15 minutes — reads all source modules and updates the `ComplianceDeadline` table.
- `send_deadline_reminders`: Celery Beat task running daily at 08:00 IST — sends automatic reminders for deadlines due within 7 days.
- `mark_overdue_deadlines`: Celery Beat task running hourly — marks deadlines as overdue when `due_date < now`.

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
