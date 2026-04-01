# A-06 — Trending Exams & Notifications

> **URL:** `/exam/trending/`
> **File:** `a-06-trending.md`
> **Priority:** P2
> **Data:** `notification` table · `exam` table · `mock_attempt` (aggregate) · `search_log` — all computed, never hardcoded

---

## 1. Trending Dashboard

```
TRENDING — EduForge Exam Hub
What aspirants are focusing on right now | Updated: 31 March 2026, 6:00 AM

  ┌──────────────────────────────────────────────────────────────────────┐
  │  📣 BREAKING                                                         │
  │  SSC CGL 2026 notification released — 18,517 vacancies confirmed    │
  │  Application: 2 Apr – 30 Jun 2026 | [Apply at ssc.nic.in]          │
  │  EduForge mocks now updated to 2026 pattern ✅                      │
  └──────────────────────────────────────────────────────────────────────┘

  TRENDING EXAMS  [computed: mock_attempt COUNT in last 7 days + search spike]
  ┌──────┬────────────────────────────┬────────────┬────────────────────┐
  │  #   │  Exam                      │  7-day     │  Why trending      │
  │      │                            │  activity  │                    │
  ├──────┼────────────────────────────┼────────────┼────────────────────┤
  │  🔥1 │  SSC CGL 2026              │  +840% ↑  │  Notification out  │
  │  🔥2 │  TSPSC Group 4 2026        │  +320% ↑  │  Notification out  │
  │  🔥3 │  APPSC Group 2 2025        │  steady    │  Exam in Aug 2026  │
  │   4  │  AP Police Constable 2025  │  +140% ↑  │  Application open  │
  │   5  │  IBPS PO 2026              │  +80% ↑   │  Expected in Jun   │
  │   6  │  TSPSC Group 1 2024        │  steady    │  Mains in progress │
  │   7  │  VRO/VRA AP 2025           │  +240% ↑  │  Deadline: Apr 10  │
  │   8  │  UPSC CSE 2026             │  +60% ↑   │  Prelims: Jun 2026 │
  └──────┴────────────────────────────┴────────────┴────────────────────┘

  MOST ATTEMPTED MOCKS (last 7 days)  [from mock_attempt aggregate]
    1. SSC CGL 2026 Full Mock #1 (updated pattern) — 2,84,000 attempts
    2. APPSC Group 2 Prelims Mock #15              —   84,200 attempts
    3. TSPSC Group 4 Full Mock #1                 —   62,400 attempts
    4. IBPS PO 2026 Prelims Mock                  —   48,600 attempts
    5. AP Police Constable Mock #8                —   38,200 attempts

  NEW EXAMS ADDED THIS MONTH  [from exam.created_at]
    TSPSC Group 4 2026 — Telangana | Graduate | added 28 Mar 2026
    ONGC AEE 2026 — National | BE/BTech | added 25 Mar 2026
    AP GENCO JE 2026 — AP | Diploma/BE | added 22 Mar 2026
    TS Revenue RI 2026 — Telangana | 12th | added 20 Mar 2026
```

---

## 2. Notification Feed (Latest)

```
LATEST NOTIFICATIONS  [from notification table — source: official URLs]
Filter: [All ▼]  [Central]  [AP]  [Telangana]  [Other States]  [PSU]

  Apr 2, 2026 — SSC CGL 2026 Notification released
    Source: ssc.nic.in | Vacancies: 18,517 | Apply: Apr 2 – Jun 30
    [View notification] [Apply now] [Download PDF]   🔔 4,28,000 alerts sent

  Mar 30, 2026 — AP Police Constable 2025 CBT Results
    Source: slprb.ap.gov.in | Qualified: 84,240 of 6,28,000
    [View results] [Check your result]                🔔 6,28,000 alerts sent

  Mar 28, 2026 — TSPSC Group 2 2025 Final Results
    Source: tspsc.gov.in | Selected: 783 candidates
    [View merit list] [Download PDF]                  🔔 3,92,000 alerts sent

  Mar 25, 2026 — ONGC AEE 2026 Notification
    Source: ongcindia.com | Vacancies: 828 | Qualification: BE/BTech
    [View notification] [Set alert]                   🔔 42,000 alerts sent

  Mar 22, 2026 — VRO/VRA AP 2025 Application extended till Apr 10
    Source: gramasachivalayam.ap.gov.in | Extension: 10 days
    [View notification]                               🔔 2,84,000 alerts sent

  [Load older notifications...]
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/trending/?state=AP&days=7` | Trending exams computed from activity signals |
| 2 | `GET` | `/api/v1/exam/notifications/?type=state&state=TS&limit=20` | Latest notifications with filters |
| 3 | `GET` | `/api/v1/exam/trending/mocks/?days=7` | Most attempted mocks in the period |
| 4 | `GET` | `/api/v1/exam/trending/new/` | Newly added exams this month |

---

## 5. Business Rules

- Trending is computed from real signals — search volume spike (`search_log` for that exam in last 7 days vs prior 7 days), mock attempt count, notification recency, and alert subscriptions; it is never manually curated (a content team member cannot force an exam to appear as #1 trending); the algorithm is objective and transparent; an exam that received no new notification and has declining mock attempts will drop in trending rank automatically; trending must reflect genuine aspirant interest, not EduForge's commercial preference
- The "+840% ↑" activity spike for SSC CGL is computed as `(current_7day_count − prior_7day_count) / prior_7day_count × 100`; a new exam that jumps from 100 to 900 searches in a week shows +800% — correctly indicating it just became relevant; a well-established exam with millions of stable users might show only +5% even though its absolute activity is higher; trending uses percentage change, not absolute count, to surface breakout moments (notification release, result declaration) that aspirants need to act on urgently
- The notification feed is the output of the notification engine (C-01 through C-04); every entry has: `source_url` (official site), `verified: bool` (content team confirmed it's from official source), `published_at` (when official site published it), `ingested_at` (when EduForge detected it); EduForge never publishes rumours or social media posts as notifications — only official source entries are shown; unverified entries (auto-detected but not yet confirmed) are held in a pending queue until the content team verifies; aspirants see only verified notifications
- Alert count shown alongside each notification ("4,28,000 alerts sent") serves a social proof function — it communicates to an aspirant browsing the feed that hundreds of thousands of people are tracking this exam; it also serves as a platform metric; the alert count must reflect actual alerts sent via the notification engine, not a fabricated number; the `notification.alerts_sent` field is updated by the notification engine after delivery and is the value displayed
- "New exams added this month" is computed from `exam.created_at > now() - 30 days WHERE active = true`; it surfaces the content team's work to aspirants who may be looking for a niche exam that was just added; an aspirant preparing for AP GENCO JE who finds it newly available on EduForge (with mocks and syllabus) becomes an immediately engaged user; this section is also a feedback loop for the content team — if a newly added exam generates high traffic, it signals demand for more content (additional mocks, notes) for that exam

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division A*
