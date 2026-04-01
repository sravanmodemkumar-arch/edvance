# J-08 — Career Guidance & Counselling

> **URL:** `/school/welfare/career/`
> **File:** `j-08-career-guidance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Counsellor (S3) — career sessions and assessments · Academic Coordinator (S4) — stream selection approvals · Class Teacher (S3) — refer Class IX–X students · Principal (S6) — stream change approvals

---

## 1. Purpose

Career guidance helps students make informed decisions about subject streams (Class XI), higher education, and career paths. NEP 2020 mandates career counselling from Class IX onwards. CBSE recommends:
- Psychometric/aptitude assessments for Class IX–X students
- Stream counselling before Class XI subject selection
- Higher education guidance for Class XII
- Exposure to diverse career options beyond engineering and medicine

Career guidance is distinct from welfare counselling (J-01) — it is developmental and aspirational, not remedial. However, the counsellor role overlaps.

---

## 2. Page Layout

### 2.1 Header

```
Career Guidance & Counselling                        [+ Schedule Session]  [+ Group Session]
Academic Year: [2026–27 ▼]

Career sessions this year: 142 (individual: 86, group: 56)
Aptitude assessments completed: 210 (Class IX–X)
Stream change requests pending: 2
Students shortlisted for college application guidance: 72 (Class XII)
```

### 2.2 Career Guidance Activities Calendar

```
Upcoming Career Events:
  30 Mar 2026 — Group: Career Awareness — Class IX (Stream options overview)
  5 Apr 2026  — Individual: Arjun S. (XII-A) — IIT/NIT application strategy
  10 Apr 2026 — College fair (invited colleges — 8 institutions)
  15 Apr 2026 — Group: Class XI — Subject selection final counselling
  20 Apr 2026 — NEET awareness talk by Dr. Rama Rao (visiting doctor)

Past activities:
  Feb 2026 — Aptitude assessment for Class IX: 82 students ✅
  Jan 2026 — Career fair: 15 booths (engineering, medicine, law, arts, commerce) ✅
  Dec 2025 — Group: Class X stream counselling (parent + student sessions) ✅
```

---

## 3. Aptitude Assessment

```
Aptitude Assessment — Class IX — Academic Year 2025–26

Assessment tool: [Holland Code / DMIT / CBSE-recommended psychometric tool]
Administered: 15 February 2026
Students: 82/82 completed ✅

Assessment dimensions:
  ☑ Verbal aptitude
  ☑ Numerical aptitude
  ☑ Spatial reasoning
  ☑ Interest clusters (Holland: RIASEC)
  ☑ Personality traits (Big Five — simplified)

Aggregate results (class-level — individual results are confidential):
  Top interest cluster: Investigative (23%), Conventional (19%), Artistic (18%)
  Aptitude strength: Verbal (55% scored above average)

Individual student report: [Accessible only to the student, their parents, and counsellor]

Counsellor follow-up:
  Students needing individual career counselling (confused/conflicted): 14
  Students with clear direction: 42
  Students with misalignment (interest vs aptitude): 26 — [Schedule sessions]
```

---

## 4. Stream Selection — Class X to XI

```
Stream Selection — Batch 2025–26 (Class X → XI)

Process:
  Step 1: Aptitude assessment + counselling session (Feb–Mar)
  Step 2: Parent-student-counsellor meeting for undecided students (Mar–Apr)
  Step 3: Student submits stream preference form (portal — Apr 1–10)
  Step 4: Academic Coordinator reviews; assigns based on:
           - Student preference (primary factor)
           - Class IX–X marks (Science stream requires minimum 60% in Science + Maths)
           - Counsellor recommendation
  Step 5: Provisional allocation published (Apr 15)
  Step 6: Grievance period (3 days): students can request change
  Step 7: Final allocation (Apr 20)

Stream options offered:
  ☑ Science (PCM — Physics Chemistry Maths)
  ☑ Science (PCB — Physics Chemistry Biology)
  ☑ Commerce (Accountancy, Business Studies, Economics)
  ☑ Arts/Humanities (History, Political Science, Geography/Psychology/Economics)

Eligibility threshold (school policy — configurable):
  Science stream: Minimum 60% aggregate in Class X (+ 60% in Science & Maths specifically)
  Commerce: Minimum 50% aggregate
  Arts: Open (no minimum)

Stream allocation status — Class X (80 students):
  PCM: 28 (35%)  ·  PCB: 22 (27.5%)  ·  Commerce: 18 (22.5%)  ·  Arts: 12 (15%)

Stream change requests (after allocation):
  Ravi P. (X-A): Requested PCM → PCB (prefers biology)
  Sunita K. (X-B): Requested Commerce → PCM (reconsideration after counselling)
  [Review each request → Academic Coordinator decision]
```

---

## 5. Higher Education Guidance — Class XII

```
Higher Education Guidance — Class XII (72 students) — 2026–27

Categories:
  Engineering (JEE): 28 students — counsellor focus: IIT/NIT vs state colleges; coaching overlap
  Medical (NEET): 15 students — MBBS/BDS/BAMS/Nursing paths
  Commerce/CA: 10 students — CA foundation + B.Com options
  Arts/Law: 8 students — CLAT, BA (Hons) options, CUET
  Others (abroad, BBA, design, etc.): 11 students

Counsellor sessions this year:
  Individual guidance sessions: 58 completed
  Mock interview prep: 12 students
  Application essay review: 8 students (for foreign universities)

Key events:
  College fair (10 Apr 2026): 8 colleges attending — DU, SRM, Manipal, NLSIU, etc.
  CUET awareness session: 5 Apr 2026 (Counsellor + Academic Coordinator)
  JEE Main results counselling (post-result): Scheduled after April results

Referrals to external agencies:
  Abroad university: 3 students referred to college counsellor (external consultant)
  [Log external referral]
```

---

## 6. Career Resource Library

```
Career Resource Library — Student Access (via Parent/Student Portal)

Available resources:
  ● CBSE Career Guidance portal links
  ● NIOS stream guides
  ● UG entrance exam calendar (JEE/NEET/CUET/CLAT/NDA schedule)
  ● Scholarship database (J-09 integration — scholarships by career stream)
  ● Career videos curated by counsellor (Counsellor-reviewed YouTube playlist via G-09)
  ● College comparison tool (EduForge-curated for common Indian institution types)

Brochures and pamphlets: [Upload from college fair]
Last updated: 10 April 2026

Note: EduForge does not partner with or promote specific colleges; career resources
  are informational only; no affiliate relationships with coaching institutes or colleges
  are permitted in this module (conflict of interest with objective guidance).
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/welfare/career/sessions/` | Career session list |
| 2 | `POST` | `/api/v1/school/{id}/welfare/career/sessions/` | Schedule session |
| 3 | `GET` | `/api/v1/school/{id}/welfare/career/assessment/{batch}/` | Aptitude assessment results |
| 4 | `POST` | `/api/v1/school/{id}/welfare/career/stream-selection/` | Submit stream preference |
| 5 | `GET` | `/api/v1/school/{id}/welfare/career/stream-allocation/` | Stream allocation status |
| 6 | `PATCH` | `/api/v1/school/{id}/welfare/career/stream-allocation/{student_id}/change/` | Stream change request |
| 7 | `GET` | `/api/v1/school/{id}/welfare/career/resources/` | Career resource library |

---

## 8. Business Rules

- Aptitude assessment results are confidential to the student and their parents; they are NOT shared with subject teachers or used for academic grading; they are a guidance tool only
- Stream allocation is the Academic Coordinator's decision, not the counsellor's alone; the counsellor provides input but the AC has the final say on academic eligibility-based decisions
- A student who does not meet the eligibility threshold for their preferred stream can appeal to the Principal; the Principal can override the eligibility threshold with documented justification (e.g., student with 58% but strong aptitude assessment for science)
- Career guidance sessions are not confidential in the same way as welfare counselling (J-01); career guidance notes can be shared with the Academic Coordinator and parents on request
- NEP 2020 compliance: Career counselling must be available from Class IX; schools that offer career guidance only in Class XII are non-compliant with NEP spirit; EduForge tracks counselling across all classes IX–XII
- Schools cannot mandate specific streams against the student's will; a student who wants Arts despite strong science aptitude is entitled to choose Arts — the counsellor's role is to ensure the decision is informed, not to override it

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division J*
