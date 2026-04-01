# O-17 — Walk-in Enquiry Register

> **URL:** `/group/marketing/leads/walk-ins/`
> **File:** `o-17-walk-in-enquiry-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admission Telecaller Executive (Role 130, G3) — primary data entry; Campaign Manager (119) — oversight

---

## 1. Purpose

The Walk-in Enquiry Register is the digital version of the physical enquiry register that sits at every branch's admission counter. When a parent walks into a branch with their child, the front-desk staff or telecaller logs the visit here — capturing parent details, student details, class/stream interest, how they heard about the school, whether the child was present, whether a campus tour happened, and the immediate next step (counselling appointment, call back, application form given). In peak admission months (February–April), a popular branch receives 50–200 walk-ins per day, and each walk-in is the most valuable lead in the funnel — they've already invested time and effort to visit.

The problems this page solves:

1. **Paper register replacement:** Most Indian schools still use a physical register. Parents fill a line, staff can't read the handwriting, phone numbers are wrong, and nobody follows up. The digital register enforces structured data entry, validates phone numbers, and auto-creates a follow-up task.

2. **Walk-in to pipeline linkage:** A walk-in may be a first visit (new lead) or a return visit from an existing lead who was initially contacted via newspaper or WhatsApp. The register checks for existing leads by phone number and links the walk-in to the existing pipeline record rather than creating a duplicate.

3. **Branch-level visibility:** Each branch logs its own walk-ins, but the Campaign Manager at Group HQ needs to see all branches in real-time: which branch is getting heavy footfall today? Which branch has zero walk-ins despite an ongoing newspaper campaign? This visibility enables same-day resource reallocation.

4. **Follow-up enforcement:** Every walk-in that doesn't convert to an application on the spot must have a follow-up scheduled. The system enforces: no walk-in record can be marked complete without either an application submission or a follow-up date. This eliminates the "parent visited, liked the campus, went home, nobody called back, parent enrolled at competitor" pattern.

**Scale:** 5–50 branches · 10–200 walk-ins/day/branch during peak · 2,000–50,000 walk-ins/season total · 70–85% of walk-ins have a prior enquiry

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admission Telecaller Executive | 130 | G3 | Full CRUD (own branch) — log walk-ins, update outcomes | Primary data entry at branch counter |
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD (all branches) — view, edit, reassign, export | Pipeline oversight |
| Branch Principal | — | G3 | Read + Update (own branch) — view walk-ins, mark counselling outcomes | Post-walk-in counselling |
| Branch Counsellor | — | G3 | Read + Update (own branch, assigned walk-ins) — log counselling notes | Counselling outcome entry |
| Group Admission Data Analyst | 132 | G1 | Read only — walk-in analytics, footfall trends | Analytics |
| Group CEO / Chairman | — | G4/G5 | Read — all branches walk-in data | Strategic oversight |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Walk-in logging: role 130 (branch counter) or 119 (any branch). Branch staff restricted to `branch_id = user.branch_id`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Lead Management  ›  Walk-in Enquiry Register
```

### 3.2 Page Header
```
Walk-in Enquiry Register                            [+ Log Walk-in]  [Today's Summary]  [Export]
Front Desk — Kukatpally Branch (or "All Branches" for Campaign Manager view)
Sunrise Education Group · Today: 42 walk-ins · This Week: 186 · Season Total: 8,420 · Conversion: 62%
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Walk-ins Today | Integer | COUNT WHERE walk_in_date = today AND branch = user.branch (or all) | Static blue | `#kpi-today` |
| 2 | Walk-ins This Week | Integer | COUNT WHERE walk_in_date in current week | Static blue | `#kpi-week` |
| 3 | Conversion Rate | Percentage | (Applied + Enrolled) / Total Walk-ins × 100 | Green ≥ 60%, Amber 40–60%, Red < 40% | `#kpi-conversion` |
| 4 | Pending Follow-ups | Integer | COUNT WHERE outcome = 'follow_up' AND follow_up_date ≤ today AND follow_up_done = false | Red > 20, Amber 10–20, Green < 10 | `#kpi-pending-followup` |
| 5 | No-Shows Today | Integer | COUNT WHERE walk_in_booked_date = today AND actually_visited = false | Red > 10, Amber 5–10, Green < 5 | `#kpi-noshows` |
| 6 | Avg Wait Time | Minutes | AVG(counselling_start − arrival_time) WHERE walk_in_date = today | Green ≤ 15 min, Amber 15–30, Red > 30 | `#kpi-wait-time` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/leads/walk-ins/kpis/"` → `hx-trigger="load, every 60s"` → `hx-swap="innerHTML"` (auto-refresh every 60s during peak hours)

---

## 5. Sections

### 5.1 Tab Navigation

Three tabs:
1. **Today's Register** — Walk-ins logged today (real-time updating)
2. **All Walk-ins** — Historical register with full filters
3. **Analytics** — Footfall trends, branch comparison, conversion

### 5.2 Tab 1: Today's Register

**Real-time table — auto-refreshes every 30 seconds during peak hours (8 AM–5 PM).**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Token/serial number for the day |
| Token | Badge | No | Walk-in token: T-001, T-002 (sequential per branch per day) |
| Arrival Time | Time | Yes | When parent arrived |
| Parent Name | Text | Yes | Father/mother name |
| Student Name | Text | Yes | Child name |
| Phone | Text | Yes | Parent phone |
| Class Sought | Badge | Yes | Foundation / Jr Inter MPC / BiPC / etc. |
| Source | Badge | Yes | How did they hear? (Newspaper / WhatsApp / Referral / Walk-by / etc.) |
| Student Present | Badge | No | ✅ Yes / ❌ No |
| Campus Tour | Badge | No | ✅ Done / ⏳ Pending / ❌ Declined |
| Counsellor | Text | No | Assigned counsellor name |
| Wait Time | Duration | Yes | Time since arrival (if not yet counselled) |
| Status | Badge | Yes | Waiting (amber) / In Counselling (blue) / Completed (green) / Left Without Counselling (red) |
| Outcome | Badge | Yes | Application Given / Application Submitted / Follow-up Scheduled / Not Interested / Thinking |
| Actions | Buttons | No | [Start Counselling] [Complete] [Edit] |

**Colour coding rows:**
- Yellow background: Waiting > 15 minutes
- Red background: Waiting > 30 minutes (escalation alert)
- Green background: Completed with application submitted
- Grey background: Left without counselling

### 5.3 Tab 2: All Walk-ins

Full historical register.

**Filter bar:** Branch · Date Range · Class · Source · Outcome · Counsellor · Existing Lead (Yes/No) · Follow-up Status

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Walk-in Date | Date | Yes | Date of visit |
| Token | Text | No | Day token |
| Branch | Text | Yes | Branch name |
| Parent Name | Text | Yes | — |
| Student Name | Text (link) | Yes | Click → walk-in detail drawer |
| Phone | Text | Yes | — |
| Class Sought | Badge | Yes | — |
| Source | Badge | Yes | — |
| Existing Lead | Badge | Yes | ✅ Linked to L-XXXX / ❌ New |
| Counsellor | Text | Yes | — |
| Duration | Duration | Yes | Total time at branch (arrival to departure) |
| Outcome | Badge | Yes | Application Submitted / Application Given / Follow-up / Not Interested / Thinking / Left Early |
| Follow-up Date | Date | Yes | If outcome = follow-up |
| Follow-up Done | Badge | Yes | ✅ / ❌ / ⏳ Overdue |
| Pipeline Stage | Badge | Yes | Current stage in O-15 pipeline (if linked) |
| Actions | Buttons | No | [View] [Edit] [Log Follow-up] |

**Default sort:** Walk-in Date DESC, Arrival Time DESC
**Pagination:** Server-side · 50/page

### 5.4 Tab 3: Analytics

Charts and metrics (see §7).

---

## 6. Drawers & Modals

### 6.1 Modal: `log-walk-in` (640px)

- **Title:** "Log Walk-in Enquiry"
- **Fields:**
  - **Check existing lead first:**
    - Phone number (tel, required) → live search against O-15 lead pipeline
    - If match found: "Existing lead found — [Student Name], Stage: [Stage], Source: [Source]" → link walk-in to existing lead
    - If no match: proceed as new lead
  - **Parent details:**
    - Parent name (text, required)
    - Relation (dropdown): Father / Mother / Guardian
    - Phone (pre-filled from search)
    - Alt phone (tel, optional)
    - Email (optional)
  - **Student details:**
    - Student name (text, required)
    - Current class (dropdown — the class they're currently in)
    - Class/stream sought (dropdown, required — what they want to join)
    - Current school name (text, optional)
    - Date of birth (date, optional)
  - **Visit details:**
    - Arrival time (time, defaults to current time)
    - Branch (dropdown, defaults to user's branch; multi-branch for 119)
    - Student physically present? (toggle, default yes)
    - Source — "How did you hear about us?" (dropdown, required): Newspaper Ad / WhatsApp Message / Friend/Relative Referral / Parent of Existing Student / Walk-by (Passing By) / Hoarding/Banner / Online Search / School Fair / Previous Year Enquiry / Other
    - If Referral: Referred by name + phone
    - Specific campaign (dropdown, optional — link to O-08 campaign)
  - **Interests:**
    - Hostel required? (toggle)
    - Transport required? (toggle)
    - Scholarship enquiry? (toggle)
  - **Documents brought:**
    - [ ] Previous report card
    - [ ] Transfer certificate
    - [ ] Aadhar card
    - [ ] Birth certificate
    - [ ] Passport photos
  - **Initial notes** (textarea — first impression, specific questions asked by parent)
- **Buttons:** Cancel · Save Walk-in
- **Post-save behaviour:**
  - If new lead: auto-creates lead in O-15 pipeline at stage "Walk-in Done"
  - If existing lead: updates O-15 lead to stage "Walk-in Done" and links walk-in record
  - Token number auto-assigned (T-XXX)
  - Walk-in appears in Today's Register immediately
- **Access:** Role 130 (telecaller), 119, Branch Admin, or G4+

### 6.2 Modal: `complete-walk-in` (560px)

- **Title:** "Complete Walk-in — [Student Name]"
- **Fields:**
  - Counselled by (dropdown — counsellor/principal name)
  - Counselling duration (auto-calculated from start to now, editable)
  - Campus tour done? (toggle)
  - Demo class attended? (toggle + which subject)
  - Outcome (dropdown, required):
    - **Application Submitted** — filled and submitted on the spot
    - **Application Form Given** — took form home; follow-up needed
    - **Fee Structure Given** — interested but wants to compare
    - **Follow-up Scheduled** — will return on specific date
    - **Thinking / Will Decide** — needs time; generic follow-up
    - **Not Interested** — decided against joining (reason required)
    - **Left Without Counselling** — waited too long / changed mind
  - If Follow-up: follow-up date (required), follow-up type (Call / WhatsApp / Re-visit), assigned to
  - If Not Interested: reason (dropdown): Fee Too High / Location Far / Academic Mismatch / Joined Competitor (which?) / Facilities Not Satisfactory / Other
  - Fee quote given (₹, optional — what fee amount was communicated)
  - Scholarship discussed? (toggle + scholarship type if yes)
  - Parent satisfaction (1–5 stars — quick rating)
  - Counselling notes (textarea — detailed notes on discussion)
- **Buttons:** Cancel · Complete
- **Post-complete:** Updates O-15 pipeline stage to "Counselled" (or "Applied" if application submitted). Follow-up auto-scheduled if applicable.
- **Access:** Role 130, Branch Counsellor, Branch Principal, 119, or G4+

### 6.3 Drawer: `walk-in-detail` (640px, right-slide)

- **Tabs:** Details · Counselling · Follow-ups · Pipeline Link
- **Details tab:** All walk-in fields, arrival/departure times, token, documents brought, source
- **Counselling tab:** Counsellor notes, outcome, fee quote, campus tour status, demo class, satisfaction rating
- **Follow-ups tab:** All follow-ups scheduled for this walk-in; status (done/pending/overdue); notes per follow-up
- **Pipeline Link tab:** Link to O-15 lead record; current pipeline stage; full timeline from enquiry to current state
- **Footer:** [Edit] [Log Follow-up] [View in Pipeline] [Print Walk-in Slip]

### 6.4 Modal: `print-walk-in-slip` (400px)

- **Title:** "Print Walk-in Slip"
- **Content:** Formatted A5 slip with:
  - Group logo + branch name
  - Token number: T-XXX
  - Date + Time
  - Student name, parent name
  - Class/stream sought
  - Counsellor assigned
  - Next step (follow-up date / application info)
  - Branch contact number
- **Buttons:** Print · Download PDF
- **Purpose:** Give parent a physical takeaway with reference number

---

## 7. Charts

### 7.1 Daily Footfall Trend (Bar + Line)

| Property | Value |
|---|---|
| Chart type | Combo — bar (walk-ins) + line (conversion %) |
| Title | "Daily Walk-in Footfall — Last 30 Days" |
| Data | Per day: walk-in count (bar) + conversion rate (line) |
| Bar colour | `#3B82F6` blue |
| Line colour | `#10B981` green |
| X-axis | Date |
| Tooltip | "[Date]: [N] walk-ins, [X]% converted" |
| API | `GET /api/v1/group/{id}/marketing/leads/walk-ins/analytics/daily-footfall/` |

### 7.2 Branch Footfall Comparison (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Walk-ins by Branch — This Month" |
| Data | COUNT per branch |
| Colour | `#3B82F6` blue |
| Tooltip | "[Branch]: [N] walk-ins, [X]% conversion" |
| API | `GET /api/v1/group/{id}/marketing/leads/walk-ins/analytics/branch-comparison/` |

### 7.3 Hourly Distribution (Heatmap)

| Property | Value |
|---|---|
| Chart type | Heatmap (7 rows × 10 columns) |
| Title | "Walk-in Peak Hours — Day × Time" |
| Data | Rows = Mon–Sun, Columns = 8 AM–6 PM (hourly); Cell = walk-in count |
| Colour | White (0) → Light Blue → Dark Blue (peak) |
| Purpose | Identify peak hours for staffing counsellors |
| API | `GET /api/v1/group/{id}/marketing/leads/walk-ins/analytics/hourly-heatmap/` |

### 7.4 Outcome Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Walk-in Outcomes — Season [Year]" |
| Data | COUNT per outcome type |
| Colour | App Submitted: emerald / App Given: green / Follow-up: amber / Not Interested: red / Left Early: grey |
| Tooltip | "[Outcome]: [N] ([X]%)" |
| API | `GET /api/v1/group/{id}/marketing/leads/walk-ins/analytics/outcomes/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Walk-in logged | "Walk-in logged — Token T-[XXX] for [Student Name]" | Success | 3s |
| Existing lead linked | "Walk-in linked to existing lead L-[ID] — pipeline updated" | Info | 4s |
| Walk-in completed | "Walk-in completed — Outcome: [Outcome]" | Success | 3s |
| Follow-up scheduled | "Follow-up for [Name] scheduled on [Date]" | Success | 3s |
| Follow-up overdue | "[N] walk-in follow-ups overdue — call parents back!" | Warning | 5s |
| Long wait alert | "[Student Name] has been waiting [N] minutes — assign counsellor" | Warning | 5s |
| Walk-in slip printed | "Walk-in slip printed for T-[XXX]" | Success | 2s |
| Application submitted | "Application submitted for [Name] — moved to Applied stage" | Success | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No walk-ins today | 🚶 | "No Walk-ins Today" | "Walk-in enquiries will appear here as parents visit the branch." | Log Walk-in |
| No walk-ins for branch | 🏫 | "No Walk-ins for [Branch]" | "This branch hasn't recorded any walk-ins yet." | — |
| No follow-ups pending | ✅ | "All Follow-ups Done" | "Great work! All walk-in follow-ups are completed." | — |
| No analytics data | 📊 | "Not Enough Data" | "Walk-in analytics will appear after recording multiple days of visits." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + tab bar + today's table skeleton (8 rows) |
| Auto-refresh (30s) | Silent table refresh — no visible loader (seamless update) |
| Walk-in detail drawer | 640px skeleton: details section + 4 tabs |
| Complete walk-in modal | Form skeleton |
| Chart load | Grey canvas placeholder |
| All walk-ins table | 15-row table skeleton |
| Walk-in slip print | Print dialog |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/leads/walk-ins/` | G1+ | List walk-ins (filterable) |
| GET | `/api/v1/group/{id}/marketing/leads/walk-ins/today/` | G1+ | Today's register (auto-refresh) |
| GET | `/api/v1/group/{id}/marketing/leads/walk-ins/{wk_id}/` | G1+ | Walk-in detail |
| POST | `/api/v1/group/{id}/marketing/leads/walk-ins/` | G3+ | Log walk-in |
| PUT | `/api/v1/group/{id}/marketing/leads/walk-ins/{wk_id}/` | G3+ | Update walk-in |
| PATCH | `/api/v1/group/{id}/marketing/leads/walk-ins/{wk_id}/complete/` | G3+ | Complete walk-in (outcome + notes) |
| POST | `/api/v1/group/{id}/marketing/leads/walk-ins/{wk_id}/follow-up/` | G3+ | Schedule follow-up |
| PATCH | `/api/v1/group/{id}/marketing/leads/walk-ins/{wk_id}/follow-up/{fu_id}/done/` | G3+ | Mark follow-up done |
| GET | `/api/v1/group/{id}/marketing/leads/walk-ins/{wk_id}/slip/` | G2+ | Generate walk-in slip PDF |
| GET | `/api/v1/group/{id}/marketing/leads/walk-ins/check-existing/?phone={phone}` | G3+ | Check if phone matches existing lead |
| DELETE | `/api/v1/group/{id}/marketing/leads/walk-ins/{wk_id}/` | G4+ | Delete walk-in record |
| GET | `/api/v1/group/{id}/marketing/leads/walk-ins/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/leads/walk-ins/analytics/daily-footfall/` | G1+ | Footfall chart |
| GET | `/api/v1/group/{id}/marketing/leads/walk-ins/analytics/branch-comparison/` | G1+ | Branch bar chart |
| GET | `/api/v1/group/{id}/marketing/leads/walk-ins/analytics/hourly-heatmap/` | G1+ | Heatmap data |
| GET | `/api/v1/group/{id}/marketing/leads/walk-ins/analytics/outcomes/` | G1+ | Outcome donut |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../walk-ins/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 60s"` |
| Today auto-refresh | Today's table | `hx-get=".../walk-ins/today/"` | `#today-table-body` | `innerHTML` | `hx-trigger="every 30s"` |
| Tab switch | Tab click | `hx-get=".../walk-ins/?tab={today/all/analytics}"` | `#walkin-content` | `innerHTML` | `hx-trigger="click"` |
| Phone check (dedup) | Phone input | `hx-get=".../walk-ins/check-existing/?phone={val}"` | `#dedup-result` | `innerHTML` | `hx-trigger="keyup changed delay:500ms"` |
| Log walk-in | Form submit | `hx-post=".../walk-ins/"` | `#log-result` | `innerHTML` | Toast + today's table refresh |
| Complete walk-in | Complete form | `hx-patch=".../walk-ins/{id}/complete/"` | `#row-{id}` | `innerHTML` | Inline row update |
| Walk-in detail drawer | Row click | `hx-get=".../walk-ins/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Schedule follow-up | Follow-up form | `hx-post=".../walk-ins/{id}/follow-up/"` | `#followup-result` | `innerHTML` | Toast |
| Filter apply | Dropdowns | `hx-get` with params | `#walkin-table-body` | `innerHTML` | `hx-trigger="change"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#walkin-table-body` | `innerHTML` | 50/page |
| Print slip | Print button | `hx-get=".../walk-ins/{id}/slip/"` | `#slip-modal-content` | `innerHTML` | Opens printable modal |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
