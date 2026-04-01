# 30 — Waiver Approval Manager

- **URL:** `/group/finance/collection/waivers/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Fee Collection Head G3 (primary) · CFO G1 (view)

---

## 1. Purpose

The Waiver Approval Manager is the centralised workflow for fee waiver requests submitted by branch fee managers on behalf of students. A fee waiver can be full (100% of outstanding) or partial (a specific amount). All waivers must be approved at the group level — branches cannot unilaterally waive fees.

The workflow: Branch fee manager submits waiver request with supporting documents → Fee Collection Head reviews and approves/rejects → Approved waiver is applied to the student's fee account → Student notified by branch.

This prevents revenue leakage from unauthorized concessions and ensures all waivers are documented with justification.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Collection Head | G3 | Full read + approve/reject |
| Group CFO | G1 | Read — approved waivers + financial impact |
| Group Finance Manager | G1 | Read — for reconciliation |
| Group Scholarship Finance Officer | G3 | Read — scholarship-linked waivers |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Collection → Waiver Approval Manager
```

### 3.2 Page Header
- **Title:** `Fee Waiver Approval Manager`
- **Subtitle:** `[N] Pending · [X] Approved (AY) · ₹[Y] Total Waived (AY)`
- **Right-side controls:** `[AY ▾]` `[Status ▾]` `[Branch ▾]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Waiver requests pending > 48 hours | "[N] waiver requests pending for more than 48 hours." | Amber |
| Total waivers this month > budget threshold | "Fee waivers this month: ₹[X]. Approaching budget limit of ₹[Y]." | Amber |

---

## 4. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Request ID | Text | ✅ | — |
| Student Name | Text | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Class / Stream | Text | ✅ | — |
| Waiver Type | Badge: Full · Partial · Scholarship · Staff Ward | ✅ | ✅ |
| Outstanding Amount | ₹ | ✅ | — |
| Waiver Requested | ₹ | ✅ | — |
| Reason Category | Badge: Financial Hardship · Academic Merit · Staff Ward · Scholarship · Medical | ✅ | ✅ |
| Submitted By | Text | ✅ | — |
| Submitted Date | Date | ✅ | — |
| Age (Hours) | Number | ✅ | — |
| Status | Badge: Pending · Under Review · Approved · Rejected · Cancelled | ✅ | ✅ |
| Actions | Review · Approve · Reject | — | — |

### 4.1 Filters

| Filter | Type |
|---|---|
| Status | Multi-select |
| Branch | Multi-select |
| Waiver Type | Multi-select |
| Reason | Multi-select |
| Date Range | Date picker |
| Amount Range | ₹ range |

### 4.2 Search
- Student name · Request ID · Branch name

### 4.3 Pagination
- 25 rows/page · Default sort: Submitted Date asc (oldest first)

### 4.4 Bulk Actions
- Select multiple Pending → [Bulk Approve] (for small amounts below threshold)

---

## 5. Drawers

### 5.1 Drawer: `waiver-review` — Full Waiver Review
- **Trigger:** Review action
- **Width:** 720px

**Student Information**
| Field | Value |
|---|---|
| Name | [Name] |
| ID | [ID] |
| Class / Stream | [Details] |
| Student Type | [Day Scholar / Hosteler] |
| Branch | [Name] |
| Scholarship Status | [None / Scholarship Type] |

**Fee Details**
| Component | Total Fee | Paid | Outstanding |
|---|---|---|---|
| [Fee 1] | ₹ | ₹ | ₹ |
| **Total** | **₹** | **₹** | **₹** |

**Waiver Request**
| Field | Value |
|---|---|
| Waiver Type | [Full / Partial] |
| Amount Requested | ₹[X] |
| Reason | [Text] |
| Supporting Documents | [File links — income certificate, medical certificate, etc.] |
| Recommended By | [Branch Fee Manager Name + Role] |
| Recommendation Note | [Text] |

**Previous Waiver History** (if any)
| AY | Term | Amount Waived | Reason |
|---|---|---|---|
| [AY] | [Term] | ₹ | [Reason] |

**Decision Form:**

| Field | Type | Required |
|---|---|---|
| Decision | Radio: Approve · Reject · Request More Info | ✅ |
| Approved Amount | Number | ✅ (if Approve) — ≤ Outstanding |
| Decision Note | Textarea | ✅ | Min 30 chars |
| Internal Reference | Text | ❌ |

- [Cancel] [Submit Decision]

### 5.2 Drawer: `bulk-approve` — Bulk Approval
- Threshold: Only show requests ≤ ₹[configured threshold]
- Show list of selected requests with amounts
- One-line approval note
- [Confirm Bulk Approve]

---

## 6. Waiver Budget Tracker

Section below table: Monthly/Annual waiver budget consumption.

| Budget Line | Allocated | Approved | Remaining |
|---|---|---|---|
| Financial Hardship Waivers | ₹ | ₹ | ₹ |
| Staff Ward Waivers | ₹ | ₹ | ₹ |
| Merit Waivers | ₹ | ₹ | ₹ |
| **Total** | **₹** | **₹** | **₹** |

---

## 7. Charts

### 7.1 Waiver Requests by Status (Donut)
- **Segments:** Pending · Approved · Rejected

### 7.2 Monthly Waiver Amount Approved (Bar)
- **X-axis:** Months
- **Y-axis:** ₹

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Approved | "Waiver of ₹[X] approved for [Student]. Branch notified." | Success | 4s |
| Rejected | "Waiver rejected for [Student]. Branch notified with reason." | Warning | 4s |
| More info requested | "Additional information requested from [Branch] for [Student]'s waiver." | Info | 4s |
| Bulk approved | "[N] waivers approved. Total: ₹[X]. Branches notified." | Success | 5s |
| Export | "Waiver report exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No pending waivers | "No pending waivers" | "No fee waiver requests awaiting approval." |
| No waivers for period | "No waivers" | "No fee waiver requests for this period." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table + KPI bar |
| Filter change | Table skeleton |
| Review drawer | Spinner + student info skeleton |
| Submit decision | Spinner on submit button |

---

## 11. Role-Based UI Visibility

| Element | Collection Head G3 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [Approve] | ✅ | ❌ | ❌ |
| [Reject] | ✅ | ❌ | ❌ |
| [Request More Info] | ✅ | ❌ | ❌ |
| [Bulk Approve] | ✅ | ❌ | ❌ |
| View all waivers | ✅ | ✅ | ✅ |
| Waiver budget tracker | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/collection/waivers/` | JWT (G1+) | Waiver list |
| GET | `/api/v1/group/{id}/finance/collection/waivers/{wid}/` | JWT (G1+) | Waiver detail |
| PUT | `/api/v1/group/{id}/finance/collection/waivers/{wid}/decide/` | JWT (G3) | Approve/Reject/More Info |
| POST | `/api/v1/group/{id}/finance/collection/waivers/bulk-approve/` | JWT (G3) | Bulk approve |
| GET | `/api/v1/group/{id}/finance/collection/waivers/budget/` | JWT (G1+) | Budget tracker |
| GET | `/api/v1/group/{id}/finance/collection/waivers/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../waivers/?q=` | `#waiver-table-body` | `innerHTML` |
| Filter | `change` | GET `.../waivers/?status=&branch=` | `#waiver-section` | `innerHTML` |
| Review drawer | `click` | GET `.../waivers/{id}/` | `#drawer-body` | `innerHTML` |
| Submit decision | `submit` | PUT `.../waivers/{id}/decide/` | `#drawer-body` | `innerHTML` |
| Bulk approve | `click` | POST `.../waivers/bulk-approve/` | `#bulk-confirm-modal` | `innerHTML` |
| Pagination | `click` | GET `.../waivers/?page=` | `#waiver-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
