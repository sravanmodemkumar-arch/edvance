# 29 — ICC Registry

> **URL:** `/group/welfare/pocso/icc-registry/`
> **File:** `29-icc-registry.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Primary Role:** Group Child Protection Officer (Role 90, G3)

---

## 1. Purpose

The Internal Complaints Committee (ICC) is a legally mandated body under the POCSO Act 2012, Section 4. Every educational institution employing 10 or more persons must constitute an ICC — without exception. The law prescribes an exact composition: (a) a Presiding Officer who must be a senior woman employee, (b) at least 2 other internal members committed to women's causes or possessing legal knowledge, and (c) one external member from a recognised NGO or the legal profession, familiar with issues of sexual harassment. ICC members serve a fixed 3-year term; the external member must receive a nominal fee as specified by the institution. Failure to constitute an ICC is a criminal offence: a first-offence fine of up to ₹50,000, doubling to ₹1,00,000 for repeat non-compliance. The ICC is not optional — it is the institution's first-line legal response mechanism for POCSO-covered complaints.

This page is the group-wide registry and compliance dashboard for ICC composition. The Group Child Protection Officer (CPO) uses it to: register each branch's ICC at the time of constitution or reconstitution; track the 3-year term cycle for every member; verify legal composition compliance on an ongoing basis (correct gender for the Presiding Officer, mandatory external member present, minimum headcount met); record annual ICC member sensitisation training as mandated by the Ministry of Women and Child Development; and generate documentary evidence of compliance for regulatory inspection by the NCPCR, District Education Officer, or state authority. The registry also maintains an immutable term history for every branch so that reconstitutions are fully auditable over time. Scale: 20–50 branches · 3–5 ICC members per branch · 60–250 ICC members total · 3-year term cycle with rolling renewals.

This page was identified as missing in the 15-pass audit. Page 01 (Child Protection Officer Dashboard) includes a "View ICC Registry" quick action that links to this URL. Without this page, the CPO has no centralised mechanism to track ICC constitution status, detect expired terms, or demonstrate legal compliance across the group — making it critical for POCSO regulatory adherence.

---

## 2. Role Access

| Role | Level | Access | Django Decorator |
|---|---|---|---|
| Group Child Protection Officer | G3, Role 90 | Full — view all branches, constitute/reconstitute ICC, record training, send renewal reminders, export | `@require_role([90])` |
| Group CEO | G4 | Read-only — compliance matrix, KPI bar, alert banners; no edit or constitution actions | `@require_role([90, 'ceo'], read_only_for=['ceo'])` |
| Group POCSO Coordinator | G3, Role 50 | Read-only — compliance matrix and member list; no edit actions | `@require_role([90, 50], read_only_for=[50])` |
| Branch Principal | Branch | Read-only — own branch ICC composition only; cannot see other branches; no edit | `@require_role_branch(['principal'])` with branch queryset filter |
| All other roles | — | No access — 403 redirect | — |

> **Access enforcement:** The main queryset is always scoped by `group_id` from the URL. Branch Principals receive a queryset filtered to `branch=request.user.branch` — they see one row in the compliance matrix and one ICC composition. ICC member data (names, designations) is not sensitive but is still gated to Role 90, Role 50, and the relevant Branch Principal. Every constitution or reconstitution action is logged to the `icc_constitution_audit` table: `{user_id, branch_id, action, timestamp, ip_address}`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  POCSO  ›  ICC Registry
```

### 3.2 Page Header
- **Title:** `ICC Registry — Internal Complaints Committee`
- **Subtitle:** `[N] Branches · [N] Valid ICC · [N] Non-Compliant · [N] Members Total · Last updated: [timestamp]`
- **Right controls:** `+ Constitute / Reconstitute ICC` (Role 90 only) · `Record Training` (Role 90 only) · `Send Renewal Reminder` (Role 90 only) · `Export Compliance Report` (Role 90 + CEO)

### 3.3 Alert Banner

Banners are shown in priority order — Red first, then Amber. Maximum 5 banners displayed; "Show all alerts →" link below if more exist.

| Condition | Banner Text | Severity |
|---|---|---|
| Branch ICC fully expired (all member terms lapsed) | "ICC at [Branch Name] has fully expired — all member terms have lapsed. Re-constitute immediately. This is a POCSO Act non-compliance." | Red |
| External member missing from any branch | "ICC at [N] branch(es) does not include a mandatory external NGO/legal member. This is a violation of POCSO Act Section 4." | Red |
| Presiding Officer is not female | "ICC at [N] branch(es) has a Presiding Officer who is not a woman. This violates POCSO Act Section 4(1)(a). Reconstitution required." | Red |
| ICC below minimum member count (< 3 members) | "ICC at [N] branch(es) has fewer than 3 members. POCSO minimum composition requirement not met." | Red |
| Member term expiring within 14 days | "[N] ICC member term(s) expiring within 14 days across [M] branch(es). Initiate reconstitution before expiry to avoid a compliance gap." | Amber |
| Annual sensitisation training not completed this year | "[N] ICC member(s) at [M] branch(es) have not completed their mandatory annual sensitisation training for [current year]." | Amber |

---

## 4. KPI Summary Bar

Eight cards arranged in a responsive 4×2 grid. All metrics are group-wide by default; Branch Principals see own-branch metrics only. Each card that shows a non-zero count for a compliance failure is clickable and drills down to the filtered compliance matrix.

| # | Card Title | Metric | Colour Rule | Drill-down |
|---|---|---|---|---|
| 1 | Branches with Valid ICC | Branches where all legal requirements met (female PO + external member + ≥ 3 members + no expired terms) / total branches | Green = 100% · Amber 80–99% · Red < 80% | → Compliance matrix filtered to Status = Valid |
| 2 | ICC Members with Expired Terms | Count of individual members whose `term_expiry < today` and status = Active | Green = 0 · Red ≥ 1 | → Members Due for Renewal table |
| 3 | Branches with ICC Expiring in 30 Days | Branches where at least one member's term expires within 30 days | Green = 0 · Amber ≥ 1 | → Compliance matrix filtered to earliest expiry ≤ today+30 |
| 4 | Branches Missing External Member | Branches with no active external member on the ICC | Green = 0 · Red ≥ 1 | → Compliance matrix filtered to External Member = No |
| 5 | Branches Missing Female Presiding Officer | Branches where PO gender ≠ Female or PO slot is vacant | Green = 0 · Red ≥ 1 | → Compliance matrix filtered to PO Compliance = Fail |
| 6 | ICC Members Trained This Year % | (Members who completed annual sensitisation training in current calendar year / total active members) × 100 | Green = 100% · Amber 80–99% · Red < 80% | → Branch detail drawer → Training tab |
| 7 | Total ICC Members (Group-wide) | Count of all members with status = Active across all branches | Blue always (informational) | → Full member directory |
| 8 | Reconstitutions Required This Month | Branches where any member's term expired this calendar month and no reconstitution has been recorded | Green = 0 · Amber ≥ 1 | → Compliance matrix filtered to reconstitution overdue |

---

## 5. Sections

### 5.1 Branch ICC Compliance Matrix

One row per branch. The primary compliance view for the CPO.

**Search:** Free-text on branch name. 300ms debounce. Minimum 2 characters.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| ICC Status | Checkbox | Valid · Partial · Non-Compliant · Expired |
| External Member | Radio | All · Present · Missing |
| Presiding Officer Gender | Radio | All · Compliant (Female) · Non-Compliant |
| Training Compliance | Radio | All · Fully Trained · Partially Trained · Not Trained |
| Term Expiry Within | Single-select | Any · 14 days · 30 days · 60 days |
| Reconstitution Overdue | Toggle | Off / On |
| Branch | Multi-select | All branches (populated from DB) |

**Table Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Branch short name; click opens `branch-icc-detail` drawer |
| ICC Status | ✅ | Valid (Green) · Partial (Amber) · Non-Compliant (Red) · Expired (Dark Red) badge. Valid = female PO + external member + ≥ 3 members + no expired terms |
| Presiding Officer | ✅ | Name + Gender badge (Female = Green · Male/Unknown = Red). "Vacant" in red if no PO assigned |
| External Member | ✅ | Yes (Green) · No (Red). Hover shows member name and NGO/legal affiliation |
| Members Count | ✅ | Integer; Red if < 3; Amber if = 3 (legal minimum); Green if > 3 |
| Earliest Term Expiry | ✅ | Date of the soonest-expiring active member's term; Red if past; Amber if ≤ 30 days |
| Training Compliance % | ✅ | % of active ICC members who completed annual sensitisation training this year; Red < 100%; Green = 100% |
| Last Reconstitution Date | ✅ | DD-MMM-YYYY; "Not on Record" in grey if no reconstitution recorded |
| Actions | ❌ | View · Reconstitute · Record Training · Remind |

**Default sort:** ICC Status (Non-Compliant / Expired first, then Partial, then Valid), then Branch alphabetically.
**Pagination:** Server-side · 25 rows/page.
**Row highlight:** Non-Compliant and Expired rows have a red left border (2px). Partial rows have an amber left border.

---

### 5.2 ICC Compliance Trend Chart

A time-series visualisation showing compliance health across the group over the past 12 months.

- **Primary series (bars):** % of branches with a Valid ICC per month (left Y-axis, 0–100%).
- **Overlay line:** Count of branches with a missing external member (right Y-axis, integer).
- **X-axis:** Month labels (Jan–Dec or rolling 12 months from current month).
- **Tooltip:** Month · Valid ICC % · Branches missing external member count.
- **Data source:** `GET /api/v1/group/{group_id}/welfare/pocso/icc/compliance-trend/`
- **Interaction:** Clicking a bar filters the compliance matrix to that month's snapshot. HTMX loads chart data on `hx-trigger="load"`.

---

### 5.3 Members Due for Renewal

A dedicated sub-section listing all individual ICC members whose terms expire within 60 days, across all branches. Purpose: proactive action before any gap in legal composition.

**Search:** Member name, branch name. 300ms debounce.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Days Until Expiry | Range | 0 – 60 (default: 0–60) |
| Member Type | Checkbox | Internal · External · NGO |
| Training This Year | Radio | All · Trained · Not Trained |

**Table Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Member Name | ✅ | Full name |
| Branch | ✅ | |
| Designation | ✅ | |
| Member Type | ✅ | Internal (Blue) · External/NGO (Purple) · Legal External (Teal) badge |
| Role in ICC | ✅ | Presiding Officer · Member · External Member |
| Term Expiry | ✅ | DD-MMM-YYYY; Red if ≤ 14 days; Amber if 15–30 days; Yellow if 31–60 days |
| Days Remaining | ✅ | Integer countdown; colour matches Term Expiry |
| Training This Year | ✅ | Trained ✅ / Not Trained ❌ |
| Actions | ❌ | View Branch ICC · Send Reminder |

**Default sort:** Days Remaining ascending (most urgent first).
**Pagination:** Server-side · 25 rows/page.

---

## 6. Drawers / Modals

### 6.1 Drawer — `branch-icc-detail` (680px, right side)

**Trigger:** Click on branch name in compliance matrix or "View" in Actions column.

**Header:** Branch Name · ICC Status badge · Members Count · Earliest Expiry date

**Tabs:**

#### Tab 1 — Current Members

Table of all members on the current ICC constitution:

| Column | Notes |
|---|---|
| Name | Full name |
| Designation | Job title at the institution |
| Gender | Female (Green badge) · Male (Grey badge) · Not Specified |
| Role in ICC | Presiding Officer · Member · External Member |
| Type | Internal · External NGO · External Legal |
| Employee ID / External Flag | Employee ID for internal members; "External" badge for NGO/Legal members |
| Appointed Date | DD-MMM-YYYY |
| Term Expiry | DD-MMM-YYYY; Red if expired; Amber if ≤ 30 days |
| Training Status | Trained ✅ / Not Trained ❌ (for current calendar year) |
| Status | Active (Green) · Expired (Red) · Resigned (Grey) badge |

**Footer:** `+ Add Member` (Role 90 only) · `Reconstitute ICC` (Role 90 only)

#### Tab 2 — Term History

Immutable audit trail of all past ICC constitutions for this branch.

| Column | Notes |
|---|---|
| Constitution Number | Sequential (ICC-001, ICC-002, …) |
| Constitution Date | DD-MMM-YYYY |
| Constitution Type | Fresh · Reconstitution · Addition of Member · Removal |
| Members at Constitution | Comma-separated names with roles |
| Term Period | From – To (3-year span) |
| Recorded By | User name + Role |
| Recorded On | Timestamp |

All rows are read-only. Deletion is disabled. This is a permanent audit record. Hover on any row shows full member list in a tooltip.

#### Tab 3 — Training

Annual training records for ICC members at this branch.

| Column | Notes |
|---|---|
| Training Date | DD-MMM-YYYY |
| Calendar Year | Auto-derived from date |
| Trainer Name | Name of trainer / facilitating body |
| Training Mode | In-Person · Online · Hybrid |
| Duration (hours) | |
| Attendees | Member names who attended (from this branch's ICC) |
| Non-Attendees | Members who did not attend (automatically calculated) |
| Recorded By | |

**Footer:** `+ Record Training Session` (Role 90 only)

#### Tab 4 — POCSO Complaints Handled

A privacy-respecting count view only — no complaint details are exposed here.

| Field | Value |
|---|---|
| Total Complaints Assigned to This ICC | Count (integer) |
| Complaints This Academic Year | Count (integer) |
| Open / Pending Complaints | Count (integer) |
| Closed Complaints | Count (integer) |

> Note: Complaint details (names, descriptions, stage) are available only in the POCSO Complaint Register (page 08). This tab shows counts only to contextualise the ICC's workload without breaching confidentiality of individual cases.

#### Tab 5 — Reconstitution Log

Detailed log of each reconstitution event for this branch — distinct from Term History which shows the constitution state, this log shows the events and reasons.

| Column | Notes |
|---|---|
| Date | DD-MMM-YYYY |
| Reason | Term Expired · Member Resignation · Member Departure · Court Order · Initial Constitution |
| New Composition Summary | Count of members, PO name, external member name |
| Notified To | Branch Principal · District Authority · NCPCR (if required) |
| Notification Date | DD-MMM-YYYY or "Pending" |
| Action Taken By | User name + Role |

---

### 6.2 Drawer — `constitute-icc` (680px, right side)

**Trigger:** `+ Constitute / Reconstitute ICC` page header button, or "Reconstitute" in branch Actions column. Role 90 only.

**Header:** "Constitute / Reconstitute ICC — [Branch Name if pre-selected]"

**Fields:**

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select dropdown (all branches) | Required; auto-set if triggered from branch row |
| Constitution Date | Date picker | Required; cannot be future date |
| Constitution Type | Radio: Fresh · Reconstitution · Addition of Member · Removal | Required |
| Reason (if Reconstitution / Addition / Removal) | Textarea (max 500 chars) | Required if type ≠ Fresh |
| Prior ICC Reference | Read-only auto-fill (shows last constitution record for selected branch) | Auto |

**Members Block (repeating — minimum 3 entries required):**

Each member row contains:

| Sub-Field | Type | Validation |
|---|---|---|
| Name | Text input | Required |
| Designation | Text input | Required |
| Gender | Radio: Female · Male · Other | Required |
| Employee ID | Text input | Required if Type = Internal; leave blank for external |
| External Flag | Checkbox: "External member (NGO / Legal)" | If checked, Employee ID field is hidden |
| Type | Select: Internal · External NGO · External Legal | Required |
| Role in ICC | Select: Presiding Officer · Member · External Member | Required |
| Appointed Date | Date picker (defaults to Constitution Date) | Required |
| Term Expiry | Date picker — calculated as Constitution Date + 3 years; editable | Required; must be ≥ Constitution Date + 1 year |

`+ Add Another Member` button appends a new repeating member row.
`Remove` button on each row (minimum 3 rows enforced — cannot remove below 3).

**Composition Validation Panel** (live, shown below the member block):

This panel re-evaluates on every member row change and shows compliance status in real time:

| Check | Status |
|---|---|
| Presiding Officer assigned | ✅ / ❌ |
| Presiding Officer is Female | ✅ / ❌ |
| External member present | ✅ / ❌ |
| Minimum 3 members | ✅ / ❌ |

If any check is ❌, the Save button shows a warning dialog: "This ICC constitution does not meet all POCSO Act Section 4 requirements. Are you sure you want to save? You can continue and fix the composition later, but the branch will be marked Non-Compliant until resolved."

**Footer:** `Cancel` · `Save Constitution` (disabled until Branch field and at least 3 member rows are complete; shows inline spinner on click)

**Behaviour on save:** New ICC constitution record created; compliance matrix row for the branch is recalculated immediately; audit log entry written; toast shows success.

---

### 6.3 Drawer — `record-training` (460px, right side)

**Trigger:** "Record Training" page header button, or "Record Training" in branch Actions column, or `+ Record Training Session` in Tab 3 footer.

**Header:** "Record ICC Sensitisation Training — [Branch Name if pre-selected]"

**Fields:**

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select | Required; auto-set if triggered from branch row |
| Training Date | Date picker | Required; cannot be future date |
| Calendar Year | Read-only auto-derived from Training Date | Auto |
| Trainer Name | Text input (max 200 chars) | Required |
| Trainer Organisation / Designation | Text input (max 200 chars) | Optional |
| Training Mode | Radio: In-Person · Online · Hybrid | Required |
| Duration (hours) | Number input (0.5 – 8.0) | Required |
| Topics Covered | Textarea (max 800 chars) | Required |
| Attendees | Multi-select from this branch's active ICC members | Required; at least 1 member |

**Footer:** `Cancel` · `Save Training Record`

**Behaviour on save:** Training record created; training compliance % for the branch recalculates; KPI Card 6 re-evaluates; if all members now trained, branch training status turns Green; toast shows success.

---

### 6.4 Drawer — `send-renewal-reminder` (400px, right side)

**Trigger:** "Remind" in compliance matrix Actions column, or "Send Reminder" in Members Due for Renewal table.

**Header:** "Send ICC Reconstitution Reminder — [Branch Name]"

**Fields:**

| Field | Type | Validation |
|---|---|---|
| Branch | Read-only (pre-set from trigger context) | Auto |
| Recipient | Radio: Branch Principal · Branch POCSO Nodal Officer · Both | Required |
| Expiring Members | Read-only list (name, role, expiry date) — auto-populated from branch data | Auto |
| Reminder Message | Textarea (max 1,000 chars) — pre-filled with a standard template; editable | Required |
| Urgency | Radio: Routine · Urgent (term expires < 14 days) · Critical (term already expired) — auto-suggested based on data | Required |
| Send Via | Checkbox group: Portal Notification · Email | Required; at least one |

**Pre-filled message template:**
> "This is a reminder that the ICC term(s) at [Branch] will expire on [date(s)]. Please initiate the reconstitution process in accordance with POCSO Act 2012, Section 4, before the expiry date to avoid a compliance gap. Contact the Group Child Protection Officer for guidance."

**Footer:** `Cancel` · `Send Reminder`

**Behaviour on save:** Notification dispatched to selected recipients via chosen channels; reminder logged with timestamp in the reconstitution log for the branch; toast shows success.

---

## 7. Toast Messages

| Action | Toast Text | Type | Duration |
|---|---|---|---|
| ICC constitution saved | "ICC constitution recorded for [Branch]. Compliance status updated." | Success | 4s |
| ICC saved with composition warnings | "ICC for [Branch] saved with warnings — branch is marked Non-Compliant until composition is corrected." | Warning | 8s |
| Member added to ICC | "Member [Name] added to ICC at [Branch]. Term set to [expiry date]." | Success | 4s |
| Training record saved | "ICC sensitisation training recorded for [Branch] on [date]. [N] members marked as trained." | Success | 4s |
| Renewal reminder sent | "Reconstitution reminder sent to [Recipient(s)] for [Branch]." | Success | 4s |
| Compliance matrix refreshed | "Compliance data refreshed for all [N] branches." | Info | 3s |
| Export triggered | "Compliance report export is being prepared. Download will begin shortly." | Info | 3s |
| Validation error — missing PO | "A Presiding Officer must be designated before saving this ICC constitution." | Error | 6s |
| Validation error — no external member | "At least one External (NGO/Legal) member is required. Add an external member before saving." | Error | 6s |
| Validation error — insufficient members | "An ICC must have at least 3 members. Please add more members before saving." | Error | 6s |
| Validation error — PO gender | "The Presiding Officer must be a woman as required by POCSO Act Section 4. Please correct the gender field." | Error | 6s |

---

## 8. Empty States

| Context | Heading | Description | CTA |
|---|---|---|---|
| No ICC registered for any branch | "No ICC Records Found" | "No ICC constitutions have been recorded for any branch. Register each branch's ICC to begin tracking POCSO compliance." | `+ Constitute ICC` button (Role 90 only) |
| No branches match current filters | "No Branches Match Filters" | "Try adjusting or clearing your filters to see ICC records." | `Clear Filters` button |
| Members Due for Renewal — no members in 60-day window | "No Renewals Due in the Next 60 Days" | "All ICC member terms are valid for more than 60 days. Review the compliance matrix for the full term schedule." | — |
| Branch ICC detail — Tab 1, no active members | "No Active Members on Record" | "This branch has no active ICC members recorded. Please record a constitution to add members." | `Reconstitute ICC` button (Role 90 only) |
| Branch ICC detail — Tab 3, no training records | "No Training Records" | "No sensitisation training has been recorded for this branch's ICC. Record the annual training to complete compliance." | `+ Record Training Session` button (Role 90 only) |
| Branch ICC detail — Tab 5, no reconstitution events | "No Reconstitution Events" | "No reconstitution events have been logged for this branch. The initial constitution will appear here once recorded." | — |
| Compliance Trend Chart — insufficient data | "Not Enough Data for Trend" | "Trend data will appear once ICC records have been registered for at least 2 months." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 8 KPI cards (grey shimmer) + compliance matrix (10 grey rows × 9 columns) + trend chart (grey rectangle, 280px tall) + members renewal table (5 grey rows) |
| Filter / search apply | Table body spinner overlay on compliance matrix; KPI cards shimmer and refresh after table settles |
| Compliance trend chart load | Chart area shows grey rectangle with shimmer gradient until HTMX response arrives |
| Branch ICC detail drawer open | Drawer slides in with skeleton: tab bar + 8 grey field blocks in the current tab |
| Current Members tab load | Table skeleton: 5 grey rows × 9 columns |
| Term History tab load | Table skeleton: 4 grey rows × 6 columns |
| Training tab load | Table skeleton: 3 grey rows × 6 columns |
| POCSO Complaints Handled tab load | 4 grey stat blocks (count cards) |
| Reconstitution Log tab load | Table skeleton: 4 grey rows × 6 columns |
| Constitute ICC form submit | Save button disabled + spinner + "Saving…" label; composition validation panel shows spinner while re-calculating |
| Record training form submit | Save button disabled + spinner + "Recording…" label |
| Send reminder form submit | Send button disabled + spinner + "Sending…" label |
| Export triggered | Export button disabled + spinner until file is prepared |
| KPI bar auto-refresh | Individual card values shimmer (not full card skeleton) |

---

## 10. Role-Based UI Visibility

| UI Element | Role 90 (CPO) | Group CEO | Role 50 (POCSO Coord.) | Branch Principal | All Others |
|---|---|---|---|---|---|
| Full compliance matrix (all branches) | ✅ | ✅ | ✅ | Own branch only | ❌ |
| KPI Summary Bar | Full detail | Full detail | Full detail | Own branch metrics | ❌ |
| Alert banners | Full detail | Full detail | Full detail | Own branch only | ❌ |
| Compliance Trend Chart | ✅ | ✅ | ✅ | ❌ | ❌ |
| Members Due for Renewal section | ✅ | ✅ | ✅ | Own branch members | ❌ |
| `+ Constitute / Reconstitute ICC` button | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Record Training` button | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Send Renewal Reminder` button | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Export Compliance Report` button | ✅ | ✅ | ❌ | ❌ | ❌ |
| Branch ICC detail drawer — View | ✅ | ✅ | ✅ | Own branch only | ❌ |
| Tab 1 Current Members — `+ Add Member` | ✅ | ❌ | ❌ | ❌ | ❌ |
| Tab 1 Current Members — `Reconstitute ICC` | ✅ | ❌ | ❌ | ❌ | ❌ |
| Tab 2 Term History | ✅ (read-only) | ✅ (read-only) | ✅ (read-only) | Own branch (read-only) | ❌ |
| Tab 3 Training — `+ Record Training` | ✅ | ❌ | ❌ | ❌ | ❌ |
| Tab 4 POCSO Complaints Handled (counts) | ✅ | ✅ | ✅ | Own branch | ❌ |
| Tab 5 Reconstitution Log | ✅ | ✅ | ✅ | Own branch | ❌ |
| Actions column — Reconstitute | ✅ | ❌ | ❌ | ❌ | ❌ |
| Actions column — Record Training | ✅ | ❌ | ❌ | ❌ | ❌ |
| Actions column — Remind | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

**Base URL:** `/api/v1/group/{group_id}/welfare/pocso/icc/`

All endpoints require JWT authentication. Role-scoping is enforced server-side on every request.

| Method | Endpoint | Description | Auth / Role |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/pocso/icc/` | List all branch ICC records (compliance matrix) — paginated, filtered, role-scoped | JWT; Role 90, CEO, Role 50, Branch Principal (scoped) |
| GET | `/api/v1/group/{group_id}/welfare/pocso/icc/kpi/` | KPI summary bar data for all 8 cards | JWT; Role 90, CEO, Role 50, Branch Principal (scoped) |
| GET | `/api/v1/group/{group_id}/welfare/pocso/icc/alerts/` | Active alert banner conditions | JWT; Role 90, CEO, Role 50, Branch Principal (scoped) |
| GET | `/api/v1/group/{group_id}/welfare/pocso/icc/compliance-trend/` | 12-month compliance trend chart data | JWT; Role 90, CEO, Role 50 |
| GET | `/api/v1/group/{group_id}/welfare/pocso/icc/members/renewal/` | Members due for renewal within 60 days | JWT; Role 90, CEO, Role 50, Branch Principal (scoped) |
| GET | `/api/v1/group/{group_id}/welfare/pocso/icc/{branch_id}/` | Branch ICC detail — current members, composition status | JWT; Role 90, CEO, Role 50, Branch Principal (own) |
| GET | `/api/v1/group/{group_id}/welfare/pocso/icc/{branch_id}/term-history/` | All past constitutions for a branch (immutable) | JWT; Role 90, CEO, Role 50, Branch Principal (own) |
| GET | `/api/v1/group/{group_id}/welfare/pocso/icc/{branch_id}/training/` | Training records for a branch's ICC | JWT; Role 90, CEO, Role 50, Branch Principal (own) |
| GET | `/api/v1/group/{group_id}/welfare/pocso/icc/{branch_id}/complaint-counts/` | Count of POCSO complaints handled by this ICC (no details) | JWT; Role 90, CEO, Role 50, Branch Principal (own) |
| GET | `/api/v1/group/{group_id}/welfare/pocso/icc/{branch_id}/reconstitution-log/` | Reconstitution event log for a branch | JWT; Role 90, CEO, Role 50, Branch Principal (own) |
| POST | `/api/v1/group/{group_id}/welfare/pocso/icc/constitute/` | Create a new ICC constitution or reconstitution | JWT; Role 90 only |
| PATCH | `/api/v1/group/{group_id}/welfare/pocso/icc/{branch_id}/members/{member_id}/` | Update a single member record (status change, term correction) | JWT; Role 90 only |
| POST | `/api/v1/group/{group_id}/welfare/pocso/icc/{branch_id}/training/` | Record a training session | JWT; Role 90 only |
| POST | `/api/v1/group/{group_id}/welfare/pocso/icc/{branch_id}/reminders/` | Send renewal reminder to branch | JWT; Role 90 only |
| GET | `/api/v1/group/{group_id}/welfare/pocso/icc/export/` | Export compliance report (all branches, all fields) | JWT; Role 90, CEO |

**Query parameters for the list endpoint (`GET /`):**

| Parameter | Type | Description |
|---|---|---|
| `icc_status` | str[] | `valid`, `partial`, `non_compliant`, `expired` |
| `external_member` | bool | `true` = has external member · `false` = missing |
| `po_compliant` | bool | `true` = female PO · `false` = non-compliant PO |
| `training_compliant` | bool | `true` = all members trained this year |
| `expiry_within_days` | int | e.g., `30` — branches with any member expiring within N days |
| `reconstitution_overdue` | bool | `true` = any member term expired this month and no new constitution recorded |
| `branch_id` | int[] | Filter to specific branch(es) |
| `search` | str | Branch name (partial match) |
| `page` | int | Page number (default: 1) |
| `page_size` | int | Default 25, max 100 |
| `sort_by` | str | Column name; prefix `-` for descending (e.g., `-earliest_term_expiry`) |

**Query parameters for renewal endpoint (`GET /members/renewal/`):**

| Parameter | Type | Description |
|---|---|---|
| `branch_id` | int[] | Filter to specific branch(es) |
| `days_max` | int | Max days until expiry (default: 60) |
| `member_type` | str[] | `internal`, `external_ngo`, `external_legal` |
| `trained_this_year` | bool | Filter to trained/untrained members |
| `search` | str | Member name or branch name |
| `page` | int | Page number |
| `page_size` | int | Default 25 |
| `sort_by` | str | e.g., `days_remaining`, `-name` |

---

## 12. HTMX Patterns

### Pattern Table

| Interaction | hx-trigger | hx-get / hx-post | hx-target | hx-swap |
|---|---|---|---|---|
| Compliance matrix search | `keyup changed delay:300ms` | GET `.../icc/?search={val}&{filters}` | `#compliance-matrix-body` | `innerHTML` |
| Advanced filter apply | `change` on any filter input | GET `.../icc/?{all-filter-params}` | `#compliance-matrix-section` | `innerHTML` |
| Compliance matrix pagination | `click` | GET `.../icc/?page={n}` | `#compliance-matrix-section` | `innerHTML` `hx-push-url="true"` |
| Branch ICC detail drawer open | `click` on branch name or View action | GET `.../icc/{branch_id}/` | `#drawer-container` | `innerHTML` |
| Drawer tab switch | `click` on tab button | GET `.../icc/{branch_id}/?tab={tab_slug}` | `#drawer-tab-content` | `innerHTML` |
| Term History tab load | `click` on Term History tab | GET `.../icc/{branch_id}/term-history/` | `#drawer-tab-content` | `innerHTML` |
| Training tab load | `click` on Training tab | GET `.../icc/{branch_id}/training/` | `#drawer-tab-content` | `innerHTML` |
| Reconstitution Log tab load | `click` on Reconstitution Log tab | GET `.../icc/{branch_id}/reconstitution-log/` | `#drawer-tab-content` | `innerHTML` |
| Constitute ICC form submit | `click` on Save Constitution | POST `.../icc/constitute/` | `#compliance-matrix-section` | `innerHTML` + `hx-on::after-request="closeDrawer(); fireToast();"` |
| Live composition validation | `change` on any member sub-field | GET `.../icc/validate-composition/` (partial form POST with `hx-include`) | `#composition-check-panel` | `innerHTML` |
| Record training submit | `click` on Save Training Record | POST `.../icc/{branch_id}/training/` | `#training-tab-content` | `innerHTML` + `hx-on::after-request="closeDrawer(); fireToast();"` |
| Send reminder submit | `click` on Send Reminder | POST `.../icc/{branch_id}/reminders/` | `#reminder-result` | `innerHTML` + `hx-on::after-request="closeDrawer(); fireToast();"` |
| Members renewal search | `keyup changed delay:300ms` | GET `.../icc/members/renewal/?search={val}` | `#renewal-table-body` | `innerHTML` |
| Compliance trend chart load | `load` | GET `.../icc/compliance-trend/` | `#compliance-trend-chart` | `innerHTML` |
| KPI bar load | `load` | GET `.../icc/kpi/` | `#kpi-bar` | `innerHTML` |
| KPI bar auto-refresh | `every 600s` (10 minutes) | GET `.../icc/kpi/` | `#kpi-bar` | `innerHTML` |
| Alert banners load | `load` | GET `.../icc/alerts/` | `#alert-banner` | `innerHTML` |

---

### Inline HTML Snippets

#### 1. Compliance Matrix Search with Advanced Filters

```html
<!-- Search bar with 300ms debounce, includes all filter fields -->
<div class="flex items-center gap-3 mb-4">
  <input
    id="icc-search"
    name="search"
    type="text"
    placeholder="Search branch name…"
    class="w-72 px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-indigo-500 focus:border-indigo-500"
    hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/"
    hx-trigger="keyup changed delay:300ms"
    hx-target="#compliance-matrix-section"
    hx-swap="innerHTML"
    hx-include="#icc-filter-form"
    hx-indicator="#matrix-spinner"
  >
  <div id="matrix-spinner" class="htmx-indicator">
    <svg class="animate-spin h-5 w-5 text-indigo-500" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
    </svg>
  </div>
</div>

<!-- Filter form — hidden inputs are included in every search/filter request -->
<form id="icc-filter-form">
  <input type="hidden" name="page" value="1">
  <!-- ICC Status checkboxes -->
  <fieldset class="flex gap-3 flex-wrap">
    <label class="flex items-center gap-1 text-sm">
      <input type="checkbox" name="icc_status" value="valid"
             hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/"
             hx-trigger="change"
             hx-target="#compliance-matrix-section"
             hx-swap="innerHTML"
             hx-include="#icc-filter-form, #icc-search">
      Valid
    </label>
    <label class="flex items-center gap-1 text-sm">
      <input type="checkbox" name="icc_status" value="partial"
             hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/"
             hx-trigger="change"
             hx-target="#compliance-matrix-section"
             hx-swap="innerHTML"
             hx-include="#icc-filter-form, #icc-search">
      Partial
    </label>
    <label class="flex items-center gap-1 text-sm">
      <input type="checkbox" name="icc_status" value="non_compliant"
             hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/"
             hx-trigger="change"
             hx-target="#compliance-matrix-section"
             hx-swap="innerHTML"
             hx-include="#icc-filter-form, #icc-search">
      Non-Compliant
    </label>
    <label class="flex items-center gap-1 text-sm">
      <input type="checkbox" name="icc_status" value="expired"
             hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/"
             hx-trigger="change"
             hx-target="#compliance-matrix-section"
             hx-swap="innerHTML"
             hx-include="#icc-filter-form, #icc-search">
      Expired
    </label>
  </fieldset>

  <!-- External member filter -->
  <select name="external_member"
          class="mt-2 text-sm border border-gray-300 rounded px-2 py-1"
          hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/"
          hx-trigger="change"
          hx-target="#compliance-matrix-section"
          hx-swap="innerHTML"
          hx-include="#icc-filter-form, #icc-search">
    <option value="">External Member — All</option>
    <option value="true">Present</option>
    <option value="false">Missing</option>
  </select>
</form>

<!-- Compliance matrix target -->
<div id="compliance-matrix-section">
  <!-- Server renders table rows here -->
</div>
```

#### 2. Branch ICC Detail Drawer Open

```html
<!-- Triggered from compliance matrix row — branch name or View button -->
<button
  class="text-indigo-600 hover:underline text-sm font-medium"
  hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/{{ branch_id }}/"
  hx-trigger="click"
  hx-target="#drawer-container"
  hx-swap="innerHTML"
  hx-indicator="#drawer-spinner"
  @click="drawerOpen = true"
>
  {{ branch.short_name }}
</button>

<!-- Drawer shell — Alpine.js controls visibility; HTMX fills content -->
<div id="drawer-container"
     x-data="{ drawerOpen: false }"
     x-show="drawerOpen"
     x-transition:enter="transition ease-out duration-300"
     x-transition:enter-start="translate-x-full"
     x-transition:enter-end="translate-x-0"
     class="fixed inset-y-0 right-0 w-[680px] bg-white shadow-2xl z-50 overflow-y-auto flex flex-col">
  <!-- HTMX injects drawer content (header + tabs + tab content) here -->
  <div id="drawer-spinner" class="htmx-indicator flex items-center justify-center h-full">
    <svg class="animate-spin h-8 w-8 text-indigo-500" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
    </svg>
  </div>
</div>
```

#### 3. Live Composition Validation in Constitute ICC Form

```html
<!-- Member block — each row of the repeating member form -->
<div class="member-row border border-gray-200 rounded-lg p-4 mb-3" id="member-row-{{ idx }}">
  <div class="grid grid-cols-3 gap-3">
    <div>
      <label class="text-xs text-gray-500 font-medium">Name *</label>
      <input type="text" name="members[{{ idx }}][name]"
             class="w-full border border-gray-300 rounded px-2 py-1 text-sm mt-1"
             hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/validate-composition/"
             hx-trigger="change"
             hx-target="#composition-check-panel"
             hx-swap="innerHTML"
             hx-include="#constitute-icc-form"
             required>
    </div>
    <div>
      <label class="text-xs text-gray-500 font-medium">Role in ICC *</label>
      <select name="members[{{ idx }}][role]"
              class="w-full border border-gray-300 rounded px-2 py-1 text-sm mt-1"
              hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/validate-composition/"
              hx-trigger="change"
              hx-target="#composition-check-panel"
              hx-swap="innerHTML"
              hx-include="#constitute-icc-form">
        <option value="">Select role…</option>
        <option value="presiding_officer">Presiding Officer</option>
        <option value="member">Member</option>
        <option value="external_member">External Member</option>
      </select>
    </div>
    <div>
      <label class="text-xs text-gray-500 font-medium">Gender *</label>
      <div class="flex gap-3 mt-2">
        <label class="flex items-center gap-1 text-sm">
          <input type="radio" name="members[{{ idx }}][gender]" value="female"
                 hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/validate-composition/"
                 hx-trigger="change"
                 hx-target="#composition-check-panel"
                 hx-swap="innerHTML"
                 hx-include="#constitute-icc-form">
          Female
        </label>
        <label class="flex items-center gap-1 text-sm">
          <input type="radio" name="members[{{ idx }}][gender]" value="male"
                 hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/validate-composition/"
                 hx-trigger="change"
                 hx-target="#composition-check-panel"
                 hx-swap="innerHTML"
                 hx-include="#constitute-icc-form">
          Male
        </label>
      </div>
    </div>
  </div>
</div>

<!-- Live composition validation panel — server re-renders on every field change -->
<div id="composition-check-panel"
     class="mt-4 p-4 bg-gray-50 border border-gray-200 rounded-lg">
  <!-- Server returns this HTML snippet based on current form state -->
  <h4 class="text-sm font-semibold text-gray-700 mb-2">Composition Check</h4>
  <ul class="space-y-1 text-sm">
    <li class="flex items-center gap-2">
      <!-- Rendered by server based on current data: -->
      <span class="text-green-600">✅</span>
      <span>Presiding Officer assigned</span>
    </li>
    <li class="flex items-center gap-2">
      <span class="text-red-500">❌</span>
      <span class="text-red-600 font-medium">Presiding Officer must be Female (POCSO Section 4)</span>
    </li>
    <li class="flex items-center gap-2">
      <span class="text-red-500">❌</span>
      <span class="text-red-600 font-medium">External (NGO/Legal) member is missing</span>
    </li>
    <li class="flex items-center gap-2">
      <span class="text-green-600">✅</span>
      <span>Minimum 3 members met ({{ member_count }} members)</span>
    </li>
  </ul>
</div>

<!-- Save button — disabled until server confirms valid composition -->
<button
  type="submit"
  id="save-constitution-btn"
  class="btn-primary"
  hx-post="/api/v1/group/{{ group_id }}/welfare/pocso/icc/constitute/"
  hx-target="#compliance-matrix-section"
  hx-swap="innerHTML"
  hx-include="#constitute-icc-form"
  hx-disabled-elt="this"
  hx-on::after-request="closeDrawer(); fireToast(event);"
>
  Save Constitution
</button>
```

#### 4. KPI Bar Auto-Refresh (every 10 minutes)

```html
<div
  id="kpi-bar"
  class="grid grid-cols-4 gap-4 mb-6"
  hx-get="/api/v1/group/{{ group_id }}/welfare/pocso/icc/kpi/"
  hx-trigger="load, every 600s"
  hx-swap="innerHTML"
  hx-indicator="#kpi-refresh-indicator"
>
  <!-- Server renders 8 KPI cards. Shimmer shown while refreshing via htmx-indicator -->
  <!-- Example card skeleton shown on initial load: -->
  <div class="bg-white border border-gray-200 rounded-lg p-4 animate-pulse">
    <div class="h-3 bg-gray-200 rounded w-3/4 mb-2"></div>
    <div class="h-8 bg-gray-200 rounded w-1/2"></div>
  </div>
</div>
<span id="kpi-refresh-indicator" class="htmx-indicator text-xs text-gray-400 ml-2">Refreshing…</span>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
