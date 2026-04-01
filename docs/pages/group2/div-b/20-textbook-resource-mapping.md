# 20 — Textbook & Resource Mapping

> **URL:** `/group/acad/textbooks/`
> **File:** `20-textbook-resource-mapping.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** CAO G4 · Academic Director G3 · Curriculum Coordinator G2 · Stream Coords G3 · Academic MIS Officer G1

---

## 1. Purpose

The Textbook & Resource Mapping page is the group's authoritative register of prescribed textbooks — one source of truth that maps board, class, and subject to the exact textbook that every branch must use. For a group operating across CBSE, BSEAP, BSETS, and State Board affiliations simultaneously, different boards mandate different textbooks for the same subject — this page resolves that complexity centrally.

Branch procurement teams use the export from this page to generate their annual textbook purchase lists. Without this registry, branches in a 50-branch group would each independently identify textbooks, leading to variation, double-procurement, and students in the same stream using different editions. The Curriculum Coordinator and Academic Director maintain this register at the start of each academic year, adding any new editions or revised board-prescribed texts, and flagging outdated editions for replacement.

The page also serves the Library & Learning Resources division as a cross-reference for library acquisitions. While this page does not link to the Library module directly, the export format is compatible with library procurement formats used across Indian educational institutions, including publisher name, ISBN, edition year, and approximate price in Indian Rupees (₹).

---

## 2. Role Access

| Role | Level | Can View | Can Create | Can Edit | Can Delete | Notes |
|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ | ✅ | ✅ (Archive only) | Full authority |
| Group Academic Director | G3 | ✅ All | ✅ | ✅ | ✅ (Archive only) | Operational ownership |
| Group Curriculum Coordinator | G2 | ✅ All | ✅ | ✅ | ❌ | Add and edit textbook entries |
| Group Exam Controller | G3 | ✅ All | ❌ | ❌ | ❌ | View for exam paper reference |
| Group Results Coordinator | G3 | ❌ | ❌ | ❌ | ❌ | No access |
| Stream Coord — MPC | G3 | ✅ MPC only | ❌ | ❌ | ❌ | View own stream textbooks |
| Stream Coord — BiPC | G3 | ✅ BiPC only | ❌ | ❌ | ❌ | View own stream textbooks |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC only | ❌ | ❌ | ❌ | View own stream textbooks |
| JEE/NEET Integration Head | G3 | ✅ MPC+BiPC | ❌ | ❌ | ❌ | View coaching reference books |
| IIT Foundation Director | G3 | ✅ Foundation only | ❌ | ❌ | ❌ | View Foundation textbooks |
| Olympiad & Scholarship Coord | G3 | ✅ All | ❌ | ❌ | ❌ | View for olympiad reference materials |
| Special Education Coordinator | G3 | ✅ All | ❌ | ❌ | ❌ | View for adapted material identification |
| Academic MIS Officer | G1 | ✅ All | ❌ | ❌ | ❌ | Read-only |
| Academic Calendar Manager | G3 | ❌ | ❌ | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Textbook & Resource Mapping
```

### 3.2 Page Header (with action buttons — role-gated)
```
Textbook & Resource Mapping               [+ Add Textbook]  [Export Procurement List ↓]
[Group Name] · Prescribed textbook register                (CAO / Academic Dir / Curriculum Coord)
```

Action button visibility:
- `[+ Add Textbook]` — CAO, Academic Director, Curriculum Coordinator
- `[Export Procurement List ↓]` — All roles with view access (exports branch-ready XLSX)

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Textbook Entries | Count of active entries |
| Academic Year | Current year (e.g. 2025–26) |
| Boards Covered | Count of boards with at least 1 entry |
| Subjects Mapped | Count of distinct subjects with at least 1 textbook |
| Entries Without ISBN | Count (data quality alert) |
| Updated This Month | Count of new/edited entries |

Stats bar refreshes on page load.

---

## 4. Main Textbook Table

### 4.1 Search
- Full-text across: Textbook Name, Publisher, Subject, ISBN
- 300ms debounce · Highlights match in Textbook Name column
- Scope: Current academic year active entries by default

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Board | Multi-select | CBSE · BSEAP · BSETS · ICSE · State Board |
| Class | Multi-select | Class 6–12 |
| Subject | Multi-select | Populated based on Board + Class selection |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · Foundation |
| Year (Edition) | Select | 2020 · 2021 · 2022 · 2023 · 2024 · 2025 |
| Publisher | Multi-select | NCERT · Arihant · S. Chand · Pearson · Laxmi · Oswaal · Orient Black Swan · Others |
| Status | Multi-select | Active · Superseded · Archived |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | CAO, Academic Dir, Coord | Row select for bulk actions |
| Board | Badge | ✅ | All | CBSE / BSEAP / BSETS / State |
| Class | Text | ✅ | All | e.g. Class 11 |
| Subject | Text | ✅ | All | Subject name |
| Textbook Name | Text + link | ✅ | All | Opens textbook-add drawer (edit mode) |
| Publisher | Text | ✅ | All | e.g. NCERT, S. Chand |
| ISBN | Text | ✅ | All | 13-digit ISBN. "—" if not entered |
| Edition Year | Text | ✅ | All | e.g. 2024 |
| Approx Price (₹) | Number | ✅ | CAO, Academic Dir, Curriculum Coord, MIS | ₹ value — for procurement budgeting |
| Status | Badge | ✅ | All | Active · Superseded · Archived |
| Actions | — | ❌ | Role-based | See Row Actions |

**Column visibility toggle:** Gear icon top-right — saves preference per user.

**Default sort:** Board ascending, then Class ascending, then Subject ascending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z entries" · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| Edit | Pencil | CAO, Academic Dir, Curriculum Coord | `textbook-add` drawer 480px (edit mode) | Pre-filled |
| Mark Superseded | Replace icon | CAO, Academic Dir | Inline confirm + new edition prompt | Marks current as Superseded, prompts to add replacement |
| Archive | Archive box | CAO, Academic Dir | Confirm modal 420px | Soft archive |

### 4.5 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | All with view access | Procurement format with all columns including price |
| Archive Selected | CAO, Academic Dir | Batch archive — requires reason |
| Mark Selected as Superseded | CAO, Academic Dir | Batch supersede — use when new edition replaces old |

---

## 5. Drawers & Modals

### 5.1 Drawer: `textbook-add` — Add / Edit Textbook
- **Trigger:** [+ Add Textbook] button or Edit row action
- **Width:** 480px

| Field | Type | Required | Validation |
|---|---|---|---|
| Board | Select | ✅ | CBSE · BSEAP · BSETS · ICSE · State Board |
| Class | Select | ✅ | Class 6–12 |
| Stream | Multi-select | ❌ | Optional — associates textbook with stream |
| Subject | Select | ✅ | From Subject-Topic Master filtered by Board + Class |
| Textbook Title | Text | ✅ | Min 3 chars, max 200 |
| Publisher | Text | ✅ | Min 2 chars, max 100 |
| Author(s) | Text | ❌ | Comma-separated |
| ISBN (13-digit) | Text | ❌ | 13-digit validation. Warning shown if empty |
| Edition Year | Select | ✅ | 2018–current year |
| Approx Price (₹) | Number | ❌ | Integer, ₹1–₹10,000 |
| Alternate Textbook | Text | ❌ | Acceptable substitute if primary not available |
| Remarks | Textarea | ❌ | Max 200 chars — e.g. "NCERT mandatory for CBSE; supplementary allowed" |
| Status | Select | ✅ | Active · Superseded |

**Submit:** "Save Textbook" — validates ISBN format if provided. Duplicate detection: warns if same Board + Class + Subject + Publisher combination already exists.

### 5.2 Modal: Mark as Superseded
- **Width:** 420px
- **Content:** "Mark '[Textbook Name]' as superseded? You will be prompted to add the replacement edition."
- **Fields:** Effective from academic year (select — current or next year)
- **Buttons:** [Mark Superseded & Add Replacement] (primary) → opens `textbook-add` drawer with subject/board/class pre-filled for new entry + [Cancel]

### 5.3 Modal: Archive Confirm
- **Width:** 420px
- **Content:** "Archive '[Textbook Name]'? This entry will no longer appear in procurement exports."
- **Fields:** Reason (required, min 10 chars)
- **Buttons:** [Confirm Archive] (danger) + [Cancel]

---

## 6. Charts

No charts section. This page is a data register; analysis happens in the Academic MIS and branch dashboards. The Export Procurement List is the primary output mechanism.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Textbook added | "'[Title]' added to register for [Board] Class [X] — [Subject]." | Success | 4s |
| Textbook updated | "'[Title]' updated." | Success | 4s |
| Marked superseded | "'[Title]' marked as superseded." | Warning | 5s |
| Textbook archived | "'[Title]' archived." | Warning | 6s |
| Duplicate warning | "A textbook for this Board/Class/Subject/Publisher combination already exists. Check before saving." | Warning | Manual |
| Export started | "Procurement list preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No entries in register | "No textbooks mapped yet" | "Add the first textbook to build the procurement register." | [+ Add Textbook] |
| No results for search | "No textbooks match" | "Try a different title, publisher, or ISBN." | [Clear Search] |
| Filter returns empty | "No textbooks match your filters" | "Try removing some filters." | [Clear All Filters] |
| Board + Class has no entries | "No textbooks mapped for [Board] Class [X]" | "Add textbooks for this board and class." | [+ Add Textbook] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| textbook-add drawer open | Spinner in drawer body |
| Textbook save submit | Spinner in submit button |
| Archive confirm submit | Spinner in confirm button |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Curriculum Coord G2 | Exam Controller G3 | Stream Coords G3 | MIS Officer G1 |
|---|---|---|---|---|---|---|
| [+ Add Textbook] button | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| [Export Procurement List] button | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Edit row action | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Mark Superseded action | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Archive row action | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Bulk archive | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Approx Price (₹) column | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Stream filter (all streams) | ✅ | ✅ | ✅ | ✅ | ❌ (own only) | ✅ |
| Row checkbox (for bulk) | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/textbooks/` | JWT | List entries (filtered/sorted/paginated) |
| POST | `/api/v1/group/{group_id}/acad/textbooks/` | JWT (CAO/Dir/Coord) | Add textbook entry |
| GET | `/api/v1/group/{group_id}/acad/textbooks/{tb_id}/` | JWT | Textbook detail |
| PUT | `/api/v1/group/{group_id}/acad/textbooks/{tb_id}/` | JWT (CAO/Dir/Coord) | Update entry |
| DELETE | `/api/v1/group/{group_id}/acad/textbooks/{tb_id}/` | JWT (CAO/Dir) | Archive entry (soft) |
| POST | `/api/v1/group/{group_id}/acad/textbooks/{tb_id}/supersede/` | JWT (CAO/Dir) | Mark as superseded |
| GET | `/api/v1/group/{group_id}/acad/textbooks/export/` | JWT | Procurement XLSX export |
| GET | `/api/v1/group/{group_id}/acad/textbooks/stats/` | JWT | Summary stats bar data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Textbook search | `input delay:300ms` | GET `.../textbooks/?q=` | `#textbook-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../textbooks/?filters=` | `#textbook-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../textbooks/?sort=&dir=` | `#textbook-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../textbooks/?page=` | `#textbook-table-section` | `innerHTML` |
| Add drawer open | `click` | GET `.../textbooks/add-form/` | `#drawer-body` | `innerHTML` |
| Edit drawer open | `click` | GET `.../textbooks/{id}/edit-form/` | `#drawer-body` | `innerHTML` |
| Save submit | `submit` | POST or PUT `.../textbooks/` | `#drawer-body` | `innerHTML` |
| Archive confirm | `click` | DELETE `.../textbooks/{id}/` | `#textbook-row-{id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../textbooks/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
