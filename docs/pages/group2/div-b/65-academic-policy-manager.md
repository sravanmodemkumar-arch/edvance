# 65 — Academic Policy Manager

> **URL:** `/group/acad/academic-policies/`
> **File:** `65-academic-policy-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** CAO G4 · Academic Director G3 · Curriculum Coordinator G2 (view) · All Div-B roles (view published) · Branch staff (read + acknowledge via branch portal)

---

## 1. Purpose

The Academic Policy Manager is the version-controlled repository for all academic policies that govern how the institution group conducts education — result policies, assessment policies, promotion and re-examination policies, grace marks policies, and scholarship eligibility policies. These policies were previously distributed informally: emailed as PDFs, posted in WhatsApp groups, or referenced verbally in meetings. The result was that branches often operated on outdated policy versions, disputed promotion decisions citing different policy documents, or were unaware of policy changes until they caused a student welfare incident.

This page treats academic policies as living documents that require formal versioning, controlled publication, and tracked acknowledgement. Every policy has a version history, and any two versions can be compared side-by-side using a diff view — so when the result policy changes from a 33% pass mark to a 35% pass mark, the change is unambiguous, attributed, and dated. When a new version is published, all branches in scope receive an acknowledgement request. The CAO and Calendar Manager can see which branches have acknowledged and which have not, and can send targeted reminders to non-acknowledging branches.

The distinction between this page and the Governance Policy Manager in Division A (page 19) is important: Division A manages governance, conduct, POCSO, and operational policies for institution management. This page manages purely academic policies — the rules that determine how students are assessed, promoted, and supported academically. The two policy repositories are separate because they have different owners (CAO for academic, Chairman/MD for governance) and different audiences (teaching and academic staff vs. all staff and management).

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Full — create, publish, archive | Primary authority; final approver |
| Group Academic Director | G3 | ✅ Full | ✅ Draft + propose | Can draft policies; cannot publish without CAO |
| Group Curriculum Coordinator | G2 | ✅ Published policies only | ❌ | Read-only view of published policies |
| Group Exam Controller | G3 | ✅ Published | ❌ | Read + acknowledge |
| Group Results Coordinator | G3 | ✅ Published | ❌ | Read + acknowledge |
| Stream Coordinators (all) | G3 | ✅ Published | ❌ | Read + acknowledge |
| Group JEE/NEET Integration Head | G3 | ✅ Published | ❌ | Read + acknowledge |
| Group IIT Foundation Director | G3 | ✅ Published | ❌ | Read + acknowledge |
| Group Olympiad & Scholarship Coord | G3 | ✅ Published | ❌ | Read + acknowledge |
| Group Special Education Coordinator | G3 | ✅ Published | ❌ | Read + acknowledge |
| Group Academic MIS Officer | G1 | ✅ Published | ❌ | Read-only |
| Group Academic Calendar Manager | G3 | ✅ Published | ❌ | Read + acknowledge |
| Branch staff (Principal/Academic Coordinator) | Branch portal | ✅ Published (in scope) | ❌ | Read + acknowledge via branch portal |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Gap-Fill  ›  Academic Policy Manager
```

### 3.2 Page Header
```
Academic Policy Manager                               [+ New Policy]  [Export Policy Library ↓]
Version-controlled academic policies — [Group Name]             (CAO: create/publish · Acad Dir: draft)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Published Policies | Count |
| Policies in Draft | Count — blue |
| Archived Policies | Count — grey |
| Policies Awaiting Branch Acknowledgement | Count — amber |
| Branches with Unacknowledged Policies | Count — red |
| Policies Updated This Academic Year | Count |

---

## 4. Main Content

### 4.1 Search
- Full-text across: Policy name, category
- 300ms debounce · Highlights match in Policy Name column

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Category | Multi-select | Result / Assessment / Promotion / Re-exam / Scholarship |
| Status | Multi-select | Draft / Published / Archived |
| Branch Scope | Select | All / Zone / Specific branch |
| Acknowledgement Required | Select | Yes / No |
| Acknowledged by All Branches | Select | Yes / No / Partially |
| Academic Year | Select | Current + last 3 years |

Active filter chips dismissible. "Clear All". Filter badge count.

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | CAO, Academic Dir |
| Policy Name | Text + link | ✅ | Opens policy view drawer |
| Category | Badge | ✅ | Result / Assessment / Promotion / Re-exam / Scholarship |
| Version | Text | ✅ | e.g. v1.0, v2.3 |
| Status | Badge | ✅ | Draft (blue) / Published (green) / Archived (grey) |
| Effective Date | Date | ✅ | |
| Last Updated | Date | ✅ | |
| Branch Scope | Text | ✅ | All / Zone / [Branches] |
| Branches Acknowledged | Progress bar + fraction | ✅ | e.g. 42/50 — shown only if acknowledgement required |
| Actions | — | ❌ | Role-based |

**Default sort:** Status (Published first), then Last Updated descending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Action | Notes |
|---|---|---|---|---|
| View | Eye | All roles | `policy-view` drawer 560px | Full policy + version history + acknowledgements |
| Edit / Continue Draft | Pencil | CAO, Academic Dir | `policy-create` drawer 640px (pre-filled) | Edit draft; cannot edit published (must create new version) |
| Publish | Globe | CAO only | Confirm modal | Publishes draft; notifies branches |
| Create New Version | Copy | CAO, Academic Dir | `policy-create` drawer | Creates v+1 from current published — previous auto-archived |
| Archive | Archive | CAO only | Confirm modal | Moves published to archived |
| Send Acknowledgement Reminder | Bell | CAO | Confirm modal | Reminds non-acknowledging branches |
| Export PDF | Download | All roles | PDF download | Single policy formatted PDF |

### 4.5 Bulk Actions (CAO, Academic Dir)

| Action | Notes |
|---|---|
| Export Selected (PDF bundle) | Multiple policies in single ZIP |
| Send Reminder — All Unacknowledged | Bulk reminder for all selected policies with pending acknowledgements |

---

## 5. Drawers & Modals

### 5.1 Drawer: `policy-create` — New / Edit Policy
- **Trigger:** [+ New Policy] or Edit action or Create New Version
- **Width:** 640px
- **Tabs:** Content · Category & Scope · Effective Date · Acknowledgement · Preview

#### Tab: Content
| Field | Type | Required | Notes |
|---|---|---|---|
| Policy Name | Text | ✅ | Min 5, max 200 chars |
| Policy content | Rich text editor | ✅ | Supports headings, tables, bullet lists, bold/italic · Min 100 chars |
| Internal notes | Textarea | ❌ | Not visible in published policy; for internal reference only |
| Summary (for branch notice board) | Textarea | ✅ | 2–3 sentence plain-language summary · Max 500 chars |

**Rich text editor:** Supports: H1/H2/H3 · Bold · Italic · Underline · Bullet list · Numbered list · Table · Paste from Word (auto-cleans formatting).

#### Tab: Category & Scope
| Field | Type | Required | Notes |
|---|---|---|---|
| Category | Select | ✅ | Result / Assessment / Promotion / Re-exam / Scholarship |
| Applicable to | Multi-select | ✅ | All branches / Zone(s) / Specific branches |
| Applicable streams | Multi-select | ✅ | All / MPC / BiPC / MEC / CEC / HEC / Foundation |
| Applies from class | Multi-select | ✅ | All / Class 6–12 |
| Supersedes | Search + select | ❌ | Select a previous policy this one replaces |

#### Tab: Effective Date
| Field | Type | Required | Notes |
|---|---|---|---|
| Effective from | Date | ✅ | Cannot be in the past for new draft |
| Effective until | Date | ❌ | If time-limited policy |
| Academic year applicability | Select | ✅ | Current / All future / Specific year |

#### Tab: Acknowledgement
| Field | Type | Required | Notes |
|---|---|---|---|
| Require branch acknowledgement | Toggle | ✅ | Default on |
| Acknowledgement deadline | Date | Conditional | Required if acknowledgement on |
| Reminder: N days before deadline | Select | ✅ | 7 / 14 / 21 days |
| Remind who at branch | Select | ✅ | Principal / Academic Coordinator / Both |
| Acknowledge at group level too | Toggle | ❌ | Requires all Div-B group staff to acknowledge |

#### Tab: Preview
- Renders policy content as it will appear to branches
- Shows policy header: Name · Category · Version · Effective Date · Issued by (CAO name)
- [Download Preview PDF] button

- **Submit (Academic Dir):** "Save as Draft" — submits for CAO review
- **Submit (CAO):** "Save as Draft" or "Publish Immediately"
- **On publish:** All branches in scope notified · Acknowledgement request sent if required · Previous published version auto-archived

### 5.2 Drawer: `policy-view`
- **Width:** 560px
- **Tabs:** Current Version · Version History · Branch Acknowledgements

**Tab: Current Version**
Full policy content rendered (rich text, formatted). Header: Name · Category · v[X.Y] · Status · Effective date · Issued by.
[Download PDF] · [Download Summary PDF] (summary only).

**Tab: Version History**
| Column | Notes |
|---|---|
| Version | v1.0, v1.1, v2.0 etc. |
| Status | Published / Archived / Draft |
| Published On | Date |
| Published By | Name |
| Summary of changes | Brief change summary |
| [Compare with current] | Opens diff view modal |
| [Download this version] | PDF of that version |

**Tab: Branch Acknowledgements**
Two sub-lists: Acknowledged / Not Yet Acknowledged.
| Column | Notes |
|---|---|
| Branch | |
| Acknowledged By | Staff name |
| Acknowledged At | Datetime |
| Method | Portal / Email |

[Send Reminder to Unacknowledged] button (CAO only).

### 5.3 Modal: `version-diff-view`
- **Width:** 860px (full-width for readability)
- **Trigger:** "Compare with current" in Version History tab
- **Content:** Side-by-side diff view
  - Left panel: Selected version (older) — text, sections
  - Right panel: Current version — text, sections
  - Added text: Green highlight
  - Deleted text: Red strikethrough
  - Unchanged text: Normal
- **Header:** Comparing v[X] vs v[Y]
- **Buttons:** [Close] · [Download Diff PDF]

### 5.4 Modal: `publish-confirm`
- **Width:** 420px
- **Content:** "Publish '[Policy Name]' v[X.Y]? This will notify all branches in scope and require acknowledgement by [Deadline]."
- **Fields:** Confirm notification channel (Email / WhatsApp / Both, default Both) · Internal publish note (optional)
- **Buttons:** [Publish Policy] (green) · [Cancel]
- **On confirm:** Policy status → Published · Branch notifications sent · Previous version → Archived · Audit log

### 5.5 Modal: `archive-confirm`
- **Width:** 420px
- **Content:** "Archive '[Policy Name]'? It will no longer appear in active policy lists for branches."
- **Fields:** Reason (required, min 20 chars)
- **Buttons:** [Confirm Archive] · [Cancel]

### 5.6 Modal: `acknowledgement-reminder`
- **Width:** 420px
- **Content:** "Send acknowledgement reminder for '[Policy Name]' to [N] branches that have not yet acknowledged?"
- **Fields:** Message preview (editable, max 400 chars) · Channel (Email / WhatsApp / Both)
- **Buttons:** [Send Reminder] · [Cancel]

---

## 6. Charts

### 6.1 Acknowledgement Rate by Policy (Horizontal Bar)
- **Type:** Horizontal bar
- **Data:** % branches acknowledged per published policy with required acknowledgement
- **Colour:** Green ≥ 90% · Amber 50–89% · Red < 50%
- **Tooltip:** Policy name · Acknowledged: N / N branches · %
- **Export:** PNG

### 6.2 Policy Count by Category (Donut)
- **Type:** Donut
- **Data:** Count of published policies per category
- **Centre text:** Total published policies
- **Tooltip:** Category · Count
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Policy saved as draft | "Policy saved as draft. Submit to CAO for publication." | Info | 4s |
| Policy published | "'[Name]' v[X] published. [N] branches notified." | Success | 4s |
| Policy archived | "'[Name]' archived. Branches notified." | Warning | 6s |
| New version created | "v[X+1] of '[Name]' created as draft. Previous version archived on publish." | Info | 4s |
| Acknowledgement reminder sent | "Reminder sent to [N] branches for '[Name]'" | Success | 4s |
| Export started | "Policy export preparing…" | Info | 4s |
| Branch acknowledged (system) | "[Branch] acknowledged '[Policy Name]'" | Info | — (system log) |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No policies yet | "No academic policies" | "Create your first academic policy to begin governing assessments and promotions consistently" | [+ New Policy] |
| No policies match filters | "No policies match" | "Clear filters to see all policies" | [Clear Filters] |
| No unacknowledged branches | "All branches have acknowledged" | "All branches in scope have acknowledged this policy" | — |
| Version history — single version | "No previous versions" | "This is the first version of this policy" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) |
| Table filter/search/sort/page | Inline skeleton rows |
| Policy create drawer | Spinner → tabbed form |
| Policy view drawer | Spinner → tabs load |
| Version diff modal | Spinner → diff renders |
| Publish confirm submit | Spinner in confirm button |
| Charts load | Skeleton chart areas |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Curriculum Coord G2 | All other Div-B G3 |
|---|---|---|---|---|
| [+ New Policy] | ✅ | ✅ (draft) | ❌ | ❌ |
| Edit draft | ✅ | ✅ (own drafts) | ❌ | ❌ |
| Publish | ✅ | ❌ | ❌ | ❌ |
| Create New Version | ✅ | ✅ (creates draft) | ❌ | ❌ |
| Archive | ✅ | ❌ | ❌ | ❌ |
| Send Acknowledgement Reminder | ✅ | ❌ | ❌ | ❌ |
| View published policies | ✅ | ✅ | ✅ | ✅ |
| View draft policies | ✅ | ✅ (own) | ❌ | ❌ |
| Version diff view | ✅ | ✅ | ❌ | ❌ |
| Branch acknowledgements tab | ✅ | ✅ | ❌ | ❌ |
| Export PDF | ✅ | ✅ | ✅ | ✅ |
| Internal notes field | ✅ | ✅ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/academic-policies/` | JWT | Policy list (role-filtered: status) |
| GET | `/api/v1/group/{group_id}/acad/academic-policies/stats/` | JWT | Stats bar |
| POST | `/api/v1/group/{group_id}/acad/academic-policies/` | JWT (G3 Dir, G4) | Create policy (draft) |
| GET | `/api/v1/group/{group_id}/acad/academic-policies/{id}/` | JWT | Policy detail (current version) |
| PUT | `/api/v1/group/{group_id}/acad/academic-policies/{id}/` | JWT (G3 Dir [draft], G4) | Update draft |
| POST | `/api/v1/group/{group_id}/acad/academic-policies/{id}/publish/` | JWT (G4 CAO) | Publish |
| POST | `/api/v1/group/{group_id}/acad/academic-policies/{id}/archive/` | JWT (G4 CAO) | Archive |
| POST | `/api/v1/group/{group_id}/acad/academic-policies/{id}/new-version/` | JWT (G3 Dir, G4) | Create v+1 as draft |
| GET | `/api/v1/group/{group_id}/acad/academic-policies/{id}/versions/` | JWT (G3+) | Version history |
| GET | `/api/v1/group/{group_id}/acad/academic-policies/{id}/diff/?v1={v}&v2={v}` | JWT (G3+) | Diff any two versions |
| GET | `/api/v1/group/{group_id}/acad/academic-policies/{id}/acknowledgements/` | JWT (G3+) | Acknowledgement status |
| POST | `/api/v1/group/{group_id}/acad/academic-policies/{id}/remind-acknowledgements/` | JWT (G4) | Send reminder to unacknowledged |
| GET | `/api/v1/group/{group_id}/acad/academic-policies/{id}/export-pdf/` | JWT | Download policy PDF |
| GET | `/api/v1/group/{group_id}/acad/academic-policies/export/?format=zip` | JWT | Bulk PDF export |
| GET | `/api/v1/group/{group_id}/acad/academic-policies/charts/acknowledgement-rate/` | JWT | Bar chart |
| GET | `/api/v1/group/{group_id}/acad/academic-policies/charts/count-by-category/` | JWT | Donut chart |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../academic-policies/?q=` | `#policy-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../academic-policies/?filters=` | `#policy-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../academic-policies/?sort=&dir=` | `#policy-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../academic-policies/?page=` | `#policy-table-section` | `innerHTML` |
| Create/Edit drawer | `click` | GET `.../academic-policies/create-form/` | `#drawer-body` | `innerHTML` |
| Save draft submit | `submit` | POST `.../academic-policies/` | `#drawer-body` | `innerHTML` |
| View drawer | `click` | GET `.../academic-policies/{id}/` | `#drawer-body` | `innerHTML` |
| Version history tab | `click` | GET `.../academic-policies/{id}/versions/` | `#policy-versions-container` | `innerHTML` |
| Acknowledgements tab | `click` | GET `.../academic-policies/{id}/acknowledgements/` | `#policy-ack-container` | `innerHTML` |
| Publish confirm | `click` | POST `.../academic-policies/{id}/publish/` | `#policy-row-{id}` | `outerHTML` |
| Archive confirm | `click` | POST `.../academic-policies/{id}/archive/` | `#policy-row-{id}` | `outerHTML` |
| Send reminder | `click` | POST `.../academic-policies/{id}/remind-acknowledgements/` | `#toast-container` | `beforeend` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
