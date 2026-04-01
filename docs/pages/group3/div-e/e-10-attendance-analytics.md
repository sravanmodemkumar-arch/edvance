# E-10 — School-wide Attendance Analytics

> **URL:** `/school/attendance/analytics/`
> **File:** `e-10-attendance-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Coordinator (S4) — full · Principal (S6) — full

---

## 1. Purpose

School-wide analytics view of attendance — used by the Academic Coordinator and Principal for strategic decisions. Answers questions like:
- Which class has the worst attendance this year?
- Are Mondays consistently worse (post-weekend absenteeism)?
- Are certain months worse (festival season, exam-before-absence)?
- Which teacher's class has consistently lower attendance (may indicate a class management issue)?
- What is the chronic absentee count (students missing > 25% of school year)?

---

## 2. Page Layout

### 2.1 KPI Strip
```
School-wide Attendance — 2026–27 (to date, 198 working days)

Overall: 89.4%  ·  Target: 90%  ·  Status: ⚠️ Slightly below target
Students below 75%: 11  ·  Students below 65%: 3  ·  Perfect attendance: 18
```

### 2.2 Class-wise Heatmap

```
Class Attendance % Heatmap — October 2026
(Red < 80%, Amber 80–85%, Yellow 85–90%, Green ≥ 90%)

          Apr   May   Jun   Jul   Aug   Sep   Oct   Nov   Dec   Jan   Feb   Mar
Nursery   97%   96%   95%   97%   95%   94%   96%   —     —     —     —     —
LKG       96%   95%   94%   96%   94%   93%   95%   —
Class I   95%   94%   93%   94%   92%   91%   93%   —
Class V   92%   91%   90%   91%   89%   88%   90%   —
Class VI  90%   89%   88%   89%   87%   86%   87%   —
Class IX  88%   87%   86%   87%   85%   84%   83%   —  ← Dipping
Class X   87%   86%   85%   86%   84%   83%   82%   —
Class XI  86%   85%   84%   85%   83%   82%   80%   —  ⚠️ Watch
Class XII 88%   87%   86%   87%   85%   84%   83%   —
```

---

## 3. Day-of-Week Analysis

```
Attendance by Day of Week — Full Year Average

Monday:    86.2%  ████████████████████████░░░░  (post-weekend dip)
Tuesday:   91.4%  ████████████████████████████
Wednesday: 92.1%  █████████████████████████████
Thursday:  91.8%  █████████████████████████████
Friday:    88.3%  ██████████████████████████░░  (pre-weekend dip)
Saturday:  85.4%  █████████████████████████░░░  (half-day session, optional)

Insight: Monday absence 6% higher than midweek average — consider motivation program.
```

---

## 4. Chronic Absentee Profile

```
Chronic Absentees (< 75% attendance) — 11 students

Class  Count  Avg %   Common Pattern
XI-A    2     71%     Both from same area (bus route 4 issues?)
XI-B    3     68%     Mix of reasons
X-B     2     72%     Sports tournaments (3 on-duty + low general attendance)
IX-A    2     70%     —
Others  2     73%     —

Top absent reasons (chronic absentees):
  Medical / Health issues: 4 students
  Unexplained: 5 students
  Transport (bus route): 2 students  ← Investigate Route 4
```

---

## 5. Teacher Marking Compliance

```
Attendance Marking Compliance — March 2026

Class        Class Teacher         Days marked   Days missed   Compliance
Nursery-A    Ms. Kavya              20/20          0/20         100% ✅
XI-A         Ms. Anita              19/20          1/20          95% ✅
IX-B         Mr. Ravi               18/20          2/20          90% ⚠️
XII-A        Ms. Lakshmi            16/20          4/20          80% ❌ Action needed

Teachers with < 90% marking compliance get an alert sent to Academic Coordinator.
```

---

## 6. CBSE 220 Working Day Progress

```
CBSE 220 Working Days Compliance — 2026–27

Working days conducted (Apr–Mar): 198 / 220
Remaining school days: 2 (28, 29 Mar 2026)
Projected at year-end: 200 working days

⚠️ SHORTFALL: 20 days below CBSE minimum of 220 days

Reason for shortfall:
  Extended Diwali break: 5 days extra
  Flood closure (Oct 2026): 8 days
  Teacher training days: 7 days
  Total: 20 days gap

Remediation:
  School has already conducted 8 Saturday classes (counted as working days)
  Additional required: 12 more working days
  Options: Extend summer break utilisation / Saturday classes

[View CBSE 220-Day Compliance in B-38 Academic Year Planner]
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/analytics/?year={y}` | School-wide KPIs |
| 2 | `GET` | `/api/v1/school/{id}/attendance/analytics/heatmap/?year={y}` | Class × month heatmap |
| 3 | `GET` | `/api/v1/school/{id}/attendance/analytics/day-of-week/?year={y}` | Day-of-week analysis |
| 4 | `GET` | `/api/v1/school/{id}/attendance/analytics/chronic-absentees/?year={y}` | Chronic absentee profile |
| 5 | `GET` | `/api/v1/school/{id}/attendance/analytics/teacher-compliance/?month={m}&year={y}` | Teacher marking compliance |
| 6 | `GET` | `/api/v1/school/{id}/attendance/analytics/220-day-check/?year={y}` | CBSE 220 working day status |
| 7 | `GET` | `/api/v1/school/{id}/attendance/analytics/export/?year={y}` | Export analytics PDF |

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
