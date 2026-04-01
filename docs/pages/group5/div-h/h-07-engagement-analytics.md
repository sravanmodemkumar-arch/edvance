# H-07 — Student Engagement Analytics

> **URL:** `/coaching/online/engagement/`
> **File:** `h-07-engagement-analytics.md`
> **Priority:** P2
> **Roles:** Online Coordinator (K4) · Academic Director (K5) · Branch Manager (K6)

---

## 1. Engagement Dashboard

```
STUDENT ENGAGEMENT ANALYTICS — All Online Batches
March 2026  |  Total online students: 1,284

  PLATFORM ACTIVITY:
    Total logins (March):       18,420  (avg 14.3 logins/student) ✅
    Total video minutes watched: 3,42,840 min  (avg 267 min/student = 4.4 hrs)
    Total tests taken:          14,840  (avg 11.6 tests/student)
    Total doubts raised:         2,184  (avg 1.7 doubts/student)
    Total material downloads:    6,840  (avg 5.3 per student)

  DAILY ACTIVITY PATTERN:
    Peak usage: 8:00–10:00 PM  (live + post-session recording rush)
    Second peak: 6:00–7:00 AM  (morning revision before offline classes)
    Lowest: 2:00–5:00 PM       (work hours for employed students)

  ENGAGEMENT BAND DISTRIBUTION:
    Band         │ Score Range │ Students  │ % Total │ Trend
    ─────────────┼─────────────┼───────────┼─────────┼─────────────────────
    High (>75)   │  75–100    │    386    │  30.1%  │ ↑ +4.2% vs Feb ✅
    Medium (50–75)│  50–74    │    488    │  38.0%  │ ↑ +1.8% vs Feb ✅
    Low (25–50)  │  25–49    │    286    │  22.3%  │ ↓ -2.4% vs Feb ✅
    At-Risk (<25) │   0–24    │    124    │   9.6%  │ ↓ -3.6% vs Feb ✅

  IMPROVEMENT: At-Risk band reduced from 13.2% (Feb) to 9.6% (Mar) ✅
  (Driven by: WhatsApp re-engagement calls for 68 disengaged students in Feb)
```

---

## 2. Content Consumption Analysis

```
CONTENT CONSUMPTION — Most & Least Consumed (March 2026)

  TOP 5 MOST WATCHED VIDEOS (by total view-minutes):
    Rank │ Video                            │ Views │ Avg Watch% │ Total Min
    ─────┼──────────────────────────────────┼───────┼────────────┼───────────
    1    │ Quant: DI Caselets Part 1        │  224  │  78.4%    │  11,238
    2    │ Reasoning: Seating Arrangement   │  196  │  72.6%    │   9,012
    3    │ Quant: Mensuration 3D            │  182  │  68.4%    │   7,642
    4    │ English: Cloze Test Advanced     │  168  │  82.2%    │   8,640
    5    │ Reasoning: Blood Relations       │  154  │  74.8%    │   7,200

  BOTTOM 5 LEAST WATCHED (from last 30 days):
    1. GK: State Capitals Revision — 28 views (28% avg watch) — ARCHIVE candidate
    2. Quant: Basic Fractions (very easy) — 34 views — too elementary for this batch
    3. English: Parts of Speech — 36 views — pre-enrollment level
    4. Reasoning: Analogy Basic — 38 views — too easy for CGL level
    5. GK: Historical Timeline 1857–1947 — 40 views (static, prefer live notes)

  RECOMMENDATION: Archive basic-level videos; replace with advanced difficulty
  Action: Online Coordinator to review with Academic Director by Apr 5
```

---

## 3. Cohort Comparison

```
COHORT COMPARISON — Engagement vs Performance (Mock #25)

  Engagement Band  │ Avg Mock #25 Score │ Students │ Tier-I Probability
  ─────────────────┼────────────────────┼──────────┼───────────────────
  High (>75)       │    138.4 / 200     │   386    │  64.2% > cutoff
  Medium (50–75)   │    108.6 / 200     │   488    │  28.4% > cutoff
  Low (25–50)      │     78.2 / 200     │   286    │   6.8% > cutoff
  At-Risk (<25)    │     48.4 / 200     │   124    │   0.8% > cutoff

  CORRELATION: 0.84 (engagement score vs test score) — strong positive correlation ✅
  Insight: A 10-point engagement score increase correlates with ~9-point score increase
  Action: Invest coordinator time in moving Low → Medium band (highest ROI for TCC)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/online/engagement/dashboard/?month=2026-03` | Full engagement analytics |
| 2 | `GET` | `/api/v1/coaching/{id}/online/engagement/content/?month=2026-03` | Content consumption analytics |
| 3 | `GET` | `/api/v1/coaching/{id}/online/engagement/cohort/?batch={bid}` | Cohort engagement vs performance |
| 4 | `GET` | `/api/v1/coaching/{id}/online/engagement/trend/?batch={bid}&months=3` | 3-month engagement trend |
| 5 | `POST` | `/api/v1/coaching/{id}/online/engagement/campaign/` | Launch re-engagement campaign |

---

## 5. Business Rules

- The engagement-performance correlation (0.84) is the strongest evidence TCC has for investing in engagement improvement; a coordinator who improves a cohort's average engagement score from 45 to 55 (10 points) should expect a ~9-point increase in mock scores; this is the teaching effectiveness argument for online engagement work — it is not just about students staying subscribed, it is about students improving; the Academic Director uses this correlation in faculty briefings to motivate engagement-boosting activities
- Content consumption data is used to retire under-performing content; a video with fewer than 30 views in 90 days and below 40% average watch time is a candidate for retirement; the coordinator reviews these candidates with the faculty who created them; some low-view content is "reference material" (accessed only when needed, not routinely) and should be kept; others are genuinely low-quality or wrong-level content; the distinction requires judgement, not just metrics — the coordinator's role is to curate, not delete mechanically
- Daily activity patterns (peak at 8–10 PM) inform the live session schedule; TCC's evening live sessions (7–9 PM) align with peak engagement; morning sessions (6 AM) serve students who work during the day; the Online Coordinator monitors activity pattern shifts month-to-month; if peak usage shifts to 6–8 PM (earlier), live sessions may need to be rescheduled accordingly; schedule changes require 14 days notice and are decided by the Academic Director with student input (survey)
- Re-engagement campaigns (the 42% re-engagement rate for personal WhatsApp calls) are time-intensive; with 124 at-risk students, the coordinator cannot personally call each one; the strategy is: tier the at-risk students by "recovery potential" (attended at least 5 sessions before going silent = higher potential than those who never engaged), prioritise the high-potential group for personal calls, and use automated WhatsApp for the low-potential group; this triage is tracked in the campaign dashboard
- Engagement analytics data (individual student login times, content viewed, doubts raised) is personal data under DPDPA 2023; it is used by TCC for service improvement and student support; it must not be shared with third parties (including the student's parents, unless the student is a minor); it must not be used for marketing to non-students (e.g., "based on your sibling's activity, we think you'd benefit from…"); the data processor agreement with EduForge specifies these restrictions

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division H*
