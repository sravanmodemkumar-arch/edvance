# div-a-11 — Subscription Plans

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total institutions | 2,050 |
| Plan tiers | Starter / Standard / Professional / Enterprise |
| Starter institutions | ~820 (40%) |
| Standard institutions | ~850 (41%) |
| Professional institutions | ~280 (14%) |
| Enterprise institutions | ~100 (5%) |
| Plan changes/month | ~15–25 upgrades · ~5–8 downgrades |
| Custom Enterprise plans | ~30 (negotiated pricing) |
| Add-ons available | 5 (Extra Students / API Access / White-label / Parent Portal / Bulk SMS) |

**Why this matters:** Plan Management is the revenue levers page. The COO uses it to see plan distribution, identify upgrade opportunities, manage pricing, and track plan change velocity. The CEO approves custom Enterprise pricing here. A poorly-managed plan change can silently over/under-bill an institution.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Subscription Plans |
| Route | `/exec/plans/` |
| Django view | `SubscriptionPlansView` |
| Template | `exec/subscription_plans.html` |
| Priority | P2 |
| Nav group | Finance |
| Required role | `exec`, `superadmin`, `finance` |
| 2FA required | Creating/editing plans · changing institution plan |
| HTMX poll | None (static reference data) |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Subscription Plans              [+ New Plan] [+ New Add-on]         │
├──────────────────────────────────────────────────────────────────────────────┤
│ TABS: [Plan Catalog] [Institution Plans] [Add-ons] [Plan History]           │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: PLAN CATALOG                                                            │
│                                                                              │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────────────┐ │
│ │ STARTER  │  │STANDARD  │  │PROFESS.  │  │ ENTERPRISE                   │ │
│ │ ₹5,000/m │  │₹15,000/m │  │₹40,000/m │  │ Custom pricing               │ │
│ │ 820 inst │  │ 850 inst │  │ 280 inst │  │ 100 institutions             │ │
│ │          │  │          │  │          │  │                              │ │
│ │ Features │  │ Features │  │ Features │  │ Features                     │ │
│ │ list ... │  │ list ... │  │ list ... │  │ list ...                     │ │
│ │          │  │          │  │          │  │                              │ │
│ │ [Edit]   │  │ [Edit]   │  │ [Edit]   │  │ [Edit]                       │ │
│ └──────────┘  └──────────┘  └──────────┘  └──────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 Tab: Plan Catalog

`id="tab-catalog"` · `hx-get="?part=catalog"`

#### 4.1.1 Plan Cards Grid

**Container:** `grid grid-cols-4 gap-4 p-4`
**Each plan card:** `bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-6 flex flex-col`
**Enterprise card:** `border-[#F59E0B]` golden border

**Plan card anatomy (per card):**
```
┌─────────────────────────────────────┐
│ STARTER                   [Edit ✎]  │  ← name text-sm font-bold uppercase + Edit icon btn
│ ₹5,000                              │  ← price text-3xl font-bold text-white
│ per institution / month             │  ← sub text-xs text-[#64748B]
│                                     │
│ Annual: ₹54,000 (10% off)           │  ← annual price text-sm text-[#94A3B8]
│                                     │
│ 820 institutions currently          │  ← count with link → Institution Plans tab filtered
│ ₹4.1L MRR                          │  ← MRR contribution
│                                     │
│ ─────────────────────────────────── │
│ ✓ Up to 500 students                │
│ ✓ 10 exams/month                    │  ← feature list text-sm text-[#94A3B8]
│ ✓ Basic reports                     │  ← ✓ = text-[#34D399] · ✗ = text-[#EF4444]
│ ✗ API access                        │
│ ✗ White-label portal                │
│ ✗ Priority support                  │
│                                     │
│ Add-ons available: +3               │  ← clickable, opens add-ons panel
└─────────────────────────────────────┘
```

**Edit button:** pencil icon `text-[#64748B] hover:text-white` · opens Edit Plan Drawer (§5.1) · requires 2FA

---

#### 4.1.2 Plan Comparison Table (below cards)

Full-width feature comparison matrix
**Rows:** each feature · **Columns:** Starter / Standard / Professional / Enterprise

| Feature | Starter | Standard | Professional | Enterprise |
|---|---|---|---|---|
| Students | 500 | 2,000 | 10,000 | Unlimited |
| Exams/month | 10 | 50 | 200 | Unlimited |
| Storage | 10 GB | 50 GB | 200 GB | Custom |
| API access | ✗ | ✗ | ✓ | ✓ |
| Webhook | ✗ | ✗ | ✓ | ✓ |
| White-label | ✗ | ✗ | ✗ | ✓ |
| Custom domain | ✗ | ✗ | ✗ | ✓ |
| Parent portal | Add-on | Add-on | ✓ | ✓ |
| SLA | Standard | Standard | Professional | Enterprise |
| Support | Email | Email+Chat | Priority | Dedicated CSM |
| Price/month | ₹5,000 | ₹15,000 | ₹40,000 | Custom |

**Cell styling:** ✓ `text-[#34D399]` · ✗ `text-[#EF4444]` · "Add-on" `text-[#FCD34D] text-xs`

---

### 4.2 Tab: Institution Plans

`id="tab-institutions"` · `hx-get="?part=institution_plans"`

**Purpose:** Which institution is on which plan? Filter, sort, change plans.

#### 4.2.1 Toolbar

[Search...] · [Type ▾] · [Plan ▾] · [SLA ▾] · Sort: [Plan ▾]

#### 4.2.2 Institution Plans Table

| Column | Detail |
|---|---|
| Institution | Name + type icon |
| Current Plan | Plan badge |
| Monthly Rate | `₹XX,XXX` (may differ from base if custom) |
| Students (current) | Count vs plan limit (progress bar) |
| Add-ons | List of enabled add-ons as small chips |
| Plan Since | Date |
| Next Renewal | Date + "N days" |
| Upgrade Signal | `⚡` if > 80% of any limit used |
| Actions ⋯ | Change Plan / Manage Add-ons / View Invoices |

**[Change Plan]** → Change Plan Modal (§6.1) · requires 2FA

**Pagination:** 25/page

---

### 4.3 Tab: Add-ons

`id="tab-addons"` · `hx-get="?part=addons"`

#### 4.3.1 Add-on Catalog Cards

`grid grid-cols-3 gap-4 p-4`

Each add-on card:
```
┌─────────────────────────────────┐
│ Parent Portal                   │
│ ₹2,000 / month                  │
│ Available for: Standard, Pro    │
│                                 │
│ Enabled at 342 institutions     │
│ ₹6.8L add-on MRR               │
│                                 │
│ [Edit] [Disable Add-on]         │
└─────────────────────────────────┘
```

Add-ons: Extra Students (₹5/student/month) · API Access (₹5,000/month) · White-label (₹10,000/month) · Parent Portal (₹2,000/month) · Bulk SMS (₹1,000/month)

#### 4.3.2 Add-on Adoption Table

| Add-on | Enabled Institutions | MRR Contribution | Avg per Institution |
|---|---|---|---|
| Parent Portal | 342 | ₹6.8L | ₹1,988 |
| Extra Students | 185 | ₹3.7L | ₹2,000 |
| ... | | | |

---

### 4.4 Tab: Plan History

`id="tab-history"` · `hx-get="?part=plan_history"`

**Purpose:** Audit trail of all plan changes across the platform.

#### 4.4.1 Filter Bar

[Institution ▾] · [Change Type ▾] (Upgrade/Downgrade/New/Cancel) · [Date Range ▾]

#### 4.4.2 Plan History Table

| Column | Detail |
|---|---|
| Institution | Name + type |
| Change Type | Upgrade (green ↑) / Downgrade (red ↓) / New / Cancel |
| From Plan | Old plan badge (or `—` for new) |
| To Plan | New plan badge |
| MRR Impact | `+₹X,XXX` green or `-₹X,XXX` red |
| Changed By | User name + role |
| Changed At | Timestamp |
| Reason | Text (optional) |
| Actions ⋯ | View Invoice / View Institution |

**Sort:** Changed At desc
**Pagination:** 25/page

---

## 5. Drawers

### 5.1 Edit Plan Drawer (560 px)

**2FA required to open.**
`id="plan-edit-drawer"` · `body.drawer-open`

**Header:** Plan name + "Edit Plan" · `[×]`

**Tab bar (2 tabs):** Pricing & Limits · Features

**Tab A — Pricing & Limits:**
| Field | Type | Detail |
|---|---|---|
| Plan name | Text (read-only for standard plans) | |
| Monthly price | Decimal input | `₹` prefix |
| Annual price | Decimal input (auto-filled as 10× monthly) | editable override |
| Student limit | Number | `0` = unlimited |
| Exams/month limit | Number | `0` = unlimited |
| Storage limit (GB) | Number | |
| API calls/day limit | Number | `0` = unlimited |
| SLA tier | Select | Standard / Professional / Enterprise |

**Tab B — Features:**
Toggle switches for each feature (same list as §4.1.2)
`accent-[#6366F1]`

**Effective date selector:**
- Immediately (affects new invoices only)
- From next billing cycle (default, safest)
- Custom date

**Impact preview (below form):**
"This change affects 820 institutions. Their next invoices will reflect the new pricing."

**Footer:** [Cancel] [Save Plan Changes]

**POST:** `hx-post="?part=save_plan&id={plan_id}"` · 2FA enforced server-side

---

### 5.2 Add-on Edit Drawer (480 px)

Same pattern as §5.1 but for add-on configuration:
- Name · Price · Available plans (multi-select) · Description · Enabled toggle

---

## 6. Modals

### 6.1 Change Institution Plan Modal (560 px)

**2FA required.**

**Header:** "Change Plan — {Institution Name}"

**Current plan:** highlighted card showing current plan + current monthly rate

**Plan selection:** Radio group with plan cards (4 plans)
- If institution > plan student limit: amber warning "This institution has {N} students which exceeds the {plan} limit of {M}"

**Add-ons section:** show which add-ons carry over vs which become included/excluded

**Proration section:**
"Switching from Standard to Professional mid-cycle will add ₹X,XXX to the next invoice (prorated {N} days remaining)."

**Effective date:**
- [Immediately] [Next billing cycle] [Custom date]

**Reason:** Text input (required for downgrades)

**Footer:** [Cancel] [Confirm Plan Change]

---

### 6.2 New Plan Modal (480 px)

**2FA required.**
Fields: Name · Type (Standard/Custom) · Price · Limits (same as Edit drawer Tab A) · Features toggles
**Footer:** [Cancel] [Create Plan]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=catalog` | `exec/partials/plan_catalog.html` | Tab click |
| `?part=institution_plans` | `exec/partials/inst_plans_table.html` | Tab click · filter change |
| `?part=addons` | `exec/partials/plan_addons.html` | Tab click |
| `?part=plan_history` | `exec/partials/plan_history.html` | Tab click · filter change |
| `?part=plan_drawer&id={id}` | `exec/partials/plan_edit_drawer.html` | Edit button click |
| `?part=save_plan&id={id}` | JSON result | Drawer form POST |
| `?part=change_plan` | JSON result | Change Plan modal POST |

**Django view dispatch:**
```python
class SubscriptionPlansView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_billing"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "catalog": "exec/partials/plan_catalog.html",
                "institution_plans": "exec/partials/inst_plans_table.html",
                "addons": "exec/partials/plan_addons.html",
                "plan_history": "exec/partials/plan_history.html",
                "plan_drawer": "exec/partials/plan_edit_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/subscription_plans.html", ctx)

    def post(self, request):
        part = request.GET.get("part", "")
        handlers = {
            "save_plan": self._handle_save_plan,
            "change_plan": self._handle_change_plan,
        }
        if part in handlers:
            return handlers[part](request)
        return HttpResponseNotAllowed(["GET"])
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| Plan catalog tab | < 300 ms | > 800 ms |
| Institution plans table (25 rows) | < 400 ms | > 1 s |
| Plan history table | < 400 ms | > 1 s |
| Plan edit drawer | < 250 ms | > 700 ms |
| Full page initial load | < 1 s | > 2.5 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Institution on custom Enterprise pricing | Plan badge shows "Enterprise (Custom)" · monthly rate shown as negotiated value |
| Plan downgrade: institution exceeds new limit | Downgrade blocked with error "Institution has 12,400 students; Professional plan limit is 10,000" unless override checkbox checked by Finance role |
| Plan deleted (archived) | Existing institutions remain on it; plan shown as "Legacy — [Plan Name]" badge |
| Price change on existing plan | Shows impact preview; proration calculated; audit log entry created |
| Add-on incompatible with current plan | Add-on card greyed out for incompatible plans with tooltip |
| 0 institutions on a plan | Plan card still shown (can edit); institution count = 0 |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`4` | Switch tabs |
| `N` | New plan (catalog tab) |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/subscription_plans.html` | Full page shell |
| `exec/partials/plan_catalog.html` | Plan cards + comparison table |
| `exec/partials/inst_plans_table.html` | Institution plans table |
| `exec/partials/plan_addons.html` | Add-on catalog + table |
| `exec/partials/plan_history.html` | Plan change history table |
| `exec/partials/plan_edit_drawer.html` | Edit plan drawer |
| `exec/partials/addon_edit_drawer.html` | Edit add-on drawer |
| `exec/partials/change_plan_modal.html` | Change institution plan modal |
| `exec/partials/new_plan_modal.html` | Create new plan modal |

---

## 12. Component References

| Component | Used in |
|---|---|
| `PlanCard` | §4.1.1 |
| `FeatureComparisonTable` | §4.1.2 |
| `TabBar` | §4.1–4.4 |
| `InstitutionPlansTable` | §4.2.2 |
| `UsageLimitBar` | §4.2.2 students column |
| `AddOnCard` | §4.3.1 |
| `AddOnAdoptionTable` | §4.3.2 |
| `PlanHistoryTable` | §4.4.2 |
| `DrawerPanel` | §5.1–5.2 |
| `FeatureFlagToggle` | §5.1 Tab B |
| `PlanComparisonRadio` | §6.1 |
| `ModalDialog` | §6.1–6.2 |
| `PaginationStrip` | Tables |
