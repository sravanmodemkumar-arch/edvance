# O-32 — Press Release Manager

> **URL:** `/group/marketing/toppers/press-releases/`
> **File:** `o-32-press-release-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary drafter & distributor

---

## 1. Purpose

The Press Release Manager is the group's centralised press-release authoring, approval, and distribution system for all public communications — topper result announcements, felicitation event invitations, new branch launches, exam result highlights, award recognitions, and milestone achievements. In the Indian education market, press releases are the primary mechanism for earned media coverage: when Narayana announces "4,200 students scored above 90% in Telangana Intermediate" or Sri Chaitanya publishes "312 students in JEE Advanced Top 10,000," these announcements reach parents via Eenadu, Sakshi, Deccan Chronicle, Times of India, and 50+ regional publications — generating advertising-equivalent value worth lakhs without direct ad spend.

The problems this page solves:

1. **Language management chaos:** A Telangana-based group needs every press release in Telugu (for Eenadu, Sakshi, Namaste Telangana), English (for Deccan Chronicle, Times of India, The Hindu), and optionally Hindi (for Hindi-medium publications in states like Madhya Pradesh, Rajasthan, or Uttar Pradesh). Without a system, the Telugu version gets sent to the English desk, the English version has Telugu statistics, and the Hindi version is a week late.

2. **Approval bottleneck:** Press releases containing student marks, ranks, and institutional claims ("No. 1 in Telangana") must be verified before distribution. A single factual error — wrong rank, wrong percentage, wrong branch name — damages credibility with journalists and can trigger ASCI complaints. The system enforces Draft → Review → Approve (G4) before any distribution.

3. **Media list management:** The group maintains relationships with 50–200 journalists across print, TV, and digital media. Contact details change, beats rotate, publications restructure. Without a system, the Campaign Manager maintains a personal WhatsApp contact list that walks out the door when they leave.

4. **Distribution tracking:** After a press release is sent, which publications actually ran the story? Which journalist responded? Did the story appear on page 3 or page 17? Publication tracking closes the loop from release to coverage.

5. **Timing criticality:** Board results are announced at a specific hour. The group that sends its press release within 2 hours of results gets front-page coverage the next day. The group that takes 2 days gets nothing. The system pre-drafts releases with template data, then fills in actual numbers the moment results arrive.

**Scale:** 20–100 press releases per season · 3 languages · 50–200 journalist contacts · 10–30 publications tracked · 2–5 result days requiring same-day turnaround

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — draft, edit, submit for approval, distribute | Primary author |
| Group Topper Relations Manager | 120 | G3 | Read + Draft — create topper-specific releases | Co-author for topper PRs |
| Group Campaign Content Coordinator | 131 | G2 | Read + Edit drafts — proofread, format, attach media kit | Content support |
| Group Admission Data Analyst | 132 | G1 | Read — view releases and publication tracking | MIS reference |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve releases before distribution | Mandatory gate for external comms |
| Branch Principal | — | G3 | Read (own branch mentions) — view releases that mention their branch | Reference only |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Draft creation: role 119, 120, or G4+. Approval: G4/G5 only. Distribution: role 119 with approved status only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Topper Relations & PR  ›  Press Release Manager
```

### 3.2 Page Header
```
Press Release Manager                              [+ New Release]  [Media List]  [Templates]  [Export]
Campaign Manager — Ramesh Venkataraman
Sunrise Education Group · Season 2025-26 · 42 releases · 18 published · 156 journalist contacts
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Releases | Integer | COUNT(releases) WHERE season = current | Static blue | `#kpi-total` |
| 2 | Published | Integer | COUNT WHERE status = 'published' | Static green | `#kpi-published` |
| 3 | Pending Approval | Integer | COUNT WHERE status = 'review' | Amber > 5, Red > 10 | `#kpi-pending` |
| 4 | Media Pickups | Integer | COUNT(publication_trackings) WHERE picked_up = true this season | Static emerald | `#kpi-pickups` |
| 5 | Avg Turnaround | Duration | AVG(approved_at − created_at) for approved releases | Green ≤ 4h, Amber 4–24h, Red > 24h | `#kpi-turnaround` |
| 6 | Active Journalists | Integer | COUNT(journalist_contacts) WHERE status = 'active' | Static blue | `#kpi-journalists` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/press-releases/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **All Releases** — Master list of all press releases
2. **Drafts & Pending** — Releases in Draft / Review / Needs Revision states
3. **Media List** — Journalist contacts, publications, beats
4. **Publication Tracking** — Which release appeared where

### 5.2 Tab 1: All Releases

**Filter bar:** Season · Status (Draft/Review/Approved/Published/Archived) · Language (Telugu/English/Hindi) · Category (Topper Results/Event/Milestone/General) · Date range · Created by

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Title | Text (link) | Yes | Click → detail drawer |
| Category | Badge | Yes | Topper Results / Felicitation Event / New Branch / Exam Results / Award / Milestone / General |
| Language | Badge set | No | 🟢 TE · 🟢 EN · ⚪ HI — shows which language versions exist |
| Target Date | Date | Yes | Intended release date |
| Created | Date | Yes | Draft creation date |
| Author | Text | Yes | Campaign Manager / Topper Relations Manager |
| Approval | Badge | Yes | Draft (grey) / In Review (amber) / Approved (green) / Rejected (red) |
| Distribution | Badge | Yes | Not Sent / Sent ([N] contacts) / Partially Sent |
| Pickups | Integer | Yes | Number of publications that ran the story |
| Status | Badge | Yes | Draft / Review / Approved / Published / Archived |
| Actions | Buttons | No | [View] [Edit] [Submit for Review] [Distribute] |

**Default sort:** Target Date DESC (most recent first)
**Pagination:** Server-side · 25/page

### 5.3 Tab 2: Drafts & Pending

Same table structure as Tab 1, filtered to status IN ('draft', 'review', 'revision_needed'). Highlights overdue items (target date in the past, still not approved) with a red left-border.

**Workflow status flow:**
```
DRAFT → IN_REVIEW → APPROVED → PUBLISHED → ARCHIVED
                  ↘ REVISION_NEEDED → DRAFT (re-edit)
                  ↘ REJECTED (with reason)
```

### 5.4 Tab 3: Media List

Centralised journalist and publication contact directory.

**Filter bar:** Publication · Beat (Education/General/City/State) · Language · Medium (Print/TV/Digital/Wire Agency) · City · Status (Active/Inactive)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Journalist Name | Text (link) | Yes | Click → contact drawer |
| Publication | Text | Yes | Eenadu / Sakshi / Deccan Chronicle / Times of India / The Hindu / TV9 / etc. |
| Beat | Badge | Yes | Education / City / State / General / Business |
| Medium | Badge | Yes | Print / TV / Digital / Wire Agency |
| Language | Badge | Yes | Telugu / English / Hindi / Multi |
| City | Text | Yes | Hyderabad / Vijayawada / Visakhapatnam / Delhi / etc. |
| Designation | Text | No | Reporter / Sub-editor / Bureau Chief / Editor |
| Phone | Text | No | WhatsApp-enabled indicator |
| Email | Text | No | — |
| Last Contacted | Date | Yes | Most recent release sent |
| Pickup Rate | Percentage | Yes | (Releases picked up / Releases sent) × 100 |
| Status | Badge | Yes | Active (green) / Inactive (grey) / Bounced (red) |
| Actions | Buttons | No | [View] [Edit] [Send Release] |

**Default sort:** Publication ASC, then Journalist Name ASC
**Pagination:** Server-side · 50/page

### 5.5 Tab 4: Publication Tracking

Track whether press releases actually appeared in target publications.

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Release Title | Text | Yes | Press release name |
| Publication | Text | Yes | Where it appeared |
| Date Appeared | Date | Yes | Publication date |
| Page / Section | Text | No | "Page 3, City Edition" or "Education Supplement Page 1" |
| Size | Badge | No | Full Story / Brief Mention / Headline Only / Photo Only |
| Clipping | Thumbnail | No | Uploaded scan/screenshot (links to O-33 Media Mention Tracker) |
| Online URL | Link | No | If digital publication |
| Sentiment | Badge | Yes | Positive / Neutral / Negative |
| Notes | Text | No | — |

**Default sort:** Date Appeared DESC

---

## 6. Drawers & Modals

### 6.1 Modal: `new-release` (720px)

- **Title:** "Create Press Release"
- **Fields:**
  - **Release metadata:**
    - Title (text, required — e.g., "Sunrise Group Students Shine in TSBIE 2026 Results")
    - Category (dropdown, required): Topper Results / Felicitation Event / New Branch Launch / Exam Results / Award Recognition / Milestone Achievement / General Announcement
    - Target release date (date, required)
    - Target audience (multi-select): Print Media / TV Channels / Digital Publications / Wire Agencies / Internal
    - Priority (dropdown): Urgent (same-day) / Normal (2-day) / Planned (advance scheduling)
    - Related event (dropdown — link to O-29 felicitation event, optional)
    - Related toppers (multi-select from O-28 Topper Database, optional — auto-populates topper stats)
  - **Content (per language tab — Telugu / English / Hindi):**
    - Headline (text, required for at least one language)
    - Sub-headline (text, optional)
    - Body (rich text editor — supports bold, italic, bullet lists, tables)
    - Quotes section:
      - Chairman/CEO quote (textarea, optional)
      - Principal quote (textarea, optional)
      - Student/Parent quote (textarea, optional)
    - Boilerplate (auto-filled from group settings — "About Sunrise Education Group…")
    - Contact for media queries (auto-filled — Campaign Manager name, phone, email)
  - **Attachments:**
    - Media kit (upload — ZIP/PDF with high-res logos, photos, fact sheet)
    - Topper photos (auto-pulled from O-28 if toppers linked)
    - Supporting documents (marksheets, certificates, event photos)
  - **Distribution list:**
    - Select journalist groups (multi-select): All Education Beat / Telugu Media / English Media / Hindi Media / TV Channels / Custom List
    - Exclude specific contacts (multi-select, optional)
- **Buttons:** Cancel · Save as Draft · Submit for Review
- **Access:** Role 119, 120, or G4+

### 6.2 Modal: `template-selector` (560px)

- **Title:** "Press Release Templates"
- **Templates available:**
  - **Board Results Template** — Pre-filled structure: headline with board name, aggregate stats table (appeared/passed/≥90%/≥95%/centum), branch-wise top 3, Chairman quote placeholder, boilerplate
  - **JEE/NEET Results Template** — Structure: headline with exam name, total qualified, top ranks, subject-wise highlights, branch comparison
  - **Felicitation Event Template** — Structure: event date/venue, chief guest, number of awardees, event schedule highlights, RSVP details
  - **New Branch Launch Template** — Structure: location, facilities, courses offered, admission dates, inaugural event details
  - **General Announcement Template** — Flexible structure: headline, body, quote, boilerplate
- **Action:** Select template → Pre-populates `new-release` modal fields
- **Access:** Role 119, 120, 131

### 6.3 Modal: `approval-review` (640px, G4/G5 only)

- **Title:** "Review Press Release — [Title]"
- **Content preview:** Rendered press release in all available languages (tabbed)
- **Checklist (mandatory before approval):**
  - ☐ All student marks/ranks verified against O-28 Topper Database
  - ☐ No ASCI-violating claims ("No. 1", "Best", "Top" without substantiation)
  - ☐ Chairman/CEO quote approved
  - ☐ Contact details correct
  - ☐ Boilerplate current
  - ☐ Media kit attached
- **Actions:** Approve ✅ / Request Revision (with comments) / Reject ❌ (with reason)
- **Note:** Approval triggers notification to role 119 for distribution
- **Access:** G4/G5 only

### 6.4 Modal: `distribute-release` (560px)

- **Title:** "Distribute — [Release Title]"
- **Pre-condition:** Status must be 'approved'
- **Distribution channels:**
  - Email (select journalist groups → preview recipient count)
  - WhatsApp (select contacts with WhatsApp — sends PDF + key stats message)
  - Manual (mark as "handed to agency" for groups using external PR agencies)
- **Scheduling:** Send now / Schedule for [date + time]
- **Preview:** Email preview with subject line, body, attachments
- **Buttons:** Cancel · Send Now · Schedule
- **Access:** Role 119 only (post-approval)

### 6.5 Drawer: `release-detail` (720px, right-slide)

- **Tabs:** Content · Languages · Distribution · Tracking · History
- **Content tab:** Full rendered press release (primary language), metadata, linked toppers, linked event
- **Languages tab:** Side-by-side comparison of Telugu / English / Hindi versions; word count per version; translation status (Complete/Partial/Not Started)
- **Distribution tab:** Sent to [N] journalists on [date]; delivery status per contact (Sent/Delivered/Opened/Bounced)
- **Tracking tab:** Publications that picked up the release (linked to Tab 4 data); total media pickups; estimated media value
- **History tab:** Audit trail — created, edited, submitted, approved/rejected, distributed, with timestamps and actor names
- **Footer:** [Edit] [Submit for Review] [Distribute] [Track Pickup] [Archive] [Duplicate]

### 6.6 Drawer: `journalist-detail` (560px, right-slide)

- **Sections:**
  - Contact details (name, publication, designation, phone, email, WhatsApp, address)
  - Beat & coverage areas
  - Relationship notes (how contact was established, preferences — "prefers WhatsApp over email", "needs Telugu copy")
  - Release history: list of releases sent to this journalist with pickup status
  - Pickup rate: X% (N picked up / M sent)
- **Footer:** [Edit] [Send Release] [Deactivate]

### 6.7 Modal: `add-journalist` (480px)

- **Title:** "Add Journalist Contact"
- **Fields:**
  - Name (text, required)
  - Publication (dropdown from publication master or free text, required)
  - Medium (dropdown): Print / TV / Digital / Wire Agency
  - Beat (dropdown): Education / City / State / General / Business
  - Language (dropdown): Telugu / English / Hindi / Multi
  - City (text, required)
  - Designation (text)
  - Phone (text — with WhatsApp toggle)
  - Email (email)
  - Preferred channel (dropdown): Email / WhatsApp / Both
  - Notes (textarea)
- **Buttons:** Cancel · Save
- **Access:** Role 119 or G4+

### 6.8 Modal: `log-pickup` (480px)

- **Title:** "Log Publication Pickup — [Release Title]"
- **Fields:**
  - Publication (dropdown from media list + free text)
  - Date appeared (date, required)
  - Page / Section (text — "Page 3, City Edition")
  - Coverage size (dropdown): Full Story / Brief Mention / Headline Only / Photo Only
  - Online URL (URL, optional)
  - Clipping upload (file — JPEG/PNG/PDF, max 10 MB)
  - Sentiment (dropdown): Positive / Neutral / Negative
  - Notes (textarea)
- **Buttons:** Cancel · Save Pickup
- **Access:** Role 119, 131, or G4+

---

## 7. Charts

### 7.1 Releases by Category (Doughnut)

| Property | Value |
|---|---|
| Chart type | Doughnut (Chart.js 4.x) |
| Title | "Press Releases by Category — Current Season" |
| Data | COUNT per category (Topper Results, Event, Branch Launch, etc.) |
| Colour | Category-specific palette |
| Tooltip | "[Category]: [N] releases ([X]%)" |
| API | `GET /api/v1/group/{id}/marketing/press-releases/analytics/by-category/` |

### 7.2 Monthly Release & Pickup Trend (Dual Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Monthly: Releases Sent vs Media Pickups" |
| Data | Per month: count published, count pickups |
| Colour | Blue = sent, Green = picked up |
| Tooltip | "[Month]: [X] sent, [Y] picked up ([Z]% pickup rate)" |
| API | `GET /api/v1/group/{id}/marketing/press-releases/analytics/monthly-trend/` |

### 7.3 Pickup Rate by Publication (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Pickup Rate by Publication" |
| Data | Pickup % per publication (releases picked up / releases sent × 100) |
| Colour | Green ≥ 60%, Amber 30–59%, Red < 30% |
| API | `GET /api/v1/group/{id}/marketing/press-releases/analytics/pickup-by-publication/` |

### 7.4 Language Distribution (Stacked Bar)

| Property | Value |
|---|---|
| Chart type | Stacked bar |
| Title | "Releases by Language Availability" |
| Data | Per month: count with Telugu / English / Hindi versions |
| Colour | Telugu `#FF6B35`, English `#1E40AF`, Hindi `#10B981` |
| Purpose | Ensure all releases have multi-language coverage |
| API | `GET /api/v1/group/{id}/marketing/press-releases/analytics/by-language/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Release created | "Press release '[Title]' saved as draft" | Success | 3s |
| Submitted for review | "Release '[Title]' submitted for G4 approval" | Success | 3s |
| Approved | "Release '[Title]' approved — ready for distribution" | Success | 4s |
| Revision requested | "Release '[Title]' needs revision — see comments" | Warning | 5s |
| Rejected | "Release '[Title]' rejected by [Approver] — [Reason]" | Error | 5s |
| Distributed | "Release '[Title]' sent to [N] journalist contacts" | Success | 4s |
| Pickup logged | "Publication pickup logged — [Publication] on [Date]" | Success | 3s |
| Journalist added | "Journalist '[Name]' added to [Publication] media list" | Success | 3s |
| Distribution scheduled | "Release scheduled for distribution on [Date] at [Time]" | Info | 4s |
| Template applied | "Template '[Name]' applied — fill in details" | Info | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No releases this season | 📰 | "No Press Releases Yet" | "Create your first press release to announce topper results or events to media." | New Release |
| No journalist contacts | 📇 | "Media List Empty" | "Add journalist contacts to distribute press releases effectively." | Add Journalist |
| No pickups tracked | 📋 | "No Publication Pickups" | "Log media pickups to track which publications covered your releases." | Log Pickup |
| No approved releases | ⏳ | "Nothing Ready to Distribute" | "All releases are in draft or awaiting approval. Submit drafts for G4 review." | View Drafts |
| No releases for filter | 🔍 | "No Matching Releases" | "Adjust filters to find press releases." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + filter bar + table skeleton (12 rows) |
| Tab switch | Content skeleton |
| Release detail drawer | 720px skeleton: tabs + content placeholder |
| New release modal | Form skeleton with language tabs |
| Distribution sending | Spinner: "Sending to [N] contacts…" with progress bar |
| Approval review modal | Content preview shimmer + checklist skeleton |
| Media list load | Table skeleton (25 rows) |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/press-releases/` | G1+ | List releases (paginated, filterable) |
| GET | `/api/v1/group/{id}/marketing/press-releases/{release_id}/` | G1+ | Release detail |
| POST | `/api/v1/group/{id}/marketing/press-releases/` | G3+ | Create release |
| PUT | `/api/v1/group/{id}/marketing/press-releases/{release_id}/` | G3+ | Update release |
| DELETE | `/api/v1/group/{id}/marketing/press-releases/{release_id}/` | G4+ | Delete release |
| PATCH | `/api/v1/group/{id}/marketing/press-releases/{release_id}/submit/` | G3+ | Submit for review |
| PATCH | `/api/v1/group/{id}/marketing/press-releases/{release_id}/approve/` | G4+ | Approve release |
| PATCH | `/api/v1/group/{id}/marketing/press-releases/{release_id}/reject/` | G4+ | Reject release |
| PATCH | `/api/v1/group/{id}/marketing/press-releases/{release_id}/revise/` | G4+ | Request revision |
| POST | `/api/v1/group/{id}/marketing/press-releases/{release_id}/distribute/` | G3+ | Distribute to media list |
| POST | `/api/v1/group/{id}/marketing/press-releases/{release_id}/pickups/` | G2+ | Log publication pickup |
| GET | `/api/v1/group/{id}/marketing/press-releases/{release_id}/pickups/` | G1+ | List pickups for release |
| GET | `/api/v1/group/{id}/marketing/press-releases/journalists/` | G1+ | List journalist contacts |
| POST | `/api/v1/group/{id}/marketing/press-releases/journalists/` | G3+ | Add journalist |
| PUT | `/api/v1/group/{id}/marketing/press-releases/journalists/{journalist_id}/` | G3+ | Update journalist |
| DELETE | `/api/v1/group/{id}/marketing/press-releases/journalists/{journalist_id}/` | G3+ | Remove journalist |
| GET | `/api/v1/group/{id}/marketing/press-releases/templates/` | G1+ | List templates |
| GET | `/api/v1/group/{id}/marketing/press-releases/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/press-releases/analytics/by-category/` | G1+ | Category doughnut |
| GET | `/api/v1/group/{id}/marketing/press-releases/analytics/monthly-trend/` | G1+ | Monthly trend chart |
| GET | `/api/v1/group/{id}/marketing/press-releases/analytics/pickup-by-publication/` | G1+ | Pickup rate chart |
| GET | `/api/v1/group/{id}/marketing/press-releases/analytics/by-language/` | G1+ | Language distribution |
| POST | `/api/v1/group/{id}/marketing/press-releases/export/` | G1+ | Export report |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../press-releases/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#releases-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Dropdowns | `hx-get` with params | `#releases-table-body` | `innerHTML` | `hx-trigger="change"` |
| Release detail drawer | Row click | `hx-get=".../press-releases/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create release | Form submit | `hx-post=".../press-releases/"` | `#create-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Submit for review | Button click | `hx-patch=".../press-releases/{id}/submit/"` | `#status-badge-{id}` | `innerHTML` | Inline badge update |
| Approve release | Approval form | `hx-patch=".../press-releases/{id}/approve/"` | `#approval-result` | `innerHTML` | Toast + badge update |
| Distribute | Distribution form | `hx-post=".../press-releases/{id}/distribute/"` | `#distribute-result` | `innerHTML` | Progress indicator |
| Log pickup | Pickup form | `hx-post=".../press-releases/{id}/pickups/"` | `#pickup-list` | `beforeend` | Appends to tracking list |
| Journalist CRUD | Form submit | `hx-post / hx-put` | `#journalist-table-body` | `innerHTML` | Table refresh |
| Media list load | Media List tab | `hx-get=".../press-releases/journalists/"` | `#media-list-content` | `innerHTML` | `hx-trigger="click"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#releases-table-body` | `innerHTML` | 25/page |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
