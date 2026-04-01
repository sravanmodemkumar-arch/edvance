# O-10 — Newspaper & Print Ad Tracker

> **URL:** `/group/marketing/campaigns/newspaper/`
> **File:** `o-10-newspaper-print-ad-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary tracker

---

## 1. Purpose

The Newspaper & Print Ad Tracker is a centralised register of every newspaper advertisement placed by the group across all publications, editions, languages, and branches throughout the admission season. In the Indian education market, newspaper advertising remains the single largest marketing spend category — consuming 30–40% of the total marketing budget for large groups and 40–50% for small groups. A group like Narayana running 50 branches in Telangana and Andhra Pradesh might place 300–500 newspaper insertions per season across Eenadu, Sakshi, Deccan Chronicle, Namaste Telangana, Times of India, The Hindu, and their regional editions.

The tracking challenges are enormous:
- Each publication has multiple editions (Hyderabad City, Telangana State, AP State, National), each with different rates
- Rate cards are negotiated annually with agencies; actual rates often differ from rate card by 20–40% (agency commission, volume discounts)
- Response tracking is near-impossible without a system — which ad in which paper on which date generated how many calls to which branch helpline?
- Creative artwork varies — Telugu ads differ from English ads; half-page vs quarter-page use different layouts
- Invoicing lags by 30–60 days; without a log, reconciliation with agency invoices is a nightmare

This page provides: a complete insertion register, cost tracking with agency rate reconciliation, response attribution (leads generated per insertion), creative asset linkage, publication calendar view, and performance analytics to determine which publication × edition × size × day-of-week combination delivers the best CPL.

**Scale:** 5–50 branches · 50–500 insertions per season · 5–15 publications · ₹50L–₹5Cr newspaper spend per season

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — add insertions, track response, manage rates | Primary tracker |
| Group Campaign Content Coordinator | 131 | G2 | Read + Link creative | Links artwork to insertions |
| Group Admission Data Analyst | 132 | G1 | Read + Export | Performance analytics |
| Group CFO / Finance Director | 30 | G1 | Read — cost data only | Invoice reconciliation |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Create/edit: role 119 or G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Campaign Planning  ›  Newspaper & Print Ad Tracker
```

### 3.2 Page Header
```
Newspaper & Print Ad Tracker                   [Add Insertion]  [Bulk Import]  [Publication Master]  [Export]
Campaign Manager — Ramesh Venkataraman
Season 2026-27 · 287 insertions · ₹1,42,00,000 spent · 4,200 leads attributed
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Insertions | Integer | COUNT(insertions) WHERE season = current | Static blue | `#kpi-total-insertions` |
| 2 | Total Spend | ₹ Amount | SUM(insertion_cost) this season | Amber if > budget allocation | `#kpi-total-spend` |
| 3 | Leads Attributed | Integer | SUM(leads) WHERE source = 'newspaper' this season | Static green | `#kpi-leads` |
| 4 | Avg CPL | ₹ Amount | Total spend / Total leads | Green ≤ ₹500, Amber ₹501–₹1,500, Red > ₹1,500 | `#kpi-avg-cpl` |
| 5 | Best Publication | Text | Publication with lowest CPL (min 10 leads) | Static blue | `#kpi-best-pub` |
| 6 | Upcoming (7d) | Integer | COUNT insertions WHERE ad_date within 7 days AND status = 'booked' | Static blue | `#kpi-upcoming` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/newspaper/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Insertion Register

Master table of all newspaper insertions.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Ad Date | Date | Yes | Publication date |
| Publication | Text | Yes | Eenadu / Sakshi / Deccan Chronicle / etc. |
| Edition | Text | Yes | Hyderabad City / Telangana / AP / National |
| Language | Badge | Yes | Telugu / English / Hindi |
| Ad Size | Badge | Yes | Full Page / Half Page / Quarter Page / Strip / Classified |
| Position | Badge | Yes | Front / Back / Inside / Education Supp / ROP |
| Colour | Badge | Yes | Colour / B&W |
| Creative | Thumbnail (40×40) | No | Preview of artwork used |
| Campaign | Text | Yes | Linked campaign name |
| Branch(es) | Text | Yes | Which branches' helpline is printed |
| Rate Card Cost | ₹ Amount | Yes | Published rate |
| Actual Cost | ₹ Amount | Yes | Negotiated/paid amount |
| Discount % | Percentage | Yes | (Rate − Actual) / Rate × 100 |
| Leads | Integer | Yes | Enquiries attributed to this insertion |
| CPL | ₹ Amount | Yes | Actual cost / Leads |
| Invoice # | Text | No | Agency invoice reference |
| Status | Badge | Yes | Booked (blue) / Published (green) / Cancelled (red) / Pending Invoice (amber) |
| Actions | Buttons | No | [View] [Edit] [Log Response] |

**Default sort:** Ad Date DESC (most recent first)
**Pagination:** Server-side · 25/page

**Filters:**
- Publication (dropdown)
- Edition (dropdown)
- Language (dropdown)
- Ad size (dropdown)
- Campaign (dropdown)
- Date range (from–to)
- Status (dropdown)
- Branch (dropdown)

### 5.2 Publication Calendar

Calendar view showing newspaper ads plotted on dates. Each date cell shows ad badges with publication abbreviation + size.

```
Mon 13 Jan     Tue 14 Jan     Wed 15 Jan     Thu 16 Jan     Fri 17 Jan     Sat 18 Jan     Sun 19 Jan
                              [EE-HYD-FP]                   [SK-TS-HP]     [EE-TS-FP]
                              [SK-HYD-QP]                                   [DC-HYD-HP]
                              [TOI-HYD-Strip]                               [NT-TS-QP]
```

Legend: EE=Eenadu, SK=Sakshi, DC=Deccan Chronicle, TOI=Times of India, NT=Namaste Telangana, TH=The Hindu
Sizes: FP=Full Page, HP=Half Page, QP=Quarter Page

Click on badge opens insertion detail.

### 5.3 Publication Master

Reference table of all publications, editions, and rate cards.

**Columns:**

| Column | Type | Notes |
|---|---|---|
| Publication | Text | Newspaper name |
| Edition | Text | City/State/National |
| Language | Badge | Telugu / English / Hindi |
| Circulation | Integer | Claimed daily circulation |
| Readership | Integer | Claimed readership (IRS data) |
| Rate — Full Page (Colour) | ₹ Amount | Published rate card |
| Rate — Half Page (Colour) | ₹ Amount | |
| Rate — Quarter Page (Colour) | ₹ Amount | |
| Rate — Full Page (B&W) | ₹ Amount | |
| Negotiated Discount | Percentage | Group's negotiated discount % |
| Agency | Text | Media buying agency |
| Contact Person | Text | Agency contact |
| Phone | Text | Agency phone |
| Season Contract | Badge | Yes / No / Renewal Due |

**Editable by:** Role 119 or G4+

### 5.4 Performance by Publication

Aggregated performance analytics per publication.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Publication | Text | Yes | |
| Edition | Text | Yes | |
| Insertions | Integer | Yes | Count this season |
| Total Spend | ₹ Amount | Yes | |
| Total Leads | Integer | Yes | |
| CPL | ₹ Amount | Yes | Cost per lead |
| Conversions | Integer | Yes | Enrollments from newspaper leads |
| CPA | ₹ Amount | Yes | Cost per admission |
| Best Day | Text | No | Day of week with highest response |
| Best Size | Badge | No | Ad size with best CPL |
| Trend | Sparkline | No | Lead response trend over insertions |
| ROI Rating | Badge | Yes | ⭐⭐⭐ (High) / ⭐⭐ (Medium) / ⭐ (Low) |

**Default sort:** CPL ASC (best performing first)

### 5.5 Performance by Ad Size

| Ad Size | Insertions | Avg Cost | Avg Leads | Avg CPL | Best For |
|---|---|---|---|---|---|
| Full Page (Colour) | 24 | ₹4,80,000 | 45 | ₹10,667 | Brand awareness, topper showcase |
| Half Page (Colour) | 68 | ₹2,20,000 | 28 | ₹7,857 | Admission drives, fee announcements |
| Quarter Page (Colour) | 112 | ₹85,000 | 12 | ₹7,083 | Regular admission reminders |
| Strip (Colour) | 45 | ₹35,000 | 5 | ₹7,000 | Helpline number visibility |
| Education Supplement | 38 | ₹1,50,000 | 32 | ₹4,688 | Best CPL — targeted readership |

---

## 6. Drawers & Modals

### 6.1 Modal: `add-insertion` (640px)
- **Title:** "Add Newspaper Insertion"
- **Fields:**
  - Publication (dropdown from publication master, required)
  - Edition (dropdown — dependent on publication, required)
  - Ad date (date picker, required)
  - Ad size (dropdown, required): Full Page / Half Page / Quarter Page / Strip / Classified / Custom
  - Position (dropdown): Front Page / Back Page / Inside / Education Supplement / Run of Paper
  - Colour (toggle): Colour / B&W
  - Rate card cost (₹, auto-filled from publication master, editable)
  - Actual cost (₹, required — after negotiation/discount)
  - Agency / Vendor (dropdown)
  - Campaign (dropdown — link to campaign)
  - Branch helpline number(s) printed (multi-select branches)
  - Creative artwork (link from O-03 material library or upload)
  - Booking reference (text)
  - Notes (textarea)
- **Buttons:** Cancel · Save as Booked
- **Access:** Role 119 or G4+

### 6.2 Modal: `bulk-import` (560px)
- **Title:** "Bulk Import Insertions"
- **Description:** "Upload an Excel file with multiple newspaper insertions."
- **Template download:** [Download Template XLSX]
- **File upload:** Drag-and-drop XLSX, max 5 MB
- **Behaviour:** Parse → preview table → confirm → create records
- **Access:** Role 119 or G4+

### 6.3 Modal: `log-response` (480px)
- **Title:** "Log Ad Response — [Publication] [Date]"
- **Fields:**
  - Leads received (integer — helpline calls + walk-ins mentioning this ad)
  - Source attribution method (dropdown): Helpline tracking / Walk-in mentioned / Coupon code / UTM / Estimated
  - Branch-wise breakdown (if multi-branch ad):
    - Branch A: [N] leads
    - Branch B: [N] leads
  - Notes (textarea)
- **Buttons:** Cancel · Save Response
- **Note:** Leads entered here are linked to the lead pipeline (O-15) with source = "Newspaper: [Publication] [Date]"

### 6.4 Drawer: `insertion-detail` (640px, right-slide)
- **Tabs:** Details · Creative · Response · Cost · Invoice
- **Details tab:** All insertion metadata, publication, edition, size, date, campaign
- **Creative tab:** Full-size preview of the ad artwork
- **Response tab:** Leads attributed, branch-wise split, conversion status of those leads
- **Cost tab:** Rate card vs actual, discount %, agency commission, total with GST
- **Invoice tab:** Invoice details, payment status, receipt upload
- **Footer:** [Edit] [Log Response] [Upload Invoice] [Cancel Insertion]

---

## 7. Charts

### 7.1 Monthly Newspaper Spend (Bar Chart)

| Property | Value |
|---|---|
| Chart type | Bar (Chart.js 4.x) |
| Title | "Monthly Newspaper Ad Spend — Current Season" |
| Data | Monthly total spend on newspaper ads |
| Colour | `#1E40AF` dark blue |
| Tooltip | "[Month]: ₹[X] across [N] insertions" |
| API | `GET /api/v1/group/{id}/marketing/newspaper/analytics/monthly-spend/` |

### 7.2 CPL by Publication (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Cost per Lead by Publication" |
| Data | CPL per publication (min 5 insertions) |
| Colour | Green ≤ ₹5,000 / Amber ₹5,001–₹10,000 / Red > ₹10,000 per bar |
| API | `GET /api/v1/group/{id}/marketing/newspaper/analytics/cpl-by-publication/` |

### 7.3 Response by Day of Week (Bar)

| Property | Value |
|---|---|
| Chart type | Vertical bar |
| Title | "Average Ad Response by Day of Week" |
| Data | Average leads per insertion, grouped by day of week |
| Colour | `#3B82F6` blue with highest day highlighted green |
| Insight | Most Indian education newspaper ads perform best on Sundays (family reading) and Wednesdays (mid-week supplements) |
| API | `GET /api/v1/group/{id}/marketing/newspaper/analytics/response-by-day/` |

### 7.4 Spend vs Response Scatter

| Property | Value |
|---|---|
| Chart type | Scatter (Chart.js 4.x) |
| Title | "Ad Cost vs Lead Response" |
| Data | Each point = one insertion; X = cost, Y = leads |
| Colour | Green = above efficiency line / Red = below |
| Tooltip | "[Publication] [Edition] [Date]: ₹[X] → [Y] leads (CPL: ₹[Z])" |
| API | `GET /api/v1/group/{id}/marketing/newspaper/analytics/spend-vs-response/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Insertion added | "Insertion added: [Publication] [Edition] — [Date] — [Size]" | Success | 3s |
| Insertion updated | "Insertion updated" | Success | 2s |
| Response logged | "[N] leads logged for [Publication] [Date]" | Success | 3s |
| Bulk import complete | "[N] insertions imported successfully" | Success | 4s |
| Insertion cancelled | "Insertion cancelled: [Publication] [Date]" | Info | 3s |
| Invoice uploaded | "Invoice uploaded for [Publication] [Date]" | Success | 2s |
| Export ready | "Newspaper tracker export ready for download" | Success | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No insertions recorded | 📰 | "No Newspaper Ads Tracked" | "Add your first newspaper insertion to start tracking ad performance." | Add Insertion |
| No publications in master | 📋 | "Publication Master Empty" | "Add publications and rate cards before booking insertions." | Open Publication Master |
| No response logged | 📊 | "No Response Data" | "Log ad responses to track which publications deliver the best leads." | — |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/newspaper/` | G1+ | List insertions (paginated, filterable) |
| GET | `/api/v1/group/{id}/marketing/newspaper/{insertion_id}/` | G1+ | Single insertion detail |
| POST | `/api/v1/group/{id}/marketing/newspaper/` | G3+ | Add insertion |
| PUT | `/api/v1/group/{id}/marketing/newspaper/{insertion_id}/` | G3+ | Update insertion |
| PATCH | `/api/v1/group/{id}/marketing/newspaper/{insertion_id}/response/` | G3+ | Log ad response |
| PATCH | `/api/v1/group/{id}/marketing/newspaper/{insertion_id}/status/` | G3+ | Cancel insertion |
| POST | `/api/v1/group/{id}/marketing/newspaper/{insertion_id}/invoice/` | G3+ | Upload invoice |
| POST | `/api/v1/group/{id}/marketing/newspaper/bulk-import/` | G3+ | Bulk import XLSX |
| GET | `/api/v1/group/{id}/marketing/newspaper/publications/` | G1+ | Publication master list |
| POST | `/api/v1/group/{id}/marketing/newspaper/publications/` | G3+ | Add publication |
| PUT | `/api/v1/group/{id}/marketing/newspaper/publications/{pub_id}/` | G3+ | Update publication/rates |
| GET | `/api/v1/group/{id}/marketing/newspaper/calendar/` | G1+ | Calendar view data |
| GET | `/api/v1/group/{id}/marketing/newspaper/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/newspaper/analytics/monthly-spend/` | G1+ | Monthly spend chart |
| GET | `/api/v1/group/{id}/marketing/newspaper/analytics/cpl-by-publication/` | G1+ | CPL chart |
| GET | `/api/v1/group/{id}/marketing/newspaper/analytics/response-by-day/` | G1+ | Day-of-week chart |
| GET | `/api/v1/group/{id}/marketing/newspaper/analytics/spend-vs-response/` | G1+ | Scatter plot data |
| POST | `/api/v1/group/{id}/marketing/newspaper/export/` | G1+ | Export report |

---

## 11. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../newspaper/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Insertion table | `<div id="insertion-table">` | `hx-get=".../newspaper/"` | `#insertion-table-body` | `innerHTML` | `hx-trigger="load"` |
| Filter apply | Filter controls | `hx-get` with params | `#insertion-table-body` | `innerHTML` | `hx-trigger="change"` |
| Calendar view | Calendar tab | `hx-get=".../newspaper/calendar/?month={m}"` | `#calendar-content` | `innerHTML` | `hx-trigger="click"` |
| Insertion detail drawer | Row click | `hx-get=".../newspaper/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Add insertion | Form submit | `hx-post=".../newspaper/"` | `#add-result` | `innerHTML` | Toast + table refresh |
| Log response | Response form | `hx-patch=".../newspaper/{id}/response/"` | `#response-cell-{id}` | `innerHTML` | Inline CPL update |
| Bulk import | Upload form | `hx-post=".../newspaper/bulk-import/"` | `#import-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Publication master | Tab/link | `hx-get=".../newspaper/publications/"` | `#pub-master-content` | `innerHTML` | Separate section |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#insertion-table-body` | `innerHTML` | Table body only |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
