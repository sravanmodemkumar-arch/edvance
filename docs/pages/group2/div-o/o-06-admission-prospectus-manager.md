# O-06 — Admission Prospectus Manager

> **URL:** `/group/marketing/brand/prospectus/`
> **File:** `o-06-admission-prospectus-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Campaign Content Coordinator (Role 131, G2) — primary manager

---

## 1. Purpose

The Admission Prospectus Manager handles the creation, version control, distribution, and tracking of admission prospectuses (printed and digital) across all branches. The prospectus is the single most important marketing document for an Indian education institution — it is what a parent takes home after a walk-in, what is handed out at school fairs, and what is downloaded from the website. A typical large education group produces 10–30 prospectus variants each admission season: one per branch (with branch-specific details), one per stream (MPC, BiPC, MEC), separate ones for hostelers vs day scholars, and a group-level overview prospectus.

The challenges this page solves:

1. **Version chaos:** Branch-specific prospectuses need annual updates — fee structures change, new toppers replace last year's, affiliation numbers update, infrastructure photos change. Without version control, branches distribute outdated prospectuses with last year's fees and retired toppers.

2. **Print run management:** A group ordering 50,000 prospectuses across 30 branches needs to track: how many per branch, which printer/vendor, delivery date, cost per copy, and remaining stock. Running out mid-season means walk-in parents leave empty-handed.

3. **Digital distribution:** The digital prospectus (PDF) is shared via WhatsApp, linked on the website, and emailed to enquiries. The platform provides a single canonical URL per branch that always points to the latest version — no broken links, no stale PDFs floating in WhatsApp groups.

**Scale:** 5–50 branches · 10–30 prospectus variants · 20,000–2,00,000 printed copies per season · 5,000–50,000 digital downloads per season

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Campaign Content Coordinator | 131 | G2 | Full CRUD — create, edit, version, publish, track | Primary manager |
| Group Admissions Campaign Manager | 119 | G3 | Read + Approve final version | Approves before print/publish |
| Group Topper Relations Manager | 120 | G3 | Read + Suggest topper content | Provides topper data for prospectus |
| Branch Principal | — | G3 | Read (own branch) + Request print run | Requests additional copies |
| Branch Admin | — | G2 | Read + Download (own branch digital) | Downloads PDF for sharing |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Upload/edit: role 131 or G4+. Branch users filtered to own branch.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Brand & Content  ›  Admission Prospectus Manager
```

### 3.2 Page Header
```
Admission Prospectus Manager                   [Create Prospectus]  [Print Order]  [Export Report]
Content Coordinator — Meena Raghavan
Sunrise Education Group · Season 2026-27 · 24 variants · 1,45,000 printed · 18,400 digital downloads
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Variants | Integer | COUNT(prospectus) WHERE season = current AND status = 'published' | Static blue | `#kpi-variants` |
| 2 | Branches Covered | N / Total | COUNT DISTINCT branches with published prospectus / total branches | Green = 100%, Amber < 100% | `#kpi-branches-covered` |
| 3 | Total Printed | Integer | SUM(print_copies_ordered) this season | Static blue | `#kpi-printed` |
| 4 | Remaining Stock | Integer | SUM(print_copies_ordered − print_copies_distributed) | Red if any branch at 0, Amber < 20% remaining, Green ≥ 20% | `#kpi-stock` |
| 5 | Digital Downloads | Integer | COUNT(digital_downloads) this season | Static green | `#kpi-downloads` |
| 6 | Pending Approval | Integer | COUNT(prospectus) WHERE status = 'pending_approval' | Red > 5, Amber 1–5, Green = 0 | `#kpi-pending` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/prospectus/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Prospectus Variants Grid

Card-based grid (3 columns). Each card represents one prospectus variant.

**Card Layout:**

```
┌────────────────────────────────┐
│  ┌──────────────────────────┐  │
│  │                          │  │
│  │   [Cover Page Preview]   │  │
│  │      (200×280 px)        │  │
│  │                          │  │
│  └──────────────────────────┘  │
│                                │
│  📖 Kukatpally Branch — MPC    │
│  Season: 2026-27 · v2.1       │
│  Pages: 24 · Language: EN+TE  │
│                                │
│  Print: 8,000 ordered          │
│  Stock: 2,140 remaining        │
│  Digital: 1,240 downloads      │
│                                │
│  Status: ✅ Published          │
│  [Preview] [Download] [Edit]   │
└────────────────────────────────┘
```

**Fields per card:**
- Cover page thumbnail (auto-generated from uploaded PDF)
- Prospectus title: Branch name + Stream/Type
- Season, version, page count, language(s)
- Print: copies ordered, stock remaining (progress bar)
- Digital: download count
- Status: Draft / Pending Approval / Published / Archived
- Actions: [Preview] [Download PDF] [Edit] (per role)

**Filters:** Branch · Stream (MPC/BiPC/MEC/CEC/General) · Type (Day Scholar/Hosteler/Group Overview) · Status · Language
**Sort:** Branch name A-Z / Newest / Most Downloads
**Pagination:** Infinite scroll · 12 cards per load

### 5.2 Print Run Tracker

Table tracking physical printing orders and stock levels.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | Branch name |
| Variant | Text | Yes | Prospectus type |
| Version | Text | Yes | Current version |
| Printer/Vendor | Text | Yes | Printing vendor name |
| Copies Ordered | Integer | Yes | Total print run |
| Cost/Copy | ₹ Amount | Yes | Per-unit printing cost |
| Total Cost | ₹ Amount | Yes | Copies × cost |
| Order Date | Date | Yes | When ordered |
| Delivery Date | Date | Yes | Expected/actual delivery |
| Delivered | Integer | Yes | Copies received |
| Distributed | Integer | Yes | Copies given to walk-ins/events |
| Remaining | Integer | Yes | Stock on hand; red if < 100 |
| Reorder Needed | Badge | Yes | ✅ Yes (stock < threshold) / ❌ No |
| Actions | Buttons | No | [Update Stock] [Reorder] [View] |

**Default sort:** Remaining ASC (lowest stock first)
**Pagination:** Server-side · 25/page

### 5.3 Digital Download Analytics

Table showing digital prospectus download stats per variant.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Variant | Text | Yes | Prospectus title |
| Branch | Text | Yes | Branch |
| Public URL | Copy button | No | Shareable URL (canonical — always latest version) |
| Downloads (Total) | Integer | Yes | All-time downloads |
| Downloads (This Month) | Integer | Yes | Current month |
| QR Code | Thumbnail | No | QR code for printed materials (links to digital PDF) |
| Avg Time on Page | Duration | Yes | Average viewing duration (if embedded viewer used) |
| Source Breakdown | Mini badges | No | Web: X / WhatsApp: Y / Email: Z |

### 5.4 Prospectus Content Checklist

Standard content sections that every prospectus must include. Used during creation and review.

| Section | Required | Notes |
|---|---|---|
| Cover Page | ✅ | Group logo, branch name, tagline, academic year, stream |
| Chairman's Message | ✅ | Standard message from Group Chairman |
| About the Group | ✅ | History, vision, mission, number of branches |
| About the Branch | ✅ | Branch-specific: location, infrastructure, campus photos |
| Academic Programmes | ✅ | Streams offered, subjects, board affiliation |
| Faculty Highlights | ✅ | Key teachers, qualifications, experience |
| Topper Gallery | ✅ | Board/JEE/NEET toppers with photos, ranks, marks |
| Infrastructure | ✅ | Labs, library, sports, smart classrooms — with photos |
| Hostel (if applicable) | Conditional | Hostel facilities, rooms, mess, security |
| Transport | Optional | Bus routes, fleet photos |
| Fee Structure | ✅ | Current year fees — tuition, hostel, transport, extras |
| Scholarship Information | ✅ | Scholarship types, eligibility, application process |
| Admission Process | ✅ | Steps, documents required, dates, contact |
| Contact & Location | ✅ | Address, phone, email, map, QR code for website |
| Testimonials | Optional | Parent/student quotes |
| Back Cover | ✅ | Group logo, tagline, all branch addresses |

---

## 6. Drawers & Modals

### 6.1 Modal: `create-prospectus` (640px)
- **Title:** "Create New Prospectus"
- **Fields:**
  - Title (text, required — e.g., "Kukatpally Branch — MPC Prospectus 2026-27")
  - Branch (dropdown, required — or "Group Overview" for group-level)
  - Stream (multi-select): MPC / BiPC / MEC / CEC / HEC / Foundation / General
  - Type (dropdown): Day Scholar / Hosteler / Combined / Group Overview
  - Language (multi-select, required): English / Telugu / Hindi / Tamil / Bilingual
  - Season (dropdown, auto-selected to current)
  - Page count (integer, optional — for planning)
  - Upload PDF (file, optional — can be added later)
  - Content checklist review (toggle — mark which sections are included)
  - Notes (textarea)
- **Buttons:** Cancel · Save as Draft · Submit for Approval
- **Access:** Role 131 or G4+

### 6.2 Modal: `print-order` (560px)
- **Title:** "Place Print Order"
- **Fields:**
  - Prospectus variant (dropdown — from published list)
  - Printer/Vendor (dropdown from vendor master + add new)
  - Copies to order (integer, required)
  - Cost per copy (₹, required)
  - Expected delivery date (date)
  - Paper quality (dropdown): 130 GSM Art Paper / 170 GSM Art Paper / 200 GSM Matt / Custom
  - Binding type (dropdown): Saddle Stitch / Perfect Bind / Spiral
  - Delivery address (dropdown — branch address, auto-filled)
  - Notes (textarea)
- **Buttons:** Cancel · Place Order
- **Access:** Role 131 or G4+

### 6.3 Drawer: `prospectus-detail` (720px, right-slide)
- **Tabs:** Preview · Details · Versions · Print History · Downloads · Distribution
- **Preview tab:** Embedded PDF viewer (page-by-page navigation)
- **Details tab:** All metadata, content checklist status, creation date, approval status
- **Versions tab:** Version history — date, uploader, changes, download per version
- **Print History tab:** All print orders for this variant — vendor, quantity, cost, delivery status
- **Downloads tab:** Digital download log — date, source (web/WhatsApp/email), location (if available)
- **Distribution tab:** Physical copies — distributed to events, walk-ins, remaining stock chart
- **Footer:** [Download PDF] [Upload New Version] [Place Print Order] [Generate QR] [Archive]

### 6.4 Modal: `update-stock` (480px)
- **Title:** "Update Stock — [Branch] [Variant]"
- **Fields:**
  - Copies distributed since last update (integer)
  - Distribution purpose (dropdown): Walk-in Parents / School Fair / Open Day / Mailed / Other
  - New stock count (auto-calculated: previous remaining − distributed)
  - Notes (textarea)
- **Buttons:** Cancel · Update
- **Access:** Role 131, Branch Admin, or G4+

### 6.5 Modal: `generate-qr` (400px)
- **Title:** "Generate QR Code"
- **Preview:** QR code image linking to digital prospectus URL
- **Options:**
  - Include branch logo in QR centre (toggle)
  - QR size: 2cm / 3cm / 5cm / 10cm
  - Format: PNG / SVG
  - Tracking UTM parameter (auto-added for source tracking)
- **Buttons:** Cancel · Download QR
- **Note:** QR code always points to the canonical URL — if the prospectus is updated, the QR still works

---

## 7. Charts

### 7.1 Print vs Digital Distribution (Stacked Bar)

| Property | Value |
|---|---|
| Chart type | Stacked bar (Chart.js 4.x) |
| Title | "Prospectus Distribution — Print vs Digital by Branch" |
| Data | Per branch: print copies distributed (bar 1) + digital downloads (bar 2) |
| X-axis | Branch name |
| Y-axis | Count |
| Colour | Print: `#3B82F6` blue; Digital: `#10B981` green |
| Tooltip | "[Branch]: [N] printed, [M] digital — total reach: [N+M]" |
| API | `GET /api/v1/group/{id}/marketing/prospectus/analytics/distribution/` |

### 7.2 Stock Levels by Branch (Bar Chart)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Remaining Prospectus Stock by Branch" |
| Data | Remaining copies per branch |
| Colour | Green > 500, Amber 100–500, Red < 100 (per bar) |
| API | `GET /api/v1/group/{id}/marketing/prospectus/analytics/stock-levels/` |

### 7.3 Digital Downloads Trend (Line)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Digital Prospectus Downloads — Last 6 Months" |
| Data | Monthly download count |
| Colour | `#10B981` green |
| API | `GET /api/v1/group/{id}/marketing/prospectus/analytics/download-trend/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Prospectus created | "Prospectus '[Title]' created — status: Draft" | Success | 3s |
| Submitted for approval | "Prospectus '[Title]' submitted for approval" | Info | 3s |
| Approved | "Prospectus '[Title]' approved and published" | Success | 4s |
| New version uploaded | "Version [X] uploaded for '[Title]' — previous version archived" | Success | 4s |
| Print order placed | "Print order: [N] copies of '[Title]' — delivery by [Date]" | Success | 4s |
| Stock updated | "Stock updated: [Branch] now has [N] copies remaining" | Success | 3s |
| Stock low alert | "Low stock: [Branch] has only [N] copies remaining — reorder recommended" | Warning | 6s |
| QR generated | "QR code generated. Click to download." | Success | 4s |
| Download started | "Downloading '[Title]' (v[X])…" | Info | 2s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No prospectuses created | 📖 | "No Prospectuses Yet" | "Create your first admission prospectus for the current season." | Create Prospectus |
| No print orders | 🖨️ | "No Print Orders" | "Place a print order once a prospectus is approved." | — |
| No digital downloads | 📥 | "No Downloads Yet" | "Digital downloads will appear once the prospectus is published and shared." | — |
| Branch has no prospectus | 🏫 | "No Prospectus for This Branch" | "A prospectus has not yet been created for your branch. Contact Group HQ." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + 6 card-shaped grid placeholders |
| Prospectus grid scroll | 3 new card shimmer blocks appended |
| Print tracker table | 8-row table skeleton |
| Prospectus detail drawer | 720px skeleton: large PDF placeholder + 6 tabs |
| PDF viewer load | Grey rectangle with "Loading prospectus…" + page count |
| QR generation | Spinner: "Generating QR code…" |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/prospectus/` | G1+ | List all prospectus variants |
| GET | `/api/v1/group/{id}/marketing/prospectus/{pros_id}/` | G1+ | Single prospectus detail |
| POST | `/api/v1/group/{id}/marketing/prospectus/` | G2+ | Create new prospectus |
| PUT | `/api/v1/group/{id}/marketing/prospectus/{pros_id}/` | G2+ | Update metadata |
| PATCH | `/api/v1/group/{id}/marketing/prospectus/{pros_id}/status/` | G3+ | Approve/reject/archive |
| POST | `/api/v1/group/{id}/marketing/prospectus/{pros_id}/versions/` | G2+ | Upload new version |
| GET | `/api/v1/group/{id}/marketing/prospectus/{pros_id}/versions/` | G1+ | Version history |
| GET | `/api/v1/group/{id}/marketing/prospectus/{pros_id}/download/` | G2+ | Download PDF |
| POST | `/api/v1/group/{id}/marketing/prospectus/{pros_id}/print-orders/` | G2+ | Place print order |
| GET | `/api/v1/group/{id}/marketing/prospectus/{pros_id}/print-orders/` | G1+ | Print order history |
| PATCH | `/api/v1/group/{id}/marketing/prospectus/{pros_id}/stock/` | G2+ | Update stock level |
| POST | `/api/v1/group/{id}/marketing/prospectus/{pros_id}/qr/` | G2+ | Generate QR code |
| GET | `/api/v1/group/{id}/marketing/prospectus/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/prospectus/analytics/distribution/` | G1+ | Distribution chart data |
| GET | `/api/v1/group/{id}/marketing/prospectus/analytics/stock-levels/` | G1+ | Stock chart data |
| GET | `/api/v1/group/{id}/marketing/prospectus/analytics/download-trend/` | G1+ | Download trend data |

### Public Endpoint (No Auth — for parent/student download)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/prospectus/{group_slug}/{branch_slug}/` | Public canonical URL — always returns latest published PDF |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../prospectus/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Grid load | `<div id="prospectus-grid">` | `hx-get=".../prospectus/"` | `#prospectus-grid` | `innerHTML` | `hx-trigger="load"` |
| Filter apply | Filter dropdowns | `hx-get` with filter params | `#prospectus-grid` | `innerHTML` | `hx-trigger="change"` |
| Infinite scroll | Sentinel | `hx-get=".../prospectus/?page={n+1}"` | `#prospectus-grid` | `beforeend` | `hx-trigger="revealed"` |
| Detail drawer | Card click | `hx-get=".../prospectus/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create form | Form submit | `hx-post=".../prospectus/"` | `#create-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Print order | Order form submit | `hx-post=".../prospectus/{id}/print-orders/"` | `#order-result` | `innerHTML` | Toast + table refresh |
| Stock update | Update form | `hx-patch=".../prospectus/{id}/stock/"` | `#stock-cell-{id}` | `innerHTML` | Inline update |
| QR generate | Generate button | `hx-post=".../prospectus/{id}/qr/"` | `#qr-modal-content` | `innerHTML` | Shows QR in modal |
| Version upload | Upload form | `hx-post=".../prospectus/{id}/versions/"` | `#version-list` | `afterbegin` | `hx-encoding="multipart/form-data"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
