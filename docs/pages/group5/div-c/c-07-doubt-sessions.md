# C-07 — Doubt Session Management

> **URL:** `/coaching/faculty/doubts/`
> **File:** `c-07-doubt-sessions.md`
> **Priority:** P2
> **Roles:** Faculty (K2) · Batch Coordinator (K3)

---

## 1. Doubt Queue

```
DOUBT SESSION — Mr. Suresh Kumar (Quantitative Aptitude)
As of 30 March 2026 | Open doubts: 18

  Filter: [All Batches ▼]  [All Topics ▼]  [Status: Open ▼]

  #  │ Student         │ Batch            │ Topic             │ Question         │ Submitted   │ Status
  ───┼─────────────────┼──────────────────┼───────────────────┼──────────────────┼─────────────┼──────────────
  1  │ Divya Sharma    │ SSC CGL Morning  │ Mensuration 3D    │ "How to find     │ 30 Mar 8:14 │ 🔴 Urgent (2d)
     │ TCC-2404        │                  │                   │  CSA of frustum" │             │
  2  │ Karthik M.      │ SSC CGL Morning  │ Data Interp.      │ "DI Q3 Mock #23  │ 29 Mar 6:45 │ 🟡 Open (1d)
     │ TCC-2405        │                  │                   │  — step 2 unclear"│             │
  3  │ Priya R.        │ SSC CGL Evening  │ Caselet DI        │ "Income/Exp table │ 29 Mar 11:30│ 🟡 Open (1d)
     │ TCC-2402        │                  │                   │  caselet approach"│             │
  4  │ Akhil Kumar     │ SSC CGL Morning  │ Time & Work       │ "Efficiency ratio │ 28 Mar 9:00 │ ✅ Answered
     │ TCC-2401        │                  │                   │  problem method"  │             │
  5  │ Ravi Singh      │ SSC CGL Morning  │ Algebra           │ "Quadratic with   │ 28 Mar 7:45 │ ✅ Answered
     │ TCC-2403        │                  │                   │  substitution"    │             │
  ...  (13 more open)

  SLA: All doubts must be answered within 48 hours of submission
  🔴 1 doubt approaching SLA breach (Divya Sharma — 2 days pending)
```

---

## 2. Doubt Detail & Answer

```
DOUBT: Divya Sharma (TCC-2404) — SSC CGL Morning
Submitted: 28 Mar 2026, 08:14 | Topic: Mensuration 3D

  QUESTION REFERENCE:
  Quant Sprint #17 — Q14 (Hard, Mensuration 3D)
  "A frustum is formed by cutting a cone of height 30 cm and base radius
   21 cm with a plane parallel to the base at height 12 cm. Find the
   curved surface area of the frustum."

  STUDENT'S DOUBT:
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ Sir, I understand the formula CSA = π(R+r)l but I don't know how to find  │
  │ the slant height 'l' of the frustum. Can you explain with this question?  │
  └─────────────────────────────────────────────────────────────────────────────┘

  STUDENT'S ATTEMPTED SOLUTION (uploaded image):
  [📷 Student_attempt_divya_2404.jpg — 120 KB]
  Attempt shows: R=21, r=?, h=18 — student is unsure how to find r

  FACULTY RESPONSE:
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ Good doubt! Step-by-step:                                                  │
  │                                                                             │
  │ Original cone: H=30, R=21. Cut at height 12 from base → top portion h=18  │
  │                                                                             │
  │ Find r (top radius): By similar triangles, r/R = (H-h)/H                  │
  │   r/21 = (30-12)/30 = 18/30 = 3/5 → r = 21 × 3/5 = 12.6 cm              │
  │                                                                             │
  │ Find slant height l: l = √[(R-r)² + h_frustum²]                          │
  │   h_frustum = 12 (distance between cuts) → wait: frustum height = 30-18  │
  │   Actually: cut at height 12 FROM BASE, so frustum is bottom 12 cm        │
  │   h_frustum = 12, R=21, r = 21×(18/30) = 12.6                            │
  │   l = √[(21-12.6)² + 12²] = √[8.4² + 144] = √[70.56+144] = √214.56     │
  │      ≈ 14.65 cm                                                            │
  │ CSA = π(R+r)×l = π(21+12.6)×14.65 = π×33.6×14.65 ≈ 1546.5 cm²          │
  │                                                                             │
  │ Key trick: Always use similar triangles to find r first!                  │
  └─────────────────────────────────────────────────────────────────────────────┘
  [Attach image/formula]  [LaTeX preview]

  [Mark as Answered]   [Schedule Live Session]   [Save Draft]

  SIMILAR DOUBTS (auto-linked):
  • Ravi S. asked similar Mensuration 3D doubt (Mar 22) — [View answer]
  • 3 other students viewed Ravi's answered doubt this week
```

---

## 3. Doubt Analytics

```
DOUBT ANALYTICS — Mr. Suresh Kumar | Last 30 Days

  VOLUME:
    Total doubts received:   94
    Answered within 24 hrs:  71  (75.5%)
    Answered within 48 hrs:  18  (19.1%)
    Pending > 48 hrs:         5  (5.4%) ⚠️ SLA breach

  RESPONSE TIME:
    Avg response time:  14.2 hours
    Fastest:            22 minutes
    Slowest:            61 hours ⚠️

  TOP DOUBT TOPICS (where students need most help):
    Topic               │ Doubts │ % of Total │ Reopen Rate
    ────────────────────┼────────┼────────────┼────────────
    Caselet DI          │  26    │   27.7%    │  18%
    Mensuration 3D      │  18    │   19.1%    │  12%
    Data Interpretation │  14    │   14.9%    │   8%
    Algebra             │   9    │    9.6%    │   5%
    Time, Speed, Dist.  │   8    │    8.5%    │   3%
    Others              │  19    │   20.2%    │   —

  ⚠️ Caselet DI: high doubts + 18% reopen rate = explanation quality needs review
     Action taken: 2 additional sessions scheduled in April ✅

  PEER HELP (doubts answered by fellow students before faculty):
    12 doubts (12.8%) had student answers rated 4+/5 by doubt-raiser
    → These students flagged as peer tutors (B+ batch standing required)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/doubts/?faculty={fid}&status=open` | Open doubt queue |
| 2 | `POST` | `/api/v1/coaching/{id}/doubts/{did}/answer/` | Submit answer to a doubt |
| 3 | `GET` | `/api/v1/coaching/{id}/doubts/similar/?topic={t}&qid={qid}` | Similar doubts on same topic |
| 4 | `GET` | `/api/v1/coaching/{id}/doubts/analytics/?faculty={fid}&month=2026-03` | Monthly doubt stats |
| 5 | `POST` | `/api/v1/coaching/{id}/doubts/{did}/session/` | Schedule live doubt-clearing session |
| 6 | `GET` | `/api/v1/coaching/{id}/doubts/?student={sid}` | All doubts by a specific student |

---

## 5. Business Rules

- Every submitted doubt must receive a faculty response within 48 hours; a doubt that goes unanswered for 48 hours is automatically escalated to the Batch Coordinator (K3) who can reassign it to another available faculty in the same subject; this SLA exists because students preparing for government exams work on tight timelines — a Caselet DI doubt raised on Tuesday before Friday's exam must be answered before the exam, not after
- The "reopen rate" (student marks answer as insufficient and asks again) is a teaching quality signal; a 5% reopen rate is expected (the original doubt was complex); an 18% reopen rate on Caselet DI means the faculty's written explanations for that topic are unclear — either the faculty needs to use more visual examples or schedule a live session to cover the topic collectively; the system flags topics with reopen rate > 15% for Academic Director review
- Doubt answers with LaTeX-rendered formulas and step-by-step solutions are rated higher by students than plain-text answers; the quality score shown in the faculty's quarterly review (B-07) includes doubt answer quality ratings; a faculty who writes thorough, well-formatted answers improves their quality score; plain "see the formula" answers with no worked solution get poor ratings
- "Similar doubts" auto-linking reduces faculty effort and builds a doubt knowledge base; when 5 or more students ask the same doubt, the system creates a "class-level gap" flag and suggests the faculty address it in the next class session rather than answering individually — this is more efficient and signals a teaching gap, not just individual confusion; the flagged topic appears on the Academic Dashboard (B-06) for the Academic Director
- Peer help (student-to-student answers) is encouraged but moderated; a student-provided answer must be rated ≥ 4/5 by the doubt-raiser before it closes the doubt; if rated < 4, it falls back to the faculty queue; peer tutors who consistently provide high-rated answers receive a "Peer Tutor" badge visible on their student profile, and TCC uses this for alumni testimonials and community building

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division C*
