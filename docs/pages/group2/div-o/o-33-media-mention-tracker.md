# O-33 — Media Mention Tracker

> **URL:** `/group/marketing/pr/media-mentions/`
> **File:** `o-33-media-mention-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary tracker

---

## 1. Purpose

The Media Mention Tracker is the group's centralised monitoring system for all media coverage — newspaper clippings, TV news segments, online articles, magazine features, blog posts, and social media mentions — across all publications, channels, and languages. In the Indian education market, media coverage is both a marketing asset and a reputation risk. When Eenadu runs a front-page story on "Narayana students sweep JEE Advanced Top 100," that single clipping is worth more than a ₹5 lakh full-page ad. Conversely, when Sakshi reports "Parents protest fee hike at Sri Chaitanya branch," that story circulates on WhatsApp parent groups within hours and damages admissions for the entire season.

The problems this page solves:

1. **Scattered clipping collection:** After results season, branches cut newspaper clippings, photograph them on phones, and WhatsApp them to head office. Some are blurry. Some are cropped. Some are never sent. TV coverage is watched live but never recorded. Online articles are bookmarked but the URLs break. Without a system, the group has no reliable archive of its media presence.

2. **No media value quantification:** Marketing directors and CEOs ask "What is our media coverage worth?" Advertising Value Equivalent (AVE) — the cost the group would have paid to buy the same space as a paid advertisement — is the standard industry metric. A half-page story in Eenadu Hyderabad edition is worth ₹2.2 lakh (rate card) × multiplier (earned media is valued 2–3× because editorial credibility exceeds ad credibility). Without tracking, the group cannot calculate total earned media value and compare it against paid media spend.

3. **Sentiment blind spots:** Not all coverage is positive. Fee hike protests, student safety incidents, teacher misconduct allegations, exam malpractice rumours — these negative stories require immediate crisis communication. Without systematic tracking, negative coverage is discovered only when parents call to cancel admissions.

4. **Competitive intelligence:** Tracking competitor mentions — "Sri Chaitanya opens 10 new branches in Karnataka" or "FIITJEE announces partnership with IIT faculty" — provides strategic intelligence for the group's planning.

5. **Historical archive:** Media coverage history is invaluable for NAAC accreditation documentation (colleges), CBSE affiliation renewals (schools), and government grant applications where "media recognition" is a supporting criterion.

**Scale:** 50–500 media mentions per season · 3 languages · 10–30 publications actively tracked · ₹10L–₹2Cr estimated AVE per season · Sentiment split typically 75% positive / 15% neutral / 10% negative

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — add mentions, upload clippings, set sentiment, calculate AVE | Primary tracker |
| Group Topper Relations Manager | 120 | G3 | Read + Add — log topper-related coverage | Co-contributor |
| Group Campaign Content Coordinator | 131 | G2 | Read + Upload — upload clippings, attach to mentions | Clipping management |
| Group Admission Data Analyst | 132 | G1 | Read + Export — media analytics, AVE reports | MIS and reporting |
| Group CEO / Chairman | — | G4/G5 | Read — monitor coverage, especially negative sentiment alerts | Executive overview |
| Branch Principal | — | G3 | Read (own branch mentions) — view coverage mentioning their branch | Reference only |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Create/edit mentions: role 119, 120, or G4+. Clipping upload: role 119, 120, 131. AVE override: G4+ only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  PR & Media  ›  Media Mention Tracker
```

### 3.2 Page Header
```
Media Mention Tracker                              [+ Add Mention]  [Bulk Upload]  [AVE Report]  [Export]
Campaign Manager — Ramesh Venkataraman
Sunrise Education Group · Season 2025-26 · 214 mentions · ₹84,60,000 AVE · 82% positive
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Mentions | Integer | COUNT(mentions) WHERE season = current | Static blue | `#kpi-total` |
| 2 | Positive | Integer | COUNT WHERE sentiment = 'positive' | Static green | `#kpi-positive` |
| 3 | Negative | Integer | COUNT WHERE sentiment = 'negative' | Red > 0, else green (zero) | `#kpi-negative` |
| 4 | Total AVE | ₹ Amount | SUM(ave_value) this season | Static emerald | `#kpi-ave` |
| 5 | This Month | Integer | COUNT WHERE created_at within current month | Static blue | `#kpi-monthly` |
| 6 | Pending OCR | Integer | COUNT WHERE clipping_uploaded = true AND ocr_status = 'pending' | Amber > 10, Red > 25 | `#kpi-ocr-pending` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/media-mentions/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **All Mentions** — Master list of all media mentions
2. **Clipping Gallery** — Visual grid of uploaded newspaper/magazine clippings
3. **Sentiment Dashboard** — Sentiment analysis and trend monitoring
4. **AVE Report** — Advertising Value Equivalent calculations and reporting

### 5.2 Tab 1: All Mentions

**Filter bar:** Season · Medium (Print/TV/Digital/Magazine/Blog/Social) · Sentiment (Positive/Neutral/Negative) · Publication · Language (Telugu/English/Hindi) · Category (Topper Results/Event Coverage/Fee Related/General/Negative Incident/Competitor) · Branch mentioned · Date range

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Date | Date | Yes | Date of publication/broadcast |
| Headline / Title | Text (link) | Yes | Click → detail drawer |
| Publication / Channel | Text | Yes | Eenadu / Sakshi / TV9 / NDTV / etc. |
| Medium | Badge | Yes | Print / TV / Digital / Magazine / Blog / Social |
| Language | Badge | Yes | Telugu / English / Hindi |
| Category | Badge | Yes | Topper Results / Event Coverage / Branch Opening / Fee Related / General / Negative Incident / Competitor |
| Sentiment | Badge | Yes | 🟢 Positive / 🟡 Neutral / 🔴 Negative |
| Clipping | Thumbnail (40×40) | No | Uploaded scan; grey placeholder if none |
| Page / Slot | Text | No | "Page 3" or "9 PM Prime" or "Homepage" |
| Branch(es) | Text | Yes | Which branches mentioned |
| AVE (₹) | Currency | Yes | Calculated advertising value equivalent |
| Source | Badge | No | Manual / OCR Auto / Google Alert / Agency |
| Actions | Buttons | No | [View] [Edit] [Upload Clipping] |

**Default sort:** Date DESC (most recent first)
**Pagination:** Server-side · 25/page

### 5.3 Tab 2: Clipping Gallery

Visual grid of uploaded newspaper/TV/magazine clippings, displayed as thumbnails with overlay metadata.

**Grid card layout (4 columns):**
```
┌─────────────────────────┐
│  [Clipping Image]        │
│                          │
│  📰 Eenadu (Telugu)      │
│  "Sunrise Toppers Shine" │
│  12-May-2026 · Page 3    │
│  🟢 Positive · ₹2.2L AVE │
│  [View Full] [Download]  │
└─────────────────────────┘
```

**Filters:** Same as Tab 1
**Sort:** Date DESC
**Pagination:** 20 cards per page (lazy load on scroll)

**OCR extraction panel:** When a clipping is uploaded (JPEG/PNG/PDF), the system queues OCR extraction via server-side Tesseract (Telugu + English + Hindi language packs). OCR output is stored as searchable text, enabling full-text search across clippings. OCR confidence score displayed; low-confidence extractions flagged for manual review.

### 5.4 Tab 3: Sentiment Dashboard

Aggregate sentiment analysis view with trend monitoring.

#### 5.4.1 Sentiment Summary

| Metric | Value | Visual |
|---|---|---|
| Positive mentions | 176 (82%) | Green progress bar |
| Neutral mentions | 24 (11%) | Amber progress bar |
| Negative mentions | 14 (7%) | Red progress bar |
| Sentiment score | +0.75 (scale −1 to +1) | Gauge chart |

#### 5.4.2 Negative Mention Alert Panel

Top-priority section showing all negative mentions with:
- Date, publication, headline, summary
- Branch affected
- Response status: Not Addressed / Response Drafted / Response Published / Resolved
- Assigned to (who is handling the crisis communication)

**Indian-specific negative categories:**
- Fee hike protests (most common — parents protest mid-year fee increases)
- Student safety incidents (bus accidents, campus incidents — POCSO implications)
- Exam malpractice allegations (leaked papers, proxy exams)
- Teacher misconduct (rare but high-impact)
- RTE compliance issues (non-admission of EWS students)
- Infrastructure complaints (overcrowding, lack of facilities)

#### 5.4.3 Competitor Mention Tracker

Separate sub-section tracking mentions of competitor groups:

| Competitor | Mentions | Positive | Neutral | Negative | Key Themes |
|---|---|---|---|---|---|
| Sri Chaitanya | 45 | 38 | 5 | 2 | JEE results, expansion |
| FIITJEE | 22 | 18 | 3 | 1 | Faculty, online |
| Allen Career | 18 | 15 | 2 | 1 | NEET results |

### 5.5 Tab 4: AVE Report

Advertising Value Equivalent report for earned media valuation.

#### 5.5.1 AVE Calculation Method

| Factor | Description | Source |
|---|---|---|
| Base rate | Publication's rate card for equivalent ad space (from O-10 Publication Master) | Auto-linked |
| Size factor | Full page = 1.0 / Half page = 0.5 / Quarter page = 0.25 / Brief mention = 0.1 | Dropdown on mention |
| Placement factor | Front page = 3.0 / Page 2-3 = 2.0 / Inside = 1.0 / Supplement = 0.8 | Dropdown on mention |
| Colour factor | Colour = 1.0 / B&W = 0.6 | Auto-detect or manual |
| Earned media multiplier | Editorial coverage credibility multiplier: Print = 2.5× / TV = 3.0× / Digital = 1.5× | Configurable by G4 |
| **AVE = Base rate × Size × Placement × Colour × Multiplier** | | |

#### 5.5.2 AVE Summary Table

| Publication | Mentions | Total AVE (₹) | % of Total | Top Story |
|---|---|---|---|---|
| Eenadu | 42 | ₹28,40,000 | 33.5% | "Sunrise JEE Results 2026" |
| Sakshi | 38 | ₹22,60,000 | 26.7% | "4,200 students above 90% in TSBIE" |
| Deccan Chronicle | 18 | ₹12,80,000 | 15.1% | "Sunrise felicitation ceremony" |
| TV9 Telugu | 8 | ₹8,40,000 | 9.9% | Results day live coverage |
| Times of India | 12 | ₹6,20,000 | 7.3% | "Education group expands to Karnataka" |

**Total earned media AVE vs paid media spend comparison:** AVE / Total ad spend (from O-09) = Earned Media Ratio. Target: ≥ 1.0 (earned media worth at least as much as paid).

---

## 6. Drawers & Modals

### 6.1 Modal: `add-mention` (640px)

- **Title:** "Add Media Mention"
- **Fields:**
  - **Publication details:**
    - Publication / Channel (dropdown from media master + free text, required)
    - Medium (dropdown, required): Print / TV / Digital / Magazine / Blog / Social Media
    - Language (dropdown, required): Telugu / English / Hindi / Other
    - Date of publication/broadcast (date, required)
  - **Content details:**
    - Headline / Title (text, required)
    - Summary (textarea — 2-3 sentence description of the coverage)
    - Full text (textarea, optional — or auto-filled via OCR)
    - Online URL (URL, optional — for digital publications)
    - Page number / TV slot / Section (text)
  - **Classification:**
    - Category (dropdown, required): Topper Results / Event Coverage / Branch Opening / Fee Related / Award / General / Negative Incident / Competitor Mention
    - Sentiment (dropdown, required): Positive / Neutral / Negative
    - Branch(es) mentioned (multi-select, optional)
    - Related press release (dropdown — link to O-32 release that generated this coverage, optional)
    - Related toppers (multi-select from O-28, optional)
  - **Clipping:**
    - Upload clipping (file — JPEG/PNG/PDF, max 15 MB)
    - Upload video clip (file — MP4, max 100 MB, for TV coverage)
    - Screenshot (file — for online coverage)
  - **AVE inputs:**
    - Coverage size (dropdown): Full Story / Half Story / Brief Mention / Headline Only / Photo Only
    - Placement (dropdown): Front Page / Page 2-3 / Inside / Supplement / Homepage / Below Fold
    - Auto-calculated AVE (display) — editable override for G4+
  - **Source:**
    - How discovered (dropdown): Manual / Google Alert / Agency Provided / Branch Reported / Social Monitoring
- **Buttons:** Cancel · Save
- **Access:** Role 119, 120, 131, or G4+

### 6.2 Modal: `bulk-upload` (560px)

- **Title:** "Bulk Upload Clippings"
- **Step 1:** Drag-and-drop multiple files (JPEG/PNG/PDF, max 15 MB each, up to 20 files)
- **Step 2:** OCR processing queue — shows progress bar per file
- **Step 3:** Review extracted text + auto-detected publication/date/headline (where possible)
- **Step 4:** Manual metadata entry for fields OCR could not extract: sentiment, category, branch, AVE inputs
- **Step 5:** Confirm and save all mentions
- **Buttons:** Cancel · Process · Save All
- **Access:** Role 119, 131, or G4+

### 6.3 Drawer: `mention-detail` (720px, right-slide)

- **Tabs:** Overview · Clipping · OCR Text · AVE · Linked
- **Overview tab:** Full metadata — publication, date, headline, summary, sentiment badge, category, branches mentioned, source
- **Clipping tab:** Full-resolution clipping image (zoomable), video player (for TV clips), original file download
- **OCR Text tab:** Extracted text from clipping OCR; confidence score; editable (for corrections); full-text searchable
- **AVE tab:** AVE calculation breakdown — base rate, size factor, placement factor, multiplier, final AVE value; edit factors if G4+
- **Linked tab:** Linked press release (O-32), linked toppers (O-28), linked event (O-29)
- **Footer:** [Edit] [Recalculate AVE] [Upload Better Clipping] [Link to Release] [Delete]

### 6.4 Modal: `negative-response` (560px, for negative mentions)

- **Title:** "Respond to Negative Coverage — [Headline]"
- **Fields:**
  - Severity (dropdown): Low (factual error) / Medium (complaint coverage) / High (safety incident) / Critical (legal/regulatory)
  - Assigned to (dropdown — team member responsible for response)
  - Response strategy (dropdown): No Action / Factual Correction / Official Statement / Legal Notice / Meeting with Editor
  - Response draft (rich text — the official response or clarification)
  - Response status (dropdown): Not Addressed / Response Drafted / Response Sent / Published Correction / Resolved
  - Follow-up date (date, optional)
  - Notes (textarea)
- **Buttons:** Cancel · Save Response
- **Access:** Role 119 or G4+ (negative mentions require escalation to G4)

---

## 7. Charts

### 7.1 Sentiment Trend (Line Chart)

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "Media Sentiment Trend — Monthly" |
| Data | Per month: count positive, neutral, negative mentions |
| Colour | Green = positive, Amber = neutral, Red = negative |
| Tooltip | "[Month]: [X] positive, [Y] neutral, [Z] negative" |
| API | `GET /api/v1/group/{id}/marketing/media-mentions/analytics/sentiment-trend/` |

### 7.2 AVE by Publication (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Advertising Value Equivalent by Publication" |
| Data | Total AVE per publication |
| Colour | `#10B981` green gradient |
| Tooltip | "[Publication]: ₹[X] AVE across [N] mentions" |
| API | `GET /api/v1/group/{id}/marketing/media-mentions/analytics/ave-by-publication/` |

### 7.3 Medium Distribution (Doughnut)

| Property | Value |
|---|---|
| Chart type | Doughnut |
| Title | "Mentions by Medium" |
| Data | COUNT per medium (Print, TV, Digital, Magazine, Blog, Social) |
| Colour | Medium-specific palette |
| Tooltip | "[Medium]: [N] mentions ([X]%)" |
| API | `GET /api/v1/group/{id}/marketing/media-mentions/analytics/by-medium/` |

### 7.4 Earned vs Paid Comparison (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar |
| Title | "Earned Media (AVE) vs Paid Media Spend — Monthly" |
| Data | Per month: total AVE from earned media, total paid media spend (from O-09/O-10/O-11) |
| Colour | Green = earned (AVE), Blue = paid |
| Purpose | Show ROI of PR efforts compared to advertising spend |
| API | `GET /api/v1/group/{id}/marketing/media-mentions/analytics/earned-vs-paid/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Mention added | "Media mention added: '[Headline]' — [Publication]" | Success | 3s |
| Mention updated | "Media mention updated" | Success | 2s |
| Clipping uploaded | "Clipping uploaded — OCR processing queued" | Success | 3s |
| OCR completed | "OCR extraction complete for [N] clippings" | Success | 4s |
| OCR failed | "OCR failed for '[Filename]' — upload clearer image" | Warning | 5s |
| Bulk upload complete | "[N] clippings uploaded, [M] processed successfully" | Success | 4s |
| AVE recalculated | "AVE recalculated: ₹[Amount]" | Info | 3s |
| Negative mention alert | "⚠ Negative coverage detected: '[Headline]' in [Publication]" | Error | 6s |
| Response saved | "Response to '[Headline]' saved — status: [Status]" | Success | 3s |
| Export ready | "Media mention report ready for download" | Success | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No mentions this season | 📰 | "No Media Mentions Tracked" | "Add media mentions to track your group's coverage across newspapers, TV, and digital publications." | Add Mention |
| No clippings uploaded | 🖼️ | "No Clippings Yet" | "Upload newspaper clippings and screenshots to build your media archive." | Upload Clipping |
| No negative mentions | ✅ | "All Clear" | "No negative media coverage this season. Keep monitoring." | — |
| No AVE data | 📊 | "No AVE Calculated" | "Add mentions with coverage size and placement to calculate advertising value equivalent." | — |
| No mentions for filter | 🔍 | "No Matching Mentions" | "Adjust filters to find media mentions." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + filter bar + table skeleton (12 rows) |
| Tab switch | Content skeleton |
| Clipping gallery load | Grid placeholder (8 cards) |
| Mention detail drawer | 720px skeleton: tabs + image placeholder + text lines |
| Clipping image load | Image placeholder with spinner |
| OCR processing | Progress bar: "Processing [N] of [M] clippings…" |
| Bulk upload wizard | Step content shimmer + file list skeleton |
| AVE report load | Table skeleton + summary cards shimmer |
| Sentiment dashboard | Gauge placeholder + alert panel skeleton |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/media-mentions/` | G1+ | List mentions (paginated, filterable) |
| GET | `/api/v1/group/{id}/marketing/media-mentions/{mention_id}/` | G1+ | Mention detail |
| POST | `/api/v1/group/{id}/marketing/media-mentions/` | G2+ | Add mention |
| PUT | `/api/v1/group/{id}/marketing/media-mentions/{mention_id}/` | G3+ | Update mention |
| DELETE | `/api/v1/group/{id}/marketing/media-mentions/{mention_id}/` | G4+ | Delete mention |
| POST | `/api/v1/group/{id}/marketing/media-mentions/{mention_id}/clipping/` | G2+ | Upload clipping |
| GET | `/api/v1/group/{id}/marketing/media-mentions/{mention_id}/ocr/` | G1+ | Get OCR text |
| PUT | `/api/v1/group/{id}/marketing/media-mentions/{mention_id}/ocr/` | G3+ | Edit OCR text |
| POST | `/api/v1/group/{id}/marketing/media-mentions/bulk-upload/` | G3+ | Bulk upload clippings |
| PATCH | `/api/v1/group/{id}/marketing/media-mentions/{mention_id}/ave/` | G3+ | Recalculate/override AVE |
| PATCH | `/api/v1/group/{id}/marketing/media-mentions/{mention_id}/response/` | G3+ | Save negative response |
| GET | `/api/v1/group/{id}/marketing/media-mentions/gallery/` | G1+ | Clipping gallery (paginated) |
| GET | `/api/v1/group/{id}/marketing/media-mentions/sentiment/` | G1+ | Sentiment dashboard data |
| GET | `/api/v1/group/{id}/marketing/media-mentions/ave-report/` | G1+ | AVE summary report |
| GET | `/api/v1/group/{id}/marketing/media-mentions/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/media-mentions/analytics/sentiment-trend/` | G1+ | Sentiment trend chart |
| GET | `/api/v1/group/{id}/marketing/media-mentions/analytics/ave-by-publication/` | G1+ | AVE bar chart |
| GET | `/api/v1/group/{id}/marketing/media-mentions/analytics/by-medium/` | G1+ | Medium doughnut |
| GET | `/api/v1/group/{id}/marketing/media-mentions/analytics/earned-vs-paid/` | G1+ | Earned vs paid chart |
| POST | `/api/v1/group/{id}/marketing/media-mentions/export/` | G1+ | Export report |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../media-mentions/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#mentions-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Dropdowns | `hx-get` with params | `#mentions-table-body` | `innerHTML` | `hx-trigger="change"` |
| Mention detail drawer | Row click | `hx-get=".../media-mentions/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Add mention | Form submit | `hx-post=".../media-mentions/"` | `#add-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Upload clipping | File upload | `hx-post=".../media-mentions/{id}/clipping/"` | `#clipping-preview` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Bulk upload | Upload form | `hx-post=".../media-mentions/bulk-upload/"` | `#bulk-upload-wizard` | `innerHTML` | Multi-step with progress |
| OCR result load | Clipping processed | `hx-get=".../media-mentions/{id}/ocr/"` | `#ocr-content` | `innerHTML` | `hx-trigger="load"` on OCR tab |
| AVE recalculate | Override form | `hx-patch=".../media-mentions/{id}/ave/"` | `#ave-display-{id}` | `innerHTML` | Inline value update |
| Sentiment dashboard | Tab click | `hx-get=".../media-mentions/sentiment/"` | `#sentiment-content` | `innerHTML` | Loads gauge + alert panel |
| Gallery load | Gallery tab | `hx-get=".../media-mentions/gallery/"` | `#gallery-content` | `innerHTML` | Grid layout |
| Gallery scroll | Scroll bottom | `hx-get=".../media-mentions/gallery/?page={n}"` | `#gallery-grid` | `beforeend` | Infinite scroll append |
| Negative response | Response form | `hx-patch=".../media-mentions/{id}/response/"` | `#response-status-{id}` | `innerHTML` | Badge update |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#mentions-table-body` | `innerHTML` | 25/page |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
