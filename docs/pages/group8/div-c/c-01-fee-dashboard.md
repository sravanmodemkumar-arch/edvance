# C-01 — Fee Dashboard

> **URL:** `/parent/fees/dashboard/`
> **File:** `c-01-fee-dashboard.md`
> **Priority:** P1
> **Roles:** Parent (view) · Institution Accounts Office (publish fee structure) · EduForge Finance (platform fee reconciliation)

---

## 1. Consolidated Fee Overview — All Children

```
FEE DASHBOARD — Mrs. Lakshmi Devi
Academic Year: 2025–26

  ── CONSOLIDATED SUMMARY ────────────────────────────────────────────────
  Total Annual Fees (all children):                         Rs. 3,12,588
  Paid to Date:                                             Rs. 1,72,500
  Pending:                                                  Rs. 1,40,088
  Next Due:  Rs. 60,000 (Ravi — GCEH 2nd instalment)       Due: 15 Jan 2026

  ── CHILD-WISE BREAKDOWN ────────────────────────────────────────────────

  [1] RAVI KUMAR — B.Tech CSE 3rd Year, GCEH Hyderabad
      Fee Type           Annual      Paid       Pending    Due Date
      ─────────────────  ─────────   ─────────  ─────────  ──────────
      Tuition Fee        85,000      42,500     42,500     15 Jan 2026
      Special Fee        15,000       7,500      7,500     15 Jan 2026
      Lab Fee            10,000      10,000          0     — Paid —
      Exam Fee           10,000           0     10,000     15 Jan 2026
      ─────────────────  ─────────   ─────────  ─────────
      COLLEGE TOTAL    1,20,000      60,000     60,000

      Hostel Fee         80,000      40,000     40,000     15 Jan 2026
      ─────────────────  ─────────   ─────────  ─────────
      RAVI TOTAL       2,00,000    1,00,000   1,00,000

      Payment Schedule: 2 instalments (July + January)
      1st instalment (Jul 2025): Rs. 1,00,000   ✅ Paid 08 Jul 2025
      2nd instalment (Jan 2026): Rs. 1,00,000   ⏳ Due 15 Jan 2026

  [2] PRIYA KUMAR — Class 11 MPC, Sri Chaitanya Vijayawada
      Fee Type           Annual      Paid       Pending    Due Date
      ─────────────────  ─────────   ─────────  ─────────  ──────────
      Tuition Fee        85,000      42,500     42,500     (Q3+Q4)
      Bus Transport      24,000      12,000     12,000     (Q3+Q4)
      ─────────────────  ─────────   ─────────  ─────────
      PRIYA TOTAL      1,09,000      54,500     54,500

      Payment Schedule: 4 quarterly instalments
      Q1 (Jun 2025): Rs. 27,250   ✅ Paid 04 Jun 2025
      Q2 (Sep 2025): Rs. 27,250   ✅ Paid 01 Sep 2025
      Q3 (Dec 2025): Rs. 27,250   ⏳ Due 15 Dec 2025
      Q4 (Mar 2026): Rs. 27,250   ○  Upcoming

  [3] RAVI KUMAR — TopRank Academy (Coaching Subscription)
      Plan               Monthly     Paid       Pending    Next Debit
      ─────────────────  ─────────   ─────────  ─────────  ──────────
      Standard Plan         299      18,000*        0      01 Jan 2026
      (* Rs. 299 x 6 months auto-debited Jun–Nov 2025)
      ─────────────────  ─────────   ─────────  ─────────
      COACHING TOTAL       3,588      1,794      1,794     (remaining months)

      Auto-debit: ✅ Active — SBI UPI (lakshmi.devi@sbi)
      Next debit: Rs. 299 on 01 Jan 2026
```

---

## 2. Overdue Alerts & Reminders

```
OVERDUE & UPCOMING — Mrs. Lakshmi Devi

  ── OVERDUE ──────────────────────────────────────────────────────────────
  (No overdue items currently)

  ── DUE WITHIN 30 DAYS ──────────────────────────────────────────────────
  15 Dec 2025  Priya — Sri Chaitanya Q3 instalment         Rs. 27,250
               [Pay Now]  [Set Reminder]

  01 Jan 2026  Ravi — TopRank auto-debit                   Rs.    299
               Auto-debit active — no action needed

  15 Jan 2026  Ravi — GCEH 2nd instalment                  Rs. 1,00,000
               [Pay Now]  [Pay in Parts]  [Set Reminder]

  ── LATE FEE SIMULATION ─────────────────────────────────────────────────
  If GCEH 2nd instalment is paid after 15 Jan 2026:
    16 Jan – 15 Feb:  +Rs. 1,200 (1.2% late fee per month as per GCEH policy)
    16 Feb – 15 Mar:  +Rs. 2,400 (cumulative)
    After 15 Mar:     Exam hall ticket may be withheld — contact accounts office

  ── NOTIFICATION SETTINGS ────────────────────────────────────────────────
  Remind me via:  [x] SMS   [x] WhatsApp   [x] App Push   [ ] Email
  Remind before:  (o) 7 days  ( ) 15 days  ( ) 30 days
  Overdue alert:  Daily until paid
```

---

## 3. Year-on-Year Fee Comparison

```
ANNUAL FEE TREND — All Children Combined

  Academic Year    Total Fees    Change
  ─────────────    ──────────    ──────
  2023–24          2,65,000      —
  2024–25          2,88,000      +8.7%
  2025–26          3,12,588      +8.5%

  Note: 2025–26 increase due to Ravi's hostel fee revision (+Rs. 5,000)
        and Sri Chaitanya bus route change (+Rs. 4,000)

  [Download Full Fee History (PDF)]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/parent/fees/dashboard/` | Consolidated fee summary for all linked children |
| 2 | `GET` | `/api/v1/parent/fees/dashboard/{child_id}/` | Detailed fee breakdown for a specific child |
| 3 | `GET` | `/api/v1/parent/fees/dashboard/{child_id}/instalments/` | Instalment schedule with payment status |
| 4 | `GET` | `/api/v1/parent/fees/overdue/` | Overdue and upcoming due items across all children |
| 5 | `GET` | `/api/v1/parent/fees/trend/` | Year-on-year fee comparison data |
| 6 | `PATCH` | `/api/v1/parent/fees/notifications/` | Update reminder preferences (channels, timing) |

---

## 5. Business Rules

- The consolidated fee dashboard aggregates fee data from multiple institution types — colleges (GCEH), schools (Sri Chaitanya), and coaching platforms (TopRank) — each of which uses a different fee structure and payment cadence; the platform normalises these into a unified view by pulling fee-head-level data from each institution's accounts module via EduForge's inter-tenant API, converting all amounts to annual equivalents for the summary row while preserving the original instalment schedule per child; the parent never needs to log into three separate portals to understand their total educational expenditure, which for a family like Mrs. Lakshmi Devi amounts to Rs. 3,12,588 across three institutions in a single academic year.

- Overdue fee alerts must respect each institution's specific late fee policy, which varies significantly across institution types; GCEH charges 1.2% per month on overdue college fees with a hard consequence of withholding exam hall tickets after 60 days, Sri Chaitanya charges 1.5% per month on school fees with transport suspension after 45 days of non-payment, and TopRank's coaching subscription simply lapses if the auto-debit fails for two consecutive months; the dashboard displays the late fee simulation proactively so parents can see the financial impact of delayed payment before the due date arrives, and the system never applies late fees on its own — it only displays what the institution's policy will impose.

- Fee data freshness is critical because institutions may revise fee structures mid-year (hostel fee hikes, transport route changes, government fee regulation orders); the dashboard pulls from the institution's canonical fee ledger in near-real-time with a cache TTL of no more than 15 minutes; if the institution's accounts office updates a fee head (for example, GCEH revising hostel fees from Rs. 75,000 to Rs. 80,000 following a governing body resolution), the parent dashboard reflects the change within 15 minutes and a push notification is sent explaining the revision with a link to the institution's official circular if uploaded.

- The notification engine for fee reminders must handle the parent's preference for communication channel (SMS, WhatsApp, app push, email) and timing (7, 15, or 30 days before due date), but it must also respect the institution's communication policies; some institutions (particularly schools like Sri Chaitanya) send their own fee reminders via their parent communication system, so EduForge's reminders are marked as "supplementary" and the parent can disable EduForge reminders per institution if the institution's own reminders are sufficient; the system deduplicates by checking if the institution has sent a fee reminder within the last 48 hours before sending EduForge's own reminder.

---

*Last updated: 2026-03-31 · Group 8 — Parents Portal · Division C*
