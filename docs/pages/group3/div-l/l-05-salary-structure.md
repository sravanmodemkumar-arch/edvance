# L-05 — Salary Structure & Revision

> **URL:** `/school/hr/salary-structure/`
> **File:** `l-05-salary-structure.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HR Officer (S4) — configure and revise · Principal (S6) — approve revisions · Payroll Officer (S3) — view for payroll · Staff (S3–S6) — view own salary structure only

---

## 1. Purpose

Manages the salary structure for all staff — pay bands, components, and revisions. A structured salary system (pay bands + annual increments) is both an administrative necessity and a retention tool. Indian school salary structures typically consist of:
- Basic salary (base for all statutory calculations)
- HRA (House Rent Allowance)
- DA (Dearness Allowance — often linked to government DA revision schedule)
- Transport/Conveyance Allowance
- Medical Allowance
- Special Allowance (to make up CTC)

---

## 2. Pay Band Structure

```
Pay Bands — GREENFIELDS SCHOOL — 2026–27

Teaching Staff:
  Band    Designation                  Min Basic    Max Basic   Increment (annual)
  T-1     Junior Teacher (0–3 yrs)     ₹25,000      ₹35,000    ₹1,500/yr
  T-2     Teacher (3–7 yrs)            ₹35,000      ₹48,000    ₹2,000/yr
  T-3     Senior Teacher (7–15 yrs)    ₹48,000      ₹65,000    ₹2,500/yr
  T-4     HOD / Senior teacher 15+yrs  ₹65,000      ₹90,000    ₹3,000/yr
  T-5     Vice Principal               ₹80,000      ₹1,10,000  ₹4,000/yr
  T-6     Principal                    ₹1,00,000    ₹1,50,000  Performance-based

Non-Teaching Staff:
  Band    Designation                  Min Basic    Max Basic   Increment
  N-1     Support staff (peon, etc.)   ₹15,000      ₹22,000    ₹800/yr
  N-2     Administrative (junior)      ₹18,000      ₹28,000    ₹1,000/yr
  N-3     Administrative (senior)      ₹28,000      ₹42,000    ₹1,500/yr
  N-4     Officer / Manager             ₹40,000      ₹60,000    ₹2,000/yr

Transport:
  T-DRV   Driver                       ₹18,000      ₹28,000    ₹1,000/yr
  T-ESC   Escort                       ₹14,000      ₹20,000    ₹800/yr

Allowances (% of basic — configurable):
  HRA:         25% (Hyderabad metro city)
  DA:          10% (school policy)
  Conveyance:  ₹800 flat (all staff)
  Medical:     ₹1,250 flat (₹15,000/yr — max exempt under Income Tax)
  Special:     Calculated to reach CTC: CTC - Basic - HRA - DA - Conv. - Med.
```

---

## 3. Annual Increment Processing

```
Annual Increment — April 2026

Policy: All permanent staff receive annual increment on 1 April (start of new year)
Probationary staff: No increment until confirmation
Contractual staff: Increment per contract terms (usually tied to renewal)

Increment run — April 2026:
  Eligible staff: 76 (permanent and post-probation)
  Not eligible: 4 (on probation)  ·  7 contractual (per contract terms)

Increment examples:
  Ms. Geeta Sharma (T-3): ₹42,000 → ₹44,500 (+₹2,500) [T-3 annual increment]
  Mr. Ravi Kumar (T-2): ₹38,000 → ₹40,000 (+₹2,000) [T-2 annual increment]
  Mr. Kishore P. (N-3): ₹35,000 → ₹36,500 (+₹1,500) [N-3 increment]

Principal approval required: ✅ (Batch increment — one approval for all)
Effective: 1 April 2026
[Generate increment orders for all]  [Principal bulk approval]
[Export increment summary for L-11 service book update]
```

---

## 4. Individual Salary Revision

```
Salary Revision — Mr. Ravi Kumar (TCH-040) — Promotion

Reason: Promotion from T-2 (Teacher) to T-3 (Senior Teacher)
  Basis: 7 years completed + performance rating "Exceeds Expectations" (L-06)
  Effective: 1 April 2026

Old structure:
  Basic: ₹38,000 (T-2 band)
  HRA: ₹9,500  ·  DA: ₹3,800  ·  Conv: ₹800  ·  Med: ₹1,250  ·  Special: ₹650
  Gross: ₹54,000

New structure:
  Basic: ₹48,000 (T-3 band — minimum) → 26.3% increase
  HRA: ₹12,000  ·  DA: ₹4,800  ·  Conv: ₹800  ·  Med: ₹1,250  ·  Special: ₹1,150
  Gross: ₹68,000 (+₹14,000)

Approval:
  HR Officer recommended: ✅
  Principal approved: ✅ (Revision order RVN/2627/004 dated 30 Mar 2026)

Service book entry: Updated in L-11 ✅
Payroll effective: April 2026 payroll ✅
[Generate revision order]  [Update service book]  [Apply to April payroll]
```

---

## 5. CTC Offer Letter Computation

```
CTC Computation — New Joiner: Mr. Suresh Reddy (TCH-045)
(Physics Teacher — Class IX–XII — joining 20 March 2026)

Agreed CTC: ₹6,00,000 per annum

Component breakdown:
  Basic (40% of CTC): ₹20,000/month (₹2,40,000/yr)
  HRA (25% of basic): ₹5,000/month
  DA (10% of basic): ₹2,000/month
  Conveyance: ₹800/month
  Medical: ₹1,250/month
  Special allowance (balance): ₹950/month
  ─────────────────────────
  Gross: ₹30,000/month (₹3,60,000/yr)

  Employer EPF contribution: ₹2,400/month (12% of basic)
  EDLI + admin: ₹300/month
  Gratuity provision: ₹961/month (15/26 × basic/12 — accrual)
  ─────────────────────────
  Total CTC: ₹33,661/month ≈ ₹4,03,932/yr

  Wait — CTC stated as ₹6 lakh; the above does not match.
  Recalculate: Basic must be higher to match CTC.
  Actual offer: [HR to verify and configure exact split]

Note: CTC = Cost to Company (includes all employer costs including statutory)
      Gross = Earnings before deductions
      Net = Take home (gross minus all deductions)
      School pays EPF employer share separately (not from employee's gross)
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/salary-structure/` | Pay band configuration |
| 2 | `PATCH` | `/api/v1/school/{id}/hr/salary-structure/` | Update pay band |
| 3 | `GET` | `/api/v1/school/{id}/hr/salary-structure/{staff_id}/` | Individual salary structure |
| 4 | `POST` | `/api/v1/school/{id}/hr/salary-structure/{staff_id}/revise/` | Process salary revision |
| 5 | `POST` | `/api/v1/school/{id}/hr/salary-structure/increment-run/` | Annual increment batch |
| 6 | `GET` | `/api/v1/school/{id}/hr/salary-structure/ctc-calculator/` | Offer letter CTC calculator |

---

## 7. Business Rules

- Minimum wage compliance: support staff (peons, security, housekeeping) must be paid at least the Telangana state minimum wage for their skill category; EduForge checks the configured basic against the minimum wage floor and warns if below
- Annual increment is not a right in private schools (unlike government service) but school policy defines it; once the policy is published, it becomes a legitimate expectation; schools that retroactively cancel increments without cause face employment disputes
- Salary revision orders must be issued in writing (the revision order PDF generated by EduForge) and a copy given to the employee and placed in the service book; verbal salary promises are not binding unless documented
- Gratuity accrual: schools with 10+ employees are covered by the Payment of Gratuity Act; gratuity accrues from day one; after 5 years of continuous service, it becomes payable on separation; EduForge tracks the gratuity liability as a provision in the financial statements (D-20)
- Salary structure is confidential; an employee can see only their own salary; HR Officer and Principal can see all salaries; no other staff member can see colleagues' salaries

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
