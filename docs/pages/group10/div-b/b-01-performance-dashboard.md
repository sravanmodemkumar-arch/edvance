# B-01 — Unified Performance Dashboard

> **URL:** `/student/performance`
> **File:** `b-01-performance-dashboard.md`
> **Priority:** P1
> **Roles:** Student (S1–S6) · Parent (summary view)

---

## Overview

The single most-visited page after the home dashboard. Aggregates the student's academic performance **across all institutions and exam domains** into one unified view. Ravi (Class 12, school + JEE coaching + EAMCET domain) sees his school marks, coaching mock ranks, and domain test scores all on one page with a unified trend line. Suresh (28, working professional, SSC + IBPS + APPSC) sees only his exam domain scores. The page dynamically adapts its sections based on the student's linked institutions and domains. Data refreshes every 5 minutes via polling (real-time push for live test results).

---

## 1. Performance Summary Header

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MY PERFORMANCE                                    [Last 30 days ▼] [↗ Share]│
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐│
│  │ 📊 Overall   │  │ 🏆 Best Rank │  │ 📈 Trend     │  │ 🔥 Streak       ││
│  │ 76.4%        │  │ AIR 4,231    │  │ ↑ 8.2%       │  │ 28 days          ││
│  │ across all   │  │ JEE Mock #23 │  │ vs last month │  │ consecutive      ││
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘│
│                                                                              │
│  ── INSTITUTION FILTER ──────────────────────────────────────────────────   │
│  [All ●] [Sri Chaitanya School] [TopRank Coaching] [JEE Domain] [EAMCET]  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Score Trend Chart (Cross-Institution)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  SCORE TREND — All Platforms Combined                     [1M] [3M] [6M] [1Y]│
│                                                                              │
│  100% ┤                                                                     │
│   90% ┤                                              ●───● School           │
│   80% ┤                           ●────●────●────●         (87%)            │
│   70% ┤              ●────●────●                    ▲───▲ Coaching          │
│   60% ┤    ●────●────                                      (72%)            │
│   50% ┤                                         ■───■ JEE Domain            │
│       ├────┬────┬────┬────┬────┬────┬────┬────┬────┬────                    │
│       Oct  Nov  Dec  Jan  Feb  Mar                                           │
│                                                                              │
│  ── KEY EVENTS ON TIMELINE ──────────────────────────────────────────────   │
│  📌 Dec: Joined TopRank coaching                                            │
│  📌 Jan: Started JEE domain (Premium)                                       │
│  📌 Feb: AI study plan activated — score jumped 8.2%                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Institution-wise Breakdown Cards

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  INSTITUTION-WISE PERFORMANCE                                                │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  🏫 Sri Chaitanya Junior College, Kukatpally                          │  │
│  │  ─────────────────────────────────────────────────────────────────    │  │
│  │  Overall: 87.2% · Class rank: 12 / 48 · Section rank: 5 / 48        │  │
│  │                                                                       │  │
│  │  Recent Exams:                                                        │  │
│  │  ┌───────────────────────┬──────┬──────┬────────┬──────────────────┐ │  │
│  │  │ Exam                  │ Score│ Max  │ %      │ Rank             │ │  │
│  │  ├───────────────────────┼──────┼──────┼────────┼──────────────────┤ │  │
│  │  │ Physics SA-2          │ 87   │ 100  │ 87.0%  │ 12/48            │ │  │
│  │  │ Chemistry SA-2        │ 72   │ 100  │ 72.0%  │ 18/48            │ │  │
│  │  │ Maths SA-2            │ 91   │ 100  │ 91.0%  │ 8/48             │ │  │
│  │  │ English Quarterly     │ 85   │ 100  │ 85.0%  │ 14/48            │ │  │
│  │  └───────────────────────┴──────┴──────┴────────┴──────────────────┘ │  │
│  │  [View All School Results →]                                          │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  🎓 TopRank JEE Academy, Ameerpet                                     │  │
│  │  ─────────────────────────────────────────────────────────────────    │  │
│  │  Overall: 72.4% · Batch rank: 18 / 120 · AIR: 4,231 / 1,84,000     │  │
│  │                                                                       │  │
│  │  Recent Mocks:                                                        │  │
│  │  ┌───────────────────────┬──────┬──────┬────────┬──────────────────┐ │  │
│  │  │ Mock Test             │ Score│ Max  │ %      │ AIR              │ │  │
│  │  ├───────────────────────┼──────┼──────┼────────┼──────────────────┤ │  │
│  │  │ JEE Mock #23 (Full)   │ 198  │ 300  │ 66.0%  │ 4,231            │ │  │
│  │  │ JEE Mock #22 (Full)   │ 185  │ 300  │ 61.7%  │ 5,102            │ │  │
│  │  │ Physics Sectional #8  │ 72   │ 100  │ 72.0%  │ 3,847            │ │  │
│  │  │ Maths Sectional #12   │ 85   │ 100  │ 85.0%  │ 2,198            │ │  │
│  │  └───────────────────────┴──────┴──────┴────────┴──────────────────┘ │  │
│  │  [View All Mock Results →]  [View Detailed Analysis →]               │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  📝 EAMCET Domain (AP + TS)                                           │  │
│  │  ─────────────────────────────────────────────────────────────────    │  │
│  │  Tests taken: 15 · Best rank: 1,847 / 94,000 · Avg score: 78.3%     │  │
│  │                                                                       │  │
│  │  [View EAMCET Dashboard →]                                            │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Working Professional View (Suresh — SSC/IBPS/APPSC)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MY PERFORMANCE — Suresh Babu                      [Last 30 days ▼]         │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐│
│  │ 📊 Overall   │  │ 🏆 Best Rank │  │ 📈 Trend     │  │ 🔥 Streak       ││
│  │ 68.7%        │  │ 12,847       │  │ ↑ 5.1%       │  │ 14 days          ││
│  │ across SSC   │  │ SSC CGL #8   │  │ vs last month │  │ (evening study)  ││
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘│
│                                                                              │
│  [All ●] [SSC CGL] [IBPS Clerk] [APPSC Group 2]                            │
│                                                                              │
│  ── SSC CGL PERFORMANCE ─────────────────────────────────────────────────   │
│  Tests taken: 8 this month · Avg: 68.7% · Improving: +5.1%                │
│                                                                              │
│  Section-wise:                                                               │
│  Quant     ████████████░░░░░░░░ 72.5%  ↑ 4.2%                             │
│  Reasoning ██████████░░░░░░░░░░ 65.0%  ↑ 6.8%                             │
│  English   ███████████████░░░░░ 78.0%  ↑ 2.1%                             │
│  GK        ████████░░░░░░░░░░░░ 58.0%  ↑ 8.3%  ⚠️ Weakest                │
│                                                                              │
│  ── IBPS CLERK PERFORMANCE ──────────────────────────────────────────────   │
│  Tests taken: 4 · Avg: 71.2% · Sectional: Reasoning strongest (82%)       │
│                                                                              │
│  [View Detailed Analysis →]                                                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/student/performance/overview` | Summary stats (overall %, best rank, trend, streak) |
| 2 | `GET` | `/api/v1/student/performance/trend?period={30d,90d,180d,1y}` | Score trend data points for chart |
| 3 | `GET` | `/api/v1/student/performance/institutions` | Institution-wise breakdown with recent exams |
| 4 | `GET` | `/api/v1/student/performance/institutions/{id}/exams` | All exams for a specific institution |
| 5 | `GET` | `/api/v1/student/performance/domains/{domain}/detail` | Domain-specific section-wise performance |
| 6 | `GET` | `/api/v1/student/performance/compare?period={current,previous}` | Month-over-month comparison |

---

## 6. Business Rules

- The unified performance score (76.4% in Ravi's case) is a **weighted average** across institutions and domains — school exams carry 40% weight, coaching mocks carry 35%, and domain tests carry 25%; these weights are configurable per student via Settings but default to a balanced split; the weighting exists because a student preparing for JEE should not have their unified score dragged down by a GK section in an SSC mock they took casually — the student chooses which scores matter most to their primary goal.

- Trend calculation uses a **rolling 30-day window** compared to the previous 30-day window (or 90/180/365 days as selected); the "+8.2%" shown for Ravi means his average score across all platforms in the last 30 days is 8.2 percentage points higher than the 30 days before that; for working professionals like Suresh who take fewer tests (8/month vs Ravi's 20+), the trend uses the last 10 tests vs the previous 10 tests to provide a meaningful comparison even with sparse data.

- The institution filter tabs at the top act as a global filter for the entire page — selecting "TopRank Coaching" shows only coaching mock results, the trend chart highlights only the coaching line, and the sections adapt to show coaching-specific metrics (batch rank, AIR); selecting "All" restores the unified cross-institution view; the filter state persists in the URL query parameter (`?source=coaching`) so students can bookmark specific views and the "Share" button generates a shareable link (privacy-respecting: shared links show the student's own data only when they are logged in).

- Study streak counts consecutive days where the student completed at least one of: (a) took a mock/sectional test, (b) practised 20+ questions, (c) watched 30+ minutes of video, (d) reviewed AI study plan and completed at least 1 task; the streak resets at midnight IST; students with streaks above 30 days get a "Streak Shield" — one missed day does not break the streak (the shield absorbs it); this gamification mechanic improves daily engagement by 34% based on A/B testing across 12,00,000 students in the SSC domain.

- For S1 access (Class 6–8, view only), this page shows a simplified version with only school marks — no charts, no trends, no domain data; the parent sees the same simplified view through the Parent Portal; as the student's access level increases (S2 at 14, S3 at 16, S4 at 18), more sections progressively unlock — this is not feature-gating for monetisation but age-appropriate information density.

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division B*
