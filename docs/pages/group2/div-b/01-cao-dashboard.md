# 01 — CAO Dashboard

> **URL:** `/group/acad/cao/`
> **File:** `01-cao-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Chief Academic Officer (G4) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Chief Academic Officer (CAO). Single-screen academic command centre providing visibility across all streams, all branches, and all academic functions simultaneously. The CAO is the highest academic authority at group level, responsible for curriculum standards, examination integrity, teacher performance, and result quality across all 50 branches.

This dashboard surfaces the composite Academic Health Score for the group, highlights branches that are lagging in curriculum delivery, flags pending approvals that only the CAO can clear (exam papers, result releases, IEP reviews, policy changes), and gives a live stream-wise result summary. The CAO starts every working day here and should not need to navigate elsewhere for the first 20 minutes of their day.

The page is designed for a large group running 20,000–1,00,000 students across 5 states, 7+ streams, with up to 50 branches running concurrent exams. All data is scoped to the CAO's group only and pulls from FastAPI aggregation endpoints that consolidate branch-level data in real time.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | Full — all sections, all actions | This is their exclusive dashboard |
| Group Academic Director | G3 | — | Has own dashboard `/group/acad/director/` |
| Group Curriculum Coordinator | G2 | — | Has own dashboard `/group/acad/curriculum-coord/` |
| Group Exam Controller | G3 | — | Has own dashboard `/group/acad/exam-controller/` |
| Group Results Coordinator | G3 | — | Has own dashboard `/group/acad/results-coord/` |
| Group Stream Coord — MPC | G3 | — | Has own dashboard `/group/acad/stream/mpc/` |
| Group Stream Coord — BiPC | G3 | — | Has own dashboard `/group/acad/stream/bipc/` |
| Group Stream Coord — MEC/CEC | G3 | — | Has own dashboard `/group/acad/stream/mec-cec/` |
| Group JEE/NEET Integration Head | G3 | — | Has own dashboard `/group/acad/jee-neet/` |
| Group IIT Foundation Director | G3 | — | Has own dashboard `/group/acad/iit-foundation/` |
| Group Olympiad & Scholarship Coord | G3 | — | Has own dashboard `/group/acad/olympiad/` |
| Group Special Education Coordinator | G3 | — | Has own dashboard `/group/acad/special-ed/` |
| Group Academic MIS Officer | G1 | — | Has own dashboard `/group/acad/mis/` |
| Group Academic Calendar Manager | G3 | — | Has own dashboard `/group/acad/cal-manager/` |

> **Access enforcement:** Django view decorator `@require_role('cao')`. Any other role hitting this URL is redirected to their own dashboard URL. CAO may *view* (but not *edit*) other role dashboards by navigating directly to their URLs — all write actions on those pages are gated server-side to the exclusive role.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Division  ›  CAO Dashboard
```

### 3.2 Page Header
```
Welcome back, [CAO Name]                        [Download Academic Report ↓]  [Settings ⚙]
[Group Name] — Chief Academic Officer · Last login: [date time] · [Group Logo]
```

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel at top of page, above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch name + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all X alerts →" link to Exam Conflict Monitor or relevant section

**Alert trigger examples:**
- Exam calendar conflicts unresolved for >24 hours (red — Critical)
- Branch curriculum coverage <60% with 30 days left in term (red — Critical)
- IEP review overdue by >7 days (red — POCSO / welfare risk)
- CAO approval pending on result release for >48 hours (yellow — Warning)
- Teacher performance average <3.0 in ≥3 branches simultaneously (yellow — Warning)
- CPD completion rate <50% with deadline <14 days (yellow — Warning)

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Academic Health Score | Composite gauge `78/100` — composite of attendance × result % × curriculum adherence × teacher performance | Aggregated via `/cao/kpi-cards/` | Green ≥85 · Yellow 70–84 · Red <70 | → Section 5.1 (gauge detail drawer) |
| Curriculum Coverage | `82%` avg syllabus completion this term across all branches and streams | Branch syllabus data | Green ≥90% · Yellow 75–89% · Red <75% | → Syllabus Manager `/group/acad/syllabus/` |
| Exam Conflicts | `3` unresolved scheduling conflicts — red pulsing badge if >0 | Exam calendar conflict engine | Green = 0 · Yellow 1–2 · Red ≥3 | → Exam Conflict Monitor `/group/acad/exam-conflicts/` |
| Pending Approvals | `12` items across all queues — pulsing badge if >0 | Approval aggregation | Badge always visible if >0 | → Section 5.3 (Approval Queue) |
| Group Avg Result | `71.4%` current term across all streams and branches | Result aggregation | Green ≥75% · Yellow 60–74% · Red <60% | → Result Moderation `/group/acad/result-moderation/` |
| Special Ed IEPs Overdue | `4` IEPs past review date | IEP tracker | Green = 0 · Yellow 1–3 · Red ≥4 | → Special Ed Dashboard `/group/acad/special-ed/` |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/cao/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Academic Health Score Gauge

> Composite score (0–100) representing the overall academic standing of the group this term.

**Display:** Large gauge chart (Chart.js 4.x doughnut-style) centred in a card, 240px diameter.

**Composite formula (shown in tooltip):**
- Avg Attendance across branches: 25% weight
- Avg Result % across all exams this term: 30% weight
- Curriculum Adherence (avg syllabus coverage %): 25% weight
- Teacher Performance (avg teacher rating / 5 × 100): 20% weight

**Score bands:** 0–59 → Red zone · 60–74 → Amber zone · 75–84 → Yellow zone · 85–100 → Green zone.

**Sub-score breakdown (below gauge):** Four mini stat tiles showing each component's current value with its individual colour status.

**Trend arrow:** Comparison to last term's score — ↑ green / ↓ red.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cao/health-score/"` `hx-trigger="every 5m"` `hx-target="#health-score-card"` `hx-swap="innerHTML"`.

---

### 5.2 Curriculum Coverage by Branch

> Horizontal bar chart showing % syllabus completed this term per branch — CAO uses this to spot which branches are lagging.

**Display:** Horizontal bar chart (Chart.js 4.x). One bar per branch, sorted ascending (worst first).

**X-axis:** 0–100% (syllabus completion percentage).

**Bar colours:** Green ≥85% · Amber 70–84% · Red <70%.

**Tooltip:** Branch name · Stream(s) · Coverage %  · Weeks remaining in term · Expected coverage at this point.

**Filters (within card):**
- Stream selector (All / MPC / BiPC / MEC-CEC / Foundation / Integrated)
- Term selector (Current / Previous)

**Click on bar:** Opens branch curriculum detail drawer (560px) — topics covered vs pending, lesson plan submission rate, last update date.

**Export:** "Export PNG" button top-right of chart card.

**Empty state:** "No curriculum data available for this term. Ensure syllabus is configured for all branches."

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cao/curriculum-coverage/"` `hx-trigger="change"` on stream/term selectors `hx-target="#curriculum-chart"` `hx-swap="innerHTML"`.

---

### 5.3 Pending Approvals Queue

> Items awaiting CAO's explicit approval — exam papers, result releases, IEP reviews, policy changes.

**Display:** Card list (not table) — max 6 cards, "View all in Approval Hub →" link.

**Card fields:** Type badge | Subject/Exam name | Branch (if applicable) | Submitted by | Days pending (red if >3 for papers, >2 for results) | [Approve ✓] [Reject ✗] [View Details →]

**Approval types shown here:**

| Type | Badge colour | SLA |
|---|---|---|
| Exam paper for publication | Blue | 3 days |
| Result release approval | Purple | 2 days |
| IEP review sign-off | Orange | 5 days |
| Academic policy change | Grey | 7 days |
| CPD programme approval | Teal | 5 days |

**Approve action:** `hx-post="/api/v1/group/{group_id}/acad/approvals/{approval_id}/approve/"` — on success: toast "Approval recorded and notified" · card removed from queue · audit log entry written.

**Reject action:** Opens 400px modal with required reason field (min 20 chars). POST with reason. Notifies submitter via system notification.

---

### 5.4 Stream Result Summary

> 4-column stat grid — MPC / BiPC / MEC-CEC / Foundation — group average this term vs last term.

**Display:** 4 stat cards in a row, each card showing:
- Stream name + colour indicator
- Group average score this term (large number, e.g. `73.2%`)
- Last term average (smaller, greyed)
- Delta: ↑ 2.1% (green) or ↓ 1.3% (red)
- Highest scoring branch name + score
- Lowest scoring branch name + score

**Click on card:** Opens stream result detail drawer (640px) — per-branch scores, subject breakdown, rank distribution.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cao/stream-results/"` `hx-trigger="every 5m"` `hx-target="#stream-result-grid"` `hx-swap="innerHTML"`.

---

### 5.5 Top 5 / Bottom 5 Branches (Academic Health)

> Split table — two columns: Top 5 on the left, Bottom 5 on the right — ranked by academic health score.

**Display:** Side-by-side tables within a single card.

**Columns (each table):** Rank · Branch Name · State · Academic Health Score · Delta from last term (arrow + %) · Quick Link.

**Delta arrows:** ↑ green / ↓ red / → flat grey.

**"Quick Link":** [View Branch →] — opens branch academic detail page for that branch.

**Default sort:** Academic health score descending for Top 5, ascending for Bottom 5.

**Update frequency:** Refreshes with page load; manual "Refresh ↺" button in card header.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cao/branch-rankings/"` `hx-target="#branch-rankings-card"` `hx-swap="innerHTML"` on manual refresh click.

---

### 5.6 Teacher Performance Alerts

> Branches where average teacher rating is below 3.0 — requires CAO's attention.

**Display:** List with severity dots. Each item is a row: red/amber dot + Branch Name + Avg Rating (e.g. `2.7 / 5.0`) + Flagged subjects count + [View Details →] link.

**Severity logic:** Red dot — avg rating <2.5 · Amber dot — avg rating 2.5–2.99.

**Filter (within card):** Show only Critical (red) / Show All.

**"View Details" →** Opens teacher performance breakdown drawer (560px) — per-teacher ratings, subjects, last observation date, pending CPD items.

**Empty state:** "All branches meeting teacher performance standards. Average rating ≥ 3.0 group-wide." — Green checkmark illustration.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cao/teacher-alerts/"` `hx-trigger="every 5m"` `hx-target="#teacher-alerts-section"` `hx-swap="innerHTML"`.

---

### 5.7 Upcoming Major Exams (14-Day Timeline)

> Timeline of all major exams across all branches scheduled in the next 14 days with approval status.

**Display:** Vertical timeline — each entry: Date badge (left) + Exam name + Stream + Class + Branch count + Approval status badge + Paper status badge.

**Status badges:**
- Approval: `Draft` (grey) · `Pending Approval` (yellow) · `Approved` (green) · `Live` (blue)
- Paper: `Paper Not Ready` (red) · `Paper Ready` (green) · `Answer Key Pending` (amber)

**Colour-coded date blocks:** Red if exam is <3 days away and paper not approved.

**Filter:** Exam type (Unit Test / Mid-term / Annual / Mock / Olympiad) — multi-select within card.

**Click on entry:** Opens exam detail drawer (560px) — full exam info, branch readiness table, conflict check.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cao/upcoming-exams/"` `hx-trigger="every 5m"` `hx-target="#exam-timeline"` `hx-swap="innerHTML"`.

---

### 5.8 Special Ed IEP Due Counter

> Alert counter for IEPs with overdue reviews — links directly to Special Education section.

**Display:** Alert card — large count number + "IEPs overdue for review" label. Background red if >0, green if 0.

**Below count:** List of up to 5 overdue IEPs — Student name (masked to initials for privacy), Branch, Days overdue, [Review →] link.

**"View All IEPs →"** links to `/group/acad/special-ed/`.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cao/iep-overdue/"` `hx-trigger="every 5m"` `hx-target="#iep-due-card"` `hx-swap="innerHTML"`.

---

### 5.9 Result Publication Queue

> Results approved and awaiting final publication across branches — status strip.

**Display:** Horizontal status strip — one pill per pending result set. Each pill: Exam name (truncated) + Branch + Status badge ([Publish Now] button if CAO-approved and ready).

**Publish action:** `hx-post="/api/v1/group/{group_id}/acad/results/{result_id}/publish/"` — confirms with modal ("Publish results for [Exam] to [N] branches?"). On success: result goes live + toast.

**"View Full Queue →"** links to Result Moderation `/group/acad/result-moderation/`.

---

### 5.10 Recent Academic Decisions (Audit Trail)

> Last 10 CAO actions with timestamp and branch — quick reference and accountability.

**Display:** Table — compact, 10 rows, no pagination.

**Columns:** # | Action | Subject/Exam/Branch | Timestamp | Outcome (Approved / Rejected / Published) | Reference ID.

**Click on row:** Opens read-only audit detail modal (420px) with full action context.

**"View Full Audit Log →"** links to `/group/acad/audit-log/`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `approval-detail` (from Approval Queue cards)
- **Width:** 560px
- **Tabs:** Details · History · Action
- **Details tab:** Full approval request context — what is being approved, who submitted, when, rationale, attached files (exam paper PDF preview / result report)
- **History tab:** Previous approvals/rejections for this item type from this branch
- **Action tab:** [Approve with optional comment] [Reject with required reason (min 20 chars)] [Request More Info]
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/approvals/{approval_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.2 Drawer: `branch-curriculum-detail` (from Curriculum Coverage chart click)
- **Width:** 560px
- **Tabs:** Coverage · Lesson Plans · Topics Pending
- **Coverage tab:** Subject-wise coverage % table for the selected branch — sortable
- **Lesson Plans tab:** Submission rate per teacher, pending plans count, last submission date
- **Topics Pending tab:** List of topics not yet covered — subject, chapter, expected coverage date
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/branches/{branch_id}/curriculum-detail/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.3 Drawer: `stream-result-detail` (from Stream Result Summary cards)
- **Width:** 640px
- **Tabs:** Branch Scores · Subject Breakdown · Rank Distribution
- **Branch Scores tab:** All branches for this stream — sortable table: Branch, Avg Score, Pass %, Toppers count, Rank
- **Subject Breakdown tab:** Per-subject avg marks + pass % — horizontal bar chart
- **Rank Distribution tab:** Stacked bar — score bands (A/B/C/D/F) per branch
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/cao/stream-results/{stream_id}/detail/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.4 Modal: `result-publish-confirm`
- **Width:** 420px
- **Content:** "Publish results for [Exam Name] to [N] branches? Students will be able to view their results immediately."
- **Warning text:** "This action cannot be undone. Ensure answer keys are finalised before publishing."
- **Buttons:** [Publish Results] (primary green) + [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/results/{result_id}/publish/"` — toast + audit log

### 6.5 Modal: `approval-reject` (from Approval Queue reject action)
- **Width:** 400px
- **Fields:** Reason (textarea, required, min 20 chars) · Notify submitter via (checkbox: System notification / WhatsApp / Email)
- **Buttons:** [Confirm Rejection] (danger red) + [Cancel]

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Approval recorded | "Approval recorded and notified to submitter" | Success (green) | 4s auto-dismiss |
| Rejection submitted | "Rejection recorded with reason. Submitter notified." | Success | 4s |
| Result published | "Results for [Exam] published across [N] branches." | Success | 5s |
| IEP review signed off | "IEP review sign-off recorded for [Student initials], [Branch]." | Success | 4s |
| KPI load error | "Failed to load academic KPI data. Retrying in 60s…" | Error (red) | Manual dismiss |
| Page data refresh | "Dashboard refreshed" | Info | 3s |
| Export triggered | "Academic report export started — download will begin shortly." | Info | 4s |
| Approval queue empty | "All approval queues are clear." | Info | 3s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No pending approvals | Checkmark circle | "All approvals are clear" | "No academic approvals require your attention right now." | — |
| No exam conflicts | Calendar with check | "No scheduling conflicts" | "All branch exam schedules are conflict-free." | — |
| No teacher alerts | Star icon | "All teachers performing well" | "No branches have teacher ratings below 3.0." | — |
| No upcoming exams (14 days) | Calendar outline | "No exams in the next 14 days" | "No major exams are scheduled in the next two weeks." | [View Exam Calendar] |
| No IEPs overdue | Shield check | "All IEP reviews are current" | "No student IEPs are past their review date." | — |
| No result queue items | Document check | "No results pending publication" | "All approved results have been published." | — |
| No curriculum data | Chart outline | "Curriculum data unavailable" | "Syllabus configuration is pending for one or more branches." | [Go to Syllabus Manager] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + gauge placeholder + curriculum chart skeleton + approval queue (4 skeleton cards) |
| KPI card auto-refresh | Subtle shimmer over existing card values (no layout shift) |
| Approval action (Approve/Reject click) | Spinner inside button + button disabled during API call |
| Curriculum chart filter change | Chart area shimmer + spinner centred in chart space |
| Stream result card click (drawer open) | Spinner in drawer body |
| Result publish confirm | Spinner inside [Publish Results] button + button disabled |
| Health score gauge refresh | Gauge arc animates from current to new value |
| IEP counter refresh | Number ticks from old to new value with shimmer |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | All other Div-B roles |
|---|---|---|
| Page itself | ✅ Rendered | ❌ Redirected to own dashboard |
| Alert Banner | ✅ Shown | N/A |
| [Approve] / [Reject] in Approval Queue | ✅ Enabled | N/A |
| [Publish Now] in Result Queue | ✅ Enabled | N/A |
| [Download Academic Report] header button | ✅ Shown | N/A |
| Stream result detail drawer — all tabs | ✅ Full access | N/A |
| Teacher performance alert list | ✅ Shown | N/A |
| IEP overdue counter + list | ✅ Shown | N/A |
| Audit trail table | ✅ Shown | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/cao/dashboard/` | JWT (G4) | Full page data — KPIs, alerts, approvals, widgets |
| GET | `/api/v1/group/{group_id}/acad/cao/kpi-cards/` | JWT (G4) | KPI card values only (for auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/cao/health-score/` | JWT (G4) | Academic health score + sub-component breakdown |
| GET | `/api/v1/group/{group_id}/acad/cao/curriculum-coverage/` | JWT (G4) | Branch curriculum coverage chart data (filter: stream, term) |
| GET | `/api/v1/group/{group_id}/acad/cao/stream-results/` | JWT (G4) | Stream result summary — 4 streams, term avg + delta |
| GET | `/api/v1/group/{group_id}/acad/cao/stream-results/{stream_id}/detail/` | JWT (G4) | Full stream result detail for drawer |
| GET | `/api/v1/group/{group_id}/acad/cao/branch-rankings/` | JWT (G4) | Top 5 / Bottom 5 branches by academic health |
| GET | `/api/v1/group/{group_id}/acad/cao/teacher-alerts/` | JWT (G4) | Branches with avg teacher rating <3.0 |
| GET | `/api/v1/group/{group_id}/acad/cao/upcoming-exams/` | JWT (G4) | Major exams in next 14 days across all branches |
| GET | `/api/v1/group/{group_id}/acad/cao/iep-overdue/` | JWT (G4) | Overdue IEP reviews count + list |
| GET | `/api/v1/group/{group_id}/acad/approvals/?role=cao` | JWT (G4) | CAO-level approval queue (all types) |
| POST | `/api/v1/group/{group_id}/acad/approvals/{approval_id}/approve/` | JWT (G4) | Approve item |
| POST | `/api/v1/group/{group_id}/acad/approvals/{approval_id}/reject/` | JWT (G4) | Reject with reason |
| GET | `/api/v1/group/{group_id}/acad/approvals/{approval_id}/` | JWT (G4) | Approval detail for drawer |
| GET | `/api/v1/group/{group_id}/acad/results/publication-queue/` | JWT (G4) | Results pending publication |
| POST | `/api/v1/group/{group_id}/acad/results/{result_id}/publish/` | JWT (G4) | Publish results to branches |
| GET | `/api/v1/group/{group_id}/acad/branches/{branch_id}/curriculum-detail/` | JWT (G4) | Branch curriculum detail for drawer |
| GET | `/api/v1/group/{group_id}/acad/cao/audit-trail/?limit=10` | JWT (G4) | Last 10 CAO actions |
| GET | `/api/v1/group/{group_id}/acad/cao/report/?format=pdf` | JWT (G4) | Download academic report PDF |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../cao/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Health score auto-refresh | `every 5m` | GET `.../cao/health-score/` | `#health-score-card` | `innerHTML` |
| Curriculum chart stream filter | `change` | GET `.../cao/curriculum-coverage/?stream={val}&term={val}` | `#curriculum-chart` | `innerHTML` |
| Branch bar click (curriculum) | `click` | GET `.../branches/{id}/curriculum-detail/` | `#drawer-body` | `innerHTML` |
| Stream result card click | `click` | GET `.../cao/stream-results/{stream_id}/detail/` | `#drawer-body` | `innerHTML` |
| Teacher alert list refresh | `every 5m` | GET `.../cao/teacher-alerts/` | `#teacher-alerts-section` | `innerHTML` |
| Upcoming exams refresh | `every 5m` | GET `.../cao/upcoming-exams/` | `#exam-timeline` | `innerHTML` |
| IEP counter refresh | `every 5m` | GET `.../cao/iep-overdue/` | `#iep-due-card` | `innerHTML` |
| Approval detail open | `click` | GET `.../acad/approvals/{id}/` | `#drawer-body` | `innerHTML` |
| Approve button | `click` | POST `.../acad/approvals/{id}/approve/` | `#approval-queue` | `innerHTML` |
| Reject button | `click` | (opens modal — no direct HTMX swap) | — | — |
| Reject confirm (modal) | `click` on Confirm | POST `.../acad/approvals/{id}/reject/` | `#approval-queue` | `innerHTML` |
| Result publish confirm | `click` on Publish | POST `.../acad/results/{id}/publish/` | `#result-publication-strip` | `innerHTML` |
| Branch rankings manual refresh | `click` on ↺ | GET `.../cao/branch-rankings/` | `#branch-rankings-card` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
