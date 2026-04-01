# 17 — Scholarship Exam Scheduler

> **URL:** `/group/adm/scholarship-exam/scheduler/`
> **File:** `17-scholarship-exam-scheduler.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Scholarship Exam Manager (Role 26, G3) — primary

---

## 1. Purpose

The Scholarship Exam Scheduler is the central planning surface for all scholarship entrance examinations run across the group during an admission cycle. The Group Scholarship Exam Manager uses this page to create exam events, assign branches as physical or online venues, define registration windows (open/close dates), set candidate eligibility rules, and coordinate answer paper dispatch to branch invigilators. Every scholarship exam — whether merit-based, need-based, stream-specific, or NTSE-preparatory — is created and tracked from this single page.

Large scholarship exam drives involve concurrent sittings across 20–40 branches spread across multiple cities on the same day. Logistically, this creates the potential for resource conflicts: two exams may inadvertently be scheduled at the same branch and time, the same invigilator pool may be double-booked, or registration windows may overlap. The Scheduling Conflict Detector (Section 5.4) runs automatically on every save and flags these conflicts before they become operational problems.

The page also acts as an operations dashboard in the days leading up to each exam. Branch venue confirmations, invigilator assignments, and registration counts are surfaced in real time so the Scholarship Exam Manager can intervene — calling branches that have not confirmed halls, following up on low registration rates, or redistributing candidates to alternative venues if hall capacity is exceeded.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Exam Manager (26) | G3 | Full CRUD — create exams, edit, cancel, open/close registration, confirm venues | Primary owner of this page |
| Group Admissions Director (23) | G3 | Approve exam creation + view all | Cannot edit after approval |
| Group Admission Coordinator (24) | G3 | View only — all exams, all branches | No create/edit/cancel |
| Chief Academic Officer | G2 | View only | Read-only cross-division access |
| Branch Principal | Branch | View exams assigned to own branch | Scoped by branch |
| Group Scholarship Manager (Role 27) | G3 | Read — Section 5.1 (Exam Schedule Table) and Section 5.3 (Registration Status) only | Needs exam visibility to coordinate scholarship awards |

**Enforcement:** All access decisions are made server-side in Django using `request.user.role` checks in views and template conditionals. No client-side role logic is used. Write actions on the API require JWT claims with `role >= G3` and `function == scholarship_exam`. The Director's approval action uses a dedicated approval endpoint. View decorator: `@role_required(['scholarship_exam_manager', 'admissions_director', 'admission_coordinator', 'scholarship_manager', 'cao', 'branch_principal'])`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarship Exams → Scheduler
```

### 3.2 Page Header
- **Title:** Scholarship Exam Scheduler
- **Subtitle:** `{Current Cycle Name}` — e.g., "Admissions Cycle 2026-27"
- **Action Buttons:** `[+ Schedule New Exam]` (Scholarship Exam Manager only) · `[Export Schedule PDF]` · `[Cycle ▾]` (cycle switcher dropdown)
- **Status Chip:** Active Cycle badge (green) or Closed Cycle (grey)

### 3.3 Alert Banner
Triggers (dismissible, auto-reappear after 24 h if unresolved):
- **Red — Scheduling Conflict:** "2 scheduling conflicts detected. Two exams share Branch XYZ on {date}. [Resolve →]"
- **Amber — Venue Unconfirmed:** "7 branches have not confirmed venues for {Exam Name} (exam in 6 days). [View →]"
- **Amber — Registration Closing Soon:** "Registration for {Exam Name} closes in 2 days. Current: 340 registered of 600 target. [View →]"
- **Blue — Approval Required:** "Merit Scholarship Exam 2026 is pending Director approval before registration can open."

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Exams Scheduled | Count of exam records in current cycle (any status except Cancelled) | `scholarship_exam` table | Blue always | → filtered schedule table |
| Registrations Open Now | Count of exams with status = Registration Open and registration_close_date >= today | `scholarship_exam` aggregation | Green > 0 · Grey = 0 | → filtered to open exams |
| Total Registered Candidates | SUM of registered_count across all non-cancelled exams in cycle | `exam_registration` aggregation | Blue always | → full candidate list |
| Venue Unconfirmed | Count of (exam × branch) pairs where venue_confirmed = False and exam not cancelled | `exam_branch_venue` aggregation | Red > 0 · Green = 0 | → Section 5.3 |
| Scheduling Conflicts | Count of active conflicts from conflict detector | `exam_conflict` table | Red > 0 · Green = 0 | → Section 5.4 |
| Exams in Next 7 Days | Count of exams with exam_date BETWEEN today AND today+7 | `scholarship_exam` filter | Amber > 0 · Green = 0 | → filtered calendar view |

**HTMX Refresh:** KPI bar refreshes every 5 minutes via `hx-trigger="every 5m"` targeting `#kpi-bar` with `GET /api/v1/group/{group_id}/adm/scholarship-exam/scheduler/kpis/`.

---

## 5. Sections

### 5.1 Exam Schedule Table

**Display:** Sortable, selectable (checkbox), server-side paginated (20/page). Default sort: exam_date ASC.

**Columns:**

| Column | Notes |
|---|---|
| Checkbox | Bulk select |
| Exam Name | Linked — click opens Manage Drawer |
| Type | Badge: Merit (blue) / Need-based (purple) / Stream-specific (teal) / NTSE-prep (orange) |
| Date | Formatted DD-MMM-YYYY |
| Time | HH:MM (IST) |
| Mode | Offline (grey chip) / Online (blue chip) |
| Branches | Count with tooltip listing branch names |
| Registered | Numeric — links to candidate list |
| Target | Numeric — registration target |
| Venue Status | All Confirmed (green) / Partial (amber) / None (red) |
| Status Badge | Draft (grey) / Registration Open (green) / Registration Closed (amber) / Conducted (blue) / Results Pending (purple) / Completed (teal) |
| Actions | `[Edit →]` `[Manage →]` `[Cancel]` — Edit/Cancel hidden for Conducted/Completed |

**Filters:** Status (multi-select), Mode, Date range (from–to datepicker), Type (multi-select)

**Bulk Actions (Scholarship Exam Manager only):** `[Open Registration for Selected]` · `[Close Registration]` · `[Export Schedule]`

**HTMX Pattern:** Filter changes trigger `hx-get="/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/list/"` targeting `#exam-table-body` with `hx-swap="innerHTML"`. Pagination via `hx-get` on page links.

**Empty State:** No exams scheduled yet. Icon: calendar-plus. Heading: "No Exams Scheduled". CTA: `[+ Schedule First Exam]`.

---

### 5.2 Exam Calendar

**Display:** Full-month calendar grid (Monday–Sunday). Toggle: Month / Week view. Navigation: `[← Prev]` `[Today]` `[Next →]`.

**Exam Marks:** Colour-coded dot/pill on exam date — colour matches status badge. Multiple exams on same date stacked.

**Hover Tooltip (HTMX):** On date cell hover, lazy-load tooltip showing: Exam name, Type, Mode, Registered count, Venue status. `hx-trigger="mouseenter"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/scheduler/{exam_id}/tooltip/`.

**Click:** Clicking an exam pill scrolls to and highlights that exam row in Section 5.1 table.

**Empty State:** No exams in this month. Message inline: "No exams scheduled in {Month YYYY}."

---

### 5.3 Branch Venue Confirmation Status

**Display:** Collapsible section — expanded by default when venue_unconfirmed KPI > 0. Per-exam accordion: click exam name to expand branch rows.

**Columns (per exam × branch row):**

| Column | Notes |
|---|---|
| Branch | Branch name + city |
| Venue Confirmed | Yes (green ✓) / No (red ✗) |
| Hall Capacity | Numeric (seats) |
| Invigilators Assigned | Count |
| Actions | `[Confirm →]` (opens venue-confirm-drawer) — disabled if already confirmed |

**Filters:** Exam (dropdown), Confirmation status

**HTMX Pattern:** `[Confirm →]` opens venue-confirm-drawer via `hx-get="/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/venue/{venue_id}/confirm-drawer/"` targeting `#drawer-container`.

**Empty State:** All branches confirmed for all upcoming exams. Icon: check-circle. Heading: "All Venues Confirmed".

---

### 5.4 Scheduling Conflict Detector

**Display:** Alert list — automatically computed on page load and on every exam save. Each conflict shown as a red card.

**Conflict Card Fields:** Conflict type (Branch double-booked / Registration window overlap / Invigilator double-assigned) · Exam A name + date · Exam B name + date · Branch name · Overlap window · Severity (High/Medium)

**Actions on Card:** `[Reschedule Exam A →]` · `[Reschedule Exam B →]` · `[Dismiss (add exception)]`

**HTMX Pattern:** `hx-trigger="load"` and re-triggered on any exam save: `GET /api/v1/group/{group_id}/adm/scholarship-exam/scheduler/conflicts/` targeting `#conflict-list`.

**Empty State:** No conflicts detected. Icon: shield-check (green). Heading: "No Scheduling Conflicts". Description: "All exams are conflict-free."

---

### 5.5 Registration Window Status

**Display:** Card list — one card per exam with status = Registration Open.

**Card Fields:** Exam name · Open since (date) · Closing date (with days-remaining countdown chip) · Registered count · Daily registration rate sparkline (Chart.js inline sparkline — last 7 days) · Progress bar (registered / target)

**HTMX Pattern:** Section refreshes every 5 minutes via `hx-trigger="every 5m"` targeting `#registration-window-list`.

**Empty State:** No exams have registration open right now. Icon: calendar-x. Message: "No active registration windows."

---

## 6. Drawers & Modals

### 6.1 Exam Create/Edit Drawer
- **Width:** 640px (right slide-in)
- **Trigger:** `[+ Schedule New Exam]` or `[Edit →]` on table row
- **HTMX Endpoint (load):** `GET /api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exam-form/{exam_id}/` (exam_id = `new` for create)
- **Tabs:**
  1. **Basic Info** — Exam name, Type, Description, Academic year, Cycle
  2. **Schedule** — Date, Start time, Duration (minutes), Mode (Offline/Online), Online platform link (if Online)
  3. **Branches & Venues** — Multi-select branches; per-branch: hall name, capacity, invigilator count
  4. **Eligibility** — Class, Stream, Min marks in previous exam, Fee paid required
  5. **Registration Settings** — Registration open date, Registration close date, Max registrations, Allow walk-in
  6. **Fees** — Exam fee amount, Fee waiver allowed, Fee collection method
  7. **Review** — Summary of all tabs before submit
- **Submit:** `hx-post` / `hx-put` → `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exams/` · on success: close drawer, refresh table, show success toast

### 6.2 Conflict Resolution Drawer
- **Width:** 480px
- **Trigger:** `[Reschedule One →]` on conflict card
- **HTMX Endpoint (load):** `GET /api/v1/group/{group_id}/adm/scholarship-exam/scheduler/conflicts/{conflict_id}/resolve/`
- **Content:** Shows conflicting exams side by side. Date/time edit fields for one or both. Validation re-runs on field change (HTMX inline validation).
- **Submit:** `hx-put` → `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exams/{exam_id}/` · conflict list refreshes after save

### 6.3 Venue Confirm Drawer
- **Width:** 400px
- **Trigger:** `[Confirm →]` in Section 5.3
- **HTMX Endpoint (load):** `GET /api/v1/group/{group_id}/adm/scholarship-exam/scheduler/venue/{venue_id}/confirm-drawer/`
- **Content:** Branch name, exam name, hall name (editable), capacity (editable), invigilator names (text), [Confirm Venue] button
- **Submit:** `hx-post` → `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/venue/{venue_id}/confirm/` · on success: update row in Section 5.3, show toast

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Exam created | "Exam '{name}' scheduled successfully." | Success | 4 s |
| Exam updated | "Exam '{name}' updated." | Success | 3 s |
| Registration opened | "Registration opened for '{name}'." | Success | 4 s |
| Registration closed | "Registration closed for '{name}'." | Info | 3 s |
| Exam cancelled | "Exam '{name}' has been cancelled." | Warning | 5 s |
| Venue confirmed | "Venue confirmed for {Branch} — {Exam}." | Success | 3 s |
| Conflict detected on save | "Scheduling conflict detected. Review required." | Error | 6 s |
| Conflict resolved | "Conflict resolved. Schedule updated." | Success | 4 s |
| Bulk registration open | "{n} exams opened for registration." | Success | 4 s |
| Export triggered | "Schedule export is being prepared. Download will start shortly." | Info | 4 s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No exams in current cycle | Calendar-plus icon | "No Exams Scheduled Yet" | "Start by creating the first scholarship exam for this admission cycle." | `[+ Schedule New Exam]` |
| No conflicts | Shield-check icon (green) | "No Scheduling Conflicts" | "All exams are conflict-free." | None |
| No open registration windows | Calendar-x icon | "No Active Registration Windows" | "Open registration for an exam to see it here." | `[View Schedule →]` |
| No exams on selected calendar month | Calendar icon | "No Exams in {Month}" | "No scholarship exams are scheduled for this period." | `[+ Schedule Exam]` |
| Filter returns no results | Search icon | "No Exams Match Filters" | "Try adjusting your filter criteria." | `[Clear Filters]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer (6 cards) + table rows shimmer (5 rows) |
| KPI bar refresh (every 5 min) | Subtle in-place spinner on each KPI card — no layout shift |
| Exam table filter/search | Table body skeleton (5 row shimmer) while fetching |
| Exam calendar month change | Calendar grid shimmer overlay |
| Drawer open | 400px-wide right-panel skeleton with tab shimmer |
| Venue confirm drawer | 400px drawer skeleton — 3 field shimmers |
| Conflict list refresh | List shimmer (3 row cards) |
| Registration window list refresh | Card list shimmer (2-3 cards) |
| Bulk action (open/close registration) | Button spinner + toast "Processing…" |

---

## 10. Role-Based UI Visibility

| Element | Exam Manager (26) | Director (23) | Coordinator (24) | CAO | Branch Principal | Sch Mgr (27) |
|---|---|---|---|---|---|---|
| `[+ Schedule New Exam]` button | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Edit →]` on table row | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Cancel]` on table row | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Bulk action bar | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Approve]` action (Director) | Hidden | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Confirm →]` in venue table | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Reschedule One →]` on conflict | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Conflict Detector section | Visible | Visible | Visible (read) | Visible (read) | Hidden | Hidden |
| Section 5.1 Exam Schedule Table | Visible | Visible | Visible | Visible (read) | Own branches only | R (read-only, no edit/cancel actions) |
| Section 5.3 Registration Status | Visible | Visible | Visible | Hidden | Hidden | R (read-only) |
| Section 5.5 registration windows | Visible | Visible | Visible | Hidden | Hidden | Hidden |
| Export button | Visible | Visible | Visible | Hidden | Hidden | Hidden |
| Branch Principal row scope | N/A | N/A | N/A | N/A | Own branches only | N/A |

*All UI visibility decisions made server-side in Django template. No client-side JS role checks.*

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/kpis/` | JWT G3 read | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/list/` | JWT G3 read | Paginated, filtered exam list |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exams/` | JWT G3 write | Create new exam |
| PUT | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exams/{exam_id}/` | JWT G3 write | Update exam |
| DELETE | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exams/{exam_id}/` | JWT G3 write | Cancel exam (soft delete) |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exam-form/{exam_id}/` | JWT G3 read | Exam create/edit drawer HTML fragment |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/calendar/` | JWT G3 read | Calendar data (month param) |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/{exam_id}/tooltip/` | JWT G3 read | Calendar hover tooltip fragment |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/venues/` | JWT G3 read | Venue confirmation status list |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/venue/{venue_id}/confirm/` | JWT G3 write | Confirm venue |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/venue/{venue_id}/confirm-drawer/` | JWT G3 read | Venue confirm drawer fragment |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/conflicts/` | JWT G3 read | Conflict list |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/conflicts/{conflict_id}/resolve/` | JWT G3 read | Conflict resolution drawer fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exams/{exam_id}/registration/open/` | JWT G3 write | Open registration for exam |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exams/{exam_id}/registration/close/` | JWT G3 write | Close registration |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/registration-windows/` | JWT G3 read | Active registration window cards |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exams/{exam_id}/approve/` | JWT G3 Director | Director approves exam |
| DELETE | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exams/{exam_id}/` | JWT G3 | Cancel (delete) a scheduled exam |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/scheduler/exams/bulk-close-registration/` | JWT G3 | Close registration for multiple exams simultaneously |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `/api/v1/.../scheduler/kpis/` | `#kpi-bar` | `innerHTML` |
| Filter exams table | `change` on filter inputs (debounce 300ms) | GET `.../scheduler/list/?{filters}` | `#exam-table-body` | `innerHTML` |
| Paginate exam table | `click` on page link | GET `.../scheduler/list/?page={n}` | `#exam-table-container` | `innerHTML` |
| Sort exam table column | `click` on column header | GET `.../scheduler/list/?sort={col}&dir={asc|desc}` | `#exam-table-body` | `innerHTML` |
| Open exam create drawer | `click` on `[+ Schedule New Exam]` | GET `.../scheduler/exam-form/new/` | `#drawer-container` | `innerHTML` |
| Open exam edit drawer | `click` on `[Edit →]` | GET `.../scheduler/exam-form/{exam_id}/` | `#drawer-container` | `innerHTML` |
| Submit exam form (create) | `submit` on exam form | POST `.../scheduler/exams/` | `#exam-table-body` | `innerHTML` (+ close drawer) |
| Submit exam form (edit) | `submit` on exam form | PUT `.../scheduler/exams/{exam_id}/` | `#exam-table-body` | `innerHTML` |
| Calendar month navigate | `click` prev/next | GET `.../scheduler/calendar/?month={YYYY-MM}` | `#calendar-grid` | `innerHTML` |
| Calendar exam hover tooltip | `mouseenter` on exam pill | GET `.../scheduler/{exam_id}/tooltip/` | `#tooltip-{exam_id}` | `innerHTML` |
| Conflict list refresh on save | `htmx:afterRequest` from exam form | GET `.../scheduler/conflicts/` | `#conflict-list` | `innerHTML` |
| Open venue confirm drawer | `click` on `[Confirm →]` | GET `.../scheduler/venue/{venue_id}/confirm-drawer/` | `#drawer-container` | `innerHTML` |
| Submit venue confirmation | `submit` on venue form | POST `.../scheduler/venue/{venue_id}/confirm/` | `#venue-row-{venue_id}` | `outerHTML` |
| Open conflict resolution drawer | `click` on `[Reschedule One →]` | GET `.../scheduler/conflicts/{conflict_id}/resolve/` | `#drawer-container` | `innerHTML` |
| Registration window list refresh | `every 5m` | GET `.../scheduler/registration-windows/` | `#registration-window-list` | `innerHTML` |
| Bulk open registration | `click` on `[Open Registration for Selected]` | POST `.../scheduler/exams/bulk-open-registration/` | `#exam-table-body` | `innerHTML` |
| Open exam manage drawer | `click` on `[Manage →]` | GET `.../scheduler/exam-form/{exam_id}/` | `#drawer-container` | `innerHTML` |
| Cancel exam | `click from:.btn-cancel-exam` | DELETE `.../adm/scholarship-exam/scheduler/exams/{id}/` | `#exam-schedule-table` | `innerHTML` |
| Bulk close registration | `click from:#btn-bulk-close-reg` | POST `.../exams/bulk-close-registration/` | `#exam-schedule-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
