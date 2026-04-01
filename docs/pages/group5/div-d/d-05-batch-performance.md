# D-05 — Batch Performance Analytics

> **URL:** `/coaching/batches/performance/`
> **File:** `d-05-batch-performance.md`
> **Priority:** P2
> **Roles:** Batch Coordinator (K4) · Academic Director (K5) · Branch Manager (K6)

---

## 1. Batch Score Overview

```
BATCH PERFORMANCE — SSC CGL MORNING (240 students)
Last 5 Full Mocks  |  As of 30 March 2026

  Test           │ Date    │ Avg/200 │ Top   │ < 80  │ Median │ StdDev │ Cutoff est.
  ───────────────┼─────────┼─────────┼───────┼───────┼────────┼────────┼────────────
  Full Mock #23  │ 15 Mar  │  124.6  │ 178   │  28   │  126   │  24.2  │ 145
  Full Mock #22  │ 28 Feb  │  118.4  │ 172   │  36   │  118   │  26.1  │ 143
  Full Mock #21  │ 15 Feb  │  112.8  │ 168   │  44   │  112   │  27.4  │ 142
  Full Mock #20  │ 01 Feb  │  108.2  │ 163   │  52   │  108   │  29.0  │ 141
  Full Mock #19  │ 18 Jan  │  102.4  │ 158   │  64   │  102   │  30.2  │ 140

  Trend: +22.2 pts over 5 mocks ✅ | StdDev decreasing ✅ | Avg approaching cutoff ⚠️
  ── Cutoff estimate: 145 | Students above cutoff: 68/240 (28.3%) ──
```

---

## 2. Subject-Wise Accuracy (Cross-Batch Heatmap)

```
SUBJECT ACCURACY — SSC CGL MORNING vs EVENING (March 2026)

  Subject          │ Morning Avg │ Evening Avg │ Diff  │ Flag
  ─────────────────┼─────────────┼─────────────┼───────┼────────────────────
  Quant (25)       │   16.4      │   15.8      │ +0.6  │ ✅ Morning better
  English (25)     │   17.2      │   18.1      │ -0.9  │ ⚠️ Evening better
  Reasoning (25)   │   18.6      │   17.4      │ +1.2  │ ✅ Morning better
  GK/CA (25)       │   13.8      │   13.2      │ +0.6  │ ✅ Morning better
  ─────────────────┴─────────────┴─────────────┴───────┴────────────────────
  TOTAL (100)      │   66.0      │   64.5      │ +1.5  │ ✅ Morning leads

  NOTE: English gap — Evening batch faculty (Ms. Kavita Menon) on leave for
  2 weeks in March; substitute faculty covered. English score dip expected.
  Recovery session scheduled Apr 2–4 (extra classes) ✅
```

---

## 3. Top Performers & At-Risk Spotlight

```
TOP 10 STUDENTS — SSC CGL MORNING (Mock #23, 15 Mar 2026)

  Rank │ Student           │ Score/200 │ Quant │ English │ Reasoning │ GK
  ─────┼───────────────────┼───────────┼───────┼─────────┼───────────┼────
  1    │ Akhil Kumar       │  178/200  │ 24    │  22     │   24      │ 23  ← Rank 1 batch
  2    │ Rajesh Kumar      │  172/200  │ 22    │  23     │   24      │ 22
  3    │ Meena Kapoor      │  168/200  │ 21    │  24     │   22      │ 21
  4    │ Divya Sharma      │  165/200  │ 23    │  21     │   22      │ 20
  5    │ Suresh P.         │  162/200  │ 21    │  22     │   20      │ 22
  ...  (5 more)

STUDENTS MOST IMPROVED (Mock #23 vs Mock #19):
  1. Lakshmi T. (TCC-2409): +38 pts (82→120) → moved from Weak to Average
  2. Kiran S. (TCC-2421):   +34 pts (78→112) → moved from Critical to Average
  3. Anitha K. (TCC-2408):  +28 pts (98→126) → moved from Average to Good

AT-RISK SPOTLIGHT (below 80 in Mock #23):
  ⚠️ 28 students scored < 80/200 — risk of demoralization
  Action: Group counselling session scheduled Apr 1 (3 groups × 10 students)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/performance/tests/?tests=5` | Score overview across last N tests |
| 2 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/performance/subjects/?month=2026-03` | Subject accuracy heatmap |
| 3 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/performance/top/?test={tid}&limit=10` | Top performers in a test |
| 4 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/performance/improved/?from={t1}&to={t2}` | Most improved students between two tests |
| 5 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/performance/at-risk/?threshold=80` | Students below score threshold |
| 6 | `GET` | `/api/v1/coaching/{id}/batches/performance/compare/?b1={bid1}&b2={bid2}` | Cross-batch performance comparison |

---

## 5. Business Rules

- Batch performance data is aggregated at the section level (Quant, English, Reasoning, GK) and overall; subject-level breakdowns visible to the Batch Coordinator can be shared with faculty only in aggregate form — individual student scores per subject are not shared coordinator-to-faculty directly; faculty access their own subject performance data through the Faculty portal (C-06) with subject-scoped views; this prevents coordinators from becoming information brokers between faculty
- The "cutoff estimate" shown in the batch overview is generated by the platform based on previous year SSC CGL cutoffs and current mock difficulty calibration; it is an estimate, not a guarantee; the platform shows a disclaimer that actual cutoffs depend on candidate pool, paper difficulty, and normalisation; coordinators must not present this as a prediction to students or parents — it should be framed as "your batch median vs estimated passing threshold"
- Cross-batch comparison is restricted to the Academic Director and Branch Manager; coordinators can see their own batch's trend but cannot view competing batch data (e.g., SSC CGL Morning coordinator should not see Banking Batch scores); this prevents inter-coordinator rivalry and ensures coordinators focus on their own batch's improvement rather than benchmarking against peers
- "Most improved" tracking serves two purposes: recognising student effort (featured in batch WhatsApp group by coordinator) and validating teaching effectiveness (an improvement of 30+ points over 5 tests is evidence of effective remedial teaching, factored into the faculty's quarterly review); coordinators must tag the contributing faculty when recording improvement milestones, creating a direct link between teaching input and student output
- Batch performance reports are shared with parent groups (for minor student batches) in aggregate form only — batch average, top score, and pass-rate estimate; individual student scores are never shared in group formats; parents who want their child's individual performance must access it through the Parent Portal (O-01) with their own login; coordinators sharing individual student scores in batch WhatsApp groups violates DPDPA 2023 data minimisation principles

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division D*
