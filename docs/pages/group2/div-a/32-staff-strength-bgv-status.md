# 32 — Staff Strength & BGV Status

> **URL:** `/group/gov/staff-strength/`
> **File:** `32-staff-strength-bgv-status.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 · MD G5 · CEO G4 · President G4 (Academic staff) · VP G4 (Non-teaching/Ops)

---

## 1. Purpose

Cross-branch staff headcount, role distribution, vacancy tracking, and Background Verification
(BGV) + POCSO compliance monitoring dashboard. Enables the MD and CEO to ensure every branch is
staffed to policy-defined norms, that no unverified staff member is working with students, and
that all POCSO training obligations are met.

This is a dedicated governance view — branch-level HR modules have more granular staff editing;
this page is the group-level read + alert + action layer.

---

## 2. Role Access

| Role | Access | Scope |
|---|---|---|
| Chairman | Full — all data, all actions | All |
| MD | Full — all data, all actions | All |
| CEO | Full — read + send reminders + export | All |
| President | Academic staff only (teaching roles) | Teaching staff |
| VP | Non-teaching / operational staff only | Operations |
| Others | ❌ | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Staff Strength & BGV Status
```

### 3.2 Page Header
```
Staff Strength & BGV Status                            [Export Report ↓]  [Send BGV Reminder]
[N] total staff · [N] branches · Data as of: [date time]
```

### 3.3 Alert Banner (conditional — shown only when triggered)
**Triggered when:** Any branch has BGV-expired staff who are still active.

```
⚠  BGV Compliance Alert — [N] staff members across [N] branches have expired BGV
   and are currently active. Immediate action required.         [View Affected →]
```
Banner colour: Red background (`bg-red-50 border-red-400`). Dismissible per session.

### 3.4 Tabs
```
Headcount Overview  |  BGV Status  |  POCSO Training  |  Vacancies
```

---

## 4. Headcount Overview Tab

### 4.1 Summary Cards (top)

| Card | Value |
|---|---|
| Total Staff | 3,247 |
| Teaching Staff | 2,180 |
| Non-Teaching | 847 |
| Administrative | 220 |
| Vacancies (Open) | 143 |
| New Joins (This Month) | 38 |

### 4.2 Branch Headcount Table

**Search:** Branch name. Debounce 300ms.

**Filters:** Zone · State · Staff Type · Strength Status (Below Norm/At Norm/Above Norm).

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | Branch name + city |
| Zone | Badge | ✅ | |
| Total Staff | Number | ✅ | |
| Teaching | Number | ✅ | |
| Non-Teaching | Number | ✅ | |
| Admin | Number | ✅ | |
| Norm (Teaching) | Number | ✅ | Policy-defined minimum from branch config |
| Strength Status | Badge | ✅ | ✅ At Norm · ⚠ Below Norm · ℹ Above Norm |
| Open Vacancies | Number | ✅ | Red if >0 in critical roles |
| New Joins (Month) | Number | ✅ | |
| Exits (Month) | Number | ✅ | |
| Actions | — | ❌ | [Drill Down] |

**Default sort:** Open Vacancies descending (branches with most gaps first).

**Pagination:** 25/page.

---

## 5. BGV Status Tab

### 5.1 BGV Summary Cards

| Card | Value | Colour |
|---|---|---|
| BGV Verified — All Clear | 2,847 | Green |
| BGV Pending (initiated, not complete) | 287 | Yellow |
| BGV Expired | 68 | Red |
| BGV Not Initiated | 45 | Red |
| BGV Override (manual clearance) | 12 | Orange |

### 5.2 BGV Compliance Table (branch level)

**Search:** Branch name. Debounce 300ms.

**Filters:** Zone · BGV Risk Level (High/Medium/Low) · Has Expired BGV.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| Zone | Badge | ✅ | |
| Total Staff | Number | ✅ | |
| BGV Clear | Number | ✅ | |
| BGV Pending | Number | ✅ | Yellow if >0 |
| BGV Expired | Number | ✅ | Red if >0 |
| Not Initiated | Number | ✅ | Red if >0 |
| BGV % Compliant | Progress bar + % | ✅ | Green ≥95% · Yellow 80–94% · Red <80% |
| Risk Level | Badge | ✅ | 🔴 High · 🟡 Medium · 🟢 Low |
| Actions | — | ❌ | [Drill Down] [Send Reminder] |

**Default sort:** BGV % Compliant ascending (worst first).

**Pagination:** 25/page.

### 5.3 Individual Staff BGV Table (expanded from drill-down)

Accessed via branch drill-down drawer. Shows per-staff BGV status.

**Columns:** Staff Name · Role · Staff Type · BGV Status · BGV Provider · Initiated Date · Completed Date · Expiry Date · Days Until Expiry · Actions ([View Details] [Update Status]).

---

## 6. POCSO Training Tab

### 6.1 POCSO Summary Cards

| Card | Value | Colour |
|---|---|---|
| POCSO Trained — This Year | 2,640 | Green |
| Training Pending (enrolled) | 420 | Yellow |
| Training Not Done | 187 | Red |
| POCSO Training % | 85.6% | Yellow |

### 6.2 POCSO Compliance Table (branch level)

**Search:** Branch name. Debounce 300ms.

**Filters:** Zone · POCSO Compliance % range.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| Zone | Badge | ✅ | |
| Teaching Staff | Number | ✅ | |
| POCSO Trained | Number | ✅ | |
| POCSO Pending | Number | ✅ | |
| Not Done | Number | ✅ | Red if >0 |
| Training % | Progress bar + % | ✅ | Green ≥100% · Yellow 80–99% · Red <80% |
| Last Training Date | Date | ✅ | |
| Next Renewal Due | Date | ✅ | Red if <60 days |
| Actions | — | ❌ | [Drill Down] [Schedule Training] |

**Default sort:** Training % ascending.

**Pagination:** 25/page.

---

## 7. Vacancies Tab

### 7.1 Vacancy Summary Cards

| Card | Value |
|---|---|
| Total Open Positions | 143 |
| Critical Vacancies (Principal/HOD) | 12 |
| Teaching Role Vacancies | 98 |
| Non-Teaching Vacancies | 45 |
| Avg Days Open | 34 days |

### 7.2 Vacancies Table

**Search:** Role, branch name. Debounce 300ms.

**Filters:** Branch · Zone · Role Type · Days Open (>30 / >60 / >90) · Critical Only.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| Zone | Badge | ✅ | |
| Role | Text | ✅ | e.g. "Mathematics Teacher", "Vice Principal" |
| Role Type | Badge | ✅ | Teaching · Non-Teaching · Admin |
| Subject / Area | Text | ✅ | |
| Positions Open | Number | ✅ | |
| Days Open | Number | ✅ | Red if >60 |
| Critical | Badge | ✅ | ⚡ Critical · — |
| Status | Badge | ✅ | Open · Interview in Progress · Offer Made |
| Actions | — | ❌ | [View] [Mark Filled] |

**Default sort:** Critical first → Days Open descending.

**Pagination:** 25/page.

---

## 8. Drawers & Modals

### 8.1 Drawer: `staff-branch-drill`
- **Trigger:** Any tab → [Drill Down] on branch row
- **Width:** 680px
- **Tabs:** Headcount · BGV · POCSO · Vacancies

#### Tab: Headcount
- Branch summary (name, principal, city, total students)
- Staff breakdown by type (teaching/non-teaching/admin) with norm comparison
- Role-level breakdown: PGT/TGT/PRT counts vs required norms
- New joins + exits this month
- Attrition rate (annualised)

#### Tab: BGV
- Per-staff BGV table for this branch
- Columns: Staff ID · Name · Role · BGV Status (badge) · Expiry Date · Days Until Expiry
- [Update BGV Status] per row (Chairman/MD only) → opens `bgv-update` modal
- [Send Reminder to Branch] button (to branch HR/Principal)

#### Tab: POCSO
- Per-staff POCSO status for this branch
- Columns: Staff ID · Name · Role · Training Status · Training Date · Certificate No. · Expiry
- [Schedule Training] for non-trained staff (sends notification to branch)

#### Tab: Vacancies
- Vacancies list for this branch only
- [Mark Filled] per vacancy

---

### 8.2 Modal: `bgv-update`
- **Width:** 480px
- **Trigger:** [Update BGV Status] per staff
- **Fields:**
  | Field | Type | Required |
  |---|---|---|
  | Staff ID | Text | Read-only |
  | Staff Name | Text | Read-only |
  | Current Status | Badge | Read-only |
  | New Status | Select | ✅ | Pending · In Progress · Cleared · Expired · Override — Manual Clearance |
  | BGV Provider | Text | ❌ | |
  | Verification Date | Date | Conditional | Required if Cleared |
  | Expiry Date | Date | Conditional | Required if Cleared |
  | Certificate / Reference No. | Text | ❌ | |
  | Override Reason | Textarea | Conditional | Required if Override — min 50 chars |
  | Notes | Textarea | ❌ | |
- **Buttons:** [Update Status] + [Cancel]
- **Audit:** Every BGV status change logged to Group Audit Log with before/after.

---

### 8.3 Modal: `bgv-bulk-reminder`
- **Trigger:** [Send BGV Reminder] in page header
- **Width:** 480px
- **Content:** Summary of affected staff (N pending, N expired, N not initiated) across N branches
- **Fields:**
  | Field | Type | Required |
  |---|---|---|
  | Send To | Radio | ✅ | Branch Principals (for their staff) · HR Contacts · Both |
  | Channel | Multi-select | ✅ | WhatsApp · Email |
  | Template | Select | ✅ | Standard BGV Reminder · Urgent BGV Notice |
  | Custom Note | Textarea | ❌ | |
- **Buttons:** [Send Reminder] + [Cancel]

---

### 8.4 Modal: `pocso-schedule-training`
- **Width:** 480px
- **Fields:**
  | Field | Type | Required |
  |---|---|---|
  | Branch | Multi-select | ✅ | |
  | Training Mode | Select | ✅ | Online · In-Person · Hybrid |
  | Training Date | Date | ✅ | |
  | Training Provider | Text | ❌ | |
  | Notify Staff | Toggle | ✅ | Default On |
  | Notify Branch Principal | Toggle | ✅ | Default On |
- **Buttons:** [Schedule Training] + [Cancel]

---

### 8.5 Modal: `vacancy-mark-filled`
- **Width:** 380px
- **Fields:** Filled Date (date, required) · Staff Name (text, optional) · Notes (textarea, optional)
- **Buttons:** [Mark Filled] + [Cancel]

---

## 9. Charts

### 9.1 Staff Type Distribution (group-wide)
- **Type:** Donut chart
- **Data:** Teaching vs Non-Teaching vs Admin
- **Export:** PNG

### 9.2 BGV Compliance by Zone
- **Type:** Grouped horizontal bar chart
- **Data:** One row per zone — stacked bars: Cleared / Pending / Expired / Not Initiated
- **Export:** PNG

### 9.3 POCSO Training Progress (branch-wise)
- **Type:** Horizontal bar chart
- **Data:** % trained per branch (sorted ascending)
- **Threshold line:** 100% target
- **Export:** PNG

### 9.4 Headcount Trend (last 12 months)
- **Type:** Line chart
- **Data:** Total staff count per month (this academic year)
- **Separate lines:** Teaching (blue) · Non-Teaching (orange) · Admin (gray)
- **Export:** PNG

### 9.5 Vacancy Age Distribution
- **Type:** Bar chart
- **Data:** Vacancies grouped by age: 0–30d · 31–60d · 61–90d · 90d+
- **Colour:** Green → Yellow → Orange → Red
- **Export:** PNG

---

## 10. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| BGV status updated | "BGV status updated for [Staff Name]" | Success | 4s |
| BGV override recorded | "Manual BGV clearance recorded — audit log updated" | Warning | 6s |
| Reminder sent | "BGV reminder sent to [N] branch principals" | Success | 4s |
| Training scheduled | "POCSO training scheduled for [N] branches on [date]" | Success | 4s |
| Vacancy marked filled | "Vacancy marked filled" | Success | 4s |
| Export started | "Staff report generating…" | Info | Manual |
| Export ready | "Staff report ready — click to download" | Success | Manual |

---

## 11. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No BGV issues | "Full BGV Compliance" | "All active staff have valid BGV clearance" | — |
| No POCSO gaps | "POCSO Training Complete" | "All staff are trained for the current year" | — |
| No vacancies | "No open vacancies" | "All positions are filled across branches" | — |
| No results (filter) | "No staff match" | "Try different filters" | [Clear Filters] |

---

## 12. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: alert banner area + summary cards + table (10 rows) |
| Tab switch | Inline skeleton rows |
| Filter apply | Inline skeleton rows |
| Branch drill-down drawer | Spinner in drawer |
| BGV update modal | Spinner in modal button |
| Chart initial load | Chart skeleton placeholder |
| Export | Spinner in export button |

---

## 13. Role-Based UI Visibility

| Element | Chairman/MD | CEO | President | VP |
|---|---|---|---|---|
| All tabs | ✅ | ✅ | Academic staff only | Non-teaching only |
| Staff names (PII) | ✅ | ✅ | ❌ | ❌ |
| [Update BGV Status] | ✅ | ❌ | ❌ | ❌ |
| [BGV Override] option | Chairman/MD only | ❌ | ❌ | ❌ |
| [Send BGV Reminder] | ✅ | ✅ | ❌ | ❌ |
| [Schedule Training] | ✅ | ✅ | ✅ | ❌ |
| [Mark Vacancy Filled] | ✅ | ✅ | ❌ | ❌ |
| [Export Report] | ✅ | ✅ | ❌ | ❌ |
| Alert Banner | ✅ | ✅ | ❌ | ❌ |
| All charts | ✅ | ✅ | Partial | Partial |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/staff-strength/summary/` | JWT (G4/G5) | Headcount + BGV + POCSO summary |
| GET | `/api/v1/group/{id}/staff-strength/headcount/` | JWT (G4/G5) | Branch headcount table |
| GET | `/api/v1/group/{id}/staff-strength/bgv/` | JWT (G4/G5) | BGV status table |
| GET | `/api/v1/group/{id}/staff-strength/pocso/` | JWT (G4/G5) | POCSO training table |
| GET | `/api/v1/group/{id}/staff-strength/vacancies/` | JWT (G4/G5) | Vacancies table |
| GET | `/api/v1/group/{id}/staff-strength/branch/{bid}/drill/` | JWT (G4/G5) | Branch drill-down |
| PUT | `/api/v1/group/{id}/staff-strength/bgv/{staff_id}/` | JWT (G5) | Update BGV status |
| POST | `/api/v1/group/{id}/staff-strength/bgv/reminder/` | JWT (G4/G5) | Send BGV reminder |
| POST | `/api/v1/group/{id}/staff-strength/pocso/schedule/` | JWT (G4/G5) | Schedule POCSO training |
| PUT | `/api/v1/group/{id}/staff-strength/vacancies/{vid}/fill/` | JWT (G4/G5) | Mark vacancy filled |
| GET | `/api/v1/group/{id}/staff-strength/charts/bgv-by-zone/` | JWT (G4/G5) | BGV zone chart |
| GET | `/api/v1/group/{id}/staff-strength/charts/pocso-progress/` | JWT (G4/G5) | POCSO chart |
| GET | `/api/v1/group/{id}/staff-strength/charts/headcount-trend/` | JWT (G4/G5) | Trend chart |
| GET | `/api/v1/group/{id}/staff-strength/export/` | JWT (G4/G5) | Export staff report |

---

## 15. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | GET `.../staff-strength/?tab=headcount\|bgv\|pocso\|vacancies` | `#staff-tab-content` | `innerHTML` |
| Search (branch) | `input delay:300ms` | GET `.../staff-strength/{tab}/?q=` | `#staff-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../staff-strength/{tab}/?filters=` | `#staff-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../staff-strength/{tab}/?sort=&dir=` | `#staff-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../staff-strength/{tab}/?page=` | `#staff-table-section` | `innerHTML` |
| Open branch drill-down drawer | `click` | GET `.../staff-strength/branch/{bid}/drill/` | `#drawer-body` | `innerHTML` |
| BGV status update (modal confirm) | `click` | PUT `.../staff-strength/bgv/{staff_id}/` | `#bgv-row-{staff_id}` | `outerHTML` |
| Alert strip auto-refresh | `every 5m` | GET `.../staff-strength/summary/` | `#alert-strip` | `innerHTML` |
| Summary cards refresh | `every 5m` | GET `.../staff-strength/summary/` | `#summary-cards` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
