# I-03 — Occupancy Report

> **URL:** `/coaching/hostel/occupancy/`
> **File:** `i-03-occupancy-report.md`
> **Priority:** P2
> **Roles:** Hostel Warden (K3) · Branch Manager (K6) · Accounts (K5)

---

## 1. Monthly Occupancy Report

```
HOSTEL OCCUPANCY REPORT — March 2026
Toppers Coaching Centre, Hyderabad Main

  SUMMARY:
    Avg occupancy (March):    90.0%  (108/120)
    Peak occupancy:           91.7%  (Mar 12 — 110/120)
    Lowest occupancy:         88.3%  (Mar 1 — 106/120 — exam leaves)

  MOVEMENT SUMMARY:
    Students checked in (March):    6  (new academic year enrollment)
    Students checked out (March):   3  (2 course completed, 1 withdrawal)
    Net change:                    +3  (cumulative occupancy grew)

  OCCUPANCY BY BLOCK:
    Block   │ Capacity │ Avg Occupied │ Avg Occupancy │ Variance
    ────────┼──────────┼──────────────┼───────────────┼──────────────
    Block A │    60    │     54.2     │    90.3%      │ ±1.2 beds/day
    Block B │    60    │     53.8     │    89.7%      │ ±1.4 beds/day

  REVENUE IMPACT:
    Full occupancy revenue (120 × ₹7,000):  ₹  8,40,000
    Actual collected (90% occupancy):        ₹  7,56,000  (108 × ₹7,000)
    Vacancy loss (12 rooms × ₹7,000):        ₹    84,000/month
    Annual vacancy loss at current rate:     ₹ 10,08,000 ← significant

  WAITLIST:
    Male students on waitlist:    8 (interested in Block A from May 2026 batch)
    Female students on waitlist:  6 (interested in Block B from May 2026 batch)
    → All 12 vacancies can be filled from waitlist when May batch starts ✅
```

---

## 2. Occupancy Trend

```
OCCUPANCY TREND — April 2025 – March 2026

  Month    │ Capacity │ Occupied │ Occupancy │ vs Target (90%)
  ─────────┼──────────┼──────────┼───────────┼──────────────────
  Apr 25   │   120    │    96    │   80.0%   │ ⚠️ Below target
  May 25   │   120    │   112    │   93.3%   │ ✅ Above (new batch)
  Jun 25   │   120    │   110    │   91.7%   │ ✅ Above
  Jul 25   │   120    │   106    │   88.3%   │ 🟡 Slightly below
  Aug 25   │   120    │   108    │   90.0%   │ ✅ On target
  Sep 25   │   120    │   110    │   91.7%   │ ✅ Above
  Oct 25   │   120    │   112    │   93.3%   │ ✅ Above
  Nov 25   │   120    │   108    │   90.0%   │ ✅ On target
  Dec 25   │   120    │   102    │   85.0%   │ ⚠️ Below (holidays)
  Jan 26   │   120    │   106    │   88.3%   │ 🟡 Slightly below
  Feb 26   │   120    │   108    │   90.0%   │ ✅ On target
  Mar 26   │   120    │   108    │   90.0%   │ ✅ On target

  Annual avg occupancy:  89.6%  (just below 90% target)
  Annual hostel revenue: ₹ 3,72,96,000 (₹3.73 Cr at ₹7,000/bed/month × 108 avg)
  Note: Actual G-07 figure of ₹3.15L/month reflects a portion of hostel students
        (some on scholarship or reduced rate)
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/hostel/occupancy/?month=2026-03` | Monthly occupancy report |
| 2 | `GET` | `/api/v1/coaching/{id}/hostel/occupancy/trend/?months=12` | 12-month occupancy trend |
| 3 | `GET` | `/api/v1/coaching/{id}/hostel/occupancy/waitlist/` | Waitlist by block and gender |
| 4 | `GET` | `/api/v1/coaching/{id}/hostel/occupancy/revenue/?month=2026-03` | Revenue impact of vacancy |

---

## 5. Business Rules

- The 90% occupancy target is the break-even threshold; below 85%, the hostel starts running at a loss (fixed costs — rent, staff, utilities — don't decrease with occupancy); above 95%, there's no capacity for emergency allotments (a student whose accommodation falls through needs a bed immediately); the 85–95% range is the operational sweet spot; the warden manages the waitlist proactively to bring occupancy into this range after each batch transition
- December and exam-period months have predictably lower occupancy as students travel home or stay off-campus during exam season; the warden plans for these periods by not filling long-term waiting-list allotments in October-November (saving spots for the December low period is counterproductive); instead, the Branch Manager reviews whether to offer a short-term "exam period" hostel discount to retain students who would otherwise stay at relatives' homes during exam months
- Occupancy data is used in the annual hostel lease renewal negotiation; if TCC's occupancy has averaged 90% for 2+ years, it has a strong case for a long-term lease at a fixed rent; if occupancy is volatile (60–95%), the landlord may resist a long-term commitment; the warden must maintain accurate monthly occupancy records for 3 years for this purpose
- The waitlist management (14 students waiting for May 2026 batch) means the 12 current vacancies will be filled when May batch starts; the warden pre-allots rooms to waitlisted students as soon as the current occupant's departure date is confirmed; this reduces vacancy loss (12 rooms at ₹7,000 each = ₹84,000/month of lost revenue); the goal is zero vacancy days between one occupant's departure and the next arrival
- Occupancy reports are shared with the Director monthly as part of the branch MIS; the Director monitors hostel occupancy as a leading indicator of batch health — a sudden drop in hostel occupancy (students leaving mid-course) may signal a course quality issue or a competitor luring students away; conversely, a full waitlist indicates TCC's hostel quality and price point are competitive and should inform capacity expansion planning

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division I*
