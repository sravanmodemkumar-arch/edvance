# 48 — Accommodation Request Tracker

> **URL:** `/group/acad/special-ed/accommodations/`
> **File:** `48-accommodation-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Special Education Coordinator G3 · CAO G4 · Exam Controller G3 (approved accommodations view)

---

## 1. Purpose

The Accommodation Request Tracker manages the pipeline through which branches formally request exam accommodations for students with special needs, and the Group Special Education Coordinator reviews and approves or denies each request. Once approved, accommodations are automatically flagged in the Branch Exam Schedule (page 25) so that the Exam Controller and branch staff know exactly what to arrange — a separate room, a scribe, extra time, or large-print paper — for each affected student in each upcoming exam.

Without this tracker, accommodation requests are communicated informally by phone or email, creating a compliance and welfare risk: a student entitled to a scribe under their IEP might be seated in the main exam hall simply because the branch forgot to request or the Exam Controller was unaware of the entitlement. This page eliminates that gap by creating a formal, auditable request-and-approval chain that feeds directly into exam logistics.

The accommodation types supported reflect CBSE's official Special Assessment Provisions and the guidelines of the Board of Secondary Education for respective state boards operating in the group: extra time (30 or 60 additional minutes), provision of a scribe, separate examination room, large-font question paper, oral examination option, and a designated reader. Approved accommodations are immutable once the exam begins — revocation or modification requires Coordinator-level action with a reason.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Override approve/deny | Final override authority |
| Group Academic Director | G3 | ❌ | ❌ | No access |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ Approved accommodations only | ❌ | Read-only; sees only Approved status rows — for exam logistics |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ✅ Full | ✅ Full CRUD + approve/deny | Primary owner |
| Group Academic MIS Officer | G1 | ❌ | ❌ | No access |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |
| Branch Principal | Branch portal | ❌ (submits via branch) | ❌ | Submits requests via branch portal; not this page |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Special Education  ›  Accommodation Request Tracker
```

### 3.2 Page Header
```
Accommodation Request Tracker                              [Export Approved List ↓]
Exam accommodations for special needs students     Pending: [N] · Upcoming exams: [N]
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Pending Review | Count — amber |
| Approved | Count — green |
| Denied | Count — red |
| Partially Approved | Count — teal |
| Implemented (exam conducted) | Count |
| Upcoming Exams with Accommodations | Count of exams within 14 days that have approved accommodations |

---

## 4. Main Content

### 4.1 Search
- Full-text across: Student ID, Request ID, Exam name, Branch name
- Student name search available to Special Ed Coord and CAO only
- 300ms debounce · Highlights match in Request ID and Exam columns

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Exam | Multi-select | Upcoming and past exams (from Group Exam Calendar) |
| Status | Multi-select | Pending · Approved · Partially Approved · Denied · Implemented |
| Accommodation Type | Multi-select | Extra time 30 min · Extra time 60 min · Scribe · Separate room · Large font paper · Oral exam · Reader |
| Exam date range | Date range picker | |
| Submitted date | Date range picker | |

Exam Controller sees only Status = Approved and Implemented (enforced server-side; filter still shows but status locked).

Active filter chips dismissible. "Clear All". Filter badge count.

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Bulk select (Spec Ed Coord only) |
| Request ID | Text | ✅ | e.g. ACC-2025-00341 |
| Student ID | Text | ✅ | |
| Student Name | Text | ✅ | Visible to Spec Ed Coord and CAO; hidden from Exam Controller |
| Branch | Text | ✅ | |
| Exam | Text + link | ✅ | Links to exam in Group Exam Calendar |
| Exam Date | Date | ✅ | Red if exam ≤ 3 days; amber if ≤ 7 days |
| Accommodation Type | Tags | ❌ | All requested types shown as tags |
| Status | Badge | ✅ | Pending (amber) · Approved (green) · Partially Approved (teal) · Denied (red) · Implemented (grey) |
| Requested By | Text | ✅ | Branch staff name |
| Submitted At | Datetime | ✅ | |
| Actions | — | ❌ | Role-based |

**Default sort:** Exam Date ascending (soonest exams first), then Status (Pending first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Action | Notes |
|---|---|---|---|---|
| Review | Clipboard | Special Ed Coord, CAO | `accommodation-request-view` drawer 480px | Full review with decision |
| View (read-only) | Eye | Exam Controller | `accommodation-view-readonly` drawer 480px | Approved details only |
| Approve | Check | Special Ed Coord, CAO | Inline confirm | Quick approve with optional note |
| Deny | X | Special Ed Coord | Confirm modal | Reason required |
| Mark Implemented | Flag | Special Ed Coord | Inline confirm | After exam conducted |

### 4.5 Bulk Actions (Spec Ed Coord only)

| Action | Notes |
|---|---|
| Approve Selected | Bulk approve with optional note — confirm modal |
| Export Approved (XLSX) | Export all approved accommodations for logistics sharing |

---

## 5. Drawers & Modals

### 5.1 Drawer: `accommodation-request-view` — Review & Decide
- **Trigger:** Review row action
- **Width:** 480px

**Section 1 — Student & Disability**
- Student ID · Student name · Branch · Class
- Disability type · Severity (from Special Needs Registry page 46)
- IEP reference link (links to IEP Manager page 47)
- Medical certificate status (Uploaded / Not uploaded)

**Section 2 — Exam Details**
- Exam name · Date · Duration · Venue type
- Other accommodated students in same exam: Count

**Section 3 — Requested Accommodations**
Table of requested accommodation types with:

| Accommodation | Requested | Medical Basis | Reviewer Decision |
|---|---|---|---|
| Extra time 30 min | ✅ | IEP reference | Approve / Deny |
| Extra time 60 min | ❌ | — | — |
| Scribe | ✅ | Medical cert attached | Approve / Deny |
| Separate room | ❌ | — | — |
| Large font paper | ✅ | IEP reference | Approve / Deny |
| Oral exam | ❌ | — | — |
| Reader | ❌ | — | — |

Each requested accommodation line has its own Approve / Deny radio — enabling partial approval.

**Section 4 — Decision**
| Field | Type | Required | Notes |
|---|---|---|---|
| Overall decision | Auto | — | Approved / Partially Approved / Denied — computed from individual lines |
| Reviewer notes | Textarea | ❌ | Internal notes; not visible to branch |
| Reason for any denial | Textarea | Conditional | Required if any line is denied; min 20 chars |
| Notify branch on decision | Toggle | ✅ | Default on |

- **Buttons:** [Save Decision] · [Cancel]
- **On save:** Status updated in table · Branch notified if toggle on · Approved accommodations auto-flagged in Branch Exam Schedule (page 25) for this student × exam combination

### 5.2 Drawer: `accommodation-view-readonly` (Exam Controller view)
- **Width:** 480px
- **Content:** Student ID (no name) · Branch · Exam · Accommodation types approved · Exam date · Implementation notes
- Read-only; no action buttons

### 5.3 Modal: `deny-confirm`
- **Width:** 420px
- **Trigger:** Deny action on row
- **Content:** "Deny accommodation request [ACC-ID] for Student [ID] — [Exam Name]?"
- **Fields:** Reason (Textarea, required, min 20 chars) · Notify branch (checkbox, default on)
- **Buttons:** [Confirm Deny] (danger) · [Cancel]

### 5.4 Modal: `bulk-approve-confirm`
- **Width:** 420px
- **Content:** "Approve [N] selected accommodation requests?"
- **Fields:** Note to branches (optional, Textarea) · Notify all branches (checkbox, default on)
- **Buttons:** [Confirm Bulk Approve] · [Cancel]
- **On confirm:** All selected rows updated to Approved · Branch Exam Schedule flagged for each · Notifications sent

---

## 6. Charts

### 6.1 Accommodation Type Usage (Horizontal Bar)
- **Type:** Horizontal bar
- **Data:** Count of approved accommodations per type across current academic year
- **X-axis:** Count
- **Y-axis:** Accommodation type labels
- **Colour:** Single colorblind-safe teal
- **Tooltip:** Type · Count
- **Export:** PNG

### 6.2 Request Status Distribution (Donut)
- **Type:** Donut
- **Data:** Pending / Approved / Partially Approved / Denied / Implemented
- **Centre text:** Total requests this year
- **Tooltip:** Status · Count · %
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Request approved | "Accommodation approved for Student [ID] — [Exam]. Branch Exam Schedule updated." | Success | 4s |
| Request partially approved | "Partial accommodation approved for Student [ID]. Branch notified." | Success | 4s |
| Request denied | "Accommodation request denied. Branch notified with reason." | Warning | 6s |
| Bulk approve | "[N] accommodation requests approved. Branch Exam Schedules updated." | Success | 4s |
| Marked implemented | "Accommodation marked as implemented for [Exam]" | Success | 4s |
| Export triggered | "Export preparing… download will start shortly" | Info | 4s |
| Branch Exam Schedule integration error | "Accommodation approved but Exam Schedule update failed — retry or update manually" | Error | Manual dismiss |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No requests yet | "No accommodation requests" | "Requests submitted by branches via the branch portal will appear here for review" | — |
| No pending requests | "No pending requests" | "All requests have been reviewed. Well done." | — |
| No approved (Exam Controller view) | "No approved accommodations" | "Approved accommodations for upcoming exams will appear here" | — |
| No results match filters | "No requests match your filters" | "Clear filters to see all requests" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) |
| Table filter/search/sort/page | Inline skeleton rows |
| Review drawer open | Spinner → content renders |
| Readonly drawer open | Spinner → content |
| Bulk approve submit | Spinner in confirm button + table refreshes |
| Export triggered | Spinner in export button |

---

## 10. Role-Based UI Visibility

| Element | Spec Ed Coord G3 | CAO G4 | Exam Controller G3 |
|---|---|---|---|
| Full request table | ✅ | ✅ | ✅ (Approved/Implemented only) |
| Student name column | ✅ | ✅ | ❌ (hidden) |
| Review action | ✅ | ✅ | ❌ |
| Approve inline action | ✅ | ✅ | ❌ |
| Deny action | ✅ | ✅ | ❌ |
| View readonly action | ❌ | ❌ | ✅ |
| Mark Implemented | ✅ | ❌ | ❌ |
| Bulk actions | ✅ | ❌ | ❌ |
| [Export Approved List] | ✅ | ✅ | ✅ |
| Stats bar | ✅ (full) | ✅ (full) | ✅ (Approved/Implemented counts only) |
| Reviewer notes field | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/special-ed/accommodations/` | JWT | List requests (role-filtered) |
| GET | `/api/v1/group/{group_id}/acad/special-ed/accommodations/stats/` | JWT | Stats bar |
| GET | `/api/v1/group/{group_id}/acad/special-ed/accommodations/{id}/` | JWT (G3+) | Request detail |
| POST | `/api/v1/group/{group_id}/acad/special-ed/accommodations/{id}/decide/` | JWT (G3 Spec Ed, G4) | Approve/deny with per-type decisions |
| POST | `/api/v1/group/{group_id}/acad/special-ed/accommodations/bulk-approve/` | JWT (G3 Spec Ed) | Bulk approve |
| PATCH | `/api/v1/group/{group_id}/acad/special-ed/accommodations/{id}/implemented/` | JWT (G3 Spec Ed) | Mark implemented |
| GET | `/api/v1/group/{group_id}/acad/special-ed/accommodations/export/?format=xlsx&status=approved` | JWT | Export approved list |
| GET | `/api/v1/group/{group_id}/acad/special-ed/accommodations/charts/type-usage/` | JWT | Bar chart |
| GET | `/api/v1/group/{group_id}/acad/special-ed/accommodations/charts/status-distribution/` | JWT | Donut chart |

**Branch Exam Schedule integration (internal service call on approval):**
| POST | `/api/v1/group/{group_id}/acad/branch-exam-schedule/flag-accommodation/` | Internal JWT | Flags student+exam combination in schedule |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../accommodations/?q=` | `#accommodation-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../accommodations/?filters=` | `#accommodation-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../accommodations/?sort=&dir=` | `#accommodation-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../accommodations/?page=` | `#accommodation-table-section` | `innerHTML` |
| Review drawer open | `click` | GET `.../accommodations/{id}/review-form/` | `#drawer-body` | `innerHTML` |
| Decision submit | `submit` | POST `.../accommodations/{id}/decide/` | `#acc-row-{id}` | `outerHTML` |
| View readonly drawer | `click` | GET `.../accommodations/{id}/` | `#drawer-body` | `innerHTML` |
| Mark implemented | `click` | PATCH `.../accommodations/{id}/implemented/` | `#acc-row-{id}` | `outerHTML` |
| Stats bar refresh | `revealed` | GET `.../accommodations/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
