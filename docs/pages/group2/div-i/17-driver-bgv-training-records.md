# 17 — Driver BGV & Training Records

> **URL:** `/group/transport/staff/bgv-training/`
> **File:** `17-driver-bgv-training-records.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Fleet Manager (primary) · Transport Safety Officer · Transport Director

---

## 1. Purpose

Manages Background Verification (BGV) status and training records for all drivers and conductors. BGV is mandatory for all staff who interact with minors (POCSO compliance). Training records cover road safety, defensive driving, first aid, and emergency evacuation.

BGV covers: Criminal record check, previous employment verification, address verification, and character references. Any driver with a failed BGV or incomplete BGV must not operate a school vehicle.

Training is annual for road safety, biannual for defensive driving, and one-time for first aid certification (with renewal every 3 years).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Fleet Manager | G3 | Full — update BGV status, log training | Primary owner |
| Group Transport Safety Officer | G3 | Read — safety compliance verification | View only |
| Group Transport Director | G3 | View + approve suspension on BGV fail | Oversight |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Driver BGV & Training Records
```

### 3.2 Page Header
- **Title:** `Driver BGV & Training Records`
- **Subtitle:** `[N] Staff · BGV Cleared: [N] · Training Current: [N]%`
- **Right controls:** `Log Training` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| BGV failed for active driver | "[N] active drivers have FAILED BGV. Must be removed from duty immediately." | Red |
| BGV pending > 60 days | "[N] drivers have had BGV pending for > 60 days." | Amber |
| Road safety training overdue | "[N] drivers have overdue annual road safety training." | Amber |
| First aid certification expired | "[N] drivers have expired first aid certification." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| BGV Cleared | % of staff | Green = 100% · Red < 100% |
| BGV Pending | Count | Yellow > 0 |
| BGV Failed | Count | Red > 0 |
| Road Safety Training Current | % | Green = 100% · Red < 100% |
| First Aid Certified | % | Blue |
| Defensive Driving Current | % | Blue |

---

## 5. Sections

### 5.1 BGV Status Table

> BGV status for all drivers/conductors across branches.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| BGV Status | Radio | All / Cleared / Pending / Failed / Not Initiated |

**Columns:** Name · Branch · Role · Joining Date · BGV Initiated Date · BGV Vendor · Status · Clearance Date · Notes · Actions (Update Status · View Report)

**Pagination:** Server-side · 25/page.

---

### 5.2 Training Records Table

> Training completion status for all staff.

**Tabs:** Road Safety · Defensive Driving · First Aid · Emergency Evacuation

**Columns:** Name · Branch · Training Type · Last Completed · Next Due · Status (Current / Due Soon / Overdue) · Trainer/Vendor · Certificate No · [View Certificate] · [Log Training]

**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `update-bgv`
- **Width:** 520px
- **Fields:** Staff Name (pre-filled) · BGV Vendor · Initiation Date · Status (Pending / Cleared / Failed / Withdrawn) · Clearance Date (if Cleared) · Failure Reason (if Failed) · Upload BGV Report (PDF)
- **Warning on Failed:** "Failed BGV will result in route assignment removal and suspension notification."

### 6.2 Drawer: `log-training`
- **Trigger:** Log Training button
- **Width:** 520px
- **Fields:** Staff (multi-select or individual) · Training Type · Date Completed · Trainer / Training Organisation · Duration (hours) · Location (online / in-person) · Certificate Number · Upload Certificate (PDF/JPG) · Expiry Date (if applicable)
- **Validation:** Completion date cannot be future

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| BGV updated — cleared | "[Name]'s BGV status updated: Cleared." | Success | 4s |
| BGV updated — failed | "[Name]'s BGV FAILED. Route assignment removed. Director notified." | Warning | 6s |
| BGV update failed | "Failed to update BGV status. Please retry." | Error | 5s |
| Training logged | "Training record logged for [Name] — [Training Type]." | Success | 4s |
| Training log failed | "Failed to log training record. Check completion date and certificate details." | Error | 5s |
| Bulk training reminder | "Training reminders sent to [N] staff." | Info | 4s |
| Reminder failed | "Failed to send training reminders. Please retry." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| All BGV cleared | "All Staff BGV Cleared" | "No pending or failed BGV records." | — |
| All training current | "All Training Current" | "All staff have completed required training within validity period." | — |
| No filter results (BGV) | "No Staff Match Filters" | "Adjust branch or BGV status filters." | [Clear Filters] |
| No search results | "No Staff Found for '[term]'" | "Check the name or employee ID." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + BGV table + training table |
| Tab switch in training section | Table body skeleton |
| BGV update drawer | 520px skeleton |

---

## 10. Role-Based UI Visibility

| Element | Fleet Manager G3 | Safety Officer G3 | Transport Director G3 |
|---|---|---|---|
| Update BGV Status | ✅ | ❌ | ✅ (approve fail action) |
| Log Training | ✅ | ❌ | ❌ |
| Send Training Reminder | ✅ | ❌ | ✅ |
| Remove from Duty on BGV Fail | ✅ (propose) | ❌ | ✅ (execute) |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/staff/bgv/` | JWT (G3+) | BGV status list |
| PATCH | `/api/v1/group/{group_id}/transport/staff/{id}/bgv/` | JWT (G3+) | Update BGV status |
| GET | `/api/v1/group/{group_id}/transport/staff/training/` | JWT (G3+) | Training records list |
| POST | `/api/v1/group/{group_id}/transport/staff/training/` | JWT (G3+) | Log training |
| POST | `/api/v1/group/{group_id}/transport/staff/training/bulk-reminder/` | JWT (G3+) | Send reminders |
| GET | `/api/v1/group/{group_id}/transport/staff/bgv-training/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/staff/bgv/export/` | JWT (G3+) | Export BGV records |
| GET | `/api/v1/group/{group_id}/transport/staff/training/export/` | JWT (G3+) | Export training records |

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| BGV table filter | `click` | GET `.../bgv/?{filters}` | `#bgv-table-section` | `innerHTML` |
| BGV table sort | `click` on header | GET `.../bgv/?sort={col}&dir={asc/desc}` | `#bgv-table-section` | `innerHTML` |
| BGV table pagination | `click` | GET `.../bgv/?page={n}` | `#bgv-table-section` | `innerHTML` |
| Training tab switch | `click` | GET `.../training/?type={tab}` | `#training-table-section` | `innerHTML` |
| Training table sort | `click` on header | GET `.../training/?sort={col}&dir={asc/desc}` | `#training-table-section` | `innerHTML` |
| Training table pagination | `click` | GET `.../training/?page={n}` | `#training-table-section` | `innerHTML` |
| BGV search | `input delay:300ms` | GET `.../bgv/?q={val}` | `#bgv-table-body` | `innerHTML` |
| BGV update submit | `click` | PATCH `.../staff/{id}/bgv/` | `#bgv-row-{id}` | `outerHTML` |
| Log training submit | `click` | POST `.../training/` | `#training-table-section` | `innerHTML` |
| Send bulk training reminder | `click` | POST `.../training/bulk-reminder/` | `#reminder-btn` | `outerHTML` |
| Export | `click` | GET `.../bgv/export/` | `#export-btn` | `outerHTML` |

> **Audit trail:** All write actions (BGV update, training log) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
