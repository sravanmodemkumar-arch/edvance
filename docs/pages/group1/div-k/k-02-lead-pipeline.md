# K-02 — Lead Pipeline

**Route:** `GET /group1/k/pipeline/`
**Method:** Django `TemplateView` + HTMX part-loads; server-side pagination
**Primary roles:** B2B Sales Manager (#57), Sales Executive — Schools (#58), Sales Executive — Colleges (#59), Sales Executive — Coaching (#60), Inside Sales Executive (#97)
**Also sees:** Sales Ops Analyst (#95) read-only all, Pre-Sales Engineer (#96) assigned leads only, Demo Manager (#62) read-only with demo status column

---

## Purpose

Master lead management workspace. Execs use this daily to manage their active pipeline — creating new leads, logging activities, advancing stages, and scheduling demos. The Sales Manager uses it for pipeline reviews, bulk reassignments before territory changes, and weekly inspection of stale or high-risk deals. Inside Sales Executive (#97) uses it as their primary inbound qualification queue. Sales Ops Analyst exports data for win/loss analysis and quota reporting. The page is designed to be fast and keyboard-navigable for high-frequency use.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Lead table rows | `sales_lead` JOIN auth_user (owner, manager) LEFT JOIN MAX(`sales_activity`.occurred_at) as last_activity | Live — no cache; each filter/sort/page triggers a fresh DB query |
| Stage tab counts | `sales_lead` GROUP BY stage filtered to current user scope | 5 min (separate lightweight query) |
| Demo status column | `sales_demo_tenant` WHERE lead_id IN (page's lead_ids); joined in-memory post-query | 5 min |
| Owner dropdown (Manager filter) | auth_user WHERE role IN (58,59,60,97) AND is_active=True | 60 min |
| Territory filter options | Enum list from application constants (no DB query) | Static |

The lead table itself is live (no Memcached) because pipeline data must reflect real-time stage moves and activity logs. Stage tab counts use a 5-minute cache to avoid hammering GROUP BY on every keystroke in the search box.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?stage` | `all`, `prospect`, `contacted`, `demo_scheduled`, `demo_done`, `proposal_sent`, `negotiation`, `closed_won`, `closed_lost` | `all` | Filters lead table to one stage; also highlights the corresponding tab |
| `?type` | `school`, `college`, `coaching`, `group` (comma-separated for multi) | — | Filter by institution_type |
| `?owner` | user_id (Manager and Ops only) | — (exec sees own; manager sees all) | Filter table to one exec's leads |
| `?territory` | Territory enum value (comma-separated for multi) | — | Filter by territory |
| `?source` | lead_source enum value (comma-separated for multi) | — | Filter by lead_source |
| `?close_before` | ISO date `YYYY-MM-DD` | — | Show leads where expected_close_date ≤ this date |
| `?stale` | `true` | — | Show only leads with no activity in 14+ days |
| `?q` | string ≥ 2 chars | — | Full-text search: ILIKE on institution_name, contact_name, city |
| `?sort` | `arr_asc`, `arr_desc`, `created_asc`, `created_desc`, `close_asc`, `activity_asc` | `activity_asc` (stalest first) | Table sort order |
| `?page` | integer ≥ 1 | `1` | Pagination |

All params persist in URL via `hx-push-url="true"`. Browser back/forward navigates correctly between filter states.

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/k/pipeline-table/` | Lead table body + pagination | Filter/page/sort change | `#k-pipeline-table` |
| `htmx/k/stage-tabs/` | Stage tab badges | After lead create/stage move | `#k-stage-tabs` |
| `htmx/k/pipeline-export/` | Async export trigger | Export button click | `#k-export-status` |

The table partial includes the row count label ("Showing 1–25 of 142") and pagination controls so that they re-render atomically on filter change without touching the filter bar or stage tabs.

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LEAD PIPELINE                                       [+ Create Lead]    │
├─────────────────────────────────────────────────────────────────────────┤
│  [All(142)] [Prospect(28)] [Contacted(31)] [Demo Sched.(18)]            │
│  [Demo Done(22)] [Proposal Sent(19)] [Negotiation(11)]                  │
│  [Won(8 MTD)] [Lost(5 MTD)]                                             │
├─────────────────────────────────────────────────────────────────────────┤
│  FILTER BAR                                                             │
│  [🔍 Search institution, contact, city...]                              │
│  [Type▼]  [Territory▼]  [Owner▼]  [Source▼]  [Close Before▼]          │
│  [Stale Only ☐]                               [Clear All Filters]      │
├──────┬───────────────────────┬──────────┬──────────────┬───────┬───────┤
│  ☐   │ Institution + City    │ Type     │ Stage        │ ARR   │ Owner │
├──────┼───────────────────────┼──────────┼──────────────┼───────┼───────┤
│  ☐   │ KIMS Senior School    │ SCHOOL   │ DEMO_SCHED.  │ ₹1.2L │ Rahul │
│      │ Hyderabad, Telangana  │          │              │       │       │
├──────┼───────────────────────┼──────────┼──────────────┼───────┼───────┤
│  ☐   │ SR Commerce College   │ COLLEGE  │ PROPOSAL_SEN │ ₹90K  │ Priya │
│      │ Pune, Maharashtra     │          │              │       │       │
├──────┴───────────────────────┴──────────┴──────────────┴───────┴───────┤
│  [Last Act.] [Actions ···]  ← these two columns continue right →       │
├─────────────────────────────────────────────────────────────────────────┤
│  Showing 1–25 of 142   [Bulk Actions▼]   [Export CSV]   ← 1 2 3 4 → │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Components

### Stage Tabs

Nine stage tabs plus an "All" tab. Rendered as a horizontal tab bar above the filter row.

| Tab | Label | Count badge source |
|---|---|---|
| All | `All` | Total leads in current scope (exec or org-wide) |
| PROSPECT | `Prospect` | Count in this stage, scoped to viewer |
| CONTACTED | `Contacted` | Count in this stage |
| DEMO_SCHEDULED | `Demo Sched.` | Count in this stage |
| DEMO_DONE | `Demo Done` | Count in this stage |
| PROPOSAL_SENT | `Proposal Sent` | Count in this stage |
| NEGOTIATION | `Negotiation` | Count in this stage |
| CLOSED_WON | `Won (MTD)` | Count WHERE won_at in current month |
| CLOSED_LOST | `Lost (MTD)` | Count WHERE lost_at in current month |

Active tab highlighted with border-bottom and bold font. Count badges turn amber if the stage count has increased by ≥ 5 since last page load (surfaced via a `data-prev-count` attribute compared on HTMX swap).

Clicking a tab sets `?stage=<stage>` and reloads the table partial via HTMX. Tab badge counts are cached separately (5 min) and rendered via the `stage_tabs` partial.

---

### Filter Bar

The filter bar sits between the stage tabs and the lead table. All filter changes trigger an HTMX reload of the `table` partial with `hx-push-url="true"`.

**Search field:** Full-width text input. ILIKE `%q%` query on `sales_lead.institution_name`, `sales_lead.contact_name`, `sales_lead.city`. Minimum 2 characters; 300ms debounce before firing HTMX request. Shows a subtle spinner in the field during loading.

**Type filter:** Multi-select dropdown. Options: School, College, Coaching, Group. Translates to `institution_type IN (...)` filter. Defaults to all types.

**Territory filter:** Multi-select dropdown populated from the territory enum. Options are all 12 territory values. Manager and Ops see all; exec sees only their assigned territory (pre-selected, locked).

**Owner filter (Manager #57 and Ops #95 only):** Single-select dropdown showing active Sales Execs and Inside Sales (#97, #58, #59, #60). Default: All (no filter). Exec roles do not see this filter — their view is always scoped to `owner_id = current_user`.

**Source filter:** Multi-select dropdown. All 8 lead_source enum values. Inside Sales #97 sees ORGANIC_INBOUND and MARKETING_CAMPAIGN pre-selected by default (their typical queue).

**Close Before:** Date picker input. When set, filters to leads WHERE `expected_close_date ≤ selected_date`. Useful for managers doing end-of-quarter pipeline review.

**Stale Only checkbox:** When checked, applies the stale lead filter (no activity in 14+ days, or created >7 days ago with zero activities). Equivalent to `?stale=true`. Stale rows in the table also get an amber left-border highlight regardless of this filter.

**Clear All Filters:** Resets all filter params to defaults and reloads. Does not reset the stage tab selection.

---

### Lead Table

Server-side paginated, 25 rows per page. Sortable by clicking column headers (sort cycles: asc → desc → default).

| Column | Width | Description |
|---|---|---|
| Checkbox | 32px | Row selection for bulk actions; header checkbox selects current page (max 50 for bulk ops) |
| Institution Name + City | ~240px | Institution name (bold, link → K-03); city + state on second line in grey-500 text |
| Type | 80px | Badge: SCHOOL=blue-100/blue-700 · COLLEGE=violet-100/violet-700 · COACHING=orange-100/orange-700 · GROUP=slate-100/slate-700 |
| Stage | 120px | Badge colour: PROSPECT=grey · CONTACTED=blue · DEMO_SCHEDULED=indigo · DEMO_DONE=purple · PROPOSAL_SENT=amber · NEGOTIATION=orange · CLOSED_WON=green · CLOSED_LOST=red |
| ARR | 80px | Formatted ₹1.2L / ₹90K / ₹2.4Cr; sorted numerically. Tooltip shows raw paise value |
| Owner | 100px | Exec name. For exec viewers: column header reads "Owner" but value always shows "Me" for own leads (reduces cognitive load). For Manager/Ops: full name. |
| Last Activity | 90px | Relative time: "Today" / "2d ago" / "Never". >14d ago shown with amber background highlight. "Never" shown with red background if lead is >7 days old. |
| Actions | 56px | 3-dot menu (see below) |

**Actions 3-dot menu options per row:**
- View Account (→ K-03)
- Edit Lead Details (opens Edit Lead drawer, same fields as Create Lead)
- Log Activity (opens Log Activity modal inline)
- Move Stage (opens Stage Move modal with stage dropdown + optional notes; lost_reason required if moving to CLOSED_LOST)
- Assign Pre-Sales (Manager only; assigns `presales_id` from Pre-Sales Engineer dropdown; only for leads with ARR ≥ ₹2L)
- Delete (soft-delete; Manager #57 only; confirmation modal required; moves to a deleted state not visible in pipeline)

**Row click (non-link area):** Opens K-03 Account Profile for that lead in the same tab.

**Stale row highlight:** Leads with last activity >14 days ago have a subtle amber left-border (3px amber-400) on the row to draw attention without being alarming.

---

### Bulk Actions

Available only to B2B Sales Manager (#57). Appears as a dropdown above the table footer once ≥ 1 row is checked. Maximum 50 rows can be selected at once (a banner appears if the user tries to select more: "Bulk actions limited to 50 leads at a time").

| Bulk Action | Behaviour |
|---|---|
| Assign to Exec | Modal opens with a dropdown of active Sales Execs (#58–60) and Inside Sales (#97). On confirm: POST `/group1/k/pipeline/bulk-assign/` with lead_ids + new_owner_id. Success: toast "N leads assigned to [Exec Name]." Table reloads. |
| Move to Stage | Modal opens with a stage dropdown. If CLOSED_LOST selected: lost_reason dropdown (required) also appears. On confirm: POST `/group1/k/pipeline/bulk-stage/`. Logs a system activity for each lead with notes "Bulk stage move by [Manager Name]". Bulk Move to Stage — validation: (1) Shows count: "Moving [N] leads to [Stage]". (2) Validates that all selected leads are eligible for that stage transition (cannot move CLOSED_WON leads backwards without Manager confirmation). (3) If mixed eligibility: "3 of 8 leads cannot be moved to this stage (already closed). Move the other 5?" (4) Requires reason text if moving to CLOSED_LOST. (5) On confirm: bulk UPDATE with system sales_activity logged on each lead: "Stage moved from [old] to [new] by Sales Manager" — does not count as exec activity. |
| Export Selected | Triggers CSV export of the selected rows only (bypasses the 200-row async threshold — always synchronous since ≤50 rows). |
| Delete | Confirmation modal with count: "Delete N leads permanently? This cannot be undone." POST `/group1/k/pipeline/bulk-delete/`. Soft-delete; recoverable by Platform Admin only. |

---

### Create Lead Drawer

Triggered by the `[+ Create Lead]` button in the page header. Opens as a right-side drawer (640px wide) without navigating away. Inside Sales #97 and Sales Execs #58–60 can create leads. Manager #57 can create on behalf of any exec.

**Form UI conventions:** Required fields marked with * (asterisk) in label. Optional fields have "(optional)" suffix. Inline validation fires on blur (field loses focus) for all validated fields. Form-level error summary shown at top of drawer if submit attempted with errors.

**Form fields:**

| Field | Type | Validation |
|---|---|---|
| Institution Name* | Text input | Required; min 3 chars; max 300 chars |
| Institution Type* | Radio group (4 options) | Required |
| Segment Size* | Select dropdown with tooltip guide | Required; tooltip explains MICRO (<100 students) through ENTERPRISE (>10,000) |
| State* | Select (Indian states + UTs, 36 options) | Required |
| City* | Text input | Required; min 2 chars |
| Contact Name* | Text input | Required |
| Contact Phone* | Text input | Required; regex ^[6-9]\d{9}$; shown as +91 prefix + 10-digit input |
| Contact Email (optional) | Email input | Optional; standard email validation |
| Lead Source* | Select dropdown | Required; Inside Sales #97 sees ORGANIC_INBOUND and MARKETING_CAMPAIGN only |
| Territory* | Select dropdown | Required; auto-suggested based on selected State using a state→territory mapping table; user can override |
| Assigned To* | Select dropdown | Manager: full exec list (required). Exec: pre-filled with self (read-only). Inside Sales: self (read-only). |
| Student Count Estimate (optional) | Number input | Optional; integer ≥ 0; triggers ARR auto-calculation |
| ARR Estimate (₹)* | Number input (paise stored, ₹ displayed) | Required; ≥ 0; auto-calculated as student_count × ₹60 (school default), ₹50 (college), ₹150 (coaching) if student count provided; user can override |
| Expected Close Date (optional) | Date picker | Optional; must be a future date if set; validation: close_date > today. Maximum forward limit: Cannot be more than 3 years from today (prevents joke entries). If beyond 3 years: "Expected close date seems far out. Please confirm." validation warning (soft, not hard block). Past dates: blocked with error "Expected close date cannot be in the past." |
| Notes (optional) | Textarea | Optional; max 2000 chars |

**ARR validation bounds:** Minimum ₹0 (allowed but triggers amber warning "Estimated ARR seems low — please confirm"). Maximum per type: SCHOOL ₹50L, COLLEGE ₹30L, COACHING ₹2Cr, GROUP ₹5Cr. Values exceeding max show validation error "ARR estimate exceeds typical range for this institution type." Both client-side (HTML5 max attribute) and server-side (DRF serializer) enforced. **Zero-ARR policy:** ₹0 ARR is allowed at form submission (lead may be created before deal size is known). Amber warning shown inline: "Estimated ARR is ₹0 — please update before closing." Server-side constraint: if stage transition to CLOSED_WON is attempted with arr_estimate_paise = 0, server returns validation error: "ARR must be greater than ₹0 to mark this deal as Won." This is enforced in Django model clean() method, not DB constraint, to preserve admin override capability.

**ARR auto-calculation logic:**
- When institution_type is set AND student_count_estimate is entered, ARR field auto-populates:
  - SCHOOL: student_count × ₹60 (minimum ₹60K cap)
  - COLLEGE: student_count × ₹50 (minimum ₹40K cap)
  - COACHING: student_count × ₹150 (minimum ₹1.5L cap)
  - GROUP: no auto-calculation; manager enters manually
- ARR field remains editable after auto-fill (highlighted with a subtle amber background to indicate it was auto-calculated).

**Zero-student edge case:** If student_count_estimate = 0, ARR auto-calculates to ₹0 but the minimum cap warning shows. User must either enter a non-zero student count or manually override the ARR field. ARR cannot be saved as ₹0 for CLOSED_WON leads (server validates: if stage IN ('CLOSED_WON') then arr_estimate_paise > 0).

**On submit success:** (1) POST /group1/k/pipeline/create/ → 201 response with new lead_id. (2) HTMX: hx-swap="none" on form, JS-triggered: close drawer modal, OOB swap updates stage tab counts (#k-stage-tabs), redirects to K-03 for new lead ID (hx-redirect). (3) Shows success toast "Lead created: [Institution Name]" with "View →" quick link. If duplicate institution_name detected (server-side check): 409 response → inline error "A lead for [Institution Name] already exists in pipeline. View existing lead →".

**Validation errors:** Rendered inline below each field; the first invalid field receives focus. Form does not clear on validation failure.

---

### Export CSV

**Trigger:** `[Export CSV]` button in the table footer. Exports the currently filtered and sorted lead list (not just the current page).

**Columns exported (20):** lead_id, institution_name, institution_type, segment_size, stage, territory, state, city, contact_name, contact_phone, contact_email, lead_source, arr_estimate_inr, student_count_estimate, expected_close_date, owner_name, manager_name, last_activity_date, last_activity_type, created_at.

**Sync export (≤ 200 rows):** Direct HTTP response with `Content-Disposition: attachment; filename=leads_export_YYYYMMDD.csv`. Triggers immediately.

**Async export (> 200 rows):** POST to `/group1/k/pipeline/export/` queues a Celery task. Immediate response: amber toast "Export queued — you'll receive an email with the download link shortly." Email sent to current user's email with a signed S3 URL (valid 24 hours). Available to Sales Execs for their own leads, Manager for all, Ops for all.

**Role restriction:** Create Lead button hidden for #95, #96, #62, #61. Export button hidden for #96 (Pre-Sales has no pipeline export access).

---

## Empty States

| Condition | Message | CTA |
|---|---|---|
| No leads match active filters | "No leads match your current filters." with filter icon | [Clear Filters] button |
| Exec has no leads assigned yet | "You don't have any leads yet. Create your first lead to get started." | [+ Create Lead] button |
| Stage tab is empty (e.g., Negotiation tab: 0 leads) | "No leads in [Stage Name] right now." with stage icon | [View all leads] link back to All tab |
| No stale leads (Stale Only filter checked but 0 results) | "No stale leads — your pipeline is up to date." with green shield | — |
| Pre-Sales #96 with no assigned leads | "No leads assigned to you yet. Leads with ARR > ₹2L will appear here when assigned by the Sales Manager." | — |
| Duplicate institution name detected on create | "A lead for [Institution Name] already exists in pipeline. [View existing →]" — shown as inline error below Institution Name field (not toast). Submit button disabled until name is changed or user explicitly acknowledges. | — |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Lead created successfully | "Lead created for [Institution Name]. Redirecting to account profile..." | Green (success) |
| Stage moved | "[Institution Name] moved to [New Stage]." | Green (success) |
| Stage move to CLOSED_WON | "Deal closed! [Institution Name] — ₹[ARR] ARR. Onboarding handoff initiated." | Green (success, auto-dismissed after 5s) |

Note: CLOSED_WON trigger also initiates a subscription activation task in Division M — Billing Admin (#70) receives in-app + email notification with institution name, ARR, plan tier, and deal ID. This is documented in the Integration Points section of div-k-pages-list.md.
| Bulk assignment complete | "[N] leads assigned to [Exec Name]." | Green (success) |
| Bulk stage move complete | "[N] leads moved to [Stage]." | Green (success) |
| Export queued (async) | "Export queued — download link will be emailed to [user email]." | Amber (info) |
| Lead soft-deleted | "Lead deleted." with [Undo] link (5s window; clicking Undo sends DELETE-reversal POST) | Red (warning) |
| Validation error on create | "Please fix the errors in the form before submitting." | Red (error) |
| Duplicate phone number detected | "A lead with this contact phone already exists: [Institution Name]. [View lead →]" | Amber (warning; non-blocking — user can still submit) |

---

## Authorization

**Route guard:** `@division_k_required(allowed_roles=[57, 58, 59, 60, 95, 96, 97])` applied to `LeadPipelineView`.

| Scenario | Behaviour |
|---|---|
| Unauthenticated | Redirect to login |
| Sales Exec (#58–60) | `sales_lead` queryset filtered to `WHERE owner_id = request.user.id` |
| Inside Sales (#97) | Queryset filtered to `WHERE owner_id = request.user.id AND lead_source IN ('ORGANIC_INBOUND', 'MARKETING_CAMPAIGN')` |
| Pre-Sales (#96) | Queryset filtered to `WHERE presales_id = request.user.id` |
| Sales Ops (#95) | Unscoped read. All write endpoints (POST/PATCH/DELETE) return 403. |
| Bulk Delete POST with non-#57 user | 403 Forbidden |
| Lead belonging to different exec (direct URL) | 404 Not Found (not 403 — avoids information leakage) |

---

## Role-Based View Differences

| Feature | 57 Manager | 58/59/60 Execs | 95 Ops Analyst | 97 Inside Sales Exec (#97) | 96 Pre-Sales | 62 Demo Mgr |
|---|---|---|---|---|---|---|
| See all leads | Yes — full org | Own segment leads only | Yes — read-only all | Own inbound leads only | Assigned leads only | Read-only all (demo status focus) |
| Owner filter | Yes | No (scoped to self) | Yes (read-only) | No (scoped to self) | No | No |
| Create lead | Yes | Yes | No | Yes (inbound/campaign sources) | No | No |
| Bulk assign | Yes | No | No | No | No | No |
| Bulk stage move | Yes | No | No | No | No | No |
| Bulk delete | Yes | No | No | No | No | No |
| Delete single lead | Yes | No | No | No | No | No |
| Move stage (single) | Yes | Own leads only | No | Own leads (PROSPECT→CONTACTED→DEMO_SCHEDULED only) | No | No |
| Export CSV | Yes (all) | Yes (own leads only) | Yes (all, full 20 columns) | Yes (own leads only) | No | No |
| Demo status column | Yes | Yes | Yes | Yes | No | Yes (primary focus) |
| Assign Pre-Sales (3-dot) | Yes (for ARR ≥ ₹2L leads) | No | No | No | No | No |
| [+ Create Lead] button visible | Yes | Yes | No | Yes | No | No |
