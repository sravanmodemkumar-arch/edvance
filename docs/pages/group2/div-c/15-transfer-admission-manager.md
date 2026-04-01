# Page 15 — Transfer Admission Manager

- **URL:** `/group/adm/transfers/`
- **Template:** `portal_base.html`
- **Theme:** Light

---

## 1. Purpose

The Transfer Admission Manager handles the sensitive and operationally complex process of mid-year inter-branch student transfers. A student enrolled in Branch A — with a fee structure, hostel arrangement, and class schedule established — requests a move to Branch B. This could arise because a family has relocated to another city, the student or parents prefer a different hostel environment, the stream they want is unavailable at their current branch, or exceptional personal circumstances have made the current placement untenable. Whatever the reason, a transfer is not merely a data change — it triggers a chain of operational adjustments across two branches and the finance function.

The source branch must formally confirm the release of the seat, the target branch must have verified capacity in the right stream and student type category, any fee differential (e.g., if Branch B has higher tuition or different hostel charges) must be calculated, collected, or waived, and the physical movement of the student's records must be coordinated. Without a formal workflow managing all of this, transfers devolve into phone calls, WhatsApp messages, and ad-hoc approvals that create confusion about which branch's records are authoritative. This page imposes structure and accountability on the process.

Only the Director can approve cross-branch transfers — this ensures that no single branch Coordinator can unilaterally accept a student from another branch without group-level sign-off. The Transfer Approval Flow (Section 5.2) makes every step of the approval chain visible, so the Director, both branch teams, and the finance team can see exactly where a request stands. The Fee Differential Manager (Section 5.5) ensures that every financial implication of a transfer is accounted for and resolved before the transfer is marked complete, preventing situations where a student has physically moved but fee records are inconsistent.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | Full access — approve / reject / override | Only role that can approve transfers |
| Group Admission Coordinator (Role 24) | G3 | Create requests + view all + track status | Cannot approve transfers |
| Group Admission Counsellor (Role 25) | G3 | View own students' transfer requests only | Read-only |
| CFO / Finance | G3+ | View only — Fee Differential section (5.5) | Sees fee impact and payment status; can initiate `[Collect →]` and `[Waive →]` actions |
| CEO / Executive | G3+ | Read only | Full overview |

> **Enforcement:** Transfer approval endpoints enforce `request.user.role == 'admissions_director'` at the Django view layer with HTTP 403 on violation. The `[Collect →]` and `[Waive →]` fee actions enforce `request.user.role in ['cfo', 'finance']`. Counsellor querysets filter to `transfer.student.assigned_counsellor = request.user`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Transfer Admission Manager
```

### 3.2 Page Header
- **Title:** Transfer Admission Manager
- **Subtitle:** Mid-year inter-branch student transfers — `{current_cycle_name}`
- **Right-side actions:** `[+ New Transfer Request]` (Coordinator) · `[Export →]` (Coordinator / Director) · `[Refresh ↺]`

### 3.3 Alert Banner

| Trigger | Message |
|---|---|
| Transfer requests pending Director approval > 0 | "{N} transfer request(s) awaiting your approval." (Director only) |
| Transfer requests older than 7 days without action | "{N} transfer request(s) have been pending for over 7 days without action." |
| Fee differential unresolved for approved transfers | "{N} approved transfer(s) have unresolved fee differentials. Finance action required." |
| Seat adjustment pending after approval | "{N} seat count adjustment(s) pending in the seat matrix following recent transfer approvals." |
| Transfers approved this term > configurable threshold | "{N} transfers approved this term — above the normal range. Review for patterns." |

---

## 4. KPI Summary Bar

> Auto-refreshes every 5 minutes via HTMX: `hx-get="/api/v1/group/{group_id}/adm/transfers/kpis/" hx-trigger="every 5m" hx-target="#transfers-kpi-bar" hx-swap="innerHTML"`

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Active Transfer Requests | Count with status Pending or In Progress | `TransferRequest.status__in=['pending','in_progress']` | Amber if > 5; red if > 15; green if 0 | Filters request table to active |
| Transfers Approved (this term) | Approved transfers in current academic term | `status='approved', approved_at >= term_start` | Neutral (blue) | Filters history table to this term |
| Pending Director Approval | Requests at Director Approval step | Workflow step filter | Red if > 0; green if 0 | Filters request table to step=Director Approval |
| Branches with Most Inflow | Top 3 branches by net incoming transfers | Computed | Neutral (indigo) | Opens transfer history with branch filter |
| Seat Adjustments Pending | Transfer-approved records where seat matrix not yet updated | Computed | Amber if > 0 | Opens seat impact summary (5.3) |
| Requests > 7 Days Without Action | Count of old unresolved requests | `pending_since < today − 7 days` | Red if > 0; green if 0 | Filters to overdue requests |

---

## 5. Sections

### 5.1 Transfer Request Table

**Display:** Sortable, server-side paginated table. 20 rows per page.

**Columns:**

| Column | Notes |
|---|---|
| Request ID | Clickable — opens transfer-review-drawer |
| Student Name | Name |
| Current Branch | Source branch |
| Current Stream | Source stream |
| Target Branch | Destination branch |
| Target Stream | Destination stream |
| Reason | Truncated; hover for full |
| Student Type Change? | Yes/No — e.g., Day Scholar → Hosteler |
| Request Date | `DD MMM YYYY` |
| Days Pending | Integer; amber 4–7; red > 7 |
| Status | Badge: Pending (amber) / In Progress (blue) / Approved (green) / Rejected (red) / Completed (grey) |
| Actions | `[View →]` · `[Approve →]` (Director, on eligible rows) · `[Reject →]` (Director) |

**Filters:** Status, Current Branch, Target Branch, Stream, Days Pending range

**HTMX Pattern:** Filter changes: `hx-get="/api/v1/group/{group_id}/adm/transfers/?{filters}"` `hx-target="#transfer-table-body"` `hx-swap="innerHTML"` `hx-trigger="change"`. Pagination: `hx-target="#transfer-table-wrapper"`. `[View →]` click: `hx-get="/api/v1/group/{group_id}/adm/transfers/{request_id}/review/"` `hx-target="#transfer-review-drawer"` `hx-swap="innerHTML"`.

**Empty State:** "No transfer requests found for the selected filters."

---

### 5.2 Transfer Approval Flow

**Display:** For each active transfer request, a horizontal timeline card shows the current step in the approval chain. Displayed as a collapsible section with one timeline per active request (collapsed to a summary list when more than 5 are active).

**Steps:**
1. Requested (date, requested by)
2. Source Branch Confirmed (date, confirmed by — or pending)
3. Target Branch Capacity Check (date, confirmed by — or pending)
4. Fee Adjustment Calculated (date — or pending)
5. Director Approval (date, approved by — or pending)
6. Transfer Complete (date — or pending)

Each step shows a tick (completed), spinner (in progress), or circle (upcoming). Clicking the card opens the transfer-review-drawer.

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/transfers/active-flows/"` `hx-trigger="load, every 5m"` `hx-target="#transfer-flow-panel"` `hx-swap="innerHTML"`

**Empty State:** "No active transfer approvals in progress."

---

### 5.3 Seat Impact Summary

**Display:** Live-updating table showing the net seat impact of recently approved transfers that have not yet been reflected in the seat matrix.

| Column | Notes |
|---|---|
| Branch | Branch name |
| Stream | Stream |
| Direction | Source (+1 seat) or Target (−1 seat) |
| Transfer ID | Linked transfer request |
| Net Change | +1 or −1 |
| Status | Applied to Matrix (green) / Pending (amber) |

`[Apply to Matrix →]` button (Coordinator/Director) — triggers the seat matrix update for all pending adjustments.

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/transfers/seat-impact/"` `hx-trigger="load, every 5m"` `hx-target="#seat-impact-table"` `hx-swap="innerHTML"`

**Empty State:** "All seat adjustments from approved transfers have been applied to the seat matrix."

---

### 5.4 Transfer History

**Display:** Paginated table of completed transfers (status = Completed or Rejected). 20 rows per page.

| Column | Notes |
|---|---|
| Student Name | Name |
| From Branch | Source |
| To Branch | Destination |
| Transfer Date | Date of completion |
| Reason | Reason category |
| Approved By | Director name |
| Status | Completed (green) / Rejected (red) |

**Filters:** Current Branch (source), Target Branch, Date range, Status

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/transfers/history/?{filters}"` `hx-target="#transfer-history-table-body"` `hx-swap="innerHTML"` `hx-trigger="change"` on filters. Pagination: `hx-target="#transfer-history-wrapper"`.

**Empty State:** "No completed transfers this term."

---

### 5.5 Fee Differential Manager

**Display:** Table of approved transfers where the fee at the target branch differs from the fee at the source branch.

| Column | Notes |
|---|---|
| Student Name | Name |
| Old Fee (per term) | Fee at source branch |
| New Fee (per term) | Fee at target branch |
| Differential | Old − New (positive = refund due; negative = additional payment due) |
| Payment Status | Paid (green) / Pending (amber) / Waived (grey) / Refund Due (blue) |
| Actions | `[Collect →]` (Finance — triggers fee collection record) · `[Waive →]` (Finance — marks as waived with reason) · `[View →]` |

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/transfers/fee-differential/"` `hx-trigger="load, every 5m"` `hx-target="#fee-differential-table"` `hx-swap="innerHTML"`. `[Collect →]` and `[Waive →]` trigger modals via HTMX.

**Empty State:** "No fee differentials pending. All transfers have matching or resolved fee structures."

---

## 6. Drawers & Modals

### 6.1 Transfer Review Drawer
- **Width:** 640px (right-side slide-in)
- **Trigger:** `[View →]` in table, or approval flow card click
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/transfers/{request_id}/review/`

**Tabs:**

| Tab | Content |
|---|---|
| Student Profile | Name, class, stream, current enrolment details, contact info, guardian details |
| Current Enrollment | Branch, stream, section, hostel details, fee schedule, enrolment date |
| Transfer Request | Requested target branch/stream, reason category, detailed reason, student type change, supporting documents |
| Branch Capacity | Target branch available seats and hostel availability (real-time from seat matrix) |
| Fee Impact | Old fee vs new fee, differential, payment options |
| Decision | Director approval form: Approve / Reject, notes (required on rejection), effective date; visible only to Director |

---

### 6.2 Fee Differential Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Collect →]` or `[Waive →]` in fee differential table
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/transfers/{transfer_id}/fee-action/`

**Collect fields:** Amount to collect, Payment mode (Cash/Online/Cheque), Transaction reference, Notes.
**Waive fields:** Reason for waiver (dropdown: Director Discretion / Scholarship / Hardship / Other), Approval note.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Transfer request created | "Transfer request {ID} created for {Student name}." | Success | 4s |
| Transfer approved | "Transfer approved: {Student name} → {Target Branch}. Seat matrix update pending." | Success | 5s |
| Transfer rejected | "Transfer rejected for {Student name}. Student notified." | Warning | 4s |
| Seat matrix updated | "Seat adjustments from transfer {ID} applied to seat matrix." | Success | 4s |
| Fee collected | "Fee differential of ₹{amount} collected for {Student name}." | Success | 4s |
| Fee waived | "Fee differential waived for {Student name}. Reason: {reason}." | Info | 5s |
| Export started | "Export is being prepared. Download will start shortly." | Info | 5s |
| Transfer completion failed | "Cannot complete transfer — target branch capacity check failed." | Error | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No active transfer requests | Arrows graphic | "No Active Transfer Requests" | "No inter-branch transfer requests are currently pending." | `[+ New Transfer Request]` |
| Filter returns no rows | Search-miss graphic | "No Matching Requests" | "No transfer requests match the selected filters." | `[Clear Filters]` |
| No approval flows active | Timeline graphic | "No Active Approval Flows" | "No transfers are currently moving through the approval process." | — |
| No seat impact pending | Grid graphic | "No Pending Seat Adjustments" | "All approved transfers have been reflected in the seat matrix." | — |
| No transfer history | Archive graphic | "No Transfer History" | "Completed and rejected transfers will appear here." | — |
| No fee differentials | Finance graphic | "No Fee Differentials" | "No approved transfers have outstanding fee differences." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Full-page skeleton (table + KPI bar + flow panel shimmer) |
| KPI bar auto-refresh | Inline spinner on each KPI card |
| Filter change (transfer table) | Table body skeleton (5-row shimmer) |
| Pagination click | Table body skeleton |
| Approval flow panel refresh | Panel skeleton |
| Seat impact table refresh | Table body skeleton |
| Transfer history filter change | Table body skeleton |
| Fee differential table refresh | Table body skeleton |
| Transfer review drawer open | Drawer content skeleton |
| Drawer tab switch | Tab content spinner |
| Fee differential modal open | Modal skeleton |
| Approve / Reject action | Button spinner + row update |
| Seat matrix apply | Button spinner "Applying adjustments…" |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions are made server-side in the Django template. No client-side JS role checks.

| Element | Dir (23) | Coord (24) | Counsellor (25) | CFO | CEO |
|---|---|---|---|---|---|
| [+ New Transfer Request] | Hidden | Visible | Hidden | Hidden | Hidden |
| [Export →] button | Visible | Visible | Hidden | Visible | Hidden |
| Transfer Request Table — all branches | Visible | Visible | Own students (read) | Hidden | Visible |
| [Approve →] / [Reject →] actions | Visible | Hidden | Hidden | Hidden | Hidden |
| Decision tab in review drawer | Visible | Hidden | Hidden | Hidden | Hidden |
| Transfer Approval Flow | Visible | Visible | Hidden | Hidden | Hidden |
| Seat Impact Summary | Visible | Visible | Hidden | Visible | Hidden |
| [Apply to Matrix →] button | Visible | Visible | Hidden | Hidden | Hidden |
| Transfer History | Visible | Visible | Own students | Visible | Visible |
| Fee Differential Manager | Visible | Visible | Hidden | Visible (full — collect/waive) | Visible (read) |
| [Collect →] in fee differential | Hidden | Hidden | Hidden | Visible | Hidden |
| [Waive →] in fee differential | Hidden | Hidden | Hidden | Visible | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/transfers/` | JWT G3+ | List transfer requests with filters |
| POST | `/api/v1/group/{group_id}/adm/transfers/` | JWT G3 | Create new transfer request |
| GET | `/api/v1/group/{group_id}/adm/transfers/kpis/` | JWT G3+ | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/transfers/active-flows/` | JWT G3+ | Active transfer approval flows |
| GET | `/api/v1/group/{group_id}/adm/transfers/seat-impact/` | JWT G3+ | Pending seat impact from approved transfers |
| POST | `/api/v1/group/{group_id}/adm/transfers/seat-impact/apply/` | JWT G3 | Apply seat adjustments to seat matrix |
| GET | `/api/v1/group/{group_id}/adm/transfers/history/` | JWT G3+ | Completed transfer history |
| GET | `/api/v1/group/{group_id}/adm/transfers/fee-differential/` | JWT G3+ | Fee differentials for approved transfers |
| POST | `/api/v1/group/{group_id}/adm/transfers/{transfer_id}/fee-action/` | JWT G3 (Finance) | Collect or waive fee differential |
| GET | `/api/v1/group/{group_id}/adm/transfers/{request_id}/review/` | JWT G3+ | Transfer review form/detail |
| PATCH | `/api/v1/group/{group_id}/adm/transfers/{request_id}/approve/` | JWT G3 (Director) | Approve transfer request |
| PATCH | `/api/v1/group/{group_id}/adm/transfers/{request_id}/reject/` | JWT G3 (Director) | Reject transfer request |
| GET | `/api/v1/group/{group_id}/adm/transfers/export/` | JWT G3+ | Export transfer requests as CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `/api/v1/group/{group_id}/adm/transfers/kpis/` | `#transfers-kpi-bar` | `innerHTML` |
| Transfer table filter change | `change` | GET `/api/v1/group/{group_id}/adm/transfers/?{filters}` | `#transfer-table-body` | `innerHTML` |
| Transfer table pagination click | `click` | GET `/api/v1/group/{group_id}/adm/transfers/?page={n}&{filters}` | `#transfer-table-wrapper` | `innerHTML` |
| Transfer table sort click | `click` | GET `/api/v1/group/{group_id}/adm/transfers/?sort={col}&order={dir}` | `#transfer-table-body` | `innerHTML` |
| [View →] row click | `click` | GET `/api/v1/group/{group_id}/adm/transfers/{request_id}/review/` | `#transfer-review-drawer` | `innerHTML` |
| Drawer tab switch | `click` | GET `/api/v1/group/{group_id}/adm/transfers/{request_id}/review/?tab={tab}` | `#drawer-tab-content` | `innerHTML` |
| [Approve →] quick action | `click` | PATCH `/api/v1/group/{group_id}/adm/transfers/{request_id}/approve/` | `#transfer-table-body` | `innerHTML` |
| Approval flow panel refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/transfers/active-flows/` | `#transfer-flow-panel` | `innerHTML` |
| Seat impact table refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/transfers/seat-impact/` | `#seat-impact-table` | `innerHTML` |
| [Apply to Matrix →] click | `click` | POST `/api/v1/group/{group_id}/adm/transfers/seat-impact/apply/` | `#seat-impact-table` | `innerHTML` |
| Transfer history filter change | `change` | GET `/api/v1/group/{group_id}/adm/transfers/history/?{filters}` | `#transfer-history-table-body` | `innerHTML` |
| Transfer history pagination | `click` | GET `/api/v1/group/{group_id}/adm/transfers/history/?page={n}&{filters}` | `#transfer-history-wrapper` | `innerHTML` |
| Fee differential table refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/transfers/fee-differential/` | `#fee-differential-table` | `innerHTML` |
| [Collect →] / [Waive →] click | `click` | GET `/api/v1/group/{group_id}/adm/transfers/{transfer_id}/fee-action/` | `#fee-action-modal` | `innerHTML` |
| Fee action form submit | `submit` | POST `/api/v1/group/{group_id}/adm/transfers/{transfer_id}/fee-action/` | `#fee-differential-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
