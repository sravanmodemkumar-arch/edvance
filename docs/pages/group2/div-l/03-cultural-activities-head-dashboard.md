# 03 — Cultural Activities Head Dashboard

> **URL:** `/group/cultural/head/`
> **File:** `03-cultural-activities-head-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Cultural Activities Head (Role 99, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Cultural Activities Head. Owns all group-wide cultural programming — Annual Day events, inter-branch debate and quiz competitions, fine arts (painting, rangoli, craft), performing arts (music, dance, drama), and literary events (essay, elocution). Ensures every branch participates in group-level cultural events and that competition results are recorded, certificates generated, and toppers recognized.

Core responsibilities:
- Plan and coordinate Annual Day across all branches (largest single event)
- Organize inter-branch competitions (debate, quiz, cultural arts)
- Track branch-wise participation and award ceremony logistics
- Register students for external competitions (Youth Parliament, Kalolsavam, State Youth Festival)

Scale: 20–50 branches · 15–40 cultural events per year · 2,000–20,000 student participants.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Cultural Activities Head | 99 | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group Sports Director | 97 | G3 | View cultural calendar only | No write access |
| Group NSS/NCC Coordinator | 100 | G3 | View shared events calendar | No write access |
| Group Chairman / CEO | — | G5 / G4 | View via Governance Reports | Not this URL |
| All others | — | — | — | Redirected |

> **Access enforcement:** `@require_role('cultural_activities_head')` on all views and API endpoints.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Cultural Activities Head Dashboard
```

### 3.2 Page Header
```
Welcome back, [Head Name]                    [+ New Event]  [Export Cultural Report ↓]
[Group Name] — Cultural Activities Head · Last login: [date time]
AY [current academic year]  ·  [N] Events Planned  ·  [N] Branches Participating  ·  [N] Students Registered
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with zero cultural participation this term | "[N] branch(es) have no cultural event participation this term." | Red |
| Annual Day not scheduled | "Annual Day for AY [year] has not been scheduled yet. Recommended by February." | Amber |
| Competition result entry overdue | "[N] completed competition(s) have no results entered yet." | Amber |
| External registration deadline approaching | "External competition [Name] registration closes in [N] days — [N] students not yet registered." | Amber |

---

## 4. KPI Summary Bar (7 cards)

All metrics reflect the currently selected Academic Year filter (default: current AY). Each card is HTMX-loaded independently on page load using `hx-trigger="load"`.

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Events Planned This AY | Total cultural events created for current academic year | `CulturalEvent.objects.filter(ay=current_ay).count()` | Blue always | `#kpi-events-planned` |
| 2 | Branches Participating | Branches with at least one event participation this term | `Branch.objects.filter(cultural_participations__ay=current_ay).distinct().count()` | Green = all · Yellow = 1–3 missing · Red = 4+ missing | `#kpi-branches-participating` |
| 3 | Total Student Participants | Students registered for at least one cultural event this AY | `CulturalParticipant.objects.filter(ay=current_ay).values('student').distinct().count()` | Blue always | `#kpi-total-participants` |
| 4 | Events This Month | Events scheduled in current calendar month | `CulturalEvent.objects.filter(ay=current_ay, date__month=today.month).count()` | Blue always | `#kpi-events-month` |
| 5 | Competitions Pending Results | Completed competitions with no results entered | `CulturalEvent.objects.filter(ay=current_ay, status='completed', results_entered=False).count()` | Green = 0 · Red > 0 | `#kpi-pending-results` |
| 6 | Annual Day Status | "Scheduled [date]" or "Not Scheduled" | `AnnualDay.objects.filter(ay=current_ay).first()` — checks `date` field | Green if scheduled · Red if not & within 60 days of AY end | `#kpi-annual-day` |
| 7 | External Competition Registrations | Students registered for external events this AY | `CulturalParticipant.objects.filter(ay=current_ay, event__is_external=True).values('student').distinct().count()` | Blue always | `#kpi-external-reg` |

**HTMX:** Each card uses `hx-get` to a dedicated sub-endpoint with `hx-trigger="load"` and shows a skeleton while loading. AY selector change triggers all KPI cards to refresh via `hx-swap-oob="true"`.

Auto-refresh: `hx-trigger="every 5m"` `hx-get="/api/v1/group/{id}/cultural/head/kpi/"` `hx-target="#kpi-bar"` `hx-swap="innerHTML"`.

---

## 5. Sections

### 5.1 Upcoming Events — Action Required

> Events in the next 30 days requiring Cultural Head attention.

**Display:** Card list (max 6) — sorted by date ascending.

**Card fields:**
- Event name · Type badge (Annual Day / Debate / Quiz / Fine Arts / Music / Dance / Drama / External)
- Date · Venue · Participating branches count
- Status badge: Planning · Registration Open · Registration Closed · Ready
- Action required indicator: e.g. "Results not entered", "Venue not confirmed", "Registration closing in 3 days"
- [View Details] link

---

### 5.2 Branch Participation Status

> Which branches are active in cultural events this term.

**Search:** Branch name, city. Debounce 300ms.

**Filters:** State, Type, Participation Status.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text + link | ✅ | |
| City | Text | ✅ | |
| Events Participated | Number | ✅ | This term. Green ≥ 3 · Yellow 1–2 · Red = 0 |
| Students Registered | Number | ✅ | |
| Last Event | Date | ✅ | Red if > 90 days ago |
| Annual Day? | Badge | ✅ | Scheduled / Not Scheduled |
| Actions | — | ❌ | View Events |

**Default sort:** Events Participated ascending (least active branches first).

**Pagination:** 25/page.

---

### 5.3 Competition Results Pending

> Competitions that are completed but results not yet entered.

**Display:** Table — max 8 rows, "View All →" to page 12.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Competition Name | Text | ✅ | |
| Type | Badge | ✅ | Debate · Quiz · Arts · Music · Dance · Drama |
| Date Held | Date | ✅ | |
| Branches Participated | Number | ✅ | |
| Days Since Event | Number | ✅ | Red if > 7 |
| Actions | — | ❌ | [Enter Results] [View] |

**[Enter Results]:** Opens `competition-result-entry` drawer.

---

### 5.4 Annual Day Planning Tracker (current AY)

> Consolidated status of Annual Day planning across all branches.

**Display:** Table — one row per branch.

**Filters:** Scheduled / Not Scheduled toggle (default: All).

**Default sort:** Annual Day Date ascending (earliest scheduled branch first); "Not set" entries sorted to the bottom.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| Annual Day Date | Date | ✅ | "Not set" if blank — shown in red |
| Venue | Text | ❌ | |
| Chief Guest | Text | ❌ | "Not confirmed" if blank |
| Programme Finalized | Badge | ✅ | ✅ Yes · ❌ No |
| Invitations Sent | Badge | ✅ | ✅ Yes · ❌ No |
| Actions | — | ❌ | [Edit Annual Day] [View] |

**[Edit Annual Day]:** Opens the `cultural-event-create` drawer pre-filled with the selected branch's Annual Day record. All existing fields are populated; edits update the existing record (not create a new one).

---

## 6. Drawers & Modals

### 6.1 Drawer: `cultural-event-create`
- **Trigger:** [+ New Event] header button, or [Edit Annual Day] in section 5.4 (pre-filled mode)
- **Width:** 680px
- **Tabs:** Details · Participants · Schedule · Venue

#### Tab: Details
| Field | Type | Required | Validation |
|---|---|---|---|
| Event Name | Text | ✅ | Min 3, max 150 chars |
| Event Type | Select | ✅ | Annual Day · Debate · Quiz · Fine Arts · Music · Dance · Drama · Literary · External |
| Academic Year | Select | ✅ | Current AY default |
| Description | Textarea | ❌ | Max 500 chars |
| Is Inter-Branch? | Toggle | ✅ | On = competition between branches |
| Is External Participation? | Toggle | ❌ | On = external event (state/national) |

#### Tab: Participants
| Field | Type | Required | Validation |
|---|---|---|---|
| Participating Branches | Multi-select | ✅ | At least 1 |
| Registration Deadline | Date | Conditional | Required if Is Inter-Branch |
| Max Participants per Branch | Number | ❌ | Limit per branch |
| Category | Multi-select | ❌ | Junior (Class 6–8) · Senior (Class 9–12) |

#### Tab: Schedule
| Field | Type | Required | Validation |
|---|---|---|---|
| Event Date | Date | ✅ | |
| Start Time | Time | ❌ | |
| Duration | Text | ❌ | e.g. "Full day" / "3 hours" |
| Reporting Time | Time | ❌ | When participants should arrive |

#### Tab: Venue
| Field | Type | Required | Validation |
|---|---|---|---|
| Venue Name | Text | ✅ | |
| Branch (if at branch) | Select | ❌ | |
| Address | Textarea | ❌ | |
| Capacity | Number | ❌ | |
| Venue Confirmed | Toggle | ❌ | Default off |

**Submit:** "Create Event" (new mode) / "Save Changes" (edit mode) — disabled until Details + Participants tabs valid.

### 6.2 Drawer: `competition-result-entry`
- **Width:** 560px
- **Tabs:** Results · Positions · Certificates
- **Results tab:** Table — Branch · Participant name · Category · Score/Marks (if applicable) · Position (1st/2nd/3rd/Participation) · Notes
- **Positions tab:** Overall winner · First runner-up · Second runner-up · Best performance award
- **Certificates tab:** Generate certificate toggle · Certificate type (Winner/Runner-up/Participation) · [Generate & Download All] button

---

## 7. Charts

All charts use Chart.js 4.x, are fully responsive, use a colorblind-safe palette, include legend and tooltip with exact numbers, and each has a PNG export button (top-right corner of each chart card).

### 7.1 Cultural Participation by Event Type (current AY)

| Property | Value |
|---|---|
| Chart type | Donut |
| Title | "Cultural Participation by Event Type — [Selected AY]" |
| Data | Student participation count by event type |
| Segments | Annual Day · Debate · Quiz · Fine Arts · Music · Dance · Drama · External |
| Centre text | Total participants |
| Tooltip | "[Type]: [N] students ([X]%)" |
| Empty state | "No participation data for the selected period." |
| API endpoint | `GET /api/v1/group/{id}/cultural/analytics/type-distribution/` |
| HTMX | `hx-get="/api/v1/group/{id}/cultural/analytics/type-distribution/"` `hx-trigger="load"` `hx-target="#chart-type-distribution"` `hx-swap="innerHTML"` |
| Export | PNG button top-right of chart card |

### 7.2 Branch Cultural Participation Trend (last 3 AY)

| Property | Value |
|---|---|
| Chart type | Grouped bar chart |
| Title | "Branch Cultural Participation Trend — Last 3 Academic Years" |
| Data | Events participated per AY per branch (top 10 most active) |
| X-axis | Academic years |
| Y-axis | Event count |
| Tooltip | "[Branch] · [AY] · Events: [N]" |
| Empty state | "No trend data available for the selected period." |
| API endpoint | `GET /api/v1/group/{id}/cultural/analytics/participation-trend/` |
| HTMX | `hx-get="/api/v1/group/{id}/cultural/analytics/participation-trend/"` `hx-trigger="load"` `hx-target="#chart-participation-trend"` `hx-swap="innerHTML"` |
| Export | PNG button top-right of chart card |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event created | "Cultural event [Name] created. Branches notified." | Success | 4s |
| Results entered | "Competition results saved for [Event Name]." | Success | 4s |
| Certificates generated | "[N] certificates generated and ready for download." | Success | 4s |
| Annual Day plan saved | "Annual Day details for [Branch] saved successfully." | Success | 4s |
| Export started | "Cultural report generating…" | Info | 4s |
| Validation error | "Please complete all required fields before saving." | Error | Manual |
| Certificate generation failed | "Certificate generation failed. Please try again or contact support." | Error | Manual |
| API error | "Failed to load data. Refresh the page." | Error | Manual |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No events this AY | 🗓 | "No cultural events planned" | "Create your first event for this academic year" | [+ New Event] |
| No competitions pending results | ✅ | "All results entered" | "Every completed competition has results recorded" | — |
| No external registrations | 🏆 | "No external event registrations" | "Register students for state/national cultural competitions" | [Go to Competition Tracker] |
| No branches in annual day tracker | 📋 | "No branches found" | "No branches match the current filter selection" | [Clear Filters] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 7 KPI cards + event cards (4) + branch table (5 rows) + charts |
| Branch table search/filter | Inline skeleton rows |
| Event create drawer open | Spinner in drawer |
| Edit Annual Day drawer open | Spinner in drawer while pre-filling fields from API |
| Result entry submit | Spinner in submit button + drawer blocked until response |
| Certificate generation | Full-page overlay "Generating [N] certificates…" with progress indicator; all other UI blocked |
| KPI auto-refresh | Shimmer on card values |

---

## 11. Role-Based UI Visibility

| Element | Cultural Head G3 | Sports Dir / NSS Coord G3 | Others |
|---|---|---|---|
| Page | ✅ | ❌ redirect | ❌ redirect |
| [+ New Event] header button | ✅ | ❌ | ❌ |
| [Enter Results] on pending table | ✅ | ❌ | ❌ |
| [Edit Annual Day] action | ✅ | ❌ | ❌ |
| [Export Cultural Report] | ✅ | ❌ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/cultural/head/dashboard/` | JWT (G3 Cultural) | Full dashboard |
| GET | `/api/v1/group/{id}/cultural/head/kpi/` | JWT (G3) | KPI bar data (all 7 cards) |
| GET | `/api/v1/group/{id}/cultural/head/kpi/{slug}/` | JWT (G3) | Individual KPI card data |
| GET | `/api/v1/group/{id}/cultural/events/?upcoming=true&days=30` | JWT (G3) | Upcoming events |
| GET | `/api/v1/group/{id}/cultural/branches/participation/` | JWT (G3) | Branch participation status |
| GET | `/api/v1/group/{id}/cultural/competitions/?results_pending=true` | JWT (G3) | Competitions without results |
| GET | `/api/v1/group/{id}/cultural/annual-day/status/` | JWT (G3) | Annual Day planning per branch |
| POST | `/api/v1/group/{id}/cultural/events/` | JWT (G3) | Create cultural event |
| PATCH | `/api/v1/group/{id}/cultural/events/{eid}/` | JWT (G3) | Edit existing event (Annual Day pre-fill edit) |
| POST | `/api/v1/group/{id}/cultural/competitions/{cid}/results/` | JWT (G3) | Submit competition results |
| POST | `/api/v1/group/{id}/cultural/competitions/{cid}/certificates/` | JWT (G3) | Generate certificates |
| GET | `/api/v1/group/{id}/cultural/analytics/type-distribution/` | JWT (G3) | Chart 7.1 — participation by event type |
| GET | `/api/v1/group/{id}/cultural/analytics/participation-trend/` | JWT (G3) | Chart 7.2 — branch participation trend |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load | `#kpi-bar` container | GET `.../cultural/head/kpi/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"`; shows skeleton per card while loading |
| KPI auto-refresh | `#kpi-bar` container | GET `.../cultural/head/kpi/` | `#kpi-bar` | `innerHTML` | `hx-trigger="every 5m"` |
| Chart 7.1 load | `#chart-type-distribution` container | GET `.../cultural/analytics/type-distribution/` | `#chart-type-distribution` | `innerHTML` | `hx-trigger="load"`; AY selector change re-triggers via `hx-swap-oob` |
| Chart 7.2 load | `#chart-participation-trend` container | GET `.../cultural/analytics/participation-trend/` | `#chart-participation-trend` | `innerHTML` | `hx-trigger="load"` |
| Branch table search | Search input | GET `.../cultural/branches/participation/?q=` | `#branch-table-body` | `innerHTML` | `hx-trigger="input delay:300ms"` |
| Branch table filter | Filter controls | GET `.../cultural/branches/participation/?filters=` | `#branch-table-section` | `innerHTML` | `hx-trigger="click"` |
| Branch table pagination | Pagination links | GET `.../cultural/branches/participation/?page=` | `#branch-table-section` | `innerHTML` | `hx-trigger="click"` |
| Open event create drawer | [+ New Event] button | GET `.../cultural/events/create-form/` | `#drawer-body` | `innerHTML` | `hx-trigger="click"` |
| Open Annual Day edit drawer | [Edit Annual Day] button per row | GET `.../cultural/events/{eid}/edit-form/` | `#drawer-body` | `innerHTML` | `hx-trigger="click"`; pre-fills all fields from existing event record |
| Open result entry drawer | [Enter Results] button per row | GET `.../cultural/competitions/{id}/result-form/` | `#drawer-body` | `innerHTML` | `hx-trigger="click"` |
| Submit results | Results drawer form | POST `.../cultural/competitions/{id}/results/` | `#drawer-body` | `innerHTML` | `hx-trigger="submit"`; fires success toast on `hx-on::after-request` |

---

*Page spec version: 1.1 · Last updated: 2026-03-21*
