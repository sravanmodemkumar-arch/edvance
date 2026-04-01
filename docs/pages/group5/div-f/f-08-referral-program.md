# F-08 — Referral Program Management

> **URL:** `/coaching/admissions/referral/`
> **File:** `f-08-referral-program.md`
> **Priority:** P3
> **Roles:** Admissions Counsellor (K3) · Accounts (K5) · Branch Manager (K6)

---

## 1. Referral Program Overview

```
REFERRAL PROGRAM — Toppers Coaching Centre
As of 30 March 2026

  CURRENT SCHEME:
    Refer a friend → ₹ 1,000 reward (credited to your fee account or bank)
    Condition: Friend must enroll + attend at least 30 days of classes
    Max referrals: No cap per student
    Referral discount for referred student: ₹ 500 off base fee

  STATS (March 2026):
    Total active referrers:       84 students
    New referrals this month:     42 leads
    Enrolled via referral:        26 students
    Referral-to-enroll rate:      61.9% ← highest of all sources ✅
    Rewards pending payout:       ₹ 18,000 (18 confirmed, awaiting 30-day rule)
    Rewards paid (March):         ₹ 14,000 (14 referrals past 30-day mark)

  TOP REFERRERS:
    1. Akhil Kumar (TCC-2401):      4 referrals enrolled  → ₹ 4,000 earned
    2. Divya Sharma (TCC-2404):     3 referrals enrolled  → ₹ 3,000 earned
    3. Priya Reddy (TCC-2402):      2 referrals enrolled  → ₹ 2,000 earned
```

---

## 2. Referral Claim & Approval

```
REFERRAL CLAIMS — Pending (6 pending approval)

  #  │ Referrer          │ Referred Student │ Enrolled  │ 30-Day Mark │ Status
  ───┼───────────────────┼──────────────────┼───────────┼─────────────┼──────────────────
  1  │ Akhil Kumar (2401)│ Suresh Babu Rao  │ 30 Mar 26 │ 29 Apr 26   │ ⏳ Awaiting 30d
  2  │ Divya Sharma(2404)│ Meena Kapoor     │ 28 Mar 26 │ 27 Apr 26   │ ⏳ Awaiting 30d
  3  │ Ravi Singh (2403) │ Vikram Goud      │ 27 Mar 26 │ 26 Apr 26   │ ⏳ Awaiting 30d
  4  │ Anitha K.  (2408) │ Kavitha Devi     │ 25 Mar 26 │ 24 Apr 26   │ ⏳ Awaiting 30d
  5  │ Karthik M. (2405) │ Mohammed Tariq   │ 22 Mar 26 │ 21 Apr 26   │ ⏳ Awaiting 30d
  6  │ Rajesh K.  (2410) │ Renu Sharma      │ 20 Mar 26 │ 19 Apr 26   │ ✅ 30d passed → [Pay Now]

  CLAIM VALIDATION:
    Auto-check: Referral recorded at enquiry stage ✅
    Auto-check: Referred student active in batch (30+ days) — pending for 5
    Manual check: Bank details verified for Rajesh K. ✅

  [Process Payment — Rajesh Kumar: ₹ 1,000 to SBI A/C XXXXX7890]
```

---

## 3. Referral Settings

```
REFERRAL PROGRAM SETTINGS — Academic Year 2026–27

  Reward amount (referrer):    ₹ 1,000 per successful referral
  Discount (referred student): ₹ 500 off base course fee
  Minimum attendance to qualify: 30 days of classes attended
  Reward mode:                 (●) Bank transfer  ( ) Fee account credit
  Max referrals per student:   No cap
  Referral link tracking:      (●) Enabled — unique URL per student
  GSTIN of reward:             ₹ 1,000 referral reward — TDS applicable if total
                                rewards to a student exceed ₹5,000 in a financial year
                                (TDS @ 5% under Section 194H — commission)
  [Save Settings]   [Preview Referral Card (student-facing)]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/referrals/?month=2026-03` | All referrals and their status |
| 2 | `POST` | `/api/v1/coaching/{id}/referrals/` | Record a new referral claim |
| 3 | `POST` | `/api/v1/coaching/{id}/referrals/{rid}/approve/` | Approve referral reward payout |
| 4 | `GET` | `/api/v1/coaching/{id}/referrals/leaderboard/` | Top referrers |
| 5 | `GET` | `/api/v1/coaching/{id}/referrals/settings/` | Program configuration |

---

## 5. Business Rules

- The 30-day attendance condition prevents TCC from paying referral rewards for students who enroll and immediately drop out; the referral reward is earned when the referred student is a genuine, attending student — not merely enrolled on paper; the 30 days are measured from the batch start date (not enrollment date) to ensure the referred student is actively participating; if the referred student drops out on day 29, the referral reward is not paid — this is clearly disclosed in the referral program terms
- Referral rewards exceeding ₹5,000 in a financial year trigger TDS (Tax Deducted at Source) obligations under Section 194H of the Income Tax Act (commission to residents); TCC must deduct 5% TDS before paying; the student-referrer receives ₹950 instead of ₹1,000 for the fifth referral in the year (if the first four reached ₹4,000); the TDS certificate (Form 16A) is provided to the student within 15 days of deduction; many students are unaware of this provision — the counsellor should explain it proactively when onboarding high-volume referrers
- Referral claims submitted after enrollment (not at enquiry stage) are reviewed with higher scrutiny; a late claim ("I forgot to mention my friend referred me, please give me the discount/reward") requires the referring student to have demonstrably mentioned TCC to the enrolling student (a WhatsApp message, a shared YouTube video) — not just an assertion; the Branch Manager reviews late claims; a clear pattern of late claims from a single student is a fraud indicator and is logged
- Referral tracking via unique URLs allows TCC to attribute online leads (YouTube comment referrals, WhatsApp forwards) to specific students; the unique URL generates a lead in the CRM with the referrer's student ID pre-populated; this reduces manual referral claim disputes; students who share their referral link on social media or in coaching preparation communities generate passive referrals without active effort; this is encouraged as it amplifies TCC's reach
- The referral programme is the highest-quality lead source (61.9% conversion) and the lowest cost-per-acquisition (₹1,000 reward vs ₹500–₹2,000 for paid digital ads); TCC's marketing strategy should prioritise referral activation over paid acquisition; the Marketing team (L-01) is responsible for promoting the referral program through batch WhatsApp announcements, SMS campaigns, and batch coordinator reminders; the Admissions team is responsible for tracking and processing rewards

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division F*
