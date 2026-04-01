# O-04 — Branch Signage & Hoarding Tracker

> **URL:** `/group/marketing/brand/signage/`
> **File:** `o-04-branch-signage-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Campaign Content Coordinator (Role 131, G2) — primary tracker

---

## 1. Purpose

The Branch Signage & Hoarding Tracker is a centralised inventory and compliance system for all physical signage, outdoor hoardings, flex banners, and branded installations across every branch in the group. In Indian education groups, outdoor branding is the single largest category of marketing spend — hoardings at busy junctions, flex banners on school gates, bus branding panels, auto-rickshaw back ads, and directional signboards consume 10–15% of the total marketing budget for large groups.

The problem this page solves is threefold:

1. **Inventory chaos:** A group with 30 branches might have 500+ physical signage installations — gate boards, building facades, classroom nameplates, direction signs, hoardings on rented sites, flex banners at junctions. Nobody knows exactly how many exist, where they are, what condition they're in, or when they were last updated. When the group updates its logo or tagline, half the branches still display the old version six months later.

2. **Rental tracking:** Outdoor hoardings (20×10 ft, 30×15 ft) are rented from hoarding agencies at monthly/quarterly rates. Without tracking, renewals get missed, payments duplicate, and prime locations are lost to competitors. During admission season, a Narayana or Sri Chaitanya group might rent 200+ hoarding sites across a state — each with different vendors, rates, and renewal dates.

3. **Compliance enforcement:** Municipal corporations (GHMC, BBMP, etc.) have strict rules on signage sizes, illumination, and permissions. Unauthorised hoardings get removed, and penalties range from ₹5,000 to ₹50,000 per instance. The platform tracks municipal approvals and expiry dates.

**Scale:** 5–50 branches · 100–1,000 permanent signage items · 50–300 rented hoardings (seasonal) · 200–2,000 flex banners (seasonal)

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Campaign Content Coordinator | 131 | G2 | Full CRUD — add, edit, archive signage records | Primary tracker manager |
| Group Admissions Campaign Manager | 119 | G3 | Read + Approve hoarding rentals | Approves rental commitments |
| Group Admission Data Analyst | 132 | G1 | Read only | View inventory and spend data |
| Branch Admin Staff | — | G2 | Read + Update (own branch signage only) | Updates condition, photos |
| Group CFO / Finance Director | 30 | G1 | Read — spend data only | Monitors hoarding rental spend |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. CRUD restricted to role 131 or G4+. Branch staff filtered to `branch_id = user.branch_id`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Brand & Content  ›  Signage & Hoarding Tracker
```

### 3.2 Page Header
```
Branch Signage & Hoarding Tracker              [Add Signage]  [Add Hoarding]  [Export Report]
Content Coordinator — Meena Raghavan
Sunrise Education Group · 28 branches · 412 signage items · 87 active hoardings
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Signage Items | Integer | COUNT(signage) WHERE status = 'active' | Static blue | `#kpi-total-signage` |
| 2 | Active Hoardings | Integer | COUNT(hoardings) WHERE status = 'active' | Static blue | `#kpi-active-hoardings` |
| 3 | Monthly Rental Spend | ₹ Amount | SUM(hoarding_monthly_rent) WHERE status = 'active' | Amber if > budget, Green if ≤ budget | `#kpi-rental-spend` |
| 4 | Renewals Due (30 days) | Integer | COUNT(hoardings) WHERE renewal_date within 30 days | Red > 10, Amber 5–10, Green < 5 | `#kpi-renewals-due` |
| 5 | Brand Non-Compliant | Integer | COUNT(signage) WHERE brand_compliant = FALSE | Red > 0, Green = 0 | `#kpi-non-compliant` |
| 6 | Municipal Permits Expiring | Integer | COUNT(signage) WHERE permit_expiry within 30 days | Red > 0, Amber if any within 60d, Green = none | `#kpi-permits-expiring` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/signage/kpis/"` → `hx-trigger="load"` → `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Tab Navigation

Three main tabs:
1. **Permanent Signage** — Gate boards, building facades, classroom nameplates, direction signs
2. **Hoardings & Outdoor** — Rented hoardings, bus shelters, junction banners
3. **Flex & Temporary** — Event banners, admission season flex, auto-rickshaw ads

### 5.2 Tab 1: Permanent Signage

**Filter bar:** Branch (dropdown) · Type (dropdown) · Condition (Good / Fair / Poor / Damaged) · Brand Compliant (Yes / No / All) · Installed Year

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Photo | Thumbnail (60×60 px) | No | Latest photo of the signage |
| Branch | Text | Yes | Branch name + city |
| Signage Type | Badge | Yes | Gate Board / Facade / Nameplate / Direction / Bus Panel / Other |
| Location | Text | Yes | Specific location description (e.g., "Main gate — left side") |
| Dimensions | Text | Yes | W × H (feet or cm) |
| Material | Text | Yes | ACP / Flex / Vinyl / Acrylic / LED / Painted |
| Installed Date | Date | Yes | When installed |
| Condition | Badge | Yes | Good (green) / Fair (amber) / Poor (orange) / Damaged (red) |
| Brand Compliant | Badge | Yes | ✅ Yes / ❌ No (current logo, colours, fonts?) |
| Last Inspection | Date | Yes | When was condition last verified |
| Municipal Permit | Badge | Yes | Valid / Expired / Not Required / Pending |
| Actions | Buttons | No | [View] [Update] [Archive] |

**Default sort:** Brand Compliant ASC (non-compliant first)
**Pagination:** Server-side · 25/page

### 5.3 Tab 2: Hoardings & Outdoor

**Filter bar:** Branch / Area (dropdown) · Vendor (dropdown) · Status (Active / Expired / Scheduled) · Size · Renewal within 30/60/90 days

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Photo | Thumbnail (60×60 px) | No | Hoarding photo |
| Location | Text | Yes | Road/junction name + city |
| Branch (Nearest) | Text | Yes | Which branch this hoarding serves |
| Size | Text | Yes | e.g., "20×10 ft", "30×15 ft" |
| Type | Badge | Yes | Hoarding / Bus Shelter / Unipole / Gantry / Wall Wrap |
| Vendor / Agency | Text | Yes | Hoarding rental agency name |
| Monthly Rent | ₹ Amount | Yes | Rental cost per month |
| Start Date | Date | Yes | Rental start |
| End Date | Date | Yes | Rental end / renewal date |
| Days to Renewal | Integer | Yes | Red ≤ 7, Amber 8–30, Green > 30, Grey = expired |
| Creative | Thumbnail | No | Current artwork displayed on hoarding |
| Status | Badge | Yes | Active (green) / Expiring (amber) / Expired (red) / Scheduled (blue) |
| Municipal Permit | Badge | Yes | Valid / Expired / Applied / Not Required |
| Actions | Buttons | No | [View] [Renew] [Replace Creative] [End] |

**Default sort:** Days to Renewal ASC (soonest renewal first)
**Pagination:** Server-side · 25/page

### 5.4 Tab 3: Flex & Temporary

**Filter bar:** Branch · Event/Campaign · Status (Active / Removed / Scheduled) · Type

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Photo | Thumbnail (60×60) | No | Banner photo |
| Branch | Text | Yes | Branch name |
| Type | Badge | Yes | Flex Banner / Standee / Auto-Rickshaw / Pamphlet Box / Event Backdrop |
| Location | Text | Yes | Where installed/placed |
| Campaign | Text | Yes | Linked admission campaign |
| Install Date | Date | Yes | When put up |
| Remove By Date | Date | Yes | Planned removal date |
| Size | Text | Yes | Dimensions |
| Cost | ₹ Amount | Yes | Printing + installation cost |
| Status | Badge | Yes | Active / Scheduled / Removed |
| Actions | Buttons | No | [View] [Mark Removed] [Archive] |

**Default sort:** Install Date DESC
**Pagination:** Server-side · 25/page

### 5.5 Hoarding Renewal Calendar

Mini calendar view (monthly) showing all hoarding renewal dates. Each date cell shows count of renewals due. Click on a date opens the list of hoardings due that day.

- Red dates: renewals due (not yet actioned)
- Green dates: renewed
- Grey dates: no renewals

---

## 6. Drawers & Modals

### 6.1 Modal: `add-signage` (560px)
- **Title:** "Add Permanent Signage"
- **Fields:**
  - Branch (dropdown, required)
  - Signage type (dropdown, required): Gate Board / Building Facade / Classroom Nameplate / Direction Sign / Bus Side Panel / Bus Rear Panel / Auto Panel / Other
  - Location description (text, required — e.g., "Main gate — left pillar")
  - Dimensions — Width (number + unit dropdown: feet/cm) × Height
  - Material (dropdown): ACP / Flex / Vinyl / Acrylic / LED Backlit / Painted Wall / Glow Sign
  - Installed date (date picker)
  - Cost (₹, optional)
  - Vendor name (text, optional)
  - Municipal permit number (text, optional)
  - Municipal permit expiry (date, optional)
  - Photo upload (up to 3 photos, max 10 MB each)
  - Condition (dropdown): Good / Fair / Poor / Damaged
  - Brand compliant (toggle): Yes / No
  - Non-compliance notes (textarea, if No)
- **Buttons:** Cancel · Save
- **Access:** Role 131 (G2) or G4+

### 6.2 Modal: `add-hoarding` (560px)
- **Title:** "Add Hoarding / Outdoor Installation"
- **Fields:**
  - Location / Address (text, required)
  - City / Area (text, required)
  - Nearest branch (dropdown, required)
  - GPS coordinates (lat/long, optional — for map view)
  - Size (dropdown): 10×10 ft / 20×10 ft / 20×20 ft / 30×15 ft / 40×20 ft / Custom
  - Type (dropdown): Hoarding / Bus Shelter / Unipole / Gantry / Wall Wrap / Pole Kiosk
  - Vendor / Agency (dropdown — from vendor master, or add new)
  - Monthly rent (₹, required)
  - Deposit amount (₹, optional)
  - Rental start date (date, required)
  - Rental end date (date, required)
  - Auto-renewal (toggle + renewal period dropdown: Monthly / Quarterly / Half-yearly / Yearly)
  - Creative artwork (file upload — current design displayed on hoarding)
  - Municipal permit number (text, optional)
  - Municipal permit expiry (date, optional)
  - Photo of installed hoarding (upload, up to 3)
  - Notes (textarea)
- **Buttons:** Cancel · Save
- **Access:** Role 131 (G2) or G4+

### 6.3 Drawer: `signage-detail` (640px, right-slide)
- **Tabs:** Details · Photos · History · Compliance
- **Details tab:** All fields from add modal, read-only (editable for G2+)
- **Photos tab:** Photo gallery with upload date, condition at time of photo. Upload new photo button.
- **History tab:** Audit log — condition changes, photo updates, compliance status changes
- **Compliance tab:** Brand compliance checklist:
  - Logo correct version? ✅/❌
  - Colours match palette? ✅/❌
  - Font correct? ✅/❌
  - Branch name spelled correctly? ✅/❌
  - Contact number current? ✅/❌
  - Municipal permit valid? ✅/❌
  - Overall: Compliant / Non-Compliant
- **Footer:** [Edit] [Update Condition] [Upload Photo] [Archive]

### 6.4 Drawer: `hoarding-detail` (640px, right-slide)
- **Tabs:** Details · Photos · Rental History · Creative History
- **Details tab:** Full hoarding details, rental terms, vendor info
- **Photos tab:** Installation photos, condition photos with dates
- **Rental History tab:** All rental periods — start, end, amount paid, vendor, renewal notes
- **Creative History tab:** All artwork versions displayed on this hoarding over time, with date ranges
- **Footer:** [Edit] [Renew Rental] [Change Creative] [End Rental] [Archive]

### 6.5 Modal: `renew-hoarding` (480px)
- **Title:** "Renew Hoarding Rental"
- **Pre-filled:** Current vendor, location, current rent
- **Fields:**
  - New rental period: Start date → End date
  - New monthly rent (₹, pre-filled with current, editable)
  - Change creative? (toggle — if yes, upload new artwork)
  - Notes (textarea)
- **Buttons:** Cancel · Renew
- **Behaviour:** Creates new rental record; extends end date; toast confirmation

---

## 7. Charts

### 7.1 Hoarding Spend by Area (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Monthly Hoarding Rental by Area — Current Month" |
| Data | SUM(monthly_rent) grouped by city/area |
| X-axis | ₹ Amount |
| Y-axis | City / Area name |
| Colour | `#3B82F6` (blue) |
| Tooltip | "[Area]: ₹[X]/month across [N] hoardings" |
| API | `GET /api/v1/group/{id}/marketing/signage/analytics/spend-by-area/` |

### 7.2 Signage Condition Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Signage Condition — All Branches" |
| Data | COUNT per condition: Good / Fair / Poor / Damaged |
| Colour | Green / Amber / Orange / Red |
| Tooltip | "[Condition]: [N] items ([X]%)" |
| API | `GET /api/v1/group/{id}/marketing/signage/analytics/condition-distribution/` |

### 7.3 Brand Compliance by Branch (Stacked Bar)

| Property | Value |
|---|---|
| Chart type | Stacked horizontal bar (Chart.js 4.x) |
| Title | "Brand Compliance by Branch" |
| Data | Per branch: count compliant (green) vs non-compliant (red) |
| X-axis | Count |
| Y-axis | Branch name |
| Colour | Green (compliant) / Red (non-compliant) |
| Tooltip | "[Branch]: [N] compliant, [M] non-compliant ([X]%)" |
| API | `GET /api/v1/group/{id}/marketing/signage/analytics/compliance-by-branch/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Signage added | "Signage '[Type]' added for [Branch]" | Success | 3s |
| Hoarding added | "Hoarding at [Location] added — rental ₹[X]/month" | Success | 3s |
| Hoarding renewed | "Hoarding at [Location] renewed until [Date]" | Success | 4s |
| Hoarding ended | "Hoarding rental at [Location] ended" | Info | 3s |
| Condition updated | "Signage condition updated to [Condition]" | Success | 2s |
| Photo uploaded | "Photo added to [Signage/Hoarding]" | Success | 2s |
| Rental expiring soon | "Hoarding at [Location] expires in [N] days — renew or end" | Warning | 6s |
| Municipal permit expiring | "Municipal permit for [Location] expires in [N] days" | Warning | 6s |
| Archive confirmed | "Signage item archived" | Info | 2s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No signage records | 🪧 | "No Signage Tracked" | "Add your first signage installation to start tracking brand presence." | Add Signage |
| No hoardings | 📋 | "No Hoardings Added" | "Track outdoor hoardings to manage rentals and renewals." | Add Hoarding |
| No flex/temporary items | 🎪 | "No Temporary Signage" | "Flex banners and event signage will appear here during campaigns." | — |
| No renewals due | ✅ | "No Renewals Due" | "All hoarding rentals are current. Next renewal check in [N] days." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + tab bar placeholder + table skeleton (8 rows) |
| Tab switch | Table skeleton replacing content area |
| Signage detail drawer | Right-slide skeleton with photo gallery placeholder + 4 tabs |
| Photo upload | Progress bar inside modal/drawer |
| Chart load | Grey canvas placeholder |
| Calendar load | 7×5 grey cell grid placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/signage/` | G1+ | List all signage (filterable by type) |
| GET | `/api/v1/group/{id}/marketing/signage/{item_id}/` | G1+ | Single signage detail |
| POST | `/api/v1/group/{id}/marketing/signage/` | G2+ | Add signage/hoarding |
| PUT | `/api/v1/group/{id}/marketing/signage/{item_id}/` | G2+ | Update signage record |
| DELETE | `/api/v1/group/{id}/marketing/signage/{item_id}/` | G4+ | Archive signage |
| POST | `/api/v1/group/{id}/marketing/signage/{item_id}/photos/` | G2+ | Upload photo |
| PATCH | `/api/v1/group/{id}/marketing/signage/{item_id}/condition/` | G2+ | Update condition |
| POST | `/api/v1/group/{id}/marketing/hoardings/{item_id}/renew/` | G2+ | Renew hoarding rental |
| PATCH | `/api/v1/group/{id}/marketing/hoardings/{item_id}/end/` | G2+ | End hoarding rental |
| GET | `/api/v1/group/{id}/marketing/signage/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/signage/renewals-calendar/` | G1+ | Calendar data |
| GET | `/api/v1/group/{id}/marketing/signage/analytics/spend-by-area/` | G1+ | Spend analytics |
| GET | `/api/v1/group/{id}/marketing/signage/analytics/condition-distribution/` | G1+ | Condition stats |
| GET | `/api/v1/group/{id}/marketing/signage/analytics/compliance-by-branch/` | G1+ | Compliance stats |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../signage/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab button click | `hx-get=".../signage/?type={permanent/hoarding/flex}"` | `#signage-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Filter dropdowns | `hx-get` with filter params | `#signage-table-body` | `innerHTML` | `hx-trigger="change"` |
| Detail drawer | Row click | `hx-get=".../signage/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Add signage | Form submit | `hx-post=".../signage/"` | `#add-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Renew hoarding | Renew form submit | `hx-post=".../hoardings/{id}/renew/"` | `#renew-result` | `innerHTML` | Toast + table refresh |
| Photo upload | Photo form | `hx-post=".../signage/{id}/photos/"` | `#photo-gallery` | `beforeend` | Appends new photo |
| Calendar load | Calendar tab | `hx-get=".../signage/renewals-calendar/"` | `#renewal-calendar` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#signage-table-body` | `innerHTML` | Table body only |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
