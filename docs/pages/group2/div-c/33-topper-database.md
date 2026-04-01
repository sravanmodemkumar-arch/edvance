# Page 33: Topper Database

**URL:** `/group/adm/alumni/toppers/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions
**Module:** Alumni

---

## 1. Purpose

The Topper Database is the curated record of every outstanding academic achiever produced by the group across all branches — board exam rank holders, JEE and NEET rankers, NTSE/KVPY awardees, and state-level academic stars. For coaching institutes of the calibre of Narayana and Sri Chaitanya, the topper list is not merely a record of past success; it is the primary marketing asset. Prospective students and their parents choose a coaching institute primarily on the strength of its published results. A well-managed topper database, with verified ranks, professional photographs, and compelling quotes, feeds directly into admissions brochures, website banners, outdoor advertising, and social media campaigns.

The Alumni Relations Manager uses this page to collect topper records from branch principals at the end of each exam cycle, verify the rank and score details against official result sheets, gather photographs and personal quotes, and publish the profiles to the group's website through a managed integration. The publication workflow is deliberate: profiles pass through Draft → Published → Featured states, with Featured profiles appearing in the prominent banner sections of the website and admissions materials. The ability to drag-and-reorder featured toppers enables the marketing team to curate the most impactful profiles for the homepage without developer involvement.

Beyond marketing, the topper database serves an admissions intelligence function. Branch-level topper counts reveal which branches are producing the highest concentration of top performers — data that the Admissions Director can use to defend premium fee structures for top branches or identify branches whose academic quality needs improvement. The pending-completion alerts ensure that high-value profiles (a JEE rank holder with no photograph or a board topper with no quote) do not sit idle in draft state while the admission season passes, preventing the common institutional failure of having great results but failing to publicize them.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Alumni Relations Manager (28) | G3 | Full CRUD — create, edit, publish, feature, export | Primary owner |
| Group Admissions Director (23) | G3 | View + feature approval (Featured status requires Director sign-off if configured) | Strategic oversight |
| Group Marketing Director | G3 | View + feature and publish for marketing use | Marketing publication role |
| CEO / Principal | G3 | View-only (strategic visibility) | No edit permissions |

Access enforcement: All views protected with `@login_required` and `@role_required(['alumni_manager', 'admissions_director', 'marketing_director', 'ceo'])`. Feature approval gate enforced in Django view: `if profile.status == 'featured' and not request.user.has_perm('approve_featured_topper'): raise PermissionDenied`.

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal → Admissions → Alumni → Topper Database`

### 3.2 Page Header
**Title:** Topper Database
**Subtitle:** Academic achievers, rankers, and awardees across all branches
**Actions (right-aligned):**
- `[+ Add Topper]` — primary button, opens topper-profile-editor drawer in create mode
- `[Export for Marketing]` — secondary button (exports published toppers with photo URLs and rank details)

### 3.3 Alert Banner

| Condition | Banner Type | Message |
|---|---|---|
| Profiles without photo > 10 | Warning (amber) | "N topper profiles are missing photos. [Review Incomplete Profiles →]" |
| New exam cycle results not yet entered | Info (blue) | "JEE Advanced [Year] results are out. [Add Toppers for This Cycle →]" |
| Featured toppers homepage slots empty | Warning (amber) | "No toppers are currently featured for the homepage. [Feature Toppers →]" |
| Bulk publish completed | Success (green) | "N profiles published successfully." |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Toppers in Database | COUNT all topper records | `toppers` | Blue always | No drill-down |
| Board Toppers | COUNT toppers WHERE achievement_type IN (Board_10th, Board_12th) | `toppers` | Blue always | Filters table to board toppers |
| JEE / NEET Rankers | COUNT toppers WHERE achievement_type IN (JEE_Rank, NEET_Rank) | `toppers` | Blue always | Filters table to JEE/NEET |
| State Rank Holders | COUNT toppers WHERE achievement_type = State_Topper | `toppers` | Blue always | Filters table to state toppers |
| Published Profiles | COUNT toppers WHERE status IN (Published, Featured) | `toppers` | Green if ≥ 80% of total; amber if 50–79%; red if < 50% | Filters table to published |
| Pending Photo / Verification | COUNT toppers WHERE photo IS NULL OR verified = False | `toppers` | Red if > 0; green if 0 | Scrolls to Section 5.4 |

**HTMX auto-refresh pattern (every 5 minutes):**
```html
<div id="kpi-bar"
     hx-get="/group/adm/alumni/toppers/kpis/"
     hx-trigger="load, every 300s"
     hx-target="#kpi-bar"
     hx-swap="outerHTML">
  <!-- KPI cards rendered here -->
</div>
```

---

## 5. Sections

### 5.1 Topper Table

**Display:** Full-width sortable, selectable, server-side paginated table (20 rows/page). Default sort: batch_year descending, then score/rank ascending.

**Columns:**

| Column | Notes |
|---|---|
| Checkbox | For bulk selection |
| Topper ID | Auto-generated, e.g. TOP-0221 |
| Name | Full name |
| Branch | Branch attended |
| Batch Year | Year of achievement, e.g. 2024 |
| Achievement Type | Board 1st / JEE Rank / NEET Rank / NTSE / State Topper / Group Topper (colour-coded badge) |
| Score / Rank | e.g. "AIR 47" or "99.2%" |
| College Admitted | College name |
| Profile Status | Draft / Published / Featured (colour-coded badge) |
| Photo | Yes (green dot) / No (red dot) |
| Actions | `[View →]` `[Edit →]` `[Publish]` (if Draft) `[Feature]` (if Published) |

**Filters:**
- Achievement type (multi-select)
- Branch (dropdown)
- Batch year (from / to)
- Profile status (Draft / Published / Featured / All)

**Search:** Name, college name, rank/score

**Bulk actions:**
- `[Publish Selected]` — sets status to Published for all selected Draft profiles
- `[Feature Selected]` — sets status to Featured (requires Director approval if configured)
- `[Export for Marketing]` — exports selected profiles with rank, photo URL, quote

**HTMX:** Filter inputs use `hx-get="/group/adm/alumni/toppers/table/"` with `hx-trigger="change"`, `hx-target="#toppers-table"`. Pagination: `hx-get` with `?page=N`.

**Empty state:** "No topper profiles match the selected filters."

---

### 5.2 Achievement Distribution (Bar Chart)

**Display:** Chart.js 4.x grouped bar chart. X-axis: batch years (last 5 years). Y-axis: count. Series: one bar per achievement type (Board 1st / JEE Rank / NEET Rank / NTSE / State Topper / Group Topper). Each year shows a cluster of bars.

**Tooltip:** Year, achievement type, count.

**HTMX:** `hx-get="/group/adm/alumni/toppers/achievement-chart/"` lazy-loaded on `intersect once`.

---

### 5.3 Branch Topper Leaderboard

**Display:** Sortable table. Branches ranked by total toppers produced. Default sort: Total descending.

**Columns:**

| Column | Notes |
|---|---|
| Rank | # |
| Branch | Branch name |
| JEE Rankers | Count |
| NEET Rankers | Count |
| Board Toppers | Count (10th + 12th combined) |
| NTSE / State | Count |
| Total | Grand total (primary sort column) |

**HTMX:** `hx-get="/group/adm/alumni/toppers/branch-leaderboard/"` loaded on section init.

**Empty state:** "No topper data to rank branches. Add topper records to populate this table."

---

### 5.4 Profiles Pending Completion

**Display:** Alert-style list panel. Shows topper records where photo is missing, rank/score is unverified, or key fields (college, quote) are incomplete.

**Each entry shows:**
Topper name | Branch | Achievement type | Batch year | Missing fields (comma-separated: "Photo, Quote, College") | `[Send Completion Request →]` button

**Send Completion Request:** Opens a lightweight modal to send a WhatsApp/email message to the branch principal requesting the missing details. `hx-post="/group/adm/alumni/toppers/{id}/completion-request/"`.

**HTMX:** `hx-get="/group/adm/alumni/toppers/pending-completion/"` on page load.

**Empty state (positive):** "All topper profiles are complete. Ready for publication."

---

### 5.5 Featured Toppers Strip

**Display:** Card grid (horizontal scrollable row). Each card: topper photo (from Cloudflare R2), name, rank/achievement, batch year, college admitted. Cards are drag-to-reorder (for homepage display priority). Maximum 12 featured slots shown.

**Card actions:**
- `[Unfeature]` — removes from Featured strip, returns to Published
- Reorder handle (drag icon left edge of card)

**Homepage priority note:** Card order determines display order on the group website homepage. Dragging saves position via `hx-post="/group/adm/alumni/toppers/feature-order/"` with ordered IDs.

**HTMX:** Strip loaded via `hx-get="/group/adm/alumni/toppers/featured/"` on page load. Reorder post: `hx-post="/group/adm/alumni/toppers/feature-order/"`, `hx-target="#featured-strip"`, `hx-swap="innerHTML"`.

**Empty state:** "No toppers are currently featured. Publish profiles and use `[Feature]` to add them here."

---

## 6. Drawers & Modals

### 6.1 `topper-profile-editor` Drawer
**Width:** 640px
**Trigger:** `[+ Add Topper]` or `[Edit →]` in table
**HTMX endpoint:** `hx-get="/group/adm/alumni/toppers/create/"` or `hx-get="/group/adm/alumni/toppers/edit/{id}/"` lazy-loaded
**Tabs:**
1. **Basic Info** — Name, DOB, branch, batch year, stream, class
2. **Achievement Details** — Achievement type (dropdown), score/rank, subject (for board toppers), exam name and year, verification status toggle
3. **Photo Upload** — Upload profile photo (stored on Cloudflare R2; max 2MB; JPEG/PNG only); existing photo preview; remove button
4. **Quote** — Topper's testimonial quote (textarea, max 300 chars); attributed name and class display
5. **Social Links** — LinkedIn URL, Instagram URL (optional)
6. **Publication Settings** — Status (Draft / Published / Featured); visibility on website toggle; branch-specific display toggle
7. **Preview** — Read-only card preview showing how profile will appear on website

---

### 6.2 `publish-confirm-modal` Modal
**Width:** 400px
**Trigger:** `[Publish]` action button in table or bulk publish
**HTMX endpoint:** `hx-get="/group/adm/alumni/toppers/publish-confirm/{id}/"` lazy-loaded
**Content:**
- Summary of profile (name, achievement, photo status, verification status)
- Warning if photo is missing: "Profile has no photo. Publish anyway?"
- `[Confirm Publish]` — `hx-post="/group/adm/alumni/toppers/{id}/publish/"`
- `[Cancel]` — closes modal

---

### 6.3 `feature-manager` Drawer
**Width:** 480px
**Trigger:** `[Feature]` action in table
**HTMX endpoint:** `hx-get="/group/adm/alumni/toppers/feature/{id}/"` lazy-loaded
**Content:**
- Profile summary
- Current featured count (e.g., "8 of 12 feature slots used")
- Feature position (slot number input, 1–12)
- Display duration option (Permanent / Until date)
- Notify website team? (toggle)
- `[Confirm Feature]` — `hx-post="/group/adm/alumni/toppers/{id}/feature/"`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Topper created | "Topper profile for [Name] created as Draft." | Success | 4s |
| Topper updated | "Profile updated successfully." | Success | 3s |
| Profile published | "[Name]'s profile is now published." | Success | 4s |
| Profile featured | "[Name] added to Featured strip at position N." | Success | 4s |
| Unfeatured | "[Name] removed from Featured strip." | Info | 3s |
| Bulk publish | "N profiles published successfully." | Success | 4s |
| Completion request sent | "Completion request sent to [Branch] principal." | Success | 3s |
| Feature order saved | "Homepage feature order updated." | Success | 2s |
| Photo upload success | "Photo uploaded and saved to Cloudflare R2." | Success | 3s |
| Photo upload failed | "Photo upload failed. File must be JPEG/PNG under 2MB." | Error | 5s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No topper records yet | Trophy outline | "No toppers added yet" | "Add topper records for the latest exam cycle to start building the database." | `[+ Add Topper →]` |
| No results matching filters | Filter icon | "No toppers match your filters" | "Try adjusting achievement type, branch, or batch year." | `[Clear Filters]` |
| Pending completion — all complete | Shield checkmark | "All profiles complete" | "No topper profiles are missing photos or details." | None |
| Featured strip empty | Star outline | "No featured toppers" | "Publish topper profiles and mark them as Featured to populate this strip." | `[View Published Toppers]` |
| Branch leaderboard — no data | Trophy outline | "No branch data yet" | "Branch rankings will appear once topper records are added." | None |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load (KPI bar) | Skeleton cards (6 cards, grey shimmer) |
| Topper table loading | Skeleton rows (5 rows, column placeholders) |
| Achievement distribution chart | Skeleton grouped bars |
| Branch leaderboard loading | Skeleton rows (5 rows) |
| Pending completion list loading | Skeleton list rows (4 rows) |
| Featured strip loading | Skeleton cards (4 cards horizontal) |
| Drawer opening | Spinner centred in drawer body |
| Photo upload in progress | Upload progress bar in drawer Photo tab |
| Bulk publish in progress | Button spinner + "Publishing N profiles…" label |
| KPI auto-refresh | Subtle pulse on KPI cards |

---

## 10. Role-Based UI Visibility

All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Alumni Manager (28) | Admissions Director (23) | Marketing Director | CEO |
|---|---|---|---|---|
| `[+ Add Topper]` button | Visible | Hidden | Hidden | Hidden |
| `[Edit →]` action | Visible | Hidden | Hidden | Hidden |
| `[Publish]` action | Visible | Visible | Visible | Hidden |
| `[Feature]` action | Visible | Visible (with approval) | Visible | Hidden |
| `[Unfeature]` on strip card | Visible | Hidden | Visible | Hidden |
| Drag-to-reorder on featured strip | Visible | Hidden | Visible | Hidden |
| Bulk publish/feature buttons | Visible | Hidden | Visible | Hidden |
| `[Send Completion Request →]` | Visible | Hidden | Hidden | Hidden |
| `[Export for Marketing]` | Visible | Visible | Visible | Hidden |
| Publication Settings tab in editor | Visible | Hidden | Visible | Hidden |
| Preview tab in editor | Visible | Visible | Visible | Visible |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/alumni/toppers/kpis/` | JWT G3+ | KPI bar metrics |
| GET | `/api/v1/group/{group_id}/adm/alumni/toppers/` | JWT G3+ | List toppers with filters |
| POST | `/api/v1/group/{group_id}/adm/alumni/toppers/` | JWT G3 write | Create topper profile |
| GET | `/api/v1/group/{group_id}/adm/alumni/toppers/{id}/` | JWT G3+ | Get topper detail |
| PATCH | `/api/v1/group/{group_id}/adm/alumni/toppers/{id}/` | JWT G3 write | Update topper profile |
| POST | `/api/v1/group/{group_id}/adm/alumni/toppers/{id}/publish/` | JWT G3 write | Publish topper profile |
| POST | `/api/v1/group/{group_id}/adm/alumni/toppers/{id}/feature/` | JWT G3 write | Feature topper profile |
| POST | `/api/v1/group/{group_id}/adm/alumni/toppers/{id}/unfeature/` | JWT G3 write | Remove from featured |
| POST | `/api/v1/group/{group_id}/adm/alumni/toppers/feature-order/` | JWT G3 write | Save featured strip order |
| POST | `/api/v1/group/{group_id}/adm/alumni/toppers/bulk-publish/` | JWT G3 write | Bulk publish selected profiles |
| GET | `/api/v1/group/{group_id}/adm/alumni/toppers/achievement-chart/` | JWT G3+ | Achievement distribution chart data |
| GET | `/api/v1/group/{group_id}/adm/alumni/toppers/branch-leaderboard/` | JWT G3+ | Branch topper leaderboard |
| GET | `/api/v1/group/{group_id}/adm/alumni/toppers/pending-completion/` | JWT G3+ | Profiles with missing photo or data |
| POST | `/api/v1/group/{group_id}/adm/alumni/toppers/{id}/completion-request/` | JWT G3 write | Send completion request to branch |
| GET | `/api/v1/group/{group_id}/adm/alumni/toppers/featured/` | JWT G3+ | Featured toppers for strip |
| POST | `/api/v1/group/{group_id}/adm/alumni/toppers/{id}/photo/` | JWT G3 write | Upload photo to Cloudflare R2 |
| GET | `/api/v1/group/{group_id}/adm/alumni/toppers/export/` | JWT G3+ | Export toppers for marketing |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 300s` | GET `/group/adm/alumni/toppers/kpis/` | `#kpi-bar` | `outerHTML` |
| Filter change → reload table | `change` on filter inputs | GET `/group/adm/alumni/toppers/table/` | `#toppers-table` | `innerHTML` |
| Table pagination | `click` on page link | GET `/group/adm/alumni/toppers/table/?page=N` | `#toppers-table` | `innerHTML` |
| Lazy load achievement chart | `intersect once` | GET `/group/adm/alumni/toppers/achievement-chart/` | `#achievement-chart` | `innerHTML` |
| Load branch leaderboard | `load` | GET `/group/adm/alumni/toppers/branch-leaderboard/` | `#branch-leaderboard` | `innerHTML` |
| Load pending completion list | `load` | GET `/group/adm/alumni/toppers/pending-completion/` | `#pending-completion-panel` | `innerHTML` |
| Load featured strip | `load` | GET `/group/adm/alumni/toppers/featured/` | `#featured-strip` | `innerHTML` |
| Open topper editor drawer | `click` on `[+ Add Topper]` or `[Edit →]` | GET `/group/adm/alumni/toppers/create/` or `/edit/{id}/` | `#drawer-container` | `innerHTML` |
| Open publish confirm modal | `click` on `[Publish]` | GET `/group/adm/alumni/toppers/publish-confirm/{id}/` | `#modal-container` | `innerHTML` |
| Confirm publish | `click` on `[Confirm Publish]` | POST `/group/adm/alumni/toppers/{id}/publish/` | `#toppers-table` | `innerHTML` |
| Open feature manager drawer | `click` on `[Feature]` | GET `/group/adm/alumni/toppers/feature/{id}/` | `#drawer-container` | `innerHTML` |
| Confirm feature | `click` on `[Confirm Feature]` | POST `/group/adm/alumni/toppers/{id}/feature/` | `#featured-strip` | `innerHTML` |
| Unfeature from strip | `click` on `[Unfeature]` | POST `/group/adm/alumni/toppers/{id}/unfeature/` | `#featured-strip` | `innerHTML` |
| Featured strip reorder save | `end` (drag event) | POST `/group/adm/alumni/toppers/feature-order/` | `#feature-order-status` | `innerHTML` |
| Send completion request | `click` on `[Send Completion Request →]` | POST `/group/adm/alumni/toppers/{id}/completion-request/` | `#completion-row-{id}` | `outerHTML` |
| Bulk publish selected | `click` (after confirm) | POST `/group/adm/alumni/toppers/bulk-publish/` | `#toppers-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
