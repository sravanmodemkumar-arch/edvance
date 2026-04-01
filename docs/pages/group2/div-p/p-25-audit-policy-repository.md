# P-25 — Audit Policy Repository

> **URL:** `/group/audit/policies/`
> **File:** `p-25-audit-policy-repository.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Internal Audit Head (Role 121, G1) — primary operator

---

## 1. Purpose

The Audit Policy Repository is the authoritative library of all Division P governance documents — the policies, procedures, standards, and guidelines that define how the Audit & Quality function operates. It governs how audits are planned, how findings are classified, how CAPA timelines are set, how escalation triggers are configured, how compliance scoring is calculated, and what standards auditors are held to.

Without a policy repository, audit practices drift over time. When a new Audit Head joins, they may change how findings are classified. When an Inspection Officer leaves, their successor may apply different scoring standards. When the CBSE updates its affiliation norms, it may take months for the updated requirement to appear in checklists. The repository maintains all governing documents in one place, with version history, approval workflow, and a mandatory annual review cycle.

The problems this page solves:

1. **Policy scattered across email and WhatsApp:** Audit policies, CAPA standards, escalation rules, and scoring methodologies circulate as email attachments or WhatsApp messages. No one knows which version is current. The repository is the single authoritative source.

2. **No policy version control:** When a policy is updated, the old version disappears. There is no record of what the policy was before the change, when it changed, who approved it, or why. This is a compliance failure in itself. The repository maintains full version history with immutable records.

3. **Annual review cycle not tracked:** Audit policies should be reviewed annually (or more frequently when regulations change). Without a tracking system, policies go years without review. The repository sets review due dates and sends alerts when policies are past their review deadline.

4. **Policy acknowledgement gap:** Auditors and field staff must be aware of policies that govern their work. The repository tracks who has acknowledged reading each policy — creating an accountability trail.

5. **Regulatory reference integration:** Audit policies are grounded in specific regulations — CBSE norms, RTE provisions, POCSO requirements, state education rules. The repository links each policy to its regulatory basis, making it easy to update when regulations change and demonstrating regulatory grounding to external auditors.

**Scale:** 30–60 policy documents · 5–10 policy categories · Annual review cycle · 8 auditors + staff who must acknowledge policies

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Internal Audit Head | 121 | G1 | Full — create, edit, approve, publish all policies | Primary operator + approver |
| Group Compliance Data Analyst | 127 | G1 | Read + Track acknowledgements | Reporting |
| Group Inspection Officer | 123 | G3 | Read — policies governing inspection work | Must acknowledge |
| Group Academic Quality Officer | 122 | G1 | Read — policies governing academic audit | Must acknowledge |
| Group Affiliation Compliance Officer | 125 | G1 | Read — affiliation and regulatory policies | Must acknowledge |
| Group Grievance Audit Officer | 126 | G1 | Read — grievance audit policies | Must acknowledge |
| Group Process Improvement Coordinator | 128 | G3 | Read — CAPA and escalation policies | Must acknowledge |
| Branch Principal | — | G3 | Read — policies relevant to branch compliance | Awareness |
| Group CEO / Chairman | — | G4/G5 | Read all + Final approval for major policy changes | Governance |

> **Policy acknowledgement enforcement:** When a new policy is published or an existing policy is updated to a major version (v2.0, v3.0), all staff in the required acknowledgement list must click `[I have read and understood this policy]`. The system tracks acknowledgement dates and sends reminders to non-acknowledgers every 7 days for 30 days.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Policy Repository
```

### 3.2 Page Header
```
Audit Policy Repository                         [+ New Policy]  [Review Due List]  [Export]
Internal Audit Head — T. Subramaniam
Sunrise Education Group · 42 policies · 38 current · 3 under review · 1 overdue for review · 2 pending acknowledgement
```

### 3.3 Filter Bar
```
Category: [All / Audit Governance / CAPA & Escalation / Scoring & Methodology / Inspection / Affiliation / Grievance Audit / POCSO / Data & Privacy ▼]
Status: [All / Published / Draft / Under Review / Deprecated ▼]
Review Status: [All / Current / Due for Review / Overdue for Review ▼]
Acknowledgement: [All / Acknowledged by Me / Pending My Acknowledgement ▼]
                                                                        [Reset]
```

### 3.4 Policy Library Table

| # | Column | Content |
|---|---|---|
| 1 | Policy ID | `POL-AUD-001` |
| 2 | Policy Name | Audit Frequency & Coverage Policy |
| 3 | Category | Audit Governance |
| 4 | Version | v2.1 |
| 5 | Status | Published / Draft / Under Review / Deprecated |
| 6 | Published On | 01-Apr-2025 |
| 7 | Review Due | 01-Apr-2026 · ⚠️ if overdue |
| 8 | Regulatory Basis | CBSE Affiliation Bylaws 2018 · RTE Act 2009 |
| 9 | Acknowledged By | 7 / 8 staff ✅ · 1 pending |
| 10 | Actions | [View] · [Edit] · [Review Due] |

**Alert banner** (when overdue reviews exist):
```
⚠️ 1 policy is overdue for annual review: CAPA Timelines & Severity Classification Policy — due 01-Jan-2026
```

---

## 4. Policy Categories & Standard Policies

### Category 1 — Audit Governance

| Policy ID | Policy Name | Scope | Current Version |
|---|---|---|---|
| POL-AUD-001 | Audit Frequency & Coverage Policy | All branches · all audit types | v2.1 |
| POL-AUD-002 | Auditor Independence & Conflict-of-Interest Policy | All auditors | v1.3 |
| POL-AUD-003 | Auditor Rotation Policy | All auditors | v1.2 |
| POL-AUD-004 | Audit Evidence & Documentation Standards | All auditors | v2.0 |
| POL-AUD-005 | Audit Report Classification Policy (Confidentiality) | All | v1.1 |

### Category 2 — CAPA & Escalation

| Policy ID | Policy Name | Scope | Current Version |
|---|---|---|---|
| POL-CAPA-001 | CAPA Timelines & Severity Classification Policy | All | v2.2 |
| POL-CAPA-002 | Root Cause Analysis Standards | All auditors | v1.3 |
| POL-CAPA-003 | Corrective Action Verification Standards | 128, 123 | v1.4 |
| POL-CAPA-004 | Escalation Rules & Authority Levels | All | v2.0 |
| POL-CAPA-005 | Branch Improvement Plan Initiation Criteria | 128, 121 | v1.1 |

### Category 3 — Scoring & Methodology

| Policy ID | Policy Name | Scope | Current Version |
|---|---|---|---|
| POL-SCR-001 | Compliance Score Calculation Methodology | 127, 121 | v2.3 |
| POL-SCR-002 | Dimension Weights & Review Process | 121, G4 | v1.2 |
| POL-SCR-003 | Score Band Definitions & Thresholds | All | v1.1 |
| POL-SCR-004 | Branch Quality Ranking Methodology | 127 | v1.0 |

### Category 4 — Inspection Policy

| Policy ID | Policy Name | Scope | Current Version |
|---|---|---|---|
| POL-INS-001 | Inspection Visit Protocol | 123 | v2.1 |
| POL-INS-002 | Surprise Inspection Ratio Policy | 121, 123 | v1.2 |
| POL-INS-003 | Photo Evidence Standards | 123 | v1.3 |
| POL-INS-004 | Inspector Code of Conduct | 123 | v1.0 |

### Category 5 — POCSO & Safeguarding

| Policy ID | Policy Name | Scope | Current Version |
|---|---|---|---|
| POL-POC-001 | POCSO Complaint Audit Protocol | 126, 121 | v1.3 |
| POL-POC-002 | Internal Committee (IC) Constitution Standards | All | v1.2 |
| POL-POC-003 | POCSO Audit Independence Policy | 126 | v1.0 |

### Category 6 — Data & Privacy

| Policy ID | Policy Name | Scope | Current Version |
|---|---|---|---|
| POL-DPR-001 | Grievance Data Masking & DPDPA Compliance | 126, 127 | v1.1 |
| POL-DPR-002 | Audit Record Retention Policy | 121 | v1.0 |
| POL-DPR-003 | Audit Data Access & Sharing Policy | All | v1.2 |

---

## 5. Policy Detail View

**URL:** `/group/audit/policies/{policy_id}/`

### Header
```
CAPA Timelines & Severity Classification Policy              [Edit]  [Deprecate]  [Download PDF]
POL-CAPA-001 · v2.2 · Published · Category: CAPA & Escalation
Published: 15-Jan-2026 · Review Due: 15-Jan-2027 · Approved by: T. Subramaniam (121)
```

### Section 1 — Policy Metadata

| Field | Value |
|---|---|
| Policy ID | POL-CAPA-001 |
| Full Title | CAPA Timelines & Severity Classification Policy |
| Category | CAPA & Escalation |
| Purpose | Defines how audit findings are classified by severity (Critical, Major, Minor) and the mandatory timelines for root cause submission, action planning, and closure for each severity level |
| Scope | All branches · All finding sources (audit, inspection, affiliation, grievance) |
| Effective Date | 15-Jan-2026 |
| Review Due | 15-Jan-2027 |
| Owner | Group Internal Audit Head (121) |
| Approver | Group Internal Audit Head (121) · CEO for major revisions |
| Regulatory Basis | RTE Act 2009 · CBSE Affiliation Bylaws 2018 · POCSO Act 2012 (for Critical severity findings) |
| Related Policies | POL-CAPA-002 (Root Cause Analysis) · POL-CAPA-004 (Escalation Rules) |
| Related Platform Pages | P-15 (CAPA Register) · P-16 (Escalation Manager) |

### Section 2 — Policy Content

Full policy text, structured with headings and sub-headings. Rendered in the platform with formatting (bold, bullets, tables). Not a static PDF — version-controlled text.

**Example policy content for POL-CAPA-001:**

```
1. Severity Classification

1.1 Critical Severity
   Definition: Finding that poses immediate risk to student safety, legal compliance,
   or institutional accreditation.
   Examples: Fire exit blocked, expired fire NOC, POCSO violation, structural
   safety deficiency, unlicensed operation.

   Mandatory timelines:
     Root cause submission: within 3 working days of finding
     Action plan submission: within 5 working days of finding
     Corrective action completion: within 15 working days of finding
     Verification: within 3 working days of action completion
     Closure approval: CEO / Chairman required

   Auto-escalation: Escalated to CEO on day 1 if not acknowledged.

1.2 Major Severity
   Definition: Significant non-conformance affecting quality, financial integrity,
   or regulatory compliance but not posing immediate safety risk.
   Examples: Fee reconciliation discrepancy > ₹50,000, lesson plan non-submission
   for 2+ weeks, affiliation document expired.

   Mandatory timelines:
     Root cause submission: within 7 working days
     Action plan submission: within 10 working days
     Corrective action completion: within 30 working days
     Verification: within 7 working days of action completion
     Closure approval: Internal Audit Head (121) required

   Auto-escalation: To Zone Director at day 7; to Audit Head at day 21; to CEO at day 35.

1.3 Minor Severity
   Definition: Process gap or observation that does not affect immediate safety,
   financial integrity, or regulatory compliance.
   Examples: Attendance register not updated daily, notice board outdated,
   staff attendance late entry.

   Mandatory timelines:
     Root cause submission: within 14 working days
     Action plan submission: within 21 working days
     Corrective action completion: within 60 working days
     Closure approval: Process Improvement Coordinator (128) authority

   Auto-escalation: To Zone Director at day 14; to Audit Head at day 45.

2. Cross-Classification Rules
   2.1 A finding initially classified as Minor that recurs at the same branch
       within 12 months is automatically upgraded to Major.
   2.2 A finding initially classified as Major that recurs at the same branch
       within 6 months is automatically upgraded to Critical.
   2.3 Reclassification requires Audit Head (121) approval and must be
       documented in the CAPA record.

3. Reporting
   3.1 The compliance score (P-10) includes a CAPA Closure Rate dimension.
       Closure rates are calculated based on findings closed within the
       mandatory timeline for their severity.
   3.2 Open Critical findings older than 30 days are reported in the monthly
       MIS report (P-21) as a priority item.
```

### Section 3 — Version History

| Version | Date | Changed By | Approved By | Change Summary |
|---|---|---|---|---|
| v2.2 | 15-Jan-2026 | T. Subramaniam (121) | T. Subramaniam (121) | Added cross-classification rules (Section 2) |
| v2.1 | 01-Apr-2025 | T. Subramaniam (121) | T. Subramaniam (121) | Updated Minor closure timeline from 45 to 60 days |
| v2.0 | 01-Sep-2024 | T. Subramaniam (121) | P. Ramaiah (CEO) | Major revision — added Critical severity category; aligned to POCSO Act |
| v1.3 | 01-Mar-2024 | T. Subramaniam (121) | T. Subramaniam (121) | Added auto-escalation rules |

**`[View v2.1]`** `[View v2.0]` — links to read-only view of prior versions.

### Section 4 — Acknowledgement Tracking

| Staff Member | Role | Acknowledged | Date |
|---|---|---|---|
| S. Reddy | Inspection Officer (123) | ✅ | 16-Jan-2026 |
| T. Latha | Academic Quality Officer (122) | ✅ | 17-Jan-2026 |
| K. Ravi | Affiliation Officer (125) | ✅ | 16-Jan-2026 |
| M. Srinivas | Grievance Audit Officer (126) | ✅ | 18-Jan-2026 |
| K. Venkatesh | Process Improvement Coordinator (128) | ✅ | 16-Jan-2026 |
| P. Sunitha | Compliance Data Analyst (127) | ✅ | 17-Jan-2026 |
| R. Sharma | (New hire — joined Feb-2026) | ❌ Pending | — |
| T. Subramaniam | Internal Audit Head (121) | ✅ (author) | 15-Jan-2026 |

**`[Send Reminder to Pending]`** — sends automated reminder to R. Sharma.

**My acknowledgement status** (logged-in user view):
```
You have read and acknowledged this policy.  ✅  Acknowledged on 16-Jan-2026
```

Or if pending:
```
⚠️ You have not yet acknowledged this policy.
[I have read and understood this policy — Acknowledge Now]
```

---

## 6. Modals

### Modal 1 — New Policy

**Trigger:** `[+ New Policy]`

**Form:**
```
Policy Name: [___________________________]
Category: [Audit Governance / CAPA & Escalation / Scoring / Inspection / POCSO / Data ▼]
Purpose (one-line): [___________________________]
Scope: [___________________________]
Owner: [121 — Audit Head ▼]  (or assign to another role)
Regulatory Basis: [Tag input — type regulation name + Enter]
Related Policies: [Multi-select from existing ▼]
Related Platform Pages: [Multi-select ▼]
Review Cycle: [Annual / Semi-annual / On regulation change ▼]
Acknowledgement Required From: [Multi-select roles ▼]
```

Opens full policy text editor after creation.

---

### Modal 2 — Schedule Review

**Trigger:** `[Review Due]` action or `[Review Due List]` button.

**Form:**
```
Policy: CAPA Timelines & Severity Classification Policy v2.2
Last reviewed: 15-Jan-2026  ·  Review due: 15-Jan-2027

Review Options:
  ◉ Policy is still current — extend review date by 1 year (no changes needed)
  ○ Minor update required — will edit inline and republish as v2.3
  ○ Major revision required — will create draft and seek CEO approval

Notes: [___________________________]
New Review Due Date: [15-Jan-2027 ▼]
```

---

## 7. Policy Editor

Full-page editor (same structure as Report editor in P-21):
- Left panel: Policy sections navigator
- Centre: Rich text editor (bold, headings, bullets, tables, numbered lists)
- Right panel: Metadata + version status + comments (for review cycle)

Toolbar:
```
[Save Draft]  [Preview PDF]  [Submit for Approval]
```

Major version changes (v2.x → v3.0) require CEO approval. Minor changes (v2.1 → v2.2) require Audit Head self-approval.

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Policy created | "POL-CAPA-006 created — Annual Audit Self-Assessment Policy · Draft" | Success (green) |
| Policy published | "POL-CAPA-001 v2.2 published — 8 staff notified to acknowledge" | Success (green) |
| Policy acknowledged | "POL-CAPA-001 acknowledged by S. Reddy · 16-Jan-2026" | Success (green) |
| Reminder sent | "Acknowledgement reminder sent to R. Sharma — POL-CAPA-001" | Info (blue) |
| Policy review due | "⚠️ POL-CAPA-001 annual review due — 15-Jan-2027" | Warning (amber) |
| Policy overdue | "🔴 POL-INS-002 is overdue for review by 45 days" | Error (red) |
| Version history viewed | "Viewing archived version: POL-CAPA-001 v2.0 (read-only)" | Info (blue) |

---

## 9. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No policies | Documents outline | "No audit policies in the repository. Add your first policy to establish governance standards." | `[+ New Policy]` |
| Filter returns zero | Magnifying glass | "No policies match your filters." | `[Reset Filters]` |
| No overdue reviews | Clock with green tick | "All policies are within their review cycle — no overdue reviews." | — |

---

## 10. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Policy library table | Skeleton rows → data | < 500ms |
| Policy detail page | Section skeletons → populated | < 1s |
| Version history | Skeleton table → data | < 500ms |
| Policy editor | Section tree + editor → populated | < 1s |
| Acknowledgement table | Skeleton rows → data | < 500ms |

---

## 11. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/policies/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | List policies (filterable) | G1+ |
| 2 | GET | `/{policy_id}/` | Policy detail with current content | G1+ |
| 3 | POST | `/` | Create new policy (draft) | 121 |
| 4 | PATCH | `/{policy_id}/` | Update policy content or metadata | 121 |
| 5 | POST | `/{policy_id}/submit-approval/` | Submit for approval | 121 |
| 6 | POST | `/{policy_id}/approve/` | Approve and publish | 121 (minor) · G4 (major) |
| 7 | POST | `/{policy_id}/deprecate/` | Deprecate policy | 121 |
| 8 | GET | `/{policy_id}/versions/` | Version history | G1+ |
| 9 | GET | `/{policy_id}/versions/{v}/` | Archived version content (read-only) | G1+ |
| 10 | POST | `/{policy_id}/acknowledge/` | Record user acknowledgement | Any logged-in user in ack list |
| 11 | GET | `/{policy_id}/acknowledgements/` | Who has/hasn't acknowledged | 121 |
| 12 | POST | `/{policy_id}/remind/` | Send acknowledgement reminder | 121 |
| 13 | GET | `/review-due/` | Policies due or overdue for review | G1+ |
| 14 | POST | `/{policy_id}/schedule-review/` | Mark reviewed, set next review date | 121 |
| 15 | GET | `/export/` | Export all policies as PDF bundle | G1+ |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Policy table load | Page load | `hx-get=".../policies/"` | `#policy-table` | `innerHTML` | — |
| Filter change | Select change | `hx-get` with filters | `#policy-table` | `innerHTML` | — |
| Policy detail | Row `[View]` click | — | Full page navigate | — | Sub-page |
| New policy modal | `[+ New Policy]` click | — | `#modal-content` | `innerHTML` | Modal → redirect to editor |
| Acknowledge | `[Acknowledge Now]` click | `hx-post=".../policies/{id}/acknowledge/"` | `#ack-status` | `innerHTML` | Toast + badge update |
| Send reminder | `[Send Reminder]` click | `hx-post=".../policies/{id}/remind/"` | `#remind-result` | `innerHTML` | Toast |
| Review modal | `[Review Due]` click | — | `#modal-content` | `innerHTML` | Modal |
| Submit review | Form submit | `hx-post=".../policies/{id}/schedule-review/"` | `#review-result` | `innerHTML` | Toast + date update |
| Version history | Tab/link click | `hx-get=".../policies/{id}/versions/"` | `#version-panel` | `innerHTML` | Side panel |
| Archived version | `[View v2.0]` click | `hx-get=".../policies/{id}/versions/{v}/"` | `#policy-content` | `innerHTML` | Read-only overlay |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
