# [13] — Insurance Registry

> **URL:** `/group/legal/insurance/`
> **File:** `n-13-insurance-registry.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Insurance Coordinator (Role 129, G1) — insurance policies tracking, claims management, renewal alerts

---

## 1. Purpose

The Insurance Registry tracks all insurance policies held by the Institution Group and its branches — student group accident insurance, staff medical/health insurance, Directors & Officers (D&O) liability insurance, property and building insurance, third-party liability insurance, and vehicle insurance (for transport fleet). Insurance is a critical risk management tool; a lapsed policy at the time of a student accident or property fire can expose the group to enormous uninsured liability.

The Group Insurance Coordinator (Role 129, G1) uses this page to: maintain the complete insurance portfolio; receive expiry alerts well before policy lapse; track claims filed and their settlement status; and ensure every branch has the mandatory minimum insurance coverage required by CBSE and state education authorities. For large groups, the insurance portfolio across 50 branches can involve 100+ active policies with varied renewal dates.

The page links with the Legal Notices & Litigation page (N-09) — when a court case arises from an insured event, the insurance coordinator can see which policy is relevant. It also links with Division J (Health & Medical) for student accident claim data.

Scale: 5–50 branches · 5–20 policy types · 50–500 active policies group-wide · Claims: 5–50 per year

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Reviews policy terms externally |
| Group Compliance Manager | 109 | G1 | Read — Mandatory coverage verification | Views which branches meet mandatory insurance requirements |
| Group RTI Officer | 110 | G1 | No Access | Not relevant |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Not relevant |
| Group POCSO Reporting Officer | 112 | G1 | No Access | Not relevant |
| Group Data Privacy Officer | 113 | G1 | No Access | Not relevant |
| Group Contract Administrator | 127 | G3 | No Access | Not relevant (insurance policies are not service contracts) |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Policies linked to litigation | Views policies relevant to active court cases |
| Group Insurance Coordinator | 129 | G1 | Full Read | Primary user; all policies, claims, renewals |

> **Access enforcement:** `@require_role(roles=[109,128,129], min_level=G1)`. G4/G5 full read.
>
> **Note:** G1 access is read-only on this page. Insurance policy renewals and new policies are arranged externally by the Insurance Coordinator with insurers; this page records the result.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Insurance Registry
```

### 3.2 Page Header
```
Insurance Registry                              [Export ↓]
Group Insurance Coordinator — [Name]
[Group Name] · [N] Active Policies · Total Premium: ₹[amount]/year · [N] Open Claims
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Policy expired (not renewed) | "[N] insurance policy(ies) have expired — group is currently uninsured for those risks." | Critical (red) |
| Policy expiring within 30 days | "[N] policy(ies) expire within 30 days. Contact insurer for renewal immediately." | High (amber) |
| Policy expiring within 60 days | "[N] policy(ies) expire within 60 days. Initiate renewal process." | Medium (yellow) |
| Open claim overdue for settlement (> 60 days) | "[N] insurance claim(s) have been open for more than 60 days without settlement." | Medium (yellow) |
| Branch missing mandatory insurance | "[N] branch(es) do not have mandatory [type] insurance coverage. CBSE compliance risk." | High (amber) |

---

## 4. KPI Summary Bar (7 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Policies | Count | COUNT WHERE status = 'active' | Blue | `#kpi-active-policies` |
| 2 | Expiring (60 Days) | Count | COUNT WHERE expiry BETWEEN TODAY AND TODAY+60 | Red > 5, Amber 1–5, Green = 0 | `#kpi-expiring-60d` |
| 3 | Expired (Unrenewed) | Count | COUNT WHERE expiry < TODAY AND renewed = False | Red > 0, Green = 0 | `#kpi-expired` |
| 4 | Total Annual Premium | Sum (₹) | SUM annual_premium WHERE status = 'active' | Blue (info) | `#kpi-total-premium` |
| 5 | Open Claims | Count | COUNT WHERE status NOT IN ('settled','rejected','withdrawn') | Amber > 5, Blue ≤ 5 | `#kpi-open-claims` |
| 6 | Claims Settled (This FY) | Count | COUNT WHERE status = 'settled' AND fy = current | Green | `#kpi-settled-claims` |
| 7 | Branches with Full Coverage | Count | COUNT branches with all mandatory policy types active | Green if = total | `#kpi-full-coverage` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/insurance/kpis/"` with `hx-trigger="load, every 300s"`.

---

## 5. Sections

### 5.1 Insurance Policies Table

**Search:** Policy number, insurer name, branch, policy type. Debounced 350ms.

**Filters:**
- Policy Type: `All` · `Student Group Accident` · `Staff Medical / Group Health` · `Property & Building` · `Vehicle` · `D&O Liability` · `Third-Party Liability` · `Fire Insurance` · `Other`
- Status: `All` · `Active` · `Expiring Soon` · `Expired` · `Terminated`
- Branch: dropdown (+ Group Level for group-wide policies)

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Policy Number | Monospace | Yes | Insurer-issued |
| Policy Type | Badge | Yes | |
| Insurer Name | Text | Yes | |
| Branch / Scope | Text | Yes | Specific branch or "All Branches" |
| Sum Insured (₹) | Currency | Yes | |
| Annual Premium (₹) | Currency | Yes | |
| Policy Start | Date | Yes | |
| Policy End | Date | Yes | Red < 30d, amber < 60d |
| Days to Expiry | Badge | Yes | Red if negative |
| Status | Badge | Yes | |
| Open Claims | Integer | No | Count of open claims against this policy |
| Actions | Buttons | No | [View] |

**Default sort:** Policy End ASC
**Pagination:** Server-side · Default 25/page

---

### 5.2 Claims Register

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Claim ID | Monospace | Yes | AUTO: CLM-YYYYMMDD-NNNN |
| Policy Number | Link | Yes | Links to parent policy |
| Claim Date | Date | Yes | Date claim was filed |
| Branch | Text | Yes | |
| Claim Type | Badge | Yes | Accident / Property Damage / Vehicle / Medical / Other |
| Claim Amount (₹) | Currency | Yes | Amount claimed |
| Settlement Amount (₹) | Currency | No | Amount settled (blank if pending) |
| Days Open | Integer | Yes | Red > 60 |
| Status | Badge | Yes | Filed / Under Review / Settled / Rejected / Withdrawn |
| Actions | Buttons | No | [View] |

**Default sort:** Claim Date DESC

---

## 6. Drawers & Modals

### 6.1 Drawer: `policy-detail` (720px)
- **Tabs:** Overview · Coverage Details · Claims · Documents · Renewal History
- **Overview:** Policy number, type, insurer, agent name/contact, branch/scope, sum insured, premium, dates, status
- **Coverage Details:** Covered risks, exclusions, deductible, claim limit per event
- **Claims tab:** List of all claims against this policy
- **Documents tab:** Policy document, renewal notice, endorsements
- **Renewal History tab:** Past policy cycles

### 6.2 Drawer: `claim-detail` (680px)
- **Tabs:** Overview · Documents · Communication · Timeline
- **Overview:** Claim ID, policy, branch, incident date, claim date, type, amount claimed, settlement amount, status, adjuster name
- **Documents:** Claim form, supporting evidence, survey report, settlement letter
- **Communication:** Correspondence with insurer
- **Timeline:** Status change log

---

## 7. Charts

### 7.1 Insurance Coverage by Branch — Status Heatmap

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Insurance Coverage Status by Branch" |
| Data | Per branch: count of Active / Expiring / Expired policies |
| Colour | Active=green, Expiring=amber, Expired=red |
| Tooltip | "[Branch]: [N] active, [N] expiring, [N] expired" |
| API endpoint | `GET /api/v1/group/{id}/legal/insurance/coverage-by-branch/` |
| HTMX | `hx-get` on load → `hx-target="#chart-coverage-branch"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Premium Distribution by Type — Donut

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Annual Premium by Policy Type" |
| Data | Sum of premium per policy type |
| Tooltip | "[Type]: ₹[total] per year ([N] policies)" |
| API endpoint | `GET /api/v1/group/{id}/legal/insurance/premium-by-type/` |
| HTMX | `hx-get` on load → `hx-target="#chart-premium-by-type"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Policy expiry alert | "[Policy Type] at [Branch] expires in [N] days." | Warning | 6s |
| Policy expired | "[Policy Number] has expired. Group is uninsured for this risk." | Error | 8s |
| Claim status updated | "Claim [CLM-ID] status updated to [status]." | Success | 3s |
| Export triggered | "Generating insurance registry export…" | Info | 3s |
| Export ready | "Insurance export ready. Click to download." | Success | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No policies | `shield` | "No Insurance Policies" | "No insurance policies have been recorded." | Contact IT Admin |
| No claims | `check-circle` | "No Claims on Record" | "No insurance claims have been filed." | — |
| Filter returns no results | `search` | "No Matching Policies" | | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 7 KPI + two 8-row table skeletons |
| Filter/search | Spinner overlay |
| Charts | Grey canvas + spinner |
| Drawer open | Right-slide skeleton |

---

## 11. Role-Based UI Visibility

| Element | Insurance Coord (129) | Compliance Mgr (109) | Legal Dispute (128) | CEO/Chairman |
|---|---|---|---|---|
| Full policies table | Visible | Mandatory coverage view | Policy-linked disputes | Full |
| Claims register | Full | Not visible | Relevant claims | Full |
| Financial data (premium, sum insured) | Visible | Not visible | Not visible | Visible |
| Charts | Both | Not visible | Not visible | Both |
| Export | Visible | Not visible | Not visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/insurance/policies/` | G1+ | Paginated policies list |
| GET | `/api/v1/group/{id}/legal/insurance/policies/{pol_id}/` | G1+ | Policy detail |
| GET | `/api/v1/group/{id}/legal/insurance/claims/` | G1+ | Claims register |
| GET | `/api/v1/group/{id}/legal/insurance/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/legal/insurance/coverage-by-branch/` | Role 129, G4+ | Chart data |
| GET | `/api/v1/group/{id}/legal/insurance/premium-by-type/` | Role 129, G4+ | Chart data |
| POST | `/api/v1/group/{id}/legal/insurance/export/` | G1+ | Async export |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + refresh | KPI container | GET `.../insurance/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Policies table | Table body | GET `.../insurance/policies/` | `#policies-table-body` | `innerHTML` | `hx-trigger="load"` |
| Claims table | Table body | GET `.../insurance/claims/` | `#claims-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search | Search input | GET with `?q=` | `#policies-table-body` | `innerHTML` | Debounce 350ms |
| Open policy drawer | [View] / row | GET `.../insurance/policies/{pol_id}/` | `#right-drawer` | `innerHTML` | |
| Open claim drawer | [View] in claims | GET `.../insurance/claims/{clm_id}/` | `#right-drawer` | `innerHTML` | |
| Charts | Chart containers | GET chart endpoints | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination | GET with `?page={n}` | `#policies-table-body` | `innerHTML` | |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
