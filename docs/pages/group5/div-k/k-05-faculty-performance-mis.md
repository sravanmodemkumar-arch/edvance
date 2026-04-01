# K-05 — Faculty Performance MIS

> **URL:** `/coaching/analytics/faculty/`
> **File:** `k-05-faculty-performance-mis.md`
> **Priority:** P2
> **Roles:** Academic Director (K5) · Branch Manager (K6) · Director (K7)

---

## 1. Faculty Performance Overview

```
FACULTY PERFORMANCE MIS — Q3 AY 2025–26
As of 31 March 2026

  FACULTY SCORECARD:
    Faculty         │ Subject  │ Attend% │ Avg Rating │ Student Gain │ Doubt SLA% │ Score
    ────────────────┼──────────┼─────────┼────────────┼──────────────┼────────────┼──────
    Ms. Kavita M.   │ English  │  98.4%  │  4.6/5.0  │   +6.2 pts   │   96.8%    │  A+
    Mr. Suresh K.   │ Quant    │  96.2%  │  4.3/5.0  │   +8.4 pts   │   92.4%    │  A
    Mr. Mohan R.    │ Reasoning│  94.8%  │  4.1/5.0  │   +7.8 pts   │   88.6%    │  A
    Mr. Ravi S.     │ GK/CA    │  92.6%  │  3.8/5.0  │   +5.2 pts   │   84.2%    │  B+
    Ms. Preethi L.  │ English  │  97.2%  │  4.4/5.0  │   +5.8 pts   │   94.2%    │  A
    Mr. Arjun T.    │ Quant    │  93.8%  │  4.2/5.0  │   +7.4 pts   │   90.6%    │  A
    Ms. Rekha N.    │ Reasoning│  95.4%  │  4.0/5.0  │   +6.6 pts   │   86.8%    │  A-
    Mr. Venkat R.   │ GK/CA    │  91.4%  │  4.1/5.0  │   +6.0 pts   │   88.4%    │  A-
    ────────────────┴──────────┴─────────┴────────────┴──────────────┴────────────┴──────

  SCORING METHODOLOGY:
    Attendance (25%):     >98% = A+, 95–98% = A, 90–95% = B+, <90% = B
    Student Rating (30%): >4.5 = A+, 4.0–4.5 = A, 3.5–4.0 = B+, <3.5 = B
    Student Gain (30%):   Top quartile = A+, 2nd = A, 3rd = B+, 4th = B
    Doubt SLA (15%):      >95% = A+, 90–95% = A, 85–90% = B+, <85% = B
```

---

## 2. Individual Faculty Detail

```
FACULTY DETAIL — Mr. Ravi S. (GK/CA)
Q3 Performance Review | Flagged for improvement

  ATTENDANCE RECORD:
    Classes scheduled (Q3):  48    │  Classes delivered: 44  (91.7%)
    Classes cancelled:         4    │  Reason: 2 medical, 2 exam duty
    Substitute arranged:       3    │  Gap class (makeup): 1

  STUDENT RATINGS TREND:
    Q1: 4.1/5.0  →  Q2: 4.0/5.0  →  Q3: 3.8/5.0  (declining ⚠️)
    Key feedback: "Less current affairs depth" "Relies too much on old material"

  SUBJECT SCORE ANALYSIS:
    Students' avg GK score (Mock#1):   26.5/50
    Students' avg GK score (Mock#25):  31.7/50  (+5.2 pts)
    Peer benchmark (other GK teacher): +6.0 pts average
    Gap vs peer:                        -0.8 pts ⚠️

  DOUBT RESOLUTION:
    Q3 doubts assigned:   64
    Resolved within 48h:  54  (84.4% — below 90% SLA target ⚠️)
    Unresolved >5 days:    4
    Student satisfaction: 3.6/5.0

  ACTION PLAN (agreed with Academic Director, 29 Mar 2026):
    1. Dedicate last 15 min of each session to last-30-days CA
    2. Weekly CA quiz (10 Qs) starting Apr 5
    3. Doubt resolution: must clear all pending by end of each week
    4. Review at end of Q4 — if no improvement, PIP to be initiated
```

---

## 3. Comparative Analytics

```
FACULTY COMPARATIVE ANALYSIS — All Faculty Q3

  BEST PRACTICES (from top performers):
    Ms. Kavita M. (4.6/5.0) — shares her session plan 48h before class
    Mr. Suresh K. (+8.4 pts gain) — "DI Clinic" extra sessions on Saturdays
    Mr. Mohan R. (88.6% doubt SLA) — uses video explanations for complex Qs

  PEER LEARNING SESSIONS (Academic Calendar Q4):
    Apr 10: Session structuring (Kavita M. presents to all faculty)
    Apr 24: Doubt resolution best practices (Suresh K. & Mohan R.)
    May 8:  Current affairs integration in GK classes (Venkat R.)

  FRANCHISE BENCHMARK:
    Main branch avg faculty rating:  4.2/5.0
    Franchise 1 (Secunderabad):      4.0/5.0
    Franchise 2 (Warangal):          3.8/5.0
    Franchise 3 (Nizamabad):         4.1/5.0
    Benchmark gap alert: Franchise 2 rating below 4.0 threshold ⚠️
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/analytics/faculty/?quarter=Q3-2026` | Faculty scorecard by quarter |
| 2 | `GET` | `/api/v1/coaching/{id}/analytics/faculty/{fid}/detail/` | Individual faculty performance detail |
| 3 | `GET` | `/api/v1/coaching/{id}/analytics/faculty/benchmark/` | Cross-branch faculty benchmarking |
| 4 | `GET` | `/api/v1/coaching/{id}/analytics/faculty/trends/?from=Q1&to=Q3&year=2026` | Rating trend over quarters |
| 5 | `POST` | `/api/v1/coaching/{id}/analytics/faculty/{fid}/action-plan/` | Record improvement action plan |

---

## 5. Business Rules

- Faculty performance is evaluated on four equally-weighted dimensions: attendance (the baseline expectation), student rating (perceived quality), student gain (actual learning outcome), and doubt SLA (responsiveness); no single dimension dominates; a faculty with a high student rating but low student gain may be popular but not effective; a faculty with high student gain but low rating may be rigorous but alienating; the composite score requires all four to be strong for an A+ designation
- Declining rating trends are more concerning than low absolute ratings; a faculty who consistently scores 4.0/5.0 is stable and predictable; a faculty who drops from 4.1 to 4.0 to 3.8 across three consecutive quarters is on a negative trajectory that, if unchecked, may reach 3.2 within 2 more quarters; the trend triggers early intervention (action plan, peer support, Academic Director coaching) before the rating becomes seriously problematic
- The faculty MIS is shared with individual faculty members only in their quarterly review — each faculty sees their own data, not peers'; the comparative benchmarking (peer learning sessions) is framed positively ("what Ms. Kavita does that works well") rather than negatively ("you scored lower than Ms. Kavita"); faculty performance data is sensitive HR information and is not disclosed to students, parents, or the broader staff; a data leak of a faculty member's performance scores could damage their professional reputation and TCC's working relationship with them
- A Performance Improvement Plan (PIP) is initiated only after two consecutive quarters of below-threshold performance, documented action plans that were not followed, and a formal conversation with the Academic Director; the PIP is not a punishment but a structured support framework with clear targets (e.g., raise rating from 3.8 to 4.1 within one quarter, improve doubt SLA from 84% to 90%); TCC's faculty employment contract specifies the PIP process and the consequences of not meeting PIP targets (including contract non-renewal)
- Cross-branch faculty benchmarking allows TCC to identify whether a performance issue is individual (one teacher at one branch) or systemic (all GK teachers across all branches performing poorly, suggesting a curriculum or material problem rather than a teaching problem); Franchise 2's rating below 4.0 triggers a call from the Academic Director to the franchise's academic coordinator to understand the root cause — it may be a staffing issue, student demographic difference, or a specific teacher's performance that the franchise needs to address

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division K*
