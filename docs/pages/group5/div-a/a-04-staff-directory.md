# A-04 — Staff Directory

> **URL:** `/coaching/admin/staff/`
> **File:** `a-04-staff-directory.md`
> **Priority:** P2
> **Roles:** Director/Owner (K7) · Branch Manager (K6) · Operations Director (K6)

---

## 1. Staff Directory Overview

```
STAFF DIRECTORY — TOPPERS COACHING CENTRE
As of 30 March 2026

HEADCOUNT SUMMARY:
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  40 Faculty     22 Admin/Ops    8 Counsellors    6 Support    76 Total       │
  │  (38 active     (admissions,    (batch,          (accounts,   staff across   │
  │   2 on leave)    fee, IT)        academic)        security)    4 branches     │
  └──────────────────────────────────────────────────────────────────────────────┘

BGV STATUS:
  ✅ Verified:    68 staff (89.5%)
  ⚠️ Pending:     5 staff  (6.6%) ← POCSO risk — minor students present
  🔴 Overdue:     3 staff  (3.9%) — escalation required (>30 days pending)

FILTER / SEARCH:
  [Search by name or ID...]   [Branch: All ▼]  [Role: All ▼]  [BGV: All ▼]

  ┌────┬─────────────────────┬───────────────────────────┬──────────────┬──────────────┬─────────┐
  │ ID │ Name                │ Role                      │ Branch       │ BGV Status   │ Actions │
  ├────┼─────────────────────┼───────────────────────────┼──────────────┼──────────────┼─────────┤
  │ F1 │ Mr. Suresh Kumar    │ Faculty — Quant (Sr.)     │ Main         │ ✅ Verified  │ [View]  │
  │ F2 │ Ms. Divya Nair      │ Faculty — Quant           │ Main         │ ✅ Verified  │ [View]  │
  │ F3 │ Mr. Arun Pillai     │ Faculty — Quant           │ Main         │ ⚠️ Pending  │ [View]  │
  │ F4 │ Mr. Kiran Sharma    │ Faculty — Reasoning       │ Main         │ ✅ Verified  │ [View]  │
  │ F5 │ Ms. Meena Iyer      │ Faculty — English         │ Main         │ ✅ Verified  │ [View]  │
  │ F6 │ Mr. Ravi Naidu      │ Faculty — English         │ Dilsukhnagar │ ✅ Verified  │ [View]  │
  │ F7 │ Mr. Rajesh Varma    │ Faculty — GK/CA           │ Main         │ ✅ Verified  │ [View]  │
  │ F8 │ Mr. Praveen Rao     │ Faculty — Banking         │ Main         │ 🔴 Overdue  │ [View]  │
  │ A1 │ Ms. Priya Sharma    │ Branch Manager            │ Main         │ ✅ Verified  │ [View]  │
  │ A2 │ Mr. Deepak Sinha    │ Admissions Counsellor     │ Dilsukhnagar │ ✅ Verified  │ [View]  │
  │ ...│ ...                 │ ...                       │ ...          │ ...          │         │
  └────┴─────────────────────┴───────────────────────────┴──────────────┴──────────────┴─────────┘

  Showing 10 of 76 staff   [← Prev]  Page 1 of 8  [Next →]
```

---

## 2. Staff Profile — Detail View

```
STAFF PROFILE
──────────────────────────────────────────────────────────────────────────────
  Name:          Mr. Suresh Kumar
  Employee ID:   TCC-F001
  Role:          Senior Faculty — Quantitative Aptitude
  Branch:        Main (Himayatnagar)
  Joined:        14 June 2019 (6 years 9 months)
  Status:        Active
  Contact:       +91-98490-XXXXX  |  suresh.kumar@toppers.in

QUALIFICATIONS:
  B.Tech (ECE) — JNTU Hyderabad, 2013
  M.Sc (Mathematics) — Osmania University, 2016
  Teaching experience: 9 years (3 yrs industry + 6 yrs coaching)

BATCHES ASSIGNED (current):
  SSC CGL Morning — Quant (Mon/Wed/Fri 6–8AM)
  Banking Morning — Quant (Tue/Thu/Sat 6–8AM)
  Crash Course Apr 2026 — Quant (Mon–Sat 7–9AM)

PERFORMANCE:
  Student rating (last 6 months):  4.6 / 5.0  (based on 384 responses)
  Classes taken (Mar 2026):         26 / 26  (100% attendance)
  Questions uploaded to bank:       1,240 (Quant)

BGV:
  Status:  ✅ Verified — 12 Jan 2024
  Agency:  AuthBridge India
  Checks:  Identity ✅  Address ✅  Education ✅  Criminal ✅
  Next renewal: Jan 2026  ← Due soon

  [Edit Profile]  [Renew BGV]  [Reassign Batch]  [Deactivate]
```

---

## 3. Add New Staff

```
ADD NEW STAFF MEMBER

  Full Name:          [__________________________________]
  Mobile:             [__________________________________]
  Email:              [__________________________________]
  Role:               [Select role ▼                     ]
  Branch:             [Select branch ▼                   ]
  Date of Joining:    [DD/MM/YYYY]
  Employment Type:    ( ) Full-time  ( ) Contract  ( ) Visiting/Part-time
  Subjects (Faculty): [ ] Quant  [ ] Reasoning  [ ] English  [ ] GK
                      [ ] Banking  [ ] Computer  [ ] Hindi  [ ] Other
  Salary (₹/month):  [__________]  (visible: K7 only)
  Platform Access:    ( ) Enabled  ( ) Disabled (enable after BGV)

  BGV:
    BGV Required:     ( ) Yes — initiate immediately  ( ) No (K0 roles)
    POCSO Training:   ( ) Completed  ( ) Pending  ( ) Not required

  [Save & Send Login Invite]  [Cancel]

  ⚠️ Platform access will be disabled until BGV is marked complete
     for roles that interact with minor students (Foundation batch)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/staff/` | Staff list with filters |
| 2 | `GET` | `/api/v1/coaching/{id}/staff/{staff_id}/` | Full staff profile |
| 3 | `POST` | `/api/v1/coaching/{id}/staff/` | Add new staff member |
| 4 | `PATCH` | `/api/v1/coaching/{id}/staff/{staff_id}/` | Update staff details |
| 5 | `DELETE` | `/api/v1/coaching/{id}/staff/{staff_id}/` | Deactivate staff (soft delete) |
| 6 | `GET` | `/api/v1/coaching/{id}/staff/bgv-status/` | BGV pending/overdue report |
| 7 | `POST` | `/api/v1/coaching/{id}/staff/{staff_id}/bgv/initiate/` | Trigger BGV with agency |

---

## 5. Business Rules

- Platform access must be disabled by default for new staff until BGV is marked complete; any staff member who will interact with students under 18 (Foundation batch, minor hostel residents) without a completed BGV creates a POCSO liability for the coaching centre; the Director cannot override this restriction for roles flagged as having minor-student contact; TCC has 120 Foundation students aged 14–15 — every faculty and coordinator handling these students must be BGV-cleared
- BGV renewal is required every 2 years for all staff with platform access; the system sends automated reminders to the Operations Director at 90, 30, and 7 days before expiry; staff whose BGV expires are not automatically deactivated (to avoid operational disruption) but are flagged with an orange warning visible to the Branch Manager and Director; renewal must be completed within 30 days of expiry before the system enforces access restriction
- Salary data (visible to K7 Director only) is stored in an encrypted column and is excluded from all API responses for K6 and below; a Branch Manager who requests a staff export sees all fields except salary; this prevents salary comparison conflicts between staff at the same level and protects the coaching centre from internal pay equity disputes
- Staff profile ratings (student feedback) are aggregated at the batch level and are visible to the Academic Director and Branch Manager but not to the faculty member themselves in real-time; faculty receive their ratings only in the quarterly review session; this prevents faculty from attempting to influence students' feedback responses during active batch periods
- Deactivating a staff member is a two-step process: first, the Branch Manager marks them inactive; second, the system checks for pending obligations (classes scheduled in the next 14 days, active test papers assigned, unresolved doubt queue items); the system will not complete deactivation until all obligations are reassigned; this prevents operational disruption when a faculty member resigns suddenly mid-batch

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division A*
