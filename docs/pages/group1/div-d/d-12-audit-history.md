# D-12 — Question Audit & Version History

> **Route:** `/content/audit/<uuid>/`
> **Division:** D — Content & Academics
> **Primary Roles:** Content Director (18) · Question Approver (29)
> **Access via:** D-11 drawer "Version History" link · D-04 Published tab · D-04 drawer
> **File:** `d-12-audit-history.md`
> **Priority:** P2 — Mandatory once first unpublish or amendment occurs
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Question Audit & Version History
**Route:** `/content/audit/<uuid>/` — where `<uuid>` is the question ID
**Part-load routes:**
- `/content/audit/<uuid>/?part=timeline` — audit timeline events
- `/content/audit/<uuid>/?part=compare&v1={version}&v2={version}` — side-by-side version diff
- `/content/audit/<uuid>/?part=restore-confirm&version={n}` — restore confirmation panel

---

## 2. Purpose (Business Objective)

Every question on the platform accumulates a history: it was created, saved, submitted, returned with feedback, revised, reviewed again, approved, published, and possibly unpublished and corrected. When something goes wrong — a question with a wrong answer key reaches 74,000 students, a reviewer missed a factual error, a question was unexpectedly unpublished — the Director and Approver need to know exactly what happened, who did it, and when.

D-12 provides a complete, immutable, per-question audit trail. The audit log is INSERT-only at the application layer — no update or delete route exists. Every state transition, tag change, export event, and access level modification is recorded with the actor, their IP address, a before/after snapshot, and a timestamp.

The version compare feature lets the Director or Approver see precisely what changed between any two versions of a question — which option was edited, which tag was corrected, what explanation was rewritten. The restore feature gives the Approver the power to revert a question to any prior version if a revision made things worse.

**Business goals:**
- Provide a complete, immutable audit trail for every question (compliance + accountability)
- Enable precise version comparison between any two historical snapshots
- Allow Approver to restore a question to a prior version when needed
- Enforce DPDPA: author identity (name, email, IP) never exported to CSV/PDF

---

## 3. User Roles

| Role | Access |
|---|---|
| Content Director (18) | Full read of audit timeline + version compare. Cannot restore versions (that is Approver's authority). |
| Question Approver (29) | Full read + version restore action |

> **Route access:** The `/content/audit/<uuid>/` URL returns 403 for all other roles. SMEs cannot access their own question's full audit trail — they see only the reviewer comment on return (shown in D-01 and D-02). This prevents SMEs from viewing reviewer identity (DPDPA) and system-level action metadata.

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header

- H1: "Audit Trail: Question {uuid short}" (e.g. "Audit Trail: Question …3f8a")
- Subject · Topic · Current State · Published Date (if published)
- "Back to Published Bank" link (→ D-11 for this question) or "Back to Approval Queue" (→ D-04), depending on the referrer

---

### Section 2 — Timeline View

**Purpose:** Visual chronological audit of every significant event in this question's lifecycle.

**Layout:** Vertical timeline, newest at top, oldest at bottom. Each event is a card.

**Event card structure:**
- Event type label (see Event Types below)
- Actor: "Role Title" (e.g. "Question Reviewer") — role title only. Never personal name or email (DPDPA).
- Timestamp: Full datetime in IST
- IP Address: visible only to Content Director and Approver (shown as last octet masked: "43.XXX.XXX.182" — partial masking, not full mask)
- Before State → After State: field-level diff for tag changes. Full state for state transitions.
- Comments: reviewer comment, return reason, approver note (where applicable)

**Event Types:**

| Event | Icon | Description |
|---|---|---|
| Created | 📄 Grey | SME created the question in D-02 |
| Saved as Draft | 💾 Grey | Autosave or manual save-draft |
| Submitted for Review | ➤ Blue | SME submitted — state: DRAFT → UNDER_REVIEW |
| Assigned to Reviewer | 👤 Blue | Auto-assigned from D-15 routing |
| Returned to SME | ↩ Orange | Reviewer returned — includes reason category + full comment |
| Revision Submitted | ➤↩ Blue | SME resubmitted after return — revision count shown |
| Passed to Approver | ✓ Blue | Reviewer passed — state: UNDER_REVIEW → PENDING_APPROVAL |
| Committee Pass 1 | ✓¹ Purple | First reviewer passed in committee review (G7) |
| Committee Pass 2 | ✓² Purple | Second reviewer passed — question now at Approver |
| Approved + Published | ✅ Green | Approver published — state → PUBLISHED |
| Approver Send-Back | ↩ Purple | Approver sent back to Reviewer — includes reason + note |
| Tag Amendment | 🏷 Amber | Difficulty or access level re-tagged by Approver |
| Access Amendment | 🔐 Amber | Access level changed post-publish (G4) |
| Valid Until Extended | 📅 Amber | Expiry date extended (G5) |
| Taxonomy Retag | 🗂 Grey | Topic/subtopic changed via D-09 bulk retag (G10) |
| Exported | 📤 Grey | Question included in a CSV/PDF export (who, filter used) |
| Unpublished | 🚫 Red | Approver or emergency — state → AMENDMENT_REVIEW |
| Emergency Unpublished | 🚨 Dark Red | Emergency bulk unpublish (G8) — task ID shown |
| Amendment Review Assigned | 👤 Orange | Fast-track review assignment |
| Amendment Approved | ✅ Amber | Re-approved after amendment — state → PUBLISHED |
| Archived | 📦 Grey | Nightly Celery task or Director manual archive — state → ARCHIVED |
| Version Restored | ↺ Purple | Approver restored a prior version |
| Duplicate Acknowledged | ⚠ Yellow | SME acknowledged a duplicate match in D-02 or D-07 |

**Events that are NOT shown** (stored in log but filtered from UI):
- Raw autosave events (too granular — only explicit submit/save actions shown)
- Celery task heartbeat events

---

### Section 3 — Version Compare

**Purpose:** See exactly what changed between any two historical question versions.

**Version selector:**
Two dropdown selectors ("Compare Version A" and "Compare Version B") populated with all versioned snapshots for this question. Each version shows: "Version {n} — submitted by SME {date}" or "Version {n} — amendment revision {date}".

"Compare" button → loads `?part=compare&v1={n}&v2={n}` → side-by-side diff view.

**Side-by-side diff layout:**

| Section | Version A (left) | Version B (right) |
|---|---|---|
| Question Body | Rendered — changed text highlighted in red (removed) and green (added) | — |
| Option A | Rendered | Rendered — changes highlighted |
| Option B | — | — |
| Option C | — | — |
| Option D | — | — |
| Correct Answer | "Option C" | "Option B" — if changed: shown in amber |
| Explanation | Rendered | Changes highlighted |
| Difficulty | Medium | Hard — changed: amber |
| Topic | Algebra — Basic | Algebra — Advanced — changed |
| Access Level | Platform-Wide | — (unchanged, shown in grey) |
| Exam Types | SSC CGL | SSC CGL · SSC CHSL — new addition in green |
| Content Type | Evergreen | — (unchanged) |
| Valid Until | — | — (N/A for Evergreen) |

**Diff algorithm:** Python `difflib.unified_diff` on plain text fields. Rendered fields (LaTeX, HTML) compared at plain text level — changes shown in the rendered view with character-level green/red highlighting using `<mark>` tags.

**"Restore to Version A" button (Approver only):**
Appears in the version compare view when comparing a past version (A) against a more recent version (B).

Restoring a prior version:
1. Confirmation modal: "Restore question to Version {n}? The question will move to DRAFT state attributed to the original SME. They will need to review and resubmit. Reason for restore:" (text field ≥ 20 chars required)
2. 2FA re-prompt
3. On confirm:
   - `content_question` fields restored to Version A's snapshot values
   - State → DRAFT (not PUBLISHED — Approver cannot directly restore to published; the question must go through the pipeline again)
   - Original SME notified: "Your question was restored to an earlier version by the Approver. Review and resubmit when ready."
   - `content_question_audit_log` entry: `action: VersionRestored · from_version: {B} · to_version: {A} · actor · reason`

---

### Section 4 — Export Audit Section

**Purpose:** Dedicated visibility into every export action involving this question — for compliance and secrecy tracking.

Below the main timeline, a collapsible "Export Events" section:

| Column | Description |
|---|---|
| Exported At | Timestamp |
| Actor Role | Content Director / Question Approver — role title, not name (DPDPA) |
| Format | CSV / PDF |
| Filters Used | Summary of filters active when export was triggered (e.g. "Subject: Physics · Difficulty: Hard · Exam Type: SSC CGL") |
| Export Batch ID | UUID — for cross-referencing multiple questions in the same export batch |

Export events are part of the audit trail but surfaced separately because they are compliance-sensitive — every question that leaves the platform boundary should have a clear record of who exported it and why.

---

## 5. Data Models

### `content_question_audit_log` (INSERT-only — append-only)
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_id` | FK → content_question | — |
| `action` | varchar | Full enum of all event types above |
| `actor_id` | FK → auth.User | — |
| `actor_ip` | inet | Stored for DPDPA audit — partially masked in UI display |
| `before_state` | jsonb | Snapshot of changed fields before action |
| `after_state` | jsonb | Snapshot after action |
| `reviewer_comment` | text | Nullable — for Returned events |
| `return_reason_category` | varchar | Nullable |
| `reason_text` | text | Nullable — for Unpublish, Restore, Access Change reasons |
| `task_id` | varchar | Nullable — Celery task ID for bulk/emergency ops |
| `version_number` | int | Nullable — which snapshot version this event created |
| `created_at` | timestamptz | Immutable — indexed for efficient per-question timeline queries |

**Database enforcement of INSERT-only:**
- Application layer: no Django ORM `update()` or `delete()` call exists for this model anywhere in the codebase
- PostgreSQL row-level security (optional additional layer): `DENY UPDATE, DELETE ON content_question_audit_log TO app_user` can be enforced at DB level by DBA
- External audit: the `content_question_audit_log` table is included in the nightly backup (C-12 snapshots) and its row count growth is monitored (an unexpected decrease would indicate tampering)

### `content_question_versions`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_id` | FK → content_question | — |
| `version_number` | int | 1, 2, 3… sequential |
| `snapshot` | jsonb | Full serialised state of the question at the time of this version — question body, all options, explanation, all tags |
| `reviewer_comment` | text | Nullable — populated when the Reviewer returns this version |
| `reviewer_return_reason` | varchar | Nullable |
| `created_at` | timestamptz | Submit timestamp for this version |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.view_question_audit')` — Roles 18 + 29 |
| Version restore | `permission='content.restore_question_version'` — Role 29 only. Director sees the "Restore" button greyed with tooltip "Only Question Approver can restore versions." |
| Export event visibility | Shown to Director and Approver. Export actor is shown as role title only (never name). |
| Actor IP display | Shown in masked form (last 2 octets revealed) to Director and Approver — for internal accountability only. Never exported to CSV/PDF. |
| DPDPA enforcement | Author name, email, full IP — excluded from all export formats. All UI displays show role title ("GK SME", "Question Reviewer") rather than personal identity. |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Question has no audit log entries (data migration question) | Timeline shows: "Audit trail starts from [date imported]. Events prior to this date are not available." — for bulk-imported legacy questions that predate the audit log implementation. |
| Restore to a version where the original SME's account is deactivated | Restore proceeds. The question moves to DRAFT attributed to the original SME's user ID. If the SME account is deactivated, the question appears in D-01 with a "SME Account Deactivated — Contact Content Director" note instead of the usual edit button. Director then manually reassigns the question to an active SME. |
| Two Approvers compare versions simultaneously | No conflict — version compare is purely read-only against the `content_question_versions` table. Concurrent reads are always safe. |
| Audit log entry for emergency bulk unpublish has 500 question IDs | Each question gets its own individual audit log entry (1 row per question per event). The emergency batch is linked by `task_id` — all 500 rows share the same `task_id` value, allowing the full batch to be identified from any individual question's trail. |
| Director tries to export the audit trail as a CSV | Export button is not provided on D-12. The audit trail is accessible only through the D-12 UI. For external audit purposes, DBA can provide a read-only database snapshot — the audit log is never exported through the application layer (DPDPA: actor IP and timing data is sensitive). |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-11 Published Bank | D-11 → D-12 | "Version History" link opens D-12 for the selected question | URL navigation: `/content/audit/{question_id}/` |
| D-04 Approval Queue | D-04 actions → D-12 | All Approver actions (publish, unpublish, re-tag, send-back) logged | INSERT into `content_question_audit_log` on every action |
| D-03 Review Queue | D-03 actions → D-12 | Pass / Return / Flag decisions logged | INSERT into `content_question_audit_log` on every decision |
| D-09 Taxonomy (G10) | D-09 bulk retag → D-12 | Taxonomy retag events per question | INSERT into `content_question_audit_log` with `action: TaxonomyRetag` per question |
| D-07 Bulk Import | D-07 → D-12 | Import batch export events | INSERT into `content_question_export_log` per question in batch |
| D-13 Quality Analytics | D-12 → D-13 | Audit events of type TagAmendment feed D-13 difficulty calibration | D-13 queries `content_question_audit_log` for re-tag events |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search & Filtering — Timeline
- Filter bar above the timeline (not a collapsible panel — audit pages benefit from always-visible filters).
- Filters: Event Type (multi-select checkboxes: show/hide categories), Actor Role (All / SME / Reviewer / Approver / Director / System), Date Range.
- "Reset Filters" link.
- Default: all event types shown, no date filter, newest first.

### Timeline Pagination
- Show 25 events per page (audit timelines can have 50+ events for busy questions). Numbered controls: "Page 1 of 4 · Showing 1–25 of 94 events".
- "Jump to: [Oldest] [Newest]" links always visible.
- Event filter changes reset to page 1.

### Export Events Section
- Collapsible below main timeline. Default collapsed.
- Table: Exported At · Actor Role · Format · Filters Used · Export Batch ID.
- Sortable by Exported At DESC (default).
- Pagination: 25 per page if > 25 export events.
- No export action available here (DPDPA constraint documented as tooltip on a greyed "Export" placeholder: "Audit trail export is not available through the application — contact DBA for read-only snapshot").

### Empty States
| Section | Heading | Subtext |
|---|---|---|
| Timeline — legacy question (pre-audit) | "Audit trail starts from {date}" | "This question was imported before audit logging was implemented. Events prior to this date are not available." |
| Export Events — none | "No exports recorded" | "This question has not been included in any CSV or PDF export." |
| Version Compare — no versions | "Only one version exists" | "This question has not been revised. No version comparison is available." |

### Toast Messages
| Action | Toast |
|---|---|
| Restore version (Approver) | ✅ "Question restored to Version {N} — SME notified" (Success 4s) |
| 2FA fail on restore | ❌ "Verification failed — version not restored" (Error persistent) |
| Version Compare loaded | No toast — compare renders inline |
| Filter applied to timeline | No toast — timeline updates inline |

### Loading States
- Timeline initial load: 5-event skeleton (event card shimmer — icon + text lines).
- Timeline filter apply: shimmer overlay on timeline while fetching filtered events.
- Version Compare load: side-by-side skeleton (two column pairs of shimmer text blocks) while diff renders.
- "Restore" 2FA modal: spinner on "Confirm" button while 2FA verifies.

### Version Compare — Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Side-by-side two columns (Version A left, Version B right). Diff highlighting via `<mark>` tags. |
| Tablet | Same two-column layout, slightly narrower columns. Horizontal scroll if content overflows. |
| Mobile | **Tab interface**: "Version A" tab · "Version B" tab · "Differences" tab (shows only changed fields). Side-by-side is not usable on mobile. Differences tab highlights which fields changed and shows both values stacked. |

### Timeline — Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Vertical timeline with full event cards (wide). IP address visible in card. |
| Tablet | Same but event card narrower. IP address collapsed to icon (hover/tap to reveal). |
| Mobile | Event cards stack full-width. IP address hidden from card (available in expanded detail tap). |

### Modal — Version Restore
- Title: "Restore Question to Version {N}?"
- Body: Explanation of consequences (question → DRAFT, original SME notified, must re-submit through full pipeline).
- Reason field: textarea, ≥ 20 chars required. Error: "Please provide a reason (minimum 20 characters)".
- 2FA prompt: TOTP input field. "Confirm Restore" button disabled until reason is valid AND 2FA code is 6 digits.
- Cancel closes modal without any action.

### Role-Based UI
- "Restore to Version A" button: Approver (29) only. Director (18) sees the button greyed with tooltip: "Only the Question Approver can restore versions."
- IP Address display: Director and Approver see partially masked IP (last 2 octets revealed). If a future admin role is added, this visibility rule must be explicitly reconfigured.
- Export Events section: Director and Approver. SMEs cannot access this page at all (403 at route level).

---

*Page spec complete.*
*Next file: `d-13-quality-analytics.md`*
