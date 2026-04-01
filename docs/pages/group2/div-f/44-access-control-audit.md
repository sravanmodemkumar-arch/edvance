# Page 44: Access Control Audit

**URL:** `/group/it/security/access-audit/`
**Roles:** Group Cybersecurity Officer (Role 56, G1) — read; Group IT Admin (Role 54, G4) — manage
**Priority:** P1
**Division:** F — Group IT & Technology

---

## 1. Purpose

Periodic review of all user access rights across the EduForge platform to identify and remediate three categories of access risk:

1. **Over-Privileged Accounts** — Staff whose assigned role gives them more access than required for their current job function (role creep)
2. **Stale Accounts** — Accounts belonging to staff who have left the organisation but were never deactivated, or accounts with no login activity in over 90 days
3. **Role Creep** — Staff who have accumulated additional permissions over time without formal review

Access reviews are mandatory every quarter (Q1, Q2, Q3, Q4) for each branch. The IT Admin (Role 54) manages the review process — generates the user list for each branch, reviews each user, and takes actions (approve continued access, suspend, or downgrade role).

Results are automatically logged to the IT Audit Log (Page 52) for accountability. The Cybersecurity Officer (Role 56, G1) can monitor the review process and read all results but cannot take any actions.

Access reviews feed into the group's DPDP Act 2023 compliance programme — the right to data minimisation requires that access to personal data is limited to those who genuinely need it.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Admin (Role 54, G4) | Full management | Start reviews, review user lists, take actions (approve/suspend/downgrade) |
| Group IT Director (Role 53, G4) | Read + override | Can view all results; can override any action |
| Group Cybersecurity Officer (Role 56, G1) | Read-only | View review register and results; no action buttons |
| All other roles | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > Cybersecurity > Access Control Audit`

**Page Header:**
- Title: `Access Control Audit`
- Subtitle: `Quarterly access rights review — identify over-privileged and stale accounts`
- Right side: `+ Start New Access Review` (Role 54 only), `Export Register (CSV)` button

**Alert Banners:**

1. **Overdue Access Review** (red, non-dismissible):
   - Condition: any branch whose access review for the current quarter is past the 90-day deadline and status ≠ Completed
   - Text: `Access review overdue: [Branch Name] Q[N] [Year] — [X] days past deadline. Mandatory quarterly review required.`

2. **Stale Accounts Detected** (amber, dismissible per session):
   - Condition: review found stale accounts that have not yet been acted upon
   - Text: `[X] stale accounts (no login >90 days) identified in [Branch] access review. Action required before next audit.`

3. **Over-Privileged Accounts Pending Action** (amber, dismissible per session):
   - Condition: over-privileged accounts flagged in a completed review with no action taken
   - Text: `[X] over-privileged accounts from [Branch] Q[N] review are still pending role review.`

---

## 4. KPI Summary Bar

Five KPI cards in a 5-column responsive grid.

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Users Reviewed (Last Quarter) | Total users included in reviews completed in the last quarter | Number |
| 2 | Over-Privileged Accounts Flagged | Count of over-privileged findings from last quarter reviews | Number — red if > 0 |
| 3 | Stale Accounts (No Login >90 Days) | Count of accounts with last_login_date < today - 90 days across all branches | Number — red if > 0 |
| 4 | Access Reviews Due | Count of branches where current quarter review has not been started or completed | Number — red if > 0 |
| 5 | Reviews Completed On Time % | Reviews completed before deadline / total reviews required × 100 | % — red if < 100% |

---

## 5. Main Table — Access Review Register

**Table Title:** `Access Review Register`
**Description:** One row per branch per quarter showing the access review cycle status.

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Review Period | Badge | Q1 2026 / Q2 2026 etc. |
| Branch | Text | Branch name |
| Users in Scope | Number | Total user accounts reviewed |
| Over-Privileged Found | Number | Count flagged as over-privileged in this review |
| Stale Found | Number | Count flagged as stale (no login >90 days) |
| Actions Taken | Text | Summary: `X Suspended, Y Downgraded, Z Approved` |
| Completed By | Text | IT Admin name who completed the review |
| Completed Date | Date | Date review was marked complete |
| Status | Badge | Scheduled (blue) / In Progress (amber) / Completed (green) / Overdue (red) |
| Actions | Buttons | `Start Review` (Role 54, Scheduled status) / `Continue Review` (Role 54, In Progress) / `View Results` (all) |

### Filters

- **Review Period:** Dropdown (Q1 2025, Q2 2025, ... Q4 2026)
- **Branch:** Multi-select dropdown
- **Status:** All / Scheduled / In Progress / Completed / Overdue

### Search

Search on branch name. `hx-trigger="keyup changed delay:400ms"`, targets `#review-table`.

### Pagination

Server-side, 20 rows per page. `hx-get="/group/it/security/access-audit/table/?page=N"`, targets `#review-table`.

### Sorting

Sortable: Review Period, Branch, Status, Completed Date. Default sort: Status (Overdue first, then In Progress, then Scheduled, then Completed) + Review Period descending.

---

## 6. Drawers

**Note:** Completed access reviews cannot be deleted (audit trail requirement). Results are immutable after completion.

### A. Start Access Review Drawer (560px, right-side — Role 54 only)

Triggered by `+ Start New Access Review` or `Start Review` button.

**Drawer Header:** `Start Access Review`

**Fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Review Period | Dropdown | Yes | Q1 2026 / Q2 2026 / Q3 2026 / Q4 2026 |
| Branch | Dropdown | Yes | Select branch; or "All Branches" to generate simultaneous reviews |
| Review Scope | Checkbox group | Yes | All users / Active users only / Users with data access only |
| Include Stale Threshold | Number input | Yes | Days without login to flag as stale (default 90) |
| Over-Privileged Detection | Toggle | Yes | Auto-flag users whose role exceeds minimum required for their staff category |
| Review Deadline | Date | Yes | Auto-suggests end of quarter; editable |
| Notes | Textarea | No | Internal notes for this review cycle |

**Footer:** `Generate User List & Start Review` / `Cancel`

On submit: `hx-post="/api/v1/it/security/access-audit/start/"`. System generates list of all users for that branch with current roles, last login dates, and risk flags. Status → In Progress. Toast: `Access review started for [Branch] [Period]. [X] users in scope.`

---

### B. Review User List Drawer (720px, right-side — Role 54/53 only)

Triggered by `Start Review` or `Continue Review` button. This is the working interface for the review.

**Drawer Header:** `Access Review — [Branch] — [Period]`

**Progress bar:** `Reviewed: X / Y users`

**User Review Table (within drawer):**

| Field | Value | Action |
|-------|-------|--------|
| Name | [Full Name] | |
| Role | [Current Role] | |
| Access Level | G1/G2/G3/G4 | |
| Last Login | [date] or `Never` | |
| Risk Flag | None / Over-Privileged / Stale / Both (coloured badge) | |
| Reviewer Action | Dropdown: Approve / Suspend / Downgrade Role | Required for each user |
| Notes | Text input | Optional |

**Bulk actions:**
- `Approve All with No Flags` — one-click approve all users with no risk flag
- `Select All Stale → Suspend` — pre-fill action for all stale accounts

**Navigation:** Previous / Next user buttons; or scroll within the drawer list.

**Complete Review button:** Enabled only when all users have a reviewer action selected.

**Footer:** `Save Progress & Close` (saves partial work) / `Complete Review` (marks review as Completed; all actions applied)

On Complete: `hx-post="/api/v1/it/security/access-audit/{review_id}/complete/"`. All actions applied (suspensions/role downgrades written to user records and IT Audit Log). Toast: `Access review completed for [Branch] [Period]. X suspended, Y downgraded, Z approved.`

**Audit:** All review actions (suspend/downgrade/approve per user) and the overall review completion are logged to the IT Audit Log with actor, timestamp, and actions taken.

---

### C. View Past Review Results Drawer (640px — all roles)

Triggered by `View Results` button.

**Sections:**

**Review Summary:**
- Period, Branch, Total users in scope
- Completed by, Completed date
- Over-privileged found: X
- Stale found: X
- Actions: X suspended, Y downgraded, Z approved

**Actions Taken (table):**

| User | Risk Flag | Action Taken | Previous Role | New Role/Status | Actioned By | Date |
|------|-----------|-------------|---------------|-----------------|-------------|------|
| ... | ... | ... | ... | ... | ... | ... |

**Footer:** `Close` | `Export Results (CSV)` (Role 54/53)

---

## 7. Charts

No dedicated charts section (this is a procedural/operational page). An inline mini-summary strip below the KPI bar shows:

**Quarterly Review Completion Status (Current Year):**
- Visual grid: Q1 / Q2 / Q3 / Q4 × each branch
- Cell colour: Completed (green) / In Progress (amber) / Scheduled (blue) / Overdue (red) / N/A (grey)
- Tooltip on hover: status + completion date
- This replaces chart section for this page.

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Review started | Success: `Access review started for [Branch] [Period]. [X] users in scope.` |
| Progress saved | Info: `Review progress saved. [X] of [Y] users reviewed.` |
| Review completed | Success: `Access review completed. [X] suspended, [Y] downgraded, [Z] approved. Changes logged.` |
| User suspended | Success: `[User] account suspended. IT Audit Log updated.` |
| User role downgraded | Success: `[User] role downgraded to [Role]. IT Audit Log updated.` |
| User approved | Info: `[User] access approved for continued access.` |
| Export initiated | Info: `Exporting review results.` |
| Validation error | Error: `Complete reviewer action for all users before finalising the review.` |

---

**Audit Trail:** All access review lifecycle events (start, individual actions, completion) are logged to the IT Audit Log. Suspended and downgraded users are also reflected in the IT Audit Log entry for the review.

**Notifications for Critical Events:**
- Access review overdue (scheduled date passed without completion): IT Admin (in-app amber + email) + IT Director (email)
- Severity 1 over-privileged access found during review: Cybersecurity Officer + IT Director (in-app amber + email) immediately
- Access review completed: IT Director (in-app info notification)

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No reviews started | Icon + `No access reviews on record. Start a quarterly review using "+ Start New Access Review".` |
| No reviews match filters | `No reviews match the selected filters.` |
| All reviews completed for year | Green banner: `All quarterly access reviews for [Year] are complete.` |
| User list empty (no users in scope) | In review drawer: `No users matched the selected scope for this branch.` |
| Actions taken table empty | `No actions were taken in this review — all access was approved.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI bar | 5 skeleton shimmer cards |
| Review register table | 5 skeleton rows |
| Quarterly status grid | Skeleton grid of cells |
| Review user list (drawer) | Spinner while generating user list |
| View results drawer | Spinner then section render |
| Complete Review button | `Applying actions...` + disabled while processing |

---

## 11. Role-Based UI Visibility

| UI Element | Role 56 (G1) | Role 54 (G4) | Role 53 (G4) |
|------------|-------------|-------------|-------------|
| Start New Access Review | Hidden | Visible | Hidden |
| Start Review / Continue Review | Hidden | Visible | Hidden |
| View Results | Visible | Visible | Visible |
| Review user list (action dropdowns) | Not rendered | Visible | Visible (override) |
| Approve/Suspend/Downgrade controls | Hidden | Visible | Visible |
| Export CSV | Hidden | Visible | Visible |
| Overdue alert banner | Visible (read) | Visible (actionable) | Visible |
| Stale accounts banner | Visible (read) | Visible (actionable) | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/security/access-audit/` | Fetch review register (paginated) |
| POST | `/api/v1/it/security/access-audit/start/` | Start new access review (Role 54) |
| GET | `/api/v1/it/security/access-audit/{review_id}/` | Fetch review detail |
| GET | `/api/v1/it/security/access-audit/{review_id}/users/` | Fetch user list for review |
| PUT | `/api/v1/it/security/access-audit/{review_id}/users/{user_id}/` | Save reviewer action for user |
| POST | `/api/v1/it/security/access-audit/{review_id}/complete/` | Complete review + apply actions |
| GET | `/api/v1/it/security/access-audit/kpis/` | Fetch KPI values |
| GET | `/api/v1/it/security/access-audit/quarterly-grid/` | Quarterly completion grid data |
| GET | `/api/v1/it/security/access-audit/{review_id}/export/csv/` | Export review results |
| GET | `/api/v1/it/security/access-audit/export/csv/` | Export full register |

---

## 13. HTMX Patterns

```html
<!-- Review register table -->
<div id="review-table"
     hx-get="/group/it/security/access-audit/table/"
     hx-trigger="load"
     hx-target="#review-table"
     hx-include="#review-filter-form">
</div>

<!-- Quarterly grid -->
<div id="quarterly-grid"
     hx-get="/group/it/security/access-audit/quarterly-grid/"
     hx-trigger="load"
     hx-target="#quarterly-grid">
</div>

<!-- Start review drawer -->
<button hx-get="/group/it/security/access-audit/start-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  + Start New Access Review
</button>

<!-- Start review submit -->
<form hx-post="/api/v1/it/security/access-audit/start/"
      hx-target="#review-table"
      hx-swap="outerHTML"
      hx-on::after-request="closeDrawer(); refreshKPIs()">
  <button type="submit">Generate User List & Start Review</button>
</form>

<!-- Review user list drawer -->
<button hx-get="/group/it/security/access-audit/{{ review.id }}/user-list/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  Continue Review
</button>

<!-- Save individual user action (inline) -->
<select name="action"
        hx-put="/api/v1/it/security/access-audit/{{ review.id }}/users/{{ user.id }}/"
        hx-trigger="change"
        hx-target="#user-row-{{ user.id }}"
        hx-swap="outerHTML"
        hx-include="[name='notes_{{ user.id }}']">
</select>

<!-- Complete review -->
<button hx-post="/api/v1/it/security/access-audit/{{ review.id }}/complete/"
        hx-target="#review-table"
        hx-swap="outerHTML"
        hx-confirm="Complete this review? All actions will be applied and logged."
        hx-on::after-request="closeDrawer(); refreshKPIs()">
  Complete Review
</button>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
