# J-05 — Welfare Programs

> **URL:** `/coaching/student-affairs/welfare/`
> **File:** `j-05-welfare-programs.md`
> **Priority:** P2
> **Roles:** Student Counsellor (K3) · Branch Manager (K6) · Director (K7)

---

## 1. Active Welfare Programs

```
WELFARE PROGRAMS — AY 2026–27
Toppers Coaching Centre | As of 30 March 2026

  Program                   │ Beneficiaries │ Value/Benefit           │ Budget (AY) │ Status
  ──────────────────────────┼───────────────┼─────────────────────────┼─────────────┼──────────────
  Scholarship (Div G)       │     295       │ Fee waiver (₹500–18K)   │ ₹6.5 L      │ ✅ Active
  Vikram Reddy Merit Award  │       3       │ 100% fee + ₹5,000 book  │ ₹59,000     │ ✅ Active
  Emergency Financial Aid   │      12       │ ₹1,000–₹5,000 one-time  │ ₹40,000     │ ✅ Active
  Book Lending Library      │     180       │ Free NCERT/GK reference │ ₹20,000/yr  │ ✅ Active
  Mental Health Support     │      28       │ Free counselling (TCC)  │ ₹0 (in-house│ ✅ Active
  Medical First Aid         │     All       │ First aid kit, nurse    │ ₹15,000/yr  │ ✅ Active
  Women's Safety Initiative │     All F     │ Self-defence, helpline  │ ₹12,000/yr  │ ✅ Active
  ──────────────────────────┴───────────────┴─────────────────────────┴─────────────┴──────────────

  TOTAL WELFARE BUDGET (AY 2026–27):  ₹7.46 Lakh
  Budget spent (Mar 2026 YTD):        ₹6.82 Lakh  (91.4% utilised)
  Budget remaining:                   ₹  64,000   (for Apr–Jun 2026)
```

---

## 2. Emergency Financial Aid

```
EMERGENCY FINANCIAL AID — Active Cases

  Purpose: One-time support for students facing genuine financial emergencies
  Not the same as scholarship (which is fee-related); this is for immediate hardship

  ACTIVE DISBURSEMENTS (AY 2026–27):
    #  │ Student         │ Amount   │ Reason                    │ Approved by │ Date
    ───┼─────────────────┼──────────┼───────────────────────────┼─────────────┼───────────
    1  │ Pavan Reddy     │ ₹2,500  │ Father hospitalised (ICU)  │ Director    │ Feb 2026
    2  │ Kiran Naidu     │ ₹1,000  │ Travel for exam            │ BM          │ Mar 2026
    3  │ Sravya Rao      │ ₹1,500  │ Medical (appendix surgery) │ Director    │ Jan 2026
    ...  (9 more)
    TOTAL:              ₹28,400

  PROCESS:
    Student → Counsellor (verbal request) → Counsellor submits to BM
    BM approves up to ₹2,000 | Director approves ₹2,001–₹5,000
    Paid directly to student's UPI or bank (no cash)
    Not repayable — a welfare grant, not a loan

  PENDING:
    Mohammed R. — requesting ₹1,500 for medical expense (pending verification)
```

---

## 3. Book Lending Library

```
BOOK LENDING LIBRARY — As of 30 March 2026

  CATALOGUE:
    Category          │ Titles │ Copies │ Currently Lent │ Available
    ──────────────────┼────────┼────────┼────────────────┼──────────
    NCERT (6–12 Sci)  │   24   │   96   │      48        │    48
    NCERT (6–12 SST)  │   18   │   72   │      36        │    36
    GK Reference      │   12   │   48   │      28        │    20
    Aptitude (Agrawal)│    8   │   32   │      24        │     8
    English Grammar   │    6   │   24   │      18        │     6
    Reasoning (Verbal)│    6   │   24   │      12        │    12
    ──────────────────┴────────┴────────┴────────────────┴──────────
    TOTAL             │   74   │  296   │     166        │   130

  LENDING RULES:
    Max books per student:   3 at a time
    Lending period:          30 days (renewable once)
    Overdue fine:            ₹5/day after 30 days
    Lost book:               Replacement cost (typically ₹150–₹400)

  CURRENTLY OVERDUE (> 30 days):
    8 students | Books: 12 | Fines: ₹280
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-affairs/welfare/programs/` | All welfare programs |
| 2 | `POST` | `/api/v1/coaching/{id}/student-affairs/welfare/aid/` | Submit emergency aid request |
| 3 | `PATCH` | `/api/v1/coaching/{id}/student-affairs/welfare/aid/{aid}/approve/` | Approve aid (BM or Director) |
| 4 | `GET` | `/api/v1/coaching/{id}/student-affairs/welfare/library/` | Book library catalogue |
| 5 | `POST` | `/api/v1/coaching/{id}/student-affairs/welfare/library/lend/` | Lend a book |
| 6 | `GET` | `/api/v1/coaching/{id}/student-affairs/welfare/budget/?year=2026-27` | Welfare budget utilisation |

---

## 5. Business Rules

- Welfare programmes are funded from TCC's operating budget as a corporate responsibility commitment; the ₹7.46 lakh annual welfare budget (0.5% of revenue) is reviewed by the Director annually; a welfare programme that is consistently under-utilised (e.g., no students using a programme) is restructured or replaced; a programme consistently over-budget is either expanded or capped; the welfare budget is not discretionary spending — it is planned and approved at the start of each academic year
- Emergency financial aid is a welfare grant (not a loan); students are not asked to repay; attaching repayment conditions would deter students from seeking help in genuine need; TCC absorbs the cost as an investment in student retention and success; a student who receives ₹2,500 in a crisis and clears their exam is more valuable to TCC's brand (success story, referral, alumni network) than the ₹2,500 cost; the Director reviews aid disbursements quarterly to ensure the purpose is genuine emergency support, not a substitute for fee collection
- The book lending library serves students who cannot afford to buy reference books (₹400–₹600 per book); lending books reduces the financial barrier to quality preparation; books are purchased by TCC at the start of each academic year based on the previous year's demand; the book catalogue is updated annually; outdated editions are retired (NCERT revisions, new GK books); the library is managed by the receptionist with the counsellor as the custodian
- The Women's Safety Initiative includes: a self-defence workshop (2 sessions per year), a dedicated helpline number posted in Block B and all female bathrooms, a POCSO awareness session at the start of each batch, and a designated female counsellor for students who prefer not to speak to a male staff member; the initiative is budgeted at ₹12,000 per year (primarily the self-defence trainer's fee); it is non-negotiable as a welfare commitment for institutions with female students
- Welfare data (which students received aid, what amounts, and why) is sensitive personal data; it is visible only to the Counsellor, Branch Manager, and Director; other staff (faculty, coordinators, accounts clerks) do not know who received emergency aid or which students are on scholarship; this protects the student's dignity and prevents any subtle bias in how staff treat them; a student receiving ₹2,500 in emergency aid must be treated identically to a full-fee-paying student in every other respect

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division J*
