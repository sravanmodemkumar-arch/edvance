# N-08 — Apply Leave for Child (Parent View)

> **URL:** `/parent/leave/`
> **File:** `n-08-leave-application.md`
> **Template:** `parent_portal.html`
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P)

---

## 1. Purpose

Parents apply for planned leave for their child through the portal instead of sending a written note. The application goes to the Class Teacher for approval, is linked to E-01 (attendance module), and maintains a proper record. This eliminates forged leave notes and ensures every absence is accounted for.

Retroactive leave applications (post-absence) are also supported — when a child was unexpectedly absent, the parent can submit a reason retroactively, which the CT can approve and convert the absence from "unnotified" to "approved/condoned".

---

## 2. Leave Application Form

```
LEAVE APPLICATION — Rahul Rao (Class X-A)

PLANNED LEAVE:

  Reason category:
    ○ Family function (wedding, ceremony)
    ● Medical (doctor/hospital visit)
    ○ Personal (family travel, other)
    ○ Religious observance

  From date: 15 April 2026 (Wednesday)
  To date:   16 April 2026 (Thursday)
  Number of school days: 2 days

  Details: "Rahul has a dental procedure on 15 April (orthodontic surgery at Nims,
            Hyderabad). Recovery expected 1 day — returning 17 April."

  Attach document (optional): [Appointment letter — upload PDF/photo]
    dental_appointment_15apr.pdf ← attached ✅

  Request to collect missed work:
    "Please ask class friends / post homework on diary — Rahul will complete."

  [Submit Leave Application]

After submission:
  Application sent to: Mr. Deepak C. (Class Teacher, X-A)
  Expected response: Within 24 hours (school day)
  WhatsApp confirmation: Sent ✅

  LEAVE APPLICATION STATUS: Pending CT approval ⏳
```

---

## 3. Retroactive Leave Application (Post-Absence)

```
RETROACTIVE LEAVE — Rahul was absent 12 March 2026 (unnotified)

Parent notification received: "Rahul was marked absent on 12 March.
  Please provide a reason. [Submit explanation →]"

PARENT RETROACTIVE SUBMISSION:
  Date of absence: 12 March 2026
  Reason: "Rahul had sudden fever (102°F) in the morning. We took him to a clinic.
            Fever resolved by evening — he returned next day."
  Document: fever_12march.jpg (clinic bill) ← attached

  [Submit retroactive application]

CLASS TEACHER VIEW (after submission):
  Approval options:
    ● Approve — change absence to "Medical leave (condoned)"
    ○ Reject — absence remains "Unnotified/LOP"
    ○ Acknowledge only — note reason but keep as absent (no penalty, no LOP)

  CT action: Approved ✅ — Entry updated in E-01
  Parent notification: "Rahul's absence on 12 March has been condoned as Medical Leave."
```

---

## 4. Leave Balance View

```
LEAVE STATUS — Rahul Rao (2025–26)

Leave Type    Entitlement  Used  Available  Notes
─────────────────────────────────────────────────────────────────────────────
Approved      (no limit)    7    —         Medical + family (all condoned) ✅
Unnotified    0            16   —         ⚠ 16 unnotified absences (retroactive pending: 5)
LOP           0             0   —         No Loss of Pay applied ✅

ATTENDANCE IMPACT:
  Total absences: 23
  Approved / condoned: 7 (after retroactive processing)
  Unnotified (not yet explained): 11 (parent can still submit for 12 ← with CT's discretion)
  CBSE eligibility: 89.5% ✅ (unaffected by leave type — CBSE counts all absences)

Note: CBSE 75% threshold counts ALL absences regardless of reason.
  Approved/medical leave reduces welfare risk but does NOT reduce CBSE absence count.
```

---

## 5. Leave History

```
LEAVE HISTORY — Rahul Rao (2025–26)

  Date(s)        Days  Type               Status     CT Note
  15–16 Apr 2026  2    Medical (planned)  Pending ⏳  —
  4 Feb 2026       1   Family (approved)  Approved ✅  "Occasion noted"
  12 Mar 2026      1   Medical (retro)    Approved ✅  "Fever — condoned"
  [23 total absences — 7 approved, 16 unnotified (12 with retroactive in progress)]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/leave/apply/` | Submit leave application |
| 2 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/leave/status/` | Leave balance and status |
| 3 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/leave/history/` | Leave history |
| 4 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/leave/retroactive/` | Submit retroactive explanation |
| 5 | `DELETE` | `/api/v1/parent/{parent_id}/child/{student_id}/leave/{leave_id}/` | Cancel pending application |

---

## 7. Business Rules

- Leave applications are not auto-approved; Class Teacher must explicitly approve; the system allows CT to set a standing rule ("auto-approve medical leave with attachment up to 3 days") but this is CT's discretion, not a default
- A leave application must be submitted at least 1 school day in advance for planned leave; same-day applications are accepted but marked "urgent — CT to review immediately"; retroactive applications can be submitted up to 7 calendar days after the absence
- Attaching a supporting document (medical slip, appointment letter) is strongly encouraged but not mandatory; CT can approve without a document based on trust; however, for CBSE condonation cases (attendance near 75%), documentation is essential
- Repeated unnotified absences without retroactive explanation (>5 in a term) trigger a welfare flag (J-11) — the system prompts the Class Teacher to check on the student's welfare; this safeguard ensures that chronic unexplained absence is not just an attendance management issue but a potential welfare concern
- RTE students' absences are handled identically to fee-paying students — RTE students have the same attendance obligations; the school cannot discriminate in attendance management based on fee status (RTE Act requires non-discriminatory treatment)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
