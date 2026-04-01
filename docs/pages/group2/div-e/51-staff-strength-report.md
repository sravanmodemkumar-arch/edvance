# 51 — Staff Strength Report

- **URL:** `/group/hr/reports/strength/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group HR Director (Role 41, G3)

---

## 1. Purpose

The Staff Strength Report provides a real-time snapshot of sanctioned versus actual staff strength across all branches and role categories. This is one of the highest-priority reports in the HR function because it is the foundation of three critical institutional processes: budget planning, regulatory compliance, and recruitment prioritisation. Without accurate and current strength data, the HR Director cannot make defensible decisions in any of these areas.

Every branch in the group operates under a sanctioned staff structure — a formally approved list of posts with defined counts per category. A typical branch sanctioned structure might be: Mathematics Teacher × 4, Science Teacher × 3, English Teacher × 2, Hindi Teacher × 2, Computer Teacher × 1, Physical Education × 1, Office Administrator × 2, Accountant × 1, Peon × 2, Librarian × 1, and so on. This sanctioned structure is approved by the Board and is linked to the student enrolment capacity of the branch. Actual strength is the number of posts currently filled by employed, active staff. The difference is the vacancy count — posts that are funded and approved but unfilled.

Vacancies are classified on two dimensions: role category (Teaching vs. Non-Teaching) and urgency. A vacancy becomes Critical when the post is a core academic subject (Mathematics, Science, English, Languages) and has been unfilled for more than 30 days — because these vacancies directly affect curriculum delivery and can trigger regulatory inspection findings. Critical vacancies also affect student-teacher ratio compliance, which is a mandatory requirement under CBSE, state board, and NAAC/NATA accreditation frameworks. The report flags these prominently so the HR Director can direct the recruitment team to prioritise them.

The report is also the input to the monthly HR MIS Report (page 49). Budget planners use it to calculate the cost saved from unfilled posts versus the risk of leaving academic positions vacant. Recruitment managers use it to set the priority ranking of open positions. This page is P0 because the data it surfaces has immediate consequences for regulatory compliance and student welfare — a school found to be operating below minimum teacher:student ratios faces board de-recognition.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director | G3 | Full access — all branches, all categories, export, sanctioned strength edit | Primary operator |
| Group HR Manager | G3 | Read-only — all branches, export | Operational support |
| Group Recruiter — Teaching | G0 | No EduForge access | Receives vacancy briefings via email from HR |
| Group Recruiter — Non-Teaching | G0 | No EduForge access | Same as above |
| Branch Principal | G3 | Read-only — own branch only | Reviews own branch vacancy status |
| Group Performance Review Officer | G1 | Read-only — headcount data only | Used in appraisal context |
| All other roles | — | No access | Page not rendered |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › Reports › Staff Strength Report
```

### 3.2 Page Header

- **Title:** Staff Strength Report
- **Subtitle:** Sanctioned vs. Actual Staff — real-time vacancy tracking across all branches
- **As-of date badge:** "Data as of [date] [time]" — auto-updated on page load
- **Primary CTA:** `Export Report` (PDF + CSV options in dropdown)
- **Secondary CTA:** `Update Sanctioned Strength` (HR Director only — opens editor for sanctioned posts)
- **View Toggle:** Branch Summary View (default) / Detailed Category View / Critical Vacancies View

### 3.3 Alert Banner (conditional)

- **Red:** `[N] critical vacancies — core academic posts unfilled for > 30 days. Regulatory risk.` Action: `View Critical`
- **Amber:** `[N] branches have vacancy rate above 20%. Review recruitment status.` Action: `View Branches`
- **Blue:** `Teacher:Student ratio below recommended 1:30 in [N] branches.` Action: `View`
- **Green:** No critical vacancies and all branches above minimum strength — shown when no active alerts

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Sanctioned Posts | Sum of all sanctioned posts across all branches and categories | Blue always | No drill-down |
| Actual Staff | Count of active, employed staff (all branches combined) | Blue always | Navigate to Staff Directory (page 13) |
| Total Vacancies | Sanctioned − Actual | Amber if > 50, red if > 100, green if < 20 | Switch to Critical Vacancies View |
| Critical Vacancies (>30 days) | Count of vacancies in core academic categories unfilled > 30 days | Red if > 0, else green | Filter table to critical rows |
| Vacancy Rate % | Total Vacancies ÷ Total Sanctioned × 100 | Green if < 10%, amber 10–20%, red > 20% | No drill-down |
| Teacher:Student Ratio (avg) | Group-wide average active teachers ÷ enrolled students | Green if ≤ 1:30, amber 1:30–1:40, red > 1:40 | No drill-down |

---

## 5. Main Table — Branch Strength Summary (Default View)

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text (link — drill down to category view for this branch) | Yes (A–Z) | Yes — text search |
| Category | Text (Teaching / Non-Teaching — shown in Detailed View; grouped in Summary View) | Yes | Yes — dropdown |
| Sanctioned | Numeric | Yes | No |
| Actual | Numeric | Yes | No |
| Vacancy | Numeric (Sanctioned − Actual) | Yes | No |
| Critical | Badge (Yes / No) — Yes if core academic vacancy > 30 days | No | Yes — toggle |
| Days Vacant | Numeric (max days vacant across all open posts in row) | Yes | Yes — range dropdown |
| Recruitment Status | Badge (Active / No Action / On Hold / Position Closed) | No | Yes — dropdown |
| Actions | Icon buttons: View Detail / Edit Sanctioned Strength | No | No |

### 5.1 Filters

- **Branch:** Multi-select dropdown
- **Role Category:** Teaching / Non-Teaching / All
- **Vacancy Status:** Has Vacancies / No Vacancies / All
- **Critical Only:** Toggle
- **Recruitment Status:** Active / No Action / On Hold / Position Closed / All
- **Days Vacant Range:** 0–30 / 30–60 / 60–90 / 90+ / All
- **Reset Filters** button

### 5.2 Search

Text search on Branch name. Min 2 characters, 400 ms debounce.

### 5.3 Pagination

Server-side. Default 25 rows per page (larger default due to data density). Options: 25 / 50 / 100. "Showing X–Y of Z rows."

---

## 6. Drawers

### 6.1 Branch Detail Drill-Down

Triggered by clicking Branch name. Opens wide drawer or navigates to scoped sub-view.

**Displays (role-by-role breakdown for selected branch):**
- Table: Role Title / Sanctioned Posts / Filled / Vacant / Critical / Days Vacant / Names of Current Staff in Role
- Summary: Total sanctioned, total filled, total vacant, vacancy rate
- Teacher:Student ratio for this branch
- Export: "Export Branch Strength PDF"

### 6.2 Update Sanctioned Strength

HR Director only. Triggered by `Update Sanctioned Strength` button or Edit icon on row.

**Fields:**
- Branch (dropdown)
- Role Category (dropdown: Teaching / Non-Teaching)
- Role Title (text — must match an existing role in the staff directory schema)
- Current Sanctioned Count (read-only display)
- New Sanctioned Count (numeric input)
- Effective Date of Change (date picker, defaults to today)
- Reason for Change (dropdown: Board Approval / Student Intake Change / Budget Revision / School Expansion / Regulatory Requirement)
- Board Approval Reference (text, required if reason = Board Approval)
- Notes (textarea, optional)

**Validation:** New count cannot reduce below current actual count (cannot have sanctioned < filled).

**Submit:** `Update Sanctioned Strength` → PATCH `/api/hr/strength/sanctioned/{branch_id}/{role_id}/`

### 6.3 Critical Vacancies View

Triggered by `Critical Vacancies View` tab or KPI card drill-down.

**Renders** a separate table:
- All vacancies where: role is core academic (Math, Science, English, Language, Core Subject) AND days_vacant > 30
- Columns: Branch / Role / Days Vacant / Sanctioned / Filled / Recruitment Status / Priority
- Priority auto-assigned: P0 = > 60 days, P1 = 31–60 days
- Action per row: "Open Recruitment" (links to Recruitment Pipeline page with pre-filled role and branch)

### 6.4 Delete Confirmation

Not applicable — no records are deleted on this page. Sanctioned strength changes are versioned (append-only log), not deletions.

---

## 7. Charts

### Chart A — Vacancy Rate by Branch (Horizontal Bar Chart)

- **Type:** Horizontal bar chart
- **Y-axis:** Branch names
- **X-axis:** Vacancy rate %
- **Reference line:** 10% acceptable threshold (dashed)
- **Bar colour:** Green < 10%, amber 10–20%, red > 20%
- **Tooltip:** Branch, vacancy rate %, vacancy count, sanctioned total
- **Export:** PNG

### Chart B — Staff Strength Composition by Branch (Stacked Bar Chart)

- **Type:** Stacked vertical bar chart
- **X-axis:** Branch names
- **Y-axis:** Headcount
- **Stack 1:** Teaching staff (blue)
- **Stack 2:** Non-Teaching staff (teal)
- **Stack 3:** Vacancies (red, extending above stacks to show sanctioned total)
- **Tooltip:** Branch, teaching count, non-teaching count, vacancy count, sanctioned total
- **Export:** PNG

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| Sanctioned strength updated | Success | "Sanctioned strength updated for [Branch] — [Role]. Change effective [date]." |
| Export initiated | Info | "Generating Staff Strength Report. Downloading shortly." |
| Export ready | Success | "Report downloaded." |
| Critical vacancy alert | Warning | "[Role] at [Branch] has been vacant for [N] days. Escalate recruitment." |
| Sanctioned < Actual validation error | Error | "Sanctioned count cannot be set below the current filled count of [N]." |
| Server error | Error | "Failed to load strength data. Please retry." |

---

## 9. Empty States

**No data (new group setup):**
> Icon: org chart outline
> "No sanctioned strength data has been configured yet."
> "Set up the sanctioned structure for each branch using 'Update Sanctioned Strength'."
> CTA: `Update Sanctioned Strength`

**Filtered results return nothing:**
> Icon: magnifying glass
> "No rows match your current filters."
> CTA: `Reset Filters`

---

## 10. Loader States

- Page load: Skeleton KPI bar + skeleton table rows
- View toggle switch: Table skeleton replaces current table while new view loads
- Branch drill-down drawer: Spinner while role-level data fetches
- Charts: Grey placeholder boxes with pulse animation; load independently
- Export: Button spinner + "Generating..." during PDF/CSV creation

---

## 11. Role-Based UI Visibility

| UI Element | HR Director | HR Manager | Branch Principal | Perf. Review Officer |
|---|---|---|---|---|
| `Update Sanctioned Strength` button | Visible | Hidden | Hidden | Hidden |
| Edit Sanctioned action per row | Visible | Hidden | Hidden | Hidden |
| All branches in table | Yes | Yes | Own branch only | Yes (read-only) |
| Critical Vacancies View tab | Visible | Visible | Hidden | Hidden |
| Teacher:Student Ratio KPI | Visible | Visible | Visible (own branch) | Visible |
| Export Report button | Visible | Visible | Visible (own branch PDF) | Hidden |
| Sanctioned strength edit log | Visible | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/strength/` | Paginated branch-category strength data |
| GET | `/api/hr/strength/{branch_id}/` | Role-level breakdown for specific branch |
| PATCH | `/api/hr/strength/sanctioned/{branch_id}/{role_id}/` | Update sanctioned count for a role |
| GET | `/api/hr/strength/critical-vacancies/` | List of critical vacancies |
| GET | `/api/hr/strength/kpis/` | KPI summary bar data |
| GET | `/api/hr/strength/charts/vacancy-rate/` | Vacancy rate by branch chart data |
| GET | `/api/hr/strength/charts/composition/` | Strength composition chart data |
| GET | `/api/hr/strength/export/` | Generate staff strength report (PDF/CSV) |

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| Table load | `hx-get` on page render | Fetches branch summary |
| View toggle (Summary/Detailed/Critical) | `hx-get` on toggle buttons + `hx-target="#main-content"` | Swaps between view templates |
| Filter change | `hx-get` + `hx-include` | Re-fetches filtered table |
| Search | `hx-trigger="keyup changed delay:400ms"` | Debounced branch name search |
| Pagination | `hx-get` on page buttons | Fetches page N |
| Branch drill-down | `hx-get` + `hx-target="#drawer"` | Loads role-level data for branch |
| Sanctioned update form | `hx-patch` + `hx-target="#row-{id}"` | Patches sanctioned count, updates row |
| Chart load | `hx-get` on `#chart-{n}` independently | Async chart data fetch |
| KPI refresh | `hx-get` on `#kpi-bar` after sanctioned updates | Refreshes KPI values |
| Toast | `hx-swap-oob` on `#toast-container` | Out-of-band toast on mutations |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
