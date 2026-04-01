# I-01 — Student Counselling Services

> **URL:** `/college/welfare/counselling/`
> **File:** `i-01-counselling.md`
> **Priority:** P1
> **Roles:** Student Counsellor (S3) · Welfare Officer (S4) · Principal/Director (S6)

---

## 1. Counselling Service Overview

```
STUDENT COUNSELLING — GCEH

COUNSELLOR:
  Ms. Asha Reddy (M.Sc. Psychology, Registered Counsellor — RCI certified)
  Schedule: Monday, Wednesday, Friday — 10 AM to 4 PM
  Location: Welfare Block, Room W-02 (separate entrance — privacy maintained)
  Emergency contact: 9849XXXXXX (WhatsApp available after hours for crisis)
  Fee: Free to all GCEH students

HOSTEL VISITS:
  Tuesday, Thursday: Hostel welfare visits (boys + girls alternating)
  Group sessions: Monthly (hostel common room — study stress, relationships)
  Warden-counsellor coordination: Monthly meeting (welfare issues discussed anonymously)

APPOINTMENT SYSTEM:
  EduForge → Welfare → Book Counselling
  Appointment appears as "Wellness Appointment" on student's timetable (no "Counselling" label)
  Faculty cannot see counselling bookings (separate calendar — privacy)
  Walk-in: Allowed if no scheduled appointment (counsellor's discretion)

REFERRAL PATHWAYS:
  Warden → counsellor: "Student seems distressed" — warm referral
  Faculty → counsellor: "Student performance dropping with no academic reason" — suggest
  Parent → counsellor: Parent may call to raise concern (counsellor does NOT disclose session content to parents for adult students — Mental Health Care Act 2017)
  Counsellor → psychiatrist: For students needing medical intervention
    GCEH MoU: NIMHANS affiliated counsellor for teleconsultation; Kamineni Hospital referral
```

---

## 2. Counselling Sessions

```
COUNSELLING LOG — Anonymised Summary
(Individual records are DPDPA special-category data; not visible in this report)

SESSIONS 2026–27 (April 2026 – March 2027):
  Total sessions: 142
  Unique students: 68 (12.2% of 556 students)
  Repeat sessions: 74 (average 2.1 sessions/student)
  Walk-in vs appointment: 38% walk-in, 62% appointment

PRESENTING CONCERNS (anonymised categories):
  Academic stress (exams, results, backlog anxiety):  48 sessions (33.8%)
  Career uncertainty (placement anxiety, branch regret): 28 sessions (19.7%)
  Relationship issues (peer, romantic, family):        24 sessions (16.9%)
  Financial stress:                                    18 sessions (12.7%)
  Mental health (depression/anxiety self-reported):    12 sessions (8.5%)
  Ragging/harassment (referred to ARC/ICC):             4 sessions (2.8%)
  Other:                                               8 sessions (5.6%)

CRISIS INTERVENTIONS:
  Suicidal ideation: 2 cases (both referred to psychiatrist + parents informed
                              with student's consent in both cases)
  Self-harm concern: 1 case (psychiatric referral + follow-up ✅)
  All 3 students: Currently stable and continuing college ✅

COUNSELLOR OBSERVATIONS (trends):
  Nov 2026 spike: JNTU exam period — sessions doubled (19 in Nov vs 8/month avg)
  Most underserved: Male students (14% of sessions vs 38.5% share — stigma barrier)
  Action: Boys' hostel awareness session conducted Jan 2027 (30 students attended)
```

---

## 3. Confidentiality Framework

```
COUNSELLING CONFIDENTIALITY (Mental Health Care Act 2017 + DPDPA 2023)

WHAT IS CONFIDENTIAL:
  ✅ Everything discussed in counselling sessions
  ✅ The fact that a student is seeing the counsellor
  ✅ Assessment, diagnosis, or clinical notes
  ✅ Any personal information shared

EXCEPTIONS (counsellor may breach confidentiality):
  1. Immediate danger to self (suicidal with plan + means):
     → Parent/guardian informed (with student awareness if possible)
     → Principal informed for emergency protocol
     → 108 emergency if imminent risk
  2. Imminent danger to others:
     → Report to Principal + police if necessary
  3. Legal requirement (court order):
     → Counsellor consults with legal counsel before disclosing

WHO CAN ACCESS COUNSELLING RECORDS:
  Counsellor only (session notes)
  Welfare Officer: Aggregate statistics only (anonymised)
  Principal: Only if student is in serious risk + counsellor reports
  Faculty/Parents/Classmates: NEVER
  EduForge: Stores only session count + date (not content) in a separate encrypted table

STUDENT RIGHTS:
  Right to access own records: Yes (student can request their notes)
  Right to erasure: Yes (after leaving college — DPDPA)
  Right to refuse sharing: Yes (except crisis exceptions above)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/welfare/counselling/appointment/` | Book counselling appointment |
| 2 | `GET` | `/api/v1/college/{id}/welfare/counselling/my-appointments/` | Student's own appointments |
| 3 | `GET` | `/api/v1/college/{id}/welfare/counselling/statistics/` | Anonymised statistics (counsellor/welfare) |
| 4 | `POST` | `/api/v1/college/{id}/welfare/counselling/referral/` | Warden/faculty referral |

---

## 5. Business Rules

- Counselling records are health information — the highest category of sensitive personal data under DPDPA 2023; the college has no right to access session content; even the Principal can access only the minimum (student is in crisis — Y/N) and only when the counsellor determines there is a safety need; IT systems must store counselling session notes in an isolated, separately encrypted data store with audit logs on every access
- The mental health care of students is not optional charity; NAAC Criterion 5.1 evaluates student welfare services, and the absence of a qualified counsellor is a notable deficiency; beyond NAAC, student mental health crises that escalate because there was no counselling support create serious legal and reputational consequences for institutions
- Crisis protocol (suicidal ideation) must be clearly documented and all relevant staff must know it; a counsellor who identifies a student with a credible suicidal plan must act immediately; the protocol should include: parent contact, psychiatric referral, college medical officer alert, and follow-up schedule; EduForge's crisis flags are visible only to the counsellor and Welfare Officer
- Male students' lower utilisation of counselling services is a systemic issue across institutions; the solution is multiple: peer counsellor programme (trained senior students), sports-based mental wellness, and normalising help-seeking; a single female counsellor in a college that is 62% male will face this barrier; supplementing with peer counsellors from the student community is effective
- Parental rights vs student rights for adult students (18+): Under the Mental Health Care Act 2017, an adult student has full autonomy over their mental health care; parents cannot demand to know what their adult child discussed with the counsellor; this is a common source of conflict that the counsellor must navigate professionally; EduForge's consent management module records whether the student has consented to parental information sharing

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division I*
