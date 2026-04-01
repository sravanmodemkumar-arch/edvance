# A-01 — Admission Applications

> **URL:** `/college/students/applications/`
> **File:** `a-01-applications.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Admissions Officer (S3) — manage applications · Registrar (S4) — oversee process · Principal/Director (S6) — approve management quota · Applicant (public access for submission)

---

## 1. Purpose

Manages the inbound flow of admission applications — from the prospective student's initial application through to document verification and offer of admission. College-specific complexities:
- Multiple intake types: merit quota (open/category), management quota, NRI quota, lateral entry (for engineering diploma holders)
- Entrance exam score linkage: NEET (medical), JEE Main/Advanced (engineering), CAT/MAT/CMAT (management), CUET (central university UG), state-level CET
- Reservation matrix: SC/ST/OBC-NCL/EWS/PwD as per central/state policy
- Documents: Category certificates (caste, EWS income), entrance score cards, qualifying mark sheets, gap certificate (if any)
- Multiple programmes per application (student may apply for B.Tech CSE, ECE, Mechanical — ranked preference)

---

## 2. Application Form

```
ADMISSION APPLICATION — 2026–27
GREENFIELDS COLLEGE OF ENGINEERING, Hyderabad
AICTE Approved | Affiliated to JNTU Hyderabad

PROGRAMME APPLIED FOR:
  ● B.Tech — Undergraduate Engineering (4 years)
  Priority 1: Computer Science & Engineering (CSE)
  Priority 2: Electronics & Communication Engineering (ECE)
  Priority 3: Mechanical Engineering (ME)

APPLICANT DETAILS:
  Name: Mr. Aakash Sharma
  Date of Birth: 14 July 2007
  Gender: Male
  Category: OBC-NCL ← [Caste certificate required]
  PwD: No
  Aadhaar: XXXX-XXXX-1234 (masked after entry)
  Mobile: +91 98XXXXXX
  Email: aakash.sharma2007@gmail.com

QUALIFYING EXAMINATION:
  Class XII Board: CBSE 2025
  Marks: 92.4% (PCM: 94.2%)
  Class XII Certificate: [Upload PDF] ✅

ENTRANCE EXAM:
  JEE Main 2025 (Session 2): Score 178/300  |  Percentile: 88.4
  JEE Score Card: [Upload PDF] ✅

CATEGORY DOCUMENTS:
  OBC (NCL) Certificate: [Upload PDF] — issued by MRO, Secunderabad ✅
  Income Certificate: ₹4,20,000/year ← [EWS: income ≤8L; OBC-NCL income ≤8L for central institutions]

APPLICATION FEE:
  Category: OBC-NCL → ₹500 (general: ₹600; SC/ST/PwD: ₹0)
  Payment: [Pay via UPI/Card] → ✅ Paid (TXN-2026-GCEH-00412)

[Submit Application]  |  Application ID: APP-2026-CSE-00412
```

---

## 3. Application Dashboard — Admissions Officer View

```
APPLICATIONS DASHBOARD — B.Tech 2026–27
GREENFIELDS COLLEGE OF ENGINEERING

Total applications received: 1,847
  B.Tech CSE: 824  |  ECE: 412  |  Mechanical: 298  |  Civil: 183  |  EEE: 130

Intake (AICTE approved):
  CSE: 120 seats  |  ECE: 60 seats  |  ME: 60 seats  |  Civil: 60 seats  |  EEE: 60 seats
  Total: 360 seats

CATEGORY-WISE SEAT MATRIX (Telangana state norms — Engineering):
  Category      %    CSE  ECE  ME   Civil EEE   Total
  Open (UR)     25%   30   15   15    15   15     90
  OBC           27%   33   16   16    16   16     97
  SC            15%   18    9    9     9    9     54
  ST             6%    7    4    4     4    4     23
  EWS           10%   12    6    6     6    6     36
  BC-D/E         5%    6    3    3     3    3     18
  PwD (horiz.)   5%   (horizontal — across all categories)
  Management    30%   36   18   18    18   18    108
  NRI            3%    4    2    2     2    2     12
  ─────────────────────────────────────────────────────
  Convener:     70%  (state counselling — TGCHE)
  Management:   30%  (college's direct admission quota)

APPLICATIONS STATUS SUMMARY:
  Received:           1,847
  Verified:             892
  Pending verification: 744
  Rejected (incomplete): 211
  Shortlisted for merit list: 892

[Bulk verify applications]  [Generate merit list]  [TGCHE upload]
```

---

## 4. Document Verification

```
APPLICATION DETAIL — APP-2026-CSE-00412
Mr. Aakash Sharma

DOCUMENT CHECKLIST:
  ☑ Class XII mark sheet (CBSE 2025): ✅ Verified — PCM 94.2%
  ☑ JEE Main score card: ✅ Verified — Percentile 88.4
  ☑ OBC-NCL caste certificate: ✅ Verified (MRO stamp, recent date)
  ☑ OBC income certificate: ✅ ₹4,20,000 < ₹8L limit ← NCL confirmed
  ☑ Aadhaar copy: ✅ DOB matches
  ☑ Transfer Certificate (from Class XII school): ✅
  ☑ Passport photograph: ✅
  ☑ Application fee: ✅ Paid

ELIGIBILITY CHECK:
  ● PCM 45% minimum (OBC): 94.2% ✅ (AICTE B.Tech minimum eligibility)
  ● JEE Main valid score: ✅ (percentile 88.4 > 45th percentile minimum for OBC)
  ● Age: 18 years 8 months on admission date → ✅ (no upper age limit for B.Tech)

MERIT RANK (OBC-NCL, CSE):
  JEE Percentile weighted: 88.4%
  PCM marks weighted: 94.2%
  Combined score: 90.1 (formula: JEE 70% + PCM 30%)
  OBC-NCL CSE merit rank: 12/187 eligible OBC applicants ← Competitive ✅

STATUS: Verified ✅  |  [Add to merit list]  |  [Issue offer letter]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/applications/` | Submit application (public) |
| 2 | `GET` | `/api/v1/college/{id}/applications/` | List applications (staff) |
| 3 | `GET` | `/api/v1/college/{id}/applications/{app_id}/` | Application detail |
| 4 | `PATCH` | `/api/v1/college/{id}/applications/{app_id}/verify/` | Verify documents |
| 5 | `GET` | `/api/v1/college/{id}/applications/stats/` | Dashboard summary |
| 6 | `POST` | `/api/v1/college/{id}/applications/{app_id}/reject/` | Reject with reason |
| 7 | `GET` | `/api/v1/college/{id}/applications/merit-list/?programme={prog}&category={cat}` | Generate merit list |

---

## 6. Business Rules

- AICTE mandates minimum eligibility for B.Tech: 45% in PCM (40% for SC/ST/PwD); the application system must reject or flag applications below this threshold during initial screening; allowing ineligible applicants to enter the selection process creates legal risk
- OBC-NCL (Non-Creamy Layer) status depends on both caste and income (<₹8 lakh annual family income); the income certificate must be recent (issued within the current financial year or the preceding year); outdated income certificates (>2 years old) are a common application fraud vector
- Category certificates issued by Revenue authorities (MRO/Tahsildar) are the only valid documents; certificates from non-revenue offices are not accepted; the system flags certificates from unrecognised issuing authorities
- Management quota seats (30% in AICTE-affiliated private engineering colleges in TS) can be filled by the college directly — but even management quota students must meet minimum eligibility; filling management quota seats with ineligible students is an AICTE violation
- Application fee waiver (SC/ST/PwD) is mandatory per UGC/AICTE guidelines; no admission fee can be charged to SC/ST/PwD applicants at the application stage; the system enforces ₹0 fee for these categories automatically

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division A*
