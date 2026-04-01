# 16 — Driver Licence Tracker

> **URL:** `/group/transport/staff/licences/`
> **File:** `16-driver-license-tracker.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Fleet Manager (primary) · Transport Safety Officer · Transport Director

---

## 1. Purpose

Dedicated tracker for all driver driving licences across the group. Operating a school bus with an expired or invalid licence is a criminal offence. This page ensures zero-tolerance compliance — every driver's DL type, validity, endorsements, and renewal status is tracked and automatically flagged before expiry.

Licence types relevant for school transport:
- **HMV (Heavy Motor Vehicle)** — Required for full-size buses > 7.5T
- **PSV (Public Service Vehicle)** — Required for contract carriage / school buses
- **LMV (Light Motor Vehicle)** — Mini vans / small vehicles

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Fleet Manager | G3 | Full — update renewal status, upload scans | Primary owner |
| Group Transport Safety Officer | G3 | Read — compliance verification | View only |
| Group Transport Director | G3 | View — oversight | Read only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Driver Licence Tracker
```

### 3.2 Page Header
- **Title:** `Driver Licence Tracker`
- **Subtitle:** `[N] Active Drivers · [N] Compliance Issues · Compliance Score: [N]%`
- **Right controls:** `Advanced Filters` · `Bulk Reminder` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Licence expired | "[N] drivers have expired licences. Must be taken off duty immediately." | Red |
| Driver on duty with expired licence | "[N] drivers with expired licences are currently rostered on active routes." | Red |
| Licence expiring ≤ 7 days | "[N] licences expire within 7 days." | Amber |
| Licence expiring ≤ 30 days | "[N] licences expire within 30 days." | Amber |
| PSV endorsement missing | "[N] drivers operating PSV routes have no PSV endorsement on their DL." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Active Drivers | Count | Blue |
| Fully Licence-Compliant | Valid DL + PSV endorsement | Green = 100% · Red < 100% |
| Licence Expired | Count | Red > 0 |
| Expiring ≤ 30 days | Count | Yellow > 0 |
| Missing PSV Endorsement | Count | Red > 0 |
| Licences Renewed This Month | Count | Blue |

---

## 5. Main Table — Licence Compliance Register

**Search:** Driver name, employee ID, licence number. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Licence Type | Checkbox | LMV / HMV / PSV |
| Status | Radio | All / Valid / Expiring Soon (≤30d) / Expired |
| PSV Endorsement | Radio | All / Has PSV / Missing PSV |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Driver Name | ✅ | Link → staff detail (Page 15) |
| Branch | ✅ | |
| Route | ✅ | Current assignment |
| Licence No | ✅ | |
| Licence Type | ✅ | LMV / HMV / PSV / HMV+PSV |
| Issue Date | ✅ | |
| Expiry Date | ✅ | Colour coded |
| Days to Expiry | ✅ | Red ≤ 7 · Yellow ≤ 30 · Green > 30 |
| PSV Endorsement | ✅ | ✅ Yes · ❌ No |
| DL Scan | ✅ | ✅ Uploaded · ❌ Missing |
| Renewal Status | ✅ | Current / Renewal In Progress / Expired |
| Actions | ❌ | Update · Upload Scan · Send Reminder |

**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `update-licence`
- **Trigger:** Actions → Update
- **Width:** 520px
- **Fields:** Driver (pre-filled from row) · Licence Number · Licence Type (multi-select) · Issue Date · Expiry Date · PSV Endorsement (checkbox) · Issuing Authority (RTO name) · Renewal Status · Upload Scan (PDF/JPG)
- **Validation:** Expiry date must be future for "Current" status

---

## 7. Automated Reminder System

| Trigger | Recipient | Channel |
|---|---|---|
| 30 days before expiry | Fleet Manager | In-app + email |
| 15 days before expiry | Fleet Manager + Transport Director | In-app + email |
| 7 days before expiry | Fleet Manager + Director + Branch Transport | In-app + email + WhatsApp |
| Day of expiry | All + Group COO (if driver on duty) | Critical in-app |
| Day after expiry | System flags driver as non-compliant; removes from active roster | Auto-status update |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Licence updated | "[Name]'s licence updated. New expiry: [date]." | Success | 4s |
| Licence update failed | "Failed to update licence. Check expiry date and licence number." | Error | 5s |
| Scan uploaded | "DL scan uploaded for [Name]." | Info | 4s |
| Scan upload failed | "Failed to upload scan. Check file format (PDF/image)." | Error | 5s |
| Reminder sent | "Licence renewal reminder sent to [N] drivers." | Info | 4s |
| Reminder failed | "Failed to send reminders. Please retry." | Error | 5s |
| Driver flagged non-compliant | "[Name] flagged non-compliant. Route assignment suspended." | Warning | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No compliance issues | "All Drivers Licence-Compliant" | "All drivers have valid licences and PSV endorsements." | — |
| No drivers | "No Drivers Registered" | "Sync driver data from HRMS." | [→ Driver Registry] |
| No filter results | "No Drivers Match Filters" | "Adjust branch, licence type, or status filters." | [Clear Filters] |
| No search results | "No Drivers Found for '[term]'" | "Check the driver name, employee ID, or licence number." | [Clear Search] |

---

## 10. Role-Based UI Visibility

| Element | Fleet Manager G3 | Safety Officer G3 | Transport Director G3 |
|---|---|---|---|
| Update Licence | ✅ | ❌ | ❌ |
| Upload Scan | ✅ | ❌ | ❌ |
| Send Bulk Reminder | ✅ | ❌ | ✅ |
| Remove Driver from Duty | ✅ | ✅ (flag) | ✅ (execute) |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/staff/licences/` | JWT (G3+) | Licence compliance list |
| PATCH | `/api/v1/group/{group_id}/transport/staff/{id}/licence/` | JWT (G3+) | Update licence details |
| POST | `/api/v1/group/{group_id}/transport/staff/licences/bulk-reminder/` | JWT (G3+) | Send reminders |
| GET | `/api/v1/group/{group_id}/transport/staff/licences/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/staff/licences/export/` | JWT (G3+) | Export |

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../licences/?q={val}` | `#licence-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../licences/?{filters}` | `#licence-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../licences/?sort={col}&dir={asc/desc}` | `#licence-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../licences/?page={n}` | `#licence-table-section` | `innerHTML` |
| Open update drawer | `click` on Update | GET `.../staff/{id}/licence/` | `#drawer-body` | `innerHTML` |
| Update submit | `click` | PATCH `.../staff/{id}/licence/` | `#licence-row-{id}` | `outerHTML` |
| Send bulk reminder | `click` | POST `.../licences/bulk-reminder/` | `#reminder-btn` | `outerHTML` |
| Export | `click` | GET `.../licences/export/` | `#export-btn` | `outerHTML` |

> **Audit trail:** All write actions (licence update, scan upload, bulk reminders) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
