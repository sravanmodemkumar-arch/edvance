# K-06 — Channel Partner Portal

**Route:** `GET /group1/k/channel-partners/`
**Method:** Django `ListView` + HTMX part-loads + drawer-based detail + modal
**Primary role:** Channel Partner Manager (#63)
**Also sees:** B2B Sales Manager (#57 — view + commission approval), Sales Ops Analyst (#95 — read-only)

---

## Purpose

Full lifecycle management of EduForge's reseller, distributor, affiliate, and referral network. Channel partners source institution leads and earn commissions — default 10% of first-year ARR — on deals they introduce and that close as CLOSED_WON. At scale with 2,050 institutions, 15–30% of deals may flow through channel partners, making this a strategically important revenue channel. The Channel Partner Manager uses this page to track partner health, onboard new partners, approve earned commissions, monitor deal attribution, and manage the full partner lifecycle from ONBOARDING through ACTIVE, SUSPENDED, or INACTIVE. The B2B Sales Manager has view access and the ability to approve commissions above 15% rate and high-value payouts. Sales Ops Analyst has read-only visibility across all partners and commission data.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Partner list | `sales_channel_partner` | 2 min |
| Deal attribution | `sales_channel_deal` JOIN `sales_lead` | 5 min |
| Commission ledger | `sales_channel_deal` filtered by `commission_status` | 2 min |
| Partner performance chart | Pre-aggregated analytics from Celery nightly task | 1 hour |
| Pending approvals panel | `sales_channel_deal` WHERE `commission_status='PENDING'` | 1 min |
| KPI strip aggregates | `sales_channel_partner` + `sales_channel_deal` aggregates | 2 min |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?status` | `all`, `active`, `onboarding`, `inactive`, `suspended` | `active` | Filter table by partner status |
| `?type` | `reseller`, `distributor`, `affiliate`, `referral` | — | Filter by partner_type |
| `?territory` | Territory string | — | Filter by partner territory |
| `?q` | String | — | ILIKE search on `partner_name`; 300ms debounce |
| `?page` | Integer | `1` | Pagination; 25 rows per page |

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/k/channel-partners/table/` | Partner table | Filter/page change | `#k-cp-table` |
| `htmx/k/channel-partners/approvals/` | Pending commissions panel | 1-min auto-refresh | `#k-cp-approvals` |
| `htmx/k/channel-partners/<id>/deals/` | Partner deal list (drawer) | Drawer open | `#k-cp-deals-{id}` |
| `htmx/k/channel-partners/<id>/ledger/` | Commission ledger (drawer) | After approval action | `#k-cp-ledger-{id}` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────┐
│  CHANNEL PARTNER PORTAL          [+ Onboard Partner]        │
├──────────┬──────────┬──────────┬──────────────────────────┤
│ Active   │ Total ARR│ Pending  │ Avg Commission           │
│ Partners │ Sourced  │ Approvals│ Rate                     │
│ 14       │ ₹1.8Cr   │ 3        │ 10.2%                   │
├──────────┴──────────┴──────────┴──────────────────────────┤
│  ⚠ 3 Commission Approvals Pending  [Review Now →]          │
├───────────────────────────────────────────────────────────┤
│  [Status▼] [Type▼] [Territory▼]  🔍 Search partner...    │
├─────────────┬──────┬─────────┬──────┬───────────┬────────┤
│ Partner     │ Type │ State   │Deals │ ARR       │Actions │
├─────────────┼──────┼─────────┼──────┼───────────┼────────┤
│ EduReach TS │ RES. │Telangana│  12  │ ₹42L      │ [···]  │
│ BrightPath  │ DIST.│Karnataka│   5  │ ₹18L      │ [···]  │
│ LearnLink   │ AFF. │AP       │   2  │  ₹6L      │ [···]  │
└─────────────┴──────┴─────────┴──────┴───────────┴────────┘
   Showing 1–14 of 14 active partners                ← 1 →
```

---

## Components

### 1. KPI Strip

```
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ 14               │ │ ₹1.8Cr           │ │ 3                │ │ 10.2%            │
│ Active Partners  │ │ Total ARR        │ │ Pending          │ │ Avg Commission   │
│ (status=ACTIVE)  │ │ Sourced          │ │ Approvals        │ │ Rate             │
│                  │ │                  │ │ ⚠ amber if >0    │ │ (ACTIVE partners)│
└──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘
```

- **Active Partners:** `COUNT(*) WHERE status='ACTIVE'`
- **Total ARR Sourced:** `SUM(total_arr_paise) WHERE status='ACTIVE'` — formatted ₹1.8Cr / ₹42L etc.
- **Pending Approvals:** `COUNT(*) FROM sales_channel_deal WHERE commission_status='PENDING'` — tile turns amber if count > 0
- **Avg Commission Rate:** `AVG(commission_rate_pct) WHERE status='ACTIVE'` — two decimal places, e.g. "10.2%"

HTMX 2-min auto-refresh. Tapping the Pending Approvals tile opens the Commission Approval Modal directly.

---

### 2. Pending Approvals Alert Bar

Displayed directly below the KPI strip only when `COUNT(sales_channel_deal WHERE commission_status='PENDING') > 0`.

```
┌─────────────────────────────────────────────────────────────────────┐
│  ⚠  3 commission approvals pending — ₹82,500 held   [Review Now →]  │
└─────────────────────────────────────────────────────────────────────┘
```

- Amber background bar. Text: "⚠ [N] commission approval[s] pending — ₹[total_commission_paise formatted] held."
- "Review Now →" link: opens Commission Approval Modal (Component 7).
- HTMX 1-min auto-refresh. Bar disappears automatically when all commissions cleared.
- Hidden entirely when no pending commissions exist.

---

### 3. Filter Bar

```
[Status ▼]  [Type ▼]  [Territory ▼]  [🔍 Search partner name...]  [Clear All]
```

- **Status:** Single-select dropdown — All / Active / Onboarding / Inactive / Suspended. Default: Active.
- **Type:** Multi-select — RESELLER / DISTRIBUTOR / AFFILIATE / REFERRAL. Each shows coloured badge preview.
- **Territory:** Multi-select dropdown populated from distinct `territory` values in `sales_channel_partner`.
- **Search:** ILIKE on `partner_name`; 300ms debounce triggers HTMX table reload.
- **Clear All:** Visible when any filter deviates from default. Resets all params.

---

### 4. Channel Partner Table

Sortable by partner name, total deals closed, total ARR sourced, last deal date. 25 rows per page.

| Column | Detail |
|---|---|
| Partner Name | Text; row click opens Partner Detail Drawer |
| Type badge | RESELLER=blue / DISTRIBUTOR=teal / AFFILIATE=amber / REFERRAL=grey |
| State | Short state name |
| Status badge | ACTIVE=green / ONBOARDING=indigo / INACTIVE=grey / SUSPENDED=red |
| Total Deals Closed | Integer from `total_deals_closed` field |
| Total ARR Sourced | `total_arr_paise` formatted (₹XL / ₹XCr) |
| Commission Balance | `commission_earned_paise - commission_paid_paise`; red text if any `commission_status='DISPUTED'` for this partner |
| Last Deal Date | `last_deal_at` formatted "12 Feb 2026"; "Never" in grey if no deals yet |
| Bank Account | Green "✓ Verified" or amber "⚠ Unverified" — turns red if unverified and there are commissions in APPROVED or PENDING status awaiting payout |
| Actions | 3-dot menu: View Details / Edit / Approve Commission / Suspend / Reactivate |

**Row states:**
- Amber row tint: partner has unverified bank account with pending payout
- Red row tint: partner is SUSPENDED

---

### 5. Onboard New Partner Drawer

Triggered by [+ Onboard Partner] button top right. Slide-in from right.

```
┌──────────────────────────────────────────────────────────────────┐
│  Onboard New Channel Partner                                     │
├──────────────────────────────────────────────────────────────────┤
│  Partner Name*          [________________________________]        │
│                         (checking for duplicates...)             │
│  Partner Type*          [RESELLER                       ▼]       │
│                         RESELLER / DISTRIBUTOR / AFFILIATE /     │
│                         REFERRAL                                 │
│  Primary Contact Name*  [________________________________]        │
│  Contact Phone*         [10-digit mobile               ]         │
│  Contact Email*         [email@domain.com              ]         │
│  Primary State*         [Telangana                     ▼]        │
│  Territory*             [TS — Hyderabad Zone           ]         │
│                         (auto-suggested by state; overridable)   │
│  Commission Rate %      [10.00]   (range: 5.00 – 25.00)         │
│                         ⚠ Rates above 15% require Sales Manager  │
│                         approval before partner is activated.    │
│  Bank Account Verified  [ ] (toggle after offline verification)  │
│  Notes                  [Additional context or referral source ] │
│                                                                  │
│  [Cancel]                          [Onboard Partner]            │
└──────────────────────────────────────────────────────────────────┘
```

**Validation rules:**
- Partner Name: required; min 3 chars; max 200 chars. On blur: API call `/htmx/k/channel-partners/check-name/` — warns "A partner with a similar name already exists: [Name]. Confirm to proceed."
- Partner Type: required.
- Contact Phone: 10-digit Indian mobile regex; rejects if non-numeric or wrong length.
- Contact Email: standard email validation.
- Primary State: required dropdown.
- Territory: auto-populated from state mapping; editable text field.
- Commission Rate: NUMERIC 5,2; min 5.00; max 25.00. If value > 15.00: shows inline warning and flags record for #57 approval before ACTIVE transition.
- Bank Account Verified: defaults unchecked. Cannot be checked programmatically — requires manual confirmation after offline bank verification.

**On submit:** POST to `/group1/k/channel-partners/create/`. Creates partner with `status='ONBOARDING'`. On success:
- Refreshes partner table and KPI strip via HTMX.
- Notification dispatched to #57 Sales Manager: "New channel partner onboarded: [Name] ([Type]) — Territory: [Territory]"
- If commission rate > 15%: additional approval-required notification to #57.
- Partner moves ONBOARDING → ACTIVE manually by the Manager after the first deal closes and bank account is verified.

---

### 6. Partner Detail Drawer

Opens on partner row click. Full-width right-side drawer with five tabs.

**Drawer header:**
```
EduReach TS — Telangana                                  [ACTIVE]
RESELLER  ·  Territory: TS — Hyderabad Zone  ·  Owner: Ravi Kumar
Commission Rate: 10%  ·  Total Deals: 12  ·  Total ARR: ₹42L
```

---

#### Tab a — Overview

Key stats card layout:

| Field | Value |
|---|---|
| Partner Type | RESELLER |
| Status | ACTIVE |
| Primary State | Telangana |
| Territory | TS — Hyderabad Zone |
| Contact Name | Suresh Patel |
| Contact Phone | +91 98765 43210 |
| Contact Email | suresh@edureachts.com |
| Commission Rate | 10.00% |
| Bank Account | ✓ Verified |
| Onboarded At | 12 Jan 2025 |

**Bank account verification protection:**
The `bank_account_verified` field can only be set to TRUE via the Django admin panel by Platform Admin (#10) after manual offline bank account confirmation. It cannot be set via the Sales module API endpoints — the Sales API serializer marks this field as read-only. This prevents bypass of the verification process.

When `bank_account_verified = False` and commission_status = APPROVED, the payout to the external payment system (Razorpay) is **blocked at the Billing module level** (Division M). Billing Admin (#70) sees "Payout blocked — bank account unverified" in their commission payout queue. Demo Manager or Channel Partner Manager cannot override this.

UI: In K-06 partner table, unverified partners with approved-but-unpaid commissions show a red "⚠ Verify bank account" badge. Clicking opens a tooltip: "Bank account verification required before payout. Contact Platform Admin to complete verification."
| Last Deal Closed | 8 Mar 2026 |
| Commission Earned | ₹4,20,000 |
| Commission Paid | ₹3,50,000 |
| Commission Balance | ₹70,000 |

[Edit Partner] button (Manager #63 only) → opens the same Onboard Partner form pre-filled with existing values. Commission rate edit above 15% re-triggers approval workflow.

**Commission rate change for active partners:**
When editing an active partner's commission_rate_pct to a value >15%:
- If previous rate was ≤15%: shows modal "Changing commission rate from [old]% to [new]% exceeds 15%. This requires Sales Manager approval. Submit for review?" [Submit] [Cancel].
- If submitted: partner record not updated immediately. A `sales_commission_rate_change_request` record created with: partner_id, requested_rate, requested_by, requested_at, status=PENDING.
- Sales Manager (#57) receives in-app + email notification. [Approve] / [Reject] buttons.
- On approval: partner commission_rate_pct updated. System sales activity logged: "Commission rate changed from [old]% to [new]% — approved by [Manager]."
- Pending rate changes shown in Partner Detail Drawer → Overview tab: "⚠ Rate change request pending approval ([new]%)."

---

#### Tab b — Deals

Table of all `sales_lead` records where `is_channel_deal=TRUE` AND `channel_partner_id=<this partner>`.

| Column | Detail |
|---|---|
| Institution Name | Link → K-03 Account Profile |
| Institution Type | SCHOOL / COLLEGE / COACHING badge |
| Stage | Current pipeline stage badge |
| ARR Estimate | `arr_estimate_paise` formatted |
| Won At | Date or "—" if not yet won |
| Commission Amount | `sales_channel_deal.commission_paise` formatted; "Pending" if deal not won |
| Commission Status | PENDING=amber / APPROVED=blue / PAID=green / DISPUTED=red |

Empty state: "No deals attributed to this partner yet."

Loaded via HTMX on tab open: `htmx/k/channel-partners/<id>/deals/`.

---

#### Tab c — Commission Ledger

Detailed `sales_channel_deal` rows for this partner. Loaded via `htmx/k/channel-partners/<id>/ledger/`.

| Column | Detail |
|---|---|
| Institution Name | From joined `sales_lead.institution_name` |
| Deal ARR | `sales_lead.arr_estimate_paise` formatted |
| Commission Amount | `commission_paise` formatted |
| Status | PENDING=amber / APPROVED=blue / PAID=green / DISPUTED=red |
| Approved By | User name or "—" |
| Approved At | Date or "—" |
| Paid At | Date or "—" |
| Actions | [Dispute] button (red, requires dispute reason text) — visible to #63 and #57 only |

**Commission workflow:**
1. Lead closes as CLOSED_WON → `commission_status` auto-set to PENDING
2. Channel Partner Manager or Sales Manager opens this ledger → clicks Approve (or uses Commission Approval Modal)
3. `commission_status` → APPROVED; `approved_by` = current user; `approved_at` = now()
4. Finance team (#70) processes bank transfer offline → marks PAID; `paid_at` = now()
5. Disputes: sets status = DISPUTED; dispute reason stored; notification to #57 and Finance

Note on Div-I integration: When a channel-partner-sourced deal (is_channel_deal=True) reaches CLOSED_WON, the same onboarding task creation applies as non-channel deals — Onboarding Specialist (#51, Div-I) receives both an in-app notification AND a task record is created in the support_onboarding_task table. Commission flow is separate from onboarding flow.

Ledger re-renders via HTMX after each approval or dispute action.

**Commission Dispute Resolution Workflow:**

1. **Raise dispute** — Channel Partner Manager (#63) or Sales Manager (#57) clicks "Dispute" on a commission row. Opens "Raise Dispute" modal requiring: dispute_reason (dropdown: WRONG_AMOUNT / WRONG_PARTNER / DUPLICATE_DEAL / NOT_OUR_DEAL / OTHER) + free-text explanation (required, min 20 chars). On submit: commission_status → DISPUTED. In-app + email notification to Sales Manager (#57).

2. **Review** — Sales Manager (#57) reviews the dispute. Opens the commission row's detail view showing: original deal, commission calculation, partner's claim, dispute reason. Actions: [Resolve — Keep Original Amount] / [Resolve — Adjust Amount] (allows entering corrected commission_paise) / [Reject Dispute — Commission Valid].

3. **Resolution outcomes:**
   - Resolve (keep/adjust): commission_status → APPROVED (with corrected amount if adjusted). Approved_by = Sales Manager. Notification to #63.
   - Reject dispute: commission_status reverts to PENDING for normal approval flow. Notification to #63 with rejection reason.

4. **Audit trail:** Every dispute action (raised, reviewed, resolved, rejected) is logged in a `sales_commission_dispute_log` table with: commission_id, action, actor_id, reason, created_at. Visible in the Commission Ledger tab as a collapsed "Dispute History" expandable row.

5. **Escalation:** Disputes unresolved >14 days trigger an alert to Platform COO (#3) via in-app notification.

---

#### Tab d — Performance Chart

Chart.js bar chart rendered from pre-aggregated analytics. No live query — 1-hour cache.

```
Deals Closed per Quarter (last 4 quarters)

     Q2 '25   Q3 '25   Q4 '25   Q1 '26
  6  ┤ █████   ██       ████     ████████
  4  ┤
  2  ┤
  0  ┴─────────────────────────────────
     ARR (₹L) line overlay ——————————
```

- Bar chart: deals closed per quarter (last 4 quarters)
- Line overlay: ARR sourced per quarter (secondary Y-axis on right)
- Both data series from `analytics_sales_funnel` filtered to `owner_id` of this partner's associated deals
- Tooltip: "Q1 2026 — 8 deals, ₹28L ARR"
- If fewer than 2 quarters of data: "Not enough data to display performance chart yet."

---

#### Tab e — Activity Log

Chronological log of interactions with this partner. Same format as K-03 activity timeline. Newest first.

```
● REVIEW_CALL   15 Mar 2026 · 11:00 AM   Ravi Kumar
  "Quarterly review call. Pipeline healthy — 3 leads in DEMO_DONE.
   Discussed Q2 target of 15 deals. Bank account re-verification pending."
  Next: Follow up on bank docs by 22 Mar

● ONBOARDING_SESSION   12 Jan 2025 · 10:00 AM   Ravi Kumar
  "Initial onboarding session. Walked through lead submission process,
   commission structure, and portal access setup."
```

Activity types: CALL / EMAIL / MEETING / ONBOARDING_SESSION / REVIEW_CALL

[+ Log Activity] button. Inline form collapses after save:

```
Type*       [CALL                  ▼]
Date/Time*  [2026-03-21]  [14:00  ]
Notes       [What happened?        ]
Next Action [Next step             ]  Due: [date]
[Save Activity]
```

HTMX retargets activity log section on save.

---

### 7. Commission Approval Modal

Opened via "Review Now →" in the Pending Approvals Alert Bar, or via KPI tile click, or via the 3-dot "Approve Commission" action on a partner row.

Shows all `sales_channel_deal` rows WHERE `commission_status='PENDING'` across all partners.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Commission Approvals (3 pending — ₹82,500 held)                             │
│  [Select All]  [Bulk Approve Selected ✓]                                     │
├─────────────┬──────────────────────┬────────┬──────┬───────────┬────────────┤
│ Partner     │ Institution          │ ARR    │ Rate │ Commission│ Days Pending│
├─────────────┼──────────────────────┼────────┼──────┼───────────┼────────────┤
│ EduReach TS │ Sunrise Public School│ ₹4.2L  │ 10%  │ ₹42,000   │ 5 days     │
│ BrightPath  │ MG College, Mysuru   │ ₹3.0L  │ 10%  │ ₹30,000   │ 3 days     │
│ LearnLink   │ BrainBox Coaching    │ ₹1.05L │ 10%  │ ₹10,500   │ 1 day      │
├─────────────┴──────────────────────┴────────┴──────┴───────────┴────────────┤
│  Row actions: [Approve ✓]  [Dispute ✗]                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Individual row actions:**
- **[Approve]:** Green button. Confirms "Approve ₹[amount] commission for [Partner] — [Institution]?" POST → `commission_status=APPROVED`, `approved_by=current_user`, `approved_at=now()`. Row removed from modal. Notification dispatched to #63 and Finance team (#70).
- **[Dispute]:** Red button. Opens inline reason text field (min 20 chars required). POST → `commission_status=DISPUTED`. Notification to #63 with dispute reason.

**Bulk approve:**
- Checkboxes on each row. "Select All" header checkbox.
- "Bulk Approve Selected" button with confirmation dialog: "Approve [N] commissions totalling ₹[amount]? This cannot be undone."
- Only #57 and #63 can approve. #95 Ops sees this modal read-only (no Approve/Dispute buttons).

---

## Empty States

| Condition | Message |
|---|---|
| No active partners | "No active channel partners. Onboard a partner to start sourcing deals through your reseller network." |
| No partners match current filters | "No partners match the current filters. Try clearing some filters." |
| No pending approvals | "All commissions are up to date. ✓" (shown in the approvals panel area) |
| No deals for partner (Deals tab) | "No deals attributed to this partner yet." |
| No ledger entries for partner (Ledger tab) | "No commission records for this partner yet." |
| No activity for partner (Activity tab) | "No activity logged for this partner yet." |
| Filter returns zero results | "No partners match the current filters." with [Clear All Filters] |

---

## Toast Messages

| Action | Toast |
|---|---|
| Partner onboarded | "Channel partner onboarded: [Name] — [Type]" (green) |
| Partner updated | "Partner updated: [Name]" (green) |
| Commission approved | "Commission of ₹[amount] approved for [Partner] — [Institution]" (green) |
| Bulk commissions approved | "[N] commissions approved totalling ₹[amount]" (green) |
| Commission disputed | "Commission disputed for [Partner] — [Institution]. Reason logged." (amber) |
| Partner suspended | "Partner [Name] has been suspended." (amber) |
| Partner reactivated | "Partner [Name] reactivated." (green) |
| Commission paid (Finance-triggered) | "Commission of ₹[amount] marked as paid for [Partner]." (green) |
| Duplicate name warning | "A partner with a similar name already exists. Review before submitting." (amber) |
| Commission rate approval required | "Commission rate above 15% — submitted to Sales Manager for approval." (blue) |
| Activity logged | "Activity logged for [Partner Name]" (green) |

---

---

## Authorization

**Route guard:** `@division_k_required(allowed_roles=[63, 57, 95])` applied to `ChannelPartnerView`.

| Scenario | Behaviour |
|---|---|
| Channel Partner Mgr (#63) | Full CRUD on channel partners, deals attribution, activity log |
| Sales Manager (#57) | Read all + approve/reject commissions. POST to onboard partner triggers approval workflow (not immediate activation). |
| Sales Ops (#95) | Read-only. All POST/PATCH/DELETE return 403. |
| Commission approval endpoint | POST `/k/channel-partners/commissions/<id>/approve/` — restricted to #57 only. Returns 403 for all others. |
| `bank_account_verified` PATCH | Not available in Sales API. Only Django admin (Platform Admin #10) can write this field. |
| Any other role | 403 Forbidden |

---

## Role-Based View Summary

| Feature | #57 Manager | #63 Channel Partner Mgr | #95 Ops Analyst | Others |
|---|---|---|---|---|
| View partner list | Full | Full | Read-only | No access |
| Onboard partner | Approve only | Full | No | No |
| Edit partner | Yes | Yes | No | No |
| View deal attribution | All partners | All partners | Read-only | No |
| Commission ledger | View + approve | View + raise dispute | Read-only | No |
| Commission approval | Yes | No | No | No |
| Raise commission dispute | Yes | Yes | No | No |
| Resolve commission dispute | Yes | No | No | No |
| Change commission rate | Approve >15% | Submit request | No | No |
| Suspend/reactivate partner | Yes | No | No | No |
| View performance chart | Yes | Yes | Yes (read) | No |
| Export partner data | Yes | Own partners | Yes | No |
