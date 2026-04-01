# C-10 — Class Promotion Manager

> **URL:** `/school/students/promotion/`
> **File:** `c-10-class-promotion-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Academic Coordinator (S4) — full · Principal (S6) — full · Class Teacher (S3) — view own class

---

## 1. Purpose

Manages the annual year-end process of moving students from their current class to the next — the single most consequential operation at year end. Without this operation, all 380 students remain in their 2025–26 classes for the 2026–27 year. Class Promotion Manager:
1. Processes result data from B-18 (Result Computation)
2. Assigns a promotion decision to each student: Promoted / Retained / Promoted with Compartment / Supplementary Exam
3. Handles Class XI stream allocation (new students + IX→XI moving up)
4. Restructures sections (merge thin sections, create new sections if enrollment grows)
5. Reassigns roll numbers in the new classes

This is a careful, multi-step process done under the Academic Coordinator's oversight with Principal approval. Errors here (wrong student promoted, wrong class assigned) cascade to attendance, fees, and marks for the entire next year.

**NEP 2020 No-Detention Policy:** Classes I–V (primary) — no student can be retained on academic grounds alone; they are promoted regardless of marks. Class VI–VIII — state-specific (some states extended no-detention to VIII). Class IX+ — normal pass/fail rules apply.

**CBSE Rule:** Students failing in Class IX must appear in supplementary exam (B-39). If they fail supplementary, they repeat Class IX. Students who pass CBSE Class X board automatically move to Class XI (school cannot retain a board-passed student).

---

## 2. Page Layout

### 2.1 Header
```
Class Promotion Manager — Year-End 2025–26    [Start Promotion Process]  [Bulk Promote]  [Export Promotion List]
Status: Promotion in Progress
Results Finalised: ✅  |  Promotion Decisions: 342/380 done  |  Sections Restructured: ⬜  |  Principal Approved: ⬜
Current Year: 2025–26  →  Promoting to: 2026–27
```

### 2.2 Class-wise Promotion Status
| Current Class | Students | Promoted | Retained | Supplementary | Section Change | Status |
|---|---|---|---|---|---|---|
| Nursery | 40 | 40 | 0 | — | No change | ✅ Done |
| LKG | 38 | 38 | 0 | — | No change | ✅ Done |
| Class I | 41 | 41 | 0 | — | No change | ✅ Done |
| Class V | 38 | 38 | 0 | — | (NEP — no detention) | ✅ Done |
| Class VIII | 42 | 40 | 0 | 2 | No change | 🔄 In Progress |
| Class IX | 38 | 34 | 2 | 2 | No change | 🔄 In Progress |
| Class X | 36 | 36 | 0 | 0 | → Goes to Class XI | ✅ Done |
| Class XI | 38 | 36 | 1 | 1 | No change | 🔄 In Progress |
| Class XII | 34 | 34 | 0 | 0 | → Alumni (graduated) | ✅ Done |

---

## 3. Promotion Prerequisite Check

Before starting the promotion process:

```
Prerequisite Checklist:
✅ Results finalised (B-18) for all classes
✅ Supplementary exam results entered (B-39) for Class IX, X, XI
✅ Board exam results imported (Class X: CBSE May 2026)
⬜ Class XII board results imported — waiting (CBSE declares June 2026)
⬜ Class XI compartment results imported — waiting

[Proceed with available classes]  [Wait for all results]
```

Academic Coordinator can proceed class by class as results become available.

---

## 4. Promotion Decision — Class IX Example

### 4.1 Decision Grid
```
Class IX-A — 2025–26 — Promotion to Class X-A (2026–27)

Roll  Name          Phy  Che  Bio/Mat  Eng  SSt  Hindi  Total   Pass?  Supp?  Decision
01    Anjali Das    78   82   75       80   76   72     463/600  ✅    —      Promoted ▼
02    Arjun Sharma  42   45   38       52   48   55     280/600  ❌    ✅     Supplementary (Math) ▼
03    Priya Venkat  82   86   84       84   80   78     494/600  ✅    —      Promoted ▼
04    Rohit Kumar   28   32   30       45   38   42     215/600  ❌    ❌     Retained ▼
```

The [▼] dropdown for each student shows options:
- **Promoted** — moves to next class
- **Supplementary Exam** — failed in 1–2 subjects; gets supplementary exam attempt (B-39)
- **Promoted with Grace** — passed after grace marks (B-37) — shown automatically
- **Retained** — failed in 3+ subjects (or failed supplementary); stays in same class
- **NEP Promoted (No-Detention)** — Classes I–V; promoted regardless
- **Special Promotion** — Principal's discretionary promotion (requires written justification)

### 4.2 Batch Action
For classes where all students passed:
```
Class V-A — 42 students — All passed (NEP No-Detention applied)
[Bulk Promote All → Class VI-A] ✓
```

---

## 5. Class X → Class XI (Stream Allocation)

Special flow for students moving from Class X to Class XI:

### 5.1 Board Result Import
```
CBSE Class X Board Results 2026 — Import
[Upload CSV from CBSE website]  or  [Manual Entry]

Matched to school students: 36/36
Results mapped: Passed 36, Failed 0, Compartment 0
```

### 5.2 Stream Application

After board results are imported, each Class X student (now promoted to XI) must declare a stream:

```
Stream Allocation — Class XI 2026–27

Student              Class X %  Board Merit  Applied Stream  Eligible  Allocated Section
Arjun Sharma         85.4%      ✅           Science (PCM)   ✅         XI-A
Priya Venkat         88.2%      ✅           Science (PCB)   ✅         XI-A
Rohit Kumar          72.1%      ✅           Commerce        ✅         XI-C
Anjali Das           68.4%      ✅           Arts            ✅         XI-E
Suresh M.            55.2%      ✅           Commerce        ⚠️ Low %   XI-C (Principal approval req.)
```

Stream eligibility criteria are school-configurable (e.g., Science PCM requires Class X Math ≥ 60%).

### 5.3 New Students for Class XI
Students admitted fresh into Class XI (from other schools) are enrolled in C-05 and added to the stream allocation here.

---

## 6. Section Restructuring

If enrollment changes significantly (new sections needed or thin sections to merge):

```
Section Restructuring — 2026–27

Current Class X:    2 sections (A: 38, B: 36) → Total: 74 students
New Class XI:       Science: 52 (new: 38 + transfers: 14)
                    Commerce: 18
                    Arts: 4

Suggested:
  XI-A: Science PCM — 28 students
  XI-B: Science PCB — 24 students
  XI-C: Commerce — 18 students
  XI-D: Arts — 4 students (merge into XI-C if Arts < 10)

[Accept Suggestion]  [Customize Sections]
```

---

## 7. Roll Number Reassignment

After sections are confirmed, roll numbers are reassigned for the new year:

```
Class XI-A — Roll Number Assignment

Options:
○ Alphabetical (default)
● Carry forward from Class X
○ Custom order

[Generate Roll Numbers]

Roll  Student Name         Previous Class  Previous Roll
01    Anjali Das           X-A             01
02    Arjun Sharma         X-A             02  (transferred from another school: fresh roll)
03    Priya Venkat         X-B             14
...
```

---

## 8. Principal Approval & Activation

After all classes are processed:

```
Promotion Summary — Ready for Principal Approval
Academic Year: 2025–26 → 2026–27

Total Students Processed: 380
  Promoted (normal):     342
  NEP Promoted:           72 (Classes I–V)
  Supplementary Exam:     12 (pending B-39 results)
  Retained:                8
  Class XII Graduated:    34 → Alumni Registry (C-22)
  New Enrollments (XI):   22

[Review and Approve — Principal]

Once approved, promotion becomes effective:
  • All student class/section records update
  • Attendance modules initialise for 2026–27
  • Fee structures apply for new classes
  • Timetable builder (B-07) becomes active for 2026–27
```

After Principal approval, changes are committed and cannot be bulk-undone (individual corrections possible through C-11 Internal Transfer).

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/promotion/?year={year}` | Promotion status overview |
| 2 | `GET` | `/api/v1/school/{id}/students/promotion/{class_id}/` | Class-wise promotion decisions |
| 3 | `PATCH` | `/api/v1/school/{id}/students/promotion/{student_id}/decision/` | Set promotion decision per student |
| 4 | `POST` | `/api/v1/school/{id}/students/promotion/{class_id}/bulk-promote/` | Bulk promote entire class |
| 5 | `GET` | `/api/v1/school/{id}/students/promotion/xi/stream-allocation/` | Class XI stream allocation view |
| 6 | `PATCH` | `/api/v1/school/{id}/students/promotion/xi/stream-allocation/{student_id}/` | Assign stream |
| 7 | `POST` | `/api/v1/school/{id}/students/promotion/sections/restructure/` | Section restructure plan |
| 8 | `POST` | `/api/v1/school/{id}/students/promotion/roll-numbers/generate/` | Generate roll numbers for new year |
| 9 | `POST` | `/api/v1/school/{id}/students/promotion/approve/` | Principal approval — activates promotion |

---

## 10. Business Rules

- Promotion cannot be activated until B-18 result computation is finalised for that class — system enforces this prerequisite
- NEP 2020 no-detention: Classes I–V are automatically flagged for promotion; the system does not allow "Retained" status for these classes (Principal override with very high friction — requires written reason and is logged for RTE compliance)
- Class X board-passed students cannot be retained in Class X — CBSE rules; system hard-blocks this
- Once Principal approval is given and promotion is activated, it is irreversible in bulk; individual student corrections require the C-11 Internal Transfer path
- Class XII graduates are automatically moved to Alumni Registry (C-22); their student profile remains accessible as historical record
- Stream eligibility thresholds for Class XI are school-configurable but cannot be set higher than CBSE recommendations

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
