# 44 — Olympiad Results & Awards

> **URL:** `/group/acad/olympiad/results/`
> **File:** `44-olympiad-results-awards.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Olympiad & Scholarship Coord G3 · CAO G4 · Academic MIS Officer G1 · Marketing/Div-O (read-only export)

---

## 1. Purpose

The Olympiad Results & Awards page is where official external exam results are recorded, verified, and celebrated. When NTSE results are published by NCERT, when NSO rankings arrive from Science Olympiad Foundation, or when state-level olympiad scorecards are distributed, this page is the single entry point through which those results enter the group's academic record.

Recording results serves more than archive purposes. Results on this page feed directly into two downstream actions that have real financial and operational impact: scholarship nomination (linking to the Scholarship Exam Manager on page 45 and Div-C disbursement) and marketing amplification (linking to the Division-O press release and social media workflow). A student who wins a national-level olympiad medal is a key marketing asset for the institution — but only if the win is captured, verified, and transmitted promptly.

In the Indian competitive education market — where parent decisions to continue or switch institutions are heavily influenced by olympiad performance — the visual Medal Wall on this page also serves as a motivational tool within the group's internal academic community. The page covers result entry (manual or XLSX bulk import), award level recording, certificate upload, and nomination workflows.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Nominate for scholarship | Can view all; can nominate toppers |
| Group Academic Director | G3 | ❌ | ❌ | No access |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ✅ Full | ✅ Full CRUD + nominate | Primary owner of this page |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ Read-only | ❌ | Summary stats, no student PII |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |
| Marketing / Div-O Staff | Cross-div | ✅ Read-only export | ❌ No CUD | Can export award data for PR use |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Olympiad & Scholarships  ›  Results & Awards
```

### 3.2 Page Header
```
Olympiad Results & Awards                        [+ Record Result]  [Bulk Import XLSX ↓]  [Export ↓]
[Group Name] · [Academic Year]                                                   (Olympiad Coord only)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Results Recorded | Count across all olympiads this year |
| Gold Medals | Count |
| Silver Medals | Count |
| Bronze Medals | Count |
| Merit / Qualifier | Count |
| Scholarship Nominations Pending | Count — links to scholarship nomination queue |

Stats bar is live — refreshes with page.

---

## 4. Main Content

### 4.1 Search
- Full-text across: Student name, Olympiad name, Branch name
- 300ms debounce · Highlights match in Student and Olympiad columns

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Olympiad | Multi-select | NTSE · NMMS · NSO · IMO · KVPY · State Olympiad · Other |
| Branch | Multi-select | All branches in group |
| Class | Multi-select | Class 6–12 |
| Award Level | Multi-select | Gold · Silver · Bronze · Merit · Qualifier · No Award |
| Rank Type | Select | State Rank · National Rank · International Rank |
| Scholarship Nominated | Select | Yes / No / Pending |
| Academic Year | Select | Current + last 3 years |

Active filter chips are dismissible. "Clear All" link clears all. Filter count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Row select for bulk actions |
| Olympiad | Text + badge | ✅ | |
| Branch | Text | ✅ | |
| Student Name | Text + link | ✅ | Opens student profile |
| Class | Badge | ✅ | |
| Score | Number | ✅ | Raw score or percentile |
| Rank | Text | ✅ | e.g. "State Rank 12" or "National Rank 45" |
| Award Level | Badge | ✅ | Gold / Silver / Bronze / Merit / Qualifier / None |
| Certificate | Icon | ❌ | PDF icon if uploaded; dash if not |
| Scholarship Nominated | Badge | ✅ | Yes / No |
| Entered By | Text | ❌ | Staff who recorded this result |
| Actions | — | ❌ | Role-based |

**Column visibility toggle:** Gear icon top-right.

**Default sort:** Award Level descending (Gold first), then Olympiad name, then Branch.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z results" · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Action | Notes |
|---|---|---|---|---|
| View | Eye | All roles | `result-view` drawer 480px | Full result details |
| Edit | Pencil | Olympiad Coord | `result-entry` drawer 480px | Edit score, rank, award |
| Nominate for Scholarship | Star | Olympiad Coord, CAO | Modal confirm | Triggers scholarship workflow |
| Send to Marketing | Megaphone | Olympiad Coord | Modal confirm | Sends to Div-O PR flow |
| Delete | Trash | Olympiad Coord | Confirm modal | Soft delete; requires reason |

### 4.5 Bulk Actions (shown when rows selected)

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | All with export | Selected result rows |
| Nominate Selected for Scholarship | Olympiad Coord, CAO | Bulk nomination — confirm modal |
| Export Selected — Marketing Format | Olympiad Coord | Formatted for press release |

---

## 5. Drawers & Modals

### 5.1 Drawer: `result-entry` — Record / Edit Result
- **Trigger:** [+ Record Result] button or Edit row action
- **Width:** 480px

| Field | Type | Required | Validation |
|---|---|---|---|
| Student | Search + select | ✅ | Search by name or roll — searches across all branches |
| Olympiad | Select | ✅ | From Olympiad Registry (page 42) |
| Academic Year | Select | ✅ | Current year pre-selected |
| Score | Number | ✅ | Min 0; max configured per olympiad |
| Rank Type | Select | ✅ | State / National / International / Not Ranked |
| Rank Value | Number | Conditional | Required if Rank Type selected |
| Award Level | Select | ✅ | Gold / Silver / Bronze / Merit / Qualifier / None |
| Certificate | File upload | ❌ | PDF only, max 5 MB |
| Notes | Textarea | ❌ | Max 300 chars |

- **Submit:** "Save Result" — disabled until required fields valid
- **On success:** Row added/updated in table · Toast

### 5.2 Drawer: `result-view`
- **Trigger:** View row action
- **Width:** 480px
- **Content:** All fields read-only · Certificate preview (embedded PDF viewer if uploaded) · Nomination status · Created/updated by + timestamp

### 5.3 Modal: `bulk-import-xlsx`
- **Trigger:** [Bulk Import XLSX] header button
- **Width:** 520px
- **Content:** Template download link · File upload area · Validation: max 500 rows · Error report shown inline if rows fail validation (column-level errors highlighted)
- **Fields in template:** Student Roll No · Olympiad Name · Score · Rank Type · Rank Value · Award Level · Notes
- **On success:** Preview of parsed rows before commit · [Confirm Import] button

### 5.4 Modal: `nominate-scholarship-confirm`
- **Width:** 420px
- **Content:** "Nominate [Student Name] for scholarship based on [Olympiad] [Award Level] result?"
- **Fields:** Scholarship type (Merit/External Olympiad Award) · Notes (optional)
- **Buttons:** [Confirm Nomination] (primary) · [Cancel]
- **On confirm:** Nomination record created in Scholarship Exam Manager (page 45) · Notification to Results Coordinator

### 5.5 Modal: `send-to-marketing-confirm`
- **Width:** 420px
- **Content:** "Share [Student Name]'s [Olympiad] result with the Marketing team for press release?"
- **Fields:** Include photo? (checkbox) · Message to marketing team (textarea, optional)
- **Buttons:** [Send to Marketing] · [Cancel]
- **On confirm:** Div-O workflow triggered · Log entry created

---

## 6. Charts

### 6.1 Medals by Olympiad (Grouped Bar)
- **Type:** Grouped horizontal bar
- **Data:** Gold/Silver/Bronze count per olympiad
- **X-axis:** Count
- **Y-axis:** Olympiad names
- **Series:** Gold · Silver · Bronze (colorblind-safe: amber, teal, coral)
- **Tooltip:** Olympiad · Gold: N · Silver: N · Bronze: N
- **Export:** PNG

### 6.2 Branch Performance — Award Distribution (Stacked Bar)
- **Type:** Stacked bar (vertical)
- **Data:** Awards per branch, stacked by award level
- **X-axis:** Branch names
- **Y-axis:** Award count
- **Tooltip:** Branch · Award breakdown
- **Export:** PNG

### 6.3 Medal Wall (Visual Section — not a chart.js chart)
- **Layout:** Card grid (4 columns, responsive to 2 on tablet) — shown below charts
- **Each card:** Student photo (if uploaded, else initials avatar) · Student name · Olympiad name · Award badge (Gold/Silver/Bronze icon) · Branch name
- **Sorted:** Gold first, then Silver, then Bronze
- **Visible to:** All roles with access to this page

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Result recorded | "Result recorded for [Student Name] — [Olympiad]" | Success | 4s |
| Result updated | "Result updated for [Student Name]" | Success | 4s |
| Result deleted | "Result removed. Record archived." | Warning | 6s |
| Scholarship nominated | "[Student Name] nominated for scholarship" | Success | 4s |
| Sent to marketing | "Result shared with Marketing team" | Success | 4s |
| Bulk import success | "[N] results imported successfully" | Success | 4s |
| Bulk import partial | "[N] imported, [M] rows had errors — see error report" | Warning | 6s |
| Export started | "Export preparing… download will start shortly" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No results recorded yet | "No olympiad results recorded" | "Record results when official scorecards arrive from exam bodies" | [+ Record Result] |
| No results match filters | "No results match your filters" | "Try adjusting or clearing your filters" | [Clear Filters] |
| No search results | "No results found" | "Check the student name or olympiad name and try again" | [Clear Search] |
| Medal wall — no medals | "No medals yet this year" | "Gold, Silver, and Bronze awardees will appear here once results are recorded" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar (6 cards) + table (10 rows) + chart areas |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| Result entry drawer open | Spinner in drawer body |
| Bulk import drawer open | Spinner |
| Result view drawer open | Spinner → rendered content |
| Chart load | Skeleton chart placeholder → chart renders |
| Medal wall load | Skeleton card grid (8 cards) |

---

## 10. Role-Based UI Visibility

| Element | Olympiad Coord G3 | CAO G4 | MIS G1 | Marketing/Div-O |
|---|---|---|---|---|
| [+ Record Result] button | ✅ | ❌ | ❌ | ❌ |
| [Bulk Import XLSX] button | ✅ | ❌ | ❌ | ❌ |
| [Export] button | ✅ | ✅ | ✅ | ✅ |
| Edit row action | ✅ | ❌ | ❌ | ❌ |
| Delete row action | ✅ | ❌ | ❌ | ❌ |
| Nominate for Scholarship | ✅ | ✅ | ❌ | ❌ |
| Send to Marketing action | ✅ | ❌ | ❌ | ❌ |
| Bulk nomination | ✅ | ✅ | ❌ | ❌ |
| Student name (PII) | ✅ | ✅ | ❌ (count only) | ✅ (export only) |
| Medal Wall | ✅ | ✅ | ❌ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/olympiad/results/` | JWT | List results (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/olympiad/results/stats/` | JWT | Summary stats bar data |
| POST | `/api/v1/group/{group_id}/acad/olympiad/results/` | JWT (G3) | Record new result |
| PUT | `/api/v1/group/{group_id}/acad/olympiad/results/{id}/` | JWT (G3) | Update result |
| DELETE | `/api/v1/group/{group_id}/acad/olympiad/results/{id}/` | JWT (G3) | Soft delete result |
| POST | `/api/v1/group/{group_id}/acad/olympiad/results/bulk-import/` | JWT (G3) | XLSX bulk import |
| POST | `/api/v1/group/{group_id}/acad/olympiad/results/{id}/nominate/` | JWT (G3/G4) | Nominate for scholarship |
| POST | `/api/v1/group/{group_id}/acad/olympiad/results/{id}/send-marketing/` | JWT (G3) | Trigger Div-O PR workflow |
| GET | `/api/v1/group/{group_id}/acad/olympiad/results/medal-wall/` | JWT | Medal wall card data |
| GET | `/api/v1/group/{group_id}/acad/olympiad/results/export/?format=xlsx` | JWT | Export results |
| GET | `/api/v1/group/{group_id}/acad/olympiad/results/charts/medals-by-olympiad/` | JWT | Grouped bar chart data |
| GET | `/api/v1/group/{group_id}/acad/olympiad/results/charts/branch-awards/` | JWT | Stacked bar chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../results/?q=` | `#results-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../results/?filters=` | `#results-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../results/?sort=&dir=` | `#results-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../results/?page=` | `#results-table-section` | `innerHTML` |
| Result view drawer | `click` | GET `.../results/{id}/` | `#drawer-body` | `innerHTML` |
| Result entry drawer open | `click` | GET `.../results/entry-form/` | `#drawer-body` | `innerHTML` |
| Result entry submit | `submit` | POST `.../results/` | `#drawer-body` | `innerHTML` |
| Medal wall load | `load` | GET `.../results/medal-wall/` | `#medal-wall-container` | `innerHTML` |
| Nominate confirm | `click` | POST `.../results/{id}/nominate/` | `#toast-container` | `beforeend` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
