# O-40 — Marketing MIS Report

> **URL:** `/group/marketing/analytics/mis-report/`
> **File:** `o-40-marketing-mis-report.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admission Data Analyst (Role 132, G1) — primary author and scheduler

---

## 1. Purpose

The Marketing MIS Report is the group's standardised monthly Management Information System report — a fixed-format, auto-generated document that captures every critical marketing metric (leads received, conversions achieved, money spent, seats filled, exceptions flagged) in a consistent structure that the CEO and Board of Directors expect on the 1st of every month without fail. In Indian corporate governance — whether it is a family-run trust operating 8 schools in Andhra Pradesh or a corporate chain running 40 branches across 5 states — MIS reports are the backbone of management oversight. The Board does not open dashboards; the Board reads a monthly document in a familiar format, compares this month's numbers with last month's and the same month last year, and makes decisions within 10 minutes of reading.

The problems this page solves:

1. **Format inconsistency kills comparability:** The entire value of an MIS report lies in its consistency. If January's report has 12 sections and February's has 8, the Board cannot compare. If the CPL is calculated differently each month (some months include WhatsApp spend, others exclude it), trends are meaningless. The system locks the report template — same sections, same metrics, same calculation methodology — every single month. Any template change requires G4/G5 approval and is versioned.

2. **Manual report generation wastes a week:** In most groups, the Data Analyst spends the first 5 working days of every month pulling data from disparate sources, cross-checking with finance (did the ₹8L newspaper bill get booked to marketing or admin?), formatting Excel sheets, and emailing PDFs. By the time the report reaches the CEO, it is the 8th or 10th — stale data. The system auto-generates the report on the 1st of each month using live data from O-08 through O-37, with human review and annotation before distribution.

3. **Exception reporting is an afterthought:** The Board cares about two things: "Are we on track?" and "What needs my attention?" Generic tables bury exceptions. The MIS report highlights branches below target fill rate, channels with deteriorating ROI, spend overruns, and conversion drops — surfaced as red-flagged exceptions at the top of the report, before the detailed data.

4. **Distribution chaos:** The CEO wants it by email. The CFO wants it in the Board WhatsApp group. The Branch Principal wants only their branch's section. Without automated, role-based distribution, the same report gets reformatted 3 times and sent through 4 channels. The system supports scheduled auto-email on the 1st (or configurable date), with role-based section filtering.

5. **Historical MIS amnesia:** When the Board asks "What was our CPL in October 2024?", nobody can find that month's report. Email attachments are lost, shared drives are unorganised. The system maintains a complete archive of every monthly MIS with version history, accessible in 2 clicks.

**Scale:** 12 reports per year (monthly) · 5–50 branches · auto-generated on schedule · 8–15 report sections · emailed to 5–20 stakeholders · historical archive spanning 3–5 years · comparison with previous month + same month last year

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admission Data Analyst | 132 | G1 | Full CRUD — configure template, review auto-generated report, annotate, approve, schedule | Primary owner |
| Group Admissions Campaign Manager | 119 | G3 | Read + Annotate — view report, add campaign context notes | Adds operational context |
| Group Topper Relations Manager | 120 | G3 | Read — view topper-related MIS sections | Reference only |
| Group Admission Telecaller Executive | 130 | G3 | Read (own section) — view telecalling metrics section | Performance self-review |
| Group Campaign Content Coordinator | 131 | G2 | Read — view content and material performance section | Reference only |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — review MIS, approve for distribution, configure recipients | Final authority; primary consumer |
| Branch Principal | — | G3 | Read (own branch) — view branch-specific extract of MIS | Monthly branch performance check |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Template configuration: role 132 or G4+. Auto-generation runs as system job (no auth — writes to draft status). Annotation: roles 119, 132, G4+. Distribution approval: G4/G5. Branch principals receive filtered extract only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Analytics & Reports  >  Marketing MIS Report
```

### 3.2 Page Header
```
Marketing MIS Report                                  [Month: Mar 2026 ▼]  [Configure Template]  [Schedule]  [Export]  [Distribute]
Data Analyst — Priya Venkatesh
Sunrise Education Group · March 2026 MIS · Status: Review · Auto-generated: 01 Mar 2026 05:30 IST · 28 branches
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Leads This Month | Integer | COUNT(new_leads) WHERE month = selected | Static blue | `#kpi-leads` |
| 2 | Conversions This Month | Integer | COUNT(new_enrollments) WHERE month = selected | Static green | `#kpi-conversions` |
| 3 | Month Spend (₹) | Amount | SUM(campaign_spend) WHERE month = selected | Amber > 110% of monthly budget, Red > 130% | `#kpi-spend` |
| 4 | Month CPL (₹) | Amount | Month spend / Month leads | Green ≤ ₹800, Amber ₹800–₹1,200, Red > ₹1,200 | `#kpi-cpl` |
| 5 | Fill Rate (Cumulative) | Percentage | (Cumulative enrolled since Sep / Season target) × 100 | Green ≥ on-track (monthly milestone), Amber within 5% of milestone, Red > 5% below | `#kpi-fill-rate` |
| 6 | MoM Growth % | Percentage | (This month conversions − Last month conversions) / Last month conversions × 100 | Green > 0%, Red ≤ 0% | `#kpi-mom-growth` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/analytics/mis-report/kpis/?month={month}"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Current Month MIS** — The active month's report in standard format
2. **Exception Report** — Red-flagged items requiring Board attention
3. **Historical Browser** — Archive of all previous MIS reports
4. **Schedule & Distribution** — Auto-generation schedule, recipient list, delivery log
5. **Template Configuration** — Define which sections, metrics, and formats appear in the MIS

### 5.2 Tab 1: Current Month MIS

The core MIS report rendered as a structured document (scrollable, printable) with the following fixed sections:

#### 5.2.1 Section A: Month Summary Dashboard

Top-of-report KPI panel (6 metrics with month value, previous month, same month last year, variance indicators):

| Metric | This Month | Previous Month | MoM Change | Same Month Last Year | YoY Change |
|---|---|---|---|---|---|
| New Leads | 4,850 | 4,120 | +17.7% ▲ | 3,940 | +23.1% ▲ |
| Conversions (New Enrollments) | 1,420 | 1,180 | +20.3% ▲ | 1,050 | +35.2% ▲ |
| Conversion Rate | 29.3% | 28.6% | +0.7% ▲ | 26.6% | +2.7% ▲ |
| Marketing Spend | ₹28,50,000 | ₹26,00,000 | +9.6% ▲ | ₹24,00,000 | +18.8% ▲ |
| CPL | ₹588 | ₹631 | −6.8% ▼ | ₹609 | −3.4% ▼ |
| CPA | ₹2,007 | ₹2,203 | −8.9% ▼ | ₹2,286 | −12.2% ▼ |
| Cumulative Fill Rate | 72.4% | 64.7% | +7.7% ▲ | 61.2% | +11.2% ▲ |
| Seats Remaining | 5,091 | 6,511 | — | 7,182 | — |

**Traffic light system:** Each MoM and YoY cell colour-coded: Green = improvement, Red = deterioration, Grey = neutral

#### 5.2.2 Section B: Branch-wise Monthly Performance

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Leads | Integer | Yes | New leads this month |
| Conversions | Integer | Yes | New enrollments this month |
| Conv. Rate | Percentage | Yes | — |
| Cumulative Enrolled | Integer | Yes | Since season start |
| Season Target | Integer | No | — |
| Fill Rate % | Progress bar | Yes | Cumulative enrolled / Season target |
| On Track? | Badge | Yes | On Track (green) / At Risk (amber) / Behind (red) — compared to monthly milestone |
| Spend (₹) | Amount | Yes | Branch-level spend this month |
| CPL (₹) | Amount | Yes | — |
| MoM Lead Change | Percentage | Yes | vs previous month |

**Summary row:** Group totals
**Conditional formatting:** Rows with fill rate > 5% below monthly milestone highlighted with red left-border

#### 5.2.3 Section C: Channel Performance This Month

| Source | Leads | Conv. | Conv. Rate | Spend (₹) | CPL (₹) | CPA (₹) | MoM Leads | MoM ROI |
|---|---|---|---|---|---|---|---|---|
| Newspaper / Print | 1,200 | 380 | 31.7% | 9,50,000 | 792 | 2,500 | +8% | −3% |
| Digital Ads | 1,450 | 340 | 23.4% | 7,00,000 | 483 | 2,059 | +22% | +15% |
| WhatsApp / SMS | 680 | 240 | 35.3% | 1,20,000 | 176 | 500 | +12% | +5% |
| Walk-in (Direct) | 520 | 220 | 42.3% | — | — | — | +5% | — |
| Referral | 480 | 140 | 29.2% | 30,000 | 63 | 214 | +30% | +20% |
| Open Day / Events | 320 | 60 | 18.8% | 4,50,000 | 1,406 | 7,500 | +45% | −10% |
| Telecalling | 200 | 40 | 20.0% | 6,00,000 | 3,000 | 15,000 | −5% | −8% |

#### 5.2.4 Section D: Spend vs Budget This Month

| Category | Monthly Budget (₹) | Actual Spend (₹) | Variance (₹) | Variance % | Status |
|---|---|---|---|---|---|
| Newspaper & Print | 10,00,000 | 9,50,000 | −50,000 | −5.0% | Under budget |
| Digital Ads | 6,67,000 | 7,00,000 | +33,000 | +4.9% | Slight over |
| WhatsApp / SMS | 1,25,000 | 1,20,000 | −5,000 | −4.0% | Under budget |
| Outdoor / BTL | 3,75,000 | 3,80,000 | +5,000 | +1.3% | On budget |
| Events & Open Days | 2,50,000 | 4,50,000 | +2,00,000 | +80.0% | Over budget ⚠️ |
| Other | 2,00,000 | 2,50,000 | +50,000 | +25.0% | Over budget |
| **TOTAL** | **26,17,000** | **28,50,000** | **+2,33,000** | **+8.9%** | **Over budget** |

#### 5.2.5 Section E: Lead Funnel This Month

```
New Leads:            4,850  ████████████████████████████████████████  100%
Contacted:            4,320  ███████████████████████████████████████   89.1%
Counselling Booked:   2,840  ██████████████████████████               58.6%
Counselling Done:     2,210  █████████████████████                    45.6%
Application Filed:    1,820  ███████████████████                      37.5%
Offer Made:           1,620  █████████████████                        33.4%
Fee Paid (Enrolled):  1,420  ██████████████                           29.3%
```

**Drop-off analysis:** Largest drop = Contacted → Counselling Booked (30.5% lost). Action: Improve telecaller follow-up scripts; introduce automated WhatsApp counselling booking link.

#### 5.2.6 Section F: Pending Actions

Actionable items surfaced from the month's data:

| # | Action Item | Owner | Branch | Deadline | Status |
|---|---|---|---|---|---|
| 1 | Mehdipatnam fill rate at 58% — deploy additional telecaller | Campaign Mgr (119) | Mehdipatnam | 10 Mar 2026 | Pending |
| 2 | Events budget exceeded by 80% — seek G4 approval for reallocation | Data Analyst (132) | Group HQ | 05 Mar 2026 | Pending |
| 3 | Referral leads up 30% — extend referral bonus programme through April | Campaign Mgr (119) | All | 15 Mar 2026 | Pending |
| 4 | Digital CPL improved — consider shifting ₹2L from print to digital next month | Data Analyst (132) | Group HQ | 01 Apr 2026 | Draft |

### 5.3 Tab 2: Exception Report

Auto-flagged items requiring Board attention. Pulled from current month's data using configurable thresholds.

**Exception categories:**

| # | Exception Type | Threshold | Current Status | Affected | Severity |
|---|---|---|---|---|---|
| 1 | Branch below fill milestone | Fill rate > 5% below monthly target | Mehdipatnam (58%), Dilsukhnagar (69%) | 2 branches | Critical |
| 2 | Channel ROI deteriorating | MoM ROI drop > 10% | Events & Open Days (−10%), Telecalling (−8%) | 2 channels | Warning |
| 3 | Budget overrun | Monthly spend > 110% of budget | Events & Open Days (+80%) | 1 category | Critical |
| 4 | Conversion rate drop | MoM conversion rate drop > 3% | — (none this month) | 0 | Clear |
| 5 | Lead volume decline | MoM leads drop > 10% | Telecalling (−5%) | 1 channel | Watch |
| 6 | CPL spike | CPL > 150% of 3-month average | — (none this month) | 0 | Clear |

**Exception detail (expandable per row):**
- What happened (auto-generated narrative)
- Root cause (analyst's assessment — editable)
- Recommended action (analyst's recommendation — editable)
- CEO decision (G4/G5 input — dropdown: Acknowledge / Action Required / Defer to Season Report)

### 5.4 Tab 3: Historical Browser

**Filter bar:** Month/Year · Status (Published/Draft) · Search by keyword

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Month | Text | Yes | "March 2026" |
| Status | Badge | Yes | Published / Draft / Archived |
| Generated On | Datetime | Yes | Auto-generation timestamp |
| Reviewed By | Text | Yes | Analyst who reviewed |
| Approved By | Text | Yes | G4/G5 who approved (if applicable) |
| Distributed On | Datetime | Yes | When emailed to stakeholders |
| Recipients | Integer | No | Number of email recipients |
| Exceptions | Integer | Yes | Number of red-flagged exceptions |
| Actions | Buttons | No | [View] [Download PDF] [Compare] |

**Default sort:** Month DESC (most recent first)
**Pagination:** Server-side · 12/page (1 year per page)

**Compare feature:** Select 2 months → side-by-side comparison view (same format, metrics from both months in adjacent columns).

### 5.5 Tab 4: Schedule & Distribution

#### 5.5.1 Auto-Generation Schedule

| Setting | Value | Configurable By |
|---|---|---|
| Generation day | 1st of each month | G4+ |
| Generation time | 05:30 IST | G4+ |
| Data cutoff | Last day of previous month, 23:59 IST | System (fixed) |
| Review deadline | 3rd of each month (auto-reminder to role 132) | G4+ |
| Distribution day | 5th of each month (after review) | G4+ |
| Fallback | If 1st is a holiday, generate on next working day | System |

#### 5.5.2 Distribution List

| Recipient | Email | Role | Sections Received | Format |
|---|---|---|---|---|
| Anil Kumar (CEO) | ceo@sunrise.edu | G4 | Full report | PDF + Email summary |
| Priya Venkatesh (Data Analyst) | priya@sunrise.edu | 132 | Full report | PDF |
| Ramesh Venkataraman (Campaign Mgr) | ramesh@sunrise.edu | 119 | Full report | PDF |
| [Each Branch Principal] | principal-{branch}@sunrise.edu | G3 | Branch-specific extract | PDF |
| CFO | cfo@sunrise.edu | G4 | Sections A + D (financial) | PDF |

#### 5.5.3 Delivery Log

| Month | Scheduled | Generated | Reviewed | Distributed | Delivery Status |
|---|---|---|---|---|---|
| Mar 2026 | 01 Mar 05:30 | 01 Mar 05:32 ✅ | Pending | Pending | Awaiting review |
| Feb 2026 | 01 Feb 05:30 | 01 Feb 05:31 ✅ | 02 Feb 14:20 ✅ | 05 Feb 06:00 ✅ | All delivered (8/8) |
| Jan 2026 | 01 Jan 05:30 | 02 Jan 05:30 ✅ (holiday fallback) | 03 Jan 11:45 ✅ | 05 Jan 06:00 ✅ | All delivered (8/8) |

### 5.6 Tab 5: Template Configuration

**Purpose:** Define and version the MIS report template. Changes require G4/G5 approval.

**Template sections (toggle on/off, reorder):**
- ☑ Section A: Month Summary Dashboard (locked — always included)
- ☑ Section B: Branch-wise Performance
- ☑ Section C: Channel Performance
- ☑ Section D: Spend vs Budget
- ☑ Section E: Lead Funnel
- ☑ Section F: Pending Actions
- ☐ Section G: Telecaller Productivity (optional — for large groups with 5+ telecallers)
- ☐ Section H: Content Performance (optional — creative asset engagement)
- ☐ Section I: Competitor Intelligence Summary (optional — pulls from O-38)

**Threshold configuration (for exception reporting):**

| Exception | Default Threshold | Custom Threshold | Last Changed |
|---|---|---|---|
| Branch below fill milestone | > 5% below target | Configurable | — |
| Channel ROI deterioration | > 10% MoM drop | Configurable | — |
| Budget overrun | > 10% of monthly budget | Configurable | — |
| Conversion rate drop | > 3% MoM drop | Configurable | — |
| Lead volume decline | > 10% MoM drop | Configurable | — |
| CPL spike | > 150% of 3-month avg | Configurable | — |

**Template version history:**

| Version | Date | Changed By | Change Summary | Status |
|---|---|---|---|---|
| 1.0 | 01 Sep 2025 | Priya Venkatesh | Initial template — 6 sections | Active |
| 1.1 | 15 Nov 2025 | Priya Venkatesh | Added Section G (Telecaller Productivity) | Active |
| 1.2 | 01 Jan 2026 | Priya Venkatesh | Added competitor intelligence summary | Pending Approval |

---

## 6. Drawers & Modals

### 6.1 Modal: `mis-configuration` (640px)

- **Title:** "MIS Report Configuration"
- **Tabs:** Sections · Metrics · Thresholds · Branding
- **Sections tab:**
  - Toggle on/off report sections (checkboxes)
  - Drag-reorder sections
  - Per section: title (editable), included metrics (multi-select from available metrics)
- **Metrics tab:**
  - Define which KPIs appear in Section A dashboard
  - Custom calculated metrics (formula builder — select from available fields)
  - Decimal places, currency formatting, percentage formatting
- **Thresholds tab:**
  - Configure exception trigger thresholds (per exception type)
  - Severity levels: Critical / Warning / Watch
  - Notification rules: who gets notified when exceptions are triggered
- **Branding tab:**
  - Report header: group logo upload, header text
  - Report footer: confidentiality notice, page numbering style
  - Colour scheme: Primary colour for headers and charts
- **Buttons:** Cancel · Save Draft · Submit for Approval (G4)
- **Access:** Role 132 or G4+

### 6.2 Modal: `schedule-configuration` (560px)

- **Title:** "MIS Auto-Generation & Distribution Schedule"
- **Fields:**
  - **Generation schedule:**
    - Day of month (integer, 1–28, required — avoid 29–31 for February safety)
    - Time (time, required — default 05:30 IST)
    - Holiday handling (dropdown): Next working day / Same day regardless / Skip month
  - **Review workflow:**
    - Auto-assign reviewer (dropdown from role 132 users)
    - Review deadline (integer — days after generation, default 2)
    - Reminder (toggle — send reminder to reviewer if not reviewed by deadline)
  - **Distribution schedule:**
    - Distribution day (integer — days after generation, default 4)
    - Distribution time (time, default 06:00 IST)
    - Auto-distribute after approval (toggle) — if G4 approves before distribution day, send immediately
    - Manual distribution only (toggle) — disable auto-distribution
  - **Recipients:**
    - Add recipient (name, email, role, sections to include, format)
    - Remove recipient
    - Test email (send test MIS to single recipient)
- **Buttons:** Cancel · Save Schedule
- **Access:** G4+

### 6.3 Drawer: `historical-mis-viewer` (720px, right-slide)

- **Title:** "MIS Report — [Month Year]"
- **Content:** Full rendered MIS report for the selected month (same format as Tab 1, but read-only with historical data)
- **Comparison mode:** Toggle — show side-by-side with another month (split view)
- **Metadata bar:** Generated on [date] · Reviewed by [name] on [date] · Distributed to [N] recipients on [date]
- **Annotations:** Historical annotations shown inline with report sections
- **Footer:** [Download PDF] [Compare with Another Month] [Close]
- **Access:** G1+

### 6.4 Modal: `custom-date-range` (480px)

- **Title:** "Custom Date Range Report"
- **Purpose:** Generate an ad-hoc MIS report for a non-standard date range (e.g., "15 Jan – 15 Feb" for a specific campaign period or Board meeting preparation).
- **Fields:**
  - Start date (date, required)
  - End date (date, required)
  - Report title (text — defaults to "Marketing MIS: [Start] to [End]")
  - Sections to include (checkboxes — same as template)
  - Comparison period (toggle): Compare with equivalent period last year?
- **Validation:** Date range must be ≤ 90 days; for longer periods use Season Report (O-39)
- **Buttons:** Cancel · Generate Report
- **Access:** Role 132 or G4+

### 6.5 Modal: `exception-action` (480px)

- **Title:** "Exception Action — [Exception Description]"
- **Read-only:** Exception type, threshold, current value, affected branch/channel
- **Fields:**
  - Root cause assessment (textarea, required — analyst fills)
  - Recommended action (textarea, required)
  - Assigned to (dropdown — Campaign Manager, Branch Principal, etc.)
  - Deadline (date)
  - CEO decision (dropdown, G4/G5 only): Acknowledge / Action Required / Defer / Override Threshold
  - CEO notes (textarea, G4/G5 only)
- **Buttons:** Cancel · Save Assessment · Submit to CEO (for analyst) · Approve Action (for G4/G5)
- **Access:** Role 132 for assessment; G4/G5 for decision

### 6.6 Modal: `month-comparison` (720px)

- **Title:** "Compare MIS Reports"
- **Fields:**
  - Month 1 (dropdown, required — e.g., "March 2026")
  - Month 2 (dropdown, required — e.g., "February 2026" or "March 2025")
- **Layout:** Side-by-side tables — Section A (dashboard) from both months with delta column
- **Delta highlighting:** Green = improvement, Red = deterioration (auto-calculated)
- **Buttons:** Close · Export Comparison
- **Access:** G1+

---

## 7. Charts

### 7.1 Monthly KPI Dashboard (Mini Charts)

| Property | Value |
|---|---|
| Chart type | Sparkline mini charts (Chart.js 4.x) — one per KPI card |
| Title | "[Metric] — Last 6 Months" |
| Data | Per KPI: 6-month trailing values rendered as mini line/bar within the KPI card |
| Colour | Line colour matches KPI card accent; fill area at 10% opacity |
| Size | 120px × 40px per sparkline (embedded in KPI card) |
| API | `GET /api/v1/group/{id}/marketing/analytics/mis-report/kpis/?months=6` (returns trailing 6-month series) |

### 7.2 Branch Heatmap

| Property | Value |
|---|---|
| Chart type | Heatmap / Matrix (Chart.js 4.x with chartjs-chart-matrix plugin) |
| Title | "Branch × Month Fill Rate Heatmap — Current Season" |
| Data | Rows = branches; Columns = months (Sep–current); Cell = fill rate as of that month |
| Colour | Green (≥ milestone) → Yellow (within 5%) → Red (> 5% below milestone) |
| Tooltip | "[Branch] in [Month]: [X]% filled ([N] enrolled / [M] target)" |
| API | `GET /api/v1/group/{id}/marketing/analytics/mis-report/charts/branch-heatmap/` |

### 7.3 Spend vs Budget Bar

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Spend vs Budget by Category — [Month]" |
| Data | X-axis = budget category; Bar 1 = budgeted; Bar 2 = actual |
| Colour | Budget = `#94A3B8` grey, Actual = `#10B981` green (red if > 110% of budget) |
| Tooltip | "[Category]: Budget ₹[X], Actual ₹[Y] ([Z]% variance)" |
| API | `GET /api/v1/group/{id}/marketing/analytics/mis-report/charts/spend-vs-budget/` |

### 7.4 Lead Funnel Horizontal Bar

| Property | Value |
|---|---|
| Chart type | Horizontal bar / Funnel (Chart.js 4.x) |
| Title | "Lead Funnel — [Month]" |
| Data | Stages: New Leads → Contacted → Counselling Booked → Counselling Done → Application → Offer → Enrolled |
| Colour | Progressive from `#3B82F6` (widest) to `#10B981` (narrowest) |
| Annotations | Drop-off % between each stage shown as labels |
| Tooltip | "[Stage]: [N] leads ([X]% of total, [Y]% drop from previous stage)" |
| API | `GET /api/v1/group/{id}/marketing/analytics/mis-report/charts/lead-funnel/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| MIS auto-generated | "MIS report for [Month] auto-generated — ready for review" | Info | 4s |
| MIS reviewed | "MIS report for [Month] reviewed and marked ready" | Success | 3s |
| MIS approved | "MIS report for [Month] approved by [Name] — scheduled for distribution" | Success | 4s |
| MIS distributed | "MIS report emailed to [N] recipients" | Success | 4s |
| Distribution failed | "MIS distribution failed for [N] recipients — check email addresses" | Error | 6s |
| Schedule saved | "MIS auto-generation schedule updated — next: [Date] at [Time]" | Success | 3s |
| Template saved | "MIS template changes saved — pending G4 approval" | Success | 3s |
| Template approved | "MIS template v[X] approved — effective from next generation" | Success | 4s |
| Exception flagged | "[N] exceptions detected in [Month] MIS — review required" | Warning | 5s |
| Exception resolved | "Exception '[Type]' resolved — action by [Owner]" | Success | 3s |
| Custom report generated | "Custom MIS report generated for [Start] to [End]" | Success | 4s |
| Annotation added | "Annotation added to Section [X] of [Month] MIS" | Success | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No MIS reports generated | 📊 | "No MIS Reports" | "Configure the MIS template and schedule to start auto-generating monthly reports." | Configure Template |
| Current month not generated | 📅 | "Report Not Yet Generated" | "The MIS report for [Month] has not been generated. Auto-generation is scheduled for [Date]." | Generate Now |
| No exceptions this month | ✅ | "No Exceptions" | "All metrics are within acceptable thresholds this month. No action items." | — |
| No historical reports | 📁 | "No Historical Reports" | "MIS history will appear here after the first report is generated and distributed." | — |
| No distribution recipients | 📧 | "No Recipients Configured" | "Add recipients to the MIS distribution list for automatic monthly delivery." | Configure Recipients |
| No data for month | ⏳ | "No Data Available" | "Marketing data for [Month] is not yet available. Data syncs from source pages on the 1st." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer (with sparkline placeholders) + report section skeletons |
| Month switch | Full content skeleton with KPI shimmer |
| Tab switch | Content skeleton |
| MIS auto-generation | Progress bar: "Generating MIS... Section [N] of [M]" |
| Branch heatmap | Grid skeleton with cell placeholders |
| Historical MIS drawer | 720px skeleton: header bar + report content placeholder |
| PDF export | Spinner: "Generating PDF..." |
| Email distribution | Spinner: "Sending to [N] recipients..." with progress |
| Template config modal | Form skeleton with tab navigation |
| Comparison modal | Split-panel skeleton (2 columns) |
| Chart load | Grey canvas placeholder |
| Exception report | Table skeleton (6 rows) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/` | G1+ | Get current month MIS report |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/?month={YYYY-MM}` | G1+ | Get specific month MIS |
| POST | `/api/v1/group/{id}/marketing/analytics/mis-report/generate/` | G1+ | Trigger manual MIS generation |
| PATCH | `/api/v1/group/{id}/marketing/analytics/mis-report/{report_id}/review/` | G1+ | Mark report as reviewed |
| PATCH | `/api/v1/group/{id}/marketing/analytics/mis-report/{report_id}/approve/` | G4+ | Approve for distribution |
| POST | `/api/v1/group/{id}/marketing/analytics/mis-report/{report_id}/distribute/` | G4+ | Distribute to recipients |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/history/` | G1+ | List all historical MIS reports |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/history/{report_id}/` | G1+ | View specific historical MIS |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/compare/` | G1+ | Compare two months (query: month1, month2) |
| POST | `/api/v1/group/{id}/marketing/analytics/mis-report/custom/` | G1+ | Generate custom date range report |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/exceptions/` | G1+ | List exceptions for current month |
| PUT | `/api/v1/group/{id}/marketing/analytics/mis-report/exceptions/{exc_id}/` | G1+ | Update exception assessment |
| PATCH | `/api/v1/group/{id}/marketing/analytics/mis-report/exceptions/{exc_id}/decide/` | G4+ | CEO decision on exception |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/template/` | G1+ | Get current MIS template configuration |
| PUT | `/api/v1/group/{id}/marketing/analytics/mis-report/template/` | G1+ | Update template (creates new version, pending approval) |
| PATCH | `/api/v1/group/{id}/marketing/analytics/mis-report/template/approve/` | G4+ | Approve template change |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/template/history/` | G1+ | Template version history |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/schedule/` | G1+ | Get schedule configuration |
| PUT | `/api/v1/group/{id}/marketing/analytics/mis-report/schedule/` | G4+ | Update schedule |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/distribution/` | G1+ | Get distribution list |
| PUT | `/api/v1/group/{id}/marketing/analytics/mis-report/distribution/` | G4+ | Update distribution list |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/distribution/log/` | G1+ | Distribution delivery log |
| POST | `/api/v1/group/{id}/marketing/analytics/mis-report/annotations/` | G1+ | Add annotation to report section |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/annotations/` | G1+ | List annotations |
| POST | `/api/v1/group/{id}/marketing/analytics/mis-report/export/pdf/` | G1+ | Export as PDF |
| POST | `/api/v1/group/{id}/marketing/analytics/mis-report/export/excel/` | G1+ | Export as Excel |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/kpis/` | G1+ | KPI values (supports ?months=N for trailing series) |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/charts/branch-heatmap/` | G1+ | Branch heatmap data |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/charts/spend-vs-budget/` | G1+ | Spend vs budget chart data |
| GET | `/api/v1/group/{id}/marketing/analytics/mis-report/charts/lead-funnel/` | G1+ | Lead funnel chart data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../mis-report/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Month switch | Month dropdown | `hx-get=".../mis-report/?month={YYYY-MM}"` | `#mis-content` | `innerHTML` | Full content reload |
| Tab switch | Tab click | `hx-get` with tab param | `#mis-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Generate report | Generate button | `hx-post=".../mis-report/generate/"` | `#generate-progress` | `innerHTML` | Progress bar with polling |
| Review mark | Review button | `hx-patch=".../mis-report/{id}/review/"` | `#report-status` | `innerHTML` | Status badge update |
| Approve report | Approve button | `hx-patch=".../mis-report/{id}/approve/"` | `#report-status` | `innerHTML` | Status badge update + toast |
| Distribute | Distribute button | `hx-post=".../mis-report/{id}/distribute/"` | `#distribute-result` | `innerHTML` | Progress spinner |
| Historical MIS drawer | History row click | `hx-get=".../mis-report/history/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Exception action | Exception row click | `hx-get=".../mis-report/exceptions/{id}/"` | `#exception-modal` | `innerHTML` | Modal with assessment form |
| Exception decide | CEO decision form | `hx-patch=".../mis-report/exceptions/{id}/decide/"` | `#exc-status-{id}` | `innerHTML` | Inline badge update |
| Template save | Config form submit | `hx-put=".../mis-report/template/"` | `#template-result` | `innerHTML` | Toast + version badge |
| Schedule save | Schedule form submit | `hx-put=".../mis-report/schedule/"` | `#schedule-result` | `innerHTML` | Toast confirmation |
| Chart load | Tab/section visible | `hx-get=".../mis-report/charts/..."` | `#chart-{name}` | `innerHTML` | `hx-trigger="intersect once"` |
| Add annotation | Annotation form | `hx-post=".../mis-report/annotations/"` | `#annotation-list` | `beforeend` | Appends to section |
| Export PDF | Export button | `hx-post=".../mis-report/export/pdf/"` | `#export-result` | `innerHTML` | Download trigger |
| Month comparison | Comparison form | `hx-get=".../mis-report/compare/?m1=...&m2=..."` | `#comparison-content` | `innerHTML` | Side-by-side render |
| Custom report | Custom form submit | `hx-post=".../mis-report/custom/"` | `#custom-result` | `innerHTML` | Generate + render |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
