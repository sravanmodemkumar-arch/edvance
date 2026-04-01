# O-14 — Outdoor & BTL Campaign Tracker

> **URL:** `/group/marketing/campaigns/outdoor/`
> **File:** `o-14-outdoor-campaign-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary tracker

---

## 1. Purpose

The Outdoor & BTL (Below-The-Line) Campaign Tracker manages all non-digital, non-print-media marketing activities — the ground-level campaigns that penetrate local catchment areas around each branch. In the Indian education market, outdoor and BTL activities account for 10–20% of total marketing spend for large groups and are the primary marketing channel for small trusts that cannot afford newspaper ads. These activities include: auto-rickshaw back-panel branding, bus shelter ads, pamphlet distribution at traffic signals, standee placement at tuition centres, wall painting campaigns in semi-urban areas, school gate banner installations, society gate permission boards, and local event sponsorships.

The problems this page solves:

1. **Scattered execution:** BTL activities happen at 20–50 locations per branch simultaneously — auto-rickshaws run routes nobody tracks, pamphlets are distributed without knowing how many or where, wall paintings are done and forgotten. This page centralises all outdoor/BTL activity tracking with GPS-tagged locations, photos, and completion verification.

2. **Vendor management:** Each activity involves local vendors — auto-rickshaw unions (₹300–₹800/auto/month for back-panel ads), pamphlet distribution agencies (₹0.50–₹2 per pamphlet), wall painting contractors (₹5–₹15 per sq ft), standee fabricators. Without tracking, vendors bill for 1,000 autos when only 600 are actually running branded panels.

3. **ROI measurement:** Outdoor campaigns are notoriously hard to measure. The platform links each outdoor campaign to a unique phone number or QR code, enabling lead attribution. An auto-rickshaw ad with "Call 9876XXXXXX" routes to a tracking number tied to this campaign, so every call is counted.

4. **Compliance:** Municipal corporations (GHMC, BBMP, BMC) regulate outdoor advertising. Flex banners on public property get removed and fined (₹5,000–₹50,000). The platform tracks which installations have municipal permits and which are on private property (no permit needed).

**Scale:** 5–50 branches · 50–500 outdoor installations per season · 10–50 BTL activities per branch · ₹1–50L outdoor budget per branch per season

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — create, track, close outdoor campaigns | Primary manager |
| Group Campaign Content Coordinator | 131 | G2 | Read + Upload — creative artwork for outdoor installations | Manages artwork files |
| Group Admission Data Analyst | 132 | G1 | Read only — spend and ROI data | Analytics |
| Branch Admin Staff | — | G2 | Read + Update (own branch) — update installation status, upload verification photos | Ground verification |
| Group CFO / Finance Director | 30 | G1 | Read — spend data only | Cost oversight |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve high-value outdoor contracts | Approval for large spends |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. CRUD: role 119 or G4+. Branch staff filtered to `branch_id = user.branch_id`. Content upload: 131 or G3+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Campaign Planning  ›  Outdoor & BTL Campaign Tracker
```

### 3.2 Page Header
```
Outdoor & BTL Campaign Tracker                      [+ New Activity]  [Map View]  [Export Report]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · 142 active installations · 38 BTL activities · ₹18.4L spent
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Installations | Integer | COUNT(activities) WHERE status = 'active' | Static blue | `#kpi-active` |
| 2 | Total Spend (Season) | ₹ Amount | SUM(cost) WHERE season = current | Amber if > 90% budget, Green ≤ 90% | `#kpi-spend` |
| 3 | Leads Attributed | Integer | COUNT(leads) WHERE source IN ('outdoor','btl') from O-15 | Static green | `#kpi-leads` |
| 4 | Cost per Lead | ₹ Amount | Total outdoor spend / attributed leads | Green ≤ ₹500, Amber ₹500–₹1000, Red > ₹1000 | `#kpi-cpl` |
| 5 | Installations Expiring (30d) | Integer | COUNT WHERE end_date within 30 days | Red > 10, Amber 5–10, Green < 5 | `#kpi-expiring` |
| 6 | Pending Verification | Integer | COUNT WHERE verification_status = 'pending' | Red > 20, Amber 10–20, Green < 10 | `#kpi-pending-verify` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/campaigns/outdoor/kpis/"` → `hx-trigger="load"` → `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Activity List** — All outdoor/BTL activities in table view
2. **Map View** — GPS-plotted installations on map
3. **Vendor Tracker** — Vendor performance and payments
4. **Analytics** — Spend, reach, ROI charts

### 5.2 Tab 1: Activity List

**Filter bar:** Activity Type · Branch · Status (Active / Completed / Scheduled / Expired) · Vendor · Date Range · Verification Status

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Activity Name | Text (link) | Yes | Click → detail drawer |
| Type | Badge | Yes | Auto-Rickshaw / Bus Shelter / Wall Painting / Standee / Pamphlet Drop / Society Gate / School Gate Banner / Event Sponsorship / Traffic Signal / Other |
| Branch | Text | Yes | Target branch |
| Location / Area | Text | Yes | Specific location or area covered |
| Quantity | Integer | Yes | Number of units (autos, standees, pamphlets, sq ft) |
| Start Date | Date | Yes | Campaign start |
| End Date | Date | Yes | Campaign end |
| Duration | Text | Yes | N days |
| Vendor | Text | Yes | Vendor name |
| Total Cost (₹) | Amount | Yes | Total cost for this activity |
| Tracking Code | Text | No | Unique phone number or QR code for lead attribution |
| Leads | Integer | Yes | Attributed leads from tracking code |
| Verification | Badge | Yes | Verified (green) / Pending (amber) / Failed (red) |
| Status | Badge | Yes | Scheduled (blue) / Active (green) / Completed (grey) / Expired (red) |
| Actions | Buttons | No | [View] [Verify] [Extend] [End] |

**Default sort:** Status (Active first) then End Date ASC
**Pagination:** Server-side · 25/page

### 5.3 Tab 2: Map View

Interactive map (Leaflet.js with OpenStreetMap tiles) showing all outdoor installations.

**Map features:**
- **Markers:** Each installation = pin on map; colour-coded by type (auto = yellow, hoarding = blue, wall painting = orange, etc.)
- **Cluster view:** At city zoom level, markers cluster with count badges
- **Branch radius:** Toggle to show 5 km / 10 km radius circles around each branch — ideal for catchment planning
- **Filter:** Same filters as Tab 1; map updates dynamically
- **Marker popup:**
  ```
  Auto-Rickshaw Branding — Route: Kukatpally–Miyapur
  Vendor: Sri Sai Auto Agency
  Quantity: 25 autos · ₹15,000/month
  Active: 15 Jan – 15 Apr 2026
  Leads: 42 calls via 9876543210
  [View Details] [Verify]
  ```
- **Heatmap layer:** Toggle to show lead density heatmap — where are outdoor campaigns generating the most calls?

### 5.4 Tab 3: Vendor Tracker

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Vendor Name | Text | Yes | Agency/contractor name |
| Type | Badge | Yes | Auto Agency / Printer / Wall Painter / Distribution / Fabricator / Event |
| Activities | Integer | Yes | Number of activities with this vendor |
| Total Value (₹) | Amount | Yes | Total contract value this season |
| Paid (₹) | Amount | Yes | Amount paid to date |
| Pending (₹) | Amount | Yes | Unpaid balance |
| Verification Pass % | Percentage | Yes | What % of this vendor's work passed verification |
| Rating | Stars (1–5) | Yes | Internal quality rating |
| Actions | Buttons | No | [View] [Rate] [Payment History] |

### 5.5 Tab 4: Analytics

Charts and metrics (see §7).

---

## 6. Drawers & Modals

### 6.1 Modal: `create-activity` (640px)

- **Title:** "Add Outdoor / BTL Activity"
- **Fields:**
  - Activity name (text, required — e.g., "Auto Branding — Kukatpally Routes")
  - Type (dropdown, required): Auto-Rickshaw Back Panel / Auto-Rickshaw Full Wrap / Bus Shelter Ad / Bus Side Panel / Wall Painting / Standee / Flex Banner / Pamphlet Distribution / Society Gate Board / School Gate Banner / Traffic Signal Standee / Event Sponsorship / Balloon/Kite Branding / Other
  - Branch (dropdown, required)
  - Location/Area (text, required — area name, route, or address)
  - GPS coordinates (lat/long, optional — for map pin)
  - Quantity (integer, required — number of units)
  - Unit description (text — "autos" / "standees" / "sq ft" / "pamphlets" / etc.)
  - Vendor (dropdown from vendor master + add new)
  - Cost breakdown:
    - Fabrication/Printing cost (₹)
    - Installation cost (₹)
    - Monthly rental (₹, if applicable — recurring)
    - Total cost (₹, auto-calculated or manual)
  - Start date (date, required)
  - End date (date, required)
  - Linked campaign from O-08 (optional)
  - Budget line from O-09 (dropdown)
  - Creative artwork (file upload — design file used for this installation)
  - Tracking code (auto-generated or manual):
    - Tracking phone number (dedicated number for this activity)
    - QR code URL (auto-generated with UTM params)
  - Municipal permit (toggle: Required / Not Required / Obtained)
    - If required: permit number, expiry date
  - Notes (textarea)
- **Buttons:** Cancel · Save
- **Access:** Role 119 or G4+

### 6.2 Modal: `verify-activity` (480px)

- **Title:** "Verify Installation — [Activity Name]"
- **Purpose:** Branch staff or campaign team verifies that the outdoor installation is actually live and matches specs.
- **Fields:**
  - Verification date (date, defaults to today)
  - Verification type (dropdown): In-Person / Photo Check / Vendor Report
  - Actual quantity verified (integer — may differ from ordered: "ordered 50 autos, only 38 found with branding")
  - Condition (dropdown): Good / Damaged / Faded / Missing / Partially Installed
  - Photos (upload, required — at least 1 photo of the installation in-situ)
  - GPS location (auto-captured from device if available)
  - Match with artwork? (toggle — does the actual installation match the approved design?)
  - Notes (textarea)
- **Buttons:** Cancel · Submit Verification
- **Behaviour:** If actual quantity < ordered, flags vendor for discrepancy. If condition = Damaged/Missing, triggers vendor notification.
- **Access:** Role 119, Branch Admin (own branch), or G4+

### 6.3 Drawer: `activity-detail` (640px, right-slide)

- **Tabs:** Details · Photos · Verification History · Leads · Cost
- **Details tab:** All activity fields, vendor info, tracking code, permit status
- **Photos tab:** Gallery of installation photos (from creation + all verifications), with date stamps
- **Verification History tab:** All verification entries — date, verifier, quantity found, condition, photos
- **Leads tab:** Calls/enquiries received via tracking code, linked to O-15 lead records
- **Cost tab:** Fabrication + installation + rental breakdown, vendor payment status, linked budget line
- **Footer:** [Edit] [Verify] [Extend] [End Activity] [Archive]

### 6.4 Modal: `extend-activity` (480px)

- **Title:** "Extend Activity Duration"
- **Pre-filled:** Current end date, vendor, monthly cost
- **Fields:**
  - New end date (date, required)
  - Additional cost (₹, if any)
  - Reason (dropdown): Performing Well / Admission Season Extension / Vendor Offered Discount / Other
  - Notes (textarea)
- **Buttons:** Cancel · Extend
- **Access:** Role 119 or G4+

---

## 7. Charts

### 7.1 Spend by Activity Type (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Outdoor Spend by Activity Type — Season [Year]" |
| Data | SUM(cost) grouped by activity type |
| Colour | Distinct colour per type |
| Centre text | Total: ₹[X] |
| Tooltip | "[Type]: ₹[X] ([Y]% of outdoor budget)" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/outdoor/analytics/spend-by-type/` |

### 7.2 Lead Attribution by Activity Type (Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Leads Generated by Outdoor Activity Type" |
| Data | COUNT(leads) per activity type |
| Colour | `#10B981` green |
| Tooltip | "[Type]: [N] leads (CPL: ₹[X])" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/outdoor/analytics/leads-by-type/` |

### 7.3 Branch Outdoor Coverage (Map Heatmap)

| Property | Value |
|---|---|
| Chart type | Map heatmap (Leaflet.js heat layer) |
| Title | "Outdoor Campaign Coverage" |
| Data | GPS points of all installations, weighted by lead count |
| Colour | Blue (low density) → Red (high density) |
| Purpose | Identify coverage gaps and high-performing zones |
| API | `GET /api/v1/group/{id}/marketing/campaigns/outdoor/analytics/coverage-heatmap/` |

### 7.4 Vendor Performance (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped horizontal bar |
| Title | "Vendor Performance — Ordered vs Verified Quantity" |
| Data | Per vendor: ordered quantity (bar 1) vs verified quantity (bar 2) |
| Colour | Ordered: `#93C5FD` light blue; Verified: `#3B82F6` blue (red if < 80% match) |
| Tooltip | "[Vendor]: Ordered [N], Verified [M] ([X]% match)" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/outdoor/analytics/vendor-performance/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Activity created | "Activity '[Name]' created — [N] [units] at [Location]" | Success | 3s |
| Activity verified | "Verification submitted — [N]/[M] units confirmed" | Success | 3s |
| Quantity discrepancy | "Warning: Verified [N] vs ordered [M] — vendor flagged" | Warning | 5s |
| Activity extended | "Activity '[Name]' extended to [New End Date]" | Success | 3s |
| Activity ended | "Activity '[Name]' ended — total spend: ₹[X]" | Info | 3s |
| Lead attributed | "New lead from outdoor tracking — [Phone] via [Activity]" | Info | 3s |
| Permit expiring | "Municipal permit for [Location] expires in [N] days" | Warning | 5s |
| Vendor rated | "Vendor '[Name]' rated [N]/5 stars" | Success | 2s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No outdoor activities | 🪧 | "No Outdoor Campaigns" | "Add your first outdoor or BTL activity to start tracking ground-level campaigns." | New Activity |
| No activities for branch | 🏫 | "No Activities for [Branch]" | "No outdoor campaigns are active for your branch." | — |
| No map pins | 🗺️ | "No Locations Plotted" | "Add GPS coordinates to outdoor activities to see them on the map." | — |
| No vendors | 👷 | "No Vendors Added" | "Add your first outdoor advertising vendor." | — |
| No leads attributed | 📊 | "No Leads Tracked" | "Leads will appear when tracking codes (phone/QR) receive responses." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + tab bar + table skeleton (10 rows) |
| Tab switch | Content area skeleton |
| Map view load | Grey map rectangle with "Loading map…" + marker placeholders |
| Activity detail drawer | 640px skeleton: photo gallery placeholder + 5 tabs |
| Photo upload | Progress bar in modal |
| Chart load | Grey canvas placeholder |
| Vendor tracker load | Table skeleton (8 rows) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/campaigns/outdoor/` | G1+ | List all outdoor activities |
| GET | `/api/v1/group/{id}/marketing/campaigns/outdoor/{act_id}/` | G1+ | Activity detail |
| POST | `/api/v1/group/{id}/marketing/campaigns/outdoor/` | G3+ | Create activity |
| PUT | `/api/v1/group/{id}/marketing/campaigns/outdoor/{act_id}/` | G3+ | Update activity |
| PATCH | `/api/v1/group/{id}/marketing/campaigns/outdoor/{act_id}/extend/` | G3+ | Extend activity |
| PATCH | `/api/v1/group/{id}/marketing/campaigns/outdoor/{act_id}/end/` | G3+ | End activity |
| DELETE | `/api/v1/group/{id}/marketing/campaigns/outdoor/{act_id}/` | G4+ | Delete activity |
| POST | `/api/v1/group/{id}/marketing/campaigns/outdoor/{act_id}/verify/` | G2+ | Submit verification |
| GET | `/api/v1/group/{id}/marketing/campaigns/outdoor/{act_id}/verifications/` | G1+ | Verification history |
| GET | `/api/v1/group/{id}/marketing/campaigns/outdoor/{act_id}/leads/` | G1+ | Attributed leads |
| GET | `/api/v1/group/{id}/marketing/campaigns/outdoor/vendors/` | G1+ | List vendors |
| POST | `/api/v1/group/{id}/marketing/campaigns/outdoor/vendors/{vid}/rate/` | G3+ | Rate vendor |
| GET | `/api/v1/group/{id}/marketing/campaigns/outdoor/map-data/` | G1+ | Map pins and clusters |
| GET | `/api/v1/group/{id}/marketing/campaigns/outdoor/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/campaigns/outdoor/analytics/spend-by-type/` | G1+ | Spend donut |
| GET | `/api/v1/group/{id}/marketing/campaigns/outdoor/analytics/leads-by-type/` | G1+ | Lead bar chart |
| GET | `/api/v1/group/{id}/marketing/campaigns/outdoor/analytics/coverage-heatmap/` | G1+ | Heatmap data |
| GET | `/api/v1/group/{id}/marketing/campaigns/outdoor/analytics/vendor-performance/` | G1+ | Vendor chart |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../outdoor/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get=".../outdoor/?tab={list/map/vendors/analytics}"` | `#outdoor-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Filter dropdowns | `hx-get` with params | `#outdoor-table-body` | `innerHTML` | `hx-trigger="change"` |
| Activity detail drawer | Row click | `hx-get=".../outdoor/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create activity | Form submit | `hx-post=".../outdoor/"` | `#create-result` | `innerHTML` | Toast + table refresh |
| Verify activity | Verify form | `hx-post=".../outdoor/{id}/verify/"` | `#verify-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Map load | Tab switch to map | JS-initiated Leaflet map + `fetch()` for pin data | — | — | Non-HTMX (Leaflet.js handles rendering) |
| Extend activity | Extend form | `hx-patch=".../outdoor/{id}/extend/"` | `#extend-result` | `innerHTML` | Toast |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#outdoor-table-body` | `innerHTML` | Table body |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
