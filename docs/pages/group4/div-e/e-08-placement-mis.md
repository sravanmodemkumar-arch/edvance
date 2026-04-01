# E-08 — Placement MIS & Reports

> **URL:** `/college/placement/reports/`
> **File:** `e-08-placement-mis.md`
> **Priority:** P2
> **Roles:** Training & Placement Coordinator (S4) · Principal/Director (S6) · Trust/Management (S7) · NAAC Coordinator (S4)

---

## 1. Placement Dashboard (Season View)

```
PLACEMENT MIS DASHBOARD — 2026–27 Season
As of 27 March 2027

SEASON OVERVIEW:
  ┌─────────────────────────────────────────────────────────────────┐
  │  67.5%         23          ₹4.5L         90.5%                 │
  │  Placed        Companies   Median CTC     NIRF GO (est.)        │
  │  224/332       visited     (accepted)                           │
  └─────────────────────────────────────────────────────────────────┘

FUNNEL ANALYSIS:
  Total Students: 332
  → Eligible (CGPA/backlog criteria): 291 (87.7%)
  → Registered for at least 1 drive: 278 (83.7%)
  → Appeared in at least 1 drive: 268 (80.7%)
  → Selected by at least 1 company: 238 (71.7%)
  → Accepted at least 1 offer: 224 (67.5%)

FUNNEL LEAKAGES:
  Eligible but not registered: 13 students (9 going abroad, 4 self-arranged)
  Registered but not appeared: 10 students (medical: 4, exam clash: 3, unknown: 3)
  Selected but not accepted: 14 students (turned down all offers — seeking better)
  Action: Placement Coordinator counselling for "selected but not accepted" group

WEEKLY TREND (offers in hand):
  Week 1 Aug:  0 → Week 4 Sep: 42 → Week 8 Nov: 118 → Week 12 Jan: 168 → Week 16 Mar: 224
  Current week (27 Mar): +6 new offers (March active drives)
  Forecast to April end: 238–244 (pipeline active)
```

---

## 2. Company Performance Report

```
COMPANY PERFORMANCE ANALYSIS — 2026–27

COMPANY FUNNEL METRICS:
  Company         | Applied | Appeared | Selected | Offers | Join Rate | Avg CTC
  ─────────────────────────────────────────────────────────────────────────────────
  TCS             | 198     | 189      | 62       | 42     | ~100%     | ₹3.36L
  Infosys         | 194     | 189      | 24       | 22     | ~100%     | ₹3.6L–4.5L
  Amazon          | 45      | 44       | 6        | 4      | 100%      | ₹18.5L
  Goldman Sachs   | 28      | 27       | 3        | 2      | 100%      | ₹22.0L
  Wipro           | 188     | 181      | 18       | 12     | ~95%      | ₹3.5L
  Deloitte        | 62      | 61       | 7        | 5      | 100%      | ₹7.0L
  HCL             | 166     | 162      | 15       | 9      | ~95%      | ₹3.8L

MOST SELECTIVE: Goldman Sachs (7.4% selection rate) | Amazon (9.1%)
HIGHEST VOLUME: TCS (42 offers) | Wipro (12) | Infosys (22)
BEST CTC: Goldman Sachs ₹22L | Amazon ₹18.5L | Deloitte ₹7.0L
MOST DECLINED: Wipro (5 offers declined — students preferred alternatives)

COMPANY RELATIONSHIP HEALTH:
  TCS: ⭐⭐⭐⭐⭐ Excellent (long-term; 5th consecutive year)
  Amazon: ⭐⭐⭐⭐ Good (2nd year; expanding intake)
  Wipro: ⭐⭐⭐⭐ Good (stable)
  Company X (small startup): ⭐⭐ Poor — cancelled drive 2 days before
                                   (disrupted scheduling; on watch list)
```

---

## 3. Governing Body / Management Report

```
PLACEMENT SEASON REPORT — To Governing Body (Quarterly)

Q3 2026–27 (January – March 2027):

PLACEMENT PROGRESS:
  Cumulative placed: 224 / 332 (67.5%)
  This quarter: +56 offers accepted (Q1: 82, Q2: 86, Q3: 56)
  Remaining: 8–15 expected from April drives
  Final forecast: 72–75% (matching last year's 72.8% outcome)

FINANCIAL METRICS:
  Training spend YTD: ₹11.4L (within ₹12L budget)
  Cost per placed student: ₹11.4L / 224 = ₹5,089/student
  NIRF GO (est.): 90.5% — strong ranking metric

HIGHLIGHTS:
  ⭐ Goldman Sachs returned for 2nd year (₹22L CTC — highest campus offer)
  ⭐ ONGC PSU drive scheduled — first PSU in 3 years (Mech/EEE students benefit)
  ⭐ PPO from internships: 12 students (reduces pressure on campus drives)
  ⭐ Core branch (Mech) improvement: 36.7% vs 29.8% last year

CONCERNS:
  ⚠️ Mech branch still lowest (36.7%) — core hiring market sluggish
     Action: Automotive/manufacturing sector outreach initiated
  ⚠️ 14 students who cleared tests but declined all offers — seeking unusually high CTC
     Action: Career counselling + realistic expectations session
  ⚠️ IT sector hiring down 8% nationwide (industry trend) — managed via diversification

BUDGET REQUEST Q4:
  April drives (4 companies): ₹1.2L estimated (hospitality + testing infrastructure)
  Alumni engagement event: ₹80K (Annual Placement Alumni Meet — networking)
```

---

## 4. AICTE Mandatory Returns

```
AICTE RETURNS — Placement Data (Annual)

AICTE MANDATORY DISCLOSURE (Annual — aicte-india.org portal):
  Section F: Placement Data
    Total students eligible for placement: 291
    Students placed: 218 (prior year — 2024–25 batch; current year pending)
    Highest CTC: ₹42L (2024–25 batch)
    Lowest CTC: ₹2.4L
    Average CTC: ₹6.2L
    Companies visited: 26 (2024–25 season)

  Filing deadline: 30 June of each year (for prior academic year)
  EduForge auto-generates AICTE placement section from actual data
  Verification: Principal certifies accuracy (digital signature on AICTE portal)
  Filing status (2025–26): ✅ Filed 28 June 2026

AICTE-STUDENT BENEFIT MAP:
  AICTE uses placement data to compute "Employability Index" for institutions
  Institutions with <50% placement 3 years running are flagged for review
  GCEH 3-year average: 72.3% → No concern
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/placement/reports/dashboard/` | Real-time placement dashboard |
| 2 | `GET` | `/api/v1/college/{id}/placement/reports/funnel/` | Student placement funnel analysis |
| 3 | `GET` | `/api/v1/college/{id}/placement/reports/company-performance/` | Company-wise metrics |
| 4 | `GET` | `/api/v1/college/{id}/placement/reports/governing-body/` | GB quarterly report |
| 5 | `GET` | `/api/v1/college/{id}/placement/reports/aicte/` | AICTE mandatory disclosure data |

---

## 6. Business Rules

- Placement data in AICTE Mandatory Disclosure is public (published on AICTE portal); prospective students and parents compare placement rates across colleges; inflated data is detectable by students themselves (alumni of the same batch can contradict); AICTE has penalised colleges for misreporting in the mandatory disclosure, including withdrawal of approvals — EduForge's source-of-truth approach prevents this
- Funnel analysis is the most actionable placement MIS tool; knowing exactly where students drop out (eligible but not registered, selected but not accepting) allows targeted intervention; a placement cell that only tracks the final placement % misses the intermediate opportunities to improve
- Governing Body reporting must include negative trends alongside positives; a Management Report that only shows achievements creates false comfort; the GB must be aware of the core branch placement challenge, market trends, and company relationship issues to make informed decisions about training investment, infrastructure, and strategy
- NIRF Graduation Outcomes uses a formula that includes higher studies and government exams, not just placement; colleges that focus only on IT campus placement and ignore students going for GATE/civil services, entrepreneurship, or research miss easy NIRF GO points; EduForge tracks all outcome categories and ensures they are counted in the NIRF data submission
- The placement cell must maintain a 3-year archive of all placement records (offer letters, registration forms, attendance); NAAC peer teams request evidence from the most recent 3 academic years; a placement cell that cannot produce records beyond the current year fails the historical trend analysis requirement

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division E*
