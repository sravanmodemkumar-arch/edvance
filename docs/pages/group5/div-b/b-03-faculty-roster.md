# B-03 — Faculty Roster & Load Management

> **URL:** `/coaching/academic/faculty-roster/`
> **File:** `b-03-faculty-roster.md`
> **Priority:** P1
> **Roles:** Academic Director (K6) · Academic Coordinator (K5) · Course Head (K5)

---

## 1. Faculty Load Overview

```
FACULTY ROSTER — TOPPERS COACHING CENTRE
As of 30 March 2026

LOAD SUMMARY:
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  40 Faculty     28.4 hrs/wk    4 Overloaded    2 Under-utilised   6 Batches │
  │  Active         Avg load       (>36 hrs/wk)    (<18 hrs/wk)       avg/faculty│
  └──────────────────────────────────────────────────────────────────────────────┘

FACULTY LOAD TABLE:
  Name               │ Subject     │ Batches │ Hrs/Wk │ Rating │ Status
  ───────────────────┼─────────────┼─────────┼────────┼────────┼──────────────
  Mr. Suresh Kumar   │ Quant       │    4    │  38    │ 4.6    │ ⚠️ Overloaded
  Ms. Divya Nair     │ Quant       │    3    │  28    │ 4.4    │ ✅ Normal
  Mr. Arun Pillai    │ Quant       │    2    │  20    │ 4.1    │ ✅ Normal
  Mr. Kiran Sharma   │ Reasoning   │    4    │  36    │ 4.5    │ ⚠️ High
  Ms. Ananya Roy     │ Reasoning   │    3    │  26    │ 4.2    │ ✅ Normal
  Ms. Meena Iyer     │ English     │    4    │  38    │ 4.7    │ ⚠️ Overloaded
  Mr. Ravi Naidu     │ English     │    2    │  18    │ 3.8    │ ✅ Normal
  Mr. Rajesh Varma   │ GK/CA       │    6    │  42    │ 4.3    │ 🔴 Overloaded
  Ms. Sunita Bhat    │ GK/CA       │    2    │  16    │ 4.0    │ 🔴 Under-util.
  Mr. Praveen Rao    │ Banking     │    4    │  34    │ 4.2    │ ✅ Normal
  Ms. Latha Reddy    │ Banking     │    2    │  20    │ 3.6    │ ✅ Normal
  Mr. Deepak Sinha   │ Computer    │    3    │  22    │ 4.3    │ ✅ Normal
  ...28 more faculty │             │         │        │        │
```

---

## 2. Faculty Assignment Matrix

```
FACULTY–BATCH ASSIGNMENT MATRIX

                     │ SSC CGL│ SSC CGL│ SSC    │ RRB    │ Banking│ Found. │ Dropper
                     │ Morn   │ Eve    │ CHSL   │ NTPC   │ Morn   │ 9-10   │ JEE
  ───────────────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────
  Mr. Suresh (Quant) │ ✅ Pri │        │ ✅ Pri │        │ ✅ Pri │        │
  Ms. Divya (Quant)  │        │ ✅ Pri │        │ ✅ Pri │        │ ✅ Pri │
  Mr. Arun (Quant)   │        │        │        │        │        │        │ ✅ Pri
  Mr. Kiran (Reason) │ ✅ Pri │ ✅ Pri │        │ ✅ Pri │        │        │
  Ms. Ananya (Reason)│        │        │ ✅ Pri │        │ ✅ Pri │ ✅ Pri │
  Ms. Meena (English)│ ✅ Pri │        │ ✅ Pri │        │ ✅ Pri │ ✅ Pri │
  Mr. Ravi (English) │        │ ✅ Pri │        │ ✅ Pri │        │        │
  Mr. Rajesh (GK/CA) │ ✅ Pri │ ✅ Pri │ ✅ Pri │ ✅ Pri │ ✅ Pri │        │
  Ms. Sunita (GK/CA) │        │        │        │        │        │ ✅ Pri │ ✅ Pri
  Mr. Praveen (Bank) │        │        │        │        │ ✅ Pri │        │
  Ms. Latha (Bank)   │        │        │        │        │        │        │

  Pri = Primary faculty | Bkp = Backup (for substitution)
  ⚠️ Mr. Rajesh (GK) assigned to 6 batches — redistribute to Ms. Sunita (2 batches only)
```

---

## 3. Rebalance Faculty Load

```
LOAD REBALANCING TOOL

  Issue identified: Mr. Rajesh Varma (GK/CA) — 42 hrs/week (overloaded)
                    Ms. Sunita Bhat (GK/CA) — 16 hrs/week (under-utilised)

  PROPOSED REBALANCING:
    Transfer: RRB NTPC Weekend GK sessions → Ms. Sunita Bhat
    Transfer: Banking Evening GK sessions → Ms. Sunita Bhat
    Effect:   Mr. Rajesh: 42 → 30 hrs/wk ✅
              Ms. Sunita: 16 → 28 hrs/wk ✅

  IMPACT CHECK:
    Students affected:  320 + 200 = 520 students
    Student notification: WhatsApp alert drafted ✅
    Effective date: 7 April 2026 (after this week's classes)
    Approval required: Academic Director ✅

  [Approve Rebalancing]  [Modify]  [Cancel]

  ⚠️ Ms. Sunita's student rating: 4.0/5.0 vs Mr. Rajesh's 4.3/5.0
     Recommendation: Notify students; offer makeup session with Mr. Rajesh if needed
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/academic/faculty-roster/` | All faculty with load & ratings |
| 2 | `GET` | `/api/v1/coaching/{id}/academic/faculty/{fid}/schedule/` | Faculty weekly schedule |
| 3 | `GET` | `/api/v1/coaching/{id}/academic/faculty-batch-matrix/` | Assignment matrix |
| 4 | `POST` | `/api/v1/coaching/{id}/academic/faculty/reassign/` | Reassign faculty to batch |
| 5 | `GET` | `/api/v1/coaching/{id}/academic/faculty/overload-report/` | Overloaded/under-utilised faculty |

---

## 5. Business Rules

- Faculty load above 36 hours/week is the overload threshold; sustained overload (>4 weeks) leads to declining teaching quality, more absences, and higher attrition; Mr. Suresh Kumar and Ms. Meena Iyer are both at 38 hours — the Academic Coordinator must create rebalancing plans before the next batch cycle; star faculty who are perpetually overloaded eventually leave for competitors who offer lower teaching loads with equivalent pay
- Faculty assignments must maintain subject consistency within a batch; changing the primary Quant faculty mid-batch disrupts students' learning continuity and is a common complaint in student surveys; unavoidable changes (faculty resignation, illness) must be accompanied by a handover session where both faculty jointly address the batch; the Academic Director approves all mid-batch faculty changes
- The faculty-batch assignment matrix must be reviewed every 3 months at minimum; batch sizes change (new enrollments, dropouts), exam dates shift, and faculty availability changes; a static assignment from June that is never reviewed becomes misaligned with October realities; EduForge triggers a review prompt to the Academic Coordinator on the 1st of every 3rd month
- Backup faculty assignment is mandatory for every batch; if the primary faculty is absent, the backup must be able to cover the session without cancellation; backup faculty should ideally be from the same subject with equivalent or higher student ratings; a batch with no backup assignment is an operational risk; the assignment matrix highlights batches with no backup in orange
- Faculty load calculation includes all teaching hours plus doubt session hours but excludes question bank creation time and administrative work; the actual faculty burden is therefore higher than the load figure suggests; coaching centres that count only classroom hours underestimate faculty stress; TCC's policy is to count doubt sessions at 0.5x teaching hour weight, giving a truer picture of cognitive load

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division B*
