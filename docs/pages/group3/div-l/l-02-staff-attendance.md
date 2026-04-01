# L-02 — Staff Attendance

> **URL:** `/school/hr/attendance/`
> **File:** `l-02-staff-attendance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HR Officer (S4) — full access · Principal (S6) — view and approve · Vice Principal (S5) — take attendance/view · Class Teacher (S3) — view own attendance only · Administrative Officer (S3) — view

---

## 1. Purpose

Tracks daily attendance of all staff. Staff attendance has multiple uses:
- **Payroll:** Leave deductions, LOP (Loss Of Pay) for unauthorised absences
- **CBSE inspection:** Staff attendance register is reviewed; absent without sanction is a finding
- **Timetable:** If a teacher is absent, L-13 (substitute management) is triggered
- **Patterns:** Chronic Monday/Friday absences, excessive sick leave, performance concerns
- **DEO inspection:** Government inspectors check teacher attendance in government-aided schools; for private schools, CBSE inspectors check

---

## 2. Page Layout

### 2.1 Daily Attendance

```
Staff Attendance — 27 March 2026 (Friday)               [Mark Attendance]
Taken by: Vice Principal at 8:05 AM

Teaching Staff (45):
  Present: 43  ·  Absent (approved leave): 1  ·  Absent (unexplained): 1

  Status:  ✅ Present: 43 teachers
           🌴 On approved leave: Ms. Priya Iyer (EL — 1 day)
           ❓ Absent without intimation: Mr. Vijay P. — [Call and follow up]

Non-Teaching Staff (22):
  Present: 21  ·  Absent: 1 (approved leave)

Transport Staff (11):
  All present ✅ (Driver/escort attendance is taken by Transport In-Charge at 6:30 AM)

[Submit attendance — 8:05 AM]
```

### 2.2 Monthly Summary

```
Staff Attendance Summary — March 2026

Working days in March: 23

                   Present Days  Leave Days  LOP Days  Attendance %
Teaching (45 staff):
  Average:          21.8          1.0         0.2       95.0%
  Highest absentee: Mr. Vijay P. — 5 days absent (3 SL + 2 LOP) ⚠️
  Perfect attendance: 28 teachers ✅

Non-Teaching:
  Average: 22.2 / 23 = 96.5%

Late arrivals (after 8:15 AM):
  5 instances (4 different staff)
  Threshold: 3 late arrivals/month = half-day deduction on 4th (school policy)
```

---

## 3. Biometric / Digital Check-In

```
Attendance Method — GREENFIELDS SCHOOL

Method: ● Biometric (fingerprint — at school gate) + EduForge sync
        ○ Manual (taken by VP)
        ○ Hybrid (biometric + VP override)

Biometric device: Suprema BioStation L2 (at main staff entrance)
EduForge integration: Device pushes attendance events via API at each punch

Attendance rules:
  Before 8:10 AM: Marked "On Time"
  8:10 AM – 8:30 AM: Marked "Late"
  After 8:30 AM: Requires VP/Principal sanction; otherwise LOP

Leave request submitted before: Absent but approved
Absent without leave request: Marked LOP after 2 days (school gives 2 days grace period
  for emergency situations; if no leave application after 2 days, it becomes LOP automatically)

Remote attendance (for rare work from home — non-applicable for teachers):
  N/A for teaching staff (physical presence mandatory for classroom teaching)
  Only applicable for Administrative Officer on approved WFH days
```

---

## 4. Attendance Pattern Alerts

```
Attendance Patterns — March 2026

⚠️ Mr. Vijay P. (Class V Teacher):
  5 absences in March (SL: 3 consecutive Mon-Wed + 2 LOP Friday-Monday)
  Pattern: Absences are clustered around weekends (Friday + Monday)
  Action required: VP conversation + attendance counselling
  If pattern continues: Escalate to formal HR action (L-06 performance)

⚠️ Ms. Kavitha M. (Class VI Maths):
  12 late arrivals in March — ⚠️ HIGH
  Pattern: Consistently 15–20 minutes late
  Threshold exceeded (3/month) → 3 half-day deductions applied this month
  Action: VP conversation required; may need transport arrangement help

✅ 28 teachers: Perfect attendance March ✅
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/attendance/?date={date}` | Daily staff attendance |
| 2 | `POST` | `/api/v1/school/{id}/hr/attendance/` | Submit attendance (manual) |
| 3 | `POST` | `/api/v1/school/{id}/hr/attendance/biometric-sync/` | Sync biometric events |
| 4 | `GET` | `/api/v1/school/{id}/hr/attendance/monthly/?month={m}&staff={id}` | Monthly summary |
| 5 | `GET` | `/api/v1/school/{id}/hr/attendance/patterns/` | Attendance pattern alerts |
| 6 | `GET` | `/api/v1/school/{id}/hr/attendance/staff/{staff_id}/` | Individual attendance history |

---

## 6. Business Rules

- LOP (Loss of Pay) is automatic after 2 consecutive unexplained absences; it feeds directly into payroll (L-04) for the affected month
- Principal must sign the monthly staff attendance register (physical format prescribed by state education department); EduForge generates the monthly register PDF for printing; Principal OTP sign-off in system supplements the physical signature
- Transport staff attendance is managed separately at 6:30 AM by Transport In-Charge; it feeds into the same L-02 system but is submitted as a separate role
- Biometric data (fingerprint) is processed by the biometric device only; EduForge receives only the attendance event (staff ID + timestamp + in/out) — not the fingerprint itself; this is a DPDPA-compliant design
- Late arrival deductions: school policy (configurable); default is 3 late arrivals per month before deduction triggers; the deduction logic is applied in payroll (L-04) automatically

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
