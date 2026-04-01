# 22 — Scholarship Registry

**URL:** `/group/adm/scholarship-registry/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions · Scholarship Section

---

## 1. Purpose

The Scholarship Registry is the authoritative master record of every scholarship scheme offered or tracked by the group. It serves two distinct categories: first, group-defined schemes that the group itself funds and administers — merit scholarships, need-based grants, sports excellence awards, and special category incentives; and second, government-mandated or government-sponsored schemes (NSP, PMSS, state scholarship programs) where the group facilitates student enrolment, submits applications to the government portal, and claims reimbursements. Both categories are maintained in this registry as the single source of truth.

For each scheme, the registry captures the full scheme profile: eligibility criteria (marks threshold, income limit, category), award structure (percentage tuition waiver, fixed annual amount, or recurring term grant), duration (one-time or renewable over the entire course), maximum beneficiary cap per cycle, and renewal conditions. When the Scholarship Manager creates a new scheme, it goes through a Director approval step before becoming active. Pausing or discontinuing a scheme also requires Director-level confirmation to prevent accidental disruption of ongoing beneficiaries.

The Scheme Renewal Calendar is operationally critical — it ensures the Scholarship Manager never misses a renewal window where beneficiaries need to reapply or have their eligibility re-verified. Government scheme enrollment tracking ensures that the group's compliance with mandatory programs (like RTE and PMSS) is visible at the group level, and that reimbursement claims are submitted and followed up with state/central authorities. Finance teams use the disbursement data in this registry as input for the fee adjustment module.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Manager (27) | G3 | Full CRUD — create, edit, pause, discontinue schemes | Primary owner |
| Group Admissions Director (23) | G3 | View all + approve new schemes + approve pause/discontinue | Cannot create directly |
| Chief Financial Officer | G1 | View only — especially disbursement figures | Read-only, finance context |
| Group Scholarship Exam Manager (26) | G3 | View eligibility criteria only | Read-only, linked to exam design |
| Group Admission Coordinator (24) | G3 | No access | Excluded |
| Group Admission Counsellor (25) | G3 | No access | Not this page's scope |

**Enforcement:** `@role_required(['scholarship_manager', 'admissions_director', 'cfo', 'scholarship_exam_manager'])` at the Django view level. CFO and Scholarship Exam Manager see a read-only template variant (`scheme_readonly=True` in context). Create/edit/status-change API endpoints require JWT with `role == scholarship_manager`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarships → Scholarship Registry
```

### 3.2 Page Header
- **Title:** Scholarship Registry
- **Subtitle:** Master record of all scholarship schemes — group-defined and government
- **Action Buttons:** `[+ Add Scheme]` (Scholarship Manager only) · `[Bulk Update Amounts]` (Scholarship Manager only) · `[Export Registry PDF]`
- **Summary Chip:** "X active schemes · ₹Y total annual commitment"

### 3.3 Alert Banner
Triggers:
- **Amber — Scheme Renewal Due:** "3 scholarship schemes have renewals due in the next 30 days. [View Renewal Calendar →]"
- **Red — Beneficiary Expiry:** "{n} students have expired scholarships with no renewal action. [View →]"
- **Amber — Government Scheme Disbursement Pending:** "PMSS disbursement for AY 2025-26 not yet received. {n} students affected. [Track →]"
- **Blue — Approval Pending:** "2 new scheme proposals are awaiting Director approval."
- **Green — Scheme Approved:** "'{Scheme Name}' approved by Director and is now Active."

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Active Scholarship Schemes | COUNT of schemes with status = 'active' | `scholarship_scheme` table | Blue always | → Section 5.1 filtered to active |
| Total Beneficiaries (Current Year) | COUNT of active `scholarship_beneficiary` records in current AY | `scholarship_beneficiary` | Blue always | → beneficiary list |
| Total Annual Scholarship Value (₹) | SUM of award amounts for all active beneficiaries in current AY | `scholarship_beneficiary` aggregation | Blue always | → budget summary |
| Government Schemes Tracked | COUNT of schemes with type in ('govt_state', 'govt_central') | `scholarship_scheme` filter | Blue always | → Section 5.4 |
| Schemes Up for Renewal This Term | COUNT of schemes with next_renewal_date within 60 days | `scholarship_scheme` aggregation | Amber > 0 · Green = 0 | → Section 5.3 |
| Students with Expired Scholarships | COUNT of beneficiaries where renewal_due_date < today and status = 'active' | `scholarship_beneficiary` | Red > 0 · Green = 0 | → expired renewals list |

**HTMX Refresh:** Every 5 minutes via `hx-trigger="every 5m"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Scholarship Scheme Directory

**Display:** Sortable, selectable (checkbox), server-side paginated (20/page). Default sort: status (active first), then scheme_name ASC.

**Columns:**

| Column | Notes |
|---|---|
| Scheme Name | Linked — click opens scheme-create-edit drawer in view mode |
| Type | Merit (blue) / Need-based (purple) / RTE (orange) / Govt-State (teal) / Govt-Central (green) / Group-Special (grey) — badges |
| Eligibility Criteria | Truncated summary (100 chars) — hover for full text |
| Award Amount / % Waiver | Formatted: ₹X,XXX or XX% |
| Duration | One-time / Annual / Full Course |
| Max Beneficiaries | Numeric (or "Unlimited") |
| Current Beneficiaries | Count — linked to scheme-beneficiaries-list drawer |
| Renewal Frequency | Annual / Per-term / None |
| Status | Active (green) / Paused (amber) / Pending Approval (blue) / Discontinued (red) |
| Actions | `[Edit →]` · `[View Beneficiaries →]` · `[Pause]` / `[Activate]` toggle (Manager only) |

**Filters:** Type (multi-select), Status (multi-select)

**Actions (top):** `[+ Add Scheme]` · `[Bulk Update Amounts]`

**HTMX Pattern:** Filter changes → `GET /api/v1/group/{group_id}/adm/scholarship-registry/schemes/?{filters}` targeting `#scheme-table-body`.

**Empty State:** No schemes defined. Icon: gift. Heading: "No Scholarship Schemes". CTA: `[+ Add First Scheme]`.

---

### 5.2 Beneficiary Count by Scheme

**Display:** Horizontal bar chart (Chart.js 4.x) — one bar per active scheme. X-axis: count of current beneficiaries. Y-axis: scheme names.

**Colour:** Bars coloured by scheme type (matching badge colours in Section 5.1).

**Tooltip:** Scheme name, current beneficiaries, max beneficiaries, utilisation %.

**Interaction:** Click a bar → opens scheme-beneficiaries-list drawer for that scheme.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-registry/stats/beneficiary-distribution/`.

---

### 5.3 Scheme Renewal Calendar

**Display:** List — schemes with renewal due within 60 days. Sorted by renewal deadline ASC.

**Columns:** Scheme Name · Type · Current Beneficiaries · Renewal Deadline · Days Until Renewal (countdown chip — red < 14 days, amber 15–30, green > 30) · `[Send Renewal Notices →]`

**`[Send Renewal Notices →]`:** Triggers bulk WhatsApp/email notification to all beneficiaries of that scheme prompting them to reapply or submit renewal documents.

**HTMX Pattern:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-registry/renewals/upcoming/` targeting `#renewal-calendar`.

**Empty State:** No renewals due in the next 60 days. Icon: calendar-check. Heading: "No Renewals Due Soon."

---

### 5.4 Government Scheme Enrollment Tracker

**Display:** Table — one row per government scheme.

**Columns:**

| Column | Notes |
|---|---|
| Scheme | Scheme name (NSP, PMSS, State Scholarship, etc.) |
| Students Enrolled | COUNT enrolled from this group |
| Application Submitted to Govt | Yes/No + date |
| Disbursed by Govt | Amount received (₹) |
| Claimed by School | Amount claimed (₹) |
| Transferred to Students | Amount passed to students (₹) |
| Pending | (Claimable – Received) in ₹ — red if > 0 |
| Actions | `[View Details →]` (opens govt-scheme-detail drawer) |

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-registry/govt-schemes/tracker/`.

**Empty State:** No government schemes configured. CTA: `[+ Add Govt Scheme]`.

---

### 5.5 Scheme Performance Summary

**Display:** Table — per scheme, historical performance metrics.

**Columns:**

| Column | Notes |
|---|---|
| Scheme Name | Linked |
| Total Awarded Since Inception | Cumulative beneficiary count |
| Renewal Rate % | (Renewed beneficiaries / eligible for renewal) × 100 |
| Dropout Rate % | (Discontinued mid-term / total awarded) × 100 |
| Avg Score of Beneficiaries | For merit schemes: avg exam score of all beneficiaries |
| Total Disbursed (₹) | Cumulative disbursement |

**Sort:** Renewal Rate % DESC default.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-registry/stats/scheme-performance/`.

---

## 6. Drawers & Modals

### 6.1 Scheme Create / Edit Drawer
- **Width:** 640px
- **Trigger:** `[+ Add Scheme]` (new) or `[Edit →]` on row
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-registry/schemes/{scheme_id}/form/` (scheme_id = `new` for create)
- **Tabs:**
  1. **Basic Details** — Scheme name, type (dropdown), description, academic year applicability
  2. **Eligibility** — Criteria type (marks/income/category/combination), threshold values, applicable classes/streams
  3. **Award Structure** — Award type (percentage waiver / fixed amount / hybrid), amount/percentage, applicable fee heads
  4. **Renewal Terms** — Duration, renewal frequency, renewal criteria, max renewal cycles
  5. **Linked Exams** — Link to scholarship entrance exams that feed recommendations into this scheme
  6. **Active / Pause** — Status toggle with justification field; note: status change requires Director approval
- **Submit:** `hx-post` / `hx-put` → `/api/v1/group/{group_id}/adm/scholarship-registry/schemes/` · triggers approval workflow for new schemes

### 6.2 Scheme Beneficiaries List Drawer
- **Width:** 560px
- **Trigger:** `[View Beneficiaries →]` on table row or bar chart click
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-registry/schemes/{scheme_id}/beneficiaries/`
- **Content:** Paginated list of current beneficiaries — Student name, Branch, Class, Award amount, Start date, Renewal due date, Status (Active / Renewal Due / Expired)
- **Filter:** Branch, Status
- **Export:** `[Export CSV]` from drawer

### 6.3 Government Scheme Detail Drawer
- **Width:** 480px
- **Trigger:** `[View Details →]` in Section 5.4
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-registry/govt-schemes/{scheme_id}/detail/`
- **Content:** Scheme name, government portal reference, students enrolled list, application submission history (dates, reference numbers), disbursement history from govt, claim records, pending amounts, contact details of nodal officer.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Scheme created (pending approval) | "'{Scheme Name}' created. Awaiting Director approval before activation." | Info | 5 s |
| Scheme approved | "'{Scheme Name}' approved and is now Active." | Success | 4 s |
| Scheme updated | "'{Scheme Name}' updated." | Success | 3 s |
| Scheme paused | "'{Scheme Name}' paused. Existing beneficiaries are not affected until renewal." | Warning | 5 s |
| Scheme discontinued | "'{Scheme Name}' discontinued." | Warning | 5 s |
| Bulk amounts updated | "{n} scheme amounts updated." | Success | 4 s |
| Renewal notices sent | "Renewal notices sent to {n} beneficiaries for '{Scheme Name}'." | Success | 4 s |
| Govt scheme updated | "Government scheme record updated." | Success | 3 s |
| Export queued | "Registry export PDF is being prepared." | Info | 3 s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No schemes defined | Gift icon | "No Scholarship Schemes" | "Add the first scholarship scheme to begin tracking awards." | `[+ Add Scheme]` |
| No active schemes | Pause icon | "No Active Schemes" | "All schemes are paused or discontinued." | `[View All Schemes]` |
| No renewals due | Calendar-check icon | "No Renewals Due" | "No scholarship schemes have renewals due in the next 60 days." | None |
| No government schemes | Government-building icon | "No Government Schemes Configured" | "Add a government scheme to start tracking NSP, PMSS, or state scholarship enrollments." | `[+ Add Govt Scheme]` |
| Filter returns no schemes | Search icon | "No Schemes Match Filters" | "Adjust type or status filters." | `[Clear Filters]` |
| Scheme Performance Summary (5.5) is empty | Chart outline icon | "No Performance Data Available" | "Scheme performance data requires at least one completed cycle with disbursements. Data will appear automatically after the first disbursement." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | KPI shimmer (6 cards) + scheme table skeleton (5 rows) |
| KPI auto-refresh | In-place spinner per card |
| Scheme table filter change | Table body skeleton (5 row shimmer) |
| Beneficiary chart load | Chart.js horizontal bar loading animation |
| Renewal calendar load | List skeleton (3 item shimmers) |
| Govt scheme tracker load | Table skeleton (4 row shimmer) |
| Scheme performance table load | Table skeleton (5 row shimmer) |
| Scheme create/edit drawer open | 640px drawer with 6 tab-label shimmers + form shimmer |
| Beneficiaries drawer open | 560px drawer list skeleton (10 row shimmer) |
| Govt detail drawer open | 480px drawer content shimmer |
| Renewal notices dispatch | Button spinner + "Sending…" text |
| Bulk amount update | Button spinner + "Processing…" text |

---

## 10. Role-Based UI Visibility

| Element | Scholarship Mgr (27) | Director (23) | CFO | Exam Mgr (26) | Coordinator (24) |
|---|---|---|---|---|---|
| `[+ Add Scheme]` button | Visible | Hidden | Hidden | Hidden | No access |
| `[Edit →]` on scheme | Visible | Hidden | Hidden | Hidden | No access |
| `[Pause]` / `[Activate]` toggle | Visible | Hidden | Hidden | Hidden | No access |
| `[Bulk Update Amounts]` | Visible | Hidden | Hidden | Hidden | No access |
| `[Approve]` scheme action | Hidden | Visible | Hidden | Hidden | No access |
| Section 5.1 scheme directory | Visible (full) | Visible (full) | Visible (read) | Visible (eligibility only) | No access |
| Section 5.2 beneficiary chart | Visible | Visible | Visible | Hidden | No access |
| Section 5.3 renewal calendar | Visible (full) | Visible | Hidden | Hidden | No access |
| `[Send Renewal Notices →]` | Visible | Hidden | Hidden | Hidden | No access |
| Section 5.4 govt tracker | Visible | Visible | Visible (full) | Hidden | No access |
| Section 5.5 scheme performance | Visible | Visible | Visible | Hidden | No access |
| `[Export Registry PDF]` | Visible | Visible | Visible | Hidden | No access |
| Disbursement figures | Visible | Visible | Visible | Hidden | No access |

*All UI visibility decisions made server-side in Django template. No client-side JS role checks.*

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarship-registry/kpis/` | JWT G3 | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-registry/schemes/` | JWT G3 | Paginated, filtered scheme list |
| POST | `/api/v1/group/{group_id}/adm/scholarship-registry/schemes/` | JWT G3 write | Create scheme |
| GET | `/api/v1/group/{group_id}/adm/scholarship-registry/schemes/{scheme_id}/form/` | JWT G3 | Scheme form drawer fragment |
| PUT | `/api/v1/group/{group_id}/adm/scholarship-registry/schemes/{scheme_id}/` | JWT G3 write | Update scheme |
| POST | `/api/v1/group/{group_id}/adm/scholarship-registry/schemes/{scheme_id}/approve/` | JWT G3 Director | Director approval |
| POST | `/api/v1/group/{group_id}/adm/scholarship-registry/schemes/{scheme_id}/pause/` | JWT G3 write | Pause scheme |
| POST | `/api/v1/group/{group_id}/adm/scholarship-registry/schemes/{scheme_id}/activate/` | JWT G3 write | Activate scheme |
| POST | `/api/v1/group/{group_id}/adm/scholarship-registry/schemes/bulk-update-amounts/` | JWT G3 write | Bulk update award amounts |
| GET | `/api/v1/group/{group_id}/adm/scholarship-registry/schemes/{scheme_id}/beneficiaries/` | JWT G3 | Beneficiaries drawer fragment |
| GET | `/api/v1/group/{group_id}/adm/scholarship-registry/stats/beneficiary-distribution/` | JWT G3 | Beneficiary chart data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-registry/renewals/upcoming/` | JWT G3 | Renewals due within 60 days |
| POST | `/api/v1/group/{group_id}/adm/scholarship-registry/schemes/{scheme_id}/send-renewal-notices/` | JWT G3 write | Send renewal notifications |
| GET | `/api/v1/group/{group_id}/adm/scholarship-registry/govt-schemes/tracker/` | JWT G3 | Govt scheme tracker table |
| POST | `/api/v1/group/{group_id}/adm/scholarship-registry/govt-schemes/` | JWT G3 | Create a new government scheme tracking record |
| GET | `/api/v1/group/{group_id}/adm/scholarship-registry/govt-schemes/{scheme_id}/detail/` | JWT G3 | Govt scheme detail drawer |
| PUT | `/api/v1/group/{group_id}/adm/scholarship-registry/govt-schemes/{scheme_id}/` | JWT G3 write | Update govt scheme record |
| GET | `/api/v1/group/{group_id}/adm/scholarship-registry/stats/scheme-performance/` | JWT G3 | Scheme performance summary |
| GET | `/api/v1/group/{group_id}/adm/scholarship-registry/export/pdf/` | JWT G3 | Export registry PDF |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `.../scholarship-registry/kpis/` | `#kpi-bar` | `innerHTML` |
| Filter scheme table | `change` on filter inputs | GET `.../scholarship-registry/schemes/?{filters}` | `#scheme-table-body` | `innerHTML` |
| Paginate scheme table | `click` on page link | GET `.../scholarship-registry/schemes/?page={n}` | `#scheme-table-container` | `innerHTML` |
| Open scheme create drawer | `click` on `[+ Add Scheme]` | GET `.../scholarship-registry/schemes/new/form/` | `#drawer-container` | `innerHTML` |
| Open scheme edit drawer | `click` on `[Edit →]` | GET `.../scholarship-registry/schemes/{id}/form/` | `#drawer-container` | `innerHTML` |
| Submit scheme form (create) | `submit` on scheme form | POST `.../scholarship-registry/schemes/` | `#scheme-table-body` | `innerHTML` |
| Submit scheme form (edit) | `submit` on scheme form | PUT `.../scholarship-registry/schemes/{id}/` | `#scheme-row-{id}` | `outerHTML` |
| Pause scheme | `click` on `[Pause]` | POST `.../scholarship-registry/schemes/{id}/pause/` | `#scheme-row-{id}` | `outerHTML` |
| Activate scheme | `click` on `[Activate]` | POST `.../scholarship-registry/schemes/{id}/activate/` | `#scheme-row-{id}` | `outerHTML` |
| Approve scheme (Director) | `click` on `[Approve]` | POST `.../scholarship-registry/schemes/{id}/approve/` | `#scheme-row-{id}` | `outerHTML` |
| Open beneficiaries drawer | `click` on `[View Beneficiaries →]` or bar chart | GET `.../scholarship-registry/schemes/{id}/beneficiaries/` | `#drawer-container` | `innerHTML` |
| Load beneficiary chart | `load` on chart section | GET `.../scholarship-registry/stats/beneficiary-distribution/` | `#beneficiary-chart-data` | `innerHTML` |
| Load renewal calendar | `load` on section | GET `.../scholarship-registry/renewals/upcoming/` | `#renewal-calendar` | `innerHTML` |
| Send renewal notices | `click` on `[Send Renewal Notices →]` | POST `.../scholarship-registry/schemes/{id}/send-renewal-notices/` | `#renewal-row-{id}` | `outerHTML` |
| Load govt scheme tracker | `load` on section | GET `.../scholarship-registry/govt-schemes/tracker/` | `#govt-tracker-table` | `innerHTML` |
| Open govt scheme detail drawer | `click` on `[View Details →]` | GET `.../scholarship-registry/govt-schemes/{id}/detail/` | `#drawer-container` | `innerHTML` |
| Load scheme performance | `load` on section | GET `.../scholarship-registry/stats/scheme-performance/` | `#performance-table` | `innerHTML` |
| Bulk update scheme amounts | `click from:#btn-bulk-update-amounts` | POST `.../scholarship-registry/bulk-update-amounts/` | `#scheme-directory-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
