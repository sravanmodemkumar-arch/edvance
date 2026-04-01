# L-10 — Separation & Exit Management

> **URL:** `/school/hr/separation/`
> **File:** `l-10-separation.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HR Officer (S4) — manage separation process · Principal (S6) — approve separation, issue relieving letter · Accounts Officer (S3) — full and final settlement · VP (S5) — transition planning

---

## 1. Purpose

Manages staff separation — voluntary (resignation), involuntary (termination, non-renewal), retirement, and retirement on superannuation. Exit management involves:
- Notice period serving / buyout
- Handover of classes, materials, and responsibilities
- Full and final (F&F) settlement (leave encashment, pending salary, gratuity, PF withdrawal)
- Relieving letter and experience certificate issuance
- CBSE/state service book closing

---

## 2. Separation Types

```
Separation Type    Process                         Notice Required   Gratuity   Experience Cert
Resignation        Employee initiates              1 month           If ≥5 yrs  Yes
Non-renewal (contract) School does not renew       30 days notice    If ≥5 yrs  Yes
Termination (cause)    School terminates for cause Varies (PIP + HR process)  No (for cause) No (for cause)
Termination (BGV)      Adverse BGV result         Immediate          No         No
Retirement (age)       55–60 (school policy)       3 months notice   Yes        Yes
Voluntary early retire  By agreement               By agreement      Yes        Yes
Death in service        —                          —                 Yes (nominees) —
```

---

## 3. Resignation Process

```
Resignation — Ms. Priya Iyer (TCH-015)

Resignation submitted: 15 March 2026
Last working day proposed by employee: 14 April 2026 (30 days notice)
Reason: Personal — moving to another city

Principal acknowledgement: ✅ 15 March 2026
Notice period: 1 month (per appointment letter) ← serving in full ✅

Transition checklist:
  ☑ Class XI English — substitute teacher arranged (L-08/L-13) by 20 March ✅
  ☑ Handover notes: Chapters covered, pending topics, class strengths/concerns → due 10 April
  ☑ Exam papers in progress: Class XI mid-term (handover to HOD English by 5 April)
  ☑ School property returned:
    ☐ Staff ID card  ☐ Locker key  ☐ Lab keys (N/A — English teacher)
    ☐ Library books on loan (G-03 — 2 books — due return)
    ☐ School laptop (if issued): None
  ☑ EduForge deactivation: 15 April 2026 (day after last working day)

Exit interview conducted: ✅ 10 April (VP)
  Key feedback: "School is great; moving for family. Would recommend working here."
  [Log exit interview notes for HR analytics]

Full and Final Settlement (F&F):
  Last working day: 14 April 2026
  Settlement due date: 14 May 2026 (30 days after LWD — standard)

F&F Calculation:
  Pending salary (1–14 April): ₹61,600 × 14/30 = ₹28,747
  EL encashment: 22 days × (₹42,000/26) = ₹35,538
  Gratuity: Service = 7 years 9 months → (7 years eligible) × 15 days × ₹42,000/26
           = 7 × 15 × ₹1,615 = ₹1,69,615 (Gratuity Act — 7 years completed) ✅
  Less: Any advance outstanding: ₹0
  Net F&F: ₹2,33,900

  [Generate F&F computation sheet]  [Principal approve]  [Disburse]

Relieving letter: Issued 14 April 2026
  "Ms. Priya Iyer served as English Teacher (Classes XI) from 10 July 2018 to 14 April 2026.
   She has been relieved of all duties on 14 April 2026. Her conduct and work are recorded
   as satisfactory. We wish her all the best."

[Issue relieving letter]  [Close service book (L-11)]  [Archive records]
```

---

## 4. Termination for Cause

```
Termination — Mr. Vijay P. (TCH-044) — Performance basis

Background:
  2 consecutive Needs Improvement ratings (L-06)
  PIP initiated April 2026 — goals not achieved by July 2026 review
  Second written warning issued 15 July 2026

Formal process:
  ☑ PIP documented and signed by employee ✅
  ☑ Two written warnings issued (copies in service book) ✅
  ☑ Show-cause notice issued 20 July: "Why should your services not be terminated?"
  ☑ Employee's written response received: 25 July 2026
  ☑ Inquiry committee (2 teachers + VP + HR): Meeting 30 July 2026
  ☑ Inquiry finding: "Employee's response does not demonstrate improvement plan;
     goals not met; termination recommended"
  ☑ Principal decision: Termination effective 31 August 2026 (1 month notice pay in lieu)

F&F for termination:
  Notice pay in lieu: ₹32,000 (1 month gross basic)
  Pending salary (August): ₹0 (notice pay covers August)
  EL encashment: 8 days × ₹1,154 = ₹9,232
  Gratuity: 4 years 3 months — NOT eligible (gratuity requires 5 full years)
  Net F&F: ₹41,232

Termination letter issued: 1 August 2026
  [This termination is for performance cause; a certificate of service may be given
   but no "satisfactory" certification — letter states "services terminated on
   [date] due to non-performance"]

Note: Termination must follow due process (show-cause, inquiry, response);
  arbitrary termination exposes the school to labour court claims
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/school/{id}/hr/separation/resign/` | Log resignation |
| 2 | `GET` | `/api/v1/school/{id}/hr/separation/{staff_id}/` | Separation details and checklist |
| 3 | `POST` | `/api/v1/school/{id}/hr/separation/{staff_id}/ff-settlement/` | Generate F&F computation |
| 4 | `POST` | `/api/v1/school/{id}/hr/separation/{staff_id}/relieve/` | Issue relieving letter |
| 5 | `GET` | `/api/v1/school/{id}/hr/separation/upcoming/` | Staff on notice (transition planning) |

---

## 6. Business Rules

- Gratuity is a statutory payment once the employee has completed 5 continuous years; the school cannot refuse or reduce it; withholding gratuity is an offence under the Payment of Gratuity Act
- F&F settlement must be paid within 30 days of the last working day; delayed payment attracts 8–10% interest per annum (per Gratuity Act for gratuity; general law for salary)
- For termination for cause, the inquiry process must be fair and documented; a termination without show-cause and inquiry is vulnerable to labour court challenge; the entire process (PIP, warnings, show-cause, inquiry, decision) must be in the HR record
- Experience certificate: issued to all employees who leave on good terms (resignation, retirement, non-renewal without cause); not issued for termination for cause; for BGV-based termination (adverse police report), no experience certificate
- EduForge account is deactivated on the last working day + 1; data access continues for the HR Officer for service book and F&F; the employee's personal view of their own payslips is available for 90 days post-separation for their reference
- Service book is closed (L-11) with the final entry on the last working day; it is then archived; the physical service book is returned to the employee on request or kept by the school per state rules

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
