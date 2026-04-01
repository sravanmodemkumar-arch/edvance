# A-11 — Holiday & Leave Calendar

> **URL:** `/school/admin/calendar/holidays/`
> **File:** `a-11-holiday-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full · VP Admin (S5) — full · VP Academic (S5) — view · Admin Officer (S3) — view

---

## 1. Purpose

Dedicated management page for the school's holiday calendar and leave policy. While A-10 (Academic Calendar) shows all events, this page focuses specifically on holiday management and the leave entitlement rules that govern staff leave requests. It is the reference source for staff when they apply for leave and for the office when processing leave approvals.

---

## 2. Page Layout

### 2.1 Tab Bar
```
[School Holidays] [Staff Leave Policy] [Leave Balance Summary] [Leave Encashment Register]
```

---

## 3. Tab: School Holidays

**Holiday list for the academic year:**

| Date | Day | Holiday Name | Type | Board Coverage | Gazette Ref |
|---|---|---|---|---|---|
| 14 Apr 2025 | Mon | Dr. B.R. Ambedkar Jayanti | National (Central) | All boards | — |
| 1 May 2025 | Thu | Maharashtra/Gujarat Day (TS: holiday if so declared) | State | State-specific | GO No: — |
| 15 Aug 2025 | Fri | Independence Day | National | All boards | — |
| 25 Dec 2025 | Thu | Christmas | National (Central) | All boards | — |
| 26 Jan 2026 | Mon | Republic Day | National | All boards | — |
| … | … | … | … | … | … |

**Holiday types:**
- National Holiday (Central Government — Gazette of India)
- State Holiday (State Government — applicable state)
- School Holiday (declared by institution — Annual Day, Sports Day, etc.)
- Board Holiday (declared by CBSE/ICSE regional office for inspections, result days etc.)
- Emergency Closure (declared on same day — civic unrest, flooding, etc.)

**[+ Add Holiday]** drawer (400px):
- Date, name, type, applicable to (all / specific staff / specific students)
- Gazette reference no (for official holidays)
- [Notify parents/staff toggle] with advance notice setting

**[Import State Holidays]:** Pulls from EduForge's pre-loaded state government holiday list for the school's state (based on institution profile). School can select/deselect before importing.

**Year Total:**
```
National: 3 · State: 8 · School: 6 · Emergency: 0 · Total: 17 holidays
Working Days: 220 (CBSE minimum met ✅)
```

---

## 4. Tab: Staff Leave Policy

Leave types and entitlements as per Indian school staff service rules.

| Leave Type | Code | Entitlement (per year) | Carry Forward | Notes |
|---|---|---|---|---|
| Casual Leave | CL | 12 days | No (lapse at year end) | Max 3 consecutive days; no accumulation |
| Earned Leave / Privilege Leave | EL/PL | 15 days (earned at 1.25 day/month) | Yes (max 30 days) | Can be encashed on retirement/departure |
| Medical / Sick Leave | ML/SL | 12 days | No | Medical certificate required for > 3 days |
| Maternity Leave | MatL | 180 days (6 months) | N/A | Government of India Maternity Benefit Act |
| Paternity Leave | PatL | 15 days | No | Within 6 months of child's birth/adoption |
| Leave Without Pay | LWP | On approval | N/A | Deducted from salary; no entitlement |
| Compensation Off | CompOff | Per extra duty done | Expire in 30 days | E.g., for working on declared holidays |
| Study Leave | StudyL | 2 years (lifetime) | N/A | Principal + Promoter approval; teaching bond required |
| Extra Ordinary Leave | EOL | On approval | N/A | Serious personal reason; no salary |

**[Edit Leave Policy]** — Principal can modify entitlement days (subject to legal minimums). Each change logged with reason and timestamp.

---

## 5. Tab: Leave Balance Summary

Overview of all staff leave balances for the current academic year.

**Summary table:**
| Staff Name | Dept | CL Used | CL Balance | EL Earned | EL Used | EL Balance | ML Used | LWP Days | Carry Forward (EL) |
|---|---|---|---|---|---|---|---|---|---|
| Ms. Sudha Rani | Science | 4 | 8 | 11.25 | 6 | 5.25 | 0 | 0 | 8 (from last yr) |
| Mr. Ramesh Kumar | Maths | 7 | 5 | 9.5 | 4 | 5.5 | 0 | 2 | 15 |
| … | … | … | … | … | … | … | … | … | … |

**Filters:** Department · Leave type · Show only negative balances (staff in LWP territory)
**Export:** CSV for payroll processing

---

## 6. Tab: Leave Encashment Register

Year-end leave encashment records (earned leave can be encashed):

| Staff Name | EL Balance | EL Encashed | Rate (₹/day) | Amount | Date | Approved By |
|---|---|---|---|---|---|---|
| Mr. Rao (Retired) | 28 | 28 | ₹1,200 | ₹33,600 | 31 Mar 2026 | Principal |
| Ms. Begum (Resigned) | 12 | 12 | ₹900 | ₹10,800 | 15 Mar 2026 | Principal |

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/holidays/` | Holiday list for year |
| 2 | `POST` | `/api/v1/school/{id}/holidays/` | Add holiday |
| 3 | `DELETE` | `/api/v1/school/{id}/holidays/{id}/` | Remove holiday |
| 4 | `POST` | `/api/v1/school/{id}/holidays/import/` | Import state holiday list |
| 5 | `GET` | `/api/v1/school/{id}/leave-policy/` | Leave policy definitions |
| 6 | `PATCH` | `/api/v1/school/{id}/leave-policy/` | Update leave policy |
| 7 | `GET` | `/api/v1/school/{id}/staff/leave-balances/` | All staff leave balances |
| 8 | `GET` | `/api/v1/school/{id}/staff/leave-encashment/` | Leave encashment register |
| 9 | `POST` | `/api/v1/school/{id}/staff/leave-encashment/` | Record encashment |

---

## 8. Business Rules

- Casual Leave cannot be combined with other leave types to form a long absence without Principal's written approval
- Maternity Leave entitlement (180 days) is non-negotiable — Indian law minimum; school cannot set it lower
- Leave policy changes take effect from the next month (existing balances unaffected)
- Emergency closure declared on the same day: auto-notifies all parents and staff via registered WhatsApp/SMS
- Holiday deletion that conflicts with an already-approved staff leave → triggers notification to affected staff to re-apply

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
