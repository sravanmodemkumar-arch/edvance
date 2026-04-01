# 17 — Insurance Claim Register

> **URL:** `/group/health/insurance-claims/`
> **File:** `17-insurance-claim-register.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Medical Coordinator (primary) · Group School Medical Officer (submit claims for own branch)

---

## 1. Purpose

Track every student and staff insurance claim across all branches from first notice of loss through final settlement. The register covers three claim types: accident claims (injuries sustained on campus, on transport, or during school activities), medical/hospitalisation claims (illness-related admissions), and death claims. Each claim record captures the full lifecycle: incident date, affected person details, injury or illness type, treating hospital, insurer reference number, amount claimed, amount approved, settlement date, and any rejection reasons.

Role 88 (Group Medical Insurance Coordinator, G0) operates externally — they liaise directly with insurers and brokers and do not have a platform login. The Group Medical Coordinator is the authoritative platform user for all claim record management in EduForge. Branch-level School Medical Officers may initiate claims for incidents at their own branch; the Medical Coordinator reviews and progresses all claims to settlement.

Operational importance: prevents policy lapse risk by flagging claims not filed within 30 days of an incident, surfaces high-value or rejected claims needing immediate coordinator attention, and provides a full audit trail for the insurer, board, and any regulatory inquiry.

Scale: 20–200 claims per academic year across all branches of a large group.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Medical Coordinator | G3 | Full CRUD — create, edit, update status, settle, export | Primary platform owner of all claims |
| Group School Medical Officer | G3 | Create claims for own branch + view own branch claims | Cannot edit or settle claims from other branches |
| CFO / Finance Director | Group | View all claims + export | Financial oversight; no create or edit |
| CEO | Group | View KPI summary and claim totals only | No drill-down into individual claim records |
| Medical Insurance Coordinator | G0 — External | No platform access | Communicates externally with Medical Coordinator |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('medical_coordinator', 'school_medical_officer', 'cfo', 'ceo')` on all health claim views. Branch scoping for School Medical Officer enforced server-side: `claim.branch == request.user.branch`. CFO and CEO enforce read-only via `@require_role` with `readonly=True` flag. CEO restricted to aggregate endpoints only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Insurance Claim Register
```

### 3.2 Page Header
- **Title:** `Insurance Claim Register`
- **Subtitle:** `[N] Claims This AY · [N] Pending Settlement · ₹[X] Total Claimed · ₹[X] Total Settled`
- **Right controls:** `+ File New Claim` (Medical Coordinator + School Medical Officer) · `Advanced Filters` · `Export` (Medical Coordinator + CFO)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Claim pending > 30 days without any status update | "⚠ [N] claim(s) have had no update in over 30 days. Review and follow up with insurer." | Amber |
| High-value claim (> ₹1,00,000) pending settlement | "⚠ [N] high-value claim(s) (> ₹1 lakh) are pending settlement. Priority follow-up required." | Amber |
| Rejected claim requires resubmission | "[N] claim(s) have been rejected by the insurer and require corrected resubmission." | Red |
| Claim not filed within 30 days of incident (policy lapse risk) | "POLICY LAPSE RISK: [N] incident(s) occurred more than 30 days ago without a claim being filed. Verify coverage immediately." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Claims This AY | Total claims filed in current academic year | Blue always |
| Claims Pending Settlement | Status = Filed / Under Review / Resubmitted | Green = 0 · Yellow 1–5 · Red > 5 |
| Total Amount Claimed (₹) | Sum of `amount_claimed` across all claims this AY | Blue always |
| Total Amount Settled (₹) | Sum of `amount_approved` where status = Settled | Blue always; sub-label shows settlement rate % |
| Rejected Claims | Status = Rejected (not yet resubmitted) | Green = 0 · Red ≥ 1 |
| Avg Settlement Time (days) | Mean days from `date_filed` to `settlement_date` for settled claims | Green < 30 · Yellow 30–60 · Red > 60 |

---

## 5. Main Table — Insurance Claim Register

**Search:** Claim ID, patient name, hospital name. 300ms debounce, minimum 2 characters.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches in group |
| Claim Type | Checkbox | Accident / Hospitalisation / Death |
| Status | Checkbox | Filed / Under Review / Approved / Settled / Rejected / Resubmitted |
| Policy | Multi-select | All active and historical policies |
| Date Filed | Date range picker | Custom date range |
| Days Pending | Radio | All / > 15 days / > 30 days / > 60 days |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Claim ID | ✅ | Auto-generated; format `CLM-YYYY-NNNN`; click → `claim-detail` drawer |
| Date Filed | ✅ | Date claim was entered into EduForge |
| Branch | ✅ | Branch where incident occurred |
| Patient Name | ✅ | Student or staff member name; tooltip shows ID, class, branch |
| Type | ✅ | Accident / Hospitalisation / Death — colour-coded badge |
| Policy | ✅ | Short policy name; tooltip shows policy number and insurer |
| Hospital | ✅ | Hospital name |
| Amount Claimed (₹) | ✅ | Formatted with comma separators |
| Amount Approved (₹) | ✅ | Blank if not yet settled; green text if settled |
| Status | ✅ | Filed (blue) / Under Review (amber) / Approved (teal) / Settled (green) / Rejected (red) / Resubmitted (purple) |
| Days Pending | ✅ | Days since `date_filed` where status ≠ Settled; red if > 30 |
| Actions | ❌ | View · Edit · Update Status · Download |

**Default sort:** Status (Rejected first, then Under Review, then Filed, then Approved, then Resubmitted, then Settled), then Days Pending descending.
**Pagination:** Server-side · 25 records per page.
**Bulk actions:** Export Claims Register as CSV or XLSX (Medical Coordinator + CFO only). Async background job for large exports.

---

## 6. Drawers / Modals

### 6.1 Drawer — `claim-detail` (700px, right side)

Triggered by Claim ID link or **View** action.

**Tabs:**

#### Tab 1 — Claim Details

| Field | Notes |
|---|---|
| Claim ID | Auto-generated reference |
| Date Filed | Date entered in EduForge |
| Policy | Policy name + insurer + policy number |
| Patient Name | Link to student or staff record |
| Student / Staff ID | |
| Class & Section | (Students only) |
| Branch | |
| Hostel / Day Scholar | |
| Incident Date | Date the injury/illness/event occurred |
| Incident Description | Full narrative text |
| Injury / Illness Type | ICD-10 category (e.g., S00–T98 Injuries; J00–J99 Respiratory; K00–K93 GI; etc.) + free text diagnosis |
| Hospital Name | |
| Admission Date | If hospitalisation |
| Discharge Date | If hospitalisation; blank if outpatient |
| Treating Doctor | Name and qualification |
| Total Hospital Bill (₹) | Gross bill before insurance |
| Claimed Amount (₹) | Amount formally claimed under policy |
| Policy Reference | Insurer's reference or acknowledgement number (if received) |

#### Tab 2 — Documents

Upload and view all supporting documents. Each document shows: document name, upload date, uploaded by, verified status (Verified / Pending Verification / Rejected).

| Document Type | Required For | Notes |
|---|---|---|
| Discharge Summary | Hospitalisation / Death | PDF or image; max 20 MB |
| Hospital Bill (itemised) | All types | |
| Investigation Reports (lab, radiology) | All types | Multiple files allowed |
| ID Proof | All types | Aadhar / Student ID |
| FIR Copy | Accident claims | Required if police case |
| Death Certificate | Death claims | |
| Prescription Copies | Outpatient claims | |
| Claim Form (signed) | All types | Filled insurer claim form |
| Insurer Approval Letter | Approved / Settled claims | Uploaded on receipt |

Each document row has: View (inline preview) · Download · Delete (Medical Coordinator only) · Mark Verified.

#### Tab 3 — Timeline

Chronological log of all status changes, document uploads, and notes. Each entry:

| Field | Notes |
|---|---|
| Timestamp | Date and time |
| Action | Status change / Document uploaded / Note added / Escalated |
| By | User name and role |
| Previous Status | If status change |
| New Status | If status change |
| Note | Any accompanying comment |

New entries are appended via HTMX partial without full drawer reload.

#### Tab 4 — Settlement

Editable only by Medical Coordinator. Read-only for all others.

| Field | Type | Notes |
|---|---|---|
| Insurer Reference Number | Text input | Insurer's claim reference ID |
| Approved Amount (₹) | Number input | Amount insurer approved for payment |
| Settlement Date | Date picker | |
| Payment Mode | Radio: Cheque / NEFT / Direct Hospital | |
| Payment To | Radio: Student / Parent / Hospital Direct | |
| Deductions (₹) | Number input | Any amount deducted by insurer |
| Deduction Reason | Text area | Reason for deduction (e.g., non-covered item, co-pay) |
| Settlement Notes | Text area (max 500 chars) | |

**Footer:** `Save Settlement Details` · `Mark as Settled` (final action — prompts confirmation modal).

#### Tab 5 — Notes

Internal notes by the Medical Coordinator. Not visible to branch-level School Medical Officers or any other role. Each note: timestamp, text, author. Add new note via text area + Save button.

---

### 6.2 Drawer — `claim-create` (680px, right side)

Triggered by **+ File New Claim**.

| Field | Type | Validation |
|---|---|---|
| Patient Search | Autocomplete from student/staff registry | Required; type ≥ 3 characters |
| Patient Type | Radio: Student / Staff | Auto-detected from patient search; override allowed |
| Branch | Single-select (auto-filled from patient; School Medical Officer sees own branch only) | Required |
| Incident Date | Date picker | Required; must be ≤ today |
| Incident Description | Textarea (max 1,000 chars) | Required |
| Claim Type | Radio: Accident / Hospitalisation / Death | Required |
| Policy | Single-select (auto-suggests active policies covering patient's branch) | Required |
| Hospital Name | Text input | Required |
| Admission Date | Date picker | Required for Hospitalisation/Death; optional for Accident |
| Discharge Date | Date picker | Optional; must be ≥ Admission Date if provided |
| Treating Doctor | Text input | Required |
| ICD Category | Single-select dropdown (ICD-10 chapter list) | Required |
| Injury / Illness Description | Text input (max 300 chars) | Required |
| Total Hospital Bill (₹) | Number input | Required |
| Claimed Amount (₹) | Number input | Required; must be ≤ Total Hospital Bill; auto-bounded to policy coverage limit with warning if exceeded |
| Documents Upload | Multi-file upload (PDF/JPG/PNG, max 20 MB each) | At least one document required |
| Initial Status | Fixed: Filed | Auto-set on create |

**Validation rules:**
- Incident date must be ≤ policy expiry date; warning shown if within 30 days of policy start (possible pre-existing condition exclusion).
- Patient must be confirmed as covered under selected policy (API check against policy branch coverage and scope).
- If incident date > 30 days ago: warning banner "Policy lapse risk — verify your insurer's claim filing deadline before proceeding."

**Footer:** `Cancel` · `Save as Draft` · `File Claim`

---

### 6.3 Drawer — `status-update` (500px, right side)

Triggered by **Update Status** action in table.

| Field | Type | Validation |
|---|---|---|
| Claim ID | Read-only | |
| Current Status | Read-only | |
| New Status | Single-select: Filed / Under Review / Approved / Settled / Rejected / Resubmitted | Required; must be logical progression |
| Insurer Reference Number | Text input | Required if new status = Under Review, Approved, or Settled |
| Update Note | Textarea (max 500 chars) | Required |
| Document Upload | File upload | Optional; required if status = Approved (approval letter) |

**Footer:** `Cancel` · `Update Status`

Status regression rules (server-enforced): Settled claims cannot be moved back to any prior status. Approved claims cannot be moved directly to Filed.

---

### 6.4 Modal — `reject-and-resubmit` (460px, centred)

Triggered from Status Update when new status = Rejected, or directly from a Rejected claim's Actions menu.

| Field | Type | Validation |
|---|---|---|
| Claim ID | Read-only | |
| Rejection Reason from Insurer | Textarea (max 500 chars) | Required |
| Documents to Add / Correct | Checklist of existing docs with "needs correction" flag; plus new file upload | Required — at least one corrective action |
| Planned Resubmission Date | Date picker | Required |
| Notes | Textarea (max 300 chars) | Optional |

**Footer:** `Cancel` · `Save Rejection & Schedule Resubmission`

On save: status set to Rejected; timeline entry created; alert banner count updated. When Medical Coordinator subsequently resubmits, status moves to Resubmitted.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Claim filed | "Claim [CLM-ID] filed successfully." | Success |
| Draft saved | "Claim saved as draft. Complete remaining fields to file." | Info |
| Status updated | "Claim [CLM-ID] status updated to [New Status]." | Success |
| Claim settled | "Claim [CLM-ID] marked as settled. Settlement details recorded." | Success |
| Rejection recorded | "Rejection recorded for Claim [CLM-ID]. Resubmission scheduled for [date]." | Warning |
| Document uploaded | "Document uploaded and added to Claim [CLM-ID]." | Success |
| Export initiated | "Export is being prepared. You will be notified when the download is ready." | Info |
| Validation error — patient not covered | "Selected patient is not covered under this policy. Verify policy scope before filing." | Error |
| Validation error — incident after policy expiry | "Incident date is after the policy expiry date. This claim cannot be filed under this policy." | Error |
| Save failed | "Please complete all required fields before filing the claim." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No claims this AY | "No insurance claims this academic year." | "Claims will appear here once filed. Use '+ File New Claim' to record a new claim." | `+ File New Claim` |
| No claims match filters | "No claims match your current filters." | "Try adjusting your filters or clearing the date range." | `Clear Filters` |
| No search results | "No claims found for '[search term]'." | "Check the claim ID, patient name, or hospital name." | `Clear Search` |
| Documents tab — no documents | "No documents uploaded for this claim." | "Upload the discharge summary, hospital bill, and any supporting reports." | — |
| Timeline tab — fresh claim | "No timeline events yet." | "Status changes, uploads, and notes will be recorded here." | — |
| Settlement tab — not yet approved | "Settlement details not yet available." | "Settlement information will appear here once the insurer approves this claim." | — |
| Notes — no notes | "No internal notes yet." | "Add a note to record follow-up actions or insurer communications." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 6 KPI cards (grey) + table (5 grey rows × 12 columns) |
| Filter apply | Table body spinner overlay; KPI bar refreshes simultaneously |
| Search debounce | Table body inline spinner while request in-flight |
| Claim detail drawer open | Drawer skeleton: tab bar (5 tabs) + content block (8 grey field rows) |
| Timeline tab load | Timeline skeleton (4 grey event rows) |
| Documents tab load | File list skeleton (3 grey rows with icon + name placeholders) |
| Settlement tab load | Form skeleton (6 grey input fields) |
| Claim create / edit save | Submit button spinner; all form fields disabled; overlay on drawer |
| Status update submit | Modal footer spinner; buttons disabled |
| Document upload | Per-file progress bar (0–100%); upload button disabled during upload |
| Export job | Export button shows spinner + "Preparing…" label; replaced by "Download" link when ready |

---

## 10. Role-Based UI Visibility

| UI Element | Medical Coordinator | School Medical Officer | CFO / Finance Director | CEO |
|---|---|---|---|---|
| Full claim list (all branches) | ✅ | Own branch only | ✅ | ❌ (KPI summary only) |
| + File New Claim button | ✅ | ✅ (own branch) | ❌ | ❌ |
| Edit action | ✅ | ❌ | ❌ | ❌ |
| Update Status action | ✅ | ❌ | ❌ | ❌ |
| Reject & Resubmit modal | ✅ | ❌ | ❌ | ❌ |
| Settlement tab — edit | ✅ | ❌ | ❌ | ❌ |
| Settlement tab — view | ✅ | ✅ (own branch) | ✅ | ❌ |
| Notes tab | ✅ (create + view) | ❌ | ❌ | ❌ |
| Documents tab — upload | ✅ | ✅ (own branch claims) | ❌ | ❌ |
| Documents tab — download | ✅ | ✅ (own branch) | ✅ | ❌ |
| Export button | ✅ | ❌ | ✅ | ❌ |
| KPI bar — all 6 cards | ✅ | Filtered to own branch | ✅ | Summary cards only |
| Alert banners | ✅ | Own branch alerts only | ✅ (amount alerts) | ❌ |
| Download action (single claim) | ✅ | ✅ (own branch) | ✅ | ❌ |
| Medical Insurance Coordinator G0 | No platform access | — | — | — |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/insurance-claims/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/insurance-claims/` | List all claims (paginated, filtered, branch-scoped by role) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/insurance-claims/` | File a new claim | Medical Coordinator / School Medical Officer |
| GET | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/` | Retrieve full claim detail | JWT + role check + branch scope |
| PATCH | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/` | Update claim fields | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/insurance-claims/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/insurance-claims/alerts/` | Active alert conditions | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/status/` | Update claim status | Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/settle/` | Mark claim as settled with settlement details | Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/reject/` | Record rejection and schedule resubmission | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/timeline/` | Claim timeline events | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/notes/` | Add internal note | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/notes/` | List internal notes | Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/documents/` | Upload document | Medical Coordinator / School Medical Officer |
| GET | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/documents/{doc_id}/` | Download specific document | JWT + role check |
| DELETE | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/documents/{doc_id}/` | Delete document | Medical Coordinator |
| PATCH | `/api/v1/group/{group_id}/health/insurance-claims/{claim_id}/documents/{doc_id}/verify/` | Mark document as verified | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/insurance-claims/export/` | Export claims register CSV/XLSX | Medical Coordinator / CFO |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `search` | str | Claim ID, patient name, or hospital |
| `branch` | int[] | Branch filter (multi-select) |
| `type` | str[] | `accident`, `hospitalisation`, `death` |
| `status` | str[] | `filed`, `under_review`, `approved`, `settled`, `rejected`, `resubmitted` |
| `policy` | int[] | Policy ID filter |
| `date_from` | date | Filed date range start (ISO 8601) |
| `date_to` | date | Filed date range end (ISO 8601) |
| `days_pending` | int | Filter: `15`, `30`, or `60` (greater than) |
| `page` | int | Page number (1-indexed) |
| `page_size` | int | Default 25; max 100 |
| `ordering` | str | e.g. `-days_pending`, `status`, `date_filed` |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search debounce | `hx-get="/api/.../insurance-claims/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#claims-table-body"` `hx-include="#filter-form"` | Table rows replaced; KPI bar updated |
| Filter form apply | `hx-get="/api/.../insurance-claims/"` `hx-trigger="change"` `hx-target="#claims-table-body"` `hx-include="#filter-form"` | Table rows replaced |
| KPI bar load and refresh | `hx-get="/api/.../insurance-claims/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On initial load and after filter |
| Alert banner load | `hx-get="/api/.../insurance-claims/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | On page load; permanent alerts persist until resolved |
| Pagination | `hx-get="/api/.../insurance-claims/?page={n}"` `hx-target="#claims-table-body"` `hx-push-url="true"` | Page swap preserving filter state |
| Claim detail drawer open | `hx-get="/api/.../insurance-claims/{claim_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` `hx-indicator="#drawer-loader"` | Drawer slides in; Claim Details tab default |
| Drawer tab switch | `hx-get="/api/.../insurance-claims/{claim_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` `hx-trigger="click"` | Tab content swapped lazily on first click; cached thereafter |
| Timeline tab lazy load | `hx-get="/api/.../insurance-claims/{claim_id}/timeline/"` `hx-target="#timeline-content"` `hx-trigger="click[tab='timeline'] once"` | Loaded once on first tab click |
| Add timeline entry | `hx-post="/api/.../insurance-claims/{claim_id}/status/"` `hx-target="#timeline-content"` `hx-swap="beforeend"` | New entry appended without full drawer reload |
| Notes tab load | `hx-get="/api/.../insurance-claims/{claim_id}/notes/"` `hx-target="#notes-content"` `hx-trigger="click[tab='notes'] once"` | Loaded once on first tab click |
| Add note submit | `hx-post="/api/.../insurance-claims/{claim_id}/notes/"` `hx-target="#notes-list"` `hx-swap="beforeend"` | New note appended; textarea cleared |
| Document upload progress | `hx-post="/api/.../insurance-claims/{claim_id}/documents/"` `hx-encoding="multipart/form-data"` `hx-target="#documents-list"` `hx-indicator="#upload-progress"` | Progress bar shown; document list refreshed on completion |
| Document verify | `hx-patch="/api/.../insurance-claims/{claim_id}/documents/{doc_id}/verify/"` `hx-target="#doc-row-{doc_id}"` `hx-swap="outerHTML"` | Row status badge updated |
| Claim create submit | `hx-post="/api/.../insurance-claims/"` `hx-target="#claims-table-body"` `hx-on::after-request="closeDrawer(); fireToast();"` | New row prepended to table; drawer closed; KPI refreshed |
| Status update submit | `hx-post="/api/.../insurance-claims/{claim_id}/status/"` `hx-target="#claim-row-{claim_id}"` `hx-swap="outerHTML"` `hx-on::after-request="closeDrawer(); fireToast();"` | Row status badge updated in-place |
| Settle action confirm | `hx-post="/api/.../insurance-claims/{claim_id}/settle/"` `hx-target="#claim-row-{claim_id}"` `hx-swap="outerHTML"` | Row updated; KPI bar refreshed via out-of-band swap |
| Export initiate | `hx-get="/api/.../insurance-claims/export/"` `hx-target="#export-status"` `hx-trigger="click"` | Export button replaced with "Preparing…" spinner; polling begins for download readiness |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
