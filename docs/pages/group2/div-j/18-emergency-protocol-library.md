# 18 — Emergency Protocol Library

> **URL:** `/group/health/emergency-protocols/`
> **File:** `18-emergency-protocol-library.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Emergency Response Officer (primary) · Group Medical Coordinator (co-owner for medical SOPs)

---

## 1. Purpose

Centralised, versioned library of all emergency Standard Operating Procedures (SOPs) for the group. Every branch must have access to applicable SOPs for the following categories: Medical Emergency (cardiac arrest, seizure, anaphylaxis, severe injury, diabetic emergency), Fire Evacuation, Natural Disaster (earthquake, flood, cyclone), Road Accident (transport-related incidents, on-campus vehicle accidents), Missing Student Protocol, and Campus Security Breach.

SOPs are versioned: each edit creates a new version and archives the previous one. SOPs are distributed to applicable branches through the portal, and branch Principals must acknowledge receipt. Branch staff access their own branch's SOPs in read-only mode via the branch portal. Drills conducted under each SOP are tracked and linked here.

Annual review is mandatory for all active SOPs. Overdue reviews are flagged to the Emergency Response Officer and Medical Coordinator. The SOP library serves as the single source of truth for emergency preparedness compliance, referenced by the compliance report (Page 24) and the drill scheduler (Page 19).

Scale: 10–20 SOP types, each with an average of 2 versions on file; total library of 20–40 SOP records.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Emergency Response Officer | G3 | Full CRUD — create, edit, version, distribute, archive all SOPs | Primary owner |
| Group Medical Coordinator | G3 | Create and edit Medical Emergency SOPs; view all SOPs | Co-owner for medical category |
| Branch Principal | Branch | Read-only — own branch SOPs only (via branch portal) | Cannot edit, create, or distribute |
| CEO / COO | Group | View all SOPs | Executive oversight; no edit |
| All other roles | — | — | No access; branch staff access emergency numbers via sidebar widget only |

> **Access enforcement:** `@require_role('emergency_response_officer', 'medical_coordinator', 'branch_principal', 'ceo', 'coo')` with category-based write scope for Medical Coordinator enforced server-side: `sop.category == 'medical'` or `sop.category == 'transport'`. Branch Principal access scoped to `sop.applicable_branches contains request.user.branch`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Emergency Protocol Library
```

### 3.2 Page Header
- **Title:** `Emergency Protocol Library`
- **Subtitle:** `[N] Active SOPs · [N] Overdue Review · [N] Branches Fully Distributed`
- **Right controls:** `+ Create SOP` (Emergency Response Officer + Medical Coordinator) · `Advanced Filters` · `Bulk Distribute`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| SOP overdue for review (> 12 months since last review) | "⚠ [N] SOP(s) are overdue for annual review. Review and update before next drill cycle." | Amber |
| Branch missing a critical SOP (Medical Emergency or Fire Evacuation) | "CRITICAL: [N] branch(es) are missing one or more mandatory SOPs (Medical Emergency / Fire Evacuation). Distribute immediately." | Red |
| SOP in Draft status not yet approved | "[N] SOP(s) are in Draft status and have not been approved. Approve or discard." | Amber |
| Newly created SOP not yet distributed to any branch | "[N] active SOP(s) have not been distributed to any branch." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Active SOPs | SOPs with status = Active | Blue always |
| SOPs Overdue for Review | Last review date > 12 months ago | Green = 0 · Yellow 1–3 · Red > 3 |
| Branches with All SOPs Distributed | Branches where all applicable SOPs have been distributed | Blue; sub-label shows % of total branches |
| SOPs Pending Distribution | Active SOPs with one or more branches not yet distributed to | Green = 0 · Amber ≥ 1 |
| SOPs Updated This Month | SOPs with new version created in current calendar month | Blue always |

---

## 5. Sections

### 5.1 SOP Library Table

**Search:** SOP name. 300ms debounce, minimum 2 characters.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Category | Checkbox | Medical Emergency / Fire Evacuation / Natural Disaster / Transport / Missing Person / Security Breach |
| Status | Radio | All / Draft / Active / Archived |
| Review Overdue | Radio | All / Yes (> 12 months) / No |
| Branch Distribution | Radio | All / Fully Distributed / Partially Distributed / Not Distributed |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| SOP Name | ✅ | Click → `sop-detail` drawer |
| Category | ✅ | Colour-coded badge per category |
| Version | ✅ | e.g. v1.0, v2.3; tooltip shows version history count |
| Last Reviewed | ✅ | Date; red if > 12 months ago; green if ≤ 6 months |
| Next Review Due | ✅ | Calculated from last review + review cycle; red if past |
| Status | ✅ | Draft (grey) / Active (green) / Archived (dark grey) badge |
| Branches Distributed | ✅ | Count of branches distributed to / total applicable branches; e.g. "45 / 50" |
| Actions | ❌ | View · Edit · New Version · Distribute · Archive |

**Default sort:** Status (Draft first, then Active, then Archived), then Next Review Due ascending.
**Pagination:** Server-side · 25 records per page.

---

### 5.2 Branch Distribution Sub-table (drill-down)

Accessed by clicking the **Branches Distributed** count cell in the main table. Expands inline below the SOP row via HTMX.

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Branch name |
| Distributed Date | ✅ | Date SOP was distributed to this branch |
| Acknowledged By | ✅ | Principal name (blank if not yet acknowledged) |
| Acknowledgement Date | ✅ | Date of acknowledgement; blank if pending |
| Drills Based on This SOP (count) | ✅ | Count of drills at this branch linked to this SOP; click → drill list filter |

Sub-table filtered to the selected SOP. Rows with no acknowledgement highlighted in amber. Re-distribute button available per row for Emergency Response Officer.

---

## 6. Drawers / Modals

### 6.1 Drawer — `sop-detail` (720px, right side)

Triggered by SOP name link or **View** action.

**Tabs:**

#### Tab 1 — Content

Full SOP text displayed in structured read-only view. Sections:

| Section | Notes |
|---|---|
| Trigger Conditions | What event or observation activates this SOP |
| Immediate Steps | Numbered sequential actions (1 to N); each step on separate line with bold action verb |
| Responsibilities by Role | Table: Role → Specific responsibilities in this emergency |
| Resources Required | Equipment, medicines, contact tools, assembly area, fire extinguisher locations, etc. |
| Contact Numbers | Emergency contacts: local hospital, ambulance, fire brigade, police, group Emergency Response Officer, branch principal, parent notification coordinator |
| Escalation Path | Step-by-step: who informs whom and in what order; time thresholds for each escalation |
| Post-Incident Actions | Steps to take after the emergency is resolved: parent communication, documentation, incident reporting, medical follow-up, debrief |

Edit button (Emergency Response Officer / Medical Coordinator for medical SOPs only) opens `sop-edit` drawer for current version or triggers `new-version` flow.

#### Tab 2 — Version History

| Column | Notes |
|---|---|
| Version | v1.0 → current |
| Date | Version creation date |
| Changed By | User name + role |
| Change Summary | Free text description of what changed in this version |
| Approval Status | Approved / Pending / Draft |
| Actions | View (read-only) · Restore as Current (Emergency Response Officer only) |

#### Tab 3 — Distribution

Table of all branches applicable to this SOP with distribution status:

| Column | Notes |
|---|---|
| Branch | Branch name |
| Applicable | Yes / No (based on SOP applicability settings) |
| Distributed | Yes / No + date |
| Acknowledged | Yes / No + date + by whom |
| Overdue Acknowledgement | Yes/No flag (> 14 days since distribution without acknowledgement) |
| Actions | Distribute (if not yet distributed) · Re-distribute · Send Reminder |

#### Tab 4 — Drills

Table of all drills across all branches that reference this SOP as the guiding protocol.

| Column | Notes |
|---|---|
| Drill Name | Auto-generated from type + branch + date |
| Branch | |
| Date | |
| Outcome Score | Pass / Fail / Partial |
| Issues Found | Count; click → opens drill detail drawer (Page 19) |

---

### 6.2 Drawer — `sop-create` (700px, right side)

Triggered by **+ Create SOP**.

| Field | Type | Validation |
|---|---|---|
| SOP Name | Text input (max 200 chars) | Required; must be unique within category |
| Category | Single-select: Medical Emergency / Fire Evacuation / Natural Disaster / Transport / Missing Person / Security Breach | Required |
| Applicability | Radio: All Branches / Specific Branches / Hostel Only / Day School Only | Required |
| Specific Branches | Multi-select (shown only if Applicability = Specific Branches) | Required if specific |
| Content — Trigger Conditions | Rich text editor section | Required |
| Content — Immediate Steps | Rich text editor (ordered list enforced) | Required; minimum 3 steps |
| Content — Responsibilities by Role | Rich text editor (table view preferred) | Required |
| Content — Resources Required | Rich text editor | Required |
| Content — Contact Numbers | Structured input: Contact Name + Role + Phone (add rows) | Required; minimum 3 contacts |
| Content — Escalation Path | Rich text editor | Required |
| Content — Post-Incident Actions | Rich text editor | Required |
| Review Cycle | Radio: 6 months / 12 months | Required; default 12 months |
| Owner | Radio: Emergency Response Officer / Medical Coordinator | Required |
| Initial Status | Radio: Draft / Active | Required; cannot set Active without all mandatory sections complete |

**Footer:** `Cancel` · `Save as Draft` · `Save & Activate`

---

### 6.3 Drawer — `sop-edit / new-version` (700px, right side)

Triggered by **Edit** action (creates in-place edit with new version if material changes detected) or **New Version** action (explicit version bump).

| Field | Type | Notes |
|---|---|---|
| Current Version | Read-only | Displayed prominently |
| Current Status | Read-only | |
| All content fields | Pre-populated from current version | All sections editable |
| Version Notes | Textarea (max 500 chars) | Required — describe what changed and why |
| Version Type | Radio: Minor revision (e.g. v1.1) / Major revision (e.g. v2.0) | Required |

On save: current version automatically archived; new version number assigned; new version set to Draft pending approval; approval workflow: Emergency Response Officer must explicitly approve before status → Active.

**Footer:** `Cancel` · `Save New Version as Draft` · `Save & Approve New Version`

---

### 6.4 Modal — `distribute-modal` (500px, centred)

Triggered by **Distribute** action from table or Distribution tab.

| Field | Type | Validation |
|---|---|---|
| SOP Name | Read-only | |
| SOP Version | Read-only | Shows current active version |
| Select Branches | Multi-select (pre-selected with applicable branches not yet distributed) | Required |
| Distribution Method | Checkbox: WhatsApp Notification + Portal Access (both selected by default) | Required |
| Require Acknowledgement | Radio: Yes / No | Default: Yes |
| Acknowledgement Deadline | Date picker | Required if Require Acknowledgement = Yes; must be ≥ 3 days from today |
| Message to Principal | Textarea (max 300 chars, pre-filled with default message) | Optional |

**Footer:** `Cancel` · `Distribute Now`

On distribute: portal access granted to selected branches; WhatsApp notification sent to branch principals if selected; acknowledgement request created with deadline.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| SOP created (draft) | "SOP saved as draft. Complete all mandatory sections to activate." | Info |
| SOP activated | "SOP '[Name]' activated and ready for distribution." | Success |
| SOP updated / new version | "New version [v.N] of '[SOP Name]' created. Previous version archived." | Success |
| SOP distributed | "SOP '[Name]' distributed to [N] branch(es). Acknowledgement requested by [date]." | Success |
| SOP archived | "SOP '[Name]' archived. It will no longer appear in active library." | Info |
| Acknowledgement reminder sent | "Acknowledgement reminder sent to [N] branch principal(s)." | Info |
| Validation error — incomplete sections | "Complete all mandatory SOP sections (Trigger, Steps, Roles, Contacts, Escalation, Post-Event) before activating." | Error |
| Distribution failed — no active version | "Cannot distribute: SOP is in Draft or Archived status. Activate before distributing." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No SOPs in library | "No emergency SOPs on record." | "Create your first SOP to begin building the group's emergency protocol library." | `+ Create SOP` |
| No SOPs in category | "No SOPs in this category." | "No [Category] SOPs have been created yet." | `+ Create SOP` |
| No results for filters | "No SOPs match your current filters." | "Try adjusting the category, status, or distribution filters." | `Clear Filters` |
| Version history — single version | "This is the first and only version." | "Version history will appear here after the first update." | — |
| Distribution tab — no branches | "This SOP has not been distributed to any branch yet." | "Use the Distribute action to send it to all applicable branches." | `Distribute Now` |
| Drills tab — no drills | "No drills have referenced this SOP yet." | "Drills using this protocol will appear here once scheduled." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 5 KPI cards + SOP table (5 grey rows × 8 columns) |
| Filter apply | Table body inline spinner; KPI bar refreshes |
| Branch distribution sub-table expand | Inline skeleton: 3 grey rows × 6 columns |
| SOP detail drawer open | Drawer skeleton: tab bar + content area (structured section blocks in grey) |
| Version history tab load | Table skeleton (3 grey rows) |
| Distribution tab load | Table skeleton (5 grey rows) |
| Drills tab load | Table skeleton (3 grey rows) |
| SOP create / edit save | Submit button spinner; all fields disabled |
| Distribute modal submit | Modal footer spinner + "Distributing to [N] branches…" |
| Content rich text editor | Editor loads with slight delay; show skeleton placeholder until JS editor initialised |

---

## 10. Role-Based UI Visibility

| UI Element | Emergency Response Officer | Medical Coordinator | Branch Principal | CEO / COO |
|---|---|---|---|---|
| Full SOP library (all categories) | ✅ | ✅ | Own branch SOPs only | ✅ (view only) |
| + Create SOP button | ✅ | Medical category only | ❌ | ❌ |
| Edit action (all categories) | ✅ | Medical category only | ❌ | ❌ |
| New Version action | ✅ | Medical category only | ❌ | ❌ |
| Distribute action | ✅ | ❌ | ❌ | ❌ |
| Archive action | ✅ | ❌ | ❌ | ❌ |
| Approve new version | ✅ | ❌ | ❌ | ❌ |
| Version history tab | ✅ | ✅ | ❌ | ✅ |
| Distribution tab — full | ✅ | ✅ (view only) | ❌ | ✅ (view only) |
| Distribution tab — send reminder | ✅ | ❌ | ❌ | ❌ |
| Drills tab | ✅ | ✅ | ❌ | ✅ |
| Content tab (read) | ✅ | ✅ | ✅ (own branch SOPs) | ✅ |
| Content tab (edit) | ✅ | Medical SOPs only | ❌ | ❌ |
| KPI bar — all 5 cards | ✅ | ✅ | ❌ | ✅ |
| Alert banners | ✅ | ✅ | ❌ | ✅ |
| Bulk Distribute button | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/emergency-protocols/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/emergency-protocols/` | List all SOPs (paginated, filtered) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/emergency-protocols/` | Create new SOP | Emergency Response Officer / Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/` | Retrieve full SOP detail | JWT + role check + branch scope |
| PATCH | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/` | Update SOP (minor edit) | Emergency Response Officer / Medical Coordinator (own category) |
| GET | `/api/v1/group/{group_id}/health/emergency-protocols/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/emergency-protocols/alerts/` | Active alert conditions | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/version/` | Create new version | Emergency Response Officer / Medical Coordinator (own category) |
| POST | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/approve/` | Approve draft version | Emergency Response Officer |
| POST | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/archive/` | Archive SOP | Emergency Response Officer |
| GET | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/versions/` | Version history list | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/versions/{version_id}/` | Specific version content | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/distribute/` | Distribute SOP to branches | Emergency Response Officer |
| GET | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/distribution/` | Distribution status per branch | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/distribution/{branch_id}/remind/` | Send acknowledgement reminder | Emergency Response Officer |
| GET | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/drills/` | Drills linked to this SOP | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/emergency-protocols/{sop_id}/distribution/{branch_id}/` | Branch-specific distribution detail | JWT + role check |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `search` | str | SOP name |
| `category` | str[] | `medical`, `fire`, `natural_disaster`, `transport`, `missing_person`, `security` |
| `status` | str | `draft`, `active`, `archived` |
| `review_overdue` | bool | `true` = only SOPs with last review > 12 months |
| `distribution` | str | `full`, `partial`, `none` |
| `page` | int | Page number |
| `page_size` | int | Default 25; max 100 |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search debounce | `hx-get="/api/.../emergency-protocols/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#sop-table-body"` `hx-include="#filter-form"` | Table rows replaced |
| Filter form apply | `hx-get="/api/.../emergency-protocols/"` `hx-trigger="change"` `hx-target="#sop-table-body"` `hx-include="#filter-form"` | Table and KPI bar refreshed |
| KPI bar load | `hx-get="/api/.../emergency-protocols/kpi/"` `hx-trigger="load"` `hx-target="#kpi-bar"` | On page load |
| Alert banner load | `hx-get="/api/.../emergency-protocols/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | On page load |
| Pagination | `hx-get="/api/.../emergency-protocols/?page={n}"` `hx-target="#sop-table-body"` `hx-push-url="true"` | Page swap |
| Distribution sub-table expand | `hx-get="/api/.../emergency-protocols/{sop_id}/distribution/"` `hx-target="#dist-subtable-{sop_id}"` `hx-trigger="click"` `hx-swap="innerHTML"` | Inline sub-table inserted below SOP row; toggle on second click |
| SOP detail drawer open | `hx-get="/api/.../emergency-protocols/{sop_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Content tab default |
| Drawer tab switch | `hx-get="/api/.../emergency-protocols/{sop_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` `hx-trigger="click"` | Tab content lazy loaded on first click |
| Version history tab | `hx-get="/api/.../emergency-protocols/{sop_id}/versions/"` `hx-target="#versions-content"` `hx-trigger="click[tab='versions'] once"` | Loaded once on first click |
| Distribution tab load | `hx-get="/api/.../emergency-protocols/{sop_id}/distribution/"` `hx-target="#distribution-content"` `hx-trigger="click[tab='distribution'] once"` | Loaded once on first click |
| Drills tab load | `hx-get="/api/.../emergency-protocols/{sop_id}/drills/"` `hx-target="#drills-content"` `hx-trigger="click[tab='drills'] once"` | Loaded once on first click |
| SOP create submit | `hx-post="/api/.../emergency-protocols/"` `hx-target="#sop-table-body"` `hx-on::after-request="closeDrawer(); fireToast();"` | New SOP row prepended; drawer closed |
| SOP edit submit | `hx-patch="/api/.../emergency-protocols/{sop_id}/"` `hx-target="#sop-row-{sop_id}"` `hx-swap="outerHTML"` | Row updated in-place |
| New version submit | `hx-post="/api/.../emergency-protocols/{sop_id}/version/"` `hx-target="#sop-row-{sop_id}"` `hx-swap="outerHTML"` `hx-on::after-request="fireToast();"` | Version column updated; toast shown |
| Approve version | `hx-post="/api/.../emergency-protocols/{sop_id}/approve/"` `hx-target="#sop-row-{sop_id}"` `hx-swap="outerHTML"` | Status badge updated |
| Distribute modal submit | `hx-post="/api/.../emergency-protocols/{sop_id}/distribute/"` `hx-target="#distribution-content"` `hx-on::after-request="closeModal(); fireToast();"` | Distribution tab refreshed; Branches Distributed count updated via out-of-band swap |
| Send reminder | `hx-post="/api/.../emergency-protocols/{sop_id}/distribution/{branch_id}/remind/"` `hx-target="#dist-row-{branch_id}"` `hx-swap="outerHTML"` | Row "Last Reminder" column updated |
| Archive confirm | `hx-post="/api/.../emergency-protocols/{sop_id}/archive/"` `hx-target="#sop-row-{sop_id}"` `hx-swap="outerHTML"` | Row status badge changes to Archived; row moved to end of table |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
