# N-03 — Data Privacy & DPDP Compliance

**Route:** `GET /legal/privacy/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Data Privacy Officer (#76), Legal Officer (#75)
**Also sees:** Data Compliance Analyst (#104) — read-only on DSR tab and Consent tab; Security Engineer (#16) — breach tab (creates incidents); Platform Admin (#10) — consent coverage read-only

---

## Purpose

DPDP Act 2023 compliance operations centre. EduForge processes personal data of up to 7.6 million students (many of whom are minors — "children" under DPDP Act §9) across 2,050 institutions and therefore qualifies as a "significant data fiduciary" candidate under rules that MEITY may notify. This page covers three operational domains: (1) Data Subject Requests — individuals exercising rights under §11–14 of the DPDP Act with mandatory 30-day resolution; (2) Breach Incident Management — security incidents triggering 72-hour DPDP authority notification and 6-hour CERT-In report; (3) Consent Coverage — tracking consent state across all data principals across all institutions.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `dpdp_dsr` counts by status + `dpdp_breach_incident` open counts + `dpdp_consent_record` coverage stats | 5 min |
| DSR table | `dpdp_dsr` JOIN `institution` JOIN `user` (assigned_to) | 2 min |
| DSR trend chart | `dpdp_dsr` GROUP BY month: opened, resolved, breached_sla | 60 min |
| Breach table | `dpdp_breach_incident` JOIN `user` (discovered_by) | 1 min |
| Breach notification timeline | `dpdp_breach_incident` single row: cert_in_notified_at, dpdp_notified_at, institutions_notified_at | no cache |
| Consent coverage by institution | `dpdp_consent_record` GROUP BY institution_id: total_users, consented_users, consent_version | 10 min |
| Consent trend | `dpdp_consent_record` monthly snapshot aggregates | 60 min |
| Data flow register | `dpdp_data_flow` JOIN `dpdp_sub_processor` | 30 min |

Cache keys scoped to `(user_id, tab, filters)`. `?nocache=true` for DPO (#76) and Legal Officer (#75).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?tab` | `dsr`, `breaches`, `consent`, `data_flows` | `dsr` | Active tab |
| `?status` | Tab-specific status values | `all` | Filter by record status |
| `?request_type` | `access`, `erase`, `correct`, `restrict`, `portability`, `grievance`, `all` | `all` | DSR tab: filter by request type |
| `?institution_id` | UUID | — | Filter DSR/consent to one institution |
| `?severity` | `low`, `medium`, `high`, `critical`, `all` | `all` | Breach tab: filter by severity |
| `?q` | string | — | Search: DSR requester name/email, breach ID, institution name |
| `?sort` | Tab-specific sort options | `due_at_asc` (DSR), `discovered_at_desc` (breaches) | Table sort |
| `?page` | integer | `1` | Server-side pagination |
| `?export` | `csv` | — | Export filtered DSR or breach records (DPO + Legal Officer only) |
| `?nocache` | `true` | — | Bypass Memcached (DPO + Legal Officer only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Auto-Refresh | Target ID |
|---|---|---|---|---|
| KPI strip | `?part=kpi` | Page load + tab change | 5 min | `#n3-kpi-strip` |
| DSR table | `?part=dsr_table` | Tab=dsr + filter/sort/page change | 2 min | `#n3-dsr-table` |
| DSR trend chart | `?part=dsr_trend` | Tab=dsr load | 60 min | `#n3-dsr-trend` |
| Breach table | `?part=breach_table` | Tab=breaches + filter change | 1 min | `#n3-breach-table` |
| Consent coverage table | `?part=consent_table` | Tab=consent + filter change | 10 min | `#n3-consent-table` |
| Consent trend chart | `?part=consent_trend` | Tab=consent load | 60 min | `#n3-consent-trend` |
| Data flow register | `?part=data_flows` | Tab=data_flows load | 30 min | `#n3-data-flows` |

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Data Privacy & DPDP Compliance    [Search... 🔍]   [+ New DSR]   │
├────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (4 tiles — tab-aware)                                   │
├────────────────────────────────────────────────────────────────────┤
│  [DSR] [Breach Incidents] [Consent Coverage] [Data Flow Register]  │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  TAB CONTENT (see tab specs below)                                 │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip (4 tiles — tab-aware)

KPI tiles update to reflect the active tab. Common tiles shown across all tabs:

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 7            │ │ 3            │ │ 0            │ │ 94.2%        │
│ Open DSRs    │ │ Near SLA     │ │ Active       │ │ Consent      │
│              │ │ (≤ 10 days)  │ │ Breaches     │ │ Coverage     │
│ 2 ERASE/CORR │ │ ⚠ Attention  │ │ ✓ Clean      │ │ 71.1L users  │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Tile 1 — Open DSRs:** `COUNT(dpdp_dsr) WHERE status IN ('OPEN','IN_PROGRESS')`. Sub-label shows count of erase/correction requests specifically (higher complexity). Amber if any near SLA, red if any overdue.

**Tile 2 — Near SLA:** `COUNT(dpdp_dsr) WHERE status IN ('OPEN','IN_PROGRESS') AND due_at <= today+10d`. Red if any `due_at <= today+5d`, amber if `due_at <= today+10d`. Clicking filters DSR table to near-SLA records.

**Tile 3 — Active Breaches:** `COUNT(dpdp_breach_incident) WHERE status NOT IN ('RESOLVED')`. "✓ Clean" in green if 0. Red with pulsing dot if > 0. Clicking switches to Breach tab.

**Tile 4 — Consent Coverage:** `SUM(consented_users) / SUM(total_users) × 100` across all institutions. Sub-label: "N users covered". Green if ≥ 95%, amber if 90–94.9%, red if < 90%. Clicking switches to Consent tab.

---

## Tab A — Data Subject Requests (DSR)

### DSR Trend Chart

Line chart — 12 months of DSR volume and SLA performance.

- **Lines:** DSRs opened (solid blue-500) · DSRs resolved (solid green-500) · SLA breaches (dashed red-400)
- **Y-axis:** count of DSRs
- **Reference line:** none (SLA breaches ideally = 0 always)
- **Right Y-axis:** avg resolution days (0–30 days). Red zone fill above 30-day mark.
- **Hover tooltip:** month · opened · resolved · SLA breaches · avg resolution days
- **Low data:** "No DSRs" label on months with 0 records

---

### DSR Filter Row

```
Type: [All ▼]  Status: [All ▼]  Institution: [All ▼]  Requester role: [All ▼]
Due: [All ▼]   [Apply]   [Clear]   Sort: [Due date ↑ ▼]   Showing 7 open DSRs
[+ Log New DSR]    [Export CSV]
```

- **[+ Log New DSR]:** DPO (#76) and Data Compliance Analyst (#104, triage only). Opens New DSR modal.
- **[Export CSV]:** DPO (#76) and Legal Officer (#75) only.

---

### DSR Table

Sortable, server-side paginated (25 per page).

| Column | Description |
|---|---|
| DSR ID | `dpdp_dsr.reference_number` (e.g. `DSR-2026-044`) |
| Request Type | Badge: ACCESS (blue) / ERASE (red) / CORRECT (amber) / RESTRICT (orange) / PORTABILITY (teal) / GRIEVANCE (purple) / NOMINATION (grey) |
| Requester | Name + email + role badge (STUDENT / STAFF / INSTITUTION_ADMIN / PARENT) |
| Institution | Institution name (link → institution profile) + type badge |
| Status | OPEN (grey) / IN_PROGRESS (blue) / PENDING_LEGAL (amber) / RESOLVED (green) / REJECTED (red) |
| Raised At | Date (relative if < 7 days) |
| Due At | `raised_at + 30 days`. Red if ≤ 5 days remaining, amber if ≤ 10 days. "OVERDUE" badge in red if past. |
| Days Left | Countdown. "OVERDUE (Nd)" in red if past due_at |
| Assigned To | DPO or Data Compliance Analyst avatar + name |
| Actions | [View] [Assign] [Resolve] [Reject] |

**OVERDUE row:** red-50 background.
**PENDING_LEGAL row:** amber-50 background (escalated to Legal Officer for legal opinion).

**[View]:** Opens DSR Detail Drawer.
**[Assign]:** DPO (#76) only. Opens assign dropdown: self or Data Compliance Analyst (#104).
**[Resolve]:** DPO (#76) only. Opens Resolution Modal.
**[Reject]:** DPO (#76) only. Opens Rejection Modal with reason.

---

### DSR Detail Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  DSR-2026-044  ·  ERASE REQUEST                     [Close ×]   │
├──────────────────────────────────────────────────────────────────┤
│  Requester:  Aisha Sharma                                        │
│  Email:      aisha.sharma@student.dps.edu                        │
│  Role:       STUDENT                                             │
│  Institution: Delhi Public School                                │
│                                                                  │
│  Raised:     14 Mar 2026 09:14 IST                               │
│  Due:        13 Apr 2026 09:14 IST  (23 days remaining)          │
│  Status:     IN_PROGRESS                                         │
│  Assigned to: Priya DPO (Data Privacy Officer)                   │
├──────────────────────────────────────────────────────────────────┤
│  Request details:                                                │
│  "I want all my exam result data and personal profile deleted     │
│  from the EduForge platform. I have left this institution."      │
├──────────────────────────────────────────────────────────────────┤
│  Scope assessment:                                               │
│  Affected data: Student profile · exam_attempt records ·         │
│  result records · notification preferences · login history       │
│  Linked schemas: dps_school · analytics_schema (aggregated)      │
│                                                                  │
│  Exemption check: ☐ Data required for legal obligation           │
│                   ☐ Data required for ongoing litigation         │
│                   ☐ Statistical purpose (anonymised retained)    │
├──────────────────────────────────────────────────────────────────┤
│  Internal notes:  [Add note...                           ]       │
│                                                                  │
│  [Mark Pending Legal]  [Resolve]  [Reject]                       │
└──────────────────────────────────────────────────────────────────┘
```

Tabs:
1. **Details** (default): As above
2. **Audit Log:** All status changes, assignments, notes with actor + timestamp
3. **Data Map:** Read-only view of all tables/schemas containing data for this requester (pre-computed by Data Compliance Analyst)

**[Resolve]:** Opens Resolution Modal — DPO confirms action taken (data erased, data exported, data corrected etc.), selects resolution type, adds resolution notes. Updates `dpdp_dsr.status='RESOLVED'`, `resolved_at=now()`. Triggers confirmation email to requester.

**[Reject]:** Opens Rejection Modal — DPO selects rejection reason (legal exemption / request not verifiable / data not held / other) + rejection notes. Triggers rejection email with right to complain to DPDP authority.

**[Mark Pending Legal]:** Escalates to Legal Officer (#75) for opinion (e.g., contested erasure requests where institution claims right to retain for compliance). Adds `status='PENDING_LEGAL'`.

---

### DSR Request Type Reference (DPDP Act 2023)

> **Statutory basis note:** The Digital Personal Data Protection Act 2023 defines four rights for data principals: §11 (Right to Information), §12 (Right to Correction & Erasure), §13 (Right to Grievance Redressal), §14 (Right to Nominate). There is NO "Right to Restrict Processing" in DPDP Act 2023 — that is GDPR Article 18 and does not apply to Indian law. The RESTRICT type below is a platform goodwill extension only, not a statutory obligation.
>
> **Breach notification timing:** DPDP Act requires notifying the DPDP authority "in such form and manner as may be prescribed" (§8(6)(f)) — i.e., notification form and timeline are defined by Rules, not the Act itself. Industry standard following anticipated rules and international best practice is 72 hours. The 72h figure used in this spec is the operational target, not a statutory number. The CERT-In 6-hour window is a separate obligation under CERT-In Directions 2022, not DPDP Act.

| Type | DPDP Section | Must Fulfill | Rejection Grounds | Special Workflow |
|---|---|---|---|---|
| ACCESS | §11 — Right to Information | Yes | Data not held; requester unverifiable | Provide data in machine-readable format (JSON/CSV) within 30 days. Covers: data categories collected, how processed, list of processors, whether shared with third parties. |
| ERASE | §12 — Right to Erasure | Yes (with exemptions) | Legal obligation to retain; ongoing litigation; statistical/research purpose with anonymisation | Requires Legal Officer review if institution contests. Data erased from all linked schemas including tenant + analytics. Exemptions must be documented in audit log. |
| CORRECT | §12 — Right to Correction | Yes | Correction would distort factual historical record | Same §12 as erasure. Applied to all linked schemas. Correction versioned in audit trail. |
| RESTRICT | *(Not in DPDP Act — platform goodwill extension)* | No statutory obligation | May reject: platform determines appropriate processing limitation | Platform voluntarily restricts processing while dispute is open. Status: PLATFORM_EXTENSION. No 30-day clock applies — handle per internal SLA (target: 14 days). |
| PORTABILITY | *(Anticipated under future DPDP Rules — not yet in force)* | Yes when notified by MEITY | Technically infeasible | Machine-readable structured format (JSON). Includes exam data, performance history. Currently accepted as goodwill; will become mandatory on Rules notification. |
| GRIEVANCE | §13 — Right to Grievance Redressal | Yes — respond within 30 days | Grievance not substantiated after review | If unresolved after 30 days → DPO must log formal Data Protection Board complaint in `regulatory_filing` (N-04) as `filing_type='DPB_COMPLAINT'`. |
| NOMINATION | §14 — Right to Nominate | Yes if valid documentation | Invalid nomination form; no proof of incapacity or death | Requires: death certificate OR court incapacity order (PDF upload in DSR drawer). Nominee identity proof mandatory. Legal Officer must co-approve resolution. Nominee exercises ALL §11–§13 rights on behalf of deceased/incapacitated principal. |

**Validation rules by type:**
- **ERASE + children's data:** Mandatory DPO review — cannot auto-close. Children's data erasure creates `legal_compliance_deadline` entry ("Child erasure review — DSR-[id]") in N-07.
- **NOMINATION:** `dpdp_dsr.supporting_documents` field required (file upload in drawer). Cannot be resolved without Legal Officer co-approval.
- **GRIEVANCE:** If unresolved after 30 days → DPO must log a formal Data Protection Board complaint in `regulatory_filing` (N-04) as `filing_type='DPB_COMPLAINT'`.
- **RESTRICT:** Not a statutory right. DPO discretion. Create note in audit log explaining basis for accepting/rejecting restriction.
- **Duplicate guard:** Two open DSRs of same type for same email → DPO notified; second DSR linked to first via `dpdp_dsr.related_dsr_id`.

**Minor/child DSR special handling:**
When `requester_role = 'STUDENT'` and `request_type IN ('ERASE', 'CORRECT')`:
- New DSR modal shows additional field: "Is requester under 18 years of age? ● Yes ○ No ○ Unknown"
- If Yes: `dpdp_dsr.is_requester_minor = true`; automatically triggers `is_children_data = true`; creates N-07 deadline "Child DSR review — DSR-[id]"; mandatory DPO manual review (cannot be delegated to Analyst)
- If institution type = SCHOOL: default warning banner "Requester is likely a minor based on institution type — please verify age"
- **Parent/guardian consent:** For ERASE requests where `is_requester_minor=true`, resolution cannot proceed until parent/guardian email verified. [Verify Parent Email] button in DSR Detail Drawer sends a verification code. Guardian must reply with code + explicit consent statement. Audit log records: "Resolution approved by parent/guardian on [date] from IP [ip]."
- Toast on minor erasure resolution: "DSR-[id] resolved with verified parental consent."

---

### Breach Root Cause Workflow

**On incident creation:** `root_cause` field is NULL; Breach Detail Drawer shows `[under investigation]`.

**During investigation:** DPO (#76) or Security Engineer (#16) can update root_cause via [Update Root Cause] inline edit button in the Breach Detail Drawer. Each update creates an audit log entry.

**On [Resolve Breach]:** Server-side validation — if `root_cause IS NULL OR LENGTH(root_cause) < 50`: 400 error + toast "Enter root cause analysis (min 50 characters) before resolving."

**Root cause examples (reference taxonomy):**
- Compromised API key / credential exposure
- Unpatched software vulnerability (CVE reference if applicable)
- Misconfigured S3 bucket / storage exposure
- Insider access abuse
- Third-party sub-processor breach
- Social engineering / phishing

**Severity classification matrix (for incident creation):**
| Severity | Trigger | Mandatory action |
|---|---|---|
| LOW | < 100 records; no sensitive data; no children's data | DPDP authority notification at DPO discretion |
| MEDIUM | 100–10,000 records; personal data only | CERT-In report; DPDP authority if breach is "likely to affect rights of data principals" |
| HIGH | 10,000–500,000 records; OR any sensitive/children's data | CERT-In 6h + DPDP authority 72h mandatory |
| CRITICAL | > 500,000 records; OR financial data exposed; OR children's data at scale | CERT-In 6h + DPDP authority 72h + institution notification "without delay" + CEO notification |

---

### Breach-to-DSR Linkage

DSR records are NOT auto-created when a breach is logged — the DPDP Act imposes a separate obligation (breach notification to authority) from the right of individuals to submit DSRs.

**Linkage model:**
- `dpdp_dsr.related_breach_incident_id` (nullable FK) — set when a data subject submits a DSR specifically arising from a breach notification
- `dpdp_breach_incident.related_dsr_ids` (JSON array) — all DSRs raised in connection with this breach

**In DSR Detail Drawer:** If `related_breach_incident_id` is set → "[View Related Breach: BRN-2026-001 →]" link appears in Details tab.

**In Breach Detail Drawer:** Count shown: "N DSRs raised in connection with this breach." with [View DSRs →] link.

**Audit trail:** Both records maintain separate timelines. Breach RESOLVED does not auto-close related DSRs — each DSR must be resolved independently within its own 30-day clock.

---

### New DSR Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Log New Data Subject Request                                    │
├──────────────────────────────────────────────────────────────────┤
│  Institution*   [Search institution...                    ]      │
│  Request type*  [Erasure (Right to Erase)               ▼]       │
│  Requester name*  [                                      ]       │
│  Requester email*  [                                     ]       │
│  Requester role*  [Student                              ▼]       │
│  Raised at*  [___ / ___ / _____]  (default: today)              │
│  Request details*  [                                             │
│                                                                  │
│                                                                  ]│
│  Received via:  ● Email  ○ Portal  ○ Written letter  ○ Other    │
│                                                                  │
│  Due date (computed): 13 Apr 2026 (30 days from raised_at)       │
│                                                                  │
│  [Cancel]                              [Log Request]             │
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Institution: required; must be active
- Request type: required
- Requester name: required; min 2 chars
- Requester email: required; valid email
- Requester role: required
- Raised at: required; cannot be future date
- Request details: required; min 20 chars
- Duplicate check: warns (does not block) if open DSR exists for same email + type

POST to `/legal/privacy/dsr/create/`. Sets `status='OPEN'`, `due_at = raised_at + 30 days`. Auto-assigns to DPO (#76).

**Real-time vs submit-time validation:** Email format (on blur), raised_at date format (on change). Required fields + duplicate check at submit-time only.
**Unsaved changes warning:** On modal close with any field filled: "You have unsaved changes. Discard them?" [Cancel] [Discard].

---

## Tab B — Breach Incidents

### Active Breach Alert

When any breach has `status NOT IN ('RESOLVED')`, shows a persistent alert strip above the table:

```
┌────────────────────────────────────────────────────────────────────┐
│  ⚠  ACTIVE BREACH: BRN-2026-001  ·  Severity: HIGH               │
│  Discovered: 21 Mar 2026 01:14 IST  ·  Affected: ~12,000 records  │
│  CERT-In deadline:   21 Mar 2026 07:14 IST   ⏱ 4h 22m remaining  │
│  DPDP authority:     23 Mar 2026 01:14 IST   ⏱ 52h 22m remaining │
│                                          [View Full Detail →]      │
└────────────────────────────────────────────────────────────────────┘
```

Live countdown refreshed every 60 seconds (JS setInterval + HTMX partial). Red background if CERT-In < 2 hours remaining.

---

### Breach Table

| Column | Description |
|---|---|
| Breach ID | `dpdp_breach_incident.breach_code` (e.g. `BRN-2026-001`) |
| Discovered At | Date + time (IST) |
| Nature | UNAUTHORIZED_ACCESS / DATA_LEAK / RANSOMWARE / INSIDER_THREAT / THIRD_PARTY_BREACH / OTHER |
| Severity | CRITICAL (dark red) / HIGH (red) / MEDIUM (amber) / LOW (grey) |
| Affected Records | Estimated count (formatted: "~12,000") |
| CERT-In | ✓ Submitted [ref] or "Pending" (red if > 4h from discovery) |
| DPDP Authority | ✓ Submitted [ref] or "Pending" (red if > 48h from discovery) |
| Institutions Notified | ✓ All / "Partial: N/M" / "Pending" |
| Status | OPEN / UNDER_INVESTIGATION / REPORTED / RESOLVED |
| Actions | [View] [Log Notification] [Close] |

**OPEN + CRITICAL row:** pulsing red left border.

---

### Breach Detail Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  BRN-2026-001  ·  DATA BREACH                       [Close ×]   │
├──────────────────────────────────────────────────────────────────┤
│  Severity: HIGH          Status: UNDER_INVESTIGATION             │
│  Nature: Unauthorized access to student records                  │
│  Discovered: 21 Mar 2026 01:14 IST                               │
│  Discovered by: Kiran Singh (Security Engineer #16)              │
│  Root cause: [under investigation]                               │
├──────────────────────────────────────────────────────────────────┤
│  Affected Data                                                   │
│  Categories: Personal data · Children's data                     │
│  Estimated records: ~12,000 students                             │
│  Affected institutions:  DPS, Victory College, Excel Hub (+7)    │
│  Affected tenant schemas: dps_school, victory_college (+7)       │
├──────────────────────────────────────────────────────────────────┤
│  Notification Timeline                                           │
│                                                                  │
│  ⏱ CERT-In 6h deadline:    21 Mar 2026 07:14 IST  ← 4h 22m left │
│  ✗ CERT-In submitted:      NOT YET              [Log Submission] │
│                                                                  │
│  ⏱ DPDP authority 72h:     23 Mar 2026 01:14 IST  ← 52h left    │
│  ✗ DPDP authority notified: NOT YET             [Log Submission] │
│                                                                  │
│  ✗ Institutions notified:  NOT YET              [Log Submission] │
├──────────────────────────────────────────────────────────────────┤
│  Remediation notes: [                                           ]│
│                                                                  │
│  [Resolve Breach]    (available after all notifications logged)  │
└──────────────────────────────────────────────────────────────────┘
```

**[Log Submission]:** Opens notification log modal — entering authority name, submission reference, submission timestamp, submission method (email/portal/phone), notes. Creates `dpdp_breach_notification_log` record. Updates `dpdp_breach_incident.cert_in_notified_at` / `dpdp_authority_notified_at` / `institutions_notified_at` accordingly.

**[Resolve Breach]:** Available only when all three notification types have been logged. DPO (#76) only. Requires root_cause and remediation_notes fields to be filled. Sets `status='RESOLVED'`, `resolved_at=now()`.

---

### New Breach Incident Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Log Data Breach Incident                                        │
├──────────────────────────────────────────────────────────────────┤
│  Nature*   [Unauthorized Access                           ▼]     │
│  Severity*  ● Low  ● Medium  ● High  ● Critical                  │
│  Discovered at*  [___ / ___ / ____]  [__:__ IST]                 │
│  Discovered by*  [Search user...                          ]      │
│  Affected data categories  [☐ Personal  ☐ Sensitive  ☐ Children] │
│  Estimated affected records*  [                          ]       │
│  Affected institution IDs  [Search and add institutions...  ]    │
│  Initial incident description*  [                               │
│                                                                  ]│
│                                                                  │
│  CERT-In 6h deadline: [computed from discovered_at]             │
│  DPDP authority 72h deadline: [computed from discovered_at]     │
│                                                                  │
│  [Cancel]                              [Create Incident]         │
└──────────────────────────────────────────────────────────────────┘
```

Available to: Security Engineer (#16) and DPO (#76). POST to `/legal/privacy/breaches/create/`. On creation, immediately triggers a real-time notification to DPO (#76) and Legal Officer (#75) via Django Channels.

---

## Tab C — Consent Coverage

### Consent Trend Chart

Line chart — 12 months of overall consent coverage %.

- **Line:** consent_coverage_pct (0–100%)
- **Reference line:** 95% target (dashed green)
- **X-axis:** month labels
- **Y-axis:** 0–100%
- **Hover tooltip:** month · consented users · total users · coverage % · consent policy version active

---

### Consent Coverage Table

Per-institution consent coverage, sortable by coverage % (lowest first by default — surfaces institutions needing attention).

| Column | Description |
|---|---|
| Institution | Name + type badge |
| Total Users | `dpdp_consent_record.total_users` for that institution |
| Consented | `dpdp_consent_record.consented_users` |
| Coverage % | `(consented / total) × 100`. Red if < 80%, amber if 80–94.9%, green if ≥ 95% |
| Consent Version | Policy version they consented to (e.g. `v2.0`). Amber if not on latest version |
| Last Consent Activity | Most recent consent recorded (relative date) |
| Actions | [View Details] [Re-consent Campaign] |

**[Re-consent Campaign]:** DPO (#76) only. Triggers institution admin notification asking them to prompt users to re-consent to the latest policy version. POST to `/legal/privacy/consent/reconsent-campaign/`.

Paginated: 50 rows per page. Filter: institution type, coverage bucket (< 80% / 80–94% / ≥ 95%), consent version.

---

## Tab D — Data Flow Register

### Purpose

Documents all personal data flows within the EduForge platform as required by DPDP Act 2023 Article 8(6) and for maintaining an internal Records of Processing Activities (ROPA). At 2,050 institutions and 7.6M users, understanding where data moves is critical for responding to erasure requests and conducting Privacy Impact Assessments.

### Data Flow Table

| Column | Description |
|---|---|
| Flow ID | `dpdp_data_flow.reference` (e.g. `DF-2026-042`) |
| Data Category | Personal / Sensitive / Children's / Aggregate/Anonymised |
| From System | Source service (e.g. `exam_engine`, `notification_service`) |
| To System / Processor | Destination or sub-processor name |
| Purpose | Free text (e.g. "SMS OTP delivery via DLT") |
| Legal Basis | Consent / Contract / Legal Obligation / Legitimate Interest |
| Sub-processor | Name (links to N-06 sub-processor agreement) |
| Retention Period | Days / indefinite |
| Last Reviewed | Date. Amber if > 12 months ago |
| Actions | [View] [Edit] [Mark Reviewed] |

**[+ Add Data Flow]:** DPO (#76) and Legal Officer (#75).
**[Edit]:** DPO (#76) only.
**[Mark Reviewed]:** DPO (#76) and Legal Officer (#75). Updates `last_reviewed_at=now()`.

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| DSR table | No DSRs match filters | "No data subject requests found." with [Clear Filters] button |
| DSR table (no open DSRs at all) | All resolved | "All data subject requests resolved." with green checkmark |
| Breach table | No breaches ever | "No breach incidents recorded." with green shield icon |
| Consent table | No data | "Consent records not yet initialised." |
| Data flow register | Empty | "No data flows documented. Add your first data flow." with [+ Add Data Flow] |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| DSR logged | "DSR-[id] created. Due: [due_at]." | Blue |
| DSR resolved | "DSR-[id] resolved. Confirmation email sent to requester." | Green |
| DSR rejected | "DSR-[id] rejected. Rejection notice sent." | Amber |
| Breach created | "⚠ Breach BRN-[id] created. CERT-In due: [time]." | Red (critical) |
| CERT-In submission logged | "CERT-In submission recorded. Reference: [ref]." | Green |
| DPDP authority notification logged | "DPDP authority notification recorded. Reference: [ref]." | Green |
| Breach resolved | "Breach BRN-[id] marked resolved." | Green |
| Re-consent campaign triggered | "Re-consent campaign sent to [institution]." | Blue |

---

## Authorization

**Route guard:** `@division_n_required(allowed_roles=[75, 76, 16, 104, 10])` with tab-level restrictions.

| Scenario | Behaviour |
|---|---|
| Security Engineer (#16) | Can only access Breach tab; DSR/Consent/DataFlow tabs return 403 |
| Platform Admin (#10) | Read-only on Consent tab only |
| Data Compliance Analyst (#104) | Read-only on DSR tab and Consent tab; no Breach or DataFlow access |
| New breach creation | Security Engineer (#16) and DPO (#76) only |
| DSR resolution / rejection | DPO (#76) only |
| Export CSV | DPO (#76) and Legal Officer (#75) only |

---

## Role-Based UI Visibility Summary

| Element | 75 Legal | 76 DPO | 16 Security Eng. | 10 Platform Admin | 104 Analyst |
|---|---|---|---|---|---|
| DSR tab (full) | Yes | Yes | No | No | Read-only |
| DSR — Create DSR | No | Yes | No | No | Yes (triage log) |
| DSR — Resolve/Reject | No | Yes | No | No | No |
| Breach tab | Yes (read) | Yes (full) | Yes (create + log) | No | No |
| Breach — Create incident | No | Yes | Yes | No | No |
| Consent tab | Yes (read) | Yes (full) | No | Yes (read) | Yes (read) |
| Re-consent campaign | No | Yes | No | No | No |
| Data flow register | Yes (read) | Yes (full) | No | No | No |
| Export CSV | Yes | Yes | No | No | No |
| [?nocache=true] | Yes | Yes | No | No | No |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| DSR table (paginated, 25 rows) | < 600ms P95 | Index on `(status, due_at)` |
| Breach alert banner update | < 500ms (1 min auto-refresh) | Must be fast — clock is running |
| Consent coverage table (2,050 rows, paginated 50) | < 800ms P95 | Pre-aggregated by institution nightly |
| Export CSV (all DSRs) | < 20s | Synchronous up to 500 rows; async Celery task beyond |

---

## Background Tasks

**Task N-3 — DSR SLA Monitor (every 4 hours):**
- Scans `dpdp_dsr` WHERE `status IN ('OPEN','IN_PROGRESS') AND due_at <= today+3d`
- Sends email alert to DPO (#76) with list of at-risk DSRs
- Creates entries in `legal_compliance_deadline` for calendar N-07

**Task N-4 — Consent Coverage Snapshot (daily, 02:00 IST):**
- Aggregates consent records per institution into `dpdp_consent_snapshot` for trend chart
- Flags institutions where coverage dropped > 5% since last snapshot (sends alert to DPO)

**Keyboard shortcuts (N-03):**

| Key | Action |
|---|---|
| `g` `l` | Go to Legal Dashboard (N-01) |
| `g` `d` | Go to Data Privacy / DPDP (this page) |
| `1` | Switch to DSR tab |
| `2` | Switch to Breach Incidents tab |
| `3` | Switch to Consent Coverage tab |
| `4` | Switch to Data Flow Register tab |
| `n` | Open New DSR modal (DPO only) |
| `/` | Focus search input |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |

**Task N-5 — Breach Deadline Monitor (every 15 minutes):**
- Checks all active breach incidents for approaching CERT-In (6h) and DPDP authority (72h) deadlines
- Sends escalating notifications: DPO at T-2h (CERT-In), DPO+Legal Officer at T-30min
- Creates audit log entry for each notification sent
