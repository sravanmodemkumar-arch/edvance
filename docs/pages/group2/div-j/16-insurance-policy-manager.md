# 16 — Insurance Policy Manager

> **URL:** `/group/health/insurance-policies/`
> **File:** `16-insurance-policy-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Medical Coordinator (primary — manages in platform) · Group Medical Insurance Coordinator (G0 — external actor, feeds data to Medical Coordinator)

---

## 1. Purpose

Track and manage all student and staff medical and accident insurance policies across the group. Each policy covers a defined set of branches (or all branches), with full details on insurer, policy number, coverage type, coverage limits, premium, sum insured per student, start and end dates, renewal status, and associated documents.

The Medical Coordinator is the platform user who creates, updates, and renews policy records in EduForge. The Group Medical Insurance Coordinator (Role 88, G0) does not have a platform login — they operate externally, managing relationships with insurers and brokers, and pass policy information to the Medical Coordinator for entry into the system. This separation is intentional: the platform tracks and governs the policies; the external coordinator handles procurement.

Key operational uses: identifying when policies are expiring (renewal must be initiated ≥ 30 days in advance to avoid lapse), confirming all students and staff are covered under at least one active policy, tracking claim volumes and settlement rates for annual policy review, and providing emergency hospitalisation reference (which hospital network, what is cashless vs reimbursement).

Scale: 1–5 policies per group (typically one group-wide student accident policy, one student medical policy, one staff group mediclaim, and possibly a separate hostel-specific policy). Small groups may have only one combined policy; large groups may have separate policies per branch cluster.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Medical Coordinator | G3 | Full CRUD — create, edit, renew, update coverage, upload documents | Primary platform owner |
| CFO / Finance Director | Group | View only — for premium budget tracking | No create or edit |
| CEO / Chairman | Group | View only | Executive oversight |
| Group Emergency Response Officer | G3 | View only — for emergency hospitalisation reference | Cashless hospital list and coverage type visible |
| Medical Insurance Coordinator | G0 — External | No platform access | Feeds data to Medical Coordinator externally |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('medical_coordinator', 'cfo', 'ceo', 'chairman', 'emergency_response_officer')` with read-only enforcement for non-Coordinator roles. Premium and financial fields visible to CFO and Medical Coordinator; hidden for Emergency Response Officer.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Insurance Policy Manager
```

### 3.2 Page Header
- **Title:** `Insurance Policy Manager`
- **Subtitle:** `[N] Active Policies · [N] Students Covered · [N] Expiring Within 30 Days`
- **Right controls:** `+ Add Policy` (Medical Coordinator only) · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Policy expiry within 30 days | "URGENT: [N] policy/policies expire within 30 days. Initiate renewal immediately to avoid coverage lapse." | Red |
| Policy lapsed (expiry date past, no renewal) | "CRITICAL: [N] policy/policies have lapsed. Students may be uninsured. Immediate action required." | Red — permanent until resolved |
| Students not covered under any policy | "[N] students at [Branch(es)] are not covered under any active insurance policy." | Red |
| Premium payment overdue | "[N] policies have a premium payment that is overdue." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Active Policies | Policies with status = Active | Green if ≥ 1 · Red if 0 |
| Policies Expiring in 30 Days | Policies with expiry date ≤ today + 30 days | Green = 0 · Yellow 1–2 · Red > 2 |
| Total Students Covered | Unique students covered under at least one active policy | Blue; sub-label shows % of total enrolled |
| Total Sum Insured (₹) | Sum of (per-student sum insured × students covered) across all active policies | Blue always |
| Claims This Year — Count | Total insurance claims filed in current calendar year (all policies) | Blue always |

---

## 5. Main Table — Insurance Policy Register

**Search:** Policy number, insurer name. 300ms debounce, minimum 2 characters.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Policy Type | Checkbox | Student Accident / Student Medical / Staff Group Mediclaim / Hostel Specific / Combined |
| Status | Radio | All / Active / Expiring / Lapsed / Renewed |
| Expiry | Radio | All / Expiring in 30 days / Expiring in 60 days / Expiring in 90 days / Already expired |
| Branch Coverage | Multi-select | All branches / Specific branches |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Policy Name | ✅ | Descriptive name e.g. "Group Student Accident 2025–26"; link → `policy-detail` drawer |
| Insurer | ✅ | Insurance company name |
| Policy Number | ✅ | Alphanumeric reference |
| Type | ✅ | Badge per type |
| Branches Covered | ✅ | Count; tooltip lists branch names |
| Students Covered | ✅ | Count (latest from policy record) |
| Premium (₹/year) | ✅ | Formatted with comma separator; hidden for Emergency Response Officer |
| Sum Insured per Student (₹) | ✅ | Hidden for Emergency Response Officer |
| Start Date | ✅ | |
| Expiry Date | ✅ | Red if past; amber if within 30 days; green if > 60 days away |
| Days to Expiry | ✅ | Countdown number; negative if lapsed; red/amber/green rules same as Expiry Date |
| Status | ✅ | Active (green) / Expiring (amber) / Lapsed (red) / Renewed (blue) badge |
| Actions | ❌ | View · Edit · Renew · Download Policy |

**Default sort:** Status (Lapsed first, then Expiring, then Active), then Days to Expiry ascending.
**Pagination:** Server-side · 25/page.
**Bulk actions:** Export (Medical Coordinator, CFO only).

---

## 6. Drawers / Modals

### 6.1 Drawer — `policy-detail` (700px, right side)

Triggered by policy name link or **View** action.

**Tabs:**

#### Tab 1 — Policy Details
| Field | Notes |
|---|---|
| Policy Name | |
| Insurer | Company name + logo if available |
| Broker | Name + contact (if policy obtained via broker) |
| Policy Number | |
| Type | Badge |
| Coverage Period | Start date – Expiry date |
| Premium (₹/year) | Annual premium; hidden for Emergency Response Officer |
| GST on Premium | Amount and percentage |
| Total Policy Cost | Premium + GST |
| Payment Schedule | Annual / Half-yearly / Quarterly |
| Next Premium Due Date | Date; amber if within 30 days |
| Premium Payment Status | Paid / Overdue / Partially Paid |
| Branches Covered | List of all branches included in this policy |
| Students Covered (count) | From latest policy endorsement |
| Staff Covered (count) | From latest policy endorsement |
| Policy Effective For | All branches / Hostel students only / Day scholars only / Specific branch list |

#### Tab 2 — Coverage
What the policy covers.

| Coverage Type | Covered | Limit (₹) | Notes |
|---|---|---|---|
| Accidental Death | ✅ / ❌ | | |
| Permanent Disability | ✅ / ❌ | | |
| Accidental Hospitalisation | ✅ / ❌ | | |
| Illness Hospitalisation | ✅ / ❌ | | |
| Daily Hospital Cash | ✅ / ❌ | per day | |
| Outpatient Consultation | ✅ / ❌ | | |
| Dental (injury-related) | ✅ / ❌ | | |
| Vision (accident-related) | ✅ / ❌ | | |
| Ambulance Charges | ✅ / ❌ | | |
| Pre-existing Conditions | ❌ (standard exclusion) | — | |
| Self-harm / Suicide Attempt | ❌ (standard exclusion) | — | |

**Exclusions list:** Full text of policy exclusions (free text / uploaded from policy document).

**Cashless Hospital Network:**
- Total hospitals in network: [N]
- Download cashless hospital list (PDF/Excel)
- Nearest cashless hospitals to group branches: table — Branch · Hospital Name · Distance (km)

#### Tab 3 — Claims Summary
Claim statistics for this policy in the current policy period.

| Metric | Value |
|---|---|
| Total Claims Filed | Count |
| Claims Settled | Count + total ₹ settled |
| Claims Rejected | Count + primary rejection reasons |
| Claims Pending | Count + total ₹ pending |
| Total Amount Claimed (₹) | |
| Total Amount Settled (₹) | |
| Settlement Rate % | Settled / Filed × 100 |
| Average Claim Settlement Days | |

Claims are entered by the Medical Coordinator — EduForge does not integrate with insurer systems. Claims data is manually maintained.

#### Tab 4 — Renewal History
All past policy periods.

| Policy Period | Insurer | Policy Number | Premium (₹) | Sum Insured (₹) | Students | Total Claims | Status |
|---|---|---|---|---|---|---|---|

Each row is a historical policy period. Click row → view past policy document.

#### Tab 5 — Documents
| Document | Status | Last Updated | Action |
|---|---|---|---|
| Policy Document (PDF) | Uploaded / Missing | Date | View · Download |
| Schedule of Benefits | Uploaded / Missing | Date | View · Download |
| Cashless Hospital List | Uploaded / Missing | Date | View · Download |
| Claim Form (blank) | Uploaded / Missing | Date | View · Download |
| Endorsement Letters | List of endorsements | Date each | View · Download |
| Premium Receipt | Uploaded / Missing | Date | View · Download |

> Policy status cannot be set to Active if Policy Document is missing — enforced in UI and API.

---

### 6.2 Drawer — `policy-create` (680px, right side)

Triggered by **+ Add Policy** (Medical Coordinator only).

| Field | Type | Validation |
|---|---|---|
| Policy Name | Text input (max 150 chars) | Required |
| Insurer | Text input | Required |
| Broker Name | Text input | Optional |
| Broker Contact | Phone + email | Optional |
| Policy Number | Text input | Required; unique |
| Policy Type | Single-select: Student Accident / Student Medical / Staff Group Mediclaim / Hostel Specific / Combined | Required |
| Coverage Start Date | Date picker | Required |
| Coverage End Date | Date picker | Required; must be after start |
| Branches Covered | Multi-select (with Select All) | Required |
| Policy Scope | Radio: All students / Hostel students only / Day scholars only | Required |
| Students Covered Count | Number input | Required |
| Staff Covered Count | Number input | Required if staff policy |
| Premium per Year (₹) | Number input | Required |
| GST % | Number input | Required |
| Payment Schedule | Radio: Annual / Half-yearly / Quarterly | Required |
| Sum Insured per Student (₹) | Number input | Required |
| Coverage — what is covered | Checkbox grid (see Tab 2 fields) with limit amount inputs | Required; at least one |
| Exclusions | Textarea (max 2,000 chars) | Optional |
| Policy Document Upload | File upload (PDF, max 30 MB) | Required before setting status to Active |
| Initial Status | Radio: Draft / Active | Required |

**Footer:** `Cancel` · `Save as Draft` · `Save & Activate`

Activating without Policy Document upload triggers validation error.

---

### 6.3 Drawer — `policy-edit` (680px, right side)

Pre-populated. Policy Number and Insurer are read-only after a policy is set to Active (to preserve audit integrity). All other fields editable.

---

### 6.4 Modal — `mark-renewed` (460px, centred)

Triggered by **Renew** action. Used when an existing policy is renewed for a new period.

| Field | Type | Validation |
|---|---|---|
| Previous Policy Number | Read-only | |
| Previous Expiry Date | Read-only | |
| New Policy Number | Text input | Required; may be same or new number |
| New Coverage Start Date | Date picker | Required; should be day after previous expiry |
| New Coverage End Date | Date picker | Required |
| New Annual Premium (₹) | Number input | Required |
| New Sum Insured per Student (₹) | Number input | Required |
| Students Covered (updated count) | Number input | Required |
| Premium Payment Status | Radio: Paid / Scheduled / Overdue | Required |
| Upload New Policy PDF | File upload (PDF, max 30 MB) | Required |
| Notes | Textarea (max 300 chars) | Optional |

**Footer:** `Cancel` · `Confirm Renewal`

After renewal: old policy period moved to Renewal History; new policy period created as Active. Previous record kept for audit.

---

### 6.5 Modal — `branch-coverage-update` (480px, centred)

Triggered from Coverage tab — to add or remove branches from a policy's coverage.

| Field | Type | Validation |
|---|---|---|
| Policy Name | Read-only | |
| Currently Covered Branches | Read-only list | |
| Add Branches | Multi-select (branches not already covered) | Optional |
| Remove Branches | Multi-select (currently covered branches) | Optional |
| Effective Date | Date picker | Required |
| Reason | Textarea (max 200 chars) | Required |
| Updated Students Count | Number input | Required |
| Upload Endorsement Letter | File upload (PDF) | Required if insurer has issued endorsement |

**Footer:** `Cancel` · `Update Coverage`

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Policy created | "Insurance policy created successfully." | Success |
| Draft saved | "Policy saved as draft. Upload policy document to activate." | Info |
| Policy activated | "Policy activated. Coverage is now live." | Success |
| Policy updated | "Policy details updated." | Success |
| Policy renewed | "Policy renewed for new period. Previous period archived." | Success |
| Branch coverage updated | "Branch coverage updated. Endorsement filed." | Success |
| Document uploaded | "Policy document uploaded successfully." | Success |
| Export triggered | "Export is being prepared. Download will start shortly." | Info |
| Activation blocked — no document | "Upload the policy document PDF before activating this policy." | Error |
| Save failed — validation | "Please complete all required fields before saving." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No policies in registry | "No insurance policies on record." | "Add the group's first insurance policy to get started." | `+ Add Policy` button |
| No active policies | "No active insurance policies." | "All policies have lapsed or been cancelled. Add or renew a policy immediately to restore student coverage." | `+ Add Policy` button |
| No results for filters | "No policies match your current filters." | "Try adjusting your filters." | `Clear Filters` |
| Claims summary — no claims this period | "No claims recorded for this policy period." | "Claims data will appear here once entered." | — |
| Documents tab — no documents | "No documents uploaded." | "Upload the policy PDF, schedule of benefits, and claim forms." | — |
| Renewal history — first period | "No previous policy periods on record." | "Renewal history will appear here after the first renewal." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: KPI bar (5 grey cards) + policy table (5 grey rows × 12 columns) |
| Filter apply | Table body spinner; KPI bar updates |
| Policy detail drawer open | Drawer skeleton: tab headers + 3 grey content blocks |
| Claims summary tab | Metrics skeleton (6 grey blocks) while loading |
| Renewal history tab | Table skeleton (3 grey rows) |
| Documents tab | File list skeleton (4 grey rows) |
| Policy create/edit save | Submit button spinner; form disabled |
| Renewal modal submit | Spinner + "Processing renewal…" in modal footer |
| Document upload | Progress bar in Documents tab; upload button disabled |

---

## 10. Role-Based UI Visibility

| UI Element | Medical Coordinator | CFO / Finance Director | CEO / Chairman | Emergency Response Officer |
|---|---|---|---|---|
| Full policy list | ✅ | ✅ (view only) | ✅ (view only) | ✅ (view only) |
| Policy Details tab — premium fields | ✅ | ✅ | ✅ | ❌ (hidden) |
| Coverage tab — cashless hospitals | ✅ | ✅ | ✅ | ✅ |
| Coverage limits / exclusions | ✅ | ✅ | ✅ | ✅ (coverage type only) |
| Claims Summary tab | ✅ | ✅ | ✅ | ❌ |
| Renewal History tab | ✅ | ✅ | ✅ | ❌ |
| Documents tab | ✅ | ✅ | ✅ | ✅ (policy document only) |
| + Add Policy button | ✅ | ❌ | ❌ | ❌ |
| Edit action | ✅ | ❌ | ❌ | ❌ |
| Renew action | ✅ | ❌ | ❌ | ❌ |
| Download Policy action | ✅ | ✅ | ✅ | ✅ |
| Branch Coverage Update modal | ✅ | ❌ | ❌ | ❌ |
| Export button | ✅ | ✅ | ❌ | ❌ |
| KPI bar — all cards | ✅ | ✅ | Active policies + students covered only | Active policies + cashless hospitals only |
| Alert banners | ✅ | ✅ (expiry + lapse) | ✅ (lapse only) | ✅ (lapse only) |
| Medical Insurance Coordinator G0 | No platform access | — | — | — |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/insurance-policies/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/insurance-policies/` | List all policies (paginated, filtered) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/insurance-policies/` | Create new policy | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/insurance-policies/{policy_id}/` | Retrieve policy detail (field-masked by role) | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/insurance-policies/{policy_id}/` | Update policy | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/insurance-policies/kpi/` | KPI summary bar data | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/insurance-policies/{policy_id}/renew/` | Mark policy as renewed with new period details | Medical Coordinator |
| PATCH | `/api/v1/group/{group_id}/health/insurance-policies/{policy_id}/branch-coverage/` | Update branch coverage | Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/insurance-policies/{policy_id}/documents/` | Upload document to policy | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/insurance-policies/{policy_id}/documents/{doc_id}/` | Download specific policy document | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/insurance-policies/{policy_id}/claims/` | Claims summary for policy | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/insurance-policies/{policy_id}/claims/` | Add claim record | Medical Coordinator |
| PATCH | `/api/v1/group/{group_id}/health/insurance-policies/{policy_id}/claims/{claim_id}/` | Update claim status | Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/insurance-policies/{policy_id}/renewal-history/` | Past policy periods | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/insurance-policies/export/` | Export policies CSV | Medical Coordinator / CFO |
| GET | `/api/v1/group/{group_id}/health/insurance-policies/alerts/` | Fetch active alert conditions | JWT + role check |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `type` | str[] | Policy type filter |
| `status` | str | `active`, `expiring`, `lapsed`, `renewed` |
| `expiry` | str | `30d`, `60d`, `90d`, `expired` |
| `branch` | int[] | Branch coverage filter |
| `page` | int | Page number |
| `page_size` | int | 25 default, max 50 |
| `search` | str | Policy number or insurer |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search debounce | `hx-get="/api/.../insurance-policies/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#policies-table-body"` | Table rows replaced |
| Filter form apply | `hx-get="/api/.../insurance-policies/"` `hx-trigger="change"` `hx-target="#policies-table-body"` `hx-include="#filter-form"` | Table and KPI bar refreshed |
| Pagination | `hx-get="/api/.../insurance-policies/?page={n}"` `hx-target="#policies-table-body"` `hx-push-url="true"` | Page swap |
| Policy detail drawer open | `hx-get="/api/.../insurance-policies/{policy_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Policy Details tab default |
| Drawer tab switch | `hx-get="/api/.../insurance-policies/{policy_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content swapped; field masking applied server-side per role |
| Claims tab load | `hx-get="/api/.../insurance-policies/{policy_id}/claims/"` `hx-target="#claims-content"` `hx-trigger="click[tab='claims']"` | Claims data loaded on tab click |
| Renewal history tab load | `hx-get="/api/.../insurance-policies/{policy_id}/renewal-history/"` `hx-target="#renewal-history-content"` `hx-trigger="click[tab='renewal_history']"` | Historical periods loaded on tab click |
| Documents tab load | `hx-get="/api/.../insurance-policies/{policy_id}/documents/"` `hx-target="#documents-content"` `hx-trigger="click[tab='documents']"` | Document list loaded |
| Document download | `hx-get="/api/.../insurance-policies/{policy_id}/documents/{doc_id}/"` `hx-target="_blank"` | File served with Content-Disposition: attachment |
| Document upload | `hx-post="/api/.../insurance-policies/{policy_id}/documents/"` `hx-encoding="multipart/form-data"` `hx-target="#documents-list"` | Document list refreshed after upload |
| Policy create form submit | `hx-post="/api/.../insurance-policies/"` `hx-target="#policies-table-body"` `hx-on::after-request="closeDrawer(); fireToast();"` | New row prepended; drawer closed |
| Policy edit form submit | `hx-patch="/api/.../insurance-policies/{policy_id}/"` `hx-target="#policy-row-{policy_id}"` `hx-swap="outerHTML"` | Row updated; drawer closed |
| Renew modal submit | `hx-post="/api/.../insurance-policies/{policy_id}/renew/"` `hx-target="#policy-row-{policy_id}"` `hx-swap="outerHTML"` | Row status updated to Renewed; new active period row prepended; modal closed |
| Branch coverage update modal submit | `hx-patch="/api/.../insurance-policies/{policy_id}/branch-coverage/"` `hx-target="#coverage-branch-list"` | Branch coverage list in drawer refreshed |
| KPI bar refresh | `hx-get="/api/.../insurance-policies/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |
| Alert banner load | `hx-get="/api/.../insurance-policies/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Lapse alert is permanent; non-dismissable until policy renewed |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
