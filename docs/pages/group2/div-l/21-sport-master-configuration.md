# 21 — Sport Master Configuration

> **URL:** `/group/sports/master/`
> **File:** `21-sport-master-configuration.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Group Sports Director G3 (Role 97, full CRUD) · Group Sports Coordinator G3 (Role 98, view only)

---

## 1. Purpose

Configuration page for the Sports Director to manage the group's officially recognised sport catalog. Defines which sports exist at the group level — including the sport's code, category, gender eligibility rules, minimum and maximum player counts, eligible age groups, permitted tournament formats, and mandatory documentation requirements. Branch sports programs are constrained to this catalog; no branch may register a team or enter a tournament for a sport that does not appear in the master list. This ensures cross-branch comparability in analytics (Page 20 — Extra-Curricular Analytics), consistent tournament registration validation (Page 07 — Inter-Branch Tournament Manager), accurate equipment procurement planning (Page 10 — Sports Equipment Inventory), and consistent coach assignment eligibility (Page 09 — Coach & Staff Registry).

The catalog is not AY-scoped — sport definitions are permanent configuration objects. Changes take effect immediately across all dependent pages and processes. Infrequently modified: a typical group adds 1–3 sports per year and rarely removes any. A large group typically runs 8–20 official sports.

> **See also:** Page 07 — Inter-Branch Tournament Manager (reads tournament formats from this catalog) · Page 08 — Sports Team Registry (validates sport against this catalog on team creation) · Page 09 — Coach & Staff Registry (sport specialisation field constrained to this catalog) · Page 10 — Sports Equipment Inventory (sport classification field constrained to this catalog) · Page 20 — Extra-Curricular Analytics (sport breakdown charts use this catalog as dimension source)

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Sports Director | G3, Role 97 | Full — create, edit, deactivate, manage all catalog records, upload rule documents | Sole write authority on the sport catalog |
| Group Sports Coordinator | G3, Role 98 | View only — read all catalog records and view rule documents | Cannot create, edit, deactivate, or upload documents |
| Group Cultural Activities Head | G3, Role 99 | No access | 403 on direct URL; sport catalog is outside this role's scope |
| Group NSS/NCC Coordinator | G3, Role 100 | No access | 403 on direct URL |
| Group Library Head | G2, Role 101 | No access | 403 on direct URL |

> **Access enforcement:** `@require_role(['sports_director', 'sports_coordinator'])` on all read endpoints. `@require_role(['sports_director'])` on all write endpoints (POST, PATCH, DELETE/deactivate). File upload endpoints (rule documents) enforced at `@require_role(['sports_director'])`. Inline eligibility matrix edit enforced server-side — the toggle endpoint rejects requests from any role other than 97.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Sport Master Configuration
```

### 3.2 Page Header
```
Sport Master Configuration                   [+ Add Sport]  [Export Catalog ↓]
Group Sports Director — [Director Name]
[N] Sports in Catalog  ·  [N] Active  ·  [N] Inactive  ·  Last updated: [DD MMM YYYY]
```

`[+ Add Sport]` — opens `sport-create` drawer. Role 97 only; hidden for Role 98.
`[Export Catalog ↓]` — exports the full catalog (all columns) to XLSX or PDF. Available to Roles 97 and 98.

> No AY selector is shown on this page. The sport catalog is global configuration, not academic-year scoped.

### 3.3 Alert Banners

Stacked above the KPI bar. Each banner is individually dismissible for the session.

| Condition | Banner Text | Severity |
|---|---|---|
| Sports with missing rule documents | "[N] sport(s) are missing a rule document. Upload rule documents to ensure tournament compliance." | Amber |
| Inactive sport has active teams this AY | "[N] inactive sport(s) still have active teams registered this academic year. Review team status." | Red |
| No sports in catalog | "No sports have been added to the group catalog. Add at least one sport to enable team registrations." | Blue |
| Sport deactivated in last 7 days | "[Sport Name] was deactivated on [date]. [N] branch(es) had active teams registered for this sport." | Amber |

---

## 4. KPI Summary Bar

Four metric cards displayed horizontally. All counts are derived from the sport catalog without AY filtering, except "Sports with Active Teams" which queries the current academic year.

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Sports in Catalog | Count of all records regardless of status | Neutral (indigo) always | Clears filters, reloads full table |
| Sports with Active Teams (This AY) | Count of sports where at least one team is registered and active in current AY | Green if > 0; Amber if 0 | Filters table to sports with `active_teams > 0` |
| Sports with No Teams Anywhere | Count of active catalog sports where `active_teams = 0` across all branches and all AYs | Red if > 0; Green if 0 | Filters table to `active_teams = 0` |
| Sports with Missing Rule Documents | Count of active sports where `rule_document = null` | Red if > 0; Green if 0 | Filters table to `has_rule_document = false` |

```
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│  Total in Catalog   │ │  Active Teams (AY)  │ │  No Teams Anywhere  │ │  Missing Rule Doc   │
│        14           │ │        11           │ │        2            │ │        3            │
│   ● Indigo          │ │   ● Green           │ │   ● Red             │ │   ● Red             │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

> KPI bar loaded via HTMX `hx-trigger="load"` from `/api/v1/sports/master/kpi-summary/`. Refreshes automatically after any create, edit, or deactivate action using `hx-trigger="load, catalogUpdated from:body"`.

---

## 5. Sections

### 5.1 Sport Catalog

**Search bar:**
```
[🔍 Search sport name or code…]  [Category ▾]  [Gender Eligibility ▾]  [Status ▾]  [Rule Document ▾]  [🔽 More Filters]  [Reset]
```

Active filter chips displayed below the bar; each chip has an × to dismiss.

**Filters:**

| Filter | Options |
|---|---|
| Category | All / Individual / Team |
| Gender Eligibility | All / All Genders / Boys Only / Girls Only |
| Status | Active (default) / Inactive / All |
| Rule Document | All / Uploaded / Missing |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| (Checkbox) | Checkbox | — | Select-all in header; drives bulk actions |
| Sport Name | Text (link → `sport-edit` drawer) | ▲▼ | Full name; bold |
| Code | Text | ▲▼ | 3–5 letter uppercase code e.g. `CRI`, `FOO`, `VOL` |
| Category | Badge | — | Individual (blue) / Team (green) |
| Gender Eligibility | Badge | — | All Genders (indigo) / Boys Only (sky) / Girls Only (pink) |
| Min Players | Number | ▲▼ | Shown as "—" for Individual sports |
| Max Players | Number | ▲▼ | Shown as "—" for Individual sports |
| Eligible Age Groups | Tag cloud | — | Tags: U-12, U-14, U-17, U-19, Open; pill-styled |
| Active Teams (This AY) | Number | ▲▼ | Count of active teams registered for this sport in current AY; links to filtered Sports Team Registry |
| Equipment Master | Icon | — | ✅ (green) = linked to equipment category · ❌ (red) = not linked |
| Rule Document | Icon | — | ✅ (green, clickable → `rule-document-view` modal) · ❌ (red) = missing |
| Status | Badge | — | Active (green) / Inactive (grey) |
| Actions | — | — | [Edit] · [View Rules] · [Deactivate] (Role 97 only) |

`[Edit]` — opens `sport-edit` drawer (Role 97 only; button hidden for Role 98).
`[View Rules]` — opens `rule-document-view` modal if document exists; disabled with tooltip "No rule document uploaded" if missing.
`[Deactivate]` — opens `sport-deactivate` confirmation modal (Role 97 only; hidden for Role 98).

**Default sort:** Sport Name ASC.
**Pagination:** 25 rows per page. Controls: `« Previous  Page N of N  Next »`. Rows-per-page selector: 25 / 50 / 100.
**Bulk actions** (shown when ≥ 1 row selected): `[Bulk Deactivate (N)]` · `[Export Catalog ↓]`.

---

### 5.2 Age Group Eligibility Matrix

Read-only visual grid displayed below the main catalog table. Title: "Age Group Eligibility Matrix — All Active Sports".

**Layout:** Rows = active sports (same order as catalog table, current sort). Columns: U-12 | U-14 | U-17 | U-19 | Open.

**Cells:** ✅ green filled cell if the sport is eligible for that age group · ❌ grey filled cell if not eligible.

**Interaction (Role 97 only):** Clicking any ✅ or ❌ cell opens a small inline confirmation popover anchored to the cell:
```
Toggle eligibility?
[Sport Name]  ›  [Age Group]
Currently: Eligible / Not Eligible
[Confirm Toggle]  [Cancel]
```
`[Confirm Toggle]` fires a PATCH to `/api/v1/sports/master/{sport_id}/eligibility/` with `{ age_group: "U-14", eligible: true/false }`. The cell updates via HTMX `hx-swap="outerHTML"` on the cell element.

For Role 98: cells are non-interactive; cursor is default; no popover rendered.

> **Implementation note:** The matrix is server-rendered as an HTML table fragment via `/htmx/sports/master/eligibility-matrix/` and loaded with HTMX `hx-trigger="load"`. After any toggle confirmation, only the affected row is refreshed via `hx-target` on that row's `<tr>` element.

---

## 6. Drawers & Modals

### 6.1 `sport-create` Drawer — 480 px, right-slide

**Trigger:** `[+ Add Sport]` header button (Role 97 only).

**Tabs:** Basic | Rules | Advanced

---

**Tab: Basic**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Sport Name | Text | Yes | Min 2, max 80 characters; must be unique in catalog (case-insensitive) |
| Sport Code | Text | Yes | Min 2, max 5 characters; auto-generated from first letters of sport name words (e.g. "Cricket" → "CRI"); editable; uppercase enforced; must be unique |
| Category | Select | Yes | Individual / Team |
| Gender Eligibility | Select | Yes | All Genders / Boys Only / Girls Only |
| Min Players | Number | Conditional | Shown only when Category = Team; min 1 |
| Max Players | Number | Conditional | Shown only when Category = Team; must be ≥ Min Players |
| Eligible Age Groups | Multi-select checkboxes | Yes | Options: U-12 / U-14 / U-17 / U-19 / Open; at least one must be selected |
| Display Order | Number | No | Integer; controls sort order in dropdowns on other pages; defaults to next available integer |
| Status | Toggle | Yes | Active (default on) / Inactive |

---

**Tab: Rules**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Rule Document | File upload | No | PDF only; max 20 MB; uploaded to Cloudflare R2; shows upload progress bar; filename stored in model |
| Code of Conduct | Textarea | No | Max 2,000 characters; plain text; displayed in team onboarding |
| Minimum Certified Coach Required? | Toggle | Yes | Default: off; if on, all team registrations for this sport require an assigned coach with a coaching certification on file |
| Mandatory Medical Clearance? | Toggle | Yes | Default: off; if on, all players in any tournament for this sport must have a medical fitness certificate uploaded before tournament registration is confirmed |

---

**Tab: Advanced**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Tournament Formats Allowed | Multi-checkbox | No | Knockout / League / Round Robin / Combined; all checked by default |
| Max Teams Per Branch in Any Tournament | Number | No | Default: 1; min 1; controls how many teams from a single branch can register in one tournament for this sport |
| Notes | Textarea | No | Internal notes for Sports Director; max 500 characters; not shown to branches |

**Footer:** `[Cancel]`  `[Save Sport]`

On save: table reloads, KPI bar refreshes, sport code uniqueness re-validated server-side.

---

### 6.2 `sport-edit` Drawer — 480 px, right-slide

**Trigger:** `[Edit]` action in table row, or clicking Sport Name link (Role 97 only).

**Content:** Same 3 tabs as `sport-create`, pre-filled with existing values.

> **Version note displayed at top of drawer (amber info bar):**
> "Changes to Min/Max Players affect all existing teams — eligibility warnings will appear in tournament registration for any team that no longer meets the updated count. Changes to Eligible Age Groups will immediately re-evaluate tournament eligibility for all enrolled teams."

**Footer:** `[Cancel]`  `[Save Changes]`

---

### 6.3 `sport-deactivate` Modal — 380 px, centred

**Trigger:** `[Deactivate]` action in table row (Role 97 only).

**Header:** "Deactivate [Sport Name]?"

**Body:**
```
This sport will no longer be available for new team registrations or
tournament entries. Existing teams and historical records are preserved.

⚠ [N] active team(s) are currently registered for [Sport Name] in
   this academic year across [N] branch(es).
```

**Confirm checkbox** (required before `[Deactivate]` button becomes active):
```
☐  I understand that no new teams or tournaments can be created for this sport after deactivation.
```

**Footer:** `[Cancel]`  `[Deactivate]` (orange button; enabled only after checkbox ticked)

---

### 6.4 `rule-document-view` Modal — 560 px, centred

**Trigger:** `[View Rules]` action in table row, or clicking ✅ icon in Rule Document column.

**Header:** "[Sport Name] — Rule Document"

**Body:** PDF.js embedded viewer, full height of modal (scrollable). Viewer controls: page navigation arrows, zoom in/out, page count display.

**Footer:** `[Download PDF]` (triggers Cloudflare R2 signed URL download) · `[Close]`

> **Upload replacement:** For Role 97, a `[Replace Document]` button appears in the footer alongside `[Download PDF]`. Clicking it opens a file-input in-place inside the modal for uploading a replacement PDF (max 20 MB). On save, the previous document is archived on R2 (not deleted) and the new version is set as current.

---

## 7. Charts

All charts use Chart.js 4.x. Export: each chart has an `[Export PNG]` button rendered below the chart that triggers `chart.toBase64Image()` and downloads the image.

### 7.1 Teams Per Sport — Active This AY

| Attribute | Value |
|---|---|
| Type | Horizontal bar chart |
| Data | One bar per sport; value = count of active teams registered in current AY |
| X-axis | Team count (integer ticks, starts at 0) |
| Y-axis | Sport names; sorted by team count DESC |
| Bar colour | Indigo-500 |
| Tooltip | "[Sport Name]: [N] active team(s) across [N] branch(es)" |
| Export | `[Export PNG]` |

### 7.2 Sports Coverage Per Branch

| Attribute | Value |
|---|---|
| Type | Dense horizontal grouped bar chart (one group per branch; one bar per sport within group) — used to approximate a heatmap since Chart.js 4.x has no native heatmap |
| Data | For each branch: one bar per sport, bar height = 1 if branch has a team for that sport in current AY; 0 if not |
| Colour | Bar present (value=1): green-400 · Bar absent (value=0): grey-200 |
| X-axis | Sport codes (3-letter abbreviations); max 20 labels before label rotation |
| Y-axis | Branch count (0 or 1) — effectively a presence indicator |
| Legend | Branch names rendered as separate datasets |
| Tooltip | "[Branch Name] — [Sport Name]: Has Team / No Team" |
| Interaction | Clicking a bar navigates (new tab) to the Sports Team Registry filtered to that branch + sport |
| Note | For groups with > 25 branches, the chart renders only the top 25 branches by total sport coverage count. A "View All" link expands to a paginated data table. |
| Export | `[Export PNG]` |

---

## 8. Toast Messages

| Action | Toast Text | Type | Duration |
|---|---|---|---|
| Sport created | "Sport '[Name]' added to the catalog with code [CODE]." | Success | 4 s |
| Sport updated | "Sport '[Name]' has been updated." | Success | 4 s |
| Sport deactivated | "Sport '[Name]' has been deactivated. Existing teams and records are preserved." | Success | 4 s |
| Rule document uploaded | "Rule document for '[Name]' uploaded successfully." | Success | 4 s |
| Rule document replaced | "Rule document for '[Name]' replaced. Previous version archived." | Success | 4 s |
| Age group toggle saved | "[Sport Name] — [Age Group] eligibility updated." | Success | 4 s |
| Bulk deactivate complete | "[N] sport(s) deactivated." | Success | 4 s |
| Export complete | "Catalog exported to [format]." | Success | 4 s |
| Sport name already exists | "A sport named '[Name]' already exists in the catalog." | Error | Manual dismiss |
| Sport code already exists | "Sport code '[CODE]' is already assigned to '[Existing Sport Name]'." | Error | Manual dismiss |
| Rule document upload failed | "File upload failed. Only PDF files up to 20 MB are accepted." | Error | Manual dismiss |
| Max Players < Min Players | "Max Players must be greater than or equal to Min Players." | Error | Manual dismiss |
| Deactivate blocked — no confirmation | "Please tick the confirmation checkbox before deactivating." | Error | 4 s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No sports in catalog at all | "Catalog is Empty" | "No sports have been added to the group catalog. Add at least one sport to enable team registrations across all branches." | `[+ Add Sport]` (Role 97 only) |
| Filters return no results | "No Sports Match Your Filters" | "No sports match the selected filters. Adjust your filters or reset to view all catalog entries." | `[Reset Filters]` |
| Age group matrix with no active sports | "No Active Sports" | "The eligibility matrix will appear here once at least one sport is active in the catalog." | `[+ Add Sport]` (Role 97 only) |
| Rule document view — document missing | "No Rule Document Uploaded" | "No rule document has been uploaded for this sport." | `[Upload Rule Document]` (Role 97 only) |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load — KPI bar | 4 shimmer cards, full width of bar |
| Initial page load — catalog table | 8 shimmer rows with column-width-proportional shimmer blocks |
| Filter / search applied | Table area replaced by 20 px indigo spinner centred in the table zone while HTMX fetch is in-flight |
| Eligibility matrix load | Full matrix area shows a single grey shimmer block of equivalent height |
| Age group toggle in-flight | Clicked cell shows a 14 px spinner replacing the ✅/❌ icon; other cells remain interactive |
| `sport-create` / `sport-edit` drawer open | Drawer slides in immediately; no spinner (form is synchronously rendered server-side) |
| Rule document upload | Per-file progress bar inside the drawer: "Uploading rule document… [N]%" |
| Rule document modal open | Modal appears with PDF.js spinner until document bytes are loaded |
| `[Save Sport]` / `[Save Changes]` clicked | Submit button disabled, text changes to "Saving…" with inline spinner |
| `[Export Catalog ↓]` clicked | Button disabled, text: "Generating export…" with spinner; re-enabled on completion |

---

## 11. Role-Based UI Visibility

| UI Element | Role 97 — Sports Director | Role 98 — Sports Coordinator |
|---|---|---|
| KPI Summary Bar | Full | Full (read-only) |
| `[+ Add Sport]` button | Visible | Hidden |
| `[Export Catalog ↓]` button | Visible | Visible |
| Catalog table — all rows | Visible | Visible |
| `[Edit]` action column | Visible | Hidden |
| `[View Rules]` action column | Visible | Visible |
| `[Deactivate]` action column | Visible | Hidden |
| Bulk action bar | Visible | Hidden |
| Sport Name cell (as link) | Opens `sport-edit` drawer | Opens `sport-edit` drawer (read-only, pre-filled, no save) |
| Age group matrix cells | Clickable (toggle popover) | Read-only (no interaction) |
| Alert banners | Full detail, dismissible | Full detail, non-dismissible |
| `rule-document-view` modal | `[Download PDF]` + `[Replace Document]` | `[Download PDF]` only |
| `sport-deactivate` modal | Accessible | Inaccessible (no trigger rendered) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/sports/master/` | Roles 97, 98 | List all sports with filters: `category`, `gender`, `status`, `has_rule_document`, `search`, `page`, `page_size`, `ordering` |
| POST | `/api/v1/sports/master/` | Role 97 only | Create a new sport; `multipart/form-data` to support rule document upload |
| GET | `/api/v1/sports/master/{sport_id}/` | Roles 97, 98 | Retrieve full sport detail including R2 signed URL for rule document |
| PATCH | `/api/v1/sports/master/{sport_id}/` | Role 97 only | Update sport fields; re-evaluates team eligibility warnings if min/max players changed |
| POST | `/api/v1/sports/master/{sport_id}/deactivate/` | Role 97 only | Deactivates sport; returns count of affected active teams in response for banner display |
| POST | `/api/v1/sports/master/bulk-deactivate/` | Role 97 only | Body: `{ sport_ids: [uuid, …] }`; deactivates all listed sports |
| PATCH | `/api/v1/sports/master/{sport_id}/eligibility/` | Role 97 only | Body: `{ age_group: string, eligible: boolean }`; updates single cell in eligibility matrix |
| GET | `/api/v1/sports/master/eligibility-matrix/` | Roles 97, 98 | Returns all active sports × all age groups as a 2D structure for matrix render |
| GET | `/api/v1/sports/master/kpi-summary/` | Roles 97, 98 | Returns `{ total_sports, sports_with_active_teams, sports_no_teams, sports_missing_docs }` |
| POST | `/api/v1/sports/master/{sport_id}/rule-document/` | Role 97 only | Upload or replace rule document; `multipart/form-data`; stores to Cloudflare R2 |
| GET | `/api/v1/sports/master/export/` | Roles 97, 98 | Query params: all list filters + `format` (`xlsx` \| `pdf`); returns file download |
| GET | `/api/v1/sports/master/chart/teams-per-sport/` | Roles 97, 98 | Returns sport names + active team counts for Chart 7.1 |
| GET | `/api/v1/sports/master/chart/coverage-per-branch/` | Roles 97, 98 | Returns branch × sport presence matrix for Chart 7.2 |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar on page load | `load` | GET `/api/v1/sports/master/kpi-summary/` | `#sport-kpi-bar` | `innerHTML` |
| KPI bar after catalog mutation | `catalogUpdated from:body` | GET `/api/v1/sports/master/kpi-summary/` | `#sport-kpi-bar` | `innerHTML` |
| Catalog table on page load | `load` | GET `/api/v1/sports/master/?page=1` | `#sport-catalog-table` | `innerHTML` |
| Search / filter change | `change, input delay:400ms` | GET `/api/v1/sports/master/` (includes all filter params via `hx-include`) | `#sport-catalog-table` | `innerHTML` |
| Pagination click | `click` | GET `/api/v1/sports/master/?page=N` | `#sport-catalog-table` | `innerHTML` |
| Column header sort click | `click` | GET `/api/v1/sports/master/?ordering=field` | `#sport-catalog-table` | `innerHTML` |
| `[+ Add Sport]` button | `click` | GET `/htmx/sports/master/create-drawer/` | `#drawer-container` | `innerHTML` |
| `[Edit]` / Sport Name link | `click` | GET `/htmx/sports/master/{sport_id}/edit-drawer/` | `#drawer-container` | `innerHTML` |
| `sport-create` / `sport-edit` form submit | `submit` | POST/PATCH `/api/v1/sports/master/` (or `/{sport_id}/`) | `#sport-catalog-table` | `innerHTML` |
| `[Deactivate]` action | `click` | GET `/htmx/sports/master/{sport_id}/deactivate-modal/` | `#modal-container` | `innerHTML` |
| Deactivate confirm submit | `click` | POST `/api/v1/sports/master/{sport_id}/deactivate/` | `#sport-catalog-table` | `innerHTML` |
| `[View Rules]` action | `click` | GET `/htmx/sports/master/{sport_id}/rule-document-modal/` | `#modal-container` | `innerHTML` |
| Eligibility matrix load | `load` | GET `/api/v1/sports/master/eligibility-matrix/` | `#eligibility-matrix` | `innerHTML` |
| Age group cell toggle confirm | `click` | PATCH `/api/v1/sports/master/{sport_id}/eligibility/` | `#matrix-row-{sport_id}` | `outerHTML` |
| Category field change (show/hide player count fields) | `change` | GET `/htmx/sports/master/conditional-fields/?category=team` | `#player-count-fields` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
