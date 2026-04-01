# N-04 — Regulatory Filings

**Route:** `GET /legal/filings/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Regulatory Affairs Exec (#77), Legal Officer (#75)
**Also sees:** DPO (#76) — CERT-In and DPDP filings only; Security Engineer (#16) — CERT-In incident reports (creates); Platform Admin (#10) — read-only on TRAI/MeitY tabs

---

## Purpose

EduForge operates under multiple regulatory frameworks simultaneously. The SMS sender ID `EDUFGE` must be maintained on TRAI's DLT platform (lapse = all OTPs and notification SMSs fail for 2,050 institutions). Cybersecurity incidents must be reported to CERT-In within 6 hours. The Intermediary Liability framework under IT Act §79 requires annual compliance certification and grievance officer maintenance. MeitY's IT rules require monthly content moderation reports. This page tracks all filings across authorities, manages documents, and ensures no deadline is missed. At scale, a missed TRAI DLT renewal causes platform-wide OTP failure for ~7.6M students; a missed CERT-In report carries ₹5 lakh penalty and criminal liability for responsible person.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `regulatory_filing` aggregated by status + overdue count | 5 min |
| Filing table | `regulatory_filing` JOIN `user` (submitted_by) | 5 min |
| Filing calendar | `regulatory_filing` WHERE due_date <= today+90d | 10 min |
| Authority summary tiles | `regulatory_filing` GROUP BY authority | 30 min |
| Document list (per filing) | `regulatory_filing_document` WHERE filing_id = ? | no cache |
| Filing detail | `regulatory_filing` single row JOIN audit log | no cache |
| Overdue/critical strip | `regulatory_filing` WHERE status='OVERDUE' OR (status IN ('UPCOMING','IN_PROGRESS') AND due_date <= today+7d) | 2 min |

Cache keys scoped to `(user_id, authority, filters)`. `?nocache=true` for Regulatory Affairs Exec (#77) and Legal Officer (#75).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?authority` | `trai`, `cert_in`, `meity`, `state_board`, `other`, `all` | `all` | Filter by regulatory authority |
| `?status` | `upcoming`, `in_progress`, `submitted`, `acknowledged`, `overdue`, `all` | `all` | Filter by filing status |
| `?period` | `this_year`, `last_year`, `all` | `this_year` | Reporting period filter |
| `?q` | string | — | Search filing title, reference number |
| `?sort` | `due_date_asc`, `due_date_desc`, `authority`, `status` | `due_date_asc` | Table sort |
| `?page` | integer | `1` | Server-side pagination |
| `?filing_id` | UUID | — | Open a specific filing in the detail drawer on load |
| `?export` | `csv` | — | Export filing list (Reg. Affairs Exec + Legal Officer) |
| `?nocache` | `true` | — | Bypass Memcached (Reg. Affairs Exec + Legal Officer only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Auto-Refresh | Target ID |
|---|---|---|---|---|
| KPI strip | `?part=kpi` | Page load | 5 min | `#n4-kpi-strip` |
| Critical/overdue strip | `?part=critical_strip` | Page load | 2 min | `#n4-critical-strip` |
| Authority summary tiles | `?part=authority_tiles` | Page load | 30 min | `#n4-authority-tiles` |
| Filing table | `?part=table` | Page load + filter/sort/page change | — | `#n4-filing-table` |
| Filing calendar | `?part=calendar` | Tab=calendar + period change | 10 min | `#n4-calendar` |

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Regulatory Filings   [Search filings... 🔍]    [+ New Filing]    │
├────────────────────────────────────────────────────────────────────┤
│  ⚠ CRITICAL/OVERDUE STRIP (shown only when urgent items exist)    │
├────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (4 tiles)                                               │
├────────────────────────────────────────────────────────────────────┤
│  AUTHORITY SUMMARY TILES (TRAI | CERT-In | MeitY | Other)         │
├────────────────────────────────────────────────────────────────────┤
│  [Table View] [Calendar View]                                      │
│                                                                    │
│  FILTER ROW                                                        │
│  FILING TABLE + PAGINATION  (or FILING CALENDAR)                  │
└────────────────────────────────────────────────────────────────────┘
```

---

## Components

### Critical/Overdue Strip

Shown only when `regulatory_filing` has rows where `status='OVERDUE'` OR `due_date <= today+3d`.

```
┌────────────────────────────────────────────────────────────────────┐
│  ⚠  3 filings require immediate attention:                        │
│  CERT-In #INC-2026-003 (due in 4h) · TRAI DLT renewal (due in 2d) │
│  · MeitY monthly report Jan 2026 (OVERDUE — 3 days)               │
│                              [View All Critical →]                 │
└────────────────────────────────────────────────────────────────────┘
```

Red background for OVERDUE items, amber for < 24h, yellow for < 3 days. Auto-refresh every 2 minutes.

---

### KPI Strip (4 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 24           │ │ 3            │ │ 0            │ │ 18           │
│ Filings This │ │ Due ≤ 7 Days │ │ OVERDUE      │ │ Submitted &  │
│ Year         │ │              │ │              │ │ Acknowledged │
│ 18 ack'd     │ │ ⚠ Act now    │ │ ✓ All clear  │ │ 75% rate     │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Tile 1 — Filings This Year:** `COUNT(regulatory_filing) WHERE YEAR(due_date) = current_year`. Sub-label: "N acknowledged". Clicking → `?period=this_year`.

**Tile 2 — Due ≤ 7 Days:** `COUNT(regulatory_filing) WHERE status IN ('UPCOMING','IN_PROGRESS') AND due_date <= today+7d`. Sub-label "⚠ Act now" if > 0. Amber if 1–3, red if > 3. Clicking → `?status=upcoming&sort=due_date_asc`.

**Tile 3 — Overdue:** `COUNT(regulatory_filing) WHERE status='OVERDUE'`. "✓ All clear" green if 0. Pulsing red if > 0. Clicking → `?status=overdue`.

**Tile 4 — Acknowledged Rate:** `COUNT(ACKNOWLEDGED) / COUNT(SUBMITTED + ACKNOWLEDGED) × 100` for this year. Green if ≥ 90%, amber if 70–89%, red if < 70%.

---

### Authority Summary Tiles

Four tiles — one per major regulatory authority.

```
┌─────────────────────┐  ┌─────────────────────┐
│  TRAI               │  │  CERT-In             │
│  DLT Registration ✓ │  │  2 incidents filed   │
│  Sender ID: EDUFGE  │  │  Last: BRN-2026-001  │
│  Renewal: 1 Nov 26  │  │  (pending ack.)      │
│  [View filings →]   │  │  [View filings →]    │
└─────────────────────┘  └─────────────────────┘
┌─────────────────────┐  ┌─────────────────────┐
│  MeitY              │  │  State Boards / Other│
│  IT Rules compliant │  │  3 filings           │
│  Annual report: ✓   │  │  Next: AP Board      │
│  Monthly: Jan ⚠     │  │  due: 30 Apr 2026    │
│  [View filings →]   │  │  [View filings →]    │
└─────────────────────┘  └─────────────────────┘
```

Each tile shows the most critical status for that authority. [View filings →] filters table to that authority.

**TRAI tile detail:**
- Entity registration status: ACTIVE / PENDING_RENEWAL
- Sender ID `EDUFGE`: active/suspended
- Last DLT renewal date
- Next renewal due date
- Template registrations: count ACTIVE / PENDING / REJECTED

**CERT-In tile detail:**
- Total incidents reported this FY
- Latest incident reference + status
- Annual cybersecurity compliance report: filed / due date

**MeitY tile detail:**
- Intermediary compliance certification: current year filed / due
- Monthly content moderation reports: which months filed, which pending
- Grievance Officer designation: current officer + appointment date (required under IT Rules 2021)

**Other tile:**
- State education board filings: upcoming count
- Any other authority filings

---

### Filter Row

```
Authority: [All ▼]  Status: [All ▼]  Period: [This Year ▼]
[Search reference or title...]    [Apply]   [Clear]
Sort: [Due date ↑ ▼]   Showing 24 filings   [Export CSV]
```

---

### Filing Table

Sortable, selectable, server-side paginated (25 per page).

| Column | Description |
|---|---|
| Filing ID | `regulatory_filing.reference` (e.g. `TRAI-2026-001`, `CERT-2026-003`) |
| Authority | TRAI / CERT-In / MeitY / STATE_BOARD / OTHER — with authority logo icon |
| Filing Type | SMS_SENDER_ID_RENEWAL / DLT_TEMPLATE_REG / CERT_IN_INCIDENT_REPORT / MEITY_ANNUAL / MEITY_MONTHLY / INTERMEDIARY_COMPLIANCE / OTHER |
| Subject / Period | Brief description or period label (e.g. "FY 2025-26", "Jan 2026") |
| Due Date | Date. Red if OVERDUE, amber if ≤ 7 days, green otherwise |
| Status | UPCOMING (grey) / IN_PROGRESS (blue) / SUBMITTED (teal) / ACKNOWLEDGED (green) / OVERDUE (red) |
| Submitted At | Date or "Not yet" |
| Reference # | Authority-issued reference number (after submission) or "Pending" |
| Submitted By | Avatar + name |
| Documents | Count of attached documents (e.g. "3 files") |
| Actions | [View] [Update Status] [Attach Document] |

**OVERDUE row:** red-50 background, pulsing red left border.
**SUBMITTED (awaiting ack) row:** teal-50 background.

**[View]:** Opens Filing Detail Drawer.
**[Update Status]:** Opens Status Update Modal. Available to Regulatory Affairs Exec (#77) and Legal Officer (#75).
**[Attach Document]:** Opens file upload. Accepts PDF/DOCX/XLSX; max 20MB per file.

---

### Filing Detail Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  TRAI-2026-001  ·  TRAI DLT Entity Renewal 2026-27  [Close ×]   │
├──────────────────────────────────────────────────────────────────┤
│  Authority: TRAI                    Status: UPCOMING              │
│  Filing type: SMS_SENDER_ID_RENEWAL                              │
│  Period: FY 2026-27                                              │
│  Due date: 1 Nov 2026 (in 225 days)                              │
│  Submitted at: —                                                 │
│  Reference #: —                                                  │
├──────────────────────────────────────────────────────────────────┤
│  Description:                                                    │
│  Annual renewal of DLT entity registration for sender ID         │
│  EDUFGE on TRAI's DLT platform (Vodafone). Renewal window       │
│  opens 60 days before expiry. Lapse causes SMS delivery         │
│  failure for all OTPs and exam notifications.                    │
├──────────────────────────────────────────────────────────────────┤
│  Checklist                                                       │
│  ☐ Gather company registration documents                        │
│  ☐ Prepare board resolution (if required by operator)           │
│  ☐ Submit application on DLT portal (vi.in/bsn.in)             │
│  ☐ Pay renewal fee                                              │
│  ☐ Record acknowledgment reference                              │
├──────────────────────────────────────────────────────────────────┤
│  Documents (0 attached)                                          │
│  [Attach Document]                                               │
├──────────────────────────────────────────────────────────────────┤
│  Notes: [Add internal note...                            ]       │
│                                                                  │
│  [Mark In Progress]  [Mark Submitted]  [Mark Acknowledged]       │
└──────────────────────────────────────────────────────────────────┘
```

**Tabs:**
1. **Details** (default): As above
2. **Documents:** List of all attached documents with download links
3. **Audit Log:** All status changes, document uploads, notes with actor + timestamp

**Status transition buttons:**
- [Mark In Progress]: Sets `status='IN_PROGRESS'`
- [Mark Submitted]: Opens modal to capture submission timestamp + reference number
- [Mark Acknowledged]: Opens modal to capture acknowledgment timestamp + authority reference

---

### New Filing Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Create New Regulatory Filing                                    │
├──────────────────────────────────────────────────────────────────┤
│  Authority*  [TRAI                                        ▼]     │
│  Filing type*  [SMS Sender ID Renewal                     ▼]     │
│  Period / Subject*  [FY 2026-27                          ]       │
│  Due date*  [___ / ___ / _____]                                  │
│  Recurrence  [Annual                                      ▼]     │
│    → None / Monthly / Quarterly / Annual                         │
│  Description*  [                                                 │
│                                                                  ]│
│  Checklist items  [Add checklist item...         [+ Add item]]   │
│  Assign to*  [Priya R. (Reg. Affairs Exec)        ▼]             │
│                                                                  │
│  [Cancel]                              [Create Filing]           │
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Authority: required
- Filing type: required
- Period/Subject: required; min 3 chars
- Due date: required; cannot be more than 30 days in the past
- Description: required; min 20 chars

POST to `/legal/filings/create/`. Creates `regulatory_filing` record with `status='UPCOMING'`.

**MeitY monthly content moderation report — data source:** Content moderation actions from the platform's content review system: count of items reported, removed, withheld per month. Data sourced from `platform_content_report` table (owned by Platform Admin #10 / Engineering). Regulatory Affairs Exec (#77) exports the monthly aggregates and attaches as PDF/XLSX to the MeitY filing record. No real-time pull — monthly Celery task aggregates data by 1st of each month.

**Real-time vs submit-time validation (New Filing modal):** Due date format (on change). Required fields + past-date check at submit-time.
**Unsaved changes warning:** On modal close with fields modified: "You have unsaved changes. Discard them?" [Cancel] [Discard]. If recurrence ≠ NONE, sets `next_due_date` computation rule (stored as `recurrence_days_offset`). Creates `legal_compliance_deadline` entry visible in N-07.

---

### Calendar View

Monthly calendar showing filing due dates.

```
         MARCH 2026
  Mon  Tue  Wed  Thu  Fri  Sat  Sun
   ...
  16   17   18   19   20   21   22
                           ⚠CERT
  23   24   25   26   27   28   29
       TRAI
  30   31
  MEITY
```

- Each filing shown as a coloured dot/badge on its due date: TRAI (blue) · CERT-In (red) · MeitY (purple) · Other (grey)
- Clicking a filing badge opens the Filing Detail Drawer
- Colour-coding reflects urgency: overdue = red pill, today/tomorrow = amber pill, normal = authority colour
- Navigation: [< Previous] [Month label] [Next >]

---

## TRAI DLT Template Registry

Sub-section below the filing table (collapsible), accessible via [TRAI DLT Templates] tab. Shows all SMS templates registered on DLT platform:

| Template ID | Template Name | Category | Status | Registered | Use Case |
|---|---|---|---|---|---|
| DLT-TMP-001 | OTP Delivery | TRANSACTIONAL | ACTIVE | 12 Jan 2024 | User login OTP |
| DLT-TMP-002 | Exam Reminder | PROMOTIONAL | ACTIVE | 12 Jan 2024 | Exam schedule notification |
| DLT-TMP-003 | Result Notification | TRANSACTIONAL | ACTIVE | 12 Jan 2024 | Result publication SMS |
| DLT-TMP-004 | Invoice Due | TRANSACTIONAL | PENDING | 10 Mar 2026 | Billing reminder |

Templates with `status='REJECTED'` shown in red; `status='PENDING'` in amber. [+ Register Template] for Regulatory Affairs Exec.

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| Critical strip | No urgent filings | Not shown — section hidden entirely |
| Filing table | No filings match filters | "No filings found." with [Clear Filters] |
| Filing table (no filings at all) | Fresh system | "No regulatory filings created yet." with [+ New Filing] button |
| TRAI template registry | No templates | "No DLT templates registered." with [+ Register Template] |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Filing created | "Filing [ref] created. Due: [due_date]." | Blue |
| Status → In Progress | "Filing [ref] marked as In Progress." | Blue |
| Status → Submitted | "Filing [ref] marked as Submitted. Reference: [ref]." | Green |
| Status → Acknowledged | "Filing [ref] acknowledged by [authority]." | Green |
| Document attached | "Document [filename] attached to [filing_ref]." | Blue |
| Overdue alert (auto-triggered) | "⚠ Filing [ref] is now OVERDUE." | Red |

---

## Authorization

**Route guard:** `@division_n_required(allowed_roles=[75, 76, 77, 16, 10])` with authority-level restrictions.

| Scenario | Behaviour |
|---|---|
| DPO (#76) | Can only view/interact with CERT-In authority filings and any filing with `dpdp_related=true` flag |
| Security Engineer (#16) | Can only view CERT-In incident reports; can trigger new CERT-In report from N-03 breach workflow |
| Platform Admin (#10) | Read-only on TRAI and MeitY tabs; cannot create or update filings |
| Create / Update Status | Regulatory Affairs Exec (#77) and Legal Officer (#75) |

---

## Role-Based UI Visibility Summary

| Element | 75 Legal | 76 DPO | 77 Reg. Affairs | 16 Security | 10 Platform Admin |
|---|---|---|---|---|---|
| All filings (full table) | Yes | CERT-In + DPDP only | Yes | CERT-In only | Yes (read) |
| Create new filing | Yes | No | Yes | No | No |
| Update filing status | Yes | CERT-In only | Yes | No | No |
| Attach document | Yes | CERT-In only | Yes | No | No |
| TRAI DLT template registry | Yes (read) | No | Yes (full) | No | Yes (read) |
| Calendar view | Yes | Yes (filtered) | Yes | No | Yes |
| Export CSV | Yes | No | Yes | No | No |
| [?nocache=true] | Yes | No | Yes | No | No |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Filing table (paginated, 25 rows) | < 500ms P95 | Low volume (~50–200 filings total) |
| Critical strip auto-refresh | < 300ms (2 min TTL) | Must be fast during breach scenarios |
| Calendar view generation | < 800ms P95 | Aggregates ~12 months of filings |

---

## Background Tasks

**Task N-6 — Filing Deadline Monitor (daily, 07:00 IST):**
- Sets `status='OVERDUE'` for filings where `status IN ('UPCOMING','IN_PROGRESS') AND due_date < today`
- Sends daily email to Regulatory Affairs Exec (#77) and Legal Officer (#75) listing all upcoming (< 14 days) and overdue filings
- Creates `legal_compliance_deadline` entry for N-07 calendar

**Task N-7 — TRAI DLT Status Sync (weekly, Sunday 06:00 IST):**
- Checks DLT template statuses via TRAI operator API (if available) or flags for manual review
- Updates `dpdp_dlt_template.status` accordingly
- Alerts Regulatory Affairs Exec on REJECTED or SUSPENDED templates

---

## MeitY Grievance Officer Management

**Regulatory basis:** IT Rules 2021 §4(1)(b) requires every intermediary with > 5 million users to designate a Grievance Officer whose name and contact must be published on the platform and be reachable for complaint resolution within 24 hours of receipt.

EduForge qualifies as an intermediary with > 5 million users (7.6M students). Failure to maintain a current, published Grievance Officer causes loss of safe harbour protection under IT Act §79 — making EduForge liable for user-generated content and third-party data on the platform.

**Configuration section** (within N-04 page, accessible via MeitY authority tile → [Manage Officer] link):

```
┌────────────────────────────────────────────────────────────────────┐
│  MeitY Grievance Officer — IT Rules 2021 §4(1)(b)                 │
├────────────────────────────────────────────────────────────────────┤
│  Primary Officer                                                   │
│  Name: Arjun Mehta (Legal Officer)                                │
│  Designation: Legal Officer                                       │
│  Email: grievance-officer@eduforge.in                             │
│  Phone: +91-XXXXX-XXXXX                                           │
│  Appointed: 1 Jan 2026                                            │
│                                                                    │
│  Backup Officer (if primary unavailable > 24h)                    │
│  Name: —                          [+ Designate Backup]            │
│                                                                    │
│  Published on: /grievance-officer  (platform public page)         │
│  Last reviewed: 1 Jan 2026                                        │
│                                                                    │
│  [Update Officer]  (Legal Officer #75 + Reg. Affairs Exec #77)    │
└────────────────────────────────────────────────────────────────────┘
```

**[Update Officer] modal:**
- Current officer name* (required)
- Designation* (required)
- Contact email* (required; must be `@eduforge.in` domain)
- Contact phone* (required)
- Appointment date* (required; defaults to today)
- Backup officer name (optional)
- Effective from (date — can be future for planned transitions)

**On update:**
1. `meity_grievance_officer` table updated (`officer_name`, `email`, `phone`, `appointed_at`, `effective_from`)
2. Platform's public `/grievance-officer` page auto-updated (reads from this table)
3. Audit log entry created: who changed, previous officer, new officer, timestamp
4. Celery task enqueued to re-publish updated officer contact to platform
5. N-07 compliance calendar: annual review deadline updated ("Grievance Officer annual review — [next year]")

**Compliance check (Task N-6 extension):** If `meity_grievance_officer.appointed_at < today-365d`, creates N-07 deadline "Annual Grievance Officer review due" in REGULATORY category and emails Regulatory Affairs Exec.

**Grievance complaint tracking:** Complaints received at `grievance-officer@eduforge.in` must be acknowledged within 24 hours (IT Rules 2021 §4(1)(c)). Tracking via a lightweight `meity_grievance_complaint` table:
- complaint_id, received_at, sender_email, nature, status (OPEN/ACKNOWLEDGED/RESOLVED), resolved_at, resolution_notes
- N-04 filing strip shows count of open grievance complaints as a sub-indicator on the MeitY tile

**Keyboard shortcuts (N-04):**

| Key | Action |
|---|---|
| `g` `l` | Go to Legal Dashboard (N-01) |
| `g` `r` | Go to Regulatory Filings (this page) |
| `1` | Switch to Table View |
| `2` | Switch to Calendar View |
| `n` | Open New Filing modal |
| `/` | Focus search input |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |
