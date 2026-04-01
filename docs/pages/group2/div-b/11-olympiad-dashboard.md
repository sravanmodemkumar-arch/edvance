# 11 — Olympiad & Scholarship Coordinator Dashboard

> **URL:** `/group/acad/olympiad/`
> **File:** `11-olympiad-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Olympiad & Scholarship Coordinator (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Olympiad & Scholarship Coordinator. This role manages the full lifecycle of competitive examination participation — from announcing exam schedules, driving branch-level student registrations, tracking exam results, to awarding scholarships and following up on medal/rank recognitions. Olympiads tracked include NTSE, NMMS, NSO, IMO, and KVPY, along with JEE and NEET as scholarship-qualifying pathways and state-level examinations such as KCET.

The coordinator's primary daily value comes from knowing: which olympiads are approaching registration deadlines (so branches can be reminded), which exam results have arrived but not yet been formally logged, which scholarship-eligible students are still awaiting their award, and how branch participation rates compare to the previous year. The dashboard is built around these four flows.

The role exists at both large and small groups. For small groups, one person may combine this role with another; the dashboard is designed to be usable even with low data volumes — empty states are informative, not disorienting. This role coordinates closely with the IIT Foundation Director (for Foundation student nominations) and the JEE/NEET Integration Head (for coaching-track scholarship pathways).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Olympiad & Scholarship Coord | G3 | Full — all sections, all actions | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | Full read + override actions | Full oversight |
| Group Academic Director | G3 | Read — all sections | Academic oversight |
| Group IIT Foundation Director | G3 | Read — scholarship pipeline and NTSE/NMMS sections | Foundation-to-olympiad pipeline |
| Group JEE/NEET Integration Head | G3 | Read — scholarship section (JEE/NEET pathway) | Coaching scholarship coordination |
| Group Stream Coordinator — MPC | G3 | Read — NSO/IMO/JEE-related sections | Stream-level visibility |
| Group Stream Coordinator — BiPC | G3 | Read — NSO/NEET-related sections | Stream-level visibility |
| Group Stream Coordinator — MEC/CEC | G3 | Read — NMMS section only | Commerce olympiad context |
| Group Curriculum Coordinator | G2 | — | No access |
| Group Exam Controller | G3 | Read — exam schedule section only | Scheduling coordination |
| Group Special Education Coordinator | G3 | Read — scholarship section only (special needs scholarship tracking) | Cross-function |
| Group Academic MIS Officer | G1 | Read-only — all sections | No write controls visible |
| Group Academic Calendar Manager | G3 | Read — olympiad calendar section only | Calendar coordination |

> **Access enforcement:** Django view decorator `@require_role('olympiad_coord')`. CAO and MIS Officer admitted via role-union check. All other roles redirected to own dashboard unless listed above.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Olympiad & Scholarship  ›  Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]                          [Register for Exam +]  [Settings ⚙]
Group Olympiad & Scholarship Coordinator  ·  Last login: [date time]  ·  [Group Logo]
```

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch name + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all →" link

**Alert trigger examples:**
- Olympiad registration deadline < 7 days away with branch participation < 50%
- Olympiad results received from external body but not yet logged in the system > 3 days
- Scholarship-eligible student not awarded > 45 days past eligibility date
- KVPY registration window open and no students registered from any branch
- Medal/rank follow-up overdue — qualified student not yet formally acknowledged

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Active Exam Registrations | Total students currently registered across all open olympiads | Registration module | Green ≥ target · Yellow 60–99% · Red < 60% of last year baseline | → Section 5.2 Registrations by Exam |
| Upcoming Deadlines | Count of olympiads with registration deadline in next 14 days + earliest deadline date | Calendar module | Green = none · Yellow 1–2 upcoming · Red ≥ 3 or deadline < 3 days | → Section 5.1 Olympiad Calendar |
| Results Pending Logging | Olympiad result sets received but not yet formally logged in system | Results module | Green = 0 · Yellow 1–3 · Red > 3 (pulsing badge) | → Section 5.3 Results Tracker |
| Medals & Ranks This Year | Gold + Silver + Bronze + National Rank mentions — cumulative this academic year | Results module | Green if ≥ last year · Yellow = same · Red < last year | → Section 5.4 Medals & Ranks |
| Scholarships Pending Award | Students who qualified but scholarship not yet formally awarded | Scholarship module | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.6 Scholarship Pipeline |
| Avg Branch Participation | Average % of eligible students registered per olympiad across all branches | Analytics module | Green ≥ 60% · Yellow 40–60% · Red < 40% | → Section 5.5 Branch Participation |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/olympiad/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Olympiad Calendar

> All upcoming olympiads with key dates — registration deadline, exam date, result date — in a single event strip.

**Display:** Event strip (horizontal scrollable timeline) + tabular list toggle.

**Event strip item fields:** Exam name badge (colour-coded by exam body) · Registration deadline · Exam date · Result expected date · Students registered (group total) · [Manage →]

**Exam colour coding:**
- NTSE: Blue
- NMMS: Teal
- NSO: Orange
- IMO: Purple
- KVPY: Red
- JEE (scholarship pathway): Dark blue
- NEET (scholarship pathway): Green
- KCET & state exams: Grey

**Urgency indicators:**
- Registration deadline < 3 days: red badge with countdown ("2 days left")
- Registration deadline < 7 days: amber badge

**[Manage →]:** Opens olympiad management drawer.

**Drawer: `olympiad-manage`**
- Width: 600px
- Tabs: Registration Status · Exam Details · Results · History
- Registration Status tab: Branch-by-branch registration count + [Send Reminder to Branch]
- Exam Details: Official exam date, duration, syllabus link, official body website
- Results: Log results when received / view logged results

**[+ Add Olympiad / Exam] button** (top-right of section): Opens olympiad creation drawer.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/olympiad/calendar/"` · `hx-trigger="load"` · `hx-target="#olympiad-calendar-section"`.

---

### 5.2 Registrations by Exam

> How many students are registered per olympiad, broken down by exam.

**Display:** Stat cards (one per active exam)

**Card content per exam:**
- Exam name + official body (e.g., "NSO — Science Olympiad Foundation")
- Students registered: [N] (group total)
- Branches participating: [M] of [Total offering this stream]
- Class breakdown: Class-wise enrollment (e.g., Cl. 9: 45 · Cl. 10: 62 · Cl. 11: 38)
- Registration deadline: [date] + urgency badge
- [View Details →] button

**View Details →:** Opens a registration drill-down drawer per exam.

**Drawer: `exam-registration-detail`**
- Width: 560px
- Content: Branch-by-branch table — Branch · Class · Students registered · Registration deadline status · [Send Reminder]
- Filter: Sort by registration count ascending (lowest first — prompt action)

**Below stat cards — summary comparison table:**

| Column | Description |
|---|---|
| Exam | Exam name |
| Registered This Year | Total students |
| Registered Last Year | Comparison |
| Delta | ↑ / ↓ % change |
| Participation Rate | % of eligible students registered (by stream) |
| Status | Registration Open · Closed · Upcoming |

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/olympiad/registrations/"` · `hx-trigger="load"` · `hx-target="#registrations-section"`.

---

### 5.3 Results Tracker

> Status of each olympiad's results — submitted to external body / awaiting results / results received / results logged.

**Display:** Status table (sortable)

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Exam | ✅ | Exam name |
| Exam Date | ✅ | When the exam was held |
| Students Appeared | ✅ | Count |
| Result Expected Date | ✅ | Official result announcement date |
| Result Status | ✅ | Awaiting · Received (not logged) · Logged · Verified |
| Students Qualified | ✅ | Count (shown after results logged) |
| Top Score (Group) | ✅ | Highest score achieved in the group |
| Actions | ❌ | [Log Results →] · [View Results →] · [Request Recheck] |

**[Log Results →]:** Opens results logging drawer — bulk entry or file upload (CSV with student code, score, rank, medal/rank tier).

**Drawer: `log-results`**
- Width: 640px
- Tabs: Upload CSV · Manual Entry · Preview · Submit
- Upload CSV: Template download + upload with row-level validation
- Manual Entry: Student code search + score + rank + medal tier input
- Preview: Shows parsed results before final submission
- Submit: POST to results endpoint → changes status to Logged

**[View Results →]:** Opens results view drawer (read-only) — student-level results table.

**Red badge:** On any row where Result Status = "Received (not logged)" for > 3 days.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/olympiad/results/"` · `hx-trigger="load"` · `hx-target="#results-tracker-section"`.

---

### 5.4 Medals & Ranks Highlight

> Gold, Silver, Bronze, and national rank recognitions accumulated this academic year across all branches and olympiads.

**Display:** Highlight cards (top of section) + detail table below.

**Highlight cards:**
- Gold medals / Rank 1: [N] — gold background
- Silver medals / Rank 2–3: [N] — silver background
- Bronze medals / Rank 4–10: [N] — bronze background
- National rank mentions (top 100): [N] — blue background
- State rank mentions (top 50 in state): [N] — teal background

**Detail table (below highlight cards):**

| Column | Sortable | Notes |
|---|---|---|
| Student Code | ✅ | Name visible G3+ |
| Branch | ✅ | |
| Exam | ✅ | |
| Achievement | ✅ | Gold / Silver / Bronze / Rank [N] |
| Exam Date | ✅ | |
| Acknowledged | ✅ | Y / N — whether school has formally recognised the achievement |
| Actions | ❌ | [Acknowledge →] [Issue Certificate] [Add to Group Showcase] |

**[Acknowledge →]:** Marks achievement as formally acknowledged by the school — triggers notification to branch Principal.

**[Issue Certificate]:** Opens certificate generation modal (uses group letterhead template).

**[Add to Group Showcase]:** Adds to group-level achievement wall (public-facing feature).

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/olympiad/medals/"` · `hx-trigger="load"` · `hx-target="#medals-section"`.

---

### 5.5 Branch Participation Rate

> Per-olympiad, per-branch participation rate — what % of eligible students in each branch are registered.

**Display:** Bar chart (Chart.js 4.x)

**X-axis:** Branches (abbreviated, full name in tooltip)

**Y-axis:** Participation rate % (0–100%)

**Bar grouping:** One bar per olympiad, grouped by branch. Or: branch filter to show all olympiads for one branch as separate bars.

**Target line:** Group target participation rate (dashed grey horizontal line, configurable by coordinator).

**Tooltip:** Branch · Exam · Eligible students · Registered · Participation % · Delta from last year

**Colour alert:** Bars < 30% = red · 30–60% = amber · > 60% = green

**Filter within chart:** Exam selector (one or all) · Branch filter · Year (current / previous for comparison)

**Export:** "Export PNG" and "Export XLSX" buttons top-right.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/olympiad/participation/"` · filter changes trigger `hx-get` with params · `hx-target="#participation-section"`.

---

### 5.6 Scholarship Exam Pipeline

> Kanban-style view tracking scholarship examinations and award status.

**Display:** Kanban board — 5 columns (swimlanes)

**Columns (left to right):**
1. Announced — Scholarship exam announced, registration not yet open
2. Registration Open — Students can register; coordinator tracks branch signups
3. Exam Conducted — Exam done; awaiting results
4. Results Received — Results logged; eligible students identified
5. Award Pending / Awarded — Final stage: scholarship disbursed or pending disbursement

**Card fields:** Scholarship name · Exam body · Eligible class(es) · Stream · Students registered / qualified / awarded · Deadline / Exam date · [View Details →]

**[+ Add Scholarship Exam]** button (top-right of section): Opens scholarship exam creation drawer.

**Drag-and-drop** between columns (G3 only): Moves scholarship through the pipeline stages, with mandatory confirmation.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/olympiad/scholarship-pipeline/"` · `hx-trigger="load"` · `hx-target="#pipeline-section"` · drag-and-drop: `hx-post` on drop event with `{scholarship_id, new_stage}`.

---

### 5.7 Follow-up Due — Qualified but Not Awarded

> Students who have qualified for a scholarship or olympiad benefit but have not yet received the formal award.

**Display:** Alert list (card-style, sorted by days overdue)

**Card fields:** Student code (name visible G3+) · Branch · Exam qualified in · Qualification date · Award type (Scholarship / Medal / Certificate / Fee waiver) · Days overdue (red if > 45 days) · Status · [Follow Up →] [Mark Awarded]

**[Follow Up →]:** Opens follow-up action drawer — log a contact attempt with branch, send reminder email/WhatsApp, set next follow-up date.

**[Mark Awarded]:** Quick-action POST — marks award as given + prompts for award date and mode (cheque / bank transfer / fee credit / trophy).

**Empty state:** "No follow-ups overdue. All qualified students have received their awards." — green checkmark.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/olympiad/follow-up/"` · `hx-trigger="load"` · `hx-target="#followup-section"`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `olympiad-manage`
- **Trigger:** [Manage →] in Section 5.1 olympiad calendar
- **Width:** 600px
- **Tabs:** Registration Status · Exam Details · Results · History
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/olympiad/{exam_id}/manage/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.2 Drawer: `exam-registration-detail`
- **Trigger:** [View Details →] in Section 5.2 registration card
- **Width:** 560px
- **Content:** Branch-by-branch registration table; [Send Reminder] per branch
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/olympiad/{exam_id}/registrations/"` `hx-target="#drawer-body"`

### 6.3 Drawer: `log-results`
- **Trigger:** [Log Results →] in Section 5.3 results tracker
- **Width:** 640px
- **Tabs:** Upload CSV · Manual Entry · Preview · Submit
- **HTMX:** `hx-post="/api/v1/group/{group_id}/acad/olympiad/{exam_id}/results/"` on submit

### 6.4 Drawer: `follow-up-action`
- **Trigger:** [Follow Up →] in Section 5.7 follow-up list
- **Width:** 480px
- **Fields:** Contact attempt log (text) · Communication channel · Next follow-up date · [Save Log] [Send Reminder Now]
- **HTMX:** `hx-post="/api/v1/group/{group_id}/acad/olympiad/follow-up/{student_id}/log/"` on save

### 6.5 Modal: `mark-awarded-confirm`
- **Trigger:** [Mark Awarded] in Section 5.7 follow-up list
- **Width:** 420px
- **Content:** "Mark award as given for Student [Code]?" · Award date picker · Award mode (Scholarship cheque / Bank transfer / Fee credit / Trophy / Certificate) · [Confirm] [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/olympiad/follow-up/{student_id}/award/"` → toast + card removed from list

### 6.6 Modal: `acknowledge-achievement`
- **Trigger:** [Acknowledge →] in Section 5.4 medals table
- **Width:** 420px
- **Content:** Achievement summary (read-only) · Acknowledgement mode (Branch assembly / Newsletter / Certificate) · [Confirm Acknowledgement] [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/olympiad/medals/{achievement_id}/acknowledge/"` → notifies branch Principal → toast

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Results logged | "Results logged for [Exam Name] — [N] students recorded" | Success (green) | 5s auto-dismiss |
| Reminder sent to branch | "Registration reminder sent to [Branch Name] for [Exam Name]" | Info (blue) | 4s |
| Achievement acknowledged | "Achievement acknowledged — [Branch Name] Principal notified" | Success | 4s |
| Award marked given | "Award recorded for Student [Code] — [Branch Name] notified" | Success | 5s |
| Scholarship exam pipeline moved | "[Scholarship Name] moved to [Stage]" | Info | 4s |
| Follow-up log saved | "Follow-up logged for Student [Code]" | Success | 4s |
| KPI load error | "Failed to load KPI data. Retrying…" | Error (red) | Manual dismiss |
| Registration deadline alert | "Registration deadline for [Exam] is [N] days away — [N] branches still have 0 registrations" | Warning (yellow) | Manual dismiss |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No olympiads configured | Calendar outline | "No olympiads set up yet" | "Add upcoming olympiad and scholarship exams to start tracking participation" | [Register for Exam +] |
| No registrations yet | Document outline | "No registrations recorded" | "No student registrations have been entered for any olympiad yet" | — |
| No results logged | Clipboard outline | "No results logged" | "Log exam results when received to track medals and scholarship eligibility" | — |
| No medals this year | Trophy outline | "No medals or ranks yet" | "No medals or national rank mentions have been recorded this academic year" | — |
| No follow-ups overdue | Checkmark circle | "All awards issued" | "Every qualified student has received their scholarship or award" | — |
| Scholarship pipeline empty | Kanban outline | "No scholarship exams tracked" | "Add scholarship exams to track the pipeline from announcement to award" | [+ Add Scholarship Exam] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + calendar event strip (4 placeholders) + results table (5 rows) |
| Olympiad calendar load | Horizontal skeleton strip — 4 event card placeholders |
| Registrations section load | Skeleton stat cards — one per exam (3–5 placeholders) |
| Results tracker table load | Skeleton rows — 5 rows |
| Medals section load | Skeleton highlight cards (5) + skeleton table rows (5) |
| Participation chart load | Spinner centred in chart area |
| Scholarship pipeline load | Skeleton kanban columns — 5 column outlines |
| Follow-up list load | Skeleton alert cards — 3 cards |
| Drawer open | Skeleton rows inside drawer body |
| KPI auto-refresh | Subtle shimmer over existing card values |
| Mark awarded / acknowledge button click | Spinner inside button + button disabled |

---

## 10. Role-Based UI Visibility

| Element | Olympiad Coord (G3) | CAO (G4) | Foundation Director (G3) | MIS Officer (G1) | All others |
|---|---|---|---|---|---|
| Page itself | ✅ Rendered | ✅ Rendered (override) | ✅ Partial read | ✅ Read-only | ❌ Redirected |
| Alert Banner | ✅ Shown | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| [Register for Exam +] header | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Log Results →] | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Acknowledge →] achievement | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Mark Awarded] | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Follow Up →] | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| Pipeline drag-and-drop | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Send Reminder] branch | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| Student names | ✅ Visible | ✅ Visible | ✅ Visible (scholarship/NTSE section) | ❌ Code only | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/olympiad/dashboard/` | JWT (G3+) | Full page data |
| GET | `/api/v1/group/{group_id}/acad/olympiad/kpi-cards/` | JWT (G3+) | KPI card values (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/olympiad/calendar/` | JWT (G3+) | Olympiad calendar event strip |
| GET | `/api/v1/group/{group_id}/acad/olympiad/{exam_id}/manage/` | JWT (G3+) | Olympiad management drawer data |
| GET | `/api/v1/group/{group_id}/acad/olympiad/registrations/` | JWT (G3+) | Registrations by exam — stat cards + comparison table |
| GET | `/api/v1/group/{group_id}/acad/olympiad/{exam_id}/registrations/` | JWT (G3+) | Branch-by-branch registration detail |
| POST | `/api/v1/group/{group_id}/acad/olympiad/{exam_id}/remind/` | JWT (G3) | Send registration reminder to branch |
| GET | `/api/v1/group/{group_id}/acad/olympiad/results/` | JWT (G3+) | Results tracker table |
| POST | `/api/v1/group/{group_id}/acad/olympiad/{exam_id}/results/` | JWT (G3) | Log results (CSV upload or manual) |
| GET | `/api/v1/group/{group_id}/acad/olympiad/medals/` | JWT (G3+) | Medals and ranks highlight data |
| POST | `/api/v1/group/{group_id}/acad/olympiad/medals/{achievement_id}/acknowledge/` | JWT (G3) | Acknowledge achievement |
| GET | `/api/v1/group/{group_id}/acad/olympiad/participation/` | JWT (G3+) | Branch participation chart data |
| GET | `/api/v1/group/{group_id}/acad/olympiad/scholarship-pipeline/` | JWT (G3+) | Scholarship pipeline kanban data |
| POST | `/api/v1/group/{group_id}/acad/olympiad/scholarship-pipeline/{scholarship_id}/move/` | JWT (G3) | Move scholarship to next stage |
| GET | `/api/v1/group/{group_id}/acad/olympiad/follow-up/` | JWT (G3+) | Follow-up due list |
| POST | `/api/v1/group/{group_id}/acad/olympiad/follow-up/{student_id}/log/` | JWT (G3) | Log a follow-up contact attempt |
| POST | `/api/v1/group/{group_id}/acad/olympiad/follow-up/{student_id}/award/` | JWT (G3) | Mark award as given |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `/api/.../olympiad/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Olympiad calendar load | `load` | GET `/api/.../olympiad/calendar/` | `#olympiad-calendar-section` | `innerHTML` |
| Open olympiad manage drawer | `click` | GET `/api/.../olympiad/{exam_id}/manage/` | `#drawer-body` | `innerHTML` |
| Registration detail drawer | `click` | GET `/api/.../olympiad/{exam_id}/registrations/` | `#drawer-body` | `innerHTML` |
| Send reminder to branch | `click` | POST `/api/.../olympiad/{exam_id}/remind/` | `#toast-container` | `afterbegin` |
| Open log-results drawer | `click` | GET `/api/.../results/` (drawer init) | `#drawer-body` | `innerHTML` |
| Submit results log | `click` | POST `/api/.../olympiad/{exam_id}/results/` | `#results-tracker-section` | `innerHTML` |
| Acknowledge achievement | `click` | POST `/api/.../medals/{id}/acknowledge/` | `#medals-section` | `innerHTML` |
| Participation filter change | `change` | GET `/api/.../participation/?exam={}&branch={}&year={}` | `#participation-section` | `innerHTML` |
| Pipeline card move | `drop` | POST `/api/.../scholarship-pipeline/{id}/move/` | `#pipeline-section` | `innerHTML` |
| Mark awarded confirm | `click` | POST `/api/.../follow-up/{id}/award/` | `#followup-section` | `innerHTML` |
| Follow-up log save | `click` | POST `/api/.../follow-up/{id}/log/` | `#followup-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
