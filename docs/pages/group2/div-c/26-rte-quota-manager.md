# Page 26: RTE Quota Manager

**URL:** `/group/adm/rte-quota/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions · Scholarship Section

---

## 1. Purpose

The Right to Education Act (RTE), 2009, mandates that every private unaided school in India reserve 25% of seats in the entry-level class (Class 1 or Pre-Primary) for children from Economically Weaker Sections (EWS) and Disadvantaged Groups (DG). Failure to comply can result in regulatory penalties, denial of school recognition renewal, or CBSE affiliation cancellation — making this one of the highest-stakes compliance obligations for the group. The RTE Quota Manager provides a centralised, group-wide view of compliance status for every branch, manages the student registry, facilitates the government-mandated lottery process where applicable, and tracks reimbursement claims from state and central governments.

Each branch that admits RTE students is entitled to reimbursement from the government at a per-student rate set by the state education department. This rate is typically based on a government-calculated per-pupil expenditure figure and is paid annually or per term. The group must submit claims on behalf of each branch to the state portal, maintain supporting documentation for each RTE student, and ensure that eligible students' families hold valid EWS or DG certificates. Documentation compliance is tracked in Section 5.5 — any student with expired or missing certificates creates a reimbursement risk and a compliance audit risk.

The lottery process is relevant in branches where the number of applicants for RTE seats exceeds the number of seats available. In such cases, the RTE rules require a draw-of-lots conducted in the presence of a government official. The Lottery Process Manager (Section 5.3) facilitates recording of applicants, the draw, and result communication. Most branches will not need the lottery, but it must be available for the few that are oversubscribed. State-wise compliance reporting is provided for groups that operate across multiple states with different RTE reimbursement rates and compliance definitions.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Manager (27) | G3 | Full — compliance management, document tracking, RTE registry, lottery | Primary owner including RTE scope |
| Group Admissions Director (23) | G3 | View + override + approve branch additions | Cannot edit compliance records directly |
| Group Admission Coordinator (24) | G3 | View only — all branches | No edit |
| Legal/Compliance Officer | G2 | View all — compliance audit | Read-only across all branches |
| Chief Financial Officer | G1 | Reimbursement section — full access | Finance scope only |
| Branch Principal | Branch | View and update own branch RTE records | Branch-scoped |

**Enforcement:** `@role_required(['scholarship_manager', 'admissions_director', 'coordinator', 'compliance_officer', 'cfo', 'principal'])`. Scholarship Manager has group-wide write access. Branch Principal is scoped via `branch == request.user.branch` at queryset level. CFO can only access reimbursement endpoints. Legal Officer gets read-only template (`rte_readonly=True`).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarships → RTE Quota Manager
```

### 3.2 Page Header
- **Title:** RTE Quota Manager
- **Subtitle:** Right to Education Act compliance — 25% seat reservation mandate
- **Action Buttons:** `[Export Compliance Report]` · `[Download Reimbursement Claim PDF]` · `[+ Add RTE Student]` (Scholarship Manager only)
- **Compliance Summary Chip:** "X/Y branches compliant" — green if X = Y, amber if partial, red if < 75% of Y

### 3.3 Alert Banner
Triggers:
- **Red — Non-compliant Branches:** "{n} branches are non-compliant (< 25% RTE seats filled). Risk of regulatory action. [View →]"
- **Red — Document Risk:** "{n} RTE students have expired or missing EWS/DG certificates. [Fix Now →]"
- **Amber — Reimbursement Claim Due:** "Annual reimbursement claim for AY 2025-26 has not been submitted to the state government. Deadline: {date}. [Submit →]"
- **Amber — Lottery Required:** "{n} branches have more RTE applicants than seats and lottery has not been conducted. [Schedule Lottery →]"
- **Blue — Admission Season Reminder:** "RTE admissions for AY 2026-27 open on {date}. Ensure all branches have updated seat counts."

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Branches Compliant | COUNT where rte_compliance_status = 'compliant' | `rte_compliance` | Green if = total branches · Amber partial · Red if < 75% | → Section 5.1 filtered compliant |
| Branches Non-Compliant | COUNT where compliance_pct < 100 | `rte_compliance` | Red > 0 · Green = 0 | → Section 5.1 filtered non-compliant |
| Total RTE Students (Group) | COUNT of active `rte_student` records across all branches | `rte_student` | Blue always | → Section 5.2 |
| Reimbursement Claims Submitted | COUNT of claim submissions in current year | `rte_reimbursement` | Blue always | → Section 5.4 |
| Reimbursement Received (₹) | SUM of received_amount from `rte_reimbursement` | `rte_reimbursement` | Green always | → Section 5.4 |
| Students with Incomplete Documents | COUNT where any required doc status = 'missing' or 'expired' | `rte_document` | Red > 0 · Green = 0 | → Section 5.5 |

**HTMX Refresh:** Every 5 minutes via `hx-trigger="every 5m"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 RTE Compliance Table

**Display:** Sortable, server-side paginated (20/page). One row per branch. Default sort: compliance_pct ASC (non-compliant first).

**Columns:**

| Column | Notes |
|---|---|
| Branch | Branch name + city + state |
| Total Class 1 Seats | Integer |
| 25% Mandated | Calculated: floor(total × 0.25) |
| RTE Enrolled | Count of active RTE students in Class 1 this year |
| % Compliance | (enrolled / mandated) × 100 |
| Lottery Conducted | Yes (green ✓) / No (grey –) / Required (amber — oversubscribed) |
| Documents Verified | All verified (green) / Partial (amber) / None (red) |
| Reimbursement Submitted | Yes (green) / No (red) for current year |
| Reimbursement Received | ₹ amount or "Pending" |
| Status | Compliant (green) / Partial (amber) / Non-compliant (red) |
| Actions | `[View →]` · `[Edit →]` (Scholarship Manager / Principal) |

**Colour:** Row background: green (compliant) · amber (partial 75–99%) · red (< 75%)

**Filters:** Compliance status (Compliant / Partial / Non-compliant), District/State

**HTMX Pattern:** Filter changes → `GET /api/v1/group/{group_id}/adm/rte-quota/compliance/` targeting `#compliance-table-body`.

**Empty State:** No branches configured. CTA: `[Configure Branches]`.

---

### 5.2 RTE Student Registry

**Display:** Paginated table (20/page). All active RTE students across all branches. Default sort: admission_date DESC.

**Columns:**

| Column | Notes |
|---|---|
| Student Name | Full name |
| Branch | Branch name |
| Class | Current class |
| Year of Admission | Academic year |
| EWS/DG Certificate Status | Valid (green) / Expiring within 90 days (amber) / Expired (red) / Missing (red ✗) |
| Income Proof Status | Valid / Expired / Missing — same colour logic |
| Address Proof Status | Valid / Expired / Missing |
| Admission Date | DD-MMM-YYYY |
| Actions | `[View Documents →]` (opens rte-student-detail drawer) |

**Filters:** Branch, Document status (any issue / all complete)

**HTMX Pattern:** Filter changes → `GET /api/v1/group/{group_id}/adm/rte-quota/students/` targeting `#rte-student-table-body`.

**Empty State:** No RTE students registered. Heading: "No RTE Students Registered."

---

### 5.3 Lottery Process Manager

**Display:** Accordion section — one card per branch that has more RTE applicants than seats (oversubscribed). Collapsed branches that are not oversubscribed.

**Card per oversubscribed branch:**
- Branch name · Total RTE seats · Total applicants · Status chip (Lottery Not Scheduled / Lottery Scheduled / Completed)
- Action buttons: `[Schedule Lottery →]` · `[Record Applicants →]` · `[Conduct Draw →]` · `[Record Results →]` · `[Issue Admission Letters →]`
- Steps are sequential — next step only enabled after previous is completed.

**Lottery Steps (sequential, tracked):**
1. Record applicants (upload or manual entry)
2. Schedule draw date/time (with government official confirmation note)
3. Conduct draw (system-assisted random selection — `[Run Random Draw]`)
4. Record results (selected candidates list)
5. Issue admission letters to selected candidates

**HTMX Pattern:** Each step action posts to respective endpoint and refreshes the branch card via `hx-swap="outerHTML"` on the card element.

**Empty State:** No branches are oversubscribed for RTE seats. Heading: "No Lottery Required."

---

### 5.4 Government Reimbursement Tracker

**Display:** Table — one row per branch with RTE students.

**Columns:**

| Column | Notes |
|---|---|
| Branch | Branch name |
| Students (RTE) | Count |
| Per-Student Rate (₹) | State-set reimbursement rate |
| Total Claimable (₹) | Students × rate |
| Claimed (₹) | Amount submitted in claim |
| Received from Govt (₹) | Amount received |
| Transferred to School (₹) | Amount credited to school |
| Pending (₹) | Claimable – Received — red if > 0 |

**Footer row:** Group totals for all ₹ columns.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/rte-quota/reimbursement/` targeting `#reimbursement-table`.

---

### 5.5 Document Verification Queue

**Display:** Alert list — RTE students with incomplete, expired, or missing documents. Sorted by branch, then student name.

**Columns:** Student Name · Branch · Class · Missing Docs (comma-separated: EWS cert / Income proof / Address proof) · `[Send Reminder →]` · `[View →]`

**`[Send Reminder →]`:** Sends WhatsApp notification to branch (not parent directly) prompting document collection. Logs the reminder with timestamp.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/rte-quota/document-queue/` targeting `#doc-verification-queue`. Auto-refreshes every 5 minutes.

**Empty State:** No document issues. Icon: file-check. Heading: "All Documents Complete."

---

### 5.6 State-wise Compliance Report

**Display:** Table — visible only for groups operating in multiple states.

**Columns:** State · Branches (count) · Compliant Branches · Non-compliant Branches · Total RTE Students · Claim Status (Submitted/Not submitted) · Avg Compliance %

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/rte-quota/state-compliance/` targeting `#state-compliance-table`.

**Empty State:** Group operates in a single state — section hidden.

---

## 6. Drawers & Modals

### 6.1 RTE Student Detail Drawer
- **Width:** 640px
- **Trigger:** `[View Documents →]` in Section 5.2 or `[View →]` in compliance table
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/rte-quota/students/{student_id}/detail/`
- **Tabs:**
  1. **Student Profile** — Name, DOB, class, branch, parent details, EWS/DG category
  2. **EWS Documents** — EWS certificate (preview), expiry date, issuing authority; DG certificate if applicable
  3. **Admission Details** — Year of admission, seat type, lottery reference if applicable, admission letter
  4. **Reimbursement Status** — This student's share in branch reimbursement claim — claimed/received status

### 6.2 Lottery Manager Drawer
- **Width:** 560px
- **Trigger:** Any lottery step button in Section 5.3
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/rte-quota/lottery/{branch_id}/{step}/`
- **Content varies by step:**
  - Step 1: Applicant upload (CSV) or manual entry form
  - Step 2: Date/time/government official name for the draw
  - Step 3: [Run Draw] button — system picks random candidates up to seat count; shows selected + waitlist
  - Step 4: Review results, add notes, confirm
  - Step 5: Preview admission letter template; [Send Letters] bulk action

### 6.3 Reimbursement Claim Drawer
- **Width:** 480px
- **Trigger:** `[Submit Claim →]` or `[View Details →]` in Section 5.4
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/rte-quota/reimbursement/{branch_id}/claim/`
- **Content:** Claim summary (students, amount, rate), claim period, supporting document checklist, government portal submission reference number field, submission date. `[Mark as Submitted]` button.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| RTE student added | "RTE student {Name} registered for {Branch}." | Success | 4 s |
| Document reminder sent | "Document reminder sent to {Branch} for {n} students." | Info | 4 s |
| Lottery draw completed | "Lottery completed for {Branch}: {n} students selected, {m} on waitlist." | Success | 5 s |
| Admission letters sent | "Admission letters sent to {n} selected RTE candidates at {Branch}." | Success | 4 s |
| Reimbursement claim submitted | "Reimbursement claim marked as submitted for {Branch}. Reference: {ref}." | Success | 4 s |
| Compliance report exported | "Compliance report PDF is being prepared." | Info | 3 s |
| Branch RTE record updated | "RTE record updated for {Branch}." | Success | 3 s |
| Document expiry alert | "3 EWS certificates at {Branch} expire within 90 days." | Warning | 5 s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No branches configured | Building-x icon | "No Branches Configured" | "Configure branch seat counts to begin RTE compliance tracking." | `[Configure Branches]` |
| No RTE students | Users icon | "No RTE Students Registered" | "Add RTE students for branches to begin tracking." | `[+ Add RTE Student]` |
| No lottery required | Ticket icon | "No Lottery Required" | "No branch has more RTE applicants than available seats." | None |
| No document issues | File-check icon | "All Documents Complete" | "All RTE students have valid and complete documents." | None |
| Single state (5.6 hidden) | — | — | Section hidden — not applicable | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | KPI shimmer (6 cards) + compliance table skeleton (8 rows) |
| KPI auto-refresh | In-place spinner per card |
| Compliance table filter change | Table skeleton (8 row shimmer) |
| RTE student registry load | Table skeleton (10 row shimmer) |
| Student registry filter change | Table skeleton (10 row shimmer) |
| Reimbursement tracker load | Table skeleton (6 row shimmer) |
| Document queue load | List skeleton (5 row shimmers) |
| Document queue auto-refresh | Subtle shimmer overlay on list |
| State compliance table load | Table skeleton (4 row shimmer) |
| RTE student detail drawer | 640px drawer with 4 tab shimmers |
| Lottery manager drawer | 560px drawer with step content shimmer |
| Reimbursement claim drawer | 480px drawer form skeleton |
| Lottery draw in progress | Animated spinner with "Conducting draw…" |

---

## 10. Role-Based UI Visibility

| Element | Scholarship Mgr (27) | Director (23) | Coordinator (24) | Compliance Officer | CFO | Principal |
|---|---|---|---|---|---|---|
| `[+ Add RTE Student]` | Visible | Hidden | Hidden | Hidden | Hidden | Visible (own branch) |
| `[Edit →]` compliance row | Visible | Hidden | Hidden | Hidden | Hidden | Visible (own branch) |
| Section 5.3 Lottery | Visible (full) | Visible (view) | Visible (view) | Visible (view) | Hidden | Visible (own branch) |
| `[Schedule Lottery →]` | Visible | Hidden | Hidden | Hidden | Hidden | Visible (own branch) |
| Section 5.4 Reimbursement | Visible | Visible | Visible (view) | Visible | Visible (full) | Visible (own branch) |
| `[Mark as Submitted]` (claim) | Visible | Hidden | Hidden | Hidden | Visible | Hidden |
| Section 5.5 Doc Queue | Visible (full) | Visible (read) | Visible (read) | Visible (read) | Hidden | Visible (own branch) |
| `[Send Reminder →]` | Visible | Hidden | Hidden | Hidden | Hidden | Visible (own branch) |
| Section 5.6 State Compliance | Visible | Visible | Visible | Visible | Visible | Hidden |
| `[Export Compliance Report]` | Visible | Visible | Visible | Visible | Hidden | Hidden |
| `[Download Reimbursement Claim PDF]` | Visible | Visible | Hidden | Hidden | Visible | Hidden |

*All UI visibility decisions made server-side in Django template. No client-side JS role checks.*

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/rte-quota/kpis/` | JWT G3 | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/rte-quota/compliance/` | JWT G3 | Compliance table (paginated, filtered) |
| PUT | `/api/v1/group/{group_id}/adm/rte-quota/compliance/{branch_id}/` | JWT G3 write | Update branch RTE record |
| GET | `/api/v1/group/{group_id}/adm/rte-quota/students/` | JWT G3 | RTE student registry (paginated) |
| POST | `/api/v1/group/{group_id}/adm/rte-quota/students/` | JWT G3 write | Add RTE student |
| GET | `/api/v1/group/{group_id}/adm/rte-quota/students/{student_id}/detail/` | JWT G3 | Student detail drawer fragment |
| PUT | `/api/v1/group/{group_id}/adm/rte-quota/students/{student_id}/` | JWT G3 write | Update student record |
| GET | `/api/v1/group/{group_id}/adm/rte-quota/lottery/{branch_id}/{step}/` | JWT G3 | Lottery step drawer fragment |
| POST | `/api/v1/group/{group_id}/adm/rte-quota/lottery/{branch_id}/draw/` | JWT G3 write | Execute random lottery draw |
| POST | `/api/v1/group/{group_id}/adm/rte-quota/lottery/{branch_id}/complete/` | JWT G3 write | Complete lottery and record results |
| POST | `/api/v1/group/{group_id}/adm/rte-quota/lottery/{branch_id}/send-letters/` | JWT G3 write | Send admission letters |
| GET | `/api/v1/group/{group_id}/adm/rte-quota/reimbursement/` | JWT G3 | Reimbursement tracker table |
| GET | `/api/v1/group/{group_id}/adm/rte-quota/reimbursement/{branch_id}/claim/` | JWT G3 | Claim drawer fragment |
| POST | `/api/v1/group/{group_id}/adm/rte-quota/reimbursement/{branch_id}/claim/submit/` | JWT G3/CFO | Mark claim as submitted |
| GET | `/api/v1/group/{group_id}/adm/rte-quota/document-queue/` | JWT G3 | Document verification queue |
| POST | `/api/v1/group/{group_id}/adm/rte-quota/document-queue/{student_id}/send-reminder/` | JWT G3 write | Send document reminder |
| GET | `/api/v1/group/{group_id}/adm/rte-quota/state-compliance/` | JWT G3 | State-wise compliance table |
| GET | `/api/v1/group/{group_id}/adm/rte-quota/export/compliance-report/` | JWT G3 | Export compliance report PDF |
| GET | `/api/v1/group/{group_id}/adm/rte-quota/export/reimbursement-claim/` | JWT G3/CFO | Download reimbursement claim PDF |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `.../rte-quota/kpis/` | `#kpi-bar` | `innerHTML` |
| Filter compliance table | `change` on filter inputs | GET `.../rte-quota/compliance/?{filters}` | `#compliance-table-body` | `innerHTML` |
| Paginate compliance table | `click` on page link | GET `.../rte-quota/compliance/?page={n}` | `#compliance-table-container` | `innerHTML` |
| Open RTE student detail | `click` on `[View Documents →]` | GET `.../rte-quota/students/{id}/detail/` | `#drawer-container` | `innerHTML` |
| Filter student registry | `change` on filter inputs | GET `.../rte-quota/students/?{filters}` | `#rte-student-table-body` | `innerHTML` |
| Paginate student registry | `click` on page link | GET `.../rte-quota/students/?page={n}` | `#rte-student-table-container` | `innerHTML` |
| Open lottery step drawer | `click` on lottery step button | GET `.../rte-quota/lottery/{branch_id}/{step}/` | `#drawer-container` | `innerHTML` |
| Execute lottery draw | `click` on `[Run Random Draw]` | POST `.../rte-quota/lottery/{branch_id}/draw/` | `#lottery-result-area` | `innerHTML` |
| Complete lottery step | `submit` on lottery step form | POST `.../rte-quota/lottery/{branch_id}/complete/` | `#lottery-card-{branch_id}` | `outerHTML` |
| Load reimbursement table | `load` on section | GET `.../rte-quota/reimbursement/` | `#reimbursement-table` | `innerHTML` |
| Open claim drawer | `click` on `[View Details →]` | GET `.../rte-quota/reimbursement/{branch_id}/claim/` | `#drawer-container` | `innerHTML` |
| Submit claim | `click` on `[Mark as Submitted]` | POST `.../rte-quota/reimbursement/{branch_id}/claim/submit/` | `#reimbursement-row-{branch_id}` | `outerHTML` |
| Load document queue | `load` on section | GET `.../rte-quota/document-queue/` | `#doc-verification-queue` | `innerHTML` |
| Doc queue auto-refresh | `every 5m` | GET `.../rte-quota/document-queue/` | `#doc-verification-queue` | `innerHTML` |
| Send doc reminder | `click` on `[Send Reminder →]` | POST `.../rte-quota/document-queue/{id}/send-reminder/` | `#doc-row-{id}` | `outerHTML` |
| Load state compliance | `load` on section | GET `.../rte-quota/state-compliance/` | `#state-compliance-table` | `innerHTML` |
| Refresh KPIs after update | `htmx:afterRequest` from update calls | GET `.../rte-quota/kpis/` | `#kpi-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
