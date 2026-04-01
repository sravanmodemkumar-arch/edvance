# N-04 — Financial & Tax Compliance

> **URL:** `/coaching/compliance/financial/`
> **File:** `n-04-financial-compliance.md`
> **Priority:** P2
> **Roles:** Director (K7) · Accounts Manager (K5) · Branch Manager (K6)

---

## 1. GST Compliance

```
GST COMPLIANCE — TCC Edu Pvt Ltd
GSTIN: 36AABCT1234F1ZX | State: Telangana (36)

  GST RATE SCHEDULE:
    Service                    │ SAC Code │ GST Rate │ Notes
    ───────────────────────────┼──────────┼──────────┼──────────────────────────────
    Coaching / tuition fees    │  9992    │   18%    │ Private coaching (not exempt)
    Hostel fees                │  9963    │    0%    │ < ₹1,000/day tariff → exempt
    Study material (printed)   │  4901    │    5%    │ Educational books
    Study material (digital)   │  9984    │   18%    │ Online content delivery
    Test series subscription   │  9984    │   18%    │ Online service
    Certificate fees           │  9983    │   18%    │ Admin/professional service
    ───────────────────────────┴──────────┴──────────┴──────────────────────────────

  MONTHLY FILING STATUS (FY 2025–26):
    Month    │ GSTR-1  │ GSTR-3B │ Tax Paid │ Late Fee │ Status
    ─────────┼─────────┼─────────┼──────────┼──────────┼────────
    Apr-25   │ ✅      │ ✅      │ ₹ 82,400 │  ₹0      │ OK
    May-25   │ ✅      │ ✅      │ ₹ 92,800 │  ₹0      │ OK
    Jun-25   │ ✅      │ ✅      │ ₹ 98,400 │  ₹0      │ OK
    [Jul–Feb] │ All ✅  │ All ✅  │ —        │  ₹0      │ OK
    Mar-26   │ ✅      │ ✅      │ ₹118,400 │  ₹0      │ OK ✅
    ─────────┴─────────┴─────────┴──────────┴──────────┴────────
    FY TOTAL GST PAID:  ₹14.2 L  | Pending input credit review: Apr 2026
```

---

## 2. TDS Compliance

```
TDS COMPLIANCE — FY 2025–26

  TDS DEDUCTION REGISTER (Q4 — Jan–Mar 2026):

    Section │ Category           │ Rate │ Threshold │ TDS Deducted │ Filed (26Q)
    ────────┼────────────────────┼──────┼───────────┼──────────────┼────────────
    192     │ Salary (faculty)   │ Slab │    N/A    │  ₹2.84 L    │ ✅ (24Q)
    192     │ Salary (non-teach) │ Slab │    N/A    │  ₹0.96 L    │ ✅ (24Q)
    194C    │ Vendor contracts   │  2%  │  ₹30,000  │  ₹0.42 L    │ ✅ (26Q)
    194J    │ EduForge (SaaS)    │ 10%  │  ₹30,000  │  ₹0.36 L    │ ✅ (26Q)
    194H    │ Referral commissions│  5% │  ₹15,000  │  ₹0.08 L    │ ✅ (26Q)
    ────────┴────────────────────┴──────┴───────────┴──────────────┴────────────
    TOTAL TDS (Q4):  ₹4.66 L  | Annual FY25-26 TDS: ₹18.4 L

  KEY DATES (Q4 FY 2025–26):
    TDS remittance (Jan–Mar):   ✅ Paid 7th each month
    Form 26Q (Q4):              Due 30 Apr 2026 — ⏳ preparation in progress
    Form 24Q (Q4 salary TDS):   Due 30 Apr 2026 — ⏳ preparation in progress
    Form 16 (staff):            To be issued by 15 Jun 2026
    Form 16A (vendors):         To be issued by 15 Jun 2026

  REFERRAL REWARD TDS NOTE:
    Student referrals > ₹15,000/yr: TDS 5% (Sec 194H — Commission/Brokerage)
    Alumni referral awards (non-cash "Ambassador" recognition): No TDS ✅
    Cash referral awards to alumni: Would attract 194H — AVOIDED (L-07 policy)
```

---

## 3. Income Tax & Audit

```
INCOME TAX — FY 2025–26 (TCC Edu Pvt Ltd)

  ADVANCE TAX (paid quarterly):
    Jun 2025 instalment:   ₹3.20 L ✅
    Sep 2025 instalment:   ₹6.40 L ✅
    Dec 2025 instalment:   ₹9.60 L ✅
    Mar 2026 instalment:   ₹3.20 L ✅ (paid 15 Mar 2026)
    Total advance tax:     ₹22.40 L

  ESTIMATED TAX LIABILITY (FY 2025–26):
    Net profit before tax:  ₹48.38 L (K-04 revenue MIS)
    Corporate tax rate:     22% + 10% surcharge + 4% cess = 25.17%
    Estimated tax:          ₹12.18 L
    Advance tax paid:       ₹22.40 L (excess — refund or adjust in ITR)
    Note: Final liability after CA computation — advance tax estimated
    ITR filing:             Due 31 Oct 2026 (post-audit) — CA engaged ✅

  STATUTORY AUDIT:
    Auditor:    M/s Sharma & Associates, CAs, Hyderabad
    Engaged:    Annual retainer ₹1.2 L/yr
    FY 2025–26 audit:    Starts Jun 2026, target completion Sep 2026
    Audit scope:  Financial statements, TDS, GST reconciliation, compliance
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/compliance/financial/gst/` | GST filing status |
| 2 | `GET` | `/api/v1/coaching/{id}/compliance/financial/tds/` | TDS deduction register |
| 3 | `GET` | `/api/v1/coaching/{id}/compliance/financial/advance-tax/` | Advance tax payment record |
| 4 | `GET` | `/api/v1/coaching/{id}/compliance/financial/audit/` | Audit status and timeline |
| 5 | `POST` | `/api/v1/coaching/{id}/compliance/financial/tds/remittance/` | Record TDS remittance |

---

## 5. Business Rules

- GST Input Tax Credit (ITC) allows TCC to offset GST paid on purchases (vendor invoices where vendors charge GST) against GST collected from students; for example, if EduForge charges ₹3.6 lakh + 18% GST (₹64,800), TCC can claim this as ITC against the GST liability from student fees; the ITC must be reconciled monthly in GSTR-2B (auto-populated from vendor filings); a vendor who does not file their GST returns denies TCC the ITC on that purchase; TCC must monitor vendor GST compliance and avoid vendors with repeated filing failures as it creates TCC's own ITC risk
- Excess advance tax (TCC paid ₹22.4 lakh advance tax vs an estimated ₹12.18 lakh liability) results in a refund upon filing the ITR; the CA will compute the exact liability after all deductions (depreciation, welfare expenses, professional fees); the refund typically takes 3–6 months after ITR filing; excess advance tax does not earn interest if paid before the due dates; the accounts team should compute advance tax more precisely in FY 2026–27 to avoid unnecessary cash outflow (the ₹10.2 lakh excess tied up for up to 18 months represents an opportunity cost)
- The Section 194H TDS on student referral rewards requires careful tracking; if a student refers multiple students and earns cumulative rewards exceeding ₹15,000 in a financial year, TDS at 5% must be deducted before payment; TCC must obtain the student's PAN to deduct TDS correctly; if the student does not provide PAN, TDS is deducted at 20%; the deducted amount is remitted to the IT department and reflected in Form 26AS of the student (who can claim credit in their own ITR); the referral reward register (F-08) must track cumulative rewards per student per financial year
- Corporate tax at 25.17% (22% + surcharge + cess) applies to TCC as a domestic company that has opted for the concessional tax rate under Section 115BAA; this rate is available only if TCC does not claim certain exemptions (80IC, 80IB); TCC's CA confirmed in FY 2022-23 that the 115BAA regime is more favourable than the regular rate with exemptions; the regime choice, once made, is irrevocable; the Director should not approve any tax advice that suggests switching back to the old regime without CA validation
- The statutory audit (Section 44AB mandatory audit) is different from an internal audit; the statutory audit is conducted by an independent CA firm (M/s Sharma & Associates) and results in a Tax Audit Report (Form 3CB/3CD) filed along with the ITR; it certifies that TCC's accounts are maintained correctly and that taxable income is computed correctly; the auditor has the right to access all financial records, books of accounts, and supporting documents; denying auditor access to any record is a serious compliance violation; the Director and Branch Manager must cooperate fully and provide all requested documents within the audit timeline

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division N*
