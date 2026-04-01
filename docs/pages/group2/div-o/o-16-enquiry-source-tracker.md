# O-16 — Enquiry Source Tracker

> **URL:** `/group/marketing/leads/sources/`
> **File:** `o-16-enquiry-source-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary analyst

---

## 1. Purpose

The Enquiry Source Tracker provides real-time attribution analytics — answering the question every Indian education group CEO asks: "Which marketing channel is actually bringing us students?" In groups spending ₹2–10 crore on marketing, misattributing sources means misallocating budget. A newspaper ad may generate 5,000 calls but only 200 enrollments, while a quiet referral programme generates 800 enrollments at 1/10th the cost. Without precise source tracking, groups keep pouring money into high-noise, low-conversion channels.

The problems this page solves:

1. **Attribution accuracy:** Parents interact with multiple channels before enrolling — they see a newspaper ad, then search online, then receive a WhatsApp message, then walk in. Which source gets credit? The platform supports first-touch (first channel), last-touch (final channel before walk-in), and multi-touch (weighted credit) attribution models.

2. **Source-specific tracking infrastructure:** Each source needs different tracking mechanisms. Newspaper ads use dedicated phone numbers (one per edition/date). Digital ads use UTM parameters. WhatsApp uses campaign IDs. Walk-ins use a "How did you hear about us?" field. Referrals use referral codes. This page configures and monitors all tracking codes.

3. **Source-to-enrollment mapping:** Knowing that a source generated 5,000 enquiries is useless if you don't know how many of those enquiries actually enrolled. This page connects O-15 (lead pipeline) to source attribution, showing the complete journey: Source → Enquiry → Contacted → Walk-in → Enrolled, per source.

4. **Campaign-level granularity:** Not just "newspaper" vs "digital" — the tracker shows "Eenadu Hyderabad edition Jan 15 half-page ad" generated 342 calls at ₹87 per call, while "Sakshi Telangana edition Jan 16 quarter-page" generated 89 calls at ₹224 per call. This enables precise media buying decisions.

**Scale:** 10+ source types · 50–500 tracking codes per season · 2,000–2,00,000 enquiries to attribute · real-time attribution updates as leads progress through pipeline

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — configure sources, tracking codes, attribution rules | Primary operator |
| Group Admission Data Analyst | 132 | G1 | Read + Export — full analytics access, download reports | Primary analytics consumer |
| Group Admission Telecaller Executive | 130 | G3 | Read (source data on assigned leads only) | Sees source when handling lead |
| Group CEO / Chairman | — | G4/G5 | Read — full source analytics for budget decisions | Strategic consumer |
| Group CFO / Finance Director | 30 | G1 | Read — source vs spend data | Budget justification |
| Branch Principal | — | G3 | Read (own branch sources) | Branch-level source performance |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Source configuration: role 119 or G4+. Analytics read: G1+. Branch users filtered to own branch data.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Lead Management  ›  Enquiry Source Tracker
```

### 3.2 Page Header
```
Enquiry Source Tracker                              [+ Add Source]  [Manage Tracking Codes]  [Export Report]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · 48,200 leads tracked · 12 source types · 186 tracking codes active
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Enquiries (Season) | Integer | COUNT(leads) WHERE season = current | Static blue | `#kpi-total` |
| 2 | Top Source | Source name + count | Source with MAX leads | Static blue | `#kpi-top-source` |
| 3 | Best Converting Source | Source name + % | Source with MAX(enrolled/leads) (min 50 leads) | Static green | `#kpi-best-convert` |
| 4 | Lowest CPL Source | Source name + ₹ | Source with MIN(spend/leads) | Static green | `#kpi-lowest-cpl` |
| 5 | Unattributed Leads | Integer | COUNT WHERE source = 'unknown' OR source IS NULL | Red > 10%, Amber 5–10%, Green < 5% | `#kpi-unattributed` |
| 6 | Active Tracking Codes | Integer | COUNT(tracking_codes) WHERE status = 'active' | Static blue | `#kpi-tracking-codes` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/leads/sources/kpis/"` → `hx-trigger="load"` → `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Source Performance** — Source-wise lead count, conversion, cost metrics
2. **Tracking Codes** — Phone numbers, UTM codes, QR codes management
3. **Attribution Model** — Configure first-touch / last-touch / multi-touch
4. **Trends** — Source performance over time

### 5.2 Tab 1: Source Performance

**Master source performance table.**

**Filter bar:** Season · Branch · Date Range · Source Type · Campaign

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Source | Text + icon | Yes | Source name with colour-coded icon |
| Type | Badge | Yes | Newspaper / Digital / WhatsApp / Walk-in / Referral / School Fair / Open Day / Website / Telecall / Email / Outdoor / Other |
| Enquiries | Integer | Yes | Total leads from this source |
| % of Total | Percentage | Yes | Enquiries / Total leads |
| Contacted | Integer | Yes | Leads that reached "Contacted" stage |
| Interested | Integer | Yes | Leads that reached "Interested" |
| Walk-ins | Integer | Yes | Leads that completed walk-in |
| Enrolled | Integer | Yes | Leads that enrolled |
| Conversion % | Percentage | Yes | Enrolled / Enquiries (colour: green ≥ 25%, amber 15–25%, red < 15%) |
| Spend (₹) | Amount | Yes | Total spend on this source (from O-09) |
| CPL (₹) | Amount | Yes | Spend / Enquiries |
| CPA (₹) | Amount | Yes | Spend / Enrolled (Cost Per Admission) |
| ROI | Multiple | Yes | (Enrolled × avg fee) / Spend |
| Trend | Sparkline | No | Mini 12-week trend line |

**Default sort:** Enquiries DESC
**Pagination:** Not needed (typically 10–15 rows)

**Expandable rows:** Click on a source row to expand and see campaign-level breakdown within that source. E.g., "Newspaper" expands to show each newspaper ad insertion individually.

### 5.3 Tab 2: Tracking Codes

Management of all tracking mechanisms.

#### 5.3.1 Phone Tracking Numbers

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Tracking Number | Phone | Yes | Dedicated number (e.g., 9876543001) |
| Assigned To | Text | Yes | Source + campaign (e.g., "Eenadu — Jan 15 — Full Page") |
| Source Type | Badge | Yes | Newspaper / Outdoor / Flex Banner |
| Branch | Text | Yes | Which branch this routes to |
| Total Calls | Integer | Yes | Calls received on this number |
| Leads Created | Integer | Yes | Leads auto-created from calls |
| Status | Badge | Yes | Active (green) / Paused (amber) / Retired (grey) |
| Active Since | Date | Yes | When number was activated |
| Actions | Buttons | No | [View Call Log] [Reassign] [Pause] [Retire] |

#### 5.3.2 UTM Tracking Codes

| Column | Type | Sortable | Notes |
|---|---|---|---|
| UTM Code | Text | Yes | Full UTM string |
| Source | Text | Yes | utm_source value |
| Medium | Text | Yes | utm_medium value |
| Campaign | Text | Yes | utm_campaign value |
| Content | Text | No | utm_content (optional) |
| Clicks | Integer | Yes | Total clicks with this UTM |
| Leads | Integer | Yes | Form submissions with this UTM |
| Status | Badge | Yes | Active / Expired |
| Actions | Buttons | No | [Copy Link] [QR Code] [View Analytics] |

#### 5.3.3 QR Codes

| Column | Type | Sortable | Notes |
|---|---|---|---|
| QR Code | Thumbnail | No | QR image |
| Label | Text | Yes | Description |
| Destination URL | Text | No | Where QR points to |
| Placed On | Text | Yes | "Prospectus" / "Flex Banner" / "Bus Panel" |
| Scans | Integer | Yes | Total scans |
| Leads | Integer | Yes | Leads from this QR |
| Actions | Buttons | No | [Download QR] [View Analytics] |

### 5.4 Tab 3: Attribution Model

Configuration page for how source credit is assigned.

**Attribution models:**

| Model | Description | When to Use |
|---|---|---|
| **First Touch** | 100% credit to the first source a lead interacted with | "What channel creates awareness?" |
| **Last Touch** | 100% credit to the last source before enrollment/walk-in | "What channel closes the deal?" |
| **Linear** | Equal credit split across all touchpoints | "Every channel contributed equally" |
| **Time Decay** | More credit to recent touchpoints, less to older ones | "Recent interactions matter more" |
| **Position Based** | 40% first touch, 40% last touch, 20% split among middle | "Both discovery and closing matter" |

**Current model:** [Dropdown to select] — default: First Touch (most common for Indian education groups)

**Preview:** When model changes, table in Tab 1 recalculates using new attribution.

### 5.5 Tab 4: Trends

Charts showing source performance over time (see §7).

---

## 6. Drawers & Modals

### 6.1 Modal: `add-source` (480px)

- **Title:** "Add Lead Source"
- **Fields:**
  - Source name (text, required — e.g., "Eenadu Telugu Daily")
  - Source type (dropdown, required): Newspaper / Digital Ads / WhatsApp / Walk-in / Referral / School Fair / Open Day / Website / Telecall / Email / Outdoor / SMS / Social Media / Other
  - Parent source (dropdown, optional — for sub-sources: "Eenadu" under "Newspaper")
  - Tracking method (dropdown): Phone Number / UTM Code / QR Code / Manual Entry / Auto-Detect
  - Linked budget line from O-09 (dropdown, optional)
  - Expected CPL (₹, optional — benchmark for comparison)
  - Notes (textarea)
- **Buttons:** Cancel · Save
- **Access:** Role 119 or G4+

### 6.2 Modal: `create-tracking-code` (560px)

- **Title:** "Create Tracking Code"
- **Type selector:** Phone Number / UTM Link / QR Code
- **Phone Number fields:**
  - Phone number (tel — from purchased tracking number pool or virtual number provider)
  - Assign to source + campaign (dropdowns)
  - Route calls to branch (dropdown)
  - IVR greeting (optional — "Thank you for calling Sunrise Education Group…")
- **UTM Link fields:**
  - Base URL (pre-filled: group website)
  - utm_source (text, required)
  - utm_medium (text, required)
  - utm_campaign (text, required)
  - utm_content (text, optional)
  - utm_term (text, optional)
  - Generated URL (auto-built, with copy button)
- **QR Code fields:**
  - Destination URL (text, required — or select from UTM links)
  - Label (text, required)
  - QR size: 2cm / 3cm / 5cm / 10cm
  - Format: PNG / SVG
  - Include logo in centre (toggle)
- **Buttons:** Cancel · Create
- **Access:** Role 119 or G4+

### 6.3 Drawer: `source-detail` (640px, right-slide)

- **Tabs:** Performance · Leads · Campaigns · Tracking · History
- **Performance tab:**
  - Source KPIs: enquiries, conversion %, CPL, CPA, ROI
  - Comparison with group average
  - Monthly performance trend (mini chart)
- **Leads tab:**
  - Paginated list of all leads from this source
  - Stage distribution (mini funnel)
  - Filter by branch / stage / date
- **Campaigns tab:**
  - All campaigns that used this source
  - Per-campaign performance
- **Tracking tab:**
  - All tracking codes linked to this source
  - Code performance (calls/clicks/scans per code)
- **History tab:**
  - Season-over-season performance (this source across 3 years)
- **Footer:** [Edit] [Export Data] [Archive]

---

## 7. Charts

### 7.1 Source Contribution (Treemap)

| Property | Value |
|---|---|
| Chart type | Treemap (Chart.js treemap plugin) |
| Title | "Lead Sources — Proportional Contribution" |
| Data | Per source: rectangle area = lead count; colour = conversion rate (green = high, red = low) |
| Tooltip | "[Source]: [N] leads, [X]% conversion, CPL ₹[Y]" |
| API | `GET /api/v1/group/{id}/marketing/leads/sources/analytics/treemap/` |

### 7.2 Source Funnel Comparison (Grouped Funnel)

| Property | Value |
|---|---|
| Chart type | Multi-funnel comparison (custom) |
| Title | "Conversion Funnel by Top 5 Sources" |
| Data | Top 5 sources side-by-side, each showing: Enquiry → Contacted → Walk-in → Enrolled |
| Colour | Per source |
| Purpose | See where each source's leads drop off |
| API | `GET /api/v1/group/{id}/marketing/leads/sources/analytics/source-funnels/` |

### 7.3 CPL vs CPA by Source (Scatter)

| Property | Value |
|---|---|
| Chart type | Scatter (Chart.js 4.x) |
| Title | "Cost per Lead vs Cost per Admission — by Source" |
| Data | Each point = 1 source; X = CPL (₹), Y = CPA (₹); bubble size = lead count |
| Colour | Green (below benchmark) / Red (above benchmark) |
| Tooltip | "[Source]: CPL ₹[X], CPA ₹[Y], [N] leads" |
| Quadrant labels | Top-left: "High CPA, Low CPL" / Bottom-right: "Low CPA, High CPL" / Bottom-left: "Efficient" / Top-right: "Inefficient" |
| API | `GET /api/v1/group/{id}/marketing/leads/sources/analytics/cpl-vs-cpa/` |

### 7.4 Weekly Source Trend (Stacked Area)

| Property | Value |
|---|---|
| Chart type | Stacked area (Chart.js 4.x) |
| Title | "Weekly Lead Inflow by Source — Last 16 Weeks" |
| Data | Weekly lead count per source |
| Colour | Per source type |
| X-axis | Week number |
| Y-axis | Lead count |
| Purpose | See which sources peak during which admission phases |
| API | `GET /api/v1/group/{id}/marketing/leads/sources/analytics/weekly-trend/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Source added | "Source '[Name]' added" | Success | 3s |
| Tracking code created | "Tracking code created — [Type]: [Code]" | Success | 3s |
| Attribution model changed | "Attribution model changed to [Model] — recalculating…" | Info | 3s |
| UTM link copied | "UTM link copied to clipboard" | Success | 2s |
| QR code downloaded | "QR code downloaded" | Success | 2s |
| Source archived | "Source '[Name]' archived" | Info | 3s |
| Tracking code retired | "Tracking code [Code] retired" | Info | 3s |
| Unattributed alert | "[N] leads have no source attribution — review required" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No sources configured | 📡 | "No Sources Configured" | "Add lead sources to start tracking where your enquiries come from." | Add Source |
| No tracking codes | 🔗 | "No Tracking Codes" | "Create tracking phone numbers, UTM links, or QR codes." | Create Tracking Code |
| No leads for source | 📊 | "No Leads for [Source]" | "This source hasn't generated any leads yet." | — |
| No trend data | 📈 | "Not Enough Data" | "Trend charts require at least 4 weeks of lead data." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + tab bar + table skeleton (12 rows) |
| Tab switch | Content area skeleton |
| Source detail drawer | 640px skeleton: KPI bar + 5 tabs |
| Tracking code table | Table skeleton (10 rows) |
| Attribution recalculation | Full-width progress bar: "Recalculating attribution…" |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/leads/sources/` | G1+ | List all sources with performance |
| GET | `/api/v1/group/{id}/marketing/leads/sources/{src_id}/` | G1+ | Source detail |
| POST | `/api/v1/group/{id}/marketing/leads/sources/` | G3+ | Add source |
| PUT | `/api/v1/group/{id}/marketing/leads/sources/{src_id}/` | G3+ | Update source |
| DELETE | `/api/v1/group/{id}/marketing/leads/sources/{src_id}/` | G4+ | Archive source |
| GET | `/api/v1/group/{id}/marketing/leads/sources/tracking-codes/` | G1+ | List tracking codes |
| POST | `/api/v1/group/{id}/marketing/leads/sources/tracking-codes/` | G3+ | Create tracking code |
| PATCH | `/api/v1/group/{id}/marketing/leads/sources/tracking-codes/{code_id}/` | G3+ | Update/retire code |
| GET | `/api/v1/group/{id}/marketing/leads/sources/attribution-model/` | G1+ | Current attribution config |
| PUT | `/api/v1/group/{id}/marketing/leads/sources/attribution-model/` | G3+ | Change attribution model |
| GET | `/api/v1/group/{id}/marketing/leads/sources/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/leads/sources/analytics/treemap/` | G1+ | Treemap data |
| GET | `/api/v1/group/{id}/marketing/leads/sources/analytics/source-funnels/` | G1+ | Multi-funnel data |
| GET | `/api/v1/group/{id}/marketing/leads/sources/analytics/cpl-vs-cpa/` | G1+ | Scatter data |
| GET | `/api/v1/group/{id}/marketing/leads/sources/analytics/weekly-trend/` | G1+ | Weekly trend data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../sources/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get=".../sources/?tab={performance/tracking/attribution/trends}"` | `#sources-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Dropdowns | `hx-get` with params | `#source-table-body` | `innerHTML` | `hx-trigger="change"` |
| Row expand | Source row click | `hx-get=".../sources/{id}/campaigns/"` | `#expand-row-{id}` | `innerHTML` | Inline campaign breakdown |
| Source detail drawer | Detail button | `hx-get=".../sources/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Attribution model change | Model select | `hx-put=".../sources/attribution-model/"` | `#source-table-body` | `innerHTML` | Recalculates all values |
| Tracking code create | Form submit | `hx-post=".../sources/tracking-codes/"` | `#tracking-result` | `innerHTML` | Toast |
| UTM copy | Copy button | JS clipboard API | — | — | Toast notification |
| Chart load | Tab 4 click | `hx-get=".../sources/analytics/..."` | `#chart-container` | `innerHTML` | Per-chart |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
