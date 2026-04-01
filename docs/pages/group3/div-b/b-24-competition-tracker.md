# B-24 — Academic Competition Tracker

> **URL:** `/school/academic/competitions/`
> **File:** `b-24-competition-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Academic Coordinator (S4) — full · HOD (S4) — own dept competitions · Subject Teacher (S3) / Class Teacher (S3) — submit student entries · Principal (S6) — full

---

## 1. Purpose

Tracks all academic competitions and olympiads that school students participate in — NTSE, KVPY, Science Olympiad (SOF NSO), Maths Olympiad (SOF IMO), CBSE Science Exhibition, NMMS, Talent Searches, state-level competitions, and school-conducted inter-school events. Indian competitive exam culture is intense — many students in CBSE schools appear for 4–5 olympiads per year. Schools that perform well in these competitions use it as a marketing differentiator ("8 Gold medals in SOF Olympiads"). This page tracks registrations, fee payments, results, and achievements in one place.

---

## 2. Page Layout

### 2.1 Header
```
Academic Competition Tracker                      [+ Register Competition]  [Export Achievement Report]
Academic Year: 2025–26
Registered Competitions: 14  ·  Students Participated: 847  ·  Awards Won: 24
Upcoming: SOF NSO Level 2 — 15 Apr 2026
```

---

## 3. Competition List

| Competition | Conducting Body | Subject | Level | Students Registered | Date | Status | Results | Awards |
|---|---|---|---|---|---|---|---|---|
| NSO 2025 (Science Olympiad) | SOF | Science | National | 284 | 12 Nov 2025 | ✅ Complete | 4 gold, 8 silver | 12 |
| IMO 2025 (Maths Olympiad) | SOF | Maths | National | 210 | 19 Nov 2025 | ✅ Complete | 2 gold, 6 silver | 8 |
| NTSE 2025 | NCERT | All subjects | National | 28 (Class X) | 2 Nov 2025 | ✅ Stage 1 done | 6 qualified for Stage 2 | — |
| CBSE Science Exhibition | CBSE | Science | School → National | 6 teams | 15 Jan 2026 | ✅ School level | 1 team to district | 1 |
| SOF NSO Level 2 | SOF | Science | National | 12 (qualified) | 15 Apr 2026 | ⏳ Upcoming | — | — |
| KVPY 2025 | DST | Science | National | 3 (Class XI) | 3 Nov 2025 | ✅ Complete | 0 qualified | — |
| State Math Talent Test | State Govt | Maths | State | 45 | 20 Feb 2026 | ✅ Complete | 3 state-level awards | 3 |

---

## 4. Competition Detail View

### NSO 2025 — Science Olympiad

```
Organiser: Science Olympiad Foundation (SOF)
Level:     National — school conducts Level 1; top performers go to Level 2
Date:      12 Nov 2025
Fee:       ₹175 per student
Classes:   I–XII (age-appropriate categories)
Total Registered: 284 students

Registration:
  Deadline:     30 Oct 2025 (met ✅)
  Fee Collected: ₹49,700 (from students)
  Paid to SOF:   ₹49,700 via DD  ·  Receipt: SOF/AP/2025/00384

Results:
  Gold Medals:   4 students (Arjun Sharma, Priya V, Rohit K, Anjali D)
  Silver Medals: 8 students
  Bronze Medals: 14 students
  Qualified for Level 2: 12 students (top 10% nationally)

Teacher Coordinator: Ms. Anjali Singh (Science HOD)
```

---

## 5. Student Achievement Record

| Student | Class | Competition | Level | Award | Year |
|---|---|---|---|---|---|
| Arjun Sharma | IX-A | SOF NSO | National Level 1 | Gold Medal | 2025–26 |
| Priya Venkat | IX-A | SOF IMO | National Level 1 | Gold Medal | 2025–26 |
| Rohit Kumar | XI-A | SOF NSO | National Level 1 | Gold Medal | 2025–26 |
| Anjali Das | X-A | NTSE | Stage 1 | Qualified for Stage 2 | 2025–26 |
| Suresh M | XII-A | KVPY | National | Qualified for Interview | 2024–25 |

Student achievements feed into:
- Report card (co-curricular achievements section)
- School annual report / magazine
- Merit certificate generation (Principal's office)
- Student profile (for competitive exam applications)

---

## 6. Register New Competition

[+ Register Competition] → form:

| Field | Value |
|---|---|
| Competition Name | Text |
| Conducting Body | SOF / NCERT / CBSE / State Govt / School / Private |
| Subject Area | Science / Maths / English / All / Other |
| Level | School-level / District / State / National / International |
| Classes Eligible | Multi-select |
| Registration Deadline | Date |
| Exam Date | Date |
| Fee per Student | Amount |
| Registration Mode | Online (portal link) / Offline (DD/cash) |
| Teacher Coordinator | Staff member |
| Notes | Any specific preparation requirements |

---

## 7. CBSE Mandatory Competitions

CBSE mandates schools participate in certain competitions:
- **Science Exhibition (SCE):** Annual; school conducts internal round; best projects go to cluster/district
- **Heritage India Quiz:** CBSE organises; participation encouraged
- **Fit India School Certification:** Physical education + activity based
- **Eco Club activities:** Environmental awareness

These are auto-tracked as "CBSE Mandatory" category. CBSE inspectors check participation records.

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/competitions/?year={year}` | Competition list |
| 2 | `POST` | `/api/v1/school/{id}/competitions/` | Register competition |
| 3 | `GET` | `/api/v1/school/{id}/competitions/{comp_id}/` | Competition detail |
| 4 | `PATCH` | `/api/v1/school/{id}/competitions/{comp_id}/results/` | Update results/awards |
| 5 | `GET` | `/api/v1/school/{id}/competitions/achievements/?student_id={id}` | Student achievements |
| 6 | `GET` | `/api/v1/school/{id}/competitions/export/?year={year}` | Export achievement report |

---

## 9. Business Rules

- Competition fee collection from students is tracked but the financial transaction is managed in the Fee module (div-d) — this page only records whether fee was collected (boolean)
- Awards won are entered manually by the teacher coordinator after results are declared by the competition organiser
- Student achievement records are permanent — they remain visible in the student's profile even after they graduate
- CBSE mandatory competitions (Science Exhibition, etc.) show a compliance flag if the school has not registered for them by a certain date each year

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
