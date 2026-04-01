# E-14 — Event / Activity Attendance

> **URL:** `/school/attendance/events/`
> **File:** `e-14-event-activity-attendance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Activity Teacher / Event Coordinator (S3) — manage own events · Physical Education Teacher (S3) — sports events · Class Teacher (S3) — school trips/class events · Academic Coordinator (S4) — full · Administrative Officer (S3) — field trip permission slips · Principal (S6) — approval for external events

---

## 1. Purpose

Tracks attendance for events, activities, and programmes that are outside the normal classroom schedule:
- **School annual functions / sports days / science fairs** — students attending vs not attending
- **Field trips / educational tours** — mandatory attendance for safety/insurance
- **Sports practice sessions** — for sports certificate and on-duty consideration
- **Extra-curricular activity sessions** (NSS/NCC/Scouts/clubs) — separate attendance from class
- **Inter-school competitions** — students who are out for competition (on-duty status)
- **Parent-Teacher Meetings** — teacher side (which teachers were present)

This is distinct from E-01 daily attendance (which records school presence) and E-02 period attendance (which records subject periods). Events are optional or parallel school activities.

---

## 2. Page Layout

### 2.1 Header
```
Event / Activity Attendance                         [+ New Event]  [Export]
Academic Year: [2026–27 ▼]

Upcoming Events: 3  ·  Active (Today): 1  ·  Completed This Month: 8
```

### 2.2 Events List
```
Filter: [All Events ▼]  Type: [All Types ▼]  [Search]

Type          Event Name                    Date(s)       Organiser        Attendance  Status
🏆 Sports     Inter-School Cricket Tourney  27–28 Mar 26  Mr. Suresh       14/14       Active
🎭 Cultural   Annual Day Rehearsal          24 Mar 2026   Ms. Anita        42/45       Completed
🔬 Academic   Science Exhibition            22 Mar 2026   Mr. Arun         89/94       Completed
🚌 Field Trip Nehru Science Centre Visit   18 Mar 2026   Ms. Kavya        38/40       Completed
📋 NSS        NSS Camp — Day 1–3            10–12 Mar 26  Mr. Vijay       22/22       Completed
🎓 PTM        Parent–Teacher Meeting        8 Mar 2026    Admin            —/—         Completed
```

---

## 3. New Event Creation

```
[+ New Event] → drawer:

Event Details
─────────────
Event Name:    [Inter-School Cricket Tournament              ]
Event Type:    [Sports ▼]   (Sports / Cultural / Academic / Field Trip / NSS / NCC /
                              Scouts / Club / PTM / Other)
Date(s):       [27 Mar 2026] to [28 Mar 2026]   (single day or range)
Venue:         [District Sports Complex, Vijayawada          ]
External Venue: ☑ Yes (outside school premises)

Organiser/In-charge: [Mr. Suresh Kumar — PE Teacher ▼]
Co-ordinators:       [Add more staff ▼]

Participant Scope:
  ● Specific students (add by name/roll)
  ○ Entire class(es)
  ○ Entire school
  ○ Selected activity group

Participants:        [+ Add Students]  (autocomplete search)
  Selected: 14 students (from Classes IX–XII, Cricket team)

Permission slip required: ☑ Yes (for field trips / external venues)
  → Parent acknowledgement required before student can participate
  → [Generate Permission Slip PDF]

On-Duty status: ☑ Grant on-duty to participants
  → Effect: These students' absence from class during event period
    will be marked as On-Duty in E-01/E-02 (excluded from denominator)
  → Academic Coordinator approval required for on-duty grant

[Save Event]  [Save & Start Attendance]
```

---

## 4. Taking Attendance for an Event

```
[Take Attendance] → Event attendance screen:

Inter-School Cricket Tournament — Day 1 (27 Mar 2026)
Venue: District Sports Complex  ·  Organiser: Mr. Suresh Kumar

Participants: 14 students

Mode: ● Mark present/absent  ○ QR check-in scan

Roll  Name              Class  Permission  Status
01    Ravi Kumar         XI-A  ✅ Signed   [Present ▼]  ← default
02    Sanjay M.          X-B   ✅ Signed   [Present ▼]
03    Dinesh P.          XI-B  ✅ Signed   [Absent   ▼]  ← override
04    Priya Venkat       XI-A  ✅ Signed   [Present ▼]
...

QR Check-In Mode:
  → Scan student ID QR code (from C-15 student ID card)
  → Student auto-marked Present + timestamp logged
  → Use for large events (sports day, annual function) where
    manual roll call is impractical

[Save Attendance]  [Mark All Present]
```

---

## 5. Field Trip Specific Workflow

Field trips have additional safety requirements:

```
Field Trip — Nehru Science Centre Visit (18 Mar 2026)
Class: VII-A, VII-B   Students: 40   Staff: 4

Pre-trip checklist:
  ☑ Permission slips received: 38/40
  ⚠️ 2 students (Kavya P., Amit R.) — permission slip pending
     → Cannot board bus without signed slip
     → [Send reminder to parents]

  ☑ Medical info reviewed (C-18 health records of travelling students)
  ☑ Emergency contact numbers printed (carried by teacher)
  ☑ First-aid kit assigned
  ☑ Bus route confirmed

Attendance — Departure (8:30 AM):
  Students on bus: 38/40  (2 stayed back — no permission slip)
  Staff on bus: 4/4

Attendance — Return (4:30 PM):
  Students returned: 38/38  ✅ Headcount complete
  Any incidents: [Log Incident]

Safe return confirmed: ✅  Time: 4:42 PM  Logged by: Ms. Kavya
```

---

## 6. On-Duty Propagation

When an event grants on-duty status:

```
On-Duty Status Update — Cricket Tournament (27–28 Mar 2026)

The following 14 students have been marked On-Duty for:
  27 Mar 2026 (full day)
  28 Mar 2026 (full day)

Effect in E-01 Daily Attendance:
  → These students will show as OD (On-duty) instead of Absent
  → OD days excluded from attendance denominator

Effect in E-02 Period Attendance:
  → Periods during these dates marked OD for these students
  → Subject-wise attendance not penalised

Academic Coordinator Approval: ✅ Approved by [Name] on 25 Mar 2026

[View affected E-01 records]  [View E-11 eligibility impact]
```

---

## 7. NSS / NCC / Scouts — Session Attendance

These activity groups have recurring sessions tracked separately:

```
NSS Unit 42 — Session Attendance
In-charge: Mr. Vijay Kumar  ·  Academic Year: 2026–27

Session log:
Date        Day  Session Type        Location      Present  Total
10 Mar 2026  Tue  Regular meeting     School Hall     20      22
17 Mar 2026  Tue  Community service   Village Rampur  22      22
10–12 Mar    —    NSS Camp            District HQ     22      22
Total hours: 12 regular sessions + 3-day camp = approx 45 hours

NSS Certificate eligibility (240 hours required):
Ramesh V.:  186/240 hours  ⚠️ Below threshold
Sita D.:    248/240 hours  ✅ Eligible for NSS certificate
```

---

## 8. Annual Day / Sports Day — Mass Attendance

For school-wide events with 500+ students:

```
Annual Day 2026 — Attendance (Mass Mode)

Date: 22 Feb 2026   Venue: School Auditorium   Expected: 520 students

Attendance Mode: Class-wise bulk mark
  → Class teachers mark present/absent list for own class
  → No individual QR scanning needed for in-school event

Summary (after all classes submitted):
Class     Expected  Present  Absent  % Present
Nursery-A    25       25       0      100%
Nursery-B    24       23       1       96%
...
Class XII    35       33       2       94%

Total: 498/520 = 95.8% school attendance

Students absent: 22 (absentees noted by class teachers)
Reason (most): Family functions (annual day falls on working day)
```

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/events/?year={y}&type={type}` | Events list |
| 2 | `POST` | `/api/v1/school/{id}/attendance/events/` | Create event |
| 3 | `GET` | `/api/v1/school/{id}/attendance/events/{event_id}/` | Event detail |
| 4 | `POST` | `/api/v1/school/{id}/attendance/events/{event_id}/attendance/` | Submit event attendance |
| 5 | `GET` | `/api/v1/school/{id}/attendance/events/{event_id}/attendance/` | Event attendance summary |
| 6 | `POST` | `/api/v1/school/{id}/attendance/events/{event_id}/on-duty-grant/` | Grant on-duty to participants |
| 7 | `GET` | `/api/v1/school/{id}/attendance/events/activity-groups/?year={y}` | NSS/NCC/Scouts session logs |
| 8 | `GET` | `/api/v1/school/{id}/attendance/events/field-trip/{event_id}/checklist/` | Field trip safety checklist |
| 9 | `GET` | `/api/v1/school/{id}/attendance/events/{event_id}/permission-slip-pdf/` | Permission slip PDF |

---

## 10. Business Rules

- On-duty status for events requires Academic Coordinator approval; it is not auto-granted when an event is created
- Field trips to external venues require permission slips for every student; a student without a signed slip cannot be marked present for departure (safety/liability requirement)
- NSS participation is tracked separately from school attendance — NSS certificate requires 240 hours of verified service; EduForge tracks session hours but certificate is issued by NSS Programme Officer (school nodal officer), not the school directly
- Event attendance does not affect E-01 daily attendance counts unless on-duty is explicitly granted
- For inter-school competitions, on-duty status automatically flows from E-14 to E-01/E-02 for the duration of the competition
- PTM attendance (teacher side) is tracked here to ensure all class teachers attended; missed PTM is noted in staff report (L module)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
