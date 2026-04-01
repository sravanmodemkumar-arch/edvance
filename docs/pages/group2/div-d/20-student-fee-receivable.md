# 20 — Student Fee Receivable Tracker

- **URL:** `/group/finance/fee-receivable/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Roles:** Accounts Manager G1 (primary) · Fee Collection Head G3 · Finance Manager G1

---

## 1. Purpose

The Student Fee Receivable Tracker provides a cross-branch view of all outstanding student fee dues — tuition, hostel, transport, mess, and coaching fees. Unlike the Fee Collection Dashboard (Page 28) which shows operational collection drives and waiver workflows, this page is the accounting layer: it tracks each student's receivable balance by aging bucket, flags high-value defaulters, and feeds the Accounts Manager's ledger.

The Accounts Manager uses this to validate that branch-reported outstanding dues match the group ledger, identify students approaching write-off thresholds, and produce the receivable ageing statement required by the CFO and statutory auditors.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Accounts Manager | G1 | Full read + export |
| Group Fee Collection Head | G3 | Full read + export |
| Group Finance Manager | G1 | Full read |
| Group CFO | G1 | Read — summary only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Student Fee Receivable Tracker
```

### 3.2 Page Header
- **Title:** `Student Fee Receivable Tracker`
- **Subtitle:** `AY [Year] · [N] Students with Dues · Total Outstanding: ₹[X]`
- **Right-side controls:** `[AY ▾]` `[Term ▾]` `[Branch ▾]` `[Fee Type ▾]` `[Export ↓]`

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Receivable | ₹ | Red if > 5% of annual demand |
| 0–30 Days | ₹ | Amber |
| 31–60 Days | ₹ | Orange |
| >60 Days | ₹ | Red |
| Students with Dues | Count | Red if growing |
| Write-off Risk (>90 days) | ₹ | Red |

---

## 5. Main Table — Student-Level Receivable

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Student Name | Text | ✅ | — |
| Student ID | Text | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Class / Stream | Text | ✅ | ✅ |
| Student Type | Badge: Day Scholar · Hosteler | ✅ | ✅ |
| Total Due | ₹ | ✅ | — |
| 0–30 Days | ₹ | ✅ | — |
| 31–60 Days | ₹ | ✅ | — |
| >60 Days | ₹ (red) | ✅ | — |
| Waiver Applied | ₹ | ✅ | — |
| Net Receivable | ₹ | ✅ | — |
| Last Payment | Date | ✅ | — |
| Actions | View Detail | — | — |

### 5.1 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select |
| Student Type | Multi-select |
| Class | Multi-select |
| Age Bucket | Select: All · 0–30 · 31–60 · >60 days |
| Fee Type | Multi-select: Tuition · Hostel · Transport · Mess · Coaching |
| Amount Range | ₹ range slider |

### 5.2 Search
- Student name · Student ID · 300ms debounce

### 5.3 Pagination
- Server-side · 25 rows/page · Default sort: >60 days amount desc

---

## 6. Drawers

### 6.1 Drawer: `student-receivable-detail` — Student Fee Detail
- **Trigger:** View Detail action
- **Width:** 680px

**Tab: Fee Breakdown**

| Fee Component | Billed | Paid | Waiver | Balance |
|---|---|---|---|---|
| Tuition Fee — Term 1 | ₹ | ₹ | ₹ | ₹ |
| Tuition Fee — Term 2 | ₹ | ₹ | ₹ | ₹ |
| Hostel Fee | ₹ | ₹ | ₹ | ₹ |
| Mess Fee | ₹ | ₹ | ₹ | ₹ |
| Transport Fee | ₹ | ₹ | ₹ | ₹ |
| **Total** | **₹** | **₹** | **₹** | **₹** |

**Tab: Payment History**
| Date | Amount | Mode | Receipt Number |
|---|---|---|---|
| [Date] | ₹ | Online / Cash / Cheque | [Ref] |

**Tab: Communication Log**
- Previous reminders sent to student/parent
- (read-only — collection actions happen on Fee Collection pages)

---

## 7. Branch Receivable Summary (Aggregated View)

Toggle: `[Student Level ↔ Branch Level]`

Branch Level view:

| Branch | Students with Dues | 0–30 | 31–60 | >60 | Total |
|---|---|---|---|---|---|
| [Branch A] | [N] | ₹ | ₹ | ₹ | ₹ |

---

## 8. Charts

### 8.1 Receivable Ageing (Stacked Bar by Branch)
- **Stacks:** 0–30 (yellow) · 31–60 (orange) · >60 (red)
- **Export:** PNG

### 8.2 Receivable Trend — Group Total (Line)
- **X-axis:** Months of AY
- **Y-axis:** Total outstanding ₹
- **Export:** PNG

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export | "Receivable tracker exported." | Info | 3s |

---

## 10. Empty States

| Condition | Heading | Description |
|---|---|---|
| No receivables | "No outstanding receivables" | "All student fees are collected for this period." |
| Filter returns none | "No students match" | "Adjust filters to see student receivables." |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table skeleton |
| Filter change | Table skeleton |
| Detail drawer | Spinner + skeleton tabs |

---

## 12. Role-Based UI Visibility

| Element | Accounts Mgr G1 | Collection Head G3 | Finance Mgr G1 |
|---|---|---|---|
| Full table (all branches) | ✅ | ✅ | ✅ |
| Student detail | ✅ | ✅ | ❌ |
| Export | ✅ | ✅ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/fee-receivable/` | JWT (G1+) | Student receivable list |
| GET | `/api/v1/group/{id}/finance/fee-receivable/{sid}/` | JWT (G1+) | Student detail |
| GET | `/api/v1/group/{id}/finance/fee-receivable/branch-summary/` | JWT (G1+) | Branch aggregated |
| GET | `/api/v1/group/{id}/finance/fee-receivable/ageing/` | JWT (G1+) | Ageing data |
| GET | `/api/v1/group/{id}/finance/fee-receivable/export/` | JWT (G1+) | Export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../fee-receivable/?q=` | `#receivable-table-body` | `innerHTML` |
| Filter | `change` | GET `.../fee-receivable/?branch=&age=` | `#receivable-section` | `innerHTML` |
| View toggle | `click` | GET `.../fee-receivable/branch-summary/` | `#receivable-section` | `innerHTML` |
| Student detail | `click` | GET `.../fee-receivable/{sid}/` | `#drawer-body` | `innerHTML` |
| Pagination | `click` | GET `.../fee-receivable/?page=` | `#receivable-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
