# G-05 — Content Management (Admin CMS)

> **URL:** `/admin/exam/content/`
> **File:** `g-05-content-management.md`
> **Priority:** P1
> **Data:** `study_material` + `question` + `current_affair` — unified CMS for all exam content

---

## 1. Content Dashboard (Admin)

```
CONTENT CMS — Admin Dashboard
Content Team | 31 March 2026

  CONTENT INVENTORY:
    Study material (notes + PDFs):   4,840 items
    Video lectures:                  2,180 videos (1,840 hrs total)
    Questions in bank:            18,40,000
    Current affairs entries:        12,480 (since Jan 2025)
    Mock tests published:            1,840

  MONTHLY TARGETS vs ACTUALS (March 2026):
    Metric               │ Target │ Actual │ Status
    ─────────────────────┼────────┼────────┼────────
    New questions created │ 10,000 │  8,400 │ 🟡 84%
    Questions reviewed    │ 15,000 │ 12,600 │ 🟡 84%
    Study notes published │    24  │    22  │ ✅ 92%
    Videos published      │    12  │    14  │ ✅ 117%
    CA entries published  │   180  │   186  │ ✅ 103%
    Mock tests created    │    28  │    26  │ ✅ 93%
    Error reports resolved│   300  │   284  │ ✅ 95%

  CONTENT PIPELINE:
    Drafts awaiting review:        842
    Reviewed, pending publish:     124
    Published today:                38
    Flagged for quality review:     18

  TEAM:
    Subject experts (content):     24 (8 Telugu, 8 English, 8 bilingual)
    Reviewers:                      8
    Video editors:                  4
    CA writers:                     6
```

---

## 2. Content Workflow

```
CONTENT LIFECYCLE

  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │  DRAFT   │ →  │  REVIEW  │ →  │ APPROVED │ →  │ PUBLISHED│
  │ (creator)│    │(reviewer)│    │ (auto)   │    │ (live)   │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
       │               │               │               │
  Created by      Reviewed by     If review passes  Goes live on
  subject expert  different person  → auto-approved    exam portal
                  Checks: accuracy Quality gate:      Visible to
                  language, tags   no errors, all     aspirants
                  formatting       tags present

  REJECTED CONTENT:
    Review fails → sent back to creator with feedback
    Creator revises → re-submits for review
    Max 3 review cycles → escalated to content lead

  BULK OPERATIONS:
    [Import questions from CSV]  [Bulk tag update]  [Bulk publish]
    [Retire outdated content]  [Export content report]
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/admin/exam/content/dashboard/` | Content inventory and pipeline stats |
| 2 | `GET` | `/api/v1/admin/exam/content/pipeline/?status=review` | Content items by workflow status |
| 3 | `POST` | `/api/v1/admin/exam/content/review/{id}/approve/` | Approve content item |
| 4 | `POST` | `/api/v1/admin/exam/content/review/{id}/reject/` | Reject with feedback |
| 5 | `GET` | `/api/v1/admin/exam/content/analytics/?month=2026-03` | Monthly content production metrics |

---

## 5. Business Rules

- The two-person rule (creator ≠ reviewer) is the quality gate; a subject expert who creates a question cannot review their own work — cognitive bias ("I wrote it, so it must be right") causes errors to slip through; the reviewer checks: factual accuracy (is the answer correct?), language quality (is the Telugu grammatically correct?), tagging accuracy (is it mapped to the right syllabus node and exam?), and formatting (are options properly structured?); this adds latency (24–48 hrs review cycle) but prevents quality issues reaching aspirants
- Content production targets are set monthly by the content lead based on: (a) demand — exams with upcoming dates need more mocks and practice questions; (b) coverage gaps — topics with fewer than 50 questions are under-served; (c) new exams — a newly added exam needs baseline content (at least 2 full mocks, syllabus-mapped notes, and 500 questions) before it is commercially viable; the March targets reflect April's needs (SSC CGL notification expected → increase SSC content production)
- Telugu content creation requires native Telugu-medium subject experts, not translators; the content team has 8 dedicated Telugu content creators who write notes, questions, and explanations in Telugu as primary content; English versions are created in parallel (not as translations of Telugu); this dual-origin approach produces higher quality in both languages compared to creating in one language and translating to the other
- Retiring outdated content (CA entries > 12 months, questions referencing old data, notes on superseded policies) is an active process; the CMS flags content by age and the content team reviews flagged items monthly; a question asking "Who is the current Chief Minister of AP?" with an answer from 2019 is dangerously wrong if it appears in a 2026 mock; retirement removes the content from active mock tests and practice sets but preserves it in the "historical" archive for reference
- Error resolution SLA: questions reported as incorrect by aspirants (E-03 "Report Error") must be resolved within 72 hours; resolution means: confirmed correct (report dismissed with explanation), corrected (answer key changed, re-scoring triggered), or retired (question removed from active use); the 72-hour SLA ensures aspirants are not repeatedly encountering a wrong question across multiple mock tests before it is fixed

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division G*
