# L-09 — Onboarding

> **URL:** `/school/hr/onboarding/`
> **File:** `l-09-onboarding.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HR Officer (S4) — manage onboarding checklist · Vice Principal (S5) — induction programme · Academic Coordinator (S4) — academic systems orientation

---

## 1. Purpose

Structured onboarding for new staff ensures they are:
- Compliant (BGV submitted, POCSO training done, documents verified)
- Equipped (EduForge access, email, keys, ID card)
- Oriented (school culture, policies, academic calendar, reporting structure)
- Ready to teach (curriculum understanding, timetable, class teacher briefing)

A poor onboarding experience leads to early attrition; a teacher who doesn't understand expectations in the first month may fail probation due to unclear signals.

---

## 2. Onboarding Checklist

```
Onboarding — Ms. Anita Rao (TCH-046) — Joined 1 April 2026

Pre-Joining (Before Day 1):
  ☑ Appointment letter issued and signed
  ☑ EduForge account created (username: anita.rao@greenfields; temp password sent)
  ☑ Official email set up: anita.rao@greenfieldsschool.edu
  ☑ Timetable assigned (24 periods History IX–X) ✅
  ☑ Class Teacher — IX-A assigned ✅
  ☑ BGV form sent (to submit on Day 1) ✅

Day 1 (1 April 2026):
  ☑ School tour (buildings, labs, library, staffroom, admin office)
  ☑ Photo ID card: [Printed] ✅
  ☑ Staff locker allotted: Room 12, Locker 5 ✅
  ☑ Classroom keys: Allocated ✅
  ☑ BGV form submitted to police station ✅ (Compliance Officer accompanied)
  ☑ Bank account details collected for payroll ✅
  ☑ PAN card copy collected ✅
  ☑ Document originals verified: ✅ (B.A., B.Ed., CTET, experience letters)
  ☑ Service book opened: L-11 ✅
  ☑ Emergency contact recorded ✅

Week 1 (induction activities):
  ☑ Principal welcome meeting: 1 April 2026 ✅
  ☑ HR policy orientation (leave, attendance, payroll): 2 April ✅
  ☑ Academic orientation (CBSE curriculum, assessment pattern): VP — 3 April ✅
  ☑ EduForge training (how to take attendance, enter marks, communicate): 4 April ✅
  ⬜ POCSO awareness training: 10 April (scheduled — first Friday after joining)
  ☑ Classroom observation: Observed VP's Social Science class (model lesson) ✅
  ☑ Mentor teacher assigned: Ms. Geeta Sharma (senior social science teacher) ✅

Month 1 milestones:
  ⬜ First unit test results entered (E-09 and B-module)
  ⬜ First PTM participation (April PTM — with mentor teacher initially)
  ⬜ POCSO awareness: ✅ completed 10 April ← (pending)
  ⬜ Mentor meeting (end of Month 1): 30 April 2026

Month 3 (probation mid-point):
  ⬜ VP classroom observation (feedback session)
  ⬜ Formal probation review discussion

Month 6 (probation end):
  ⬜ Formal appraisal (L-06)
  ⬜ Confirmation of service OR extension of probation

[Generate onboarding PDF for HR file]
```

---

## 3. EduForge System Orientation

```
EduForge Access Setup — Ms. Anita Rao

Role assigned in EduForge: Class Teacher + Subject Teacher
Modules accessible:
  ✅ E-01 Attendance (Class IX-A — her class only)
  ✅ B-series academic modules (enter marks, view reports)
  ✅ F-09 Diary messages (assign homework)
  ✅ J-01 Welfare (refer students to counsellor, see welfare flags for IX-A)
  ✅ L-03 Leave (apply own leave)
  ✅ L-04 Payslip (view own payslip)
  ✅ F-05 PTM (manage PTM slots for IX-A)

Access NOT granted:
  ✗ Other classes' attendance or marks
  ✗ Fee or financial modules
  ✗ HR records of other staff
  ✗ POCSO register (J-02)
  ✗ Admin/compliance modules

Training given: 4 April 2026 (30-minute walkthrough by Academic Coordinator)
Practice mode: Available for 2 weeks (actions don't affect live data) ✅
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/onboarding/{staff_id}/` | Onboarding checklist for staff |
| 2 | `PATCH` | `/api/v1/school/{id}/hr/onboarding/{staff_id}/item/{item_id}/` | Mark checklist item done |
| 3 | `GET` | `/api/v1/school/{id}/hr/onboarding/pending/` | Staff with incomplete onboarding |

---

## 5. Business Rules

- POCSO awareness training must be completed within 30 days of joining; if the general annual session has already passed, the new joiner completes a dedicated induction session with the POCSO Designated Officer; this is non-negotiable (K-05)
- Service book must be opened on Day 1 (L-11); it records joining date, initial designation, basic pay, and relevant details; it is a permanent document
- EduForge access is provisioned before Day 1 (pre-joining); the new teacher can explore the system before their first class; this reduces anxiety and errors on Day 1
- Mentor teacher assignment: a senior teacher in the same subject/section is assigned as mentor for the first term; the mentor is not the appraiser (VP is); this separation ensures the new teacher can ask the mentor openly without fear of evaluation
- Onboarding checklist incompletion: if any mandatory item is not completed within the specified timeframe (BGV submission, POCSO training), the HR Officer escalates to the VP; persistent non-compliance with onboarding requirements feeds into the probation review

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
