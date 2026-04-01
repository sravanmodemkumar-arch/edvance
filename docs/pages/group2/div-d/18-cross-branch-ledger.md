# 18 — Cross-Branch Ledger (Payable / Receivable)

- **URL:** `/group/finance/ledger/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Roles:** Accounts Manager G1 (primary) · Finance Manager G1 · CFO G1 · Internal Auditor G1

---

## 1. Purpose

The Cross-Branch Ledger provides a consolidated view of all payable and receivable transactions across the group. It aggregates vendor payables, student fee receivables, inter-branch transfers, government grant receivables, and scholarship disbursements into a single ledger intelligence layer. The Accounts Manager uses this page to detect ageing balances, duplicate entries, and inter-branch fund movement discrepancies.

This is a read-only aggregate view — the source data originates in branch accountant systems and the external payroll/vendor payment software. The Accounts Manager reconciles these feeds against the group ledger and flags anomalies for investigation.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Accounts Manager | G1 | Full read |
| Group Finance Manager | G1 | Full read |
| Group CFO | G1 | Full read |
| Group Internal Auditor | G1 | Full read (audit access) |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Cross-Branch Ledger
```

### 3.2 Page Header
- **Title:** `Cross-Branch Ledger`
- **Subtitle:** `As of [Date] · FY [Year] · [N] Branches`
- **Right-side controls:** `[As-of Date ▾]` `[Branch ▾]` `[Type ▾]` `[Export ↓]`

---

## 4. Tabs

### Tab 1: Payables

| Column | Type | Sortable |
|---|---|---|
| Payable Type | Badge: Vendor · Salary · GST/TDS · Inter-Branch · Other | ✅ |
| Party Name | Text | ✅ |
| Branch | Text | ✅ |
| Invoice Date | Date | ✅ |
| Due Date | Date | ✅ |
| Amount | ₹ | ✅ |
| Paid | ₹ | ✅ |
| Balance | ₹ (red if > 0) | ✅ |
| Age (Days) | Number | ✅ |
| Status | Badge: Current · Overdue · Disputed | ✅ |
| Actions | View | — |

**Ageing summary row below table:**
```
0–30 days: ₹[X] | 31–60 days: ₹[Y] | 61–90 days: ₹[Z] | >90 days: ₹[W]
```

### Tab 2: Receivables

| Column | Type | Sortable |
|---|---|---|
| Receivable Type | Badge: Student Fee · Govt Grant · RTE Reimbursement · Inter-Branch | ✅ |
| Party Name | Text | ✅ |
| Branch | Text | ✅ |
| Due Date | Date | ✅ |
| Amount | ₹ | ✅ |
| Received | ₹ | ✅ |
| Balance | ₹ | ✅ |
| Age (Days) | Number | ✅ |
| Status | Badge: Current · Overdue · Written Off | ✅ |
| Actions | View | — |

**Ageing summary row below table:**
```
0–30 days: ₹[X] | 31–60 days: ₹[Y] | 61–90 days: ₹[Z] | >90 days: ₹[W]
```

### Tab 3: Inter-Branch Transfers

| Column | Type | Sortable |
|---|---|---|
| From Branch | Text | ✅ |
| To Branch | Text | ✅ |
| Transfer Date | Date | ✅ |
| Amount | ₹ | ✅ |
| Purpose | Text | ✅ |
| Status | Badge: Confirmed · Pending · Disputed | ✅ |
| Actions | View | — |

---

## 5. Filters (all tabs)

| Filter | Type |
|---|---|
| Branch | Multi-select |
| Date Range | Date picker: From – To |
| Status | Multi-select |
| Amount Range | ₹ range |

### Search
- Party name · 300ms debounce

### Pagination
- Server-side · 25 rows/page per tab

---

## 6. Drawers

### 6.1 Drawer: `ledger-entry-detail` — Transaction Detail
- **Trigger:** View action
- **Width:** 640px

| Field | Value |
|---|---|
| Transaction ID | [ID] |
| Type | [Payable/Receivable] |
| Party | [Name] |
| Branch | [Name] |
| Invoice / Reference | [Number] |
| Date | [Date] |
| Due Date | [Date] |
| Amount | ₹ |
| Amount Paid/Received | ₹ |
| Balance | ₹ |
| Payment History | Table: Date · Amount · Mode · Reference |
| Source | [Branch system / Payroll software / Manual] |

---

## 7. Charts

### 7.1 Payable Ageing (Stacked Bar by Branch)
- **Stacks:** 0–30 · 31–60 · 61–90 · >90 days
- **Export:** PNG

### 7.2 Receivable Ageing (Stacked Bar by Branch)
- **Same structure as payable ageing**

### 7.3 Payable vs Receivable — Group Summary (Bar)
- **Side-by-side:** Total payable · Total receivable per branch

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export | "Ledger exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No payables | "No outstanding payables" | "All payables are cleared." |
| No receivables | "No outstanding receivables" | "All receivables are collected." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton tabs + table skeleton |
| Tab switch | Table skeleton |
| Filter change | Inline skeleton |
| Detail drawer | Spinner + skeleton fields |

---

## 11. Role-Based UI Visibility

| Element | Accounts Mgr G1 | Finance Mgr G1 | CFO G1 | Auditor G1 |
|---|---|---|---|---|
| All tabs | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/ledger/payables/` | JWT (G1+) | Payables list |
| GET | `/api/v1/group/{id}/finance/ledger/receivables/` | JWT (G1+) | Receivables list |
| GET | `/api/v1/group/{id}/finance/ledger/inter-branch/` | JWT (G1+) | Inter-branch transfers |
| GET | `/api/v1/group/{id}/finance/ledger/entry/{eid}/` | JWT (G1+) | Transaction detail |
| GET | `/api/v1/group/{id}/finance/ledger/ageing/` | JWT (G1+) | Ageing summary |
| GET | `/api/v1/group/{id}/finance/ledger/export/?type=payables` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | GET `.../ledger/{type}/` | `#ledger-tab-body` | `innerHTML` |
| Filter | `change` | GET `.../ledger/{type}/?branch=&status=` | `#ledger-table` | `innerHTML` |
| Search | `input delay:300ms` | GET `.../ledger/{type}/?q=` | `#ledger-table-body` | `innerHTML` |
| Detail drawer | `click` | GET `.../ledger/entry/{id}/` | `#drawer-body` | `innerHTML` |
| Pagination | `click` | GET `.../ledger/{type}/?page=` | `#ledger-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
