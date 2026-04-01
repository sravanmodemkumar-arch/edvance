# C-07 — RTE Admission Manager

> **URL:** `/school/admissions/rte/`
> **File:** `c-07-rte-admission-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Admission Officer (S3) — full · Administrative Officer (S3) — read · Academic Coordinator (S4) — read · Principal (S6) — full

---

## 1. Purpose

Manages the RTE (Right to Education Act 2009) Section 12(1)(c) admission process — the mandatory 25% reservation of seats in all private unaided schools (and aided schools above minimum standard) for children from EWS (Economically Weaker Sections) and DG (Disadvantaged Groups). This is a legal obligation enforced by the State Government — schools that violate it face fine, de-recognition, or affiliation cancellation.

The RTE process is completely separate from the general admission process (C-01 to C-04):
- **No entrance test is allowed** for RTE students
- **Lottery system** is mandatory when applications exceed available seats
- **State government portal** manages applications; schools must upload their seat availability
- **Reimbursement:** Government reimburses the school for RTE students at the prescribed fee rate (typically ₹800–₹2,500/month depending on state); schools must claim this quarterly/annually
- **Documents:** Income certificate, caste certificate, residence proof — all state-specific

RTE quota applies for entry-level classes only (Nursery / Class I / LKG depending on school) — students admitted under RTE continue until Class VIII without repeating the process.

---

## 2. Page Layout

### 2.1 Header
```
RTE Admission Manager — 2026–27               [Upload Seat Availability to State Portal]  [Conduct Lottery]  [Export]
RTE Seats: 40  ·  Applications Received: 86  ·  Lottery Done: ✅  ·  Selected: 40  ·  Enrolled: 36  ·  Unfilled: 4
Reimbursement Status: Q3 2025–26 — ₹2,88,000 claimed · ₹2,16,000 received · ₹72,000 pending
```

### 2.2 Quick Stats
```
RTE Students Currently Enrolled (All Years):
Class Nursery: 10  ·  LKG: 9  ·  UKG: 10  ·  Class I: 8  ·  II: 10  ·  III: 9  ·  IV: 8  ·  V: 7
Total RTE Students: 71 (all active, continuing from their year of admission)
```

---

## 3. Seat Availability Declaration

Each year, before the state government's RTE application window opens (typically November–December):

| Field | Value |
|---|---|
| Entry Class | LKG (or as per state mandate) |
| Total Seats in Entry Class | 40 |
| 25% RTE Seats | 10 (auto-computed) |
| EWS Seats | 7 |
| DG / SC Seats | 2 |
| DG / ST Seats | 1 |
| Seats Declaration Date | 15 Nov 2025 |
| Submitted to State Portal | ✅ (via APRS/Samagra/state-specific portal) |

---

## 4. RTE Application List

Applications received through state portal (import) or manual entry:

| Appln No. | Student Name | Parent Name | Category | Income Proof | DOB | Age Check | Status |
|---|---|---|---|---|---|---|---|
| RTE/AP/2026/0084 | Raju S. | Suresh S. | EWS | ✅ Verified | 12 May 2020 | ✅ 5y 10m | Selected (Lottery) |
| RTE/AP/2026/0085 | Meena D. | Dinesh D. | SC | ✅ Verified | 3 Aug 2020 | ✅ 5y 7m | Selected (Lottery) |
| RTE/AP/2026/0086 | Priya K. | Kamala K. | EWS | ⚠️ Income mismatch | 1 Jan 2019 | ❌ Overage | Rejected |
| RTE/AP/2026/0091 | Arun M. | Mohan M. | EWS | ✅ Verified | 15 Sep 2020 | ✅ 5y 6m | Waitlist (Lottery) |

**Import from State Portal:**
- [Import Applications] → upload the CSV/Excel from the state government's RTE portal (format varies by state: Andhra Pradesh uses AP RTE Portal CSV, Maharashtra uses Samagra format)
- System validates: age eligibility, category, duplicate applications

---

## 5. Eligibility Verification

### 5.1 Age Criteria (entry class)
- LKG (Class I) admission: Child must be between 3–6 years as of a prescribed date (state-specific)
- System auto-computes from DOB

### 5.2 Income Verification
EWS: Family annual income ≤ ₹1,00,000 (central definition; states may vary):
- Certificate issuing authority: Tahsildar / SDM / Ward Officer
- System can flag if income certificate is older than 1 year or from wrong authority

### 5.3 Category Verification
- SC/ST: Caste certificate from competent authority
- OBC: OBC certificate (non-creamy layer for EWS seats)
- DG: Depends on state definition — may include orphans, HIV-affected, migrant children, differently-abled

---

## 6. Lottery Process

When applications > available RTE seats, a lottery is mandatory:

### 6.1 Pre-Lottery Checklist
- [ ] All applications verified for eligibility
- [ ] Ineligible applications rejected with reason
- [ ] Notice of lottery published 7 days in advance (school notice board + website)
- [ ] Date/time/venue of lottery communicated to state authorities

### 6.2 Conduct Lottery

[Conduct Lottery] → step by step:

**Step 1: Confirm Eligible Pool**
```
Category: EWS
Available Seats: 7
Eligible Applications: 34

EWS Lottery Pool: 34 applications | 7 seats to fill
```

**Step 2: Run Lottery**
```
[Run Lottery — EWS Category]

Lottery Algorithm: System uses cryptographically secure random number generation (CSPRNG).
Lottery is transparent — conducted in presence of:
  □ Parent representatives (at least 2)
  □ Teacher representative
  □ School representative (Principal / Admission Officer)

[Generate Lottery Results]
```

**Step 3: Lottery Results**
```
EWS Lottery Results — 26 Mar 2026
Presided by: Ms. Kavitha (Principal)
Witnesses: Mr. Raju Yadav (Parent), Ms. Sunita (Parent), Mr. Ramesh (Teacher)

Selected (7 seats):
1. Raju S.     (Appln RTE/AP/2026/0084)
2. Meena D.    (Appln RTE/AP/2026/0085)
...
7. Arun M.     (Appln RTE/AP/2026/0091)

Waitlist (27 not selected):
WL-1: Kavya P.
...

[Print Lottery Result]  [Upload to State Portal]  [Notify Parents]
```

### 6.3 Lottery Report
Generated automatically for state portal submission — includes: eligible pool, seats available, lottery date, witnesses, selected students list, waitlist.

---

## 7. RTE Enrollment Tracking

After lottery/selection, RTE selected students proceed through:
```
Selected → Documents Verified → Enrolled (C-05) → Active RTE Student
```

| Appln No. | Name | Selected Category | Enrolled | Enrollment Date | Student ID |
|---|---|---|---|---|---|
| RTE/AP/2026/0084 | Raju S. | EWS | ✅ | 5 Apr 2026 | STU-0001190 |
| RTE/AP/2026/0085 | Meena D. | SC | ✅ | 5 Apr 2026 | STU-0001191 |

Unfilled seats (if selected candidate doesn't show up):
- Next on waitlist is automatically offered
- If all waitlisted candidates exhaust without filling all RTE seats, state government is informed — schools cannot use unfilled RTE seats for general admission

---

## 8. RTE Reimbursement Claim

Government reimburses school at prescribed rate per RTE student per month:

### 8.1 Current Year Reimbursement Status
| Quarter | RTE Students | Rate/Month | Amount Due | Claimed Date | Amount Received | Status |
|---|---|---|---|---|---|---|
| Q1 (Apr–Jun 2025) | 68 | ₹1,200 | ₹2,44,800 | 30 Jul 2025 | ₹2,44,800 | ✅ Received |
| Q2 (Jul–Sep 2025) | 69 | ₹1,200 | ₹2,48,400 | 31 Oct 2025 | ₹2,48,400 | ✅ Received |
| Q3 (Oct–Dec 2025) | 71 | ₹1,200 | ₹2,55,600 | 31 Jan 2026 | ₹2,16,000 | ⚠️ Partial (₹39,600 pending) |
| Q4 (Jan–Mar 2026) | 71 | ₹1,200 | ₹2,55,600 | Due: 30 Apr 2026 | — | ⏳ Not yet claimed |

### 8.2 Claim Generation
[Generate Q4 Claim] → produces:
- List of RTE students with attendance records
- Class-wise count
- Amount computation
- In state-prescribed format (PDF + Excel)
- Submitted through state DEO (District Education Officer) or online portal

---

## 9. Compliance Alerts

| Alert | Trigger | Action |
|---|---|---|
| Lottery not conducted | Applications > seats and no lottery record | Mandatory before admitting any RTE student |
| RTE seats unfilled | End of admission season with vacant RTE seats | Inform state DEO; document reason |
| Reimbursement claim overdue | Claim not filed > 15 days after quarter end | Alert to Admin Officer |
| Attendance < 75% for RTE student | Same as general students | Attendance module alert |
| Aadhaar not seeded within 30 days of enrollment | APAAR mandate | Reminder to Admin Officer |

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/admissions/rte/?year={year}` | RTE overview |
| 2 | `GET` | `/api/v1/school/{id}/admissions/rte/applications/?year={year}` | Application list |
| 3 | `POST` | `/api/v1/school/{id}/admissions/rte/applications/import/` | Import from state portal CSV |
| 4 | `PATCH` | `/api/v1/school/{id}/admissions/rte/applications/{appln_id}/verify/` | Mark eligibility |
| 5 | `POST` | `/api/v1/school/{id}/admissions/rte/lottery/` | Run lottery + generate result |
| 6 | `GET` | `/api/v1/school/{id}/admissions/rte/lottery/{lottery_id}/report/` | Lottery report PDF |
| 7 | `GET` | `/api/v1/school/{id}/admissions/rte/students/?year={year}` | Enrolled RTE students |
| 8 | `GET` | `/api/v1/school/{id}/admissions/rte/reimbursement/?year={year}` | Reimbursement status |
| 9 | `POST` | `/api/v1/school/{id}/admissions/rte/reimbursement/claim/` | Generate quarterly claim |

---

## 11. Business Rules

- Lottery algorithm uses CSPRNG (cryptographically secure) — the system logs the random seed used so the lottery can be audited and reproduced if challenged
- RTE students cannot be charged any fee — not admission fee, not tuition, not development fee; fee collection from RTE students is prohibited under RTE Act and triggers a compliance alert if attempted in div-d
- Unfilled RTE seats at year-end must be declared to state authorities; they cannot be converted to general seats
- The RTE reimbursement amount is set by the state government (not EduForge) — schools configure the current rate in school settings; EduForge then computes quarterly claims based on that rate × enrolled RTE student count × attendance-adjusted months
- CBSE affiliation compliance check (A-29) includes RTE compliance as a mandatory item — this page's data feeds that check

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
