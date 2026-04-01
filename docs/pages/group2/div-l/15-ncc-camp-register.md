# 15 — NCC Camp Register

> **URL:** `/group/nss/ncc-camps/`
> **File:** `15-ncc-camp-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Group NSS/NCC Coordinator (Role 100, G3) — full

---

## 1. Purpose

Register of National Cadet Corps (NCC) camps and training activities across all branches in the group. NCC cadets must attend the Annual Training Camp (ATC) and the Combined Annual Training Camp (CATC) — both are mandatory requirements for progression to the next NCC certificate level (A, B, or C) and for eligibility for prestigious events such as the Republic Day Camp in New Delhi. Missing mandatory camps blocks a cadet from receiving their certificate and counts against the branch's NCC performance report submitted to the NCC Directorate.

The Group NSS/NCC Coordinator uses this page to: maintain a complete register of all camps (upcoming, ongoing, and completed) across the academic year; nominate cadets from each branch for specific camps; record actual attendance and mark per-day presence for multi-day camps; track certificate issuance post-camp; manage NCC officer assignments per delegation; and export nomination lists and attendance reports for the NCC Directorate. Camps are organised by NCC Directorates at the district or state level, but the group is responsible for coordinating all cadet nominations and logistics across its branches.

Scale: Large groups manage 500–3,000 NCC cadets across Army, Naval, Air, and Girls Divisions. Camps run year-round with many running simultaneously across different wings. The camp register may contain 30–80 camp entries per academic year.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group NSS/NCC Coordinator | 100 | G3 | Full — create camps, edit, record attendance, issue certificates, manage cadet registry, export | Sole owner |
| Group Sports Director | 97 | G3 | No access | Redirected to own dashboard |
| Group Cultural Activities Head | 99 | G3 | No access | Redirected to own dashboard |
| Group Library Head | 101 | G2 | No access | Redirected to own dashboard |
| All other roles | — | — | No access | Redirected to own dashboard |

> **Access enforcement:** Django decorator `@require_role(['nss_ncc_coordinator'])` on all views and API endpoints for this page. No read-only partial access is granted to any other role.

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group HQ  ›  Sports & Extra-Curricular  ›  NCC  ›  NCC Camp Register
```

### 3.2 Page Header

```
NCC Camp Register                              [+ Add Camp]  [+ Register Cadets]  [Export ↓]
Group NSS/NCC Coordinator — [Officer Name]
AY [YYYY-YY]  ·  [N] Camps This AY  ·  [N] Total Cadets  ·  [N] Mandatory Camps Attended  ·  [N] Certificates Issued
```

`[+ Add Camp]` — opens `ncc-camp-create` drawer.
`[+ Register Cadets]` — opens a branch-select modal leading to bulk cadet import (CSV template) for that branch's NCC unit.
`[Export ↓]` — exports filtered camp register to XLSX or PDF.

### 3.3 Alert Banners (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| ATC/CATC camps exist with 0 nominations from some branches | "[N] branch(es) have not nominated any cadets for mandatory ATC/CATC camps." | Red |
| Camps with end date passed and attendance not recorded | "[N] completed camp(s) have no attendance recorded. Record attendance to enable certificate issuance." | Yellow |
| Upcoming camp registration deadline in ≤ 3 days | "Registration deadline for '[Camp Name]' is in [N] day(s)." | Orange |
| Certificates eligible but not yet issued for > 10 cadets | "[N] cadets are eligible for certificates but certificates have not been issued." | Blue |

---

## 4. KPI Summary Bar

Five KPI cards rendered in a horizontal scrollable bar. All values scoped to the selected academic year.

| Card | Metric | Calculation | HTMX Target | Empty State |
|---|---|---|---|---|
| Total NCC Cadets (Group-Wide) | All cadets enrolled in NCC across all branches this AY | `NCCCadet.objects.filter(ay=current_ay).count()` | `#kpi-total-cadets` | "0" with grey badge |
| Camps This AY | All camp records created for this AY | `NCCCamp.objects.filter(ay=current_ay).count()` | `#kpi-total-camps` | "0" |
| Mandatory Camp Attendance (ATC/CATC) | Cadets with attendance recorded in ≥ 1 ATC or CATC camp | Computed from attendance records filtered by `camp_type__in=['ATC','CATC']` | `#kpi-mandatory-att` | "0 / [N]" |
| Certificates Issued This AY | Sum of certificates issued across all camps this AY | `NCCCertificate.objects.filter(issued_date__gte=ay_start).count()` | `#kpi-certs-issued` | "0" |
| Upcoming Camps (Next 30 Days) | Camps with `start_date` within 30 days from today and status = Upcoming | `NCCCamp.objects.filter(start_date__range=(today, today+30d), status='upcoming').count()` | `#kpi-upcoming` | "0" in green badge |

**HTMX pattern:** Each card uses `hx-get` to its dedicated sub-endpoint with `hx-trigger="load"` and renders a skeleton rectangle while loading. AY selector change triggers refresh of all 5 KPI cards via `hx-swap-oob="true"`.

---

## 5. Sections

### 5.1 Camp Register

Main table of all NCC camps for the selected academic year. Default sort: Start Date ASC (soonest upcoming first). Server-side paginated at 25 rows/page.

**Table Columns:**

| Column | Field | Notes |
|---|---|---|
| Camp Name | `NCCCamp.name` | Sortable; clickable — opens `camp-detail` drawer |
| Camp Type | `NCCCamp.camp_type` | Colour-coded badge (see type list below) |
| NCC Wing | `NCCCamp.wing` | Badge: Army (olive), Naval (navy blue), Air (sky blue), Girls (pink) |
| Start Date | `NCCCamp.start_date` | DD MMM YYYY; sortable |
| End Date | `NCCCamp.end_date` | DD MMM YYYY |
| Location / Venue | `NCCCamp.venue` | Text; truncated at 40 chars; full value in tooltip |
| Organizing Unit | `NCCCamp.organizing_directorate` | Text; "—" if not filled |
| Cadets Nominated | Sum of nominations from all branches for this camp | Integer; badge |
| Attendance | `[actual_present] / [nominated]` | e.g. "45 / 50"; colour: green if ≥ 90%, yellow 70–89%, red < 70%; "—" if not recorded |
| Certificate Status | `NCCCamp.certificate_status` | Badge: Pending (grey) / Issued (green) / Partial (yellow) |
| Actions | Inline | "View" / "Edit" / "Record Attendance" / "Issue Certificates" |

**Camp Type Badge Colours:**

| Camp Type | Badge Colour |
|---|---|
| Annual Training Camp (ATC) | Dark green |
| Combined Annual Training Camp (CATC) | Dark blue |
| Basic Leadership Camp (BLC) | Teal |
| Advance Leadership Camp (ALC) | Indigo |
| Republic Day Camp (RDC) | Saffron |
| Independence Day Camp (IDC) | Saffron |
| National Integration Camp (NIC) | Purple |
| Thal Sainik Camp | Olive |
| Vayu Sainik Camp | Sky blue |
| Naval Sainik Camp | Navy |
| Special NCC Camp | Orange |
| Attachment Camp | Grey |
| Social Service Camp | Cyan |

**Inline Actions:**
- `View` — opens `camp-detail` drawer, Overview tab.
- `Edit` — opens `ncc-camp-create` drawer pre-populated with existing data.
- `Record Attendance` — opens `attendance-mark` modal. Visible only when camp Start Date has passed.
- `Issue Certificates` — opens `camp-detail` drawer on Certificates tab. Visible only when camp status = Completed.

**Filter Drawer (hx-get `/api/ncc/camps/` with params):**

| Filter | Type | Options |
|---|---|---|
| Camp Type | Multi-select checkbox | All 13 camp types |
| NCC Wing | Multi-select checkbox | Army / Naval / Air / Girls |
| Status | Radio | All / Upcoming / Ongoing / Completed |
| Academic Year | Select | Current AY + 2 prior |

Active filters rendered as dismissible chips below the filter bar. "Clear All" resets table.

**Search:** Free-text on Camp name, Location/Venue, Camp Type. `hx-trigger="keyup changed delay:400ms"`.

**Pagination:** `hx-get` with `page` param; `hx-target="#camp-register-table-body"`.

---

### 5.2 Cadet Registry (Per Branch)

Summary table showing NCC cadet counts and officer information per branch. Not paginated (branch-level, ≤ 50 rows). Default sort: Branch name ASC.

**Table Columns:**

| Column | Field | Notes |
|---|---|---|
| Branch | `branch.name` | Sortable |
| Wing | Primary NCC wing active at branch | Badge (Army/Naval/Air/Girls); "Multiple" badge if more than one wing active |
| Total Cadets | `NCCCadet.objects.filter(branch=b, ay=ay).count()` | Integer; sortable |
| Senior Division | Count with `division = SD` | Integer |
| Junior Division | Count with `division = JD` | Integer |
| Girls Division | Count with `division = GD` | Integer |
| NCC Officer Name | `NCCUnit.officer_name` | Text; "—" if not registered |
| Officer Contact | `NCCUnit.officer_contact` | Masked: shows last 4 digits (e.g. ××××-5678) |
| Last Camp Date | Most recent camp end date with cadets from this branch | Date; "Never" (red) if no camps |
| Actions | Inline | "View Cadets" — opens `camp-detail` drawer scoped to that branch's cadet list |

---

## 6. Drawers & Modals

### 6.1 Drawer: `ncc-camp-create` (560px, slides from right)

**Trigger:** `[+ Add Camp]` button or "Edit" inline action. Coordinator only.

**4 Tabs:**

#### Tab 1 — Camp

| Field | Type | Validation | Notes |
|---|---|---|---|
| Camp Name | Text input | Required; min 3, max 150 chars | Placeholder: "e.g. Annual Training Camp — Army Wing Mar 2026" |
| Camp Type | Select | Required | 13 types from list above |
| NCC Wing | Select | Required | Army / Naval / Air / Girls |
| Start Date | Date picker | Required | |
| End Date | Date picker | Required; ≥ Start Date | Auto-calculates duration in days; shown as helper text below the field |
| Location / Venue | Text input | Required; max 200 chars | |
| Organizing Directorate | Text input | Optional; max 200 chars | e.g. "12 NCC Bn, Pune Directorate" |
| Registration Deadline | Date picker | Optional; must be ≤ Start Date | |

#### Tab 2 — Cadets

Repeatable section — one entry per branch delegation. Minimum 1 entry required.

| Field | Type | Validation | Notes |
|---|---|---|---|
| Branch | Select | Required per entry | Only branches with active NCC units shown |
| Number of Cadets | Number input | Required; min 1; integer | |
| Cadet Names | Textarea | Optional; max 3000 chars | Free text or paste from roster |
| Upload Cadet List | File upload | Optional; PDF/Excel; max 5 MB | Alternative to textarea |
| Max Cadets Allowed | Number input | Optional | Upper limit set by organizing directorate; shows warning if Number of Cadets exceeds this |

`[+ Add Another Branch]` button appends a new row of the above fields.

#### Tab 3 — Officers

Per branch entry added in Tab 2, one officer delegation row is auto-generated. Fields per row:

| Field | Type | Validation | Notes |
|---|---|---|---|
| NCC Officer Name | Text input | Required; max 150 chars | |
| Rank | Text input | Optional; max 50 chars | e.g. "Lt", "Capt" |
| Contact Number | Text input | Required; 10-digit mobile | |
| ANO / SO Name | Text input | Optional; max 150 chars | Associate NCC Officer / Staff Officer |
| Emergency Contact | Text input | Required; 10-digit mobile; must differ from Contact Number | |

#### Tab 4 — Logistics

| Field | Type | Validation | Notes |
|---|---|---|---|
| Transport Arranged | Toggle | Default Off | If On: reveals "Transport Details" textarea (optional, max 300 chars) |
| Kit Requirement | Multi-checkbox | Optional | Options: Uniform / Sleeping Bag / Identity Card / Medical Certificate |
| Medical Certificate Required | Toggle | Default Off | If On: flagged as mandatory requirement in cadet nomination list |
| Payment / Fee | Currency input (INR) | Optional; min 0 | Fee per cadet if applicable |
| Notes | Textarea | Optional; max 500 chars | General coordinator notes |

**Footer Buttons:** `[Save Camp]`; `[Save & Send Nominations]` (sends SMS/email notification to branch NCC officers listing nominated cadets); `[Cancel]`.

---

### 6.2 Drawer: `camp-detail` (560px, slides from right)

**Trigger:** "View" inline action in Section 5.1 or camp name click.

**Header:** Camp Name, Wing badge, Type badge, Status badge (Upcoming / Ongoing / Completed / Cancelled).

**4 Tabs:**

#### Tab 1 — Overview

All camp metadata displayed in a two-column read-only layout:
- Camp Name, Type, Wing, Status
- Start Date, End Date, Duration (auto-calculated days)
- Location / Venue, Organizing Directorate
- Registration Deadline
- Total Nominated Cadets (group-wide), Branches Participating
- Logistics: Transport, Kit Requirements, Medical Cert Required, Fee per Cadet

**Buttons (Coordinator only):** `[Edit Camp]` — reopens `ncc-camp-create` drawer in edit mode. `[Cancel Camp]` — changes status to Cancelled after confirmation modal: "Are you sure you want to cancel this camp? All branch officers will be notified. This action cannot be undone." Confirmation requires typing the camp name.

#### Tab 2 — Cadets

Nominated cadets grouped by branch. Expandable branch accordion rows — each row header shows "Branch Name — [N] Cadets" and expands to show the cadets table:

| Column | Notes |
|---|---|
| Name | Cadet full name |
| Branch | Branch name |
| Class / Year | e.g. "Class XI" or "B.Sc. II Year" |
| Wing | Army SD / Army JD / Naval / Air / Girls |
| Nomination Status | Badge: Confirmed (green) / Pending (yellow) / Withdrawn (red) |

Pagination within each branch accordion if > 25 cadets in that branch.

`[Withdraw Cadet]` action per row (Coordinator only); triggers `hx-post` to withdraw endpoint, replaces row badge with "Withdrawn" via `hx-swap="outerHTML"`.

#### Tab 3 — Attendance

Visible only when camp Start Date has passed.

If camp is multi-day: a Date selector at the top allows switching between per-day attendance records. If single-day: attendance is marked once.

**Attendance Table:**

| Column | Notes |
|---|---|
| Cadet Name | |
| Branch | |
| Present | Checkbox; checked = present for selected day |
| Days Attended | For multi-day: auto-updated count of days marked present |
| Overall Attendance % | `(days_attended / total_camp_days) * 100`; green ≥ 75%, yellow 50–74%, red < 50% |

`[Save Attendance]` button — `hx-post` to `/api/ncc/camps/{id}/attendance/` with date and presence data.
`[Export Attendance Sheet]` — XLSX download of the full attendance grid.

Auto-calculated summary at the bottom: "Present: [N] / Nominated: [N] — Overall Attendance: [N]%".

#### Tab 4 — Certificates

Visible only when camp status = Completed.

**Eligible Cadets Table** (attendance ≥ configured threshold, default 75%):

| Column | Notes |
|---|---|
| Cadet Name | |
| Branch | |
| Attendance % | Colour-coded as in Tab 3 |
| Certificate Type | Select per row: Participation / Excellence / Best Cadet |
| Certificate Status | Badge: Not Issued (grey) / Issued (green) |
| Download | "Download PDF" link — visible only when Issued |

**Bulk Actions:**
- `[Generate Certificates]` — triggers PDF certificate generation for all eligible cadets with status "Not Issued". `hx-post` to `/api/ncc/camps/{id}/certificates/generate/`. Shows inline progress indicator: "Generating [N] certificates…" with spinner. On complete, table refreshes via `hx-swap-oob`.
- `[Download All (ZIP)]` — downloads all issued certificates as a ZIP archive.

---

### 6.3 Modal: `attendance-mark` (560px, centred)

**Trigger:** "Record Attendance" inline action in Section 5.1, or `[Mark Attendance]` within `camp-detail` Tab 3.

| Field | Type | Notes |
|---|---|---|
| Camp Name | Display (read-only, pre-filled) | |
| Date | Date picker | Required; defaults to today; bounded within camp Start–End date range |
| Cadet List with Checkboxes | Checkbox table | Name, Branch, checkbox for Present / Absent |
| Mark All Present | Bulk toggle at top of checkbox column | Selects all checkboxes client-side (no HTMX) |

`[Save Attendance]` — `hx-post` to `/api/ncc/camps/{id}/attendance/`. Closes modal on success; success toast shown.
`[Cancel]` — discards without saving.

---

## 7. Charts

### 7.1 Camp Attendance by Wing (Grouped Bar Chart)

- **Type:** Grouped vertical bar chart
- **X-axis:** NCC Wings (Army / Naval / Air / Girls)
- **Y-axis:** Cadet count
- **Series per group:** Nominated (blue bar) vs Attended (green bar) — one pair per wing
- **Data endpoint:** `GET /api/ncc/charts/attendance-by-wing/?ay={ay}`
- **HTMX:** `hx-get` on page load; `hx-trigger="load"`. Rendered into `#chart-wing-attendance`.
- **Tooltip:** "Wing: [X] — Nominated: [N], Attended: [N], Rate: [N]%"
- **Empty state:** "No camp attendance data available for this academic year."

### 7.2 Camp Type Distribution This AY (Horizontal Bar Chart)

- **Type:** Horizontal bar chart
- **Y-axis:** Camp types (ordered by frequency DESC)
- **X-axis:** Number of camps
- **Bar colour:** Single colour (indigo) — consistent across all bars
- **Data endpoint:** `GET /api/ncc/charts/camp-type-distribution/?ay={ay}`
- **HTMX:** `hx-get` on page load; `hx-trigger="load"`. Rendered into `#chart-camp-types`.
- **Tooltip:** "[Camp Type]: [N] camps, [N] total cadets nominated"
- **Empty state:** "No camps recorded for this academic year."

---

## 8. Toast Messages

| Trigger | Toast Text | Type |
|---|---|---|
| Camp created | "Camp '[Name]' has been added to the register." | Success |
| Camp updated | "Camp '[Name]' has been updated." | Success |
| Camp cancelled | "Camp '[Name]' has been cancelled." | Warning |
| Attendance saved | "Attendance recorded for [N] cadets on [Date]." | Success |
| Certificates generated | "[N] certificates generated for '[Camp Name]'." | Success |
| Certificate generation partially failed | "[N] certificates generated. [N] failed — please retry." | Warning |
| Cadet nomination saved | "[N] cadet(s) nominated from [Branch] for '[Camp Name]'." | Success |
| Cadet withdrawn | "Cadet '[Name]' has been withdrawn from '[Camp Name]'." | Info |
| File upload exceeds 5 MB | "File too large. Maximum allowed size is 5 MB." | Error |
| Invalid file type | "Invalid file type. Please upload PDF or Excel only." | Error |
| Required field missing on save | "Please complete all required fields before saving." | Error |
| Registration deadline passed | "The registration deadline for this camp has passed." | Warning |
| Export triggered | "Preparing export… You will be notified when ready." | Info |
| API error | "Something went wrong. Please try again or contact support." | Error |

---

## 9. Empty States

| Section / Component | Condition | Icon | Heading | Body Text | CTA |
|---|---|---|---|---|---|
| Section 5.1 — Camp Register | No camps for this AY | calendar | "No Camps Registered" | "No NCC camps have been registered for this academic year." | [+ Add Camp] |
| Section 5.1 — filtered result empty | Filters return no rows | filter | "No Matching Camps" | "Adjust your filters or search term to find camps." | [Clear Filters] |
| Section 5.2 — Cadet Registry | No branches have NCC units | users | "No NCC Units Registered" | "No branches have NCC units registered for this academic year." | [+ Register Cadets] |
| `camp-detail` — Cadets tab | No cadets nominated | user-plus | "No Cadets Nominated" | "No cadets have been nominated for this camp from any branch." | [Edit Camp] |
| `camp-detail` — Attendance tab | Camp start date not yet reached | clock | "Camp Not Started" | "Attendance can only be recorded after the camp start date." | — |
| `camp-detail` — Attendance tab | Camp started, no attendance recorded | clipboard | "No Attendance Recorded" | "Record attendance to enable certificate issuance." | [Mark Attendance] |
| `camp-detail` — Certificates tab | Camp not completed | lock | "Camp Not Completed" | "Certificates can only be issued after the camp is marked as completed." | — |
| `camp-detail` — Certificates tab | No cadets meet attendance threshold | x-circle | "No Eligible Cadets" | "No cadets meet the minimum attendance threshold for certificate issuance." | — |
| Chart 7.1 | No attendance data | bar-chart-2 | "No Attendance Data" | "Record camp attendance to view wing-level participation." | — |
| Chart 7.2 | No camps this AY | bar-chart | "No Camp Data" | "No camps have been registered for this academic year." | — |

---

## 10. Loader States

| Component | Loader Type | Duration Trigger |
|---|---|---|
| KPI cards (all 5) | Skeleton rectangle (48px tall, full card width, animated pulse) | Until `hx-get` response received |
| Section 5.1 table body | Skeleton rows (5 rows × all column widths, animated pulse) | Until table data fetched |
| Section 5.2 table body | Skeleton rows (5 rows) | Until data fetched |
| `ncc-camp-create` drawer — Tab 2 branch options | Spinner in branch dropdown | While branch list fetches on drawer open |
| `camp-detail` drawer body | Skeleton rows (5 rows) | Until overview data fetched |
| `camp-detail` — Cadets tab | Skeleton rows (5 rows) | Until cadet list fetched on tab click |
| `camp-detail` — Attendance tab | Skeleton rows (5 rows) | Until attendance data fetched on tab click |
| `camp-detail` — Certificates tab | Skeleton rows (5 rows) | Until eligibility data fetched on tab click |
| Certificate generation | Inline spinner + "Generating [N] certificates…" text | During POST to generate endpoint |
| Chart 7.1 | Skeleton rectangle (200px tall, full width) | Until Chart.js render |
| Chart 7.2 | Skeleton rectangle (180px tall, full width) | Until Chart.js render |
| File upload in drawer | Inline progress bar below upload field | During upload |

---

## 11. Role-Based UI Visibility

| UI Element | NSS/NCC Coordinator (100) | Sports Director (97) | Cultural Head (99) | Library Head (101) |
|---|---|---|---|---|
| Page access | Yes — full | No — redirect | No — redirect | No — redirect |
| `[+ Add Camp]` button | Visible + active | — | — | — |
| `[+ Register Cadets]` button | Visible + active | — | — | — |
| `[Export ↓]` button | Visible + active | — | — | — |
| Section 5.1 — "Edit" inline action | Visible | — | — | — |
| Section 5.1 — "Record Attendance" action | Visible (post-start-date only) | — | — | — |
| Section 5.1 — "Issue Certificates" action | Visible (post-completion only) | — | — | — |
| `camp-detail` — `[Edit Camp]` button | Visible | — | — | — |
| `camp-detail` — `[Cancel Camp]` button | Visible | — | — | — |
| `camp-detail` — `[Withdraw Cadet]` action | Visible | — | — | — |
| `camp-detail` — `[Generate Certificates]` button | Visible | — | — | — |
| `camp-detail` — `[Download All ZIP]` button | Visible | — | — | — |
| Alert banners | All visible | — | — | — |
| KPI cards | All 5 visible | — | — | — |

---

## 12. API Endpoints

All endpoints under `/api/ncc/`. Authentication: session cookie + CSRF token. All endpoints restricted to Role 100.

| Method | Endpoint | Description | Response |
|---|---|---|---|
| GET | `/api/ncc/camps/?ay={ay}&type={types}&wing={wings}&status={s}&search={q}&page={n}` | Paginated camp register for Section 5.1 | `{results: [...], count, next, previous}` |
| POST | `/api/ncc/camps/create/` | Register a new camp | Created camp object |
| GET | `/api/ncc/camps/{id}/` | Single camp detail | Camp object with related nominations |
| PATCH | `/api/ncc/camps/{id}/update/` | Update camp metadata | Updated camp object |
| POST | `/api/ncc/camps/{id}/cancel/` | Cancel a camp (requires confirmation payload) | `{status: "cancelled"}` |
| GET | `/api/ncc/camps/{id}/cadets/` | Nominated cadets for a camp, paginated per branch | `[{branch, cadets: [...]}]` |
| POST | `/api/ncc/camps/{id}/cadets/nominate/` | Add cadet nominations from a branch | Created nomination records |
| POST | `/api/ncc/camps/{id}/cadets/{cadet_id}/withdraw/` | Withdraw a cadet nomination | `{status: "withdrawn"}` |
| GET | `/api/ncc/camps/{id}/attendance/?date={d}` | Attendance records for a camp, optionally per day | `[{cadet_id, name, present, days_attended, pct}]` |
| POST | `/api/ncc/camps/{id}/attendance/` | Save attendance for a given date | `{saved: N, date}` |
| GET | `/api/ncc/camps/{id}/certificates/eligible/` | List cadets eligible for certificates | `[{cadet_id, name, branch, attendance_pct, cert_type, cert_status}]` |
| POST | `/api/ncc/camps/{id}/certificates/generate/` | Generate certificates for all eligible cadets | `{generated: N, failed: N}` |
| GET | `/api/ncc/camps/{id}/certificates/download-zip/` | Download all issued certificates as ZIP | Binary ZIP download |
| GET | `/api/ncc/cadets/?branch={id}&ay={ay}` | Cadet registry data for Section 5.2 | `[{branch, wing, total, sd, jd, gd, officer_name, officer_contact, last_camp_date}]` |
| GET | `/api/ncc/kpi/?ay={ay}` | All 5 KPI card values | `{total_cadets, total_camps, mandatory_att, certs_issued, upcoming}` |
| GET | `/api/ncc/charts/attendance-by-wing/?ay={ay}` | Data for Chart 7.1 | `[{wing, nominated, attended}]` |
| GET | `/api/ncc/charts/camp-type-distribution/?ay={ay}` | Data for Chart 7.2 | `[{camp_type, count, total_cadets}]` |
| GET | `/api/ncc/export/?ay={ay}&format={xlsx\|pdf}&camp={ids}` | Export camp register | Binary file download |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | `hx-get` / `hx-post` | `hx-target` | `hx-swap` | Notes |
|---|---|---|---|---|---|
| KPI card load | Each card container | `GET /api/ncc/kpi/?ay={ay}` | `#kpi-{card-id}` | `innerHTML` | `hx-trigger="load"` |
| AY selector change | `<select name="ay">` | `GET /api/ncc/kpi/?ay={ay}` | Multiple via `hx-swap-oob="true"` | `outerHTML` | Refreshes KPI bar + all tables |
| Camp register table load | `#camp-register-table-body` | `GET /api/ncc/camps/` | `#camp-register-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search input | `<input name="search">` | `GET /api/ncc/camps/?search={q}` | `#camp-register-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:400ms"` |
| Filter drawer apply | `[Apply Filters]` button | `GET /api/ncc/camps/?{params}` | `#camp-register-table-body` | `innerHTML` | Drawer closes after response |
| Pagination | Page number links | `GET /api/ncc/camps/?page={n}` | `#camp-register-table-body` | `innerHTML` | |
| Cadet registry load | `#cadet-registry-body` | `GET /api/ncc/cadets/` | `#cadet-registry-body` | `innerHTML` | `hx-trigger="load"` |
| Drawer open — camp detail | "View" / camp name link | `GET /api/ncc/camps/{id}/` | `#drawer-camp-body` | `innerHTML` | Drawer slides open |
| Drawer tab — Cadets | Tab 2 click in `camp-detail` | `GET /api/ncc/camps/{id}/cadets/` | `#drawer-tab-cadets-body` | `innerHTML` | `hx-trigger="click"` on tab |
| Drawer tab — Attendance | Tab 3 click | `GET /api/ncc/camps/{id}/attendance/` | `#drawer-tab-attendance-body` | `innerHTML` | `hx-trigger="click"` |
| Attendance date change | Date picker in attendance tab | `GET /api/ncc/camps/{id}/attendance/?date={d}` | `#attendance-table-body` | `innerHTML` | `hx-trigger="change"` |
| Save attendance | `[Save Attendance]` button | `POST /api/ncc/camps/{id}/attendance/` | `#attendance-save-status` | `innerHTML` | Row statuses updated via `hx-swap-oob` |
| Mark all present toggle | "Mark All Present" checkbox | JavaScript sets all checkboxes | — | — | Client-side only; no HTMX until Save |
| Drawer tab — Certificates | Tab 4 click | `GET /api/ncc/camps/{id}/certificates/eligible/` | `#drawer-tab-certs-body` | `innerHTML` | `hx-trigger="click"` |
| Generate certificates | `[Generate Certificates]` button | `POST /api/ncc/camps/{id}/certificates/generate/` | `#certs-table-body` | `innerHTML` | Shows spinner; full table refreshes on complete |
| Cadet withdraw | `[Withdraw Cadet]` per row | `POST /api/ncc/camps/{id}/cadets/{cadet_id}/withdraw/` | `#cadet-row-{id}` | `outerHTML` | Replaces row with "Withdrawn" status badge |
| Chart 7.1 load | `#chart-wing-attendance` | `GET /api/ncc/charts/attendance-by-wing/` | `#chart-wing-attendance` | `innerHTML` | Response contains `<canvas>` + Chart.js init script |
| Chart 7.2 load | `#chart-camp-types` | `GET /api/ncc/charts/camp-type-distribution/` | `#chart-camp-types` | `innerHTML` | Response contains `<canvas>` + Chart.js init script |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
