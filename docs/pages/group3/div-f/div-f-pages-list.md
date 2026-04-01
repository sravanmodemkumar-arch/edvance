# Division F — Communication & PTM — Pages List

> **Group:** 3 — School Portal
> **Division:** F — Communication & PTM
> **Total Pages:** 16
> **Directory:** `docs/pages/group3/div-f/`

---

## Purpose

Manages all outbound and inbound communication between the school and parents/students, inter-staff communication, circular and notice management, and Parent-Teacher Meeting (PTM) scheduling and outcomes. Indian school communication has specific characteristics:
- **WhatsApp is the primary channel** (98% of Indian school parents use WhatsApp; email is secondary)
- **Circular culture:** Printed circulars sent home in student diary for parent signature are legally binding communication
- **PTM compliance:** CBSE schools are required to hold PTMs at least twice per year; results PTM before result declaration is common practice
- **Parent engagement gap:** Many Indian parents (especially in semi-urban/rural areas) engage only via PTM; digital channels are supplementary
- **Language:** Most parents prefer regional language (Telugu/Tamil/Hindi) for routine messages; formal notices remain in English
- **Staff internal communication:** WhatsApp groups are informal but prevalent; EduForge provides formal alternatives (notices, task assignments)

---

## Roles (new to this division)

| Role | Code | Level | Description |
|---|---|---|---|
| Communication Coordinator | S3 | S3 | Manages circulars, announcements, PTM scheduling; usually Admin Officer or designated staff member |
| Class Teacher | S3 | S3 | Communicates with own class parents; PTM host for own class |
| Subject Teacher | S3 | S3 | Sends subject-specific notices (syllabus, exam dates) to own class |
| Academic Coordinator | S4 | S4 | Oversees all communication, approves external communications |
| Principal | S6 | S6 | Signs formal circulars; approves communications going to media or external bodies |
| Parent | Parent Portal | P | Receives all communications; can reply for 2-way interactions |

---

## Pages

| Page ID | Title | URL Slug | Priority | Key Function |
|---|---|---|---|---|
| F-01 | Announcement & Notice Board | `announcements/` | P0 | School-wide announcements visible to all parents and staff |
| F-02 | Circular Manager | `circulars/` | P1 | Create, send, and track printed + digital circulars |
| F-03 | WhatsApp Broadcast Manager | `whatsapp/` | P1 | Template-based WhatsApp broadcasts (Meta Business API) |
| F-04 | SMS & Email Campaigns | `sms-email/` | P2 | Fallback channels; exam alerts; parent email campaigns |
| F-05 | PTM Scheduler | `ptm/schedule/` | P1 | Schedule PTM sessions, assign slots, send invitations |
| F-06 | PTM Conduct & Minutes | `ptm/conduct/` | P1 | During PTM — record discussion points, parent feedback, follow-ups |
| F-07 | PTM Outcome Register | `ptm/outcomes/` | P2 | Post-PTM register of what was discussed, decisions taken |
| F-08 | Parent Feedback & Grievance | `parent-feedback/` | P1 | Structured feedback form; grievance escalation; resolution tracking |
| F-09 | Student Diary / Planner Messages | `diary-messages/` | P2 | Homework/task assigned via diary app; parent signature tracking |
| F-10 | Emergency Alert System | `emergency-alerts/` | P0 | Mass emergency notifications (fire/flood/security/accident) |
| F-11 | Internal Staff Noticeboard | `staff-notices/` | P2 | Internal notices to staff only (not parents); staff acknowledgement |
| F-12 | Event Invitation Manager | `event-invitations/` | P2 | Annual Day, Sports Day, Republic Day — formal invitations to parents |
| F-13 | Parent Communication Log | `comm-log/` | P1 | Per-parent, per-student audit trail of all communications |
| F-14 | Complaint & Grievance Register | `grievances/` | P1 | Formal complaints; POCSO / RTE / DPDPA complaint intake; escalation |
| F-15 | Fee & Exam Reminder Campaigns | `reminder-campaigns/` | P1 | Scheduled automated reminders (fee due, exam schedule, last date) |
| F-16 | Communication Analytics | `comm-analytics/` | P2 | Open rates, response rates, channel effectiveness, engagement trends |

---

## Key Integrations

- **E-09 / E-16:** Attendance shortage alerts feed into F-03 WhatsApp campaigns
- **D-09 / D-10:** Fee defaulter notices trigger F-03 / F-04 campaigns
- **B-11 / B-13:** Exam admit card and result notifications trigger F-03
- **C-05:** Parent phone numbers and email sourced from enrollment
- **A-10:** Academic calendar events trigger F-12 event invitations
- **J-05 (POCSO):** POCSO complaints intake via F-14 grievance register with special handling
- **Meta Business API / Interakt / Wati:** WhatsApp delivery through approved BSP (Business Solution Provider)
- **MSG91 / Exotel:** SMS fallback
- **SendGrid / SES:** Email campaigns

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
