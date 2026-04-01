# H-08 — Warden Duty Register

> **URL:** `/school/hostel/duty/`
> **File:** `h-08-warden-duty-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Warden (S3) — submit duty report · Chief Warden (S4) — manage roster · Principal (S6) — review duty register

---

## 1. Purpose

Maintains the warden duty roster and night rounds log. A critical accountability document:
- **Duty roster:** Which warden is responsible for which block on which night
- **Night rounds log:** Physical rounds conducted by warden during the night (typically 10 PM, 12 AM, 3 AM); proof that the warden was present and alert
- **Incident reporting:** Any incidents during duty (fight, student illness, fire alarm, unauthorised absence) logged here
- **CBSE inspection:** The duty register is produced during residential school inspection to demonstrate adequate supervision

---

## 2. Page Layout

### 2.1 Header
```
Warden Duty Register                                 [Duty Roster]  [Submit Night Report]
Date: 27 March 2026 (Wednesday Night)

Tonight's duty:
  Boys' Block A: Mr. Suresh Kumar (Primary Warden)
  Boys' Block B: Mr. Ravi Kumar (Secondary)
  Girls' Block: Ms. Radha (Primary Warden — mandatory female)
  Overnight relief: Mr. Kishore (2 AM–6 AM)
```

### 2.2 Duty Roster
```
March 2026 Duty Roster

Date    Day    Boys Block-A     Boys Block-B    Girls Block        Night Relief
26 Mar  Tue    Mr. Suresh K.    Mr. Ravi K.     Ms. Radha         Mr. Kishore
27 Mar  Wed    Mr. Suresh K.    Mr. Vijay M.    Ms. Radha         Ms. Kavitha
28 Mar  Thu    Mr. Arun S.      Mr. Ravi K.     Ms. Meena         Mr. Kishore
[Weekend] Sat  —Senior Warden on duty—           Ms. Radha (Full)  —

[Edit Roster]  [Auto-generate next month's roster]
```

---

## 3. Night Rounds Log

```
Night Rounds — 27 March 2026 — Boys' Block A

Warden: Mr. Suresh Kumar

Round 1 — 10:00 PM (Lights Out Check):
  All rooms checked: ✅ 27/27 rooms
  Students in rooms: ✅ All accounted (168/168; 5 on approved leave)
  Lights off by: 10:15 PM
  Observations: Room 104 — dormitory students were noisy. Reminded to sleep.
  Digital sign-off: 10:18 PM [Warden signs in app]

Round 2 — 12:30 AM:
  All rooms: ✅ Quiet  ·  No incidents
  Digital sign-off: 12:33 AM

Round 3 — 3:00 AM:
  All rooms: ✅ Quiet
  Room 102: Suresh K. — mild fever; given paracetamol; reported to Matron at 7 AM
  Digital sign-off: 3:07 AM

Relief handoff — 6:00 AM: → Mr. Kishore
  "Uneventful night. Suresh K. (Room 102) has mild fever — Matron aware."
  [Handoff signed by both wardens]
```

---

## 4. Incident Report

```
[Report Incident]

Date & Time: 27 March 2026, 10:45 PM
Block/Location: Boys' Block A, Room 103
Warden on duty: Mr. Suresh Kumar

Incident type:
  ○ Noise/disturbance  ● Student illness  ○ Fight  ○ Unauthorised absence
  ○ Electrical/fire alarm  ○ Visitor (unauthorised)  ○ Other

Description:
  Student Vijay S. (X-B, Room 103) complained of stomach pain at 10:45 PM.
  Warden escorted student to Matron (H-07). Diagnosed as gas pain; given antacid.
  Returned to room by 11:15 PM. No further issues.

Actions taken: ✅ Matron informed  ✅ Parent not disturbed (minor)

[Log Incident]  ← automatically added to duty register for the night
```

---

## 5. Duty Register Export (CBSE Format)

```
WARDEN DUTY REGISTER — GREENFIELDS SCHOOL HOSTEL
March 2026 — Boys' Hostel Block A

Date   Duty Warden     Rounds   Incidents  Sign-off
1 Mar  Mr. Suresh K.   3/3 ✅   None       ✅ 6:00 AM
2 Mar  Mr. Ravi K.     3/3 ✅   None       ✅ 6:00 AM
...
27 Mar Mr. Suresh K.   3/3 ✅   1 (illness)✅ 6:00 AM

Total nights: 27  ·  Rounds missed: 0  ·  Incidents: 3 (minor)

Certified by: Mr. [Chief Warden Name]  ·  Date: 27 Mar 2026
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/duty/roster/?month={m}&year={y}` | Monthly duty roster |
| 2 | `POST` | `/api/v1/school/{id}/hostel/duty/roster/` | Create/update roster |
| 3 | `POST` | `/api/v1/school/{id}/hostel/duty/rounds/` | Submit night rounds log |
| 4 | `POST` | `/api/v1/school/{id}/hostel/duty/incident/` | Report incident |
| 5 | `GET` | `/api/v1/school/{id}/hostel/duty/register/?month={m}&year={y}&block={block}` | Duty register export |

---

## 7. Business Rules

- Night rounds must be logged digitally (timestamped); paper-only logging is not accepted — timestamp provides proof that rounds were actually conducted at the right time
- Three rounds per night are the minimum (10 PM, 12-1 AM, 3 AM); during exam season, a 4th round is added (5:30 AM for morning alarms)
- A warden who misses a round without documented reason (illness, emergency) receives an escalation alert to Chief Warden; 3+ missed rounds in a month triggers a performance review
- Girls' block rounds can only be conducted by female wardens — never by male wardens (MHA guidelines)
- Incidents are categorised: minor (no parent notification needed), moderate (parent notified next morning), major (parent notified immediately and Principal informed)
- The duty register is an official school document; once the Chief Warden signs the monthly register, it is locked and retained for 3 years

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
