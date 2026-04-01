# D-13 — Scholarship Payment Tracker

> **URL:** `/school/fees/scholarships/`
> **File:** `d-13-scholarship-payments.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Accountant (S3) — full · Administrative Officer (S3) — full · Principal (S6) — full

---

## 1. Purpose

Tracks government scholarships received by students — PM e-Vidya, NSP (National Scholarship Portal) scholarships, state scholarships (SC/ST Pre-Matric, Post-Matric, OBC scholarships). These scholarships are disbursed directly to the student's bank account (not to the school). The school must:
1. Track which students have applied and received scholarships
2. Ensure school scholarship (D-02) and government scholarship don't double-cover the same fee head
3. Provide the government with school attendance and enrollment verification letters (required for scholarship renewal)

---

## 2. Page Layout

### 2.1 Header
```
Scholarship Payment Tracker — 2026–27        [+ Add Scholarship Record]  [Generate Verification Letters]  [Export]
Students with Government Scholarships: 42
Total Scholarship Amount (to students): ₹8,42,000/year
```

### 2.2 Scholarship Register
| Student | Class | Scheme | Annual Amount | Applied On | Status | Received | Fee Adjustment |
|---|---|---|---|---|---|---|---|
| Ravi Kumar | X-A | ST Pre-Matric (NSP) | ₹3,500 | Sep 2026 | ✅ Disbursed | ₹3,500 | Tuition reduced |
| Meena D. | VIII-A | SC Post-Matric | ₹7,000 | Oct 2026 | ✅ Disbursed | ₹7,000 | Tuition reduced |
| Priya S. | XI-A | PM Yashasvi (OBC) | ₹1,25,000 | Sep 2026 | ⏳ Pending | — | Pending |

---

## 3. Scholarship Schemes Tracked

| Scheme | Eligibility | Amount |
|---|---|---|
| ST Pre-Matric (NSP) | ST students Classes IX–X | ₹3,500/year |
| ST Post-Matric | ST students Classes XI–XII | ₹7,000–₹12,000/year |
| SC Pre-Matric | SC students Classes IX–X | ₹3,500/year |
| SC Post-Matric | SC students Classes XI–XII | ₹7,000/year |
| OBC Pre-Matric | OBC students income < ₹1L | ₹1,500/year |
| PM Yashasvi | OBC/EBC/DNT Classes IX–XII | ₹75,000–₹1,25,000/year |
| State Scholarships | State-specific (varies) | Varies |

---

## 4. Verification Letter Generation

Schools must issue attendance and enrollment verification letters for scholarship renewal:

[Generate Verification Letters] → per-student letters confirming:
- Student is enrolled in the school
- Current class and academic year
- Attendance percentage
- Not receiving any other major scholarship from school (to prevent double-dipping)

---

## 5. Fee Adjustment on Scholarship Receipt

When a student receives a government scholarship, the Accountant adjusts the fee ledger:
```
Meena Devi — SC Post-Matric Scholarship — ₹7,000 received (Oct 2026)

Fee Adjustment:
  Annual Tuition: ₹60,000
  SC Post-Matric scholarship: -₹7,000
  Net tuition due from parent: ₹53,000

Remaining installments adjusted proportionally.
Note on ledger: "SC Post-Matric Scholarship NSP/2026/AP/08421 — ₹7,000 credit"
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/scholarships/?year={year}` | Scholarship register |
| 2 | `POST` | `/api/v1/school/{id}/fees/scholarships/` | Add scholarship record |
| 3 | `PATCH` | `/api/v1/school/{id}/fees/scholarships/{scholarship_id}/received/` | Mark scholarship received |
| 4 | `GET` | `/api/v1/school/{id}/fees/scholarships/verification-letters/?student_ids=[]` | Generate verification letters |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
