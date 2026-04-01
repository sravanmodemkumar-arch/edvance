# E-04 — Placement Statistics & NIRF Data

> **URL:** `/college/placement/statistics/`
> **File:** `e-04-placement-statistics.md`
> **Priority:** P1
> **Roles:** Training & Placement Coordinator (S4) · NAAC Coordinator (S4) · Principal/Director (S6) · Trust/Management (S7)

---

## 1. Annual Placement Statistics

```
PLACEMENT STATISTICS — Batch 2022–26 (Final Year 2025–26)
(Annual report; submitted for NAAC and NIRF)

BATCH PROFILE:
  Total students (graduated): 294 (of 332 admitted; 38 still completing — laterals + backlogs)
  Programme: B.Tech (CSE 120, ECE 80, EEE 45, Mech 49)

PLACEMENT OUTCOMES:
  Placed (campus + off-campus): 218 (74.1% of 294 graduated)
  Higher education (PG/abroad):  36 (12.2%)
  Government/competitive exams:  12 (4.1%)
  Entrepreneurship:               4 (1.4%)
  Not placed / seeking:          24 (8.2%)

PLACEMENT BY BRANCH:
  CSE:  112 placed / 120 graduated = 93.3% ← highest
  ECE:   60 placed / 80 graduated  = 75.0%
  EEE:   28 placed / 45 graduated  = 62.2%
  Mech:  18 placed / 49 graduated  = 36.7% ← core sector challenge

SALARY STATISTICS (placed students):
  Maximum CTC:     ₹42.0L  (1 student — Google SWE, off-campus FAANG)
  Median CTC:      ₹4.5L
  Mean CTC:        ₹6.2L   (skewed by high outliers)
  Min CTC:         ₹2.4L
  ₹10L+ offers:   22 students (10.1%)
  ₹4L–10L offers: 142 students (65.1%)
  <₹4L offers:    54 students (24.8%)

COMPANIES (top recruiters by headcount):
  TCS: 42  |  Infosys: 22  |  Wipro: 18  |  HCL: 15  |  Accenture: 12
  Persistent: 9  |  Deloitte: 7  |  Amazon: 4  |  Others: 89

YEAR-OVER-YEAR TREND:
  2022–23 batch: 68.4% placement
  2023–24 batch: 70.1%
  2024–25 batch: 72.8%
  2025–26 batch: 74.1%  ← consistent improvement
  3-year average: 72.3%
```

---

## 2. NIRF Data Submission

```
NIRF — GRADUATION OUTCOMES (GO) PARAMETER
(National Institutional Ranking Framework — Annual Submission)

DATA FIELDS REQUIRED BY NIRF (Engineering):

PhD Awarded (5 years): 0  (GCEH has no PhD programme currently)

Placement & Higher Education:
  x = students placed: 218
  y = higher education: 36
  z = government/competitive: 12
  n = total graduating: 294

  GO Score = (x + y + z) / n = (218 + 36 + 12) / 294 = 266/294 = 90.5%

  Note: NIRF GO includes placement + higher studies + govt jobs (not just placement)
        This explains why NIRF GO score (90.5%) > pure placement rate (74.1%)

MEDIAN SALARY (NIRF format):
  Median salary of placed students: ₹4,50,000/yr (must exclude outliers per NIRF formula)
  NIRF salary score: Computed on log scale — ₹4.5L → moderate score

NIRF SUBMISSION TIMELINE:
  Data reference period: Academic year ending June 2026
  Submission deadline: Typically January–February (following year)
  EduForge: Pre-fills NIRF form from EduForge placement data
  Verification: NAAC Coordinator + Principal approve before submission
  Supporting data: Company-wise offer letters count, salary proof (aggregated)

NIRF SUBMISSION STATUS:
  2026 submission: ✅ Submitted January 2026 (for 2024–25 batch)
  2027 submission: ⬜ Pending (due February 2027 — current season data)
  Data collection: In progress (final season not concluded)
```

---

## 3. NAAC Criterion 5.2 Data

```
NAAC CRITERION 5.2 — STUDENT PROGRESSION

5.2.1 — Placement (out of 5 marks):
  Formula: % of students placed
  GCEH data: 74.1% (2025–26), 72.8% (2024–25), 70.1% (2023–24)
  3-year average: 72.3%
  Self-assessment score: 3.9/5 (NAAC lookup table: >70% → 4/5 is aspirational)

5.2.2 — Progression to Higher Education (out of 2 marks):
  Formula: % going to higher studies
  GCEH data: 12.2%
  Self-assessment: 1.4/2

5.2.3 — Students qualifying in national competitive exams (out of 3 marks):
  GATE, CAT, GRE, GMAT, UPSC, etc.
  GCEH data: GATE qualifiers (18), CAT (3), GRE (6), UPSC (2) = 29 students (9.9%)
  Self-assessment: 1.8/3

NAAC EVIDENCE (to be compiled):
  ✅ Offer letter copies (aggregated — not individual details)
  ✅ Company-wise placement register signed by Placement Officer
  ✅ Student declaration of higher education/employment (signed)
  ✅ NIRF submission acknowledgement
  ✅ Alumni survey (6-month post-graduation follow-up)
  ⬜ LinkedIn verification (optional but strengthens evidence)
```

---

## 4. Placement Dashboard

```
PLACEMENT REAL-TIME DASHBOARD — 2026–27 Season
As of 27 March 2027

SEASON PROGRESS:
  Students placed:       224 / 332 (67.5%)  ████████████████░░░
  Companies visited:     23 / ~30 expected
  Remaining season:      ~3 weeks (April drives planned)
  Projected final rate:  ~72% (based on pipeline)

SEGMENT BREAKDOWN:
  IT/Software:    172 (76.8% of placed)
  Core Engg:      18 (8.0%)
  BFSI/Analytics: 22 (9.8%)
  PSU/Govt:        5 (2.2%)
  Others:          7 (3.1%)

TOP SALARY OFFERS (current season):
  Goldman Sachs:  ₹22.0L   (2 students)
  Amazon:         ₹18.5L   (4 students)
  Microsoft:      ₹16.8L   (1 intern-to-PPO)
  Deloitte:       ₹7.0L    (5 students)

SOCIAL EQUITY TRACKER:
  SC/ST students placed: 18 / 26 (69.2%)   — on par with general batch
  OBC students placed:   62 / 89 (69.7%)   — on par
  Girl students placed:  78 / 112 (69.6%)  — on par ✅
  PwD student:           1 / 1 (100%) — Arun PwD placed at Infosys (DE role)
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/placement/statistics/annual/` | Annual placement statistics |
| 2 | `GET` | `/api/v1/college/{id}/placement/statistics/nirf/` | NIRF-formatted GO data |
| 3 | `GET` | `/api/v1/college/{id}/placement/statistics/naac/` | NAAC Criterion 5.2 data |
| 4 | `GET` | `/api/v1/college/{id}/placement/statistics/dashboard/` | Real-time season dashboard |
| 5 | `GET` | `/api/v1/college/{id}/placement/statistics/branch-wise/` | Branch-wise placement breakdown |

---

## 6. Business Rules

- NIRF data must be accurate and verifiable; inflating placement numbers (counting students who got offers but didn't join, or students in higher studies as "placed") is data fraud; NIRF has implemented verification mechanisms and has deranked/penalised institutions found submitting false data; EduForge computes NIRF-format data from actual offer acceptance records, not from manually entered numbers
- The NAAC metric counts "students placed" as those with confirmed employment, not just offer letters; students who received offers but declined (waiting for better opportunities) are not counted as placed; EduForge tracks offer acceptance status, not merely offer issuance
- Social equity tracking in placement is a NAAC Criterion 5.3 requirement (diversity and inclusion); institutions must demonstrate that placement outcomes are equitable across SC/ST, OBC, female, and PwD students; if significant gaps exist, the IQAC must document corrective measures (targeted training, mentoring)
- Off-campus placement (student placed independently without going through placement cell) should still be captured in the statistics; EduForge allows students to self-report off-campus offers with company + offer letter upload; this improves reported placement rates without distortion (the off-campus placements are real and verifiable)
- Mean vs median salary: Institutions often report mean CTC which is skewed by a few high-paying outliers (₹40L+ offers); NIRF uses median (more representative); NAAC peer teams ask both; EduForge reports both clearly with the outlier effect explained — this demonstrates analytical integrity rather than trying to hide it

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division E*
