# E-02 — Period-wise Attendance (Subject Teacher)

> **URL:** `/school/attendance/period/{class_id}/{period_id}/`
> **File:** `e-02-period-attendance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Subject Teacher (S3) — own periods only (full) · Class Teacher (S3) — full own class · Academic Coordinator (S4) — read all · Principal (S6) — full

---

## 1. Purpose

Period-wise attendance marking for Subject Teachers. While the Class Teacher marks daily attendance (E-01), many schools — especially for Classes IX–XII — also want subject-wise period attendance to:
- Track students who attend school but bunk specific periods ("proxy" problem)
- Compute subject-wise attendance % (CBSE mandates 75% per subject, not just overall)
- Identify students who attend school but miss their weak subject repeatedly
- Feed data to the HOD for syllabus delivery tracking (was student present when topic was taught?)

Period attendance is typically marked at the start of each period (first 2 minutes). With 8 periods per day and 40 students, the teacher has ~3 seconds per student — so the interface must be extremely fast.

---

## 2. Page Layout

### 2.1 My Today's Periods (Subject Teacher view — dashboard)

When a Subject Teacher logs in, they see:

```
Your Periods — Thursday, 27 March 2026

Period  Time         Class    Subject    Room    Status
P1      8:00–8:45    XI-A     Physics    Lab-1   ✅ Marked (36/38)
P3      9:30–10:15   X-B      Physics    302     ⬜ Mark Now  ← current period
P5      11:00–11:45  XI-B     Physics    Lab-1   ⏳ Upcoming
P7      1:45–2:30    XII-A    Physics    304     ⏳ Upcoming
```

Clicking [Mark Now] → opens the period attendance grid.

---

## 3. Period Attendance Grid

```
XI-A — Physics — Period 3 — 27 March 2026 — 9:30 AM

Roll  Name             Status    [P][A][L]
──────────────────────────────────────────
01    Anjali Das        —        [P][A][L]
02    Arjun Sharma     Absent↓   [P][A][L]  ← pre-marked absent from E-01
03    Bharath Kumar     —        [P][A][L]
...
38    Zara Ahmed        —        [P][A][L]
```

**Pre-populated from E-01:**
- Students marked absent in daily attendance are pre-marked absent (grey row, locked)
- Students marked present in daily attendance are pre-marked present (can be changed to absent if they left or are bunking)
- The teacher only needs to change deviations from the daily status — saves significant time

**Keyboard navigation:** Same as E-01 — Arrow Down, P/A/L keys.

---

## 4. One-tap Confirmation

For periods where no changes from daily attendance:
```
[All Present (matching daily attendance) — Confirm in 1 tap]
→ Marks all present students as present; keeps absent students absent
→ Done in 1 click
```

This is the most common case (90% of periods) — teacher just taps Confirm.

---

## 5. Subject-wise Attendance Accumulation

After each period mark, the system updates the per-student subject-wise attendance:

```
Physics Attendance — Arjun Sharma — 2026–27
Total Physics periods taught: 86
Arjun present for: 72 periods
Subject attendance: 83.7%  ✅ Above 75% CBSE threshold
```

This subject-wise % feeds:
- E-08 Student Attendance Report (shows per-subject breakdown)
- E-09 Shortage Alerts (subject-wise alert if below 75%)
- E-11 Exam Eligibility (subject-wise eligibility check for CBSE)

---

## 6. Proxy Detection

The system compares daily attendance (E-01) vs period attendance (E-02):

```
⚠️ Proxy Alert — 27 March 2026

Rohit Kumar (XI-A):
  Daily attendance (E-01): PRESENT (marked 8:15 AM by Class Teacher)
  Period 3 (Physics): ABSENT (marked 9:30 AM by Physics Teacher)
  Period 4 (Chemistry): ABSENT (marked 10:15 AM by Chemistry Teacher)

Student present at school but absent from 2 periods.
→ Alert sent to: Class Teacher, Academic Coordinator
```

---

## 7. Missed Period Marking

If a teacher forgot to mark a period:
```
⚠️ You have 1 unmarked period from yesterday:
  P5 — Physics — XI-A — 26 March 2026

[Mark Now]  (within 24 hours: no approval needed)
[Request Late Entry] (beyond 24 hours: Class Teacher / Academic Coordinator approval)
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/period/?teacher_id={id}&date={date}` | Teacher's periods for day |
| 2 | `GET` | `/api/v1/school/{id}/attendance/period/{class_id}/{period_id}/?date={date}` | Period attendance grid (pre-populated) |
| 3 | `POST` | `/api/v1/school/{id}/attendance/period/{class_id}/{period_id}/` | Submit period attendance |
| 4 | `GET` | `/api/v1/school/{id}/attendance/period/subject-summary/?student_id={id}&subject_id={id}&year={y}` | Subject-wise attendance for student |
| 5 | `GET` | `/api/v1/school/{id}/attendance/period/proxy-alerts/?date={date}` | Proxy detection alerts |

---

## 9. Business Rules

- A Subject Teacher can only mark attendance for periods where they are the assigned teacher per the timetable (B-06) — system blocks marking for other teachers' periods
- Period attendance is supplementary to daily attendance; daily attendance (E-01) takes precedence for official attendance % computation; period attendance adds subject-wise granularity
- A student already marked absent in E-01 cannot be marked present in E-02 for that day (they weren't in school); the reverse is possible (present in school but absent from a specific period)
- Period attendance data is retained for 3 years for academic review; used in HOD's B-01 dashboard for subject delivery tracking

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
