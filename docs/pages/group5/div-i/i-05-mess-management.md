# I-05 — Mess / Food Management

> **URL:** `/coaching/hostel/mess/`
> **File:** `i-05-mess-management.md`
> **Priority:** P2
> **Roles:** Hostel Warden (K3) · Mess Contractor (external) · Branch Manager (K6)

---

## 1. Today's Menu & Meal Summary

```
MESS MANAGEMENT — 30 March 2026 (Monday)

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  TODAY'S ATTENDANCE: 108 residents  │  Meals served today: 322 of 324   │
  └──────────────────────────────────────────────────────────────────────────┘

  TODAY'S MENU:
    BREAKFAST (7:00–7:45 AM):
      Idli (4 pieces) + Sambar + Coconut chutney
      Tea / Coffee  |  Served: 106 students ✅ (2 in early morning class)

    LUNCH (12:00–1:00 PM):
      Rice + Dal + Mixed vegetable sabzi + Papad + Salad
      Curd rice option available  |  Served: 108 students ✅

    DINNER (7:30–8:30 PM):
      Chapati (4) + Paneer curry + Jeera rice + Pickle
      Fruit (banana)  |  Upcoming — not yet served

  WEEKLY MENU (30 Mar – 5 Apr 2026):
    Mon: Idli / Rice-Dal / Chapati-Paneer
    Tue: Dosa / Rajma rice / Chapati-Egg (non-veg day)
    Wed: Upma / Veg biryani / Chapati-Dal
    Thu: Poha / Curd rice / Chapati-Chicken (non-veg day)
    Fri: Idli / Rice-Sambhar / Chapati-Mix veg
    Sat: Paratha / Pulao / Chapati-Mutton (non-veg day)
    Sun: Poori-Bhaji (special) / Biryani (non-veg) / Rest (dinner optional)
```

---

## 2. Meal Count & Special Dietary

```
SPECIAL DIETARY REQUIREMENTS — Active Residents

  Student          │ Room   │ Requirement             │ Verified by
  ─────────────────┼────────┼─────────────────────────┼────────────────────
  Akhil Kumar      │ A-01   │ Vegetarian only          │ Family request ✅
  Priya Reddy      │ B-11   │ Diabetic — no sugar      │ Doctor's cert ✅
  Kiran Naidu      │ A-05   │ No onion/garlic (Jain)   │ Student declaration ✅
  Divya Sharma     │ B-08   │ Vegetarian only          │ Family request ✅
  Ravi Singh       │ A-04   │ No pork (Muslim)         │ Student declaration ✅
  Mohammed R.      │ A-12   │ Halal meat only (Muslim) │ Student declaration ✅

  Total special diet: 22 students (20.4% of hostel)
  Mess contractor notified: ✅ | Non-veg days: Halal meat confirmed ✅

  MEAL SKIPS (pre-notified for today):
    Breakfast skipped: 2 (early morning batch, taken meal token from warden)
    Dinner will skip:  8 students (going home for evening, returning by 10:30 PM)
    → Token system: students must notify warden by 9 AM for that day's meal skips
```

---

## 3. Mess Contractor Management

```
MESS CONTRACTOR — Annapurna Catering Services
Contract: Apr 2025 – Mar 2026 (renewal pending for 2026–27)

  CONTRACT TERMS:
    Rate:           ₹120/student/day × 108 students = ₹12,960/day
    Monthly cost:   ₹12,960 × 30 = ₹3,88,800
    Quality check:  Warden inspects kitchen weekly; Branch Manager quarterly
    FSSAI License:  Yes — Annapurna FSSAI Reg. 10019023001234 ✅
    Hygiene cert.:  Telangana Food Safety Dept. — valid Mar 2027 ✅

  MONTHLY PAYMENT:
    Invoice raised by Annapurna: 1st of each month for previous month
    Payment within 7 days of invoice
    March invoice: ₹3,88,800 (based on 108 × 30 days × ₹120)
    Paid: 5 March 2026 ✅

  COMPLAINTS (March 2026):
    Food quality (cold/stale):  3 complaints → 1 valid (warden confirmed)
    Late serving:                1 complaint (dinner 30 min late Mar 22)
    Foreign object in food:      0 complaints ✅
    Contractor notice issued:    1 (for late serving — verbal warning)

  CONTRACT RENEWAL NOTES:
    Current rate ₹120/day — contractor requesting ₹135/day (+12.5%) for 2026–27
    TCC counter-offer: ₹128/day (+6.7%) — negotiation ongoing
    Decision needed by: 10 April 2026 (before May batch starts)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/hostel/mess/menu/?date=2026-03-30` | Day's menu |
| 2 | `GET` | `/api/v1/coaching/{id}/hostel/mess/weekly/?week=2026-W14` | Weekly menu |
| 3 | `POST` | `/api/v1/coaching/{id}/hostel/mess/menu/` | Create or update menu |
| 4 | `GET` | `/api/v1/coaching/{id}/hostel/mess/dietary/` | Special dietary requirements |
| 5 | `POST` | `/api/v1/coaching/{id}/hostel/mess/complaint/` | Log a mess complaint |
| 6 | `GET` | `/api/v1/coaching/{id}/hostel/mess/contractor/` | Contractor details and contract |

---

## 5. Business Rules

- Mess food quality directly affects student performance; students who eat poorly prepared or nutritionally inadequate food (high in oil/salt, low in protein and vegetables) have lower energy and concentration levels for studying; TCC's menu is designed by a registered dietitian (consulted annually) with a balance of carbohydrates, proteins, and vegetables; the warden is responsible for ensuring the contractor follows the approved menu and does not substitute cheaper ingredients; a formal weekly check by the warden is documented and shared with the Branch Manager
- FSSAI (Food Safety and Standards Authority of India) registration and a valid state food safety certificate are non-negotiable conditions of the mess contract; TCC's liability for any food safety incident (contamination, food poisoning) is significant; the contractor's FSSAI license must be displayed in the kitchen; if the license expires, the contractor must renew before the next meal cycle; TCC verifies renewal status at quarterly contract reviews; an expired FSSAI license during active service is a legal violation for which TCC (as the premise owner) shares liability
- Students must notify the warden of meal skips by 9 AM for that day; this notification goes to the contractor so they can adjust the day's preparation quantity; wasted food (prepared but not consumed) is a cost to TCC — the contractor charges per student per day regardless of consumption; the token/notification system reduces waste by allowing preparation adjustments; students who repeatedly skip meals without notice are counselled (meal skipping is often a stress indicator)
- Special dietary requirements (vegetarian, halal, diabetic, Jain) are accommodated as a welfare obligation; TCC cannot force a Muslim student to eat non-halal meat or a Jain student to consume onion/garlic; these requirements are recorded at hostel admission (not at course enrollment) and communicated to the mess contractor; the contractor must provide separate serving utensils and preparation areas for halal and vegetarian food to prevent cross-contamination; failure to comply is a contract violation
- The mess contractor rate negotiation (₹120 → ₹135/day, counter-offer ₹128) is a business decision with a deadline driven by the May batch start; if no contractor agreement is reached by April 10, TCC must either: (a) extend the current contract month-to-month at the current rate, or (b) invite bids from alternative contractors; the Branch Manager manages this negotiation; the Director is involved if the increase exceeds 10% (as it impacts the hostel P&L significantly — ₹12.5/day × 108 students × 365 days = ₹4.93 lakh/year impact)

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division I*
