# D-02 — My Eligible Exams

> **URL:** `/exam/eligibility/my-eligible/`
> **File:** `d-02-eligible-exams.md`
> **Priority:** P1
> **Data:** Runs eligibility engine (D-01) against ALL active exams for logged-in user; cached and refreshed daily

---

## 1. Eligible Exams View

```
MY ELIGIBLE EXAMS — Ravi Kumar
Profile: Male · 24 yrs · OBC (BC-B) · AP Domicile · Graduate (B.Com)
Eligible for: 62 of 198 active exams ✅

  OPEN NOW (application period active) — 4 exams
  ┌──────────────────────────────────────────────────────────────────────┐
  │  SSC CGL 2026          │ Central  │ Apply by: 30 Jun 2026  │ [Apply]│
  │  VRO/VRA AP 2025       │ State-AP │ Apply by: 10 Apr 2026  │ [Apply]│
  │  TS Police Constable 25│ State-TS │ Apply by: 15 Apr 2026  │ [Apply]│
  │  ONGC AEE 2026         │ PSU      │ ❌ Ineligible (BE req) │        │
  └──────────────────────────────────────────────────────────────────────┘
  Wait — ONGC shows here? No — ONGC requires B.E, user is B.Com → FILTERED OUT.
  Only truly eligible exams appear in this list.

  UPCOMING (notification expected within 90 days) — 8 exams
  ┌──────────────────────────────────────────────────────────────────────┐
  │  IBPS PO 2026           │ Banking  │ Expected: Jun 2026 │ [Alert] │
  │  IBPS Clerk 2026        │ Banking  │ Expected: Jul 2026 │ [Alert] │
  │  SSC CHSL 2026          │ Central  │ Expected: Sep 2026 │ [Alert] │
  │  APPSC Group 3 2026     │ State-AP │ Expected: Aug 2026 │ [Alert] │
  │  AP DSC (SGT) 2026      │ Teaching │ ❌ Needs B.Ed/D.El.Ed│         │
  │  TSPSC Group 4 2026     │ State-TS │ ❌ TS domicile req  │         │
  │  [+ 2 more eligible]    │          │                     │         │
  └──────────────────────────────────────────────────────────────────────┘
  (Ineligible exams shown separately only if user explicitly enables "show why I'm not eligible")

  SORT: [Deadline Soon ▼]  [Vacancies]  [Salary]  [Competition Ratio]
  FILTER: [All types ▼]  [State: AP ▼]  [Qualification ▼]

  ELIGIBLE BY TYPE:
    Central:    18 exams
    AP State:   16 exams
    Banking:     8 exams
    TS State:    2 exams (only non-domicile-restricted posts)
    PSU:         6 exams
    Police:      4 exams (if physical standards met)
    Teaching:    0 exams (B.Ed not held)
    Railway:     8 exams
```

---

## 2. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/eligibility/my-eligible/?sort=deadline` | All eligible exams for authenticated user |
| 2 | `GET` | `/api/v1/exam/eligibility/my-eligible/stats/` | Eligible count by type |

---

## 5. Business Rules

- The eligible exams list is the single most valuable personalisation output of the platform; an aspirant who sees "you are eligible for 62 exams" — many of which they may not have known about — discovers new opportunities; a 24-year-old AP graduate who never considered IBPS Clerk or RRB NTPC (because they only knew about APPSC) now sees these options; the eligible exams list is a career-widening tool, not just a filtering tool
- The list is computed by running the eligibility engine (D-01) against every active exam and caching the result; the cache is refreshed: (a) daily at 6 AM; (b) immediately when the user updates their profile (D-03); (c) when a new exam is added to the system; this ensures the list reflects the latest exam additions and any profile changes; a stale cache that doesn't show a newly added exam would miss the recommendation window
- Ineligible exams are hidden by default (the user sees only what they qualify for); showing ineligible exams alongside eligible ones creates confusion and noise; however, a toggle "Show why I'm not eligible for other exams" reveals the filtered-out exams with clear failure reasons ("TS domicile required", "B.Ed required", "Age exceeds limit by 2 years"); this transparency helps users understand what they'd need to become eligible (e.g., completing B.Ed opens 12 more teaching exams)
- TS domicile exams showing for an AP domicile user only happens when specific posts within a TS exam do not require TS domicile (some central deputation posts in TSPSC Group 2 may not have domicile restrictions); the engine checks at the post level, not just the exam level; if even one post within a TS exam is open to AP domicile candidates, the exam appears in the eligible list with a note: "Eligible for 3 of 62 posts (non-domicile-restricted posts only)"
- The sort-by-salary option helps aspirants prioritise exams with higher earning potential; however, the system must not present salary as the primary sort (which could bias aspirants toward high-salary exams they have lower chances of clearing) — deadline-soon is the default sort because missing a deadline is irreversible; salary sort is available for aspirants who want to compare earning potential across their eligible options

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division D*
