# G-03 — Staff BGV Record

> **Route:** `/bgv/staff/{staff_id}/`
> **Division:** G — Background Verification
> **Primary Role:** BGV Executive (40) — full edit on assigned cases; BGV Ops Supervisor (92) — full
> **Supporting Roles:** BGV Manager (39) — full; POCSO Compliance Officer (41) — read on POCSO-flagged records only; Platform Admin (10) — full
> **File:** `g-03-staff-record.md`
> **Priority:** P0 — the authoritative record for one staff member's BGV

---

## 1. Page Name & Route

**Page Name:** Staff BGV Record
**Route:** `/bgv/staff/{staff_id}/`
**Part-load routes:**
- `/bgv/staff/{staff_id}/?part=overview` — overview tab
- `/bgv/staff/{staff_id}/?part=documents` — documents tab
- `/bgv/staff/{staff_id}/?part=vendor` — vendor communication tab
- `/bgv/staff/{staff_id}/?part=history` — verification history tab
- `/bgv/staff/{staff_id}/?part=audit` — audit log tab

---

## 2. Purpose

G-03 is the single source of truth for one staff member's entire BGV lifecycle — current verification status, all documents, vendor submissions, results, and complete audit history. Every significant BGV action happens here or is recorded here.

**Who needs this page:**
- BGV Executive (40) — document upload, vendor submission, result entry
- BGV Ops Supervisor (92) — FLAGGED result review and approval decision
- BGV Manager (39) — escalation review, institution notification decisions
- POCSO Compliance Officer (41) — view POCSO-related verification details when a case is open

---

## 3. Layout

```
┌───────────────────────────────────────────────────────────────────┐
│  Breadcrumb: BGV Queue / {institution_name} / {staff_ref}         │
│  Staff header: {staff_ref} | {role_title} | {institution_name}    │
│  Status badge: [CLEAR] / [DOCUMENTS_REQUESTED] / [VENDOR_SENT]   │
│  POCSO flag badge (red, if active): ⚠️ POCSO FLAG                 │
├───────────────────────────────────────────────────────────────────┤
│  Tabs: Overview | Documents | Vendor Communication | History | Audit │
├───────────────────────────────────────────────────────────────────┤
│  Tab content area                                                 │
└───────────────────────────────────────────────────────────────────┘
```

**Page-level action buttons (top right, role-gated):**
- [Edit Staff Details] — BGV Executive (40) or above only
- [Create Re-Verification] — BGV Ops Supervisor (92), BGV Manager (39)
- [Suspend Staff BGV] — BGV Manager (39) only (marks staff as SUSPENDED — blocks portal access if integrated)
- [Cancel BGV Request] — BGV Ops Supervisor (92), BGV Manager (39) only. Available when `bgv_verification.status NOT IN (COMPLETE, CANCELLED)`. Confirmation modal: "Cancel verification for {staff_ref}? Verification will be marked CANCELLED. Institution admin will be notified. Reason (required, max 300 chars):" — sets `status = CANCELLED`, `final_result = CANCELLED`, logs to audit. `bgv_staff.bgv_status` reverts to previous value (NOT_INITIATED for first verification; CLEAR if prior CLEAR existed). Note: if POCSO flag was set before cancellation, POCSO case remains open — cancellation does not close POCSO cases.

---

## 4. Staff Header

Persistent across all tabs. Shows at a glance the staff member's identity and current status.

| Field | Notes |
|---|---|
| Staff Ref | `bgv_staff.staff_ref` — e.g. `BGV-SCH001-0042` |
| Full Name | Decrypted and shown only to BGV Executive (40), Supervisor (92), Manager (39). POCSO Compliance Officer (41) sees `[Protected — DPDPA]`. Platform Admin (10) sees full name. |
| Role Title | e.g. "Mathematics Teacher" |
| Department | e.g. "Academic" |
| Institution | Institution name + type badge |
| Date of Joining | — |
| Minor Access | "Yes" (critical marker) / "No" |
| BGV Status | Current `bgv_staff.bgv_status` as coloured pill |
| Verification Validity | If CLEAR: "Valid until {expiry_date}" (green) / "Expired {date} ago" (red) |
| Active POCSO Case | If `bgv_pocso_case` linked to this staff with open status: red banner "Active POCSO Case: {case_ref} — [View Case →]" |

---

## 5. Tab-Wise Detailed Breakdown

---

### Tab 1 — Overview

Summary of the current active verification and next required action.

#### Section A — Current Verification Status

Timeline stepper showing the current verification's lifecycle:

```
● Initiated → ● Documents Requested → ● Documents Received → ● Vendor Sent → ● Vendor Returned → ● Reviewed → ● CLEAR / FLAGGED
```

Each step shows:
- Status: Complete (✅), Current (🔵), Pending (○), Skipped (—)
- Timestamp when completed
- Who performed the action

#### Section B — Next Action Banner

Contextual call-to-action based on current status.

| Current Status | Banner Content |
|---|---|
| DOCUMENTS_REQUESTED | "⏳ Waiting for documents from institution. [Send Reminder]" |
| DOCUMENTS_RECEIVED | "📋 Documents received. Review checklist and mark ready for vendor. [Go to Documents Tab →]" |
| READY_FOR_VENDOR | "📤 Ready to submit to vendor. [Select Vendor & Submit →]" |
| VENDOR_SENT | "⏳ Awaiting vendor result — sent {N} days ago (SLA: {sla_hours}h). [Poll Status]" |
| VENDOR_RETURNED | "📩 Vendor result received: **{vendor_result}**. [Review & Finalise →]" |
| AWAITING_APPROVAL | "🔄 FLAGGED result submitted for Supervisor review. [Approve / Reject] (Supervisor only)" |
| CLEAR | "✅ Verification CLEAR. Valid until {expiry_date}." |
| FLAGGED | "🚨 FLAGGED — awaiting institution notification from BGV Manager." |

#### Section C — Current Verification Summary Card

| Field | Value |
|---|---|
| Verification ID | UUID (truncated: first 8 chars) |
| Type | INITIAL / RENEWAL / RE_VERIFICATION |
| Initiated By | User name and role |
| Initiated At | Datetime |
| Assigned To | BGV Executive name |
| Vendor | Vendor name or "Not assigned" |
| Vendor Ref | `vendor_request_ref` or "—" |
| SLA Due | `sla_due_at` with countdown or "⚠️ OVERDUE {N}h" |
| Vendor Result | Pending / CLEAR / FLAGGED / INCONCLUSIVE |
| Final Result | Pending / CLEAR / FLAGGED / INCONCLUSIVE / CANCELLED |
| Result Reviewed By | Supervisor name or "—" |

#### Section D — FLAGGED / INCONCLUSIVE Review Panel

Shown only when `vendor_result IN (FLAGGED, INCONCLUSIVE)` and `final_result = PENDING`.

**For BGV Executive (40):**
- Vendor result summary (text from `vendor_result_detail`)
- [Download Vendor Report] (signed R2 URL, 30-min expiry)
- Executive review notes field (required, min 20 chars)
- [Submit for Supervisor Approval] → sets awaiting approval, notifies Supervisor (92)

**For BGV Ops Supervisor (92) — after executive submission:**
- Vendor result detail
- Executive's review notes (read-only)
- Supervisor decision: radio — "Confirm FLAGGED" / "Mark INCONCLUSIVE" / "Override: CLEAR"
- Supervisor decision note (required, min 30 chars — rationale is audited)
- If POCSO offense detected: checkbox "This involves a POCSO Act offense" → `pocso_flag = true` → required fields: Offense Type (text), Offense Date (optional)
- [Approve Decision] → confirmation modal: "You are about to mark {staff_ref} as {decision}. This will trigger institution notification workflow. This action is logged and cannot be undone. Confirm?"

**Approval confirmation modal (400px):**
- Shows: staff ref, institution, decision (FLAGGED/INCONCLUSIVE/CLEAR)
- If FLAGGED: "Institution will be notified by BGV Manager after approval."
- If POCSO flagged: "A POCSO case will be auto-created. POCSO Compliance Officer will be notified immediately."
- [Confirm Approval] / [Cancel]

---

### Tab 2 — Documents

Complete document checklist for the current verification.

#### Document Checklist Table

| Column | Notes |
|---|---|
| Document Type | Required document label (from G-08 config) |
| Required | Yes / No |
| Status | Not Uploaded (grey) / Uploaded (amber) / Verified (green) / Rejected (red) |
| File Name | Original filename |
| Uploaded By | User and datetime |
| Verified | ✅ by {user} on {date} or — |
| Rejection Reason | Shown if rejected |
| Actions | [View] · [Verify] · [Reject] · [Replace] |

**[View]** — opens signed R2 URL in new tab. URLs expire in 30 minutes. If URL is expired, button re-fetches. Access logged in `bgv_audit_log`.

**[Verify]** — marks document as verified. Requires confirmation: "Mark {document_type} as verified?" Available to BGV Executive (40) and above.

**[Reject]** — opens inline rejection form: Rejection Reason (select: EXPIRED · ILLEGIBLE · WRONG_DOCUMENT_TYPE · TAMPERED · OTHER) + notes. Institution notified to re-upload.

**[Replace]** — available only if current document is REJECTED or for documents already uploaded. Prompts new file upload; old file version retained in S3 for audit.

#### Upload New Document

[+ Upload Document] (above table):
- Select document type (dropdown)
- File picker — max 10MB; allowed: PDF, JPG, PNG, WEBP
- Upload progress indicator
- On success: row added to checklist with "Uploaded" status

**"All documents complete" banner:** Shown when all required documents are uploaded AND at least verified = true. Green banner with [Mark Ready for Vendor] CTA.

---

### Tab 3 — Vendor Communication

Record of all vendor interactions for the current verification.

#### Section A — Vendor Submission Log

| Column | Notes |
|---|---|
| Timestamp | Datetime |
| Direction | OUTBOUND (to vendor) / INBOUND (from vendor) |
| Event | e.g. "Initial submission" / "Status poll" / "Webhook received" |
| Vendor Ref | — |
| Status | HTTP status code + result |
| Duration | API call duration in ms |

Drawn from `bgv_vendor_transaction` records for this verification.

#### Section B — Vendor Result Detail

Read-only. Shows `vendor_result_detail` in full. Formatted text block.

[Download Vendor Report PDF] — if `vendor_result_document_url` is set. Signed URL, 30-min expiry.

#### Section C — Poll Vendor Status

Available when `bgv_verification.status = VENDOR_SENT`.

[Poll Vendor Now] — triggers `GET {vendor.api_base_url}/status/{vendor_request_ref}`. Shows result inline. If vendor reports complete, offers [Record Result].

**Manual result entry** (for vendors without webhook support): [Record Vendor Result Manually] — for BGV Ops Supervisor (92) and Manager (39) only. Requires: result (select), result detail (text), and attaching vendor report PDF. All manual entries flagged with `manual_entry = true` in audit log.

---

### Tab 4 — History

All verifications for this staff member, from initial through all renewals and re-verifications.

#### Verification History Table

| Column | Notes |
|---|---|
| Verification ID | Truncated UUID |
| Type | INITIAL / RENEWAL / RE_VERIFICATION |
| Initiated | Date |
| Vendor | Vendor name |
| Final Result | CLEAR / FLAGGED / INCONCLUSIVE / CANCELLED |
| Validity Period | `initiated_at` to `expiry_date` or "N/A" |
| Actions | [View Record →] — opens this tab set for historical verification (read-only) |

**Gap detection:** If gap between two consecutive verifications' validity periods > 0 days: ⚠️ "BGV gap: {N} days unverified between {date} and {date}" — shown inline between relevant rows.

**Current verification** is highlighted with a "CURRENT" badge.

---

### Tab 5 — Audit Log

Immutable trail of every action taken on this staff record and all linked verifications.

#### Audit Table

| Column | Notes |
|---|---|
| Timestamp | Datetime (IST), sortable DESC default |
| Action | e.g. `DOCUMENT_UPLOADED` · `VENDOR_SENT` · `RESULT_RECEIVED` · `FLAGGED_APPROVED` |
| Entity | STAFF / VERIFICATION / DOCUMENT / POCSO_CASE |
| Performed By | User name + role, or "System (Celery)" |
| Change | "{old_value} → {new_value}" JSON summary |
| Note | Optional note attached to action |

Pagination: 25 rows. [Export Audit CSV] (BGV Manager, Platform Admin only).

---

## 6. Data Model Reference

**`bgv_staff`** — master staff record
**`bgv_verification`** — linked by `staff_id`; current = `bgv_staff.current_verification_id`
**`bgv_document`** — linked by `verification_id`
**`bgv_vendor_transaction`** — linked by `verification_id`
**`bgv_pocso_case`** — linked by `staff_id` and `verification_id`
**`bgv_audit_log`** — linked by `entity_id = bgv_staff.id` or `verification_id`

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | BGV Executive (40) (own assigned), Supervisor (92), Manager (39), POCSO Officer (41), Platform Admin (10) |
| Full name decryption | BGV Executive (40), Supervisor (92), Manager (39), Platform Admin (10) |
| POCSO Officer name access | Blocked — sees `[Protected — DPDPA]` |
| POCSO Officer page access | Only for staff records linked to an open POCSO case |
| [Verify Document] | BGV Executive (40) and above |
| [Reject Document] | BGV Executive (40) and above |
| [Submit for Supervisor Approval] | BGV Executive (40) only |
| [Approve Decision] (FLAGGED/INCONCLUSIVE) | BGV Ops Supervisor (92) only |
| [Override: CLEAR] on FLAGGED | BGV Ops Supervisor (92) — logged with mandatory note |
| [Create Re-Verification] | Supervisor (92), Manager (39) |
| [Suspend Staff BGV] | BGV Manager (39), Platform Admin (10) |
| [Export Audit CSV] | BGV Manager (39), Platform Admin (10) |
| [Manual vendor result entry] | Supervisor (92), Manager (39) |
| View Vendor Communication tab | BGV Executive (40) and above (not POCSO Officer) |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| BGV Executive opens record not assigned to them | 403 page: "This verification is assigned to another executive. Contact your Supervisor to reassign." |
| Document R2 URL expired on [View] | Silently re-fetches signed URL. If R2 error: "Document temporarily unavailable. Try again in a moment." |
| Supervisor approves CLEAR override on FLAGGED | Audit log records `CLEAR_OVERRIDE` with mandatory note. Manager (39) notified in-app: "Supervisor overrode FLAGGED to CLEAR for {staff_ref} at {institution}." |
| POCSO flag set mid-approval | If Supervisor checks POCSO flag during approval: confirmation modal adds POCSO-specific language; POCSO case auto-created on confirm. |
| Vendor report PDF missing (URL null) | [Download Vendor Report] button hidden. Warning: "Vendor did not attach a report document. Request report from vendor." |
| Staff record no longer has_minor_access | Yellow info banner: "This staff member's minor access has been removed. BGV is still valid for record-keeping purposes." |
| Verification history shows gap | ⚠️ Gap warning as described in Tab 4. BGV Manager notified. |
| Two supervisors open approval panel simultaneously | Optimistic locking via `bgv_verification.version` field: approval modal fetches current version on open; submit includes version; if version mismatch on save → "This verification was updated by another session since you opened the approval panel. Reload to see latest state." POCSO checkbox conflict (one sets POCSO, other doesn't): reject concurrent submission; user must reload and re-enter. |
| Staff terminated mid-BGV (VENDOR_SENT or earlier) | BGV Executive or Supervisor can [Cancel BGV Request] from Overview tab. Verification status → `CANCELLED`. `bgv_staff.bgv_status` → `NOT_INITIATED`. Audit note required. If POCSO flag detected in a subsequent vendor return (for a cancelled verification) → POCSO case still auto-created regardless of employment status. |
| Re-verification also returns INCONCLUSIVE (second vendor) | BGV Manager (39) must review manually. No third automatic re-verification. Options: [Accept as Inconclusive] (institution notified, staff access at institution's discretion), [Request Third-Party Adjudication] (added to notes — manual process), or [Override: CLEAR] (Supervisor — requires strong documented rationale). |

---

## 9. UI Patterns

### Loading States
- Staff header: shimmer (3 lines + badge)
- Tab content: section-specific skeleton (timeline stepper shimmer for Overview; table row shimmer for Documents)

### Toasts
| Action | Toast |
|---|---|
| Document uploaded | ✅ "Document uploaded — {document_type}" (3s) |
| Document verified | ✅ "Document verified" (3s) |
| Document rejected | ⚠️ "Document rejected — institution notified to re-upload" (4s) |
| Submitted for approval | ✅ "Submitted for Supervisor approval" (4s) |
| Supervisor approves CLEAR | ✅ "Verification marked CLEAR — {staff_ref} expiry: {date}" (5s) |
| Supervisor approves FLAGGED | ⚠️ "FLAGGED — BGV Manager notified for institution action" (5s) |
| POCSO flag auto-creates case | 🚨 "POCSO case created: {case_ref} — POCSO Compliance Officer notified" (6s, persistent until dismissed) |

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full tab layout; documents table 6 columns |
| Tablet | Tabs collapse to dropdown; table reduces to 4 columns |
| Mobile | Read-only view recommended. Actions available but single-column layout. |

---

*Page spec complete.*
*G-03 covers: staff header with DPDPA-safe name handling → 5-tab layout (Overview / Documents / Vendor Communication / History / Audit) → status timeline stepper → contextual next-action banner → document checklist with upload/verify/reject → FLAGGED result review workflow → Supervisor approval gate with POCSO detection → vendor API log → historical verification gap detection → full audit trail.*
