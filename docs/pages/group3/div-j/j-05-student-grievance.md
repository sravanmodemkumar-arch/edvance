# J-05 — Student Grievance Register

> **URL:** `/school/welfare/grievance/`
> **File:** `j-05-student-grievance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — all grievances · Vice Principal (S5) — handle escalated grievances · Class Teacher (S3) — view own class grievances · Counsellor (S3) — welfare-related grievances · Administrative Officer (S3) — admin/fee grievances

---

## 1. Purpose

A structured mechanism for students and parents to raise concerns about the school's functioning — separate from disciplinary matters (J-04) and POCSO (J-02). Student grievances include academic concerns, fee disputes, facilities complaints, teacher behaviour, and systemic issues.

Regulatory basis:
- **CBSE Affiliation Bye-Laws:** Every school must have a student grievance redressal mechanism
- **NCPCR (National Commission for Protection of Child Rights):** Schools must have a redressal forum; NCPCR accepts complaints directly from students/parents if the school does not resolve
- **RTE Act:** Students admitted under Section 12(1)(c) have specific protections against discrimination — grievances related to RTE admissions are high priority
- **Consumer Protection Act 2019:** Education services are covered; parent can file a consumer complaint for deficiency in services; a documented grievance register shows the school's due diligence

---

## 2. Page Layout

### 2.1 Header

```
Student Grievance Register                           [+ Log Grievance]
Academic Year: [2026–27 ▼]

Pending grievances: 4
  Overdue (SLA breach): 1 ⚠️ (RTE grievance — > 15 days)
Resolved this term: 18
Escalated to NCPCR/DEO: 0 (school resolved before external escalation)
```

### 2.2 Grievance List

```
GRV No.        Date         Complainant         Category          SLA    Status
GRV/2627/001   3 Apr 2026   Parent (Ravi P.)    Fee dispute        7d     ✅ Resolved (5d)
GRV/2627/002   12 Apr 2026  Student (self)      Teacher behaviour  10d    ✅ Resolved (8d)
GRV/2627/003   2 May 2026   Parent (RTE child)  RTE — diff. treat  15d    ⚠️ Overdue (17d)
GRV/2627/004   20 May 2026  Student (self)      Library access     7d     ✅ Resolved (3d)
GRV/2627/005   27 Mar 2026  Parent              Exam result query  10d    🟡 Open (day 1)

SLA by category:
  Fee disputes: 7 days
  Teacher behaviour: 10 days
  RTE-related: 15 days (NCPCR guideline)
  Academic (marks/results): 10 days
  Facilities/infrastructure: 14 days
  General: 14 days
```

---

## 3. Log New Grievance

```
[+ Log Grievance]

Grievance No.: GRV/2627/006 (auto-generated)
Date: [27 March 2026]

Submitted by:
  ● Student (self — via student portal)  ○ Parent  ○ Walk-in (logged by front office)

Complainant: [Arjun S. — XI-A]  ·  Parent: [Mr. S. Sharma]  ·  Contact: [040-XXXXX]

Category:
  ○ Fee dispute / billing error
  ○ Academic: marks, results, evaluation
  ● Teacher behaviour / classroom environment
  ○ Infrastructure / facilities
  ○ Library / sports / lab access
  ○ Exam conduct
  ○ RTE-related (admission, discrimination, fee)
  ○ Transport
  ○ Hostel (if applicable)
  ○ Other: [___________]

Grievance description:
  [During the Chemistry class on 26 March, Mr. Ramesh (Chemistry teacher, XII-A)
   reportedly singled out Arjun in front of the class and said "students like you
   should not be in the science stream — you will never pass Board exams." Arjun
   felt humiliated and has refused to attend Chemistry class today.]

Supporting documents: [No file uploaded]
Anonymous: ● No  ○ Yes — (anonymous grievances receive less follow-up; identity stored but not shown)

Assigned to: [Vice Principal (S5)] — default for teacher behaviour category
SLA: 10 days — resolve by 6 April 2026

Auto-acknowledgement sent to parent/student: ✅ (via F-03 WhatsApp)
  "Your grievance GRV/2627/006 has been registered. We will respond by 6 April 2026."

[Submit Grievance]
```

---

## 4. Grievance Resolution Workflow

```
GRV/2627/006 — Teacher Behaviour — Arjun S. (XI-A)

Step 1: Review (VP)
  Reviewed: 28 March 2026
  VP notes: "Spoke with Mr. Ramesh privately on 28 Mar. He acknowledges the
             comment was inappropriate and regrets the impact. The context was
             frustration with student's recent test performance (54%)."

  Finding: Comment was inappropriate and violates the student's dignity (NCPCR guidelines
           + RTE Section 17 spirit — while not corporal punishment, public humiliation
           is a concern).

Step 2: Action taken
  ☑ Formal counselling with Mr. Ramesh — verbal advisory to maintain professional conduct
  ☑ Mr. Ramesh to apologise to Arjun in a one-on-one conversation (not classroom)
  ☑ Arjun will be allowed to sit at the front of class if he prefers (optional)
  ☑ Academic support offered: extra doubt sessions for Arjun in Chemistry

Step 3: Response to complainant
  Method: ● Call from VP (personal)  ○ WhatsApp  ○ Written
  Content: VP called parent (Mr. Sharma) on 2 April and explained the finding
           and action taken. Parent expressed satisfaction.

  Outcome: ● Satisfied — Resolved  ○ Not satisfied — escalate to Principal

Principal review: Not required (parent satisfied)

Close grievance: ✅ 2 April 2026 (within 10-day SLA)
[Close Grievance]
```

---

## 5. RTE Grievance — Special Handling

```
GRV/2627/003 — RTE Admission Grievance ⚠️ OVERDUE

Student: [RTE child — Class III — admitted under Sec 12(1)(c)]
Parent complaint: "Our child is made to sit separately from general students
  and is not allowed to use the school library."

Category: RTE discrimination — 15-day SLA (NCPCR guidelines)
Status: Overdue by 2 days ⚠️

Finding:
  Investigation (Principal + class teacher): Library restriction was a misunderstanding
  by the library assistant who thought RTE children had "limited privileges."
  There is NO such restriction — RTE students have ALL the same rights as fee-paying students.

Action:
  ☑ Library assistant corrected — all students have equal access ✅
  ☑ Principal issued a written reminder to all staff: RTE students are full students
     of the school with no distinction in access, seating, or facilities
  ☑ Class teacher confirmed child now seated with class ✅

  ⚠️ 2-day SLA breach: Logged
  If parent had escalated to NCPCR, the school would have been called to explain.
  The resolution was substantive; the delay was administrative.

Parent informed: ✅ 19 May 2026 (apologised for delay)

Note: NCPCR can impose penalties on schools for RTE violations including differential
  treatment; maintaining this documented resolution record protects the school.

[Close Grievance — Add SLA breach note]
```

---

## 6. NCPCR / External Escalation Tracking

```
External Escalation Tracker

Criteria for external escalation:
  - Grievance unresolved within SLA + 50% additional time
  - Parent dissatisfied after Principal review
  - RTE-related complaints with systemic concern
  - Parent files NCPCR complaint independently

NCPCR Complaints filed against school: 0 (current year)

If NCPCR contacts school:
  1. DO NOT dismiss or deny — cooperate fully
  2. Pull up the grievance record from J-05
  3. Prepare written response documenting the school's actions
  4. NCPCR has authority to inspect, investigate, and order corrective action
  5. Repeated NCPCR complaints can affect CBSE affiliation renewal

Escalation from consumer forum:
  If a parent files a consumer court complaint (District Consumer Disputes Redressal Commission):
  The J-05 grievance register record showing the school's attempts to resolve is the
  primary defence document. Schools should ensure every grievance has a documented response.
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/welfare/grievance/` | Grievance list |
| 2 | `POST` | `/api/v1/school/{id}/welfare/grievance/` | Submit grievance |
| 3 | `GET` | `/api/v1/school/{id}/welfare/grievance/{grv_id}/` | Grievance detail |
| 4 | `PATCH` | `/api/v1/school/{id}/welfare/grievance/{grv_id}/resolve/` | Resolve grievance |
| 5 | `GET` | `/api/v1/school/{id}/welfare/grievance/overdue/` | SLA-breached grievances |
| 6 | `GET` | `/api/v1/school/{id}/welfare/grievance/student/{student_id}/` | Student's grievance history |
| 7 | `GET` | `/api/v1/school/{id}/welfare/grievance/export/` | Export register (NCPCR/CBSE format) |

---

## 8. Business Rules

- Every grievance receives an auto-acknowledgement within 24 hours with a reference number and resolution deadline
- RTE-related grievances have a 15-day maximum SLA; breach generates an automatic alert to the Principal and is flagged in the CBSE affiliation compliance dashboard (K-01)
- A student can submit a grievance anonymously via the student portal; however, anonymous grievances receive a general response ("we have reviewed the concern") — they cannot receive personalised resolution updates since the identity is withheld
- If a parent files the same grievance at NCPCR before the school's SLA expires, the school must respond to NCPCR while simultaneously resolving the internal grievance — the school cannot say "we need more time" to NCPCR once contacted
- Teacher behaviour grievances: the teacher is not shown the student's identity by default; the VP/Principal handles the inquiry; the teacher is told the nature of the complaint not the complainant (same principle as anti-ragging)
- Grievance records are retained for 5 years post-resolution; RTE-related records are retained for 7 years (matching statutory audit requirements)
- Grievance data is shared with NCPCR on formal request; it is not published or sent to CBSE routinely

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division J*
