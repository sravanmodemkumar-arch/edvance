# Page Spec Writing Prompt

> **Purpose:** Paste this prompt (+ the target block at the bottom) into Claude to generate
> production-grade Django page specifications for any division.
> **Rule:** No Redis anywhere. Use ORM optimisation or Memcached only.

---

```
You are writing production-grade Django page specifications for a SaaS exam
platform (Srav). Each spec is a complete implementation blueprint — not a
summary or wireframe. Write consecutively, finish every file, never stop
to ask for confirmation.

════════════════════════════════════════════════════════
PLATFORM CONTEXT (always in scope)
════════════════════════════════════════════════════════

Architecture:
• Django CBV with LoginRequiredMixin + PermissionRequiredMixin
• HTMX partials: hx-get="?part=X", hx-target="#id", hx-swap="innerHTML"
• Poll-pause pattern:
    hx-trigger="every Xs[!document.querySelector('.modal-open,.drawer-open')]"
• Celery + database-backed cache for async tasks and background jobs
• PostgreSQL 15 multi-tenant (2,051 schemas: 2,050 tenant + 1 shared)
• AWS: Lambda · ECS · RDS Multi-AZ · CloudFront · S3 · KMS
  Secrets Manager · ACM · SES · Cost Explorer API
• Razorpay payments — no raw card data, tokenised only
• Flutter mobile (iOS + Android) — FCM push, Hive AES-256 local storage
• GST: SAC 9993 education services · CGST/SGST intra-state · IGST inter-state
• DPDPA 2023 compliance — student PII in ap-south-1 (Mumbai) only
• CERT-In: 6-hour breach reporting · DPDPA: 72-hour Data Protection Board notice
• Scale: 74,000 peak concurrent exam submissions · 2.4M–7.6M students

Caching strategy:
• NO Redis. Use Django's Memcached backend (django.core.cache) if a
  shared cache is needed, otherwise optimise at the ORM level first.
• Prefer: select_related / prefetch_related / annotate / values() / only()
  over any cache layer. Add Memcached only when a query cannot be made
  fast enough at the ORM level.

Role access levels:
  Level 1 = read-only
  Level 2 = limited writes
  Level 3 = full feature writes (PM / QA)
  Level 4 = engineering writes (infra, code, config)
  Level 5 = Platform Admin — unrestricted, all actions 2FA + audit-logged

UI conventions:
• Dark theme: bg-base #040810 · surface-1 #08101E · accent #6366F1
• Drawers: right-anchored, width stated per drawer
• Sensitive values: absent from DOM entirely (not CSS-hidden)
• Bulk actions: max stated per page (e.g. 200 items)
• Confirmation for destructive actions: type "DELETE" / "END" / confirm modal
• All date/time: IST (UTC+5:30), displayed as "DD MMM YYYY HH:MM IST"

════════════════════════════════════════════════════════
SOURCE FILES TO READ FIRST
════════════════════════════════════════════════════════

Before writing any page, read:
  1. The pages-list file for this division (provided below or in context)
  2. Any cross-referenced page descriptions (e.g. "integrates with C-09")
  3. The Role Summary table — understand what each role owns and cannot do
  4. The Scale Context table — every design decision must be defensible at scale
  5. The Key Architectural Decisions section (if present)
  6. The Compliance Obligations section (if present)
  7. The Role-to-Page Access Matrix — determines per-role read/write/no-access
  8. The Shared Drawers list — reuse, don't reinvent

════════════════════════════════════════════════════════
PAGE SPEC STRUCTURE — write every section for every page
════════════════════════════════════════════════════════

Each page spec file must contain ALL of the following sections.
Do not skip any section. Do not write placeholder text.

─── HEADER ────────────────────────────────────────────
# Page [ID] — [Page Name]

**Role:** [Role name]
**Route:** `/[url-path]/`
**Django View:** `[ViewClassName]`
**Template:** `[app/template/path.html]`
**Access:** `PermissionRequiredMixin` → `[app.permission_codename]`
**Poll interval:** [Xs / none]  ← state explicitly

─── SECTION 1: Purpose ───────────────────────────────
3–5 sentences. Answer: what job does this page let the role do, why does
it matter at scale, what happens if this page doesn't exist. Include
exact numbers from the Scale Context (2,051 schemas, 74K peak, etc.)

─── SECTION 2: URL & Routing ─────────────────────────
List every URL this page owns:
  /base-path/                    → main view
  /base-path/<id>/               → detail view (if needed)
  /base-path/<id>/action/        → action endpoints (POST)
  /base-path/export/             → export endpoints
  /base-path/live/               → HTMX partial poll endpoints

─── SECTION 3: Page Layout ───────────────────────────
Full ASCII box-drawing layout. Must include:
• Page title + action buttons (top right)
• Role-permission note if certain buttons are hidden for some roles
• Summary/KPI strip (4–6 stat cards)
• Tab bar (label every tab)
• Primary content for EACH tab (not just the first)
  - For tables: show column headers + 3–4 example data rows
  - For forms: show every field with type, placeholder, validation hint
  - For charts: label axes, show legend, state data source
  - For drawers: show a separate ASCII box for drawer content including all tabs
• Empty state (what shows when no data)
• Pagination controls if the list can exceed 50 rows

─── SECTION 4: HTMX Partial Map ──────────────────────
Table: `?part=` value → handler method → template partial → poll interval
For every tab and every live-updating component.

─── SECTION 5: Django View ───────────────────────────
Full Python class. Include:
• Class declaration with all mixins
• `get()` method with `_is_htmx()` dispatch
• Separate handler method for every `?part=` value
• All context variables built with optimised querysets
  (select_related, prefetch_related, annotate, values(), only())
• POST handler(s) with permission checks
• `_is_htmx()` static method
• Inline comments for non-obvious logic

─── SECTION 6: Models ────────────────────────────────
Full Django model definitions. Include:
• Every field with type, constraints, help_text
• ForeignKey / ManyToMany with on_delete, related_name
• choices tuples defined before the model (not inline strings)
• Meta: ordering, unique_together, indexes, verbose_name
• Properties or methods the view uses
• __str__
• No abstract or base classes — write concrete models only
• If a model already exists (e.g. Exam, Institution), reference it
  as a FK — do not redefine it

─── SECTION 7: Celery Tasks ──────────────────────────
Every async task this page triggers or depends on. For each task:
• @shared_task(queue='queue_name') decorator
• Full function body — no "# logic here" stubs
• Celery beat schedule entry (if periodic)
• What triggers it (user action / schedule / event)
• Retry policy if relevant (max_retries, countdown)
• What it does on failure (alert? mark error? retry?)

─── SECTION 8: DB Query Optimisation ─────────────────
No Redis. For every queryset in the view, state:

  QUERY:    what data it fetches
  ORM:      the exact .select_related() / .prefetch_related() /
            .annotate() / .values() / .only() / .defer() chain used
  INDEXES:  which DB index makes this fast (must exist in Section 10)
  VOLUME:   expected row count at scale
  CACHE:    if a Memcached cache.get/set is added, state:
              key pattern, TTL, when busted, which Django cache backend

Only add Memcached if the ORM alone cannot achieve acceptable latency.
Justify every cache addition with a specific volume/latency reason.

─── SECTION 9: Security ──────────────────────────────
Cover ALL of:
• Which permissions gate which actions (read vs write vs destructive)
• 2FA requirements (state: always / for destructive / never)
• What is absent from DOM for lower-access roles (not just CSS-hidden)
• Rate limiting (state req/min and which DRF throttle class)
• IDOR prevention (object-level permission checks)
• Sensitive value handling (masked in UI, absent from DOM, in Secrets Manager)
• Audit log: every write action → what is logged (actor, IP, before, after)
• Any DPDPA / CERT-In / compliance-specific controls on this page

─── SECTION 10: DB Schema ────────────────────────────
SQL DDL for all new tables:
• CREATE TABLE with column names + types + constraints
• All indexes (CREATE INDEX ON ...)
• Any partial indexes for common query patterns
• Foreign key constraints
• State which schema these live in: shared platform schema or per-tenant schema

─── SECTION 11: Validation Rules ─────────────────────
Markdown table:
| Rule | Detail |
|------|--------|
One row per validation. Cover:
• Field-level (type, length, pattern, range)
• Cross-field (field A valid only if field B is set)
• Business rules (cannot do X if Y is in state Z)
• Bulk action limits
• File upload limits (type, size, dimensions if image)
• Confirmation requirements for destructive actions

════════════════════════════════════════════════════════
FUNCTIONAL GAP ANALYSIS — run before writing any spec
════════════════════════════════════════════════════════

After reading the pages list but BEFORE writing the first spec:

1. For each role, enumerate every job they must do day-to-day.
2. Map each job to an existing page. If no page covers it → it is a gap.
3. Determine: does the gap need a NEW page, or an AMENDMENT to an existing one?
   • New page if: the gap is a primary workflow with its own data models
   • Amendment if: it is a tab/section that belongs naturally in an existing page
4. Add new pages to the pages-list (update the file).
5. Add gap amendments as a numbered list (G1, G2, …) at the bottom of
   the pages-list, then implement each amendment inside the relevant spec file
   using ## Amendment GX — [Name] sections.
6. Update the Functional Coverage Matrix and totals line.

Do NOT write "gap identified — will address later." Address all gaps immediately.

════════════════════════════════════════════════════════
CROSS-PAGE INTEGRATION — always describe
════════════════════════════════════════════════════════

For every page, explicitly name any other division/page it integrates with.
Example format in the spec:
  Integrates with:
  • Div B page 03 (Release Manager) — receives deploy approval gate
  • Div A page 12 (Incident Manager) — pushes P0 alerts to War Room
  • Div B page 24 (Performance Test Dashboard) — shares load test triggers

Use the exact page IDs so the links are unambiguous.

════════════════════════════════════════════════════════
QUALITY BAR — what "done" means for each section
════════════════════════════════════════════════════════

DONE means a senior Django/Celery/AWS engineer can implement the page
from the spec alone, without asking a single question. That means:

✅ Every model field has a type + constraint
✅ Every Celery task has a full function body — no stub bodies
✅ Every queryset uses explicit select_related/prefetch_related/annotate
✅ Every DB index in Section 10 matches the query pattern in Section 8
✅ Every form field has explicit validation (not just "required")
✅ Every destructive action states the 2FA requirement and confirmation UX
✅ ASCII layouts show real data — not placeholder rows
✅ Polling intervals are explicitly stated, not implied
✅ Role-based UI differences are explicit ("Backend Engineer sees this
   column; Frontend Engineer does not see this tab")
✅ No Redis anywhere — use ORM optimisation or Memcached only

NOT done if it contains:
❌ # TODO: implement
❌ similar to the pattern above
❌ add appropriate validation
❌ the usual auth checks apply
❌ Redis keys, Redis TTLs, or any redis-py / django-redis imports

════════════════════════════════════════════════════════
EXECUTION INSTRUCTIONS
════════════════════════════════════════════════════════

1. Read the pages-list file completely.
2. Run the Functional Gap Analysis. Update the pages-list file first.
3. Write all page specs in priority order (P0 → P1 → P2 → P3).
4. For each page:
   a. Write all 11 sections completely before moving to the next page.
   b. Include all amendments (GX) for that page at the bottom.
   c. Mark the page ✅ in the pages-list file immediately after completing it.
5. After all pages are done, do a final pass:
   • Confirm all cross-page references are consistent
   • Confirm all gap amendments are implemented
   • Update pages-list footer: total pages, gaps resolved, last updated date
6. Git: stage all new + modified files, commit with structured message,
   push to the current feature branch, then merge to main.

Do NOT stop between pages to ask for confirmation.
Do NOT stop when you discover a gap — fix it inline.
Do NOT write partial specs — every section, every page.
Do NOT use Redis anywhere in the output.
```

---

## How to use

Paste the prompt block above into Claude, then append one of the target blocks below.

---

### Division C — Engineering (18 pages)

```
TARGET: Division C — Engineering
Pages list:  docs/pages/group1/div-c/div-c-pages-list.md
Output dir:  docs/pages/group1/div-c/
Naming:      c-01-tenant-manager.md  →  c-18-incidents.md
Start:       gap analysis → P0 → P1 → P2
```

### Division D — Content (add when pages-list is ready)

```
TARGET: Division D — Content
Pages list:  docs/pages/group1/div-d/div-d-pages-list.md
Output dir:  docs/pages/group1/div-d/
Naming:      d-01-[name].md  →  d-XX-[name].md
Start:       gap analysis → P0 → P1 → P2
```

### Division E — Institution Portal (add when pages-list is ready)

```
TARGET: Division E — Institution Portal
Pages list:  docs/pages/group1/div-e/div-e-pages-list.md
Output dir:  docs/pages/group1/div-e/
Naming:      e-01-[name].md  →  e-XX-[name].md
Start:       gap analysis → P0 → P1 → P2
```

> For any new division: copy one of the target blocks above, swap the
> division letter, pages-list path, output dir, and naming pattern.
> The prompt body never changes.
