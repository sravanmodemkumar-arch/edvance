# H-05 — Leave Management

> **URL:** `/college/hr/leave/`
> **File:** `h-05-leave-management.md`
> **Priority:** P2
> **Roles:** Faculty/Staff (S3) · HOD (S4) · HR Officer (S3) · Principal/Director (S6)

---

## 1. Leave Policy

```
LEAVE POLICY — GCEH
(AICTE/UGC recommendations + Telangana Shops & Establishments Act)

LEAVE TYPES:

  CL (Casual Leave):
    Entitlement: 12 days/year (pro-rated for new joins)
    Carry-forward: NOT allowed (lapses on 31 December)
    Max at a time: 3 days (beyond 3 days — use EL or proceed as LOP)
    Purpose: Personal/incidental matters (doctor visit, family function, etc.)
    Notice: 24-hour advance; for emergencies — same day (with retrospective application)

  EL (Earned Leave):
    Entitlement: 15 days per 6 months (30 days/year)
    Earn: Based on actual days worked (not days absent)
    Carry-forward: Allowed (max 300 days accumulated)
    Encashment: On retirement/resignation (EL encashment up to 300 days)
    Formula: ₹(Basic + DA) / 26 × days encashed
    Notice: 7 days advance for planned EL

  Duty Leave (DL):
    For: Official duties outside college (NAAC visit, AICTE inspection, court duty)
    Approval: Principal
    Not counted against EL/CL

  Academic Leave (AL):
    For: FDP, conferences, research visits, university examiner duty
    Approval: Principal (>3 days: Governing Body ratification)
    Limit: 30 days/year
    Salary: Full (treated as duty)

  Maternity Leave (ML):
    26 weeks (full salary) — see G-06 for details
    Paternity Leave: 15 days (GCEH policy — not legally mandated for private)

  Medical Leave:
    For: Hospitalisation or major illness (not covered by CL)
    Approval: Medical certificate mandatory
    Limit: As needed (with certificate); after 3 months — half pay

  LOP (Loss of Pay):
    When all other leave exhausted
    Salary deduction: ₹(Basic + DA) / 26 × LOP days
    EPF: Full contribution still due on actual pay drawn
```

---

## 2. Leave Application

```
LEAVE APPLICATION — Dr. Suresh K.
Type: Academic Leave (FDP)
From: 14 January 2027 (Monday)
To:   18 January 2027 (Friday)
Days: 5 days
Reason: AICTE ATAL FDP on Cybersecurity (NITK Surathkal — official programme)

Supporting doc: ✅ ATAL FDP invitation letter (uploaded)
HOD approval: ✅ Dr. Priya M. approved 10 January 2027
Principal approval: ✅ Dr. R. Venkataraman approved 11 January 2027

CLASS ADJUSTMENT:
  CS201 classes (5 periods): Substitution assigned by HOD
    Monday/Tuesday: Mr. Arun M. (substituted 2 periods/day)
    Wed–Fri: 3 periods — Ms. Deepa R.
  Recorded in substitution register ✅

LEAVE BALANCE AFTER THIS LEAVE:
  Academic Leave 2026–27: Used 5 days; balance 25 days (of 30 max)
  EL: Unaffected (not academic leave type)

LEAVE CALENDAR — Department View (HOD view only):
  Helps HOD plan: Simultaneous absence of multiple faculty from same dept flagged
  Warning: If >30% of a department is on leave same day → system alert to Principal
  Current: CSE — Dr. Suresh (5 days) + Mr. Anil (3 days CL) overlap 16–18 Jan
           Faculty strength: 14 → 12 available (86% coverage) → within threshold ✅
```

---

## 3. Leave Register

```
LEAVE REGISTER — 2026–27 (Sample — CSE Department)

Faculty          | CL Used | CL Bal | EL Balance | AL Used | LOP
──────────────────────────────────────────────────────────────────────────────
Dr. Suresh K.    | 8       | 4      | 42 days    | 12 days | 0
Dr. Priya M.     | 6       | 6      | 38 days    | 8 days  | 0
Dr. Ramesh D.    | 10      | 2      | 28 days    | 4 days  | 0
Mr. Arun M.      | 5       | 7      | 22 days    | 2 days  | 0
Ms. Deepa R.     | 12      | 0      | 18 days    | 6 days  | 2 days ←

Ms. Deepa R. — LOP 2 days:
  Both CLs exhausted; took 2 days leave without EL application
  HOD flagged: Advised to plan leaves better
  Salary deduction: ₹(₹72,000 + ₹28,800) / 26 × 2 = ₹7,753
  Next salary: Deducted ✅

EL ENCASHMENT (On exit — for planning):
  If Dr. Suresh resigns today: 42 EL days
  Encashment = ₹(₹1,12,400 + ₹44,960) / 26 × 42 = ₹2,53,772
  Provision in gratuity + leave encashment liability: Finance tracks ✅
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hr/leave/balance/{employee_id}/` | Leave balance |
| 2 | `POST` | `/api/v1/college/{id}/hr/leave/apply/` | Apply for leave |
| 3 | `POST` | `/api/v1/college/{id}/hr/leave/{id}/approve/` | Approve/reject leave |
| 4 | `GET` | `/api/v1/college/{id}/hr/leave/calendar/?month=2027-01` | Department leave calendar |
| 5 | `GET` | `/api/v1/college/{id}/hr/leave/register/` | Full leave register |

---

## 5. Business Rules

- CL (Casual Leave) is for unforeseen personal needs; it should not be used as additional EL by planning family vacations as "casual" leave; HODs who rubber-stamp CL applications for planned 5–7 day breaks are undermining the leave policy; EduForge flags CL applications >3 days for Principal review (beyond the policy maximum per spell)
- Academic leave for FDP and conferences is a professional development entitlement — denying it without reason affects faculty morale and ultimately harms the institution (faculty stop attending conferences, publications drop, NAAC scores suffer); HODs must plan department coverage in advance and should not routinely deny academic leave
- LOP calculation must be done on actual days (not "months"); a faculty member taking 2 days LOP in a 31-day month should have 2/31 of monthly salary deducted (some employers incorrectly use 30 as denominator always); Telangana Shops & Establishments Act uses the concept of "wages per day" = monthly wages / working days in the month; EduForge uses the correct denominator
- Leave encashment liability (accumulated EL) is a contingent liability that grows over time; a faculty member with 280 EL days accumulated represents approximately 10 months of salary in contingent liability; the Finance team must provision for this annually in the balance sheet; unexpected mass resignations without provision can create a liquidity crisis
- Simultaneous absence alerts protect academic continuity; if 40% of CSE faculty are on leave simultaneously (FDP season — October/November) and no substitution is arranged, students miss significant teaching time; this affects both learning outcomes (NAAC Criterion 2) and parent/student satisfaction; the threshold alert (>30% absent same day) is a practical minimum control

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division H*
