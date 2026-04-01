# 26 — Exam Conflict Monitor

> **URL:** `/group/acad/exam-conflicts/`
> **File:** `26-exam-conflict-monitor.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 · Exam Controller G3 · Academic Calendar Manager G3

---

## 1. Purpose

The Exam Conflict Monitor is the automated conflict detection and resolution centre for exam scheduling across all branches. Every time an exam is created or modified in the Group Exam Calendar, the system runs an instant conflict check and surfaces any overlapping schedules here. The rule is simple: zero unresolved hard conflicts are tolerated. A persistent alert banner appears across all academic pages until every hard conflict is resolved.

Conflicts come in two severities. Hard conflicts are scheduling errors that must be resolved before an exam can be published — for example, two exams scheduled at the same branch on the same date and time. Soft conflicts are warnings that may or may not require action — for example, two different streams in the same branch running exams on the same day (allowed, but flagged so the Exam Controller can verify venues and invigilator capacity are adequate). The monitor groups conflicts by type and allows the Exam Controller to take resolution actions directly: reschedule one of the conflicting exams, merge them if appropriate, or acknowledge and ignore a soft conflict with a documented reason.

The resolution workflow is fully audited. Every decision — reschedule, merge, or ignore — is logged with actor and timestamp. CAO can see the full history of how a conflict was identified and resolved, providing accountability for scheduling decisions that affect tens of thousands of students across 50 branches.

---

## 2. Role Access

| Role | Level | Can View | Can Resolve | Can Ignore (Soft) | Notes |
|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ | ✅ | Full authority — override any conflict |
| Group Academic Director | G3 | ✅ All | ❌ | ❌ | View-only |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ All | ✅ | ✅ | Operational ownership |
| Group Results Coordinator | G3 | ✅ All | ❌ | ❌ | View for result planning |
| Stream Coord — MPC | G3 | ✅ (if involves MPC) | ❌ | ❌ | View conflicts affecting own stream |
| Stream Coord — BiPC | G3 | ✅ (if involves BiPC) | ❌ | ❌ | View conflicts affecting own stream |
| Stream Coord — MEC/CEC | G3 | ✅ (if involves MEC/CEC) | ❌ | ❌ | View conflicts affecting own stream |
| JEE/NEET Integration Head | G3 | ✅ (JEE/NEET) | ❌ | ❌ | View coaching exam conflicts |
| IIT Foundation Director | G3 | ✅ (Foundation) | ❌ | ❌ | View Foundation conflicts |
| Olympiad & Scholarship Coord | G3 | ❌ | ❌ | ❌ | No access |
| Special Education Coordinator | G3 | ❌ | ❌ | ❌ | No access |
| Academic MIS Officer | G1 | ❌ | ❌ | ❌ | No access |
| Academic Calendar Manager | G3 | ✅ All | ❌ | ✅ (Soft, propose only) | View + propose resolutions; cannot execute directly |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Exam Conflict Monitor
```

### 3.2 Page Header (with action buttons — role-gated)
```
Exam Conflict Monitor                     [Run Conflict Check ↻]  [Export XLSX ↓]
[Group Name] · Automated conflict detection and resolution         (CAO / Exam Controller)
```

Action button visibility:
- `[Run Conflict Check ↻]` — CAO, Exam Controller (manual trigger; also runs automatically on every exam create/edit)
- `[Export XLSX ↓]` — CAO, Exam Controller, Academic Calendar Manager

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Open Conflicts | Count of Unresolved conflicts |
| Hard Conflicts | Count (red if > 0) |
| Soft Conflicts | Count (amber) |
| Resolved This Week | Count |
| Ignored (with reason) | Count |
| Last Conflict Check | Timestamp of last auto-detection run |

Stats bar refreshes on page load. Hard Conflicts > 0 shows a persistent banner: "⚠ [N] unresolved hard conflict(s). Affected exams cannot be published until resolved."

This banner also appears on the Group Exam Calendar, Branch Exam Schedule, and Exam Paper Builder pages.

---

## 4. Main Conflict List

### 4.1 Search
- Full-text across: Conflict ID, Exam Names involved, Branch Names
- 300ms debounce · Highlights match in Conflict ID column

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Conflict Type | Multi-select | Same branch, same date/time · Same stream, same date (multi-branch) · Same class + branch, overlapping window · Holiday overlap · Back-to-back (< 30 min gap) |
| Severity | Multi-select | Hard · Soft |
| Status | Multi-select | Open · Resolved · Ignored (with reason) |
| Date Range | Date range | Conflict exam date From / To |
| Branch | Multi-select | Branches involved in conflict |
| Stream | Multi-select | Streams involved |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Conflict Groups

Conflicts are displayed grouped by conflict type with a section heading and count. Within each group, rows represent individual conflicts.

**Group headings:**
1. Same Branch, Same Date/Time (Hard)
2. Same Class + Branch, Overlapping Window (Hard)
3. Holiday Overlap (Hard)
4. Same Branch, Back-to-Back Exams (Soft)
5. Same Stream, Same Date — Multiple Branches (Soft, informational)

### 4.4 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| Conflict ID | Text | ✅ | All | Auto-generated e.g. CONF-2025-0042 |
| Type | Badge | ✅ | All | Conflict type description |
| Exams Involved | Text + links | ❌ | All | Names of 2+ conflicting exams (each links to Group Exam Calendar) |
| Branches | Text | ✅ | All | Affected branch names |
| Date | Date | ✅ | All | Date of the conflicting exams |
| Severity | Badge | ✅ | All | Hard (red) · Soft (amber) |
| Status | Badge | ✅ | All | Open · Resolved · Ignored |
| Detected At | Date+time | ✅ | All | When system detected this conflict |
| Actions | — | ❌ | Role-based | See Row Actions |

**Default sort:** Severity (Hard first), then Date ascending (soonest conflict first), then Status (Open first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

### 4.5 Row Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| View Detail | Eye | All | `conflict-detail` drawer 560px | Full conflict breakdown + resolution options |
| Reschedule Exam A | Calendar | CAO, Exam Controller | Opens Group Exam Calendar drawer for Exam A | Pre-filtered to that exam's edit form |
| Reschedule Exam B | Calendar | CAO, Exam Controller | Opens Group Exam Calendar drawer for Exam B | Pre-filtered to that exam's edit form |
| Ignore | X | CAO, Exam Controller (Soft only) | `ignore-confirm` modal 420px | Reason required — Hard conflicts cannot be ignored |

### 4.6 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | CAO, Exam Controller, Calendar Mgr | Conflict report export |

---

## 5. Drawers & Modals

### 5.1 Drawer: `conflict-detail` — Conflict Detail
- **Trigger:** View Detail row action or Conflict ID column link
- **Width:** 560px
- **Tabs:** Affected Exams · Timeline · Proposed Resolution · Action

#### Tab: Affected Exams
Table showing each conflicting exam:
- Exam Name · Stream · Class · Branch · Date · Start Time · End Time · Status · Paper Status
Each row has [View Exam] link → opens Group Exam Calendar view drawer for that exam.

Conflict type description: plain-language explanation of why this is a conflict. e.g. "Both exams are scheduled at Hyderabad East Branch on 15 April 2026 from 9:00 AM to 12:00 PM. The same physical space and invigilators cannot serve two simultaneous exams."

#### Tab: Timeline
Chronological event log for this conflict:
- Conflict detected → by system at [timestamp]
- Exam A created → by [user] at [timestamp]
- Exam B created → by [user] at [timestamp]
- Resolution actions (if any)

#### Tab: Proposed Resolution
For Open conflicts — system suggests one or more resolution options based on conflict type:

| Resolution | Description |
|---|---|
| Reschedule Exam A | Move Exam A to next available non-conflicting date |
| Reschedule Exam B | Move Exam B to next available non-conflicting date |
| Merge Exams | If same paper — schedule once for both groups (separate halls) |
| Ignore (Soft only) | Acknowledge with reason — conflict remains visible but won't block publish |

Each option shows a one-line preview of what the proposed change would look like. [Apply This Resolution] button (CAO/Exam Controller only) executes the proposed change.

Calendar Manager: can view proposed resolutions and add a note/comment, but cannot execute. Their note is visible to Exam Controller.

#### Tab: Action
Visible to CAO and Exam Controller only. Direct action controls:

| Field | Type | Required | Notes |
|---|---|---|---|
| Resolution Action | Select | ✅ | Reschedule Exam A · Reschedule Exam B · Merge · Ignore (soft only) |
| New Date (if rescheduling) | Date picker | Conditional | Conflict check runs again on new date |
| New Time (if rescheduling) | Time picker | Conditional | |
| Reason / Notes | Textarea | ✅ | Min 20 chars — explains decision |
| Notify Affected Branches | Checkbox | — | Default on |

[Apply Resolution] button — executes action, marks conflict Resolved, notifies branches if checked.

### 5.2 Modal: `ignore-confirm` — Ignore Conflict
- **Width:** 420px
- **Available for:** Soft conflicts only. Hard conflicts show this button as disabled with tooltip "Hard conflicts must be resolved — they cannot be ignored."
- **Content:** "Ignore conflict [CONF-ID]? This conflict will remain visible but will not block exam publication."
- **Fields:** Reason for ignoring (required, min 30 chars) · Reviewed and understood (checkbox, required)
- **Buttons:** [Confirm Ignore] (amber) + [Cancel]
- **On confirm:** Status → Ignored · Audit log entry · Conflict remains visible in filter (hidden from default Open view)

---

## 6. Charts

No dedicated charts section. The grouped list display and stats bar provide the operational view needed.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Conflict check complete (no conflicts) | "Conflict check complete. No conflicts found." | Success | 4s |
| Conflict check complete (conflicts found) | "Conflict check complete. [N] conflict(s) detected." | Warning | 6s |
| Conflict resolved | "Conflict [CONF-ID] resolved. Branches notified." | Success | 4s |
| Conflict ignored | "Conflict [CONF-ID] acknowledged and ignored." | Info | 4s |
| New conflict detected (real-time) | "New scheduling conflict detected for [Date] — [Branch]." | Warning | Manual (persist until viewed) |
| Export started | "Export preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open conflicts | "No exam conflicts" | "All scheduled exams are clear of conflicts. The calendar is conflict-free." | — |
| Filter returns empty | "No conflicts match your filters" | "Try removing some filters or check resolved/ignored conflicts." | [Clear All Filters] |
| No conflicts of a severity type | "No hard conflicts" or "No soft conflicts" | "No conflicts of this type currently detected." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + grouped conflict list (skeleton rows per group) |
| Filter/search | Inline skeleton rows |
| Manual conflict check trigger | Full stats bar + list refresh with spinner overlay |
| conflict-detail drawer open | Spinner + skeleton tabs |
| Resolution action submit | Spinner in Apply Resolution button |
| Ignore confirm | Spinner in confirm button |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Exam Controller G3 | Calendar Manager G3 | Academic Dir G3 | Stream Coords G3 |
|---|---|---|---|---|---|
| [Run Conflict Check] button | ✅ | ✅ | ❌ | ❌ | ❌ |
| [Export XLSX] button | ✅ | ✅ | ✅ | ❌ | ❌ |
| Reschedule Exam A/B actions | ✅ | ✅ | ❌ | ❌ | ❌ |
| Ignore action (soft conflicts) | ✅ | ✅ | ❌ | ❌ | ❌ |
| Action tab (drawer) | ✅ | ✅ | ❌ | ❌ | ❌ |
| Proposed Resolution tab (add note) | ✅ | ✅ | ✅ (note only) | ✅ (view) | ❌ |
| Affected Exams tab | ✅ | ✅ | ✅ | ✅ | ✅ (own stream) |
| Timeline tab | ✅ | ✅ | ✅ | ✅ | ✅ (own stream) |
| Stream filter (all streams) | ✅ | ✅ | ✅ | ✅ | ❌ (own only) |
| Conflict Detected At column | ✅ | ✅ | ✅ | ✅ | ✅ |
| Hard conflict banner (all acad pages) | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/exam-conflicts/` | JWT | List conflicts (filtered/sorted/paginated) |
| POST | `/api/v1/group/{group_id}/acad/exam-conflicts/check/` | JWT (CAO/Exam Ctrl) | Manually trigger conflict detection run |
| GET | `/api/v1/group/{group_id}/acad/exam-conflicts/{conf_id}/` | JWT | Conflict detail + timeline |
| POST | `/api/v1/group/{group_id}/acad/exam-conflicts/{conf_id}/resolve/` | JWT (CAO/Exam Ctrl) | Apply resolution action |
| POST | `/api/v1/group/{group_id}/acad/exam-conflicts/{conf_id}/ignore/` | JWT (CAO/Exam Ctrl) | Ignore soft conflict with reason |
| GET | `/api/v1/group/{group_id}/acad/exam-conflicts/stats/` | JWT | Summary stats bar data |
| GET | `/api/v1/group/{group_id}/acad/exam-conflicts/export/` | JWT | XLSX export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Conflict search | `input delay:300ms` | GET `.../exam-conflicts/?q=` | `#conflicts-list` | `innerHTML` |
| Filter apply | `click` | GET `.../exam-conflicts/?filters=` | `#conflicts-list` | `innerHTML` |
| Sort column | `click` | GET `.../exam-conflicts/?sort=&dir=` | `#conflicts-list` | `innerHTML` |
| Pagination | `click` | GET `.../exam-conflicts/?page=` | `#conflicts-list` | `innerHTML` |
| Detail drawer open | `click` | GET `.../exam-conflicts/{id}/` | `#drawer-body` | `innerHTML` |
| Manual check trigger | `click` | POST `.../exam-conflicts/check/` | `#conflicts-list, #stats-bar` | `innerHTML` (both) |
| Resolve action submit | `submit` | POST `.../exam-conflicts/{id}/resolve/` | `#conflict-row-{id}` | `outerHTML` |
| Ignore confirm | `click` | POST `.../exam-conflicts/{id}/ignore/` | `#conflict-row-{id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../exam-conflicts/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
