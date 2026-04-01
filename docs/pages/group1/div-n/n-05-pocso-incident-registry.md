# N-05 — POCSO Incident Registry

**Route:** `GET /legal/pocso/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** POCSO Reporting Officer (#78), Legal Officer (#75)
**No other roles have access. This is the most access-restricted page on the platform.**

---

## Purpose

POCSO Act 2012 (Protection of Children from Sexual Offences) §19 mandates that any person who has knowledge of a POCSO offence must report it to the Special Juvenile Police Unit (SJPU) or local police. Since EduForge is a platform intermediary serving 1,000+ schools and coaching centres — many with minor students — it is a mandatory reporting entity. NCPCR (National Commission for Protection of Child Rights) additionally requires that institutional grievances involving minors be escalated within 24 hours.

At scale: 1,000 schools + 100 coaching centres = 1,100 institutions with guaranteed minor student populations. Unreported or mishandled incidents create criminal liability for EduForge's designated Reporting Officer and senior management under §19 and §21.

This page handles: incident intake, NCPCR submission workflow, police coordination tracking, BGV cross-reference, and case closure. Every field is encrypted at rest. Access logging is mandatory and immutable.

---

## Security Model

- **Encryption at rest:** All `pocso_incident` records encrypted using AWS KMS. `case_notes` and `victim_reference` use separate field-level encryption key (KMS key `pocso-victim-data-key`). Only decrypted on authenticated access by roles #75 and #78.
- **Access logs:** Every view of a POCSO incident record creates an immutable audit entry in `pocso_access_log` (separate table, append-only, no DELETE permission). Logs are retained for 7 years.
- **No caching:** All POCSO data served live from database. No Memcached. `Cache-Control: no-store, no-cache` on all responses.
- **Session scope:** After 15 minutes of inactivity on this page, session redirects to dashboard with "Session expired for data protection" message.
- **Export restriction:** CSV export produces a redacted version (victim reference field always replaced with `[PROTECTED]`). Full unredacted data only accessible via direct DB export by Legal Officer with POCSO Reporting Officer countersignature logged.
- **Print prevention:** `@media print { * { display: none !important; } }` CSS on all POCSO pages.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `pocso_incident` counts by status | No cache — live |
| Incident table | `pocso_incident` JOIN `institution` | No cache — live |
| NCPCR timeline | `pocso_incident` single row: ncpcr fields | No cache — live |
| BGV cross-reference | `bgv_verification` WHERE staff_id = accused_staff_id | No cache — live |
| Incident detail | `pocso_incident` + `pocso_case_note` + `pocso_access_log` | No cache — live |

No caching on any POCSO data. All queries execute against the primary PostgreSQL node.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?status` | `received`, `acknowledged`, `under_investigation`, `submitted_to_ncpcr`, `closed`, `all` | `all` | Filter by incident status |
| `?institution_type` | `school`, `coaching`, `all` | `all` | Filter by institution type |
| `?ncpcr_pending` | `1` | — | Show only incidents where NCPCR submission not yet made and 24h window approaching |
| `?sort` | `date_desc`, `ncpcr_due_asc`, `status` | `ncpcr_due_asc` | Table sort (most urgent first by default) |
| `?page` | integer | `1` | Server-side pagination |
| `?incident_id` | UUID | — | Open specific incident in drawer on load |

No `?export` or `?q` parameters — search/export operations require explicit justification (see below).

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Auto-Refresh | Target ID |
|---|---|---|---|---|
| KPI strip | `?part=kpi` | Page load | 2 min | `#n5-kpi-strip` |
| NCPCR alert strip | `?part=ncpcr_alert` | Page load | 2 min | `#n5-ncpcr-alert` |
| Incident table | `?part=table` | Page load + filter/sort/page change | — | `#n5-incident-table` |

No auto-refresh on incident table — data is sensitive; explicit manual refresh only. Each auto-refresh of KPI/alert strips creates an access log entry.

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  POCSO Incident Registry                          [+ Log Incident] │
│  ⚠ Strictly confidential — all access is logged and audited.      │
├────────────────────────────────────────────────────────────────────┤
│  ⏱ NCPCR DEADLINE ALERT (shown when submission due within 12h)    │
├────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (4 tiles)                                               │
├────────────────────────────────────────────────────────────────────┤
│  FILTER ROW                                                        │
│  INCIDENT TABLE + PAGINATION                                       │
└────────────────────────────────────────────────────────────────────┘
```

---

## Components

### NCPCR Deadline Alert Strip

Shown when any incident has `ncpcr_submitted_at IS NULL AND ncpcr_due_at <= now()+12h`.

```
┌────────────────────────────────────────────────────────────────────┐
│  ⏱  NCPCR SUBMISSION DUE — POCSO-2026-001                         │
│  Institution: Sunrise Academy   Reported to EduForge: 21 Mar 01:14│
│  NCPCR deadline: 22 Mar 01:14 IST   Time remaining: 11h 22m        │
│                                    [Open Incident →]               │
└────────────────────────────────────────────────────────────────────┘
```

Red background with pulsing border if < 4h remaining. Live countdown via JS + HTMX partial (2-min refresh). Multiple incidents with pending NCPCR: most urgent shown, [+N more] expands.

---

### KPI Strip (4 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 2            │ │ 1            │ │ 1            │ │ 14           │
│ Open         │ │ NCPCR        │ │ Police FIR   │ │ Closed (FY)  │
│ Incidents    │ │ Pending      │ │ Awaited      │ │              │
│ (active)     │ │ ⚠ 11h left   │ │              │ │ All resolved │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Tile 1 — Open Incidents:** `COUNT(pocso_incident) WHERE status NOT IN ('CLOSED')`. Red if > 0.

**Tile 2 — NCPCR Pending:** `COUNT(pocso_incident) WHERE ncpcr_submitted_at IS NULL AND status NOT IN ('CLOSED')`. Sub-label shows time until nearest deadline. Red if any < 4h, amber if any < 12h.

**Tile 3 — Police FIR Awaited:** `COUNT(pocso_incident) WHERE police_fir_filed=false AND status NOT IN ('CLOSED')`. Amber if > 0. (Police FIR is not always required — only if EduForge is directly reporting; often institution files the FIR and EduForge tracks.)

**Tile 4 — Closed This FY:** `COUNT(pocso_incident) WHERE status='CLOSED' AND date_reported_to_eduforge >= start_of_current_fy`. Green tile — indicates cases handled and closed.

---

### Filter Row

```
Status: [All ▼]  Institution type: [School ▼]
NCPCR pending: [☐]   Sort: [NCPCR due ↑ ▼]   Showing 2 open incidents

[Export Redacted CSV]  (requires justification — see below)
```

**[Export Redacted CSV]:** Opens justification modal — POCSO Reporting Officer (#78) or Legal Officer (#75) must enter a mandatory justification text (min 20 chars). Justification is logged in `pocso_access_log` with timestamp, actor, IP, and export_type='CSV'. Exported CSV has `victim_reference` always replaced with `[PROTECTED]`.

---

### Incident Table

Minimal columns — victim-identifying information never appears in the table view.

| Column | Description |
|---|---|
| Incident Code | `pocso_incident.incident_code` (e.g. `POCSO-2026-001`) |
| Institution | Name + type badge. No victim/accused names in this column. |
| Date Reported | Date incident was reported to EduForge (`date_reported_to_eduforge`) |
| Nature | SEXUAL_HARASSMENT / INAPPROPRIATE_CONTENT / GROOMING / PHYSICAL_ABUSE / CYBER_EXPLOITATION / OTHER — shown as icon + label |
| NCPCR Deadline | `ncpcr_due_at`. Red if past, amber if < 12h. "Submitted ✓" once logged. |
| Police FIR | "Filed" / "Awaited" / "N/A" |
| Status | RECEIVED / ACKNOWLEDGED / UNDER_INVESTIGATION / SUBMITTED_TO_NCPCR / CLOSED |
| Assigned To | POCSO Reporting Officer avatar + name |
| Actions | [View Full Detail] |

No [Edit] or [Delete] in table — all edits happen within the drawer with mandatory audit trail. No bulk actions.

**[View Full Detail]:** Opens Incident Detail Drawer. Access logged immediately upon drawer open.

---

### Incident Detail Drawer

Full case detail. All fields visible to both Legal Officer (#75) and POCSO Reporting Officer (#78). Tabs:

**Tab 1 — Incident Details**

```
┌──────────────────────────────────────────────────────────────────┐
│  POCSO-2026-001                                     [Close ×]    │
│  Status: UNDER_INVESTIGATION                                     │
├──────────────────────────────────────────────────────────────────┤
│  INCIDENT INFORMATION                                            │
│  Institution: Sunrise Academy (Coaching Centre, Hyderabad)       │
│  Date of incident: 19 Mar 2026 (estimated)                       │
│  Date reported to EduForge: 21 Mar 2026 01:14 IST                │
│  Nature: SEXUAL_HARASSMENT                                       │
│  Accused type: STAFF                                             │
│  Accused BGV ID: BGV-2025-0842 (linked)  [View BGV Record →]    │
│  BGV status at incident: ✓ VERIFIED (cleared 15 Jan 2025)        │
├──────────────────────────────────────────────────────────────────┤
│  VICTIM INFORMATION  ⚠ STRICTLY CONFIDENTIAL                    │
│  Victim reference: [ENCRYPTED — click to view]                   │
│  Victims: 1  ·  All minors: Yes                                  │
│  Victim age range: 14–16 years                                   │
├──────────────────────────────────────────────────────────────────┤
│  NCPCR SUBMISSION                                                │
│  Required: Yes                                                   │
│  Deadline: 22 Mar 2026 01:14 IST  ⏱ 11h 22m remaining           │
│  Submitted: Not yet                    [Log NCPCR Submission]    │
│  NCPCR Reference: —                                              │
├──────────────────────────────────────────────────────────────────┤
│  POLICE COORDINATION                                             │
│  FIR filed by institution: Not confirmed                         │
│  EduForge reporting to police: Required                          │
│  Police station: [SJPU Hyderabad — to be confirmed]              │
│  FIR number: —                         [Log FIR Details]        │
├──────────────────────────────────────────────────────────────────┤
│  SOCIAL WELFARE                                                  │
│  Child welfare committee (CWC) contacted: No                     │
│  CWC district: Hyderabad                                         │
│                                [Log CWC Contact]                 │
├──────────────────────────────────────────────────────────────────┤
│  [Update Status]  [Close Case]  (requires resolution criteria)   │
└──────────────────────────────────────────────────────────────────┘
```

**[View victim reference]:** Requires re-authentication (password confirmation). Decrypts `victim_reference` field inline. Access logged with `decryption_access=true` flag.

**[Log NCPCR Submission]:** Modal — enter NCPCR submission method (online portal / email / physical), reference number, submission timestamp. Updates `ncpcr_submitted_at`, `ncpcr_reference`.

**[Log FIR Details]:** Modal — enter FIR number, police station, filed by (institution / EduForge), filed date, copy attached (file upload). Updates `police_fir_filed=true`, `police_fir_number`.

**[Log CWC Contact]:** Modal — enter CWC district, contact person, date contacted, case number assigned. Updates `social_welfare_contacted=true`.

**[Update Status]:** Dropdown of valid status transitions. Each transition requires a brief mandatory note.

**[Close Case]:** Available when: (1) NCPCR submitted, (2) police coordination documented, (3) at least one case note with closing summary. Opens Close Case Modal. Sets `status='CLOSED'`, `closed_at=now()`.

**Tab 2 — Case Notes**

Chronological log of all internal case notes. Add note field at bottom.

```
  21 Mar 2026 02:30 IST — Priya R. (POCSO Officer)
  "Incident reported via phone by institution coordinator Ramesh.
   Institutional management has been informed. Accused has been
   suspended pending investigation."

  21 Mar 2026 09:00 IST — Arjun M. (Legal Officer)
  "Legal team reviewed. NCPCR submission to proceed today."
  [View all notes...]
```

New note: min 20 chars. All notes are immutable once saved.

**Tab 3 — Access Log**

Immutable log of every access to this incident record.

| Time | User | Role | Action | IP |
|---|---|---|---|---|
| 21 Mar 2026 02:15 IST | Priya R. | POCSO Officer | Opened detail drawer | 103.xx.xx.xx |
| 21 Mar 2026 09:00 IST | Arjun M. | Legal Officer | Opened detail drawer | 103.xx.xx.xx |
| 21 Mar 2026 09:15 IST | Priya R. | POCSO Officer | Viewed victim reference | 103.xx.xx.xx |

Cannot be deleted or exported by any in-app user.

---

### Log New Incident Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Log New POCSO Incident                                          │
│  ⚠ All information entered here is strictly confidential        │
│    and encrypted. Access is logged.                              │
├──────────────────────────────────────────────────────────────────┤
│  Institution*   [Search institution (schools + coaching only)  ] │
│  Date of incident*  [___ / ___ / _____]  (approximate if unknown)│
│  Date reported to EduForge*  [___ / ___ / _____]  (today)       │
│  Nature*  [Sexual Harassment                              ▼]     │
│  Accused type*  ● Staff  ● External person  ● Unknown           │
│  If Staff — BGV ID  [Search staff BGV record...           ]      │
│  [+ Add another accused]  (supports multiple accused)            │
│  Victim count*  [                ]  ·  All minors? ● Yes ● No   │
│  Victim age range  [___] to [___] years                         │
│  Victim reference (code/initials only)*  [                ]     │
│    (Do NOT enter full name — use anonymised reference code)      │
│  Report received via*  ● Phone  ● Email  ● In person  ● Portal  │
│  Initial incident description*  [                               │
│                                                                  │
│                                                                 ]│
│                                                                  │
│  NCPCR submission required: ● Yes  ○ No  ○ Confirm with Legal   │
│  NCPCR deadline: [computed — date_reported + 24 hours]          │
│                                                                  │
│  [Cancel]                              [Log Incident]            │
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Institution: required; includes **schools, coaching centres, AND intermediate colleges** (colleges have students aged 16–18 who are legal minors under POCSO Act). Groups are excluded (not direct institutions).
- Date of incident: required; cannot be in the future
- Date reported: required; cannot be before date of incident; defaults to today
- Nature: required
- Accused type: required
- BGV ID: required if accused_type = STAFF for the **primary** accused; each additional accused added via [+ Add another accused] also requires a BGV ID if staff. Stored in `pocso_incident_accused` child table (incident_id, accused_type, bgv_id, accused_order)
- Victim count: required; integer ≥ 1
- Victim reference: required; min 2 chars, max 20 chars; no email addresses or full names allowed (server-side regex validation)
- Initial description: required; min 50 chars
- NCPCR required: defaults to Yes if nature involves direct harm (SEXUAL_HARASSMENT / GROOMING / PHYSICAL_ABUSE / CYBER_EXPLOITATION)

POST to `/legal/pocso/incidents/create/`. On creation:
1. Sets `status='RECEIVED'`, `ncpcr_due_at = date_reported_to_eduforge + 24 hours`
2. Immediately sends encrypted email notification to Legal Officer (#75)
3. Creates `legal_compliance_deadline` entry for NCPCR deadline in N-07 calendar
4. Creates initial access log entry for creator

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| NCPCR alert strip | No pending NCPCR submissions | Not shown — section hidden entirely |
| Incident table | No open incidents | "No open POCSO incidents. All cases resolved." with green checkmark |
| Incident table (all time empty) | No incidents ever | "No incidents recorded." — with reassuring but not dismissive tone |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Incident created | "POCSO-[code] logged. NCPCR deadline: [ncpcr_due_at]." | Amber (sensitive) |
| NCPCR submission logged | "NCPCR submission recorded. Reference: [ref]." | Green |
| FIR details logged | "Police FIR details recorded." | Green |
| Case status updated | "Status updated to [new_status]." | Blue |
| Case closed | "POCSO-[code] closed." | Green |
| Victim reference accessed | "Access to victim data logged for compliance." | Amber (awareness) |

---

## Authorization

**Route guard:** `@pocso_restricted(allowed_roles=[75, 78])` applied to all POCSO views.

```python
# Strictest authorization check in the codebase
@require_http_methods(["GET", "POST"])
@pocso_restricted(allowed_roles=[75, 78])
@require_active_session(max_idle_minutes=15)
@log_access_on_entry(log_table='pocso_access_log')
def pocso_incident_view(request):
    ...
```

| Scenario | Behaviour |
|---|---|
| Unauthenticated | Redirect to `/login/?next=/legal/pocso/` |
| Any role NOT #75 or #78 | 403 — no information leakage in error message ("You do not have access to this page.") |
| Session idle > 15 minutes | Force re-login; log "session_timeout" in pocso_access_log |
| HTMX part requests without session | 403 |
| Direct URL access to drawer data (`/legal/pocso/incidents/{id}/`) | 403 for any non-allowed role; 200 with access log for allowed roles |
| Django admin panel | POCSO models explicitly excluded from admin via `@admin.register(..., site=pocso_admin_site)` — separate admin site requiring separate authentication |

No other roles may view any POCSO data under any circumstances. No "view own cases" exception — all incidents accessible to both #75 and #78.

---

## Role-Based UI Visibility Summary

| Element | 75 Legal Officer | 78 POCSO Officer | All other roles |
|---|---|---|---|
| Page access | Yes | Yes | 403 |
| Log new incident | No | Yes | 403 |
| View incident list | Yes | Yes | 403 |
| View incident detail | Yes | Yes | 403 |
| View victim reference (re-auth) | Yes | Yes | 403 |
| Log NCPCR submission | No | Yes | 403 |
| Log FIR details | No | Yes | 403 |
| Update status | No | Yes | 403 |
| Add case notes | Yes | Yes | 403 |
| Close case | No | Yes | 403 |
| Access log (tab 3) | Yes (read) | Yes (read) | 403 |
| Export redacted CSV | Yes | Yes | 403 |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Page load | < 1.5s P95 | Low volume (typically < 50 open incidents) |
| NCPCR alert strip (2 min auto-refresh) | < 300ms | Direct DB query, no cache |
| Incident detail drawer | < 500ms | Single row fetch; KMS decrypt adds ~100ms |
| Victim reference decrypt | < 200ms | KMS API call; separate key |

---

## NCPCR Annual Compliance Reporting

At the end of each financial year, the POCSO Reporting Officer (#78) can generate an annual report of all incidents for the FY from this page:

**[Generate Annual NCPCR Report]** button (visible to #78 only, appears after 1 April each year):
- Generates a structured report: total incidents by nature, by institution type, NCPCR submission compliance rate, outcomes (cases closed, FIRs filed, child welfare interventions)
- Produces a PDF formatted per NCPCR reporting template
- Victim counts only — no individual victim data
- Legal Officer (#75) must counter-approve before report is finalized
- Report stored in N-06 Document Repository under `document_type='ANNUAL_POCSO_REPORT'`

---

## POCSO Backup Officer Designation

**Operational need:** If the primary POCSO Reporting Officer (#78) is unavailable (leave, illness, resignation) during an active NCPCR deadline window, the 24-hour clock continues. A designated backup must be able to act immediately.

**Configuration:** Legal Officer (#75) manages the backup officer designation via the Settings panel within N-05. Accessible via **[Settings ⚙]** button in the page header. Route: `GET /legal/pocso/?tab=settings`. Opens a dedicated settings drawer (not a full page). POST to `/legal/pocso/backup-officer/designate/` to save changes.

```
┌────────────────────────────────────────────────────────────────────┐
│  POCSO Officer Designation                         [Settings]      │
├────────────────────────────────────────────────────────────────────┤
│  Primary POCSO Reporting Officer: Priya R. (#78)                  │
│  Backup Officer: [Not designated]   [+ Designate Backup]          │
│                                                                    │
│  Escalation rule: If primary has no login activity for > 4 hours  │
│  during an active NCPCR deadline window → auto-escalate to backup  │
│  + send alert to Legal Officer.                                    │
└────────────────────────────────────────────────────────────────────┘
```

**Backup Officer access:**
- Must be an EduForge employee with Level 1+ access
- Granted temporary POCSO page access by Legal Officer from this panel
- Access is role-scoped: backup can only view/edit incidents assigned to primary #78 if primary is inactive
- Access automatically revoked when primary #78 logs back in (with 30-min grace period)
- All access logged in `pocso_access_log` with `is_backup_access=true` flag

**[+ Designate Backup] modal (Legal Officer only):**
- Search EduForge staff: name/email
- Select staff member
- Confirm: "This grants [name] temporary POCSO page access when primary officer is unavailable."
- Creates `pocso_backup_officer` record: `user_id`, `designated_by`, `designated_at`

**Task N-5 extension — Backup Activation Monitor (every 30 minutes when NCPCR deadline active):**
- Checks: any `pocso_incident WHERE ncpcr_submitted_at IS NULL AND ncpcr_due_at <= today+12h`
- AND primary officer #78 has `last_login_at < now() - 4h`
- → Sends emergency alert to backup officer + Legal Officer (#75) + CEO (#1)
- Alert: "POCSO Reporting Officer unavailable. NCPCR deadline approaching: POCSO-[code] due [time]. Backup officer [name] must act immediately."
- Does NOT auto-grant access — backup must be explicitly activated by Legal Officer

---

## FIR Document Upload Specification

When logging FIR details via [Log FIR Details] modal:

**File upload requirements:**
- Accepted formats: PDF, JPEG, PNG, TIFF
- Maximum size: 10 MB per file (police FIRs are typically scanned PDFs)
- Validation: PDF must be parseable; images must decode without error

**Error handling:**
| Error | User Message | System Action |
|---|---|---|
| Invalid format (e.g., .docx) | "File must be PDF or image (JPG/PNG/TIFF). Please upload a valid police FIR copy." | Reject; no upload |
| Corrupted PDF | "PDF could not be read. Please re-upload a clear, uncorrupted copy." | Reject; no upload |
| File too large (> 10MB) | "File exceeds 10MB. Please compress or scan at lower resolution." | Reject; no upload |
| Upload timeout (S3 slow) | "Upload failed. Check your connection and retry." | Retry once; if still fails, toast persists |

**On successful upload:**
- File stored in S3: `s3://eduforge-legal-secure/pocso/{incident_code}/fir_{timestamp}.pdf`
- Server-side encryption: KMS key `pocso-victim-data-key` (same key as victim data)
- File is **immutable** once uploaded: no overwrite or delete permitted in-app
- To correct an error: add a new note in Case Notes explaining the error; upload correct file as second attachment
- Audit log entry: `"FIR document uploaded by [user] at [time] from IP [ip]. File: fir_{timestamp}.pdf"`

---

## Keyboard Shortcuts (N-05)

| Key | Action |
|---|---|
| `g` `l` | Go to Legal Dashboard (N-01) |
| `g` `p` | Go to POCSO Registry (this page) |
| `n` | Open Log New Incident modal (POCSO Officer #78 only) |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |

> Note: No search shortcuts — N-05 deliberately omits free-text search (see Security Model). Keyboard navigation is intentionally limited.

---

## Integration with BGV (Division G)

When an incident is logged with `accused_type='STAFF'` and a BGV ID is linked:

1. The BGV record `bgv_verification.status` is automatically flagged to `FLAGGED_POCSO` via an internal API call to `/bgv/flag/`
2. The BGV Operations Supervisor (#92) receives a notification: "Staff member BGV-[id] has been linked to a POCSO incident. Access requires coordination with Legal."
3. The flagged BGV record cannot be approved by any BGV role until the POCSO case is closed and Legal Officer (#75) sends a clearance via `/legal/pocso/bgv-clearance/`
4. If the accused staff member is currently active on the EduForge platform (has user account), Platform Admin (#10) receives an automated alert to review access — no automatic suspension (that requires separate instruction from Legal Officer to avoid procedural liability)
