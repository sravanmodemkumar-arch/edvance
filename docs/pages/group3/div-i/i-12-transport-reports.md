# I-12 — Transport Reports

> **URL:** `/school/transport/reports/`
> **File:** `i-12-transport-reports.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Transport In-Charge (S3) — full access · Accounts Officer (S3) — financial reports · Administrative Officer (S3) — view · Principal (S6) — summary dashboard and CBSE reports

---

## 1. Purpose

Consolidated reporting across all transport sub-modules (I-01 through I-11). Transport reports serve:
- **Management:** Principal reviews fleet utilisation, route efficiency, cost per student
- **Financial:** Fee collected vs. cost; contract payments vs. transport revenue
- **Safety:** Incident frequency, safety checklist compliance, speed violations
- **CBSE Affiliation:** Transport safety register and compliance documentation for inspection
- **RTO/Insurance:** Fleet register and incident history for regulatory submissions

---

## 2. Report Categories

### 2.1 Fleet Utilisation Report

```
Fleet Utilisation — Academic Year 2026–27
Report period: April 2026 – March 2027

Vehicle        Route    School Days  Days Active  Days Maint.  Utilisation  Notes
AP29AB1234     R01      220          218          2            99.1%        ✅ Excellent
AP29CD5678     R02      220          215          5            97.7%        ✅ Good
AP29GH3456     R03      220          201          19           91.4%        ⚠️ High maint days
AP29IJ7890     R04      220          220          0            100%         ✅ Perfect
AP29KL1234     R05      220          217          3            98.6%        ✅ Good
Van (Staff)    Staff    220          216          4            98.2%        ✅ Good

Fleet average utilisation: 97.5%
Total vehicle-days: 1,320
Total maintenance days (across fleet): 33

Top issue — AP29GH3456:
  19 maintenance days — 4 separate incidents
  Recommendation: Review vehicle age/condition; consider replacement or enhanced maintenance schedule
  Cost of repairs: ₹38,400 (from I-01 maintenance log)

[Export fleet utilisation PDF]
```

### 2.2 Route Efficiency Report

```
Route Efficiency Analysis — 2026–27

Route  Students  Seats  Load%   Avg On-Time  Avg Delay   Incidents  Cost/Student/Month
R01    44        52     84.6%   96.3%        4.2 min      1          ₹1,273
R02    38        52     73.1%   92.8%        8.7 min      2          ₹1,421  ← review
R03    30        40     75.0%   94.1%        5.1 min      3          ₹933 (hired)
R04    55        52    105.8%  ⚠️ OVERLOADED  91.2%       7 min      1 acc   ₹618 (hired)
R05    32        40     80.0%   98.1%        1.8 min      0          ₹1,031

Observations:
  ⚠️ Route R04: OVERLOADED (55/52 seats) — immediate action required
     Resolution required before next school day (I-02 alert)
  ⚠️ Route R02: Below-average on-time performance; driver performance review suggested
  ✅ Route R05: Best performer — consider this route as model

Route R04 overload history: 2nd month in a row — unresolved
  [Escalate to Principal]  [View I-02 resolution actions]
```

### 2.3 Financial Summary — Transport

```
Transport Financial Summary — 2026–27

INCOME (Transport Fees Collected):
  Route R01: 44 students × ₹13,500/yr = ₹5,94,000
  Route R02: 38 students × ₹12,600/yr = ₹4,78,800
  Route R03: 30 students × ₹14,400/yr = ₹4,32,000
  Route R04: 55 students × ₹15,000/yr = ₹8,25,000
  Route R05: 32 students × ₹10,800/yr = ₹3,45,600
  Staff Van: 8 staff × ₹7,200/yr = ₹57,600
  Total fee income: ₹27,33,000

  Fee collection rate: 94.2% (₹25,74,486 collected, ₹1,58,514 outstanding)

EXPENDITURE (Estimated annual):
  Fuel (owned fleet 4 vehicles): ₹8,40,000 (@ ₹70/km × 30,000 km/vehicle avg)
  Driver salaries (5 drivers + 6 escorts): ₹21,60,000 (₹15,000/driver × 5 + ₹12,000/escort × 6)
  Vehicle maintenance (owned fleet): ₹1,24,000 (from I-01 log)
  Insurance + statutory docs (owned fleet): ₹1,68,000 (₹42,000/vehicle × 4)
  Contract transport payments (Venkatesh + Balaji): ₹27,12,000 (₹2,26,000/month × 12)
  GPS/CCTV maintenance: ₹36,000
  Miscellaneous: ₹24,000
  Total expenditure: ₹60,64,000

NET (Transport P&L):
  Total income: ₹27,33,000
  Total expenditure: ₹60,64,000
  Net transport loss: ₹(33,31,000)

Note: School transport is a welfare service — it is subsidised from tuition fee income.
The true cost/student/year is ₹2,527; the school charges ₹1,200–₹1,500 (50–60% recovery).
This cross-subsidy is common in Indian schools and is a known operational model.

[Export financial report]  [Compare vs prior year]
```

### 2.4 Safety Compliance Report

```
Transport Safety Compliance Report — 2026–27

Safety Checklist Compliance:
  Expected daily checklists: 220 days × 4 routes = 880
  Submitted: 851 (96.7%)
  Missed: 29 (3.3%) — all followed up with written warnings

Speed Violations:
  Total recorded: 4 (via GPS I-06)
  >40 km/h incidents: 4
  >50 km/h incidents: 1 (Route R04 — major violation — disciplinary action taken)
  Drivers with >2 violations: 1 (Kishore R. — Route R04) — [Review I-04 record]

Incidents (from I-08):
  Total incidents: 12
  Road accidents: 1 (minor — no injuries)
  Breakdowns: 6
  Medical emergencies: 3
  Misconduct/other: 2

CCTV compliance:
  Routes with functioning CCTV: 4/4 ✅ (at time of annual check)
  Non-functioning periods logged: 2 incidents, both resolved within 24 hours ✅

GPS compliance:
  Routes with active GPS: 4/4 ✅
  Offline events >30 minutes: 3 (all equipment resets — resolved same day)

BGV compliance:
  All drivers BGV-verified: ✅ 5/5
  All escorts BGV-verified: ✅ 6/6
  Annual medical fitness current: ✅ 5/5 drivers (as of report date)

CBSE inspection readiness: ✅ All registers complete and Principal-signed
[Generate CBSE transport safety report PDF]
```

### 2.5 Bus Attendance Summary (Cross-referenced with E-01)

```
Bus Attendance Summary — Term 1 (Apr–Jun 2026)

Total bus trips (morning + evening): 220 × 2 × 4 routes = 1,760 trip-days

Attendance discrepancies (I-05 vs E-01):
  Total discrepancies detected: 18
  Type breakdown:
    Student boarded bus but marked absent in school (E-01): 3  ⚠️ HIGH SEVERITY
    Student not on bus but present in school (parent dropped): 14  (low severity — explained)
    Unresolved discrepancies: 1  (still under investigation)

  The 3 high-severity discrepancies were investigated:
    All 3 resolved — students located within 15 minutes
    No missing child escalation to police required ✅

Parent notification compliance:
  "Not at stop" alerts sent: 312 individual instances
  Alert sent within 2 minutes of missed stop: 308/312 (98.7%) ✅
  Unresolved parent non-response (escalated to Transport In-Charge): 4

[Export attendance summary]
```

### 2.6 Student-wise Transport History

```
Student: Arjun Sharma (XI-A) — Route R01

Academic Year: 2026–27 (Report period: Apr–Oct 2026)

Transport enrollment: Active ✅  ·  Pickup stop: Kothapet Bus Stop

Monthly attendance summary:
  Month    School Days  Boarded (AM)  Absent (AM)  Dropped (PM)  Late arrivals
  April         22          20             2             20            0
  May           22          21             1             21            0
  June          20          18             2             18            0
  July          22          22             0             22            0
  August        22          21             1             20            1
  September     22          20             2             20            0
  October (so far) 5         5             0              5            0

Total rides: 127/133 (95.5%)  ·  Absences: 8 (all parent-confirmed)

Temporary stop changes this year: 1 (28 Mar 2026 — uncle's house, Dilsukhnagar — I-03)
Outstanding transport fees: ₹0 ✅

[Export student transport history]  [Print for parent on request]
```

---

## 3. CBSE Affiliation Transport Register

```
CBSE Affiliation Transport Safety Register — 2026–27
[CBSE Affiliation Bye-Laws — Transport Section]

School: GREENFIELDS SCHOOL
CBSE Affiliation No.: 1200XXX

Section A: Fleet Details
  Total vehicles: 5 buses + 1 van = 6 school vehicles
  Hired vehicles: 3 buses (2 operators)
  All vehicles comply: Yellow colour, GPS, CCTV, speed governor ✅

Section B: Driver/Escort Details
  Total drivers: 8 (5 school-employed + 3 contractor)
  All BGV-verified: ✅
  All with valid HMV license: ✅
  Female escorts on all routes: ✅ 6 escorts for 5 student routes + 1 relief

Section C: Incident Register Summary
  [See I-08 export]

Section D: Safety Checklist Compliance
  Annual compliance rate: 96.7% ✅

Section E: GPS Tracking
  All buses GPS-equipped: ✅
  AIS-140 compliance: ✅

Signed: Principal ___________________ Date: __________
        Transport In-Charge _________ Date: __________

[Export as PDF]  [Print for CBSE inspection]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/transport/reports/fleet-utilisation/` | Fleet utilisation report |
| 2 | `GET` | `/api/v1/school/{id}/transport/reports/route-efficiency/` | Route efficiency analysis |
| 3 | `GET` | `/api/v1/school/{id}/transport/reports/financial/?year={yr}` | Transport P&L summary |
| 4 | `GET` | `/api/v1/school/{id}/transport/reports/safety/?year={yr}` | Safety compliance report |
| 5 | `GET` | `/api/v1/school/{id}/transport/reports/attendance-summary/?term={t}` | Bus attendance vs school attendance |
| 6 | `GET` | `/api/v1/school/{id}/transport/reports/student/{student_id}/?year={yr}` | Student transport history |
| 7 | `GET` | `/api/v1/school/{id}/transport/reports/cbse-register/` | CBSE affiliation format export |
| 8 | `GET` | `/api/v1/school/{id}/transport/reports/dashboard/` | Principal summary dashboard |

---

## 5. Business Rules

- Transport P&L is informational; transport is treated as a cost centre (not a profit centre) for the school; the subsidy from tuition fees is a conscious management decision
- Route efficiency report flags any route where load factor falls below 60% for two consecutive months — the Transport In-Charge should consider consolidating that route to reduce costs
- CBSE affiliation transport register must be signed by both the Principal and the Transport In-Charge; it is submitted as part of the annual affiliation renewal package and must be available during inspection
- The financial report crosses to D-20 (expenditure vouchers) for salary data and D-19 (vendor payments) for contract payments; these are not re-entered here — the report pulls live data from those modules
- Speed violation report feeds into I-04 driver profile (disciplinary history); three violations in a year trigger a mandatory disciplinary committee review
- All reports have a data retention period matching the underlying data: safety reports (3 years), incident reports (indefinitely for accident/POCSO), financial reports (7 years per Income Tax Act)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
