# 49 — Branch Plan Manager

- **URL:** `/group/finance/eduforge-billing/plans/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** EduForge Billing Coordinator G3 (primary) · CFO G1

---

## 1. Purpose

The Branch Plan Manager is the master view of EduForge subscription plans assigned to each branch within the group. Each branch operates on a plan (Starter, Growth, Pro, Enterprise) that determines feature access, student seat count, and storage limits. The Billing Coordinator manages plan assignments, seat adjustments, trial extensions, and plan upgrades/downgrades.

This page tracks per-branch plan status, renewal dates, seat utilisation, and billing amounts — the source of truth for the group's EduForge subscription portfolio.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group EduForge Billing Coordinator | G3 | Full read + manage plans |
| Group CFO | G1 | Read — cost summary |
| Group Finance Manager | G1 | Read — billing totals |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → EduForge Billing → Branch Plan Manager
```

### 3.2 Page Header
- **Title:** `Branch Plan Manager`
- **Subtitle:** `[N] Branches · Total Annual Billing: ₹[X] · [Y] Renewals This Month`
- **Right-side controls:** `[Branch ▾]` `[Plan ▾]` `[Status ▾]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| Renewal due in ≤ 7 days | "[N] branch plan(s) renewing within 7 days. Review and confirm." | Amber |
| Seat limit exceeded | "[N] branch(es) have exceeded their plan seat limit." | Red |
| Plan expired | "[N] branch plan(s) have expired." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Branches | Count | Neutral |
| Active Plans | Count | Green |
| Expiring This Month | Count | Amber if > 0 |
| Total Monthly Billing | ₹ | Neutral |
| Seat Utilisation (Group Avg) | % | Red if > 95% |
| Overdue Renewals | Count | Red if > 0 |

---

## 5. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text | ✅ | ✅ |
| Current Plan | Badge: Starter · Growth · Pro · Enterprise | ✅ | ✅ |
| Plan Status | Badge: Active · Trial · Expired · Suspended | ✅ | ✅ |
| Start Date | Date | ✅ | — |
| Renewal Date | Date | ✅ | — |
| Days to Renewal | Number (red if ≤ 7) | ✅ | — |
| Student Seats | N / Max | ✅ | — |
| Staff Seats | N / Max | ✅ | — |
| Storage Used | GB / Max GB | ✅ | — |
| Monthly Cost | ₹ | ✅ | — |
| Annual Cost | ₹ | ✅ | — |
| Billing Mode | Badge: Monthly · Annual | ✅ | ✅ |
| Actions | View · Upgrade · Adjust Seats · Renew | — | — |

### 5.1 Filters
- Branch · Plan type · Status · Renewal month

### 5.2 Search
- Branch name

### 5.3 Pagination
- 20 rows/page · Sort: Renewal Date asc

---

## 6. Drawers

### 6.1 Drawer: `plan-detail` — Branch Plan Detail
- **Width:** 720px

**Plan Overview:**
- Branch · Current Plan · Status · Plan Period
- Student Seats: [Used] / [Max]
- Staff Seats: [Used] / [Max]
- Storage: [Used GB] / [Max GB]
- Add-ons: [List if any]
- Billing Contact · Invoice Email

**Feature Access List:**
| Feature | Included | Notes |
|---|---|---|
| Admissions Module | ✅ | Unlimited |
| Finance Module | ✅ | |
| Academic Module | ✅ | |
| Advanced Analytics | ❌ | Pro+ |
| API Access | ❌ | Enterprise |

**Invoice History (last 12 months):**
| Month | Amount | Status | Invoice |
|---|---|---|---|
| Mar 2026 | ₹[X] | Paid | [Download] |

### 6.2 Drawer: `plan-upgrade` — Upgrade / Change Plan
- **Width:** 640px

**Plan Selection:**

| Plan | Monthly | Annual | Student Seats | Storage |
|---|---|---|---|---|
| Starter | ₹[X] | ₹[Y] | 300 | 50 GB |
| Growth | ₹[X] | ₹[Y] | 1,000 | 200 GB |
| Pro | ₹[X] | ₹[Y] | 5,000 | 1 TB |
| Enterprise | Custom | Custom | Unlimited | Unlimited |

| Field | Type | Required |
|---|---|---|
| New Plan | Radio | ✅ |
| Billing Mode | Select: Monthly · Annual | ✅ |
| Effective Date | Date | ✅ |
| Notes / Reason | Textarea | ❌ |

**Proration summary:** "Upgrade from Growth → Pro effective [Date]. Proration credit: ₹[X]. Next invoice: ₹[Y]."

- [Cancel] [Confirm Upgrade]

### 6.3 Drawer: `seat-adjustment` — Adjust Seats
| Field | Type | Required |
|---|---|---|
| Student Seats | Number | ✅ |
| Staff Seats | Number | ✅ |
| Effective Date | Date | ✅ |
| Reason | Textarea | ✅ |

**Cost Impact:** "Adding [N] seats at ₹[X]/seat = ₹[Y]/month additional."

### 6.4 Drawer: `plan-renew` — Renew Plan
| Field | Type | Required |
|---|---|---|
| Renewal Period | Select: 1 month · 6 months · 12 months | ✅ |
| Plan (same or change) | Radio | ✅ |
| Billing Mode | Select | ✅ |
| Renewal Invoice No | Text (auto-gen) | — |

- [Confirm Renewal]

---

## 7. Charts

### 7.1 Plan Distribution (Donut)
- **Segments:** Starter · Growth · Pro · Enterprise

### 7.2 Monthly Billing Trend (Bar — Last 12 Months)

### 7.3 Seat Utilisation by Branch (Horizontal Bar)
- **Colour:** Green < 80% · Amber 80–95% · Red > 95%

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Plan upgraded | "Plan for [Branch] upgraded to [Plan] from [Date]." | Success | 4s |
| Seats adjusted | "Seats for [Branch] updated: [N] student, [N] staff." | Success | 4s |
| Plan renewed | "[Branch] plan renewed for [N] months." | Success | 4s |
| Seat limit alert | "[Branch] has exceeded seat limit. Please upgrade." | Warning | 6s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No branches | "No branches enrolled" | "No branch plans configured yet." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table |
| Drawer | Spinner + form skeleton |

---

## 11. Role-Based UI Visibility

| Element | Billing Coordinator G3 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [Upgrade Plan] | ✅ | ❌ | ❌ |
| [Adjust Seats] | ✅ | ❌ | ❌ |
| [Renew Plan] | ✅ | ❌ | ❌ |
| View all branches | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/billing/plans/` | JWT (G1+) | Branch plan list |
| GET | `/api/v1/group/{id}/finance/billing/plans/{bid}/` | JWT (G1+) | Plan detail |
| POST | `/api/v1/group/{id}/finance/billing/plans/{bid}/upgrade/` | JWT (G3) | Upgrade plan |
| POST | `/api/v1/group/{id}/finance/billing/plans/{bid}/seats/` | JWT (G3) | Adjust seats |
| POST | `/api/v1/group/{id}/finance/billing/plans/{bid}/renew/` | JWT (G3) | Renew plan |
| GET | `/api/v1/group/{id}/finance/billing/plans/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../plans/?plan=&status=` | `#plans-table` | `innerHTML` |
| Detail drawer | `click` | GET `.../plans/{id}/` | `#drawer-body` | `innerHTML` |
| Upgrade form | `click` | GET `.../plans/{id}/upgrade-form/` | `#drawer-body` | `innerHTML` |
| Submit upgrade | `submit` | POST `.../plans/{id}/upgrade/` | `#plan-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
