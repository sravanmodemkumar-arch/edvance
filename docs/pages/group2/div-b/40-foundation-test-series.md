# 40 — Foundation Test Series

> **URL:** `/group/acad/iit-foundation/tests/`
> **File:** `40-foundation-test-series.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** IIT Foundation Director G3 · CAO G4 · Exam Controller G3 · Results Coordinator G3

---

## 1. Purpose

The Foundation Test Series manages the complete mock and periodic test pipeline specifically for Classes 6–10 enrolled in the group's IIT Foundation programme. While the overall exam pipeline (pages 22–28) handles all group exams, Foundation tests have their own series structure, question pattern, and pedagogical intent: they are designed to develop problem-solving instinct and mathematical reasoning from early classes — not just to test curriculum recall.

The structure of this page mirrors the JEE/NEET Test Series Manager (page 35) deliberately, as the operational workflow is identical: create test → assign paper → schedule across branches → moderate results → publish → track performance. The key distinction is the audience: Classes 6–10 instead of Classes 11–12, a different question pattern (Olympiad-style puzzle questions for younger classes, increasingly JEE-like format for Class 9–10), and a different performance interpretation (no AIR estimates — instead, a Foundation Ranking within the group's Foundation programme).

For the IIT Foundation Director, the test series is the most direct signal of how the programme is performing year-on-year. A Foundation student who ranks in the top 10% across three or more consecutive tests in Class 8 is a candidate for the group's internal merit scholarship and early identification for intensive JEE coaching in Class 11. This page creates the test records that feed that identification pipeline.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All classes, all tests | ✅ View · Approve · Override | Full oversight |
| Group Academic Director | G3 | ✅ All | ❌ | Read-only |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ All | ✅ Paper assignment | Cannot create tests |
| Group Results Coordinator | G3 | ✅ All | ✅ Publish results | Cannot create tests |
| Group Stream Coord — MPC | G3 | ❌ | ❌ | No access (Foundation is pre-stream) |
| Group Stream Coord — BiPC | G3 | ❌ | ❌ | No access |
| Group Stream Coord — MEC/CEC | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ✅ Class 9–10 tests (pipeline) | ❌ | Read-only awareness |
| Group IIT Foundation Director | G3 | ✅ All classes, all tests | ✅ Full — create · edit · schedule · publish | Primary operator |
| Group Olympiad & Scholarship Coord | G3 | ✅ All (scholarship eligibility) | ❌ | Read-only |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ All | ✅ Export only | Read-only |
| Group Academic Calendar Manager | G3 | ✅ Dates/schedule only | ❌ | Calendar coordination |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  IIT Foundation  ›  Foundation Test Series
```

### 3.2 Page Header
```
Foundation Test Series                              [+ New Test]  [Export XLSX ↓]
[Group Name] · Academic Year [YYYY–YY]              IIT Foundation Director only — new test button
```

### 3.3 Class Filter Tabs (primary navigation within this page)

Five secondary tabs above the table: **All Classes** · **Class 6** · **Class 7** · **Class 8** · **Class 9** · **Class 10**

Selecting a class tab filters the main table to tests for that class only. "All Classes" shows all Foundation tests across Classes 6–10.

### 3.4 Summary Stats Bar

| Stat | Value (All Classes) |
|---|---|
| Total Tests (This Year) | 42 |
| Class 6 | 8 tests |
| Class 7 | 8 tests |
| Class 8 | 9 tests |
| Class 9 | 9 tests |
| Class 10 | 8 tests |
| Results Published | 30 |
| Upcoming | 10 |
| In Draft | 2 |

---

## 4. Main Content

### 4.1 Search / Filters / Table

**Search:** Test name — 300ms debounce.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Class | Multi-select | Class 6 · 7 · 8 · 9 · 10 |
| Subject | Multi-select | Mathematics · Physics · Chemistry · Combined (all subjects) |
| Status | Multi-select | Draft · Scheduled · Paper Assigned · Active · Completed · Results Published |
| Date Range | Date picker | Test date range |
| Branch Scope | Multi-select | All branches · Specific branches |

### 4.2 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Test # | Text | ✅ | e.g. FDN-CL8-07 (Foundation Class 8 Test 7) |
| Test Name | Text | ✅ | e.g. "Class 8 Foundation — Term 2 Mock 3" |
| Class | Badge | ✅ | Class 6 · 7 · 8 · 9 · 10 |
| Subject | Badge | ✅ | Maths · Physics · Chemistry · Combined |
| Test Date | Date | ✅ | |
| Total Questions | Number | ✅ | |
| Total Marks | Number | ✅ | |
| Duration | Text | ❌ | |
| Branch Scope | Text | ❌ | "All Branches" or count |
| Paper Status | Badge | ✅ | Not Assigned · Assigned · Approved · Published |
| Status | Badge | ✅ | Colour-coded |
| Results Published | Badge | ✅ | Yes · No |
| Actions | — | ❌ | See row actions |

**Default sort:** Class (ascending) → Test Date (ascending).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50.

### 4.3 Row Actions

| Action | Icon | Visible To | Opens | Notes |
|---|---|---|---|---|
| View Details | Eye | All with access | `test-detail` drawer 560px | |
| Edit Test | Pencil | Foundation Dir · CAO | `test-edit` drawer 640px | Draft and Scheduled status only |
| Open Paper Builder | Paper | Foundation Dir · Exam Controller | Page 24 — Exam Paper Builder | Pre-fills Foundation class context |
| View Results | Chart | All | `test-result` drawer 560px | After results published |
| Performance Analysis | Bar | Foundation Dir · CAO | Page 41 — Foundation Performance filtered to this test | |
| Publish Results | Broadcast | Foundation Dir · Results Coord · CAO | `publish-confirm` modal | After moderation |
| Delete | Trash | Foundation Dir · CAO | Confirm modal | Draft status only |

### 4.4 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | Foundation Dir · CAO · MIS | Test metadata export |
| Send Schedule to Branches | Foundation Dir | Notify branch Foundation coordinators of upcoming tests |

---

## 5. Drawers & Modals

### 5.1 Drawer: `test-create` / `test-edit`
- **Width:** 640px
- **Tabs:** Test Identity · Paper · Branch Scope · Schedule · Notification

#### Tab: Test Identity
| Field | Type | Required | Notes |
|---|---|---|---|
| Test Name | Text | ✅ | Max 100 chars |
| Class | Select | ✅ | Class 6 · 7 · 8 · 9 · 10 |
| Subject | Select | ✅ | Mathematics · Physics · Chemistry · Combined |
| Question Pattern | Select | ✅ | Olympiad Style (Classes 6–8) · JEE Pattern (Classes 9–10) · Mixed · Custom |
| Total Questions | Number | ✅ | Auto-suggested from pattern (50 for Olympiad / 75 for JEE pattern) |
| Total Marks | Number | ✅ | Auto-suggested |
| Duration | Text | ✅ | HH:MM |
| Marking Scheme | Select | ✅ | +4/−1 · +3/0 · +1/0 (for younger classes) |
| Test Series # | Number | Auto | Next in sequence for this class |
| Academic Term | Select | ✅ | Term 1 (Apr–Sep) · Term 2 (Oct–Mar) |

**Question Pattern notes:**
- Olympiad Style (Class 6–8): Higher-order thinking, puzzle-based, non-routine problems
- JEE Pattern (Class 9–10): Section A (MCQ) + Section B (Integer type) mirroring JEE Main format to acclimatise students early

#### Tab: Paper
- Paper assignment: Link from Exam Paper Builder or select from approved Foundation question bank
- Paper Status display
- [Open Paper Builder →] button

#### Tab: Branch Scope
- Radio: All Foundation branches · Selected branches
- Multi-select (if selected)
- Shows student count estimate based on selection + class enrollment data

#### Tab: Schedule
| Field | Required |
|---|---|
| Test Date | ✅ |
| Start Time | ✅ |
| Result Upload Deadline | ✅ |
| Answer Key Publish Date | ❌ |

#### Tab: Notification
- Notify branch Foundation coordinators on create (toggle, default on)
- Student portal notification (toggle, default on)
- Parent notification (toggle, default off for younger classes — configurable)

**Submit:** [Create Test] / [Save Changes]

---

### 5.2 Drawer: `test-detail`
- **Width:** 560px
- **Tabs:** Overview · Paper Status · Branch Status · Results Summary

Same structure as page 35 (JEE/NEET test-detail) adapted for Foundation context.

#### Tab: Results Summary (shown after results published)
- Total students appeared
- Group average %
- Subject-wise averages (for Combined tests)
- Top 10 performers (anonymised — roll number only, for Olympiad Coord scholarship use)
- No AIR estimates — instead shows Foundation Programme Rank (rank within group Foundation students of that class)

---

### 5.3 Drawer: `test-result`
- **Width:** 560px
- **Tabs:** Leaderboard · Subject-wise · Scholarship Flags

#### Tab: Leaderboard
Table: Foundation Rank · Roll Number · Branch · Score · Percentage · Percentile within class.

#### Tab: Subject-wise
For combined tests: Subject · Group Avg · Max · Group Pass %.

#### Tab: Scholarship Flags
List of students who rank in top 10% for this test — used by Olympiad & Scholarship Coordinator.
Note: "Students appear in full scholarship eligibility tracker after 3+ tests. See Foundation Performance (page 41)."

---

### 5.4 Modal: `publish-confirm`
- **Width:** 440px
- **Checklist:**
  - ✅ Marks uploaded by all branches in scope
  - ✅ Answer key published
  - ✅ Moderation approved
- **Publish to:** Student portal (default on) · Parent portal/SMS (default off for Class 6–7 · default on for Class 9–10) — configurable per class in class config
- **Buttons:** [Publish Results] + [Cancel]

---

## 6. Charts

### 6.1 Test Count per Class — This Year (Bar)
- **Type:** Vertical grouped bar chart
- **X-axis:** Class levels (Class 6–10)
- **Y-axis:** Test count
- **Bars:** Completed (green) · Upcoming (blue) · Draft (grey)
- **Tooltip:** Class · Completed: N · Upcoming: N · Draft: N
- **Export:** PNG

### 6.2 Group Average Score Trend per Class (Multi-line)
- **Type:** Multi-line chart
- **X-axis:** Test sequence within academic year
- **Y-axis:** Group average % for that class
- **Lines:** One per class (Class 6–10) — 5 lines
- **Colorblind-safe 5-colour palette:** Blue (Cl6) · Orange (Cl7) · Green (Cl8) · Purple (Cl9) · Teal (Cl10)
- **Tooltip:** Test # · Class · Avg %
- **Filter:** Class multi-select within chart card
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Test created | "Foundation test [FDN-CL8-07] created for Class 8 on [Date]. Branches notified." | Success | 5s |
| Test edited | "[Test Name] updated." | Success | 4s |
| Results published | "Results published for [Test Name]. [N] students notified." | Success | 5s |
| Test deleted | "Draft test [Test Name] deleted." | Warning | 4s |
| Cannot delete | "Only Draft tests can be deleted." | Error | Manual |
| Schedule sent | "Foundation test schedule sent to [N] branch coordinators." | Success | 4s |
| Export started | "XLSX preparing — download will begin shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No tests yet | "No Foundation Tests Yet" | "Create the first test for this academic year's Foundation series" | [+ New Test] |
| No tests for class | "No Tests for Class [N]" | "No Foundation tests have been created for Class [N] yet" | [+ New Test] |
| No tests match filters | "No Tests Match" | "Try adjusting filters or search" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + class tabs + table (10 rows) |
| Class tab switch | Inline table skeleton rows (10) |
| Filter/search/sort/page | Inline skeleton rows (10) |
| Test-create/edit drawer | Spinner in drawer body |
| Test-detail / result drawers | Spinner + skeleton tabs |
| Publish confirm | Spinner inside [Publish Results] + button disabled |
| Chart load | Spinner centred in chart card |
| Export | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | Foundation Dir G3 | CAO G4 | Exam Controller G3 | Results Coord G3 | MIS G1 |
|---|---|---|---|---|---|
| [+ New Test] button | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit Test action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Open Paper Builder action | ✅ | ❌ | ✅ | ❌ | ❌ |
| Publish Results action | ✅ | ✅ | ❌ | ✅ | ❌ |
| Delete (Draft) action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Scholarship Flags tab in result drawer | ✅ | ✅ | ❌ | ❌ | ❌ |
| Export XLSX | ✅ | ✅ | ❌ | ❌ | ✅ |
| Performance Analysis action | ✅ | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/tests/` | JWT | Foundation test list |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/tests/stats/` | JWT | Summary stats bar |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/tests/` | JWT (Foundation Dir) | Create test |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/tests/{test_id}/` | JWT | Test detail drawer |
| PUT | `/api/v1/group/{group_id}/acad/iit-foundation/tests/{test_id}/` | JWT (Foundation Dir / CAO) | Update test |
| DELETE | `/api/v1/group/{group_id}/acad/iit-foundation/tests/{test_id}/` | JWT (Foundation Dir / CAO) | Delete (Draft only) |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/tests/{test_id}/publish-results/` | JWT (Foundation Dir / Results Coord / CAO) | Publish results |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/tests/{test_id}/results/` | JWT | Results drawer data |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/tests/{test_id}/results/scholarship-flags/` | JWT (Foundation Dir / CAO / Olympiad Coord) | Scholarship eligible students |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/tests/notify-branches/` | JWT (Foundation Dir) | Send schedule notification |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/tests/export/?format=xlsx` | JWT | Export XLSX |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/tests/charts/count-by-class/` | JWT | Test count bar chart |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/tests/charts/avg-trend/` | JWT | Avg score trend multi-line chart |

Query params: `class_level`, `subject`, `status`, `branch_ids`, `date_from`, `date_to`, `q`, `sort`, `page`.

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Class tab switch | `click` | GET `.../tests/?class_level=` | `#foundation-test-table-section` | `innerHTML` |
| Test search | `input delay:300ms` | GET `.../tests/?q=&class_level=` | `#test-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../tests/?filters=` | `#test-table-section` | `innerHTML` |
| Sort / paginate | `click` | GET `.../tests/?sort=&page=` | `#test-table-section` | `innerHTML` |
| Create/edit drawer open | `click` | GET `.../tests/create-form/` or `.../tests/{id}/edit-form/` | `#drawer-body` | `innerHTML` |
| Test detail drawer open | `click` | GET `.../tests/{id}/` | `#drawer-body` | `innerHTML` |
| Result drawer open | `click` | GET `.../tests/{id}/results/` | `#drawer-body` | `innerHTML` |
| Publish confirm | `click` | POST `.../tests/{id}/publish-results/` | `#test-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
