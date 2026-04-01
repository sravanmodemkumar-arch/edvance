# E-08 — Student Attendance Report

> **URL:** `/school/attendance/reports/student/{student_id}/`
> **File:** `e-08-student-attendance-report.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Class Teacher (S3) — own class · Administrative Officer (S3) — full · Academic Coordinator (S4) — all · Principal (S6) — full · Parent (read-only own child via parent portal)

---

## 1. Purpose

The complete attendance history for a single student — the most detailed attendance view. This is P0 because:
- **CBSE exam eligibility (E-11)** reads directly from this report
- **Board exam registration (B-33)** requires attendance % certification
- **Parent portal** shows this to parents so they can monitor their child
- **Scholarship applications** require certified attendance certificate (E-12) which is computed from this data
- **Court cases** (custody disputes, child welfare) sometimes require school attendance records

The report shows every single working day, the student's attendance status, and computed percentages — across all subjects, monthly, termly, and for the full year.

---

## 2. Page Layout

### 2.1 Student Header Card
```
Arjun Sharma (STU-0001187)  ·  Class XI-A  ·  Roll 02
Academic Year: 2026–27  ·  Class Teacher: Ms. Anita Reddy

Attendance Summary:
Working Days (Apr–Mar): 198  ·  Present: 172  ·  Absent: 22  ·  Late: 4
Overall %: 86.9%  (172 present + 2 on-duty = 174 eligible days)

Status: ✅ Eligible for exam (> 75%)
Risk: Can afford 6 more absences before falling below 75% threshold
Board Exam Status: ✅ Attendance %  certified at 86.9% (as of 27 Mar 2026)
```

### 2.2 Monthly Breakdown Bar Chart (Chart.js)

```
Monthly Attendance %
Apr: 100% ████████████████████████
May:  95% ██████████████████████░
Jun:  91% █████████████████████░░
Jul:  95% ██████████████████████░
Aug:  86% ████████████████████░░░
Sep:  82% ██████████████████░░░░░
Oct:  82% ██████████████████░░░░░  ← dip in Oct (flu)
Nov:  90% █████████████████████░░
Dec:  86% ████████████████████░░░
Jan:  91% █████████████████████░░
Feb:  88% ████████████████████░░░
Mar:  86% ████████████████████░░░ (month in progress)
```

---

## 3. Day-wise Attendance Calendar

```
Academic Year 2026–27 — Day-wise Calendar

APRIL 2026
Mo  Tu  We  Th  Fr  Sa
          1P   2P   3P   4P
 6P   7P   8P   9P  10P  11P
13P  14P  15H  16P  17P  18P
20P  21P  22P  23P  24P  25P
27P  28P  29P  30P

MAY 2026
...

Legend: P=Present  A=Absent  L=Late  H=Holiday  ML=Medical Leave  OD=On-duty  S=Sunday/Off
```

Each day cell is clickable — opens the attendance record for that day (who marked it, what time, any correction history).

---

## 4. Subject-wise Attendance

```
Subject-wise Attendance — 2026–27 (to date)

Subject      Teacher           Periods  Present  Absent  %       Status
Physics      Mr. Arun          86       72       14      83.7%   ✅
Chemistry    Ms. Priya         84       70       14      83.3%   ✅
Mathematics  Ms. Kavitha       88       78       10      88.6%   ✅
English Core Ms. Anita         80       74        6      92.5%   ✅
Phy. Edu.    Mr. Suresh        42       40        2      95.2%   ✅
```

---

## 5. Absence Detail

```
Absence Log — 2026–27

Date       Day   Type             Leave Applied  Reason              Condonation Eligible
05 Aug 2026  Wed  Absent           ✅ Medical     Viral fever         Yes
06 Aug 2026  Thu  Medical Leave    ✅ Medical     Viral fever         Yes
07 Aug 2026  Fri  Medical Leave    ✅ Medical     Viral fever         Yes
15 Sep 2026  Tue  Absent           ❌ No leave    —                   No
22 Oct 2026  Thu  Absent           ❌ No leave    —                   No
23 Oct 2026  Fri  Absent           ❌ No leave    —                   No
...

Total absences: 22
  With medical leave: 8 (condonation eligible)
  On-duty: 2 (excluded from denominator)
  Unexplained absences: 12
```

---

## 6. Condonation Eligibility Preview

```
Condonation Eligibility Analysis

Working days: 198
Present: 172
On-duty (excluded): 2  → effective denominator: 196
Raw attendance %: 172/196 = 87.8%

For CBSE condonation consideration:
  Medical absences: 8 (eligible for condonation)
  Max condone-able: 8 (medical) + 0 (school representation)
  If condonation granted for 8 medical days:
    Effective attendance: (172+8)/(196+0) = 180/196 = 91.8%

Current status: ✅ Already above 75% — condonation not required
Condonation becomes relevant only if raw % falls below 75%.
```

---

## 7. Parent Portal View

Same data but simplified:
```
Attendance — Arjun Sharma (Class XI-A)

📊 This Year: 87% ✅ (172/198 days)
📅 This Month (Mar): 86% (12/14 days so far)

Last 5 absences:
  25 Mar 2026 — Absent (no leave applied)
  22 Mar 2026 — Absent (no leave applied)
  ...

⚠️ Reminder: Minimum 75% attendance required for annual exam.
   Current: 87%  —  You can afford 24 more absences.

[Apply Leave]  [View Full History]
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/students/{student_id}/?year={year}` | Full attendance record |
| 2 | `GET` | `/api/v1/school/{id}/attendance/students/{student_id}/monthly/?month={m}&year={y}` | Monthly breakdown |
| 3 | `GET` | `/api/v1/school/{id}/attendance/students/{student_id}/subject/?year={y}` | Subject-wise attendance |
| 4 | `GET` | `/api/v1/school/{id}/attendance/students/{student_id}/absence-log/?year={y}` | Absence detail log |
| 5 | `GET` | `/api/v1/school/{id}/attendance/students/{student_id}/eligibility/?year={y}` | Exam eligibility + condonation |
| 6 | `GET` | `/api/v1/school/{id}/attendance/students/{student_id}/calendar/?year={y}` | Day-wise calendar data |
| 7 | `GET` | `/api/v1/school/{id}/attendance/students/{student_id}/parent-summary/?year={y}` | Simplified parent view |

---

## 9. Business Rules

- Attendance % = (days present + on-duty days) / (total working days − on-duty days excluded from denominator)
- Medical leave is NOT subtracted from denominator — it is counted as absence, but is eligible for condonation (E-11)
- The denominator is the number of working days the school actually held classes (not the planned 220 days) — adjusted for any school closures, holidays that were added, etc.
- Board exam attendance certification: the system computes attendance as of the date of LOC submission (B-33) — not year-end; schools must maintain 75% up to the board exam date
- Parent can see their own child's attendance only; no access to other students' data (DPDPA — data minimisation)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
