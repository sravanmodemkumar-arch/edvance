# A-23 — Approval Workflow Hub

> **URL:** `/school/admin/approvals/`
> **File:** `a-23-approval-workflow-hub.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Principal (S6) — full · VP Academic (S5) — own items · VP Admin (S5) — own items · Promoter (S7) — Promoter-level items

---

## 1. Purpose

Centralised queue of all pending approvals for the school's management. Every action that requires sign-off — staff leave, purchase requests, exam schedules, result publication, fee waivers, TC issuance, student disciplinary actions, policy changes — flows through this hub. The approver sees all items waiting for their action in one place instead of hunting across modules.

**Indian school approval culture:** Indian schools (especially private unaided) operate on a hierarchical approval model. Teachers cannot act without HOD approval; HODs cannot act without VP approval; VPs cannot act without Principal approval for anything significant. This formal chain ensures accountability but creates bottlenecks if there's no digital hub. This page eliminates the "I sent the paper but Principal didn't see it" problem.

---

## 2. Page Layout

### 2.1 Header
```
Approval Workflow Hub                        [My Approvals ▼]  [Delegated ▼]  [History]
Pending for me: 12  ·  Overdue (>3 days): 2  ·  Total institution pending: 28
Date: [26 Mar 2026]
```

### 2.2 Filter/View Bar
```
[All Types ▼]  [All Requesters ▼]  [Priority: All ▼]  [Date: All ▼]
```

---

## 3. Pending Approvals Queue

Default view: sorted by urgency (overdue first, then by days pending).

| # | Type | Description | Requested By | Date | Days Pending | Urgency | Action |
|---|---|---|---|---|---|---|---|
| 1 | Staff Leave | Mr. Rajan T — CL 28–29 Mar (2 days) | Mr. Rajan T | 25 Mar | 1 day | 🟡 Normal | [Review] |
| 2 | Purchase Request | 2 AC units for staffroom — ₹1.8L | VP Admin | 22 Mar | 4 days | 🔴 Overdue | [Review] |
| 3 | Result Publication | Class IX Unit Test 2 — 312 students | VP Academic | 24 Mar | 2 days | 🟡 Normal | [Review] |
| 4 | Fee Waiver | Partial waiver — Aryan Sharma, Class XII | Accountant | 20 Mar | 6 days | 🔴 Overdue | [Review] |
| 5 | TC Issuance | TC for Priya B, Class VIII (family shifting) | Admin Officer | 25 Mar | 1 day | 🟡 Normal | [Review] |
| 6 | Exam Schedule | Pre-Board 2 schedule — Class X, XII | VP Academic | 24 Mar | 2 days | 🟡 Normal | [Review] |

---

## 4. Approval Types Matrix

| Approval Type | Default Approver | Escalate To | Auto-Approve if >7 days |
|---|---|---|---|
| Staff Leave (CL, SL, 1–3 days) | VP Academic (teaching) / VP Admin (non-teaching) | Principal | No |
| Staff Leave (EL, 4+ days) | VP → Principal | Promoter | No |
| Maternity Leave | Principal | Promoter (for salary continuity) | No |
| Purchase Request (< ₹10,000) | VP Admin | — | No |
| Purchase Request (₹10,000–₹1L) | Principal | — | No |
| Purchase Request (> ₹1L) | Principal → Promoter | — | No |
| Exam Schedule (internal) | VP Academic | Principal | No |
| Exam Schedule (board) | Principal | — | No |
| Result Publication (internal) | VP Academic | Principal | No |
| Result Publication (board) | Principal only | — | No |
| Fee Waiver (< ₹5,000) | Accountant → Principal | — | No |
| Fee Waiver (> ₹5,000) | Principal → Promoter | — | No |
| TC Issuance | Principal | — | No |
| Staff Appointment | Principal | Promoter (if above VP level) | No |
| Disciplinary Action | Principal | Promoter (for dismissal) | No |
| Policy Change | Principal | Promoter | No |
| Circular (standard) | VP Academic / VP Admin | — | No |
| Circular (about discipline/fees) | Principal | — | No |

---

## 5. Approval Detail Drawer (universal, all types)

**560px wide, tabs: Details · Context · History · Action**

**Details tab:** Full description of what is being requested — fields vary by type
- Leave: Staff name, leave type, dates, reason, balance remaining, team impact
- Purchase: Item description, vendor, quotations (upload slots), budget code, justification
- Result: Exam name, class, statistics (avg, pass %, top/bottom students), anomaly flags
- Fee waiver: Student name, fee outstanding, waiver amount, reason, family background
- TC: Student name, class, reason for transfer, last attendance date, dues status

**Context tab:**
- Related records (previous purchases of same category, last fee waiver for this student, etc.)
- Flags: "Last purchase > ₹25,000: no quotation uploaded" | "Student has 2 prior fee waivers this year"

**History tab:**
- Timeline of who touched this request and what they did

**Action tab:**
- [✅ Approve] — with optional note
- [↩ Return for More Info] — reason required; returns to requester
- [❌ Reject] — reason required; notifies requester
- [🔀 Delegate to …] — assign to another approver (e.g., if Principal is on leave)
- TOTP required for: fee waivers > ₹5,000, salary changes, dismissal decisions

---

## 6. Delegation Settings

**[Set Delegation]** — if Principal is going on leave:
- Delegate all my approvals to: [VP Academic / VP Admin / select staff]
- Duration: from [date] to [date]
- Types to delegate: all / specific types (e.g., leave only)
- Delegated approvals are logged with "delegated by Principal [name]"

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/approvals/?status=pending&approver=me` | My pending approvals |
| 2 | `GET` | `/api/v1/school/{id}/approvals/{approval_id}/` | Approval detail |
| 3 | `POST` | `/api/v1/school/{id}/approvals/{approval_id}/decide/` | Approve/return/reject |
| 4 | `POST` | `/api/v1/school/{id}/approvals/{approval_id}/delegate/` | Delegate to another |
| 5 | `GET` | `/api/v1/school/{id}/approvals/history/` | Completed approvals history |
| 6 | `GET` | `/api/v1/school/{id}/approvals/stats/` | KPI strip stats |
| 7 | `POST` | `/api/v1/school/{id}/approvals/delegation/` | Set up delegation rule |

---

## 8. Business Rules

- No item can be auto-approved; all require explicit human approval
- Rejections require reason (minimum 20 characters) — prevents "rejected without explanation" culture
- Promoter items: only Promoter can approve; delegation allowed only to Principal
- Overdue approvals (> configured threshold, default 3 days) → daily email/WhatsApp reminder to approver
- Result publication once approved is irreversible in the current version (audit requirement); corrections require "Amendment Publication" workflow

---

## 9. HTMX Patterns

### Live badge update (pending count in nav)
```html
<span id="approval-badge"
      hx-get="/api/v1/school/{{ school_id }}/approvals/stats/"
      hx-trigger="every 2m"
      hx-target="#approval-badge"
      hx-swap="outerHTML">
  12
</span>
```

### Inline approve
```html
<form hx-post="/api/v1/school/{{ school_id }}/approvals/{{ approval_id }}/decide/"
      hx-target="#approval-row-{{ approval_id }}"
      hx-swap="outerHTML">
  <input type="hidden" name="decision" value="APPROVED">
  <button type="submit" class="btn-success-sm">✅ Approve</button>
</form>
```

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
