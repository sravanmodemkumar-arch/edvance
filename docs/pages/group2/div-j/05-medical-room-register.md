# 05 — Medical Room Register

> **URL:** `/group/health/medical-rooms/`
> **File:** `05-medical-room-register.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Medical Coordinator (primary) · School Medical Officer · Emergency Response Officer (view)

---

## 1. Purpose

Master register of all medical rooms and sick bays across every branch in the group. Each record represents a physical medical facility at a branch — its location, type, equipment inventory, assigned nursing staff, operational status, inspection history, and incident linkage.

This is the infrastructure baseline for the entire health programme. Every branch must maintain at least one operational medical room as a regulatory and accreditation requirement. The register enables the Medical Coordinator to verify that every branch is equipped and staffed, track equipment compliance (particularly life-critical items like AED and oxygen), schedule and log periodic inspections, and identify gaps before they become regulatory violations or patient safety incidents.

Scale: 1–3 medical rooms per branch × 20–50 branches = 20–150 room records. Each room holds 5–50 equipment items tracked individually. Inspections are mandated every 90 days (quarterly).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Medical Coordinator | G3 | Full — create, edit, inspect, decommission | Primary owner of this register |
| Group School Medical Officer | G3 | Edit + inspect | Cannot create new rooms or decommission |
| Group Emergency Response Officer | G3 | Read only | For emergency supply verification |
| Branch Principal | Branch G3 | Read — own branch only | Cannot edit; aggregate view |
| All other roles | — | — | No access |

> **Access enforcement:** Django view decorator `@require_role('medical_coordinator', 'school_medical_officer', 'emergency_response_officer')` with permission-level checks per action.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Medical Room Register
```

### 3.2 Page Header
- **Title:** `Group Medical Room Register`
- **Subtitle:** `[N] Total Rooms · [N] Operational · [N] Non-Operational · [N] Branches Without Room`
- **Right controls:** `+ Add Medical Room` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with no medical room | "[N] branches have no registered medical room. Regulatory non-compliance." | Red |
| Critical equipment missing (AED, oxygen, stretcher) | "Critical equipment missing at [Branch] — [Item] not present in medical room." | Red |
| Inspection overdue > 90 days | "[N] medical rooms have inspections overdue by more than 90 days." | Red |
| Nurse not assigned | "[N] medical rooms have no assigned nurse. Rooms cannot be considered operational." | Amber |
| Next inspection due within 7 days | "[Room] at [Branch] inspection is due in [N] days." | Amber |

---

## 4. KPI Summary Bar (5 cards)

| Card | Metric | Colour Rule |
|---|---|---|
| Total Medical Rooms | All registered rooms across all branches | Blue always |
| Fully Operational | Rooms with Operational status, nurse assigned, equipment compliant | Green = 100% of total · Yellow < 95% · Red < 90% |
| Equipment Non-Compliant | Rooms with any missing or failed critical equipment item | Green = 0 · Yellow 1–3 · Red > 3 |
| Branches Without Medical Room | Branches with zero registered rooms | Green = 0 · Red > 0 (any gap is critical) |
| Inspections Overdue | Rooms whose last inspection date + 90 days is before today | Green = 0 · Yellow 1–5 · Red > 5 |

---

## 5. Main Table — Medical Room Register

**Search:** Branch name, room name/location. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Status | Checkbox | Operational / Under Renovation / Non-Functional / Decommissioned |
| Equipment Compliance | Radio | All / Compliant / Issues Found |
| Nurse Assigned | Radio | All / Assigned / Not Assigned |
| Inspection | Radio | All / Up to Date / Overdue ≤ 30d / Overdue > 30d / Overdue > 90d |
| Room Type | Checkbox | Sick Bay / Medical Room / First Aid Post / Counselling Room |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | |
| Room Name / Location | ✅ | Link → `medical-room-detail` drawer |
| Type | ✅ | Sick Bay / Medical Room / First Aid Post |
| Nurse Assigned | ✅ | Name or ❌ None |
| Status | ✅ | Colour badge: Operational (Green) / Under Renovation (Yellow) / Non-Functional (Red) / Decommissioned (Grey) |
| Equipment Compliance | ✅ | ✅ Compliant / ⚠ Issues / ❌ Critical Missing |
| Last Inspection | ✅ | Date; Red if > 90 days ago |
| Next Inspection Due | ✅ | Date; Red if past due, Yellow if within 14 days |
| Actions | ❌ | View · Edit · Inspect · Decommission (Medical Coordinator only) |

**Default sort:** Status (Non-Functional first), then Equipment Compliance (Critical Missing first).
**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `medical-room-detail` — View Room Full Profile
- **Trigger:** Room Name link or Actions → View
- **Width:** 680px
- **Tabs:** Profile · Equipment · Staff · Inspection History · Incidents

**Profile tab:**
| Field | Value |
|---|---|
| Room ID | System-generated unique ID |
| Branch | Branch name |
| Room Name | e.g., "Ground Floor Sick Bay" |
| Location / Floor | e.g., Block A, Ground Floor |
| Area (sq ft) | Numeric |
| Room Type | Sick Bay / Medical Room / First Aid Post / Counselling Room |
| Operational Since | Date |
| Last Renovation | Date or — |
| Current Status | Operational / Under Renovation / Non-Functional |
| Notes | Any relevant notes about this room |

**Equipment tab:**

Critical equipment checklist — each item with current status:

| Equipment Item | Status | Last Checked | Notes |
|---|---|---|---|
| AED (Automated External Defibrillator) | ✅ / ⚠ / ❌ | Date | |
| Stretcher / Trolley | ✅ / ⚠ / ❌ | Date | |
| Oxygen Cylinder (with mask/regulator) | ✅ / ⚠ / ❌ | Date | |
| BP Apparatus (manual + digital) | ✅ / ⚠ / ❌ | Date | |
| Thermometers (oral + infrared) | ✅ / ⚠ / ❌ | Date | |
| Pulse Oximeter | ✅ / ⚠ / ❌ | Date | |
| First Aid Kit (stocked) | ✅ / ⚠ / ❌ | Date | |
| Medicine Cabinet (locked) | ✅ / ⚠ / ❌ | Date | |
| Examination Table / Bed | ✅ / ⚠ / ❌ | Date | |
| Washbasin with running water | ✅ / ⚠ / ❌ | Date | |
| Glucometer | ✅ / ⚠ / ❌ | Date | |
| Nebuliser | ✅ / ⚠ / ❌ | Date | |
| Cold Pack / Ice Pack supply | ✅ / ⚠ / ❌ | Date | |
| Bandages / Dressings supply | ✅ / ⚠ / ❌ | Date | |
| Antiseptic / Disinfectant | ✅ / ⚠ / ❌ | Date | |

Status legend: ✅ = Present & functional · ⚠ = Present but needs attention (low supplies / due check) · ❌ = Missing or non-functional

Overall equipment compliance score shown at top: [N]/15 items compliant.

**Staff tab:**
| Field | Notes |
|---|---|
| Primary Nurse | Name, qualification (RN/ANM/DGNM), timing, contact |
| Backup Nurse | Name, contact, availability |
| Doctor (visiting) | Name, days/times of visit, contact |
| Emergency Contact | On-call medical contact for after-hours |

**Inspection History tab:**
- Last 5 inspections in reverse chronological order
- Per inspection: date, inspector name, overall score (0–100), items flagged, issues noted, resolution status, next inspection date
- "Conduct Inspection" button → `inspection-record` modal

**Incidents tab:**
- All medical incidents that occurred at this room
- Columns: date, incident type, severity, patient type, outcome, status
- Linked to Emergency Response incident log

---

### 6.2 Drawer: `medical-room-create` — Add New Medical Room
- **Trigger:** `+ Add Medical Room` button (Medical Coordinator only)
- **Width:** 640px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Select | Required; from group branches list |
| Room Name | Text | Required; unique per branch |
| Location / Floor | Text | Required |
| Room Type | Select | Sick Bay / Medical Room / First Aid Post / Counselling Room |
| Area (sq ft) | Number | Optional |
| Operational Since | Date | Required; cannot be future date |
| Status | Select | Default: Operational |
| Nurse Assigned | Lookup | Type-ahead from medical staff registry |
| Equipment Present (checklist) | Checkboxes | All 15 items listed; check those present at setup |
| Notes | Textarea | Optional |

**Validation:** Branch + Room Name combination must be unique. At least 5 equipment items must be checked to allow Operational status.

---

### 6.3 Drawer: `medical-room-edit` — Edit Medical Room
- **Trigger:** Actions → Edit
- **Width:** 640px
- **Fields:** Same as create, pre-populated. Read-only: Branch, Room ID, Operational Since.
- **Status change to Non-Functional:** Requires a reason note (mandatory field appears).
- **Available to:** Medical Coordinator (all fields) · School Medical Officer (equipment, staff, status only)

---

### 6.4 Modal: `inspection-record` — Conduct Inspection
- **Trigger:** Actions → Inspect · "Conduct Inspection" in Inspection History tab
- **Width:** 480px

**Fields:**
| Field | Type | Notes |
|---|---|---|
| Inspector Name | Text | Default: current user; editable |
| Inspection Date | Date | Default: today |
| Overall Score | Number (0–100) | Auto-calculates from item statuses |
| Equipment Status (per item) | Select × 15 | ✅ OK / ⚠ Needs Attention / ❌ Missing/Broken |
| General Observations | Textarea | |
| Issues Found | Textarea | Auto-populated from ⚠ and ❌ items |
| Action Required | Textarea | |
| Next Inspection Date | Date | Default: today + 90 days |

**Validation:** All 15 equipment items must have a status selected. Score auto-calculated: 100 × (OK items / 15). Warning shown if score < 60.

---

### 6.5 Modal: `medical-room-decommission` — Decommission Medical Room
- **Trigger:** Actions → Decommission on table row; "Decommission Room" button in `medical-room-detail` Profile tab footer
- **Width:** 460px
- **Available to:** Medical Coordinator (G3) only
- **Guard:** Cannot decommission a room if it is the only registered room for its branch — system blocks with inline error: "This is the only medical room at [Branch]. Add a replacement room before decommissioning."

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Room Name | Read-only | Pre-populated |
| Branch | Read-only | Pre-populated |
| Confirm Room Name | Text | Must type exact room name to enable Submit button |
| Reason for Decommission | Select | Renovated / Merged with Another Room / Branch Closure / Permanent Damage / Regulatory Non-Compliance / Other |
| Additional Notes | Textarea | Required if Reason = Other |
| Effective Date | Date | Required; cannot be past date |
| Transfer Equipment To | Select | Another medical room at same branch (if available); or — None / Off-site Storage |
| Final Inspection Conducted | Checkbox | Confirms a closing inspection was done |
| Notify Group COO | Checkbox | Default ✅ — sends decommission notification to senior leadership |

**On confirm:** Room status set to `Decommissioned`; all future inspections cancelled; equipment transferred if destination selected; audit event logged; alert cleared or re-raised for branch coverage gap.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Room created | "Medical room '[Name]' added for [Branch]." | Success | 4s |
| Room updated | "Medical room '[Name]' updated." | Success | 4s |
| Inspection recorded | "Inspection recorded for '[Room]' at [Branch]. Score: [N]/100." | Success | 4s |
| Inspection score low | "Inspection recorded — score [N]/100. Action required for [N] items." | Warning | 6s |
| Status changed to Non-Functional | "Medical room '[Name]' marked Non-Functional. Medical Coordinator notified." | Warning | 5s |
| Room decommissioned | "Medical room '[Name]' at [Branch] has been decommissioned. Group COO notified." | Warning | 6s |
| Decommission blocked | "Cannot decommission: '[Name]' is the only medical room at [Branch]. Add a replacement first." | Error | 6s |
| Room export initiated | "Medical room register export is being prepared. You'll be notified when ready." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No rooms registered | "No Medical Rooms Registered" | "Add the first medical room to begin building the health infrastructure register." | [+ Add Medical Room] |
| No results for filters | "No Rooms Match Filters" | "Try adjusting the branch, status, or compliance filters." | [Clear Filters] |
| No equipment issues | "All Equipment Compliant" | "All registered medical rooms have compliant equipment status." | — |
| No overdue inspections | "All Inspections Up to Date" | "No medical rooms have overdue inspection schedules." | — |
| Inspection history empty | "No Inspections on Record" | "No inspections have been conducted for this room yet." | [Conduct Inspection] |
| No incidents at room | "No Incidents at This Room" | "No medical incidents have been recorded for this room." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 5 KPI cards + table skeleton (12 rows × 9 columns) + alerts |
| Filter/search | Table body skeleton (10 rows) |
| Room detail drawer open | 680px drawer skeleton; each tab loads lazily on click |
| Profile tab load | Field-level skeleton (label + value pairs) |
| Equipment tab load | Checklist skeleton (15 rows with shimmer) |
| Inspection History tab | Table skeleton (5 rows × 6 columns) |
| Inspection modal | 480px form skeleton |
| Create/Edit drawer | 640px form skeleton |

---

## 10. Role-Based UI Visibility

| Element | Medical Coordinator G3 | School Medical Officer G3 | Emergency Response Officer G3 |
|---|---|---|---|
| Create Medical Room | ✅ | ❌ | ❌ |
| Edit Medical Room (all fields) | ✅ | ❌ | ❌ |
| Edit Equipment / Staff / Status | ✅ | ✅ | ❌ |
| Conduct Inspection | ✅ | ✅ | ❌ |
| View All Rooms | ✅ | ✅ | ✅ |
| View Equipment Details | ✅ | ✅ | ✅ |
| Decommission Room | ✅ | ❌ | ❌ |
| Export Register | ✅ | ✅ | ❌ |
| View Incident History | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/medical-rooms/` | JWT (G3+) | Paginated, filtered room list |
| GET | `/api/v1/group/{group_id}/health/medical-rooms/{id}/` | JWT (G3+) | Full room profile (all tab data) |
| POST | `/api/v1/group/{group_id}/health/medical-rooms/` | JWT (Role 85) | Create new medical room |
| PATCH | `/api/v1/group/{group_id}/health/medical-rooms/{id}/` | JWT (Role 85, 86) | Update room details |
| GET | `/api/v1/group/{group_id}/health/medical-rooms/kpis/` | JWT (G3+) | KPI card values |
| POST | `/api/v1/group/{group_id}/health/medical-rooms/{id}/inspect/` | JWT (Role 85, 86) | Record new inspection |
| GET | `/api/v1/group/{group_id}/health/medical-rooms/{id}/inspections/` | JWT (G3+) | Inspection history |
| GET | `/api/v1/group/{group_id}/health/medical-rooms/{id}/incidents/` | JWT (G3+) | Incidents at this room |
| POST | `/api/v1/group/{group_id}/health/medical-rooms/{id}/decommission/` | JWT (Role 85) | Decommission a medical room |
| POST | `/api/v1/group/{group_id}/health/medical-rooms/export/` | JWT (Role 85, 86) | Initiate async CSV/XLSX export; returns `{job_id}` |
| GET | `/api/v1/group/{group_id}/health/medical-rooms/export/status/{job_id}/` | JWT (Role 85, 86) | Poll export job status (`pending` / `ready` / `failed`) |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../medical-rooms/?q={val}` | `#rooms-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../medical-rooms/?{filters}` | `#rooms-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../medical-rooms/?page={n}` | `#rooms-table-section` | `innerHTML` |
| Sort by column | `click` on header | GET `.../medical-rooms/?sort={col}&dir={asc/desc}` | `#rooms-table-section` | `innerHTML` |
| Open room detail drawer | `click` on Room Name | GET `.../medical-rooms/{id}/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch | `click` | GET `.../medical-rooms/{id}/?tab={name}` | `#drawer-tab-content` | `innerHTML` |
| Submit create room | `click` | POST `.../medical-rooms/` | `#rooms-table-section` | `innerHTML` |
| Submit edit room | `click` | PATCH `.../medical-rooms/{id}/` | `#room-row-{id}` | `outerHTML` |
| Submit inspection | `click` | POST `.../medical-rooms/{id}/inspect/` | `#inspection-history-list` | `innerHTML` |
| Submit decommission | `click` Confirm | POST `.../medical-rooms/{id}/decommission/` | `#room-row-{id}` | `outerHTML` |
| OOB KPI refresh on decommission | (triggered by decommission POST response) | — | `#kpi-bar` | `hx-swap-oob="true"` |
| Initiate register export | `click` Export | POST `.../medical-rooms/export/` | `#export-status` | `innerHTML` |
| Poll export status | `every 5s [!#export-done]` | GET `.../medical-rooms/export/status/{job_id}/` | `#export-status` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
