# L-01 — Marketing Dashboard

> **URL:** `/coaching/marketing/`
> **File:** `l-01-marketing-dashboard.md`
> **Priority:** P2
> **Roles:** Branch Manager (K6) · Marketing Coordinator (K3) · Director (K7)

---

## 1. Marketing Overview

```
MARKETING DASHBOARD — Toppers Coaching Centre
As of 31 March 2026 | AY 2025–26

  ┌──────────────────────────────────────────────────────────────────────┐
  │  ACQUISITION SUMMARY                                                 │
  ├──────────────┬──────────────┬──────────────┬────────────────────────┤
  │  LEADS (Mar) │  DEMOS (Mar) │  ENROLLMENTS │  COST PER ENROLLMENT   │
  │    842        │    312       │    128       │      ₹1,840            │
  │  ↑ 14% MoM   │  ↑ 8% MoM   │  ↑ 12% MoM  │  ↓ ₹220 vs last mo   │
  ├──────────────┴──────────────┴──────────────┴────────────────────────┤
  │  MARKETING SPEND (Mar 2026):  ₹52,000                               │
  │    Digital ads:    ₹28,000  (53.8%)                                 │
  │    Events:         ₹12,000  (23.1%)                                 │
  │    Print/offline:  ₹ 8,000  (15.4%)                                 │
  │    Content/design: ₹ 4,000  ( 7.7%)                                 │
  │  ROI:  128 enrollments × ₹32,000 avg fee = ₹40.96 L revenue        │
  │        Marketing spend ₹52,000 → ROI: 78.8× ✅                     │
  └──────────────────────────────────────────────────────────────────────┘

  CHANNEL PERFORMANCE (Mar 2026):
    Channel         │ Leads │ Demos │ Enrolled │ Conv% │ Cost/Lead │ Cost/Enroll
    ────────────────┼───────┼───────┼──────────┼───────┼───────────┼────────────
    Google Ads      │  228  │   84  │    32    │ 14.0% │  ₹123     │  ₹875
    Facebook/Insta  │  184  │   56  │    18    │  9.8% │   ₹98     │ ₹1,836
    Walk-in         │  186  │  186  │    36    │ 19.4% │    ₹0     │    ₹0
    Alumni referral │  124  │  124  │    24    │ 19.4% │    ₹0     │ ₹1,500*
    Student referral│   72  │   72  │    14    │ 19.4% │    ₹0     │ ₹1,250*
    Organic search  │   48  │   —   │     4    │  8.3% │    ₹0     │    ₹0
    ────────────────┴───────┴───────┴──────────┴───────┴───────────┴────────────
    * Referral reward cost included in cost/enrollment
```

---

## 2. Brand Metrics

```
BRAND HEALTH METRICS — March 2026

  ONLINE PRESENCE:
    Google Business rating:    4.6/5.0 (248 reviews)  ✅
    JustDial rating:           4.3/5.0 (186 reviews)  ✅
    Sulekha:                   4.4/5.0  (92 reviews)  ✅
    Facebook page rating:      4.5/5.0 (124 reviews)  ✅

    Google Business impressions (Mar):   18,400
    Website sessions (Mar):               4,840
    Website enquiry form submissions:       312
    Average enquiry-to-callback time:    < 2 hrs (target: < 4 hrs) ✅

  SOCIAL MEDIA:
    Instagram followers:       8,420  (↑ 380 Mar)
    Facebook page likes:       6,280  (↑ 180 Mar)
    YouTube subscribers:       2,840  (↑ 140 Mar)
    LinkedIn page followers:   1,240  (↑ 82 Mar)
    WhatsApp broadcast list:   3,620  (opted-in students + prospects)

  CONTENT PUBLISHED (Mar 2026):
    Instagram posts:    24  │  Reels:  8  │  Stories: 62
    YouTube videos:      4  │  avg views: 2,840
    Blog posts:          2  │  avg organic sessions: 420
    WhatsApp broadcasts: 8  │  open rate: 62%
```

---

## 3. Campaigns Active

```
ACTIVE CAMPAIGNS — March–April 2026

  Campaign                     │ Channel      │ Budget   │ Status   │ Leads │ Goal
  ─────────────────────────────┼──────────────┼──────────┼──────────┼───────┼──────────────
  SSC CGL 2026 Batch Open      │ Google+Meta  │ ₹18,000  │ ✅ Live  │  184  │ 50 enrolments
  IBPS PO 2026 Pre-launch      │ Meta only    │ ₹ 8,000  │ ✅ Live  │   92  │ 30 enrolments
  Alumni Success Reel Series   │ YouTube+Insta│ ₹ 4,000  │ ✅ Live  │   —   │ Brand awareness
  Result Celebration (SSC CGL) │ All channels │ ₹ 6,000  │ ✅ Live  │   62  │ 20 enrolments
  Summer Foundation Batch      │ Google+Print │ ₹12,000  │ 📅 Apr 1 │   —   │ 60 enrolments

  [Edit Campaign]   [View Performance]   [Pause]   [New Campaign +]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/marketing/dashboard/` | Marketing dashboard summary |
| 2 | `GET` | `/api/v1/coaching/{id}/marketing/channels/performance/?month=2026-03` | Channel performance metrics |
| 3 | `GET` | `/api/v1/coaching/{id}/marketing/brand/metrics/` | Brand rating and social metrics |
| 4 | `GET` | `/api/v1/coaching/{id}/marketing/campaigns/` | All campaigns with status |
| 5 | `POST` | `/api/v1/coaching/{id}/marketing/campaigns/` | Create new campaign |
| 6 | `GET` | `/api/v1/coaching/{id}/marketing/roi/?month=2026-03` | Marketing ROI calculation |

---

## 5. Business Rules

- Marketing ROI is calculated as (revenue from new enrollments) ÷ (marketing spend); TCC's March ROI of 78.8× means every ₹1 spent on marketing generated ₹78.8 in revenue; this exceptionally high ROI is partly explained by the fact that 40% of enrollments came from referrals (zero direct spend); the more meaningful metric is the paid channel ROI, which is lower; the Branch Manager tracks both total ROI and paid-channel-only ROI to assess the true efficiency of marketing investment
- Cost per enrollment (₹1,840 in March) is the primary efficiency metric for paid marketing; this must be benchmarked against the average revenue per student (₹32,000 for a full course) and the lifetime value (referrals generated by a placed student); acquiring a student at ₹1,840 who then generates 2 referrals (saving ₹3,700 in future acquisition costs) has a true cost of ₹1,840 − ₹3,700 = negative acquisition cost; this referral LTV calculation justifies investing in student success programs (welfare, alumni network) as marketing spend
- Google Business and third-party ratings are monitored weekly; a drop in Google rating below 4.0 or a spike in negative reviews is treated as a brand emergency requiring immediate investigation and response; TCC responds to all reviews (positive and negative) within 48 hours; the response to a negative review is never defensive or dismissive — it acknowledges the concern, provides context, and invites the reviewer to contact TCC directly; a public combative response to a 2-star review does more brand damage than the review itself
- WhatsApp broadcast list (3,620 contacts) is managed under DPDPA 2023 consent requirements; every contact on the broadcast list opted in (either via website form, walk-in consent form, or existing student/alumni relationship); bulk messaging to numbers without consent is illegal under TRAI regulations (UCC guidelines) and risks TCC's number being flagged as spam; opt-out requests must be honoured within 24 hours and the number removed permanently from all broadcast lists
- Campaign performance data from Google Ads and Meta Ads is integrated via their respective APIs into the EduForge marketing dashboard; this avoids manual CSV imports and ensures real-time data; the marketing coordinator can see leads, cost per lead, and conversion funnel directly without switching between platforms; however, TCC uses the EduForge CRM (F-02) as the single source of truth for leads — platform-reported leads that do not appear in the CRM are not counted as validated leads

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division L*
