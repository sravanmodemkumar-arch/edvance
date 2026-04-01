# P-10 — Branch Compliance Scorecard

> **URL:** `/group/audit/scorecard/`
> **File:** `p-10-branch-compliance-scorecard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Internal Audit Head (Role 121, G1) — primary viewer

---

## 1. Purpose

The Branch Compliance Scorecard is the single-page answer to: "How compliant is each branch?" It computes a weighted composite score across six compliance dimensions — Financial, Academic, Safety, Affiliation, CAPA Closure, and Grievance Resolution — and presents a clear grade (A+ through D) per branch. In Indian education, this scorecard is what the CEO presents at the quarterly Trust Board meeting, what the Audit Head uses to prioritise inspections, and what determines whether a branch is flagged for "special monitoring."

The problems this page solves:

1. **No single compliance metric:** Without a composite score, the CEO must look at 6 different reports to assess a branch. The scorecard combines them: a branch might score 90% on academics but 45% on safety — the composite reveals the risk that individual reports hide.

2. **Branch ranking for governance:** Trust Boards need rankings. "Which are our best-run branches? Which need intervention?" The scorecard provides a league table — sortable, filterable, and drillable — that turns compliance into a competitive metric among branch principals.

3. **Trend visibility:** A branch that dropped from Grade A to Grade C in one quarter needs immediate attention. The scorecard tracks quarterly trends and highlights degradation with visual indicators, ensuring problems are caught early.

4. **Customisable weights:** Different groups prioritise differently — a group with many hostelers may weight Safety at 30% instead of 20%. The scorecard allows G4/G5 to configure dimension weights, making the score reflect the group's actual priorities.

5. **Automated data aggregation:** The scorecard pulls data automatically from P-03 (Financial), P-04 (Academic), P-05 (Safety), P-11 (Affiliation), P-15 (CAPA), and P-18 (Grievance) — no manual data entry. This ensures the score is always current, not a point-in-time snapshot.

**Scale:** 5–50 branches · 6 dimensions · quarterly recalculation · A+ to D grading · drillable to dimension and finding level

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Internal Audit Head | 121 | G1 | Full read + configure weights + override | Scorecard owner |
| Group Academic Quality Officer | 122 | G1 | Read — academic dimension detail | — |
| Group Inspection Officer | 123 | G3 | Read — safety/infrastructure dimension | — |
| Group ISO / NAAC Coordinator | 124 | G1 | Read — affiliation dimension | — |
| Group Affiliation Compliance Officer | 125 | G1 | Read — affiliation dimension | — |
| Group Grievance Audit Officer | 126 | G1 | Read — grievance dimension | — |
| Group Compliance Data Analyst | 127 | G1 | Full read + analytics | MIS generation |
| Group Process Improvement Coordinator | 128 | G3 | Read — CAPA dimension | — |
| Group CEO / Chairman | — | G4/G5 | Full read + configure weights + approve methodology | Board presentation |
| Group COO | 59 | G4 | Full read | Operational oversight |
| Branch Principal | — | G3 | Read (own branch) — own scorecard only | Self-assessment |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Weight configuration: G4/G5 only. Branch Principals see their own branch scorecard only (anonymised peer comparison available).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Branch Compliance Scorecard
```

### 3.2 Page Header
```
Branch Compliance Scorecard                           [Configure Weights]  [Recalculate]  [Export]
Audit Head — K. Ramachandra Rao
Sunrise Education Group · Q3 FY 2025-26 · 28 branches · Group Average: 81% (Grade A) · Top: Ameerpet (96%) · Bottom: Uppal (45%)
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Group Avg Score | Percentage | AVG(composite_score) across all branches | Green ≥ 85%, Amber 70–84%, Red < 70% | `#kpi-avg` |
| 2 | A+ / A Branches | Integer | COUNT(branches) WHERE grade IN ('A+', 'A') | Static green | `#kpi-top` |
| 3 | C / D Branches | Integer | COUNT(branches) WHERE grade IN ('C', 'D') | Red > 3, Amber 1–3, Green = 0 | `#kpi-bottom` |
| 4 | Improving | Integer | Branches where score increased vs previous quarter | Static green | `#kpi-improving` |
| 5 | Declining | Integer | Branches where score decreased vs previous quarter | Red > 5, Amber 1–5, Green = 0 | `#kpi-declining` |
| 6 | Weakest Dimension | Text | Dimension with lowest group-average score | — | `#kpi-weakest` |

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Scorecard** — The main branch ranking with composite scores
2. **Dimension Detail** — Per-dimension scores across branches
3. **Trend Analysis** — Quarterly trends per branch
4. **Weight Configuration** — Scoring methodology (G4/G5)

### 5.2 Tab 1: Scorecard (League Table)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Rank | Integer | Yes | 1–N based on composite score |
| Branch | Text (link) | Yes | Opens branch detail drawer |
| Financial (20%) | Percentage | Yes | From P-03 |
| Academic (25%) | Percentage | Yes | From P-04 |
| Safety (20%) | Percentage | Yes | From P-05 |
| Affiliation (15%) | Percentage | Yes | From P-11 |
| CAPA Closure (10%) | Percentage | Yes | From P-15 |
| Grievance (10%) | Percentage | Yes | From P-18 |
| Composite Score | Percentage | Yes | Weighted average |
| Grade | Badge | Yes | A+ (≥95%) / A (85–94%) / B (70–84%) / C (50–69%) / D (<50%) |
| Trend | Arrow + % | Yes | Change vs previous quarter |
| Open Findings | Integer | Yes | Total unresolved |
| Status | Badge | No | 🟢 Compliant / 🟡 Monitor / 🔴 Intervention |

**Colour coding:** Each percentage cell colour-coded Green/Amber/Red based on threshold

**Row highlighting:** D-grade branches highlighted with red background; newly declined branches (dropped ≥ 1 grade) highlighted amber

### 5.3 Tab 2: Dimension Detail

**Dimension selector (6 radio buttons):**

Selected dimension shows branch-wise breakdown:

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Rank | Integer | Yes | Rank within this dimension |
| Branch | Text | Yes | — |
| Score | Percentage | Yes | Dimension score |
| Sub-component 1 | Percentage | Yes | e.g., for Financial: Fee Reconciliation |
| Sub-component 2 | Percentage | Yes | e.g., Vendor Payment Compliance |
| Sub-component 3 | Percentage | Yes | e.g., Petty Cash Audit |
| Sub-component 4 | Percentage | Yes | e.g., Scholarship Compliance |
| Open Findings | Integer | Yes | Within this dimension |
| Last Audit Date | Date | Yes | Most recent audit for this dimension |
| Trend | Arrow | Yes | vs previous quarter |

**Sub-components per dimension:**
- **Financial:** Fee reconciliation, Vendor payments, Petty cash, Scholarship compliance, Budget adherence
- **Academic:** Lesson plan compliance, Exam paper quality, Teaching hours, Lab completion, Syllabus coverage
- **Safety:** Fire safety, CCTV coverage, Infrastructure condition, Transport compliance, Hygiene
- **Affiliation:** Requirements met %, Document readiness, Expiry management
- **CAPA Closure:** On-time closure %, Overdue count, Repeat finding rate
- **Grievance:** Resolution time, Satisfaction rate, Repeat complaint rate

### 5.4 Tab 3: Trend Analysis

**Branch trend table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Q1 Score | Percentage | Yes | — |
| Q2 Score | Percentage | Yes | — |
| Q3 Score | Percentage | Yes | — |
| Q4 Score | Percentage | Yes | — |
| FY Average | Percentage | Yes | — |
| Direction | Badge | Yes | Improving / Stable / Declining |
| Best Quarter | Text | No | — |
| Worst Quarter | Text | No | — |
| Volatility | Badge | Yes | High (> 15% swing) / Medium (5–15%) / Low (< 5%) |

**Trend chart displayed above table** (see §7)

### 5.5 Tab 4: Weight Configuration (G4/G5)

**Current weights:**

| Dimension | Current Weight | Range | Last Modified | Modified By |
|---|---|---|---|---|
| Financial Compliance | 20% | 10–30% | 15 Apr 2025 | CEO |
| Academic Quality | 25% | 15–35% | 15 Apr 2025 | CEO |
| Safety & Infrastructure | 20% | 15–30% | 15 Apr 2025 | CEO |
| Affiliation Compliance | 15% | 5–20% | 15 Apr 2025 | CEO |
| CAPA Closure Rate | 10% | 5–15% | 15 Apr 2025 | CEO |
| Grievance Resolution | 10% | 5–15% | 15 Apr 2025 | CEO |
| **Total** | **100%** | — | — | — |

**Edit controls:** Sliders per dimension. Total must equal 100%. Preview shows score recalculation impact.

**Grade thresholds (configurable):**

| Grade | Threshold | Default |
|---|---|---|
| A+ | ≥ X% | 95% |
| A | ≥ X% | 85% |
| B | ≥ X% | 70% |
| C | ≥ X% | 50% |
| D | < X% | Below 50% |

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-scorecard-detail` (780px, right-slide)

- **Title:** "Scorecard — [Branch Name] · [Grade Badge]"
- **Tabs:** Overview · Financial · Academic · Safety · Affiliation · CAPA · Grievance · History
- **Overview tab:**
  - Composite score with grade
  - Radar chart: 6 dimensions
  - Quarterly trend mini-chart
  - Rank among all branches
  - Key strengths (top 2 dimensions)
  - Key risks (bottom 2 dimensions)
  - Open findings count by dimension
  - Recommended actions (auto-generated based on lowest dimensions)
- **Dimension tabs (Financial through Grievance):**
  - Sub-component breakdown
  - Latest audit summary and date
  - Open findings list
  - Score calculation transparency: which metrics → what score
- **History tab:**
  - Quarterly scores for last 8 quarters
  - Score trend chart
  - Grade history: when did grade change?
  - Major events: findings opened/closed, audits conducted
- **Footer:** [View All Findings (P-06)] [Schedule Audit (P-02)] [View Reports (P-09)] [Export PDF]
- **Access:** G1+ (Division P roles); Branch Principal (own branch only)

### 6.2 Modal: `configure-weights` (560px, G4/G5)

- **Title:** "Configure Scorecard Weights"
- **Fields:**
  - Per dimension: slider (range as specified) + percentage display
  - Total indicator: must equal 100% (validation)
  - Grade thresholds: A+ / A / B / C / D cutoff percentages
  - Preview: "Applying these weights would change N branches' grades"
  - Effective from (date — usually start of next quarter)
  - Reason for change (textarea — logged for audit)
- **Buttons:** Cancel · Preview Impact · Apply
- **Access:** G4/G5 only

### 6.3 Modal: `recalculate-scores` (480px)

- **Title:** "Recalculate All Scores"
- **Content:** "This will refresh all branch scores using latest data from P-03, P-04, P-05, P-11, P-15, P-18."
- **Fields:**
  - Period (dropdown): Current quarter / Specific quarter
  - Include incomplete audits? (toggle — default: no)
- **Buttons:** Cancel · Recalculate
- **Output:** Progress bar + summary of changes (N branches changed grade)
- **Access:** Role 121, G4+

### 6.4 Modal: `export-scorecard` (480px)

- **Title:** "Export Scorecard"
- **Fields:**
  - Format (radio): PDF (Board presentation) / Excel (detailed data) / CSV
  - Period (dropdown): Current quarter / FY to date / Specific quarter
  - Include (checkboxes): Overall rankings / Dimension detail / Trend data / Findings summary
  - PDF: Include radar charts per branch? (toggle)
  - Watermark (dropdown): None / CONFIDENTIAL / BOARD COPY
- **Buttons:** Cancel · Export
- **Access:** G1+ (Division P roles)

---

## 7. Charts

### 7.1 Branch Ranking (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Branch Compliance Ranking — Current Quarter" |
| Data | Composite score per branch, sorted descending |
| Colour | Per-grade colours: A+ green, A teal, B amber, C orange, D red |
| Target line | Group average (dashed) |
| API | `GET /api/v1/group/{id}/audit/scorecard/analytics/ranking/` |

### 7.2 Dimension Radar (Group Average)

| Property | Value |
|---|---|
| Chart type | Radar/Spider |
| Title | "Group Compliance Profile — 6 Dimensions" |
| Data | Group AVG per dimension |
| Overlay | Previous quarter (dashed) |
| API | `GET /api/v1/group/{id}/audit/scorecard/analytics/dimension-radar/` |

### 7.3 Quarterly Trend (Multi-Line)

| Property | Value |
|---|---|
| Chart type | Multi-line |
| Title | "Branch Compliance Trend — Last 4 Quarters" |
| Data | Composite score per branch per quarter |
| Highlight | Top 3 and bottom 3 in bold; rest greyed |
| API | `GET /api/v1/group/{id}/audit/scorecard/analytics/trend/` |

### 7.4 Grade Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut |
| Title | "Branch Grade Distribution" |
| Data | COUNT per grade: A+, A, B, C, D |
| Centre text | N branches |
| API | `GET /api/v1/group/{id}/audit/scorecard/analytics/grade-distribution/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Scores recalculated | "Scores recalculated — [N] grade changes" | Success | 4s |
| Weights updated | "Scorecard weights updated — effective [Date]" | Success | 3s |
| Export generated | "Scorecard exported as [Format]" | Success | 3s |
| Grade dropped | "⚠️ [Branch] dropped to Grade [C/D] — intervention recommended" | Warning | 6s |
| D-grade alert | "🔴 [Branch] scored [X]% — Grade D — CEO notification sent" | Error | 6s |
| No data available | "Insufficient audit data for [Branch] — score unavailable" | Info | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No audit data | 📊 | "No Scorecard Data" | "Compliance scores require completed audits. Schedule your first audit." | Go to Audit Calendar |
| Insufficient data for branch | ⚠️ | "Incomplete Data — [Branch]" | "At least one audit per dimension is needed to compute a score." | — |
| No trend data | 📈 | "Trend Not Available" | "Trend analysis requires at least 2 quarters of data." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + table skeleton |
| Scorecard table | Table skeleton with coloured cells |
| Branch detail drawer | 780px skeleton: radar chart + 8 tabs |
| Recalculation | Progress bar with branch counter |
| Chart load | Grey canvas placeholder |
| Trend table | Table skeleton with sparklines |
| Weight configuration | Slider skeleton |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit/scorecard/` | G1+ | All branch scores |
| GET | `/api/v1/group/{id}/audit/scorecard/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/audit/scorecard/branches/{branch_id}/` | G1+ | Branch detail scorecard |
| GET | `/api/v1/group/{id}/audit/scorecard/dimensions/` | G1+ | Dimension detail |
| GET | `/api/v1/group/{id}/audit/scorecard/dimensions/{dimension}/` | G1+ | Specific dimension breakdown |
| GET | `/api/v1/group/{id}/audit/scorecard/trend/` | G1+ | Quarterly trend data |
| POST | `/api/v1/group/{id}/audit/scorecard/recalculate/` | 121, G4+ | Recalculate all scores |
| GET | `/api/v1/group/{id}/audit/scorecard/weights/` | G1+ | Current weight configuration |
| PUT | `/api/v1/group/{id}/audit/scorecard/weights/` | G4+ | Update weights |
| GET | `/api/v1/group/{id}/audit/scorecard/analytics/ranking/` | G1+ | Ranking bar chart |
| GET | `/api/v1/group/{id}/audit/scorecard/analytics/dimension-radar/` | G1+ | Dimension radar |
| GET | `/api/v1/group/{id}/audit/scorecard/analytics/trend/` | G1+ | Trend multi-line |
| GET | `/api/v1/group/{id}/audit/scorecard/analytics/grade-distribution/` | G1+ | Grade donut |
| GET | `/api/v1/group/{id}/audit/scorecard/export/` | G1+ | Export scorecard |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../scorecard/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#scorecard-content` | `innerHTML` | `hx-trigger="click"` |
| Branch detail drawer | Row click | `hx-get=".../scorecard/branches/{id}/"` | `#right-drawer` | `innerHTML` | 780px drawer |
| Dimension select | Radio click (Tab 2) | `hx-get=".../scorecard/dimensions/{dim}/"` | `#dimension-table` | `innerHTML` | `hx-trigger="change"` |
| Recalculate | Button click | `hx-post=".../scorecard/recalculate/"` | `#recalc-result` | `innerHTML` | Progress bar |
| Update weights | Form submit | `hx-put=".../scorecard/weights/"` | `#weight-result` | `innerHTML` | Toast + preview |
| Export | Form submit | `hx-get=".../scorecard/export/"` | `#export-result` | `innerHTML` | Download |
| Chart load | Tab shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |
| Sort | Header click | `hx-get` with sort param | `#scorecard-table` | `innerHTML` | `hx-trigger="click"` |
| Pagination | Page click | `hx-get` with page param | `#table-body` | `innerHTML` | — |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
