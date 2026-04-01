# 37 — Privacy Policy Manager

- **URL:** `/group/it/privacy/policies/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4) — Full access; Group Data Privacy Officer (Role 55, G1) — Read-only

---

## 1. Purpose

The Privacy Policy Manager is the version-controlled repository for all privacy-related policy documents that govern data processing across the group. These are the documents that inform data subjects (students, parents, staff, visitors) about their rights and the group's obligations under the DPDP Act 2023 and other applicable laws. The documents managed here include:

**Privacy Policy** — the comprehensive statement of how the group collects, processes, shares, and retains personal data. Required under DPDP Act Section 5 (notice requirement).

**Cookie Policy** — for the group's web portals, documenting what cookies are set, for what purpose, and how data subjects can opt out.

**Data Retention Policy** — the internal governance document specifying how long each category of personal data is retained before deletion or anonymisation.

**DPDP Notice** — a concise, accessible notice required to be provided to data subjects at the point of data collection under DPDP Act. This is typically embedded in admission forms, onboarding forms, and portal login flows.

Each policy document is version-controlled: when a policy is updated (e.g., new processing activities added, retention periods changed, contact details updated), a new version is created rather than overwriting the previous. The old version is archived and remains accessible for audit purposes. When a policy is published, the system sends an acknowledgement request to all branch principals — they must confirm they have read and understood the new version. The IT Admin tracks acknowledgement rates and sends reminders to branches that have not acknowledged.

The Data Privacy Officer has read-only access to review policy content and track acknowledgement status — they may flag to the IT Admin if policy content is legally insufficient. The IT Admin is the operational manager of the policy lifecycle.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full access — create, edit, publish, archive, track acknowledgements | Operational management |
| Group Data Privacy Officer | G1 | Read-only — view policies and acknowledgement status | Reviews for legal adequacy; provides feedback via comment |
| Group IT Director | G4 | Read-only | Governance oversight |
| All other Division F roles | — | Hidden | No access |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Data Privacy → Privacy Policy Manager
```

### 3.2 Page Header
- **Title:** `Privacy Policy Manager`
- **Subtitle:** `[N] Active Policies · [N] Pending Acknowledgement · Policy Repository`
- **Role Badge:** `Group IT Admin` or `Group Data Privacy Officer`
- **Right-side controls (IT Admin only):** `+ Create Policy` · `Export`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Branch principal has not acknowledged updated policy >14 days | "[N] branch(es) have not acknowledged the latest [Policy Name] (version [X]) in more than 14 days. Send reminder." | Amber |
| Policy approaching its review date (if review date set) | "Privacy Policy '[Name]' is due for review on [date]. Ensure it is updated to reflect any new data processing activities." | Amber |
| Policy published but DPO has flagged a concern | "Data Privacy Officer has flagged a concern on policy '[Name]'. Review DPO comments before further publishing." | Amber |
| All branch principals acknowledged | (Positive confirmation — shown as green dismissible banner) "All branches have acknowledged [Policy Name] v[X]." | Green (dismissible) |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Policies | Count of policies with status = Active | Blue | Filter by Active |
| Pending Acknowledgement | Count of branches that have not acknowledged the latest active version of any policy | Amber if > 0 | Opens acknowledgement tracking view |
| Policies Updated This Year | Count of policies with a new version published in the current calendar year | Blue | Filter by current year |
| Overdue Acknowledgements | Branches that have not acknowledged within 14 days of policy publication | Red if > 0 | Filter by overdue |

---

## 5. Main Table — Policy Repository

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Policy Name | Text (link to view/edit drawer) | Yes | Yes (text search) |
| Type | Badge (Privacy Policy / Cookie Policy / Retention Policy / DPDP Notice / Other) | Yes | Yes (multi-select) |
| Version | Text (e.g., "v3.1") | Yes | No |
| Status | Badge (Active / Draft / Archived) | Yes | Yes (multi-select) |
| Effective Date | Date | Yes | Yes (date range) |
| Branches Acknowledged | Text ("N / Total" — e.g., "18 / 22") | Yes | No |
| Last Updated | Datetime (relative) | Yes | No |
| Actions | View / Edit / Publish / Archive / Track Acknowledgements | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Type | Multi-select checkbox | Privacy Policy / Cookie Policy / Retention Policy / DPDP Notice / Other |
| Status | Multi-select checkbox | Active / Draft / Archived |
| Effective Date | Date range picker | Any range |

### 5.2 Search
- Policy Name; 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `policy-create` — Create Policy
- **Trigger:** `+ Create Policy` button
- **Width:** 720px (wider for rich text editor)
- **Fields:**
  - Policy Name (required, text — e.g., "Group Privacy Policy")
  - Type (required, dropdown)
  - Version (required, text — e.g., "v1.0"; suggest semantic versioning)
  - Effective Date (required, date picker — when this version takes effect)
  - Review Due Date (optional, date picker — when this policy should be reviewed again)
  - Policy Body (required, rich text editor — supports headings, lists, bold/italic, links; minimum 200 characters)
    - Pre-fill options: "Load template for [Type]" buttons which populate the editor with a DPDP Act-compliant template for that policy type
  - Publish Immediately (toggle — if off, saves as Draft; if on, proceeds to Publish modal on submit)
  - Internal Notes for DPO (optional, textarea — notes visible to DPO and IT Admin only; not part of published policy)

### 6.2 Drawer: `policy-edit` — Edit Policy
- **Trigger:** Actions → Edit (available on Draft policies; for Active policies, creates a new version)
- **Width:** 720px
- **Behaviour for Active policies:**
  - A warning banner: "This policy is currently Active. Editing will create a new draft version [current version + 0.1 increment]. The active version remains live until the new version is published."
  - All fields editable; version auto-incremented (can be overridden)
  - Internal changelog field (required when editing active policy): "Summary of changes from previous version"
- **Behaviour for Draft policies:** Direct edit, same form as create

### 6.3 Modal: Publish Policy
- **Trigger:** Actions → Publish (available for Draft policies)
- **Confirmation screen:**
  - "Publishing [Policy Name] v[X] will:"
  - - Set this version as the Active version
  - - Archive the previous active version (if any)
  - - Send an acknowledgement request to [N] branch principals
  - - Display this policy on branch portals where applicable
  - Acknowledge requests sent via: in-app notification + email to all branch principals
  - Confirm Publish button / Cancel button
- On publish: policy.status → Active; previous Active → Archived; acknowledgement_requests created for all branches

### 6.4 Modal: Archive Policy
- **Trigger:** Actions → Archive
- **Confirmation:** "Archiving '[Policy Name]' v[X] will remove it from active use. Select the replacement policy that supersedes it, or confirm there is no replacement."
- Replace with: dropdown (select another policy or "No replacement — policy being retired")
- Buttons: Confirm Archive · Cancel

### 6.5 Drawer: `acknowledgement-tracker` — Track Acknowledgements
- **Trigger:** Actions → Track Acknowledgements
- **Width:** 720px
- **Header:** Policy name, version, published date, total branches, acknowledged count
- **Table: Branch Acknowledgement Status**

  | Column | Content |
  |---|---|
  | Branch Name | Text |
  | Principal Name | Text |
  | Acknowledgement Status | Badge (Acknowledged / Pending / Overdue [>14d]) |
  | Acknowledged Date | Datetime or "—" |
  | Acknowledgement Method | Badge (Portal Click / Email Response / "—") |
  | Reminder Sent | Date of last reminder or "No reminder sent" |
  | Actions | Send Reminder (IT Admin only) |

- **Bulk action (IT Admin only):** "Send Reminder to All Pending" button — sends reminder to all branches that have not yet acknowledged
- **Send Individual Reminder:** Sends in-app notification + email to the specific branch principal

### 6.6 Drawer: `policy-view` — View Policy
- **Trigger:** Click on Policy Name
- **Width:** 720px
- **Content:**
  - Policy metadata (type, version, effective date, status)
  - Full rendered policy body (HTML rendered from stored rich text)
  - Version history list (all past versions — version number, published date, archived date, download link for each)
  - DPO notes (if any — visible to IT Admin and DPO)
  - Acknowledgement summary: N branches acknowledged / Total
- **DPO Review Notes:** DPO can add a comment on the policy content (text area, visible to IT Admin)

**Audit Trail:** All policy lifecycle events (creation, publication, archival, DPO review comments, reminder sends) are automatically logged to the IT Audit Log with actor and timestamp.

---

## 7. Charts

No standalone charts on this page.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Policy created (draft) | "Policy '[Name]' v[X] saved as draft." | Info | 3s |
| Policy published | "Policy '[Name]' v[X] published. Acknowledgement requests sent to [N] branch principals." | Success | 5s |
| Policy archived | "Policy '[Name]' v[X] archived." | Info | 3s |
| Reminder sent (individual) | "Acknowledgement reminder sent to [Principal Name] at [Branch Name]." | Info | 3s |
| Bulk reminder sent | "Reminder sent to [N] pending branch principals for '[Policy Name]'." | Info | 4s |
| DPO comment saved | "Review comment saved on policy '[Name]'." | Success | 3s |
| All branches acknowledged | "All [N] branches have acknowledged '[Policy Name]' v[X]." | Success | 4s |
| Policy publish failed | Error: `Failed to publish policy. Ensure policy body has content and version is valid.` | Error | 5s |
| Policy archive failed | Error: `Failed to archive policy. Verify replacement policy selection.` | Error | 5s |
| Reminder send failed | Error: `Failed to send acknowledgement reminder to [Branch Name].` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No policies | "No Policies in Repository" | "No privacy policies have been created yet. Create a Privacy Policy and DPDP Notice as a priority to comply with DPDP Act 2023." | + Create Policy |
| No acknowledgements pending | "All Acknowledged" | "All branch principals have acknowledged the current active version." | — |
| No results for filter | "No Matching Policies" | "No policies match the selected filters." | Clear Filters |
| Policy body empty | "No Content" | "This policy has no body content. Edit the policy to add content before publishing." | Edit Policy |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 4 KPI shimmer cards + table skeleton (8 rows) |
| Filter / search | Table skeleton shimmer |
| View policy drawer | Drawer spinner; policy body rendered after metadata loads |
| Acknowledgement tracker drawer | Drawer spinner; branch table loads progressively |
| Publish modal confirm | Button spinner: "Publishing policy and sending acknowledgement requests…" |
| Edit policy drawer | Drawer spinner; rich text editor initialises with content |
| Send bulk reminders | Button spinner: "Sending reminders to [N] branches…" |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | Data Privacy Officer (G1) | IT Director (G4) | Cybersecurity Officer (G1) | IT Support Executive (G3) |
|---|---|---|---|---|---|
| + Create Policy | Visible | Hidden | Hidden | Hidden | Hidden |
| Edit Action | Visible | Hidden | Hidden | Hidden | Hidden |
| Publish Action | Visible | Hidden | Hidden | Hidden | Hidden |
| Archive Action | Visible | Hidden | Hidden | Hidden | Hidden |
| Track Acknowledgements | Visible | Visible (read-only) | Visible (read-only) | Hidden | Hidden |
| Send Reminder buttons | Visible | Hidden | Hidden | Hidden | Hidden |
| Policy Body (view) | Visible | Visible | Visible | Hidden | Hidden |
| Version History | Visible | Visible | Visible | Hidden | Hidden |
| DPO Review Notes | Visible (read) | Visible + editable | Visible (read) | Hidden | Hidden |
| Internal Notes for DPO | Visible (read + edit) | Visible (read) | Hidden | Hidden | Hidden |
| Export | Visible | Hidden | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/privacy/policies/` | JWT (G1+) | Paginated policy list |
| POST | `/api/v1/it/privacy/policies/` | JWT (G4 — IT Admin) | Create new policy (draft) |
| GET | `/api/v1/it/privacy/policies/{id}/` | JWT (G1+) | Full policy detail + version history |
| PATCH | `/api/v1/it/privacy/policies/{id}/` | JWT (G4 — IT Admin) | Update draft policy content |
| POST | `/api/v1/it/privacy/policies/{id}/publish/` | JWT (G4 — IT Admin) | Publish policy; send acknowledgements |
| POST | `/api/v1/it/privacy/policies/{id}/archive/` | JWT (G4 — IT Admin) | Archive policy |
| GET | `/api/v1/it/privacy/policies/{id}/acknowledgements/` | JWT (G1+) | Branch acknowledgement status list |
| POST | `/api/v1/it/privacy/policies/{id}/acknowledgements/remind-all/` | JWT (G4 — IT Admin) | Send bulk reminder to pending branches |
| POST | `/api/v1/it/privacy/policies/{id}/acknowledgements/{branch_id}/remind/` | JWT (G4 — IT Admin) | Send reminder to individual branch |
| POST | `/api/v1/it/privacy/policies/{id}/dpo-comment/` | JWT (G1 DPO) | DPO adds review comment on policy |
| GET | `/api/v1/it/privacy/policies/kpis/` | JWT (G1+) | KPI card values |
| GET | `/api/v1/it/privacy/policies/templates/{type}/` | JWT (G4 — IT Admin) | Fetch policy template for given type |
| GET | `/api/v1/it/privacy/policies/export/` | JWT (G4) | Export policy list |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/privacy/policies/kpis/` | `#kpi-bar` | `innerHTML` |
| Load policies table | `load` | GET `/api/v1/it/privacy/policies/` | `#policies-table` | `innerHTML` |
| Apply filters | `change` on filter controls | GET `/api/v1/it/privacy/policies/?type=...&status=...` | `#policies-table` | `innerHTML` |
| Search policies | `input` (300ms debounce) | GET `/api/v1/it/privacy/policies/?q=...` | `#policies-table` | `innerHTML` |
| Open view drawer | `click` on Policy Name | GET `/api/v1/it/privacy/policies/{id}/` | `#policy-drawer` | `innerHTML` |
| Open acknowledgement tracker | `click` on Track Acknowledgements | GET `/api/v1/it/privacy/policies/{id}/acknowledgements/` | `#policy-drawer` | `innerHTML` |
| Send individual reminder | `click` on Send Reminder | POST `.../remind/` | `#ack-row-{branch_id}` | `outerHTML` |
| Send bulk reminder | `click` on Remind All Pending | POST `.../remind-all/` | `#acknowledgements-table` | `innerHTML` |
| Load template | `click` on Load Template button | GET `/api/v1/it/privacy/policies/templates/{type}/` | `#policy-body-editor` | `innerHTML` |
| Submit create | `click` on Create Draft | POST `/api/v1/it/privacy/policies/` | `#policies-table` | `innerHTML` |
| Confirm publish | `click` on Confirm Publish | POST `/api/v1/it/privacy/policies/{id}/publish/` | `#policies-table` | `innerHTML` |
| Confirm archive | `click` on Confirm Archive | POST `/api/v1/it/privacy/policies/{id}/archive/` | `#policies-table` | `innerHTML` |
| Save DPO comment | `click` on Save Comment | POST `.../dpo-comment/` | `#dpo-comment-result` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/it/privacy/policies/?page=N` | `#policies-table` | `innerHTML` |
| Export policies | `click` on Export | GET `/api/v1/it/privacy/policies/export/` | `#export-result` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
