# Group 3 — Division E: Student Attendance
## Pages Master List

> **Division:** E — Student Attendance
> **Group:** 3 — School Portal
> **Total Pages:** 16
> **Roles Served:** Class Teacher (S3) · Subject Teacher (S3) · Administrative Officer (S3) · Academic Coordinator (S4) · Principal (S6) · Parent (read-only via parent portal)

---

## Roles in this Division

| Role | Access Level | Primary Responsibility |
|---|---|---|
| **Subject Teacher** | S3 | Mark period-wise attendance for their own subject |
| **Class Teacher** | S3 | Mark daily attendance; manage leave applications; view class attendance report |
| **Administrative Officer** | S3 | Attendance corrections, medical leave processing, court-order attendance |
| **Academic Coordinator** | S4 | Cross-class attendance overview; shortage alerts; attendance policy enforcement |
| **Principal** | S6 | School-wide attendance dashboard; policy configuration; attendance for board exam eligibility |

---

## Page List

### Cluster 1 — Daily Attendance Marking

| Page ID | File | Title | Priority | Notes |
|---|---|---|---|---|
| E-01 | `e-01-daily-attendance.md` | Daily Attendance (Class Teacher) | P0 | Morning roll call; present/absent/late; SMS/WhatsApp parent alert on absence |
| E-02 | `e-02-period-attendance.md` | Period-wise Attendance (Subject Teacher) | P1 | Per-period marking by subject teacher; feeds E-01 aggregate |
| E-03 | `e-03-attendance-correction.md` | Attendance Correction Register | P1 | Amend wrong marks; all corrections logged with reason + approver |

### Cluster 2 — Leave Management

| Page ID | File | Title | Priority | Notes |
|---|---|---|---|---|
| E-04 | `e-04-leave-application.md` | Student Leave Application | P1 | Parent applies; Class Teacher approves; categories (medical, family, personal) |
| E-05 | `e-05-leave-register.md` | Leave Register | P1 | All approved leaves; medical leave (requires doctor certificate); long absence tracking |
| E-06 | `e-06-late-arrival.md` | Late Arrival Register | P2 | Students arriving after bell; threshold alerts (> 5 late arrivals/month) |

### Cluster 3 — Attendance Analytics

| Page ID | File | Title | Priority | Notes |
|---|---|---|---|---|
| E-07 | `e-07-class-attendance-report.md` | Class Attendance Report | P1 | Monthly/termly class-wise % report; teacher-absent days excluded |
| E-08 | `e-08-student-attendance-report.md` | Student Attendance Report | P0 | Per-student full year attendance; critical for 75% CBSE eligibility |
| E-09 | `e-09-shortage-alerts.md` | Attendance Shortage Alerts | P0 | Auto-alert when student falls below 75% (CBSE) or 85% (school policy) |
| E-10 | `e-10-attendance-analytics.md` | School-wide Attendance Analytics | P1 | Day-wise trends; class comparison; chronic absentee patterns |

### Cluster 4 — Compliance & Eligibility

| Page ID | File | Title | Priority | Notes |
|---|---|---|---|---|
| E-11 | `e-11-exam-eligibility.md` | Exam Attendance Eligibility | P0 | 75% rule for half-yearly/annual; condonation workflow; blocks exam if ineligible |
| E-12 | `e-12-attendance-certificate.md` | Attendance Certificate Generator | P1 | For scholarships, sports nominations, visa applications |
| E-13 | `e-13-cbse-attendance-register.md` | CBSE Attendance Register | P1 | CBSE-format class register printout; required for board inspection |

### Cluster 5 — Special Attendance Scenarios

| Page ID | File | Title | Priority | Notes |
|---|---|---|---|---|
| E-14 | `e-14-event-attendance.md` | Event / Activity Attendance | P2 | Sports day, annual day, excursion — separate from class attendance |
| E-15 | `e-15-holiday-working-day.md` | Holiday & Working Day Manager | P1 | Mark which days are working; feeds attendance % computation; holiday attendance (special drives) |
| E-16 | `e-16-parent-notifications.md` | Parent Absence Notifications | P1 | Auto WhatsApp/SMS on absence; notification log; parent acknowledgements |

---

## Implementation Priority

### P0 — Must-have at launch
- **E-01** Daily Attendance — without this, no attendance data exists
- **E-08** Student Attendance Report — needed for parent view, board exam eligibility
- **E-09** Shortage Alerts — CBSE compliance; without this, schools miss students at risk
- **E-11** Exam Eligibility — hard block for under-75% students; without this, ineligible students appear in exam hall

### P1 — Needed within first month
- E-02, E-03, E-04, E-05, E-07, E-10, E-12, E-13, E-15, E-16

### P2 — Enhancement
- E-06, E-14

---

## Key Regulatory Context

- **CBSE Rule:** Students must have 75% attendance in the subject to be eligible for annual/board exams. School can condone up to 25% shortage with Principal's recommendation (medical/sports/representation reasons). Below 50% — no exam permitted under any circumstance.
- **CBSE 220 Working Days:** Schools must have minimum 220 working days per academic year (Class I–XII). This feeds B-38 Academic Year Planner.
- **RTE:** Attendance register is a legally mandated record; must be maintained class-wise, signed by class teacher daily.
- **Board Exam:** CBSE requires school to certify student attendance as part of LOC (B-33). Students below 75% must be listed with condonation reasons.
- **NEP 2020:** Schools must identify chronic absentees early (< 60% in any month) and initiate counselling/home visit.

---

## Data Dependencies

| Depends On | For |
|---|---|
| C-05 Enrollment | Student roster per class |
| C-10 Class Promotion | Updated class list each year |
| A-10 Academic Calendar | Working days for % computation |
| A-11 Holiday Calendar | Exclude holidays from working days |
| B-07 Timetable | Period-wise schedule for E-02 subject attendance |
| B-33 Board Exam Registration | Attendance % certification for LOC |

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
