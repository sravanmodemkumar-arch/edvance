# 03 — Release Manager

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total institutions impacted per release | 2,050 |
| Students indirectly impacted | 2.4M–7.6M |
| Peak concurrent users during release window | Up to 74,000 |
| Releases per quarter | 6–8 production releases |
| Hotfixes per quarter | 4–8 emergency hotfixes |
| Average items per release | 8–15 features/fixes |
| Feature flags deployed per release | 3–8 flags per release |
| DB migrations per release | 0–5 (zero-downtime migrations only) |
| Deployment window | Weeknights 11 PM–2 AM IST (off-peak) |
| Rollback window (SLA) | Must be reversible within 15 min |

**Why this page matters at scale:** With 2,050 institutions and 2.4M+ students depending on the platform, a bad release during exam day is catastrophic. At 74K concurrent exam submissions, even a 99.9% uptime SLA means 74 students affected per second of downtime. This page manages the entire release lifecycle — from planning to QA sign-off to staged deployment to rollback — so that PM Platform, QA, and Engineering have one shared source of truth. The changelog editor here is what institutions read in their "What's New" section.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Release Manager |
| Route | `/product/releases/` |
| Detail route | `/product/releases/<release_id>/` |
| Django view class | `ReleaseManagerView` |
| Template | `product/release_manager.html` |
| Permission — view | `portal.view_releases` (all div-b roles) |
| Permission — manage | `portal.manage_releases` (PM Platform only) |
| Permission — deploy | `portal.deploy_release` (PM Platform + 2FA) |
| Permission — rollback | `portal.rollback_release` (PM Platform + CTO override + 2FA) |
| 2FA required | Yes — deploy to production, rollback, close release |
| HTMX poll — pipeline board | Every 60s (paused when drawer/modal open) |
| HTMX poll — staging checks | Every 30s when staging release exists |
| Nav group | Product |
| Nav icon | `rocket` |
| Priority | P1 |

---

## 3. Wireframe

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Release Manager          [+ New Release]  [Export Changelog]  [View Archive]│
├──────────┬──────────┬──────────┬──────────┬──────────┬───────────────────────────────┤
│ Total    │ Planning │ In Dev   │ Staging  │ In Prod  │ Avg Cycle Time                │
│Releases  │    3     │    2     │    1     │    1     │  14.2 days                    │
│  (Q1:8)  │          │          │ v2.4.1   │ v2.4.0   │  ↓2.1d vs last Q             │
├──────────┴──────────┴──────────┴──────────┴──────────┴───────────────────────────────┤
│ TABS: [Pipeline (Kanban)] [All Releases] [Hotfixes] [Changelogs] [Deployment Log]    │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ TAB: PIPELINE (KANBAN)                                                              │
│                                                                                     │
│ ┌─ PLANNING ─────┐  ┌─ DEVELOPMENT ──┐  ┌─ STAGING ──────┐  ┌─ PRODUCTION ───────┐│
│ │ v2.5.0         │  │ v2.4.2         │  │ v2.4.1         │  │ v2.4.0             ││
│ │ Q2 Target      │  │ Target: Apr 2  │  │ ● QA in progr. │  │ ✓ Deployed Mar 10  ││
│ │ 6 items        │  │ 9 items        │  │ Target: Mar 25 │  │ 8 items shipped    ││
│ │ [Edit]         │  │ 2 blockers     │  │ 1 P0 blocker   │  │ Uptime: 99.97%     ││
│ │                │  │ [Edit]         │  │ [View Details] │  │ [View Details]     ││
│ │ v2.4.3         │  │                │  │                │  │                    ││
│ │ Hotfix planned │  │                │  │                │  │                    ││
│ └────────────────┘  └────────────────┘  └────────────────┘  └────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

**Container:** `flex gap-4 p-4` · 6 cards · `bg-[#0D1526] rounded-xl border border-[#1E2D4A]`
**Poll:** `hx-get="?part=kpi" hx-trigger="every 60s[!document.querySelector('.drawer-open,.modal-open')]" hx-target="#kpi-strip" hx-swap="outerHTML"`

| # | Card | Value Format | Delta | Alert |
|---|---|---|---|---|
| 1 | Total Releases (quarter) | `8` | vs last quarter | — |
| 2 | Planning | `3` | — | — |
| 3 | In Development | `2` | — | — |
| 4 | In Staging | `1` release name | — | If > 14d in staging = amber |
| 5 | In Production | `1` release name + deploy date | — | — |
| 6 | Avg Cycle Time | `14.2 days` | `↓2.1d` vs last Q | > 21d = amber |

**Staging card:** shows release name badge `v2.4.1` + progress bar of QA checks completed `7/12`
**Production card:** shows release name + uptime since deploy (e.g., `99.97% · 12d stable`)

---

### 4.2 Tab Bar

| Tab | hx-get | Description |
|---|---|---|
| Pipeline (Kanban) | `?part=pipeline` | Visual Kanban board — drag-and-drop between stages |
| All Releases | `?part=all_releases` | Full sortable/filterable table of all releases |
| Hotfixes | `?part=hotfixes` | Emergency patches only — separate fast-track workflow |
| Changelogs | `?part=changelogs` | Published changelogs per release — institution-facing |
| Deployment Log | `?part=deploy_log` | Every deployment event with actor, time, environment, result |

---

### 4.3 Tab: Pipeline (Kanban)

**Container:** `grid grid-cols-4 gap-4 p-4`
**Poll:** `hx-get="?part=pipeline" hx-trigger="every 60s[!document.querySelector('.drawer-open,.modal-open')]" hx-target="#pipeline-board" hx-swap="innerHTML"`

#### 4.3.1 Column Definitions

| Column | Status | Header colour | Card count |
|---|---|---|---|
| Planning | `planning` | `text-[#94A3B8]` | Unlimited |
| Development | `development` | `text-[#F59E0B]` | Max 3 concurrent |
| Staging | `staging` | `text-[#6366F1]` | Max 2 concurrent |
| Production | `production` | `text-[#10B981]` | Shows last 3 deployed |

Column header: `flex justify-between items-center px-3 py-2`
- Title: `text-xs font-semibold uppercase tracking-wider`
- Count badge: `text-xs bg-[#1E2D4A] text-[#94A3B8] px-1.5 py-0.5 rounded-full`

#### 4.3.2 Release Card (in Kanban)

`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4 mb-3 cursor-pointer hover:border-[#6366F1] transition-colors`

**Card content layout:**
```
[Version badge]  [Type badge]           [Risk badge]
Release name
Target date · Cycle time so far
────────────────────────────
Items: 9  ·  Bugs: 3  ·  Flags: 4
QA: ████████░░  7/12 checks
[QA Lead avatar] [Blocker count: 2 ⚠]
```

**Version badge:** `font-mono text-xs bg-[#131F38] px-2 py-0.5 rounded`

**Type badge:**
- Feature Release: `bg-[#312E81] text-[#A5B4FC]`
- Hotfix: `bg-[#450A0A] text-[#F87171]`
- Security Patch: `bg-[#1A0A0A] text-[#F87171] border border-[#EF4444]`

**Risk badge:**
- Low: `bg-[#064E3B] text-[#34D399]`
- Medium: `bg-[#451A03] text-[#FCD34D]`
- High: `bg-[#450A0A] text-[#F87171]`
- Critical: `bg-[#EF4444] text-white animate-pulse`

**QA progress bar:** `bg-[#1E2D4A] rounded-full h-2` fill `bg-[#6366F1]` · `{N}/{total} checks` label

**Blocker count:** `text-xs text-[#F87171]` — shown only when > 0 blockers

**Card click:** opens Release Detail Drawer (640px)

**Stage advance button (bottom of card):**
- Planning → Development: [Move to Development]
- Development → Staging: [Move to Staging] — requires QA approval toggle
- Staging → Production: [Deploy to Production] — requires 2FA + all QA checks passed
- Available only to PM Platform role

**Drag-and-drop:** `draggable="true"` on each card — `hx-post="?action=move_release" hx-vals='{"release_id": X, "new_status": "staging"}'`
Visual drop zone: `border-2 border-dashed border-[#6366F1]` on hover

#### 4.3.3 Staging Automated Checks Panel

Shown below Staging column when a release is in staging:
`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4 mt-4`
**Poll:** `hx-get="?part=staging_checks" hx-trigger="every 30s[!document.querySelector('.drawer-open,.modal-open')]"`

| Check | Status | Duration | Last Run |
|---|---|---|---|
| DB migration dry-run | ✅ Pass | 2.4s | 5m ago |
| API smoke tests (47 endpoints) | ✅ Pass | 18s | 5m ago |
| HTMX partial load tests | ✅ Pass | 7s | 5m ago |
| Feature flag validation | ⏳ Running | — | now |
| Performance baseline | ✅ Pass | 45s | 5m ago |
| Security scan | ✅ Pass | 120s | 5m ago |
| Rollback dry-run | ⬜ Not run | — | — |
| Exam day scenario test | ❌ Fail | 38s | 5m ago |

**[Run All Checks]:** `bg-[#6366F1]` · `hx-post="?action=run_staging_checks"`
**[Run Failed Only]:** `bg-[#131F38]` — re-runs only failed checks

Exam day scenario failure — expanded inline:
`bg-[#1A0A0A] border border-[#EF4444] rounded p-3 text-xs text-[#F87171]`
"Exam day scenario test failed: 74K concurrent submission test failed at 68K (target: 74K+10%=81K). P99 latency: 2,840ms (threshold: 2,000ms). [View Full Report]"

---

### 4.4 Tab: All Releases

**Toolbar:**

| Control | Type | Options |
|---|---|---|
| Search | Text · debounce 300ms | Release version or name |
| Status | Multi-select | Planning · Development · Staging · Production · Rolled Back · Archived |
| Type | Multi-select | Feature Release · Hotfix · Security Patch · DB Migration |
| Quarter | Dropdown | Q1 2026 · Q2 2026 · Q3 2025 · All |
| Risk Level | Multi-select | Low · Medium · High · Critical |
| [Apply] | Button | `bg-[#6366F1]` |

**Table columns:**

| Column | Width | Sortable |
|---|---|---|
| Version | 100px | Yes |
| Release Name | 200px | Yes |
| Type | 120px | Yes |
| Status | 120px | Yes |
| Risk | 100px | Yes |
| Items | 80px | Yes |
| Target Date | 120px | Yes |
| Deploy Date | 120px | Yes |
| Cycle Time | 100px | Yes |
| QA Sign-off | 120px | No |
| Actions ⋯ | 48px | — |

**Status badge colours:**
- Planning: `bg-[#1E2D4A] text-[#94A3B8]`
- Development: `bg-[#451A03] text-[#FCD34D]`
- Staging: `bg-[#312E81] text-[#A5B4FC]`
- Production: `bg-[#064E3B] text-[#34D399]`
- Rolled Back: `bg-[#450A0A] text-[#F87171]`
- Archived: `bg-[#1E2D4A] text-[#475569] opacity-60`

**Row state — rolled back:** `bg-[#1A0A0A] border-l-4 border-[#EF4444]`

**Kebab menu (⋯):**
- View Details → opens Release Detail Drawer
- Edit Release → opens Release Edit Drawer (PM Platform only)
- Move to Staging → stage advance (with confirmation)
- Deploy to Production → 2FA modal
- Rollback → 2FA modal (only for production releases)
- Archive → confirmation
- Delete → confirmation (only planning stage)

**Pagination:** 10/25/50 per page · "Showing X–Y of Z"

---

### 4.5 Tab: Hotfixes

**Purpose:** Emergency patches that bypass the standard planning cycle. Fast-track: Hotfix Created → Staging (1h) → Production (4h target).

**SLA column:** shows time since hotfix created · amber if > 4h · red if > 8h
**Priority column:** P0 (same day) · P1 (next business day)

**[+ New Hotfix]** button: smaller modal than full release — fewer required fields, auto-set to High risk.

**Table columns:**
Version · Description · Severity · Status · Created · Time in Pipeline · Deploy ETA · Actions ⋯

---

### 4.6 Tab: Changelogs

**Purpose:** Institution-facing release notes. What institutions see in their "What's New" panel.

#### 4.6.1 Changelog List

Left sidebar (240px): list of all deployed releases
Each item: version + date + `[Published ✓]` or `[Draft]`
Selected release highlights: `bg-[#131F38] border-l-2 border-[#6366F1]`

#### 4.6.2 Changelog Editor (right panel)

**Mode toggle:** [Edit] · [Preview]

**Edit mode:**
`textarea.bg-[#131F38] border border-[#1E2D4A] font-mono text-sm text-[#F1F5F9] p-4 rounded-xl w-full`
Height: `min-h-[400px]`
Supports Markdown. Toolbar: **B** · *I* · `Code` · `## Heading` · `- List` · `[Link]`

**Changelog sections structure (auto-template):**
```markdown
## What's New in v2.4.1

### ✨ New Features
- [Institution Portal] Student leaderboard now shows district rank
- [Exam Engine] Timer pause-on-network-loss with grace period

### 🐛 Bug Fixes
- Fixed: Exam result PDF export failing for >5,000 students
- Fixed: WhatsApp notification not sending for group institutions

### ⚡ Performance
- Exam submission throughput improved by 18%

### 🔒 Security
- Session token rotation interval reduced from 24h to 8h

> This update was deployed on 25 Mar 2026 at 1:15 AM IST.
> Downtime: 0 minutes (zero-downtime deployment).
```

**Target audience toggle:** [All Institutions] · [Schools only] · [Coaching only] · [Enterprise plan only]
Creates audience-specific changelogs from the same base.

**Auto-generate from items button:** [Auto-generate from Release Items]
Pulls all items in the release and creates a draft changelog grouped by type.

**Preview mode:** rendered Markdown · institution portal preview frame (400px wide) showing how it looks in the institution's "What's New" panel.

**Publish button:** [Publish Changelog] → makes it visible to institutions
**Schedule button:** [Schedule → date/time picker] → auto-publishes at set time
**Unpublish:** [Unpublish] → removes from institution view

**Status:** Draft / Scheduled / Published / Unpublished badges

---

### 4.7 Tab: Deployment Log

**Purpose:** Full audit trail of every deployment event — who deployed, when, to which environment, result.

**Filter toolbar:** Date range · Environment · Result (success/failed/rolled-back) · Deployed by

**Table:**

| Column | Detail |
|---|---|
| # | Sequential deployment number |
| Release | Version badge |
| Environment | Staging · Production |
| Deployed By | Staff name |
| Started | Absolute timestamp |
| Duration | Minutes:Seconds |
| Result | ✅ Success · ❌ Failed · ↩ Rolled Back |
| DB Migrations | Count · `0 migrations` or `3 migrations applied` |
| Flags Deployed | Count of flag state changes |
| Downtime | `0s` or duration in seconds |
| Notes | Short note from deployer |
| Actions | [View Full Log] [Download Log] |

**[View Full Log]:** opens Deployment Log Drawer (640px) with:
- Full stdout/stderr log output in `font-mono text-xs`
- DB migration details
- Flag change events
- Rollback instructions (if rolled back)
- Timeline: Started → DB Migrations → Service Restart → Health Checks → Complete

---

## 5. Drawers

### 5.1 Release Detail Drawer (640px)

**Trigger:** Kanban card click / All Releases row click
**Header:** Version badge + Release name + Status badge + Risk badge + `[×]`

**Tab bar (6 tabs):**

---

#### Tab A — Overview

**Two-column layout:**

Left:
- Target date · Actual deploy date · Cycle time (days)
- Release owner (PM name)
- Description (editable)
- Risk level (editable dropdown: Low/Medium/High/Critical)
- Risk justification text area

Right:
- Items summary: Features `6` · Bugs `3` · Performance `1` · Security `1` · Total `11`
- Flags included: `4 flags` link → shows Tab C
- DB Migrations: `2 migrations` badge
- Linked JIRA epic: clickable link

**Progress bar:** `Planning → Development → Staging → Production`
Current stage highlighted in `bg-[#6366F1]`
Step labels: `text-xs text-[#94A3B8]`

**Stage advance button:**
`bg-[#6366F1] text-white px-4 py-2 rounded-lg text-sm`
Label changes by current stage: "Move to Development" / "Move to Staging" / "Deploy to Production"
"Deploy to Production" requires 2FA — inline 2FA verification field appears.

---

#### Tab B — Changelog / Items

**Two sub-tabs:** [Items (internal)] · [Changelog (institution-facing)]

**Items view:**
Table of all release items:
| # | Type | Title | Module | JIRA | Status | Added by |
|---|---|---|---|---|---|---|

Type badges: Feature · Bug Fix · Performance · Security · Documentation
Status: Planned · In Dev · Done · Blocked

[+ Add Item] → inline row insert:
- Type dropdown
- Title text
- Module dropdown (20 modules)
- JIRA ticket text
- Status

**Drag handles** on rows: reorder items

**Changelog view:**
Same as §4.6.2 but scoped to this drawer (smaller preview)

---

#### Tab C — Feature Flags

Table of all flags linked to this release:

| Flag Key | Flag Name | Status Change | Rollout % | When | Impact |
|---|---|---|---|---|---|
| `new_exam_ui` | New Exam Interface v3 | Disabled → 10% partial | 10% | On deploy | ~205 institutions |
| `batch_export_v2` | Batch Export v2 | 50% → 100% | 100% | On deploy | All 2,050 |

**[Link Flag]** button → search and select flags from Feature Flags page
**[Remove]** per row

**Risk assessment:**
If any flag changes affect > 50% of institutions: amber warning banner
If any flag has kill-switch activated in this release: red warning banner

---

#### Tab D — QA Sign-off

**Checklist of sign-offs required before production deploy:**

| # | Check | Required By | Status | Signed Off By | Time |
|---|---|---|---|---|---|
| 1 | Automated tests pass (all suites) | QA Engineer | ✅ | Ravi K. | Mar 23 14:32 |
| 2 | Exam day scenario test (74K) | QA Engineer | ❌ | — | — |
| 3 | Performance baseline met | QA Engineer | ✅ | Ravi K. | Mar 23 14:40 |
| 4 | Security scan clean | Security Engineer | ✅ | Auto | Mar 23 14:35 |
| 5 | DB migration dry-run | DBA | ✅ | Suresh M. | Mar 23 16:00 |
| 6 | Rollback tested | QA Engineer | ⬜ | — | — |
| 7 | Changelog drafted | PM Platform | ✅ | Priya S. | Mar 23 17:00 |
| 8 | Stakeholder sign-off | PM Platform | ⬜ | — | — |

**Release readiness gate:**
`bg-[#0D1526] rounded-xl p-4 border border-[#1E2D4A]`
Gauge: `0–100` · current: 75 (6/8 checks complete)
"2 sign-offs remaining before production deploy is unlocked"

**[Sign Off] buttons:** only shown to role that owns each check
**2FA required** for PM's stakeholder sign-off and Deploy button

**Override (emergency):** [Force Deploy — Override QA Gate]
`bg-[#450A0A] text-[#F87171]` — only CTO/CEO (Level 5)
Opens Emergency Deploy Modal requiring typed acknowledgement + 2FA

---

#### Tab E — DB Migrations

**Migration list:**

| # | Migration File | App | Type | Reversible | Dry-run Status |
|---|---|---|---|---|---|
| 1 | `0042_add_flag_domain_index` | product | Add Index | ✅ Yes | ✅ Passed |
| 2 | `0043_alter_institution_plan` | institutions | Alter Column | ✅ Yes | ✅ Passed |

**Zero-downtime migration rules panel:**
`bg-[#0D1526] rounded p-3 text-xs text-[#94A3B8]`
Each migration must:
- ✅ Use `db_index=True` not raw SQL index (concurrent build)
- ✅ Not drop columns until data migration complete (2-release cycle)
- ✅ Be reversible (rollback must work)
- ✅ Dry-run must pass on staging

**[Run Dry-run]** button: `hx-post="?action=run_migration_dryrun&release_id={id}"`

---

#### Tab F — Rollback

`bg-[#1A0A0A] border border-[#EF4444] rounded-xl p-4`

**Rollback target:** "Will roll back to v2.3.2 (deployed 10 Mar 2026)"

**Impact summary:**
- `{N}` DB migrations to reverse (list them)
- `{N}` feature flags will revert to previous state (list them)
- Estimated rollback duration: `~8 minutes`
- Estimated downtime: `~2 minutes`

**Rollback steps preview (read-only):**
1. Stop incoming traffic (CloudFront WAF rule)
2. Revert feature flags to v2.3.2 state
3. Run DB migration reverse (django migrate app 0041)
4. Deploy v2.3.2 container image
5. Health checks (3 passing required)
6. Re-enable traffic

**[Initiate Rollback]:** `bg-[#EF4444] text-white`
→ Opens Rollback Confirmation Modal (2FA + typed reason + CTO acknowledgement)
Only available when release status = `production`

---

**Drawer footer:** [Edit Release] · [Export PDF] · [Close]

---

## 6. Modals

### 6.1 New Release Modal

**Trigger:** [+ New Release] header button
**Width:** 600px

**Form fields:**

| Field | Type | Validation |
|---|---|---|
| Version | Text · `font-mono` | Required · semantic version `X.Y.Z` · unique |
| Release Name | Text | Required · max 120 chars |
| Type | Select | Feature Release · Hotfix · Security Patch · DB Migration Only |
| Description | Textarea | Required · min 20 chars |
| Target Date | Date picker | Required · must be future · must not be exam day (calendar check) |
| Risk Level | Select | Low / Medium / High / Critical |
| Risk Justification | Textarea | Required if High or Critical |
| QA Lead | User select | Required |
| DB Migrations Expected | Checkbox | `[ ] This release includes DB migrations` |
| Linked Epic | Text | JIRA epic link (optional) |
| Deployment Window | Select | Auto-suggest off-peak (11PM–2AM IST) or custom |

**Exam day conflict check:**
`hx-get="?part=exam_day_check&date={date}" hx-trigger="change from:#target-date" hx-target="#date-warnings"`
If target date overlaps a scheduled exam:
`bg-[#1A0A0A] border border-[#EF4444] rounded p-3` — "⚠ {N} exams scheduled on this date. Deployment window conflict."

**Footer:** [Create Release] · [Cancel]

---

### 6.2 Deploy to Production Modal

**Trigger:** "Deploy to Production" button in drawer Tab A or Kanban card
**Width:** 560px

**Pre-deploy checklist display:**
Shows all 8 sign-off items with current status — all must be ✅ before deploy button is active.

**Deployment configuration:**
- Deployment window: `[Tonight at 11:00 PM IST ▾]` or custom
- Deployment strategy: Rolling · Blue-Green · Canary (default Rolling)
- Notify institutions: `[ ] Send "Scheduled Maintenance" notification to institutions 1h before`
- Rollback trigger: `Auto-rollback if error rate > [0.5]% within [15] min of deploy`

**Confirmation fields:**
- Type release version to confirm: `input placeholder="Type v2.4.1 to confirm"`
- 2FA code: `input placeholder="Enter 6-digit code"`
- Deployment notes: `textarea placeholder="Any notes for the deployment log"`

**Footer:** [Deploy Now] `bg-[#6366F1]` (enabled only when all checks pass + version typed + 2FA entered) · [Cancel]

---

### 6.3 Rollback Confirmation Modal

**Trigger:** [Initiate Rollback] in drawer Tab F
**Width:** 540px
**Style:** `bg-[#070C18] border border-[#EF4444]`

**Impact summary:**
`bg-[#1A0A0A] rounded p-4 mb-4`
- Institutions affected: `2,050`
- Downtime estimate: `~2 minutes`
- DB migrations to reverse: list
- Flags to revert: list

**Required fields:**
- Rollback reason: `textarea` required · min 20 chars
- Incident reference: `text` — link to Incident Manager entry
- 2FA code: `input`
- Type "ROLLBACK" to confirm: `input` — button disabled until typed exactly

**CTO acknowledgement:** if logged-in user is not CTO/CEO:
`bg-[#451A03] border border-[#F59E0B] rounded p-3`
"This action requires CTO or CEO acknowledgement. An approval request has been sent via Slack."
[Check Approval Status] button — polls every 10s

**Footer:** [Confirm Rollback] `bg-[#EF4444]` · [Cancel]

---

### 6.4 New Hotfix Modal

**Trigger:** [+ New Hotfix] in Hotfixes tab
**Width:** 520px (streamlined — fewer fields than full release)

| Field | Type |
|---|---|
| Version | Text · auto-suggest next patch version |
| Description | Textarea · what is broken and impact |
| Severity | Select · P0 (SLA: 4h) / P1 (SLA: 24h) |
| Affected Module | Multi-select |
| Related Incident | Search · links to Incident Manager |
| Affected Institutions | Number estimate |
| Root Cause (known?) | Textarea (optional — fill in later) |

**Footer:** [Create Hotfix] · [Cancel]
Auto-moves to Staging immediately (skips Planning + Development stages).

---

## 7. Django View

```python
# portal/apps/product/views.py

class ReleaseManagerView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_releases"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":              "product/partials/releases_kpi.html",
                "pipeline":         "product/partials/releases_pipeline.html",
                "all_releases":     "product/partials/releases_table.html",
                "hotfixes":         "product/partials/releases_hotfixes.html",
                "changelogs":       "product/partials/releases_changelogs.html",
                "deploy_log":       "product/partials/releases_deploy_log.html",
                "release_drawer":   "product/partials/release_drawer.html",
                "staging_checks":   "product/partials/staging_checks.html",
                "exam_day_check":   "product/partials/exam_day_check.html",
                "changelog_preview":"product/partials/changelog_preview.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "product/release_manager.html", ctx)

    def post(self, request):
        action = request.POST.get("action")

        gated_actions = {
            "deploy_production", "rollback_release",
            "force_deploy", "qa_signoff",
        }
        if action in gated_actions:
            if not request.session.get("2fa_verified"):
                return JsonResponse({"error": "2FA required"}, status=403)

        if not request.user.has_perm("portal.manage_releases"):
            return JsonResponse({"error": "Permission denied"}, status=403)

        dispatch = {
            "create_release":       self._create_release,
            "update_release":       self._update_release,
            "move_stage":           self._move_stage,
            "deploy_production":    self._deploy_production,
            "rollback_release":     self._rollback_release,
            "run_staging_checks":   self._run_staging_checks,
            "run_migration_dryrun": self._run_migration_dryrun,
            "qa_signoff":           self._qa_signoff,
            "add_release_item":     self._add_release_item,
            "link_flag":            self._link_flag,
            "publish_changelog":    self._publish_changelog,
            "auto_generate_changelog": self._auto_generate_changelog,
        }
        handler = dispatch.get(action)
        if handler:
            return handler(request)
        return JsonResponse({"error": "Unknown action"}, status=400)

    def _build_context(self, request):
        from portal.apps.product.models import Release
        from django.core.cache import cache

        kpi = cache.get_or_set(
            "product:releases:kpi",
            lambda: {
                "total_quarter": Release.objects.current_quarter().count(),
                "planning":      Release.objects.filter(status="planning").count(),
                "development":   Release.objects.filter(status="development").count(),
                "staging":       Release.objects.filter(status="staging").first(),
                "production":    Release.objects.filter(status="production").order_by("-deploy_date").first(),
                "avg_cycle":     Release.objects.avg_cycle_time_days(),
            },
            60
        )
        return {
            "kpi": kpi,
            "releases": Release.objects.select_related("owner", "qa_lead").order_by("-created_at"),
        }
```

---

## 8. Release Data Model Reference

```python
class Release(models.Model):
    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("development", "Development"),
        ("staging", "Staging"),
        ("production", "Production"),
        ("rolled_back", "Rolled Back"),
        ("archived", "Archived"),
    ]
    TYPE_CHOICES = [
        ("feature", "Feature Release"),
        ("hotfix", "Hotfix"),
        ("security", "Security Patch"),
        ("migration", "DB Migration Only"),
    ]
    RISK_CHOICES = [
        ("low", "Low"), ("medium", "Medium"),
        ("high", "High"), ("critical", "Critical"),
    ]

    version      = models.CharField(max_length=20, unique=True)
    name         = models.CharField(max_length=120)
    release_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planning", db_index=True)
    risk_level   = models.CharField(max_length=10, choices=RISK_CHOICES, default="medium")
    risk_justification = models.TextField(blank=True)
    description  = models.TextField()
    target_date  = models.DateField()
    deploy_date  = models.DateTimeField(null=True, blank=True)
    rollback_date = models.DateTimeField(null=True, blank=True)
    cycle_time_days = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    owner        = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="owned_releases")
    qa_lead      = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="qa_releases")
    flags        = models.ManyToManyField("FeatureFlag", blank=True, through="ReleaseFlagDeployment")
    changelog_md = models.TextField(blank=True)
    changelog_published = models.BooleanField(default=False)
    changelog_audience  = models.CharField(max_length=20, default="all")
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["target_date"]),
        ]

    @classmethod
    def current_quarter(cls):
        from django.utils import timezone
        now = timezone.now()
        quarter_start = now.replace(month=((now.month - 1) // 3) * 3 + 1, day=1)
        return cls.objects.filter(created_at__gte=quarter_start)

    @classmethod
    def avg_cycle_time_days(cls):
        from django.db.models import Avg
        result = cls.objects.filter(
            status="production",
            cycle_time_days__isnull=False
        ).aggregate(avg=Avg("cycle_time_days"))
        return result["avg"] or Decimal("0")
```

---

## 9. Empty States

| Section | Copy |
|---|---|
| Pipeline (no releases) | "No active releases. Click '+ New Release' to start your first release." |
| All Releases (filtered) | "No releases match your filters. Try adjusting your search." |
| Hotfixes | "No hotfixes. Great — the platform is stable!" |
| Deployment Log | "No deployments recorded yet." |
| Changelog (no content) | "No changelog written yet. Click 'Auto-generate' to draft from release items." |

---

## 10. Error States

| Error | Display |
|---|---|
| Deploy blocked by failed QA checks | "Cannot deploy: {N} QA checks have not passed. Resolve blockers first." `bg-[#1A0A0A] border border-[#EF4444]` |
| Rollback not available | "Rollback not available — no reversible migration path to previous version." |
| Staging check timeout | "Staging check timed out after 5 minutes. [Retry]" |
| Exam day conflict | "⚠ Target date conflicts with {N} scheduled exams. Choose a different window." |
| 2FA failure on deploy | "Invalid 2FA code. Deploy cancelled. Try again." |

---

## 11. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `N` | New Release modal |
| `H` | New Hotfix modal |
| `1–5` | Switch tabs |
| `Esc` | Close drawer/modal |
| `↑↓` | Navigate release list |
| `Enter` | Open Release Detail Drawer |
| `R` | Refresh pipeline board |
