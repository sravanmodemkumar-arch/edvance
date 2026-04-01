# N-01 — Regulatory Compliance Overview

> **URL:** `/coaching/compliance/`
> **File:** `n-01-regulatory-compliance.md`
> **Priority:** P1
> **Roles:** Director (K7) · Branch Manager (K6) · Accounts Manager (K5)

---

## 1. Compliance Overview

```
REGULATORY COMPLIANCE DASHBOARD — Toppers Coaching Centre
As of 31 March 2026 | Financial Year End (FY 2025–26)

  COMPLIANCE HEALTH: ✅ COMPLIANT (36/38 items complete, 2 in progress)

  STATUS BY DOMAIN:
    Domain                    │ Items │ Compliant │ In Progress │ Overdue │ Risk
    ──────────────────────────┼───────┼───────────┼─────────────┼─────────┼────────
    Tax (IT, GST, TDS)        │  12   │    11     │      1      │    0    │ LOW ✅
    Labour (PF, ESI, Shops)   │   8   │     8     │      0      │    0    │ LOW ✅
    Student welfare (POCSO)   │   4   │     4     │      0      │    0    │ LOW ✅
    Data protection (DPDPA)   │   5   │     5     │      0      │    0    │ LOW ✅
    Food safety (FSSAI)       │   2   │     2     │      0      │    0    │ LOW ✅
    Fire & building safety    │   4   │     3     │      1      │    0    │ MED 🟡
    Consumer protection       │   3   │     3     │      0      │    0    │ LOW ✅
    ──────────────────────────┴───────┴───────────┴─────────────┴─────────┴────────
    TOTAL                     │  38   │    36     │      2      │    0    │ LOW ✅

  KEY LICENCES (all current):
    Shop & Establishment Registration:   Reg. No. TS-2018-12345 | Valid ✅
    GSTIN:                              36AABCT1234F1ZX | Registered Apr 2018 ✅
    PF Registration:                    TGHYD00012345000 ✅
    ESI Code:                           41000112345 ✅
    Fire NOC:                           HFD-2026-4521 | Valid till Jan 2027 ✅
    FSSAI (Nirmal Caterers, vendor):    10016012345678 | Valid till Aug 2026 ✅
    GHMC Building NOC (Block C):        GHMC-2026-BN-8920 | Obtained Mar 2026 ✅
```

---

## 2. Key Compliance Obligations

```
ACTIVE COMPLIANCE OBLIGATIONS — TCC Hyderabad

  1. INCOME TAX:
     Entity type:        Private limited company (TCC Edu Pvt Ltd)
     PAN:                AABCT1234F
     TAN:                HYDH01234A
     FY 2025–26 ITR:     Due 31 Jul 2026 (Accounts + CA preparation by Jun 2026)
     Advance tax:        All 4 instalments paid ✅ (Jun, Sep, Dec, Mar)
     Audit requirement:  Section 44AB (turnover > ₹1 Cr) — mandatory ✅

  2. GST:
     GST rate on coaching: 18% (SAC 9992 — private coaching centre)
     GST rate on hostel:   0% if tariff < ₹1,000/day; 12% if > ₹1,000/day
     TCC hostel tariff:    ₹350/day (below threshold → 0% GST) ✅
     Annual GSTR-9:        Due Dec 2026 (after FY 2025–26 reconciliation)

  3. TDS:
     Faculty salaries:    Section 192 (TDS on salary per slab rate)
     Vendor payments:     Section 194C (2%/1%) and 194J (10%)
     Student referral rewards: Section 194H (5%) if > ₹15,000/yr per payee
     Form 16 (salary):    Issued to staff by June 15 each year
     Form 16A (vendors):  Issued quarterly

  4. LABOUR LAW:
     PF: 12% employee + 12% employer on basic (≤ ₹15,000 or voluntary)
     ESI: 0.75% employee + 3.25% employer (if monthly wages ≤ ₹21,000)
     Gratuity: Payable after 5 years of continuous service (Payment of Gratuity Act)
     Minimum wage: All support staff paid above TS minimum wage (₹12,000+ basic) ✅
```

---

## 3. Compliance Risk Register

```
COMPLIANCE RISK REGISTER — As of 31 March 2026

  Risk                          │ Likelihood │ Impact │ Risk Score │ Mitigation
  ──────────────────────────────┼────────────┼────────┼────────────┼──────────────────────────
  GST notice (ITC mismatch)     │  LOW       │  HIGH  │   MEDIUM   │ Monthly reconciliation ✅
  TDS default (vendor payment)  │  LOW       │  HIGH  │   MEDIUM   │ Auto calendar reminder ✅
  DPDPA consent gap             │  MEDIUM    │  HIGH  │   HIGH     │ Consent audit Q1 FY26-27
  Data breach (student data)    │  LOW       │ V.HIGH │   HIGH     │ MFA, encryption, backup ✅
  POCSO allegation (unfounded)  │  LOW       │ V.HIGH │   HIGH     │ POCSO SOP + counsellor ✅
  Consumer complaint (false ad) │  LOW       │  MEDIUM│   MEDIUM   │ Disclaimer on all ads ✅
  Fire incident (hostel)        │  LOW       │ V.HIGH │   HIGH     │ NOC, drills, extinguishers ✅
  Block C occupancy w/o NOC     │  MEDIUM    │  HIGH  │   HIGH     │ NOC scheduled pre-Aug 2026 🟡
  ──────────────────────────────┴────────────┴────────┴────────────┴──────────────────────────

  HIGH RISK ITEMS REQUIRING DIRECTOR ATTENTION:
    (a) DPDPA consent audit — schedule before Jul 2026 (FY start)
    (b) Block C occupancy NOC — application to be filed Jun 2026 for Aug target
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/compliance/overview/` | Compliance dashboard |
| 2 | `GET` | `/api/v1/coaching/{id}/compliance/licences/` | Licence register and expiry |
| 3 | `GET` | `/api/v1/coaching/{id}/compliance/risks/` | Compliance risk register |
| 4 | `PATCH` | `/api/v1/coaching/{id}/compliance/risks/{rid}/` | Update risk mitigation status |
| 5 | `GET` | `/api/v1/coaching/{id}/compliance/obligations/` | Regulatory obligations by category |

---

## 5. Business Rules

- TCC as a private coaching centre offering commercial coaching services (SSC/Banking exam prep) is classified as a service provider subject to 18% GST on coaching fees; this is different from government-recognised educational institutions exempt from GST; TCC is not eligible for the educational institution GST exemption; TCC must collect GST from students, file monthly returns, and remit the tax to the government; failure to charge or collect GST when required is a liability — TCC becomes responsible for the tax amount that was not collected
- TCC's annual turnover exceeding ₹1 crore triggers the mandatory tax audit under Section 44AB of the Income Tax Act; the audit must be completed by a Chartered Accountant and the audit report filed before the ITR; the ITR deadline for companies subject to audit is October 31 (after CA completes audit by September 30); TCC's CA engagement must be active and ongoing, not just at year-end; the CA advises on tax planning (legal), not tax evasion (illegal); any advice that involves suppressing income, inflating expenses, or misclassifying transactions must be rejected by the Director
- Minimum wage compliance is verified annually; the Telangana government revises minimum wages every 6 months; the Operations Coordinator checks the current minimum wage gazette before each revision and ensures all support staff (security, housekeeping, maintenance) are paid at or above the applicable category rate; paying below minimum wage is a criminal offence under the Minimum Wages Act 1948; documentation of minimum wage compliance (payslips, salary registers) must be maintained and available for inspection by the Labour Department
- The compliance risk register is reviewed quarterly by the Director and Branch Manager; risks are not static — a "LOW likelihood" data breach risk can become "HIGH" if TCC's IT coordinator leaves without a replacement; the risk register must be updated when staff change, regulatory requirements change, or a near-miss incident occurs; the Director assigns a named owner to each HIGH-risk item; an unowned HIGH risk item is itself a governance failure; risk management is about anticipating failures, not just responding to them
- Consumer Protection Act 2019 requires TCC to honour all service commitments made at enrollment (batch schedule, faculty, study material, test series); if TCC cannot deliver the committed service (faculty quits mid-course, batch cancelled), TCC must either provide an equivalent alternative or issue a pro-rata refund; a consumer complaint to the Consumer Disputes Redressal Commission (CDRC) about an unfulfilled service commitment could result in a compensation order; TCC's enrollment agreement (F-04) documents all service commitments and the remedies in case of non-delivery — this protects TCC legally while being fair to students

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division N*
