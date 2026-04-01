# M-02 — Academic Performance Analytics

> **URL:** `/school/mis/academic/`
> **File:** `m-02-academic-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full view · Vice Principal (S5) — full view · Academic Coordinator (S4) — full view · HOD (S4) — own department only · Class Teacher (S3) — own class/section only

---

## 1. Purpose

Academic analytics translates raw marks (from B-series modules) into insights for school improvement. This is where patterns are found — a weak subject across multiple classes, a brilliant class in one section vs a struggling peer section, a single teacher whose students consistently underperform, or a subject that dips post-mid-year.

Analytics hierarchy:
1. School-wide performance by subject and class
2. Class/Section comparison (same grade, different sections)
3. Subject performance trend over time
4. At-risk student identification (early warning system)
5. Teacher performance correlation (sensitive — VP/Principal only)
6. Board exam results analysis (CBSE Class X and XII)

---

## 2. School-Wide Subject Performance

```
ACADEMIC ANALYTICS — SCHOOL-WIDE
Academic Year: 2025–26  |  Unit Test 1 (Feb 2026)
Total students assessed: 1,186 (out of 1,240 enrolled — 54 absent/exempted)

SUBJECT PERFORMANCE — SCHOOL-WIDE AVERAGE:
  Subject              Classes     Avg Score   Pass%   Trend vs Last Test
  English              VI–XII       76.3%      97.2%   ▲ +1.8%
  Mathematics          VI–XII       68.4%      88.7%   ▼ -2.1% ⚠
  Science              VI–VIII      74.1%      95.6%   ► Stable
  Physics              IX–XII       65.2%      82.4%   ▼ -3.4% ⚠
  Chemistry            IX–XII       71.8%      90.1%   ► Stable
  Biology              XI–XII       73.2%      92.3%   ► Stable
  Social Science       VI–X         72.8%      96.4%   ▲ +2.3%
  Telugu/Hindi         VI–XII       69.1%      91.2%   ▲ +1.1%
  Computer Science     IX–XII       81.4%      98.8%   ▲ +4.2%

ALERTS:
  🔴 Physics declining (Class XI-A: 58.3%) — investigate [Drill-down]
  🔴 Mathematics school-wide dip — cross-class pattern [Drill-down]
  🟡 Class IX-B English below school average [Drill-down]
```

---

## 3. Section Comparison — Same Grade

```
SECTION COMPARISON — CLASS IX (4 sections, 156 students)

Subject: Mathematics (Unit Test 1, Feb 2026)

  Section   Avg Score  Pass%   Top Score  Fail Count  Teacher
  IX-A       72.4%     94.4%   97/100     5           Mr. Deepak C.
  IX-B       64.8%     85.4%   92/100     11          Mr. Deepak C.
  IX-C       71.1%     91.2%   98/100     6           Ms. Priya M.
  IX-D       68.9%     87.8%   94/100     8           Ms. Priya M.

Observation: IX-B (Mr. Deepak's section B) notably weaker than IX-A (same teacher).
  Analysis: IX-B has 8 students from EWS background (per admission data);
            3 students with SLD (J-07 CWSN); section composition factor.
  Recommendation: Remedial for IX-B bottom 11 students; not a teacher performance issue
  [VP note added: "Composition-adjusted; Deepak's IX-A is top. Action: arrange IX-B remedial."]

SECTION RANKING — All subjects combined (Class IX):
  Rank  Section  Combined Avg  Comment
  1     IX-A     74.2%         ✅ Consistently strong
  2     IX-C     73.0%         ✅
  3     IX-D     70.1%         Borderline
  4     IX-B     66.4%         ⚠ Needs intervention
```

---

## 4. Trend Analysis — Year View

```
TREND ANALYSIS — Class X Mathematics (2024–25 full year)

                  Term 1     MT-1    Term 2    MT-2    Final
  School avg (X)  69.2%     66.8%    71.4%    70.1%   74.2%
  X-A             72.1%     70.4%    74.8%    73.2%   77.4%
  X-B             67.4%     63.1%    69.2%    68.4%   72.1%
  X-C             71.0%     70.2%    72.8%    71.8%   75.6%
  X-D             68.2%     65.8%    70.1%    68.9%   73.8%

Observation: Mid-term dip (MT-1 and MT-2) is a consistent pattern — students
  underperform in mid-terms, recover for finals.
  Analysis: Mid-terms cover more chapters in shorter time; final is more predictable
  (students revise strategically). Pattern is acceptable; watch for outliers.

BOARD EXAM CORRELATION (Class X CBSE 2025):
  Board exam avg (Maths): 76.8%
  Internal Unit Test avg (Maths, same year): 71.4%
  Correlation coefficient: 0.87 (strong positive) ✅
  — Internal assessments are reliable predictors; school's grading is not inflated
```

---

## 5. At-Risk Student Identification

```
AT-RISK STUDENTS — Early Warning System

Criteria triggering at-risk flag:
  🔴 Critical: Score <33% in any subject in last 2 assessments
  🟡 Warning: Score 33–45% in core subject (Maths/Science/English)
  🟡 Warning: Score declining >10% across 2 consecutive assessments
  🟡 Warning: Attendance <75% + any failing grade

AT-RISK LIST — Current (as of Unit Test 1, Feb 2026):

  Student ID  Name*          Class   Risk    Subjects at Risk   Teacher notified
  STU-0421    —              XI-A    🔴      Physics (31%)      VP + Mr. Ravi K. ✅
  STU-0618    —              XII-A   🔴      Chemistry (28%)    VP + Ms. Sunita P. ✅
  STU-0734    —              X-B     🟡      Maths (38%)        Class Teacher ✅
  STU-0891    —              IX-B    🟡      Maths + Hindi      Class Teacher ✅
  STU-1024    —              VII-C   🟡      Maths (39%)        Class Teacher ✅
  [14 students total — full names visible to VP/Principal only; Class Teacher sees own class]

* Student names shown to Principal/VP only; Class Teacher sees their class's at-risk list

ACTION WORKFLOW:
  Notify Class Teacher → Class Teacher initiates parent contact (F-09 diary/phone)
  → If no improvement in 30 days → VP review + remedial classes
  → If no improvement in 60 days → Counsellor referral (J-01 welfare check)
  → Board exam candidates (Class X, XII): tracked monthly from September

[Send bulk notification to Class Teachers of at-risk students]
```

---

## 6. Board Exam Analysis

```
BOARD EXAM ANALYSIS — CBSE 2025

CLASS X RESULTS:
  Appeared: 156  |  Passed: 154 (98.7%)  |  Compartment: 2  |  Distinction: 28

  Subject-wise pass%:
    English:  99.4% ✅  |  Maths: 96.8% ✅  |  Science: 97.4% ✅
    Soc Sci:  98.1% ✅  |  Telugu: 99.4% ✅  |  Second Language pass: 99.4%

  Topper: STU-0208 (name shown to Principal) — 97.4% aggregate
  School highest CGPA: 10 — 4 students
  School average CGPA: 8.6 (vs CBSE national avg 7.8) — above national avg ✅

CLASS XII RESULTS:
  Appeared: 92  |  Passed: 88 (95.7%)  |  Compartment: 4  |  Distinction: 15
  Science stream: 56 appeared — 54 passed (96.4%)
  Commerce stream: 36 appeared — 34 passed (94.4%)

YEAR-ON-YEAR BOARD RESULTS (Class X):
  Year      Pass%    Avg CGPA   Distinctions
  2022–23   97.8%    8.3        19
  2023–24   99.2%    8.5        25
  2024–25   98.7%    8.6        28     ← current year
  Trend: Improving steadily ✅

CBSE MERIT RANKING: School ranked among top 15% in Telangana (CBSE data)
```

---

## 7. Teacher Performance Correlation

```
TEACHER PERFORMANCE — ACADEMIC CORRELATION
[SENSITIVE — VP and Principal only]

This report correlates student performance with individual teachers,
controlling for section composition factors.

Mathematics — Class IX (same subject, 4 sections):
  Teacher        Sections  Avg Score  Adj. Score*  Rating
  Mr. Deepak C.  IX-A, IX-B  68.6%     72.1%       ✅ (IX-B has EWS+CWSN adjustment)
  Ms. Priya M.   IX-C, IX-D  70.0%     70.0%       ✅

Physics — Class XI (declining — deep dive):
  Teacher        Sections  Avg Score  Adj. Score*  Rating
  Mr. Ravi K.    XI-A, XI-B  58.3%     58.3%       ⚠ Below school average
                                                      (no composition factor)
  Mr. Suresh T.  XI-C, XI-D  67.4%     67.4%       ✅

  Observation: Mr. Ravi K.'s sections consistently 8–10% below Mr. Suresh T.'s.
  Pattern: 2nd consecutive year (last year: 61% vs 68%).
  Recommended action: VP classroom observation (L-06) + focused discussion.
  Note: This is NOT a disciplinary flag — it is a development flag.
  [Feeds into L-06 appraisal with context]

* Adj. Score = score adjusted for section composition (EWS%, CWSN count, avg prior performance)
  Methodology: Applied to ensure fair comparison across sections with different profiles.
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/mis/academic/subject-summary/` | School-wide subject performance |
| 2 | `GET` | `/api/v1/school/{id}/mis/academic/section-comparison/?class={grade}` | Section comparison for a grade |
| 3 | `GET` | `/api/v1/school/{id}/mis/academic/trend/?class={grade}&subject={subj}` | Multi-assessment trend |
| 4 | `GET` | `/api/v1/school/{id}/mis/academic/at-risk/` | At-risk student list |
| 5 | `GET` | `/api/v1/school/{id}/mis/academic/board-results/?year={yr}` | Board exam analysis |
| 6 | `GET` | `/api/v1/school/{id}/mis/academic/teacher-correlation/` | Teacher-outcome correlation (restricted) |
| 7 | `POST` | `/api/v1/school/{id}/mis/academic/at-risk/notify/` | Bulk notify teachers of at-risk students |

---

## 9. Business Rules

- Teacher performance correlation data is visible only to VP and Principal — not to the HOD or Academic Coordinator; this prevents it from leaking to peer teachers (who may judge, gossip, or create a hostile environment); it is a development insight, not a punitive measure
- At-risk student lists are visible to the Class Teacher for their own class only; they do not see other classes' at-risk lists; Principal and VP see the full school list
- Section comparison must always be shown with composition context (EWS%, CWSN count, prior performance band of the section); raw ranking without context can unfairly stigmatise sections that have higher proportions of students from disadvantaged backgrounds
- Board exam analysis is a public-facing metric for school reputation; it feeds into the school's website and prospectus; the Principal approves the marketing use of board results (e.g., "top 15% in Telangana") before publication
- At-risk identification triggers a workflow, not just a report; the system sends notifications, logs parent contact attempts, and tracks whether intervention was made; a student who remains at-risk for 60 days without documented intervention is flagged as a safeguarding concern (academic neglect)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division M*
