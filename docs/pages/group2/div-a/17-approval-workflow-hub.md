# 17 — Approval Workflow Hub

> **URL:** `/group/gov/approvals/`
> **File:** `17-approval-workflow-hub.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Chairman G5 (all) · MD G5 · CEO G4 · President G4 · VP G4 (their queues only)

---

## 1. Purpose

Central queue for all approval workflows across the institution group. Instead of approvals
arriving via WhatsApp or email, every structured decision requiring sign-off flows through this hub.
Each role sees only the approvals routed to them. Chairman sees all.

Approval types routed through this hub:
- Annual Strategic Plan
- New Branch Activation
- Branch Deactivation
- Exam Schedule (G4 President)
- Exam Result Publication (cross-branch results release)
- Fee Structure Change
- Scholarship Waiver (large amounts)
- Staff Transfer Between Branches
- Policy Override
- Budget Variance Request
- Grievance Escalation Directive
- Board Resolution

---

## 2. Role Access

| Role | Sees | Notes |
|---|---|---|
| Chairman | All approval types across all roles | Override authority |
| MD | MD-level items (branch activation, policy, user provisioning) | |
| CEO | CEO-level items (ops policy, fee change, escalation directive) | |
| President | Academic items only (exam schedules) | |
| VP | Ops items (staff transfer, procurement, infrastructure) | |
| Trustee | ❌ | |
| Advisor | ❌ | |
| Exec Secretary | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Approval Workflow Hub
```

### 3.2 Page Header
```
Approval Workflow Hub                                  [Delegate ▼]  [Export Audit ↓]
[N] pending · [N] approved this month · [N] rejected   (Chairman/MD only)
```

### 3.3 Tab Navigation
```
My Queue ([N])  |  Sent for Approval  |  All Approvals (Chairman/MD)  |  Completed
```

---

## 4. My Queue Tab (default)

> Approvals currently awaiting this role's action.

**Search:** Item title, branch name, submitter name. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Type | Multi-select | All approval types (see list above) |
| Branch | Multi-select | |
| Priority | Select | Any · Urgent · Normal |
| Age | Select | Any · 0–3 days · 4–7 days · >7 days |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Text | ✅ | APR-2026-0042 |
| Type | Badge | ✅ | Colour-coded by type |
| Priority | Badge | ✅ | Urgent (red) · Normal (grey) |
| Subject / Title | Text (truncated 80) | ✅ | |
| Branch | Text | ✅ | Or "Group-level" |
| Submitted By | Text | ✅ | Name + role |
| Submitted On | Date | ✅ | |
| Days Pending | Number | ✅ | Red if >7 |
| Actions | — | ❌ | [Approve] [Reject] [View] [Delegate] |

**Default sort:** Days Pending descending (oldest first).

**Pagination:** 25/page.

**Inline Approve:** `hx-post` on [Approve] → success: row disappears + toast.
Supported only for simple, low-risk approval types (e.g. exam schedule without conflicts).

**[View] action:** Opens `approval-detail` drawer for full context before deciding.

**[Delegate] action:** Opens delegate modal (Chairman/MD only).

**Bulk actions (Chairman/MD):**
- Select rows → [Approve All Selected] (non-conflicting types only) → confirm modal listing all items.

---

## 5. Sent for Approval Tab

> Items this role has submitted to others for approval.

**Columns:** Same as My Queue but with "Sent To" column instead of "Actions", and "Status" column.

**Status values:** Pending · Approved · Rejected · Withdrawn.

**Row action:** [Withdraw] (pulls back submitted item — allowed before action taken).

---

## 6. All Approvals Tab (Chairman / MD only)

> Full cross-role approval visibility.

Same table structure with added columns:
- Assigned To (which role's queue it's in)
- Routed Via (auto-routed or manual)

Filters add: "Assigned To" role filter.

---

## 7. Completed Tab

> Approved and rejected items — audit trail.

Same columns + "Decision" (Approved/Rejected) + "Decision By" + "Decision Date" + "Reason (if rejected)".

**Cannot be altered** — read-only, immutable record.

**Export:** CSV of completed approvals for selected date range.

---

## 8. Drawers & Modals

### 8.1 Drawer: `approval-detail`
- **Trigger:** Any row → [View]
- **Width:** 640px
- **Tabs:** Details · History · Action

#### Tab: Details
- Full approval request details (varies by type):
  - Annual Plan: Plan summary, financial totals, enrollment targets
  - Exam Schedule: Branch, date, stream, class, conflict status
  - Fee Change: Old fee vs new fee, % change, branch, reason
  - Staff Transfer: From branch, to branch, staff name, role, reason
  - etc.
- Attachments: Any documents uploaded by submitter
- Submitter's notes

#### Tab: History
- Previous approvals/rejections for same type from same branch (last 5)
- Pattern flags: "This branch has submitted 4 exam schedule rejections this year"

#### Tab: Action
| Action | Visible When |
|---|---|
| [Approve] + optional comment | Status = Pending, role is approver |
| [Reject] + required reason | Status = Pending, role is approver |
| [Delegate to…] + select target role | Chairman/MD only |
| [Override Approval] + reason | Chairman only — can force-approve rejected items |
| [Withdraw] | Submitter only, before decision |

**Approve:** POST → approval recorded → submitter notified via WhatsApp → audit entry.

**Reject:** Required reason (min 30 chars, 500 limit). Submitter notified with reason.

**Override (Chairman):** Overrides any previous rejection. Requires reason.

### 8.2 Modal: `bulk-approve-confirm`
- **Width:** 480px
- **Content:** Lists all selected items with type + branch + subject
- **Warning:** If any selected are Urgent or have conflicts, they are highlighted
- **Buttons:** [Approve All [N] Items] + [Cancel]

### 8.3 Modal: `delegate-approval`
- **Width:** 420px
- **Fields:** Delegate to (select from same-level or lower role that can approve this type) · Note (optional)
- **Buttons:** [Delegate] + [Cancel]

### 8.4 Modal: `withdraw-approval`
- **Width:** 380px
- **Content:** "Withdraw this approval request?"
- **Fields:** Reason (optional)
- **Buttons:** [Withdraw] + [Cancel]

---

## 9. Charts

### 9.1 Approval Volume by Type (this month)
- **Type:** Horizontal bar chart
- **Data:** Count of approvals per type (pending / approved / rejected)
- **Colour:** Grey (pending) · Green (approved) · Red (rejected)
- **Export:** PNG

### 9.2 Avg Days to Decision by Type
- **Type:** Bar chart
- **Data:** Average days between submission and decision per approval type
- **Benchmark:** Group SLA target (e.g. 3 days for exam schedules)
- **Export:** PNG

---

## 10. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Approval granted | "[Type] approved. [Submitter] notified." | Success | 4s |
| Rejection submitted | "[Type] rejected. Reason sent to [Submitter]." | Success | 4s |
| Bulk approve | "[N] items approved" | Success | 4s |
| Delegated | "Approval delegated to [Role]. [Role] notified." | Info | 4s |
| Withdrawn | "Approval request withdrawn" | Info | 4s |
| Override | "Chairman override applied. Previous rejection reversed." | Warning | 6s |
| Error | "Failed to process approval. Try again." | Error | Manual |

---

## 11. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| My Queue empty | "You're all caught up" | "No approvals are waiting for your action" | — |
| No sent items | "Nothing sent yet" | "Submissions you make for others' approval will appear here" | — |
| Completed tab empty | "No completed approvals" | "Approved or rejected items will appear here" | — |

---

## 12. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 4 tab headers + table (8 rows) |
| Tab switch | Inline skeleton rows for new tab |
| Approval detail drawer | Spinner in drawer |
| Approve/Reject action | Spinner in action buttons + button disabled |
| Bulk approve submit | Full-page overlay "Processing [N] approvals…" |

---

## 13. Role-Based UI Visibility

| Element | Chairman | MD | CEO | President | VP |
|---|---|---|---|---|---|
| My Queue — Exam type | ✅ | ✅ | ✅ | ✅ | ❌ |
| My Queue — Fee type | ✅ | ✅ | ✅ | ❌ | ✅ |
| My Queue — Annual Plan | ✅ | ✅ | ❌ | ❌ | ❌ |
| All Approvals tab | ✅ | ✅ | ❌ | ❌ | ❌ |
| [Delegate] action | ✅ | ✅ | ❌ | ❌ | ❌ |
| [Override] action | ✅ | ❌ | ❌ | ❌ | ❌ |
| Bulk Approve | ✅ | ✅ | ❌ | ❌ | ❌ |
| [Export Audit] | ✅ | ✅ | ❌ | ❌ | ❌ |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/approvals/?queue=mine&status=pending` | JWT | My pending queue |
| GET | `/api/v1/group/{id}/approvals/?submitted_by=me` | JWT | Sent for approval |
| GET | `/api/v1/group/{id}/approvals/?status=completed` | JWT | Completed |
| GET | `/api/v1/group/{id}/approvals/` | JWT (G5) | All approvals |
| GET | `/api/v1/group/{id}/approvals/{aid}/` | JWT | Approval detail |
| POST | `/api/v1/group/{id}/approvals/{aid}/approve/` | JWT | Approve |
| POST | `/api/v1/group/{id}/approvals/{aid}/reject/` | JWT | Reject with reason |
| POST | `/api/v1/group/{id}/approvals/{aid}/delegate/` | JWT (G5/G4) | Delegate |
| POST | `/api/v1/group/{id}/approvals/{aid}/withdraw/` | JWT | Withdraw |
| POST | `/api/v1/group/{id}/approvals/{aid}/override/` | JWT (G5 Chairman) | Override |
| POST | `/api/v1/group/{id}/approvals/bulk-approve/` | JWT (G5/G4) | Bulk approve list |
| GET | `/api/v1/group/{id}/approvals/charts/volume/` | JWT | Volume by type chart |
| GET | `/api/v1/group/{id}/approvals/charts/avg-days/` | JWT | Avg days chart |

---

## 15. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | GET `.../approvals/?tab=queue\|sent\|all\|completed` | `#approvals-tab-content` | `innerHTML` |
| Search | `input delay:300ms` | GET `.../approvals/?q=` | `#approvals-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../approvals/?type=&branch=&priority=&age=` | `#approvals-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../approvals/?sort=&dir=` | `#approvals-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../approvals/?page=` | `#approvals-table-section` | `innerHTML` |
| Open approval detail drawer | `click` | GET `.../approvals/{aid}/` | `#drawer-body` | `innerHTML` |
| Approve inline | `click` | POST `.../approvals/{aid}/approve/` | `#approval-row-{aid}` | `outerHTML` |
| Bulk approve (confirm modal) | `click` | POST `.../approvals/bulk-approve/` | `#approvals-tab-content` | `innerHTML` |
| Withdraw | `click` | POST `.../approvals/{aid}/withdraw/` | `#approval-row-{aid}` | `outerHTML` |
| Override (Chairman) | `click` | POST `.../approvals/{aid}/override/` | `#approval-row-{aid}` | `outerHTML` |
| Pending queue auto-refresh | `every 60s` | GET `.../approvals/stats/` | `#approvals-pending-badge` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
