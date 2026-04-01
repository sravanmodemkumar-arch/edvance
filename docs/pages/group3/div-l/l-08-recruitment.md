# L-08 — Recruitment

> **URL:** `/school/hr/recruitment/`
> **File:** `l-08-recruitment.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HR Officer (S4) — manage recruitment process · Principal (S6) — interview panel, final selection · Vice Principal (S5) — conduct demo classes, interview · Academic Coordinator (S4) — subject-specific evaluation

---

## 1. Purpose

Manages the recruitment lifecycle for new staff — from vacancy identification to offer letter. Schools have specific requirements for teacher recruitment under CBSE and RTE:
- Qualifications must meet CBSE Affiliation Bye-Laws standards
- TET requirement for Classes I–VIII must be verified at hiring
- BGV must be initiated before deployment (K-05)
- Appointment letter must specify probation period, terms of service

---

## 2. Vacancy Management

```
Open Positions — 2026–27

Position                Class Assigned   Qualification Required    Status
Physics Teacher (XI–XII) Class XI–XII    M.Sc Physics + B.Ed       ✅ Filled (Mr. Suresh R. — 20 Mar)
History Teacher (IX–X)   Class IX–X      B.A. History + B.Ed       ⏳ Interviewing
Substitute Pool          —               B.Ed + subject expertise   ⬜ 2 positions open
Hostel Warden (Female)   Hostel          Any graduate + experience  ⬜ Interviewing

History Teacher — Position Profile:
  Classes: IX–X (4 sections each)
  Periods/week: 24
  CBSE TET/STET: Required (K-02: current teacher has TET under process — this is a new hire)
  Additional: Class Teacher availability preferred
  CTC range: ₹4,00,000 – ₹5,00,000/year (T-2 to T-3 band)
```

---

## 3. Job Posting

```
Job Posting — History Teacher

Posted on: 10 March 2026
Platforms: School website (careers page) + teacher job portals
  ● School website career page
  ● TeachersAhead.com (teacher-specific platform)
  ● NaukriGuru (general — for reach)
  ● CBSE teacher network newsletter (if applicable)
  ● Whatsapp teacher group (Hyderabad CBSE teachers network)

Application deadline: 31 March 2026
Applications received: 14 (as of 27 March 2026)

Shortlisting criteria (auto-filter):
  ✅ Graduation + B.Ed: 14/14 ✅ (all have minimum qualification)
  ✅ CTET/STET-TS: 10/14 (4 do not have TET — excluded for direct hire;
     may be hired if willing to obtain TET within 6 months — noted for probation condition)
  ✅ Minimum 3 years experience: 9/14 (5 are freshers — kept in secondary pool)

Shortlisted for demo + interview: 6 candidates
```

---

## 4. Recruitment Process

```
Recruitment Process — History Teacher

Stage 1: Application review ✅ (shortlisted 6)
Stage 2: Demo class (25–30 min, Class IX-A students, topic assigned)
  Evaluation criteria:
    Content accuracy: 30%
    Classroom presence and engagement: 25%
    Language and communication: 20%
    Lesson structure and pedagogy: 25%

Stage 3: Interview (20–30 min)
  Panel: Principal, VP, HOD Social Science, parent representative (optional)
  Topics: Subject knowledge, classroom management, NEP 2020 awareness,
          handling diverse learners, school culture fit

Stage 4: Document verification
  ☑ Originals of all certificates seen
  ☑ TET certificate verified (if claimed)
  ☑ Previous employment letter (relieving letter from last school)
  ☑ Reference check (call previous principal)

Stage 5: BGV initiation (before offer letter is accepted)
  BGV submitted to police station BEFORE first day (K-05)

Demo + Interview Schedule:
  Day 1 (28 Mar): Candidates 1–3
  Day 2 (29 Mar): Candidates 4–6
  Decision by: 1 April 2026

Current evaluation:
  Candidate A (Ms. Anita Rao): Demo 88% · Interview: Strong ✅
  Candidate B (Mr. Kiran V.):  Demo 82% · Interview: Good, fresher ✓
  ...
```

---

## 5. Appointment Letter

```
GREENFIELDS SCHOOL — APPOINTMENT LETTER

To,
Ms. Anita Rao

Dear Ms. Anita,

We are pleased to appoint you as HISTORY TEACHER (Class IX–X) at GREENFIELDS SCHOOL,
Chaitanyapuri, Hyderabad, subject to the following terms and conditions:

1. Designation: History Teacher
2. Date of joining: 1 April 2026
3. CTC: ₹5,20,000 per annum (see attached salary annexure)
4. Probation period: 6 months (1 April 2026 to 30 September 2026)
5. Notice period: 1 month (both parties) after confirmation; 30 days during probation
6. Leave: As per school leave policy (L-03)
7. Working hours: 7:45 AM to 3:30 PM; 5.5 days/week

Conditions of employment:
  a. This appointment is subject to satisfactory police background verification.
     You are required to submit the BGV form on the date of joining.
     Deployment in student-facing roles is conditional on BGV clearance.
  b. CTET/STET-TS must be obtained within 12 months of joining.
     Failure to obtain TET by 31 March 2027 will result in review of continuation.
  c. This appointment is conditional on providing originals of all educational
     certificates on joining; if any certificate is found to be forged,
     the appointment is void and FIR will be filed.
  d. POCSO awareness training is mandatory within 30 days of joining.
  e. The school may require you to act as Class Teacher for an assigned section.

Signed: Principal — Ms. Meena Rao   Date: 31 March 2026

Please sign and return a copy by: 2 April 2026.
[Download offer letter]  [Log acceptance date]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/recruitment/vacancies/` | Open vacancies |
| 2 | `POST` | `/api/v1/school/{id}/hr/recruitment/vacancies/` | Create vacancy |
| 3 | `POST` | `/api/v1/school/{id}/hr/recruitment/applications/` | Log application |
| 4 | `GET` | `/api/v1/school/{id}/hr/recruitment/applications/?vacancy={id}` | Applications for vacancy |
| 5 | `POST` | `/api/v1/school/{id}/hr/recruitment/applications/{id}/stage/` | Update recruitment stage |
| 6 | `POST` | `/api/v1/school/{id}/hr/recruitment/offer/` | Generate offer letter |

---

## 7. Business Rules

- A teacher cannot join and take a class on Day 1 if their BGV has not been submitted; BGV submission is Day 1 activity; demo and observation classes while BGV is in process are supervised (another teacher present)
- Qualification verification is mandatory before offer letter is signed; the original certificate must be seen; a photocopy-only acceptance and later discovery of forgery is legally more complex
- TET condition in appointment letter: for Classes I–VIII teachers without TET, a time-bound condition (12 months) must be in the appointment letter; if TET is not obtained, the school has documented grounds for non-renewal
- Relieving letter from previous employer: the school should verify that the candidate is not absconding from their previous employment (common problem); a relieving letter or equivalent confirmation protects the school
- Reference check: calling the previous principal is a best practice; previous employer may disclose concerns that do not appear in documents (discipline issues, child safety concerns)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
