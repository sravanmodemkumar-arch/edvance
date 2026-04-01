# E-09 — Attendance Shortage Alerts

> **URL:** `/school/attendance/shortage-alerts/`
> **File:** `e-09-shortage-alerts.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Class Teacher (S3) — own class alerts · Academic Coordinator (S4) — all classes · Principal (S6) — school-wide view

---

## 1. Purpose

Proactively alerts when students are approaching or below the minimum attendance threshold. This is P0 because without early warning:
- A student reaches 74.9% only in March (too late to recover)
- CBSE blocks the student from the annual exam
- School faces parent complaints and potential legal issues

The alert system has two tiers:
1. **Warning (85% threshold):** Early warning — student still has time to recover
2. **Critical (75% threshold):** CBSE minimum — student risks exam disqualification
3. **Danger (< 65%):** Student cannot recover even with 100% future attendance — exam blocked

Alerts fire automatically when daily attendance is submitted (E-01) — the system recomputes every student's running attendance % and raises alerts immediately.

---

## 2. Page Layout

### 2.1 Header
```
Attendance Shortage Alerts — 2026–27         27 March 2026
School-wide Alerts: 28 students

🔴 Danger (< 65%) — Cannot recover:  3 students
🟠 Critical (65–75%) — At risk:      8 students
🟡 Warning (75–85%) — Watch:        17 students
```

### 2.2 Alert List

```
Filter: [All ▼]  Class: [All ▼]  [Export Alerts]

── 🔴 DANGER — Below 65% — Exam will be blocked ───────────────────────────

Roll  Name          Class  Working Days  Present  %      Max Possible %  Action
02    Chandana Rao  XI-A   198           120    60.6%    75.2% (marginal) [Contact Parent NOW]
08    Vijay S.      X-B    198           118    59.6%    74.0% ← CANNOT reach 75%  [Mark for Block]
15    Meena D.      XII-A  198           115    58.1%    73.1% ← CANNOT reach 75%  [Mark for Block]

── 🟠 CRITICAL — 65–75% — Requires urgent action ──────────────────────────

11    Suresh K.     IX-A   198           142    71.7%    87.5% (possible)  [Alert Sent]
...

── 🟡 WARNING — 75–85% — Early warning ────────────────────────────────────

22    Kavya P.      XI-B   198           165    83.3%    97.0% (safe)     [Monitor]
...
```

---

## 3. Student Alert Detail

Clicking any alert row:

```
Chandana Rao — XI-A — Roll 04 — Attendance Alert

Current:       120/198 = 60.6%  🔴 DANGER
Max possible:  120+32 / 230 = 75.2%  (if present for all remaining 32 days)
Margin:        Very thin — must attend EVERY remaining day

Absence breakdown:
  Without leave (unexplained): 48 days
  Medical (documented): 20 days
  Family leave: 10 days
  Total absent: 78 days

Condonation eligibility:
  Medical 20 days — eligible
  If condonation granted: (120+20)/198 = 70.7% — STILL below 75%
  Principal must apply for special condonation to CBSE (CBSE Circular 2023)

Action History:
  15 Oct 2026: Warning alert sent to parent via WhatsApp ✅
  1 Nov 2026: Class Teacher called parent — discussed (note logged)
  15 Nov 2026: Critical alert — written notice sent (E-10 Demand equivalent)
  1 Dec 2026: Academic Coordinator met parent — committed to improvement
  Now: Still in danger zone

Recommended Actions:
  [Generate Parent Notice — Final Warning]
  [Schedule Parent Meeting with Principal]
  [Apply for CBSE Condonation (Academic Coordinator)]
  [Mark student as Exam Ineligible — Block (Principal approval req.)]
```

---

## 4. Maximum Possible Attendance Calculator

For each at-risk student, the system shows:

```
Max Recovery Calculation — Suresh Kumar (IX-A)

Current: 142/198 = 71.7%
Remaining working days (27 Mar → 31 Mar + 2026–27 year end): 32 days

If present for ALL 32 remaining days:
  (142 + 32) / (198 + 32) = 174/230 = 75.7%  ✅ Can barely recover

If present for 90% of remaining:
  (142 + 29) / 230 = 171/230 = 74.3%  ❌ Below 75%

→ Must attend at least 31 of 32 remaining days to cross 75% threshold
→ Cannot afford even 1 more absence
```

---

## 5. Bulk Alert Actions

```
[Send WhatsApp to All Warning-Level Parents]
[Send WhatsApp to All Critical-Level Parents]  ← separate message; more urgent tone
[Generate Notices for All Danger-Level Students]
[Export Alert List for PTM]
```

WhatsApp message templates:
- Warning: "Dear Parent, your ward [Name]'s attendance is [%] this year. Minimum required is 75%. Please ensure regular attendance. — [School]"
- Critical: "URGENT: [Name]'s attendance is [%] — at risk of exam disqualification. Please contact the class teacher immediately. — [School]"
- Danger: "FINAL NOTICE: [Name]'s attendance is [%]. He/She may be debarred from the annual examination. Please meet the Principal this week. — [School]"

---

## 6. Notification History per Student

```
Chandana Rao — Alert Notification Log

Date        Alert Level  Message Type        Sent To         Acknowledged
15 Oct 2026  Warning      WhatsApp            Father          ✅ Seen
1 Nov 2026   Critical     Phone call          Father          ✅ Committed
15 Nov 2026  Critical     Written notice      Father (signed) ✅ Acknowledged
1 Dec 2026   Critical     WhatsApp            Father          ✅ Seen
15 Dec 2026  Danger       WhatsApp            Father          ⬜ Not seen
1 Jan 2027   Danger       WhatsApp            Father          ⬜ Not seen
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/shortage-alerts/?year={y}` | All shortage alerts |
| 2 | `GET` | `/api/v1/school/{id}/attendance/shortage-alerts/{student_id}/` | Student alert detail + max recovery |
| 3 | `POST` | `/api/v1/school/{id}/attendance/shortage-alerts/notify/` | Send bulk WhatsApp alerts |
| 4 | `GET` | `/api/v1/school/{id}/attendance/shortage-alerts/notification-log/{student_id}/` | Alert history |
| 5 | `GET` | `/api/v1/school/{id}/attendance/shortage-alerts/export/?year={y}` | Export alert list |

---

## 8. Business Rules

- Alerts are recomputed after every E-01 daily attendance submission — not just at month-end
- The "max possible %" calculation accounts for remaining working days in the academic year (from A-10 Academic Calendar, minus already-elapsed days, minus remaining planned holidays)
- Warning threshold (85%) and critical threshold (75%) are configurable per school; CBSE minimum of 75% cannot be set lower — it is a hard floor
- Alert notifications are logged per student; school must be able to demonstrate (in case of parent dispute or board complaint) that they proactively informed parents about attendance shortage
- Principal is responsible for signing any CBSE condonation application for students below 75%; the system generates the condonation application form in E-11

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
