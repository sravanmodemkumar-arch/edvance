# 25 — Fee Revision History & Audit Trail

- **URL:** `/group/finance/fee-structure/revision-history/`
- **Template:** `portal_base.html`
- **Priority:** P2
- **Role:** Fee Structure Manager G3 · CFO G1 · Internal Auditor G1

---

## 1. Purpose

The Fee Revision History page maintains a complete, tamper-proof audit trail of every fee structure change made across all branches and academic years. Every field modification — tuition increase, new component addition, removal of a fee component, or publication event — is logged with user, timestamp, old value, and new value.

This page serves two purposes: (1) operational — the Fee Structure Manager can trace back why a specific branch has a different fee than expected; (2) compliance — the Internal Auditor and statutory auditor can verify that fee changes followed the approval workflow and were not made ad-hoc without authorisation.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Structure Manager | G3 | Read — own changes |
| Group CFO | G1 | Full read — all branches |
| Group Internal Auditor | G1 | Full read — audit access |
| Group Finance Manager | G1 | Full read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Structure → Revision History
```

### 3.2 Page Header
- **Title:** `Fee Revision History & Audit Trail`
- **Subtitle:** `[N] Revisions · AY [Year]`
- **Right-side controls:** `[AY ▾]` `[Branch ▾]` `[Date Range ▾]` `[Export ↓]`

---

## 4. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Revision ID | Text | ✅ | — |
| Branch | Text | ✅ | ✅ |
| AY | Text | ✅ | ✅ |
| Student Type | Badge | ✅ | ✅ |
| Fee Component | Text | ✅ | ✅ |
| Change Type | Badge: Created · Updated · Published · Archived | ✅ | ✅ |
| Old Value | ₹ / Text | — | — |
| New Value | ₹ / Text | — | — |
| Change % | % (red if increase, green if decrease) | ✅ | — |
| Changed By | Text (username) | ✅ | — |
| Changed At | Datetime | ✅ | — |
| Actions | View Context | — | — |

### 4.1 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select |
| AY | Multi-select |
| Change Type | Multi-select |
| Date Range | Date picker |
| Changed By | User select |
| Student Type | Multi-select |

### 4.2 Search
- Branch name · Fee component name

### 4.3 Pagination
- Server-side · 25 rows/page · Default sort: Changed At desc

---

## 5. Drawers

### 5.1 Drawer: `revision-context` — Revision Context View
- **Trigger:** View Context
- **Width:** 680px

| Field | Value |
|---|---|
| Revision ID | [ID] |
| Branch | [Name] |
| AY | [Year] |
| Template Name | [Name] |
| Student Type | [Type] |
| Fee Component | [Name] |
| Change Type | [Badge] |
| Old Value | ₹[X] |
| New Value | ₹[Y] |
| Change % | [%] |
| Changed By | [Name] ([Role]) |
| Changed At | [Datetime] |
| Reason / Note | [Text if provided] |
| Approval Reference | [Board resolution number / Manager approval] |
| Related Revisions | Other fields changed in same session |

---

## 6. Annual Fee Change Report (Sub-section)

Comparison table: AY [Previous] vs AY [Current] for each fee component per branch.

| Branch | Component | AY N-1 Fee | AY N Fee | Change % |
|---|---|---|---|---|
| [Branch A] | Tuition | ₹ | ₹ | +10% |

**[Export AY Change Report]** — PDF formatted for Board review

---

## 7. Charts

### 7.1 Average Tuition Fee Trend (Line)
- **X-axis:** AY [Year-4] to AY [Current]
- **Y-axis:** Group average tuition fee
- **Export:** PNG

### 7.2 Revision Volume by Month (Bar)
- **Data:** Count of revisions per month

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export | "Fee revision history exported." | Info | 3s |
| AY change report | "Annual fee change report ready." | Success | 4s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No revisions | "No revision history" | "No fee structure changes recorded for this period." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Filter change | Inline table skeleton |
| Context drawer | Spinner |

---

## 11. Role-Based UI Visibility

| Element | Fee Struct Mgr G3 | CFO G1 | Auditor G1 |
|---|---|---|---|
| View all branches | ✅ | ✅ | ✅ |
| View context drawer | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |
| Export AY Change Report | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/fee-structure/revisions/` | JWT (G1+) | Revision list |
| GET | `/api/v1/group/{id}/finance/fee-structure/revisions/{rid}/` | JWT (G1+) | Revision context |
| GET | `/api/v1/group/{id}/finance/fee-structure/revisions/ay-comparison/` | JWT (G1+) | AY comparison table |
| GET | `/api/v1/group/{id}/finance/fee-structure/revisions/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../revisions/?branch=&change_type=` | `#revision-table` | `innerHTML` |
| Date range | `change` | GET `.../revisions/?from=&to=` | `#revision-table` | `innerHTML` |
| Context drawer | `click` | GET `.../revisions/{id}/` | `#drawer-body` | `innerHTML` |
| Pagination | `click` | GET `.../revisions/?page=` | `#revision-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
