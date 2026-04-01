# O-23 — Admission Offer Campaigns

> **URL:** `/group/marketing/enrollment/offers/`
> **File:** `o-23-admission-offer-campaigns.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary operator

---

## 1. Purpose

The Admission Offer Campaigns page manages all fee discounts, early-bird offers, sibling concessions, scholarship-linked waivers, and promotional incentives used to accelerate enrollment. In Indian education, fee discounting is an art — offer too little and parents go to competitors; offer too much and margins collapse. Large groups run 5–15 different offer types simultaneously during admission season, each with eligibility criteria, validity windows, approval workflows, and financial impact tracking.

The problems this page solves:

1. **Offer proliferation control:** Without a central system, branches create ad-hoc offers — "principal's special discount," "last-day offer," "community-specific concession" — that aren't tracked and erode revenue unpredictably. This page mandates: every offer must be approved by G4/G5 before use.

2. **Financial impact visibility:** Each offer has a revenue impact. "10% early-bird discount for first 500 applicants" across 30 branches means ₹50L–₹2Cr in revenue reduction. The CFO needs real-time visibility into total discount exposure.

3. **Eligibility enforcement:** Offers have specific eligibility rules: "Only for students scoring ≥ 90% in previous board exam" or "Only for siblings of existing students." The system validates eligibility at the time of fee payment and blocks ineligible claims.

4. **Time-bound management:** Early-bird offers expire on a date. Flash sale offers last 48 hours. The system auto-activates and auto-deactivates offers based on configured date ranges.

**Scale:** 5–15 offer types/season · 500–10,000 students claiming offers · ₹50L–₹5Cr total discount value per season · real-time tracking across 5–50 branches

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — create, edit, activate offers | Primary operator |
| Group Admission Data Analyst | 132 | G1 | Read — offer analytics, financial impact | Reporting |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve new offers, set discount caps | Financial authority |
| Group CFO / Finance Director | 30 | G1 | Read — discount exposure, revenue impact | Financial oversight |
| Branch Principal | — | G3 | Read (own branch) + Apply offers to applicants | Applies approved offers at branch level |
| Branch Counsellor | — | G3 | Read — see available offers during counselling | Communicates offers to parents |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Offer creation: 119 or G4+. Offer approval: G4/G5 only. Offer application at branch: Branch Principal or 119.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Enrollment Drives  ›  Admission Offer Campaigns
```

### 3.2 Page Header
```
Admission Offer Campaigns                            [+ Create Offer]  [Offer Calculator]  [Export]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · 8 active offers · 2,840 claims · ₹1.42 Cr total discount given
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Offers | Integer | COUNT(offers) WHERE status = 'active' AND today BETWEEN start_date AND end_date | Static blue | `#kpi-active` |
| 2 | Total Claims | Integer | COUNT(offer_claims) WHERE season = current | Static blue | `#kpi-claims` |
| 3 | Total Discount Given | ₹ Amount | SUM(discount_amount) across all claims | Amber if > budget, Green ≤ budget | `#kpi-discount` |
| 4 | Avg Discount per Student | ₹ Amount | Total discount / claims | Static blue | `#kpi-avg-discount` |
| 5 | Revenue Impact | ₹ Amount | Total discount as % of gross fee revenue | Red > 15%, Amber 10–15%, Green < 10% | `#kpi-revenue-impact` |
| 6 | Pending Approval | Integer | COUNT(offers) WHERE status = 'pending_approval' | Red > 3, Amber 1–3, Green = 0 | `#kpi-pending` |

---

## 5. Sections

### 5.1 Tab Navigation

Three tabs:
1. **Active Offers** — Currently running offers with claims and impact
2. **Offer History** — Past season offers for reference
3. **Financial Impact** — Revenue impact analytics

### 5.2 Tab 1: Active Offers

**Card-based grid (2 columns):**

```
┌───────────────────────────────────────────┐
│  🏷️ Early Bird Discount — 10% off        │
│  Status: ✅ Active                         │
│  Valid: 15 Nov 2025 → 31 Jan 2026         │
│  Branches: All · Classes: All              │
│  Eligibility: Apply before deadline        │
│                                            │
│  Claims: 1,240 / 2,000 cap                │
│  ████████████░░░░░ 62%                     │
│  Total Discount: ₹62,40,000               │
│  Enrollments via offer: 1,080 (87%)       │
│                                            │
│  [View Details] [Pause] [Edit] [Extend]   │
└───────────────────────────────────────────┘
```

**Also shown as table (toggle view):**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Offer Name | Text (link) | Yes | — |
| Type | Badge | Yes | Early Bird / Sibling / Scholarship / Merit / Loyalty / Flash / Referral / Custom |
| Discount | Text | Yes | "10% off" or "₹5,000 flat" or "Full tuition waiver" |
| Valid Period | Date range | Yes | Start → End |
| Branches | Text | Yes | All or specific |
| Eligibility | Text | No | Short description |
| Claims | Integer + cap | Yes | N / cap (progress bar) |
| Total Discount (₹) | Amount | Yes | Sum of all discounts applied |
| Enrollment Impact | Integer | Yes | Students who enrolled with this offer |
| Status | Badge | Yes | Draft / Pending / Active / Paused / Expired / Exhausted |
| Actions | Buttons | No | [View] [Pause] [Extend] [Clone] |

### 5.3 Tab 2: Offer History

Same table as Tab 1 but for previous seasons, with final outcome metrics.

### 5.4 Tab 3: Financial Impact

Charts and tables showing total discount exposure (see §7).

---

## 6. Drawers & Modals

### 6.1 Modal: `create-offer` (640px)

- **Title:** "Create Admission Offer"
- **Fields:**
  - Offer name (text, required — e.g., "Early Bird 2026-27 — 10% Off")
  - Offer type (dropdown, required):
    - **Early Bird** — Discount for applications before a deadline
    - **Sibling Discount** — Discount for siblings of existing students
    - **Merit/Scholarship** — Based on academic performance or entrance exam score
    - **Loyalty** — Returning students / re-admission
    - **Referral Reward** — Discount for referred students (linked to O-24)
    - **Flash Sale** — Limited-time (24–72 hour) urgency offer
    - **Community/Category** — SC/ST/OBC/EWS concession
    - **Custom** — Any other offer
  - Discount structure:
    - Discount type (radio): Percentage / Flat Amount / Fee Component Waiver
    - If Percentage: X% off (slider 1–100%)
    - If Flat: ₹X off total fee
    - If Component Waiver: Select fee components to waive (Admission Fee / First Term / Transport / Hostel / Activity Fee)
    - Max discount amount (₹, optional — cap even for percentage)
  - Eligibility criteria:
    - Branches (multi-select): All / Specific branches
    - Classes (multi-select): All / Specific classes
    - Streams (multi-select): All / Specific streams
    - Academic requirement (optional): Previous score ≥ X% / Entrance exam rank ≤ Y
    - Category (optional): General / SC / ST / OBC / EWS
    - Sibling enrolled? (toggle — for sibling discount)
    - New student only / Returning student / Both
  - Validity:
    - Start date (date, required)
    - End date (date, required)
    - Claim cap (integer, optional — max N students can claim this offer)
  - Stackable? (toggle — can this combine with other offers?)
  - Approval required per claim? (toggle — if yes, branch must get G4 approval per student)
  - Budget cap (₹, optional — max total discount spend)
  - Internal notes (textarea)
- **Buttons:** Cancel · Save as Draft · Submit for Approval
- **Validation:**
  - End date > Start date
  - Discount percentage ≤ group-level max cap (default 50%, configurable by G5)
  - Budget cap validation against O-09 budget lines
- **Access:** Role 119 or G4+
- **Approval flow:** Draft → Pending Approval (G4/G5 reviews) → Active

### 6.2 Modal: `offer-calculator` (560px)

- **Title:** "Offer Impact Calculator"
- **Purpose:** Simulate financial impact of a proposed offer before creating it
- **Fields:**
  - Discount: X% or ₹X
  - Estimated claims: N students
  - Average fee per student: ₹X (auto-filled from current fee structure)
  - Applicable branches (affects student count estimate)
- **Output:**
  - Total gross revenue (without discount): ₹X
  - Total discount exposure: ₹Y
  - Net revenue: ₹X − ₹Y
  - Discount as % of gross: Z%
  - Break-even: Need X additional enrollments at full fee to compensate
- **Buttons:** Close · Create Offer with These Parameters
- **Access:** Role 119, 132, G4+

### 6.3 Drawer: `offer-detail` (720px, right-slide)

- **Tabs:** Overview · Claims · Branch Breakdown · Financial · History
- **Overview tab:** All offer details, eligibility, validity, status, approval chain
- **Claims tab:** List of students who claimed this offer — name, branch, class, discount amount, enrollment status
- **Branch Breakdown tab:** Per-branch: claims count, total discount, enrollment rate
- **Financial tab:** Total discount given, revenue impact, budget utilisation
- **History tab:** Offer lifecycle — created, approved, activated, paused, expired; all changes with who/when
- **Footer:** [Edit] [Pause/Resume] [Extend] [Clone for Next Season] [Deactivate]

### 6.4 Modal: `approve-offer` (480px, G4/G5)

- **Title:** "Approve Offer — [Offer Name]"
- **Content:** Offer summary, eligibility, discount, estimated financial impact
- **Actions:** Approve / Approve with Modifications / Reject (with reason)
- **Access:** G4/G5 only

---

## 7. Charts

### 7.1 Discount by Offer Type (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Total Discount by Offer Type" |
| Data | SUM(discount_amount) per offer type |
| Colour | Per type |
| Centre text | Total: ₹[X] |
| API | `GET /api/v1/group/{id}/marketing/enrollment/offers/analytics/by-type/` |

### 7.2 Claims Over Time (Area)

| Property | Value |
|---|---|
| Chart type | Stacked area |
| Title | "Offer Claims — Weekly Trend" |
| Data | Weekly claim count per offer type |
| API | `GET /api/v1/group/{id}/marketing/enrollment/offers/analytics/claims-trend/` |

### 7.3 Offer Effectiveness (Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar |
| Title | "Offer Effectiveness — Claims vs Enrollments" |
| Data | Per offer: claims (bar 1) vs enrollments from claims (bar 2) |
| Purpose | Shows which offers convert claims to actual enrollments |
| API | `GET /api/v1/group/{id}/marketing/enrollment/offers/analytics/effectiveness/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Offer created | "Offer '[Name]' created — pending approval" | Success | 3s |
| Offer approved | "Offer '[Name]' approved — now active" | Success | 4s |
| Offer rejected | "Offer '[Name]' rejected: [Reason]" | Warning | 5s |
| Offer activated | "Offer '[Name]' is now live" | Success | 3s |
| Offer paused | "Offer '[Name]' paused" | Info | 3s |
| Offer expired | "Offer '[Name]' has expired — [N] total claims" | Info | 3s |
| Claim cap reached | "Offer '[Name]' claim cap reached — offer auto-deactivated" | Warning | 5s |
| Budget cap reached | "Offer '[Name]' budget cap reached (₹[X]) — offer paused" | Warning | 5s |
| High discount alert | "Warning: Total discount exposure exceeds ₹[X]" | Warning | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No offers | 🏷️ | "No Admission Offers" | "Create your first offer to incentivise early enrollment." | Create Offer |
| No active offers | 📋 | "No Active Offers" | "All offers are either expired or paused." | Create Offer |
| No claims | 🎫 | "No Claims Yet" | "Claims will appear as students use offers during enrollment." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + offer cards/table skeleton |
| Offer detail drawer | 720px skeleton: overview + 5 tabs |
| Calculator | Form skeleton + output placeholder |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/enrollment/offers/` | G1+ | List all offers |
| GET | `/api/v1/group/{id}/marketing/enrollment/offers/{offer_id}/` | G1+ | Offer detail |
| POST | `/api/v1/group/{id}/marketing/enrollment/offers/` | G3+ | Create offer |
| PUT | `/api/v1/group/{id}/marketing/enrollment/offers/{offer_id}/` | G3+ | Update offer |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/offers/{offer_id}/status/` | G3+ | Activate/pause/deactivate |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/offers/{offer_id}/approve/` | G4+ | Approve/reject |
| GET | `/api/v1/group/{id}/marketing/enrollment/offers/{offer_id}/claims/` | G1+ | List claims |
| POST | `/api/v1/group/{id}/marketing/enrollment/offers/{offer_id}/claims/` | G3+ | Apply offer to student |
| GET | `/api/v1/group/{id}/marketing/enrollment/offers/calculator/` | G1+ | Calculator simulation |
| GET | `/api/v1/group/{id}/marketing/enrollment/offers/kpis/` | G1+ | KPIs |
| GET | `/api/v1/group/{id}/marketing/enrollment/offers/analytics/by-type/` | G1+ | Type donut |
| GET | `/api/v1/group/{id}/marketing/enrollment/offers/analytics/claims-trend/` | G1+ | Trend chart |
| GET | `/api/v1/group/{id}/marketing/enrollment/offers/analytics/effectiveness/` | G1+ | Effectiveness bars |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../offers/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#offers-content` | `innerHTML` | `hx-trigger="click"` |
| Offer detail drawer | Card/row click | `hx-get=".../offers/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create offer | Form submit | `hx-post=".../offers/"` | `#create-result` | `innerHTML` | Toast |
| Status change | Status button | `hx-patch=".../offers/{id}/status/"` | `#status-badge-{id}` | `innerHTML` | Inline update |
| Approve | Approve form | `hx-patch=".../offers/{id}/approve/"` | `#approval-result` | `innerHTML` | Toast + card refresh |
| Calculator | Calc form | `hx-get=".../offers/calculator/?..."` | `#calc-output` | `innerHTML` | Live calculation |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
