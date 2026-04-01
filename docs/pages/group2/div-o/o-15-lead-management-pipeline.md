# O-15 — Lead Management Pipeline

> **URL:** `/group/marketing/leads/pipeline/`
> **File:** `o-15-lead-management-pipeline.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary pipeline owner

---

## 1. Purpose

The Lead Management Pipeline is the central nervous system of the entire admissions operation — it tracks every prospective student from first enquiry to confirmed enrollment across all branches. In Indian education groups, the admission funnel is brutally competitive: a large group like Narayana or Sri Chaitanya receives 50,000–2,00,000 enquiries per season but enrolls only 15,000–50,000 students (25–30% conversion). The group that manages this funnel best — fastest response to enquiries, most persistent follow-up, fewest leads lost in handoffs — wins the admission battle.

The problems this page solves:

1. **Lead leakage:** Without a pipeline, leads fall through cracks at every handoff. A newspaper ad generates 500 calls, but only 300 get logged. Of those, 200 get assigned to telecallers, but 50 are never called. Of the 150 called, 80 express interest but only 40 get a follow-up. By the time the walk-in happens, 60% of original leads are lost. This pipeline makes every stage visible with zero-tolerance for unactioned leads.

2. **Multi-source aggregation:** Leads arrive from 10+ sources simultaneously — newspaper helpline calls, website form submissions, WhatsApp replies, walk-in registers, school fair sign-ups, referrals, digital ad clicks. Without aggregation, the same parent calling the newspaper number AND filling the website form gets counted twice and called twice. The pipeline deduplicates by phone number and merges multi-source leads.

3. **Branch routing:** An enquiry for "Jr Inter MPC" might need routing to the Kukatpally branch (which has MPC capacity) rather than the Dilsukhnagar branch (which is full for MPC). The pipeline routes leads to the right branch based on: parent's pin code, preferred branch, stream availability, and seat capacity (from Division C seat matrix).

4. **Stage management:** The Indian admission pipeline has well-defined stages: Enquiry → Contacted → Interested → Walk-in Booked → Walk-in Completed → Counselled → Application Submitted → Offered Seat → Fee Paid → Enrolled. Each stage has expected timelines, and delays at any stage trigger escalation alerts.

5. **Handoff to Division C:** When a lead reaches "Fee Paid" status, it becomes a confirmed student and is handed off to Division C (Admissions) for formal enrollment processing, TC collection, and section assignment. This handoff must be seamless — no data re-entry.

**Scale:** 2,000–2,00,000 leads/season · 5–50 branches · 10+ lead sources · 10 pipeline stages · 5–50 telecallers processing leads · 15–90 day average enquiry-to-enrollment cycle

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — all leads, all branches, all stages; assign, reassign, bulk operations | Pipeline owner |
| Group Admission Telecaller Executive | 130 | G3 | Read + Update (own assigned leads only) — update stage, log calls, schedule follow-up | Cannot create leads or see others' leads |
| Group Topper Relations Manager | 120 | G3 | Read only — view leads for topper-source leads (scholarship exam toppers converting) | Cross-reference only |
| Group Admission Data Analyst | 132 | G1 | Read only — all leads, all branches; export for analytics | No stage changes |
| Group Campaign Content Coordinator | 131 | G2 | No access to lead pipeline | — |
| Group CEO / Chairman | — | G4/G5 | Read — full pipeline visibility; bulk reassign authority | Strategic oversight |
| Branch Principal | — | G3 | Read + Update (own branch leads) — can advance leads from walk-in onwards | Post-walk-in stage management |
| Branch Counsellor | — | G3 | Read + Update (own branch, post-counselling leads) — update counselling outcome | Counselling stage specialist |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Lead creation: role 119, 130 (via O-17/O-18), or system (auto-capture from forms/WhatsApp). Telecallers (130) restricted to `assigned_to = user.id`. Branch staff restricted to `branch_id = user.branch_id`. Bulk operations: role 119 or G4+ only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Lead Management  ›  Lead Pipeline
```

### 3.2 Page Header
```
Lead Management Pipeline                            [+ Add Lead]  [Import Leads]  [Bulk Actions ▾]  [Export]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · 48,200 total leads · 12,400 active · 8,640 enrolled (17.9% conversion)
```

---

## 4. KPI Summary Bar (8 cards — expanded for P0 criticality)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Leads (Season) | Integer | COUNT(leads) WHERE season = current | Static blue | `#kpi-total` |
| 2 | Active Leads | Integer | COUNT(leads) WHERE stage NOT IN ('enrolled','lost','duplicate') | Static blue | `#kpi-active` |
| 3 | New Today | Integer | COUNT(leads) WHERE created_date = today | Static green | `#kpi-today` |
| 4 | Unactioned (> 24h) | Integer | COUNT WHERE stage = 'new' AND created_at < NOW() − 24h | Red > 50, Amber 10–50, Green < 10 | `#kpi-unactioned` |
| 5 | Conversion Rate | Percentage | Enrolled / Total × 100 | Green ≥ 25%, Amber 15–25%, Red < 15% | `#kpi-conversion` |
| 6 | Avg Days to Enroll | Decimal | AVG(enrolled_date − created_date) for enrolled leads | Green ≤ 30, Amber 30–60, Red > 60 | `#kpi-avg-days` |
| 7 | Enrolled (Season) | Integer | COUNT WHERE stage = 'enrolled' | Static emerald | `#kpi-enrolled` |
| 8 | Lost (Season) | Integer | COUNT WHERE stage = 'lost' | Red if > 50% of total, Amber 30–50%, Green < 30% | `#kpi-lost` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/leads/pipeline/kpis/"` → `hx-trigger="load"` → `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 View Switcher

Three views:
1. **Kanban View** — Pipeline stages as columns, leads as cards (default)
2. **Table View** — Flat list with all lead fields
3. **Funnel View** — Visual funnel showing drop-off at each stage

### 5.2 Filter Bar (Persistent across views)

| Filter | Type | Options | Default |
|---|---|---|---|
| Season | Dropdown | 2024-25 / 2025-26 / 2026-27 | Current |
| Branch | Multi-select | All branches + "Unassigned" | All |
| Source | Multi-select | Newspaper / Digital / WhatsApp / Walk-in / Referral / School Fair / Open Day / Website / Telecall / Email / Other | All |
| Stage | Multi-select | All 10 stages (see §5.3) | All active stages |
| Assigned To | Multi-select | All telecallers/counsellors + "Unassigned" | All |
| Class/Stream | Multi-select | Foundation / Jr Inter MPC / Jr Inter BiPC / Sr Inter / Degree / Other | All |
| Date Range | Date picker | Custom range | Current season |
| Priority | Multi-select | Hot / Warm / Cold | All |
| Phone Search | Text input | Search by phone number (partial match) | — |
| Name Search | Text input | Search by parent/student name | — |

### 5.3 Pipeline Stages

| Stage # | Stage Name | Code | Colour | Expected Action | Max SLA | Auto-escalation |
|---|---|---|---|---|---|---|
| 1 | New Enquiry | `new` | `#94A3B8` Grey | Assign to telecaller | 4 hours | If unassigned > 4h → alert to Campaign Manager |
| 2 | Assigned | `assigned` | `#3B82F6` Blue | Telecaller makes first call | 24 hours | If no call logged > 24h → escalate to supervisor |
| 3 | Contacted | `contacted` | `#6366F1` Indigo | Assess interest level | 48 hours | If no disposition > 48h → follow-up reminder |
| 4 | Interested | `interested` | `#8B5CF6` Purple | Book walk-in / demo class | 7 days | If no walk-in booked > 7d → re-engage call |
| 5 | Walk-in Booked | `walkin_booked` | `#F59E0B` Amber | Parent visits branch | Walk-in date | If walk-in date passes without visit → "No Show" follow-up |
| 6 | Walk-in Done | `walkin_done` | `#D97706` Orange | Counselling session | 3 days | If no counselling > 3d post walk-in → alert |
| 7 | Counselled | `counselled` | `#EC4899` Pink | Application submission | 7 days | If no application > 7d → follow-up |
| 8 | Application Submitted | `applied` | `#14B8A6` Teal | Seat offer | 3 days | Process within 3d |
| 9 | Offered Seat | `offered` | `#10B981` Green | Fee payment | 14 days | If no payment > 14d → offer expires warning |
| 10 | Enrolled | `enrolled` | `#059669` Emerald | Handoff to Division C | Immediate | Auto-push to C-08 |

**Terminal stages (no further progression):**
- **Lost** (`lost`) — Lead decided not to join (with reason)
- **Duplicate** (`duplicate`) — Merged with another lead
- **Invalid** (`invalid`) — Wrong number, fake enquiry, spam

### 5.4 Kanban View (Default)

10 columns, one per active stage. Each column:
- **Header:** Stage name · Lead count · Total value (if fee offers made)
- **Cards:** Lead summary cards stacked vertically
- **Drag-and-drop:** Cards can be dragged between adjacent stages (forward only by default; backward allowed for 119/G4+)
- **Column scroll:** If > 10 cards, column scrolls internally with "Load more" at bottom

**Lead card layout:**
```
┌───────────────────────────────┐
│ 🔴 HOT     Rajesh Kumar       │
│ S/o Suresh · Class: Jr Inter  │
│ 📱 +91 98765 43210            │
│ 🏫 Kukatpally Branch          │
│ 📰 Source: Newspaper (Eenadu) │
│ 📅 Created: 15 Jan 2026       │
│ 👤 Assigned: Meena (Telecall) │
│ ⏰ Last action: 2 days ago    │
│ ───────────────────────────── │
│ [Call] [WhatsApp] [Note] [▸]  │
└───────────────────────────────┘
```

**Card colour coding:**
- Left border colour = priority: Red (Hot) / Amber (Warm) / Blue (Cold)
- Card background: White (normal) / Light red (SLA breached — unactioned beyond max SLA)

### 5.5 Table View

Full-featured table with all lead fields.

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Lead ID | Text | Yes | Auto-generated (e.g., L-2026-00142) |
| Student Name | Text (link) | Yes | Click → lead detail drawer |
| Parent Name | Text | Yes | Father/mother/guardian name |
| Phone | Text | Yes | Primary contact number |
| Alt Phone | Text | No | Secondary number |
| Email | Text | No | If available |
| Class Sought | Badge | Yes | Foundation / Jr Inter MPC / Jr Inter BiPC / etc. |
| Branch | Text | Yes | Preferred or assigned branch |
| Source | Badge | Yes | Lead source (colour-coded) |
| Campaign | Text | Yes | Specific campaign that generated this lead |
| Stage | Badge | Yes | Current pipeline stage (colour-coded) |
| Priority | Badge | Yes | Hot / Warm / Cold |
| Assigned To | Text | Yes | Telecaller or counsellor name |
| Created Date | DateTime | Yes | When lead entered system |
| Last Action | DateTime | Yes | When last stage change or note |
| Days in Stage | Integer | Yes | How long in current stage |
| SLA Status | Badge | Yes | On Time (green) / Warning (amber) / Breached (red) |
| Total Calls | Integer | Yes | Number of call attempts |
| Next Follow-up | Date | Yes | Scheduled follow-up date |
| Actions | Buttons | No | [View] [Call] [WhatsApp] [Assign] |

**Default sort:** SLA Status (Breached first) then Created Date DESC
**Pagination:** Server-side · 50/page (high-volume)

### 5.6 Funnel View

Visual funnel chart showing lead count at each stage with drop-off percentages.

```
┌─────────────────────────────────────────────┐
│            New Enquiry: 48,200              │  100%
├─────────────────────────────────────────┤
│          Contacted: 38,560                  │  80%
├─────────────────────────────────────┤
│        Interested: 22,414                   │  46.5%
├─────────────────────────────────┤
│      Walk-in Done: 14,460                   │  30%
├─────────────────────────────┤
│    Counselled: 11,568                       │  24%
├─────────────────────────────┤
│  Applied: 10,411                            │  21.6%
├───────────────────────┤
│ Offered: 9,640                              │  20%
├───────────────────┤
│ Enrolled: 8,640                             │  17.9%
└───────────────────┘
```

- Click on any funnel stage → filters table/kanban to that stage
- Hover shows: count, %, drop-off from previous stage, avg days in stage

### 5.7 Lead Deduplication

**Auto-deduplication rules:**
- Match on phone number (primary): exact match → merge
- Match on phone + student name (fuzzy): flag as potential duplicate
- When merging: keep earliest created date, combine all source attributions, merge notes/call logs, keep the more-advanced stage

**Duplicate queue:** List of suspected duplicates for manual review (Campaign Manager or G4+).

### 5.8 Lead Scoring

Automatic priority scoring based on configurable rules:

| Signal | Points | Example |
|---|---|---|
| Source = Referral | +30 | Referrals convert at 2× the rate |
| Source = Walk-in | +25 | Walk-in shows high intent |
| Source = Digital Ad | +10 | Lower intent but valid |
| Class = Jr Inter (high demand) | +15 | High-demand stream |
| Responded to callback within 1 hour | +20 | High engagement |
| Multiple sources (enquired via 2+ channels) | +15 | Repeated interest |
| Parent is alumni | +20 | Alumni loyalty factor |
| Sibling already enrolled | +25 | Sibling preference |
| Pin code within 5 km of branch | +10 | Proximity indicator |
| Enquiry during early-bird phase | +10 | Early intent = serious |

**Score → Priority mapping:**
- ≥ 70 points → Hot (red)
- 40–69 points → Warm (amber)
- < 40 points → Cold (blue)

---

## 6. Drawers & Modals

### 6.1 Modal: `add-lead` (560px)

- **Title:** "Add New Lead"
- **Fields:**
  - Student name (text, required)
  - Parent name (text, required)
  - Relation (dropdown): Father / Mother / Guardian
  - Phone (tel, required — +91 format, validated for 10 digits)
  - Alt phone (tel, optional)
  - Email (email, optional)
  - Class/Stream sought (dropdown, required): Foundation / Jr Inter MPC / Jr Inter BiPC / Jr Inter MEC / Jr Inter CEC / Sr Inter / Degree / Other
  - Preferred branch (dropdown — auto-suggests based on pin code if available)
  - Pin code (text, optional — 6 digits, Indian format)
  - Source (dropdown, required): Newspaper / Digital / WhatsApp / Walk-in / Referral / School Fair / Open Day / Website / Telecall / Email / Phone Call / Other
  - Campaign (dropdown — optional, link to specific campaign from O-08)
  - Referred by (text, optional — if source = Referral: parent name + phone)
  - Current school (text, optional)
  - Notes (textarea)
- **Validation:**
  - Phone: check for duplicates before saving → if match found, show existing lead details with option to merge or create anyway
  - Pin code → auto-suggest nearest branch
- **Buttons:** Cancel · Save · Save & Add Another
- **Access:** Role 119, 130 (telecallers), Branch Admin, or G4+

### 6.2 Modal: `import-leads` (640px)

- **Title:** "Import Leads"
- **Step 1 — Upload:**
  - File upload: CSV / Excel (.xlsx)
  - Template download: "Download sample template" button
  - Required columns: Student Name, Parent Name, Phone
  - Optional columns: Email, Class, Branch, Source, Campaign, Notes, Pin Code
- **Step 2 — Map Columns:**
  - Auto-detect column mapping (fuzzy header matching)
  - Manual override: dropdown per column
  - Preview: first 5 rows with mapped data
- **Step 3 — Validation & Dedup:**
  - Row count: total, valid, invalid (with error details)
  - Duplicates found: N rows match existing leads
  - Options: Skip duplicates / Merge duplicates / Import as new
- **Step 4 — Assign:**
  - Default assignment: auto-assign to telecallers (round-robin) / assign all to specific person / leave unassigned
  - Default source: if not in file, assign bulk source
- **Summary:** N leads to import, M duplicates handled, assignment rule
- **Buttons:** Cancel · Import
- **Access:** Role 119 or G4+

### 6.3 Drawer: `lead-detail` (720px, right-slide)

- **Tabs:** Profile · Timeline · Calls · Follow-ups · Documents · Linked
- **Profile tab:**
  - Student name, parent name, phone (click-to-call), email
  - Class/stream, preferred branch, pin code, current school
  - Source, campaign, referred by
  - Lead score: [XX] points → Priority: Hot/Warm/Cold (breakdown tooltip)
  - Stage: current stage badge + stage timeline (horizontal progress bar)
  - Assigned to: telecaller/counsellor name + reassign button
  - Created: date · Last action: date · Days in pipeline: N
  - Quick actions bar: [Call Now] [Send WhatsApp] [Schedule Follow-up] [Add Note] [Advance Stage ▸]
- **Timeline tab:**
  - Chronological activity log:
    - Stage changes (with who changed and when)
    - Calls (inbound/outbound, duration, disposition)
    - WhatsApp messages sent/received
    - Notes added
    - Follow-ups scheduled/completed
    - Walk-in records
    - Counselling notes
    - Application events
    - Fee payment events
  - Each entry: timestamp, actor, action, details
- **Calls tab:**
  - All call records for this lead
  - Per call: date, time, duration, direction (inbound/outbound), telecaller name, disposition, notes
  - Total calls, total duration, answer rate
- **Follow-ups tab:**
  - Scheduled follow-ups: date, type (call/WhatsApp/visit), assigned to, status
  - Overdue follow-ups highlighted in red
  - Add follow-up button
- **Documents tab:**
  - Uploaded documents: application form, ID proof, marksheet, TC (as lead progresses)
  - Upload button per document type
- **Linked tab:**
  - Linked leads (duplicates/family members)
  - Linked campaigns (all campaigns this lead interacted with)
  - Walk-in record (from O-17)
  - Application record (once submitted — links to Division C)
  - Fee payment record (once paid — links to Division D)
- **Footer:** [Edit] [Advance Stage] [Mark as Lost] [Mark as Duplicate] [Transfer Branch] [Delete (G4+)]

### 6.4 Modal: `advance-stage` (480px)

- **Title:** "Advance Lead — [Student Name]"
- **Current stage:** [Badge]
- **Next stage:** [Dropdown — typically next sequential stage, but can skip]
- **Stage-specific fields:**
  - **→ Contacted:** Disposition (Interested / Not Interested / Call Back Later / Not Reachable / Wrong Number / DND)
  - **→ Interested:** Interest level (High/Medium/Low), preferred visit date
  - **→ Walk-in Booked:** Walk-in date, time, branch, with whom
  - **→ Walk-in Done:** Walk-in notes, student present? parent present? campus tour done?
  - **→ Counselled:** Counsellor name, counselling notes, recommended stream/branch, fee discussed?
  - **→ Applied:** Application reference number, documents submitted
  - **→ Offered:** Seat details (branch, class, section), fee structure, offer validity date
  - **→ Enrolled:** Fee receipt number, enrollment date, → triggers Division C handoff
  - **→ Lost:** Reason (dropdown): Joined Competitor / Fee Too High / Location Issue / Academic Mismatch / No Response / Changed City / Other + competitor name (if applicable) + notes
- **Buttons:** Cancel · Advance
- **Access:** Based on stage — telecaller for early stages, counsellor for mid stages, 119/G4+ for all

### 6.5 Modal: `bulk-actions` (560px)

- **Title:** "Bulk Actions — [N] leads selected"
- **Actions:**
  - **Assign to:** Dropdown of telecallers → assigns all selected leads
  - **Change stage:** Dropdown → advances all to selected stage (with validation)
  - **Change branch:** Dropdown → reassigns branch
  - **Change priority:** Dropdown → Hot/Warm/Cold
  - **Send WhatsApp:** Select template → sends to all selected contacts
  - **Export:** Download selected leads as CSV/Excel
  - **Mark as Lost:** With bulk reason
  - **Mark as Duplicate:** Merge selected into one
- **Buttons:** Cancel · Apply
- **Access:** Role 119 or G4+

### 6.6 Modal: `transfer-branch` (480px)

- **Title:** "Transfer Lead to Another Branch"
- **Current branch:** [Badge]
- **New branch:** Dropdown
- **Reason:** Dropdown (Seat Full at Current / Parent Preference / Closer to Home / Stream Availability / Other)
- **Reassign to:** Dropdown (telecaller/counsellor at new branch)
- **Notes:** Textarea
- **Buttons:** Cancel · Transfer
- **Behaviour:** Lead moves to new branch, assignment changes, full history preserved
- **Access:** Role 119 or G4+

---

## 7. Charts

### 7.1 Pipeline Funnel (Funnel Chart)

| Property | Value |
|---|---|
| Chart type | Funnel (custom CSS or Chart.js plugin) |
| Title | "Admission Pipeline — Season [Year]" |
| Data | Lead count per stage (10 stages) |
| Colour | Progressive: grey → blue → purple → amber → green → emerald |
| Tooltip | "[Stage]: [N] leads ([X]% of total, [Y]% drop from prev)" |
| API | `GET /api/v1/group/{id}/marketing/leads/pipeline/analytics/funnel/` |

### 7.2 Lead Sources (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Lead Sources — Season [Year]" |
| Data | COUNT(leads) per source |
| Colour | Newspaper blue, Digital purple, WhatsApp green, Walk-in amber, Referral pink, etc. |
| Centre text | Total: [N] leads |
| Tooltip | "[Source]: [N] leads ([X]%)" |
| API | `GET /api/v1/group/{id}/marketing/leads/pipeline/analytics/by-source/` |

### 7.3 Daily Lead Inflow (Area Chart)

| Property | Value |
|---|---|
| Chart type | Area chart (Chart.js 4.x) |
| Title | "Daily New Leads — Last 90 Days" |
| Data | COUNT(leads) per day WHERE created_date in range |
| Colour | `#3B82F6` blue area with gradient |
| X-axis | Date |
| Y-axis | Count |
| Annotations | Vertical lines marking campaign launches and phase transitions |
| API | `GET /api/v1/group/{id}/marketing/leads/pipeline/analytics/daily-inflow/` |

### 7.4 Branch Conversion Comparison (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped horizontal bar |
| Title | "Branch Conversion Rates" |
| Data | Per branch: leads received (bar 1) + enrolled (bar 2) + conversion % (label) |
| Colour | Leads: `#93C5FD` light blue; Enrolled: `#059669` emerald |
| Tooltip | "[Branch]: [N] leads → [M] enrolled ([X]%)" |
| API | `GET /api/v1/group/{id}/marketing/leads/pipeline/analytics/branch-conversion/` |

### 7.5 Stage Ageing (Box Plot / Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Average Days in Each Pipeline Stage" |
| Data | AVG(days_in_stage) per stage |
| Colour | Green (within SLA) / Red (exceeding SLA) per bar |
| Benchmark line | SLA target for each stage |
| Tooltip | "[Stage]: Avg [X] days (SLA: [Y] days)" |
| API | `GET /api/v1/group/{id}/marketing/leads/pipeline/analytics/stage-ageing/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Lead created | "Lead '[Student Name]' created — assigned to [Telecaller]" | Success | 3s |
| Lead imported | "[N] leads imported — [M] duplicates skipped" | Success | 4s |
| Stage advanced | "Lead '[Name]' advanced to [Stage]" | Success | 2s |
| Lead enrolled | "🎉 Lead '[Name]' enrolled at [Branch]! Handoff to Div C initiated." | Success | 5s |
| Lead marked lost | "Lead '[Name]' marked as lost — reason: [Reason]" | Info | 3s |
| Lead assigned | "Lead '[Name]' assigned to [Telecaller]" | Success | 2s |
| Bulk action applied | "[N] leads updated — [Action] applied" | Success | 3s |
| Branch transferred | "Lead '[Name]' transferred from [Old] to [New Branch]" | Info | 3s |
| Duplicate detected | "Possible duplicate: '[Name]' matches existing lead L-[ID]" | Warning | 5s |
| SLA breach alert | "[N] leads have breached SLA — review immediately" | Error | 6s |
| Follow-up due | "[N] follow-ups due today" | Info | 3s |
| Call logged | "Call logged — [Duration] — [Disposition]" | Success | 2s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No leads in pipeline | 📋 | "No Leads Yet" | "Add your first lead manually or import from a campaign." | Add Lead / Import Leads |
| No leads in stage | 📊 | "No Leads in [Stage]" | "No leads are currently at this stage." | — |
| No leads for telecaller | 👤 | "No Leads Assigned" | "You have no leads assigned. Check with your Campaign Manager." | — |
| No leads for branch | 🏫 | "No Leads for [Branch]" | "No enquiries have been received for your branch yet." | — |
| Pipeline not configured | ⚙️ | "Pipeline Not Set Up" | "Configure your pipeline stages and SLA rules before adding leads." | Configure |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 8 KPI shimmer cards + filter bar placeholder + kanban skeleton (10 columns × 3 card placeholders) |
| View switch (kanban/table/funnel) | Content area skeleton for target view |
| Kanban card drag | Ghost card + drop zone highlight |
| Lead detail drawer | 720px skeleton: profile header + 6 tab placeholders |
| Table view load | 15-row table skeleton |
| Funnel view load | Funnel shape placeholder (8 grey bars) |
| Import wizard steps | Step content shimmer |
| Chart load | Grey canvas placeholder |
| Bulk action processing | Full-width progress bar: "Processing [N] leads…" |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/leads/pipeline/` | G1+ | List leads (filterable, paginated) |
| GET | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/` | G1+ | Lead detail |
| POST | `/api/v1/group/{id}/marketing/leads/pipeline/` | G3+ | Create lead |
| PUT | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/` | G3+ | Update lead |
| PATCH | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/stage/` | G3+ | Advance/change stage |
| PATCH | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/assign/` | G3+ | Assign/reassign lead |
| PATCH | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/transfer/` | G3+ | Transfer to another branch |
| PATCH | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/priority/` | G3+ | Update priority |
| POST | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/notes/` | G3+ | Add note |
| POST | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/calls/` | G3+ | Log call |
| POST | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/follow-ups/` | G3+ | Schedule follow-up |
| GET | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/timeline/` | G1+ | Activity timeline |
| POST | `/api/v1/group/{id}/marketing/leads/pipeline/import/` | G3+ | Bulk import |
| POST | `/api/v1/group/{id}/marketing/leads/pipeline/bulk/` | G3+ | Bulk actions |
| GET | `/api/v1/group/{id}/marketing/leads/pipeline/duplicates/` | G3+ | Duplicate queue |
| POST | `/api/v1/group/{id}/marketing/leads/pipeline/duplicates/{dup_id}/merge/` | G3+ | Merge duplicates |
| DELETE | `/api/v1/group/{id}/marketing/leads/pipeline/{lead_id}/` | G4+ | Delete lead |
| GET | `/api/v1/group/{id}/marketing/leads/pipeline/kanban/` | G1+ | Kanban view data (grouped by stage) |
| GET | `/api/v1/group/{id}/marketing/leads/pipeline/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/leads/pipeline/analytics/funnel/` | G1+ | Funnel data |
| GET | `/api/v1/group/{id}/marketing/leads/pipeline/analytics/by-source/` | G1+ | Source donut |
| GET | `/api/v1/group/{id}/marketing/leads/pipeline/analytics/daily-inflow/` | G1+ | Daily inflow chart |
| GET | `/api/v1/group/{id}/marketing/leads/pipeline/analytics/branch-conversion/` | G1+ | Branch comparison |
| GET | `/api/v1/group/{id}/marketing/leads/pipeline/analytics/stage-ageing/` | G1+ | Stage ageing data |

### Integration Endpoints

| Direction | System | Endpoint | Purpose |
|---|---|---|---|
| Inbound | Website form | `/webhooks/leads/website/` | Auto-create lead from website enquiry form |
| Inbound | WhatsApp reply | `/webhooks/leads/whatsapp/` | Auto-create lead from WhatsApp campaign reply |
| Inbound | Digital ad (Google/Meta) | `/webhooks/leads/digital/` | Auto-create from lead form ads |
| Outbound | Division C (Admissions) | POST `/api/v1/institution/{id}/admissions/` | Push enrolled lead to formal admission system |
| Outbound | Division D (Finance) | GET `/api/v1/group/{id}/finance/fee-receipts/` | Verify fee payment for enrollment stage |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../pipeline/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| View switch | View button click | `hx-get=".../pipeline/?view={kanban/table/funnel}"` | `#pipeline-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Any filter change | `hx-get` with filter params | `#pipeline-content` | `innerHTML` | `hx-trigger="change"` |
| Kanban load | Default view | `hx-get=".../pipeline/kanban/"` | `#kanban-board` | `innerHTML` | `hx-trigger="load"` |
| Kanban card drag | Drop on new column | JS drag → `hx-patch=".../pipeline/{id}/stage/"` | `#kanban-board` | `innerHTML` | Confirm modal for certain transitions |
| Lead detail drawer | Card/row click | `hx-get=".../pipeline/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Add lead | Form submit | `hx-post=".../pipeline/"` | `#add-result` | `innerHTML` | Dedup check inline before submit |
| Advance stage | Stage form | `hx-patch=".../pipeline/{id}/stage/"` | `#stage-badge-{id}` | `innerHTML` | Inline badge update + kanban refresh |
| Log call | Call form | `hx-post=".../pipeline/{id}/calls/"` | `#timeline-{id}` | `afterbegin` | Prepend to timeline |
| Add note | Note form | `hx-post=".../pipeline/{id}/notes/"` | `#timeline-{id}` | `afterbegin` | Prepend to timeline |
| Schedule follow-up | Follow-up form | `hx-post=".../pipeline/{id}/follow-ups/"` | `#followup-list-{id}` | `afterbegin` | Prepend |
| Assign lead | Assign dropdown | `hx-patch=".../pipeline/{id}/assign/"` | `#assigned-{id}` | `innerHTML` | Inline update |
| Bulk action | Bulk form | `hx-post=".../pipeline/bulk/"` | `#bulk-result` | `innerHTML` | Progress bar + toast |
| Import wizard | Step nav | `hx-post=".../pipeline/import/"` | `#import-wizard` | `innerHTML` | Multi-step |
| Table pagination | Page controls | `hx-get` with `?page={n}` | `#pipeline-table-body` | `innerHTML` | 50/page |
| Phone search | Input keyup (debounced) | `hx-get=".../pipeline/?phone={input}"` | `#pipeline-content` | `innerHTML` | `hx-trigger="keyup changed delay:500ms"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
