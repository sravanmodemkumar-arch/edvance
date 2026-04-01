# A-08 — Class & Section Manager

> **URL:** `/school/admin/classes/`
> **File:** `a-08-class-section-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Principal (S6) — full · VP Academic (S5) — full · VP Admin (S5) — view

---

## 1. Purpose

Defines the school's complete class-section structure for the academic year. Every other module depends on this: attendance is taken per class-section, timetable is built per class-section, exam seating is assigned per class-section, fee structure can be differentiated by stream/section type. Changes here propagate platform-wide — deleting a section that has enrolled students requires a migration workflow.

**Indian school structure specifics:**
- Naming conventions vary: Class 1/I/One, LKG/Nursery/Kindergarten, Section A/B/C/D
- Schools often add sections mid-year when enrolment exceeds projections
- XI–XII sections are stream-based: MPC, BiPC, MEC, CEC, HEC, Computer Science combinations
- Integration coaching schools add parallel batch sections (e.g., "XI MPC A — Regular", "XI MPC B — IIT Track")

---

## 2. Page Layout

### 2.1 Header
```
Class & Section Manager — Academic Year 2025–26          [+ Add Class] [+ Add Section] [Print Structure]
Total: 14 classes · 52 sections · 1,048 students enrolled
```

### 2.2 View Toggle
```
[Tree View ▼]  [Grid View]  [Table View]
```

---

## 3. Tree View (default)

Expandable tree: Level → Class → Sections

```
Pre-Primary
  ├── LKG        [3 sections: A, B, C] — 78 students — Class Teacher: Ms. Anitha, Mr. Raju, Ms. Kavitha
  └── UKG        [3 sections: A, B, C] — 82 students

Primary (I–V)
  ├── Class I    [4 sections: A, B, C, D] — 142 students
  ├── Class II   [4 sections: A, B, C, D] — 138 students
  ├── Class III  [4 sections: A, B, C, D] — 136 students
  ├── Class IV   [3 sections: A, B, C]    — 108 students
  └── Class V    [3 sections: A, B, C]    — 104 students

Upper Primary (VI–VIII)
  ├── Class VI   [3 sections: A, B, C] — 96 students
  ├── Class VII  [3 sections: A, B, C] — 92 students
  └── Class VIII [3 sections: A, B, C] — 87 students

Secondary (IX–X)
  ├── Class IX   [4 sections: A, B, C, D] — 112 students
  └── Class X    [4 sections: A, B, C, D] — 108 students

Senior Secondary (XI–XII)
  ├── Class XI   [MPC A · MPC B · BiPC A · BiPC B · Commerce A · Humanities A] — 76 students
  └── Class XII  [MPC A · MPC B · BiPC A · BiPC B · Commerce A · Humanities A] — 73 students
```

Click any section row → opens section detail drawer.

---

## 4. Section Detail Drawer

**480px wide**

**Header:** Class XI · Section MPC A · 38 students enrolled

**Tabs: Overview · Students · Subjects · Settings**

**Overview:**
- Class Teacher: [Select Staff ▼]
- Room No / Classroom: [Enter]
- Medium of instruction: English / Regional language
- Section type: Regular / Scholarship / IIT Track / NEET Track / Composite
- Max capacity: 40 · Current: 38 · Available seats: 2

**Students tab:**
- List of all enrolled students in this section (Name · Roll No · Gender · Admission Status)
- [Move Student to Another Section] per student (triggers migration workflow)
- [Bulk Move] — move multiple students + maintain roll number sequence

**Subjects tab:**
- List of subjects taught in this section/stream
- Subject · Periods/Week · Teacher Assigned · Status
- [Edit Subjects →] link to A-09 Stream Configuration

**Settings:**
- Section active: Yes / No (deactivate = no new enrolments; existing students unaffected)
- Use custom roll number prefix: [e.g., "11MPA-"]
- Include in CBSE reports: Yes / No

---

## 5. Add/Edit Class Form

**Triggered by [+ Add Class]**

| Field | Description |
|---|---|
| Class Name | Dropdown: LKG · UKG · Class I–XII (or custom for some boards) |
| Display Name | Auto-filled; overridable (e.g., "Year 11" for IB schools) |
| Level | Pre-Primary / Primary / Upper Primary / Secondary / Senior Secondary |
| Stream (XI–XII only) | MPC / BiPC / MEC / CEC / HEC / Computer / Arts / Vocational |
| Academic Year | Current year (auto-set) |
| Initial Sections | Number of sections to create now (1–10) |
| Section naming | A, B, C… / 1, 2, 3… / Custom |
| Max capacity per section | Default: 40 (CBSE norm); editable |

---

## 6. Add Section to Existing Class

- Select class → enter section name → assign class teacher → set capacity
- Assigns the next available letter/number automatically
- Triggers: "New section added: Class IX Section E — roll numbers E001–E040 reserved"

---

## 7. Year Transition Wizard

**[Start Year Transition]** button — runs at academic year close

1. **Confirm class promotions:** Which classes move up (X → XI, XII → alumni)
2. **Stream selection for XI:** Students from X state intended stream choices
3. **Section configuration for new year:** Retain sections / add / remove
4. **Roll number reassignment:** New roll numbers for promoted classes
5. **Class teacher reassignment:** Confirm/change class teachers for next year
6. **Section capacity review:** Reduce capacity if enrolment declines, add sections if increasing

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/classes/` | All classes + sections tree |
| 2 | `POST` | `/api/v1/school/{id}/classes/` | Create class |
| 3 | `GET` | `/api/v1/school/{id}/classes/{class_id}/` | Class detail |
| 4 | `PATCH` | `/api/v1/school/{id}/classes/{class_id}/` | Update class |
| 5 | `POST` | `/api/v1/school/{id}/classes/{class_id}/sections/` | Add section |
| 6 | `GET` | `/api/v1/school/{id}/sections/{section_id}/` | Section detail |
| 7 | `PATCH` | `/api/v1/school/{id}/sections/{section_id}/` | Update section |
| 8 | `POST` | `/api/v1/school/{id}/sections/{section_id}/deactivate/` | Deactivate section |
| 9 | `POST` | `/api/v1/school/{id}/students/{student_id}/move-section/` | Move student between sections |
| 10 | `POST` | `/api/v1/school/{id}/classes/year-transition/` | Initiate year transition wizard |

---

## 9. Business Rules

- Cannot delete a section with enrolled students; must move all students first
- Deactivating a section freezes enrolment but preserves all historical data
- Max sections per class: 12 (platform limit; schools with more contact Platform Admin)
- Class teacher assignment is validated against staff directory — only active staff can be assigned
- Year transition can only be initiated by Principal; requires confirmation with "2025-26 to 2026-27" typed explicitly

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
