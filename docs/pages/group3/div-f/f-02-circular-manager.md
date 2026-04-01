# F-02 — Circular Manager

> **URL:** `/school/circulars/`
> **File:** `f-02-circular-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Communication Coordinator (S3) — draft/send · Academic Coordinator (S4) — approve school-wide · Principal (S6) — approve and sign official circulars · Class Teacher (S3) — distribute to own class (mark distributed)

---

## 1. Purpose

Manages official school circulars — numbered, dated documents sent home with students for parent signature. The Indian school circular is both a communication tool and a legal instrument:
- **Fee circulars** define the amount, due date, and late fee — legally binding on both school and parent
- **Examination circulars** (schedule, syllabus, instructions) — if a student cannot appear due to schedule conflict, the circular is evidence the information was provided
- **Holiday circulars** — parents need advance notice for child-care arrangements
- **Policy circulars** — dress code changes, new rules, co-curricular activity fees — must be signed by parent to become binding
- **CBSE compliance**: Affiliation requires schools to maintain circular issuance records for inspection

Circulars differ from F-01 announcements: circulars are numbered (CIR/YEAR/SEQ), printed on school letterhead, signed by Principal, distributed physically via student diary AND sent digitally.

---

## 2. Page Layout

### 2.1 Header
```
Circular Manager                                    [+ New Circular]  [Export Register]
Academic Year: [2026–27 ▼]

Circulars Issued This Year: 48
Pending Acknowledgement: 3 circulars awaiting parent sign-off
```

### 2.2 Circular Register
```
Circ No.        Title                             Issued      Audience        Status
CIR/2026/048    Annual Exam Schedule (Class X)    22 Mar 26   Class X         ✅ Distributed
CIR/2026/047    Term 2 Fee Circular               1 Mar 26    All parents     ✅ Distributed
CIR/2026/046    PTM Schedule — Secondary          25 Feb 26   Classes VI–XII  ✅ Distributed
CIR/2026/045    Dress Code Update                 20 Feb 26   All parents     ⏳ Signature pending (42%)
CIR/2026/044    Sports Day Invitation             5 Feb 26    All parents     ✅ Complete
```

---

## 3. Create Circular

```
[+ New Circular] → full-page form:

SCHOOL CIRCULAR
───────────────────────────────────────────────────────────────────────
Circular No.: CIR/2026/049  (auto-assigned sequential)
Date: 27 March 2026

To: [Parents of Class XI and XII Students        ]
Re: [Annual Examination Schedule 2026–27         ]

Category:
  ○ Fee / Finance  ● Academic / Examination  ○ Holiday  ○ Event  ○ Policy / Rules
  ○ Health & Safety  ○ Co-curricular  ○ General

Body (WYSIWYG rich text editor on letterhead template):
  ┌─────────────────────────────────────────────────────────────────┐
  │   [School Logo]          [School Name]         [Affiliation No.]│
  │                                                                  │
  │   Circular No.: CIR/2026/049          Date: 27 March 2026      │
  │   To: Parents of Class XI & XII                                 │
  │   Re: Annual Examination Schedule 2026–27                       │
  │                                                                  │
  │   Dear Parent,                                                   │
  │                                                                  │
  │   This is to inform you that the Annual Examination for         │
  │   Classes XI and XII will be conducted as per the schedule...   │
  │                                                                  │
  │   [Table: Subject / Date / Time / Venue]                        │
  │                                                                  │
  │   ______________________                                         │
  │   [Principal Name]                                              │
  │   Principal                                                      │
  └─────────────────────────────────────────────────────────────────┘

Attachments: [+ Add] (syllabus PDF, time table PDF)

Acknowledgement required: ☑ Yes
  Tear-off slip text:
  "I, _____________________ (parent of _________________, Class ___)
   have read and understood Circular No. CIR/2026/049 dated 27 Mar 2026.
   Signature: ____________  Date: ____________"

Distribution:
  ☑ Print (for student diary distribution)
  ☑ WhatsApp PDF to parents
  ☑ Post on F-01 Notice Board
  ☐ Email

Classes: [☑ XI-A  ☑ XI-B  ☑ XII-A  ☑ XII-B]
Copies per class: [Auto: based on class strength]

[Save Draft]  [Preview PDF]  [Submit for Principal Approval]
```

---

## 4. Circular PDF Generation

```
Generated PDF:
  ● School letterhead (auto-populated from school profile)
  ● Sequential circular number
  ● Principal's digital signature image (if registered)
  ● School seal image
  ● Tear-off acknowledgement slip at bottom (if required)
  ● QR code linking to digital version (parents can download original)

Print layout:
  A4 portrait, 1 page (circulars must be concise)
  If > 1 page: second page has only content (no header repeat)
  Tear-off slip: 3 cm at bottom, dotted cut line
```

---

## 5. Distribution Tracking

```
Distribution Status — CIR/2026/049 — Class XI-A (45 students)

Physical distribution:
  ✅ Distributed via student diary: 43/45 students (Class Teacher: Ms. Anita)
  ⬜ Not distributed yet: 2 (Chandana Rao — absent; Vijay S. — absent)
  Distributed on: 27 Mar 2026  by: Ms. Anita Reddy

Digital distribution:
  WhatsApp: 43/45 delivered  ·  2 failed (no valid number)
  Posted on notice board: ✅

Acknowledgement (tear-off slip returned):
  Returned: 18/43 (42%)   Not yet: 25
  Deadline: 30 Mar 2026 (3 days after distribution)
  [Send reminder to non-responding parents]

Per-student acknowledgement tracking:
  Roll 01 — Anjali Das — ✅ Returned 28 Mar 2026
  Roll 02 — Arjun Sharma — ⬜ Not returned
  Roll 03 — Chandana Rao — 🔴 Not distributed (absent)
```

---

## 6. Fee Circular Special Handling

Fee circulars have regulatory requirements:

```
Fee Circular Validation — CIR/2026/047 (Term 2 Fee Circular):

✅ Fee amounts match D-01 Fee Structure (approved 15 Apr 2025)
✅ Due date specified: 31 March 2026
✅ Late fee amount specified: ₹50/month after grace period (as per D-03)
✅ Bank account details (for NEFT) included
⚠️ FRA ceiling check: Tuition fee increase = 8% vs prior year → within 10% FRA ceiling ✅
✅ RTE student exclusion note included ("RTE-admitted students are exempt")

[Approve & Publish]
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/circulars/?year={y}` | Circular register |
| 2 | `POST` | `/api/v1/school/{id}/circulars/` | Create circular |
| 3 | `GET` | `/api/v1/school/{id}/circulars/{circ_id}/` | Circular detail |
| 4 | `POST` | `/api/v1/school/{id}/circulars/{circ_id}/approve/` | Principal approval |
| 5 | `POST` | `/api/v1/school/{id}/circulars/{circ_id}/distribute/` | Mark as distributed (class-wise) |
| 6 | `POST` | `/api/v1/school/{id}/circulars/{circ_id}/acknowledge/{student_id}/` | Record parent acknowledgement |
| 7 | `GET` | `/api/v1/school/{id}/circulars/{circ_id}/ack-status/` | Acknowledgement tracking |
| 8 | `GET` | `/api/v1/school/{id}/circulars/{circ_id}/pdf/` | PDF generation |

---

## 8. Business Rules

- Circular numbers are sequential within the academic year (CIR/YEAR/SEQ); gaps are not permitted — if a circular is cancelled before printing, it is voided (not deleted) with reason noted
- Fee circulars require Academic Coordinator + Principal approval; other circulars require Academic Coordinator only
- A published circular cannot be edited — only a corrigendum (new circular referencing the original) can be issued
- Physical distribution must be completed within 2 school days of issuance; Class Teacher confirms distribution in the system
- Acknowledgement deadline is typically 3 school days after distribution; the system sends a WhatsApp reminder to parents who have not responded
- Circulars are retained for 7 years (financial) or 3 years (general) — classification drives retention period

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
