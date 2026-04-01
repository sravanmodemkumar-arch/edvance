# I-04 — Driver & Escort Management

> **URL:** `/school/transport/staff/`
> **File:** `i-04-driver-escort-management.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Transport In-Charge (S3) — manage · Administrative Officer (S3) — document tracking · Principal (S6) — approve new hires

---

## 1. Purpose

Manages transport staff — drivers and female escorts (attendants). CBSE and Supreme Court requirements for transport staff:
- **Driver requirements:** Commercial vehicle license (HMV), minimum 3 years driving experience, police background verification, medical fitness certificate (no vision defects, no medical contraindications to driving), no criminal history
- **Female escort (mandatory):** All routes carrying girls must have a female attendant; she is responsible for boarding/alighting safety and student discipline on the bus
- **Annual medical check:** Drivers must undergo annual medical fitness assessment (eyesight, blood pressure, hearing)
- **Training:** CBSE circular recommends first aid training for drivers; child safety training for escorts

---

## 2. Page Layout

### 2.1 Header
```
Driver & Escort Management                           [+ Add Driver]  [+ Add Escort]
Academic Year: [2026–27 ▼]

Drivers: 8 active  ·  Escorts: 6 active
Documents expiring (< 30 days): 2 (driver licenses)
Medical fitness: 6/8 up to date  ·  2 overdue for renewal
Background verification: 8/8 completed ✅
```

### 2.2 Staff List
```
Name          Role    Route  License No.   BGV     Medical Fit  License Exp   Status
Raju Kumar    Driver  R01    TG1234AB5678  ✅ Done  ✅ Mar 2026  15 Nov 2028   ✅ Active
Suresh M.     Driver  R02    TG2345CD6789  ✅ Done  ⚠️ Overdue   15 Jun 2027   ⚠️ Medical due
Dinesh P.     Driver  R03    AP3456EF7890  ✅ Done  ✅ Feb 2026  20 Mar 2027   ✅ Active
Ms. Kavitha   Escort  R01    —             ✅ Done  ✅ Jan 2026  N/A           ✅ Active
Ms. Priya     Escort  R02    —             ✅ Done  ✅ Dec 2025  N/A           ✅ Active
```

---

## 3. Driver Profile

```
Driver: Raju Kumar

Employee ID: DRV-001  ·  Joined: 15 Jun 2020
Assigned route: Route R01 (Chaitanyapuri)
Bus: AP29AB1234

License:
  Type: HMV (Heavy Motor Vehicle)
  Number: TG1234AB5678
  Valid until: 15 November 2028  ✅
  Endorsements: Public service vehicle (PSV) badge ✅

Background Verification:
  Police verification: ✅ Completed 1 May 2020 (Rajendranagar Police Station)
  Address verified: ✅
  Criminal record: None ✅
  Re-verification due: May 2025 → ⚠️ OVERDUE (CBSE recommends every 5 years)
  [Schedule re-verification]

Medical Fitness:
  Last medical check: 15 March 2026 ✅
  Next due: 15 March 2027
  Vision: 6/6 corrected ✅  ·  BP: 120/80 ✅  ·  Hearing: Normal ✅
  Contraindications: None

Training:
  First Aid Training: ✅ Completed 1 Feb 2024 (Red Cross)
  Child Safety Training: ✅ Completed 15 Jun 2023 (CBSE programme)

Incident history:
  2020-2026: No accidents  ✅
  3 minor traffic violations: [View]

Emergency contact: Wife — +91 9876-XXXXX
```

---

## 4. Female Escort Profile

```
Escort: Ms. Kavitha Rao

Employee ID: ESC-001  ·  Role: Female Transport Escort
Assigned route: Route R01 (Chaitanyapuri)

Responsibilities:
  ✅ Boarding/alighting supervision at each stop
  ✅ Student headcount before departure and at school
  ✅ Emergency contact for parents (she has all student parent numbers)
  ✅ Discipline management on bus
  ✅ First point of contact if student is unwell on bus

Background Verification: ✅ Completed  ·  Medical fitness: ✅ Jan 2026
POCSO awareness training: ✅ Completed (mandatory for all staff with child contact)

Emergency contact with parents: Kavitha has the parent contact list for Route R01
  If any student does not board at their stop, she calls the parent immediately.
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/transport/staff/?type={driver|escort}` | Staff list |
| 2 | `POST` | `/api/v1/school/{id}/transport/staff/` | Add driver/escort |
| 3 | `GET` | `/api/v1/school/{id}/transport/staff/{staff_id}/` | Staff profile |
| 4 | `PATCH` | `/api/v1/school/{id}/transport/staff/{staff_id}/document/` | Update document |
| 5 | `GET` | `/api/v1/school/{id}/transport/staff/compliance-alerts/` | BGV/medical/license expiry alerts |

---

## 6. Business Rules

- All transport staff must have completed police background verification before their first duty — no exceptions; a driver cannot be deployed without a verified BGV in the system
- Female escort is mandatory on any route with even 1 girl student; the system flags routes with girls and no escort as "non-compliant"
- Medical fitness certificate is annual; a driver without a current medical certificate is removed from duty roster automatically
- POCSO awareness training is mandatory for all transport staff (escorts and drivers); they interact directly with children daily
- Driver leave: If a driver is on leave, the Transport In-Charge must assign a substitute driver from the roster; substitute driver must also be BGV-verified and license-valid; ad-hoc hiring without BGV is prohibited

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
