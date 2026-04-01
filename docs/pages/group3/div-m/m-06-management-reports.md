# M-06 — Trust & Management Board Reports

> **URL:** `/school/mis/management/`
> **File:** `m-06-management-reports.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Trust/Management (S7) — multi-school view + full download · Principal (S6) — own school view + download · MIS Coordinator (S4) — generate and share reports (cannot see salary details)

---

## 1. Purpose

The Management Board Reports are designed for the school's governing body — the Trust, Society, or Management Committee — who oversee multiple schools or have strategic oversight of the school. Unlike the Principal's operational dashboard, management reports are:
- **Higher-level:** Trends over years, not daily pulse
- **Multi-school:** Comparative view across the trust's schools
- **Strategic:** Student growth, financial sustainability, compliance health, quality metrics
- **Periodic:** Monthly summary, quarterly board report, annual report

Audience: Trust Secretary, Chairman, Board Members, Finance Committee, Correspondent

---

## 2. Multi-School Overview

```
MANAGEMENT BOARD VIEW — GREENFIELDS EDUCATION TRUST
Schools under trust: 3 (Hyderabad, Secunderabad, Warangal)

SCHOOL SUMMARY — March 2026:
  ──────────────────────────────────────────────────────────────────────────────
  School              Students  Staff   Fee Coll%  Compliance  Board Results
  ──────────────────────────────────────────────────────────────────────────────
  Greenfields Hyd     1,240     127     91.8%      88/100 🟡   98.7% pass (X)
  Greenfields Sec       980     104     94.2%      92/100 ✅   97.8% pass (X)
  Greenfields Wgl       620      72     88.4%      79/100 🔴   95.4% pass (X)
  ──────────────────────────────────────────────────────────────────────────────
  TRUST TOTAL:        2,840     303     91.4%      86/100 avg

ATTENTION FLAGS:
  🔴 Greenfields Warangal: Compliance 79/100 — below trust threshold (80)
     3 critical gaps: Fire NOC lapsed + BGV 5 staff pending + RTE reimbursement claim not filed
     [Escalated to Trust Secretary]
  🟡 Hyderabad: 24 students below 75% attendance — CBSE board risk
  ✅ Secunderabad: All green this month
```

---

## 3. Quarterly Board Report

```
QUARTERLY MANAGEMENT REPORT — Q3 2025–26 (Jan–Mar 2026)
Prepared by: MIS Coordinator (Hyderabad)
Reviewed by: Principal

1. ENROLMENT & GROWTH:
   Start of year (April 2025): 1,218 students
   Current (March 2026):       1,240 students (+22 new admissions mid-year)
   Target 2026–27:             1,300 students
   New applications received (for 2026–27): 148 (vs 118 last year = +25.4% interest) ✅

2. ACADEMIC PERFORMANCE:
   Unit Test 1 (Feb 2026): School avg 71.2% (target 72%) — marginally below target
   Board exam 2025 (Class X): 98.7% pass — above 97% target ✅
   Board exam 2025 (Class XII): 95.7% pass — below 97% target ⚠
   Remedial initiated for Class XII Physics/Chemistry ✅

3. FINANCIAL HEALTH:
   Q3 fee collection: ₹72,20,000 / ₹78,00,000 billed (92.6%) ✅
   YTD outstanding: ₹17,80,000 (7.0% of billed)
   Payroll (Q3): ₹1,41,98,520 disbursed (on time ✅)
   Training budget utilisation: 48% (significant underuse — carry forward approved ✅)

4. COMPLIANCE:
   Score at Q3-end: 88/100
   CBSE inspection prep: 87/100 readiness
   No critical compliance failures this quarter ✅

5. HR:
   New joiners: 2 (TCH-046 Ms. Anita Rao, TCH-031 Mr. Suresh R.)
   Separations: 1 (resignation — Ms. Priya Iyer, LWD 14 Apr 2026)
   PIP active: 1 (Mr. Vijay P. — ongoing)
   Appraisal cycle in progress (due Apr 2026)

6. WELFARE:
   Active welfare flags: 8 students
   Counselling load: 14 active cases (anonymous)
   Grievances: 3 open (1 overdue — action in progress)
   No POCSO cases this quarter ✅
   No anti-ragging cases this quarter ✅

7. RECOMMENDATIONS TO BOARD:
   ① Approve training budget carry-forward: ₹2.6L → wellness programme
   ② Authorise library expansion completion (₹9L capital work)
   ③ Review Warangal school compliance — visit recommended
   ④ Discuss 2026–27 fee revision (CPI-linked increase — management call)

[Download Board Report PDF]  [Share via email to Board]
```

---

## 4. Annual Performance Report

```
ANNUAL REPORT — 2025–26 (SUMMARY EXTRACT)
For: Governing Board / Annual Trust Meeting

KEY METRICS (2025–26):
  Students served:        1,240
  Staff employed:         127
  Working days delivered: 220 (100% of target) ✅

ACADEMIC ACHIEVEMENTS:
  Class X CBSE: 98.7% pass, 4 students CGPA 10, school avg 8.6
  Class XII CBSE: 95.7% pass
  3 students in CBSE merit list (state level)
  8 students selected for national Olympiads

INSTITUTIONAL QUALITY:
  CBSE Affiliation: Grade A (maintained for 5th consecutive year) ✅
  Parent satisfaction survey (F-module): 84% satisfied or very satisfied
  Staff retention: 96.1% (only 5 separations; attrition 3.9%)
  Training hours (total): 2,840 teacher-hours (22 hours/teacher avg)

FINANCIAL SUMMARY:
  Fee revenue collected: ₹2,36,70,000
  Total cost: ₹6,58,84,000
  Trust subsidy: ₹4,22,14,000
  Cost per student: ₹53,133/year (₹4,428/month)

COMMUNITY & COMPLIANCE:
  RTE EWS/DG students enrolled: 310 (25.0%) ✅
  POCSO incidents: 0 (this year) ✅
  CBSE inspection: Not conducted this year (last: 2023 — Grade A)
  12A/80G compliance: ✅ (Form 10B filed 28 Sep 2025)

[Full annual report — 18 pages]  [Download for board presentation]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/trust/{trust_id}/mis/multi-school/` | Multi-school overview (Trust S7 only) |
| 2 | `GET` | `/api/v1/school/{id}/mis/management/quarterly/` | Quarterly board report |
| 3 | `GET` | `/api/v1/school/{id}/mis/management/annual/` | Annual performance report |
| 4 | `GET` | `/api/v1/school/{id}/mis/management/kpi-trends/` | KPI trend data (year-on-year) |
| 5 | `GET` | `/api/v1/school/{id}/mis/management/export/?format=pdf` | Export board report PDF |
| 6 | `POST` | `/api/v1/school/{id}/mis/management/share/` | Share report via email to board members |

---

## 6. Business Rules

- Trust-level multi-school view (S7) is strictly limited to the trust's own schools — a Trust/Management user cannot view any other trust's data; the trust boundary is enforced at the data model level (school.trust_id FK)
- Management reports are generated on-demand, not auto-scheduled; the MIS Coordinator generates the quarterly report, the Principal reviews and approves, then it is shared with the board; this workflow ensures the Principal has a chance to add context or corrections before the Trust sees numbers
- Individual student and staff data is never shown in management reports — only aggregates and counts; a Trust board member should not see individual salary details, POCSO case details, or specific student welfare information; the board's role is governance, not operations
- Annual report generation should be triggered after the final CBSE board results are available (typically May/June); the academic year MIS report is finalised only after all board results are confirmed; earlier versions are clearly marked "preliminary"
- Multi-school comparison is designed to identify outlier schools requiring trust-level attention — not to rank schools for competitive purposes; the framing is always "which school needs support?" not "which school is best?"

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division M*
