# J-04 — Discipline Register

> **URL:** `/school/welfare/discipline/`
> **File:** `j-04-discipline-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full access, final authority on all orders · Vice Principal (S5) — full access · Discipline Committee Member (S3) — investigate and recommend · Class Teacher (S3) — log minor incidents, view own class · Counsellor (S3) — view referred cases (not investigation notes)

---

## 1. Purpose

Records all disciplinary incidents and the school's response — from minor classroom infractions to serious offences requiring committee inquiry. Discipline management in Indian schools must balance:
- **RTE Act Section 17:** Corporal punishment is absolutely prohibited; no physical punishment or mental harassment is permitted; violation by a teacher is a punishable offence
- **CBSE Conduct Rules:** Schools must have a documented discipline policy; expulsion of students requires a fair-hearing process
- **Student rights:** Students have the right to a hearing before any major disciplinary action (suspension/expulsion)
- **Child rights (NCPCR):** Dignity of the child must be preserved in all disciplinary proceedings; no public shaming

The register also tracks patterns: a student with 3 minor incidents becomes a welfare concern (referral to counsellor); a student with repeated severe infractions may require parent counselling and alternative intervention.

---

## 2. Page Layout

### 2.1 Header

```
Discipline Register                                  [+ Log Incident]
Academic Year: [2026–27 ▼]

This year:
  Minor incidents logged: 47
  Moderate incidents: 12
  Severe incidents (committee inquiry): 3
  Suspensions issued: 2
  Expulsions: 0
  Students with 3+ incidents (welfare flag): 2 → [Referred to counsellor J-01]
```

### 2.2 Incident List

```
Filter: Class [All ▼]  Severity [All ▼]  Status [All ▼]

INC No.        Date        Student       Class  Severity   Type                 Status
DISC/2627/001  5 Apr 2026  Rohit P.      IX-B   Minor      Homework not done    Closed — verbal
DISC/2627/002  12 Apr 2026 Arjun S.      XI-A   Minor      Mobile phone in class Closed — warning
DISC/2627/003  2 May 2026  Rakesh M.     X-A    Moderate   Classroom disruption  Closed — parents called
DISC/2627/004  18 Jun 2026 Vikram G.     XI-B   Severe     Physical fight        ✅ Committee resolved
DISC/2627/005  3 Jul 2026  Priya L.      XII-A  Minor      Absent without reason Closed — CT noted
DISC/2627/...  ...
```

---

## 3. Log Incident

```
[+ Log Incident]

Incident No.: DISC/2627/048 (auto-generated)
Date: [27 March 2026]  Time: [10:30 AM]
Logged by: Ms. Geeta Sharma (Class Teacher IX-B)

Student(s) involved:
  [Sanjay R. — IX-B]  [+ Add more if multiple students]

Incident type:
  Minor (class teacher handles):
    ○ Homework not submitted (repeated)
    ○ Mobile phone in class
    ● Disrespectful behaviour to teacher
    ○ Late to class (repeated)
    ○ Uniform non-compliance (repeated)

  Moderate (VP / class teacher with parent):
    ○ Classroom disruption (affecting others)
    ○ Absenteeism without valid reason (pattern)
    ○ Academic dishonesty (copying homework)

  Severe (discipline committee inquiry):
    ○ Physical violence / fighting
    ○ Vandalism of school property
    ○ Substance use (tobacco/alcohol) on school premises
    ○ Cheating in examination (J-04 + exam conduct linkage)
    ○ Threat to student/teacher
    ○ Social media misconduct targeting school community

  ⚠️ Zero-tolerance (immediate Principal + committee):
    ○ Ragging (→ J-03 also)
    ○ Any form of sexual misconduct (→ J-02 POCSO)
    ○ Weapon possession on school premises
    ○ Corporal punishment BY A TEACHER → this is a complaint against staff, not student

Description:
  [Student Sanjay R. responded to the class teacher's question by saying
   "I don't have to answer you" loudly in front of the class, and walked out
   of the classroom without permission.]

Witnesses: [Classmates — 30 students were present]

Immediate action taken:
  ☑ Student was asked to sit outside the Principal's office
  ☑ Parent notified: ← will be done after this log entry

Recommended response:
  ● Verbal counselling + parent intimation
  ○ Written warning
  ○ Parent called to school
  ○ Referral to counsellor (J-01)
  ○ Committee inquiry

[Save Incident]

Note: Incidents are never published to parents or other students in a way
  that publicly shames the student. Parent is informed privately.
```

---

## 4. Corporal Punishment Complaint (Against Staff)

```
⚠️ CORPORAL PUNISHMENT / MENTAL HARASSMENT COMPLAINT — AGAINST STAFF

RTE Act Section 17: Corporal punishment is BANNED. Any physical punishment or
mental harassment of a student by a teacher or school staff is a punishable
offence. This includes:
  - Any physical hitting, slapping, twisting ears, kneeling on floor for hours
  - Public humiliation (calling a student stupid, worthless, making them stand all day)
  - Withholding food (in hostels — H-08 also applies)

If a student or parent reports corporal punishment:
  1. Logged here (J-04) as a complaint against staff — NOT as a student discipline incident
  2. Immediately escalated to Principal
  3. Staff member must be taken off class duties pending inquiry (same-day)
  4. Inquiry by Principal + one senior teacher (parent representative optional)
  5. If substantiated: staff disciplinary action; HR record updated
  6. If government school: mandatory report to DEO
  7. If parent files a police complaint: school cooperates fully

Complaint: [________________________]
Staff member concerned: [Select from staff directory]
[Log Complaint — Escalate to Principal Immediately]
```

---

## 5. Suspension Process

```
Suspension Order — Student: Vikram G. (XI-B)
Incident: DISC/2627/004 — Physical fight — 18 June 2026

Discipline Committee Findings (meeting: 20 June 2026):
  Committee members: VP (chair), HOD Social Studies, HOD Science, Parent rep
  Hearing: Both students heard separately; witnesses heard
  Finding: Vikram G. initiated the fight (unprovoked); the other student (Anil P.)
           was primarily defending himself
  Recommendation: 3-day suspension; counselling referral; parents to accompany on return

Principal Order (22 June 2026):
  Suspension: 3 school days (23–25 June 2026)
  Additional: Must return with both parents; written apology to Anil P.;
              mandatory counselling (3 sessions — J-01)

Execution:
  ☑ Parent called to school: 22 Jun (mother attended)
  ☑ Suspension letter issued: DISC/ORD/2627/004
  ☑ Parent signed acknowledgement
  ☑ Re-admission on 26 Jun after parents met Principal ✅

Rights afforded:
  ☑ Student was heard (fair hearing conducted)
  ☑ Parents were notified before suspension took effect
  ☑ Suspension does not affect CBSE attendance calculation:
    These 3 days are noted as "suspension" — they do not count as working days
    BUT they also don't count as student's attendance (no benefit/no double penalty)
    The CBSE attendance shortfall rule (75%) is applied to working days only.
    Consulted CBSE: Suspended days are excluded from total working days count
    for the affected student only, but must not exceed 10 days in a year.
    [Principal note: verified with CBSE regional office, 21 Jun 2026]
```

---

## 6. Student Discipline Pattern Tracking

```
Student: Sanjay R. (IX-B) — Discipline Summary

Incidents:
  DISC/2627/018  5 May 2026    Minor: Late to class x3 in week     Verbal warning
  DISC/2627/031  10 Jun 2026   Minor: Mobile phone in class         Written warning
  DISC/2627/048  27 Mar 2026   Minor: Disrespectful to teacher      [Pending resolution]

Threshold alert: ⚠️ 3 incidents in one academic year
  → Auto-flag to Counsellor (J-01): "Sanjay has had 3 discipline incidents;
    please review if there is a welfare concern beneath the behaviour"
  → Counsellor view: behaviour pattern only; no session notes shared back to discipline

Parent engagement:
  Parent informed of Incident 1: Yes (verbal — CT)
  Parent informed of Incident 2: Yes (written notice)
  Parent informed of Incident 3: ← pending

Note: "Disrespectful behaviour" pattern in a previously compliant student
  may indicate stress, peer issues, or home circumstances — counsellor referral
  is welfare-oriented, not punitive.
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/welfare/discipline/` | Incident list |
| 2 | `POST` | `/api/v1/school/{id}/welfare/discipline/` | Log incident |
| 3 | `GET` | `/api/v1/school/{id}/welfare/discipline/{inc_id}/` | Incident detail |
| 4 | `PATCH` | `/api/v1/school/{id}/welfare/discipline/{inc_id}/resolve/` | Resolve with outcome |
| 5 | `GET` | `/api/v1/school/{id}/welfare/discipline/student/{student_id}/` | Student discipline history |
| 6 | `POST` | `/api/v1/school/{id}/welfare/discipline/{inc_id}/suspend/` | Initiate suspension order |
| 7 | `GET` | `/api/v1/school/{id}/welfare/discipline/committee-cases/` | Cases pending committee inquiry |
| 8 | `GET` | `/api/v1/school/{id}/welfare/discipline/pattern-flags/` | Students with 3+ incidents (welfare alerts) |

---

## 8. Business Rules

- Corporal punishment reports against teachers are handled as a staff complaint, not a student discipline matter; they are logged separately with escalation to the Principal and mandatory inquiry
- Suspension requires a fair hearing before the order is issued; the student must be heard (even briefly); parents must be notified; a student cannot be suspended with retroactive effect (i.e., suspended days cannot start before the order date)
- Expulsion is an extreme measure; it requires a full committee inquiry with parent present, Principal order, and the school must assist the student in finding another school (RTE mandate to not leave a child out of schooling)
- Three minor incidents in one year automatically generates a welfare referral to the counsellor; this referral is labelled as welfare support — the counsellor explores the cause, not the punishment
- Discipline records are retained for the student's full enrollment period + 5 years; severe incidents (suspension/expulsion) are retained indefinitely
- DPDPA: Discipline records are personal data of a minor; they cannot be shared with third parties (e.g., other schools, prospective employers) without the Principal's specific written authorisation; TC (C-13) includes a character certificate but DOES NOT include the detailed discipline log
- Class teachers can log minor incidents; VP and Principal can escalate; only Principal can issue suspension or expulsion orders — no other role has that authority

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division J*
