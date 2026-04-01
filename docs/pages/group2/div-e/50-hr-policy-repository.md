# 50 — HR Policy Repository

- **URL:** `/group/hr/policies/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Director (Role 41, G3)

---

## 1. Purpose

The HR Policy Repository is the centralized, version-controlled store for all HR policies applicable across the group. All branches operate under a unified HR policy framework set by Group HR, with branch-specific addendums permitted only where explicitly allowed. This page is where the HR Director creates, updates, archives, and publishes policies. Branch staff access the published versions of applicable policies through their branch portal — any update to a policy at group level is automatically reflected in what branch staff see.

The policies maintained in this repository are: Leave Policy (defines annual leave, sick leave, casual leave, maternity, paternity, and special leave entitlements), Attendance Policy (working hours, late arrivals, biometric compliance, work-from-home rules), Code of Conduct (professional behaviour, communication standards, confidentiality obligations), Anti-Ragging Policy (group's stance and procedures on ragging — mandated by AICTE/UGC), POCSO Policy (institution's child protection framework and reporting obligations), POSH Policy (internal sexual harassment prevention and ICC procedure), Dress Code Policy (uniform requirements and appearance standards), Transfer Policy (criteria and process for staff transfers between branches), Grievance Redressal Policy (formal grievance process, SLAs, escalation matrix), Promotion and Appraisal Policy (criteria, frequency, and transparency standards for staff promotions), Salary Advance Policy (eligibility, limits, and recovery terms for salary advances), and Disciplinary Policy (spectrum of disciplinary action, procedural fairness standards, appeal rights).

Each policy record includes metadata: policy name, category, version number (major.minor format — e.g., 3.1), effective date, last reviewed date, applicable staff types (Teaching / Non-Teaching / All), and approved-by name and designation. When the HR Director edits a published policy, the system does not overwrite it — it creates a new version draft. The previous version is archived and remains accessible in the version history. This ensures that any disciplinary or legal proceeding can reference the exact policy text in force at the time of the incident.

The repository also tracks staff acknowledgement. When a new policy version is published, branch staff are expected to read and acknowledge it via their branch portal. This page shows the group-wide acknowledgement rate per policy, enabling the HR Director to identify policies with low awareness (which may indicate that staff have not been adequately briefed, or that the policy is not prominently surfaced in the branch portal).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director | G3 | Full CRUD + Publish + Archive + Version Management | Primary operator |
| Group HR Manager | G3 | Read-only + Create Draft (HR Director approval required to publish) | Draft creation support |
| Branch Principal | G3 | Read-only (published policies applicable to their branch) | View-only; no create/edit |
| All teaching staff (via branch portal) | G0–G1 | Read-only — applicable published policies only | View and acknowledge |
| Group Training & Dev Manager | G2 | Read-only (POCSO + Training policies only) | Scoped reference |
| All other group roles | — | No access to this group HR admin page | Branch portal access only |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › HR Policy Repository
```

### 3.2 Page Header

- **Title:** HR Policy Repository
- **Subtitle:** Group HR Policy Framework — version-controlled, branch-distributed
- **Primary CTA:** `+ Create Policy` (HR Director only)
- **Secondary CTA:** `Export Policy List` (CSV — metadata table)
- **Header badge:** Count of policies in Draft / Under Review status shown in amber

### 3.3 Alert Banner (conditional)

- **Amber:** `[N] policies are due for annual review. Review and republish before expiry.` Action: `View Due`
- **Amber:** `[N] policy drafts are pending publication approval.` Action: `Review Drafts`
- **Blue:** `[N] policies have staff acknowledgement rate below 80%.` Action: `View`
- **Green:** All policies current and published — shown when no active alerts

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Policies | Count of all non-deleted policy records | Blue always | No drill-down |
| Policies Due for Annual Review | Count where review_due_date within next 60 days or past due | Amber if > 0, else grey | Filter to due policies |
| Policies Pending Publication | Count in Draft or Under Review status | Amber if > 0, else grey | Filter to pending policies |
| Recently Updated | Count updated in last 30 days | Blue always | Filter to recently updated |
| Policies Acknowledged by All Staff % | % of published policies where all_staff_acknowledged = true | Green if ≥ 90%, amber 75–89%, red < 75% | Filter to low-acknowledgement policies |
| Archived Policies | Count of archived (superseded) policy versions | Grey always | No drill-down |

---

## 5. Main Table — Policy Register

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Policy Name | Text (link — opens View drawer) | Yes (A–Z) | Yes — text search |
| Category | Badge (Leave / Attendance / Conduct / POCSO / POSH / HR Process / Other) | No | Yes — checkbox group |
| Version | Text (e.g., v3.1) | Yes | No |
| Effective Date | Date | Yes | Yes — date range |
| Review Due | Date + urgency chip | Yes | Yes — overdue toggle |
| Status | Badge (Published / Draft / Under Review / Archived) | No | Yes — checkbox group |
| Applicable Staff | Text (All / Teaching / Non-Teaching) | No | Yes — dropdown |
| Acknowledgement % | Progress bar (% of applicable staff who acknowledged current version) | Yes | Yes — range dropdown |
| Actions | Icon buttons: View / Edit (creates new version) / Archive / Publish | No | No |

### 5.1 Filters

- **Status:** Published / Draft / Under Review / Archived / All
- **Category:** Multi-select checkboxes
- **Applicable Staff:** All / Teaching / Non-Teaching
- **Review Status:** Overdue / Due within 60 days / Current / All
- **Acknowledgement Rate:** All / Below 80% / Below 50%
- **Reset Filters** button

### 5.2 Search

Text search on Policy Name. Min 2 characters, 400 ms debounce.

### 5.3 Pagination

Server-side. Default 20 rows per page. Options: 10 / 20 / 50. "Showing X–Y of Z policies."

---

## 6. Drawers

### 6.1 Create Policy

Triggered by `+ Create Policy`. Wide right slide-in drawer.

**Fields:**
- Policy Name (text, max 150 characters)
- Category (dropdown — 7 categories)
- Applicable Staff Types (checkboxes: Teaching / Non-Teaching — default: both)
- Applicable Employment Types (checkboxes: Permanent / Contract / Visiting — default: all)
- Effective Date (date picker)
- Review Frequency (dropdown: 6 months / 12 months / 24 months / As Needed)
- Review Due Date (auto-calculated from effective date + review frequency)
- Approved By (text — name and designation of approving authority)
- Policy Content (rich text editor — headings, bold, lists, tables supported; no embedded images)
- Attachments (PDF upload, optional — for policy document in official format, max 10 MB)
- Initial Status (radio: Save as Draft / Submit for Review)

**Validation:** Policy Name must be unique. Content required (minimum 200 characters).

**Submit:** `Create Policy` → POST `/api/hr/policies/`

### 6.2 View Policy

Read-only drawer showing full policy details.

**Displays:**
- Policy metadata (name, category, version, dates, approved by)
- Full policy content rendered from stored rich text
- Acknowledgement statistics (total applicable staff / acknowledged / pending)
- Version history table (version number / effective date / status / archived date)
- Download as PDF button (opens signed URL to uploaded PDF, or generates from rich text if no PDF uploaded)

### 6.3 Edit Policy (Creates New Version)

Triggered by Edit icon. Not available for Archived policies.

**Behaviour:**
- System displays confirmation dialog: "Editing will create a new draft version (v[N+1]). The current published version will remain active until the new version is published. Continue?"
- On confirm: Opens Create Policy form pre-filled with current policy data
- Version number auto-incremented (major if significant change, minor if minor — HR Director selects on save)
- Previous version status remains Published until new version is published; on new version publish → prior version auto-archived

**Fields:** Same as Create. All fields editable in new draft.

### 6.4 Archive Policy

**Fields:**
- Policy ID (locked)
- Archive Reason (dropdown: Superseded by New Version / Policy Withdrawn / Merged with Another Policy / Regulatory Change)
- Notes (textarea, optional)
- Confirmation checkbox: "I confirm this policy should be archived and removed from branch-facing views."

**Submit:** `Archive Policy` → PATCH `/api/hr/policies/{id}/archive/` — status changes to Archived; no longer visible to branch staff

### 6.5 Publish Policy

**Fields:**
- Policy ID (locked)
- Confirm Effective Date (date — defaults to today or pre-set effective date)
- Notify All Branch Principals: checkbox (default checked)
- Require Staff Acknowledgement: checkbox (default checked — adds "read and acknowledged" prompt in branch portal)
- Publish Note (textarea, optional — message to accompany notification)

**Submit:** `Publish Policy` → PATCH `/api/hr/policies/{id}/publish/` — status = Published; notifications sent; prior version auto-archived if applicable

---

## 7. Charts

No dedicated charts on this page. Policy acknowledgement trend data is available in the HR Analytics Dashboard (page 47).

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| Policy created (draft) | Success | "Policy '[Name]' saved as draft." |
| Policy submitted for review | Info | "Policy '[Name]' submitted for review. Awaiting HR Director approval." |
| Policy published | Success | "Policy '[Name]' v[N] published. [N] branches notified." |
| New version draft created | Info | "New draft v[N] created for '[Name]'. Published version remains active." |
| Policy archived | Warning | "Policy '[Name]' archived. Removed from branch-facing views." |
| Low acknowledgement alert | Warning | "[N] staff members have not acknowledged '[Policy Name]'." |
| Server error | Error | "Failed to save. Please retry or contact support." |

---

## 9. Empty States

**No policies in repository (new group setup):**
> Icon: document stack with plus sign
> "No HR policies in the repository yet."
> "Create your first policy using '+ Create Policy'."
> CTA: `+ Create Policy`

**Filtered results return nothing:**
> Icon: magnifying glass
> "No policies match your current filters."
> CTA: `Reset Filters`

---

## 10. Loader States

- Page load: Skeleton KPI cards + skeleton table rows
- Drawer open (View): Spinner while policy content and acknowledgement data loads
- Rich text editor (Create/Edit): Editor toolbar appears first; content renders after brief load
- Version history in View drawer: Inline spinner while version list loads
- Export: Button spinner + "Generating..." during CSV generation

---

## 11. Role-Based UI Visibility

| UI Element | HR Director | HR Manager | Branch Principal | Staff (Branch Portal) |
|---|---|---|---|---|
| `+ Create Policy` button | Visible | Visible (draft only) | Hidden | Hidden |
| Edit action | Visible | Visible (draft only) | Hidden | Hidden |
| Archive action | Visible | Hidden | Hidden | Hidden |
| Publish action | Visible | Hidden | Hidden | Hidden |
| Acknowledgement % column | Visible | Visible | Hidden | N/A |
| All categories | Visible | Visible | Published + applicable only | Published + applicable only |
| Version History | Visible | Visible | Current version only | Current version only |
| Export Policy List | Visible | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/policies/` | Paginated policy list with filters |
| POST | `/api/hr/policies/` | Create new policy (draft) |
| GET | `/api/hr/policies/{id}/` | Single policy detail + version history |
| PATCH | `/api/hr/policies/{id}/` | Update draft policy |
| POST | `/api/hr/policies/{id}/new-version/` | Create new version from existing policy |
| PATCH | `/api/hr/policies/{id}/publish/` | Publish policy version |
| PATCH | `/api/hr/policies/{id}/archive/` | Archive policy |
| GET | `/api/hr/policies/{id}/acknowledgements/` | Acknowledgement stats per branch |
| GET | `/api/hr/policies/kpis/` | KPI summary bar data |
| GET | `/api/hr/policies/export/` | Export policy metadata CSV |

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| Table load | `hx-get` on page render | Fetches policy list |
| Filter/search change | `hx-get` + `hx-include` | Re-fetches filtered table |
| Pagination | `hx-get` on page buttons | Fetches page N |
| Drawer open (View) | `hx-get` + `hx-target="#drawer"` | Loads policy detail |
| Create / Edit form submit | `hx-post` / `hx-patch` + `hx-target="#table-body"` | Creates or updates policy, refreshes table |
| Publish action | `hx-patch` + `hx-confirm` + `hx-target="#row-{id}"` | Confirmation before publish; updates row status |
| Archive action | `hx-patch` + `hx-confirm` + `hx-target="#row-{id}"` | Confirmation before archive; updates row |
| KPI refresh | `hx-get` on `#kpi-bar` after any mutation | Reloads KPI counts |
| Toast | `hx-swap-oob` on `#toast-container` | Out-of-band toast injection |
| Rich text editor | JavaScript-initialised (not HTMX) | Editor initialises after drawer renders |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
