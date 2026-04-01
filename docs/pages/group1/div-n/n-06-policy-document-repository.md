# N-06 — Policy & Document Repository

**Route:** `GET /legal/documents/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Legal Officer (#75), DPO (#76)
**Also sees:** Contract Coordinator (#103) — contract templates (read-only); Regulatory Affairs Exec (#77) — regulatory filing documents (read-only); All EduForge staff — public-facing policies (view only, via separate read-only endpoint)

---

## Purpose

Version-controlled repository for all legal and compliance documents. At 2,050 institutions and 7.6M users, a single published Terms of Service (ToS) or Privacy Policy applies uniformly but must be versioned, audited, and re-accepted when materially changed. Three separate ToS variants exist (School / College / Coaching Centre) because the data categories processed for hosteler students in schools differ from coaching centre adult students. The DPO uses this to maintain the sub-processor register required under DPDP Act §8(6). Legal Officer uses it to manage contract templates that flow into N-02. When a new policy version is published, the platform triggers a re-acceptance workflow for all affected institution users on next login.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `legal_policy_document` counts by type/status | 30 min |
| Document table | `legal_policy_document` JOIN `user` (authored_by, approved_by) | 10 min |
| Version history (per document) | `legal_policy_document` WHERE document_family_id = ? ORDER BY version_number DESC | 5 min |
| Sub-processor register | `dpdp_sub_processor` JOIN `legal_policy_document` (DPA template) | 30 min |
| Publication impact | `institution_tos_acceptance` pending re-acceptance count | 15 min |
| Contract template library | `legal_contract_template` WHERE status='ACTIVE' | 30 min |
| Document detail | `legal_policy_document` single row + `legal_document_review_log` | no cache |

Cache keys scoped to `(user_id, document_type_filter)`. `?nocache=true` for Legal Officer (#75) and DPO (#76).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?tab` | `policies`, `templates`, `sub_processors`, `annual_reports` | `policies` | Active tab |
| `?doc_type` | `tos`, `privacy_policy`, `dpa`, `cookie_policy`, `internal_template`, `all` | `all` | Filter by document type |
| `?applicable_to` | `school`, `college`, `coaching`, `group`, `all`, `platform` | `all` | Filter by applicability |
| `?status` | `draft`, `under_review`, `approved`, `published`, `superseded`, `all` | `all` | Filter by document status |
| `?q` | string | — | Search document name, version label |
| `?sort` | `updated_at_desc`, `version_desc`, `doc_type`, `status` | `updated_at_desc` | Table sort |
| `?page` | integer | `1` | Server-side pagination |
| `?nocache` | `true` | — | Bypass Memcached (Legal Officer + DPO only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Auto-Refresh | Target ID |
|---|---|---|---|---|
| KPI strip | `?part=kpi` | Page load | 30 min | `#n6-kpi-strip` |
| Document table | `?part=table` | Page load + tab/filter/sort/page change | — | `#n6-doc-table` |
| Sub-processor register | `?part=sub_processors` | Tab=sub_processors | 30 min | `#n6-sub-processors` |
| Publication impact panel | `?part=pub_impact` | Page load | 15 min | `#n6-pub-impact` |

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Policy & Document Repository  [Search... 🔍]   [+ New Document]  │
├────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (4 tiles)                                               │
├────────────────────────────────────────────────────────────────────┤
│  [Policies & ToS] [Contract Templates] [Sub-Processors] [Reports] │
├────────────────────────────────────────────────────────────────────┤
│  FILTER ROW                                                        │
│  DOCUMENT TABLE + PAGINATION                                       │
├────────────────────────────────────────────────────────────────────┤
│  PUBLICATION IMPACT PANEL                                          │
└────────────────────────────────────────────────────────────────────┘
```

---

## Components

### KPI Strip (4 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 12           │ │ 3            │ │ 8            │ │ 2            │
│ Published    │ │ Under Review │ │ Sub-Processors│ │ Pending      │
│ Documents    │ │              │ │ Registered   │ │ Re-acceptance │
│ (current ver)│ │ 1 DPO review │ │ 5 active DPAs│ │ (2 instit.)  │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Tile 1 — Published Documents:** `COUNT(legal_policy_document) WHERE status='PUBLISHED'`. Sub-label: "current version" count. Clicking → `?status=published`.

**Tile 2 — Under Review:** `COUNT(legal_policy_document) WHERE status='UNDER_REVIEW'`. Sub-label: which type needs DPO review (for DPDP-related documents). Amber if any > 14 days in review state.

**Tile 3 — Sub-Processors:** `COUNT(dpdp_sub_processor) WHERE status='ACTIVE'`. Sub-label: "N active DPAs" = count with valid DPA. Clicking → switches to Sub-Processors tab.

**Tile 4 — Pending Re-acceptance:** `COUNT(institution) WHERE tos_re_acceptance_required=true`. Shows number of institutions whose users need to re-accept updated policies on next login. Green if 0 (all accepted). Amber if > 0.

---

### Tab A — Policies & ToS

#### Document Table

Sortable, paginated (25 per page).

| Column | Description |
|---|---|
| Document Name | Descriptive name (e.g. "Terms of Service — School Institutions v3.2") |
| Type | ToS / Privacy Policy / DPA Template / Cookie Policy / Other |
| Applicable To | ALL / SCHOOL / COLLEGE / COACHING / GROUP (badges) |
| Version | `version_label` (e.g. `v3.2`) |
| Status | DRAFT (grey) / UNDER_REVIEW (amber) / APPROVED (blue) / PUBLISHED (green) / SUPERSEDED (strikethrough grey) |
| Effective From | Date (for PUBLISHED/SUPERSEDED) |
| Authored By | Avatar + name |
| Approved By | Avatar + name or "Pending" |
| Last Updated | Relative date |
| Actions | [View] [Edit Draft] [Review] [Publish] [New Version] |

**SUPERSEDED row:** grey-50 background, all text in grey-400.
**PUBLISHED row (current version):** green-50 left border.
**UNDER_REVIEW row:** amber-50 background.

**[View]:** Opens Document Detail Drawer.
**[Edit Draft]:** Available only for `status='DRAFT'`. Legal Officer + DPO (for privacy docs) + Contract Coordinator (for templates only).
**[Review]:** Opens Review Modal. DPO (#76) for Privacy Policy/DPA/Cookie Policy; Legal Officer (#75) for ToS/other.
**[Publish]:** Opens Publish Modal. Legal Officer (#75) required for all types; DPO (#76) must co-approve Privacy Policy and DPA.
**[New Version]:** Creates a new `DRAFT` document record with `version_number = current + 0.1 minor` or `current + 1.0 major` (selector in modal). Clones current content. Legal Officer (#75) only.

---

### Document Detail Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  Terms of Service — School Institutions                [Close ×] │
│  v3.2  ·  PUBLISHED  ·  Effective: 1 Jan 2026                   │
├──────────────────────────────────────────────────────────────────┤
│  Type: Terms of Service           Applicable to: SCHOOL          │
│  Authored by: Arjun M. (Legal Officer)  12 Dec 2025              │
│  Reviewed by: Priya DPO (DPO)           18 Dec 2025              │
│  Approved by: Arjun M. (Legal Officer)  20 Dec 2025              │
│  Published by: Arjun M. (Legal Officer) 1 Jan 2026               │
├──────────────────────────────────────────────────────────────────┤
│  Changelog summary:                                              │
│  "Added DPDP Act 2023 data processing clauses (§4, §8). Updated  │
│  data retention schedule to 3 years post-institution exit."      │
├──────────────────────────────────────────────────────────────────┤
│  Institution acceptance:                                         │
│  1,000 school institutions affected                              │
│  All accepted: 998/1,000 (99.8%)                                 │
│  Pending re-acceptance: 2 institutions                            │
├──────────────────────────────────────────────────────────────────┤
│  [Download PDF]   [View Raw Content]   [Create New Version]      │
│  [View Version History]                                          │
└──────────────────────────────────────────────────────────────────┘
```

Tabs:
1. **Details** (default): As above
2. **Version History:** All versions of this document family, sortable by version number
3. **Audit Log:** All status changes, reviews, approvals, publications with actor + timestamp
4. **Acceptance Report:** For published ToS/Privacy Policy — institution-by-institution acceptance status

---

### New Document / New Version Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  New Document Version                                            │
├──────────────────────────────────────────────────────────────────┤
│  Based on: ToS — School Institutions v3.2                        │
│  New version type:  ● Minor (v3.3)  ○ Major (v4.0)              │
│  New version label: [v3.3                                 ]      │
│  Document name: [Terms of Service — School Institutions v3.3]   │
│  Changelog summary*  [                                           │
│    Briefly describe what changed from v3.2...            ]       │
│  Effective from*  [___ / ___ / _____]                            │
│  Review required from:  ☑ Legal Officer  ☑ DPO (required for ToS)│
│                                                                  │
│  [Cancel]                              [Create Draft]            │
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Version label: required; must follow semver-like pattern (e.g. `v3.3`); must be > current version
- Changelog summary: required; min 20 chars
- Effective from: required; cannot be more than 30 days in the past

POST to `/legal/documents/new-version/`. Creates `legal_policy_document` with `status='DRAFT'`, `document_family_id` = same as source.

---

### Review Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Review — ToS School v3.3  (Draft)                               │
├──────────────────────────────────────────────────────────────────┤
│  Reviewer role: DPO (required for ToS with data processing terms)│
│                                                                  │
│  Review outcome:  ● Approve  ○ Return for revision               │
│  Review notes*  [                                                │
│                                                                  ]│
│  If returning: revision instructions*  [                        ]│
│                                                                  │
│  [Cancel]                              [Submit Review]           │
└──────────────────────────────────────────────────────────────────┘
```

POST to `/legal/documents/{id}/review/`. Updates `status='APPROVED'` (if approved) or `status='DRAFT'` (if returned). Creates `legal_document_review_log` entry.

---

### Publish Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Publish ToS — School Institutions v3.3                          │
├──────────────────────────────────────────────────────────────────┤
│  Status check:                                                   │
│  ✓ Legal Officer review: Approved (Arjun M., 19 Jan 2026)        │
│  ✓ DPO review: Approved (Priya DPO, 20 Jan 2026)                 │
│                                                                  │
│  Effective from: 1 Feb 2026 (as set during draft creation)       │
│                                                                  │
│  Publication impact:                                             │
│  This will affect 1,000 school institution users.               │
│  On publish, re-acceptance will be required for all school        │
│  institution admin users on their next login.                    │
│                                                                  │
│  Previous version (v3.2) will be marked SUPERSEDED.             │
│                                                                  │
│  Type "PUBLISH" to confirm:  [                        ]          │
│                                                                  │
│  [Cancel]                              [Publish]                 │
└──────────────────────────────────────────────────────────────────┘
```

POST to `/legal/documents/{id}/publish/`. Atomically:
1. Sets this document `status='PUBLISHED'`, `published_at=now()`
2. Sets previous PUBLISHED version of same family → `status='SUPERSEDED'`, `superseded_at=now()`
3. Sets `institution_tos_acceptance.re_acceptance_required=true` for all affected institutions
4. Queues Celery task N-8 to notify institution admins of updated ToS

---

### Tab B — Contract Templates

Shows `legal_contract_template` records. Used by Contract Coordinator in N-02.

| Column | Description |
|---|---|
| Template Name | e.g. "Master Service Agreement v2.1" |
| Contract Type | MSA / DPA / SLA / NDA / MoU |
| Version | e.g. `v2.1` |
| Status | DRAFT / ACTIVE / ARCHIVED |
| Effective From | Date |
| Active Contracts Using | `COUNT(legal_contract) WHERE template_id = this.id AND status='ACTIVE'` |
| Actions | [View] [New Version] [Archive] |

**[Archive]:** Legal Officer (#75) only. Available only if "Active Contracts Using" = 0 (cannot archive a template in active use). Shows confirmation: "This template will be unavailable for new contracts. Existing contracts are unaffected."

---

### Tab C — Sub-Processor Register

Required under DPDP Act §8(6): data fiduciaries must maintain a record of all data processors (sub-processors) they engage. EduForge as data processor must maintain this register and publish a list to data principals on request.

| Column | Description |
|---|---|
| Sub-Processor Name | Company name |
| Service | What data processing they perform (e.g. "SMS OTP delivery", "Cloud hosting", "Email delivery") |
| Data Categories | Personal / Sensitive / Children's (badges) |
| Country | India / USA / EU / Other |
| DPA Status | ACTIVE (green) / EXPIRED (red) / DRAFT (grey) / NONE (red) |
| DPA Expiry | Date or "No DPA" |
| Last Security Review | Date. Red if > 12 months ago |
| Contact | Primary contact email |
| Actions | [View DPA] [Edit] [Deactivate] |

**[+ Add Sub-Processor]:** DPO (#76) only. Opens modal.
**[View DPA]:** Links to DPA document in this repository.
**[Deactivate]:** DPO (#76) only. Marks sub-processor as INACTIVE — triggers alert to evaluate contract obligations.

Current sub-processors (illustrative):

| Processor | Service | Data |
|---|---|---|
| AWS (Amazon Web Services) | Cloud hosting, RDS, Lambda, S3 | Personal, Sensitive, Children's |
| Twilio / Exotel | WhatsApp Business API | Personal |
| Razorpay | Payment processing | Financial personal data |
| Firebase / FCM | Push notifications | Personal (device tokens) |
| Kaleyra / Gupshup | SMS OTP (TRAI DLT) | Personal |
| Cloudflare | CDN, WAF | Technical (no personal data in transit — encrypted) |
| SendGrid | Transactional email | Personal (email addresses) |
| DigiSign | E-signature | Personal, identity documents |

**International transfer compliance:** DPDP Act §16 restricts cross-border data transfers. Flag shown (⚠) for sub-processors in countries not on MEITY's approved list. DPO required to document transfer safeguards.

---

### Tab D — Annual Reports

Archive of all annual compliance reports:
- Annual POCSO Reports (from N-05)
- Annual Data Protection Report (DPO's assessment)
- Annual Legal Compliance Certificate (Legal Officer)
- Annual CERT-In Cybersecurity Report

Stored as PDF files with access logging. View/download available to Legal Officer (#75) and DPO (#76) only.

---

### Publication Impact Panel

Below the document table. Shows current re-acceptance status:

```
  Re-acceptance pending:  2 institutions

  Delhi Coaching Hub    ToS — Coaching v2.1   Published: 1 Jan 2026   Not yet accepted
  Excel Institute       ToS — Coaching v2.1   Published: 1 Jan 2026   Not yet accepted

  [Send Reminder to Pending] (Legal Officer only)
```

[Send Reminder]: Sends email to institution admin(s) via Notification Manager (F-06) asking them to log in and accept the updated terms.

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| Document table | No documents match filters | "No documents found." with [Clear Filters] |
| Sub-processor register | No sub-processors | "No sub-processors registered. Add your first sub-processor." |
| Publication impact panel | All institutions have accepted | "All institutions have accepted current policy versions." with green checkmark |
| Version history | Only one version exists | "This is the original version." |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Draft created | "Draft [name] v[ver] created." | Blue |
| Review submitted — approved | "[doc name] approved by [reviewer role]." | Green |
| Review submitted — returned | "[doc name] returned for revision." | Amber |
| Document published | "[doc name] v[ver] published. Previous version superseded." | Green |
| Re-acceptance reminders sent | "Reminder sent to [N] institutions." | Blue |
| Sub-processor added | "[name] added to sub-processor register." | Blue |
| Template archived | "Template [name] archived." | Amber |

---

## Authorization

**Route guard:** `@division_n_required(allowed_roles=[75, 76, 77, 103])` with tab-level restrictions.

| Scenario | Behaviour |
|---|---|
| Regulatory Affairs Exec (#77) | Read-only on Annual Reports tab (regulatory filing documents) only |
| Contract Coordinator (#103) | Read-only on Contract Templates tab only; cannot create/archive templates |
| Publish action | Legal Officer (#75) required; DPO (#76) co-approval required for Privacy Policy/DPA |
| Archive template | Legal Officer (#75) only; blocked if template has active contracts |
| Sub-processor management | DPO (#76) full; Legal Officer (#75) read-only |

---

## Role-Based UI Visibility Summary

| Element | 75 Legal | 76 DPO | 77 Reg. Affairs | 103 Contract Coord. |
|---|---|---|---|---|
| Policies & ToS tab (full) | Yes | Yes | No | No |
| Create new document version | Yes | Privacy/DPA only | No | No |
| Review documents | Yes (ToS/other) | Yes (privacy docs) | No | No |
| Publish documents | Yes | Co-approve privacy | No | No |
| Contract templates tab | Yes (full) | No | No | Yes (read) |
| Archive template | Yes | No | No | No |
| Sub-processor register | Yes (read) | Yes (full) | No | No |
| Annual reports tab | Yes | Yes | Yes (read) | No |
| Send re-acceptance reminders | Yes | No | No | No |
| [?nocache=true] | Yes | Yes | No | No |

---

## Background Tasks

**Task N-8 — ToS Publication Notifier (triggered on document publish):**
- Sends email to all institution admin users of affected institution type
- Email includes: what changed (changelog summary), link to new policy, and information that re-acceptance is required on next login
- Creates `legal_document_notification_log` records

**Task N-9 — Document Review Reminder (weekly, Monday 09:00 IST):**
- Scans `legal_policy_document` WHERE `status='UNDER_REVIEW' AND review_started_at <= today-7d`
- Sends email to assigned reviewer: "Document [name] has been awaiting your review for [N] days."

**Task N-10 — Annual Document Audit (annually, 1 April):**
- Checks all PUBLISHED documents for policy review dates (annual review required per internal governance)
- For each document where `published_at < today-365d AND status='PUBLISHED'`: sets amber "⚠ Review due" badge in document table
- Creates `legal_compliance_deadline` entries for each document due for review (category: POLICY, visible in N-07)
- Sends report to Legal Officer (#75) and DPO (#76) listing all documents pending annual review

**Task N-11 — Sub-Processor DPA Expiration Monitor (daily, 07:00 IST):**
- Scans all `dpdp_sub_processor` WHERE `dpa_expiry_date <= today+90d AND dpa_status='ACTIVE'`
- Sets `dpa_status = 'EXPIRING_SOON'` for those within 90 days
- Sets `dpa_status = 'EXPIRED'` for those where `dpa_expiry_date < today`
- Sends email to DPO (#76): "[N] sub-processor DPAs expiring or expired — action required."
- Creates `legal_compliance_deadline` entries (category: REGULATORY) in N-07 calendar for each

---

## Sub-Processor DPA Lifecycle

Detailed status transitions for sub-processor DPAs (required per DPDP Act §8(6)):

| Status | Condition | UI indicator | Action required |
|---|---|---|---|
| ACTIVE | `dpa_expiry_date >= today+90d` | Green badge | None |
| EXPIRING_SOON | `dpa_expiry_date BETWEEN today AND today+90d` | Amber badge ⚠ | [Renew DPA] button visible |
| EXPIRED | `dpa_expiry_date < today` | Red badge — processing BLOCKED | [Renew DPA] required immediately |
| NONE | No DPA record | Red badge | Cannot process personal data; DPO must negotiate DPA |

**[Renew DPA] action:**
1. Opens modal pre-filled with current sub-processor details
2. DPO uploads new signed DPA (PDF, max 20MB)
3. Sets new `dpa_expiry_date`
4. Updates `dpa_status = 'ACTIVE'`
5. Creates audit log: who renewed, previous expiry, new expiry
6. Sends confirmation email to sub-processor contact
7. Clears N-07 calendar deadline for this sub-processor

**Processing block:** If `dpa_status = 'EXPIRED'`, application-level middleware prevents any API call to that sub-processor from completing. Error message to operational staff: "Sub-processor [name] DPA expired. Contact DPO to renew before resuming use."

---

## ToS Re-acceptance Workflow (Institution Users)

When a new ToS version is published for a given institution type, all institution admin users of that type must re-accept on their next login.

**User-side flow (institution admin on login):**
1. Non-dismissible modal overlay appears before dashboard loads
2. Header: "Updated Terms of Service — action required"
3. Displays: previous version ("v3.1") → new version ("v3.2"), effective date, and changelog summary
4. [Download PDF] link to full new ToS document
5. Buttons: **[Decline]** (red-outlined) and **[Accept]** (green solid)

**Accept:**
- `institution_tos_acceptance.accepted = true`, `accepted_at = now()`, `re_acceptance_required = false`
- Acceptance IP + user agent stored in audit log
- User proceeds to their dashboard
- Toast: "Terms accepted. Thank you."

**Decline:**
- `institution_tos_acceptance.accepted = false` logged (decline date + reason if provided)
- User sees: "You must accept the updated Terms of Service to continue using EduForge. Please contact EduForge support if you have questions."
- Modal reappears on every subsequent login until accepted
- After **7 days of decline without contact**: Contract Coordinator (#103) receives alert to follow up
- After **14 days**: Legal Officer (#75) receives escalation + option to suspend institution access via [Suspend Access] (which routes through Billing Admin #70)

**Audit trail:** All accept/decline events logged in `institution_tos_acceptance` with user_id, institution_id, version, event_type, timestamp, ip_address.

**Reporting:** Legal Officer can view acceptance status per institution in the Document Detail Drawer → Acceptance Report tab (N-06).

---

## Public Policy Publication URLs

All PUBLISHED policy documents are served at public-facing CDN-cached endpoints accessible without authentication:

| Document | Public URL | Applicable To | Updated When |
|---|---|---|---|
| Terms of Service — Schools | `/legal/tos/school/` | School institutions | On each PUBLISHED status update |
| Terms of Service — Colleges | `/legal/tos/college/` | College institutions | On each PUBLISHED status update |
| Terms of Service — Coaching | `/legal/tos/coaching/` | Coaching centres | On each PUBLISHED status update |
| Privacy Policy | `/legal/privacy-policy/` | All institutions + public | On each PUBLISHED status update |
| Cookie Policy | `/legal/cookies/` | All users | On each PUBLISHED status update |
| Sub-processor Register | `/legal/sub-processors/` | Public | Auto-updated from N-06 sub-processor table; refreshed daily |
| Grievance Officer | `/legal/grievance-officer/` | All users | Auto-updated from N-04 MeitY officer record |

**Serving mechanism:** Each public URL renders the latest PUBLISHED document for that type. Content served as static HTML (generated on publish by Task N-8) and cached at CDN level with `Cache-Control: max-age=3600`. On new publish, Task N-8 triggers CDN cache invalidation for that URL.

**Version permalink:** Historical versions accessible at `/legal/tos/school/v3.1/` etc. for legal audit trail. These are immutable once generated.

**Emergency update process:** If a court order or regulatory direction requires immediate ToS amendment outside the normal review cycle:
1. Legal Officer creates a NEW DRAFT with `emergency_update=true` flag
2. Normal review cycle is compressed to 24 hours (both Legal Officer and DPO review same-day)
3. [Publish Emergency] button (Legal Officer only) bypasses the "Type PUBLISH to confirm" step but still requires DPO email confirmation
4. Post-publish: `legal_compliance_deadline` created: "Emergency ToS update — explain regulatory basis within 7 days" in STATUTORY category (N-07)

---

## Unsaved Changes Warning

Applies to all modals and drawers in N-06 (New Document, Review, Publish, Sub-Processor, Template):
- On attempt to close modal/drawer or navigate away with any form field modified from its initial state:
  - Dialog: "You have unsaved changes. Discard them and close?" [Cancel] [Discard changes]
- Implemented via browser `beforeunload` event + HTMX `hx-confirm` on close buttons
- **Exception:** Read-only drawers (version history, audit log) have no unsaved changes warning

---

## Keyboard Shortcuts (N-06)

| Key | Action |
|---|---|
| `g` `l` | Go to Legal Dashboard (N-01) |
| `g` `o` | Go to Policy Repository (this page) |
| `1` | Switch to Policies & ToS tab |
| `2` | Switch to Contract Templates tab |
| `3` | Switch to Sub-Processors tab |
| `4` | Switch to Annual Reports tab |
| `n` | Open New Document Version modal (Legal Officer only) |
| `/` | Focus search input |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |
