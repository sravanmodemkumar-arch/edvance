# A-15 — RTE Compliance Tracker

> **URL:** `/school/admin/rte/`
> **File:** `a-15-rte-compliance-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full · Promoter (S7) — view · VP Admin (S5) — full · Admin Officer (S3) — view + data entry

---

## 1. Purpose

Tracks the school's compliance with the Right to Education Act 2009 (RTE Act) — specifically Section 12(1)(c) which mandates that every private unaided school must reserve 25% of seats in Class 1 (or the entry-level class) for children from Economically Weaker Sections (EWS) and Disadvantaged Groups (DG), providing them free education. Non-compliance: state government can refuse fee reimbursement, withhold recognition, or impose financial penalties.

**RTE Section 12(1)(c) compliance requirements:**
1. Maintain at least 25% EWS/DG students in the entry class
2. Provide completely free education to these students (no fees, no hidden charges)
3. Receive government reimbursement for each RTE student (per-student amount varies by state: ₹12,000–₹26,000/year)
4. Submit annual utilisation certificate to the state government
5. Conduct admissions through state government's RTE lottery portal (in most states)
6. Maintain separate records for RTE students

---

## 2. Page Layout

### 2.1 Header
```
RTE Compliance Tracker — 2025–26            [Submit Annual Report] [Export Student List] [Sync with State RTE Portal]
State: Telangana · Board: CBSE · Entry Class: LKG
```

### 2.2 Compliance Status Bar
```
✅ RTE Compliance Status: 27 students (27/90 = 30%) — Target: 25% (23 seats) — COMPLIANT
Reimbursement Claimed: ₹4.86L · Received: ₹3.24L · Pending: ₹1.62L
```

---

## 3. Main Sections

### 3.1 RTE Seat Summary

| Metric | Value |
|---|---|
| Entry class (current year) | LKG |
| Total LKG capacity | 90 seats |
| Mandated RTE seats (25%) | 23 seats |
| RTE students enrolled | 27 students |
| Over-compliance buffer | 4 extra (good for audit) |
| EWS category | 18 students |
| DG category (SC/ST/OBC) | 9 students |

---

### 3.2 RTE Student Register

Table of all RTE students currently enrolled in the school (not just entry class — all years):

| Admission No | Name | Current Class | Admission Year | Category | Income Certificate | Documents Complete | Fee Status | State Portal ID |
|---|---|---|---|---|---|---|---|---|
| SVHS-2023-RTE-001 | Mahesh K | Class III | 2023–24 | EWS | ✅ Submitted | ✅ | Free | TS-RTE-789 |
| SVHS-2024-RTE-001 | Divya S | Class II | 2024–25 | DG (SC) | ✅ Submitted | ⚠️ DOB proof pending | Free | TS-RTE-891 |
| … | … | … | … | … | … | … | … | … |

Filters: Year of admission · Category (EWS/DG) · Document status · Class

**[View/Edit]** per student: opens student profile with RTE-specific fields.

---

### 3.3 Annual Admission (Current Year)

For the current admission season's RTE slots:

| Stage | Count |
|---|---|
| Applications Received | 68 |
| Lottery Conducted (date) | 15 Jan 2026 |
| Students Selected (lottery) | 23 |
| Wait-listed | 45 |
| Offers Accepted | 21 |
| Documents Verified | 18 |
| Enrolled | 18 |
| Remaining slots | 9 (5 from acceptance dropout + 4 under-enrolled) |

**[Run Lottery]** → randomised selection from all eligible applicants (state portal synced)
**[Generate Lottery Results PDF]** → state board prescribed format for display at school notice board (mandatory under RTE rules)

---

### 3.4 Government Reimbursement Tracker

| Academic Year | RTE Students | Reimbursement Rate | Total Claimable | Claimed | Received | Pending | Notes |
|---|---|---|---|---|---|---|---|
| 2025–26 | 27 | ₹18,000/student | ₹4,86,000 | ✅ ₹4,86,000 | ₹3,24,000 | ₹1,62,000 | State treasury delay |
| 2024–25 | 22 | ₹18,000/student | ₹3,96,000 | ✅ ₹3,96,000 | ₹3,96,000 | — | Fully received |
| 2023–24 | 19 | ₹16,500/student | ₹3,13,500 | ✅ Filed | ₹2,64,000 | ₹49,500 | Partial payment |

**[Submit Reimbursement Claim]** → generates utilisation certificate + student list in prescribed format for submission to District Education Office.

---

### 3.5 Document Compliance Checklist (per RTE student)

Per student, documents required:
- Income certificate from tehsildar / revenue officer (EWS: family income < ₹1–3.5L/year depending on state)
- Caste certificate (for DG category: SC/ST)
- Age proof: Birth certificate / Hospital record
- Residence proof: Aadhaar card or ration card (address within school's notified neighbourhood)
- Aadhaar number (UDISE+ requires Aadhaar for all RTE students)

Document status per student: ✅ Submitted · ⚠️ Pending · ❌ Missing

[Bulk reminder] → sends WhatsApp message to parents with missing documents.

---

## 4. State RTE Portal Integration

| Feature | Description |
|---|---|
| Sync student list | Push enrolled RTE students to state RTE portal (state-specific API) |
| Pull lottery results | Download state-assigned student list from portal |
| Submit utilisation cert | Upload annual utilisation certificate |

**Portal links supported:** TS-RTE portal · AP RTE portal · MH RTE portal · Karnataka RTE portal · (extensible)

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/rte/summary/` | RTE compliance summary |
| 2 | `GET` | `/api/v1/school/{id}/rte/students/` | All RTE students list |
| 3 | `GET` | `/api/v1/school/{id}/rte/admissions/current-year/` | Current season RTE admissions |
| 4 | `POST` | `/api/v1/school/{id}/rte/admissions/lottery/` | Run admission lottery |
| 5 | `GET` | `/api/v1/school/{id}/rte/reimbursement/` | Reimbursement history |
| 6 | `POST` | `/api/v1/school/{id}/rte/reimbursement/claim/` | Submit claim |
| 7 | `POST` | `/api/v1/school/{id}/rte/sync-portal/` | Sync with state RTE portal |
| 8 | `GET` | `/api/v1/school/{id}/rte/documents-status/` | Document compliance per student |

---

## 6. Business Rules

- RTE students must never be charged any fee — system blocks any fee posting for students with `rte_student = True`
- Lottery must be conducted in the presence of a government observer (state rule in most states) — EduForge records the observer's name and date as part of lottery metadata
- Under-compliance (< 25% RTE students) → red alert on Principal Dashboard + Promoter Dashboard; cannot be hidden
- RTE reimbursement is tax-free income for the school; recorded separately in finance module

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
