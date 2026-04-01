# 25 — Safety Inspection Planner

> **URL:** `/group/welfare/safety-audit/planner/`
> **File:** `25-safety-inspection-planner.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Safety Audit Officer (Role 96, G1) — plan and schedule inspections

---

## 1. Purpose

Annual inspection planning tool for the Group Safety Audit Officer. The officer builds and manages the full-year safety inspection calendar for all branches across all eight inspection categories. This is the **pre-visit planning layer** — logistics, assignments, and scheduling — before the actual inspection occurs. Inspection reports are recorded in page 26.

**Eight inspection categories:**

| # | Category | Scope |
|---|---|---|
| 1 | Fire Safety | Extinguishers (count, expiry, location), hydrants, escape routes, fire alarm system, assembly point, staff fire training |
| 2 | Building Safety | Structural integrity, visible cracks, drainage, roof condition, staircases, classrooms and common area safety |
| 3 | Electrical Safety | Distribution panel boxes, earthing continuity, overloading indicators, open wiring, emergency lighting |
| 4 | Playground & Sports Safety | Equipment condition, surface (grass/rubber), fencing, shade, first-aid proximity |
| 5 | Hostel Safety | Fire exits in hostel blocks, warden room locations, emergency lighting in corridors, evacuation plan displayed |
| 6 | Transport Yard Safety | Vehicle condition, fuel storage compliance, parking bay safety, tyre and brake logs |
| 7 | Food Safety | Kitchen hygiene, storage temperature logs, pest control records, food handler health certificates |
| 8 | Lab Safety | Chemical storage and labelling, fume hood condition, personal protective equipment availability, ventilation |

Each branch must receive at least one **Full Audit** per year (covering all 8 categories in a single visit or a scheduled sequence of visits within 30 days). Individual category inspections may also be planned as standalone **Targeted Visits**. Surprise visits are unannounced and are planned by the Safety Audit Officer without advance notification to the branch.

**Role level G1 means:** read access to all existing data + create inspection schedule + annotate plans. The Safety Audit Officer cannot edit or delete operational data created by other roles. Field edits to the inspection plan (reschedule, cancel) are within scope.

Scale: 20–50 branches. At one full audit per branch per year plus targeted and surprise visits, the planner manages 40–200 inspection records per year.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Safety Audit Officer | G1 | Read all + create inspection plan + reschedule + cancel | Primary owner; cannot edit inspection reports (page 26) |
| Group COO | G4 | Read all — full planning calendar | No create; no edit |
| Branch Principal | Branch | Read own branch's scheduled inspections (not surprise visits) | Surprise visits are hidden from branch view until the inspector arrives |
| Group Chairman / CEO | G5 | Read — annual calendar summary + completion rate | No create; no edit |
| All other roles | — | No access | — |

> **Access enforcement:** `@require_role('safety_audit_officer', 'coo', 'branch_principal', 'chairman')`. Branch Principal role: querysets filtered to own branch and `type != 'surprise'`. Surprise visit records have `is_hidden_from_branch=True`; this flag is evaluated at the serialiser layer.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Safety Audit  ›  Inspection Planner
```

### 3.2 Page Header
- **Title:** `Safety Inspection Planner`
- **Subtitle:** `[Academic Year] · [N] Inspections Planned · [N] Completed · [N] Pending · [N] Overdue`
- **Right controls:** `+ Create Inspection Plan` · `View Annual Calendar` · `Advanced Filters` · `Export CSV`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Branches not yet scheduled | "[N] branches have no inspection scheduled for the current academic year. Plan inspections immediately." | Red |
| Inspections overdue (planned date passed, not completed) | "[N] inspections are overdue — planned date has passed without a completed report." | Red |
| Full audit coverage below 100% | "[N] branches have not yet received a full audit this year." | Amber |
| Inspector schedule conflict | "Inspector [Name] has overlapping planned visits on [Date]. Review the calendar." | Amber |

---

## 4. KPI Summary Bar

Eight cards in a responsive 4×2 grid. All metrics reflect the currently selected Academic Year and Branch filters.

| # | Card | Metric | Colour Rule |
|---|---|---|---|
| 1 | Total Planned This Year | Count of all inspection plan records for the year | Blue always |
| 2 | Completed | Count with Status = Completed (linked report submitted) | Green always |
| 3 | Pending | Count with Status = Confirmed or Draft and planned date not yet passed | Blue always |
| 4 | Overdue | Planned date passed + Status ≠ Completed or Cancelled | Red > 0 · Green = 0 |
| 5 | Branches Not Yet Scheduled | Count of branches with zero confirmed inspections this year | Red > 5 · Yellow 1–5 · Green = 0 |
| 6 | Full Audit Coverage % | (Branches with at least one Full Audit completed / Total branches) × 100 | Green = 100% · Yellow 80–99% · Red < 80% |
| 7 | Inspections by Category | Mini bar: count per category (8 bars) | Visual only |
| 8 | Inspections by Type | Mini donut: Scheduled / Surprise / Targeted proportions | Visual only |

---

## 5. Main Table — Inspection Plans

### 5.1 Search
Full-text search on: Inspection ID, Branch Name, Inspector Name. Debounce 300 ms, minimum 2 characters.

### 5.2 Advanced Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Category | Checkbox | Fire · Building · Electrical · Playground · Hostel · Transport · Food · Lab · Full Audit |
| Type | Checkbox | Scheduled · Surprise · Targeted |
| Status | Checkbox | Draft · Confirmed · Completed · Cancelled · Rescheduled |
| Date Range (Planned Date) | Date picker | From – To |
| Inspector | Single-select | All inspectors on record |
| Overdue Only | Toggle | Yes / No |
| Academic Year | Single-select | Current + 2 prior years |

### 5.3 Table Columns

| Column | Sortable | Notes |
|---|---|---|
| Inspection ID | ✅ | System-generated (e.g., INS-2026-00089) |
| Branch | ✅ | |
| Category | ✅ | Fire / Building / Electrical / Playground / Hostel / Transport / Food / Lab / Full Audit tag |
| Type | ✅ | Scheduled (blue) · Surprise (red) · Targeted (amber) badge |
| Inspector(s) | ✅ | Primary inspector name; "(+N more)" if multiple |
| Planned Date | ✅ | DD-MMM-YYYY; red if overdue |
| Status | ✅ | Draft (grey) · Confirmed (blue) · Completed (green) · Cancelled (dark grey) · Rescheduled (purple) badge |
| Last Updated | ✅ | Relative time |
| Actions | ❌ | View · Edit · Reschedule · Cancel |

**Default sort:** Planned Date ascending (soonest first), then Overdue records pinned to top.
**Pagination:** Server-side · 25 rows/page.
**Surprise visit rows:** Visible to Safety Audit Officer and COO only. Branch Principal sees a filtered list that excludes these rows (enforced server-side).

---

## 6. Drawers / Modals

### 6.1 Drawer — `inspection-plan-detail` (600px, right side)

Triggered by **View** in Actions column.

| Field | Notes |
|---|---|
| Inspection ID | Read-only |
| Branch | Name + address |
| Inspection Category | Tag(s) — Full Audit lists all 8 categories |
| Type | Scheduled / Surprise / Targeted |
| Inspector(s) | Names + contact numbers |
| Planned Date | DD-MMM-YYYY |
| Expected Duration | e.g., "Full day (6–8 hours)" |
| Travel Mode | Road / Rail / Air |
| Accommodation Required | Yes / No; if Yes: hotel name + confirmation number |
| Checklist Version Assigned | e.g., "Fire Safety Checklist v3.2 (2025)" |
| Branch Contact | Name + mobile + role |
| Inspector Notes | Free text — any pre-visit information or specific focus areas |
| Status | Badge |
| Status History | Compact timeline: Draft → Confirmed → (Completed / Cancelled / Rescheduled) with timestamps |
| Linked Inspection Report | Link to report in page 26 (shown once status = Completed) |

**Footer actions (Safety Audit Officer only):** `Edit Plan` · `Reschedule` · `Cancel Plan`

---

### 6.2 Drawer — `create-inspection-plan` (560px, right side)

Triggered by **+ Create Inspection Plan** button.

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select (searchable) | Required |
| Inspection Category | Checkbox list (multi-select for Full Audit; single for targeted) | Required; at least one; if all 8 selected, auto-labelled "Full Audit" |
| Inspection Type | Radio: Scheduled · Surprise · Targeted | Required |
| Planned Date | Date picker | Required; not in past |
| Inspector(s) | Multi-select (search by name from inspector registry) | Required; at least one |
| Primary Inspector | Single-select (from above list) | Required |
| Expected Duration | Single-select: Half Day (3–4h) · Full Day (6–8h) · Multi-Day | Required |
| Travel Mode | Radio: Road · Rail · Air · No Travel (local) | Required |
| Accommodation Required | Toggle | Required |
| Hotel / Accommodation Details | Text input | Required if Accommodation = Yes |
| Checklist Version | Single-select (pulls from checklist template registry per selected categories) | Required; auto-populated based on category |
| Branch Contact Name | Text input | Required |
| Branch Contact Mobile | Text input (10-digit validation) | Required |
| Branch Contact Role | Single-select | Required |
| Inspector Notes | Textarea (max 1,000 chars) | Optional |
| Status | Radio: Draft · Confirmed | Required |

**Surprise type behaviour:** If Type = Surprise, a warning is shown: *"This inspection is marked as Surprise. It will not be visible to the branch principal or staff in their portal view until the inspector checks in at the branch."*

**Conflict check:** On selecting Inspector + Planned Date, HTMX fires a conflict-check call. If the inspector already has a confirmed visit on that date, an inline warning appears: *"[Inspector] has a confirmed visit to [Branch] on [Date]. Review before confirming."*

**Footer:** `Cancel` · `Save as Draft` · `Save & Confirm`

**Validation:**
- Planned Date must be a weekday
- If Type = Full Audit, all 8 category checkboxes must be selected
- If Accommodation Required = Yes, Hotel details required

---

### 6.3 Drawer — `reschedule-inspection` (400px, right side)

Triggered by **Reschedule** in Actions column or plan detail drawer.

| Field | Type | Validation |
|---|---|---|
| Inspection ID | Read-only | |
| Branch | Read-only | |
| Original Planned Date | Read-only | |
| New Planned Date | Date picker | Required; not in past; must be different from original |
| Reason for Rescheduling | Single-select: Branch Request · Inspector Unavailability · Weather / Force Majeure · Logistical Issue · Other | Required |
| Additional Notes | Textarea (max 500 chars) | Optional |

**Footer:** `Cancel` · `Confirm Reschedule`

**Behaviour:** On confirm, Status updated to Rescheduled; original planned date and reason logged in the status history; Branch Principal receives notification (except for surprise visits). Inspector receives notification of new date.

---

### 6.4 Drawer — `annual-calendar-view` (800px, right side)

Triggered by **View Annual Calendar** button. Full-year timeline visualisation.

**Layout:** A 12-column grid (Jan–Dec or Apr–Mar depending on academic year setting), one row per branch.

| Element | Detail |
|---|---|
| Row labels | Branch names (alphabetical or by region) |
| Column headers | Month abbreviations |
| Cell markers | Coloured dot per planned inspection: Blue (Scheduled) · Red (Surprise — hidden from branch view) · Amber (Targeted) · Green (Completed) · Grey (Cancelled) |
| Tooltip | On hover: Inspection ID, Category, Type, Inspector, Status |
| Click | Opens `inspection-plan-detail` drawer for that inspection |
| Empty cell | Light grey background — no inspection planned for this branch in this month |
| Row highlight | Rows for branches with no Full Audit planned are highlighted with a subtle amber row background |

**Legend:** Colour legend below the calendar.

**Filters within calendar view:** Year selector · Category filter · Type filter (checkboxes).

**Export:** Calendar view can be exported as PNG or PDF from within the drawer.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Inspection plan created (Draft) | "Inspection plan [ID] saved as Draft." | Success |
| Inspection plan confirmed | "Inspection plan [ID] confirmed. Inspector will be notified." | Success |
| Plan rescheduled | "Inspection [ID] rescheduled to [New Date]." | Success |
| Plan cancelled | "Inspection [ID] has been cancelled." | Warning |
| Inspector conflict detected | "Warning: [Inspector] already has a visit planned on [Date]. Resolve before confirming." | Warning |
| Surprise inspection created | "Surprise inspection [ID] planned. Branch will not be notified." | Info |
| Checklist auto-assigned | "Checklist version [V] auto-assigned for [Category]." | Info |
| Validation error | "Please complete all required fields before saving." | Error |
| Export triggered | "Calendar export is being prepared." | Info |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No inspections for current filters | "No inspections match the current filters." | "Try adjusting or clearing your filters." | `Clear Filters` button |
| No inspections planned this year | "No inspections planned for this academic year." | "Create the first inspection plan to begin scheduling." | `+ Create Inspection Plan` button |
| Annual calendar — branch with no plans | Row shows: "No visits planned" label in grey across all months | Branch highlighted with amber row background | Clicking row opens `create-inspection-plan` pre-filled with that branch |
| Plan detail — no linked report | Linked Inspection Report field shows: "Report not yet submitted." | "(Report will appear here after the inspection is completed and submitted.)" | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 8 KPI cards + table (10 grey rows × 9 columns) |
| Filter / search apply | Table body spinner overlay; KPI cards refresh after |
| Inspection plan detail drawer open | Drawer skeleton: 12 grey field blocks in 2-column layout |
| Annual calendar drawer open | 800px drawer: full grid skeleton — grey dots across a 12×50 matrix placeholder |
| Create form — checklist auto-populate | Checklist Version field shows "Loading checklist versions…" spinner for 300 ms |
| Inspector conflict check | Inline spinner next to inspector + date fields: "Checking for conflicts…" |
| Reschedule submit | Modal footer spinner; disabled until complete |
| Calendar export | Progress bar in calendar drawer footer |

---

## 10. Role-Based UI Visibility

| UI Element | Safety Audit Officer | COO | Branch Principal | Chairman |
|---|---|---|---|---|
| Full inspection plan list | ✅ (all branches, all types) | ✅ (all branches, all types) | Own branch, no surprise visits | Summary view only |
| + Create Inspection Plan | ✅ | ❌ | ❌ | ❌ |
| Edit / Reschedule / Cancel | ✅ | ❌ | ❌ | ❌ |
| Surprise visit records visible | ✅ | ✅ | ❌ (hidden server-side) | ❌ |
| Annual Calendar button | ✅ | ✅ | Own branch only | ❌ |
| Checklist Version field | ✅ | Read-only | ❌ | ❌ |
| Inspector Notes field | ✅ | Read-only | ❌ | ❌ |
| Export CSV | ✅ | ✅ | ❌ | ❌ |
| KPI bar — full detail | ✅ | ✅ | Own branch metrics | Summary % only |
| Alert banners | ✅ | ✅ | Own branch alerts | ❌ |
| Overdue alert | ✅ | ✅ | Own branch | ❌ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/welfare/safety/inspections/plans/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/safety/inspections/plans/` | List inspection plans (paginated, filtered, role-scoped) | JWT + role check |
| POST | `/api/v1/group/{group_id}/welfare/safety/inspections/plans/` | Create new inspection plan | Safety Audit Officer |
| GET | `/api/v1/group/{group_id}/welfare/safety/inspections/plans/{plan_id}/` | Retrieve plan detail | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/welfare/safety/inspections/plans/{plan_id}/` | Edit inspection plan | Safety Audit Officer |
| POST | `/api/v1/group/{group_id}/welfare/safety/inspections/plans/{plan_id}/reschedule/` | Reschedule inspection | Safety Audit Officer |
| POST | `/api/v1/group/{group_id}/welfare/safety/inspections/plans/{plan_id}/cancel/` | Cancel inspection plan | Safety Audit Officer |
| GET | `/api/v1/group/{group_id}/welfare/safety/inspections/plans/kpi/` | KPI summary bar | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/safety/inspections/plans/calendar/` | Annual calendar matrix data | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/safety/inspections/plans/conflict-check/` | Inspector date conflict check | Safety Audit Officer |
| GET | `/api/v1/group/{group_id}/welfare/safety/inspections/plans/alerts/` | Active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/safety/inspections/plans/export/` | Export CSV | Safety Audit Officer / COO |
| GET | `/api/v1/group/{group_id}/welfare/safety/checklists/` | List available checklist versions by category | Safety Audit Officer |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Filter by branch ID(s) |
| `category` | str[] | `fire`, `building`, `electrical`, `playground`, `hostel`, `transport`, `food`, `lab`, `full_audit` |
| `type` | str[] | `scheduled`, `surprise`, `targeted` |
| `status` | str[] | `draft`, `confirmed`, `completed`, `cancelled`, `rescheduled` |
| `date_from` | date | Planned date range start |
| `date_to` | date | Planned date range end |
| `inspector` | int | Filter by inspector ID |
| `overdue_only` | bool | Only overdue inspections |
| `academic_year` | str | e.g., `2025-26` |
| `page` | int | Page number |
| `page_size` | int | Default 25, max 100 |
| `search` | str | Inspection ID, branch, inspector name |

**Conflict check query parameters:**

| Parameter | Type | Description |
|---|---|---|
| `inspector_id` | int | Inspector to check |
| `planned_date` | date | Date to check for conflicts |
| `exclude_plan_id` | int | Exclude current plan from conflict check (used during edit) |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search input | `hx-get="/api/.../plans/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#plans-table-body"` `hx-include="#filter-form"` | Table body replaced |
| Filter apply | `hx-get="/api/.../plans/"` `hx-trigger="change"` `hx-target="#plans-table-body"` `hx-include="#filter-form"` | Table + KPI refreshed |
| Pagination | `hx-get="/api/.../plans/?page={n}"` `hx-target="#plans-table-body"` `hx-push-url="true"` | Page swap |
| Plan detail drawer open | `hx-get="/api/.../plans/{plan_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in |
| Inspector + date conflict check | `hx-get="/api/.../plans/conflict-check/?inspector_id={id}&planned_date={date}"` `hx-trigger="change from:#inspector-select, change from:#planned-date"` `hx-target="#conflict-warning"` | Inline conflict warning partial swapped |
| Category selection — checklist auto-populate | `hx-get="/api/.../checklists/?category={slugs}"` `hx-trigger="change from:.category-checkbox"` `hx-target="#checklist-version-field"` | Checklist version dropdown populated |
| Surprise type selection | `hx-trigger="change from:#inspection-type-radio"` `hx-target="#surprise-warning-banner"` | Warning partial swapped in if value = surprise |
| Create plan submit | `hx-post="/api/.../plans/"` `hx-target="#plans-table-body"` `hx-on::after-request="closeDrawer(); fireToast();"` | New row prepended; drawer closes |
| Plan edit submit | `hx-patch="/api/.../plans/{plan_id}/"` `hx-target="#plan-row-{plan_id}"` `hx-swap="outerHTML"` | Row updated in place |
| Reschedule submit | `hx-post="/api/.../plans/{plan_id}/reschedule/"` `hx-target="#plan-row-{plan_id}"` `hx-swap="outerHTML"` | Row status badge updated; drawer closes |
| Cancel plan submit | `hx-post="/api/.../plans/{plan_id}/cancel/"` `hx-target="#plan-row-{plan_id}"` `hx-swap="outerHTML"` | Row status updated to Cancelled |
| Annual calendar open | `hx-get="/api/.../plans/calendar/?year={year}"` `hx-target="#drawer-container"` `hx-trigger="click"` | 800px calendar drawer loaded |
| Calendar filter change | `hx-get="/api/.../plans/calendar/?year={year}&category={slugs}&type={slugs}"` `hx-trigger="change"` `hx-target="#calendar-grid"` `hx-include="#calendar-filter-form"` | Calendar grid updated |
| KPI bar refresh | `hx-get="/api/.../plans/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |
| Alert banner load | `hx-get="/api/.../plans/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Conditional banner |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
