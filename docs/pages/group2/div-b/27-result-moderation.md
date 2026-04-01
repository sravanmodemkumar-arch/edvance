# 27 — Result Moderation

> **URL:** `/group/acad/result-moderation/`
> **File:** `27-result-moderation.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** CAO G4 · Exam Controller G3 · Results Coordinator G3 · Stream Coords G3 · Academic MIS Officer G1

---

## 1. Purpose

Result Moderation is the quality gate between raw marks uploaded by branches and results published to students and parents. The workflow is: branches upload raw marks through the branch portal → marks arrive in this queue → the Exam Controller or Results Coordinator opens the moderation view → statistical checks run automatically → the moderator reviews, adjusts if necessary, and approves → results are released to the Cross-Branch Results Publisher for final publication.

At group scale, this page manages result data for thousands of students across 50 branches simultaneously. An annual exam at a large group might involve 40,000–80,000 individual mark entries arriving from 50 branches within a 48-hour window. The statistical check engine automatically flags anomalies: branches where the average score is below 25% (possible data entry error), standard deviation above 30 (unusual spread), missing roll numbers in the upload, or any entry where marks exceed the maximum for that subject. These flags are surfaced prominently in the moderation view before any human review begins.

The Moderation Adjustments tab allows the Results Coordinator to make documented mark changes within policy — for example, applying grace marks per board policy, correcting a transcription error flagged by the branch, or adjusting for a printing error in the exam paper. Every adjustment is recorded with reason and actor, creating a complete audit chain from raw upload to published result.

---

## 2. Role Access

| Role | Level | Can View | Can Open Moderation | Can Adjust Marks | Can Approve | Can Reject | Notes |
|---|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ | ✅ | ✅ | ✅ | Full override authority |
| Group Academic Director | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | View-only |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | ❌ | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ All | ✅ | ✅ | ✅ | ✅ | Operational ownership |
| Group Results Coordinator | G3 | ✅ All | ✅ | ✅ | ✅ | ✅ | Approve and publish |
| Stream Coord — MPC | G3 | ✅ MPC | ❌ | ❌ | ❌ | ❌ | View own stream results |
| Stream Coord — BiPC | G3 | ✅ BiPC | ❌ | ❌ | ❌ | ❌ | View own stream results |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC | ❌ | ❌ | ❌ | ❌ | View own stream results |
| JEE/NEET Integration Head | G3 | ✅ JEE/NEET | ❌ | ❌ | ❌ | ❌ | View coaching results |
| IIT Foundation Director | G3 | ✅ Foundation | ❌ | ❌ | ❌ | ❌ | View Foundation results |
| Olympiad & Scholarship Coord | G3 | ❌ | ❌ | ❌ | ❌ | ❌ | No access |
| Special Education Coordinator | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | View for IEP student result tracking |
| Academic MIS Officer | G1 | ✅ All | ❌ | ❌ | ❌ | ❌ | Read-only |
| Academic Calendar Manager | G3 | ❌ | ❌ | ❌ | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Result Moderation
```

### 3.2 Page Header (with action buttons — role-gated)
```
Result Moderation                         [Approve All Passing]  [Export XLSX ↓]
[Group Name] · Branch marks → group review → publication         (CAO / Exam Controller / Results Coord)
```

Action button visibility:
- `[Approve All Passing]` — CAO, Exam Controller, Results Coordinator (approves all branches for selected exam that pass all statistical checks)
- `[Export XLSX ↓]` — CAO, Exam Controller, Results Coordinator, Academic Director, MIS Officer

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Awaiting Upload | Branch-exam pairs where marks not yet uploaded |
| Uploaded, Unreviewed | Uploaded but moderation not started |
| Under Moderation | Currently being reviewed |
| Approved | Cleared for publication |
| Published | Results released to students |
| Rejected / Re-upload Requested | Count of returned uploads |

Stats bar refreshes on page load.

---

## 4. Main Moderation Queue Table

### 4.1 Search
- Full-text across: Exam Name, Branch Name
- 300ms debounce · Highlights match in Exam and Branch columns
- Scope: All statuses except Archived by default

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Exam Name | Search input | From Group Exam Calendar |
| Branch | Multi-select | All branches |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · Foundation · Integrated JEE · NEET |
| Class | Multi-select | Class 6–12 |
| Status | Multi-select | Awaiting Upload · Uploaded · Under Moderation · Approved · Published · Rejected |
| Date Uploaded | Date range | From / To |
| Has Flags | Toggle | Show only rows with at least 1 statistical flag |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | CAO, Exam Controller, Results Coord | Row select for bulk approve |
| Exam | Text | ✅ | All | Exam name |
| Branch | Text + link | ✅ | All | Branch name — opens branch-exam-detail |
| Stream | Badge | ✅ | All | Stream |
| Class | Text | ✅ | All | Class |
| Marks Uploaded | Badge | ✅ | All | Yes / No / Partial |
| Upload Date | Date+time | ✅ | All | When branch uploaded marks. "—" if not yet uploaded |
| Moderator | Text | ✅ | CAO, Exam Controller, Results Coord | Assigned moderator or "Unassigned" |
| Statistical Flags | Badge | ✅ | All | Count of auto-flags. Red if > 0 |
| Status | Badge | ✅ | All | Awaiting Upload · Uploaded · Under Moderation · Approved · Published · Rejected |
| Actions | — | ❌ | Role-based | See Row Actions |

**Default sort:** Status (Uploaded first, then Under Moderation), then Upload Date ascending (oldest first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

**Row highlighting:** Rows with statistical flags have an amber left border. Rejected rows have red.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| Download Raw Marks | Download | CAO, Exam Controller, Results Coord | Direct XLSX download | Raw marks as uploaded by branch |
| Open Moderation View | Eye + pencil | CAO, Exam Controller, Results Coord | `moderation-view` drawer 680px | Full moderation workflow |
| Approve | Checkmark | CAO, Exam Controller, Results Coord | Inline confirm | Available only if no critical flags |
| Reject with Reason | X | CAO, Exam Controller, Results Coord | `reject-reason` drawer 480px | Returns to branch for re-upload |
| Request Re-upload | Refresh | CAO, Exam Controller, Results Coord | `re-upload-request` modal 420px | Branch must re-upload corrected marks |

### 4.5 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Approve All Branches for This Exam | CAO, Exam Controller, Results Coord | Approves all branches for a selected exam that pass all statistical checks |
| Export Selected (XLSX) | CAO, Exam Controller, Results Coord, MIS | Raw marks + moderation status export |

---

## 5. Drawers & Modals

### 5.1 Drawer: `moderation-view` — Moderation Workflow
- **Trigger:** Open Moderation View row action
- **Width:** 680px
- **Tabs:** Raw Marks Table · Statistical Checks · Moderation Adjustments · Approval

#### Tab: Raw Marks Table
Full student marks table: Roll No · Student Name · Subject 1 · Subject 2 · ... · Total · Pass/Fail (computed).

- Sortable by any column
- Editable cells: show only in Moderation Adjustments tab (not here — read-only in this tab)
- Pagination within drawer: 50 rows per page
- Filter within drawer: show only Fail / show only Pass / show only flagged rows
- Download button: raw marks XLSX

Flags displayed inline:
- Red cell: marks exceed maximum for subject
- Amber cell: marks are 0 (check if absent or error)
- Orange row: student roll number not in enrollment list

#### Tab: Statistical Checks
Auto-computed checks run on upload. Re-runs on demand via [Re-run Checks] button.

| Check | Threshold | Flag Type |
|---|---|---|
| Average score | < 25% average → possible data error | Critical (blocks approval) |
| Standard deviation | > 30 → unusual spread | Warning (advisory) |
| Missing roll numbers | Any enrolled student missing from upload | Critical (blocks approval) |
| Marks exceed maximum | Any subject mark > max marks | Critical (blocks approval) |
| Z-score outliers | Students with Z-score > 3.5 or < -3.5 | Warning (advisory) |
| Pass rate | > 98% or < 5% → possible data anomaly | Warning (advisory) |
| Total mismatch | Uploaded total ≠ sum of subjects | Critical (blocks approval) |

Each check: Status (Pass/Fail) · Details · Affected students/count.

Critical flag present → [Approve] button in Approval tab is disabled with tooltip explaining which checks failed. Moderator must resolve or the CAO must use force-approve with override reason.

#### Tab: Moderation Adjustments
Table of all mark changes made during moderation. Initially empty.

[+ Add Adjustment] button opens inline row:
- Roll No (search from students list) · Subject · Original Mark · Adjusted Mark · Reason (required, select from: Grace marks per board policy · Transcription error · Printing error in paper · Other) · Evidence (text) · Authorised by (pre-filled with current user)

All adjustments are non-destructive — original marks preserved; adjusted marks shown alongside. Any adjustment triggers a re-run of statistical checks.

Adjustment history: immutable once saved. Cannot be deleted. Can be reversed by adding a new adjustment row returning to original value.

#### Tab: Approval
Read-only summary: exam, branch, stream, class, total students, pass count, fail count, pass %, statistical check summary.

**Approval action (CAO/Exam Controller/Results Coordinator):**
- [Approve] — enabled only if no critical flags (or CAO using override)
- [Force Approve (Override)] — CAO only — requires override reason (min 50 chars) — fully audited
- [Reject with Reason] → opens reject-reason drawer
- [Request Re-upload] → opens re-upload-request modal

**On Approve:** Status → Approved · Moderation timestamp logged · Exam entry in Cross-Branch Results Publisher updated.

### 5.2 Drawer: `reject-reason` — Rejection
- **Trigger:** Reject with Reason row action or button in Approval tab
- **Width:** 480px

| Field | Type | Required | Validation |
|---|---|---|---|
| Rejection Reason | Textarea | ✅ | Min 30 chars — specific and actionable |
| Issues Found | Multi-select | ❌ | Critical flags unresolved · Marks exceed maximum · Missing students · Statistical anomaly · Other |
| Notify Branch Principal | Checkbox | — | Default on |
| Resubmission Deadline | Date picker | ❌ | Optional deadline for branch to re-upload |

**Submit:** "Send Rejection" — branch notified. Status → Rejected.

### 5.3 Modal: `re-upload-request` — Request Re-upload
- **Width:** 420px
- **Content:** "Request [Branch Name] to re-upload marks for [Exam Name]?"
- **Fields:** Reason (required) · Issues to fix (freeform) · Deadline for re-upload (date picker) · Notify branch principal (checkbox, default on)
- **Buttons:** [Send Request] (primary) + [Cancel]
- **On confirm:** Branch notified via WhatsApp + email · Status → "Re-upload Requested"

---

## 6. Charts

### 6.1 Marks Distribution Histogram (Rendered Inside Moderation Drawer)
- **Type:** Histogram — rendered in Statistical Checks tab of the moderation view drawer
- **Data:** Score distribution for all students in this branch-exam
- **X-axis:** Score bands (0–9, 10–19, 20–29, ..., 90–100)
- **Y-axis:** Student count
- **Overlay:** Normal distribution curve for comparison
- **Tooltip:** Score band · Count · % of total
- **Reference lines:** Mean (blue) · Median (green) · ±1 SD (grey dashed)
- **Export:** PNG from within drawer

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Marks approved | "[Branch Name] — [Exam Name] marks approved." | Success | 4s |
| Marks rejected | "[Branch Name] — [Exam Name] rejected. Branch notified." | Warning | 6s |
| Re-upload requested | "Re-upload request sent to [Branch Name]." | Info | 4s |
| Force approve (CAO) | "[Branch Name] force-approved by override. Audit entry created." | Warning | 6s |
| Bulk approved | "[N] branches approved for [Exam Name]." | Success | 4s |
| Adjustment saved | "Mark adjustment saved for Roll No [X] — [Subject]." | Info | 4s |
| Statistical check re-run | "Statistical checks re-run. [N] flags found." | Info | 4s |
| Export started | "Export preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No uploads awaiting | "No results pending moderation" | "All uploaded results have been reviewed. Awaiting branch uploads for upcoming exams." | [View Exam Calendar] |
| No matches for search | "No results match" | "Try a different exam or branch name." | [Clear Search] |
| Filter returns empty | "No results match your filters" | "Try removing some filters." | [Clear All Filters] |
| No adjustments made | "No adjustments yet" | "All marks are as uploaded by the branch." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| moderation-view drawer open | Spinner + skeleton tabs |
| Raw marks table load (in drawer) | Spinner in table area — may take 1–3s for large branches |
| Statistical checks load | Spinner in checks tab |
| Statistical checks re-run | Spinner + "Running checks…" text |
| Marks adjustment save | Spinner in save button |
| Approve action | Spinner in approve button |
| Reject action | Spinner in reject button |
| Bulk approve | Full overlay "Approving [N] branches…" |
| Histogram chart render | Spinner in chart area |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Exam Controller G3 | Results Coord G3 | Stream Coords G3 | MIS Officer G1 |
|---|---|---|---|---|---|
| [Approve All Passing] button | ✅ | ✅ | ✅ | ❌ | ❌ |
| [Export XLSX] button | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ |
| Open Moderation View action | ✅ | ✅ | ✅ | ❌ | ❌ |
| Approve action (row) | ✅ | ✅ | ✅ | ❌ | ❌ |
| Reject action (row) | ✅ | ✅ | ✅ | ❌ | ❌ |
| Request Re-upload action | ✅ | ✅ | ✅ | ❌ | ❌ |
| Force Approve (override) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Moderation Adjustments tab | ✅ | ✅ | ✅ | ❌ | ❌ |
| Statistical Checks tab | ✅ | ✅ | ✅ | ❌ | ❌ |
| Download Raw Marks | ✅ | ✅ | ✅ | ❌ | ❌ |
| Moderator column | ✅ | ✅ | ✅ | ❌ | ✅ |
| Statistical Flags column | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ |
| Stream filter (all streams) | ✅ | ✅ | ✅ | ❌ (own only) | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/result-moderation/` | JWT | List moderation queue (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/result-moderation/{mod_id}/` | JWT | Moderation item detail |
| GET | `/api/v1/group/{group_id}/acad/result-moderation/{mod_id}/raw-marks/` | JWT (mod roles) | Raw marks table data |
| GET | `/api/v1/group/{group_id}/acad/result-moderation/{mod_id}/download/` | JWT (mod roles) | Download raw marks XLSX |
| GET | `/api/v1/group/{group_id}/acad/result-moderation/{mod_id}/stats-checks/` | JWT (mod roles) | Statistical check results |
| POST | `/api/v1/group/{group_id}/acad/result-moderation/{mod_id}/stats-checks/rerun/` | JWT (mod roles) | Re-run statistical checks |
| POST | `/api/v1/group/{group_id}/acad/result-moderation/{mod_id}/adjustments/` | JWT (mod roles) | Add mark adjustment |
| POST | `/api/v1/group/{group_id}/acad/result-moderation/{mod_id}/approve/` | JWT (mod roles) | Approve moderation item |
| POST | `/api/v1/group/{group_id}/acad/result-moderation/{mod_id}/force-approve/` | JWT (CAO) | Force approve with override reason |
| POST | `/api/v1/group/{group_id}/acad/result-moderation/{mod_id}/reject/` | JWT (mod roles) | Reject with reason |
| POST | `/api/v1/group/{group_id}/acad/result-moderation/{mod_id}/request-reupload/` | JWT (mod roles) | Request re-upload |
| POST | `/api/v1/group/{group_id}/acad/result-moderation/bulk-approve/` | JWT (mod roles) | Bulk approve passing items |
| GET | `/api/v1/group/{group_id}/acad/result-moderation/stats/` | JWT | Summary stats bar data |
| GET | `/api/v1/group/{group_id}/acad/result-moderation/export/` | JWT | XLSX export |
| GET | `/api/v1/group/{group_id}/acad/result-moderation/{mod_id}/charts/histogram/` | JWT (mod roles) | Marks distribution histogram data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Queue search | `input delay:300ms` | GET `.../result-moderation/?q=` | `#moderation-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../result-moderation/?filters=` | `#moderation-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../result-moderation/?sort=&dir=` | `#moderation-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../result-moderation/?page=` | `#moderation-table-section` | `innerHTML` |
| Moderation drawer open | `click` | GET `.../result-moderation/{id}/` | `#drawer-body` | `innerHTML` |
| Raw marks pagination (drawer) | `click` | GET `.../result-moderation/{id}/raw-marks/?page=` | `#raw-marks-table` | `innerHTML` |
| Re-run stats checks | `click` | POST `.../result-moderation/{id}/stats-checks/rerun/` | `#stats-checks-content` | `innerHTML` |
| Approve (row) | `click` | POST `.../result-moderation/{id}/approve/` | `#mod-row-{id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../result-moderation/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
