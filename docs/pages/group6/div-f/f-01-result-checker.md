# F-01 — Result Checker

> **URL:** `/exam/{slug}/results/check/`
> **File:** `f-01-result-checker.md`
> **Priority:** P1
> **Data:** `exam_result` table (if EduForge hosts result data) OR redirect to official source

---

## 1. Result Check Flow

```
RESULT CHECKER — {exam.name}
[Example: TSPSC Group 2 — 2025 Final Result]

  ┌──────────────────────────────────────────────────────────────────────┐
  │  TSPSC GROUP 2 — 2025                                               │
  │  Result Status: ✅ FINAL RESULT DECLARED — 28 March 2026            │
  │  Source: tspsc.gov.in                                                │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                      │
  │  CHECK YOUR RESULT:                                                  │
  │  Method 1: [Check at tspsc.gov.in ↗] (official — recommended)       │
  │  Method 2: Enter details below (EduForge mirror — if available)     │
  │                                                                      │
  │  Hall Ticket No: [ _______________  ]                                │
  │  Date of Birth:  [ __ / __ / ____ ]                                  │
  │  [Check Result]                                                      │
  │                                                                      │
  │  ⚠️ EduForge result data is sourced from official publications.      │
  │  Always verify your result at tspsc.gov.in for official confirmation.│
  └──────────────────────────────────────────────────────────────────────┘

  RESULT (if checked):
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Hall Ticket: 0824-TSPSC-G2-482840                                  │
  │  Name: K. Srinivas                                                   │
  │  Category: BC-B                                                      │
  │  Prelims Score: 92/150 — Qualified ✅                                │
  │  Mains Score:   284/600                                              │
  │  Interview:     42/75                                                │
  │  Final:         326/675 — Rank: 184 (BC-B)                          │
  │  Status:        ✅ SELECTED — Post: Revenue Inspector, Warangal      │
  │                                                                      │
  │  [Download result PDF ↗]  [Share 🎉]                                 │
  │  [Were you an EduForge user? Share your success story →]             │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/{slug}/results/status/` | Result availability status |
| 2 | `POST` | `/api/v1/exam/{slug}/results/check/` | Check result by hall ticket + DOB |
| 3 | `GET` | `/api/v1/exam/{slug}/results/statistics/` | Overall result statistics (qualified count, category-wise) |

---

## 5. Business Rules

- EduForge hosts result data ONLY when official conducting bodies publish results as downloadable PDFs or structured data; EduForge does not scrape login-protected result portals (tspsc.gov.in requires hall ticket + DOB to check results); the primary method is always "Check at official website" — EduForge's mirror is a secondary convenience feature available only when public result PDFs are processed; this approach respects the conducting body's systems and avoids overloading their servers with EduForge-proxied requests
- Result data displayed by EduForge is read-only and sourced from the official publication; EduForge never modifies, interpolates, or estimates result data; if a conducting body publishes a result PDF with 783 names, EduForge's mirror shows exactly 783 results; a discrepancy between EduForge's data and the official source means EduForge's data is wrong and must be corrected immediately; the official source is always authoritative
- The "Share your success story" prompt appears alongside positive results (Selected / Qualified); this is a tactful moment to collect testimonials — the aspirant is at peak happiness and most likely to share; the prompt links to a consent-based success story submission form where the aspirant can choose to share their name, photo, exam, score, and a quote; this feeds the platform's testimonial bank used in marketing; the timing is not manipulative — it is a genuine invitation extended at the right moment
- Result day traffic spikes are the biggest infrastructure challenge; when TSPSC Group 2 results are declared, 3.92 lakh users hit the result checker simultaneously; the result data must be pre-loaded into a fast cache (Redis/CDN) before the notification alert is sent; the alert should be staggered (sent in batches over 5–10 minutes) to spread the traffic spike; the result page must be lightweight (no heavy JavaScript, minimal API calls) to serve under extreme load
- Privacy of result data: EduForge's result checker requires hall ticket number + DOB (same as the official portal); it does not provide a "search all results" or "browse by name" feature; a user cannot look up someone else's result without their hall ticket number; this prevents misuse (a prospective employer checking if a candidate actually passed) and protects aspirant privacy; the data is purged from EduForge's cache 6 months after publication (official source remains authoritative)

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division F*
