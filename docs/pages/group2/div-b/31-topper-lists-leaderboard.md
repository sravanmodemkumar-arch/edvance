# 31 — Topper Lists & Leaderboard

> **URL:** `/group/acad/toppers/`
> **File:** `31-topper-lists-leaderboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 · Results Coordinator G3 · Academic Director G3 · Stream Coordinators G3 · Academic MIS Officer G1

---

## 1. Purpose

The Topper Lists & Leaderboard page is the institution group's official record of academic achievement. Across a group of 50 branches and 80,000 students, identifying and celebrating consistent toppers requires a structured, auditable system — not a manual spreadsheet. This page produces that record automatically from computed ranks.

The leaderboard feeds directly into two downstream workflows: scholarship nominations (Div-C — Group Scholarship Manager) and marketing campaigns (Div-O — Group Marketing). The "Nominate for Scholarship" action initiates a Div-C scholarship nomination flow. The "Send to Marketing" action packages the topper data into a press-ready format for the Div-O Marketing team, enabling WhatsApp broadcast cards and newspaper ads without manual re-keying.

Historical consistency tracking allows the group to identify students who rank in the top tier across multiple exams — not just one — making scholarship nominations and recognition more equitable. A student who ranks #1 in a single exam but declines in subsequent tests is distinguished from one who ranks in the top 10% across six consecutive tests.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All tabs, all data | ✅ Nominate for Scholarship · Send to Marketing · Export | Full authority |
| Group Academic Director | G3 | ✅ All tabs | ✅ Export only | No nomination authority |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ All tabs | ❌ | Read-only |
| Group Results Coordinator | G3 | ✅ All tabs | ✅ Nominate · Send to Marketing · Export | Primary operator |
| Group Stream Coord — MPC | G3 | ✅ Per Stream tab (MPC) + Per Subject (MPC subjects) | ❌ | Filtered to own stream |
| Group Stream Coord — BiPC | G3 | ✅ Per Stream tab (BiPC) + Per Subject (BiPC subjects) | ❌ | Filtered to own stream |
| Group Stream Coord — MEC/CEC | G3 | ✅ Per Stream tab (MEC/CEC) + Per Subject | ❌ | Filtered to own stream |
| Group JEE/NEET Integration Head | G3 | ✅ Per Stream (JEE/NEET integrated) | ❌ | Read-only |
| Group IIT Foundation Director | G3 | ✅ Per Branch (Foundation class toppers) | ❌ | Read-only |
| Group Olympiad & Scholarship Coord | G3 | ✅ All tabs | ✅ Nominate for Scholarship | No marketing send authority |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ All tabs | ✅ Export only | No nomination authority |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Topper Lists & Leaderboard
```

### 3.2 Page Header
```
Topper Lists & Leaderboard                          [Export PDF ↓]  [Export XLSX ↓]
[Group Name] · Exam: [Exam Name]  [Change Exam ▾]  Results Coord / CAO only — action buttons
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Students Ranked | 82,340 |
| Top 10 (Group Overall) | 10 students |
| Streams Included | 5 |
| Branches Represented (Top 100) | 18 of 50 |
| Consistent Toppers (3+ exams, Top 10%) | 47 |

---

## 4. Main Content

### 4.1 Leaderboard Tabs

Five tabs — each is a separate filtered view of the rank table:

| Tab | Filter Behaviour |
|---|---|
| Group Overall | All streams · All branches · Group rank 1 upwards |
| Per Stream | User selects stream — shows rank within selected stream |
| Per Subject | User selects stream + subject — shows subject topper rank |
| Per Branch | User selects branch — shows branch-internal rank 1 upwards |
| Per Class | User selects class (e.g. Class 11) — shows rank within that class |

Tab selection persists across filter changes. Switching exam reloads all tabs.

### 4.2 Search / Filters

**Search:** Student name or roll number — 300ms debounce, highlights match in Name column.

**Filters (common across tabs — tab-specific ones noted):**

| Filter | Type | Options | Applies To |
|---|---|---|---|
| Exam | Select | Dropdown of completed exams with ranks | All tabs — also shown in header |
| Rank Range | Select | Top 10 · Top 50 · Top 100 · Custom from–to | All tabs |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · Foundation · Integrated JEE/NEET | Group Overall tab |
| Subject | Select | Dynamically populated based on selected stream | Per Subject tab |
| Branch | Multi-select | All 50 branches | Group Overall · Per Subject |
| Branch | Single select | One branch at a time | Per Branch tab |
| Class | Multi-select | Class 6–12 | Per Class tab |
| Consistent Topper | Checkbox | Show only students who ranked in top 10% across 3+ exams | Group Overall tab |

Active filter chips: Dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Rank | Number (bold) | ✅ | Rank within the active tab scope |
| Photo | Avatar | ❌ | 36px circle; placeholder silhouette if not uploaded |
| Roll Number | Text | ✅ | |
| Student Name | Text | ✅ | Full name |
| Branch | Text | ✅ | Branch name + code in smaller text |
| Class | Text | ✅ | e.g. Class 11 |
| Stream | Badge | ✅ | |
| Score | Number | ✅ | Total marks obtained |
| Max Marks | Number | ❌ | Total possible marks |
| Percentage | Number | ✅ | 1 decimal place |
| Percentile | Number | ✅ | Group or tab-scope percentile |
| Consistent Topper | Badge | ❌ | "3+ Exams Top 10%" badge — shown in Group Overall tab only |
| Actions | — | ❌ | See row actions |

**Default sort:** Rank ascending (Rank 1 at top).

**Pagination:** Server-side · Default 50/page · Selector 25/50/100 · "Showing X–Y of Z students".

**Row select:** Checkbox per row + select-all header checkbox.

### 4.4 Row Actions

| Action | Icon | Visible To | Opens | Notes |
|---|---|---|---|---|
| View Topper Profile | Eye | All with access | `topper-profile` drawer 480px | Full exam history |
| Nominate for Scholarship | Award | CAO · Results Coord · Olympiad Coord | `nominate-scholarship` modal 460px | Links to Div-C flow |
| Send to Marketing | Megaphone | CAO · Results Coord | `send-marketing-confirm` modal 440px | Links to Div-O flow |
| Export Certificate Data | Download | CAO · Results Coord · MIS | Direct download — CSV row for certificate printing | |

### 4.5 Bulk Actions (shown when rows selected)

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (PDF Topper List) | CAO · Results Coord · MIS | Formatted for notice board / WhatsApp broadcast |
| Export Selected (XLSX) | CAO · Results Coord · MIS | Raw data for admin use |
| Nominate Selected for Scholarship | CAO · Results Coord · Olympiad Coord | Batch nomination — opens confirm modal with list |
| Send Selected to Marketing | CAO · Results Coord | Batch send — packages all selected for Div-O |

---

## 5. Drawers & Modals

### 5.1 Drawer: `topper-profile`
- **Trigger:** Eye icon row action or clicking student name
- **Width:** 480px
- **Tabs:** Current Exam · Exam History · Scholarship Eligibility

#### Tab: Current Exam
| Field | Value |
|---|---|
| Student Photo | 80px circle avatar |
| Full Name | |
| Roll Number | |
| Branch | Name + address |
| Class & Stream | |
| Group Rank | Large bold |
| Branch Rank | |
| Percentile | |
| Total Score | X / Max |
| Subject Breakdown | Table: Subject · Score · Max · % |

#### Tab: Exam History
Table: Exam Name · Date · Group Rank · Branch Rank · Percentile · Score · Stream — sorted newest first.

Mini line chart: Rank trend over last 6 exams (lower = better, Y-axis inverted).

Consistent Topper badge shown if student appears in top 10% for 3+ consecutive exams.

#### Tab: Scholarship Eligibility
- Eligibility criteria met / not met (bullet checklist)
- Current scholarship status: None · Nominated · Awarded · Conditions pending
- History of past scholarship nominations with outcome
- [Nominate for Scholarship] button (same as row action — visible to authorised roles)
- Branch admin contact: "Contact [Branch Admin Name] for student's guardian details."

---

### 5.2 Modal: `nominate-scholarship`
- **Trigger:** "Nominate for Scholarship" row action or button in topper-profile drawer
- **Width:** 460px
- **Title:** "Nominate [Student Name] for Scholarship — [Exam Name]"
- **Content:**
  - Student summary: Name · Branch · Rank · Percentile · Score
  - Scholarship type selector: Merit · Need-based · Special Achievement (Olympiad/Foundation)
  - Scholarship scheme selector: Dynamically populated from Div-C schemes currently accepting nominations
  - Basis for nomination: Text area (required, min 50 chars)
  - Supporting evidence: "Rank [N] in Group — [Exam Name] — [Date]" (auto-populated)
  - Attachments: Optional PDF upload (score report, branch principal recommendation)
- **Buttons:** [Submit Nomination to Div-C] (primary) + [Cancel]
- **On confirm:** Nomination record created · Sent to Div-C Group Scholarship Manager · Toast shown · Nomination badge updated in profile

---

### 5.3 Modal: `send-marketing-confirm`
- **Trigger:** "Send to Marketing" row action
- **Width:** 440px
- **Title:** "Send Topper to Marketing — [Student Name]"
- **Content:**
  - Student summary card preview (as Div-O will see it): Photo · Name · Branch · Rank · Score · Achievement headline
  - Achievement headline field (pre-filled, editable): e.g. "Rank 1 in Group — [Exam Name] — [Group Name]"
  - Consent note: "Branch admin must have obtained parent consent for name/photo use in marketing materials."
  - Consent confirmed checkbox (required, not pre-checked)
  - Media channels: WhatsApp Broadcast · Social Media Post · Press Release — checkboxes
- **Buttons:** [Send to Div-O Marketing] (primary) + [Cancel]
- **On confirm:** Marketing record created in Div-O flow · Notification sent to Group Marketing team · Toast shown

---

### 5.4 Modal: `bulk-nominate-scholarship`
- **Width:** 500px
- **Title:** "Bulk Scholarship Nomination — [N] Students"
- **Content:** Scrollable list of selected students with Name · Rank · Branch · Percentile
- **Scholarship type:** Single selector applies to all in batch
- **Basis:** Batch note (required, min 30 chars) applied to all nominations
- **Note:** "Each nomination will be reviewed individually by the Scholarship Coordinator."
- **Buttons:** [Submit [N] Nominations] + [Cancel]

---

## 6. Charts

### 6.1 Top 10 Toppers by Branch (Bar)
- **Type:** Horizontal bar chart
- **X-axis:** Count of students in Top 100 group rank
- **Y-axis:** Branch names (sorted by count descending)
- **Colour:** Blue bars, green highlight for top 3 branches
- **Tooltip:** Branch · Count in Top 100 · Best rank
- **Shown:** Group Overall tab only
- **Export:** PNG

### 6.2 Score Distribution by Stream (Box Plot or Grouped Bar)
- **Type:** Grouped vertical bar chart (box-plot approximated with min/Q1/median/Q3/max bars if Chart.js 4.x box plugin available, else grouped bar)
- **X-axis:** Streams (MPC / BiPC / MEC / CEC / Foundation)
- **Y-axis:** Score %
- **Shows:** Group topper (top bar) · Group median · Branch median per stream
- **Colorblind-safe:** Distinct hues per stream — Blue (MPC) · Green (BiPC) · Amber (MEC) · Teal (CEC)
- **Export:** PNG

### 6.3 Rank Consistency Tracker (Line — Historical view)
- **Type:** Line chart (multiple lines — one per consistent topper student)
- **X-axis:** Last 6 exams (by date)
- **Y-axis:** Group rank (lower = better, Y-axis inverted — Rank 1 at top)
- **Lines:** Up to 10 students shown (top consistent toppers)
- **Tooltip:** Exam name · Rank · Score
- **Legend:** Student names
- **Filter:** Stream filter within chart card
- **Shown:** Historical view section
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Scholarship nomination submitted | "Nomination for [Student Name] submitted to Div-C Scholarship Manager." | Success | 5s |
| Send to marketing confirmed | "Topper data for [Student Name] sent to Div-O Marketing team." | Success | 5s |
| Bulk nomination submitted | "[N] scholarship nominations submitted to Div-C." | Success | 5s |
| Export PDF started | "Topper list PDF preparing — download will begin shortly." | Info | 4s |
| Export XLSX started | "XLSX export preparing — download will begin shortly." | Info | 4s |
| Certificate data downloaded | "Certificate data for [Student Name] downloaded." | Success | 3s |
| No consent checked | "Please confirm parent consent before sending to marketing." | Error | Manual |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No exam selected | "Select an Exam" | "Choose a completed exam with computed ranks to view toppers" | [Select Exam ▾] |
| No ranks computed yet | "Rankings not yet computed" | "Ranks must be computed before toppers can be listed" | [Go to Rank Computation →] |
| No students in rank range | "No students in this range" | "Try expanding the rank range or changing filters" | [Clear Filters] |
| Tab — no data for stream | "No ranked students for [Stream]" | "No students in this stream were ranked in the selected exam" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + tab bar + table (10 skeleton rows) |
| Tab switch | Skeleton table rows (10) within tab content area |
| Exam selector change | Full table and stats skeleton reload |
| Filter/search/sort/page | Inline skeleton rows (10) |
| Topper profile drawer open | Spinner in drawer body + skeleton tabs |
| Chart section load | Spinner centred in each chart card |
| Nomination submit | Spinner inside [Submit Nomination] button + button disabled |
| Marketing send | Spinner inside [Send to Div-O Marketing] button + button disabled |
| PDF export | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Results Coord G3 | Stream Coords G3 | Olympiad Coord G3 | MIS G1 |
|---|---|---|---|---|---|
| All tabs visible | ✅ | ✅ | ✅ (own stream tabs only) | ✅ | ✅ |
| Nominate for Scholarship button | ✅ | ✅ | ❌ | ✅ | ❌ |
| Send to Marketing button | ✅ | ✅ | ❌ | ❌ | ❌ |
| Export PDF/XLSX | ✅ | ✅ | ❌ | ❌ | ✅ |
| Export Certificate Data | ✅ | ✅ | ❌ | ❌ | ✅ |
| Bulk actions bar | ✅ | ✅ | ❌ | ✅ (nomination only) | ✅ (export only) |
| Scholarship Eligibility tab in drawer | ✅ | ✅ | ❌ | ✅ | ❌ |
| Branch admin contact in drawer | ✅ | ✅ | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/toppers/` | JWT | Exam list for selector |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/overall/` | JWT | Group Overall tab data |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/by-stream/` | JWT | Per Stream tab data |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/by-subject/` | JWT | Per Subject tab data |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/by-branch/` | JWT | Per Branch tab data |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/by-class/` | JWT | Per Class tab data |
| GET | `/api/v1/group/{group_id}/acad/toppers/stats/` | JWT | Summary stats bar |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/student/{student_id}/` | JWT | Topper profile drawer data |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/student/{student_id}/history/` | JWT | Exam history tab |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/student/{student_id}/scholarship-eligibility/` | JWT | Scholarship eligibility tab |
| POST | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/student/{student_id}/nominate/` | JWT (CAO / Results Coord / Olympiad Coord) | Submit scholarship nomination |
| POST | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/student/{student_id}/send-to-marketing/` | JWT (CAO / Results Coord) | Send to Div-O |
| POST | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/bulk-nominate/` | JWT (CAO / Results Coord / Olympiad Coord) | Bulk scholarship nomination |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/export/?format=pdf` | JWT | Export topper list PDF |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/export/?format=xlsx` | JWT | Export XLSX |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/charts/by-branch/` | JWT | Branch topper distribution chart |
| GET | `/api/v1/group/{group_id}/acad/toppers/{exam_id}/charts/stream-distribution/` | JWT | Score distribution by stream chart |
| GET | `/api/v1/group/{group_id}/acad/toppers/charts/rank-consistency/` | JWT | Rank consistency historical chart |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Exam selector change | `change` | GET `.../toppers/?exam_id=` | `#toppers-page-body` | `innerHTML` |
| Tab switch | `click` | GET `.../toppers/{exam_id}/{tab}/` | `#toppers-table-section` | `innerHTML` |
| Student search | `input delay:300ms` | GET `.../toppers/{exam_id}/{tab}/?q=` | `#toppers-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../toppers/{exam_id}/{tab}/?filters=` | `#toppers-table-section` | `innerHTML` |
| Sort / paginate | `click` | GET `.../toppers/{exam_id}/{tab}/?sort=&page=` | `#toppers-table-section` | `innerHTML` |
| Open topper profile | `click` | GET `.../toppers/{exam_id}/student/{id}/` | `#drawer-body` | `innerHTML` |
| Submit nomination | `click` | POST `.../student/{id}/nominate/` | `#nomination-modal-body` | `innerHTML` |
| Send to marketing | `click` | POST `.../student/{id}/send-to-marketing/` | `#marketing-modal-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
