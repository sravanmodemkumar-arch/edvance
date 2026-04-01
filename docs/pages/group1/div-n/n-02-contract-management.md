# N-02 — Contract Management

**Route:** `GET /legal/contracts/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Legal Officer (#75), Contract Coordinator (#103)
**Also sees (read-only):** DPO (#76) — DPA contracts only; Finance Manager (#69) via link from M-01 (contract status only, read)

---

## Purpose

Manages the full lifecycle of all legal agreements between EduForge and its 2,050 institutions. Every institution requires at minimum three signed documents before they go live: a Master Service Agreement (MSA), a Data Processing Agreement (DPA — mandatory under DPDP Act 2023 since EduForge processes student personal data as a data processor), and a record of Terms of Service digital acceptance. At scale, manual tracking of 6,150+ documents across multiple versions, renewal dates, and signature states is not viable — this page provides the full CRUD lifecycle with an automated expiry pipeline.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Summary KPI strip | `legal_contract` aggregated by status | 10 min |
| Contract table | `legal_contract` JOIN `institution` JOIN `legal_contract_template` JOIN `user` (created_by) | 5 min |
| Institution search | `institution` (name, type) | 60 min |
| Template library | `legal_contract_template` WHERE status='ACTIVE' | 30 min |
| Expiry timeline chart | `legal_contract` GROUP BY month of expiry_date for next 12 months | 30 min |
| Signature status funnel | `legal_contract` GROUP BY status (DRAFT→SENT→SIGNED→ACTIVE) | 30 min |
| Contract detail | `legal_contract` single row JOIN audit log JOIN `legal_contract_version` | no cache |
| Renewal pipeline | `legal_contract` WHERE status='ACTIVE' AND expiry_date <= today+60d | 10 min |

Cache keys scoped to `(user_id, filters)`. `?nocache=true` for Legal Officer (#75) only.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?status` | `draft`, `sent`, `signed`, `active`, `expiring_soon`, `expired`, `terminated`, `all` | `all` | Filter by contract status |
| `?contract_type` | `msa`, `dpa`, `sla`, `tos_acceptance`, `nda`, `mou`, `all` | `all` | Filter by contract type |
| `?institution_type` | `school`, `college`, `coaching`, `group`, `all` | `all` | Filter by institution type |
| `?expiry_before` | `YYYY-MM-DD` | — | Contracts expiring before date |
| `?expiry_after` | `YYYY-MM-DD` | — | Contracts expiring after date |
| `?institution_id` | institution UUID | — | Contracts for a specific institution |
| `?q` | string | — | Full-text search: institution name, contract reference |
| `?sort` | `expiry_asc`, `expiry_desc`, `institution_name`, `created_at_desc`, `status` | `expiry_asc` | Table sort order |
| `?page` | integer | `1` | Server-side pagination |
| `?export` | `csv` | — | Export filtered contract list (Legal Officer only) |
| `?nocache` | `true` | — | Bypass Memcached (Legal Officer #75 only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Auto-Refresh | Target ID |
|---|---|---|---|---|
| KPI strip | `?part=kpi` | Page load | 10 min | `#n2-kpi-strip` |
| Expiry timeline chart | `?part=expiry_timeline` | Page load | 30 min | `#n2-expiry-timeline` |
| Signature funnel | `?part=sig_funnel` | Page load | 30 min | `#n2-sig-funnel` |
| Contract table | `?part=table` | Page load + filter change + sort + page | — | `#n2-contract-table` |
| Renewal pipeline | `?part=renewal_pipeline` | Page load | 10 min | `#n2-renewal-pipeline` |
| Contract detail drawer | `/legal/contracts/{id}/detail/` | [View] action click | — | `#n2-contract-detail` |

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Contract Management   [Search contracts...  🔍]   [+ New Contract]│
├────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (4 tiles)                                               │
├──────────────────────────┬─────────────────────────────────────────┤
│  EXPIRY TIMELINE         │  SIGNATURE STATUS FUNNEL                │
│  (12 months, bar chart)  │  (DRAFT → SENT → SIGNED → ACTIVE)      │
├──────────────────────────┴─────────────────────────────────────────┤
│  FILTER ROW                                                        │
│  CONTRACT TABLE + PAGINATION                                       │
├────────────────────────────────────────────────────────────────────┤
│  RENEWAL PIPELINE (next 60 days)                                   │
└────────────────────────────────────────────────────────────────────┘
```

---

## Components

### KPI Strip (4 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 2,050        │ │ 14           │ │ 48           │ │ 99.8%        │
│ Active       │ │ Expiring     │ │ Awaiting     │ │ Coverage     │
│ Contracts    │ │ < 30 days    │ │ Signature    │ │ (MSA)        │
│ ↑+3 this mo.│ │ ⚠ 3 critical │ │ (SENT status)│ │ 2046/2050    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Tile 1 — Active Contracts (MSA):** `COUNT(legal_contract) WHERE contract_type='MSA' AND status='ACTIVE'`. Delta shows contracts activated this month. Green if = 2,050, amber if ≥ 2,000, red if < 2,000. Clicking filters table to `?status=active&contract_type=msa`.

**Tile 2 — Expiring < 30 Days:** `COUNT(legal_contract) WHERE status='ACTIVE' AND expiry_date <= today+30d`. Sub-label: "N critical" where `expiry_date <= today+7d`. Amber if 1–10, red if > 10. Clicking → `?status=expiring_soon`.

**Tile 3 — Awaiting Signature:** `COUNT(legal_contract) WHERE status='SENT_FOR_SIGNATURE'`. Age indicator: "oldest N days" from `sent_at`. Red if any > 14 days awaiting. Clicking → `?status=sent`.

**Tile 4 — Coverage %:** `COUNT(institution has ACTIVE MSA) / 2050 × 100`. Tooltip shows breakdown: MSA coverage / DPA coverage / SLA coverage. Green if 100%, amber if ≥ 98%, red if < 98%.

---

### Expiry Timeline Chart

Bar chart — number of contracts expiring per month for the next 12 months.

- **Stacked bars by type:** MSA (blue-500) · DPA (violet-500) · SLA (orange-400) · Other (grey-300)
- **X-axis:** month labels (MMM YY)
- **Y-axis:** count of contracts expiring
- **Red reference line** at 50 (high-volume expiry month indicator)
- **Hover tooltip:** month · total expiring · breakdown by type
- **Bar click:** filters contract table to that month (`?expiry_after=first_of_month&expiry_before=last_of_month`)

---

### Signature Status Funnel

Horizontal funnel chart showing contracts at each stage of the signing workflow.

```
DRAFT           [████████░░░░░░░░░░░░]  124 (5.9%)
SENT            [██████████████░░░░░░]  48  (2.3%)
SIGNED          [███░░░░░░░░░░░░░░░░░]  12  (0.6%)
ACTIVE          [████████████████████]  2,050 (97.4%)
EXPIRED         [█░░░░░░░░░░░░░░░░░░░]  18  (0.9%)
TERMINATED      [░░░░░░░░░░░░░░░░░░░░]  3   (0.1%)
```

- Clicking a stage filters the contract table to that status
- `EXPIRED` shown in red-100 background row
- Counts represent all contract records (all types combined)

---

### Filter Row

```
Type: [All ▼]  Status: [All ▼]  Institution type: [All ▼]
Expiry: [From: ─────] [To: ─────]    [Apply]   [Clear]
Sort: [Expiry ↑ ▼]    Showing 2,255 contracts     [Export CSV]
```

- **Search:** `[Search institution name or contract ref... 🔍]` — searches `institution.name` and `legal_contract.reference_number`. Min 2 chars, 300ms debounce.
- **[Export CSV]:** Legal Officer (#75) only. Filename: `eduforge_contracts_YYYY-MM-DD.csv`.

---

### Contract Table

Sortable, selectable (checkbox per row), server-side paginated (50 per page).

| Column | Description |
|---|---|
| ☐ | Row checkbox for bulk actions |
| Institution | Name (link → institution profile) + type badge (SCHOOL/COLLEGE/COACHING/GROUP) |
| Contract Type | MSA / DPA / SLA / ToS Acceptance / NDA / MoU |
| Reference # | `legal_contract.reference_number` (e.g. `EF-MSA-2024-0847`) |
| Status | Badge: DRAFT (grey) / SENT (blue) / SIGNED (teal) / ACTIVE (green) / EXPIRING SOON (amber) / EXPIRED (red) / TERMINATED (dark red) |
| Effective Date | Start date |
| Expiry Date | Date. Red if < 7 days, amber if < 30 days, green otherwise |
| Days to Expiry | Positive integer or "Expired N days ago" in red |
| Signed By | Signatory name + designation (from institution) |
| Template Version | e.g. `v2.1` — links to template in N-06 |
| Actions | [View] [Renew] [Send Reminder] [Terminate] |

**EXPIRING_SOON row:** amber-50 background.
**EXPIRED row:** red-50 background. [Renew] action prominent.
**TERMINATED row:** grey-100 background, strikethrough on dates. No actions available.

**[View]:** Opens Contract Detail Drawer (see below).
**[Renew]:** Opens Renewal Modal. Available to Legal Officer and Contract Coordinator.
**[Send Reminder]:** Available for SENT_FOR_SIGNATURE contracts only (sends email to institution signatory). Contract Coordinator and Legal Officer.
**[Terminate]:** Legal Officer only. Opens Termination Confirmation modal.

**Bulk actions (visible when rows selected):**
- [Send Reminder to Selected] — for SENT contracts
- [Export Selected as PDF] — downloads ZIP of contract PDFs
- [Assign Template Version] — update template version across selected DRAFT contracts

---

### Contract Detail Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  MSA  ·  Delhi Public School                        [Close ×]    │
│  EF-MSA-2024-0847                                                │
├──────────────────────────────────────────────────────────────────┤
│  Status: ACTIVE                      Template: v2.1              │
│  Effective: 1 Apr 2024               Expiry: 31 Mar 2026         │
│  Days remaining: 10 days             ⚠ Renewal required soon     │
├──────────────────────────────────────────────────────────────────┤
│  Signatory                                                       │
│  Dr. Ramesh Kumar                                                │
│  Principal · principal@dps.edu                                   │
│  Signed: 28 Mar 2024 · Method: E-SIGNATURE (DigiSign)            │
│  DigiSign Reference: DS-2024-339821                              │
├──────────────────────────────────────────────────────────────────┤
│  Created by: Priya Sharma (Contract Coordinator)  2 Mar 2024     │
│  Reviewed by: Arjun Mehta (Legal Officer)         27 Mar 2024    │
├──────────────────────────────────────────────────────────────────┤
│  [Download PDF]  [Initiate Renewal]  [View Audit Log]            │
│  [Terminate Contract]  (Legal Officer only)                      │
└──────────────────────────────────────────────────────────────────┘
```

**Tabs within drawer:**
1. **Overview** (default): As shown above
2. **Version History:** List of all contract versions for this institution + type, linked to N-06 templates
3. **Audit Log:** All actions on this contract record (create, edit, send, sign, renew, terminate) with actor, timestamp, IP

**[Download PDF]:** Generates PDF from `legal_contract.document_url` (S3). Available to Legal Officer and Contract Coordinator.
**[Initiate Renewal]:** Opens Renewal Modal.
**[Terminate Contract]:** Legal Officer only. Opens Termination Confirmation.

---

### New Contract Modal / Renewal Modal

**New Contract Modal:**

```
┌──────────────────────────────────────────────────────────────────┐
│  New Contract                                                    │
├──────────────────────────────────────────────────────────────────┤
│  Institution*  [Search institution...                     ]      │
│  Contract type*  [Master Service Agreement (MSA)        ▼]       │
│  Template version*  [v2.1 (current — effective 1 Jan 2026) ▼]   │
│  Effective date*  [___ / ___ / _____]                            │
│  Expiry date*  [___ / ___ / _____]   (default: effective + 2yr) │
│  Signatory name*  [                                       ]      │
│  Signatory email*  [                                      ]      │
│  Signatory designation*  [                                ]      │
│  Custom notes  [Optional notes visible internally only   ]       │
│                                                                  │
│  ⚠  This institution already has an ACTIVE MSA (EF-MSA-2024-    │
│     0847). Creating a new one will supersede the current.        │
│                                                                  │
│  Signature method:  ● E-Signature (DigiSign)  ○ Manual Upload   │
│                                                                  │
│  [Cancel]                    [Save as Draft]  [Send for Signature]│
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Institution: required; must be an active institution in the system
- Contract type: required
- Template version: required; must be ACTIVE template
- Effective date: required; cannot be in the past by more than 30 days
- Expiry date: required; must be > effective date; max 5 years
- Signatory name: required; min 2 chars
- Signatory email: required; valid email format
- Signatory designation: required; min 2 chars
- Overlap guard: warns (does not block) if active contract of same type already exists for institution
- DPA guard: if contract_type = DPA, checks that institution has ACTIVE MSA; blocks if MSA missing: "Institution must have an active MSA before a DPA can be created."

**[Save as Draft]:** POST to `/legal/contracts/drafts/create/`. Creates `legal_contract` record with `status='DRAFT'`. Available to Contract Coordinator (#103) and Legal Officer (#75).

**[Send for Signature]:** POST to `/legal/contracts/send/`. Creates record with `status='SENT_FOR_SIGNATURE'` and dispatches e-signature request via DigiSign API (or email with PDF link if Manual Upload). Legal Officer (#75) must review before send for contracts with `requires_legal_review=true`.

**Validation timing:**
- **Real-time (on blur/change):** Email format (signatory email), date format/range (effective date, expiry date)
- **Submit-time:** Institution required check, overlap guard, DPA guard, all required fields
- **Unsaved changes warning:** On attempt to close modal or navigate away with any field filled: "You have unsaved changes. Discard them?" [Cancel] [Discard]

**SIGNED → ACTIVE transition:**
- **DigiSign path:** When DigiSign webhook fires `document.signed` with `all_parties_signed=true` → status auto-set to ACTIVE (see DigiSign Webhook Specification section)
- **Manual Upload path:** After signatory uploads signed PDF, Contract Coordinator marks status as SIGNED. Legal Officer (#75) then uses [Activate Contract] button in detail drawer → POST to `/legal/contracts/{id}/activate/` → sets `status='ACTIVE'`, `effective_date=today` (or future date if specified). Requires mandatory note: "Verified signed document authenticity."
- **Both paths:** `legal_compliance_deadline` entry for the expiry date is created/updated in N-07 calendar on ACTIVE status.

**Contract Reference Number Generation:**
Format: `EF-{TYPE_CODE}-{YEAR}-{SEQUENCE_4DIGITS}`
- `TYPE_CODE`: MSA / DPA / SLA / TOS / NDA / MOU
- `YEAR`: calendar year of contract creation
- `SEQUENCE_4DIGITS`: auto-incrementing integer per type per year, zero-padded to 4 digits (0001–9999)
- Generated by database trigger on INSERT into `legal_contract`; unique index on `reference_number`
- Examples: `EF-MSA-2024-0001`, `EF-DPA-2025-0847`, `EF-SLA-2026-0012`
- Read-only field — not editable after creation

**Contract Coverage — All 3 Required Types:**
Coverage Tile 4 in the KPI strip shows MSA coverage. Full coverage per institution requires all three:

| Contract | Required for | Minimum before |
|---|---|---|
| MSA (Master Service Agreement) | All institutions | Before any subscription activation |
| DPA (Data Processing Agreement) | All institutions | Before any student data is processed — DPDP Act §8(6) |
| SLA (Service Level Agreement) | All institutions | Before go-live |

**[Coverage Gap Report]** (accessible via [View] on Tile 4): Table showing each of the 2,050 institutions and which of the three required contracts are ACTIVE (✓) or missing (✗). Filterable by gap type. Export CSV available to Legal Officer.

**Bulk Contract Creation (Institution Onboarding):**
When onboarding a new institution (triggered from Onboarding Specialist #51 handoff), a [+ Bulk Create (MSA + DPA + SLA)] button allows the Contract Coordinator to fill shared fields once (institution, signatory, effective date) and instantiate all three contracts in a single submit action. POST to `/legal/contracts/bulk-create/`. Creates three `legal_contract` records atomically. Failure on any one rolls back all three.

**Institution Offboarding Contract Workflow:**
When an institution is flagged for offboarding (Billing Admin #70 → support request):
1. Contract Coordinator (#103) receives alert: "Institution [name] flagged for offboarding."
2. [Terminate All Active Contracts] bulk action in the institution's contract list (Contract Coordinator can initiate; Legal Officer must co-approve via one-click approval email)
3. Termination reason: "Institution exit", effective date = offboarding date
4. On all contracts terminated: system automatically enqueues a DPDP Act §12 erasure DSR on behalf of the institution in N-03 (`dpdp_dsr.request_type='ERASE'`, `requester_role='INSTITUTION_ADMIN'`)
5. N-07 deadline created: "Institution data erasure — [name]" (category: DSR)

**Contract Template Preview:**
Before instantiating: [Preview Template] link next to template version dropdown opens a read-only modal displaying the full template text (PDF rendered inline or markdown). Contract Coordinator (#103) can view but not edit. Legal Officer (#75) can annotate with "requires legal review" flag from the preview modal.

**Renewal Modal:** Same form, pre-filled with current contract data. Effective date defaults to `current_expiry + 1 day`. Creates a new `legal_contract` row; old row updated to `status='SUPERSEDED'` once new contract is ACTIVE.

---

### Termination Confirmation Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Terminate Contract — EF-MSA-2024-0847                           │
│  Delhi Public School                                             │
├──────────────────────────────────────────────────────────────────┤
│  ⚠ This will immediately mark the MSA as TERMINATED.            │
│  The institution's platform access should be reviewed by          │
│  Support (#47) before termination.                               │
│                                                                  │
│  Termination date*  [___ / ___ / _____]  (default: today)       │
│  Reason*  [Select reason...                               ▼]     │
│    → Mutual agreement / Breach by institution / Non-payment /    │
│       Regulatory issue / Platform exit / Other                   │
│  Internal notes*  [                                              ]│
│                                                                  │
│  Type "TERMINATE" to confirm:  [                     ]           │
│                                                                  │
│  [Cancel]                                     [Terminate]        │
└──────────────────────────────────────────────────────────────────┘
```

**POST** to `/legal/contracts/{id}/terminate/`. Legal Officer (#75) only. Requires typing "TERMINATE" confirmation. Updates `legal_contract.status = 'TERMINATED'`. Audit log entry created with reason + actor + timestamp.

---

### Renewal Pipeline

Compact view of all MSAs expiring within 60 days, grouped by urgency bucket.

```
  Renewal Pipeline — 60 days ahead

  CRITICAL (< 7 days):  3 institutions
  └─ Delhi Public School     MSA  Expires: 22 Mar (in 1d)   [Initiate]
  └─ Sunrise Academy         MSA  Expires: 24 Mar (in 3d)   Renewal sent ✓
  └─ Excel Coaching Hub      MSA  Expires: 27 Mar (in 6d)   [Initiate]

  ATTENTION (7–30 days):  11 institutions
  └─ Victory College         MSA  Expires: 12 Apr (in 22d)  [Initiate]
  └─ ...

  UPCOMING (31–60 days):  27 institutions
  [View all 27 →]
```

- Renewal initiated = contract in SENT_FOR_SIGNATURE or SIGNED status for that institution/type
- [Initiate]: Opens Renewal Modal
- [View all 27 →]: links to `?status=active&expiry_before=today+60d`

**Visible to:** Legal Officer (#75) and Contract Coordinator (#103).

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| Contract table | No contracts match filters | "No contracts found for the selected filters." with [Clear Filters] button |
| Renewal pipeline | No contracts expiring in 60 days | "No renewals due in the next 60 days." with green checkmark |
| Awaiting signature | No contracts in SENT status | "No contracts awaiting signature." |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Contract created (draft) | "Contract draft created for [institution]." | Blue (info) |
| Contract sent for signature | "Contract sent to [signatory_email] for signature." | Blue (info) |
| Contract signed (webhook from DigiSign) | "[institution] has signed the [type] contract. [Activate →]" | Green |
| Contract activated | "Contract [ref] is now ACTIVE." | Green |
| Renewal initiated | "Renewal sent to [institution] for signature." | Blue |
| Termination confirmed | "Contract [ref] terminated. Reason: [reason]." | Amber (warning) |
| Reminder sent | "Signature reminder sent to [signatory_email]." | Blue |
| Export CSV queued | "Contract export is being prepared. You will be notified when ready." | Blue |

---

## Authorization

**Route guard:** `@division_n_required(allowed_roles=[75, 76, 103])` applied to `ContractManagementView`.

| Scenario | Behaviour |
|---|---|
| Unauthenticated | Redirect to `/login/?next=/legal/contracts/` |
| Role not in allowed list | 403 |
| DPO (#76) | Read-only; can only view DPA contracts (`contract_type='DPA'` filter applied server-side); no create/edit/terminate |
| Contract Coordinator (#103) | Cannot terminate contracts; cannot send contracts requiring legal review (`requires_legal_review=true`) |
| Terminate action | Legal Officer (#75) only; other roles receive 403 on POST |
| Export CSV | Legal Officer (#75) only |

---

## Role-Based UI Visibility Summary

| Element | 75 Legal Officer | 76 DPO | 103 Contract Coordinator |
|---|---|---|---|
| Full contract table (all types) | Yes | DPA contracts only | Yes |
| Create new contract | Yes | No | Yes |
| Send for signature | Yes | No | Yes (standard only) |
| Send legally-reviewed contract | Yes | No | No |
| [Terminate] action | Yes | No | No |
| Renewal pipeline | Yes | No | Yes |
| Export CSV | Yes | No | No |
| [?nocache=true] | Yes | No | No |
| Template library link (N-06) | Yes (full) | Yes (read) | Yes (read) |
| Audit log (drawer tab) | Yes | No | Yes (own actions) |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Contract table (paginated, 50 rows) | < 800ms P95 (cache hit) | Index on `(status, expiry_date, institution_id)` |
| Expiry timeline chart | < 600ms P95 (30 min TTL) | Pre-aggregated by month |
| Export CSV generation | < 30s | Async Celery task (N-1) if > 500 rows; otherwise synchronous |
| Full page load | < 2s P95 | Parts load in parallel |
| DigiSign webhook processing | < 500ms | Status update + audit log on receipt |

---

## Background Tasks

**Task N-1 — Contract Expiry Scanner (daily, 08:00 IST):**
- Sets `status = 'EXPIRING_SOON'` for contracts where `status='ACTIVE' AND expiry_date <= today+30d`
- Sends daily email digest to Legal Officer (#75) and Contract Coordinator (#103) listing all expiring contracts
- Creates `legal_compliance_deadline` entry for each expiring contract (visible in N-07 calendar)

**Task N-2 — Unsigned Contract Reminder (every 3 days):**
- For each `legal_contract` WHERE `status='SENT_FOR_SIGNATURE' AND sent_at <= today-7d` and no reminder in last 3 days:
  - Sends reminder email to institution signatory
  - Creates `legal_contract_reminder` audit log entry
  - After 3 reminders with no response: flags for Contract Coordinator manual follow-up

---

## DigiSign Webhook Specification

EduForge receives signature completion notifications from DigiSign via webhook. This is the primary mechanism for automatic contract status transitions.

**Endpoint:** `POST /legal/contracts/webhooks/digisign/`

**Authentication:** HMAC-SHA256 signature in `X-DigiSign-Signature` header. Verified against `settings.DIGISIGN_WEBHOOK_SECRET`. Requests failing verification return 403 immediately (no processing).

**Expected payload:**
```json
{
  "event": "document.signed",
  "document_id": "DS-2024-339821",
  "signed_by_email": "principal@dps.edu",
  "signed_at": "2024-03-28T10:14:32Z",
  "all_parties_signed": true,
  "document_status": "completed",
  "metadata": {
    "legal_contract_id": "<eduforge-uuid>"
  }
}
```

**Processing (on receipt of valid `document.signed` event):**
1. Look up `legal_contract` WHERE `id = metadata.legal_contract_id`
2. Verify `legal_contract.status = 'SENT_FOR_SIGNATURE'` (idempotency guard)
3. Set `status = 'SIGNED'`, `signed_at = signed_at`, `signature_reference = document_id`
4. If `all_parties_signed = true`: set `status = 'ACTIVE'`, `effective_date = today` (if not already set in future)
5. Create audit log entry: "Contract signed via DigiSign. Ref: [document_id]"
6. Push real-time notification to Contract Coordinator (#103) and Legal Officer (#75) via Django Channels: "[institution] has signed [contract_type]. [View →]"

**Error handling:**
| Error | Response | Action |
|---|---|---|
| HMAC verification failed | 403 | Log attempt, alert Security Engineer (#16) |
| `legal_contract_id` not found | 404 | Log + alert Contract Coordinator |
| Contract already ACTIVE (duplicate) | 200 (idempotent) | No state change; log as duplicate |
| Status transition invalid (e.g., TERMINATED → SIGNED) | 400 | Log error; alert Legal Officer |
| Processing error (DB exception) | 500 | DigiSign retries up to 3×; after max retries, alert via email |

**Manual Upload fallback (when DigiSign unavailable):**
If e-signature service is down, Contract Coordinator can use "Manual Upload" method in the Send for Signature modal:
- Uploads a scanned signed PDF
- Manually enters signatory name, signature date
- Sets `signature_method = 'MANUAL_UPLOAD'` instead of `'DIGISIGN'`
- Legal Officer (#75) must verify and activate manually via [Activate Contract] button in drawer

**Keyboard shortcuts (N-02):**

| Key | Action |
|---|---|
| `g` `l` | Go to Legal Dashboard (N-01) |
| `g` `c` | Go to Contract Management (this page) |
| `n` | Open New Contract modal |
| `/` | Focus contract search input |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |

## Search & Filter Loading States

**Search field (min 2 chars, 300ms debounce):**
- While debouncing (< 300ms since last keystroke): loading spinner icon appears in search input right side; table is NOT updated yet
- After debounce, HTMX GET issued: table rows replaced with shimmer skeleton (matching current page row count)
- Results loaded: table re-renders with match count updated in filter row ("Showing N contracts")
- 0 results: Empty state shown (see Empty States)
- Search error (DB fail): Toast "Search failed. Please try again." + table retains previous results

**Filter changes (status, type, institution_type dropdowns):**
- On [Apply]: immediate table shimmer — no debounce (filters are definitive user actions)
- Filter row shows "Filtering..." spinner next to [Apply] button during load
- On completion: "Showing N contracts" count updates

**Contract Detail Drawer — Loading & Error States:**
- On [View] action: drawer slide-in overlay appears immediately (empty shell)
- Content skeleton (3 placeholder rows) shown for < 500ms typical
- On 404 (contract deleted mid-session): "Contract not found. It may have been deleted." + [Close] button
- On 403: "You do not have permission to view this contract."
- Audit Log tab: lazy-loaded on tab click (not on drawer open); shows its own skeleton while loading

**Contract Coordinator — [Send for Signature] restriction:**
- When `legal_contract.requires_legal_review = true`:
  - [Send for Signature] button is **disabled** (grey, cursor-not-allowed)
  - Hover tooltip: "Legal Officer review required before sending. Assign to Legal Officer to proceed."
  - No POST accepted — server returns 403 with `{"error": "legal_review_required"}` if bypassed via API
  - Toast (if attempted): "This contract requires Legal Officer review before it can be sent for signature."
