# E-07 — Class Attendance Report

> **URL:** `/school/attendance/reports/class/{class_id}/`
> **File:** `e-07-class-attendance-report.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Class Teacher (S3) — own class · Academic Coordinator (S4) — all classes · Principal (S6) — full

---

## 1. Purpose

Provides the Class Teacher and Academic Coordinator with monthly and termly attendance reports for a class. Used for: PTM preparation (showing parents their child's attendance trend), Academic Coordinator's cross-class comparison, Principal's monthly review, and CBSE half-yearly inspection compliance.

---

## 2. Page Layout

### 2.1 Header
```
Class Attendance Report — XI-A — 2026–27
Class Teacher: Ms. Anita Reddy  ·  Students: 38  ·  Working Days so far: 198

View: ● Monthly  ○ Termly  ○ Full Year
Month: [October 2026 ▼]
```

### 2.2 Monthly Report — Class XI-A — October 2026

```
Working Days in October 2026: 22  (Teacher absent: 1 day — substitution provided)

Roll  Name             Oct WD  Present  Absent  Late  %      Trend     Status
01    Anjali Das        22      21        1       0   95.5%   →         ✅
02    Arjun Sharma      22      19        2       1   86.4%   ↓ (-3%)   ✅
03    Bharath Kumar     22      22        0       0  100.0%   ↑         ✅
04    Chandana Rao      22      16        6       0   72.7%   ↓ (-8%)   ⚠️ Alert
05    Dinesh Reddy      22      18        3       1   81.8%   →         ✅
...
38    Zara Ahmed        22      20        2       0   90.9%   ↑         ✅

Class Average: 88.6%  ·  Highest: 100% (Bharath)  ·  Lowest: 72.7% (Chandana)
Students below 75%: 1 (Chandana Rao — Alert sent to parents 18 Oct)
```

### 2.3 Trend Arrows
- ↑ = attendance improved vs last month
- ↓ = attendance dropped vs last month (red if drop > 5%)
- → = stable

---

## 3. Termly View

```
Term 1 (Apr–Sep 2026) — Class XI-A

Working Days: 110

Roll  Name          Present  Absent  Medical  On-duty  %      Status
01    Anjali Das     104        6       2        1    94.5%    ✅
...
04    Chandana Rao    82       28       8        0    74.5%   ⚠️ Below 75% threshold
```

---

## 4. Month-over-Month Chart (Chart.js)

```
Class XI-A — Monthly Attendance %

100% ─
 95% ─       ●───●
 90% ─  ●───●     ●───●
 85% ─                   ●──●
 80% ─
      Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec  Jan  Feb  Mar
```

---

## 5. Subject-wise Class Attendance (from E-02)

```
Subject-wise Attendance — XI-A — Oct 2026

Subject      Periods  Avg Present  Avg %   Low Scorers (< 75%)
Physics        22        35/38    92.1%    0
Chemistry      22        34/38    89.5%    1 (Chandana)
Mathematics    22        36/38    94.7%    0
English        20        37/38    97.4%    0
```

---

## 6. Export

```
[Export PDF — Class Register (CBSE format)]
[Export Excel — Raw data]
[Export PDF — PTM Parent Report (one-page per student summary)]
```

PTM Parent Report (sent to parents at each PTM):
```
STUDENT PROGRESS REPORT — ATTENDANCE
Student: Arjun Sharma | Class: XI-A | Month: October 2026

Working Days: 22
Present: 19 (86.4%)  ·  Absent: 2  ·  Late: 1
Year-to-date: 89.4% (Oct to date: 172/192 days)

[Bar chart of month-wise attendance]

Message from Class Teacher: Arjun's attendance is satisfactory.
One absence was due to medical reason (dental). Please ensure regular attendance.
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/reports/class/{class_id}/?month={m}&year={y}` | Monthly class report |
| 2 | `GET` | `/api/v1/school/{id}/attendance/reports/class/{class_id}/term/?term={t}&year={y}` | Termly report |
| 3 | `GET` | `/api/v1/school/{id}/attendance/reports/class/{class_id}/subject/?month={m}&year={y}` | Subject-wise report |
| 4 | `GET` | `/api/v1/school/{id}/attendance/reports/class/{class_id}/export/?month={m}&year={y}` | Export class register PDF |
| 5 | `GET` | `/api/v1/school/{id}/attendance/reports/class/{class_id}/ptm-report/?month={m}&year={y}` | PTM parent report PDF (all students) |

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
