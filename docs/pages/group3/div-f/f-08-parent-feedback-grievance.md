# F-08 — Parent Feedback & Grievance

> **URL:** `/school/parent-feedback/`
> **File:** `f-08-parent-feedback-grievance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Administrative Officer (S3) — intake, categorise · Class Teacher (S3) — own class feedback view · Academic Coordinator (S4) — resolve academic grievances · Principal (S6) — escalated grievances, POCSO/RTE complaints · Communication Coordinator (S3) — track SLA · Parent — submit feedback/complaint via parent portal

---

## 1. Purpose

Structured intake and resolution tracking for parent feedback and complaints. Indian school context:
- **Right to feedback:** Parents (especially RTE beneficiaries) have a right to raise issues without fear; schools must demonstrate a formal grievance mechanism
- **CBSE Affiliation Requirement:** Affiliation Bye-Laws mandate a formal grievance redressal mechanism; inspectors look for this during renewal
- **POCSO complaints:** If a parent raises a child protection concern, it must be immediately routed to the POCSO Designated Person (a legally appointed official per POCSO Act 2012) — not treated as a routine grievance
- **RTE complaints:** Parents of RTE-admitted students can raise complaints to the District Education Officer (DEO); schools must respond within 30 days per RTE Section 32
- **DPDPA:** Any complaint involving data privacy must be handled by the school's Data Protection Officer within 30 days
- **Consumer Forum:** If unresolved, parents can approach Consumer Dispute Redressal Commission; a formal grievance trail is the school's defence

---

## 2. Page Layout

### 2.1 Header
```
Parent Feedback & Grievance                          [Submit Grievance (on behalf)]
Academic Year: [2026–27 ▼]

Open Grievances: 5  ·  Resolved This Month: 12  ·  Escalated: 1
Avg Resolution Time: 4.2 days  ·  SLA breaches: 0 (target: resolve within 7 days)

Categories Today: Academic 2 · Fee 1 · Safety 0 · POCSO 0 · RTE 0
```

### 2.2 Grievance Register
```
GRV No.      Parent / Student      Category     Raised      Status        SLA
GRV/2026/042  Parent of Ravi K.    Academic     25 Mar 26   🟡 In Progress  Due 1 Apr
GRV/2026/041  Parent of Sita D.    Fee          24 Mar 26   🟡 In Progress  Due 31 Mar
GRV/2026/040  Parent of Meena D.   Academic     22 Mar 26   ✅ Resolved     3 days
GRV/2026/039  Parent of Vijay S.   Attendance   20 Mar 26   ✅ Resolved     2 days
GRV/2026/038  Parent of Kavya P.   Transport    18 Mar 26   ✅ Resolved     5 days
GRV/2026/001  Parent of Rohit A.   RTE Benefit  3 Apr 2026  🔴 Escalated    SLA breached
```

---

## 3. Submit Grievance (Admin on behalf or Parent Portal)

```
Submit New Grievance

Submitted by: ● Parent (via parent portal)  ○ Staff (on behalf of parent)
Student: [Ravi Kumar — XI-A] (search)
Parent name: Derived from C-20 family linkage: Mr. Suresh Kumar
Contact: +91 9876-XXXXX

Category (select one):
  ○ Academic (marks, syllabus, teaching quality)
  ○ Fee & Finance (overcharging, receipt not issued, refund delayed)
  ○ Attendance (incorrect marking, leave not approved)
  ○ Transport (bus late, driver behaviour, route issue)
  ○ Safety & Infrastructure (playground, food, fire safety)
  ○ Staff Conduct (teacher behaviour, harassment — non-POCSO)
  ○ POCSO (child sexual abuse, inappropriate behaviour) ← IMMEDIATE ESCALATION
  ○ RTE Benefit (admission denial, benefit not received)
  ○ DPDPA / Data Privacy (data shared without consent)
  ○ Other

Subject: [Annual exam marks not matching expected score       ]
Description:
  ┌────────────────────────────────────────────────────────────────┐
  │ My son Ravi Kumar's Physics score in the term 2 exam was      │
  │ marked as 42/100 but I believe there was an error in          │
  │ calculation. I would like re-verification.                     │
  └────────────────────────────────────────────────────────────────┘

Attachments: [Upload supporting documents] (optional)

Assign to: [Academic Coordinator ▼] (auto-assigned by category)
Priority: ● Normal  ○ High  ○ Urgent

SLA: 7 days (standard) or 48 hours (urgent) or 24 hours (POCSO/safety)

[Submit Grievance]
```

---

## 4. POCSO Complaint — Special Handling

```
⚠️ POCSO Category Selected — IMMEDIATE PROTOCOL ACTIVATED

POCSO (Protection of Children from Sexual Offences) Act, 2012:
Every school must have a designated Designated Person (DP) for POCSO complaints.
Complaint must be reported to local police / CHILDLINE within 24 hours (Section 19).

AUTOMATIC ACTIONS TRIGGERED:
  ✅ Confidential alert sent to POCSO Designated Person: Ms. Radha Krishnamurthy
  ✅ Alert sent to Principal (read-only copy)
  ✅ Complaint locked — only DP can access details (not general staff)
  ✅ SLA: 24-hour mandatory first response by DP

DP is notified by: WhatsApp + Email + in-app alert (all three simultaneously)

Standard school grievance process is SUSPENDED for POCSO complaints.
Follow POCSO protocol (J-05 POCSO module).

[The complaint details are now accessible ONLY to the POCSO DP]
[Other staff cannot view the complaint — DPDPA + POCSO confidentiality]
```

---

## 5. Grievance Resolution Workflow

```
Grievance GRV/2026/042 — Ravi Kumar (XI-A) — Marks Dispute

Timeline:
  25 Mar 2026 10:15 AM — Grievance submitted by parent (parent portal)
  25 Mar 2026 10:15 AM — Auto-assigned to Academic Coordinator
  25 Mar 2026 10:16 AM — WhatsApp confirmation sent to parent:
     "We have received your concern (Ref: GRV/2026/042). We will respond within 7 days."

Resolution steps:
  Step 1 (assigned): Academic Coordinator to review marks entry (B-16)
  Step 2: Physics teacher Mr. Arun to re-check answer sheet
  Step 3: If error found → correction in B-16 → updated mark sheet to parent
  Step 4: If no error → explain marking scheme to parent

Current status: Step 2 — In review
Notes: "Mr. Arun confirmed marks are correct. Checking for totalling error."

[Add Internal Note]  [Request info from parent]  [Mark Resolved]  [Escalate to Principal]

Resolution response to parent (on closure):
  "Dear Mr. Suresh Kumar, regarding GRV/2026/042 — We have reviewed Ravi's Physics
   paper. The total was correctly computed. The marks are: Q1=8, Q2=12, Q3=10,
   Q4=12 = Total 42. If you'd like to see the answer sheet, please contact us
   to schedule an appointment. — Academic Coordinator"

[Send Response & Close]
```

---

## 6. RTE Grievance — Special Handling

```
RTE Grievance GRV/2026/001 — RTE benefit not received

Nature: Parent of RTE-admitted student claims school charged development fee
         (RTE-admitted students are exempt from all fees)

Applicable law: RTE Act Section 12(1)(c) + State RTE Rules
Escalation path: School → District Education Officer (DEO) → State → NCPCR

Auto-actions:
  → Assigned to Principal (RTE complaints bypass Academic Coordinator)
  → 30-day resolution SLA (per RTE Section 32)
  → If unresolved in 30 days → DEO escalation report auto-generated

[View RTE Student Profile (C-07)]  [View Fee Ledger (D-07)]  [Generate DEO Report]
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/grievances/?year={y}&status={status}` | Grievance register |
| 2 | `POST` | `/api/v1/school/{id}/grievances/` | Submit grievance |
| 3 | `GET` | `/api/v1/school/{id}/grievances/{grv_id}/` | Grievance detail |
| 4 | `POST` | `/api/v1/school/{id}/grievances/{grv_id}/notes/` | Add internal note |
| 5 | `POST` | `/api/v1/school/{id}/grievances/{grv_id}/resolve/` | Resolve with response |
| 6 | `POST` | `/api/v1/school/{id}/grievances/{grv_id}/escalate/` | Escalate |
| 7 | `GET` | `/api/v1/school/{id}/grievances/analytics/?year={y}` | Resolution analytics |

---

## 8. Business Rules

- POCSO complaints are routed exclusively to the POCSO Designated Person and are not visible to general staff; the school's data security controls must enforce this at the database level (row-level security by category)
- RTE complaints have a statutory 30-day resolution window; system generates a DEO-format escalation letter after day 25 as a warning
- All grievances receive an automatic acknowledgement WhatsApp within 5 minutes of submission (even outside office hours)
- Fee-related grievances require the Accountant (S3) to review the fee ledger (D-07) as part of the resolution workflow
- A grievance cannot be closed without a resolution note visible to the parent — "resolved without reason" is not permitted
- Resolved grievances are retained for 3 years; POCSO and RTE grievances are retained for 7 years
- The Principal receives a monthly grievance summary report automatically on the 1st of each month

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
