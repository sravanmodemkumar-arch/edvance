# M-05 — Vendor & Supplier Management

> **URL:** `/coaching/operations/vendors/`
> **File:** `m-05-vendor-management.md`
> **Priority:** P3
> **Roles:** Branch Manager (K6) · Operations Coordinator (K4) · Accounts Manager (K5)

---

## 1. Vendor Register

```
VENDOR REGISTER — Toppers Coaching Centre
As of 31 March 2026

  ACTIVE VENDORS:
    ID    │ Vendor Name           │ Category          │ Contract │ Annual Value │ Status
    ──────┼───────────────────────┼───────────────────┼──────────┼──────────────┼──────────
    V-001 │ EduForge Pvt Ltd      │ SaaS Platform     │ Annual   │ ₹3.60 L     │ ✅ Active
    V-002 │ CoolTech AC Services  │ AC Maintenance    │ AMC      │ ₹0.96 L     │ ✅ Active
    V-003 │ PrintMaster Hyd       │ Study material    │ Per order│ ₹1.20 L     │ ✅ Active
    V-004 │ Nirmal Caterers       │ Hostel mess (food)│ Monthly  │ ₹8.40 L     │ ✅ Active
    V-005 │ SecureGuard Agency    │ Security services │ Monthly  │ ₹2.40 L     │ ✅ Active
    V-006 │ Clean Sweep Hyd       │ Housekeeping      │ Monthly  │ ₹0.84 L     │ ✅ Active
    V-007 │ Airtel Leased Line    │ Internet (primary)│ Annual   │ ₹1.44 L     │ ✅ Active
    V-008 │ BSNL (backup)         │ Internet (backup) │ Annual   │ ₹0.36 L     │ ✅ Active
    V-009 │ S.V. Electricals      │ Electrical repair │ Per call │ ₹0.18 L     │ ✅ Active
    V-010 │ Raju Carpentry Works  │ Furniture repair  │ Per call │ ₹0.12 L     │ ✅ Active
    V-011 │ Zoom Video Comm.      │ Online classes    │ Annual   │ ₹0.48 L     │ ✅ Active
    V-012 │ Microsoft (reseller)  │ Office 365        │ Annual   │ ₹0.84 L     │ ✅ Active
    ──────┴───────────────────────┴───────────────────┴──────────┴──────────────┴──────────
    TOTAL ANNUAL VENDOR SPEND: ₹20.82 L

  VENDORS UNDER REVIEW:
    V-002 (CoolTech): 8-day delay on Room 4 AC — performance review Apr 2026
    V-003 (PrintMaster): Price increase request 12% — counter-negotiation pending
```

---

## 2. Vendor Performance

```
VENDOR PERFORMANCE REVIEW — Q3 AY 2025–26

  Vendor           │ Category    │ SLA Met% │ Quality │ Responsiveness│ Rating │ Action
  ─────────────────┼─────────────┼──────────┼─────────┼───────────────┼────────┼──────────────
  EduForge         │ SaaS        │  99.6%   │  4.8/5  │    Excellent  │ ⭐⭐⭐⭐⭐ │ Renew ✅
  Nirmal Caterers  │ Mess food   │  96.4%   │  4.2/5  │    Good       │ ⭐⭐⭐⭐  │ Continue
  SecureGuard      │ Security    │  98.8%   │  4.4/5  │    Good       │ ⭐⭐⭐⭐  │ Continue
  Airtel           │ Internet    │  99.1%   │  4.6/5  │    Excellent  │ ⭐⭐⭐⭐⭐ │ Continue
  PrintMaster      │ Printing    │  88.4%   │  3.9/5  │    Average    │ ⭐⭐⭐   │ Negotiate fee
  CoolTech AC      │ AC maint.   │  72.0%   │  3.4/5  │    Poor ⚠️    │ ⭐⭐    │ PIP / Replace
  Clean Sweep      │ Housekeep.  │  94.2%   │  4.0/5  │    Good       │ ⭐⭐⭐⭐  │ Continue

  CoolTech AC — Escalation:
    SLA breach count (Q3):  4 incidents
    Current open breach:    8 days (Room 4 AC — MNT-42)
    Action: Formal notice issued 30 Mar 2026; find alternative vendor by Apr 15
```

---

## 3. Purchase Orders

```
PURCHASE ORDERS — March 2026

  PO#     │ Vendor         │ Item                      │ Amount   │ Status
  ────────┼────────────────┼───────────────────────────┼──────────┼──────────────
  PO-0184 │ PrintMaster    │ SSC CGL study material Q4 │ ₹28,400  │ ✅ Delivered
  PO-0185 │ Nirmal Catrers │ Mess food (March)         │ ₹70,000  │ ✅ Delivered
  PO-0186 │ SecureGuard    │ Security services (March) │ ₹20,000  │ ✅ Delivered
  PO-0187 │ Office depot   │ Stationery (Q1 supply)    │ ₹ 4,200  │ ⏳ Pending
  PO-0188 │ Local supplier │ Whiteboard markers (24pk) │ ₹ 1,800  │ ⏳ Pending

  APPROVAL WORKFLOW:
    < ₹5,000:      Operations Coordinator approves
    ₹5,001–₹50,000: Branch Manager approves
    > ₹50,000:     Director approves
    All POs:       Accounts reviews before payment

  TDS ON VENDOR PAYMENTS:
    Nirmal Caterers (mess):  Section 194C — TDS 2% if annual > ₹1L ✅
    SecureGuard:             Section 194C — TDS 2% ✅
    EduForge:                Section 194J — TDS 10% (professional service) ✅
    PrintMaster:             Section 194C — TDS 1% (individual) ✅
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/operations/vendors/` | Vendor register |
| 2 | `GET` | `/api/v1/coaching/{id}/operations/vendors/{vid}/performance/` | Vendor performance rating |
| 3 | `POST` | `/api/v1/coaching/{id}/operations/vendors/purchase-orders/` | Create purchase order |
| 4 | `GET` | `/api/v1/coaching/{id}/operations/vendors/purchase-orders/` | All purchase orders |
| 5 | `PATCH` | `/api/v1/coaching/{id}/operations/vendors/purchase-orders/{pid}/approve/` | Approve PO |

---

## 5. Business Rules

- Vendor selection for contracts above ₹1 lakh annual value requires a minimum of 3 competitive quotes; the selection criteria include price, quality, responsiveness, and vendor financial stability; the Branch Manager documents the selection rationale in the procurement file; selecting a higher-priced vendor (e.g., SecureGuard at ₹2.4 lakh vs a cheaper agency at ₹1.8 lakh) is permissible if the quality justification is documented; the Director reviews all new vendor contracts above ₹5 lakh; this documented procurement process protects TCC from allegations of vendor favouritism or kickbacks
- TDS deduction on vendor payments is a legal obligation; TCC is required to deduct TDS at source (Section 194C for contractors, 194J for professional services) and remit to the Income Tax department by the 7th of the following month; failure to deduct TDS makes TCC jointly liable for the tax; failure to remit attracts interest at 1.5% per month and potential prosecution; the Accounts Manager maintains a TDS deduction register and files quarterly TDS returns (Form 26Q); vendors receive Form 16A annually showing TDS deducted — this is important for their own tax filings
- Vendor performance issues (CoolTech's 72% SLA compliance) follow a structured escalation: (1) verbal warning at first breach; (2) formal written notice at repeated breaches; (3) contract termination with 30 days' notice if performance doesn't improve; the AMC contract with CoolTech includes a penalty clause for SLA breaches (₹500 per breach day); invoking this clause and finding an alternative vendor are both legitimate responses to the current 8-day Room 4 breach; TCC should not remain with a consistently underperforming vendor out of relationship inertia
- The hostel mess contract with Nirmal Caterers (₹8.4 lakh/year, the largest vendor spend) requires monthly quality inspections; the Branch Manager or Operations Coordinator visits the mess at least twice per month unannounced to check food quality, hygiene, and adherence to the agreed menu; the FSSAI licence of Nirmal Caterers must be valid and displayed at the mess; TCC holds a copy of Nirmal's FSSAI licence in the vendor file; serving food without a valid FSSAI licence from the caterer is a compliance risk for TCC as the institution operating the hostel (N-01 compliance section)
- PrintMaster's price increase request (12%) requires negotiation before acceptance; the Branch Manager obtains 2 alternative quotes from other printers; if competitors quote 8% lower than the proposed new rate, TCC uses this to negotiate PrintMaster down to a 5–6% increase; if PrintMaster is unwilling, TCC switches vendors; long-term vendor relationships have value (familiarity with TCC's materials, quality consistency) but not unconditional loyalty; the negotiation outcome and the final agreed rate are documented before the new purchase orders are processed

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division M*
