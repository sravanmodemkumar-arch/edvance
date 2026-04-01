# G-02 — Staff Verification Queue

> **Route:** `/bgv/queue/`
> **Division:** G — Background Verification
> **Primary Role:** BGV Executive (40) — main operational workspace; BGV Ops Supervisor (92) — full view + assign
> **Supporting Roles:** BGV Manager (39) — read + assign; Platform Admin (10) — full
> **File:** `g-02-staff-verification-queue.md`
> **Priority:** P0 — BGV Executives live on this page all day

---

## 1. Page Name & Route

**Page Name:** Staff Verification Queue
**Route:** `/bgv/queue/`
**Part-load routes:**
- `/bgv/queue/?part=queue-table` — main queue table (HTMX partial)
- `/bgv/queue/?part=stats-bar` — queue stats bar
- `/bgv/queue/?part=assign-drawer` — assignment drawer partial

---

## 2. Purpose

G-02 is the operational workspace where BGV Executives process incoming BGV requests. It surfaces all verifications that need action, enables document review, vendor submission, and status updates — all without leaving the queue view.

**Who needs this page:**
- BGV Executive (40) — processes own assigned queue; views unassigned items
- BGV Ops Supervisor (92) — assigns verifications to executives; monitors queue health
- BGV Manager (39) — queue overview; can reassign and prioritise

**When is it used:**
- Continuously during working hours — BGV Executives' primary interface
- Morning: Supervisor reviews overnight vendor returns, assigns new items
- Throughout day: Executives process documents, submit to vendor, record results
- End of day: Supervisor checks SLA status, reassigns overdue items

---

## 3. Layout

```
┌───────────────────────────────────────────────────────────────┐
│  Page header: "Staff Verification Queue"   [Create Manual BGV] │
├───────────────────────────────────────────────────────────────┤
│  Stats bar: Total | My Queue | Unassigned | SLA Today | Done  │
├──────────────────────────────────────┬────────────────────────┤
│  Tabs: All | Docs Pending | Ready    │  Filters: Search,      │
│  for Vendor | Vendor Returned |      │  Type, Priority,       │
│  Awaiting Approval | Overdue         │  Institution, Assigned  │
├──────────────────────────────────────┴────────────────────────┤
│  Queue Table (server-side paginated, 25 rows)                 │
│  [ ] Ref | Institution | Type | Priority | Status | SLA | Assign │
├───────────────────────────────────────────────────────────────┤
│  Bulk Action Bar (appears when rows selected):                │
│  [Assign to…] [Mark Docs Received] [Send to Vendor (batch)]  │
└───────────────────────────────────────────────────────────────┘
```

Action drawer slides in from the right when a row is clicked (does not navigate away).

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Stats Bar

Live counters above the queue. Refreshed on page load and via HTMX every 2 minutes.

| Stat | Description | Colour |
|---|---|---|
| Total in Queue | All verifications with `final_result = PENDING` | Neutral |
| My Queue | Assigned to current user | Neutral |
| Unassigned | `assigned_to_id IS NULL` | Amber if > 0 |
| SLA Due Today | `sla_due_at ≤ today 23:59 IST` and still PENDING | Red if > 0, else green |
| Completed Today | `final_result IN (CLEAR, FLAGGED)` and `reviewed_at` date = today | Green |

Stats bar is visible to all roles with queue access. BGV Executive sees counts matching their permission scope.

---

### Section B — Queue Tabs

| Tab | Filter | Badge |
|---|---|---|
| All | All PENDING verifications | Total count |
| Docs Pending | `bgv_verification status = DOCUMENTS_REQUESTED` | Count |
| Documents Received | `status = DOCUMENTS_RECEIVED` — ready for BGV Executive review | Count |
| Ready for Vendor | Documents complete, not yet sent to vendor | Count |
| Vendor Returned | `vendor_returned_at IS NOT NULL` and `final_result = PENDING` — awaiting review | Count |
| Awaiting Approval | `vendor_result IN (FLAGGED, INCONCLUSIVE)` and `reviewed_by_id IS NULL` — Supervisor approval needed | Count — Supervisor (92) and Manager (39) only |
| Overdue | `sla_due_at < now()` and `final_result = PENDING` | Count — red badge |

**BGV Executive (40)** sees only their assigned items in all tabs, plus unassigned items in "Docs Pending" and "Documents Received" tabs (so they can self-assign).

**BGV Ops Supervisor (92)** and **BGV Manager (39)** see all items across all tabs, including an **"Unassigned"** quick-filter button in the filter bar that shows only items where `assigned_to_id IS NULL`.

**Search scope:** Text search queries `bgv_staff.staff_ref` (exact or partial, e.g. `BGV-SCH001`) and institution name. Full name is NOT searchable (DPDPA compliance — full names are encrypted and not indexed for search). BGV Executive search is additionally scoped to their own assigned items.

---

### Section C — Queue Table

| Column | Sortable | Notes |
|---|---|---|
| Checkbox | — | Row selection for bulk actions |
| Staff Ref | No | `bgv_staff.staff_ref` — anonymised e.g. `BGV-SCH001-0042` |
| Institution | Yes | Institution name |
| Type | Yes | SCHOOL / COLLEGE / COACHING |
| Verification Type | No | INITIAL / RENEWAL / RE_VERIFICATION |
| Priority | Yes | CRITICAL (red) · HIGH (orange) · MEDIUM (amber) · LOW (grey) — see priority rules below |
| Status | No | Pill badge: DOCUMENTS_REQUESTED · DOCUMENTS_RECEIVED · READY_FOR_VENDOR · VENDOR_SENT · VENDOR_RETURNED |
| Documents | No | `{received}/{required}` e.g. "3/5" with colour: green if complete, amber if partial, red if 0 |
| SLA | Yes (default: ASC) | Countdown: "2d 4h" remaining or "⚠️ 2h overdue" in red |
| Assigned To | No | Executive name pill or "Unassigned" (amber) |
| Action | — | [Open →] — opens action drawer |

**Priority rules** (system-assigned, not manually editable):
- `CRITICAL`: POCSO flag detected (`pocso_flag = true`)
- `HIGH`: SLA ≤ 24h remaining, or staff with `has_minor_access = true` in active institution (currently running exams)
- `MEDIUM`: RENEWAL type, or `sla_due_at` within 3 days
- `LOW`: INITIAL type, standard SLA timeline

**Default sort:** Priority (CRITICAL first) then SLA ascending.

---

### Section D — Bulk Actions

Appears when ≥ 1 row is selected. Actions apply to all selected rows.

| Action | Available To | Behaviour |
|---|---|---|
| [Assign to…] | Supervisor (92), Manager (39) | Dropdown of BGV Executives; assigns `assigned_to_id`; in-app notification sent to assignee. Confirmation: "Assign {N} verifications to {name}?" |
| [Mark Docs Received] | BGV Executive (40), Supervisor (92) | Sets `status = DOCUMENTS_RECEIVED` for selected verifications at DOCUMENTS_REQUESTED status. Logs to `bgv_audit_log`. |
| [Send to Vendor] | BGV Executive (40), Supervisor (92) | Batch vendor submission modal (see Section E). Only rows at READY_FOR_VENDOR status. |
| [Reassign] | Supervisor (92), Manager (39) | Reassign from one executive to another |

Bulk actions are disabled if selected rows include items in incompatible states (e.g. trying to [Send to Vendor] when some selected rows are not READY_FOR_VENDOR — those are skipped with a warning).

---

### Section E — Action Drawer

Slides in from right (400px width) when [Open →] or row-click is triggered. Does not navigate away from queue page.

**Drawer header:** `{staff_ref} — {institution_name}` + `[Open Full Record →]` link to G-03.

**Tabs within drawer:** Quick Actions | Documents | Notes

#### Quick Actions Tab

Shows the next available action based on current status:

| Current Status | Available Actions |
|---|---|
| DOCUMENTS_REQUESTED | [Mark Documents Received] · [Send Document Reminder to Institution] · [Manually Upload Document] |
| DOCUMENTS_RECEIVED | [Review Documents] (opens document checklist) · [Request Missing Documents] · [Mark Ready for Vendor] |
| READY_FOR_VENDOR | [Select Vendor & Submit] (vendor selection modal) · [View Documents] |
| VENDOR_SENT | [Poll Vendor Status] · [Mark as Vendor Returned] (if webhook missed) · [Contact Vendor] |
| VENDOR_RETURNED | [Review Result & Submit for Approval] (if FLAGGED/INCONCLUSIVE) · [Mark CLEAR] (if vendor_result = CLEAR) |

**[Mark CLEAR] confirmation:** "Confirm CLEAR result for {staff_ref}? This will set their BGV status to CLEAR with expiry {expiry_date}. Confirm?"

**[Review Result & Submit for Approval]** (for FLAGGED/INCONCLUSIVE):
- Shows vendor result summary
- BGV Executive adds review note (required, min 20 chars)
- [Submit for Supervisor Approval] → sets `reviewed_by_id = NULL`, `awaiting_approval = true`, notifies Supervisor (92) in-app

#### Documents Tab

Document checklist for the verification. Required documents per check type are defined in G-08 config.

| Column | Notes |
|---|---|
| Document Type | e.g. Aadhar, Police Clearance |
| Required | Yes / No |
| Status | Uploaded / Missing / Rejected |
| Uploaded At | Datetime if uploaded |
| [View] | Opens signed R2 URL in new tab (30-minute expiry) |
| [Reject] | Prompts for rejection reason; sets `rejection_reason` |
| [Upload] | File picker; max 10MB; allowed types: PDF, JPG, PNG |

"All required documents received" green banner when checklist is complete.

#### Notes Tab

Thread of internal notes for this verification.

- Text area (max 500 chars) + [Add Note]
- Notes are stored in `bgv_audit_log` with `action = NOTE_ADDED`
- All roles with access to this verification can add notes
- Notes are NOT visible to institutions or staff

---

### Section F — Create Manual BGV Modal

Triggered by [Create Manual BGV] button (BGV Executive, Supervisor, Manager).

Used when institution has not yet submitted via portal, or for emergency re-verification.

**Fields:**
| Field | Control | Notes |
|---|---|---|
| Institution | Searchable select | Required |
| Staff Member | Searchable select (institution staff list) or [+ New Staff Record] | Required |
| Verification Type | Radio: INITIAL / RE_VERIFICATION | Required; RENEWAL is system-created only |
| Reason / Notes | Textarea (max 300 chars) | Required for RE_VERIFICATION |
| Assign To | Select: BGV Executive | Defaults to current user if BGV Executive |
| Priority Override | Select: CRITICAL / HIGH / MEDIUM / LOW | Default: MEDIUM. Requires Supervisor (92) if setting CRITICAL. |

**Validation:**
- Cannot create INITIAL if staff already has a CLEAR active verification (not expired)
- CRITICAL priority override requires Supervisor or Manager role — shown as locked for BGV Executive (40)

**[Create BGV Request] → **`bgv_verification` created. Drawer closes. Queue refreshes. ✅ "BGV request created — assigned to {name}" toast 4s.

---

### Section G — Vendor Selection Modal

Triggered by [Select Vendor & Submit] in action drawer.

| Field | Control | Notes |
|---|---|---|
| Vendor | Searchable select | Only ACTIVE vendors with `health_status = HEALTHY` shown by default. "Show degraded vendors" toggle. |
| Checks Required | Multi-select checkboxes | Pre-populated from `bgv_config.default_checks`; override per verification |
| Expected Turnaround | Auto-populated | `vendor.sla_hours` shown |
| Notes to Vendor | Textarea (optional) | Max 200 chars |

**Vendor health warning:** If selected vendor `health_status = DEGRADED`: ⚠️ "This vendor is currently degraded — turnaround may be delayed. Contact vendor before submitting."

**[Submit to Vendor]:**
- API call to `POST {vendor.api_base_url}/submit` with encrypted payload
- On success: `vendor_sent_at` set, `vendor_request_ref` stored, status → VENDOR_SENT
- On failure: Error shown inline — "Vendor API error: {message}. Retry or select a different vendor."
- Submission logged to `bgv_vendor_transaction`

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | BGV Executive (40), BGV Ops Supervisor (92), BGV Manager (39), Platform Admin (10) |
| See all verifications | BGV Ops Supervisor (92), BGV Manager (39), Platform Admin (10) |
| See only own assigned items | BGV Executive (40) |
| BGV Executive self-assign from Unassigned | Yes — can assign unassigned DOCS_PENDING items to themselves |
| [Assign to…] bulk action | BGV Ops Supervisor (92), BGV Manager (39) only |
| [Create Manual BGV] | All BGV roles |
| CRITICAL priority override | BGV Ops Supervisor (92), BGV Manager (39) only |
| [Submit for Supervisor Approval] | BGV Executive (40) only — supervisor cannot self-approve |
| Approve FLAGGED decision | BGV Ops Supervisor (92) only — in G-03 (not this page) |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Queue is empty (all complete) | Empty state per tab: "No verifications pending in this category." with checkmark icon |
| Vendor API call fails during submission | Error shown in drawer: "Submission failed — vendor did not respond. {Error detail}. Retry?" [Retry] re-attempts once; if fails again: "Contact vendor support. Verification held at READY_FOR_VENDOR." |
| Vendor webhook missed (result received but no status update) | BGV Executive can [Mark as Vendor Returned] manually from VENDOR_SENT status. Prompts: "Confirm vendor has returned result? Enter vendor transaction ref:" — manual override logged. |
| Two executives open same drawer simultaneously | Last save wins. If conflict detected on save: "This verification was updated by another session. Reload to see latest state." |
| Institution deactivated mid-verification | Verification remains in queue. Warning banner in drawer: "Institution {name} has been deactivated. Verification will complete as normal; compliance record archived." |
| Staff marked as no longer has_minor_access | Verification automatically deprioritised (set to LOW priority). Warning in drawer: "Staff member's minor access status has been updated. Verify with institution before proceeding." |
| BGV Executive leaves company (account deactivated) | Their assigned verifications show as "Unassigned" automatically. Supervisor notified in-app: "{N} verifications unassigned — reassign needed." |

---

## 7. UI Patterns

### Loading States
- Stats bar: shimmer 5 tiles
- Queue table: 10-row shimmer
- Action drawer: skeleton (header + 3 tab labels + content area shimmer)

### Toasts
| Action | Toast |
|---|---|
| Docs marked received | ✅ "Documents marked received for {staff_ref}" (3s) |
| Vendor submitted | ✅ "Submitted to {vendor_name} — ref {vendor_ref}" (4s) |
| Marked CLEAR | ✅ "Verification CLEAR — {staff_ref} expiry set to {date}" (4s) |
| Submitted for approval | ✅ "Sent to Supervisor for approval — {staff_ref}" (4s) |
| Assign complete | ✅ "{N} verification(s) assigned to {name}" (3s) |

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table; drawer opens 400px right panel |
| Tablet | Table columns: Ref, Institution, Status, SLA, Action. Drawer opens full-width overlay. |
| Mobile | Card list view (not table). Action drawer full-screen. Read-only recommendation: "Queue management is best on desktop." |

---

*Page spec complete.*
*G-02 covers: stats bar (live queue counts) → tabbed queue (All / Docs Pending / Docs Received / Ready for Vendor / Vendor Returned / Awaiting Approval / Overdue) → queue table with priority + SLA countdown → bulk actions (assign / mark received / batch vendor submit) → action drawer (Quick Actions / Documents / Notes) → vendor selection modal → create manual BGV modal.*
