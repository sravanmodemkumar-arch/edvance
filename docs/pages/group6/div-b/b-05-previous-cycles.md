# B-05 — Previous Cycles & History

> **URL:** `/exam/{exam-slug}/history/`
> **File:** `b-05-previous-cycles.md`
> **Priority:** P2
> **Data:** `exam_cycle` table — one record per historical cycle of each exam; links to cut-offs, results, PYQs

---

## 1. Exam History View

```
EXAM HISTORY — {exam.name}
[Example: APPSC Group 2]
Tab: [History] active

  ALL CYCLES  [from exam_cycle WHERE exam_slug = 'appsc-group-2' ORDER BY year DESC]
  ┌───────────────────────────────────────────────────────────────────────────────────┐
  │  Year    │ Notification │ Vacancies │ Applicants │ Ratio  │ General Cutoff│ Status │
  ├──────────┼──────────────┼───────────┼────────────┼────────┼───────────────┼────────┤
  │  2025    │  Oct 2025    │    897    │  4,28,000  │ 477:1  │  TBD          │ Active │
  │  2022    │  Dec 2022    │    783    │  3,82,000  │ 488:1  │  268/600      │ Done ✅│
  │  2019    │  Jun 2019    │    645    │  2,96,000  │ 459:1  │  254/600      │ Done ✅│
  │  2016    │  Aug 2016    │    514    │  2,12,000  │ 412:1  │  238/600      │ Done ✅│
  │  2012    │  Mar 2012    │    402    │  1,48,000  │ 368:1  │  222/600      │ Done ✅│
  └───────────────────────────────────────────────────────────────────────────────────┘

  TREND ANALYSIS:
    Vacancies trend:    402 → 514 → 645 → 783 → 897  (↑ increasing)
    Applicants trend:   1.48L → 2.12L → 2.96L → 3.82L → 4.28L  (↑ increasing faster)
    Competition ratio:  368 → 412 → 459 → 488 → 477  (fluctuating — slight decrease in 2025)
    Cutoff trend:       222 → 238 → 254 → 268 → TBD  (↑ steadily increasing)
    Projected 2025:     272–280/600 (based on trend — see rank predictor F-03)

  PATTERN CHANGES:
    2022: Prelims pattern changed — 150 Qs in 150 min (was 120 in 120)
    2019: TS-specific topics added to Mains Paper 4
    2016: Age relaxation increased from 40 to 42 for OBC
```

---

## 2. Cycle Detail (Drill-Down)

```
CYCLE DETAIL — APPSC Group 2 — 2022
[User clicked on a historical cycle]

  TIMELINE:
    Notification:    Dec 2022
    Application:     Dec 2022 – Jan 2023
    Prelims:         May 2023  |  Result: Jul 2023
    Mains:           Dec 2023  |  Result: Aug 2024
    Interview:       Oct 2024  |  Final result: Dec 2024
    Total duration:  24 months (notification to final result)

  CUT-OFFS (2022):
    Category  │ Prelims │ Mains    │ Final (Mains+Interview)
    ──────────┼─────────┼──────────┼────────────────────────
    General   │  72/150 │  268/600 │  298/675
    BC-A      │  66/150 │  248/600 │  272/675
    BC-B      │  64/150 │  242/600 │  264/675
    SC        │  58/150 │  224/600 │  248/675
    ST        │  52/150 │  206/600 │  228/675
    EWS       │  68/150 │  258/600 │  286/675

  RESOURCES FROM THIS CYCLE:
    Previous year question paper (Prelims): [Download PDF — Telugu] [English]
    Previous year question paper (Mains Paper 1–4): [Download each]
    Answer keys (official): [Download]
    Topper interviews: 3 available  [Watch]

  [View cut-off analysis →]  [Practice PYQs from this cycle →]
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/{slug}/history/` | All cycles for this exam |
| 2 | `GET` | `/api/v1/exam/{slug}/history/{cycle_year}/` | Cycle detail — timeline, cut-offs, PYQs |
| 3 | `GET` | `/api/v1/exam/{slug}/history/trends/` | Computed trend data (vacancy, applicant, cutoff) |

---

## 5. Business Rules

- Exam history operates at the exam-slug level (e.g., "appsc-group-2"), not the cycle level; the cycle year is a dimension within the exam; this means `appsc-group-2-2025` and `appsc-group-2-2022` are not separate exams in the DB — they are cycles of the same exam `appsc-group-2`; the current active cycle is the one shown on the exam detail page (B-01); the history page shows all past cycles; this structure ensures that trend analysis works automatically as new cycles are added
- Cut-off data from previous cycles is one of the most valuable datasets for aspirants; the content team enters category-wise cut-offs from official result notifications published by APPSC/TSPSC/SSC; the data must match the official source exactly — a cut-off entered as 268 when the official figure is 264 could cause an aspirant to over-estimate the difficulty and change their strategy; every cut-off entry links to the official source PDF for verification
- Trend projections ("Projected 2025: 272–280/600") are statistical extrapolations and must be labelled "Estimated based on historical trends — not an official figure"; the projection model uses linear regression on the last 4–5 cycles' cut-offs, adjusted for vacancy change and applicant count change; it is useful as a rough guide but not reliable as a planning tool; aspirants who target "just above the projected cut-off" are at risk because actual cut-offs can spike unpredictably (a difficult paper lowers the cut-off; an easy paper raises it)
- Pattern changes across cycles are documented in the history to help aspirants understand what has changed; an aspirant using 2016 APPSC Group 2 PYQs for 2025 preparation must know that the Prelims pattern changed in 2022 (120 Qs → 150 Qs, timing changed); without this context, practicing old-pattern papers gives a false sense of preparation; the content team annotates major pattern changes on the history page for every cycle where a significant change occurred
- Previous year question papers (PYQs) from each cycle are stored as downloadable PDFs and also digitised as individual questions in the question bank (E-05) tagged by cycle year, exam stage, and syllabus node; a student can either download the full paper for a timed practice run, or practice individual PYQs topic-by-topic; the digitised PYQs are critical for analytics — the system can compute topic-wise frequency across cycles ("Polity: 12 Qs in 2022, 14 Qs in 2019, 10 Qs in 2016") which feeds the syllabus weightage estimation (B-02)

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division B*
