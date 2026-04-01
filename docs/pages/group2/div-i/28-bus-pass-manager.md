# 28 — Bus Pass Manager

> **URL:** `/group/transport/fees/bus-passes/`
> **File:** `28-bus-pass-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Transport Fee Manager (primary) · Route Planning Manager (view)

---

## 1. Purpose

Manages bus pass issuance, renewal, and revocation for all students enrolled in group transport. A bus pass authorises a student to board the assigned bus at their designated stop. Passes have validity periods (typically annual or per term) and are linked to the student's transport allocation record (Page 14).

Students with an expired or suspended bus pass must not be permitted to board. Bus drivers and conductors verify passes at point of boarding. Digital bus passes (QR-code based) are generated here; PDF passes can be downloaded and printed.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Fee Manager | G3 | Full — issue, renew, suspend, revoke | Primary owner |
| Group Route Planning Manager | G3 | Read — validate allocation before pass issue | View only |
| Branch Transport In-Charge | Branch G3 | Issue/renew for own branch only | Scoped |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Bus Pass Manager
```

### 3.2 Page Header
- **Title:** `Bus Pass Manager`
- **Subtitle:** `[N] Active Passes · [N] Expiring (7 days) · [N] Suspended · AY [current]`
- **Right controls:** `+ Issue Pass` · `Bulk Issue` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Passes expiring in 7 days | "[N] bus passes expire within 7 days. Renew before students are denied boarding." | Amber |
| Students on route without valid pass | "[N] students on active routes do not have a valid bus pass." | Red |
| Suspended students still boarding | "[N] students with suspended passes have active boarding records in GPS data." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Active Passes | Currently valid | Blue |
| Expiring ≤ 7 days | | Yellow > 0 · Red > 20 |
| Expiring ≤ 30 days | | Yellow > 0 |
| Suspended Passes | Due to fee default | Yellow > 0 |
| Expired Passes | Past validity with no renewal | Yellow > 0 |
| Passes Issued This Month | | Blue |

---

## 5. Main Table — Bus Pass Register

**Search:** Student name, pass number, roll number. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Status | Checkbox | Active / Expired / Suspended / Revoked |
| Expiry | Radio | All / Expiring ≤ 7d / Expiring ≤ 30d / Expired |
| Class | Multi-select | 1–12 |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Pass No | ✅ | QR-linked identifier |
| Student Name | ✅ | Link → student transport detail (Page 14) |
| Roll No | ✅ | |
| Class | ✅ | |
| Branch | ✅ | |
| Route | ✅ | |
| Pickup Stop | ✅ | |
| Issue Date | ✅ | |
| Expiry Date | ✅ | Colour-coded |
| Status | ✅ | Active / Expired / Suspended / Revoked badge |
| Actions | ❌ | View · Renew · Suspend · Revoke · Download PDF |

**Bulk actions:** Bulk renew selected · Bulk issue for new AY · Export.
**Pagination:** Server-side · 25/page.

---

## 6. Drawers

> **Audit trail:** All write actions (issue, renew, suspend, revoke pass; bulk issue) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

### 6.1 Drawer: `issue-pass`
- **Trigger:** + Issue Pass
- **Width:** 540px
- **Fields:** Branch · Student (searchable — must be allocated to a route, Page 14) · Route (auto-filled from allocation) · Pickup Stop (auto-filled) · Drop Stop · Issue Date · Expiry Date · Photo (optional — for digital pass display) · Notes
- **Validation:** Student must have active transport allocation before pass can be issued · Expiry date must be future
- **On save:** Pass generated; QR code created; parent notified via WhatsApp

### 6.2 Drawer: `pass-detail`
- **Width:** 540px
- **Content:** Pass card preview (student photo, name, route, stop, pass no, QR code) · Issue date · Expiry · Status · Renewal history · Suspension history
- **Actions:** [Download PDF] · [Renew] · [Suspend] · [Revoke]

### 6.3 Modal: `renew-pass`
- **Width:** 480px
- **Fields:** Pass No (pre-filled) · New Expiry Date · Academic Year · Confirm fee cleared (checkbox)
- **On confirm:** Pass renewed; new QR generated; parent notified

### 6.4 Modal: `suspend-pass`
- **Width:** 480px
- **Fields:** Reason (Fee Default / Misconduct / Other) · Effective Date · Expected Reinstatement Date · Notify Parent (checkbox) · Note to Bus Driver

### 6.5 Modal: `revoke-pass`
- **Width:** 480px
- **Fields:** Reason · Effective Date
- **Warning:** "Revoked passes cannot be reinstated. Issue a new pass if needed."

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Pass issued | "Bus pass [No] issued for [Name]. QR generated. Parent notified." | Success | 4s |
| Issue failed | "Failed to issue pass. Ensure [Student] has an active transport allocation." | Error | 5s |
| Pass renewed | "Bus pass renewed for [Name]. New expiry: [date]." | Success | 4s |
| Renew failed | "Failed to renew pass. Check fee clearance and expiry date." | Error | 5s |
| Pass suspended | "Bus pass suspended for [Name]. Driver notified." | Warning | 5s |
| Suspend failed | "Failed to suspend bus pass. Please retry." | Error | 5s |
| Pass revoked | "Bus pass revoked for [Name]." | Warning | 5s |
| Revoke failed | "Failed to revoke bus pass. Please retry." | Error | 5s |
| Bulk issue complete | "[N] bus passes issued. Download summary." | Info | 4s |
| Bulk issue failed | "Bulk issue failed. [N] students had errors — check allocation status." | Error | 6s |
| Export failed | "Export failed. Please try again." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No passes | "No Bus Passes Issued" | "Issue passes for all students enrolled in transport." | [+ Issue Pass] |
| No expiring passes | "No Passes Expiring Soon" | "All active passes have validity > 30 days." | — |
| No filter results | "No Passes Match Filters" | "Adjust branch, status, expiry, or class filters." | [Clear Filters] |
| No search results | "No Passes Found for '[term]'" | "Check the student name, pass number, or roll number." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + pass table |
| Filter/search | Table body skeleton |
| Issue pass drawer | 540px skeleton |
| PDF download | Spinner on button for 2–3 seconds |

---

## 10. Role-Based UI Visibility

| Element | Fee Manager G3 | Route Planning Mgr G3 | Branch Transport |
|---|---|---|---|
| Issue Pass | ✅ | ❌ | ✅ (own branch) |
| Renew Pass | ✅ | ❌ | ✅ (own branch) |
| Suspend Pass | ✅ | ❌ | ❌ |
| Revoke Pass | ✅ | ❌ | ❌ |
| Bulk Issue | ✅ | ❌ | ✅ (own branch) |
| Download PDF | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/bus-passes/` | JWT (G3+) | Pass list |
| POST | `/api/v1/group/{group_id}/transport/bus-passes/` | JWT (G3+) | Issue pass |
| GET | `/api/v1/group/{group_id}/transport/bus-passes/{id}/` | JWT (G3+) | Pass detail |
| POST | `/api/v1/group/{group_id}/transport/bus-passes/{id}/renew/` | JWT (G3+) | Renew pass |
| POST | `/api/v1/group/{group_id}/transport/bus-passes/{id}/suspend/` | JWT (G3+) | Suspend |
| POST | `/api/v1/group/{group_id}/transport/bus-passes/{id}/revoke/` | JWT (G3+) | Revoke |
| POST | `/api/v1/group/{group_id}/transport/bus-passes/bulk-issue/` | JWT (G3+) | Bulk issue passes for new AY |
| GET | `/api/v1/group/{group_id}/transport/bus-passes/{id}/pdf/` | JWT (G3+) | Download PDF pass |
| GET | `/api/v1/group/{group_id}/transport/bus-passes/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/bus-passes/export/` | JWT (G3+) | Export pass register |

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../bus-passes/?q={val}` | `#pass-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../bus-passes/?{filters}` | `#pass-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../bus-passes/?sort={col}&dir={asc/desc}` | `#pass-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../bus-passes/?page={n}` | `#pass-table-section` | `innerHTML` |
| Open pass detail drawer | `click` on Pass No | GET `.../bus-passes/{id}/` | `#drawer-body` | `innerHTML` |
| Issue pass submit | `click` | POST `.../bus-passes/` | `#pass-table-section` | `innerHTML` |
| Renew pass confirm | `click` | POST `.../bus-passes/{id}/renew/` | `#pass-row-{id}` | `outerHTML` |
| Suspend pass confirm | `click` | POST `.../bus-passes/{id}/suspend/` | `#pass-row-{id}` | `outerHTML` |
| Revoke pass confirm | `click` | POST `.../bus-passes/{id}/revoke/` | `#pass-row-{id}` | `outerHTML` |
| Bulk issue submit | `click` | POST `.../bus-passes/bulk-issue/` | `#pass-table-section` | `innerHTML` |
| Download PDF | `click` | GET `.../bus-passes/{id}/pdf/` | `#pdf-btn-{id}` | `outerHTML` |
| Export | `click` | GET `.../bus-passes/export/` | `#export-btn` | `outerHTML` |

> **Audit trail:** All write actions (issue, renew, suspend, revoke pass; bulk issue) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
