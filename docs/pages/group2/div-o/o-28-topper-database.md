# O-28 — Topper Database & Showcase

> **URL:** `/group/marketing/toppers/database/`
> **File:** `o-28-topper-database.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Topper Relations Manager (Role 120, G3) — primary curator

---

## 1. Purpose

The Topper Database & Showcase is the group's crown jewel marketing asset — a structured, searchable, media-ready database of every academic achiever across all branches, all boards, and all competitive exams. In the Indian education market, toppers are the ultimate social proof. When Narayana announces "4,200 students scored above 95% in Telangana Intermediate" or Sri Chaitanya publishes "312 of our students cracked JEE Advanced Top 10,000," parents queue up for admissions. The group that can quickly compile, verify, photograph, and publish topper data within 24 hours of results wins the news cycle and the next admission season.

The problems this page solves:

1. **Data compilation chaos:** Board results (CBSE, ICSE, 28 state boards), competitive exam results (JEE Main, JEE Advanced, NEET, CLAT, CUET), and internal scholarship exam results arrive on different dates. Each branch has 20–500 toppers to compile. Without a central database, branches send Excel sheets by WhatsApp, photos are missing, marks are misreported, and the marketing team spends 3 days verifying what should take 3 hours.

2. **Photo + testimonial readiness:** Every topper display (newspaper ad, flex banner, website, WhatsApp broadcast) needs: student photo, marks/rank, branch, parent quote, student quote. The database ensures these are pre-collected (photo day before results) or rapidly collected (within 24 hours post-results).

3. **Multi-format publishing:** The same topper data powers: full-page newspaper ads (top 50 toppers with photos), WhatsApp broadcasts (result summaries), website showcase pages, social media posts (individual topper cards), flex banners at branch gates, and felicitation event invitations. The database feeds all these formats via templates.

4. **Historical archive:** Toppers from previous years are marketing gold — "Our alumni who cracked IIT, AIIMS, NLU" stories. The database maintains multi-year records with current career status where available.

**Scale:** 200–5,000 toppers/season · 5–50 branches · 3–10 exam types · 5–15 publishing formats · 2–5 year historical depth

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Topper Relations Manager | 120 | G3 | Full CRUD — add, edit, verify, publish toppers | Primary curator |
| Group Admissions Campaign Manager | 119 | G3 | Read + Use — access topper data for campaigns | Uses in campaign materials |
| Group Campaign Content Coordinator | 131 | G2 | Read + Download — access photos and data for creative design | Creates topper ad layouts |
| Group Admission Data Analyst | 132 | G1 | Read — topper analytics, branch-wise result summaries | MIS and reports |
| Branch Principal | — | G3 | Read + Submit (own branch) — submit topper data and photos | Initial data entry |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — verify showcase before public release | Quality gate |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Topper creation/editing: role 120 or G4+. Branch principals can submit for own branch via portal. Publishing: role 120 with G4 approval.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Topper Relations  ›  Topper Database & Showcase
```

### 3.2 Page Header
```
Topper Database & Showcase                           [+ Add Topper]  [Bulk Import]  [Publish Showcase]  [Export]
Topper Relations Manager — Lakshmi Naidu
Sunrise Education Group · Results Season 2025-26 · 1,842 toppers · 28 branches · 3 boards · 4 exams
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Toppers | Integer | COUNT WHERE season = current | Static blue | `#kpi-total` |
| 2 | Board Toppers (≥90%) | Integer | COUNT WHERE exam_type = 'board' AND percentage ≥ 90 | Static green | `#kpi-board` |
| 3 | JEE/NEET Qualifiers | Integer | COUNT WHERE exam_type IN ('jee_main','jee_adv','neet') AND qualified = true | Static emerald | `#kpi-competitive` |
| 4 | Photos Pending | Integer | COUNT WHERE photo_status = 'pending' | Red > 50, Amber 10–50, Green < 10 | `#kpi-photos-pending` |
| 5 | Published | Integer | COUNT WHERE status = 'published' | Static blue | `#kpi-published` |
| 6 | Branches Reported | N/M | Branches that submitted data / total branches | Green = all, Red = incomplete | `#kpi-branches` |

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Topper Directory** — Searchable, filterable master list
2. **Result Summary** — Board/exam-wise aggregate results
3. **Showcase Builder** — Create publishable topper showcases
4. **Archive** — Historical toppers (previous seasons)

### 5.2 Tab 1: Topper Directory

**Filter bar:** Season · Branch · Board/Exam · Percentage/Rank Range · Photo Status (Ready/Pending) · Published Status · Category (General/SC/ST/OBC)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Photo | Thumbnail (50×50) | No | Student photo; grey placeholder if pending |
| Student Name | Text (link) | Yes | Click → detail drawer |
| Branch | Text | Yes | — |
| Board/Exam | Badge | Yes | CBSE / TSBIE / AP Board / ICSE / JEE Main / JEE Adv / NEET / CLAT / CUET |
| Class | Badge | Yes | Class 10 / Class 12 / Jr Inter / Sr Inter |
| Stream | Badge | Yes | MPC / BiPC / MEC / CEC / General |
| Percentage / Rank | Text | Yes | "98.4%" or "AIR 1,245" or "State Rank 42" |
| Subject Topper | Badge | No | If topped any individual subject: "Maths: 100" |
| Parent Name | Text | No | — |
| Testimonial | Badge | Yes | ✅ Collected / ❌ Pending |
| Photo | Badge | Yes | ✅ Ready / 📸 Pending / ❌ Not Available |
| Status | Badge | Yes | Draft / Verified / Published / Archived |
| Actions | Buttons | No | [View] [Edit] [Publish] [Generate Card] |

**Default sort:** Percentage DESC (highest achievers first)
**Pagination:** Server-side · 50/page

### 5.3 Tab 2: Result Summary

Aggregate results dashboard:

#### 5.3.1 Board Results Summary

| Board | Students Appeared | Pass % | ≥90% | ≥95% | ≥98% | Centum (100) | State/National Ranks |
|---|---|---|---|---|---|---|---|
| TSBIE (Telangana) | 4,200 | 99.2% | 1,420 | 380 | 45 | 12 (in Maths) | State 1st: Sai Krishna |
| AP Board | 2,100 | 98.8% | 680 | 180 | 22 | 5 | — |
| CBSE | 800 | 99.5% | 340 | 120 | 18 | 8 | — |
| ICSE | 200 | 100% | 110 | 45 | 8 | 3 | — |

#### 5.3.2 Competitive Exam Summary

| Exam | Students Appeared | Qualified | Top 1,000 | Top 5,000 | Top 10,000 | Best Rank |
|---|---|---|---|---|---|---|
| JEE Main 2026 | 3,800 | 2,420 | 12 | 85 | 320 | AIR 342 |
| JEE Advanced 2026 | 1,200 | 680 | 3 | 28 | 95 | AIR 567 |
| NEET 2026 | 2,400 | 1,840 | 5 | 42 | 180 | AIR 1,245 |
| CLAT 2026 | 120 | 85 | — | 8 | 22 | AIR 2,340 |

### 5.4 Tab 3: Showcase Builder

Create publishable topper showcases in various formats:

**Showcase types:**
- **Newspaper Ad Layout** — Full-page / half-page with topper grid (photo + name + marks)
- **WhatsApp Card** — Individual topper card (1080×1080 px) or summary card
- **Website Banner** — Scrolling topper carousel for group website
- **Flex Banner** — Branch gate banner with top 10–20 toppers
- **Social Media Post** — Instagram/Facebook format cards
- **Press Release Data** — Formatted text block for media

**Builder interface:**
- Select toppers (filter + multi-select from directory)
- Choose template/format
- Auto-populate template with topper data
- Preview
- Download / Publish

### 5.5 Tab 4: Archive

Previous seasons' topper data with "Alumni Update" feature — track where former toppers are now (IIT, AIIMS, NLU, etc.) for long-term brand building.

---

## 6. Drawers & Modals

### 6.1 Modal: `add-topper` (640px)

- **Title:** "Add Topper Record"
- **Fields:**
  - **Student details:**
    - Student name (text, required)
    - Student photo (upload, max 5 MB — JPEG/PNG)
    - Branch (dropdown, required)
    - Class (dropdown): 10 / 12 / Jr Inter / Sr Inter
    - Stream (dropdown): MPC / BiPC / MEC / CEC / HEC / General
    - Admission year (when they joined the group)
  - **Exam details:**
    - Board/Exam (dropdown, required): CBSE / ICSE / TSBIE / AP Board / JEE Main / JEE Advanced / NEET / CLAT / CUET / Internal Scholarship / Other
    - Hall ticket / Roll number (text)
    - Result date (date)
    - Overall percentage / CGPA / Marks (number)
    - Overall rank (integer, optional — for competitive exams)
    - State rank (integer, optional)
    - Subject-wise marks (dynamic form — add subject + marks):
      - Subject name (dropdown/text)
      - Marks obtained / Total marks
      - Subject rank (optional)
      - Centum (100/100)? (auto-detect)
  - **Testimonial:**
    - Student quote (textarea, optional — "I thank my teachers at Sunrise…")
    - Parent quote (textarea, optional)
    - Parent name (text)
    - Video testimonial URL (optional — YouTube/uploaded)
  - **Parent/contact details:**
    - Father name (text)
    - Mother name (text)
    - Phone (for felicitation invite)
  - **Categories:**
    - Category: General / SC / ST / OBC / EWS (for category-specific highlights)
    - Gender: Male / Female / Other
    - Hostel student? (toggle)
    - Scholarship student? (toggle — for "scholarship exam toppers" showcase)
  - **Verification:**
    - Upload marksheet / result screenshot (file, required for verification)
    - Verified by (auto-filled on verification)
- **Buttons:** Cancel · Save as Draft · Submit for Verification
- **Access:** Role 120, Branch Principal (own branch), or G4+

### 6.2 Modal: `bulk-import` (640px)

- **Title:** "Bulk Import Toppers"
- **Step 1:** Upload Excel/CSV with columns: Student Name, Branch, Board, Class, Stream, Percentage, Rank, Subject Marks
- **Step 2:** Map columns + validate data
- **Step 3:** Review — N valid, M errors, P duplicates
- **Step 4:** Import + assign photo collection tasks
- **Buttons:** Cancel · Import
- **Access:** Role 120 or G4+

### 6.3 Drawer: `topper-detail` (720px, right-slide)

- **Tabs:** Profile · Marks · Testimonial · Media · History
- **Profile tab:** Photo (large), name, branch, class, stream, board, overall marks/rank, category, admission year
- **Marks tab:** Subject-wise marks table, centum badges, rank details
- **Testimonial tab:** Student quote, parent quote, video embed (if available)
- **Media tab:** All photos (profile, with parents, felicitation), generated showcase cards, newspaper ad appearances
- **History tab:** If archived from previous season: current status (university, career), alumni connection
- **Footer:** [Edit] [Verify] [Generate Card] [Add to Showcase] [Publish] [Archive]

### 6.4 Modal: `generate-topper-card` (560px)

- **Title:** "Generate Topper Card — [Student Name]"
- **Template select:** WhatsApp Card / Social Media / Flex Banner / Press Release
- **Preview:** Rendered card with student photo, name, marks, branch, group branding
- **Customise:** Add/remove elements, adjust text, change photo crop
- **Buttons:** Cancel · Download PNG · Download PDF · Share via WhatsApp
- **Access:** Role 120, 131, or G4+

### 6.5 Modal: `verify-topper` (480px, G4/G5)

- **Title:** "Verify Topper Record"
- **Content:** Student details, marks, uploaded marksheet preview
- **Actions:** Verify ✅ / Reject ❌ (with reason) / Request Re-upload
- **Note:** Verification required before any topper can be published externally
- **Access:** Role 120 (initial verify), G4/G5 (final approval for publishing)

---

## 7. Charts

### 7.1 Toppers by Branch (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Toppers by Branch (≥90%)" |
| Data | COUNT per branch WHERE percentage ≥ 90 |
| Colour | `#10B981` green |
| Tooltip | "[Branch]: [N] toppers (≥90%)" |
| API | `GET /api/v1/group/{id}/marketing/toppers/database/analytics/by-branch/` |

### 7.2 Percentage Distribution (Histogram)

| Property | Value |
|---|---|
| Chart type | Bar histogram (Chart.js 4.x) |
| Title | "Score Distribution — [Board/Exam]" |
| Data | Count per percentage range: <60 / 60–70 / 70–80 / 80–90 / 90–95 / 95–98 / 98–100 |
| Colour | Progressive green (darker = higher) |
| API | `GET /api/v1/group/{id}/marketing/toppers/database/analytics/score-distribution/` |

### 7.3 Year-over-Year Comparison (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar |
| Title | "Toppers Year-over-Year — Last 3 Seasons" |
| Data | Per season: count ≥90%, ≥95%, ≥98% |
| Purpose | Show improving trend (or flag decline) |
| API | `GET /api/v1/group/{id}/marketing/toppers/database/analytics/yoy-comparison/` |

### 7.4 Subject-wise Centum Count (Bar)

| Property | Value |
|---|---|
| Chart type | Bar |
| Title | "Subject-wise 100/100 (Centum) Achievers" |
| Data | Per subject: count of centum scorers |
| Colour | `#EAB308` gold |
| API | `GET /api/v1/group/{id}/marketing/toppers/database/analytics/centum-count/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Topper added | "Topper '[Name]' added — [Board]: [Marks]" | Success | 3s |
| Bulk imported | "[N] toppers imported from [Branch/All]" | Success | 4s |
| Topper verified | "Topper '[Name]' verified ✅" | Success | 3s |
| Topper published | "Topper '[Name]' published to showcase" | Success | 3s |
| Card generated | "Topper card generated — download ready" | Success | 3s |
| Photo pending | "[N] toppers still need photos — prioritise collection" | Warning | 5s |
| Showcase published | "Showcase '[Name]' published with [N] toppers" | Success | 4s |
| Duplicate detected | "Possible duplicate: '[Name]' matches existing record" | Warning | 5s |
| Verification rejected | "Topper '[Name]' rejected — [Reason]" | Warning | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No toppers this season | 🏆 | "No Toppers Yet" | "Add toppers as board and exam results are announced." | Add Topper / Bulk Import |
| No photos collected | 📸 | "Photos Pending" | "[N] toppers need photos for showcase readiness." | — |
| No showcases created | 🎨 | "No Showcases" | "Create a topper showcase for newspaper ads, WhatsApp, or social media." | Create Showcase |
| No results for board | 📊 | "No Results for [Board]" | "Results for [Board] haven't been uploaded yet." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + filter bar + table skeleton (15 rows) |
| Tab switch | Content skeleton |
| Topper detail drawer | 720px skeleton: photo placeholder + 5 tabs |
| Bulk import wizard | Step content shimmer |
| Card generation | Spinner: "Generating card…" |
| Showcase builder | Template grid placeholder + preview area |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/toppers/database/` | G1+ | List toppers (filterable) |
| GET | `/api/v1/group/{id}/marketing/toppers/database/{topper_id}/` | G1+ | Topper detail |
| POST | `/api/v1/group/{id}/marketing/toppers/database/` | G3+ | Add topper |
| PUT | `/api/v1/group/{id}/marketing/toppers/database/{topper_id}/` | G3+ | Update topper |
| DELETE | `/api/v1/group/{id}/marketing/toppers/database/{topper_id}/` | G4+ | Delete topper |
| POST | `/api/v1/group/{id}/marketing/toppers/database/import/` | G3+ | Bulk import |
| PATCH | `/api/v1/group/{id}/marketing/toppers/database/{topper_id}/verify/` | G3+ | Verify topper |
| PATCH | `/api/v1/group/{id}/marketing/toppers/database/{topper_id}/publish/` | G3+ | Publish topper |
| POST | `/api/v1/group/{id}/marketing/toppers/database/{topper_id}/card/` | G2+ | Generate topper card |
| GET | `/api/v1/group/{id}/marketing/toppers/database/summary/` | G1+ | Result summary tables |
| GET | `/api/v1/group/{id}/marketing/toppers/database/showcases/` | G1+ | List showcases |
| POST | `/api/v1/group/{id}/marketing/toppers/database/showcases/` | G3+ | Create showcase |
| GET | `/api/v1/group/{id}/marketing/toppers/database/archive/` | G1+ | Historical toppers |
| GET | `/api/v1/group/{id}/marketing/toppers/database/kpis/` | G1+ | KPIs |
| GET | `/api/v1/group/{id}/marketing/toppers/database/analytics/by-branch/` | G1+ | Branch bar |
| GET | `/api/v1/group/{id}/marketing/toppers/database/analytics/score-distribution/` | G1+ | Histogram |
| GET | `/api/v1/group/{id}/marketing/toppers/database/analytics/yoy-comparison/` | G1+ | YoY chart |
| GET | `/api/v1/group/{id}/marketing/toppers/database/analytics/centum-count/` | G1+ | Centum chart |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../database/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#toppers-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Dropdowns | `hx-get` with params | `#topper-table-body` | `innerHTML` | `hx-trigger="change"` |
| Topper detail drawer | Row click | `hx-get=".../database/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Add topper | Form submit | `hx-post=".../database/"` | `#add-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Verify topper | Verify button | `hx-patch=".../database/{id}/verify/"` | `#status-badge-{id}` | `innerHTML` | Inline badge |
| Generate card | Generate form | `hx-post=".../database/{id}/card/"` | `#card-preview` | `innerHTML` | Shows card in modal |
| Bulk import | Import form | `hx-post=".../database/import/"` | `#import-wizard` | `innerHTML` | Multi-step |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#topper-table-body` | `innerHTML` | 50/page |
| Summary load | Summary tab | `hx-get=".../database/summary/"` | `#summary-content` | `innerHTML` | Tables render |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
