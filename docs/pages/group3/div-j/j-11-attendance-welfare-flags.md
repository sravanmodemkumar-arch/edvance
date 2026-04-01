# J-11 — Attendance & Academic Welfare Flags

> **URL:** `/school/welfare/flags/`
> **File:** `j-11-attendance-welfare-flags.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Counsellor (S3) — all flags, triage and action · Class Teacher (S3) — own class flags · Academic Coordinator (S4) — academic risk flags · Principal (S6) — high-risk and escalated flags

---

## 1. Purpose

A unified welfare flag dashboard that aggregates signals from multiple modules:
- **E-09:** Attendance falls below 75% or triggers threshold alerts
- **J-04:** 3+ discipline incidents in a year
- **J-01:** Counsellor identifies a welfare concern
- **H-12:** Hostel welfare flag
- **J-03:** Anti-ragging victim
- **J-06:** Health alerts (unexplained absence, sick room patterns)
- Academic: Grade drop >20% between two consecutive assessments

This is the counsellor's central triage screen — instead of checking each module separately, all welfare signals surface here with recommended actions.

---

## 2. Dashboard

```
Welfare Flags Dashboard                              [Action Required: 7]
27 March 2026  ·  Counsellor: Ms. Ananya Krishnan

HIGH PRIORITY (immediate action):
  ● Rahul M. (IX-B) — 3 signals: attendance <60%, discipline pattern, counsellor active
    [View case]  [Schedule session today]

  ● Kiran S. (IX-A) — Hostel welfare flag (homesickness) + attendance 65%
    [View case]  [Coordinate with Chief Warden]

MEDIUM PRIORITY (this week):
  ● Sunita P. (VIII-B) — Grade drop 35% (Math: 89% → 54% between Term 1 and 2)
    [View case]  [Refer to subject teacher for extra support]

  ● Aryan V. (XI-B) — Anti-ragging incident (accused — counsellor referral per J-03)
    [View case]  [First session scheduled 1 Apr]

  ● Meera L. (VIII-C) — E-09 flag: 12 Monday absences (pattern — possible avoidance)
    [View case]  [Contact parent]

LOW PRIORITY (review this month):
  ● Deepa R. (X-A) — CWSN flag: Board exam accommodation application pending
    [Remind Academic Coordinator]

  ● Vijay K. (XII-A) — 0 weekend leaves from hostel all year (H-14 flag — social isolation?)
    [Welfare check by warden; escalate if pattern continues]

Statistics:
  Total active flags: 22
  New this week: 4
  Resolved this week: 3
  Average time to first action: 2.1 days
```

---

## 3. Flag Details — Multi-Signal Student

```
Flag Detail — Rahul M. (IX-B)

Active signals (3):

Signal 1: ATTENDANCE — from E-09
  Current attendance: 58% (122/220 days)
  75% threshold: requires 42 more working days of attendance to reach 75%
  Days remaining in year: 38 — ⚠️ CANNOT reach 75% even with 100% attendance hereafter
  E-09 status: Condonation application in process (E-10)
  Parent notified: ✅ 3 notices sent (F-16 parent notifications)
  CBSE action: At risk of not being eligible for Board exam if attendance not condoned

Signal 2: DISCIPLINE PATTERN — from J-04
  3 minor discipline incidents since April 2026
  Auto-referred to counsellor on 15 March (threshold trigger)
  Pattern: All 3 incidents happened on Mondays (possible weekend impact?)

Signal 3: COUNSELLOR ACTIVE CASE — from J-01
  Case COUNS/2627/018 opened 27 March (today — first session)
  Initial assessment: Social withdrawal, possible family stress
  Risk level: Low (current assessment — may change after more sessions)

Recommended actions:
  ✅ Session 1 today — rapport building
  ⬜ Parent meeting (counsellor + class teacher) — schedule for next week
  ⬜ Explore attendance pattern with parent (Monday pattern especially)
  ⬜ Coordinate with E-10 condonation application status

[Update welfare plan]  [Log action taken]
```

---

## 4. Grade Drop Flag

```
Academic Risk Flag — Sunita P. (VIII-B)

Grade drop detected: Mathematics
  Term 1 average: 89% (Excellent)
  Term 2 average: 54% (Fail)
  Drop: 35 percentage points — ⚠️ Significant

CBSE risk: No (Class VIII — no Board exam risk)
Academic risk: Yes — may affect Class IX placement

Possible reasons (auto-suggested based on pattern):
  ● New teacher in Term 2? Check with AC — [Mr. Ramesh replaced Ms. Priya in Jan 2026]
  ● Personal/home circumstances? Counsellor check
  ● Syllabus difficulty spike? Term 2 algebra is harder
  ● Missing foundational concepts?

Recommended actions:
  1. Subject teacher referral for remedial support — [Refer to Mr. Ramesh]
  2. Counsellor welfare check (brief — 15 min) to rule out personal factors
  3. Parent awareness — [Send academic alert F-16]

[Mark actions taken]
```

---

## 5. Hostel Welfare Cross-Reference

```
Hostel Welfare Flags — Cross-Reference with Day School

Students flagged by hostel warden (H-12):
  Kiran S. (IX-A):
    Hostel flag: Homesickness — eating less, calling home multiple times daily
    School flag: 65% attendance (borderline)
    Linked concern: Homesickness may be driving attendance avoidance (feigning illness)
    Joint action: Counsellor + Chief Warden joint meeting scheduled 28 Mar

  Ananya P. (VII-B):
    Hostel flag: Occasional nightmares, disturbed sleep
    School flag: None (academic performance normal)
    Note: Not yet a school-side welfare concern but monitor; counsellor informed

Coordination protocol:
  For hostel students, welfare flags from H-12 and J-11 are cross-linked.
  Hostel wardens and the counsellor coordinate for students with flags in both.
  Girls' hostel: Female counsellor or female warden leads; male staff do not meet
  the student alone (MHA guidelines apply in welfare meetings too).
```

---

## 6. Welfare Flag Lifecycle

```
Flag Lifecycle:

OPEN → ASSIGNED → ACTION IN PROGRESS → RESOLVED / ESCALATED

Stage transitions:
  OPEN: Flag auto-generated from source module (E-09, J-04, H-12, etc.)
  ASSIGNED: Counsellor acknowledges and claims the flag within 48 hours
  ACTION IN PROGRESS: At least one action taken (session scheduled, parent contacted)
  RESOLVED: Counsellor marks resolved when the underlying concern is addressed
  ESCALATED: If counsellor determines professional clinical referral needed, or
             POCSO concern, or the student is at high risk — Principal is looped in

SLA:
  High priority flags: First action within 24 hours
  Medium priority: First action within 3 school days
  Low priority: First action within 1 week

Report to Principal:
  Any flag that is not actioned within its SLA auto-notifies the Principal
  with: student name, flag type, days open, counsellor status
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/welfare/flags/` | All active welfare flags |
| 2 | `GET` | `/api/v1/school/{id}/welfare/flags/priority/{level}/` | Flags by priority (high/medium/low) |
| 3 | `GET` | `/api/v1/school/{id}/welfare/flags/student/{student_id}/` | All flags for one student |
| 4 | `PATCH` | `/api/v1/school/{id}/welfare/flags/{flag_id}/action/` | Log action taken |
| 5 | `PATCH` | `/api/v1/school/{id}/welfare/flags/{flag_id}/resolve/` | Resolve flag |
| 6 | `POST` | `/api/v1/school/{id}/welfare/flags/` | Manually create a flag |
| 7 | `GET` | `/api/v1/school/{id}/welfare/flags/sla-breached/` | SLA-breached flags (for Principal) |
| 8 | `GET` | `/api/v1/school/{id}/welfare/flags/dashboard/` | Counsellor dashboard summary |

---

## 8. Business Rules

- Welfare flags are automatically generated from source modules; the counsellor cannot prevent a flag from being raised (it is automatic), but can mark it as "reviewed — no action needed" with a reason
- The flag dashboard is visible to the counsellor (all flags), class teacher (own class only — limited information), and Principal (all — for oversight); parents never see the welfare flag dashboard
- Class teacher view of flags: shows only "student has a welfare flag" and "counsellor is working on it"; the class teacher does not see the reasons or signals unless the counsellor explicitly shares them
- Flag priority levels are auto-assigned but the counsellor can re-prioritise; however, re-prioritisation from HIGH to MEDIUM requires a reason to be logged
- SLA breach reporting to Principal is automatic and cannot be disabled; this ensures welfare concerns are not quietly missed
- When a flag involves the hostel and the school simultaneously (cross-module), the counsellor and hostel's Chief Warden coordinate; the first point of contact for the student is determined by which setting the concern originates from
- Academic risk flags (grade drop) do not automatically require counselling — the first response is a teacher-level academic intervention; counselling is escalated if the teacher's initial check suggests a welfare dimension (family stress, peer problems, etc.)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division J*
