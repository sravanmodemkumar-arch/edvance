# H-08 — HR MIS & Reports

> **URL:** `/college/hr/reports/`
> **File:** `h-08-hr-mis.md`
> **Priority:** P2
> **Roles:** HR Officer (S3) · Finance Manager (S4) · Principal/Director (S6) · Trust/Management (S7)

---

## 1. HR Dashboard

```
HR DASHBOARD — GCEH
As of 27 March 2027

STAFF STRENGTH:
  Teaching Faculty:     62 (58 regular + 4 contract)
  Non-Teaching Staff:   38 (28 permanent + 10 contract/outsourced)
  TOTAL:               100

VACANCIES:
  Open positions: 3 (CSE Asst. Prof., EEE Assoc. Prof., Mech Asst. Prof.)
  Recruitment status: Selection committee completed (Dr. Deepak R. for CSE)
                      EEE + Mech: Interviews scheduled May 2027

ATTRITION (2026–27 YTD):
  Resigned: 2 (1 CSE junior faculty — moved to startup; 1 non-teaching — personal)
  Retired: 1 (Dr. Ramaiah — July 2026)
  Attrition rate (YTD): 3/100 = 3.0%
  3-year avg attrition: 4.2% ← stable; industry avg for engineering colleges: 8–12%

PAYROLL THIS MONTH:
  Gross: ₹47.32L | Net: ₹37.48L | TDS: ₹3.82L | EPF: ₹8.10L
  Payslips issued: ✅ 100/100

LEAVE STATUS (today):
  On leave: 8 faculty (4 CL, 3 AL, 1 ML)
  Present: 54 faculty (87.1% attendance)

APPRAISAL (2025–26):
  Outstanding: 14 (22.6%) | Excellent: 26 (41.9%) | Good: 16 (25.8%)
  PIP active: 1 faculty (Mr. Anil K.)
  Next cycle: April 2027

COMPLIANCE:
  EPF: ✅ Filed up to Feb 2027 | Mar ECR due 15 Apr
  PT:  ✅ Filed up to Feb 2027 | Mar due 10 Apr
  TDS: ✅ Deposited; Q4 return due 31 May
  Form 16: Due 15 Jun 2027
```

---

## 2. Monthly HR Report

```
MONTHLY HR REPORT — March 2027

STAFFING CHANGES:
  Joins: 0
  Resignations: 0
  On notice period: Mr. Kiran T. (contract faculty — decided not to renew; ends 30 Apr)
  New vacancy: CSE — 1 (Mr. Kiran T. departure; replacement: Dr. Deepak R. joining Jun 2027)

PAYROLL SUMMARY:
  Total staff on payroll: 100
  Payroll processed: ✅ 8 March 2027
  Anomalies detected: 1 (Ms. Sunita K. salary appeared higher — reason: Feb backdated increment)
                       Reviewed and approved ✅

LEAVE SUMMARY:
  CL availed: 28 instances (18 faculty, 10 non-teaching)
  EL availed: 6 instances
  LOP: 2 instances (2 non-teaching staff)
  Academic Leave: 8 instances (4 FDPs, 4 conferences)

ATTRITION ANALYSIS:
  Faculty tenure distribution:
    <2 years: 8 faculty (highest attrition risk group)
    2–5 years: 18 faculty
    5–10 years: 22 faculty (most stable)
    >10 years: 14 faculty (long-tenured; succession planning needed)

UPCOMING HR EVENTS:
  15 Apr: EPF ECR deadline
  1 May: Annual increment initiation (for 1 Jul increment)
  Apr–May: Annual appraisal cycle begins
  Jun: 3 new faculty expected to join (Dr. Deepak + 2 others from ongoing recruitment)
```

---

## 3. NAAC HR Data

```
NAAC CRITERION 2.4 — FACULTY PROFILE (Data for SSR)

2.4.1 — Full-time teachers with PhD:
  PhD faculty: 25/62 = 40.3% (target: >60% for Grade A)
  3-year trend: 2023–24: 34.4%, 2024–25: 37.1%, 2025–26: 40.3% → improving ✅
  Self-assessment: 3/5 (below Grade A threshold)

2.4.2 — Average FDP days per teacher per year:
  2025–26: 7.2 days (62 faculty × 7.2 = 446 total FDP days)
  NAAC benchmark: >5 days → 4/5
  Self-assessment: 4/5 ✅

2.4.3 — Awards and recognitions:
  Best paper awards: 2 (2025–26)
  Fellowship/professional body memberships: 18 faculty (IEEE, ACM, ISTE)
  National/international awards: 1 (Dr. Suresh K. — Young Scientist Award, DST 2026)

2.4.4 — Faculty retention:
  Average tenure (current faculty): 7.8 years
  Faculty with >5 years: 36/62 = 58.1%
  Attrition (3-year avg): 4.2% (low — positive sign)

CRITERION 6.3 — FACULTY EMPOWERMENT:
  Financial support for conference travel: ✅ (₹4L FDP budget)
  Research seed funding: ✅ (₹12L/year)
  Sabbatical leave policy: Exists (1 semester after 7 years service) ✅
  Appraisal system: ✅ (documented, annual)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hr/reports/dashboard/` | HR dashboard |
| 2 | `GET` | `/api/v1/college/{id}/hr/reports/monthly/?month=2027-03` | Monthly HR report |
| 3 | `GET` | `/api/v1/college/{id}/hr/reports/naac/` | NAAC Criterion 2.4 + 6.3 data |
| 4 | `GET` | `/api/v1/college/{id}/hr/reports/attrition/` | Attrition analysis (trend) |
| 5 | `GET` | `/api/v1/college/{id}/hr/reports/payroll-annual/` | Annual payroll summary |

---

## 5. Business Rules

- Attrition tracking by tenure cohort (< 2 years, 2–5 years, etc.) is more actionable than aggregate attrition; most institutions track only the overall rate; knowing that junior faculty (<2 years) have 3× the attrition rate of mid-tenure faculty points to specific interventions (better onboarding, mentoring, competitive pay for new hires) rather than generic retention efforts
- The succession risk from 14 long-tenured faculty (>10 years) is as important as the attrition risk from junior faculty; when senior faculty retire or leave simultaneously, institutional knowledge is lost and accreditation metrics (PhD count, publications) drop suddenly; GCEH's succession plan should identify which senior faculty are within 5 years of retirement and plan replacements
- NAAC's Criterion 2.4 is often where institutions lose significant marks; improving from 40.3% to 60% PhD faculty (needed for Grade A) requires 12 more PhD faculty in a college of 62 — achievable over 3–4 years by hiring only PhD faculty and supporting existing faculty in PhD completion; EduForge tracks PhD enrolment and expected completion dates for this planning
- HR data confidentiality under DPDPA 2023 requires that salary data, performance data, and personal data of employees not be accessible to non-authorized staff; the HR dashboard visible to the Principal is different from the dashboard visible to HODs (no salary data) and from what HR staff see (all data); EduForge implements role-based data access for all HR screens
- Annual reports on HR (to Governing Body) are a governance requirement; the Governing Body cannot fulfil its oversight role if it only sees financial data without understanding the human capital health (attrition, vacancies, appraisal distribution, FDP investment); GCEH presents the HR MIS to the Governing Body at the September meeting annually

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division H*
