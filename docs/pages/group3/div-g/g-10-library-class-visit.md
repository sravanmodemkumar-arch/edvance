# G-10 — Library Class Visit

> **URL:** `/school/library/class-visits/`
> **File:** `g-10-library-class-visit.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Librarian (S3) — schedule and manage · Class Teacher (S3) — book visit and supervise · Academic Coordinator (S4) — oversee scheduling

---

## 1. Purpose

Schedules and tracks structured class library visits — time when an entire class comes to the library as part of the timetable (A-13 Timetable integration). CBSE's Reading Culture initiative and NEP 2020 encourage dedicated library periods. This ensures equitable access — not just self-motivated students visit the library, but every class has a structured library engagement.

---

## 2. Page Layout

### 2.1 Header
```
Library Class Visits                                 [Schedule Visit]  [View Timetable]
Academic Year: [2026–27 ▼]   Month: [March 2026 ▼]

Visits scheduled this month: 22  ·  Completed: 18  ·  Upcoming: 4
Students who visited library this month: 312/380 (82%)
```

### 2.2 Visit Schedule
```
Date         Class    Time         Teacher       Librarian  Students  Books Issued  Status
27 Mar 2026  XI-A     10:00-10:45  Ms. Anita     Ms. Kavitha  45       32           🟢 In Progress
26 Mar 2026  IX-B     11:00-11:45  Mr. Ravi      Ms. Kavitha  38       30           ✅ Completed
25 Mar 2026  VI-A     9:00-9:45    Ms. Radha     Ms. Kavitha  34       28           ✅ Completed
```

---

## 3. Schedule Visit

```
[Schedule Visit]

Class: [XI-A ▼]  ·  Teacher: [Ms. Anita Reddy ▼]
Date: [27 March 2026]  ·  Time: [10:00 AM] to [10:45 AM]
Library capacity check: 45 students — Library capacity: 60 ✅

Activity type:
  ● Free reading + issue (students browse and borrow)
  ○ Reading programme session (G-11 — structured reading activity)
  ○ Project research (students use reference section for a specific project)
  ○ Digital library introduction (G-09 — first time using DIKSHA etc.)

Librarian assigned: [Ms. Kavitha ▼]

[Schedule Visit]
```

---

## 4. During Visit — Librarian View

```
Class Visit In Progress — XI-A — 27 Mar 2026 (10:00 AM)

45 students present  ·  Teacher: Ms. Anita

Quick issue mode: [BATCH ISSUE MODE — ON] (G-03 batch feature)
  → Students approach counter → scan card → scan book → next

Running tally:
  Books issued so far: 32  ·  Students who haven't issued yet: 13
  Time remaining: 12 minutes

Reference books used in-library (not issued):
  [Log in-library usage] (for statistics — which reference books are read but not borrowed)

[End Visit]  [Extend by 10 minutes]
```

---

## 5. Visit Analytics

```
Class XI-A — Library Visit History 2026-27

Month      Date       Duration  Books Issued  Reading Activity
April       15 Apr      45 min      35/45       Free reading
May         20 May      45 min      38/45       Free reading
...
March       27 Mar      45 min      32/45       Free reading

Avg issue rate: 33/45 (73%)
Most popular genres this class: Fiction (45%), Science (32%), Biographies (23%)
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/class-visits/?month={m}&year={y}` | Visit schedule |
| 2 | `POST` | `/api/v1/school/{id}/library/class-visits/` | Schedule visit |
| 3 | `PATCH` | `/api/v1/school/{id}/library/class-visits/{visit_id}/complete/` | Mark visit complete |
| 4 | `GET` | `/api/v1/school/{id}/library/class-visits/analytics/?year={y}` | Visit analytics |

---

## 7. Business Rules

- Library class visits are logged in E-14 (Event/Activity Attendance) when they are timetabled as a class period; they are also logged here for library-specific tracking
- Each class should visit the library at least once per month per the Reading Culture recommendation; the system flags classes that haven't visited in 6 weeks
- During a class visit, the batch issue mode in G-03 allows rapid processing — the librarian can process 40 students in 20 minutes with barcode scanning
- Reference section usage during class visits is optionally logged for collection usage statistics

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
