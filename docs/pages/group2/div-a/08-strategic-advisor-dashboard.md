# 08 — Strategic Advisor Dashboard

> **URL:** `/group/gov/advisor/`
> **File:** `08-strategic-advisor-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Strategic Advisor (G1) — exclusive landing page

---

## 1. Purpose

Read-only analytics and strategy view for the Group Strategic Advisor. The Advisor's mandate
is to analyse trends, identify growth opportunities, and guide the Chairman on 3-year strategy
— with zero write access to the platform.

Core use cases:
- View 3-year enrollment, revenue, and academic performance trends
- Study expansion feasibility analyses prepared for new locations
- Review inter-branch benchmarking to identify high/low performers
- Access historical KPI data for strategic input

**Critical rule:** Zero write controls rendered. Every `[Edit]`, `[Approve]`, `[+ New]`,
`[Export]` for sensitive data is hidden server-side. The Advisor can only view and download
pre-generated strategic reports.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Strategic Advisor | G1 | Read-only — all analytics sections | Exclusive dashboard |
| Chairman | G5 | — | Own dashboard |
| All G4/G3/G1 others | — | — | Own dashboards |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Strategic Advisor Dashboard
```

### 3.2 Page Header
```
Strategic Intelligence — [Advisor Name]                [Download Strategy Brief ↓]
Group Strategic Advisor · Last login: [date time]
```

> No action buttons except [Download Strategy Brief] (a pre-generated PDF from Group MIS).

---

## 4. KPI Summary Bar (6 cards — all read-only)

| Card | Metric | Colour Rule | Notes |
|---|---|---|---|
| 3-Year Enrollment CAGR | `+12.4%` | Green >10% · Yellow 5–10% · Red <5% | Compound annual growth |
| Revenue Growth (3Y) | `+18.7%` | Green >15% · Yellow 8–15% · Red <8% | FY comparison |
| Market Penetration | `34%` of target districts | Green >50% · Yellow 25–50% · Red <25% | Districts with active branches |
| Expansion Studies | `3 feasibility studies` | Info | Completed + In Progress |
| Academic Improvement | `+7.2 pts` YoY | Green >5 · Yellow 2–5 · Red <2 | Avg score point improvement |
| Branches Added (3Y) | `+8 branches` | Info | From 40 to 48 branches |

> All cards are static display — no click-through action. Drill-down links below chart sections.

---

## 5. Sections

### 5.1 3-Year Enrollment Trend

> Strategic view of student enrollment growth across the entire group.

**Display:** Line chart + summary table.

#### Chart: Enrollment Trend
- **Type:** Multi-line chart
- **Lines:** Total Enrollment · Day Scholars · Hostelers (if group has hostels) · Integrated Coaching
- **X-axis:** Academic years (FY2024, FY2025, FY2026 + FY2027 projection with dashed line)
- **Y-axis:** Student count
- **Tooltip:** Year · Category · Count · Growth: +X%
- **Projection line:** FY2027 estimated (dashed, based on CAGR)
- **Export:** PNG

#### Summary Table (below chart — read-only, no search/filter for G1)
| FY | Total | Day Scholars | Hostelers | Growth % |
|---|---|---|---|---|
| FY2024 | 65,200 | 42,100 | 23,100 | — |
| FY2025 | 73,800 | 47,200 | 26,600 | +13.2% |
| FY2026 | 82,340 | 52,600 | 29,740 | +11.6% |
| FY2027 (proj) | 92,000 | 58,800 | 33,200 | +11.7% |

---

### 5.2 3-Year Revenue & Financial Trend

> Revenue growth analysis for strategic planning input.

**Display:** Bar + line combo chart.

- **Bar:** Annual revenue by FY (₹ Crores)
- **Line overlay:** Revenue per student (₹)
- **X-axis:** FY years
- **Y-axis (left):** ₹ Crores (revenue)
- **Y-axis (right):** ₹ per student
- **Tooltip:** FY · Revenue: ₹X.XCr · Per Student: ₹X,XXX · Growth: +X%
- **Note:** Financial data is G1-safe — shows totals only, no branch-level breakdown for Advisor
- **Export:** PNG

---

### 5.3 Academic Performance Trend (4 Terms)

> How academic quality is improving or declining group-wide.

**Display:** Combo chart.

- **Bar:** Exam pass rate % per term
- **Line:** Average score % per term
- **X-axis:** Last 4 exam terms
- **Y-axis:** % (0–100)
- **Benchmark line:** 90% target pass rate (dashed)
- **Tooltip:** Term · Pass rate: X% · Avg score: X%
- **Export:** PNG

---

### 5.4 Expansion Feasibility Studies

> All feasibility studies done for potential new branches — read-only for Advisor.

**Display:** Card grid — 3 columns.

**Card fields per study:**
- Location name + State
- Status badge: Complete · In Progress · On Hold
- Demand Score: X / 100 (colour-coded)
- Competition Level: Low / Medium / High
- Recommended: ✅ Proceed · ⚠ Conditional · ❌ Not Recommended
- Last updated date
- [View Details] link

**[View Details]:** Opens `expansion-study-view` drawer (read-only).

> G1 Advisor cannot create or edit feasibility studies. For that: page 15 (Chairman/CEO/MD).

---

### 5.5 Benchmarking Snapshot

> Top and bottom performers — for strategic input on resource allocation.

**Display:** Two compact tables side-by-side.

#### Top 5 Branches (by composite score)
| Rank | Branch | Score | Enrollment | Fee % | Avg Score |
|---|---|---|---|---|---|
| 1 | [Name] | 94 | X | X% | X% |
| ... | | | | | |

#### Bottom 5 Branches (needs attention)
| Rank | Branch | Score | Enrollment | Fee % | Avg Score |
|---|---|---|---|---|---|
| 46 | [Name] | 52 | X | X% | X% |
| ... | | | | | |

**"View Full Benchmarking →"** link to page 16 (read-only for G1).

---

### 5.6 Strategic Brief Download

> Pre-generated strategic analysis report for Advisor's use.

**Display:** Card with last generated date.

- **Document:** "Group Strategic Brief — Q1 FY2027 — [Date]"
- **Contents:** Enrollment trends · Revenue analysis · Market share · Expansion pipeline · Branch performance tiers
- **[Download PDF] button:** Initiates PDF download
- **Note:** "Brief generated by Group MIS Officer. Contact them for updated brief."

---

## 6. Drawers (Read-Only Only)

### 6.1 Drawer: `expansion-study-view` (read-only)
- **Trigger:** Expansion card → [View Details]
- **Width:** 640px
- **Tabs:** Overview · Demographics · Competition · Financials · Recommendation
- **All tabs:** Read-only — all form fields disabled, no edit icons
- **Overview:** Location, catchment area, study date, status
- **Demographics:** Population data, student-age population, existing school density
- **Competition:** Competitor schools, their enrollment, fee structure comparison
- **Financials:** Projected enrollment Year 1–3, projected revenue, break-even timeline
- **Recommendation:** Final recommendation with justification text and risk factors

---

## 7. Charts Summary (all 4 charts on page)

| # | Chart | Type | Export |
|---|---|---|---|
| 1 | Enrollment Trend (3Y + projection) | Multi-line | PNG |
| 2 | Revenue & Per-Student Trend | Bar + line combo | PNG |
| 3 | Academic Performance (4 terms) | Bar + line combo | PNG |
| 4 | Benchmarking — Top/Bottom (inline tables) | Table (no chart) | — |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Strategy brief download | "Strategic brief downloading…" | Info | 4s |
| Brief not available | "Strategic brief hasn't been generated yet. Contact the MIS Officer." | Warning | 6s |
| Session expired | "Your session has expired. Please log in again." | Error | Manual |
| Data load error | "Failed to load trend data. Refresh to try again." | Error | Manual |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No enrollment data | "Historical data not yet available" | "Enrollment trend data will appear after 2+ academic years of usage" | — |
| No expansion studies | "No expansion studies" | "No feasibility studies have been completed yet" | — |
| No strategy brief | "No strategy brief available" | "The MIS Officer will generate a brief before your next advisory session" | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 6 KPI cards + 3 chart placeholders + expansion cards (3) + top/bottom tables |
| Expansion drawer open | Spinner in drawer |
| Chart data load | Spinner centred in each chart area |
| PDF download | Spinner in download button (momentary) |

---

## 11. Role-Based UI Visibility

| Element | Advisor G1 | All others |
|---|---|---|
| Page | ✅ | ❌ redirect |
| All charts | ✅ Read-only | N/A |
| Expansion card [View Details] | ✅ Read-only drawer | N/A |
| [Download Strategy Brief] | ✅ | N/A |
| Any [Edit] / [+ New] / [Approve] button | ❌ hidden | N/A |
| Branch-level financial breakdown | ❌ hidden (aggregate only) | N/A |
| Export chart PNG | ✅ | N/A |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/advisor/dashboard/` | JWT (G1 Advisor) | Full dashboard data |
| GET | `/api/v1/group/{id}/analytics/enrollment-trend/?years=3` | JWT (G1) | 3-year enrollment trend |
| GET | `/api/v1/group/{id}/analytics/revenue-trend/?years=3` | JWT (G1) | 3-year revenue trend |
| GET | `/api/v1/group/{id}/analytics/academic-trend/?terms=4` | JWT (G1) | 4-term academic trend |
| GET | `/api/v1/group/{id}/expansion/studies/` | JWT (G1) | Expansion feasibility list |
| GET | `/api/v1/group/{id}/expansion/studies/{sid}/` | JWT (G1) | Study detail (read-only) |
| GET | `/api/v1/group/{id}/benchmarking/top-bottom/` | JWT (G1) | Top/bottom 5 branches |
| GET | `/api/v1/group/{id}/reports/strategy-brief/latest/` | JWT (G1) | Download strategy brief PDF |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Open expansion study drawer | `click` | GET `.../expansion/studies/{id}/` | `#drawer-body` | `innerHTML` |
| Download strategy brief | `click` | GET `.../reports/strategy-brief/latest/` | — | — (triggers download) |
| Chart year filter | `change` | GET `.../enrollment-trend/?years={val}` | `#enrollment-chart-data` | `innerHTML` (re-renders) |
| Dashboard data refresh | `every 5m` | GET `.../advisor/dashboard/summary/` | `#advisor-summary` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
