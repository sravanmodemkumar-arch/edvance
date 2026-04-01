# G-06 — POCSO Case Management

> **Route:** `/bgv/pocso/`
> **Division:** G — Background Verification
> **Primary Role:** POCSO Compliance Officer (41) — full case management; POCSO Reporting Officer (78) — full
> **Supporting Roles:** BGV Manager (39) — read + escalate; Legal Officer (75) — read; Platform Admin (10) — full
> **File:** `g-06-pocso-case-management.md`
> **Priority:** P0 — POCSO Act 2012 legal requirement; unreported cases = criminal liability

---

## 1. Page Name & Route

**Page Name:** POCSO Case Management
**Route:** `/bgv/pocso/`
**Part-load routes:**
- `/bgv/pocso/?part=case-list` — case list
- `/bgv/pocso/{case_id}/?part=detail` — case detail drawer
- `/bgv/pocso/?part=stats-bar` — stats bar

---

## 2. Purpose

G-06 is the case management workspace for all POCSO Act 2012 flagged staff members identified during BGV. Every case where a vendor or BGV Executive identifies a POCSO-related offense must flow through this page — from initial flag → NCPCR mandatory report → institution notification → employment action → case closure.

**Critical legal context:**
Under POCSO Act 2012 Section 19 and Section 21 (mandatory reporting): any person who knows of a POCSO offense against a child but fails to report it to authorities can face imprisonment up to 6 months. EduForge is a platform used by minors — knowledge of a POCSO offender on staff triggers mandatory reporting.

NCPCR (National Commission for Protection of Child Rights) must be notified. State Child Protection committees may also need to be informed.

**Who needs this page:**
- POCSO Compliance Officer (41) — primary case handler
- POCSO Reporting Officer (78) — files NCPCR reports
- BGV Manager (39) — oversight; institution access suspension decisions
- Legal Officer (75) — read-only; for legal advice on case handling

---

## 3. Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  MANDATORY REPORTING BANNER (persistent red) — if overdue cases │
├─────────────────────────────────────────────────────────────────┤
│  Page header: "POCSO Case Management"   [+ Create Case Manually]│
├─────────────────────────────────────────────────────────────────┤
│  Stats bar: Open | Under Review | NCPCR Reported | Closed       │
├──────────────────────────────┬──────────────────────────────────┤
│  Tabs: All | Open | Under    │  Filters: Status | Institution  │
│  Review | NCPCR Reported |   │  Type | Date Range | Handled By │
│  Suspended | Closed          │                                  │
├──────────────────────────────┴──────────────────────────────────┤
│  Case Table (server-side paginated, 25 rows)                    │
├─────────────────────────────────────────────────────────────────┤
│  Case Detail Drawer (slides in on row click)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Mandatory Reporting Banner

Persistent. Shown when any case has:
- `action_status IN (OPEN, UNDER_REVIEW)` AND `created_at < now() - 24 hours`

**Banner content:** `🚨 {N} POCSO case(s) require NCPCR reporting. Mandatory reporting deadline: within 24 hours of identification. [Review Overdue Cases →]`

Red background. Cannot be dismissed. Visible to all roles with page access.

**Why 24 hours:** POCSO Act requires "immediate" reporting. EduForge policy defines 24 hours as the outer limit — enough time for case review but meeting the spirit of the Act.

---

### Section B — Stats Bar

| Stat | Description | Colour |
|---|---|---|
| Open | `action_status = OPEN` | Red |
| Under Review | `action_status = UNDER_REVIEW` | Amber |
| Institution Notified | `institution_notified = true` but `ncpcr_reported = false` | Amber |
| NCPCR Reported | `ncpcr_reported = true` | Blue |
| Employment Suspended | `action_status = EMPLOYMENT_SUSPENDED` | Purple |
| Closed | `action_status = CLOSED` | Green |

---

### Section C — Case Tabs

| Tab | Filter | Badge |
|---|---|---|
| All | All cases | Total |
| Open | `action_status = OPEN` | Count — red |
| Under Review | `action_status = UNDER_REVIEW` | Count |
| NCPCR Reported | `ncpcr_reported = true` | Count |
| Employment Suspended | `action_status = EMPLOYMENT_SUSPENDED` | Count |
| Closed | `action_status = CLOSED` | Count |

---

### Section D — Case Table

| Column | Sortable | Notes |
|---|---|---|
| Case Ref | No | `POCSO-{YYYYMMDD}-{seq}` e.g. `POCSO-20260321-00001` |
| Institution | Yes | Institution name |
| Type | Yes | SCHOOL / COLLEGE / COACHING |
| Staff Ref | No | Anonymised `bgv_staff.staff_ref` |
| Offense Type | No | Truncated to 60 chars |
| Source | No | BGV_VENDOR / MANUAL_FLAG / ANONYMOUS_TIP |
| Status | Yes | Action status pill |
| Institution Notified | No | ✅ Yes / — No |
| NCPCR Reported | No | ✅ Yes (with ref) / — No |
| FIR Filed | No | ✅ Yes (with ref) / — No |
| Opened | Yes | `created_at` date |
| Days Open | Yes (default: DESC) | `today - created_at.date()` — red if > 1 day and not reported |
| Handled By | No | Officer name |
| Action | — | [Open →] |

**NCPCR Ref** shown inline when `ncpcr_reported = true`: `NCPCR-{ref}`.

---

### Section E — Case Detail Drawer

600px drawer. Contains the complete case file.

**Drawer header:**
- Case ref badge
- Action status pill (coloured)
- Days open counter
- `[Open Full Case Page]` (for long cases — same content in full-page view at `/bgv/pocso/{case_id}/`)

**Drawer tabs: Case Details | Actions Timeline | NCPCR Filing | Institution Actions | Documents | Audit Log**

---

#### Case Details Tab

**Case information (read-only for all; BGV Manager can edit offense details before NCPCR report):**

| Field | Value |
|---|---|
| Case Ref | `POCSO-{YYYYMMDD}-{seq}` |
| Staff Ref | `bgv_staff.staff_ref` |
| Institution | Name + type |
| Offense Type | Full text |
| Offense Date | Date or "Unknown" |
| Offense Jurisdiction | Court/police district |
| Source | BGV_VENDOR / MANUAL_FLAG / ANONYMOUS_TIP |
| Source Verification | Link to `bgv_verification` (G-03) |
| Handled By | POCSO Officer name |
| Created At | Datetime |
| Action Status | Current status |

**[Edit Offense Details]** (POCSO Officer, Manager only — available before NCPCR report only):
- Edit: Offense Type, Offense Date, Offense Jurisdiction
- Once `ncpcr_reported = true`: fields are locked permanently. "Offense details cannot be changed after NCPCR report has been filed."

---

#### Actions Timeline Tab

Chronological log of all case actions.

Each entry shows:
- Datetime
- Action type (auto-generated or manual)
- Performed by
- Notes

**Standard action steps expected:**
1. Case Created (auto from BGV result or manual)
2. Case Under Review (POCSO Officer picks up case)
3. FIR Filed with Local Police (POCSO Section 19(1))
4. Institution Notified
5. NCPCR Report Filed
6. SCWC Notified (State Child Welfare Committee — jurisdiction of the institution's state)
7. Employment Suspended (if applicable)
8. Case Closed

Progress indicator shows which steps are complete vs pending.

---

#### NCPCR Filing Tab

The primary workflow for mandatory reporting. This tab contains three sub-sections:
1. **NCPCR Report** — always visible from case creation
2. **Police Reporting (FIR)** — visible from case creation; shown in amber until completed
3. **SCWC Notification** — visible from case creation; shown in amber until completed

All three sections display simultaneously in sequence. Completed sections show a ✅ header. Incomplete sections show ⏳. This single tab gives POCSO Officer the full mandatory reporting workflow in one view.

**Pre-report checklist** (must confirm before filing):
- [ ] Offense details verified against vendor report
- [ ] Institution has been notified (or note explaining why not yet)
- [ ] Legal Officer (75) has been consulted (if offense type is contested) — [Notify Legal Officer] sends in-app message to Legal Officer (75) and Legal Officer (75) can add a read-only case note. Not a blocking step.
- [ ] Staff's access to minors has been suspended or pending

**NCPCR Report Form:**
| Field | Control | Notes |
|---|---|---|
| NCPCR Reference Number | Text | Received from NCPCR after reporting; can be filled retroactively |
| Report Date | Date | Date report was filed |
| Reporting Method | Select: NCPCR_PORTAL · EMAIL · FAX · PHONE_CALL | — |
| Report Summary | Textarea (min 100 chars) | Summary of offense and steps taken |
| Supporting Documents | File upload | e.g. BGV vendor report PDF, police clearance copy |

**[Mark as NCPCR Reported]:**
- Confirmation modal: "Confirm NCPCR report filed for case {case_ref}? NCPCR ref: {ref}. This action is permanent and logged."
- Sets `ncpcr_reported = true`, `ncpcr_ref`, `ncpcr_reported_at`
- Action status → `NCPCR_REPORTED`
- BGV Manager (39) notified in-app

**Overdue warning:** If case is OPEN for > 24h with `ncpcr_reported = false`: red inline warning: "⚠️ NCPCR reporting deadline exceeded. Report immediately."

**If NCPCR ref not yet received:** [Mark Report Filed — Ref Pending] option. Sets `ncpcr_reported = true` with `ncpcr_ref = PENDING`. POCSO Officer must update with actual ref within 48h (system reminder sent).

#### Police Reporting (FIR) Section

**POCSO Act Section 19(1) mandates reporting to local police. This is separate from and in addition to NCPCR.**

**FIR Filing Form:**
| Field | Control | Notes |
|---|---|---|
| Police Station | Text | Name and location of station with jurisdiction over the institution |
| FIR Reference Number | Text | FIR number from police station |
| FIR Filed Date | Date | — |
| Reporting Officer | Text | Name of police officer who received the complaint |
| Notes | Textarea (max 300 chars) | Any additional details |

**[Mark FIR Filed]:**
- Sets `police_reported = true`, `fir_ref`, `fir_filed_at`, `police_station`
- Logged in `bgv_audit_log` with `action = FIR_FILED`

**Overdue warning:** If NCPCR reported but `police_reported = false` for > 48h: amber inline warning: "⚠️ FIR with local police not yet recorded. POCSO Section 19(1) requires police notification."

#### State Child Welfare Committee (SCWC) Section

**POCSO Act also requires reporting to the SCWC of the state where the offense occurred.**

**SCWC Filing Form:**
| Field | Control | Notes |
|---|---|---|
| State | Select | Pre-filled from institution's registered state |
| SCWC Name | Auto-filled | e.g. "Maharashtra State Commission for Protection of Child Rights" — from G-08 SCWC contacts config |
| SCWC Reference Number | Text | Reference number from SCWC acknowledgement |
| Report Date | Date | — |
| Reporting Method | Select: EMAIL · PORTAL · FAX | — |
| Notes | Textarea | — |

**[Mark SCWC Notified]:**
- Sets `scwc_reported = true`, `scwc_ref`, `scwc_reported_at`
- Logged in audit log

---

#### Institution Actions Tab

Actions to be taken with the institution.

**Institution Notification:**

| Field | Control | Notes |
|---|---|---|
| Notification Method | Select: EMAIL / IN_APP / PHONE_CALL / FORMAL_NOTICE | — |
| Notification Date | Date | — |
| Notes | Textarea | What was communicated |

**[Mark Institution Notified]:**
- Sets `institution_notified = true`, `institution_notified_at`, `institution_notification_method`
- Action status → `INSTITUTION_NOTIFIED`

**Staff Access Suspension:**

[Suspend Staff Platform Access] (BGV Manager 39 only):
- Confirmation: "This will mark {staff_ref} as SUSPENDED in the BGV system and notify Platform Admin to revoke institution portal access. Confirm?"
- Sets `bgv_staff.bgv_status = SUSPENDED`
- In-app alert sent to Platform Admin (10) to revoke institution portal login for this staff member
- Action status → `EMPLOYMENT_SUSPENDED`

---

#### Documents Tab

All documents attached to this POCSO case.

Columns: Document Name | Type (VENDOR_REPORT / NCPCR_FILING / FIR_COPY / SCWC_CORRESPONDENCE / CORRESPONDENCE / OTHER) | Uploaded By | Date | [View] | [Delete]

[+ Attach Document] — upload supporting documents.

Documents stored in private R2 bucket, separate from general BGV documents. Access logged in `bgv_audit_log`.

---

#### Audit Log Tab

Every action on this POCSO case, immutable.

| Column | Notes |
|---|---|
| Timestamp | — |
| Action | e.g. CASE_CREATED · NCPCR_REPORTED · INSTITUTION_NOTIFIED · STATUS_CHANGED |
| Performed By | User or System |
| Change | "{old} → {new}" |
| Note | — |

[Export Case Audit CSV] — POCSO Officer, Legal Officer, Platform Admin.

---

### Section F — Create Case Manually

Triggered by [+ Create Case Manually] (POCSO Officer, BGV Manager).

Used when a POCSO offense is reported via anonymous tip or identified outside the BGV vendor flow.

| Field | Control | Notes |
|---|---|---|
| Source | Radio: MANUAL_FLAG / ANONYMOUS_TIP | — |
| Institution | Searchable select | Required |
| Staff Member | Searchable select or [+ New Staff Record] | If anonymous tip, staff may not exist yet |
| Offense Type | Text (max 300 chars) | Required |
| Offense Date | Date | Optional |
| Offense Jurisdiction | Text | Optional |
| Initial Notes | Textarea (max 500 chars) | Required |
| Attach Evidence | File upload | Optional |

**[Create POCSO Case]:**
- Generates `case_ref = POCSO-{YYYYMMDD}-{seq}`
- Sets `action_status = OPEN`
- Notifies POCSO Officer (41) and BGV Manager (39) in-app
- ✅ "POCSO case created: {case_ref}" toast

**Deduplication check:** Before creation, system checks for existing open case for the same `staff_id`. If found: "An open POCSO case already exists for this staff member: {existing_case_ref}. Add to existing case instead?" [View Existing Case] / [Create New Case Anyway].

---

### Section G — Case Closure

Available when all required steps are complete.

**Closure prerequisites** — [Close Case] button is disabled until all are met:

| Prerequisite | Field | Override |
|---|---|---|
| NCPCR report filed | `ncpcr_reported = true` | None — cannot close without NCPCR report |
| FIR with local police | `police_reported = true` | Can override with documented justification: "FIR Not Applicable — {reason}" (min 50 chars). Requires BGV Manager confirmation. |
| Institution notified | `institution_notified = true` | None |
| Employment action confirmed | `action_status = EMPLOYMENT_SUSPENDED` OR closure reason documents institution's own action | Free text in closure modal |

Each unmet prerequisite shown as a red ✗ checklist item above the [Close Case] button. Completed prerequisites shown as ✅.

**[Close Case]** (POCSO Officer, BGV Manager):
- Modal: Closure reason (required, min 50 chars)
- Closure type: Select — RESOLVED_EMPLOYMENT_TERMINATED · RESOLVED_EMPLOYMENT_RETAINED_BY_INSTITUTION · FALSE_POSITIVE_CONFIRMED · INCONCLUSIVE_INSUFFICIENT_EVIDENCE · OTHER
- If FIR override invoked: "Explain why police reporting is not applicable (min 50 chars):" — logged separately
- [Confirm Closure]
- Sets `action_status = CLOSED`, `closed_at`, `closure_reason`

**Closed cases are never deleted.** Legal retention: 10 years post-closure.

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | POCSO Compliance Officer (41), POCSO Reporting Officer (78), BGV Manager (39), Legal Officer (75), Platform Admin (10) |
| BGV Executive (40) | No direct access — may see POCSO flag in G-03 but cannot manage cases |
| BGV Ops Supervisor (92) | No access — POCSO cases are above supervisor scope; handled at compliance level |
| POCSO Compliance Officer (41) | Full case management except [Suspend Staff Access] (Manager only) |
| POCSO Reporting Officer (78) | Full case management including NCPCR filing; same as Officer (41) |
| Legal Officer (75) | Read-only across all tabs. Cannot take any action. |
| [Edit Offense Details] | POCSO Officer (41), Reporting Officer (78), BGV Manager (39) — before NCPCR report only |
| [Mark as NCPCR Reported] | POCSO Officer (41), Reporting Officer (78) |
| [Mark FIR Filed] | POCSO Officer (41), Reporting Officer (78), BGV Manager (39) |
| [Mark SCWC Notified] | POCSO Officer (41), Reporting Officer (78), BGV Manager (39) |
| [Suspend Staff Access] | BGV Manager (39), Platform Admin (10) |
| [Mark as False Positive] | Requires BOTH: (POCSO Officer (41) OR Reporting Officer (78)) AND BGV Manager (39) confirmation. Neither can do it alone — two-person rule enforced via two-step confirmation: first actor clicks [Initiate False Positive Override] → second actor sees pending override and [Confirm False Positive]. |
| [Merge Duplicate Cases] | POCSO Officer (41), Reporting Officer (78), BGV Manager (39) |
| [Close Case] | POCSO Officer (41), Reporting Officer (78), BGV Manager (39) — only when all prerequisites met |
| [Export Case Audit CSV] | All with page access |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| NCPCR ref not yet received at time of filing | [Mark Report Filed — Ref Pending] flow. System sends daily reminder to POCSO Officer until ref is entered. |
| Staff no longer employed (institution confirms dismissal) | Employment Suspended step skipped. Note added: "Institution confirmed employment terminated prior to case creation." Case can proceed to closure. |
| Anonymous tip — staff not in system | Case created with `staff_id = NULL`. BGV Executive notified to create staff record and initiate BGV. Case linked when staff record is created. |
| POCSO Compliance Officer on leave — case stale | BGV Manager (39) receives escalation after 24h of no action on OPEN cases. Manager can reassign handler. |
| Duplicate case from vendor + manual flag | Deduplication check as described. If two separate cases exist for same staff: merge prompt for POCSO Officer. Merge retains most recent case ref; links both audit logs. |
| Vendor report was false positive (verified by police) | Override flow: [Mark as False Positive] — requires BGV Manager + POCSO Officer joint confirmation. Adds note "CLEARED — false positive confirmed by {authority}". Case status → CLOSED with closure type FALSE_POSITIVE_CONFIRMED. BGV staff status reverted to CLEAR. |
| Institution challenges the offense | Formal dispute process: institution must submit written challenge within 48h of notification via institution portal. BGV Manager receives challenge; Legal Officer (75) reviews. If contested: BGV Manager adds "DISPUTE_RECEIVED" note to case; 7-day review window. If false positive confirmed → [Mark as False Positive] flow. If offense upheld → Legal Officer (75) adds formal rejection note; BGV Manager notifies institution in writing. Dispute state is not a system status — tracked via case notes and communication log. |
| NCPCR portal offline at time of filing | [Mark Report Filed — Ref Pending] option (same as no-ref flow). Note added: "NCPCR portal unavailable at time of filing — filed via {method}." Retry for confirmation ref within 72h. |
| Staff was mid-BGV when terminated | BGV Executive can [Cancel BGV Request] from G-03. If POCSO flag detected after termination → case still created. Institution notification adjusted with note: "Staff no longer employed as of {date} — case reported for record and institutional review." Case proceeds to NCPCR reporting regardless. |

---

## 7. Celery Task — POCSO SLA Monitor

`monitor_pocso_case_sla` — runs hourly.

- Checks all cases with `action_status IN (OPEN, UNDER_REVIEW)` and `created_at < now() - 24h`
- If `ncpcr_reported = false`: sends in-app notification to POCSO Officer (41), POCSO Reporting Officer (78), BGV Manager (39): "POCSO case {case_ref} has exceeded 24h without NCPCR report. Immediate action required."
- Notification escalation: if still unreported after 48h → Platform Admin (10) and Legal Officer (75) notified.
- Checks `ncpcr_ref = PENDING` cases older than 48h → sends reminder to POCSO Officer: "NCPCR reference number not yet recorded for {case_ref}."
- Checks `police_reported = false` and `ncpcr_reported = true` and case > 48h old → amber reminder to POCSO Officer: "FIR with local police not yet recorded for {case_ref}."

---

## 8. UI Patterns

### Loading States
- Stats bar: 5-tile shimmer
- Case table: 8-row shimmer
- Drawer: header shimmer + tab skeleton + content shimmer

### Toasts
| Action | Toast |
|---|---|
| Case created | 🚨 "POCSO case created: {case_ref}" (6s, persistent) |
| NCPCR report filed | ✅ "NCPCR report recorded — case ref: {ncpcr_ref}" (5s) |
| FIR filed | ✅ "FIR recorded — ref: {fir_ref}, {police_station}" (4s) |
| SCWC notified | ✅ "SCWC notification recorded — ref: {scwc_ref}" (4s) |
| Institution notified | ✅ "Institution notification recorded" (4s) |
| Staff suspended | ⚠️ "Staff access suspended — Platform Admin notified" (5s) |
| Case closed | ✅ "POCSO case {case_ref} closed" (4s) |

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table + 600px drawer |
| Tablet | Reduced table columns (Case Ref, Status, Days Open, Action). Drawer full overlay. |
| Mobile | Card list. Drawer full-screen. Read-only recommendation for sensitive data management. |

---

*Page spec complete.*
*G-06 covers: mandatory reporting banner (24h overdue) → stats bar (6 case statuses) → tabbed case list → case detail drawer (Case Details / Actions Timeline / NCPCR Filing / Institution Actions / Documents / Audit Log) → NCPCR report form with ref-pending option → staff access suspension workflow → manual case creation with deduplication check → false positive override → case closure prerequisites + retention policy → Celery 24h SLA monitor with escalation to Platform Admin.*
