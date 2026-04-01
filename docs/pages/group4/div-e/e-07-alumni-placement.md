# E-07 — Alumni Placement & Outcome Tracking

> **URL:** `/college/placement/alumni/`
> **File:** `e-07-alumni-placement.md`
> **Priority:** P2
> **Roles:** Training & Placement Coordinator (S4) · NAAC Coordinator (S4) · Principal/Director (S6)

---

## 1. Alumni Employment Tracking

```
ALUMNI EMPLOYMENT TRACKING — GCEH

PURPOSE:
  NAAC Criterion 5.2.2 — Student outcome tracking (required evidence)
  NIRF Graduation Outcomes — employment data 1 year after graduation
  Placement cell improvement — understanding long-term career trajectories
  Alumni engagement — identifying potential guest lecturers, mentors, recruiters

6-MONTH SURVEY (mandatory NAAC evidence):
  Timing: 6 months after graduation (December following June graduation)
  Method: EduForge survey link sent to alumni email + SMS
  Response rate 2025–26 batch (6-month survey, Dec 2025): 68.4% (201/294)
  Non-response handling: 3 reminders via WhatsApp (class group coordinators help)

SURVEY RESULTS — Batch 2021–25 (6-month survey, December 2025):
  Employment (job):          174 / 201 responded (86.6% of respondents)
  Higher education (PG):      18 / 201 (9.0%)
  Entrepreneurship:            4 / 201 (2.0%)
  Seeking employment:          5 / 201 (2.5%)

  Imputed full batch (294 total):
    Employment: ~83%  (applying 68.4% response bias assumption — upper bound)
    This aligns with placement records: 74.1% placed through placement cell +
    self-placed + post-graduation employment ≈ 80–85%

1-YEAR FOLLOW-UP:
  Timing: 12 months after graduation (June following year)
  Target: Capture job changes, promotions, higher education starts
  2025 batch (1-year survey, June 2026 — in progress)
    Response: 52.1% (smaller as contact details decay after 1 year)
```

---

## 2. Alumni Career Progression

```
NOTABLE ALUMNI CAREER TRAJECTORIES (2020–26 batches)

CAREER PROGRESSION EXAMPLES:
  Batch 2020–24:
    Priya R. (CSE): TCS → promoted to Senior Engineer in 18 months
    Arun K. (ECE): Wipro → switched to Qualcomm (₹14L → ₹28L jump at 2 yrs)
    Vikram S. (Mech): BHEL → appeared GATE 2025 → IIT Bombay M.Tech ✅

  Batch 2019–23:
    Deepika V. (CSE): Amazon SDE-1 → SDE-2 (₹18L → ₹32L, 2 years)
    Suresh T. (EEE): ONGC → appeared UPSC Engineering Services → Selected ✅
    Rohini P. (IT): Started SaaS startup (HR-tech) → raised ₹50L seed funding

ALUMNI LINKEDIN INTEGRATION:
  Optional: Alumni can link LinkedIn profile to EduForge alumni network
  Purpose: Placement cell can see career progression; identify mentors/recruiters
  DPDPA: LinkedIn link is voluntary; EduForge does not scrape LinkedIn
  Coverage: 142 / 294 (48.3%) of recent batch linked LinkedIn

COMPANY REFERRALS BY ALUMNI:
  2026–27 season: 18 companies approached via alumni referral
  Alumni-referred drives: 4 companies scheduled (RetailTech, FinEdge, CloudBit, InnoSystems)
  Alumni as guest faculty: 12 lectures (NAAC criterion 1.3 — industry interface evidence)
  Alumni mentors: 48 student-alumni mentor pairs (Placement cell facilitated)
```

---

## 3. Placement Outcome Report (NAAC Format)

```
NAAC CRITERION 5.2 — EVIDENCE COMPILATION

FIVE-YEAR PLACEMENT TREND:
  2021–22 batch: 64.2% placement  (post-COVID recovery year)
  2022–23 batch: 68.4%
  2023–24 batch: 70.1%
  2024–25 batch: 72.8%
  2025–26 batch: 74.1%  ← most recent
  5-year average: 69.9%

HIGHEST PACKAGE (5 years):
  2021–22: ₹28.0L  (Google — off-campus FAANG)
  2022–23: ₹35.0L  (Microsoft — campus drive)
  2023–24: ₹40.0L  (Goldman Sachs + Amazon)
  2024–25: ₹42.0L  (Google SWE — off-campus)
  2025–26: ₹22.0L  (Goldman Sachs — campus) [Note: FAANG off-campus not captured this yr]

MEDIAN PACKAGE TREND:
  2021–22: ₹3.6L → 2025–26: ₹4.5L (CAGR +5.7% — slightly above inflation)

NAAC SELF-ASSESSMENT (Criterion 5.2.1 — Placement):
  Score = f(% placed) — 5-year average 69.9%
  NAAC metric:
    >90%: Full marks
    75–90%: 4/5
    60–75%: 3.5/5 ← GCEH range
    50–60%: 3/5
    <50%: 2/5
  Self-assessment: 3.5/5 (conservative; aiming for 4/5 next cycle)

EVIDENCE DOCUMENTS:
  ✅ Offer letter samples (10 per year, across companies — anonymised)
  ✅ Placement register (all students, all companies, signed)
  ✅ Alumni survey summary reports (3 years)
  ✅ NIRF submission acknowledgements
  ✅ LinkedIn profiles (18 notable alumni for illustration)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/placement/alumni/` | Alumni employment records |
| 2 | `POST` | `/api/v1/college/{id}/placement/alumni/survey/` | Submit alumni survey response |
| 3 | `GET` | `/api/v1/college/{id}/placement/alumni/statistics/` | Alumni outcome statistics (5-year) |
| 4 | `GET` | `/api/v1/college/{id}/placement/alumni/naac-report/` | NAAC Criterion 5.2 evidence package |

---

## 5. Business Rules

- Alumni tracking requires continued engagement; contact details degrade after graduation (email becomes inactive, phone changes); maintaining a WhatsApp group per batch with class representative as coordinator has proven effective in keeping 60–70% of alumni reachable; EduForge exports batch contact list (with consent) for this purpose
- NAAC expects "documented systematic process" for alumni tracking — not just numbers; a placement cell that maintains structured 6-month and 1-year surveys, documented follow-up methodology, and consistent evidence over 3 cycles scores much higher than one that presents data without process documentation
- Alumni sharing their placement/career details in surveys is voluntary; DPDPA 2023 applies — alumni must have consented to continued contact for professional tracking purposes at the time of graduation; EduForge's exit process includes a consent capture for post-graduation surveys that is kept separate from college communications consent
- Alumni who become recruiters at their companies are the most valuable long-term placement network; the placement cell must actively identify and cultivate these relationships; EduForge flags alumni who transition to HR/recruitment roles (based on LinkedIn sync or survey responses) for proactive engagement by the Placement Coordinator

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division E*
