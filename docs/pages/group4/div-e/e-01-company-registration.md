# E-01 — Company & Recruiter Registration

> **URL:** `/college/placement/companies/`
> **File:** `e-01-company-registration.md`
> **Priority:** P1
> **Roles:** Placement Officer (S3) · Training & Placement Coordinator (S4) · Principal/Director (S6)

---

## 1. Company Database

```
COMPANY DATABASE — GCEH Placement Cell 2026–27

REGISTERED COMPANIES: 47
ACTIVE (visited/scheduled this season): 28
NEW THIS SEASON: 9

COMPANY SEGMENTS:
  IT/Software:         22 companies (46.8%)
  Core Engineering:     8 companies (17.0%)  ← Civil, Mech, EEE, ECE hardware
  BFSI/Analytics:       7 companies (14.9%)
  Product/Startup:      5 companies (10.6%)
  PSU/Government:       3 companies (6.4%)   ← BHEL, ONGC, DRDO
  Consulting/Others:    2 companies (4.3%)

TIER CLASSIFICATION:
  Tier 1 (CTC ≥₹8L):   12 companies (TCS, Infosys, HCL, Wipro, Accenture, Deloitte,
                          Amazon, Microsoft, Goldman Sachs, ISRO [govt], BHEL, ONGC)
  Tier 2 (CTC ₹4–8L):  22 companies (mid-size IT, product, BFSI)
  Tier 3 (CTC <₹4L):   13 companies (local IT, startups, smaller firms)

COMPANY RECORD — Infosys Ltd.
  Segment: IT/Software (Tier 1)
  SPOC (Single Point of Contact): Ms. Rekha Sharma (Campus Relations Manager)
  Email: campus.relations@infosys.com | Phone: XXXXXXXXXX
  Recruitment type: Service (BFSI + IT support roles)
  Roles offered: Systems Engineer, Digital Specialist Engineer
  CTC: ₹3.6L/yr (Systems Engineer), ₹4.5L/yr (Digital Specialist)
  Eligibility: 60% aggregate (all semesters), no active backlogs
  Test: Infosys InfyTQ platform (pre-placed or online hub test)
  Bond: 1 year (no bond for Digital Specialist)
  Last visit: October 2025 (placed 14 students)
  Scheduled 2026–27: ✅ (October 2026 — confirmed)
```

---

## 2. Company Registration Form

```
COMPANY REGISTRATION — New Company Onboarding

COMPANY DETAILS:
  Company Name: Persistent Systems Ltd.
  Type: Listed company (BSE: 533218)
  Sector: IT/Product
  Headquarters: Pune, Maharashtra
  Website: www.persistent.com

HR/CAMPUS CONTACT:
  Name: Mr. Aditya Bhosale
  Designation: Senior HR Business Partner — Campus
  Email: campus@persistent.com
  Phone: 9XXXXXXXXX

RECRUITMENT DETAILS:
  Roles: Associate Software Engineer
  CTC offered: ₹5.5L/yr
  Bond: None
  Min CGPA: 6.5 (no active backlogs)
  Branches eligible: CSE, IT, ECE, EEE (GCEH has: CSE 180, ECE 120, EEE 60, Mech 60)
  Test mode: Online (AMCAT-based Persistent assessment)
  Process: Online test → Technical interview → HR interview
  Hiring timeline: November – February (academic year)
  Expected headcount: 8–12 students

DOCUMENTS UPLOADED:
  ✅ Company profile brochure
  ✅ Role description
  ✅ CTC breakup (fixed + variable + ESOPs if any)
  ✅ Bond/agreement terms

STATUS: Verified by Placement Officer ✅ | Principal approved ✅
Tier classification: Tier 2

[Schedule Campus Drive]  [Share with Students]  [Download JD]
```

---

## 3. Company Approval Workflow

```
COMPANY APPROVAL WORKFLOW

Step 1: Company submits registration (EduForge recruiter portal)
Step 2: Placement Officer reviews:
          ✅ Company legitimacy (CIN/GST verification)
          ✅ Offer letter template review (no misleading terms)
          ✅ Process details clear
          ✅ No placement fee to students (prohibited by UGC and AICTE)
          ⚠️ Bond >2 years flagged for Principal review
Step 3: Placement Officer recommends → Principal approves (or rejects with reason)
Step 4: Company notified → SPOC contact saved → Drive scheduling begins

REJECTED COMPANIES (2026–27 examples):
  Company X: Rejected — no CIN found; possible fly-by-night
  Company Y: Rejected — bond 3 years + salary holdback clause (predatory)
  Company Z: Rejected — requires students to pay training fee after joining (illegal)

BLACKLISTED COMPANIES (permanent):
  Maintained by Placement Coordinator; backed up by historical incident record
  EduForge prevents scheduling drives for blacklisted companies
  Shared (optional) via NAAC placement cell peer network
```

---

## 4. Student-Company Matching

```
ELIGIBLE STUDENTS DATABASE — for recruiters

GCEH 2026–27 FINAL YEAR: 332 students
  CSE: 135  |  ECE: 96  |  EEE: 54  |  Mech: 47

STUDENT ELIGIBILITY FILTERS (per company criteria):
  For Infosys (60%, no active backlog):
    Eligible: 287 / 332 students
    Ineligible: 45 (CGPA below threshold or active backlogs)

STUDENT PROFILE EXPORT TO COMPANY:
  Consent required: ✅ (DPDPA 2023 — student must consent to sharing resume with recruiter)
  Consent mechanism: EduForge → Placement → Drives → Infosys Campus Drive →
                     "Share your profile? [YES/NO]" (student chooses)
  Data shared: Name, roll number, CGPA, branch, contact — only what company needs
  Data NOT shared: Aadhaar, bank details, religion, caste (unless PSU requires)
  DPDPA log: Each export timestamped with student consent record

RESUME BUILDER (EduForge feature):
  Students can build standard resume from profile data
  Export: PDF; download to apply or share via placement cell
  ATS-friendly format (verified against Infosys / TCS / Accenture parsers)
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/placement/companies/` | All registered companies |
| 2 | `POST` | `/api/v1/college/{id}/placement/companies/register/` | New company registration |
| 3 | `POST` | `/api/v1/college/{id}/placement/companies/{id}/approve/` | Approve/reject company |
| 4 | `GET` | `/api/v1/college/{id}/placement/students/eligible/` | Eligible students (filter by CGPA/branch) |
| 5 | `POST` | `/api/v1/college/{id}/placement/students/export/` | Export student profiles (consent-gated) |

---

## 6. Business Rules

- Placement fee from students is strictly prohibited; neither the college placement cell nor any company can charge students for campus placement activities; if a company offers "jobs" in exchange for a training fee or deposit, this is a scam and the company must be rejected and blacklisted; multiple AICTE and UGC circulars prohibit this; students who report such demands should be protected from retaliation
- CTC transparency: The full CTC breakup must be disclosed to students before they apply — including variable pay, joining bonus (often one-time), ESOPs (illiquid), and bond clauses; presenting a headline CTC figure without disclosing that 40% of it is variable or ESOPs is misleading; EduForge requires companies to upload the CTC breakup document before drive scheduling
- Student data export to companies requires documented consent under DPDPA 2023; a blanket consent signed at admission does not cover sharing data with specific companies years later; purpose-specific, company-specific consent at the time of drive registration is required; this also aligns with global GDPR best practices (likely relevant if company is a multinational)
- Bond agreements of >2 years or those with punitive financial penalties for early exit should be flagged; while bonds are legal, courts have struck down bonds that are unconscionable (extremely large penalty for short employment); the placement cell should advise students of bond terms and flag aggressive clauses
- PSU/government sector placement (BHEL, ONGC, DRDO) requires reservation documentation (SC/ST/OBC/PwD certificates); the placement cell must maintain these separately and assist reserved-category students in PSU application processes where reservation benefits apply

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division E*
