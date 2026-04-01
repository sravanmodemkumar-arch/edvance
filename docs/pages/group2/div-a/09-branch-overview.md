# 09 — Branch Overview

> **URL:** `/group/gov/branches/`
> **File:** `09-branch-overview.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Chairman G5 · MD G5 · CEO G4 (full) · President G4 · VP G4 (view) · Trustee G1 · Advisor G1 (read)

---

## 1. Purpose

Master registry of all branches in the institution group. This is the central operational page
for branch lifecycle management — viewing health metrics, activating/deactivating portals,
and launching the branch onboarding workflow for new branches.

For a large group with 50 branches across 5 states, this page is the single pane of glass for
branch status, performance, and compliance health.

---

## 2. Role Access

| Role | Level | Can View | Can Create | Can Edit | Can Activate/Deactivate |
|---|---|---|---|---|---|
| Chairman | G5 | ✅ All columns | ✅ | ✅ | ✅ |
| MD | G5 | ✅ All columns | ✅ | ✅ | ✅ |
| CEO | G4 | ✅ All columns | ❌ | ✅ (limited) | ✅ |
| President | G4 | ✅ Academic cols only | ❌ | ❌ | ❌ |
| VP | G4 | ✅ Ops cols only | ❌ | ❌ | ❌ |
| Trustee | G1 | ✅ Read-only | ❌ | ❌ | ❌ |
| Advisor | G1 | ✅ Read-only | ❌ | ❌ | ❌ |
| Exec Secretary | G3 | ❌ | ❌ | ❌ | ❌ |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Branch Overview
```

### 3.2 Page Header
```
Branch Overview                                        [+ New Branch]  [Export CSV ↓]
[Group Name] · 50 branches across 5 states            (Chairman/MD only)
```

### 3.3 Summary Stats Bar (top of page, above search)
| Stat | Value |
|---|---|
| Total Branches | 50 |
| Active | 48 |
| Inactive | 2 |
| In Onboarding | 2 |
| Total Students | 82,340 |
| Total Staff | 3,247 |

Stats bar is live — refreshes with page.

---

## 4. Main Branch Table

### 4.1 Search
- Full-text across: Branch Name, City, District, State, Principal Name
- 300ms debounce · Highlights match in Name column

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| State | Multi-select | Andhra Pradesh · Telangana · Karnataka · Maharashtra · Tamil Nadu (group-specific) |
| District | Multi-select | Populated based on State selection |
| Type | Multi-select | Day Scholar Only · Hostel · Both |
| Streams | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · Integrated JEE/NEET |
| Status | Multi-select | Active · Inactive · Onboarding |
| Performance Tier | Select | Top 25% · Mid 50% · Bottom 25% |
| BGV Risk | Checkbox | BGV Compliance <95% only |
| Fee Default | Checkbox | Monthly collection <85% only |
| Hostel | Checkbox | Has hostel only |
| Zone | Multi-select | Zone 1, Zone 2… (large groups only) |

Active filter chips: Dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | All | Row select for bulk actions |
| Branch Name | Text + link | ✅ | All | Opens Branch Detail page 10 |
| Code | Text | ✅ | All | e.g. HYD-04 |
| City / District | Text | ✅ | All | |
| State | Badge | ✅ | All | |
| Type | Badge | ✅ | All | Day · Hostel · Both |
| Streams | Tags | ❌ | All | MPC, BiPC etc. |
| Students | Number | ✅ | All | Total enrolled |
| Day Scholar | Number | ✅ | Chairman/MD/CEO | Enrolled day scholars |
| Hostelers | Number | ✅ | Chairman/MD/CEO | Enrolled hostelers |
| Staff | Number | ✅ | Chairman/MD | Total staff count |
| Fee % | Progress bar + % | ✅ | Chairman/MD/CEO/VP | Monthly collection rate |
| Attendance % | Progress bar + % | ✅ | All | Monthly avg |
| BGV % | Progress bar + % | ✅ | Chairman/MD | Red if <95% |
| POCSO % | Progress bar + % | ✅ | Chairman/MD/CEO | Red if <100% |
| Zone | Text | ✅ | All | Large groups only |
| Principal | Text | ❌ | Chairman/MD/CEO | Principal name |
| Status | Badge | ✅ | All | Active · Inactive · Onboarding |
| Board Affil. | Badge | ✅ | Chairman/MD | CBSE · State Board |
| Last Audit | Date | ✅ | All | Red if >365 days ago |
| Actions | — | ❌ | Role-based | See below |

**Column visibility toggle:** Gear icon top-right — save preference per user.

**Default sort:** Status (Active first), then Branch Name ascending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z branches" · Page jump input.

**Row select:** Checkbox per row + select-all. Shows selected count badge.

### 4.4 Row Actions

| Action | Icon | Visible To | Modal/Drawer | Notes |
|---|---|---|---|---|
| View | Eye | All roles | Opens Branch Detail page 10 | |
| Quick View | Expand | All roles | `branch-quick-view` drawer 560px | Summary without leaving page |
| Edit | Pencil | Chairman, MD, CEO | `branch-edit` drawer 680px | Full branch edit form |
| Activate / Deactivate | Toggle | Chairman, MD, CEO | `branch-activate-confirm` modal | Audited — reason required |
| Delete | Trash | Chairman, MD only | Confirm modal 420px | Soft delete only — never permanent |
| View on Map | Map pin | All | Opens Google Maps with branch address | External link |

### 4.5 Bulk Actions (shown when rows selected)

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (CSV) | All with export access | Exports selected branch rows |
| Deactivate Selected | Chairman, MD | Batch deactivate — requires reason — audited |
| Assign to Zone | Chairman, MD, CEO | Assigns selected branches to a zone |

---

## 5. Drawers & Modals

### 5.1 Drawer: `branch-create` — New Branch
- **Trigger:** [+ New Branch] header button
- **Width:** 680px
- **Tabs:** Profile · Address · Board Affiliation · Principal · Config

#### Tab: Profile
| Field | Type | Required | Validation |
|---|---|---|---|
| Branch Name | Text | ✅ | Min 3 chars, max 100, unique in group |
| Branch Code | Text | ✅ | 3–8 alphanumeric, auto-suggested, unique |
| Branch Type | Select | ✅ | Day Scholar Only · Hostel · Both |
| Streams Offered | Multi-select | ✅ | At least 1 stream |
| Established Year | Year picker | ✅ | 1900 – current year |
| Student Capacity | Number | ✅ | Min 100 |
| Hostel Capacity | Number | Conditional | Required if Type includes Hostel |
| Zone | Select | ❌ | Large groups only — assigns branch to a zone |

#### Tab: Address
| Field | Type | Required | Validation |
|---|---|---|---|
| Address Line 1 | Text | ✅ | Max 200 chars |
| Address Line 2 | Text | ❌ | Max 200 chars |
| City | Text | ✅ | |
| District | Text | ✅ | |
| State | Select | ✅ | Indian states dropdown |
| Pincode | Text | ✅ | 6 digits |
| Google Maps Link | URL | ❌ | Valid URL |
| Latitude / Longitude | Number pair | ❌ | Auto-populated if Maps link given |

#### Tab: Board Affiliation
| Field | Type | Required | Validation |
|---|---|---|---|
| Board | Multi-select | ✅ | CBSE · BSEAP · BSETS · ICSE · State Board |
| Affiliation Number | Text | Conditional | Required per board selected |
| Affiliation Valid Until | Date | Conditional | Future date |
| School Category | Select | ✅ | Primary · Secondary · Senior Secondary |

#### Tab: Principal
| Field | Type | Required | Validation |
|---|---|---|---|
| Assign Principal | Search + select | ✅ | Search from provisioned users, filter by principal role |
| Or Invite New Principal | Button | Conditional | Opens `user-create` flow within drawer |

#### Tab: Config
| Field | Type | Required | Notes |
|---|---|---|---|
| Enable Portal | Toggle | ✅ | On = branch staff can log in |
| Enable Hostel Module | Toggle | Conditional | Shown only if Type = Hostel |
| Enable Transport Module | Toggle | ❌ | |
| WhatsApp Notifications | Toggle | ❌ | |
| Academic Year Start | Date | ✅ | Inherits from group default, overridable |

**Submit:** "Create Branch" — disabled until all required tabs valid (tab icons show red dot if
invalid). Full-page overlay on submit: "Setting up branch portal… This takes ~30 seconds".

**On success:** Branch appears in table · onboarding pipeline triggered automatically.

### 5.2 Drawer: `branch-edit` — Edit Branch
- **Width:** 680px — same tabs as `branch-create`, pre-filled
- **Config tab extra:** Cannot disable portal if branch has active students

### 5.3 Drawer: `branch-quick-view`
- **Trigger:** Eye icon in row actions
- **Width:** 560px
- **Tabs:** Overview · Students · Finance · Health
- **Overview:** Address, principal, streams, status, established year, affiliation
- **Students:** Total enrollment breakdown by type (table: Day Scholar Regular/Scholarship/RTE/Hosteler AC/Non-AC Boys/Girls)
- **Finance:** Current month fee collection, outstanding, last 3 months trend (mini line chart)
- **Health:** BGV % · POCSO % · Last audit date · Open escalations count
- **All read-only** — [Open Full Detail →] button at bottom

### 5.4 Modal: `branch-activate-confirm`
- **Width:** 420px
- **Content:** "You are about to [Activate/Deactivate] [Branch Name]. This action is audited."
- **Fields:** Reason (required, min 20 chars) · Notify principal? (checkbox, default on)
- **Buttons:** [Confirm Deactivate] (danger red) / [Confirm Activate] (primary green) + [Cancel]
- **On confirm:** Status updated · Branch principal notified · MD/Chairman alerted · audit entry

### 5.5 Modal: `branch-delete-confirm`
- **Width:** 420px
- **Content:** "Permanently remove [Branch Name] from the platform?"
- **Warning:** "All data (students, staff, exams, fees) will be archived. This cannot be undone."
- **Fields:** Type branch name to confirm (text match required) · Reason (required, min 50 chars)
- **Buttons:** [Delete Branch] (danger, enabled only when name typed correctly) + [Cancel]

---

## 6. Charts

### 6.1 Enrollment by State (Bubble / Bar)
- **Type:** Horizontal bar chart
- **Data:** Total enrollment per state
- **X-axis:** Student count
- **Y-axis:** State names
- **Tooltip:** State · Total: N · Branches: N
- **Export:** PNG

### 6.2 Branch Performance Matrix (scatter — optional view)
- **Type:** Scatter chart
- **X-axis:** Fee Collection %
- **Y-axis:** Academic Score %
- **Each point:** One branch (labelled with branch code)
- **Quadrants:** Stars (high fee + high score) · Under-served (low fee + high score) · Risk (low both) · Operational (high fee + low score)
- **Tooltip:** Branch name · Fee: X% · Score: X%
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Branch created | "Branch [Name] created. Onboarding pipeline started." | Success | 4s |
| Branch edited | "Branch [Name] updated" | Success | 4s |
| Branch activated | "Branch [Name] portal activated. Principal notified." | Success | 4s |
| Branch deactivated | "Branch [Name] deactivated. Principal and MD notified." | Warning | 6s |
| Branch deleted | "Branch [Name] removed from platform. Data archived." | Warning | 6s |
| Duplicate code | "Branch code already exists. Use a different code." | Error | Manual |
| Export started | "Export preparing… download will start shortly" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches yet | "No branches set up" | "Add your first branch to start managing your institution group" | [+ New Branch] |
| No search results | "No branches match" | "Try different search terms or clear your filters" | [Clear Filters] |
| Filter returns empty | "No branches match your filters" | "Try removing some filters to see more results" | [Clear All Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| branch-create drawer open | Spinner in drawer |
| Branch create submit | Full-page overlay "Setting up branch portal…" |
| Branch activate/deactivate | Spinner in confirm button + overlay after confirm |
| Quick view drawer open | Spinner + skeleton tabs |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | Chairman/MD G5 | CEO G4 | President/VP G4 | Trustee/Advisor G1 |
|---|---|---|---|---|
| [+ New Branch] button | ✅ | ❌ | ❌ | ❌ |
| [Export CSV] button | ✅ | ✅ | ❌ | ❌ |
| Edit row action | ✅ | ✅ (limited) | ❌ | ❌ |
| Activate/Deactivate action | ✅ | ✅ | ❌ | ❌ |
| Delete row action | ✅ | ❌ | ❌ | ❌ |
| Bulk Deactivate | ✅ | ❌ | ❌ | ❌ |
| Staff column | ✅ | ❌ | ❌ | ❌ |
| BGV % column | ✅ | ❌ | ❌ | ❌ |
| Day Scholar / Hosteler columns | ✅ | ✅ | ❌ | ❌ |
| Fee % column | ✅ | ✅ | VP only | ❌ |
| Filter drawer | ✅ | ✅ | ✅ (fewer filters) | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/branches/` | JWT | Branch list (filtered/sorted/paginated) |
| GET | `/api/v1/group/{id}/branches/{bid}/` | JWT | Branch detail |
| POST | `/api/v1/group/{id}/branches/` | JWT (G5) | Create branch |
| PUT | `/api/v1/group/{id}/branches/{bid}/` | JWT (G5/G4) | Update branch |
| DELETE | `/api/v1/group/{id}/branches/{bid}/` | JWT (G5) | Soft delete branch |
| POST | `/api/v1/group/{id}/branches/{bid}/activate/` | JWT (G4+) | Activate/deactivate |
| GET | `/api/v1/group/{id}/branches/{bid}/quick-view/` | JWT | Quick view data |
| GET | `/api/v1/group/{id}/branches/export/?format=csv` | JWT (G5/G4) | Export CSV |
| GET | `/api/v1/group/{id}/branches/stats/` | JWT | Summary stats bar |
| GET | `/api/v1/group/{id}/branches/charts/enrollment-by-state/` | JWT | Chart data |
| GET | `/api/v1/group/{id}/branches/charts/performance-matrix/` | JWT | Scatter chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Branch search | `input delay:300ms` | GET `.../branches/?q=` | `#branch-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../branches/?filters=` | `#branch-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../branches/?sort=&dir=` | `#branch-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../branches/?page=` | `#branch-table-section` | `innerHTML` |
| Quick view | `click` | GET `.../branches/{id}/quick-view/` | `#drawer-body` | `innerHTML` |
| Create drawer open | `click` | GET `.../branches/create-form/` | `#drawer-body` | `innerHTML` |
| Create submit | `submit` | POST `.../branches/` | `#drawer-body` | `innerHTML` |
| Activate/Deactivate confirm | `click` | POST `.../branches/{id}/activate/` | `#branch-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
