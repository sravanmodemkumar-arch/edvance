# 02 — Feature Flags

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Active flags in production | ~120 |
| Institutions affected by flags | 2,050 |
| Students indirectly affected | 2.4M–7.6M |
| Peak concurrent users during flag change | Up to 74,000 |
| Flag types | Boolean · Percentage rollout · Per-institution · Per-plan-tier · Per-institution-type |
| Flag owners | PM Platform · PM Exam Domains · PM Institution Portal |
| Audit events per day | ~50–200 flag changes |
| Flag dependencies | ~40 dependency relationships across 120 flags |

**Why this page matters at scale:** A single misconfigured flag can silently break the exam experience for 74,000 concurrent students or disable billing for 2,050 institutions. The Feature Flags page is the highest-risk configuration surface in Division B. Every change must be audited, reversible with a kill-switch, and observable via rollout analytics. PM Platform reviews this page daily. A "partial rollout" left running for 90 days without progression is technical debt that creates inconsistent institution experiences.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Feature Flags |
| Route | `/product/feature-flags/` |
| Django view class | `FeatureFlagsView` |
| Template | `product/feature_flags.html` |
| Permission — view | `portal.view_feature_flags` (all div-b roles) |
| Permission — manage | `portal.manage_feature_flags` (PM Platform only) |
| Permission — publish / kill | `portal.publish_feature_flags` (PM Platform + 2FA) |
| 2FA required | Yes — for enable, disable, kill-switch, rollout % change > 50% |
| HTMX poll — KPI strip | Every 60s (paused when drawer/modal open) |
| HTMX poll — flag table | No auto-poll (on-demand; flag state changes are explicit) |
| Nav group | Product |
| Nav icon | `toggle-right` |
| Priority | P0 |

---

## 3. Wireframe

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Feature Flags                 [+ New Flag]  [Import]  [Export CSV]  [Audit]│
├────────┬────────┬────────┬────────┬────────┬────────────────────────────────────────┤
│ Total  │ Enabled│ Partial│Disabled│Deprecat│ Stale Warnings                        │
│  120   │   89   │   8    │  18    │   5    │  3 flags need attention ⚠             │
├────────┴────────┴────────┴────────┴────────┴────────────────────────────────────────┤
│ TABS: [All Flags (120)] [Enabled (89)] [Partial Rollout (8)] [Disabled (18)]       │
│       [Deprecated (5)] [My Flags] [Stale (3)]                                      │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ TOOLBAR: [🔍 Search flags...] [Owner ▾] [Type ▾] [Domain ▾] [Age ▾] [Apply][Reset] │
│ Active chips: Owner: PM Platform ×   Domain: Exam ×   [Clear all]                  │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ TABLE HEADER                                                                         │
│ ☐ │ Flag Key        │ Name                   │ Status │ Rollout  │ Owner │ Age │ ⋯  │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ ☐ │ new_exam_ui     │ New Exam Interface v3  │ ●Partial│ 10%  ██░│ PM P  │ 14d │ ⋯ │
│ ☐ │ ai_mcq_gen      │ AI MCQ Generation      │ ●Enabled│ 100% ██ │ PM P  │ 45d │ ⋯ │
│ ☐ │ batch_export    │ Batch Result Export    │ ●Enabled│ 100% ██ │ PM P  │ 90d │ ⋯ │
│ ☐ │ v3_leaderboard  │ V3 Leaderboard UI      │ ●Partial│  5%  █░ │ PM P  │ 7d  │ ⋯ │
│ ☐ │ old_auth_flow   │ Legacy Auth Flow       │ ●Deprec.│  0%    │ PM P  │180d │ ⋯ │
│ ...                                                                                  │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ PAGINATION: [← Prev] [1] [2] [3] ... [12] [Next →]   Showing 1–10 of 120           │
│ Per page: [10 ▾]                                       [Select all on page ☐]       │
│ Bulk actions: [Enable Selected] [Disable Selected] [Deprecate Selected] [Delete]    │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

**Container:** `flex gap-4 p-4` · 5 cards · `bg-[#0D1526] rounded-xl border border-[#1E2D4A]`
**Poll:** `hx-get="?part=kpi" hx-trigger="every 60s[!document.querySelector('.drawer-open,.modal-open')]" hx-target="#kpi-strip" hx-swap="outerHTML"`

| # | Card | Value | Delta | Alert | Tooltip |
|---|---|---|---|---|---|
| 1 | Total Flags | `120` | +3 this week | > 200 = amber | "Total flags across all owners" |
| 2 | Enabled | `89` | — | — | "Fully enabled for all eligible institutions" |
| 3 | Partial Rollout | `8` | — | > 20 = amber | "Enabled for a % of institutions" |
| 4 | Disabled | `18` | — | — | "Inactive; can be re-enabled" |
| 5 | Stale Warnings | `3` | — | Any stale = amber pulsing | "Flags not changed in > 60 days while partial" |

**Stale card:** when value > 0, card border pulses amber: `animate-pulse border-[#F59E0B]`

---

### 4.2 Tab Bar

| Tab | Badge | hx-get | Description |
|---|---|---|---|
| All Flags | `120` | `?part=table&status=all` | Full list |
| Enabled | `89` | `?part=table&status=enabled` | Active flags |
| Partial Rollout | `8` | `?part=table&status=partial` | Gradual rollout flags |
| Disabled | `18` | `?part=table&status=disabled` | Inactive flags |
| Deprecated | `5` | `?part=table&status=deprecated` | Scheduled for removal |
| My Flags | dynamic | `?part=table&owner=me` | Flags owned by logged-in PM |
| Stale | `3` | `?part=table&stale=true` | Flags needing attention |

Badge: `text-xs bg-[#1E2D4A] text-[#94A3B8] px-1.5 py-0.5 rounded-full ml-1`

---

### 4.3 Toolbar

**Container:** `flex flex-wrap gap-3 p-4 bg-[#0D1526] rounded-xl border border-[#1E2D4A] mb-4`

| Control | Type | Options | Width |
|---|---|---|---|
| Search | Text · debounce 300ms | Flag key or name search | 280px |
| Owner | Dropdown | All · PM Platform · PM Exam Domains · PM Institution Portal | 180px |
| Type | Multi-select | Boolean · Percentage · Per-Institution · Per-Plan · Per-Type | 180px |
| Domain | Multi-select | Exam · Content · Analytics · Communication · Billing · Infrastructure · All | 200px |
| Age | Dropdown | Any · < 7d · 7–30d · 30–90d · > 90d (stale) | 150px |
| [Apply] | Button | `bg-[#6366F1] text-white px-4 py-2 rounded-lg` | auto |
| [Reset] | Ghost | `text-[#94A3B8] hover:text-white` | auto |

**Active filter chips:** `flex flex-wrap gap-2 mt-2`
Each chip: `text-xs bg-[#1E2D4A] text-[#94A3B8] px-2 py-1 rounded-full` with `×` remove
"Clear all" link: `text-[#6366F1] text-xs` — shown when ≥ 2 chips active

---

### 4.4 Flag Table

**Container:** `id="flags-table"` · `hx-get="?part=table" hx-trigger="filter-change" hx-swap="innerHTML"`

#### 4.4.1 Table Header

| Column | Width | Sortable | Default Sort |
|---|---|---|---|
| ☐ Select all | 40px | — | — |
| Flag Key | 200px | Yes | — |
| Name | 260px | Yes | — |
| Status | 120px | Yes | Asc |
| Rollout | 160px | Yes | — |
| Type | 100px | Yes | — |
| Domain | 120px | No | — |
| Owner | 100px | No | — |
| Institutions Affected | 140px | Yes | — |
| Last Changed | 120px | Yes | Desc (default) |
| Changed By | 120px | No | — |
| Actions ⋯ | 48px | — | — |

#### 4.4.2 Table Row Detail

**Row background by status:**
- Enabled: `bg-[#0D1526]` (default)
- Partial: `bg-[#131F38]` with left border `border-l-4 border-[#F59E0B]`
- Disabled: `bg-[#0D1526] opacity-60`
- Deprecated: `bg-[#0D1526] opacity-40 line-through text-[#475569]`
- Stale: `bg-[#1A1000] border-l-4 border-[#F59E0B]`

**Flag Key cell:** `font-mono text-xs text-[#94A3B8]` — copy-to-clipboard icon on hover

**Status badge:**

| Status | Badge style |
|---|---|
| Enabled | `bg-[#064E3B] text-[#34D399]` + green dot |
| Partial | `bg-[#451A03] text-[#FCD34D]` + amber dot |
| Disabled | `bg-[#1E2D4A] text-[#94A3B8]` + grey dot |
| Deprecated | `bg-[#450A0A] text-[#F87171]` + red dot |

**Rollout column:**
- Progress bar: `bg-[#1E2D4A] rounded-full h-2 w-32`
  - Fill: `bg-[#6366F1]` for enabled portion
- Percentage label: `text-xs text-[#94A3B8] ml-2`
- `100%` shown as solid fill — no percentage label needed

**Type badge:** `text-xs px-2 py-0.5 rounded-full`
- Boolean: `bg-[#1E2D4A] text-[#94A3B8]`
- Percentage: `bg-[#312E81] text-[#A5B4FC]`
- Per-Institution: `bg-[#064E3B] text-[#6EE7B7]`
- Per-Plan: `bg-[#0C4A6E] text-[#7DD3FC]`
- Per-Type: `bg-[#3B1764] text-[#D8B4FE]`

**Institutions Affected cell:**
- `2,050` for fully enabled Boolean flags
- `~205` for 10% rollout
- `—` for disabled flags

**Last Changed cell:** relative time `text-[#94A3B8] text-xs` — absolute on hover (tooltip)

**Actions kebab menu (⋯):**
- Edit / Configure → opens Flag Detail Drawer
- Enable / Disable (toggle) → requires 2FA
- Set Rollout % → opens mini inline rollout modal
- Add Institution Override → opens override modal
- View Audit History → opens drawer on Audit tab
- Deprecate Flag → confirmation modal
- Delete Flag → confirmation modal (only if disabled + no active overrides)

#### 4.4.3 Row Expand (stale warning flags)

Stale flag rows have an expand button: `▼` chevron right side
Expanded: inline amber row below with:
```
⚠ This flag has been at 10% rollout for 67 days.
  Recommended actions: [Increase to 50%] [Increase to 100%] [Disable] [Deprecate]
```
Each action button triggers appropriate modal.

---

### 4.5 Pagination

**Container:** `flex items-center justify-between px-4 py-3 border-t border-[#1E2D4A]`

**Left:** "Showing 1–10 of 120 flags"  `text-sm text-[#94A3B8]`
**Centre:** page pills
- `[← Prev]` · `[1]` `[2]` `[3]` `...` `[12]` · `[Next →]`
- Active pill: `bg-[#6366F1] text-white`
- Inactive pill: `bg-[#1E2D4A] text-[#94A3B8] hover:bg-[#131F38]`
- All `px-3 py-1 rounded text-sm`

**Right:** Per page selector `<select class="bg-[#131F38] border border-[#1E2D4A] text-[#94A3B8] text-sm rounded px-2 py-1">`
Options: `10 / 25 / 50 / 100`

**HTMX:** `hx-get="?part=table&page=N&per_page=M" hx-target="#flags-table" hx-swap="innerHTML"`

---

### 4.6 Bulk Actions Bar

**Shown when:** ≥ 1 row checkbox selected
**Container:** `fixed bottom-0 left-0 right-0 bg-[#0D1526] border-t border-[#1E2D4A] px-6 py-3 flex items-center gap-4 z-40`

Content:
- `X flag(s) selected` — `text-sm text-[#F1F5F9]`
- [Enable Selected] — `bg-[#064E3B] text-[#34D399] px-3 py-1.5 rounded text-sm`
- [Disable Selected] — `bg-[#1E2D4A] text-[#94A3B8] px-3 py-1.5 rounded text-sm`
- [Deprecate Selected] — `bg-[#451A03] text-[#FCD34D] px-3 py-1.5 rounded text-sm`
- [Delete Selected] — `bg-[#450A0A] text-[#F87171] px-3 py-1.5 rounded text-sm`
- [Cancel Selection] — ghost text

**Bulk enable/disable:** 2FA required when affecting > 10% of active flags or any flag with > 1,000 institutions affected.

---

## 5. Drawers

### 5.1 Flag Detail Drawer (560px)

**Trigger:** Row click or kebab → Edit
**Slide-in:** right side · `transition-transform duration-300 ease-out`
**Backdrop:** `bg-black/40 z-40`
**On open:** `document.body.classList.add('drawer-open')`
**On close:** `document.body.classList.remove('drawer-open')`

**Header:**
```
[Flag Key: font-mono]    [Status badge]    [⚠ Stale warning if applicable]    [×]
Flag Name (editable inline — pencil icon)
Owner badge · Created date · Last changed by
```

**Tab bar (4 tabs):** `flex border-b border-[#1E2D4A]`

---

#### Tab A — Configuration

**Flag Key (read-only):**
`text-xs font-mono bg-[#070C18] border border-[#1E2D4A] px-3 py-2 rounded w-full`
Copy icon: `cursor-pointer text-[#475569] hover:text-[#94A3B8]`

**Flag Name:**
`input.bg-[#131F38] border border-[#1E2D4A] text-[#F1F5F9] px-3 py-2 rounded w-full`
Max 80 chars

**Description:**
`textarea.bg-[#131F38] border border-[#1E2D4A] text-[#94A3B8] px-3 py-2 rounded w-full` · 3 rows
Purpose, expected behaviour, rollout plan

**Status Toggle:**
`flex items-center gap-3`
Toggle switch: `w-11 h-6 rounded-full transition-colors` · enabled: `bg-[#6366F1]` · disabled: `bg-[#1E2D4A]`
Label: current state text
**2FA prompt:** shown inline when toggling Enabled ↔ Disabled if > 100 institutions affected

**Rollout Type Selector (radio group):**
```
○ Boolean (all or nothing)
○ Percentage rollout
○ Per-institution override list
○ By plan tier
○ By institution type
```

**Percentage Rollout Section** (shown when type = Percentage):
- Slider: `input[type=range]` `0–100` · accent: `#6366F1`
- Live preview: `"~{N} institutions will see this feature"`
  - Calculation: `round(rollout_pct / 100 * 2050)` institutions
- Ramp schedule: `[ ] Auto-ramp: increase by 10% every [7] days if no errors`
- Error threshold: `Stop ramp if error rate exceeds [0.5]%`

**By Plan Tier** (shown when type = Per-Plan):
Checkbox grid:
```
☑ Starter (620 institutions)
☑ Standard (840 institutions)
☑ Professional (410 institutions)
☑ Enterprise (180 institutions)
```

**By Institution Type** (shown when type = Per-Type):
```
☑ Schools (1,000)
☑ Colleges (800)
☑ Coaching Centres (100)
☐ Institution Groups (150)
```

**Kill Switch (danger zone):**
`bg-[#1A0A0A] border border-[#EF4444] rounded-xl p-4 mt-4`
Red text: "Emergency kill switch — immediately disables for ALL institutions"
[Kill Switch — Disable Now] button: `bg-[#EF4444] text-white` · requires 2FA + typed reason

---

#### Tab B — Institution Overrides

**Purpose:** Override the default rollout for specific institutions. E.g., enable a partial-rollout flag for a specific beta institution regardless of the rollout %.

**Search institutions:** `input placeholder="Search institution name..."` debounce 300ms
`hx-get="?part=institution_search" hx-trigger="keyup changed delay:300ms" hx-target="#override-search-results"`

**Overrides table:**
| Column | Detail |
|---|---|
| Institution | Name + type badge |
| Override | Enabled / Disabled (opposite of default) |
| Set by | Staff name |
| Set on | Relative date |
| Expires | Date or Never |
| Actions | [Edit] [Remove] |

**Add Override button:** `bg-[#131F38] border border-[#1E2D4A] text-[#94A3B8] hover:border-[#6366F1]`
Opens inline form:
- Institution search autocomplete
- Override direction: Enable / Disable
- Expiry date picker (optional)
- Reason (required, 10 char min)

**Pagination:** 10/page if > 10 overrides

**Bulk remove overrides:** select + [Remove Selected]

---

#### Tab C — Audit History

**Filter row:** Date range picker · Actor dropdown · Action type dropdown

**Timeline:** `space-y-3`

Each event:
```
● [actor avatar initials] [actor name] [action verb] [changed field]
  [old value → new value]
  [timestamp absolute] · [IP address]
```

Event types and colours:
- Created: `text-[#34D399]` · green dot
- Enabled: `text-[#34D399]` · green dot
- Disabled: `text-[#F87171]` · red dot
- Rollout % changed: `text-[#FCD34D]` · amber dot
- Override added: `text-[#A5B4FC]` · indigo dot
- Override removed: `text-[#94A3B8]` · grey dot
- Kill-switch triggered: `text-[#EF4444]` · pulsing red dot
- Deprecated: `text-[#F87171]` · red dot

**Load more:** `hx-get="?part=flag_audit&flag_id={id}&page={n}" hx-swap="beforeend"`

**Export:** [Export Audit CSV] button — downloads full audit trail for this flag

---

#### Tab D — Dependencies

**Purpose:** Shows which flags this flag depends on (must be enabled first) and which flags depend on this one.

**Depends On section:**
Table: Dep Flag Key · Name · Status · Action (remove dependency)
[Add Dependency] button → search dropdown

**Required By section:**
Table: Dependent Flag Key · Name · Status
(read-only — removing these dependencies done from those flags)

**Dependency Graph:**
SVG tree diagram rendered inline · 200px height
- Current flag: `fill: #6366F1` rectangle
- Dependencies: `fill: #064E3B` rectangles
- Dependents: `fill: #1E2D4A` rectangles
- Arrows: `stroke: #475569`

**Conflict warnings:**
`bg-[#1A0A0A] border border-[#EF4444] rounded p-3`
- Circular dependency detected: "flag_a → flag_b → flag_a"
- Disabled dependency: "This flag requires `flag_x` which is currently disabled"

---

**Footer:**
`flex justify-between items-center px-6 py-4 border-t border-[#1E2D4A]`
- Left: [Delete Flag] `text-[#F87171] text-sm` (only if disabled + no active overrides)
- Right: [Cancel] · [Save Changes] `bg-[#6366F1]` (2FA for publish/kill changes)

---

## 6. Modals

### 6.1 New Flag Modal

**Trigger:** [+ New Flag] header button
**Width:** 560px

**Form fields:**

| Field | Type | Validation |
|---|---|---|
| Flag Key | Text · `font-mono` | Required · slug format `[a-z0-9_]` · max 80 chars · unique check on blur |
| Flag Name | Text | Required · max 120 chars |
| Description | Textarea | Required · min 20 chars · explain purpose and rollout plan |
| Type | Select | Boolean · Percentage · Per-Institution · Per-Plan · Per-Type |
| Domain | Select | Exam · Content · Analytics · Communication · Billing · Infrastructure |
| Owner | Select | PM Platform · PM Exam Domains · PM Institution Portal |
| Initial Status | Radio | Disabled (safe default) · Enabled · Partial (10%) |
| Dependencies | Multi-select search | Optional — other flags this requires |
| Linked Release | Select | Optional — associate with a release |
| Rollout Plan | Textarea | Optional — describe progression plan |

**Flag key uniqueness check:**
`hx-get="?part=flag_key_check&key={value}" hx-trigger="blur" hx-target="#flag-key-feedback"`
- Available: `✓ Available` in green
- Taken: `✗ Already in use` in red

**Footer:** [Create Flag] · [Cancel]
On success: row appears at top of table · success toast: `"Flag '{key}' created"` `bg-[#064E3B]`

---

### 6.2 Rollout % Change Modal

**Trigger:** kebab → "Set Rollout %" OR inline from stale warning action
**Width:** 480px

**Current state display:**
`Current rollout: 10% (~205 institutions)`

**New rollout slider:** 0–100 range · `accent-[#6366F1]`
Live preview: "Will affect ~{N} of 2,050 institutions"

**Impact breakdown:**
| Institution Type | Currently Seeing | Will See After |
|---|---|---|
| Schools | ~100 | ~{new_n} |
| Colleges | ~82 | ~{new_n} |
| Coaching | ~10 | ~{new_n} |
| Groups | ~15 | ~{new_n} |

**Auto-ramp toggle:**
`[ ] Enable auto-ramp: increase by [10]% every [7] days if error rate < [0.5]%`

**Change reason:** `textarea` required · min 10 chars

**2FA gate:** shown when new % - old % > 50 (large jump)

**Footer:** [Apply Rollout Change] · [Cancel]

---

### 6.3 Deprecate Flag Modal

**Trigger:** kebab → Deprecate or bulk Deprecate Selected
**Width:** 480px

**Warning banner:** `bg-[#451A03] border border-[#F59E0B] rounded p-3`
"Deprecated flags remain in code but are always treated as disabled. Schedule final removal."

**Form:**
- Deprecation reason: textarea required
- Target removal date: date picker (required)
- Assigned to (for removal): team member dropdown
- JIRA ticket: text input (optional)

**Dependency check:**
If other flags depend on this: `bg-[#1A0A0A] border border-[#EF4444] rounded p-3`
"⚠ {N} flags depend on this flag. They must be updated before deprecation."
Lists dependent flags.

**Footer:** [Confirm Deprecation] · [Cancel]

---

### 6.4 Import Flags Modal

**Trigger:** [Import] header button
**Width:** 560px

**File drop zone:**
`border-2 border-dashed border-[#1E2D4A] rounded-xl p-8 text-center`
`hover:border-[#6366F1]`
"Drag and drop a JSON or CSV flags file here, or click to browse"

**Supported formats:** JSON (EduForge export format) · CSV

**Preview table** (after file selected):
| Flag Key | Name | Status | Conflicts |
- Conflicts highlighted in red: "Key already exists — will overwrite"
- New flags: green "Will create"

**Import options:**
- `[×]` Skip conflicting / `[○]` Overwrite conflicting / `[○]` Rename conflicting (append `_v2`)
- `[ ] Preserve existing overrides on conflicting flags`

**Footer:** [Import {N} Flags] · [Cancel]

---

## 7. Django View

```python
# portal/apps/product/views.py

class FeatureFlagsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_feature_flags"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":               "product/partials/flags_kpi.html",
                "table":             "product/partials/flags_table.html",
                "flag_drawer":       "product/partials/flag_drawer.html",
                "flag_audit":        "product/partials/flag_audit.html",
                "flag_overrides":    "product/partials/flag_overrides.html",
                "flag_dependencies": "product/partials/flag_dependencies.html",
                "institution_search":"product/partials/institution_search.html",
                "flag_key_check":    "product/partials/flag_key_check.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "product/feature_flags.html", ctx)

    def post(self, request):
        action = request.POST.get("action")

        # 2FA gate for sensitive actions
        sensitive_actions = {
            "enable_flag", "disable_flag", "kill_switch",
            "set_rollout", "bulk_enable", "bulk_disable",
            "deprecate_flag", "delete_flag",
        }
        if action in sensitive_actions:
            if not request.session.get("2fa_verified"):
                return JsonResponse({"error": "2FA required", "redirect": "/auth/2fa/"}, status=403)

        # Check manage permission
        if not request.user.has_perm("portal.manage_feature_flags"):
            return JsonResponse({"error": "Permission denied"}, status=403)

        if action == "create_flag":
            return self._create_flag(request)
        elif action == "update_flag":
            return self._update_flag(request)
        elif action == "set_rollout":
            return self._set_rollout(request)
        elif action == "kill_switch":
            return self._kill_switch(request)
        elif action == "deprecate_flag":
            return self._deprecate_flag(request)
        elif action == "delete_flag":
            return self._delete_flag(request)
        elif action == "add_override":
            return self._add_override(request)
        elif action == "remove_override":
            return self._remove_override(request)
        elif action == "bulk_enable":
            return self._bulk_enable(request)
        elif action == "bulk_disable":
            return self._bulk_disable(request)
        elif action == "import_flags":
            return self._import_flags(request)

        return JsonResponse({"error": "Unknown action"}, status=400)

    def _build_context(self, request):
        from portal.apps.product.models import FeatureFlag
        from django.core.cache import cache

        filters = {
            "status": request.GET.get("status", "all"),
            "owner": request.GET.get("owner", ""),
            "type": request.GET.getlist("type"),
            "domain": request.GET.getlist("domain"),
            "search": request.GET.get("q", ""),
            "stale": request.GET.get("stale", ""),
        }

        qs = FeatureFlag.objects.select_related("owner", "last_changed_by")
        if filters["status"] != "all":
            qs = qs.filter(status=filters["status"])
        if filters["search"]:
            qs = qs.filter(
                Q(key__icontains=filters["search"]) |
                Q(name__icontains=filters["search"])
            )
        if filters["owner"]:
            qs = qs.filter(owner__username=filters["owner"])
        if filters["stale"] == "true":
            from django.utils import timezone
            from datetime import timedelta
            cutoff = timezone.now() - timedelta(days=60)
            qs = qs.filter(status="partial", last_changed__lt=cutoff)

        # KPI — Redis cached
        kpi = cache.get_or_set(
            "product:flags:kpi",
            lambda: {
                "total":      FeatureFlag.objects.count(),
                "enabled":    FeatureFlag.objects.filter(status="enabled").count(),
                "partial":    FeatureFlag.objects.filter(status="partial").count(),
                "disabled":   FeatureFlag.objects.filter(status="disabled").count(),
                "deprecated": FeatureFlag.objects.filter(status="deprecated").count(),
                "stale":      FeatureFlag.objects.stale_count(),
            },
            60
        )

        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("per_page", 10))
        paginator = Paginator(qs.order_by("-last_changed"), per_page)
        page_obj = paginator.get_page(page)

        return {
            "flags": page_obj,
            "paginator": paginator,
            "kpi": kpi,
            "filters": filters,
        }
```

---

## 8. Flag Data Model Reference

```python
# portal/apps/product/models.py

class FeatureFlag(models.Model):
    STATUS_CHOICES = [
        ("enabled",    "Enabled"),
        ("partial",    "Partial Rollout"),
        ("disabled",   "Disabled"),
        ("deprecated", "Deprecated"),
    ]
    TYPE_CHOICES = [
        ("boolean",       "Boolean"),
        ("percentage",    "Percentage Rollout"),
        ("per_institution","Per Institution"),
        ("per_plan",      "By Plan Tier"),
        ("per_type",      "By Institution Type"),
    ]
    DOMAIN_CHOICES = [
        ("exam",          "Exam"),
        ("content",       "Content"),
        ("analytics",     "Analytics"),
        ("communication", "Communication"),
        ("billing",       "Billing"),
        ("infrastructure","Infrastructure"),
    ]

    key          = models.SlugField(max_length=80, unique=True, db_index=True)
    name         = models.CharField(max_length=120)
    description  = models.TextField()
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default="disabled", db_index=True)
    flag_type    = models.CharField(max_length=20, choices=TYPE_CHOICES, default="boolean")
    domain       = models.CharField(max_length=20, choices=DOMAIN_CHOICES)
    rollout_pct  = models.PositiveSmallIntegerField(default=0)  # 0–100
    owner        = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="owned_flags")
    dependencies = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="dependents")
    linked_release = models.ForeignKey("Release", on_delete=models.SET_NULL, null=True, blank=True)
    deprecation_date = models.DateField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True, db_index=True)
    last_changed_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="flag_changes")

    class Meta:
        ordering = ["-last_changed"]
        indexes = [
            models.Index(fields=["status", "domain"]),
            models.Index(fields=["last_changed"]),
        ]

    @classmethod
    def stale_count(cls):
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=60)
        return cls.objects.filter(status="partial", last_changed__lt=cutoff).count()


class FeatureFlagOverride(models.Model):
    flag        = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE, related_name="overrides")
    institution = models.ForeignKey("Institution", on_delete=models.CASCADE)
    enabled     = models.BooleanField()
    set_by      = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    set_at      = models.DateTimeField(auto_now_add=True)
    expires_at  = models.DateTimeField(null=True, blank=True)
    reason      = models.TextField()

    class Meta:
        unique_together = [("flag", "institution")]


class FeatureFlagAudit(models.Model):
    flag        = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE, related_name="audit_events")
    actor       = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    action      = models.CharField(max_length=40)  # enabled, disabled, rollout_changed, etc.
    field       = models.CharField(max_length=40, blank=True)
    old_value   = models.TextField(blank=True)
    new_value   = models.TextField(blank=True)
    reason      = models.TextField(blank=True)
    ip_address  = models.GenericIPAddressField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
```

---

## 9. Empty States

| Section | Copy | Visual |
|---|---|---|
| No flags (all tab) | "No feature flags yet. Create your first flag to start controlled rollouts." | Toggle icon |
| No flags (filtered) | "No flags match your current filters. Try adjusting or clearing filters." | Filter icon |
| No overrides | "No institution overrides for this flag." | Building icon |
| No audit history | "No audit events recorded for this flag yet." | Clock icon |
| No dependencies | "This flag has no dependencies configured." | Diagram icon |

---

## 10. Error States

| Error | Display |
|---|---|
| 2FA failure | Inline in modal: `bg-[#1A0A0A] border border-[#EF4444] p-3 rounded` "Invalid code. Try again." |
| Duplicate flag key | Inline under field: `text-[#F87171] text-xs` "A flag with this key already exists." |
| Circular dependency | In dependency tab: `bg-[#1A0A0A] border border-[#EF4444]` "Circular dependency detected." |
| Save failed (network) | Toast: "Save failed. Check connection and retry." `bg-[#450A0A]` |
| Kill-switch on flag with dependents | Modal shows warning: "{N} flags depend on this. Killing it may break their logic." with list |

---

## 11. Webhook Event Catalog

**Purpose:** Institutions on Professional and Enterprise plans can subscribe to platform events via webhooks — receiving real-time HTTP POST callbacks when events like `exam.result_published`, `student.enrolled`, or `institution.plan_changed` occur. PM Platform defines which events exist, what their payload looks like, and which plan tiers have access. This sits in Feature Flags because webhook access per event type is a feature-flag-like entitlement.

**Why here and not in Plan Config (page 04):** Webhook events are platform capabilities that can be individually toggled — exactly like feature flags. A new event type (e.g., `exam.proctoring_flag_raised`) can be released gradually (to 10% of Enterprise institutions first) before going to 100%.

---

### Event Catalog Table

| Event Type | Payload Fields | Trigger | Plan Access | Status | Rollout |
|---|---|---|---|---|---|
| `exam.result_published` | exam_id · institution_id · total_students · published_at | Results Coordinator publishes | Standard+ | ✅ Enabled | 100% |
| `student.enrolled` | student_id · series_id · institution_id · enrolled_at | Student enrols in test series | Professional+ | ✅ Enabled | 100% |
| `exam.started` | exam_id · institution_id · student_count · started_at | Exam session goes live | Professional+ | ✅ Enabled | 100% |
| `exam.submitted` | exam_id · student_id · submitted_at · attempt_id | Student submits exam | Enterprise | ✅ Enabled | 100% |
| `institution.plan_changed` | institution_id · old_plan · new_plan · effective_date | Plan upgrade/downgrade | Professional+ | ✅ Enabled | 100% |
| `payment.overdue` | institution_id · amount · due_date · days_overdue | Invoice 30+ days overdue | Standard+ | ✅ Enabled | 100% |
| `exam.proctoring_flag_raised` | exam_id · student_id · flag_type · timestamp | Proctoring detects anomaly | Enterprise | 🔨 Beta | 15% |
| `student.result_downloaded` | student_id · result_id · downloaded_at | Student downloads result PDF | Professional+ | ⬜ Draft | 0% |
| `institution.admin_changed` | institution_id · old_admin · new_admin · changed_at | Institution admin role reassigned | Standard+ | ⬜ Draft | 0% |

**Plan access column:** Which plan tiers can subscribe to this event. Controlled by Plan Config (page 04) — the entitlement is configured there; the event definition lives here.

**Status values:** Enabled (stable, all eligible institutions can subscribe) · Beta (rolling out, some eligible institutions) · Draft (defined but not yet released) · Deprecated (will be removed — existing subscribers warned)

---

### Webhook Event Detail Drawer (640px)

**Trigger:** Row click in Event Catalog
**Tabs: Definition · Subscribers · Payload Schema · Changelog**

**Tab A — Definition:**
- Event key (read-only, `font-mono`)
- Display name
- Description: plain text description of when this fires
- Plan access: dropdown (Starter / Standard / Professional / Enterprise)
- Rollout %: slider (same as feature flag rollout)
- Status toggle: Draft → Enabled → Deprecated

**Tab B — Subscribers:**
Table of institutions currently subscribed to this event:

| Institution | Plan | Endpoint URL | Added | Last delivery | Delivery health |
|---|---|---|---|---|---|
| Sri Chaitanya | Enterprise | `https://api.srichaitanya.in/hooks/edu` | Jan 5 | 2 min ago | ✅ 99.8% |
| Narayana Group | Enterprise | `https://erp.narayana.in/webhook/` | Feb 1 | 5 min ago | ✅ 99.9% |
| DPS Hyderabad | Professional | `https://dps-hyd.in/portal-hook` | Mar 10 | 8 hours ago | ⚠ 82% (degraded) |

Delivery health: % of last 1,000 deliveries that returned HTTP 2xx within 10s.
Degraded institutions (< 95% health) highlighted amber; PM can view failure logs.

**Tab C — Payload Schema:**
JSON schema definition of the event payload — read-only. Example:
```
exam.result_published payload:
{
  "event": "exam.result_published",
  "version": "1.2",
  "timestamp": "2026-03-20T14:30:00Z",
  "institution_id": "INST-1234",
  "data": {
    "exam_id": "EXM-8891",
    "total_students": 1240,
    "published_at": "2026-03-20T14:29:58Z",
    "result_url": "https://portal.srichaitanya.in/results/EXM-8891"
  }
}
```
**[Copy Schema]** · **[Download JSON Schema]**

**Tab D — Changelog:**
Version history of this event's payload schema:
- v1.2 (Mar 2026): Added `result_url` field
- v1.1 (Jan 2026): Added `total_students` field
- v1.0 (Oct 2025): Initial release

**Deprecation warning:** If PM marks an event as Deprecated, all subscriber institutions receive an email notification: "The event `exam.result_published` v1.0 will be retired on [date]. Migrate to v1.2 before [date]." A 90-day sunset period is mandatory.

---

### API Deprecation Lifecycle (flag-adjacent concern)

Some features also have API endpoint lifecycles managed here — when PM Platform decides to retire a v1 API endpoint:

1. PM adds a deprecation notice to the relevant feature flag: "API: `/v1/exams/list/` → sunset date: Jul 1, 2026"
2. Flag description shows deprecation banner in the flag drawer
3. All institutions using the deprecated endpoint appear in the Subscribers tab (detected from API gateway logs)
4. Announcement Manager (page 07) auto-notified to send deprecation notice to affected institutions
5. On sunset date: flag automatically kills the endpoint (kill-switch automation)

---

## 12. Security & Audit Requirements

- **Every flag change** writes to `FeatureFlagAudit` — actor, IP, old/new values, reason
- **Kill-switch actions** additionally write to the platform-wide Audit Log (div-a-17)
- **2FA required for:** enable, disable, kill-switch, rollout % change > 50%, bulk actions
- **Deprecation creates JIRA ticket** (optional) via webhook to JIRA API
- **Export** (CSV/JSON) is logged as an audit event
- **Permissions checked** server-side on every POST — client-side disable of buttons is UX only

---

## 12. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `N` | Open New Flag modal |
| `/` | Focus search input |
| `Esc` | Close drawer/modal |
| `↑ ↓` | Navigate table rows |
| `Enter` on row | Open Flag Detail Drawer |
| `Space` on row | Toggle row checkbox |
| `Ctrl+A` | Select all on current page |
| `E` | Enable selected flags |
| `D` | Disable selected flags |
