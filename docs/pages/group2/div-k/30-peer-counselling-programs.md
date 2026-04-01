# 30 — Peer Counselling Programs

> **URL:** `/group/welfare/counselling/peer-programs/`
> **File:** `30-peer-counselling-programs.md`
> **Template:** `portal_base.html`
> **Priority:** P2
> **Primary Role:** Group Counselling Head (Role 94, G3)

---

## 1. Purpose

Peer counselling programs train senior students (Class 11–12) as peer supporters who provide first-level emotional support to fellow students — listening, referring to professional counsellors, and flagging crisis situations early. Unlike professional counselling sessions tracked on page 21 (Counselling Session Register), peer counselling is delivered by trained student volunteers, operating under the direct supervision of the branch counsellor and the oversight of the Group Counselling Head. The program operates across three interconnected components: (a) Peer Counsellor selection and training — identifying suitable student volunteers, enrolling them, and equipping them with skills in active listening, empathy, and crisis recognition; (b) Program delivery — structured group sessions, peer listening hours, and awareness events held at branch level; and (c) Referral tracking — the pipeline of students flagged by peer counsellors to professional counsellors, ensuring that peer detection of distress translates into formal clinical support without delay.

The Group Counselling Head manages this program group-wide. Responsibilities include: designing the peer counselling curriculum and training methodology; training branch counsellors who then deliver training to peer counsellors at each branch; monitoring program delivery (session frequency, attendance, topic coverage) across all branches; tracking referral rates from peer counsellors to professional counsellors and auditing intake outcomes; identifying branches with weak or absent programs and driving corrective action; coordinating the annual refresher training cycle for all active peer counsellors; and compiling the annual peer counselling program report for leadership and regulatory submission. Large groups run structured programs with 5–10 trained peer counsellors per branch; smaller branches may operate informal programs with 2–4 volunteers. Scale: 20–50 branches · 5–10 peer counsellors per branch · 100–500 peer counsellors total · 200–1,000 peer sessions per year.

This page was identified as missing in the 15-pass audit. It is referenced in two existing pages: page 05 (Counselling Head Dashboard) includes a "Peer Counselling Programs This Month" KPI card that links here, and page 21 (Counselling Session Register) tracks referrals from peer counsellors to professional counsellors. Without this page, the Counselling Head has no centralised mechanism to manage peer counsellor enrolment, monitor program delivery, respond to crisis escalations from peer counsellors, or report on the program's reach and effectiveness. This gap leaves a significant welfare mechanism unmanaged at the group level.

---

## 2. Role Access

| Role | Level | Access | Django Decorator |
|---|---|---|---|
| Group Counselling Head | G3, Role 94 | Full — all branches, all peer counsellors, all sessions, all referrals; can enrol/deactivate peer counsellors, record sessions, plan training, respond to crisis flags | `@require_role([94])` |
| Branch Counsellor | Branch, G2 | Own branch only — can view own branch peer counsellors, enrol peer counsellors at own branch, record own branch sessions; cannot see other branches | `@require_role([94, 'branch_counsellor'])` with `queryset.filter(branch=request.user.branch)` |
| Branch Principal | Branch, G2 | Own branch read-only — branch program status, session count, trained peer counsellor list; no edit actions | `@require_role_branch(['principal'])` with read-only flag |
| Group COO | G4 | Aggregate read-only — KPI bar and branch program status matrix; no individual peer counsellor records or session details | `@require_role(['coo'])` with aggregate-only queryset |
| All other roles | — | No access — 403 redirect | — |

> **Access enforcement:** All peer counsellor records, session records, and referral records are queryset-filtered by `group_id` from the URL path. Branch Counsellor objects are further filtered to `branch=request.user.branch`. Student names in the peer counsellor directory are visible to the Group Counselling Head and the assigned Branch Counsellor only — Branch Principals see student names at their own branch. Referral records display the referring peer counsellor's name only to the Counselling Head and the branch counsellor; concern descriptions are anonymised for all roles. Crisis escalation records are visible to the Counselling Head and the relevant Branch Counsellor immediately; Branch Principals are notified but cannot view clinical detail.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Counselling  ›  Peer Counselling Programs
```

### 3.2 Page Header
- **Title:** `Peer Counselling Programs`
- **Subtitle:** `[N] Branches · [N] Active Programs · [N] Peer Counsellors · [N] Sessions This Month · [N] Referrals This Month`
- **Right controls:** `+ Enrol Peer Counsellor` (Counselling Head + Branch Counsellor) · `Record Session` (Counselling Head + Branch Counsellor) · `Schedule Refresher Training` (Counselling Head only) · `Export Program Report` (Counselling Head only)

### 3.3 Alert Banner

Banners are shown in priority order — Red first, then Amber. Maximum 5 banners shown simultaneously; "View all alerts →" link below if more exist.

| Condition | Banner Text | Severity |
|---|---|---|
| Crisis escalation unacknowledged > 2 hours | "Peer counsellor crisis flag at [Branch Name] raised [N] hour(s) ago has not been acknowledged by the Branch Counsellor or Counselling Head. Immediate professional response required." | Red |
| Branch with no peer counsellors and no professional counsellor | "Branch [Name] has no trained peer counsellors and no active professional counsellor. Students at this branch have no counselling access. Urgent action required." | Red |
| Crisis flag with no follow-up session within 48 hours | "A peer-flagged crisis at [Branch] on [date] has no follow-up professional counselling session recorded. Outcome unknown." | Red |
| Peer counsellor refresher training overdue (more than 12 months since training) | "[N] peer counsellor(s) at [M] branch(es) are overdue for their annual refresher training." | Amber |
| Branch with no sessions this month | "[N] branch(es) with an active peer counselling program have logged no sessions this month." | Amber |

---

## 4. KPI Summary Bar

Eight cards arranged in a responsive 4×2 grid. All metrics apply to the current calendar month by default; Branch Counsellors and Branch Principals see their own branch's metrics only. Cards with a non-zero compliance failure count are clickable and drill down to the relevant section with a pre-applied filter.

| # | Card Title | Metric | Colour Rule | Drill-down |
|---|---|---|---|---|
| 1 | Branches with Active Peer Program | Branches that have logged at least 1 session this calendar month / total branches with an enrolled peer counsellor | Green = 100% · Amber < 80% · Red < 60% | → Branch Program Status Matrix filtered to sessions this month > 0 |
| 2 | Trained Peer Counsellors Total | Count of peer counsellors with status = Active across all branches | Blue always (informational) | → Peer Counsellor Directory |
| 3 | Peer Sessions This Month | Count of all session records in the current calendar month | Blue always (informational) | → Branch Status Matrix sorted by sessions this month descending |
| 4 | Branches with No Peer Session This Month | Count of branches that have active peer counsellors but zero sessions logged this month | Green = 0 · Amber ≥ 1 | → Branch Status Matrix filtered to sessions this month = 0 |
| 5 | Referrals Raised This Month | Count of referrals flagged by peer counsellors to professional counsellors in the current month | Blue always (informational) | → Referral Pipeline section |
| 6 | Peer Counsellors Due for Refresher | Count of active peer counsellors whose last training was > 12 months ago | Green = 0 · Amber ≥ 1 | → Peer Counsellor Directory filtered to refresher_due = true |
| 7 | Crisis Escalations This Month | Count of sessions where a crisis flag was raised by a peer counsellor in the current month | Green = 0 · Red ≥ 1 | → Referral Pipeline section filtered to crisis_flag = true |
| 8 | Branches with No Trained Peer Counsellors | Count of branches where total active peer counsellors = 0 | Green = 0 · Amber ≥ 1 | → Branch Status Matrix filtered to active_peer_counsellors = 0 |

**Auto-refresh:** KPI bar refreshes automatically every 10 minutes using `hx-trigger="every 600s"`. Cards 7 (Crisis Escalations) and 4 (Branches with No Peer Session) have a visual pulse animation when their value is non-zero.

---

## 5. Sections

### 5.1 Branch Program Status Matrix

The primary overview — one row per branch, showing the health of the peer counselling program at each location.

**Search:** Free-text on branch name. 300ms debounce. Minimum 2 characters.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Program Status | Checkbox | Active · Inactive · Not Started |
| Sessions This Month | Radio | All · Has Sessions · No Sessions |
| Crisis Flags | Toggle | Show only branches with a crisis flag this month |
| Training Compliance | Radio | All · Fully Compliant · Partially Compliant · Non-Compliant |
| Active Peer Counsellors | Radio | All · Has Counsellors · None |
| Branch | Multi-select | All branches |

**Table Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Branch short name; click opens `branch-peer-program-detail` drawer |
| Active Peer Counsellors | ✅ | Integer count; Red = 0; Amber = 1–2; Green ≥ 3 |
| Sessions This Month | ✅ | Integer; Grey = 0; Blue ≥ 1 |
| Referrals This Month | ✅ | Integer count; Blue ≥ 1; Grey = 0 |
| Last Session Date | ✅ | DD-MMM-YYYY; Amber if > 30 days ago for an Active program; Grey "—" if never |
| Training Compliance % | ✅ | % of active peer counsellors trained within last 12 months; Red < 80%; Amber 80–99%; Green = 100% |
| Crisis Flags This Month | ✅ | Integer; Red badge if ≥ 1; Green = 0 |
| Program Status | ✅ | Active (Green) · Inactive (Amber) · Not Started (Grey) badge |
| Actions | ❌ | View · Record Session · Enrol Counsellor |

**Default sort:** Crisis Flags This Month descending, then Sessions This Month ascending (least active first within no-crisis branches).
**Pagination:** Server-side · 25 rows/page.
**Row highlight:** Branches with a crisis flag this month have a red left border. Branches with zero sessions and active peer counsellors have an amber left border.

---

### 5.2 Peer Counsellor Directory

Searchable, filterable list of all peer counsellors across all branches. This is the master roster of trained student volunteers.

**Search:** Student name, class/section, branch. 300ms debounce.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Status | Checkbox | Active · Graduated · Inactive · Suspended |
| Class | Checkbox | Class 11 · Class 12 |
| Refresher Due | Toggle | On = show only counsellors whose refresher is overdue |
| Training Year | Single-select | Current year + 2 prior years |

**Table Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Student Name | ✅ | Full name (visible to Counselling Head and own Branch Counsellor; Branch Principal sees names at own branch) |
| Class / Section | ✅ | e.g., "Class 12 – A" |
| Branch | ✅ | |
| Initial Training Date | ✅ | DD-MMM-YYYY — date of first peer counsellor training |
| Last Training Date | ✅ | Most recent training (initial or refresher) |
| Refresher Due | ✅ | Date (Initial Training Date + 12 months); Red if past; Amber if ≤ 30 days |
| Referrals Made | ✅ | Integer count — total referrals raised since enrolment |
| Status | ✅ | Active (Green) · Graduated (Blue) · Inactive (Grey) · Suspended (Amber) badge |
| Actions | ❌ | View Profile · Deactivate (Counselling Head + own Branch Counsellor) |

**Default sort:** Branch alphabetically, then Status (Active first), then Initial Training Date descending.
**Pagination:** Server-side · 25 rows/page.

---

### 5.3 Session Volume Chart

Visual overview of session delivery across branches and over time. Rendered below the Peer Counsellor Directory on desktop (full-width); stacked on mobile.

- **Primary series (bars):** Count of sessions per branch for the current month (X-axis: branch names; Y-axis: session count). Bar colour: Blue for branches with sessions; Light grey for branches with zero sessions.
- **Overlay line:** Monthly session count trend for the past 6 months, group-wide (second Y-axis on right, integer).
- **Tooltip:** Branch name · Sessions this month (bar series) OR Month · Total sessions (line series).
- **Interaction:** Clicking a bar in the chart filters Section 5.1 to that branch.
- **Data source:** `GET /api/v1/group/{group_id}/welfare/counselling/peer-programs/session-chart/`

---

### 5.4 Referral Pipeline

A dedicated section tracking all peer-counsellor-raised referrals — students flagged by peer counsellors to professional counsellors. This is the critical handoff point where peer support connects to clinical support.

**Search:** Branch name, intake status. 300ms debounce.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Intake Status | Checkbox | Accepted · Pending · Declined · In Progress |
| Crisis Flag | Toggle | Show only crisis-level referrals |
| Date Range | Date range picker | Date referral was raised |
| Month | Single-select | Current + 5 prior months |

**Table Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Referral ID | ✅ | System-generated (e.g., PR-2026-00042) |
| Branch | ✅ | |
| Date Raised | ✅ | DD-MMM-YYYY |
| Concern (Anonymised) | ❌ | Free-text description anonymised: "Student [S-XXXX] expressed concern about…" — student not named in this table |
| Crisis Flag | ✅ | Yes (Red badge) · No (Grey) |
| Intake Status | ✅ | Accepted (Green) · Pending (Amber) · Declined (Red) · In Progress (Blue) badge |
| Professional Counsellor | ✅ | Name of counsellor who received the referral; "Unassigned" in Amber if still pending |
| Intake Date | ✅ | DD-MMM-YYYY or "—" |
| Outcome | ✅ | Ongoing · Resolved · Escalated Further · No Show · "—" if pending |
| Actions | ❌ | View Referral |

**Default sort:** Crisis Flag descending (crisis referrals first), then Date Raised descending.
**Pagination:** Server-side · 25 rows/page.

---

## 6. Drawers / Modals

### 6.1 Drawer — `branch-peer-program-detail` (640px, right side)

**Trigger:** Click on branch name in Program Status Matrix or "View" in Actions column.

**Header:** Branch Name · Program Status badge · Active Peer Counsellors count · Sessions This Month count

**Tabs:**

#### Tab 1 — Peer Counsellors
Table of all peer counsellors enrolled at this branch (past and present). Columns: Name · Class/Section · Status · Training Date · Refresher Due · Referrals Made · Actions (View Profile, Deactivate).

#### Tab 2 — Sessions
Chronological list of all session records for this branch. Columns: Date · Session Type · Counsellors Present · Participants Count · Topics Covered · Referrals Raised (count) · Crisis Flags · Recorded By.

#### Tab 3 — Referrals
All referrals raised by peer counsellors at this branch. Matches columns in Section 5.4 Referral Pipeline, pre-filtered to this branch.

#### Tab 4 — Training Log
All training events (initial and refresher) for peer counsellors at this branch.

| Column | Notes |
|---|---|
| Training Date | DD-MMM-YYYY |
| Training Type | Initial Training · Annual Refresher |
| Trainer / Supervisor | Name |
| Topics Covered | |
| Duration | Hours |
| Attendees | Names of peer counsellors who attended |
| Non-Attendees | Auto-calculated from active roster |
| Mode | In-Person · Online · Hybrid |

#### Tab 5 — Program History
Timeline of key program events: Program Started date, Enrollment waves, Status changes (Active / Inactive), reconstitution of peer counsellor cohort, and any formal program reviews. Read-only.

---

### 6.2 Drawer — `enroll-peer-counsellor` (560px, right side)

**Trigger:** `+ Enrol Peer Counsellor` page header button, or "Enrol Counsellor" in branch Actions column.

**Header:** "Enrol Peer Counsellor"

**Fields:**

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select | Required; auto-set for Branch Counsellor |
| Student Name | Autocomplete — branch student directory (debounce 300ms) | Required; must resolve to an actual student record |
| Class / Section | Read-only auto-filled from student record | Auto |
| Student ID | Read-only auto-filled | Auto |
| Class Validation | Inline check — must be Class 11 or Class 12 | Enforced: if Class < 11, validation error: "Peer counsellors must be enrolled from Class 11 or 12." |
| Selection Reason | Textarea (max 500 chars) — why this student was selected (good listener, empathetic, leadership qualities, teacher nomination, etc.) | Required; min 30 characters |
| Supervising Counsellor | Single-select (branch counsellors at selected branch) | Required |
| Initial Training Date | Date picker | Required; cannot be future date |
| Training Mode | Radio: In-Person · Online · Hybrid | Required |
| Trainer / Facilitator | Text input | Required |
| Training Duration (hours) | Number (1.0 – 16.0) | Required |
| Topics Covered in Training | Textarea (max 600 chars) — e.g., active listening, crisis recognition, referral protocol | Required |
| Consent Form | File upload — signed consent from student and guardian (PDF/JPG, max 10 MB) | Required; upload is mandatory before enrolment can be saved |
| Notes | Textarea (max 300 chars) | Optional |

**Footer:** `Cancel` · `Enrol Peer Counsellor`

**Validation summary:**
- Student must be Class 11 or Class 12 (hard block — cannot proceed if class < 11).
- Consent form upload is mandatory (file upload field; Save is disabled until file is attached).
- Selection Reason must be at least 30 characters.
- Training Date cannot be in the future.

**Behaviour on save:** New peer counsellor record created with Status = Active; Training Date recorded as Initial Training Date; Refresher Due = Training Date + 12 months; branch training compliance recalculates; toast shows success.

---

### 6.3 Drawer — `record-peer-session` (520px, right side)

**Trigger:** `Record Session` page header button, or "Record Session" in branch Actions column.

**Header:** "Record Peer Counselling Session"

**Fields:**

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select | Required; auto-set for Branch Counsellor |
| Session Date | Date picker | Required; cannot be future date |
| Session Type | Radio: Group Session · Awareness Event · Peer Listening Hour | Required |
| Peer Counsellors Present | Multi-select from this branch's active peer counsellor list | Required; at least 1 |
| Facilitating Counsellor | Single-select (branch counsellors at selected branch) | Required |
| Duration (minutes) | Number (15 – 240) | Required |
| Participants Count | Number (1 – 500) | Required |
| Topics Covered | Textarea (max 600 chars) — e.g., exam stress, peer pressure, body image, anti-bullying | Required |
| Referrals Raised | Number (0 – 50) | Required; defaults to 0 |
| Brief Referral Reason (if Referrals > 0) | Textarea (max 400 chars) — anonymised description of concern(s); no student names | Required if Referrals > 0; note displayed: "Do not include student names — describe concern categories only." |
| Any Crisis Flags | Radio: No · Yes | Required |
| Crisis Description (if Yes) | Textarea (max 600 chars) — nature of the flagged situation; anonymised | Required if Crisis Flags = Yes |

**Crisis Flag Conditional Reveal:** When "Any Crisis Flags = Yes" is selected, a new section slides into view below the radio buttons with:
- Crisis Description field (required, min 50 chars)
- Urgency Level radio: Moderate · High · Immediate
- Inline alert box: "Selecting Yes will trigger an immediate notification to the Branch Counsellor and Group Counselling Head. A professional counsellor must follow up within 24 hours (Moderate/High) or 2 hours (Immediate)."

**Footer:** `Cancel` · `Record Session`

**Behaviour on save:**
- Session record created; branch session count for the month increments.
- If Referrals > 0: referral records created in Referral Pipeline with Intake Status = Pending.
- If Crisis Flags = Yes: crisis escalation workflow triggered — portal notification sent to Branch Counsellor and Counselling Head immediately; a crisis alert entry is created; KPI Card 7 increments; alert banner fires if Counselling Head does not acknowledge within 2 hours.

---

### 6.4 Drawer — `peer-referral-detail` (480px, right side)

**Trigger:** "View Referral" in Referral Pipeline table Actions column.

**Header:** Referral ID · Branch · Date Raised · Crisis Flag badge · Intake Status badge

**Content:**

| Field | Notes |
|---|---|
| Referral ID | Read-only |
| Branch | Read-only |
| Date Raised | DD-MMM-YYYY |
| Peer Counsellor (Raised By) | Name shown only to Counselling Head and the branch's Branch Counsellor; all other authorised roles see "Peer Counsellor [anonymised]" |
| Concern Description | Anonymised: "Student [S-XXXX] expressed concern about [concern category]. [Brief description without identifying details]." Student name is never shown in this drawer regardless of role. |
| Crisis Flag | Yes (Red badge) / No |
| Urgency Level | Moderate · High · Immediate (shown only if crisis = Yes) |
| Professional Counsellor Assigned | Name or "Unassigned" |
| Intake Status | Accepted · Pending · Declined · In Progress badge |
| Intake Date | DD-MMM-YYYY or "—" |
| Intake Notes | Brief notes from the professional counsellor on intake (visible to Counselling Head and Branch Counsellor only) |
| Outcome | Ongoing · Resolved · Escalated Further · No Show · "—" |
| Outcome Date | If resolved/closed |
| Outcome Notes | Counsellor notes (Counselling Head and Branch Counsellor only) |

**Footer actions (Counselling Head and Branch Counsellor only):**
- `Assign Counsellor` — opens inline select of branch counsellors; auto-updates intake status to Accepted
- `Update Intake Status` — inline select: Accepted · Declined · In Progress
- `Update Outcome` — inline select + optional notes textarea

---

### 6.5 Drawer — `refresher-training-planner` (460px, right side)

**Trigger:** `Schedule Refresher Training` page header button. Counselling Head only.

**Header:** "Schedule Peer Counsellor Refresher Training"

**Fields:**

| Field | Type | Validation |
|---|---|---|
| Branches to Include | Multi-select — all branches (or "All Branches" toggle) | Required; at least 1 |
| Training Date | Date picker | Required; cannot be past date |
| Training Mode | Radio: In-Person · Online · Hybrid | Required |
| Trainer / Facilitator | Text input (max 200 chars) | Required |
| Topics to Cover | Multi-select: Active Listening · Crisis Recognition · Referral Protocol · Boundaries and Self-Care · Empathy Skills · Suicide Prevention Basics · Other | Required; at least 2 |
| Custom Topics (if Other) | Textarea (max 300 chars) | Required if Other is selected |
| Duration (hours) | Number (1.0 – 8.0) | Required |
| Target Peer Counsellors | Read-only summary — count of active peer counsellors at selected branches who are due for refresher; generated when branches are selected | Auto |
| Communication to Branch Counsellors | Toggle: Send Advance Notice Now (via portal notification + email) | Optional |

**Footer:** `Cancel` · `Schedule Training`

**Behaviour on save:** Training event created in the system; if Communication toggle is on, portal notifications sent to all branch counsellors at selected branches with training date, mode, and topic list; training event appears in Tab 4 (Training Log) for each relevant branch.

---

## 7. Toast Messages

| Action | Toast Text | Type | Duration |
|---|---|---|---|
| Peer counsellor enrolled | "Peer counsellor [Student Name] enrolled at [Branch]. Refresher due: [date]." | Success | 4s |
| Enrolment blocked — wrong class | "Peer counsellors must be from Class 11 or 12. Enrolment not allowed for this student." | Error | 6s |
| Enrolment blocked — no consent | "Consent form is required before enrolment. Please attach the signed consent form." | Error | 6s |
| Session recorded | "Session recorded at [Branch] on [date]. [N] referral(s) created." | Success | 4s |
| Session recorded with crisis flag | "Session recorded. Crisis flag raised at [Branch]. Branch Counsellor and Counselling Head have been notified." | Warning | 8s (persistent until dismissed) |
| Crisis unacknowledged alert | "Crisis flag at [Branch] raised [N] hours ago has not been acknowledged. Immediate attention required." | Error | Persistent |
| Referral intake updated | "Referral [ID] intake status updated to [status]." | Success | 3s |
| Referral assigned to counsellor | "Referral [ID] assigned to [Counsellor Name]. Intake status set to Accepted." | Success | 4s |
| Refresher training scheduled | "Refresher training scheduled for [N] branch(es) on [date]. [N] branch counsellors notified." | Success | 4s |
| Peer counsellor deactivated | "Peer counsellor [Student Name] deactivated at [Branch]. Record retained for audit." | Info | 4s |
| Export triggered | "Program report export is being prepared. Download will begin shortly." | Info | 3s |
| Validation error | "Please complete all required fields before saving." | Error | 5s |
| Crisis acknowledged | "Crisis escalation at [Branch] acknowledged. Follow-up required within [N] hours." | Success | 4s |

---

## 8. Empty States

| Context | Heading | Description | CTA |
|---|---|---|---|
| No branches have active programs | "No Peer Counselling Programs Found" | "No branches have started a peer counselling program yet. Enrol peer counsellors at a branch to get started." | `+ Enrol Peer Counsellor` button |
| Branch program status matrix — no branches match filters | "No Branches Match Filters" | "Try adjusting or clearing your filters to see program data." | `Clear Filters` button |
| Peer Counsellor Directory — no counsellors enrolled | "No Peer Counsellors Enrolled" | "No students have been enrolled as peer counsellors. Enrol students from Class 11 or 12 at each branch to begin the program." | `+ Enrol Peer Counsellor` button |
| Peer Counsellor Directory — no results for search | "No Peer Counsellors Found" | "No peer counsellors match your search or filters." | `Clear Filters` button |
| Referral Pipeline — no referrals | "No Referrals Raised" | "No referrals have been raised by peer counsellors. Referrals will appear here when peer counsellors flag students for professional support." | — |
| Referral Pipeline — no results for filters | "No Referrals Match Filters" | "Try clearing your filters to see all referrals." | `Clear Filters` button |
| Branch detail drawer — Tab 1, no peer counsellors | "No Peer Counsellors at This Branch" | "No students have been enrolled as peer counsellors at this branch. Enrol students from Class 11 or 12 to start the program." | `+ Enrol Peer Counsellor` button |
| Branch detail drawer — Tab 2, no sessions | "No Sessions Recorded" | "No peer counselling sessions have been recorded at this branch. Record the first session to begin tracking program activity." | `Record Session` button |
| Branch detail drawer — Tab 3, no referrals | "No Referrals at This Branch" | "No referrals have been raised by peer counsellors at this branch." | — |
| Branch detail drawer — Tab 4, no training | "No Training Records" | "No training events have been recorded for peer counsellors at this branch." | `Schedule Refresher Training` button (Counselling Head only) |
| Session Volume Chart — no data | "Not Enough Session Data" | "Session chart data will appear once at least one session is recorded across branches." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 8 KPI cards (grey shimmer) + branch program status matrix (10 grey rows × 9 columns) + peer counsellor directory (8 grey rows) + session volume chart (grey rectangle, 260px tall) + referral pipeline (5 grey rows) |
| Filter / search apply on matrix | Table body spinner overlay on the matrix; KPI cards shimmer and refresh after table settles |
| Filter / search apply on directory | Directory table body spinner overlay |
| Filter apply on referral pipeline | Referral pipeline table spinner overlay |
| Branch detail drawer open | Drawer slides in with skeleton: tab bar + 8 grey content blocks |
| Tab 1 (Peer Counsellors) load | Table skeleton: 5 grey rows × 7 columns |
| Tab 2 (Sessions) load | Table skeleton: 4 grey rows × 7 columns |
| Tab 3 (Referrals) load | Table skeleton: 4 grey rows × 8 columns |
| Tab 4 (Training Log) load | Table skeleton: 3 grey rows × 7 columns |
| Tab 5 (Program History) load | Timeline skeleton: 4 grey timeline entries |
| Enrol peer counsellor — student autocomplete | Dropdown spinner while fetching student matches (300ms debounce fires) |
| Enrol peer counsellor — class validation | Brief 100ms inline spinner next to class field while validation result loads |
| Record session form submit | Save button disabled + spinner + "Recording…" label |
| Crisis flag reveal animation | New fields slide down with CSS transition (200ms); no spinner |
| Crisis notification dispatch | After session save with crisis flag: brief "Notifying…" overlay on toast before success toast fires |
| Peer referral detail drawer open | Drawer slides in with skeleton: 10 grey field blocks + footer button skeletons |
| Refresher training planner — branch select | "Target Peer Counsellors" count area shows spinner while count is fetched from API |
| Schedule training form submit | Save button disabled + spinner + "Scheduling…" label |
| KPI bar auto-refresh | Individual card values shimmer (not full card skeleton); Cards 7 and 4 have a visible pulsing ring when non-zero |
| Session Volume Chart load | Chart area shows grey rectangle with shimmer gradient until HTMX response arrives |
| Export triggered | Export button disabled + spinner until file is prepared server-side |

---

## 10. Role-Based UI Visibility

| UI Element | Counselling Head G3 | Branch Counsellor G2 | Branch Principal G2 | Group COO G4 |
|---|---|---|---|---|
| Branch Program Status Matrix — all branches | ✅ | Own branch only | Own branch only (read) | ✅ (aggregate) |
| Peer Counsellor Directory — all branches | ✅ | Own branch only | Own branch only (read) | ❌ |
| Student name in directory | ✅ | Own branch ✅ | Own branch ✅ | ❌ |
| Session Volume Chart | ✅ | ✅ (own branch data) | ✅ (own branch data) | ✅ (aggregate) |
| Referral Pipeline — all branches | ✅ | Own branch only | ❌ | ❌ |
| Referring peer counsellor name in referral | ✅ | Own branch ✅ | ❌ | ❌ |
| `+ Enrol Peer Counsellor` button | ✅ | ✅ (own branch) | ❌ | ❌ |
| `Record Session` button | ✅ | ✅ (own branch) | ❌ | ❌ |
| `Schedule Refresher Training` button | ✅ | ❌ | ❌ | ❌ |
| `Export Program Report` button | ✅ | ❌ | ❌ | ❌ |
| Crisis escalation notification | ✅ (receives + can acknowledge) | ✅ (receives + can acknowledge) | ✅ (receives notification only) | ❌ |
| Crisis flag acknowledge action | ✅ | ✅ (own branch) | ❌ | ❌ |
| Branch detail drawer — all tabs | ✅ | Own branch all tabs | Own branch — Tab 1 (view), Tab 2 (view), Tab 4 (view) only | ❌ |
| Referral — Assign Counsellor action | ✅ | ✅ (own branch) | ❌ | ❌ |
| Referral — Update Outcome action | ✅ | ✅ (own branch) | ❌ | ❌ |
| Deactivate Peer Counsellor action | ✅ | ✅ (own branch) | ❌ | ❌ |
| KPI bar full detail | ✅ | Own branch | Own branch | Aggregate (no individual records) |
| Alert banners | ✅ (all branches) | Own branch alerts only | Own branch alerts only | ❌ |

---

## 11. API Endpoints

**Base URL:** `/api/v1/group/{group_id}/welfare/counselling/peer-programs/`

All endpoints require JWT authentication. Role-scoping is enforced server-side; Branch Counsellors receive querysets filtered to `branch=request.user.branch`.

| Method | Endpoint | Description | Auth / Role |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/` | Branch program status matrix — paginated, filtered, role-scoped | JWT; all authorised roles |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/kpi/` | KPI summary bar (8 cards) | JWT; all authorised roles |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/alerts/` | Active alert banner conditions | JWT; all authorised roles |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/session-chart/` | Session volume chart data (branches × months) | JWT; all authorised roles |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/peer-counsellors/` | Peer counsellor directory — all branches (role-scoped) | JWT; Counselling Head, Branch Counsellor, Branch Principal |
| POST | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/peer-counsellors/` | Enrol a new peer counsellor | JWT; Counselling Head, Branch Counsellor (own branch) |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/peer-counsellors/{counsellor_id}/` | Individual peer counsellor profile detail | JWT; Counselling Head, own Branch Counsellor |
| PATCH | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/peer-counsellors/{counsellor_id}/` | Update peer counsellor status (deactivate, reactivate) | JWT; Counselling Head, own Branch Counsellor |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/{branch_id}/` | Branch program detail (all 5 tabs — lazy per tab) | JWT; Counselling Head, own Branch Counsellor, own Branch Principal |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/{branch_id}/sessions/` | Session list for a branch | JWT; Counselling Head, own Branch Counsellor, own Branch Principal |
| POST | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/{branch_id}/sessions/` | Record a new session | JWT; Counselling Head, Branch Counsellor (own branch) |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/{branch_id}/training/` | Training log for a branch | JWT; Counselling Head, own Branch Counsellor, own Branch Principal |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/referrals/` | Referral pipeline — all branches (role-scoped) | JWT; Counselling Head, Branch Counsellor (own branch) |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/referrals/{referral_id}/` | Referral detail (anonymised; peer counsellor name role-gated) | JWT; Counselling Head, own Branch Counsellor |
| PATCH | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/referrals/{referral_id}/` | Update referral intake status, assign counsellor, update outcome | JWT; Counselling Head, own Branch Counsellor |
| POST | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/refresher-training/` | Schedule a refresher training event for one or more branches | JWT; Counselling Head only |
| POST | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/crisis/{crisis_id}/acknowledge/` | Acknowledge a crisis flag | JWT; Counselling Head, own Branch Counsellor |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/export/` | Export full program report | JWT; Counselling Head only |
| GET | `/api/v1/group/{group_id}/welfare/counselling/peer-programs/validate-student/` | Validate student eligibility (class 11/12 check) during enrolment | JWT; Counselling Head, Branch Counsellor |

**Query parameters for branch program status matrix (`GET /`):**

| Parameter | Type | Description |
|---|---|---|
| `program_status` | str[] | `active`, `inactive`, `not_started` |
| `has_sessions_this_month` | bool | `true` = at least 1 session · `false` = zero sessions |
| `crisis_flag_this_month` | bool | `true` = show only branches with crisis flags |
| `has_peer_counsellors` | bool | `true` / `false` |
| `branch_id` | int[] | Filter to specific branch(es) |
| `search` | str | Branch name partial match |
| `page` | int | Page number (default: 1) |
| `page_size` | int | Default 25, max 100 |
| `sort_by` | str | Column name; prefix `-` for descending |

**Query parameters for peer counsellor directory (`GET /peer-counsellors/`):**

| Parameter | Type | Description |
|---|---|---|
| `branch_id` | int[] | Filter to specific branch(es) |
| `status` | str[] | `active`, `graduated`, `inactive`, `suspended` |
| `class_level` | str[] | `class_11`, `class_12` |
| `refresher_due` | bool | `true` = overdue for refresher |
| `training_year` | str | e.g., `2026` |
| `search` | str | Student name, class/section, branch name |
| `page` | int | Page number |
| `page_size` | int | Default 25 |
| `sort_by` | str | e.g., `refresher_due`, `-initial_training_date` |

**Query parameters for referral pipeline (`GET /referrals/`):**

| Parameter | Type | Description |
|---|---|---|
| `branch_id` | int[] | Filter to specific branch(es) |
| `intake_status` | str[] | `accepted`, `pending`, `declined`, `in_progress` |
| `crisis_flag` | bool | `true` = crisis referrals only |
| `date_from` | date | Filter by date raised (YYYY-MM-DD) |
| `date_to` | date | Filter by date raised (YYYY-MM-DD) |
| `month` | str | e.g., `2026-03` — shorthand for month filter |
| `search` | str | Branch name or intake status |
| `page` | int | Page number |
| `page_size` | int | Default 25 |
| `sort_by` | str | e.g., `-crisis_flag`, `-date_raised` |

---

## 12. HTMX Patterns

### Pattern Table

| Interaction | hx-trigger | hx-get / hx-post | hx-target | hx-swap |
|---|---|---|---|---|
| Branch matrix search | `keyup changed delay:300ms` | GET `.../peer-programs/?search={val}&{filters}` | `#branch-matrix-section` | `innerHTML` |
| Branch matrix filter apply | `change` on any filter input | GET `.../peer-programs/?{all-filter-params}` | `#branch-matrix-section` | `innerHTML` |
| Branch matrix pagination | `click` | GET `.../peer-programs/?page={n}` | `#branch-matrix-section` | `innerHTML` `hx-push-url="true"` |
| Peer counsellor directory search | `keyup changed delay:300ms` | GET `.../peer-programs/peer-counsellors/?search={val}&{filters}` | `#directory-table-body` | `innerHTML` |
| Directory filter apply | `change` | GET `.../peer-programs/peer-counsellors/?{filters}` | `#directory-section` | `innerHTML` |
| Directory pagination | `click` | GET `.../peer-programs/peer-counsellors/?page={n}` | `#directory-section` | `innerHTML` |
| Branch detail drawer open | `click` on branch name or View | GET `.../peer-programs/{branch_id}/` | `#drawer-container` | `innerHTML` |
| Drawer tab switch | `click` on tab button | GET `.../peer-programs/{branch_id}/?tab={tab_slug}` | `#drawer-tab-content` | `innerHTML` |
| Sessions tab load | `click` on Sessions tab | GET `.../peer-programs/{branch_id}/sessions/` | `#drawer-tab-content` | `innerHTML` |
| Training Log tab load | `click` on Training Log tab | GET `.../peer-programs/{branch_id}/training/` | `#drawer-tab-content` | `innerHTML` |
| Enrol peer counsellor — student autocomplete | `keyup changed delay:300ms` | GET `.../peer-programs/validate-student/?name={val}&branch={id}` | `#student-dropdown` | `innerHTML` |
| Enrol peer counsellor form submit | `click` on Enrol button | POST `.../peer-programs/peer-counsellors/` | `#directory-section` | `innerHTML` + `hx-on::after-request="closeDrawer(); fireToast();"` |
| Record session form submit | `click` on Record Session | POST `.../peer-programs/{branch_id}/sessions/` | `#branch-matrix-section` | `innerHTML` + `hx-on::after-request="closeDrawer(); fireToast();"` |
| Crisis flag radio — conditional reveal | `change` on crisis_flags radio | GET `.../peer-programs/session-crisis-fields/?flag={val}` | `#crisis-flag-fields` | `innerHTML` |
| Referral pipeline search | `keyup changed delay:300ms` | GET `.../peer-programs/referrals/?search={val}` | `#referral-table-body` | `innerHTML` |
| Referral filter apply | `change` | GET `.../peer-programs/referrals/?{filters}` | `#referral-section` | `innerHTML` |
| Referral detail drawer open | `click` on View Referral | GET `.../peer-programs/referrals/{referral_id}/` | `#drawer-container` | `innerHTML` |
| Assign counsellor to referral | `click` on Assign button | PATCH `.../peer-programs/referrals/{referral_id}/` | `#referral-row-{referral_id}` | `outerHTML` |
| Update referral intake status | `change` on inline select | PATCH `.../peer-programs/referrals/{referral_id}/` | `#referral-row-{referral_id}` | `outerHTML` |
| KPI bar auto-refresh | `load, every 600s` | GET `.../peer-programs/kpi/` | `#kpi-bar` | `innerHTML` |
| Alert banners load | `load` | GET `.../peer-programs/alerts/` | `#alert-banner` | `innerHTML` |
| Session volume chart load | `load` | GET `.../peer-programs/session-chart/` | `#session-volume-chart` | `innerHTML` |
| Schedule refresher — branch count fetch | `change` on branch multi-select | GET `.../peer-programs/refresher-training/?branches={ids}` | `#target-counsellors-count` | `innerHTML` |
| Schedule refresher form submit | `click` on Schedule Training | POST `.../peer-programs/refresher-training/` | `#refresher-result` | `innerHTML` + `hx-on::after-request="closeDrawer(); fireToast();"` |
| Crisis acknowledge | `click` on Acknowledge button | POST `.../peer-programs/crisis/{crisis_id}/acknowledge/` | `#alert-banner` | `innerHTML` + `fireToast()` |

---

### Inline HTML Snippets

#### 1. Branch Matrix Search and Filter

```html
<!-- Branch program status matrix search + filter form -->
<div class="flex flex-wrap items-center gap-3 mb-4">
  <input
    id="branch-matrix-search"
    name="search"
    type="text"
    placeholder="Search branch name…"
    class="w-64 px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-indigo-500 focus:border-indigo-500"
    hx-get="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/"
    hx-trigger="keyup changed delay:300ms"
    hx-target="#branch-matrix-section"
    hx-swap="innerHTML"
    hx-include="#matrix-filter-form"
    hx-indicator="#matrix-spinner"
  >
  <div id="matrix-spinner" class="htmx-indicator">
    <svg class="animate-spin h-5 w-5 text-indigo-500" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
    </svg>
  </div>
</div>

<form id="matrix-filter-form" class="flex flex-wrap gap-3 mb-4">
  <input type="hidden" name="page" value="1">

  <!-- Program Status checkboxes -->
  <div class="flex gap-2">
    {% for status, label in [('active','Active'), ('inactive','Inactive'), ('not_started','Not Started')] %}
    <label class="flex items-center gap-1 text-sm">
      <input type="checkbox" name="program_status" value="{{ status }}"
             hx-get="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/"
             hx-trigger="change"
             hx-target="#branch-matrix-section"
             hx-swap="innerHTML"
             hx-include="#matrix-filter-form, #branch-matrix-search">
      {{ label }}
    </label>
    {% endfor %}
  </div>

  <!-- Crisis flag toggle -->
  <label class="flex items-center gap-1 text-sm text-red-700 font-medium">
    <input type="checkbox" name="crisis_flag_this_month" value="true"
           hx-get="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/"
           hx-trigger="change"
           hx-target="#branch-matrix-section"
           hx-swap="innerHTML"
           hx-include="#matrix-filter-form, #branch-matrix-search">
    Crisis Flags Only
  </label>
</form>

<div id="branch-matrix-section">
  <!-- Server renders table here -->
</div>
```

#### 2. Peer Counsellor Directory Search

```html
<!-- Directory search bar with refresher-due toggle -->
<div class="flex items-center gap-3 mb-4">
  <input
    id="directory-search"
    name="search"
    type="text"
    placeholder="Search by student name, class, or branch…"
    class="w-72 px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-indigo-500 focus:border-indigo-500"
    hx-get="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/peer-counsellors/"
    hx-trigger="keyup changed delay:300ms"
    hx-target="#directory-section"
    hx-swap="innerHTML"
    hx-include="#directory-filter-form"
    hx-indicator="#dir-spinner"
  >
  <label class="flex items-center gap-1 text-sm text-amber-700 font-medium">
    <input
      type="checkbox"
      name="refresher_due"
      value="true"
      form="directory-filter-form"
      hx-get="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/peer-counsellors/"
      hx-trigger="change"
      hx-target="#directory-section"
      hx-swap="innerHTML"
      hx-include="#directory-filter-form, #directory-search">
    Refresher Overdue
  </label>
  <div id="dir-spinner" class="htmx-indicator">
    <svg class="animate-spin h-4 w-4 text-indigo-400" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
    </svg>
  </div>
</div>

<form id="directory-filter-form">
  <input type="hidden" name="page" value="1">
  <!-- Status, class, branch filters rendered by server template -->
</form>

<div id="directory-section">
  <!-- Server renders peer counsellor directory table rows here -->
</div>
```

#### 3. Enrol Peer Counsellor — Form with Student Autocomplete and Consent Upload

```html
<form
  id="enroll-form"
  hx-post="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/peer-counsellors/"
  hx-target="#directory-section"
  hx-swap="innerHTML"
  hx-encoding="multipart/form-data"
  hx-on::after-request="closeDrawer(); fireToast(event);"
  hx-indicator="#enroll-spinner"
>
  <!-- Branch select -->
  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-1">Branch *</label>
    <select name="branch_id" class="w-full border border-gray-300 rounded px-3 py-2 text-sm" required>
      {% for branch in branches %}
        <option value="{{ branch.id }}" {% if branch == user.branch %}selected{% endif %}>{{ branch.name }}</option>
      {% endfor %}
    </select>
  </div>

  <!-- Student name autocomplete -->
  <div class="mb-4 relative">
    <label class="block text-sm font-medium text-gray-700 mb-1">Student Name *</label>
    <input
      id="student-name-input"
      name="student_name_q"
      type="text"
      placeholder="Type student name to search…"
      class="w-full border border-gray-300 rounded px-3 py-2 text-sm"
      hx-get="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/validate-student/"
      hx-trigger="keyup changed delay:300ms"
      hx-target="#student-dropdown"
      hx-swap="innerHTML"
      hx-include="[name='branch_id']"
      autocomplete="off"
    >
    <!-- Hidden field receives the selected student ID -->
    <input type="hidden" name="student_id" id="student-id-field">
    <div id="student-dropdown"
         class="absolute z-10 w-full bg-white border border-gray-200 rounded shadow-lg mt-1 max-h-48 overflow-y-auto">
      <!-- Server renders matching student list items here;
           each item: <div class="px-3 py-2 text-sm hover:bg-indigo-50 cursor-pointer"
                            hx-on:click="setStudent('{{ s.id }}', '{{ s.name }}', '{{ s.class }}')">
                       {{ s.name }} – {{ s.class_section }}
                     </div>
      -->
    </div>
    <!-- Class validation inline result -->
    <div id="class-validation" class="mt-1 text-sm"></div>
    <!-- Server returns either:
         <span class="text-green-600">✅ Class {{ class }} — eligible for enrolment</span>
         OR
         <span class="text-red-600">❌ Class {{ class }} — peer counsellors must be Class 11 or 12</span>
    -->
  </div>

  <!-- Consent form upload — mandatory -->
  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Consent Form * <span class="text-xs text-gray-400 font-normal">(Student + Guardian signed — PDF or JPG, max 10 MB)</span>
    </label>
    <input type="file" name="consent_form" accept=".pdf,.jpg,.jpeg"
           class="w-full text-sm border border-dashed border-gray-300 rounded px-3 py-2 cursor-pointer"
           required
           id="consent-upload"
           onchange="document.getElementById('enroll-submit-btn').disabled = false;">
    <p class="text-xs text-amber-700 mt-1">Enrolment cannot be saved until a consent form is uploaded.</p>
  </div>

  <!-- Footer -->
  <div class="flex justify-end gap-3 mt-6 pt-4 border-t border-gray-200">
    <button type="button" class="btn-outline" onclick="closeDrawer()">Cancel</button>
    <button
      type="submit"
      id="enroll-submit-btn"
      class="btn-primary"
      hx-disabled-elt="this"
      disabled
    >
      <span id="enroll-spinner" class="htmx-indicator mr-2">
        <svg class="animate-spin h-4 w-4 inline" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
        </svg>
      </span>
      Enrol Peer Counsellor
    </button>
  </div>
</form>
```

#### 4. Record Session — Crisis Flag Conditional Reveal

```html
<form
  id="record-session-form"
  hx-post="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/{{ branch_id }}/sessions/"
  hx-target="#branch-matrix-section"
  hx-swap="innerHTML"
  hx-on::after-request="closeDrawer(); fireToast(event);"
>
  <!-- ... other form fields (branch, date, type, counsellors, duration, topics) ... -->

  <!-- Referrals section -->
  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-1">Referrals Raised *</label>
    <input type="number" name="referrals_raised" value="0" min="0" max="50"
           class="w-24 border border-gray-300 rounded px-3 py-2 text-sm"
           hx-get="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/session-referral-fields/"
           hx-trigger="change"
           hx-target="#referral-reason-block"
           hx-swap="innerHTML"
           hx-include="[name='referrals_raised']">
  </div>
  <div id="referral-reason-block" class="mb-4">
    <!-- Server renders textarea only if referrals_raised > 0:
         <div class="animate-fadeIn">
           <label class="block text-sm font-medium text-gray-700 mb-1">Brief Referral Reason *</label>
           <p class="text-xs text-amber-700 mb-1">Do not include student names — describe concern categories only.</p>
           <textarea name="referral_reason" rows="3" maxlength="400" required
                     class="w-full border border-gray-300 rounded px-3 py-2 text-sm"></textarea>
         </div>
         Otherwise: empty div.
    -->
  </div>

  <!-- Crisis flag radio — conditional reveal -->
  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-2">Any Crisis Flags? *</label>
    <div class="flex gap-4">
      <label class="flex items-center gap-2 text-sm">
        <input type="radio" name="crisis_flag" value="false"
               checked
               hx-get="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/session-crisis-fields/"
               hx-trigger="change"
               hx-target="#crisis-flag-fields"
               hx-swap="innerHTML"
               hx-vals='{"flag": "false"}'>
        No
      </label>
      <label class="flex items-center gap-2 text-sm text-red-700 font-medium">
        <input type="radio" name="crisis_flag" value="true"
               hx-get="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/session-crisis-fields/"
               hx-trigger="change"
               hx-target="#crisis-flag-fields"
               hx-swap="innerHTML"
               hx-vals='{"flag": "true"}'>
        Yes
      </label>
    </div>
  </div>

  <!-- Crisis fields — revealed by server when flag = true -->
  <div id="crisis-flag-fields">
    <!--
      When flag = true, server returns:
      <div class="border border-red-200 bg-red-50 rounded-lg p-4 animate-slideDown">
        <div class="flex items-start gap-2 mb-3">
          <span class="text-red-500 text-lg">⚠</span>
          <p class="text-sm text-red-700 font-medium">
            Selecting Yes will immediately notify the Branch Counsellor and Group Counselling Head.
            A professional counsellor must follow up within 24 hours (Moderate/High) or 2 hours (Immediate).
          </p>
        </div>
        <div class="mb-3">
          <label class="block text-sm font-medium text-gray-700 mb-1">Crisis Description * (anonymised)</label>
          <textarea name="crisis_description" rows="3" maxlength="600" minlength="50" required
                    placeholder="Describe the concern without naming the student…"
                    class="w-full border border-red-300 rounded px-3 py-2 text-sm focus:ring-red-400"></textarea>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Urgency Level *</label>
          <div class="flex gap-3">
            <label class="flex items-center gap-1 text-sm"><input type="radio" name="urgency" value="moderate" required> Moderate</label>
            <label class="flex items-center gap-1 text-sm text-amber-700"><input type="radio" name="urgency" value="high"> High</label>
            <label class="flex items-center gap-1 text-sm text-red-700 font-medium"><input type="radio" name="urgency" value="immediate"> Immediate</label>
          </div>
        </div>
      </div>

      When flag = false, server returns: <div></div>
    -->
  </div>

  <div class="flex justify-end gap-3 mt-6 pt-4 border-t border-gray-200">
    <button type="button" class="btn-outline" onclick="closeDrawer()">Cancel</button>
    <button type="submit" class="btn-primary" hx-disabled-elt="this">Record Session</button>
  </div>
</form>
```

#### 5. Referral Detail Drawer

```html
<!-- Trigger from referral pipeline table row -->
<button
  class="text-indigo-600 hover:underline text-sm"
  hx-get="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/referrals/{{ referral_id }}/"
  hx-trigger="click"
  hx-target="#drawer-container"
  hx-swap="innerHTML"
  hx-indicator="#drawer-spinner"
  @click="drawerOpen = true"
>
  View Referral
</button>

<!-- Inline referral assignment inside the drawer (rendered by server, updated in place) -->
<div id="referral-detail-{{ referral_id }}">
  <div class="space-y-3 text-sm">
    <!-- Server renders all referral fields; footer actions below -->
    <div class="pt-4 border-t border-gray-200 flex gap-2">
      <!-- Assign counsellor action — inline select -->
      <select
        name="counsellor_id"
        class="border border-gray-300 rounded px-2 py-1 text-sm"
        hx-patch="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/referrals/{{ referral_id }}/"
        hx-trigger="change"
        hx-target="#referral-row-{{ referral_id }}"
        hx-swap="outerHTML"
        hx-vals='{"action": "assign_counsellor"}'
        hx-on::after-request="fireToast(event);"
      >
        <option value="">Assign counsellor…</option>
        {% for counsellor in branch_counsellors %}
          <option value="{{ counsellor.id }}" {% if counsellor.id == assigned_counsellor_id %}selected{% endif %}>
            {{ counsellor.name }}
          </option>
        {% endfor %}
      </select>

      <!-- Update outcome inline -->
      <select
        name="outcome"
        class="border border-gray-300 rounded px-2 py-1 text-sm"
        hx-patch="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/referrals/{{ referral_id }}/"
        hx-trigger="change"
        hx-target="#referral-row-{{ referral_id }}"
        hx-swap="outerHTML"
        hx-vals='{"action": "update_outcome"}'
        hx-on::after-request="fireToast(event);"
      >
        <option value="">Update outcome…</option>
        <option value="ongoing">Ongoing</option>
        <option value="resolved">Resolved</option>
        <option value="escalated">Escalated Further</option>
        <option value="no_show">No Show</option>
      </select>
    </div>
  </div>
</div>
```

#### 6. KPI Auto-Refresh Every 10 Minutes

```html
<!-- KPI summary bar — loads on page load and refreshes every 10 minutes -->
<div
  id="kpi-bar"
  class="grid grid-cols-4 gap-4 mb-6"
  hx-get="/api/v1/group/{{ group_id }}/welfare/counselling/peer-programs/kpi/"
  hx-trigger="load, every 600s"
  hx-swap="innerHTML"
  hx-indicator="#kpi-refresh-indicator"
>
  <!-- Skeleton shown while loading (server renders actual cards after first load) -->
  {% for i in range(8) %}
  <div class="bg-white border border-gray-200 rounded-lg p-4 animate-pulse">
    <div class="h-3 bg-gray-200 rounded w-3/4 mb-2"></div>
    <div class="h-8 bg-gray-200 rounded w-1/2 mb-1"></div>
    <div class="h-2 bg-gray-100 rounded w-1/3"></div>
  </div>
  {% endfor %}
</div>

<!-- Subtle refresh indicator (top-right corner of KPI bar) -->
<div id="kpi-refresh-indicator"
     class="htmx-indicator absolute top-2 right-2 flex items-center gap-1 text-xs text-gray-400">
  <svg class="animate-spin h-3 w-3" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
  </svg>
  Refreshing…
</div>

<!--
  KPI Card 7 (Crisis Escalations) — server renders with pulsing ring when non-zero:
  <div class="bg-white border-2 border-red-400 rounded-lg p-4 relative">
    <div class="absolute top-2 right-2 h-3 w-3 bg-red-500 rounded-full animate-ping"></div>
    <p class="text-xs text-gray-500 font-medium uppercase tracking-wide">Crisis Escalations This Month</p>
    <p class="text-3xl font-bold text-red-600 mt-1">{{ crisis_count }}</p>
    <a hx-get="/api/v1/.../peer-programs/referrals/?crisis_flag=true"
       hx-target="#referral-section" hx-swap="innerHTML"
       hx-trigger="click" class="text-xs text-red-600 underline mt-1 block">View crisis referrals →</a>
  </div>
-->
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
