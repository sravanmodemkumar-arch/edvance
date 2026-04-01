# 24 — Hosteler Fee Configuration

- **URL:** `/group/finance/fee-structure/hosteler-config/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Fee Structure Manager G3 (primary) · CFO G1 (view)

---

## 1. Purpose

Hosteler fee configuration is the most complex fee setup in the group because it varies across four dimensions: gender (Boys / Girls) × accommodation type (AC / Non-AC). Each combination has distinct fee components: hostel admission, monthly hostel, mess, laundry, medical, and any other campus services. This page provides a dedicated, structured interface for configuring and publishing hosteler fees per branch.

Critical compliance requirement: boys and girls hostel fees must be tracked separately (separate campus infrastructure). AC hostels have different utility and maintenance costs than Non-AC. Scholarship and concession overlays are tracked separately on Page 27.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Structure Manager | G3 | Full CRUD + publish |
| Group CFO | G1 | Read-only |
| Group Finance Manager | G1 | Read-only |
| Group Hostel Welfare Officer | G3 | Read — mess fee + hostel fee only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Structure → Hosteler Fee Configuration
```

### 3.2 Page Header
- **Title:** `Hosteler Fee Configuration`
- **Subtitle:** `AY [Year] · [N] Branches with Hostels`
- **Right-side controls:** `[AY ▾]` `[Branch ▾]` `[Export ↓]`

---

## 4. Main Table — Hosteler Fee Status by Branch

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Has Hostel | Badge: Yes / No | ✅ |
| Boys Non-AC Configured | Badge: Published · Draft · Missing | ✅ |
| Boys AC Configured | Badge | ✅ |
| Girls Non-AC Configured | Badge | ✅ |
| Girls AC Configured | Badge | ✅ |
| Status | Badge: All Published · Partial · Missing | ✅ |
| Actions | Configure · View | — |

**Filters:** Branch · Has Hostel · Status
**Search:** Branch name
**Pagination:** 20 rows/page

---

## 5. Drawers

### 5.1 Drawer: `hosteler-config` — Configure Hosteler Fees
- **Trigger:** Configure action
- **Width:** 900px

**Tabs:** `Boys Non-AC` | `Boys AC` | `Girls Non-AC` | `Girls AC`

Each tab contains:

| Fee Component | Amount (₹) | Frequency | Notes |
|---|---|---|---|
| Hostel Admission Fee | Input | One-time | Refundable deposit note |
| Monthly Hostel Rent | Input | Monthly | |
| Mess Fee — Veg | Input | Monthly | |
| Mess Fee — Non-Veg | Input | Monthly | (if applicable) |
| Laundry Charges | Input | Monthly | |
| Medical Room Fee | Input | Annual | |
| Electricity Charges (AC only) | Input | Monthly | AC tab only |
| Generator Charges | Input | Monthly | |
| Caution Deposit | Input | One-time refundable | |
| [+ Add Custom Component] | | | |

**Annual Total (auto-calculated):** ₹[X] per year per student

**Payment Schedule:**
- Term-wise split: % per term
- Late fee: ₹[X]/month after [N] days

**Actions:**
- [Save as Draft] [Publish This Tab] [Publish All Tabs]

### 5.2 Drawer: `hosteler-fee-view` — View Published Fees (read-only version)
- Same layout, no edit fields

---

## 6. Charts

### 6.1 Hosteler Fee Comparison Across Branches (Grouped Bar)
- **Groups:** Boys Non-AC · Boys AC · Girls Non-AC · Girls AC
- **X-axis:** Branches
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Fees published | "Hosteler fees published for [Branch] — [Category]." | Success | 4s |
| All tabs published | "All hosteler fee categories published for [Branch]." | Success | 4s |
| Draft saved | "Hosteler fee draft saved for [Branch] — [Category]." | Info | 3s |
| Validation error | "Mess fee cannot be zero for [Category]." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| No hostel branches | "No hostel branches" | "No branches have hostels configured for this AY." |
| Branch has no hostel | "Hostel not applicable" | "This branch has no hostel students. Mark as Day Scholar only." |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Config drawer | Spinner + skeleton tabs |
| Publish | Spinner on publish button |

---

## 10. Role-Based UI Visibility

| Element | Fee Struct Mgr G3 | CFO G1 | Hostel Officer G3 |
|---|---|---|---|
| [Configure] action | ✅ | ❌ | ❌ |
| [Publish] | ✅ | ❌ | ❌ |
| View fees | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/fee-structure/hosteler/` | JWT (G1+) | Branch hosteler status |
| GET | `/api/v1/group/{id}/finance/fee-structure/hosteler/{bid}/` | JWT (G1+) | Branch hosteler fee detail |
| PUT | `/api/v1/group/{id}/finance/fee-structure/hosteler/{bid}/{category}/` | JWT (G3) | Update fees |
| POST | `/api/v1/group/{id}/finance/fee-structure/hosteler/{bid}/{category}/publish/` | JWT (G3) | Publish category |
| POST | `/api/v1/group/{id}/finance/fee-structure/hosteler/{bid}/publish-all/` | JWT (G3) | Publish all |
| GET | `/api/v1/group/{id}/finance/fee-structure/hosteler/export/` | JWT (G1+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Config drawer | `click` | GET `.../hosteler/{bid}/config-form/` | `#drawer-body` | `innerHTML` |
| Tab switch (Boys AC etc.) | `click` | GET `.../hosteler/{bid}/{category}/` | `#fee-tab-body` | `innerHTML` |
| Publish category | `click` | POST `.../hosteler/{bid}/{category}/publish/` | `#category-tab-status` | `outerHTML` |
| Save draft | `submit` | PUT `.../hosteler/{bid}/{category}/` | `#drawer-footer` | `outerHTML` |
| AY switch | `change` | GET `.../hosteler/?ay=` | `#hosteler-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
