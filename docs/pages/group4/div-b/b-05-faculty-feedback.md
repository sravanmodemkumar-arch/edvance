# B-05 — Student-Faculty Feedback (Mandatory)

> **URL:** `/college/academic/feedback/`
> **File:** `b-05-faculty-feedback.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Student (S1) — submit feedback (anonymous) · Dean Academics (S5) — view aggregate results · HOD (S4) — view department aggregate (not individual comments) · Principal/Director (S6) — full view · Faculty (S3) — view own aggregate score (not individual responses)

---

## 1. Purpose

Student feedback on faculty teaching quality is mandatory for:
- NAAC accreditation (criterion 2.4 — Teacher Quality)
- NBA accreditation (Programme Outcome assessment)
- Internal HR (appraisal of teaching faculty — sensitive)
- Academic quality improvement (closing the loop)

The feedback system is designed to be:
- **Anonymous** — students cannot be identified from their feedback
- **Constructive** — structured questionnaire with numeric ratings + optional comments
- **Actionable** — aggregate results with specific dimension scores (not just an overall number)
- **Fair** — results shared with faculty only at aggregate level; individual harsh comments not shared verbatim (to prevent retaliatory behaviour)

---

## 2. Feedback Form — Student View

```
FACULTY FEEDBACK — Student Portal
Semester II 2026–27  |  Feedback window: 1–15 April 2027

Rate each faculty member for courses you are enrolled in.
Your feedback is anonymous — your name is NOT attached to responses.

FACULTY: Dr. Anita K. | COURSE: CS201 Data Structures & Algorithms

Rate 1–5 (1=Very Poor, 2=Poor, 3=Average, 4=Good, 5=Excellent):

TEACHING QUALITY:
  Content delivery clarity:                     [1] [2] [3] [●4] [5]
  Pace of teaching (appropriate speed):          [1] [2] [●3] [4] [5]
  Examples and real-world applications:          [1] [2] [3] [●4] [5]
  Encourages questions and participation:        [1] [2] [3] [4] [●5]

PREPARATION & ORGANISATION:
  Comes prepared to class:                       [1] [2] [3] [4] [●5]
  Covers syllabus systematically:                [1] [2] [3] [●4] [5]
  Uses teaching aids (PPT, board, demo) well:    [1] [2] [3] [●4] [5]

ASSESSMENT:
  Mid-term exams were fair and relevant:         [1] [2] [3] [●4] [5]
  Timely return of corrected papers:             [1] [2] [3] [●4] [5]

ACCESSIBILITY:
  Available for doubts (office hours, after class): [1] [2] [3] [4] [●5]
  Respectful and professional in conduct:         [1] [2] [3] [4] [●5]

OVERALL:
  Overall rating for this faculty:               [1] [2] [3] [●4] [5]

OPTIONAL COMMENT (anonymous):
  [Text box — max 300 characters]
  "Very good at explaining algorithms but the pace is slightly fast. Lab sessions are excellent."

[Submit Feedback]  |  [Skip this faculty] ← Skipping counts as non-response

RESPONSE STATUS:
  CS201 (Dr. Anita K.): ⬜ Pending → ✅ Submitted
  CS203 (Mr. Suresh V.): ⬜ Pending
  [Continue to next →]
```

---

## 3. Aggregate Results — Dean Academics View

```
FACULTY FEEDBACK RESULTS — Semester II 2026–27
Generated: 20 April 2027 (after feedback window closed)
Response rate: 273/332 students (82.2%) ✅

FACULTY AGGREGATE SCORES (out of 5.0):

Faculty           Dept  Courses   Responses  Score   Trend
Dr. Anita K.      CSE   CS201     68/78      4.18    ▲ +0.12
Mr. Suresh V.     CSE   CS203     70/78      4.02    ► Stable
Dr. Ramesh M.     CSE   CS205     65/78      3.71    ▼ -0.24 ⚠
Ms. Neeraja R.    HS    HS201     72/78      4.45    ▲ +0.31
Mr. Pradeep T.    EE    EE201     60/78      3.42    ▼ -0.38 ⚠ Low
Dr. Ravi P.       ME    ME201     74/78      4.28    ► Stable
[Full list — 48 faculty]

DEPARTMENT AVERAGES:
  CSE: 3.97  |  EE: 3.55 ⚠  |  ME: 4.21  |  Civil: 4.08  |  ECE: 3.89

DIMENSION SCORES (school-wide):
  Content delivery: 3.94  |  Preparation: 4.21  |  Assessment: 3.86
  Accessibility: 4.12  |  Overall: 3.98

ALERTS:
  ⚠ Mr. Pradeep T. (EE201): Score 3.42 — second consecutive low semester (3.80 last sem)
    Recommended action: Dean Academics discussion + classroom observation
  ⚠ Dr. Ramesh M. (CS205): Declining trend — syllabus coverage also flagged in B-02
    Likely correlated — incomplete syllabus → lower student satisfaction
```

---

## 4. Faculty View — Own Score Only

```
FEEDBACK SUMMARY — Dr. Anita K. (CS201)
[Faculty sees aggregate only — no individual responses]

Your score this semester: 4.18 / 5.0
Department average: 3.97  |  Your rank: 2 / 12 in CSE department ✅

Dimension breakdown:
  Teaching Quality: 4.22
  Preparation: 4.45
  Assessment: 3.98
  Accessibility: 4.12
  Overall: 4.18

Key themes from student comments (anonymised, aggregated by sentiment):
  Positive: "Clear explanations" (mentioned 24×) | "Good lab sessions" (18×)
  Improvement: "Pace too fast" (mentioned 12×) | "More examples needed" (8×)

[These themes are extracted by sentiment analysis — no individual comment is shown]

Reflection note (voluntary, for your records):
  [You may note your own reflections on this feedback for your teaching portfolio]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/feedback/form/?student={id}&semester={sem}` | Get feedback form for student |
| 2 | `POST` | `/api/v1/college/{id}/feedback/submit/` | Submit feedback (anonymous) |
| 3 | `GET` | `/api/v1/college/{id}/feedback/results/?faculty={id}&semester={sem}` | Faculty aggregate score |
| 4 | `GET` | `/api/v1/college/{id}/feedback/department-summary/?dept={dept}` | Department scores |
| 5 | `GET` | `/api/v1/college/{id}/feedback/naac/?criterion=2.4` | NAAC criterion 2.4 evidence |

---

## 6. Business Rules

- Feedback is genuinely anonymous — no student identifier (name, roll number, IP address) is stored with the feedback response; only the response count per faculty per course is verified (for calculating response rate); anonymity is essential for honest feedback
- Faculty cannot view individual comments — only aggregate sentiment themes; individual verbatim comments (even if positive) could be used to identify students if the student used their own writing style or mentioned specific incidents; the system shows only aggregated themes
- A faculty member's feedback score is NOT directly used in salary decisions or termination (that would create perverse incentives for grade inflation and pandering to students); it is used in the annual appraisal as one input (e.g., "faculty development opportunity") alongside classroom observation and course completion
- Response rate <60% makes the feedback statistically unreliable; the system flags surveys with <60% response as "insufficient for reporting"; faculty are not disadvantaged by a low-response survey; instead, the college should investigate why students are not responding (consent, fatigue, portal usability)
- NAAC assessors look for both the feedback system and evidence of "closing the loop" — i.e., did the college do anything about low scores? A faculty member who consistently gets low scores with no documented intervention is a NAAC red flag

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division B*
