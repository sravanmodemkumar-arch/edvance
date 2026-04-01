# 10 — IIT Foundation Director Dashboard

> **URL:** `/group/acad/iit-foundation/`
> **File:** `10-iit-foundation-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group IIT Foundation Director (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group IIT Foundation Director. The IIT Foundation programme covers Classes 6 through 10 — five class levels across all branches that offer the programme. It is a structured pre-coaching pathway designed to build the mathematical reasoning, scientific aptitude, and problem-solving habits that IIT/NEET aspirants need well before they enter the MPC or BiPC streams in Class 11.

The Director oversees syllabus completion by class level, test scores and rankings across branches, teacher qualification standards (IIT/NIT graduate teachers are preferred for Maths and Science in this programme), scholarship eligibility identification, and the transition pipeline — tracking which Class 10 Foundation graduates are expected to join the JEE or NEET integrated tracks in Class 11.

The dashboard presents data segmented by class level (Class 6, 7, 8, 9, 10) across all participating branches. Branches that do not offer the Foundation programme are shown in a non-participating section at the bottom of relevant tables. The programme may run independently of or alongside the regular school syllabus; the dashboard tracks both coverage of the Foundation-specific curriculum and alignment with the NCERT/State Board curriculum at each class level.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IIT Foundation Director | G3 | Full — all sections, all actions | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | Full read + override actions | CAO oversees all academic programmes |
| Group Academic Director | G3 | Read — syllabus completion and teacher qualification sections | Academic oversight |
| Group Curriculum Coordinator | G2 | Read — syllabus and content sections only | Curriculum alignment |
| Group JEE/NEET Integration Head | G3 | Read — Class 10 transition tracker and high-performer table | Transition pipeline tracking |
| Group Stream Coordinator — MPC | G3 | Read — Class 10 transition tracker only | Prospective MPC student pool |
| Group Stream Coordinator — BiPC | G3 | Read — Class 10 transition tracker only | Prospective BiPC student pool |
| Group Olympiad & Scholarship Coord | G3 | Read — scholarship eligibility tracker only | Scholarship pipeline |
| Group Exam Controller | G3 | Read — upcoming Foundation tests timeline | Exam scheduling |
| Group Special Education Coordinator | G3 | — | Has own dashboard |
| Group Academic MIS Officer | G1 | Read-only — all sections | No write controls visible |
| Group Academic Calendar Manager | G3 | Read — upcoming Foundation tests section only | Calendar coordination |

> **Access enforcement:** Django view decorator `@require_role('iit_foundation_director')`. CAO and MIS Officer admitted via role-union check. All other roles are redirected to their own dashboard unless explicitly listed above.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  IIT Foundation  ›  Foundation Director Dashboard
```

### 3.2 Page Header
```
Welcome back, [Director Name]                          [Schedule Foundation Test +]  [Settings ⚙]
Group IIT Foundation Director  ·  Last login: [date time]  ·  [Group Logo]
```

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch name + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all →" link

**Alert trigger examples:**
- Foundation syllabus completion < 60% in any class level with < 3 weeks to term-end test
- Branch offering Foundation has a Maths or Science teacher with no IIT/NIT background flagged in qualification check
- Class 10 students approaching the JEE/NEET transition with no Foundation test scores recorded (dropped out without exit record)
- Scholarship-eligible student not formally identified > 30 days past eligibility threshold
- Upcoming Foundation test < 48 hrs away with no paper assigned

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Foundation Enrollment | Total students in Foundation programme (Classes 6–10) across all branches + trend | Enrollment module | Green if ≥ target · Yellow 80–99% · Red < 80% | → Section 5.3 Class-wise Enrollment |
| Avg Syllabus Completion | `XX%` — weighted average across all class levels and participating branches | Syllabus tracking | Green ≥ 85% · Yellow 70–85% · Red < 70% | → Section 5.1 Foundation Coverage |
| Foundation Avg Score | Group avg marks across last completed Foundation group test | Results module | Green ≥ 65% · Yellow 50–65% · Red < 50% | → Section 5.2 Test Scores by Class |
| Teacher Qualification Rate | `XX%` Foundation Maths/Science teachers with IIT/NIT/equivalent background | HR/qualification data | Green ≥ 90% · Yellow 75–90% · Red < 75% | → Section 5.5 Teacher Qualification |
| Upcoming Foundation Tests | Count of Foundation tests in next 14 days across all branches and classes | Exam calendar | Badge always shown; pulsing if any test < 48 hrs away | → Section 5.6 Upcoming Tests |
| Scholarship Eligible | Students who have crossed internal merit threshold — Foundation scholarship eligible | Analytics module | Green = 0 pending · Yellow 1–10 pending action · Red > 10 | → Section 5.7 Scholarship Tracker |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/iit-foundation/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Foundation Programme Coverage by Class

> Syllabus completion per class level (Class 6–10) across all participating branches.

**Display:** Per-class horizontal progress bars — one group per class level.

**Class levels:** Class 6 · Class 7 · Class 8 · Class 9 · Class 10

**Subjects tracked per class:** Mathematics · Science (Physics + Chemistry) · Mental Ability / Reasoning

**Progress bar display (within each class group):**

| Column | Description |
|---|---|
| Subject | Subject name |
| Branches Reporting | Branches that have submitted progress / total offering this class |
| Group Avg Completion | Weighted average across reporting branches |
| Progress Bar | Green ≥ 85% · Amber 70–85% · Red < 70% |
| Lowest Branch | Branch name with lowest completion — link to branch detail |
| Actions | [View Detail →] opens class-subject breakdown drawer |

**Drawer: `foundation-coverage-detail`**
- Width: 560px
- Content: Branch-by-branch table for selected class + subject — Branch · Completion % · Topics Done · Topics Remaining · Last Updated
- Filter: Sort by completion % ascending

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/iit-foundation/coverage/"` · `hx-trigger="load"` · `hx-target="#coverage-section"`.

---

### 5.2 Foundation Test Scores by Class

> Average test score per class level — this term — across all participating branches.

**Display:** Grouped bar chart (Chart.js 4.x)

**X-axis:** Class levels (Class 6, 7, 8, 9, 10)

**Y-axis:** Average score percentage (0–100%)

**Bar grouping:** Per branch (each branch = one colour, legend). Maximum 10 branches shown in one view; branch filter to isolate.

**Tooltip:** Class level · Branch · Avg score this term · Avg score last term · Delta

**Additional line overlay:** Group target score per class (dashed grey line)

**Filters within chart card:**
- Class multi-select (default: all)
- Branch filter (default: all; single branch for trend view)
- Term selector (current term / previous term)

**Export:** "Export PNG" button top-right of chart card.

**Empty state:** "No Foundation test score data for this term. Ensure tests have been conducted and results uploaded."

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/iit-foundation/test-scores/"` · filter changes trigger `hx-get` with params · `hx-target="#test-scores-section"` · `hx-swap="innerHTML"`.

---

### 5.3 Class-wise Enrollment

> Student enrollment per class per branch — shows programme penetration across the group.

**Display:** Dual-level stat cards + branch breakdown table.

**Stat cards (top row — one per class):**
- Class 6: [N] students · [M] branches
- Class 7: [N] students · [M] branches
- Class 8: [N] students · [M] branches
- Class 9: [N] students · [M] branches
- Class 10: [N] students · [M] branches

**Branch breakdown table (below stat cards):**

| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | Link to Branch Detail page |
| City | ✅ | |
| Cl. 6 | ✅ | Enrollment; red = 0 if programme offered |
| Cl. 7 | ✅ | Enrollment |
| Cl. 8 | ✅ | Enrollment |
| Cl. 9 | ✅ | Enrollment |
| Cl. 10 | ✅ | Enrollment |
| Total Foundation | ✅ | Sum across all classes |
| Programme Status | ✅ | Active · No Enrollment · Not Offered |

**Filters:** Class level · Programme status · City/District.

**Default sort:** Total Foundation enrollment descending.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/iit-foundation/enrollment/"` · filter changes trigger `hx-get` · `hx-target="#enrollment-section"`.

---

### 5.4 Top Foundation Students — Leaderboard

> Group-wide leaderboard of Foundation students ranked by their programme score.

**Display:** Table (top 25 students by default)

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Rank | ✅ | Group-level rank |
| Student Code | ✅ | Anonymised code; actual name visible G3+ |
| Class | ✅ | 6 / 7 / 8 / 9 / 10 |
| Branch | ✅ | Branch name |
| Foundation Score | ✅ | Best score this term |
| Subject Strength | ❌ | Highest-scoring subject badge |
| Trend | ❌ | ↑ / ↓ / → vs previous term |
| Actions | ❌ | [View Profile →] [Nominate for Scholarship] |

**Filters:** Class level (filter to specific class) · Branch · Term (current / previous)

**[Nominate for Scholarship]:** POST to nominate student → feeds into Scholarship Tracker (Section 5.7). Only active if student meets eligibility criteria (otherwise greyed out with tooltip).

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/iit-foundation/leaderboard/"` · filter changes trigger `hx-get` · `hx-target="#leaderboard-section"`.

---

### 5.5 Teacher Qualification Flag

> Branches where Foundation Maths or Science teachers do not meet the preferred qualification standard (IIT/NIT/equivalent engineering/science graduate).

**Display:** Alert list (card-style)

**Card fields:** Branch name · City · Subject (Maths / Science) · Teacher name · Qualification held · Qualification flag (Preferred qualification missing / Under-qualified / Unverified) · Days since flagged · [View Teacher →] [Raise HR Request]

**Severity:** Red card = Unverified or Under-qualified · Amber = Missing preferred IIT/NIT background but otherwise qualified

**[View Teacher →]:** Opens read-only teacher profile drawer.

**[Raise HR Request]:** Opens HR request form pre-filled with subject, branch, requirement description.

**Drawer: `teacher-profile-view`**
- Width: 480px
- Content: Teacher name · Qualification · Certifications · Classes assigned · Teaching experience (years) · Last observation rating
- Actions (G3): [Raise HR Request →]

**Empty state:** "No teacher qualification issues detected. All Foundation teachers meet required standards." — green checkmark.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/iit-foundation/teacher-flags/"` · `hx-trigger="load"` · `hx-target="#teacher-flags-section"`.

---

### 5.6 Upcoming Foundation Tests

> All Foundation programme tests scheduled in the next 14 days, across all branches and classes.

**Display:** Timeline (vertical, day-by-day)

**Timeline item fields:** Date badge · Test name · Type (Unit Test / Term Exam / Mock / Group Assessment) · Class(es) covered · Branches count · Paper Status badge · [View →]

**Colour coding:** Unit Test (blue) · Term Exam (orange) · Group Assessment (purple) · Mock (grey)

**Alert:** Any test < 48 hrs away with Paper Status "Not Assigned" → red alert strip above timeline.

**Empty state:** "No Foundation tests scheduled in the next 14 days."

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/iit-foundation/upcoming-tests/"` · `hx-trigger="load"` · `hx-target="#upcoming-tests-section"`.

---

### 5.7 Scholarship Eligibility Tracker

> Foundation students who have crossed the internal merit threshold and are eligible for the group's Foundation merit scholarship.

**Display:** Counter badge (students eligible but not yet formally processed) + action table.

**Table columns:**

| Column | Sortable | Notes |
|---|---|---|
| Student Code | ✅ | Anonymised; name visible G3+ |
| Class | ✅ | 6–10 |
| Branch | ✅ | |
| Foundation Score | ✅ | Score that triggered eligibility |
| Eligibility Date | ✅ | When threshold was crossed |
| Days Pending | ✅ | Red if > 30 days |
| Status | ✅ | Eligible (new) · Nominated · Under Review · Awarded · Declined |
| Actions | ❌ | [Nominate →] [Mark Ineligible with Reason] |

**Filters:** Class · Branch · Status · Days pending (> 7 / > 14 / > 30)

**[Nominate →]:** Opens nomination drawer — pre-fills student details, allows adding nomination notes, links to Olympiad Coord for cross-reference (scholarship may be coordinated together).

**Drawer: `scholarship-nominate`**
- Width: 520px
- Fields: Student details (read-only) · Foundation scores summary · Nomination note (rich text) · Co-nominate for external scholarship? (checkbox linking to Olympiad Coord queue)
- Action: [Submit Nomination] → POST + sends notification to scholarship committee

**Empty state:** "No students currently meeting the Foundation merit scholarship threshold." — trophy outline icon.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/iit-foundation/scholarships/"` · filter changes trigger `hx-get` · `hx-target="#scholarship-section"`.

---

### 5.8 Class 10 Transition Tracker

> Class 10 Foundation students who will be transitioning to Class 11 — identifies those expected to join JEE or NEET integrated tracks.

**Display:** Summary cards + table.

**Summary cards:**
- Class 10 Foundation students this year: [N]
- Declared JEE intent: [N] (link to JEE/NEET Integration Head dashboard)
- Declared NEET intent: [N]
- Undecided / Other: [N]
- No response recorded: [N] (red if > 0)

**Table columns:**

| Column | Sortable | Notes |
|---|---|---|
| Student Code | ✅ | Anonymised |
| Branch | ✅ | |
| Foundation Score | ✅ | |
| Declared Track | ✅ | JEE · NEET · Other · No response |
| Counselling Done | ✅ | Y / N — green / red |
| Actions | ❌ | [Mark Counselled] [Update Track Intent] |

**Filters:** Branch · Declared track · Counselling status

**[Mark Counselled]:** POST to update counselling status for this student.

**[Update Track Intent]:** Opens mini modal with track selection dropdown.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/iit-foundation/transition/"` · filter changes trigger `hx-get` · `hx-target="#transition-section"`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `foundation-coverage-detail`
- **Trigger:** [View Detail →] in Section 5.1 progress bar row
- **Width:** 560px
- **Content:** Branch-by-branch table for selected class + subject; sortable by completion %
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/iit-foundation/coverage/{class_level}/{subject_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.2 Drawer: `teacher-profile-view`
- **Trigger:** [View Teacher →] in Section 5.5 qualification flag card
- **Width:** 480px
- **Content:** Teacher profile — qualifications, classes assigned, observation rating
- **Actions:** [Raise HR Request →]
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/iit-foundation/teachers/{teacher_id}/"` `hx-target="#drawer-body"`

### 6.3 Drawer: `scholarship-nominate`
- **Trigger:** [Nominate →] in Section 5.7 scholarship table
- **Width:** 520px
- **Fields:** Student details (read-only) · Foundation scores · Nomination note · Co-nominate checkbox
- **HTMX:** `hx-post="/api/v1/group/{group_id}/acad/iit-foundation/scholarships/{student_id}/nominate/"` on submit

### 6.4 Modal: `update-track-intent`
- **Trigger:** [Update Track Intent] in Section 5.8 transition table
- **Width:** 380px
- **Content:** Student code (read-only) · Track intent dropdown (JEE / NEET / Other / No response) · [Save] [Cancel]
- **On save:** `hx-post="/api/v1/group/{group_id}/acad/iit-foundation/transition/{student_id}/track/"` → toast + row updates

### 6.5 Modal: `schedule-foundation-test`
- **Trigger:** [Schedule Foundation Test +] in page header
- **Width:** 500px
- **Content:** Test name · Type (Unit / Term / Group / Mock) · Class level(s) selector · Date + duration · Branches scope · Paper assignment · [Schedule] [Cancel]
- **On schedule:** `hx-post="/api/v1/group/{group_id}/acad/iit-foundation/tests/schedule/"` → toast + upcoming tests section refreshes

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Foundation test scheduled | "Foundation test scheduled for [Class(es)] on [date] — [N] branches notified" | Success (green) | 5s auto-dismiss |
| Student nominated for scholarship | "Scholarship nomination submitted for Student [Code]" | Success | 4s |
| Student marked ineligible | "Student marked ineligible with reason recorded" | Info (blue) | 4s |
| Teacher HR request raised | "HR request raised for [Subject] teacher at [Branch Name]" | Success | 5s |
| Counselling status updated | "Counselling status updated for Student [Code]" | Success | 4s |
| Track intent updated | "Track intent updated to [JEE/NEET/Other] for Student [Code]" | Success | 4s |
| KPI load error | "Failed to load KPI data. Retrying…" | Error (red) | Manual dismiss |
| Coverage data missing | "Coverage data unavailable for some branches. Check reporting." | Warning (yellow) | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No branches offer Foundation | Building outline | "No IIT Foundation programme configured" | "No branches in this group currently offer the IIT Foundation programme" | — |
| No test scores for term | Bar chart outline | "No test score data" | "No Foundation tests have been conducted or results uploaded for this term" | — |
| No upcoming tests | Calendar outline | "No tests in the next 14 days" | "No Foundation tests are scheduled for the next two weeks" | [Schedule Foundation Test +] |
| No teacher qualification issues | Checkmark circle | "All teachers qualified" | "All Foundation Maths and Science teachers meet the required standards" | — |
| No scholarship-eligible students | Trophy outline | "No eligible students yet" | "No Foundation students have crossed the merit scholarship threshold this term" | — |
| No Class 10 students | Document outline | "No Class 10 data" | "No Class 10 Foundation students recorded for this academic year" | — |
| Leaderboard empty | Podium outline | "No leaderboard data" | "Complete at least one Foundation test to generate rankings" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + coverage bars (5 class groups) + chart placeholder |
| Coverage section load | Skeleton progress bar rows — 5 class groups × 3 subjects |
| Test scores chart load | Spinner centred in chart area |
| Enrollment table load | Skeleton table rows — 5 rows |
| Leaderboard table load | Skeleton rows — 10 rows |
| Teacher flags section load | Skeleton alert cards — 3 cards |
| Scholarship table load | Skeleton rows — 5 rows |
| Transition table load | Skeleton rows — 5 rows |
| Drawer open | Skeleton rows inside drawer body |
| KPI auto-refresh | Subtle shimmer over existing card values |
| Schedule test modal submit | Spinner inside [Schedule] button + button disabled |

---

## 10. Role-Based UI Visibility

| Element | Foundation Director (G3) | CAO (G4) | JEE/NEET Head (G3) | MIS Officer (G1) | All others |
|---|---|---|---|---|---|
| Page itself | ✅ Rendered | ✅ Rendered (override) | ✅ Partial read | ✅ Read-only | ❌ Redirected |
| Alert Banner | ✅ Shown | ✅ Shown | ✅ Shown (transition/high-perf alerts) | ✅ Shown | N/A |
| [Schedule Foundation Test +] | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Nominate →] scholarship | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Raise HR Request] teacher | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Mark Counselled] | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Update Track Intent] | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| Student names (leaderboard) | ✅ Visible | ✅ Visible | ✅ Visible (transition table only) | ❌ Code only | N/A |
| Scholarship tracker section | ✅ Full access | ✅ Full access | ❌ Hidden | ✅ Read-only | N/A |
| Class 10 transition section | ✅ Full access | ✅ Full access | ✅ Read (own section) | ✅ Read-only | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/dashboard/` | JWT (G3+) | Full page data |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/kpi-cards/` | JWT (G3+) | KPI card values only (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/coverage/` | JWT (G3+) | Syllabus coverage by class level |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/coverage/{class_level}/{subject_id}/` | JWT (G3+) | Branch-by-branch coverage for one class/subject |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/test-scores/` | JWT (G3+) | Chart data — avg test scores by class |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/enrollment/` | JWT (G3+) | Class-wise enrollment data |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/leaderboard/` | JWT (G3+) | Top student leaderboard |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/leaderboard/{student_id}/nominate/` | JWT (G3) | Nominate student for scholarship from leaderboard |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/teacher-flags/` | JWT (G3+) | Teacher qualification flags |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/teachers/{teacher_id}/` | JWT (G3+) | Teacher profile detail |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/teachers/hr-request/` | JWT (G3) | Raise HR request for teacher |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/upcoming-tests/` | JWT (G3+) | Upcoming Foundation tests (next 14 days) |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/tests/schedule/` | JWT (G3) | Schedule a new Foundation test |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/scholarships/` | JWT (G3+) | Scholarship eligibility tracker |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/scholarships/{student_id}/nominate/` | JWT (G3) | Submit scholarship nomination |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/scholarships/{student_id}/ineligible/` | JWT (G3) | Mark student ineligible |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/transition/` | JWT (G3+) | Class 10 transition tracker data |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/transition/{student_id}/counselled/` | JWT (G3) | Mark student as counselled |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/transition/{student_id}/track/` | JWT (G3) | Update declared track intent |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `/api/.../iit-foundation/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Coverage section load | `load` | GET `/api/.../iit-foundation/coverage/` | `#coverage-section` | `innerHTML` |
| Subject detail drawer | `click` | GET `/api/.../coverage/{class}/{subject}/` | `#drawer-body` | `innerHTML` |
| Test scores chart filter | `change` | GET `/api/.../test-scores/?class={}&branch={}&term={}` | `#test-scores-section` | `innerHTML` |
| Enrollment filter change | `change` | GET `/api/.../enrollment/?class={}&status={}` | `#enrollment-section` | `innerHTML` |
| Leaderboard filter | `change` | GET `/api/.../leaderboard/?class={}&branch={}&term={}` | `#leaderboard-section` | `innerHTML` |
| Nominate from leaderboard | `click` | POST `/api/.../leaderboard/{id}/nominate/` | `#toast-container` | `afterbegin` |
| Scholarship table filter | `change` | GET `/api/.../scholarships/?class={}&status={}&days={}` | `#scholarship-section` | `innerHTML` |
| Open nomination drawer | `click` | GET `/api/.../scholarships/{id}/` | `#drawer-body` | `innerHTML` |
| Submit nomination | `click` | POST `/api/.../scholarships/{id}/nominate/` | `#scholarship-section` | `innerHTML` |
| Transition filter | `change` | GET `/api/.../transition/?track={}&counselled={}` | `#transition-section` | `innerHTML` |
| Mark counselled | `click` | POST `/api/.../transition/{id}/counselled/` | `#transition-section` | `innerHTML` |
| Schedule test modal submit | `click` | POST `/api/.../tests/schedule/` | `#upcoming-tests-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
