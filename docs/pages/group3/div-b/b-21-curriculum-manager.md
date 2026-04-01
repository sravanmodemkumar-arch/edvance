# B-21 — Curriculum Manager

> **URL:** `/school/academic/curriculum/`
> **File:** `b-21-curriculum-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Coordinator (S4) — full · HOD (S4) — own dept · Principal (S6) — full · VP Academic (S5) — full

---

## 1. Purpose

Manages the school's curriculum structure — which subjects are taught in which classes, what the annual syllabus for each subject is, board-prescribed frameworks, and how the curriculum maps to learning outcomes. This is the master reference data that the Syllabus Tracker (B-03), Topic Master (B-22), and Lesson Plan workflows all draw from. The Academic Coordinator maintains this and aligns it with the latest NCERT/CBSE syllabus updates each year. NEP 2020 has significantly changed curriculum structures — integration of vocational subjects, reduced rote content, competency-based learning objectives — and this page is where those changes are reflected in the school's actual offering.

---

## 2. Page Layout

### 2.1 Header
```
Curriculum Manager                                [+ Add Subject]  [Import Board Syllabus]  [Export Curriculum Map]
Academic Year: 2025–26  ·  Board: CBSE  ·  Classes: LKG–XII
Subjects configured: 42  ·  Active: 40  ·  Pending review: 2
```

---

## 3. Curriculum Tree

Left panel: Class level → Subjects tree

```
Class Level Tree
─────────────────────────────
▼ Primary (I–V)
   ├── English (Core)
   ├── Hindi (Core)
   ├── Mathematics (Core)
   ├── Environmental Studies (Core)
   ├── Computer Science (Additional)
   └── Art & Craft (Activity)

▼ Middle (VI–VIII)
   ├── English (Core)
   ├── Hindi (Core)
   ├── Mathematics (Core)
   ├── Science (Core)
   ├── Social Studies (Core)
   ├── Sanskrit (3rd Language)
   ├── Computer Science (Additional)
   └── Physical Education (Activity)

▼ Secondary (IX–X)
   ├── English (Core)
   ├── Hindi (Core)
   ├── Mathematics (Core)
   ├── Science (Core)
   ├── Social Studies (Core)
   └── Computer Applications (Additional/Optional)

▼ Senior Secondary (XI–XII)
   ├── Stream: MPC
   │   ├── English (Core)
   │   ├── Mathematics (Core)
   │   ├── Physics (Core)
   │   ├── Chemistry (Core)
   │   ├── Computer Science (Elective)
   │   └── Physical Education (Optional)
   ├── Stream: BiPC
   │   ├── English (Core)
   │   ├── Biology (Core)
   │   ├── Physics (Core)
   │   ├── Chemistry (Core)
   │   └── Psychology (Optional)
   └── Stream: Commerce
       ├── English (Core)
       ├── Accountancy (Core)
       ├── Business Studies (Core)
       ├── Economics (Core)
       └── Mathematics (Elective)
```

Click any subject → opens subject detail on right panel.

---

## 4. Subject Detail Panel

### Subject: Science — Class IX (CBSE)

```
Subject Details
─────────────────────────────────────────────────
Name:         Science
Class:        IX
Board:        CBSE
Code:         CBSE086 (CBSE subject code)
Type:         Core (mandatory)
Max Marks:    100 (80 theory + 20 IA)
Theory Marks: 80
IA Marks:     20 (3 PTs + Notebook + Enrichment)
Practical:    No formal board practical
Duration:     3 hours (theory paper)
Periods/Week: 6 (includes 1 double-period lab)
Language:     English (medium)

NCERT Textbook: Science – Class IX (NCERT, 2023 edition)
CBSE Syllabus Updated: 2023–24 (rationalized syllabus)

Chapters: 15 chapters (see Topic Master B-22)
─────────────────────────────────────────────────
Learning Objectives:
• Apply scientific method to real-world phenomena
• Understand fundamental concepts of Physics, Chemistry, Biology
• Develop lab skills through practical work

NEP 2020 Integration:
• Competency-based questions included in assessments
• Bagless day: Science activity once per week
• Integration with environmental studies

Assessment Pattern:
  Section A: MCQ (1m × 20 = 20m)
  Section B: SA1 (2m × 5 = 10m)
  Section C: SA2 (3m × 8 = 24m)
  Section D: LA (5m × 3 = 15m)
  Section E: Case-based (4m × 2 + 1m × 1 = 11m)
─────────────────────────────────────────────────
Teachers Assigned (2025–26): Ms. Anjali Singh (IX-A, IX-B), Mr. Ravi Kumar (IX-C)
Status: ✅ Active
[Edit]  [View Topics (B-22)]  [View Syllabus Tracker (B-03)]
```

---

## 5. Import Board Syllabus

[Import Board Syllabus] → imports latest CBSE/board-prescribed syllabus:

| Board | Class | Subject | Syllabus Version | Status |
|---|---|---|---|---|
| CBSE | IX | Science | 2023–24 Rationalized | ✅ Imported |
| CBSE | X | Mathematics | 2024–25 | ✅ Imported |
| CBSE | XI | Physics | 2024–25 | ⬜ Import Available |
| CBSE | XI | Chemistry | 2024–25 | ⬜ Import Available |

[Import All Available] → imports all CBSE syllabus updates as new topic lists in B-22.

EduForge maintains a curated CBSE/NCERT syllabus database that schools can import from. After import, Academic Coordinator reviews and publishes.

---

## 6. Curriculum Gap Analysis

System-generated report showing gaps between:
- Board-prescribed syllabus (imported)
- School's configured topic list (B-22)

| Subject | Class | Board Chapters | School Topics | Missing | Extra |
|---|---|---|---|---|---|
| Science | IX | 15 chapters, 89 topics | 15 chapters, 89 topics | 0 | 0 ✅ |
| Mathematics | XI | 16 chapters, 112 topics | 14 chapters, 98 topics | 14 topics | 0 ⚠️ |
| Economics | XI | 10 chapters, 72 topics | 10 chapters, 74 topics | 0 | 2 (school additions) |

Academic Coordinator resolves gaps by updating B-22 (Topic Master).

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/curriculum/?year={year}` | Full curriculum tree |
| 2 | `GET` | `/api/v1/school/{id}/curriculum/subject/{subject_id}/` | Subject detail |
| 3 | `POST` | `/api/v1/school/{id}/curriculum/subjects/` | Add subject |
| 4 | `PATCH` | `/api/v1/school/{id}/curriculum/subjects/{subject_id}/` | Update subject |
| 5 | `POST` | `/api/v1/school/{id}/curriculum/import-board/` | Import board syllabus |
| 6 | `GET` | `/api/v1/school/{id}/curriculum/gap-analysis/` | Gap analysis report |
| 7 | `GET` | `/api/v1/school/{id}/curriculum/export/` | Export curriculum map PDF |

---

## 8. Business Rules

- Subjects cannot be deleted if they have historical marks data; only archived
- Board subject codes (CBSE subject codes like 086, 041) must be correct for CBSE portal submissions — validated against CBSE master list
- Subject periods/week from this page feed as default into B-30 (Subject Allocation); Timetable Coordinator can override per class
- CBSE rationalized syllabus (2023–24 onward) reduces content by ~30%; schools that imported old syllabus must re-import to align with reduced topic list; gap analysis highlights this
- NEP 2020 integration fields (activity-based learning, bagless day subjects) are informational; they affect lesson plan templates but not assessment marks

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
