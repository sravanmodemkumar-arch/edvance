# 35 — JEE/NEET Test Series Manager

> **URL:** `/group/acad/jee-neet/test-series/`
> **File:** `35-jee-neet-test-series.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** JEE/NEET Integration Head G3 · CAO G4 · Exam Controller G3 · Results Coordinator G3

---

## 1. Purpose

The JEE/NEET Test Series Manager governs the full mock test series lifecycle for students enrolled in Integrated JEE and Integrated NEET coaching programmes across all group branches. In competitive exam preparation at this scale — potentially 8,000–15,000 students preparing for JEE Main, JEE Advanced, and NEET-UG simultaneously — the test series is the primary feedback loop that determines how preparation is calibrated term-over-term.

Each mock test in the series must follow the exact NTA (National Testing Agency) exam pattern: JEE Main mock tests have 75 questions (Physics 25, Chemistry 25, Maths 25) with integer-type and MCQ formats; NEET mock tests have 180 questions (Physics 45, Chemistry 45, Botany 45, Zoology 45). The test creation flow links directly to the Exam Paper Builder (page 24) to ensure question paper structure follows NTA norms rather than regular school exam formats.

After each mock test, the system generates per-student AIR (All India Rank) estimates based on the student's percentile relative to the mock cohort. While this is an approximation — the mock cohort is the group's coaching students, not the national JEE/NEET pool — it gives students and parents a directional indicator of preparation level. This page manages the complete pipeline from test creation through result publication and AIR estimate generation.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ View · Approve · Override | Full override authority |
| Group Academic Director | G3 | ✅ All | ❌ | Read-only |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ All | ✅ Paper assignment only | Cannot create or publish tests |
| Group Results Coordinator | G3 | ✅ All | ✅ Publish results | Cannot create tests |
| Group Stream Coord — MPC | G3 | ✅ JEE tests | ❌ | Read-only — JEE stream interest |
| Group Stream Coord — BiPC | G3 | ✅ NEET tests | ❌ | Read-only — NEET stream interest |
| Group Stream Coord — MEC/CEC | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ✅ All | ✅ Full — create · edit · schedule · publish · mark official | Primary operator |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ All | ✅ Export only | Read-only |
| Group Academic Calendar Manager | G3 | ✅ Dates/schedule only | ❌ | Schedule view for calendar coordination |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  JEE/NEET  ›  Test Series Manager
```

### 3.2 Page Header
```
JEE/NEET Test Series Manager                        [+ New Test]  [Export XLSX ↓]
[Group Name] · Academic Year [YYYY–YY]              JEE/NEET Head only — action buttons
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Tests in Series (This Year) | 18 |
| JEE Tests | 10 |
| NEET Tests | 8 |
| Completed (Results Published) | 12 |
| Upcoming (Scheduled) | 4 |
| In Draft | 2 |
| Students Enrolled (JEE) | 6,240 |
| Students Enrolled (NEET) | 4,880 |

---

## 4. Main Content

### 4.1 Search / Filters / Table

**Search:** Test name — 300ms debounce.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Type | Multi-select | JEE Main · JEE Advanced · NEET-UG · Both (combined mock) |
| Status | Multi-select | Draft · Scheduled · Paper Assigned · Active (Live) · Completed · Results Published · Official |
| Date Range | Date picker | Test date range |
| Branch Scope | Multi-select | All branches · Specific branches |
| Official Test | Checkbox | Show only tests marked as "Official" (anchor tests used for AIR benchmarking) |

### 4.2 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Test # | Number | ✅ | Sequential within academic year (JEE-01, NEET-01 etc.) |
| Test Name | Text | ✅ | e.g. "JEE Main Mock — Test 7" |
| Type | Badge | ✅ | JEE Main · JEE Advanced · NEET · Combined |
| Test Date | Date | ✅ | Scheduled date |
| Total Questions | Number | ✅ | 75 for JEE, 180 for NEET |
| Total Marks | Number | ✅ | 300 for JEE (4 marks each, −1 for wrong), 720 for NEET |
| Duration | Text | ❌ | 3 hrs for JEE · 3h 20m for NEET |
| Branch Scope | Text | ❌ | "All Branches" or list of specific branches |
| Paper Status | Badge | ✅ | Not Assigned · Assigned · Approved · Published |
| Status | Badge | ✅ | See filter options |
| Official | Badge | ❌ | "Official" green badge if marked |
| Results Published | Badge | ✅ | Yes · No |
| Actions | — | ❌ | See row actions |

**Default sort:** Test Date ascending (upcoming tests first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50.

### 4.3 Row Actions

| Action | Icon | Visible To | Opens | Notes |
|---|---|---|---|---|
| View Details | Eye | All | `test-detail` drawer 560px | Full test overview |
| Edit Test | Pencil | JEE/NEET Head · CAO | `test-edit` drawer 640px | Only before test is live |
| Open Paper Builder | Pencil-paper | JEE/NEET Head · Exam Controller | Opens page 24 (Exam Paper Builder) with pre-filled exam linkage | External navigation |
| View Results | Chart | All with access | `test-result` drawer 560px | After results published |
| Performance Analysis | Bar chart | JEE/NEET Head · CAO · Results Coord | Opens `/group/acad/jee-neet/performance/?test_id=` | Links to page 37 |
| Mark as Official | Star | JEE/NEET Head · CAO | Confirm modal 380px | Official tests used for AIR benchmarking |
| Publish Results | Broadcast | JEE/NEET Head · Results Coord · CAO | `publish-results-confirm` modal 440px | After results moderated |
| Delete (Draft only) | Trash | JEE/NEET Head · CAO | Confirm modal 380px | Only allowed for Draft status |

### 4.4 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | JEE/NEET Head · CAO · MIS | Exports selected test metadata |
| Send Schedule to Branches | JEE/NEET Head · CAO | Notifies branch coordinators of upcoming test dates |

---

## 5. Drawers & Modals

### 5.1 Drawer: `test-create` / `test-edit`
- **Trigger:** [+ New Test] header button / Pencil icon row action
- **Width:** 640px
- **Tabs:** Test Identity · Paper · Branch Scope · Schedule · Notification

#### Tab: Test Identity
| Field | Type | Required | Validation |
|---|---|---|---|
| Test Name | Text | ✅ | Max 100 chars |
| Test Type | Select | ✅ | JEE Main · JEE Advanced · NEET-UG · Combined Mock |
| Test Number in Series | Number | ✅ | Auto-suggested (next in sequence) |
| NTA Exam Pattern | Toggle | ✅ | On = enforces NTA question counts and marking scheme |
| Total Questions | Number | Auto | Auto-filled from NTA pattern (75 / 180) — editable if NTA pattern off |
| Total Marks | Number | Auto | Auto-filled from pattern (300 / 720) — editable if NTA pattern off |
| Duration | Text | ✅ | HH:MM format |
| Marking Scheme | Radio | ✅ | +4/−1 (JEE) · +4/0 (NEET MCQ) · +4/−1 + Integer type (JEE) |
| Official Test | Toggle | ❌ | Marks test as official AIR benchmarking test |

#### Tab: Paper
- "Link to Exam Paper Builder" — [Open Paper Builder →] button (external navigation to page 24 with this test pre-selected as the exam context)
- Paper status indicator: Not Created · In Draft · Submitted for Approval · Approved · Published
- Paper assignment field: Select from approved papers in the group question bank
- Instruction note: "Papers for JEE/NEET tests follow NTA pattern. Use the Exam Paper Builder to create or link a paper."

#### Tab: Branch Scope
- Radio: All Branches · Specific Branches
- If "Specific Branches": Multi-select from group branch list
- Students included count: Auto-calculated based on JEE/NEET enrolled students in selected branches
- Current count: "Estimated [N] students will take this test"

#### Tab: Schedule
| Field | Type | Required | Validation |
|---|---|---|---|
| Test Date | Date picker | ✅ | Must be a future date |
| Start Time | Time picker | ✅ | HH:MM 24hr |
| End Time | Time picker | Auto | Calculated from start time + duration |
| Result Upload Deadline | Date picker | ✅ | At least 2 days after test date |
| Results Publication Date | Date picker | ❌ | Planned publication date (informational) |
| Answer Key Publication | Date picker | ❌ | After test ends, before results |

#### Tab: Notification
| Setting | Type | Default |
|---|---|---|
| Notify branch coordinators on creation | Toggle | On |
| Notify students via portal | Toggle | On |
| Reminder to students 2 days before | Toggle | On |
| Reminder to branches 1 day before | Toggle | On |
| WhatsApp notification | Toggle | On |

**Submit:** "Create Test" / "Save Changes" — disabled until all required tabs valid (tab icons show red dot if incomplete).

---

### 5.2 Drawer: `test-detail`
- **Width:** 560px
- **Tabs:** Overview · Paper Status · Branch Status · Results Summary

#### Tab: Overview
Full test metadata as per Test Identity tab, plus current status, creation timestamp, created by.

#### Tab: Paper Status
- Paper ID and name
- Creator and creation date
- Approval status with approver name
- Publication status
- [Open Paper →] link to Exam Paper Builder

#### Tab: Branch Status
Table: Branch Name · JEE Students · NEET Students · Readiness Status · Hall Tickets Generated · Actions (Send Reminder)

#### Tab: Results Summary (shown after results published)
- Total students appeared
- Avg score (JEE / NEET separately)
- Top scorer (masked — first name only + branch)
- Percentile distribution summary
- AIR estimate range for group median student

---

### 5.3 Drawer: `test-result`
- **Trigger:** "View Results" row action
- **Width:** 560px
- **Tabs:** Leaderboard · Subject-wise · AIR Estimates

#### Tab: Leaderboard
Table: Rank · Student (anonymised for lower roles — roll number only) · Branch · Score · Percentile — Top 50 only. Full data in performance page 37.

#### Tab: Subject-wise
Table: Subject · Group Avg Score · Group Avg % · Max Possible · Lowest avg branch · Highest avg branch

#### Tab: AIR Estimates
- Group's AIR estimate range based on percentile position in national mock databases (if available)
- Disclaimer: "AIR estimates are approximations based on this group's coaching cohort. Actual JEE/NEET AIR may differ."
- Distribution: Table of percentile bands and corresponding estimated AIR ranges
  - e.g. P90+ → AIR 1–5,000 · P75–90 → AIR 5,000–20,000 · P50–75 → AIR 20,000–50,000

---

### 5.4 Modal: `mark-official-confirm`
- **Width:** 380px
- **Title:** "Mark as Official Test — [Test Name]"
- **Content:** "Official tests are used as anchor points for AIR estimation across the series. This test will be included in trend benchmarking."
- **Buttons:** [Mark as Official] (primary) + [Cancel]

---

### 5.5 Modal: `publish-results-confirm`
- **Width:** 440px
- **Title:** "Publish Results — [Test Name]"
- **Checklist:**
  - ✅ Marks uploaded by all branches
  - ✅ Answer key published
  - ✅ Results moderated
  - ✅ AIR estimates computed
- **Publish channels:** Student portal (default on) · Parent SMS · Parent WhatsApp
- **Buttons:** [Publish Results] (primary) + [Cancel]

---

## 6. Charts

### 6.1 Score Trend Across Mock Series (Line)
- **Type:** Multi-line chart
- **X-axis:** Test numbers in series (JEE-01 through JEE-10 / NEET-01 through NEET-08)
- **Y-axis:** Group average score (out of 300 for JEE / 720 for NEET)
- **Lines:** Group Avg (blue solid) · Top 10% cohort avg (green dashed) · Bottom 25% cohort avg (red dashed)
- **Annotations:** Official tests marked with a star on the X-axis
- **Tooltip:** Test # · Avg score · Students appeared
- **Colorblind-safe:** Blue / Green / Red with distinct dash patterns
- **Export:** PNG

### 6.2 AIR Prediction Band Over Series (Area Chart)
- **Type:** Area chart with confidence band
- **X-axis:** Test numbers
- **Y-axis:** Estimated AIR (inverted — lower AIR = better — label reads "Estimated AIR")
- **Data:** Median estimated AIR per test + P25 to P75 band shaded
- **Tooltip:** Test # · Median AIR estimate · P25–P75 range
- **Note below chart:** "AIR estimates improve in accuracy as the series progresses and more official tests are included."
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Test created | "Test [JEE-07] scheduled for [Date]. Branch coordinators notified." | Success | 5s |
| Test edited | "[Test Name] updated." | Success | 4s |
| Paper linked | "Exam paper linked to [Test Name]." | Success | 4s |
| Marked as official | "[Test Name] marked as Official. Included in AIR benchmarking." | Success | 4s |
| Results published | "Results published for [Test Name]. [N] students notified." | Success | 5s |
| Test deleted | "Draft test [Test Name] deleted." | Warning | 4s |
| Cannot delete (not draft) | "Only Draft tests can be deleted. This test is [Status]." | Error | Manual |
| Schedule notification sent | "Test schedule sent to [N] branch coordinators." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No tests in series | "No Tests Yet" | "Create the first mock test in this year's JEE/NEET series" | [+ New Test] |
| No tests match filters | "No Tests Match" | "Try adjusting your filters or search term" | [Clear Filters] |
| Results not published | "Results Pending" | "Results for this test have not been published yet" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| Test-create/edit drawer | Spinner in drawer body |
| Test-detail / result drawers | Spinner + skeleton tabs |
| Results publish action | Spinner inside [Publish Results] button + button disabled |
| Chart initial load | Spinner centred in chart card |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | JEE/NEET Head G3 | CAO G4 | Exam Controller G3 | Results Coord G3 | MIS G1 |
|---|---|---|---|---|---|
| [+ New Test] button | ✅ | ❌ (can override approve) | ❌ | ❌ | ❌ |
| Edit Test action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Open Paper Builder action | ✅ | ❌ | ✅ | ❌ | ❌ |
| Mark as Official action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Publish Results action | ✅ | ✅ | ❌ | ✅ | ❌ |
| Delete (Draft) action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Performance Analysis action | ✅ | ✅ | ❌ | ✅ | ❌ |
| AIR Estimates tab in result drawer | ✅ | ✅ | ❌ | ✅ | ✅ |
| Export XLSX | ✅ | ✅ | ❌ | ❌ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/jee-neet/test-series/` | JWT | Test series list |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/test-series/stats/` | JWT | Summary stats bar |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/test-series/` | JWT (JEE/NEET Head) | Create test |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/test-series/{test_id}/` | JWT | Test detail drawer data |
| PUT | `/api/v1/group/{group_id}/acad/jee-neet/test-series/{test_id}/` | JWT (JEE/NEET Head / CAO) | Update test |
| DELETE | `/api/v1/group/{group_id}/acad/jee-neet/test-series/{test_id}/` | JWT (JEE/NEET Head / CAO) | Delete (Draft only) |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/test-series/{test_id}/mark-official/` | JWT (JEE/NEET Head / CAO) | Mark as official |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/test-series/{test_id}/publish-results/` | JWT (JEE/NEET Head / Results Coord / CAO) | Publish results |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/test-series/{test_id}/results/` | JWT | Results summary for drawer |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/test-series/notify-branches/` | JWT (JEE/NEET Head) | Send schedule notification |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/test-series/export/?format=xlsx` | JWT | Export test list XLSX |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/test-series/charts/score-trend/` | JWT | Score trend line chart |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/test-series/charts/air-prediction/` | JWT | AIR prediction area chart |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Test search | `input delay:300ms` | GET `.../test-series/?q=` | `#test-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../test-series/?filters=` | `#test-table-section` | `innerHTML` |
| Sort / paginate | `click` | GET `.../test-series/?sort=&page=` | `#test-table-section` | `innerHTML` |
| Create/edit drawer open | `click` | GET `.../test-series/create-form/` or `.../test-series/{id}/edit-form/` | `#drawer-body` | `innerHTML` |
| Test detail drawer open | `click` | GET `.../test-series/{id}/` | `#drawer-body` | `innerHTML` |
| Result drawer open | `click` | GET `.../test-series/{id}/results/` | `#drawer-body` | `innerHTML` |
| Publish results confirm | `click` | POST `.../test-series/{id}/publish-results/` | `#test-row-{id}` | `outerHTML` |
| Mark official confirm | `click` | POST `.../test-series/{id}/mark-official/` | `#test-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
