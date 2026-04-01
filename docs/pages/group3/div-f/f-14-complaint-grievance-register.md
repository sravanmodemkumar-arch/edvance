# F-14 — Complaint & Grievance Register

> **URL:** `/school/grievances/`
> **File:** `f-14-complaint-grievance-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Administrative Officer (S3) — intake and log · Academic Coordinator (S4) — resolve academic/attendance complaints · Principal (S6) — formal complaints and escalations · POCSO Designated Person — POCSO category (exclusive access) · Parent — submit via parent portal

---

## 1. Purpose

Formal register of all complaints and grievances received by the school — from parents, students, staff, or external parties. Distinct from F-08 (which is the submission interface); F-14 is the formal register / case management system where complaints are tracked through resolution.

Indian regulatory requirements:
- **CBSE Affiliation Bye-Laws Chapter 8.11:** Schools must maintain a grievance register and produce it during inspection
- **RTE Act Section 32:** Grievance redressal mechanism mandatory; complaints to be disposed within 30 working days
- **POCSO Act Section 21:** Any person who fails to report child sexual abuse knowledge is punishable; school staff receiving a complaint must immediately forward to POCSO DP + police
- **NDMA School Safety Guidelines:** Safety complaints (fire hazard, crumbling infrastructure) must be logged and acted on within 48 hours
- **State School Education Regulations:** Most states require schools to maintain a complaints register and present it to the District Education Officer on demand
- **Consumer Protection Act 2019:** Schools providing fee-based services are subject to consumer protection; formal complaint trail is the school's defence

---

## 2. Page Layout

### 2.1 Header
```
Complaint & Grievance Register                       [+ Log New Complaint]  [Export Register]
Academic Year: [2026–27 ▼]

Open: 5  ·  Resolved: 47  ·  Escalated to External: 1
SLA Compliance: 93% (resolved within 7 days standard / 30 days RTE)
```

### 2.2 Register
```
GRV No.       Complainant     Category        Received      Resolved    SLA     Status
GRV/2026/048  Parent of Ravi  Academic        25 Mar 2026   —           1 Apr   🟡 In Progress
GRV/2026/047  Parent of Sita  Fee             24 Mar 2026   —           31 Mar  🟡 In Progress
GRV/2026/031  Anonymous       Staff Conduct   5 Feb 2026    7 Feb 2026  ✅      ✅ Resolved
GRV/2026/001  Parent of Rohit RTE Benefit     3 Apr 2026    —           3 May   🔴 Escalated → DEO
GRV/2026/044  Student (XII-A) POCSO           ██████████    ██████████  ██████  🔒 POCSO Restricted
```

Note: POCSO entries are masked from general staff view — only POCSO DP and Principal see them.

---

## 3. Complaint Categories & SLA Matrix

```
Category               SLA    Assigned To            Escalation Path
Academic (marks, syllabus) 7 days  Acad. Coordinator → Principal
Fee dispute            7 days    Accountant → Principal
Attendance dispute     3 days    Class Teacher → Acad. Coord
Staff conduct          3 days    Principal (direct)
Infrastructure/Safety  48 hours  Admin Officer → Principal → Trust
Transport              3 days    Transport HOD → Admin Officer
POCSO                  24 hours  POCSO DP → Police → Principal  ← mandatory reporting
RTE benefit            30 days   Principal → DEO (if unresolved)  ← statutory
DPDPA / Data Privacy   30 days   Data Protection Officer (Principal/designated)
Missing records        7 days    Admin Officer → Principal
Anonymous complaint    7 days    Principal reviews and assigns
```

---

## 4. Complaint Detail & Resolution Workflow

```
GRV/2026/048 — Academic Complaint

Status: 🟡 In Progress (Day 2 of 7)

Submitted by: Parent of Ravi Kumar (XI-A)
Contact: +91 9876-XXXXX
Submission method: Parent portal
Received: 25 Mar 2026 10:15 AM

Category: Academic — Marks dispute
Subject: Physics term 2 paper marks incorrect

Description:
  "My son Ravi Kumar's Physics score in the term 2 exam was marked as 42/100
   but I believe there was an error in calculation. The answer sheet shows
   correct answers in Q3 but full marks were not awarded."

Attachments: photo_of_answersheet.jpg (2.1 MB)  [View]

────────────────────────────────────────────────────────────────────
RESOLUTION WORKFLOW
────────────────────────────────────────────────────────────────────
Assigned to: Academic Coordinator (Ms. Prabha)
Assigned on: 25 Mar 2026 10:16 AM (auto)

Step 1: Academic Coordinator reviewed
  "Requesting Mr. Arun (Physics) to re-check the answer sheet for Q3."
  — Ms. Prabha, 25 Mar 2026 11:30 AM

Step 2: Physics teacher response (26 Mar 2026):
  "Q3 answer is partially correct — student gets 5/10 not 8/10.
   Total is correctly 42. No change required."

Step 3: Communicate to parent
  Response drafted: "Dear Mr. Suresh, we have reviewed Ravi's Physics answer sheet...
   Q3 marking is correct per the marking scheme..." [Edit response]

[Mark Resolved & Send Response]  [Escalate to Principal]
[Request Parent Meeting]
```

---

## 5. Anonymous Complaint Handling

```
Anonymous Complaint — GRV/2026/031

Source: Anonymous (submitted via school website contact form)
Category: Staff Conduct
Description: "A teacher in Class VIII-B is regularly making students miss lunch
              for incomplete homework. Students are afraid to report."

Handling:
  → Assigned to Principal (all anonymous complaints go to Principal)
  → Principal investigates discreetly
  → No response to complainant (anonymous — no contact)
  → Outcome: "Principal spoke with Class VIII-B teacher on 7 Feb 2026.
     Behaviour confirmed and counselled. Will monitor."
  → Resolved without disclosure of teacher identity to complainant

[Mark Resolved]  [Escalate to Academic Coordinator]
```

---

## 6. External Escalation Log

```
External Escalation — GRV/2026/001 — RTE Benefit Dispute

Complaint: Parent of Rohit A. (Class I-A) claims school charged Activity Fee
           to an RTE-admitted student (RTE students are fee-exempt).

School response timeline:
  3 Apr 2026: Complaint received
  10 Apr 2026: Fee Accountant reviewed — fee wrongly charged (data entry error)
  12 Apr 2026: Refund issued ₹2,400 to parent (receipt attached)
  15 Apr 2026: Parent escalated to DEO anyway (claimed delay)

DEO escalation response:
  DEO Reference: GVR-2026-DEO-0234
  DEO response deadline: 30 days from complaint (30 Apr 2026)
  School document submission: ✅ Fee refund receipt, ledger extract, RTE register

DEO Resolution (2 May 2026):
  "Matter resolved at school level; refund confirmed. No further action required."

[View DEO Correspondence]  [Archive Escalation]
```

---

## 7. CBSE Inspection Export

```
[Export Register] → CBSE Inspection Format

GRIEVANCE REGISTER — GREENFIELDS SCHOOL — 2026–27
Affiliation No.: AP2000123

Total complaints received: 52
Resolved within SLA: 48 (92%)
POCSO complaints: 1 (handled per POCSO protocol; details in restricted register)
RTE complaints: 1 (resolved; no DEO action required)
Pending: 5

Certified by: [Principal Name], Principal  ·  Date: 27 Mar 2026  ·  Seal: [SCHOOL SEAL]
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/grievances/?year={y}&status={status}` | Grievance register |
| 2 | `POST` | `/api/v1/school/{id}/grievances/` | Log complaint |
| 3 | `GET` | `/api/v1/school/{id}/grievances/{grv_id}/` | Complaint detail |
| 4 | `POST` | `/api/v1/school/{id}/grievances/{grv_id}/resolution/` | Add resolution note |
| 5 | `POST` | `/api/v1/school/{id}/grievances/{grv_id}/close/` | Close with response |
| 6 | `POST` | `/api/v1/school/{id}/grievances/{grv_id}/escalate/` | Escalate externally |
| 7 | `GET` | `/api/v1/school/{id}/grievances/export-register/?year={y}` | CBSE format PDF |

---

## 9. Business Rules

- POCSO category complaints: system immediately alerts POCSO DP + Principal + logs timestamp of notification (mandatory under POCSO Section 19); all other staff are excluded from viewing the case
- RTE category complaints: 30-day SLA tracked by the system; on day 25, a reminder is sent to Principal; on day 30, the system auto-generates a DEO escalation report ready for dispatch
- Anonymous complaints: no acknowledgement is sent (no contact details); but the complaint is investigated and outcomes logged
- Safety/Infrastructure complaints: marked as 48-hour emergency; triggers an immediate notification to Admin Officer + Principal; if unaddressed in 48 hours, system escalates to School Management Trust email
- DPDPA complaints: assigned to the Data Protection Officer (typically the Principal or a designated staff member); must respond within 30 days per DPDPA 2023 Section 13
- All complaint records are retained for 7 years; POCSO records follow court timelines (potentially indefinitely if criminal case is filed)
- The grievance register is an official school document — its authenticity is certified by the Principal on the export PDF

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
