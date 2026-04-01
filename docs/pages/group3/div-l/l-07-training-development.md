# L-07 — Training & Professional Development

> **URL:** `/school/hr/training/`
> **File:** `l-07-training-development.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HR Officer (S4) — manage training calendar · Academic Coordinator (S4) — academic training needs · Principal (S6) — approve external training, budget · Staff (S3–S5) — apply for training, view own record

---

## 1. Purpose

Manages professional development for all staff. NEP 2020 emphasises continuous teacher development; CBSE mandates certain trainings (POCSO awareness, CBSE orientation programmes, subject-specific workshops). Well-trained teachers deliver better outcomes.

Training types:
- **Mandatory (compliance):** POCSO annual awareness, DPDPA, fire safety, first aid refresher
- **CBSE-sponsored:** Regional orientation programmes, subject-specific workshops, new curriculum implementation
- **School-initiated:** Internal workshops on pedagogy, digital tools, classroom management
- **External (individual):** Teacher attends a conference, seminar, or course at their expense or school sponsorship
- **Online/self-paced:** CBSE i-EXCEL portal, DIKSHA teacher training, Google for Education

---

## 2. Training Calendar

```
Training Calendar — 2026–27

Mandatory Trainings:
  Date         Training                              Target          Status
  22 Jun 2026  POCSO Awareness (annual)              All staff       ⬜ Planned
  22 Jun 2026  DPDPA Awareness (combined session)    All staff       ⬜ Planned
  Jul 2026     Fire Safety & First Aid Refresher     All staff       ⬜ Planned
  Sep 2026     CBSE New Assessment Framework (IX–X)  IX–X teachers   ⬜ Planned

School-Initiated:
  Date         Training                              Target          Status
  24 May 2026  NEP 2020 — Activity-based learning   Primary CT's    ⬜ Planned
  July 2026    Google Classroom + Digital tools     All teaching    ⬜ Planned
  Aug 2026     Effective PTM communication          Class Teachers  ⬜ Planned

External (Approved):
  Date         Training                              Staff           Cost     Status
  5–6 Apr 2026 CBSE Orientation (Chemistry XI–XII)  Ms. Sunita      ₹2,500   ✅ Approved
  15 May 2026  Cambridge Assessment (IGCSE Methods) Mr. Ravi K.     ₹8,000   ⬜ Pending approval

Completed this year:
  22 Jun 2025  POCSO Awareness ✅ (85/87 staff)
  15 Oct 2025  CBSE Mathematics workshop ✅ (3 maths teachers)
  Nov 2025     Google for Education training ✅ (18 teachers)
```

---

## 3. Training Record — Individual Staff

```
Training Record — Ms. Geeta Sharma (TCH-031)

Mandatory compliance training:
  Year    POCSO Awareness    DPDPA/Data Privacy  Fire Safety
  2022    ✅ Jun 2022        N/A                  ✅ Jun 2022
  2023    ✅ Jun 2023        N/A                  ✅ Jun 2023
  2024    ✅ Jun 2024        N/A                  ✅ Jun 2024
  2025    ✅ Jun 2025        ✅ Jun 2025           ✅ Jun 2025
  2026    ⬜ Planned Jun 2026

Professional development:
  Oct 2025: CBSE Regional Orientation (Social Science — New Pattern) — 2 days ✅
  Mar 2025: Storytelling in Social Science (internal workshop) ✅
  May 2024: Classroom management — 1-day workshop (external) ✅

CEP (Continuing Education Points):
  CBSE has introduced a CEP system for teacher continuous development.
  Ms. Geeta: 18 CEP points this year ✅ (target: 12 per year — above target)

Training needs (from L-06 appraisal):
  "Could have done more external training" (VP feedback)
  Recommended: 1 more external training in 2026–27 (academic content area)
```

---

## 4. External Training Approval

```
External Training Application — Mr. Ravi Kumar (TCH-040)

Event: Cambridge Assessment — IGCSE Methodology Workshop
Organiser: Cambridge Assessment International Education
Dates: 15–16 May 2026 (2 days)
Location: Bangalore (travel required)

Cost:
  Registration: ₹5,000
  Travel (train): ₹2,500
  Accommodation (1 night): ₹2,500
  Total: ₹10,000

School sponsorship requested: ● 100%  ○ 50%  ○ None (own expense; paid leave granted)
Justification: "CBSE schools are increasingly seeing IGCSE-returning students; exposure
  to IGCSE methodology will help in differentiating instruction."

Impact on teaching:
  Classes affected: 2 days — Class XI Physics + XII Physics
  Substitute arranged: Mr. Suresh T. (available) ✅

Approved by VP: ✅ 20 March 2026
Approved by Principal: ⏳ Pending (budget: ₹10,000 — within VP referral limit is ₹5,000;
  exceeds limit → Principal must approve)

[Principal approve/reject]

On return (mandatory):
  ☑ Submit report on training (1-2 page summary)
  ☑ Share learning with other teachers (15-min team meeting presentation)
  ☑ Certificate uploaded to L-07 training record
```

---

## 5. CBSE Teacher Training Programmes

```
CBSE Training Ecosystem — School's Participation

CBSE i-EXCEL Portal (https://cbseit.in):
  Platform for teacher orientation for new curriculum/policy changes
  Mandatory: Completion for all teachers teaching revised subjects
  Status 2025–26:
    Social Science (new pattern Class X): 4 teachers — 4/4 completed ✅
    Mathematics (competency-based): 5 teachers — 5/5 ✅
    Science new NCERT: 3 teachers — 3/3 ✅

CBSE Regional Orientations:
  School sends 2–3 teachers per year to regional CBSE orientations
  Subjects covered rotate (CBSE announces schedule each year)
  2025–26: Chemistry + Social Science orientations attended ✅

DIKSHA (Digital Infrastructure for Knowledge Sharing):
  NEP 2020 platform; teacher training modules
  Teachers encouraged to complete NISTHA (National Initiative for School Heads and Teachers' Holistic Advancement) modules
  Status: 8 teachers completed NISTHA certification this year
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/training/calendar/` | Training calendar |
| 2 | `POST` | `/api/v1/school/{id}/hr/training/calendar/` | Add training event |
| 3 | `GET` | `/api/v1/school/{id}/hr/training/staff/{staff_id}/` | Individual training record |
| 4 | `POST` | `/api/v1/school/{id}/hr/training/application/` | Apply for external training |
| 5 | `PATCH` | `/api/v1/school/{id}/hr/training/application/{id}/approve/` | Approve training request |
| 6 | `POST` | `/api/v1/school/{id}/hr/training/attendance/{event_id}/` | Mark attendance for training event |
| 7 | `GET` | `/api/v1/school/{id}/hr/training/compliance-status/` | Mandatory training completion status |

---

## 7. Business Rules

- POCSO awareness training is annually mandatory for all staff; a staff member who misses the session must complete a makeup within 30 days; missing 2 consecutive years is an HR flag that surfaces in the K-05 compliance module
- External training sponsored by the school (>₹5,000) requires the employee to serve the school for a minimum of 1 year after training; if they leave before that, a proportional recovery is made from the final settlement (standard "clawback" clause in appointment letter)
- Training budget is part of the school's annual budget; the HR Officer proposes the training budget in April; the Principal approves; mid-year training expenses above ₹5,000 require Principal case-by-case approval
- On returning from any external training, the employee must submit a brief report and share learning with colleagues; this ensures training investment multiplies across the staff; reports are filed in the training record
- CBSE orientation completion certificates must be uploaded to the training record; they are shown during CBSE inspection as evidence of teacher development
- NEP 2020 emphasis: schools that can show structured teacher development (training log with completion certificates) fare better in CBSE inspection; inspectors specifically ask about professional development initiatives

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
