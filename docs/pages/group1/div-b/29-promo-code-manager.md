# 29 — Promo Code & Discount Manager

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Promo Code & Discount Manager |
| Route | `/product/promos/` |
| Django view | `PromoCodeManagerView` |
| Template | `product/promo_manager.html` |
| Priority | **P2** |
| Nav group | Product |
| Required roles | `pm_platform` · `superadmin` |
| All others | Read-only (can see active promos, not create/edit) |
| HTMX poll | None (on-demand config page) |
| Cache | Redis TTL 300s for promo validity lookups |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` |

---

## 2. Purpose & Business Logic

**The discount problem:**

EduForge's sales and BD teams regularly close deals with discount offers: "SCHOOL2026 — 20% off for the first year for all schools that sign up before March 31". Currently there is no platform-managed discount system — discounts are manually applied by Billing Admin (Division M) as one-off invoice adjustments, with no tracking, no expiry enforcement, no usage caps, and no analytics.

PM Platform owns the promotional strategy. This page gives PM Platform full control over:

1. **Promo Codes** — alphanumeric codes that institutions enter during sign-up or renewal to receive a discount
2. **Partner Discounts** — pre-negotiated % discount for specific partner channels (e.g., a school association MoU: all members get 15% off)
3. **Seasonal Offers** — time-bound flat discounts applied automatically to all new signups in a date window (no code required)
4. **Referral Credits** — institution A refers institution B; institution A gets ₹5,000 account credit

**Business rules:**
- Promo codes are case-insensitive, alphanumeric, 4–20 characters
- A single promo code can apply to: specific institution types, specific plans, specific states, or all
- Stacking: only one promo code per subscription (last applied wins; cannot stack two codes)
- Discount types: % off (e.g., 20%), flat ₹ off (e.g., ₹5,000/yr), extended trial (e.g., +30 days free)
- Codes are enforced at billing time — if code is expired when invoice generates, discount is NOT applied
- All applied discounts appear on the invoice line as "Promo: SCHOOL2026 — 20% discount applied"

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| PM Platform | All | Create, edit, deactivate promo codes |
| Superadmin | All | Same as PM Platform |
| All Division B (others) | Active promos list only | No create/edit |
| Division M (Billing Admin) | All | Can view only — actual billing adjustment is automatic |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Header & Summary Strip

```
Promo Code & Discount Manager                    [+ New Promo Code]  [Export CSV]
────────────────────────────────────────────────────────────────────────────────
Active Codes   Redemptions (MTD)   Revenue at Discount   Avg Discount %   Expiring <7d
    18             142                  ₹4.2 L                16.8%             3
```

- "Revenue at Discount" = sum of discount amounts applied this month across all active codes
- "Expiring <7d" → click filters table to those codes; amber if > 0

---

### Section 2 — Promo Code Table

```
PROMO CODES                [Status: All ▾]  [Type ▾]  [Institution Type ▾]  [Search...]
────────────────────────────────────────────────────────────────────────────────
Code           Type        Discount   Target            Uses   Cap    Expires      Status
────────────────┼───────────┼──────────┼─────────────────┼──────┼──────┼────────────┼──────
SCHOOL2026      % off       20%        Schools · All plans  84   500   31 Mar 2026  ✅ Active
NEET2026        % off       15%        All · Professional+  42   200   30 Jun 2026  ✅ Active
PARTNER-ASSOC   % off       25%        All · Enterprise     12   Unlimited  Never  ✅ Active
EARLYBIRD       Flat ₹      ₹10,000    Coaching · Any       8    50    15 Apr 2026  ✅ Active
TRIAL30         Free days   +30 days   New signup only      204  1000  31 Dec 2026  ✅ Active
EXPIRED2025     % off       10%        All                  312  —     31 Dec 2025  ❌ Expired
```

- Status filters: All / Active / Expired / Deactivated / Scheduled
- "Uses" = total redemptions to date
- "Cap" = max uses (Unlimited if not set)
- When Uses = Cap: status auto-changes to "Maxed Out" (shown as amber, not red)
- Click row → Promo Detail Drawer (Section 6)
- ⋯ menu: Edit / Deactivate / Duplicate / View Usage Log

---

### Section 3 — Partner Discounts

```
PARTNER DISCOUNTS                                                  [+ Add Partner Discount]
────────────────────────────────────────────────────────────────────────────────
Partner                   Discount   Institutions   Contract Expiry   Status
─────────────────────────┼──────────┼──────────────┼─────────────────┼──────
AP School Association     15% off    214 schools    31 Mar 2027       ✅ Active
Telangana Coaching MoU    20% off    48 coaching    30 Jun 2026       ✅ Active
CBSE Partner Prog.        10% off    122 schools    Perpetual          ✅ Active
```

- Partner discounts are applied automatically based on institution's partner affiliation tag — no code required
- "Institutions" = currently benefiting institutions
- Edit: change discount %, expiry date
- Cannot delete active partner discount if institutions are on it — must set expiry date

---

### Section 4 — Redemption Analytics

**Purpose:** PM Platform needs to understand which promos drive the most revenue, which codes are being used fraudulently, and which campaigns are ROI-positive.

```
REDEMPTION ANALYTICS — Last 90 Days
────────────────────────────────────────────────────────────────────────────────
[Bar chart: Chart.js — redemptions per code per month, stacked by institution type]

TOP CODES BY REDEMPTION
Code            Redemptions   Revenue Lost   New Institutions Added   Net ARR Impact
────────────────┼─────────────┼──────────────┼────────────────────────┼──────────────
TRIAL30          204           ₹0 (free trial) 38 converted to paid     ₹7.8L ARR
SCHOOL2026        84          ₹1.2L           84 new institutions       ₹12.6L ARR

Conversion Rate: TRIAL30 → paid: 38 / 204 = 18.6%  (target: > 20%)
```

---

### Section 5 — Scheduled Promos

```
UPCOMING / SCHEDULED PROMOS
────────────────────────────────────────────────────────────────────────────────
Code              Starts        Ends         Discount   Target       Status
────────────────┼─────────────┼────────────┼──────────┼─────────────┼──────────
APRIL2026         01 Apr 2026   30 Apr 2026   25% off    All          ⏰ Scheduled
SUMMER2026        01 May 2026   31 Jul 2026   15% off    Schools       ⏰ Scheduled
```

- Scheduled promos auto-activate at midnight IST on start date
- Celery beat task: `activate_scheduled_promos()` runs at 00:05 IST daily

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Promo Code & Discount Manager                        [+ New Promo] [CSV]   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Active: 18  |  MTD Redemptions: 142  |  Revenue at Discount: ₹4.2L       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  PROMO CODE TABLE                                                           ║
║  SCHOOL2026  20% off  Schools  84/500 uses  Expires 31 Mar ✅              ║
║  TRIAL30     +30 days  All    204/1000     Expires 31 Dec ✅               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  PARTNER DISCOUNTS                                                          ║
║  AP School Assoc: 15% off · 214 institutions · Expires Mar 2027 ✅         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  REDEMPTION ANALYTICS — [Chart: redemptions/month per code]                 ║
║  TRIAL30: 204 redemptions · 18.6% conversion                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Promo Detail Drawer (560px)

Triggered by clicking any promo row.

```
SCHOOL2026 — 20% off for Schools
────────────────────────────────────────────────────────────────────────────────
Status: ✅ Active   Created by: @pm_platform_1   Created: 01 Jan 2026

CONFIGURATION
Discount type:    % off
Discount value:   20%
Applies to:       Schools (all plan tiers)
Max uses:         500   (84 used, 416 remaining)
Expiry:           31 Mar 2026 23:59 IST
Min plan:         Any
Stackable:        No

USAGE LOG (last 10)
Sunrise Academy     20 Jan 2026  ₹3,000 off  New subscription
Delhi Model School  22 Jan 2026  ₹3,600 off  New subscription
…

[Edit]  [Deactivate]  [Duplicate]  [View All Usage →]
```

---

## 7. Create/Edit Promo Modal (640px)

```
Create Promo Code
────────────────────────────────────────────────────────────────────────────────
Code *            [SCHOOL2026          ] (auto-generate [🎲])
Type *            [% Discount ▾]   (% Discount / Flat ₹ / Free Trial Days)
Value *           [20     ] %
Description *     [For schools joining before March 31, 2026          ]

TARGETING
Institution type  [☑ Schools  ☐ Colleges  ☐ Coaching  ☐ All]
Min plan          [Any ▾]
State (optional)  [All states ▾]

LIMITS
Max uses          [500     ]   (leave blank = unlimited)
Max per inst.     [1       ]   (max times one institution can use this code)
Stackable         [☐ Allow stacking with other codes]

SCHEDULE
Start date        [01 Jan 2026]   Start time  [00:00 IST]
Expiry date       [31 Mar 2026]   Expiry time [23:59 IST]
                  ☐ Never expires

PREVIEW
Code SCHOOL2026 will give schools 20% off their first invoice.
Example: School on Standard plan (₹30,000/yr) → saves ₹6,000.
────────────────────────────────────────────────────────────────────────────────
[Cancel]                                              [Save Draft]  [Activate]
```

- "Activate" requires confirmation: "This code will be immediately usable. Confirm?"
- Free Trial Days type: additional fields "Trial days" + "Applies to: New signup only / Any renewal"
- Code uniqueness: validated on blur against existing codes (case-insensitive)

---

## 8. HTMX Architecture

| `?part=` | Target | Trigger |
|---|---|---|
| `summary` | `#promo-summary` | load |
| `codes` | `#promo-table` | load + filter change |
| `partners` | `#partner-discounts` | load |
| `analytics` | `#promo-analytics` | load |
| `scheduled` | `#scheduled-promos` | load |
| `promo-drawer` | `#drawer-container` | row click |

---

## 9. Backend View & API

```python
class PromoCodeManagerView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_promo_codes"

    def get(self, request):
        can_manage = request.user.role in {"pm_platform","superadmin"}
        if _is_htmx(request):
            part = request.GET.get("part","")
            dispatch = {
                "summary":       "product/promos/partials/summary.html",
                "codes":         "product/promos/partials/codes_table.html",
                "partners":      "product/promos/partials/partners.html",
                "analytics":     "product/promos/partials/analytics.html",
                "scheduled":     "product/promos/partials/scheduled.html",
                "promo-drawer":  "product/promos/partials/promo_drawer.html",
            }
            if part in dispatch:
                ctx = self._build_ctx(request, can_manage)
                return render(request, dispatch[part], ctx)
        ctx = self._build_ctx(request, can_manage)
        return render(request, "product/promo_manager.html", ctx)

    def post(self, request):
        if request.user.role not in {"pm_platform","superadmin"}:
            return HttpResponseForbidden()
        action = request.POST.get("action","")
        handlers = {
            "create": self._handle_create,
            "update": self._handle_update,
            "deactivate": self._handle_deactivate,
        }
        if action in handlers:
            return handlers[action](request)
        return HttpResponseBadRequest()
```

**Promo validation at billing time (called from billing module, not this view):**
```python
def validate_promo_code(code: str, institution, plan) -> dict:
    """Returns {valid, discount_type, discount_value, reason}"""
    r = get_redis_connection()
    cache_key = f"promo:valid:{code.upper()}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    try:
        promo = PromoCode.objects.get(code__iexact=code, status="active")
    except PromoCode.DoesNotExist:
        return {"valid": False, "reason": "Code not found or expired"}
    if promo.expiry_at and promo.expiry_at < now():
        return {"valid": False, "reason": "Code has expired"}
    if promo.max_uses and promo.uses_count >= promo.max_uses:
        return {"valid": False, "reason": "Code usage limit reached"}
    if promo.institution_type and institution.type not in promo.institution_type:
        return {"valid": False, "reason": "Code not valid for this institution type"}
    result = {"valid": True, "discount_type": promo.discount_type,
              "discount_value": promo.discount_value}
    r.setex(cache_key, 300, json.dumps(result))
    return result
```

---

## 10. Database Schema

```python
class PromoCode(models.Model):
    DISCOUNT_TYPES = [("pct","Percentage"),("flat","Flat ₹"),("trial_days","Free Trial Days")]
    STATUS = [("draft","Draft"),("active","Active"),("deactivated","Deactivated"),("expired","Expired")]

    code              = models.CharField(max_length=20, unique=True, db_index=True)
    description       = models.TextField()
    discount_type     = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value    = models.DecimalField(max_digits=10, decimal_places=2)
    institution_type  = models.JSONField(default=list)  # ["school","college"] or [] = all
    min_plan          = models.CharField(max_length=20, blank=True)  # "" = any
    target_states     = models.JSONField(default=list)  # [] = all states
    max_uses          = models.IntegerField(null=True)   # null = unlimited
    max_per_inst      = models.IntegerField(default=1)
    stackable         = models.BooleanField(default=False)
    starts_at         = models.DateTimeField()
    expiry_at         = models.DateTimeField(null=True)  # null = never expires
    status            = models.CharField(max_length=20, choices=STATUS, db_index=True)
    uses_count        = models.IntegerField(default=0)   # denormalised counter
    created_by        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at        = models.DateTimeField(auto_now_add=True)


class PromoRedemption(models.Model):
    promo             = models.ForeignKey(PromoCode, on_delete=models.PROTECT,
                                           related_name="redemptions")
    institution       = models.ForeignKey("Institution", on_delete=models.PROTECT)
    invoice           = models.ForeignKey("Invoice", null=True, on_delete=models.SET_NULL)
    discount_amt_inr  = models.DecimalField(max_digits=12, decimal_places=2)
    redeemed_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("promo","institution")  # max_per_inst=1 enforced here


class PartnerDiscount(models.Model):
    partner_name      = models.CharField(max_length=200)
    partner_slug      = models.CharField(max_length=50, unique=True)
    discount_pct      = models.DecimalField(max_digits=5, decimal_places=2)
    contract_expiry   = models.DateField(null=True)  # null = perpetual
    is_active         = models.BooleanField(default=True)
    institutions      = models.ManyToManyField("Institution", blank=True,
                                                related_name="partner_discounts")
    created_by        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
```

---

## 11. Validation Rules

| Action | Validation |
|---|---|
| Create code | Code unique (case-insensitive), 4–20 alphanumeric chars, no spaces |
| Discount % | 1%–99% only |
| Flat ₹ | Max ₹1,00,000; cannot exceed plan price |
| Trial days | 7–90 days |
| Expiry date | Must be ≥ today + 1 day |
| Max uses | 1–100,000 |
| Deactivate | Cannot deactivate if Billing has in-progress invoice applying this code |
| Edit active code | Can change expiry, max_uses (if new cap > current uses), description only — cannot change discount % on active code |

---

## 12. Security Considerations

- Promo codes visible to all internal users — codes themselves are not secret (institutions type them)
- Revenue discount data: accessible to all div-b + div-m; discount amount per institution visible only to PM Platform + Billing Admin
- Rate limiting on promo validation API: 10 attempts/min per institution to prevent brute-force code guessing
- Audit log: every create/edit/deactivate logged with old/new values
- Partner discount affiliations: institution's partner tag set by Sales team (div-k) — PM Platform cannot arbitrarily assign institutions to partner discounts

---

## 13. Edge Cases

| State | Behaviour |
|---|---|
| Code reaches max_uses at billing time | Validation returns invalid; institution not charged; support ticket auto-created for ops to investigate |
| Two institutions apply code simultaneously at cap | Redis atomic INCR check: first succeeds, second gets "Code just expired" error |
| Partner discount + promo code both applicable | Partner discount takes precedence (stackable=false); promo code rejected with message "Partner discount already applied" |
| Promo code applied to renewal (not new signup) | Depends on `applies_to` field; if "new signup only" — rejected at billing with clear message on invoice |

---

*Last updated: 2026-03-20*
