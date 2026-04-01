# 09 — Coach & Sports Staff Registry

> **URL:** `/group/sports/coaches/`
> **File:** `09-coach-staff-registry.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Sports Director G3 (Role 97, full) · Sports Coordinator G3 (Role 98, full manage assignments)

---

## 1. Purpose

Central registry of all coaches and sports support staff across every branch in the group. Each record captures personal profile, sports expertise (multi-sport coaches are common), formal qualifications and certifications (SAI Level, NSNIS, Diploma, Degree, State Certificate), employment type, team assignments, BGV (Background Verification) status, and contract dates. The Sports Director can flag coaching vacancies at specific branches for specific sports and request that HR initiates a hiring process. The Sports Coordinator manages day-to-day assignment changes and tracks certification renewal. Both roles can see BGV status across the group — BGV is non-negotiable for all staff with student contact. Scale: 2–10 coaches per branch × up to 50 branches = up to 500 coach records group-wide. Coaches with expired certifications or BGV failures represent program quality and liability risk; the page surfaces these gaps through alert banners and KPI cards before they affect tournaments or lead to compliance issues.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Sports Director | 97 | G3 | Full CRUD — create, edit, deactivate, flag vacancies, cross-branch reassign | Can flag vacancy and trigger hiring request to HR |
| Sports Coordinator | 98 | G3 | Full — create, edit, manage team assignments | Cannot deactivate or flag vacancy |
| Group Cultural Activities Head | 99 | G3 | View only — all coach records | No create or edit actions; BGV status visible |
| All other roles | — | — | No access | 403 on direct URL |

> **Access enforcement:** `@require_role(['sports_director', 'sports_coordinator', 'cultural_head'])` on read. `@require_role(['sports_director', 'sports_coordinator'])` on create/edit. `@require_role(['sports_director'])` on deactivate and vacancy flag. BGV status field visible to all three roles.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Coach & Sports Staff Registry
```

### 3.2 Page Header
```
Coach & Sports Staff Registry         [+ Add Coach]  [↑ Import Coaches]  [Export ↓]
[N] Total Coaches  ·  [N] Branches Covered  ·  [N] BGV Pending  ·  [N] Contracts Expiring
```

`[+ Add Coach]` — opens `coach-create` drawer (Roles 97, 98).
`[↑ Import Coaches]` — opens 480 px import modal; XLSX template download + file upload; Role 97 only.
`[Export ↓]` — exports filtered coach list to XLSX/PDF.

**Subtitle bar:** No AY selector (coaches are not AY-scoped); page shows all active records plus a toggle to "Include Inactive / Deactivated".

### 3.3 Alert Banners

Stacked above the KPI bar. Each banner dismissible for the session.

| Condition | Banner Text | Severity |
|---|---|---|
| BGV status = Failed for any coach | "[N] coach(es) have a failed BGV. These staff should not have student contact. Immediate review required." | Red |
| BGV pending > 30 days | "[N] coach(es) have had BGV pending for more than 30 days." | Amber |
| Certification expired | "[N] coach(es) have an expired sports certification." | Red |
| Contract expiring within 30 days | "[N] coach contract(s) expire within 30 days. Renew or replace to avoid vacancy." | Amber |
| Branches with zero coaches | "[N] branch(es) have no coach assigned for any sport." | Amber |
| No coaches in registry | "No coaches have been added to the registry. Add the first coach to begin." | Blue |

---

## 4. KPI Summary Bar

Five cards displayed horizontally below the alert banners. Auto-refresh every 5 minutes via HTMX polling (`hx-trigger="every 5m"`).

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Coaches | All active coach records | `Coach.objects.filter(status='active').count()` | Blue (neutral) | `#kpi-total-coaches` |
| 2 | With Team Assignment | Coaches with at least one current team assignment | `Coach.objects.filter(status='active', team_assignments__isnull=False).distinct().count()` | Green if > 50% of total; Amber if 30–50%; Red if < 30% | `#kpi-assigned` |
| 3 | Coaching Vacancies | Branch-sport pairs with no coach assigned | `CoachVacancy.objects.filter(filled=False).count()` | Red if > 0; Green if 0 | `#kpi-vacancies` |
| 4 | BGV Pending | Coaches with BGV status = Pending or Not Started | `Coach.objects.filter(bgv_status__in=['pending','not_started']).count()` | Red if > 5; Amber if 1–5; Green if 0 | `#kpi-bgv-pending` |
| 5 | Contracts Expiring (30d) | Coaches with contract end date within next 30 days | `Coach.objects.filter(contract_end__range=[today, today+30d]).count()` | Red if > 0; Green if 0 | `#kpi-expiring` |

**HTMX:** Each card loads independently via `hx-get` with `hx-trigger="load"` and shows skeleton while loading.

Auto-refresh: `hx-trigger="every 5m"` `hx-get="/api/v1/group/{id}/sports/coaches/kpi/"` `hx-target="#kpi-bar"` `hx-swap="innerHTML"`.

---

## 5. Sections

### 5.1 Coach Registry

**Display note:** Main table below the KPI bar. Shows all active coaches by default. "Include Inactive" toggle in filter bar adds deactivated records (shown with grey row tint).

**Search:** Coach name, sport name, branch name. Debounce 300 ms. Cleared with × icon.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches in group |
| Sport | Multi-select | All sports (dynamic from sport master) |
| Qualification | Multi-select | SAI Level 1 · SAI Level 2 · NSNIS · NIS Diploma · Degree in Physical Education · State Certificate · Other |
| BGV Status | Multi-select | Cleared · Pending · Failed · Not Started |
| Has Team Assignment | Select | Yes · No |
| Contract Status | Multi-select | Active · Expiring (30 days) · Expired |
| Employment Type | Multi-select | Full-Time · Part-Time · Visiting |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Name | Text + link | Yes | Opens `coach-detail` drawer |
| Branch | Text + link | Yes | Primary branch; links to branch page |
| Sports Expertise | Tag list | No | Up to 3 sport tags shown; "+N more" tooltip for additional |
| Qualification | Text | Yes | Abbreviated: "SAI L2", "NSNIS", "B.P.Ed" etc. |
| Teams Assigned | Number + link | Yes | Count of current team assignments; click filters Section 5.1 or opens detail |
| BGV Status | Badge | Yes | Cleared (green) · Pending (yellow) · Failed (red) · Not Started (grey) |
| Contract End Date | Date | Yes | Red text if within 30 days or already expired; "Open-ended" if no end date |
| Joining Date | Date | Yes | |
| Actions | Button group | No | View · Edit · Reassign · Flag Vacancy |

**Action notes:**
- View — always visible; opens `coach-detail` drawer
- Edit — Roles 97 and 98; opens `coach-create` in edit mode
- Reassign — Roles 97 and 98; opens `coach-reassign` modal
- Flag Vacancy — Role 97 only; opens `flag-vacancy` modal for a specific sport at a branch

**Default sort:** Branch name ascending, then Name ascending.

**Pagination:** Server-side · 25 rows per page.

---

### 5.2 Vacancy Flags

**Display note:** Collapsible section shown just above Section 5.1 when the "Vacancies" KPI > 0. Shows all branch-sport pairs with no assigned coach. Header: "Coaching Vacancies — [N] open" with a red badge.

| Column | Type | Notes |
|---|---|---|
| Branch | Text | Branch name |
| Sport | Badge | Sport with no coach |
| Vacancy Since | Date | Date when the last coach was deactivated/reassigned away, or the branch was onboarded with no coach assigned |
| Days Open | Number | Red text if > 30 days |
| Actions | Buttons | [Request Hiring] (Role 97) · [Assign Existing Coach] (Roles 97, 98) |

[Request Hiring] — opens 420 px modal with Branch (pre-filled), Sport (pre-filled), Justification (textarea, required), Urgency (select: Urgent/Normal); submits a notification to HR division.
[Assign Existing Coach] — opens `coach-reassign` modal pre-filled with the vacancy branch and sport.

---

## 6. Drawers & Modals

### Drawer: `coach-create`
- **Trigger:** `[+ Add Coach]` header button, or [Edit] row action
- **Width:** 560 px
- **Tabs:** Profile · Qualifications · Assignment

#### Tab: Profile
| Field | Type | Required | Validation |
|---|---|---|---|
| Full Name | Text | Yes | Min 3, max 100 characters |
| Employee ID | Text | Yes | Alphanumeric, max 20 characters; must be unique within group |
| Branch | Select | Yes | From group branch list |
| Date of Joining | Date | Yes | Must not be in the future |
| Contact Number | Tel | Yes | 10-digit Indian mobile number; unique |
| Email | Email | No | Valid email format |
| Gender | Select | Yes | Male · Female · Other · Prefer Not to Say |
| Date of Birth | Date | Yes | Must be at least 18 years before today |
| Photo | Image upload | No | JPG or PNG; max 2 MB |

#### Tab: Qualifications
| Field | Type | Required | Validation |
|---|---|---|---|
| Sports Expertise | Multi-select | Yes | At least 1 sport from master list |
| Highest Qualification | Select | Yes | SAI NIS Diploma · B.P.Ed · M.P.Ed · Degree in Physical Education · State Board Certificate · Other |
| Certification Name | Text | No | Max 100 characters |
| Issuing Body | Text | No | Max 100 characters |
| Certification Number | Text | No | Max 50 characters |
| Certification Expiry Date | Date | No | Alert shown inline if within 60 days of today |
| Years of Experience | Number | Yes | Integer ≥ 0 |
| Notable Achievements | Textarea | No | Max 500 characters |
| Document Upload | File | No | PDF or JPG/PNG; max 5 files; 10 MB each |

#### Tab: Assignment
| Field | Type | Required | Validation |
|---|---|---|---|
| Assigned Branch | Select (pre-filled from Profile tab) | Yes | |
| Teams Assigned | Multi-select | No | Filtered to teams at the selected branch matching sports expertise |
| Employment Type | Select | Yes | Full-Time · Part-Time · Visiting |
| Contract Start Date | Date | Yes | |
| Contract End Date | Date | No | Must be after Contract Start Date if provided |
| Salary Grade | Text | No | Internal reference; max 20 characters |

---

### Drawer: `coach-detail`
- **Trigger:** Coach Name link in table, or [View] row action
- **Width:** 560 px
- **Tabs:** Profile · Branches & Teams · Achievements

#### Tab: Profile
All profile fields displayed read-only. Certification status card (Valid / Expiring / Expired). BGV status badge with date verified and agency name.

[Edit] button (Role 97, 98) — opens `coach-create` in edit mode.

#### Tab: Branches & Teams
Current assignments table:

| Column | Notes |
|---|---|
| Branch | Branch name |
| Team | Team name + sport badge |
| Since | Date of assignment |
| Status | Active · Ended |

[+ Assign to Branch] button (Role 97, 98) — opens 480 px modal: Branch (select) · Sport (select, filtered to coach expertise) · Teams (multi-select, filtered by branch + sport) · Effective Date (date, required) · Notes (textarea, optional).

#### Tab: Achievements
List of coaching achievements: Tournament wins, state-level players developed, awards received.

Each entry: Year · Achievement Description · Verified (checkbox).

[+ Add Achievement] button (Role 97, 98) — inline form appended below list.

---

### Modal: `coach-reassign`
- **Width:** 420 px
- **Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Current Branch / Team | Display (pre-filled) | — | Read-only |
| New Branch | Select | Yes | From group branch list |
| New Team | Select | Yes | Filtered by new branch and coach sport expertise |
| Effective Date | Date | Yes | Must be today or future |
| Reason | Textarea | Yes | Min 20, max 500 characters |
| Notify Coach | Checkbox | No | Default checked — sends system notification to coach's email |

- **Buttons:** [Confirm Reassignment] (primary) · [Cancel] (ghost)

### Modal: `deactivate-coach`
- **Width:** 420 px
- **Warning note:** "Deactivating [Name] will remove them from [N] active team assignment(s). Reassign those teams before deactivating, or they will be left without a coach."
- **Fields:** Reason (textarea, required, min 20 characters) · Effective Date (date, default today)
- **Buttons:** [Deactivate] (red danger) · [Cancel] (ghost)

---

## 7. Charts

All charts use Chart.js 4.x. Rendered in a two-column grid below the main table. Export as PNG via button on each chart card.

### 7.1 Coach Qualification Distribution
- **Type:** Donut chart
- **Segments:** SAI NIS Diploma · B.P.Ed · M.P.Ed · Degree · State Certificate · Other
- **Centre text:** "[N] Total Coaches"
- **Tooltip:** "[Qualification]: [N] coaches ([X]%)"
- **Export:** PNG

### 7.2 Coach-to-Athlete Ratio Per Branch — Top 10
- **Type:** Horizontal bar chart
- **Data:** Ratio of athletes to coaches per branch; top 10 branches by highest athlete count
- **X-axis:** Ratio value (athletes per coach)
- **Y-axis:** Branch names (sorted descending by ratio)
- **Benchmark line:** Group average ratio shown as vertical dashed line
- **Tooltip:** "[Branch]: [N] athletes / [M] coaches = [ratio]:1"
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Coach created | "Coach [Name] added to registry — assigned to [Branch]." | Success | 4 s |
| Coach updated | "Coach [Name] profile updated." | Success | 4 s |
| Coach deactivated | "[Name] deactivated. [N] team assignment(s) have been unlinked." | Warning | 6 s |
| Coach reassigned | "[Name] reassigned to [New Branch] — [New Team] effective [Date]." | Success | 4 s |
| Branch assignment added | "[Name] assigned to [Branch] — [Sport]." | Info | 4 s |
| Vacancy flagged | "Vacancy flagged for [Sport] at [Branch]. HR notified." | Info | 4 s |
| Validation error | "Please correct the highlighted fields before saving." | Error | 5 s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No coaches in registry | "No coaches registered" | "Add coaches and sports staff to begin building the registry." | [+ Add Coach] |
| No coaches match filters | "No coaches found" | "Try adjusting the branch, sport, or qualification filters." | [Clear Filters] |
| No vacancies (Section 5.2) | "No vacancies flagged" | "All branches have at least one coach assigned per sport." | — |
| No team assignments (Branches & Teams tab) | "No team assignments" | "Assign this coach to a branch team to begin tracking their work." | [+ Assign to Branch] |
| No achievements (Achievements tab) | "No achievements recorded" | "Add coaching achievements to build this coach's professional profile." | [+ Add Achievement] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: KPI bar (5 cards) + alert banners + vacancy section + table (8 rows) + charts |
| Table filter or search change | Inline skeleton rows replacing table body |
| KPI auto-refresh (every 5 min) | Spinner icon on each KPI card |
| Drawer open | Spinner centred in drawer body; tab skeleton after load |
| Photo or document upload | Progress bar below upload field; percentage shown |
| Deactivate confirm | Spinner inside [Deactivate] modal button |
| Hiring request submit | Spinner inside [Request Hiring] modal button |

---

## 11. Role-Based UI Visibility

| Element | Sports Director G3 (97) | Sports Coordinator G3 (98) | Cultural Activities Head G3 (99) |
|---|---|---|---|
| [+ Add Coach] | Visible | Visible | Hidden |
| [↑ Import Coaches] | Visible | Hidden | Hidden |
| [Export ↓] | Visible | Visible | Visible |
| [Edit] row action | Visible | Visible | Hidden |
| [Reassign] row action | Visible | Visible | Hidden |
| [Flag Vacancy] row action | Visible | Hidden | Hidden |
| [Deactivate] action (in drawer) | Visible | Hidden | Hidden |
| [Request Hiring] in vacancy section | Visible | Hidden | Hidden |
| BGV Status field in table and drawer | Visible | Visible | Visible (read-only) |
| Contract details fields in drawer | Visible | Visible | Hidden |
| KPI drill-down links | Visible | Visible | Visible (read-only) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{gid}/sports/coaches/` | JWT (Role 97, 98, 99) | Paginated coach list with filters |
| POST | `/api/v1/group/{gid}/sports/coaches/` | JWT (Role 97, 98) | Create coach profile |
| GET | `/api/v1/group/{gid}/sports/coaches/{cid}/` | JWT (Role 97, 98, 99) | Coach detail |
| PUT | `/api/v1/group/{gid}/sports/coaches/{cid}/` | JWT (Role 97, 98) | Update coach profile |
| POST | `/api/v1/group/{gid}/sports/coaches/{cid}/deactivate/` | JWT (Role 97) | Deactivate coach |
| POST | `/api/v1/group/{gid}/sports/coaches/{cid}/reassign/` | JWT (Role 97, 98) | Reassign to new branch/team |
| GET | `/api/v1/group/{gid}/sports/coaches/{cid}/assignments/` | JWT (Role 97, 98, 99) | All team assignments for coach |
| POST | `/api/v1/group/{gid}/sports/coaches/{cid}/assignments/` | JWT (Role 97, 98) | Add branch assignment |
| DELETE | `/api/v1/group/{gid}/sports/coaches/{cid}/assignments/{aid}/` | JWT (Role 97, 98) | Remove assignment |
| GET | `/api/v1/group/{gid}/sports/coaches/vacancies/` | JWT (Role 97, 98) | Branch-sport pairs with no coach |
| POST | `/api/v1/group/{gid}/sports/coaches/vacancies/{vid}/request-hiring/` | JWT (Role 97) | Flag vacancy and notify HR |
| GET | `/api/v1/group/{gid}/sports/coaches/kpi/` | JWT (Role 97, 98, 99) | KPI card values |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load | `#kpi-bar` container | GET `/api/v1/group/{gid}/sports/coaches/kpi/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"`; skeleton shimmer per card |
| KPI auto-refresh | `#kpi-bar` container | GET `/api/v1/group/{gid}/sports/coaches/kpi/` | `#kpi-bar` | `innerHTML` | `hx-trigger="every 5m"` |
| Coach search | Search input | GET `/api/v1/group/{gid}/sports/coaches/?q={val}` | `#coach-table-body` | `innerHTML` | `hx-trigger="input delay:300ms"` |
| Filter apply | Filter controls | GET `/api/v1/group/{gid}/sports/coaches/?filters={encoded}` | `#coach-table-section` | `innerHTML` | `hx-trigger="change"` |
| Include inactive toggle | Toggle switch | GET `/api/v1/group/{gid}/sports/coaches/?include_inactive={bool}` | `#coach-table-section` | `innerHTML` | `hx-trigger="change"` |
| Pagination | Pagination controls | GET `/api/v1/group/{gid}/sports/coaches/?page={n}` | `#coach-table-section` | `innerHTML` | `hx-trigger="click"` |
| Open coach drawer | Name link / [View] | GET `/api/v1/group/{gid}/sports/coaches/{cid}/drawer/` | `#drawer-body` | `innerHTML` | `hx-trigger="click"` |
| Drawer tab switch | Tab buttons | GET `/api/v1/group/{gid}/sports/coaches/{cid}/{tab}/` | `#drawer-tab-content` | `innerHTML` | `hx-trigger="click"`; lazy-loads tab content |
| Add achievement | Achievement form submit | POST `/api/v1/group/{gid}/sports/coaches/{cid}/achievements/` | `#achievements-list` | `beforeend` | `hx-trigger="submit"`; appends new row |
| Chart 7.1 load | Chart container | GET `/api/v1/group/{gid}/sports/analytics/coach-bgv-status/` | `#chart-bgv-status` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.2 load | Chart container | GET `/api/v1/group/{gid}/sports/analytics/coach-coverage-by-branch/` | `#chart-coach-coverage` | `innerHTML` | `hx-trigger="load"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
