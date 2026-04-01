# J-01 — Principal Dashboard

> **URL:** `/college/reports/principal/`
> **File:** `j-01-principal-dashboard.md`
> **Priority:** P1
> **Roles:** Principal/Director (S6) · Trust/Management (S7)

---

## 1. Executive Dashboard

```
PRINCIPAL DASHBOARD — GCEH
As of 27 March 2027

INSTITUTION HEALTH SCORE: 81 / 100
  ████████████████████████████████░░░░░░░░  81%

DOMAIN SCORECARD:
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ Domain              │ Score  │ Trend     │ Alert                           │
  ├─────────────────────┼────────┼───────────┼─────────────────────────────────┤
  │ Academic            │ 84/100 │ ↑ +2      │ 2 result uploads pending        │
  │ Attendance          │ 87/100 │ → stable  │ CE-3A branch below 75% cutoff   │
  │ Finance             │ 78/100 │ ↓ -3      │ ₹42L fee defaulters outstanding │
  │ Placement           │ 82/100 │ ↑ +4      │ Mech branch at 36.7% only       │
  │ Research            │ 74/100 │ ↑ +1      │ SERB report due 31 Mar          │
  │ Compliance          │ 86/100 │ → stable  │ Fire NOC pending renewal        │
  │ HR                  │ 88/100 │ → stable  │ 3 vacancies open                │
  │ Hostel              │ 76/100 │ ↓ -1      │ Block A satisfaction 71.6%      │
  └─────────────────────┴────────┴───────────┴─────────────────────────────────┘

OVERALL HEALTH = WEIGHTED AVG (Academic 25% + Finance 20% + Compliance 20%
                               + Placement 15% + HR 10% + Research 10%)
```

---

## 2. Today's Snapshot

```
TODAY — 27 March 2027 (Friday)

ATTENDANCE:
  Students present:  1,240 / 1,424  (87.1%)
  Faculty on duty:   59 / 62        (95.2%)
  Non-teaching:      34 / 38        (89.5%)

CLASSES TODAY:
  Scheduled: 48 | Conducted: 44 | Cancelled: 4
  Cancellation reason: 2 faculty on academic leave (conference); 2 substitutes arranged

FEE COLLECTIONS (today):
  Online payments received: 14 (₹1,08,400)
  Counter payments: 6 (₹42,000)
  Total today: ₹1,50,400

INCIDENTS / FLAGS:
  🔴 1 student: Medical emergency (Ravi K., Room 204 hostel — treated at campus dispensary)
  🟡 1 faculty: Mr. Anil K. (PIP) — counselling session at 14:00 today
  🟡 Block A water pump: Reported faulty (estate manager informed; repair today)
  🟢 No disciplinary incidents

UPCOMING TODAY:
  10:00 — Academic Council sub-committee (timetable rationalisation)
  14:00 — Placement drive: Cognizant (82 students registered)
  16:30 — NBA NBA Criterion 3 review meeting (CSE Dept.)
```

---

## 3. Key Performance Indicators (Month View)

```
KPI DASHBOARD — March 2027

ACADEMIC:
  Average attendance (month):        88.4%       Target: 90%   ⚠️ -1.6%
  CIA marks uploaded (on time):      91.2%       Target: 95%   ⚠️
  Student-teacher ratio:             23:1        AICTE norm: 20:1  ⚠️ (3 vacancies)
  Faculty PhD %:                     40.3%       NAAC A target: 60%  📈 improving

FINANCE:
  Fee collection (semester 2 YTD):  ₹3.84Cr     Target: ₹4.68Cr   82.1%
  Fee defaulters:                   127 students (₹42.3L outstanding)
  Operating surplus (YTD):          ₹38.4L      Target: ₹45L
  Payroll disbursed (on time):      ✅ 100%

PLACEMENT (2026–27 season):
  Students placed:                   224 / 332   67.5%
  Median CTC:                        ₹4.5L
  Companies visited (YTD):           23

RESEARCH (YTD 2026–27):
  Publications accepted:             13
  Active grants:                     5 (₹79.7L)
  Patents (YTD):                     0 filed (1 expected April)

COMPLIANCE:
  Pending P1 alerts:                 2
  Pending P2 alerts:                 3
  NAAC SSR completion:               92%  (target 100% by 1 Apr 2027)

HR:
  Attrition YTD:                     3.0%        3-year avg: 4.2%  ✅
  Open vacancies:                    3
  FDP days/faculty (YTD):            4.8         Target: 7.2/year
```

---

## 4. NAAC / NBA Status Summary

```
NAAC CYCLE 3 — STATUS (As of 27 March 2027)

SSR Preparation:
  Criterion 1 (Curricular Aspects):    ✅ Complete
  Criterion 2 (Teaching-Learning):     ✅ Complete
  Criterion 3 (Research):              ✅ Complete
  Criterion 4 (Infrastructure):        ✅ Complete
  Criterion 5 (Student Support):       ✅ Complete
  Criterion 6 (Governance):            ⬜ 85% (2 sub-sections pending)
  Criterion 7 (Institutional Values):  ⬜ 90% (Best practices section in draft)

SSR TARGET SUBMISSION:   1 April 2027
PEER TEAM VISIT (est.): October 2027

ESTIMATED NAAC GRADE:  A (3.5–4.0 range)
  Current CGP estimate: 3.62/4.0
  Key vulnerability: Faculty PhD % (Criterion 2.4) + Student satisfaction (7.x)

NBA (B.Tech CSE + ECE):
  SAR submitted:        ✅ November 2025
  Site visit expected:  November 2027
  Accreditation status: In process (current accreditation valid until Nov 2027)
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/reports/principal/dashboard/` | Full principal dashboard |
| 2 | `GET` | `/api/v1/college/{id}/reports/principal/today/` | Today's snapshot |
| 3 | `GET` | `/api/v1/college/{id}/reports/principal/kpi/?period=month` | Monthly KPI summary |
| 4 | `GET` | `/api/v1/college/{id}/reports/principal/naac-status/` | NAAC/NBA preparation status |
| 5 | `GET` | `/api/v1/college/{id}/reports/principal/alerts/` | Cross-domain active alerts |

---

## 6. Business Rules

- The Principal Dashboard is the single entry point for institutional situational awareness; a Principal who must navigate 10 different modules to understand the institution's status will inevitably miss signals; the health score and domain scorecard are designed to surface the 3–5 items that require the Principal's personal attention today, not present all data equally
- The institution health score must be calculated on a documented methodology (weights + deduction model) disclosed to the Governing Body; a score that is opaque or manipulable undermines trust; GCEH's score is computed from source module data automatically — the Principal cannot manually adjust it, which makes it credible in Governing Body presentations
- The "today's snapshot" section reflects live data as of the time of access; it is not a daily report but a real-time view; faculty duty status feeds from biometric login; fee payments feed from the payment gateway; the Principal sees this on arrival and can immediately identify if, for example, fewer than 80% faculty are on duty and take corrective action within the day
- Monthly KPI deviation alerts (e.g., attendance 88.4% vs 90% target) are meaningful only when paired with trend data and causal explanation; the dashboard provides 3-month trend sparklines and allows the HOD to add a comment; a Principal who acts on a single month's deviation without understanding the trend may introduce unnecessary pressure; EduForge's KPI commentary field enables contextual explanation from the responsible unit head
- The Principal Dashboard is not a surveillance tool but a management support system; faculty and staff must understand that the data visible to the Principal is aggregated and intended for institutional improvement, not individual monitoring; EduForge's privacy policy and institutional communication should clearly state this; individual-level data (e.g., specific faculty attendance) is accessible only to the HOD and HR, not displayed on the Principal's summary view

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division J*
