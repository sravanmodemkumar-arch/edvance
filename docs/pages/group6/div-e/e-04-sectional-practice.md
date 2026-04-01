# E-04 — Sectional & Topic-wise Practice

> **URL:** `/exam/{slug}/practice/` · `/exam/practice/?topic=indian-polity`
> **File:** `e-04-sectional-practice.md`
> **Priority:** P1
> **Data:** `question` table filtered by `syllabus_node_ids[]` + `exam_tags[]` — dynamic question sets

---

## 1. Practice Modes

```
PRACTICE — APPSC Group 2 2025
Choose your practice mode

  ┌──────────────────────────────────────────────────────────────────────┐
  │  MODE 1: SECTIONAL TEST                                              │
  │  Timed test on a section of the exam (e.g., General Studies: 75 Qs) │
  │  Simulates one section of the actual exam                            │
  │  [Start Sectional →]  Section: [General Studies ▼]                   │
  ├──────────────────────────────────────────────────────────────────────┤
  │  MODE 2: TOPIC-WISE PRACTICE                                         │
  │  Untimed practice on a specific topic (e.g., AP Economy: 20 Qs)     │
  │  Focus on weak areas identified in your mock analysis               │
  │  [Start Topic Practice →]  Topic: [AP Economy ▼]  Qs: [20 ▼]       │
  ├──────────────────────────────────────────────────────────────────────┤
  │  MODE 3: DAILY QUIZ                                                  │
  │  10 questions across mixed topics — generated fresh daily            │
  │  Quick revision, streaks tracked (you're on a 12-day streak 🔥)     │
  │  [Start Daily Quiz →]                                                │
  ├──────────────────────────────────────────────────────────────────────┤
  │  MODE 4: PYQ PRACTICE                                                │
  │  Practice previous year questions topic-wise                         │
  │  Filter: [APPSC Group 2 ▼]  Year: [All ▼]  Topic: [Indian Polity▼] │
  │  Available: 280 PYQs across 5 cycles                                 │
  │  [Start PYQ Practice →]                                              │
  ├──────────────────────────────────────────────────────────────────────┤
  │  MODE 5: WEAK AREA BLITZ                                             │
  │  Auto-generated from your weakest topics (analysis-driven)           │
  │  Your weak areas: AP Economy (37.5%) · DI (40%) · NVR (33.3%)      │
  │  30 Qs focused on these 3 topics                                     │
  │  [Start Weak Area Blitz →]                                           │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Topic-wise Practice (Example)

```
TOPIC PRACTICE — AP Economy (APPSC Group 2)
20 Questions | Untimed | Show answer after each question

  Q.1  ఆంధ్రప్రదేశ్ GSDP (2024–25) లో అత్యధిక వాటా కలిగిన రంగం?
       Which sector has the highest share in AP GSDP (2024–25)?

       (A) Agriculture
       (B) Manufacturing
       (●) Services  ← selected
       (D) Mining

       [Check Answer]

       ✅ CORRECT — Services sector contributes ~52% of AP GSDP (2024–25).
       Agriculture: ~28%, Manufacturing: ~16%, Mining: ~4%.
       Source: AP Economic Survey 2024–25.

       [Next Question →]   [Bookmark]   [Report Error]

  PROGRESS: 1 / 20  │  Correct: 1  │  Wrong: 0
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/exam/{slug}/practice/start/` | Start practice session (`{ mode, topic, count }`) |
| 2 | `GET` | `/api/v1/exam/{slug}/practice/topics/` | Available topics with question counts |
| 3 | `POST` | `/api/v1/exam/practice/daily-quiz/` | Generate daily quiz for user |
| 4 | `GET` | `/api/v1/exam/practice/weak-areas/?uid={uid}` | Weak area questions (analysis-driven) |
| 5 | `POST` | `/api/v1/exam/practice/session/{sid}/response/` | Submit answer in practice mode |

---

## 5. Business Rules

- Topic-wise practice draws questions from the question bank filtered by `syllabus_node_ids` matching the selected topic AND `exam_tags` matching the current exam; a student practicing "AP Economy" for APPSC Group 2 gets questions tagged to `syllabus_node: AP Economy` AND `exam_tag: APPSC Group 2`; they do not get AP Economy questions tagged only to TSPSC Group 2 (which may have TS-specific economic data); the filtering ensures content relevance to the specific exam's syllabus
- Daily Quiz generates 10 questions using a spaced-repetition-inspired algorithm: 3 questions from the user's weakest topics, 3 from topics not practiced in the last 7 days, and 4 from random topics for variety; the quiz is generated fresh daily (same user gets different questions each day); streak tracking (12-day streak) gamifies daily practice — the system sends a reminder at the user's preferred time if they haven't taken today's quiz by evening; streaks are visible on the My Exams dashboard as a motivation metric
- Weak Area Blitz is the most targeted practice mode; it reads the user's topic-wise accuracy from their last 3 mock attempts, identifies topics below 50% accuracy, and generates a 30-question set focused exclusively on those topics; the question difficulty within the blitz is calibrated — first 10 questions are at the user's current level, next 10 are slightly harder, last 10 are at exam difficulty; this progressive difficulty prevents the blitz from being either too easy (no learning) or too hard (demotivating)
- Practice mode shows the answer and explanation after each question (unlike mock tests which show them only after submission); this is intentional — practice is for learning, mocks are for assessment; a student who gets a wrong answer in practice mode immediately reads the explanation and learns the concept; in mock mode, they don't know they got it wrong until 2.5 hours later; the practice-after-each-question format reduces the gap between error and correction, which learning research shows accelerates retention
- Cross-exam question reuse in practice mode (using `exam_tags[]`) means a student practicing "Indian Polity" for APPSC Group 2 benefits from questions that were created for SSC CGL, UPSC CSE, and TSPSC Group 1; the question bank for "Indian Polity" across all exams is much richer than the APPSC-specific bank alone; however, the system must filter out questions that reference exam-specific context ("as asked in SSC CGL 2024 Tier-I") to avoid confusing APPSC aspirants

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division E*
