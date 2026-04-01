# B-25 — Co-Curricular Activity Register

> **URL:** `/school/academic/cca/`
> **File:** `b-25-cca-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Academic Coordinator (S4) — full · Class Teacher (S3) — submit events · Subject Teacher (S3) — submit events · Principal (S6) — full

---

## 1. Purpose

Maintains the register of all co-curricular activities (CCAs) — sports events, cultural programmes, debates, quiz competitions, literary events, science fairs, annual day performances, and community service activities. CBSE's CCE (Continuous and Comprehensive Evaluation) framework includes co-scholastic activities as a graded component (displayed on report cards for Classes VI–X). Schools also need CCA records for CBSE annual inspection, for student application portfolios (CUET/college admissions), and for school annual reports. NEP 2020 emphasises co-curricular activities as integral to education, not extras.

---

## 2. Page Layout

### 2.1 Header
```
Co-Curricular Activity Register                   [+ Add Activity]  [Export Annual Report]
Academic Year: 2025–26
Activities Recorded: 68  ·  Student Participations: 2,840  ·  External Events: 12
Awards / Recognitions: 34
```

---

## 3. Activity Categories

| Category | Subcategories |
|---|---|
| Literary | Debate, Essay, Poem recitation, Elocution, Story writing, Quiz |
| Cultural | Dance (classical/folk/western), Drama, Skit, Music (vocal/instrumental) |
| Sports | Athletics, Cricket, Football, Badminton, Kho-Kho, Kabaddi, Carrom, Chess |
| Creative | Drawing, Painting, Craft, Photography, Model making |
| Science & Technology | Science fair, Robotics, STEM activity, Innovation project |
| Community Service | NSS, Blood donation camp, Cleanliness drive, Tree plantation |
| Leadership | Student Council, Event management, House activities |
| CBSE Mandatory | Science Exhibition, Heritage Quiz, Fit India, Eco Club |

---

## 4. Activity List

| # | Activity Name | Category | Date(s) | Organiser | Level | Participants | Awards | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Annual Day 2026 | Cultural | 28 Feb 2026 | Admin | School | 186 students | Best performance: Class XI-A | ✅ Done |
| 2 | Inter-House Debate | Literary | 5 Jan 2026 | Academic Coord | School | 40 students | Winner: Tagore House | ✅ Done |
| 3 | Sports Day 2026 | Sports | 15 Jan 2026 | PT Dept | School | 620 students | Overall: Gandhi House | ✅ Done |
| 4 | Science Exhibition | Science | 2 Feb 2026 | Science HOD | School → District | 12 teams | 1 team to district | ✅ Done |
| 5 | Republic Day Programme | Cultural | 26 Jan 2026 | Admin | School | 80 students | — | ✅ Done |
| 6 | Earth Day | Community | 22 Apr 2026 | Eco Club | School | All | — | ⏳ Upcoming |
| 7 | NSS Camp | Community | May 2026 | NSS Teacher | State | 35 students | — | ⏳ Upcoming |

---

## 5. Activity Detail View

### Annual Day 2026

```
Activity: Annual Day 2026
Category: Cultural  ·  Level: School
Date: 28 Feb 2026  ·  Duration: Full day (9 AM – 6 PM)
Organiser: Administrative Officer Ms. Kavitha
Venue: School Auditorium

Student Participants:
  Performance items: 24 (dance, drama, music)
  Total performers: 186 students
  Technical crew: 12 students
  Backstage crew: 18 students

Chief Guest: District Collector Ms. Priya Mehta
Attendees: 800+ (students, parents, staff, guests)

Awards:
  Best Performance: Class XI-A (Western Dance)
  Best New Talent: Arjun Sharma (XI-A) — Violin recital

Photo Gallery: [View 120 photos]  (uploaded by photography club)

Teacher Coordinators:
  Overall: Ms. Kavitha (Admin Officer)
  Cultural: Ms. Suma (English HOD)
  Technical: Mr. Dinesh (CS Teacher)

CBSE Report Tag: Annual Day — Cultural & Co-scholastic activity (CBSE CCE record)
```

---

## 6. Student CCA Portfolio

For each student, their CCA participations are logged:

| Student: Arjun Sharma — Class XI-A |
|---|
| Annual Day 2026 — Violin Recital — School level — Best New Talent Award |
| Sports Day 2026 — 100m Sprint — School level — 2nd place |
| Inter-House Debate — Literary — School level — Participant |
| SOF NSO 2025 — Science Olympiad — National — Gold Medal |
| Science Exhibition 2026 — Science fair — School level — Best Project (district qualifier) |

CCA portfolio exported for:
- CBSE co-scholastic report card grades
- College admission portfolios (CUET, class XI admission forms)
- School leaving certificate (TC) — activities mentioned

---

## 7. CBSE Co-Scholastic Grading

For Classes VI–X, CBSE requires annual co-scholastic grades on report cards (A+/A/B/C):

| Student | Work Education | Art Education | Health & PE | Discipline | Sports Participation | Overall CCA Grade |
|---|---|---|---|---|---|---|
| Arjun Sharma | A | A+ | A+ | A | ✅ Active | A+ |
| Priya V | A+ | A+ | A | A | ✅ Active | A+ |
| Rahul G | B | A | B | B | ⬜ Minimal | B |

Grades feed from:
- Work Education: Class teacher assessment
- Art: Art teacher assessment
- Health/PE: PT teacher assessment
- Discipline: Class teacher
- Sports: Participation in sports events (tracked here in B-25)

Academic Coordinator can see school-wide summary to check if grades are entered for all classes before report card generation.

---

## 8. Inter-House System

Many Indian schools use the "House System" (4 houses named after national leaders/values):

| House | Colour | House Teacher | Points This Year |
|---|---|---|---|
| Gandhi House | Green | Mr. Ramesh | 845 |
| Nehru House | Blue | Ms. Leela | 820 |
| Tagore House | Yellow | Mr. Bala | 890 |
| Sarojini House | Red | Ms. Anjali | 775 |

House points accumulated from:
- Sports events
- Literary events (debate, quiz)
- Cultural events
- Academic competitions
- Good citizenship/service

Annual prize-giving ceremony at Annual Day — [Export House Points Tally]

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/cca/?year={year}` | Activity list |
| 2 | `POST` | `/api/v1/school/{id}/cca/` | Add activity |
| 3 | `GET` | `/api/v1/school/{id}/cca/{activity_id}/` | Activity detail |
| 4 | `PATCH` | `/api/v1/school/{id}/cca/{activity_id}/` | Update activity |
| 5 | `GET` | `/api/v1/school/{id}/cca/student/{student_id}/portfolio/` | Student CCA portfolio |
| 6 | `GET` | `/api/v1/school/{id}/cca/co-scholastic/?class_id={id}` | Co-scholastic grades for class |
| 7 | `PATCH` | `/api/v1/school/{id}/cca/co-scholastic/{student_id}/` | Update co-scholastic grades |
| 8 | `GET` | `/api/v1/school/{id}/cca/houses/points/` | House points tally |
| 9 | `GET` | `/api/v1/school/{id}/cca/export/?year={year}` | Annual CCA report PDF |

---

## 10. Business Rules

- Co-scholastic grades (for CBSE report cards) must be entered before B-19 (Report Card Generator) can produce CBSE-compliant report cards for Classes VI–X
- Activity records are permanent — they form part of the student's academic history
- CBSE mandatory activities (Science Exhibition, Fit India, Heritage Quiz) that have not been recorded by December generate a compliance warning in A-29 (Compliance Dashboard)
- House points are advisory (no formal grading); schools use them for inter-house annual championship

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
