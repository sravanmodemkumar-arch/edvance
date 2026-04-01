# C-21 — Admission Analytics Dashboard

> **URL:** `/school/admissions/analytics/`
> **File:** `c-21-admission-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Admission Officer (S3) — full · Academic Coordinator (S4) — full · Principal (S6) — full

---

## 1. Purpose

Provides analytics on the school's admission process — conversion funnel, class-wise fill rates, source of enquiries, year-on-year trends, and seat utilisation. The Principal and management make critical annual decisions based on this:
- How many Class I sections to open next year (based on enquiry demand)?
- Which admission sources are working (justify education fair expenditure)?
- Is the RTE fill rate on track?
- Are Class XI science seats filling or is the school losing students to competitor schools?

---

## 2. Page Layout

### 2.1 KPI Strip
```
Admission Analytics — 2026–27               Academic Year: [2026–27 ▼]
──────────────────────────────────────────────────────────────────────────────────
  Total Enquiries    284         Forms Issued    124 (43.7%)
  Seats Available    380         Confirmed       239 (62.9%)
  Conversion Rate    84.2%       Avg Days to     12.4 days
  (Enquiry→Enroll)               Close
──────────────────────────────────────────────────────────────────────────────────
```

### 2.2 Conversion Funnel (Chart.js)
```
Admissions Funnel — 2026–27

Enquiries     ████████████████████████████████████████  284
↓ Contacted   ████████████████████████████████████     249 (87.7%)
↓ Form Issued ██████████████████████████               186 (65.5%)
↓ Shortlisted ████████████████                         124 (43.7%)
↓ Confirmed   ██████████████                           106 (37.3%)
↓ Enrolled    █████████████                             84 (29.6%)  ← Year so far
```

### 2.3 Class-wise Fill Rate (Table + Bar Chart)
```
Class       Available  Confirmed  Fill%   Waitlisted  Comparison (Last Year)
Nursery        30         28       93%        6        88% (+5%)  ↑
LKG            30         26       87%        4        90% (-3%)  ↓
Class I        30         30      100%        8        94% (+6%)  ↑ FULL
Class IX       55         48       87%        6        82% (+5%)  ↑
XI Science     55         52       95%        9        88% (+7%)  ↑
XI Commerce    35         30       86%        5        80% (+6%)  ↑
XI Arts        20          8       40%        0        38% (+2%)  ↓ (Arts demand low)
```

### 2.4 Enquiry Source Breakdown (Doughnut Chart)
```
Where do enquiries come from?

Walk-in        84  (29.6%)  ████████████████████████
Sibling Ref    48  (16.9%)  ██████████████
Website Form   38  (13.4%)  ████████████
Phone          56  (19.7%)  █████████████████
WhatsApp       28  ( 9.9%)  ████████
Education Fair 16  ( 5.6%)  █████
Social Media   12  ( 4.2%)  ████
Other           2  ( 0.7%)  ▌

ROI insight: Education fair generated 16 enquiries at ₹48,000 spend = ₹3,000/enquiry
             Sibling referral generated 48 enquiries at ₹0 = ₹0/enquiry ← Best ROI
```

### 2.5 Year-on-Year Trend (Line Chart — 4 years)
```
Total Enquiries by Year:
2023–24: 212  →  2024–25: 238  →  2025–26: 261  →  2026–27: 284  (↑ 8.8%)

Conversion Rate by Year:
2023–24: 78%  →  2024–25: 80%  →  2025–26: 82%  →  2026–27: 84%  (↑ 2pp)
```

### 2.6 Stage-wise Drop-off Analysis
```
Where are leads being lost?

Enquiry → Contacted:        249/284 = 87.7%  (35 leads never contacted → ⚠️ Follow-up gap)
Contacted → Form Issued:    186/249 = 74.7%  (63 contacts didn't proceed → School fee?)
Form Issued → Shortlisted:  124/186 = 66.7%  (62 forms not returned → ⚠️ High incomplete rate)
Shortlisted → Confirmed:    106/124 = 85.5%  (18 shortlisted declined → Competition)
Confirmed → Enrolled:        84/106 = 79.2%  (22 confirmed but not enrolled yet — in progress)
```

---

## 3. Monthly Timeline View

```
Enquiry Timeline — 2026–27 (Monthly)

Oct 2025: ▌  8 enquiries   (Early interest — NRI)
Nov 2025: ████ 42 enquiries (Admission season opens)
Dec 2025: ████████ 68 enquiries (Peak month 1)
Jan 2026: ██████████ 82 enquiries (Peak month 2)
Feb 2026: █████████ 72 enquiries (Decision month)
Mar 2026: ████ 12 enquiries (Closing)
```

---

## 4. Class XI Demand Analysis

Special view for Class XI (critical year):

```
Class XI — Stream Demand 2026–27

              Applied  Selected  Enrolled  Last Year  Trend
Science PCM     84       38        32        30        ↑
Science PCB     42       14        10        12        ↓
Commerce        38       18        16        14        ↑
Arts            12        4         4         5        ↓

Insight: PCM demand high; consider opening 3rd section next year.
Arts demand declining; consider combining Commerce+Arts if < 10 students.
```

---

## 5. RTE Compliance View

```
RTE Admission Compliance — 2026–27

Required (25% of entry class):  10 seats
Applications Received:          86
Lottery Conducted:              ✅ 26 Mar 2026
Selected:                       10
Enrolled:                        8 (2 pending)
Unfilled RTE Seats:              0

Reimbursement Expected:  ₹1,44,000/year (10 students × ₹1,200/month × 12)
```

---

## 6. Export

[Export Report] → Admission Analytics PDF for management/board meeting:
- Executive summary (1 page)
- Funnel chart + source breakdown
- Class-wise fill rate table
- 4-year trend
- Recommendations (auto-generated based on data)

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/admissions/analytics/?year={year}` | Full analytics data |
| 2 | `GET` | `/api/v1/school/{id}/admissions/analytics/funnel/?year={year}` | Conversion funnel |
| 3 | `GET` | `/api/v1/school/{id}/admissions/analytics/source/?year={year}` | Source breakdown |
| 4 | `GET` | `/api/v1/school/{id}/admissions/analytics/fill-rate/?year={year}` | Class-wise fill rate |
| 5 | `GET` | `/api/v1/school/{id}/admissions/analytics/trend/?from={year}&to={year}` | Year-on-year trend |
| 6 | `GET` | `/api/v1/school/{id}/admissions/analytics/export/?year={year}` | Export analytics PDF |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
