# 24 — Medical Compliance Report

> **URL:** `/group/health/compliance/`
> **File:** `24-medical-compliance-report.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Medical Coordinator (primary) · Group Emergency Response Officer (emergency compliance columns)

---

## 1. Purpose

Compliance monitoring report covering all health-related regulatory and policy requirements across every branch of the group. The report gives the Medical Coordinator, Group Chairman, and Board a single authoritative view of how well each branch is meeting its health obligations. It also gives the Medical Coordinator the operational tool needed for monthly management review — identifying which branches need intervention, assigning remediation actions, and tracking their resolution.

Ten compliance categories are assessed: Medical Room Operational Status, Doctor Visit Frequency, Medicine Stock, Health Screening Completion, Student Health Records Completeness, Insurance Coverage, First Responder Certification, SOP Distribution and Acknowledgement, Emergency Drill Completion, and Incident Post-Incident Review.

Compliance scores are computed automatically from data in the source modules (Pages 05, 07, 08, 10, 11, 16, 17, 18, 19, 20, 22). Scores update daily. The Medical Coordinator can add remediation actions for failing items and track them to resolution. Remediation actions can be assigned to Branch Principals or Group Coordinators.

The report is also the primary export document for regulatory submissions (e.g., state education board health compliance requirements) and for Board governance review.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Medical Coordinator | G3 | Full view of all 10 compliance categories + manage remediation actions + export | Primary owner |
| Group Emergency Response Officer | G3 | View emergency compliance columns (Categories 7–10) only | Cannot see medical/insurance categories |
| CEO / Chairman | Group | Full view + export | No remediation action management |
| CFO | Group | Insurance Coverage category (Category 6) only | Financial governance |
| Board Member | G1 | Full view; no edit | Governance oversight |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('medical_coordinator', 'emergency_response_officer', 'ceo', 'chairman', 'cfo', 'board_member')`. Category-level visibility enforced server-side: API returns only visible category columns per role. Remediation action create/update restricted to Medical Coordinator.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Medical Compliance Report
```

### 3.2 Page Header
- **Title:** `Medical Compliance Report`
- **Subtitle:** `Group Overall Score: [N]% · [N] Branches Fully Compliant · Last Full Data Sync: [timestamp]`
- **Right controls:** `Advanced Filters` · `Export Compliance Report (PDF/XLSX)` (Medical Coordinator + CEO/Chairman) · `+ Add Remediation Action` (Medical Coordinator)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Group overall compliance < 70% | "⚠ Group health compliance score is critically low at [N]%. Immediate intervention required across [N] branches." | Red |
| Multiple branches with Red score (< 70%) | "[N] branches have overall compliance scores below 70%. Priority review required." | Red |
| Compliance items expiring this month | "⚠ [N] compliance items are expiring this month (e.g., insurance, first responder certs). Renew to maintain scores." | Amber |
| Remediation actions overdue | "[N] remediation action(s) are past their due date and remain unresolved." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Overall Group Health Compliance Score % | Weighted average across all 10 categories × all branches | Green ≥ 90% · Yellow 70–90% · Red < 70% |
| Branches Fully Compliant | Branches with overall score ≥ 90% | Blue; sub-label shows % of total |
| Compliance Items Failing | Count of branch × category cells scoring < 70% | Green = 0 · Yellow 1–10 · Red > 10 |
| Items Expiring This Month | Policies, certifications, SOPs with expiry in current month | Green = 0 · Amber ≥ 1 |
| Remediation Actions Open | Open remediation actions (status = Open or In Progress) | Green = 0 · Amber 1–10 · Red > 10 |
| Last Full Audit Date | Date the Medical Coordinator last ran a formal compliance audit | Blue; amber if > 90 days ago |

---

## 5. Sections

### 5.1 Compliance Matrix (Main Section)

Grid layout:
- **Rows:** All branches (alphabetical by default)
- **Columns:** 10 compliance categories (see below)

**Compliance Categories:**

| # | Category | Source Module | What is Measured |
|---|---|---|---|
| 1 | Medical Room Operational | Page 05 | Room status = Active + at least one nurse assigned + equipment compliance ≥ 80% |
| 2 | Doctor Visit Frequency | Page 07 | Actual visits per week ≥ required minimum (typically ≥ 2 general practitioner visits/week) |
| 3 | Medicine Stock | Page 08 | No critical stock shortages + no expired medicines on hand |
| 4 | Health Screening | Page 11 | All mandatory screening types scheduled and completed for current AY |
| 5 | Student Health Records | Page 10 | ≥ 90% of hostel students with complete health records; ≥ 80% of day scholars |
| 6 | Insurance Coverage | Pages 16, 17 | At least one active policy covering all students at this branch |
| 7 | First Responders | Page 22 | ≥ 5 certified first responders with valid certifications |
| 8 | SOPs | Page 18 | All mandatory SOPs (Medical Emergency + Fire + Natural Disaster) distributed to branch + acknowledged by Principal |
| 9 | Drills | Page 19 | All 4 mandatory drill types completed at least the required number of times this AY |
| 10 | Incident Review | Page 20 | All incidents closed in last 6 months have a completed post-incident review |

**Cell content:**
- Score percentage (e.g., "87%") shown inside each cell
- Cell background colour:
  - Green (≥ 90%): fully compliant
  - Yellow (70–89%): partially compliant
  - Red (< 70%): non-compliant
  - Grey (N/A): not applicable for this branch (e.g., no hostel = some categories not applicable)

**Row summary:**
- Rightmost column: **Overall Score** (weighted average of applicable categories) with colour
- Row sorted by Overall Score ascending by default (worst first for intervention targeting)

**Cell interaction:**
- Click any cell → expands to show specific gap details inline (HTMX partial)
- OR opens `branch-compliance-detail` drawer pre-filtered to that category

---

### 5.2 Compliance Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Compliance Category | Checkbox | All 10 categories |
| Score Band | Radio | All / Green (≥ 90%) / Yellow (70–89%) / Red (< 70%) |
| Zone | Multi-select | Group's geographical zones (if configured) |

Filters apply to the compliance matrix (hides/shows rows based on selected branches + highlights failing categories).

---

### 5.3 Per-Branch Detail (drill-down from branch name)

Opens `branch-compliance-detail` drawer. See Section 6.1.

---

### 5.4 Historical Compliance Trend (Chart Panel)

Positioned below the compliance matrix.

**Chart 1 — Group Overall Compliance Score by Month (Line Chart)**
- X-axis: Month (last 12 months)
- Y-axis: Compliance score % (0–100)
- Single line: group overall average
- Benchmark line at 90% (fully compliant threshold)
- Hover: exact score + month

**Chart 2 — Top 5 and Bottom 5 Branch Trend Lines**
- X-axis: Month (last 12 months)
- Y-axis: Compliance score %
- Lines: top 5 branches (green shades) + bottom 5 branches (red shades)
- Toggle: show top 5 / bottom 5 / both
- Hover: branch name + score

Download both charts as PNG or CSV.

---

### 5.5 Remediation Actions List (below trend chart)

Filterable list of all open and recently closed remediation actions.

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | |
| Compliance Category | ✅ | |
| Action Description | ❌ | What needs to be done |
| Assigned To | ✅ | Branch Principal / Group Coordinator name |
| Due Date | ✅ | Red if past due |
| Priority | ✅ | High / Medium / Low badge |
| Status | ✅ | Open / In Progress / Done — badge |
| Escalated | ❌ | Yes / No |
| Actions | ❌ | View · Edit · Mark Done · Escalate |

Filter: Status (checkbox: Open / In Progress / Done), Priority (checkbox), Branch (multi-select), Category (checkbox).
Pagination: 25/page.

---

## 6. Drawers / Modals

### 6.1 Drawer — `branch-compliance-detail` (720px, right side)

Triggered by clicking branch name in compliance matrix or **View Records** from matrix row.

**Tabs:**

#### Tab 1 — Summary

| Field | Notes |
|---|---|
| Branch Name | |
| Overall Compliance Score | Large number display; colour-coded |
| Rank Among All Branches | e.g., "12th of 45 branches" |
| Items Passing (count) | Categories with score ≥ 90% |
| Items Partially Compliant (count) | Score 70–89% |
| Items Failing (count) | Score < 70% |
| Trend vs Last Month | Arrow + % point change; e.g., "↑ +3.2% vs last month" |

Summary grid of all 10 categories with score badge for quick visual scan.

#### Tab 2 — Item Details

Full detail for each of the 10 compliance items:

| Field | Notes |
|---|---|
| Category | |
| Score | % |
| Specific Gap | Descriptive gap: e.g., "Doctor Visit Frequency — 1.4 visits/week (required: 2.0)" |
| Evidence | Link to source record (e.g., link to doctor visit schedule for this branch in Page 07) |
| Last Checked Date | When data was last synced from source module |
| Issue | Concise issue description |
| Recommended Action | What the Medical Coordinator recommends to fix this |
| Responsible | Branch Principal or specific role |
| Due Date | Target resolution date |
| Status | Current status of the gap |

Each item row has: **+ Add Remediation Action** button (Medical Coordinator only).

#### Tab 3 — Remediation Plan

All remediation actions for this branch:

| Column | Notes |
|---|---|
| Compliance Item | Which of the 10 categories |
| Action | Description |
| Assigned To | |
| Due Date | Red if past due |
| Priority | |
| Status | Open / In Progress / Done |
| Escalated | Yes / No |
| Actions | Edit · Mark Done · Escalate |

Add new action via **+ Add Action** at top of tab.

#### Tab 4 — History

Compliance scores by month for this branch (last 12 months):

| Column | Notes |
|---|---|
| Month | |
| Overall Score | |
| Category 1–10 Scores | Individual columns for each category |

Line chart: this branch's overall score over 12 months vs group average.

---

### 6.2 Modal — `add-remediation-action` (480px, centred)

Triggered by **+ Add Remediation Action** in Item Details tab or **+ Add Remediation Action** in page header.

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select (auto-filled if opened from branch drawer) | Required |
| Compliance Item | Single-select: dropdown of 10 compliance categories | Required |
| Action Description | Textarea (max 500 chars) | Required |
| Assigned To | Radio: Branch Principal / Group Medical Coordinator / Group Emergency Response Officer | Required |
| Assigned To (name) | Autocomplete from relevant role users | Required |
| Due Date | Date picker | Required |
| Priority | Radio: High / Medium / Low | Required |
| Notes | Textarea (max 300 chars) | Optional |

**Footer:** `Cancel` · `Add Action`

---

### 6.3 Modal — `mark-item-compliant` (440px, centred)

Triggered by **Mark Done** action on a remediation action row. Used to record that a compliance gap has been resolved.

| Field | Type | Validation |
|---|---|---|
| Compliance Item | Read-only | |
| Branch | Read-only | |
| Action Completed | Textarea (max 300 chars) — describe what was done | Required |
| Evidence Description | Textarea (max 300 chars) | Required |
| Verified By | Text input | Required |
| Verification Date | Date picker (default: today) | Required |

**Footer:** `Cancel` · `Mark as Resolved`

On save: remediation action status = Done; compliance matrix cell re-scored from source data; historical log entry created.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Remediation action added | "Remediation action added for [Branch] — [Category]." | Success |
| Remediation action updated | "Remediation action updated." | Success |
| Remediation action marked done | "Remediation action marked as resolved. Compliance score will update on next sync." | Success |
| Compliance item marked compliant | "[Category] compliance item for [Branch] marked as resolved." | Success |
| Export initiated | "Compliance report export initiated. You will be notified when ready." | Info |
| Export ready | "Your compliance report is ready. [Download]" | Success (persistent) |
| Export failed | "Export failed. Please retry." | Error |
| Data sync note | "Compliance scores are updated daily. Last sync: [timestamp]." | Info (dismissable on first login each day) |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No compliance data | "Compliance data is not yet available." | "Data will populate once source modules (medical rooms, doctor visits, etc.) have entries." | — |
| No branches fail compliance | "All branches are fully compliant." | "All branches are scoring ≥ 90% across all health compliance categories. Excellent work." | — |
| No remediation actions | "No open remediation actions." | "All compliance gaps have been resolved or no actions have been created yet." | `+ Add Remediation Action` |
| No results for matrix filters | "No branches match your current filters." | "Try adjusting the score band or branch filters." | `Clear Filters` |
| Branch detail — history tab no data | "No historical compliance data for this branch." | "Monthly scores will accumulate from this point forward." | — |
| Remediation list — filtered to empty | "No remediation actions match your filters." | "Try clearing the status or priority filters." | `Clear Filters` |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 6 KPI cards + compliance matrix (10 grey columns × 10 grey rows) |
| Compliance matrix load | Matrix cells load row by row with progressive fill; spinner on each row until score computed |
| Filter apply | Matrix rows filtered; spinner overlay on matrix during reload |
| Branch compliance detail drawer open | Drawer skeleton: 4 tab headers + summary grid placeholder |
| Item Details tab load | List skeleton (10 grey rows — one per compliance item) |
| Remediation Plan tab load | Table skeleton (3 grey rows) |
| History tab load | Chart skeleton + table skeleton |
| Trend charts load | Chart area spinner overlay |
| Remediation list load | Table skeleton (5 grey rows × 8 columns) |
| Export job | Export button spinner; replaced by "Preparing…" then download link |
| Mark as resolved modal submit | Modal footer spinner + "Updating compliance scores…" |

---

## 10. Role-Based UI Visibility

| UI Element | Medical Coordinator | Emergency Response Officer | CEO / Chairman | CFO | Board Member |
|---|---|---|---|---|---|
| Full compliance matrix (all 10 categories) | ✅ | Categories 7–10 only | ✅ | Category 6 only | ✅ |
| Category 1: Medical Room | ✅ | ❌ | ✅ | ❌ | ✅ |
| Category 2: Doctor Visit | ✅ | ❌ | ✅ | ❌ | ✅ |
| Category 3: Medicine Stock | ✅ | ❌ | ✅ | ❌ | ✅ |
| Category 4: Health Screening | ✅ | ❌ | ✅ | ❌ | ✅ |
| Category 5: Health Records | ✅ | ❌ | ✅ | ❌ | ✅ |
| Category 6: Insurance Coverage | ✅ | ❌ | ✅ | ✅ | ✅ |
| Category 7: First Responders | ✅ | ✅ | ✅ | ❌ | ✅ |
| Category 8: SOPs | ✅ | ✅ | ✅ | ❌ | ✅ |
| Category 9: Drills | ✅ | ✅ | ✅ | ❌ | ✅ |
| Category 10: Incident Review | ✅ | ✅ | ✅ | ❌ | ✅ |
| + Add Remediation Action button | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit / Mark Done / Escalate (remediation) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Branch compliance detail drawer | ✅ | Own categories tabs | ✅ | Category 6 tab | ✅ |
| Historical trend charts | ✅ | ✅ | ✅ | ❌ | ✅ |
| Export button | ✅ | ❌ | ✅ | ❌ | ❌ |
| KPI bar — all 6 cards | ✅ | Incident-related cards | ✅ | Insurance card only | ✅ |
| Alert banners | ✅ | Emergency-related alerts | ✅ | Insurance alerts | ✅ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/compliance/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/compliance/` | Compliance matrix data (branch × category, role-filtered) | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/compliance/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/compliance/alerts/` | Active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/compliance/{branch_id}/` | Branch compliance detail (all 10 items) | JWT + role check + category scope |
| GET | `/api/v1/group/{group_id}/health/compliance/{branch_id}/history/` | Branch compliance monthly history (12 months) | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/compliance/trend/` | Group overall compliance monthly trend (12 months) | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/compliance/trend/branches/` | Top 5 + bottom 5 branch trend lines | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/compliance/remediation/` | List all remediation actions (paginated, filtered) | Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/compliance/remediation/` | Create remediation action | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/compliance/remediation/{action_id}/` | Retrieve remediation action detail | Medical Coordinator |
| PATCH | `/api/v1/group/{group_id}/health/compliance/remediation/{action_id}/` | Update remediation action | Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/compliance/remediation/{action_id}/resolve/` | Mark remediation action as done | Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/compliance/remediation/{action_id}/escalate/` | Escalate remediation action | Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/compliance/export/` | Initiate async export (PDF or XLSX) | Medical Coordinator / CEO / Chairman |
| GET | `/api/v1/group/{group_id}/health/compliance/export/{job_id}/status/` | Poll export job status | Same as POST |
| GET | `/api/v1/group/{group_id}/health/compliance/export/{job_id}/download/` | Download completed export | Same as POST |

**Query parameters for compliance matrix endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Branch filter |
| `category` | int[] | Category numbers (1–10) |
| `score_band` | str | `green`, `yellow`, `red` |
| `zone` | int[] | Zone filter |
| `ordering` | str | `overall_score` (asc = default, worst first), `-overall_score` (desc) |

**Query parameters for remediation list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Branch filter |
| `category` | int[] | Category numbers (1–10) |
| `status` | str[] | `open`, `in_progress`, `done` |
| `priority` | str[] | `high`, `medium`, `low` |
| `page` | int | Page number |
| `page_size` | int | Default 25; max 100 |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Compliance matrix load | `hx-get="/api/.../compliance/"` `hx-trigger="load"` `hx-target="#compliance-matrix"` `hx-indicator="#matrix-spinner"` | Matrix loads on page initialisation |
| Filter apply | `hx-get="/api/.../compliance/"` `hx-trigger="change"` `hx-target="#compliance-matrix"` `hx-include="#filter-form"` | Matrix rows filtered and replaced |
| KPI bar load | `hx-get="/api/.../compliance/kpi/"` `hx-trigger="load"` `hx-target="#kpi-bar"` | On page load |
| Alert banner load | `hx-get="/api/.../compliance/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | On page load |
| Compliance matrix cell click (inline expand) | `hx-get="/api/.../compliance/{branch_id}/?category={cat_num}"` `hx-target="#cell-detail-{branch_id}-{cat_num}"` `hx-trigger="click"` `hx-swap="innerHTML"` | Cell detail row inserted below matrix row; second click collapses |
| Branch compliance detail drawer open | `hx-get="/api/.../compliance/{branch_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Summary tab default |
| Drawer tab switch | `hx-get="/api/.../compliance/{branch_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` `hx-trigger="click"` | Lazy load on first click |
| Item Details tab load | `hx-get="/api/.../compliance/{branch_id}/?tab=item_details"` `hx-target="#item-details-content"` `hx-trigger="click[tab='item_details'] once"` | Loaded once on first click |
| History tab load | `hx-get="/api/.../compliance/{branch_id}/history/"` `hx-target="#history-content"` `hx-trigger="click[tab='history'] once"` | Loaded once |
| Remediation plan tab load | `hx-get="/api/.../compliance/remediation/?branch={branch_id}"` `hx-target="#remediation-content"` `hx-trigger="click[tab='remediation'] once"` | Loaded once |
| Trend chart load | `hx-get="/api/.../compliance/trend/"` `hx-trigger="load"` `hx-target="#trend-chart-container"` | On page load; chart rendered from returned JSON |
| Branch trend lines load | `hx-get="/api/.../compliance/trend/branches/"` `hx-trigger="load"` `hx-target="#branch-trend-container"` | On page load |
| Remediation list load | `hx-get="/api/.../compliance/remediation/"` `hx-trigger="load"` `hx-target="#remediation-list"` | On page load |
| Remediation filter apply | `hx-get="/api/.../compliance/remediation/"` `hx-trigger="change"` `hx-target="#remediation-list"` `hx-include="#remediation-filter-form"` | List replaced |
| Remediation pagination | `hx-get="/api/.../compliance/remediation/?page={n}"` `hx-target="#remediation-list"` `hx-push-url="false"` | List page swapped |
| Add remediation action modal submit | `hx-post="/api/.../compliance/remediation/"` `hx-target="#remediation-list"` `hx-on::after-request="closeModal(); fireToast(); refreshKPI();"` | New action prepended to list; KPI updated |
| Mark done modal submit | `hx-post="/api/.../compliance/remediation/{action_id}/resolve/"` `hx-target="#remediation-row-{action_id}"` `hx-swap="outerHTML"` `hx-on::after-request="closeModal(); fireToast(); refreshMatrix();"` | Action row status updated; compliance matrix re-scored |
| Compliance matrix refresh (post-resolution) | Out-of-band swap: `hx-swap-oob="true"` on matrix in resolve response | Affected cell score updated without full page reload |
| Export initiate | `hx-post="/api/.../compliance/export/"` `hx-target="#export-status"` `hx-trigger="click"` | Export button replaced with "Preparing…" |
| Export status poll | `hx-get="/api/.../compliance/export/{job_id}/status/"` `hx-trigger="every 5s [exportPending]"` `hx-target="#export-status"` | Polls until complete; download link replaces indicator |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
