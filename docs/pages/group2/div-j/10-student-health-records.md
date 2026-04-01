# 10 — Student Health Records

> **URL:** `/group/health/student-records/`
> **File:** `10-student-health-records.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Medical Coordinator (primary) · Group School Medical Officer · Group Special Education Coordinator (view special needs students)

---

## 1. Purpose

Master student health records across all branches in the group. Each student record contains: blood group, known allergies (with severity grading), chronic conditions (asthma, diabetes, epilepsy, cardiac conditions, etc.), disability and special needs status, vaccination history, emergency contact information, and parent-authorised medication permissions.

This is the single source of truth for student health identity. It is critical for emergency response — first responders must be able to access a student's blood group, allergies, and emergency contacts instantly, without navigating through multiple systems. The emergency card print function exists precisely for this use case.

Records are created at student admission time (seeded from the admissions module) and maintained by the School Medical Officer at each branch. The Medical Coordinator holds group-level oversight — enforcing completeness standards, managing bulk import for new intakes, and ensuring all hosteler records are complete (hostelers have higher risk profile due to separation from family).

Scale: 20,000–100,000 student records. Bulk import required for large annual intakes (500–2,000 new students per branch). Search and filter performance is critical at this scale — all queries server-side with indexed fields.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Medical Coordinator | G3 | Full — view all, manage standards, bulk import, export | Primary owner |
| Group School Medical Officer | G3 | Edit medical section for own branch students | Cannot edit student identity fields |
| Group Emergency Response Officer | G3 | View emergency section only — name, blood group, allergy, emergency contacts | Read-only; no clinical history |
| Group Special Education Coordinator | G3 | View special needs / disability section only | No medical/clinical history |
| Branch Principal | Branch G3 | Count summary only — no individual details | Aggregate dashboard widget only |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('medical_coordinator', 'school_medical_officer', 'emergency_response_officer', 'special_ed_coordinator')` with section-level access masks applied per role at the API serialiser layer. Branch-scoped queryset applied for School Medical Officer.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Student Health Records
```

### 3.2 Page Header
- **Title:** `Student Health Records`
- **Subtitle:** `[N] Total Records · [N] Complete · [N] Incomplete · Last Updated [Date]`
- **Right controls:** `Advanced Filters` · `Bulk Import` (Medical Coordinator only) · `Export` (Medical Coordinator only — redacted)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Hosteler student with serious condition missing emergency contact | "[N] hosteler students with serious conditions have no emergency contact on record. Immediate update required." | Red |
| Incomplete records for hosteler students | "[N] hosteler student records are incomplete (missing blood group or emergency contact)." | Red |
| Bulk import errors pending review | "Your last bulk import completed with [N] errors. Review and correct before records are finalised." | Amber |
| Records not updated in > 1 year | "[N] student records have not been updated in over 12 months. Review for accuracy." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Records | All student health records across all branches | Blue always |
| Records with Chronic Conditions | Students with one or more chronic conditions on record | Blue; sub-label shows % of total |
| Allergy Records | Students with one or more documented allergies | Blue; sub-label shows % of total |
| Incomplete Records | Records missing blood group, emergency contact, or vaccination status | Green = 0 · Yellow 1–100 · Red > 100 |
| Records Updated This AY | Records with `last_updated` in current academic year | Green ≥ 90% · Yellow 70–89% · Red < 70% |
| Students with Parent Medication Authorisation | Students with at least one parent-signed medication consent | Blue always |

---

## 5. Main Table — Student Health Records

**Search:** Student name, student ID, branch name, class. 300ms debounce, minimum 2 characters.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Class | Multi-select | Class 1–12 / Pre-KG / KG |
| Has Chronic Condition | Radio | All / Yes / No |
| Has Allergy | Radio | All / Yes / No |
| Blood Group | Multi-select | A+ / A- / B+ / B- / AB+ / AB- / O+ / O- / Unknown |
| Record Status | Radio | All / Complete / Incomplete |
| Hostel / Day Scholar | Radio | All / Hostel / Day Scholar |
| Last Updated | Radio | All / Updated this AY / Not updated this AY |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Student Name | ✅ | Link → `health-record-view` drawer |
| Student ID | ✅ | |
| Class | ✅ | Class + Section |
| Branch | ✅ | Branch name |
| Blood Group | ✅ | Value or `Unknown` (orange badge) |
| Allergy Flag | ✅ | None / Mild / Moderate / Severe (red badge) |
| Chronic Condition | ✅ | None / condition name(s) — first 2 shown, remainder as `+N more` |
| Hostel / Day Scholar | ✅ | Hostel (blue) / Day Scholar (grey) |
| Record Status | ✅ | Complete (green badge) / Incomplete (red badge) |
| Last Updated | ✅ | Date; orange if > 365 days ago |
| Actions | ❌ | View · Edit · Print Emergency Card |

**Default sort:** Record Status (Incomplete first), then Last Updated ascending (oldest first).
**Pagination:** Server-side · 25 records per page.
**Bulk actions:** Export (Medical Coordinator only — redacted: blood group + allergy only, no clinical notes); Print Emergency Cards (selected records).

---

## 6. Drawers / Modals

### 6.1 Drawer — `health-record-view` (700px, right side)

Triggered by student name link or **View** action. Read-only for Emergency Response Officer and Special Education Coordinator (section-filtered).

**Tabs:**

#### Tab 1 — Basic
| Field | Notes |
|---|---|
| Student Photo | Pulled from portal student profile |
| Full Name | |
| Student ID | |
| Date of Birth | |
| Class / Section | |
| Branch | |
| Hostel / Day Scholar | |
| Academic Year of Admission | |

#### Tab 2 — Medical
| Field | Notes |
|---|---|
| Blood Group | Verified / Unverified badge |
| Known Allergies | List: Allergen name · Severity (Mild/Moderate/Severe) · Reaction description · Date identified |
| Chronic Conditions | List: Condition name · ICD-10 code · Date diagnosed · Current medications · Treating doctor |
| Disabilities / Special Needs | List: Type · Assessment date · Support requirements |
| Vaccination Status | Checkbox list with dates given — see below |

**Vaccination status table:**

| Vaccine | Date Given | Due Date | Status |
|---|---|---|---|
| BCG | | | Given / Pending / Unknown |
| Polio (OPV) | | | Given / Pending / Unknown |
| MMR | | | Given / Pending / Unknown |
| Hepatitis B | | | Given / Pending / Unknown |
| Tetanus (Td/Tdap) | | | Given / Pending / Unknown |
| COVID-19 | | | Given / Pending / Unknown |
| Typhoid | | | Given / Pending / Unknown |

#### Tab 3 — Emergency
| Field | Notes |
|---|---|
| Parent / Guardian Name | Primary |
| Relation to Student | Mother / Father / Guardian |
| Primary Phone | |
| Secondary Phone | |
| Family Doctor Name | |
| Family Doctor Phone | |
| Nearest Hospital | Name + address |
| Emergency Notes | Any specific instructions (e.g., "Do not administer aspirin") |

#### Tab 4 — Authorisations
| Authorisation | Status | Signed Form |
|---|---|---|
| Administration of paracetamol for fever | Authorised / Not Authorised / Pending | View upload |
| Administration of ORS for dehydration | Authorised / Not Authorised / Pending | View upload |
| Emergency hospitalisation without prior contact | Authorised / Not Authorised / Pending | View upload |
| Sharing records with external specialists | Authorised / Not Authorised / Pending | View upload |

Upload link opens signed form PDF in new tab. Upload button allows School Medical Officer to attach new consent form.

#### Tab 5 — Consultation History
Full list of consultations linked to this student (from the consultation register).

| Column | Notes |
|---|---|
| Date | |
| Branch | |
| Doctor | |
| Complaint Category | |
| Diagnosis | ICD-10 |
| Outcome | |
| Follow-up Required | |
| Referral | |

---

### 6.2 Drawer — `health-record-edit` (680px, right side)

Triggered by **Edit** action. School Medical Officer sees own branch students only; Medical Coordinator sees all.

> Student identity fields (Name, ID, DOB, Class, Branch) are **read-only** — managed by the admissions module.

**Editable sections:**

**Medical section:**

| Field | Type | Notes |
|---|---|---|
| Blood Group | Single-select | A+ / A- / B+ / B- / AB+ / AB- / O+ / O- / Unknown |
| Blood Group Verified | Toggle | Mark as lab-verified |
| Allergies | Repeating list: Allergen · Severity · Reaction · Date | Add / Remove rows |
| Chronic Conditions | Repeating list: Condition · ICD-10 · Diagnosed date · Current medications · Treating doctor | Add / Remove rows |
| Disabilities / Special Needs | Repeating list: Type · Assessment date · Support requirements | Add / Remove rows |
| Vaccination Status | Checkbox + date per vaccine | |

**Authorisations section:**

| Field | Type | Notes |
|---|---|---|
| Consent type | Read-only (preset list) | |
| Status | Toggle — Authorised / Not Authorised / Pending | |
| Upload signed form | File upload (PDF, max 5 MB) | |

**Footer:** `Cancel` · `Save Changes`

---

### 6.3 Emergency Card Print — `emergency-card-print`

Triggered by **Print Emergency Card** action. No drawer — opens a print-preview page (`/group/health/student-records/{student_id}/emergency-card/`).

Generated as printable A5 card (landscape):

| Section | Content |
|---|---|
| Header | Group logo · School name · Branch name |
| Student details | Name · Student ID · Class · Section · DOB |
| Critical medical | Blood Group (large font) · Allergies (severity highlighted) · Chronic conditions |
| Emergency contacts | Parent name + phone · Family doctor + phone · Nearest hospital |
| Authorisations | Paracetamol / ORS / Emergency hospitalisation — Authorised / Not Authorised |
| QR code | Links to full health record (JWT-protected link, valid 24h) |
| Footer | "Issued by EduForge Health Module · Date: [today]" |

**Print controls:** Print button · Download as PDF button.

---

### 6.4 Modal — `bulk-import` (500px, centred)

Triggered by **Bulk Import** button (Medical Coordinator only).

**Steps:**

**Step 1 — Upload:**
| Field | Notes |
|---|---|
| Download template | Link to CSV template with required columns |
| Upload CSV | File picker (CSV only, max 10 MB) |
| Select Branch | Single-select — import applies to one branch at a time |
| Academic Year | Single-select |

**Step 2 — Column Mapping:**
System auto-detects column headers. Mapping table shows:

| CSV Column | Maps To | Status |
|---|---|---|
| (CSV header) | (System field dropdown) | Auto-mapped / Needs review |

**Step 3 — Validation Preview:**
| Summary | Detail |
|---|---|
| Total rows | Count |
| Valid rows | Count |
| Error rows | Count — downloadable error report |
| Warning rows | Count (e.g., missing optional fields) |

Error row list shows: Row number · Column · Issue description · Suggested fix.

**Step 4 — Confirm Import:**
`Import [N] valid records` button. Error rows excluded; can download error list to fix and re-import.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Record updated | "Health record updated successfully." | Success |
| Authorisation consent uploaded | "Consent form uploaded and linked to record." | Success |
| Emergency card generated | "Emergency card ready — print or download." | Success |
| Bulk import initiated | "Import in progress. You will be notified when complete." | Info |
| Bulk import complete | "Import complete — [N] records added, [N] errors." | Success / Warning |
| Export triggered | "Export is being prepared. Download will start shortly." | Info |
| Blood group updated | "Blood group updated and marked as verified." | Success |
| Save failed — validation | "Please correct the highlighted fields before saving." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No records for branch/filter | "No health records found." | "Adjust filters or use Bulk Import to add records for this branch." | `Bulk Import` button |
| No allergies on record | "No allergies recorded for this student." | "Add known allergies in the Medical tab." | — |
| No chronic conditions | "No chronic conditions recorded." | — | — |
| No consultations in history | "No consultations on record for this student." | "Consultations will appear here once logged in the Consultation Register." | — |
| No vaccination data | "Vaccination history not recorded." | "Update vaccination status in the Medical tab." | — |
| Bulk import — no errors | "All rows imported successfully. No errors found." | — | `Close` button |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: KPI bar (6 grey cards) + table (10 grey rows × 11 columns) |
| Filter / search apply | Table body spinner overlay; KPI bar updates separately |
| Health record drawer open | Drawer skeleton: Basic tab loads first; other tabs load on click |
| Emergency card generation | Button shows spinner + "Generating card…"; disabled to prevent double-click |
| Bulk import CSV validation | Progress bar with "Validating [N] of [Total] rows…" |
| Export preparation | Button spinner + "Preparing export…" |

---

## 10. Role-Based UI Visibility

| UI Element | Medical Coordinator | School Medical Officer | Emergency Response Officer | Special Ed Coordinator | Branch Principal |
|---|---|---|---|---|---|
| Full record — all tabs | ✅ | ✅ (own branch) | ❌ | ❌ | ❌ |
| Basic tab | ✅ | ✅ | ✅ | ✅ | ❌ |
| Medical tab — full | ✅ | ✅ | ❌ | ❌ | ❌ |
| Medical tab — disabilities only | ✅ | ✅ | ❌ | ✅ | ❌ |
| Emergency tab | ✅ | ✅ | ✅ | ❌ | ❌ |
| Authorisations tab | ✅ | ✅ | ❌ | ❌ | ❌ |
| Consultation History tab | ✅ | ✅ | ❌ | ❌ | ❌ |
| Edit button | ✅ | ✅ (own branch) | ❌ | ❌ | ❌ |
| Print Emergency Card | ✅ | ✅ | ✅ | ❌ | ❌ |
| Bulk Import button | ✅ | ❌ | ❌ | ❌ | ❌ |
| Export button | ✅ | ❌ | ❌ | ❌ | ❌ |
| KPI bar | ✅ Full | ✅ (own branch) | Partial (emergency stats) | Partial (special needs count) | Count widget only |
| Alert banners | ✅ Full | ✅ (own branch) | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/student-records/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/student-records/` | List all student health records (paginated, filtered) | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/student-records/{student_id}/` | Retrieve full health record for a student | JWT + section-level access mask |
| PATCH | `/api/v1/group/{group_id}/health/student-records/{student_id}/` | Update medical section of health record | School Medical Officer / Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/student-records/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/student-records/{student_id}/emergency-card/` | Generate emergency card data (print view) | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/student-records/export/` | Export redacted CSV (blood group + allergy only) | Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/student-records/bulk-import/` | Initiate bulk import from CSV | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/student-records/bulk-import/{import_id}/status/` | Poll import job status | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/student-records/bulk-import/{import_id}/errors/` | Download error row report | Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/student-records/{student_id}/authorisations/` | Upload consent form for an authorisation | School Medical Officer / Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/student-records/alerts/` | Fetch active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/student-records/{student_id}/consultation-history/` | All consultations for a student | JWT + role check |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Filter by branch ID(s) |
| `class_name` | str[] | Filter by class |
| `has_chronic` | bool | Filter students with chronic conditions |
| `has_allergy` | bool | Filter students with allergies |
| `blood_group` | str[] | Filter by blood group |
| `record_status` | str | `complete` or `incomplete` |
| `hostel` | bool | Filter hostel/day scholar |
| `updated_this_ay` | bool | Filter by update recency |
| `page` | int | Page number |
| `page_size` | int | 25 default, max 100 |
| `search` | str | Name, ID, or branch |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search debounce | `hx-get="/api/.../student-records/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#records-table-body"` | Table rows replaced; minimum 2 chars before trigger |
| Filter form apply | `hx-get="/api/.../student-records/"` `hx-trigger="change"` `hx-target="#records-table-body"` `hx-include="#filter-form"` | Table body and KPI bar refreshed |
| Pagination | `hx-get="/api/.../student-records/?page={n}"` `hx-target="#records-table-body"` `hx-push-url="true"` | Page swap with URL update |
| Health record drawer open | `hx-get="/api/.../student-records/{student_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Basic tab loaded by default |
| Drawer tab switch | `hx-get="/api/.../student-records/{student_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content swapped |
| Emergency card trigger | `hx-get="/api/.../student-records/{student_id}/emergency-card/"` `hx-target="#print-frame"` | Print preview rendered in iframe; print/PDF buttons shown |
| Bulk import CSV upload | `hx-post="/api/.../student-records/bulk-import/"` `hx-encoding="multipart/form-data"` `hx-target="#import-step-container"` | Step 2 (column mapping) replaces step 1 content |
| Bulk import validation | `hx-get="/api/.../student-records/bulk-import/{id}/status/"` `hx-trigger="every 2s"` `hx-target="#import-progress"` | Progress bar updates until complete; stops polling on completion |
| Edit form save | `hx-patch="/api/.../student-records/{student_id}/"` `hx-target="#drawer-tab-content"` | Tab content refreshed with saved values; toast fired |
| KPI bar refresh | `hx-get="/api/.../student-records/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |
| Alert banner load | `hx-get="/api/.../student-records/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Shown or hidden based on conditions |
| Consent form upload | `hx-post="/api/.../student-records/{student_id}/authorisations/"` `hx-encoding="multipart/form-data"` `hx-target="#auth-row-{auth_id}"` | Authorisation row updated with new status badge |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
