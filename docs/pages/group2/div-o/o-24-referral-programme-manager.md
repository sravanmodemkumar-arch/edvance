# O-24 — Referral Programme Manager

> **URL:** `/group/marketing/enrollment/referrals/`
> **File:** `o-24-referral-programme-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary operator

---

## 1. Purpose

The Referral Programme Manager tracks every parent, alumni, and staff referral that brings a new student enquiry, and manages the incentive rules, approval workflows, and payout lifecycle for those referrals. In Indian education groups, referral is the single highest-converting lead source — a referred lead converts at 30–40% versus 10–15% for newspaper ads and 6–10% for digital campaigns. The reason is trust: when a satisfied parent tells a neighbour "my child is doing well at Sunrise, you should also send your child there," that carries more weight than any full-page ad in Eenadu or Deccan Chronicle.

For a large group spending ₹2–10 Cr annually on marketing, referral incentives consume only 3–5% of the budget but generate 15–25% of total enrollments. The cost-per-admission (CPA) from referrals is typically ₹300–₹800 versus ₹2,500–₹6,500 for newspaper or digital. This makes referral the highest-ROI channel by a wide margin — but only if it's systematically tracked, incentivised, and paid out on time. Without a system:

The problems this page solves:

1. **Untracked referrals:** A parent tells the branch office "Meena aunty sent us," and the front desk nods but never records it. When Meena aunty asks about her referral discount 3 months later, nobody knows what she's talking about. This page creates a formal referral chain: referrer → referred student → lead record → enrollment confirmation → payout trigger.

2. **Incentive inconsistency:** Branch A offers ₹2,000 cash for a referral, Branch B offers ₹5,000 fee discount, Branch C gives nothing. Parents compare notes at school gates and complain about unfairness. This page enforces group-level referral incentive rules with standardised slabs, configurable by class/stream/branch but approved centrally.

3. **Payout delays and disputes:** A parent referred 3 families, all enrolled, and expects ₹15,000 in fee discount — but the finance team says "we don't have any record." This page tracks the complete payout lifecycle: referral logged → enrollment verified → incentive calculated → approval → payout (fee discount credit or cash transfer) → TDS deducted if applicable → receipt generated.

4. **TDS and GST compliance:** Under Indian Income Tax Act, cash referral payouts exceeding ₹20,000 in a financial year to a single person attract TDS at 10% (Section 194R for benefits, Section 194J for professional services). If the referrer is an agent or professional (e.g., education consultant, coaching centre owner), GST input applies. The system must track cumulative payouts per referrer per FY, auto-flag TDS thresholds, and generate Form 16A/26QS entries.

5. **Referrer segmentation:** A parent who referred 5 families is a "Super Referrer" and deserves VIP treatment — reserved seats at annual day, invitation to CEO meet, higher incentive slab. An alumni who refers batch-mates' children has a different motivation than a staff member. The system segments referrers by type (Parent / Alumni / Staff / Community Leader / Education Consultant / Other) and tracks lifetime referral value.

6. **Fraud prevention:** Branch staff sometimes create fake referrals to pocket cash incentives, or parents claim referral credit for students who were already in the pipeline. The system requires: (a) referral must be logged before or within 48 hours of lead creation, (b) referred student's lead record in O-15 must not pre-date the referral claim, (c) cash payouts require Campaign Manager or G4 approval, (d) staff self-referrals are flagged for review.

**Scale:** 500–5,000 referrals/season · 3–5% of marketing budget · ₹5L–₹50L total referral payouts · 200–2,000 unique referrers · TDS tracking for ₹20K+ payouts · integration with O-15 leads, O-09 budget, Division D finance

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — create/edit referral programmes, log referrals, approve payouts < ₹25,000, configure incentive rules | Primary operator |
| Group Topper Relations Manager | 120 | G3 | Read — view referrals from alumni channel for cross-referencing with ambassador programme | Alumni referral insights |
| Group Admission Telecaller Executive | 130 | G3 | Read + Log — log referral source during telecalling, view referrer details on assigned leads | Records referral at lead capture |
| Group Admission Data Analyst | 132 | G1 | Read + Export — referral analytics, ROI reports, referrer segmentation data | Reporting |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve referral programmes, approve cash payouts ≥ ₹25,000, set incentive caps | Financial authority |
| Group CFO / Finance Director | 30 | G1 | Read — payout exposure, TDS liability, budget utilisation | Financial oversight; triggers Division D payables |
| Branch Principal | — | G3 | Read (own branch) + Log referrals — log walk-in referrals, view own branch referral performance | Branch-level referral capture |
| Branch Counsellor | — | G3 | Read (own branch) — view referrer details during counselling to acknowledge referral | Builds referrer relationship |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Referral programme creation: 119 or G4+. Programme approval: G4/G5 only. Referral logging: 119, 130, Branch Principal. Payout approval: 119 (< ₹25K), G4/G5 (≥ ₹25K). TDS data visible to 119, 132, CFO (30), G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Enrollment Drives  ›  Referral Programme Manager
```

### 3.2 Page Header
```
Referral Programme Manager                            [+ Log Referral]  [Configure Programme]  [Export]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · 2 active programmes · 1,842 referrals · 684 enrolled (37.1% conversion) · ₹18.6L paid out
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Referrals | Integer | COUNT(referrals) WHERE season = current | Static blue | `#kpi-total` |
| 2 | Referral Conversion | Percentage | Enrolled referrals / Total referrals × 100 | Green ≥ 35%, Amber 20–35%, Red < 20% | `#kpi-conversion` |
| 3 | Active Referrers | Integer | COUNT(DISTINCT referrer_id) WHERE season = current AND has_referral = true | Static blue | `#kpi-referrers` |
| 4 | Total Payouts | ₹ Amount | SUM(payout_amount) WHERE season = current AND status = 'paid' | Amber if > 80% of budget, Green ≤ 80% | `#kpi-payouts` |
| 5 | Pending Payouts | ₹ Amount | SUM(payout_amount) WHERE status IN ('approved','pending_approval') | Red > ₹5L, Amber ₹1L–₹5L, Green < ₹1L | `#kpi-pending` |
| 6 | CPA (Referral) | ₹ Amount | Total payouts / Enrolled referrals | Green ≤ ₹800, Amber ₹800–₹1,500, Red > ₹1,500 | `#kpi-cpa` |

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Referral Log** — All referrals with status, referrer, referred student, payout
2. **Referrer Directory** — Unique referrers with lifetime stats and segmentation
3. **Programme Rules** — Active incentive programmes and slab configuration
4. **Payout Tracker** — Payout lifecycle, approvals, TDS, finance integration

### 5.2 Tab 1: Referral Log

**Filter bar:**

| Filter | Type | Options | Default |
|---|---|---|---|
| Season | Dropdown | 2024-25 / 2025-26 / 2026-27 | Current |
| Branch | Multi-select | All branches | All |
| Referrer Type | Multi-select | Parent / Alumni / Staff / Community Leader / Education Consultant / Other | All |
| Referral Status | Multi-select | Pending Verification / Verified / Enrolled / Payout Pending / Paid / Rejected / Expired | All |
| Programme | Dropdown | All programmes / specific programme | All |
| Date Range | Date picker | Custom range | Current season |

**Referral table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Referral ID | Text | Yes | Auto-generated (e.g., REF-2026-00142) |
| Referrer Name | Text (link) | Yes | Click → referrer detail drawer |
| Referrer Type | Badge | Yes | Parent / Alumni / Staff / Community / Consultant |
| Referred Student | Text (link) | Yes | Click → lead detail drawer (O-15) |
| Class Sought | Badge | Yes | Foundation / Jr Inter MPC / etc. |
| Branch | Text | Yes | Referred student's branch |
| Referral Date | Date | Yes | When referral was logged |
| Lead Status | Badge | Yes | Pipeline stage from O-15 (New → Enrolled / Lost) |
| Enrollment Status | Badge | Yes | Not Enrolled / Enrolled / Withdrawn |
| Incentive Type | Text | Yes | Fee Discount / Cash / Both |
| Payout Amount | ₹ Amount | Yes | Calculated from programme rules |
| Payout Status | Badge | Yes | Not Due / Pending Approval / Approved / Paid / TDS Deducted / Rejected |
| Actions | Buttons | No | [View] [Verify] [Process Payout] |

**Default sort:** Referral Date DESC
**Pagination:** Server-side · 25/page

### 5.3 Tab 2: Referrer Directory

**Referrer cards (grid) + table toggle:**

```
┌───────────────────────────────────────────┐
│  👤 Srinivas Reddy — Parent               │
│  S/o enrolled: Arjun R. (Class X, Hyd-1)  │
│  📱 +91 98765 43210                        │
│  Type: Parent · Since: 2024-25             │
│                                            │
│  Referrals: 7 total · 5 enrolled           │
│  ████████████████░░░ 71% conversion        │
│  Lifetime Payout: ₹35,000                  │
│  Tier: ⭐ Super Referrer                   │
│                                            │
│  [View Details] [Send Thank You] [Upgrade] │
└───────────────────────────────────────────┘
```

**Referrer table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Referrer Name | Text (link) | Yes | Click → referrer detail drawer |
| Type | Badge | Yes | Parent / Alumni / Staff / Community / Consultant |
| Phone | Text | Yes | Contact number |
| Relation to Group | Text | No | E.g., "Parent of Arjun (Class X, Kukatpally)" |
| Total Referrals | Integer | Yes | Lifetime count |
| Enrolled Referrals | Integer | Yes | Successfully enrolled |
| Conversion % | Percentage | Yes | Enrolled / Total |
| Total Payout (₹) | Amount | Yes | Lifetime payout |
| FY Payout (₹) | Amount | Yes | Current FY (for TDS tracking) |
| TDS Applicable | Badge | Yes | Yes (FY payout > ₹20K) / No |
| Tier | Badge | Yes | Standard / Silver (3+ enrolled) / Gold (5+ enrolled) / Super (10+ enrolled) |
| Last Referral | Date | Yes | Most recent referral date |
| Actions | Buttons | No | [View] [Send Thank You] [Invite to Event] |

### 5.4 Tab 3: Programme Rules

**Active programmes (card-based):**

```
┌───────────────────────────────────────────────────────────────┐
│  📋 Parent Referral Programme 2026-27                        │
│  Status: ✅ Active · Valid: 15 Nov 2025 → 30 Jun 2026       │
│  Type: Fee Discount for Referrer + Referred                   │
│                                                               │
│  Incentive Slabs:                                             │
│  ┌───────────────────────────────────────────────────┐       │
│  │ Class         │ Referrer Gets  │ Referred Gets    │       │
│  │ Foundation    │ ₹2,000 fee adj │ ₹1,000 fee adj  │       │
│  │ Jr Inter      │ ₹3,000 fee adj │ ₹2,000 fee adj  │       │
│  │ Sr Inter      │ ₹2,500 fee adj │ ₹1,500 fee adj  │       │
│  └───────────────────────────────────────────────────┘       │
│                                                               │
│  Conditions: Payout only on enrollment confirmed (fee paid)   │
│  Budget Cap: ₹25,00,000 · Used: ₹18,60,000 (74.4%)         │
│  ██████████████████████████████░░░░░░░░ 74%                  │
│                                                               │
│  [Edit] [Pause] [Clone for Next Season] [View Referrals]     │
└───────────────────────────────────────────────────────────────┘
```

**Programme configuration table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Programme Name | Text (link) | Yes | Click → programme detail |
| Season | Text | Yes | 2025-26, 2026-27, etc. |
| Referrer Types | Badges | No | Which referrer types are eligible |
| Incentive Model | Text | No | Fee Discount / Cash / Both |
| Referrer Incentive | Text | No | Summary (e.g., "₹2K–₹5K per class") |
| Referred Incentive | Text | No | Summary |
| Budget Cap | ₹ Amount | Yes | Max total programme spend |
| Utilisation | Percentage + bar | Yes | Budget used % |
| Total Referrals | Integer | Yes | Under this programme |
| Status | Badge | Yes | Draft / Pending Approval / Active / Paused / Expired |
| Actions | Buttons | No | [Edit] [Pause/Resume] [Clone] |

### 5.5 Tab 4: Payout Tracker

**Filter bar:** Payout Status · Referrer Type · Branch · Date Range · Amount Range · TDS Flag

**Payout table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Payout ID | Text | Yes | Auto-generated (e.g., PAY-REF-2026-00042) |
| Referrer Name | Text (link) | Yes | — |
| Referral ID | Text (link) | Yes | Links to referral record |
| Referred Student | Text | Yes | Student who enrolled |
| Branch | Text | Yes | Enrollment branch |
| Incentive Type | Badge | Yes | Fee Discount / Cash |
| Gross Amount | ₹ Amount | Yes | Before TDS |
| TDS (₹) | ₹ Amount | Yes | 10% if FY cumulative > ₹20,000 |
| Net Amount | ₹ Amount | Yes | Gross − TDS |
| Status | Badge | Yes | Pending Verification / Pending Approval / Approved / Sent to Finance / Paid / Rejected |
| Approval | Text | No | Approver name + date |
| Payment Date | Date | Yes | When paid (fee adjustment date or cash transfer date) |
| Payment Mode | Badge | Yes | Fee Adjustment / Bank Transfer / Cheque / UPI |
| Actions | Buttons | No | [Approve] [Reject] [View Receipt] |

**TDS summary panel (above table):**

```
TDS Summary — FY 2025-26
Total Cash Payouts: ₹32,40,000 · Referrers Above ₹20K: 42 · Total TDS Deducted: ₹1,24,000
TDS Due (Pending Deposit): ₹18,600 · Next TDS Deposit Deadline: 7 Apr 2026
[Generate TDS Certificate] [Download 26QS Data]
```

---

## 6. Drawers & Modals

### 6.1 Modal: `log-referral` (560px)

- **Title:** "Log New Referral"
- **Fields:**
  - Referrer search (phone or name — auto-complete against existing referrer directory)
  - If new referrer:
    - Referrer name (text, required)
    - Referrer phone (tel, required — +91, 10 digits)
    - Referrer type (dropdown, required): Parent / Alumni / Staff / Community Leader / Education Consultant / Other
    - Relation to group (text — e.g., "Parent of Arjun, Class X, Kukatpally branch")
    - PAN number (text, optional — required for cash payouts > ₹20,000/FY; format validated ABCDE1234F)
    - Bank account details (optional — for cash payouts: account number, IFSC, bank name)
  - Referred student name (text, required)
  - Referred parent name (text, required)
  - Referred phone (tel, required)
  - Class/stream sought (dropdown, required)
  - Preferred branch (dropdown)
  - Link to existing lead (auto-search by phone — if lead exists in O-15, link automatically)
  - Referral programme (dropdown — select applicable programme)
  - How was referral communicated? (dropdown): Word of Mouth / Referral Card / WhatsApp Share / Online Form / Staff Recommendation / Other
  - Notes (textarea)
- **Validation:**
  - Referred student phone checked against O-15 pipeline: if lead exists and was created > 48 hours before referral date → warning: "Lead pre-dates referral — verify authenticity"
  - Referrer phone ≠ referred phone (self-referral block)
  - If referrer type = Staff → flag for Campaign Manager review (staff incentive conflict of interest)
  - Duplicate referral check: same referrer + same referred phone → block
- **Buttons:** Cancel · Save Referral · Save & Create Lead (if no lead exists in O-15)
- **Access:** Role 119, 130, Branch Principal

### 6.2 Modal: `configure-programme` (640px)

- **Title:** "Configure Referral Programme"
- **Fields:**
  - Programme name (text, required — e.g., "Parent Referral Programme 2026-27")
  - Season (dropdown, required)
  - Eligible referrer types (multi-select): Parent / Alumni / Staff / Community Leader / Education Consultant / All
  - Eligible branches (multi-select): All / Specific branches
  - Eligible classes (multi-select): All / Specific classes
  - Incentive model:
    - **Referrer incentive:**
      - Type (radio): Fee Discount / Cash Payout / Both
      - Slab configuration (repeatable rows):
        - Class/Stream (dropdown)
        - Amount (₹) or Percentage (%)
        - Cap per referral (₹)
      - Tiered bonus (optional):
        - 3rd enrolled referral in season: +₹X bonus
        - 5th enrolled referral: +₹X bonus
        - 10th enrolled referral: +₹X bonus
    - **Referred student incentive:**
      - Type (radio): Fee Discount / Application Fee Waiver / None
      - Amount (₹) or Percentage (%)
  - Payout trigger (dropdown, required):
    - On lead verified (risky — student may not enroll)
    - On enrollment confirmed (fee paid) — **recommended**
    - On completion of first term (safest but slowest)
  - Validity: Start date → End date
  - Budget cap (₹, required — links to O-09 budget line "Referral Incentives")
  - Max referrals per referrer per season (integer, optional — fraud cap)
  - Approval required per payout? (toggle — if yes, each payout needs 119/G4 approval)
  - Auto-approve threshold (₹ — payouts below this amount auto-approve; above requires manual)
  - TDS auto-deduction (toggle — default ON for cash payouts)
  - Internal notes (textarea)
- **Buttons:** Cancel · Save as Draft · Submit for Approval
- **Approval flow:** Draft → Pending Approval (G4/G5 reviews) → Active
- **Access:** Role 119 (create), G4/G5 (approve)

### 6.3 Drawer: `referral-detail` (720px, right-slide)

- **Tabs:** Overview · Referral Chain · Payout History · Communications
- **Overview tab:**
  - Referral ID, date, programme, status
  - Referrer: name, phone, type, tier, lifetime referrals
  - Referred student: name, parent, phone, class, branch
  - Lead link: direct link to O-15 lead record with current pipeline stage
  - Enrollment status: Not Enrolled / Enrolled (date) / Withdrawn (date + reason)
  - Incentive: referrer amount + referred student amount
  - Payout status: timeline (Logged → Verified → Enrollment Confirmed → Payout Approved → Paid)
- **Referral Chain tab:**
  - If referred student's parent later refers others → show the chain:
    - Referrer A → Student B enrolled → Parent B refers → Student C enrolled → ...
  - Chain depth (1st generation, 2nd generation, etc.)
  - Total enrollments in chain
- **Payout History tab:**
  - All payout events for this referral: approval, TDS deduction, payment, receipt
  - Payment proof: transaction ID, bank reference, fee adjustment receipt
- **Communications tab:**
  - WhatsApp/SMS sent to referrer (thank you, payout confirmation, TDS certificate)
  - Referral card generated (if any)
  - Event invitations sent
- **Footer:** [Verify] [Process Payout] [Send Thank You] [Reject (with reason)] [Flag Fraud]

### 6.4 Drawer: `referrer-profile` (720px, right-slide)

- **Tabs:** Profile · Referral History · Payouts · Engagement
- **Profile tab:**
  - Name, phone, email, type, PAN, bank details (masked)
  - Relation to group, since when
  - Tier: Standard / Silver / Gold / Super + progress to next tier
  - Lifetime stats: total referrals, enrolled, conversion %, total payout
  - FY stats: current FY referrals, FY payout, TDS applicable?
- **Referral History tab:**
  - Table of all referrals by this person: student name, date, status, amount
  - Season-wise breakdown
- **Payouts tab:**
  - Complete payout history with TDS details
  - FY-wise cumulative: FY 2024-25: ₹X, FY 2025-26: ₹Y
  - TDS certificates issued
  - [Generate TDS Certificate for FY] button
- **Engagement tab:**
  - Events invited to (Open Day, Annual Day, CEO Meet)
  - Thank-you messages sent
  - Referral card distributed? (date, quantity)
  - Net Promoter Score (if surveyed)
- **Footer:** [Edit Profile] [Send Referral Card] [Invite to Event] [Upgrade Tier] [Deactivate]

### 6.5 Modal: `approve-payout` (480px)

- **Title:** "Approve Referral Payout — [Referrer Name]"
- **Content:**
  - Referral summary: referrer → referred student → enrollment date
  - Programme: [Name]
  - Gross amount: ₹X
  - FY cumulative for this referrer: ₹Y (highlighted if > ₹20,000)
  - TDS applicable: Yes/No · TDS amount: ₹Z
  - Net payout: ₹X − ₹Z = ₹W
  - Payment mode: Fee Adjustment / Bank Transfer / Cheque / UPI
  - If bank transfer: bank details preview (masked account number)
- **Actions:** Approve / Approve with Modification (adjust amount) / Reject (with reason)
- **Access:** 119 (< ₹25K), G4/G5 (≥ ₹25K)

### 6.6 Modal: `bulk-payout` (560px)

- **Title:** "Bulk Payout Processing — [N] referrals"
- **Content:**
  - List of referrals ready for payout (enrollment confirmed, incentive calculated)
  - Total gross: ₹X · Total TDS: ₹Y · Total net: ₹Z
  - Payment mode: Fee Adjustment (applied to next fee cycle) / Bank Transfer (batch NEFT/IMPS)
  - Approval: auto-approved if each < threshold; flagged items listed separately
- **Buttons:** Cancel · Process All · Process Selected
- **Access:** Role 119 or G4+

### 6.7 Modal: `fraud-review` (480px)

- **Title:** "Fraud Review — Referral [ID]"
- **Flags raised:**
  - Lead pre-dates referral by > 48 hours
  - Referrer is staff member (conflict of interest)
  - Same referrer submitted > [N] referrals in [period] (velocity check)
  - Referrer and referred share same address/phone prefix
  - Referred student enrolled and withdrew within 30 days (hit-and-run)
- **Actions:** Clear (referral is legitimate) / Reject (with reason) / Escalate to G4
- **Access:** Role 119 or G4+

---

## 7. Charts

### 7.1 Referral Conversion Funnel (Funnel)

| Property | Value |
|---|---|
| Chart type | Funnel (custom CSS/Chart.js plugin) |
| Title | "Referral Pipeline — Season [Year]" |
| Data | Stages: Referral Logged → Lead Created → Contacted → Interested → Walk-in → Counselled → Enrolled |
| Colour | Grey → Blue → Purple → Amber → Green → Emerald (progressive) |
| Tooltip | "[Stage]: [N] referrals ([X]% of total)" |
| API | `GET /api/v1/group/{id}/marketing/enrollment/referrals/analytics/funnel/` |

### 7.2 Referrals by Type (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Referrals by Referrer Type" |
| Data | COUNT(referrals) per referrer type |
| Segments | Parent (blue) · Alumni (purple) · Staff (amber) · Community (green) · Consultant (pink) · Other (grey) |
| Centre text | Total: [N] referrals |
| API | `GET /api/v1/group/{id}/marketing/enrollment/referrals/analytics/by-type/` |

### 7.3 Monthly Referrals & Payouts (Combo Bar + Line)

| Property | Value |
|---|---|
| Chart type | Combo — bar (referrals) + line (payouts ₹) |
| Title | "Monthly Referrals vs Payouts — Season [Year]" |
| Bars | Monthly referral count (stacked by status: enrolled/pending/lost) |
| Line | Monthly payout amount (₹) |
| X-axis | Month (Nov → Jun) |
| Y-axis left | Count |
| Y-axis right | ₹ Amount |
| API | `GET /api/v1/group/{id}/marketing/enrollment/referrals/analytics/monthly-trend/` |

### 7.4 Top Referrers Leaderboard (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Top 15 Referrers — Enrolled Referrals" |
| Data | Top 15 referrers by enrolled referral count |
| Colour | Tier-coded: Super (gold) · Gold (amber) · Silver (blue) · Standard (grey) |
| Label | Referrer name + count + total payout |
| API | `GET /api/v1/group/{id}/marketing/enrollment/referrals/analytics/top-referrers/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Referral logged | "Referral logged — [Referrer] → [Student] (REF-[ID])" | Success | 3s |
| Referral verified | "Referral REF-[ID] verified — payout will trigger on enrollment" | Success | 3s |
| Payout approved | "Payout of ₹[X] approved for [Referrer]" | Success | 3s |
| Payout processed | "₹[X] paid to [Referrer] via [Mode] — Receipt: [No]" | Success | 4s |
| Bulk payout processed | "[N] payouts processed — total ₹[X]" | Success | 4s |
| TDS deducted | "TDS of ₹[X] (10%) deducted — net payout ₹[Y] for [Referrer]" | Info | 4s |
| TDS threshold alert | "⚠️ [Referrer] FY payout crossed ₹20,000 — TDS now applicable on future payouts" | Warning | 6s |
| Programme created | "Referral programme '[Name]' created — pending approval" | Success | 3s |
| Programme approved | "Referral programme '[Name]' approved — now active" | Success | 4s |
| Fraud flagged | "⚠️ Referral REF-[ID] flagged for review — [Reason]" | Warning | 5s |
| Referral rejected | "Referral REF-[ID] rejected: [Reason]" | Warning | 4s |
| Budget cap warning | "Referral programme '[Name]' at [X]% of budget cap — ₹[Y] remaining" | Warning | 5s |
| Duplicate referral | "Duplicate: [Referrer] already referred [Student] — blocked" | Error | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No referral programmes | 📋 | "No Referral Programmes" | "Create your first referral programme to incentivise parent, alumni, and staff referrals." | Configure Programme |
| No referrals logged | 🤝 | "No Referrals Yet" | "Referrals will appear here as they are logged by telecallers, branches, or the online form." | Log Referral |
| No referrers | 👥 | "No Referrers in Directory" | "The referrer directory populates automatically when referrals are logged." | — |
| No payouts pending | ✅ | "All Payouts Processed" | "No referral payouts are pending — all approved payouts have been processed." | — |
| No data for analytics | 📊 | "Insufficient Referral Data" | "Charts require at least 10 referrals to display meaningful analytics." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + tab bar placeholder + table skeleton (10 rows) |
| Tab switch | Content area skeleton |
| Referral detail drawer | 720px skeleton: overview header + 4 tabs |
| Referrer profile drawer | 720px skeleton: profile header + stats + referral list |
| Programme cards | 2-column card grid shimmer |
| Payout table | Table skeleton with TDS summary panel placeholder |
| Chart load | Grey canvas placeholder per chart |
| Bulk payout modal | List skeleton + totals placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/` | G1+ | List all referrals (filterable, paginated) |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/{ref_id}/` | G1+ | Referral detail |
| POST | `/api/v1/group/{id}/marketing/enrollment/referrals/` | G3+ | Log new referral |
| PUT | `/api/v1/group/{id}/marketing/enrollment/referrals/{ref_id}/` | G3+ | Update referral |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/referrals/{ref_id}/verify/` | G3+ | Verify referral |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/referrals/{ref_id}/reject/` | G3+ | Reject referral |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/referrals/{ref_id}/flag/` | G3+ | Flag for fraud review |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/referrers/` | G1+ | Referrer directory |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/referrers/{referrer_id}/` | G1+ | Referrer profile |
| PUT | `/api/v1/group/{id}/marketing/enrollment/referrals/referrers/{referrer_id}/` | G3+ | Update referrer profile |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/programmes/` | G1+ | List programmes |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/programmes/{prog_id}/` | G1+ | Programme detail |
| POST | `/api/v1/group/{id}/marketing/enrollment/referrals/programmes/` | G3+ | Create programme |
| PUT | `/api/v1/group/{id}/marketing/enrollment/referrals/programmes/{prog_id}/` | G3+ | Update programme |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/referrals/programmes/{prog_id}/status/` | G3+ | Activate/pause programme |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/referrals/programmes/{prog_id}/approve/` | G4+ | Approve/reject programme |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/payouts/` | G1+ | List payouts |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/referrals/payouts/{pay_id}/approve/` | G3+ | Approve payout (119 < ₹25K, G4+ ≥ ₹25K) |
| POST | `/api/v1/group/{id}/marketing/enrollment/referrals/payouts/bulk/` | G3+ | Bulk payout processing |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/payouts/tds-summary/` | G1+ | TDS summary for FY |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/payouts/{pay_id}/receipt/` | G1+ | Payout receipt |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/analytics/funnel/` | G1+ | Referral funnel chart |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/analytics/by-type/` | G1+ | Referrer type donut |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/analytics/monthly-trend/` | G1+ | Monthly trend combo |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/analytics/top-referrers/` | G1+ | Top referrers bar |
| GET | `/api/v1/group/{id}/marketing/enrollment/referrals/export/` | G1+ | Export referral data |

### Integration Endpoints

| Direction | System | Endpoint | Purpose |
|---|---|---|---|
| Inbound | O-15 Lead Pipeline | `GET /api/v1/group/{id}/marketing/leads/pipeline/?source=referral` | Auto-link referral to lead when source = Referral |
| Inbound | O-15 Stage Change | Webhook on lead stage = 'enrolled' | Trigger payout eligibility when referred student enrolls |
| Outbound | Division D (Finance) | `POST /api/v1/group/{id}/finance/payables/` | Push approved cash payouts to vendor/payable ledger |
| Outbound | Division D (Finance) | `POST /api/v1/group/{id}/finance/fee-adjustments/` | Push fee discount adjustments for referrer's child |
| Outbound | Division D (Finance) | `GET /api/v1/group/{id}/finance/tds/26qs/` | Fetch TDS deposit status for reconciliation |
| Inbound | O-09 Budget Manager | `GET /api/v1/group/{id}/marketing/campaigns/budget/lines/?channel=referral` | Check referral budget utilisation |
| Outbound | O-12 WhatsApp | `POST /api/v1/group/{id}/marketing/whatsapp/send/` | Send referral thank-you, payout confirmation, TDS certificate |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../referrals/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#referrals-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Dropdown change | `hx-get` with filter params | `#referrals-content` | `innerHTML` | `hx-trigger="change"` |
| Referral detail drawer | Row click | `hx-get=".../referrals/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Referrer profile drawer | Referrer name click | `hx-get=".../referrals/referrers/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Log referral | Form submit | `hx-post=".../referrals/"` | `#log-result` | `innerHTML` | Dedup check inline; Toast |
| Verify referral | Verify button | `hx-patch=".../referrals/{id}/verify/"` | `#status-badge-{id}` | `innerHTML` | Inline badge update |
| Approve payout | Approve form | `hx-patch=".../referrals/payouts/{id}/approve/"` | `#payout-status-{id}` | `innerHTML` | Toast + row refresh |
| Bulk payout | Bulk form | `hx-post=".../referrals/payouts/bulk/"` | `#bulk-result` | `innerHTML` | Progress bar + toast |
| Programme create | Form submit | `hx-post=".../referrals/programmes/"` | `#programme-result` | `innerHTML` | Toast + card refresh |
| Programme status | Status button | `hx-patch=".../referrals/programmes/{id}/status/"` | `#prog-status-{id}` | `innerHTML` | Inline update |
| Flag fraud | Flag button | `hx-patch=".../referrals/{id}/flag/"` | `#fraud-result` | `innerHTML` | Toast + badge update |
| Chart load | Per chart | `hx-get=".../referrals/analytics/..."` | `#chart-{name}` | `innerHTML` | Lazy-load |
| Table pagination | Page controls | `hx-get` with `?page={n}` | `#referral-table-body` | `innerHTML` | 25/page |
| Phone search (referrer) | Input keyup | `hx-get=".../referrals/referrers/?phone={input}"` | `#referrer-search-results` | `innerHTML` | `hx-trigger="keyup changed delay:500ms"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
