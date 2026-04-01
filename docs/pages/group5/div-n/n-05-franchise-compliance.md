# N-05 — Franchise Compliance

> **URL:** `/coaching/compliance/franchise/`
> **File:** `n-05-franchise-compliance.md`
> **Priority:** P2
> **Roles:** Director (K7) · Branch Manager (K6) · Franchise Coordinator (K4)

---

## 1. Franchise Network Overview

```
FRANCHISE NETWORK — Toppers Coaching Centre
As of 31 March 2026

  FRANCHISES (active):
    #  │ Branch Name          │ City         │ Since  │ Students │ Compliance │ Royalty
    ───┼──────────────────────┼──────────────┼────────┼──────────┼────────────┼────────
    F1 │ TCC Secunderabad     │ Secunderabad │ 2020   │   640    │ ✅ Good    │ Current
    F2 │ TCC Warangal         │ Warangal     │ 2021   │   480    │ 🟡 Review │ Current
    F3 │ TCC Nizamabad        │ Nizamabad    │ 2022   │   360    │ ✅ Good    │ Current
    F4 │ TCC Karimnagar       │ Karimnagar   │ 2023   │   280    │ ✅ Good    │ Current
    F5 │ TCC Nalgonda         │ Nalgonda     │ 2023   │   220    │ ✅ Good    │ Current
    F6 │ TCC Khammam          │ Khammam      │ 2024   │   180    │ ✅ Good    │ Current
    ───┴──────────────────────┴──────────────┴────────┴──────────┴────────────┴────────
    TOTAL FRANCHISE STUDENTS: 2,160

  ROYALTY INCOME (AY 2025–26):
    Per-student royalty:  ₹1,500/student enrolled (deducted from fee collected)
    Annual royalty income: ₹32.4 L (2,160 students × ₹1,500)
    Collection status:    All 6 franchises current ✅

  COMPLIANCE ISSUES:
    TCC Warangal (F2): Faculty rating 3.8/5.0 — below 4.0 threshold ⚠️
                       Under review — action plan required by Apr 30
```

---

## 2. Franchise Agreement Compliance

```
FRANCHISE AGREEMENT — Key Obligations

  WHAT FRANCHISEE MUST DO:
    1. Use TCC brand, curriculum, and test series only ✅ (all branches)
    2. Pay royalty monthly (₹1,500/student) within 7 days of fee collection
    3. Maintain minimum standards: faculty rating > 4.0, SLA > 90%
    4. Use EduForge portal for all student management
    5. Submit monthly MIS report to TCC head office
    6. Obtain all local licences (Shop & Est., GST registration)
    7. Not conduct any competing activities (other exam coaching brands)
    8. Grant access for TCC quality audits (annual + unannounced spot visits)

  WHAT TCC MUST PROVIDE:
    1. Brand licence and usage rights
    2. Test series access (28 full mocks + sectionals)
    3. Study material (master copies for local printing)
    4. EduForge portal access and training
    5. Academic support (doubt resolution escalation to main faculty)
    6. Annual franchisee conference and training
    7. Marketing support (digital templates, social media guidance)

  TCC WARANGAL (F2) — COMPLIANCE REVIEW:
    Faculty rating Q3:    3.8/5.0 (below 4.0 threshold)
    MIS report (Mar):     Submitted late (8th instead of 5th)
    Royalty:              Current ✅
    Action:               Director call scheduled Apr 3 | Action plan due Apr 30
    Consequence if no improvement by Jun 2026: Franchise agreement review clause activated
```

---

## 3. Franchise MIS Comparison

```
FRANCHISE MIS — Q3 Performance Comparison

  Metric                  │ Main Hyd │ F1 Secy  │ F2 Warangal│ F3 Nizbd │ F4 Knagar│ F5 Nlgda
  ────────────────────────┼──────────┼──────────┼────────────┼──────────┼──────────┼────────
  Faculty avg rating      │  4.2/5   │  4.0/5   │  3.8/5 ⚠️  │  4.1/5   │  4.0/5   │  4.1/5
  Avg mock score          │ 142/200  │ 138/200  │  132/200   │ 136/200  │ 140/200  │ 138/200
  Attendance rate         │  87.3%   │  84.2%   │   81.6%    │  83.8%   │  86.4%   │  84.0%
  Doubt SLA compliance    │  91.2%   │  88.4%   │   82.4%    │  87.6%   │  89.2%   │  86.8%
  Collection rate         │  92.3%   │  89.4%   │   86.2%    │  88.8%   │  90.4%   │  87.6%
  Grievance rate          │  2.0%    │  1.8%    │   3.2% 🟡  │  1.6%    │  1.4%    │  1.8%
  Student satisfaction    │  4.2/5   │  4.0/5   │  3.7/5 ⚠️  │  4.0/5   │  4.1/5   │  4.0/5
  ────────────────────────┴──────────┴──────────┴────────────┴──────────┴──────────┴────────

  NETWORK AVERAGE (all branches): Faculty: 4.0 | Score: 138 | Satisfaction: 4.0
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/compliance/franchise/` | Franchise network overview |
| 2 | `GET` | `/api/v1/coaching/{id}/compliance/franchise/{fid}/` | Individual franchise compliance |
| 3 | `GET` | `/api/v1/coaching/{id}/compliance/franchise/mis/` | Franchise comparison MIS |
| 4 | `POST` | `/api/v1/coaching/{id}/compliance/franchise/{fid}/action/` | Log compliance action |
| 5 | `GET` | `/api/v1/coaching/{id}/compliance/franchise/royalty/` | Royalty collection status |

---

## 5. Business Rules

- The franchise agreement is TCC's primary legal tool for maintaining quality standards across branches; it is not merely a revenue arrangement but a quality assurance contract; a franchisee who uses the TCC brand must deliver a minimum quality standard (faculty rating > 4.0, student satisfaction > 3.8) because student dissatisfaction at TCC Warangal damages the TCC brand nationally — students search "TCC coaching review" and see negative reviews without knowing which branch they refer to; brand protection requires contractual enforcement of quality standards
- Royalty income of ₹1,500 per student is the economic model for TCC's franchise system; from TCC's perspective, each franchise student contributes ₹1,500 with zero service delivery cost (TCC provides curriculum and brand, franchise manages local operations); at 2,160 students, this generates ₹32.4 lakh with minimal marginal cost; however, the royalty model creates a tension — franchisees want to maximise enrollment (revenue) while TCC wants to maximise quality; a franchisee who enrolls 800 students with a 3.5/5.0 rating is more profitable for themselves but damages TCC's brand; the franchise agreement balances enrollment incentives with quality minimums
- Unannounced spot audits (permitted under the franchise agreement) are TCC's most effective quality monitoring tool; a franchisee who knows when the audit is coming can prepare for it; an unannounced visit during a class reveals the actual teaching environment — whether faculty are present, whether classes start on time, whether facilities match the commitment; TCC's Director conducts at least one unannounced visit per franchise per year; the audit finding must be documented, shared with the franchisee, and followed up within 30 days; a franchisee who refuses entry for an audit is in breach of the franchise agreement
- TCC Warangal's declining quality (3.8 faculty rating, 82.4% doubt SLA) requires a structured intervention before it reaches a threshold where franchise agreement termination must be considered; the Director's April 3 call is the first formal escalation; an action plan with specific targets (faculty rating ≥ 4.0 by Q4, doubt SLA ≥ 88% by Q4) and a 90-day review is the standard intervention; if targets are not met by June 2026, the franchise agreement's "quality breach" clause allows TCC to mandate management changes or, in extreme cases, terminate the franchise; franchise termination must follow the contractual notice period (90 days) and any applicable franchise law protections in India
- New franchise onboarding (Karimnagar and Khammam — planned for AY 2026–27) follows a 3-month pre-opening checklist: franchisee background verification (L-07 growth planning), legal agreement execution, EduForge setup and training, local licence verification (Shop & Est., GST, fire NOC), staff hiring support, and a "soft launch" with TCC main branch observers present; a franchise that opens without completing the pre-opening checklist creates immediate quality and legal risks; TCC's franchise coordinator manages the onboarding process and signs off on readiness before opening day

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division N*
