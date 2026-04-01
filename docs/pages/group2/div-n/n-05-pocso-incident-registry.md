# [05] — POCSO Incident Registry

> **URL:** `/group/legal/pocso/`
> **File:** `n-05-pocso-incident-registry.md`
> **Template:** `portal_base.html` (light theme — restricted)
> **Priority:** P0
> **Role:** Group POCSO Reporting Officer (Role 112, G1) — POCSO Act 2012 mandatory incident recording and NCPCR reporting

---

## 1. Purpose

The POCSO Incident Registry is the most access-restricted page in Division N. It manages the mandatory reporting obligations under the Protection of Children from Sexual Offences (POCSO) Act 2012. Under Section 19 of the POCSO Act, any person who has knowledge of a sexual offence against a child must report it to the Special Juvenile Police Unit (SJPU) or local police. Under Section 21, failure to report is itself a criminal offence. Additionally, the National Commission for Protection of Child Rights (NCPCR) requires institutions to report incidents through their online portal within 24 hours of coming to the institution's knowledge.

The Group POCSO Reporting Officer is responsible for: receiving incident reports escalated from Branch Principals; recording all mandatory details; coordinating with the Internal Committee; tracking police FIR status; and submitting the required NCPCR report within 24 hours. This page provides a controlled, encrypted environment to manage these obligations without exposing sensitive child-related data to unauthorised staff.

All data on this page is encrypted at rest using AES-256. Every access (read, write, export) is immutably logged in an audit trail that cannot be modified by any user including G5 Super Admin. No bulk CSV export is permitted without explicit G5 approval and audit logging. Student identifiers in the list view are masked — full names visible only in the detail drawer for authorised roles.

Scale: 5–50 branches · 0–10 incidents per year group-wide (each incident is high-severity)

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Advises on legal proceedings externally |
| Group Compliance Manager | 109 | G1 | Read — Restricted View | Sees aggregate counts only; no individual incident details |
| Group RTI Officer | 110 | G1 | No Access | POCSO records are exempt from RTI disclosure (s.8(1)(h)) |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | No role in POCSO |
| Group POCSO Reporting Officer | 112 | G1 | Full Read + Record + Upload | Primary user; can record incidents, upload NCPCR submissions |
| Group Data Privacy Officer | 113 | G1 | No Access | POCSO data processed under separate legal basis |
| Group Contract Administrator | 127 | G3 | No Access | No role in POCSO |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Limited | Views only criminal proceedings and court case tracking |
| Group Insurance Coordinator | 129 | G1 | No Access | No role in POCSO |

> **Access enforcement:** `@require_role(roles=[112,128], min_level=G1)` for detail access. Role 109 sees counts only. G4 (CEO) reads summary; G5 (Chairman) reads full details.
>
> **Security:** All access logged in immutable audit table (`pocso_access_log`). Failed access attempts logged and alerted to G5. Session timeout on this page: 15 minutes (overrides global timeout). No clipboard copy on masked fields.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  POCSO Incident Registry   [🔒 Restricted]
```

### 3.2 Page Header
```
POCSO Incident Registry                         [+ Record Incident]  [Export — G5 Only]
Group POCSO Reporting Officer — [Officer Name]
[Group Name] · Restricted Access · Session: [time remaining]
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any incident recorded within past 24 hours without NCPCR submission | "CRITICAL: Incident [INC-NNNN] requires NCPCR reporting — [X] hours remaining. POCSO Act s.19." | Critical (red, sticky) |
| Any incident with no FIR reference after 48 hours | "Incident [INC-NNNN] — no police FIR reference recorded after 48 hours. Escalate immediately." | Critical (red) |
| Any Internal Committee review overdue | "Internal Committee review overdue for [N] incident(s). POCSO s.19 mandates timely review." | High (amber) |
| Session expiring in 2 minutes | "Your session will expire in 2 minutes due to inactivity. Click to extend." | Warning (yellow) |
| NCPCR portal maintenance notification | "NCPCR portal may be under maintenance. Confirm submission via email if portal is unavailable." | Info (blue) |

---

## 4. KPI Summary Bar (6 cards)
> Note: KPI cards for POCSO contain aggregate counts only — no individual identifiers.

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Incidents (This FY) | Count | COUNT pocso_incidents WHERE fy = current_fy | Blue (neutral) | `#kpi-total-incidents` |
| 2 | NCPCR Reports Submitted | Count | COUNT WHERE ncpcr_submitted = True | Green if = total, Red if < total | `#kpi-ncpcr-submitted` |
| 3 | NCPCR Reports Pending | Count | COUNT WHERE ncpcr_submitted = False | Red if > 0, Green = 0 | `#kpi-ncpcr-pending` |
| 4 | Active Incidents (Open) | Count | COUNT WHERE status NOT IN ('closed','archived') | Red if > 0, Green = 0 | `#kpi-active` |
| 5 | FIR Filed | Count (this FY) | COUNT WHERE police_fir_filed = True | Blue | `#kpi-fir-filed` |
| 6 | Cases Resolved | Count (this FY) | COUNT WHERE status = 'closed' | Green | `#kpi-resolved` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/pocso/kpis/"` with `hx-trigger="load, every 120s"` (shorter interval for critical data).

---

## 5. Sections

### 5.1 Incident List (Main Table)

**Search:** Search by Incident ID or Branch only (no free-text name search in list view — protects victim identity).

**Filters:**
- Status: `All` · `Recorded` · `NCPCR Pending` · `Under Investigation` · `Closed` · `Archived`
- Branch: dropdown
- NCPCR Status: `Submitted` · `Pending`
- FIR Status: `Filed` · `Not Filed` · `Not Applicable`
- Period: FY selector

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Incident ID | Text (monospace) | Yes | Auto-generated: INC-YYYY-NNNN |
| Recorded Date | Date | Yes | Date incident was recorded in this system |
| Incident Date | Date | Yes | Date incident occurred (may differ from recorded date) |
| Branch | Text | Yes | Branch name only — no address displayed in list |
| Victim Identifier | Masked text | No | "Student – [Age Group]" only (e.g., "Student – Minor F, 14y") — no name |
| Type | Badge | No | Type masked to "POCSO Incident" in list — details in drawer only |
| NCPCR Status | Badge | Yes | Submitted (green) / Pending (red) / N/A |
| Hours to NCPCR Deadline | Badge | Conditional | Shown only if NCPCR not yet submitted; red if < 6 hours |
| FIR Status | Badge | Yes | Filed / Not Filed / N/A |
| Internal Committee | Badge | Yes | Convened / Pending / N/A |
| Status | Badge | Yes | Recorded / Under Investigation / Closed |
| Actions | Buttons | No | [View Details] (authorised roles only) |

**Default sort:** Recorded Date DESC (most recent first)
**Pagination:** Server-side · Default 25/page

> **Security controls on list view:**
> - Victim name, address, contact details NOT shown in list view under any circumstances
> - All columns except Incident ID and Branch rendered server-side with role-based masking
> - Table HTML does not include hidden/data attributes with sensitive fields

---

## 6. Drawers & Modals

### 6.1 Drawer: `pocso-incident-detail` (760px, right-slide)
Access: Role 112 (POCSO Officer), Role 128 (Legal Dispute Coord — limited tabs), G5 (Chairman).
**Access to this drawer is itself logged in `pocso_access_log`.**

- **Tabs:** Overview · Victim & Perpetrator Details · NCPCR Submission · Police & Legal · Internal Committee · Documents · Timeline
- **Overview tab:**
  - Incident ID, Recorded Date, Incident Date, Incident Location (campus/hostel/other)
  - Branch, Branch Principal (who reported internally), Date reported to Group POCSO Officer
  - Status badge, Urgency level
  - Hours elapsed since incident knowledge (countdown to 24-hr NCPCR deadline if not yet submitted)
  - Brief Description (non-identifying — e.g., "Physical contact incident in dormitory")
- **Victim & Perpetrator Details tab (Role 112, G5 only):**
  - Victim: Name (masked to initials in display — full name stored encrypted), Age, Gender, Class, Student type (Day/Hosteler)
  - Perpetrator: Name, Relationship to victim (student/staff/outsider/unknown), If staff: Employee ID, BGV status
  - Guardian notified: Yes/No, Date, Mode
- **NCPCR Submission tab:**
  - NCPCR Portal Reference Number (if submitted)
  - Submitted By, Submitted Date and Time
  - NCPCR acknowledgement document (download)
  - [Submit to NCPCR] button (opens `ncpcr-submission` modal) — Role 112 only
  - If overdue: red banner with hours overdue
- **Police & Legal tab:**
  - Police Station Name, FIR Number, FIR Date
  - Investigating Officer (if known), Case Number
  - Court proceedings (if any): Case ID, Court, Next Hearing Date
  - [Update Legal Status] button — Role 128 and 112
- **Internal Committee tab:**
  - Committee Convened: Yes/No, Date Convened
  - Committee Members listed
  - Meeting minutes (download)
  - Outcome recommendation (Closure / Further Action / Counselling / Transfer / Termination of perpetrator)
  - [Update Committee Status] — Role 112
- **Documents tab:** All documents: NCPCR submission, Police FIR copy, Internal Committee minutes, Medical examination report, Legal notices. Each: encrypted filename, upload date, uploader, [Download] (audited).
- **Timeline tab:** Immutable audit trail — every action, status change, document access, user, timestamp. Cannot be modified, deleted, or exported without G5 approval.

### 6.2 Modal: `record-incident` (680px)
Used by POCSO Reporting Officer to record a new incident.

| Field | Type | Required | Validation |
|---|---|---|---|
| Incident Date | Date picker | Yes | Cannot be future; alert if > 7 days ago |
| Branch | Select | Yes | |
| Incident Location | Select | Yes | Classroom / Dormitory / Campus / Transport / Off-Campus / Unknown |
| Brief Description | Textarea | Yes | 50–500 chars; non-identifying language only |
| Victim Age Group | Select | Yes | Below 6 / 6–10 / 11–14 / 15–18 |
| Victim Gender | Select | Yes | Female / Male / Other |
| Victim Type | Select | Yes | Day Scholar / Hosteler |
| Perpetrator Type | Select | Yes | Student / Teaching Staff / Non-Teaching Staff / External Person / Unknown |
| Reported By (Branch) | Text | Yes | Name and designation of branch reporter |
| Date Reported to Group | Date | Yes | When Group POCSO Officer was informed |
| Guardian Notified | Toggle | Yes | Yes / No |
| Immediate Action Taken | Textarea | Yes | What was done immediately |

**Footer:** Cancel · Save Incident
**On success:** Incident ID generated; NCPCR 24-hour clock starts; alert banner triggered if on dashboard.

### 6.3 Modal: `ncpcr-submission` (560px)
Used to record NCPCR portal submission.

| Field | Type | Required | Validation |
|---|---|---|---|
| NCPCR Portal Reference | Text | Yes | Alphanumeric, min 5 chars |
| Submitted Date and Time | Datetime picker | Yes | Cannot be before incident date |
| Submitted By | Text | Yes | Name and designation |
| Acknowledgement Document | File upload | No | PDF/image, max 10MB |
| Notes | Textarea | No | Any special circumstances |

**Footer:** Cancel · Confirm NCPCR Submission
**Warning shown if:** Submission time is > 24 hours after incident knowledge: "Warning: This submission is [N] hours after the 24-hour deadline. Record reason in Notes."

---

## 7. Charts

> Charts on POCSO page contain aggregate data only — no individual or identifying information.

### 7.1 Incidents by Year (Bar Chart)

| Property | Value |
|---|---|
| Chart type | Vertical bar (Chart.js 4.x) |
| Title | "POCSO Incidents — Last 5 Financial Years" |
| Data | Count of incidents per FY |
| X-axis | Financial Year |
| Y-axis | Incident count |
| Colour | `#3B82F6` (blue — neutral, non-alarming) |
| Tooltip | "FY [year]: [N] incidents recorded" |
| API endpoint | `GET /api/v1/group/{id}/legal/pocso/incidents-by-year/` |
| HTMX | `hx-get` on load → `hx-target="#chart-pocso-by-year"` → `hx-swap="innerHTML"` |
| Export | PNG (G5 only) |

### 7.2 NCPCR Compliance Rate (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "NCPCR Reporting Compliance — Current FY" |
| Data | Submitted within 24h / Submitted late / Pending |
| Segments | 3 segments |
| Colour | On-time = `#22C55E`, Late = `#F59E0B`, Pending = `#EF4444` |
| Tooltip | "[Segment]: [N] incidents" |
| API endpoint | `GET /api/v1/group/{id}/legal/pocso/ncpcr-compliance/` |
| HTMX | `hx-get` on load → `hx-target="#chart-ncpcr-compliance"` → `hx-swap="innerHTML"` |
| Export | PNG (G5 only) |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Incident recorded | "Incident [INC-YYYY-NNNN] recorded. NCPCR submission required within 24 hours." | Warning | 10s (sticky) |
| NCPCR submission recorded | "NCPCR submission logged for [INC-NNNN]. Reference: [portal-ref]." | Success | 6s |
| NCPCR deadline approaching | "CRITICAL: [INC-NNNN] — NCPCR deadline in [N] hours." | Error | Sticky |
| Document uploaded | "Document uploaded for [INC-NNNN]." | Success | 4s |
| Session expiring | "Session expiring in 2 minutes. Click to extend." | Warning | Persistent until dismissed |
| Unauthorised access attempt | "Access Denied. This incident has restricted access." | Error | 5s |
| Export denied | "Bulk export requires Chairman (G5) approval." | Error | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No incidents this FY | `shield-check` | "No POCSO Incidents This Year" | "No incidents have been recorded in the current financial year." | — |
| No incidents on record at all | `shield` | "No Incidents on Record" | "The POCSO incident registry is empty." | Record Incident (Role 112 only) |
| Filter returns no matches | `search` | "No Matching Incidents" | "No incidents match the selected filters." | Clear Filters |
| NCPCR tab — not yet submitted | `clock` | "NCPCR Submission Pending" | "Click 'Submit to NCPCR' to record the mandatory submission." | Submit to NCPCR |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 6 KPI shimmer cards + 5-row masked table skeleton |
| Table filter | Spinner on table body; rows dimmed |
| Drawer open | Right-slide skeleton — no content shown until fully loaded (security: no partial renders) |
| Chart load | Grey canvas placeholder with centred spinner |
| Document download | Button spinner while download prepares |
| Session extension | Short spinner in session banner |

---

## 11. Role-Based UI Visibility

| Element | POCSO Officer (112, G1) | Compliance Mgr (109, G1) | Legal Dispute (128, G1) | CEO (G4) | Chairman (G5) |
|---|---|---|---|---|---|
| Incident list | Full (masked victim) | Counts only (no list rows) | View only (masked) | View only (masked) | Full (unmasked) |
| [+ Record Incident] button | Visible | Not visible | Not visible | Not visible | Visible |
| Victim details tab in drawer | Visible | Not visible | Not visible | Not visible | Visible |
| NCPCR tab | Full access | Not visible | Not visible | Read-only | Full access |
| Police & Legal tab | Full access | Not visible | Read + Edit | Read-only | Full access |
| Documents tab | Full access | Not visible | Limited (legal docs only) | Read-only | Full access |
| Timeline tab | Read-only | Not visible | Read-only | Read-only | Read-only |
| Export button | Not visible | Not visible | Not visible | Not visible | Visible (G5 only) |
| Charts | Visible | Not visible | Not visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/pocso/` | Role 112, 128, G4+ | Paginated incident list (masked) |
| POST | `/api/v1/group/{id}/legal/pocso/` | Role 112, G5 | Record new incident |
| GET | `/api/v1/group/{id}/legal/pocso/{inc_id}/` | Role 112, 128, G4+ | Incident detail (role-scoped fields) |
| POST | `/api/v1/group/{id}/legal/pocso/{inc_id}/ncpcr-submission/` | Role 112, G5 | Record NCPCR submission |
| PATCH | `/api/v1/group/{id}/legal/pocso/{inc_id}/legal-status/` | Role 112, 128, G4+ | Update police/court status |
| GET | `/api/v1/group/{id}/legal/pocso/kpis/` | Role 112, 109 (counts), G4+ | KPI values |
| GET | `/api/v1/group/{id}/legal/pocso/incidents-by-year/` | Role 112, G4+ | Aggregate yearly chart data |
| GET | `/api/v1/group/{id}/legal/pocso/ncpcr-compliance/` | Role 112, G4+ | NCPCR compliance donut data |
| GET | `/api/v1/group/{id}/legal/pocso/{inc_id}/timeline/` | Role 112, G5 | Immutable access log for one incident |
| POST | `/api/v1/group/{id}/legal/pocso/{inc_id}/documents/` | Role 112, G5 | Upload document |
| GET | `/api/v1/group/{id}/legal/pocso/{inc_id}/documents/{doc_id}/download/` | Role 112, 128, G4+ | Download (audited) |

> All endpoints on `/legal/pocso/` require the following additional security headers:
> - `X-Access-Purpose: [required — describes reason for access]`
> - `X-Session-Verified: true`
> Access without these headers returns HTTP 403.

### Query Parameters for Incident List

| Parameter | Type | Description |
|---|---|---|
| `status` | string | recorded / ncpcr_pending / under_investigation / closed / archived |
| `ncpcr_status` | string | submitted / pending |
| `fir_status` | string | filed / not_filed |
| `branch_id` | integer | Filter to specific branch |
| `fy` | string | Financial year |
| `page` | integer | Default 1 |
| `page_size` | integer | 10 / 25; default 10 (restricted) |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + refresh | `<div id="kpi-bar">` | GET `.../pocso/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 120s"` (shorter interval) |
| Table load | `<tbody id="pocso-table-body">` | GET `.../pocso/` | `#pocso-table-body` | `innerHTML` | `hx-trigger="load"` |
| Filter by status | Status chips | GET `.../pocso/?status={v}` | `#pocso-table-body` | `innerHTML` | `hx-trigger="click"` |
| Filter by branch | Branch dropdown | GET `.../pocso/?branch_id={id}` | `#pocso-table-body` | `innerHTML` | `hx-trigger="change"` |
| Open detail drawer | [View Details] button | GET `.../pocso/{inc_id}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` — access logged server-side |
| Drawer tab: victim details | Tab click | GET `.../pocso/{inc_id}/victim-details/` (Role 112, G5) | `#drawer-tab-content` | `innerHTML` | Lazy-loaded; requires role check on endpoint |
| Drawer tab: NCPCR | Tab click | GET `.../pocso/{inc_id}/ncpcr-tab/` | `#drawer-tab-content` | `innerHTML` | Lazy-loaded |
| Drawer tab: timeline | Tab click | GET `.../pocso/{inc_id}/timeline/` | `#drawer-tab-content` | `innerHTML` | Lazy-loaded |
| Record incident modal | [+ Record Incident] | GET `/htmx/legal/pocso/record-form/` | `#modal-container` | `innerHTML` | Opens modal |
| Submit incident form | Incident form | POST `.../pocso/` | `#pocso-table-body` | `afterbegin` | Prepends new row; triggers NCPCR alert |
| NCPCR submission modal | [Submit to NCPCR] in drawer | GET `/htmx/legal/pocso/{inc_id}/ncpcr-form/` | `#modal-container` | `innerHTML` | Opens modal |
| Submit NCPCR | NCPCR form | POST `.../pocso/{inc_id}/ncpcr-submission/` | `#ncpcr-status-badge-{inc_id}` | `outerHTML` | Updates badge in row and drawer |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
