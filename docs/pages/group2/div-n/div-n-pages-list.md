# Division N — Legal & Compliance (Institution Group Level)
## Page Index

> **Division:** N — Legal & Compliance
> **Group:** Group 2 — Institution Groups (chains/trusts/societies owning 5–50 schools/colleges)
> **Scale:** 150 groups · 5–50 branches per group · ~1,900 total institutions
> **Base URL:** `/group/legal/`
> **Last updated:** 2026-03-21

---

## Overview

Division N covers the complete legal and compliance function for an Institution Group. It encompasses regulatory compliance with CBSE/State Board affiliation requirements, RTI Act 2005 obligations, POCSO Act 2012 mandatory reporting, DPDP Act 2023 data privacy, staff contract management, trust/society legal documents, litigation tracking, vendor agreements, and consolidated compliance calendaring across all branches.

### Two Deployment Profiles

| Profile | Branches | Students | Staffing Model |
|---|---|---|---|
| Large Group | 20–50 | 20,000–1,00,000 | Dedicated legal & compliance team (all 9 roles staffed) |
| Small Group | 5–10 | 2,000–8,000 | 1–2 people covering multiple roles; G0 roles absent |

---

## Roles in Division N

| Role ID | Role Name | Level | Large Group | Small Group |
|---|---|---|---|---|
| 108 | Group Legal Officer | G0 | Dedicated | Owner handles (no platform user) |
| 109 | Group Compliance Manager | G1 | Dedicated | Shared — primary compliance user |
| 110 | Group RTI Officer | G1 | Dedicated | Shared with Compliance Manager |
| 111 | Group Regulatory Affairs Officer | G0 | Dedicated | Owner handles (no platform user) |
| 112 | Group POCSO Reporting Officer | G1 | Dedicated | Shared — restricted access |
| 113 | Group Data Privacy Officer | G1 | Dedicated | Shared |
| 127 | Group Contract Administrator | G3 | Dedicated | N/A — Small Groups omit this role |
| 128 | Group Legal Dispute Coordinator | G1 | Dedicated | N/A — Small Groups omit this role |
| 129 | Group Insurance Coordinator | G1 | Dedicated | Shared |

**Access Level Summary:**
- G0 = No Platform Access (work in external tools; appear in role table for reference only)
- G1 = Read-Only (view dashboards, download reports, no create/edit/delete)
- G3 = Operations (full CRUD on contracts, staff, vendor agreements)
- G4 = Admin (configure portals, roles, feature toggles)
- G5 = Super Admin (unrestricted — Chairman/Founder)

---

## Pages in Division N

| # | File | Page Title | Priority | Primary Role | Key Function |
|---|---|---|---|---|---|
| 01 | `n-01-legal-compliance-dashboard.md` | Legal & Compliance Dashboard | P0 | Group Compliance Manager (109, G1) | Unified compliance score, deadlines, alerts |
| 02 | `n-02-affiliation-compliance-tracker.md` | Affiliation Compliance Tracker | P0 | Group Compliance Manager (109, G1) | CBSE/ICSE/State Board affiliation per branch |
| 03 | `n-03-rti-request-manager.md` | RTI Request Manager | P0 | Group RTI Officer (110, G1) | RTI Act 2005 — request tracking, 30-day deadlines |
| 04 | `n-04-regulatory-filings-tracker.md` | Regulatory Filings Tracker | P1 | Group Regulatory Affairs Officer (111, G0) | AISHE, UDISE+, State Dept annual filings |
| 05 | `n-05-pocso-incident-registry.md` | POCSO Incident Registry | P0 | Group POCSO Reporting Officer (112, G1) | POCSO Act 2012 — 24-hr NCPCR reporting |
| 06 | `n-06-data-privacy-dpdp.md` | Data Privacy & DPDP Compliance | P0 | Group Data Privacy Officer (113, G1) | DPDP Act 2023 — consent, 72-hr breach notification |
| 07 | `n-07-staff-contracts-registry.md` | Staff Contracts Registry | P1 | Group Contract Administrator (127, G3) | Employment contracts lifecycle, digital signatures |
| 08 | `n-08-trust-legal-document-repository.md` | Trust & Legal Document Repository | P0 | Group Legal Officer (108, G0) | Trust deed, land docs, certificates — encrypted vault |
| 09 | `n-09-legal-notices-litigation-register.md` | Legal Notices & Litigation Register | P1 | Group Legal Dispute Coordinator (128, G1) | Litigation tracking, court dates, legal notices |
| 10 | `n-10-vendor-legal-agreements.md` | Vendor & Third-Party Legal Agreements | P1 | Group Contract Administrator (127, G3) | Vendor/supplier contracts, AMCs, MOUs |
| 11 | `n-11-inspection-visit-tracker.md` | Inspection Visit Tracker | P1 | Group Compliance Manager (109, G1) | CBSE/NAAC/State inspection tracking, deficiencies |
| 12 | `n-12-student-parent-consent.md` | Student/Parent Consent Management | P1 | Group Data Privacy Officer (113, G1) | DPDP Act 2023 consent records, mass campaigns |
| 13 | `n-13-insurance-registry.md` | Insurance Registry | P1 | Group Insurance Coordinator (129, G1) | Policy tracking, claims management |
| 14 | `n-14-annual-returns-statutory-filings.md` | Annual Returns & Statutory Filings | P1 | Group Compliance Manager (109, G1) | IT returns, PF/ESI, fee regulation consolidated |
| 15 | `n-15-compliance-policy-repository.md` | Compliance Policy Repository | P2 | Group Compliance Manager (109, G1) | Versioned policies, branch acknowledgement |
| 16 | `n-16-compliance-audit-report.md` | Compliance Audit Report | P1 | Group Compliance Manager (109, G1) | Annual audit — branch scores, radar chart, trend |
| 17 | `n-17-grievance-legal-escalations.md` | Grievance Legal Escalations | P1 | Group Legal Dispute Coordinator (128, G1) | Consumer forum, HC writs, legal stage tracking |
| 18 | `n-18-affiliation-renewal-calendar.md` | Affiliation Renewal Calendar | P1 | Group Compliance Manager (109, G1) | Visual calendar of all renewal deadlines |
| 19 | `n-19-cross-branch-compliance-status.md` | Cross-Branch Compliance Status | P0 | Group Compliance Manager (109, G1) | Executive matrix — all branches × all dimensions |
| 20 | `n-20-compliance-calendar.md` | Compliance Calendar & Unified Deadlines | P0 | Group Compliance Manager (109, G1) | Master deadline calendar, ICS export |

---

## Regulatory Framework Covered

| Regulation | Scope | Key Deadline |
|---|---|---|
| CBSE Affiliation Bye-laws 2018 | School affiliation renewal | As per affiliation cycle |
| RTI Act 2005 | Information request responses | 30 days (45 for third-party) |
| POCSO Act 2012 | Child sexual abuse incident reporting | 24 hours to NCPCR |
| DPDP Act 2023 | Personal data breach notification | 72 hours to CERT-In / DPB |
| IT Act 2000 + CERT-In Directions 2022 | Cyber incident reporting | 6 hours to CERT-In |
| AISHE Annual Reporting | Higher education statistics | September–October annually |
| UDISE+ / DISE | School data reporting | July–September annually |
| Income Tax Act (Trust) | 12A/80G compliance | As per AY deadlines |
| NITI Aayog / NGO Darpan | Society/trust registration | Annual renewal |
| PF / ESI (Labour laws) | Employee benefit filings | Monthly / annual |

---

## Navigation Structure

```
Group HQ
└── Legal & Compliance (Division N)
    ├── N-01  Legal & Compliance Dashboard          [Home / Landing]
    ├── N-02  Affiliation Compliance Tracker
    ├── N-03  RTI Request Manager
    ├── N-04  Regulatory Filings Tracker
    ├── N-05  POCSO Incident Registry               [Restricted]
    ├── N-06  Data Privacy & DPDP Compliance
    ├── N-07  Staff Contracts Registry
    ├── N-08  Trust & Legal Document Repository     [Restricted]
    ├── N-09  Legal Notices & Litigation Register   [Restricted]
    ├── N-10  Vendor & Third-Party Agreements
    ├── N-11  Inspection Visit Tracker
    ├── N-12  Student/Parent Consent Management
    ├── N-13  Insurance Registry
    ├── N-14  Annual Returns & Statutory Filings
    ├── N-15  Compliance Policy Repository
    ├── N-16  Compliance Audit Report
    ├── N-17  Grievance Legal Escalations
    ├── N-18  Affiliation Renewal Calendar
    ├── N-19  Cross-Branch Compliance Status
    └── N-20  Compliance Calendar & Unified Deadlines
```

---

## Access Matrix Summary

| Page | 108 (G0) | 109 (G1) | 110 (G1) | 111 (G0) | 112 (G1) | 113 (G1) | 127 (G3) | 128 (G1) | 129 (G1) |
|---|---|---|---|---|---|---|---|---|---|
| N-01 Dashboard | — | Read | Read | — | Read | Read | Read | Read | Read |
| N-02 Affiliation | — | Read | Read | — | — | — | — | — | — |
| N-03 RTI | — | Read | Read | — | — | — | — | — | — |
| N-04 Regulatory | — | Read | — | — | — | — | — | — | — |
| N-05 POCSO | — | Read | — | — | Read | — | — | — | — |
| N-06 DPDP | — | Read | — | — | — | Read | — | — | — |
| N-07 Contracts | — | Read | — | — | — | — | Full CRUD | — | — |
| N-08 Trust Docs | — | Read | — | — | — | — | — | Read | — |
| N-09 Litigation | — | Read | — | — | — | — | — | Read | — |
| N-10 Vendor Agr | — | Read | — | — | — | — | Full CRUD | — | — |
| N-11 Inspection | — | Read | — | — | — | — | — | — | — |
| N-12 Consent | — | Read | — | — | — | Read | — | — | — |
| N-13 Insurance | — | Read | — | — | — | — | — | — | Read |
| N-14 Returns | — | Read | — | — | — | — | — | — | — |
| N-15 Policies | — | Read | — | — | — | — | — | — | — |
| N-16 Audit | — | Read | — | — | — | — | — | — | — |
| N-17 Grievance | — | Read | — | — | — | — | — | Read | — |
| N-18 Calendar | — | Read | Read | — | — | — | — | — | — |
| N-19 Cross-Branch | — | Read | — | — | — | — | — | — | — |
| N-20 Cal Unified | — | Read | Read | — | — | — | — | — | — |

> G4 (CEO, IT Admin) and G5 (Chairman/Founder) have full read access to all pages.
> G5 additionally has export approval and configuration rights.
> "—" = No access (G0 roles have no platform login; other roles have no permission for that page).

---

---

## Completion Status

| # | File | Status | Lines (approx) |
|---|---|---|---|
| Index | `div-n-pages-list.md` | ✅ Complete | 155 |
| 01 | `n-01-legal-compliance-dashboard.md` | ✅ Complete | 335 |
| 02 | `n-02-affiliation-compliance-tracker.md` | ✅ Complete | 325 |
| 03 | `n-03-rti-request-manager.md` | ✅ Complete | 305 |
| 04 | `n-04-regulatory-filings-tracker.md` | ✅ Complete | 295 |
| 05 | `n-05-pocso-incident-registry.md` | ✅ Complete | 340 |
| 06 | `n-06-data-privacy-dpdp.md` | ✅ Complete | 340 |
| 07 | `n-07-staff-contracts-registry.md` | ✅ Complete | 310 |
| 08 | `n-08-trust-legal-document-repository.md` | ✅ Complete | 290 |
| 09 | `n-09-legal-notices-litigation-register.md` | ✅ Complete | 290 |
| 10 | `n-10-vendor-legal-agreements.md` | ✅ Complete | 270 |
| 11 | `n-11-inspection-visit-tracker.md` | ✅ Complete | 260 |
| 12 | `n-12-student-parent-consent.md` | ✅ Complete | 280 |
| 13 | `n-13-insurance-registry.md` | ✅ Complete | 250 |
| 14 | `n-14-annual-returns-statutory-filings.md` | ✅ Complete | 270 |
| 15 | `n-15-compliance-policy-repository.md` | ✅ Complete | 240 |
| 16 | `n-16-compliance-audit-report.md` | ✅ Complete | 280 |
| 17 | `n-17-grievance-legal-escalations.md` | ✅ Complete | 270 |
| 18 | `n-18-affiliation-renewal-calendar.md` | ✅ Complete | 260 |
| 19 | `n-19-cross-branch-compliance-status.md` | ✅ Complete | 290 |
| 20 | `n-20-compliance-calendar.md` | ✅ Complete | 360 |

**Total: 21 files · ~6,100 lines · 20 fully-specified pages · 8 audit fixes applied (v1.1)**

---

*Division N index version: 1.2 · Last updated: 2026-03-22*
