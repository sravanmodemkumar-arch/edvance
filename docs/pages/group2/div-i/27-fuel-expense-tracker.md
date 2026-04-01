# 27 — Fuel & Expense Tracker

> **URL:** `/group/transport/operations/fuel/`
> **File:** `27-fuel-expense-tracker.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Fleet Manager (primary) · Transport Director · CFO (view)

---

## 1. Purpose

Tracks fuel consumption and transport operational expenses across the entire fleet — fuel fills, mileage, fuel efficiency (km/litre), toll charges, and miscellaneous operational costs. Helps the Fleet Manager identify abnormal fuel consumption (potential theft or inefficiency) and provides the CFO with accurate transport cost data.

This page is financial-operational. Fuel cost is typically 40–60% of total transport operating cost. A large group's fleet (300+ buses) burns ₹10–30 lakhs/month in fuel.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Fleet Manager | G3 | Full — record, edit, generate reports | Primary owner |
| Group Transport Director | G3 | View + approve large expenses | Oversight |
| Group CFO | G1 | Read-only — cost reporting | View only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Fuel & Expense Tracker
```

### 3.2 Page Header
- **Title:** `Fuel & Expense Tracker`
- **Subtitle:** `[Month] · Total Fuel Cost: ₹[N] · Avg Efficiency: [N] km/L · Fleet: [N] buses`
- **Right controls:** `+ Record Fuel Fill` · `+ Record Expense` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Bus fuel efficiency drops > 20% vs baseline | "Bus [No]'s fuel efficiency has dropped > 20%. Possible engine issue." | Amber |
| Monthly fuel spend > budget threshold | "[Branch] transport fuel spend is [N]% over monthly budget." | Amber |
| Expense without receipt uploaded | "[N] expense records have no receipt uploaded." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Fuel Cost (Month) | ₹ | Blue |
| Fuel Consumed (Month) | Litres | Blue |
| Avg Fleet Efficiency | km/litre | Green ≥ 8 · Yellow 5–8 · Red < 5 |
| Toll & Misc Expenses | ₹ | Blue |
| Total Transport Opex (Month) | ₹ fuel + maintenance + misc | Blue |
| Cost per Student per Month | ₹ | Blue (informational) |

---

## 5. Sections

### 5.1 Fuel Fill Records Table

**Filters:** Branch · Bus No · Date Range · Fuel Type (Diesel / CNG / Electric)

**Columns:** Date · Bus No · Branch · Odometer Reading (km) · Litres Filled · Rate/Litre (₹) · Amount (₹) · Fuel Station · Driver · Receipt Uploaded · Actions (View · Edit)

**Pagination:** Server-side · 25/page.

---

### 5.2 Fleet Fuel Efficiency Table

> Per-vehicle efficiency metrics — helps identify underperformers.

**Columns:** Bus No · Branch · Route · Fuel Type · Baseline Efficiency (km/L) · Current Month Avg (km/L) · Variance % · Total Km (Month) · Total Fuel Cost (Month) · Status (Normal / Alert)

**Default sort:** Variance % descending (worst efficiency drop first).

---

### 5.3 Expense Records (Non-Fuel)

> Toll charges, parking, cleaning, miscellaneous operational.

**Columns:** Date · Bus No · Branch · Expense Type · Amount (₹) · Description · Receipt Uploaded · Recorded By · Actions (View · Edit)

---

### 5.4 Monthly Cost Chart

**Chart — Cost Breakdown (Pie)**
- Fuel / Maintenance / Toll & Misc / Driver Wages (if tracked)

**Chart — Monthly Fuel Spend Trend (Line)**
- 12-month fuel spend with budget line

---

## 6. Drawers

### 6.1 Drawer: `record-fuel-fill`
- **Width:** 520px
- **Fields:** Bus No (searchable) · Date · Odometer Reading (km) · Litres Filled · Rate per Litre (₹) · Amount (₹, auto-calculated) · Fuel Type · Fuel Station Name · Driver Name · Upload Receipt (optional)

### 6.2 Drawer: `record-expense`
- **Width:** 520px
- **Fields:** Bus No · Date · Expense Type (Toll / Parking / Cleaning / Repair — minor / Other) · Amount (₹) · Description · Upload Receipt

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Fuel fill recorded | "Fuel fill recorded for [Bus No]. Amount: ₹[N]." | Success | 4s |
| Fuel fill failed | "Failed to record fuel fill. Check odometer reading and litres filled." | Error | 5s |
| Expense recorded | "Expense recorded for [Bus No]." | Success | 4s |
| Expense failed | "Failed to record expense. Please retry." | Error | 5s |
| Efficiency alert | "Fuel efficiency alert for [Bus No]. Fleet Manager notified." | Warning | 5s |
| Export failed | "Export failed. Please try again." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No records this month | "No Fuel Records This Month" | "Record the first fuel fill to start tracking." | [+ Record Fuel Fill] |
| No filter results (fuel) | "No Fuel Records Match Filters" | "Adjust branch, bus number, or date range filters." | [Clear Filters] |
| No filter results (expenses) | "No Expense Records Match Filters" | "Adjust branch or expense type filters." | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + fuel table + efficiency table + charts |
| Filter/search | Table body skeleton |
| Record drawer | 520px skeleton |

---

## 10. Role-Based UI Visibility

| Element | Fleet Manager G3 | Transport Director G3 | CFO G1 |
|---|---|---|---|
| Record Fuel Fill | ✅ | ❌ | ❌ |
| Record Expense | ✅ | ❌ | ❌ |
| Approve Large Expense | ❌ | ✅ | ❌ |
| View All Data | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/fuel/` | JWT (G3+) | Fuel fill records |
| POST | `/api/v1/group/{group_id}/transport/fuel/` | JWT (G3+) | Record fuel fill |
| GET | `/api/v1/group/{group_id}/transport/fuel/efficiency/` | JWT (G3+) | Fleet efficiency table |
| GET | `/api/v1/group/{group_id}/transport/expenses/` | JWT (G3+) | Non-fuel expenses |
| POST | `/api/v1/group/{group_id}/transport/expenses/` | JWT (G3+) | Record expense |
| GET | `/api/v1/group/{group_id}/transport/fuel/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/fuel/cost-charts/` | JWT (G3+) | Chart data |
| GET | `/api/v1/group/{group_id}/transport/fuel/export/` | JWT (G3+) | Export fuel records |
| GET | `/api/v1/group/{group_id}/transport/expenses/export/` | JWT (G3+) | Export expense records |

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Fuel table filter | `click` | GET `.../fuel/?{filters}` | `#fuel-table-section` | `innerHTML` |
| Fuel table sort | `click` on header | GET `.../fuel/?sort={col}&dir={asc/desc}` | `#fuel-table-section` | `innerHTML` |
| Fuel table pagination | `click` | GET `.../fuel/?page={n}` | `#fuel-table-section` | `innerHTML` |
| Expense table filter | `click` | GET `.../expenses/?{filters}` | `#expense-table-section` | `innerHTML` |
| Expense table sort | `click` on header | GET `.../expenses/?sort={col}&dir={asc/desc}` | `#expense-table-section` | `innerHTML` |
| Expense table pagination | `click` | GET `.../expenses/?page={n}` | `#expense-table-section` | `innerHTML` |
| Record fuel fill submit | `click` | POST `.../fuel/` | `#fuel-table-section` | `innerHTML` |
| Record expense submit | `click` | POST `.../expenses/` | `#expense-table-section` | `innerHTML` |
| Export fuel | `click` | GET `.../fuel/export/` | `#export-btn` | `outerHTML` |

> **Audit trail:** All write actions (record fuel fill, record expense) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
