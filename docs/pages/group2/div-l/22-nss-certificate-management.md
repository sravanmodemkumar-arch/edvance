# 22 — NSS Certificate Management

> **URL:** `/group/nss/certificates/`
> **File:** `22-nss-certificate-management.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Group NSS/NCC Coordinator G3 (Role 100, full CRUD) · Group Cultural Activities Head G3 (Role 99, view — summary counts only)

---

## 1. Purpose

Manages two closely related year-end workflows that are exclusively owned by the Group NSS/NCC Coordinator:

**1. NSS Certificate Generation and Tracking.** The NSS Certificate is the primary credential awarded to volunteers who complete the National Service Scheme programme. It is issued by the state NSS Directorate through the university-affiliated NSS unit. Eligibility requires: (a) minimum 240 verified hours of NSS service in the academic year, (b) completion of at least one Special Camp (mandatory 7-day residential camp), and (c) Good Conduct with no unresolved disciplinary issues. This page identifies all eligible volunteers group-wide, generates individual PDF certificates, tracks generation and dispatch status, and exports the official completion list in the format prescribed by the State NSS Directorate for annual submission.

**2. NSS Programme Officer Registry.** Each NSS unit is supervised by a Programme Officer (PO) — a faculty member appointed and recognised by the affiliated university and state NSS Directorate. Their qualifications, training status, appointment term, and contact details must be maintained for university and directorate compliance. This registry provides the cross-branch view of all Programme Officers and flags approaching term expirations and training non-compliance.

These two workflows are combined on one page because both are intensive March-April year-end processes owned exclusively by the same role (NSS/NCC Coordinator), and they are operationally interdependent — certificate exports require Programme Officer details in the submission cover letter.

Scale: 2,000–8,000 NSS volunteers per large group. Certificate generation is an annual batch operation in March-April. Approximately 60–80% of enrolled volunteers typically achieve the 240-hour threshold.

> **See also:** Page 14 — NSS Programme Tracker (authoritative source for activity logs, 240h tracking, and Special Camp attendance verification; this page reads eligibility data from Page 14's records) · Page 04 — NSS/NCC Coordinator Dashboard (summary KPIs for the full NSS programme) · Page 23 — NCC Cadet Registry (parallel end-of-year workflow for NCC cadets)

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group NSS/NCC Coordinator | G3, Role 100 | Full — view all sections, generate certificates, export directorate formats, manage Programme Officer registry, send reminders | Sole write authority; all generation and export actions restricted to this role |
| Group Cultural Activities Head | G3, Role 99 | View only — KPI summary bar counts and Section 5.3 Programme Officer table (non-contact columns) | Cannot access certificate detail, generate, export, or edit any record; contact numbers and emails hidden |
| Group Sports Director | G3, Role 97 | No access | 403 on direct URL |
| Group Sports Coordinator | G3, Role 98 | No access | 403 on direct URL |
| Group Library Head | G2, Role 101 | No access | 403 on direct URL |

> **Access enforcement:** `@require_role(['nss_ncc_coordinator', 'cultural_head'])` on the page view. `@require_role(['nss_ncc_coordinator'])` on all POST, PATCH, DELETE endpoints and all export endpoints. The certificate PDF generation endpoint additionally checks that the requesting user's group matches the volunteer's group. Cultural Head role returns a restricted template that hides Sections 5.1 and 5.2 entirely and renders Section 5.3 with contact fields masked.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  NSS  ›  NSS Certificate Management
```

### 3.2 Page Header
```
NSS Certificate Management                  [Generate Certificates ▾]  [Export ↓]
Group NSS/NCC Coordinator — [Coordinator Name]
AY [academic year]  ·  [N] Eligible Volunteers  ·  [N] Certificates Generated  ·  [N] Programme Officers
```

`[Generate Certificates ▾]` — dropdown with two options: "Generate for Single Volunteer" (opens `certificate-generate-single` drawer) and "Bulk Generate" (opens `certificate-generate-bulk` drawer). Role 100 only; hidden for Role 99.
`[Export ↓]` — dropdown: "Directorate Format (XLSX)", "Formatted Report (PDF)", "Generate Cover Letter". Role 100 only.

**AY selector:** Dropdown top-right. Changing AY reloads Section 5.1 and 5.2 data via HTMX. Section 5.3 (Programme Officers) is not AY-scoped and does not reload on AY change.

### 3.3 Alert Banners

Stacked above the KPI bar. Each is individually dismissible for the session.

| Condition | Banner Text | Severity |
|---|---|---|
| Certificates not yet generated and AY is in March–April window | "[N] eligible volunteers have not yet had certificates generated. Year-end generation window is open." | Amber |
| Programme Officers with expired terms | "[N] Programme Officer term(s) have expired. Update appointments to maintain NSS unit recognition." | Red |
| Programme Officers with overdue training | "[N] Programme Officer(s) have overdue NSS orientation training. Compliance required before next AY." | Amber |
| All eligible certificates generated | "All [N] eligible volunteer certificates have been generated for AY [year]." | Green |
| Directorate submission export not completed this AY | "State Directorate submission export has not been generated for AY [year]. Generate before the submission deadline." | Amber |

---

## 4. KPI Summary Bar

Five metric cards displayed horizontally. AY-scoped except Programme Officers card.

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total 240h Achievers (This AY) | Count of volunteers with `total_hours >= 240` in selected AY | Indigo neutral | Filters Section 5.1 to `hours >= 240` |
| Certificate Eligible | Count with `hours >= 240` AND `special_camp = true` AND `conduct = Good` | Green if > 0; Amber if 0 | Filters Section 5.1 to `eligible = Yes` |
| Certificates Generated | Count with `certificate_status in (Generated, Downloaded, Dispatched)` | Green if = Certificate Eligible; Amber otherwise | Filters to `certificate_status != Not Generated` |
| Certificates Pending Generation | Count eligible but `certificate_status = Not Generated` | Red if > 0; Green if 0 | Filters to `eligible = Yes AND certificate_status = Not Generated` |
| Programme Officers (All Branches) | Count of all active Programme Officers across all branches | Indigo neutral; Red if any have expired terms | Scrolls page to Section 5.3 |

```
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  240h Achievers  │ │  Cert Eligible   │ │  Generated       │ │  Pending Gen.    │ │  Programme Offs. │
│      3,847       │ │     2,991        │ │     2,640        │ │       351        │ │        42        │
│   ● Indigo       │ │   ● Green        │ │   ● Amber        │ │   ● Red          │ │   ● Indigo       │
└──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘
```

> KPI bar loaded via HTMX `hx-trigger="load"` from `/api/v1/nss/certificates/kpi-summary/?ay={ay}`. Refreshes after any certificate generate or status change via `hx-trigger="load, certAction from:body"`.

---

## 5. Sections

### 5.1 Certificate Tracker — Eligible Volunteers

**Search bar:**
```
[🔍 Search volunteer name, enrolment no., or branch…]  [Branch ▾]  [Eligible ▾]  [Certificate Status ▾]  [Special Camp ▾]  [Hours Range ▾]  [Reset]
```

Active filter chips displayed below bar with × per chip.

**Filters:**

| Filter | Options |
|---|---|
| Branch | Multi-select list of all group branches |
| Eligible | All / Yes / No / Pending |
| Certificate Status | Multi-select: Not Generated / Generated / Downloaded / Dispatched |
| Special Camp | Yes / No |
| Hours Range | Custom min–max numeric inputs (applied to `total_hours`) |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| (Checkbox) | Checkbox | — | Select-all in header; drives bulk generate action |
| Volunteer Name | Text | ▲▼ | Full name |
| Branch | Text | ▲▼ | Branch short name |
| NSS Unit Code | Text | ▲▼ | E.g. `AP/KR-037` |
| Enrolment No (NSS) | Text | — | NSS Directorate-issued enrolment number |
| Class | Text | ▲▼ | E.g. `B.Sc. II`, `B.Com. I` |
| Hours Completed | Number | ▲▼ | Colour: green if ≥ 240; amber if 200–239; red if < 200 |
| Special Camp | Badge | — | ✅ Attended (green) / ❌ Not Attended (red) |
| Conduct | Badge | — | Good (green) / Issue Pending (amber) |
| Eligible? | Badge | — | Eligible (green) / Ineligible (red) / Review Pending (amber) |
| Certificate Status | Badge | — | Not Generated (grey) / Generated (blue) / Downloaded (indigo) / Dispatched (green) |
| Actions | — | — | [View] · [Generate] · [Download] · [Mark Dispatched] |

`[View]` — opens `volunteer-hours-log` drawer.
`[Generate]` — opens `certificate-generate-single` drawer pre-filled with this volunteer's data. Disabled with tooltip "Not Eligible" if `eligible = No`.
`[Download]` — triggers direct Cloudflare R2 signed URL download of generated PDF. Disabled with tooltip "Not Generated Yet" if `certificate_status = Not Generated`.
`[Mark Dispatched]` — opens inline confirmation micro-modal: "Mark certificate as physically dispatched to volunteer?" `[Confirm]` · `[Cancel]`. Updates status to Dispatched.

**Default sort:** Eligible DESC (Eligible rows first), then Volunteer Name ASC.
**Pagination:** 25 rows per page. Controls: `« Previous  Page N of N  Next »`. Rows-per-page: 25 / 50 / 100.
**Bulk actions** (shown when ≥ 1 row selected): `[Generate Certificates for Selected (N)]` (opens `certificate-generate-bulk` with pre-selected volunteers) · `[Export Selected List]` (XLSX).

---

### 5.2 State Directorate Submission Export

Dedicated export panel — not a data table. Displayed below Section 5.1, collapsible. Title: "State Directorate Submission — Annual Export".

> "Export the official NSS completion list for submission to the State NSS Directorate. The format follows the NSS Directorate's prescribed template."

**AY selector** (within this panel, independent of the page-level AY selector): defaults to current AY; can export prior-year data.

**Summary line (auto-calculated):**
```
AY [year]  ·  Branches: [N]  ·  NSS Units: [N]  ·  Total Eligible Volunteers: [N]  ·  Certificates Generated: [N]
```

**Export buttons:**

| Button | Action | Format | Columns Exported |
|---|---|---|---|
| `[Export to XLSX (Directorate Format)]` | Generates XLSX per NSS Directorate prescribed template | XLSX | S.No · Branch · NSS Unit Code · University Affiliation · Volunteer Name · Enrolment No · Class · Total Hours · Special Camp Dates · Certificate Eligible (Y/N) |
| `[Export to PDF (Formatted Report)]` | Generates print-ready group submission report | PDF | All above columns + group name, coordinator name, date, page numbers |
| `[Generate Cover Letter]` | Populates a cover letter template and downloads as DOCX | DOCX | Group name · Coordinator name · Total eligible count · AY · Submission date · Signature block (coordinator name + designation auto-filled) |

All three buttons are Role 100 only. Clicking any button disables the button with "Generating…" text and spinner; re-enables on completion.

**Export log** (compact table, last 5 exports):

| Column | Notes |
|---|---|
| Export Type | XLSX Directorate / PDF Report / Cover Letter |
| AY | Academic year exported |
| Generated On | `DD MMM YYYY HH:MM` |
| Generated By | Coordinator name |
| Download | `[↓ Re-download]` link (Cloudflare R2 signed URL, 24h expiry) |

---

### 5.3 NSS Programme Officer Registry

**Search bar:**
```
[🔍 Search officer name, branch, or university…]  [Branch ▾]  [Training Status ▾]  [Term Status ▾]  [Reset]
```

**Filters:**

| Filter | Options |
|---|---|
| Branch | Multi-select list of all branches |
| Training Status | Multi-select: Trained / Pending / Overdue |
| Term Status | All / Active / Expired / Expiring (within 90 days) |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ▲▼ | Branch short name |
| NSS Unit Code | Text | ▲▼ | |
| University Affiliation | Text | ▲▼ | University the NSS unit is affiliated to |
| Programme Officer Name | Text | ▲▼ | |
| Employee ID | Text | — | Faculty employee ID |
| Training Status | Badge | — | Trained (green) / Pending (amber) / Overdue (red) |
| Appointment Date | Date | ▲▼ | `DD MMM YYYY` |
| Term End Date | Date | ▲▼ | Red text if expired or within 30 days; amber if within 31–90 days |
| Contact No | Text | — | Hidden for Role 99 (Cultural Head) |
| Actions | — | — | [Edit] · [View Unit] · [Send Reminder] |

`[Edit]` — opens `nss-officer-edit` drawer. Role 100 only; hidden for Role 99.
`[View Unit]` — navigates to Page 14 (NSS Programme Tracker) filtered to this unit. Opens in same tab.
`[Send Reminder]` — opens `send-reminder` modal. Role 100 only.

**Default sort:** Term End Date ASC (soonest expiry first, placing expired and expiring records at top).
**Pagination:** 25 rows per page.

---

## 6. Drawers & Modals

### 6.1 `certificate-generate-single` Drawer — 480 px, right-slide

**Trigger:** `[Generate Certificates ▾]` → "Generate for Single Volunteer", or `[Generate]` action in table row.

**Header:** "Generate NSS Certificate — [Volunteer Name]"

**Pre-filled read-only info block:**
```
Volunteer: [Name]  ·  Branch: [Branch]  ·  NSS Unit: [Unit Code]
Hours Completed: [N] hrs  ·  Special Camp: ✅/❌  ·  Conduct: Good/Issue Pending
Eligibility Status: [badge]
```

**Form fields:**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Certificate Date | Date picker | Yes | Defaults to today; cannot be future |
| Coordinator Signature Authority | Text | No | Name to appear as signing authority on certificate; defaults to logged-in Coordinator's name |
| University Name | Text | Auto-filled | Auto-populated from NSS Unit Code's university affiliation record; read-only |
| Download After Generation | Toggle | Yes | Default: on; if on, triggers automatic download of the generated PDF immediately after generation |

**Footer:** `[Cancel]`  `[Generate Certificate]`

On click: button disabled with "Generating…" and spinner; async PDF generation call to FastAPI; on success: certificate status updated to "Generated", toast shown, PDF downloaded if toggle is on.

---

### 6.2 `certificate-generate-bulk` Drawer — 560 px, right-slide

**Trigger:** `[Generate Certificates ▾]` → "Bulk Generate", or `[Generate Certificates for Selected (N)]` bulk action.

**Tabs:** Selection | Preview

---

**Tab: Selection**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Scope | Radio | Yes | All Eligible Volunteers (current AY) / Selected Branches / Custom Selection |
| Branch (if Selected Branches) | Multi-select | Conditional | Shown only when Scope = Selected Branches |
| Volunteer list (if Custom) | Inline table with checkboxes | Conditional | Shown when Scope = Custom Selection; searchable by name/enrolment; pre-selected from bulk action if triggered from table |
| Certificate Date | Date picker | Yes | Defaults to today; cannot be future |
| Signature Authority | Text | No | Defaults to Coordinator name |
| Generate PDF | Checkbox | Yes | Default: checked |

> "Bulk generation may take 2–5 minutes for large groups with 3,000+ eligible volunteers."

---

**Tab: Preview**

Auto-populated when user switches to this tab after setting scope on Selection tab. Tab switch triggers a count API call.

```
[N] certificates will be generated
Across [N] branches  ·  [N] NSS units
Scope: [All Eligible / Selected Branches: Branch A, Branch B / Custom: N selected]
Certificate Date: [DD MMM YYYY]
Signing Authority: [Name]
```

**Breakdown table (compact):**
| Branch | NSS Unit | Eligible Volunteers | Already Generated |
|---|---|---|---|
| Branch Name | Unit Code | N | N |

`[Generate All]` button (indigo) — fires async bulk generation job. On click:
- Button replaced by progress bar: "Generating certificates… [N] of [N]" (polled via HTMX `hx-trigger="every 3s"` against `/api/v1/nss/certificates/bulk-status/{job_id}/`)
- On completion: progress bar replaced by success message "[N] certificates generated successfully." + `[Download All (ZIP)]` button

`[Cancel]` button.

---

### 6.3 `nss-officer-edit` Drawer — 480 px, right-slide

**Trigger:** `[Edit]` action in Section 5.3 table row. Also serves as create (opened via `[+ Add Programme Officer]` button in Section 5.3 header — Role 100 only).

**Header:** "Edit Programme Officer" / "Add Programme Officer"

**Tab:** Single-tab form.

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Branch | Select | Yes | Dropdown of all group branches |
| NSS Unit Code | Text | Yes | E.g. `AP/KR-037`; must match an existing unit in Page 14's unit registry |
| Programme Officer Name | Text | Yes | Full name; min 3, max 100 chars |
| Employee ID | Text | Yes | Alphanumeric; validated against HR roster if integration available |
| University Affiliation | Text | No | University the NSS unit is affiliated to; auto-suggested from unit code |
| Training Status | Select | Yes | Trained / Pending / Overdue |
| Appointment Date | Date picker | Yes | Cannot be future |
| Term End Date | Date picker | No | If set, must be after Appointment Date |
| Contact Number | Text | Yes | 10-digit mobile number; validated format |
| Email | Email | No | Validated format |
| Notes | Textarea | No | Internal notes; max 300 characters |

**Footer:** `[Cancel]`  `[Save]`

---

### 6.4 `send-reminder` Modal — 380 px, centred

**Trigger:** `[Send Reminder]` action in Section 5.3 table row.

**Header:** "Send Reminder — [Programme Officer Name]"

| Field | Type | Required | Notes |
|---|---|---|---|
| To | Read-only text | — | Pre-filled: "[Officer Name] — [email]" |
| CC Branch Principal | Toggle | No | Optional; if on, Branch Principal email added to CC from branch record |
| Message preview | Read-only textarea | — | Pre-populated template: "Dear [Officer Name], this is a reminder regarding your NSS Programme Officer responsibilities for AY [year]. Your term ends on [date]. Please complete outstanding actions. — [Coordinator Name], Group NSS/NCC Coordinator." |
| Additional Note | Text | No | Appended to message body; max 200 characters |

**Footer:** `[Cancel]`  `[Send]`

On send: in-app notification queued; toast shown.

---

### 6.5 `volunteer-hours-log` Drawer — 480 px, right-slide

**Trigger:** `[View]` action in Section 5.1 table row.

**Tabs:** Hours Summary | Activity Log

---

**Tab: Hours Summary**

Read-only info card:
```
[Volunteer Name]  ·  [Branch]  ·  [NSS Unit Code]  ·  Class: [class]
Enrolment No: [no]
```

Progress bar: `[████████████░░░] 210 / 240 hrs` — indigo fill if < 240; green fill if ≥ 240.

| Field | Value |
|---|---|
| Total Hours Completed | [N] hrs |
| Special Camp Attended | ✅ Yes — [Camp Name, dates] / ❌ No |
| Conduct Status | Good / Issue Pending |
| Eligibility | [badge] Eligible / Ineligible / Review Pending |
| Certificate Status | [badge] Not Generated / Generated / Downloaded / Dispatched |

`[Generate Certificate]` button shown at bottom if `eligible = Yes AND certificate_status = Not Generated`. Role 100 only.

---

**Tab: Activity Log**

Sourced from Page 14 (NSS Programme Tracker) activity records.

| Column | Notes |
|---|---|
| Activity Name | Name of NSS activity/camp |
| Type | Regular Activity / Special Camp / Special Programme / Training |
| Date | `DD MMM YYYY` |
| Hours Credited | Number |
| Verification Status | Badge: Verified (green) / Pending (amber) / Rejected (red) |
| Notes | Activity-level notes |

Sorted by Date DESC. Pagination: 15 rows per tab.

---

## 7. Charts

All charts use Chart.js 4.x. Each chart has an `[Export PNG]` button that calls `chart.toBase64Image()` and downloads the image.

### 7.1 Certificate Eligibility Status Distribution

| Attribute | Value |
|---|---|
| Type | Donut chart |
| Data | 4 segments: Eligible (hours ≥ 240 + special camp + good conduct) · Ineligible — Hours Issue (hours < 240) · Ineligible — No Special Camp (hours ≥ 240 but no special camp) · Pending Review (conduct issue or incomplete verification) |
| Colours | Eligible: green-500 · Hours Issue: red-400 · No Special Camp: orange-400 · Pending Review: amber-400 |
| Centre label | Total enrolled volunteers |
| Tooltip | "[Segment Label]: [N] volunteers ([N]%)" |
| Legend | Below chart, horizontal |
| Export | `[Export PNG]` |

### 7.2 Branch-wise Certificate Generation Progress

| Attribute | Value |
|---|---|
| Type | Horizontal stacked bar chart |
| Data | One row per branch (top 10 branches by eligible count); two segments per bar: Generated (green) and Eligible but Not Generated (amber) |
| X-axis | Volunteer count (integer ticks, starts at 0) |
| Y-axis | Branch names |
| Sort | Branches sorted by total eligible count DESC |
| Tooltip | "[Branch Name]: [N] generated / [N] eligible ([N]% complete)" |
| Legend | Generated (green) · Pending Generation (amber) |
| Export | `[Export PNG]` |

---

## 8. Toast Messages

| Action | Toast Text | Type | Duration |
|---|---|---|---|
| Single certificate generated | "Certificate generated for [Volunteer Name]. Ready for download." | Success | 4 s |
| Bulk generation job started | "Bulk certificate generation started. [N] certificates queued." | Info | 4 s |
| Bulk generation complete | "[N] certificates generated and ready for download (ZIP)." | Success | 4 s |
| Certificate marked Dispatched | "Certificate for [Volunteer Name] marked as dispatched." | Success | 4 s |
| Directorate XLSX exported | "Directorate format XLSX exported for AY [year]. [N] volunteers included." | Success | 4 s |
| PDF report exported | "Formatted PDF report exported for AY [year]." | Success | 4 s |
| Cover letter generated | "Cover letter generated and downloaded." | Success | 4 s |
| Programme Officer saved | "Programme Officer record for [Name] saved." | Success | 4 s |
| Reminder sent | "Reminder sent to [Officer Name]." | Success | 4 s |
| Generate attempted — ineligible | "Cannot generate certificate: [Volunteer Name] does not meet eligibility criteria." | Error | Manual dismiss |
| Export failed | "Export generation failed. Please try again or contact support." | Error | Manual dismiss |
| Bulk job failed (partial) | "Bulk generation completed with [N] errors. Download partial ZIP and review error log." | Error | Manual dismiss |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No NSS volunteers in selected AY | "No Volunteer Records" | "No NSS volunteer records are available for AY [year]. Activity data is sourced from the NSS Programme Tracker." | `[Go to NSS Programme Tracker]` |
| No eligible volunteers | "No Eligible Volunteers Yet" | "No volunteers have met the 240-hour + Special Camp eligibility criteria for certificate generation in AY [year]." | None |
| Certificate tracker — filters return no results | "No Results Match Filters" | "Adjust your filters or reset to view all volunteers." | `[Reset Filters]` |
| Section 5.3 — no Programme Officers | "No Programme Officers Recorded" | "No Programme Officer records found. Add Programme Officers to maintain NSS unit compliance." | `[+ Add Programme Officer]` (Role 100 only) |
| Export log — no prior exports | "No Exports Generated" | "No Directorate submission exports have been generated for this group. Generate the first export when ready." | None |
| Volunteer hours log — no activities | "No Activities Logged" | "No NSS activities have been logged for this volunteer in the NSS Programme Tracker." | `[Open Programme Tracker]` |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load — KPI bar | 5 shimmer cards, full width |
| Initial page load — Section 5.1 table | 10 shimmer rows with column-proportional shimmer |
| AY selector change | Section 5.1 table and KPI bar replaced by shimmer; Section 5.3 unchanged |
| Filter / search applied | Table area replaced by 20 px indigo spinner centred in table zone |
| Section 5.3 table initial load | 8 shimmer rows |
| Certificate generate single — in-flight | Button disabled, "Generating…" + inline spinner; overlay prevented by disabled state |
| Bulk generation — in-flight | Progress bar in drawer preview tab: "Generating certificates… [N] / [N]"; polled every 3 s |
| Export button clicked | Button disabled, "Generating export…" + spinner |
| Cover letter generate | Button disabled, "Generating…" + spinner |
| `volunteer-hours-log` drawer — load | Drawer slides in; both tabs show shimmer skeleton while data loads |
| `nss-officer-edit` drawer — pre-fill | Drawer slides in; fields show shimmer briefly while edit data is fetched |

---

## 11. Role-Based UI Visibility

| UI Element | Role 100 — NSS/NCC Coordinator | Role 99 — Cultural Head |
|---|---|---|
| KPI Summary Bar | Full — all 5 cards | Full — all 5 cards (read-only counts) |
| AY selector | Visible | Hidden (Cultural Head sees default AY only) |
| `[Generate Certificates ▾]` button | Visible | Hidden |
| `[Export ↓]` button | Visible | Hidden |
| Section 5.1 — Certificate Tracker table | Full | Hidden entirely |
| Section 5.2 — Directorate Export panel | Full | Hidden entirely |
| Section 5.3 — Programme Officer table | Full — all columns | Visible — Contact No and Email columns hidden |
| `[Edit]` action (Section 5.3) | Visible | Hidden |
| `[Send Reminder]` action (Section 5.3) | Visible | Hidden |
| `[View Unit]` action (Section 5.3) | Visible | Visible |
| `[+ Add Programme Officer]` (Section 5.3 header) | Visible | Hidden |
| Alert banners — all conditions | Full | Only "Programme Officers with expired terms" banner shown |
| Charts 7.1 and 7.2 | Visible | Hidden |
| `volunteer-hours-log` drawer | Accessible (Generate Certificate button visible) | Inaccessible (no trigger rendered) |
| Bulk action bar | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/nss/certificates/` | Role 100 | List volunteers with cert eligibility data; params: `branch`, `eligible`, `cert_status`, `special_camp`, `hours_min`, `hours_max`, `search`, `ay`, `page`, `page_size`, `ordering` |
| GET | `/api/v1/nss/certificates/{volunteer_id}/` | Role 100 | Retrieve single volunteer cert detail including hours log |
| POST | `/api/v1/nss/certificates/{volunteer_id}/generate/` | Role 100 | Generate single certificate PDF; body: `{ cert_date, signature_authority, download_on_complete }` |
| POST | `/api/v1/nss/certificates/bulk-generate/` | Role 100 | Initiate bulk generation job; body: `{ scope, branch_ids, volunteer_ids, cert_date, signature_authority, ay }`; returns `{ job_id }` |
| GET | `/api/v1/nss/certificates/bulk-status/{job_id}/` | Role 100 | Poll bulk generation progress; returns `{ total, completed, failed, status, download_url_zip }` |
| PATCH | `/api/v1/nss/certificates/{volunteer_id}/dispatch/` | Role 100 | Mark certificate status as Dispatched |
| GET | `/api/v1/nss/certificates/kpi-summary/` | Roles 99, 100 | Returns `{ achievers_240h, cert_eligible, generated, pending_generation, programme_officers }`; query: `ay` |
| GET | `/api/v1/nss/certificates/export/directorate-xlsx/` | Role 100 | Export XLSX in directorate format; query: `ay` |
| GET | `/api/v1/nss/certificates/export/formatted-pdf/` | Role 100 | Export formatted PDF report; query: `ay` |
| GET | `/api/v1/nss/certificates/export/cover-letter/` | Role 100 | Generate and download cover letter DOCX; query: `ay` |
| GET | `/api/v1/nss/programme-officers/` | Roles 99, 100 | List Programme Officers; params: `branch`, `training_status`, `term_status`, `search`, `page`, `page_size`, `ordering` |
| POST | `/api/v1/nss/programme-officers/` | Role 100 | Create Programme Officer record |
| PATCH | `/api/v1/nss/programme-officers/{officer_id}/` | Role 100 | Update Programme Officer record |
| POST | `/api/v1/nss/programme-officers/{officer_id}/send-reminder/` | Role 100 | Queue in-app notification to Programme Officer; body: `{ cc_principal, additional_note }` |
| GET | `/api/v1/nss/certificates/chart/eligibility-distribution/` | Role 100 | Returns segment counts for Chart 7.1; query: `ay` |
| GET | `/api/v1/nss/certificates/chart/branch-progress/` | Role 100 | Returns top-10 branch progress data for Chart 7.2; query: `ay` |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar on page load | `load` | GET `/api/v1/nss/certificates/kpi-summary/?ay={ay}` | `#nss-cert-kpi-bar` | `innerHTML` |
| KPI bar after cert action | `certAction from:body` | GET `/api/v1/nss/certificates/kpi-summary/?ay={ay}` | `#nss-cert-kpi-bar` | `innerHTML` |
| Section 5.1 table on page load | `load` | GET `/api/v1/nss/certificates/?page=1&ay={ay}` | `#cert-tracker-table` | `innerHTML` |
| AY selector change | `change` | GET `/api/v1/nss/certificates/?ay={new_ay}&page=1` | `#cert-tracker-table` | `innerHTML` |
| Filter / search change | `change, input delay:400ms` | GET `/api/v1/nss/certificates/` (hx-include all filter inputs) | `#cert-tracker-table` | `innerHTML` |
| `[Generate]` action (single) | `click` | GET `/htmx/nss/certificates/{volunteer_id}/generate-drawer/` | `#drawer-container` | `innerHTML` |
| `[View]` action | `click` | GET `/htmx/nss/certificates/{volunteer_id}/hours-log-drawer/` | `#drawer-container` | `innerHTML` |
| `[Mark Dispatched]` confirm | `click` | PATCH `/api/v1/nss/certificates/{volunteer_id}/dispatch/` | `#cert-row-{volunteer_id}` | `outerHTML` |
| Section 5.3 table on page load | `load` | GET `/api/v1/nss/programme-officers/?page=1` | `#officer-registry-table` | `innerHTML` |
| Section 5.3 filter change | `change` | GET `/api/v1/nss/programme-officers/` (hx-include filter inputs) | `#officer-registry-table` | `innerHTML` |
| `[Edit]` action (Section 5.3) | `click` | GET `/htmx/nss/programme-officers/{officer_id}/edit-drawer/` | `#drawer-container` | `innerHTML` |
| Officer edit form submit | `submit` | PATCH `/api/v1/nss/programme-officers/{officer_id}/` | `#officer-registry-table` | `innerHTML` |
| `[Send Reminder]` action | `click` | GET `/htmx/nss/programme-officers/{officer_id}/reminder-modal/` | `#modal-container` | `innerHTML` |
| Bulk generation progress poll | `every 3s [status != complete]` | GET `/api/v1/nss/certificates/bulk-status/{job_id}/` | `#bulk-progress-bar` | `innerHTML` |
| Certificate generate single submit | `submit` | POST `/api/v1/nss/certificates/{volunteer_id}/generate/` | `#cert-row-{volunteer_id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
