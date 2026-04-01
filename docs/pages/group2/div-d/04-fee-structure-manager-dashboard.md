# 04 — Group Fee Structure Manager Dashboard

- **URL:** `/group/finance/fee-structure/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Fee Structure Manager (Role 33, G3)

---

## 1. Purpose

The Fee Structure Manager Dashboard is the configuration centre for all fee types across all branches in the group. This role (G3 — operational write access) is responsible for ensuring that every branch has correctly configured fees before the academic year starts: day scholar tuition, hosteler fees (AC/Non-AC, boys/girls), integrated coaching fees, transport fees, mess charges, and stream-specific fees.

The platform enforces that no branch can collect fees without a published fee structure approved at the group level. This dashboard shows publication status per branch, highlights any branches missing fee configuration, tracks all revision history, and surfaces cross-branch fee comparisons to ensure equitable and intentional differentiation.

A fee structure error discovered after admission season can cause refund obligations, regulatory penalties, and student/parent disputes. This page exists to eliminate that risk.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Fee Structure Manager | G3 | Full read + write + publish | Primary owner |
| Group CFO | G1 | Read — all sections | Cannot modify |
| Group Finance Manager | G1 | Read — all sections | Cannot modify |
| Group Fee Collection Head | G3 | Read — published fees only | Cannot modify structure |
| Branch Accountant | Branch | Read — own branch fees only | After publication |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Structure Manager
```

### 3.2 Page Header
- **Title:** `Fee Structure Manager`
- **Subtitle:** `AY [Year] · [N] Branches · [X] Published · [Y] Draft · [Z] Missing`
- **Role Badge:** `Group Fee Structure Manager`
- **Right-side controls:** `[Academic Year ▾]` `[+ New Fee Template]` `[Bulk Publish]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any branch missing fee structure for current AY | "Fee structure not configured for [N] branch(es). Students cannot be billed." | Red |
| Fee structure unpublished (draft) for any branch | "[N] branch(es) have draft fee structures not yet published." | Amber |
| Fee revision pending approval | "[N] fee revision requests awaiting approval." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Branches with Published Fees | Count | Green = all branches | → Fee status table |
| Branches in Draft | Count | Amber if > 0 | → Fee status table |
| Branches with No Fee Config | Count | Red if > 0 | → Page 22 |
| Fee Templates Active | Count | Informational | → Page 22 |
| Pending Revisions | Count | Amber if > 0 | → Page 25 |
| Concession Policies Active | Count | Informational | → Page 27 |

---

## 5. Main Table — Branch Fee Status

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text + link | ✅ | ✅ |
| Day Scholar Fee | ₹ / Badge (Set · Missing) | ✅ | ✅ |
| Hosteler Fee (Non-AC) | ₹ / Badge | ✅ | ✅ |
| Hosteler Fee (AC) | ₹ / Badge | ✅ | ✅ |
| Transport Fee | ₹ / Badge | ✅ | ✅ |
| Coaching Fee | ₹ / Badge | ✅ | ✅ |
| Status | Badge: Published · Draft · Missing | ✅ | ✅ |
| Last Updated | Date | ✅ | — |
| Actions | View · Edit · Publish · Clone | — | — |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Status | Multi-select | Published · Draft · Missing |
| Branch | Multi-select | Branch names |
| Student Type | Multi-select | Day Scholar · Hosteler · Integrated Coaching |

### 5.2 Search
- Full-text: branch name
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `fee-structure-view` — View Branch Fee Structure
- **Trigger:** View action on table row
- **Width:** 720px

**Tab: Day Scholar Fees**
| Fee Component | Amount | Frequency | Stream |
|---|---|---|---|
| Tuition Fee | ₹ | Monthly / Term / Annual | All / MPC / BiPC |
| Admission Fee | ₹ | One-time | All |
| Exam Fee | ₹ | Per exam | All |
| Lab Fee | ₹ | Annual | Science streams |
| Library Fee | ₹ | Annual | All |
| Activity Fee | ₹ | Annual | All |

**Tab: Hosteler Fees**
| Fee Component | Boys Non-AC | Boys AC | Girls Non-AC | Girls AC |
|---|---|---|---|---|
| Hostel Admission | ₹ | ₹ | ₹ | ₹ |
| Monthly Hostel | ₹ | ₹ | ₹ | ₹ |
| Mess Fee | ₹ | ₹ | ₹ | ₹ |
| Laundry | ₹ | ₹ | ₹ | ₹ |

**Tab: Transport Fees**
- Route-wise transport fee table (route name → ₹/month)

**Tab: Coaching Fees**
- JEE/NEET integrated: ₹
- IIT Foundation (per class): ₹

**Tab: Revision History**
- Changelog of all modifications with user + date

### 6.2 Drawer: `fee-structure-publish` — Publish Confirmation
- Shows summary of fee structure
- Confirm publish: "Publish fees for [Branch] for AY [Year]. Branch can begin billing students."
- [Cancel] [Publish]

---

## 7. Charts

### 7.1 Fee Comparison by Branch (Bar)
- **X-axis:** Branches
- **Series:** Day Scholar (blue) · Hosteler Non-AC (green) · Hosteler AC (orange)
- **Export:** PNG

### 7.2 Fee Structure Completeness (Donut)
- **Segments:** Published · Draft · Missing
- **Centre:** "[N] branches total"

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Fee structure published | "Fee structure published for [Branch]. Branch can now collect fees." | Success | 4s |
| Bulk publish | "Fee structures published for [N] branches." | Success | 4s |
| Draft saved | "Draft saved for [Branch]." | Info | 3s |
| Missing config | "Cannot publish — [Field] is missing for [Branch]." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No fee templates | "No fee templates" | "Create the first fee template for this academic year." | [+ New Fee Template] |
| All fees published | "All fee structures published" | "All branches have published fee structures." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table skeleton (20 rows) |
| AY switch | Full table skeleton |
| Drawer open | Spinner + skeleton tabs |

---

## 11. Role-Based UI Visibility

| Element | Fee Structure Mgr G3 | CFO G1 | Finance Mgr G1 | Collection Head G3 |
|---|---|---|---|---|
| [+ New Fee Template] | ✅ | ❌ | ❌ | ❌ |
| [Bulk Publish] | ✅ | ❌ | ❌ | ❌ |
| Edit action | ✅ | ❌ | ❌ | ❌ |
| Publish action | ✅ | ❌ | ❌ | ❌ |
| View all branches | ✅ | ✅ | ✅ | ✅ (own) |
| Export | ✅ | ✅ | ✅ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/fee-structure/` | JWT (G1+) | Branch fee status list |
| GET | `/api/v1/group/{id}/finance/fee-structure/kpis/` | JWT (G1+) | KPI cards |
| GET | `/api/v1/group/{id}/finance/fee-structure/{bid}/` | JWT (G1+) | Branch fee detail |
| POST | `/api/v1/group/{id}/finance/fee-structure/` | JWT (G3) | Create fee template |
| PUT | `/api/v1/group/{id}/finance/fee-structure/{bid}/` | JWT (G3) | Update fee structure |
| POST | `/api/v1/group/{id}/finance/fee-structure/{bid}/publish/` | JWT (G3) | Publish |
| POST | `/api/v1/group/{id}/finance/fee-structure/bulk-publish/` | JWT (G3) | Bulk publish |
| GET | `/api/v1/group/{id}/finance/fee-structure/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../fee-structure/?q=` | `#branch-table-body` | `innerHTML` |
| Filter | `change` | GET `.../fee-structure/?status=` | `#branch-section` | `innerHTML` |
| Pagination | `click` | GET `.../fee-structure/?page=` | `#branch-section` | `innerHTML` |
| View drawer | `click` | GET `.../fee-structure/{bid}/` | `#drawer-body` | `innerHTML` |
| Publish | `click` | POST `.../fee-structure/{bid}/publish/` | `#publish-confirm-modal` | `innerHTML` |
| AY switch | `change` | GET `.../fee-structure/?ay=` | `#fee-structure-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
