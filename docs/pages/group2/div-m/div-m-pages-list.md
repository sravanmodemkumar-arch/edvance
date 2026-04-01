# Group 2 — Division M: Analytics & MIS — Pages Reference

> **Division:** M — Analytics & MIS
> **Roles:** 6 roles (see Role Summary)
> **Base URL prefixes:** `/group/analytics/` · `/group/mis/` · `/group/data/`
> **Theme:** Light (`portal_base.html`)
> **Status key:** ✅ Spec done · ⬜ Not started

---

## Scale Context

| Dimension | Value |
|---|---|
| Institution Groups on Platform | 150 |
| Branches per group | 5–50 |
| Students per large group | 20,000–1,00,000 |
| Staff per large group | 3,000+ |
| MIS reports generated per month | 8–20 (one per report type + board-level) |
| Data dimensions tracked | Academic · Fee · Attendance · Hostel · Transport · HR · Welfare |
| Report consumers | Chairman · Board · CEO · CAO · CFO · Zone Directors |
| Academic year | April 1 – March 31 |
| Analytics data retention | 5 Academic Years (rolling) |

---

## Division M — Role Summary

| # | Role | Level | Large | Small | Post-Login URL |
|---|---|---|---|---|---|
| 102 | Group Analytics Director | G1 | ✅ Dedicated | ❌ | `/group/analytics/director/` |
| 103 | Group MIS Officer | G1 | ✅ Dedicated | ✅ 1 person | `/group/mis/officer/` |
| 104 | Group Academic Data Analyst | G1 | ✅ Dedicated | ❌ | `/group/analytics/academic/` |
| 105 | Group Exam Analytics Officer | G1 | ✅ Dedicated | ❌ | `/group/analytics/exam/` |
| 106 | Group Hostel Analytics Officer | G1 | ✅ Dedicated | ❌ | `/group/analytics/hostel/` |
| 107 | Group Strategic Planning Officer | G1 | ✅ Dedicated | ❌ | `/group/analytics/strategy/` |

> **Access note:** All Division M roles are **G1 — Read Only**. They can view, analyse, generate reports, and export data from all divisions. They cannot create, edit, or delete records in other divisions. Within Division M, they can fully manage their own analytics outputs (reports, plans, feasibility studies, export jobs).

---

## Section 1 — Role Dashboards

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 01 | Analytics Director Dashboard | `/group/analytics/director/` | `01-analytics-director-dashboard.md` | P0 | ✅ |
| 02 | MIS Officer Dashboard | `/group/mis/officer/` | `02-mis-officer-dashboard.md` | P0 | ✅ |
| 03 | Academic Data Analyst Dashboard | `/group/analytics/academic/` | `03-academic-data-analyst-dashboard.md` | P0 | ✅ |
| 04 | Exam Analytics Officer Dashboard | `/group/analytics/exam/` | `04-exam-analytics-officer-dashboard.md` | P0 | ✅ |
| 05 | Hostel Analytics Officer Dashboard | `/group/analytics/hostel/` | `05-hostel-analytics-officer-dashboard.md` | P0 | ✅ |
| 06 | Strategic Planning Officer Dashboard | `/group/analytics/strategy/` | `06-strategic-planning-officer-dashboard.md` | P0 | ✅ |

---

## Section 2 — MIS Reporting System

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 07 | Monthly MIS Report Builder | `/group/mis/builder/` | `07-monthly-mis-report-builder.md` | P1 | ✅ |
| 08 | MIS Report Archive | `/group/mis/archive/` | `08-mis-report-archive.md` | P1 | ✅ |
| 09 | Board Report Generator | `/group/mis/board-report/` | `09-board-report-generator.md` | P1 | ✅ |

---

## Section 3 — Cross-Branch Intelligence

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 10 | Cross-Branch Performance Hub | `/group/analytics/performance/` | `10-cross-branch-performance-hub.md` | P1 | ✅ |
| 11 | Branch Health Scorecard | `/group/analytics/scorecard/` | `11-branch-health-scorecard.md` | P1 | ✅ |

---

## Section 4 — Student & Academic Analytics

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 12 | Dropout Signal Monitor | `/group/analytics/dropout/` | `12-dropout-signal-monitor.md` | P1 | ✅ |
| 13 | Rank Trend Analyser | `/group/analytics/rank-trends/` | `13-rank-trend-analyser.md` | P1 | ✅ |
| 14 | Attendance Analytics | `/group/analytics/attendance/` | `14-attendance-analytics.md` | P2 | ✅ |
| 15 | Fee Collection Analytics | `/group/analytics/fees/` | `15-fee-collection-analytics.md` | P1 | ✅ |

---

## Section 5 — Teacher Performance Analytics

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 16 | Teacher Performance Analytics | `/group/analytics/teachers/` | `16-teacher-performance-analytics.md` | P1 | ✅ |

---

## Section 6 — Exam Analytics

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 17 | Exam Performance Heatmap | `/group/analytics/exam-heatmap/` | `17-exam-performance-heatmap.md` | P1 | ✅ |
| 18 | Topic Gap Analysis | `/group/analytics/topic-gaps/` | `18-topic-gap-analysis.md` | P1 | ✅ |

---

## Section 7 — Hostel Analytics

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 19 | Hostel Occupancy Analytics | `/group/analytics/hostel-occupancy/` | `19-hostel-occupancy-analytics.md` | P1 | ✅ |
| 20 | Hostel Welfare Trend Analytics | `/group/analytics/hostel-welfare/` | `20-hostel-welfare-trend-analytics.md` | P2 | ✅ |

---

## Section 8 — Strategic Planning

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 21 | Branch Feasibility Analyser | `/group/analytics/feasibility/` | `21-branch-feasibility-analyser.md` | P2 | ✅ |
| 22 | Three-Year Expansion Plan | `/group/analytics/expansion-plan/` | `22-three-year-expansion-plan.md` | P2 | ✅ |

---

## Section 9 — Data Quality & Export

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 23 | Data Quality Dashboard | `/group/analytics/data-quality/` | `23-data-quality-dashboard.md` | P2 | ✅ |
| 24 | Analytics Export Centre | `/group/analytics/exports/` | `24-analytics-export-centre.md` | P2 | ✅ |

---

## Shared Drawers & Overlays (all div-m pages)

| Drawer | Trigger | Width | Tabs | Description |
|---|---|---|---|---|
| `mis-report-builder` | MIS Builder → New Report | 680px | Scope · Sections · Schedule · Preview | Full MIS report configuration |
| `report-detail` | Archive → row | 680px | Overview · Sections · Recipients · Download | Report detail + download history |
| `board-report-config` | Board Report → Configure | 680px | Scope · Slides · Cover · Delivery | Board report setup |
| `dropout-student-detail` | Dropout Monitor → row | 560px | Profile · Risk Factors · Attendance · Actions | At-risk student detail |
| `rank-trend-detail` | Rank Trends → row | 560px | Trend Line · Branch Compare · Subject Drilldown | Rank performance detail |
| `teacher-performance-detail` | Teacher Analytics → row | 560px | Overview · Subjects · Trends · Branch | Teacher data drilldown |
| `exam-heatmap-drilldown` | Heatmap → cell | 480px | Subject · Topic · Branch · Time | Heatmap cell drilldown |
| `topic-gap-detail` | Topic Gap → row | 560px | Branches Affected · Trend · Recommendations | Topic gap detail |
| `hostel-branch-detail` | Hostel Analytics → row | 560px | Occupancy · Fee · Welfare · History | Branch hostel analytics |
| `feasibility-study-create` | Feasibility → + New Study | 680px | Location · Demand · Finance · Infrastructure · Risk | New feasibility study |
| `feasibility-study-detail` | Feasibility → row | 680px | Summary · Data · Recommendations · Status | Feasibility study detail |
| `expansion-plan-create` | Expansion Plan → + New Plan | 680px | Overview · Branches · Timeline · Budget | New expansion plan |
| `export-job-create` | Export Centre → + New Export | 560px | Dataset · Filters · Format · Delivery | Configure export job |
| `data-quality-branch-detail` | Quality Dashboard → row | 480px | Missing Fields · Last Updated · Actions | Branch data quality detail |

---

## UI Component Standard (applied to every page in div-m)

| Component | Specification |
|---|---|
| **Tables** | Sortable all columns · Checkbox row select + select-all · Responsive (card on mobile < 768px) · Column visibility toggle · Row count badge |
| **Search** | Full-text, 300ms debounce, highlights match |
| **Advanced Filters** | Slide-in filter drawer · Active filters as dismissible chips · "Clear All" · Filter count badge |
| **Pagination** | Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z results" · Page jump input |
| **Drawers** | Slide from right · Widths: 400/480/520/560/640/680px · Backdrop click closes (unsaved-changes guard) · ESC closes |
| **Modals** | Centred overlay · Confirm/delete only · Max 480px |
| **Forms** | Inline validation on blur · Required `*` · Character counter on textareas · Disabled submit until valid · Server error summary at top |
| **Toasts** | Bottom-right · Success 4s · Error manual · Warning 6s · Info 4s · Max 3 stacked |
| **Loaders** | Skeleton screens · Spinner on action buttons · Overlay for critical ops |
| **Empty States** | Illustration + heading + description + CTA · Separate "no data" vs "no search results" states |
| **Charts** | Chart.js 4.x · Responsive · Colorblind-safe palette · Legend · Tooltip · PNG export |
| **Role-based UI** | All write controls rendered server-side based on role level · G1 sees all data read-only · G1 can manage own analytics outputs |

---

## Role → Page Access Matrix

| Page | Analytics Dir G1 | MIS Officer G1 | Academic Analyst G1 | Exam Analytics G1 | Hostel Analytics G1 | Strategic Planning G1 |
|---|---|---|---|---|---|---|
| 01 Analytics Director Dashboard | ✅ Full | — | — | — | — | — |
| 02 MIS Officer Dashboard | — | ✅ Full | — | — | — | — |
| 03 Academic Data Analyst Dashboard | — | — | ✅ Full | — | — | — |
| 04 Exam Analytics Dashboard | — | — | — | ✅ Full | — | — |
| 05 Hostel Analytics Dashboard | — | — | — | — | ✅ Full | — |
| 06 Strategic Planning Dashboard | — | — | — | — | — | ✅ Full |
| 07 MIS Report Builder | ✅ View | ✅ Full | ✅ View | ✅ View | ✅ View | ✅ View |
| 08 MIS Report Archive | ✅ View | ✅ Full | ✅ View | ✅ View | ✅ View | ✅ View |
| 09 Board Report Generator | ✅ Full | ✅ Full | ✅ View | ✅ View | ✅ View | ✅ View |
| 10 Cross-Branch Performance Hub | ✅ Full | ✅ View | ✅ Full | ✅ View | ✅ View | ✅ View |
| 11 Branch Health Scorecard | ✅ Full | ✅ View | ✅ View | ✅ View | ✅ View | ✅ Full |
| 12 Dropout Signal Monitor | ✅ View | ✅ View | ✅ Full | ✅ View | — | — |
| 13 Rank Trend Analyser | ✅ View | ✅ View | ✅ Full | ✅ Full | — | ✅ View |
| 14 Attendance Analytics | ✅ View | ✅ Full | ✅ Full | — | — | ✅ View |
| 15 Fee Collection Analytics | ✅ Full | ✅ Full | — | — | ✅ View | ✅ Full |
| 16 Teacher Performance Analytics | ✅ View | ✅ View | ✅ Full | ✅ View | — | — |
| 17 Exam Performance Heatmap | ✅ View | ✅ View | ✅ View | ✅ Full | — | — |
| 18 Topic Gap Analysis | ✅ View | ✅ View | ✅ Full | ✅ Full | — | — |
| 19 Hostel Occupancy Analytics | ✅ View | ✅ View | — | — | ✅ Full | ✅ View |
| 20 Hostel Welfare Trend Analytics | ✅ View | ✅ View | — | — | ✅ Full | — |
| 21 Branch Feasibility Analyser | ✅ View | ✅ View | — | — | — | ✅ Full |
| 22 Three-Year Expansion Plan | ✅ View | ✅ View | — | — | — | ✅ Full |
| 23 Data Quality Dashboard | ✅ Full | ✅ Full | ✅ View | ✅ View | ✅ View | ✅ View |
| 24 Analytics Export Centre | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full |

---

## Functional Coverage Audit — Zero Gaps

| # | Job to Be Done | Role | Page |
|---|---|---|---|
| 1 | View cross-branch performance intelligence at a glance | Analytics Director | 01, 10 |
| 2 | Generate and distribute monthly MIS reports to Chairman/Board | MIS Officer | 02, 07, 08 |
| 3 | Build board-level presentation reports with charts and summaries | MIS Officer / Analytics Dir | 09 |
| 4 | Detect dropout signals and at-risk students before they leave | Academic Data Analyst | 12 |
| 5 | Analyse rank trends across academic years and branches | Academic Data Analyst / Exam Analytics | 13 |
| 6 | Track attendance patterns and correlate with academic performance | Academic Data Analyst | 14 |
| 7 | Monitor fee collection rates and defaulter patterns across branches | MIS Officer / Analytics Dir | 15 |
| 8 | Analyse teacher performance using objective data | Academic Data Analyst | 16 |
| 9 | Identify high-performing and underperforming teachers cross-branch | Academic Data Analyst | 16 |
| 10 | Generate exam performance heatmaps per branch per subject | Exam Analytics Officer | 17 |
| 11 | Identify topic-wise knowledge gaps across all branches | Exam Analytics Officer / Academic Analyst | 18 |
| 12 | Track hostel occupancy rates, AC vs Non-AC, Boys vs Girls | Hostel Analytics Officer | 19 |
| 13 | Analyse hostel welfare trends and escalation patterns | Hostel Analytics Officer | 20 |
| 14 | Analyse hostel fee collection and defaulter patterns | Hostel Analytics Officer / MIS Officer | 19, 15 |
| 15 | Conduct feasibility study for a new branch location | Strategic Planning Officer | 21 |
| 16 | Build and maintain 3-year expansion plan with budget projections | Strategic Planning Officer | 22 |
| 17 | Score every branch on a composite health index | Analytics Director / Strategic Planning | 11 |
| 18 | Compare branches side-by-side on key performance metrics | Analytics Director | 10 |
| 19 | Monitor data quality and completeness across all branches | Analytics Dir / MIS Officer | 23 |
| 20 | Export any dataset in PDF/XLSX for offline distribution | All | 24 |
| 21 | Schedule recurring automated reports for senior stakeholders | MIS Officer | 07, 09 |
| 22 | Archive and retrieve historical MIS reports by month/year | MIS Officer | 08 |
| 23 | Track which branches haven't submitted data (missing data alerts) | Analytics Dir / MIS Officer | 23 |
| 24 | Identify correlation between teacher performance and student results | Academic Data Analyst | 16, 13 |
| 25 | Analyse JEE/NEET performance trends for integrated coaching branches | Exam Analytics Officer | 17, 18 |
| 26 | Track student welfare event severity trends for hostel branches | Hostel Analytics Officer | 20 |
| 27 | Provide strategic analysis for new branch expansion decisions | Strategic Planning Officer | 21, 22, 11 |
| 28 | Monitor transport utilisation rates and route efficiency trends | MIS Officer / Analytics Dir | 02, 01 |
| 29 | Track scholarship conversion rates and merit trends | Academic Data Analyst | 13 |
| 30 | Generate branch-wise net promoter score from student/parent data | Analytics Director | 11 |
| 31 | Produce NSS/NCC participation analytics for compliance reporting | MIS Officer | 02, 08 |
| 32 | Track POCSO incident trends and resolution rates | MIS Officer | 02 |
| 33 | Analyse admissions funnel — enquiry to enrollment conversion | Analytics Director | 10 |
| 34 | Cross-reference exam performance with attendance data | Academic Data Analyst | 14, 13 |
| 35 | Identify branches with highest and lowest staff retention rates | MIS Officer / Strategic Planning | 02, 22 |
| 36 | Produce analytics data consumed by Division A governance roles | All | 01, 10, 11 |
| 37 | Ensure analytics data integrity before board presentations | Analytics Dir / MIS Officer | 23, 09 |

---

## Implementation Priority

```
P0 — Before division portal goes live
  01–06   All 6 role dashboards

P1 — Sprint 2
  07, 08, 09, 10, 11, 12, 13, 15, 16, 17, 18, 19

P2 — Sprint 3
  14, 20, 21, 22, 23, 24
```

---

## Division Count Summary

| Division | Total | Large Uses | Small Uses |
|---|---|---|---|
| M — Analytics & MIS | 24 | 24 | 3–4 (MIS Officer covers most) |

---

*Last updated: 2026-03-21 · Total pages: 24 · Roles: 6 · Audit pass: 1 — zero gaps · Deep audit: 37-item functional coverage*
