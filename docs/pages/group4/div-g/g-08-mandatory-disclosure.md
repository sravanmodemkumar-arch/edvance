# G-08 — AICTE Mandatory Disclosure Generator

> **URL:** `/college/compliance/mandatory-disclosure/`
> **File:** `g-08-mandatory-disclosure.md`
> **Priority:** P1
> **Roles:** Compliance Officer (S4) · NAAC Coordinator (S4) · Principal/Director (S6)

---

## 1. Mandatory Disclosure Overview

```
AICTE MANDATORY DISCLOSURE — GCEH
(aicte-india.org Approval Process Handbook 2025–26 — Appendix 10)

PURPOSE:
  Public transparency: Prospective students and parents can verify claims
  Regulatory compliance: AICTE verifies during inspection
  Consumer protection: Prevents misleading admissions marketing

PUBLICATION REQUIREMENT:
  Live on college website: www.gceh.ac.in/mandatory-disclosure ✅
  Updated: At start of academic year (by 30 September)
  AICTE portal: Updated on AICTE website simultaneously ✅
  Hard copy: Available at admission office for physical inspection

SECTIONS REQUIRED (EduForge auto-generates from ERP data):
  A: General Information
  B: AICTE Approval Status
  C: Courses Offered with Intake
  D: Faculty Details
  E: Infrastructure
  F: Admission Procedure
  G: Fee Structure
  H: Placement Data (prior year)
  I: Hostel / Transport Availability
  J: Research & Publications
  K: Industry Linkages (MoUs)

LAST UPDATED: 15 July 2026 (current academic year)
NEXT UPDATE DUE: 30 September 2027
```

---

## 2. Auto-Generated Sections

```
SECTION A — GENERAL INFORMATION (Auto-generated)

Institution Name: Government College of Engineering Hyderabad (GCEH)
Type: Private unaided (self-financing), non-minority
Established: 2008
Address: Plot No. 14, JNTU Road, Kukatpally, Hyderabad — 500072
Phone: 040-2341-XXXX | Email: info@gceh.ac.in
Website: www.gceh.ac.in
NAAC Grade: B+ (CGPA 2.82, October 2022)
NBA: B.Tech CSE, ECE — Accredited (2023–2026)
AICTE EoA No.: [Current year EoA number]
JNTU Affiliation: ✅ (Affiliation No: JNTU-H/GCEH/2008)

SECTION D — FACULTY DETAILS (Auto-generated from HR module)

FACULTY DATA (as of 30 June 2026):

Department | Sanctioned | Actual | PhD | PG+UG | <5 yrs exp | Avg experience
───────────────────────────────────────────────────────────────────────────────
CSE        | 14         | 14     | 8   | 6     | 2          | 8.4 yrs
ECE        | 12         | 12     | 6   | 6     | 1          | 9.1 yrs
EEE        | 8          | 8      | 4   | 4     | 2          | 7.8 yrs
Mech       | 8          | 8      | 3   | 5     | 3          | 7.2 yrs
Civil      | 6          | 6      | 2   | 4     | 1          | 10.2 yrs
Maths      | 4          | 4      | 2   | 2     | 0          | 12.1 yrs
───────────────────────────────────────────────────────────────────────────────
Total      | 62         | 62     | 25  | 37    | 9          | 8.9 yrs

Note: AICTE requires sanctioned = actual; any vacancies must be disclosed
EduForge: Auto-checks faculty count against AICTE approval; flags deficit

SECTION G — FEE STRUCTURE (Auto-generated from Fee module)

2026–27 FEE STRUCTURE (AFRC Approved):
  Category              | Convener (70%)  | Management (30%)
  B.Tech (CSE/ECE/EEE): ₹85,000/yr      | ₹1,40,000/yr
  B.Tech Mech:          ₹85,000/yr      | ₹1,40,000/yr
  M.Tech CSE:           ₹75,000/yr      | ₹1,20,000/yr
  MBA:                  ₹90,000/yr      | ₹1,50,000/yr
  MCA:                  ₹70,000/yr      | ₹1,10,000/yr

Additional fees: Exam (₹120/subject JNTU), Library (₹500/yr), ID card (₹200)
Caution deposit: ₹5,000 (refundable)
Development fee: NOT collected (Telangana Capitation Fee Act prohibition)

SECTION H — PLACEMENT (Auto-generated from Placement module — E-04)
  Prior year (2024–25 batch): 72.8% placed
  Median CTC: ₹4.2L | Max CTC: ₹42.0L
  Companies visited: 26
```

---

## 3. Disclosure Consistency Check

```
MANDATORY DISCLOSURE CONSISTENCY AUDIT
(EduForge automated cross-check before publication)

CONSISTENCY CHECKS:
  ✅ Fee structure in disclosure matches AFRC approval order
  ✅ Faculty count in disclosure matches HR module active faculty
  ✅ Placement data in disclosure matches Placement module output
  ✅ NAAC grade matches current accreditation status
  ✅ NBA status matches accreditation records
  ⚠️ Faculty PhD count: Disclosure shows 25 PhD; HR module shows 24 PhD
     (Dr. Ramesh D. PhD awarded — HR module updated; disclosure not yet synced)
     Action: Re-sync disclosure Section D before publishing
  ✅ Hostel capacity matches Hostel module inventory

DISCREPANCY RESOLUTION:
  All discrepancies flagged → Compliance Officer reviews → Manual approval required
  After resolution: Compliance Officer marks disclosure "Verified" + Principal approves
  EduForge logs: Who updated each section, when, and version history

VERSION CONTROL:
  Each mandatory disclosure version is stored (for AICTE inspection — any year)
  Current version: v2026-07 (July 2026 update)
  Previous version: v2025-09 (September 2025 update) — archived ✅
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/compliance/disclosure/generate/` | Generate disclosure from ERP data |
| 2 | `GET` | `/api/v1/college/{id}/compliance/disclosure/consistency/` | Run consistency check |
| 3 | `POST` | `/api/v1/college/{id}/compliance/disclosure/approve/` | Principal approves disclosure |
| 4 | `GET` | `/api/v1/college/{id}/compliance/disclosure/history/` | Version history |
| 5 | `GET` | `/api/v1/college/{id}/compliance/disclosure/public/` | Public disclosure (PDF/web) |

---

## 5. Business Rules

- The mandatory disclosure is a public document; anything stated in it is legally binding; a student who is admitted based on information in the mandatory disclosure (e.g., placement % of 90% when actual is 60%) has a consumer complaint under Consumer Protection Act 2019 against the institution; the Chief Compliance Officer and Principal who sign the disclosure bear personal responsibility for its accuracy
- Automatic generation from ERP data (rather than manual entry) is the most reliable way to keep mandatory disclosure accurate; EduForge's disclosure generator pulls live data from HR, fee, placement, and hostel modules with a consistency check; manual entry introduces copy-paste errors and inconsistencies between what the ERP records and what the disclosure states
- AICTE's online portal also shows the mandatory disclosure data submitted by the college; if the portal data differs from the college website data, it creates an inconsistency that inspectors can detect immediately; EduForge's direct AICTE portal sync (where API access exists) ensures the portal is updated simultaneously with the website
- The mandatory disclosure must include accurate hostel and transport information; prospective students from outside Hyderabad make hostel decisions based on this disclosure; if the disclosure says "hostel available for 400 students" but only 280 seats exist, this is a false representation that can be complained about to AICTE and consumer courts
- Archives of past mandatory disclosures must be maintained; AICTE inspectors sometimes compare current vs prior year disclosures to detect sudden "improvements" in data that are statistically implausible; having consistent, gradual improvement trajectories in the disclosure data across years demonstrates genuine institutional progress

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division G*
