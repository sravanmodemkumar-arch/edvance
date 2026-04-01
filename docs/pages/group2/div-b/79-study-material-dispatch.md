# 79 — Study Material Dispatch Tracker

> **URL:** `/group/acad/material-dispatch/`
> **File:** `79-study-material-dispatch.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Curriculum Coordinator G2 (full — create dispatch) · Academic Director G3 (view) · CAO G4 (view)

---

## 1. Purpose

Tracks the dispatch and branch receipt acknowledgement of physical printed study materials:
workbooks, question sheets, reference modules, lab manuals, and practice papers.

**Why separate from Content Library (Page 17)?** Content Library manages digital files (PDFs, videos).
This page manages **physical copies** — printed, dispatched in boxes, received by branches.

Gaps this closes:
- No visibility into whether Branch X has received the Chemistry workbook
- No confirmation that printed papers were delivered before exam day
- No reorder request tracking when branches need extra copies

---

## 2. Role Access

| Role | Level | Can Create Dispatch | Can Track | Can View | Notes |
|---|---|---|---|---|---|
| Curriculum Coordinator | G2 | ✅ | ✅ | ✅ | Primary owner |
| Academic Director | G3 | ❌ | ❌ | ✅ | View only |
| CAO | G4 | ❌ | ❌ | ✅ | View only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Study Material Dispatch Tracker
```

### 3.2 Page Header
```
Study Material Dispatch Tracker                      [+ New Dispatch]  [Export ↓]
AY 2025–26 · Term [N] · [M] Dispatches · [P] Pending Acknowledgement
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Dispatches (term) | 38 |
| Fully Acknowledged | 29 |
| Pending Acknowledgement | 7 |
| Overdue Acknowledgement (>7 days) | 2 |
| Total Copies Dispatched | 24,830 |
| Reorder Requests Open | 4 |

---

## 4. Main Table

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Material Name | Text + link | ✅ | |
| Type | Badge | ✅ | Workbook · Question Sheet · Reference · Lab Manual · Practice Paper · Other |
| Term | Badge | ✅ | |
| Dispatch Date | Date | ✅ | |
| Total Copies | Number | ✅ | |
| Branches | Number | ✅ | Number of branches receiving |
| Acknowledged | Number | ✅ | Branches acknowledged / total |
| Outstanding | Number | ✅ | Branches not yet acknowledged |
| Status | Badge | ✅ | Dispatched · Partially Acknowledged · Fully Acknowledged · Overdue |
| Actions | — | ❌ | View · Send Reminder |

### 4.1 Filters

| Filter | Type | Options |
|---|---|---|
| Term | Multi-select | Term 1 / 2 / 3 |
| Material Type | Multi-select | Workbook · Question Sheet · Reference · Lab Manual · Practice Paper |
| Status | Multi-select | Dispatched · Partially · Fully · Overdue |
| Branch | Multi-select | Branch names |

### 4.2 Search
- Full-text: material name
- 300ms debounce

---

## 5. Drawers

### 5.1 Drawer: `dispatch-create` — New Dispatch
- **Trigger:** [+ New Dispatch] header button
- **Width:** 640px

| Field | Type | Required | Validation |
|---|---|---|---|
| Material Name | Text | ✅ | |
| Type | Select | ✅ | |
| Term | Select | ✅ | |
| Linked Digital Content | Select | ❌ | Link to Content Library (Page 17) — optional |
| Dispatch Date | Date | ✅ | |
| Vendor / Printer | Text | ❌ | |
| Branch Quantity Table | Per branch: Branch → Quantity | ✅ | All branches must have quantity |
| Notes | Text | ❌ | e.g. "Distribute before April 5th" |

**Branch Quantity Table:**

| Branch | Quantity |
|---|---|
| [Branch A] | 480 |
| [Branch B] | 320 |
| ... | ... |

- Auto-fill by student count: [Distribute by Enrollment] button
- Total quantity auto-calculated

### 5.2 Drawer: `dispatch-detail` — Dispatch Detail
- **Trigger:** View row action
- **Width:** 640px

**Tab: Overview**
- Material · Type · Term · Dispatch Date · Vendor · Notes
- Total copies · Branches · Acknowledged % gauge

**Tab: Branch Acknowledgements**

| Column | Type |
|---|---|
| Branch | Text |
| Quantity Sent | Number |
| Acknowledged | Badge (Yes / Pending / Overdue) |
| Acknowledged Date | Date |
| Acknowledged By | Text (Principal name) |
| Proof | Link (uploaded photo/scan, if provided) |

- **[Send Reminder]** per branch or bulk to pending branches
- **[Mark Acknowledged]** — manual override if branch confirms by phone

**Tab: Reorder Requests**
- Branches that have requested additional copies
- Request: Branch · Current Qty · Requested Additional Qty · Reason · Status

---

## 6. Branch Acknowledgement (Branch Portal Side)

Branch Principals receive notification: "Study material '[Name]' dispatched. Please acknowledge receipt."
- Branch portal: Acknowledge button → optional quantity check · optional photo upload
- Acknowledgement date + username recorded automatically

---

## 7. Reorder Request

Branch staff can request additional copies via their branch portal.
Group-side Curriculum Coordinator sees all open reorder requests in **Tab: Reorder Requests**.

Reorder workflow:
1. Branch submits reorder request
2. Curriculum Coordinator reviews and approves
3. Additional copies dispatched → new dispatch record created (linked to original)

---

## 8. Alert Logic

| Condition | Alert | Recipient |
|---|---|---|
| Branch not acknowledged within 7 days | In-app badge | Curriculum Coordinator |
| Dispatch overdue > 7 days with no acknowledgement | Red alert | Curriculum Coordinator |
| Reorder request submitted | Notification | Curriculum Coordinator |

---

## 9. Charts

### 9.1 Dispatch Completion % by Branch (Bar)
- **Data:** % of dispatches acknowledged per branch (sorted ascending)
- **Color:** Green ≥ 90% · Amber 70–89% · Red < 70%
- **Export:** PNG

### 9.2 Outstanding Acknowledgements (Bar)
- **Data:** Dispatches with pending acknowledgement — sorted by overdue days
- **Export:** PNG

---

## 10. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Dispatch created | "Dispatch created for [N] branches. [M] total copies." | Success | 4s |
| Reminder sent | "Acknowledgement reminder sent to [N] branches." | Info | 4s |
| Acknowledgement recorded | "Branch [Name] acknowledged receipt of '[Material]'." | Success | 3s |
| Reorder approved | "Reorder approved for [Branch]. Dispatch in progress." | Success | 4s |
| Overdue alert | "[N] dispatches overdue for acknowledgement." | Warning | 6s |

---

## 11. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No dispatches | "No dispatches yet" | "Create the first study material dispatch." | [+ New Dispatch] |
| All acknowledged | "All dispatches acknowledged" | "All branches have acknowledged receipt." | — |
| No reorder requests | "No reorder requests" | "Branches have not requested additional copies." | — |

---

## 12. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton: stats bar + 6 table rows |
| Filter/search | Inline skeleton |
| Detail drawer | Spinner + skeleton tabs |
| Reminder send | Spinner on reminder button |

---

## 13. Role-Based UI Visibility

| Element | Curr Coord G2 | Academic Dir G3 | CAO G4 |
|---|---|---|---|
| [+ New Dispatch] | ✅ | ❌ | ❌ |
| [Send Reminder] | ✅ | ❌ | ❌ |
| [Mark Acknowledged] (override) | ✅ | ❌ | ❌ |
| [Approve Reorder] | ✅ | ❌ | ❌ |
| View all dispatches | ✅ | ✅ | ✅ |
| Charts | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/material-dispatch/` | JWT (G2+) | Dispatch list |
| POST | `/api/v1/group/{id}/acad/material-dispatch/` | JWT (G2) | Create dispatch |
| GET | `/api/v1/group/{id}/acad/material-dispatch/{did}/` | JWT (G2+) | Dispatch detail |
| GET | `/api/v1/group/{id}/acad/material-dispatch/{did}/acknowledgements/` | JWT (G2+) | Branch ack list |
| POST | `/api/v1/group/{id}/acad/material-dispatch/{did}/acknowledge/{bid}/` | JWT (G2) | Manual acknowledge |
| POST | `/api/v1/group/{id}/acad/material-dispatch/{did}/send-reminder/` | JWT (G2) | Send reminder |
| GET | `/api/v1/group/{id}/acad/material-dispatch/reorders/` | JWT (G2+) | Reorder requests |
| PUT | `/api/v1/group/{id}/acad/material-dispatch/reorders/{rid}/approve/` | JWT (G2) | Approve reorder |
| GET | `/api/v1/group/{id}/acad/material-dispatch/stats/` | JWT (G2+) | Summary stats |
| GET | `/api/v1/group/{id}/acad/material-dispatch/export/?format=csv` | JWT (G2+) | Export |

---

## 15. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../material-dispatch/?q=` | `#dispatch-table-body` | `innerHTML` |
| Filter | `click` | GET `.../material-dispatch/?filters=` | `#dispatch-section` | `innerHTML` |
| Pagination | `click` | GET `.../material-dispatch/?page=` | `#dispatch-section` | `innerHTML` |
| Open detail drawer | `click` | GET `.../material-dispatch/{id}/` | `#drawer-body` | `innerHTML` |
| Create dispatch submit | `submit` | POST `.../material-dispatch/` | `#drawer-body` | `innerHTML` |
| Acknowledgements tab | `click` | GET `.../material-dispatch/{id}/acknowledgements/` | `#ack-tab-body` | `innerHTML` |
| Send reminder | `click` | POST `.../send-reminder/` | `#reminder-btn` | `outerHTML` |
| Manual acknowledge | `click` | POST `.../acknowledge/{bid}/` | `#ack-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
