# 17 — Shared Content Library

> **URL:** `/group/acad/content-library/`
> **File:** `17-shared-content-library.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** CAO G4 · Academic Director G3 · Curriculum Coordinator G2 · Stream Coords G3 · Academic MIS Officer G1 · Library & Learning Resources Head (Div-L G2, upload access)

---

## 1. Purpose

The Shared Content Library is the group's central repository of all academic learning resources — PDF notes, video links (YouTube or hosted), MCQ sets, revision sheets, model answer papers, and reference documents. Every resource uploaded here is immediately accessible to all branches in the group through the branch portal, ensuring that a well-prepared set of notes from one branch's teacher becomes available to 49 other branches within minutes of approval.

For a group with 50 branches and 2,000–5,000 teachers, the library eliminates the redundancy of every branch independently creating the same material. It enforces a quality gate through the content review workflow: resources uploaded by branch teachers or stream coordinators must be approved before going live. Only CAO, Academic Director, and Curriculum Coordinator can approve — preventing low-quality content from reaching students group-wide.

The Library & Learning Resources Head from Division L (Library & Learning Resources) also has upload access to this library. This cross-division access ensures that centrally procured digital resources — textbook PDFs, reference materials, and licensed content — can be added to the academic content pool without requiring a Division B staff member to do the upload. All uploads from Div-L go through the same content review queue before going live.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Upload | Can Edit | Can Delete | Notes |
|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ | ✅ | ✅ (Archive) | Full authority + approve content |
| Group Academic Director | G3 | ✅ All | ✅ | ✅ | ✅ (Archive) | Approve and manage library |
| Group Curriculum Coordinator | G2 | ✅ All | ✅ | ✅ Own uploads | ❌ | Upload + edit own content; cannot approve |
| Group Exam Controller | G3 | ✅ All | ❌ | ❌ | ❌ | View for question bank cross-reference |
| Group Results Coordinator | G3 | ✅ All | ❌ | ❌ | ❌ | View-only |
| Stream Coord — MPC | G3 | ✅ MPC | ✅ (own stream) | ✅ Own uploads | ❌ | Upload for MPC stream; review queue for approval |
| Stream Coord — BiPC | G3 | ✅ BiPC | ✅ (own stream) | ✅ Own uploads | ❌ | Upload for BiPC stream |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC | ✅ (own stream) | ✅ Own uploads | ❌ | Upload for MEC/CEC stream |
| JEE/NEET Integration Head | G3 | ✅ MPC+BiPC | ✅ (JEE/NEET) | ✅ Own uploads | ❌ | Upload coaching resources |
| IIT Foundation Director | G3 | ✅ Foundation | ✅ (Foundation) | ✅ Own uploads | ❌ | Upload Foundation materials |
| Olympiad & Scholarship Coord | G3 | ✅ All | ✅ | ✅ Own uploads | ❌ | Upload olympiad prep material |
| Special Education Coordinator | G3 | ✅ All | ✅ | ✅ Own uploads | ❌ | Upload adapted/accessible content |
| Academic MIS Officer | G1 | ✅ All | ❌ | ❌ | ❌ | Read-only |
| Academic Calendar Manager | G3 | ✅ All | ❌ | ❌ | ❌ | View-only |
| Library & Learning Resources Head (Div-L) | G2 | ✅ All | ✅ | ✅ Own uploads | ❌ | Cross-division upload access — goes to review queue |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Shared Content Library
```

### 3.2 Page Header (with action buttons — role-gated)
```
Shared Content Library                    [+ Upload Content]  [Export XLSX ↓]
[Group Name] · Central academic resource repository         (Roles with upload access)
```

Action button visibility:
- `[+ Upload Content]` — CAO, Academic Dir, Curriculum Coord, Stream Coords, JEE/NEET Head, Foundation Dir, Olympiad Coord, Special Ed Coord, Div-L Library Head
- `[Export XLSX ↓]` — All roles with view access

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Resources | Count of active approved items |
| Added This Month | Count |
| Pending Review | Count (links to Content Upload Queue page 21) |
| Rejected This Month | Count |
| Total Downloads (This Term) | Count |
| Most Downloaded Subject | Subject name |

Stats bar refreshes on page load.

---

## 4. Main Content Library Table

### 4.1 Search
- Full-text across: Title, Topic Keyword, Subject Name, Uploaded By
- 300ms debounce · Highlights match in Title column
- Scope: Active approved content by default

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Content Type | Multi-select | PDF · Video (YouTube) · MCQ Set · Revision Sheet · Model Answer · Reference Doc |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · Integrated JEE · Integrated NEET |
| Subject | Multi-select | Populated based on Stream selection |
| Class | Multi-select | Class 6–12 |
| Status | Multi-select | Active · Pending Review · Rejected · Archived |
| Date Uploaded | Date range | From / To date picker |
| Uploaded By | Search input | Filter by uploader name or role |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | All | Row select for bulk actions |
| Title | Text + link | ✅ | All | Opens content-review drawer (preview) |
| Type | Badge | ✅ | All | PDF · Video · MCQ Set · Revision · Model Answer |
| Subject | Text | ✅ | All | Subject name |
| Topic | Text | ✅ | All | Topic within subject |
| Stream | Badge | ✅ | All | Stream badge |
| Class | Text | ✅ | All | Class 6–12 |
| Uploaded By | Text | ✅ | All | Uploader name + role |
| Date | Date | ✅ | All | Upload date |
| Downloads | Number | ✅ | CAO, Academic Dir, MIS | Total download count |
| Status | Badge | ✅ | All | Active · Pending Review · Rejected · Archived |
| Actions | — | ❌ | Role-based | See Row Actions |

**Column visibility toggle:** Gear icon top-right — saves preference per user.

**Default sort:** Date uploaded descending (newest first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z resources" · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| View | Eye | All | `content-review` drawer 560px (preview tab) | Opens preview + metadata |
| Download | Download | All with view access | Direct file download / URL open | PDF downloads file; Video opens YouTube URL |
| Edit Metadata | Pencil | CAO, Academic Dir, Curriculum Coord, Uploader (own content) | `content-upload` drawer 680px (edit mode) | Edit title, subject, topic, stream |
| Archive | Archive box | CAO, Academic Dir | Confirm modal 420px | Soft archive — reason required |
| Move to Stream | Arrows | CAO, Academic Dir, Curriculum Coord | `move-stream` modal 420px | Reassign content to different stream |

### 4.5 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Archive Selected | CAO, Academic Dir | Batch archive — requires reason |
| Move to Subject | CAO, Academic Dir, Curriculum Coord | Reassign selected items to a different subject |
| Change Stream | CAO, Academic Dir, Curriculum Coord | Reassign selected to different stream |
| Export Selected (XLSX) | All with view access | Metadata only — no file export |

---

## 5. Drawers & Modals

### 5.1 Drawer: `content-upload` — Upload Content
- **Trigger:** [+ Upload Content] header button
- **Width:** 680px
- **Tabs:** File / Link · Metadata · Access Scope · Preview · Submit

#### Tab: File / Link
| Field | Type | Required | Validation |
|---|---|---|---|
| Content Type | Select | ✅ | PDF · Video (YouTube link) · MCQ Set · Revision Sheet · Model Answer · Reference Doc |
| File Upload | File input | Conditional | Required if Type = PDF / Revision / MCQ Set / Model Answer. Max 50 MB. Accepted: .pdf, .docx, .xlsx |
| Video URL | URL input | Conditional | Required if Type = Video. Must be valid YouTube URL |
| Title | Text | ✅ | Min 3 chars, max 200 |
| Description | Textarea | ❌ | Max 500 chars |

#### Tab: Metadata
| Field | Type | Required | Validation |
|---|---|---|---|
| Stream | Multi-select | ✅ | At least 1 stream |
| Class | Multi-select | ✅ | At least 1 class |
| Subject | Select | ✅ | From Subject-Topic Master filtered by Stream |
| Topic | Select | ✅ | From Subject-Topic Master filtered by Subject |
| Board | Multi-select | ❌ | CBSE · BSEAP · BSETS · ICSE |
| Tags | Tag input | ❌ | Freeform comma-separated keywords |
| Language | Select | ❌ | English · Telugu · Hindi · Tamil · Kannada |

#### Tab: Access Scope
| Field | Type | Required | Notes |
|---|---|---|---|
| Visible To | Multi-select | ✅ | All Branches · Select Branches · Group Staff Only |
| Branch Scope | Multi-select | Conditional | Required if "Select Branches" chosen |
| Available From | Date | ❌ | Schedule content to appear from a future date |

#### Tab: Preview
Live preview panel:
- PDF: Embedded PDF viewer (first 3 pages)
- Video: YouTube thumbnail embed
- MCQ Set: First 5 questions rendered

Read-only. Navigation back to edit tabs if content looks wrong.

#### Tab: Submit
| Field | Type | Required | Notes |
|---|---|---|---|
| Submit for Review | Button | — | Sends to Content Upload Queue (page 21) for approval |
| Notes to Reviewer | Textarea | ❌ | Optional context for the approving reviewer |

**Submit:** "Submit for Review" — content enters Pending Review status. CAO/Academic Dir uploading their own content can self-approve via a "Publish Directly" toggle.

### 5.2 Drawer: `content-review` — Preview & Review
- **Trigger:** View row action or Title column link
- **Width:** 560px
- **Tabs:** Preview · Metadata · Reviewer Notes · Approve / Reject

#### Tab: Preview
Full embedded preview of content (PDF viewer or YouTube embed). Download button at bottom.

#### Tab: Metadata
Read-only display: Title, Type, Subject, Topic, Stream, Class, Uploaded By, Date, Downloads, Tags, Board, Language.

#### Tab: Reviewer Notes
Displays all reviewer comments from the Content Upload Queue workflow. Each note: reviewer name, date, comment text. Read-only.

#### Tab: Approve / Reject
Visible only to: CAO, Academic Director, Curriculum Coordinator (for own-stream uploads).
- [Approve] button — publishes content as Active
- [Reject] button → opens reject-reason input (required, min 20 chars) + "Notify uploader?" checkbox
- [Request Changes] button → sends feedback without rejecting — status remains Pending Review

### 5.3 Modal: Archive Confirm
- **Width:** 420px
- **Content:** "Archive '[Title]'? This resource will no longer be visible to branches."
- **Fields:** Reason (required, min 10 chars)
- **Buttons:** [Confirm Archive] (danger) + [Cancel]

### 5.4 Modal: Move to Stream
- **Width:** 420px
- **Fields:** Current stream (read-only) · Target stream (select) · Confirm subject/topic still valid (checkbox)
- **Buttons:** [Move Resource] (primary) + [Cancel]

---

## 6. Charts

### 6.1 Downloads by Subject (Bar Chart)
- **Type:** Vertical bar chart
- **Data:** Total downloads per subject this term
- **X-axis:** Subject names
- **Y-axis:** Download count
- **Tooltip:** Subject · Downloads: N · Most downloaded: [title]
- **Filter:** Stream selector, Class selector, Date range
- **Export:** PNG

### 6.2 Content Additions per Month (Line Chart)
- **Type:** Line chart — monthly data points
- **Data:** New resources added per month (last 12 months)
- **X-axis:** Month (Apr–Mar)
- **Y-axis:** Resources added
- **Tooltip:** Month · Added: N · Approved: M · Rejected: P
- **Export:** PNG

### 6.3 Coverage by Topic (% Complete)
- **Type:** Horizontal bar chart
- **Data:** % of topics in selected subject with at least 1 approved resource
- **X-axis:** % coverage (0–100%)
- **Y-axis:** Topic names
- **Colour:** Red 0%, Amber < 50%, Green ≥ 50%
- **Filter:** Stream, Subject, Class
- **Export:** PNG · XLSX raw data

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Content submitted for review | "'[Title]' submitted for review." | Success | 4s |
| Content approved (self-approve) | "'[Title]' published to library." | Success | 4s |
| Content approved (by reviewer) | "'[Title]' approved and live." | Success | 4s |
| Content rejected | "'[Title]' rejected. Uploader notified." | Warning | 6s |
| Content archived | "'[Title]' archived." | Warning | 6s |
| Content metadata updated | "'[Title]' metadata updated." | Success | 4s |
| Move to stream | "'[Title]' moved to [Stream]." | Success | 4s |
| Export started | "Export preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No content in library | "Library is empty" | "Upload the first resource to build your content library." | [+ Upload Content] |
| No content for subject | "No content for this subject yet" | "Upload the first resource for [Subject]." | [+ Upload Content] |
| No results for search | "No content matches" | "Try different title or topic keywords." | [Clear Search] |
| Filter returns empty | "No content matches your filters" | "Try removing some filters." | [Clear All Filters] |
| No approved content (only pending) | "Content is awaiting review" | "[N] resources are pending approval. Check the Upload Queue." | [View Upload Queue] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| content-upload drawer open | Spinner in drawer body |
| content-review drawer open | Spinner + skeleton tabs |
| File upload in progress | Progress bar in File/Link tab |
| Preview tab load | Spinner in preview area |
| Content approve/reject submit | Spinner in action button |
| Charts load | Skeleton chart placeholders |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Curriculum Coord G2 | Stream Coords G3 | MIS Officer G1 | Div-L Library Head G2 |
|---|---|---|---|---|---|---|
| [+ Upload Content] button | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| [Export XLSX] button | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Edit Metadata row action | ✅ | ✅ | ✅ (own) | ✅ (own) | ❌ | ✅ (own) |
| Archive row action | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Approve / Reject tab | ✅ | ✅ | ✅ (own stream) | ❌ | ❌ | ❌ |
| Downloads column | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Bulk archive | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Stream filter (all streams) | ✅ | ✅ | ✅ | ❌ (own only) | ✅ | ✅ |
| Status filter (all statuses) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (own uploads) |
| Charts section | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/content-library/` | JWT | List resources (filtered/sorted/paginated) |
| POST | `/api/v1/group/{group_id}/acad/content-library/` | JWT (upload roles) | Upload new resource |
| GET | `/api/v1/group/{group_id}/acad/content-library/{res_id}/` | JWT | Resource detail + preview metadata |
| PUT | `/api/v1/group/{group_id}/acad/content-library/{res_id}/` | JWT (edit roles) | Update metadata |
| DELETE | `/api/v1/group/{group_id}/acad/content-library/{res_id}/` | JWT (CAO/Dir) | Archive resource (soft) |
| POST | `/api/v1/group/{group_id}/acad/content-library/{res_id}/approve/` | JWT (CAO/Dir/Coord) | Approve resource |
| POST | `/api/v1/group/{group_id}/acad/content-library/{res_id}/reject/` | JWT (CAO/Dir/Coord) | Reject resource with reason |
| GET | `/api/v1/group/{group_id}/acad/content-library/{res_id}/download/` | JWT | Serve file download or redirect to URL |
| GET | `/api/v1/group/{group_id}/acad/content-library/stats/` | JWT | Summary stats bar data |
| GET | `/api/v1/group/{group_id}/acad/content-library/export/` | JWT | XLSX metadata export |
| GET | `/api/v1/group/{group_id}/acad/content-library/charts/downloads-by-subject/` | JWT | Bar chart data |
| GET | `/api/v1/group/{group_id}/acad/content-library/charts/additions-trend/` | JWT | Line chart data |
| GET | `/api/v1/group/{group_id}/acad/content-library/charts/topic-coverage/` | JWT | Coverage bar chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Content search | `input delay:300ms` | GET `.../content-library/?q=` | `#library-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../content-library/?filters=` | `#library-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../content-library/?sort=&dir=` | `#library-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../content-library/?page=` | `#library-table-section` | `innerHTML` |
| View/preview drawer | `click` | GET `.../content-library/{id}/` | `#drawer-body` | `innerHTML` |
| Upload drawer open | `click` | GET `.../content-library/upload-form/` | `#drawer-body` | `innerHTML` |
| Upload submit | `submit` | POST `.../content-library/` | `#drawer-body` | `innerHTML` |
| Approve action | `click` | POST `.../content-library/{id}/approve/` | `#content-row-{id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../content-library/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
