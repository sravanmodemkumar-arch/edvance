# B-04 — Test Series Management

> **URL:** `/tsp/admin/tests/`
> **File:** `b-04-test-management.md`
> **Priority:** P1
> **Roles:** TSP Admin · TSP Manager · Test Manager

---

## 1. Test Series List & Schedule

```
TEST SERIES MANAGEMENT — TopRank Academy
84 published | 12 draft | 6 scheduled | 3 archived

  SEARCH: [Search test name...                     ]
  FILTER: Exam: [All ▼]  Type: [All ▼]  Status: [All ▼]  Creator: [All ▼]

  ┌──────────────────────────────────────────────────────────────────────────────────────┐
  │  # │ Test Name                      │ Exam      │ Type    │ Qs  │Attempts│ Status   │
  ├────┼────────────────────────────────┼───────────┼─────────┼─────┼────────┼──────────┤
  │  1 │ APPSC Gr2 Prelims Mock #13     │ APPSC Gr2 │ Full    │ 150 │    —   │ Sched.   │
  │    │ Auto-publish: 01 Apr 2026 6 AM │           │         │     │        │ 01 Apr   │
  │  2 │ APPSC Gr2 Prelims Mock #12     │ APPSC Gr2 │ Full    │ 150 │   842  │ Live     │
  │  3 │ SSC CGL Tier-I Mock #8         │ SSC CGL   │ Full    │ 100 │   614  │ Live     │
  │  4 │ Banking Awareness Weekly #14   │ IBPS PO   │ Section │  25 │   328  │ Live     │
  │  5 │ APPSC Polity Sectional #6      │ APPSC Gr2 │ Section │  30 │   480  │ Live     │
  │  6 │ RRB NTPC CBT-1 Mock #4         │ RRB NTPC  │ Full    │ 100 │   196  │ Live     │
  │  7 │ SSC CGL Tier-I Mock #9         │ SSC CGL   │ Full    │ 100 │    —   │ Draft    │
  │    │ Review pending (Ravi K.)        │           │         │     │        │          │
  │  … │ …                              │ …         │ …       │ …   │   …    │ …        │
  │ 84 │ APPSC Gr2 Prelims Mock #1      │ APPSC Gr2 │ Full    │ 150 │ 2,840  │ Live     │
  └──────────────────────────────────────────────────────────────────────────────────────┘

  [+ Create New Test]  [Clone from Template]  [Import from EduForge Library]
  [Schedule Bulk Publish]  [Export Test List]
```

---

## 2. Test Creation & Configuration

```
CREATE NEW MOCK TEST

  ── BASIC INFO ────────────────────────────────────────────────────────────
  Test Name:            [ APPSC Gr2 Prelims Mock #13                ]
  Exam:                 [ APPSC Group 2 ▼ ]
  Stage:                [ Prelims ▼ ]
  Type:                 [ Full Length ▼ ]
                        Options: Full Length | Sectional | Topic-wise | PYQ | Mini Mock

  ── PATTERN (auto-filled from exam pattern, editable) ─────────────────────
  Total Questions:      [ 150 ]        Total Marks: [ 150 ]
  Duration:             [ 150 ] minutes
  Negative Marking:     [ -1/3 per wrong answer ▼ ]
  Language:             [ ✅ Telugu  ✅ English ]

  ── SECTIONS ──────────────────────────────────────────────────────────────
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Section                   │ Questions │ Marks │ Source             │
  ├────────────────────────────┼───────────┼───────┼────────────────────┤
  │  General Studies           │    60     │   60  │ [Select Questions] │
  │  Indian Polity & Governance│    30     │   30  │ [Select Questions] │
  │  Indian Economy            │    20     │   20  │ [Select Questions] │
  │  AP History & Culture      │    15     │   15  │ [Select Questions] │
  │  General Science           │    15     │   15  │ [Select Questions] │
  │  Reasoning & Mental Ability│    10     │   10  │ [Select Questions] │
  │  TOTAL                     │   150     │  150  │                    │
  └──────────────────────────────────────────────────────────────────────┘
  [+ Add Section]

  ── QUESTION SELECTION ────────────────────────────────────────────────────
  Method:  (●) Manual pick from question bank
           (○) Auto-generate (select topics + difficulty, system picks)
           (○) Clone from existing mock (modify 20–30% questions)

  ── SCHEDULING ────────────────────────────────────────────────────────────
  Publish mode:  (○) Publish now
                 (●) Schedule for: [ 01 Apr 2026 ] [ 06:00 AM ]
                 (○) Save as draft (publish manually later)

  ── ACCESS CONTROL ────────────────────────────────────────────────────────
  Visibility:    (○) All students  (●) Specific batches: [ APPSC-Mar26, APPSC-Jan26 ]
  Pricing:       (●) Included in subscription  (○) Separate purchase: Rs.[ __ ]
  Free preview:  [ ○ Yes (first 5 questions visible) ]  [ ● No ]

  [Save Draft]  [Preview Test]  [Publish / Schedule]
```

---

## 3. Clone from Template & EduForge Library

```
CLONE / IMPORT OPTIONS

  ── CLONE FROM EXISTING MOCK ──────────────────────────────────────────────
  Source mock:     [ APPSC Gr2 Prelims Mock #12 ▼ ]
  Clone method:   (●) Deep clone (copy all questions, create new mock)
                  (○) Shuffle clone (same questions, randomised order)
                  (○) Variant clone (replace 30% questions with similar difficulty)

  Preview: 150 questions will be cloned. 45 questions (30%) will be
           replaced with new questions from the same topics & difficulty.
  [Create Clone]

  ── IMPORT FROM EDUFORGE TEMPLATE LIBRARY ─────────────────────────────────
  EduForge provides ready-made mock templates for licensed TSPs.

  ┌──────────────────────────────────────────────────────────────────────┐
  │  Template                      │ Exam      │ Qs  │ Used By │ Rating │
  ├────────────────────────────────┼───────────┼─────┼─────────┼────────┤
  │  APPSC Gr2 Prelims Template #1 │ APPSC Gr2 │ 150 │ 42 TSPs │ 4.6/5  │
  │  SSC CGL Tier-I Template #1    │ SSC CGL   │ 100 │ 68 TSPs │ 4.8/5  │
  │  IBPS PO Prelims Template #1   │ IBPS PO   │ 100 │ 31 TSPs │ 4.5/5  │
  │  RRB NTPC CBT-1 Template #1    │ RRB NTPC  │ 100 │ 22 TSPs │ 4.3/5  │
  └──────────────────────────────────────────────────────────────────────┘

  [Import Template] → Creates a draft mock with template questions.
  TSP can edit, add own questions, rebrand, and publish.

  NOTE: Imported templates count against your content licence quota.
  TopRank Academy: 1,240 / 5,000 template questions used this month.
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/tsp/admin/tests/` | List all tests for this TSP (filterable) |
| 2 | `POST` | `/api/v1/tsp/admin/tests/` | Create new mock test |
| 3 | `GET` | `/api/v1/tsp/admin/tests/{id}/` | Test detail with questions and config |
| 4 | `PATCH` | `/api/v1/tsp/admin/tests/{id}/` | Update test config, schedule, access |
| 5 | `POST` | `/api/v1/tsp/admin/tests/{id}/publish/` | Publish or schedule a test |
| 6 | `POST` | `/api/v1/tsp/admin/tests/{id}/clone/` | Clone an existing mock test |
| 7 | `GET` | `/api/v1/tsp/admin/templates/` | Browse EduForge template library |
| 8 | `POST` | `/api/v1/tsp/admin/templates/{id}/import/` | Import a template as draft mock |

---

## 5. Business Rules

- The auto-fill from exam pattern is a critical accuracy feature; when a Test Manager selects "APPSC Group 2 Prelims," the system auto-fills 150 questions, 150 marks, 150 minutes, and negative marking of -1/3 from the exam pattern stored in the EduForge exam database; the Test Manager can override these values (e.g., creating a "mini mock" with 50 questions in 50 minutes), but overrides trigger a warning: "This mock does not match the official APPSC Gr2 Prelims pattern — students may be confused"; maintaining pattern accuracy is essential because students use these mocks to build exam-day stamina and time management skills; a 100-question mock for a 150-question exam gives false confidence about time management
- Test scheduling with auto-publish is how TSPs simulate a structured coaching schedule; TopRank Academy schedules one full mock every Monday at 6:00 AM and one sectional test every Thursday at 6:00 AM; students expect this rhythm and plan their week around it; the scheduler runs as a cron job that checks for tests due for publication every minute; if the scheduler fails (server downtime), the test is published at the next successful check with a "Delayed publication" flag; TSP Admins receive a push notification when a scheduled test is published and an alert if publication is delayed by more than 30 minutes
- Clone and variant generation dramatically reduce the effort of creating new mocks; a full APPSC Gr2 Prelims mock with 150 manually selected questions takes 3–4 hours of faculty time; a variant clone (replace 30% questions) takes 30 minutes because 105 questions are reused and only 45 new questions need selection; the system ensures variant questions match the original's topic distribution and difficulty level; however, clone abuse (publishing 10 nearly identical mocks) degrades student trust — if students notice the same questions across mocks, they lose confidence in the TSP's content quality; the system warns if question overlap between two published mocks exceeds 50%
- EduForge template imports are metered against the TSP's content licence quota; TopRank Academy's Standard plan includes 5,000 template question imports per month; each imported template mock counts its full question count against this quota (a 150-question APPSC template consumes 150 of the 5,000 monthly quota); the quota resets on the 1st of each month; if the TSP exceeds the quota, template imports are blocked until the next month or the TSP upgrades their plan; the TSP's own questions (created by their faculty) are unlimited and do not count against any quota; this incentivises TSPs to build their own question bank while using EduForge templates to fill gaps

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division B*
