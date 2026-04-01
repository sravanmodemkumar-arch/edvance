# E-05 — Leave Register

> **URL:** `/school/attendance/leave/register/`
> **File:** `e-05-leave-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Administrative Officer (S3) — full · Class Teacher (S3) — own class view · Academic Coordinator (S4) — full · Principal (S6) — full

---

## 1. Purpose

The consolidated register of all approved student leaves across the school — the administrative record that CBSE inspectors check when they want to verify attendance vs leave documentation. This page also tracks long-absence cases (students absent for 10+ consecutive days without leave) which require home visits per RTE and NEP 2020 norms.

---

## 2. Page Layout

### 2.1 Header
```
Student Leave Register — 2026–27             [Export]  [Long Absence Alerts]
Total Leaves: 284  ·  Medical: 112  ·  Family: 86  ·  On-duty: 24  ·  Personal: 62
Total Leave Days: 842
```

### 2.2 Leave Register Table
| App No. | Student | Class | Type | From | To | Days | Doc | Approved By | Date |
|---|---|---|---|---|---|---|---|---|---|
| LA-2026-048 | Arjun Sharma | XI-A | Family | 28 Mar | 30 Mar | 3 | — | Ms. Anita (CT) | 27 Mar |
| LA-2026-047 | Priya Venkat | XI-A | Medical | 25 Mar | 25 Mar | 1 | ✅ | Ms. Anita (CT) | 25 Mar |
| LA-2026-022 | Rohit Kumar | IX-B | Medical | 5 Feb | 10 Feb | 5 | ✅ | Mr. Ravi (Admin) | 12 Feb |

### 2.3 Filters
```
Class: [All ▼]  Type: [All ▼]  Date: [Mar 2026 ▼]  Duration: [All ▼ / > 3 days / > 7 days]
```

---

## 3. Long Absence Tracker

[Long Absence Alerts] → students absent for 10+ consecutive days:

```
Long Absence Alerts — 2026–27

Student         Class  Last Present  Days Absent  Leave Applied?  Status
Suresh Kumar    IX-A   18 Feb 2026   37 days      ❌ No leave      ⚠️ CRITICAL
Meena Devi      VI-B   5 Mar 2026    22 days      ✅ Medical leave  ✅ Documented
Ravi Nair       VII-A  10 Mar 2026   17 days      ❌ No leave      ⚠️ ACTION NEEDED
```

For each uncontacted long-absence student:

```
Action Required — Suresh Kumar (IX-A) — 37 days absent

Contact attempts:
  20 Feb 2026: Class Teacher called 9876543210 — No answer
  25 Feb 2026: Class Teacher called — Number switched off
  1 Mar 2026:  Admin Officer called — Number switched off
  5 Mar 2026:  Registered letter sent — [Upload proof]

Next step: HOME VISIT scheduled for 10 Mar 2026
  Assigned: Mr. Ramesh (Admin Officer) + Ms. Priya (Class Teacher)
  [Schedule Home Visit]  [Mark as Dropout → C-12]
```

---

## 4. Medical Leave Documentation

For leaves requiring medical certificates:

```
Medical Leave Record — Rohit Kumar (IX-B)

Leave: 5–10 Feb 2026 (6 days) — Typhoid fever
Doctor Certificate:
  Doctor: Dr. Arvind Nair, Sunshine Clinic, Kukatpally
  Date: 5 Feb 2026
  Diagnosis: Enteric fever (Typhoid)
  Rest recommended: 7 days
  [View Certificate PDF]

Certificate verified by: Meera (Admin Officer) on 12 Feb 2026
Condonation eligibility: ✅ Medical leave (eligible for condonation in E-11)
```

---

## 5. Monthly Leave Summary (per class)

```
Class XI-A — March 2026 — Leave Summary

Type          Students  Days
Medical            3      8
Family Function    5     12
Personal           2      3
On-duty            1      4
────────────────────────────
Total             11     27 student-days of absence

Working days in March: 20
Class average attendance: 89.4%
```

---

## 6. Export

[Export] → CBSE leave register format:
- Student-wise list with all leaves, types, supporting documents
- Month-wise summary per class
- Long absence tracking report

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/leave/register/?year={year}&class_id={id}` | Leave register |
| 2 | `GET` | `/api/v1/school/{id}/attendance/leave/long-absence/?threshold_days={n}` | Long absence list |
| 3 | `POST` | `/api/v1/school/{id}/attendance/leave/long-absence/{student_id}/action/` | Log contact attempt / home visit |
| 4 | `GET` | `/api/v1/school/{id}/attendance/leave/register/export/?year={year}` | Export leave register |

---

## 8. Business Rules

- Medical certificates submitted after the leave must be submitted within 5 working days of return — system flags medical leave as "Doc pending" until uploaded
- Long absence tracking (> 10 days): Class Teacher is responsible for first contact attempt; > 15 days: Administrative Officer escalates; > 30 days: Academic Coordinator + Principal decide dropout vs continued on-roll
- RTE student long absences are reported to the state government (OOSC register, C-12) within 15 days
- On-duty leave certificates must be signed by the Sports Teacher or Department Head who authorised the participation — not just a parent note

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
