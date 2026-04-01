# O-11 — Digital Ad Spend Dashboard

> **URL:** `/group/marketing/campaigns/digital/`
> **File:** `o-11-digital-ad-spend-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Admission Data Analyst (Role 132, G1) — primary viewer; Campaign Manager (119) for config

---

## 1. Purpose

The Digital Ad Spend Dashboard is a reference and analytics page that consolidates the group's digital advertising activity across Google Ads, Meta (Facebook/Instagram), YouTube, and other online platforms. Unlike the Newspaper Tracker (O-10) where the platform is the system of record, digital ad campaigns are managed in external platforms (Google Ads console, Meta Business Suite). This page does NOT replace those tools — it serves as a reference layer that:

1. **Aggregates spend data** manually entered or imported from external platforms so that the Campaign Manager and Data Analyst can see total marketing spend (newspaper + digital + WhatsApp + outdoor) in one place
2. **Maps UTM-tracked leads** from the lead pipeline (O-15) back to digital campaigns, enabling CPL/CPA calculation
3. **Provides comparative analytics** — how does Google Ads CPL compare to newspaper CPL? Is Meta delivering cheaper leads than outdoor?
4. **Tracks external campaign IDs** so that when the Digital Marketing Executive (Role 116, G0) reports performance, the data can be cross-referenced

In Indian education groups, digital spend is 15–25% of marketing budget for large groups and 10–20% for small groups. The channels are:
- **Google Ads:** Search ads for "best school in Hyderabad", "CBSE school near me", "JEE coaching Kukatpally" — high intent, higher CPL
- **Meta (Facebook/Instagram):** Lead generation ads targeting parents aged 30–45 in specific pin codes — volume play, lower CPL
- **YouTube:** Pre-roll video ads featuring toppers and campus tours — brand awareness, hard to attribute directly
- **Google My Business:** Organic presence optimisation per branch — zero cost but critical for walk-in discovery

**Scale:** ₹15L–₹2Cr digital spend per season · 10–50 external campaigns across platforms · 2,000–20,000 digital leads per season

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admission Data Analyst | 132 | G1 | Read + Export — primary analytics viewer | Views all data, generates reports |
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — add/edit campaign entries, import data | Manages the tracker |
| Group Digital Marketing Executive | 116 | G0 | No Platform Access | Manages ads in Google/Meta directly |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Data entry: role 119 or G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Campaign Planning  ›  Digital Ad Spend Dashboard
```

### 3.2 Page Header
```
Digital Ad Spend Dashboard                     [Add Campaign Entry]  [Import Data]  [Export Report]
Data Analyst — Kavitha Rajan
Season 2026-27 · 28 digital campaigns tracked · ₹68,00,000 spent · 8,400 leads attributed
```

**Important notice banner (permanent):**
```
ℹ️  This page tracks digital ad spend for consolidated reporting. Actual campaigns are managed in
    Google Ads / Meta Business Suite / YouTube Studio. Data is manually entered or imported.
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Digital Spend | ₹ Amount | SUM(digital_campaign_spend) this season | Static blue | `#kpi-digital-spend` |
| 2 | Digital % of Total Mktg | Percentage | Digital spend / Total marketing spend × 100 | Static blue | `#kpi-digital-pct` |
| 3 | Digital Leads | Integer | COUNT leads WHERE source IN ('google_ads','meta','youtube') | Static green | `#kpi-digital-leads` |
| 4 | Avg CPL (Digital) | ₹ Amount | Digital spend / Digital leads | Green ≤ ₹300, Amber ₹301–₹800, Red > ₹800 | `#kpi-digital-cpl` |
| 5 | Best Platform | Text | Platform with lowest CPL (min 50 leads) | Static green | `#kpi-best-platform` |
| 6 | Conversions (Digital) | Integer | COUNT enrolled WHERE source = digital | Static green | `#kpi-digital-conversions` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/digital/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Platform Summary Cards

Horizontal row of platform cards showing aggregated metrics per platform.

**Card per platform:**

```
┌──────────────────────────────┐
│  🔵 Google Ads                │
│                              │
│  Spend: ₹28,00,000          │
│  Campaigns: 12               │
│  Leads: 3,200                │
│  CPL: ₹875                   │
│  CPA: ₹4,667                 │
│  Conv Rate: 5.6%             │
│                              │
│  [View Details →]            │
└──────────────────────────────┘
```

Platforms: Google Ads / Meta (Facebook+Instagram) / YouTube / Other

### 5.2 Digital Campaign Register

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row |
| Platform | Badge | Yes | Google Ads / Meta / YouTube / Other |
| External Campaign ID | Text | No | ID from external platform (for cross-reference) |
| Campaign Name | Text | Yes | Name as configured in external platform |
| Type | Badge | Yes | Search / Display / Video / Lead Gen / Retargeting |
| Target Geography | Text | Yes | Cities / Pin codes / Radius |
| Target Audience | Text | No | Age, interests, keywords |
| Start Date | Date | Yes | Campaign start |
| End Date | Date | Yes | Campaign end |
| Budget (External) | ₹ Amount | Yes | Budget set in external platform |
| Spend (Actual) | ₹ Amount | Yes | Actual spend reported |
| Impressions | Integer | Yes | Ad impressions |
| Clicks | Integer | Yes | Ad clicks |
| CTR | Percentage | Yes | Clicks / Impressions × 100 |
| Leads | Integer | Yes | Leads attributed (via UTM or manual) |
| CPL | ₹ Amount | Yes | Spend / Leads |
| Conversions | Integer | Yes | Enrollments from these leads |
| CPA | ₹ Amount | Yes | Spend / Conversions |
| Landing Page | URL | No | Where ad traffic goes |
| UTM Campaign | Text | No | UTM parameter for tracking |
| Status | Badge | Yes | Active / Paused / Completed |
| Last Updated | Date | Yes | When data was last refreshed |
| Actions | Buttons | No | [View] [Edit] [Update Metrics] |

**Default sort:** Spend DESC
**Pagination:** Server-side · 25/page

### 5.3 UTM Lead Attribution

Table showing how digital leads are attributed to specific campaigns via UTM parameters.

| UTM Source | UTM Medium | UTM Campaign | Leads | Enrolled | Conv % | Revenue Est |
|---|---|---|---|---|---|---|
| google | cpc | admission_2026_hyderabad | 1,240 | 68 | 5.5% | ₹47,60,000 |
| facebook | paid | neet_coaching_leads | 890 | 42 | 4.7% | ₹29,40,000 |
| instagram | paid | campus_tour_reel | 420 | 18 | 4.3% | ₹12,60,000 |
| youtube | video | topper_testimonial_jan | 310 | 8 | 2.6% | ₹5,60,000 |
| google | organic | — | 1,800 | 112 | 6.2% | ₹78,40,000 |

### 5.4 Digital vs Other Channels Comparison

Side-by-side comparison of digital channels vs traditional channels.

| Metric | Newspaper | Digital (All) | WhatsApp/SMS | Outdoor | Events | Referral |
|---|---|---|---|---|---|---|
| Total Spend | ₹1,42,00,000 | ₹68,00,000 | ₹28,00,000 | ₹42,00,000 | ₹32,00,000 | ₹18,00,000 |
| Total Leads | 4,200 | 8,400 | 3,100 | 800 | 1,400 | 900 |
| CPL | ₹3,381 | ₹810 | ₹903 | ₹5,250 | ₹2,286 | ₹2,000 |
| Conversions | 320 | 450 | 180 | 40 | 120 | 85 |
| CPA | ₹44,375 | ₹15,111 | ₹15,556 | ₹1,05,000 | ₹26,667 | ₹21,176 |
| Conv Rate | 7.6% | 5.4% | 5.8% | 5.0% | 8.6% | 9.4% |

---

## 6. Drawers & Modals

### 6.1 Modal: `add-campaign-entry` (560px)
- **Title:** "Add Digital Campaign Entry"
- **Fields:**
  - Platform (dropdown, required): Google Ads / Meta / YouTube / Other
  - External campaign ID (text)
  - Campaign name (text, required)
  - Campaign type (dropdown): Search / Display / Video / Lead Gen / Retargeting / Shopping
  - Target geography (text — cities, pin codes)
  - Target audience (textarea — age, interests, keywords)
  - Start date (date)
  - End date (date)
  - Budget (₹)
  - Landing page URL (URL)
  - UTM parameters (auto-generated or manual): source, medium, campaign, content, term
  - Notes (textarea)
- **Buttons:** Cancel · Save

### 6.2 Modal: `update-metrics` (480px)
- **Title:** "Update Campaign Metrics — [Campaign Name]"
- **Fields:**
  - Date range (from–to — period being reported)
  - Spend (₹)
  - Impressions (integer)
  - Clicks (integer)
  - Leads (integer — manually counted or from UTM)
  - Conversions (integer)
  - Notes (textarea)
- **Buttons:** Cancel · Update
- **Note:** Each update appends to history; not overwrite. Total = SUM of all updates.

### 6.3 Modal: `import-data` (560px)
- **Title:** "Import Digital Campaign Data"
- **Options:**
  - Upload CSV/XLSX (template download available)
  - Manual entry (opens add form for each row)
- **CSV Columns:** Platform, Campaign ID, Campaign Name, Date, Spend, Impressions, Clicks, Leads
- **Behaviour:** Parse → preview → confirm → merge with existing records

### 6.4 Drawer: `campaign-entry-detail` (640px, right-slide)
- **Tabs:** Overview · Metrics History · Leads · Notes
- **Overview tab:** All campaign fields, UTM parameters, landing page link
- **Metrics History tab:** Table of all metric updates over time — date range, spend, impressions, clicks, leads
- **Leads tab:** Leads from O-15 pipeline attributed to this campaign via UTM
- **Notes tab:** Internal notes
- **Footer:** [Edit] [Update Metrics] [Archive]

---

## 7. Charts

### 7.1 Digital Spend by Platform (Donut)

| Property | Value |
|---|---|
| Chart type | Donut |
| Title | "Digital Spend by Platform — Current Season" |
| Data | Spend per platform |
| Colour | Google: `#4285F4` / Meta: `#1877F2` / YouTube: `#FF0000` / Other: `#9CA3AF` |
| API | `GET /api/v1/group/{id}/marketing/digital/analytics/spend-by-platform/` |

### 7.2 CPL Comparison Across All Channels (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "CPL Comparison — Digital vs Traditional Channels" |
| Data | CPL per channel (newspaper, Google, Meta, YouTube, WhatsApp, outdoor, events, referral) |
| Colour | Green ≤ ₹1,000 / Amber ₹1,001–₹3,000 / Red > ₹3,000 |
| API | `GET /api/v1/group/{id}/marketing/digital/analytics/cpl-all-channels/` |

### 7.3 Monthly Digital Spend & Leads (Combo)

| Property | Value |
|---|---|
| Chart type | Combo — bars (spend) + line (leads) |
| Title | "Monthly Digital Spend & Lead Volume" |
| Data | Monthly spend (bars) + monthly lead count (line) |
| Colour | Bars: `#3B82F6` / Line: `#10B981` |
| API | `GET /api/v1/group/{id}/marketing/digital/analytics/monthly-trend/` |

### 7.4 Funnel: Digital Impressions → Clicks → Leads → Enrolled

| Property | Value |
|---|---|
| Chart type | Funnel |
| Title | "Digital Funnel — Season to Date" |
| Stages | Impressions → Clicks → Landing Page Visits → Leads → Enrolled |
| API | `GET /api/v1/group/{id}/marketing/digital/analytics/funnel/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Campaign entry added | "Digital campaign '[Name]' added for tracking" | Success | 3s |
| Metrics updated | "Metrics updated for '[Name]' — ₹[X] spend, [N] leads" | Success | 3s |
| Data imported | "[N] campaign records imported from CSV" | Success | 4s |
| Entry archived | "Campaign entry '[Name]' archived" | Info | 3s |
| Export ready | "Digital ad spend report ready for download" | Success | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No digital campaigns tracked | 📱 | "No Digital Campaigns Tracked" | "Add digital campaign entries to consolidate spend and attribution data." | Add Campaign Entry |
| No leads attributed | 📊 | "No Digital Leads Attributed" | "Ensure UTM parameters are configured so leads can be traced to digital campaigns." | — |
| No data for platform | 🔍 | "No [Platform] Data" | "No campaigns tracked for this platform yet." | Add Campaign Entry |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/digital/` | G1+ | List digital campaign entries |
| GET | `/api/v1/group/{id}/marketing/digital/{entry_id}/` | G1+ | Single entry detail |
| POST | `/api/v1/group/{id}/marketing/digital/` | G3+ | Add campaign entry |
| PUT | `/api/v1/group/{id}/marketing/digital/{entry_id}/` | G3+ | Update entry |
| POST | `/api/v1/group/{id}/marketing/digital/{entry_id}/metrics/` | G3+ | Add metrics update |
| GET | `/api/v1/group/{id}/marketing/digital/{entry_id}/metrics/` | G1+ | Metrics history |
| POST | `/api/v1/group/{id}/marketing/digital/import/` | G3+ | Import CSV/XLSX |
| GET | `/api/v1/group/{id}/marketing/digital/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/digital/platform-summary/` | G1+ | Platform cards data |
| GET | `/api/v1/group/{id}/marketing/digital/utm-attribution/` | G1+ | UTM lead attribution |
| GET | `/api/v1/group/{id}/marketing/digital/channel-comparison/` | G1+ | Cross-channel comparison |
| GET | `/api/v1/group/{id}/marketing/digital/analytics/spend-by-platform/` | G1+ | Spend donut |
| GET | `/api/v1/group/{id}/marketing/digital/analytics/cpl-all-channels/` | G1+ | CPL comparison |
| GET | `/api/v1/group/{id}/marketing/digital/analytics/monthly-trend/` | G1+ | Monthly combo chart |
| GET | `/api/v1/group/{id}/marketing/digital/analytics/funnel/` | G1+ | Digital funnel |
| POST | `/api/v1/group/{id}/marketing/digital/export/` | G1+ | Export report |

---

## 11. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../digital/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Platform cards | `<div id="platform-cards">` | `hx-get=".../digital/platform-summary/"` | `#platform-cards` | `innerHTML` | `hx-trigger="load"` |
| Campaign table | `<div id="campaign-table">` | `hx-get=".../digital/"` | `#campaign-table-body` | `innerHTML` | `hx-trigger="load"` |
| UTM table | `<div id="utm-table">` | `hx-get=".../digital/utm-attribution/"` | `#utm-table-body` | `innerHTML` | `hx-trigger="load"` |
| Comparison table | `<div id="comparison">` | `hx-get=".../digital/channel-comparison/"` | `#comparison-content` | `innerHTML` | `hx-trigger="load"` |
| Entry detail drawer | Row click | `hx-get=".../digital/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Add entry | Form submit | `hx-post=".../digital/"` | `#add-result` | `innerHTML` | Toast |
| Update metrics | Form submit | `hx-post=".../digital/{id}/metrics/"` | `#metrics-result` | `innerHTML` | Toast + card refresh |
| Import data | Upload form | `hx-post=".../digital/import/"` | `#import-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Filter/sort | Controls | `hx-get` with params | `#campaign-table-body` | `innerHTML` | `hx-trigger="change"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
