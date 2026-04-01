# O-08 — Campaign Builder

> **URL:** `/group/marketing/campaigns/{campaign_id}/`
> **File:** `o-08-campaign-builder.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary builder/editor

---

## 1. Purpose

The Campaign Builder is the detailed configuration and execution management page for a single admission campaign. While the Calendar (O-07) gives the bird's-eye view of all campaigns across the season, this page is where the Campaign Manager drills into one specific campaign — configures its channels, assigns branches, sets daily budgets, defines target audiences, links creative materials, assigns telecalling follow-up rules, sets milestones, and monitors execution metrics once the campaign is live.

Every campaign in an Indian education group is multi-faceted. A "February Newspaper Blitz" campaign is not just newspaper ads — it involves:
- Selecting which Telugu/English dailies and which editions (Hyderabad city, Telangana state, Andhra Pradesh)
- Choosing ad sizes (quarter-page, half-page, full-page) and dates
- Coordinating WhatsApp follow-up blasts the same morning the newspaper ad appears
- Assigning telecallers to call leads who respond via the helpline number printed in the ad
- Tracking which branches' phone numbers ring, how many leads come in, and from which edition
- Linking to the creative artwork from the Material Library (O-03)
- Monitoring daily spend vs budget
- Pausing underperforming editions mid-campaign and reallocating budget

This page handles all of that in a single unified interface with tabs for configuration, execution tracking, and performance analytics.

**Scale:** 1 campaign at a time · 1–50 branches targeted · 1–5 channels per campaign · ₹50,000–₹1,00,00,000 per campaign · 7–90 day duration

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — configure, launch, pause, edit, close | Primary builder |
| Group Topper Relations Manager | 120 | G3 | Read only | Views topper-campaign linkages |
| Group Campaign Content Coordinator | 131 | G2 | Read + Link materials | Links creative assets from O-03 |
| Group Admission Telecaller Executive | 130 | G3 | Read — assigned actions only | Views own telecalling assignments |
| Group Admission Data Analyst | 132 | G1 | Read only | Views performance data |
| Group CEO | — | G4 | Read + Approve high-budget campaigns | Approves campaigns > ₹10L |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Edit restricted to role 119 or G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Campaign Planning  ›  [Campaign Name]
```

### 3.2 Page Header
```
February Newspaper Blitz                       [Edit]  [Pause ⏸]  [Clone]  [Close Campaign]
Status: Active · Day 14 of 30 · Phase 3 — Newspaper Blitz
Budget: ₹8,00,000 · Spent: ₹4,20,000 (52%) · Leads: 1,240 · Conversions: 86
Campaign Manager — Ramesh Venkataraman · Created: 01-Jan-2026
```

**Status bar:** Visual progress bar showing day X of Y with budget spend overlay.

### 3.3 Tab Navigation

5 main tabs:
1. **Configuration** — Campaign setup and targeting
2. **Channels** — Channel-specific configuration (newspaper editions, WhatsApp lists, etc.)
3. **Execution** — Live monitoring, daily logs, actions
4. **Performance** — Analytics, ROI, lead source attribution
5. **Materials** — Linked creative assets

---

## 4. Tab 1: Configuration

### 4.1 Basic Details

| Field | Type | Editable | Notes |
|---|---|---|---|
| Campaign Name | Text | Yes (draft/scheduled) | Max 120 chars |
| Description / Objective | Textarea | Yes | What this campaign aims to achieve |
| Campaign Type | Dropdown | Yes (draft only) | Admission Drive / Scholarship Promotion / Brand Awareness / Topper Showcase / Event Promotion / Referral Drive |
| Channel(s) | Multi-select badges | Yes | Newspaper / Digital / WhatsApp / SMS / Outdoor / Event / Email |
| Phase | Auto-detected | No | Based on start date |
| Start Date | Date | Yes | Can extend but not shorten active campaign |
| End Date | Date | Yes | |
| Status | Badge | Auto | Draft → Scheduled → Active → Paused → Completed / Cancelled |

### 4.2 Targeting

| Field | Type | Notes |
|---|---|---|
| Target Branches | Multi-select or All | Which branches this campaign covers |
| Target Streams | Multi-select | MPC / BiPC / MEC / CEC / HEC / Foundation / All |
| Target Student Type | Multi-select | Day Scholar / Hosteler (Boys) / Hosteler (Girls) / Integrated / All |
| Target Class Range | Multi-select | Class 1–5 / Class 6–8 / Class 9–10 / Class 11–12 / All |
| Target Geography | Text tags | Pin codes, areas, districts targeted |
| Target Parent Segment | Dropdown | New Parents / Existing Parents (sibling) / Alumni / Transfer / All |

### 4.3 Budget & Targets

| Field | Type | Notes |
|---|---|---|
| Total Budget | ₹ Amount | Budget allocated from season plan |
| Daily Budget Cap | ₹ Amount | Optional — auto-pauses if daily spend exceeds |
| Lead Target | Integer | Expected total enquiries |
| Conversion Target | Integer | Expected enrollments from this campaign |
| Target CPA | ₹ Amount | Target cost per admission |
| Target CPL | ₹ Amount | Target cost per lead |

### 4.4 Milestones

Repeatable milestone rows:

| Milestone | Date | Status | Owner |
|---|---|---|---|
| Creative brief approved | 15-Dec-2025 | ✅ Complete | Content Coordinator |
| Artwork designed | 22-Dec-2025 | ✅ Complete | Brand Manager (external) |
| Artwork approved | 28-Dec-2025 | ✅ Complete | Campaign Manager |
| Print order placed | 02-Jan-2026 | ✅ Complete | Content Coordinator |
| Newspaper booking confirmed | 05-Jan-2026 | ✅ Complete | Campaign Manager |
| Campaign launch | 15-Jan-2026 | ✅ Complete | Auto |
| Mid-campaign review | 30-Jan-2026 | 🔵 Upcoming | Campaign Manager |
| Campaign end | 14-Feb-2026 | 🔵 Upcoming | Auto |
| Post-campaign analysis | 21-Feb-2026 | ⬜ Pending | Data Analyst |

### 4.5 Telecalling Integration

| Field | Type | Notes |
|---|---|---|
| Telecalling follow-up enabled | Toggle | If ON, leads from this campaign auto-enter telecalling queue |
| Auto-assign to telecaller | Toggle | Round-robin assignment to available telecallers |
| Follow-up within (hours) | Integer | SLA — leads must be called within N hours of entry |
| Follow-up script | Dropdown | Select from O-18 telecalling scripts |
| Escalation rule | Dropdown | If not called within SLA → escalate to Campaign Manager |

---

## 5. Tab 2: Channels

Dynamic tab content based on selected channels. Each channel has its own sub-section.

### 5.1 Newspaper Channel

**Publication Schedule Table:**

| Column | Type | Notes |
|---|---|---|
| Publication | Dropdown | Eenadu / Sakshi / Deccan Chronicle / Times of India / Hindu / Namaste Telangana / etc. |
| Edition | Dropdown | Hyderabad City / Telangana State / AP State / National |
| Language | Badge | Telugu / English / Hindi |
| Ad Date | Date | Publication date |
| Ad Size | Dropdown | Quarter Page / Half Page / Full Page / Strip / Classified |
| Position | Dropdown | Front Page / Back Page / Inside Page / Education Supplement / ROP |
| Colour | Badge | Colour / B&W |
| Cost | ₹ Amount | Per insertion cost |
| Creative | Link | Links to material from O-03 |
| Helpline Number | Text | Which branch number to print on ad |
| Status | Badge | Booked / Published / Cancelled |
| Response | Integer | Leads attributed to this insertion (post-publish) |

**Add row:** [+ Add Newspaper Insertion]

### 5.2 WhatsApp / SMS Channel

| Field | Type | Notes |
|---|---|---|
| Message Template | Dropdown | From DLT-approved templates (O-12) |
| Target List | Dropdown | All leads / New enquiries / Interested / Specific branches |
| List Size (estimated) | Integer | Auto-calculated from target criteria |
| Schedule | Date + Time | Delivery date and time |
| Repeat | Dropdown | One-time / Daily / Weekly / Custom |
| Status | Badge | Scheduled / Sent / Delivered / Failed |

### 5.3 Digital Channel

| Field | Type | Notes |
|---|---|---|
| Platform | Multi-select | Google Ads / Facebook/Meta / Instagram / YouTube |
| Campaign ID (external) | Text | Reference to external ad platform campaign |
| Daily Budget (external) | ₹ Amount | Budget set in ad platform |
| Landing Page URL | URL | Where ads point to |
| UTM Parameters | Auto-generated | `utm_source={platform}&utm_medium=cpc&utm_campaign={campaign_slug}` |
| Notes | Textarea | External platform performance notes |

### 5.4 Outdoor / BTL Channel

| Field | Type | Notes |
|---|---|---|
| Type | Dropdown | Hoarding / Bus Shelter / Auto-Rickshaw / Pamphlet / Wall Painting |
| Locations | Multi-row | Location + City + Vendor + Cost + Start–End dates |
| Links to O-04 | Button | Opens signage tracker filtered to this campaign's hoardings |

### 5.5 Event Channel

| Field | Type | Notes |
|---|---|---|
| Event Type | Dropdown | Open Day / School Fair / Mall Stall / Society Event / Parent Meetup |
| Linked Events | Multi-select | Links to O-25 (Open Day) or O-26 (School Fair) events |
| Expected Footfall | Integer | Estimated parents/visitors |
| Lead Target | Integer | Expected enquiries from event |

---

## 6. Tab 3: Execution

### 6.1 Daily Execution Log

Table showing day-by-day campaign activity.

**Columns:**

| Column | Type | Notes |
|---|---|---|
| Date | Date | Calendar date |
| Day # | Integer | Day 1, 2, 3… of campaign |
| Spend Today | ₹ Amount | Total spend across all channels this day |
| Leads Today | Integer | New enquiries attributed to campaign |
| Calls Made | Integer | Telecalling follow-ups for this campaign's leads |
| Conversions | Integer | Enrollments from campaign leads on this day |
| Key Activity | Text | Notable action — "Eenadu full-page ad published", "WhatsApp blast sent" |
| Notes | Text | Manager's daily notes |

**Default sort:** Date DESC (latest first)
**Inline edit:** Manager can add notes directly in the table

### 6.2 Live Alerts

Real-time alerts specific to this campaign:
- "Daily budget cap reached — campaign auto-paused for today"
- "Telecalling SLA breach: 12 leads not called within 4 hours"
- "WhatsApp delivery rate dropped to 68% — check DLT template status"
- "Newspaper ad response from Sakshi Hyderabad: 0 leads — verify helpline number"

### 6.3 Action Items

Task-style list of pending actions for this campaign:

| Action | Assigned To | Due | Status |
|---|---|---|---|
| Upload creative for Week 3 newspaper insertion | Content Coordinator | 25-Jan | Pending |
| Call 48 uncontacted leads from WhatsApp batch | Telecaller Team | 22-Jan | In Progress |
| Review mid-campaign metrics and adjust budget | Campaign Manager | 30-Jan | Upcoming |
| Confirm Sakshi Hyderabad full-page for 01-Feb | Campaign Manager | 28-Jan | Pending |

---

## 7. Tab 4: Performance

### 7.1 Performance Summary Table

| Metric | Target | Actual | % of Target | Status |
|---|---|---|---|---|
| Total Leads | 2,000 | 1,240 | 62% | 🟡 (day 14 of 30 — on track if linear) |
| Total Conversions | 150 | 86 | 57% | 🟡 |
| Total Spend | ₹8,00,000 | ₹4,20,000 | 52% | ✅ (spend tracking below day %) |
| CPL (Cost per Lead) | ₹400 | ₹339 | 85% | ✅ (below target = good) |
| CPA (Cost per Admission) | ₹5,333 | ₹4,884 | 92% | ✅ |
| Conversion Rate | 7.5% | 6.9% | 92% | 🟡 |

### 7.2 Channel Attribution Table

| Channel | Leads | % of Total | Spend | CPL | Conversions | CPA |
|---|---|---|---|---|---|---|
| Newspaper (Eenadu) | 520 | 41.9% | ₹2,40,000 | ₹462 | 38 | ₹6,316 |
| Newspaper (Sakshi) | 310 | 25.0% | ₹1,20,000 | ₹387 | 24 | ₹5,000 |
| WhatsApp Blast | 280 | 22.6% | ₹30,000 | ₹107 | 18 | ₹1,667 |
| Walk-in (Ad Response) | 130 | 10.5% | ₹30,000 | ₹231 | 6 | ₹5,000 |

### 7.3 Branch-wise Performance

| Branch | Leads | Conversions | Conv % | Spend Allocated | CPA |
|---|---|---|---|---|---|
| Kukatpally | 280 | 22 | 7.9% | ₹1,00,000 | ₹4,545 |
| Dilsukhnagar | 210 | 18 | 8.6% | ₹80,000 | ₹4,444 |
| Nampally | 190 | 14 | 7.4% | ₹70,000 | ₹5,000 |
| … | … | … | … | … | … |

### 7.4 Charts (within Performance tab)

- **Daily Leads Trend:** Line chart — leads per day since campaign start
- **Channel ROI Comparison:** Bar chart — CPL and CPA per channel
- **Cumulative Spend vs Budget:** Area chart — spend curve vs budget line
- **Lead Stage Distribution:** Funnel — from enquiry to enrolled for this campaign's leads

---

## 8. Tab 5: Materials

Table of creative assets linked to this campaign from O-03 Material Library.

**Columns:**

| Column | Type | Notes |
|---|---|---|
| Thumbnail | Image (60×45) | Preview |
| Material Name | Text | Link to O-03 detail |
| Type | Badge | Newspaper Ad / WhatsApp Image / Flex / Prospectus |
| Version | Text | Current version |
| Status | Badge | Published / Pending / Draft |
| Used In | Text | Which channel/insertion this material is used for |
| Downloads | Integer | Branch downloads of this material |
| Actions | Buttons | [Preview] [Unlink] [Replace] |

**Link Material button:** Opens modal to search and select materials from O-03.

---

## 9. Drawers & Modals

### 9.1 Modal: `edit-campaign` (640px)
Same fields as O-07 Add Campaign modal, pre-filled with current values. Restrictions:
- Active campaigns: cannot change channel type or remove branches
- Completed campaigns: fully read-only

### 9.2 Modal: `clone-campaign` (480px)
- **Title:** "Clone Campaign"
- **Pre-filled:** All configuration from current campaign
- **Editable:** Campaign name (appends " — Copy"), dates, budget
- **Buttons:** Cancel · Create Clone
- **Use case:** Repeating a successful campaign format for next month/phase

### 9.3 Modal: `close-campaign` (480px)
- **Title:** "Close Campaign"
- **Summary:** Final metrics — leads, conversions, spend, CPA, CPL
- **Fields:**
  - Outcome (dropdown): Successful / Partially Successful / Underperformed / Cancelled
  - Lessons learned (textarea)
  - Recommended for repeat? (toggle)
- **Buttons:** Cancel · Close Campaign
- **Behaviour:** Status → 'completed', triggers post-campaign report in O-39

### 9.4 Drawer: `newspaper-insertion-detail` (640px)
- **Tabs:** Details · Creative · Response · Cost
- For a single newspaper insertion: publication, edition, date, size, position, creative preview, response metrics, cost breakdown

---

## 10. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Campaign updated | "Campaign '[Name]' configuration updated" | Success | 3s |
| Campaign launched | "Campaign '[Name]' is now ACTIVE" | Success | 4s |
| Campaign paused | "Campaign '[Name]' paused" | Info | 3s |
| Campaign resumed | "Campaign '[Name]' resumed" | Success | 3s |
| Campaign closed | "Campaign '[Name]' closed — final CPA: ₹[X]" | Success | 5s |
| Campaign cloned | "Campaign cloned as '[New Name]'" | Success | 3s |
| Newspaper insertion added | "Insertion added: [Publication] [Edition] on [Date]" | Success | 3s |
| Material linked | "Material '[Name]' linked to campaign" | Success | 2s |
| Budget warning | "Campaign spend at [X]% of budget" | Warning | 5s |
| Daily cap reached | "Daily budget cap reached — campaign paused for today" | Warning | 6s |
| Milestone due | "Milestone '[Name]' due in [N] days" | Info | 4s |

---

## 11. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| New campaign (no channels configured) | 📢 | "Configure Channels" | "Select and configure at least one channel to launch this campaign." | Go to Channels Tab |
| No execution data yet | 📊 | "Campaign Not Started" | "Execution data will appear once the campaign goes live." | — |
| No materials linked | 📁 | "No Materials Linked" | "Link creative assets from the Material Library for this campaign." | Link Material |
| No leads yet | 📋 | "No Leads Recorded" | "Leads will appear here once the campaign starts generating enquiries." | — |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/` | G1+ | Full campaign detail |
| PUT | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/` | G3+ | Update campaign config |
| PATCH | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/status/` | G3+ | Change status |
| POST | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/clone/` | G3+ | Clone campaign |
| POST | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/close/` | G3+ | Close with summary |
| GET | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/channels/` | G1+ | Channel configurations |
| PUT | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/channels/{channel}/` | G3+ | Update channel config |
| GET | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/execution/` | G1+ | Daily execution log |
| POST | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/execution/` | G3+ | Add daily log entry |
| GET | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/performance/` | G1+ | Performance summary |
| GET | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/performance/channel-attribution/` | G1+ | Channel breakdown |
| GET | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/performance/branch-wise/` | G1+ | Branch breakdown |
| GET | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/materials/` | G1+ | Linked materials |
| POST | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/materials/` | G2+ | Link material |
| DELETE | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/materials/{material_id}/` | G2+ | Unlink material |
| GET | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/milestones/` | G1+ | Milestone list |
| PATCH | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/milestones/{ms_id}/` | G3+ | Update milestone |
| GET | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/actions/` | G1+ | Action items |
| GET | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/newspaper-insertions/` | G1+ | Newspaper schedule |
| POST | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/newspaper-insertions/` | G3+ | Add insertion |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Tab switch | Tab button | `hx-get=".../campaigns/{id}/?tab={name}"` | `#tab-content` | `innerHTML` | `hx-trigger="click"` |
| Config load | Config tab active | `hx-get=".../campaigns/{id}/config/"` | `#config-content` | `innerHTML` | Lazy load |
| Channels load | Channels tab | `hx-get=".../campaigns/{id}/channels/"` | `#channels-content` | `innerHTML` | Dynamic sub-sections |
| Execution log | Execution tab | `hx-get=".../campaigns/{id}/execution/"` | `#execution-log` | `innerHTML` | `hx-trigger="load"` |
| Performance load | Performance tab | `hx-get=".../campaigns/{id}/performance/"` | `#performance-content` | `innerHTML` | Charts + tables |
| Materials load | Materials tab | `hx-get=".../campaigns/{id}/materials/"` | `#materials-content` | `innerHTML` | Material cards |
| Add newspaper insertion | Form submit | `hx-post=".../campaigns/{id}/newspaper-insertions/"` | `#newspaper-table-body` | `beforeend` | New row appended |
| Link material | Modal select | `hx-post=".../campaigns/{id}/materials/"` | `#materials-list` | `beforeend` | Material card added |
| Update milestone | Checkbox/date change | `hx-patch=".../campaigns/{id}/milestones/{ms_id}/"` | `#milestone-row-{ms_id}` | `outerHTML` | Inline update |
| Status change | Status button | `hx-patch=".../campaigns/{id}/status/"` | `#campaign-header` | `innerHTML` | Header refreshes |
| Daily log add | Inline form | `hx-post=".../campaigns/{id}/execution/"` | `#execution-log` | `afterbegin` | New row at top |
| Clone | Clone modal submit | `hx-post=".../campaigns/{id}/clone/"` | — | — | Redirect to new campaign page |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
