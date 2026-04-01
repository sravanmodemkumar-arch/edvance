# 38 — RTE Reimbursement Tracker

- **URL:** `/group/finance/scholarship/rte-reimbursement/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Scholarship Finance Officer G3 (primary) · CFO G1

---

## 1. Purpose

The RTE Reimbursement Tracker manages claims submitted to state education departments for reimbursement of fees waived for students admitted under the Right to Education Act (RTE) 25% quota. Schools are legally required to admit 25% of seats (Class 1 / LKG) to economically weaker section students at zero fee. The state government reimburses the school at a notified per-child rate. This reimbursement process is slow (6–18 months typically) and requires proper claim documentation.

The Finance Officer tracks: how many RTE students are enrolled per branch, the reimbursement per-child rate (state notification), total claim amount, claims submitted, claims received, and outstanding claims. Untracked RTE claims represent recoverable revenue that the group is leaving on the table.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Scholarship Finance Officer | G3 | Full read + manage claims |
| Group CFO | G1 | Read |
| Group Finance Manager | G1 | Read |
| Group Compliance Manager (Div N) | G1 | Read — compliance view |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Scholarship Finance → RTE Reimbursement Tracker
```

### 3.2 Page Header
- **Title:** `RTE Reimbursement Tracker`
- **Subtitle:** `AY [Year] · [N] RTE Students · ₹[Claimed] Claimed · ₹[Received] Received`
- **Right-side controls:** `[AY ▾]` `[Branch ▾]` `[+ New Claim]` `[Export ↓]`

---

## 4. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text | ✅ | ✅ |
| AY | Text | ✅ | ✅ |
| RTE Students | Count | ✅ | — |
| State Rate (per child) | ₹ | ✅ | — |
| Total Claim Amount | ₹ | ✅ | — |
| Claim Submitted | Badge: Yes · No | ✅ | ✅ |
| Submitted Date | Date | ✅ | — |
| Amount Received | ₹ | ✅ | — |
| Balance Pending | ₹ | ✅ | — |
| Status | Badge: Not Submitted · Submitted · Partial · Received · Rejected | ✅ | ✅ |
| Actions | View · Update · Submit Claim | — | — |

### 4.1 Filters
- Branch · AY · Status

### 4.2 Pagination
- 20 rows/page

---

## 5. Drawers

### 5.1 Drawer: `rte-claim` — Submit/Update RTE Claim
- **Width:** 680px

| Field | Type | Required |
|---|---|---|
| Branch | Select | ✅ |
| AY | Select | ✅ |
| RTE Students Enrolled | Number | ✅ |
| State Notified Rate (per child/year) | Number | ✅ |
| Total Claim Amount | Auto-calculated | — |
| Claim Submission Date | Date | ✅ |
| State Reference Number | Text | ❌ |
| Supporting Documents | File upload | ❌ |
| Amount Received (if partial) | Number | ❌ |
| Notes | Textarea | ❌ |

### 5.2 Drawer: `rte-detail` — Claim Detail
- Full claim history
- Student list (RTE students in this branch/AY)
- Payment receipts from state

---

## 6. Summary Section

| Item | Value |
|---|---|
| Total RTE Students (Group, AY) | [N] |
| Total Entitlement (all branches) | ₹[X] |
| Total Claimed | ₹[Y] |
| Total Received | ₹[Z] |
| Total Pending | ₹[W] |
| Not yet claimed | ₹[V] |

---

## 7. Charts

### 7.1 RTE Claim Status by Branch (Bar — Stacked)
- **Stacks:** Received · Pending · Not Claimed

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Claim submitted | "RTE claim for [Branch] submitted. Amount: ₹[X]." | Success | 4s |
| Receipt recorded | "RTE reimbursement of ₹[X] received for [Branch]." | Success | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No RTE students | "No RTE students" | "No RTE quota students enrolled for this AY." | — |
| Claims not submitted | "Claims pending" | "RTE claims not yet submitted for [N] branches." | [+ New Claim] |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/scholarship/rte/` | JWT (G1+) | RTE claim list |
| POST | `/api/v1/group/{id}/finance/scholarship/rte/` | JWT (G3) | Create/submit claim |
| GET | `/api/v1/group/{id}/finance/scholarship/rte/{rid}/` | JWT (G1+) | Detail |
| PUT | `/api/v1/group/{id}/finance/scholarship/rte/{rid}/` | JWT (G3) | Update claim |
| GET | `/api/v1/group/{id}/finance/scholarship/rte/export/` | JWT (G1+) | Export |

---

## 11. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../rte/?branch=&status=` | `#rte-table` | `innerHTML` |
| Claim drawer | `click` | GET `.../rte/claim-form/` | `#drawer-body` | `innerHTML` |
| Detail | `click` | GET `.../rte/{id}/` | `#drawer-body` | `innerHTML` |
| Submit | `submit` | POST `.../rte/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
