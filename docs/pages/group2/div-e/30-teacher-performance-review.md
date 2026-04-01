# 30 — Teacher Performance Review

- **URL:** `/group/hr/appraisal/teacher-reviews/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Performance Review Officer (Role 46, G1) — Read Only

---

## 1. Purpose

The Teacher Performance Review page is a cross-branch read-only analytical view of all teacher appraisals submitted under the current active appraisal cycle. The Group Performance Review Officer's mandate is analytical integrity: this role exists to prevent rating inflation, identify genuine underperformers, and surface patterns that require HR Director intervention. The page provides all data needed to make these judgements without allowing the officer to modify any appraisal record.

Rating inflation — where a branch gives the majority of its teachers 4 or 5 out of 5 without credible evidence — is a systemic issue in school groups. The Performance Review Officer compares each teacher's rating to the group average for their subject and flags branches whose average deviates significantly upward. Conversely, the officer tracks teachers rated 1 or 2, ensures they have been nominated for a Performance Improvement Plan (PIP), and verifies the branch has communicated the outcome to the teacher.

Teachers recommended for promotion (rated 4–5 with additional recommendation flag from branch principal) appear highlighted in the promotion pipeline column. These cases feed directly into the Promotion Recommendation Tracker (page 31). Teachers flagged for PIP appear in a separate filter, and the officer can view the full appraisal form narrative for each case. All anomalies observed — inflation flags, missing calibration, unexplained rating changes — are logged as internal observations that the officer sends to the HR Director directly from this page.

Because this is a G1 read-only role, the page has no create, edit, or delete capability. Every interactive element either opens a view drawer or applies a filter. The page is intentionally dense with analytical tools: sorting by deviation score, filtering by anomaly type, and the rating distribution chart are the core tools for this officer's daily work during an appraisal cycle.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Performance Review Officer | G1 | Read Only + Flag to HR Director | Cannot edit any appraisal data |
| Group HR Director | G3 | Full Read + Edit Calibrated Rating | Can make calibration adjustments from this view |
| Group HR Manager | G3 | Read Only | Monitors flagged cases |
| Group Training & Development Manager | G2 | No Access | Not on appraisal workflow |
| Branch Principal | Branch G3 | Own Branch Only | Cannot see other branches |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > Performance Appraisal > Teacher Performance Review`

### 3.2 Page Header
- **Title:** Teacher Performance Review
- **Subtitle:** Cross-branch appraisal review for active cycle — [Cycle Name shown dynamically]
- **Actions (top-right):**
  - `Export Appraisal Summary` (CSV/XLSX)
  - `Flag to HR Director` (opens compose observation modal — Performance Review Officer only)
  - Cycle selector dropdown (if multiple cycles exist, switch between them)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Rating inflation detected (branch average > group average + 1.0) | "ALERT: [N] branch(es) show potential rating inflation. Review highlighted rows." | Amber — dismissible |
| PIP nominations missing for rated-1/2 teachers | "WARNING: [N] teachers rated 1–2 have no PIP nomination on file." | Amber — dismissible |
| Calibration not yet completed for any branch | "INFO: Calibration phase is in progress. Some ratings shown are uncalibrated." | Blue — dismissible |
| No active appraisal cycle | "No active appraisal cycle found. Data shown is from the most recently closed cycle." | Grey — informational |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Appraisals Reviewed | Count of submitted teacher appraisals in active cycle | Blue always | No drill-down |
| Rating Inflation Flags | Branches with avg deviation > +1.0 above group avg | Red if > 0, Green if 0 | Filters table to flagged branches |
| PIP Recommendations | Teachers with Calibrated Rating ≤ 2 flagged for PIP | Amber if > 0, Green if 0 | Filters table to PIP Flag = Yes |
| Promotion Recommendations | Teachers with Calibrated Rating ≥ 4 and promotion flag | Green if > 0, Blue if 0 | Filters table to Promotion Flag = Yes |
| Branch-Average Deviation | Max deviation value across all branches (absolute) | Red if > 1.5, Amber 1.0–1.5, Green < 1.0 | No drill-down |
| Calibration Required | Branches with uncalibrated ratings | Amber if > 0, Green if 0 | Filters table to calibration pending |

---

## 5. Main Table — Teacher Appraisal Records

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Teacher Name | Text + avatar | Yes | No |
| Branch | Badge | Yes | Yes — dropdown |
| Subject | Text | Yes | Yes — dropdown |
| Self-Rating | Number (1–5 or ABCD) | Yes | Yes — range |
| Manager Rating | Number (1–5 or ABCD) | Yes | Yes — range |
| Calibrated Rating | Number + highlight if changed | Yes | Yes — range |
| PIP Flag | Icon (flag or dash) | No | Yes — Yes/No |
| Promotion Flag | Icon (star or dash) | No | Yes — Yes/No |
| Branch Avg | Decimal (e.g., 3.8) | Yes | No |
| Deviation | Signed decimal vs group avg (e.g., +0.9) | Yes | Yes — range |
| Status | Badge (Submitted / Calibrated / Published) | No | Yes — multi-select |
| Actions | Eye icon (view drawer) | No | No |

### 5.1 Filters
- **Branch:** multi-select
- **Subject:** multi-select
- **Rating Range:** self-rating, manager rating, calibrated rating (min–max sliders)
- **Anomaly Type:** Inflation Flag / PIP Flag / Promotion Flag / Deviation > 1 / All
- **Status:** Submitted / Calibrated / Published
- **Cycle:** dropdown (defaults to active cycle)

### 5.2 Search
Free-text search on Teacher Name. Triggers `hx-get` on keyup with 400 ms debounce.

### 5.3 Pagination
Server-side, 25 rows per page. Displays `Showing X–Y of Z teachers`. Preserves active filters and sort order across pages.

---

## 6. Drawers

### 6.1 Create
Not applicable — read-only page. No create action.

### 6.2 View Full Appraisal
**Trigger:** Row click or eye icon
**Displays:** Teacher profile (name, branch, subject, join date), full appraisal form responses (all KPI items with self-rating, manager rating, calibrated rating per item), narrative comments from appraiser, POCSO and BGV status summary, promotion/PIP recommendation text, appraiser name and date, calibration notes if any.

### 6.3 Edit
Not available for Performance Review Officer (G1). HR Director (G3) can access a limited calibration edit: change Calibrated Rating with mandatory reason text, which is logged with timestamp and reviewer name.

### 6.4 Flag to HR Director (observation modal)
**Trigger:** `Flag to HR Director` header button or per-row flag icon
**Fields:**
- Select teacher(s) or branch(es) being flagged
- Anomaly Type (dropdown: Inflation / PIP Missing / Deviation / Other)
- Observation Notes (textarea, required)
- Urgency (Normal / High)
- Submit — sends in-app notification to HR Director with link to this page

---

## 7. Charts

**Rating Distribution by Branch (Grouped Bar Chart)**
- X-axis: Branch names
- Y-axis: Count of teachers
- Series per rating value: 1 (red), 2 (orange), 3 (yellow), 4 (teal), 5 (green)
- Group average line overlay (dashed)
- Tooltip: hover shows count and % of branch total for that rating
- Highlights branches with deviation > 1.0 with a warning indicator on X-axis label

**Self vs Calibrated Rating Scatter Plot**
- X-axis: Self-Rating
- Y-axis: Calibrated Rating
- Each point = one teacher, colour-coded by branch
- Points far from the diagonal line (self ≠ calibrated) indicate significant adjustment
- Used to spot branches where manager/calibration systematically inflates or deflates

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Observation flagged to HR Director | "Observation sent to HR Director successfully." | Success | 4s |
| Export triggered | "Appraisal summary export started." | Info | 4s |
| Cycle switched | "Showing appraisal data for cycle: [Name]." | Info | 3s |
| Calibration edit saved (HR Director only) | "Calibrated rating updated for [Teacher Name]." | Success | 4s |
| Flag submission failed | "Failed to send observation. Please try again." | Error | 6s |

---

## 9. Empty States

- **No appraisals submitted yet:** "No teacher appraisals have been submitted for the current cycle. Check back once the Manager Assessment phase is complete."
- **No results match filters:** "No appraisals match the selected filters. Try broadening your filter criteria."
- **No active cycle:** "No active appraisal cycle is currently running. Select a past cycle from the dropdown to view historical data."

---

## 10. Loader States

- Table skeleton: 8 placeholder rows with shimmer on initial load.
- KPI cards: skeleton rectangles with shimmer.
- Drawer: spinner centred while full appraisal form loads.
- Chart container: grey placeholder with "Loading chart…" text until data arrives.

---

## 11. Role-Based UI Visibility

| Element | Perf. Review Officer (G1) | HR Director (G3) | HR Manager (G3) |
|---|---|---|---|
| View full appraisal drawer | Visible | Visible | Visible |
| Edit calibrated rating | Hidden | Visible + enabled | Hidden |
| Flag to HR Director button | Visible + enabled | Hidden | Hidden |
| Export button | Visible | Visible | Visible |
| Cycle selector | Visible | Visible | Visible |
| Per-row flag icon | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/appraisal/teacher-reviews/` | JWT G1+ | List teacher appraisal records (paginated) |
| GET | `/api/v1/hr/appraisal/teacher-reviews/{id}/` | JWT G1+ | View full appraisal form for one teacher |
| PATCH | `/api/v1/hr/appraisal/teacher-reviews/{id}/calibrate/` | JWT G3 HR Director | Update calibrated rating |
| POST | `/api/v1/hr/appraisal/teacher-reviews/flag/` | JWT G1 Perf. Review Officer | Submit observation to HR Director |
| GET | `/api/v1/hr/appraisal/teacher-reviews/kpis/` | JWT G1+ | KPI summary bar data |
| GET | `/api/v1/hr/appraisal/teacher-reviews/charts/distribution/` | JWT G1+ | Rating distribution by branch chart data |
| GET | `/api/v1/hr/appraisal/teacher-reviews/charts/scatter/` | JWT G1+ | Self vs calibrated rating scatter data |
| GET | `/api/v1/hr/appraisal/teacher-reviews/export/` | JWT G1+ | Export appraisal summary |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search teacher by name | keyup changed delay:400ms | GET `/api/v1/hr/appraisal/teacher-reviews/?q={val}` | `#reviews-table-body` | innerHTML |
| Filter change (branch/anomaly/status) | change | GET `/api/v1/hr/appraisal/teacher-reviews/?{params}` | `#reviews-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/appraisal/teacher-reviews/?page={n}` | `#reviews-table-body` | innerHTML |
| Open view drawer | click | GET `/api/v1/hr/appraisal/teacher-reviews/{id}/` | `#drawer-container` | innerHTML |
| Cycle selector change | change | GET `/api/v1/hr/appraisal/teacher-reviews/?cycle={id}` | `#reviews-table-body` | innerHTML |
| Refresh KPI bar | load | GET `/api/v1/hr/appraisal/teacher-reviews/kpis/` | `#kpi-bar` | innerHTML |
| Refresh distribution chart | change | GET `/api/v1/hr/appraisal/teacher-reviews/charts/distribution/?{params}` | `#chart-distribution` | innerHTML |
| Open flag observation modal | click | GET `/api/v1/hr/appraisal/teacher-reviews/flag/form/` | `#modal-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
