# E-06 — Mock Test Analytics

> **URL:** `/exam/mocks/analytics/` (user) · `/admin/exam/mocks/analytics/` (admin)
> **File:** `e-06-mock-analytics.md`
> **Priority:** P2
> **Data:** `mock_attempt` aggregate — user-level progress trends + platform-level quality metrics

---

## 1. User-Level Analytics

```
MY MOCK ANALYTICS — Ravi Kumar
Exam: APPSC Group 2 2025 | 14 mocks attempted

  SCORE TREND:
    Mock #  │ Date     │ Score  │ Rank     │ %ile  │ Δ Score
    ────────┼──────────┼────────┼──────────┼───────┼────────
    Mock 1  │ Nov 2025 │ 96/150 │ 28,420   │ 93.4% │  —
    Mock 5  │ Dec 2025 │108/150 │ 18,640   │ 95.6% │ +12
    Mock 10 │ Jan 2026 │116/150 │ 10,280   │ 97.6% │  +8
    Mock 14 │ Mar 2026 │124/150 │  4,820   │ 98.9% │  +8

    📈 Trend: +28 marks over 14 mocks (+2/mock avg) — steady improvement ✅
    🎯 Projected score at exam time (Aug 2026): 136–140/150

  TOPIC ACCURACY TREND (last 5 mocks):
    Topic             │ Mock 10 │ Mock 11 │ Mock 12 │ Mock 13 │ Mock 14 │ Trend
    ──────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼──────
    Indian Polity     │  83%    │  92%    │  88%    │  95%    │ 100%    │ ↑ ✅
    AP Economy        │  25%    │  30%    │  38%    │  33%    │  38%    │ → 🟡
    Data Interp.      │  40%    │  45%    │  35%    │  42%    │  40%    │ → 🟡
    Reasoning         │  72%    │  68%    │  75%    │  78%    │  72%    │ → ✅

  TIME MANAGEMENT:
    Avg time per Q:       0.95 min (target: 1.0 min) ✅
    Questions unattempted: Mock 1: 35 → Mock 14: 20  (↓ improving)
    Time spent per section: GS 82 min, MA 60 min (should be 75/75)
```

---

## 2. Platform-Level Analytics (Admin)

```
PLATFORM MOCK ANALYTICS — March 2026
Admin Dashboard | Content Team

  VOLUME:
    Total mock attempts (Mar):     42,80,000
    Unique users who attempted:    8,42,000
    Avg attempts per user:         5.1

  BY EXAM (top 10):
    SSC CGL:           12,40,000 attempts (29.0%)
    APPSC Group 2:      4,28,000 attempts (10.0%)
    TSPSC Group 4:      3,62,000 attempts (8.5%)
    IBPS PO:            2,84,000 attempts (6.6%)
    RRB NTPC:           2,42,000 attempts (5.7%)
    [+ others]

  QUALITY METRICS:
    Avg completion rate:     82.4% (users who submit vs abandon)
    Avg score (all mocks):   58.2% of total marks
    Questions with <30% correct: 24,800 (too hard? or poor quality?)
    Error reports received:     1,840 (resolved: 1,620, pending: 220)

  ENGAGEMENT:
    Users who took ≥5 mocks this month: 2,84,000 (33.7% of active)
    Daily quiz streaks active:           1,42,000 users
    Practice sessions (topic-wise):      18,60,000
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/mocks/analytics/user/?uid={uid}&exam={slug}` | User's mock trend for an exam |
| 2 | `GET` | `/api/v1/exam/mocks/analytics/user/topics/?uid={uid}&exam={slug}` | Topic accuracy trend |
| 3 | `GET` | `/api/v1/admin/exam/mocks/analytics/platform/?month=2026-03` | Platform-level analytics |
| 4 | `GET` | `/api/v1/admin/exam/mocks/analytics/quality/` | Question quality signals |

---

## 5. Business Rules

- Score projection ("136–140 at exam time") uses linear regression on the user's mock score trend; the model considers: rate of improvement (declining as the user approaches their ceiling), time remaining before the exam, and the user's practice frequency; the projection is displayed as a range (not a point estimate) with the caveat "based on current trend — actual performance depends on continued preparation"; an aspirant who stops studying after seeing "projected 140" and the actual exam difficulty is higher will underperform — the projection assumes continued effort
- Questions with less than 30% correct answer rate (24,800 flagged) are either genuinely difficult (appropriate for advanced mocks) or have a quality issue (ambiguous, wrong answer key, poorly worded); the content team reviews these by examining: (a) the explanation — is it clear? (b) the answer key — is it correct? (c) the question text — is it unambiguous? (d) the difficulty tag — should it be upgraded to "expert"? A question flagged as "easy" but answered correctly by only 20% of users is either mistagged or has a hidden issue
- Mock completion rate (82.4%) means 17.6% of users who start a mock abandon it before submitting; abandonment reasons include: (a) ran out of time and gave up (7–8%); (b) technical issue (app crash, internet loss — ~3%); (c) deliberate — started to "see the questions" without intention to finish (~5%); (d) emergency/interruption (~2%); the system distinguishes between timer-expiry auto-submissions (counted as completions) and manual abandonment; the technical abandonment rate (3%) is the engineering team's target to reduce
- The platform analytics drive content investment decisions; SSC CGL generating 29% of all mock attempts but having only 26% of the question bank suggests under-investment; APPSC Group 2 at 10% of attempts with only 8.8% of the bank is also slightly under-resourced; the content team uses the demand-to-supply ratio (attempts per available question) to prioritise question creation for exams where the ratio is highest — these are exams where users are encountering repeated questions most frequently
- User-level mock analytics are private to the user; EduForge does not share individual users' mock scores, ranks, or topic analytics with coaching institutions, employers, or other users; the My Exams dashboard and mock analytics are visible only to the authenticated user; aggregate anonymised data (platform-level analytics) is used for internal content team decisions and may be published in marketing materials ("our users improved by an average of 24 marks over 10 mocks") with appropriate anonymisation

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division E*
