# A-18 — Staff Leave Management

> **URL:** `/school/admin/staff/leave/`
> **File:** `a-18-staff-leave-management.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** VP Admin (S5) — full · VP Academic (S5) — teaching staff approvals · Principal (S6) — full + final override · Admin Officer (S3) — view + manage application forms

---

## 1. Purpose

Manages the full lifecycle of staff leave requests — from application to approval, attendance marking, and balance deduction. The approval chain is: Staff applies → HOD reviews (for teaching staff) → VP Academic (teaching) or VP Admin (non-teaching) approves → Principal approves if > 3 days. Leave balance auto-updates attendance records.

---

## 2. Page Layout

### 2.1 Header
```
Staff Leave Management                       [+ Apply on Behalf]  [Export Leave Register]
Filter: Category [All ▼]  Dept [All ▼]  Status [Pending ▼]  Month [Mar 2026 ▼]
```

### 2.2 Summary Strip (current month)

| Type | Pending | Approved | Rejected | LWP this month |
|---|---|---|---|---|
| CL | 4 | 12 | 1 | 0 |
| EL | 2 | 5 | 0 | 0 |
| ML | 0 | 1 | 0 | 0 |
| SL | 2 | 8 | 1 | 0 |
| LWP | 1 | 2 | 0 | 3 |
| **Total** | **9** | **28** | **2** | **3** |

---

## 3. Pending Approvals Table

| Staff | Dept | Leave Type | From | To | Days | Applied On | Days Pending | Approver | Action |
|---|---|---|---|---|---|---|---|---|---|
| Mr. Rajan T | Maths | CL | 28 Mar | 29 Mar | 2 | 25 Mar | 1 day | VP Academic | [Approve] [Reject] [View] |
| Ms. Kavitha | Language | EL | 1 Apr | 5 Apr | 5 | 22 Mar | 4 days | VP Academic | [Approve] [Reject] [View] |
| Mr. Suresh | Admin | SL | 26 Mar | 27 Mar | 2 | 26 Mar | 0 days | VP Admin | [Approve] [Reject] [View] |

**[Approve]** and **[Reject]** inline via HTMX — no full page reload.
**[View]** → opens leave-approve drawer (480px) with full details.

---

## 4. Leave Register (All Approved)

| Staff | Dept | Leave Type | From | To | Days | Approved By | Notes |
|---|---|---|---|---|---|---|---|
| Ms. Rani | Science | ML | 1 Oct 2025 | 31 Mar 2026 | 182 | Principal | Maternity — second child |
| Mr. Ganesh | Maths | EL | 14 Nov 2025 | 18 Nov 2025 | 5 | VP Academic | Annual family function |
| … | … | … | … | … | … | … | … |

Searchable, filterable, exportable.

---

## 5. Leave Balance Dashboard

Grid view: staff (rows) × leave types (columns)

| Staff | CL Bal | EL Earned | EL Used | EL Bal | SL Bal | CompOff |
|---|---|---|---|---|---|---|
| Ms. Sudha | 8 | 11.25 | 6 | 5.25 | 12 | 1 |
| Mr. Rajan | 5 | 9.5 | 4 | 5.5 | 10 | 0 |

Negative balances (LWP situation) shown in red.
[Export for Payroll] → CSV for salary deduction computation.

---

## 6. Leave Application on Behalf

**[+ Apply on Behalf]** — for when staff cannot apply themselves (sick, no device):
- Select staff member
- Fill leave details (type, dates, reason)
- Submits into normal approval workflow

---

## 7. Leave Calendar View

Month calendar showing all staff leaves (colour by leave type):
- Useful for spotting "leave clustering" (too many staff absent same day)
- Flagged: if > 15% teaching staff absent on any day → alert

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/staff/leave/?status=pending` | Pending leaves |
| 2 | `POST` | `/api/v1/school/{id}/staff/leave/` | Apply leave (staff) or on behalf |
| 3 | `GET` | `/api/v1/school/{id}/staff/leave/{leave_id}/` | Leave detail |
| 4 | `POST` | `/api/v1/school/{id}/staff/leave/{leave_id}/approve/` | Approve leave |
| 5 | `POST` | `/api/v1/school/{id}/staff/leave/{leave_id}/reject/` | Reject with reason |
| 6 | `GET` | `/api/v1/school/{id}/staff/leave-balances/` | All staff balances |
| 7 | `GET` | `/api/v1/school/{id}/staff/leave-calendar/?month={month}` | Leave calendar |
| 8 | `GET` | `/api/v1/school/{id}/staff/leave/export/?month={month}` | Leave register export |

---

## 9. Business Rules

- Casual leave: maximum 3 consecutive days without medical certificate; 4+ days → must be SL with certificate
- Maternity leave: auto-calculated 180 days; system blocks any LWP marking during maternity leave period
- Leave overlap: if another staff in same department applied the same days → flagged but not blocked (VP decides)
- Leave encashment at year end: system computes EL balance × eligible days × daily rate from payroll records
- CL lapses on 31 March (end of academic year); system shows warning 30 days before

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
