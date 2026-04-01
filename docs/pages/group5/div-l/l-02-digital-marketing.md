# L-02 — Digital Marketing & SEO

> **URL:** `/coaching/marketing/digital/`
> **File:** `l-02-digital-marketing.md`
> **Priority:** P2
> **Roles:** Marketing Coordinator (K3) · Branch Manager (K6)

---

## 1. SEO Performance

```
SEO DASHBOARD — toppers-coaching.in
As of 31 March 2026

  ORGANIC SEARCH (Google Search Console — Mar 2026):
    Total impressions:    84,200
    Total clicks:          4,840
    Average CTR:           5.75%
    Average position:     18.4

  TOP PERFORMING PAGES:
    URL                                    │ Impressions │ Clicks │ CTR   │ Avg Pos
    ───────────────────────────────────────┼─────────────┼────────┼───────┼────────
    /ssc-cgl-coaching-hyderabad/           │   24,800    │  1,640 │ 6.6%  │  4.2  ✅
    /ibps-po-coaching-hyderabad/           │   18,400    │  1,020 │ 5.5%  │  6.8  ✅
    /mock-test-series-ssc-cgl/             │   12,600    │    680 │ 5.4%  │  8.4  ✅
    /best-coaching-centre-hyderabad/       │   10,200    │    440 │ 4.3%  │ 14.6  🟡
    /bank-po-coaching-hyderabad/           │    8,400    │    360 │ 4.3%  │ 16.2  🟡
    /ssc-cgl-results-toppers-2026/         │    4,200    │    380 │ 9.0%  │  5.4  ✅ (new)
    ───────────────────────────────────────┴─────────────┴────────┴───────┴────────

  TARGET KEYWORDS (not yet ranking well):
    "ssc cgl coaching near me" — position 28 (target: top 10) ⚠️
    "best coaching for government exam Hyderabad" — position 32 ⚠️
    SEO action: Local SEO improvements, Google Business optimisation
```

---

## 2. Paid Ads Dashboard

```
PAID ADVERTISING — March 2026

  GOOGLE ADS:
    Campaign         │ Spend    │ Impressions │ Clicks │ CTR   │ Conv │ CPA
    ─────────────────┼──────────┼─────────────┼────────┼───────┼──────┼───────
    SSC CGL 2026     │ ₹14,200  │   42,800    │  1,480 │ 3.46% │  26  │ ₹546
    IBPS PO 2026     │ ₹ 6,800  │   18,400    │    680 │ 3.70% │  12  │ ₹567
    Brand (TCC)      │ ₹ 3,200  │   12,800    │    940 │ 7.34% │  18  │ ₹178
    ─────────────────┴──────────┴─────────────┴────────┴───────┴──────┴───────
    TOTAL Google     │ ₹24,200  │   74,000    │  3,100 │ 4.19% │  56  │ ₹432

  META ADS (Facebook + Instagram):
    Campaign         │ Spend    │ Reach      │ Clicks │ CTR   │ Conv │ CPA
    ─────────────────┼──────────┼────────────┼────────┼───────┼──────┼───────
    SSC CGL Lead Gen │ ₹ 8,400  │   68,400   │  1,240 │ 1.81% │  18  │ ₹467
    Alumni Success   │ ₹ 2,800  │   42,000   │    640 │ 1.52% │   —  │  n/a
    IBPS Lead Gen    │ ₹ 2,600  │   28,400   │    480 │ 1.69% │   8  │ ₹325
    ─────────────────┴──────────┴────────────┴────────┴───────┴──────┴───────
    TOTAL Meta       │ ₹13,800  │  138,800   │  2,360 │ 1.70% │  26  │ ₹531

  TOTAL PAID SPEND:  ₹38,000  │  TOTAL CONVERSIONS: 82  │  BLENDED CPA: ₹463
```

---

## 3. Email & WhatsApp Campaigns

```
MESSAGING CAMPAIGNS — March 2026

  EMAIL MARKETING:
    List size:              2,840 (active enquiries + students + alumni)
    Campaign: "SSC CGL 2026 batch now open" — sent 10 Mar 2026
      Delivered:    2,796  │  Opened: 1,008 (36.1%)  │  Clicked: 284 (10.2%)
      Unsubscribed:    12  │  Bounced:  44            │  Enquiries from: 28
    Campaign: "Mock test result celebration" — sent 25 Mar 2026
      Delivered:    2,802  │  Opened: 1,284 (45.8%)  │  Clicked: 412 (14.7%)

  WHATSAPP BROADCAST:
    List size:              3,620 (opted-in)
    Message: "SSC CGL 2026 batch filling fast — 8 seats remaining"
      Delivered:    3,588  │  Read:  2,240 (62.4%)  │  Replies: 84
      Opt-outs:        6   │  Action: removed from list ✅

  SMS (Transactional only — not marketing):
    Used only for: OTP, payment confirmation, class cancellation alerts
    Not used for: promotional messages (TRAI DLT compliance)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/marketing/digital/seo/` | SEO performance metrics |
| 2 | `GET` | `/api/v1/coaching/{id}/marketing/digital/ads/?month=2026-03` | Paid ads performance by campaign |
| 3 | `POST` | `/api/v1/coaching/{id}/marketing/digital/campaign/` | Create new digital campaign |
| 4 | `GET` | `/api/v1/coaching/{id}/marketing/digital/email/campaigns/` | Email campaign history |
| 5 | `POST` | `/api/v1/coaching/{id}/marketing/digital/whatsapp/broadcast/` | Send WhatsApp broadcast |
| 6 | `GET` | `/api/v1/coaching/{id}/marketing/digital/whatsapp/optout-list/` | Opt-out list management |

---

## 5. Business Rules

- Paid advertising campaigns target students in the 18–28 age group in Hyderabad and nearby districts (Rangareddy, Medchal); ad targeting uses demographic and interest signals (government jobs, banking exam, SSC/UPSC content engagement) but does not use sensitive personal data categories prohibited under DPDPA 2023 (religion, caste, political affiliation); Meta and Google ad platforms must be configured to exclude these targeting criteria; the marketing coordinator reviews targeting settings monthly to ensure compliance
- Google Ads conversion tracking is set up to count a "conversion" when a user fills in the website enquiry form (not when they enroll); the actual enrollment conversion happens later in the counselling process and is tracked in the CRM (F-02); the CPA reported in the Google Ads dashboard (₹432–₹567) is cost per enquiry lead, not cost per enrollment; the true cost per enrollment from paid channels is higher (enquiry-to-enrollment conversion is ~14%); both metrics are tracked and reported separately to avoid inflating the efficiency of paid channels
- WhatsApp marketing is subject to TRAI's Unsolicited Commercial Communications (UCC) guidelines and Meta's Business Messaging Policy; TCC uses only WhatsApp Business API (not the regular WhatsApp app) for broadcasts; every broadcast includes an opt-out instruction ("Reply STOP to unsubscribe"); opt-outs are processed within 24 hours and logged; the opt-out list is shared with the CRM to ensure opted-out contacts are not re-added to any broadcast list; TRAI penalties for UCC violations start at ₹50,000 per complaint, making compliance non-negotiable
- Local SEO is TCC's highest-ROI digital channel because coaching students search with strong local intent ("SSC coaching Hyderabad", "near Ameerpet"); ranking on page 1 for these terms delivers high-quality leads with zero cost per click; Google Business Profile optimisation (consistent NAP — name, address, phone; fresh photos; review responses; posts) is the primary local SEO lever; the marketing coordinator spends 2 hours per week on Google Business maintenance, which is more cost-effective than ₹14,000/month in Google Ads for the same keyword
- Email list hygiene is maintained quarterly; bounced addresses (44 in March) are removed after 2 consecutive bounces; unsubscribed addresses (12 in March) are added to a permanent suppression list and never contacted again, even if they re-enquire via another channel; emailing a suppressed address is a DPDPA 2023 violation; the suppression list is stored separately from the active contact list and is checked against every email send; a marketing coordinator who re-adds suppressed contacts to the active list is liable for a data breach under TCC's internal policy

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division L*
