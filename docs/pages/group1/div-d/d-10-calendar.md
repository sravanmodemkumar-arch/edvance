# D-10 — Content Calendar & Quota Planner

> **Route:** `/content/director/calendar/`
> **Division:** D — Content & Academics
> **Primary Role:** Content Director (18)
> **Read Access:** SME ×9 (19–27) — own quota and freeze status only
> **File:** `d-10-calendar.md`
> **Priority:** P1 — Needed once ≥ 2 SMEs are producing content
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Content Calendar & Quota Planner
**Route:** `/content/director/calendar/`
**Part-load routes:**
- `/content/director/calendar/?part=calendar-grid&month={YYYY-MM}` — monthly calendar grid
- `/content/director/calendar/?part=quota-table` — SME quota configuration table
- `/content/director/calendar/?part=performance-chart` — actual vs target 6-month chart
- `/content/director/calendar/?part=sme-view&sme_id={user_id}` — SME-restricted view of own quota

---

## 2. Purpose (Business Objective)

Content production at the scale of 15,000–20,000 questions per month does not happen spontaneously. Without explicit monthly quota targets per SME, production becomes uneven — one SME authors 500 questions while another produces 50, coverage gaps widen in under-resourced subjects, and exam periods arrive without sufficient content depth.

The Content Calendar provides the operational planning layer: when are the major exam dates? When should content freeze? Which months need production surges for season-specific exams? How does the Director set SME-specific monthly targets and track progress against them?

At the same time, the freeze mechanism is a critical safety feature: once an exam paper's question pool is finalised, new questions for that exam type must not enter the pool until after the exam (preventing accidental contamination of a sealed exam set). D-10 is where these freeze dates are configured — and D-02 enforces them at the SME's Submit button.

**Business goals:**
- Enable monthly quota planning per SME per subject per exam type
- Track actual production vs quota in real-time (published + in-pipeline counts)
- Manage content freeze dates per exam type (enforced in D-02 and D-04)
- Visualise upcoming exam peaks so the Director can plan production surges in advance
- Give SMEs a read-only view of their own quota and freeze status (no Director-level data visible)

---

## 3. User Roles

| Role | Access |
|---|---|
| Content Director (18) | Full — calendar edit, quota set, freeze config, assignment config |
| SME ×9 (19–27) | Read — own quota for current + next month · freeze status for own exam types · upcoming exam dates. Accessed via `/content/director/calendar/?sme_view=1` — renders only the SME-relevant subset. |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header (Director View)

- H1: "Content Calendar & Quota Planner"
- Month navigator: "← February 2026 | March 2026 | April 2026 →" — arrows navigate the calendar grid
- "Today" button — jumps to current month
- "Year View" toggle — switches calendar from monthly grid to year-at-a-glance (12 small month grids)

---

### Section 2 — Calendar View (Monthly Grid)

**Layout:** Standard month grid (7 columns = days of week, rows = weeks). Each day cell shows:

**Production indicator (bar fill):**
Daily published question count vs daily target (monthly quota / working days in month).
- Bar fill: green if at/above target · amber 50–99% · red < 50%
- Count label: "23 published" inside the bar

**Event markers (overlay badges on specific dates):**
- 🔵 Blue: Official exam date (imported from D-10 Upcoming Exam Dates panel)
- 🔴 Red: Content freeze date for a specific exam type (questions for this exam type cannot be submitted after this date)
- 🟡 Yellow: Production target milestone (Director-set custom markers: "GK surge: 200 questions needed by this date")
- 🟢 Green: Content freeze lifted

**Day cell click:** Opens a day-detail side panel showing:
- Breakdown of published questions by subject for that day
- Freeze events active on that day (which exam types are frozen)
- Any custom milestone notes the Director set

---

### Section 3 — Quota Config Table

**Purpose:** The core planning grid — Director sets monthly targets per SME.

**Layout:** Table with SMEs as rows, months as columns (current month + next 3 months shown by default; "Show More" expands to 12 months).

| Row Header | Description |
|---|---|
| GK SME | Role label (not personal name) |
| Math SME | — |
| (etc. for all 9 subjects) | — |

**Each cell (SME × Month):** Editable integer field — "120" (the monthly quota).
- Click to edit: inline input field
- Tab / Enter: saves and moves to next cell
- Unsaved changes highlighted in amber border
- "Save All" button (sticky at bottom) — saves all changed cells in one POST

**On save:**
- Updates `content_sme_quota` table for each SME + month combination
- In-app notification sent to the SME: "Your question quota for March 2026 has been updated to 120 questions." (D-01 KPI strip reflects the new target on next poll)
- Content type target sub-edit: hover over a cell shows a secondary edit icon → opens a popover: "Content Type Target Breakdown: Evergreen {N} / Current Affairs {N} / Time-Sensitive {N}" — optional per-SME per-month content type targets

**Column-level target row:**
Below the SME rows: "Total Monthly Target" row — sum of all SME quotas for that month. Shows the Director the total expected production.

**SME-to-Subject Assignment panel (below table):**

A matrix showing which SMEs are assigned to which Subject + Exam Type combinations. One SME can cover multiple subjects (Regional Language SME covers Telugu + Hindi + Urdu variants of State Board); one subject can have multiple SMEs for volume (GK might have 2 SMEs for high Current Affairs volume).

"Edit Assignments" → opens a modal with Subject × Exam Type grid and SME assignment dropdowns per cell.

---

### Section 4 — Actual vs Target Chart

**Purpose:** 6-month rolling view of actual production vs quota per SME — visualises performance trends over time.

**Chart type:** Grouped bar chart — per month, one bar group per SME.

Per SME bar group:
- Green bar: Questions published this month
- Amber bar: Questions in pipeline (in review + pending approval — "committed" to producing this month)
- Outline bar: Quota target

**Hover tooltip:** "GK SME — March 2026: Published 89 / In Pipeline 23 / Quota 120 · Effective progress: 93%"

**Chart controls:**
- Subject filter: view all SMEs or filter to specific subjects
- "Quota vs Published only" toggle — simplifies to just the two key bars
- "Export Chart Data" — downloads the underlying data as CSV (published count + quota per SME per month for the 6-month window)

---

### Section 5 — SME-to-Subject Assignment Panel

**Purpose:** Formal assignment of SMEs to Subject + Exam Type combinations. Determines which SMEs should be producing questions for which exam types, and informs D-15 reviewer assignment routing.

**Layout:** Two-column assignment editor:
- Left: Subject + Exam Type pairs (e.g. "Mathematics — SSC CGL")
- Right: Assigned SME (dropdown — all active SME role accounts) + Backup SME (optional)

**Save:** Updates `content_sme_subject_assignment` table. Changes take effect immediately — D-09 coverage gaps and D-05 SME Production Table reflect updated assignments.

---

### Section 6 — Upcoming Exam Dates Panel

**Purpose:** Calendar of major national and state exam events — context for production planning.

**Table:**

| Column | Description |
|---|---|
| Exam Name | SSC CGL Tier 1 2026 |
| Exam Type Code | SSC_CGL |
| Exam Date | 2026-03-20 |
| Content Freeze Date | 2026-02-28 (set here, enforced in D-02 + D-04) |
| Content Freeze Status | Active / Future / Lifted |
| "Edit" action | Edit dates inline |

**Add Exam Date:** "Add Exam" button → inline form: Exam Name + Exam Type (dropdown) + Exam Date + Content Freeze Date (date picker — must be before Exam Date).

**Purpose of these dates:**
1. Calendar view shows them as event markers (🔵 blue = exam date, 🔴 red = freeze date)
2. D-02 Submit button checks freeze status for the selected exam types — blocks submission if frozen
3. D-04 Approve+Publish checks freeze for the question's exam types — blocks approval for frozen exam types
4. D-05 Director Dashboard shows upcoming peaks in the SME Productivity section as planning context

---

### Section 7 — Content Freeze Config

**Purpose:** Formally configure which exam types are in content freeze — separate from the exam dates panel (which records freeze dates for future planning); this section shows the current active freeze status.

**Active Freezes table:**

| Column | Description |
|---|---|
| Exam Type | SSC CGL |
| Freeze Start | 2026-02-28 |
| Freeze End | Exam Date: 2026-03-20 (auto-lifted after exam date) |
| Status | 🔴 Active / 🟡 Future / 🟢 Lifted |
| "Lift Freeze Early" action | Director can lift freeze before exam date (e.g. if exam postponed) |

**Lift Freeze action:**
Confirmation modal: "Lift content freeze for SSC CGL? SMEs will be able to submit questions for this exam type immediately." Reason field (optional). Freeze record updated: `content_exam_freeze.freeze_end = now()`. D-02 and D-04 read from this table in real-time — the freeze lift takes effect immediately on next Submit attempt.

**Content Freeze enforcement (D-02 and D-04 side):**
D-10 configures the freeze dates in `content_exam_freeze` table. D-02 checks this table on Submit (no cache — real-time check needed). D-04 checks on Approve+Publish. The freeze check is purely: `content_exam_freeze.exam_type_code IN question.exam_types AND content_exam_freeze.freeze_start <= today <= freeze_end`.

---

### Section 8 — Content Type Targets

**Purpose:** Beyond total quota targets, the Director sets per-subject, per-month targets for content type distribution — ensuring the GK SME produces enough fresh Current Affairs questions, and the Math SME focuses on Evergreen content.

**Grid:** SME × Content Type (Evergreen / Current Affairs / Time-Sensitive) × Month.

For each cell: integer target (0 = not applicable).

Examples:
- Math SME, Evergreen, March 2026: 120 (all quota is Evergreen — Math content doesn't expire)
- GK SME, Current Affairs, March 2026: 80 (most GK quota should be current events)
- GK SME, Time-Sensitive, March 2026: 20 (budget, election-specific questions)
- GK SME, Evergreen, March 2026: 20 (historical/polity/geography questions)

These targets appear in D-01's Coverage Gaps tab for GK SME as a freshness indicator — showing not just how many questions exist in a topic, but how many are fresh vs expiring.

---

### Section 9 — SME View (Restricted)

**Trigger:** SME accesses `/content/director/calendar/?sme_view=1` or is linked here from D-01.

**What the SME sees (own data only):**
- Current month quota: "Your March 2026 quota: 120 questions"
- Progress: "Published: 47 · In Pipeline: 31 · Remaining to produce: 42"
- Content type target breakdown (if set by Director for this SME)
- Content Freeze Status: "SSC CGL: Frozen until 20 March 2026" — for each exam type relevant to this SME's subject
- Upcoming exam dates for this SME's exam types (next 3 months)

**What the SME does NOT see:**
- Other SMEs' quotas or production data
- Total production targets
- Director's planning notes
- The full quota config table

---

## 5. Data Models

### `content_sme_quota`
| Field | Type | Notes |
|---|---|---|
| `sme_user_id` | FK → auth.User | — |
| `month` | date | First day of month (2026-03-01) |
| `target_count` | int | Total questions for this month |
| `evergreen_target` | int | Nullable — optional content type breakdown |
| `current_affairs_target` | int | Nullable |
| `time_sensitive_target` | int | Nullable |
| `set_by` | FK → auth.User | Director who set this |
| `set_at` | timestamptz | — |

### `content_exam_freeze`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `exam_type_code` | varchar | SSC_CGL · etc. |
| `exam_name` | varchar | Display name |
| `exam_date` | date | Official exam date |
| `freeze_start` | date | From this date: no new submissions for this exam type |
| `freeze_end` | date | Auto = exam_date; can be overridden if freeze lifted early |
| `status` | varchar | Future · Active · Lifted |
| `lifted_early_by` | FK → auth.User | Nullable |
| `lifted_at` | timestamptz | Nullable |

### `content_calendar_event`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `event_date` | date | — |
| `event_type` | varchar | ExamDate · FreezeDate · ProductionMilestone · FreezeLift |
| `exam_type_code` | varchar | Nullable |
| `label` | varchar | Display text for calendar cell badge |
| `created_by` | FK → auth.User | — |

### `content_sme_subject_assignment`
| Field | Type | Notes |
|---|---|---|
| `sme_user_id` | FK → auth.User | — |
| `subject_id` | FK → content_taxonomy_subject | — |
| `exam_type_code` | varchar | — |
| `is_primary` | boolean | Primary or backup assignment |
| `assigned_by` | FK → auth.User | Director |
| `assigned_at` | timestamptz | — |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Full page access | `PermissionRequiredMixin(permission='content.manage_calendar')` — Role 18 |
| SME view | `permission='content.view_own_quota'` — Roles 19–27. `?sme_view=1` parameter triggers SME-scoped view; server validates the user's role before rendering SME-only subset. |
| Freeze lift action | Role 18 only |
| Quota edit | Role 18 only — SMEs can see their quota but cannot change it |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Director sets quota to 0 for a month | Allowed — "0 quota" means the SME is not expected to produce content this month (e.g. on leave). D-01 KPI strip shows "No quota set (0)" in grey rather than red. |
| Exam postponed after freeze is active | Director clicks "Lift Freeze Early" + updates the Exam Date in the Upcoming Exam Dates panel. SMEs can immediately submit for that exam type again. D-02 real-time check picks up the lifted freeze within milliseconds. |
| Director tries to set a content freeze end date before its start date | Date picker validation: freeze_end must be ≥ freeze_start. Client-side validation + server-side validation. |
| SME accesses the full director calendar URL (without `?sme_view=1`) | Permission check returns 403 — director calendar URL requires `content.manage_calendar` permission which SMEs don't have. |
| Monthly quota notifications fail to deliver (in-app notification service down) | Quota is saved successfully. Notification delivery is best-effort (Celery task). If delivery fails, it's retried twice. After 2 retries, failure is logged — SME sees the updated quota on their next D-01 load via the ORM-level KPI strip query. |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-02 Question Editor | D-10 → D-02 | Content freeze dates (real-time check on Submit) | `content_exam_freeze` direct ORM read — no cache |
| D-04 Approval Queue | D-10 → D-04 | Content freeze dates (check on Approve+Publish) | Same `content_exam_freeze` ORM read |
| D-01 SME Dashboard | D-10 → D-01 | Monthly quota target for SME KPI strip | `content_sme_quota` ORM read |
| D-05 Director Dashboard | D-05 reads D-10 | Upcoming exam dates for SME Productivity section | `content_exam_freeze` + `content_calendar_event` |
| D-14 Syllabus Coverage | D-10 → D-14 | Exam date config propagated to D-14 Exam Date Config panel | Shared `content_exam_freeze` table |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- **Quota Config Table:** Placeholder "Filter SMEs…". Instant filter by role label (typically < 15 rows, no debounce needed).
- **Upcoming Exam Dates panel:** Placeholder "Search exam dates…". Searches: exam name, exam type code.
- **Active Freezes table:** Placeholder "Filter freezes…". Searches: exam type code, exam name.

### Sortable Columns — Quota Config Table
| Column | Default Sort |
|---|---|
| SME Role | ASC (alphabetical) — default |
| Monthly Target | DESC |
| Quota Achieved % (current month) | ASC (most behind first) |

### Sortable Columns — Upcoming Exam Dates Table
| Column | Default Sort |
|---|---|
| Exam Date | **ASC (soonest first)** — default |
| Content Freeze Date | ASC |
| Status | Custom: Active Freeze → Future → Lifted |

### Pagination
- Quota Config Table: typically < 15 rows (one per SME). Show all, no pagination.
- Upcoming Exam Dates: 25 rows, numbered controls (can grow over time).
- Active Freezes: 25 rows, numbered controls.

### Empty States
| Section | Heading | Subtext |
|---|---|---|
| Calendar — no exam dates | "No exam dates configured" | "Add upcoming exam dates to see freeze dates and production peaks on the calendar." |
| Quota Config — no SMEs assigned | "No SMEs configured" | "Assign SMEs to subjects in the Reviewer Assignments page first." |
| Active Freezes — none | "No active content freezes" | "Content freezes are activated automatically on their configured start dates." |

### Toast Messages
| Action | Toast |
|---|---|
| Quota saved | ✅ "Quota updated — SME notified" (Success 4s) |
| Quota notification failed to deliver | ⚠ "Quota saved — notification to SME could not be delivered. They'll see the update on next login." (Warning 8s) |
| Add exam date | ✅ "Exam date added" (Success 4s) |
| Edit exam date | ✅ "Exam date updated" (Success 4s) |
| Lift freeze early | ✅ "Content freeze lifted for {Exam Type} — SMEs can now submit questions" (Success 4s) |
| Freeze date validation fail | ❌ "Freeze date must be before the exam date" (Error inline) |
| Unsaved quota cells | ⚠ "You have unsaved quota changes. Save before navigating away." (Warning — fires on tab switch or page unload) |

### Loading States
- Calendar grid: shimmer placeholder (7×5 grid of grey day cells) on month navigation.
- Actual vs Target chart: chart-area shimmer rectangle while data loads.
- Quota Config Table: 10-row skeleton on page load.
- Upcoming Exam Dates: 5-row skeleton on tab open.

### Calendar Grid — Interaction Detail
- Day cell click: opens a right-side **Day Detail Panel** (360px width, not a full drawer). Panel shows: date heading, published count breakdown by subject, active freezes that day, custom milestone notes.
- Day Detail Panel close: X button or click outside.
- **Year View:** 12 small month grids (2-column layout). Each day cell shows a coloured dot (green/amber/red based on production vs target). No text — click any day → opens month view for that month with that day highlighted.
- **Mobile Year View:** 4 mini months visible at once. Horizontal scroll to see all 12 months.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Calendar grid full month. Quota table side-by-side with chart. Panels at right. |
| Tablet | Calendar grid slightly smaller. Quota table: horizontal scroll (month columns narrow). Chart below table. |
| Mobile | Calendar grid: single-week view (7 cells). Swipe left/right to navigate weeks. Month jump: month picker dropdown. Quota table: SME name + current month target + action — other month columns hidden (horizontal scroll). |

### SME View (`?sme_view=1`) — UI Details
- Header: "Your Quota & Exam Schedule" (not the Director title).
- No calendar grid shown — SME sees a structured list view instead (simpler, no production bar charts).
- Quota progress: ring chart (donut) — Published / In Pipeline / Remaining to produce. Colour: green / amber / grey.
- Content Freeze list: table with Exam Type, Freeze Status (Active/Future/Lifted), Freeze Until date. No edit controls.
- Upcoming Exam Dates: card list (next 3 exams for this SME's subjects) — exam name, date, days until.

### Form Validation — Add Exam Date Modal
| Field | Validation |
|---|---|
| Exam Name | Required, ≥ 5 chars |
| Exam Type | Required (dropdown) |
| Exam Date | Required, must be ≥ today |
| Content Freeze Date | Required, must be < Exam Date |

"Add Exam" button disabled until all fields valid. Freeze date picker auto-suggests `exam_date - 21 days` as default.

### Role-Based UI
- Quota Config Table edit: Director only. SMEs see own quota row as read-only.
- Add Exam Date / Edit / Lift Freeze: Director only.
- Content Type Target popover: Director only (hover edit icon).
- Year View toggle: available to both Director and SME (SME sees simplified year view).

---

*Page spec complete.*
*Next file: `d-11-published-bank.md`*
