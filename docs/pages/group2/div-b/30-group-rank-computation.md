# 30 — Group Rank Computation

> **URL:** `/group/acad/rankings/`
> **File:** `30-group-rank-computation.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Results Coordinator G3 · CAO G4 · Exam Controller G3 · Academic MIS Officer G1

---

## 1. Purpose

Group Rank Computation is the engine room of the cross-branch academic ranking system. When 50 branches each upload marks independently, this page collects all uploads, validates completeness, and runs a single unified rank computation that produces a fair, cross-branch All-Group rank for every student. The outcome is the group rank list that drives topper announcements, scholarship nominations, and parent communications.

The "Compute Rankings" button is structurally disabled until every branch required for the exam has both uploaded marks and received moderation approval. This design eliminates partial-rank errors — the single most common complaint in multi-branch groups that run rankings with incomplete data. Missing branches are surfaced explicitly with branch names and their upload status so the Results Coordinator can chase the right contacts directly from this page.

Re-computation is permitted only when a branch uploads corrected marks — for example, after a data entry error is discovered. Every re-computation requires a documented reason and generates a new immutable audit entry. The re-computed rank list replaces the previous one, and the previous computation is archived with its reason.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All sections | ✅ Full — override compute, approve re-computation | Can force-compute with reason |
| Group Academic Director | G3 | ✅ Summary only | ❌ | No compute authority |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ Status table | ✅ Trigger computation only | Cannot view student marks |
| Group Results Coordinator | G3 | ✅ All sections | ✅ Full — primary operator | Can view all student ranks |
| Group Stream Coord — MPC | G3 | ✅ MPC stream only | ❌ | Filtered view, read-only |
| Group Stream Coord — BiPC | G3 | ✅ BiPC stream only | ❌ | Filtered view, read-only |
| Group Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC stream only | ❌ | Filtered view, read-only |
| Group JEE/NEET Integration Head | G3 | ✅ JEE/NEET results only | ❌ | Read-only |
| Group IIT Foundation Director | G3 | ✅ Foundation results only | ❌ | Read-only |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ Post-computation only | ❌ | Can view ranks after compute — no write |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Rank Computation
```

### 3.2 Page Header
```
Group Rank Computation                              [Export XLSX ↓]  [Re-computation Log ↓]
[Group Name] · Exam: [Exam Name]  [Change Exam ▾]
```

Exam selector dropdown at the top — switching exam reloads the entire page state via HTMX.

### 3.3 Computation Readiness Bar

A prominent status strip immediately below the header:

| Condition | Banner Style | Message |
|---|---|---|
| All branches uploaded + moderated | Green banner | "All 50 branches ready. Rank computation can proceed." |
| Some branches missing | Amber banner | "3 branches have not uploaded marks. Computation blocked." |
| No uploads at all | Grey banner | "No branches have uploaded marks yet for this exam." |
| Computation in progress | Blue banner (animated) | "Computing rankings… Please wait. This takes 1–3 minutes." |
| Computation complete | Green banner | "Rankings computed. 82,340 students ranked. Computed at [datetime] by [actor]." |

---

## 4. Main Content

### 4.1 Branch Upload Status Table

**Purpose:** Shows every branch's upload and moderation status for the selected exam. Makes it immediately clear who is blocking computation.

**Search:** Branch name — 300ms debounce.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Upload Status | Multi-select | Uploaded · Not Uploaded · Re-upload Requested |
| Moderation Status | Multi-select | Pending · Approved · Rejected |
| Included in Computation | Select | Yes · No · N/A |

### 4.2 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Row select for bulk actions |
| Branch Name | Text | ✅ | Branch code in smaller text |
| City / State | Text | ✅ | |
| Marks Uploaded | Badge | ✅ | Uploaded (green) · Not Uploaded (red) · Re-upload Pending (amber) |
| Upload Date | Datetime | ✅ | Blank if not uploaded |
| Students Count | Number | ✅ | Students whose marks are included |
| Moderation Status | Badge | ✅ | Pending · Approved · Rejected |
| Moderator | Text | ❌ | Name of group-level moderator |
| Included in Computation | Badge | ✅ | Yes · No · Excluded (manual) |
| Reason (if excluded) | Text | ❌ | Shown only for manually excluded branches |
| Actions | — | ❌ | See row actions |

**Highlight rows where upload is missing:** Full row background `bg-red-50` for "Not Uploaded" rows. Amber `bg-amber-50` for re-upload pending.

**Default sort:** Upload Status (Not Uploaded first), then Branch Name.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

### 4.3 Row Actions

| Action | Icon | Visible To | Modal/Drawer | Notes |
|---|---|---|---|---|
| Send Upload Reminder | Bell | Results Coord · CAO | Confirm modal 380px | Sends WhatsApp/email to branch principal |
| View Uploaded Marks | Table | Results Coord · CAO | `branch-marks-view` drawer 640px | Raw marks for that branch |
| Exclude from Computation | Ban | CAO only | `exclude-reason` modal 380px | With mandatory reason — audited |
| Include Back | Check | CAO only | Confirm modal | Re-includes previously excluded branch |

### 4.4 Bulk Actions (shown when rows selected)

| Action | Visible To | Notes |
|---|---|---|
| Send Upload Reminder to Selected | Results Coord · CAO | Batch reminder to selected branches |
| Export Selected Branch Status (CSV) | Results Coord · CAO · MIS | Export rows for offline tracking |

---

### 4.5 Compute Rankings Control Panel

Positioned between the status table and the rank results section. Shown only to Results Coordinator and CAO.

```
┌─────────────────────────────────────────────────────────────────────┐
│  Branches ready:  47 / 50                                            │
│  Missing: Vijayawada-02, Kurnool-01, Guntur-03  [View Missing ↑]    │
│                                                                       │
│  [  Compute Rankings  ]   ← DISABLED until all branches ready        │
│  Tip: Chase missing branches or exclude them (CAO only) to proceed   │
│                                                                       │
│  Last computed: 12 Feb 2026 · 14:30 IST · by Priya Sharma           │
│  [Re-compute] — requires reason — available only after first compute │
└─────────────────────────────────────────────────────────────────────┘
```

**Compute Rankings button state logic:**
- **Disabled (grey):** Any branch not uploaded or not moderation-approved
- **Enabled (primary blue):** All included branches uploaded and approved
- **CAO override enabled:** CAO sees "Compute with Override" secondary button that is always enabled — requires mandatory reason (min 30 chars)

---

### 4.6 Rank Results Table (shown after computation)

Displayed below the control panel after computation completes.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · Foundation · JEE/NEET |
| Class | Multi-select | Class 6–12 |
| Branch | Multi-select | All 50 branches |
| Rank Range | Select | Top 10 · Top 50 · Top 100 · Top 500 · Custom (from–to) |
| Percentile Band | Select | P90+ · P75–90 · P50–75 · Below P50 |

**Search:** Student name or roll number — 300ms debounce.

### Rank Results Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Group Rank | Number (bold) | ✅ | Primary identifier |
| Roll Number | Text | ✅ | |
| Student Name | Text | ✅ | |
| Branch | Text | ✅ | Branch name + code |
| Stream | Badge | ✅ | |
| Class | Text | ✅ | |
| Subject Marks | Multiple number cols | ✅ | One column per subject in exam |
| Total Marks | Number | ✅ | Sum of all subjects |
| Max Marks | Number | ❌ | Total possible marks |
| Percentage | Number | ✅ | (Total / Max) × 100 |
| Percentile | Number | ✅ | Group percentile (1 decimal) |
| Actions | — | ❌ | View detail |

**Pagination:** Server-side · Default 50/page · Selector 25/50/100/All.

### Rank Results Row Actions

| Action | Icon | Visible To | Opens |
|---|---|---|---|
| View Student Rank Detail | Eye | All | `student-rank-detail` drawer 480px |

---

## 5. Drawers & Modals

### 5.1 Drawer: `student-rank-detail`
- **Trigger:** Eye icon on rank results row
- **Width:** 480px
- **Tabs:** Rank Overview · Subject Breakdown · Comparison

#### Tab: Rank Overview
| Field | Value |
|---|---|
| Student Name | Full name |
| Roll Number | |
| Branch | Name + code |
| Stream | |
| Class | |
| Group Rank | Bold, large text |
| Branch Rank | Rank within own branch only |
| Percentile | e.g. 96.4th percentile |
| AIR Estimate (JEE/NEET only) | e.g. Approx. AIR 2,400–2,800 (based on mock percentile) |
| Total Score | X / Y |
| Exam Date | |

#### Tab: Subject Breakdown
Table: Subject · Score · Max · Percentage · Subject Rank (within group) · Subject Percentile

#### Tab: Comparison
Mini chart: This student's score vs group average vs branch average — per subject (radar or grouped bar).

---

### 5.2 Drawer: `branch-marks-view`
- **Trigger:** "View Uploaded Marks" row action
- **Width:** 640px
- **Header:** "Uploaded Marks — [Branch Name] — [Exam Name]"
- **Content:** Full marks table — Roll No · Student Name · Subject marks columns · Total — sortable
- **Statistical summary:** Mean · Median · SD · Min · Max — shown above table
- **Download:** "Download Branch Marks (XLSX)" button
- **Read-only** — no edit in this drawer

---

### 5.3 Modal: `compute-confirm`
- **Trigger:** "Compute Rankings" button
- **Width:** 440px
- **Title:** "Compute Group Rankings — [Exam Name]"
- **Content:**
  - "You are about to compute group ranks for [Exam Name]."
  - "Branches included: [N]"
  - "Total students: [N]"
  - "Estimated time: 1–3 minutes"
  - Warning if any branches were excluded: "Note: [N] branches excluded. Excluded branches' students will NOT be ranked."
- **Optional note:** Text field for computation log entry
- **Buttons:** [Compute Rankings] (primary) + [Cancel]

---

### 5.4 Modal: `recompute-confirm`
- **Trigger:** [Re-compute] button (post first computation)
- **Width:** 440px
- **Title:** "Re-compute Rankings — [Exam Name]"
- **Warning:** "Re-computation will replace the existing rank list. The previous computation will be archived. This action is audited."
- **Fields:**
  - Reason for re-computation (required, min 30 chars) — e.g. "Kurnool branch re-uploaded corrected marks after data entry error"
  - Notify Results Coordinator? (checkbox, default on if CAO is acting)
- **Buttons:** [Re-compute Rankings] (amber warning style) + [Cancel]

---

### 5.5 Modal: `send-reminder-confirm`
- **Width:** 380px
- **Title:** "Send Upload Reminder — [Branch Name]"
- **Content:** "Send an upload reminder to [Branch Principal Name] at [Branch Name]."
- **Channels:** WhatsApp (default on) · Email (default on)
- **Preview:** Short preview of message text
- **Buttons:** [Send Reminder] (primary) + [Cancel]
- **On confirm:** Reminder sent · Toast shown · Last reminder timestamp updated in status table

---

### 5.6 Modal: `exclude-reason`
- **Width:** 380px
- **Title:** "Exclude [Branch Name] from Rank Computation"
- **Warning:** "This branch's students will not receive a group rank for this exam. This is audited."
- **Fields:**
  - Reason (required, min 30 chars)
  - Notify branch principal? (checkbox, default on)
- **Buttons:** [Confirm Exclusion] (danger red) + [Cancel]

---

## 6. Charts

### 6.1 Score Distribution Bell Curve
- **Type:** Line chart (kernel density estimate approximated with smoothed histogram)
- **X-axis:** Total marks (0 to max marks)
- **Y-axis:** Number of students
- **Overlay:** Mean (solid vertical line, blue) · Median (dashed vertical line, teal)
- **Tooltip:** Score band · Student count · Percentile
- **Colorblind-safe:** Blue line on white background, high contrast gridlines
- **Export:** PNG

### 6.2 Percentile Band Distribution (Bar)
- **Type:** Vertical grouped bar chart
- **X-axis:** Percentile bands — P0–10 · P10–25 · P25–50 · P50–75 · P75–90 · P90–100
- **Y-axis:** Student count
- **Bars coloured:** Red (P0–25) · Amber (P25–50) · Blue (P50–75) · Green (P75–100) — colorblind-safe with distinct hues
- **Tooltip:** Band · Count · % of total students
- **Export:** PNG

### 6.3 Branch Average Score Comparison (Bar)
- **Type:** Horizontal bar chart
- **X-axis:** Average score %
- **Y-axis:** Branch names (sorted highest to lowest)
- **Colour:** Green ≥ 70% · Amber 50–70% · Red < 50%
- **Tooltip:** Branch name · Avg score · Students included · Branch rank
- **Export:** PNG
- **Shown below rank results table**

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Computation triggered | "Rank computation started for [Exam Name]. Check back in 1–3 minutes." | Info | 6s |
| Computation complete | "Rankings computed. [N] students ranked across [M] branches." | Success | 5s |
| Re-computation triggered | "Re-computation started. Previous ranks archived." | Warning | 6s |
| Reminder sent | "Upload reminder sent to [Branch Principal Name] at [Branch Name]." | Success | 4s |
| Branch excluded | "[Branch Name] excluded from rank computation. Reason recorded." | Warning | 6s |
| Branch re-included | "[Branch Name] re-included in rank computation." | Success | 4s |
| Export started | "XLSX export preparing — download will begin shortly." | Info | 4s |
| Computation failed | "Rank computation failed. Error: [reason]. Contact technical support." | Error | Manual |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No exam selected | "Select an Exam" | "Choose an exam from the dropdown above to begin rank computation" | [Select Exam ▾] |
| No branches uploaded | "No marks uploaded yet" | "Branches have not uploaded marks for this exam yet. Send reminders to branch principals." | [Send Reminders] |
| No ranks computed yet | "Ranks not computed" | "Once all branches upload and moderation is complete, click Compute Rankings." | — |
| Rank results — no search match | "No students match" | "Try a different search term or clear filters" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: readiness bar + status table (10 rows) |
| Exam selector change | Full section skeleton reload |
| Status table filter/search | Inline skeleton rows (10) |
| Rank computation running | Blue animated progress bar across top of control panel + "Computing…" text + disable all action buttons |
| Student rank detail drawer | Spinner in drawer body + skeleton content |
| Branch marks drawer | Spinner in drawer body + skeleton table |
| Export triggered | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Results Coord G3 | Exam Controller G3 | Stream Coords G3 | MIS G1 |
|---|---|---|---|---|---|
| Compute Rankings button | ✅ + Override | ✅ | ✅ (trigger only) | ❌ | ❌ |
| Re-compute button | ✅ | ✅ | ❌ | ❌ | ❌ |
| Exclude Branch from Computation | ✅ | ❌ | ❌ | ❌ | ❌ |
| Send Reminder action | ✅ | ✅ | ❌ | ❌ | ❌ |
| View Branch Marks drawer | ✅ | ✅ | ❌ | ❌ | ❌ |
| Rank Results table | ✅ | ✅ | ❌ | ✅ (own stream) | ✅ |
| Student Rank Detail drawer | ✅ | ✅ | ❌ | ✅ (own stream) | ✅ |
| AIR Estimate in drawer | ✅ | ✅ | ❌ | JEE/NEET Head only | ✅ |
| Export XLSX button | ✅ | ✅ | ❌ | ❌ | ✅ |
| Re-computation Log download | ✅ | ✅ | ❌ | ❌ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/rankings/` | JWT | Exam list for selector |
| GET | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/readiness/` | JWT | Branch upload status table |
| GET | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/readiness/stats/` | JWT | Readiness summary counts |
| POST | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/compute/` | JWT (Results Coord / CAO) | Trigger rank computation |
| GET | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/compute-status/` | JWT | Poll computation progress |
| POST | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/recompute/` | JWT (Results Coord / CAO) | Re-trigger with reason |
| GET | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/ranks/` | JWT | Rank results (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/ranks/{student_id}/` | JWT | Student rank detail |
| GET | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/branch/{branch_id}/marks/` | JWT (Results Coord / CAO) | Raw marks for branch |
| POST | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/branch/{branch_id}/reminder/` | JWT (Results Coord / CAO) | Send upload reminder |
| POST | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/branch/{branch_id}/exclude/` | JWT (CAO) | Exclude branch with reason |
| POST | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/branch/{branch_id}/include/` | JWT (CAO) | Re-include branch |
| GET | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/ranks/export/?format=xlsx` | JWT | Export rank list XLSX |
| GET | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/recompute-log/` | JWT | Re-computation history log |
| GET | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/charts/distribution/` | JWT | Bell curve chart data |
| GET | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/charts/percentile-bands/` | JWT | Percentile band chart data |
| GET | `/api/v1/group/{group_id}/acad/rankings/{exam_id}/charts/branch-avg/` | JWT | Branch average bar chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Exam selector change | `change` | GET `.../rankings/?exam_id=` | `#ranking-page-body` | `innerHTML` |
| Branch status search | `input delay:300ms` | GET `.../readiness/?q=` | `#branch-status-table-body` | `innerHTML` |
| Branch status filter | `click` | GET `.../readiness/?filters=` | `#branch-status-section` | `innerHTML` |
| Branch status sort/page | `click` | GET `.../readiness/?sort=&page=` | `#branch-status-section` | `innerHTML` |
| Compute rankings trigger | `click` | POST `.../compute/` | `#compute-panel` | `outerHTML` |
| Poll computation status | `every 5s` (conditional — while computing) | GET `.../compute-status/` | `#compute-status-banner` | `innerHTML` |
| Rank results search | `input delay:300ms` | GET `.../ranks/?q=` | `#rank-table-body` | `innerHTML` |
| Rank results filter/sort/page | `click` | GET `.../ranks/?filters=&sort=&page=` | `#rank-table-section` | `innerHTML` |
| Student rank detail drawer | `click` | GET `.../ranks/{student_id}/` | `#drawer-body` | `innerHTML` |
| Branch marks drawer | `click` | GET `.../branch/{branch_id}/marks/` | `#drawer-body` | `innerHTML` |
| Send reminder confirm | `click` | POST `.../branch/{branch_id}/reminder/` | `#branch-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
