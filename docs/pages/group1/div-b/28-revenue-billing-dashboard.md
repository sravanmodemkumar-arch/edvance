# Page 28 — Revenue & Billing Dashboard

**URL:** `/portal/product/revenue/`
**Permission:** `product.view_revenue_dashboard`
**Priority:** P1
**Roles:** PM Platform, CEO/CXO (read-only), Finance Team

---

## Purpose

Central financial visibility and analytics dashboard for the SRAV platform business. Provides PM Platform and leadership with real-time and historical views of revenue performance: MRR, ARR, churn, plan distribution, add-on revenue, GST compliance, and cohort revenue retention. While the Plan Config page (page 04) handles pricing setup and the institutional subscription workflows handle individual billing, this page aggregates all financial signals into actionable business intelligence.

Core responsibilities:
- Track Monthly Recurring Revenue (MRR) and Annual Recurring Revenue (ARR) across all plan tiers
- Measure subscriber churn (institutions cancelling or downgrading) and expansion (upgrading)
- Analyse revenue by institution type, plan tier, geographic region, and acquisition channel
- Track add-on revenue (extra storage, bulk SMS credits, custom branding, API access)
- Monitor payment health: collections, outstanding dues, refund rates
- Provide GST compliance reporting for India tax obligations (GST 18% on SaaS)
- Cohort revenue retention analysis: what % of revenue from a signup cohort is retained after N months
- Forecast revenue based on current MRR trends and pipeline

**Scale:**
- 1,950+ active subscriber institutions
- 4 plan tiers × 4 institution types = 16 plan variants
- Monthly billing cycle + annual prepay options
- All amounts in INR; Decimal(28,2) arithmetic (no float)
- GST registration: GSTIN held by SRAV Technologies Pvt Ltd
- Payment gateways: Razorpay (primary) + manual NEFT/RTGS for Enterprise

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Revenue & Billing Dashboard"          Period ▾  [Export]      │
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 8 cards (auto-refresh every 300s)                  │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  Overview · MRR/ARR · Churn & Expansion · Plan Distribution     │
│  Collections · Add-ons · GST Compliance · Cohort Analysis       │
│  Forecast · Audit Log                                           │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Period Selector

Global period selector in header applies to all tabs:
- Last 7 days
- Last 30 days (default)
- Last 90 days
- Last 12 months
- Current month to date
- Custom date range
- Year to date (Apr 1 – present, Indian financial year)

---

## KPI Strip — 8 Cards (auto-refresh every 300s)

| # | Label | Value | Colour | Delta | Click Action |
|---|---|---|---|---|---|
| 1 | MRR | Current month's recurring revenue (INR, excl. GST) | — | vs last month (% and absolute) | Opens MRR/ARR tab |
| 2 | ARR | MRR × 12 (annualised) | — | vs last month | Opens MRR/ARR tab |
| 3 | Active Subscribers | Institutions with active subscription | — | vs last month (+/-) | Opens Plan Distribution |
| 4 | Net MRR Growth | New MRR − Churned MRR + Expansion MRR | Green if positive · Red if negative | — | Opens Churn & Expansion |
| 5 | Gross Churn Rate | % of MRR lost to cancellation/downgrade this month | Red if > 3% · Amber 1–3% | vs last month | Opens Churn & Expansion |
| 6 | Collections (MTD) | Payments received this month (month to date) | — | vs last month | Opens Collections |
| 7 | Outstanding Dues | Unpaid invoices overdue | Red if > ₹5L | — | Opens Collections |
| 8 | GST Collected (MTD) | GST portion of all invoices this month | — | — | Opens GST Compliance |

KPI values animate count-up on page load. Large monetary values formatted as ₹X.XL (lakhs) or ₹X.XCr (crores) for readability.

---

## Tab 1 — Overview

High-level executive view of the business's financial health.

### MRR Waterfall Chart

Shows how MRR changed month-over-month. Waterfall (bridge) chart:

```
Starting MRR: ₹48.2L
+ New MRR (new subscriptions):     +₹3.4L  (green bar)
+ Expansion MRR (upgrades):        +₹1.2L  (blue bar)
− Churn MRR (cancellations):       −₹1.8L  (red bar)
− Contraction MRR (downgrades):    −₹0.4L  (orange bar)
= Ending MRR: ₹50.6L
```

Net MRR growth: +₹2.4L (+5.0%) shown prominently.

### Revenue by Plan Tier (Donut Chart)

| Plan | Institutions | MRR | % of Total |
|---|---|---|---|
| Starter | 820 | ₹8.2L | 16.2% |
| Standard | 640 | ₹16.0L | 31.6% |
| Professional | 380 | ₹19.0L | 37.5% |
| Enterprise | 110 | ₹7.4L | 14.7% |

### Revenue by Institution Type (Bar Chart)

| Type | Institutions | MRR | Avg MRR per Institution |
|---|---|---|---|
| School | 980 | ₹14.7L | ₹1,500 |
| College | 760 | ₹17.1L | ₹2,250 |
| Coaching Centre | 95 | ₹12.4L | ₹13,050 |
| Group | 115 | ₹6.4L | ₹5,565 |

### Revenue Geographic Distribution

Choropleth map of India: states coloured by MRR contribution. Hover shows state name + MRR + institution count. Top 5 states by revenue shown as separate bar chart alongside map.

| State | Institutions | MRR | % |
|---|---|---|---|
| Telangana | 280 | ₹9.2L | 18.2% |
| Andhra Pradesh | 240 | ₹7.8L | 15.4% |
| Maharashtra | 200 | ₹6.4L | 12.6% |
| Karnataka | 180 | ₹5.1L | 10.1% |
| Tamil Nadu | 160 | ₹4.8L | 9.5% |

---

## Tab 2 — MRR / ARR

Detailed Monthly and Annual Recurring Revenue analysis.

### MRR Trend Chart (12 months)

Line chart: monthly MRR over last 12 months. X-axis: months. Y-axis: INR (lakhs). Breakdowns:
- Total MRR (primary line)
- Breakdown by plan tier (toggle: stacked area chart or multi-line)
- Toggle: Include add-on revenue / Exclude add-on revenue

Reference line: ARR target (if set by PM Platform in settings).

### MRR Components Table (month-by-month)

| Month | Starting MRR | New MRR | Expansion | Churn | Contraction | Ending MRR | Net Growth |
|---|---|---|---|---|---|---|---|
| Mar 2026 | ₹48.2L | ₹3.4L | ₹1.2L | ₹1.8L | ₹0.4L | ₹50.6L | +5.0% |
| Feb 2026 | ₹45.8L | ₹4.1L | ₹0.9L | ₹2.1L | ₹0.5L | ₹48.2L | +5.2% |
| Jan 2026 | ₹43.2L | ₹3.8L | ₹1.4L | ₹2.2L | ₹0.4L | ₹45.8L | +6.0% |

### ARR Milestones

Milestone tracker showing progress toward ARR goals:
- Current ARR: ₹6.07Cr (₹50.6L × 12)
- Next milestone: ₹6.5Cr ARR (₹54.2L MRR needed)
- Progress bar: 93% to next milestone
- At current growth rate: estimated to reach ₹6.5Cr in 1.2 months

### Revenue per Institution Analysis

| Metric | Value |
|---|---|
| Average Revenue per User (ARPU) | ₹2,595 per institution per month |
| Median ARPU | ₹2,000 |
| Highest ARPU | ₹45,000 (large coaching centre on Enterprise custom plan) |
| Lowest paying (active) | ₹500 (grandfathered Starter plan) |

---

## Tab 3 — Churn & Expansion

Tracks revenue lost (churn, contraction) and gained (new, expansion) at institution level.

### Churn Summary Cards (4 cards)

| Card | Value |
|---|---|
| Gross Churn Rate | % of MRR lost to cancellations this month |
| Net Churn Rate | Gross churn minus expansion MRR (can be negative = net revenue retention > 100%) |
| Institutions Churned | Count of institutions that cancelled this month |
| Net Revenue Retention (NRR) | Revenue from last month's institutions this month / last month's revenue (>100% = good) |

### Churn Analysis Table

All institutions that churned (cancelled or downgraded) in the selected period:

| Institution | Type | Plan (was) | Plan (now) | Churn Type | MRR Lost | Churn Date | Last Active | Exit Reason |
|---|---|---|---|---|---|---|---|---|
| ABC Academy | Coaching | Professional | Cancelled | Full Churn | ₹8,500 | 15 Mar | 28 Feb | "Switching to competitor" |
| City School | School | Standard | Starter | Downgrade | ₹1,200 | 10 Mar | 8 Mar | "Exam season over, don't need full features" |

**Exit Reasons (categorical analysis):**
Exit reason collected via automated exit survey (required step before cancellation flow). Categories:
- Pricing too high
- Switching to competitor
- No longer need platform (exam season ended)
- Technical issues
- Poor support experience
- School/institution closed
- Unpaid (auto-churn after 60 days overdue)

Donut chart showing distribution of exit reasons for the period.

### Expansion Analysis Table

Institutions that upgraded in the period:

| Institution | Type | Plan (was) | Plan (now) | Expansion Type | MRR Added | Upgrade Date |
|---|---|---|---|---|---|---|
| Bright Future Coaching | Coaching | Standard | Professional | Upgrade | ₹4,500 | 5 Mar |
| Govt. Engineering College | College | Professional | Enterprise | Upgrade | ₹12,000 | 12 Mar |

### Churn Risk Indicators

Institutions flagged at risk of churning (pre-emptive CSM intervention targets):

| Institution | Plan | Churn Risk Score | Risk Factors | Days Until Renewal | CSM |
|---|---|---|---|---|---|
| Sunrise Institute | Standard | 82% (High) | No login 21 days · Only 2 of 8 features used · Support ticket unresolved | 14 days | Unassigned |
| Modern School | Starter | 68% (Medium) | Domain coverage < 30% · No exam in 45 days | 28 days | Riya Kapoor |

**Churn Risk Score** (0–100): ML-derived from usage signals:
- Days since last login (high weight)
- Feature adoption: % of plan features used
- Exam frequency in last 30 days
- Support ticket sentiment (if open)
- Payment history
- Domain coverage %

Score ≥ 70: High risk (red); 40–69: Medium (amber); < 40: Low (green).

"Assign CSM" button on each row. "Send Win-back Email" button: opens email compose with win-back template pre-loaded.

---

## Tab 4 — Plan Distribution

Analysis of subscriber distribution across plan tiers.

### Plan Distribution Table

| Plan | Institutions | % of Total | MRR | % of Revenue | ARPU | Avg Contract Length |
|---|---|---|---|---|---|---|
| Starter | 820 | 42% | ₹8.2L | 16% | ₹1,000 | Monthly |
| Standard | 640 | 33% | ₹16.0L | 32% | ₹2,500 | Monthly / Annual |
| Professional | 380 | 19% | ₹19.0L | 38% | ₹5,000 | Monthly / Annual |
| Enterprise | 110 | 6% | ₹7.4L | 14% | ₹6,727 | Annual |

### Plan Upgrade/Downgrade Flow Chart

Sankey diagram showing plan transitions in the last 3 months:
- How many moved Starter → Standard, Standard → Professional, etc.
- How many moved downwards
- How many stayed on the same plan

### Annual vs Monthly Billing Distribution

| Plan | Monthly Billing | Annual Billing | Annual Billing % |
|---|---|---|---|
| Starter | 780 | 40 | 4.9% |
| Standard | 520 | 120 | 18.8% |
| Professional | 260 | 120 | 31.6% |
| Enterprise | 0 | 110 | 100% |

Annual billing institutions shown separately: they pay a full year upfront (often at 10–20% discount). Revenue from annual plans deferred over 12 months for MRR calculation.

### Plan Feature Adoption

For each plan tier: which features are being actively used vs dormant. Identifies upsell opportunities.

| Feature | Standard Usage (%) | Notes |
|---|---|---|
| Analytics Deep Dive | 45% | Underused — upsell to Professional |
| API Access | 8% | Very low — upsell trigger |
| Custom Branding | 62% | Strong adoption |
| Multiple Admin Roles | 55% | — |

Low feature adoption on a higher plan is a downgrade risk; low feature availability on a lower plan is an upgrade trigger.

---

## Tab 5 — Collections

Billing, payments, and outstanding dues management.

### Collections Summary Cards (4 cards)

| Card | Value |
|---|---|
| Collected (MTD) | Total payments received this month |
| Outstanding (Current) | Invoices due but not yet overdue |
| Overdue | Invoices past due date |
| Refunds (MTD) | Refunds processed this month |

### Invoice Table

| Column | Detail |
|---|---|
| Invoice ID | INV-NNNNNN |
| Institution | Name + plan |
| Invoice Date | Date |
| Due Date | Date |
| Amount (excl. GST) | INR |
| GST Amount | INR |
| Total Amount | INR |
| Status | Paid · Pending · Overdue · Cancelled · Refunded |
| Payment Method | Razorpay / NEFT / RTGS / Cheque |
| Actions | View · Download PDF · Send Reminder · Mark Paid (manual) |

**Filters:** Status / Institution / Date range / Plan tier / Payment method

**Overdue Escalation Rules:**
- 7 days overdue: automated reminder email + in-app notice to institution admin
- 15 days overdue: CSM assigned (if not already) and manual call flag
- 30 days overdue: access restricted to read-only
- 60 days overdue: account suspended; auto-churn

### Invoice Detail Drawer (640px)

**Header:** Invoice ID · Institution · Date · Status
**Tab 1 — Invoice Details:**
- Line items (plan subscription + any add-ons)
- GST breakdown (CGST/SGST for intra-state; IGST for inter-state)
- Payment received: timestamp, method, transaction ID
- Razorpay order ID (for online payments)
- GSTIN of institution (shown on invoice)

**Tab 2 — Communication Log:**
All emails/calls related to this invoice: automated reminders + manual CSM notes

**Tab 3 — Adjustments:**
Any credit notes or adjustments applied to this invoice (e.g. pro-rata refund for mid-month cancellation).

### Payment Health Dashboard

- **Collection rate:** % of invoiced amount collected (target > 95%)
- **Days Sales Outstanding (DSO):** avg days between invoice issue and payment receipt (target < 15 days)
- **Failed payment rate:** % of Razorpay attempts that failed (target < 3%)
- **Recurring payment success:** for auto-renewing subscriptions, % successfully charged on renewal date

---

## Tab 6 — Add-ons

Revenue from add-on services beyond the base subscription.

### Add-on Revenue Summary

| Add-on | Institutions Using | MRR | Avg per Institution |
|---|---|---|---|
| Extra Storage (+10GB) | 240 | ₹1.2L | ₹500 |
| Bulk SMS Credits (top-up) | 310 | ₹0.93L | ₹300 |
| Custom Domain | 180 | ₹0.36L | ₹200 |
| API Access Tier | 85 | ₹0.85L | ₹1,000 |
| White-label Branding | 45 | ₹1.35L | ₹3,000 |
| Proctoring Premium | 95 | ₹1.9L | ₹2,000 |
| Dedicated Account Manager | 22 | ₹1.1L | ₹5,000 |
| **Total Add-on MRR** | — | **₹7.69L** | — |

Add-on MRR shown separately and as % of total MRR in overview metrics.

### Add-on Adoption Trend

Line chart: monthly add-on revenue per add-on type over last 12 months. Shows which add-ons are growing.

### Upsell Opportunities

Institutions with high usage signals for an add-on they haven't purchased:

| Institution | Potential Add-on | Signal | MRR Opportunity |
|---|---|---|---|
| Learning Tree Academy | API Access | 3 API calls failed due to rate limit this week | ₹1,000/mo |
| National College | Extra Storage | At 87% of storage quota | ₹500/mo |

---

## Tab 7 — GST Compliance

India-specific tax compliance view. SRAV is a GST-registered entity (GSTIN: [masked]).

### GST Summary (current financial year)

| Month | Taxable Revenue | GST Rate | GST Amount | GSTR-1 Filed | GSTR-3B Filed |
|---|---|---|---|---|---|
| Mar 2026 | ₹50.6L | 18% | ₹9.1L | Pending | Pending |
| Feb 2026 | ₹48.2L | 18% | ₹8.7L | ✓ Filed | ✓ Filed |
| Jan 2026 | ₹45.8L | 18% | ₹8.2L | ✓ Filed | ✓ Filed |

### GST Breakdown by Transaction Type

| Type | Amount | CGST | SGST | IGST |
|---|---|---|---|---|
| SaaS Subscription (intra-state — Telangana) | ₹28.4L | ₹2.55L | ₹2.55L | — |
| SaaS Subscription (inter-state) | ₹22.2L | — | — | ₹4.0L |
| Total GST Collected | ₹50.6L | ₹2.55L | ₹2.55L | ₹4.0L |

CGST + SGST applies when SRAV's place of supply = customer's state (both in Telangana).
IGST applies for interstate transactions (customer in other state).

### B2B Invoice Register

Table of all B2B invoices (institutions with GSTIN provided). Required for GSTR-1 filing.

| Invoice | Date | Institution | GSTIN | Taxable Amt | GST | Total | Supply Type |
|---|---|---|---|---|---|---|---|
| INV-10482 | 1 Mar | Bright Future Coaching | 36AAACB1234K1Z5 | ₹8,500 | ₹1,530 | ₹10,030 | Intra-state |
| INV-10483 | 1 Mar | Modern College | 27AAACM5678L1Z2 | ₹5,000 | ₹900 | ₹5,900 | Inter-state |

**"Export for GSTR-1"** button: downloads JSON format compatible with GST portal upload.
**"Export for Tally"** button: exports in Tally XML format for accounting team.
**"Download All Invoices"** button: ZIP of all PDF invoices for selected month.

### HSN/SAC Code

SRAV's services fall under SAC code 998315 (IT Infrastructure Provisioning Services) or 998314 (IT Support Services). SAC code shown on all invoices. PM Platform can configure which SAC code applies per service type.

---

## Tab 8 — Cohort Analysis

Revenue retention by signup cohort — the gold standard metric for SaaS business health.

### Cohort Revenue Retention Table

How much of the revenue from each signup cohort is retained after N months:

| Cohort | Month 0 MRR | Month 1 | Month 2 | Month 3 | Month 6 | Month 12 | Month 24 |
|---|---|---|---|---|---|---|---|
| Jan 2025 | ₹3.4L | 92% | 88% | 86% | 82% | 78% | 71% |
| Feb 2025 | ₹2.8L | 94% | 90% | 88% | 84% | 79% | — |
| Mar 2025 | ₹3.1L | 91% | 87% | 84% | 80% | 76% | — |
| Jan 2026 | ₹4.2L | 95% | — | — | — | — | — |

Colour coding: ≥ 80% green · 60–79% amber · < 60% red.

Net Revenue Retention > 100% is possible if expansion (upgrades) exceeds churn within a cohort.

### Cohort Chart (Visual)

Heat map table as above but with colour gradient fill. Standard SaaS cohort chart format.

### Key Cohort Metrics

| Metric | Value |
|---|---|
| Avg Month-12 Revenue Retention | 78% |
| Best Cohort (Month-12) | Sep 2025: 83% |
| Worst Cohort (Month-12) | Jun 2025: 71% |
| Net Revenue Retention (trailing 12 months) | 108% (expansion > churn) |

NRR > 100% is the "holy grail" of SaaS — existing customers are spending more over time, meaning growth doesn't depend solely on new customer acquisition.

---

## Tab 9 — Forecast

Revenue forecasting based on current trends and pipeline.

### Revenue Forecast Summary

| Metric | This Month (actual) | Next Month (forecast) | Quarter End (forecast) | Year End (forecast) |
|---|---|---|---|---|
| MRR | ₹50.6L | ₹53.1L | ₹57.8L | ₹72.4L |
| ARR | ₹6.07Cr | ₹6.37Cr | ₹6.94Cr | ₹8.69Cr |
| New MRR expected | ₹3.4L | ₹3.6L | — | — |
| Expected churn | ₹1.8L | ₹1.9L | — | — |

### Forecast Methodology

Forecast uses a combination of:
- **Historical trend:** CAGR of MRR over last 6 months extrapolated forward
- **Pipeline input:** Known Enterprise deals in sales pipeline (PM Platform manually enters pipeline value)
- **Seasonality adjustment:** Academic calendar seasonality (Jan–Apr = peak signups; May–Jun = low; Jul–Sep = medium peak)
- **Churn forecast:** Based on institutions at high churn risk (risk score ≥ 70) — forecast assumes 60% of high-risk institutions churn

### Forecast Assumptions Panel

PM Platform can adjust forecast inputs:
- Expected new MRR from pipeline (manual input)
- Churn rate assumption (default: trailing 3-month avg)
- Expansion rate assumption
- Seasonality factor override

### Scenario Analysis

Three scenarios:
- **Conservative (P10):** Low growth, high churn — shows downside
- **Base Case (P50):** Current trend continuation
- **Optimistic (P90):** High growth, low churn — shows upside

Each scenario shows MRR trajectory for next 12 months as a fan chart (coloured bands).

---

## Tab 10 — Audit Log

Every change to revenue-impacting configurations and manual actions is logged.

| Timestamp | Actor | Action | Detail |
|---|---|---|---|
| 20 Mar 2026 | Finance Admin | Invoice marked paid | INV-10482 marked as NEFT received ₹10,030 |
| 19 Mar 2026 | PM Platform | Credit note issued | CN-1024 applied to INV-10478 (pro-rata refund) |
| 18 Mar 2026 | PM Platform | Plan changed | Modern School downgraded Standard → Starter |
| 15 Mar 2026 | Razorpay webhook | Payment received | INV-10480 paid ₹5,900 via Razorpay TXN_abc123 |

All financial actions immutable. CSV export.

---

## Access Control

This page contains sensitive financial data. Access is restricted:

| Role | Access |
|---|---|
| PM Platform | Full access (all tabs, all actions) |
| CEO / CXO | Read-only access (all tabs, no actions) |
| Finance Team | Collections tab + GST tab full access; Overview and MRR/ARR read-only |
| PM Institution Portal | Churn & Expansion tab read-only (to understand at-risk institutions) |
| CSM Lead | Churn & Expansion + Collections (overdue only) read-only |
| All others | No access |

2FA required for:
- Marking an invoice as paid manually
- Issuing a credit note
- Modifying a subscription plan in this dashboard (billing management)

---

## Integration Points

| Page | Integration |
|---|---|
| Page 04 — Plan Config | Plan pricing is configured in Plan Config. This page shows the revenue outcomes of those pricing decisions. |
| Page 14 — Portal Feature Config | Feature flags are linked to plan tiers. This page shows which plan tiers are generating the most revenue and should drive feature investment. |
| Page 17 — Onboarding Workflow | Institutions that complete onboarding faster tend to have higher 12-month retention. Cohort analysis here can be segmented by onboarding completion time. |
| Page 18 — Notification Templates | Fee reminder and subscription expiring notification templates are managed in notification manager. This page shows their effectiveness (overdue rate, collection rate). |

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| MRR waterfall chart | Bridges New + Expansion − Churn − Contraction | Shows the composition of MRR change — not just the direction but why it changed |
| Decimal(28,2) arithmetic | Never float | Indian tax law requires exact paise-level precision; float rounding errors would cause GST filing discrepancies |
| NRR tracking | Net Revenue Retention as KPI | NRR > 100% means growth is net-negative churn even without new customers — the strongest SaaS health metric |
| Churn risk score | ML-derived from usage signals | Proactive churn intervention before institutions cancel is more effective than win-back after |
| Exit survey required | Mandatory before cancellation | Without exit reason data, product improvements cannot be targeted to the right churn causes |
| GST compliance tab | Built into revenue dashboard | Finance team needs GST data in the same tool as revenue data; separate export workflows cause errors |
| Cohort analysis | Standard SaaS heat map | Industry-standard format; immediately comparable to SaaS benchmarks |
| Annual billing deferred over 12 months | MRR calculation rule | Annual prepay inflates a single month's cash; MRR must reflect recurring revenue only |
| Forecast fan chart | 3 scenarios (P10/P50/P90) | Point forecasts create false precision; range shows uncertainty and enables planning for downside |
| Financial year as April–March | Indian FY | SRAV's tax year follows Indian financial year; all YTD metrics reset April 1 |
| 2FA for manual payment actions | Security requirement | Revenue data manipulation is a fraud risk; 2FA gates on financial actions are mandatory |
| Role-based financial visibility | PM/CEO/Finance/CSM layers | Not all roles need full financial visibility; granular access prevents internal data leakage |
