# B-01 — Curriculum & Syllabus Management

> **URL:** `/college/academic/curriculum/`
> **File:** `b-01-curriculum.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HOD (S4) · Dean Academics (S5) · Faculty (S3) — view own courses · Registrar (S4)

---

## 1. Purpose

Manages the college's curriculum structure — programme-wise, year/semester-wise course listings, credit distributions, and syllabus documents. Critical for:
- NAAC accreditation (criterion 1 — Curricular Aspects)
- AICTE compliance (programme structure must match approved template)
- Faculty workload computation (courses × credits × sections)
- Student course registration pre-population
- Syllabus completion tracking (lesson plans in B-02 reference this)

---

## 2. Programme Structure

```
CURRICULUM — B.Tech CSE (R26 Regulation — JNTU Hyderabad)
AICTE Model Curriculum + JNTU-specific additions
Academic Year: 2026–27

SEMESTER I (Odd semester — July–December):
  S# Code    Course                          Category  Credits  Hours/wk
  1  MA101    Matrices & Calculus             BSC       4        4L+0T+0P
  2  CS101    Problem Solving with C          ESC       4        3L+0T+2P
  3  ME101    Engineering Workshop            ESC       1.5      0L+0T+3P
  4  EC101    Basic Electronics               ESC       3        3L+0T+0P
  5  CH101    Engineering Chemistry           BSC       3        3L+0T+0P
  6  EN101    English & Communication I       HSSC      2        2L+0T+0P
  7  CS103    Programming Lab                 ESC       1.5      0L+0T+3P
  8  CH103    Chemistry Lab                   BSC       1        0L+0T+2P
  ────────────────────────────────────────────────────────────────
  Semester I total credits: 20

[Full 8-semester curriculum — 160 credits for Honours]

CURRICULUM CATEGORIES:
  BSC = Basic Science Courses
  ESC = Engineering Science Courses
  PCC = Programme Core Courses
  PEC = Programme Elective Courses
  OEC = Open Elective Courses
  MC = Mandatory Courses (non-credit: Constitution, Environmental Studies)
  EAC = Employability / Activity Courses
  PROJ = Project work

CREDIT DISTRIBUTION (AICTE model — B.Tech):
  BSC: 20 credits  |  ESC: 18 credits  |  PCC: 50 credits
  PEC: 18 credits  |  OEC: 12 credits  |  MC: 4 (non-credit)
  EAC: 8 credits   |  PROJ: 16 credits  |  Internship: 6 credits
  ──────────────────────────────────────────────────────────
  Total: 152 credits (standard) + 8 research (Honours with Research)

[AICTE compliance check: Credit distribution vs AICTE guidelines]
  BSC (min 20%): 20/160 = 12.5% ⚠ ← AICTE requires 20% BSC
  [Review curriculum with Dean Academics]
```

---

## 3. Syllabus Documents

```
SYLLABUS — CS201: Data Structures & Algorithms
Regulation: R26 | Version: 2026

Credits: 4  |  Hours: 3L + 0T + 2P (Lab 2 hrs/week)
Pre-requisite: CS101 (Problem Solving with C)
Faculty: Dr. Anita K.

UNIT I: Introduction to Data Structures (9 hours)
  Primitive and non-primitive data structures, Linear and non-linear DS,
  Arrays, Stacks (LIFO), Queues (FIFO), Circular queues, Priority queues
  Implementation in C; Applications

UNIT II: Linked Lists (9 hours)
  Singly, Doubly, Circular linked lists; Operations; Applications;
  Memory management; Dynamic allocation

UNIT III: Trees (9 hours)
  Binary trees, BST, AVL trees, B-trees; Traversals; Applications

UNIT IV: Graphs (9 hours)
  Graph representations; BFS, DFS; Shortest paths (Dijkstra, Bellman-Ford);
  MST (Kruskal, Prim); Applications

UNIT V: Sorting & Searching (9 hours)
  Bubble, Selection, Insertion, Merge, Quick, Heap sort;
  Linear search, Binary search; Hashing

TOTAL: 45 theory hours + 30 lab hours

TEXT BOOKS:
  1. Tanenbaum, "Data Structures Using C" — Prentice Hall
  2. Sahni, "Data Structures, Algorithms & Applications in C++"

REFERENCE: Weiss, Cormen (CLRS) algorithms text

[Download syllabus PDF]  [View coverage tracking → B-02]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/curriculum/programmes/` | All programmes and structures |
| 2 | `GET` | `/api/v1/college/{id}/curriculum/courses/?programme={prog}&semester={sem}` | Courses for a semester |
| 3 | `GET` | `/api/v1/college/{id}/curriculum/course/{code}/syllabus/` | Syllabus document |
| 4 | `PUT` | `/api/v1/college/{id}/curriculum/course/{code}/syllabus/` | Update syllabus (HOD only) |
| 5 | `GET` | `/api/v1/college/{id}/curriculum/aicte-compliance/` | AICTE credit distribution check |

---

## 5. Business Rules

- Curriculum changes require Academic Council approval and JNTU (affiliating university) approval; a college cannot unilaterally change the syllabus for affiliated programmes; even adding an elective requires formal approval; EduForge tracks the approval status before making curriculum changes visible to students and faculty
- AICTE's model curriculum is a guideline; each state technical university (JNTU, VTU, Anna University) adapts it; the college must follow the university-prescribed curriculum, not directly the AICTE model; but AICTE inspects compliance with their own guidelines during inspection — the compliance check above flags gaps for proactive resolution
- Every semester's curriculum is version-controlled (R22, R26, R28 etc.); different batches may be on different regulations; a student who failed a subject and is repeating it may be doing so under an older regulation; the system must correctly identify which regulation applies to which student-subject combination

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division B*
