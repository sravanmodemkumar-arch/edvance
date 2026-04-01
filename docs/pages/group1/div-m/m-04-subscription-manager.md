# M-04 — Subscription Manager

**Route:** `GET /finance/subscriptions/`
**Method:** Django `TemplateView` + HTMX part-loads; server-side pagination
**Primary roles:** Billing Admin (#70), Pricing Admin (#74)
**Also sees:** Finance Manager (#69) read + approve plan changes; Finance Analyst (#101) read-only; AR Exec (#71) read-only (to see plan context before follow-up calls)

---

## Purpose

Single source of truth for all 2,050 institution subscriptions. Billing Admin uses this to activate new subscriptions (triggered by Division K CLOSED_WON handoff), upgrade/downgrade plans, adjust seat counts, manage billing cycle changes, suspend overdue accounts, and reactivate post-payment. Pricing Admin uses it to verify plan assignments and run bulk tier migrations when a new plan is launched. Finance Analyst monitors ARR distribution and flags anomalies. At any moment this page must answer: "Which institutions are on which plan, what do they pay, when does it expire, and what is their ARR contribution?"

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `analytics_revenue` latest month + `finance_subscription` active/suspended counts | 5 min |
| Subscription table | `finance_subscription` JOIN `finance_plan` JOIN `institution` JOIN auth_user (created_by) | 5 min |
| Tab counts | `finance_subscription` GROUP BY status | 5 min |
| Subscription detail drawer | `finance_subscription` + `finance_plan` + `finance_invoice` (last 3 invoices) + `finance_ar_aging` | Live |
| Plan options dropdown | `finance_plan` WHERE is_active=TRUE | 60 min |
| Expiring soon widget | `finance_subscription` WHERE end_date BETWEEN today AND today+60d | 5 min |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?status` | `all`, `active`, `suspended`, `expired`, `cancelled` | `active` | Pre-selects tab; filters table |
| `?tier` | `STARTER`, `STANDARD`, `PROFESSIONAL`, `ENTERPRISE` (comma-sep) | — | Filter by plan tier |
| `?type` | `school`, `college`, `coaching`, `group` (comma-sep) | — | Filter by institution type |
| `?expiring` | `30`, `60`, `90` | — | Show subscriptions expiring within N days |
| `?auto_renew` | `true`, `false` | — | Filter by auto_renew flag |
| `?q` | string ≥ 2 chars | — | ILIKE on institution_name |
| `?sort` | `end_date_asc`, `arr_desc`, `arr_asc`, `institution_name`, `created_desc` | `end_date_asc` | Table sort |
| `?page` | integer ≥ 1 | `1` | Pagination |
| `?export` | `csv` | — | Export (FM + Billing Admin + Pricing Admin) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| KPI strip | `?part=kpi` | Page load + 5 min poll | `#sub-kpi` |
| Subscription table | `?part=table` | Tab click · filter · sort · page | `#sub-table` |
| Tab counts | `?part=tab_counts` | After status change | `#sub-tabs` |
| Subscription drawer | `?part=drawer&id={id}` | Row click | `#sub-drawer` |
| Expiring widget | `?part=expiring` | Page load | `#sub-expiring` |
| Create/Edit modal | `?part=create_modal` or `?part=edit_modal&id={id}` | CTA click | `#modal-container` |
| Suspend modal | `?part=suspend_modal&id={id}` | [Suspend] action | `#modal-container` |
| Reactivate modal | `?part=reactivate_modal&id={id}` | [Reactivate] action | `#modal-container` |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  Subscription Manager                  [+ New Subscription]          │
├──────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (5 tiles)                                                 │
├──────────────────────────────────────────────────────────────────────┤
│  [Active(1950)] [Suspended(45)⚠] [Expired(42)] [Cancelled(13)]       │
├──────────────────────────────────────────────────────────────────────┤
│  [🔍 Search institution...]                                          │
│  [Tier▼] [Type▼] [Expiring▼] [Auto-Renew▼]          [Clear All]    │
├──────────────────────────────────────────────────────────────────────┤
│  EXPIRING SOON STRIP (cards scrollable)                              │
├──────────────────────────────────────────────────────────────────────┤
│  ☐ │ Institution │ Plan Tier │ Seats │ ARR │ End Date │ Status │ ⋯  │
│    │ 2,050 rows…                                                     │
├──────────────────────────────────────────────────────────────────────┤
│  Showing 1–25 of 1,950   [Bulk: Remind ▼]   [Export CSV]  [← 1 2 →]│
└──────────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip (5 tiles)

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ 1,950    │ │ ₹4.24Cr  │ │ 45       │ │ 42       │ │ 87%      │
│ Active   │ │ Total ARR│ │ Suspended│ │ Expiring │ │ Auto-    │
│ Subs     │ │          │ │ Accounts │ │ (60 days)│ │ Renew %  │
│ ↑+8 MoM  │ │ ↑+₹18L   │ │ ↑+3 MoM  │ │ ₹8.4L at │ │ of active│
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

- Tile 3 (Suspended): amber if > 20; red if > 50. Click → `?status=suspended`
- Tile 4 (Expiring 60d): amber if > 50. Shows ARR at risk. Click → `?expiring=60`
- Tile 5 (Auto-Renew %): target > 80%. Amber if 60–79%, red if < 60%.

---

## Expiring Soon Strip

Horizontally scrollable cards for subscriptions expiring within 30 days. Sorted by `end_date ASC`.

```
┌──────────────────────────────┐  ┌──────────────────────────────┐
│ KIMS School                  │  │ Delhi Coaching Hub            │
│ STANDARD · 420 seats         │  │ ENTERPRISE · 8,500 members    │
│ ARR: ₹84,000                 │  │ ARR: ₹12,40,000              │
│ Expires: 22 Mar (in 1d)      │  │ Expires: 30 Mar (in 9d)       │
│ Auto-renew: OFF ⚠             │  │ Auto-renew: ON               │
│ [Renew Now] [View Account]   │  │ [View Account]                │
└──────────────────────────────┘  └──────────────────────────────┘
```

- Red border: expires ≤ 3 days
- Amber border: expires 4–14 days
- Green border: auto_renew=ON and expires > 7 days (low urgency)
- [Renew Now] opens the Edit Subscription modal with end_date pre-set to +1 year (Billing Admin #70 only)
- [View Account] cross-links to J-03 Account Profile in Division J
- Empty state: "No subscriptions expiring in the next 30 days."

---

## Subscription Table

Server-side paginated, 25 rows per page.

| Column | Width | Description |
|---|---|---|
| Checkbox | 32px | Row selection; max 50 for bulk |
| Institution | 200px | Name (link → M-04 drawer) + type badge; city on 2nd line |
| Plan Tier | 90px | STARTER=grey · STANDARD=blue · PROFESSIONAL=indigo · ENTERPRISE=violet (all as badges) |
| Seats | 70px | Integer; tooltip: "max_seats for this plan: N" |
| ARR (₹) | 100px | `finance_subscription.arr_paise` formatted; right-aligned |
| Billing Cycle | 80px | MONTHLY or ANNUAL badge |
| Start Date | 95px | Date |
| End Date | 95px | Date; red if ≤ 14 days and auto_renew=OFF |
| Auto-Renew | 80px | Toggle switch; inline PATCH to `/finance/subscriptions/{id}/` (no confirmation dialog); immediate effect; toast: "Auto-renew [enabled/disabled] for [institution]." Available to Billing Admin (#70) and FM (#69) only. |
| Status | 110px | ACTIVE=green · SUSPENDED=red · EXPIRED=amber · CANCELLED=slate |
| Actions | 48px | 3-dot menu |

**Row click (non-link):** Opens subscription detail drawer.

**Auto-Renew toggle:** Inline PATCH to `/finance/subscriptions/{id}/` for Billing Admin (#70). Read-only toggle for all other roles (no click handler; cursor: not-allowed; tooltip: "Only Billing Admin can change this").

---

### Kebab Menu Actions

| Action | Available When | Role |
|---|---|---|
| View Subscription | Always | All |
| Edit Subscription | ACTIVE | Billing Admin (#70) + FM (#69) |
| Upgrade Plan | ACTIVE | Billing Admin (#70); FM (#69) confirms > 20% ARR change |
| Downgrade Plan | ACTIVE | Billing Admin (#70) + FM (#69) |
| Suspend Account | ACTIVE | Billing Admin (#70) + Collections Exec (#102) + 2FA |
| Reactivate Account | SUSPENDED | Billing Admin (#70) + FM (#69) + 2FA |
| Cancel Subscription | ACTIVE | FM (#69) only + 2FA |
| Generate Invoice (manual) | ACTIVE | Billing Admin (#70); shortcuts to M-03 Generate modal pre-filled |

---

## Subscription Detail Drawer (640px)

```
┌──────────────────────────────────────────────────────────┐
│  Delhi Coaching Hub — Subscription              [×] [Edit]│
├──────────────────────────────────────────────────────────┤
│  PLAN DETAILS                                            │
│  Plan:   ENTERPRISE (slug: enterprise-v3)                │
│  ARR:    ₹12,40,000      Billing: ANNUAL                 │
│  Seats:  8,500           Auto-Renew: ON                  │
│  Start:  01 Apr 2025     End: 31 Mar 2026 (in 10 days)   │
│  Discount: 10% (Annual Payment) until 31 Mar 2026        │
├──────────────────────────────────────────────────────────┤
│  PLAN FEATURES (from plan.features_json)                 │
│  ✓ Unlimited exams    ✓ AI MCQ generation                │
│  ✓ BGV integration    ✓ Custom branding                   │
│  ✓ Priority support   ✓ Dedicated CSM                    │
├──────────────────────────────────────────────────────────┤
│  RECENT INVOICES                                         │
│  INV-2026-00610  Mar 2026  ₹1,03,333  PAID   01 Mar ✓   │
│  INV-2025-00410  Feb 2026  ₹1,03,333  PAID   01 Feb ✓   │
│  INV-2025-00210  Jan 2026  ₹1,03,333  PAID   01 Jan ✓   │
│  [View all invoices →]                                   │
├──────────────────────────────────────────────────────────┤
│  AR AGING                                                │
│  Current (0-30d): ₹0    31-60d: ₹0    90+d: ₹0          │
│  Total Outstanding: ₹0  ← healthy                        │
└──────────────────────────────────────────────────────────┘
```

**Plan Features:** Rendered from `finance_plan.features_json` as a checkbox list (read-only). All active features shown with ✓; unavailable features shown with ✗ in grey.

**Recent Invoices:** Last 3 invoices from `finance_invoice` for this institution. Status badge + paid/overdue indicator. [View all invoices →] links to M-03?q=<institution_name>.

**AR Aging:** Shows `finance_ar_aging` buckets for this institution. If any bucket > 0, shows amber/red highlighting. [View AR →] links to M-05?institution_id=<id>.

**Suspended account banner:** If status='SUSPENDED', prominent red banner: "Account suspended on [suspended_at] — Reason: [suspended_reason]. [Reactivate →]"

---

## Create / Edit Subscription Modal (560px)

Used for both creating new subscriptions (post-CLOSED_WON handoff) and editing existing ones.

| Field | Type | Validation |
|---|---|---|
| Institution* | Typeahead search | Required; unique (only one active subscription per institution) |
| Plan* | Select from `finance_plan` WHERE is_active=TRUE | Required |
| Seats* | Integer input | Required; ≥ plan.min_seats; ≤ plan.max_seats (if set); warning if seats > 1.5× institution's historical student count |
| Billing Cycle* | Radio: MONTHLY / ANNUAL | Required; Annual gives 10% default discount |
| Start Date* | Date picker | Required; default: today |
| End Date* | Date picker | Required; must be > start_date; default: +1 year for ANNUAL, +1 month for MONTHLY |
| Auto-Renew | Checkbox | Default: TRUE |
| ARR (₹)* | Decimal input | Auto-calculated: plan.base_price + (seats × plan.price_per_seat); editable (Enterprise custom pricing); changes > 20% show amber warning |
| Discount | Select from active `finance_discount` WHERE institution_id=this or global | Optional |
| Notes | Textarea | Optional; max 500 chars |

**ARR auto-calculation:** When Plan or Seats changes, ARR field updates: `base_price_paise + (seats × price_per_seat_paise) - discount_amount`. Displayed in ₹. If user manually overrides ARR (Enterprise custom pricing), field gets amber background.

**ARR change > 20% warning (edit mode):** "This change increases/decreases ARR by ₹X.XL ([N]%). Finance Manager approval required for ARR changes > 20%." — if FM (#69) is not the actor, creates a pending approval request; FM receives in-app notification.

**ARR > 20% Approval Flow:**
1. Billing Admin submits change. If ARR delta > 20%, subscription saved with `status = 'PENDING_APPROVAL'` (subscription is held, not yet active).
2. Toast to Billing Admin: "ARR change of ₹[delta] sent to Finance Manager for approval."
3. FM sees PENDING_APPROVAL row in subscription table (amber badge). Kebab menu shows [Approve ARR Change] / [Reject ARR Change].
4. On Approve: PATCH `/finance/subscriptions/{id}/approve-arr/` → status → ACTIVE; Billing Admin notified; invoice generation proceeds.
5. On Reject: FM adds rejection note; Billing Admin notified; subscription returned to previous state.

**On save (non-pending):** POST/PATCH `/finance/subscriptions/` or `/finance/subscriptions/{id}/`. Toast: "Subscription [created/updated] for [institution]." Task M-2 is notified to skip auto-generation for this institution's next billing period (since we just created/updated manually).

---

## Suspend Account Modal (480px — with 2FA)

```
  Suspend Account
  ─────────────────────────────────────────────────────────
  Delhi Coaching Hub · ENTERPRISE · ₹12.4L ARR
  ─────────────────────────────────────────────────────────
  Reason*  [NON_PAYMENT ▼]   (options: NON_PAYMENT/POLICY_VIOLATION/
                               INSTITUTION_REQUEST/LEGAL_HOLD)
  Notes*   [3rd notice sent; no response since 5 Mar...   ]
  ─────────────────────────────────────────────────────────
  ⚠ Suspending will:
  • Block all logins for institution staff and students
  • Disable exam creation and result access
  • Send suspension notice to institution admin
  ─────────────────────────────────────────────────────────
  2FA code*  [      ]
  [Cancel]                              [Suspend Account]
```

- Reason: required
- Notes: required (min 20 chars)
- 2FA: required
- On confirm: `finance_subscription.status → SUSPENDED`, `suspended_at`, `suspended_reason` set. Notifies Division C Platform Admin (#10) to revoke platform access. Notifies Division J Account Manager (#54) and CSM (#53). Notifies institution billing contact via email.

---

## Reactivate Account Modal (480px — with 2FA)

```
  Reactivate Account
  ─────────────────────────────────────────────────────────
  Delhi Coaching Hub · ENTERPRISE · SUSPENDED since 05 Mar 2026
  Reason for suspension: NON_PAYMENT
  Notes: 3rd notice sent; no response since 5 Mar
  ─────────────────────────────────────────────────────────
  Outstanding Balance:  ₹1,77,000  (2 overdue invoices)
  ─────────────────────────────────────────────────────────
  Reactivation Reason*
  [PAYMENT_RECEIVED ▼]
  (options: PAYMENT_RECEIVED / PAYMENT_PLAN_AGREED /
            DISPUTE_RESOLVED / LEGAL_HOLD_LIFTED /
            MANAGEMENT_OVERRIDE)
  Notes*  [Received ₹1,77,000 via NEFT; ref TXN-XXXXXXXX...]
  ─────────────────────────────────────────────────────────
  ☐  I confirm outstanding balance has been reviewed
     and reactivation is authorised.
  ─────────────────────────────────────────────────────────
  2FA code*  [      ]
  [Cancel]                          [Reactivate Account]
```

**Validation:**
- Reactivation Reason: required
- Notes: required; min 20 chars; max 2000 chars
- Authorisation checkbox: must be checked
- 2FA: required

**Outstanding balance warning:** If `finance_ar_aging` still shows overdue balance at reactivation time, the modal shows the balance prominently in amber. Does NOT block reactivation (FM / Billing Admin may reactivate on payment plan), but forces acknowledgement.

**On confirm:** PATCH `/finance/subscriptions/{id}/reactivate/`.
- `finance_subscription.status → ACTIVE`
- `suspended_at` / `suspended_reason` cleared; `reactivated_at`, `reactivated_by_id`, `reactivation_reason` set
- Notifies Division C Platform Admin (#10) to restore platform access
- Notifies Division J Account Manager (#54) and CSM (#53)
- Notifies institution billing contact via email: "Your EduForge account has been reactivated."
- Writes `finance_audit_log` entry (table=finance_subscription, action=REACTIVATE)

Toast: "[institution] account reactivated. Platform access restored."

**Authorization:** Available to FM (#69) and Billing Admin (#70) only. Both require 2FA.

---

## Cancel Subscription Modal (480px — FM #69 only, with 2FA)

```
  Cancel Subscription
  ─────────────────────────────────────────────────────────
  Delhi Coaching Hub · ENTERPRISE · ₹12.4L ARR
  Active since: 01 Apr 2025 · End date: 31 Mar 2026
  ─────────────────────────────────────────────────────────
  Reason*  [INSTITUTION_REQUEST ▼]
           (INSTITUTION_REQUEST / CHURNED / BANKRUPT /
            CONTRACT_VIOLATION / MERGED_CONSOLIDATED)
  Notes*   [Institution confirmed non-renewal in writing...]
  Effective Date*  [31 Mar 2026]
  ─────────────────────────────────────────────────────────
  ⚠ Cancelling will:
  • Set subscription status to CANCELLED
  • Stop future invoice auto-generation (Task M-2 skip)
  • Notify Division J Account Manager and CSM
  • Notify institution billing contact via email
  ─────────────────────────────────────────────────────────
  2FA code*  [      ]
  [Cancel]                        [Confirm Cancellation]
```

**Validation:**
- Reason: required
- Notes: required; min 20 chars; max 2000 chars; HTML-escaped on display
- Effective Date: required; ≥ today; ≤ `finance_subscription.end_date`
- 2FA: required

**On confirm:** POST `/finance/subscriptions/{id}/cancel/`.
- `finance_subscription.status → CANCELLED`; `cancelled_at` = now; reason + notes stored
- Division J: in-app + email to Account Manager (#54) and CSM (#53)
- Institution billing contact: email "Your EduForge subscription has been cancelled effective [date]."
- `finance_audit_log` entry (action=CANCELLED)

Toast: "[institution] subscription cancelled effective [effective date]."

---

## Bulk Actions

| Bulk Action | Behaviour | Role |
|---|---|---|
| Send Renewal Reminder | Bulk email via F-06 to institutions expiring in ≤ 60 days. Shows count + ARR at risk. | Billing Admin, FM |
| Export Selected | CSV of selected rows (≤ 50). | Billing Admin, FM, Pricing Admin |
| Bulk Tier Migration | Only for Pricing Admin when launching a new plan: modal with "Migrate N institutions from [Old Plan] to [New Plan] effective [date]". Requires FM confirmation. Creates a pending approval task. | Pricing Admin + FM approval |

---

## Empty States

| Condition | Message | CTA |
|---|---|---|
| No active subscriptions | "No active subscriptions yet." | [+ New Subscription] |
| No subscriptions match filters | "No subscriptions match your current filters." | [Clear Filters] |
| Suspended tab: none | "No suspended accounts." | — |
| Expiring strip: none | "No subscriptions expiring in the next 30 days." | — |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Subscription created | "Subscription activated for [institution] — [Plan] plan, ₹[ARR] ARR." | Green |
| Subscription updated | "[institution] subscription updated." | Green |
| Plan upgraded | "[institution] upgraded from [old] to [new] plan." | Green |
| Account suspended | "[institution] account suspended. Platform access revoked." | Amber (warning) |
| Account reactivated | "[institution] account reactivated. Platform access restored." | Green |
| ARR change > 20% pending FM approval | "ARR change of ₹[delta] sent to Finance Manager for approval." | Amber |
| FM approved ARR change | "ARR change approved and applied to [institution] subscription." | Green |
| Auto-renew toggled | "Auto-renew [enabled/disabled] for [institution]." | Green |

---

## Authorization

**Route guard:** `@division_m_required(allowed_roles=[69, 70, 71, 74, 101])`.

| Scenario | Behaviour |
|---|---|
| Billing Admin (#70) | Full CRUD; suspend/reactivate + 2FA; auto-renew toggle |
| Finance Manager (#69) | Full read + approve ARR changes + cancel subscription + reactivate + 2FA |
| AR Exec (#71) | Read-only all tabs; no write actions; useful for seeing plan context before follow-up calls |
| Pricing Admin (#74) | Full read; edit plan_id (tier changes) + bulk tier migration; no suspend/reactivate |
| Finance Analyst (#101) | Read-only; no actions |
| Collections Exec (#102) | Suspend action only on ACTIVE subscriptions; no other edits |

---

## Role-Based UI Visibility Summary

| Feature | 69 FM | 70 Billing | 71 AR Exec | 74 Pricing | 101 Analyst | 102 Collections |
|---|---|---|---|---|---|---|
| [+ New Subscription] | Yes | Yes | No | No | No | No |
| Full table all tabs | Yes | Yes | Yes (read) | Yes (read) | Yes (read) | Active tab only |
| Edit Subscription | Yes | Yes | No | Plan tier only | No | No |
| Upgrade/Downgrade | Yes (+ approve >20%) | Yes | No | Yes | No | No |
| Auto-Renew toggle | Yes | Yes | No | No | No | No |
| Suspend Account | No (via FM approval) | Yes + 2FA | No | No | No | Yes + 2FA |
| Reactivate Account | Yes + 2FA | Yes + 2FA | No | No | No | No |
| Cancel Subscription | Yes + 2FA | No | No | No | No | No |
| Bulk Tier Migration | Yes (approve) | No | No | Yes (initiate) | No | No |
| Export CSV | Yes | Yes | No | Yes | No | No |
| Expiring Soon strip | Yes | Yes | Yes (read) | Yes | Yes (read) | No |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Initial page load (SSR) | < 2s P95 | KPI strip + expiring-soon strip from cache; table live |
| KPI strip | < 500ms P95 (cache hit) | 5-min TTL |
| Subscription table (25 rows) | < 400ms P95 | Indexed on `institution_id`, `status`, `plan_id` |
| Subscription detail drawer | < 300ms P95 | Live fetch; `finance_subscription` + `finance_ar_aging` JOIN |
| Expiring soon card strip | < 600ms P95 (cache hit) | 5-min TTL; sorted by `end_date ASC` |
| ARR change > 20% approval workflow | < 1s round-trip | POST to approval endpoint; in-app notification queued |
| Bulk tier migration (≤ 50 institutions) | < 10s | Celery task; immediate amber toast with job ID |

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `s` | Go to Subscription Manager (M-04) |
| `n` | Open New Subscription modal (Billing Admin, FM) |
| `/` | Focus institution search |
| `e` | Export CSV (FM, Billing Admin, Pricing Admin) |
| `←` / `→` | Previous / next page in subscription table |
| `1`–`5` | Switch to tab: ALL / ACTIVE / SUSPENDED / CANCELLED / EXPIRING |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |

