# F-13 — Parent Communication Log

> **URL:** `/school/comm-log/`
> **File:** `f-13-parent-communication-log.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Class Teacher (S3) — own class · Administrative Officer (S3) — all · Academic Coordinator (S4) — all · Principal (S6) — full · Administrative Officer (S3) — log manual calls

---

## 1. Purpose

Unified audit trail of every communication between the school and a specific parent/student — across all channels (WhatsApp, SMS, email, phone call, physical notice). This answers the critical question: "When did we inform the parent, about what, and did they acknowledge?"

Why this is critical for Indian schools:
- **CBSE condonation (E-11):** CBSE asks "did the school inform the parents before the attendance problem became irrecoverable?" — the comm log is the proof
- **Fee dispute (D-10):** Parent claims they were never informed of the due date — the log shows 3 WhatsApp messages and 1 SMS
- **Exam block dispute:** Parent claims the school never warned them about the attendance/academic issue — the log is the school's legal defence
- **NCPCR complaint:** If a parent escalates to NCPCR (National Commission for Protection of Child Rights), the school's communication record is reviewed
- **Consumer forum:** Fee disputes in consumer court require evidence of communication

---

## 2. Page Layout

### 2.1 Header
```
Parent Communication Log                             [Log Manual Communication]
Academic Year: [2026–27 ▼]

Search: [Student name or parent name]
Class: [All ▼]   Channel: [All ▼]   Type: [All ▼]
```

### 2.2 Per-Student Communication Timeline

Searching "Chandana Rao":

```
Chandana Rao (XI-A, Roll 04)  ·  Parent: Mrs. Vimala Rao (+91 9876-XXXXX)

Communication Log — 2026–27 (Chronological, newest first)

Date         Channel    Type                      Sent By          Status
27 Mar 2026  WhatsApp   Attendance danger alert   Auto (E-09)      ✅ Delivered / ⬜ Not seen
15 Mar 2026  WhatsApp   Attendance critical alert Auto (E-09)      ✅ Read (6:14 PM)
9 Mar 2026   In-person  PTM — Principal meeting   Principal (Dr.N) ✅ Parent present
9 Mar 2026   WhatsApp   PTM reminder              Auto (F-05)      ✅ Read
1 Mar 2026   WhatsApp   Attendance critical alert Auto (E-09)      ✅ Read
20 Feb 2026  Phone call Class teacher called       Ms. Anita Reddy  ✅ Connected (logged)
15 Jan 2026  Written    Attendance warning notice  Admin Office     ✅ Parent signed
15 Oct 2025  WhatsApp   Attendance warning        Auto (E-09)      ✅ Read

[View full year]  [Export as PDF]  [Print for CBSE/court]
```

---

## 3. Log Manual Communication

For phone calls, in-person meetings, and physical letters that are not auto-logged:

```
[Log Manual Communication]

Student: [Chandana Rao — XI-A]
Parent: Mrs. Vimala Rao (mother)
Date & Time: [20 Feb 2026] [11:30 AM]

Channel:
  ● Phone call
  ○ In-person meeting
  ○ Physical letter sent
  ○ Physical letter received from parent
  ○ Email (manually sent outside system)

Communication type:
  ○ Academic concern  ● Attendance concern  ○ Fee  ○ Welfare  ○ POCSO  ○ General

Summary:
  ┌──────────────────────────────────────────────────────────────────────┐
  │ Class teacher Ms. Anita Reddy called Mrs. Vimala Rao (mother) to    │
  │ discuss Chandana's attendance (60.6% as of 20 Feb). Mother stated   │
  │ that Chandana had been ill and medical certificates are being        │
  │ obtained. Mother committed to sending certificates by 28 Feb 2026.  │
  │ Call duration: 8 minutes.                                            │
  └──────────────────────────────────────────────────────────────────────┘

Outcome: ● Issue acknowledged by parent  ○ Parent disputed  ○ No answer  ○ Disconnected

Follow-up required: ☑ Yes — "Certificates by 28 Feb 2026"  ·  Due: 28 Feb 2026
Logged by: Ms. Anita Reddy

[Save Communication Log]
```

---

## 4. Export for Legal / CBSE Purposes

```
[Export as PDF] → Generates:

PARENT COMMUNICATION RECORD
Student: Chandana Rao  ·  Class: XI-A  ·  Academic Year: 2026–27
School: Greenfields School  ·  Affiliation: AP2000123

This record has been extracted from EduForge (an accredited school management system)
and reflects all communication between the school and the parents of the above student.

Communication Records:
──────────────────────────────────────────────────────────────────────────
Date         Type                          Status/Outcome
15 Oct 2025  WhatsApp warning (85% thresh) Read by parent 15 Oct 2025, 6:42 PM
20 Feb 2026  Phone call (teacher to parent) Parent acknowledged — committed to docs
1 Mar 2026   WhatsApp critical (75% thresh) Read by parent 1 Mar 2026, 7:15 PM
15 Mar 2026  Attendance warning notice      Parent signed — filed in school records
9 Mar 2026   PTM — Principal meeting        Parent attended (signed PTM register)
27 Mar 2026  WhatsApp danger alert          Delivered — unread as of 27 Mar 2026
──────────────────────────────────────────────────────────────────────────

Certified by: [Principal Name], Principal  ·  Date: 27 Mar 2026  ·  Seal: [SCHOOL SEAL]

This document is generated for submission to: ● CBSE  ○ Court  ○ DEO  ○ Other
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/comm-log/{student_id}/?year={y}` | Student communication timeline |
| 2 | `POST` | `/api/v1/school/{id}/comm-log/{student_id}/manual/` | Log manual communication |
| 3 | `GET` | `/api/v1/school/{id}/comm-log/{student_id}/export-pdf/` | Export for legal/CBSE use |
| 4 | `GET` | `/api/v1/school/{id}/comm-log/class/{class_id}/?type={type}&year={y}` | Class-wise comm log |

---

## 6. Business Rules

- Auto-logged communications (WhatsApp, SMS, email) pull from F-03/F-04/E-16 delivery records — no manual entry needed
- Manual communications (phone calls, physical letters) must be logged by the school staff member within 24 hours of the communication — delayed logging reduces its legal weight
- The log is append-only — entries cannot be edited or deleted; if a correction is needed, a new entry with "Correction to [date] entry:" prefix is added
- For POCSO-flagged students, communication logs involving the POCSO case are visible only to the POCSO Designated Person — they are stored in the same log but with restricted access
- The PDF export carries a timestamp of export generation — courts require this to verify the record was not post-fabricated
- Retention: 7 years post-student exit (or until student turns 21, whichever is later) — aligns with limitation period for civil suits

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
