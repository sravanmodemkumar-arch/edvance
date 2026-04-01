# A-17 — Staff Attendance Overview

> **URL:** `/school/admin/staff/attendance/`
> **File:** `a-17-staff-attendance-overview.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** VP Admin (S5) — full · VP Academic (S5) — view teaching staff · Principal (S6) — view all · Admin Officer (S3) — view

---

## 1. Purpose

Tracks daily attendance of all school staff — teaching and non-teaching. Serves two purposes: operational (ensure all classes are covered today) and HR (monthly attendance feeds into salary computation and leave deduction). In large Indian schools, staff attendance is marked via biometric devices, but EduForge provides a digital fallback for schools without biometrics or for staff away from their registered device.

---

## 2. Page Layout

### 2.1 Header
```
Staff Attendance — 26 Mar 2026 (Today)      [Mark Attendance]  [View History]  [Export Month]
Date: [26 Mar 2026 ▼]     Category: [All ▼]   Department: [All ▼]
```

### 2.2 Today's Summary Strip

| Today | Count | % |
|---|---|---|
| Total Staff | 110 | — |
| Present | 97 | 88.2% |
| Absent (Leave Approved) | 7 | 6.4% |
| Absent (Unauthorized) | 4 | 3.6% |
| On Duty Off-campus | 2 | 1.8% |

---

## 3. Main Sections

### 3.1 Daily Attendance Table

| Name | Dept | Type | Biometric | Override Status | Leave Type | Actions |
|---|---|---|---|---|---|---|
| Ms. Sudha Rani | Science | Teaching | ✅ In: 8:18 AM | — | — | [Mark Late Punch/Out] |
| Mr. Rajan T | Maths | Teaching | ❌ No punch | Manual: Present | — | — |
| Ms. Priya K | Language | Teaching | ⚠️ Late: 9:45 AM | — | — | [Mark Half Day] |
| Mr. Suresh (Guard) | Admin | Non-Teaching | ✅ In: 7:55 AM | — | — | — |
| Mrs. Rani | Science | Teaching | ❌ No punch | Absent (Approved) | CL | — |
| Mr. Ganesh | Maths | Teaching | ❌ No punch | Absent (Unauthorized) | — | [Mark Absent / Allow Late Entry] |

**Attendance states:**
- Present — on time
- Late (> school start time + 15 min grace)
- Half Day (in < 3 hours before end or requested)
- Absent — Leave approved (linked to leave record)
- Absent — Unauthorized (no leave applied or not approved)
- On Duty Off-campus (exam invigilation at another school, training, etc.)
- Holiday/Sunday (auto-set from calendar)

**[Mark Attendance]** button — opens bulk manual marking modal (for days when biometric failed):
- Checkboxes for each staff member: Present / Absent / Late / Half Day / OD
- Submit marks all at once

---

### 3.2 Monthly Attendance Calendar (per staff)

Toggle to see individual staff month view:
- Select staff → month calendar
- Each date: Green (P) · Red (A) · Amber (L) · Orange (Late) · Grey (Holiday)
- Monthly summary: Working days: 24 · Present: 20 · Absent: 2 · Leave: 2 · Total absent (leave + unauth): 4

---

### 3.3 Department-wise Attendance

| Department | Total Staff | Present Today | Absent (Auth) | Absent (Unauth) | % Present |
|---|---|---|---|---|---|
| Science | 12 | 11 | 1 | 0 | 91.7% |
| Maths | 10 | 9 | 0 | 1 | 90.0% |
| Language | 14 | 12 | 1 | 1 | 85.7% |
| Social Studies | 8 | 7 | 1 | 0 | 87.5% |
| Admin/Office | 8 | 7 | 0 | 1 | 87.5% |

---

### 3.4 Substitute Needed Alert

Auto-identified when a teaching staff is absent and has scheduled classes today:

| Teacher | Classes Today | Substitute Arranged | Action |
|---|---|---|---|
| Mr. Rajan T | VI B Math, IX A Math, XI MPC | ❌ Not arranged | [Arrange Substitute] |
| Ms. Priya K | III A English, IV B English | ✅ Ms. Kavitha | — |

**[Arrange Substitute]** → opens substitute picker: shows all staff with free periods matching the absent teacher's periods.

---

## 4. Biometric Integration

If school has biometric device integrated:
- Punch data syncs automatically (webhook or scheduled pull every 30 min)
- Late punches flagged automatically
- Manual overrides recorded with reason (VP Admin approval required for P-to-A changes)

If no biometric:
- VP Admin or Admin Officer manually marks attendance per day
- Must be marked before 11 AM to count as on-time for that day

---

## 5. Monthly Report

**[Export Month]** → CSV with:
- All staff × all days
- Summary row: total present, absent, late, OD
- Formatted for payroll input (accountant uses this for salary processing)

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/staff/attendance/?date={date}` | Daily attendance |
| 2 | `POST` | `/api/v1/school/{id}/staff/attendance/bulk-mark/` | Bulk manual marking |
| 3 | `PATCH` | `/api/v1/school/{id}/staff/attendance/{att_id}/override/` | Override single record |
| 4 | `GET` | `/api/v1/school/{id}/staff/{staff_id}/attendance/?month={month}` | Staff monthly calendar |
| 5 | `GET` | `/api/v1/school/{id}/staff/attendance/dept-summary/?date={date}` | Dept-wise summary |
| 6 | `GET` | `/api/v1/school/{id}/staff/attendance/substitutes-needed/?date={date}` | Absent teachers + classes |
| 7 | `GET` | `/api/v1/school/{id}/staff/attendance/export/?month={month}` | Monthly attendance CSV |
| 8 | `POST` | `/api/v1/school/{id}/staff/attendance/biometric-sync/` | Pull biometric punch data |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
