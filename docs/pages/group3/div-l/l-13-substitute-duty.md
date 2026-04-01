# L-13 — Substitute & Duty Management

> **URL:** `/school/hr/substitutes/`
> **File:** `l-13-substitute-duty.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Coordinator (S4) — assign substitutes, manage duty roster · Vice Principal (S5) — approve duty assignments · HR Officer (S4) — duty pay computation · Principal (S6) — override and final approval · Staff (S3–S5) — view own duty assignments

---

## 1. Purpose

When a teacher is absent, their classes cannot be left unsupervised — this is a child safety requirement, not just a curriculum continuity issue. Substitute and duty management covers:
- Identifying free-period teachers available for substitute duty
- Assigning substitutes fairly (rotation-based, not the same teacher every time)
- Tracking total substitute load (to avoid overburdening specific teachers)
- Duty roster (exam invigilation, event duties, gate duty, bus duty)
- Extra duty compensation (where applicable per school policy)
- Integration with L-02 (attendance) to auto-trigger substitute need

---

## 2. Daily Substitute Dashboard

```
SUBSTITUTE MANAGEMENT — 27 March 2026 (Friday)

Absences Today:
  Ms. Priya Iyer (TCH-015)  — English, Class XI     [On approved leave (L-03) ✅]
  Mr. Vijay P. (TCH-044)    — Social Sci, Class VII  [Sick leave: SMS at 7:15 AM]
  Ms. Radha N. (TCH-028)    — Art, Class VI–VIII     [Absent, no intimation ⚠]

Periods Requiring Coverage:
  ──────────────────────────────────────────────────────────────────────
  Period  Class      Subject     Regular Teacher   Substitute Assigned
  ──────────────────────────────────────────────────────────────────────
  P1      XI-A       English     Ms. Priya Iyer    Mr. Arun K. (free P1) ✅
  P2      XI-B       English     Ms. Priya Iyer    Ms. Jyothi P. (free P2) ✅
  P3      VII-B      Soc Sci     Mr. Vijay P.      Mr. Arjun R. (free P3) ✅
  P4      VII-A      Soc Sci     Mr. Vijay P.      Ms. Anita Rao (free P4) ✅
  P5      VII-C      Soc Sci     Mr. Vijay P.      Mr. Arjun R. (free P5) ✅
  P6      VI-A       Art         Ms. Radha N.      Mr. Deepak C. (free P6) ✅
  P7      VI-B       Art         Ms. Radha N.      Ms. Rekha B. (free P7) ✅
  P8      VI-C       Art         Ms. Radha N.      [No free teacher — GAP ⚠]
  ──────────────────────────────────────────────────────────────────────

GAP ALERT — P8, VI-C: No teacher with free period available
  Resolution options:
    ① Merge VI-C with VI-B (P8) in Room 2 [class size: 38+36=74 → exceeds room capacity ✗]
    ② VP supervises VI-C P8 directly ← Selected by VP ✅
    ③ Send VI-C students to library (structured reading — librarian present)

[Auto-notify substitutes via EduForge push notification] ✅ sent at 7:45 AM
```

---

## 3. Substitute Assignment Logic

```
SUBSTITUTE ASSIGNMENT ALGORITHM

Step 1: Identify free teachers at the period requiring coverage
  — Pull timetable (L-12) for that period
  — Filter: teachers with FREE period at that time
  — Exclude: teachers already doing a substitute that day (max 2 substitutes/day)
  — Exclude: teachers with a medical/leave flag for that day

Step 2: Sort available teachers by:
  Priority 1: Fewest total substitute periods this term (fairness rotation)
  Priority 2: Subject match (prefer same subject; for non-specialist Art/PT, any teacher)
  Priority 3: Same section familiarity (class teacher of that section preferred)

Step 3: Auto-suggest top 3 candidates; Academic Coordinator confirms with one click

Step 4: Notify substitute teacher (push notification + EduForge bell notification)
  Message: "You have been assigned substitute duty for [Class] [Subject] Period [X]
           today. Please proceed to [Room] at [time]. — Academic Coordinator"

Step 5: Log substitute assignment (teacher, class, period, date, type, notified at)

SUBSTITUTE TYPES:
  Type                Description
  Emergency-same      Same subject teacher (ideal — curriculum continuity)
  Emergency-free      Any free teacher (supervision duty — student revision period)
  Pre-planned         Arranged in advance (known leave, event, training)
  Long-term           Teacher absent >3 days → dedicated substitute arrangement
```

---

## 4. Substitute Tracking Register

```
SUBSTITUTE REGISTER — April 2026

Date    Absent Teacher    Class  Period  Substitute        Type           Status
01-Apr  Ms. Priya Iyer    XI-A   P1      Mr. Arun K.       Emergency-free ✅
01-Apr  Ms. Priya Iyer    XI-B   P2      Ms. Jyothi P.     Emergency-same ✅
03-Apr  Mr. Ravi K.       XI-B   P4      Ms. Sunita P.     Emergency-same ✅
03-Apr  Mr. Ravi K.       XII-A  P5      Mr. Suresh T.     Emergency-same ✅
05-Apr  Ms. Kavitha N.    IX-A   P2      Ms. Priya M.      Emergency-same ✅
10-Apr  Ms. Radha N.      VI-A   P6      Mr. Deepak C.     Emergency-free ✅
...
[Full month view with export]

SUBSTITUTE BURDEN SUMMARY — April 2026 (first 10 days):
  Teacher              Substitute periods taken  Warning threshold (20/month)
  Mr. Arun K.          6                         ✅ Normal
  Ms. Jyothi P.        4                         ✅ Normal
  Ms. Sunita P.        5                         ✅ Normal
  Ms. Priya M.         7                         ✅ Normal
  Mr. Deepak C.        8                         ⚠ Approaching (pace: 24/month)
  Mr. Arjun R.         9                         ⚠ Approaching (pace: 27/month)

ACTION: Academic Coordinator notified — reassign next substitutes away from Mr. Deepak
and Mr. Arjun to balance load.
```

---

## 5. Duty Roster

```
DUTY ROSTER — June 2026 (Exam Invigilation — Unit Test 1)

Exam Dates: 15–20 June 2026
Exam Coordinator: Ms. Kavitha N. (HOD Maths)

INVIGILATION ASSIGNMENTS:
  Date     Exam (Class/Subject)   Room  Invigilator 1      Invigilator 2
  15-Jun   Class IX — Maths       R-01  Mr. Deepak C.      Ms. Anita Rao
  15-Jun   Class X — Science      R-02  Ms. Rekha B.       Mr. Suresh T.
  15-Jun   Class XI — Physics     R-03  Ms. Kavitha N.     Mr. Arun K.
  16-Jun   Class IX — English     R-01  Ms. Jyothi P.      Ms. Geeta S.
  16-Jun   Class X — Maths        R-02  Ms. Priya M.       Mr. Vijay P.
  16-Jun   Class XI — Chemistry   R-03  Ms. Sunita P.      Ms. Radha N.
  ...
  [Full schedule — 20-Jun]

INVIGILATION RULES:
  ✅ Teacher cannot invigilate their own subject/class (conflict of interest)
  ✅ Two invigilators per room minimum (exam integrity)
  ✅ Flying squad (VP or senior teacher): 1 per session for cross-room visits
  ✅ Class Teacher cannot invigilate their own section (but can invigilate other sections)

OTHER DUTY TYPES:
  Gate Duty (morning): 7:30–8:10 AM — teacher at main gate for student arrival safety
    Rotation: All Class Teachers (one per week, Mon–Fri)
    Current week (15-Jun): Ms. Anita Rao (Mon), Mr. Arjun R. (Tue), ...

  Bus Duty: Teacher accompanies afternoon buses 1–2 times/month per teacher
    (Separate from hired escort — teacher presence for accountability)

  PTM Duty: All Class Teachers on PTM days (F-05 integration)

  Event Duty: Annual Day, Sports Day, Republic Day — separate duty sheet
    VP publishes 2 weeks in advance; teachers confirm availability
```

---

## 6. Extra Duty Compensation

```
EXTRA DUTY POLICY — Greenfields School

Within-scope (no extra pay):
  Substitute periods: Up to 5/month included in regular employment
  Gate duty, bus duty: Up to 2/month included
  PTM, event duties: Included (normal working hours)

Extra duty pay (school policy — above included threshold):
  Substitute periods >5/month: ₹150 per period
  Exam invigilation >6 sessions/exam-cycle: ₹200 per additional session
  Weekend event duty (school-day gate duty on Saturdays): ₹300/day
  Camp duty (overnight, residential): ₹500/day + meals

Guest Lecturers / Visiting Faculty:
  Paid per period: ₹400–₹800/period (depends on subject/qualification)
  TDS Sec 194J applicable if annual payment >₹30,000 (professional fees — 10%)
  Payroll integration: Period count × per-period rate → added to monthly payroll run

EXTRA DUTY LOG — Ms. Rekha B. (TCH-018) — June 2026:
  Substitute periods: 8 (threshold: 5) → 3 extra × ₹150 = ₹450
  Exam invigilation: 4 sessions (within 6 limit) → ₹0
  Gate duty: 2 days (within threshold) → ₹0
  June extra duty payment: ₹450 → added to June salary (L-04 integration) ✅

[View all extra duty claims for June]  [Approve and send to payroll]
```

---

## 7. Long-Term Substitute Arrangement

```
LONG-TERM SUBSTITUTE — Ms. Priya Iyer (TCH-015) Resignation
Last working day: 14 April 2026

Replacement needed from: 15 April 2026
Subject: English (Classes XI)
Periods/week: 12 (3 sections × 4 periods each)

Options considered:
  Option A: Internal reallocation — existing English teachers take extra load
    Ms. Rekha B.: current 24 periods → would become 28 (exceeds limit ✗)
    Ms. Jyothi P.: current 16 periods → would become 22 (feasible ✅ but interim only)
  Option B: Hire substitute teacher on daily-wage basis
    Rate: ₹1,200/day (school policy for substitute teachers — qualified B.Ed)
    TDS: Not applicable below threshold; but PAN must be collected
    Risk: Curriculum consistency, student rapport
  Option C: Accelerate recruitment (L-08) for permanent hire (target: June 2026)

Decision: Option A interim (Ms. Jyothi P.) until May 31; Option C recruitment to fill
by June 1, 2026.

Curriculum continuity brief prepared by Ms. Priya Iyer (handover notes):
  Class XI-A: Completed up to Chapter 8 (Hornbill); Writing skills: formal letter
  Class XI-B: Completed Chapter 7; gap in grammar (tenses — needs attention)
  Class XI-C: On track; strong readers; need more writing practice

[Long-term substitute file]  [Recruit permanent (L-08)]
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/substitutes/daily/` | Today's absence + coverage status |
| 2 | `POST` | `/api/v1/school/{id}/hr/substitutes/assign/` | Assign substitute for a period |
| 3 | `GET` | `/api/v1/school/{id}/hr/substitutes/register/` | Monthly substitute register |
| 4 | `GET` | `/api/v1/school/{id}/hr/substitutes/burden/` | Substitute load by teacher (fairness) |
| 5 | `GET` | `/api/v1/school/{id}/hr/duty/roster/` | Duty roster (invigilation, gate, bus) |
| 6 | `POST` | `/api/v1/school/{id}/hr/duty/roster/` | Create duty assignment |
| 7 | `GET` | `/api/v1/school/{id}/hr/duty/extra-pay/` | Extra duty compensation summary |
| 8 | `POST` | `/api/v1/school/{id}/hr/duty/extra-pay/approve/` | Approve extra duty for payroll |
| 9 | `GET` | `/api/v1/school/{id}/hr/substitutes/free-teachers/?date={date}&period={n}` | Available teachers for substitute |

---

## 9. Business Rules

- No class can be left unsupervised — this is an absolute child safety requirement; if no substitute is available, the VP or Principal must personally supervise or merge classes only if total size stays within room capacity; a gap in supervision is a serious safety incident
- Substitute assignment must be logged in the register even if it is a single period; the register is inspected by CBSE officials who look for evidence of continuous teaching coverage; gaps without explanation are noted as deficiencies
- The fairness rotation rule (fewest substitutes first) prevents the same teachers from being repeatedly burdened; in practice, free-period distribution in the timetable means some subjects have more free-period alignment — the algorithm handles this automatically but the coordinator can override for specific reasons
- A teacher assigned as substitute is still responsible for the class — they cannot leave students unattended to do their own work; substitute periods count as teaching for workload and duty purposes
- For exam invigilation, the rule prohibiting a teacher from invigilating their own subject is standard practice to prevent coaching or leaking during exams; the system enforces this automatically when generating the duty roster
- Extra duty pay above threshold must be approved by the Principal (not just Academic Coordinator) before being sent to payroll; this prevents unauthorized compensation claims; the L-04 payroll system only accepts approved extra duty records with an approval reference
- Guest lecturers paid per period are subject to TDS Sec 194J (professional fees, 10%) if their annual payment to that individual from the school exceeds ₹30,000; the HR module tracks cumulative payments per individual and auto-flags when approaching the threshold

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
