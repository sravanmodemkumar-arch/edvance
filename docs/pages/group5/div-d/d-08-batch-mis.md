# D-08 — Batch MIS & Reports

> **URL:** `/coaching/batches/reports/`
> **File:** `d-08-batch-mis.md`
> **Priority:** P2
> **Roles:** Batch Coordinator (K4) · Branch Manager (K6) · Academic Director (K5)

---

## 1. Monthly MIS Report

```
MONTHLY MIS — SSC CGL MORNING BATCH
March 2026  |  Generated: 30 Mar 2026, 11:00 PM

  ┌────────────────────────────────────────────────────────────────────────────┐
  │  BATCH HEALTH SCORE:  82 / 100  ✅ Good                                   │
  │  Attendance: 85.4%  |  Avg Score: 124.6/200  |  At-Risk: 5.8%            │
  └────────────────────────────────────────────────────────────────────────────┘

  ACADEMIC SUMMARY:
    Tests conducted:         8  (6 subject sprints, 2 full mocks)
    Avg full mock score:   124.6 / 200
    Score trend (Jan–Mar): 102.4 → 124.6  (+22.2 pts ✅)
    Students above cutoff: 68 / 240  (28.3%)

  ATTENDANCE SUMMARY:
    Working days:    26
    Batch avg:       85.4%  (target: 85% ✅)
    < 60%:            8 students — counsellor action initiated ✅
    Corrections made: 12 (all audited)

  FACULTY DELIVERY:
    Scheduled classes:    52
    Delivered:            50  (96.2% delivery rate)
    Cancelled:             2  (medical — substitutes arranged ✅)
    Late submission (attendance):  3 instances ⚠️

  FEE COLLECTION:
    Monthly due (batch):    ₹ 3,60,000  (240 × ₹1,500/month)
    Collected:              ₹ 3,18,000  (88.3%)
    Pending:                ₹  42,000   (29 students)
    Overdue > 30 days:      ₹  24,000   (18 students) → escalated ✅

  CONTENT COVERAGE:
    Curriculum completion (Mar):  82% of planned topics ✅
    Caselet DI: 0% coverage (gap noted — 2 extra sessions Apr) ⚠️

  [Download PDF]   [Share with Branch Manager]   [Archive]
```

---

## 2. Exam-Result Tracking (Post-Exam)

```
RESULT TRACKING — SSC CGL 2024 (TCC Alumni)
Results declared: 25 Feb 2026

  TCC Students appeared (SSC CGL 2024):   184
  Students from SSC CGL Morning batch:      96

  RESULTS:
    Tier-I cleared:           52 / 96  (54.2%) ✅ (national avg: ~38%)
    Tier-I + Tier-II cleared: 28 / 96  (29.2%) ✅
    Final selection (post DV): 18 / 96  (18.8%)

  POSTING BREAKDOWN (18 selected):
    CSS (Central Secretariat):   4
    Income Tax Inspector:        6
    CBI Sub-Inspector:           2
    Auditor (AG):                4
    Tax Assistant:               2

  vs PREVIOUS COHORT (2023):
    Final selections: 12 / 88 (13.6%) → 18 / 96 (18.8%) ↑ +5.2% ✅

  [Export Results]   [Use in Marketing Report]   [Flag Success Stories]
```

---

## 3. Report Builder (Custom MIS)

```
CUSTOM REPORT BUILDER

  Report Name:  [Q1 2026 Academic Summary — SSC CGL Morning     ]
  Period:       [01 Jan 2026] to [31 Mar 2026]
  Batch:        [SSC CGL Morning ▼]

  Include sections:
    [✓] Attendance summary (monthly, with bands)
    [✓] Test performance (score trend, subject breakdown)
    [✓] At-risk student list (anonymised for external sharing)
    [✓] Fee collection status
    [✓] Faculty delivery rates
    [ ] Individual student scores (internal use only)
    [ ] Parent communication log

  Format:  (●) PDF  ( ) Excel  ( ) Dashboard view only
  Access:  (●) This coordinator + Branch Manager  ( ) All staff  ( ) External share

  [Generate Report]   [Save as Template]   [Schedule Monthly Auto-report]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/mis/?month=2026-03` | Monthly MIS report for a batch |
| 2 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/results/?exam=ssc-cgl-2024` | Post-exam result tracking |
| 3 | `POST` | `/api/v1/coaching/{id}/batches/{bid}/reports/custom/` | Generate custom MIS report |
| 4 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/reports/` | All generated reports for a batch |
| 5 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/mis/health-score/?month=2026-03` | Batch health score calculation |

---

## 5. Business Rules

- The monthly MIS report is auto-generated on the last working day of the month and distributed to the Batch Coordinator, Academic Director, and Branch Manager; coordinators cannot prevent this auto-distribution — the report serves as the branch's management information for the month; the only control coordinators have is adding a "coordinator's note" section (max 200 words) that appears at the top of the report for context
- The "Batch Health Score" (0–100) is a composite metric: 40% attendance score, 40% academic improvement score, 20% fee collection rate; a batch with excellent scores but poor attendance (e.g., students scoring well but skipping class) gets a lower health score, signalling a risk of batch attrition; a batch with high attendance but stagnant scores signals a teaching effectiveness issue; both dimensions are needed for a complete picture
- Post-exam result tracking is a mandatory activity for all batches whose exam cycle has concluded; coordinators must log whether each enrolled student appeared for the exam and their result (cleared/not cleared/result pending); this data feeds TCC's success rate published on the website and in marketing material; result data must be collected with student consent (they are adults and result is their personal data); students who don't share results are counted as "result not reported" — not as "failed"
- The custom report builder restricts "individual student scores" from being included in externally-shareable reports; even internally, a report containing individual performance data requires a data-classification marking ("Internal — Confidential"); these reports cannot be printed in batch and left on desks; the system logs every report generation and download with user identity, which serves as accountability for data handling
- MIS data from branch batches rolls up to the franchise performance dashboard (A-05) for franchise locations; franchise batch coordinators must submit MIS by the 3rd of the following month; late submission (after the 5th) triggers an automatic escalation to the franchise operations team; persistent late submission is a contractual performance default under TCC's franchise agreement and can result in franchise support being suspended

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division D*
