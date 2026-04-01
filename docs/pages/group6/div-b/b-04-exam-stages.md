# B-04 — Exam Stages, Pattern & Marking Scheme

> **URL:** `/exam/{exam-slug}/pattern/`
> **File:** `b-04-exam-stages.md`
> **Priority:** P1
> **Data:** `exam_stage` table — each stage is a record; supports any number of stages, any exam

---

## 1. Stage-wise Pattern View

```
EXAM PATTERN — {exam.name}
[Example: TSPSC Group 1 — 2024]
Tab: [Pattern] active

  STAGES  [from exam_stage WHERE exam_id = this exam ORDER BY sequence]
  ┌──────────────────────────────────────────────────────────────────────┐
  │  STAGE 1 — PRELIMS (Screening)                                      │
  │  Mode:         CBT (Computer Based Test)                             │
  │  Total marks:  150                                                   │
  │  Duration:     150 minutes (2 hrs 30 min)                            │
  │  Questions:    150 MCQs                                              │
  │  Negative:     −⅓ mark per wrong answer                             │
  │  Qualifying:   Yes (cut-off based — only to shortlist for Mains)     │
  │  Language:     Telugu / English (bilingual)                           │
  │                                                                      │
  │  SECTION BREAKDOWN:                                                  │
  │    Section                    │ Questions │ Marks │ Duration          │
  │    ──────────────────────────┼───────────┼───────┼─────────          │
  │    General Studies            │    75     │   75  │ (combined)       │
  │    Mental Ability / Reasoning │    75     │   75  │                   │
  │    TOTAL                      │   150     │  150  │ 150 min          │
  ├──────────────────────────────────────────────────────────────────────┤
  │  STAGE 2 — MAINS (Merit-determining)                                 │
  │  Mode:         Pen & Paper (descriptive + objective)                 │
  │  Total marks:  900                                                   │
  │  Duration:     3 papers × 3 hours each = 9 hours over 3 days        │
  │  Language:     Telugu / English (bilingual)                           │
  │                                                                      │
  │  PAPER BREAKDOWN:                                                    │
  │    Paper                      │ Type       │ Marks │ Duration        │
  │    ──────────────────────────┼────────────┼───────┼────────         │
  │    Paper 1: General Essay     │ Descriptive│  150  │ 3 hours        │
  │    Paper 2: History, Polity,  │ Descriptive│  150  │ 3 hours        │
  │             Geography, Economy│            │       │                 │
  │    Paper 3: Science, Tech,    │ Descriptive│  150  │ 3 hours        │
  │             Mental Ability    │            │       │                 │
  │    Paper 4: AP & TS special   │ Descriptive│  150  │ 3 hours        │
  │    (Note: 4 papers ↑ — rendering adapts to any number from DB)      │
  │    TOTAL                      │            │  600  │ 12 hours       │
  ├──────────────────────────────────────────────────────────────────────┤
  │  STAGE 3 — INTERVIEW (Personality Test)                              │
  │  Mode:         In-person (TSPSC office)                              │
  │  Total marks:  75                                                    │
  │  Duration:     20–30 minutes                                         │
  │  Language:     English / Telugu (candidate's choice)                  │
  │  Components:   Leadership, communication, subject knowledge          │
  ├──────────────────────────────────────────────────────────────────────┤
  │  FINAL MERIT:                                                        │
  │    Mains (600) + Interview (75) = 675 total merit marks              │
  │    (Prelims marks NOT counted in final merit)                        │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Model

```
exam_stage {
  id,
  exam_id,                ← FK to exam
  sequence,               ← 1, 2, 3… (rendering order)
  name,                   ← "Prelims" | "Mains" | "Interview" | "Physical Test" | "Typing Test" | any
  mode,                   ← "cbt" | "pen_paper" | "interview" | "physical" | "skill" | "online"
  total_marks,
  duration_minutes,
  questions (nullable),   ← null for interviews / physical tests
  negative_marking,       ← "-1/3" | "-0.5" | "none" | any string
  is_qualifying,          ← true = screening only, false = merit-determining
  language_medium[],
  merit_weight,           ← what fraction of this stage counts in final merit
  sections[]: {           ← JSON array of sections within a stage
    name, questions, marks, duration_minutes (nullable)
  },
  notes,                  ← freeform text for edge cases ("pen & paper for Paper 1, CBT for Paper 2")
}
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/{slug}/pattern/` | All stages with sections |
| 2 | `GET` | `/api/v1/exam/{slug}/pattern/{stage_id}/` | Single stage detail |

---

## 5. Business Rules

- The stage model supports any exam pattern through its flexible `sections[]` JSON and unlimited number of stages; SSC CGL has 2 CBT stages; TSPSC Group 1 has Prelims + Mains (4 papers) + Interview; AP Police SI has Written + Physical Measurement + Physical Efficiency + Interview; NDA has Written + SSB Interview (5-day process); NEET has 1 single-stage exam; the same template renders all of these because it iterates over `stages[]` and within each stage over `sections[]` — no pattern-specific logic
- The `mode` field distinguishes between computer-based tests (where EduForge can provide identical mock experience), pen-and-paper exams (where mock tests simulate the content but not the writing experience), physical tests (where EduForge provides a physical prep guide instead of a mock), interviews (where EduForge provides preparation tips and common questions), and skill tests like typing (where EduForge provides a typing practice tool); the template renders different action buttons based on `mode`: CBT → "Take Mock", physical → "View Physical Prep Guide", interview → "Common Questions"
- The `is_qualifying` flag is critical for aspirant strategy; if Prelims is qualifying only (TSPSC Group 1, UPSC CSE), the aspirant should aim to just clear the cut-off and invest prep time into Mains which determines the final merit; if both stages count (SSC CGL Tier-I + Tier-II), the aspirant must score high in both; this strategic distinction is surfaced prominently: "Prelims — Qualifying only (marks not counted in final merit)" vs "Tier-I — Merit-determining (marks count toward selection)"
- The `negative_marking` field is a string, not a fixed enum, because marking schemes vary: SSC uses −0.5 per wrong answer; UPSC uses −⅓; some exams use −¼; NEET uses −1; some stages of some exams have no negative marking (IBPS descriptive papers); the string is rendered as-is in the UI — the template does not interpret or validate it; the content team enters the exact marking scheme from the official notification
- Final merit computation (shown at the bottom of the pattern page) is a critical decision aid; if TSPSC Group 1 merit = Mains (600) + Interview (75) and Prelims is qualifying only, this is fundamentally different from SSC CGL where both tiers count; the merit formula is computed from `SUM(stage.total_marks × stage.merit_weight WHERE is_qualifying = false)`; the template renders this automatically: if 2 stages are merit-determining, both appear in the merit formula; if only 1 counts, only that appears; the aspirant sees exactly how their final rank will be calculated

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division B*
