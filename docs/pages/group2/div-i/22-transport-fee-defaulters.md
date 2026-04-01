# 22 — Transport Fee Defaulters

> **URL:** `/group/transport/fees/defaulters/`
> **File:** `22-transport-fee-defaulters.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Transport Fee Manager (primary) · Transport Director

---

## 1. Purpose

Dedicated view of all students with outstanding transport fees across every branch, sorted by days overdue. The Fee Manager takes escalation actions — send reminders, suspend bus passes, notify parents, and escalate to branch — directly from this page.

This page exists separately from the collection page (Page 21) because defaulter management requires a different workflow — it's about chasing overdue payments, not recording new ones.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Fee Manager | G3 | Full — all actions | Primary owner |
| Group Transport Director | G3 | View + approve bus pass suspension | Oversight |
| Branch Accountant | Branch role | View own branch defaulters | Scoped |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Transport Fee Defaulters
```

### 3.2 Page Header
- **Title:** `Transport Fee Defaulters`
- **Subtitle:** `[N] Defaulters · Total Outstanding: ₹[N] · AY [current]`
- **Right controls:** `Send Bulk Reminder` · `Export Defaulter List` · `Advanced Filters`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| 0-payment defaulters > 60 days | "[N] students have made no payment in > 60 days." | Red |
| Students with suspended pass still on route | "[N] students with suspended bus passes are still on route allocation." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Defaulters | All branches | Yellow > 0 · Red > 50 |
| Defaulters (30d+) | 30+ days outstanding | Red > 0 |
| Zero-Payment (60d+) | No payment in 60d | Red > 0 |
| Total Outstanding (₹) | Sum | Yellow always |
| Bus Passes Suspended | Count | Blue |
| Escalated to Branch | Count this month | Blue |

---

## 5. Main Table — Defaulter List

**Search:** Student name, roll number, branch, route. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Outstanding Days | Radio | All / 1–30d / 31–60d / 60d+ |
| Bus Pass Status | Radio | All / Active / Suspended |
| Payment History | Checkbox | Zero-payment (no payment in 60d) |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Student Name | ✅ | Link → student transport detail (Page 14) |
| Roll No | ✅ | |
| Class | ✅ | |
| Branch | ✅ | |
| Route | ✅ | |
| Outstanding (₹) | ✅ | |
| Days Outstanding | ✅ | Colour: Yellow 1–30 · Orange 31–60 · Red > 60 |
| Last Payment Date | ✅ | |
| Bus Pass Status | ✅ | Active / Suspended badge |
| Reminders Sent | ✅ | Count this term |
| Actions | ❌ | Send Reminder · Suspend Pass · Escalate · Record Payment |

**Default sort:** Days outstanding descending.
**Pagination:** Server-side · 25/page.
**Bulk actions:** Send bulk reminder · Bulk export.

---

## 6. Drawers & Modals

### 6.1 Modal: `send-reminder`
- **Width:** 480px
- **Trigger:** Actions → Send Reminder · or Send Bulk Reminder button
- **Content:** Student name, outstanding amount, days overdue
- **Fields:** Channel (WhatsApp / SMS / Both) · Message template · Custom note
- **On confirm:** WhatsApp/SMS sent to parent; reminder count incremented; audit log

### 6.2 Modal: `suspend-bus-pass`
- **Width:** 480px
- **Trigger:** Actions → Suspend Pass
- **Fields:** Effective Date · Reason (Non-payment) · Notify Parent (checkbox) · Notes
- **Warning:** "Student will be denied boarding from [date] until fee is cleared."

### 6.3 Modal: `escalate-to-branch`
- **Width:** 480px
- **Trigger:** Actions → Escalate
- **Fields:** Branch Principal / Accountant (auto-filled) · Escalation Note · Deadline for resolution
- **On confirm:** Task created in branch portal; email sent; audit log

### 6.4 Drawer: `record-payment` (inline quick-record)
- **Width:** 480px
- Same as Page 21 record payment — pre-filled with student details
- Removes student from defaulter list once full outstanding cleared

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Reminder sent | "Reminder sent to [Name]'s parent." | Info | 4s |
| Reminder failed | "Failed to send reminder. Check WhatsApp/SMS configuration." | Error | 5s |
| Bulk reminder sent | "Reminders sent to [N] defaulters." | Info | 4s |
| Bulk reminder failed | "Failed to send bulk reminders. Please retry." | Error | 5s |
| Bus pass suspended | "Bus pass suspended for [Name]. Effective [date]." | Warning | 6s |
| Suspension failed | "Failed to suspend bus pass. Please retry." | Error | 5s |
| Escalated | "Case escalated to [Branch]. Accountant notified." | Info | 4s |
| Escalation failed | "Failed to escalate case. Please retry." | Error | 5s |
| Payment recorded | "Payment recorded. [Name] removed from defaulter list." | Success | 4s |
| Payment record failed | "Failed to record payment. Please retry." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No defaulters | "No Transport Fee Defaulters" | "All transport fees are current." | — |
| No filter results | "No Defaulters Match Filters" | "Adjust branch, outstanding days, or bus pass status filters." | [Clear Filters] |
| No search results | "No Defaulters Found for '[term]'" | "Check the student name, roll number, or branch." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + defaulter table |
| Filter/search | Table body skeleton |
| Modal confirm | Spinner on action button |

---

## 10. Role-Based UI Visibility

| Element | Fee Manager G3 | Transport Director G3 |
|---|---|---|
| Send Reminder | ✅ | ❌ |
| Suspend Bus Pass | ✅ | ✅ |
| Escalate to Branch | ✅ | ✅ |
| Record Payment | ✅ | ❌ |
| Export | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/fees/defaulters/` | JWT (G3+) | Defaulter list |
| POST | `/api/v1/group/{group_id}/transport/fees/defaulters/bulk-reminder/` | JWT (G3+) | Bulk reminder |
| POST | `/api/v1/group/{group_id}/transport/fees/students/{id}/suspend-pass/` | JWT (G3+) | Suspend bus pass |
| POST | `/api/v1/group/{group_id}/transport/fees/defaulters/{id}/escalate/` | JWT (G3+) | Escalate to branch |
| GET | `/api/v1/group/{group_id}/transport/fees/defaulters/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/fees/defaulters/export/` | JWT (G3+) | Export |

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../defaulters/?q={val}` | `#defaulter-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../defaulters/?{filters}` | `#defaulter-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../defaulters/?sort={col}&dir={asc/desc}` | `#defaulter-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../defaulters/?page={n}` | `#defaulter-table-section` | `innerHTML` |
| Send reminder confirm | `click` | POST `.../defaulters/bulk-reminder/` | `#defaulter-table-section` | `innerHTML` |
| Suspend pass confirm | `click` | POST `.../students/{id}/suspend-pass/` | `#defaulter-row-{id}` | `outerHTML` |
| Escalate confirm | `click` | POST `.../defaulters/{id}/escalate/` | `#defaulter-row-{id}` | `outerHTML` |
| Export | `click` | GET `.../defaulters/export/` | `#export-btn` | `outerHTML` |

> **Audit trail:** All write actions (send reminder, suspend pass, escalate, record payment) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
