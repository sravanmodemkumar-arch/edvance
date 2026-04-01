# M-02 — Staff Management

> **URL:** `/coaching/operations/staff/`
> **File:** `m-02-staff-management.md`
> **Priority:** P2
> **Roles:** Branch Manager (K6) · Director (K7) · HR Coordinator (K4)

---

## 1. Staff Directory

```
STAFF DIRECTORY — Toppers Coaching Centre, Hyderabad Main
As of 31 March 2026

  TEACHING STAFF (Faculty):
    ID     │ Name             │ Subject      │ Designation   │ Type       │ Join Date
    ───────┼──────────────────┼──────────────┼───────────────┼────────────┼───────────
    F-001  │ Mr. Suresh K.    │ Quant        │ Senior Faculty│ Full-time  │ Apr 2018
    F-002  │ Ms. Kavita M.    │ English      │ Senior Faculty│ Full-time  │ Jun 2019
    F-003  │ Mr. Mohan R.     │ Reasoning    │ Faculty       │ Full-time  │ Aug 2020
    F-004  │ Mr. Ravi S.      │ GK/CA        │ Faculty       │ Full-time  │ Jan 2021
    F-005  │ Ms. Preethi L.   │ English      │ Faculty       │ Full-time  │ Mar 2022
    F-006  │ Mr. Arjun T.     │ Quant        │ Faculty       │ Full-time  │ Sep 2022
    F-007  │ Ms. Rekha N.     │ Reasoning    │ Faculty       │ Part-time  │ Nov 2022
    F-008  │ Mr. Venkat R.    │ GK/CA        │ Faculty       │ Full-time  │ Feb 2023
    (6 more faculty — online + subject specialists)

  NON-TEACHING STAFF:
    ID     │ Name             │ Role               │ Dept          │ Type       │ Join Date
    ───────┼──────────────────┼────────────────────┼───────────────┼────────────┼───────────
    S-001  │ Ms. Anitha R.    │ Student Counsellor │ Student Afrs  │ Full-time  │ Jul 2020
    S-002  │ Mr. Rajan K.     │ Admissions Coord.  │ Admissions    │ Full-time  │ Mar 2021
    S-003  │ Ms. Deepa M.     │ Admissions Coord.  │ Admissions    │ Full-time  │ Aug 2021
    S-004  │ Mr. Karthik V.   │ Accounts Manager   │ Finance       │ Full-time  │ Jan 2019
    S-005  │ Ms. Lakshmi P.   │ Accounts Clerk     │ Finance       │ Full-time  │ Jun 2022
    S-006  │ Mr. Suman G.     │ IT Coordinator     │ Technology    │ Full-time  │ Oct 2021
    S-007  │ Ms. Priya V.     │ Receptionist       │ Admin         │ Full-time  │ Apr 2023
    S-008  │ Mr. Ramu N.      │ Hostel Warden (M)  │ Hostel        │ Full-time  │ May 2020
    S-009  │ Ms. Saroja T.    │ Hostel Warden (F)  │ Hostel        │ Full-time  │ Jun 2020
    S-010  │ Mr. Mohan D.     │ Maintenance        │ Operations    │ Full-time  │ Mar 2021
    (8 more: security, housekeeping, cook, assistant staff)

  OPEN POSITION:
    Admin Coordinator (S-role) — advertised Mar 15, interviews Apr 5
```

---

## 2. Staff Attendance

```
STAFF ATTENDANCE — March 2026

  FACULTY ATTENDANCE:
    Faculty           │ Working Days │ Present │ Leave │ Absent │ Attend%
    ──────────────────┼──────────────┼─────────┼───────┼────────┼────────
    Mr. Suresh K.     │     26       │   25    │   1   │   0    │  96.2%
    Ms. Kavita M.     │     26       │   26    │   0   │   0    │ 100.0%
    Mr. Mohan R.      │     26       │   24    │   2   │   0    │  92.3%
    Mr. Ravi S.       │     26       │   24    │   1   │   1    │  92.3% 🟡
    Ms. Preethi L.    │     26       │   26    │   0   │   0    │ 100.0%
    Mr. Arjun T.      │     26       │   25    │   1   │   0    │  96.2%
    [Others avg]      │     26       │   25.1  │  0.8  │   0.1  │  96.5%
    ──────────────────┴──────────────┴─────────┴───────┴────────┴────────
    Faculty average:  96.8% ✅ (target: >95%)

  NON-TEACHING STAFF ATTENDANCE:
    Average:  97.2% ✅
    Absences: 2 (medical leave — Ms. Anitha R. 1 day, Mr. Mohan D. 1 day)

  LEAVE BALANCE (selected staff):
    Mr. Suresh K.:  EL 12 remaining | CL 3 remaining
    Ms. Kavita M.:  EL 18 remaining | CL 6 remaining
    Mr. Ravi S.:    EL 8 remaining  | CL 1 remaining (1 used, 1 unauthorised)
```

---

## 3. Payroll Summary

```
PAYROLL SUMMARY — March 2026

  SALARY STRUCTURE (ranges — not individual):
    Senior Faculty (F-001, F-002):    ₹65,000–₹80,000/mo
    Faculty (full-time):              ₹40,000–₹55,000/mo
    Faculty (part-time):              ₹500–₹800/session
    Student Counsellor:               ₹32,000–₹38,000/mo
    Admissions Coordinator:           ₹28,000–₹35,000/mo
    Accounts Manager:                 ₹38,000–₹45,000/mo
    IT Coordinator:                   ₹32,000–₹40,000/mo
    Support staff:                    ₹18,000–₹25,000/mo

  MARCH 2026 PAYROLL:
    Total salary (teaching):          ₹18.2 L
    Total salary (non-teaching):      ₹ 8.4 L
    PF contribution (employer 12%):   ₹ 3.2 L
    ESI (if applicable):              ₹ 0.4 L
    TDS deducted at source:           ₹ 1.8 L
    ─────────────────────────────────────────
    GROSS PAYROLL (Mar 2026):         ₹32.0 L

  PAYROLL DATE: 1st of each month (credit by 2nd if 1st is holiday)
  TDS remittance to IT dept: by 7th of following month
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/operations/staff/` | Staff directory |
| 2 | `GET` | `/api/v1/coaching/{id}/operations/staff/{sid}/` | Staff profile and details |
| 3 | `GET` | `/api/v1/coaching/{id}/operations/staff/attendance/?month=2026-03` | Staff attendance summary |
| 4 | `GET` | `/api/v1/coaching/{id}/operations/staff/payroll/?month=2026-03` | Payroll summary |
| 5 | `POST` | `/api/v1/coaching/{id}/operations/staff/leave/` | Submit leave request |
| 6 | `PATCH` | `/api/v1/coaching/{id}/operations/staff/leave/{lid}/approve/` | Approve/reject leave |

---

## 5. Business Rules

- Staff attendance data from the biometric system feeds directly into the payroll calculation; an absent day reduces the salary proportionally (for non-salaried components) or is marked as LOP (Loss of Pay) if no leave balance is available; Mr. Ravi S.'s 1 unauthorised absence reduces his March salary by 1/26th of his monthly salary; the payroll system applies this automatically but the Branch Manager must approve the final payroll before processing; disputes about attendance ("I was present but the biometric didn't register") must be resolved before the 25th of the month via the attendance dispute form
- Part-time faculty (Ms. Rekha N. — Reasoning) are paid per session; their attendance is tracked session-by-session, not daily; a session not conducted (cancelled class, substitute arranged) is not paid; if TCC cancels a class for operational reasons (power failure, holiday), TCC still pays the part-time faculty's session fee as it is not the faculty member's fault; if the faculty cancels unilaterally without advance notice, the session fee is not paid and a breach notice is recorded in their contract file
- PF (Provident Fund) contribution of 12% employer + 12% employee applies to staff earning ≤ ₹15,000 basic salary; staff earning above ₹15,000 can voluntarily opt into PF or opt out; TCC registers as a PF-covered establishment under EPFO and files monthly ECR (Electronic Challan cum Return); non-compliance with PF is a criminal offence (Section 14 of EPFO Act 1952) with penalties and potential prosecution of the Director; the Accounts Manager monitors PF compliance monthly
- Salary ranges are not disclosed to staff below Branch Manager level; each staff member knows their own package; disclosing salary ranges to all staff (or to students) creates internal equity disputes and external embarrassment; the payroll data in the EduForge system is accessible only to the Branch Manager, Director, and Accounts Manager; a staff member who requests salary information about a colleague is told politely that individual compensation is confidential; only aggregated ranges for recruitment advertising are public
- The open Admin Coordinator position is being filled through structured interviews (panel: Branch Manager + HR); TCC does not hire family members of existing staff for positions where a reporting relationship would exist (to avoid nepotism and conflict of interest); the hiring decision is documented with interview scores and rationale; a rejected candidate who later complains of discrimination must be able to see documented, objective selection criteria; TCC follows fair employment practices regardless of government mandates as it protects the organisation from reputational and legal risk

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division M*
