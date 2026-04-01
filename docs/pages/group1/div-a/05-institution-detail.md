# div-a-05 — Institution List

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total institutions | 2,050 |
| Schools | 1,000 |
| Colleges (Intermediate) | 800 |
| Institution Groups | 150 |
| Coaching Centres | 100 |
| Indian states | 28 |
| Plan tiers | Starter / Standard / Professional / Enterprise |
| SLA tiers | Standard / Professional / Enterprise |
| Status states | Active / Suspended / Churned / Onboarding / Trial |

**Why this matters:** The Institution List is the master directory. Any platform operator — COO, Ops, Support — lands here when they need to find an institution. It must handle power-user queries ("all Enterprise coaching centres in AP with > 10K students, no exam in 14 days") and resolve in under 500ms at 2,050 rows. Every row is a gateway to the full Institution Detail page (div-a-06).

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Institutions |
| Route | `/exec/institutions/` |
| Django view | `InstitutionListView` |
| Template | `exec/institution_list.html` |
| Priority | P1 |
| Nav group | Institutions |
| Required role | `exec`, `superadmin`, `ops`, `support` |
| 2FA required | No (read-only) |
| HTMX poll | None (on-demand only) |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Institutions                          [+ New Institution] [Export ▾] │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────────────────┤
│  Total   │  Active  │  Trial   │ Suspended│ Onboard- │  Net New             │
│  2,050   │  1,894   │   82     │   48     │ ing  26  │  +38 (30d)           │
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────────────────┤
│ [🔍 Search institutions...]                                                  │
│ [Type ▾] [State ▾] [Plan ▾] [SLA ▾] [Status ▾] [Students ▾] [Last Active ▾]│
│ Active filters: Type: Coaching × | State: AP ×                  [Clear all] │
├──────────────────────────────────────────────────────────────────────────────┤
│ [☐] [Bulk Actions ▾]  Sort: [Last Active ▾]  [Columns ▾]  Showing 1–25 / 127│
├──────────────────────────────────────────────────────────────────────────────┤
│ ☐ │ Institution      │ Type   │ State │ Plan   │ Students │ Exams │ Status  │
│   │ ABC Coaching Ctr │ Coach  │ AP    │ Enterp │ 12,400   │ 842   │ ● Active│
│   │ XYZ College      │ College│ TN    │ Prof   │ 1,800    │  94   │ ● Active│
│   │ ...                                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│ [← Prev]  1  2  3 … 82  [Next →]           Per page: [25 ▾]                 │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

**Container:** `flex gap-4 p-4` · 6 cards · `bg-[#0D1526] rounded-xl border border-[#1E2D4A]`
**No auto-poll** (list is on-demand; stale-while-revalidate on page load only)

| # | Card | Detail |
|---|---|---|
| 1 | Total | All institutions ever created (incl. churned) |
| 2 | Active | Status = Active |
| 3 | Trial | Status = Trial |
| 4 | Suspended | Status = Suspended |
| 5 | Onboarding | Status = Onboarding (< 30 days old, never ran exam) |
| 6 | Net New (30d) | New active institutions minus churned in last 30 days |

**KPI card anatomy (88px height):**
```
┌─────────────────────────────┐
│  Total                      │ ← label: text-xs text-[#64748B] uppercase tracking-wide
│  2,050                      │ ← value: text-2xl font-bold text-white data-count-up
│  ↑ +38 vs last month        │ ← delta: text-xs
└─────────────────────────────┘
```

---

### 4.2 Search Bar

`id="institution-search"` · full width below KPI strip
`<input type="text" placeholder="Search by name, ID, city, state, contact email...">`
**Styling:** `w-full bg-[#0D1526] border border-[#1E2D4A] rounded-xl px-4 py-3 text-white placeholder-[#475569]`
**Debounce:** 400ms · `hx-trigger="keyup changed delay:400ms"` · `hx-get="?part=table"` · `hx-include="#filter-form"` · `hx-target="#institution-table"` · `hx-swap="innerHTML"`
**Clear button:** `×` appears when input non-empty · inline right-side icon `text-[#64748B] hover:text-white`

---

### 4.3 Filter Bar

`id="filter-form"` · `flex flex-wrap gap-3 px-4 pb-3`

| Filter | Type | Options | HTMX behaviour |
|---|---|---|---|
| Type | Multi-select dropdown | All / School / College / Coaching / Group | Immediate trigger |
| State | Searchable multi-select | 28 states + UTs | Immediate trigger |
| Plan | Multi-select | Starter / Standard / Professional / Enterprise | Immediate trigger |
| SLA | Multi-select | Standard / Professional / Enterprise | Immediate trigger |
| Status | Multi-select | Active / Trial / Suspended / Onboarding / Churned | Immediate trigger |
| Students | Range dropdown | Any / < 500 / 500–2K / 2K–10K / > 10K | Immediate trigger |
| Last Active | Dropdown | Any / Today / 7d / 14d / 30d / 60d+ idle | Immediate trigger |

**Dropdown anatomy:** `relative` wrapper · button `flex items-center gap-2 bg-[#0D1526] border border-[#1E2D4A] rounded-lg px-3 py-2 text-sm text-[#94A3B8]` · chevron icon · panel: `absolute z-50 top-full mt-1 bg-[#0D1526] border border-[#1E2D4A] rounded-xl shadow-2xl min-w-[200px] p-2`

**Multi-select option item:** `flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-[#131F38] cursor-pointer` · checkbox `accent-[#6366F1]` · label `text-sm text-white`

**Active filter chips:** `flex flex-wrap gap-2 px-4 pb-2`
Each chip: `inline-flex items-center gap-1 text-xs bg-[#1E2D4A] text-[#94A3B8] px-2.5 py-1 rounded-full`
Remove button: `×` `hover:text-white cursor-pointer`
"Clear all filters" link: `text-xs text-[#6366F1] hover:text-[#818CF8] ml-2`

---

### 4.4 Table Toolbar

`flex items-center justify-between px-4 py-3 border-b border-[#1E2D4A]`

**Left side:**
- Select-all checkbox `accent-[#6366F1]` · indeterminate state when partial selection
- Bulk actions dropdown (disabled when 0 selected): [Suspend] [Activate] [Export selected] [Assign plan] · shows count badge "3 selected"
- Sort: `[Last Active ▾]` dropdown — options: Last Active / Name A–Z / Students ↓ / ARR ↓ / Joined Date ↓

**Right side:**
- Column visibility: `[Columns ▾]` dropdown · toggleable columns listed with checkboxes
- "Showing X–Y of Z" text `text-sm text-[#94A3B8]`
- Result count updates via `hx-swap-oob` on every table refresh

---

### 4.5 Institution Table

`id="institution-table"` `hx-get="/exec/institutions/?part=table"` `hx-trigger="load" hx-swap="innerHTML"`

**Container:** `bg-[#0D1526] rounded-xl border border-[#1E2D4A] overflow-x-auto`

**Table:** `w-full text-sm`
**Head row:** `bg-[#070C18] text-[#64748B] text-xs uppercase tracking-wider`
**Each `th`:** `px-4 py-3` · sortable columns have `cursor-pointer hover:text-white` + `↑↓` sort indicator
**Body row:** `border-b border-[#131F38] hover:bg-[#131F38] cursor-pointer transition-colors` · click anywhere → opens Institution Quick-View Drawer

#### Column Specifications

| Column | Sortable | Width | Detail |
|---|---|---|---|
| ☐ | — | 40px | Checkbox; click selects row for bulk actions |
| Institution | ✓ | 240px | Name (truncate at 36 chars) + `title` full name + type icon SVG 16px left · Group: expand chevron `▶` |
| Type | ✓ | 100px | Badge pill: School `bg-[#1E3A5F] text-[#60A5FA]` · College `bg-[#064E3B] text-[#34D399]` · Coaching `bg-[#451A03] text-[#FCD34D]` · Group `bg-[#2E1065] text-[#A78BFA]` |
| State | ✓ | 120px | State abbreviation + full name on hover tooltip |
| Plan | ✓ | 120px | Plan badge: Starter grey · Standard blue · Professional indigo · Enterprise gold |
| SLA | ✓ | 100px | SLA badge: Standard `text-[#64748B]` · Professional `text-[#6366F1]` · Enterprise `text-[#F59E0B]` |
| Students | ✓ | 100px | Count with `K` suffix if ≥ 1000 · right-aligned `font-mono` |
| Total Exams | ✓ | 100px | All-time exam count · right-aligned |
| Last Active | ✓ | 120px | Relative time (e.g., "2h ago" / "3d ago") · red if > 14d |
| Health Score | ✓ | 100px | 0–100 score · coloured badge: ≥ 80 green · 60–79 amber · < 60 red |
| Status | ✓ | 110px | Status dot + label: Active `#34D399` · Trial `#60A5FA` · Suspended `#F87171` · Onboarding `#FCD34D` |
| Actions ⋯ | — | 48px | Kebab menu → [View Detail] [Edit] [Suspend/Activate] [View Invoices] [Login as Admin] |

**Group row expand behaviour:** Coaching groups have `▶` chevron in Name cell
`hx-get="?part=children&group_id={id}"` `hx-target="#group-children-{id}"` `hx-swap="innerHTML"`
Child rows render with 24px left-indent · chevron rotates 90° on expand · `hx-indicator` shows spinner in name cell

**Row loading skeleton (on table refresh):** 10 rows of:
`<tr class="animate-pulse"><td><div class="h-4 bg-[#1E2D4A] rounded w-3/4"></div></td>...</tr>`

---

### 4.6 Pagination Strip

`flex items-center justify-between px-4 py-3 border-t border-[#1E2D4A]`

**Left:** "Showing 1–25 of 127 institutions" · `text-sm text-[#94A3B8]`
**Center:**
- [← Prev] button · `disabled:opacity-30` when on page 1
- Page pills: first page · ... · current-2 · current-1 · [current] · current+1 · current+2 · ... · last page
- Active page: `bg-[#6366F1] text-white rounded-lg px-3 py-1`
- Inactive page: `text-[#94A3B8] hover:bg-[#131F38] rounded-lg px-3 py-1`
- [Next →] button · disabled on last page
**Right:** Per-page `<select>` · options: 10 / 25 / 50 / 100 · `bg-[#131F38] border border-[#1E2D4A] rounded-lg px-2 py-1 text-sm`

**HTMX on page change:** `hx-get="?part=table&page={n}&per_page={pp}"` · `hx-target="#institution-table"` · `hx-swap="innerHTML"` · `hx-push-url="true"` (URL updates so page is bookmarkable)

---

## 5. Drawers

### 5.1 Institution Quick-View Drawer (480 px)

Triggered by row click. Slides in from right.
`id="institution-drawer"` · `w-[480px] fixed right-0 top-0 h-full bg-[#0D1526] border-l border-[#1E2D4A] z-50`
`body.drawer-open` added on open.

**Header (64px):**
`flex items-center justify-between px-6 py-4 border-b border-[#1E2D4A]`
- Left: Institution name `text-lg font-semibold text-white` + type badge
- Right: `[Open Full Profile →]` button (links to div-a-06) + `[×]` close

**Tab bar (4 tabs):**
`flex border-b border-[#1E2D4A] px-6`
Tabs: Overview · Exams · Billing · Contacts

**Tab A — Overview:**
- Status badge + last active time
- Key metrics row: Students · Exams (total) · ARR · Health Score
- Plan + SLA tier row
- State · District · City
- Onboarded date
- Assigned customer success rep
- Recent activity timeline (last 5 events): `text-xs text-[#94A3B8]`

**Tab B — Exams:**
- Last 10 exams table: Name · Date · Students · Status · Score avg
- [View All Exams →] link → div-a-03 with institution filter

**Tab C — Billing:**
- Current plan + ARR
- Last invoice: amount + status (Paid/Overdue) + date
- Next renewal date
- Outstanding balance (if any) — red if > 0
- [View All Invoices →] link → div-a-10

**Tab D — Contacts:**
- Primary contact: Name · Role · Email · Phone
- Billing contact (if different)
- Technical contact (if different)
- [Edit Contacts] button

**Drawer footer (56px):**
`flex gap-3 px-6 py-4 border-t border-[#1E2D4A] bg-[#070C18]`
[Open Full Profile →] [Edit] [Suspend] [Close]

---

## 6. Modals

### 6.1 New Institution Modal (640 px)

Triggered by [+ New Institution] header button. **2FA required.**

**Header:** "Create Institution" · `[×]`

**Step indicator:** Step 1 of 3 — Basic Info · Step 2 of 3 — Plan & SLA · Step 3 of 3 — Contacts

**Step 1 — Basic Info:**
| Field | Type | Validation |
|---|---|---|
| Institution name | Text input | Required · min 3 chars · unique check via `hx-get="?part=check_name"` |
| Institution type | Radio group | School / College / Coaching / Group |
| Parent group | Searchable dropdown | Only shown if type ≠ Group |
| State | Dropdown | 28 states + UTs |
| District | Dropdown (loaded by state) | `hx-get="?part=districts&state={id}"` |
| City | Text input | |
| Website | URL input | Optional · HTTPS validated |

**Step 2 — Plan & SLA:**
| Field | Type | Detail |
|---|---|---|
| Subscription plan | Radio group with pricing | Starter / Standard / Professional / Enterprise |
| SLA tier | Radio group | Standard / Professional / Enterprise |
| Billing cycle | Toggle | Monthly / Annual |
| Expected student count | Number input | Used for capacity planning |

**Step 3 — Contacts:**
| Field | Type |
|---|---|
| Primary contact name | Text |
| Primary contact email | Email + uniqueness check |
| Primary contact phone | Tel |
| Admin email (login) | Email |

**Footer:** [Back] [Next →] (steps 1–2) or [Cancel] [Create Institution] (step 3)

**POST:** `hx-post="/exec/institutions/?part=create"` · `hx-swap="outerHTML"` on success shows confirmation · on error shows inline field errors

---

### 6.2 Bulk Actions Confirmation Modal (480 px)

When bulk action selected with N rows checked.

**Header:** e.g., "Suspend 3 institutions?"

**Body:** Table of selected institutions (name, type, status) · warning text if action is irreversible

**Footer:** [Cancel] [Confirm Action]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/inst_list_kpi.html` | Page load |
| `?part=table` | `exec/partials/inst_table.html` | Page load · search · filter · sort · page change |
| `?part=children&group_id={id}` | `exec/partials/inst_group_children.html` | Group row expand click |
| `?part=drawer&id={id}` | `exec/partials/inst_quick_drawer.html` | Row click |
| `?part=check_name` | JSON response | Name uniqueness check (modal step 1) |
| `?part=districts&state={id}` | HTML `<option>` list | State dropdown change (modal step 1) |
| `?part=create` | `exec/partials/inst_create_result.html` | Modal form POST |

**Django view dispatch:**
```python
class InstitutionListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_institutions"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/inst_list_kpi.html",
                "table": "exec/partials/inst_table.html",
                "children": "exec/partials/inst_group_children.html",
                "drawer": "exec/partials/inst_quick_drawer.html",
                "districts": "exec/partials/district_options.html",
            }
            if part == "check_name":
                name = request.GET.get("name", "")
                exists = Institution.objects.filter(name__iexact=name).exists()
                return JsonResponse({"exists": exists})
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/institution_list.html", ctx)

    def post(self, request):
        if _is_htmx(request) and request.GET.get("part") == "create":
            return self._handle_create(request)
        return HttpResponseNotAllowed(["GET"])
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 200 ms | > 500 ms |
| Table load (25 rows, default filters) | < 400 ms | > 1 s |
| Search with debounce (complex query) | < 500 ms | > 1.2 s |
| Group row expand (50 children) | < 300 ms | > 800 ms |
| Quick-view drawer open | < 250 ms | > 700 ms |
| Full page initial load | < 1 s | > 2.5 s |
| Export CSV (2,050 rows) | < 3 s | > 8 s |

**Caching strategy:** Table queries use DB indexes on `(type, state, plan, status, last_active)`. KPI counts are Redis-cached (TTL 60s). No Redis for table (filters vary too much; use read replica instead).

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| 0 results for filters | Empty state: icon + "No institutions match your filters" + [Clear all filters] button |
| All filters cleared | Full 2,050 rows with default sort (last active desc) |
| > 1,000 results | Show first page with "Showing 1–25 of 1,247" — no full count scan (use `COUNT(*)` with LIMIT guard) |
| Suspended institution row | Row background `bg-[#1A0A0A]` (subtle red tint) |
| Institution with overdue invoice | Show `⚠` amber icon in Status column with tooltip "Overdue invoice: ₹X.XX L" |
| Institution health score < 50 | Show `🔴` in Health column; row not highlighted (only indicator) |
| Group with 0 children | No expand chevron shown |
| Login as Admin action | Requires 2FA re-prompt before proceeding; shows confirmation modal |
| Bulk action on 0 rows | [Bulk Actions] button disabled |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `F` | Focus search input |
| `N` | Open New Institution modal |
| `E` | Export current filtered list |
| `↑` / `↓` | Navigate table rows |
| `Enter` | Open Quick-View drawer for focused row |
| `Space` | Toggle row selection (when table focused) |
| `Esc` | Close drawer/modal; clear search if drawer not open |
| `?` | Keyboard shortcut help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/institution_list.html` | Full page shell |
| `exec/partials/inst_list_kpi.html` | KPI strip |
| `exec/partials/inst_table.html` | Table body + pagination |
| `exec/partials/inst_group_children.html` | Expandable group child rows |
| `exec/partials/inst_quick_drawer.html` | Quick-view drawer (4 tabs) |
| `exec/partials/inst_create_modal.html` | New Institution modal (3 steps) |
| `exec/partials/inst_bulk_confirm_modal.html` | Bulk action confirmation |
| `exec/partials/district_options.html` | District `<option>` list for modal |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `SearchInput` | §4.2 |
| `MultiSelectDropdown` | §4.3 filters |
| `FilterChip` | §4.3 active chips |
| `TableToolbar` | §4.4 |
| `BulkActionsDropdown` | §4.4 |
| `InstitutionTable` | §4.5 |
| `TypeBadge` | §4.5 Type column |
| `PlanBadge` | §4.5 Plan column |
| `StatusDot` | §4.5 Status column |
| `HealthScoreBadge` | §4.5 Health column |
| `KebabMenu` | §4.5 Actions column |
| `GroupExpandRow` | §4.5 Group rows |
| `PaginationStrip` | §4.6 |
| `DrawerPanel` | §5.1 |
| `TabBar` | §5.1 drawer tabs |
| `StepWizard` | §6.1 modal |
| `ModalDialog` | §6.1–6.2 |
