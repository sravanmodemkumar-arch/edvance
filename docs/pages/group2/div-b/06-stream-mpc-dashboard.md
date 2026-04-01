# 06 — Stream Coordinator MPC Dashboard

> **URL:** `/group/acad/stream/mpc/`
> **File:** `06-stream-mpc-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Stream Coordinator — MPC (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Stream Coordinator for MPC (Mathematics, Physics, Chemistry) (G3). This role is responsible for the academic quality of the MPC stream across all branches in the group. Their scope is focused: everything on this dashboard is filtered exclusively to MPC data. They do not see BiPC or other stream data on this page.

The MPC Stream Coordinator manages syllabus delivery for the three core subjects (Mathematics, Physics, Chemistry), monitors teacher load and understaffing risks per branch, tracks lesson plan submission quality, reviews upcoming MPC-stream exams, identifies content gaps in the study material library for MPC topics, and drafts announcements to MPC stream teachers across all branches.

For a large group with MPC running across all 50 branches, with separate Class XI and Class XII sections, and with IIT-JEE aspirants integrated into the MPC curriculum, this dashboard tracks both standard MPC performance and the intersection with JEE preparation. Subject coverage is the primary signal — the coordinator must ensure Physics, Chemistry, and Mathematics are being taught at the right pace across all branches.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Stream Coord — MPC | G3 | Full — all MPC sections, all MPC actions | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | View only — cannot edit | CAO may view but not act on this role's exclusive dashboard |
| Group Academic Director | G3 | View only | Can view MPC summary for curriculum oversight |
| Group Curriculum Coordinator | G2 | — | Has own dashboard `/group/acad/curriculum-coord/` |
| Group Exam Controller | G3 | — | Has own dashboard `/group/acad/exam-controller/` |
| Group Results Coordinator | G3 | — | Has own dashboard `/group/acad/results-coord/` |
| Group Stream Coord — BiPC | G3 | — | Has own dashboard `/group/acad/stream/bipc/` |
| Group Stream Coord — MEC/CEC | G3 | — | Has own dashboard `/group/acad/stream/mec-cec/` |
| Group JEE/NEET Integration Head | G3 | — | Has own dashboard `/group/acad/jee-neet/` — coordinates with MPC Coord |
| Group IIT Foundation Director | G3 | — | Has own dashboard `/group/acad/iit-foundation/` |
| Group Olympiad & Scholarship Coord | G3 | — | Has own dashboard `/group/acad/olympiad/` |
| Group Special Education Coordinator | G3 | — | Has own dashboard `/group/acad/special-ed/` |
| Group Academic MIS Officer | G1 | — | Has own dashboard `/group/acad/mis/` |
| Group Academic Calendar Manager | G3 | — | Has own dashboard `/group/acad/cal-manager/` |

> **Access enforcement:** Django view decorator `@require_role('stream_coord_mpc')`. Any other role hitting this URL is redirected to their own dashboard. CAO and Academic Director landing here see a read-only banner: "Viewing as [Role] — write actions are disabled on this page." All data on this page is hard-filtered to `stream=MPC` at the API level — no stream selector is exposed.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Division  ›  Stream Coordinator  ›  MPC Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]                 [Draft Announcement ✉]  [Settings ⚙]
[Group Name] — MPC Stream Coordinator · Last login: [date time] · [Group Logo]
```

**Stream pill:** A permanent `MPC` badge in the header subtitle confirms the scoped context.

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel at top of page, above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch name (if applicable) + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all →" links to relevant section

**Alert trigger examples (MPC-specific):**
- Mathematics coverage <55% in ≥3 branches with <6 weeks left in term (red — Critical)
- Physics teacher vacant in ≥2 branches (red — Critical — understaffing)
- MPC exam in <48 hours with no lesson plan submitted for exam topics (red — Critical)
- Chemistry lesson plan submission <60% in any branch (yellow — Warning)
- Content gap: ≥10 MPC topics with no study material in library (yellow — Warning)
- MPC announcement draft not sent for >7 days (yellow — Warning — communication lapse)

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| MPC Syllabus Coverage | `79%` avg completion across all branches — Mathematics / Physics / Chemistry combined | Syllabus data (MPC filter) | Green ≥90% · Yellow 75–89% · Red <75% | → Section 5.1 (Progress Bars) |
| MPC Avg Score (Latest Exam) | `68.4%` group average across all MPC branches, most recent MPC exam | Result data (MPC filter) | Green ≥70% · Yellow 55–69% · Red <55% | → Section 5.2 (Score Trend Chart) |
| MPC Teachers (Group Total) | `342` MPC teachers across all branches · `12` unfilled vacancies | HR data (MPC filter) | Green = 0 vacancies · Yellow 1–5 · Red >5 | → Section 5.3 (Teacher Load) |
| Lesson Plan Submissions | `71%` branches with ≥90% submission for MPC subjects | Lesson plan data (MPC filter) | Green ≥90% · Yellow 70–89% · Red <70% | → Section 5.4 (Heatmap) |
| Upcoming MPC Exams (14 days) | `5` exams scheduled for MPC stream in next 14 days | Exam calendar (MPC filter) | Always informational | → Section 5.6 (Timeline) |
| MPC Content Gaps | `18` MPC topics with no study material in library | Content library (MPC filter) | Green = 0 · Yellow 1–15 · Red >15 | → Section 5.7 (Gap Alerts) |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Stream Syllabus Completion — Per-Subject Progress Bars

> Physics / Chemistry / Mathematics syllabus completion per branch — the MPC Coordinator's primary daily signal.

**Display:** Three subject panels side by side (or stacked on narrow screens), each containing a horizontal bar chart for that subject.

**Panel: Mathematics**
- Y-axis: Branch names, sorted by completion % ascending (worst first)
- X-axis: 0–100% completion
- Bar colours: Green ≥85% · Amber 70–84% · Red <70%
- Reference line: Expected % at this point in the term (dashed)

**Panel: Physics**
- Same layout as Mathematics

**Panel: Chemistry**
- Same layout as Mathematics

**Tooltip (all panels):** Branch name · Subject · Completion % · Topics covered: X of Y · Expected % at this week · Gap vs expected.

**Class filter (above all panels):** Class XI / Class XII / Both — defaults to Both.

**Branch filter:** Multi-select — defaults to All MPC branches.

**Click on any bar:** Opens branch-subject syllabus detail drawer (560px) — topic-level completion, teacher assignment, chapter breakdown.

**Export (per panel):** "Export PNG" button on each panel.

**Empty state:** "No syllabus data for MPC [Subject]. Configure the MPC syllabus in the Syllabus Manager."

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/syllabus-completion/?class={}&branch={}"` on filter change `hx-target="#mpc-syllabus-panels"` `hx-swap="innerHTML"`.

---

### 5.2 Stream Average Score Trend — Line Chart

> Term-over-term group average per subject (Mathematics, Physics, Chemistry) — is MPC performance improving or declining?

**Display:** Multi-line chart (Chart.js 4.x). X-axis = last 6 terms. Y-axis = group average score %. Three lines: Mathematics (blue), Physics (orange), Chemistry (green).

**Tooltip:** Term name · Mathematics avg % · Physics avg % · Chemistry avg % · MPC composite avg %.

**Reference line:** 60% pass threshold (dashed red horizontal line).

**Class filter:** Class XI / Class XII / Both.

**Click on any data point:** Opens term-subject detail drawer (480px) — branch-wise scores for that term and subject, min/max/avg.

**Export:** "Export PNG" + "Export CSV (raw data)" buttons.

**Empty state:** "No MPC score trend data. At least 2 terms of exam data required to show a trend."

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/score-trend/?class={}"` on class filter change `hx-target="#mpc-score-trend"` `hx-swap="innerHTML"`.

---

### 5.3 Teacher Load by Subject — Bar Chart

> Teachers per subject (Mathematics / Physics / Chemistry) per branch — identify understaffed branches.

**Display:** Grouped bar chart (Chart.js 4.x). X-axis = branches. For each branch: 3 bars — Mathematics (blue), Physics (orange), Chemistry (green). Y-axis = number of teachers.

**Understaffing threshold line:** Minimum expected teachers per subject per branch (configurable in stream config — typically 2 per subject per class).

**Bars below threshold:** Highlighted with a red border.

**Tooltip:** Branch name · Subject · Teacher count · Vacancies · Minimum required.

**Click on bar:** Opens teacher list drawer (480px) — teachers for that branch and subject: Name, Qualification, Experience (years), Rating, Class assigned (XI/XII), Full-time/Part-time.

**Export:** "Export PNG" button.

**Class filter:** Class XI / Class XII / Both.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/teacher-load/?class={}"` on filter change `hx-target="#mpc-teacher-load"` `hx-swap="innerHTML"`.

---

### 5.4 Lesson Plan Submission — Heatmap

> Branch × Subject coverage for MPC lesson plans — same structure as Curriculum Coordinator's heatmap but scoped to MPC only.

**Display:** Heatmap grid. Rows = Branches. Columns = Mathematics · Physics · Chemistry (and sub-columns: Class XI / Class XII for each).

**Cell colour logic:**
- Green (`bg-green-500`): Complete — all topics for this subject-class have a plan
- Amber (`bg-yellow-400`): Partial — some topics covered
- Red (`bg-red-500`): No plan — zero plans for this subject-class combination
- Grey (`bg-gray-200`): Not applicable for this branch

**Cell tooltip:** Branch · Subject · Class · Topics with plan: X/Y · Last uploaded: date · Uploader name.

**Click on cell:** Opens lesson plan cell detail drawer (560px) — topic list, which have plans, which are missing.

**[Upload Plan]** button (shown for cells with 0 plans): Opens content upload drawer pre-filtered to MPC.

**"View Lesson Plan Standards →"** links to `/group/acad/lesson-plans/`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/lesson-plan-heatmap/"` `hx-trigger="load"` `hx-target="#mpc-lesson-heatmap"` `hx-swap="innerHTML"`.

---

### 5.5 Top & Bottom Branches (MPC) — Split Table

> Branches ranked by MPC composite average — top 5 on the left, bottom 5 on the right.

**Display:** Side-by-side tables within a single card. Same structure as CAO's branch ranking but scoped to MPC.

**Columns (each table):** Rank · Branch Name · State · MPC Composite Avg % · Delta from last term (↑/↓) · Best Subject · Worst Subject · Quick Link.

**"Quick Link" → [View Branch →]:** Opens branch MPC detail drawer (560px) — subject-wise breakdown.

**Default sort:** MPC Composite Avg descending for Top 5, ascending for Bottom 5.

**Exam selector:** Dropdown of last 5 MPC group exams — coordinator picks which exam to rank by.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/branch-rankings/?exam={}"` on exam selector change `hx-target="#mpc-rankings-card"` `hx-swap="innerHTML"`.

---

### 5.6 Upcoming MPC Exams — Timeline

> Exams scheduled for MPC stream in the next 14 days — exclusively MPC exams.

**Display:** Vertical timeline — each entry: Date badge · Exam name · Class (XI/XII/Both) · Branch count · Approval status · Paper status.

**Status badges:**
- Approval: `Pending Approval` (yellow) · `Approved` (green) · `Live` (blue)
- Paper: `Paper Not Ready` (red) · `Paper Ready` (green) · `Answer Key Pending` (amber)

**Date colour:** Red if <3 days away and paper not approved.

**Filter:** Exam type (Unit Test / Mid-term / Annual / Mock) — single-select, within card.

**Click on entry:** Opens MPC exam detail drawer (560px) — exam info, branch list, per-branch readiness (hall assigned, invigilators confirmed, paper received).

**"View Full MPC Exam Calendar →"** links to `/group/acad/exam-calendar/?stream=mpc`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/upcoming-exams/?type={}"` on filter change `hx-target="#mpc-exam-timeline"` `hx-swap="innerHTML"`.

---

### 5.7 Content Gap Alerts — Alert List

> MPC topics with no study material in the shared content library — the MPC Coordinator ensures coverage.

**Display:** Alert list. Each item: Red dot · Subject (Mathematics/Physics/Chemistry) · Topic name · Chapter · Class · Branches affected (count) · [Create Task →] button.

**Sort:** By subject then by chapter sequence number.

**Filter (within section):** Subject (All / Mathematics / Physics / Chemistry) · Class (XI / XII / Both).

**[Create Task →]:** Opens task assignment modal (420px) — assign to a teacher or branch coordinator to upload study material for this topic. Fields: Assign to, Due date, Priority, Notes.

**Count badge:** Total gap count shown above list — e.g. "18 MPC topics with no study material."

**Empty state:** "No content gaps. All MPC topics have at least one study material in the library." — Green shield.

**"View MPC Content in Library →"** links to `/group/acad/content-library/?stream=mpc`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/content-gaps/?subject={}&class={}"` on filter change `hx-target="#mpc-gap-alerts"` `hx-swap="innerHTML"`.

---

### 5.8 Stream Announcement Drafts — Draft List

> MPC-specific communications drafted for MPC stream teachers across all branches — not yet sent.

**Display:** List — each item: Draft name · Created date · Last edited · Recipient scope (All MPC teachers / Specific branches) · [Edit →] [Preview →] [Send Now →] [Delete ✗] buttons.

**[Draft Announcement ✉] header button:** Opens announcement draft drawer (640px) — rich text editor with template options (Exam reminder / Syllabus update / CPD notice / General) + recipient scope + schedule.

**[Send Now →]:** Opens send confirm modal — shows recipient count + preview. POST to send via system notification + WhatsApp (if configured).

**[Schedule →]:** Allows scheduling announcement for a future date/time.

**Empty state:** "No announcement drafts. Click 'Draft Announcement' in the header to create one." — Message icon illustration.

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-subject-syllabus-detail` (from progress bar chart click)
- **Width:** 560px
- **Tabs:** Topics · Teacher · Chapter Breakdown
- **Topics tab:** Topic, Chapter, Sequence, Status (Covered/In Progress/Not Started), Expected completion week
- **Teacher tab:** Teacher name, qualification, topics assigned, topics completed, last lesson update
- **Chapter Breakdown tab:** Chapter-wise % completion bar chart (mini horizontal bars)
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/branch-subject-detail/?branch={}&subject={}&class={}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.2 Drawer: `term-subject-detail` (from Score Trend chart click)
- **Width:** 480px
- **Content:** Branch-wise scores for selected term and subject — sortable table: Branch, Avg %, Pass %, Max score, Min score
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/term-subject-detail/?term={}&subject={}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.3 Drawer: `branch-teacher-list-subject` (from Teacher Load chart click)
- **Width:** 480px
- **Content:** Teachers for selected branch and subject: Name, Qualification (B.Sc/M.Sc/B.Tech/M.Tech/PhD), Experience (years), Current Rating, Classes assigned (XI/XII), Full-time/Part-time, [View Profile]
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/branch-teachers/?branch={}&subject={}&class={}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.4 Drawer: `mpc-lesson-plan-cell-detail` (from heatmap cell)
- **Width:** 560px
- **Tabs:** Topics with Plans · Missing Topics
- **Topics with Plans tab:** Topic, Subtopics, Uploader, Upload date, Download count
- **Missing Topics tab:** Topic, Chapter, Sequence no., [Assign Upload Task →]
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/lesson-plan-cell/?branch={}&subject={}&class={}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.5 Drawer: `branch-mpc-detail` (from rankings Quick Link)
- **Width:** 560px
- **Tabs:** Score Summary · Syllabus · Teachers
- **Score Summary tab:** Mathematics, Physics, Chemistry — avg score, pass %, grade band breakdown
- **Syllabus tab:** Per-subject coverage %, topics remaining, completion timeline projection
- **Teachers tab:** Count per subject, vacancies, avg rating
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/stream/mpc/branch-detail/{branch_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.6 Drawer: `announcement-draft` (from [Draft Announcement ✉] header)
- **Width:** 640px
- **Tabs:** Compose · Recipients · Schedule · Preview
- **Compose tab:** Template selector (dropdown) · Subject line · Body (rich text editor — bold, italic, bullets, headers) · Attachments (PDF only, max 5MB)
- **Recipients tab:** Scope (All MPC teachers / Specific branches — multi-select / Specific class — XI/XII) · Estimated recipients count shown live
- **Schedule tab:** Send now / Schedule for (date + time picker, IST) / Save as draft
- **Preview tab:** Renders message as it will appear in the notification system + WhatsApp preview
- **HTMX submit:** POST `.../stream/mpc/announcements/` on Send / PUT `.../stream/mpc/announcements/{id}/` on Save Draft

### 6.7 Modal: `send-announcement-confirm`
- **Width:** 400px
- **Content:** "Send announcement to [N] MPC teachers across [M] branches?"
- **Shows:** Subject line, first 100 chars of body, recipient count, channels (System / WhatsApp)
- **Buttons:** [Send Now] (primary) + [Cancel]

### 6.8 Modal: `content-gap-assign-task`
- **Width:** 420px
- **Pre-filled:** Subject, Topic, Chapter, Class
- **Fields:** Assign to (search dropdown — MPC teachers or branch academic coordinators) · Due date · Priority (Low/Medium/High) · Notes (optional)
- **Buttons:** [Create Task] + [Cancel]

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Announcement sent | "MPC announcement sent to [N] teachers across [M] branches." | Success (green) | 5s |
| Draft saved | "Announcement draft '[Name]' saved." | Success | 4s |
| Draft deleted | "Draft '[Name]' deleted." | Warning | 4s |
| Content gap task created | "Task assigned to [Name] for [Topic] gap in [Subject]." | Success | 4s |
| Upload plan submitted | "Lesson plan submitted for review. It will appear in the content library after approval." | Info | 4s |
| KPI load error | "Failed to load MPC stream data. Retrying…" | Error (red) | Manual dismiss |
| Export triggered | "Export started — download will begin shortly." | Info | 4s |
| Observation task created | "Observation task created for [Subject] teacher at [Branch]." | Success | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No syllabus data | Chart outline | "No MPC syllabus data" | "MPC syllabus has not been configured for any branch yet." | [Go to Syllabus Manager] |
| No score trend data | Line chart outline | "No MPC score trend" | "At least 2 terms of MPC exam data are required to show a trend." | — |
| No content gaps | Shield check | "No MPC content gaps" | "Every MPC topic has at least one study material in the library." | — |
| No upcoming exams | Calendar outline | "No MPC exams in 14 days" | "No MPC stream exams are scheduled in the next two weeks." | [View Exam Calendar] |
| No announcement drafts | Message outline | "No drafts" | "No announcement drafts saved. Create one using the 'Draft Announcement' button." | [Draft Announcement] |
| No teacher load data | People outline | "No MPC teacher data" | "Teacher assignments have not been configured for MPC branches." | — |

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

---

## 10. Role-Based UI Visibility

| Element | MPC Stream Coord G3 | CAO G4 (view-only) | Academic Director G3 (view-only) | All other roles |
|---|---|---|---|---|
| Page itself | ✅ Rendered | ✅ Read-only banner | ✅ Read-only banner | ❌ Redirected |
| Alert Banner | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| [Draft Announcement ✉] header button | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Send Now →] on drafts | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Create Task →] in content gaps | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Upload Plan] on heatmap cells | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| Export buttons on charts | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| Branch detail drawer (all tabs) | ✅ Shown | ✅ Shown | ✅ Shown | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/dashboard/` | JWT (G3) | Full page data (MPC-scoped) |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/kpi-cards/` | JWT (G3) | KPI card values (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/syllabus-completion/` | JWT (G3) | 3-subject syllabus progress bars (class, branch filters) |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/branch-subject-detail/` | JWT (G3) | Branch-subject syllabus detail (drawer) |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/score-trend/` | JWT (G3) | Term-over-term MPC score chart (class filter) |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/term-subject-detail/` | JWT (G3) | Term-subject score detail (drawer) |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/teacher-load/` | JWT (G3) | Teacher count per subject per branch chart |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/branch-teachers/` | JWT (G3) | Teachers for branch-subject (drawer) |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/lesson-plan-heatmap/` | JWT (G3) | MPC lesson plan heatmap data |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/lesson-plan-cell/` | JWT (G3) | Heatmap cell detail (drawer) |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/branch-rankings/` | JWT (G3) | Top 5 / Bottom 5 MPC branches (exam filter) |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/branch-detail/{branch_id}/` | JWT (G3) | Branch MPC detail drawer |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/upcoming-exams/` | JWT (G3) | Next 14 days MPC exam timeline (type filter) |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/content-gaps/` | JWT (G3) | MPC topics with no study material |
| POST | `/api/v1/group/{group_id}/acad/stream/mpc/content-gaps/assign-task/` | JWT (G3) | Assign gap fill task |
| GET | `/api/v1/group/{group_id}/acad/stream/mpc/announcements/?status=draft` | JWT (G3) | Draft announcements list |
| POST | `/api/v1/group/{group_id}/acad/stream/mpc/announcements/` | JWT (G3) | Create / send announcement |
| PUT | `/api/v1/group/{group_id}/acad/stream/mpc/announcements/{id}/` | JWT (G3) | Update draft announcement |
| DELETE | `/api/v1/group/{group_id}/acad/stream/mpc/announcements/{id}/` | JWT (G3) | Delete draft |
| POST | `/api/v1/group/{group_id}/acad/stream/mpc/announcements/{id}/send/` | JWT (G3) | Send draft announcement |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../stream/mpc/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Syllabus panels filter (class/branch) | `change` | GET `.../stream/mpc/syllabus-completion/?class={}&branch={}` | `#mpc-syllabus-panels` | `innerHTML` |
| Syllabus bar click | `click` | GET `.../stream/mpc/branch-subject-detail/?branch={}&subject={}&class={}` | `#drawer-body` | `innerHTML` |
| Score trend class filter | `change` | GET `.../stream/mpc/score-trend/?class={}` | `#mpc-score-trend` | `innerHTML` |
| Score trend data point click | `click` | GET `.../stream/mpc/term-subject-detail/?term={}&subject={}` | `#drawer-body` | `innerHTML` |
| Teacher load class filter | `change` | GET `.../stream/mpc/teacher-load/?class={}` | `#mpc-teacher-load` | `innerHTML` |
| Teacher load bar click | `click` | GET `.../stream/mpc/branch-teachers/?branch={}&subject={}&class={}` | `#drawer-body` | `innerHTML` |
| Heatmap cell click | `click` | GET `.../stream/mpc/lesson-plan-cell/?branch={}&subject={}&class={}` | `#drawer-body` | `innerHTML` |
| Rankings exam filter | `change` | GET `.../stream/mpc/branch-rankings/?exam={}` | `#mpc-rankings-card` | `innerHTML` |
| Exam timeline type filter | `change` | GET `.../stream/mpc/upcoming-exams/?type={}` | `#mpc-exam-timeline` | `innerHTML` |
| Content gap filter (subject/class) | `change` | GET `.../stream/mpc/content-gaps/?subject={}&class={}` | `#mpc-gap-alerts` | `innerHTML` |
| Announcement send (modal confirm) | `click` | POST `.../stream/mpc/announcements/{id}/send/` | `#announcement-drafts-list` | `innerHTML` |
| Draft delete | `click` | DELETE `.../stream/mpc/announcements/{id}/` | `#announcement-drafts-list` | `innerHTML` |
| Draft announcement create (drawer) | `click` on header button | GET `.../stream/mpc/announcements/create-form/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
