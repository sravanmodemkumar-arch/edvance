# B-03 — Syllabus Tracker

> **URL:** `/school/academic/dept/<dept>/syllabus/`
> **File:** `b-03-syllabus-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** HOD (S4) — full own dept · VP Academic (S5) — read all · Academic Coordinator (S4) — read all · Class Teacher (S3) — update own class · Subject Teacher (S3) — update own subject · Principal (S6) — full

---

## 1. Purpose

Tracks the pace of syllabus delivery across every subject and class in the department against the planned schedule. The HOD's primary accountability to the Principal is syllabus completion — if a class falls significantly behind, it means students will reach the board exam under-prepared. This page gives the HOD real-time visibility into which teacher is on pace, which is behind, and what remedial action (extra periods, reduced scope) is needed. It replaces the physical syllabus register maintained by each teacher.

**Indian context:** CBSE circulars remind schools every year that "100% syllabus completion before the board exam is mandatory." State board inspectors specifically check syllabus registers during school inspections. The NCERT/CBSE prescribed syllabus is topic-by-topic — each topic in this tracker maps to a specific chapter section in the board-prescribed textbook.

---

## 2. Page Layout

### 2.1 Header
```
Syllabus Tracker — Science Department              [Export Register]  [Print Summary]
Term: [Term 2 ▼]  Class: [All ▼]  Subject: [All ▼]  Teacher: [All ▼]
Academic Year: 2025–26  ·  Week 12 of 36  ·  Target completion: 33.3%
```

---

## 3. Summary Cards (Top Strip)

```
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│ Subjects On Track│ Subjects Behind  │ Avg Coverage     │ Expected by Week │
│   (≥ target %)   │   (< target %)   │   (all subjects) │   (auto-calc)    │
│                  │                  │                  │                  │
│      8           │       4          │     61.8%        │     33.3%        │
│  ✅ green        │  🔴 red          │  ↑ above target  │  Week 12 norm    │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

---

## 4. Main View — Subject × Class Coverage Grid

Default view shows a table of every subject-class combination in the department:

| Subject | Class | Teacher | Topics Done | Total Topics | Coverage % | Target % | Status | Last Updated |
|---|---|---|---|---|---|---|---|---|
| Physics | XII-A | Ms. Lakshmi | 14 | 26 | 53.8% | 33.3% | ✅ Ahead | 24 Mar |
| Physics | XII-B | Ms. Lakshmi | 13 | 26 | 50.0% | 33.3% | ✅ Ahead | 22 Mar |
| Chemistry | XII-A | Mr. Ravi | 10 | 28 | 35.7% | 33.3% | ✅ On Track | 25 Mar |
| Physics | XI-A | Dr. Suresh | 8 | 30 | 26.7% | 33.3% | ⚠️ Behind | 20 Mar |
| Biology | XI-B | Ms. Anjali | 5 | 30 | 16.7% | 33.3% | 🔴 Critical | 15 Mar |

Status logic:
- **✅ Ahead:** Coverage % > Target % + 5%
- **✅ On Track:** Coverage % within ±5% of target
- **⚠️ Behind:** Coverage % = target% − 5% to −15%
- **🔴 Critical:** Coverage % < target% − 15%

Click any row → expands to **topic-level detail** for that subject-class.

---

## 5. Topic-Level Detail (Expanded Row / Drawer)

When a subject-class row is clicked, a `topic-coverage-update` drawer opens (420px) showing the topic list:

### Drawer: Physics — Class XI-A (Dr. Suresh P)

```
Chapter / Topic                              Status          Date        Teacher Note
─────────────────────────────────────────────────────────────────────────────────────
Ch 1 — Physical World
  1.1 What is physics?                       ✅ Done         3 Feb       —
  1.2 Scope and excitement                   ✅ Done         4 Feb       —
  1.3 Physics, technology and society        ✅ Done         4 Feb       —

Ch 2 — Units and Measurements
  2.1 Introduction                           ✅ Done         6 Feb       —
  2.2 The international system of units      ✅ Done         7 Feb       —
  2.3 Measurement of length                  ✅ Done         10 Feb      —
  2.4 Measurement of mass                    ✅ Done         11 Feb      —
  2.5 Measurement of time                    🔄 In Progress  —           Started; practical pending
  2.6 Accuracy, precision, errors            ⬜ Not Started  —           —
  2.7 Significant figures                    ⬜ Not Started  —           —

Ch 3 — Motion in a Straight Line
  3.1 Introduction                           ⬜ Not Started  —           —
  ...
```

**Status options per topic:**
- ✅ Done — topic fully taught, including examples and exercises
- 🔄 In Progress — started but not completed
- ⏭️ Skipped — intentionally deferred to later (teacher must note reason)
- ⬜ Not Started — default

**[Mark as Done]** button per topic row — teacher can update directly. Date auto-stamps.

**[Update All Selected]** — bulk update with checkbox selection + status + date.

---

## 6. Progress Chart View

Toggle between Table and Chart views:

**Bar Chart (per subject-class):** Horizontal bars showing % done vs target %. Sorted by gap (most behind first). Colour-coded red/amber/green.

**Heat Map View:** Class levels (rows) × Subjects (columns) = % coverage. Same colour scale as B-01 syllabus section.

---

## 7. Syllabus Plan vs Actuals

The **planned pace** is set at the start of the term (from the Academic Year Planner B-38 or manually configured). The tracker compares actual coverage vs the plan:

| Week | Planned Topics Done (Physics XI-A) | Actual Topics Done | Gap |
|---|---|---|---|
| Week 1 | 3 | 3 | 0 |
| Week 2 | 6 | 6 | 0 |
| Week 3 | 9 | 8 | -1 |
| Week 4 | 12 | 10 | -2 |
| Week 5 | 15 | 11 | -4 🔴 |

---

## 8. HOD Alerts

Auto-generated alerts that appear in HOD's notification feed:

| Trigger | Alert |
|---|---|
| Subject falls 15%+ behind target | "Biology XI-B is 16.6% behind schedule — intervention needed" |
| Teacher hasn't updated in 10 days | "Physics XI-A: last update 10 days ago — check with Dr. Suresh" |
| Subject marked 100% complete before exam date | "Chemistry XII-A marked complete — well done, 3 weeks early" |
| Topic marked Skipped | "Mr. Ravi skipped Ch 9.4 (Chemistry XII-B) — review needed" |

Skipped topics require HOD acknowledgement — skipping without HOD approval generates an alert to VP Academic.

---

## 9. Exam Readiness Report

Available before each scheduled exam (B-10). Shows syllabus coverage status for classes appearing in the upcoming exam:

| Class | Subject | Coverage % | Topics Remaining | Days to Exam | Feasible? |
|---|---|---|---|---|---|
| XII-A | Physics | 78.4% | 6 topics | 21 days | ✅ Yes |
| XI-B | Biology | 55.0% | 14 topics | 21 days | ⚠️ Tight (0.67 topics/day needed) |
| XI-A | Chemistry | 42.3% | 16 topics | 21 days | 🔴 No (need 0.76/day; avg is 0.4) |

HOD can add a note ("Extra periods scheduled for XI-A Chemistry on Saturdays") to attach to the exam readiness report, which goes to Principal.

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/syllabus/?dept={dept_id}&term={term}` | Department-wide coverage grid |
| 2 | `GET` | `/api/v1/school/{id}/syllabus/{subject_id}/class/{class_id}/` | Topic list for a subject-class |
| 3 | `PATCH` | `/api/v1/school/{id}/syllabus/topics/{topic_id}/` | Update topic status (done/in-progress/skipped) |
| 4 | `POST` | `/api/v1/school/{id}/syllabus/topics/bulk-update/` | Bulk topic status update |
| 5 | `GET` | `/api/v1/school/{id}/syllabus/heatmap/?term={term}` | Heatmap data for chart view |
| 6 | `GET` | `/api/v1/school/{id}/syllabus/plan-vs-actual/?subject_id={id}&class_id={id}` | Weekly planned vs actual |
| 7 | `GET` | `/api/v1/school/{id}/syllabus/exam-readiness/?exam_id={id}` | Pre-exam coverage report |
| 8 | `GET` | `/api/v1/school/{id}/syllabus/export/?dept={dept_id}&term={term}` | Export register PDF |

---

## 11. Business Rules

- Target % is computed as: (working days elapsed in term ÷ total working days in term) × 100, with a configurable buffer (default +5% lead — expect teachers to be slightly ahead, not exactly at pace)
- Skipped topics must have a reason note; HOD must acknowledge skipped topics within 24 hours or VP Academic is auto-notified
- Teachers can only update topics for their own assigned subjects and classes
- HOD can update any topic in their department (for corrections or when a substitute teacher taught)
- Topic list is seeded from B-22 (Topic Master); HOD or Academic Coordinator must set up topics in B-22 first
- Deleted or archived topics show as ~~strikethrough~~ in the list (cannot be deleted if marked Done — audit requirement)
- Syllabus completion % feeds into teacher performance scoring (weight: 30%) visible in B-05 (Dept Analytics)
- Export Register generates a format identical to the physical syllabus register (one row per topic, with completion date and teacher signature column — "signed by HOD" footer for inspection)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
