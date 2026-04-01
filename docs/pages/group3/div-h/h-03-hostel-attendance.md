# H-03 — Hostel Attendance

> **URL:** `/school/hostel/attendance/`
> **File:** `h-03-hostel-attendance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Warden (S3) — daily roll call for own block · Chief Warden (S4) — school-wide hostel attendance · Principal (S6) — emergency override · Matron (S3) — girls' hostel attendance

---

## 1. Purpose

Hostel attendance is distinct from school attendance (E-01) — it tracks where students are at night, not during school hours. P0 because:
- **Child safety:** Knowing that a boarding student is not in their room at night is a safety emergency
- **Duty of care:** The school is in loco parentis for boarding students 24/7; an unaccounted student triggers a missing child protocol (F-10)
- **Leave tracking:** Cross-references with H-04 (hostel leave/exeat) — if a student is absent from hostel headcount but has approved weekend leave, that's expected; if absent with no leave, it's a crisis
- **Night roll call:** The primary safety check — typically done at 9 PM (after dinner) and again at 10:30 PM (lights out); both must be logged

---

## 2. Page Layout

### 2.1 Header
```
Hostel Attendance                                    [Night Roll Call]  [Morning Check]
Date: 27 March 2026 (Wednesday)

Evening Roll Call (9:00 PM):  ⏳ Not yet taken (due in 2 hours)
  Boys' Block A: 168 students
  Girls' Block B: 112 students

On Leave Tonight (approved H-04):
  Boys: 5 students (weekend leave)
  Girls: 3 students

Expected in hostel tonight:
  Boys: 163  ·  Girls: 109
```

### 2.2 Roll Call Interface
```
Night Roll Call — Boys' Block A — 27 March 2026 — 9:00 PM

Warden: Mr. Suresh Kumar

[Quick Mode: Mark All Present] then mark exceptions

Room 101: Arjun Sharma ✅  ·  Ravi Kumar ✅
Room 102: Suresh K. ✅    ·  [Vacant bed]
Room 103: Vijay S. — 🔴 ABSENT (on leave: ✅ H-04 approved — weekend leave)
          Dinesh P. ✅
Room 104: [6 dormitory students — 6/6 present ✅]
...

Exceptions:
  Present on leave: 5 (Vijay S. and 4 others — approved H-04)
  Unaccounted: 0  ✅

[Submit Roll Call — 9:00 PM]
```

---

## 3. Unaccounted Student Protocol

```
🚨 UNACCOUNTED STUDENT ALERT

Night Roll Call — 28 March 2026 — 9:00 PM

Suresh Kumar (IX-A, Room 102-A) — NOT PRESENT
Leave status: No approved leave for tonight

IMMEDIATE ACTIONS:
  1. ✅ Check all common areas (TV room, study hall, dining room, bathrooms)
     [Mark as Found if located]
  2. ✅ Alert other wardens to check their blocks
  3. ✅ Check with friends/roommate (last seen when/where)

If not found within 10 minutes:
  4. → Alert Principal immediately
  5. → Notify parents: WhatsApp + Phone call
     "URGENT: Your ward Suresh Kumar has not been accounted for in the
      9 PM hostel roll call. We are investigating. Please confirm if he
      is with you. Principal, Greenfields School"
  6. → Review gate log (H-05 visitor register / school gate) — did he leave?

If not found within 30 minutes:
  7. → Police intimation (mandatory for minor missing > 30 min from school premises)
     [Generate Police Report — Juvenile Justice Act / IPC 363]
  8. → F-10 Emergency Alert to all parents (school-wide awareness)

[Suresh Found — Mark Safe]  [Escalate to Principal NOW]  [Call Police]
```

---

## 4. Morning Attendance

```
Morning Check — 28 March 2026 — 6:30 AM

Students present at morning assembly in hostel: 163/163 expected ✅

Students on leave (returning today):
  Vijay S. — weekend leave ended yesterday; expected back by 7 PM Sunday
  [Check if returned: ✅ Returned 6:45 PM Sunday]

Students on extended leave (not expected):
  Chandana Rao — home leave (15 Mar – 30 Mar) — CBSE medical exam leave

[Mark Morning Attendance Submitted]
```

---

## 5. Monthly Hostel Attendance Register

```
Hostel Attendance Register — Boys' Block A — March 2026

Student          Class  1  2  3  ...  25  26  27  28  Total  On Leave
Arjun Sharma     XI-A   P  P  P  ...   P   P   P   P   27/27    0
Vijay S.         X-B    P  P  P  ...   P  WL   P   P   25/27    2(WL)
Suresh K.        IX-A   P  P  P  ...   P   P   P   P   27/27    0

Legend: P=Present  WL=Weekend Leave  HL=Home Leave  S=Sick Room  UA=Unaccounted

[Export Register]  [Print for Warden Sign-off]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/attendance/?block={block}&date={date}` | Roll call status for block |
| 2 | `POST` | `/api/v1/school/{id}/hostel/attendance/roll-call/` | Submit night roll call |
| 3 | `POST` | `/api/v1/school/{id}/hostel/attendance/morning-check/` | Submit morning check |
| 4 | `GET` | `/api/v1/school/{id}/hostel/attendance/unaccounted/?date={date}` | Unaccounted students |
| 5 | `POST` | `/api/v1/school/{id}/hostel/attendance/unaccounted/{student_id}/found/` | Mark student found |
| 6 | `GET` | `/api/v1/school/{id}/hostel/attendance/register/?block={block}&month={m}&year={y}` | Monthly register |

---

## 7. Business Rules

- Night roll call must be completed by 9:30 PM; if not submitted by 10 PM, the system sends an alert to the Chief Warden
- Any unaccounted student (not on approved leave, not found in 10 minutes) immediately triggers parent notification; this is not optional — the warden cannot delay this to "investigate first"
- Roll call data is cross-referenced with H-04 leave register; students on approved leave are auto-marked as "On Leave" and not counted as unaccounted
- Girls' hostel roll call is submitted only by female wardens (Matron/Warden Female); male staff cannot access or submit girls' hostel attendance
- Hostel attendance register is a legal document — once submitted (after Chief Warden sign-off), corrections require Chief Warden approval and are appended as amendments, not overwritten
- During exam season, a 10 PM roll call is added as a second check point

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
