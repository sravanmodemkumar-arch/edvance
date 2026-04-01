# B-34 — Remedial Teaching Register

> **URL:** `/school/academic/remedial/`
> **File:** `b-34-remedial-teaching.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Coordinator (S4) — full · HOD (S4) — own dept · Subject Teacher (S3) — conduct/record sessions · Class Teacher (S3) — view own class students · Principal (S6) — full

---

## 1. Purpose

Tracks remedial (supplementary) teaching for students who are academically at risk — scoring below the threshold in one or more subjects. NEP 2020 explicitly mandates: "students who are struggling academically should receive supplementary instruction." CBSE also recommends remedial teaching in its annual circulars. This page manages the end-to-end cycle: identify at-risk students from results → assign remedial teacher and schedule → track student attendance in remedial sessions → conduct a re-assessment → document improvement. The Principal uses this as evidence of the school's academic support system during CBSE inspections.

**At-risk threshold:** Students scoring < 35% in any subject after an exam. Schools can configure this threshold.

---

## 2. Page Layout

### 2.1 Header
```
Remedial Teaching Register                        [+ Add Student]  [Export Register]  [Report]
Academic Year: 2025–26  ·  Post-Exam: Annual Exam 2025–26
At-Risk Students Identified: 142  ·  Enrolled in Remedial: 118  ·  Completed Remedial: 62  ·  In Progress: 56
```

---

## 3. At-Risk Student Identification

After each exam, students < 35% are auto-populated here:

**Source:** B-20 (Result Analytics) → [Remedial Plan] button pushes students here.

| Student | Class | Section | Subjects at Risk | Score | Exam | Identified Date | Status |
|---|---|---|---|---|---|---|---|
| Deepak M | XI | A | Chemistry | 28/80 (35%) | Annual 2025–26 | 28 Mar | 🔄 Remedial in progress |
| Ravi P | IX | C | Mathematics (28%), Hindi (31%) | Low | Annual | 28 Mar | ⬜ Not yet enrolled |
| Anand T | VII | B | Science | 22/80 (27.5%) | Annual | 28 Mar | 🔄 In progress |
| Suhani K | X | A | Social Studies | 30/80 (37.5%) | Annual | 28 Mar | ⬜ Not yet enrolled |

---

## 4. Remedial Enrollment

For each at-risk student, a remedial plan is created:

[Enroll] → drawer:

| Field | Value |
|---|---|
| Student | Auto-filled |
| Subject(s) at Risk | Auto-filled from results |
| Remedial Teacher | Select from department (usually same subject teacher) |
| Session Schedule | Days + Time (e.g., Mon/Wed/Fri, 3:00–4:00 PM) |
| Duration | 4 weeks / 6 weeks / 8 weeks |
| Session Count (planned) | Total sessions (e.g., 3 sessions/week × 4 weeks = 12) |
| Pre-assessment Score | Score from the triggering exam (auto-filled) |
| Goal | "Reach 50% in next unit test" |
| Parent Notified | ✅ Yes — automatic WhatsApp sent |

---

## 5. Remedial Session Log

For each enrolled student, teachers log sessions attended:

### Deepak M — Chemistry Remedial (Class XI-A)

```
Teacher: Mr. Ravi Kumar  ·  Schedule: Mon/Wed/Fri 3:00–4:00 PM
Pre-assessment Score: 28/80 (35%)  ·  Target: 50%+ in supplementary test

Session Log:
─────────────────────────────────────────────────────────────────────
Date       Time          Topics Covered                 Attended  Teacher Notes
────────────────────────────────────────────────────────────────────
31 Mar     3:00–4:00 PM  Electrochemistry basics        ✅        Good attention
2 Apr      3:00–4:00 PM  Nernst equation                ✅        Struggled with formula
4 Apr      3:00–4:00 PM  Nernst practice problems       ✅        Improved understanding
7 Apr      3:00–4:00 PM  Chemical kinetics              ❌ Absent  Parent informed
9 Apr      3:00–4:00 PM  Chemical kinetics cont.        ✅        —
11 Apr     3:00–4:00 PM  Mock mini-test (20 marks)      ✅        Scored 14/20 = 70% ↑
─────────────────────────────────────────────────────────────────────
Attendance: 5/6 sessions (83.3%)
```

---

## 6. Re-Assessment

After completing the remedial programme, a re-assessment test is conducted:

| Student | Subject | Pre-Score | Post-Score | Change | Recommendation |
|---|---|---|---|---|---|
| Deepak M | Chemistry | 28/80 (35%) | 47/80 (58.8%) | ↑ 23.8% | ✅ Passed — no further remedial |
| Ravi P | Mathematics | 22/80 (27.5%) | 29/80 (36.3%) | ↑ 8.8% | 🔄 Extended remedial needed |
| Ravi P | Hindi | 25/80 (31.3%) | 38/80 (47.5%) | ↑ 16.2% | ✅ Passed threshold |
| Anand T | Science | 22/80 (27.5%) | 24/80 (30%) | ↑ 2.5% | 🔴 No improvement — counsellor referral |

**Counsellor referral** trigger: Student completes full remedial programme with < 5% improvement → automatic referral to school counsellor (B-k-series, Student Welfare).

---

## 7. Parent Communication

Every student's enrollment in remedial is communicated to parents:

**Initial notification (auto-sent on enrollment):**
"Dear Parent, [Student Name] has been identified for remedial support in [Subject]. Sessions are scheduled on [Days] at [Time]. Attendance is important for improvement. Contact class teacher for queries."

**Progress update (weekly, auto-sent):**
"Remedial Teaching Update — [Student]: Attended 3/3 sessions this week. Topic covered: Electrochemistry. Next session: Wednesday 4 PM."

**Completion notification:**
"Remedial Teaching Completed — [Student]: Pre-score: 35%, Post-score: 58.8%. Improvement noted. Report card update pending."

---

## 8. Department-wise Remedial Summary (HOD View)

| Subject | Class | At-Risk Count | Enrolled | Completed | Avg Improvement |
|---|---|---|---|---|---|
| Chemistry | XI | 3 | 3 | 2 | +18.4% |
| Physics | XI | 1 | 1 | 0 | — |
| Biology | IX | 4 | 3 | 1 | +12.8% |
| Chemistry | IX | 2 | 2 | 2 | +21.2% |

---

## 9. Compliance Export

[Export Register] → generates the Remedial Teaching Register PDF in the format required for CBSE inspection:
- School header
- Academic year
- For each student: name, class, subject, sessions attended, pre/post score
- Teacher signature, HOD counter-sign, Principal's stamp

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/remedial/?year={year}&exam_id={id}` | At-risk + remedial list |
| 2 | `POST` | `/api/v1/school/{id}/remedial/` | Enroll student |
| 3 | `GET` | `/api/v1/school/{id}/remedial/{plan_id}/` | Plan + session log |
| 4 | `POST` | `/api/v1/school/{id}/remedial/{plan_id}/sessions/` | Log session attendance |
| 5 | `POST` | `/api/v1/school/{id}/remedial/{plan_id}/reassessment/` | Record re-assessment score |
| 6 | `GET` | `/api/v1/school/{id}/remedial/dept-summary/?dept_id={id}` | HOD dept summary |
| 7 | `GET` | `/api/v1/school/{id}/remedial/export/?year={year}` | Export register PDF |

---

## 11. Business Rules

- At-risk students from B-20 are auto-populated with status "Identified"; enrollment (creating a plan) is a separate manual step by HOD or coordinator
- If at-risk student is not enrolled within 10 days of identification, Academic Coordinator gets a reminder; after 15 days, Principal is notified
- Remedial session attendance is mandatory — if a student misses 3+ sessions, parent is called for a meeting (Class Teacher logs the meeting in A-28)
- Teachers who conduct remedial sessions outside their regular teaching hours may be eligible for school-defined honorarium (configured in Finance module)
- The re-assessment is a school-conducted test, not a CBSE exam; scores are for internal tracking only (not added to board marks)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
