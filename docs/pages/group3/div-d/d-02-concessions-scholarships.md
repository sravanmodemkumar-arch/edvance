# D-02 — Concessions & Scholarships

> **URL:** `/school/fees/concessions/`
> **File:** `d-02-concessions-scholarships.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Accountant (S3) — draft · Academic Coordinator (S4) — approve up to ₹5,000/year · Principal (S6) — full approve

---

## 1. Purpose

Manages all fee concessions and scholarships granted to students — reducing their fee liability. Indian schools offer multiple types of concessions:
- **Sibling discount:** 10% for 2nd child, 15% for 3rd child (auto-computed from C-20 family linkage)
- **Staff ward discount:** 50–100% for children of school employees
- **Merit scholarship:** Top-rank students from previous year (e.g., top 3 in each class) get partial tuition waiver
- **Need-based scholarship:** Students from low-income families (but not RTE-eligible) get partial concession
- **Management discretion:** Principal/Trust-discretionary waiver for specific cases
- **Sports quota:** Students representing district/state get fee waiver as incentive
- **PM/Government scholarships:** Central/state scholarship disbursed to student's bank — school adjusts fee receivable

---

## 2. Page Layout

### 2.1 Header
```
Concessions & Scholarships — 2026–27         [+ Grant Concession]  [Bulk Sibling Apply]  [Export]
Total Beneficiaries: 124  ·  Total Concession Value: ₹18,42,000/year
Sibling: 52  ·  Merit: 18  ·  Staff Ward: 12  ·  Need-based: 28  ·  Management: 8  ·  Sports: 6
```

### 2.2 Concession Register
| Student | Class | Type | Discount | On Which Fee Head | Approved By | Valid Till |
|---|---|---|---|---|---|---|
| Rahul Sharma | VII-B | Sibling (2nd child) | 10% tuition | Tuition only | Auto (system) | 2026–27 |
| Priya Kumar | X-A | Merit (Rank 1) | 25% tuition | Tuition only | Principal | 2026–27 |
| Arjun S. | IX-B | Staff Ward (father: teacher) | 75% all fees | All fee heads | Principal | Ongoing |
| Meena D. | VI-A | Need-based | ₹3,000/year | Tuition | Academic Coord | 2026–27 |

---

## 3. Grant Concession — Form

[+ Grant Concession] → drawer:

| Field | Value |
|---|---|
| Student | [Search] |
| Concession Type | Sibling · Staff Ward · Merit · Need-based · Sports · Management Discretion |
| Concession Amount | % of fee head  OR  Fixed amount (₹) |
| Applicable Fee Head | Tuition · All Fees · Specific heads |
| Justification | Rank 1 in Class IX (2025–26) — merit scholarship |
| Supporting Document | [Upload] — report card for merit, salary slip for need-based |
| Valid For | 2026–27 only · Until student leaves |
| Approval Required | Academic Coordinator (< ₹5,000) / Principal (≥ ₹5,000) |

---

## 4. Auto-applied Concessions

### Sibling Discount (Auto)
When siblings are linked in C-20, the sibling discount is applied automatically:
```
Sibling discount applied:
  Arjun Sharma (XI-A) — 1st child — 0% discount
  Rahul Sharma (VII-B) — 2nd child — 10% tuition discount
  Automatically adjusted in fee ledger from April 2026
```

### Staff Ward Discount (Auto on employment link)
When a staff member's ward is enrolled:
```
Staff member: Ms. Kavitha (Science Teacher, Staff ID: STF-0042)
Ward: Aditya Kavitha (VII-A, STU-0001100)
Staff ward discount: 75% on tuition (as per school policy)
Applied automatically on enrollment
```

---

## 5. Government Scholarships Adjustment

Government scholarships (PM e-Vidya, ST/SC Pre-Matric, Post-Matric) are disbursed to the student's bank account — the school doesn't receive this directly. However, schools must:
1. Track which students are receiving government scholarships
2. Ensure no double-dipping (school scholarship + government scholarship on same fee head)
3. For students receiving government scholarship: mark in fee ledger as "Government scholarship ₹X received by student — fee reduced accordingly"

| Student | Scholarship Type | Annual Amount | Disbursed To | Fee Adjustment |
|---|---|---|---|---|
| Ravi Kumar | ST Pre-Matric | ₹3,500 | Student bank a/c | Tuition reduced ₹3,500 |
| Priya Devi | SC Post-Matric | ₹7,000 | Student bank a/c | Tuition reduced ₹7,000 |

---

## 6. Impact on Fee Ledger

When a concession is approved:
```
Fee Ledger Impact — Priya Kumar (X-A) — Merit Scholarship 25%

Before scholarship:
  Tuition: ₹66,000/year  →  Installments: ₹16,500/quarter

After scholarship:
  Tuition: ₹49,500/year  →  Installments: ₹12,375/quarter
  Discount: ₹16,500/year

Note shown on receipt: "Merit Scholarship — 25% on Tuition (Rank 1, Class IX 2025–26)"
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/concessions/?year={year}` | Concession register |
| 2 | `POST` | `/api/v1/school/{id}/fees/concessions/` | Grant concession |
| 3 | `GET` | `/api/v1/school/{id}/fees/concessions/{concession_id}/` | Concession detail |
| 4 | `PATCH` | `/api/v1/school/{id}/fees/concessions/{concession_id}/approve/` | Approve concession |
| 5 | `POST` | `/api/v1/school/{id}/fees/concessions/bulk-sibling/` | Auto-apply sibling discounts for year |
| 6 | `GET` | `/api/v1/school/{id}/fees/concessions/export/?year={year}` | Export concession register |

---

## 8. Business Rules

- RTE students (C-07) are not on the concession register — they are fee-zero at source (no fee heads apply)
- Sibling discount + merit scholarship cannot be combined (school policy: maximum 1 discount type per student); the system enforces this with a warning; Principal can override
- Staff ward discount continues as long as the staff member is employed; if the staff member leaves, the discount is automatically removed from next academic year
- Any concession ≥ ₹5,000/year requires Principal approval — Academic Coordinator can approve below this threshold
- All concession approvals are immutably logged — cannot be deleted; can be revoked with reason note

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
