# Page 41: Phishing Simulation Manager

**URL:** `/group/it/security/phishing/`
**Roles:** Group Cybersecurity Officer (Role 56, G1) — read + recommend; Group IT Admin (Role 54, G4) — configure simulations
**Priority:** P1
**Division:** F — Group IT & Technology

---

## 1. Purpose

Schedule, manage, and review phishing simulation campaigns across all branches of the EduForge group. Phishing simulations are controlled tests that send realistic-looking phishing emails or messages to branch staff to assess whether they click on malicious links, open dangerous attachments, or submit credentials to fake login pages.

Objectives of phishing simulations:
- Measure staff security awareness across branches
- Identify high-risk individuals (repeat clickers) who need additional training
- Track improvement over time as security training takes effect
- Provide evidence of proactive security testing to auditors

When a staff member clicks a simulated phishing link, they are redirected to an educational page (the "training redirect") and optionally enrolled in a targeted training module. Results inform the mandatory security training programme (Page 42).

The Cybersecurity Officer (Role 56, G1) can view all campaign results and add recommendations but cannot create or configure campaigns. The IT Admin (Role 54, G4) can create, schedule, edit, and cancel campaigns.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Admin (Role 54, G4) | Full access | Create, schedule, edit, cancel campaigns; view all results (unmasked) |
| Group IT Director (Role 53, G4) | Read + export | View all campaigns and results |
| Group Cybersecurity Officer (Role 56, G1) | Read + recommend | View campaigns and anonymised results; add recommendations |
| All other roles | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > Cybersecurity > Phishing Simulation Manager`

**Page Header:**
- Title: `Phishing Simulation Manager`
- Subtitle: `Schedule and track phishing awareness simulation campaigns across all branches`
- Right side: `+ Create Campaign` button (Role 54 only), `Export Results (CSV)` button

**Alert Banners:**

1. **High Click Rate Warning** (amber, dismissible per session):
   - Condition: any completed campaign with click rate > 20%
   - Text: `[Campaign Name] — [Branch] recorded a [X]% click rate. Consider immediate targeted training for high-risk staff.`

2. **Upcoming Scheduled Campaign** (blue, informational, auto-dismiss after 7 days):
   - Condition: any campaign with status = Scheduled and scheduled_date within 7 days
   - Text: `Campaign "[Name]" is scheduled to run on [Date]. [X] recipients across [Y] branches.`

3. **Campaign In Progress** (blue, non-dismissible):
   - Condition: any campaign with status = In Progress
   - Text: `Phishing campaign "[Name]" is currently running. Do not alert staff until the campaign completes.`

---

## 4. KPI Summary Bar

Four KPI cards in a 4-column grid.

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Simulations Run (Last 12m) | Count of campaigns with status = Completed, within last 12 months | Plain number |
| 2 | Last Campaign Click Rate % | click_count / recipient_count × 100 for most recent completed campaign | % — red if > 20%, amber if 10–20%, green if < 10% |
| 3 | Staff Trained Post-Simulation | Count of staff who completed the training redirect module after clicking | Number, linked context |
| 4 | Branches Covered (Last 12m) | Count of distinct branches included in at least one campaign in last 12 months | Number out of total branches |

---

## 5. Main Table — Simulation Campaigns

**Table Title:** `Phishing Simulation Campaigns`

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Campaign Name | Text | Descriptive campaign name |
| Date Run | Date | Scheduled date (or actual run date for completed) |
| Branches Included | Text | Branch count; expand tooltip shows branch names |
| Recipients Count | Number | Total staff targeted |
| Opened % | % | % of recipients who opened the phishing message |
| Clicked % | % | % of recipients who clicked the link — colour: red if > 20% |
| Submitted Credentials % | % | % who entered credentials on the fake page |
| Reported as Phishing % | % | % who correctly reported the message as phishing (positive) |
| Status | Badge | Scheduled (blue) / In Progress (orange) / Completed (green) / Cancelled (grey) |
| Actions | Buttons | `View Results` / `Edit` (Role 54, Scheduled only) / `Cancel` (Role 54, Scheduled/In Progress) |

### Filters

- **Status:** All / Scheduled / In Progress / Completed / Cancelled
- **Branch:** Multi-select dropdown
- **Date Range:** Campaign date from/to
- **Click Rate:** All / Low (<10%) / Medium (10–20%) / High (>20%)

### Search

Search on campaign name. `hx-trigger="keyup changed delay:400ms"`, targets `#campaign-table`.

### Pagination

Server-side, 15 rows per page. `hx-get="/group/it/security/phishing/table/?page=N"`, targets `#campaign-table`.

### Sorting

Sortable: Date Run (default desc), Click Rate %, Status. Default: Date Run descending (most recent first).

---

## 6. Drawers

### A. Create Campaign Drawer (640px, right-side — Role 54 only)

Triggered by `+ Create Campaign` button.

**Drawer Header:** `Create Phishing Simulation Campaign`

**Sections:**

**Campaign Details:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Campaign Name | Text input | Yes | e.g., `Q1 2026 IT Alert Simulation` |
| Description | Textarea | No | Internal notes on campaign objective |
| Phishing Template | Dropdown | Yes | Prebuilt templates (see below) |
| Custom Template Notes | Textarea | No | Customisation notes for the template |
| Schedule Date | Date/time | Yes | Must be at least 48h in the future |

**Phishing Templates (prebuilt):**
- `IT Security Alert` — "Your account has been compromised — click to secure it"
- `Fee Payment Confirmation` — "Your fee payment is pending — confirm now"
- `WhatsApp Business Verification` — "Verify your WhatsApp business account"
- `EduForge Password Reset` — "Your EduForge password has expired — reset now"
- `CBSE Circular` — "Urgent circular from CBSE — download attached"

**Target Configuration:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Target Branches | Multi-select | Yes | Select one or all branches |
| Exclude Roles | Multi-select | No | e.g., exclude IT staff who would recognise the simulation |
| Include Only Role Categories | Multi-select | No | Academic / Administrative / Finance / Management |

**Post-Click Settings:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Training Redirect on Click | Toggle | Yes | Yes = redirect to training page on click |
| Training Module Link | URL input | Conditional | Required if Training Redirect = Yes |
| Show Simulation Reveal | Toggle | Yes | Show "This was a test" page after training redirect |

**Notification Settings:**
- Notify IT Director on completion: toggle
- Results summary auto-email: Yes/No

**Footer:** `Schedule Campaign` / `Save as Draft` / `Cancel`

On submit: `hx-post="/api/v1/it/security/phishing/"`. Toast: `Campaign "[Name]" scheduled for [Date]. [X] recipients across [Y] branches.`

**Audit:** Campaign creation and scheduling are logged to the IT Audit Log.

---

### B. Edit Campaign Drawer (640px — Role 54, Scheduled status only)

Same fields as Create drawer, pre-populated. Cannot edit if status = In Progress or Completed.

**Footer:** `Save Changes` / `Cancel`

---

### C. View Campaign Results Drawer (720px, right-side — all roles)

Triggered by `View Results` button. Read-only.

**Drawer Header:** `[Campaign Name] — Results`

**Overview Section:**
- Status badge, Date Run, Branches, Template used
- Summary metrics: Recipients / Opened % / Clicked % / Submitted % / Reported %
- Risk level badge (derived from click rate)

**Per-Branch Breakdown (table):**

| Branch | Recipients | Opened % | Clicked % | Submitted % | Reported % | Risk |
|--------|-----------|---------|---------|-----------|-----------|------|
| ... | ... | ... | ... | ... | ... | ... |

**Top Clickers Section:**
- **Role 56 (G1):** Shows anonymised list — `Staff Member #1 (Academic staff, Branch X)` — no names
- **Role 54/53 (G4):** Shows named list — `[Name] ([Role], [Branch])` — with `Send to Training` action button

**Click Timing Heat Map:**
- Visual grid showing hour-of-day vs day-of-week click distribution
- Identifies peak risk times (e.g., Monday morning clicks)

**Recommendations Section (Role 56):**
- Existing recommendations shown
- Textarea + `Add Recommendation` button

**Footer:** `Close` | `Export Results PDF` (Role 54/53)

---

### D. Cancel Campaign Drawer (440px — Role 54 only)

**Fields:**
- Warning: `Cancelling will abort the campaign. Recipients who haven't received the message will not be targeted.`
- Cancellation Reason (textarea, required)
- Confirm checkbox

**Footer:** `Confirm Cancel` (red) / `Back`

---

## 7. Charts

Three charts below the main table in a responsive layout (first full width, second and third side by side).

### Chart 1: Click Rate Trend (Last 6 Campaigns)
- **Type:** Line chart
- **X-axis:** Campaign names (last 6 completed)
- **Y-axis:** Click rate %
- **Reference line:** 20% threshold (red dashed)
- **Purpose:** Track whether click rates are improving over time across campaigns
- **Data endpoint:** `/api/v1/it/security/phishing/charts/click-trend/`

### Chart 2: Comparison by Branch (Last Campaign)
- **Type:** Horizontal bar chart
- **Y-axis:** Branch names
- **X-axis:** Click rate %
- **Colour:** Green < 10%, amber 10–20%, red > 20%
- **Purpose:** Identify branches that need targeted intervention
- **Data endpoint:** `/api/v1/it/security/phishing/charts/branch-comparison/`

### Chart 3: Improvement Rate for Repeat Offenders
- **Type:** Line chart
- **X-axis:** Campaign sequence (1st time offender, 2nd, 3rd, etc.)
- **Y-axis:** % who clicked again
- **Purpose:** Measure whether repeat offenders improve after training intervention
- **Note:** Data is anonymised — shows cohort rates, not individual names
- **Data endpoint:** `/api/v1/it/security/phishing/charts/repeat-offenders/`

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Campaign scheduled | Success: `Campaign "[Name]" scheduled for [Date]. [X] recipients in [Y] branches.` |
| Campaign saved as draft | Info: `Campaign saved as draft. Schedule when ready.` |
| Campaign edited | Success: `Campaign "[Name]" updated.` |
| Campaign cancelled | Success: `Campaign "[Name]" cancelled.` |
| Recommendation added | Success: `Recommendation submitted to IT Admin.` |
| Training triggered (Role 54) | Success: `[X] staff members sent to training module.` |
| Export initiated | Info: `Generating results export — please wait.` |
| Validation error | Error: `Please complete all required fields before scheduling.` |
| Schedule too soon | Error: `Campaign must be scheduled at least 48 hours in advance.` |
| Campaign creation failed | Error: `Failed to schedule phishing campaign. Please check inputs and try again.` | Error | 5s |

---

**Audit Trail:** All campaign lifecycle actions (create, launch, pause, stop, results viewed) are logged to the IT Audit Log.

**Notifications for Critical Events:**
- Phishing click rate > 30% for any campaign: Cybersecurity Officer (in-app amber + email) + IT Director (email)
- Campaign completed: Cybersecurity Officer (in-app info notification)
- Staff member clicks phishing link: Staff member sees training redirect page immediately; no separate notification sent

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No campaigns ever created | Icon + `No phishing simulations have been run. Create your first campaign to test staff security awareness.` |
| No completed campaigns yet | `No completed campaigns. Results will appear here after a campaign finishes.` |
| No campaigns match filters | `No campaigns match the selected filters.` |
| Repeat offender chart insufficient data | `Not enough campaign data to measure repeat offender improvement. Run at least 3 campaigns.` |
| Per-branch table empty | `No branch data available for this campaign.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI bar | 4 skeleton shimmer cards |
| Campaign table | 5 skeleton rows |
| Campaign results drawer | Spinner then progressive section render |
| Per-branch breakdown | Skeleton table rows |
| Heat map | Spinner with `Loading click timing data...` |
| Charts | Spinner in chart container |
| Schedule button (submitting) | `Scheduling...` text + disabled |

---

## 11. Role-Based UI Visibility

| UI Element | Role 56 (G1) | Role 54 (G4) | Role 53 (G4) |
|------------|-------------|-------------|-------------|
| Create Campaign button | Hidden | Visible | Hidden |
| Edit button (table) | Hidden | Visible (Scheduled only) | Hidden |
| Cancel button (table) | Hidden | Visible | Hidden |
| View Results button | Visible | Visible | Visible |
| Top clickers — named | Not shown (anonymised) | Named list shown | Named list shown |
| Send to Training button | Hidden | Visible | Hidden |
| Export Results PDF | Hidden | Visible | Visible |
| Add Recommendation | Visible | Hidden | Hidden |
| Export CSV (page) | Hidden | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/security/phishing/` | Fetch campaigns (paginated) |
| POST | `/api/v1/it/security/phishing/` | Create campaign (Role 54) |
| GET | `/api/v1/it/security/phishing/{id}/` | Fetch campaign detail |
| PUT | `/api/v1/it/security/phishing/{id}/` | Edit campaign (Role 54, Scheduled only) |
| POST | `/api/v1/it/security/phishing/{id}/cancel/` | Cancel campaign |
| GET | `/api/v1/it/security/phishing/{id}/results/` | Fetch campaign results |
| POST | `/api/v1/it/security/phishing/{id}/recommendations/` | Add recommendation (Role 56) |
| POST | `/api/v1/it/security/phishing/{id}/send-to-training/` | Send clickers to training module (Role 54) |
| GET | `/api/v1/it/security/phishing/kpis/` | Fetch KPI values |
| GET | `/api/v1/it/security/phishing/charts/click-trend/` | Click rate trend data |
| GET | `/api/v1/it/security/phishing/charts/branch-comparison/` | Branch click rate comparison |
| GET | `/api/v1/it/security/phishing/charts/repeat-offenders/` | Repeat offender improvement data |
| GET | `/api/v1/it/security/phishing/templates/` | Fetch available phishing templates |
| GET | `/api/v1/it/security/phishing/export/csv/` | Export campaign list |

---

## 13. HTMX Patterns

```html
<!-- Campaign table load -->
<div id="campaign-table"
     hx-get="/group/it/security/phishing/table/"
     hx-trigger="load"
     hx-target="#campaign-table"
     hx-include="#campaign-filter-form">
</div>

<!-- Create campaign drawer -->
<button hx-get="/group/it/security/phishing/create-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  + Create Campaign
</button>

<!-- Schedule campaign submit -->
<form hx-post="/api/v1/it/security/phishing/"
      hx-target="#campaign-table"
      hx-swap="outerHTML"
      hx-on::after-request="closeDrawer(); refreshKPIs()">
  <button type="submit">Schedule Campaign</button>
</form>

<!-- View results drawer -->
<button hx-get="/group/it/security/phishing/{{ campaign.id }}/results/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  View Results
</button>

<!-- Phishing template preview (live) -->
<select name="template_id"
        hx-get="/group/it/security/phishing/templates/preview/"
        hx-trigger="change"
        hx-target="#template-preview"
        hx-include="[name='template_id']">
</select>
<div id="template-preview" class="mt-2 p-3 border rounded bg-gray-50">
  <!-- rendered template preview -->
</div>

<!-- Cancel campaign confirmation -->
<form hx-post="/api/v1/it/security/phishing/{{ campaign.id }}/cancel/"
      hx-target="#campaign-table"
      hx-swap="outerHTML"
      hx-on::after-request="closeDrawer()">
  <button type="submit" class="btn-danger">Confirm Cancel</button>
</form>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
