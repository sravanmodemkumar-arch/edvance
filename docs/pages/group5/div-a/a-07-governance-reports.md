# A-07 — Governance MIS & Reports

> **URL:** `/coaching/admin/reports/`
> **File:** `a-07-governance-reports.md`
> **Priority:** P2
> **Roles:** Director/Owner (K7) · Finance Manager (K5)

---

## 1. Monthly Summary Report

```
MONTHLY SUMMARY — MARCH 2026
TOPPERS COACHING CENTRE (All branches + Franchise)

STUDENTS:
  Own branches:       1,840  (Main: 820, Dilsukhnagar: 480, Kukatpally: 360, Online: 180)
  Franchise network:  1,220  (6 active franchise branches)
  TOTAL ECOSYSTEM:    3,060

  New joins (March):    82   (own: 48, franchise: 34)
  Dropouts (March):     24   (own: 14, franchise: 10)   Dropout rate: 1.3% ⚠️ (target <1%)
  Net growth:          +58

REVENUE:
  Own branches:       ₹48.2L (target ₹52.0L — 92.7%)
  Royalty received:   ₹4.9L  (from 6 franchises)
  Other income:       ₹1.2L  (study material, test series subscriptions)
  TOTAL INCOME:       ₹54.3L

EXPENSES (estimated March):
  Salaries:           ₹28.4L (52.3% of revenue)
  Rent (4 locations): ₹6.8L
  Platform + IT:      ₹1.4L  (EduForge fee + SMS + WhatsApp API)
  Marketing:          ₹3.2L
  Misc ops:           ₹1.8L
  TOTAL EXPENSES:     ₹41.6L

OPERATING SURPLUS:    ₹12.7L  (23.4% margin)
```

---

## 2. Quarterly Performance Report

```
QUARTERLY REVIEW — Q4 FY 2025–26 (Jan–Mar 2026)

ACADEMIC OUTCOMES:
  SSC CGL Mock (national benchmark):
    TCC avg AIR: 3,421 (top 14.3% nationally among test-series subscribers)
    Students improved AIR by >1,000: 142 / 420 (33.8%)
    Students in AIR < 1,000 (mock): 18 — potential SSC CGL selections
  Banking IBPS Clerk 2025 (actual exam results):
    TCC students cleared Prelim: 84 / 340 (24.7%)  — above national avg (18%)
    TCC students cleared Mains: 41 / 84 (48.8%)
    TCC students selected: 29 (8.5% of enrolled Banking students) ✅

ADMISSIONS FUNNEL (Q4):
  Walk-ins / enquiries:  480
  Demo classes attended: 312 (65.0%)
  Enrolled:              218 (69.9% of demo attendees; 45.4% of enquiries)
  Lost to competitors:    94 (top competitor: Career Power — mentioned 38 times)

FACULTY PERFORMANCE:
  Student rating > 4.0/5.0:  34 / 40 faculty (85%)
  Rating < 3.5 (action zone):  2 faculty → PIP initiated
  Classes missed (no substitution): 8 instances in Q4 ← target: 0

RETENTION:
  Students completing full course:  72.4%  (target: 75%)  ⚠️ below target
  Dropout reasons (exit survey): Exam cleared 28%, Job found 18%,
                                  Fee issue 22%, Moved city 12%, Other 20%
```

---

## 3. Annual MIS Dashboard

```
ANNUAL MIS — FY 2025–26

FINANCIAL YEAR SUMMARY:
  Total revenue (own):    ₹614.4L (₹6.14Cr)
  Total royalties:        ₹56.8L
  Gross income:           ₹671.2L
  Net surplus:            ₹148.6L  (22.2% net margin)
  Capex (AY 2025–26):     ₹42L (Kukatpally branch fit-out + hostel upgrade)

STUDENT OUTCOMES FY 2025–26:
  Government job selections (confirmed): 186 students ← TOPPERS BRAND ASSET
    SSC CGL: 68 | IBPS Clerk/PO: 54 | RRB NTPC: 42 | SSC CHSL: 22
  JEE selections (Dropper batch): 14 (8 in NITs, 6 in state colleges)

GROWTH FY 2025–26 vs FY 2024–25:
  Students:       +18.4%  (1,840 vs 1,554)
  Revenue:        +22.1%  (₹6.14Cr vs ₹5.03Cr)
  Franchise:      +2 new branches (Tirupati + Nizamabad)
  Selections:     +24.0%  (186 vs 150)

NEXT YEAR TARGETS (FY 2026–27):
  Own branch students:    2,200 (+19.6%)
  Revenue (own + royal.): ₹8.0Cr
  Govt. selections:       250+
  New franchise branches: 2 (Karimnagar + Vizag)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/reports/monthly/?month=2026-03` | Monthly summary |
| 2 | `GET` | `/api/v1/coaching/{id}/reports/quarterly/?quarter=Q4&fy=2025-26` | Quarterly report |
| 3 | `GET` | `/api/v1/coaching/{id}/reports/annual/?fy=2025-26` | Annual MIS |
| 4 | `GET` | `/api/v1/coaching/{id}/reports/outcomes/` | Student government job selections |
| 5 | `POST` | `/api/v1/coaching/{id}/reports/export/?format=pdf` | Export report as PDF |

---

## 5. Business Rules

- Student government job selection data is TCC's most powerful marketing asset; every confirmed selection (SSC CGL, IBPS, RRB, UPSC) must be logged in EduForge with the student's consent for public mention; the annual 186 selections is the headline number used in all advertising — it must be verifiable with appointment letters, not just self-reported by students; unverified claims in advertising have attracted consumer forum complaints against coaching centres
- The dropout rate (1.3% in March) must be tracked and categorised; "exam cleared" and "job found" dropouts are positive outcomes and should be excluded from the operational dropout rate; the true attrition rate (students leaving due to dissatisfaction, fee issues, or moving to competitors) is 22% + 12% = 34% of all dropouts, or ~0.44% of total students; EduForge's exit survey captures this distinction, which is critical for correctly identifying retention problems
- Revenue per student (₹614.4L / ~2,000 avg students = ₹30,720/year per student) is TCC's core unit economics metric; as franchise revenue is royalty-only (15% of franchise collection), the blended revenue per student including franchise is lower; the Director must track both metrics separately to understand how franchise expansion affects profitability — franchise growth increases brand reach but dilutes per-student revenue
- Salary cost as a percentage of revenue (52.3% in March) is the most important cost control metric for coaching centres; industry benchmark for healthy coaching operations is 45–55%; TCC is at the upper end of the healthy range; if salary costs exceed 60% of revenue, the centre is operationally stressed; key drivers of salary cost creep are star faculty poaching by competitors (requiring pay increases to retain) and declining enrolments with fixed salary commitments
- The governance report is for internal Director use only; it must not be shared with Branch Managers in full — Branch Managers see only their branch's section; franchise owners see only their own franchise's data; the consolidated P&L and selection outcome data are confidential because competitors actively attempt to obtain this information to benchmark against TCC and poach faculty

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division A*
