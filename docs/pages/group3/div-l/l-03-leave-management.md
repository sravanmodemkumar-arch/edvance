# L-03 — Leave Management

> **URL:** `/school/hr/leave/`
> **File:** `l-03-leave-management.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HR Officer (S4) — full access, configure leave policy · Vice Principal (S5) — approve/reject leaves · Principal (S6) — approve Principal-level leaves (>5 days, maternity) · Staff (S2–S6) — apply for own leave

---

## 1. Purpose

Manages all staff leave — application, approval, balance tracking, and payroll integration. Leave management in Indian schools:
- Leave types are defined by school policy (not a strict national law for private schools), but Maternity Benefit Act 1961 (amended 2017) is statutory
- Minimum leave standards are often set by state private school employee associations or CBSE norms
- Leave balance flows into payroll (L-04) for LOP deductions

---

## 2. Leave Policy Configuration

```
Leave Policy — GREENFIELDS SCHOOL — 2026–27

Leave Type       Annual Entitlement  Carry Forward   Max Carry Forward  Notes
Earned Leave (EL)    12 days          ✅ Yes          30 days            Encashable at separation
Casual Leave (CL)    12 days          ❌ No           N/A               Lapse at year end
Sick Leave (SL)      12 days          ✅ Yes (up to 6 days)  18 days    Medical cert req >3 days
Maternity Leave      26 weeks         N/A             N/A                Statutory (paid)
Paternity Leave      5 days           N/A             N/A                School policy (paid)
Compensatory Off     As earned        Lapse 60 days   N/A               Earned for working Sunday/holiday
Special Leave        Principal decides  N/A            N/A               Marriage, bereavement, etc.
Study Leave           As per policy    N/A             N/A               For professional development
Loss of Pay (LOP)    When leave balance nil  N/A        N/A              Deducted from salary
```

---

## 3. Leave Application

```
Leave Application — Ms. Geeta Sharma (TCH-031)

Leave type: ● Casual Leave  ○ Earned Leave  ○ Sick Leave  ○ Special Leave
From: [2 April 2026]  To: [2 April 2026]  (1 day)
Reason: Personal work (family matter)

Leave balance (before this application):
  CL: 9 remaining  ·  SL: 12  ·  EL: 18

Class coverage:
  Classes affected: IX-B (4 periods Social Science)
  Substitute arranged: ● I will arrange  ○ Request school to arrange (L-13)
  Substitute teacher: Mr. Kiran A. (available — confirmed) ✅

Send notification to:
  ☑ Class Teacher cover teacher (Mr. Kiran A.)
  ☑ Academic Coordinator (for timetable adjustment)

[Submit Leave Application]

Approval path: ● 1 day CL → VP can approve  ○ >5 days → Principal required

Status after submission: ⏳ Pending VP approval
```

---

## 4. Leave Approval Workflow

```
Leave Approval — VP Dashboard

Pending approvals:
  Staff           Leave Type  Dates          Days  Class Impact   Action
  Ms. Geeta S.    CL          2 Apr 2026     1     IX-B (covered) [Approve] [Reject]
  Mr. Vijay P.    EL          5–9 May 2026   5     V-A (L-13 needed) [Approve] [Reject]
  Ms. Priya I.    SL          ← already approved   —              —

Approval rules:
  CL/SL ≤ 3 days: VP approves
  CL/SL > 3 days OR EL any: VP approves; Principal is informed
  > 5 days: Principal co-approval required
  Maternity: Principal approval + HR documentation
  Same-day leave: Must be called in; application submitted same day;
                  approval is retrospective (unless emergency)

Rejection reasons (dropdown):
  ● Exam period — leave not permitted
  ● Critical exam invigilation duty
  ● Inadequate substitute cover
  ● Pattern of concern (Monday/Friday)
  ● Other: [___________]
```

---

## 5. Maternity Leave

```
Maternity Leave — Ms. Kavitha M. (TCH-044)

Expected delivery: 15 May 2026

Maternity Leave entitlement (Maternity Benefit Amendment 2017):
  ✅ 26 weeks (for first 2 children)  ·  12 weeks (for 3rd child+)
  Current case: First child — 26 weeks (182 days) ✅

Leave period:
  Pre-delivery: Up to 8 weeks before expected delivery (from 19 March 2026)
  Post-delivery: Balance of 26 weeks after delivery

Paid leave: ✅ Full pay during maternity leave (statutory — school cannot reduce)

HR actions:
  ☑ Maternity leave application received: 1 March 2026 ✅
  ☑ Principal approved: 3 March 2026 ✅
  ☑ Substitute teacher (L-08/L-13) arranged for Class VI Maths: ✅ (Mr. Arjun T. — contractual)
  ☑ Medical certificate from registered medical practitioner: ✅ Attached

ESIC (Employee State Insurance):
  If school is under ESIC coverage (gross salary ≤₹21,000):
  Maternity benefit claim under ESIC — school pays and claims reimbursement from ESIC
  Ms. Kavitha: salary ₹28,000 — NOT under ESIC — school pays full maternity leave

Return to work:
  Expected return: 14 November 2026
  School to ensure same or equivalent position on return (statutory protection)
```

---

## 6. Leave Balance Summary

```
Leave Balances — March 2026 (All Staff)

[Visible to: HR Officer, VP, Principal, Individual staff (own balance only)]

Staff                CL Remaining  SL Remaining  EL Balance  EL Carry-fwd
Ms. Meena Rao        10/12          12/12         28          18 (prev yr)
Ms. Geeta Sharma     9/12           12/12         18          6 (prev yr)
Mr. Vijay P.         4/12            8/12          12          0
Ms. Kavitha M.       0/12           0/12           22          10 (maternity period)
Mr. Ravi Kumar       11/12          10/12          15          3
...

End-of-year (March 31) lapse:
  CL: All unused CL lapses on 31 March — no encashment, no carry forward
  SL: Up to 6 days carry forward; excess lapses
  EL: Carry forward with max limit of 30 days
  EL encashment at separation: Calculated on actual EL balance at exit (L-10)
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/leave/policy/` | Leave policy configuration |
| 2 | `POST` | `/api/v1/school/{id}/hr/leave/apply/` | Apply for leave |
| 3 | `GET` | `/api/v1/school/{id}/hr/leave/pending/` | Pending approvals |
| 4 | `PATCH` | `/api/v1/school/{id}/hr/leave/{leave_id}/approve/` | Approve/reject leave |
| 5 | `GET` | `/api/v1/school/{id}/hr/leave/balance/{staff_id}/` | Staff leave balance |
| 6 | `GET` | `/api/v1/school/{id}/hr/leave/summary/?month={m}` | Monthly leave summary |
| 7 | `POST` | `/api/v1/school/{id}/hr/leave/maternity/` | Process maternity leave |

---

## 8. Business Rules

- Maternity leave is a statutory right; school cannot deny or reduce it regardless of probation status, contractual type, or school finances; a teacher on maternity leave returns to the same or equivalent position
- CL cannot be combined with other leave types to exceed the max continuous leave permitted (school policy: default 5 days without Principal approval)
- Sick leave >3 consecutive days requires a medical certificate from a registered medical practitioner; submission within 3 days of returning to work; SL without certificate may be converted to LOP at VP's discretion
- Leave during examinations: teachers are generally not permitted to take leave during examination periods (CBSE Board, unit tests, annual exams) unless it is an emergency or maternity; the approval window is flagged by the system when leave falls on exam days
- EL encashment at separation: only EL balance is encashable (not CL or SL); calculation is based on last basic salary × (EL days / 26); this flows into L-10 full and final settlement
- Leave record feeds payroll (L-04) directly; approved leave of specific types (CL, SL, EL within balance) = no deduction; LOP = salary deduction per working day rate

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
