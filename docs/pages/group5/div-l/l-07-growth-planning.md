# L-07 — Growth Planning & Targets

> **URL:** `/coaching/marketing/growth/`
> **File:** `l-07-growth-planning.md`
> **Priority:** P2
> **Roles:** Director (K7) · Branch Manager (K6) · Marketing Coordinator (K3)

---

## 1. Annual Growth Targets

```
GROWTH PLAN — AY 2026–27
Director Approved | March 2026 Review

  ENROLLMENT TARGETS:
    Metric                    │ AY 2025–26 Actual │ AY 2026–27 Target │ Growth
    ──────────────────────────┼───────────────────┼───────────────────┼────────
    Total enrolled (main):    │     1,840         │     2,100         │ +14.1%
    Online enrolled:          │       330         │       450         │ +36.4%
    Hostel occupancy:         │    84/108 (78%)   │   100/120 (83%)   │ +12 beds
    New batches launched:     │         4         │         6         │ +2
    New franchise batches:    │         8         │        10         │ +2
    Alumni-to-active ratio:   │      54.5%        │      62.0%        │ +7.5pp

  REVENUE TARGETS:
    Metric                    │ AY 2025–26 Actual │ AY 2026–27 Target │ Growth
    ──────────────────────────┼───────────────────┼───────────────────┼────────
    Total revenue:            │   ₹154.3 L        │   ₹185 L          │ +19.9%
    Online revenue:           │   ₹  6.2 L        │   ₹ 12 L          │ +93.5%
    Test series (external):   │   ₹  0 L          │   ₹  4 L          │ NEW
    Net profit margin:        │     31.4%          │     32.0%          │ +0.6pp
    Cost per enrollment:      │    ₹1,840          │    ₹1,600          │ -13.0%

  QUALITY TARGETS:
    Overall student rating:   │    4.2/5.0        │    4.4/5.0        │ +0.2
    Doubt SLA compliance:     │    91.2%          │    95.0%          │ +3.8pp
    Success rate (reported):  │    48.6%          │    52.0%          │ +3.4pp
    Dropout rate (actionable):│     0.3%          │     0.2%          │ -0.1pp
```

---

## 2. Growth Initiatives

```
GROWTH INITIATIVES — AY 2026–27

  INITIATIVE 1: Online Expansion (Revenue: +₹6L target)
    Action:   Launch standalone online test series subscription (₹1,499/6mo)
    Target:   400 non-TCC students subscribe via website/app
    Owner:    Director + Technology team
    Timeline: Launch by May 2026 | Review: Sep 2026
    Risk:     Cannibalisation of in-person enrollment (monitor closely)

  INITIATIVE 2: Hostel Expansion (Revenue: +₹2.4L target)
    Action:   Add 12 beds in Block C (construction approved ₹3.2L capex)
    Target:   100% hostel occupancy by Aug 2026 (new AY intake)
    Owner:    Operations + Branch Manager
    Timeline: Construction May–Jul 2026 | Ready: Aug 2026

  INITIATIVE 3: Summer Foundation Batch (Revenue: +₹4L target)
    Action:   Launch Class 10+2 foundation batch (May–Jul 2026)
    Target:   80 students enrolled; 40 convert to SSC/banking batch Aug 2026
    Owner:    Admissions + Marketing
    Timeline: Promotion starts Apr 1 | Batch starts May 1 2026
    Fee:      ₹12,000 (3-month intensive)

  INITIATIVE 4: New Exam Category — UPSC Prelims (Revenue: +₹8L target)
    Action:   Pilot UPSC Prelims batch (GS Paper 1+2, 40 students)
    Target:   40 enrollments by Sep 2026; faculty hired by Aug 2026
    Owner:    Director + Academic Director
    Timeline: Faculty hiring: Jul 2026 | Batch launch: Oct 2026
    Risk:     UPSC market is different from SSC/banking; reputational risk if quality low

  INITIATIVE 5: Franchise Growth (Revenue: +₹6L target royalties)
    Action:   Onboard 2 new franchise branches (Karimnagar, Khammam)
    Target:   Franchise agreements signed by Jun 2026; operational Oct 2026
    Owner:    Director + Legal
    Timeline: Due diligence May–Jun; agreement Jun–Jul 2026
```

---

## 3. Marketing Budget Plan

```
MARKETING BUDGET — AY 2026–27 (Proposed)

  Category                  │ AY 2025–26 Actual │ AY 2026–27 Budget │ Change
  ──────────────────────────┼───────────────────┼───────────────────┼────────
  Digital advertising       │    ₹3.8 L         │    ₹5.2 L         │ +36.8%
  Events & seminars         │    ₹1.6 L         │    ₹2.0 L         │ +25.0%
  Content creation          │    ₹0.6 L         │    ₹1.0 L         │ +66.7%
  Referral rewards          │    ₹1.4 L         │    ₹1.8 L         │ +28.6%
  Print & offline           │    ₹0.8 L         │    ₹0.6 L         │ -25.0%
  Alumni engagement         │    ₹0.4 L         │    ₹0.8 L         │ +100.0%
  ──────────────────────────┴───────────────────┴───────────────────┴────────
  TOTAL                     │    ₹8.6 L         │   ₹11.4 L         │ +32.6%
  As % of revenue:          │     5.6%          │     6.2%           │ +0.6pp

  ALLOCATION RATIONALE:
    Digital up: Online expansion initiative requires higher digital spend
    Alumni up: Franchise growth + UPSC launch need strong alumni advocacy
    Print down: Diminishing returns vs digital; budget reallocated
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/marketing/growth/targets/?year=2026-27` | Growth targets for the year |
| 2 | `GET` | `/api/v1/coaching/{id}/marketing/growth/initiatives/` | Growth initiatives with status |
| 3 | `PATCH` | `/api/v1/coaching/{id}/marketing/growth/initiatives/{iid}/` | Update initiative progress |
| 4 | `GET` | `/api/v1/coaching/{id}/marketing/growth/budget/?year=2026-27` | Marketing budget plan |
| 5 | `GET` | `/api/v1/coaching/{id}/marketing/growth/tracking/?month=2026-04` | Actual vs target tracking |

---

## 5. Business Rules

- Growth targets are set by the Director in February each year based on the previous year's performance, market conditions, and strategic priorities; the Branch Manager provides inputs (operational capacity, staff readiness, competitive landscape); growth targets that exceed operational capacity are adjusted — promising 2,500 students when the branch physically cannot accommodate more than 2,200 is a quality failure waiting to happen; growth must be paced to maintain service quality
- The UPSC Prelims initiative carries higher reputational risk than the other initiatives; SSC/banking is TCC's established competency; UPSC is a different exam, different student profile (typically 22–28, more research-oriented), and different pedagogy; if TCC launches a UPSC batch with inadequate faculty and poor results in the first year, it damages the TCC brand beyond just the UPSC segment; the Director requires a minimum 3-faculty hire (verified UPSC expertise) and a small pilot batch (40 students) before scaling; this "prove before scale" approach protects the core brand
- The online test series for non-TCC students (Initiative 1) is a fundamentally different business model: TCC would be selling a digital product nationally, competing with TestBook (₹499–₹2,499) and Unacademy; TCC's mock test quality (rated 4.4/5.0 by students) is the competitive advantage; the pricing (₹1,499 for 6 months) is positioned above TestBook but below TCC's own in-person package; the risk of cannibalisation (students choosing the ₹1,499 online option instead of the ₹32,000 in-person course) is real and must be monitored monthly during the first 6 months
- Marketing budget as percentage of revenue (5.6% → 6.2%) is within the 5–8% benchmark for service businesses in competitive markets; TCC's historical low marketing cost (significant word-of-mouth) justifies the 5.6% baseline; the incremental 0.6pp for AY 2026–27 is justified by the new initiatives (UPSC launch, online test series, franchise market entry) which all require marketing spend in new markets; the budget is approved by the Director and is a planned commitment, not a discretionary spend that can be cut mid-year
- Growth initiative tracking is reviewed monthly by the Branch Manager and quarterly by the Director; an initiative that is 3 months behind schedule with low conversion (Summer Foundation Batch: target 80 students, enrolled 20 by June) triggers a review — continue with a revised target, pivot the approach (lower fee, different target segment), or cancel and reallocate the marketing budget; sunk-cost fallacy must be avoided — a struggling initiative that continues consuming budget because "we already spent ₹2 lakh on it" is a management failure; data-driven go/no-go decisions are required at each quarterly gate

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division L*
