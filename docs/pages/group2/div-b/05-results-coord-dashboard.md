# 05 — Results Coordinator Dashboard

> **URL:** `/group/acad/results-coord/`
> **File:** `05-results-coord-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Results Coordinator (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Results Coordinator (G3). This role is responsible for the post-moderation phase of every examination: receiving moderated results from the Exam Controller, running the cross-branch rank computation engine, tracking toppers across all streams, and controlling the final publication of results to branches and students.

The Results Coordinator is the last gate before results become public. Their dashboard is built around queue management and rank computation accuracy. They need to see at a glance: which exams have all branch marks uploaded and are ready for rank computation, which are still waiting on some branches, what the current group-level leaderboard looks like, and which published result sets are available for review.

For a large group with 50 branches all submitting marks for the same group-level exam, the rank computation is a cross-branch normalization exercise. The dashboard tracks computation status per exam with per-branch marks upload completion. All data is group-scoped and served from FastAPI computation endpoints. Rank tables support up to 1,00,000 student records.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Results Coordinator | G3 | Full — all sections, all actions | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | View only — cannot act | CAO may view but not trigger rank computation or publish results |
| Group Academic Director | G3 | View only | Can view results summary, cannot publish |
| Group Exam Controller | G3 | — | Has own dashboard `/group/acad/exam-controller/` — sends moderated results to this role |
| Group Curriculum Coordinator | G2 | — | Has own dashboard `/group/acad/curriculum-coord/` |
| Group Stream Coord — MPC | G3 | — | Has own dashboard `/group/acad/stream/mpc/` |
| Group Stream Coord — BiPC | G3 | — | Has own dashboard `/group/acad/stream/bipc/` |
| Group Stream Coord — MEC/CEC | G3 | — | Has own dashboard `/group/acad/stream/mec-cec/` |
| Group JEE/NEET Integration Head | G3 | — | Has own dashboard `/group/acad/jee-neet/` |
| Group IIT Foundation Director | G3 | — | Has own dashboard `/group/acad/iit-foundation/` |
| Group Olympiad & Scholarship Coord | G3 | — | Has own dashboard `/group/acad/olympiad/` |
| Group Special Education Coordinator | G3 | — | Has own dashboard `/group/acad/special-ed/` |
| Group Academic MIS Officer | G1 | — | Has own dashboard `/group/acad/mis/` |
| Group Academic Calendar Manager | G3 | — | Has own dashboard `/group/acad/cal-manager/` |

> **Access enforcement:** Django view decorator `@require_role('results_coord')`. Any other role hitting this URL is redirected to their own dashboard. CAO and Academic Director landing here see a read-only banner: "Viewing as [Role] — write actions are disabled on this page."

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Division  ›  Results Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]                 [Published Results Archive ↗]  [Settings ⚙]
[Group Name] — Group Results Coordinator · Last login: [date time] · [Group Logo]
```

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel at top of page, above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + exam name + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown

**Alert trigger examples:**
- Exam with CAO approval to publish has been waiting >24 hours without publication (red — Critical)
- Branch marks upload overdue: exam date was >5 days ago, marks not uploaded from ≥3 branches (red — Critical)
- Rank computation completed but results not published for >48 hours (yellow — Warning)
- Toppers report not generated after rank computation >12 hours (yellow — Warning)
- Score distribution anomaly detected post-computation (suspiciously uniform scores) (yellow — Warning)

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Rank Computation Queue | `4` exams awaiting rank computation — marks upload check | Rank queue | Green = 0 · Yellow 1–3 · Red ≥4 | → Section 5.1 (Rank Queue) |
| Results Published Today | `2` result sets published today | Publication tracker | Always informational (count badge) | → Section 5.7 (Archive) |
| Group Rank #1 Student | `[Student Name] — 98.4%` current term, MPC stream | Leaderboard | Always neutral (trophy icon) | → Section 5.5 (Leaderboard) |
| Branches Marks Uploaded | `47 / 50` branches have uploaded marks for active computations | Upload tracker | Green = all branches · Yellow = 1–5 missing · Red >5 missing | → Section 5.1 (per-exam detail) |
| Avg Score (Latest Exam) | `71.4%` group average across all branches for the most recent completed exam | Result data | Green ≥75% · Yellow 60–74% · Red <60% | → Section 5.4 (Branch-wise Chart) |
| Pending CAO Approval | `1` result set awaiting CAO sign-off before publication | Approval queue | Green = 0 · Yellow 1–2 · Red ≥3 | → Section 5.2 (Publication Queue) |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/results-coord/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Rank Computation Queue — Status List

> Exams awaiting rank computation — the Results Coordinator's primary action queue. Shows marks upload status per branch per exam.

**Display:** Vertical list — each exam as a status card.

**Card fields:**
- Exam name (large) + Stream badge + Class
- Exam date + Branch scope (N branches)
- Marks upload progress: `47 / 50 branches uploaded` — progress bar (green if 100%, amber if ≥90%, red if <90%)
- Status badge: `Marks Pending` (red) / `Ready to Compute` (green) / `Computing…` (blue spinner) / `Computed` (purple) / `Published` (grey)
- [View Upload Status →] — opens per-branch upload detail drawer
- [Run Rank Computation →] — enabled only when status = `Ready to Compute` (all branches uploaded)
- [Compute Anyway →] — enabled when ≥80% branches uploaded, with warning: "Results from missing branches will be excluded"

**Sort:** By exam date ascending (oldest exam first).

**[Run Rank Computation →]:** POST to trigger computation. Shows full-page overlay: "Computing ranks for [N] students across [M] branches… Do not close this window." Computation is async — page polls status every 5 seconds.

**[Compute Anyway →]:** Opens confirm modal — lists branches not yet uploaded, asks for confirmation, requires reason.

**Empty state:** "No exams in the rank computation queue. Exams will appear here once results are moderated by the Exam Controller." — Queue icon illustration.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/results-coord/rank-queue/"` `hx-trigger="every 2m"` `hx-target="#rank-queue-section"` `hx-swap="innerHTML"`.

---

### 5.2 Results Published Today — Counter

> Count and links to result sets published in the current calendar day.

**Display:** Counter card — large number `2` + label "results published today."

**Below counter:** List of today's published results — Exam name, Stream, Class, Published at, [View →] link.

**[View →]:** Links to the published result page for that exam.

**"View All Published Results →"** links to published results archive.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/results-coord/published-today/"` `hx-trigger="every 5m"` `hx-target="#published-today-card"` `hx-swap="innerHTML"`.

---

### 5.3 Topper Update — Stat Cards

> Group rank #1–10 names and scores for the current term — updated after each rank computation.

**Display:** 10 topper cards — ranked 1 through 10.

**Card fields:** Rank badge (gold #1, silver #2, bronze #3, neutral #4–10) · Student name · Branch · Stream · Score (%) · Subject-wise best score · Rank movement from last exam (↑ or ↓ N positions or NEW).

**Term selector:** Current term / Previous term (comparison mode).

**Stream filter:** All streams / MPC / BiPC / MEC-CEC / Foundation — filters the leaderboard to that stream.

**Click on student card:** Opens student academic profile drawer (560px) — exam-by-exam scores, attendance, branch details, teacher notes.

**Export:** "Export Top 10 as PDF" — generates a formatted toppers certificate report.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/results-coord/toppers/?term={}&stream={}"` `hx-trigger="change"` on filter selectors `hx-target="#topper-cards"` `hx-swap="innerHTML"`.

---

### 5.4 Branch-wise Average Score — Bar Chart

> All branches compared on the most recent group exam — the Results Coordinator checks for outliers.

**Display:** Horizontal bar chart (Chart.js 4.x). Y-axis = branch names. X-axis = average score %. Sorted descending (highest first).

**Bar colours:** Green ≥75% · Amber 60–74% · Red <60%.

**Reference line:** Group average (dashed vertical line).

**Tooltip:** Branch name · State · Avg score % · Pass % · Students appeared · Students passed · Highest score in branch.

**Exam selector (above chart):** Dropdown of last 10 completed exams — Results Coordinator selects which exam to compare. Defaults to most recent.

**Stream filter:** Multi-select — filters chart to selected streams only.

**Click on bar:** Opens branch score detail drawer (560px) — subject-wise breakdown for that branch in the selected exam.

**Export:** "Export PNG" + "Export CSV" buttons.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/results-coord/branch-scores/?exam={}&stream={}"` `hx-trigger="change"` on exam/stream selectors `hx-target="#branch-score-chart"` `hx-swap="innerHTML"`.

---

### 5.5 Subject Rank Distribution — Stacked Bar

> Score band breakdown per subject across the group — how students distributed across A/B/C/D/F bands.

**Display:** Stacked horizontal bar chart (Chart.js 4.x). Y-axis = subjects. X-axis = % of students. Each bar stacked by grade band.

**Grade bands and colours:**
- A (≥75%): Green
- B (60–74%): Blue
- C (50–59%): Yellow
- D (35–49%): Orange
- F (<35%): Red

**Tooltip:** Subject · Grade band · % of students · Actual student count.

**Exam selector:** Same dropdown as Section 5.4 — synced (changing one updates both charts).

**Stream filter:** Single-select — one stream at a time (subjects vary by stream).

**Click on a grade band in a bar:** Opens student list drawer (560px) — students in that subject × grade band: Roll No, Name, Branch, Score.

**Export:** "Export PNG" button.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/results-coord/subject-distribution/?exam={}&stream={}"` `hx-trigger="change"` on exam/stream `hx-target="#subject-distribution-chart"` `hx-swap="innerHTML"`.

---

### 5.6 Cross-branch Rank Leaderboard — Top 10 Table

> Roll no, name, branch, stream, total score, and group rank for the top 10 students in the most recent exam.

**Display:** Sortable table with rank medals for top 3.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Rank | Number + medal | ✅ | Gold/Silver/Bronze medal icon for 1/2/3 |
| Roll No | Text | ✅ | Group-level roll number |
| Student Name | Text | ✅ | |
| Branch | Text | ✅ | Branch name |
| State | Badge | ✅ | |
| Stream | Badge | ✅ | MPC/BiPC/MEC-CEC/Foundation |
| Total Score | Number + % | ✅ | |
| Previous Rank | Number | ✅ | Shows movement arrow |
| Actions | — | ❌ | View Profile |

**Default sort:** Rank ascending.

**Exam selector:** Dropdown of last 10 completed group exams.

**Stream filter:** Show top 10 overall / top 10 per stream toggle.

**[View Profile]:** Opens student academic profile drawer (560px).

**"Download Toppers Report →"** generates PDF with styled leaderboard.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/results-coord/leaderboard/?exam={}&stream={}"` `hx-trigger="change"` on exam/stream `hx-target="#leaderboard-table"` `hx-swap="innerHTML"`.

---

### 5.7 Result Archive Quick-access — Recent List

> Last 5 published exams — quick links for the Results Coordinator to review or re-access.

**Display:** List — 5 items. Each item: Exam name + Stream + Class + Published on date + Published by + [View Results →] link.

**[View Results →]:** Links to the full published result page for that exam.

**"View Full Archive →"** links to `/group/acad/results-coord/archive/`.

---

### 5.8 Rank Computation Status — Progress Bar

> For an ongoing rank computation — shows % of branches whose marks are uploaded and being processed.

**Display:** Progress bar card — shown prominently only when a rank computation is in progress. Hidden (collapsed) when no computation is running.

**Fields:** Exam name + Stream + Class · Progress bar (% branches marks uploaded) · Estimated completion time · Status: `Uploading Marks` / `Computation Queued` / `Computing…` / `Finalising Ranks` / `Complete`.

**Poll frequency when active:** Page polls status every 5 seconds via HTMX.

**On completion:** Progress bar collapses, toast: "Rank computation for [Exam] complete. Review and publish results." Rank queue updates.

**HTMX (active computation):** `hx-get="/api/v1/group/{group_id}/acad/results-coord/computation-status/{computation_id}/"` `hx-trigger="every 5s"` `hx-target="#computation-status-card"` `hx-swap="innerHTML"`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-upload-status` (from Rank Queue [View Upload Status →])
- **Width:** 560px
- **Tabs:** Uploaded · Pending · Excluded
- **Uploaded tab:** Table — Branch, State, Uploaded by, Upload date, Total students, Records validated, [View Marks]
- **Pending tab:** Table — Branch, State, Branch coordinator name, Last contacted, [Send Reminder] button per row
- **Excluded tab:** Branches excluded from computation (if Compute Anyway was used)
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/results-coord/upload-status/{exam_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.2 Drawer: `branch-score-detail` (from Branch Score bar chart click)
- **Width:** 560px
- **Content:** Subject-wise breakdown table for the selected branch and exam
- **Columns:** Subject · Avg Marks · Max Marks · Pass % · Grade Band Distribution (mini stacked bar)
- **Below table:** Top 3 students from this branch in this exam
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/results-coord/branch-exam-detail/?branch={}&exam={}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.3 Drawer: `subject-grade-band-students` (from Subject Distribution chart click)
- **Width:** 560px
- **Content:** Students in selected subject × grade band
- **Table:** Roll No · Name · Branch · Score · Grade
- **Pagination:** Server-side · 25/page (can be large)
- **Export:** Download XLSX
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/results-coord/grade-band-students/?subject={}&band={}&exam={}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.4 Drawer: `student-academic-profile` (from Topper cards and Leaderboard [View Profile])
- **Width:** 560px
- **Tabs:** Score History · Attendance · Branch Info
- **Score History tab:** Exam-by-exam scores table + line chart — last 6 exams — showing trend
- **Attendance tab:** Monthly attendance % for current academic year
- **Branch Info tab:** Branch name, state, stream, class, teacher names
- **All read-only**
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/students/{student_id}/profile/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.5 Modal: `rank-computation-confirm`
- **Width:** 420px
- **Content:** "Run rank computation for [Exam Name]? [N] branches have uploaded marks ([M] branches pending)."
- **If all branches uploaded:** Clean confirmation. [Compute Ranks] button (primary).
- **If some branches missing:** Warning list of missing branches + checkbox "I acknowledge that [N] branches are excluded from this computation" (required to enable submit)
- **Reason field:** Required if excluding branches (min 20 chars)
- **Buttons:** [Compute Ranks] + [Cancel]

### 6.6 Modal: `branch-marks-reminder`
- **Width:** 380px
- **Content:** "Send marks upload reminder to [Branch Name] for [Exam Name]?"
- **Fields:** Message preview (editable) · Channel (System notification / WhatsApp / Email)
- **Buttons:** [Send Reminder] + [Cancel]

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Rank computation started | "Rank computation started for [Exam]. This may take a few minutes." | Info | 5s |
| Rank computation complete | "Rank computation for [Exam] complete. Review and publish results." | Success (green) | 6s + [Publish Now →] link |
| Results published | "Results for [Exam] published. Branches and students notified." | Success | 5s |
| Marks upload reminder sent | "Upload reminder sent to [Branch] for [Exam]." | Info | 4s |
| Toppers PDF exported | "Toppers report downloading…" | Info | 3s |
| KPI load error | "Failed to load results data. Retrying…" | Error (red) | Manual dismiss |
| Computation status error | "Rank computation encountered an error. Contact system admin." | Error | Manual dismiss |
| Export triggered | "Export started — download will begin shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No items in rank queue | Queue check | "Rank queue is empty" | "No exams are awaiting rank computation. Exams appear here after Exam Controller moderation." | — |
| No results published today | Calendar outline | "No results published today" | "No exam results have been published today." | — |
| No topper data | Trophy outline | "No toppers data" | "Toppers data will appear after rank computation for the current term." | — |
| No completed exams (for charts) | Chart outline | "No exam data available" | "Complete at least one group exam with uploaded marks to view comparative analytics." | — |
| No leaderboard entries | Podium outline | "No leaderboard data" | "Run rank computation for a group exam to populate the leaderboard." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + rank queue list (4 skeleton cards) + topper cards (10 skeleton) + bar chart placeholder |
| KPI auto-refresh | Subtle shimmer over existing card values |
| Rank queue auto-refresh (every 2m) | Shimmer over list cards |
| Branch score chart exam/stream filter | Chart area shimmer + centred spinner |
| Subject distribution chart filter | Chart area shimmer + centred spinner |
| Leaderboard exam/stream filter | Table skeleton rows (10) |
| Rank computation in progress | Full-page overlay: "Computing ranks for [N] students…" with animated progress indicator |
| Topper cards stream/term filter | Card grid shimmer |
| Drawer open (any) | Spinner in drawer body + tab skeletons |
| Computation status poll | Subtle pulse on progress bar (no layout shift) |

---

## 10. Role-Based UI Visibility

| Element | Results Coord G3 | CAO G4 (view-only) | Academic Director G3 (view-only) | All other roles |
|---|---|---|---|---|
| Page itself | ✅ Rendered | ✅ Read-only banner | ✅ Read-only banner | ❌ Redirected |
| Alert Banner | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| [Run Rank Computation →] | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Compute Anyway →] | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Publish Results] action | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Send Reminder] in upload status drawer | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| Download Toppers PDF | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| Export buttons on charts | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| Student academic profile drawer | ✅ Shown | ✅ Shown | ✅ Shown | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/results-coord/dashboard/` | JWT (G3) | Full page data |
| GET | `/api/v1/group/{group_id}/acad/results-coord/kpi-cards/` | JWT (G3) | KPI card values (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/results-coord/rank-queue/` | JWT (G3) | Rank computation queue list |
| GET | `/api/v1/group/{group_id}/acad/results-coord/upload-status/{exam_id}/` | JWT (G3) | Branch upload status drawer |
| POST | `/api/v1/group/{group_id}/acad/results-coord/rank-compute/{exam_id}/` | JWT (G3) | Trigger rank computation |
| GET | `/api/v1/group/{group_id}/acad/results-coord/computation-status/{computation_id}/` | JWT (G3) | Poll computation progress |
| GET | `/api/v1/group/{group_id}/acad/results-coord/published-today/` | JWT (G3) | Today's published results |
| GET | `/api/v1/group/{group_id}/acad/results-coord/toppers/` | JWT (G3) | Top 10 students (term, stream filters) |
| GET | `/api/v1/group/{group_id}/acad/results-coord/toppers/pdf/` | JWT (G3) | Generate toppers PDF report |
| GET | `/api/v1/group/{group_id}/acad/results-coord/branch-scores/` | JWT (G3) | Branch avg score chart (exam, stream) |
| GET | `/api/v1/group/{group_id}/acad/results-coord/branch-exam-detail/` | JWT (G3) | Branch score detail drawer |
| GET | `/api/v1/group/{group_id}/acad/results-coord/subject-distribution/` | JWT (G3) | Subject grade band chart data |
| GET | `/api/v1/group/{group_id}/acad/results-coord/grade-band-students/` | JWT (G3) | Students in grade band drawer |
| GET | `/api/v1/group/{group_id}/acad/results-coord/leaderboard/` | JWT (G3) | Top 10 leaderboard (exam, stream) |
| GET | `/api/v1/group/{group_id}/acad/students/{student_id}/profile/` | JWT (G3) | Student academic profile drawer |
| POST | `/api/v1/group/{group_id}/acad/results-coord/results/{result_set_id}/publish/` | JWT (G3) | Publish result set |
| POST | `/api/v1/group/{group_id}/acad/results-coord/upload-reminder/{branch_id}/` | JWT (G3) | Send marks upload reminder |
| GET | `/api/v1/group/{group_id}/acad/results-coord/archive/?limit=5` | JWT (G3) | Last 5 published results (quick-access) |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../results-coord/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Rank queue auto-refresh | `every 2m` | GET `.../results-coord/rank-queue/` | `#rank-queue-section` | `innerHTML` |
| Upload status drawer | `click` | GET `.../results-coord/upload-status/{exam_id}/` | `#drawer-body` | `innerHTML` |
| Run rank computation (confirm) | `click` on Confirm | POST `.../results-coord/rank-compute/{exam_id}/` | `#rank-queue-section` | `innerHTML` |
| Computation status poll (active) | `every 5s` | GET `.../results-coord/computation-status/{id}/` | `#computation-status-card` | `innerHTML` |
| Published today auto-refresh | `every 5m` | GET `.../results-coord/published-today/` | `#published-today-card` | `innerHTML` |
| Topper stream/term filter | `change` | GET `.../results-coord/toppers/?term={}&stream={}` | `#topper-cards` | `innerHTML` |
| Student profile drawer | `click` | GET `.../acad/students/{id}/profile/` | `#drawer-body` | `innerHTML` |
| Branch score chart filter | `change` | GET `.../results-coord/branch-scores/?exam={}&stream={}` | `#branch-score-chart` | `innerHTML` |
| Branch score bar click | `click` | GET `.../results-coord/branch-exam-detail/?branch={}&exam={}` | `#drawer-body` | `innerHTML` |
| Subject distribution chart filter | `change` | GET `.../results-coord/subject-distribution/?exam={}&stream={}` | `#subject-distribution-chart` | `innerHTML` |
| Grade band click | `click` | GET `.../results-coord/grade-band-students/?subject={}&band={}&exam={}` | `#drawer-body` | `innerHTML` |
| Leaderboard filter | `change` | GET `.../results-coord/leaderboard/?exam={}&stream={}` | `#leaderboard-table` | `innerHTML` |
| Publish results | `click` | POST `.../results-coord/results/{id}/publish/` | `#rank-queue-section` | `innerHTML` |
| Upload reminder (modal confirm) | `click` | POST `.../results-coord/upload-reminder/{branch_id}/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
