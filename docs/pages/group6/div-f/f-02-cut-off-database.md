# F-02 — Cut-off Database

> **URL:** `/exam/{slug}/cutoffs/`
> **File:** `f-02-cut-off-database.md`
> **Priority:** P1
> **Data:** `cut_off` table — historical + current, category-wise, stage-wise, for any exam

---

## 1. Cut-off View (Per Exam)

```
CUT-OFFS — {exam.name}
[Example: APPSC Group 2 — All Cycles]
Tab: [Cut-offs] active on exam detail page (B-01)

  CURRENT CYCLE: APPSC Group 2 — 2025
    Status: Exam not yet conducted → Cut-off TBD
    [Projected cut-off from predictor (F-03): 76–82/150 General]

  HISTORICAL CUT-OFFS:
  ┌─────────────────────────────────────────────────────────────────────┐
  │  APPSC Group 2 — 2022 (Prelims — 150 marks)                        │
  │  Category   │ Cutoff │ Qualified │ Applied  │ Selection Rate        │
  │  ───────────┼────────┼───────────┼──────────┼──────────────         │
  │  General    │ 72/150 │  18,400   │ 3,82,000 │ 4.82%                │
  │  BC-A       │ 68/150 │   8,600   │ 1,24,000 │ 6.94%                │
  │  BC-B       │ 66/150 │  12,400   │ 1,46,000 │ 8.49%                │
  │  BC-C       │ 64/150 │   4,200   │   48,000 │ 8.75%                │
  │  BC-D       │ 62/150 │   6,800   │   62,000 │ 10.97%               │
  │  BC-E       │ 60/150 │   2,400   │   28,000 │ 8.57%                │
  │  SC         │ 58/150 │  14,200   │ 1,12,000 │ 12.68%               │
  │  ST         │ 52/150 │   6,400   │   42,000 │ 15.24%               │
  │  EWS        │ 68/150 │   4,800   │   48,000 │ 10.00%               │
  │  PH-Gen     │ 48/150 │     840   │    8,400 │ 10.00%               │
  ├─────────────┴────────┴───────────┴──────────┴──────────────         │
  │  FINAL MERIT CUT-OFFS (Mains + Interview — 675 marks):              │
  │  General: 298/675 | BC-B: 264/675 | SC: 248/675 | ST: 228/675      │
  └─────────────────────────────────────────────────────────────────────┘

  CUT-OFF TREND (General category, Prelims):
    2012: 52/150  →  2016: 60/150  →  2019: 68/150  →  2022: 72/150
    📈 Rising trend: ~4 marks per cycle
```

---

## 2. Cut-off Data Model

```
cut_off {
  id,
  exam_id,
  cycle_year,            ← 2022, 2019, 2016…
  stage,                 ← "prelims" | "mains" | "final"
  category,              ← "general" | "bc_a" | "bc_b" | "sc" | "st" | "ews" | "ph_gen" | any
  cut_off_marks,
  total_marks,           ← denominator (150 for prelims, 675 for final)
  qualified_count,       ← how many qualified at this stage
  applied_count,         ← how many applied (for competition ratio)
  source_url,            ← official document where this data was published
}
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/{slug}/cutoffs/?stage=prelims` | Cut-offs for an exam by stage |
| 2 | `GET` | `/api/v1/exam/{slug}/cutoffs/trend/?category=general` | Cut-off trend across cycles |
| 3 | `GET` | `/api/v1/exam/cutoffs/compare/?exams=appsc-group-2,tspsc-group-2` | Cross-exam cut-off comparison |

---

## 5. Business Rules

- Cut-off data is sourced exclusively from official conducting body publications (result notifications, merit list PDFs); community-reported cut-offs ("someone on Telegram said the cut-off was 74") are never entered into the database; every `cut_off` record must have a `source_url` pointing to the official document; during the gap between result declaration and official cut-off publication, the cut-off fields show "Awaiting official publication" rather than estimates
- Category-wise cut-offs are critical for aspirants because they directly determine whether a specific individual clears or not; a General category aspirant scoring 71/150 in APPSC Group 2 2022 Prelims did NOT qualify (cut-off was 72); a BC-B aspirant scoring 66/150 qualified; the cut-off database must store all categories published by the conducting body — the `category` field is a string (not an enum) to accommodate any state's reservation category structure without schema changes
- Cut-off trends are the most requested analytical feature; aspirants planning their preparation strategy want to know: "if the cut-off has been rising 4 marks per cycle, what should I target for 2025?"; the trend chart is computed from `cut_off.cut_off_marks WHERE exam_id AND stage AND category ORDER BY cycle_year`; a linear regression line is overlaid showing the projected cut-off for the next cycle; the projection is clearly labelled "estimate" and not presented as the actual expected cut-off
- Cross-exam cut-off comparison enables strategic decisions; an AP domicile aspirant choosing between APPSC Group 2 (cut-off 72/150, 48% threshold) and SSC CGL (cut-off 143.5/200, 71.75% threshold) can see that APPSC Group 2's relative cut-off is lower — meaning a wider range of scores qualify; this comparison must normalise the cut-offs to a common scale (percentage of total marks) since different exams have different total marks
- The `applied_count` field (how many people applied for this exam cycle) is essential for computing competition ratio; "72/150 cut-off with 3.82 lakh applicants" is a very different difficulty than "72/150 with 50,000 applicants"; the competition ratio is prominently displayed alongside the cut-off to give aspirants a complete picture of the difficulty landscape; a falling cut-off with rising applicants usually means the exam was harder (not that competition decreased)

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division F*
