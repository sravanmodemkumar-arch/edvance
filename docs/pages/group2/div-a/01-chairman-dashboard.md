# 01 — Chairman Dashboard

> **URL:** `/group/gov/chairman/`
> **File:** `01-chairman-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Chairman / Founder (G5) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Chairman/Founder. Single-screen command view of the
entire institution group — financial health, branch performance, critical alerts, and pending
approvals requiring the Chairman's signature. The Chairman sees everything across all 50 branches
in one page. No navigation required for the day's critical decisions.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Chairman / Founder | G5 | Full — all sections, all actions | This is their exclusive dashboard |
| Group MD | G5 | — | Has own dashboard `/group/gov/md/` |
| Group CEO | G4 | — | Has own dashboard `/group/gov/ceo/` |
| Group President | G4 | — | Has own dashboard |
| Group VP | G4 | — | Has own dashboard |
| Board Trustee | G1 | — | Has own read-only dashboard |
| Exec Secretary | G3 | — | Has own dashboard |
| Strategic Advisor | G1 | — | Has own dashboard |

> **Access enforcement:** Django view decorator `@require_role('chairman')`. Any other role
> hitting this URL is redirected to their own dashboard URL.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Chairman Dashboard
```

### 3.2 Page Header
```
Welcome back, [Chairman Name]                          [Download Board Pack ↓]  [Settings ⚙]
[Group Name] — Chairman & Founder · Last login: [date time] · [Group Logo]
```

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel at top of page, above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch name + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all X alerts →" link to Compliance page

**Alert trigger examples:**
- BGV expired for 3+ staff with student access (POCSO risk)
- Branch fee default >20% for 45+ days outstanding
- Annual strategic plan pending Chairman approval for >10 days
- POCSO incident Severity 1 unresolved >4h
- Branch portal deactivated for >7 days without Chairman knowledge

---

## 4. KPI Summary Bar (6 cards, top row)

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Total Enrollment | `82,340 / 1,00,000 target` + trend ↑2.3% | Aggregated across branches | Green if ≥90% target · Yellow 75–90% · Red <75% | → Branch Overview page 09 |
| Fee Collection Rate | `94.2%` this month + trend ↓1.1% | Finance aggregation | Green ≥95% · Yellow 85–95% · Red <85% | → Fee Revenue Dashboard page 31 |
| BGV Compliance | `87% staff verified` + `42 pending` | HR aggregation | Green ≥98% · Yellow 90–98% · Red <90% (POCSO risk badge) | → Staff Strength page 32 |
| Active Branches | `48 / 50 total` + `2 deactivated` | Branch status | Green = all active · Yellow = 1–2 inactive · Red = 3+ inactive | → Branch Overview page 09 |
| Pending Approvals | `7` requiring Chairman signature · pulsing badge if >0 | Approval queue | Badge always visible if >0 | → Approval Workflow Hub page 17 |
| POCSO Training | `92% staff trained` | HR compliance | Green ≥100% · Yellow 95–99% · Red <95% | → Compliance Overview page 27 |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{id}/chairman/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Critical Approval Queue

> Items awaiting Chairman's explicit approval — not CEO/MD level, Chairman-only.

**Display:** Card list (not table) — max 5 cards, "View all in Approval Hub →" link.

**Card fields:** Type badge | Subject | Branch (if applicable) | Submitted by | Days pending (red if >7) | [Approve ✓] [Reject ✗] [View Details →]

**Approval types shown here:**
- Annual Strategic Plan submission
- New branch activation proposal
- Board resolution requiring Chairman vote
- Policy overriding existing group policy
- Fee structure change >15% variance

**Approve action:** `hx-post="/api/v1/group/{id}/approvals/{approval_id}/approve/"` — on success: toast "Approval recorded" · card removed from queue · audit log entry written.

**Reject action:** Opens 400px modal with required reason field (min 20 chars). POST with reason.

---

### 5.2 Branch Health Matrix

> Master overview of all branches — Chairman sees every branch's health in one table.

**Search:** Full-text across branch name, city, district. Debounce 300ms. Highlights match in results.

**Advanced Filters (slide-in filter drawer):**
| Filter | Type | Options |
|---|---|---|
| State | Multi-select dropdown | All states where group operates |
| Type | Multi-select | Day Scholar Only · Hostel · Both |
| Status | Multi-select | Active · Inactive · Onboarding |
| Performance Tier | Select | Top 25% · Mid · Bottom 25% |
| BGV Risk | Checkbox | Show only BGV <95% |
| Fee Default | Checkbox | Show only fee <85% |

Active filter chips: Yes — dismissible, "Clear All" link, count badge on filter button.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch Name | Text + link | ✅ | Opens Branch Detail (page 10) |
| City / District | Text | ✅ | |
| Type | Badge | ✅ | Day / Hostel / Both |
| Streams | Tags | ❌ | MPC, BiPC etc. |
| Students | Number | ✅ | Total enrolled |
| Fee % | Progress bar + % | ✅ | Colour-coded green/yellow/red |
| Attendance % | Progress bar + % | ✅ | Monthly average |
| BGV % | Progress bar + % | ✅ | Red if <95% |
| POCSO % | Progress bar + % | ✅ | Red if <100% |
| Status | Badge | ✅ | Active / Inactive / Onboarding |
| Last Audit | Date | ✅ | Red if >365 days ago |
| Actions | — | ❌ | View · Edit (G5 only) · Activate/Deactivate |

**Default sort:** Fee % ascending (worst performers first so Chairman acts on them).

**Pagination:** Server-side · Default 25 rows/page · Selector 10/25/50/All · "Showing X–Y of Z branches" · Page jump input.

**Row select:** Checkbox row select + select-all header checkbox.

**Bulk actions (Chairman only):** Export selected as CSV.

**Column visibility toggle:** Yes — gear icon top-right of table.

**Row actions:**
| Action | Icon | Roles | Notes |
|---|---|---|---|
| View | Eye icon | All | Opens Branch Detail page 10 |
| Edit | Pencil | G5 only | Opens branch-edit drawer |
| Activate / Deactivate | Toggle | CEO/G5 | Opens branch-activate-confirm modal |

---

### 5.3 12-Month Financial Trend Chart

**Type:** Combo — grouped bar (Fee Collected vs Fee Expected) + line (Enrollment count secondary Y-axis).

**Library:** Chart.js 4.x.

**X-axis:** Months (Apr–Mar academic year, current year highlighted).

**Y-axis (left):** Fee amount in ₹ Crores.

**Y-axis (right):** Student enrollment count.

**Tooltip:** Month name · Collected ₹X.XCr · Expected ₹X.XCr · Collection rate X% · Enrollment: X.

**Legend:** Bottom, horizontal. Colorblind-safe: Blue (collected), Grey (expected), Orange (enrollment).

**Export:** "Export PNG" button top-right of chart card.

**Filters (within chart card):** Branch filter multi-select · Year selector (current / prev / prev-prev).

**Empty state:** "No financial data available for this period. Contact your Finance team." — no chart renders.

---

### 5.4 Quick Access Grid

6 tile grid (2 rows × 3 columns), icon + label + subtitle.

| Tile | Icon | Label | Subtitle | Link |
|---|---|---|---|---|
| 1 | 📋 | Annual Strategic Plan | Current year status | `/group/gov/strategic-plan/` |
| 2 | 📊 | Governance Reports | Last generated: [date] | `/group/gov/reports/` |
| 3 | 🔍 | Audit Log | [N] events today | `/group/gov/audit-log/` |
| 4 | 📄 | Policy Management | [N] pending acknowledgements | `/group/gov/policies/` |
| 5 | 👤 | User Provisioning | [N] accounts active | `/group/gov/users/` |
| 6 | ⚙ | Group Settings | Last updated: [date] | `/group/gov/settings/` |

---

### 5.5 Recent Board Activity (read section)

Last 3 board meeting outcomes — card list.

**Card fields:** Meeting # · Date · Type (Annual/Quarterly/Emergency) · Resolutions count · Minutes available? (PDF link) · Attendees count.

**Link:** "View Board Meeting Portal →" → page 29.

---

## 6. Drawers & Modals

### 6.1 Modal: `branch-activate-confirm`
- **Trigger:** Branch table → Activate / Deactivate toggle
- **Width:** 420px
- **Content:** "Activate/Deactivate [Branch Name]?" + reason field (required, min 20 chars) + warning text "This action is audited and cannot be reversed without Chairman approval"
- **Buttons:** [Confirm — Activate/Deactivate] (danger colour for deactivate) + [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{id}/branches/{branch_id}/activate/"` — toast success + audit log entry

### 6.2 Drawer: `approval-detail` (opened from Approval Queue cards)
- **Width:** 560px
- **Tabs:** Details · History · Action
- **Details tab:** Full approval request details (what is being approved, who requested, when, rationale, attachments)
- **History tab:** All previous approvals/rejections for this item type from this branch
- **Action tab:** [Approve with optional comment] [Reject with required reason] [Delegate to MD]
- **HTMX:** `hx-get="/api/v1/group/{id}/approvals/{approval_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Approval submitted | "Approval recorded and notified to submitter" | Success (green) | 4s auto-dismiss |
| Rejection submitted | "Rejection recorded with reason" | Success | 4s |
| Page data refresh | "Dashboard refreshed" | Info | 4s |
| KPI load error | "Failed to load KPI data. Retrying…" | Error (red) | Manual dismiss |
| Branch deactivated | "Branch [Name] deactivated. Notification sent to branch Principal." | Warning (yellow) | 6s |
| Export triggered | "Export started — you'll receive the file shortly" | Info | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No pending approvals | Checkmark circle | "All clear — nothing pending" | "No approvals require your attention right now" | — |
| No branches found (search) | Magnifier | "No branches match your search" | "Try adjusting your search or clearing filters" | [Clear Filters] |
| No branches exist | Building icon | "No branches set up yet" | "Add your first branch to get started" | [+ Add Branch] |
| No financial data | Bar chart outline | "Financial data unavailable" | "Financial data for this period hasn't been loaded yet" | [Refresh] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + branch table rows (5 skeleton rows) + chart placeholder |
| Table data fetch (filter/search/page change) | Inline skeleton rows — 5 rows, same column widths |
| KPI card auto-refresh | Subtle shimmer over existing card values |
| Approval action (Approve/Reject button click) | Spinner inside button + button disabled |
| Chart data load | Chart area shows spinner centred in chart space |
| Branch activate/deactivate confirm | Full-page overlay spinner with "Processing branch status change…" |

---

## 10. Role-Based UI Visibility

| Element | Chairman G5 | All others |
|---|---|---|
| Page itself | ✅ Rendered | ❌ Redirected to own dashboard |
| Alert Banner | ✅ Shown | N/A |
| [Approve] / [Reject] in Approval Queue | ✅ Enabled | N/A |
| [Edit] row action in Branch table | ✅ Shown | N/A |
| Branch Activate/Deactivate toggle | ✅ Shown | N/A |
| [Download Board Pack] header button | ✅ Shown | N/A |
| Export (bulk) | ✅ Shown | N/A |
| Quick Access tile — User Provisioning | ✅ Shown | N/A |
| Quick Access tile — Group Settings | ✅ Shown | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/chairman/dashboard/` | JWT (G5) | Full page data — KPIs, alerts, approvals, branches |
| GET | `/api/v1/group/{group_id}/chairman/kpi-cards/` | JWT (G5) | KPI card values only (for auto-refresh) |
| GET | `/api/v1/group/{group_id}/branches/` | JWT (G5) | Branch list with health metrics + filters/search/sort/page params |
| GET | `/api/v1/group/{group_id}/chairman/financial-trend/` | JWT (G5) | 12-month fee vs expected data |
| GET | `/api/v1/group/{group_id}/approvals/?role=chairman` | JWT (G5) | Chairman-level approval queue |
| POST | `/api/v1/group/{group_id}/approvals/{approval_id}/approve/` | JWT (G5) | Approve item |
| POST | `/api/v1/group/{group_id}/approvals/{approval_id}/reject/` | JWT (G5) | Reject with reason |
| POST | `/api/v1/group/{group_id}/branches/{branch_id}/activate/` | JWT (G5) | Activate/deactivate branch |
| GET | `/api/v1/group/{group_id}/branches/export/?format=csv` | JWT (G5) | Export branch table |
| GET | `/api/v1/group/{group_id}/board-meetings/?limit=3` | JWT (G5) | Last 3 board meetings |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Branch search input | `input delay:300ms` | `/api/.../branches/?q={val}` | `#branch-table-body` | `innerHTML` |
| Advanced filter apply | `click` on Apply button | `/api/.../branches/?filters={…}` | `#branch-table-section` | `innerHTML` |
| Pagination page change | `click` | `/api/.../branches/?page={n}` | `#branch-table-section` | `innerHTML` |
| Table sort click | `click` | `/api/.../branches/?sort={col}&dir={asc/desc}` | `#branch-table-section` | `innerHTML` |
| KPI auto-refresh | `every 5m` | `/api/.../chairman/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Open approval detail | `click` | `/api/.../approvals/{id}/` | `#drawer-body` | `innerHTML` |
| Approve button | `click` | POST `/api/.../approve/` | `#approval-queue` | `innerHTML` |
| Chart filter change | `change` | `/api/.../financial-trend/?branch={}&year={}` | `#chart-data` | `innerHTML` (re-renders chart) |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
