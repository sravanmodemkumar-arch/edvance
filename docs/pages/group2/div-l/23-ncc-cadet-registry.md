# 23 — NCC Cadet Registry

> **URL:** `/group/nss/ncc-cadets/`
> **File:** `23-ncc-cadet-registry.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Group NSS/NCC Coordinator G3 (Role 100, full — sole owner)

---

## 1. Purpose

Master registry of all NCC cadets across every branch in the group. The NCC (National Cadet Corps) programme is structured around a three-tier certificate progression — A Certificate (Class 9–10), B Certificate (Class 11), C Certificate (Class 12) — each requiring specific mandatory camps: Annual Training Camp (ATC), Combined Annual Training Camp (CATC), and advanced/national camps respectively. Each cadet has an NCC Enrollment Number issued by the NCC Directorate, belongs to a specific Wing, and serves under an Associate NCC Officer (ANO) at their branch.

This page provides the individual cadet-level view that is absent from Page 15 (NCC Camp Register), which only surfaces branch-level aggregate counts. The NSS/NCC Coordinator uses this registry for four primary purposes:

1. **Nomination for prestigious national camps.** Republic Day Camp (RDC) and Independence Day Camp (IDC) nominations require individual cadet profiles, certificate grades, disciplinary records, camp attendance percentages, and performance history. The shortlist view in Section 5.2 surfaces the top candidates.

2. **Certificate level progression tracking.** Each cadet's progress through the A → B → C certificate chain is tracked with mandatory requirement checklists (ATC/CATC/advanced camps, written exams). Cadets at risk of non-completion are flagged.

3. **NCC Directorate annual returns.** The Coordinator generates annual return documents required by the NCC Directorate listing all cadets, their enrollment numbers, certificate levels, and camp completion status.

4. **Cross-branch visibility.** The group Coordinator oversees units at up to 50 branches simultaneously. This consolidated registry eliminates the need to access each branch separately for compliance activities.

**NCC Certificate Levels:**
- A Certificate — Class 9–10; requires ATC attendance
- B Certificate — Class 11; requires CATC + ATC attendance
- C Certificate — Class 12; requires advanced camp + CATC + ATC attendance + written exam

**NCC Wings (7 categories):**
- Army Senior Division (SD) · Army Junior Division (JD) · Naval Wing (NW) · Air Wing (AW) · Girls Division — Army (G-Army) · Girls Division — Naval (G-Naval) · Girls Division — Air (G-Air)

Scale: 500–3,000 NCC cadets per large group. Cadets typically serve 2–3 years; records are AY-scoped but cadet profiles span multiple years.

> **See also:** Page 15 — NCC Camp Register (branch-level camp summaries; this page provides the individual cadet detail that Section 5.2 of Page 15 references but does not contain) · Page 04 — NSS/NCC Coordinator Dashboard (group-level NCC KPIs) · Page 22 — NSS Certificate Management (parallel year-end workflow for NSS volunteers)

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group NSS/NCC Coordinator | G3, Role 100 | Full — create, edit, deregister cadets, manage nominations, view all records, export annual returns | Sole owner; all read and write access belongs exclusively to this role |
| Group Cultural Activities Head | G3, Role 99 | No access | 403 on direct URL |
| Group Sports Director | G3, Role 97 | No access | 403 on direct URL |
| Group Sports Coordinator | G3, Role 98 | No access | 403 on direct URL |
| Group Library Head | G2, Role 101 | No access | 403 on direct URL |

> **Access enforcement:** `@require_role(['nss_ncc_coordinator'])` on all endpoints for this page (both read and write). No other role, including group admin, has access to individual cadet records through this interface. Django raises HTTP 403 with a custom error template for any other role hitting these URLs.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  NCC  ›  NCC Cadet Registry
```

### 3.2 Page Header
```
NCC Cadet Registry                          [+ Register Cadet]  [Nominate for Camp ▾]  [Export ↓]
Group NSS/NCC Coordinator — [Coordinator Name]
AY [academic year]  ·  [N] Active Cadets  ·  [N] Branches with NCC Units  ·  [N] Wings
```

`[+ Register Cadet]` — opens `cadet-create` drawer.
`[Nominate for Camp ▾]` — dropdown: "Create New Nomination" (opens `nomination-create` drawer) · "View All Nominations" (navigates to a nominations sub-view within the page, scrolling to a nominations panel below the charts).
`[Export ↓]` — dropdown: "Annual Returns (XLSX)" · "Cadet List (PDF)" · "Nomination Summary (PDF)".

**AY selector:** Dropdown top-right. Controls data in Sections 5.1 and 5.2. Section 5.3 (Wing-wise Summary) and Charts recalculate for the selected AY on change.

### 3.3 Alert Banners

Stacked above the KPI bar. Individually dismissible per session.

| Condition | Banner Text | Severity |
|---|---|---|
| Cadets at risk of non-completion (mandatory camp not attended, AY ending in ≤ 60 days) | "[N] cadet(s) have not attended their mandatory camp and the academic year ends in [N] days. Intervene to prevent non-completion." | Red |
| RDC/IDC nomination deadline approaching (≤ 14 days) | "RDC/IDC nomination deadline is in [N] days. [N] candidates are shortlisted but not yet nominated." | Amber |
| Cadets with deregistered status still in class-linked sessions | "[N] deregistered cadet(s) still appear in branch NCC rosters. Sync with branch ANOs to update unit records." | Amber |
| No cadets registered this AY | "No NCC cadets are registered for AY [year]. Register the first cadet to begin tracking." | Blue |

---

## 4. KPI Summary Bar

Five metric cards displayed horizontally. AY-scoped except Branches with NCC Units.

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total NCC Cadets (Group-wide) | Count of active cadets for selected AY | Indigo neutral | Clears all filters; reloads full table |
| C Certificate Eligible Cadets | Count of cadets in Class 12 with CATC + ATC attended (regardless of whether exam passed yet) | Green if > 0; Amber if 0 | Filters Section 5.1 to `cert_level_target = C` + `mandatory_camp = true` |
| Cadets Nominated for RDC/IDC (This AY) | Count with `rdc_idc_nominated = true` in selected AY | Indigo neutral | Scrolls to Section 5.2 |
| Branches with NCC Unit | Count of distinct branches with at least one active cadet record (not AY-scoped; reflects program presence) | Indigo neutral | No drill-down |
| Cadets at Risk | Count with mandatory camp not attended AND academic year end within 90 days | Red if > 0; Green if 0 | Filters Section 5.1 to `mandatory_camp = false AND status = Active` |

```
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  Total Cadets    │ │  C Cert Eligible │ │  RDC/IDC Nom.    │ │  Branches w/ NCC │ │  At Risk         │
│     1,847        │ │      312         │ │       24         │ │        38        │ │        67        │
│   ● Indigo       │ │   ● Green        │ │   ● Indigo       │ │   ● Indigo       │ │   ● Red          │
└──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘
```

> KPI bar loaded via HTMX `hx-trigger="load"` from `/api/v1/ncc/cadets/kpi-summary/?ay={ay}`. Refreshes after any cadet create, edit, deregister, or nomination action via `hx-trigger="load, cadetAction from:body"`.

---

## 5. Sections

### 5.1 Cadet Registry

**Search bar:**
```
[🔍 Search cadet name, NCC ID, or branch…]  [Branch ▾]  [Wing ▾]  [Cert Level Target ▾]  [Mandatory Camp ▾]  [RDC/IDC Nominated ▾]  [Status ▾]  [Class ▾]  [🔽 More Filters]  [Reset]
```

Active filter chips below the bar; each dismissible with ×.

**Filters:**

| Filter | Options |
|---|---|
| Branch | Multi-select list of all group branches |
| Wing | Multi-select: Army SD / Army JD / Naval / Air / Girls Army / Girls Naval / Girls Air |
| Certificate Level Target | A (Class 9–10) / B (Class 11) / C (Class 12) |
| Mandatory Camp Completed | Yes / No |
| RDC/IDC Nominated | Yes / No |
| Status | Active (default) / Deregistered / All |
| Class | Multi-select: 6 / 7 / 8 / 9 / 10 / 11 / 12 |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| (Checkbox) | Checkbox | — | Select-all; drives bulk Nominate for Camp action |
| Cadet Name | Text (link → `cadet-detail` drawer) | ▲▼ | Full name; link opens detail drawer |
| Branch | Text | ▲▼ | Branch short name |
| Class | Text | ▲▼ | E.g. `10-A`, `11 Science` |
| Wing | Badge | — | Army SD (olive) / Army JD (olive-light) / Naval (blue) / Air (sky) / Girls Army (rose-olive) / Girls Naval (rose-blue) / Girls Air (rose-sky) |
| NCC ID | Text | — | Enrollment number issued by NCC Directorate; "—" if not yet issued |
| Enrollment Year | Year | ▲▼ | Year cadet joined NCC |
| Certificate Level (Target) | Badge | ▲▼ | A Working Towards (amber) / B Working Towards (amber) / C Working Towards (amber) |
| A Certificate | Icon | — | ✅ Earned · ⏳ In Progress · ❌ Not Started |
| B Certificate | Icon | — | ✅ Earned · ⏳ In Progress · ❌ Not Started |
| C Certificate | Icon | — | ✅ Earned · ⏳ In Progress · ❌ Not Started |
| Mandatory Camp (ATC/CATC) | Icon | — | ✅ Completed · ❌ Not Completed; tooltip shows which camp is required for the cadet's current level |
| RDC/IDC Nominated? | Badge | — | Nominated (indigo) / Not Nominated (grey) |
| Status | Badge | — | Active (green) / Deregistered (red) |
| Actions | — | — | [View] · [Edit] · [Nominate for Camp] · [Deregister] |

`[View]` — opens `cadet-detail` drawer.
`[Edit]` — opens `cadet-create` drawer pre-filled for editing.
`[Nominate for Camp]` — opens `nomination-create` drawer pre-populated with this cadet's details; only shown for cadets where C certificate is in progress or earned.
`[Deregister]` — opens inline confirmation micro-modal: "Deregister [Cadet Name]? This will mark the cadet as inactive. All historical records are preserved." `[Confirm Deregister]` (red) · `[Cancel]`.

**Default sort:** Wing ASC (alphabetical by wing name), then Class ASC.
**Pagination:** 25 rows per page. Controls: `« Previous  Page N of N  Next »`. Rows-per-page: 25 / 50 / 100.
**Bulk actions** (shown when ≥ 1 row selected): `[Nominate Selected for Camp (N)]` · `[Export Selected (XLSX)]`.

---

### 5.2 Top Performers — RDC/IDC Nomination Shortlist

Compact section displayed below Section 5.1 (collapsible). Title: "RDC/IDC Nomination Shortlist — Top Performers".

> Cadets appearing here meet the base criteria for Republic Day Camp (RDC) and Independence Day Camp (IDC) nomination consideration: C Certificate in progress or earned + Camp Attendance ≥ 75% + No disciplinary record + At least one special/advanced camp attended. The Coordinator uses this section to make final nomination decisions.

**Eligibility criteria summary bar:**
```
Criteria: C Certificate (Earned or In Progress)  ·  Camp Attendance ≥ 75%  ·  No Disciplinary Record  ·  Special/Advanced Camp Attended
[N] cadets meet all criteria across [N] branches
```

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Cadet Name | Text (link → `cadet-detail` drawer) | ▲▼ | |
| Branch | Text | ▲▼ | |
| Class | Text | ▲▼ | |
| Wing | Badge | — | |
| C Cert Progress | Progress indicator | — | "Earned" / "In Progress — [N]% requirements met" |
| Camp Attendance % | Percentage | ▲▼ | Green if ≥ 75%; amber if 60–74%; red if < 60% |
| Disciplinary Record | Badge | — | Clear (green) / Minor (amber) / Serious (red) |
| Eligibility Score | Number | ▲▼ | System-calculated composite score (0–100) based on attendance %, certificate progress, camps attended, special achievements; higher = stronger candidate |
| Nominated? | Toggle | — | On = Nominated for current AY RDC/IDC; toggling to On triggers notification draft; toggles back to Off cancels nomination after confirmation |
| Actions | — | — | [Nominate] · [View Profile] |

`[Nominate]` — opens `nomination-create` drawer pre-filled with this cadet.
`[View Profile]` — opens `cadet-detail` drawer.
**Nomination toggle:** When toggled to On, a small confirmation popover appears: "Nominate [Cadet Name] for RDC/IDC [AY]? This will notify the branch ANO/POC." `[Confirm]` · `[Cancel]`. On confirm: `rdc_idc_nominated` set to `true`; in-app notification queued to branch ANO.

**Default sort:** Eligibility Score DESC.
**Pagination:** 15 rows per page (compact format).

---

### 5.3 Wing-wise Summary

Compact static summary table. Title: "Wing-wise Cadet Summary — All Branches". Updated for selected AY. Non-paginated (7 rows maximum — one per wing).

| Column | Notes |
|---|---|
| Wing | Wing name with badge colour |
| Total Cadets | Count of active cadets in this wing across all branches |
| A Cert (Earned) | Count of cadets with A Certificate earned |
| B Cert (Earned) | Count of cadets with B Certificate earned |
| C Cert (Earned) | Count of cadets with C Certificate earned |
| Mandatory Camp % | Percentage of cadets who have completed their mandatory camp (ATC/CATC as applicable) |
| RDC/IDC Nominated | Count nominated for RDC/IDC in selected AY |

**Total row** at bottom: sums across all wings.

> Table is read-only. No filters, no pagination, no drill-downs. Intended as a quick at-a-glance view. Clicking a wing name filters Section 5.1 to that wing.

---

## 6. Drawers & Modals

### 6.1 `cadet-create` Drawer — 560 px, right-slide

**Trigger:** `[+ Register Cadet]` header button (create mode) · `[Edit]` action in table row (edit mode).

**Header:** "Register New Cadet" / "Edit Cadet — [Cadet Name]"

**Tabs:** Profile | NCC Details | Records

---

**Tab: Profile**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Full Name | Text | Yes | Min 3, max 100 characters |
| Roll Number | Text | Yes | School/college roll number; unique within branch |
| Branch | Select | Yes | Dropdown of all group branches |
| Class | Select | Yes | Options: 6 / 7 / 8 / 9 / 10 / 11 / 12 |
| Date of Birth | Date picker | Yes | Must be ≤ today; cadet must be ≥ 11 years old |
| Gender | Select | Yes | Male / Female / Other |
| Contact Number | Text | No | 10-digit mobile; validated format |
| Parent / Guardian Contact | Text | Yes | 10-digit mobile; validated format |

---

**Tab: NCC Details**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| NCC ID / Enrollment No | Text | No | Issued by NCC Directorate post-enrollment; may not be available at registration time; alphanumeric |
| Wing | Select | Yes | Army SD / Army JD / Naval / Air / Girls Army / Girls Naval / Girls Air |
| Enrollment Year | Year | Yes | 4-digit year; cannot be future; cannot be more than 10 years prior |
| Certificate Level (Working Towards) | Select | Yes | A Certificate / B Certificate / C Certificate; auto-suggested based on Class field (Class 9–10 → A, Class 11 → B, Class 12 → C) but overridable |
| ANO Name | Text | No | Associate NCC Officer name at branch; free text; max 100 chars |
| Sub-Unit | Text | No | E.g. `1 AP BN NCC`, `32 AP Naval Wing NCC`; max 80 chars |
| Previous NCC Experience | Textarea | No | E.g. if transferred from another school; max 200 characters |

---

**Tab: Records**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| A Certificate Status | Select | Yes | Not Earned / In Progress / Earned |
| A Certificate Date | Date picker | Conditional | Required if status = Earned; cannot be future |
| B Certificate Status | Select | Yes | Not Earned / In Progress / Earned |
| B Certificate Date | Date picker | Conditional | Required if status = Earned |
| C Certificate Status | Select | Yes | Not Earned / In Progress / Earned |
| C Certificate Date | Date picker | Conditional | Required if status = Earned |
| Camp Attendance % | Number | No | 0–100; auto-calculated if camps are linked in `cadet-detail` Camp History; can be manually entered if camp data is not yet in system |
| Disciplinary Record | Select | Yes | Clear / Minor Issue / Serious Issue |
| Notes | Textarea | No | Internal coordinator notes; max 300 characters |

**Footer:** `[Cancel]`  `[Register Cadet]` / `[Save Changes]`

---

### 6.2 `cadet-detail` Drawer — 560 px, right-slide

**Trigger:** Clicking Cadet Name link in Section 5.1 table · `[View]` action · `[View Profile]` action in Section 5.2.

**Header:**
```
[Cadet Name]                                              [Edit] [×]
[Wing badge]  ·  [Branch]  ·  Class [N]  ·  Status: [Active/Deregistered badge]
NCC ID: [ID or "Not Yet Issued"]
```

**Tabs:** Profile | Certificates | Camp History | Nominations

---

**Tab: Profile**

Full read-only view of all Profile and NCC Details fields from `cadet-create`. `[Edit]` button at top-right opens `cadet-create` drawer in edit mode.

---

**Tab: Certificates**

Visual A → B → C progression tracker. Each level displayed as a card:

**Per certificate card layout:**
```
[A Certificate]  —  Status: [badge]
Completion Date: [DD MMM YYYY] / Not Yet Earned
Requirements:
  ✅/❌  Annual Training Camp (ATC) attended
  ✅/❌  Written Examination passed
  ✅/❌  Minimum service days met
```

B Certificate requirements additionally include: CATC attended.
C Certificate requirements additionally include: Advanced Camp attended, National Integration Camp (NIC) or equivalent attended.

Each requirement row is sourced from the cadet's camp history records (where linked) or from the manually entered status in the Records tab of `cadet-create`.

---

**Tab: Camp History**

Table of all camps attended by this cadet.

| Column | Notes |
|---|---|
| Camp Name | Full name of camp |
| Type | ATC / CATC / RDC / IDC / TSC / VSC / NSC / State Camp / NIC / Other |
| Dates | Start and end dates: `DD MMM YYYY – DD MMM YYYY` |
| Wing | Wing the camp was for |
| Attendance (Days) | Number of days attended |
| Certificate / Grade Received | Any certificate or grade awarded at the camp (e.g. "A Grade", "Best Cadet") |
| Notes | Camp-level notes |

`[Add Camp Record]` button at top of tab (Role 100 only). Opens inline form within the tab:
| Field | Type | Required |
|---|---|---|
| Camp Name | Text | Yes |
| Type | Select | Yes |
| Start Date | Date | Yes |
| End Date | Date | Yes |
| Attendance Days | Number | Yes |
| Certificate / Grade | Text | No |
| Notes | Textarea | No |

Sorted by Start Date DESC. Paginated: 10 rows per tab.

---

**Tab: Nominations**

Table of all RDC/IDC and other national/state camp nominations for this cadet.

| Column | Notes |
|---|---|
| Camp Name | Full name |
| Camp Type | RDC / IDC / TSC / VSC / NSC / State Camp / NIC |
| Year | Academic year of nomination |
| Status | Nominated (indigo) / Selected (green) / Not Selected (red) |
| Notes | Outcome notes |

`[Nominate for Camp]` button at top (Role 100 only) — opens `nomination-create` drawer pre-filled for this cadet.

Sorted by Year DESC. Paginated: 10 rows per tab.

---

### 6.3 `nomination-create` Drawer — 480 px, right-slide

**Trigger:** `[Nominate for Camp ▾]` → "Create New Nomination" · `[Nominate for Camp]` action in Section 5.1 · `[Nominate]` in Section 5.2 · `[Nominate for Camp]` button in `cadet-detail` Nominations tab.

**Tabs:** Camp | Cadets

---

**Tab: Camp**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Camp Name | Text | Yes | Full official name of the camp |
| Camp Type | Select | Yes | RDC / IDC / TSC (Thal Sainik Camp) / VSC (Vayu Sainik Camp) / NSC (Nau Sainik Camp) / State Camp / National Integration Camp / Other |
| Start Date | Date picker | Yes | Cannot be in the past |
| End Date | Date picker | Yes | Must be ≥ Start Date |
| Organizing Directorate | Text | No | E.g. "Andhra Pradesh NCC Directorate"; max 100 chars |
| Nomination Deadline | Date picker | Yes | Date by which nominations must be submitted to the Directorate; must be ≤ Start Date |
| Max Cadets from Group | Number | No | If set, system warns if selected cadets count exceeds this; no hard block |

---

**Tab: Cadets**

If triggered from a specific cadet, that cadet is pre-selected and shown at top of the list. Otherwise, starts empty.

**Cadet search (multi-select):** Search field at top — searchable by name, NCC ID, branch. Results show: Cadet Name | Branch | Class | Wing | Eligibility Score | Currently Nominated?.

**Selected cadets list:** Shows selected cadets as a table:
| Cadet Name | Branch | Wing | C Cert Progress | Eligibility Score | Remove |
|---|---|---|---|---|---|
| [name] | [branch] | [badge] | Earned / In Progress | [score] | [×] |

**Quota check:** If `Max Cadets from Group` is set, shows: "Selected: [N] / [max] cadets". Red warning if over quota.

**Footer tab-level:** `[Back]` (returns to Camp tab)

**Footer drawer-level:** `[Cancel]`  `[Confirm Nominations]`

On confirm: All selected cadets' `rdc_idc_nominated` is set to `true`; nomination records created; in-app notifications queued to branch ANOs/POCs for each cadet's branch. Toast shows confirmation count.

---

## 7. Charts

All charts use Chart.js 4.x. Each chart has an `[Export PNG]` button calling `chart.toBase64Image()` and downloading the image.

### 7.1 Cadets by Wing Distribution

| Attribute | Value |
|---|---|
| Type | Donut chart |
| Data | 7 segments — one per wing; value = active cadet count |
| Colours | Army SD: olive-600 · Army JD: olive-400 · Naval: blue-500 · Air: sky-500 · Girls Army: rose-600 · Girls Naval: rose-400 · Girls Air: rose-300 |
| Centre label | Total cadets |
| Tooltip | "[Wing Name]: [N] cadets ([N]%)" |
| Legend | Below chart, 2-column horizontal layout given 7 categories |
| Export | `[Export PNG]` |

### 7.2 Certificate Progression

| Attribute | Value |
|---|---|
| Type | Grouped bar chart |
| Data | 3 groups (A / B / C Certificate); within each group: 3 bars (Earned / In Progress / Not Started); values = cadet counts |
| X-axis | Certificate level groups: A | B | C |
| Y-axis | Cadet count (integer ticks, starts at 0) |
| Bar colours | Earned: green-500 · In Progress: amber-400 · Not Started: grey-300 |
| Tooltip | "[Cert Level] — [Status]: [N] cadets" |
| Legend | Earned · In Progress · Not Started (horizontal, above chart) |
| Export | `[Export PNG]` |

### 7.3 Camp Attendance Rate by Branch

| Attribute | Value |
|---|---|
| Type | Horizontal bar chart |
| Data | One bar per branch; value = percentage of active cadets who have completed their mandatory camp (ATC/CATC as required for their level); top 10 branches by total active cadet count |
| X-axis | Mandatory camp completion percentage (0–100%) |
| Y-axis | Branch names |
| Bar colour | Green if ≥ 80%; amber if 50–79%; red if < 50% |
| Threshold line | Vertical reference line at 80% (target completion) |
| Tooltip | "[Branch Name]: [N]% mandatory camp completion ([N] of [N] cadets)" |
| Export | `[Export PNG]` |

---

## 8. Toast Messages

| Action | Toast Text | Type | Duration |
|---|---|---|---|
| Cadet registered | "Cadet [Name] registered successfully under [Branch] — [Wing]." | Success | 4 s |
| Cadet record updated | "Cadet record for [Name] updated." | Success | 4 s |
| Cadet deregistered | "Cadet [Name] deregistered. Record preserved for historical reference." | Success | 4 s |
| Camp record added | "Camp record added for [Cadet Name]." | Success | 4 s |
| Nomination confirmed (single) | "[Cadet Name] nominated for [Camp Name]. Branch ANO notified." | Success | 4 s |
| Nomination confirmed (bulk) | "[N] cadet(s) nominated for [Camp Name]. Branch ANOs notified." | Success | 4 s |
| Nomination toggle — confirmed | "[Cadet Name] marked as nominated for RDC/IDC [AY]." | Success | 4 s |
| Nomination toggle — cancelled | "Nomination for [Cadet Name] cancelled." | Info | 4 s |
| Annual returns exported | "NCC Annual Returns exported to XLSX for AY [year]." | Success | 4 s |
| Cadet list exported | "NCC Cadet List exported to PDF." | Success | 4 s |
| Duplicate NCC ID | "NCC ID [ID] is already assigned to another cadet. Verify the enrollment number." | Error | Manual dismiss |
| Duplicate roll number in branch | "Roll number [N] is already registered at [Branch]." | Error | Manual dismiss |
| Max quota exceeded on nomination | "Selected [N] cadets exceeds the maximum quota of [max] for [Camp Name]. Reduce selection." | Error | Manual dismiss |
| Date of birth validation | "Cadet must be at least 11 years old to be registered in NCC." | Error | 4 s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No cadets registered for selected AY | "No Cadets Registered" | "No NCC cadets are registered for AY [year]. Register the first cadet to begin tracking." | `[+ Register Cadet]` |
| Filters return no results (Section 5.1) | "No Cadets Match Filters" | "No cadet records match the selected filters. Adjust filters or reset to view all." | `[Reset Filters]` |
| Section 5.2 — no cadets meet shortlist criteria | "No Eligible Nominees" | "No cadets currently meet all RDC/IDC eligibility criteria (C Certificate in progress, attendance ≥ 75%, clear conduct, special camp attended)." | None |
| `cadet-detail` — no camp history | "No Camp Records" | "No camp attendance records have been added for this cadet." | `[Add Camp Record]` |
| `cadet-detail` — no nominations | "No Nomination History" | "This cadet has no recorded nominations for national or state camps." | `[Nominate for Camp]` |
| Section 5.3 — no cadets in a wing | "No Cadets in Wing" | "No cadets are registered for this wing in the selected academic year." | None |
| Charts — no data | "No Data Available" | "Chart data will appear once cadets are registered for AY [year]." | None |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load — KPI bar | 5 shimmer cards, full width |
| Initial page load — Section 5.1 table | 10 shimmer rows with column-proportional shimmer blocks |
| Initial page load — Section 5.2 | 6 shimmer rows (compact format) |
| Initial page load — Section 5.3 | 7 shimmer rows (one per wing placeholder) |
| AY selector change | KPI bar + Sections 5.1, 5.2, 5.3 all replace with shimmer simultaneously; charts refresh |
| Filter / search in Section 5.1 | Table area replaced by 20 px indigo spinner centred in table zone |
| `cadet-create` drawer — edit mode pre-fill | Drawer slides in; all tabs show shimmer while cadet data is fetched |
| `cadet-detail` drawer — open | Drawer slides in with shimmer on all 4 tabs simultaneously; tabs populate as data arrives |
| Camp history tab — load | Tab content shows 5-row shimmer table |
| Nominations tab — load | Tab content shows 5-row shimmer table |
| `[Add Camp Record]` inline form submit | Submit button disabled, "Saving…" + spinner |
| `[Confirm Nominations]` button | Button disabled, "Submitting Nominations…" + spinner |
| Export buttons | Button disabled, "Generating…" + spinner; re-enabled on download completion |
| Charts 7.1 / 7.2 / 7.3 | Each chart canvas shows grey shimmer rectangle until data loads |
| Nomination toggle in Section 5.2 | Toggle shows spinner while API call is in-flight |

---

## 11. Role-Based UI Visibility

Given that this page has a single role (Role 100 — NSS/NCC Coordinator) as its sole user, the visibility table below documents what is shown vs. what is blocked for any other session that somehow reaches this URL (which returns HTTP 403 before rendering).

| UI Element | Role 100 — NSS/NCC Coordinator | Any Other Role |
|---|---|---|
| Entire page | Full access | HTTP 403 — redirect to own dashboard |
| KPI Summary Bar | Full | Blocked |
| AY selector | Visible | Blocked |
| `[+ Register Cadet]` | Visible | Blocked |
| `[Nominate for Camp ▾]` | Visible | Blocked |
| `[Export ↓]` | Visible | Blocked |
| Section 5.1 — Cadet Registry table | Full | Blocked |
| `[Edit]` action (5.1) | Visible | Blocked |
| `[Nominate for Camp]` action (5.1) | Visible | Blocked |
| `[Deregister]` action (5.1) | Visible | Blocked |
| Section 5.2 — Shortlist | Full | Blocked |
| Nomination toggle (5.2) | Visible + interactive | Blocked |
| Section 5.3 — Wing-wise Summary | Full | Blocked |
| `cadet-detail` drawer — all tabs | Full; `[Edit]` visible in drawer header | Blocked |
| `cadet-detail` — `[Add Camp Record]` | Visible | Blocked |
| `cadet-detail` — `[Nominate for Camp]` | Visible | Blocked |
| Charts 7.1 / 7.2 / 7.3 | Full | Blocked |
| Alert banners | Full | Blocked |
| Bulk action bar | Visible when rows selected | Blocked |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/ncc/cadets/` | Role 100 | List cadets; params: `branch`, `wing`, `cert_level`, `mandatory_camp`, `rdc_idc_nominated`, `status`, `class_year`, `search`, `ay`, `page`, `page_size`, `ordering` |
| POST | `/api/v1/ncc/cadets/` | Role 100 | Create cadet record |
| GET | `/api/v1/ncc/cadets/{cadet_id}/` | Role 100 | Retrieve full cadet detail including certificates, camp history, nominations |
| PATCH | `/api/v1/ncc/cadets/{cadet_id}/` | Role 100 | Update cadet record fields |
| POST | `/api/v1/ncc/cadets/{cadet_id}/deregister/` | Role 100 | Deregister cadet; sets `status = Deregistered`; preserves all records |
| POST | `/api/v1/ncc/cadets/{cadet_id}/camps/` | Role 100 | Add a camp history record to a cadet; `multipart/form-data` body |
| GET | `/api/v1/ncc/cadets/{cadet_id}/camps/` | Role 100 | List all camp records for a cadet |
| GET | `/api/v1/ncc/cadets/{cadet_id}/nominations/` | Role 100 | List all nomination records for a cadet |
| PATCH | `/api/v1/ncc/cadets/{cadet_id}/nominate-toggle/` | Role 100 | Toggle `rdc_idc_nominated` for current AY; body: `{ nominated: bool, ay: string }` |
| GET | `/api/v1/ncc/cadets/shortlist/` | Role 100 | Returns candidates meeting RDC/IDC criteria, sorted by eligibility score; query: `ay`, `page` |
| GET | `/api/v1/ncc/cadets/wing-summary/` | Role 100 | Returns Section 5.3 wing-wise summary data; query: `ay` |
| GET | `/api/v1/ncc/cadets/kpi-summary/` | Role 100 | Returns `{ total_cadets, c_cert_eligible, rdc_idc_nominated, branches_with_ncc, at_risk }`; query: `ay` |
| POST | `/api/v1/ncc/nominations/` | Role 100 | Create a new camp nomination record with one or more cadets; body: `{ camp_name, camp_type, start_date, end_date, deadline, directorate, max_cadets, cadet_ids: [uuid, …] }` |
| GET | `/api/v1/ncc/nominations/` | Role 100 | List all nominations; params: `ay`, `camp_type`, `page` |
| GET | `/api/v1/ncc/cadets/export/annual-returns/` | Role 100 | Export XLSX annual returns; query: `ay` |
| GET | `/api/v1/ncc/cadets/export/cadet-list-pdf/` | Role 100 | Export PDF cadet list; query: `ay`, all filter params |
| GET | `/api/v1/ncc/cadets/export/nomination-summary-pdf/` | Role 100 | Export PDF nomination summary; query: `ay` |
| GET | `/api/v1/ncc/cadets/chart/wing-distribution/` | Role 100 | Returns wing cadet counts for Chart 7.1; query: `ay` |
| GET | `/api/v1/ncc/cadets/chart/certificate-progression/` | Role 100 | Returns A/B/C × Earned/In Progress/Not Started counts for Chart 7.2; query: `ay` |
| GET | `/api/v1/ncc/cadets/chart/camp-attendance-by-branch/` | Role 100 | Returns mandatory camp completion % per branch for Chart 7.3; query: `ay` |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar on page load | `load` | GET `/api/v1/ncc/cadets/kpi-summary/?ay={ay}` | `#ncc-kpi-bar` | `innerHTML` |
| KPI bar after cadet action | `cadetAction from:body` | GET `/api/v1/ncc/cadets/kpi-summary/?ay={ay}` | `#ncc-kpi-bar` | `innerHTML` |
| Section 5.1 table on page load | `load` | GET `/api/v1/ncc/cadets/?page=1&ay={ay}` | `#cadet-registry-table` | `innerHTML` |
| AY selector change | `change` | GET `/api/v1/ncc/cadets/?ay={new_ay}&page=1` | `#cadet-registry-table` | `innerHTML` |
| Filter / search change (5.1) | `change, input delay:400ms` | GET `/api/v1/ncc/cadets/` (hx-include all filter inputs) | `#cadet-registry-table` | `innerHTML` |
| `[+ Register Cadet]` | `click` | GET `/htmx/ncc/cadets/create-drawer/` | `#drawer-container` | `innerHTML` |
| `[Edit]` action (5.1) | `click` | GET `/htmx/ncc/cadets/{cadet_id}/edit-drawer/` | `#drawer-container` | `innerHTML` |
| Cadet Name link / `[View]` action | `click` | GET `/htmx/ncc/cadets/{cadet_id}/detail-drawer/` | `#drawer-container` | `innerHTML` |
| `cadet-create` form submit | `submit` | POST/PATCH `/api/v1/ncc/cadets/` (or `/{cadet_id}/`) | `#cadet-registry-table` | `innerHTML` |
| `[Deregister]` confirm | `click` | POST `/api/v1/ncc/cadets/{cadet_id}/deregister/` | `#cadet-row-{cadet_id}` | `outerHTML` |
| Section 5.2 shortlist load | `load` | GET `/api/v1/ncc/cadets/shortlist/?ay={ay}&page=1` | `#ncc-shortlist-table` | `innerHTML` |
| Nomination toggle (5.2) | `change` | PATCH `/api/v1/ncc/cadets/{cadet_id}/nominate-toggle/` | `#shortlist-row-{cadet_id}` | `outerHTML` |
| Section 5.3 wing summary load | `load` | GET `/api/v1/ncc/cadets/wing-summary/?ay={ay}` | `#wing-summary-table` | `innerHTML` |
| `[Nominate for Camp ▾]` → Create | `click` | GET `/htmx/ncc/nominations/create-drawer/` | `#drawer-container` | `innerHTML` |
| `nomination-create` form submit | `submit` | POST `/api/v1/ncc/nominations/` | `#cadet-registry-table` (reload) | `innerHTML` |
| `[Add Camp Record]` form submit | `submit` | POST `/api/v1/ncc/cadets/{cadet_id}/camps/` | `#camp-history-table-{cadet_id}` | `innerHTML` |
| Certificate level field change (auto-suggest) | `change` | GET `/htmx/ncc/cadets/cert-suggestion/?class={class_value}` | `#cert-level-suggestion` | `innerHTML` |
| AY selector change (charts) | `change` | GET `/api/v1/ncc/cadets/chart/wing-distribution/?ay={new_ay}` etc. | `#chart-wing` etc. | `innerHTML` (re-renders chart container) |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
