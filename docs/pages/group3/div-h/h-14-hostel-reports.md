# H-14 — Hostel Reports & Analytics

> **URL:** `/school/hostel/reports/`
> **File:** `h-14-hostel-reports.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Chief Warden (S4) — full · Principal (S6) — full · Administrative Officer (S3) — export

---

## 1. Purpose

Comprehensive reporting and analytics for hostel management. Used for CBSE/state inspection reports, management review, and operational improvements.

---

## 2. Page Layout

### 2.1 Header
```
Hostel Reports & Analytics                           [Generate Report]
Academic Year: [2026–27 ▼]

Occupancy Rate: 93.3% (280/300 beds)  ·  Target: 95%
Welfare cases: 8 active  ·  Incidents this month: 3
Mess satisfaction: 3.8/5
```

### 2.2 Available Reports
```
Report                           Last Generated  Generate
Occupancy Report                 15 Mar 2026     [Generate]
Leave Pattern Analysis           15 Mar 2026     [Generate]
Health & Medical Report          Monthly auto    [View]
Welfare Cases Summary            —               [Generate]
Incident Log Summary             —               [Generate]
Mess Feedback & Hygiene Report   Monthly         [View]
CBSE Residential School Report   —               [Generate]
Annual Hostel Report             —               [Generate]
```

---

## 3. Occupancy Report

```
Occupancy Report — 2026–27 (Year to date)

Block                  Capacity  Current  Occupancy  Trend
Boys' Hostel Block A   180       168      93.3%      → Stable
Girls' Hostel Block B  120       112      93.3%      → Stable

Room type analysis:
  Single rooms (Boys):     5/5    100% (always full)
  Double rooms (Boys):    38/40    95% (1 vacant per block)
  Triple rooms (Boys):    25/30    83% (5 beds vacant)
  Dormitory (Boys):       60/60   100%

Waiting list: 5 students
Projected full occupancy: April 2027 (new academic year admissions)
```

---

## 4. Leave Pattern Analysis

```
Leave Pattern — 2026–27

Total leave requests: 1,840
  Weekend leave: 1,420 (77%)
  Home leave: 280 (15%)
  Emergency: 80 (4%)
  Medical: 60 (3%)

Weekend leave frequency per student:
  0 weekends: 8 students (never go home — concern: H-12 welfare check)
  1-2 per month: 210 students (normal range)
  3-4 per month: 42 students (every weekend — possible adjustment issue)
  5+ per month: 8 students (flagged for welfare counselling)

Late return incidents: 28 (1.5% of leaves) — most due to transport delays
```

---

## 5. CBSE Residential School Inspection Report

```
CBSE Residential School — Self-Study Report
Greenfields School (Residential Section) — 2026–27

A. Infrastructure
  Boys' Hostel: Block A — 180 beds, 45 rooms — ✅
  Girls' Hostel: Block B — 120 beds, 35 rooms, Female Warden only — ✅
  Medical Room: 1 sick room (8 beds), visiting doctor 3×/week — ✅
  CCTV: Common areas (not rooms/bathrooms) — ✅
  Fire Safety: Extinguishers every 20m, last serviced Jan 2026 — ✅
  Mess/Canteen: FSSAI certified (FSSAI/AP/12345, valid Mar 2027) — ✅

B. Staff
  Chief Warden: 1 (Mr. Arjun Reddy, MA Education)
  Wardens (Male): 4
  Wardens (Female): 3 (girls' hostel — ratio 1:40) ✅
  Matron: 1 (Ms. Kavitha Rao, B.Sc. Nursing) ✅
  Visiting Doctor: Dr. Suresh Reddy (MBBS) — 3×/week ✅

C. Registers (all maintained digitally + printed backup):
  ✅ Attendance Register (H-03)
  ✅ Leave/Exeat Register (H-04)
  ✅ Visitor Register (H-05)
  ✅ Medical Room Register (H-07)
  ✅ Duty Register (H-08)
  ✅ Conduct Register (H-10)

Certified by: Principal  ·  Date: 27 Mar 2026
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/reports/occupancy/?year={y}` | Occupancy report |
| 2 | `GET` | `/api/v1/school/{id}/hostel/reports/leave-pattern/?year={y}` | Leave analysis |
| 3 | `GET` | `/api/v1/school/{id}/hostel/reports/health/?month={m}&year={y}` | Medical report |
| 4 | `GET` | `/api/v1/school/{id}/hostel/reports/welfare/?year={y}` | Welfare summary |
| 5 | `GET` | `/api/v1/school/{id}/hostel/reports/cbse-inspection/?year={y}` | CBSE inspection report PDF |
| 6 | `GET` | `/api/v1/school/{id}/hostel/reports/annual/?year={y}` | Annual hostel report PDF |

---

## 7. Business Rules

- CBSE inspection report for residential schools must be prepared annually (before the affiliation renewal inspection); it cross-references all hostel registers
- Students who "never go home" on weekends (0 weekend leaves in a term) are flagged to the Chief Warden/Counsellor — either they have no home to go to (needs welfare support) or they prefer to stay (valid, but needs check)
- Occupancy below 80% for more than 2 months triggers a management review — hostel is under-utilised and costs may need restructuring
- All hostel reports are retained for 5 years per CBSE affiliation retention requirements

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
