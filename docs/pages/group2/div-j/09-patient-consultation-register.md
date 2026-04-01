# 09 — Patient Consultation Register

> **URL:** `/group/health/consultations/`
> **File:** `09-patient-consultation-register.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group School Medical Officer (primary) · Group Medical Coordinator (view/audit)

---

## 1. Purpose

Complete log of all patient consultations at all branches' medical rooms across the group. Every student or staff visit to the medical room is recorded here — presenting complaint, examination notes, treatment given, prescription dispensed, referral decision, and follow-up requirement. This is the clinical record system for EduForge — the equivalent of a clinical encounter log in a school health context.

Confidentiality rules apply throughout. Only authorised roles see identifiable patient records. Consultation data is the primary source for identifying health trends across the group: recurring illness patterns, injury hotspots, mental health referral volumes, and seasonal outbreak signals. Every entry must be completed at the time of consultation (or within same working day) to ensure accuracy and prevent audit flags.

The School Medical Officer owns day-to-day entry across all branches. The Medical Coordinator uses this register for audit, trend analysis, escalation, and cross-branch comparison. Strict access control prevents branch-level staff from seeing consultations at other branches, and prevents non-medical roles from accessing any identifiable clinical content.

Scale: 200–2,000 consultations per month across all branches. Large groups (50 branches, 100,000 students) may see 100+ consultations on a single peak day (examination periods, post-sports events, outbreak days).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group School Medical Officer | G3 | Full — create, edit, view all branches | Primary clinical data entry owner |
| Group Medical Coordinator | G3 | View all, export, escalate — no create | Audit and oversight role |
| Group Mental Health Coordinator | G3 | View — Mental Health complaint category only | Restricted filter enforced server-side |
| Group Emergency Response Officer | G3 | View — Injury/Emergency complaint categories only | Restricted filter enforced server-side |
| Branch Principal | Branch G3 | Count summary only — no clinical details | No access to individual records |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('school_medical_officer', 'medical_coordinator', 'mental_health_coordinator', 'emergency_response_officer')` with server-side category-level filters applied per role before queryset is returned.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Patient Consultation Register
```

### 3.2 Page Header
- **Title:** `Patient Consultation Register`
- **Subtitle:** `[N] Consultations This Month · [N] Today · [N] Follow-ups Pending`
- **Right controls:** `+ New Consultation` (School Medical Officer only) · `Advanced Filters` · `Export CSV` (Medical Coordinator only)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Follow-up overdue (due date passed, not marked done) | "[N] patient follow-ups are overdue. Review required." | Red |
| Recurring patient flagged (3+ visits this month) | "[N] patients have visited 3 or more times this month — possible chronic or serious condition." | Amber |
| Referral unanswered > 48 hours | "[N] referrals have not been updated within 48 hours of issue." | Amber |
| Consultation entry backdated > 3 days | "[N] consultation entries have been backdated by more than 3 days — audit flag raised." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Consultations This Month | Total consultation records in current calendar month | Blue always |
| Consultations Today | Records with today's date | Green if > 0 · Grey if 0 |
| Follow-ups Pending | Records where `follow_up_required = true` and follow-up not yet marked done | Green = 0 · Yellow 1–10 · Red > 10 |
| Referrals to Hospital | Records where `referred = true` this month | Blue always |
| Recurring Patients (3+ visits this month) | Distinct patients with ≥ 3 consultations in current month | Green = 0 · Yellow 1–5 · Red > 5 |
| Branches with Zero Consultations This Month | Branches where no consultation recorded this month | Green = 0 · Yellow 1–3 · Red > 3 |

---

## 5. Main Table — Patient Consultation Register

**Search:** Patient name, student ID/staff ID, branch name. 300ms debounce, minimum 2 characters.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches in group |
| Date Range | Date picker | From – To |
| Complaint Category | Checkbox | Fever / Injury / GI / Headache / Dental / Mental Health / Other |
| Patient Type | Radio | All / Student / Staff |
| Follow-up Required | Radio | All / Yes / No |
| Referred to Hospital | Radio | All / Yes / No |
| Doctor | Single-select | All visiting/assigned doctors |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Date | ✅ | DD-MMM-YYYY |
| Time | ✅ | HH:MM (24h) |
| Branch | ✅ | Branch name |
| Patient Name | ✅ | Identifiable — visible to authorised roles only; masked as `[REDACTED]` for count-only roles |
| Type | ✅ | Student / Staff badge |
| Class / Dept | ✅ | Class + Section for students; Department for staff |
| Complaint Category | ✅ | Colour-coded badge: Fever (orange) / Injury (red) / GI (yellow) / Headache (grey) / Dental (blue) / Mental Health (purple) / Other (grey) |
| Doctor | ✅ | Treating doctor name |
| Treatment | ❌ | Short text summary (first 60 chars) |
| Referral | ✅ | None / Referred (amber badge with hospital name) |
| Follow-up Required | ✅ | No / Pending (amber) / Overdue (red) / Done (green) |
| Status | ✅ | Open / Closed / Escalated |
| Actions | ❌ | View · Edit · Follow-up |

**Default sort:** Date descending, then Time descending (most recent first).
**Pagination:** Server-side · 25 records per page.
**Bulk actions:** Export selected rows to CSV (Medical Coordinator only — confidential fields excluded unless explicit role check passes).

---

## 6. Drawers / Modals

### 6.1 Drawer — `consultation-view` (700px, right side)

Triggered by clicking **View** in the Actions column or the patient name link. Read-only for Medical Coordinator; editable for School Medical Officer within 24 hours.

**Tabs:**

#### Tab 1 — Consultation
| Field | Type | Notes |
|---|---|---|
| Date | Read-only | |
| Time | Read-only | |
| Doctor | Read-only | Name + qualification |
| Presenting Complaint | Read-only | Free text — full entry |
| Examination Notes | Read-only | Full clinical notes |
| Temperature (°C) | Read-only | If recorded |
| Blood Pressure | Read-only | Systolic/Diastolic if recorded |
| Weight (kg) | Read-only | If recorded |
| Diagnosis Code | Read-only | ICD-10 short code + description (e.g., J00 — Common cold) |
| Treatment Given | Read-only | Full treatment description |
| Medicines Prescribed | Read-only | List — see Prescription tab |
| Advice Given | Read-only | Discharge/home care advice |
| Time Spent (mins) | Read-only | Duration of consultation |

#### Tab 2 — Patient Profile
| Field | Type | Notes |
|---|---|---|
| Full Name | Read-only | |
| Student ID / Staff ID | Read-only | |
| Class / Section / Branch | Read-only | |
| Blood Group | Read-only | Pulled from student health record |
| Known Allergies | Read-only | List with severity — from health record |
| Chronic Conditions | Read-only | From health record — readonly here |
| Hostel / Day Scholar | Read-only | For students |

#### Tab 3 — Prescription
| Column | Notes |
|---|---|
| Medicine Name | Generic name preferred |
| Dosage | e.g., 500 mg |
| Frequency | e.g., Twice daily after meals |
| Duration | e.g., 3 days |
| Dispensed from Medical Room Stock | Yes / No |
| External Prescription | Yes (if referred to pharmacy) / No |

#### Tab 4 — Referral
| Field | Type | Notes |
|---|---|---|
| Referred To | Read-only | Hospital name / Specialist name |
| Referral Date | Read-only | |
| Reason for Referral | Read-only | Clinical reason |
| Contact / Hospital Phone | Read-only | |
| Referral Status | Read-only | Pending / Visited / Resolved |
| Referral Notes | Read-only | Any follow-up notes from hospital |

> Referral status update button appears here for School Medical Officer: **Update Referral Status** → inline form.

#### Tab 5 — Follow-up History
Chronological list of all previous consultations for this patient across any branch.

| Column | Notes |
|---|---|
| Date | |
| Branch | |
| Doctor | |
| Complaint Category | |
| Diagnosis | ICD-10 code |
| Outcome | |
| Follow-up Required | |

Footer shows total consultation count for patient and "Recurring Patient" badge if ≥ 3 this month.

---

### 6.2 Drawer — `consultation-create` (680px, right side)

Triggered by **+ New Consultation** button. School Medical Officer only.

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select (auto-set to officer's branch for branch-level; selectable for group-level) | Required |
| Patient Search | Autocomplete (name or ID → load health record summary) | Required; minimum 3 chars; debounce 300ms |
| Patient Type | Radio — Student / Staff | Required |
| Doctor | Single-select (from doctor registry) | Required |
| Date | Date picker (defaults to today; backdating allowed; triggers audit flag if > 3 days) | Required |
| Time | Time picker (defaults to now) | Required |
| Presenting Complaint | Textarea (free text, max 1,000 chars) | Required; confidential |
| Complaint Category | Single-select: Fever / Injury / GI / Headache / Dental / Mental Health / Other | Required |
| Examination Notes | Textarea (free text, max 2,000 chars) | Optional; confidential |
| Temperature (°C) | Number input | Optional; range 35–42 |
| Blood Pressure | Two number inputs (systolic / diastolic) | Optional |
| Weight (kg) | Number input | Optional |
| Diagnosis | Single-select ICD-10 short list (50 school-relevant codes) + free text override | Required |
| Treatment Given | Textarea (max 1,000 chars) | Required |
| Prescription | Repeating line items: Medicine / Dosage / Frequency / Duration / Dispensed from stock (yes/no) | Optional; add row button |
| Advice Given | Textarea (max 500 chars) | Optional |
| Time Spent (mins) | Number input | Required |
| Referral Decision | Radio — No Referral / Refer to Hospital / Refer to Specialist | Required |
| Referral Details | Conditional (shown when referral selected): Hospital name, reason, contact | Conditional required |
| Follow-up Required | Toggle — Yes / No | Required |
| Follow-up Date | Date picker | Required if follow-up = Yes |

> **Confidentiality notice** displayed above free-text fields: *"All clinical entries are confidential and accessible only to authorised medical roles."*

**Footer:** `Cancel` · `Save Draft` · `Save & Close`

---

### 6.3 Modal — `mark-follow-up-done` (420px, centred)

Triggered by **Follow-up** action on a record with pending follow-up.

| Field | Type | Validation |
|---|---|---|
| Patient Name | Read-only | |
| Original Follow-up Date | Read-only | |
| Follow-up Completed On | Date picker (defaults to today) | Required |
| Outcome Notes | Textarea (max 500 chars) | Required |
| Further Action Required | Radio — Yes / No | Required |
| Next Follow-up Date | Date picker | Required if further action = Yes |

**Footer:** `Cancel` · `Mark as Done`

---

### 6.4 Modal — `escalate-to-coordinator` (440px, centred)

Triggered by **Escalate** link on any consultation (School Medical Officer only; auto-available when recurring patient flag or serious diagnosis).

| Field | Type | Validation |
|---|---|---|
| Consultation ID | Read-only | |
| Patient ID | Read-only (name masked for audit trail) | |
| Reason for Escalation | Textarea (max 500 chars) | Required |
| Urgency Level | Radio — Routine / Urgent / Immediate | Required |
| Attach Notes | File upload (PDF/JPG, max 5 MB) | Optional |

**Footer:** `Cancel` · `Escalate to Medical Coordinator`

Triggers notification to Medical Coordinator. Logs escalation timestamp in audit trail.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Consultation saved | "Consultation record saved successfully." | Success |
| Draft saved | "Draft saved. Complete and submit before end of day." | Info |
| Follow-up marked done | "Follow-up marked as complete." | Success |
| Escalation sent | "Consultation escalated to Medical Coordinator." | Success |
| Referral status updated | "Referral status updated." | Success |
| Export triggered | "Export is being prepared. Download will start shortly." | Info |
| Backdating audit flag | "Entry backdated by more than 3 days. Audit flag has been raised." | Warning |
| Save failed — validation error | "Please complete all required fields before saving." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No consultations this month | "No consultations recorded this month." | "All recorded consultations will appear here. Use + New Consultation to add a record." | `+ New Consultation` button |
| No results for current filters | "No records match your current filters." | "Try adjusting your search terms or filter criteria." | `Clear Filters` button |
| No follow-ups pending | "No follow-ups pending." | "All patient follow-ups are up to date." | — |
| No referrals this month | "No referrals issued this month." | "Referral records will appear here once issued from a consultation." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: KPI bar (6 grey cards) + table (8 grey rows × 13 columns) |
| Filter / search apply | Table rows replaced with spinner overlay; KPI bar updates after table resolves |
| Drawer open | Drawer slides in with tab skeleton (3 grey blocks per tab) while data loads |
| Patient autocomplete search | Inline spinner next to input; results appear below within 300ms |
| Export CSV generation | Button shows spinner + "Preparing export…" text; disables to prevent double-click |
| Follow-up modal save | Modal footer button shows spinner; form inputs disabled |

---

## 10. Role-Based UI Visibility

| UI Element | School Medical Officer | Medical Coordinator | Mental Health Coordinator | Emergency Response Officer | Branch Principal |
|---|---|---|---|---|---|
| Patient Name (identifiable) | ✅ Visible | ✅ Visible | ✅ Only Mental Health category | ✅ Only Injury/Emergency category | ❌ Hidden |
| Examination Notes | ✅ | ✅ | ✅ Own category | ✅ Own category | ❌ |
| Prescription Tab | ✅ | ✅ | ❌ | ❌ | ❌ |
| + New Consultation button | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit action | ✅ (within 24h) | ❌ | ❌ | ❌ | ❌ |
| Export CSV button | ❌ | ✅ | ❌ | ❌ | ❌ |
| Escalate to Coordinator | ✅ | ❌ | ❌ | ❌ | ❌ |
| KPI bar | ✅ Full | ✅ Full | Filtered counts only | Filtered counts only | Count summary widget only |
| Complaint Category filter | All categories | All categories | Mental Health only | Injury/Emergency only | ❌ No access to table |
| Follow-up modal | ✅ | ❌ | ❌ | ❌ | ❌ |
| Backdating audit flag | ✅ Sees flag | ✅ Sees flag | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/consultations/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/consultations/` | List all consultations (paginated, filtered) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/consultations/` | Create new consultation record | School Medical Officer |
| GET | `/api/v1/group/{group_id}/health/consultations/{consult_id}/` | Retrieve single consultation (full detail) | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/consultations/{consult_id}/` | Update consultation (within 24h window) | School Medical Officer |
| GET | `/api/v1/group/{group_id}/health/consultations/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/consultations/export/` | Export CSV (role-gated, redacted fields where applicable) | Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/consultations/{consult_id}/follow-up/` | Mark follow-up as done | School Medical Officer |
| POST | `/api/v1/group/{group_id}/health/consultations/{consult_id}/escalate/` | Escalate consultation to Medical Coordinator | School Medical Officer |
| PATCH | `/api/v1/group/{group_id}/health/consultations/{consult_id}/referral-status/` | Update referral status | School Medical Officer |
| GET | `/api/v1/group/{group_id}/health/consultations/patient-search/` | Autocomplete patient search by name or ID | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/consultations/patient/{patient_id}/history/` | Full consultation history for a patient | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/consultations/alerts/` | Fetch active alert banner conditions | JWT + role check |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Filter by branch ID(s) |
| `date_from` | date | Start of date range (YYYY-MM-DD) |
| `date_to` | date | End of date range |
| `complaint_category` | str[] | Filter by category slug(s) |
| `patient_type` | str | `student` or `staff` |
| `follow_up_required` | bool | Filter follow-up pending |
| `referred` | bool | Filter referred consultations |
| `doctor` | int | Filter by doctor ID |
| `page` | int | Page number |
| `page_size` | int | 25 default, max 100 |
| `search` | str | Name, ID, or branch |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Patient search autocomplete | `hx-get="/api/.../patient-search/?q={value}"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#patient-results"` | Dropdown list below input; select loads health record summary into drawer sidebar |
| Filter form apply | `hx-get="/api/.../consultations/"` `hx-trigger="change"` `hx-target="#consultation-table-body"` `hx-include="#filter-form"` | Table body replaced; KPI bar updated via separate `hx-get` on same trigger |
| Pagination | `hx-get="/api/.../consultations/?page={n}"` `hx-target="#consultation-table-body"` `hx-push-url="true"` | Table rows swapped; URL updated with page param |
| Consultation drawer open | `hx-get="/api/.../consultations/{id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in from right; tab 1 (Consultation) loaded by default |
| Drawer tab switch | `hx-get="/api/.../consultations/{id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` `hx-trigger="click"` | Tab content area replaced; active tab highlight updated |
| Mark follow-up done (modal) | `hx-post="/api/.../consultations/{id}/follow-up/"` `hx-target="#follow-up-status-{id}"` `hx-swap="outerHTML"` | Status badge in table row updated inline; modal closed; success toast fired |
| Escalate to coordinator (modal) | `hx-post="/api/.../consultations/{id}/escalate/"` `hx-target="#escalation-result"` | Modal body replaced with confirmation; row status badge updated |
| Referral status update | `hx-patch="/api/.../consultations/{id}/referral-status/"` `hx-target="#referral-status-{id}"` | Inline badge update in drawer Referral tab |
| KPI bar refresh | `hx-get="/api/.../consultations/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | Runs on page load and after any filter change |
| Alert banner refresh | `hx-get="/api/.../consultations/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Evaluated on load; banner shown or hidden based on response |
| Consultation create form submit | `hx-post="/api/.../consultations/"` `hx-target="#consultation-table-body"` `hx-on::after-request="closeDrawer(); fireToast();"` | New record prepended to table; drawer closed; toast fired |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
