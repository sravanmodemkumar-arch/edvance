# I-05 — Bus Attendance

> **URL:** `/school/transport/attendance/`
> **File:** `i-05-bus-attendance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Female Escort (S2) — submit attendance on bus · Transport In-Charge (S3) — view and alerts · Class Teacher (S3) — cross-reference · Administrative Officer (S3) — generate reports

---

## 1. Purpose

Records which students board and alight the school bus each day. Separate from classroom attendance (E-01) — bus attendance is a safety record. Critical use cases:
- **A student boards the bus but doesn't arrive at school** — missing child alert
- **School sends student home early but bus has already departed** — escort must know
- **Absent student's parent calls asking if child is on the bus** — escort has real-time list
- **Accident** — insurance claim requires evidence of who was on the bus
- **Cross-reference with E-01:** A student absent in school (E-01) but their parent says they sent them on the bus — discrepancy = immediate follow-up

---

## 2. Page Layout

### 2.1 Header
```
Bus Attendance                                       [Morning Summary]  [Evening Status]
Date: 27 March 2026 (Wednesday)

Morning route (to school):
  Route R01: 44 enrolled → 42 boarded ✅ (2 absent — parent informed for both)
  Route R02: 38 enrolled → 36 boarded ✅
  Route R04: 54 enrolled → 51 boarded ✅

Evening route (from school):
  Routes: All pending (school ends 4:00 PM)
```

### 2.2 Morning Attendance (Escort App View)

The female escort takes attendance on the bus using a phone/tablet:

```
Route R01 — Morning — 27 Mar 2026

Bus: AP29AB1234  ·  Driver: Raju Kumar  ·  Escort: Ms. Kavitha
Departed school stop: 6:45 AM

Stop 1 — Paradise Circle (6:45 AM):
  ● Rohit P. — ✅ Boarded
  ● Sita R. — ✅ Boarded
  ● Meena V. — ⬜ NOT at stop  → [Call parent]  → Parent says "sick today"
  [Log as absent — parent confirmed]

Stop 2 — Chaitanyapuri X-Roads (6:50 AM):
  ● 12 students → [Mark All Present]
  ● Exception: Arjun S. — ⬜ NOT at stop → [Call parent] → "Slight delay, please wait 2 min"
  [Wait logged — 2 min delay]  [Arjun boarded 6:52 AM]

...

Bus reached school: 7:22 AM
Total boarded: 42/44
2 absent: Meena V. (sick — parent confirmed), Vijay S. (absent — parent not reached)

⚠️ Vijay S. — parent not reached → [Alert Transport In-Charge + Class Teacher]
```

---

## 3. Cross-Reference with School Attendance (E-01)

After morning routes complete:

```
Cross-Reference Report — 27 March 2026 — Morning

Discrepancies:

Student: Vijay S. (X-B, Route R04)
  Bus attendance: NOT boarded (stop: Vanasthalipuram)
  School attendance (E-01): Marked PRESENT by class teacher
  ⚠️ DISCREPANCY — Student shows up in school but didn't board the bus
  Possible: Parent dropped personally, or borrowed another's bus slip
  Action: Confirm with Class Teacher / student

Student: Rohit M. (VIII-A, Route R02)
  Bus attendance: Boarded
  School attendance (E-01): Marked ABSENT
  ⚠️ DISCREPANCY — Student was on the bus but not in class
  Possible: Left school premises after arriving?
  Action: IMMEDIATE ALERT → Class Teacher + Admin Officer + Principal
  [This matches a missing-from-class scenario — escalate now]
```

---

## 4. Evening Attendance

```
Evening Route R01 — 27 March 2026 — 4:10 PM

School gate attendance (confirmed by school gate):
  All 42 students boarded ✅ (42 were at school today — 2 absent went home by other means)

[Mark Evening Attendance] → Escort marks all present at each stop drop

All drops completed: 4:58 PM
Last student dropped: Arjun Sharma (Paradise Circle)
Escort confirmation: ✅ "All students safely dropped. Route completed."

[Submit Evening Report]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/transport/attendance/?route={route_id}&date={date}` | Route attendance for date |
| 2 | `POST` | `/api/v1/school/{id}/transport/attendance/morning/` | Submit morning bus attendance |
| 3 | `POST` | `/api/v1/school/{id}/transport/attendance/evening/` | Submit evening drop attendance |
| 4 | `GET` | `/api/v1/school/{id}/transport/attendance/cross-reference/?date={date}` | School vs bus discrepancies |
| 5 | `GET` | `/api/v1/school/{id}/transport/attendance/student/{student_id}/?month={m}` | Student bus attendance history |

---

## 6. Business Rules

- Bus attendance is submitted by the female escort using the escort's mobile app; the driver cannot submit attendance (driving while using phone is illegal; also a separation of duties)
- Discrepancy between bus attendance and school attendance (E-01) is flagged automatically; a "student on bus but absent in class" discrepancy triggers an immediate alert to the Principal — this is a potential missing child situation
- Bus attendance records are retained for 3 years; accident/incident records indefinitely
- If a student does not board the bus at their stop and the parent hasn't called: the escort calls the parent immediately; if unreachable, the Transport In-Charge is alerted; if still unresolved after 15 minutes, the Principal is informed
- Evening: no student is dropped at an unattended stop (if the parent/guardian is not there to receive them); the student is brought back to school and the parent is called

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
