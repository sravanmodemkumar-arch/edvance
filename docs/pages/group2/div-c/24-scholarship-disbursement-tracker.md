# Page 24: Scholarship Disbursement Tracker

**URL:** `/group/adm/scholarship-disbursement/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions · Scholarship Section

---

## 1. Purpose

Once a scholarship is approved, its financial value must be delivered to the beneficiary — either as a direct reduction in the fee challan (fee adjustment), a cash grant, a demand draft, or a bank transfer for government-linked schemes. This delivery step is the disbursement, and the Scholarship Disbursement Tracker is the operational dashboard that ensures no approved scholarship is forgotten, delayed, or lost in the finance pipeline. The page bridges the scholarship approval system and the Finance team's fee collection module.

Disbursements may be one-time (a single exam-fee waiver) or recurring (a per-term tuition fee reduction for a student in a three-year program). The tracker therefore handles both the immediate queue of undisbursed approvals and the forward-looking calendar of recurring disbursements coming due. For fee adjustments, the Scholarship Manager marks an approval as "disbursement requested" and the Finance Manager or CFO executes the actual adjustment in the fee module — the status then flows back to this tracker via the API. For direct cash or transfer-based disbursements, the Finance Manager records the reference number and date here after payment is made.

Government-linked disbursements (NSP, PMSS, state scholarships) operate on a different cycle: the group files claims with the government portal, awaits the fund release, and then transfers the received amount to eligible students' accounts. This sub-process has its own tracker in Section 5.4. The Annual Budget Utilization chart in Section 5.5 gives the Director and CFO a real-time view of how much of the approved scholarship budget has been committed versus disbursed versus remaining, supporting mid-year budget reviews.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Manager (27) | G3 | View all + mark disbursement requested + escalate | Cannot execute finance actions |
| Chief Financial Officer (CFO) | G1 | Full — all sections including finance actions | Primary finance authority |
| Finance Manager | G2 | Disbursement section — view + mark disbursed + record references | Branch or group scope depending on configuration |
| Group Admissions Director (23) | G3 | View only | Read-only oversight |
| Group Admission Coordinator (24) | G3 | No access | Excluded |
| MIS Officer | G2 | View only — report generation | Read-only |

**Enforcement:** `@role_required(['scholarship_manager', 'cfo', 'finance_manager', 'admissions_director', 'mis_officer'])`. The `[Mark Disbursed →]` and reference-number update endpoints require JWT with `role in ['cfo', 'finance_manager']`. The Scholarship Manager can only invoke `[Escalate →]` (not mark-disbursed). Django queryset filters scope Finance Manager to their branch unless `scope == group`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarships → Disbursement Tracker
```

### 3.2 Page Header
- **Title:** Scholarship Disbursement Tracker
- **Subtitle:** Track fee adjustments, cash grants, and government transfers
- **Action Buttons:** `[Export Disbursement Report]` · `[Download Govt Claim Summary]`
- **Summary Chips:** "₹X approved but undisbursed" · "₹Y disbursed this month"

### 3.3 Alert Banner
Triggers:
- **Red — Overdue Disbursements:** "{n} approved scholarships have been undisbursed for more than 30 days. [View →]"
- **Amber — Finance Pending:** "{n} fee adjustments are queued with Finance and not yet processed. [Escalate →]"
- **Amber — Govt Grant Overdue:** "PMSS grant for AY 2025-26 — ₹{amount} is overdue. Last follow-up: {date}. [Track →]"
- **Blue — Budget Threshold:** "Annual scholarship disbursement has reached 80% of the approved budget."
- **Green — Month Summary:** "This month: ₹{amount} disbursed to {n} beneficiaries across {b} branches."

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Approved but Undisbursed (₹) | SUM of approved_amount WHERE disbursement_status = 'pending' | `scholarship_disbursement` | Red > ₹5,00,000 · Amber > 0 · Green = 0 | → Section 5.1 queue |
| Disbursed This Month (₹) | SUM of disbursed_amount WHERE disbursement_date in current month | `scholarship_disbursement` | Green always | → history filtered to this month |
| Govt Grants Receivable (₹) | SUM of (claimable_amount – received_amount) from govt grant records | `govt_grant_tracker` | Amber > 0 · Green = 0 | → Section 5.4 |
| Overdue Disbursements | COUNT where days_since_approval > 30 and status = 'pending' | `scholarship_disbursement` | Red > 0 · Green = 0 | → queue filtered by overdue |
| Fee Adjustments Pending | COUNT where type = 'fee_adjustment' and status = 'pending' | `scholarship_disbursement` | Amber > 0 · Green = 0 | → queue filtered by type |
| Budget Utilized % | (Total disbursed YTD / annual budget) × 100 | `scholarship_budget` + `scholarship_disbursement` | Green ≤ 80% · Amber 81–95% · Red > 95% | → Section 5.5 budget donut |

**HTMX Refresh:** Every 5 minutes via `hx-trigger="every 5m"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Disbursement Queue

**Display:** Sortable, selectable (checkbox), server-side paginated (20/page). Default sort: days_since_approval DESC.

**Columns:**

| Column | Notes |
|---|---|
| Student Name | Full name |
| Branch | Branch name |
| Scheme | Scheme name |
| Approved Amount | ₹ formatted |
| Disbursement Type | Fee Adjustment (blue) / Cash (green) / DD (amber) / Transfer (purple) — badge |
| Approved Date | DD-MMM-YYYY |
| Days Since Approval | Numeric — red if > 30 |
| Finance Status | Pending (grey) / Submitted to Finance (amber) / In Progress (blue) / Completed (green) |
| Actions | `[Mark Disbursed →]` (CFO/Finance Manager only) · `[Escalate →]` (Scholarship Manager) |

**Filters:** Disbursement type, Branch, Scheme, Days pending (all / >30 overdue), Finance status

**HTMX Pattern:** Filter changes → `GET /api/v1/group/{group_id}/adm/scholarship-disbursement/queue/` targeting `#disbursement-queue-body`.

**Empty State:** No undisbursed approvals. Icon: check-circle. Heading: "All Scholarships Disbursed". Description: "No approved scholarships are pending disbursement."

---

### 5.2 Disbursement History

**Display:** Paginated table (20/page). Default sort: disbursed_on DESC.

**Columns:**

| Column | Notes |
|---|---|
| Student | Full name |
| Branch | Branch name |
| Scheme | Scheme name |
| Amount (₹) | Disbursed amount |
| Type | Disbursement type badge |
| Disbursed On | Date |
| Mode | Payment mode |
| Reference | Reference number (cheque / DD / UTR / adjustment ref) |
| Disbursed by | Finance staff name |
| Actions | `[Receipt →]` (opens disbursement-detail drawer) |

**Filters:** Date range, Branch, Scheme, Mode (multi-select)

**HTMX Pattern:** Filter changes → `GET /api/v1/group/{group_id}/adm/scholarship-disbursement/history/` targeting `#disbursement-history-body`.

---

### 5.3 Monthly Disbursement Chart

**Display:** Stacked vertical bar chart (Chart.js 4.x) — month-wise disbursement totals for the current financial year.

**X-axis:** Months (Apr–Mar for Indian academic year). **Y-axis:** ₹ amount.

**Stacks:** Merit (blue) · Need-based (purple) · RTE (orange) · Government (green) · Group-Special (grey)

**Tooltip:** Month name, total disbursed, per-scheme-type breakdown, count of beneficiaries.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-disbursement/stats/monthly/` targeting `#monthly-chart-data`.

---

### 5.4 Government Grant Tracker

**Display:** Table — one row per government scheme with active grant.

**Columns:**

| Column | Notes |
|---|---|
| Scheme | NSP / PMSS / State scheme name |
| Students | Count enrolled |
| Amount Receivable (₹) | Total claimable from government |
| Submitted to Govt | Date of claim submission (or "Not yet") |
| Received from Govt (₹) | Amount received |
| Transferred to Students (₹) | Amount passed on to students |
| Pending (₹) | Receivable – Received (red if > 0) |
| Actions | `[View Details →]` (opens govt-grant-detail drawer) |

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-disbursement/govt-grants/` targeting `#govt-grant-table`.

**Empty State:** No government grants configured. Heading: "No Government Grants Tracked."

---

### 5.5 Annual Budget Utilization

**Display:** Two-panel section.

**Left — Donut Chart (Chart.js 4.x):** Three segments — Disbursed (green) · Committed/Approved but not disbursed (amber) · Remaining (grey). Centre label: total annual budget (₹).

**Right — Table breakdown by scheme type:**

| Scheme Type | Budget (₹) | Approved YTD (₹) | Disbursed YTD (₹) | Remaining (₹) | Utilized % |
|---|---|---|---|---|---|
| Merit | ... | ... | ... | ... | ... |
| Need-based | ... | ... | ... | ... | ... |
| Government | ... | ... | ... | ... | ... |
| Group-Special | ... | ... | ... | ... | ... |

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-disbursement/stats/budget-utilization/`.

---

### 5.6 Renewal Disbursement Schedule

**Display:** Calendar list — upcoming recurring scholarship renewals with disbursement due dates. Sorted by due_date ASC.

**Columns:** Student Name · Branch · Scheme · Renewal Term · Disbursement Due Date · Type · Amount · Days Until Due (amber if < 14) · `[View →]`

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-disbursement/renewal-schedule/` targeting `#renewal-schedule`.

**Empty State:** No upcoming renewal disbursements. Heading: "No Upcoming Renewals."

---

## 6. Drawers & Modals

### 6.1 Disbursement Detail Drawer
- **Width:** 560px
- **Trigger:** `[Receipt →]` in history table or `[View →]`
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-disbursement/records/{disbursement_id}/detail/`
- **Content:** Student name, branch, scheme, approved amount, disbursed amount, disbursement type, mode, reference number, disbursed by, date, approval chain summary. Download receipt PDF button.
- **Footer:** `[Download Receipt PDF]` · `[Close]`

### 6.2 Government Grant Detail Drawer
- **Width:** 480px
- **Trigger:** `[View Details →]` in Section 5.4
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-disbursement/govt-grants/{grant_id}/detail/`
- **Content:** Scheme details, students list (name, amount due), claim submission history (dates, portal ref numbers), government acknowledgements, received disbursements by date, reconciliation table (submitted vs received). Update field for new reference numbers.
- **Submit updates:** `hx-put` → `/api/v1/group/{group_id}/adm/scholarship-disbursement/govt-grants/{grant_id}/`

### 6.3 Mark Disbursed Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Mark Disbursed →]` on queue row
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-disbursement/queue/{disbursement_id}/mark-disbursed-modal/`
- **Content:** Student name, scheme, approved amount (read-only), Actual amount disbursed (editable — may differ if partial), Mode (dropdown), Reference number (text), Disbursement date (datepicker), Remarks (optional textarea). `[Confirm Disbursement]` + `[Cancel]`
- **Submit:** `hx-post` → `/api/v1/group/{group_id}/adm/scholarship-disbursement/queue/{disbursement_id}/mark-disbursed/` · updates row to Completed, moves to history

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Disbursement marked | "Disbursement recorded for {Student Name} — ₹{amount} via {mode}." | Success | 4 s |
| Escalation sent | "Disbursement for {Student Name} escalated to Finance Manager." | Info | 4 s |
| Govt grant updated | "Government grant record updated — reference {ref}." | Success | 3 s |
| Budget threshold alert | "Scholarship budget is now {n}% utilized." | Warning | 5 s |
| Export report queued | "Disbursement report is being prepared." | Info | 3 s |
| Receipt download ready | "Receipt PDF ready. Download starting." | Info | 3 s |
| Partial disbursement recorded | "Partial disbursement of ₹{amount} recorded. ₹{remaining} still pending." | Warning | 5 s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No pending disbursements | Check-circle icon | "All Scholarships Disbursed" | "No approved scholarships are awaiting disbursement." | None |
| No disbursement history | History icon | "No Disbursement History" | "Disbursement records will appear here once scholarships are processed." | None |
| No government grants | Building icon | "No Government Grants" | "No NSP, PMSS, or state scholarship grants are currently tracked." | None |
| No upcoming renewals | Calendar icon | "No Upcoming Renewals" | "No recurring scholarship renewals are scheduled." | None |
| Filter returns no results | Filter icon | "No Records Match Filters" | "Adjust filter criteria to see records." | `[Clear Filters]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | KPI shimmer (6 cards) + queue table skeleton (8 rows) |
| KPI auto-refresh | In-place spinner per card |
| Queue filter change | Table skeleton (8 row shimmer) |
| History filter change | Table skeleton (8 row shimmer) |
| Monthly chart load | Chart.js bar loading animation in canvas |
| Budget donut load | Donut chart shimmer + table skeleton |
| Govt grant table load | Table skeleton (4 row shimmer) |
| Renewal schedule load | List skeleton (5 item shimmers) |
| Disbursement detail drawer open | 560px drawer skeleton |
| Govt grant detail drawer open | 480px drawer skeleton with table shimmer |
| Mark disbursed modal open | 400px modal with form field shimmers |
| Mark disbursed submit | Row spinner + "Recording disbursement…" |

---

## 10. Role-Based UI Visibility

| Element | Scholarship Mgr (27) | CFO | Finance Mgr | Director (23) | MIS |
|---|---|---|---|---|---|
| `[Mark Disbursed →]` button | Hidden | Visible | Visible | Hidden | Hidden |
| `[Escalate →]` button | Visible | Hidden | Hidden | Hidden | Hidden |
| Mark disbursed modal | No access | Full | Full | No access | No access |
| Govt grant detail (edit) | Read only | Full | Partial | Read only | Read only |
| Section 5.5 budget breakdown | Visible | Visible | Visible | Visible | Visible |
| `[Export Disbursement Report]` | Visible | Visible | Visible | Visible | Visible |
| `[Download Govt Claim Summary]` | Visible | Visible | Visible | Visible | Hidden |
| Disbursement history (all) | Visible | Visible | Branch-scoped | Visible | Visible |
| Receipt download | Visible | Visible | Visible | Visible | Hidden |

*All UI visibility decisions made server-side in Django template. No client-side JS role checks.*

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/kpis/` | JWT G3 | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/queue/` | JWT G3 | Paginated disbursement queue |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/queue/{disbursement_id}/mark-disbursed-modal/` | JWT CFO/FM | Mark disbursed modal fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-disbursement/queue/{disbursement_id}/mark-disbursed/` | JWT CFO/FM | Mark as disbursed |
| POST | `/api/v1/group/{group_id}/adm/scholarship-disbursement/queue/{disbursement_id}/escalate/` | JWT Scholarship Mgr | Escalate to Finance |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/history/` | JWT G3 | Disbursement history (paginated) |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/records/{disbursement_id}/detail/` | JWT G3 | Disbursement detail drawer |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/stats/monthly/` | JWT G3 | Monthly disbursement chart data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/govt-grants/` | JWT G3 | Govt grant tracker table |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/govt-grants/{grant_id}/detail/` | JWT G3 | Govt grant detail drawer |
| PUT | `/api/v1/group/{group_id}/adm/scholarship-disbursement/govt-grants/{grant_id}/` | JWT CFO/FM | Update govt grant record |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/stats/budget-utilization/` | JWT G3 | Budget utilization chart + table |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/renewal-schedule/` | JWT G3 | Upcoming renewal schedule |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/export/report/` | JWT G3 | Export disbursement report |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/export/govt-claim-summary/` | JWT G3 | Govt claim summary download |
| GET | `/api/v1/group/{group_id}/adm/scholarship-disbursement/records/{disbursement_id}/receipt/` | JWT G3 | Download receipt PDF |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `.../scholarship-disbursement/kpis/` | `#kpi-bar` | `innerHTML` |
| Filter disbursement queue | `change` on filter inputs | GET `.../scholarship-disbursement/queue/?{filters}` | `#disbursement-queue-body` | `innerHTML` |
| Paginate queue | `click` on page link | GET `.../scholarship-disbursement/queue/?page={n}` | `#disbursement-queue-container` | `innerHTML` |
| Open mark-disbursed modal | `click` on `[Mark Disbursed →]` | GET `.../scholarship-disbursement/queue/{id}/mark-disbursed-modal/` | `#modal-container` | `innerHTML` |
| Submit mark disbursed | `submit` on modal form | POST `.../scholarship-disbursement/queue/{id}/mark-disbursed/` | `#queue-row-{id}` | `outerHTML` |
| Escalate disbursement | `click` on `[Escalate →]` | POST `.../scholarship-disbursement/queue/{id}/escalate/` | `#queue-row-{id}` | `outerHTML` |
| Filter disbursement history | `change` on history filters | GET `.../scholarship-disbursement/history/?{filters}` | `#disbursement-history-body` | `innerHTML` |
| Paginate history | `click` on page link | GET `.../scholarship-disbursement/history/?page={n}` | `#disbursement-history-container` | `innerHTML` |
| Open disbursement detail drawer | `click` on `[Receipt →]` / `[View →]` | GET `.../scholarship-disbursement/records/{id}/detail/` | `#drawer-container` | `innerHTML` |
| Load monthly chart | `load` on chart section | GET `.../scholarship-disbursement/stats/monthly/` | `#monthly-chart-data` | `innerHTML` |
| Load govt grant table | `load` on section | GET `.../scholarship-disbursement/govt-grants/` | `#govt-grant-table` | `innerHTML` |
| Open govt grant detail drawer | `click` on `[View Details →]` | GET `.../scholarship-disbursement/govt-grants/{id}/detail/` | `#drawer-container` | `innerHTML` |
| Submit govt grant update | `submit` on grant form | PUT `.../scholarship-disbursement/govt-grants/{id}/` | `#govt-grant-row-{id}` | `outerHTML` |
| Load budget utilization | `load` on section | GET `.../scholarship-disbursement/stats/budget-utilization/` | `#budget-utilization-section` | `innerHTML` |
| Load renewal schedule | `load` on section | GET `.../scholarship-disbursement/renewal-schedule/` | `#renewal-schedule` | `innerHTML` |
| Refresh KPIs after disbursement | `htmx:afterRequest` from mark-disbursed call | GET `.../scholarship-disbursement/kpis/` | `#kpi-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
