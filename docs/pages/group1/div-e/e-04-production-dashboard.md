# E-04 — Production Dashboard

> **Route:** `/content/video/production/`
> **Division:** E — Video & Learning
> **Primary Role:** Content Producer — Video (82)
> **Supporting Roles:** All production roles (83–89) — read own stage KPIs; Content Director (18) — read-only; Video Curator (31) — read-only
> **File:** `e-04-production-dashboard.md`
> **Priority:** P1
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Production Dashboard
**Route:** `/content/video/production/`
**Part-load routes:**
- `/content/video/production/?part=kpi-strip` — KPI tiles (polled every 60s)
- `/content/video/production/?part=pipeline-chart` — pipeline stage chart
- `/content/video/production/?part=overdue-alerts` — overdue jobs alert strip
- `/content/video/production/?part=throughput-chart` — throughput chart
- `/content/video/production/?part=my-stage-summary` — role-specific stage panel (non-Producer roles)

---

## 2. Purpose

The Production Dashboard is the command view for the Content Producer (82). It shows the health of the entire video production pipeline at a glance: how many jobs are at each stage, which are overdue, who is blocked, and what the weekly throughput looks like.

Non-Producer production roles (83–89) see a filtered view of only their own stage queue — the dashboard is their starting point to know "what do I need to work on today?"

**Business goals:**
- Prevent SLA breaches: Producer sees overdue jobs before they become blockers
- Balance workload across Scriptwriters, Animators, Editors, etc.
- Track pipeline velocity to forecast when MCQ-linked videos will be ready for students
- Surface blocked jobs (e.g. script awaiting review > 48h)

---

## 3. KPI Strip (Content Producer view)

Eight tiles, `hx-trigger="every 60s"`. Colour coding on overdue tiles.

| Tile | Value | Colour Rule | Click Action |
|---|---|---|---|
| Total Active Jobs | Count of non-terminal jobs | — | → E-05 All Jobs |
| Brief Pending | Jobs in BRIEF_PENDING state | Amber if > 10 | → E-05 filtered |
| In Script | SCRIPT_DRAFT + SCRIPT_REVIEW | — | → E-05 filtered |
| In Production | VOICE_OVER_IN_PROGRESS + ANIMATION_IN_PROGRESS + GRAPHICS_IN_PROGRESS | — | → E-05 filtered |
| In Edit | EDIT_IN_PROGRESS + AWAITING_SUBTITLE + SUBTITLE_IN_PROGRESS | — | → E-05 filtered (hover tooltip: "Includes jobs awaiting subtitle completion") |
| QA Review | QA_REVIEW | — | → E-08 QA Queue |
| Publish Queue | PUBLISH_QUEUE | — | → E-11 Publish Queue |
| Overdue | Jobs past SLA due date (any stage) — includes On Time · Overdue · Critical (>2× SLA) | Red if > 0 | → E-05 filtered: overdue only |

**KPI Strip (non-Producer roles — 83–89):**
Simplified 4-tile strip showing only their stage:
- My Assigned Jobs (total)
- In Progress (started)
- Submitted (awaiting approval)
- Overdue (past stage SLA)

Skeleton: rectangle shimmers matching tile count.

---

## 4. Overdue Alerts Strip

Shown below KPI strip if any jobs are overdue. Red background banner:

> ⚠️ **{N} jobs are overdue** — [{N} script] [{N} voice-over] [{N} animation] [{N} graphics] [{N} edit] [{N} subtitle] [{N} QA] — [View All Overdue →]

Each bracketed count is a link → E-05 filtered to that stage + overdue. Stages with 0 overdue jobs are hidden from the strip (not shown as "[0 voice-over]"). Strip is hidden entirely if all stages have 0 overdue.

If no overdue jobs: strip is hidden (not an empty state — simply absent).

---

## 5. Charts Section

All charts use Recharts `ResponsiveContainer`. No-data: grey placeholder + "No data yet".

---

### Chart 1 — Pipeline Stage Distribution (Bar Chart)

**Purpose:** Show how many jobs are at each stage right now.

- Horizontal bar chart
- Y-axis: stages (Brief Pending · Script Draft · Script Review · Script Approved · Voice Over · Animation · Graphics · Edit · Awaiting Subtitle · Subtitle · QA · Publish Queue)
- X-axis: job count
- Bar colour: blue (normal) · amber (stage has overdue jobs) · red (stage has critically overdue jobs — Critical: >2× SLA)
- Note below chart: "Voice Over, Animation, and Graphics run in parallel after script approval."
- Toggle: All Jobs / MCQ-Linked / Standalone
- Click a bar → navigates to E-05 filtered to that stage

---

### Chart 2 — Weekly Throughput (Line Chart)

**Purpose:** How many jobs moved to PUBLISHED each week over the last 12 weeks.

- X-axis: week labels (W1, W2 … W12)
- Y-axis: jobs published
- Single line with dots. Hover: tooltip with count and week date range
- Toggle: 4 weeks / 12 weeks / 26 weeks
- Reference line: "Target" (from E-12 config if set)

---

### Chart 3 — SLA Compliance by Stage (Bar Chart)

**Purpose:** What % of jobs at each stage were completed within their stage SLA.

- Grouped bar: one bar per stage
- Colour: Green ≥80% · Amber 60–79% · Red <60%
- Period: last 30 days (fixed)
- Tooltip: "{stage}: {N} on time / {M} total = {%}%"

---

### Chart 4 — MCQ-Linked vs Standalone (Pie Chart)

**Purpose:** Show the proportion of production jobs that are linked to MCQ questions vs manually created.

- Two slices: MCQ-Linked (blue) · Standalone (grey)
- Legend shows exact counts
- Click slice → E-05 filtered by source type

---

## 6. My Stage Panel (Non-Producer Roles)

Shown **instead of** the full chart section for roles 83–89. Layout: page is divided into KPI strip (top) + My Queue table (center) + two side cards (bottom).

### Role-Specific KPI Strip (4 tiles, `hx-trigger="every 60s"`)

KPI tiles are filtered to the current user's assigned jobs only:

| Role | Tile 1 | Tile 2 | Tile 3 | Tile 4 |
|---|---|---|---|---|
| Scriptwriter (83) | My Scripts — Total | In Draft (`video_script.status = DRAFT` assigned to me) | Submitted (status = SUBMITTED, waiting for review) · Revision Feedback (status = REVISION_REQUESTED returned to me) | Overdue (red if >0) |
| Script Reviewer (84) | Awaiting My Review (`video_script.status = SUBMITTED` where my stage assignment is active — assigned scripts only, not unassigned queue) | Reviewed Today | Revision Requests Sent | Avg Review Time (days, 30d) |
| Animator (85) | My Animation Jobs | In Progress | Submitted for Acceptance | Overdue (red if >0) |
| Graphics Designer (86) | My Graphics Jobs | In Progress | Submitted for Acceptance | Overdue (red if >0) |
| Video Editor (87) | My Edit Jobs | In Progress | Submitted for Acceptance | Overdue (red if >0) |
| Subtitle Editor (88) | Languages Pending | EN Incomplete | HI/TE/UR Incomplete | QA Failed Subtitles |
| QA Reviewer (89) | In My Queue | Reviewed Today | Pass Rate (30d, %) | Avg Review Time (min, 30d) |

Colour rules:
- Overdue tile: red if > 0
- Awaiting My Review (Script Reviewer): amber if > 5; red if > 10
- Pass Rate (QA Reviewer): red if < 70%

Skeleton: 4 rectangle shimmers.

### My Queue Table (center, full-width)

Sortable, paginated (25 rows), responsive.

**Common columns for all roles:**

| Column | Sortable | Notes |
|---|---|---|
| Job Title | Yes | Click → opens relevant workspace (E-06 for Scriptwriter/Reviewer; E-07 for Animator/Graphics/Editor; E-08 for QA; E-09 for Subtitle) |
| Subject · Topic | No | — |
| Content Type | No | Pill |
| Priority | No | Colour-coded |
| Stage SLA | No | "Day {N} of {total}" — red if overdue |
| Stage Status | No | Colour-coded pill (In Progress · Submitted · Revision Requested) |
| Actions | No | Role-specific CTA (see below) |

**Role-specific Action column:**

| Role | CTA |
|---|---|
| Scriptwriter (83) | [Open Editor] (→ E-06 full-page editor) |
| Script Reviewer (84) | [Review] (→ E-06 review workspace) |
| Animator (85) | [Upload Animation] (→ E-07 upload modal pre-filled) |
| Graphics Designer (86) | [Upload Graphics] (→ E-07 upload modal pre-filled) |
| Video Editor (87) | [Upload Final Edit] (→ E-07 upload modal pre-filled) |
| Subtitle Editor (88) | [Upload Subtitle] (→ E-09 upload modal pre-filled) |
| QA Reviewer (89) | [Start Review] (→ E-08 QA workspace) |

**Default sort:** Stage SLA ASC (most urgent first).

**Empty state:** "No jobs assigned to you right now. The Producer will assign work when new jobs are ready."

**Responsive:**
- Desktop: full columns
- Tablet: Job Title · Stage Status · SLA · Actions
- Mobile: card — title + status pill + SLA badge + CTA

### Bottom Row — Two Cards

**"Submitted / Awaiting Review" card (left, 50%):**
- Jobs I have submitted that are pending Producer/Reviewer acceptance
- Each row: job title · submitted {N} days ago · current status
- Waiting > stage SLA: row turns amber with "⚠️ Overdue for review"
- "Nudge Producer" link (sends Div E notification to assigned Producer: "{Role} is waiting for review on '{title}' — submitted {N} days ago.")

**"Recently Completed" card (right, 50%):**
- Jobs where my stage was APPROVED in the last 14 days
- Each row: job title · approved {N} days ago · ✅ badge
- Stat footer: "You completed {N} jobs this month."

**Part-load route:** `/content/video/production/?part=my-stage-summary&role={role_id}` — HTMX loads this section independently.

---

## 7. Recent Activity Feed

Below charts (Producer view only). Newest-first log of pipeline events:

| Event | Example |
|---|---|
| New job created | "Job created: Physics — Optics — Reflection (MCQ-linked)" |
| Stage completed | "Script approved for: Algebra — Quadratic Equations" |
| Job overdue | "🔴 OVERDUE: Chemistry — Organic — Esterification (Animation stage, 2d overdue)" |
| Job published | "✅ Published: GK — Polity — Preamble to YouTube" |
| Stage revision requested | "Revision requested on script: Biology — Genetics — Mendel's Laws" |

- Shows last 20 events. "View Full Activity →" link → E-10 Production Analytics activity log.
- `hx-trigger="every 30s"` auto-refresh.

---

## 8. Quick Actions Panel (Content Producer only)

Right sidebar (280px, desktop only) or below content on tablet/mobile.

| Action | Destination |
|---|---|
| + New Production Job | Opens Create Job modal (see E-05) |
| Import from MCQ Bank | → E-05 bulk import from D-11 |
| View Publish Queue | → E-11 |
| SLA Configuration | → E-12 |
| Production Analytics | → E-10 |

---

## 9. Access Control

| Gate | Rule |
|---|---|
| Page access | All Div E production roles (82–89), Content Director (18), Video Curator (31) |
| Full dashboard view (all charts, all KPIs, activity feed, quick actions) | Content Producer (82), Content Director (18) |
| My Stage Panel | Roles 83–89 — see only their own stage data |
| Write actions (Quick Actions, New Job button) | Content Producer (82) only |
| Role-based UI | Non-Producer roles: quick actions panel hidden; overdue strip read-only |
| Video Curator (31) view | Full dashboard read-only — same view as Content Director (18): KPI tiles, all charts, activity feed, overdue strip. Quick Actions panel is hidden. No write actions. Video Curator does not receive a My Stage Panel — they are not a production role. |

---

## 10. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| No active jobs in pipeline | KPI tiles all show 0. Charts show no-data state. Activity feed shows "No recent activity." |
| Analytics data older than 1h | Cache used (Memcached). Tiles show "Last updated: {N}m ago" label. |
| All jobs on-time | Overdue strip absent. SLA compliance chart shows all green bars. |
| Non-Producer has no assigned jobs | My Queue card shows empty state: "No jobs assigned to you at this stage." |
| Pipeline stage with > 100 jobs | Bar chart shows count as-is; clicking → E-05 with pagination. |

---

## 11. UI Patterns

### Toast Messages

| Action | Toast |
|---|---|
| Dashboard loaded fresh data | — (silent refresh, no toast) |
| Navigate-away action (e.g. "View All Overdue") | No toast — navigates directly |

### Loading States

- KPI strip: rectangle shimmers (8 tiles for Producer, 4 for others)
- Charts: grey rectangle placeholders matching chart dimensions
- Activity feed: 5-row shimmer (icon + 2 text lines per row)
- My Stage Panel: 3 card shimmers

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | KPI strip + charts 2×2 grid + activity feed + right quick-actions sidebar |
| Tablet (768–1279px) | Charts stack vertically; quick actions move below charts |
| Mobile (<768px) | KPI strip scrolls horizontally; charts hidden (link to E-10 for analytics); My Stage card only |

---

*Page spec complete.*
*E-04 covers: pipeline health command view → overdue alerts → throughput charts → stage distribution → role-specific queue view.*
