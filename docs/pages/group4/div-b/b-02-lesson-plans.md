# B-02 — Lesson Plans & Course Files (NAAC)

> **URL:** `/college/academic/lesson-plans/`
> **File:** `b-02-lesson-plans.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Faculty (S3) — own courses · HOD (S4) · Dean Academics (S5)

---

## 1. Purpose

Every faculty member must prepare a lesson plan before the semester begins and maintain a course file throughout the semester. This is:
- A NAAC criterion 2.2 evidence document ("Teaching-Learning Process")
- An academic quality assurance tool
- A record of curriculum coverage (inspectors verify that the entire syllabus was taught)
- Protection for students (if a faculty member is replaced mid-semester, the course file tells the replacement where the class is)

---

## 2. Lesson Plan — Faculty Entry

```
LESSON PLAN — CS201: Data Structures & Algorithms
Faculty: Dr. Anita K.  |  Class: CSE-A (38 students) + CSE-B (40 students)
Semester II 2026–27  |  Total theory hours: 45  |  Lab hours: 30
Prepared on: 8 January 2027  (Before semester begins — NAAC requirement)

WEEKLY PLAN:
  Week  Date       Unit  Topic                        Hours  Remarks
  1     12 Jan     I     Introduction; Primitive DS    3      Theory
  1     12 Jan     I     Arrays — implementation       2      Lab
  2     19 Jan     I     Stacks — LIFO concept          3     Theory
  2     19 Jan     I     Stack implementation (C)       2     Lab
  3     26 Jan     —     Republic Day (26 Jan)           —    Holiday
  3     28 Jan     I     Queues, Circular Q             3     Theory
  3     28 Jan     I     Queue implementation           2     Lab
  4     2 Feb      II    Linked List — Singly LL        3     Theory
  4     2 Feb      II    LL implementation              2     Lab
  [... continues to Week 15]

  Final week: Revision + question paper practice (2 hours)
  Total planned: 45 theory + 30 lab = 75 hours ✅ (matches syllabus)

INTERNAL ASSESSMENT SCHEDULE (CIE — B-03):
  Mid-I exam: 15 February 2027 (Unit I + II)
  Mid-II exam: 20 March 2027 (Unit III + IV)
  Assignment 1 due: 30 January 2027
  Assignment 2 due: 28 February 2027

[Save Lesson Plan]  [Approve (HOD)]  [Download PDF for NAAC]
```

---

## 3. Course File — Semester Progress Tracking

```
COURSE FILE — CS201 (Dr. Anita K.)
Semester II 2026–27 — Status as of 27 March 2027

SYLLABUS COMPLETION:
  Unit I:   9/9 hours ✅ (completed 28 Jan 2027)
  Unit II:  9/9 hours ✅ (completed 18 Feb 2027)
  Unit III: 9/9 hours ✅ (completed 7 Mar 2027)
  Unit IV:  7/9 hours ⏳ (in progress — 2 hours remaining: Prim MST + Applications)
  Unit V:   0/9 hours ⬜ (planned: 28 Mar – 12 Apr 2027)
  ─────────────────────────────────────────────────
  Theory: 34/45 hours (75.6%)
  Labs: 28/30 hours (93.3%)

PROJECTED COMPLETION:
  Unit IV completion: 29 March 2027
  Unit V completion: 13 April 2027
  All labs: 10 April 2027
  Buffer before exam (14 April revision): ✅ On track

DEVIATIONS FROM LESSON PLAN:
  Week 5 (9 Feb): Swapped Linked List and Trees topics — HOD approved ✅
  Week 8 (1 Mar): Class cancelled (Dr. Anita attended CBSE workshop) — substitute arranged ✅

INTERNAL MARKS STATUS (CIE — B-03):
  Mid-I: ✅ Conducted 15 Feb; marks entered
  Mid-II: ✅ Conducted 20 Mar; marks entered
  Assignments: Both submitted; marks entered ✅
  CIE total (so far): Complete ✅

[Download course file PDF]  [NAAC compliance: Lesson plan + course file = criterion 2.2 evidence]
```

---

## 4. HOD Oversight Dashboard

```
DEPARTMENT COURSE FILE STATUS — CSE Department
HOD: Dr. Kavitha R.  |  Semester II 2026–27

Faculty         Course  Lesson Plan  Syllabus%  CIE Done  NAAC Ready
Dr. Anita K.    CS201   ✅ Approved  75.6%      ✅         ✅
Mr. Suresh V.   CS203   ✅ Approved  82.1%      ✅         ✅
Dr. Ramesh M.   CS205   ✅ Approved  71.4%      ✅         ⚠ (2 units pending)
Ms. Neeraja R.  HS201   ✅ Approved  88.9%      ✅         ✅
Mr. Pradeep T.  EE201   ⚠ Pending   68.2%      ⏳         ⚠ (lesson plan not approved)
...

ALERTS:
  ⚠ Mr. Pradeep (EE201): Lesson plan not yet approved by HOD — semester 2/3 complete
  ⚠ Dr. Ramesh (CS205): Syllabus coverage 71.4% — at risk of not completing by exam

[HOD review Mr. Pradeep's lesson plan]  [Schedule catch-up for CS205]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/academic/lesson-plan/` | Create lesson plan |
| 2 | `PATCH` | `/api/v1/college/{id}/academic/lesson-plan/{id}/approve/` | HOD approve lesson plan |
| 3 | `GET` | `/api/v1/college/{id}/academic/course-file/{faculty_id}/{course_code}/` | Course file status |
| 4 | `PATCH` | `/api/v1/college/{id}/academic/course-file/{id}/progress/` | Update syllabus completion |
| 5 | `GET` | `/api/v1/college/{id}/academic/dept-coverage/?dept={dept}` | Department-wide coverage status |
| 6 | `GET` | `/api/v1/college/{id}/academic/naac-evidence/?criterion=2.2` | NAAC criterion 2.2 evidence package |

---

## 6. Business Rules

- Lesson plans must be submitted before the semester begins (before the first class); this is standard NAAC expectation (criterion 2.2); late lesson plans (submitted after semester starts) are noted as process gaps; HODs must approve lesson plans within the first week of semester
- Syllabus completion below 85% at exam time is a serious academic quality flag; if syllabus is not completed, students are disadvantaged in university exams (which test the full syllabus regardless of what the college covered); HOD and Dean Academics must intervene with extra classes / online sessions
- Course file deviations (topic swaps, class cancellations) must be documented with reasons and HOD acknowledgement; an undocumented deviation (class never taught, no record) looks like academic fraud during NAAC inspection
- NAAC assessors specifically ask for lesson plans with HOD signatures from the previous 3 years; a college that cannot produce these (even if teaching happened) receives a lower score on criterion 2.2; EduForge's digital lesson plan with timestamps and HOD e-approval is NAAC-accepted

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division B*
