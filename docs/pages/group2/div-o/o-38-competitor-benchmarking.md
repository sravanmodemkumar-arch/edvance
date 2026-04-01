# O-38 — Competitor Benchmarking

> **URL:** `/group/marketing/analytics/competitor-benchmarking/`
> **File:** `o-38-competitor-benchmarking.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Admission Data Analyst (Role 132, G1) — primary analyst

---

## 1. Purpose

The Competitor Benchmarking page is the group's strategic intelligence system for tracking, comparing, and positioning against every competing school group, standalone school, and coaching institute in its operating cities. In the Indian education market, every city tier — from Hyderabad and Vijayawada to Karimnagar and Guntur — has 3–10 competing school groups fighting for the same parent wallets. Parents comparison-shop aggressively: they visit 3–5 schools, compare fee structures (often published on websites or shared via WhatsApp), count toppers in newspaper ads, assess infrastructure during open days, and ask neighbourhood aunties which school "gives better results." A group that does not systematically track what competitors charge, claim, and build is flying blind in a market where a single competitor opening a new branch 2 km away can drain 200 admissions overnight.

The problems this page solves:

1. **Fee intelligence gap:** Competing groups publish fee structures on their websites, prospectuses, and parent WhatsApp groups. Fees change every year, often with hidden components (development fee, activity fee, transport fee, hostel charges). Without systematic tracking, the group cannot answer the CEO's basic question: "Are we the costliest school in Kukatpally, or the cheapest?" The system maintains a branch-by-branch fee comparison against each identified competitor with annual revision tracking.

2. **Topper claim warfare:** After every board/JEE/NEET result season, 3–5 groups in the same city claim "No. 1 results." Narayana says "4,200 students above 90%," Sri Chaitanya says "4,500 students above 90%," and a local group says "100% pass rate." Without tracking competitor claims (collected from newspaper ads, flex banners, press releases, and social media), the group cannot craft counter-messaging or verify its own positioning. The intelligence log captures every competitor move with evidence (photo/screenshot/URL).

3. **Branch expansion blind spots:** When a competitor opens a new branch in Manikonda or Kompally, it directly threatens the nearest existing branches. The system tracks competitor branch openings, closures, and relocations so the group can pre-emptively increase marketing spend in affected catchment areas (linking to O-27 Catchment Area Planner).

4. **SWOT documentation deficiency:** Most groups informally "know" their strengths and weaknesses versus competitors, but this knowledge lives in the heads of branch principals and marketing directors — not in a structured format the Board can act on. The page maintains a living SWOT analysis per competitor that feeds into O-39 (Admission Season Report) and annual strategy planning.

5. **Positioning drift:** Over 3–5 years, a group's market position shifts — from "affordable quality" to "premium" as fees rise, or from "topper factory" to "holistic education" as pedagogy evolves. Without a competitive positioning map, the CEO cannot see where the group sits relative to competitors on the two axes that matter most to Indian parents: fee affordability and academic results.

**Scale:** 10–50 competitors tracked per group · 5–50 branches per competitor · 3–5 cities · 1–3 intelligence entries per competitor per month · annual fee revision cycle · quarterly SWOT review

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admission Data Analyst | 132 | G1 | Full CRUD — add competitors, log intelligence, build comparisons, update SWOT | Primary analyst and curator |
| Group Admissions Campaign Manager | 119 | G3 | Read + Contribute — view benchmarks, add intelligence entries from field reports | Feeds competitive insights from campaign execution |
| Group Topper Relations Manager | 120 | G3 | Read + Contribute — add topper claim intelligence entries | Tracks competitor topper claims post-results |
| Group Admission Telecaller Executive | 130 | G3 | Read (limited) — view fee comparison for counselling conversations | Uses during parent calls: "Our fee is X vs competitor Y" |
| Group Campaign Content Coordinator | 131 | G2 | Read — view positioning data for creative briefs | Reference for messaging strategy |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — view all benchmarks, approve positioning strategy, sign off SWOT | Strategic decision-maker; presents to Board |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Competitor creation/editing: role 132 or G3+. Intelligence entry: roles 119, 120, 132, or G3+. SWOT approval: G4/G5. Export: G1+ (all data analyst and above).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Analytics & Reports  >  Competitor Benchmarking
```

### 3.2 Page Header
```
Competitor Benchmarking                               [+ Add Competitor]  [Comparison Builder]  [Intelligence Log]  [Export]
Data Analyst — Priya Venkatesh
Sunrise Education Group · Season 2025-26 · 24 competitors tracked · 3 cities · 12 intelligence entries (30d)
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Competitors Tracked | Integer | COUNT(competitors) WHERE status = 'active' | Static blue | `#kpi-competitors` |
| 2 | Avg Fee Position | Percentile | Group's avg fee as percentile rank among all tracked competitors (50th = median) | Green ≤ 40th (affordable), Amber 40–70, Red > 70th (expensive) | `#kpi-fee-position` |
| 3 | Topper Advantage | +/- Integer | Group's topper count (≥90%) minus nearest competitor's topper count | Green > 0 (ahead), Red ≤ 0 (behind) | `#kpi-topper-advantage` |
| 4 | New Competitor Moves (30d) | Integer | COUNT(intelligence_entries) WHERE created_at > NOW() - 30d | Amber > 5, Red > 10 (high activity) | `#kpi-moves-30d` |
| 5 | Market Position Score | 1–10 | Composite score: weighted average of fee competitiveness (30%), topper results (40%), branch reach (20%), brand perception (10%) | Green ≥ 7, Amber 4–6, Red < 4 | `#kpi-position-score` |
| 6 | Fee Gap (%) | Percentage | (Group avg fee − Market avg fee) / Market avg fee × 100 | Green ≤ 5% above market, Amber 5–15%, Red > 15% above market | `#kpi-fee-gap` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Competitor Directory** — Master list of all tracked competitors
2. **Fee Comparison** — Side-by-side fee matrix across competitors and classes
3. **Positioning Map** — Visual positioning on fee vs results axes
4. **SWOT Tracker** — Per-competitor SWOT analysis
5. **Intelligence Log** — Chronological record of competitor moves and market signals

### 5.2 Tab 1: Competitor Directory

**Filter bar:** City · Type (School Group/Standalone School/Coaching Institute/College Group) · Board (CBSE/ICSE/State Board/IB) · Fee Range · Status (Active/Inactive/New Entrant)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Competitor Name | Text (link) | Yes | Click → competitor detail drawer |
| Type | Badge | Yes | School Group / Standalone School / Coaching Institute / College Group |
| City | Text | Yes | Primary operating city |
| Branches | Integer | Yes | Number of known branches |
| Boards | Badge set | No | CBSE · ICSE · State · IB — which boards they offer |
| Fee Range (Annual) | Text | Yes | "₹45,000 – ₹1,20,000" — lowest to highest class |
| Claimed Students | Text | Yes | Approximate student count from their marketing claims |
| Toppers Claimed | Integer | Yes | Number of toppers claimed in latest results (from newspaper ads) |
| Last Updated | Date | Yes | When competitor record was last refreshed |
| SWOT Status | Badge | Yes | Current / Outdated (> 6 months) / Not Done |
| Threat Level | Badge | Yes | High (red) / Medium (amber) / Low (green) — analyst assessment |
| Actions | Buttons | No | [View] [Edit] [Add Intel] [Compare] |

**Default sort:** Threat Level DESC (High first), then Branches DESC
**Pagination:** Server-side · 25/page

### 5.3 Tab 2: Fee Comparison

**Matrix view** — rows = classes/grades, columns = competitors (including own group as highlighted column):

**Filter bar:** City · Class range (Nursery–12 / Jr Inter–Sr Inter) · Fee component (Tuition Only / All-inclusive / Hostel) · Academic year

| Row | Own Group | Competitor A | Competitor B | Competitor C | ... |
|---|---|---|---|---|---|
| Nursery–UKG | ₹55,000 | ₹48,000 | ₹62,000 | ₹45,000 | ... |
| Class 1–5 | ₹65,000 | ₹58,000 | ₹72,000 | ₹52,000 | ... |
| Class 6–8 | ₹78,000 | ₹68,000 | ₹85,000 | ₹62,000 | ... |
| Class 9–10 | ₹92,000 | ₹82,000 | ₹1,05,000 | ₹75,000 | ... |
| Jr Inter (MPC) | ₹1,10,000 | ₹95,000 | ₹1,25,000 | ₹88,000 | ... |
| Jr Inter (BiPC) | ₹1,15,000 | ₹1,00,000 | ₹1,30,000 | ₹92,000 | ... |

**Cell colouring:** Green = own group is cheaper · Red = own group is more expensive · Grey = no data
**Row summary:** Min / Max / Median across competitors for each class
**Column summary:** Overall positioning badge per competitor: "Budget" / "Mid-range" / "Premium"

**Data source:** Manual entry from competitor prospectuses, websites, and field intelligence. Updated during Sep–Nov (fee revision season) and Jan–Feb (admission rush).

### 5.4 Tab 3: Positioning Map

Interactive bubble chart (rendered via Chart.js 4.x, detailed in Section 7.2) displayed inline as a full-width panel.

- **X-axis:** Average annual fee (₹)
- **Y-axis:** Topper count (≥90% or JEE/NEET qualified)
- **Bubble size:** Estimated student strength
- **Own group:** Highlighted in accent colour (`#6366F1`) with label
- **Competitors:** Grey/blue bubbles with hover labels
- **Quadrant labels:** Top-left = "Value Leaders" · Top-right = "Premium Performers" · Bottom-left = "Budget Players" · Bottom-right = "Overpriced"

Below the chart: Positioning summary card — "Sunrise Education Group is in the [quadrant] quadrant — [X]th percentile on fee, [Y]th percentile on results."

### 5.5 Tab 4: SWOT Tracker

**Filter bar:** Competitor · Last updated · Status (Current/Outdated/Not Done)

One card per competitor SWOT:

```
┌─────────────────────────────────────────────────────────────────┐
│  Narayana Educational Institutions          Last updated: 15 Jan 2026
│  Threat Level: HIGH                         Updated by: Priya Venkatesh
│                                                                 │
│  ┌─ Strengths ──────────┐  ┌─ Weaknesses ──────────┐          │
│  │ • 300+ branches       │  │ • High fee complaints  │          │
│  │ • JEE/NEET top ranks  │  │ • Teacher attrition    │          │
│  │ • Aggressive PR       │  │ • Student stress cases  │          │
│  │ • Strong hostel infra │  │ • Rigid curriculum      │          │
│  └──────────────────────┘  └───────────────────────┘          │
│  ┌─ Opportunities ──────┐  ┌─ Threats ──────────────┐          │
│  │ • New NEP curriculum  │  │ • Opening 5 new branches│          │
│  │ • Parent backlash     │  │ • ₹50Cr ad spend       │          │
│  │   on competitor fees  │  │ • Poaching our teachers │          │
│  └──────────────────────┘  └───────────────────────┘          │
│                                                                 │
│  [Edit SWOT]  [View Full History]  [Export]                    │
└─────────────────────────────────────────────────────────────────┘
```

**Also available as table view:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Competitor | Text (link) | Yes | Click → SWOT edit modal |
| Threat Level | Badge | Yes | High / Medium / Low |
| Strengths | Integer | No | Count of bullet points |
| Weaknesses | Integer | No | Count of bullet points |
| Opportunities | Integer | No | Count of bullet points |
| Threats | Integer | No | Count of bullet points |
| Last Updated | Date | Yes | — |
| Updated By | Text | Yes | Analyst name |
| Status | Badge | Yes | Current (green) / Outdated (amber) / Not Done (grey) |
| Actions | Buttons | No | [Edit] [History] [Export] |

### 5.6 Tab 5: Intelligence Log

Chronological feed of competitor activities — branch openings, fee changes, topper claims, ad campaigns, facility additions, key hires, policy changes.

**Filter bar:** Competitor · Category (Fee Change / New Branch / Topper Claim / Ad Campaign / New Facility / Key Hire / Policy Change / Closure / Other) · City · Date range · Source

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Date | Date | Yes | When the intelligence was observed |
| Competitor | Text | Yes | — |
| Category | Badge | Yes | Fee Change / New Branch / Topper Claim / Ad Campaign / New Facility / Key Hire / Policy Change / Closure / Other |
| Summary | Text | No | One-line summary: "Narayana announced Jr Inter fee increase to ₹1,25,000 from ₹1,10,000" |
| City | Text | Yes | Where the activity was observed |
| Impact | Badge | Yes | High (red) / Medium (amber) / Low (green) |
| Source | Badge | Yes | Newspaper Ad / Website / WhatsApp Forward / Field Visit / Parent Feedback / Social Media / Press Release / Prospectus |
| Evidence | Link/Thumbnail | No | Uploaded screenshot, photo, or URL |
| Logged By | Text | Yes | Who added this entry |
| Actions | Buttons | No | [View] [Edit] [Link to Competitor] |

**Default sort:** Date DESC (most recent first)
**Pagination:** Server-side · 25/page

---

## 6. Drawers & Modals

### 6.1 Modal: `add-competitor` (640px)

- **Title:** "Add Competitor"
- **Fields:**
  - **Basic details:**
    - Competitor name (text, required — e.g., "Narayana Educational Institutions")
    - Type (dropdown, required): School Group / Standalone School / Coaching Institute / College Group
    - City (text, required — primary operating city)
    - State (dropdown, required)
    - Website URL (URL, optional)
    - Founded year (integer, optional)
    - Ownership type (dropdown): Trust / Society / Private Ltd / LLP / Individual
  - **Branch details:**
    - Number of branches (integer, required)
    - Branch cities (multi-text — list cities: "Hyderabad, Vijayawada, Guntur, Nellore")
    - Nearest branch to our branches (dropdown from own branch list — for proximity analysis)
    - Distance from nearest branch (km, auto-calculated if geocoded, else manual)
  - **Academic profile:**
    - Boards offered (multi-select): CBSE / ICSE / State Board (specify) / IB / IGCSE / Cambridge
    - Streams offered (multi-select): MPC / BiPC / MEC / CEC / HEC / Arts / Commerce / General
    - Classes offered (multi-select): Pre-Primary / Primary / Middle / Secondary / Senior Secondary / Jr Inter / Sr Inter
    - Coaching integration (toggle): Offers JEE/NEET coaching in-house?
    - Hostel available (toggle)
  - **Market estimates:**
    - Claimed student count (integer — from their marketing materials)
    - Estimated actual student count (integer — analyst's assessment)
    - Estimated annual revenue (₹, optional — back-calculated from students × avg fee)
    - Market share estimate (%, optional — in primary operating city)
  - **Fee data:**
    - Fee entry rows (repeating — one row per class/grade):
      - Class/Grade (dropdown)
      - Annual fee (₹)
      - Fee components included (multi-select): Tuition / Development / Activity / Lab / Transport / Hostel
      - Source (dropdown): Website / Prospectus / Parent Feedback / Field Visit
      - Academic year (dropdown)
  - **Topper data:**
    - Latest results season toppers (integer — count of ≥90% claimed)
    - Best JEE rank claimed (integer, optional)
    - Best NEET rank claimed (integer, optional)
    - State board toppers claimed (integer, optional)
    - Source of claims (text — "Full-page ad in Eenadu, 15 May 2026")
  - **Differentiators** (textarea — what they emphasise: "AI-based learning," "100% hostel campus," "Foreign university tie-ups")
  - **Threat level** (dropdown): High / Medium / Low
  - **Notes** (textarea)
- **Buttons:** Cancel · Save
- **Access:** Role 132, 119, or G4+

### 6.2 Drawer: `competitor-detail` (720px, right-slide)

- **Tabs:** Profile · Fees · Results · Intelligence · SWOT · History
- **Profile tab:** All basic details, branch count, boards, streams, differentiators, threat level badge, website link, market estimates
- **Fees tab:** Fee comparison table — own group vs this competitor across all classes; YoY fee changes; fee positioning (cheaper/pricier by how much)
- **Results tab:** Topper claims over past 3 seasons; JEE/NEET performance claims; comparison with own group's verified results
- **Intelligence tab:** All intelligence log entries for this competitor, most recent first; mini timeline view
- **SWOT tab:** Current SWOT analysis (editable); SWOT history (previous versions with dates)
- **History tab:** Audit trail — when competitor record was created, updated, by whom
- **Footer:** [Edit] [Add Intelligence] [Update SWOT] [Compare with Group] [Deactivate] [Delete]

### 6.3 Modal: `add-intelligence` (560px)

- **Title:** "Log Competitor Intelligence"
- **Fields:**
  - Competitor (dropdown from competitor list, required — pre-filled if opened from competitor detail)
  - Date observed (date, required — defaults to today)
  - Category (dropdown, required): Fee Change / New Branch Opening / Branch Closure / Topper Claim / Ad Campaign / New Facility / Key Hire / Policy Change / Scholarship Announcement / Event / Other
  - Summary (text, required — one-line description, max 200 chars)
  - Details (textarea — full description of the intelligence)
  - City (text, required)
  - Impact assessment (dropdown): High / Medium / Low
  - Source (dropdown, required): Newspaper Ad / Website / WhatsApp Forward / Field Visit / Parent Feedback / Social Media / Press Release / Prospectus / Employee Source / Other
  - Evidence upload (file — JPEG/PNG/PDF, max 10 MB — screenshot of ad, photo of hoarding, prospectus scan)
  - Evidence URL (URL, optional — link to social media post, website page, news article)
  - Affected branches (multi-select from own branch list — which of our branches are impacted)
  - Recommended action (textarea, optional — analyst's suggested response)
- **Buttons:** Cancel · Save
- **Access:** Role 132, 119, 120, or G3+

### 6.4 Modal: `comparison-builder` (720px)

- **Title:** "Comparison Builder"
- **Step 1 — Select competitors:**
  - Multi-select from competitor list (max 5 for readability)
  - Own group auto-included (highlighted)
- **Step 2 — Select dimensions:**
  - Checkboxes: Fee Range · Topper Count · Branch Count · Student Strength · JEE/NEET Performance · Hostel Availability · Board Options · Coaching Integration · Year Founded · Threat Level
- **Step 3 — Preview comparison matrix:**
  - Auto-generated side-by-side table with selected competitors × selected dimensions
  - Cell colouring: Green where own group is better, Red where competitor is better, Grey where equal or no data
  - "Best in class" badge per row (which entity leads that dimension)
- **Export options:** Download as PNG (for presentations) / PDF / Excel
- **Buttons:** Cancel · Back · Next · Export
- **Access:** Role 132 or G4+

### 6.5 Modal: `edit-swot` (640px)

- **Title:** "SWOT Analysis — [Competitor Name]"
- **Layout:** 2×2 grid
  - **Strengths** (textarea with bullet-point formatting — one per line)
  - **Weaknesses** (textarea with bullet-point formatting)
  - **Opportunities** (textarea — where can our group exploit their gaps)
  - **Threats** (textarea — how they threaten our admissions/revenue)
- **Threat level reassessment** (dropdown): High / Medium / Low
- **Review date** (date — when SWOT should be reviewed next; defaults to current + 6 months)
- **Buttons:** Cancel · Save SWOT
- **Access:** Role 132 or G4+
- **Note:** Each save creates a new SWOT version; previous versions retained for historical comparison

### 6.6 Modal: `fee-revision-entry` (480px)

- **Title:** "Update Competitor Fee — [Competitor Name]"
- **Fields:**
  - Academic year (dropdown, required)
  - Fee entries (repeating rows):
    - Class/Grade (dropdown)
    - Previous fee (₹, auto-populated from last entry)
    - New fee (₹, required)
    - Change (%, auto-calculated)
    - Source (dropdown): Website / Prospectus / Parent Feedback / Field Visit
  - Notes (textarea — e.g., "New development fee of ₹5,000 added separately")
- **Buttons:** Cancel · Save Revision
- **Access:** Role 132, 119, or G4+

---

## 7. Charts

### 7.1 Fee Comparison Grouped Bar

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Annual Fee Comparison by Class — Own Group vs Competitors" |
| Data | X-axis = class/grade; bars = one per entity (own group + top 5 competitors by threat level) |
| Colour | Own group = `#6366F1` (accent), competitors = palette of `#3B82F6`, `#10B981`, `#F59E0B`, `#EF4444`, `#8B5CF6` |
| Tooltip | "[Entity]: ₹[fee] for [Class] ([+/-X%] vs own group)" |
| API | `GET /api/v1/group/{id}/marketing/analytics/competitor-benchmarking/charts/fee-comparison/` |

### 7.2 Positioning Map (Bubble Chart)

| Property | Value |
|---|---|
| Chart type | Bubble (Chart.js 4.x) |
| Title | "Competitive Positioning — Fee vs Academic Results" |
| Data | X = avg annual fee (₹); Y = topper count (≥90%); R = estimated student strength (scaled) |
| Colour | Own group = `#6366F1` (solid, labelled), competitors = `#94A3B8` with threat-based border (High = red, Medium = amber, Low = green) |
| Quadrant lines | Median fee (vertical dashed), Median toppers (horizontal dashed) |
| Tooltip | "[Competitor]: Fee ₹[X], Toppers [Y], Students ~[Z]" |
| API | `GET /api/v1/group/{id}/marketing/analytics/competitor-benchmarking/charts/positioning-map/` |

### 7.3 Market Share Estimates (Pie)

| Property | Value |
|---|---|
| Chart type | Pie (Chart.js 4.x) |
| Title | "Estimated Market Share — [City]" |
| Data | % share per entity based on estimated student counts in selected city |
| Colour | Own group = `#6366F1`, competitors = standard palette, "Others" = `#CBD5E1` grey |
| Tooltip | "[Entity]: ~[N] students ([X]% share)" |
| Centre text | Total estimated students: [N] |
| API | `GET /api/v1/group/{id}/marketing/analytics/competitor-benchmarking/charts/market-share/` |

### 7.4 Competitive Gap Radar

| Property | Value |
|---|---|
| Chart type | Radar (Chart.js 4.x) |
| Title | "Competitive Gap — Own Group vs [Selected Competitor]" |
| Data | 6 axes: Fee Competitiveness / Topper Results / Branch Network / Infrastructure / Brand Recall / Digital Presence |
| Colour | Own group = `#6366F1` (filled, 20% opacity), Competitor = `#EF4444` (filled, 20% opacity) |
| Scale | 1–10 per axis (analyst-scored) |
| Tooltip | "[Axis]: Own [X] vs [Competitor] [Y]" |
| API | `GET /api/v1/group/{id}/marketing/analytics/competitor-benchmarking/charts/gap-radar/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Competitor added | "Competitor '[Name]' added to tracking database" | Success | 3s |
| Competitor updated | "Competitor '[Name]' details updated" | Success | 3s |
| Intelligence logged | "Intelligence entry logged — [Category] for [Competitor]" | Success | 3s |
| SWOT saved | "SWOT analysis updated for '[Competitor]' — next review [Date]" | Success | 4s |
| Fee revision saved | "Fee data updated for '[Competitor]' — [Year]" | Success | 3s |
| Comparison generated | "Comparison report generated — [N] competitors × [M] dimensions" | Success | 3s |
| Comparison exported | "Comparison exported as [Format] — download ready" | Success | 3s |
| High-impact intel | "HIGH IMPACT: [Competitor] — [Summary]. Review recommended." | Warning | 6s |
| Competitor deactivated | "Competitor '[Name]' deactivated — moved to inactive" | Info | 3s |
| Duplicate competitor | "Possible duplicate: '[Name]' matches existing '[Existing Name]'" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No competitors tracked | 🏢 | "No Competitors Tracked" | "Add your key competitors to start benchmarking fees, results, and market position." | Add Competitor |
| No intelligence entries | 📡 | "No Intelligence Logged" | "Log competitor moves — new branches, fee changes, topper claims, ad campaigns — to stay ahead." | Log Intelligence |
| No SWOT analyses | 📋 | "No SWOT Analyses" | "Create SWOT analyses for your top competitors to identify strategic opportunities." | Start SWOT |
| No fee data | 💰 | "No Fee Data Available" | "Enter competitor fee structures from their websites or prospectuses for comparison." | Add Fee Data |
| No results for filter | 🔍 | "No Matching Results" | "Adjust filters to find competitors or intelligence entries." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + filter bar + table skeleton (12 rows) |
| Tab switch | Content skeleton |
| Competitor detail drawer | 720px skeleton: profile card + 6 tabs |
| Fee comparison matrix | Table shimmer with header row + 8 data rows |
| Positioning map chart | Grey canvas placeholder with axis labels |
| Comparison builder modal | Step indicator + form skeleton |
| SWOT cards | 2×2 grid skeleton cards |
| Intelligence log load | Table skeleton (15 rows) |
| Chart load | Grey canvas placeholder |
| Export generation | Spinner: "Generating [Format] export..." |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/` | G1+ | List competitors (paginated, filterable) |
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/{comp_id}/` | G1+ | Competitor detail |
| POST | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/` | G1+ | Add competitor |
| PUT | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/{comp_id}/` | G1+ | Update competitor |
| DELETE | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/{comp_id}/` | G4+ | Delete competitor |
| PATCH | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/{comp_id}/deactivate/` | G3+ | Deactivate competitor |
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/{comp_id}/fees/` | G1+ | Fee history for competitor |
| POST | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/{comp_id}/fees/` | G1+ | Add/update fee revision |
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/fee-matrix/` | G1+ | Cross-competitor fee comparison matrix |
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/intelligence/` | G1+ | List intelligence entries (paginated) |
| POST | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/intelligence/` | G1+ | Log intelligence entry |
| PUT | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/intelligence/{intel_id}/` | G1+ | Update intelligence entry |
| DELETE | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/intelligence/{intel_id}/` | G3+ | Delete intelligence entry |
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/{comp_id}/swot/` | G1+ | Current SWOT for competitor |
| POST | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/{comp_id}/swot/` | G1+ | Save new SWOT version |
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/{comp_id}/swot/history/` | G1+ | SWOT version history |
| POST | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/comparison/` | G1+ | Generate comparison report |
| POST | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/export/` | G1+ | Export benchmarking data |
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/charts/fee-comparison/` | G1+ | Fee comparison chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/charts/positioning-map/` | G1+ | Positioning bubble chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/charts/market-share/` | G1+ | Market share pie data |
| GET | `/api/v1/group/{id}/marketing/analytics/competitor-benchmarking/charts/gap-radar/` | G1+ | Competitive gap radar data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../competitor-benchmarking/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#benchmarking-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Dropdowns | `hx-get` with params | `#competitor-table-body` | `innerHTML` | `hx-trigger="change"` |
| Competitor detail drawer | Row click | `hx-get=".../competitor-benchmarking/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Add competitor | Form submit | `hx-post=".../competitor-benchmarking/"` | `#add-result` | `innerHTML` | Toast + table refresh |
| Log intelligence | Form submit | `hx-post=".../competitor-benchmarking/intelligence/"` | `#intel-list` | `beforeend` | Prepends to log |
| Save SWOT | Form submit | `hx-post=".../competitor-benchmarking/{id}/swot/"` | `#swot-card-{id}` | `innerHTML` | Inline SWOT card update |
| Fee matrix load | Fee tab click | `hx-get=".../competitor-benchmarking/fee-matrix/"` | `#fee-matrix-content` | `innerHTML` | Matrix render |
| Comparison generate | Builder submit | `hx-post=".../competitor-benchmarking/comparison/"` | `#comparison-result` | `innerHTML` | Multi-step wizard |
| Positioning map load | Map tab / page load | `hx-get=".../competitor-benchmarking/charts/positioning-map/"` | `#chart-positioning` | `innerHTML` | `hx-trigger="intersect once"` |
| Chart load | Tab/section visible | `hx-get=".../competitor-benchmarking/charts/..."` | `#chart-{name}` | `innerHTML` | `hx-trigger="intersect once"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#competitor-table-body` | `innerHTML` | 25/page |
| Export | Export button | `hx-post=".../competitor-benchmarking/export/"` | `#export-result` | `innerHTML` | Download trigger |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
