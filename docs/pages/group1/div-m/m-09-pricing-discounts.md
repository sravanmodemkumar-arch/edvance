# M-09 — Pricing & Discounts

**Route:** `GET /finance/pricing/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** Pricing Admin (#74)
**Also sees:** Finance Manager (#69) read + approve discounts > 20%; Finance Analyst (#101) read-only

---

## Purpose

Subscription tier configuration and discount lifecycle management. Pricing Admin owns: (1) subscription plan tiers (Starter/Standard/Professional/Enterprise) — their base prices, per-seat pricing, feature flags, and effective dates; (2) institution-specific custom discounts (goodwill, competitive win-back, multi-institution group deals); (3) promo codes for marketing campaigns. Finance Manager approves any discount exceeding 20% to prevent unauthorised revenue leakage. Finance Analyst monitors ARR impact of discount patterns and models pricing changes.

At ₹4Cr+ ARR, even a 5% average discount across the portfolio = ₹20L+ of annual ARR impact. This page makes that visible and governable.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Pricing KPI strip | `analytics_revenue` plan distribution + `finance_discount` active discounts | 5 min |
| Plan table | `finance_plan` WHERE effective_until IS NULL (current plans) | 60 min |
| Plan history | `finance_plan` WHERE effective_until IS NOT NULL (past plans) | 60 min |
| Discount table | `finance_discount` JOIN `institution` LEFT JOIN `finance_plan` | 5 min |
| Promo code table | `finance_promo_code` ORDER BY valid_to DESC | 5 min |
| ARR impact analysis | `analytics_revenue` + `finance_discount` (analyst-only toggle) | 60 min |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?tab` | `plans`, `discounts`, `promos` | `plans` | Active section tab |
| `?tier` | `STARTER`, `STANDARD`, `PROFESSIONAL`, `ENTERPRISE` | — | Filter plan table or discount table |
| `?status` | `active`, `expired`, `pending_approval`, `inactive` | `active` | Filter discounts or promos |
| `?q` | string | — | ILIKE on institution_name (discounts) or promo code |
| `?page` | integer ≥ 1 | `1` | Pagination |
| `?export` | `csv` | — | Export (FM + Pricing Admin + Analyst) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| KPI strip | `?part=kpi` | Page load | `#pricing-kpi` |
| Plan table | `?part=plan_table` | Tab: plans | `#pricing-plans` |
| Discount table | `?part=discount_table` | Tab: discounts + filter | `#pricing-discounts` |
| Promo table | `?part=promo_table` | Tab: promos + filter | `#pricing-promos` |
| Plan drawer | `?part=plan_drawer&id={id}` | Row click (plans) | `#pricing-drawer` |
| Discount drawer | `?part=discount_drawer&id={id}` | Row click (discounts) | `#pricing-drawer` |
| Create/Edit Plan modal | `?part=plan_modal` or `?part=plan_modal&id={id}` | [+ New Plan] / [Edit] | `#modal-container` |
| Create Discount modal | `?part=discount_modal` or `?part=discount_modal&id={id}` | [+ Add Discount] | `#modal-container` |
| Create Promo modal | `?part=promo_modal` or `?part=promo_modal&id={id}` | [+ New Promo Code] | `#modal-container` |
| ARR impact overlay | `?part=arr_impact&tier={tier}` | [Preview ARR Impact] | `#pricing-impact` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Pricing & Discounts                                                │
├─────────────────────────────────────────────────────────────────────┤
│  PRICING KPI STRIP (5 tiles)                                        │
├─────────────────────────────────────────────────────────────────────┤
│  [Plans (4)] [Discounts (28)] [Promo Codes (6)]                     │
├─────────────────────────────────────────────────────────────────────┤
│  [Active tab content]                                               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Pricing KPI Strip (5 tiles)

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ 28       │ │ ₹1.85L   │ │ 3        │ │ 6        │ │ 4.2%     │
│ Active   │ │ Monthly  │ │ Pending  │ │ Active   │ │ Avg      │
│ Discounts│ │ ARR      │ │ FM Aprvl │ │ Promo    │ │ Discount │
│ 2,050 cov│ │ Impact   │ │ >20%     │ │ Codes    │ │ Rate     │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

- **Tile 1 (Active Discounts):** COUNT active `finance_discount`. Sub-label: "covering N institutions". Amber if > 50 (too many may indicate pricing discipline erosion).
- **Tile 2 (Monthly ARR Impact):** SUM of monthly discount savings across all active institution discounts. Amber if > ₹5L/month (> ~1.5% of ₹4Cr ARR). This is the revenue EduForge is giving away.
- **Tile 3 (Pending FM Approval):** COUNT discounts WHERE `fm_approval_required=TRUE` AND `approved_by_id IS NULL`. Red if > 0. FM (#69) sees this tile with a link to the Discounts tab filtered to `?status=pending_approval`.
- **Tile 4 (Active Promo Codes):** COUNT `finance_promo_code` WHERE is_active=TRUE AND (valid_to IS NULL OR valid_to >= today). Amber if > 10 simultaneously active codes.
- **Tile 5 (Avg Discount Rate):** AVG effective discount % across all subscriptions with active discounts: `1 - (subscribed_arr / base_arr)`. Green if < 5%, amber if 5–10%, red if > 10%.

---

## Tab: Plans

Subscription plan configuration table.

### Plan Table

| Column | Width | Description |
|---|---|---|
| Tier | 100px | STARTER/STANDARD/PROFESSIONAL/ENTERPRISE badge |
| Plan Name | 160px | e.g. "Enterprise v3 (2026)" |
| Version | 60px | Integer; latest version for each tier shown by default |
| Base Price (₹/month) | 120px | `base_price_paise / 100` in ₹; displayed as annual for ANNUAL cycle |
| Per-Seat Price (₹) | 110px | `price_per_seat_paise / 100` |
| Min / Max Seats | 100px | e.g. "0 / unlimited" or "100 / 5,000" |
| Active Subscriptions | 100px | COUNT `finance_subscription` WHERE plan_id=this AND status='ACTIVE' |
| ARR (₹) | 100px | SUM ARR of those subscriptions |
| Effective From | 90px | Date; "Current" badge if `effective_until IS NULL` |
| Status | 80px | ACTIVE / ARCHIVED badge |
| Actions | 48px | 3-dot menu: [View Details], [Edit] (Pricing Admin), [Archive] (Pricing Admin — active plans only), [View History] |

**[+ New Plan] button:** Opens Plan modal. Pricing Admin only.

**[Archive] action:** Sets `finance_plan.is_active = FALSE`; plan version becomes read-only. Confirmation: "Archive [Plan Name]? Existing subscriptions are unaffected. No new subscriptions can use this plan." POST `/finance/pricing/plans/{id}/archive/`. Only available if plan has no active subscriptions (`finance_subscription.plan_id = this AND status = 'ACTIVE'` must be 0); if subscriptions exist, button is disabled with tooltip "Cannot archive plan with active subscriptions."

**Version management:** Each plan tier can have multiple versions. Only the version with `effective_until IS NULL` is "current". Creating a new plan version auto-sets the old version's `effective_until = new_version.effective_from - 1 day`. All existing subscriptions on the old version remain; new subscriptions get the latest version.

---

### Plan Detail Drawer (640px)

```
┌─────────────────────────────────────────────────────────────────┐
│  ENTERPRISE Plan — v3 (2026)                          [×] [Edit] │
├─────────────────────────────────────────────────────────────────┤
│  PRICING                                                        │
│  Base Price:   ₹5,00,000 / year (₹41,667/month)                │
│  Per-Seat:     ₹15 / seat / year                                │
│  Min Seats:    500       Max Seats: Unlimited                   │
│  Effective:    01 Jan 2026 → current                            │
├─────────────────────────────────────────────────────────────────┤
│  FEATURES (from finance_plan_feature registry)                  │
│  ✓ Unlimited live exams        ✓ AI MCQ generation              │
│  ✓ Custom branding             ✓ Dedicated CSM assigned         │
│  ✓ BGV integration             ✓ SLA: < 4h response             │
│  ✓ API access                  ✓ Advanced analytics             │
│  ✓ White-label mobile app      ✓ Multi-campus support           │
│  ✗ Self-serve (Dedicated support required for Enterprise)       │
├─────────────────────────────────────────────────────────────────┤
│  ADOPTION                                                       │
│  Active subscriptions: 105     ARR contribution: ₹23.8Cr        │
│  % of total ARR: 56.7%         Avg seats/institution: 8,100     │
├─────────────────────────────────────────────────────────────────┤
│  PRICING HISTORY                                                │
│  v2 (2025): ₹4,00,000/yr base · 01 Jan 2025 → 31 Dec 2025       │
│  v1 (2024): ₹3,00,000/yr base · Launch → 31 Dec 2024            │
└─────────────────────────────────────────────────────────────────┘
```

---

### Create / Edit Plan Modal (560px)

| Field | Type | Validation |
|---|---|---|
| Tier* | Select: STARTER/STANDARD/PROFESSIONAL/ENTERPRISE | Required |
| Plan Name* | Text | Required; min 3 chars; suggestion: "[Tier] [Year]" |
| Base Price (₹/year)* | Decimal input (stored as paise) | Required; ≥ 0 |
| Per-Seat Price (₹/seat/year) | Decimal | Optional; default 0; used for seat-based scaling |
| Min Seats | Integer | Optional; default 0 |
| Max Seats | Integer | Optional; NULL = unlimited |
| Billing Cycle | Radio: MONTHLY / ANNUAL | Required |
| Effective From* | Date picker | Required; must be ≥ today; if editing: must be > existing active version's effective_from |
| Features | Dynamic checkbox list from a master feature registry (`finance_plan_feature`) | Select all applicable features |

**ARR Impact Preview (Finance Analyst toggle #101 or FM #69):** Below the form, shows: "If this plan replaces [old plan] for [N] existing subscriptions, ARR impact: +₹X.XL or −₹X.XL."

**Feature storage approach:** Features are stored as a JSONB array of feature IDs in `finance_plan.features_json` (e.g., `[1, 3, 7, 12]`). The master feature registry is the `finance_plan_feature` table (id, name, description, is_active). When rendering the plan detail drawer or the create/edit modal, the UI joins `features_json` IDs against `finance_plan_feature` to display human-readable feature names. This hybrid approach allows fast reads (no join for simple plan lookups) while maintaining a central feature registry for the checkbox list. The checkbox list in the modal is populated from `finance_plan_feature WHERE is_active=TRUE`.

**On save:**
- New plan: creates `finance_plan` with version = max(existing_for_tier) + 1. Sets old plan's `effective_until = effective_from - 1 day`.
- Edit: cannot edit past plans (creates a new version instead); "Archive" action available.

---

## Tab: Discounts

Institution-specific and global discounts.

### Discount Table (25 rows/page, sortable)

| Column | Width | Description |
|---|---|---|
| Institution | 180px | Name + type badge; "GLOBAL" for global discounts |
| Discount Type | 90px | PERCENTAGE or FIXED badge |
| Discount Value | 100px | "N%" or "₹X,XXX" |
| Reason | 160px | Truncated; full on hover |
| Valid From | 90px | Date |
| Valid To | 90px | Date or "Permanent" |
| Monthly ARR Impact (₹) | 110px | `institution.arr × discount_rate / 12`; amber if > ₹50K/month |
| FM Approval | 80px | ✓ Approved / ⏳ Pending / N/A |
| Status | 80px | ACTIVE/EXPIRED/PENDING badge |
| Actions | 48px | 3-dot menu |

**Pending approval rows:** Amber left border. FM (#69) sees [Approve] / [Reject] buttons directly in the row; Pricing Admin sees "Awaiting FM approval" badge.

**[+ Add Discount] button:** Opens discount creation modal. Pricing Admin only.

---

### Create / Edit Discount Modal (480px)

```
  Add Discount
  ──────────────────────────────────────────────────────────
  Institution   [Search institution...] or [Global discount ☐]
  Discount Type* [PERCENTAGE ▼]   (or FIXED_PAISE)
  Value*         [15]   %         (if >20%: FM approval required)
                                  ⚠ Current: 15% — FM approval NOT required
  Applies to Plan  [All plans ▼]   (optional filter)
  Valid From*  [01 Apr 2026]
  Valid To     [31 Mar 2027]   (leave blank = permanent)
  Reason*      [Annual payment discount — 15% off for upfront payment]
  ──────────────────────────────────────────────────────────
  ARR Impact: −₹18,000/month for [institution] at [plan] rate
  ──────────────────────────────────────────────────────────
  [Cancel]                             [Create Discount]
```

**20% threshold logic:**
- On the `discount_value` field: real-time validation on keystroke — if `discount_type = PERCENTAGE` and value > 20, inline message appears immediately below the field: "⚠ Discounts > 20% require Finance Manager approval. This discount will be created in PENDING_APPROVAL status until approved."
- If FM (#69) is the actor: no pending step; discount immediately ACTIVE.
- The inline message disappears if the user lowers the value to ≤ 20%.

**ARR Impact preview:** Real-time computation as value changes: "This discount reduces [institution]'s ARR from ₹X.XL to ₹Y.YL (−₹ZZ,ZZZ/month)."

**Validation:**
- Institution OR Global required
- Value: > 0; if PERCENTAGE: max 100 (but amber if > 25)
- Valid From: ≤ Valid To (if set)
- Reason: required; min 10 chars

---

## Tab: Promo Codes

Marketing promo codes for discount campaigns.

### Promo Code Table

| Column | Width | Description |
|---|---|---|
| Code | 140px | e.g. `SCHOOL2026` monospace; copy icon |
| Discount | 120px | "20% off" or "₹5,000 off" |
| Uses | 90px | `current_uses / max_uses` or `N / ∞` |
| Valid From | 90px | Date |
| Valid To | 90px | Date or "No expiry" |
| Plan Restriction | 120px | Plan tier badge or "Any plan" |
| Institution Type | 120px | Type badge or "Any type" |
| Status | 80px | ACTIVE=green / EXPIRED=grey / DEPLETED=amber |
| Actions | 48px | 3-dot menu |

**DEPLETED:** `current_uses >= max_uses`. Amber badge; [Extend Limit] action.
**Expired:** `valid_to < today`. Grey badge; [Clone & Extend] action.

**[+ New Promo Code] button:** Pricing Admin only.

---

### Create / Edit Promo Code Modal (480px)

| Field | Type | Validation |
|---|---|---|
| Code* | Text | Required; uppercase enforced; unique; min 4 chars; max 30 chars; regex `^[A-Z0-9_-]+$`; [Generate Random] button |
| Discount Type* | Select: PERCENTAGE / FIXED_PAISE | Required |
| Discount Value* | Decimal | Required; > 0; if PERCENTAGE > 100: error |
| Max Uses | Integer | Optional; NULL = unlimited; min 1 if set |
| Valid From* | Date picker | Required; default: today |
| Valid To | Date picker | Optional; must be > valid_from if set |
| Plan Restriction | Select from active plans | Optional; NULL = any plan |
| Institution Type Restriction | Select: all/school/college/coaching/group | Optional; NULL = any |

**[Generate Random]:** Generates a code using `secrets.token_hex(3).upper()` (6 random hex chars) prefixed with a context string. Format: `{PREFIX}{MMYYYY}{6_random_hex}`. Default prefix = "EDU"; example: `EDU0320261A4F9C`. User can edit the generated code before saving. The prefix field (3–6 uppercase letters) is editable in the modal when using Generate Random, allowing custom campaigns like "SCHOOL", "LAUNCH", "DIWALI".

**Code uniqueness:** Checked server-side on submit (not on keystroke — avoids race conditions on concurrent creation). Error displayed inline below the Code field: "Promo code [CODE] already exists. Choose a different code or click [Generate Random] again."

---

## ARR Impact Analysis (Finance Analyst + FM toggle)

When Finance Analyst (#101) or FM (#69) clicks **[Show ARR Impact]**, an overlay panel appears below the relevant tab.

**Toggle button:** `[Show ARR Impact]` (green, right-aligned above active tab). Visible only to FM (#69) and Analyst (#101).
- HTMX: `GET ?part=arr_impact&tab={plans|discounts|promos}` — target `#pricing-impact-panel` (rendered inline below tab content)
- Cache: 60-min TTL; `?nocache=true` supported
- Close: `[×]` button on panel; hides without reload (hx-swap="delete")

**Content varies by active tab:**

**For Plans tab:** "If you change [STANDARD] plan price by +₹10,000/year, applying to all 890 current Standard subscribers would generate +₹8.9Cr additional ARR — assuming 0% churn from the increase." Modelling assumes no churn (optimistic) and a 5% churn scenario (pessimistic) side by side.

**For Discounts tab:** A chart showing monthly ARR discount given away by tier and reason: "GOODWILL discounts: ₹12K/month · COMPETITIVE discounts: ₹45K/month · ANNUAL_PAYMENT discounts: ₹1.28L/month". Bar chart by discount reason.

**For Promo Codes tab:** A table showing active codes ranked by ARR impact: which promo code has been used most and cost the most ARR.

---

## Pricing Change History

Below each tab (Plans, Discounts, Promos): a collapsible "Change History" panel showing the last 10 state-changing events (from `finance_audit_log` WHERE table_name IN ('finance_plan','finance_discount','finance_promo_code')). Shows: actor, action, timestamp, old value → new value.

---

## Empty States

| Condition | Message | CTA |
|---|---|---|
| No active plans | "No active subscription plans configured." | [+ New Plan] |
| No active discounts | "No institution discounts active." | [+ Add Discount] |
| No promo codes | "No promo codes created yet." | [+ New Promo Code] |
| Discounts: no pending FM approval | "No discounts awaiting approval." | — |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Plan created | "New [Tier] plan version created. Effective from [date]." | Green |
| Plan archived | "[Plan name] archived." | Amber |
| Discount created (< 20%) | "Discount created and activated for [institution]." | Green |
| Discount created (> 20%, pending FM) | "Discount submitted for Finance Manager approval." | Amber |
| FM approved discount | "Discount for [institution] approved and activated." | Green |
| FM rejected discount | "Discount for [institution] rejected: [reason]." | Red |
| Promo code created | "Promo code [CODE] created and active." | Green |
| Promo code deactivated | "Promo code [CODE] deactivated." | Amber |
| Promo code depleted | "Promo code [CODE] has reached max uses ([N])." | Amber (auto-toast on depletion) |
| Code already exists | "Promo code [CODE] already exists. Choose a different code." | Red (inline) |

---

## Authorization

**Route guard:** `@division_m_required(allowed_roles=[69, 74, 101])`.

| Scenario | Behaviour |
|---|---|
| Pricing Admin (#74) | Full CRUD on plans, discounts, promos. Discounts > 20% land in PENDING_APPROVAL; FM must approve before activation. |
| Finance Manager (#69) | Read + approve/reject discounts > 20%. Can create discounts directly (bypasses pending step — FM is approver for themselves). Cannot create or archive plans (Pricing Admin domain). |
| Finance Analyst (#101) | Read-only; ARR Impact Analysis toggle; export CSV; no write actions. |
| Other finance roles | 403 — pricing config is restricted to Pricing Admin + FM + Analyst only. |

---

## Role-Based UI Visibility Summary

| Element | 69 FM | 74 Pricing Admin | 101 Analyst |
|---|---|---|---|
| Pricing KPI strip | All (read) + Pending approval tile | All | All (read) |
| [+ New Plan] | No | Yes | No |
| Edit Plan | No | Yes | No |
| Archive Plan | No | Yes | No |
| [+ Add Discount] | Yes (no pending step) | Yes (>20% → pending) | No |
| Edit Discount | Yes | Yes | No |
| Approve/Reject Discount > 20% | Yes (exclusive) | No | No |
| [+ New Promo Code] | No | Yes | No |
| Deactivate Promo Code | No | Yes | No |
| ARR Impact Analysis | Yes | No | Yes |
| Pricing Change History | Yes | Yes | Yes (read) |
| Export CSV | Yes | Yes | Yes |
| Plan Detail Drawer | Yes | Yes | Yes (read) |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Initial page load (SSR) | < 2s P95 | KPI strip + plan table from cache |
| KPI strip | < 500ms P95 (cache hit) | 10-min TTL |
| Plan table (all tiers, ≤ 20 rows) | < 400ms P95 (cache hit) | 30-min TTL |
| Discount table (25 rows) | < 400ms P95 (cache hit) | 10-min TTL |
| Promo code table (25 rows) | < 400ms P95 (cache hit) | 10-min TTL |
| Plan detail drawer | < 400ms P95 (cache hit) | 30-min TTL; includes adoption stats |
| ARR impact preview (modal) | < 600ms | DB query: COUNT + SUM of subscriptions on old plan |
| ARR Impact Analysis overlay | < 1s (cache hit) | 60-min TTL; FM + Analyst only |

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `p` | Go to Pricing & Discounts (M-09) |
| `n` | New Plan (Pricing Admin) / New Discount (Pricing Admin, FM) / New Promo Code (Pricing Admin) — context-sensitive to active tab |
| `1`–`3` | Switch tab: Plans / Discounts / Promo Codes |
| `e` | Export CSV |
| `/` | Focus search within active tab |
| `←` / `→` | Previous / next page |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |

