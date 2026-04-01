# H-12 — Student Welfare (Hostel)

> **URL:** `/school/hostel/welfare/`
> **File:** `h-12-student-welfare-hostel.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chief Warden (S4) — welfare oversight · Warden (S3) — report concerns · Matron (S3) — girls' welfare · School Counsellor (S4, J-01) — professional support · Principal (S6) — critical welfare decisions

---

## 1. Purpose

Manages the psychological and social welfare of boarding students — a distinct and critical concern for residential schools. Students living away from home face unique stressors:
- **Homesickness:** Very common in the first 1-2 months; can be debilitating; younger students especially (Classes VI–VIII)
- **Bullying/ragging:** Documented risk in residential settings; H-10 conduct register links here for escalation
- **Mental health:** Exam pressure, peer competition, distance from parents — boarding students are at elevated risk
- **Family crisis at home:** Student hears bad news (family illness, financial crisis, divorce) while at school — requires pastoral support
- **POCSO:** If a boarding student discloses abuse, the welfare protocol activates POCSO procedures immediately
- **LGBTQ+ sensitivity:** NEP 2020 and NCPCR guidelines require inclusive welfare support; schools must provide non-judgmental support

---

## 2. Page Layout

### 2.1 Header
```
Student Welfare — Hostel                             [Log Welfare Concern]  [Schedule Counsellor]
Academic Year: [2026–27 ▼]

Active welfare cases: 8
  Homesickness: 3  ·  Academic stress: 3  ·  Behavioural: 1  ·  Family crisis: 1
Counsellor session scheduled this week: 5
POCSO referrals this year: 0
```

### 2.2 Active Cases
```
Student       Class  Concern             Since       Counsellor   Status
Rohit M.      VI-A   Homesickness        15 Apr 26   Ms. Kavitha  🟡 In progress
Priya V.      XI-A   Academic stress     10 Mar 26   Ms. Kavitha  🟡 In progress
Arjun S.      XI-A   Ragging (H-10)      10 Mar 26   Ms. Kavitha  🟡 In progress
Meena D.     XII-A   Family crisis       20 Mar 26   Ms. Kavitha  🟡 Ongoing
```

---

## 3. Log Welfare Concern

```
[Log Welfare Concern]

Student: [Rohit M. — VI-A]
Reported by: Mr. Suresh Kumar (Warden)
Date: 15 April 2026 (Day 5 of new academic year)

Concern category:
  ● Homesickness  ○ Bullying/ragging  ○ Academic stress
  ○ Family crisis  ○ Mental health (suspected)  ○ POCSO  ○ Other

Presenting signs:
  ☑ Crying frequently (especially evenings)
  ☑ Not eating properly (3 meals missed this week)
  ☑ Withdrew from group activities
  ☐ Not sleeping
  ☐ Expressing desire to self-harm (immediate POCSO/counsellor referral)

Warden's observations:
  "Rohit came from Hyderabad for the first time. He has been crying each night
   since joining the hostel on 10 Apr. He is not participating in activities and
   barely eating. This is classic initial homesickness."

Immediate actions:
  ☑ Warden spending extra time with student ✅
  ☑ Arranged call with parents: 15 Apr 6:30 PM ✅
  ☑ Buddy system: paired with Arun (VI-A, 2nd-year student) ✅

Escalation: ☑ Refer to school counsellor (Ms. Kavitha) for professional support
Counsellor session: [16 April 2026, 4 PM]

Parent notification: ✅ "Rohit is adjusting to hostel life. The initial period can
  be challenging. We are supporting him actively. We will schedule a parent call
  this weekend. — Chief Warden"

[Submit Welfare Concern]
```

---

## 4. Counsellor Integration

```
Welfare Case — Rohit M. (VI-A) — Counsellor Session Notes

Session 1 (16 Apr 2026):
  Conducted by: Ms. Kavitha (School Counsellor, J-01)
  Duration: 45 minutes
  Observations: Student is anxious about being away from family; fears
  parents "won't remember him." Intellectually understands the opportunity
  (JNV-equivalent school) but emotionally struggling.

  Interventions:
  ✅ Normalised feelings (all new students feel this way)
  ✅ Established daily 10-minute parent video call schedule
  ✅ Introduced Rohit to 3 other Class VI students also adjusting
  ✅ Provided "friendship diary" activity

Follow-up session: 23 April 2026

Chief Warden can view: Session summary and action plan (not detailed notes)
Details are counsellor-client confidential: Detailed session notes → Counsellor only
```

---

## 5. Crisis Protocol

```
Crisis Protocol — Student in Acute Distress or Self-Harm Risk

Signs: Student expresses desire to harm themselves; severe withdrawal;
       visible injuries; extreme emotional crisis

IMMEDIATE STEPS (< 5 minutes):
  1. Warden stays with student; does NOT leave them alone
  2. [Alert Counsellor NOW] → Ms. Kavitha +91 9999-XXXXX
  3. [Alert Principal] → Dr. N. Subramanian +91 8888-XXXXX
  4. [Alert Parent] → Immediate phone call (not WhatsApp)

If counsellor unavicts in 10 minutes:
  5. → iCall helpline (TISS): 9152987821
  6. → Vandrevala Foundation: 1860-2662-345 (24/7)

If immediate physical danger:
  7. → NIMHANS National Mental Health Helpline: 080-46110007
  8. → Hospital emergency

[Crisis Alert: Log + Notify All Three (Counsellor + Principal + Parent)]

This button is visible on the welfare page to all hostel staff.
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/welfare/?year={y}` | Active welfare cases |
| 2 | `POST` | `/api/v1/school/{id}/hostel/welfare/` | Log welfare concern |
| 3 | `GET` | `/api/v1/school/{id}/hostel/welfare/{case_id}/` | Case detail |
| 4 | `POST` | `/api/v1/school/{id}/hostel/welfare/{case_id}/counsellor-note/` | Add counsellor session note |
| 5 | `POST` | `/api/v1/school/{id}/hostel/welfare/crisis/` | Trigger crisis protocol |
| 6 | `GET` | `/api/v1/school/{id}/hostel/welfare/analytics/?year={y}` | Welfare trends |

---

## 7. Business Rules

- Welfare cases are confidential — visible to Chief Warden, Counsellor, and Principal; not to other wardens or parents by default (parents are informed at the warden/counsellor's discretion)
- Self-harm risk or POCSO disclosure activates a mandatory protocol that cannot be silenced or delayed by any staff member regardless of seniority
- The school counsellor (J-01) must visit the hostel at least twice per week for welfare check-ins; their visit schedule is tracked here
- Homesickness: First 30 days are the critical adjustment period; students who don't show improvement by day 30 are escalated to the school counsellor for professional assessment
- Anti-ragging cases (H-10) are automatically linked to welfare cases — the victim receives welfare support and the aggressor receives counselling (restorative approach)
- LGBTQ+ welfare concerns are handled with additional confidentiality; the student chooses who is informed; the counsellor's support is unconditional and non-judgmental

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
