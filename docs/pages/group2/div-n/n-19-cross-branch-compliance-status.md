# [19] — Cross-Branch Compliance Status

> **URL:** `/group/legal/cross-branch-status/`
> **File:** `n-19-cross-branch-compliance-status.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Compliance Manager (Role 109, G1) — executive compliance matrix: all branches × all dimensions at a glance

---

## 1. Purpose

The Cross-Branch Compliance Status page is the most executive-facing page in Division N. It presents a single-screen matrix view of every branch's compliance status across every major compliance dimension — affiliation, RTI, POCSO, data privacy, staff contracts, regulatory filings, insurance, statutory returns, and inspection outcomes — enabling the Chairman, CEO, or Compliance Manager to see the group's compliance health in one table without navigating to individual module pages.

Each cell in the matrix is a simple colour-coded badge: ✅ Compliant (green), ⚠️ Attention (amber), ❌ Non-Compliant (red), ⏳ Due Soon (yellow), or N/A. Clicking any cell opens the relevant detail drawer from the corresponding module. The Chairman can present this report in a 2-minute Board Meeting briefing and immediately ask principals of non-compliant branches for explanations.

The page also provides a branch principal notification function — the Compliance Manager can select one or more non-compliant branches and send a compliance alert notification to the branch principal's account, requesting corrective action within a specified deadline.

Scale: 5–50 branches (rows) × 9 compliance dimensions (columns) = 45–450 status cells, updated in real time from all N modules

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | |
| Group Compliance Manager | 109 | G1 | Full View + Branch Notification | Primary user |
| Group RTI Officer | 110 | G1 | Read — RTI column only | |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | |
| Group POCSO Reporting Officer | 112 | G1 | Read — POCSO column only | |
| Group Data Privacy Officer | 113 | G1 | Read — DPDP column only | |
| Group Contract Administrator | 127 | G3 | Read — Contracts column only | |
| Group Legal Dispute Coordinator | 128 | G1 | No Access | Not relevant |
| Group Insurance Coordinator | 129 | G1 | Read — Insurance column only | |

> **Access enforcement:** `@require_role(roles=[109,110,112,113,127,129], min_level=G1)` with column-scoping. G4/G5 full access.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Cross-Branch Compliance Status
```

### 3.2 Page Header
```
Cross-Branch Compliance Status                  [Notify Branches]  [Export PDF]
Group Compliance Manager — [Name]
[Group Name] · [N] Branches · Overall Compliance: [X]% · Last updated: [datetime]
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any branch has ❌ in POCSO or Affiliation | "Critical non-compliance detected. [N] branch(es) require immediate attention in high-risk dimensions." | Critical (red) |
| Overall compliance below 70% | "Group overall compliance at [X]% — below minimum threshold." | High (amber) |
| More than 5 branches with ⚠️ Attention | "[N] branches have compliance items needing attention." | Medium (yellow) |

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Fully Compliant Branches | Count | COUNT branches WHERE all dimensions = Compliant | Green if = total | `#kpi-fully-compliant` |
| 2 | Branches Needing Attention | Count | COUNT WHERE any dimension = Attention | Amber | `#kpi-attention` |
| 3 | Non-Compliant Branches | Count | COUNT WHERE any dimension = Non-Compliant | Red > 0, Green = 0 | `#kpi-non-compliant` |
| 4 | Overall Group Score | % | weighted average across all branches+dimensions | Green ≥ 80%, Amber 60–79%, Red < 60% | `#kpi-group-score` |
| 5 | Critical Dimensions (≥ 1 red) | Count (of 9) | COUNT dimensions where any branch has ❌ | Red > 0, Green = 0 | `#kpi-critical-dims` |
| 6 | Notifications Sent (This Month) | Count | COUNT compliance_notifications WHERE sent within current month | Blue | `#kpi-notifications` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/cross-branch-status/kpis/"` with `hx-trigger="load, every 300s"`.

---

## 5. Sections

### 5.1 Cross-Branch Compliance Matrix

The main feature of this page — a sortable, filterable matrix.

**Search:** Branch name. Debounced 350ms.

**Filters:**
- Status: `All Branches` · `Fully Compliant Only` · `Has Attention Items` · `Has Non-Compliant Items`
- Dimension: Select any of the 9 dimensions to sort by that dimension
- Branch Type: `Day School` · `Hostel` · `College` · `All`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | Branch name + city |
| Affiliation | Status badge | Yes | ✅ / ⚠️ / ❌ / ⏳ |
| RTI | Status badge | Yes | |
| POCSO | Status badge | Yes | |
| Data Privacy | Status badge | Yes | |
| Staff Contracts | Status badge | Yes | |
| Reg. Filings | Status badge | Yes | |
| Insurance | Status badge | Yes | |
| Annual Returns | Status badge | Yes | |
| Inspections | Status badge | Yes | |
| Overall | Score + bar | Yes | Weighted score 0–100 |
| Select | Checkbox | No | For batch notification |

**Status badge semantics:**
- ✅ Compliant (green) — all items in this dimension are on track
- ⚠️ Attention (amber) — some items due soon or minor gaps
- ❌ Non-Compliant (red) — overdue items or failed compliance
- ⏳ Due Soon (yellow) — nothing overdue yet but deadlines approaching (< 30 days)
- N/A (grey) — dimension not applicable to this branch type

**Cell click behaviour:** Click any cell → opens a mini-drawer showing the specific item(s) causing that status, with a "Go to [Module] →" button.

**Default sort:** Overall Score ASC (worst first)
**Pagination:** Server-side · Default 50/page (show all branches if ≤ 50)

---

### 5.2 Dimension Summary Row (Pinned Footer)

A pinned row at the bottom of the table showing group averages per dimension:

| Column | Value |
|---|---|
| Branch | **Group Average** |
| Affiliation | X% compliant |
| RTI | X% compliant |
| ... (each dimension) | |
| Overall | X% |

---

## 6. Drawers & Modals

### 6.1 Drawer: `cell-detail` (560px, right-slide)
Opens when clicking any status cell.
- **Header:** [Branch Name] — [Dimension Name]
- **Status badge + summary:** Why this cell is ✅ / ⚠️ / ❌
- **Issues list:** Each specific item contributing to the status — item name, due date, days overdue, current status
- **Footer:** "Go to [Dimension Module] →" button

### 6.2 Modal: `notify-branches` (580px)
Used to send a compliance alert to branch principals.

| Field | Type | Required |
|---|---|---|
| Selected Branches | Display (pre-filled from checkbox selection) | — |
| Compliance Dimensions | Multi-checkbox (pre-selected from non-compliant) | Yes |
| Message | Textarea (template pre-filled) | Yes |
| Response Deadline | Date | Yes |
| Notification Method | Select — Platform notification / WhatsApp / Email | Yes |

**Footer:** Cancel · Send Notifications
**On success:** Toast with count of notifications sent; logged in audit trail.

### 6.3 Modal: `export-pdf` (480px)
- **Fields:** Include sections (KPI bar, Matrix, Dimension Summary), Date, Title/heading customisation
- **Buttons:** Cancel · Export PDF

---

## 7. Charts

### 7.1 Branch Compliance Score Distribution (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Branch Compliance by Dimension — Group Average" |
| Data | Group-average score per dimension (9 bars) |
| X-axis | Dimension name |
| Y-axis | Score (0–100) |
| Colour | Green ≥ 80, Amber 60–79, Red < 60 per bar |
| Tooltip | "[Dimension]: [X]% group average — [N] compliant branches" |
| API endpoint | `GET /api/v1/group/{id}/legal/cross-branch-status/dimension-averages/` |
| HTMX | `hx-get` on load → `hx-target="#chart-dim-averages"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Compliance Status Breakdown (Stacked Bar per Branch)

| Property | Value |
|---|---|
| Chart type | Stacked horizontal bar (Chart.js 4.x) |
| Title | "Compliance Status Breakdown per Branch" |
| Data | Per branch: count of ✅ / ⚠️ / ❌ cells (out of 9 dimensions) |
| Colour | Green = ✅, Amber = ⚠️, Red = ❌ |
| Tooltip | "[Branch]: [N] compliant · [N] attention · [N] non-compliant" |
| API endpoint | `GET /api/v1/group/{id}/legal/cross-branch-status/branch-breakdown/` |
| HTMX | `hx-get` on load → `hx-target="#chart-branch-breakdown"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Matrix refreshed | "Compliance status refreshed." | Info | 2s |
| Notification sent | "Compliance alert sent to [N] branch principal(s)." | Success | 4s |
| Export triggered | "Generating cross-branch compliance report…" | Info | 3s |
| Export ready | "Compliance report ready. Click to download." | Success | 6s |
| Critical cell clicked | "Showing non-compliance details for [Branch] — [Dimension]." | Info | 2s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No branches configured | `building` | "No Branches Configured" | "Add branch locations to begin compliance tracking." | Contact IT Admin |
| All branches fully compliant | `check-circle` | "Full Group Compliance ✅" | "Every branch is compliant across all dimensions. Excellent!" | Export Report |
| Filter returns no results | `search` | "No Matching Branches" | | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 6 KPI + full matrix skeleton (N rows × 11 columns, shimmer cells) |
| Matrix refresh | Shimmer overlay on all cells |
| KPI auto-refresh | Shimmer pulse on card values |
| Charts | Grey canvas + spinner |
| Cell click → drawer | Slide-in skeleton (single-column, short) |
| Notification send | Button spinner + disabled |
| Export generation | Progress toast |

---

## 11. Role-Based UI Visibility

| Element | Compliance Mgr (109) | DPO (113) | POCSO (112) | Contract Admin (127) | CEO/Chairman |
|---|---|---|---|---|---|
| Full matrix (all 9 columns) | Visible | DPDP column only | POCSO column only | Contracts column only | Full |
| Branch selection checkboxes | Visible | Not visible | Not visible | Not visible | Visible |
| [Notify Branches] button | Visible | Not visible | Not visible | Not visible | Visible |
| Dimension summary row | Visible | DPDP only | POCSO only | Contracts only | Visible |
| Charts | Both | Not visible | Not visible | Not visible | Both |
| Export | Visible | Not visible | Not visible | Not visible | Visible |
| Cell detail drawer | Full detail | DPDP cell only | POCSO cell only | Contracts cell only | Full |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/cross-branch-status/matrix/` | G1+ (column-scoped) | Full compliance matrix data |
| GET | `/api/v1/group/{id}/legal/cross-branch-status/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/legal/cross-branch-status/cell/{branch_id}/{dimension}/` | G1+ | Cell detail data |
| GET | `/api/v1/group/{id}/legal/cross-branch-status/dimension-averages/` | G1+ | Chart: dimension averages |
| GET | `/api/v1/group/{id}/legal/cross-branch-status/branch-breakdown/` | G1+ | Chart: branch stacked breakdown |
| POST | `/api/v1/group/{id}/legal/cross-branch-status/notify/` | Role 109, G4+ | Send branch notifications |
| POST | `/api/v1/group/{id}/legal/cross-branch-status/export/` | G1+ | Export PDF/Excel |

### Query Parameters

| Parameter | Type | Description |
|---|---|---|
| `status_filter` | string | all / compliant / attention / non_compliant |
| `dimension` | string | affiliation / rti / pocso / dpdp / contracts / filings / insurance / returns / inspections |
| `branch_type` | string | day_school / hostel / college / all |
| `q` | string | Branch name search |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 / 50; default 50 |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + refresh | KPI container | GET `.../cross-branch-status/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Matrix load | Matrix container | GET `.../cross-branch-status/matrix/` | `#compliance-matrix` | `innerHTML` | `hx-trigger="load"` |
| Search | Search input | GET with `?q=` | `#compliance-matrix` | `innerHTML` | Debounce 350ms |
| Status filter | Filter chips | GET with `?status_filter=` | `#compliance-matrix` | `innerHTML` | `hx-trigger="click"` |
| Column sort | Column header click | GET with `?sort={dimension}` | `#compliance-matrix` | `innerHTML` | `hx-trigger="click"` |
| Cell detail drawer | Any cell click | GET `.../cell/{branch_id}/{dimension}/` | `#cell-drawer` | `innerHTML` | Small side drawer |
| Notify modal | [Notify Branches] | GET `/htmx/legal/cross-branch-status/notify-form/` | `#modal-container` | `innerHTML` | Pre-fills selected branches |
| Charts | Chart containers | GET chart endpoints | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination | GET with `?page={n}` | `#compliance-matrix` | `innerHTML` | |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
