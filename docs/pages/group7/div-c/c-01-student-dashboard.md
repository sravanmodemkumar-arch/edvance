# C-01 — Student Dashboard

> **URL:** `/dashboard/`
> **File:** `c-01-student-dashboard.md`
> **Priority:** P1
> **Roles:** TSP Student

---

## 1. Personalised Welcome & Progress Overview

```
STUDENT DASHBOARD — TopRank Academy
www.toprankacademy.in                                         Ravi Kumar | My Account | Logout

  ── Welcome back, Ravi! ───────────────────────────────────────────────────────────
  Preparing for: APPSC Group 2 (Prelims + Mains)
  Member since: 12 Jan 2026 | Plan: Annual (expires 11 Jan 2027)

  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
  │  TESTS ATTEMPTED   │  │  AVERAGE SCORE     │  │  STUDY STREAK      │  │  NATIONAL RANK     │
  │       34           │  │    120 / 150       │  │    18 days          │  │   #142 of 1,180    │
  │  +4 this week      │  │    80.0%           │  │  Best: 26 days     │  │  Top 12%           │
  └───────────────────┘  └───────────────────┘  └───────────────────┘  └───────────────────┘

  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
  │  TIME INVESTED     │  │  QUESTIONS SOLVED  │  │  ACCURACY RATE     │  │  IMPROVEMENT        │
  │    142 hrs total   │  │    4,820           │  │    74.6%           │  │  +6.2% vs last     │
  │  3.2 hrs today     │  │  +380 this week    │  │  +2.1% this week  │  │  month average     │
  └───────────────────┘  └───────────────────┘  └───────────────────┘  └───────────────────┘
```

---

## 2. Upcoming Tests & Daily Study Plan

```
UPCOMING TESTS                                              YOUR DAILY STUDY PLAN
─────────────────────────────────────────────────           ─────────────────────────────────
                                                            31 Mar 2026 — Recommended for you
  DATE        TEST NAME                   STATUS
  ───────────────────────────────────────────────           [x] Indian Polity — Fundamental Rights
  01 Apr      APPSC Gr2 Prelims Mock #13  SCHEDULED             30 MCQs | ~25 min
              150 Qs | 150 min | 150 marks                  [ ] Current Affairs — March Week 4
              Starts: 6:00 AM                                    20 MCQs | ~15 min
                                      [Set Reminder]        [ ] General Science — Physics Basics
                                                                 25 MCQs | ~20 min
  05 Apr      APPSC Gr2 Subject: Polity   OPEN                 [Start Now]
              50 Qs | 60 min | 50 marks
              Deadline: 07 Apr 11:59 PM                     Today's Goal: 75 questions
                                      [Attempt Now]         Completed: 30 / 75 (40%)
                                                            ████████░░░░░░░░░░░░ 40%
  08 Apr      SSC CGL Tier-I Mock #9      COMING SOON
              100 Qs | 60 min | 200 marks                   ── WEEKLY PROGRESS ─────────────
              Registration opens: 06 Apr                    Mon  ████████████████████ 92 Qs
                                                            Tue  ████████████████░░░░ 78 Qs
  12 Apr      APPSC Gr2 Prelims Mock #14  SCHEDULED         Wed  ██████████████████░░ 84 Qs
              150 Qs | 150 min | 150 marks                  Thu  ████████████░░░░░░░░ 61 Qs
              Starts: 6:00 AM                               Fri  ██████████████████░░ 85 Qs
                                      [Set Reminder]        Sat  ████████████████████ 95 Qs
                                                            Sun  ██████░░░░░░░░░░░░░░ 30 Qs*
                                                                                 * Today so far
```

---

## 3. Personalised Recommendations & Weak Areas

```
SMART RECOMMENDATIONS — Based on your last 10 tests
─────────────────────────────────────────────────────────────────────────────────

  ── WEAK AREAS (Focus Here) ──────────────────────────────────────────────────
  ┌────────────────────────────────────────────────────────────────────────────┐
  │  Subject              Your Accuracy    Avg Accuracy    Gap     Action     │
  │  ──────────────────────────────────────────────────────────────────────── │
  │  Indian Economy        58.3%            72.1%         -13.8%  [Practice] │
  │  Science & Technology  62.0%            71.5%          -9.5%  [Practice] │
  │  Telangana History     64.2%            70.8%          -6.6%  [Practice] │
  └────────────────────────────────────────────────────────────────────────────┘

  ── STRONG AREAS (Maintain) ──────────────────────────────────────────────────
  ┌────────────────────────────────────────────────────────────────────────────┐
  │  Indian Polity          89.2%            74.0%         +15.2%  Excellent  │
  │  Modern Indian History  84.5%            71.2%         +13.3%  Excellent  │
  │  AP Geography           81.0%            69.8%         +11.2%  Very Good  │
  └────────────────────────────────────────────────────────────────────────────┘

  ── RECOMMENDED NEXT ─────────────────────────────────────────────────────────
  [1] Indian Economy — Budget 2026 Special (30 Qs)        Difficulty: Medium
  [2] Science & Tech — Space & Defence (25 Qs)            Difficulty: Medium
  [3] Telangana Movement — Key Events (20 Qs)             Difficulty: Easy
  [4] Current Affairs — Feb+Mar 2026 Capsule (40 Qs)      Difficulty: Mixed

  "Ravi, improving Indian Economy by 14% can boost your overall score by ~8 marks.
   That's enough to move you from Rank #142 to approximately Rank #95."
   — TopRank AI Coach
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/student/dashboard/summary/` | Dashboard summary cards (tests, score, streak, rank) |
| 2 | `GET` | `/api/v1/student/dashboard/upcoming-tests/` | Upcoming and available tests for enrolled exams |
| 3 | `GET` | `/api/v1/student/dashboard/study-plan/` | Daily study plan with personalised question sets |
| 4 | `GET` | `/api/v1/student/dashboard/recommendations/` | AI-driven weak-area analysis and practice suggestions |
| 5 | `POST` | `/api/v1/student/dashboard/reminders/` | Set or update test reminder (push/SMS/WhatsApp) |
| 6 | `GET` | `/api/v1/student/dashboard/weekly-progress/` | Daily question counts and streak data for the week |

---

## 5. Business Rules

- The student dashboard is fully white-labelled; Ravi sees "TopRank Academy" in the header, favicon, and every notification — never "EduForge"; the branding is pulled from the TSP's configuration set during onboarding (Division A) and injected into the frontend at build time via the `tsp_branding` context; even the AI Coach recommendation at the bottom is attributed to "TopRank AI Coach" rather than EduForge's recommendation engine; if the TSP has configured a custom colour scheme (#1A237E primary, #FF6F00 accent for TopRank), every button, progress bar, and card border uses those colours; this branding consistency is critical because students who see unfamiliar branding lose trust and contact the TSP complaining about phishing
- The study streak counter resets to zero if the student does not complete at least one practice session (minimum 10 questions answered) within a calendar day measured in IST (Indian Standard Time, UTC+05:30); the streak is not based on login — a student who logs in, browses the dashboard, but does not attempt any questions does not get streak credit; streak milestones at 7, 14, 30, 60, and 100 days trigger congratulatory notifications and virtual badges displayed on the profile page (C-04); the streak algorithm accounts for "freeze days" — if the TSP admin enables the streak-freeze feature, students who have a 15+ day streak get one automatic freeze per month where a missed day does not break the streak
- The "National Rank" displayed on the dashboard is computed within the TSP's student pool only (1,180 APPSC Group 2 students at TopRank Academy), not across all EduForge TSPs; this design decision was made because cross-TSP ranking would expose competitive intelligence between coaching centres and because students identify with their coaching centre's peer group; the rank is recalculated every 6 hours by a background job that aggregates the student's weighted average score across the last 10 full-length mock tests; subject-wise tests and partial tests are excluded from rank calculation to prevent gaming; the ranking algorithm uses a weighted formula: 60% average score + 25% consistency (standard deviation penalty) + 15% improvement trend
- Personalised recommendations are generated by a lightweight ML model that analyses the student's question-level response data across all attempted tests; the model identifies subjects where the student's accuracy is more than 5 percentage points below the cohort average and ranks them by potential score impact; the "score impact" estimate (e.g., "improving Indian Economy by 14% can boost your overall score by ~8 marks") is calculated using the subject's weight in the actual APPSC Group 2 exam pattern; recommendations refresh after every test attempt and are cached for 24 hours; the model also factors in recency — a weak area that the student has been practising in the last 3 days is deprioritised in favour of untouched weak areas to encourage breadth of preparation

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division C*
