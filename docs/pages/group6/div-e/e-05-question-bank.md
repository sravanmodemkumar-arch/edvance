# E-05 — Question Bank & Tagging System

> **URL:** `/admin/exam/questions/` (admin/content team)
> **File:** `e-05-question-bank.md`
> **Priority:** P1
> **Data:** `question` table — 18,40,000 questions, tagged to exams + syllabus nodes + difficulty

---

## 1. Question Bank Dashboard (Admin)

```
QUESTION BANK — Content Team Dashboard
Total questions: 18,40,000 | Reviewed: 16,24,000 (88.3%) | Pending review: 2,16,000

  FILTER: Exam: [All ▼]  Topic: [All ▼]  Difficulty: [All ▼]  Source: [All ▼]
          Language: [All ▼]  Reviewed: [All ▼]  Created: [Last 30 days ▼]

  STATS BY EXAM:
    SSC CGL:          4,84,000 Qs
    APPSC Group 2:    1,62,000 Qs
    TSPSC Group 1:    1,28,000 Qs
    IBPS PO:          1,42,000 Qs
    UPSC CSE:           98,000 Qs
    AP Police:          64,000 Qs
    [+ 78 more exams]

  STATS BY TOPIC (cross-exam):
    Indian Polity:     2,84,000 Qs (used in 28 exams)
    Quantitative Apt:  3,46,000 Qs (used in 22 exams)
    English Language:  2,18,000 Qs (used in 24 exams)
    AP & TS specific:    84,000 Qs (used in 14 exams)
    Current Affairs:   1,24,000 Qs (monthly refresh)

  CONTENT PIPELINE:
    New Qs this month:     8,400 (target: 10,000)
    Reviewed this month:  12,600 (backlog reducing ✅)
    Error reports resolved: 284 (42 questions corrected, 6 retired)
```

---

## 2. Question Creation / Edit

```
CREATE QUESTION — Content Team

  EXAM TAGS:           [✅ APPSC Group 2]  [✅ TSPSC Group 2]  [✅ SSC CGL]
  SYLLABUS NODE:       [Indian Polity → Constitutional Amendments ▼]
  DIFFICULTY:          [●] Easy  [○] Medium  [○] Hard  [○] Expert
  SOURCE:              [●] Original  [○] PYQ  [○] Adapted
  If PYQ: Exam: [APPSC Group 2 ▼]  Year: [2022]

  QUESTION TEXT (English):
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Which Constitutional Amendment introduced the Anti-Defection Law?  │
  └──────────────────────────────────────────────────────────────────────┘

  QUESTION TEXT (Telugu):
  ┌──────────────────────────────────────────────────────────────────────┐
  │  ఏ రాజ్యాంగ సవరణ పార్టీ ఫిరాయింపుల నిరోధక చట్టాన్ని ప్రవేశపెట్టింది?│
  └──────────────────────────────────────────────────────────────────────┘

  OPTIONS:
    (A) 42nd Amendment   /  42వ సవరణ
    (B) 52nd Amendment   /  52వ సవరణ  ← [✅ Correct]
    (C) 73rd Amendment   /  73వ సవరణ
    (D) 86th Amendment   /  86వ సవరణ

  EXPLANATION (English):
    The 52nd Constitutional Amendment Act, 1985, added the Tenth Schedule
    (Anti-Defection Law). It disqualifies MLAs/MPs who defect from their party.

  EXPLANATION (Telugu):
    52వ రాజ్యాంగ సవరణ చట్టం, 1985 పదవ షెడ్యూల్ (పార్టీ ఫిరాయింపుల
    నిరోధక చట్టం) ను చేర్చింది.

  [Save as Draft]  [Submit for Review]  [Publish directly] (senior content)
```

---

## 3. Tagging System

```
TAGGING HIERARCHY

  question.exam_tags[]:        Which exams this Q is relevant for
  question.syllabus_node_ids[]:Which topics this Q covers (from B-02 tree)
  question.difficulty:         1 (easy) – 5 (expert)
  question.source:             original | pyq | adapted
  question.language[]:         ["en", "te"] — which languages are available

  CROSS-EXAM TAGGING EXAMPLE:
    "52nd Amendment Anti-Defection Law" question:
      exam_tags: [APPSC Gr2, TSPSC Gr1, SSC CGL, IBPS PO, UPSC CSE]
      syllabus_nodes: [
        APPSC-Gr2 → Prelims → Polity → Constitutional Amendments,
        SSC-CGL → Tier-I → GK → Polity,
        UPSC-CSE → Prelims → GS Paper I → Polity
      ]

    This single question can appear in:
      - APPSC Group 2 mock test (as a Polity question)
      - SSC CGL mock test (as a GK question)
      - UPSC CSE practice (as a Polity question)
      - Indian Polity topic practice (for any exam)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/admin/exam/questions/?exam=appsc-group-2&topic=polity&page=1` | Browse questions |
| 2 | `POST` | `/api/v1/admin/exam/questions/` | Create new question |
| 3 | `PATCH` | `/api/v1/admin/exam/questions/{qid}/` | Edit question |
| 4 | `POST` | `/api/v1/admin/exam/questions/{qid}/review/` | Mark as reviewed |
| 5 | `GET` | `/api/v1/admin/exam/questions/stats/` | Question bank statistics |
| 6 | `POST` | `/api/v1/admin/exam/questions/bulk-import/` | CSV/Excel bulk import |

---

## 5. Business Rules

- Question quality is the product's foundation; a mock test with inaccurate, ambiguous, or outdated questions is worse than no mock test — it trains aspirants incorrectly; the two-tier quality process (create → review) ensures that every published question has been verified by a different content team member than the creator; the 88.3% review rate (16.24L of 18.4L) means 2.16 lakh questions are still pending review — these are used only in practice mode (lower stakes), never in full-length mock tests (higher stakes) until reviewed
- Telugu translations must be native-quality, not machine-translated; government exams in AP and TS provide Telugu question papers that use formal administrative Telugu — not colloquial or literary Telugu; the content team's Telugu writers must understand the exam context and produce translations that match the style aspirants will encounter in the actual exam; a machine-translated question with awkward Telugu phrasing is a disservice to Telugu-medium aspirants
- Current Affairs questions (1,24,000 in bank) have a shelf life; a question about "who won the 2024 Cricket World Cup?" is valid for 12–18 months but becomes dated and potentially wrong after that; the content team must review and retire current affairs questions older than 18 months; a mock test that includes outdated current affairs questions ("who is the current RBI Governor?" with an answer from 2023) is actively harmful; the system flags current affairs questions for review based on `created_at` + 18 months
- Bulk import (CSV/Excel) is used when the content team creates questions offline (subject experts filling a spreadsheet) and uploads them in batches of 50–500; the import validates: required fields (text, 4 options, correct answer, at least 1 exam_tag, at least 1 syllabus_node), language availability (if exam requires Telugu, question must have Telugu text), and deduplication (similar questions flagged before import); a bulk import that introduces 200 duplicate questions (rephrased versions of existing ones) wastes bank space and creates mock tests with repetitive content
- Error reports from aspirants (E-03 "Report Error" button) flow into the content team's queue with the question context, the reporter's concern, and the question's attempt statistics; a question where 90% of aspirants choose option A but the official answer is B is either a genius question or has a wrong answer key; the content team investigates using the original source (official answer key for PYQs, subject expert review for originals) and either confirms the answer or corrects it; corrections trigger re-scoring for all affected mock attempts

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division E*
