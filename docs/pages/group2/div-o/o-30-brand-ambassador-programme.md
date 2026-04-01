# O-30 — Brand Ambassador Programme

> **URL:** `/group/marketing/topper-relations/ambassadors/`
> **File:** `o-30-brand-ambassador-programme.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Topper Relations Manager (Role 120, G3) — primary operator

---

## 1. Purpose

The Brand Ambassador Programme page manages the structured engagement of toppers as the public face of the education group — their photos in newspaper ads, their video testimonials on YouTube, their school visit speeches, and their social media endorsements. In the Indian coaching and school chain market, a single topper who cracked IIT Bombay or AIIMS Delhi and says on camera "I owe my success to Sunrise Academy" is worth more than Rs.50 lakh in paid advertising. Parents trust other students far more than any institutional brochure. When Narayana or Sri Chaitanya publishes full-page newspaper ads with 300 topper photos, the implicit message to every parent in the state is: "Your child could be next." Groups like FIITJEE, Allen Career Institute, and Resonance formally sign toppers as brand ambassadors — they appear at felicitation events, open days, in newspaper ads, and WhatsApp campaigns. In return, they receive: scholarships for higher studies (Rs.25,000–Rs.5,00,000), cash rewards, laptops/tablets, and coaching fee waivers for siblings.

The problems this page solves:

1. **Informal, untracked ambassador relationships:** Most groups have informal arrangements with toppers — "Come for our admission event, we'll give you Rs.10,000." There is no contract, no tracking, no exclusivity, and the topper does the same for a competitor the next week. This page formalises the relationship: written agreement (with mandatory parent/guardian consent for minors under 18 per Indian Majority Act 1875), defined activity commitments, incentive structure, exclusivity clause, and tenure. For minors — which most Class 12 toppers are at 17 — the contract must be co-signed by a parent/guardian, and photo/video usage consent must comply with POCSO-adjacent data protection norms.

2. **Ambassador tier management:** Not all ambassadors are equal in marketing value. A state rank 1 or JEE Advanced AIR under 100 commands front-page newspaper ads and TV interviews; a school topper with 92% is valuable for branch-level flex banners and WhatsApp campaigns. The system manages three tiers — **Platinum** (state/national rank holders), **Gold** (district toppers or 95%+), **Silver** (school/branch toppers or 90%+) — each with different incentive packages, activity commitments, and content usage rights.

3. **Activity assignment and tracking:** An ambassador might be assigned 8 activities over 12 months — 2 newspaper ad photo shoots, 1 video testimonial, 2 school visit speeches, 1 social media post series, 1 admission event appearance, and 1 parent counselling session. Without tracking, 3 activities never happen, the marketing team does not follow up, and the group gets half the value from the ambassador investment.

4. **Incentive and payment management:** Ambassadors receive compensation — scholarships for their next degree, cash stipends (Rs.5,000–Rs.50,000 per activity), laptops, tablets, or tuition fee waivers for siblings. These incentives must be budgeted, approved, tracked, and linked to completed activities. The CFO needs to know the total ambassador programme cost. TDS applies on cash disbursements above Rs.20,000 under Section 194R (benefit/perquisite to business associate) — the system must flag TDS liability.

5. **Contract lifecycle management:** Ambassador agreements typically run 12–24 months. They cover: what the ambassador will do, what the group provides, exclusivity (cannot appear in competitor ads), photo/video usage rights, social media guidelines, and termination clauses. For Platinum ambassadors — whose faces appear on hoardings across the state — exclusivity is non-negotiable and breach triggers contract termination. The system tracks contract start/end, renewal reminders, and compliance.

6. **Campaign integration:** When the admissions team (O-08) builds a newspaper ad campaign, they need to pull ambassador photos and quotes. When the WhatsApp team (O-12) sends result season broadcasts, they need ambassador video clips. The ambassador database must be searchable by tier, exam type, rank, branch, and availability — and integrated with campaign tools.

7. **Alumni engagement:** Ambassadors do not stop being valuable after their contract ends. A student who was a JEE topper and is now a 3rd-year B.Tech at IIT Bombay is even more powerful — "I joined Sunrise in Class 8, cracked JEE in Class 12, and now I'm at IIT Bombay." The system tracks long-term alumni ambassador relationships, periodic engagement check-ins, and career milestone updates that feed into success stories (O-31).

**Scale:** 10–100 ambassadors/group per season · 3 tiers (Platinum 5–15, Gold 20–40, Silver 30–60) · 3–12 activities per ambassador/year · Rs.50,000–Rs.5,00,000 total programme budget per season · 1–2 year contract tenure · 5–15 active campaigns using ambassador content · Linked to O-28 (Topper Database), O-29 (Felicitation Events), O-31 (Success Stories), O-08 (Campaign Builder)

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Topper Relations Manager | 120 | G3 | Full CRUD — onboard ambassadors, assign activities, manage contracts, track incentives, manage tiers | Primary operator |
| Group Admissions Campaign Manager | 119 | G3 | Read + Use — browse ambassadors for campaign assignment, request ambassador activities | Uses ambassador content in campaigns |
| Group Campaign Content Coordinator | 131 | G2 | Read + Download — access ambassador photos/videos/testimonials for creative design | Creates campaign creatives using ambassador assets |
| Group Admission Data Analyst | 132 | G1 | Read — ambassador programme analytics, ROI per ambassador, tier performance | Reporting and MIS |
| Group Admission Telecaller Executive | 130 | G3 | Read (limited) — view ambassador names and achievements for telecalling scripts | References ambassadors during prospect calls |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve Platinum contracts, high-value incentives (>Rs.25,000), exclusivity terms | Financial and brand authority |
| Branch Principal | — | G3 | Read (own branch ambassadors) — coordinate school visits and local events | Supports local ambassador activities |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Ambassador onboarding/editing: role 120 or G4+. Platinum tier assignment: G4/G5 approval required. Contract approval: G4/G5 for contracts > Rs.50,000 total value. Incentive disbursement approval: G4+ for amounts > Rs.25,000. Campaign usage: role 119 or 131.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Topper Relations  >  Brand Ambassador Programme
```

### 3.2 Page Header
```
Brand Ambassador Programme                           [+ Enrol Ambassador]  [Activity Planner]  [Export]
Topper Relations Manager — Lakshmi Naidu
Sunrise Education Group · Season 2025-26 · 24 active ambassadors (4 Platinum · 8 Gold · 12 Silver) · 86 activities assigned · 62 completed · Rs.8.4L incentives disbursed
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Ambassadors | Integer | COUNT WHERE status IN ('active','prospect') AND season = current | Static blue | `#kpi-total` |
| 2 | Active This Season | Integer | COUNT WHERE contract_status = 'active' AND season = current | Static green | `#kpi-active` |
| 3 | Campaigns Assigned | Integer | COUNT(DISTINCT campaign_id) WHERE ambassador_activities.campaign_id IS NOT NULL AND season = current | Static blue | `#kpi-campaigns` |
| 4 | Incentives Disbursed (Rs.) | Currency | SUM(disbursed_amount) WHERE season = current | Green >= Rs.1L, Static blue otherwise | `#kpi-incentives` |
| 5 | Pending Disbursements | Currency | SUM(amount) WHERE incentive_status IN ('approved','pending_approval') AND disbursement_date IS NULL | Red > Rs.1L, Amber Rs.25K–Rs.1L, Green < Rs.25K | `#kpi-pending` |
| 6 | Avg Inquiry Attribution | Float (per ambassador) | AVG(attributed_enquiries) WHERE contract_status = 'active' this season | Green >= 50, Amber 20–49, Red < 20 | `#kpi-attribution` |

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Ambassador Directory** — Searchable list of all ambassadors with tier, status, and key metrics
2. **Activity Tracker** — All assigned activities with status, timelines, and deliverables
3. **Contracts & Incentives** — Contract lifecycle, incentive ledger, payment tracking
4. **Content Library** — Photos, videos, testimonials per ambassador
5. **Programme Analytics** — ROI, tier performance, campaign impact, engagement timeline

### 5.2 Tab 1: Ambassador Directory

**Filter bar:** Tier (Platinum/Gold/Silver/All) · Status (Active/Prospect/Alumni/Expired/Terminated) · Branch · Exam Type (Board/JEE/NEET/CLAT/CUET) · Year of Topping · Availability · Contract Status · Exclusivity (Exclusive/Non-exclusive)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Photo | Thumbnail (50x50) | No | Ambassador photo from O-28 or uploaded |
| Name | Text (link) | Yes | Click opens ambassador detail drawer |
| Tier | Badge | Yes | Platinum (purple) / Gold (amber) / Silver (grey-blue) |
| Achievement | Text | Yes | "JEE Adv AIR 567" or "TSBIE 99.2% — State 3rd" |
| Branch | Text | Yes | Branch where they studied |
| Current Status | Text | Yes | "B.Tech CSE, IIT Bombay" or "MBBS 2nd Year, AIIMS Delhi" |
| Contract Period | Date range | Yes | Start to End — e.g., "Apr 2025 – Mar 2027" |
| Contract Status | Badge | Yes | Active / Expiring Soon / Expired / Prospect / Terminated |
| Activities | N/M | Yes | Completed / Assigned — e.g., "5/8" |
| Incentives Paid | Rs. Amount | Yes | Total paid to date |
| Exclusivity | Badge | No | Exclusive / Non-exclusive |
| Attributed Enquiries | Integer | Yes | Enquiries attributed to this ambassador's content |
| Last Activity | Date | Yes | Date of most recent completed activity |
| Actions | Buttons | No | [View] [Assign Activity] [Renew] [Deactivate] |

**Default sort:** Tier (Platinum first), then Achievement rank ASC
**Pagination:** Server-side, 25/page

### 5.3 Tab 2: Activity Tracker

**Filter bar:** Ambassador · Tier · Activity Type · Status (Assigned/In Progress/Completed/Overdue/Cancelled) · Due Date Range · Campaign Link

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Ambassador | Text (link) | Yes | Name + tier badge |
| Activity Type | Badge | Yes | Newspaper Ad / Video Testimonial / School Visit / Social Media Post / Admission Event / Parent Counselling / Photo Shoot / Press Interview |
| Description | Text | No | Brief — "Appear in Eenadu full-page JEE results ad" |
| Campaign | Text (link) | Yes | Linked campaign from O-08 (if applicable) |
| Branch/Location | Text | Yes | Where the activity takes place |
| Assigned Date | Date | Yes | When activity was assigned |
| Due Date | Date | Yes | Deadline for completion |
| Status | Badge | Yes | Assigned (blue) / In Progress (amber) / Completed (green) / Overdue (red) / Cancelled (grey) |
| Deliverable | Badge | No | Submitted / Pending — photo/video/attendance proof |
| Incentive | Rs. Amount | No | Per-activity incentive amount |
| Payment | Badge | Yes | Not Due / Pending / Paid |
| Actions | Buttons | No | [View] [Mark Complete] [Reschedule] [Cancel] |

**Default sort:** Due Date ASC (nearest due first)
**Pagination:** Server-side, 30/page

### 5.4 Tab 3: Contracts & Incentives

**Sub-tabs:**
- **Contracts:** List of all ambassador contracts with tier-based SLA
- **Incentive Ledger:** Payment history across all ambassadors

#### 5.4.1 Contracts Table

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Ambassador | Text | Yes | Name with tier badge |
| Contract ID | Text | Yes | Auto-generated — AMB-2026-001 |
| Tier | Badge | Yes | Platinum / Gold / Silver |
| Start Date | Date | Yes | Contract commencement |
| End Date | Date | Yes | Contract expiry |
| Total Value | Rs. Amount | Yes | Total incentive commitment over contract period |
| Paid to Date | Rs. Amount | Yes | Cumulative disbursed |
| Balance | Rs. Amount | Yes | Total Value minus Paid to Date |
| Activities Committed | Integer | Yes | Total activities promised in contract |
| Completed | Integer | Yes | Activities completed so far |
| Exclusivity | Badge | No | Exclusive / Non-exclusive |
| Parent Consent | Badge | No | Obtained / Pending / N/A (adult) |
| Status | Badge | Yes | Draft / Pending Approval / Active / Expiring / Expired / Terminated / Renewed |
| Actions | Buttons | No | [View] [Renew] [Terminate] [Download PDF] |

**Tier-based contract defaults:**

| Parameter | Platinum | Gold | Silver |
|---|---|---|---|
| Typical tenure | 24 months | 18 months | 12 months |
| Min activities/year | 8–12 | 5–8 | 3–5 |
| Exclusivity | Mandatory | Recommended | Optional |
| Total budget range | Rs.2,00,000–Rs.5,00,000 | Rs.50,000–Rs.2,00,000 | Rs.10,000–Rs.50,000 |
| Approval required | G5 (Chairman) | G4 (CEO) | G3 (Topper Relations Mgr) |
| Benefits package | Scholarship + cash + device + sibling waiver | Scholarship + cash + device | Cash + gift voucher |

#### 5.4.2 Incentive Ledger

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Ambassador | Text | Yes | Name with tier badge |
| Activity | Text | Yes | Linked completed activity |
| Incentive Type | Badge | Yes | Cash / Scholarship / Device (Laptop/Tablet) / Fee Waiver / Gift Voucher |
| Amount | Rs. Amount | Yes | Disbursement amount |
| TDS Applicable | Badge | No | Yes (if cash > Rs.20,000) / No — Sec 194R flag |
| Status | Badge | Yes | Approved / Pending Approval / Disbursed / On Hold / Rejected |
| Approved By | Text | No | G4/G5 approver name (for amounts > Rs.25,000) |
| Disbursement Date | Date | Yes | Actual payment date |
| Payment Mode | Badge | No | Bank Transfer (NEFT/IMPS) / UPI / Cheque / In-Kind Delivery |
| Receipt | Badge | No | Acknowledged / Pending |
| Actions | Buttons | No | [View] [Disburse] [Put on Hold] |

### 5.5 Tab 4: Content Library

**Filter bar:** Ambassador · Tier · Content Type (Photo/Video/Testimonial Quote/Social Media Post/Press Clipping) · Campaign · Date Range · Usage Status (Used in Campaign/Unused)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Thumbnail | Image (80x80) | No | Preview of photo/video frame |
| Ambassador | Text (link) | Yes | Name + tier badge |
| Content Type | Badge | Yes | Photo / Video / Testimonial Quote / Social Post Screenshot / Press Clipping |
| Description | Text | No | "Newspaper ad photo — JEE results 2026" |
| Campaign Used In | Text (link) | Yes | Which campaigns featured this content |
| Upload Date | Date | Yes | When uploaded to system |
| File Size | Text | No | e.g., "2.4 MB" |
| Consent Status | Badge | No | Photo consent / Video consent / Both |
| Usage Count | Integer | Yes | Number of campaigns this content appeared in |
| Actions | Buttons | No | [View] [Download] [Add to Campaign] [Archive] |

**Default sort:** Upload Date DESC (newest first)
**Pagination:** Server-side, 20/page (grid view available)

### 5.6 Tab 5: Programme Analytics

Charts and summary tables (see Section 7). Key metrics:
- Total programme cost vs attributed admission revenue (ROI calculation)
- Activity completion rate by type and tier
- Ambassador-featured campaigns vs non-featured: conversion rate comparison
- Top-performing ambassadors by attributed enquiry count
- Tier-wise budget utilisation
- Engagement timeline showing ambassador activity over months

---

## 6. Drawers & Modals

### 6.1 Modal: `enrol-ambassador` (720px)

- **Title:** "Enrol Brand Ambassador"
- **Source:** Auto-fill from O-28 topper database (primary) or manual entry (fallback)
- **Fields:**
  - **Ambassador details (auto-fill from O-28 if selected):**
    - Search O-28 topper database (typeahead — pulls name, photo, achievement, branch, marks)
    - Or manual entry:
      - Name (text, required)
      - Photo (upload, max 5 MB — JPEG/PNG)
      - Phone (text, required — Indian mobile: 10-digit validation)
      - Email (text, optional)
      - WhatsApp number (text — primary contact channel in India)
      - Branch (dropdown — branch where they studied)
      - Achievement (text — "JEE Advanced AIR 567, 2025")
      - Board/Exam (dropdown: CBSE / ICSE / TSBIE / AP Board / JEE Main / JEE Adv / NEET / CLAT / CUET / Other)
      - Percentage / Rank (text)
      - Year of topping (dropdown: 2020–2026)
  - **Ambassador tier:**
    - Tier (dropdown, required): Platinum / Gold / Silver
    - Tier justification (auto-suggested based on achievement, editable):
      - Platinum: State rank 1–10, AIR under 100 (JEE/NEET), national-level recognition
      - Gold: District topper, 95%+ board score, AIR 100–1,000
      - Silver: School topper, 90%+ board score, AIR 1,000–10,000
  - **Current status:**
    - Current institution (text — "IIT Bombay")
    - Course (text — "B.Tech Computer Science")
    - City (text)
    - Year of study (dropdown — 1st / 2nd / 3rd / 4th / Completed)
  - **Contract details:**
    - Contract start date (date, required)
    - Contract end date (date, required — auto-suggested based on tier: Platinum 24mo, Gold 18mo, Silver 12mo)
    - Exclusivity (toggle — mandatory ON for Platinum; recommended for Gold; optional for Silver)
    - Total incentive budget (Rs., required — pre-filled with tier default range)
    - Incentive structure (repeating rows):
      - Activity type (dropdown)
      - Per-activity incentive (Rs.)
      - Incentive type: Cash / Scholarship Credit / Device / Gift Voucher / Fee Waiver
    - Additional benefits (textarea — e.g., "Laptop on completion of 6+ activities," "Sibling fee waiver for Class 11")
  - **Planned activities (pre-assign):**
    - Activity list (repeating rows, min count based on tier):
      - Activity type (dropdown)
      - Tentative date (date range)
      - Description (text)
      - Linked campaign (dropdown from O-08, optional)
  - **Legal:**
    - Upload signed agreement (PDF, optional — can be added later)
    - Photo/video usage consent (toggle, required)
    - Social media posting consent (toggle)
    - Parent/guardian consent (toggle — required if ambassador is under 18 years; system auto-checks DOB from O-28)
    - Parent/guardian name (text — required if minor)
    - Parent/guardian phone (text — required if minor)
  - **Notes:** Internal notes (textarea)
- **Validation:**
  - Platinum tier requires G4/G5 approval before activation
  - Minor ambassadors (under 18) must have parent consent toggled ON
  - At least one planned activity required
  - Exclusivity must be ON for Platinum (enforced)
- **Buttons:** Cancel | Save as Prospect | Submit for Approval
- **Access:** Role 120 or G4+

### 6.2 Drawer: `ambassador-detail` (720px, right-slide)

- **Tabs:** Profile | Activities | Contract | Incentives | Content | Engagement History
- **Profile tab:**
  - Photo (large, 200x200), name, tier badge (Platinum/Gold/Silver with colour)
  - Achievement headline (e.g., "JEE Advanced AIR 567, 2025")
  - Branch where they studied, current institution and course, city
  - Contact: phone, email, WhatsApp
  - Key stats row: Activities completed / Total | Campaigns featured in | Total earned (Rs.) | Attributed enquiries
  - Tier history (if upgraded/downgraded)
- **Activities tab:**
  - Timeline of all activities — assigned, in-progress, completed, overdue
  - Expandable cards with: activity type, description, linked campaign, deliverable status, incentive info
  - Overdue activities highlighted in red with days-overdue count
- **Contract tab:**
  - Contract summary card: ID, start/end, tier, total value, exclusivity, status
  - Signed agreement PDF viewer (inline preview)
  - Parent consent document (if minor)
  - Renewal history — previous contracts listed chronologically
  - Compliance flags: exclusivity breach alerts, contract approaching expiry
- **Incentives tab:**
  - Payment ledger for this ambassador — all disbursements with status
  - Summary: total committed, total disbursed, balance pending
  - TDS tracking: flagged entries where Sec 194R applies
  - Each row: activity linked, amount, type, mode, date, receipt status
- **Content tab:**
  - Gallery view: all photos, videos, testimonial quotes, social media screenshots, press clippings featuring this ambassador
  - Each item shows: thumbnail, description, campaigns used in, upload date
  - Video testimonials with inline playback
  - Download all as ZIP option
- **Engagement History tab:**
  - Full lifecycle log: onboarded date, tier assigned, activities assigned/completed, incentive payments, contract renewals, status changes
  - Alumni engagement notes: periodic check-in records, career milestone updates
  - Communication log: calls made, WhatsApp messages sent, emails
- **Footer:** [Edit] [Assign Activity] [Process Payment] [Renew Contract] [Change Tier] [Deactivate] [Download Agreement]

### 6.3 Modal: `assign-to-campaign` (560px)

- **Title:** "Assign to Campaign — [Ambassador Name]"
- **Fields:**
  - Activity type (dropdown, required):
    - **Newspaper Ad Appearance** — Photo in full-page/half-page result ad (Eenadu, Sakshi, The Hindu, Deccan Chronicle)
    - **Video Testimonial** — 2–5 min recorded testimonial (studio or campus)
    - **School Visit Speech** — Visit a branch, address students and parents (1–2 hours)
    - **Social Media Post** — Ambassador posts about their experience on Instagram/YouTube/LinkedIn
    - **Admission Event Appearance** — Attend open day, parent meet, or counselling session
    - **Parent Counselling** — One-on-one or group session with prospective parents
    - **Photo Shoot** — Studio session for new campaign creatives
    - **Press Interview** — Media interaction for newspaper/TV coverage
  - Linked campaign (dropdown from O-08, optional but recommended)
  - Description (textarea — specific details: "Appear in Eenadu full-page JEE results ad, page 3")
  - Branch/location (dropdown — for school visits and events)
  - Scheduled date (date, required)
  - Due date for deliverable (date)
  - Incentive for this activity (Rs. — pre-filled from contract per-activity rate, editable)
  - Briefing notes (textarea — key messages, talking points, dos and don'ts)
  - Deliverable expected (dropdown): Photo / Video File / Attendance Proof / Social Media Link / Press Clipping / None
- **Validation:**
  - Cannot assign if contract_status != 'active'
  - Cannot exceed committed activity count in contract without approval
  - Scheduled date must be within contract period
- **Buttons:** Cancel | Assign Activity
- **Access:** Role 120 or G4+

### 6.4 Modal: `record-incentive-disbursement` (480px)

- **Title:** "Record Incentive Disbursement — [Ambassador Name]"
- **Fields:**
  - Activity (dropdown — completed activities with pending payment, required)
  - Incentive type (dropdown, required): Cash / Scholarship Credit / Device (Laptop/Tablet) / Gift Voucher / Fee Waiver
  - Amount (Rs., pre-filled from activity rate, editable)
  - TDS flag (auto-calculated: "TDS applicable under Sec 194R — Rs.[amount]" if cash > Rs.20,000)
  - Payment mode (dropdown): Bank Transfer (NEFT/IMPS) / UPI / Cheque / In-Kind Delivery
  - Bank details (if Bank Transfer): Account holder, Account number, IFSC, Bank name (saved from ambassador profile)
  - UPI ID (if UPI mode selected)
  - Reference number (text — UTR/transaction ID after payment)
  - Receipt upload (file — ambassador signed acknowledgement)
  - Notes (textarea)
- **Approval workflow:**
  - Amount <= Rs.25,000: Role 120 can disburse directly
  - Amount > Rs.25,000: Requires G4 approval before disbursement
  - Platinum ambassador: All disbursements require G4 sign-off regardless of amount
- **Buttons:** Cancel | Submit for Approval | Disburse (if pre-approved or within limit)
- **Access:** Role 120 (submit), G4+ (approve and disburse)

### 6.5 Modal: `content-upload` (560px)

- **Title:** "Upload Ambassador Content — [Ambassador Name]"
- **Fields:**
  - Content type (dropdown, required): Photo / Video / Testimonial Quote / Social Media Screenshot / Press Clipping
  - Files (drag-and-drop zone — JPEG/PNG/MP4/PDF, max 20 MB per file, max 50 files per batch)
  - Description (text — "Photo shoot for Deccan Chronicle JEE results ad, May 2026")
  - Linked activity (dropdown — optional: ties content to a specific activity)
  - Linked campaign (dropdown from O-08 — optional)
  - Content consent verified? (toggle — must confirm ambassador has consented to this content usage)
  - Tags (multi-select): Newspaper Ad / Video / Social Media / Website / Prospectus / Flex Banner / WhatsApp
  - Watermark (toggle — apply group logo watermark)
- **Post-upload:** Auto-sync to ambassador's content library; optionally push to O-03 (Material Library)
- **Buttons:** Cancel | Upload [N] Files
- **Access:** Role 120, 131, or G4+

### 6.6 Modal: `renew-contract` (480px)

- **Title:** "Renew Contract — [Ambassador Name]"
- **Shows:** Previous contract summary — tier, start/end, activities committed/completed, total value, total paid, exclusivity
- **Fields:**
  - New end date (date, required — pre-filled with tier default extension)
  - Revised tier (dropdown — may upgrade Silver to Gold if performance warrants)
  - Revised incentive budget (Rs.)
  - Revised activity plan (summary textarea)
  - Exclusivity renewal (toggle)
  - Updated agreement upload (PDF, optional)
- **Buttons:** Cancel | Renew Contract
- **Access:** Role 120 initiates; G4+ approval required for Platinum/Gold; G3 sufficient for Silver

---

## 7. Charts

### 7.1 Ambassador Tier Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Ambassador Tier Distribution — Season 2025-26" |
| Data | COUNT per tier: Platinum, Gold, Silver |
| Colour | Platinum = `#7C3AED` purple, Gold = `#EAB308` amber, Silver = `#64748B` slate |
| Centre text | Total: [N] ambassadors |
| API | `GET /api/v1/group/{id}/marketing/topper-relations/ambassadors/analytics/tier-distribution/` |

### 7.2 Campaign Participation by Ambassador (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Campaign Participation — Top 15 Ambassadors" |
| Data | Top 15 ambassadors by campaign count (completed activities linked to campaigns) |
| Colour | Per tier — Platinum = `#7C3AED`, Gold = `#EAB308`, Silver = `#64748B` |
| Tooltip | "[Name] ([Tier]): [N] campaigns, [M] activities" |
| API | `GET /api/v1/group/{id}/marketing/topper-relations/ambassadors/analytics/campaign-participation/` |

### 7.3 ROI per Ambassador (Scatter)

| Property | Value |
|---|---|
| Chart type | Scatter (Chart.js 4.x) |
| Title | "Ambassador ROI — Cost vs Attributed Enquiries" |
| Data | X = total incentive paid (Rs.), Y = attributed enquiries; one dot per active ambassador |
| Colour | Per tier — Platinum = `#7C3AED`, Gold = `#EAB308`, Silver = `#64748B` |
| Tooltip | "[Name]: Rs.[X] spent, [Y] enquiries attributed" |
| Quadrant lines | Median cost (vertical), median enquiries (horizontal) — to show high-ROI vs low-ROI ambassadors |
| Purpose | Identify which ambassadors deliver the best enquiry-per-rupee return |
| API | `GET /api/v1/group/{id}/marketing/topper-relations/ambassadors/analytics/roi-scatter/` |

### 7.4 Engagement Timeline (Line)

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "Ambassador Engagement Over Time — Last 12 Months" |
| Data | 3 lines — one per tier; Y = count of completed activities per month |
| Colour | Platinum = `#7C3AED`, Gold = `#EAB308`, Silver = `#64748B` |
| X-axis | Monthly (Apr 2025 – Mar 2026) |
| Y-axis | Activities completed |
| Purpose | Show seasonal engagement patterns — peak around results season (May–Jun) and admission season (Feb–Apr) |
| API | `GET /api/v1/group/{id}/marketing/topper-relations/ambassadors/analytics/engagement-timeline/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Ambassador enrolled | "Ambassador '[Name]' enrolled as [Tier] — [Achievement]" | Success | 3s |
| Contract approved | "Contract for '[Name]' ([Tier]) approved — active until [Date]" | Success | 4s |
| Activity assigned | "Activity '[Type]' assigned to '[Name]' — due [Date]" | Success | 3s |
| Activity completed | "Activity '[Type]' by '[Name]' marked complete" | Success | 3s |
| Incentive disbursed | "Rs.[Amount] disbursed to '[Name]' for '[Activity]'" | Success | 4s |
| Contract expiring | "Contract for '[Name]' ([Tier]) expires in [N] days — renew?" | Warning | 5s |
| Contract renewed | "Contract for '[Name]' renewed until [Date]" | Success | 3s |
| Activity overdue | "Activity '[Type]' for '[Name]' is overdue by [N] days" | Warning | 5s |
| Tier changed | "Ambassador '[Name]' tier changed from [Old] to [New]" | Info | 3s |
| Ambassador deactivated | "Ambassador '[Name]' deactivated" | Info | 3s |
| Exclusivity breach alert | "Warning: '[Name]' (Platinum) may have appeared in competitor material — verify immediately" | Warning | 6s |
| Content uploaded | "[N] files uploaded for '[Name]' — content library updated" | Success | 3s |
| TDS flag | "TDS applicable on Rs.[Amount] disbursement to '[Name]' under Sec 194R" | Info | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No ambassadors | Star | "No Brand Ambassadors" | "Enrol your first topper as a brand ambassador from the Topper Database (O-28)." | Enrol Ambassador |
| No active ambassadors | Person | "No Active Ambassadors" | "All ambassador contracts have expired. Renew existing or enrol new ambassadors for this season." | Enrol / Renew |
| No Platinum ambassadors | Trophy | "No Platinum Ambassadors" | "Enrol state/national rank holders as Platinum-tier ambassadors for maximum marketing impact." | Enrol Ambassador |
| No activities assigned | Clipboard | "No Activities Assigned" | "Assign activities to ambassadors — newspaper ads, video testimonials, school visits, social media posts." | Assign Activity |
| No content uploaded | Camera | "No Ambassador Content" | "Content will appear as ambassadors complete activities and photos/videos are uploaded." | Upload Content |
| No incentives pending | Wallet | "All Incentives Current" | "All ambassador incentives have been disbursed. No pending payments." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + ambassador table skeleton (15 rows) |
| Tab switch | Content area skeleton matching target tab layout |
| Ambassador detail drawer | 720px skeleton: photo placeholder + 6 tabs |
| Activity tracker table | Filter bar shimmer + table skeleton (20 rows) |
| Contract / incentive tables | Table skeleton (15 rows) with badge placeholders |
| Content library grid | 4x3 image placeholder grid |
| Enrol ambassador modal | Form skeleton with O-28 typeahead placeholder |
| Chart load | Grey canvas placeholder with chart-type outline |
| Incentive processing | Spinner: "Processing payment..." |
| Content upload | Progress bar per file + overall batch progress |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/` | G1+ | List all ambassadors (filterable by tier, status, branch, exam) |
| GET | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/` | G1+ | Ambassador detail with all tabs data |
| POST | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/` | G3+ | Enrol new ambassador (from O-28 or manual) |
| PUT | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/` | G3+ | Update ambassador profile |
| PATCH | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/status/` | G3+ | Activate / deactivate / terminate |
| PATCH | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/tier/` | G3+ | Change tier (Platinum requires G4+) |
| DELETE | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/` | G4+ | Delete ambassador record |
| GET | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/activities/` | G1+ | List all activities for ambassador |
| POST | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/activities/` | G3+ | Assign activity to ambassador |
| PATCH | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/activities/{act_id}/` | G3+ | Update activity status (complete/cancel/reschedule) |
| GET | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/contract/` | G1+ | Current and historical contracts |
| POST | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/contract/` | G3+ | Create or renew contract |
| PATCH | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/contract/approve/` | G4+ | Approve contract |
| GET | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/incentives/` | G1+ | Incentive ledger for ambassador |
| POST | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/incentives/` | G3+ | Submit incentive disbursement |
| PATCH | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/incentives/{inc_id}/disburse/` | G4+ | Approve and disburse incentive |
| GET | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/content/` | G1+ | Ambassador content gallery |
| POST | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/{amb_id}/content/` | G2+ | Upload ambassador content (photos/videos) |
| GET | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/kpis/` | G1+ | KPI summary bar data |
| GET | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/analytics/tier-distribution/` | G1+ | Tier donut chart data |
| GET | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/analytics/campaign-participation/` | G1+ | Campaign participation bar data |
| GET | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/analytics/roi-scatter/` | G1+ | ROI scatter plot data |
| GET | `/api/v1/group/{id}/marketing/topper-relations/ambassadors/analytics/engagement-timeline/` | G1+ | Monthly engagement line data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../ambassadors/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#ambassadors-content` | `innerHTML` | `hx-trigger="click"` |
| Ambassador detail drawer | Row click | `hx-get=".../ambassadors/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Enrol ambassador | Form submit | `hx-post=".../ambassadors/"` | `#enrol-result` | `innerHTML` | Toast + refresh directory |
| O-28 topper search | Typeahead input | `hx-get="/api/v1/group/{id}/marketing/topper-relations/database/?q={term}"` | `#topper-suggestions` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Assign activity | Form submit | `hx-post=".../ambassadors/{id}/activities/"` | `#activity-result` | `innerHTML` | Toast + refresh tracker |
| Activity status update | Status button | `hx-patch=".../ambassadors/{id}/activities/{aid}/"` | `#activity-badge-{aid}` | `innerHTML` | Inline badge swap |
| Process incentive | Form submit | `hx-post=".../ambassadors/{id}/incentives/"` | `#incentive-result` | `innerHTML` | Toast |
| Contract approval | Approve button | `hx-patch=".../ambassadors/{id}/contract/approve/"` | `#contract-status-{id}` | `innerHTML` | Inline badge swap |
| Tier change | Tier dropdown | `hx-patch=".../ambassadors/{id}/tier/"` | `#tier-badge-{id}` | `innerHTML` | Confirmation required for Platinum |
| Content upload | Drop zone submit | `hx-post=".../ambassadors/{id}/content/"` | `#content-grid` | `beforeend` | `hx-encoding="multipart/form-data"` |
| Filter apply | Dropdowns change | `hx-get` with filter params | `#ambassador-table-body` | `innerHTML` | `hx-trigger="change"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#ambassador-table-body` | `innerHTML` | 25/page |
| Chart load | Tab/page load | `hx-get=".../ambassadors/analytics/..."` | `#chart-{name}` | `innerHTML` | `hx-trigger="intersect once"` — lazy load on scroll |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
