# J-01 — Student Counselling Sessions

> **URL:** `/school/welfare/counselling/`
> **File:** `j-01-student-counselling.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Counsellor (S3) — full access · Principal (S6) — view case summaries (not session notes) · Class Teacher (S3) — refer and see status only · Academic Coordinator (S4) — view aggregate trends (anonymised)

---

## 1. Purpose

Manages the school counsellor's student sessions — scheduling, session notes, follow-up plans, and welfare outcome tracking. CBSE mandates a trained counsellor in every affiliated school; the counsellor's records are confidential by profession (psychotherapy confidentiality norms) but must be available to the Principal for safety decisions and POCSO mandatory reporting.

Critical principle: **The counsellor's session notes are NOT accessible to the class teacher, parent (except in safety emergencies), or any other staff.** The class teacher can only see that a student "is in counselling" — not why, not what was discussed.

Exception: If a student discloses abuse (POCSO), or expresses suicidal ideation, the counsellor must immediately inform the Principal (POCSO DO); confidentiality does not protect harmful information.

---

## 2. Page Layout

### 2.1 Header

```
Student Counselling                                  [+ Schedule Session]  [Referrals: 3]
Counsellor: Ms. Ananya Krishnan  ·  Today: 27 March 2026 (Friday)

Today's schedule:
  10:00 AM — Priya V. (XI-A) — Session 3 (academic stress)   [View]
  11:30 AM — Rahul M. (IX-B) — Session 1 (referred by CT: withdrawal behaviour)  [View]
  2:00 PM  — Group: VIII-A (5 students) — Peer relationships workshop  [View]
  3:30 PM  — Arjun S. (XII-A) — Walk-in (self-referred)  [Open slot]

Pending referrals (not yet scheduled): 3
Active cases (ongoing): 14
Closed this term: 8
```

### 2.2 Student Case List

```
Active Cases                          [Filter: Class ▼]  [Search student]

Student         Class  Referred by    Reason                Sessions  Status        Last Session
Priya V.        XI-A   Academic Coord  Academic stress       3         🔵 Ongoing   20 Mar 2026
Rahul M.        IX-B   Class Teacher  Social withdrawal      0         🟡 Scheduled 27 Mar 2026
Sneha R.        X-A    Self-referred  Exam anxiety          5         🔵 Ongoing   18 Mar 2026
Vikram P.       XII-B  Parent request  Career indecision     2         🔵 Ongoing   15 Mar 2026
Meera L.        VIII-C Class Teacher  Bullying concern       4         🔵 Ongoing   22 Mar 2026
...

[Pending Referrals]
Referral 1: Anjali K. (VII-B) — CT: "Frequent crying, won't speak in class" — [Accept]
Referral 2: Kiran S. (IX-A)  — H-12 Hostel welfare flag: "Homesickness" — [Accept]
Referral 3: Suresh V. (X-B)  — J-03 Anti-ragging: witness — [Accept — HIGH PRIORITY]
```

---

## 3. New Session / Case Opening

```
Open New Case

Student: [Rahul M. — IX-B]
Referred by: ● Class Teacher (Ms. Geeta Sharma)  ○ Self-referred  ○ Parent  ○ Principal
             ○ Hostel warden (H-12)  ○ Class teacher via E-09 attendance flag

Referral reason (teacher's note — confidential within system):
  "Rahul has become withdrawn over the past 3 weeks. Not participating in class,
   sitting alone at lunch. His grades dropped from B to D in last test."

Initial assessment type:
  ● Individual counselling
  ○ Group session
  ○ Career counselling (J-08)
  ○ Crisis intervention

POCSO pre-screen (counsellor must answer):
  Has the referral or initial contact indicated any possibility of abuse, assault,
  or inappropriate behaviour by any adult towards this student?
  ○ Yes — initiate J-02 POCSO protocol immediately
  ● No — proceed as welfare case

Consent:
  For students under 18: parent consent required for ongoing counselling
  ☑ Parent informed of referral: ✅ (class teacher notified parent verbally)
  ☐ Written parental consent obtained: ← Required before Session 2
    [Send consent form via F-03 WhatsApp]

Case ID: COUNS/2627/018 (auto-generated)
[Open Case]
```

---

## 4. Session Notes (Counsellor-Only View)

```
Case: COUNS/2627/018 — Rahul M. (IX-B)

⚠️ CONFIDENTIAL — Accessible to Counsellor and Principal (safety review) only.
   Class teachers, parents, and other staff CANNOT view this section.

Session 1 — 27 March 2026 — 11:30 AM — 50 minutes

Session type: Individual — Rapport building (first session)

Presenting concerns (student's own words):
  "I don't want to talk to anyone. School is boring. I just want to go home."
  Student appears socially withdrawn; made minimal eye contact in first 10 min;
  gradually more responsive after rapport exercise.

Key observations:
  - No overt signs of abuse or self-harm (arms/neck visible — no marks)
  - No POCSO-reportable disclosure
  - Possible adjustment difficulty (new class/section at start of year)
  - Possible peer isolation — not part of a friend group in IX-B

Interventions used:
  - Motivational interviewing (open questions)
  - Normalisation of adjustment difficulties

Homework/between-session task:
  "Write one thing you liked about school today — even if tiny"

Risk assessment:
  ● Low risk  ○ Moderate  ○ High/Immediate concern
  Self-harm indicators: None observed
  Suicidal ideation: Not expressed; not pursued in Session 1 (building trust first)

Plan for next session:
  - Explore peer relationships
  - Explore home situation (family stress as possible factor)
  - Schedule Session 2 with 1-week interval

Next session: [3 April 2026]  [Schedule]

Session notes saved: ✅  ·  Visible to: Counsellor + Principal (safety review mode) only
```

---

## 5. POCSO Disclosure Protocol (Triggered from Session)

```
⚠️ POCSO DISCLOSURE DETECTED

If during a counselling session a student discloses any form of sexual abuse,
inappropriate touching, assault, or exploitation by ANY adult (including family):

  MANDATORY ACTIONS — counsellor cannot delay, cannot withhold, cannot seek advice first:

  1. [Secure session notes — mark as POCSO disclosure]
    → Session notes automatically restricted to Principal/DO only (J-02 POCSO register)
    → Counsellor, even, does not have solo authority to manage this case

  2. [Notify Principal immediately]
    → In-person preferred; if unavailable, call
    → Do NOT use WhatsApp or email for the initial notification (privacy)

  3. [POCSO mandatory report — DCPU within 24 hours]
    → J-02 generates the mandated report format (Form under POCSO Section 19)

  4. [Student safety:]
    → Student must not be left alone with the alleged perpetrator pending inquiry
    → If perpetrator is a school staff member: immediate suspension of that staff
    → If perpetrator is a family member: DCPU/CWC decides protective measures

  5. Record-keeping: ← Counsellor must not discard or modify notes after POCSO disclosure

  Counsellor professional note: POCSO mandatory reporting supersedes all
  counsellor-patient confidentiality norms in India. Section 21 POCSO: failure
  to report is a punishable offence (6 months imprisonment).
```

---

## 6. Crisis Intervention (Suicidal Ideation)

```
⚠️ CRISIS PROTOCOL — Suicidal Ideation Expressed

If a student expresses suicidal thoughts, self-harm intent, or severe depression
during a session:

Immediate (same session):
  1. Do NOT leave the student alone
  2. Call Principal or Vice Principal to the counsellor's room immediately
     (phone call; do not send a message visible to others)
  3. Do NOT notify parents by WhatsApp; Principal makes the parent call personally

Same day:
  4. Mandatory referral to a licensed clinical psychologist/psychiatrist
     (school counsellor is not a clinician; cannot provide clinical treatment)
  5. Parent/guardian informed same day, sensitively, by counsellor + Principal together
  6. Safety plan developed with student and parent
  7. iCall (022-25521111) / Vandrevala Foundation (1860-2662-345) helpline shared

Documentation:
  8. Session notes flagged as HIGH RISK
  9. Principal reviews daily until clinical handover confirmed
  10. Student returns to school only with clearance from the external clinician

Note: Log this as a J-06 health welfare event also; class teacher is informed
  that student is on "welfare watch" (not the reason — just the flag)
```

---

## 7. Group Sessions

```
Group Session — Peer Relationships Workshop — 27 March 2026 — 2:00 PM

Class: VIII-A  ·  Participants: 5 students (counsellor-selected)
Session theme: Handling peer conflict constructively
Duration: 60 minutes

Students:
  Meera L. (VIII-C) — Case COUNS/2627/009 (bullying concern)
  [Names of other 4 participants — counsellor decides who is in group]

Group notes:
  [Group dynamics — not linked to individual student records]

Note: Group session notes do not appear in individual student case files;
  they are stored under the group session record only. Individual student
  records note only: "Participated in group session — peer relationships —
  27 Mar 2026 — positive engagement observed"
```

---

## 8. Class Teacher View (Restricted)

```
[Class Teacher View — Ms. Geeta Sharma, Class Teacher IX-B]

Students in IX-B with welfare flags:

Student     Flag                    Counsellor Status    Action for CT
Rahul M.    ⚠️ Referred to Counsellor  Session 1 completed  Continue normal engagement;
                                                           do not ask Rahul about counselling;
                                                           refer further concerns to Counsellor
Kiran S.    📚 Academic flag (E-09)    Not yet referred     [Refer to counsellor?]

Note: You can see that a student is in counselling, but NOT what was discussed.
  This is confidential to the counsellor and Principal.
  If you have urgent new concerns about Rahul, contact the Counsellor directly.
```

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/welfare/counselling/` | Case list (counsellor view) |
| 2 | `POST` | `/api/v1/school/{id}/welfare/counselling/` | Open new case |
| 3 | `GET` | `/api/v1/school/{id}/welfare/counselling/{case_id}/` | Case detail |
| 4 | `POST` | `/api/v1/school/{id}/welfare/counselling/{case_id}/session/` | Add session notes |
| 5 | `PATCH` | `/api/v1/school/{id}/welfare/counselling/{case_id}/status/` | Update case status (close/refer) |
| 6 | `POST` | `/api/v1/school/{id}/welfare/counselling/referral/` | Teacher refers student |
| 7 | `GET` | `/api/v1/school/{id}/welfare/counselling/teacher-view/{class_id}/` | CT restricted view (flag only) |
| 8 | `GET` | `/api/v1/school/{id}/welfare/counselling/trends/` | Anonymised aggregate trends (AC/Principal) |

---

## 10. Business Rules

- Session notes are accessible only to the Counsellor and Principal; even the referring Class Teacher cannot read session content — they see only "referred / in counselling / closed"
- Parent consent in writing is required before Session 2 for students under 18; counsellors may conduct one initial assessment session to gauge urgency before formal consent; but ongoing counselling requires written parental consent
- POCSO disclosure triggers immediate escalation regardless of counsellor's clinical judgement — this is a legal mandate, not a clinical decision
- Suicidal ideation or self-harm intent: the school counsellor must refer to a licensed clinical psychologist or psychiatrist within 24 hours; the school counsellor cannot provide clinical psychiatric care
- Session notes are retained for the duration of the student's enrollment + 3 years after leaving school (in case of retrospective POCSO or welfare disputes)
- Counsellor availability: CBSE mandates at least one trained counsellor per school; in schools >500 students, the counsellor cannot double as a subject teacher; EduForge enforces this by not assigning timetable slots to a role marked as Counsellor
- Group session notes are not linked to individual case files; participation is noted in the individual record without content disclosure
- DPDPA: counselling data is among the most sensitive categories; it must never be included in bulk data exports, analytics reports, or shared with parents in written form without the student's explicit consent (for students 18+ or emancipated minors)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division J*
