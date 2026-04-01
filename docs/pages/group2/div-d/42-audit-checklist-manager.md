# 42 — Audit Checklist Manager

- **URL:** `/group/finance/audit/checklists/`
- **Template:** `portal_base.html`
- **Priority:** P2
- **Role:** Internal Auditor G1 (primary)

---

## 1. Purpose

The Audit Checklist Manager creates and manages standardised audit checklists used during branch audits. A checklist template defines the specific checks to be performed during an audit — fee collection verification, cash box count, vendor invoice matching, payroll register review, bank statement check, etc. Checklists ensure consistency across audits regardless of which auditor performs them.

During an audit (from the Audit Planner on Page 39), the assigned auditor works through the checklist, marking each item as Pass, Fail, or N/A. Failed items automatically generate draft findings. The checklist completion percentage is tracked and required before an audit can be marked complete.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Internal Auditor | G1 | Full CRUD on checklists + use during audits |
| Group Finance Manager | G1 | Read — review checklist coverage |
| Group CFO | G1 | Read — checklist summary |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Internal Audit → Audit Checklist Manager
```

### 3.2 Page Header
- **Title:** `Audit Checklist Manager`
- **Subtitle:** `[N] Checklist Templates`
- **Right-side controls:** `[+ New Checklist Template]` `[Export ↓]`

---

## 4. Main Table — Checklist Templates

| Column | Type | Sortable |
|---|---|---|
| Template Name | Text | ✅ |
| Type | Badge: Full Audit · Targeted · Surprise · Annual | ✅ |
| Version | Text | ✅ |
| Items Count | Number | ✅ |
| Categories Covered | Text | ✅ |
| Status | Badge: Active · Draft · Archived | ✅ |
| Last Updated | Date | ✅ |
| Used In Audits | Count | ✅ |
| Actions | View · Edit · Clone · Archive · Delete (draft) | — |

---

## 5. Drawers

### 5.1 Drawer: `checklist-create` — Create Template
- **Trigger:** [+ New Checklist Template]
- **Width:** 800px

| Field | Type | Required |
|---|---|---|
| Template Name | Text | ✅ |
| Type | Select | ✅ |
| Description | Textarea | ❌ |
| Categories | Multi-select: Fee · Procurement · Payroll · Assets · Compliance · IT · Hostel | ✅ |

**Checklist Items (dynamic):**

For each category selected, add items:

| # | Item Description | Category | Mandatory | Pass/Fail/NA |
|---|---|---|---|---|
| 1 | Verify fee collection register matches bank credits | Fee | ✅ | — |
| 2 | Check cash box balance against petty cash ledger | Fee | ✅ | — |
| 3 | Match vendor invoices to PO register | Procurement | ✅ | — |
| 4 | Verify payroll register signatures | Payroll | ✅ | — |
| 5 | Check if duplicate receipts exist this quarter | Fee | ✅ | — |
| [+ Add Item] | | | | |

- Items can be reordered via drag-and-drop
- [Cancel] [Save Draft] [Activate Template]

### 5.2 Drawer: `checklist-view` — View Template
- All items in read-only format
- Usage history (audits this template was used in)

### 5.3 Drawer: `checklist-run` — Run Checklist During Audit (embedded in audit workflow)
- **Width:** 800px

For each item:
| Check | Description | Result | Notes |
|---|---|---|---|
| [ ] | [Item text] | Pass / Fail / N/A | [Optional notes] |

- Progress: [X of Y items completed]
- Failed items: auto-generate draft finding prompt
- [Save Progress] [Submit Checklist]

---

## 6. Charts

### 6.1 Checklist Pass Rate by Branch (Bar)
- **Y-axis:** % of items passed in last audit
- **Sort:** Asc (lowest first)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Template created | "Checklist template '[Name]' created." | Success | 4s |
| Template activated | "Checklist '[Name]' is now active." | Success | 3s |
| Template archived | "Checklist '[Name]' archived." | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No templates | "No checklist templates" | "Create a checklist template to standardise audits." | [+ New Template] |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Create drawer | Spinner + dynamic form |

---

## 10. Role-Based UI Visibility

| Element | Internal Auditor G1 | Finance Mgr G1 |
|---|---|---|
| [+ New Template] | ✅ | ❌ |
| [Edit] | ✅ | ❌ |
| [Archive] | ✅ | ❌ |
| [Run Checklist] | ✅ | ❌ |
| View all templates | ✅ | ✅ |
| Export | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/audit/checklists/` | JWT (G1+) | Template list |
| POST | `/api/v1/group/{id}/finance/audit/checklists/` | JWT (G1) | Create template |
| GET | `/api/v1/group/{id}/finance/audit/checklists/{cid}/` | JWT (G1+) | Template detail |
| PUT | `/api/v1/group/{id}/finance/audit/checklists/{cid}/` | JWT (G1) | Update |
| POST | `/api/v1/group/{id}/finance/audit/checklists/{cid}/activate/` | JWT (G1) | Activate |
| POST | `/api/v1/group/{id}/finance/audit/checklists/{cid}/clone/` | JWT (G1) | Clone |
| DELETE | `/api/v1/group/{id}/finance/audit/checklists/{cid}/` | JWT (G1) | Delete draft |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
