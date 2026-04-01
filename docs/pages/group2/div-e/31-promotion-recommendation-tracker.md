# 31 — Promotion Recommendation Tracker

- **URL:** `/group/hr/promotions/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Director (Role 41, G3)

---

## 1. Purpose

The Promotion Recommendation Tracker manages the end-to-end workflow for staff promotion decisions arising from the annual appraisal cycle. Every promotion recommendation originates at the branch level — the branch principal nominates a staff member for promotion in their appraisal form — and then flows upward: HR Manager reviews eligibility, HR Director makes the final decision. Because promotions directly affect payroll (grade band change and salary increase), they must be fully approved and entered into the system before the new academic year payroll runs in April.

This page enforces four critical pre-approval controls. First, no promotion can be approved if the proposed new grade exceeds the maximum of the grade band without explicit CFO sign-off — this prevents unilateral salary escalation above approved compensation bands. Second, no promotion can be processed if the staff member's BGV is incomplete or flagged — a person with an unresolved background concern cannot be elevated to a senior role. Third, no promotion can proceed if POCSO awareness training has not been completed — a mandatory compliance requirement. Fourth, no promotion can be processed if there is an active disciplinary case against the staff member — the system enforces this as a hard block, not just a warning.

The HR Manager conducts the initial eligibility review: checks that the staff member meets the minimum years-in-grade requirement, that their calibrated appraisal rating qualifies (e.g., rating ≥ 4 for two consecutive cycles), that there is no disciplinary block, and that the proposed grade is within band. This review is submitted to the HR Director who makes the final call: Approve, Decline (with reason communicated to branch principal), or escalate to CFO for above-band approval.

Approved promotions are issued a Promotion Letter (generated from a template), recorded in the staff profile, and the salary change request is created for the Payroll team. All promotion records are permanent and cannot be deleted — they form part of the staff career history.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director | G3 | Full view + Approve / Decline / CFO Escalation | Final approval authority |
| Group HR Manager | G3 | Read + Eligibility Review | Submits eligibility assessment to HR Director |
| Group Performance Review Officer | G1 | Read Only | Views promotion pipeline for context |
| Group Staff Transfer Coordinator | G3 | No Access | Not applicable |
| Branch Principal | Branch G3 | Own branch only — submit recommendation | Cannot see cross-branch promotions |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > Performance Appraisal > Promotion Recommendation Tracker`

### 3.2 Page Header
- **Title:** Promotion Recommendation Tracker
- **Subtitle:** Track and approve staff promotion recommendations across all branches
- **Actions (top-right):**
  - `Export Promotions Report` (CSV/XLSX)
  - `Filter by Stage` (dropdown shortcut)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Promotions pending approval with payroll deadline < 30 days away | "URGENT: Payroll deadline is in [N] days. [N] promotions require HR Director approval to be effective from new AY." | Red — non-dismissible if < 7 days |
| CFO sign-off pending for above-band promotions | "ACTION NEEDED: [N] promotions require CFO sign-off before they can be approved." | Amber — dismissible |
| Any promotion blocked by disciplinary case | "WARNING: [N] recommendations are blocked due to active disciplinary cases." | Amber — dismissible |
| All recommendations resolved | "All promotion recommendations for this cycle have been resolved." | Green — auto-dismiss 10s |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Promotions Recommended | Total recommendations submitted in current cycle | Blue always | No drill-down |
| Pending HR Manager Review | Count at Eligibility Review stage | Amber if > 0 | Filters table to stage |
| Pending HR Director Approval | Count awaiting final decision | Amber if > 0 | Filters table to stage |
| CFO Approval Needed | Count escalated above grade band | Red if > 0 | Filters table to CFO stage |
| Promotions Approved | Count approved this cycle | Green | Filters to Approved |
| Promotions Declined | Count declined this cycle | Red if > 0 | Filters to Declined |

---

## 5. Main Table — Promotion Recommendations

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff Name | Text + avatar | Yes | No |
| From Role | Text | No | No |
| To Role | Text | No | No |
| Branch | Badge | Yes | Yes — dropdown |
| Current Grade | Badge | Yes | Yes — dropdown |
| Proposed Grade | Badge | Yes | No |
| Salary Impact (₹/month) | Currency | Yes | No |
| BGV Status | Icon badge (Clear / Flagged / Pending) | No | Yes — dropdown |
| POCSO Status | Icon badge (Complete / Pending) | No | Yes — dropdown |
| Disciplinary Flag | Icon (warning or check) | No | Yes — Yes/No |
| Status | Badge (Submitted / Under Review / Pending Approval / CFO Pending / Approved / Declined) | No | Yes — multi-select |
| Actions | Icon buttons | No | No |

### 5.1 Filters
- **Branch:** multi-select
- **Stage / Status:** multi-select
- **Proposed Grade:** dropdown
- **Blocking Issues:** BGV Pending / POCSO Pending / Disciplinary Block / Above Band — checkboxes
- **Academic Year:** dropdown

### 5.2 Search
Free-text search on Staff Name, From Role, To Role. Debounced `hx-get` on keyup (400 ms).

### 5.3 Pagination
Server-side, 25 rows per page. Shows `Showing X–Y of Z recommendations`.

---

## 6. Drawers

### 6.1 Create
Not initiated from this page — recommendations come from branch appraisal workflow. This page is the approval interface only.

### 6.2 View Recommendation Details
**Trigger:** Row click or eye icon
**Displays:** Staff profile summary, current role and grade, proposed role and grade, appraisal rating (last 2 cycles), years in current grade, branch principal's nomination text, salary impact calculation (current CTC vs. proposed CTC), BGV status detail, POCSO training date, disciplinary case history (if any), HR Manager eligibility review notes.

### 6.3 Approve Promotion
**Trigger:** Approve button (HR Director only, enabled only when all blocks cleared)
**Fields:**
- Effective Date (date picker, default = new AY start)
- Approval Notes (textarea)
- Auto-generate Promotion Letter (toggle)
- Confirm Approval button → triggers salary change request to Payroll module

### 6.4 Decline Recommendation
**Trigger:** Decline button (HR Director only)
**Fields:**
- Decline Reason (dropdown: Eligibility Not Met / Disciplinary Block / Budget Freeze / Above Band — CFO Required / Other)
- Detailed Notes (textarea, required)
- Notify Branch Principal (toggle, default on)
- Confirm Decline

---

## 7. Charts

**Promotion Pipeline Funnel**
- Stages: Submitted → HR Manager Review → HR Director Approval → CFO (if needed) → Approved / Declined
- Bar length = count at each stage
- Colour: amber for pending stages, green for approved, red for declined

**Promotions by Branch (Horizontal Bar)**
- One bar per branch showing: Approved (green), Pending (amber), Declined (red)
- Useful for spotting branches with disproportionately high recommendation counts

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Promotion approved | "Promotion for [Staff Name] approved. Effective [Date]." | Success | 5s |
| Promotion declined | "Promotion for [Staff Name] declined. Branch principal notified." | Info | 5s |
| CFO escalation created | "Escalation to CFO created for [Staff Name]'s promotion." | Info | 4s |
| Promotion letter generated | "Promotion letter for [Staff Name] generated and saved to profile." | Success | 4s |
| Blocked promotion attempted | "Cannot approve — [Staff Name] has an active disciplinary case / pending BGV / incomplete POCSO training." | Error | 7s |
| Export triggered | "Promotions report export started." | Info | 4s |

---

## 9. Empty States

- **No recommendations this cycle:** "No promotion recommendations have been submitted for the current appraisal cycle."
- **No items match filters:** "No recommendations match the selected filters. Try removing one or more filter conditions."
- **All resolved:** "All promotion recommendations for this cycle have been resolved. No pending actions."

---

## 10. Loader States

- Table skeleton: 6 placeholder rows with shimmer.
- KPI cards: skeleton shimmer on initial load.
- Recommendation view drawer: spinner while full staff and appraisal data loads.
- Chart container: grey placeholder until funnel and branch chart data resolves.

---

## 11. Role-Based UI Visibility

| Element | HR Director (G3) | HR Manager (G3) | Perf. Review Officer (G1) |
|---|---|---|---|
| Approve / Decline buttons | Visible + enabled | Hidden | Hidden |
| Eligibility Review action | Hidden | Visible + enabled | Hidden |
| CFO Escalation button | Visible + enabled | Hidden | Hidden |
| View recommendation details | Visible | Visible | Visible |
| Export button | Visible | Visible | Visible |
| Salary impact column | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/promotions/` | JWT G1+ | List promotion recommendations (paginated) |
| GET | `/api/v1/hr/promotions/{id}/` | JWT G1+ | View full recommendation details |
| PATCH | `/api/v1/hr/promotions/{id}/review/` | JWT G3 HR Manager | Submit eligibility review |
| POST | `/api/v1/hr/promotions/{id}/approve/` | JWT G3 HR Director | Approve promotion |
| POST | `/api/v1/hr/promotions/{id}/decline/` | JWT G3 HR Director | Decline with reason |
| POST | `/api/v1/hr/promotions/{id}/escalate-cfo/` | JWT G3 HR Director | Escalate above-band promotion to CFO |
| GET | `/api/v1/hr/promotions/kpis/` | JWT G1+ | KPI summary data |
| GET | `/api/v1/hr/promotions/charts/pipeline/` | JWT G1+ | Funnel chart data |
| GET | `/api/v1/hr/promotions/charts/by-branch/` | JWT G1+ | Branch breakdown chart data |
| GET | `/api/v1/hr/promotions/export/` | JWT G1+ | Export promotions report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search staff name | keyup changed delay:400ms | GET `/api/v1/hr/promotions/?q={val}` | `#promotions-table-body` | innerHTML |
| Filter change | change | GET `/api/v1/hr/promotions/?{params}` | `#promotions-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/promotions/?page={n}` | `#promotions-table-body` | innerHTML |
| Open view drawer | click | GET `/api/v1/hr/promotions/{id}/` | `#drawer-container` | innerHTML |
| Submit approve form | submit | POST `/api/v1/hr/promotions/{id}/approve/` | `#promotions-table-body` | innerHTML |
| Submit decline form | submit | POST `/api/v1/hr/promotions/{id}/decline/` | `#promotions-table-body` | innerHTML |
| Refresh KPI bar after action | htmx:afterRequest | GET `/api/v1/hr/promotions/kpis/` | `#kpi-bar` | innerHTML |
| Load pipeline chart | load | GET `/api/v1/hr/promotions/charts/pipeline/` | `#chart-pipeline` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
