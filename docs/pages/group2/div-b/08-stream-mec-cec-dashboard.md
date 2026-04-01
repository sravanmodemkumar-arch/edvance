# 08 — Stream Coordinator MEC/CEC Dashboard

> **URL:** `/group/acad/stream/mec-cec/`
> **File:** `08-stream-mec-cec-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Stream Coordinator — MEC/CEC (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Stream Coordinator covering the MEC (Mathematics, Economics, Commerce) and CEC (Civics, Economics, Commerce) streams. This role owns the academic health of both commerce-oriented streams across all branches in the group — syllabus adherence, teacher load, exam outcomes, and content gaps are visible on a single screen.

The MEC/CEC Coordinator bridges the gap between the more science-heavy MPC/BiPC streams and the humanities. Students in these streams often transition to CA, CS, law, or civil services careers, and the coordinator is responsible for ensuring appropriate preparation pathways are maintained across all branches, regardless of whether a branch offers MEC, CEC, or both.

The dashboard presents data filtered exclusively to MEC and CEC streams. No MPC, BiPC, or Foundation data is surfaced here. Where a branch does not offer MEC/CEC, it appears in a "non-participating branches" note at the bottom of relevant tables.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Stream Coordinator — MEC/CEC | G3 | Full — all sections, all actions | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | Full read + override actions | CAO can access all stream dashboards |
| Group Academic Director | G3 | Read — all widgets | Can view but cannot post stream announcements on behalf of this role |
| Group Curriculum Coordinator | G2 | Read — syllabus and content sections only | No access to exam or teacher sections |
| Group Exam Controller | G3 | Read — upcoming exams section only | Exam scheduling cross-reference |
| Group Results Coordinator | G3 | Read — score trend widget only | Results coordination visibility |
| Group Stream Coordinator — MPC | G3 | — | Has own dashboard `/group/acad/stream/mpc/` |
| Group Stream Coordinator — BiPC | G3 | — | Has own dashboard `/group/acad/stream/bipc/` |
| Group JEE/NEET Integration Head | G3 | — | Has own dashboard |
| Group IIT Foundation Director | G3 | — | Has own dashboard |
| Group Olympiad & Scholarship Coord | G3 | Read — participation widget for commerce olympiads only | Cross-division view |
| Group Special Education Coordinator | G3 | — | Has own dashboard |
| Group Academic MIS Officer | G1 | Read-only — all sections | No write controls visible |
| Group Academic Calendar Manager | G3 | Read — upcoming exams timeline only | Calendar coordination |

> **Access enforcement:** Django view decorator `@require_role('stream_coord_mec_cec')`. CAO, Academic Director, and MIS Officer are admitted via role-union check. All other roles are redirected to their own dashboard.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Stream Coordinator  ›  MEC / CEC Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]                          [New Announcement ✉]  [Settings ⚙]
Group Stream Coordinator — MEC / CEC  ·  Last login: [date time]  ·  [Group Logo]
```

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch name + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all →" link to full alerts list

**Alert trigger examples:**
- Syllabus completion < 60% in Economics or Commerce in any branch with < 4 weeks to term-end exam
- No lesson plans submitted for a core MEC/CEC subject in any branch for > 14 days
- Branch offering MEC/CEC has zero registered students in that stream
- Teacher vacancy — a core MEC/CEC subject has no assigned teacher in any branch
- Content gap alert: topic has zero study material in group library for > 30 days

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| MEC/CEC Enrollment | Total students in MEC + CEC streams across all branches + trend ↑/↓ | Stream enrollment aggregation | Green if ≥ target · Yellow 80–99% · Red < 80% | → Branch Participation detail (Section 5.5) |
| Avg Syllabus Completion | `XX%` combined across MEC + CEC subjects this term | Syllabus tracking module | Green ≥ 85% · Yellow 70–85% · Red < 70% | → Stream Syllabus Completion (Section 5.1) |
| Stream Avg Score | Group avg marks across last completed MEC/CEC group exam | Results module | Green ≥ 65% · Yellow 50–65% · Red < 50% | → Score Trend (Section 5.2) |
| Lesson Plan Compliance | `XX%` branches submitted plans for all core subjects | Lesson plan module | Green ≥ 90% · Yellow 75–90% · Red < 75% | → Lesson Plan Heatmap (Section 5.4) |
| Upcoming Stream Exams | Count of MEC/CEC exams in next 14 days | Exam calendar | Badge always shown; pulsing if any exam < 48 hrs away | → Upcoming Exams timeline (Section 5.6) |
| Content Gap Alerts | Count of topics with no study material in group library | Content library | Green = 0 · Yellow 1–5 · Red > 5 | → Content Gap Alerts (Section 5.7) |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Stream Syllabus Completion

> Per-subject syllabus completion across all branches, filtered to MEC and CEC streams only.

**Display:** Per-subject horizontal progress bars, grouped by stream (MEC group, then CEC group).

**MEC subjects tracked:** Mathematics · Economics · Commerce · Business Studies (optional elective)

**CEC subjects tracked:** Civics / Political Science · Economics · Commerce · Business Studies

**Progress bar columns:**

| Column | Description |
|---|---|
| Subject | Subject name with stream badge (MEC / CEC) |
| Branches Reporting | Count of branches that have submitted progress vs total offering this stream |
| Group Avg Completion | Weighted average % across all reporting branches |
| Progress Bar | Visual bar — green ≥ 85% · amber 70–85% · red < 70% |
| Lowest Branch | Branch name with lowest completion % — links to that branch |
| Actions | [View Detail →] opens subject-branch breakdown drawer |

**Drawer: `syllabus-subject-detail`**
- Width: 560px
- Content: Branch-by-branch table for selected subject — Branch Name · Completion % · Topics Done · Topics Remaining · Last Updated
- Filter within drawer: Sort by completion % ascending
- HTMX: `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/syllabus/{subject_id}/"` `hx-target="#drawer-body"`

**HTMX:** Section loads via `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/syllabus/"` on page load · `hx-target="#syllabus-section"` · `hx-trigger="load"`.

---

### 5.2 Stream Average Score Trend

> Term-over-term group average score per MEC/CEC subject — tracks academic trajectory.

**Display:** Line chart (Chart.js 4.x)

**X-axis:** Last 6 terms (e.g., Term 1 2023–24 → Term 2 2025–26)

**Y-axis:** Average score percentage (0–100%)

**Series:** One line per subject — Mathematics (blue) · Economics (green) · Commerce (orange) · Civics (purple) · Business Studies (grey dashed — where applicable)

**Tooltip:** Term name · Subject · Group Avg · Highest branch avg · Lowest branch avg · No. of branches reported

**Legend:** Bottom horizontal. Colorblind-safe palette.

**Filter within chart card:** Stream toggle (All / MEC only / CEC only) · Subject multi-select · Branch filter (to isolate one branch's trend)

**Export:** "Export PNG" button top-right of chart card.

**Empty state:** "No result data available for the selected term range. Ensure branch results have been uploaded and moderated."

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/score-trend/"` · filter changes trigger `hx-get` with params · `hx-target="#score-trend-chart"` · `hx-swap="innerHTML"`.

---

### 5.3 Teacher Load by Subject

> Identifies understaffed subjects across branches in the MEC/CEC stream.

**Display:** Grouped bar chart (Chart.js 4.x)

**X-axis:** Subjects (Mathematics, Economics, Commerce, Civics, Business Studies)

**Y-axis:** Number of teachers per subject across the group

**Bar grouping:** Per branch (each branch = one bar colour, legend)

**Tooltip:** Branch · Subject · Teacher count · Students per teacher ratio · Flag if ratio > 40:1

**Alert overlay:** Red exclamation badge on any bar where student-teacher ratio > 40:1 or teacher count = 0

**Actions:** [View Teacher List →] opens teacher-assignment drawer for that subject + branch.

**Drawer: `teacher-load-detail`**
- Width: 480px
- Content: Teacher name · Qualification · Classes assigned · Weekly periods · Contact email
- Action button (G3+): [Request Additional Teacher] → raises HR request ticket

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/teacher-load/"` · `hx-target="#teacher-load-section"` · `hx-trigger="load"`.

---

### 5.4 Lesson Plan Submission Heatmap

> Branch × Subject matrix showing whether lesson plans have been submitted this term.

**Display:** Heatmap grid

**Rows:** Branches offering MEC or CEC (sorted alphabetically)

**Columns:** Subjects (Mathematics, Economics, Commerce, Civics, Business Studies)

**Cell colours:**
- Dark green: Plan submitted and approved
- Light green: Plan submitted, pending review
- Amber: Plan submitted but returned with feedback — needs resubmission
- Red: No plan submitted for this term
- Grey: Branch does not offer this subject (stream not active)

**Interaction:** Click any cell → opens plan detail drawer or "no plan" prompt with [Send Reminder] action.

**Drawer: `lesson-plan-cell-detail`**
- Width: 480px
- Tabs: Plan Details · Feedback · History
- Action (G3): [Approve] [Return with Feedback] [Send Reminder to Branch]

**Bulk action (row level):** [Send Reminder to All Missing Plans] → POST to reminder endpoint for that branch.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/lesson-plans/heatmap/"` · `hx-target="#lesson-plan-heatmap"` · `hx-trigger="load"`.

---

### 5.5 Branch Participation — MEC/CEC

> Which branches offer MEC, CEC, both, or neither — with student counts.

**Display:** Table

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch Name | Text + link | ✅ | Opens Branch Detail (div-a page 10) |
| City | Text | ✅ | |
| MEC Offered | Badge | ✅ | Yes / No |
| MEC Students | Number | ✅ | 0 shown in red if offered but zero enrolled |
| CEC Offered | Badge | ✅ | Yes / No |
| CEC Students | Number | ✅ | 0 shown in red if offered but zero enrolled |
| Total Stream Students | Number | ✅ | MEC + CEC combined |
| Top Branch Subject | Text | ❌ | Subject where branch avg is highest |
| Status | Badge | ✅ | Active · No enrollment · Stream not configured |

**Filters:** Stream filter (MEC only / CEC only / Both / Neither) · Enrollment status · City/District.

**Default sort:** Total stream students descending.

**Row action:** [View Stream Detail →] → goes to branch-level stream page (branch portal, read-only for group coordinator).

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/branches/"` · `hx-target="#branch-participation-section"` · search/filter triggers fresh `hx-get`.

---

### 5.6 Upcoming Stream Exams

> All MEC/CEC exams scheduled in the next 14 days across all branches.

**Display:** Timeline (vertical, day-by-day) — maximum 14 day look-ahead.

**Timeline item fields:** Date badge · Exam name · Type (Unit Test / Mid-term / Mock / Group) · Stream (MEC / CEC / Both) · Class (Intermediate I / II) · Branches count · Paper Status badge (Approved / Pending / Not Assigned) · [View →]

**Colour coding:** Exam type — Unit Test (blue) · Mid-term (orange) · Annual (red) · Mock (grey) · Olympiad prep (purple)

**Alert:** Any exam < 48 hrs away with paper status "Not Assigned" → red alert strip above timeline.

**Empty state:** "No MEC/CEC exams scheduled in the next 14 days." — no timeline rendered, just message and calendar icon.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/upcoming-exams/"` · `hx-trigger="load"` · `hx-target="#upcoming-exams-section"`.

---

### 5.7 Content Gap Alerts

> Topics within the MEC/CEC curriculum that have zero study material in the group content library.

**Display:** Alert list (card-style, scrollable)

**Card fields:** Subject name · Topic name · Stream (MEC / CEC / Both) · Class level · Days since flagged · [Upload Content →] (opens content upload drawer) · [Assign to Coordinator →]

**Severity:** Red card if gap > 30 days · Amber if 15–30 days · Yellow if < 15 days

**Sorting:** Most critical (longest gap) first.

**Actions:**
- [Upload Content →]: opens content upload drawer pre-filled with subject, topic, stream
- [Assign →]: POST to assign this topic to a designated content creator
- [Mark as External Resource →]: mark that an external link covers this topic (resolves alert)

**Drawer: `content-upload-gap`**
- Width: 640px
- Pre-fills: Subject, topic, stream, class
- Tabs: File/Link · Metadata · Access Scope · Preview · Submit
- HTMX: `hx-post="/api/v1/group/{group_id}/acad/content-library/"` on submit

**Empty state:** "No content gaps detected — all topics have at least one resource in the library." — green checkmark illustration.

---

### 5.8 Stream Announcement Drafts

> Communications to MEC/CEC stream teachers across branches that have not yet been sent.

**Display:** Draft list (table with minimal columns)

**Columns:** Draft title · Audience (MEC teachers / CEC teachers / Both) · Created by · Created at · [Edit →] [Send →] [Delete]

**[Send] action:** Confirmation modal → POST to send endpoint → toast success → row removed from drafts.

**[+ New Announcement] button** (top-right of section card): Opens announcement composer drawer.

**Drawer: `stream-announcement-compose`**
- Width: 640px
- Fields: Title · Body (rich text) · Audience (MEC / CEC / All stream teachers) · Delivery channel (Email · WhatsApp · Portal notification · All) · Schedule (send now / schedule for date+time)
- Preview pane on right side

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/announcements/drafts/"` · `hx-target="#announcement-drafts-section"` · Send action: `hx-post` → `hx-target="#announcement-drafts-section"` `hx-swap="innerHTML"`.

---

### 5.9 Top & Bottom Performing Branches (Stream)

> Quick snapshot of best and worst branches by MEC/CEC stream average score.

**Display:** Split table — Top 5 branches on left column, Bottom 5 on right column.

**Columns (each half):** Rank · Branch Name · City · Stream Avg Score · Delta from last term (↑/↓) · [View →]

**Top 5:** Green row highlight for rank #1.

**Bottom 5:** Red row highlight for rank 5 of bottom (worst performer). Amber for others.

**Tooltip on delta:** "Improved by X% from [previous term]" or "Declined by X% from [previous term]".

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/branch-ranking/"` · `hx-trigger="load"` · `hx-target="#branch-ranking-section"`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `syllabus-subject-detail`
- **Trigger:** [View Detail →] in Section 5.1 progress bar row
- **Width:** 560px
- **Content:** Branch-by-branch syllabus table for selected subject; sortable by completion %
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/syllabus/{subject_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.2 Drawer: `teacher-load-detail`
- **Trigger:** [View Teacher List →] on chart bar click in Section 5.3
- **Width:** 480px
- **Content:** Teacher list for selected subject + branch; [Request Additional Teacher] action
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/teachers/?subject={id}&branch={id}"` `hx-target="#drawer-body"`

### 6.3 Drawer: `lesson-plan-cell-detail`
- **Trigger:** Heatmap cell click in Section 5.4
- **Width:** 480px
- **Tabs:** Plan Details · Feedback · History
- **Actions (G3):** [Approve] [Return with Feedback] [Send Reminder]
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mec-cec/lesson-plans/{branch_id}/{subject_id}/"` `hx-target="#drawer-body"`

### 6.4 Drawer: `content-upload-gap`
- **Trigger:** [Upload Content →] in Section 5.7 alert card
- **Width:** 640px
- **Tabs:** File/Link · Metadata · Access Scope · Preview · Submit
- **HTMX:** `hx-post="/api/v1/group/{group_id}/acad/content-library/"` on submit

### 6.5 Drawer: `stream-announcement-compose`
- **Trigger:** [+ New Announcement] in Section 5.8 or [Edit →] on draft row
- **Width:** 640px
- **Fields:** Title · Body (rich text) · Audience · Delivery channel · Schedule
- **HTMX:** POST to `/api/v1/group/{group_id}/acad/stream/mec-cec/announcements/` on send

### 6.6 Modal: `send-announcement-confirm`
- **Trigger:** [Send →] on draft row in Section 5.8
- **Width:** 400px
- **Content:** "Send '[Announcement Title]' to all [MEC/CEC] stream teachers?" + recipient count + delivery channel summary
- **Buttons:** [Confirm Send] (primary) + [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/stream/mec-cec/announcements/{id}/send/"` → toast success

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Lesson plan approved | "Lesson plan approved for [Subject] — [Branch Name]" | Success (green) | 4s auto-dismiss |
| Lesson plan returned | "Feedback sent to [Branch Name] for [Subject]" | Info (blue) | 4s |
| Reminder sent | "Reminder sent to [Branch Name] for missing lesson plans" | Info | 4s |
| Announcement sent | "Announcement sent to [N] MEC/CEC stream teachers" | Success | 5s |
| Content uploaded | "Content uploaded and submitted for review" | Success | 4s |
| Content gap marked external | "Topic marked as covered by external resource" | Info | 4s |
| KPI load error | "Failed to load KPI data. Retrying…" | Error (red) | Manual dismiss |
| Teacher request submitted | "Additional teacher request raised for [Subject] — [Branch]" | Success | 5s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No branches offer MEC/CEC | Building outline | "No MEC/CEC stream configured" | "No branches in this group currently offer MEC or CEC stream" | — |
| No syllabus data for term | Document outline | "Syllabus data not available" | "No branches have reported syllabus progress for this term yet" | [Refresh] |
| No upcoming exams | Calendar outline | "No exams in the next 14 days" | "No MEC/CEC exams are scheduled for the next two weeks" | — |
| No content gaps | Checkmark circle | "All topics covered" | "Every MEC/CEC topic has at least one resource in the library" | — |
| No announcement drafts | Envelope outline | "No drafts saved" | "Start composing a new announcement for your stream teachers" | [+ New Announcement] |
| No result data (chart) | Bar chart outline | "Score data unavailable" | "No result data for the selected term range" | [Refresh] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + syllabus progress bars (4 rows) + chart placeholder |
| Syllabus section load | Inline skeleton rows — 6 subject rows, same column widths |
| Score trend chart load | Spinner centred in chart area |
| Teacher load chart load | Spinner centred in chart area |
| Heatmap load | Grey placeholder grid matching branch × subject dimensions |
| Branch table fetch (filter/sort) | Inline skeleton rows — 5 rows |
| Drawer open | Skeleton rows inside drawer body |
| Announcement send | Spinner inside [Confirm Send] button + button disabled |
| KPI auto-refresh | Subtle shimmer over existing card values |

---

## 10. Role-Based UI Visibility

| Element | Stream Coord MEC/CEC (G3) | CAO (G4) | Academic Director (G3) | MIS Officer (G1) | All others |
|---|---|---|---|---|---|
| Page itself | ✅ Rendered | ✅ Rendered (override) | ✅ Read-only | ✅ Read-only | ❌ Redirected |
| Alert Banner | ✅ Shown | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| [Approve] lesson plan | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Return with Feedback] | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Send Reminder] button | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [+ New Announcement] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Send →] on draft row | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Request Additional Teacher] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Upload Content →] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/dashboard/` | JWT (G3+) | Full page data — KPIs, syllabus, alerts |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/kpi-cards/` | JWT (G3+) | KPI card values only (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/syllabus/` | JWT (G3+) | Per-subject syllabus completion |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/syllabus/{subject_id}/` | JWT (G3+) | Branch-by-branch breakdown for one subject |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/score-trend/` | JWT (G3+) | Term-over-term score data for chart |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/teacher-load/` | JWT (G3+) | Teachers per subject per branch |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/lesson-plans/heatmap/` | JWT (G3+) | Heatmap matrix data |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/lesson-plans/{branch_id}/{subject_id}/` | JWT (G3+) | Individual plan detail |
| POST | `/api/v1/group/{group_id}/acad/stream/mec-cec/lesson-plans/{plan_id}/approve/` | JWT (G3) | Approve lesson plan |
| POST | `/api/v1/group/{group_id}/acad/stream/mec-cec/lesson-plans/{plan_id}/return/` | JWT (G3) | Return plan with feedback |
| POST | `/api/v1/group/{group_id}/acad/stream/mec-cec/lesson-plans/remind/` | JWT (G3) | Send reminder to branch |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/branches/` | JWT (G3+) | Branch participation table |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/upcoming-exams/` | JWT (G3+) | Next 14 days exam list |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/content-gaps/` | JWT (G3+) | Topics with no content |
| POST | `/api/v1/group/{group_id}/acad/content-library/` | JWT (G3) | Upload content (shared endpoint) |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/branch-ranking/` | JWT (G3+) | Top/bottom branch ranking |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/announcements/drafts/` | JWT (G3) | Draft announcements list |
| POST | `/api/v1/group/{group_id}/acad/stream/mec-cec/announcements/` | JWT (G3) | Save or send announcement |
| POST | `/api/v1/group/{group_id}/acad/stream/mec-cec/announcements/{id}/send/` | JWT (G3) | Send a saved draft |
| GET | `/api/v1/group/{group_id}/acad/stream/mec-cec/teachers/` | JWT (G3+) | Teacher list with subject/branch filter |
| POST | `/api/v1/group/{group_id}/acad/stream/mec-cec/teachers/request/` | JWT (G3) | Raise additional teacher request |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `/api/.../mec-cec/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Syllabus section load | `load` | GET `/api/.../mec-cec/syllabus/` | `#syllabus-section` | `innerHTML` |
| Subject detail drawer open | `click` | GET `/api/.../syllabus/{subject_id}/` | `#drawer-body` | `innerHTML` |
| Score trend filter change | `change` | GET `/api/.../score-trend/?stream={}&subjects={}&branch={}` | `#score-trend-chart` | `innerHTML` |
| Heatmap load | `load` | GET `/api/.../lesson-plans/heatmap/` | `#lesson-plan-heatmap` | `innerHTML` |
| Heatmap cell click | `click` | GET `/api/.../lesson-plans/{branch_id}/{subject_id}/` | `#drawer-body` | `innerHTML` |
| Approve lesson plan | `click` | POST `/api/.../lesson-plans/{plan_id}/approve/` | `#lesson-plan-heatmap` | `innerHTML` |
| Send reminder | `click` | POST `/api/.../lesson-plans/remind/` | `#toast-container` | `afterbegin` |
| Branch table search | `input delay:300ms` | GET `/api/.../branches/?q={val}` | `#branch-participation-section` | `innerHTML` |
| Branch table filter | `click` on Apply | GET `/api/.../branches/?stream={}&city={}` | `#branch-participation-section` | `innerHTML` |
| Upcoming exams load | `load` | GET `/api/.../upcoming-exams/` | `#upcoming-exams-section` | `innerHTML` |
| Send announcement confirm | `click` | POST `/api/.../announcements/{id}/send/` | `#announcement-drafts-section` | `innerHTML` |
| Branch ranking load | `load` | GET `/api/.../branch-ranking/` | `#branch-ranking-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
