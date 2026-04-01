# 11 — Anti-Ragging Complaint Register

> **URL:** `/group/welfare/anti-ragging/complaints/`
> **File:** `11-anti-ragging-complaint-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Anti-Ragging Committee Head (Role 91, G3)

---

## 1. Purpose

Complete register of all anti-ragging complaints received across all branches of the group. The UGC Anti-Ragging Regulations 2009 (as amended) and the Supreme Court of India's directives in the Raghavan Committee case mandate that every institution receiving a complaint — irrespective of perceived severity — must initiate a formal investigation. There is no threshold below which a complaint may be dismissed without process.

Complaints may arrive via five channels: (a) direct student or parent report to branch, (b) UGC anti-ragging helpline (1800-180-5522), (c) anonymous online submission form, (d) faculty or staff report, or (e) referral based on CCTV footage review. Regardless of source, every complaint must pass through the UGC-mandated lifecycle: Preliminary Inquiry (within 7 working days of receipt) → Full Investigation (within 30 days) → Finding → Penalty or Resolution → Closure. Any complaint not acted upon within these timelines constitutes a regulatory breach reportable to UGC.

Additionally, every complaint must be reported to the UGC's centralised anti-ragging database (www.antiragging.in). This page provides the Anti-Ragging Committee Head with a complete, real-time view of all complaints across all branches, their current stage, SLA compliance status, UGC reporting status, and escalation flags. Scale: 0–10 complaints per year is typical for a well-run group, but each must be treated with the same rigour.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Anti-Ragging Committee Head | G3, Role 91 | Full — create, view all fields, update stage, record penalty, export | Primary owner |
| Group CEO | G4 | View only — all rows, all fields | No edit capability |
| Branch Principal | Branch-level | View — own branch complaints only; can initiate new complaint | Cannot view other branches; cannot update stage or penalty |
| Branch Anti-Ragging Coordinator | Branch-level | View — own branch; cannot edit | Read-only access to own branch complaints |
| Group Legal & Compliance Officer | G3 | View only — all rows for legal audit | No edit capability |
| All other roles | — | No access | Redirected to own dashboard |

> **Access enforcement:** Django decorator `@require_role(['anti_ragging_head'])` for write actions. Branch-scoped queryset applied to branch-level roles via `complaints.filter(branch=request.user.branch)`. Description fields are encrypted at rest; decrypted on-screen only for Role 91 and Group CEO.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Anti-Ragging  ›  Complaint Register
```

### 3.2 Page Header
```
Anti-Ragging Complaint Register                   [+ New Complaint]  [Export ↓]  [UGC Reporting Status ↗]
Group Anti-Ragging Committee Head — [Officer Name]
AY [academic year]  ·  [N] Total Complaints  ·  [N] Active  ·  [N] Closed  ·  [N] UGC Reported
```

`[+ New Complaint]` — opens `new-complaint` drawer. Role 91 and Branch Principal (limited form).
`[Export ↓]` — exports complaint log (non-confidential fields only) to PDF/XLSX.
`[UGC Reporting Status ↗]` — navigates to UGC anti-ragging portal (external link, new tab). Indicates count of complaints not yet reported to UGC database in badge.

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Preliminary Inquiry SLA breached | "[N] complaint(s) have not completed Preliminary Inquiry within 7 working days. UGC compliance breach." | Red |
| Full Investigation SLA breached | "[N] complaint(s) have exceeded the 30-day Full Investigation deadline." | Red |
| UGC database not updated | "[N] complaint(s) have not been reported to the UGC anti-ragging database." | Red |
| Complaint received via UGC helpline not acknowledged | "Helpline complaint [ID] received [N] days ago has not been acknowledged." | Red |
| Active complaint with no assigned committee member | "Complaint [ID] has no committee member assigned. Assign immediately." | Amber |
| Penalty imposed — notification to UGC pending | "Penalty for complaint [ID] must be reported to UGC within 3 days of imposition." | Amber |

---

## 4. KPI Summary Bar

Five metric cards displayed horizontally.

| Card | Metric | Colour Rule |
|---|---|---|
| Total Complaints (This AY) | Count of all complaints in current academic year | Grey (neutral) |
| Active Cases | Count where `stage ≠ Closed and ≠ Appealed` | Red if > 3; Amber if 1–3; Green if 0 |
| 7-Day Preliminary SLA Breaches | Count of active complaints with preliminary inquiry > 7 working days | Red if > 0; Green if 0 |
| 30-Day Full Investigation SLA Breaches | Count where full investigation > 30 days | Red if > 0; Green if 0 |
| UGC Not Reported | Count of complaints where `ugc_reported = False` | Red if > 0; Green if 0 |

```
┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐
│  Total (This AY)   │ │   Active Cases     │ │ 7-Day SLA Breaches │ │ 30-Day SLA Breach  │ │  UGC Not Reported  │
│        7           │ │        3           │ │        0           │ │        1           │ │        1           │
│   ● Grey           │ │   ● Red            │ │   ● Green          │ │   ● Red            │ │   ● Red            │
└────────────────────┘ └────────────────────┘ └────────────────────┘ └────────────────────┘ └────────────────────┘
```

---

## 5. Sections

### 5.1 Filters and Search Bar

```
[🔍 Search by Complaint ID / Branch]  [Branch ▾]  [Source ▾]  [Nature ▾]  [Stage ▾]  [7-Day SLA ▾]  [30-Day SLA ▾]  [UGC Reported ▾]  [Date Range 📅]  [Reset Filters]
```

| Filter | Options |
|---|---|
| Branch | All Branches / individual branch names |
| Source | All / Online Form / UGC Helpline / Staff Report / Parent Report / Anonymous / CCTV Referral |
| Nature | All / Verbal / Physical / Psychological / Cyber / Sexual |
| Stage | All / Preliminary Inquiry / Full Investigation / Finding / Penalty / Closed / Appealed |
| 7-Day SLA | All / On Track (✅) / At Risk (⚠) / Breached (❌) |
| 30-Day SLA | All / On Track (✅) / At Risk (⚠) / Breached (❌) |
| UGC Reported | All / Yes / No |
| Date Range | Custom date picker on `received_date` |

### 5.2 Complaint Table

Columns, sortable where marked (▲▼):

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Complaint ID | `complaint_id` (auto) | ▲▼ | Format: `AR-AY-NNNN` e.g. `AR-2526-0003` |
| Branch | `branch.short_name` | ▲▼ | — |
| Received Date | `received_date` | ▲▼ | `DD MMM YYYY` |
| Source | `source` | — | Badge: Online Form (Blue) · Helpline (Purple) · Staff Report (Teal) · Parent (Green) · Anonymous (Grey) · CCTV (Orange) |
| Accused Type | `accused_type` | — | Senior Student / Peer / Staff |
| Nature | `complaint_nature` | — | Verbal / Physical / Psychological / Cyber / Sexual |
| Stage | `current_stage` | ▲▼ | Colour-coded pill (see §5.3) |
| Days Since Filing | Computed | ▲▼ | Integer |
| 7-Day SLA | Computed | — | ✅ On Track · ⚠ At Risk · ❌ Breached |
| 30-Day SLA | Computed | — | ✅ On Track · ⚠ At Risk · ❌ Breached |
| UGC Reported | `ugc_reported` | — | ✅ / ❌ |
| Status | `status` | ▲▼ | Open / In Investigation / Finding Issued / Closed / Appealed |
| Actions | — | — | [View] · [Update Stage] · [Record Penalty] |

**Default sort:** `status` (Open/active first) then `received_date` ascending.

**Pagination:** 15 rows per page. Controls: `« Previous  Page N of N  Next »`. Rows-per-page: 15 / 25 / 50.

### 5.3 Stage Colour Coding

| Stage | Pill Colour |
|---|---|
| Preliminary Inquiry | Yellow |
| Full Investigation | Orange |
| Finding | Purple |
| Penalty | Red |
| Closed | Green |
| Appealed | Indigo |

### 5.4 SLA Status Logic

**7-Day Preliminary Inquiry SLA** (from `received_date`, counting working days):
- On Track (✅): ≤ 5 working days elapsed
- At Risk (⚠): 5–7 working days elapsed, inquiry not complete
- Breached (❌): > 7 working days elapsed, inquiry not complete

**30-Day Full Investigation SLA** (from `investigation_start_date`):
- On Track (✅): ≤ 21 calendar days elapsed
- At Risk (⚠): 21–30 days elapsed, investigation not complete
- Breached (❌): > 30 days elapsed, investigation not complete

---

## 6. Drawers / Modals

### 6.1 `complaint-detail` Drawer — 700 px, right-slide

**Trigger:** `[View]` button in table row.

**Header:**
```
Complaint [AR-2526-0003]                                            [×]
[Branch Name]  ·  Received: DD MMM YYYY  ·  Stage: [stage pill]
SLA: 7-Day [✅/⚠/❌]  ·  30-Day [✅/⚠/❌]  ·  UGC Reported: [✅/❌]
```

**Tab Bar:**
```
[Overview]  [Inquiry Log]  [Investigation Log]  [Penalty]  [UGC Reporting]  [Appeals]
```

**Tab 1 — Overview**

| Field | Value | Confidentiality |
|---|---|---|
| Complaint ID | `AR-2526-0003` | Public (to authorised roles) |
| Branch | [Branch Name] | Public |
| Received Date | DD MMM YYYY | Public |
| Source | Online Form / Helpline / etc. | Public |
| Accused Type | Senior Student / Peer / Staff | Public |
| Nature | Verbal / Physical / Psychological / Cyber / Sexual | Public |
| Description | [full text] | `[CONFIDENTIAL]` — encrypted; shown only to Role 91 and CEO |
| Complainant Code | `COMP-0003` (anonymised) | Public (anonymised) |
| Accused Code | `ACC-0003` (anonymised) | Public (anonymised) |
| Assigned Committee Member | [Name, Designation] | Public |
| Days Since Filing | [N] | Public |

**Tab 2 — Inquiry Log**

Timeline of preliminary inquiry actions:
```
[DD MMM YYYY · HH:MM]  [Committee Member]  [Action: e.g. "Witness interviewed — Student X"]  [Notes — CONFIDENTIAL]
```
`[+ Add Inquiry Entry]` button — Role 91 only. Each entry immutable once saved.

**Tab 3 — Investigation Log**

Same format as Inquiry Log but for Full Investigation phase. Shows investigation steps, evidence collection, and hearing records.

**Tab 4 — Penalty**

| Field | Value |
|---|---|
| Penalty Type | Suspension / Expulsion / Fine / Community Service / Counselling / Other |
| Penalty Details | [details] |
| Effective Date | DD MMM YYYY |
| Approved By | [Approving authority] |
| Appeal Window | [N] days remaining / Expired |

`[Record Penalty]` — opens `record-penalty` drawer. Only if stage is "Finding" and no penalty recorded yet.

**Tab 5 — UGC Reporting**

| Field | Value |
|---|---|
| UGC Database Reported | ✅ Yes / ❌ No |
| Date Reported | DD MMM YYYY |
| UGC Reference Number | [ref] |
| Penalty Reported to UGC | ✅ / ❌ |

`[Mark as UGC Reported]` — opens small inline form to enter date and reference number. Role 91 only.

**Tab 6 — Appeals**

| Field | Value |
|---|---|
| Appeal Filed | Yes / No |
| Appeal Date | DD MMM YYYY |
| Appealing Party | Complainant / Accused |
| Appeal Authority | [body] |
| Appeal Status | Pending / Upheld / Dismissed |
| Appeal Finding | [text — CONFIDENTIAL] |

`[Record Appeal]` — inline form. Role 91 only.

**Footer:** `[Update Stage]` (Role 91 only) · `[Export Case Summary PDF]`

---

### 6.2 `new-complaint` Drawer — 640 px, right-slide

**Trigger:** `[+ New Complaint]` header button.

**Header:**
```
Register New Anti-Ragging Complaint
All complaints are treated with equal gravity regardless of perceived severity.
```

**Fields:**

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Branch | Select | Yes | Locked to own branch for Branch Principal |
| Date Received | Date picker | Yes | Cannot be future date |
| Source | Select | Yes | Online Form · UGC Helpline · Staff Report · Parent Report · Anonymous · CCTV Referral |
| UGC Helpline Reference | Text | Conditional | Required if Source = UGC Helpline |
| Accused Type | Radio | Yes | Senior Student · Peer · Staff |
| Nature | Multi-select checkboxes | Yes | Verbal · Physical · Psychological · Cyber · Sexual (select all that apply) |
| Description | Textarea (encrypted) | Yes | Min 50 characters; `[CONFIDENTIAL]`; AES-256 encrypted at rest |
| Complainant Code | Text (auto-generated) | — | Auto-assigned in format `COMP-[NNNN]`; anonymised |
| Accused Code | Text (auto-generated) | — | Auto-assigned in format `ACC-[NNNN]`; anonymised |
| Assigned Committee Member | Select | No | From committee member register |
| Supporting Document | File upload | No | PDF/DOCX/JPG; max 20 MB |

**Validation:**
- `Date Received` must not be future.
- `Description` minimum 50 characters.
- If Source = UGC Helpline, `UGC Helpline Reference` field is mandatory.
- On save: 7-working-day SLA timer starts; stage set to "Preliminary Inquiry".

**Footer:** `[Cancel]`  `[Save & Register Complaint ▶]`

Branch Principal role gate: sees only Branch (locked), Date Received, Source, Accused Type, Nature, Description. Cannot see or assign committee member.

---

### 6.3 `update-stage` Drawer — 480 px, right-slide

**Trigger:** `[Update Stage]` button in complaint detail footer or table row action. Role 91 only.

**Header:**
```
Update Stage — Complaint [AR-2526-0003]
Current Stage: [stage pill]  ·  SLA: [indicator]
```

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| New Stage | Select | Yes | Forward progression only; options: next valid stage(s) based on current stage |
| Stage Change Date | Date picker | Yes | Defaults to today |
| Notes | Textarea | Yes | Min 20 characters; `[CONFIDENTIAL]` |
| Notify Committee Member | Checkbox | No | Auto-notification to assigned member |
| UGC Update Required | Auto-indicator | — | System shows "UGC database update may be required for this stage change" if applicable |

**Stage Transition Rules:**
- Preliminary Inquiry → Full Investigation (preliminary finding must be documented in Inquiry Log)
- Full Investigation → Finding (investigation report must exist)
- Finding → Penalty or Closed (Finding tab must be populated)
- Penalty / Closed → Appealed (appeal record required in Appeals tab)
- Appealed → Closed (appeal outcome required)

**Footer:** `[Cancel]`  `[Save Stage Update]`

---

### 6.4 `record-penalty` Drawer — 440 px, right-slide

**Trigger:** `[Record Penalty]` in Penalty tab of detail drawer. Role 91 only.

**Header:**
```
Record Penalty — Complaint [AR-2526-0003]
```

**Fields:**

| Field | Type | Required | Validation |
|---|---|---|---|
| Penalty Type | Select | Yes | Suspension · Expulsion · Fine · Community Service · Mandatory Counselling · Written Warning · Other |
| Penalty Details | Textarea | Yes | Min 30 characters |
| Effective Date | Date picker | Yes | Cannot be before `finding_date` |
| Duration (if suspension) | Text | Conditional | Required if Penalty Type = Suspension; format: "[N] days / semester / year" |
| Fine Amount (if fine) | Number | Conditional | Required if Penalty Type = Fine; currency in INR |
| Approving Authority | Select | Yes | Principal · Group Anti-Ragging Committee · Board |
| Approval Reference | Text | Yes | Meeting minutes reference or approval order number |
| UGC Report Required | Checkbox | Yes | Pre-checked; UGC must be informed of all penalties within 3 days |

**Validation:**
- Effective Date cannot precede the Finding Date.
- If UGC Report Required is unchecked, inline warning: "UGC regulations require reporting all penalties. Unchecking is not recommended."
- On save: stage auto-updated to "Penalty"; UGC reporting flag set to pending.

**Footer:** `[Cancel]`  `[Save Penalty Record]`

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Complaint registered | "Complaint [AR-ID] registered. 7-working-day Preliminary Inquiry SLA has started." | Success |
| Stage updated | "Stage updated to [Stage]. Audit trail updated." | Success |
| Inquiry / investigation entry added | "Entry recorded in [Inquiry/Investigation] Log. This entry is permanent." | Success |
| Penalty recorded | "Penalty recorded for Complaint [ID]. UGC must be notified within 3 days." | Success |
| UGC reported marked | "UGC reporting marked. Reference number saved." | Success |
| Export complete | "Complaint register exported to [format]." | Success |
| SLA breach auto-detected | "Warning: 7-day Preliminary Inquiry SLA breached for Complaint [ID]." | Warning |
| Validation — description too short | "Description must be at least 50 characters." | Error |
| Stage skip attempt | "Stage cannot be skipped. Complete [intermediate stage] first." | Error |
| Unauthorised action | "Access denied. This action requires Anti-Ragging Committee Head privileges." | Error |

---

## 8. Empty States

| Context | Illustration | Heading | Sub-text | Action |
|---|---|---|---|---|
| No complaints this AY | Shield with checkmark | "No Anti-Ragging Complaints Registered" | "No complaints have been received this academic year. The register is active." | `[Register First Complaint]` (Role 91) |
| No results match filters | Funnel icon | "No Complaints Match Filters" | "Adjust filters or reset to see all complaints." | `[Reset Filters]` |
| Inquiry log — no entries | Timeline icon | "No Inquiry Entries" | "Add the first preliminary inquiry entry to begin the official record." | `[+ Add Inquiry Entry]` (Role 91) |
| Penalty tab — no penalty recorded | Gavel icon | "No Penalty Recorded" | "Record the committee's finding and penalty once the investigation concludes." | `[Record Penalty]` (Role 91) |
| Appeals tab — no appeals | Balance scale icon | "No Appeals Filed" | "No party has filed an appeal for this complaint." | None |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 5 shimmer cards. Table: 8 shimmer rows |
| Filter application | Table content replaced by spinner (20 px, indigo) while HTMX fetches |
| Complaint detail drawer opening | Drawer slides in; content area shows spinner |
| Tab switching in detail drawer | Tab body shows spinner while HTMX fetches tab data |
| `[Save & Register Complaint]` | Button disabled, text: "Saving…", spinner |
| `[Save Stage Update]` | Button disabled, text: "Updating…" |
| `[Save Penalty Record]` | Button disabled, text: "Recording…" |
| Export | Button disabled, spinner; text: "Generating…" |

---

## 10. Role-Based UI Visibility

| UI Element | Role 91 (AR Head) | Group CEO | Branch Principal | Branch AR Coord. | Legal Compliance | All Others |
|---|---|---|---|---|---|---|
| KPI Summary Bar | Full | Full | Own branch only | Own branch only | Full | Hidden |
| Complaint table — all branches | Visible | Visible | Own branch only | Own branch only | Visible | Hidden |
| `[CONFIDENTIAL]` description field | Decrypted | Decrypted | Not visible | Not visible | Not visible | Not visible |
| `[View]` action button | Visible | Visible | Visible (own branch) | Visible (own branch) | Visible | Hidden |
| `[Update Stage]` action button | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Record Penalty]` action button | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[+ New Complaint]` header button | Visible | Hidden | Visible (limited form) | Hidden | Hidden | Hidden |
| `[Export ↓]` button | Visible | Visible | Visible (own branch) | Hidden | Visible | Hidden |
| `[+ Add Inquiry Entry]` in log | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Mark as UGC Reported]` | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Record Appeal]` | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Alert banner | Full detail | Full detail | Own branch only | Own branch only | Full detail | Hidden |

---

## 11. API Endpoints

### 11.1 List & Filter Complaints
```
GET /api/v1/welfare/anti-ragging/complaints/
```

| Query Parameter | Type | Description |
|---|---|---|
| `branch_id` | integer | Filter by branch |
| `source` | string | `online_form` · `ugc_helpline` · `staff_report` · `parent_report` · `anonymous` · `cctv_referral` |
| `nature` | string | `verbal` · `physical` · `psychological` · `cyber` · `sexual` |
| `stage` | string | `preliminary_inquiry` · `full_investigation` · `finding` · `penalty` · `closed` · `appealed` |
| `sla_7day` | string | `on_track` · `at_risk` · `breached` |
| `sla_30day` | string | `on_track` · `at_risk` · `breached` |
| `ugc_reported` | boolean | `true` · `false` |
| `date_from` | date (YYYY-MM-DD) | Filter `received_date` from |
| `date_to` | date (YYYY-MM-DD) | Filter `received_date` to |
| `search` | string | Searches `complaint_id` and `branch.short_name` |
| `page` | integer | Default: 1 |
| `page_size` | integer | 15 · 25 · 50 (default: 15) |
| `ordering` | string | `received_date` · `-received_date` · `days_since_filing` · `stage` |

### 11.2 Retrieve Complaint Detail
```
GET /api/v1/welfare/anti-ragging/complaints/{complaint_id}/
```
`description` field decrypted only for Role 91 and CEO.

### 11.3 Create Complaint
```
POST /api/v1/welfare/anti-ragging/complaints/
```
Body: `branch`, `received_date`, `source`, `ugc_helpline_ref` (optional), `accused_type`, `complaint_nature[]`, `description` (encrypted server-side), `assigned_committee_member` (optional), `document` (file, optional).
Response: 201 Created — returns `complaint_id`, `stage`, `sla_preliminary_due`.

### 11.4 Update Stage
```
PATCH /api/v1/welfare/anti-ragging/complaints/{complaint_id}/stage/
```
Body: `new_stage`, `stage_change_date`, `notes` (encrypted), `notify_member` (bool).

### 11.5 Add Inquiry / Investigation Log Entry
```
POST /api/v1/welfare/anti-ragging/complaints/{complaint_id}/inquiry-log/
POST /api/v1/welfare/anti-ragging/complaints/{complaint_id}/investigation-log/
```
Body: `entry_date`, `action`, `notes` (encrypted). Entries are immutable on creation.

### 11.6 Record Penalty
```
POST /api/v1/welfare/anti-ragging/complaints/{complaint_id}/penalty/
```
Body: `penalty_type`, `details`, `effective_date`, `duration` (optional), `fine_amount` (optional), `approving_authority`, `approval_reference`, `ugc_report_required` (bool).

### 11.7 Mark UGC Reported
```
PATCH /api/v1/welfare/anti-ragging/complaints/{complaint_id}/ugc-reporting/
```
Body: `reported_date`, `ugc_reference_number`, `penalty_reported` (bool).

### 11.8 Record Appeal
```
POST /api/v1/welfare/anti-ragging/complaints/{complaint_id}/appeal/
```
Body: `appeal_date`, `appealing_party`, `appeal_authority`, `status`, `finding` (encrypted, optional).

### 11.9 KPI Summary
```
GET /api/v1/welfare/anti-ragging/complaints/kpi-summary/
```
Response: `{ total_this_ay, active_cases, sla_7day_breaches, sla_30day_breaches, ugc_not_reported }`.

### 11.10 Export
```
GET /api/v1/welfare/anti-ragging/complaints/export/
```
Query: all filter params + `format` (`pdf` · `xlsx`). Exports non-confidential fields only.

---

## 12. HTMX Patterns

### 12.1 Table Initialisation
```html
<div id="ar-complaint-table"
     hx-get="/api/v1/welfare/anti-ragging/complaints/?page=1&page_size=15"
     hx-trigger="load"
     hx-swap="innerHTML"
     hx-indicator="#table-spinner">
</div>
```

### 12.2 Multi-Filter Application
```html
<select name="stage"
        id="filter-stage"
        hx-get="/api/v1/welfare/anti-ragging/complaints/"
        hx-trigger="change"
        hx-target="#ar-complaint-table"
        hx-swap="innerHTML"
        hx-include="#filter-branch, #filter-source, #filter-nature, #filter-sla-7day, #filter-sla-30day, #filter-ugc, #filter-date-from, #filter-date-to, #search-input">
</select>
```

### 12.3 Complaint Detail Drawer
```html
<button hx-get="/htmx/welfare/anti-ragging/complaints/{{ complaint_id }}/detail/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        class="text-indigo-600 hover:underline text-sm">
  View
</button>
```

### 12.4 Detail Drawer Tab Switching
```html
<button hx-get="/htmx/welfare/anti-ragging/complaints/{{ complaint_id }}/tab/inquiry-log/"
        hx-target="#drawer-tab-content"
        hx-swap="innerHTML"
        hx-trigger="click"
        class="drawer-tab-btn">
  Inquiry Log
</button>
```

### 12.5 New Complaint Form
```html
<form hx-post="/api/v1/welfare/anti-ragging/complaints/"
      hx-encoding="multipart/form-data"
      hx-target="#ar-complaint-table"
      hx-swap="innerHTML"
      hx-on::after-request="closeDrawer(); showToast(event); refreshKPI();">
</form>
```

### 12.6 UGC Helpline Reference Conditional Field
```html
<select name="source"
        hx-get="/htmx/welfare/anti-ragging/complaints/source-fields/"
        hx-target="#conditional-source-fields"
        hx-swap="innerHTML"
        hx-trigger="change">
</select>
<div id="conditional-source-fields"></div>
```
Server returns `ugc_helpline_ref` field block only when `source = ugc_helpline`.

### 12.7 Stage Update Form
```html
<form hx-patch="/api/v1/welfare/anti-ragging/complaints/{{ complaint_id }}/stage/"
      hx-target="#drawer-tab-content"
      hx-swap="innerHTML"
      hx-on::after-request="refreshTable(); showToast(event);">
</form>
```

### 12.8 Inline UGC Reporting Mark
```html
<button hx-patch="/api/v1/welfare/anti-ragging/complaints/{{ complaint_id }}/ugc-reporting/"
        hx-vals='{"reported_date": "{{ today }}"}'
        hx-target="#ugc-reporting-tab"
        hx-swap="innerHTML"
        hx-confirm="Mark this complaint as reported to the UGC database? Ensure you have the reference number."
        class="btn-sm btn-success">
  Mark as UGC Reported
</button>
```

### 12.9 KPI Auto-Refresh
```html
<div id="ar-kpi-bar"
     hx-get="/api/v1/welfare/anti-ragging/complaints/kpi-summary/"
     hx-trigger="load, every 300s"
     hx-swap="innerHTML">
</div>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
