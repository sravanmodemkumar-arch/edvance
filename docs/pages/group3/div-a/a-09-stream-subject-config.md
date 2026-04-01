# A-09 — Stream & Subject Configuration

> **URL:** `/school/admin/streams/`
> **File:** `a-09-stream-subject-config.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full · VP Academic (S5) — full · HOD (S4) — view own department

---

## 1. Purpose

Configures which subjects are offered in which streams and classes, maps subjects to departments, sets periods-per-week per subject per class, and defines subject combinations available at XI–XII level. This configuration drives the timetable builder (div-b), question bank subject selection, and exam paper subject options.

**Indian education streams (XI–XII):**
- **MPC** — Mathematics, Physics, Chemistry (standard science-engineering track)
- **BiPC** — Biology, Physics, Chemistry (standard science-medical/NEET track)
- **MPC + Biology** — Combined (for both JEE/NEET aspirants; some schools offer this)
- **MEC** — Mathematics, Economics, Commerce (business analytics track)
- **CEC** — Commerce, Economics, Civics (commerce track)
- **HEC** — History, Economics, Civics (humanities/arts track)
- **Computer Science** combinations — CS replaces one science in MPC/BiPC
- **Vocational** streams — per NEP 2020 (Retail, IT, Healthcare, Agriculture, etc.)

---

## 2. Page Layout

### 2.1 Tab Bar
```
[Subject Master] [Stream Configuration] [Subject-Class Mapping] [Periods per Week]
```

---

## 3. Tab: Subject Master

Defines all subjects offered in the school. Global list — used by all classes/streams.

**Subject table:**
| Subject | Code | Department | Type | Board Prescribed | Active |
|---|---|---|---|---|---|
| Mathematics | MATH | Mathematics Dept | Compulsory | Yes | ✅ |
| Physics | PHY | Science Dept | Elective (XI–XII) | Yes | ✅ |
| Telugu | TEL | Language Dept | Compulsory (I–X) | Yes | ✅ |
| Computer Science | CS | IT Dept | Elective (IX–XII) | Yes | ✅ |
| Yoga & Physical Education | YPE | Sports Dept | Compulsory | Yes | ✅ |
| Financial Markets (Vocational) | FM-VOC | Commerce Dept | Vocational | Yes | ✅ |

**Subject Types:**
- Compulsory (all students must take)
- Elective (student chooses from list)
- Activity / Co-scholastic (not graded, e.g., Art, Music, NCC)
- Vocational (NEP 2020 vocational subjects)
- Additional subject (e.g., 3rd language)

**[+ Add Subject]** → form: name, code, department, type, board-prescribed toggle, active toggle

---

## 4. Tab: Stream Configuration (XI–XII focus)

**Per-stream subject combinations:**

| Stream | Code | Core Subjects | Optional |
|---|---|---|---|
| MPC | MPC | Maths · Physics · Chemistry | + Computer Science or Botany |
| BiPC | BIPC | Biology · Physics · Chemistry | + Maths (optional) |
| MEC | MEC | Maths · Economics · Commerce | + Computer Applications |
| CEC | CEC | Commerce · Economics · Civics | + Business Studies |
| HEC | HEC | History · Economics · Civics | + Political Science |
| Computer Science | CS-MPC | Maths · Physics · Computer Science | + Chemistry |
| Vocational-IT | VOC-IT | IT, ITES · Maths · English | + any 1 core subject |

**Additional subjects available in all streams (max 1):**
- Fine Arts / Painting
- Music (Vocal / Instrumental)
- Dance / Physical Education (as board subject, not activity)
- NCC credit (some state boards accept NCC as scoring subject)

---

## 5. Tab: Subject-Class Mapping

Grid view: Subjects on Y-axis, Classes on X-axis. Checkmark per cell = this subject is taught in this class.

- Filter by department/stream
- Click any cell → opens drawer to set teacher assignment + periods/week for that combination
- Bulk assign: select multiple cells → assign teacher + periods

---

## 6. Tab: Periods per Week

**Per class, per subject — how many periods per week:**

Table: Class (row) × Subject (column) — periods per week value in each cell.

Default values loaded from CBSE/state board prescribed norms:
- Class I–V: 40 periods/week (8 periods/day × 5 days); subjects split per board recommendations
- Class VI–X: 45 periods/week (9 periods/day)
- Class XI–XII: 42 periods/week; core subjects 6 periods/week; electives 5; languages 4

[Import Board Standard] button — pre-fills from board-prescribed norms.

**Total validation:** Sum of all subject periods must equal total available periods per week. If overrun → red alert "Total periods exceed 45/week for Class IX A."

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/subjects/` | All subjects |
| 2 | `POST` | `/api/v1/school/{id}/subjects/` | Add subject |
| 3 | `PATCH` | `/api/v1/school/{id}/subjects/{subj_id}/` | Update subject |
| 4 | `GET` | `/api/v1/school/{id}/streams/` | Stream configurations |
| 5 | `POST` | `/api/v1/school/{id}/streams/` | Add stream |
| 6 | `PATCH` | `/api/v1/school/{id}/streams/{stream_id}/` | Update stream |
| 7 | `GET` | `/api/v1/school/{id}/class-subject-map/` | Subject-class mapping grid |
| 8 | `POST` | `/api/v1/school/{id}/class-subject-map/` | Assign subject to class |
| 9 | `GET` | `/api/v1/school/{id}/periods-config/` | Periods per week configuration |
| 10 | `PATCH` | `/api/v1/school/{id}/periods-config/` | Update periods per week |
| 11 | `POST` | `/api/v1/school/{id}/periods-config/import-board-standard/` | Import board norms |

---

## 8. Business Rules

- Changing a subject's department affects all existing teacher assignments — warn before save
- Removing a subject from a class-stream combination that has existing exam records → blocked (historical data protection)
- Periods per week total validation is a soft warning, not a hard block (some schools legitimately exceed standard norms with special schedules)
- Vocational subjects can only be added to XI–XII streams (NEP 2020 restriction)
- Board-prescribed subject names and codes used in all official documents; custom names for internal use only

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
