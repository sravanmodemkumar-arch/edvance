# F-06 — PTM Conduct & Minutes

> **URL:** `/school/ptm/conduct/`
> **File:** `f-06-ptm-conduct-minutes.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Class Teacher (S3) — own class PTM notes · Subject Teacher (S3) — subject meeting notes · Academic Coordinator (S4) — oversee, review all minutes · Principal (S6) — general session notes, condonation meetings

---

## 1. Purpose

Records what actually happened during the PTM — the discussion between teacher and parent, key concerns raised, commitments made, and follow-up actions. This is the bridge between the scheduling (F-05) and the outcome register (F-07).

Why PTM minutes matter for Indian schools:
- **CBSE compliance:** Schools should maintain records of parent-teacher interactions for affiliation inspection
- **Legal protection:** If a parent later disputes that they were "never informed" about their child's academic/attendance problem, the PTM minutes are the evidence that the meeting happened and the issue was discussed
- **Condonation applications (E-11):** The Principal's condonation letter to CBSE cites the school's proactive parent engagement — PTM minutes support this claim
- **Counsellor handoff (J-05):** If a student has a welfare concern identified during PTM, the Class Teacher can flag it here for the school counsellor's follow-up
- **POCSO:** If a parent reveals any child protection concern during PTM, this triggers the POCSO protocol (F-14 grievance with POCSO flag)

---

## 2. During-PTM Interface (Class Teacher)

Class Teacher uses this on a tablet/laptop during the meeting:

```
Annual PTM — 9 March 2026 — Class XI-A (Ms. Anita Reddy)

⏱ Current slot: 9:15 AM – 9:30 AM  (12 min elapsed)  [End Slot]

👤 Arjun Sharma (Roll 02)  ·  Parent: Mr. Rajesh Sharma (Father)
   Attendance: 86.9% ✅   Overall: 72/100 (B grade)   Exam eligibility: ✅

Quick view:
  Physics: 68% attendance ⚠️   English: 94% ✅   Maths: 88.6% ✅

Discussion notes (quick-entry):
  [Template shortcuts ▼]   ← Common phrases: "Parent satisfied with progress" /
                              "Advised to attend extra coaching" / "Fee commitment made"

  ┌──────────────────────────────────────────────────────────────────┐
  │ Father present. Discussed attendance (86.9% overall, Physics 68%)│
  │ Father committed to ensuring Arjun attends all Physics periods.  │
  │ Father happy with Maths performance (88.6%).                     │
  │ Concern: English essay writing weakness — advised extra practice. │
  │ Father asked about JEE coaching — teacher referred to Academic   │
  │ Coordinator.                                                      │
  └──────────────────────────────────────────────────────────────────┘

Follow-up actions:
  ☐ [+ Add action] → "Father to visit Academic Coord for JEE guidance"
     Assigned to: Mr. Rajesh Sharma (Parent)  ·  Due: 15 Mar 2026
  ☐ Monitor Physics attendance — target 75% by Apr 2026
     Assigned to: Ms. Anita (Class Teacher)

Flags:
  ○ Academic concern (refer to coordinator)
  ○ Attendance concern (follow-up required)
  ● None (meeting was satisfactory)
  ○ Welfare concern (refer to counsellor)
  ○ POCSO concern (immediate escalation)

[Save Notes]  [Next Slot →]
```

---

## 3. Absent Parent Notes

For parents who didn't attend their booked slot:

```
Missed Slot — Kavya P. (XI-B) — Parent did not come

Mark as: ● Parent absent  ○ Rescheduled
Reason (select): ○ Work  ○ Transport  ○ No reason given  ● No response

Action:
  ☑ Send follow-up WhatsApp with key discussion points (one-way)
  ☑ Log as "not attended" in PTM register

Pre-fill message for parent (customisable):
  "Dear Parent, we missed you at today's PTM for Kavya P. (XI-B).
   Key points for your awareness:
   - Attendance: 83.3% (monitoring — please ensure no more absences)
   - Academic: Performing well overall; can improve in Social Science.
   Please contact us if you have any concerns. — Ms. [Teacher], XI-B"

[Send WhatsApp Now]  [Skip]
```

---

## 4. General Session (Principal's Opening Address)

```
General Session Notes — Annual PTM 2026

Opening address by Principal [Dr. N. Subramanian]:
  Key points conveyed:
  ✅ Annual exam schedule announced (1 Apr – 30 Apr 2026)
  ✅ Summer vacation: 1 May – 15 June 2026
  ✅ Next academic year fee structure (10% increase — FRA compliant)
  ✅ School infrastructure improvements: new science lab (August 2027)
  ✅ School result: 98.5% pass rate in CBSE Board 2025-26

Parent feedback during general session:
  Q1: Transport route 4 — bus always late (raised by 3 parents)
       → Action: Transport HOD to investigate. Due: 15 Mar 2026
  Q2: Canteen food quality (raised by parent of IX-A student)
       → Action: Hygiene audit to be conducted. Due: 20 Mar 2026
  Q3: Are Saturday classes mandatory?
       → Clarified: Only designated compensatory Saturdays are mandatory.

[Save General Session Notes]
```

---

## 5. Special Meeting — Condonation Zone Students

For students below 75% attendance, a mandatory Principal meeting during PTM:

```
Special Meeting — Attendance Condonation Discussion
Student: Chandana Rao (XI-A)  ·  Attendance: 60.6% 🔴

Meeting between: Principal Dr. N. Subramanian + Mrs. Vimala Rao (Mother)
Date/Time: 9 Mar 2026, 11:30 AM

Discussion:
  Principal explained CBSE rule (75% mandatory for exam)
  Student cannot reach 75% even with 100% remaining attendance
  Principal recommending special condonation application to CBSE (CBSE Circular 2023)
  Medical certificates (20 days) to be attached to application
  Mother to provide remaining medical certificates by 15 Mar 2026

Outcome:
  ● Condonation application will be filed (E-11 → Academic Coordinator)
  Mother acknowledged: "I understand the situation and will provide documents"
  Parent signature obtained: ✅ (acknowledging awareness of exam risk)

[Print Meeting Record]  [Link to E-11 Condonation Application]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/ptm/{ptm_id}/conduct/slots/?class_id={id}` | Slot list for conduct |
| 2 | `POST` | `/api/v1/school/{id}/ptm/{ptm_id}/conduct/slots/{slot_id}/notes/` | Save meeting notes |
| 3 | `PATCH` | `/api/v1/school/{id}/ptm/{ptm_id}/conduct/slots/{slot_id}/notes/` | Update notes |
| 4 | `POST` | `/api/v1/school/{id}/ptm/{ptm_id}/conduct/general-session/` | Save general session notes |
| 5 | `POST` | `/api/v1/school/{id}/ptm/{ptm_id}/conduct/absent-followup/{student_id}/` | Send absent-parent follow-up |
| 6 | `POST` | `/api/v1/school/{id}/ptm/{ptm_id}/conduct/special-meeting/` | Save condonation/special meeting |

---

## 7. Business Rules

- PTM notes are saved in real-time (auto-save every 30 seconds); data loss during a PTM would be disruptive
- Notes are visible to: Class Teacher, Academic Coordinator, Principal — not directly to parents (parents receive a summary via WhatsApp if teacher sends it)
- POCSO flag in any slot's discussion immediately sends a secure notification to the POCSO Designated Person (J-05 module) — the teacher cannot close the flag without the Designated Person acknowledging receipt
- Welfare concern flag sends notification to school counsellor (J-01 Student Welfare module)
- Meeting duration is tracked automatically (slot start → [End Slot] click); if a meeting runs over the allotted time, the next slot parent is alerted automatically: "Your slot is delayed by [N] minutes"
- Notes cannot be deleted after the PTM day ends; corrections can be appended as "[Addendum]" entries

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
