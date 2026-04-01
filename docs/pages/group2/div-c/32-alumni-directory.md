# 32 — Alumni Directory

**URL:** `/group/adm/alumni/directory/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions
**Module:** Alumni

---

## 1. Purpose

The Alumni Directory is the authoritative searchable database of all graduates and former students across every branch in the group. For coaching institutes with histories spanning two or more decades, this database may contain upwards of 50,000 records — each representing a student whose experience with the group is a potential asset for future admissions. The Alumni Relations Manager maintains this directory as a living record: adding the current year's passing-out batch each cycle, updating contact information when alumni reach out, tracking their academic and career progression post-enrollment, and flagging those who have gone on to achieve outcomes the group can celebrate publicly.

The directory serves multiple operational functions simultaneously. For the admissions team, it is the source list for referral outreach — alumni who enrolled their siblings, cousins, or neighbors are the group's most credible marketing voice. For the marketing team, it is the talent pool for testimonials, topper profiles, and alumni-led campus visits. For leadership, it is the proof of institutional impact — a record of how many students the group has shaped and where they have gone. Each of these use cases requires different data fields and workflows, all of which are surfaced through this single page with appropriate role-based filtering.

The bulk import feature is particularly critical at the end of each academic year, when the passing-out batch from all branches must be added to the directory simultaneously. The CSV upload mechanism accepts a standard template with validation rules, identifies duplicate records, and reports errors before committing any inserts. The Alumni Relations Manager uses this to onboard hundreds or thousands of new alumni records per cycle without manual data entry, maintaining the directory's completeness as the group's enrollment base grows.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Alumni Relations Manager (28) | G3 | Full CRUD — view, create, edit, delete, bulk import, export | Primary owner |
| Group Admissions Director (23) | G3 | View-only + export | Strategic oversight, no edit |
| Group Admission Coordinator (24) | G3 | View referral-creation fields only; no personal data editing | Can create referral from alumni profile |
| Group Demo Class Coordinator (29) | G3 | No access | Not relevant to this module |

Access enforcement: All views protected with `@login_required` and `@role_required(['alumni_manager', 'admissions_director', 'admission_coordinator'])`. Coordinator's view scoped to `select_related('referrals_made')` only — personal contact details masked in template for this role.

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal → Admissions → Alumni → Directory`

### 3.2 Page Header
**Title:** Alumni Directory
**Subtitle:** Searchable database of all group alumni across branches
**Actions (right-aligned):**
- `[+ Add Alumni]` — primary button, opens alumni-edit-form drawer
- `[Bulk Import]` — secondary button, opens bulk-import-result drawer
- `[Export Directory CSV]` — secondary button

### 3.3 Alert Banner

| Condition | Banner Type | Message |
|---|---|---|
| New passing-out batch not yet imported | Warning (amber) | "The [Year] passing-out batch has not been imported. [Start Bulk Import →]" |
| Bulk import completed with errors | Warning (amber) | "Bulk import completed with N errors. [View Error Report →]" |
| Alumni with unverified contact > 30% of total | Info (blue) | "N% of alumni have unverified contact details. Consider a contact verification drive." |
| Bulk import succeeded | Success (green) | "N alumni records imported successfully." |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Total Alumni | COUNT all alumni records in directory | `alumni` | Blue always | No drill-down |
| New Alumni This Year | COUNT alumni WHERE year_of_passing = current_year | `alumni` | Blue always | Filters table to current year |
| Alumni with Verified Contact % | COUNT verified / total × 100 | `alumni` WHERE contact_status = Verified | Green if ≥ 80%; amber if 60–79%; red if < 60% | Filters to unverified |
| Alumni Who Made Referrals | COUNT distinct alumni WHERE referrals_made_count > 0 | `alumni` JOIN `referrals` | Blue always | Filters to referral-makers |
| Profiles with Career Update | COUNT alumni WHERE career_update IS NOT NULL | `alumni` | Amber if < 50%; green if ≥ 50% | No drill-down |
| Alumni by Branch (Top) | Bar micro-chart showing top 5 branches | `alumni` GROUP BY branch | Blue always | Scrolls to chart section |

**HTMX auto-refresh pattern (every 5 minutes):**
```html
<div id="kpi-bar"
     hx-get="/group/adm/alumni/directory/kpis/"
     hx-trigger="load, every 300s"
     hx-target="#kpi-bar"
     hx-swap="outerHTML">
  <!-- KPI cards rendered here -->
</div>
```

---

## 5. Sections

### 5.1 Alumni Table

**Display:** Full-width sortable, selectable, server-side paginated table (20 rows/page). Default sort: year_of_passing descending.

**Columns:**

| Column | Notes |
|---|---|
| Checkbox | For bulk selection |
| Alumni ID | Auto-generated, e.g. ALM-00421 |
| Name | Full name |
| Branch | Branch attended |
| Year of Passing | e.g. 2023 |
| Stream | MPC / BiPC / MEC / CEC |
| Class | Intermediate / School (10th) / Other |
| College Admitted | College name (if captured) |
| Career Update | Brief current status (e.g., "IIT Bombay – CS 2nd year") |
| Contact Status | Verified / Unverified / Inactive (colour-coded badge) |
| Referrals Made | Count (linked to referral tracker) |
| Actions | `[View →]` opens alumni-profile drawer; `[Edit →]` opens alumni-edit-form drawer |

**Search:** Full-text search across: name, phone (masked display), email, college admitted

**Filters:**
- Branch (multi-select dropdown)
- Year of passing (from / to)
- Stream (MPC / BiPC / MEC / CEC / All)
- Contact status (Verified / Unverified / Inactive / All)
- College (text filter)
- Has made referral (Yes / No / All)

**Bulk actions (appear when rows selected):**
- `[Export Selected CSV]`
- `[Send WhatsApp Message to Selected]` — opens message-composer modal
- `[Mark Inactive]` — with confirmation dialog

**HTMX:** Filter and search inputs use `hx-get="/group/adm/alumni/directory/table/"` with `hx-trigger="input delay:400ms"` (for search) and `hx-trigger="change"` (for dropdowns), targeting `#alumni-table` with `hx-swap="innerHTML"`. Pagination: `hx-get` with `?page=N`.

**Empty state:** "No alumni match the current search and filter criteria."

---

### 5.2 Alumni by Year Chart

**Display:** Chart.js 4.x line chart. X-axis: years (from group founding year to current). Y-axis: number of alumni added per year. Shows the group's growth trajectory.

**Tooltip:** Year, alumni count for that year.

**HTMX:** `hx-get="/group/adm/alumni/directory/by-year-chart/"` lazy-loaded on section scroll (`hx-trigger="intersect once"`), `hx-target="#alumni-by-year-chart"`.

---

### 5.3 Top Colleges (Bar Chart)

**Display:** Chart.js 4.x horizontal bar chart. Y-axis: college categories (IIT / NIT / AIIMS / State University / Other Engineering / Other Medical / Others). X-axis: count of alumni admitted to each category.

**Tooltip:** Category, count, % of total alumni with college data.

**HTMX:** `hx-get="/group/adm/alumni/directory/college-chart/"` lazy-loaded on intersect.

---

### 5.4 Branch-wise Alumni Count

**Display:** Chart.js 4.x horizontal bar chart. Y-axis: branches (sorted by count, highest at top). X-axis: total alumni count. Shows which branches have produced the most alumni.

**Clicking a branch bar** filters the alumni table to that branch via HTMX.

**HTMX:** `hx-get="/group/adm/alumni/directory/branch-chart/"` lazy-loaded on intersect. Bar click: `hx-get="/group/adm/alumni/directory/table/?branch=X"` targeting `#alumni-table`.

---

### 5.5 Bulk Import Panel

**Display:** Card panel with step-by-step import workflow.

**Steps:**
1. **Download Template** — `[Download CSV Template]` button (downloads `alumni_import_template.csv` with required column headers)
2. **Upload CSV** — File input (accepts .csv only, max 5MB). On file selection, shows row preview (first 5 rows) for verification.
3. **Validate** — `[Validate File]` — `hx-post="/group/adm/alumni/directory/import/validate/"` returns validation summary: rows found, errors (duplicate IDs, missing required fields, invalid year formats)
4. **Confirm & Import** — `[Confirm Import]` — available only after successful validation. `hx-post="/group/adm/alumni/directory/import/commit/"`

**HTMX:** Validation post targets `#import-validation-result` with `hx-swap="innerHTML"`. Commit post targets `#import-status-panel` with `hx-swap="innerHTML"` and refreshes KPI bar.

**Empty state (no file selected):** "Upload a CSV file with the alumni template to add new records in bulk."

---

## 6. Drawers & Modals

### 6.1 `alumni-profile` Drawer
**Width:** 640px
**Trigger:** `[View →]` in alumni table
**HTMX endpoint:** `hx-get="/group/adm/alumni/directory/profile/{alumni_id}/"` lazy-loaded
**Tabs:**
1. **Personal** — Name, DOB, gender, branch, stream, year of passing
2. **Academic History** — Class, subjects, exam scores (board, JEE/NEET if applicable), college admitted
3. **Career Path** — Current education/job, company/institution, last updated date, [Update Career →] inline form
4. **Referrals Made** — List of referrals submitted by this alumni (linked to referral tracker)
5. **Contact History** — Log of all contact attempts and outcomes
6. **Edit** — Full edit form (same as alumni-edit-form, embedded in tab)

---

### 6.2 `alumni-edit-form` Drawer
**Width:** 560px
**Trigger:** `[Edit →]` in table or `[+ Add Alumni]` header button
**HTMX endpoint:** `hx-get="/group/adm/alumni/directory/edit/{alumni_id}/"` (edit) or `hx-get="/group/adm/alumni/directory/create/"` (create) — lazy-loaded
**Fields:** Name, DOB, gender, phone, email, branch (dropdown), stream, year of passing, class, college admitted, career update, contact status
**Submit:** `hx-post` for create; `hx-patch` for edit. On success: refreshes table and shows toast.

---

### 6.3 `bulk-import-result` Drawer
**Width:** 480px
**Trigger:** `[Bulk Import]` header button or from alert banner
**HTMX endpoint:** `hx-get="/group/adm/alumni/directory/import/"` lazy-loaded
**Content:** Contains the full Bulk Import Panel (Section 5.5) in drawer format for users who prefer the drawer workflow. Also shows import history: last 5 imports with date, rows imported, errors.

---

### 6.4 Modal: `whatsapp-message-composer`
- **Width:** 560px
- **Trigger:** `[Send WhatsApp Message to Selected]` bulk action in Section 5.1
- **Fields:**
  - Selected alumni count (read-only info banner: "Sending to [N] alumni")
  - Message template (select dropdown): Select a template or write custom
  - Message body (textarea, max 1,024 chars — WhatsApp limit; char counter shown)
  - Include opt-out link (checkbox, default checked)
  - Schedule (radio: Send Now / Schedule for date+time)
- **Tabs:** Compose | Preview (rendered message preview) | Delivery History
- **Buttons:** `[Send Now]` / `[Schedule Send]` (primary) + `[Cancel]`
- **On confirm:** `hx-post="/api/v1/group/{group_id}/adm/alumni/bulk-whatsapp/"` → `hx-target="#bulk-action-result"` `hx-swap="innerHTML"` → toast "WhatsApp message queued for [N] alumni."
- **HTMX:** `hx-get="/api/v1/group/{group_id}/adm/alumni/whatsapp-composer-form/?ids={selected_ids}"` `hx-target="#modal-body"` `hx-swap="innerHTML"`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Alumni created | "Alumni [Name] added to directory." | Success | 4s |
| Alumni updated | "Alumni profile updated." | Success | 3s |
| Alumni marked inactive | "N alumni marked as inactive." | Warning | 4s |
| WhatsApp message sent | "WhatsApp message queued for N alumni." | Success | 4s |
| Export triggered | "CSV export is being prepared." | Info | 3s |
| Bulk import completed | "N alumni records imported. N errors found." | Success / Warning (conditional) | 5s |
| Bulk import validation failed | "N validation errors. Please fix the CSV and retry." | Error | 6s |
| Career update saved | "Career information updated for [Name]." | Success | 3s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| Directory empty (no records) | Silhouette group icon | "No alumni records yet" | "Import the first alumni batch using the Bulk Import tool, or add individual records." | `[Bulk Import →]` |
| No alumni matching search/filters | Search icon | "No alumni found" | "Try a different name, phone number, or adjust the year and branch filters." | `[Clear Filters]` |
| By-year chart — insufficient data | Bar chart outline | "Not enough data for chart" | "Alumni by year chart will render once records span at least 2 years." | None |
| College chart — no college data | Graduation cap outline | "No college data available" | "College information will appear as alumni records are updated." | None |
| Branch-wise alumni count chart (5.4) empty | Building icon | "No Branch Data Available" | "Alumni records have not yet been assigned to branches. Import alumni records with branch data to populate this chart." | `[Import Alumni]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load (KPI bar) | Skeleton cards (6 cards, grey shimmer) |
| Alumni table loading | Skeleton rows (8 rows, column placeholders) |
| Search / filter (table reload) | Skeleton rows (5 rows) during HTMX fetch |
| By-year chart loading | Skeleton chart area (line chart placeholder) |
| College chart loading | Skeleton horizontal bars (7 rows) |
| Branch chart loading | Skeleton horizontal bars (5 rows) |
| Drawer opening (any) | Spinner centred in drawer body |
| Bulk import validation | Spinner in validate button + "Validating…" label |
| Bulk import commit | Progress bar in import panel |
| KPI auto-refresh | Subtle pulse on KPI cards |

---

## 10. Role-Based UI Visibility

All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Alumni Manager (28) | Admissions Director (23) | Admission Coordinator (24) |
|---|---|---|---|
| `[+ Add Alumni]` button | Visible | Hidden | Hidden |
| `[Bulk Import]` button | Visible | Hidden | Hidden |
| `[Edit →]` action in table | Visible | Hidden | Hidden |
| Alumni profile — Edit tab | Visible | Hidden | Hidden |
| Contact details (phone, email) | Visible (full) | Visible (masked) | Hidden / masked |
| `[Mark Inactive]` bulk action | Visible | Hidden | Hidden |
| `[Send WhatsApp]` bulk action | Visible | Hidden | Hidden |
| `[Export Directory CSV]` | Visible | Visible | Hidden |
| Bulk import panel | Visible | Hidden | Hidden |
| Referrals Made column | Visible | Visible | Visible |
| Career update column | Visible | Visible | Visible |
| KPI cards (all) | Visible | Visible | Partial (referral KPIs only) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/alumni/kpis/` | JWT G3+ | KPI bar metrics |
| GET | `/api/v1/group/{group_id}/adm/alumni/` | JWT G3+ | List alumni with filters and search |
| POST | `/api/v1/group/{group_id}/adm/alumni/` | JWT G3 write | Create new alumni record |
| GET | `/api/v1/group/{group_id}/adm/alumni/{id}/` | JWT G3+ | Get alumni profile detail |
| PATCH | `/api/v1/group/{group_id}/adm/alumni/{id}/` | JWT G3 write | Update alumni record |
| POST | `/api/v1/group/{group_id}/adm/alumni/bulk-mark-inactive/` | JWT G3 write | Bulk mark alumni as inactive |
| GET | `/api/v1/group/{group_id}/adm/alumni/by-year-chart/` | JWT G3+ | Alumni count per year for chart |
| GET | `/api/v1/group/{group_id}/adm/alumni/college-chart/` | JWT G3+ | Alumni by college category |
| GET | `/api/v1/group/{group_id}/adm/alumni/branch-chart/` | JWT G3+ | Alumni count per branch |
| POST | `/api/v1/group/{group_id}/adm/alumni/import/validate/` | JWT G3 write | Validate CSV import file |
| POST | `/api/v1/group/{group_id}/adm/alumni/import/commit/` | JWT G3 write | Commit validated import |
| GET | `/api/v1/group/{group_id}/adm/alumni/export/` | JWT G3+ | Export alumni directory as CSV |
| POST | `/api/v1/group/{group_id}/adm/alumni/bulk-whatsapp/` | JWT G3 write | Queue WhatsApp messages to selected alumni |
| GET | `/api/v1/group/{group_id}/adm/alumni/whatsapp-composer-form/` | JWT G3 | Load WhatsApp message composer modal |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 300s` | GET `/group/adm/alumni/directory/kpis/` | `#kpi-bar` | `outerHTML` |
| Search input → reload table | `input delay:400ms` | GET `/group/adm/alumni/directory/table/` | `#alumni-table` | `innerHTML` |
| Filter change → reload table | `change` on filter dropdown | GET `/group/adm/alumni/directory/table/` | `#alumni-table` | `innerHTML` |
| Table pagination | `click` on page link | GET `/group/adm/alumni/directory/table/?page=N` | `#alumni-table` | `innerHTML` |
| Branch bar click → filter table | `click` on chart bar | GET `/group/adm/alumni/directory/table/?branch=X` | `#alumni-table` | `innerHTML` |
| Lazy load by-year chart | `intersect once` | GET `/group/adm/alumni/directory/by-year-chart/` | `#alumni-by-year-chart` | `innerHTML` |
| Lazy load college chart | `intersect once` | GET `/group/adm/alumni/directory/college-chart/` | `#college-chart` | `innerHTML` |
| Lazy load branch chart | `intersect once` | GET `/group/adm/alumni/directory/branch-chart/` | `#branch-chart` | `innerHTML` |
| Open alumni profile drawer | `click` on `[View →]` | GET `/group/adm/alumni/directory/profile/{id}/` | `#drawer-container` | `innerHTML` |
| Open alumni edit drawer | `click` on `[Edit →]` or `[+ Add Alumni]` | GET `/group/adm/alumni/directory/edit/{id}/` or `/create/` | `#drawer-container` | `innerHTML` |
| Submit alumni create/edit | `submit` in form | POST/PATCH `/group/adm/alumni/` or `/{id}/` | `#alumni-table` | `innerHTML` |
| Import file validation | `click` on `[Validate File]` | POST `/group/adm/alumni/directory/import/validate/` | `#import-validation-result` | `innerHTML` |
| Import commit | `click` on `[Confirm Import]` | POST `/group/adm/alumni/directory/import/commit/` | `#import-status-panel` | `innerHTML` |
| Open bulk import drawer | `click` on `[Bulk Import]` | GET `/group/adm/alumni/directory/import/` | `#drawer-container` | `innerHTML` |
| Bulk mark inactive | `click` (after confirm) | POST `/group/adm/alumni/bulk-mark-inactive/` | `#alumni-table` | `innerHTML` |
| Open WhatsApp message composer | `click from:#btn-bulk-whatsapp` | GET `.../alumni/whatsapp-composer-form/?ids={ids}` | `#modal-body` | `innerHTML` |
| Send bulk WhatsApp messages | `click from:#btn-send-whatsapp` | POST `.../alumni/bulk-whatsapp/` | `#bulk-action-result` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
