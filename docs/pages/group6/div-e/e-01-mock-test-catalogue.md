# E-01 — Mock Test Catalogue

> **URL:** `/exam/{slug}/mocks/` (per exam) · `/exam/mocks/` (cross-exam browse)
> **File:** `e-01-mock-test-catalogue.md`
> **Priority:** P1
> **Data:** `mock_test` table — each mock is tagged to an exam + stage, dynamically listed

---

## 1. Mock Catalogue (Per Exam)

```
MOCK TESTS — APPSC Group 2 2025 (Prelims)
28 mocks available | 4,28,000 aspirants | Telugu & English

  FILTER: [Prelims ▼]  [Full Length ▼]  [Free ▼]  [Newest ▼]

  ┌──────────────────────────────────────────────────────────────────────┐
  │  # │ Mock Test                       │ Qs  │ Marks│Dur │ Attempts │  │
  ├────┼─────────────────────────────────┼─────┼──────┼────┼──────────┤──┤
  │  1 │ APPSC Gr2 Prelims Mock #1       │ 150 │  150 │150m│  84,200  │🆓│
  │  2 │ APPSC Gr2 Prelims Mock #2       │ 150 │  150 │150m│  72,600  │🆓│
  │  3 │ APPSC Gr2 Prelims Mock #3       │ 150 │  150 │150m│  68,400  │🔒│
  │ …  │ …                               │     │      │    │          │  │
  │ 28 │ APPSC Gr2 Prelims Mock #28      │ 150 │  150 │150m│  12,400  │🔒│
  ├────┴─────────────────────────────────┴─────┴──────┴────┴──────────┴──┤
  │  🆓 = Free (2 mocks)  🔒 = Premium (subscription required)          │
  │                                                                       │
  │  PREVIOUS YEAR PAPERS (as mocks):                                    │
  │  PYQ 2022 Prelims  │  PYQ 2019 Prelims  │  PYQ 2016 Prelims         │
  │  [Attempt]          │  [Attempt]          │  [Attempt]                │
  │                                                                       │
  │  SECTIONAL TESTS:                                                    │
  │  Indian History (25 Qs)  │  AP Economy (20 Qs)  │  Reasoning (30 Qs) │
  │  [Attempt]               │  [Attempt]           │  [Attempt]          │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Mock Test Data Model

```
mock_test {
  id,
  exam_id,                ← FK to exam (which exam this mock is for)
  stage,                  ← "prelims" | "mains_paper_1" | "tier_i" — matches exam_stage.name
  type,                   ← "full_length" | "sectional" | "pyq" | "mini" | "topic_wise"
  title,
  language[],             ← ["te", "en"] — bilingual rendering
  questions[],            ← ordered list of question_ids
  total_questions,
  total_marks,
  duration_minutes,
  negative_marking,       ← inherits from exam_stage or overrides
  sections[]: {           ← mirrors exam pattern sections
    name, question_ids[], marks
  },
  difficulty,             ← easy | medium | hard | exam_level
  is_free,                ← true = accessible without subscription
  attempts_count,         ← live count of attempts (denormalised, updated async)
  published_at,
  active,
}

question {
  id,
  text_en, text_regional, ← bilingual question text (Markdown with LaTeX support)
  options[]: { id, text_en, text_regional, is_correct },
  explanation_en, explanation_regional,
  exam_tags[],            ← [exam_id] — which exams this Q is relevant for
  syllabus_node_ids[],    ← FK to syllabus_node — topic tagging
  difficulty,             ← 1–5 scale
  source,                 ← "original" | "pyq_2022" | "adapted"
  pyq_exam, pyq_year,    ← if this Q appeared in an actual exam
  language[],
  created_by,
  reviewed,               ← true = quality-checked by content reviewer
}
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/{slug}/mocks/?stage=prelims&type=full_length` | Mock catalogue for an exam |
| 2 | `GET` | `/api/v1/exam/mocks/browse/?type=sectional&topic=indian-polity` | Cross-exam mock browse |
| 3 | `POST` | `/api/v1/exam/mocks/{mid}/start/` | Start a mock attempt |
| 4 | `GET` | `/api/v1/exam/mocks/{mid}/` | Mock test metadata |

---

## 5. Business Rules

- The mock test catalogue is the primary monetisation surface; 2 free mocks per exam give aspirants a taste of EduForge's question quality; premium mocks (26 of 28 for APPSC Group 2) require a subscription; the free-to-premium conversion happens when the aspirant takes the 2 free mocks, sees their analysis (E-03), and recognises the value; the free mocks must be representative of the paid quality — a deliberately poor free mock followed by better paid mocks is a bait-and-switch that damages trust
- Each mock's structure (questions, sections, duration, negative marking) mirrors the actual exam pattern from `exam_stage`; an APPSC Group 2 Prelims mock has 150 questions, 150 marks, 150 minutes, and −⅓ negative — exactly matching the APPSC official pattern; when a pattern changes (e.g., APPSC revises to 120 questions), all mocks for that exam must be updated or retired and new mocks created; a mock with the wrong pattern trains the aspirant incorrectly
- Cross-exam question sharing via `exam_tags[]` allows a single question about "Fundamental Rights under Article 19" to be used in SSC CGL, APPSC Group 2, TSPSC Group 1, and IBPS PO mocks (because all four exams have Indian Polity in their syllabus); this dramatically reduces the cost of question creation while maintaining exam-specific relevance; the tag ensures the question appears in the right mock — an AP-specific history question (Satavahana dynasty) is tagged only to APPSC exams, not to SSC CGL
- Previous year question papers (PYQs) digitised as mock tests are the single highest-trust content; an aspirant who takes PYQ 2022 as a timed mock gets the closest approximation of the real exam experience; PYQ mocks must be verified against the official answer key published by the conducting body; a wrong answer key in a PYQ mock undermines the aspirant's preparation (they learn wrong answers) and EduForge's credibility; the content team verifies every PYQ answer against the official key before marking the mock as reviewed
- Bilingual rendering (Telugu + English for AP/TS exams) must present both languages simultaneously (split-screen or toggle) for mocks that match bilingual exam formats; APPSC and TSPSC exams provide question papers in both Telugu and English; the mock must replicate this by showing `text_te` and `text_en` side by side; a mock that shows only English for a Telugu-medium aspirant is incomplete preparation; the language toggle must work at the question level, not the test level — an aspirant may read GK in Telugu but Reasoning in English

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division E*
