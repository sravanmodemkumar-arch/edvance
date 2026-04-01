# I-04 — Scholarship Application Support

> **URL:** `/college/welfare/scholarships/`
> **File:** `i-04-scholarship-support.md`
> **Priority:** P1
> **Roles:** Welfare Officer (S4) · Scholarship Coordinator (S3) · Finance Manager (S4) · Student (S1)

---

## 1. Scholarship Ecosystem

```
SCHOLARSHIP SUPPORT — GCEH 2026–27

STUDENTS WITH ACTIVE SCHOLARSHIPS: 312 / 556 (56.1%)
  TS ePASS (fee waiver):  188 students
  NSP Central OBC:         42 students
  NSP SC/ST:               62 students
  AICTE Pragati (girls):   12 students
  Other (institutional):   8 students

SCHOLARSHIP COORDINATOR:
  Ms. Kavitha N. (Administrative Assistant — dedicated scholarship cell)
  Office hours: Mon–Sat 9 AM – 5 PM
  EduForge support: Scholarship status visible to students on welfare page

SCHOLARSHIP CALENDAR 2026–27:
  July 2026: TS ePASS portal opens for fresh applications
  August 2026: NSP portal opens
  September 2026: Verification deadline (college must verify on portal) ← critical
  October 2026: AICTE Pragati application (academic year start)
  November 2026: NSP renewal deadline for continuing students
  January 2027: Mid-year scholarship review + follow-up for government receivables
  March 2027: Annual TS ePASS receivable reconciliation
```

---

## 2. TS ePASS Support

```
TS ePASS SCHOLARSHIP SUPPORT

SCHEME:
  Telangana State ePASS (Electronic Payment & Application System for Scholarships)
  Eligibility: OBC/BC/SC/ST/EBC students; family income ≤₹2.5L
  Benefit: Full fee waiver (tuition fee) → paid to college as "government receivable"

STUDENT APPLICATION SUPPORT:
  Step 1: EduForge → Welfare → Scholarships → TS ePASS Guide
    Checklist displayed: Aadhaar, income certificate, caste certificate,
                          bank passbook (in student's name), marks list
  Step 2: Student applies on epassts.cgg.gov.in
  Step 3: College verifies on TS ePASS portal (Scholarship Coordinator)
    Verification deadline: 30 September 2026 (hard deadline — portal closes)
    GCEH verification completed: ✅ 28 September 2026 (210 students verified)

ISSUES ENCOUNTERED:
  18 students: Application incomplete (missing income certificate)
    Action: Scholarship cell called each student; documents collected + re-submitted
  4 students: Aadhaar-bank name mismatch
    Action: Guided to bank for name correction → corrected + re-submitted
  2 students: Income too high (>₹2.5L after checking actual certificate)
    Action: Ineligible; directed to NSP Central OBC (higher income limit ₹8L)

GOVERNMENT RECEIVABLE (College accounts — see C-04):
  TS ePASS amount expected: ₹1,60,00,000 (188 students × avg ₹85,000/yr)
  Received so far (FY 2026–27): ₹84,00,000 (52.5%)
  Pending: ₹76,00,000 (government delay — typical pattern; expected March–June)

IMPACT ON STUDENTS:
  Student's fee balance in EduForge: Shows ₹0 due (TS ePASS expected credit applied)
  No harassment for fee payment where TS ePASS is the reason for non-payment ← firm policy
  College absorbs the cash flow gap internally (trust support)
```

---

## 3. NSP Central Scholarship Support

```
NSP (NATIONAL SCHOLARSHIP PORTAL) — scholarships.gov.in

SCHEMES AVAILABLE:
  Central OBC Scholarship (MBC&ODF): Income <₹1L, NSP portal
  SC/ST Post-Matric: MoSJE / MoTA — income <₹2.5L
  Differently Abled (PwD): Income <₹2.5L

VERIFICATION PROCESS:
  Step 1: Student applies on NSP portal (fresh/renewal)
  Step 2: Institute verification on NSP portal (Level 1)
  Step 3: District Social Welfare Officer verification (Level 2)
  Step 4: State nodal officer approval (Level 3)
  Step 5: DBT to student's Aadhaar-linked bank account

  GCEH role: Level 1 verification only (EduForge captures NSP application ID from student
             and verifies enrolment + marks on NSP portal)

  Level 1 verification deadline: 30 days from student application
  GCEH turnaround: Average 4 days (same-week batch processing) ✅

NSP ISSUES:
  Common: Student applied with old bank account (dormant/closed)
    Action: Guide student to update bank on NSP portal; re-verify
  Common: Institute code entered wrong by student
    Action: Scholarship cell corrects at Level 1 verification step
  Complex: Student transferred from another college — NSP shows previous college
    Action: NOC from previous college + fresh application at GCEH

SCHOLARSHIP AMOUNTS (NSP 2026–27):
  Central OBC:  ₹5,000/year (limited amount — does not cover tuition)
  SC/ST Post-Matric: ₹3,500–₹7,500 depending on level and income
  Note: NSP is a student's personal income — arrives in student's bank, not college
        Unlike TS ePASS (which pays college), NSP is DBT to student
        College finance is NOT impacted by NSP (no government receivable from NSP)
```

---

## 4. AICTE Pragati Scholarship

```
AICTE PRAGATI — Girls' Technical Scholarship

ELIGIBILITY:
  Girl students in AICTE-approved degree programmes (B.Tech)
  Family income ≤₹8L/year
  Admission in the current year (fresh scholarship each year — no renewal)
  Only 1 girl per family

AMOUNT: ₹50,000/year (tuition fee reimbursement directly to college + ₹2,000 contingency to student)

GCEH PRAGATI 2026–27:
  Applied: 18 students (all first-year girl students eligible)
  Approved: 12 students (6 rejected — income documentation issues)
  Amount to be received: 12 × ₹50,000 = ₹6,00,000

DOCUMENTATION REQUIRED:
  Income certificate (state government format) ≤₹8L
  First-year admission letter (EAPCET)
  Bank account (in student's name)
  Aadhaar

VERIFICATION ON AICTE PORTAL: ✅ Completed October 2026
Amount received: ₹3,00,000 (50% first instalment) ✅ November 2026
Balance: ₹3,00,000 (expected March 2027)
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/welfare/scholarships/` | All scholarship records |
| 2 | `GET` | `/api/v1/college/{id}/welfare/scholarships/my/` | Student's own scholarship status |
| 3 | `GET` | `/api/v1/college/{id}/welfare/scholarships/pending-verification/` | Pending NSP/TS ePASS verifications |
| 4 | `GET` | `/api/v1/college/{id}/welfare/scholarships/government-receivable/` | Govt receivable status |

---

## 6. Business Rules

- The scholarship verification deadline (30 September for TS ePASS; 30 days for NSP) is the single most important annual event for the scholarship cell; a student whose verification is missed due to college delay loses the scholarship for the entire year — this is a significant financial harm; EduForge sends daily reminders to the Scholarship Coordinator from 15 September with a count of unverified applications; Principal gets notified from 25 September if any application remains unverified
- TS ePASS fee waiver must be applied to the student's account immediately on verification (as a provisional credit) — not only when the government pays; a student who has submitted TS ePASS documents should not be hounded for fee payment while government processing takes 6–12 months; the college's duty is to manage the government receivable and internally arrange cash flow — not to pass the government's delay cost to the student
- NSP scholarship arrives in the student's bank account (DBT) — the college has no financial role; however, the college's verification is the critical enabler; a college that delays Level 1 verification deprives students of their scholarship; this is particularly serious for SC/ST students who depend on NSP for basic living expenses; EduForge's verification dashboard shows every pending application daily to prevent this
- AICTE Pragati is an annual scheme with fixed eligibility windows; a girl student who misses the application window (typically October) loses that year's scholarship with no recourse; the scholarship cell must proactively identify and notify eligible students (first-year girl students, income criteria met) before the window opens, not after it closes
- Scholarship data in the student record is sensitive; caste certificate (required for SC/ST scholarships) is particularly sensitive under DPDPA 2023 — it reveals caste identity which is sensitive personal data; access to scholarship application data must be restricted to the scholarship coordinator and welfare officer; general admin staff should not have access to scholarship records that contain caste/income certificates

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division I*
