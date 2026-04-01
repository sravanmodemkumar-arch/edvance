# 04 — Plan & Pricing Config

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Active subscription plans | 4 tiers: Starter · Standard · Professional · Enterprise |
| Total institutions on plans | 2,050 |
| Schools on Starter/Standard | ~850 (avg ₹18K/yr ARR) |
| Colleges on Standard/Professional | ~680 (avg ₹35K/yr ARR) |
| Coaching on Professional/Enterprise | ~90 (avg ₹1.5L/yr ARR · ₹15 Cr ARR total) |
| Add-ons active | ~12 add-on SKUs |
| Plan changes per month | ~30–50 upgrades/downgrades |
| Total ARR | ~₹XX Cr |
| GST rate | 18% (SAC 9993) |
| Proration model | Daily proration on mid-cycle upgrades |
| Currency | INR only (DPDPA §16 — India data residency) |

**Why this page matters at scale:** Plan config directly controls what 2,050 institutions can do. A misconfigured plan limit (e.g., student count cap set too low) silently breaks institution workflows for thousands of students. A pricing error affects revenue recognition. Every change must be 2FA-gated, previewed before publish, and rolled out without disrupting active billing cycles. The PM Platform owns this page exclusively — billing team (Division M) sees invoices, not plan definitions.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Plan & Pricing Config |
| Route | `/product/plan-config/` |
| Django view class | `PlanConfigView` |
| Template | `product/plan_config.html` |
| Permission — view | `portal.view_plan_config` (all div-b roles read-only) |
| Permission — edit | `portal.edit_plan_config` (PM Platform only) |
| Permission — publish | `portal.publish_plan_config` (PM Platform + 2FA) |
| 2FA required | Yes — publish any plan change, price change, limit change |
| HTMX poll | None (on-demand only — plan config is not real-time) |
| Nav group | Product |
| Nav icon | `credit-card` |
| Priority | P1 |

---

## 3. Wireframe

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Plan & Pricing Config          [+ New Plan]  [Export Matrix]  [Audit Log]  │
├────────┬────────┬────────┬────────────────────────────────────────────────────────┤
│ Active │ Insti- │ Total  │ Pending Changes                                        │
│ Plans  │ tutions│  ARR   │  3 changes staged, not yet published ⚠                │
│   4    │  2,050 │ ₹XXCr  │  [Publish All Changes] [Discard Changes]              │
├────────┴────────┴────────┴────────────────────────────────────────────────────────┤
│ TABS: [Plan Catalog] [Feature Matrix] [Limits Config] [Add-ons] [Plan History]    │
├────────────────────────────────────────────────────────────────────────────────────┤
│ TAB: PLAN CATALOG                                                                  │
│                                                                                    │
│  ┌─ STARTER ──────────┐  ┌─ STANDARD ─────────┐  ┌─ PROFESSIONAL ─────┐  ┌─ ENTERPRISE ──────┐│
│  │ ₹15,000/yr         │  │ ₹30,000/yr          │  │ ₹75,000/yr         │  │ Custom pricing    ││
│  │ 620 institutions   │  │ 840 institutions    │  │ 410 institutions   │  │ 180 institutions  ││
│  │ ₹9.3 Cr ARR        │  │ ₹25.2 Cr ARR        │  │ ₹30.75 Cr ARR      │  │ ₹XXCr ARR         ││
│  │ [Edit] [Preview]   │  │ [Edit] [Preview]    │  │ [Edit] [Preview]   │  │ [Edit] [Preview]  ││
│  └────────────────────┘  └────────────────────┘  └────────────────────┘  └────────────────────┘│
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

**Container:** `flex gap-4 p-4` · 4 cards + 1 wide staged-changes banner

| # | Card | Value | Alert |
|---|---|---|---|
| 1 | Active Plans | `4` | — |
| 2 | Institutions | `2,050` | — |
| 3 | Total ARR | `₹XX Cr` (Decimal · never float) | — |
| 4 | Pending Changes | `3 staged` | Any staged = amber pulsing |

**Pending changes banner** (shown when staged count > 0):
`bg-[#451A03] border border-[#F59E0B] rounded-xl px-6 py-3 flex justify-between items-center`
Left: `⚠ 3 plan changes are staged but not yet published. Institutions will not see changes until published.`
Right: [Publish All Changes] `bg-[#6366F1]` · [Discard Changes] `text-[#F87171]`
Both require 2FA.

---

### 4.2 Tab Bar

| Tab | hx-get | Description |
|---|---|---|
| Plan Catalog | `?part=catalog` | 4 plan cards with pricing, institution count, ARR |
| Feature Matrix | `?part=matrix` | 80+ features × 4 plans entitlement grid |
| Limits Config | `?part=limits` | Student caps, exam limits, storage limits per plan |
| Add-ons | `?part=addons` | 12 add-on SKUs — pricing, availability per plan |
| Plan History | `?part=history` | Audit log of all plan changes with diff viewer |

---

### 4.3 Tab: Plan Catalog

**Layout:** `grid grid-cols-4 gap-4 p-4`

#### 4.3.1 Plan Card

`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-5`
**Staged changes indicator:** `border-[#F59E0B]` + amber dot in top-right corner

**Card sections:**

**Header:**
```
Plan Name (editable)          [Edit button — pencil icon]
Plan Tier badge
```

**Pricing block:**
```
₹ [price] / yr          ← Decimal field, editable
₹ [monthly_equiv] / mo  ← auto-computed: annual / 12
GST (18%): ₹ [gst]     ← auto-computed
Total incl. GST: ₹ [total] ← auto-computed
```
All monetary values: `Decimal(10,2)` — never float
Edited values show amber indicator: `text-[#FCD34D]` until published

**Discount section:**
```
Annual discount vs monthly: [X]%
Custom discount rules:
  ├─ Group institutions: [Y]% discount
  └─ 3-yr commitment: [Z]% discount
```

**Institution count block:**
```
Current: [N] institutions  [sparkline — 12mo trend]
MRR contribution: ₹ [N]
ARR contribution: ₹ [N]
```
Count is read-only — from live DB

**Upgrade/Downgrade rules:**
```
Can upgrade to: Professional · Enterprise
Can downgrade to: (none — Starter is base)
Downgrade restriction: [  ] Allow immediate · [○] Allow at renewal only
Proration: Daily proration on upgrade · No refund on downgrade
```

**[Edit Plan]:** opens Plan Edit Drawer (640px)
**[Preview]:** opens Plan Preview Modal — shows how the plan looks to institutions

---

#### 4.3.2 Plan Comparison Summary

Below the 4 cards:
`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4`

**3 columns:**
- Pricing table (annual): comparison row `₹15K · ₹30K · ₹75K · Custom`
- Institution count: `620 · 840 · 410 · 180`
- Revenue contribution %: donut visual `text-xs`

**Upgrade flow diagram** (SVG arrows):
```
Starter → Standard → Professional → Enterprise
  ↗ (any plan can also go straight to Enterprise)
```

---

### 4.4 Tab: Feature Matrix

**Purpose:** Define which of 80+ features each plan tier is entitled to. This is the most complex and highest-impact config surface — wrong entitlements silently break institution workflows.

#### 4.4.1 Matrix Toolbar

| Control | Type | Options |
|---|---|---|
| Search features | Text · debounce 300ms | Feature name search |
| Category | Multi-select | Exam · Content · Analytics · Communication · Billing · Administration · AI · API |
| Show only differences | Toggle | Hides rows where all 4 plans have same value |
| Edit mode | Toggle | `[ ] Edit Mode` — enable to make changes |

**Edit mode toggle:**
Default: read-only (all checkboxes disabled · `opacity-60 cursor-not-allowed`)
Edit mode: checkboxes active · unsaved changes tracked
Activating edit mode: `bg-[#451A03] border border-[#F59E0B] rounded p-2`
"You are now in edit mode. Changes are staged until published."

#### 4.4.2 Feature Matrix Table

**Layout:** `w-full` · sticky header + sticky plan columns

**Table header:**
```
Feature Name          │ Category  │ Starter │ Standard │ Professional │ Enterprise │
```
Column widths: Feature Name 280px · Category 120px · Plan columns 100px each

**Plan header cells (sticky):**
`bg-[#0D1526] border-b-2 border-[#6366F1]`
Institution count below plan name: `text-xs text-[#94A3B8]`

**Feature groups (collapsible):**
`<tr class="bg-[#131F38]">` group header row with expand/collapse chevron
Group name: `text-xs font-semibold uppercase tracking-wider text-[#94A3B8]`

**Feature row:**
`hover:bg-[#131F38]` · `border-b border-[#1E2D4A]`

Feature name cell:
- Feature name: `text-sm text-[#F1F5F9]`
- Description tooltip: `ⓘ` icon — hover shows description
- `[NEW]` badge: `bg-[#312E81] text-[#A5B4FC] text-[10px]` for recently added features
- `[BETA]` badge: `bg-[#451A03] text-[#FCD34D] text-[10px]`

Entitlement cells:
- ✓ Included: `text-[#34D399]` checkmark · `bg-[#064E3B]/20`
- ✗ Not included: `text-[#F87171]` × · `bg-transparent`
- `~` Partial / addon required: `text-[#FCD34D]` ~ · tooltip "Available as add-on"
- In edit mode: checkbox replaces icon · `accent-[#6366F1]`

**Staged change highlight:**
Changed cells: `bg-[#1A1000] border border-[#F59E0B]` + amber dot overlay

**Sample feature rows:**

| Feature | Category | Starter | Standard | Pro | Enterprise |
|---|---|---|---|---|---|
| Student enrollment | Administration | ✓ | ✓ | ✓ | ✓ |
| Exam creation | Exam | ✓ | ✓ | ✓ | ✓ |
| Live exam monitoring | Exam | ✗ | ✓ | ✓ | ✓ |
| AI MCQ generation | AI | ✗ | ✗ | ✓ | ✓ |
| Proctoring (AI) | Exam | ✗ | ✗ | ✓ | ✓ |
| Custom branding | Administration | ✗ | ✗ | ✓ | ✓ |
| WhatsApp notifications | Communication | ✗ | ✓ | ✓ | ✓ |
| API access | API | ✗ | ✗ | ✓ | ✓ |
| Dedicated support | Administration | ✗ | ✗ | ✗ | ✓ |
| Custom integrations | API | ✗ | ✗ | ✗ | ✓ |
| SLA 99.9% | Administration | ✗ | ✗ | ✗ | ✓ |
| Batch export (PDF) | Analytics | ✗ | ✓ | ✓ | ✓ |
| Student analytics | Analytics | ✗ | ✗ | ✓ | ✓ |

(Total: 80+ feature rows across 8 categories)

**Dependency warnings (inline):**
If a feature is unchecked but its dependency is checked:
`text-[#F87171] text-xs` below feature name: "⚠ Requires 'Live exam monitoring' which is unchecked for this plan"

**Bulk actions (in edit mode):**
- Select column (plan): [Enable all for Standard] [Disable all for Starter]
- Select row range: multi-select with Shift+click

---

### 4.5 Tab: Limits Config

**Purpose:** Define per-plan numeric limits — student cap, exam count, storage, API calls, concurrent users, etc. These are enforced server-side.

#### 4.5.1 Limits Table

| Limit | Starter | Standard | Professional | Enterprise |
|---|---|---|---|---|
| Max students per institution | 500 | 2,000 | 10,000 | Unlimited |
| Max exams per month | 10 | 50 | 200 | Unlimited |
| Max questions in bank | 500 | 5,000 | 50,000 | Unlimited |
| Max concurrent exam users | 100 | 500 | 5,000 | 15,000 |
| Storage (media/docs) | 5 GB | 25 GB | 100 GB | 1 TB |
| API calls per day | 0 | 0 | 10,000 | 100,000 |
| Staff accounts | 10 | 50 | 200 | Unlimited |
| WhatsApp messages/month | 0 | 500 | 5,000 | Unlimited |
| SMS per month | 0 | 200 | 2,000 | Unlimited |
| Result export (PDF batch) | ✗ | 500 students | 5,000 students | Unlimited |
| Data retention | 1 year | 3 years | 7 years | Custom |

**Each cell in edit mode:**
- `input[type=number]` · min=0 · `bg-[#131F38] border border-[#1E2D4A]`
- `0` = disabled · `-1` = unlimited
- "Unlimited" radio toggle: `[○ Set limit] [○ Unlimited]`

**Staged change indicator:** amber highlight on changed cells

**Current usage context panel (below table):**
For each limit, shows "highest actual usage vs limit":
`Coaching Centres: peak 14,800 concurrent users vs Enterprise limit 15,000 (98.7%)`
`bg-[#451A03] border border-[#F59E0B]` — amber warning when any institution is within 10% of limit

**Limit breach simulation:**
[Simulate Impact] button: shows how many institutions would breach limits if a limit is lowered
`hx-get="?part=limit_simulation&limit={key}&value={new_val}"` inline results

---

### 4.6 Tab: Add-ons

**Purpose:** 12 optional add-on SKUs that institutions can purchase on top of their plan.

#### 4.6.1 Add-on Cards Grid

`grid grid-cols-3 gap-4 p-4`

Each add-on card: `bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4`

**Card content:**
```
[Add-on Icon]  Add-on Name                [Active badge if sold]
               Description (2 lines max)

Pricing:  ₹ [price] / yr  (+ 18% GST)
Available to: [Starter ✗] [Standard ✓] [Professional ✓] [Enterprise ✓]
Current subscribers: [N] institutions
ARR from this add-on: ₹ [N]

[Edit Add-on] [Preview]
```

**Add-on examples:**

| Add-on | Price/yr | Available from | Description |
|---|---|---|---|
| AI MCQ Pack (500/mo) | ₹10,000 | Standard+ | AI-generated MCQs via Gemini API |
| Extra Storage (100 GB) | ₹5,000 | Starter+ | Additional media/document storage |
| WhatsApp Business | ₹8,000 | Standard+ | Enhanced WhatsApp with templates |
| Proctoring (AI) | ₹25,000 | Professional+ | AI-based exam proctoring |
| Custom Branding | ₹15,000 | Standard+ | White-label portal with custom domain |
| Priority Support | ₹20,000 | Standard+ | SLA 4h response (vs standard 24h) |
| Parent Portal | ₹6,000 | Starter+ | Parent login for student progress |
| Advanced Analytics | ₹12,000 | Standard+ | Cohort analysis, predictive dropout |
| API Access (Basic) | ₹18,000 | Professional+ | REST API 10K calls/day |
| Bulk SMS Pack (5,000/mo) | ₹4,000 | Starter+ | Additional SMS beyond plan limit |
| Video Library (YouTube) | ₹7,000 | Starter+ | Curated video playlists per subject |
| NEET/JEE Test Series | ₹30,000 | Starter+ | Access to national-level test series |

**[+ New Add-on]** button: opens Add-on Create Modal

---

### 4.7 Tab: Plan History

**Purpose:** Full audit trail of all plan changes with diff viewer.

#### 4.7.1 Filters

Date range · Changed by · Plan affected · Change type (price/feature/limit/addon)

#### 4.7.2 History Table

| Column | Detail |
|---|---|
| Timestamp | Absolute datetime |
| Changed By | Staff name |
| Plan | Plan name badge |
| Change Type | Price · Feature · Limit · Add-on · New Plan |
| Summary | e.g., "Raised student limit from 8,000 to 10,000 for Professional" |
| Staged → Published | Yes/No — if staged, when published |
| 2FA Verified | ✅ Yes (always for published changes) |
| Actions | [View Diff] [Revert] |

**[View Diff]** opens Plan History Diff Drawer (480px):
Two-column diff view showing before/after values in red/green highlights

**[Revert]:** creates a new staged change to revert to previous values (does not auto-publish — requires 2FA publish)

---

## 5. Drawers

### 5.1 Plan Edit Drawer (640px)

**Trigger:** [Edit] on plan card or [Edit Plan] in catalog
**Header:** Plan name + Tier badge + `[×]`

**Tab bar (4 tabs):**

---

#### Tab A — Pricing

**Fields:**

| Field | Type | Validation |
|---|---|---|
| Plan Display Name | Text | Required · max 40 chars |
| Annual Price (₹) | Decimal input | Required · min ₹0 · `Decimal(10,2)` |
| Monthly Price (₹) | Decimal input | Optional · if blank = annual/12 |
| GST Rate | Read-only display | Always 18% (SAC 9993) — not editable |
| GST Amount | Auto-computed display | |
| Price incl. GST | Auto-computed display | |
| Group discount % | Number 0–100 | For institution groups |
| 3-year commitment discount % | Number 0–100 | |
| Trial period (days) | Number 0–90 | 0 = no trial |
| Trial restrictions | Multi-select | Features disabled during trial |

**Live pricing preview** (right column):
```
₹ 75,000 /yr (excl. GST)
+ ₹ 13,500 GST (18%)
= ₹ 88,500 /yr (incl. GST)

Monthly equivalent: ₹ 6,250/mo
Daily rate: ₹ 205.48/day (for proration)
```

All computed in Python Decimal server-side — preview fetched via `hx-get="?part=pricing_preview"`

---

#### Tab B — Features

Same matrix as §4.4.2 but scoped to this one plan column.
Shows all 80+ features with toggle for this plan.
Dependency chain validated server-side on save.

---

#### Tab C — Limits

Same as §4.5.1 but editable form for this one plan column.

---

#### Tab D — Preview

**Render how this plan looks in the institution's subscription page:**
- Plan card as institutions see it
- Feature list rendered (only enabled features shown)
- Pricing block
- Compare with adjacent plans (left/right arrows)

**[Send Preview to Test Institution]** — sends preview to a designated test institution's admin email

---

**Drawer footer:**
- Left: [Delete Plan] `text-[#F87171]` (disabled if > 0 subscribers)
- Right: [Save as Draft] · [Publish Changes] `bg-[#6366F1]` (2FA required)

**Staged changes flow:**
1. User edits fields → changes tracked in `PlanStagedChange` model
2. [Save as Draft] → saves to staged, not live
3. [Publish Changes] → 2FA prompt → server validates → applies to live plan → audit log entry

---

## 6. Modals

### 6.1 Publish Changes Modal

**Trigger:** [Publish All Changes] in staged banner or [Publish Changes] in drawer
**Width:** 560px

**Staged changes summary:**
Each change listed with before → after:
```
Professional · Annual Price: ₹70,000 → ₹75,000
Standard · Feature: AI MCQ Generation  ✗ → ✓
Starter · Student Limit: 400 → 500
```

**Impact assessment:**
- Institutions affected: `1,250` (Standard + Professional subscribers)
- ARR impact: `+₹X.XX L` (price increase)
- Billing cycle impact: "Price changes take effect on next renewal. Current subscribers not affected mid-cycle."
- Feature changes: "Feature 'AI MCQ Generation' will be available to 840 Standard institutions immediately after publish."

**2FA verification:** `input placeholder="Enter 6-digit code"`

**Effective date options:**
- `[○] Immediately` — features available now
- `[○] On next billing cycle` — pricing changes only
- `[○] Scheduled: [date picker]`

**Footer:** [Confirm & Publish] `bg-[#6366F1]` · [Cancel]

---

### 6.2 Discard Changes Modal

**Trigger:** [Discard Changes] in staged banner
**Width:** 400px

"Are you sure? All {N} staged changes will be permanently discarded."
[Yes, Discard All] `bg-[#EF4444]` · [Cancel]

---

### 6.3 Limit Breach Simulation Modal

**Trigger:** [Simulate Impact] in Limits Config
**Width:** 560px

Shows table: "If [Limit] is changed from [X] to [Y]:"
| Institution | Current Usage | Would Breach? |
|---|---|---|
| SR Coaching Centre | 14,800 students | ✅ OK (under new 15K limit) |
| VR Academy | 12,400 students | ❌ Would exceed new 10K limit |

Institutions that would breach: highlighted red
[Export Breach List] · [Cancel]

---

### 6.4 New Plan Modal

**Trigger:** [+ New Plan] header button
**Width:** 560px

Fields: Plan name · Tier position (1–10) · Annual price · Based on (copy from existing plan) · Initial status (Draft / Active)

Note: new plans start as Draft · do not appear to institutions until Published

---

## 7. Django View

```python
class PlanConfigView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_plan_config"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":               "product/partials/plans_kpi.html",
                "catalog":           "product/partials/plans_catalog.html",
                "matrix":            "product/partials/plans_matrix.html",
                "limits":            "product/partials/plans_limits.html",
                "addons":            "product/partials/plans_addons.html",
                "history":           "product/partials/plans_history.html",
                "plan_drawer":       "product/partials/plan_drawer.html",
                "pricing_preview":   "product/partials/pricing_preview.html",
                "limit_simulation":  "product/partials/limit_simulation.html",
                "plan_diff":         "product/partials/plan_diff.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "product/plan_config.html", ctx)

    def post(self, request):
        action = request.POST.get("action")

        if action in {"publish_changes", "create_plan", "delete_plan"}:
            if not request.session.get("2fa_verified"):
                return JsonResponse({"error": "2FA required"}, status=403)
        if not request.user.has_perm("portal.edit_plan_config"):
            return JsonResponse({"error": "Permission denied"}, status=403)

        dispatch = {
            "save_draft":         self._save_draft,
            "publish_changes":    self._publish_changes,
            "discard_changes":    self._discard_changes,
            "create_plan":        self._create_plan,
            "delete_plan":        self._delete_plan,
            "update_feature":     self._update_feature,
            "update_limit":       self._update_limit,
            "create_addon":       self._create_addon,
            "update_addon":       self._update_addon,
            "revert_change":      self._revert_change,
        }
        handler = dispatch.get(action)
        if handler:
            return handler(request)
        return JsonResponse({"error": "Unknown action"}, status=400)

    def _publish_changes(self, request):
        from portal.apps.product.models import PlanStagedChange
        from decimal import Decimal
        staged = PlanStagedChange.objects.filter(published=False)
        for change in staged:
            change.apply()  # atomically updates live plan
            change.published = True
            change.published_by = request.user
            change.save()
        # Write to audit log
        self._write_audit(request, "published_plan_changes", count=staged.count())
        return JsonResponse({"success": True, "count": staged.count()})
```

---

## 8. Data Model Reference

```python
class SubscriptionPlan(models.Model):
    TIER_CHOICES = [
        ("starter", "Starter"),
        ("standard", "Standard"),
        ("professional", "Professional"),
        ("enterprise", "Enterprise"),
    ]
    name            = models.CharField(max_length=40)
    tier            = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True)
    annual_price    = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_price   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gst_rate        = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("18.00"))
    group_discount_pct  = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0"))
    threeyear_discount  = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0"))
    trial_days      = models.PositiveSmallIntegerField(default=0)
    is_active       = models.BooleanField(default=True, db_index=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    @property
    def gst_amount(self):
        return (self.annual_price * self.gst_rate / Decimal("100")).quantize(Decimal("0.01"))

    @property
    def total_incl_gst(self):
        return self.annual_price + self.gst_amount

    @property
    def daily_rate(self):
        return (self.annual_price / Decimal("365")).quantize(Decimal("0.01"))


class PlanFeatureEntitlement(models.Model):
    ENTITLEMENT_CHOICES = [
        ("included", "Included"),
        ("excluded", "Excluded"),
        ("addon",    "Available as Add-on"),
    ]
    plan        = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    feature_key = models.CharField(max_length=80, db_index=True)
    entitlement = models.CharField(max_length=20, choices=ENTITLEMENT_CHOICES, default="excluded")

    class Meta:
        unique_together = [("plan", "feature_key")]


class PlanLimit(models.Model):
    plan            = models.OneToOneField(SubscriptionPlan, on_delete=models.CASCADE, related_name="limits")
    max_students    = models.IntegerField(default=500)   # -1 = unlimited
    max_exams_month = models.IntegerField(default=10)
    max_questions   = models.IntegerField(default=500)
    max_concurrent  = models.IntegerField(default=100)
    storage_gb      = models.IntegerField(default=5)
    api_calls_day   = models.IntegerField(default=0)
    max_staff       = models.IntegerField(default=10)
    whatsapp_month  = models.IntegerField(default=0)
    sms_month       = models.IntegerField(default=0)
    data_retention_years = models.IntegerField(default=1)


class PlanStagedChange(models.Model):
    plan        = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=20)  # price/feature/limit/addon
    field       = models.CharField(max_length=80)
    old_value   = models.TextField()
    new_value   = models.TextField()
    staged_by   = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="staged_changes")
    staged_at   = models.DateTimeField(auto_now_add=True)
    published   = models.BooleanField(default=False)
    published_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="published_changes")
    published_at = models.DateTimeField(null=True, blank=True)

    def apply(self):
        """Atomically apply this staged change to the live plan."""
        from decimal import Decimal
        if self.change_type == "price":
            setattr(self.plan, self.field, Decimal(self.new_value))
            self.plan.save(update_fields=[self.field])
        elif self.change_type == "feature":
            PlanFeatureEntitlement.objects.update_or_create(
                plan=self.plan, feature_key=self.field,
                defaults={"entitlement": self.new_value}
            )
        elif self.change_type == "limit":
            setattr(self.plan.limits, self.field, int(self.new_value))
            self.plan.limits.save(update_fields=[self.field])
```

---

## 9. Empty States

| Section | Copy |
|---|---|
| No staged changes | "No pending changes. All plan configuration is up to date." |
| Plan History (no changes) | "No plan changes recorded yet." |
| Add-ons (none) | "No add-ons configured. Click '+ New Add-on' to create one." |
| Feature Matrix (filtered, no results) | "No features match your search." |

---

---

## G4 Amendment — API Rate Limits per Plan Tier

### Rate Limits Tab (in Plan Config Edit Drawer — Tab 5 after Preview)

**Purpose:** Configures API request throttle limits per subscription plan tier. At scale, a single Starter-tier institution making unlimited API calls can starve shared Lambda concurrency from Enterprise-tier institutions during exam peaks. Rate limits enforce fair usage and protect the platform SLA.

**Why a separate tab:** Rate limits are not a "feature" toggle — they are infrastructure-level constraints that determine platform stability under load. They belong with Plan Config because they directly define what each paying tier receives in terms of API access.

**Rate Limit Configuration Table:**

| Endpoint Category | Starter | Standard | Professional | Enterprise | Unit |
|---|---|---|---|---|---|
| General API calls | 100 | 300 | 800 | 2,000 | req/min per institution |
| Exam submission endpoint | 50 | 200 | 500 | 2,000 | req/min per institution |
| Bulk export (CSV/XLSX) | 2 | 5 | 20 | Unlimited | req/hour per institution |
| Report generation | 1 | 3 | 10 | 30 | req/hour per institution |
| Student data API | 50 | 150 | 400 | 1,500 | req/min per institution |
| Webhook delivery | 10 | 30 | 100 | 500 | events/min |
| Question bank API (read) | 20 | 60 | 200 | 1,000 | req/min per institution |

**Edit behaviour:**
- PM Platform clicks a cell value to edit it inline
- Changing a value shows a projected impact: "This change will affect 842 Standard-tier institutions currently at 270 req/min average"
- Values are validated: cannot set a lower tier higher than a higher tier (Starter cannot exceed Standard)
- "Burst allowance" toggle per row: allows 2× the limit for up to 30 seconds before throttling kicks in
- 2FA required to publish rate limit changes (same staged-changes flow as plan features)

**Rate limit breach response (displayed in this config for PM reference):**
- Institution receives HTTP 429 with `Retry-After` header
- Breach event logged in institution's usage analytics
- After 5 breaches in 1 hour: an automatic email is sent to the institution admin recommending upgrade
- After 20 breaches in 1 day: CSM is notified (visible in Revenue & Billing Dashboard page 28)

**Historical rate limit data:**
- Sparkline chart per category: "Average API usage last 30 days by tier" — shows if current limits are too tight or have headroom
- "P99 usage" column: the 99th percentile request rate across all institutions in that tier — visible in the config table to guide limit-setting decisions

---

## 10. Error States

| Error | Display |
|---|---|
| Publish fails (DB error) | "Plan publish failed. No changes were applied. Please retry." `bg-[#1A0A0A] border-[#EF4444]` |
| Dependency conflict on feature toggle | Inline warning: "Feature X requires Feature Y to also be enabled for this plan." |
| Price below minimum | "Annual price cannot be less than ₹1,000." inline under field |
| Delete plan with active subscribers | "Cannot delete — {N} institutions are currently on this plan." |
| Limit below current peak usage | Breach simulation automatically shown before allowing save |

---

## 11. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `1–5` | Switch tabs |
| `E` | Toggle edit mode (Feature Matrix / Limits) |
| `P` | Publish staged changes (triggers 2FA modal) |
| `Esc` | Close drawer/modal |
| `/` | Focus feature search |
| `Ctrl+Z` | Undo last staged change (within session) |
