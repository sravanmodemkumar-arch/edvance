# 52 — Platform Usage & License Report

- **URL:** `/group/finance/eduforge-billing/usage/`
- **Template:** `portal_base.html`
- **Priority:** P2
- **Role:** EduForge Billing Coordinator G3 (primary) · CFO G1

---

## 1. Purpose

The Platform Usage & License Report gives the group visibility into actual EduForge platform usage versus licensed limits across all branches — active users, student records, storage, API calls, and feature adoption. This helps the Billing Coordinator identify under-utilised branches (right-sizing candidates), over-utilised branches (at risk of hitting limits), and ensure license compliance.

Usage data is fetched from the EduForge licensing API and displayed alongside billing costs, enabling ROI analysis per branch.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group EduForge Billing Coordinator | G3 | Full read |
| Group CFO | G1 | Read — cost and utilisation summary |
| Group Finance Manager | G1 | Read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → EduForge Billing → Platform Usage & License Report
```

### 3.2 Page Header
- **Title:** `Platform Usage & License Report`
- **Subtitle:** `[N] Branches · Last Sync: [Datetime] · Period: [Month]`
- **Right-side controls:** `[Month ▾]` `[Branch ▾]` `[Refresh ↻]` `[Export ↓]`

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Licensed Students | Count | Neutral |
| Actual Active Students | Count | Red if > licensed |
| Total Licensed Staff | Count | Neutral |
| Actual Active Staff | Count | Red if > licensed |
| Total Storage Licensed | GB | Neutral |
| Storage Used | GB | Red if > 90% |
| Avg Monthly Cost per Student | ₹ | Neutral |

---

## 5. Main Table — Branch Usage Summary

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text | ✅ | ✅ |
| Plan | Badge | ✅ | ✅ |
| Student Seats Licensed | Number | ✅ | — |
| Active Students | Number | ✅ | — |
| Student Utilisation | % (colour-coded) | ✅ | — |
| Staff Seats Licensed | Number | ✅ | — |
| Active Staff | Number | ✅ | — |
| Storage Licensed | GB | ✅ | — |
| Storage Used | GB | ✅ | — |
| Storage % | % (colour-coded) | ✅ | — |
| Monthly Cost | ₹ | ✅ | — |
| Cost per Active Student | ₹ | ✅ | — |
| Feature Adoption | % | ✅ | — |
| Actions | View Detail | — | — |

**Utilisation colour rules:**
- < 60%: Grey (under-utilised)
- 60–85%: Green
- 85–95%: Amber
- > 95%: Red

### 5.1 Filters
- Branch · Plan · Utilisation range · Storage %

### 5.2 Pagination
- 20 rows/page · Sort: Student Utilisation desc

---

## 6. Drawers

### 6.1 Drawer: `branch-usage-detail` — Branch Usage Detail
- **Width:** 760px

**Tabs:** Usage Overview · Feature Adoption · API Usage · Cost Breakdown

**Usage Overview Tab:**
- Monthly active users (MAU) trend (line chart — last 6 months)
- Student records: Active · Inactive · Archived
- Storage breakdown: Documents · Media · Backups

**Feature Adoption Tab:**
| Feature | Accessed Last 30 Days | Last Accessed |
|---|---|---|
| Admissions Module | ✅ | [Date] |
| Fee Collection | ✅ | [Date] |
| Academic Reports | ✅ | [Date] |
| Parent App | ❌ | Never |

**Cost Breakdown Tab:**
| Component | Cost |
|---|---|
| Base Plan | ₹[X] |
| Additional Seats | ₹[Y] |
| Storage Add-on | ₹[Z] |
| Total | ₹[Total] |

---

## 7. Charts

### 7.1 Platform Usage Heatmap — Branch vs Feature
- Rows: Branches · Columns: Features · Cell: % adoption (colour gradient)

### 7.2 Cost per Active Student by Branch (Bar)
- Useful for identifying expensive low-utilisation branches

### 7.3 Storage Utilisation Across Branches (Stacked Bar)

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Usage synced | "Usage data refreshed from EduForge API." | Info | 3s |
| Over-limit alert | "[Branch] has exceeded licensed seat count. Upgrade required." | Warning | 6s |
| Export | "Usage report exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| Sync not done | "Usage data not loaded" | "Click Refresh to fetch latest usage from EduForge." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Refresh | Progress bar: "Fetching usage data..." |
| Drawer | Spinner + tab skeleton |

---

## 11. Role-Based UI Visibility

| Element | Billing Coordinator G3 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [Refresh] | ✅ | ❌ | ❌ |
| View all branches | ✅ | ✅ | ✅ |
| Cost per student | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/billing/usage/` | JWT (G1+) | Usage summary |
| POST | `/api/v1/group/{id}/finance/billing/usage/refresh/` | JWT (G3) | Sync from EduForge |
| GET | `/api/v1/group/{id}/finance/billing/usage/{bid}/` | JWT (G1+) | Branch detail |
| GET | `/api/v1/group/{id}/finance/billing/usage/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month filter | `change` | GET `.../usage/?month=` | `#usage-table` | `innerHTML` |
| Refresh | `click` | POST `.../usage/refresh/` | `#usage-section` | `outerHTML` |
| Detail drawer | `click` | GET `.../usage/{id}/` | `#drawer-body` | `innerHTML` |
| Tab switch (detail) | `click` | GET `.../usage/{id}/?tab=features` | `#usage-tab-content` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
