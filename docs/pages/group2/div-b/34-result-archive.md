# 34 — Result Archive

> **URL:** `/group/acad/results/archive/`
> **File:** `34-result-archive.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** All 14 Division B roles (read-only access)

---

## 1. Purpose

The Result Archive is the institution group's permanent, immutable repository of all published exam results and rank lists. Once results are published and archived, they cannot be edited, deleted, or modified by any user at any role level — including the CAO, Chairman, or system administrators. The archive implements a strict append-only access model.

This immutability is not just a technical design choice — it is a legal and compliance requirement. In the Indian education context, archived exam results are referenced for scholarship disputes, board appeals, transfer certificate verification, and university admission counselling (especially when students cite group rank percentiles in JEE/NEET coaching contexts). A result that could be edited post-publication would destroy the evidentiary value of the archive. The platform enforces this at the database level with immutable storage policies, and the UI reflects it by showing zero destructive controls to any user.

The archive covers all completed exams for the current group, going back to the date the group joined the platform, with a configurable retention policy (default 10 years). Authorised users can view summary reports and download full result sets and rank lists in XLSX and PDF formats. The archive also provides a cross-academic-year comparison view — allowing the CAO or Academic Director to track group performance trends over multiple years.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All records | ✅ Download XLSX · Download PDF · View Summary | No edit/delete — read-only |
| Group Academic Director | G3 | ✅ All records | ✅ Download · View Summary | Read-only |
| Group Curriculum Coordinator | G2 | ✅ Limited — own stream subjects | ✅ Download own stream | Read-only, filtered |
| Group Exam Controller | G3 | ✅ All records | ✅ Download · View Summary | Read-only |
| Group Results Coordinator | G3 | ✅ All records | ✅ Download · View Summary | Primary user |
| Group Stream Coord — MPC | G3 | ✅ MPC exams only | ✅ Download MPC results | Read-only, filtered |
| Group Stream Coord — BiPC | G3 | ✅ BiPC exams only | ✅ Download BiPC results | Read-only, filtered |
| Group Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC exams only | ✅ Download MEC/CEC results | Read-only, filtered |
| Group JEE/NEET Integration Head | G3 | ✅ JEE/NEET exams only | ✅ Download | Read-only |
| Group IIT Foundation Director | G3 | ✅ Foundation exams only | ✅ Download | Read-only |
| Group Olympiad & Scholarship Coord | G3 | ✅ All records (for scholarship verification) | ✅ Download | Read-only |
| Group Special Education Coordinator | G3 | ✅ Anonymised student data only | ✅ View summaries only | Personal data masked |
| Group Academic MIS Officer | G1 | ✅ All records | ✅ Download · View Summary | Read-only — primary MIS user |
| Group Academic Calendar Manager | G3 | ✅ Summary level only | ❌ No download | Exam dates/terms only |

> **Immutability enforcement:** No edit, update, delete, or unpublish controls are shown to any user on this page. The backend rejects any such requests with HTTP 403 regardless of role. This is enforced at the Django view layer AND the database layer (row-level update/delete triggers disabled on archived records).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Result Archive
```

### 3.2 Page Header
```
Result Archive                                       [Download Full Archive Index ↓]
[Group Name] — Immutable historical record · Data retained for 10 years
```

**Immutability notice banner (always visible, light grey):**
> "This archive is read-only. No data can be edited, deleted, or modified. Access is logged."

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Archived Exams | 847 |
| Academic Years Covered | 6 (2019–20 to 2024–25) |
| Oldest Record | April 2019 |
| Streams Covered | 7 |
| Total Student Records | 4,12,000 |
| Storage Used | 18.4 GB |

---

## 4. Main Content

### 4.1 Search / Filters / Table

**Search:** Exam name — 300ms debounce, highlights match in Exam column.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Academic Year | Select | 2019–20 · 2020–21 · 2021–22 · 2022–23 · 2023–24 · 2024–25 (current) |
| Exam Type | Multi-select | Unit Test · Mid-Term · Annual · Mock Test · Coaching Test · Olympiad · Foundation Test |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · Integrated JEE/NEET |
| Class | Multi-select | Class 6–12 |
| Term | Select | Term 1 (Apr–Sep) · Term 2 (Oct–Mar) |
| Published Date | Date range picker | Date range |

Active filter chips: Dismissible, "Clear All" link, count badge.

### 4.2 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Academic Year | Text | ✅ | e.g. 2024–25 |
| Term | Badge | ✅ | Term 1 · Term 2 |
| Exam Name | Text | ✅ | Official exam name |
| Exam Type | Badge | ✅ | Unit Test · Mid-Term etc. |
| Stream | Badge | ✅ | |
| Class | Text | ✅ | |
| Branches | Number | ✅ | Branches included in this archived result |
| Students | Number | ✅ | Total students ranked |
| Published Date | Date | ✅ | Date results were published to students |
| Archived By | Text | ❌ | User who triggered archival |
| Archived At | Datetime | ✅ | Exact timestamp |
| Actions | — | ❌ | Download only — no edit/delete |

**No row checkbox / bulk select** — archival records cannot be batch-modified or deleted.

**Default sort:** Academic Year descending, then Published Date descending (newest first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50 · "Showing X–Y of Z archived exams".

### 4.3 Row Actions

| Action | Icon | Visible To | Notes |
|---|---|---|---|
| View Summary | Eye | All roles with access | Opens `archive-summary` drawer 560px |
| Download Full Results (XLSX) | XLSX icon | CAO · Academic Dir · Results Coord · Exam Controller · MIS · Stream Coords (own stream) · JEE/NEET Head · Foundation Dir · Olympiad Coord | Downloads full marks + ranks XLSX |
| Download Rank List (PDF) | PDF icon | All roles with download access | Formatted rank list PDF — notice board format |

**No edit icon. No delete icon. No unpublish icon.** These controls are structurally absent from the UI for all roles.

### 4.4 Bulk Actions

**None.** Bulk selection is disabled on the archive page. Every download is initiated per-record.

---

## 5. Drawers & Modals

### 5.1 Drawer: `archive-summary`
- **Trigger:** Eye icon row action
- **Width:** 560px
- **Title:** "[Exam Name] — [Academic Year] — Archive Summary"
- **Tabs:** Overview · Branches · Score Summary · Download History

#### Tab: Overview
| Field | Value |
|---|---|
| Exam Name | |
| Academic Year | |
| Term | |
| Exam Date | |
| Stream | |
| Class | |
| Exam Type | |
| Question Paper ID | Linked to archived paper in Exam Paper Builder |
| Total Students | |
| Branches Included | |
| Published At | Exact datetime |
| Published By | User + role |
| Archived At | Exact datetime |
| Archived By | User + role |
| Group Average | % |
| Group Pass % | % |
| Highest Score | Rank #1 score (student name not shown in this tab — see rank list PDF) |

#### Tab: Branches
Table: Branch Name · Students Included · Branch Average % · Branch Pass % · Included in Group Rank (Y/N)

Read-only — no branch-level actions.

#### Tab: Score Summary
- Percentile distribution summary table: P10 · P25 · P50 · P75 · P90 score values
- Mini bar chart: Score band distribution (0–50% / 50–70% / 70–85% / 85–100%)
- All charts read-only — export within drawer not available (use row action downloads)

#### Tab: Download History
Table: Downloaded By · Role · Date · Format (XLSX / PDF) — immutable log of who accessed this archived result.

This tab itself is read-only and cannot be edited.

---

## 6. Charts

### 6.1 Exams Archived Per Academic Year (Bar)
- **Type:** Vertical bar chart
- **X-axis:** Academic years (2019–20 through current)
- **Y-axis:** Count of exams archived
- **Colour:** Blue bars, current year highlighted in teal
- **Tooltip:** Year · Exam count · Streams covered
- **Export:** PNG

### 6.2 Group Average Trend — Multi-Year (Line)
- **Type:** Multi-line chart
- **X-axis:** Exam terms across all academic years (chronological)
- **Y-axis:** Group average marks %
- **Lines:** One per stream (MPC · BiPC · MEC · Foundation etc.)
- **Colorblind-safe palette:** 7-colour set for up to 7 streams
- **Tooltip:** Term · Stream · Group Avg %
- **Filters within chart:** Stream multi-select · Exam type filter
- **Export:** PNG
- **Position:** Below main table in a "Historical Trends" collapsible card

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| XLSX download started | "Downloading results for [Exam Name]…" | Info | 3s |
| PDF download started | "Rank list PDF downloading for [Exam Name]…" | Info | 3s |
| Archive index download | "Archive index preparing — download will begin shortly." | Info | 4s |
| Access logged | (No visible toast — silent server-side logging) | — | — |
| Download failed | "Download failed for [Exam Name]. Please try again or contact support." | Error | Manual |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No archived exams yet | "No Archived Results" | "Results are automatically archived after publication. No exams have been published yet." | [View Results Publisher →] |
| No results for filters | "No Archived Exams Match" | "Try a different academic year or clear your filters" | [Clear Filters] |
| Year has no results | "No Results for [Academic Year]" | "No exams were archived for this academic year" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) + immutability banner |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| Archive summary drawer open | Spinner in drawer body + skeleton tabs |
| XLSX / PDF download | Spinner in download button (momentary) — no page-level loader |
| Historical trend chart load | Spinner centred in chart card |

---

## 10. Role-Based UI Visibility

| Element | All Roles with Access |
|---|---|
| Immutability notice banner | ✅ Always visible |
| Edit actions (row) | ❌ Never shown to any role |
| Delete actions (row) | ❌ Never shown to any role |
| Unpublish actions (row) | ❌ Never shown to any role |
| Bulk select checkbox | ❌ Disabled on archive page |
| View Summary (drawer) | ✅ All roles with page access |
| Download XLSX | ✅ CAO · Academic Dir · Results Coord · Exam Controller · MIS · Stream Coords (own stream) |
| Download PDF | ✅ Same as XLSX |
| Download History tab in drawer | ✅ CAO · Results Coord · MIS only |
| Archive Index download (header) | ✅ CAO · MIS · Results Coord |

Stream Coordinators see only exams from their own stream — the stream filter is server-enforced and pre-applied, not just a UI filter.

Special Education Coordinator sees only anonymised summary data — student roll numbers are masked in XLSX downloads, student names never appear.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/results/archive/` | JWT | Archive list (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/results/archive/stats/` | JWT | Summary stats bar |
| GET | `/api/v1/group/{group_id}/acad/results/archive/{exam_id}/` | JWT | Archive summary drawer data |
| GET | `/api/v1/group/{group_id}/acad/results/archive/{exam_id}/branches/` | JWT | Branches tab in drawer |
| GET | `/api/v1/group/{group_id}/acad/results/archive/{exam_id}/score-summary/` | JWT | Score summary tab in drawer |
| GET | `/api/v1/group/{group_id}/acad/results/archive/{exam_id}/download-history/` | JWT (CAO / Results Coord / MIS) | Download history tab — immutable |
| GET | `/api/v1/group/{group_id}/acad/results/archive/{exam_id}/download/?format=xlsx` | JWT | Download full results XLSX |
| GET | `/api/v1/group/{group_id}/acad/results/archive/{exam_id}/download/?format=pdf` | JWT | Download rank list PDF |
| GET | `/api/v1/group/{group_id}/acad/results/archive/export/index/?format=csv` | JWT (CAO / MIS / Results Coord) | Download archive index CSV |
| GET | `/api/v1/group/{group_id}/acad/results/archive/charts/by-year/` | JWT | Exams per year bar chart data |
| GET | `/api/v1/group/{group_id}/acad/results/archive/charts/avg-trend/` | JWT | Group average trend multi-year chart |

**Backend enforcement:** PUT, PATCH, DELETE HTTP methods return HTTP 405 (Method Not Allowed) on all archive endpoints. This is enforced at the Django Router level — not just view logic.

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Archive search | `input delay:300ms` | GET `.../archive/?q=` | `#archive-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../archive/?filters=` | `#archive-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../archive/?sort=&dir=` | `#archive-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../archive/?page=` | `#archive-table-section` | `innerHTML` |
| Archive summary drawer open | `click` | GET `.../archive/{id}/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch | `click` | GET `.../archive/{id}/branches/` or `.../score-summary/` etc. | `#archive-drawer-tab-content` | `innerHTML` |
| Trend chart filter change | `change` | GET `.../archive/charts/avg-trend/?stream=&exam_type=` | `#archive-trend-chart` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
