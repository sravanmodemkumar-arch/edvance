# A-05 — Franchise Network Management

> **URL:** `/coaching/admin/franchise/`
> **File:** `a-05-franchise-network.md`
> **Priority:** P2
> **Roles:** Director/Owner (K7) · Franchise Network Head (K5)

---

## 1. Franchise Network Overview

```
FRANCHISE NETWORK — TOPPERS COACHING CENTRE
As of 30 March 2026

NETWORK SUMMARY:
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  6 Active        1 Onboarding      2 Prospect         ₹8.4L                 │
  │  Franchise       franchise         enquiries          Royalty collected      │
  │  branches        (Warangal)        (Karimnagar, Vizag) (March 2026)          │
  └──────────────────────────────────────────────────────────────────────────────┘

FRANCHISE LIST:
  ┌───┬──────────────────────────────┬──────────┬────────┬──────────┬─────────────┬──────────┐
  │ # │ Franchise Name               │ City     │ Stud.  │ Rev(MTD) │ Royalty Due │ Status   │
  ├───┼──────────────────────────────┼──────────┼────────┼──────────┼─────────────┼──────────┤
  │ 1 │ TCC Vijayawada               │ Vijayawa.│   320  │ ₹9.6L    │ ₹1.44L      │ ✅ Active │
  │ 2 │ TCC Rajahmundry              │ Rajahmun.│   240  │ ₹7.2L    │ ₹1.08L      │ ✅ Active │
  │ 3 │ TCC Nellore                  │ Nellore  │   180  │ ₹5.4L    │ ₹0.81L      │ ✅ Active │
  │ 4 │ TCC Kurnool                  │ Kurnool  │   160  │ ₹4.8L    │ ₹0.72L      │ ✅ Active │
  │ 5 │ TCC Tirupati                 │ Tirupati │   140  │ ₹4.2L    │ ₹0.63L      │ ✅ Active │
  │ 6 │ TCC Nizamabad                │ Nizamabad│   120  │ ₹3.6L    │ ₹0.54L      │ ✅ Active │
  │ 7 │ TCC Warangal                 │ Warangal │    60  │ ₹1.8L    │ ₹0.27L      │ ⚙️ Onboard│
  └───┴──────────────────────────────┴──────────┴────────┴──────────┴─────────────┴──────────┘

  Total franchise students: 1,220 | Total royalty receivable (March): ₹5.49L
  Royalty collected (March): ₹4.92L | Overdue: ₹0.57L (TCC Nellore — 18 days)
```

---

## 2. Franchise Compliance Dashboard

```
FRANCHISE COMPLIANCE STATUS — TCC NETWORK

  ┌──────────────────────────────────────────────────────────────────────────────┐
  │ Requirement              │ TCC-VJA │ TCC-RJY │ TCC-NLR │ TCC-KNL │ TCC-TPT │
  ├──────────────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
  │ Branding guidelines      │ ✅      │ ✅      │ ⚠️*     │ ✅      │ ✅      │
  │ EduForge platform use    │ ✅      │ ✅      │ ✅      │ ✅      │ ✅      │
  │ BGV for all staff        │ ✅      │ ⚠️**    │ ✅      │ ✅      │ ✅      │
  │ Monthly royalty payment  │ ✅      │ ✅      │ 🔴 Late │ ✅      │ ✅      │
  │ Quarterly audit          │ ✅      │ ✅      │ ✅      │ ⬜ Due  │ ✅      │
  │ Mock test on TCC paper   │ ✅      │ ✅      │ ✅      │ ✅      │ ⚠️***  │
  └──────────────────────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

  * TCC Nellore: New hoarding printed without brand approval — corrective notice sent
  ** TCC Rajahmundry: 2 faculty BGV pending > 30 days — escalation to franchise owner
  *** TCC Tirupati: Used own question paper for last mock (not TCC standardised) — issue raised
```

---

## 3. Franchise Agreement Summary

```
FRANCHISE AGREEMENT — KEY TERMS (Standard TCC Franchise)

  Agreement duration:      3 years (renewable)
  Royalty structure:       15% of gross monthly fee collection
  Royalty due date:        5th of following month
  Late payment penalty:    1.5% per month on outstanding royalty
  Minimum student target:  100 students within 6 months of launch
  Brand compliance:        All marketing material must use TCC templates
  Platform mandate:        EduForge platform mandatory — no alternative LMS
  Question papers:         All mock tests must use TCC question bank
  BGV mandate:             All staff BGV within 30 days of joining
  Exit clause:             3-month notice; TCC retains student data

ONBOARDING CHECKLIST — TCC WARANGAL (in progress):
  ✅ Agreement signed: 10 Feb 2026
  ✅ Franchise fee paid: ₹3.5L (one-time)
  ✅ EduForge portal configured
  ✅ Staff BGV initiated (4 staff)
  ✅ Branding materials sent
  ⬜ Physical inspection by TCC Compliance Officer (due 5 Apr 2026)
  ⬜ First batch launch (target: 15 Apr 2026)
  ⬜ Student enrollment open
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/franchise/` | List all franchise branches |
| 2 | `GET` | `/api/v1/coaching/{id}/franchise/{fid}/` | Franchise detail + compliance status |
| 3 | `GET` | `/api/v1/coaching/{id}/franchise/royalty/` | Royalty collection status (all branches) |
| 4 | `POST` | `/api/v1/coaching/{id}/franchise/` | Onboard new franchise |
| 5 | `POST` | `/api/v1/coaching/{id}/franchise/{fid}/compliance/flag/` | Raise compliance issue |
| 6 | `GET` | `/api/v1/coaching/{id}/franchise/{fid}/performance/` | Student count + revenue trend |

---

## 5. Business Rules

- Royalty is calculated on gross fee collection, not net; a franchise that collects ₹9.6L in gross fees owes ₹1.44L royalty even if it has ₹2L in refund requests pending — this is standard franchise practice because TCC cannot control how a franchise manages its refund policy; the royalty obligation is triggered by collection, not by net revenue; franchise owners must factor this into their cash flow management
- EduForge platform usage is mandatory for all franchise branches — this is a non-negotiable contract term; TCC's ability to maintain brand quality, question bank integrity, and student data security depends on all branches using the same platform; a franchise using WhatsApp groups and Google Forms instead of EduForge violates the agreement and will receive a formal notice; three notices result in franchise termination
- Student data generated at franchise branches is owned by TCC, not the franchise owner; on exit, the franchise owner cannot retain any student contact data, test history, or fee records; this protects TCC's student relationship and prevents ex-franchisees from launching competing coaching centres using TCC's student database; EduForge stores all data in TCC's tenant schema, not a separate franchise schema
- The quarterly franchise audit is a physical visit by TCC's Franchise Compliance Officer; it checks infrastructure (classrooms, library, network), staff BGV certificates, branding compliance, and student satisfaction; audits cannot be waived even if the franchise is performing well financially — a high-revenue franchise with poor student welfare is a brand risk; TCC Kurnool's overdue audit must be completed within 30 days or franchise status will be placed under review
- Franchise performance data (student counts, revenue, compliance score) is visible to the Director and Franchise Network Head; individual franchise owners can only see their own branch data; this prevents competitive intelligence sharing between franchisees and ensures each franchise competes on quality rather than on knowledge of other franchisees' pricing or student volumes

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division A*
