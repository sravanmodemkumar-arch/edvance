# [18] — Affiliation Renewal Calendar

> **URL:** `/group/legal/affiliation-calendar/`
> **File:** `n-18-affiliation-renewal-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Compliance Manager (Role 109, G1) — visual calendar of all branch affiliation renewal deadlines

---

## 1. Purpose

The Affiliation Renewal Calendar provides a dedicated visual and timeline view of all branch affiliation renewal deadlines across the Institution Group — specifically focused on the calendar and scheduling dimension of affiliation compliance, complementing the Affiliation Compliance Tracker (N-02) which handles detailed per-affiliation records.

The calendar view helps the Compliance Manager plan the year: which months will be busy with renewal submissions, which branches need to start renewal 6 months in advance (CBSE renewal process takes 3–6 months), and where multiple branches have renewals clustered together. For large groups with 50 branches across CBSE, ICSE, and multiple state boards, renewal management requires advance planning to avoid simultaneous document collection bottlenecks.

The page offers three views: Monthly calendar (shows which branches have renewals due in each month), Timeline view (horizontal Gantt-style showing renewal periods), and Upcoming deadlines list (sorted by urgency). The Compliance Manager can print the calendar as PDF to share with the Chairman or Board.

Scale: 5–50 branches · 1 affiliation renewal per branch per cycle (annual or triennial) · 3–6 month lead time for CBSE renewals

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | |
| Group Compliance Manager | 109 | G1 | Full Read | Primary user |
| Group RTI Officer | 110 | G1 | Read — Limited (affiliation numbers for RTI) | |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | |
| Group POCSO Reporting Officer | 112 | G1 | No Access | |
| Group Data Privacy Officer | 113 | G1 | No Access | |
| Group Contract Administrator | 127 | G3 | No Access | |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Dispute-linked affiliations | |
| Group Insurance Coordinator | 129 | G1 | No Access | |

> **Access enforcement:** `@require_role(roles=[109,110,128], min_level=G1)`. G4/G5 full read.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Affiliation Renewal Calendar
```

### 3.2 Page Header
```
Affiliation Renewal Calendar                    [Export PDF]
Group Compliance Manager — [Name]
[Group Name] · [N] Renewals This Year · [N] Upcoming (Next 6 Months)
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Renewal expired (affiliation lapsed) | "[N] branch affiliation(s) have lapsed. Examination eligibility at risk." | Critical (red) |
| Renewal due within 30 days | "[N] affiliation renewal(s) due within 30 days." | High (amber) |
| Renewal process should have started (6 months before) | "[N] affiliations due for renewal require that renewal documents be submitted — start process now." | Medium (yellow) |

---

## 4. KPI Summary Bar (5 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Renewals Due This Month | Count | COUNT WHERE expiry within current month | Red > 0, Green = 0 | `#kpi-due-month` |
| 2 | Renewals Due (Next 3 Months) | Count | COUNT WHERE expiry within next 90 days | Amber > 3, Blue ≤ 3 | `#kpi-due-90d` |
| 3 | Renewals In Progress | Count | COUNT WHERE status = 'renewal_in_progress' | Blue | `#kpi-in-progress` |
| 4 | Renewals Completed (This FY) | Count | COUNT WHERE renewed_date within current FY | Green | `#kpi-completed` |
| 5 | Overdue (Lapsed) | Count | COUNT WHERE expiry < TODAY AND status = 'expired' | Red > 0, Green = 0 | `#kpi-lapsed` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/affiliation-calendar/kpis/"` with `hx-trigger="load"`.

---

## 5. Sections

### 5.1 Monthly Calendar View (Default View)

A full-year calendar grid (12 months). Each month cell contains colour-coded badges for branches with renewals due.

**Calendar cell content per month:**
- Month name
- Badges for each branch with renewal due that month: `[Branch Name] · [Board]` — colour: Red if lapsed, Amber if due, Green if renewed
- Count badge: "[N] branches"
- Click on any branch badge → opens affiliation detail drawer (same as N-02)

**Year selector:** Previous year / Current year / Next year navigation.

**Board filter:** Filter calendar to show only CBSE / ICSE / State Board / All.

---

### 5.2 Timeline View (Gantt-style)

Horizontal timeline showing each branch as a row. Bars indicate:
- Past renewal period (grey)
- Current valid period (green)
- Renewal window (amber — 3 months before expiry)
- Expired period (red)

Branches sorted by expiry date (soonest first).

Zoom levels: 6 months / 1 year / 2 years.

---

### 5.3 Upcoming Deadlines List

Sorted list of all upcoming renewals by date — same as a filtered version of N-02 but presented as a prioritised action list.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | |
| Board | Badge | Yes | |
| Expiry Date | Date | Yes | Red if past, amber if < 90d |
| Days to Expiry | Integer | Yes | Negative = expired |
| Renewal Status | Badge | Yes | Not Started / In Progress / Submitted / Renewed / Lapsed |
| Recommendation | Text | No | Auto-generated: e.g., "Start renewal process — 90 days remaining" |
| Actions | Button | No | [View Details →] |

**Default sort:** Days to Expiry ASC

---

## 6. Drawers & Modals

### 6.1 Drawer: `affiliation-detail` (680px)
Same drawer as in N-02 — opens full affiliation record with Overview, Documents, Renewal History, Deficiencies, and Timeline tabs.

### 6.2 Modal: `export-calendar-pdf` (480px)
- **Fields:** Year selector, Board filter, Include expired toggle, View (Monthly Calendar / Timeline / Upcoming List), Format (PDF / Excel / ICS — iCalendar)
- **ICS export:** Generates a `.ics` file with one VEVENT per affiliation renewal deadline; each event includes SUMMARY (branch + board), DTSTART (90 days before expiry — start renewal), DTEND (expiry date), DESCRIPTION (affiliation number + status), VALARM with 7-day and 30-day reminders; compatible with Google Calendar, Outlook, Apple Calendar
- **Buttons:** Cancel · Export

---

## 7. Charts

### 7.1 Renewal Distribution by Month — Bar Chart

| Property | Value |
|---|---|
| Chart type | Vertical bar (Chart.js 4.x) |
| Title | "Affiliation Renewals by Month — [Current Year]" |
| Data | Count of branches with affiliation expiry per month |
| X-axis | Month (Jan–Dec) |
| Y-axis | Branch count |
| Colour | Red = lapsed/expired, Amber = upcoming, Green = renewed |
| Tooltip | "[Month]: [N] renewals due ([N] completed, [N] pending, [N] lapsed)" |
| API endpoint | `GET /api/v1/group/{id}/legal/affiliation-calendar/monthly-distribution/` |
| HTMX | `hx-get` on load → `hx-target="#chart-monthly-dist"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Calendar year changed | "Showing affiliation renewals for [Year]." | Info | 2s |
| Filter applied | "Showing [Board] affiliations only." | Info | 2s |
| Export triggered | "Generating affiliation renewal calendar PDF…" | Info | 3s |
| Export ready | "Calendar PDF ready. Click to download." | Success | 6s |
| Lapsed alert | "[Branch] affiliation has lapsed — [Board]." | Error | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No affiliations configured | `calendar` | "No Affiliation Records" | "Configure branch affiliations to see the renewal calendar." | Go to Affiliation Tracker |
| No renewals this year | `check-circle` | "No Renewals This Year" | "No branch affiliations are due for renewal in the selected year." | View Next Year |
| Board filter returns no results | `search` | "No Branches Under This Board" | | Clear Filter |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 5 KPI + calendar grid shimmer |
| Calendar year change | Calendar shimmer while loading new year's data |
| Timeline view load | Horizontal bar skeleton for each branch row |
| Upcoming list load | Shimmer rows |
| Chart load | Grey canvas + spinner |
| Export generation | Progress toast |

---

## 11. Role-Based UI Visibility

| Element | Compliance Mgr (109) | RTI Officer (110) | Legal Dispute (128) | CEO/Chairman |
|---|---|---|---|---|
| Monthly calendar | Full view | Read-only (affiliation no. only) | Dispute-linked branches | Full view |
| Timeline view | Full | Not visible | Not visible | Full |
| Upcoming list | Full | Read-only | Dispute branches | Full |
| Export | Visible | Not visible | Not visible | Visible |
| Chart | Visible | Not visible | Not visible | Visible |
| Alert banners | All | Lapsed only | Lapsed only | All |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/affiliation-calendar/` | G1+ | All affiliations with expiry dates |
| GET | `/api/v1/group/{id}/legal/affiliation-calendar/monthly/` | G1+ | Calendar grid data by month |
| GET | `/api/v1/group/{id}/legal/affiliation-calendar/timeline/` | G1+ | Timeline/Gantt data |
| GET | `/api/v1/group/{id}/legal/affiliation-calendar/upcoming/` | G1+ | Upcoming renewals sorted list |
| GET | `/api/v1/group/{id}/legal/affiliation-calendar/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/legal/affiliation-calendar/monthly-distribution/` | G1+ | Bar chart data |
| POST | `/api/v1/group/{id}/legal/affiliation-calendar/export/` | G1+ | Export PDF/Excel/ICS |

### Query Parameters

| Parameter | Type | Description |
|---|---|---|
| `year` | integer | Calendar year (default: current) |
| `board` | string | cbse / icse / state_board / all |
| `view` | string | monthly / timeline / upcoming |
| `page` | integer | For upcoming list pagination |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | KPI container | GET `.../affiliation-calendar/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Calendar grid load | Calendar container | GET `.../affiliation-calendar/monthly/?year={y}` | `#calendar-grid` | `innerHTML` | `hx-trigger="load"` |
| Year navigation | Prev/Next year buttons | GET with `?year={n}` | `#calendar-grid` | `innerHTML` | `hx-trigger="click"` |
| Board filter | Board select | GET with `?board={v}` | `#calendar-grid` | `innerHTML` | `hx-trigger="change"` |
| Switch to timeline | Timeline tab | GET `.../affiliation-calendar/timeline/` | `#calendar-content` | `innerHTML` | `hx-trigger="click"` |
| Switch to upcoming | Upcoming tab | GET `.../affiliation-calendar/upcoming/` | `#calendar-content` | `innerHTML` | `hx-trigger="click"` |
| Open affiliation drawer | Branch badge click | GET `/api/v1/group/{id}/legal/affiliation/{aff_id}/` | `#right-drawer` | `innerHTML` | |
| Chart load | Chart container | GET `.../monthly-distribution/` | `#chart-monthly-dist` | `innerHTML` | `hx-trigger="load"` |

---

*Page spec version: 1.1 · Last updated: 2026-03-22*
