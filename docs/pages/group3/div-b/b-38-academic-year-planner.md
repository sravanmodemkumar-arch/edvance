# B-38 — Academic Year Planner

> **URL:** `/school/academic/planner/`
> **File:** `b-38-academic-year-planner.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Coordinator (S4) — full · Principal (S6) — approve/publish · VP Academic (S5) — full · HOD (S4) — read

---

## 1. Purpose

The pre-academic-year planning workspace where the Academic Coordinator designs the entire academic calendar before the year begins. This is distinct from A-10 (Academic Calendar) which is a display tool — B-38 is the planning and decision-making tool. The coordinator makes decisions here: how many terms, when each PT occurs, what the minimum instructional days target is, when project deadlines fall, when PTMs happen. Once finalised and approved by the Principal, this plan exports to A-10 (Academic Calendar), seeds B-10 (Exam Schedule), and gives B-03 (Syllabus Tracker) its pace targets.

**CBSE requirement:** Minimum 220 working days per academic year (excluding Sundays, public holidays, PTMs). This planner helps ensure compliance.

---

## 2. Page Layout

### 2.1 Header
```
Academic Year Planner                             [Save Draft]  [Publish Plan]  [Export to Calendar]
Academic Year: [2026–27 ▼]  ·  Status: ⬜ Draft
Board: CBSE  ·  Planning Status: Not started
Published Plan (current year 2025–26): [View 2025–26 Plan]
```

---

## 3. Year Structure Setup

### 3.1 Academic Year Boundaries

| Field | Value |
|---|---|
| Academic Year | 2026–27 |
| Year Start | 1 April 2026 |
| Year End | 31 March 2027 |
| Board | CBSE |
| Term Structure | [2 Terms ▼] / 3 Terms / Semester |

### 3.2 Term Definition

| Term | Start | End | Working Days | Notes |
|---|---|---|---|---|
| Term 1 | 1 Apr 2026 | 28 Sep 2026 | 108 | Apr–Sep including summer |
| Term 2 | 1 Oct 2026 | 31 Mar 2027 | 112 | Oct–Mar including winter |
| **Total** | | | **220** | ✅ CBSE minimum met |

**Working Days Counter** — auto-computed by excluding:
- Sundays (all)
- Public holidays imported from A-11 (Holiday Calendar)
- Pre-configured school holidays (Dussehra, Diwali, Pongal, etc.)
- PTM days (marked as non-instructional)

---

## 4. Assessment Schedule Planner

CBSE mandates minimum 3 Periodic Tests per year:

| # | Assessment | Type | Scheduled For | Duration | Max Marks | Classes | Status |
|---|---|---|---|---|---|---|---|
| 1 | Periodic Test 1 | Internal | 15–22 Apr 2026 | 1 week | 40 | I–XII | ⬜ Draft |
| 2 | Unit Test / Activity | Internal | 20–25 Jun 2026 | 4 days | 25 | VI–X | ⬜ Draft |
| 3 | Periodic Test 2 | Internal | 18–26 Aug 2026 | 1 week | 40 | I–XII | ⬜ Draft |
| 4 | Half-Yearly Exam | Major | 5–22 Oct 2026 | 2.5 weeks | 80 | VI–XII | ⬜ Draft |
| 5 | Periodic Test 3 | Internal | 5–12 Jan 2027 | 1 week | 40 | I–XII | ⬜ Draft |
| 6 | Pre-Board | Pre-Board | 1–15 Feb 2027 | 2 weeks | 80 | X, XII | ⬜ Draft |
| 7 | Annual Exam | Major | 1–22 Mar 2027 | 3 weeks | 80/100 | I–XI | ⬜ Draft |
| 8 | CBSE Board | Board | Per CBSE datesheet | 6+ weeks | 80 | X, XII | Board dates TBD |

[+ Add Assessment] — custom assessment (Sports Day make-up test, etc.)

**Conflict check:**
- No two assessments for the same class overlap in dates
- No assessment falls on a declared holiday
- 4-week gap between major assessments (configurable)

---

## 5. Project & Activity Deadline Planner

| Activity | Classes | Deadline | Submitted Via | Notes |
|---|---|---|---|---|
| Science Project (CBSE) | VI–X | 15 Sep 2026 | Class teacher | CBSE Social Science/Science project |
| Social Science Project | IX–X | 20 Sep 2026 | Class teacher | CBSE SuE 5m |
| Annual School Magazine | All | 28 Feb 2027 | Editor (student club) | Content submitted by class teachers |
| Career Guidance Workshop | X, XII | Oct–Nov 2026 | VP Academic | Annual event |
| Sports Day | All | 15 Jan 2027 | PE teacher | Full-day event; timetable adjusted |
| Science Exhibition | All | 5 Feb 2027 | Science HOD | Intra-school; top entries for CBSE exhibition |
| Annual Day | All | 28 Feb 2027 | Admin | Full-day event |

---

## 6. PTM (Parent-Teacher Meeting) Calendar

| PTM # | Purpose | Scheduled | Classes | Duration |
|---|---|---|---|---|
| PTM 1 | Post-PT1 results | 30 Apr 2026 | All | Half day |
| PTM 2 | Half-yearly results + progress | 15 Nov 2026 | All | Full day |
| PTM 3 | Annual result + promotion | 15 Apr 2027 | All | Full day |

PTM days are marked as non-instructional in the Working Days counter.

---

## 7. Instructional Days Compliance Report

| Month | Working Days (Raw) | Holidays | PTMs | Net Instructional | Cumulative |
|---|---|---|---|---|---|
| April 2026 | 24 | 3 (Ram Navami, Ambedkar J., etc.) | 1 (PTM) | 20 | 20 |
| May 2026 | 25 | 2 | 0 | 23 | 43 |
| June 2026 | 4 (summer vacation ends 22 Jun) | 1 | 0 | 3 | 46 |
| … | … | … | … | … | … |
| March 2027 | 22 | 4 (Holi, etc.) | 1 | 17 | 220 |

**CBSE compliance:** ≥ 220 days. 🟢 **On track: 220/220 projected.**

If projected total falls below 220, warning shown and Academic Coordinator must add compensatory Saturdays.

---

## 8. Publish Plan

[Publish Plan] → after Principal approval:
1. All scheduled exams exported to B-10 (Exam Schedule Manager) as draft exam entries
2. Assessment dates exported to A-10 (Academic Calendar) as exam events
3. PTM dates exported to A-10 as PTM events
4. Syllabus pace targets auto-computed in B-03 (based on term dates + working days)
5. All HODs, Class Teachers, and Subject Teachers notified: "Academic Year 2026–27 plan published"

---

## 9. Previous Year Reference

[View 2025–26 Plan] → shows the current year's plan in read-only mode, useful for reference when planning the next year.

Copy from previous year → [Use 2025–26 as Template] → imports all structure; coordinator adjusts dates.

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/academic-planner/?year={year}` | Year plan |
| 2 | `PATCH` | `/api/v1/school/{id}/academic-planner/{year}/` | Update plan |
| 3 | `POST` | `/api/v1/school/{id}/academic-planner/{year}/assessments/` | Add assessment |
| 4 | `GET` | `/api/v1/school/{id}/academic-planner/{year}/compliance/` | Instructional days report |
| 5 | `POST` | `/api/v1/school/{id}/academic-planner/{year}/publish/` | Publish to all modules |
| 6 | `GET` | `/api/v1/school/{id}/academic-planner/{year}/export/` | Export plan PDF |

---

## 11. Business Rules

- The Academic Year Planner can only be created/edited by the Academic Coordinator and Principal
- Publishing the plan pushes data to B-10, A-10, and B-03 — it cannot be undone without re-publishing a revised version
- CBSE's 220-day minimum is a hard warning — the plan cannot be approved by Principal if projected instructional days < 220 without a documented exception
- Previous year plans are retained permanently for reference; only the current and next year plans are editable

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
