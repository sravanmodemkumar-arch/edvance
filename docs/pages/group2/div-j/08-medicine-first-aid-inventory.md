# 08 — Medicine & First Aid Inventory

> **URL:** `/group/health/inventory/`
> **File:** `08-medicine-first-aid-inventory.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Medical Coordinator (primary) · School Medical Officer

---

## 1. Purpose

Track medicine and first aid supply inventory across all branch medical rooms. Set minimum stock thresholds for every item at group level, monitor current stock quantities against those thresholds, flag critical shortages and expired items, and log all replenishments and stock movements.

Every branch medical room must maintain a defined minimum set of medicines and first aid supplies at all times — core medicines (paracetamol, ORS, antihistamines, antiseptic), first aid essentials (bandages, gauze, plasters, gloves), and life-saving equipment supplies (AED pads, oxygen). The Medical Coordinator sets group-wide minimum standards; branch nurses manage day-to-day stock levels. Any branch running out of essential items before a replenishment can arrive creates a patient care risk. Expired medicines must be tracked and disposed of following pharmacy regulations.

Scale: 50–100 medicine/supply line items × 20–50 branches × 1–3 medical rooms = 1,000–15,000 individual stock records group-wide. Replenishments occur monthly or on-demand for critical items.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Medical Coordinator | G3 | Full — set standards, view all branches, approve disposal, bulk operations | Primary owner |
| Group School Medical Officer | G3 | Update own branch stock, request replenishment, view all | Cannot set group-wide standards or approve disposal group-wide |
| Group Emergency Response Officer | G3 | Read only — for emergency supply verification | View current stock levels only |
| Branch Nurse (Branch role) | Branch | Update own branch stock, request replenishment | Only own branch/room |
| All other roles | — | — | No access |

> **Access enforcement:** Django view decorator `@require_role('medical_coordinator', 'school_medical_officer', 'emergency_response_officer')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Medicine & First Aid Inventory
```

### 3.2 Page Header
- **Title:** `Medicine & First Aid Inventory`
- **Subtitle:** `[N] Branches Monitored · [N] Total Line Items · Last updated: [timestamp]`
- **Right controls:** `+ Add Item` · `Advanced Filters` · `Bulk Actions ▾` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Medicine expired — dispose immediately | "[N] expired medicine items across [N] branches require immediate disposal." | Red |
| Branch with zero stock of essential item | "[Branch] has zero stock of essential item '[Item Name]'. Replenishment needed immediately." | Red |
| Replenishment overdue | "[N] replenishment requests raised > 7 days ago with no fulfilment." | Red |
| First aid kit incomplete | "[Branch] first aid kit is missing required items: [list]. Cannot be considered compliant." | Amber |
| Items below threshold | "[N] items across [N] branches are below minimum threshold. Review stock." | Amber |
| Stock check overdue | "[Branch] stock has not been checked in > 30 days." | Amber |

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule |
|---|---|---|
| Branches with Critical Stock Alert | Branches where any essential item is at zero or below 3 days supply | Green = 0 · Yellow 1–3 · Red > 3 |
| Expired Items (to dispose) | Total expired item entries group-wide | Green = 0 · Yellow 1–10 · Red > 10 |
| Items Below Threshold (group-wide) | Total item-branch combinations where current qty < minimum | Green = 0 · Yellow 1–20 · Red > 20 |
| Replenishments Due This Week | Replenishment requests or auto-triggered orders expected this week | Blue always |
| Total Active Line Items | Distinct medicine/supply items tracked (group standard list) | Blue always |
| Branches Fully Stocked | Branches where all items meet or exceed minimum threshold | Green = all · Yellow < 90% · Red < 75% |

---

## 5. Main Table — Branch-wise Stock Summary

> Level 1 view: one row per branch medical room. Click to drill into item-level detail.

**Search:** Branch name, medical room name. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Stock Health | Radio | All / Fully Stocked / Warning / Critical |
| Last Stock Check | Date range | From — To |
| Has Expired Items | Checkbox | Show branches with expired items only |
| Has Critical Alert | Checkbox | Show branches with zero-stock essential items only |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | |
| Medical Room | ✅ | Room name; link → item-level detail view |
| Essential Medicines | ✅ | OK count / Total; colour-coded (all OK = Green, any issues = Yellow/Red) |
| First Aid | ✅ | OK count / Total |
| AED Status | ✅ | Supplies OK ✅ / Pads low ⚠ / Depleted ❌ |
| Last Stock Check | ✅ | Date; Red if > 30 days ago |
| Stock Health | ✅ | All OK (Green) / Warning ⚠ (Yellow) / Critical 🔴 (Red) |
| Actions | ❌ | View Stock · Update Stock · Request Order |

**Default sort:** Stock Health (Critical first), then Last Stock Check ascending (oldest check first).
**Pagination:** Server-side · 25/page.

---

## 6. Item-Level Detail View

> Level 2 view: triggered by clicking "View Stock" in Actions, or clicking the Medical Room link. Replaces or expands below the branch row (drills into the `branch-stock-detail` drawer).

### 6.1 Item-Level Table

**Search:** Item name. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Category | Checkbox | Medicine / First Aid / Equipment Supply |
| Status | Checkbox | OK / Low / Critical / Expired / Disposed |
| Essential Items | Checkbox | Show essential items only |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Item Name | ✅ | |
| Category | ✅ | Medicine / First Aid / Equipment Supply |
| Essential | ✅ | ✅ Yes / — No |
| Required Qty | ✅ | Group-standard minimum |
| Current Qty | ✅ | Current stock count |
| Unit | ✅ | Tablets / Strips / Bottles / Rolls / Pairs / Units |
| Expiry Date | ✅ | Date; Red if expired, Orange if expiring within 30 days |
| Status | ✅ | ✅ OK (Green) / ⚠ Low (Yellow) / 🔴 Critical (Red) / Expired (Red strikethrough) |
| Last Updated | ✅ | Date of last stock count |
| Actions | ❌ | Update Stock · Mark Disposed |

**Bulk actions (item level):** Mark selected as Disposed (expired batch); Export item list for this room.

---

## 7. Drawers

### 7.1 Drawer: `branch-stock-detail` — Branch Room Full Inventory
- **Trigger:** Actions → View Stock · Medical Room link
- **Width:** 720px
- **Tabs:** Medicines · First Aid · Equipment Supplies · Replenishment History

**Medicines tab:**
- Full item-level table for Category = Medicine
- Colour-coded rows: OK (no highlight) / Low (Yellow row) / Critical (Red row) / Expired (Red row with strikethrough on expiry date)
- Essentials shown first, then alphabetical
- "Update Stock" inline button per row

**First Aid tab:**
- Same structure for Category = First Aid
- First Aid Kit completeness score shown at top: [N]/[Required] items at acceptable level

**Equipment Supplies tab:**
- Same structure for Category = Equipment Supply (AED pads, oxygen refills, etc.)
- Items linked to equipment in medical room register where applicable

**Replenishment History tab:**
- All past replenishment requests and fulfilments for this room
- Columns: request date, requested by, items and quantities, priority, status, fulfilment date, fulfilled by, notes

---

### 7.2 Drawer: `stock-update` — Update Stock Level for Item
- **Trigger:** "Update Stock" in Actions column (any level), or inline row button
- **Width:** 560px

**Fields:**
| Field | Type | Notes |
|---|---|---|
| Branch | Select | Pre-filled from context; read-only if launched from row |
| Medical Room | Select | Auto-filtered to branch; read-only if from row |
| Item | Select + search | Type-ahead from standard item list; pre-filled from row |
| Update Type | Radio | Stock Count (full recount) / Addition (new stock received) / Adjustment (correction) |
| New Quantity | Number | Required; must be ≥ 0 |
| Batch Number | Text | Required for Medicines; optional for First Aid |
| Expiry Date | Date | Required for Medicines; optional for First Aid |
| Updated By | Text | Default: current user |
| Date of Update | Date | Default: today |
| Notes | Textarea | Optional; e.g., "Received monthly replenishment from pharmacy" |

**Validation:** New Quantity cannot be negative. If Expiry Date is in the past → warning "This batch is already expired. Consider using 'Mark Disposed' instead."

---

### 7.3 Drawer: `replenishment-request` — Raise Replenishment Order
- **Trigger:** Actions → Request Order · or Quick Action in dashboard
- **Width:** 580px

**Fields:**
| Field | Type | Notes |
|---|---|---|
| Branch | Select | Required |
| Medical Room | Select | Auto-filtered |
| Items List | Repeating rows | Item name (select) + Required Qty + Notes per item |
| Auto-populate from critical items | Button | "Add all Critical/Low items from this room" — pre-fills items below threshold |
| Priority | Select | Urgent (deliver within 2 days) / Normal (within 7 days) |
| Notes | Textarea | Any special instructions |
| Send To | Select | Medical Coordinator / Branch Principal / Both |
| Requested By | Auto | Current user |

**System behaviour on submit:** Email/notification sent to selected recipient(s). Replenishment request logged with timestamp. Status set to Pending.

---

### 7.4 Modal: `dispose-expired` — Record Disposal of Expired Items
- **Trigger:** Actions → Mark Disposed · Bulk action "Mark selected as Disposed"
- **Width:** 460px

**Display:** Summary list of selected expired items with branch, room, item name, expiry date, quantity.

**Fields:**
| Field | Type | Notes |
|---|---|---|
| Disposal Date | Date | Default: today |
| Disposal Method | Select | Destroy on Premises / Return to Pharmacy / Hand to Approved Agency |
| Disposed By | Text | Name of person conducting disposal |
| Witnessed By | Text | Second person name (recommended for controlled substances) |
| Notes | Textarea | |

**Warning text:** "Disposing expired medicines is a regulated activity. Ensure disposal follows [State] Pharmacy Act guidelines. Keep physical disposal certificate on file."

**On confirm:** All selected items have their Status updated to Disposed, quantity set to 0, and a disposal record is logged in the Replenishment History of the affected room.

---

## 8. Bulk Actions

| Action | Description | Role Required |
|---|---|---|
| Export branch stock report | Download current stock levels for selected branches as XLSX | Medical Coordinator, School Medical Officer |
| Bulk mark disposed | Dispose all expired items across selected branches in one operation | Medical Coordinator only |
| Set threshold (group standard) | Update minimum required quantity for a selected item across all branches | Medical Coordinator only |
| Generate replenishment list | Auto-generate order list for all items below threshold across selected branches | Medical Coordinator, School Medical Officer |

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Stock updated | "Stock updated for [Item] at [Room], [Branch]. New qty: [N]." | Success | 4s |
| Replenishment request submitted | "Replenishment request raised for [Branch]. Priority: [Urgent/Normal]." | Success | 5s |
| Items disposed | "[N] expired item(s) disposed at [Branch]. Records updated." | Info | 5s |
| Threshold updated | "Minimum threshold updated for '[Item]' — new standard: [N] [unit]. Applied to all branches." | Success | 5s |
| Expired item detected on save | "Warning: Batch for [Item] at [Branch] expires on [date]. Consider disposal." | Warning | 6s |
| Export prepared | "Inventory export ready for download." | Info | 4s |
| Critical stock auto-alert | "Critical stock alert: [Item] at [Branch] has reached zero." | Warning | 8s |

---

## 10. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No inventory records | "No Inventory Data" | "No stock items have been set up for any branch yet. Start by adding the group standard item list." | [+ Add Item] |
| No filter results | "No Rooms Match Filters" | "Try adjusting the branch, stock health, or date filters." | [Clear Filters] |
| No critical alerts | "All Stock Levels Healthy" | "All branches have medicine and first aid stock at or above minimum thresholds." | — |
| No expired items | "No Expired Items Found" | "No expired medicines or supplies have been flagged across any branch." | — |
| No replenishment history | "No Replenishment History" | "No replenishment orders have been placed for this room yet." | [Request Replenishment] |
| Room has no items configured | "No Items in This Room" | "No stock items have been assigned to this medical room." | [Add Items] |

---

## 11. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + branch summary table skeleton (15 rows × 8 columns) + alerts |
| Branch summary filter/search | Table body skeleton (10 rows) |
| Item-level drawer open | 720px drawer skeleton; tabs load lazily |
| Medicines tab load | Table skeleton (20 rows × 10 columns) with shimmer |
| Replenishment History tab | Table skeleton (8 rows × 8 columns) |
| Stock update drawer | 560px form skeleton |
| Replenishment request drawer | 580px form skeleton; "Add critical items" button shows spinner when populating |
| Dispose modal | Item list skeleton + form skeleton below |
| Export generation | Full-page non-blocking toast with progress indication |

---

## 12. Role-Based UI Visibility

| Element | Medical Coordinator G3 | School Medical Officer G3 | Emergency Response Officer G3 |
|---|---|---|---|
| Update Stock (any branch) | ✅ | ❌ | ❌ |
| Update Stock (own branch) | ✅ | ✅ | ❌ |
| Request Replenishment | ✅ | ✅ (own branch) | ❌ |
| Set Group-Wide Threshold | ✅ | ❌ | ❌ |
| Approve Disposal | ✅ | ❌ | ❌ |
| Record Disposal (own branch) | ✅ | ✅ | ❌ |
| View All Branches Stock | ✅ | ✅ | ✅ |
| Bulk Mark Disposed | ✅ | ❌ | ❌ |
| Generate Replenishment List | ✅ | ✅ | ❌ |
| Export Inventory Report | ✅ | ✅ | ❌ |
| Add New Item to Standard List | ✅ | ❌ | ❌ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/inventory/` | JWT (G3+) | Branch-wise stock summary list |
| GET | `/api/v1/group/{group_id}/health/inventory/kpis/` | JWT (G3+) | KPI card values |
| GET | `/api/v1/group/{group_id}/health/inventory/{room_id}/items/` | JWT (G3+) | Item-level stock for a specific room |
| PATCH | `/api/v1/group/{group_id}/health/inventory/{room_id}/items/{item_id}/` | JWT (Role 85, 86) | Update stock quantity |
| POST | `/api/v1/group/{group_id}/health/inventory/{room_id}/items/{item_id}/dispose/` | JWT (Role 85, 86) | Mark item batch as disposed |
| POST | `/api/v1/group/{group_id}/health/inventory/{room_id}/items/{item_id}/dispose/bulk/` | JWT (Role 85) | Bulk dispose expired items |
| POST | `/api/v1/group/{group_id}/health/inventory/replenishment/` | JWT (Role 85, 86) | Submit replenishment request |
| GET | `/api/v1/group/{group_id}/health/inventory/{room_id}/replenishment-history/` | JWT (G3+) | Replenishment history for room |
| PATCH | `/api/v1/group/{group_id}/health/inventory/items/{item_id}/threshold/` | JWT (Role 85) | Update group-wide minimum threshold for item |
| GET | `/api/v1/group/{group_id}/health/inventory/items/` | JWT (Role 85) | Group standard item list |
| POST | `/api/v1/group/{group_id}/health/inventory/items/` | JWT (Role 85) | Add new item to group standard list |
| GET | `/api/v1/group/{group_id}/health/inventory/export/` | JWT (Role 85, 86) | Async inventory export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Branch summary search | `input delay:300ms` | GET `.../inventory/?q={val}` | `#branch-stock-table-body` | `innerHTML` |
| Branch summary filter | `click` | GET `.../inventory/?{filters}` | `#branch-stock-table-section` | `innerHTML` |
| Pagination (branch list) | `click` | GET `.../inventory/?page={n}` | `#branch-stock-table-section` | `innerHTML` |
| Open branch stock drawer | `click` on Medical Room link | GET `.../inventory/{room_id}/items/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch | `click` | GET `.../inventory/{room_id}/items/?tab={name}` | `#drawer-tab-content` | `innerHTML` |
| Item-level search (in drawer) | `input delay:300ms` | GET `.../inventory/{room_id}/items/?q={val}` | `#item-table-body` | `innerHTML` |
| Item-level filter (in drawer) | `click` | GET `.../inventory/{room_id}/items/?{filters}` | `#item-table-body` | `innerHTML` |
| Inline stock update (from drawer) | `click` Update on item row | GET `.../inventory/{room_id}/items/{item_id}/?edit=1` | `#item-row-{item_id}` | `outerHTML` |
| Save inline stock update | `click` Save | PATCH `.../inventory/{room_id}/items/{item_id}/` | `#item-row-{item_id}` | `outerHTML` |
| Open full stock-update drawer | `click` (from main table) | GET `.../inventory/stock-update-form/?room={id}&item={id}` | `#drawer-body` | `innerHTML` |
| Auto-populate replenishment items | `click` "Add Critical Items" | GET `.../inventory/{room_id}/items/?status=critical,low` | `#replenishment-items-list` | `innerHTML` |
| Submit stock update | `click` | PATCH `.../inventory/{room_id}/items/{item_id}/` | `#stock-table-section` | `innerHTML` |
| Submit disposal | `click` | POST `.../inventory/{room_id}/items/{item_id}/dispose/` | `#item-row-{item_id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
