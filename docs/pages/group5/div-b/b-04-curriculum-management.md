# B-04 — Curriculum & Syllabus Management

> **URL:** `/coaching/academic/curriculum/`
> **File:** `b-04-curriculum-management.md`
> **Priority:** P2
> **Roles:** Academic Director (K6) · Course Head (K5) · Curriculum Designer (K4)

---

## 1. Curriculum Overview

```
CURRICULUM MANAGEMENT — SSC CGL (10-Month Course)
Course Head: Mr. Suresh Kumar

SYLLABUS COMPLETION STATUS — SSC CGL Morning Batch
As of 30 March 2026 (Month 10 of 10)

  Subject           │ Topics Total │ Covered │ Remaining │ Completion │ Status
  ──────────────────┼──────────────┼─────────┼───────────┼────────────┼────────
  Quantitative Apt. │      48      │   46    │     2     │  95.8%     │ ✅
  Reasoning         │      36      │   34    │     2     │  94.4%     │ ✅
  English Language  │      28      │   26    │     2     │  92.9%     │ ✅
  General Knowledge │      20      │   18    │     2     │  90.0%     │ ⚠️
  Computer Aptitude │      10      │   10    │     0     │ 100.0%     │ ✅
  ──────────────────┴──────────────┴─────────┴───────────┴────────────┴────────
  TOTAL             │     142      │  134    │     8     │  94.4%     │ ✅

  Remaining 8 topics: Scheduled for 1–10 April (final revision week)
  Exam date (SSC CGL 2026 Tier-I): 20 April 2026 (estimated)
```

---

## 2. Topic Sequence — Quantitative Aptitude

```
TOPIC SEQUENCE — QUANTITATIVE APTITUDE (SSC CGL)
48 Topics over 10 months

  Month 1 (Foundation):
    ✅ Number System         ✅ LCM & HCF            ✅ Fractions & Decimals
    ✅ Simplification        ✅ Percentage            ✅ Profit & Loss

  Month 2–3 (Arithmetic Core):
    ✅ Simple Interest        ✅ Compound Interest     ✅ Ratio & Proportion
    ✅ Time & Work            ✅ Pipes & Cisterns      ✅ Time, Speed & Distance
    ✅ Trains                 ✅ Boats & Streams       ✅ Ages

  Month 4–5 (Algebra & Geometry):
    ✅ Basic Algebra          ✅ Linear Equations      ✅ Quadratic Equations
    ✅ Geometry (Lines)       ✅ Triangles             ✅ Circles
    ✅ Quadrilaterals         ✅ Coordinate Geometry   ✅ Trigonometry Basics

  Month 6–7 (Data Interpretation):
    ✅ Tables                 ✅ Bar Graphs            ✅ Line Graphs
    ✅ Pie Charts             ✅ Mixed DI              ✅ Data Sufficiency

  Month 8–9 (Advanced):
    ✅ Mensuration 2D         ✅ Mensuration 3D        ✅ Statistics (Mean/Median)
    ✅ Permutation & Comb.   ✅ Probability            ✅ Surds & Indices
    ✅ Number Series          ✅ Simplification Adv.   ✅ Approximation

  Month 10 (Revision):
    ⬜ DI Mixed (Advanced)   ⬜ Full Syllabus Revision
    → Scheduled: 1–4 April 2026
```

---

## 3. Curriculum Comparison — Competitor Analysis

```
CURRICULUM BENCHMARKING

  Topic Coverage            │ TCC SSC CGL │ SSC 2025 Actual Paper │ Gap
  ──────────────────────────┼─────────────┼──────────────────────┼────────────
  Mensuration               │ ✅ 8 topics  │ 4 questions           │ ✅ adequate
  DI — Caselet              │ ✅ 3 topics  │ 5 questions           │ ⚠️ add 2 more
  Trigonometry              │ ✅ 4 topics  │ 3 questions           │ ✅ adequate
  Geometry (Circle theorem) │ ✅ 3 topics  │ 4 questions           │ ⚠️ add 1 more
  Algebra (advanced)        │ ✅ 4 topics  │ 5 questions           │ ⚠️ add practice
  English — Sentence Improv.│ ✅ 2 topics  │ 10 questions          │ 🔴 underweighted

  Action items for 2026–27 curriculum revision:
  1. Add Caselet DI as a standalone 2-week topic in Month 7
  2. Increase English sentence improvement practice from 2 → 4 sessions
  3. Add advanced algebra sprint in Month 9
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/curriculum/?course=ssc-cgl` | Curriculum structure for a course |
| 2 | `GET` | `/api/v1/coaching/{id}/curriculum/progress/?batch={id}` | Topic coverage status for a batch |
| 3 | `PATCH` | `/api/v1/coaching/{id}/curriculum/topic/{tid}/complete/` | Mark topic as covered |
| 4 | `POST` | `/api/v1/coaching/{id}/curriculum/` | Create/update curriculum for a course |
| 5 | `GET` | `/api/v1/coaching/{id}/curriculum/gap-analysis/` | Curriculum vs actual exam paper gap |

---

## 5. Business Rules

- Curriculum completion must reach 95%+ before the target exam date with a minimum 2-week revision window; a batch that completes only 85% of the syllabus before the exam leaves students underprepared for 15% of the paper; EduForge tracks topic-wise completion daily and alerts the Course Head if the completion trajectory predicts ending below 95% before the exam date
- Topic sequence design is not arbitrary; foundational topics (Number System, Basic Algebra) must precede advanced topics (Quadratic Equations, Number Series); the Curriculum Designer must ensure prerequisites are respected in the sequence; EduForge allows tagging prerequisite topics — a teacher cannot mark an advanced topic as covered if its prerequisites are incomplete
- Curriculum revision is an annual process driven by actual exam paper analysis; the previous year's SSC CGL paper is analysed topic-by-topic to calculate the number of questions per topic; topics with low TCC coverage but high exam weight are flagged for curriculum enhancement; this data-driven curriculum revision is what separates systematic coaching from ad hoc teaching
- The curriculum is a competitive asset; TCC's topic sequences, timing, and question bank mapping represent years of refinement; the Curriculum Designer role is a K4 internal role with NDA obligations; curriculum documents are watermarked and access-logged; if a faculty member leaves and joins a competitor with identical curriculum timing, EduForge's access logs serve as evidence in any IP dispute
- Different exam categories have completely independent curricula; the SSC CGL curriculum and the Banking curriculum share some topics (Quant basics, English) but have different depth, different topic ordering, and different mock test patterns; the Course Head for each category owns their curriculum; attempts to "standardise" across categories by using a single curriculum harm the specialised students who need category-specific preparation

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division B*
