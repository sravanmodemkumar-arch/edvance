# P-03 — Financial Audit Manager

> **URL:** `/group/audit/financial/`
> **File:** `p-03-financial-audit-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Internal Audit Head (Role 121, G1) — primary operator

---

## 1. Purpose

The Financial Audit Manager is where the Internal Audit Head and team conduct, track, and report on financial audits across all branches. In Indian education, financial irregularities are the single biggest governance risk — unauthorized fee concessions to "connected" families, inflated vendor invoices, petty cash siphoning, scholarship diversion, duplicate fee receipts, and off-book cash collections. For a large group collecting ₹50–500 Cr in fees annually across 20–50 branches, even a 2% leakage means ₹1–10 Cr lost per year.

The problems this page solves:

1. **Fee collection reconciliation:** Each branch collects fees via multiple channels — cash, cheque, UPI, Razorpay, bank transfer. Monthly reconciliation must verify: total collected matches total deposited, receipt numbers are sequential (no gaps = no deleted receipts), online payment gateway settlements match bank credits, and refunds are authorized. Without systematic audit, a branch accountant can delete a cash receipt and pocket the money.

2. **Vendor payment verification:** Education groups spend ₹10–50L annually per branch on vendors — printing (brochures, flex banners), transport (bus maintenance, fuel), mess (food suppliers), stationery, lab equipment, sports goods. Common frauds: inflated invoices, fictitious vendors, payment without delivery, and kickbacks. The audit must verify: vendor exists (GSTIN check), delivery receipt matches invoice, PO matches invoice, and payment was authorized.

3. **Petty cash audit:** Each branch maintains petty cash of ₹10,000–₹50,000 for small daily expenses. Common abuse: missing vouchers, back-dated entries, personal expenses charged, and round-number withdrawals without bills. The audit verifies petty cash register against bank withdrawals and supporting vouchers.

4. **Scholarship and waiver audit:** Groups disburse ₹10L–₹2Cr in scholarships and fee waivers. Audit verifies: scholarship criteria were met (academic score, income proof), approval chain was followed (not just principal's discretion), disbursement reached the student (not adjusted against non-existent fees), and RTE quota students are genuine (not seats being misused).

5. **Budget compliance:** Each branch has an approved annual budget. The audit checks: actual spend vs budgeted amounts, unbudgeted expenditures (who approved?), capital expenditure authorization, and inter-branch fund transfers.

**Scale:** 5–50 branches · ₹50–500 Cr annual fee collection · 500–5,000 vendor invoices/branch/year · Quarterly financial audits per branch · 50–200 audit findings/year (financial)

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Internal Audit Head | 121 | G1 | Full — create audits, review reports, sign-off | Primary financial auditor |
| Group Inspection Officer | 123 | G3 | Execute — conduct audit, fill checklists, upload evidence | Field execution |
| Group Compliance Data Analyst | 127 | G1 | Read — financial audit data for analytics | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read + CAPA — create corrective actions from findings | CAPA management |
| Group CFO / Finance Director | 30 | G1 | Read — audit results, financial findings | Cross-division read from Div D |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve audit reports | Final sign-off |
| Group Internal Auditor (Div D) | 36 | G1 | Read — cross-reference with Div D audits | Coordination |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Division P reads Division D financial data but cannot modify it. This separation is enforced at the API level.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Financial Audit Manager
```

### 3.2 Page Header
```
Financial Audit Manager                                [+ New Financial Audit]  [Sampling Tool]  [Export]
Audit Head — K. Ramachandra Rao
Sunrise Education Group · FY 2025-26 · 28 branches · 84 financial audits planned · 52 completed
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Audits Completed | Integer / Planned | Completed financial audits / total planned this FY | Green ≥ 85%, Amber 70–84%, Red < 70% | `#kpi-completed` |
| 2 | Open Findings | Integer | COUNT(findings) WHERE audit_type = 'financial' AND status != 'closed' | Red > 30, Amber 10–30, Green < 10 | `#kpi-findings` |
| 3 | Critical Findings | Integer | COUNT(findings) WHERE severity = 'S1' AND audit_type = 'financial' | Red > 0, Green = 0 | `#kpi-critical` |
| 4 | Total Discrepancy (₹) | Amount | SUM(discrepancy_amount) across all open financial findings | Red > ₹5L, Amber ₹1–5L, Green < ₹1L | `#kpi-discrepancy` |
| 5 | Fee Reconciliation Rate | Percentage | Branches where collection = deposit (within ₹1000 tolerance) / total × 100 | Green ≥ 95%, Amber 85–94%, Red < 85% | `#kpi-reconciliation` |
| 6 | Avg Audit Score | Percentage | AVG(audit_score) across completed financial audits | Green ≥ 85%, Amber 70–84%, Red < 70% | `#kpi-avg-score` |

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Audit List** — All financial audits with status
2. **Fee Reconciliation** — Branch-wise fee collection vs deposit
3. **Vendor Payment Audit** — Vendor invoice verification
4. **Petty Cash Audit** — Branch petty cash register audit
5. **Scholarship & Waiver Audit** — Scholarship and concession verification

### 5.2 Tab 1: Audit List

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Audit ID | Text (link) | Yes | Auto-generated: FA-2026-001 |
| Branch | Text | Yes | — |
| Audit Period | Date range | Yes | Quarter or month being audited |
| Scheduled Date | Date | Yes | When audit is/was conducted |
| Auditor(s) | Text | No | Assigned team |
| Focus Areas | Badges | No | Fee Recon / Vendor / Petty Cash / Scholarship / Budget |
| Status | Badge | Yes | Scheduled / In Progress / Report Pending / Under Review / Signed Off |
| Findings | Integer | Yes | Total findings count |
| Critical | Integer | Yes | S1 findings |
| Discrepancy (₹) | Amount | Yes | Total monetary discrepancy found |
| Score | Percentage | Yes | Audit score (0–100%) |
| Actions | Buttons | No | [View] [Start] [Submit Report] |

### 5.3 Tab 2: Fee Reconciliation

**Branch-wise fee reconciliation matrix:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Period | Text | Yes | Month or quarter |
| Total Collected (System) | ₹ Amount | Yes | From EduForge fee module (Div D) |
| Total Deposited (Bank) | ₹ Amount | Yes | From bank statement upload |
| Difference | ₹ Amount | Yes | Collected − Deposited |
| Status | Badge | Yes | ✅ Matched / ⚠️ Variance / 🔴 Mismatch |
| Cash Collected | ₹ Amount | Yes | Cash component |
| Online Collected | ₹ Amount | Yes | Razorpay/UPI component |
| Cheque Collected | ₹ Amount | Yes | Cheque component |
| Receipt Gap Check | Badge | Yes | ✅ Sequential / 🔴 Gaps found (N missing) |
| Refunds | ₹ Amount | Yes | Total refunds issued |
| Refund Authorization | Badge | Yes | ✅ All authorized / 🔴 Unauthorized found |
| Last Reconciled | Date | Yes | — |

**Variance threshold:** ≤ ₹1,000 = Auto-approved; ₹1,001–₹10,000 = Needs review; > ₹10,000 = Critical finding auto-generated

### 5.4 Tab 3: Vendor Payment Audit

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Vendor Name | Text | Yes | — |
| GSTIN Valid? | Badge | Yes | ✅ Valid / 🔴 Invalid / ⚠️ Not registered |
| Invoice No. | Text | Yes | — |
| Invoice Amount (₹) | Amount | Yes | — |
| PO Exists? | Badge | Yes | ✅ Yes / 🔴 No PO |
| Delivery Receipt? | Badge | Yes | ✅ Yes / 🔴 Missing |
| Amount Match? | Badge | Yes | ✅ Matches PO / ⚠️ Variance / 🔴 Overcharge |
| Payment Date | Date | Yes | — |
| Authorization | Badge | Yes | ✅ Authorized / 🔴 Unauthorized |
| TDS Deducted? | Badge | Yes | ✅ Yes / 🔴 Missing (if applicable) |
| Audit Status | Badge | Yes | Verified / Flagged / Under Investigation |

### 5.5 Tab 4: Petty Cash Audit

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Period | Text | Yes | Month |
| Opening Balance | ₹ Amount | Yes | — |
| Replenishments | ₹ Amount | Yes | Cash withdrawn from bank |
| Total Expenditure | ₹ Amount | Yes | Per register |
| Closing Balance | ₹ Amount | Yes | — |
| Physical Count | ₹ Amount | Yes | Actual cash counted by auditor |
| Discrepancy | ₹ Amount | Yes | Closing balance − physical count |
| Vouchers Complete? | Badge | Yes | ✅ All vouched / ⚠️ Missing N vouchers |
| Bills Attached? | Badge | Yes | ✅ All / ⚠️ Missing N |
| Round-Number Entries | Integer | Yes | Count of suspiciously round amounts (₹1000, ₹5000) |
| Status | Badge | Yes | ✅ Clean / ⚠️ Minor issues / 🔴 Discrepancy |

### 5.6 Tab 5: Scholarship & Waiver Audit

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Student Name | Text | Yes | — |
| Scholarship Type | Badge | Yes | Merit / Need / RTE / Sports / Staff Child / Management Quota |
| Original Fee (₹) | Amount | Yes | Before concession |
| Discount (₹) | Amount | Yes | Concession amount |
| Discount % | Percentage | Yes | — |
| Eligibility Proof | Badge | Yes | ✅ Verified / 🔴 Missing / ⚠️ Insufficient |
| Approval Chain | Badge | Yes | ✅ Complete / 🔴 Missing approvals |
| Authorized By | Text | Yes | Who approved the concession |
| > 25% Discount? | Badge | Yes | Requires CEO approval per policy |
| CEO Approval? | Badge | Yes | ✅ Yes / 🔴 Missing (if > 25%) |
| Audit Status | Badge | Yes | Verified / Flagged / Under Investigation |

---

## 6. Drawers & Modals

### 6.1 Modal: `create-financial-audit` (640px)

- **Title:** "New Financial Audit"
- **Fields:**
  - Branch (dropdown, required)
  - Audit period (date range — quarter/month being audited)
  - Scheduled date (date picker — when audit will be conducted)
  - Focus areas (checkboxes, at least one required):
    - Fee collection reconciliation
    - Vendor payment verification
    - Petty cash audit
    - Scholarship and waiver audit
    - Budget compliance
    - Capital expenditure review
    - Inter-branch fund transfers
  - Auditor(s) (multi-select)
  - Sampling method (dropdown): Full / Random 20% / Stratified / Risk-based
  - Sample size guidance (auto-calculated based on transaction volume)
  - Priority (radio): Routine / High / Critical
  - Special instructions (textarea)
  - Linked to previous finding? (toggle + finding ID)
- **Buttons:** Cancel · Save as Draft · Schedule
- **Validation:** Auditor available on date; no duplicate audit in same period for same branch
- **Access:** Role 121, G4+

### 6.2 Drawer: `financial-audit-detail` (780px, right-slide)

- **Title:** "Financial Audit — [Branch] · [Period]"
- **Tabs:** Overview · Fee Recon · Vendors · Petty Cash · Scholarships · Findings · Report
- **Overview tab:** Audit status, team, dates, scope, progress (checklist completion %)
- **Fee Recon tab:** Collection vs deposit reconciliation for this branch/period
- **Vendors tab:** Vendor invoices sampled and verified for this audit
- **Petty Cash tab:** Petty cash count and voucher verification
- **Scholarships tab:** Scholarship/waiver cases reviewed
- **Findings tab:** All findings from this audit with severity and CAPA status
- **Report tab:** Audit report — executive summary, detailed observations, recommendations, auditor sign-off
- **Footer:** [Add Finding] [Submit Report] [Request Sign-off] [Export PDF]
- **Access:** G1+ (Division P roles), CFO (30)

### 6.3 Modal: `add-finding` (560px)

- **Title:** "Add Financial Finding"
- **Fields:**
  - Finding category (dropdown): Fee Discrepancy / Vendor Irregularity / Petty Cash Shortage / Unauthorized Concession / Budget Overrun / Missing Documentation / Process Violation / Other
  - Severity (radio): S1 (Critical — fraud/loss > ₹1L) / S2 (Major — non-compliance) / S3 (Minor — process gap) / S4 (Observation)
  - Description (textarea, required — detailed finding)
  - Monetary impact (₹, optional — amount of discrepancy or potential loss)
  - Evidence (file upload — photos, documents, screenshots)
  - Branch personnel involved (text)
  - Root cause (dropdown): Intentional Fraud / Process Gap / Negligence / System Error / Training Gap / Other
  - Recommended action (textarea)
  - CAPA required? (toggle — auto-yes for S1 and S2)
  - CAPA assigned to (dropdown — branch principal, accountant, or specific person)
  - CAPA due date (date picker — default: S1 = 7 days, S2 = 14 days, S3 = 30 days, S4 = 60 days)
- **Buttons:** Cancel · Save Finding
- **Access:** Role 121, 123

### 6.4 Modal: `sampling-tool` (560px)

- **Title:** "Audit Sampling Calculator"
- **Purpose:** Determine how many transactions to sample for statistical significance
- **Fields:**
  - Total transactions in period (auto-filled from Division D data)
  - Confidence level (dropdown): 90% / 95% / 99%
  - Margin of error (dropdown): 1% / 3% / 5% / 10%
  - Expected error rate (slider): 1–20%
- **Output:**
  - Recommended sample size: N transactions
  - Sampling method: Random / Stratified (high-value + random)
  - High-value threshold: All transactions > ₹X must be included
- **Buttons:** Close · Apply to Audit
- **Access:** Role 121, 123

### 6.5 Modal: `bank-statement-upload` (480px)

- **Title:** "Upload Bank Statement — [Branch]"
- **Fields:**
  - Branch (pre-selected or dropdown)
  - Bank account (dropdown — branch accounts)
  - Period (month)
  - File (CSV/Excel/PDF upload)
  - File format (dropdown): SBI / HDFC / ICICI / Axis / Kotak / Other (maps columns)
- **Processing:** Auto-parses credits and maps to fee receipts
- **Output:** Reconciliation summary — matched, unmatched, extra credits
- **Buttons:** Cancel · Upload & Reconcile
- **Access:** Role 121, 123

---

## 7. Charts

### 7.1 Branch Financial Health (Bubble Chart)

| Property | Value |
|---|---|
| Chart type | Bubble (Chart.js 4.x) |
| Title | "Branch Financial Audit Health" |
| X-axis | Audit score (%) |
| Y-axis | Open findings count |
| Bubble size | Total discrepancy (₹) |
| Colour | Green (A grade) / Amber (B) / Red (C/D) |
| API | `GET /api/v1/group/{id}/audit/financial/analytics/branch-health/` |

### 7.2 Finding Category Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut |
| Title | "Financial Findings by Category" |
| Data | COUNT(findings) per category (Fee Discrepancy, Vendor, Petty Cash, etc.) |
| API | `GET /api/v1/group/{id}/audit/financial/analytics/finding-categories/` |

### 7.3 Fee Reconciliation Trend (Line)

| Property | Value |
|---|---|
| Chart type | Line |
| Title | "Fee Reconciliation — Monthly Variance Trend" |
| Data | Total variance (₹) across all branches per month |
| Threshold line | Red dashed line at ₹10,000 (critical threshold) |
| API | `GET /api/v1/group/{id}/audit/financial/analytics/reconciliation-trend/` |

### 7.4 Discrepancy by Branch (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Total Discrepancy by Branch — FY to Date" |
| Data | SUM(discrepancy_amount) per branch, sorted descending |
| Colour | Red for top 5, Amber for next 5, Green for rest |
| API | `GET /api/v1/group/{id}/audit/financial/analytics/discrepancy-by-branch/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit created | "Financial audit scheduled — [Branch], [Date]" | Success | 3s |
| Finding added | "Finding [ID] added — severity: [S1/S2/S3/S4]" | Success | 3s |
| Critical finding | "🔴 Critical finding (S1) added — auto-escalation to CEO triggered" | Error | 6s |
| Report submitted | "Audit report submitted for [Branch] — pending review" | Success | 3s |
| Report signed off | "Audit report signed off by [Name]" | Success | 4s |
| Bank statement uploaded | "Bank statement uploaded — reconciliation in progress" | Info | 3s |
| Reconciliation complete | "Reconciliation complete — [N] mismatches found" | Info | 4s |
| Discrepancy alert | "⚠️ Fee discrepancy > ₹10,000 at [Branch]" | Warning | 5s |
| CAPA created | "CAPA created for finding [ID] — assigned to [Person]" | Success | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No financial audits | 💰 | "No Financial Audits" | "Schedule your first financial audit to begin verifying branch finances." | New Financial Audit |
| No findings | ✅ | "No Financial Findings" | "No discrepancies found in completed audits. Excellent compliance!" | — |
| No bank statements | 🏦 | "No Bank Statements Uploaded" | "Upload bank statements to enable fee reconciliation." | Upload Statement |
| No vendor data | 📦 | "No Vendor Invoices to Audit" | "Vendor payment data will appear from Division D integration." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + tab content skeleton |
| Audit list | Table skeleton with 10 rows |
| Fee reconciliation matrix | Table skeleton with branch rows |
| Vendor payment table | Table skeleton with 20 rows |
| Audit detail drawer | 780px skeleton: 7 tabs |
| Bank statement reconciliation | Progress bar with step indicators |
| Chart load | Grey canvas placeholder |
| Sampling calculator | Form skeleton + output placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit/financial/` | G1+ | List all financial audits |
| GET | `/api/v1/group/{id}/audit/financial/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/audit/financial/{audit_id}/` | G1+ | Audit detail |
| POST | `/api/v1/group/{id}/audit/financial/` | 121, G4+ | Create financial audit |
| PUT | `/api/v1/group/{id}/audit/financial/{audit_id}/` | 121 | Update audit |
| PATCH | `/api/v1/group/{id}/audit/financial/{audit_id}/status/` | 121, 123 | Update status (in-progress, report-pending, etc.) |
| POST | `/api/v1/group/{id}/audit/financial/{audit_id}/findings/` | 121, 123 | Add finding |
| GET | `/api/v1/group/{id}/audit/financial/{audit_id}/findings/` | G1+ | List findings for this audit |
| POST | `/api/v1/group/{id}/audit/financial/{audit_id}/report/` | 121, 123 | Submit audit report |
| PATCH | `/api/v1/group/{id}/audit/financial/{audit_id}/signoff/` | G4+ | Sign off report |
| GET | `/api/v1/group/{id}/audit/financial/reconciliation/` | G1+ | Fee reconciliation matrix |
| POST | `/api/v1/group/{id}/audit/financial/reconciliation/upload/` | 121, 123 | Upload bank statement |
| GET | `/api/v1/group/{id}/audit/financial/vendors/` | G1+ | Vendor payment audit data |
| GET | `/api/v1/group/{id}/audit/financial/petty-cash/` | G1+ | Petty cash audit data |
| GET | `/api/v1/group/{id}/audit/financial/scholarships/` | G1+ | Scholarship/waiver audit data |
| GET | `/api/v1/group/{id}/audit/financial/sampling/` | G1+ | Sampling calculator |
| GET | `/api/v1/group/{id}/audit/financial/analytics/branch-health/` | G1+ | Branch health bubble chart |
| GET | `/api/v1/group/{id}/audit/financial/analytics/finding-categories/` | G1+ | Finding category donut |
| GET | `/api/v1/group/{id}/audit/financial/analytics/reconciliation-trend/` | G1+ | Reconciliation trend line |
| GET | `/api/v1/group/{id}/audit/financial/analytics/discrepancy-by-branch/` | G1+ | Discrepancy bar chart |
| GET | `/api/v1/group/{id}/audit/financial/export/` | G1+ | Export audit data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../financial/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#financial-content` | `innerHTML` | `hx-trigger="click"` |
| Audit detail drawer | Row click | `hx-get=".../financial/{id}/"` | `#right-drawer` | `innerHTML` | 780px drawer |
| Create audit | Form submit | `hx-post=".../financial/"` | `#create-result` | `innerHTML` | Toast + table refresh |
| Add finding | Form submit | `hx-post=".../financial/{id}/findings/"` | `#finding-result` | `innerHTML` | Toast |
| Submit report | Button click | `hx-post=".../financial/{id}/report/"` | `#report-status` | `innerHTML` | Toast + status update |
| Sign off | Button click | `hx-patch=".../financial/{id}/signoff/"` | `#signoff-status` | `innerHTML` | Toast |
| Upload bank statement | Form submit | `hx-post=".../reconciliation/upload/"` | `#upload-result` | `innerHTML` | Progress bar |
| Filter audit list | Filter change | `hx-get` with filters | `#audit-table` | `innerHTML` | `hx-trigger="change"` |
| Sampling calculator | Form change | `hx-get=".../sampling/?..."` | `#sampling-output` | `innerHTML` | Live calculation |
| Chart load | Tab shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |
| Pagination | Page click | `hx-get` with page param | `#table-body` | `innerHTML` | — |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
