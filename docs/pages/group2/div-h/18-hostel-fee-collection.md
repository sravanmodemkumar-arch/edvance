# 18 — Hostel Fee Collection

> **URL:** `/group/hostel/fees/collection/`
> **File:** `18-hostel-fee-collection.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Hostel Fee Manager (primary) · Hostel Director (view)

---

## 1. Purpose

Operational fee collection monitoring across all hostelers and branches. Shows who has paid, who hasn't, how much is outstanding, late fees accrued, and enables batch reminder dispatch, fee hold actions, and waiver recording. The Fee Collection page is the daily operational surface for the Fee Manager — the Fee Structure page (17) is configuration, this is execution.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Fee Management  ›  Fee Collection
```

### 2.2 Page Header
- **Title:** `Hostel Fee Collection — [Month/Year]`
- **Month selector:** Previous / Next month navigation
- **Subtitle:** `[N] Hostelers Billed · Collected: ₹[N] ([N]%) · Outstanding: ₹[N] · Defaulters: [N]`
- **Right controls:** `Bulk Reminder ▾` · `Export Defaulter List` · `Advanced Filters`

---

## 3. KPI Cards (Month-specific)

| Card | Metric | Colour Rule |
|---|---|---|
| Billed This Month | ₹ total billed | Blue |
| Collected | ₹ received | Blue |
| Collection % | | Green ≥ 90% · Yellow 70–90% · Red < 70% |
| Outstanding | ₹ pending | Yellow > 0 |
| Late Fee Accrued | ₹ late fees in total outstanding | Blue |
| Defaulters (30d+) | Count | Green = 0 · Red > 0 |

---

## 4. Main Table — Fee Collection Status

**Search:** Hosteler name, room #, branch. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | |
| Gender | Radio | All / Boys / Girls |
| Status | Checkbox | Paid / Partial / Unpaid / Fee Hold / Waived |
| Outstanding Days | Radio | Any / > 15d / > 30d / > 60d / > 90d |
| Hostel Type | Checkbox | AC / Non-AC |
| Stream | Multi-select | |

**Columns:**
| Column | Sortable |
|---|---|
| Hosteler Name | ✅ |
| Gender | ✅ |
| Branch | ✅ |
| Room | ✅ |
| Fee Plan | ✅ |
| Billed Amount | ✅ |
| Paid Amount | ✅ |
| Outstanding | ✅ |
| Late Fee | ✅ |
| Days Overdue | ✅ (red if > 30) |
| Status | ✅ |
| Last Payment | ✅ |
| Actions | ❌ |

**Actions per row:** View · Send Reminder · Apply Fee Hold · Record Waiver · View History.

**Bulk actions:** Send WhatsApp reminder to selected · Export selected.

**Pagination:** Server-side · 25/page.

---

## 5. Drawers

### 5.1 Drawer: `hosteler-fee-detail`
- **Width:** 560px
- **Tabs:** Current Month · Payment History · Waivers · Actions
- **Payment History:** All payments logged (date, amount, mode, receipt #, logged by)
- **Waivers:** All approved waivers with reason and approver
- **Actions tab:** Record Payment · Send Reminder · Apply Fee Hold · Issue Exit Notice

### 5.2 Drawer: `record-payment`
- **Trigger:** Actions → Record Payment (manual cash/DD/NEFT payment)
- **Width:** 480px
- **Fields:** Amount · Payment Mode (Cash / DD (Demand Draft) / NEFT / UPI) · Reference # · Date · Receipt # · Note
- **Warning:** "Online payments auto-synced from payment gateway. Record here only for manual payments."

### 5.3 Modal: `fee-waiver`
- **Width:** 480px
- **Fields:** Waiver Type (Full / Partial) · Waiver Amount · Reason (required) · Supporting Document upload
- **Approver:** Auto-assigned as Hostel Director (for amounts > ₹5,000) or Fee Manager (≤ ₹5,000)

---

## 6. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Payment recorded | "Payment of ₹[N] recorded for [Name]." | Success | 4s |
| Reminder sent | "Payment reminder sent to [Name]'s registered parent number." | Info | 3s |
| Bulk reminders sent | "Reminders sent to [N] defaulters." | Info | 4s |
| Fee hold applied | "Fee hold applied for [Name]. Branch accountant notified." | Warning | 5s |
| Waiver submitted | "Waiver of ₹[N] submitted for approval." | Info | 4s |

---

## 7. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/fees/collection/` | JWT (G3+) | Fee collection table (paginated, filtered, month) |
| GET | `/api/v1/group/{group_id}/hostel/fees/hostelers/{id}/fee-detail/` | JWT (G3+) | Per-hosteler fee detail |
| POST | `/api/v1/group/{group_id}/hostel/fees/hostelers/{id}/payment/` | JWT (G3+) | Record manual payment |
| POST | `/api/v1/group/{group_id}/hostel/fees/hostelers/{id}/remind/` | JWT (G3+) | Send reminder |
| POST | `/api/v1/group/{group_id}/hostel/fees/reminders/bulk/` | JWT (G3+) | Bulk reminder |
| POST | `/api/v1/group/{group_id}/hostel/fees/hostelers/{id}/fee-hold/` | JWT (G3+) | Apply fee hold |
| POST | `/api/v1/group/{group_id}/hostel/fees/hostelers/{id}/waiver/` | JWT (G3+) | Submit waiver |
| GET | `/api/v1/group/{group_id}/hostel/fees/collection/kpis/?month={m}&year={y}` | JWT (G3+) | Month KPI cards |
| GET | `/api/v1/group/{group_id}/hostel/fees/collection/export/` | JWT (G3+) | Export defaulter list |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
