# 37 — Scholarship Finance Approval Workflow

- **URL:** `/group/finance/scholarship/approvals/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Scholarship Finance Officer G3 (primary)

---

## 1. Purpose

The Scholarship Finance Approval Workflow manages the financial release approval stage after scholarships are academically approved by the Group Scholarship Manager (Division C). Before disbursement can proceed, the Finance Officer must verify: the student's fee account balance (to apply scholarship against outstanding dues), bank account details are verified, and the disbursement is within budget. This page is the financial gate before money moves.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Scholarship Finance Officer | G3 | Full read + approve/reject |
| Group CFO | G1 | Read — financial impact |
| Group Scholarship Manager (Div C) | G3 | Read — approval status |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Scholarship Finance → Finance Approval Workflow
```

### 3.2 Page Header
- **Title:** `Scholarship Finance Approval Workflow`
- **Subtitle:** `[N] Awaiting Finance Approval · AY [Year]`
- **Right-side controls:** `[AY ▾]` `[Status ▾]` `[Export ↓]`

---

## 4. Main Table

| Column | Type | Sortable |
|---|---|---|
| Scholarship ID | Text | ✅ |
| Student Name | Text | ✅ |
| Branch | Text | ✅ |
| Scholarship Type | Badge | ✅ |
| Approved Amount | ₹ | ✅ |
| Academic Approval By | Text | ✅ |
| Academic Approval Date | Date | ✅ |
| Fee Outstanding | ₹ | ✅ |
| Bank Account | Badge: Verified · Missing | ✅ |
| Budget Available | Badge: Yes · No | ✅ |
| Finance Status | Badge: Pending Finance · Finance Approved · Finance Rejected | ✅ |
| Actions | Review · Approve · Reject | — |

**Filters:** Type · Finance Status · Branch · Budget Available
**Pagination:** 25 rows/page

---

## 5. Drawers

### 5.1 Drawer: `finance-review` — Finance Review
- **Width:** 720px

**Finance Checks Section:**

| Check | Status | Notes |
|---|---|---|
| Budget Available | ✅ / ❌ | ₹[X] remaining in [Category] budget |
| Bank Account Verified | ✅ / ❌ | [Bank Name] · IFSC [Code] |
| Outstanding Dues | ₹[X] | Will scholarship apply against dues? |
| Previous Scholarship | None / [Details] | Check for duplicate disbursement |

**Decision Form:**
| Field | Type | Required |
|---|---|---|
| Finance Decision | Radio: Approve · Reject | ✅ |
| Apply Against Dues | Toggle | ❌ (default: NO — disburse to bank) |
| Notes | Textarea | ✅ |

- [Cancel] [Submit Finance Decision]

---

## 6. Bulk Action

- Select multiple with all checks green → [Bulk Finance Approve]

---

## 7. Charts

### 7.1 Approval Status Funnel (Bar)
- Stages: Academic Approved → Finance Pending → Finance Approved → Disbursed

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Finance approved | "Finance approval granted for [Student]. Ready to disburse." | Success | 4s |
| Finance rejected | "Finance approval rejected for [Student]. Academic team notified." | Warning | 4s |
| Bulk approved | "[N] scholarships approved for disbursement." | Success | 4s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No pending approvals | "No pending approvals" | "All scholarships have finance decisions." |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/scholarship/approvals/` | JWT (G1+) | Approval queue |
| GET | `/api/v1/group/{id}/finance/scholarship/approvals/{sid}/` | JWT (G1+) | Detail |
| PUT | `/api/v1/group/{id}/finance/scholarship/approvals/{sid}/decide/` | JWT (G3) | Finance decision |
| POST | `/api/v1/group/{id}/finance/scholarship/approvals/bulk-approve/` | JWT (G3) | Bulk approve |

---

## 11. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../approvals/?status=` | `#approvals-table` | `innerHTML` |
| Review drawer | `click` | GET `.../approvals/{id}/` | `#drawer-body` | `innerHTML` |
| Submit decision | `submit` | PUT `.../approvals/{id}/decide/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
