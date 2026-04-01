# E-04 — Student Leave Application

> **URL:** `/school/attendance/leave/apply/`
> **File:** `e-04-leave-application.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Class Teacher (S3) — apply on behalf + approve · Administrative Officer (S3) — process medical leave · Parent (via parent portal) — apply for ward · Academic Coordinator (S4) — approve long leaves (> 5 days) · Principal (S6) — approve extended leaves (> 10 days)

---

## 1. Purpose

Manages student leave applications — formal requests for pre-approved absence. Leave management in Indian schools is important because:
- **Pre-approved leave vs unauthorised absence:** An approved leave may qualify for condonation in E-11 exam eligibility; an unauthorised absence does not
- **Medical leave documentation:** Doctor's certificate for sick leave is required for CBSE condonation of attendance shortage
- **Long leaves (> 5 days):** Family function, religious pilgrimage, medical treatment out of station — require Academic Coordinator/Principal approval
- **On-duty leave:** Sports/cultural representation — never counts against the student's attendance
- **Exam leave policy:** Many schools do not grant leave during exam periods (pre-exam 7 days and during exam) — system enforces this

Parents apply through the parent portal; Class Teachers can also apply on behalf of parents (e.g., when parent calls on phone).

---

## 2. Page Layout

### 2.1 Header (Class Teacher view)
```
Student Leave Applications — Class XI-A      [+ Apply Leave]  [Export]
Pending Approval: 2  ·  Approved This Month: 8  ·  Rejected: 1
```

### 2.2 Leave Queue
| App No. | Student | From | To | Days | Type | Reason | Status | Action |
|---|---|---|---|---|---|---|---|---|
| LA-2026-048 | Arjun Sharma | 28 Mar | 30 Mar | 3 | Family | Sister's wedding | ⏳ Pending | [Approve] [Reject] |
| LA-2026-047 | Priya Venkat | 25 Mar | 25 Mar | 1 | Medical | Fever | ✅ Approved | [View] |
| LA-2026-046 | Rohit Kumar | 20 Mar | 22 Mar | 3 | Medical | Typhoid | ✅ Approved | [View] |

---

## 3. Apply Leave Form

[+ Apply Leave] OR parent portal application → same form:

| Field | Value |
|---|---|
| Student | Arjun Sharma (STU-0001187) |
| Applied By | Parent (Rajesh Sharma) / Class Teacher Ms. Anita |
| Leave From | 28 March 2026 |
| Leave To | 30 March 2026 |
| Number of Days | 3 working days (auto-computed, excluding holidays) |
| Leave Type | Medical · Family Function · Personal · Sports/Cultural (On-duty) · Religious · Bereavement · Other |
| Reason (detailed) | Elder sister's wedding — family travel to Chennai |
| Supporting Document | [Upload — optional for family leave; mandatory for medical > 2 days] |
| Is during exam period? | ⚠️ Half-yearly exam starts 2 Apr — leave ends 30 Mar (OK) |
| Approval Required From | Class Teacher (≤ 5 days) / Academic Coordinator (6–10 days) / Principal (> 10 days) |

---

## 4. Leave Type Rules

| Leave Type | Document Required | Counts Against Attendance? | Condonation Eligible? |
|---|---|---|---|
| Medical (doctor cert) | Yes (for > 2 days) | Yes (but excused) | Yes |
| Family Function | No (parent letter) | Yes | No |
| Personal | No | Yes | No |
| Sports/Cultural (On-duty) | Participation certificate | **No** (denominator excluded) | N/A |
| Religious | No | Yes | No |
| Bereavement | Death certificate optional | Yes (but excused) | Yes (Principal discretion) |

---

## 5. Approval Workflow

### Class Teacher approval (≤ 5 days):
```
Leave Application — LA-2026-048

Student: Arjun Sharma (XI-A, Roll 02)
Leave: 28–30 March 2026 (3 days)
Type: Family Function — Sister's wedding — Chennai trip
Applied by: Father (Rajesh Sharma) via Parent Portal, 27 Mar 2026 at 8:12 PM

Current Attendance: 89.5% (185/207 working days)
After this leave: 185/210 = 88.1% — still above 75% threshold ✅
Next threshold risk: Student can afford 18 more absences before hitting 75%

[Approve] [Reject — Reason: _________________] [Request More Info]
```

### Long Leave escalation (> 5 days):
- 6–10 days: Academic Coordinator approval
- > 10 days: Principal approval
- > 20 days: Principal approval + parent meeting scheduled

---

## 6. Exam Period Block

If leave request falls during exam period (from A-12 Exam Calendar):
```
⚠️ EXAM PERIOD CONFLICT

Requested leave: 1–5 Apr 2026
School policy: No leave permitted during half-yearly exam week (1–8 Apr 2026)

Exceptions:
  ○ Medical emergency (hospitalisation) — Principal discretion
  ○ Death in immediate family — Principal discretion
  ○ CBSE board exam — automatic (not applicable)

[Override with Principal approval]  [Cancel Leave Request]
```

---

## 7. On-Duty Leave (Sports / Cultural)

```
On-Duty Leave — Arjun Sharma

Event: Telangana State Cricket Tournament — District team selection
Dates: 15–18 April 2026 (4 days)
Certified by: Sports Teacher Mr. Venkat

Effect on attendance:
  These 4 days will be excluded from the attendance denominator
  Attendance before: 185/207 = 89.5%
  Attendance after (4 days excluded from denominator): 185/203 = 91.1% ↑

[Approve with On-Duty flag]
```

---

## 8. Parent Portal Application

Parents apply from the parent portal:
- Enter dates, leave type, reason
- Upload medical certificate if applicable
- Receive notification when Class Teacher approves/rejects
- View leave history for their child

```
Parent Portal — Leaves — Arjun Sharma

Leave History 2026–27:
  Apr 2026: 1 day — Medical (fever) — ✅ Approved
  Aug 2026: 3 days — Family Function — ✅ Approved
  Nov 2026: 5 days — Religious (Diwali travel) — ✅ Approved

Current Attendance: 89.5%
Leaves remaining before 75% threshold: 18 more days
```

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/leave/?class_id={id}&status={status}` | Leave application list |
| 2 | `POST` | `/api/v1/school/{id}/attendance/leave/` | Apply for leave |
| 3 | `GET` | `/api/v1/school/{id}/attendance/leave/{leave_id}/` | Leave application detail |
| 4 | `PATCH` | `/api/v1/school/{id}/attendance/leave/{leave_id}/approve/` | Approve/reject leave |
| 5 | `GET` | `/api/v1/school/{id}/attendance/leave/student/{student_id}/?year={y}` | Student's leave history |
| 6 | `GET` | `/api/v1/school/{id}/attendance/leave/impact/{student_id}/?from={date}&to={date}` | Impact on attendance % before applying |

---

## 10. Business Rules

- Leave application approval does not automatically mark the student as Present — actual daily attendance (E-01) still records absence; leave status is used for condonation eligibility computation in E-11
- On-duty leave (sports/cultural) is the only leave type where the denominator is reduced; all other leave types keep the denominator unchanged
- A student on approved leave who still appears at school is marked Present in E-01 (the leave is cancelled automatically — system prompts the Class Teacher)
- Retrospective leave applications (after the absence occurred) are allowed within 7 days with parent note; beyond 7 days, a medical certificate is required for retroactive medical leave; retroactive family leave is not permitted
- Leave during board exams (CBSE Class X/XII) is not possible to approve — CBSE exam is nationally scheduled and any absence is automatically a board exam absence (marked by CBSE separately)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
