# 23 — Scholarship Approval Workflow

**URL:** `/group/adm/scholarship-approvals/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions · Scholarship Section

---

## 1. Purpose

The Scholarship Approval Workflow page is the decision-making hub for all scholarship applications and recommendations flowing into the group's scholarship program. Recommendations arrive from three distinct sources: counsellors who recommend students during individual counselling sessions; the automated pipeline from published scholarship exam results (where candidates meeting a scheme's score threshold are auto-generated as recommendations); and branch principals or academic heads who nominate deserving students directly. All three sources converge in a single approval queue that the Group Scholarship Manager reviews and acts upon.

The approval process is deliberately differentiated based on scholarship basis. Merit scholarships backed by exam scores are largely data-driven — the Manager can see the exact score and rank, verify it meets the scheme threshold, and approve in a single click. Need-based scholarships require document review — income certificates, family size declarations, BPL card copies — and the Manager must review uploaded documents before approving. For incomplete applications, a "Request Documents" action sends an automated notification to the branch asking them to collect and upload the missing paperwork within a set window.

An SLA of 5 working days is enforced on all pending applications. Applications that cross this threshold are highlighted in red in the SLA Monitor (Section 5.2) and trigger escalation alerts to the Director. The approval history is retained permanently for audit purposes and is accessible to the Director and the Finance team for scholarship disbursement reconciliation. All approval and rejection decisions are logged with the decider's name, timestamp, and (for rejections) a mandatory reason code, creating an auditable compliance trail for government inspections and board reviews.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Manager (27) | G3 | Full — review, approve, reject, request docs | Primary decision-maker |
| Group Admissions Director (23) | G3 | View all + override decisions | Override adds a note to audit log |
| Group Admission Counsellor (25) | G3 | View own recommendations' status only | Scoped to recommendations they submitted |
| Branch Principal | Branch | View own branch nominations' status | Branch-scoped read only |
| Chief Financial Officer | G1 | View approved + history (for disbursement) | Read-only |
| Group Admission Coordinator (24) | G3 | No access to decisions | Excluded from approval function |
| Group Admission Coordinator (Role 24) | G3 | Read — can view approval records for applications they referred | Cannot approve, reject, or request documents; can track status of their scholarship referrals |

**Enforcement:** `@role_required(['scholarship_manager', 'admissions_director', 'counsellor', 'principal', 'cfo'])` at view level. Counsellor and Principal see only their own submissions via Django queryset filters (`submitted_by == request.user` or `branch == request.user.branch`). Approve/Reject/Request-Docs API endpoints require JWT with `role == scholarship_manager`. Director override uses a dedicated endpoint tagged as `action_type = override`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarships → Approval Workflow
```

### 3.2 Page Header
- **Title:** Scholarship Approval Workflow
- **Subtitle:** Review and decide on all scholarship applications and recommendations
- **Action Buttons:** `[Bulk Approve All Merit (Exam >85%)]` (Scholarship Manager only) · `[Request Docs for All Incomplete]` · `[Export Queue]`
- **Queue Count Chip:** "X applications pending decision"

### 3.3 Alert Banner
Triggers:
- **Red — SLA Breached:** "{n} applications have been pending for more than 5 days. [View SLA Breaches →]"
- **Amber — Document Incomplete:** "{n} applications are awaiting document submission. [View →]"
- **Amber — Auto-Recommendations Waiting:** "{n} exam-based auto-recommendations are awaiting bulk approval. [Review Auto-Recommendations →]"
- **Blue — High Volume Day:** "Today's queue has {n} new applications — highest this cycle."
- **Green — All Cleared:** "Approval queue is clear. No pending applications."

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Pending Approvals | COUNT of applications with status = 'pending' | `scholarship_application` | Red > 20 · Amber 1–20 · Green = 0 | → Section 5.1 approval queue |
| Approved Today | COUNT of approvals with decision_date = today | `scholarship_application` | Green always | → Section 5.4 history filtered to today |
| Rejected Today | COUNT of rejections with decision_date = today | `scholarship_application` | Blue always | → Section 5.4 history filtered to today |
| Auto-Recommended Pending | COUNT of applications with basis = 'exam_result' and status = 'pending' | `scholarship_application` | Amber > 0 · Green = 0 | → Section 5.3 |
| Document-Incomplete | COUNT where document_status = 'incomplete' and status = 'pending' | `scholarship_application` | Amber > 0 · Green = 0 | → queue filtered by doc status |
| SLA Breached (>5 days) | COUNT where status = 'pending' and days_pending > 5 | `scholarship_application` | Red > 0 · Green = 0 | → Section 5.2 SLA monitor |

**HTMX Refresh:** Every 5 minutes via `hx-trigger="every 5m"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Approval Queue

**Display:** Sortable, selectable (checkbox), server-side paginated (20/page). Default sort: days_pending DESC (longest waiting first).

**Columns:**

| Column | Notes |
|---|---|
| Checkbox | Bulk select |
| Application ID | System ref, e.g., SCH-APP-2026-0412 |
| Student Name | Full name — linked to approval-detail-drawer |
| Branch | Branch name |
| Scheme | Scheme name |
| Basis | Exam Score (blue) / Income Proof (purple) / Counsellor Rec (teal) / Principal Nomination (orange) — badge |
| Amount | ₹X,XXX or XX% waiver |
| Submitted by | Staff name |
| Date | Submitted date |
| Documents | Complete (green ✓) / Incomplete (red ✗) — with item count on hover |
| Days Pending | Numeric — red badge if > 5 |
| Actions | `[Approve ✓]` · `[Reject ✗]` · `[Request Docs]` · `[View →]` |

**Filters:** Basis (multi-select), Branch (multi-select), Scheme (multi-select), Status (pending/all), Days pending (> 5 / all), Document status (complete / incomplete)

**Bulk Actions (Scholarship Manager only):** `[Approve All Merit (Exam >85%)]` · `[Request Docs for All Incomplete]` · `[Export]`

**HTMX Pattern:** Filter changes → `GET /api/v1/group/{group_id}/adm/scholarship-approvals/queue/` targeting `#approval-queue-body`.

**Empty State:** Queue is clear. Icon: check-circle (large). Heading: "Approval Queue Clear". Description: "No applications are pending decision." CTA: None.

---

### 5.2 Approval SLA Monitor

**Display:** Alert list — applications pending > 5 days. Sorted by days_pending DESC. Collapsed when count = 0.

**Columns:** Red badge (days pending) · Application ID · Student Name · Branch · Scheme · Basis · Days Pending · `[Prioritise →]`

**`[Prioritise →]`:** Marks application as Priority (pin at top of queue in Section 5.1) + sends internal alert to Scholarship Manager.

**HTMX Pattern:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-approvals/sla-breaches/` targeting `#sla-monitor`. Auto-refreshes every 5 minutes.

**Empty State:** No SLA breaches. Icon: clock-check. Heading: "SLA Compliant". Description: "All applications are within the 5-day review window."

---

### 5.3 Auto-Recommendations Queue

**Display:** Separate sub-table — applications auto-generated from published scholarship exam results where score meets scheme threshold. Visually distinct (light blue background header).

**Columns:** Application ID · Student Name · Branch · Scheme · Exam Score · Score % · Rank (Group) · Scheme Threshold · Amount · Generated Date · Days Pending · `[Approve]` `[View →]`

**Bulk Action:** `[Bulk Approve All →]` (prominent button at top of sub-table — one-click approval for all auto-recommendations meeting the threshold exactly).

**Confirmation:** Bulk approve requires a confirmation modal with count: "Approve {n} auto-recommendations for {scheme} based on exam score ≥ {threshold}%?"

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-approvals/auto-recommendations/` targeting `#auto-rec-table`.

**Empty State:** No auto-recommendations pending. Heading: "No Auto-Recommendations Pending."

---

### 5.4 Approval History

**Display:** Paginated table — all decided applications (approved + rejected). Default sort: decision_date DESC.

**Columns:**

| Column | Notes |
|---|---|
| Student Name | Linked to approval-detail-drawer (read-only view) |
| Branch | Branch name |
| Scheme | Scheme name |
| Decision | Approved (green chip) / Rejected (red chip) / Overridden (purple chip) |
| Date | Decision date |
| Decided by | Staff name |
| Amount | Approved amount (₹ or %) |
| Actions | `[View →]` |

**Filters:** Date range, Branch, Scheme, Decision type

**HTMX Pattern:** Filter changes → `GET /api/v1/group/{group_id}/adm/scholarship-approvals/history/` targeting `#approval-history-body`.

**Empty State:** No decisions recorded yet. Message: "Approval history will appear here as decisions are made."

---

### 5.5 Rejection Reason Analysis

**Display:** Horizontal bar chart (Chart.js 4.x) — rejections in current cycle grouped by reason.

**Reason Categories (X-axis labels):** Income proof insufficient · Score below cut-off · Scheme quota full · Duplicate application · Missing document · Other

**Y-axis:** Count of rejections.

**Tooltip:** Hover shows: reason label, count, % of total rejections this cycle.

**Interaction:** Click a bar → filters approval history to that rejection reason.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-approvals/stats/rejection-reasons/`.

---

## 6. Drawers & Modals

### 6.1 Approval Detail Drawer
- **Width:** 640px
- **Trigger:** `[View →]` on queue or history row
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/detail/`
- **Tabs:**
  1. **Student Profile** — Name, branch, class, contact, parent details
  2. **Application Details** — Scheme, basis, amount requested, submission date, submitted by, application text
  3. **Documents** — Uploaded documents preview (income cert, exam scorecard, etc.) — open in new tab; document completeness checklist
  4. **Recommendation Notes** — Notes from counsellor/principal who submitted; exam score and rank if basis = exam
  5. **History** — Timeline: submitted → document check → review → decision (with timestamps and actors)
  6. **Decision** — Approve / Reject / Request Docs action panel; for reject: mandatory reason select + notes
- **Submit (Approve):** `hx-post` → `/api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/approve/`
- **Submit (Reject):** `hx-post` → `/api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/reject/`

### 6.2 Rejection Reason Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Reject ✗]` button on queue row or Decision tab in drawer
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/reject-modal/`
- **Content:** Reason select (mandatory — from reason category list) + Additional notes (textarea) + `[Confirm Rejection]` + `[Cancel]`
- **Submit:** `hx-post` → rejection endpoint · updates queue row, refreshes KPI bar, shows toast

### 6.3 Document Request Modal
- **Width:** 400px
- **Trigger:** `[Request Docs]` on queue row or in drawer
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/doc-request-modal/`
- **Content:** Checklist of missing documents (pre-filled from system) + free-text message to branch + deadline picker + `[Send Request]`
- **Submit:** `hx-post` → `/api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/request-docs/` · sends notification to branch, updates application document_status

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Application approved | "{Student Name}'s scholarship ({Scheme}) approved. ₹{Amount}." | Success | 4 s |
| Application rejected | "{Student Name}'s application rejected — {Reason}." | Info | 4 s |
| Document request sent | "Document request sent to {Branch} for {Student Name}." | Info | 4 s |
| Application prioritised | "{Student Name}'s application marked priority." | Info | 3 s |
| Bulk approve triggered | "Bulk approval initiated for {n} merit applications." | Info | 4 s |
| Bulk approve complete | "{n} merit scholarships approved successfully." | Success | 5 s |
| Bulk doc request sent | "Document request sent to {n} applications." | Info | 4 s |
| Director override applied | "Director override recorded for {Student Name}'s application." | Warning | 5 s |
| Auto-recommendation bulk approved | "{n} auto-recommendations approved from {Exam Name} results." | Success | 5 s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| Queue is empty | Check-circle icon | "Approval Queue Clear" | "No scholarship applications are pending decision." | None |
| No SLA breaches | Clock-check icon | "All Within SLA" | "All pending applications are within the 5-day review window." | None |
| No auto-recommendations | Automation icon | "No Auto-Recommendations" | "No exam-based auto-recommendations are pending approval." | None |
| No approval history | Clock icon | "No History Yet" | "Approval decisions will appear here." | None |
| Filter returns empty | Search-x icon | "No Applications Match Filters" | "Try adjusting filter criteria." | `[Clear Filters]` |
| Rejection Reason Analysis (5.5) chart empty | Chart outline icon | "No Rejection Data Yet" | "Rejection reason analysis will appear once applications have been rejected in this cycle." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | KPI shimmer (6 cards) + approval queue skeleton (8 rows) |
| KPI auto-refresh | In-place spinner per card |
| Queue filter / search | Table body skeleton (8 row shimmer) |
| SLA monitor load | List skeleton (3 item shimmers) |
| Auto-recommendations sub-table load | Table skeleton (5 row shimmer) |
| Approval history load / filter | Table skeleton (8 row shimmer) |
| Rejection reasons chart load | Bar chart canvas shimmer |
| Approval detail drawer open | 640px drawer skeleton with 6 tab-label shimmers |
| Rejection modal load | 400px modal skeleton with select + textarea shimmers |
| Document request modal load | 400px modal skeleton with checklist shimmers |
| Bulk approve processing | Button spinner + "Processing {n} approvals…" text |
| Single approve/reject action | Row-level spinner (inline) |

---

## 10. Role-Based UI Visibility

| Element | Scholarship Mgr (27) | Director (23) | Counsellor (25) | Principal | CFO | Coord (24) |
|---|---|---|---|---|---|---|
| `[Approve ✓]` action | Visible | Visible (override) | Hidden | Hidden | Hidden | Hidden |
| `[Reject ✗]` action | Visible | Visible (override) | Hidden | Hidden | Hidden | Hidden |
| `[Request Docs]` action | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Bulk action bar | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Bulk Approve All Merit]` button | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Bulk Approve All Auto-Rec]` | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Bulk Approve All]` in 5.3 | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| Section 5.1 Approval Queue table | Visible | Visible | Visible (own) | Visible (own branch) | Hidden | R (read-only rows, no action buttons) |
| Section 5.2 SLA Monitor | Visible (full + prioritise) | Visible (read) | Hidden | Hidden | Hidden | R (read-only) |
| `[Prioritise →]` button | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| Section 5.3 Auto-Rec Queue | Visible | Visible | Hidden | Hidden | Hidden | R (read-only) |
| Section 5.4 Approval History | Visible (all) | Visible (all) | Visible (own only) | Visible (own branch) | Visible (approved only) | R (read-only) |
| Section 5.5 Rejection Chart | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| Decision tab in drawer | Visible | Visible (override label) | Hidden | Hidden | Hidden | Hidden |
| Documents tab in drawer | Visible | Visible | Visible | Visible | Hidden | Visible |
| Student Profile tab in drawer | Visible | Visible | Visible (own rec) | Visible (own branch) | Hidden | Visible (referred applications) |

*All UI visibility decisions made server-side in Django template. No client-side JS role checks.*

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarship-approvals/kpis/` | JWT G3 | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-approvals/queue/` | JWT G3 | Paginated approval queue |
| GET | `/api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/detail/` | JWT G3 | Application detail drawer fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/approve/` | JWT G3 write | Approve application |
| POST | `/api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/reject/` | JWT G3 write | Reject application |
| GET | `/api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/reject-modal/` | JWT G3 | Rejection reason modal fragment |
| GET | `/api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/doc-request-modal/` | JWT G3 | Document request modal fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/request-docs/` | JWT G3 write | Send document request |
| GET | `/api/v1/group/{group_id}/adm/scholarship-approvals/sla-breaches/` | JWT G3 | SLA breach list |
| POST | `/api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/prioritise/` | JWT G3 write | Mark as priority |
| GET | `/api/v1/group/{group_id}/adm/scholarship-approvals/auto-recommendations/` | JWT G3 | Auto-recommendation sub-table |
| POST | `/api/v1/group/{group_id}/adm/scholarship-approvals/auto-recommendations/bulk-approve/` | JWT G3 write | Bulk approve auto-recommendations |
| GET | `/api/v1/group/{group_id}/adm/scholarship-approvals/history/` | JWT G3 | Approval history (paginated, filtered) |
| POST | `/api/v1/group/{group_id}/adm/scholarship-approvals/bulk-approve-merit/` | JWT G3 write | Bulk approve merit (score > 85%) |
| POST | `/api/v1/group/{group_id}/adm/scholarship-approvals/bulk-request-docs/` | JWT G3 write | Bulk request docs for incomplete |
| GET | `/api/v1/group/{group_id}/adm/scholarship-approvals/stats/rejection-reasons/` | JWT G3 | Rejection reason chart data |
| POST | `/api/v1/group/{group_id}/adm/scholarship-approvals/applications/{application_id}/override/` | JWT Director | Director override action |
| GET | `/api/v1/group/{group_id}/adm/scholarship-approvals/export/?format=csv` | JWT G3 | Export current approval queue as CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `.../scholarship-approvals/kpis/` | `#kpi-bar` | `innerHTML` |
| Filter approval queue | `change` on filter inputs | GET `.../scholarship-approvals/queue/?{filters}` | `#approval-queue-body` | `innerHTML` |
| Paginate approval queue | `click` on page link | GET `.../scholarship-approvals/queue/?page={n}` | `#approval-queue-container` | `innerHTML` |
| Sort approval queue | `click` on column header | GET `.../scholarship-approvals/queue/?sort={col}&dir={asc\|desc}` | `#approval-queue-body` | `innerHTML` |
| Open application detail drawer | `click` on `[View →]` or student name | GET `.../scholarship-approvals/applications/{id}/detail/` | `#drawer-container` | `innerHTML` |
| Inline approve (queue row) | `click` on `[Approve ✓]` | POST `.../scholarship-approvals/applications/{id}/approve/` | `#queue-row-{id}` | `outerHTML` |
| Open rejection reason modal | `click` on `[Reject ✗]` | GET `.../scholarship-approvals/applications/{id}/reject-modal/` | `#modal-container` | `innerHTML` |
| Submit rejection | `submit` on rejection form | POST `.../scholarship-approvals/applications/{id}/reject/` | `#queue-row-{id}` | `outerHTML` |
| Open document request modal | `click` on `[Request Docs]` | GET `.../scholarship-approvals/applications/{id}/doc-request-modal/` | `#modal-container` | `innerHTML` |
| Submit document request | `submit` on doc-request form | POST `.../scholarship-approvals/applications/{id}/request-docs/` | `#queue-row-{id}` | `outerHTML` |
| Load SLA monitor | `load` on section | GET `.../scholarship-approvals/sla-breaches/` | `#sla-monitor` | `innerHTML` |
| SLA monitor auto-refresh | `every 5m` | GET `.../scholarship-approvals/sla-breaches/` | `#sla-monitor` | `innerHTML` |
| Load auto-recommendations | `load` on section | GET `.../scholarship-approvals/auto-recommendations/` | `#auto-rec-table` | `innerHTML` |
| Bulk approve auto-rec | `click` on `[Bulk Approve All →]` | POST `.../scholarship-approvals/auto-recommendations/bulk-approve/` | `#auto-rec-table` | `innerHTML` |
| Filter approval history | `change` on history filters | GET `.../scholarship-approvals/history/?{filters}` | `#approval-history-body` | `innerHTML` |
| Load rejection reasons chart | `load` on chart section | GET `.../scholarship-approvals/stats/rejection-reasons/` | `#rejection-chart-data` | `innerHTML` |
| Refresh KPIs after decision | `htmx:afterRequest` from approve/reject calls | GET `.../scholarship-approvals/kpis/` | `#kpi-bar` | `innerHTML` |
| Prioritise SLA-breached application | `click from:.btn-prioritise` | POST `.../scholarship-approvals/{id}/prioritise/` | `#sla-monitor-section` | `innerHTML` |
| Export approval queue | `click from:#btn-export-queue` | GET `.../scholarship-approvals/export/?format=csv` | `#toast-container` | `afterbegin` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
