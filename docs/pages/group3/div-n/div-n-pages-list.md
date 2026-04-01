# Division N — Parent Portal

> **Group:** 3 — School Portal
> **Division:** N — Parent Portal
> **URL prefix:** `/parent/`
> **Roles added:** Parent/Guardian (S1-P) — child-specific read + limited actions (separate role group from S1 student); Multi-child Parent — parent with 2+ children at the school

---

## Division Purpose

The Parent Portal is the primary digital interface between the school and parents/guardians. It is a parent-facing view — parents see only their own child's data, not any other student's. The portal aggregates data from the school side (E, B, D, F, I, J modules) and presents it in a parent-friendly format.

Design philosophy:
- Mobile-first (most parents use smartphones; Flutter app primary; web as fallback)
- One login, all children (sibling linking supported)
- Read-heavy, limited write (parents view most things; they can apply for leave, book PTM slots, pay fees, raise complaints)
- DPDPA compliant: parents are data principals for their minor child; consent management is in this module
- Language: Hindi, Telugu, English supported (i18n)

---

## Roles

| Role | Access Level | Scope |
|---|---|---|
| Parent/Guardian (S1-P) | Read child's data + limited actions | Own child only |
| Multi-child Parent (S1-P) | Same as above, multiple children | All linked children |

Note: S1-P is a sub-role of S1 (Student + Parent tier). Parents have a separate login from students. A parent cannot view another parent's child's data.

---

## Pages in Division N

| # | File | URL | Title | Priority |
|---|---|---|---|---|
| N-01 | `n-01-parent-dashboard.md` | `/parent/dashboard/` | Parent Home Dashboard | P1 |
| N-02 | `n-02-attendance-view.md` | `/parent/attendance/` | Child's Attendance | P1 |
| N-03 | `n-03-marks-report.md` | `/parent/marks/` | Marks & Report Cards | P1 |
| N-04 | `n-04-fee-payment.md` | `/parent/fees/` | Fee Statement & Payment | P1 |
| N-05 | `n-05-diary-communication.md` | `/parent/diary/` | School Diary & Messages | P1 |
| N-06 | `n-06-transport-tracking.md` | `/parent/transport/` | Bus Tracking (Parent View) | P1 |
| N-07 | `n-07-ptm-booking.md` | `/parent/ptm/` | Parent-Teacher Meeting Booking | P1 |
| N-08 | `n-08-leave-application.md` | `/parent/leave/` | Apply Leave for Child | P1 |
| N-09 | `n-09-school-calendar.md` | `/parent/calendar/` | School Calendar & Events | P1 |
| N-10 | `n-10-grievance.md` | `/parent/grievance/` | Complaint & Grievance | P1 |
| N-11 | `n-11-consent-management.md` | `/parent/consent/` | Consent & Permissions | P1 |
| N-12 | `n-12-documents.md` | `/parent/documents/` | Child's Documents & Certificates | P1 |

---

## Integration Map

Parent Portal reads from school-side modules:
- **A-series:** Student profile, class, section, TC generation
- **B-series + E-09:** Marks, report cards, grade progress
- **D-series:** Fee statement, payment history, outstanding
- **E-01:** Daily attendance record
- **F-05:** PTM schedule
- **F-09:** School diary / homework messages
- **G-series:** Events, school calendar
- **I-series (parent view):** Bus tracking, transport notifications
- **J-series:** Leave applications, grievance
- **K-10:** Consent records (DPDPA)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
