# 16 — CCTV Camera Inventory

> **URL:** `/group/welfare/security/cctv/`
> **File:** `16-cctv-camera-inventory.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group CCTV & Security Head (Role 93, G3)

---

## 1. Purpose

Complete inventory of all CCTV cameras installed across all branches. Every camera is registered with its location (area type: Gate / Corridor / Classroom / Hostel Block / Parking / Server Room / Admin Block / Playground / Canteen), technical specifications (resolution, type: Dome / Bullet / PTZ / Fisheye), installation date, last maintenance date, current status (Functional / Degraded / Non-Functional / Under Maintenance), and the DVR/NVR unit it connects to.

The CCTV & Security Head uses this page to: track coverage compliance (minimum cameras required per area type across all branches), identify non-functional cameras requiring urgent repair, schedule preventive maintenance before due dates, and report to Group COO on overall security infrastructure health.

Minimum coverage standards enforced by the system:
- **Gate:** Minimum 2 cameras per branch · 24/7 recording required.
- **Girls Hostel Block:** All entry and exit points covered · 24/7 recording required.
- **Corridors:** Minimum 1 camera per 30m length.
- **Parking:** Full coverage required (no blind spots).

Any branch below the minimum coverage standard for any area type is flagged immediately in the alert banner and KPI bar.

Scale: 10–100 cameras per branch · 500–5,000 cameras total across the group.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group CCTV & Security Head | G3 | Full — view, add, edit, maintenance recording, bulk import, export | Primary owner |
| Group COO | G4 | View — KPI summary and branch compliance overview only; read-only | Cannot add or edit cameras |
| Branch Security Supervisor | G2 | View — own branch cameras only; can record maintenance for own branch | Branch-scoped; no add/import |
| Branch Principal | G2 | View — own branch summary only; no camera details or credentials | Read-only, summary level |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('cctv_security_head', 'branch_security_supervisor')` with branch-scope filter for G2. DVR credential fields masked for all roles except G3.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Security  ›  CCTV Camera Inventory
```

### 3.2 Page Header
```
CCTV Camera Inventory                  [+ Add Camera]  [Bulk Import ↑]  [Export Inventory ↓]
[Group Name] — Group CCTV & Security Head · Last updated: [timestamp]
[N] Total Cameras  ·  [N] Branches  ·  [N] Non-Functional  ·  Coverage Compliance: [N]%
```

### 3.3 Alert Banner (conditional — operational issues requiring attention)

| Condition | Banner Text | Severity |
|---|---|---|
| Branch below gate minimum (< 2 functional cameras at gate) | "[N] branch(es) have fewer than 2 functional gate cameras — minimum coverage standard not met: [Branch list]." | Red |
| Girls hostel entry/exit camera non-functional | "Girls Hostel entry/exit camera [Camera ID] at [Branch] is Non-Functional. Immediate repair required." | Red |
| Camera non-functional > 7 days | "[N] camera(s) have been Non-Functional for more than 7 days with no repair logged: [IDs]." | Red |
| Maintenance overdue > 30 days past due date | "[N] camera(s) are more than 30 days past their scheduled maintenance due date." | Amber |
| Recording inactive on required camera | "[N] camera(s) in 24/7-required areas (Gate/Girls Hostel) have recording marked as inactive." | Red |
| Branch below any coverage standard | "[N] branch(es) are below minimum CCTV coverage standards in at least one area type." | Amber |

Max 5 alerts visible. Alert links route to the filtered camera table. "View full security audit log →" shown below alerts.

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Cameras | Total camera count across all branches | Blue always (informational) | → Main table (no filter) |
| Functional % | Functional cameras / total cameras × 100 | Green ≥ 95% · Yellow 85–94% · Red < 85% | → Main table filtered to Functional |
| Non-Functional Count | Count of cameras with status Non-Functional | Green = 0 · Yellow 1–10 · Red > 10 | → Main table filtered to Non-Functional |
| Maintenance Overdue | Cameras past their Next Maintenance Due date | Green = 0 · Yellow 1–20 · Red > 20 | → Main table filtered to overdue |
| Branches Below Coverage Standard | Branches not meeting minimum cameras per area type | Green = 0 · Yellow 1–3 · Red > 3 | → Section 5.2 |
| Coverage Compliance % | Branches meeting all coverage standards / total branches × 100 | Green ≥ 95% · Yellow 80–94% · Red < 80% | → Section 5.2 |
| Recording Inactive (24/7 Areas) | Cameras in gate/hostel areas with recording inactive | Green = 0 · Red if any | → Main table filtered to recording=inactive and area=gate/hostel |
| Cameras Added This Month | New cameras registered this calendar month | Blue always (informational) | → Main table sorted by installation date descending |

**HTMX:** `hx-trigger="every 5m"` → Non-Functional Count and Recording Inactive auto-refresh.

---

## 5. Sections

### 5.1 Camera Inventory Table (Primary Table)

> Full list of all registered CCTV cameras across all branches.

**Search:** Camera ID, location description, DVR/NVR unit name, branch name. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Area Type | Multi-select | Gate / Corridor / Classroom / Hostel Block / Parking / Server Room / Admin Block / Playground / Canteen |
| Camera Status | Checkbox | Functional / Degraded / Non-Functional / Under Maintenance |
| Camera Type | Checkbox | Dome / Bullet / PTZ / Fisheye |
| Recording Active | Radio | All · Yes · No |
| Maintenance Overdue | Toggle | Show only cameras past Next Maintenance Due date |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Camera ID | ✅ | System-generated unique ID (e.g., CAM-BRN-0042); link → `camera-detail` drawer |
| Branch | ✅ | Branch name |
| Area Type | ✅ | Colour-coded badge: Gate (Red) · Hostel Block (Purple) · Corridor (Blue) · Parking (Orange) · Server Room (Dark Grey) · Classroom (Green) · Admin Block (Teal) · Playground (Lime) · Canteen (Yellow) |
| Location Description | ❌ | Free-text location (e.g., "Main gate — left pillar, facing road") |
| Camera Type | ✅ | Dome / Bullet / PTZ / Fisheye |
| Resolution | ✅ | e.g., 2MP / 4MP / 8MP / 12MP |
| Status | ✅ | Badge: Functional (Green) · Degraded (Yellow) · Non-Functional (Red) · Under Maintenance (Grey) |
| DVR/NVR Unit | ✅ | Unit name/ID |
| Installation Date | ✅ | Date; age shown as "(N years)" in tooltip |
| Last Maintenance | ✅ | Date; Red if > 6 months ago |
| Next Maintenance Due | ✅ | Date; Red if past due · Yellow if within 30 days |
| Recording Active | ✅ | Yes (Green ✅) / No (Red ❌) |
| Actions | ❌ | View · Record Maintenance · Edit · Decommission |

**Default sort:** Status (Non-Functional first, then Degraded, then Under Maintenance, then Functional), then Next Maintenance Due ascending.
**Pagination:** Server-side · 25/page.

---

### 5.2 Branch Coverage Compliance Panel

> Per-branch coverage compliance view — shows whether each branch meets minimum camera requirements per area type.

**Display:** Table with compliance matrix structure.

**Search:** Branch name. 300ms debounce.

**Columns:**
| Column | Notes |
|---|---|
| Branch | Branch name; link → expands to per-area-type breakdown |
| Campus Type | Day School / Residential / Large Multi-Block |
| Total Cameras | Count of all cameras at branch |
| Gate Coverage | ✅ Met / ❌ Not Met — shows "X/2 functional" |
| Girls Hostel Coverage | ✅ Met / ❌ Not Met / N/A (if no girls hostel) |
| Corridor Coverage | ✅ Met / ❌ Not Met |
| Parking Coverage | ✅ Met / ❌ Not Met / N/A |
| Overall Compliance | Green ✅ All Met / Red ❌ [N] area(s) below standard |
| Actions | View Detail · Send Report |

**Pagination:** Server-side · 25/page.
**Default sort:** Overall Compliance (non-compliant first).

---

## 6. Drawers / Modals

### 6.1 Drawer: `camera-detail`
- **Trigger:** Camera ID link in Section 5.1 table
- **Width:** 600px
- **Tabs:** Specifications · Maintenance History · DVR/NVR · Coverage Map

**Specifications tab:**
| Field | Notes |
|---|---|
| Camera ID | Read-only |
| Branch | Read-only |
| Area Type | Read-only badge |
| Location Description | Read-only |
| Camera Type | Dome / Bullet / PTZ / Fisheye |
| Resolution | e.g., 4MP |
| Make / Model | Manufacturer and model number |
| IP Address | Masked unless G3: shown as "192.168.x.xxx" for G2; full IP for G3 |
| Field of View (degrees) | Read-only |
| Night Vision | Yes / No |
| Recording Mode | Continuous / Motion-triggered / Schedule |
| Recording Active | Yes ✅ / No ❌ |
| Installation Date | Date + installer name if recorded |
| Warranty Expiry | Date; Red if expired |
| Status | Badge |
| Status Notes | Reason for Degraded / Non-Functional / Under Maintenance |
| Last Updated By | User name + timestamp |

**Maintenance History tab:**
- Chronological list of all maintenance records:
  - Date · Maintenance Type (Preventive / Corrective / Emergency) · Technician Name · Parts Replaced · Notes · Next Due Set To
- Paginated if > 10 records
- [+ Record Maintenance] button at top → opens `record-maintenance` drawer prefilled with Camera ID

**DVR/NVR tab:**
| Field | Notes |
|---|---|
| DVR/NVR Unit Name | Read-only |
| Unit ID | Read-only |
| Unit IP Address | Masked for G2; full for G3 |
| Login Username | Read-only; shown for G3 only |
| Login Password | Masked (●●●●●●●●); [Reveal] button for G3 only with audit log entry |
| Channel Number on DVR | Read-only |
| Footage Retention Period | Days (e.g., 30 days) |
| Storage Used | GB / Total GB for this unit |

**Coverage Map tab:**
- Static floor plan image of branch (if uploaded) with camera location pin.
- If no floor plan uploaded: placeholder "Floor plan not uploaded for this branch. [Upload Floor Plan]" (G3 only).
- Camera angle overlay (cone graphic) if field-of-view data available.

---

### 6.2 Drawer: `add-camera`
- **Trigger:** [+ Add Camera] button in page header
- **Width:** 580px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Searchable dropdown | Required |
| Area Type | Select | Gate / Corridor / Classroom / Hostel Block / Parking / Server Room / Admin Block / Playground / Canteen · Required |
| Location Description | Text · max 200 chars | Required · min 10 chars |
| Camera Type | Radio | Dome / Bullet / PTZ / Fisheye · Required |
| Make / Model | Text · max 100 chars | Required |
| Resolution | Select | 1MP / 2MP / 4MP / 8MP / 12MP / Other | Required |
| Field of View (degrees) | Number · 1–360 | Optional |
| Night Vision | Toggle | Default: Yes |
| IP Address | Text | Optional; validate IPv4 format if provided |
| Recording Mode | Select | Continuous / Motion-triggered / Schedule · Required |
| Recording Active | Toggle | Default: Yes |
| DVR/NVR Unit | Searchable dropdown (units at selected branch) | Required; [+ Add New DVR/NVR] inline option |
| DVR Channel Number | Number · 1–64 | Required |
| DVR Login Username | Text · max 50 chars | Optional; stored encrypted |
| DVR Login Password | Password field | Optional; stored encrypted; never returned in plain text after save |
| Installation Date | Date picker | Required; cannot be future date |
| Installer Name / Agency | Text · max 100 chars | Optional |
| Warranty Expiry | Date picker | Optional |
| Footage Retention Period (days) | Number · 1–365 | Required |
| Initial Status | Radio | Functional / Degraded / Under Maintenance · Default: Functional |
| Status Notes | Textarea · max 300 chars | Required if status is Degraded or Under Maintenance |

**Validation:**
- Branch + Area Type + Location Description combination must be unique (warn, not block: "A camera with a similar location already exists. Are you sure this is a different camera?").
- IP Address uniqueness check within branch (error if duplicate IP).

**Footer:** [Cancel] [Save Camera →]

---

### 6.3 Drawer: `record-maintenance`
- **Trigger:** "Record Maintenance" action in table or drawer footer
- **Width:** 440px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Camera ID | Read-only pre-filled | — |
| Camera Location | Read-only pre-filled | — |
| Maintenance Date | Date picker | Required; cannot be future date |
| Maintenance Type | Radio | Preventive / Corrective / Emergency · Required |
| Technician Name | Text · max 100 chars | Required |
| Technician Contact | Text · max 50 chars | Optional |
| Agency / Vendor | Text · max 100 chars | Optional |
| Issue Found | Textarea · max 400 chars | Required for Corrective and Emergency types |
| Parts Replaced | Textarea · max 300 chars | Optional; list of parts |
| Maintenance Notes | Textarea · max 500 chars | Optional |
| Camera Status After Maintenance | Radio | Functional / Degraded / Still Under Maintenance · Required |
| Recording Active After | Toggle | Required |
| Next Maintenance Due Date | Date picker | Required; must be after maintenance date |

**Validation:**
- Maintenance Date cannot be in the future.
- Next Maintenance Due must be at least 1 day after Maintenance Date.
- Status After required; if "Still Under Maintenance", a follow-up note is required.

**Footer:** [Cancel] [Save Maintenance Record →]

---

### 6.4 Drawer: `bulk-import`
- **Trigger:** [Bulk Import ↑] button in page header
- **Width:** 440px

**Purpose:** CSV import of camera inventory for a newly commissioned branch or a full inventory refresh.

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Searchable dropdown | Required; import applies to this branch only |
| Import File | File upload · .csv only · max 5MB | Required |
| Duplicate Handling | Radio | Skip duplicates (same Camera ID) / Overwrite existing / Abort if any duplicate found · Required |

**CSV Format Guidance:**
- Template download link: [Download CSV Template]
- Required columns: `area_type`, `location_description`, `camera_type`, `resolution`, `make_model`, `dvr_unit_name`, `dvr_channel`, `installation_date`, `recording_active`, `status`
- Optional columns: `ip_address`, `field_of_view`, `night_vision`, `recording_mode`, `warranty_expiry`, `retention_days`, `status_notes`
- Date format: YYYY-MM-DD

**Validation steps (server-side, shown in preview before confirm):**
1. File parsed and validated — row count, column headers.
2. Per-row validation: required fields, date formats, valid enum values.
3. Duplicate check against existing cameras at selected branch.
4. Preview table shown: N rows valid · N rows with warnings · N rows with errors.
5. User can download error report, correct CSV, and re-upload.

**Confirm step:** Shows summary: "Import [N] cameras to [Branch]? [N] will be created, [N] skipped/overwritten." [Confirm Import] [Cancel]

**Footer:** [Cancel] [Validate & Preview →] (then after preview: [Confirm Import →])

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Camera added successfully | "Camera [Camera ID] added at [Branch] — [Area Type]." | Success | 4s |
| Maintenance recorded | "Maintenance recorded for Camera [ID]. Next due: [date]." | Success | 4s |
| Status changed to Non-Functional | "Camera [ID] marked as Non-Functional. Security gap flagged for [Branch]." | Warning | 6s |
| Status changed to Functional | "Camera [ID] restored to Functional status at [Branch]." | Success | 4s |
| DVR password revealed | "DVR credentials for Camera [ID] accessed. Audit entry recorded." | Warning | 5s |
| Bulk import complete | "Bulk import complete: [N] cameras added to [Branch]. [N] rows skipped." | Success | 5s |
| Bulk import failed | "Import failed: [N] rows have errors. Download error report to review." | Error | 8s |
| Inventory exported | "Camera inventory export is being prepared. Download will begin shortly." | Info | 4s |
| Camera decommissioned | "Camera [ID] has been decommissioned and removed from active inventory." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No cameras registered for group | "No CCTV Cameras Registered" | "No camera inventory has been added yet. Start by registering cameras for each branch." | [+ Add Camera] |
| No cameras for selected branch | "No Cameras at This Branch" | "No cameras are registered for the selected branch. Import or add cameras to begin." | [+ Add Camera] [Bulk Import ↑] |
| No non-functional cameras | "All Cameras Functional" | "All registered cameras across all branches are currently functional." | — |
| No maintenance overdue | "All Maintenance Up to Date" | "No cameras are past their scheduled maintenance due date." | — |
| Search returns no results | "No Cameras Found" | "No cameras match your search or applied filters." | [Clear Filters] |
| No cameras for selected area type | "No Cameras in This Area Type" | "No cameras are registered for the selected area type at the selected branch." | [+ Add Camera] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + camera table (15 rows × 13 columns) + branch compliance panel + alerts |
| Table filter/search | Inline skeleton rows (8 rows × 13 columns) |
| KPI auto-refresh | Shimmer on Non-Functional Count and Recording Inactive card values only |
| Camera detail drawer open | 600px drawer skeleton with 4-tab bar and field skeletons |
| Maintenance History tab | List skeleton (5 rows with date + text placeholders) |
| Coverage Map tab | Rectangle placeholder (full width, 300px, animated shimmer) |
| Add camera form open | 580px drawer with 20 field skeletons |
| Record maintenance drawer open | 440px drawer with 12 field skeletons |
| Bulk import preview | Table skeleton (10 rows × 5 columns) with progress bar above |
| Branch compliance panel | Table skeleton (10 rows × 8 columns) |

---

## 10. Role-Based UI Visibility

| Element | CCTV & Security Head G3 | Group COO G4 | Branch Security Supervisor G2 | Branch Principal G2 |
|---|---|---|---|---|
| View All Branches Table | ✅ | ❌ (KPI + compliance summary only) | Own branch only | Own branch summary only |
| Add Camera | ✅ | ❌ | ❌ | ❌ |
| Record Maintenance | ✅ | ❌ | ✅ (own branch) | ❌ |
| Edit Camera Details | ✅ | ❌ | ❌ | ❌ |
| Decommission Camera | ✅ | ❌ | ❌ | ❌ |
| Bulk Import | ✅ | ❌ | ❌ | ❌ |
| View DVR IP Address (full) | ✅ | ❌ | ❌ (masked) | ❌ |
| Reveal DVR Credentials | ✅ (with audit) | ❌ | ❌ | ❌ |
| Export Inventory | ✅ | ✅ (aggregate report) | ✅ (own branch) | ❌ |
| View Compliance Panel | ✅ | ✅ (read-only) | ✅ (own branch) | ✅ (own branch, summary) |
| Alert Banner | ✅ (all alerts) | ✅ (read-only) | ✅ (own branch alerts) | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/security/cctv/` | JWT (G3+) | Camera inventory table; params: `branch_id`, `area_type`, `status`, `camera_type`, `recording_active`, `maintenance_overdue`, `q`, `page` |
| GET | `/api/v1/group/{group_id}/welfare/security/cctv/kpi-cards/` | JWT (G3+) | KPI summary bar data |
| GET | `/api/v1/group/{group_id}/welfare/security/cctv/branch-compliance/` | JWT (G3+) | Branch coverage compliance panel |
| GET | `/api/v1/group/{group_id}/welfare/security/cctv/{camera_id}/` | JWT (G3+) | Single camera detail drawer payload |
| POST | `/api/v1/group/{group_id}/welfare/security/cctv/` | JWT (G3) | Create new camera record |
| PATCH | `/api/v1/group/{group_id}/welfare/security/cctv/{camera_id}/` | JWT (G3) | Update camera details |
| DELETE | `/api/v1/group/{group_id}/welfare/security/cctv/{camera_id}/` | JWT (G3) | Decommission camera (soft delete) |
| POST | `/api/v1/group/{group_id}/welfare/security/cctv/{camera_id}/maintenance/` | JWT (G3, G2-branch) | Record maintenance entry |
| GET | `/api/v1/group/{group_id}/welfare/security/cctv/{camera_id}/maintenance/` | JWT (G3+) | Maintenance history for camera |
| POST | `/api/v1/group/{group_id}/welfare/security/cctv/bulk-import/` | JWT (G3) | Validate and import CSV; params: `branch_id`, `duplicate_handling` |
| GET | `/api/v1/group/{group_id}/welfare/security/cctv/bulk-import/template/` | JWT (G3) | Download CSV import template |
| GET | `/api/v1/group/{group_id}/welfare/security/cctv/{camera_id}/dvr-credentials/` | JWT (G3) | Reveal DVR credentials (audit logged) |
| GET | `/api/v1/group/{group_id}/welfare/security/cctv/export/` | JWT (G3+) | Async export (CSV/XLSX) of full inventory |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../cctv/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Camera table search | `input delay:300ms` | GET `.../cctv/?q={val}` | `#camera-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../cctv/?{filters}` | `#camera-table-section` | `innerHTML` |
| Maintenance overdue toggle | `change` | GET `.../cctv/?maintenance_overdue=true` | `#camera-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../cctv/?page={n}` | `#camera-table-section` | `innerHTML` |
| Open camera detail drawer | `click` on Camera ID | GET `.../cctv/{id}/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch (lazy) | `click` on tab | GET `.../cctv/{id}/?tab={name}` | `#drawer-tab-content` | `innerHTML` |
| Add camera form submit | `click` | POST `.../cctv/` | `#camera-table-section` | `innerHTML` (refresh table) |
| Record maintenance submit | `click` | POST `.../cctv/{id}/maintenance/` | `#camera-row-{id}` | `outerHTML` |
| Bulk import validate & preview | `click` | POST `.../cctv/bulk-import/?validate_only=true` | `#import-preview-area` | `innerHTML` |
| Bulk import confirm | `click` | POST `.../cctv/bulk-import/` | `#camera-table-section` | `innerHTML` |
| Branch compliance panel load | `load` | GET `.../cctv/branch-compliance/` | `#compliance-panel` | `innerHTML` |
| Reveal DVR credentials | `click` | GET `.../cctv/{id}/dvr-credentials/` | `#dvr-credentials-panel` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
