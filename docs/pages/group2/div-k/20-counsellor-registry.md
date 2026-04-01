# 20 — Counsellor Registry

> **URL:** `/group/welfare/counselling/counsellors/`
> **File:** `20-counsellor-registry.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Counselling Head (Role 94, G3)

---

## 1. Purpose

Master registry of all qualified counsellors across all branches — their qualifications, specialisations, registration numbers (RCI — Rehabilitation Council of India, for clinical psychologists; school counsellor certification), branches assigned, session capacity, and current caseload. The Group Counselling Head uses this page to: ensure every branch has at least one qualified counsellor, track certification renewals, match counsellor specialisation to student need (career / academic / mental health / trauma), manage transfers between branches during peak demand, and identify branches that need additional counsellor hiring.

Capacity norms enforced by the system:
- A counsellor assigned to a branch can serve up to **30 individual students** (active caseload) at a time.
- A counsellor can conduct up to **4 group sessions per month** at a branch.
- A branch with > 500 enrolled students must have at least 2 counsellors.

Any branch without a counsellor, any counsellor near or over capacity, and any certification nearing expiry triggers an immediate alert.

Scale: 1–3 counsellors per branch · 20–150 counsellors total across the group.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Counselling Head | G3 | Full — view, add, edit, reassign, track certifications, export | Primary owner |
| Group COO | G4 | View — KPI summary and branches without counsellor; read-only | No edit actions |
| Branch Counsellor | G2 | View own profile only; can update session availability status | Cannot view other counsellors or caseloads |
| Branch Principal | G2 | View — own branch counsellor name, specialisation, and caseload status only | No individual records |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('counselling_head', 'branch_counsellor')` with strict object-level permission for G2 counsellors (own record only).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Counselling  ›  Counsellor Registry
```

### 3.2 Page Header
```
Counsellor Registry                  [+ Add Counsellor]  [Renewal Tracker ↗]  [Export Registry ↓]
[Group Name] — Group Counselling Head · Last updated: [timestamp]
[N] Active Counsellors  ·  [N] Branches Covered  ·  [N] Branches Without Counsellor  ·  Avg Caseload: [N]%
```

### 3.3 Alert Banner (conditional — staffing and compliance gaps)

| Condition | Banner Text | Severity |
|---|---|---|
| Branch has zero counsellors | "[N] branch(es) have no qualified counsellor assigned: [Branch list]. Student welfare risk." | Red |
| Counsellor certification expired | "[N] counsellor(s) have expired RCI/certification: [names]. They cannot practice until renewed." | Red |
| Counsellor over capacity (caseload > 30) | "Counsellor [Name] at [Branch] has [N] individual students on caseload — over the 30-student limit. Redistribute caseload immediately." | Red |
| Certification expiring ≤ 30 days | "[N] counsellor certification(s) expire within 30 days. Renewal required: [names]." | Amber |
| Branch with > 500 students but only 1 counsellor | "[Branch] has [N] enrolled students and only 1 counsellor — a second counsellor is required per policy." | Amber |
| Counsellor near capacity (caseload 27–30) | "Counsellor [Name] at [Branch] is near maximum caseload ([N]/30 students). Prepare to redistribute." | Amber |

Max 5 alerts visible. Alert links route to the relevant counsellor profile or branch entry. "View all counselling compliance events →" shown below alerts.

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Active Counsellors | Count of counsellors with Status = Active | Blue always (informational) | → Main table filtered to Active |
| Branches Without Counsellor | Count of branches with zero assigned active counsellors | Green = 0 · Yellow 1–3 · Red > 3 | → Section 5.2 filtered to no counsellor |
| Certifications Expiring ≤ 30 Days | Counsellors with RCI or certification expiry within 30 days | Green = 0 · Yellow 1–5 · Red > 5 | → Main table sorted by expiry ascending |
| Average Caseload % | Mean of (current individual caseload / 30) × 100 across all active counsellors | Green < 70% · Yellow 70–89% · Red ≥ 90% | → Main table sorted by caseload descending |
| Counsellors Near-Capacity | Count of counsellors with caseload 27–30 students | Green = 0 · Yellow 1–3 · Red > 3 | → Main table filtered to caseload status Near-capacity |
| Counsellors Over Capacity | Count of counsellors with caseload > 30 students | Green = 0 · Red if any | → Main table filtered to caseload > 30 |
| On Leave Currently | Count of counsellors with Status = On Leave | Blue always (informational) | → Main table filtered to On Leave |
| Branches Requiring Extra Counsellor | Branches with > 500 students and fewer than 2 counsellors | Green = 0 · Amber if any | → Section 5.2 |

**HTMX:** `hx-trigger="every 5m"` → Branches Without Counsellor and Counsellors Over Capacity auto-refresh.

---

## 5. Sections

### 5.1 Counsellor Registry Table (Primary Table)

> Full list of all registered counsellors across all branches.

**Search:** Counsellor name, employee ID, certification number, branch name, specialisation. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches (note: a counsellor may appear in multiple branches) |
| Qualification | Checkbox | M.Sc. Counselling / B.Ed. + Counselling Cert / M.Sc. Psychology / PhD / Other |
| Specialisation | Checkbox | Academic / Career / Mental Health / Trauma / Special Needs |
| Certification Status | Radio | All · Valid · Expiring ≤ 30 Days · Expired |
| Caseload Status | Radio | All · Available (< 27 students) · Near-capacity (27–30) · Full (= 30) · Over capacity (> 30) |
| Status | Checkbox | Active / On Leave / Inactive |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Counsellor Name | ✅ | Full name; link → `counsellor-profile` drawer |
| Employee ID | ✅ | System or HR-assigned ID |
| Branch | ✅ | Primary branch; "(+N more)" tooltip if assigned to multiple branches |
| Qualification | ✅ | Highest qualification badge |
| Specialisation | ✅ | Tags: Academic (Blue) · Career (Green) · Mental Health (Purple) · Trauma (Red) · Special Needs (Orange) |
| RCI / Certification No. | ✅ | Registration number |
| Certification Valid Until | ✅ | Date; Red if expired · Orange if ≤ 30 days · Green if > 30 days |
| Current Individual Caseload | ✅ | Number e.g. "18/30"; badge: Available (Green ≤ 26) · Near-capacity (Amber 27–30) · Full (Red = 30) · Over (Dark Red > 30) |
| Monthly Session Capacity | ✅ | "X/4 group sessions this month" |
| Status | ✅ | Active (Green) · On Leave (Amber) · Inactive (Grey) |
| Actions | ❌ | View · Reassign Branch · Edit |

**Default sort:** Certification Valid Until ascending (expired first), then Current Caseload descending.
**Pagination:** Server-side · 25/page.

---

### 5.2 Branch Counsellor Coverage Panel

> Per-branch view of counsellor assignment and compliance with staffing minimums.

**Display:** Table.

**Columns:**
| Column | Notes |
|---|---|
| Branch | Branch name |
| Student Enrolment | Total enrolled students |
| Counsellors Assigned | Count of active counsellors at this branch |
| Required (Policy) | 1 for ≤ 500 students · 2 for > 500 |
| Gap | Required − Assigned; Red if > 0 |
| Total Caseload | Sum of individual caseloads across all counsellors at this branch |
| Avg Caseload % | Mean caseload % across counsellors |
| Specialisation Coverage | List of specialisation tags covered at this branch |
| Coverage Status | Covered (Green) · Understaffed (Red) · At Minimum (Amber) |
| Actions | View Counsellors · Reassign · Request Hire |

**Default sort:** Coverage Status (Understaffed first), then Gap descending.
**Pagination:** Server-side · 25/page.

---

## 6. Drawers / Modals

### 6.1 Drawer: `counsellor-profile`
- **Trigger:** Counsellor name link in Section 5.1 table
- **Width:** 640px
- **Tabs:** Profile · Qualifications · Assignments · Caseload · Sessions · Notes

**Profile tab:**
| Field | Notes |
|---|---|
| Counsellor Name | Read-only |
| Employee ID | Read-only |
| Date of Birth | Read-only |
| Gender | Read-only |
| Contact Number | Phone number |
| Email | Professional email |
| Emergency Contact | Name and phone |
| Status | Active / On Leave / Inactive badge |
| Date of Joining | Date |
| Photo | Profile photo if uploaded |

**Qualifications tab:**
| Field | Notes |
|---|---|
| Highest Qualification | e.g., M.Sc. Counselling Psychology |
| University / Institution | Name |
| Year of Completion | Year |
| RCI Registration Number | Read-only |
| RCI Valid From | Date |
| RCI Valid Until | Date; colour-coded |
| Specialisations | Tags (can be multiple) |
| Additional Certifications | List: Name · Issuing Body · Expiry Date · Status (Valid / Expired) |
| [Upload Certificate] | G3 only — upload PDF/image of any certificate |
| [Set Renewal Reminder] | Toggle per certification — auto-alert 60 days before expiry |

**Assignments tab:**
- Branch assignment history: Branch · Start Date · End Date (or "Current") · Reason for Reassignment
- Current assignments highlighted: Branch name · Caseload at this branch · Group sessions this month
- Paginated if > 10 records

**Caseload tab:**
- Current individual caseload: [N] / 30 students
- Progress bar: Green < 70% · Yellow 70–89% · Red ≥ 90% fill
- List of active individual cases: Student Code [S-XXXX] (anonymised) · Concern Category · First Session Date · Last Session Date · Status (Active / Dormant / Closed)
- Student names visible only to Counselling Head (G3) and the assigned counsellor

**Sessions tab:**
- This month: Individual sessions [N] · Group sessions [N] · Total session hours [N]
- Last 10 sessions: Date · Type · Category · Duration · Outcome badge
- "View all sessions → Counselling Session Register (Page 21)" link

**Notes tab:**
- Internal notes from Counselling Head: Date · Author · Note text
- [+ Add Note] inline form (G3 only)
- Notes are not visible to the counsellor themselves — administrative only

---

### 6.2 Drawer: `add-counsellor`
- **Trigger:** [+ Add Counsellor] button in page header
- **Width:** 600px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Full Name | Text · max 100 chars | Required |
| Employee ID | Text · max 50 chars | Required; uniqueness check |
| Date of Birth | Date picker | Required; must be 23+ years (professional minimum) |
| Gender | Select | Male / Female / Other · Required |
| Contact Number | Text · 10-digit | Required |
| Email | Email field | Required; format validated |
| Primary Branch | Searchable dropdown | Required |
| Additional Branches | Multi-select dropdown | Optional; supports multi-branch assignment |
| Highest Qualification | Select | M.Sc. Counselling / B.Ed. + Counselling Cert / M.Sc. Psychology / PhD / Other · Required |
| University / Institution | Text · max 100 chars | Required |
| Year of Completion | Number · 1970–current year | Required |
| Specialisation(s) | Multi-select checkbox | Academic / Career / Mental Health / Trauma / Special Needs · Required; at least 1 |
| RCI Registration Number | Text · max 50 chars | Required for M.Sc. Psychology / PhD; optional for others; uniqueness check |
| RCI Valid From | Date picker | Conditional: required if RCI number provided |
| RCI Valid Until | Date picker | Conditional: required if RCI number provided; must be future |
| Additional Certifications | Repeater: Name · Issuing Body · Expiry | Optional; add up to 5 |
| Date of Joining | Date picker | Required; cannot be future |
| Annual Leave Entitlement | Number | Required; default 15 |
| Status | Radio | Active (default) / Inactive · Required |

**Footer:** [Cancel] [Save Counsellor →]

---

### 6.3 Drawer: `reassign-branch`
- **Trigger:** "Reassign Branch" action in table row or counsellor-profile Assignments tab
- **Width:** 440px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Counsellor Name | Read-only pre-filled | — |
| Current Branch(es) | Read-only list | — |
| Action | Radio | Add New Branch Assignment / Remove Existing Branch / Transfer (remove all current, assign new) · Required |
| New Branch (for Add / Transfer) | Searchable dropdown | Required for Add/Transfer |
| Branch to Remove (for Remove) | Select (from current branches) | Required for Remove |
| Effective Date | Date picker | Required; cannot be past date |
| Reassignment Reason | Select | Caseload Redistribution / Student Demand at Branch / Counsellor Request / Branch Closure / Disciplinary / Other · Required |
| Reason Details | Textarea · max 300 chars | Required if reason = Other |
| Notify Branch Principal(s) | Toggle | Default: ON — notifies current and new branch principals |
| Notify Counsellor | Toggle | Default: ON |

**Validation:**
- Cannot remove from all branches (must always have at least 1 branch or set to Inactive).
- Transfer removes all current assignments; warn: "This will remove [Name] from [N] current branch(es). Confirm?"

**Footer:** [Cancel] [Save Reassignment →]

---

### 6.4 Drawer: `renewal-tracker`
- **Trigger:** [Renewal Tracker ↗] link in page header
- **Width:** 480px

**Purpose:** Consolidated view of all certifications across all counsellors that are due for renewal in the current year.

**Display:** Sorted table.

**Columns:**
| Column | Notes |
|---|---|
| Counsellor Name | Link → counsellor-profile Qualifications tab |
| Branch | Primary branch |
| Certification Type | RCI / School Counsellor Cert / Other (name) |
| Certification Number | Read-only |
| Expiry Date | Date; colour-coded |
| Days Until Expiry | Number; Red if ≤ 30 · Orange if 31–60 · Green if > 60 |
| Renewal Status | Not Started (Grey) · In Progress (Amber) · Renewed (Green) |
| Actions | Mark In Progress · Mark Renewed · Send Reminder |

**Filters:** Status (Not Started / In Progress / Renewed) · Expiry within N days (30 / 60 / 90 / All Year).

**Summary at top:** "[N] certifications require action this year. [N] expiring within 30 days. [N] already renewed."

**Footer actions:** [Export Renewal List] [Send Bulk Reminders to All Pending]

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Counsellor added | "Counsellor [Name] added and assigned to [Branch]." | Success | 4s |
| Counsellor reassigned | "Counsellor [Name] reassigned to [New Branch] effective [date]." | Success | 4s |
| Certification renewal reminder sent | "Renewal reminder sent to [Name] for [certification type] expiring [date]." | Info | 4s |
| Certification marked renewed | "Certification for [Name] marked as renewed. New expiry: [date]." | Success | 4s |
| Caseload over-capacity alert | "Warning: [Name] at [Branch] now has [N] students on caseload — over the 30-student limit." | Warning | 6s |
| Counsellor status changed to On Leave | "[Name] status changed to On Leave. [Branch] has been notified." | Info | 4s |
| Profile note added | "Note added to [Name]'s profile." | Success | 3s |
| Registry exported | "Counsellor registry export is being prepared. Download will begin shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No counsellors registered | "No Counsellors Registered" | "No counsellors have been added to the registry. Start by adding qualified counsellors for each branch." | [+ Add Counsellor] |
| No results for filter | "No Counsellors Found" | "No counsellors match your selected filters or search terms." | [Clear Filters] |
| All branches have counsellors | "All Branches Covered" | "Every branch has at least one active qualified counsellor assigned." | — |
| No certifications expiring | "All Certifications Valid" | "No counsellor certifications are expiring within the next 30 days." | — |
| No near-capacity counsellors | "All Counsellors Within Capacity" | "All counsellors have caseloads below the near-capacity threshold." | — |
| No renewal tracker items | "No Certifications Due This Year" | "No counsellor certifications are due for renewal in the current year." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + counsellor table (15 rows × 10 columns) + branch coverage panel + alerts |
| Table filter/search | Inline skeleton rows (8 rows × 10 columns) |
| KPI auto-refresh | Shimmer on Branches Without Counsellor and Counsellors Over Capacity card values |
| Counsellor profile drawer open | 640px drawer skeleton with 6-tab bar; each tab loads lazily |
| Caseload tab | Progress bar skeleton + list skeleton (8 rows) |
| Sessions tab | List skeleton (10 rows) |
| Add counsellor form | 600px drawer with 22 field skeletons |
| Reassign branch drawer | 440px drawer with 8 field skeletons |
| Renewal tracker drawer | 480px drawer with table skeleton (10 rows × 7 columns) + summary row |
| Branch coverage panel | Table skeleton (10 rows × 9 columns) |

---

## 10. Role-Based UI Visibility

| Element | Counselling Head G3 | Group COO G4 | Branch Counsellor G2 | Branch Principal G2 |
|---|---|---|---|---|
| View All Counsellors Registry | ✅ | ❌ (KPI + branches no counsellor) | Own profile only | Own branch names only |
| Add Counsellor | ✅ | ❌ | ❌ | ❌ |
| Edit Counsellor Profile | ✅ | ❌ | ❌ | ❌ |
| Reassign Branch | ✅ | ❌ | ❌ | ❌ |
| View Caseload (individual student list) | ✅ (full names) | ❌ | ✅ (own caseload, own codes) | ❌ |
| Upload Certifications | ✅ | ❌ | ❌ | ❌ |
| View Renewal Tracker | ✅ | ❌ | ❌ | ❌ |
| Add Profile Notes | ✅ | ❌ | ❌ | ❌ |
| View Sessions Tab | ✅ | ❌ | ✅ (own sessions) | ❌ |
| Export Registry | ✅ | ✅ (aggregate) | ❌ | ❌ |
| View Branch Coverage Panel | ✅ | ✅ (read-only) | ❌ | ✅ (own branch row) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/counselling/counsellors/` | JWT (G3+) | Counsellor registry table; params: `branch_id`, `qualification`, `specialisation`, `certification_status`, `caseload_status`, `status`, `q`, `page` |
| GET | `/api/v1/group/{group_id}/welfare/counselling/counsellors/kpi-cards/` | JWT (G3+) | KPI auto-refresh payload |
| GET | `/api/v1/group/{group_id}/welfare/counselling/counsellors/branch-coverage/` | JWT (G3+) | Branch counsellor coverage panel |
| GET | `/api/v1/group/{group_id}/welfare/counselling/counsellors/renewal-tracker/` | JWT (G3) | All certifications due for renewal this year |
| GET | `/api/v1/group/{group_id}/welfare/counselling/counsellors/{counsellor_id}/` | JWT (G3, self-G2) | Counsellor profile drawer payload; params: `tab` |
| POST | `/api/v1/group/{group_id}/welfare/counselling/counsellors/` | JWT (G3) | Create new counsellor record |
| PATCH | `/api/v1/group/{group_id}/welfare/counselling/counsellors/{counsellor_id}/` | JWT (G3) | Update counsellor details |
| POST | `/api/v1/group/{group_id}/welfare/counselling/counsellors/{counsellor_id}/reassign/` | JWT (G3) | Reassign counsellor to new/additional branch |
| POST | `/api/v1/group/{group_id}/welfare/counselling/counsellors/{counsellor_id}/certifications/` | JWT (G3) | Add certification record |
| PATCH | `/api/v1/group/{group_id}/welfare/counselling/counsellors/{counsellor_id}/certifications/{cert_id}/` | JWT (G3) | Update certification (mark renewed) |
| POST | `/api/v1/group/{group_id}/welfare/counselling/counsellors/{counsellor_id}/notes/` | JWT (G3) | Add administrative note to profile |
| POST | `/api/v1/group/{group_id}/welfare/counselling/counsellors/renewal-tracker/remind/` | JWT (G3) | Send bulk renewal reminders |
| GET | `/api/v1/group/{group_id}/welfare/counselling/counsellors/export/` | JWT (G3+) | Async export of counsellor registry (CSV/XLSX) |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../counsellors/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Registry table search | `input delay:300ms` | GET `.../counsellors/?q={val}` | `#counsellor-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../counsellors/?{filters}` | `#counsellor-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../counsellors/?page={n}` | `#counsellor-table-section` | `innerHTML` |
| Open counsellor profile drawer | `click` on Counsellor Name | GET `.../counsellors/{id}/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch (lazy) | `click` on tab | GET `.../counsellors/{id}/?tab={name}` | `#drawer-tab-content` | `innerHTML` |
| Add certification submit | `click` | POST `.../counsellors/{id}/certifications/` | `#certifications-list` | `beforeend` |
| Mark certification renewed | `click` | PATCH `.../counsellors/{id}/certifications/{cert_id}/` | `#cert-row-{cert_id}` | `outerHTML` |
| Reassign branch submit | `click` | POST `.../counsellors/{id}/reassign/` | `#assignments-list` | `innerHTML` |
| Add profile note | `click` | POST `.../counsellors/{id}/notes/` | `#notes-list` | `beforeend` |
| Branch coverage panel load | `load` | GET `.../counsellors/branch-coverage/` | `#coverage-panel` | `innerHTML` |
| Renewal tracker load | `load` on drawer open | GET `.../counsellors/renewal-tracker/` | `#renewal-tracker-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
