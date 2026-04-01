# 05 — Group Scholarship Manager Dashboard

- **URL:** `/group/adm/scholarships/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Scholarship Manager (Role 27, G3)

---

## 1. Purpose

The Group Scholarship Manager Dashboard is the financial and governance centre for all scholarship and fee waiver activities across the group. This page covers the complete post-selection scholarship lifecycle: reviewing and approving recommendations from counsellors, tracking ongoing disbursements of merit and need-based awards, managing fee waivers, monitoring RTE (Right to Education) quota compliance, and following up on government scholarship scheme claims. The Scholarship Manager operates at the intersection of admissions and finance — decisions made on this page directly affect fee revenue and regulatory compliance.

The approval queue is the most critical section: recommendations from counsellors arrive here with student details, scheme type, score basis, and recommended award amount. The manager must approve, reject, or send back for clarification each recommendation within a defined SLA. The page surfaces days-pending prominently to prevent approvals from ageing beyond institutional policy limits. Bulk approval of clearly eligible merit candidates is supported to reduce manual effort during peak cycle periods.

RTE quota monitoring is a regulatory necessity. The RTE section shows each branch's mandated seats, current enrolled count, and documentation verification status — critical for audit readiness. Government scheme tracking (PMSS, state schemes) requires awareness of claim submission timelines and disbursement status, which the government scheme tracker surfaces without requiring the manager to log into multiple external portals. Together, these sections make this dashboard the definitive tool for ensuring that scholarship commitments made during admissions are honoured, accurately tracked, and compliantly reported throughout the academic year.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Manager | G3 | Full read + write + approve + reject | Primary owner of this page |
| Group Admissions Director | G3 | Read-only + override approval | Can override a rejection or force-approve |
| Group Scholarship Exam Manager | G3 | Read — Section 5.3 (Merit Tracker) + exam result linkage | Limited to merit scholarship context from exam results |
| Chief Academic Officer (CAO) | G3+ | Read-only (all sections) | View only; no actions |
| Chief Financial Officer (CFO) | G3+ | Read — Section 5.2 (Disbursement), Section 5.5 (Fee Waivers), Section 5.7 (Govt Schemes) | Finance-relevant sections only |

> **Enforcement:** All access control is enforced server-side in Django views using `@role_required` decorators and queryset-level filtering. No role checks are performed in client-side JavaScript. Users without the required role receive an HTTP 403 response.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarship Manager
```

### 3.2 Page Header
- **Title:** `Scholarship Manager Dashboard`
- **Subtitle:** `Group Admissions · Academic Year: [Year] · Current Cycle: [Cycle Name]`
- **Role Badge:** `Group Scholarship Manager`
- **Right-side controls:** `[+ New Scholarship Award]` `[Bulk Approve ▾]` `[Export Disbursement Report]`

### 3.3 Alert Banner
Displayed conditionally above the KPI bar. Triggers include:

| Condition | Banner Text | Severity |
|---|---|---|
| Approval pending > 5 days | "[N] scholarship recommendation(s) have been waiting for approval for more than 5 days." | Critical (red) |
| Fee waiver requests > 10 pending | "[N] fee waiver requests are pending review. Please action them." | Warning (amber) |
| RTE quota < 75% filled with < 30 days of cycle remaining | "RTE quota is at [X]% for [N] branch(es). Cycle closing in < 30 days." | Critical (red) |
| Government scheme claim deadline approaching | "Claim deadline for [Scheme Name] is [Date] — [N] students not yet claimed." | Warning (amber) |
| Scholarship renewal due this month | "[N] scholarship holders are due for renewal review this month." | Info (blue) |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Active Scholarships | Count of currently active scholarship awards (current year) | `scholarship_award` WHERE status = 'active' AND year = current | Blue (informational) | Opens merit + need tracker combined view |
| Pending Approvals | Count of recommendations with status = 'pending' | `scholarship_recommendation` WHERE status = 'pending' | Red if > 10; amber 1–10; green = 0 | Scrolls to Section 5.1 |
| Total Disbursed (₹) | Sum of scholarship amounts paid out this year | `scholarship_disbursement` WHERE year = current | Green (always — informational financial figure) | Opens Section 5.2 chart |
| Fee Waivers Pending | Count of fee waiver requests with status = 'pending' | `fee_waiver_request` WHERE status = 'pending' | Red if > 5; amber 1–5; green = 0 | Scrolls to Section 5.5 |
| RTE Seats Filled % | (RTE enrolled / RTE mandated) × 100 across all branches | `rte_enrollment` vs `rte_quota` | Green ≥ 90%; amber 50–89%; red < 50% | Scrolls to Section 5.6 |
| Renewals Due This Month | Scholarship holders with renewal date in current month | `scholarship_award` WHERE renewal_month = current | Amber if > 0; green = 0 | Opens renewal tracker filter |

**HTMX Refresh Pattern:**
```html
<div id="kpi-bar"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarships/kpis/"
     hx-trigger="load, every 5m"
     hx-target="#kpi-bar"
     hx-swap="innerHTML">
```

---

## 5. Sections

### 5.1 Scholarship Approval Queue

**Display:** Sortable, selectable table. Rows with `days_pending` > 5 are highlighted amber; > 10 days highlighted red. Supports checkbox-based bulk approve for clearly merit-eligible rows.

**Columns:** ☐ | Applicant Name | Branch | Stream | Scheme (Merit / Need-based / RTE / Government) | Basis | Recommended Amount (₹) | Recommended By | Days Pending | Action

**Actions per row:** `[Approve ✓]` | `[Reject ✗]` | `[View →]` opens scholarship-application-detail drawer.

**Bulk Actions (header bar):** `[Bulk Approve Selected]` | `[Bulk Reject Selected]` — with confirmation dialog.

**Filters:** Scheme type, Branch, Stream, Days Pending (Any / 3+ / 5+ / 10+), Recommended By (counsellor selector)

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="approval-queue"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarships/approval-queue/"
     hx-trigger="load, change from:#approval-filters"
     hx-target="#approval-queue"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: inbox checkmark. "No pending scholarship approvals. All recommendations have been reviewed."

---

### 5.2 Scholarship Disbursement Summary

**Display:** Chart.js 4.x grouped bar chart. X-axis = months of current year. Two bars per month: Disbursed (green) and Outstanding / Pending Disbursal (amber). A filter dropdown above the chart allows switching between All Schemes, Merit, Need-based, RTE, Government.

**Fields shown below chart (summary row):** Total Disbursed YTD (₹) | Total Outstanding (₹) | Number of Awards | Average Award (₹)

**Filters:** Scheme Type, Branch, Academic Year

**HTMX Pattern:**
```html
<div id="disbursement-chart"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarships/disbursement-summary/"
     hx-trigger="load, change from:#disbursement-filters"
     hx-target="#disbursement-chart"
     hx-swap="innerHTML">
```

**Empty State:** "No disbursement data available for the selected filters and year."

---

### 5.3 Merit Scholarship Tracker

**Display:** Sortable table. All students currently holding merit scholarships. Rows where renewal date is within 30 days are highlighted amber. Rows where current score has dropped below scholarship maintenance threshold are highlighted red with a warning icon.

**Columns:** Student Name | Branch | Stream | Exam Rank | Current Score (%) | Scholarship Amount (₹) | Award Date | Renewal Due | Status

**Status Badge Values:** Active (green) | Renewal Pending (amber) | Under Review (blue) | Revoked (red)

**Filters:** Branch, Stream, Renewal Due (Any / This Month / Overdue), Status, Rank range

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="merit-tracker"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarships/merit/"
     hx-trigger="load, change from:#merit-filters"
     hx-target="#merit-tracker"
     hx-swap="innerHTML">
```

**Empty State:** "No merit scholarship holders in the current year. Merit scholarships will appear here once awarded."

---

### 5.4 Need-Based Scholarship Tracker

**Display:** Sortable table. Students holding need-based scholarships. Income proof expiry highlighted if within 60 days.

**Columns:** Student Name | Branch | Stream | Income Proof Status (Verified / Expired / Pending) | Scheme Name | Amount (₹) | Award Date | Renewal Due | Action

**Actions per row:** `[View →]` opens scholarship-application-detail drawer.

**Filters:** Branch, Stream, Income Proof Status, Renewal Due (Any / This Month / Overdue), Scheme

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="need-tracker"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarships/need-based/"
     hx-trigger="load, change from:#need-filters"
     hx-target="#need-tracker"
     hx-swap="innerHTML">
```

**Empty State:** "No need-based scholarship holders on record. Awards will appear here once approved."

---

### 5.5 Fee Waiver Queue

**Display:** Sortable table. Pending fee waiver requests from branches. Rows > 3 days pending highlighted amber.

**Columns:** Student Name | Branch | Stream | Reason | Waiver Amount Requested (₹) | Requested By | Requested On | Days Pending | Action

**Actions per row:** `[Approve]` | `[Reject]` | `[View →]` opens waiver-approval-detail drawer.

**Filters:** Branch, Reason category, Days Pending (Any / 1+ / 3+ / 7+)

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="waiver-queue"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarships/fee-waivers/"
     hx-trigger="load, change from:#waiver-filters"
     hx-target="#waiver-queue"
     hx-swap="innerHTML">
```

**Empty State:** "No fee waiver requests pending. All submitted waivers have been reviewed."

---

### 5.6 RTE Quota Status

**Display:** Sortable table. One row per branch. Branches below 75% RTE fill are highlighted amber; below 50% highlighted red.

**Columns:** Branch | RTE Mandated Seats | Enrolled | Vacant | Documents Verified (count) | Documents Pending | Compliance % | Action

**Actions per row:** `[View →]` opens rte-student-detail drawer showing enrolled RTE students for that branch.

**Filters:** Branch, Compliance % range (All / Below 75% / Below 50%)

**HTMX Pattern:**
```html
<div id="rte-status"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarships/rte-quota/"
     hx-trigger="load"
     hx-target="#rte-status"
     hx-swap="innerHTML">
```

**Empty State:** "RTE quota data is not configured. Contact the Admissions Director to set RTE seat allocations per branch."

---

### 5.7 Government Scheme Tracker

**Display:** List of government scholarship schemes the group participates in (PMSS, NSP state scheme, minority welfare scheme, etc.). Each item shows scheme-level summary and a sub-table of enrolled students and their claim status.

**Fields per scheme item:** Scheme Name | Sponsoring Body | Enrolled Students | Claims Submitted | Disbursed (₹) | Pending Claim | Claim Deadline | Status Badge

**Status Badge Values:** On Track (green) | Deadline Approaching (amber) | Overdue (red) | Closed (muted)

**Filters:** Scheme name, Status, Branch, Disbursement status

**HTMX Pattern:**
```html
<div id="govt-scheme-tracker"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarships/govt-schemes/"
     hx-trigger="load"
     hx-target="#govt-scheme-tracker"
     hx-swap="innerHTML">
```

**Empty State:** "No government scholarship schemes are configured. Add schemes from Settings → Scholarship Schemes."

---

## 6. Drawers & Modals

### 6.1 Scholarship Application Detail Drawer
- **Width:** 640px
- **Trigger:** `[View →]` in Section 5.1, 5.3, or 5.4
- **Tabs:**
  - **Applicant Profile:** Student + parent details, class, branch, stream, income info (for need-based)
  - **Scheme Details:** Recommended scheme, basis, supporting documents (marks sheet, income certificate, etc.) with document preview links
  - **Counsellor Notes:** Counsellor's notes and recommendation rationale
  - **Decision:** Approve / Reject radio buttons, Award Amount field (editable for manager), Remarks field, `[Submit Decision]`
  - **Audit Trail:** History of actions taken on this application
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/scholarships/applications/{{ application_id }}/"`

### 6.2 Fee Waiver Approval Detail Drawer
- **Width:** 560px
- **Trigger:** `[View →]` in Section 5.5
- **Tabs:**
  - **Waiver Request:** Student profile, waiver reason, supporting documents, amount requested, requesting branch
  - **Decision:** Approve / Reject / Partial Approval (with custom amount field), Remarks, `[Submit Decision]`
  - **History:** Previous waiver requests from this student (if any)
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/scholarships/fee-waivers/{{ waiver_id }}/"`

### 6.3 RTE Student Detail Drawer
- **Width:** 640px
- **Trigger:** `[View →]` in Section 5.6
- **Tabs:**
  - **Enrolled RTE Students:** Table — Student name, class, enrollment date, income certificate status, caste certificate status, other documents
  - **Add RTE Student:** Form to manually register an RTE-qualifying student to the branch
  - **Document Tracker:** Status of each required RTE document per student — bulk `[Request Missing Docs]` action
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/scholarships/rte/{{ branch_id }}/"`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Scholarship approved | "Scholarship approved for [Student Name] — [Scheme] (₹[Amount])." | Success | 5s |
| Scholarship rejected | "Scholarship recommendation for [Student Name] has been rejected." | Info | 4s |
| Bulk approve completed | "[N] scholarship(s) approved successfully." | Success | 4s |
| Fee waiver approved | "Fee waiver of ₹[Amount] approved for [Student Name]." | Success | 4s |
| Fee waiver rejected | "Fee waiver request for [Student Name] has been rejected." | Info | 4s |
| Partial approval saved | "Partial approval of ₹[Amount] saved for [Student Name]." | Success | 4s |
| RTE student added | "[Student Name] added to RTE roster for [Branch]." | Success | 4s |
| Disbursement report export initiated | "Disbursement report export started. You will be notified when ready." | Info | 4s |
| Decision failed — missing documents | "Cannot approve: required documents are missing or unverified." | Error | 6s |
| Renewal review triggered | "Renewal review initiated for [Student Name]." | Info | 3s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No pending approvals | Inbox checkmark | "Approval Queue Clear" | "No scholarship recommendations are pending your review." | — |
| No active scholarships | Award ribbon icon | "No Active Scholarships" | "Approved scholarships will appear here once awarded." | `[+ New Scholarship Award]` |
| No fee waivers pending | Receipt checkmark | "Fee Waivers Up to Date" | "No fee waiver requests are pending review." | — |
| No RTE data configured | Shield icon | "RTE Data Not Set Up" | "Configure RTE seat quotas per branch to enable quota tracking." | `[Configure RTE Quotas]` |
| No government schemes | Document icon | "No Government Schemes" | "Add government scholarship schemes to begin tracking claims." | `[Add Scheme]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| KPI bar initial load / auto-refresh | Skeleton shimmer cards (6 cards) |
| Approval queue table load | Skeleton table rows (8 rows) |
| Disbursement chart load | Skeleton bar chart (12 bars, two per month) |
| Merit tracker table load | Skeleton table rows (6 rows) |
| Need-based tracker table load | Skeleton table rows (6 rows) |
| Fee waiver queue load | Skeleton table rows (5 rows) |
| RTE status table load | Skeleton table rows (5 rows) |
| Government scheme list load | Skeleton list items (3 items) |
| Drawer content load | Spinner overlay on drawer panel |
| Bulk approve action | Full-row spinner while processing |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Scholarship Manager | Admissions Director | Scholarship Exam Manager | CAO | CFO |
|---|---|---|---|---|---|
| KPI Summary Bar (all cards) | Visible | Visible | Merit card + Pending card only | Visible | Disbursed + Waivers cards only |
| Approval Queue (5.1) | Visible + actions | Read only + override | Hidden | Read only | Hidden |
| `[Approve ✓]` / `[Reject ✗]` buttons | Visible | Visible (override) | Hidden | Hidden | Hidden |
| `[Bulk Approve]` button | Visible | Hidden | Hidden | Hidden | Hidden |
| Disbursement Summary chart (5.2) | Visible | Read only | Hidden | Read only | Visible |
| Merit Scholarship Tracker (5.3) | Visible | Read only | Read only | Read only | Hidden |
| Need-based Tracker (5.4) | Visible | Read only | Hidden | Read only | Hidden |
| Fee Waiver Queue (5.5) | Visible + [Approve] [Reject] | Read only + override | Hidden | Read only | Read only |
| RTE Quota Status (5.6) | Visible + [View] | Read only | Hidden | Read only | Hidden |
| Government Scheme Tracker (5.7) | Visible | Read only | Hidden | Read only | Visible |
| `[+ New Scholarship Award]` button | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Export Disbursement Report]` button | Visible | Visible | Hidden | Visible | Visible |
| Scholarship Detail Drawer — Decision tab | Visible | Visible (override) | Hidden | Hidden | Hidden |
| Waiver Approval Drawer — Decision tab | Visible | Visible (override) | Hidden | Hidden | Hidden |
| RTE Detail Drawer — Add Student tab | Visible | Hidden | Hidden | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarships/kpis/` | JWT G3+ | Fetch all 6 KPI card values |
| GET | `/api/v1/group/{group_id}/adm/scholarships/approval-queue/` | JWT G3+ | Pending scholarship recommendations |
| POST | `/api/v1/group/{group_id}/adm/scholarships/applications/{application_id}/approve/` | JWT G3 | Approve scholarship recommendation |
| POST | `/api/v1/group/{group_id}/adm/scholarships/applications/{application_id}/reject/` | JWT G3 | Reject scholarship recommendation |
| POST | `/api/v1/group/{group_id}/adm/scholarships/bulk-approve/` | JWT G3 | Bulk approve selected recommendations |
| GET | `/api/v1/group/{group_id}/adm/scholarships/applications/{application_id}/` | JWT G3+ | Full scholarship application detail |
| GET | `/api/v1/group/{group_id}/adm/scholarships/disbursement-summary/` | JWT G3+ | Disbursement chart data |
| GET | `/api/v1/group/{group_id}/adm/scholarships/merit/` | JWT G3+ | Merit scholarship holders list |
| GET | `/api/v1/group/{group_id}/adm/scholarships/need-based/` | JWT G3+ | Need-based scholarship holders list |
| GET | `/api/v1/group/{group_id}/adm/scholarships/fee-waivers/` | JWT G3+ | Fee waiver requests (pending) |
| GET | `/api/v1/group/{group_id}/adm/scholarships/fee-waivers/{waiver_id}/` | JWT G3+ | Fee waiver detail for drawer |
| POST | `/api/v1/group/{group_id}/adm/scholarships/fee-waivers/{waiver_id}/approve/` | JWT G3 | Approve fee waiver |
| POST | `/api/v1/group/{group_id}/adm/scholarships/fee-waivers/{waiver_id}/reject/` | JWT G3 | Reject fee waiver |
| GET | `/api/v1/group/{group_id}/adm/scholarships/rte-quota/` | JWT G3+ | RTE quota status per branch |
| GET | `/api/v1/group/{group_id}/adm/scholarships/rte/{branch_id}/` | JWT G3+ | RTE student list for a branch |
| POST | `/api/v1/group/{group_id}/adm/scholarships/rte/{branch_id}/students/` | JWT G3 | Add RTE student to branch roster |
| GET | `/api/v1/group/{group_id}/adm/scholarships/govt-schemes/` | JWT G3+ | Government scheme tracker data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 5m` | GET `/api/v1/group/{{ group_id }}/adm/scholarships/kpis/` | `#kpi-bar` | `innerHTML` |
| Approval queue filter change | `change from:#approval-filters` | GET `/api/v1/group/{{ group_id }}/adm/scholarships/approval-queue/` | `#approval-queue` | `innerHTML` |
| Approve recommendation | `click from:#btn-approve-{{ id }}` | POST `/api/v1/group/{{ group_id }}/adm/scholarships/applications/{{ id }}/approve/` | `#approval-queue` | `innerHTML` |
| Reject recommendation | `click from:#btn-reject-{{ id }}` | POST `/api/v1/group/{{ group_id }}/adm/scholarships/applications/{{ id }}/reject/` | `#approval-queue` | `innerHTML` |
| Bulk approve submit | `click from:#btn-bulk-approve` | POST `/api/v1/group/{{ group_id }}/adm/scholarships/bulk-approve/` | `#approval-queue` | `innerHTML` |
| Open scholarship detail drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/scholarships/applications/{{ id }}/` | `#drawer-panel` | `innerHTML` |
| Disbursement chart filter change | `change from:#disbursement-filters` | GET `/api/v1/group/{{ group_id }}/adm/scholarships/disbursement-summary/` | `#disbursement-chart` | `innerHTML` |
| Merit tracker filter change | `change from:#merit-filters` | GET `/api/v1/group/{{ group_id }}/adm/scholarships/merit/` | `#merit-tracker` | `innerHTML` |
| Need-based tracker filter change | `change from:#need-filters` | GET `/api/v1/group/{{ group_id }}/adm/scholarships/need-based/` | `#need-tracker` | `innerHTML` |
| Approve fee waiver | `click from:#btn-waiver-approve` | POST `/api/v1/group/{{ group_id }}/adm/scholarships/fee-waivers/{{ id }}/approve/` | `#waiver-queue` | `innerHTML` |
| Reject fee waiver | `click from:#btn-waiver-reject` | POST `/api/v1/group/{{ group_id }}/adm/scholarships/fee-waivers/{{ id }}/reject/` | `#waiver-queue` | `innerHTML` |
| Open waiver detail drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/scholarships/fee-waivers/{{ id }}/` | `#drawer-panel` | `innerHTML` |
| RTE status load | `load` | GET `/api/v1/group/{{ group_id }}/adm/scholarships/rte-quota/` | `#rte-status` | `innerHTML` |
| Open RTE branch drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/scholarships/rte/{{ branch_id }}/` | `#drawer-panel` | `innerHTML` |
| Government scheme tracker load | `load` | GET `/api/v1/group/{{ group_id }}/adm/scholarships/govt-schemes/` | `#govt-scheme-tracker` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
