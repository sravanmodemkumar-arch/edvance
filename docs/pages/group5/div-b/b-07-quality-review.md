# B-07 — Faculty Quality Review

> **URL:** `/coaching/academic/quality-review/`
> **File:** `b-07-quality-review.md`
> **Priority:** P2
> **Roles:** Academic Director (K6) · Course Head (K5)

---

## 1. Quality Review Dashboard

```
FACULTY QUALITY REVIEW — Q1 2026 (Jan–Mar)
Academic Director: Mr. Suresh Kumar

RATINGS DISTRIBUTION (40 faculty, 1,840 students surveyed):

  Rating Band   │ Faculty Count │ % of Faculty │ Action
  ──────────────┼───────────────┼──────────────┼───────────────────────────────
  4.5 – 5.0     │      8        │   20.0%      │ ✅ Star faculty — recognise
  4.0 – 4.4     │     22        │   55.0%      │ ✅ Performing — maintain
  3.5 – 3.9     │      8        │   20.0%      │ ⚠️ Watch list — coaching plan
  < 3.5         │      2        │    5.0%      │ 🔴 PIP initiated
  ──────────────┴───────────────┴──────────────┴───────────────────────────────
  Avg rating:   4.3 / 5.0   (vs 4.1 in Q4 2025 — improved ✅)

ACTION ITEMS:
  🔴 Mr. Ravi Naidu (English, Main):       3.2/5.0 — PIP meeting 2 Apr
  🔴 Ms. Latha Reddy (Banking, Dilsk):     3.4/5.0 — PIP meeting 3 Apr
  🟡 Mr. Arun Pillai (Quant, Main):        3.7/5.0 — Peer observation scheduled
  🟡 Ms. Sunita Bhat (GK, Main):           3.8/5.0 — Demo class + feedback
```

---

## 2. Faculty Review — Detail View

```
FACULTY QUALITY REVIEW — Mr. Ravi Naidu
Subject: English Language | Branch: Main | Batches: SSC CGL Eve, RRB NTPC
Review period: Q1 2026 (Jan–Mar)

STUDENT RATINGS (384 responses):
  Overall rating:           3.2 / 5.0  ← Below threshold (3.5)
  Clarity of explanation:   3.1 / 5.0
  Topic coverage:           3.4 / 5.0
  Practice material:        2.9 / 5.0  ← Weakest
  Doubt responsiveness:     3.0 / 5.0
  Punctuality:              4.2 / 5.0  ← Strength

STUDENT COMMENTS (sample, anonymised):
  "Doesn't explain 'why' — just reads from slides"          (16 similar)
  "Practice sheets are old — same questions as last year"    (24 similar)
  "Good for grammar rules but RC needs more practice papers" (18 similar)
  "Late to doubt sessions 3 times this month"                ( 8 similar)

ATTENDANCE RECORD (Q1 2026):
  Classes assigned: 52 | Classes taken: 49 | Substituted: 3
  Doubt sessions assigned: 26 | Taken: 22 | Missed: 4

PERFORMANCE IMPACT:
  English accuracy — batches taught by Mr. Ravi Naidu: 58.4%
  English accuracy — batches taught by Ms. Meena Iyer:  65.2%
  Gap: 6.8% lower where Mr. Ravi teaches ← Quantified impact

PIP ACTION PLAN:
  1. Prepare new RC practice sets (10 new passages) by 15 Apr
  2. Attend Ms. Meena Iyer's class (peer observation) 5 Apr
  3. Conduct 1 demo class before Academic Director: 12 Apr
  4. Next review: 30 Jun 2026 — if rating < 3.8, termination process begins
```

---

## 3. Quality Review Survey Form

```
STUDENT FEEDBACK SURVEY — Quarterly (sent via EduForge app)

  Faculty: [Auto-filled from student's batch]
  Subject: [Auto-filled]

  Rate each area (1 = Poor, 5 = Excellent):

  1. Clarity of explanation         [ 1  2  3  4  5 ]
  2. Depth of topic coverage        [ 1  2  3  4  5 ]
  3. Quality of practice material   [ 1  2  3  4  5 ]
  4. Responsiveness to doubts       [ 1  2  3  4  5 ]
  5. Punctuality                    [ 1  2  3  4  5 ]
  6. Overall satisfaction           [ 1  2  3  4  5 ]

  Comments (optional, anonymous):
  [                                                   ]

  [Submit]

  Survey window: 1st–7th of every quarter-end month
  Minimum responses needed: 30 per faculty (for statistically valid rating)
  Anonymity: Student identity not visible to faculty at any time
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/quality/faculty-ratings/` | All faculty ratings summary |
| 2 | `GET` | `/api/v1/coaching/{id}/quality/faculty/{fid}/review/` | Full review detail for one faculty |
| 3 | `POST` | `/api/v1/coaching/{id}/quality/pip/` | Create PIP action plan for faculty |
| 4 | `GET` | `/api/v1/coaching/{id}/quality/survey/results/?faculty={fid}` | Survey responses (aggregated) |
| 5 | `POST` | `/api/v1/coaching/{id}/quality/survey/send/` | Trigger quarterly survey to students |

---

## 5. Business Rules

- Faculty ratings are visible to the Academic Director and Course Head; individual faculty members see only their own rating and anonymised comments, not how they rank among peers; publishing rank-ordered faculty lists internally creates unhealthy competition, faculty resentment, and can trigger collective bargaining behavior; the Academic Director uses the comparative data for their own decision-making without broadcasting it to the faculty at large
- A minimum of 30 student responses is required before a faculty rating is considered statistically valid; a faculty with only 8 students who all gave low ratings may simply have a difficult batch or a personality conflict with 2 vocal students; small sample ratings must be treated as signals, not conclusions; EduForge shows the response count alongside every rating and marks ratings with <30 responses as "indicative only"
- PIP (Performance Improvement Plan) is a structured 90-day process, not a one-time warning; it requires a written plan with specific measurable targets, scheduled check-ins, and a defined outcome (improvement → continue, failure → escalation); an undocumented "warning" given verbally has no legal standing if the faculty member later disputes the termination; EduForge's PIP module creates a digital record that satisfies the documentation requirements of the Industrial Disputes Act
- Star faculty (rating 4.5+) recognition must be as deliberate as PIP for low performers; recognition can be a certificate, a salary increment recommendation, assignment to high-prestige batches (JEE, top-rank SSC), or mention in student newsletters; coaching centres that only address low performance without rewarding excellence create an environment where good faculty feel their quality is taken for granted and accept competitor offers
- Quality review cycle is quarterly; more frequent surveys cause survey fatigue and declining response quality; less frequent (annual) surveys make the data stale and miss semester-level performance changes; quarterly surveys aligned with batch milestones (post each major mock test cycle) give the most actionable feedback; the survey is sent via in-app push notification with a 7-day response window

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division B*
