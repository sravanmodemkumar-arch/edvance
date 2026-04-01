# Page 13 — Branch Allocation Manager

- **URL:** `/group/adm/allocation/`
- **Template:** `portal_base.html`
- **Theme:** Light

---

## 1. Purpose

The Branch Allocation Manager is the operational stage at which a student's admission offer transitions into a concrete seat assignment. After a student has been counselled and an offer has been extended, they must be allocated to a specific branch, stream, section, and — if they require accommodation — a hostel type (AC or Non-AC, boys or girls). This allocation creates the binding record that forms the basis for fee invoicing, class list generation, hostel room assignment, and identity document issuance.

In large groups processing thousands of applications across dozens of branches simultaneously, allocation is the most operationally intensive step in the admissions cycle. The Coordinator must balance applicant preferences (first and second branch preference), real-time seat availability, hostel capacity, and policy constraints (e.g., NRI quota, scholarship seats) all at once. The Branch Capacity Snapshot (Section 5.2) is therefore displayed as a persistent reference panel alongside the allocation queue — so the Coordinator can check availability without navigating away from the record they are currently allocating.

Cross-branch allocations — where a student is placed in a branch other than their stated preference, or where a student enrolled in Branch A requests a move to Branch B — require Director approval. This ensures that capacity decisions that affect multiple branches are made with group-level awareness rather than unilaterally by a single branch's Coordinator. The cross-branch allocation request table (Section 5.5) tracks all such requests with their current status so neither the Director nor the Coordinator needs to rely on offline communication to track approvals. Upon allocation confirmation, the system can immediately trigger offer letter generation (integrated with Page 14).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | Full access + approve cross-branch allocations | Can override any allocation; approves all cross-branch requests |
| Group Admission Coordinator (Role 24) | G3 | Full allocation CRUD — all branches | Primary user of this page; initiates allocations, manages queue |
| Group Admission Counsellor (Role 25) | G3 | View only — own students' allocation status | Cannot initiate or modify allocations |
| CFO / Finance | G3+ | Read only — fee calculation reference | Sees allocation data to trigger fee schedule creation |
| CEO / Executive | G3+ | Read only | Capacity and fill rate oversight |

> **Enforcement:** All allocation write operations require `request.user.role in ['coordinator', 'admissions_director']`. Cross-branch approval endpoints enforce `request.user.role == 'admissions_director'` at the Django view level. Counsellor queryset is filtered to `allocation.student.assigned_counsellor = request.user`. Finance role sees allocation records via a read-only serializer that excludes contact/sensitive data.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Branch Allocation Manager
```

### 3.2 Page Header
- **Title:** Branch Allocation Manager
- **Subtitle:** Assign admitted students to branches, streams, and hostel — `{current_cycle_name}`
- **Right-side actions:** `[Auto-Allocate by Preference →]` (Coordinator only) · `[Export Pending →]` · `[Refresh ↺]`

### 3.3 Alert Banner

| Trigger | Message |
|---|---|
| Pending allocations > 30 | "{N} students are awaiting allocation. Clear the queue to avoid delays in offer letter generation." |
| Branches with < 10 available seats | "{N} branch(es) have fewer than 10 available seats. Adjust allocations or update the seat matrix." |
| Cross-branch requests awaiting Director approval | "{N} cross-branch allocation request(s) require your approval." (Director only) |
| Hostel seat allocation pending > 48 hours | "{N} hostel allocation(s) have been pending for over 48 hours." |
| Offer letters not generated post-allocation > 24 hours | "{N} allocation(s) completed over 24 hours ago without offer letters generated." |

---

## 4. KPI Summary Bar

> Auto-refreshes every 5 minutes via HTMX: `hx-get="/api/v1/group/{group_id}/adm/allocation/kpis/" hx-trigger="every 5m" hx-target="#allocation-kpi-bar" hx-swap="innerHTML"`

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Pending Allocations | Students in Offered stage not yet allocated | `Allocation.status='pending'` count | Amber if > 20; red if > 50; green if < 10 | Filters to pending allocation queue |
| Allocated Today | Allocations completed today | `allocated_at__date=today` | Green if > 0 | Filters completed allocations to today |
| Branches with < 10 Seats | Count of branch-stream combos with available < 10 | Computed from seat matrix | Red if > 0; green if 0 | Opens branch capacity snapshot (5.2) |
| Cross-branch Requests Pending | Pending cross-branch requests awaiting Director | `CrossBranchRequest.status='pending'` | Amber if > 0 | Filters to cross-branch table (5.5) |
| Hostel Allocation Pending | Admitted hostel-required students not yet assigned a hostel type | Computed | Amber if > 0 | Filters pending queue to hostel_required=True |
| Offer Letters Pending | Allocations completed but offer letter not yet generated | Computed | Amber if > 0 | Links to Page 14 (Offer Letter Manager) |

---

## 5. Sections

### 5.1 Pending Allocation Queue

**Display:** Sortable, server-side paginated table. 20 rows per page. Admitted students awaiting branch/hostel assignment. Checkbox column for bulk auto-allocation.

**Columns:**

| Column | Notes |
|---|---|
| ☐ Checkbox | Select for bulk auto-allocate |
| Student Name | Name |
| Stream | MPC / BiPC / MEC / CEC / General |
| Branch Preference 1 | Requested first preference |
| Branch Preference 2 | Requested second preference or "—" |
| Hostel Required | Yes / No badge |
| Student Type | Day Scholar / Hosteler AC / Hosteler Non-AC |
| Applied Date | `DD MMM YYYY` |
| Days Waiting | Integer; green ≤ 3; amber 4–7; red > 7 |
| [Allocate →] | Opens allocation-confirm-drawer for this student |

**Filters:** Stream, Hostel Type, Days Waiting (range), Branch Preference (select)

**Bulk Actions:** `[Auto-Allocate by Preference]` — runs allocation algorithm assigning students to their first available preference. `[Export]` — CSV of pending queue.

**HTMX Pattern:** Filter changes: `hx-get="/api/v1/group/{group_id}/adm/allocation/pending/?{filters}"` `hx-target="#pending-table-body"` `hx-swap="innerHTML"` `hx-trigger="change"`. Pagination: `hx-target="#pending-table-wrapper"`. `[Allocate →]` click: `hx-get="/api/v1/group/{group_id}/adm/allocation/{student_id}/confirm/"` `hx-target="#allocation-confirm-drawer"` `hx-swap="innerHTML"`.

**Empty State:** Green checkmark graphic. Heading: "All Students Allocated." Description: "The pending allocation queue is empty. All admitted students have been assigned to branches." CTA: —

---

### 5.2 Branch Capacity Snapshot

**Display:** Compact reference table displayed as a sticky side panel or collapsible section alongside the pending queue. Gives the Coordinator live seat availability while making allocation decisions without needing to navigate to the seat matrix page.

| Column | Notes |
|---|---|
| Branch | Branch short name |
| Stream | Stream name |
| Available Seats | `Total − Enrolled` |
| Hostel Available | Count of hostel seats remaining (AC + Non-AC combined) |
| Fill % | Progress bar; colour-coded |

**Filter:** Stream dropdown (to narrow which streams are shown).

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/allocation/capacity-snapshot/"` `hx-trigger="load, every 5m"` `hx-target="#capacity-snapshot-panel"` `hx-swap="innerHTML"`

**Empty State:** "Capacity data unavailable. Check the Seat Matrix configuration."

---

### 5.3 Allocation Decision (Inline)

This is the allocation workflow triggered from `[Allocate →]` in the pending queue. It opens the allocation-confirm-drawer (see Section 6.1) rather than rendering inline. The drawer presents all required fields: Branch selector (with real-time available seat count next to each option), Stream, Section, and Hostel details if applicable. Confirming allocation triggers offer letter generation prompt.

---

### 5.4 Completed Allocations Today

**Display:** Log table of all allocations completed today. Read-only. Sortable by time.

| Column | Notes |
|---|---|
| Student Name | Name |
| Branch | Allocated branch |
| Stream | Allocated stream |
| Hostel | Hostel type or "Day Scholar" |
| Allocated By | Coordinator name |
| Time | `HH:MM` |
| [View Offer →] | Links to offer letter in Page 14 (opens in new tab or drawer) |

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/allocation/completed/?date=today"` `hx-trigger="load, every 5m"` `hx-target="#completed-today-table"` `hx-swap="innerHTML"`

**Empty State:** "No allocations completed today yet."

---

### 5.5 Cross-Branch Allocation Requests

**Display:** Sortable table. Students who have been allocated to one branch and are requesting a transfer to another branch (pre-enrolment). Requires Director approval.

**Columns:**

| Column | Notes |
|---|---|
| Student Name | Name |
| Current Allocation | Branch + Stream |
| Requested Branch | Target branch |
| Student Type Change? | Yes/No — if hostel type or day/boarder changes |
| Reason | Brief reason (truncated; hover for full text) |
| Request Date | `DD MMM YYYY` |
| Days Pending | Integer; red > 3 |
| Status | Badge: Pending (amber) / Approved (green) / Rejected (red) |
| Actions | `[View →]` `[Approve →]` (Director) `[Reject →]` (Director) |

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/allocation/cross-branch/"` `hx-trigger="load, every 5m"` `hx-target="#cross-branch-table"` `hx-swap="innerHTML"`. Approve: `hx-patch` on `[Approve →]` button. `[View →]`: opens cross-branch-approval-drawer.

**Empty State:** "No cross-branch allocation requests pending."

---

## 6. Drawers & Modals

### 6.1 Allocation Confirm Drawer
- **Width:** 560px (right-side slide-in)
- **Trigger:** `[Allocate →]` in pending queue
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/allocation/{student_id}/confirm/`

**Content:**
- Student name, stream, and preferences displayed at top (read-only)
- Branch selector — dropdown with real-time available seat count per branch (updates on stream change)
- Stream (pre-selected; editable)
- Section (if applicable)
- Hostel required toggle — if yes:
  - Hostel type: AC / Non-AC
  - Room type: Single / Double / Dormitory
  - Gender wing: Boys / Girls
- Allocation notes (optional)
- `[Confirm Allocation → Generate Offer Letter]` — on submit, creates allocation record and redirects to offer letter generation
- `[Confirm Without Offer Letter]` — allocates but defers offer letter
- `[Cancel]`

---

### 6.2 Cross-Branch Approval Drawer
- **Width:** 480px
- **Trigger:** `[View →]` or `[Approve →]` in cross-branch table (Director only for approve)
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/allocation/cross-branch/{request_id}/review/`

**Content:** Student details, current allocation, requested branch with available seat count, student type change details, reason for request, capacity impact summary (source branch +1 seat, target branch −1 seat preview), Director decision form (Approve / Reject + mandatory notes), `[Submit Decision]`.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Allocation confirmed | "{Student name} allocated to {Branch} — {Stream}. Offer letter generation triggered." | Success | 5s |
| Allocation confirmed (no offer letter) | "{Student name} allocated to {Branch} — {Stream}." | Success | 4s |
| Bulk auto-allocation completed | "{N} students auto-allocated. {M} could not be allocated — preferences unavailable." | Info | 6s |
| Cross-branch request approved | "Cross-branch transfer approved for {Student name}: {Old Branch} → {New Branch}." | Success | 5s |
| Cross-branch request rejected | "Cross-branch request rejected for {Student name}. Applicant notified." | Warning | 4s |
| Allocation failed (no available seats) | "Cannot allocate — {Branch} {Stream} has no available seats." | Error | 6s |
| Export started | "Export is being prepared. Download will start shortly." | Info | 5s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No pending allocations | Green checkmark graphic | "Queue is Clear" | "All admitted students have been assigned to branches." | — |
| Filter returns no results | Search-miss graphic | "No Matching Records" | "No pending allocations match the selected filters." | `[Clear Filters]` |
| No completed allocations today | Calendar graphic | "No Allocations Today Yet" | "Completed allocations will appear here as they are processed." | — |
| No cross-branch requests | Arrows graphic | "No Cross-Branch Requests" | "No cross-branch allocation requests are currently pending." | — |
| Branch capacity snapshot unavailable | Grid graphic | "Capacity Data Unavailable" | "Configure the seat matrix to view branch capacity." | `[Go to Seat Matrix →]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Full-page skeleton (pending table + KPI bar + capacity panel shimmer) |
| KPI bar auto-refresh | Inline spinner on each KPI card |
| Filter change (pending table) | Table body skeleton (5-row shimmer) |
| Pagination click | Table body skeleton |
| Capacity snapshot refresh | Panel skeleton |
| Completed allocations today refresh | Table body skeleton |
| Cross-branch table load/refresh | Table body skeleton |
| Allocation confirm drawer open | Drawer content skeleton |
| Branch selector real-time update (on stream change) | Inline spinner next to branch dropdown |
| Bulk auto-allocate action | Full-table overlay spinner "Running auto-allocation…" |
| Cross-branch approval drawer open | Drawer content skeleton |
| Export generation | Button spinner; button disabled |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions are made server-side in the Django template. No client-side JS role checks.

| Element | Dir (23) | Coord (24) | Counsellor (25) | CFO | CEO |
|---|---|---|---|---|---|
| Pending Allocation Queue | Visible | Visible | Hidden | Hidden | Hidden |
| [Allocate →] action | Visible | Visible | Hidden | Hidden | Hidden |
| [Auto-Allocate by Preference] button | Hidden | Visible | Hidden | Hidden | Hidden |
| Bulk checkbox + bulk actions | Visible | Visible | Hidden | Hidden | Hidden |
| Branch Capacity Snapshot | Visible | Visible | Hidden | Visible | Visible |
| Completed Allocations Today | Visible | Visible | Own students only | Visible (read) | Visible |
| Cross-Branch Requests table | Visible | Visible | Hidden | Hidden | Hidden |
| [Approve →] / [Reject →] in cross-branch | Visible | Hidden | Hidden | Hidden | Hidden |
| Allocation Confirm Drawer — full controls | Visible | Visible | Hidden | Hidden | Hidden |
| Cross-Branch Approval Drawer — decision form | Visible | Hidden | Hidden | Hidden | Hidden |
| [Export Pending →] button | Visible | Visible | Hidden | Visible | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/allocation/pending/` | JWT G3+ | List students pending allocation with filters |
| GET | `/api/v1/group/{group_id}/adm/allocation/kpis/` | JWT G3+ | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/allocation/capacity-snapshot/` | JWT G3+ | Live seat availability by branch+stream |
| GET | `/api/v1/group/{group_id}/adm/allocation/{student_id}/confirm/` | JWT G3 | Allocation confirm form fragment |
| POST | `/api/v1/group/{group_id}/adm/allocation/{student_id}/confirm/` | JWT G3 | Confirm and save allocation |
| POST | `/api/v1/group/{group_id}/adm/allocation/bulk/auto-allocate/` | JWT G3 | Bulk auto-allocate by preference |
| GET | `/api/v1/group/{group_id}/adm/allocation/completed/` | JWT G3+ | List completed allocations (filterable by date) |
| GET | `/api/v1/group/{group_id}/adm/allocation/cross-branch/` | JWT G3+ | List cross-branch allocation requests |
| GET | `/api/v1/group/{group_id}/adm/allocation/cross-branch/{request_id}/review/` | JWT G3 | Cross-branch review form |
| PATCH | `/api/v1/group/{group_id}/adm/allocation/cross-branch/{request_id}/` | JWT G3 (Director) | Approve or reject cross-branch request |
| POST | `/api/v1/group/{group_id}/adm/allocation/cross-branch/` | JWT G3 | Create new cross-branch request (Coordinator) |
| GET | `/api/v1/group/{group_id}/adm/allocation/export/` | JWT G3+ | Export pending allocations as CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `/api/v1/group/{group_id}/adm/allocation/kpis/` | `#allocation-kpi-bar` | `innerHTML` |
| Pending queue filter change | `change` | GET `/api/v1/group/{group_id}/adm/allocation/pending/?{filters}` | `#pending-table-body` | `innerHTML` |
| Pending queue pagination click | `click` | GET `/api/v1/group/{group_id}/adm/allocation/pending/?page={n}&{filters}` | `#pending-table-wrapper` | `innerHTML` |
| Pending queue sort click | `click` | GET `/api/v1/group/{group_id}/adm/allocation/pending/?sort={col}&order={dir}` | `#pending-table-body` | `innerHTML` |
| [Allocate →] button click | `click` | GET `/api/v1/group/{group_id}/adm/allocation/{student_id}/confirm/` | `#allocation-confirm-drawer` | `innerHTML` |
| Stream change in confirm drawer (update branch seats) | `change` | GET `/api/v1/group/{group_id}/adm/allocation/capacity-snapshot/?stream={id}` | `#branch-selector-options` | `innerHTML` |
| Allocation confirm form submit | `submit` | POST `/api/v1/group/{group_id}/adm/allocation/{student_id}/confirm/` | `#pending-table-body` | `innerHTML` |
| Bulk auto-allocate submit | `click` | POST `/api/v1/group/{group_id}/adm/allocation/bulk/auto-allocate/` | `#pending-table-wrapper` | `innerHTML` |
| Capacity snapshot load/refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/allocation/capacity-snapshot/` | `#capacity-snapshot-panel` | `innerHTML` |
| Completed today table load/refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/allocation/completed/?date=today` | `#completed-today-table` | `innerHTML` |
| Cross-branch table load/refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/allocation/cross-branch/` | `#cross-branch-table` | `innerHTML` |
| [View →] / [Approve →] cross-branch | `click` | GET `/api/v1/group/{group_id}/adm/allocation/cross-branch/{request_id}/review/` | `#cross-branch-approval-drawer` | `innerHTML` |
| Cross-branch decision submit | `submit` | PATCH `/api/v1/group/{group_id}/adm/allocation/cross-branch/{request_id}/` | `#cross-branch-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
