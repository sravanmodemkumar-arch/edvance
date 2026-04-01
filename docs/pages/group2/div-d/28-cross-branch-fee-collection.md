# 28 — Cross-Branch Fee Collection Dashboard

- **URL:** `/group/finance/collection/dashboard/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Fee Collection Head G3 (primary) · CFO G1 · Finance Manager G1

---

## 1. Purpose

The Cross-Branch Fee Collection Dashboard is the operational view of real-time fee collection across all branches. It tracks daily collection velocity, term-wise collection progress, payment mode breakdown (cash, online, cheque), and branch-level collection rates. The Fee Collection Head uses this to identify which branches need immediate intervention and to run collection drives.

Unlike the CFO Revenue Report (Page 13) which shows cumulative totals, this page is action-oriented — it shows today's collection, this week's trend, and which branches are falling behind their daily targets.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Collection Head | G3 | Full read + initiate reminders |
| Group CFO | G1 | Read — summary + charts |
| Group Finance Manager | G1 | Read — all sections |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Collection → Cross-Branch Dashboard
```

### 3.2 Page Header
- **Title:** `Cross-Branch Fee Collection Dashboard`
- **Subtitle:** `AY [Year] · Term [N] · Today: [Date]`
- **Right-side controls:** `[AY ▾]` `[Term ▾]` `[Branch ▾]` `[Send Bulk Reminder]` `[Export ↓]`

**HTMX auto-refresh:**
```html
hx-get=".../collection/dashboard/kpis/"
hx-trigger="every 5m"
```

---

## 4. KPI Summary Bar

| Card | Metric | Notes |
|---|---|---|
| Today's Collection | ₹ | Across all branches |
| This Term Collection | ₹ | YTD term |
| Term Target | ₹ | From budget |
| Achievement % | % | This Term / Target |
| Online Collections | ₹ (%) | Online payment ratio |
| Branches Below 80% | Count | Red if > 0 |

---

## 5. Section 5.1 — Branch Collection Status

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Term Target | ₹ | ✅ |
| Collected (Term) | ₹ | ✅ |
| Collection % | % badge | ✅ |
| Today's Collection | ₹ | ✅ |
| Outstanding | ₹ | ✅ |
| Defaulters | Count | ✅ |
| Payment Mode Split | Inline bar: Online · Cash · Cheque | — |
| Actions | View · Send Reminder | — |

**Filters:** Branch · Term · Collection % range · Student Type
**Search:** Branch name
**Pagination:** 25 rows/page · Sort: Collection % asc (worst first)

---

## 5.2 Section 5.2 — Payment Mode Analysis

| Payment Mode | Today (₹) | This Week (₹) | This Month (₹) | % of Total |
|---|---|---|---|---|
| Online (UPI / Net Banking) | ₹ | ₹ | ₹ | % |
| Cheque | ₹ | ₹ | ₹ | % |
| Cash | ₹ | ₹ | ₹ | % |
| DD | ₹ | ₹ | ₹ | % |

---

## 5.3 Section 5.3 — Installment Plan Status

| Branch | Students on Installment Plan | Installments Due | Installments Paid | Overdue |
|---|---|---|---|---|
| [Branch A] | [N] | [N] | [N] | [N] (red if >0) |

---

## 6. Charts

### 6.1 Daily Collection Trend (Line — last 30 days)
- **Series:** Total collection/day
- **X-axis:** Dates
- **Export:** PNG

### 6.2 Branch Collection Rate (Horizontal Bar)
- **Y-axis:** Branches (sorted by collection % asc)
- **X-axis:** Collection %
- **Benchmark line:** 90%

### 6.3 Payment Mode Split (Donut)
- **Segments:** Online · Cheque · Cash · DD

---

## 7. Drawers

### 7.1 Drawer: `send-reminder` — Send Fee Reminder
- **Trigger:** Send Reminder (per branch) or [Send Bulk Reminder]

| Field | Type | Required |
|---|---|---|
| Branches | Multi-select | ✅ |
| Target Segment | Select: All Defaulters · Specific Term Defaulters · Installment Overdue | ✅ |
| Channel | Multi-select: WhatsApp · SMS · In-app | ✅ |
| Message | Textarea (template pre-filled) | ✅ |
| Scheduled For | Datetime | ❌ (default: now) |

- [Cancel] [Send Reminder]

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Reminder sent | "Fee reminders sent to [N] students across [M] branches." | Info | 4s |
| Export | "Collection dashboard exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No collections today | "No collections today" | "No fee payments recorded for today yet." |
| All branches at 100% | "Full collection achieved" | "All branches have 100% collection for this term." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table + chart skeletons |
| Auto-refresh (5m) | Subtle inline refresh indicator |
| Term switch | Table + chart skeletons |
| Reminder drawer | Spinner + form skeleton |

---

## 11. Role-Based UI Visibility

| Element | Collection Head G3 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [Send Bulk Reminder] | ✅ | ❌ | ❌ |
| [Send Reminder] per branch | ✅ | ❌ | ❌ |
| Full dashboard | ✅ | ✅ | ✅ |
| Payment mode section | ✅ | ✅ | ✅ |
| Installment section | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/collection/dashboard/kpis/` | JWT (G1+) | KPI cards (real-time) |
| GET | `/api/v1/group/{id}/finance/collection/dashboard/branch-status/` | JWT (G1+) | Branch table |
| GET | `/api/v1/group/{id}/finance/collection/dashboard/payment-modes/` | JWT (G1+) | Payment mode split |
| GET | `/api/v1/group/{id}/finance/collection/dashboard/installments/` | JWT (G1+) | Installment status |
| GET | `/api/v1/group/{id}/finance/collection/dashboard/charts/` | JWT (G1+) | Chart data |
| POST | `/api/v1/group/{id}/finance/collection/send-reminder/` | JWT (G3) | Send reminders |
| GET | `/api/v1/group/{id}/finance/collection/dashboard/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../dashboard/kpis/` | `#kpi-bar` | `innerHTML` |
| Term switch | `change` | GET `.../dashboard/?term=` | `#collection-body` | `innerHTML` |
| Filter | `change` | GET `.../dashboard/branch-status/?branch=` | `#branch-table` | `innerHTML` |
| Reminder drawer | `click` | GET `.../collection/reminder-form/` | `#drawer-body` | `innerHTML` |
| Submit reminder | `submit` | POST `.../collection/send-reminder/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
