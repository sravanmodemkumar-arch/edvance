# I-07 — Maintenance Requests

> **URL:** `/coaching/hostel/maintenance/`
> **File:** `i-07-maintenance.md`
> **Priority:** P2
> **Roles:** Hostel Warden (K3) · Branch Manager (K6) · Operations (K3)

---

## 1. Maintenance Queue

```
MAINTENANCE REQUESTS — Hostel
As of 30 March 2026  |  Open: 8  |  Resolved (Mar): 24

  #     │ Location  │ Issue                  │ Raised By    │ Reported    │ Priority │ Status
  ──────┼───────────┼────────────────────────┼──────────────┼─────────────┼──────────┼──────────────
  M-241 │ A-12      │ Tube light not working │ Mohammed R.  │ 29 Mar 8 PM │ 🟡 Med   │ ⏳ Scheduled
  M-242 │ B-03      │ Tap leaking (bathroom) │ Kavitha D.   │ 29 Mar 10 AM│ 🔴 High  │ ⏳ In Progress
  M-243 │ Study room│ Projector bulb blown   │ Warden       │ 28 Mar 6 PM │ 🔴 High  │ ✅ Resolved
  M-244 │ Common rm │ Fan making noise       │ Ravi S.      │ 28 Mar 4 PM │ 🟡 Med   │ ⏳ Scheduled
  M-245 │ Gate      │ CCTV camera (gate) off │ Security     │ 27 Mar 9 PM │ 🔴 High  │ ✅ Resolved
  M-246 │ A-08      │ Wardrobe door broken   │ Arjun S.     │ 27 Mar 3 PM │ 🟢 Low   │ ⏳ Scheduled
  M-247 │ Mess      │ Gas burner weak flame  │ Mess staff   │ 26 Mar 2 PM │ 🔴 High  │ ✅ Resolved
  M-248 │ B-15      │ Window latch broken    │ Divya K.     │ 25 Mar 8 PM │ 🔴 High  │ ✅ Resolved
  ...  (open)

  CONTRACTOR ASSIGNED:
    Plumbing (M-242): Krishna Plumbers — technician arriving 30 Mar 11 AM
    Electricals (M-241, M-244): TCC in-house maintenance staff — scheduled today
```

---

## 2. Raise New Request

```
NEW MAINTENANCE REQUEST

  Raised by:    [Warden — Sunitha Verma ▼]  (or student name)
  Location:     [Block A ▼]  Room: [A-12 ▼]
  Issue type:   [Electrical ▼]
  Description:  [Tube light not working — right side of room (near study table)]
  Priority:     (●) High  ( ) Medium  ( ) Low
                High = safety/security/water/structural issue
                Medium = comfort or convenience (fan, wardrobe)
                Low = cosmetic (paint, minor fixture)

  Attach photo: [Upload: a12_light.jpg ← uploaded ✅]
  Assign to:    [TCC In-house Electrician ▼]
  Expected by:  [31 March 2026 ▼]

  [Submit Request]

  SLA:
    High:    Resolved within 24 hours
    Medium:  Resolved within 72 hours
    Low:     Resolved within 7 days
```

---

## 3. Maintenance Analytics

```
MAINTENANCE ANALYTICS — March 2026

  TOTAL REQUESTS: 32  (resolved: 24, open: 8)
  RESOLUTION RATE: 75.0%
  AVG RESOLUTION TIME:
    High priority:   18.4 hours  (SLA: 24 hrs) ✅
    Medium priority: 58.2 hours  (SLA: 72 hrs) ✅
    Low priority:    4.8 days    (SLA: 7 days) ✅

  BY CATEGORY:
    Electrical:   10 requests (31.3%) — tube lights, fan, AC, projector
    Plumbing:      8 requests (25.0%) — taps, drainage, toilets
    Carpentry:     6 requests (18.8%) — doors, wardrobes, windows
    HVAC/AC:       4 requests (12.5%) — AC units (summer season starting)
    Security/CCTV: 2 requests  (6.3%) — camera, lock
    Other:         2 requests  (6.3%)

  RECURRING ISSUES (flag for preventive maintenance):
    A-12 tube light: 3rd time in 6 months → replace entire fitting (not just bulb)
    B-bathroom taps: 4th complaint → assess piping (not just taps)

  PREVENTIVE MAINTENANCE SCHEDULED:
    Apr 15: Annual AC service (all units before summer peak)
    Apr 20: Annual electrical inspection (wiring, MCBs)
    Apr 30: Plumbing inspection (pre-monsoon check)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/hostel/maintenance/` | All maintenance requests |
| 2 | `POST` | `/api/v1/coaching/{id}/hostel/maintenance/` | Raise new maintenance request |
| 3 | `PATCH` | `/api/v1/coaching/{id}/hostel/maintenance/{mid}/` | Update request status or assign |
| 4 | `GET` | `/api/v1/coaching/{id}/hostel/maintenance/analytics/?month=2026-03` | Monthly maintenance stats |
| 5 | `GET` | `/api/v1/coaching/{id}/hostel/maintenance/scheduled/` | Upcoming preventive maintenance |

---

## 5. Business Rules

- Safety-critical issues (water leakage, broken window in ground-floor female block, CCTV camera down, gas leak suspicion) are classified as High priority and must be resolved within 24 hours regardless of time (including weekends); the warden has authority to call any contractor at any time for High priority issues; the Branch Manager is notified immediately for security and structural issues; a broken CCTV camera at the hostel gate is not just a maintenance issue — it is a security gap that must be fixed the same day
- Recurring issues (A-12 tube light reported 3 times in 6 months) signal that a temporary fix is not working; the warden must flag recurring issues for root-cause resolution (replace the entire fitting, not just the bulb); a recurring issue that is temporarily fixed 3+ times costs more in aggregate than a single permanent fix; the maintenance log provides the evidence to justify a permanent repair; the Branch Manager reviews the recurring issue report monthly and authorises spending on permanent fixes
- Student-reported maintenance issues must be acknowledged within 4 hours (a WhatsApp or portal notification: "Your complaint M-241 has been logged and is scheduled for resolution by [date]"); this acknowledgement prevents students from thinking their complaint was ignored and raising duplicates; the warden reviews new requests at 9 AM and 5 PM daily and logs acknowledgements; a student whose issue is not acknowledged within 4 hours should be able to escalate to the Branch Manager
- Preventive maintenance (annual AC service, electrical inspection, plumbing check) is scheduled proactively and funded from the hostel's operating budget; preventive maintenance is 3–5× cheaper than emergency repairs; the warden maintains a preventive maintenance calendar reviewed quarterly by the Branch Manager; skipping a scheduled AC service before summer (April–June, peak heat in Hyderabad) risks mid-summer breakdown when replacement parts have a 2-week lead time and all 108 residents are affected
- Contractor payments for maintenance work are approved by the Branch Manager, not the warden; the warden can authorise in-house maintenance staff work and minor purchases up to ₹500; anything above ₹500 (contractor call-out, part replacement) requires a Purchase Order approved by the Branch Manager; this financial control prevents the warden from entering into unauthorised contracts; the maintenance expenditure is reviewed monthly in the hostel P&L (included in "other expenses" in G-07)

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division I*
