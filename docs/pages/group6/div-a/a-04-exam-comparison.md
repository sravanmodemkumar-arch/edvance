# A-04 — Exam Comparison Tool

> **URL:** `/exam/compare/?exams=appsc-group-2,tspsc-group-2,ssc-cgl`
> **File:** `a-04-exam-comparison.md`
> **Priority:** P2
> **Data:** `exam` table — up to 3 exams side-by-side, all fields pulled from DB

---

## 1. Comparison View

```
EXAM COMPARISON TOOL
Compare up to 3 exams side by side  |  All data from official sources

  SELECT EXAMS TO COMPARE:
    Exam 1: [APPSC Group 2 2025 ▼]     ×
    Exam 2: [TSPSC Group 2 2026 ▼]     ×
    Exam 3: [SSC CGL 2026 ▼]           ×
    [+ Add exam]   [Compare]

  ┌───────────────────────┬───────────────────────┬───────────────────────┐
  │  APPSC GROUP 2 2025   │  TSPSC GROUP 2 2026   │  SSC CGL 2026         │
  │  STATE — AP           │  STATE — TS           │  CENTRAL              │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Conducting Body      │                       │                       │
  │  APPSC                │  TSPSC                │  SSC                  │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Qualification        │                       │                       │
  │  Graduate             │  Graduate             │  Graduate             │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Age (General)        │                       │                       │
  │  18 – 42              │  18 – 44              │  18 – 32              │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Vacancies            │                       │                       │
  │  897                  │  ~783 (expected)      │  ~18,000              │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Salary (Entry Level) │                       │                       │
  │  ₹27,700 – ₹44,300   │  ₹28,940 – ₹45,420   │  ₹25,500 – ₹1,51,100 │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Posting Location     │                       │                       │
  │  Andhra Pradesh only  │  Telangana only       │  Pan-India            │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Exam Stages          │                       │                       │
  │  Prelims + Mains      │  Prelims + Mains      │  Tier-I + Tier-II     │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Language Medium      │                       │                       │
  │  Telugu / English     │  Telugu / English     │  English / Hindi      │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Total Marks          │                       │                       │
  │  600 (Pre+Mains)      │  600 (Pre+Mains)      │  590 (Tier-I+II)      │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Negative Marking     │                       │                       │
  │  -⅓ (Prelims)         │  -⅓ (Prelims)         │  -0.5 (both tiers)    │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Application Status   │                       │                       │
  │  Closed (Oct 2025)    │  Expected Sep 2026    │  Open (Apr–Jun 2026)  │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Exam Date            │                       │                       │
  │  Aug 2026 (tentative) │  Feb 2027 (tentative) │  Jul–Aug 2026         │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Competition Ratio    │                       │                       │
  │  476:1 (AY 2024)      │  500:1 (AY 2023)      │  202:1 (2024)         │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Domicile Required    │                       │                       │
  │  AP domicile for most │  TS domicile for most │  None                 │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  OBC Relaxation       │                       │                       │
  │  +3 years age         │  +3 years age         │  +3 years age         │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │  Mocks Available      │                       │                       │
  │  28 mocks             │  22 mocks             │  48 mocks             │
  ├───────────────────────┼───────────────────────┼───────────────────────┤
  │                       │                       │                       │
  │  [View Full Details]  │  [View Full Details]  │  [View Full Details]  │
  │  [Take Mock]          │  [Take Mock]          │  [Take Mock]          │
  │  [Save to My Exams]   │  [Set Alert]          │  [Apply Now]          │
  └───────────────────────┴───────────────────────┴───────────────────────┘

  SHARE:  [Copy comparison link]  — URL encodes exam slugs as query params
```

---

## 2. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/compare/?exams=appsc-group-2,tspsc-group-2,ssc-cgl` | Comparison data for up to 3 exams |

---

## 5. Business Rules

- The comparison URL (`?exams=slug1,slug2,slug3`) is shareable and bookmarkable; a student who compares APPSC Group 2 vs SSC CGL and wants to share the comparison with a friend sends the URL; the comparison renders from the DB at request time so any data update (vacancy revision, date change) is reflected immediately in the shared URL — no stale snapshot is shared; this is a significant advantage over static comparison articles on other websites
- The comparison tool renders only fields that are common across all selected exams; a field that is `null` for one exam is shown as "—" (not available / not applicable); if all three exams have `domicile_required = null`, the "Domicile Required" row is hidden entirely; if one has it and others don't, the row is shown with "—" for the exams without the field; this dynamic row rendering prevents empty rows that create visual clutter and confusion
- Competition ratio is computed from `vacancies` and `registered_applicants` for historical cycles; for exams where EduForge has data from multiple years, the ratio shows the most recent year with the data year labelled ("476:1 AY 2024"); for exams with no applicant count data (new exams added to the system), the field shows "Data unavailable" rather than an estimated or fabricated figure; accuracy over completeness is the principle — aspirants making career decisions must not be given fabricated competitive ratios
- Salary range shown in the comparison is the starting basic pay from the 7th Pay Commission pay matrix for Central government posts, or the state-equivalent pay matrix for state posts; allowances (HRA, DA, TA) vary by posting city and are not included in the comparison salary figure; a note below the comparison table reads: "Salary shown is basic pay only — HRA, DA, and other allowances are additional and vary by posting location"; this prevents aspirants from comparing basic pay across central and state exams without understanding the total compensation difference

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division A*
