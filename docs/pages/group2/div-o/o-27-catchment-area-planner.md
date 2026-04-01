# O-27 — Catchment Area Planner

> **URL:** `/group/marketing/enrollment/catchment/`
> **File:** `o-27-catchment-area-planner.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary planner

---

## 1. Purpose

The Catchment Area Planner is the geographic intelligence layer for the entire marketing and enrollment operation — it maps where students actually come from (pin-code-wise), identifies under-penetrated zones, overlays competitor presence, and directs ground-level campaigns to the highest-potential areas. In Indian education, every branch has a natural catchment — typically a 5–15 km radius from which 80–90% of its students are drawn. A branch in Kukatpally (Hyderabad) doesn't compete with a branch in Dilsukhnagar; they compete with rival institutions within their own 5–10 km radius. Understanding this geographic reality is the difference between spending ₹10L on pamphlets everywhere and spending ₹3L on pamphlets in the 8 pin codes that actually convert.

The problems this page solves:

1. **Blind marketing spend:** Without catchment analysis, Campaign Managers allocate outdoor/pamphlet/auto-rickshaw budgets uniformly across areas. A branch in Miyapur might spend ₹2L on auto branding in Madhapur — but zero students from Madhapur enrol because three strong competitors sit between the two areas. Catchment data shows which pin codes actually send students and which are dead zones, preventing wasted spend.

2. **Pin-code-level enrollment intelligence:** India's 6-digit pin code system provides a natural geographic granularity. By mapping each enrolled student's residential pin code to their branch, the platform builds a precise picture: "Pin 500072 (Kukatpally) sends 340 students to our Kukatpally branch, 500049 (Miyapur) sends 180, 500018 (Mehdipatnam) sends only 12 — too far, don't spend there." This pin-code-student matrix is the foundation for all geographic decisions.

3. **Competitor mapping:** Parents choose between 2–5 institutions within their catchment. If a competitor opens a new branch in pin code 500072, student flow from that pin code may drop 20–30% next season. The planner overlays competitor school locations so the Campaign Manager can see: "We're strong in 500072 but Competitor X just opened 1.2 km from us — we need defensive marketing there."

4. **Campaign targeting:** Outdoor campaigns (O-14), pamphlet drops, auto-rickshaw branding, and society-gate boards should be concentrated in high-potential pin codes. The planner directly feeds O-14 with target-area recommendations: "Deploy 50 autos in pin codes 500072, 500049, 500085 — these are high-density, under-penetrated areas."

5. **Expansion planning:** When the group evaluates opening a new branch, catchment data reveals geographic gaps — "We draw 500 students from Shamshabad area (30 km from nearest branch) — a new branch there could capture 800+ from surrounding pin codes." This is strategic intelligence for G4/G5 leadership.

6. **Year-over-year trend:** Catchment boundaries shift. A new metro line, a highway bypass, or a competitor closure can redirect student flow. Tracking pin-code-wise enrollment YoY reveals expanding and contracting catchments, enabling proactive campaign adjustment.

**Scale:** 5–50 branches · 50–500 unique pin codes in catchment · 500–50,000 enrolled students mapped · 10–100 competitor locations tracked · 3–5 year YoY trend data

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — define catchments, map competitors, set target areas, trigger campaigns | Primary planner |
| Group Admission Data Analyst | 132 | G1 | Read + Export — pin-code analytics, heatmaps, trend data | Reporting and insights |
| Group Topper Relations Manager | 120 | G3 | Read — catchment overlap with topper feeder schools | Cross-reference |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve catchment strategy, new-branch feasibility | Strategic decisions |
| Group CFO / Finance Director | 30 | G1 | Read — revenue density per catchment area | Revenue geography |
| Branch Principal | — | G3 | Read (own branch) — see own branch's catchment map and student distribution | Local awareness |
| Branch Admin Staff | — | G2 | Read (own branch) — view catchment summary | Context for walk-in enquiries |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Catchment definition and competitor mapping: role 119 or G4+. Branch staff filtered to `branch_id = user.branch_id`. Export: G1+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Enrollment Drives  ›  Catchment Area Planner
```

### 3.2 Page Header
```
Catchment Area Planner                               [+ Add Competitor]  [Define Catchment]  [Export Report]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · 28 branches mapped · 312 pin codes · 18,420 students geo-tagged · 64 competitors tracked
```

---

## 4. KPI Summary Bar (8 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Pin Codes Mapped | Integer | COUNT(DISTINCT pin_code) WHERE student_count > 0 | Static blue | `#kpi-pincodes` |
| 2 | Students Geo-tagged | Integer + % | COUNT(students with valid pin code) / total enrolled × 100 | Green ≥ 95%, Amber 80–95%, Red < 80% | `#kpi-geotagged` |
| 3 | Avg Catchment Radius | km | AVG of 80th-percentile distance per branch | Static blue | `#kpi-avg-radius` |
| 4 | Top Pin Code | Pin + Count | Pin code with highest student count across group | Static green | `#kpi-top-pincode` |
| 5 | Under-penetrated Zones | Integer | Pin codes with high population density but < 5 students enrolled | Red > 20, Amber 10–20, Green < 10 | `#kpi-underpenetrated` |
| 6 | Competitor Locations | Integer | COUNT(competitor_locations) | Static amber | `#kpi-competitors` |
| 7 | Campaign Coverage | % | Pin codes with active outdoor campaign (O-14) / total catchment pin codes × 100 | Green ≥ 80%, Amber 50–80%, Red < 50% | `#kpi-coverage` |
| 8 | YoY Catchment Growth | ± % | (This season pin codes − last season pin codes) / last season × 100 | Green > 0%, Red ≤ 0% | `#kpi-yoy` |

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Heatmap** — Student density heatmap on interactive map
2. **Pin Code Matrix** — Tabular pin-code-wise student distribution per branch
3. **Competitor Map** — Competitor school locations overlaid on catchment
4. **Target Areas** — Campaign targeting recommendations
5. **Trend Analysis** — YoY catchment expansion/contraction

### 5.2 Tab 1: Heatmap

Interactive map (Leaflet.js with OpenStreetMap tiles) showing student density by pin code.

**Map layers (toggleable):**

| Layer | Description | Default |
|---|---|---|
| Student Density Heatmap | Colour gradient from blue (low) → yellow → red (high) based on student count per pin code centroid | ON |
| Branch Markers | Pin markers for each branch location | ON |
| Catchment Radius | Concentric circles (5 km / 10 km / 15 km) around each branch | OFF |
| Competitor Markers | Red triangle markers for competitor schools | OFF |
| Pin Code Boundaries | Pin code area outlines (from India Post geo-data) | OFF |
| Campaign Overlay | Green markers showing active outdoor installations from O-14 | OFF |

**Map controls:**
- **Branch filter:** Dropdown to isolate single branch's catchment
- **Season selector:** Compare current season vs previous seasons
- **Density mode:** Toggle between absolute count and percentage of branch enrollment
- **Zoom:** City-level (all branches) → Area-level (single branch + surrounding) → Street-level (individual pin codes)

**Pin code popup (on hover/click):**
```
Pin Code: 500072 — Kukatpally
Students Enrolled: 340 (8.2% of Kukatpally branch)
Branch Served: Kukatpally (3.2 km)
Nearest Competitor: ABC Academy (1.8 km)
YoY Change: +42 students (+14%)
Active Campaigns: 3 (12 autos, 2 standees, 1 wall painting)
[View Pin Code Detail] [Target for Campaign]
```

**Branch popup (on marker click):**
```
Kukatpally Branch
Total Enrolled: 4,140 · Pin Codes: 38
Primary Catchment (80%): 12 pin codes within 8 km
Secondary Catchment (15%): 18 pin codes, 8–15 km
Outlier (5%): 8 pin codes, > 15 km
Competitors in Catchment: 6
[View Branch Catchment Detail]
```

### 5.3 Tab 2: Pin Code Matrix

**Filter bar:** Branch · Season · Min Student Count · Distance Range · Sort Order

**Master table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Pin Code | Text | Yes | 6-digit Indian pin code |
| Area Name | Text | Yes | Locality/area corresponding to pin code |
| Branch | Text | Yes | Nearest/assigned branch |
| Distance (km) | Decimal | Yes | Distance from branch to pin code centroid |
| Students (Current) | Integer | Yes | Enrolled students this season from this pin code |
| Students (Previous) | Integer | Yes | Last season count |
| YoY Change | Delta + badge | Yes | Green (↑) / Red (↓) / Grey (—) |
| % of Branch Enrollment | Percentage | Yes | This pin code's students / total branch enrollment |
| Competitor Count | Integer | Yes | Number of competitor schools in or near this pin code |
| Lead Count | Integer | Yes | Leads from O-15 originating in this pin code |
| Conversion Rate | Percentage | Yes | Students enrolled / leads from this pin code × 100 |
| Active Campaigns | Integer | Yes | Outdoor campaigns from O-14 running in this pin code |
| Penetration Score | Badge | Yes | High (green) / Medium (amber) / Low (red) / Untapped (grey) |
| Actions | Buttons | No | [View Detail] [Target for Campaign] |

**Penetration score logic:**
- **High:** > 2% of pin code school-age population enrolled (estimated from census data)
- **Medium:** 0.5–2% penetration
- **Low:** > 0 students but < 0.5% penetration
- **Untapped:** 0 students, pin code within catchment radius

**Summary row:** Totals for selected branch/group.
**Pagination:** Server-side · 50/page
**Export:** CSV with all columns including lat/long

### 5.4 Tab 3: Competitor Map

Interactive map focused on competitor presence within each branch's catchment.

**Competitor table (below map):**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Competitor Name | Text | Yes | School/college name |
| Type | Badge | Yes | Same Stream / Coaching / CBSE / State Board / International / Other |
| Location | Text | Yes | Address + pin code |
| Distance from Branch | Decimal | Yes | km from nearest own branch |
| Nearest Own Branch | Text | Yes | Which of our branches is closest |
| Estimated Strength | Integer | Yes | Estimated student count (manual input or public data) |
| Fee Range | Text | Yes | Approximate annual fee (₹) |
| Threat Level | Badge | Yes | High (red) / Medium (amber) / Low (green) — based on proximity + strength + fee similarity |
| Overlapping Pin Codes | Integer | Yes | Number of pin codes where both we and this competitor draw students |
| Our Student Loss (est.) | Integer | No | Estimated students we lose to this competitor per season |
| Notes | Text (truncated) | No | Campaign Manager's notes |
| Actions | Buttons | No | [View] [Edit] [View on Map] |

**Threat level calculation:**
- **High:** Within 3 km of our branch + similar fee range + similar stream offering + estimated strength > 500
- **Medium:** Within 5 km OR similar offering but different fee band
- **Low:** Beyond 5 km OR different stream/board entirely

### 5.5 Tab 4: Target Areas

Recommended and manually defined campaign targeting zones.

**Auto-generated recommendations:**

| Pin Code | Area | Branch | Opportunity | Rationale | Recommended Channel | Priority | Action |
|---|---|---|---|---|---|---|---|
| 500085 | Gachibowli | Kondapur | 120 est. potential students | High IT population, 0 competitors, 8 km from branch, only 15 students currently | Auto + Society Gate + Pamphlet | High | [Create Campaign] |
| 500049 | Miyapur | Kukatpally | 80 est. potential | Growing residential area, 1 weak competitor, YoY +30% growth | Auto + Wall Painting | Medium | [Create Campaign] |
| 500032 | Secunderabad | Secunderabad | Defensive | Competitor opened new branch, our enrollment down 22% YoY | Newspaper + Flex + Event Sponsorship | High | [Create Campaign] |

**Recommendation engine logic:**
1. **Under-penetrated high-density:** Pin codes with high school-age population but low current enrollment and few competitors
2. **Growing organically:** Pin codes showing YoY growth — double down with campaigns to accelerate
3. **Defensive:** Pin codes where enrollment is declining, especially if a new competitor has appeared
4. **Adjacent opportunity:** Pin codes just outside current catchment radius but accessible via transport

**Manual target area creation:**
- Campaign Manager can manually select pin codes and mark them as target areas with notes and assigned campaigns
- Bulk select from map (lasso tool) or table (checkbox multi-select)
- Link to O-14 to create outdoor campaigns in selected pin codes

### 5.6 Tab 5: Trend Analysis

Year-over-year catchment shift analytics.

**Trend table:**

| Column | Type | Notes |
|---|---|---|
| Pin Code | Text | — |
| Area | Text | — |
| Branch | Text | — |
| Season N-2 | Integer | Students 2 seasons ago |
| Season N-1 | Integer | Students last season |
| Season N (Current) | Integer | Students this season |
| 2-Year CAGR | Percentage | Compound annual growth rate |
| Trend | Sparkline | Mini line chart (3 data points) |
| Status | Badge | Growing (green) / Stable (blue) / Declining (red) / New (purple) / Lost (grey, was > 0, now 0) |

**Catchment shift summary:**
```
Kukatpally Branch — Catchment Shift Report (2024-25 → 2026-27)
Pin codes gained: 5 (new areas sending students)
Pin codes lost: 2 (areas that stopped sending students)
Expanding pin codes: 12 (YoY growth > 10%)
Contracting pin codes: 6 (YoY decline > 10%)
Net catchment health: Expanding (+8%)
```

---

## 6. Drawers & Modals

### 6.1 Modal: `define-catchment` (640px)

- **Title:** "Define Catchment — [Branch Name]"
- **Purpose:** Manually set or adjust the catchment boundary for a branch
- **Fields:**
  - Branch (dropdown, required)
  - Primary catchment radius (km, default 5)
  - Secondary catchment radius (km, default 10)
  - Extended catchment radius (km, default 15)
  - Included pin codes (multi-select or lasso-on-map): Explicitly include pin codes even if outside radius
  - Excluded pin codes (multi-select): Exclude pin codes within radius (e.g., across a river, no transport access)
  - Notes (textarea — explain non-obvious boundaries: "Railway line at 500034 blocks student flow")
- **Auto-populated:** Pin codes within each radius ring based on branch GPS coordinates
- **Buttons:** Cancel · Save Catchment Definition
- **Access:** Role 119 or G4+

### 6.2 Modal: `add-competitor` (560px)

- **Title:** "Add Competitor School"
- **Fields:**
  - School/college name (text, required)
  - Type (dropdown, required): Same Stream Competitor / Coaching Centre / CBSE School / State Board School / ICSE School / International School / Other
  - Address (text, required)
  - Pin code (6-digit, required)
  - GPS coordinates (lat/long — optional, auto-geocoded from pin code if blank)
  - City (text, auto-filled)
  - Streams offered (multi-select): MPC / BiPC / MEC / CEC / Foundation / Other
  - Classes (multi-select): relevant class range
  - Estimated strength (integer — approximate student count)
  - Annual fee range: Min (₹) – Max (₹)
  - Founded year (optional)
  - Website URL (optional)
  - Affiliated board (text — e.g., "TSBIE", "CBSE", "ICSE")
  - Key differentiators (textarea — what they offer that we don't)
  - Threat assessment (dropdown): High / Medium / Low
  - Source of information (dropdown): Public Data / Parent Feedback / Staff Intel / Website / Press / Other
  - Notes (textarea)
- **Buttons:** Cancel · Save Competitor
- **Access:** Role 119 or G4+

### 6.3 Drawer: `pincode-detail` (720px, right-slide)

- **Tabs:** Overview · Students · Leads · Campaigns · Competitors · Trend
- **Overview tab:**
  - Pin code, area name, city, state
  - Distance from nearest branch
  - Student count (current + last 3 seasons)
  - Estimated school-age population (from census/external data)
  - Penetration rate
  - Competitor count in/near this pin code
  - Active campaigns count
  - Mini map showing pin code area with branch and competitor markers
- **Students tab:** List of enrolled students from this pin code — name, class, stream, branch, enrollment date (linked to O-22)
- **Leads tab:** Leads from O-15 originating in this pin code — stage, source, assigned telecaller
- **Campaigns tab:** Active outdoor campaigns (O-14) deployed in this pin code — type, vendor, lead attribution
- **Competitors tab:** Competitor schools located in or within 2 km of this pin code
- **Trend tab:** 3–5 year enrollment trend from this pin code (bar chart) + YoY change
- **Footer:** [Target for Campaign] [Add to Watchlist] [Export Pin Code Report]

### 6.4 Drawer: `competitor-detail` (640px, right-slide)

- **Tabs:** Profile · Catchment Overlap · Threat Analysis · History
- **Profile tab:** All competitor details — name, type, location, streams, fee, strength, website
- **Catchment Overlap tab:** List of pin codes where we both draw students — our count vs estimated competitor count per pin code
- **Threat Analysis tab:**
  - Distance from each of our branches
  - Overlapping pin code count
  - Estimated student loss per season
  - Fee comparison (their range vs ours)
  - Stream comparison
  - Suggested defensive actions
- **History tab:** When competitor was added, edits over time, any notes/intel logged
- **Footer:** [Edit] [View on Map] [Delete] [Link Defensive Campaign]

### 6.5 Modal: `target-area-campaign` (560px)

- **Title:** "Create Targeted Campaign — [Pin Code / Area]"
- **Pre-filled:** Pin code(s), area name, nearest branch, student count, competitor presence
- **Fields:**
  - Campaign name (auto-generated: "Catchment Push — [Area] — [Date]")
  - Target pin codes (multi-select, pre-filled from selection)
  - Recommended channels (pre-selected based on area type):
    - Residential area → Society gate boards + pamphlets
    - Main road area → Auto-rickshaw + flex banners
    - Market area → Standees + wall painting
    - IT corridor → Digital + WhatsApp (not outdoor)
  - Budget allocation (₹, from O-09)
  - Duration: Start → End
  - Link to O-14 outdoor activity (auto-create)
  - Notes (textarea)
- **Buttons:** Cancel · Create Campaign
- **Behaviour:** Creates linked outdoor campaign entry in O-14 with pin-code targeting pre-filled
- **Access:** Role 119 or G4+

---

## 7. Charts

### 7.1 Student Density Heatmap (Map)

| Property | Value |
|---|---|
| Chart type | Map heatmap (Leaflet.js + leaflet-heat plugin) |
| Title | "Student Density — Season [Year]" |
| Data | Pin code centroids weighted by student count |
| Colour | Blue (1–10 students) → Green (10–50) → Yellow (50–150) → Orange (150–300) → Red (300+) |
| Controls | Branch filter, season toggle, density mode |
| API | `GET /api/v1/group/{id}/marketing/enrollment/catchment/heatmap/` |

### 7.2 Pin Code Distribution (Horizontal Bar — Top 20)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Top 20 Pin Codes by Student Count — [Branch / Group]" |
| Data | Top 20 pin codes by enrollment count |
| Colour | `#3B82F6` blue; highlighted pin codes with YoY growth > 20% in `#10B981` green |
| Tooltip | "[Pin Code] — [Area]: [N] students ([X]% of branch)" |
| API | `GET /api/v1/group/{id}/marketing/enrollment/catchment/analytics/top-pincodes/` |

### 7.3 Catchment Radius Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Enrollment by Distance — [Branch]" |
| Data | Students grouped by distance ring: 0–5 km / 5–10 km / 10–15 km / > 15 km |
| Colour | `#10B981` (0–5) / `#3B82F6` (5–10) / `#F59E0B` (10–15) / `#EF4444` (>15) |
| Centre text | Total: [N] students |
| API | `GET /api/v1/group/{id}/marketing/enrollment/catchment/analytics/radius-distribution/` |

### 7.4 YoY Catchment Trend (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Catchment Trend — Top 15 Pin Codes (3-Year)" |
| Data | Per pin code: 3 bars (Season N-2, N-1, N) showing student count |
| Colour | Light grey (N-2) / Medium blue (N-1) / Dark blue (N) |
| Tooltip | "[Pin Code]: [Year] — [N] students" |
| API | `GET /api/v1/group/{id}/marketing/enrollment/catchment/analytics/yoy-trend/` |

### 7.5 Competitor Proximity (Scatter)

| Property | Value |
|---|---|
| Chart type | Scatter (Chart.js 4.x) |
| Title | "Competitor Proximity vs Our Enrollment Impact" |
| Data | Each dot = one competitor; X = distance from our branch (km); Y = our enrollment count in overlapping pin codes |
| Point size | Proportional to competitor estimated strength |
| Colour | Red (high threat) / Amber (medium) / Green (low) |
| Insight | Close + large competitors should correlate with lower enrollment in overlapping areas |
| API | `GET /api/v1/group/{id}/marketing/enrollment/catchment/analytics/competitor-proximity/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Catchment defined | "Catchment defined for [Branch] — [N] pin codes in primary zone" | Success | 3s |
| Catchment updated | "Catchment updated for [Branch] — [N] pin codes added, [M] removed" | Success | 3s |
| Competitor added | "Competitor '[Name]' added at [Pin Code] — threat level: [Level]" | Success | 3s |
| Competitor updated | "Competitor '[Name]' updated" | Success | 2s |
| Competitor deleted | "Competitor '[Name]' removed" | Info | 2s |
| Target area created | "Target area created — [N] pin codes flagged for campaign" | Success | 3s |
| Campaign linked | "Campaign created in O-14 for [Area] — [N] pin codes targeted" | Success | 4s |
| Heatmap refreshed | "Heatmap refreshed with latest enrollment data" | Info | 2s |
| Export started | "Catchment report export started — download will begin shortly" | Info | 3s |
| Low penetration alert | "⚠️ [N] pin codes within catchment have zero enrolled students" | Warning | 5s |
| Competitor threat | "⚠️ New competitor '[Name]' detected within 3 km of [Branch]" | Warning | 6s |
| Catchment contraction | "⚠️ [Branch] catchment has contracted — [N] pin codes lost vs last season" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No pin code data | 📍 | "No Pin Code Data" | "Student address data is needed to build catchment maps. Ensure enrollment forms capture residential pin codes." | — |
| No catchment defined | 🗺️ | "No Catchment Defined" | "Define the catchment area for each branch to start geographic analysis." | Define Catchment |
| No competitors mapped | 🏫 | "No Competitors Mapped" | "Add competitor schools to understand the competitive landscape in each catchment." | Add Competitor |
| No target areas | 🎯 | "No Target Areas Set" | "Identify high-potential pin codes and mark them as campaign target areas." | View Recommendations |
| Branch not geo-coded | 📌 | "Branch Location Missing" | "[Branch] doesn't have GPS coordinates. Add location to enable catchment mapping." | Update Branch |
| No YoY data | 📊 | "Insufficient Trend Data" | "At least 2 seasons of enrollment data are needed for trend analysis." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 8 KPI shimmer cards + tab bar + map placeholder |
| Heatmap tab | Grey map rectangle with "Loading map…" + branch marker placeholders |
| Pin code matrix | Table skeleton (20 rows) |
| Competitor map | Grey map rectangle + table skeleton (10 rows) |
| Target areas | Recommendation cards skeleton (5 cards) |
| Pin code detail drawer | 720px skeleton: overview + 6 tabs |
| Competitor detail drawer | 640px skeleton: profile + 4 tabs |
| Chart load | Grey canvas placeholder per chart |
| Export generation | Spinner with "Generating report…" text |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/` | G1+ | Catchment summary — all branches |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/{branch_id}/` | G1+ | Branch catchment detail |
| POST | `/api/v1/group/{id}/marketing/enrollment/catchment/{branch_id}/define/` | G3+ | Define/update catchment boundaries |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/pincodes/` | G1+ | Pin code matrix (paginated) |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/pincodes/{pincode}/` | G1+ | Pin code detail |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/heatmap/` | G1+ | Heatmap data (pin code centroids + weights) |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/competitors/` | G1+ | List all competitors |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/competitors/{comp_id}/` | G1+ | Competitor detail |
| POST | `/api/v1/group/{id}/marketing/enrollment/catchment/competitors/` | G3+ | Add competitor |
| PUT | `/api/v1/group/{id}/marketing/enrollment/catchment/competitors/{comp_id}/` | G3+ | Update competitor |
| DELETE | `/api/v1/group/{id}/marketing/enrollment/catchment/competitors/{comp_id}/` | G3+ | Delete competitor |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/targets/` | G1+ | Target area recommendations |
| POST | `/api/v1/group/{id}/marketing/enrollment/catchment/targets/` | G3+ | Create target area + linked campaign |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/trends/` | G1+ | YoY trend data |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/analytics/top-pincodes/` | G1+ | Top pin codes bar chart |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/analytics/radius-distribution/` | G1+ | Distance donut |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/analytics/yoy-trend/` | G1+ | YoY grouped bar |
| GET | `/api/v1/group/{id}/marketing/enrollment/catchment/analytics/competitor-proximity/` | G1+ | Competitor scatter |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../catchment/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get=".../catchment/?tab={heatmap/pincodes/competitors/targets/trends}"` | `#catchment-content` | `innerHTML` | `hx-trigger="click"` |
| Heatmap load | Heatmap tab | JS-initiated Leaflet map + `fetch()` for heatmap data | — | — | Non-HTMX (Leaflet.js handles rendering) |
| Pin code table | Matrix tab | `hx-get=".../catchment/pincodes/"` | `#pincode-table-body` | `innerHTML` | `hx-trigger="load"` |
| Pin code filter | Filter change | `hx-get` with filter params | `#pincode-table-body` | `innerHTML` | `hx-trigger="change"` |
| Pin code detail drawer | Row click | `hx-get=".../catchment/pincodes/{pincode}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Competitor table | Competitor tab | `hx-get=".../catchment/competitors/"` | `#competitor-table-body` | `innerHTML` | `hx-trigger="load"` |
| Competitor detail drawer | Row click | `hx-get=".../catchment/competitors/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Add competitor | Form submit | `hx-post=".../catchment/competitors/"` | `#competitor-result` | `innerHTML` | Toast + table refresh |
| Define catchment | Form submit | `hx-post=".../catchment/{branch_id}/define/"` | `#catchment-result` | `innerHTML` | Toast + map refresh |
| Target area campaign | Form submit | `hx-post=".../catchment/targets/"` | `#target-result` | `innerHTML` | Toast + creates O-14 entry |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#pincode-table-body` | `innerHTML` | Table body only |
| Chart load | Analytics sections | `hx-get=".../catchment/analytics/..."` | `#chart-container-{name}` | `innerHTML` | Per chart |
| Branch filter on map | Branch dropdown | JS re-renders map with filtered data via `fetch()` | — | — | Non-HTMX (Leaflet.js) |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
