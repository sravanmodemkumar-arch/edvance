# 04 — Exam Controller Dashboard

> **URL:** `/group/acad/exam-controller/`
> **File:** `04-exam-controller-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Exam Controller (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Exam Controller (G3). This role owns the entire examination lifecycle at group level: managing the central question bank, building and approving exam papers, scheduling examinations across all branches, moderating uploaded results, and publishing answer keys. All 50 branches may run exams simultaneously — the Exam Controller is the single point of coordination.

The dashboard is built for operational urgency. The Exam Controller needs to see at a glance: how many exam papers are in draft (not yet submitted for approval), how many scheduling conflicts exist, which branches have not confirmed exam readiness with <48 hours to go, and what is pending in the result moderation queue. Every widget on this page maps directly to an action the Exam Controller can take from the same screen.

For a large group with up to 50,000 MCQs in the question bank, multiple streams running separate question papers, and concurrent exam sessions across states — data aggregation happens server-side in FastAPI and is served as paginated, filterable datasets to the Django+HTMX frontend. LaTeX rendering is required for mathematical and scientific question previews.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Exam Controller | G3 | Full — all sections, all actions | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | View only — cannot edit | CAO may view but not act on this role's exclusive dashboard |
| Group Academic Director | G3 | View only | Can view exam schedule, cannot build papers or moderate results |
| Group Curriculum Coordinator | G2 | — | Has own dashboard `/group/acad/curriculum-coord/` |
| Group Results Coordinator | G3 | — | Has own dashboard `/group/acad/results-coord/` — receives results from Exam Controller |
| Group Stream Coord — MPC | G3 | — | Has own dashboard `/group/acad/stream/mpc/` |
| Group Stream Coord — BiPC | G3 | — | Has own dashboard `/group/acad/stream/bipc/` |
| Group Stream Coord — MEC/CEC | G3 | — | Has own dashboard `/group/acad/stream/mec-cec/` |
| Group JEE/NEET Integration Head | G3 | — | Has own dashboard `/group/acad/jee-neet/` |
| Group IIT Foundation Director | G3 | — | Has own dashboard `/group/acad/iit-foundation/` |
| Group Olympiad & Scholarship Coord | G3 | — | Has own dashboard `/group/acad/olympiad/` |
| Group Special Education Coordinator | G3 | — | Has own dashboard `/group/acad/special-ed/` |
| Group Academic MIS Officer | G1 | — | Has own dashboard `/group/acad/mis/` |
| Group Academic Calendar Manager | G3 | — | Has own dashboard `/group/acad/cal-manager/` |

> **Access enforcement:** Django view decorator `@require_role('exam_controller')`. Any other role hitting this URL is redirected to their own dashboard. CAO/Academic Director landing here see a read-only banner: "Viewing as [Role] — write actions are disabled on this page."

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Division  ›  Exam Controller Dashboard
```

### 3.2 Page Header
```
Welcome back, [Exam Controller Name]             [+ New Exam Paper]  [View Exam Calendar ↗]  [Settings ⚙]
[Group Name] — Group Exam Controller · Last login: [date time] · [Group Logo]
```

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel at top of page, above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + exam name + branch name (if applicable) + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all X alerts →" links to Exam Conflict Monitor

**Alert trigger examples:**
- Exam in <24 hours with no approved paper (red — Critical)
- Branch exam setup not confirmed with <48 hours to go (red — Critical)
- Scheduling conflict unresolved for >24 hours (red — Critical)
- Result moderation queue backed up >10 items for >2 days (red — Critical)
- Answer key not published >3 days after exam completion (yellow — Warning)
- Question bank topic coverage <80% for any active stream (yellow — Warning)

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Question Bank Total | `38,412` MCQs · `+124` added this month | Question bank | Always neutral (informational) | → Question Bank `/group/acad/question-bank/` |
| Exam Schedule Status | `14 Approved · 3 Pending · 2 Draft · 1 Live` — pipeline snapshot | Exam schedule | Red if any exams are "Live" with paper not approved | → Section 5.2 (Kanban) |
| Exam Conflicts | `3` unresolved conflicts — red pulsing badge if >0 | Conflict engine | Green = 0 · Yellow 1–2 · Red ≥3 | → Exam Conflict Monitor `/group/acad/exam-conflicts/` |
| Papers in Draft | `7` exam papers not yet submitted for approval | Paper builder | Green = 0 · Yellow 1–5 · Red >5 | → Section 5.3 (Draft Papers) |
| Result Moderation | `12` results uploaded awaiting moderation | Result moderation | Green = 0 · Yellow 1–9 · Red ≥10 | → Section 5.5 (Moderation Queue) |
| Answer Keys Pending | `4` papers with answer key not yet published | Answer key tracker | Green = 0 · Yellow 1–3 · Red ≥4 | → Section 5.6 (Answer Key Status) |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/exam-controller/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Question Bank Health — Stat Cards

> Overview of the question bank across all streams and subjects — the Exam Controller's library of exam content.

**Display:** Stat card grid — 4 cards in a row, then a per-stream breakdown table below.

**Stat Cards:**

| Card | Value | Notes |
|---|---|---|
| Total MCQs | `38,412` | All active questions |
| Added This Month | `124` | New questions added in current calendar month |
| Flagged / Under Review | `43` | Questions flagged by teachers for accuracy review |
| Retired This Month | `12` | Questions retired from active use |

**Per-stream breakdown table (below stat cards):**

| Stream | Total Questions | Added (Month) | Flagged | Coverage % (Topics with ≥5 Qs) |
|---|---|---|---|---|
| MPC | 12,340 | 42 | 18 | 91% |
| BiPC | 11,280 | 31 | 12 | 88% |
| MEC-CEC | 7,210 | 28 | 8 | 85% |
| Foundation | 5,890 | 14 | 5 | 79% |
| Integrated JEE | 1,692 | 9 | 0 | 82% |

**[View Full Question Bank →]** links to `/group/acad/question-bank/`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/exam-controller/qbank-health/"` `hx-trigger="every 5m"` `hx-target="#qbank-health-section"` `hx-swap="innerHTML"`.

---

### 5.2 Exam Schedule Status — Kanban Counts

> Visual snapshot of the exam schedule pipeline — how many exams are in each stage.

**Display:** 5-column Kanban count strip (not drag-and-drop — count cards only, clicking opens filtered exam list).

| Column | Stage | Count example | Colour |
|---|---|---|---|
| Draft | Created but not submitted for approval | 2 | Grey |
| Pending Approval | Submitted — awaiting CAO approval | 3 | Yellow |
| Approved | Approved — not yet started | 14 | Blue |
| Live | Currently running across branches | 1 | Green pulsing |
| Completed | Finished — awaiting results upload | 5 | Purple |

**Click on any column count:** Opens filtered exam list drawer (680px) — exams in that stage, sortable table: Exam Name, Stream, Class, Date, Branches, Paper Status, Conflict count, Actions.

**[+ New Exam Schedule →]** button in card header — opens exam schedule create drawer.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/exam-controller/schedule-status/"` `hx-trigger="every 5m"` `hx-target="#exam-kanban-strip"` `hx-swap="innerHTML"`.

---

### 5.3 Papers in Draft — Action List

> Exam papers that have been created but not yet submitted for approval — the Exam Controller must chase these or complete them.

**Display:** List — each item is an action card. Max 8 cards, "View all drafts →" link to Paper Builder.

**Card fields:** Stream badge · Exam name · Class · Creator name + Branch · Created at · Last edited at · Days in draft (red if >5) · [Edit →] [Submit for Approval →] [Delete ✗] buttons.

**[Edit →]:** Opens Exam Paper Builder at `/group/acad/exam-papers/?paper_id={id}`.

**[Submit for Approval →]:** Opens submit-for-approval modal (420px) — pre-filled summary, confirmation checkbox "I confirm this paper is complete and ready for review", submit button. POST to transition paper to "Pending Approval".

**[Delete ✗]:** Opens confirm modal (380px) — "Delete draft paper [Name]? This cannot be undone." Requires typing paper name to confirm.

**Sort:** Days in draft descending (oldest first).

**Empty state:** "No papers in draft. All papers have been submitted for approval or published." — Document check illustration.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/exam-controller/draft-papers/"` `hx-trigger="every 5m"` `hx-target="#draft-papers-section"` `hx-swap="innerHTML"`.

---

### 5.4 Exam Conflicts Unresolved — Alert Banner (Section)

> Live count and list of scheduling conflicts — the Exam Controller must resolve these before exams go live.

**Display:** Dedicated alert section card. Background: red `bg-red-50 border-l-4 border-red-500` if conflicts > 0, green `bg-green-50 border-l-4 border-green-500` if 0.

**If conflicts = 0:** Shows "No scheduling conflicts. All exam schedules are conflict-free." with green checkmark.

**If conflicts > 0:** Shows count badge + conflict list:

| Field | Notes |
|---|---|
| Conflict Type | Date overlap / Same batch / Room overlap / Paper not ready |
| Exam A | Name + date + stream + class |
| Exam B | The conflicting exam |
| Branches Affected | Count |
| Detected | When conflict was detected |
| Status | Unresolved / In Progress |
| Actions | [Resolve →] [View Exam →] |

**[Resolve →]:** Opens conflict resolution drawer (560px) — full conflict details, both exams side-by-side, options: Reschedule Exam A / Reschedule Exam B / Merge (if same paper) / Mark as Acceptable with reason.

**[View All Conflicts →]** links to `/group/acad/exam-conflicts/`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/exam-controller/conflicts-unresolved/"` `hx-trigger="every 2m"` `hx-target="#conflicts-section"` `hx-swap="innerHTML"`.

---

### 5.5 Result Moderation Queue — Counter

> Results uploaded by branches for exams that have completed — awaiting the Exam Controller's moderation.

**Display:** Counter card (large number) + table below.

**Counter:** Large number `12` with label "results awaiting moderation." Background red if ≥10, amber if 1–9, green if 0.

**Table columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Exam Name | Text + link | ✅ | Links to exam detail |
| Stream | Badge | ✅ | |
| Class | Text | ✅ | |
| Branch | Text | ✅ | Branch that uploaded results |
| Upload Date | Date | ✅ | Red if uploaded >2 days ago and not moderated |
| Marks Format | Badge | ❌ | Entered online / XLSX upload / OMR scan |
| Status | Badge | ✅ | Pending Moderation / Moderation in Progress / Moderated |
| Actions | — | ❌ | Review · Approve · Reject · Request Re-upload |

**[Review]:** Opens result moderation drawer (680px) — full marks data, statistical anomaly flags (suspiciously high/low scores, missing roll numbers), moderator checklist.

**[Approve]:** POST to mark result as moderated — transitions to Results Coordinator for rank computation.

**[Reject / Request Re-upload]:** Opens modal — select reason (Missing roll numbers / Marks exceed maximum / Format errors / Suspected data entry error) + notes.

**Pagination:** Server-side · 10/page.

**[View Full Moderation Page →]** links to `/group/acad/result-moderation/`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/exam-controller/moderation-queue/"` `hx-trigger="every 5m"` `hx-target="#moderation-queue-section"` `hx-swap="innerHTML"`.

---

### 5.6 Answer Key Publication — Status Table

> Papers whose answer keys are pending publication post-exam — the Exam Controller publishes these.

**Display:** Sortable table.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Exam Name | Text | ✅ | |
| Stream | Badge | ✅ | |
| Class | Text | ✅ | |
| Exam Date | Date | ✅ | |
| Days Since Exam | Number | ✅ | Red if >3 (SLA breach) |
| Answer Key Status | Badge | ✅ | Not Uploaded / Draft / Ready to Publish / Published |
| Questions | Number | ❌ | Total question count in paper |
| Actions | — | ❌ | Upload Key · Preview · Publish · Edit |

**[Upload Key]:** Opens answer key upload drawer (560px) — per-question answer input (A/B/C/D for MCQ, or numerical answer, or model answer for subjective). Supports XLSX bulk upload of answers.

**[Publish]:** Opens publish confirm modal — "Publish answer key for [Exam Name]? Students and branches will be able to view this." + confirmation. POST to publish.

**Default sort:** Days Since Exam descending (most overdue first).

**Empty state:** "All answer keys are published. No keys pending." — Green document icon.

**[View Answer Keys Page →]** links to `/group/acad/answer-keys/`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/exam-controller/answer-key-status/"` `hx-trigger="every 5m"` `hx-target="#answer-key-table"` `hx-swap="innerHTML"`.

---

### 5.7 Branch Readiness — Table

> Branches that have NOT confirmed exam setup for exams starting in <48 hours — the Exam Controller follows up.

**Display:** Sortable table. Shown only if any exam is <48 hours away. Collapsed "All branches ready" message otherwise.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| State | Badge | ✅ | |
| Exam Name | Text | ✅ | |
| Exam Date & Time | Datetime | ✅ | |
| Hours Until Exam | Number | ✅ | Red if <24, Amber if 24–48 |
| Hall Assigned | Badge | ✅ | Yes / No (red if No) |
| Invigilators Confirmed | Badge | ✅ | Yes / No (red if No) |
| Paper Received | Badge | ✅ | Yes / No (red if No) |
| Last Confirmed | Datetime | ✅ | When branch last updated readiness status |
| Actions | — | ❌ | Send Reminder · Mark Ready (override) · Call Branch |

**[Send Reminder]:** POST to send WhatsApp/system notification to branch principal. Toast: "Readiness reminder sent to [Branch]."

**[Mark Ready (override)]:** Opens confirm modal — Exam Controller can manually mark branch as ready with a note. Audited.

**Default sort:** Hours Until Exam ascending (most urgent first).

**[View Branch Exam Schedule →]** links to `/group/acad/branch-exam-schedule/`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/exam-controller/branch-readiness/"` `hx-trigger="every 5m"` `hx-target="#branch-readiness-table"` `hx-swap="innerHTML"`.

---

### 5.8 Recent Paper Activity — Audit Trail

> Last 10 paper-related actions — create / edit / approve / publish — with timestamp and actor.

**Display:** Compact table — 10 rows, no pagination.

**Columns:** # | Action (create/edit/approve/reject/publish) | Paper Name | Stream | Actor | Branch (if applicable) | Timestamp.

**Click on row:** Opens read-only audit detail modal (420px) — full context of the action.

**"View Full Paper Activity →"** links to `/group/acad/exam-papers/`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `exam-schedule-create`
- **Width:** 680px
- **Tabs:** Identity · Date & Time · Branch Scope · Paper Assignment · Notification
- **Identity tab:** Exam Name (required) · Exam Type (Unit Test/Mid-term/Annual/Mock/Coaching, required) · Stream (required) · Class (required, multi-select)
- **Date & Time tab:** Date (date picker) · Start time · Duration (hours:minutes) · Time zone (defaults to IST)
- **Branch Scope tab:** All branches / Specific branches (multi-select) — conflict check runs on save
- **Paper Assignment tab:** Link existing approved paper from bank (search + select) OR mark "Paper TBD"
- **Notification tab:** Notify branch principals (checkbox, default on) · Notify stream coordinators (checkbox) · Notification text preview
- **Submit:** `hx-post="/api/v1/group/{group_id}/acad/exam-calendar/"` — toast + Kanban count updates

### 6.2 Drawer: `exam-stage-list` (from Kanban count click)
- **Width:** 680px
- **Content:** Sortable, filterable table of exams in the selected stage
- **Columns:** Exam Name · Stream · Class · Date · Branches · Paper Status · Conflict count · [View] [Edit] [Advance Stage]
- **[Advance Stage]:** Moves exam to next pipeline stage — e.g. Draft → Pending Approval
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/exam-controller/schedule-by-stage/?stage={stage}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.3 Drawer: `conflict-resolution` (from conflict list [Resolve →])
- **Width:** 560px
- **Tabs:** Conflict Detail · Exam A · Exam B · Resolution
- **Conflict Detail tab:** Type, affected branches, detection date, severity
- **Exam A / B tabs:** Full exam details — date, time, stream, class, branches, paper status
- **Resolution tab:** Options — Reschedule Exam A / Reschedule Exam B / Merge / Accept with reason. Selection shows additional fields (new date for reschedule, merge confirmation, reason text for accept)
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/exam-controller/conflicts/{conflict_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.4 Drawer: `result-moderation` (from moderation queue [Review])
- **Width:** 680px
- **Tabs:** Marks Data · Anomaly Flags · Checklist · Decision
- **Marks Data tab:** Full marks table — Roll No, Name, Subject 1–N scores, Total, Pass/Fail status. Sortable. Download XLSX button.
- **Anomaly Flags tab:** System-detected issues — rows with marks >max, rows with all zeros, missing roll numbers, duplicate roll numbers
- **Checklist tab:** Moderator checklist — All roll numbers present? / No marks exceed max? / Aggregate calculation verified? / Format consistent? — checkboxes, must all be checked to Approve
- **Decision tab:** [Approve Moderated] · [Reject — Request Re-upload] with reason + category
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/result-moderation/{result_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.5 Drawer: `answer-key-upload`
- **Width:** 560px
- **Tabs:** Manual Entry · XLSX Upload · Preview
- **Manual Entry tab:** Per-question grid — Q1, Q2… with answer input (A/B/C/D radio for MCQ, number for numerical). Marks per question input.
- **XLSX Upload tab:** Download template button + upload field + validation: wrong question count shows error per row
- **Preview tab:** Renders answer key as it will appear to branches after publish
- **Submit:** [Save Draft] + [Save & Publish] buttons

### 6.6 Modal: `paper-submit-approval`
- **Width:** 420px
- **Content:** Summary — Paper name, stream, class, question count, created by, last edited
- **Checkbox:** "I confirm this paper is complete, accurate, and ready for CAO review."
- **Buttons:** [Submit for Approval] (primary) + [Cancel]

### 6.7 Modal: `answer-key-publish-confirm`
- **Width:** 400px
- **Content:** "Publish answer key for [Exam Name]? Branches and students will be able to view correct answers."
- **Buttons:** [Publish Answer Key] (primary green) + [Cancel]

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Exam schedule created | "Exam '[Name]' scheduled. Branch principals notified." | Success (green) | 4s |
| Paper submitted for approval | "Paper '[Name]' submitted for CAO approval." | Success | 4s |
| Paper draft deleted | "Draft paper '[Name]' deleted." | Warning | 4s |
| Conflict resolved | "Conflict resolved. Exam '[Name]' updated." | Success | 4s |
| Result approved (moderation) | "Results for '[Exam]' at [Branch] approved. Sent to Results Coordinator." | Success | 5s |
| Result rejected | "Results for '[Exam]' at [Branch] rejected. Branch notified." | Warning | 5s |
| Answer key published | "Answer key for '[Exam]' published. Branches notified." | Success | 4s |
| Branch readiness reminder sent | "Readiness reminder sent to [Branch]." | Info | 4s |
| KPI load error | "Failed to load exam controller data. Retrying…" | Error (red) | Manual dismiss |
| Export triggered | "Export started — download will begin shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No draft papers | Document check | "No papers in draft" | "All exam papers have been submitted for approval or published." | [+ New Exam Paper] |
| No conflicts | Calendar check | "No scheduling conflicts" | "All exam schedules are conflict-free." | — |
| No result moderation | Stack check | "No results awaiting moderation" | "All uploaded exam results have been moderated." | — |
| No answer keys pending | Key icon | "All answer keys published" | "No answer keys are pending publication." | — |
| No branch readiness issues | Building check | "All branches ready" | "All branches have confirmed exam setup for upcoming exams." | — |
| No upcoming exams (48 hrs) | Calendar outline | "No exams in the next 48 hours" | "No exams requiring readiness confirmation are scheduled." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + question bank stats (4 cards + table) + Kanban strip + draft papers list (5 skeleton cards) |
| KPI auto-refresh | Subtle shimmer over existing card values |
| Conflict section auto-refresh (every 2m) | Subtle shimmer over conflict list |
| Moderation queue auto-refresh | Shimmer over table rows |
| Kanban column click (drawer open) | Spinner in drawer body |
| Result moderation drawer open | Spinner + tab skeletons (marks table can be large) |
| Answer key publish confirm | Spinner inside [Publish] button + button disabled |
| Branch readiness send reminder | Spinner inside reminder button + button disabled |
| Draft paper submit for approval | Spinner inside [Submit for Approval] button |
| Answer key upload submit | Progress bar in drawer (file upload may take time) |

---

## 10. Role-Based UI Visibility

| Element | Exam Controller G3 | CAO G4 (view-only) | Academic Director G3 (view-only) | All other roles |
|---|---|---|---|---|
| Page itself | ✅ Rendered | ✅ Read-only banner | ✅ Read-only banner | ❌ Redirected |
| Alert Banner | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| [+ New Exam Paper] header button | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Submit for Approval] on draft papers | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Resolve →] in conflicts section | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Approve] / [Reject] in moderation queue | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Publish] in answer key table | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Send Reminder] in branch readiness | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Mark Ready (override)] | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| Audit trail table | ✅ Shown | ✅ Shown | ✅ Shown | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/exam-controller/dashboard/` | JWT (G3) | Full page data |
| GET | `/api/v1/group/{group_id}/acad/exam-controller/kpi-cards/` | JWT (G3) | KPI card values (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/exam-controller/qbank-health/` | JWT (G3) | Question bank stats + per-stream breakdown |
| GET | `/api/v1/group/{group_id}/acad/exam-controller/schedule-status/` | JWT (G3) | Kanban stage counts |
| GET | `/api/v1/group/{group_id}/acad/exam-controller/schedule-by-stage/` | JWT (G3) | Exams filtered by stage (drawer) |
| GET | `/api/v1/group/{group_id}/acad/exam-controller/draft-papers/` | JWT (G3) | Draft papers list |
| POST | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/submit/` | JWT (G3) | Submit paper for approval |
| DELETE | `/api/v1/group/{group_id}/acad/exam-papers/{paper_id}/` | JWT (G3) | Delete draft paper |
| GET | `/api/v1/group/{group_id}/acad/exam-controller/conflicts-unresolved/` | JWT (G3) | Unresolved conflict list |
| GET | `/api/v1/group/{group_id}/acad/exam-controller/conflicts/{conflict_id}/` | JWT (G3) | Conflict detail (drawer) |
| POST | `/api/v1/group/{group_id}/acad/exam-controller/conflicts/{conflict_id}/resolve/` | JWT (G3) | Resolve conflict with chosen action |
| GET | `/api/v1/group/{group_id}/acad/exam-controller/moderation-queue/` | JWT (G3) | Result moderation queue |
| GET | `/api/v1/group/{group_id}/acad/result-moderation/{result_id}/` | JWT (G3) | Result moderation drawer data |
| POST | `/api/v1/group/{group_id}/acad/result-moderation/{result_id}/approve/` | JWT (G3) | Approve moderated result |
| POST | `/api/v1/group/{group_id}/acad/result-moderation/{result_id}/reject/` | JWT (G3) | Reject + request re-upload |
| GET | `/api/v1/group/{group_id}/acad/exam-controller/answer-key-status/` | JWT (G3) | Answer key pending table |
| POST | `/api/v1/group/{group_id}/acad/answer-keys/{paper_id}/upload/` | JWT (G3) | Upload / update answer key |
| POST | `/api/v1/group/{group_id}/acad/answer-keys/{paper_id}/publish/` | JWT (G3) | Publish answer key |
| GET | `/api/v1/group/{group_id}/acad/exam-controller/branch-readiness/` | JWT (G3) | Branch readiness table |
| POST | `/api/v1/group/{group_id}/acad/exam-controller/branch-readiness/{branch_id}/remind/` | JWT (G3) | Send readiness reminder |
| POST | `/api/v1/group/{group_id}/acad/exam-controller/branch-readiness/{branch_id}/mark-ready/` | JWT (G3) | Override — mark branch ready |
| POST | `/api/v1/group/{group_id}/acad/exam-calendar/` | JWT (G3) | Create new exam schedule |
| GET | `/api/v1/group/{group_id}/acad/exam-controller/audit-trail/?limit=10` | JWT (G3) | Last 10 paper actions |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../exam-controller/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| QBank stats refresh | `every 5m` | GET `.../exam-controller/qbank-health/` | `#qbank-health-section` | `innerHTML` |
| Kanban auto-refresh | `every 5m` | GET `.../exam-controller/schedule-status/` | `#exam-kanban-strip` | `innerHTML` |
| Kanban column click | `click` | GET `.../exam-controller/schedule-by-stage/?stage={}` | `#drawer-body` | `innerHTML` |
| Draft papers auto-refresh | `every 5m` | GET `.../exam-controller/draft-papers/` | `#draft-papers-section` | `innerHTML` |
| Submit for approval (modal confirm) | `click` | POST `.../exam-papers/{id}/submit/` | `#draft-papers-section` | `innerHTML` |
| Conflict section auto-refresh | `every 2m` | GET `.../exam-controller/conflicts-unresolved/` | `#conflicts-section` | `innerHTML` |
| Conflict resolve drawer | `click` | GET `.../exam-controller/conflicts/{id}/` | `#drawer-body` | `innerHTML` |
| Moderation queue auto-refresh | `every 5m` | GET `.../exam-controller/moderation-queue/` | `#moderation-queue-section` | `innerHTML` |
| Moderation review drawer | `click` | GET `.../result-moderation/{id}/` | `#drawer-body` | `innerHTML` |
| Moderation approve | `click` | POST `.../result-moderation/{id}/approve/` | `#moderation-queue-section` | `innerHTML` |
| Answer key table auto-refresh | `every 5m` | GET `.../exam-controller/answer-key-status/` | `#answer-key-table` | `innerHTML` |
| Answer key publish confirm | `click` | POST `.../answer-keys/{id}/publish/` | `#answer-key-table` | `innerHTML` |
| Branch readiness auto-refresh | `every 5m` | GET `.../exam-controller/branch-readiness/` | `#branch-readiness-table` | `innerHTML` |
| Branch readiness reminder | `click` | POST `.../branch-readiness/{id}/remind/` | `#branch-readiness-table` | `innerHTML` |
| Exam schedule create drawer | `click` on header button | GET `.../exam-calendar/create-form/` | `#drawer-body` | `innerHTML` |
| Exam schedule create submit | `submit` | POST `.../acad/exam-calendar/` | `#exam-kanban-strip` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
