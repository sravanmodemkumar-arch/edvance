# L-06 — Staff Appraisal & Performance

> **URL:** `/school/hr/appraisal/`
> **File:** `l-06-appraisal.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — final ratings; approve appraisal outcomes · Vice Principal (S5) — conduct appraisals, recommend promotions · HR Officer (S4) — manage process · Staff (S3–S5) — self-appraisal + view own rating

---

## 1. Purpose

Annual appraisal of teaching and non-teaching staff — evaluates performance, determines increments beyond standard, and identifies staff for promotion, training, or performance improvement. Effective appraisal:
- Motivates high performers (recognition + faster increment)
- Identifies underperformers for support and improvement plans
- Provides defensible documentation for HR actions (disciplinary, separation)
- Drives professional development needs (feeds into L-07)

---

## 2. Appraisal Cycle

```
Appraisal Cycle — 2025–26 Annual Appraisal

Timeline:
  February 15: Self-appraisal forms sent to all permanent staff
  March 1:     Self-appraisals due back
  March 10–25: VP conducts appraisal interviews
  March 28:    VP submits ratings to Principal
  March 31:    Principal approves; increments above standard determined
  April 1:     Annual increment with appraisal-based differential applied

Self-appraisal completion:
  Submitted: 42/45 teaching ✅  ·  20/22 non-teaching ✅
  Pending: 5 (contacted — due today 27 March)
```

---

## 3. Self-Appraisal Form

```
Self-Appraisal — Ms. Geeta Sharma (TCH-031) — 2025–26

Section A: Teaching effectiveness (40% weight)
  A1. Lesson planning and curriculum coverage:
      "All lessons planned in advance; used NEP 2020 activity-based methods for
       Class X maps and case studies. 100% curriculum covered in both terms."
      Self-rating: 4/5 (Excellent)

  A2. Assessment and feedback:
      "Corrected and returned all tests within 3 school days. Used question
       analysis to identify weak areas for remediation."
      Self-rating: 4/5

  A3. Student outcomes (class results):
      "Class X average: 78% (up from 72% last year). Class IX: 74% (up from 68%)."
      Self-rating: 4/5

Section B: Professional conduct (20% weight)
  B1. Punctuality and attendance:
      "0 LOP days. 2 CL days only. Never late to class."
      Self-rating: 5/5

  B2. Relationship with students/parents:
      "PTM feedback: 96% positive. 1 parent grievance (GRV/2627/006) — resolved."
      Self-rating: 4/5

Section C: Co-curricular and school contribution (20% weight)
  C1. Extra-curricular:
      "Class Teacher IX-B: 0 discipline incidents in my class this year.
       Co-ordinated social science quiz — school level."
      Self-rating: 4/5

Section D: Professional development (20% weight)
  D1. Training attended:
      "1 external workshop (CBSE regional), 1 internal POCSO training."
      Self-rating: 3/5 (could have done more)

Section E: Goals for next year:
  "Complete geography-specific digital content creation for G-09 digital library.
   Attend CBSE orientation for Class X new pattern."

[Submit Self-Appraisal]
```

---

## 4. Appraiser Rating (VP View)

```
Appraisal — Ms. Geeta Sharma — VP Review

Self-rating: 3.8/5 (weighted average)

VP assessment:
  A (Teaching): 4/5 — "Excellent student outcomes; innovative methods; well-prepared"
  B (Professional): 4.5/5 — "Model punctuality; handled parent grievance gracefully"
  C (Co-curricular): 3.5/5 — "Class teacher role done well; quiz was good but limited scope"
  D (Development): 3/5 — "Only 1 external training; encourage more"

VP Weighted Score: 3.85/5

Rating category:
  5.0–4.5: Outstanding
  4.4–3.5: ● Exceeds Expectations
  3.4–2.5: Meets Expectations
  2.4–1.5: Needs Improvement
  < 1.5: Unsatisfactory

Ms. Geeta Sharma: 3.85 → ● Exceeds Expectations

Increment recommendation:
  Standard increment (T-3): ₹2,500
  VP recommended additional merit increment: +₹500 (Exceeds Expectations)
  Total recommended increment: ₹3,000

Principal review:
  [Approve VP rating]  [Modify rating]  [Add comments]

Principal notes: "Concur with VP rating. Ms. Geeta's class X improvement is significant.
  Recommend for Class Coordinator role next year."
  Principal approved: ✅ 30 March 2026

Feedback shared with Ms. Geeta: ✅ 31 March (personal meeting with VP)
```

---

## 5. Performance Improvement Plan (PIP)

```
Performance Improvement Plan — Mr. Vijay P. (TCH-044, Class V)

Appraisal rating: 2.1/5 — Needs Improvement (2nd consecutive year)
Issues:
  1. 5 LOP days in March alone; overall attendance 78% this year
  2. Curriculum coverage: 82% only (18% shortfall in Term 2)
  3. Class V results: Average 52% (school average: 67%)
  4. Parent complaints: 2 this year (J-05 records)

PIP Goals (April–June 2026 — 3 months):
  Goal 1: Attendance ≥95% (no unexplained absences)
  Goal 2: Curriculum coverage 100% by end of Term 1
  Goal 3: Class V average: ≥60% in Term 1 tests

Support provided:
  Observation visits by VP: 2 per month
  Mentoring by HOD Primary: Weekly
  Training: CBSE class management workshop (L-07)

Review date: July 1, 2026 (after 3 months)

  If goals achieved: PIP closed; continue on standard track
  If goals not achieved: Further HR action (formal warning → potential termination)

HR note: PIP is documented and placed on employee file; employee has received a copy
  and signed acknowledgement. PIP is NOT punitive — it is a formal support process.
  Employee has rights: Can have a union/trusted colleague present at review meetings.
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/appraisal/cycle/` | Current appraisal cycle status |
| 2 | `POST` | `/api/v1/school/{id}/hr/appraisal/self/{staff_id}/` | Submit self-appraisal |
| 3 | `POST` | `/api/v1/school/{id}/hr/appraisal/rating/{staff_id}/` | Submit VP rating |
| 4 | `GET` | `/api/v1/school/{id}/hr/appraisal/summary/` | All staff ratings summary |
| 5 | `POST` | `/api/v1/school/{id}/hr/appraisal/pip/{staff_id}/` | Create PIP |
| 6 | `GET` | `/api/v1/school/{id}/hr/appraisal/{staff_id}/history/` | Appraisal history for staff |

---

## 7. Business Rules

- Appraisal ratings feed the annual increment differential; "Outstanding" receives double the standard increment; "Needs Improvement" receives only standard (no merit component); "Unsatisfactory" (2nd year) triggers a formal PIP and potentially salary freeze
- Appraisal records are confidential between the employee, their appraiser (VP), and the Principal; a teacher should not know their colleague's rating
- The PIP must be fair, specific, time-bound, and provide genuine support; a PIP that is designed to fail (unrealistic targets) may be challenged as constructive dismissal
- Staff who disagree with their rating can submit a written representation to the Principal within 15 days; the Principal's decision on the representation is final
- Appraisal documentation (self-appraisal, VP comments, Principal final rating) is stored in the service book (L-11) for the employee's permanent record
- First-year probationary staff: evaluated at the end of probation (6 months) for confirmation; an unfavourable probation review can result in the probation being extended or service being terminated

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
