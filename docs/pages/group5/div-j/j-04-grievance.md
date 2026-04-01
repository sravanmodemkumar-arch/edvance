# J-04 — Student Grievance & Complaints

> **URL:** `/coaching/student-affairs/grievance/`
> **File:** `j-04-grievance.md`
> **Priority:** P2
> **Roles:** Student Counsellor (K3) · Branch Manager (K6) · Director (K7)

---

## 1. Grievance Register

```
GRIEVANCE REGISTER — AY 2026–27
As of 30 March 2026

  OPEN GRIEVANCES: 4
  RESOLVED THIS MONTH: 8

  ID       │ Student         │ Category          │ Against / Issue           │ Raised     │ Status
  ─────────┼─────────────────┼───────────────────┼───────────────────────────┼────────────┼──────────────
  GRV-0041 │ Priya Reddy     │ Faculty Conduct   │ Faculty dismissive tone   │ 28 Mar 26  │ ⏳ Under review
  GRV-0042 │ Ravi Singh      │ Test Issue        │ Q.14 wrong key (score -2) │ 28 Mar 26  │ ✅ Resolved
  GRV-0043 │ Kiran Naidu     │ Study Material    │ PDF not accessible (online)│ 29 Mar 26 │ ⏳ In Progress
  GRV-0044 │ Divya Sharma    │ Room Change       │ Delayed decision B-08     │ 29 Mar 26  │ ⏳ Pending
  GRV-0045 │ Mohammed R.     │ Fee Issue         │ Hostel fee penalty claim  │ 30 Mar 26  │ 🆕 New

  CATEGORIES:
    Faculty conduct:     12 total this year  (8 resolved, 4 open — 4 active)
    Test/assessment:      8 total  (8 resolved) ✅
    Fee/financial:        6 total  (4 resolved, 2 open)
    Study material/LMS:   4 total  (2 resolved, 2 open)
    Hostel:               4 total  (3 resolved, 1 open)
    Others:               2 total  (2 resolved)
    TOTAL:               36 total  (27 resolved — 75% resolution rate)
```

---

## 2. Grievance Detail

```
GRIEVANCE GRV-0041 — Priya Reddy (TCC-2402)
Category: Faculty Conduct | Raised: 28 March 2026, 4:22 PM

  COMPLAINT:
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │ During the Quant class on 27 March 2026, I asked a question about Caselet   │
  │ DI. Sir (Mr. Suresh Kumar) said "You should know this by now — why do you   │
  │ keep asking basic questions?" in front of the whole class. I felt humiliated.│
  │ Other students also noticed. I am afraid to ask questions in class now.     │
  └──────────────────────────────────────────────────────────────────────────────┘

  TCC'S RESPONSE PROCESS:
    Step 1: Branch Manager informed (confidentially) ✅ — 28 Mar 5 PM
    Step 2: Faculty (Mr. Suresh Kumar) called for private conversation → Scheduled 31 Mar
    Step 3: Student follow-up after faculty conversation → Apr 1
    Step 4: Resolution communicated to student → Apr 2

  INTERIM NOTE TO STUDENT (sent 28 Mar 6 PM):
    "Dear Priya, thank you for raising this. We take all conduct feedback
    seriously. We are reviewing the matter and will respond by April 2.
    Please know that asking questions in class is always encouraged. — TCC"

  FACULTY BRIEFING NOTE (internal — not shared with student):
    "Feedback received from student. Please reflect on classroom communication
    style. Students must feel safe asking questions. No formal action yet."

  STATUS: Under review ⏳ | Owner: Branch Manager
```

---

## 3. Grievance Resolution Workflow

```
GRIEVANCE WORKFLOW

  STAGE 1 — Receipt & Acknowledgement (within 24 hours):
    System auto-sends acknowledgement to student with reference ID
    Branch Manager and Counsellor notified (confidential)
    Expected resolution date communicated to student (5–10 business days)

  STAGE 2 — Investigation (2–5 business days):
    Branch Manager gathers facts (both sides separately — never confrontational)
    Faculty / staff member given a private opportunity to respond
    No public disclosure of complaint during investigation

  STAGE 3 — Resolution:
    Outcome communicated to student (resolution or reason for closure)
    Remedial action if applicable (apology, process change, refund, score correction)
    Documented in grievance register with resolution notes

  STAGE 4 — Escalation (if student unsatisfied):
    Student may escalate to Director within 7 days of Stage 3
    Director reviews and gives final decision (binding)
    No further internal escalation; student may seek external redressal (consumer forum)

  RESOLUTION SLA:
    Standard grievances:  10 business days
    Urgent (safety/POCSO): 24 hours
    Financial:             15 business days
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-affairs/grievances/` | All grievances |
| 2 | `POST` | `/api/v1/coaching/{id}/student-affairs/grievances/` | Submit new grievance |
| 3 | `GET` | `/api/v1/coaching/{id}/student-affairs/grievances/{gid}/` | Grievance detail |
| 4 | `PATCH` | `/api/v1/coaching/{id}/student-affairs/grievances/{gid}/` | Update status or add notes |
| 5 | `POST` | `/api/v1/coaching/{id}/student-affairs/grievances/{gid}/escalate/` | Escalate to Director |
| 6 | `GET` | `/api/v1/coaching/{id}/student-affairs/grievances/analytics/?year=2026-27` | Grievance trend analysis |

---

## 5. Business Rules

- Every grievance receives an acknowledgement within 24 hours of submission; the acknowledgement confirms receipt, provides a reference number, and gives an expected resolution date; a student who does not receive an acknowledgement may assume their complaint was lost or ignored and escalate publicly (social media, education forums); the 24-hour acknowledgement is the single most important step in preventing grievance escalation to external channels; the automated acknowledgement from the system covers this even when no human has reviewed the complaint yet
- Faculty conduct grievances are handled with strict confidentiality; the faculty member is informed of the feedback (not the complaint verbatim) and given a private opportunity to reflect and respond; the investigation is not a public tribunal; the goal is to understand what happened and prevent recurrence, not to punish the faculty; a one-time incident where a faculty member was dismissive but not abusive warrants a private conversation and reflection — formal disciplinary action is reserved for repeated or severe misconduct
- Grievances that allege harassment, gender discrimination, or any POCSO-relevant conduct are immediately escalated to the designated POCSO contact and the Director, bypassing the normal 10-business-day timeline; the Branch Manager is still involved but the investigation and decision authority shifts to the POCSO contact and Director; legal counsel may be sought; the student making such a complaint receives enhanced support including counselling and assurance that no retaliation will occur
- The grievance register's 75% resolution rate (27 of 36) is a KPI reviewed by the Director quarterly; the 25% unresolved cases are not a failure — some are in process (within SLA); "unresolved" in the analytics context means "outstanding past SLA"; the target is 100% resolution within SLA; a resolution rate below 80% within SLA triggers a Branch Manager review of the grievance process; most SLA breaches are in faculty conduct cases, which require more time for careful investigation
- A student who files a grievance must not experience any negative treatment as a result of filing; retaliation against a student for filing a grievance (reduced marks, unfavourable batch treatment, social exclusion by staff) is a serious misconduct that is itself subject to grievance; the Director is the final arbiter on retaliation allegations; TCC's grievance policy, published on the student portal, explicitly states the non-retaliation commitment; this commitment is also included in the faculty employment contract

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division J*
