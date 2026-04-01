# 09 — Fitness Certificate, Permit & Insurance Manager

> **URL:** `/group/transport/compliance/documents/`
> **File:** `09-fitness-permit-insurance-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Fleet Manager (primary) · Transport Director · Transport Safety Officer

---

## 1. Purpose

Centralised management of all statutory vehicle documents across the entire fleet — Motor Vehicle Fitness Certificates (MV Act), Route Permits (State Transport Authority), Insurance Policies (Commercial Vehicle / Passenger), and RC Book renewals.

A vehicle operating without a valid fitness certificate or insurance is a criminal liability. The Fleet Manager tracks all expiry dates, uploads renewed documents, and receives automated reminders 30/15/7 days before expiry. The Transport Director and Safety Officer have visibility into the compliance scoreboard.

Legal obligations covered:
- **Fitness Certificate** — Issued by RTO, renewed annually/biannually. Required under MV Act for all commercial vehicles.
- **Route Permit** — Issued by State Transport Authority. Required for school/contract carriage routes.
- **Insurance** — Comprehensive + third-party passenger liability. Renewed annually.
- **RC Book** — Permanent (15yr validity, then renewal). Tracks on this page if approaching expiry.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Fleet Manager | G3 | Full — upload, mark renewed, set reminders | Primary owner |
| Group Transport Director | G3 | View + approve document upload | Oversight role |
| Group Transport Safety Officer | G3 | Read — compliance check during safety audit | View only |
| Group CFO | G1 | Read — insurance cost view | View only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Fitness / Permit / Insurance Manager
```

### 3.2 Page Header
- **Title:** `Vehicle Compliance Documents`
- **Subtitle:** `[N] Vehicles · [N] Compliance Issues · Overall Score: [N]%`
- **Right controls:** `Upload Document` · `Bulk Reminder` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Any document expired | "[N] vehicles have expired documents — cannot legally operate." | Red |
| Expiring in 7 days | "[N] documents expire in 7 days. Immediate renewal required." | Red |
| Expiring in 15 days | "[N] documents expire in 15 days." | Amber |
| Insurance renewal overdue | "[N] insurance policies expired. Third-party liability risk." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Overall Compliance Score | % vehicles with all 3 docs valid | Green ≥ 98% · Yellow 90–98% · Red < 90% |
| Fitness Cert — Non-Compliant | Expired or missing | Red > 0 |
| Permit — Non-Compliant | Expired or missing | Red > 0 |
| Insurance — Non-Compliant | Expired or missing | Red > 0 |
| Expiring ≤ 30 days (any doc) | Total count | Yellow > 0 |
| Documents Uploaded This Month | Count of renewals logged | Blue |

---

## 5. Main Table — Document Compliance Register

**Tabs:** All Documents · Fitness Certificates · Route Permits · Insurance · RC Book

> Default tab: All Documents (combined view per vehicle).

**Search:** Bus number, RC number, branch. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Document Type | Checkbox | Fitness / Permit / Insurance / RC |
| Status | Radio | All / Valid / Expiring Soon (≤30d) / Expired |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Bus No | ✅ | Link → vehicle detail (Page 07) |
| Branch | ✅ | |
| Fitness Cert | ✅ | Expiry date · ✅ / ⚠ / 🔴 badge |
| Route Permit | ✅ | Expiry date · badge |
| Insurance | ✅ | Expiry date · badge |
| RC Expiry | ✅ | N/A for permanent RC |
| Overall Status | ✅ | ✅ All Valid / ⚠ Issues |
| Last Updated | ✅ | Last document upload date |
| Actions | ❌ | Upload Doc · View Docs · Send Reminder |

**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `upload-document`
- **Trigger:** Actions → Upload Doc · Or header Upload Document button
- **Width:** 540px
- **Fields:** Bus No (searchable) · Document Type · Issue Date · Expiry Date · Issuing Authority · Document Number · Upload File (PDF/JPG, max 5MB)
- **Validation:** Expiry date must be future · File type PDF or image only

> **Audit trail:** All write actions (upload document, mark renewed, send reminders) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

### 6.2 Drawer: `vehicle-document-view`
- **Trigger:** Actions → View Docs
- **Width:** 680px
- **Tabs:** Fitness Cert · Permit · Insurance · RC
- Each tab shows: Current document (embedded PDF viewer) · Issue date · Expiry date · Issuing authority · Document number · Renewal history (last 5)
- **[Renew →]** button on each tab opens upload drawer pre-filled with document type and bus number

---

## 7. Automated Reminder System

| Trigger | Recipient | Channel |
|---|---|---|
| 30 days before expiry | Fleet Manager | In-app notification + email |
| 15 days before expiry | Fleet Manager + Transport Director | In-app + email |
| 7 days before expiry | Fleet Manager + Transport Director + Branch Transport | In-app + email + WhatsApp |
| Day of expiry | All above + Group COO | In-app + email + WhatsApp (critical) |
| Day after expiry | System flags vehicle as non-compliant | Auto-status update |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Document uploaded | "Fitness certificate uploaded for [Bus No]. Expiry: [date]." | Success | 4s |
| Upload failed | "Failed to upload document. Check file format (PDF/image) and size (max 5MB)." | Error | 5s |
| Document renewed | "Route permit renewed for [Bus No]. New expiry: [date]." | Success | 4s |
| Renewal failed | "Failed to update renewal record. Please retry." | Error | 5s |
| Bulk reminder sent | "Renewal reminders sent for [N] vehicles." | Info | 4s |
| Reminder failed | "Failed to send reminders. Check notification configuration." | Error | 5s |
| Document expired | "[Bus No] insurance expired. Vehicle marked non-compliant." | Warning | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No compliance issues | "Full Document Compliance" | "All vehicles have valid fitness, permit, and insurance documents." | — |
| No vehicles | "No Vehicles Registered" | "Register vehicles in the Vehicle Register first." | [→ Vehicle Register] |
| No filter results | "No Vehicles Match Filters" | "Adjust branch, document type, or status filters." | [Clear Filters] |
| No search results | "No Vehicles Found for '[term]'" | "Check the bus number, RC number, or branch." | [Clear Search] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + document table |
| Filter/search | Table body skeleton |
| Document view drawer | PDF viewer loading spinner per tab |

---

## 11. Role-Based UI Visibility

| Element | Fleet Manager G3 | Transport Director G3 | Safety Officer G3 | CFO G1 |
|---|---|---|---|---|
| Upload Document | ✅ | ✅ | ❌ | ❌ |
| Mark Renewed | ✅ | ❌ | ❌ | ❌ |
| Send Reminder | ✅ | ✅ | ❌ | ❌ |
| View Documents | ✅ | ✅ | ✅ | ✅ (insurance only) |
| Export | ✅ | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/compliance/documents/` | JWT (G3+) | Document compliance list |
| GET | `/api/v1/group/{group_id}/transport/compliance/documents/kpis/` | JWT (G3+) | KPI cards |
| POST | `/api/v1/group/{group_id}/transport/compliance/documents/upload/` | JWT (G3+) | Upload document |
| GET | `/api/v1/group/{group_id}/transport/vehicles/{id}/documents/` | JWT (G3+) | Vehicle doc detail drawer |
| POST | `/api/v1/group/{group_id}/transport/compliance/reminders/bulk/` | JWT (G3+) | Send bulk reminders |
| GET | `/api/v1/group/{group_id}/transport/compliance/documents/export/` | JWT (G3+) | Export compliance list |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | GET `.../documents/?type={tab}` | `#doc-table-section` | `innerHTML` |
| Search | `input delay:300ms` | GET `.../documents/?q={val}` | `#doc-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../documents/?{filters}` | `#doc-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../documents/?sort={col}&dir={asc/desc}` | `#doc-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../documents/?page={n}` | `#doc-table-section` | `innerHTML` |
| Upload submit | `click` | POST `.../documents/upload/` | `#doc-table-section` | `innerHTML` |
| Open doc view drawer | `click` | GET `.../vehicles/{id}/documents/` | `#drawer-body` | `innerHTML` |
| Export | `click` | GET `.../documents/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
