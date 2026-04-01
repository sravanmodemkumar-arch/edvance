# 07 — Stream Coordinator BiPC Dashboard

> **URL:** `/group/acad/stream/bipc/`
> **File:** `07-stream-bipc-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Stream Coordinator — BiPC (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Stream Coordinator for BiPC (Biology, Physics, Chemistry) (G3). This role is responsible for the academic quality of the BiPC stream across all branches in the group. Their scope is focused: everything on this dashboard is filtered exclusively to BiPC data. They do not see MPC or other stream data on this page.

The BiPC Stream Coordinator manages syllabus delivery for the three core subjects (Biology, Physics, Chemistry), monitors teacher load and understaffing risks per branch, tracks lesson plan submission quality, reviews upcoming BiPC-stream exams, identifies content gaps in the study material library for BiPC topics, and drafts announcements to BiPC stream teachers across all branches.

BiPC carries additional weight in the group's academic performance because it feeds NEET (National Eligibility cum Entrance Test) aspirants. The coordinator must track not only standard BiPC curriculum delivery but also alignment with NEET syllabus coverage — Biology in particular has a large and specific topic list that must be tracked term-by-term. Physics and Chemistry are shared with MPC but have different depth requirements for NEET-oriented students.

For a large group with BiPC running across most of the 50 branches, with separate Class XI and Class XII sections, and with NEET-integrated students within the BiPC cohort, this dashboard tracks both standard BiPC performance and NEET preparation intersection. All data is hard-filtered to `stream=BiPC` at the API level.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Stream Coord — BiPC | G3 | Full — all BiPC sections, all BiPC actions | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | View only — cannot edit | CAO may view but not act on this role's exclusive dashboard |
| Group Academic Director | G3 | View only | Can view BiPC summary for curriculum oversight |
| Group Curriculum Coordinator | G2 | — | Has own dashboard `/group/acad/curriculum-coord/` |
| Group Exam Controller | G3 | — | Has own dashboard `/group/acad/exam-controller/` |
| Group Results Coordinator | G3 | — | Has own dashboard `/group/acad/results-coord/` |
| Group Stream Coord — MPC | G3 | — | Has own dashboard `/group/acad/stream/mpc/` |
| Group Stream Coord — MEC/CEC | G3 | — | Has own dashboard `/group/acad/stream/mec-cec/` |
| Group JEE/NEET Integration Head | G3 | — | Has own dashboard `/group/acad/jee-neet/` — coordinates with BiPC Coord on NEET alignment |
| Group IIT Foundation Director | G3 | — | Has own dashboard `/group/acad/iit-foundation/` |
| Group Olympiad & Scholarship Coord | G3 | — | Has own dashboard `/group/acad/olympiad/` |
| Group Special Education Coordinator | G3 | — | Has own dashboard `/group/acad/special-ed/` |
| Group Academic MIS Officer | G1 | — | Has own dashboard `/group/acad/mis/` |
| Group Academic Calendar Manager | G3 | — | Has own dashboard `/group/acad/cal-manager/` |

> **Access enforcement:** Django view decorator `@require_role('stream_coord_bipc')`. Any other role hitting this URL is redirected to their own dashboard. CAO and Academic Director landing here see a read-only banner: "Viewing as [Role] — write actions are disabled on this page." All data on this page is hard-filtered to `stream=BiPC` at the API level — no stream selector is exposed.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Division  ›  Stream Coordinator  ›  BiPC Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]                 [Draft Announcement ✉]  [Settings ⚙]
[Group Name] — BiPC Stream Coordinator · Last login: [date time] · [Group Logo]
```

**Stream pill:** A permanent `BiPC` badge in the header subtitle confirms the scoped context.

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel at top of page, above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch name (if applicable) + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all →" links to relevant section

**Alert trigger examples (BiPC-specific):**
- Biology coverage <55% in ≥3 branches with <6 weeks left in term (red — Critical)
- Biology teacher vacant in ≥2 branches (red — Critical — understaffing, NEET impact)
- BiPC exam in <48 hours with no lesson plan submitted for exam topics (red — Critical)
- Chemistry lesson plan submission <60% in any branch (yellow — Warning)
- Content gap: ≥10 BiPC topics with no study material, particularly NEET-weightage topics (yellow — Warning)
- BiPC announcement draft not sent for >7 days (yellow — Warning — communication lapse)
- NEET Biology topic set not aligned with group exam paper (yellow — Warning — coverage mismatch)

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| BiPC Syllabus Coverage | `77%` avg completion across all branches — Biology / Physics / Chemistry combined | Syllabus data (BiPC filter) | Green ≥90% · Yellow 75–89% · Red <75% | → Section 5.1 (Progress Bars) |
| BiPC Avg Score (Latest Exam) | `65.8%` group average across all BiPC branches, most recent BiPC exam | Result data (BiPC filter) | Green ≥70% · Yellow 55–69% · Red <55% | → Section 5.2 (Score Trend Chart) |
| BiPC Teachers (Group Total) | `318` BiPC teachers across all branches · `9` unfilled vacancies | HR data (BiPC filter) | Green = 0 vacancies · Yellow 1–5 · Red >5 | → Section 5.3 (Teacher Load) |
| Lesson Plan Submissions | `68%` branches with ≥90% submission for BiPC subjects | Lesson plan data (BiPC filter) | Green ≥90% · Yellow 70–89% · Red <70% | → Section 5.4 (Heatmap) |
| Upcoming BiPC Exams (14 days) | `4` exams scheduled for BiPC stream in next 14 days | Exam calendar (BiPC filter) | Always informational | → Section 5.6 (Timeline) |
| BiPC Content Gaps | `22` BiPC topics with no study material in library | Content library (BiPC filter) | Green = 0 · Yellow 1–15 · Red >15 | → Section 5.7 (Gap Alerts) |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Stream Syllabus Completion — Per-Subject Progress Bars

> Biology / Physics / Chemistry syllabus completion per branch — the BiPC Coordinator's primary daily signal. Biology carries the most topics (~97 NCERT chapters-equivalent for Class XI+XII) and is tracked most closely.

**Display:** Three subject panels side by side (or stacked on narrow screens), each containing a horizontal bar chart for that subject.

**Panel: Biology**
- Y-axis: Branch names, sorted by completion % ascending (worst first)
- X-axis: 0–100% completion
- Bar colours: Green ≥85% · Amber 70–84% · Red <70%
- Reference line: Expected % at this point in the term (dashed)
- NEET-critical topics indicator: Small NEET icon on branches that have not covered high-weightage NEET Biology topics yet

**Panel: Physics**
- Same layout as Biology
- Note: Physics topics shared with MPC but different depth for NEET vs JEE

**Panel: Chemistry**
- Same layout as Biology
- Note: Chemistry topics shared with MPC but NEET has specific organic/inorganic/physical chemistry weightage

**Tooltip (all panels):** Branch name · Subject · Completion % · Topics covered: X of Y · NEET-weightage topics covered: X of Z · Expected % at this week · Gap vs expected.

**Class filter (above all panels):** Class XI / Class XII / Both — defaults to Both.

**Branch filter:** Multi-select — defaults to All BiPC branches.

**Click on any bar:** Opens branch-subject syllabus detail drawer (560px) — topic-level completion, NEET alignment status, teacher assignment.

**Export (per panel):** "Export PNG" button on each panel.

**Empty state:** "No syllabus data for BiPC [Subject]. Configure the BiPC syllabus in the Syllabus Manager."

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/syllabus-completion/?class={}&branch={}"` on filter change `hx-target="#bipc-syllabus-panels"` `hx-swap="innerHTML"`.

---

### 5.2 Stream Average Score Trend — Line Chart

> Term-over-term group average per subject (Biology, Physics, Chemistry) — is BiPC performance improving or declining? NEET alignment makes score trends particularly important for this stream.

**Display:** Multi-line chart (Chart.js 4.x). X-axis = last 6 terms. Y-axis = group average score %. Three lines: Biology (green), Physics (orange), Chemistry (purple).

**Tooltip:** Term name · Biology avg % · Physics avg % · Chemistry avg % · BiPC composite avg %.

**Reference line:** 60% pass threshold (dashed red horizontal line). Secondary reference: 50% NEET qualifying estimate (dashed grey line).

**Class filter:** Class XI / Class XII / Both.

**Click on any data point:** Opens term-subject detail drawer (480px) — branch-wise scores for that term and subject, min/max/avg, NEET-high-scorer count.

**Export:** "Export PNG" + "Export CSV (raw data)" buttons.

**Empty state:** "No BiPC score trend data. At least 2 terms of exam data required to show a trend."

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/score-trend/?class={}"` on class filter change `hx-target="#bipc-score-trend"` `hx-swap="innerHTML"`.

---

### 5.3 Teacher Load by Subject — Bar Chart

> Teachers per subject (Biology / Physics / Chemistry) per branch — identify understaffed branches. Biology teacher vacancies are particularly critical given the volume of topics.

**Display:** Grouped bar chart (Chart.js 4.x). X-axis = branches. For each branch: 3 bars — Biology (green), Physics (orange), Chemistry (purple). Y-axis = number of teachers.

**Understaffing threshold line:** Minimum expected teachers per subject per branch — typically 2 per subject per class (Biology may require 3 per class for large branches due to practicals coordination).

**Bars below threshold:** Highlighted with a red border.

**Vacancy indicator:** Red "V" label on bars where confirmed vacancy exists (teacher role unfilled).

**Tooltip:** Branch name · Subject · Teacher count · Vacancies · Lab assistants (Biology/Chemistry — relevant for practical coordination) · Minimum required.

**Click on bar:** Opens teacher list drawer (480px) — teachers for that branch and subject: Name, Qualification (B.Sc Biology/M.Sc/MBBS background for Biology, B.Tech/M.Sc for Physics/Chemistry), Experience (years), Rating, Class assigned (XI/XII), Lab/theory split.

**Export:** "Export PNG" button.

**Class filter:** Class XI / Class XII / Both.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/teacher-load/?class={}"` on filter change `hx-target="#bipc-teacher-load"` `hx-swap="innerHTML"`.

---

### 5.4 Lesson Plan Submission — Heatmap

> Branch × Subject coverage for BiPC lesson plans — scoped to BiPC only.

**Display:** Heatmap grid. Rows = Branches. Columns = Biology · Physics · Chemistry (and sub-columns: Class XI / Class XII for each).

**Cell colour logic:**
- Green (`bg-green-500`): Complete — all topics for this subject-class have a plan
- Amber (`bg-yellow-400`): Partial — some topics covered
- Red (`bg-red-500`): No plan — zero plans for this subject-class combination
- Grey (`bg-gray-200`): Not applicable for this branch

**Cell tooltip:** Branch · Subject · Class · Topics with plan: X/Y · NEET-high-weightage topics with plan: A/B · Last uploaded: date · Uploader name.

**NEET alignment overlay (optional toggle):** When enabled, cells show a NEET icon if NEET-critical topics are missing from lesson plans even when overall coverage is green.

**Click on cell:** Opens lesson plan cell detail drawer (560px) — topic list, which have plans, which are missing, NEET-weightage flag per topic.

**[Upload Plan]** button (shown for cells with 0 plans): Opens content upload drawer pre-filtered to BiPC.

**"View Lesson Plan Standards →"** links to `/group/acad/lesson-plans/`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/lesson-plan-heatmap/"` `hx-trigger="load"` `hx-target="#bipc-lesson-heatmap"` `hx-swap="innerHTML"`.

---

### 5.5 Top & Bottom Branches (BiPC) — Split Table

> Branches ranked by BiPC composite average — top 5 on the left, bottom 5 on the right.

**Display:** Side-by-side tables within a single card.

**Columns (each table):** Rank · Branch Name · State · BiPC Composite Avg % · Delta from last term (↑/↓) · Best Subject · Worst Subject · NEET Qualifiers (estimated count based on mock scores) · Quick Link.

**"Quick Link" → [View Branch →]:** Opens branch BiPC detail drawer (560px) — subject-wise breakdown and NEET tracker.

**Default sort:** BiPC Composite Avg descending for Top 5, ascending for Bottom 5.

**Exam selector:** Dropdown of last 5 BiPC group exams — coordinator picks which exam to rank by.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/branch-rankings/?exam={}"` on exam selector change `hx-target="#bipc-rankings-card"` `hx-swap="innerHTML"`.

---

### 5.6 Upcoming BiPC Exams — Timeline

> Exams scheduled for BiPC stream in the next 14 days — exclusively BiPC exams.

**Display:** Vertical timeline — each entry: Date badge · Exam name · Class (XI/XII/Both) · Branch count · Approval status · Paper status · NEET-aligned flag (if this exam includes NEET-pattern questions).

**Status badges:**
- Approval: `Pending Approval` (yellow) · `Approved` (green) · `Live` (blue)
- Paper: `Paper Not Ready` (red) · `Paper Ready` (green) · `Answer Key Pending` (amber)
- NEET-pattern: `NEET Aligned` badge (teal) if paper includes NEET-style MCQs

**Date colour:** Red if <3 days away and paper not approved.

**Filter:** Exam type (Unit Test / Mid-term / Annual / Mock / NEET Practice) — single-select, within card.

**Click on entry:** Opens BiPC exam detail drawer (560px) — exam info, branch list, per-branch readiness, NEET topic coverage in paper.

**"View Full BiPC Exam Calendar →"** links to `/group/acad/exam-calendar/?stream=bipc`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/upcoming-exams/?type={}"` on filter change `hx-target="#bipc-exam-timeline"` `hx-swap="innerHTML"`.

---

### 5.7 Content Gap Alerts — Alert List

> BiPC topics with no study material in the shared content library — Biology has the most topics and therefore the most potential gaps.

**Display:** Alert list. Each item: Red dot · Subject (Biology/Physics/Chemistry) · Topic name · Chapter · Class · NEET-weightage flag (NEET-high if this topic appears frequently in past NEET papers) · Branches affected (count) · [Create Task →] button.

**Sort:** NEET-high topics first, then by subject, then by chapter sequence.

**Filter (within section):** Subject (All / Biology / Physics / Chemistry) · Class (XI / XII / Both) · NEET Weightage (All / NEET High Priority only).

**[Create Task →]:** Opens task assignment modal (420px) — assign to a teacher or branch coordinator to upload study material for this topic. Fields: Assign to, Due date, Priority (auto-set to High for NEET-high topics), Notes.

**Count badge:** Total gap count shown above list — e.g. "22 BiPC topics with no study material (8 are NEET-high priority)."

**Empty state:** "No content gaps. All BiPC topics have at least one study material in the library." — Green shield.

**"View BiPC Content in Library →"** links to `/group/acad/content-library/?stream=bipc`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/content-gaps/?subject={}&class={}&neet={}"` on filter change `hx-target="#bipc-gap-alerts"` `hx-swap="innerHTML"`.

---

### 5.8 Stream Announcement Drafts — Draft List

> BiPC-specific communications drafted for BiPC stream teachers across all branches — not yet sent.

**Display:** List — each item: Draft name · Created date · Last edited · Recipient scope (All BiPC teachers / Specific branches) · [Edit →] [Preview →] [Send Now →] [Delete ✗] buttons.

**[Draft Announcement ✉] header button:** Opens announcement draft drawer (640px) — rich text editor with template options (Exam reminder / Syllabus update / NEET alignment notice / CPD notice / General) + recipient scope + schedule.

**Template option specific to BiPC: "NEET Alignment Notice"** — pre-filled template reminding teachers to ensure NEET-weightage topics are covered in upcoming exam papers and lesson plans. Editable before sending.

**[Send Now →]:** Opens send confirm modal — shows recipient count + preview. POST to send via system notification + WhatsApp (if configured).

**[Schedule →]:** Allows scheduling announcement for a future date/time.

**Empty state:** "No announcement drafts. Click 'Draft Announcement' in the header to create one." — Message icon illustration.

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-subject-syllabus-detail` (from progress bar chart click)
- **Width:** 560px
- **Tabs:** Topics · NEET Alignment · Teacher · Chapter Breakdown
- **Topics tab:** Topic, Chapter, Sequence, Status (Covered/In Progress/Not Started), NEET Weightage (High/Medium/Low/Not in NEET), Expected completion week
- **NEET Alignment tab:** NEET-high topics — Covered: X, Not covered: Y. % NEET syllabus covered for this subject at this branch.
- **Teacher tab:** Teacher name, qualification (degree highlight: MBBS/B.Sc Bio/M.Sc for Biology), topics assigned, topics completed, last lesson update
- **Chapter Breakdown tab:** Chapter-wise % completion bar chart (mini horizontal bars)
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/branch-subject-detail/?branch={}&subject={}&class={}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.2 Drawer: `term-subject-detail` (from Score Trend chart click)
- **Width:** 480px
- **Content:** Branch-wise scores for selected term and subject — sortable table: Branch, Avg %, Pass %, Max score, Min score, NEET-qualifying-range students (≥360/720 equivalent estimate)
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/term-subject-detail/?term={}&subject={}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.3 Drawer: `branch-teacher-list-subject` (from Teacher Load chart click)
- **Width:** 480px
- **Content:** Teachers for selected branch and subject: Name, Qualification (MBBS/B.Sc/M.Sc/PhD for Biology — note: MBBS-background Biology teachers are highlighted for NEET guidance), Experience (years), Current Rating, Classes assigned (XI/XII), Lab/theory split, Practicals coordinator (Y/N)
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/branch-teachers/?branch={}&subject={}&class={}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.4 Drawer: `bipc-lesson-plan-cell-detail` (from heatmap cell)
- **Width:** 560px
- **Tabs:** Topics with Plans · Missing Topics · NEET Gap
- **Topics with Plans tab:** Topic, Subtopics, NEET Weightage, Uploader, Upload date, Download count
- **Missing Topics tab:** Topic, Chapter, Sequence no., NEET Weightage, [Assign Upload Task →]
- **NEET Gap tab:** Topics classified as NEET-high that are missing plans — priority list for urgent action
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/lesson-plan-cell/?branch={}&subject={}&class={}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.5 Drawer: `branch-bipc-detail` (from rankings Quick Link)
- **Width:** 560px
- **Tabs:** Score Summary · Syllabus · NEET Tracker · Teachers
- **Score Summary tab:** Biology, Physics, Chemistry — avg score, pass %, grade band breakdown
- **Syllabus tab:** Per-subject coverage %, NEET-weighted coverage %, topics remaining, completion timeline projection
- **NEET Tracker tab:** Estimated NEET-eligible students based on mock performance (≥360/720 threshold), improvement trend, top 5 NEET aspirants in branch by mock rank
- **Teachers tab:** Count per subject, vacancies, avg rating, MBBS-background teachers count (Biology-specific)
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/branch-detail/{branch_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.6 Drawer: `bipc-exam-detail` (from upcoming exams timeline click)
- **Width:** 560px
- **Tabs:** Exam Info · Branch Readiness · NEET Coverage
- **Exam Info tab:** Name, date, duration, stream, class, branch scope, approval status
- **Branch Readiness tab:** Per-branch readiness table — Hall assigned, Invigilators confirmed, Paper received, Last confirmed
- **NEET Coverage tab:** (Shown only for NEET-aligned exams) — which NEET chapters/topics this paper covers, % of NEET syllabus tested by this paper
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/bipc/exam-detail/{exam_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.7 Drawer: `announcement-draft` (from [Draft Announcement ✉] header)
- **Width:** 640px
- **Tabs:** Compose · Recipients · Schedule · Preview
- **Compose tab:** Template selector (Exam Reminder / Syllabus Update / NEET Alignment Notice / CPD Notice / General) · Subject line · Body (rich text editor) · Attachments (PDF only, max 5MB)
- **Recipients tab:** Scope (All BiPC teachers / Specific branches / Specific class — XI/XII) · Estimated recipients count shown live
- **Schedule tab:** Send now / Schedule for (date + time picker, IST) / Save as draft
- **Preview tab:** Renders as it will appear in notification system + WhatsApp preview
- **HTMX submit:** POST `.../stream/bipc/announcements/` on Send / PUT `.../stream/bipc/announcements/{id}/` on Save Draft

### 6.8 Modal: `send-announcement-confirm`
- **Width:** 400px
- **Content:** "Send announcement to [N] BiPC teachers across [M] branches?"
- **Shows:** Subject line, first 100 chars of body, recipient count, channels (System / WhatsApp)
- **Buttons:** [Send Now] (primary) + [Cancel]

### 6.9 Modal: `content-gap-assign-task`
- **Width:** 420px
- **Pre-filled:** Subject, Topic, Chapter, Class, NEET Weightage (auto-set)
- **Fields:** Assign to (search dropdown — BiPC teachers or branch academic coordinators) · Due date (auto-suggested: 3 days for NEET-high, 7 days for others) · Priority (auto-set: High for NEET-high topics, editable) · Notes (optional)
- **Buttons:** [Create Task] + [Cancel]

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Announcement sent | "BiPC announcement sent to [N] teachers across [M] branches." | Success (green) | 5s |
| Draft saved | "Announcement draft '[Name]' saved." | Success | 4s |
| Draft deleted | "Draft '[Name]' deleted." | Warning | 4s |
| Content gap task created | "Task assigned to [Name] for [Topic] gap in [Subject]." | Success | 4s |
| NEET-high gap task created | "High-priority task assigned for NEET-critical topic [Topic] in [Subject]." | Success (with orange border) | 5s |
| Upload plan submitted | "Lesson plan submitted for review. It will appear in the content library after approval." | Info | 4s |
| KPI load error | "Failed to load BiPC stream data. Retrying…" | Error (red) | Manual dismiss |
| Export triggered | "Export started — download will begin shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No syllabus data | Chart outline | "No BiPC syllabus data" | "BiPC syllabus has not been configured for any branch yet." | [Go to Syllabus Manager] |
| No score trend data | Line chart outline | "No BiPC score trend" | "At least 2 terms of BiPC exam data are required to show a trend." | — |
| No content gaps | Shield check | "No BiPC content gaps" | "Every BiPC topic has at least one study material in the library." | — |
| No NEET-high content gaps | Shield check (teal) | "No NEET-critical gaps" | "All NEET-high-weightage BiPC topics have study material in the library." | — |
| No upcoming exams | Calendar outline | "No BiPC exams in 14 days" | "No BiPC stream exams are scheduled in the next two weeks." | [View Exam Calendar] |
| No announcement drafts | Message outline | "No drafts" | "No announcement drafts saved. Create one using the 'Draft Announcement' button." | [Draft Announcement] |
| No teacher load data | People outline | "No BiPC teacher data" | "Teacher assignments have not been configured for BiPC branches." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + 3 subject panel bars (shimmer each) + score trend placeholder + heatmap grid skeleton |
| KPI auto-refresh | Subtle shimmer over existing card values |
| Syllabus panels filter change | All 3 panels shimmer simultaneously + spinner |
| Score trend chart filter change | Chart area shimmer + centred spinner |
| Teacher load chart filter change | Chart area shimmer + centred spinner |
| Heatmap on load | Grid shimmer until all cell data arrives |
| Branch rankings exam filter change | Table skeleton rows (5 per side) |
| Exam timeline filter change | Shimmer over timeline entries |
| Gap alerts filter change | List shimmer |
| Announcement send | Spinner inside [Send Now] button + button disabled |
| Drawer open (any) | Spinner in drawer body + tab skeletons |
| NEET Tracker tab in branch detail drawer | Spinner within tab body (computation may take a moment) |

---

## 10. Role-Based UI Visibility

| Element | BiPC Stream Coord G3 | CAO G4 (view-only) | Academic Director G3 (view-only) | All other roles |
|---|---|---|---|---|
| Page itself | ✅ Rendered | ✅ Read-only banner | ✅ Read-only banner | ❌ Redirected |
| Alert Banner | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| [Draft Announcement ✉] header button | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Send Now →] on drafts | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Create Task →] in content gaps | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Upload Plan] on heatmap cells | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| NEET Alignment tab in subject detail drawer | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| NEET Tracker tab in branch detail drawer | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| Export buttons on charts | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| NEET Coverage tab in exam detail drawer | ✅ Shown | ✅ Shown | ✅ Shown | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/dashboard/` | JWT (G3) | Full page data (BiPC-scoped) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/kpi-cards/` | JWT (G3) | KPI card values (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/syllabus-completion/` | JWT (G3) | 3-subject syllabus progress bars (class, branch filters) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/branch-subject-detail/` | JWT (G3) | Branch-subject syllabus detail with NEET alignment (drawer) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/score-trend/` | JWT (G3) | Term-over-term BiPC score chart (class filter) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/term-subject-detail/` | JWT (G3) | Term-subject score detail (drawer) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/teacher-load/` | JWT (G3) | Teacher count per subject per branch chart |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/branch-teachers/` | JWT (G3) | Teachers for branch-subject (drawer) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/lesson-plan-heatmap/` | JWT (G3) | BiPC lesson plan heatmap data (with NEET overlay data) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/lesson-plan-cell/` | JWT (G3) | Heatmap cell detail with NEET gap tab (drawer) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/branch-rankings/` | JWT (G3) | Top 5 / Bottom 5 BiPC branches (exam filter) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/branch-detail/{branch_id}/` | JWT (G3) | Branch BiPC detail drawer (with NEET tracker tab) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/upcoming-exams/` | JWT (G3) | Next 14 days BiPC exam timeline (type filter) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/exam-detail/{exam_id}/` | JWT (G3) | BiPC exam detail with NEET coverage tab (drawer) |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/content-gaps/` | JWT (G3) | BiPC topics with no study material (subject, class, neet filters) |
| POST | `/api/v1/group/{group_id}/acad/stream/bipc/content-gaps/assign-task/` | JWT (G3) | Assign gap fill task |
| GET | `/api/v1/group/{group_id}/acad/stream/bipc/announcements/?status=draft` | JWT (G3) | Draft announcements list |
| POST | `/api/v1/group/{group_id}/acad/stream/bipc/announcements/` | JWT (G3) | Create / send announcement |
| PUT | `/api/v1/group/{group_id}/acad/stream/bipc/announcements/{id}/` | JWT (G3) | Update draft announcement |
| DELETE | `/api/v1/group/{group_id}/acad/stream/bipc/announcements/{id}/` | JWT (G3) | Delete draft |
| POST | `/api/v1/group/{group_id}/acad/stream/bipc/announcements/{id}/send/` | JWT (G3) | Send draft announcement |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../stream/bipc/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Syllabus panels filter (class/branch) | `change` | GET `.../stream/bipc/syllabus-completion/?class={}&branch={}` | `#bipc-syllabus-panels` | `innerHTML` |
| Syllabus bar click | `click` | GET `.../stream/bipc/branch-subject-detail/?branch={}&subject={}&class={}` | `#drawer-body` | `innerHTML` |
| Score trend class filter | `change` | GET `.../stream/bipc/score-trend/?class={}` | `#bipc-score-trend` | `innerHTML` |
| Score trend data point click | `click` | GET `.../stream/bipc/term-subject-detail/?term={}&subject={}` | `#drawer-body` | `innerHTML` |
| Teacher load class filter | `change` | GET `.../stream/bipc/teacher-load/?class={}` | `#bipc-teacher-load` | `innerHTML` |
| Teacher load bar click | `click` | GET `.../stream/bipc/branch-teachers/?branch={}&subject={}&class={}` | `#drawer-body` | `innerHTML` |
| Heatmap NEET overlay toggle | `click` | GET `.../stream/bipc/lesson-plan-heatmap/?neet_overlay={}` | `#bipc-lesson-heatmap` | `innerHTML` |
| Heatmap cell click | `click` | GET `.../stream/bipc/lesson-plan-cell/?branch={}&subject={}&class={}` | `#drawer-body` | `innerHTML` |
| Rankings exam filter | `change` | GET `.../stream/bipc/branch-rankings/?exam={}` | `#bipc-rankings-card` | `innerHTML` |
| Exam timeline type filter | `change` | GET `.../stream/bipc/upcoming-exams/?type={}` | `#bipc-exam-timeline` | `innerHTML` |
| Exam entry click (drawer) | `click` | GET `.../stream/bipc/exam-detail/{id}/` | `#drawer-body` | `innerHTML` |
| Content gap filter (subject/class/neet) | `change` | GET `.../stream/bipc/content-gaps/?subject={}&class={}&neet={}` | `#bipc-gap-alerts` | `innerHTML` |
| Announcement send (modal confirm) | `click` | POST `.../stream/bipc/announcements/{id}/send/` | `#announcement-drafts-list` | `innerHTML` |
| Draft delete | `click` | DELETE `.../stream/bipc/announcements/{id}/` | `#announcement-drafts-list` | `innerHTML` |
| Draft announcement create (drawer) | `click` on header button | GET `.../stream/bipc/announcements/create-form/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
