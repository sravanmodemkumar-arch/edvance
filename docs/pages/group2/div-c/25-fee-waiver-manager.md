# Page 25: Fee Waiver Manager

**URL:** `/group/adm/fee-waivers/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions · Scholarship Section

---

## 1. Purpose

Fee waivers are distinct from scholarships in both origin and process. While scholarships are scheme-based awards with defined eligibility criteria, fee waivers are discretionary reductions granted case-by-case for students facing genuine hardship or demonstrating exceptional merit in circumstances not covered by an existing scheme. A family affected by sudden income loss, a student who performed brilliantly but missed a scholarship cut-off by a narrow margin, or a child of a deceased or disabled parent — these are the use cases that waivers address. They are intentionally flexible and human-reviewed rather than automated.

Waivers can apply to tuition fees, hostel fees, transport fees, or one-time exam fees. They may be full (100% of the relevant fee head) or partial (any percentage or fixed amount). Recurring waivers are granted per term or per academic year and must be explicitly renewed. The Scholarship Manager has authority to approve waivers up to a defined limit — beyond that threshold, approval escalates to the Director. For the largest waivers, CEO approval is required. This tiered authority model is displayed as a fixed banner (Section 5.2) so all users understand the escalation path.

Every waiver must be backed by documented justification — hardship documentation, income proof, principal's recommendation letter, or other supporting material — and is subject to Finance team audit. The waiver budget per branch is set annually, and Section 5.4 tracks how much of each branch's budget has been committed through approved waivers, preventing over-allocation. The page is also responsible for flagging recurring waivers that are approaching their expiry date so the Manager can decide to renew or discontinue before the next fee cycle begins.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Manager (27) | G3 | Full — approve up to ₹10,000 limit, submit/review all, escalate | Primary decision-maker within limit |
| Group Admissions Director (23) | G3 | Approve up to ₹50,000 limit + view all | Receives escalated requests |
| CEO | G1 | Approve all amounts (unlimited) | Receives Director-escalated requests |
| Group Admission Coordinator (24) | G3 | Submit waiver requests on behalf of branch | Can submit, not decide |
| Chief Financial Officer | G1 | View all — budget tracking | Read-only oversight |
| Branch Principal | Branch | Submit waiver requests for own branch | Submit only, branch-scoped |

**Enforcement:** `@role_required(['scholarship_manager', 'admissions_director', 'ceo', 'coordinator', 'cfo', 'principal'])`. Approval API endpoints enforce amount-based access: `if amount > 10000 and role != director_or_ceo: return 403`. Coordinator and Principal can only submit (POST) — they see submitted status but cannot change decisions. CFO gets read-only access. Django annotation `approval_level_required` is set on each waiver record based on amount.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarships → Fee Waiver Manager
```

### 3.2 Page Header
- **Title:** Fee Waiver Manager
- **Subtitle:** Discretionary fee reductions — tiered approval authority
- **Action Buttons:** `[+ Request Waiver]` (Coordinator/Principal for submissions) · `[Approve Selected (within limit)]` (Scholarship Manager) · `[Export Waiver Report]`
- **Summary Chips:** "{n} pending approvals" · "₹{amount} approved this term"

### 3.3 Alert Banner
Triggers:
- **Red — Budget Exceeded:** "{n} branches have waiver approvals exceeding their allocated budget. [Review →]"
- **Amber — Renewals Expiring:** "{n} recurring waivers expire at the end of this term. [View Renewals →]"
- **Amber — Escalation Queue:** "{n} waiver requests exceed your approval limit and are awaiting Director/CEO review. [View →]"
- **Blue — High-Value Request:** "A waiver request of ₹{amount} for {Student Name} requires CEO approval. [Escalate →]"

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Waiver Requests Pending | COUNT where status = 'pending' | `fee_waiver` | Amber > 0 · Green = 0 | → Section 5.1 filtered to pending |
| Waivers Approved This Term | COUNT where status = 'approved' and term = current | `fee_waiver` | Green always | → history filtered to approved |
| Total Waiver Value Approved (₹) | SUM of approved_amount in current term | `fee_waiver` | Blue always | → budget tracker |
| Waivers Exceeding Director Threshold | COUNT where amount > 50000 and status = 'pending' | `fee_waiver` | Red > 0 · Green = 0 | → escalation queue |
| Waiver Budget Utilized % | (Approved YTD / total waiver budget) × 100 | `waiver_budget` + `fee_waiver` | Green ≤ 80% · Amber 81–95% · Red > 95% | → Section 5.4 |
| Waiver Renewals Due This Month | COUNT of recurring waivers with expiry_date in current month | `fee_waiver` recurring | Amber > 0 · Green = 0 | → Section 5.6 |

**HTMX Refresh:** Every 5 minutes via `hx-trigger="every 5m"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Waiver Request Table

**Display:** Sortable, selectable (checkbox), server-side paginated (20/page). Default sort: request_date DESC.

**Columns:**

| Column | Notes |
|---|---|
| Checkbox | Bulk select (within current role's approval limit) |
| Request ID | System ref, e.g., WVR-2026-0089 |
| Student Name | Full name — linked to waiver-review-drawer |
| Branch | Branch name |
| Fee Type | Tuition (blue) / Hostel (green) / Transport (amber) / Exam (teal) — badge |
| Requested Amount (₹) | Numeric |
| % of Total Fee | Percentage |
| Reason Category | Hardship / Merit / Special Category / Sibling Concession / Staff Ward / Other |
| Supporting Doc | Uploaded (green ✓) / Not uploaded (red ✗) |
| Requested by | Staff name (counsellor / coordinator / principal) |
| Request Date | DD-MMM-YYYY |
| Approval Level Required | Scholarship Manager / Director / CEO — colour-coded |
| Status | Pending (grey) / Approved (green) / Rejected (red) / Escalated (amber) / Renewed (teal) |
| Actions | `[Approve ✓]` (within limit) · `[Reject ✗]` · `[Escalate ↑]` · `[View →]` |

**Filters:** Fee type, Status, Branch, Amount range (from–to), Approval level, Reason category

**Bulk Actions (within limit):** `[Approve Selected (within limit)]` · `[Export]`

**HTMX Pattern:** Filter changes → `GET /api/v1/group/{group_id}/adm/fee-waivers/requests/` targeting `#waiver-table-body`.

**Empty State:** No requests pending. Icon: check-circle. Heading: "No Pending Waiver Requests."

---

### 5.2 Approval Threshold Banner

**Display:** Fixed information banner — always visible on this page. Non-dismissible.

**Content:**

> **Waiver Approval Authority:**
> Waivers up to **₹10,000** — Scholarship Manager
> ₹10,001 – **₹50,000** — Admissions Director
> Above **₹50,000** — CEO

Visual: Three column layout with role, limit, and escalation path. Background: light blue info panel. Icon: info-circle.

---

### 5.3 Escalation Queue

**Display:** Sub-table — waiver requests that exceed the current user's approval limit and are pending at a higher level. Sorted by amount DESC.

**Columns:** Request ID · Student Name · Branch · Amount (₹) · Approval Level Required · Submitted to (role name) · Days Waiting · Status (Escalated / Awaiting CEO)

**For Scholarship Manager:** Shows requests escalated to Director/CEO.
**For Director:** Shows requests escalated to CEO only.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/fee-waivers/escalation-queue/` targeting `#escalation-queue`.

**Empty State:** No requests awaiting higher-level approval. Heading: "Escalation Queue Clear."

---

### 5.4 Waiver Budget Tracker

**Display:** Progress bar + breakdown table per branch.

**Progress Bar (group-wide):** Group total: Budget allocated (₹ value) · Approved YTD (₹) · Remaining (₹) · Utilization % bar.

**Table (per branch):**

| Column | Notes |
|---|---|
| Branch | Branch name |
| Budget Allocated (₹) | Annual waiver budget for branch |
| Approved YTD (₹) | Sum of approved waivers for branch in current year |
| Remaining (₹) | Budget – Approved (red if negative) |
| Utilization % | Progress bar in cell |

**Alert:** Branch rows with remaining < 0 highlighted in red (over budget).

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/fee-waivers/budget/` targeting `#budget-tracker`.

---

### 5.5 Waiver History

**Display:** Paginated table — all decided waivers (20/page). Default sort: decision_date DESC.

**Columns:**

| Column | Notes |
|---|---|
| Student | Full name |
| Branch | Branch name |
| Amount (₹) | Approved amount |
| Fee Type | Badge |
| Decision | Approved (green) / Rejected (red) |
| Decided by | Staff name + role |
| Date | Decision date |
| Reason | Reason category |
| Actions | `[View →]` |

**Filters:** Decision type, Branch, Fee type, Date range

**HTMX Pattern:** Filter changes → `GET /api/v1/group/{group_id}/adm/fee-waivers/history/` targeting `#waiver-history-body`.

---

### 5.6 Waiver Renewal Alerts

**Display:** Alert list — recurring waivers expiring this term. Sorted by expiry_date ASC.

**Columns:** Student Name · Branch · Current Waiver Amount (₹) · Fee Type · Expiry Date · Days Until Expiry (red < 7 · amber 8–30 · green > 30) · Actions: `[Renew →]` · `[Discontinue →]`

**`[Renew →]`:** Opens renewal-modal with pre-filled data.
**`[Discontinue →]`:** Confirm modal → marks waiver as discontinued for next term.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/fee-waivers/renewals/expiring/` targeting `#renewal-alerts`.

**Empty State:** No waivers expiring this term. Icon: calendar-check. Heading: "No Waivers Expiring Soon."

---

## 6. Drawers & Modals

### 6.1 Waiver Review Drawer
- **Width:** 640px
- **Trigger:** `[View →]` on table row
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/review/`
- **Tabs:**
  1. **Student Profile** — Name, branch, class, parent details, fee outstanding
  2. **Fee Details** — Total fee, fee type, amount requested, % of total fee, recurring vs one-time
  3. **Hardship Documentation** — Uploaded documents preview (income cert, principal letter, etc.); completeness checklist
  4. **Financial Impact** — Impact on branch budget: current budget remaining, post-approval remaining
  5. **Decision** — Approve / Reject / Escalate action panel with reason field (mandatory for reject/escalate)
- **Submit:** `hx-post` to respective endpoint based on action

### 6.2 Waiver Escalate Modal
- **Width:** 400px
- **Trigger:** `[Escalate ↑]` on table row or in waiver review drawer Decision tab
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/escalate-modal/`
- **Content:** Shows waiver amount, displays threshold banner info, escalation route (Scholarship Manager → Director → CEO), Reason for escalation (required), `[Escalate to {Next Level}]` + `[Cancel]`
- **Submit:** `hx-post` → `/api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/escalate/`

### 6.3 Renewal Modal
- **Width:** 400px
- **Trigger:** `[Renew →]` in Section 5.6
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/renew-modal/`
- **Content:** Pre-filled: student name, branch, fee type, current amount, new term start/end dates, renewal amount (editable — default same as current), notes, `[Renew Waiver]` + `[Cancel]`
- **Submit:** `hx-post` → `/api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/renew/`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Waiver request submitted | "Waiver request WVR-{id} submitted for {Student Name}." | Info | 4 s |
| Waiver approved | "Waiver approved for {Student Name} — ₹{amount} {fee type}." | Success | 4 s |
| Waiver rejected | "Waiver request for {Student Name} rejected — {reason}." | Info | 4 s |
| Waiver escalated | "Waiver for {Student Name} escalated to {role}." | Info | 4 s |
| Waiver renewed | "Waiver for {Student Name} renewed for {term}." | Success | 4 s |
| Waiver discontinued | "Recurring waiver for {Student Name} discontinued from next term." | Warning | 5 s |
| Bulk approve complete | "{n} waiver requests approved." | Success | 4 s |
| Budget limit reached | "Warning: {Branch} has reached its waiver budget limit." | Warning | 6 s |
| Export queued | "Waiver report is being prepared." | Info | 3 s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No pending requests | Check-circle icon | "No Pending Waiver Requests" | "All waiver requests have been decided." | None |
| Escalation queue empty | Layers icon | "Escalation Queue Clear" | "No requests are awaiting higher-level approval." | None |
| No waiver history | History icon | "No Waiver History" | "Decided waivers will appear here." | None |
| No expiring renewals | Calendar-check icon | "No Waivers Expiring Soon" | "No recurring waivers expire this term." | None |
| Filter returns empty | Filter-x icon | "No Requests Match Filters" | "Try adjusting your filter criteria." | `[Clear Filters]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | KPI shimmer (6 cards) + table skeleton (8 rows) |
| KPI auto-refresh | In-place spinner per card |
| Table filter change | Table skeleton (8 row shimmer) |
| Escalation queue load | List skeleton (3 item shimmers) |
| Budget tracker load | Progress bar shimmer + table skeleton |
| Waiver history load | Table skeleton (8 row shimmer) |
| Renewal alerts load | List skeleton (5 item shimmers) |
| Waiver review drawer open | 640px drawer with 5 tab shimmers |
| Escalate modal open | 400px modal skeleton |
| Renewal modal open | 400px modal with form field shimmers |
| Bulk approve processing | Button spinner + "Approving {n} requests…" |
| Single approve/reject | Row-level inline spinner |

---

## 10. Role-Based UI Visibility

| Element | Scholarship Mgr (27) | Director (23) | CEO | Coordinator (24) | CFO | Principal |
|---|---|---|---|---|---|---|
| `[+ Request Waiver]` button | Hidden | Hidden | Hidden | Visible | Hidden | Visible |
| `[Approve ✓]` (within limit) | Visible (≤₹10k) | Visible (≤₹50k) | Visible (all) | Hidden | Hidden | Hidden |
| `[Reject ✗]` | Visible | Visible | Visible | Hidden | Hidden | Hidden |
| `[Escalate ↑]` | Visible | Visible (to CEO) | Hidden | Hidden | Hidden | Hidden |
| Bulk approve button | Visible (within limit) | Visible (within limit) | Visible | Hidden | Hidden | Hidden |
| Section 5.2 threshold banner | Visible | Visible | Visible | Visible | Visible | Visible |
| Section 5.3 Escalation Queue | Visible | Visible | Visible | Hidden | Hidden | Hidden |
| Section 5.4 Budget Tracker | Visible | Visible | Visible | Hidden | Visible | Hidden |
| Section 5.5 Waiver History | Visible (all) | Visible (all) | Visible (all) | Visible (own branch) | Visible | Visible (own branch) |
| Section 5.6 Renewal Alerts | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| Decision tab in drawer | Visible | Visible | Visible | Hidden | Hidden | Hidden |
| Financial Impact tab | Visible | Visible | Visible | Hidden | Visible | Hidden |

*All UI visibility decisions made server-side in Django template. No client-side JS role checks.*

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/fee-waivers/kpis/` | JWT G3 | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/fee-waivers/requests/` | JWT G3 | Paginated, filtered waiver requests |
| POST | `/api/v1/group/{group_id}/adm/fee-waivers/requests/` | JWT G3 (submit roles) | Submit new waiver request |
| GET | `/api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/review/` | JWT G3 | Waiver review drawer fragment |
| POST | `/api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/approve/` | JWT G3 write (within limit) | Approve waiver |
| POST | `/api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/reject/` | JWT G3 write | Reject waiver |
| GET | `/api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/escalate-modal/` | JWT G3 | Escalate modal fragment |
| POST | `/api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/escalate/` | JWT G3 write | Escalate to next approval level |
| POST | `/api/v1/group/{group_id}/adm/fee-waivers/requests/bulk-approve/` | JWT G3 write | Bulk approve within limit |
| GET | `/api/v1/group/{group_id}/adm/fee-waivers/escalation-queue/` | JWT G3 | Escalation queue (role-scoped) |
| GET | `/api/v1/group/{group_id}/adm/fee-waivers/budget/` | JWT G3 | Budget tracker data |
| GET | `/api/v1/group/{group_id}/adm/fee-waivers/history/` | JWT G3 | Waiver history (paginated) |
| GET | `/api/v1/group/{group_id}/adm/fee-waivers/renewals/expiring/` | JWT G3 | Expiring recurring waivers |
| GET | `/api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/renew-modal/` | JWT G3 | Renewal modal fragment |
| POST | `/api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/renew/` | JWT G3 write | Renew recurring waiver |
| POST | `/api/v1/group/{group_id}/adm/fee-waivers/requests/{waiver_id}/discontinue/` | JWT G3 write | Discontinue recurring waiver |
| GET | `/api/v1/group/{group_id}/adm/fee-waivers/export/report/` | JWT G3 | Export waiver report |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `.../fee-waivers/kpis/` | `#kpi-bar` | `innerHTML` |
| Filter waiver table | `change` on filter inputs | GET `.../fee-waivers/requests/?{filters}` | `#waiver-table-body` | `innerHTML` |
| Paginate waiver table | `click` on page link | GET `.../fee-waivers/requests/?page={n}` | `#waiver-table-container` | `innerHTML` |
| Sort waiver table | `click` on column header | GET `.../fee-waivers/requests/?sort={col}&dir={asc\|desc}` | `#waiver-table-body` | `innerHTML` |
| Open waiver review drawer | `click` on `[View →]` or student name | GET `.../fee-waivers/requests/{id}/review/` | `#drawer-container` | `innerHTML` |
| Inline approve waiver | `click` on `[Approve ✓]` | POST `.../fee-waivers/requests/{id}/approve/` | `#waiver-row-{id}` | `outerHTML` |
| Inline reject waiver | `click` on `[Reject ✗]` | POST `.../fee-waivers/requests/{id}/reject/` | `#waiver-row-{id}` | `outerHTML` |
| Open escalate modal | `click` on `[Escalate ↑]` | GET `.../fee-waivers/requests/{id}/escalate-modal/` | `#modal-container` | `innerHTML` |
| Submit escalation | `submit` on escalation form | POST `.../fee-waivers/requests/{id}/escalate/` | `#waiver-row-{id}` | `outerHTML` |
| Bulk approve | `click` on `[Approve Selected]` | POST `.../fee-waivers/requests/bulk-approve/` | `#waiver-table-body` | `innerHTML` |
| Load escalation queue | `load` on section | GET `.../fee-waivers/escalation-queue/` | `#escalation-queue` | `innerHTML` |
| Load budget tracker | `load` on section | GET `.../fee-waivers/budget/` | `#budget-tracker` | `innerHTML` |
| Filter waiver history | `change` on history filters | GET `.../fee-waivers/history/?{filters}` | `#waiver-history-body` | `innerHTML` |
| Load renewal alerts | `load` on section | GET `.../fee-waivers/renewals/expiring/` | `#renewal-alerts` | `innerHTML` |
| Open renewal modal | `click` on `[Renew →]` | GET `.../fee-waivers/requests/{id}/renew-modal/` | `#modal-container` | `innerHTML` |
| Submit renewal | `submit` on renewal form | POST `.../fee-waivers/requests/{id}/renew/` | `#renewal-row-{id}` | `outerHTML` |
| Discontinue waiver | `click` on `[Discontinue →]` | POST `.../fee-waivers/requests/{id}/discontinue/` | `#renewal-row-{id}` | `outerHTML` |
| Refresh KPIs after decision | `htmx:afterRequest` from approve/reject calls | GET `.../fee-waivers/kpis/` | `#kpi-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
