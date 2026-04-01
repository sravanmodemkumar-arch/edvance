# 12 — Counsellor Registry

> **URL:** `/group/health/counsellors/`
> **File:** `12-counsellor-registry.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Mental Health Coordinator (primary) · Group Medical Coordinator (view)

---

## 1. Purpose

Centralised registry of all mental health counsellors and psychologists assigned across branches in the group. Tracks professional qualifications (RCI registration, NIMHANS training, CBT/REBT certifications), branch assignments, working schedule, specialisation area (adolescent counselling, trauma, academic stress, career guidance), caseload capacity, and active caseload.

The Mental Health Coordinator uses this registry to ensure adequate counselling coverage — particularly for branches with hostelers (higher wellbeing risk due to separation from family), ensure all RCI registrations are current and renewed before expiry, monitor caseload equity (no counsellor overwhelmed while others are underutilised), and coordinate reassignments during leaves or departures. Counsellors are first responders in mental health crises — their availability and qualification status is operationally critical.

Scale: 1–3 counsellors per large branch × 20–50 branches = 20–150 counsellors. Some counsellors may serve multiple small branches on a split-time basis.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Mental Health Coordinator | G3 | Full CRUD — create, edit, reassign, flag inactive | Primary owner |
| Group Medical Coordinator | G3 | View only | For cross-health team oversight |
| HR Director | Group | View only — for employment records | No counselling operational fields visible |
| Group Emergency Response Officer | G3 | View contact details only — name, phone, branch | No qualification or caseload data |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('mental_health_coordinator', 'medical_coordinator', 'hr_director', 'emergency_response_officer')` with field-level masks at the serialiser layer per role.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Counsellor Registry
```

### 3.2 Page Header
- **Title:** `Counsellor Registry`
- **Subtitle:** `[N] Total Counsellors · [N] Active · [N] Branches With Counsellor · [N] Without`
- **Right controls:** `+ Add Counsellor` (Mental Health Coordinator only) · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with no counsellor for > 30 days | "[N] branches have had no assigned counsellor for more than 30 days." | Red |
| RCI registration expired | "[N] counsellors have expired RCI registrations. They must not practice until renewed." | Red |
| Counsellor over maximum caseload | "[N] counsellors are currently over their maximum caseload capacity." | Amber |
| Hostel branch with no counsellor assigned | "[N] hostel branches have no counsellor assigned. High priority coverage required." | Red |
| RCI registration expiring within 60 days | "[N] counsellors have RCI registrations expiring within 60 days. Initiate renewal." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Counsellors | All active + on-leave counsellors in registry | Blue always |
| Branches with Counsellor | Branches with at least one active counsellor assigned | Green = 100% · Yellow < 90% · Red < 80% |
| Branches Without Counsellor | Branches with no active counsellor assigned | Green = 0 · Red > 0 |
| RCI Registrations Expiring (60 days) | Counsellors with RCI expiry date ≤ today + 60 days | Green = 0 · Yellow 1–3 · Red > 3 |
| Average Caseload per Counsellor | Total active cases / Total active counsellors | Green ≤ 15 · Yellow 16–20 · Red > 20 |

---

## 5. Main Table — Counsellor Registry

**Search:** Counsellor name, RCI registration number, branch name. 300ms debounce, minimum 2 characters.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Specialisation | Checkbox | Adolescent / Trauma / Academic Stress / Career Counselling / Behavioural / Family / Other |
| Status | Radio | All / Active / On Leave / Resigned |
| RCI Expiry | Radio | All / Expiring in 30 days / Expiring in 60 days / Expiring in 90 days / Already Expired |
| BGV Status | Radio | All / Verified / Pending / Failed |
| Employment Type | Checkbox | Full-time / Part-time / Visiting |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Name | ✅ | Link → `counsellor-detail` drawer |
| Qualification | ✅ | Highest degree (e.g., M.Phil Clinical Psychology) |
| RCI Reg No | ✅ | Registration number |
| Reg Expiry | ✅ | Date; red if expired, amber if within 60 days |
| Branch(es) Assigned | ✅ | Branch name(s); tooltip for multiple |
| Specialisation | ✅ | Primary specialisation badge |
| Working Hours | ❌ | e.g., Mon–Fri 9am–4pm |
| Caseload (current / max) | ✅ | e.g., 12 / 20; red badge if current > max |
| Status | ✅ | Active (green) / On Leave (amber) / Resigned (red) |
| BGV | ✅ | Verified (green) / Pending (grey) / Failed (red) |
| Actions | ❌ | View · Edit · Reassign |

**Default sort:** Status (Active first), then RCI Expiry ascending (earliest expiry first).
**Pagination:** Server-side · 25/page.
**Bulk actions:** Export (Mental Health Coordinator only).

---

## 6. Drawers / Modals

### 6.1 Drawer — `counsellor-detail` (680px, right side)

Triggered by counsellor name link or **View** action.

**Tabs:**

#### Tab 1 — Profile
| Field | Notes |
|---|---|
| Full Name | |
| Gender | |
| Date of Birth | Age calculated |
| Contact Phone | |
| Contact Email | |
| Emergency Contact | Name + phone |
| Employment Type | Full-time / Part-time / Visiting |
| Employed Since | Start date |
| Employment Status | Active / On Leave / Resigned |
| BGV Status | Verified / Pending / Failed + BGV document link |
| Reporting To | Mental Health Coordinator name |
| Notes | Internal notes field |

#### Tab 2 — Qualifications
| Field | Notes |
|---|---|
| Primary Degree | MSc Psychology / MA Psychology / M.Phil Clinical Psychology / PhD Psychology — dropdown on edit |
| University | |
| Year of Completion | |
| RCI Registration Number | Rehabilitation Council of India |
| RCI Registration Expiry | Date; alert badge if within 60 days or expired |
| RCI Certificate Upload | View PDF link; Upload button |
| Additional Certifications | List: Certification name · Issuing body · Year · Certificate upload |

**Certification list examples:** CBT (Cognitive Behavioural Therapy) · REBT · Trauma-Focused Therapy · Career Counselling · Adolescent Mental Health · Suicide Prevention (ASIST) · NIMHANS Training.

#### Tab 3 — Assignments
| Field | Notes |
|---|---|
| Assigned Branches | List of branches with effective date |
| Working Days | Mon / Tue / Wed / Thu / Fri / Sat checkboxes per branch |
| Working Hours | Start time – End time per branch |
| Counselling Room Number | Room/location at each assigned branch |
| Travel Arrangement | If visiting multiple branches: travel mode / schedule notes |

#### Tab 4 — Caseload
| Metric | Notes |
|---|---|
| Current Active Cases | Count; red badge if over max |
| Maximum Caseload Capacity | Set by coordinator |
| Caseload Utilisation % | Current / Max × 100 |
| Referral Sources Breakdown | Bar chart: Self-referred / Teacher-referred / Parent-referred / Principal-referred / Medical-referred |
| Cases by Risk Level | Count per level: Low / Medium / High / Crisis |
| Cases by Concern Category | Count per category |

#### Tab 5 — Sessions History
Last 30 sessions (anonymised — student ID only, date, session type, outcome code). Mental Health Coordinator sees student names; others see anonymised IDs only.

| Column | Notes |
|---|---|
| Session Date | |
| Student ID (anonymised) | Student name visible to Mental Health Coordinator only |
| Session Type | Individual / Group / Crisis |
| Concern Category | |
| Duration (mins) | |
| Risk Level | |
| Outcome Code | Resolved / Ongoing / Referred / Escalated |

---

### 6.2 Drawer — `counsellor-create` (640px, right side)

Triggered by **+ Add Counsellor** (Mental Health Coordinator only).

| Field | Type | Validation |
|---|---|---|
| Full Name | Text input | Required |
| Gender | Radio — Male / Female / Other / Prefer not to say | Required |
| Date of Birth | Date picker | Required |
| Contact Phone | Phone input | Required |
| Contact Email | Email input | Required |
| Emergency Contact Name | Text input | Required |
| Emergency Contact Phone | Phone input | Required |
| Employment Type | Radio — Full-time / Part-time / Visiting | Required |
| Start Date | Date picker | Required |
| Primary Degree | Single-select | Required |
| University | Text input | Required |
| Year of Completion | Year picker | Required |
| RCI Registration Number | Text input | Required |
| RCI Registration Expiry | Date picker | Required |
| RCI Certificate | File upload (PDF, max 5 MB) | Required |
| Additional Certifications | Repeating: Name · Issuing body · Year · File upload | Optional; add row button |
| Assign Branches | Multi-select | Required; at least one |
| Working Days (per branch) | Checkbox grid per assigned branch | Required |
| Working Hours (per branch) | Time range per assigned branch | Required |
| Counselling Room Number | Text input per assigned branch | Optional |
| Maximum Caseload Capacity | Number input | Required; range 1–40 |
| Specialisation | Multi-select: Adolescent / Trauma / Academic Stress / Career / Behavioural / Family / Other | Required; at least one |
| BGV Status | Radio — Verified / Pending | Required |
| BGV Document | File upload | Required if Verified |

**Footer:** `Cancel` · `Save Counsellor`

---

### 6.3 Drawer — `counsellor-edit` (640px, right side)

Pre-populated with existing data. All fields editable except: name and date of birth (HR system records — locked). Same layout as create drawer.

---

### 6.4 Modal — `reassign-counsellor` (460px, centred)

Triggered by **Reassign** action in Actions column.

| Field | Type | Validation |
|---|---|---|
| Counsellor Name | Read-only | |
| From Branch | Single-select (current branches) | Required |
| To Branch | Single-select (all branches) | Required; different from From |
| Effective Date | Date picker | Required |
| Reason for Reassignment | Textarea (max 300 chars) | Required |
| Working Schedule at New Branch | Days + hours | Required |
| Notify Affected Students | Toggle — Yes / No | Required |
| Notification Message | Textarea (max 200 chars, visible if notify = Yes) | Conditional required |

**Footer:** `Cancel` · `Confirm Reassignment`

Triggers: branch assignment updated in counsellor record; notification sent to affected students (if yes); audit log entry.

---

### 6.5 Modal — `flag-inactive` (420px, centred)

Triggered by **Flag Inactive** option in Edit menu or action menu.

| Field | Type | Validation |
|---|---|---|
| Counsellor Name | Read-only | |
| Reason | Radio — On Leave / Resigned / Contract Ended / Suspended | Required |
| Effective Date | Date picker | Required |
| Expected Return Date | Date picker | Visible if reason = On Leave |
| Replacement Arranged | Radio — Yes / No / In Progress | Required |
| Replacement Name | Single-select (from counsellor registry) | Required if Yes |
| Notes | Textarea (max 300 chars) | Optional |

**Footer:** `Cancel` · `Mark Inactive`

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Counsellor added | "Counsellor added to registry successfully." | Success |
| Counsellor updated | "Counsellor record updated." | Success |
| Reassignment confirmed | "Counsellor reassigned from [Branch A] to [Branch B] effective [Date]." | Success |
| Marked inactive | "Counsellor marked as [status] effective [Date]." | Success |
| RCI certificate uploaded | "RCI certificate uploaded and linked to record." | Success |
| Export triggered | "Export is being prepared. Download will start shortly." | Info |
| Notification sent to students | "[N] affected students notified of counsellor reassignment." | Info |
| Save failed | "Please complete all required fields before saving." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No counsellors in registry | "No counsellors registered yet." | "Add the first counsellor to get started." | `+ Add Counsellor` button |
| No results for current filters | "No counsellors match your current filters." | "Try adjusting filters." | `Clear Filters` |
| No assignments for counsellor | "No branch assignments recorded." | "Add a branch assignment in the Assignments tab." | — |
| No additional certifications | "No additional certifications on record." | — | — |
| No session history | "No session history available." | "Sessions will appear here once recorded." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: KPI bar (5 grey cards) + table (8 grey rows × 11 columns) |
| Filter / search apply | Table body spinner overlay; KPI bar refreshes |
| Counsellor detail drawer open | Drawer skeleton: tab headers + 3 content blocks per tab |
| Sessions history tab | Skeleton table (10 grey rows) while data loads |
| Caseload tab | Chart skeletons (2 grey bars) + metrics skeleton |
| Export preparation | Button spinner + "Preparing export…" |
| Reassignment confirmation | Modal footer spinner while saving |

---

## 10. Role-Based UI Visibility

| UI Element | Mental Health Coordinator | Medical Coordinator | HR Director | Emergency Response Officer |
|---|---|---|---|---|
| Full record — all tabs | ✅ | ✅ (view only) | Profile tab only | Contact details only |
| Qualifications tab | ✅ | ✅ (view only) | ✅ (view only) | ❌ |
| Assignments tab | ✅ | ✅ (view only) | ❌ | ✅ (branch + room only) |
| Caseload tab | ✅ | ✅ (view only) | ❌ | ❌ |
| Sessions History tab | ✅ (sees student names) | ❌ | ❌ | ❌ |
| + Add Counsellor button | ✅ | ❌ | ❌ | ❌ |
| Edit button | ✅ | ❌ | ❌ | ❌ |
| Reassign button | ✅ | ❌ | ❌ | ❌ |
| Flag Inactive button | ✅ | ❌ | ❌ | ❌ |
| Export button | ✅ | ❌ | ❌ | ❌ |
| RCI certificate upload | ✅ | ❌ | ❌ | ❌ |
| KPI bar | ✅ Full | ✅ Full (view) | ❌ | Branches without counsellor only |
| Alert banners | ✅ | ✅ | ❌ | ❌ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/counsellors/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/counsellors/` | List all counsellors (paginated, filtered) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/counsellors/` | Create counsellor record | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/counsellors/{counsellor_id}/` | Retrieve counsellor detail | JWT + field mask per role |
| PATCH | `/api/v1/group/{group_id}/health/counsellors/{counsellor_id}/` | Update counsellor record | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/counsellors/kpi/` | KPI summary bar data | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/counsellors/{counsellor_id}/reassign/` | Reassign to different branch | Mental Health Coordinator |
| POST | `/api/v1/group/{group_id}/health/counsellors/{counsellor_id}/flag-inactive/` | Mark counsellor inactive | Mental Health Coordinator |
| POST | `/api/v1/group/{group_id}/health/counsellors/{counsellor_id}/rci-certificate/` | Upload RCI certificate | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/counsellors/{counsellor_id}/sessions/` | Session history for counsellor (anonymised) | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/counsellors/export/` | Export counsellor registry CSV | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/counsellors/alerts/` | Fetch active alert conditions | JWT + role check |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Filter by branch ID(s) |
| `specialisation` | str[] | Filter by specialisation |
| `status` | str | `active`, `on_leave`, `resigned` |
| `rci_expiry` | str | `30d`, `60d`, `90d`, `expired` |
| `bgv_status` | str | `verified`, `pending`, `failed` |
| `employment_type` | str[] | `full_time`, `part_time`, `visiting` |
| `page` | int | Page number |
| `page_size` | int | 25 default |
| `search` | str | Name, RCI number, or branch |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search debounce | `hx-get="/api/.../counsellors/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#counsellors-table-body"` | Table rows replaced |
| Filter form apply | `hx-get="/api/.../counsellors/"` `hx-trigger="change"` `hx-target="#counsellors-table-body"` `hx-include="#filter-form"` | Table and KPI bar refresh |
| Pagination | `hx-get="/api/.../counsellors/?page={n}"` `hx-target="#counsellors-table-body"` `hx-push-url="true"` | Page swap |
| Counsellor detail drawer open | `hx-get="/api/.../counsellors/{counsellor_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Profile tab default |
| Drawer tab switch | `hx-get="/api/.../counsellors/{counsellor_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content swapped |
| Sessions history tab load | `hx-get="/api/.../counsellors/{counsellor_id}/sessions/"` `hx-target="#sessions-content"` `hx-trigger="click[tab='sessions']"` | Sessions table loaded on tab click |
| Create/edit form submit | `hx-post="/api/.../counsellors/"` (create) or `hx-patch="/api/.../counsellors/{id}/"` (edit) `hx-target="#counsellors-table-body"` | Table refreshed; drawer closed; toast fired |
| Reassign modal submit | `hx-post="/api/.../counsellors/{id}/reassign/"` `hx-target="#counsellor-row-{id}"` `hx-swap="outerHTML"` | Row updated with new branch assignment; modal closed |
| Flag inactive modal submit | `hx-post="/api/.../counsellors/{id}/flag-inactive/"` `hx-target="#counsellor-row-{id}"` `hx-swap="outerHTML"` | Row status badge updated; modal closed |
| RCI certificate upload | `hx-post="/api/.../counsellors/{id}/rci-certificate/"` `hx-encoding="multipart/form-data"` `hx-target="#rci-status-{id}"` | RCI expiry badge updated in row |
| KPI bar refresh | `hx-get="/api/.../counsellors/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |
| Alert banner load | `hx-get="/api/.../counsellors/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Conditional display |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
