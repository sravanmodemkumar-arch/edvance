# A-31 — Safety & Infrastructure Audit

> **URL:** `/school/admin/compliance/safety/`
> **File:** `a-31-safety-audit.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** VP Admin (S5) — full · Principal (S6) — approve · Promoter (S7) — view

---

## 1. Purpose

Manages the school's physical safety and infrastructure compliance — fire safety, electrical safety, CCTV, emergency drills, building safety, and general infrastructure standards required by CBSE/state board and municipal/fire department regulations. This is the operational complement to A-29 (which shows compliance status); this page is where the VP Admin actively manages the audit schedule and records evidence.

---

## 2. Page Layout

### 2.1 Header
```
Safety & Infrastructure Audit                [+ New Audit Record]  [Schedule Drill]  [Export Report]
Last Full Audit: 15 Jan 2026 · Next Planned: 15 Apr 2026
```

---

## 3. Safety Audit Checklist (current state)

### 3.1 Fire Safety

| Item | Requirement | Current Status | Last Checked | Next Due |
|---|---|---|---|---|
| Fire NOC (Municipal) | Valid certificate | ❌ EXPIRED (Jan 2025) | 15 Jan 2025 | Overdue |
| Fire Extinguishers (36 units) | All charged + in-date | ⚠️ 2 units expired | 1 Mar 2026 | Recharge needed |
| Fire Alarm System | Annual test | ✅ Tested | 1 Mar 2026 | 1 Mar 2027 |
| Sprinkler System (if installed) | Annual check | N/A | — | — |
| Emergency Exit Signage | All lit + clear | ✅ | 1 Mar 2026 | — |
| Emergency Exits (6 doors) | Not blocked | ✅ Weekly check | 25 Mar 2026 | — |
| Fire Evacuation Plan Posted | All floors | ✅ | — | — |
| Fire Drill (students + staff) | 2× per year | ✅ 15 Sep 2025 | 15 Sep 2025 | Overdue (due Mar 2026) |

### 3.2 Electrical Safety

| Item | Status |
|---|---|
| Electrical Safety Certificate (State Electricity Dept) | ❌ EXPIRED (Aug 2025) |
| MCB/ELCB functioning | ✅ |
| Wiring inspection | ⚠️ Lab block overdue |
| Generator maintenance | ✅ Feb 2026 |

### 3.3 CCTV & Surveillance

| Item | Status |
|---|---|
| Total cameras | 48 |
| Currently online | 46 (2 under repair) |
| Blind spots identified | 2 areas (pending camera addition) |
| DVR/NVR retention period | 30 days (CBSE requirement: 30 days minimum) |
| CCTV monitoring: designated person | VP Admin |

### 3.4 Building & Infrastructure

| Item | Status |
|---|---|
| Building Completion Certificate | ✅ Valid |
| Structural Safety Certificate (if > 25 years old) | N/A |
| Classroom ventilation | ✅ |
| Drinking water potability test | ✅ Jan 2026 |
| Toilet facilities (M/F separate) | ✅ 1:30 student ratio maintained |
| Ramp access (differently abled) | ⚠️ New block incomplete |
| School Canteen hygiene | ✅ Inspected Feb 2026 |

---

## 4. Drill Schedule & Records

| Drill Type | Frequency | Last Drill | Next Drill | Records |
|---|---|---|---|---|
| Fire Evacuation Drill | 2× per year | 15 Sep 2025 | Overdue (30 Mar) | [View Report] |
| Earthquake Safety Drill | Annual | 12 Aug 2025 | Aug 2026 | [View Report] |
| Mock POCSO Awareness | Annual | 15 Jan 2026 | Jan 2027 | [View Report] |
| Medical Emergency Drill | Annual | 15 Nov 2025 | Nov 2026 | [View Report] |

**[Schedule Drill]** — creates calendar event + notifies staff.
**[Record Drill Outcome]** — photos, attendance count, observer name, any deficiencies noted.

---

## 5. Infrastructure Deficiency Register

Open infrastructure issues requiring correction:

| Issue | Area | Reported By | Reported Date | Priority | Status | Action |
|---|---|---|---|---|---|---|
| Ramp in new block incomplete | New block corridor | VP Admin | 15 Feb 2026 | High | In progress | [Update] |
| 2 CCTV cameras offline | Science lab corridor | IT staff | 20 Mar 2026 | Medium | Vendor called | [Update] |
| Lab wiring overdue inspection | Chemistry lab | HOD Science | 10 Mar 2026 | High | Pending contractor | [Update] |

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/safety-audit/` | Current safety status |
| 2 | `PATCH` | `/api/v1/school/{id}/safety-audit/items/{id}/` | Update safety item |
| 3 | `POST` | `/api/v1/school/{id}/safety-audit/items/{id}/evidence/` | Upload evidence |
| 4 | `GET` | `/api/v1/school/{id}/safety-audit/drills/` | Drill schedule + history |
| 5 | `POST` | `/api/v1/school/{id}/safety-audit/drills/` | Schedule drill |
| 6 | `POST` | `/api/v1/school/{id}/safety-audit/drills/{id}/record/` | Record drill outcome |
| 7 | `GET` | `/api/v1/school/{id}/safety-audit/deficiencies/` | Open deficiency list |
| 8 | `POST` | `/api/v1/school/{id}/safety-audit/deficiencies/` | Report deficiency |
| 9 | `PATCH` | `/api/v1/school/{id}/safety-audit/deficiencies/{id}/` | Update deficiency status |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
