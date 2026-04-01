# G-04 — Institution Compliance Tracker

> **Route:** `/bgv/institutions/`
> **Division:** G — Background Verification
> **Primary Role:** BGV Manager (39) — full control; BGV Ops Supervisor (92) — full
> **Supporting Roles:** POCSO Compliance Officer (41) — read-only; Platform Admin (10) — full
> **File:** `g-04-institution-compliance-tracker.md`
> **Priority:** P1 — escalation and compliance oversight

---

## 1. Page Name & Route

**Page Name:** Institution Compliance Tracker
**Route:** `/bgv/institutions/`
**Part-load routes:**
- `/bgv/institutions/?part=table` — institution list table
- `/bgv/institutions/{institution_id}/?part=drawer` — institution detail drawer
- `/bgv/institutions/?part=summary-bar` — summary bar

---

## 2. Purpose

G-04 gives BGV Manager and Supervisor a complete view of BGV compliance status across all 1,900+ institutions. It is the primary tool for identifying non-compliant institutions, managing escalation, tracking communication history, and drilling into per-institution staff BGV status.

**Who needs this page:**
- BGV Manager (39) — escalation decisions, institution communication, compliance reporting
- BGV Ops Supervisor (92) — monitors where staff verifications are stuck at institution level
- POCSO Compliance Officer (41) — read-only; to audit coverage across institutions for NCPCR reporting

---

## 3. Layout

```
┌───────────────────────────────────────────────────────────────┐
│  Page header: "Institution Compliance Tracker"                │
│  [Export Compliance Report CSV]  [Send Bulk Reminder]         │
├───────────────────────────────────────────────────────────────┤
│  Summary bar: Total | Compliant | At Risk | Non-Compliant     │
│               | Escalated | Avg Coverage %                    │
├──────────────────────────────┬────────────────────────────────┤
│  Filters: Search | Type |    │  Sort: Coverage % | Status |   │
│  Status | Region | Escalated │  Last Activity               │
├──────────────────────────────┴────────────────────────────────┤
│  Institution Compliance Table (server-side paginated, 25 rows) │
├───────────────────────────────────────────────────────────────┤
│  Institution Detail Drawer (slides in on row click)           │
└───────────────────────────────────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Summary Bar

| Stat | Value | Colour |
|---|---|---|
| Total Institutions | All with ≥1 staff requiring BGV | Neutral |
| Compliant | `compliance_status = COMPLIANT` | Green |
| At Risk | `compliance_status = AT_RISK` | Amber |
| Non-Compliant | `compliance_status = NON_COMPLIANT` | Red |
| Escalated | `compliance_status = ESCALATED` | Purple |
| Platform Avg Coverage | Weighted avg `coverage_pct` across all institutions | Green ≥95%, Amber 80–95%, Red <80% |

Each stat is clickable — filters the table to that status.

---

### Section B — Filters

| Filter | Control | Notes |
|---|---|---|
| Search | Text input | Searches institution name |
| Institution Type | Multiselect: Schools / Colleges / Coaching | — |
| Compliance Status | Multiselect: COMPLIANT / AT_RISK / NON_COMPLIANT / ESCALATED | — |
| Region / State | Select | Institution's registered state |
| Escalated Only | Toggle | Shows only escalated institutions |
| Expired BGVs | Toggle | Shows institutions with `bgv_expired > 0` |

Filters persist in URL query params for shareable links.

---

### Section C — Institution Compliance Table

| Column | Sortable | Notes |
|---|---|---|
| Institution Name | Yes | — |
| Type | Yes | SCHOOL / COLLEGE / COACHING badge |
| Total Staff | Yes | `total_staff_with_minor_access` |
| Verified | No | `bgv_complete_clear` |
| In Progress | No | `bgv_in_progress` |
| Expired | No | `bgv_expired` count — red pill if > 0 |
| Coverage % | Yes | Progress bar (green ≥100%, amber 80–99%, red <80%) + % value |
| Status | Yes | Pill: COMPLIANT (green) / AT_RISK (amber) / NON_COMPLIANT (red) / ESCALATED (purple) |
| Last BGV Activity | Yes | `max(bgv_verification.updated_at)` for institution |
| Last Communication | No | Last communication log entry date |
| Actions | — | [View →] opens detail drawer; [Escalate] (Manager only) |

**Row click** → opens institution detail drawer.

**Bulk actions** (rows selected):
- [Send Document Reminder] — sends in-app notification to institution admin to upload pending documents
- [Escalate Selected] — BGV Manager only; prompts for escalation note; applies to all selected NON_COMPLIANT rows
- [Export Selected CSV] — export selected rows' compliance data

---

### Section D — Institution Detail Drawer

400px right drawer. Slides in on row click or [View →].

**Drawer header:**
- Institution name + type badge
- Compliance status pill
- [Open Full Institution Record] — external link to institution management (Div C)

**Drawer tabs:** Overview | Staff List | Communication Log

#### Overview Tab

**Compliance summary panel:**
| Metric | Value |
|---|---|
| Total staff requiring BGV | `total_staff_with_minor_access` |
| Not Initiated | `bgv_not_initiated` |
| In Progress | `bgv_in_progress` |
| Verified (CLEAR) | `bgv_complete_clear` |
| Flagged | `bgv_flagged` |
| Expired | `bgv_expired` |
| Coverage % | Progress bar + value |
| Last updated | `bgv_institution_compliance.last_updated_at` |

**Active POCSO cases banner:** If any open POCSO cases linked to this institution's staff: "⚠️ {N} POCSO case(s) open for this institution. [View Cases →]" (links to G-06 filtered by institution).

**Escalation panel** (BGV Manager only, shown when status = NON_COMPLIANT or ESCALATED):
- [Escalate Institution] — modal with escalation note (required, max 500 chars)
- If already escalated: escalation info (date, by whom, note) + [Update Escalation Note] + [Remove Escalation]
- Escalation: triggers in-app notification to Customer Success Manager (53)

**Compliance timeline:**
- Sparkline chart: coverage % over last 30 days for this institution
- Shows progression (or regression) of compliance

#### Staff List Tab

All staff members for this institution with their BGV status.

| Column | Notes |
|---|---|
| Staff Ref | `bgv_staff.staff_ref` |
| Role Title | Job role |
| BGV Status | Status pill |
| Verification Type | INITIAL / RENEWAL |
| SLA Due | For in-progress verifications |
| Last Updated | — |
| Action | [View Record →] → G-03 |

Pagination: 10 rows within drawer. Filter: Status (All / In Progress / CLEAR / FLAGGED / Not Initiated / Expired).

[+ Add Staff Member] — opens add staff modal (see Section E).

#### Communication Log Tab

All communications sent to or about this institution regarding BGV.

| Column | Notes |
|---|---|
| Date | Datetime |
| Type | IN_APP / EMAIL / PHONE_CALL / FORMAL_NOTICE |
| Subject | e.g. "Document reminder — 3 staff pending" |
| Sent By | User name |
| Notes | Free text notes for phone calls |

[+ Log Communication] — add a manual communication record (phone call log, meeting note). Fields: Type, Subject, Notes (max 500 chars), Date. For in-app and email, uses notification hub (F-06 or BGV notification templates).

---

### Section E — Add Staff Member Modal

Used when institution notifies BGV team of a new hire who needs BGV, but institution portal submission has not yet come through.

| Field | Control | Notes |
|---|---|---|
| Full Name | Text | Encrypted at rest |
| Role Title | Text | — |
| Department | Text | Optional |
| Date of Joining | Date picker | — |
| Minor Access | Toggle | Required — must confirm yes/no |
| Institution BGV Ref | Text | Institution's HR reference; optional |

**[Add Staff & Create BGV Request]:**
- Creates `bgv_staff` record
- Creates `bgv_verification` (INITIAL, DOCUMENTS_REQUESTED)
- Assigns to current user's queue (or prompt to assign to specific executive)
- ✅ "Staff added and BGV initiated — {staff_ref}" toast 4s

---

### Section F — Bulk Staff Import (CSV)

Used for institution onboarding when multiple staff need BGV simultaneously (new institution onboarding, large coaching centre with 50+ staff, or initial launch where entire existing staff base needs verification).

**[Import Staff from CSV]** button (BGV Manager, Supervisor only).

**Step 1 — Download template:**
[Download CSV Template] — provides a header row with all required columns.

**Required CSV columns:**
| Column | Notes |
|---|---|
| `institution_bgv_ref` | Institution's own HR ID for this staff |
| `full_name` | Will be AES-256 encrypted on import |
| `role_title` | — |
| `department` | Optional |
| `date_of_joining` | YYYY-MM-DD |
| `has_minor_access` | `yes` or `no` — required |

**Step 2 — Upload CSV:**
- File picker: .csv only; max 5MB; max 500 rows per upload
- Validation runs client-side preview before server submission

**Step 3 — Preview & Validate:**
Table showing all rows with validation status:
- ✅ Valid: ready to import
- ⚠️ Duplicate detected: `institution_bgv_ref` already exists for this institution — shows existing record
- ❌ Error: missing required field, invalid date format, etc.

Row-level errors shown inline. Cannot proceed if any ❌ errors exist.

**Duplicate handling:** User selects action for ⚠️ rows: Skip (default) / Update existing record.

**Step 4 — Assign & Import:**
| Option | Notes |
|---|---|
| Assign all to | Select specific BGV Executive, or "Leave unassigned" |
| Create BGV requests | Toggle ON (default) — creates `bgv_verification` (INITIAL, DOCUMENTS_PENDING) for each imported staff with `has_minor_access = true` |

**[Confirm Import]:**
- Batch creates `bgv_staff` records (encrypted name)
- Batch creates `bgv_verification` records for applicable staff
- Progress bar: "Importing {N} staff…"
- ✅ "{N} staff imported — {M} BGV requests created" toast 5s
- Error summary shown if any rows failed post-import

**Import logged in `bgv_audit_log`:** `action = BULK_IMPORT`, `note = "CSV import: {N} staff created, {M} duplicates skipped"`.

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | BGV Manager (39), BGV Ops Supervisor (92), POCSO Compliance Officer (41), Platform Admin (10) |
| BGV Executive (40) | No access to this page — institution-level view is above their scope |
| POCSO Compliance Officer (41) | Read-only — all sections. Cannot escalate, add staff, or log communications. Institution names visible. Staff refs shown but names hidden. |
| [Escalate Institution] | BGV Manager (39), Platform Admin (10) |
| [Send Bulk Reminder] | BGV Manager (39), Supervisor (92) |
| [Add Staff Member] | BGV Manager (39), Supervisor (92) |
| [Import Staff from CSV] | BGV Manager (39), Supervisor (92) |
| [Export Compliance Report CSV] | BGV Manager (39), POCSO Compliance Officer (41), Platform Admin (10) |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Institution with 0 staff requiring BGV | Row still shown (institution is registered). Staff count = 0. Coverage = "N/A". Note: "This institution has no staff marked as requiring BGV." |
| Institution newly onboarded (0 verifications started) | Coverage = 0%. Status = NOT_INITIATED (shown as distinct state). Reminder icon in Last Activity column. |
| All staff CLEAR but some expired | Status = AT_RISK even if coverage_pct = 100%, because `bgv_expired > 0`. |
| Escalation of already-COMPLIANT institution | System allows escalation (e.g. for POCSO-related concerns not reflected in coverage %). Warning: "This institution is currently COMPLIANT. Are you sure you want to escalate?" |
| Bulk reminder sent to compliant institution | Filtered out automatically. Warning: "{N} compliant institutions excluded from bulk reminder." |
| Institution deactivated on platform | Row persists in tracker with "DEACTIVATED" badge. BGV records retained per legal retention policy (7 years). No new BGV requests can be created for deactivated institutions. Institution deactivation status sourced from institution master (Div C); `bgv_institution_compliance` does not store a deactivated flag — deactivated status shown via join on institution master at query time. |
| Compliance percentage display after real-time update | When a verification completes (final_result set), `bgv_institution_compliance` record is updated within seconds via post-save signal. G-04 institution table reads from Memcached (5-min TTL). For immediate accuracy, BGV Manager can use `?nocache=true` to force fresh read. |
| CSV import > 500 rows | Upload blocked: "CSV contains {N} rows. Maximum is 500 rows per import. Split into multiple imports." |
| CSV import with name matching existing person at another institution | After import, system runs `person_id` deduplication check (name_hash + DOB). If match found: BGV Executive receives in-app task: "Possible duplicate staff across institutions — review and link if same person." |

---

## 7. UI Patterns

### Loading States
- Summary bar: 5-tile shimmer
- Table: 10-row shimmer
- Drawer: header shimmer + 3 tab label shimmers + content skeleton

### Toasts
| Action | Toast |
|---|---|
| Institution escalated | ✅ "Institution escalated — Customer Success notified" (4s) |
| Bulk reminder sent | ✅ "{N} institutions notified" (4s) |
| Staff added | ✅ "Staff added — BGV initiated: {staff_ref}" (4s) |
| Communication logged | ✅ "Communication logged" (3s) |

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table; drawer 400px right panel |
| Tablet | Table: Name, Coverage %, Status, Actions columns. Drawer full-width overlay. |
| Mobile | Card list. Drawer full-screen. |

---

*Page spec complete.*
*G-04 covers: summary bar (6 compliance stats) → institution table with coverage progress bars and inline escalation → detail drawer (Overview / Staff List / Communication Log) → compliance sparkline per institution → add staff member modal → bulk reminder sending → escalation workflow with Customer Success notification.*
