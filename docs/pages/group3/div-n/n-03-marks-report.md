# N-03 — Marks & Report Cards (Parent View)

> **URL:** `/parent/marks/`
> **File:** `n-03-marks-report.md`
> **Template:** `parent_portal.html`
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P)

---

## 1. Purpose

Parents see their child's academic performance — marks, grades, subject-wise analysis, report cards, and comparison to class average. This is one of the highest-traffic features in the parent portal (every test, every report card release triggers a spike in parent logins).

Report card release is a controlled event — marks are visible to parents only after the Principal/VP approves the release in the B-series module. Until release, marks are invisible on the parent portal (to prevent premature access before all marking is complete).

---

## 2. Current Assessment View

```
MARKS & PERFORMANCE — Rahul Rao (Class X-A)
Roll No. 14  |  Class Teacher: Mr. Deepak C.

LATEST ASSESSMENT: Unit Test 1 (Feb 2026) — RELEASED ✅

  Subject           Max  Marks  %      Grade  Class Avg  Rank
  ─────────────────────────────────────────────────────────────
  English            50    39   78.0%   B+    76.3%      12/39
  Mathematics        50    38   76.0%   B+    68.4%      8/39  ✅
  Science            50    37   74.0%   B+    74.1%      18/39
  Social Science     50    42   84.0%   A     72.8%      5/39  ✅
  Hindi              50    34   68.0%   B     69.1%      21/39
  ─────────────────────────────────────────────────────────────
  AGGREGATE         250   190   76.0%   B+    72.1%      11/39

TEACHER COMMENTS (Class Teacher, Mr. Deepak C.):
  "Rahul has shown good improvement in Maths and Social Science this term.
   Needs to focus more on Hindi grammar. Overall — steady progress."

[Download Unit Test 1 Report Card PDF]
```

---

## 3. Year-to-Date Performance Trend

```
PERFORMANCE TREND — 2025–26

Assessment      Aggregate%   Class Avg%   Class Rank
Term 1 (Jun)    71.2%        70.8%        15/39
Unit Test 1     76.0%        72.1%        11/39   ▲ Improving ✅
Half-Yearly     —            —            —       (Not yet held)
Unit Test 2     —            —            —       (Not yet held)
Annual          —            —            —       (Not yet held)

Trend: Improving (+4.8% from Term 1 to UT-1) ✅
Subject strengths: Social Science, Mathematics
Subject to watch: Hindi (consistently below class avg)

[View subject-wise detailed trend →]
```

---

## 4. Subject Deep-Dive

```
SUBJECT DETAIL — Mathematics (Class X-A)
Teacher: Mr. Deepak C.

All assessments this year:
  Assessment       Marks    Max    %       Class Avg
  Term 1 (Jun)     32/50   50     64.0%   67.2%  ← Below class avg
  Unit Test 1      38/50   50     76.0%   68.4%  ← Above class avg ✅
  Half-Yearly      —       —      —       —

Board exam chapter weightage (CBSE):
  Algebra (20%) · Geometry (15%) · Trigonometry (12%) · Statistics (10%) ·
  Real Numbers (6%) · Polynomials (6%) · etc.

  Chapters tested in UT-1: Real Numbers, Polynomials, Quadratic Equations
  Rahul's chapter performance:
    Real Numbers:       8/10  ✅
    Polynomials:        12/15 ✅
    Quadratic Equations: 18/25 ✅ (improved significantly)

Teacher note on Mathematics: "Good improvement. Ensure practice on word problems."
```

---

## 5. Report Card Downloads

```
REPORT CARDS — Rahul Rao (Class X-A)

  Assessment        Date Released  Status     Action
  Term 1            15 Jul 2025    Released   [Download PDF] [View Online]
  Unit Test 1       27 Mar 2026    Released   [Download PDF] [View Online]
  Half-Yearly       —              Not yet    (Expected: 15 Oct 2025) ← sic
  Unit Test 2       —              Not yet    (Expected: Dec 2025)
  Annual            —              Not yet    (Expected: Apr 2026)

CBSE BOARD EXAM RESULTS (Class X):
  Rahul's class year: Will appear in March 2026 board exams
  Board result date: Typically May (CBSE publishes results)
  [When available: Board result will appear here with CBSE marksheet PDF]

PREVIOUS YEAR REPORT CARDS:
  Class IX (2024–25): Annual — [Download]
  Class VIII (2023–24): Annual — [Download]
  [3 years of history maintained]
```

---

## 6. Co-Curricular Performance

```
CO-CURRICULAR & ACTIVITIES — Rahul Rao

Sports:
  Cricket team member (school under-14) ✅
  Annual Sports Day: 100m Sprint — 2nd place (Silver) ✅

Activities:
  Science exhibition — participant ✅
  School quiz team — represented in inter-school quiz (CBSE cluster) ✅

Achievements logged:
  ● Quiz: Runner-up, CBSE Cluster Quiz, December 2025 [Certificate →]

Co-curricular grade (report card):
  Games/Sports: A (Excellent)
  Co-curricular participation: A (Active)
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/marks/current/` | Latest assessment marks |
| 2 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/marks/trend/` | Year-to-date performance trend |
| 3 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/marks/subject/{subject_id}/` | Subject deep-dive |
| 4 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/report-cards/` | All report cards list |
| 5 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/report-cards/{rc_id}/pdf/` | Download report card PDF |

---

## 8. Business Rules

- Marks are visible to parents only after the school releases them (VP/Principal approves release in B-series); before release, the parent sees "Results not yet available"; this prevents parents from seeing provisional or unchecked marks
- Class rank is shown because parents want to understand relative performance; however, the rank is shown as a number out of total (e.g., 11/39) — not as a percentile or "above/below average" qualitative label that could create stigma
- Report card PDFs downloaded by parents carry a watermark ("Downloaded by: Rahul Rao's parent, 27-Mar-2026") for DPDPA audit trail; this is a DPDPA principle — data access is logged and the download is traceable
- Teacher comments on report cards are visible to parents; they cannot be edited by the parent; if a parent disputes a comment, the grievance path (N-10) is available
- For students who change sections mid-year (rare but happens), the marks history is preserved under the student's permanent ID and shows all assessments regardless of which section they were in at the time

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
