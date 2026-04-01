# div-a-03 — Exam Operations

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Schools | 1,000 · avg 1,000 students · max 5,000 |
| Colleges | 800 · avg 500 · max 2,000 |
| Coaching centres | 100 · avg 10,000 · max 15,000 |
| Groups | 150 · own 5–50 child institutions |
| Total institutions | 2,050 · Total students 2.4M–7.6M |
| Peak concurrent exam users | 500,000 |
| Simultaneous live exams | Up to 200 |
| Exams created per month | ~180,000 |
| Exam duration range | 30 min – 3 h |
| Table rows (all statuses) | Up to 2M all-time; default view = today (hundreds) |

**Architect's note:** The table default view is "today" to avoid loading 2M rows. Searches beyond 90 days must warn the user. Live exams are pinned to top of every view — they need immediate visibility. Bulk actions (Extend, Pause, Export) must work on selections of up to 200 exams simultaneously without page reload.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Route | `/exec/exam-ops/` |
| **Single page API** | **All partials from `/exec/exam-ops/?part={name}`** |
| View | `ExamOpsView` |
| Template | `exec/exam_ops_page.html` |
| Priority | P0 |
| Nav group | Operations |
| Roles | `exec`, `ops`, `admin` |
| Default view | Today's exams, Live status pinned top |
| HTMX poll | Stats: every 30s · Table (Live tab): every 30s |

---

## 3. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ Exam Operations           [Schedule Exam]  [Export ▾]  [↺ Refresh]         ║
╠═══════════╦═══════════╦════════════╦════════════╦═══════════════════════════╣
║ Live Now  ║ Scheduled ║ Completed  ║   Failed   ║ Avg Students / Exam       ║
║    14     ║   142     ║   53,814   ║     82     ║      248                  ║
║ ▲ 3 today ║ next 24h  ║ today      ║ today ⚠   ║ this month                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ TABS:  [Live (14) ●]  [Scheduled (142)]  [Completed]  [Failed (82)]  [All] ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ TOOLBAR                                                                      ║
║ [🔍 Search exam name or institution...]  [Inst.type▾] [Subject▾] [Date▾]  ║
║ [Class▾] [Proctor▾]  [Columns ▾]  ── Bulk: 0 selected [Actions ▾]         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ EXAM TABLE                                            hx-poll every 30s    ║
║ ☐ │ Exam Name      │ Institution  │Type│Subject│ Students │Status│Time│ ⋯ ║
║ ☐ │ JEE Mock #42   │ ABC Coaching │MCQ │Physics│  4,200   │🟢Live│2h18│⋯ ║
║ ☐ │ Math Unit Test  │ XYZ School   │MCQ │Maths  │    280   │🟢Live│1h44│⋯ ║
║ ☐ │ Chemistry Mock  │ PQR Coaching │MCQ │Chem   │  3,100   │🔵Sch │T+3h│⋯ ║
║   └─────────────────────────────────────────────────────────────────────┘  ║
║   Showing 1–25 of 156  [← 1 2 3 ... 7 →]  [25 ▾ per page]                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 5. Sections — Deep Specification

### 5.1 Page Header

**[Schedule Exam] button:** `bg-[#6366F1] text-white px-4 py-2 rounded-lg text-sm font-medium`. Opens Schedule Exam Modal (§7.1).

**[Export ▾] dropdown:**
- CSV (current filter) · Excel (with formatting) · PDF (summary report, max 500 rows)
- Async if > 1,000 rows: "Export queued — email when ready"
- POST to `/exec/exam-ops/?part=export&format=csv&{filter_params}`

**[↺ Refresh]:** Fetches stats + table. Spin animation on icon.

---

### 5.2 Stats Strip

**HTMX:** `id="eo-stats"` `hx-get="/exec/exam-ops/?part=stats"` `hx-trigger="load, every 30s[!document.querySelector('.drawer-open,.modal-open')]"` `hx-swap="innerHTML"`

| # | Card | Formula | Alert | Click |
|---|---|---|---|---|
| 1 | Live Now | Exams with status=live | Always green if > 0 | Switches to Live tab |
| 2 | Scheduled | Status=scheduled, start within 24h | — | Switches to Scheduled tab |
| 3 | Completed Today | Status=completed, today | — | Switches to Completed tab filtered to today |
| 4 | Failed Today | Status=failed, today | > 0 = red; click → alert | Opens Failed exams, auto-alerts ops |
| 5 | Avg Students/Exam | Mean students across all exams this month | — | — |

---

### 5.3 Tab Bar

**HTMX:** `id="eo-tabs"` — tabs + table rendered together by `?part=table`

```
[Live (14) ●] [Scheduled (142)] [Completed] [Failed (82)] [All]
```
Each tab label includes count badge (auto-updates with poll).

- Active: `border-b-2 border-[#6366F1] text-white pb-2`
- Inactive: `text-[#8892A4] hover:text-white pb-2`
- Count badge: `bg-[#131F38] text-[#8892A4] text-xs px-2 py-0.5 rounded ml-1`
- Failed count badge: `bg-red-900 text-red-300 text-xs px-2 py-0.5 rounded ml-1` (red when > 0)
- Click: `hx-get="/exec/exam-ops/?part=table&tab=live" hx-target="#eo-table-container" hx-swap="innerHTML"`

---

### 5.4 Toolbar

**Filter controls (horizontal, wraps on narrow screens):**

**Search input:**
- `<input type="search">` · placeholder: "Search exam name or institution…"
- 300px wide desktop, full-width mobile
- Debounced 400ms: `hx-trigger="keyup changed delay:400ms"`
- `hx-get="/exec/exam-ops/?part=table&q={{ value }}&tab={{ tab }}"` `hx-target="#eo-table-container"`
- Clear button [✕] inside input: clears and re-fetches

**Institution type dropdown:**
- `<select>` options: All · School · College · Coaching · Group
- Change: `hx-get` with `type=coaching`

**Subject dropdown:**
- `<select>` options: All + 50+ subjects (Physics, Chemistry, Maths, Biology, English, Social, + custom)
- Virtualised options list for > 50 items (CSS max-height scroll)

**Date range dropdown:**
- Options: Today (default) · Tomorrow · This Week · Next 7 Days · Last 7 Days · Last 30 Days · Custom
- Custom: dual date input `date_from` + `date_to`

**Class/Grade dropdown:**
- Multi-select: 6 · 7 · 8 · 9 · 10 · 11-Sci · 11-Com · 12-Sci · 12-Com · Foundation

**Proctoring dropdown:**
- All · Proctored only · Not proctored

**[Columns ▾] column visibility toggle:**
- Checkbox list of all table columns (except Exam Name which is always shown)
- Changes stored in localStorage per user

**Bulk actions area (right of toolbar):**
- When 0 selected: "{n} rows" in grey
- When ≥ 1 selected: `{n} selected` in white + `[Actions ▾]` dropdown
- Actions dropdown: Extend (+30 min) · Pause · Export Selected · Send Notification
- Select-all checkbox in table header: selects current page · "Select all {n} in filter" link appears below if clicked

**Active filter chips (below toolbar, only shown when filters applied):**
```
[Physics ✕] [Coaching ✕] [Today ✕]  [Clear all filters]
```
Each chip: `bg-[#131F38] border border-[#1E2D4A] text-white text-xs px-2 py-0.5 rounded` + ✕ to remove that filter

---

### 5.5 Exam Table

**HTMX:** `id="eo-table-container"` `hx-get="/exec/exam-ops/?part=table&tab=live"` `hx-trigger="load, every 30s[tab=='live' && !document.querySelector('.drawer-open,.modal-open')]"` `hx-swap="innerHTML"`

Poll only applies when Live tab is active.

**Columns:**

| Column | Width | Sortable | Detail |
|---|---|---|---|
| ☐ (checkbox) | 40px | No | Row selection for bulk actions. Header checkbox = select-page. Indeterminate state when some selected. |
| Exam Name | 240px | Yes | Clickable → Exam Detail Drawer. Truncated at 36 chars, tooltip for full. Group icon if exam spans multiple institutions. |
| Institution | 180px | Yes | Name truncated 20 chars. Type badge (small chip). Click → `/exec/institutions/{id}/` |
| Type | 60px | Yes | MCQ · Descriptive · Mixed · OMR — badge |
| Subject | 100px | Yes | Subject name |
| Students | 80px | Yes (desc) | Enrolled count. Live exams: "620 / 4,200" (submitted/enrolled). |
| Status | 100px | Yes | Status badge (see below) |
| Time | 80px | Yes | For scheduled: "T+3h" (time to start). For live: "1h 44m left" (countdown). For completed: duration. |
| ⋯ Actions | 40px | No | Context menu |

**Status badges:**

| Status | Style |
|---|---|
| 🟢 Live | `bg-green-900 text-green-300` + pulsing left border `border-l-4 border-green-500` |
| 🔵 Scheduled | `bg-blue-900 text-blue-300` |
| 🔴 Failed | `bg-red-900 text-red-300` |
| ⚫ Cancelled | `bg-gray-800 text-gray-400` |
| ⚪ Draft | `bg-gray-800 text-gray-500 italic` |
| ✅ Completed | `bg-emerald-900 text-emerald-300` |
| 🟡 Paused | `bg-amber-900 text-amber-300` |
| 🟣 Evaluating | `bg-violet-900 text-violet-300` |

**Row pinning:** Live status rows always at top of table regardless of sort.

**Row hover:** `hover:bg-[#131F38]`

**Row click (not checkbox, not ⋯):** Opens Exam Detail Drawer (§6.1)

**⋯ Actions menu (per row):**
- View Detail (opens drawer)
- Extend Duration (+10 / +15 / +30 / Custom)
- Pause Exam
- Broadcast Message
- Export Results (CSV/PDF)
- Reschedule (if scheduled)
- Cancel Exam
- Duplicate Exam

**Sort:** Default: Status (Live first) then Start Time desc. Sortable: Exam Name, Institution, Students, Status, Time.
Sort icon: ↕ unsorted · ↑ asc · ↓ desc (in column header)

**Loading skeleton:** 25 rows of pulse blocks. Columns match actual widths. Shown on tab switch and filter change.

**Empty state:**
```
🔍 No exams found
Try adjusting your filters or date range.
[Clear filters]
```
Centred, grey illustration, 200px height.

**Error state:**
```
⚠ Failed to load exams. [Retry]
```
`hx-get` retrigger on [Retry] click.

---

### 5.6 Pagination

**Rendered within `?part=table` partial:**

```
Showing 1–25 of 156                 [← Prev]  [1] [2] [3] ... [7]  [Next →]    [25 ▾ per page]
```

Layout: `flex justify-between items-center mt-4`

**"Showing X–Y of Z":** `text-[#8892A4] text-sm`

**Page number buttons:**
- Current page: `bg-[#6366F1] text-white rounded px-3 py-1`
- Other pages: `bg-transparent text-[#8892A4] hover:text-white px-3 py-1`
- Ellipsis `...` when page range > 7 pages: shows first, last, and ±2 around current

**[← Prev] / [Next →]:**
- Disabled style `opacity-30 cursor-not-allowed` on first/last page
- HTMX: `hx-get="/exec/exam-ops/?part=table&tab={{ tab }}&page=2"` `hx-target="#eo-table-container"` `hx-swap="innerHTML"`

**Per page selector:**
- `<select>` options: 10 · 25 (default) · 50 · 100
- Change: re-fetches with `per_page=50`, resets to page 1

---

## 6. Drawers

### 6.1 Exam Detail Drawer (640 px)

**Open trigger:** Click exam row (not checkbox or ⋯).

**HTMX:** `hx-get="/exec/exam-ops/?part=exam-drawer&id={{ id }}"` `hx-target="#drawer-container"` `hx-swap="innerHTML"`

**Drawer header:**
```
┌────────────────────────────────────────────────────────────────────┐
│ JEE Mock Test #42 — Physics     [🟢 Live]          [✕]           │
│ ABC Coaching Centre · MCQ · 300 marks · 3h                         │
└────────────────────────────────────────────────────────────────────┘
```

**Metric pills:**
```
[Enrolled: 4,200]  [Submitted: 620 ▲]  [In Progress: 3,572]  [Issues: 3 🔴]
```
Pills: `bg-[#131F38] rounded-full px-3 py-1 text-sm`. Issues pill: `bg-red-900/50 text-red-300` if > 0.

**Tabs:**
```
[Overview ●] [Students] [Performance] [Issues] [Actions]
```
Tab content: `hx-get="/exec/exam-ops/?part=exam-tab&id={{ id }}&tab=students"` `hx-target="#exam-tab-content"` `hx-swap="innerHTML"`

**Tab: Overview**
- Config grid: Duration · Start time · End time · Total marks · Sections · Negative marking · Shuffle · Proctoring
- Status timeline stepper (horizontal): Created → Published → Started → Live → … → Completed
- Live progress bar (if Live): "620 / 4,200 (14.8%)" + `<div class="bg-[#6366F1] h-2 rounded" style="width:14.8%">`
- Schedule history: original start + any extensions with reasons

**Tab: Students**
- Search within drawer: `<input>` placeholder "Search student name…"
- Status filter chips: [All ●] [Submitted] [In Progress] [Not Started] [Issues]
- Table (paginated 25/page within drawer):

| Column | Detail |
|---|---|
| Name | Student name |
| Class | Grade + section |
| Status | Submitted / In Progress / Not Started / Technical Issue |
| Time remaining | Countdown for in-progress |
| Score | (post-exam) out of total marks |
| ⋯ | Extend for student · View answers (post-exam) |

Pagination within drawer: `[← 1 2 3 →]` — `hx-target="#drawer-students-list"`

**Tab: Performance** (available post-exam)
- Score distribution histogram (Chart.js Bar, 10 buckets 0–100%)
- Key stats: Mean · Median · P10 · P90 · Highest · Lowest
- "Comparison with previous exam in this series" sparkline (if series detected)

**Tab: Issues**
- List of students with technical issues: name · error type · timestamp · [Resolve] action
- Error types: Submission failed · Network disconnected · Browser crash · Unknown
- [Bulk resolve all] button (marks all as acknowledged)

**Tab: Actions**

Full-width action buttons:
```
[+ Extend Duration ▾]       → dropdown: +10 / +15 / +30 / Custom
[⏸ Pause Exam]              → opens reason input inline
[📢 Broadcast Message]      → opens text area + [Send]
[⏹ Emergency End]           → type "END" to confirm
[↗ Reopen Submissions]      → for X more minutes (input)
[📊 Export Results]         → dropdown: CSV / PDF / Excel
[📋 Duplicate Exam]         → opens Schedule Exam Modal pre-filled
```

**Drawer footer (sticky):**
```
[View Full Exam Detail →]
```
Navigates to `/exec/exams/{id}/`

---

## 7. Modals

### 7.1 Schedule Exam Modal (720 px)

**Trigger:** [Schedule Exam] page header button.

**Structure:** 4-step wizard with progress indicator.

**Step 1: Basic Info**

| Field | Control | Validation |
|---|---|---|
| Exam name | Text, 100 chars | Required |
| Institution | Searchable select | Required |
| Class / Grade | Multi-select checkboxes | Required ≥ 1 |
| Subject | Select (50+ options) | Required |
| Exam type | Radio: MCQ / Descriptive / Mixed / OMR | Required |
| Series | Searchable select (existing series or "New series") | Optional |

**Step 2: Configuration**

| Field | Control | Default |
|---|---|---|
| Total marks | Number | 100 |
| Duration | HH:MM picker | 01:00 |
| Sections | Number (1–5) | 1 |
| Negative marking | Toggle + ratio select (−1/4, −1/3, −1) | Off |
| Shuffle questions | Toggle | On |
| Shuffle options | Toggle | On |
| Late submission window | Number (minutes) | 10 |

**Step 3: Schedule**

| Field | Control | Validation |
|---|---|---|
| Start date | `<input type="date">` | Required; ≥ today |
| Start time | `<input type="time">` | Required |
| End time | Auto-calculated (start + duration); shown read-only | — |
| Conflict check | Auto-run on start date/time change | Warn if > 80% of seats already in another exam |

**Step 4: Proctoring & Notify**

| Field | Detail |
|---|---|
| Enable proctoring | Toggle (only for Enterprise/Professional + add-on) |
| Snapshot interval | 30s default |
| AI sensitivity | Low / Medium / High |
| Notify students | Toggle (email/app notification) |
| Notify admins | Toggle |
| Reminder | 30 min before toggle |

**Footer (all steps):** [Cancel] [← Back] [Next →] / [Schedule Exam] (last step)

Schedule: POST `/exec/exams/` → success toast "Exam scheduled for {date}" → table refreshes

**Validation per step:** Cannot advance to next step until required fields valid.

---

### 7.2 Bulk Extend Modal (480 px)

**Trigger:** Bulk Actions → Extend (+30 min) with ≥ 2 exams selected.

Fields: Duration select (+10 / +15 / +30 / Custom number input) · Reason textarea (required) · List of selected exams (scrollable preview)

**Footer:** [Cancel] [Extend {n} Exams]

POST `/exec/exam-ops/bulk-extend/` with `{exam_ids: [], minutes: 30, reason: "..."}`

---

## 8. States & Edge Cases

| State | Behaviour |
|---|---|
| Live exam with submission failures | Row: red left border `border-l-4 border-red-500` + Issues column red count |
| Exam starting in < 15 min | Row: amber left border; Time column "⚡ T-12m" in amber |
| 200+ simultaneous live exams | Live tab shows all 200 (paginated 25/page); stats card shows 200 |
| Bulk select across pages | "Select all 156 in filter" link; HTMX passes `select_all=true` param |
| Search with 0 results | Empty state with "Try adjusting filters" message |
| Filter > 90 days | Warning banner: "Queries > 90 days may be slow. Export recommended for large ranges." |
| Proctoring column for Standard plan exam | "—" (not applicable) — don't show N/A confusingly |
| Group exam (shared paper) | Exam Name column shows 🏛 group icon + child count badge |
| Failed exam auto-alert | System auto-creates ops alert if exam status = failed. Incident card shown on Platform Health. |
| Schedule conflict | Step 3 of modal shows: "⚠ 3,400 students already have an exam at this time at this institution. Confirm scheduling?" |

---

## 9. HTMX Architecture — One URL Per Page

**Page URL:** `/exec/exam-ops/`
**All partials from:** `/exec/exam-ops/?part={name}`

```python
class ExamOpsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "stats":      "exec/partials/eo_stats.html",
                "table":      "exec/partials/eo_table.html",
                "exam-drawer":"exec/partials/eo_exam_drawer.html",
                "exam-tab":   "exec/partials/eo_exam_tab.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/exam_ops_page.html", ctx)
```

| `?part=` | Poll | Pause condition |
|---|---|---|
| `stats` | Every 30s | drawer/modal open |
| `table` | Every 30s (Live tab only) | drawer/modal open |
| `exam-drawer` | No | — |
| `exam-tab` | No | — |

---

## 10. API Endpoints

| Method | URL | Key params | Response |
|---|---|---|---|
| GET | `/exec/exam-ops/` | `part`, `tab`, `q`, `type`, `subject`, `date_from`, `date_to`, `class`, `proctor`, `page`, `per_page`, `sort`, `id`, `tab` (exam tab) | HTML |
| POST | `/exec/exams/` | New exam JSON | `{id: "..."}` |
| POST | `/exec/exams/{id}/extend/` | `{minutes, reason}` | `{status: "extended"}` |
| POST | `/exec/exams/{id}/pause/` | `{reason}` | `{status: "paused"}` |
| POST | `/exec/exams/{id}/end/` | `{confirm: "END"}` | `{status: "ended"}` |
| POST | `/exec/exams/{id}/broadcast/` | `{message}` | `{sent: n}` |
| POST | `/exec/exam-ops/bulk-extend/` | `{exam_ids[], minutes, reason}` | `{extended: n}` |
| GET | `/exec/exam-ops/?part=export` | filter params + `format` | File or 202 |

---

## 11. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| `?part=stats` | < 300 ms | > 800 ms |
| `?part=table` (25 rows, Live tab) | < 500 ms | > 1.5 s |
| Table search (by name, today) | < 400 ms | > 1 s |
| Exam drawer load | < 500 ms | > 1.5 s |
| Students tab (25 rows in drawer) | < 400 ms | > 1 s |
| Poll response (Live tab, every 30s) | < 300 ms | > 800 ms |
| Schedule modal step transitions | < 200 ms | > 500 ms |
| Bulk extend (50 exams) | < 2 s | > 5 s |
| Full page initial load | < 1.2 s | > 3 s |

---

## 12. Keyboard Shortcuts

| Key | Action |
|---|---|
| `N` | Schedule Exam (open modal) |
| `F` | Focus search input |
| `R` | Refresh all |
| `E` | Export |
| `1`–`5` | Switch tabs (Live / Scheduled / Completed / Failed / All) |
| `Shift+A` | Select all on current page |
| `Shift+D` | Deselect all |
| `↑` / `↓` | Navigate table rows |
| `Enter` | Open Exam Detail Drawer for focused row |
| `Space` | Toggle checkbox on focused row |
| `Esc` | Close drawer/modal or deselect all if bulk bar visible |
| `?` | Help |

---

## 13. HTMX Template Files

| File | Purpose |
|---|---|
| `exec/exam_ops_page.html` | Page shell with toolbar + tab target + table target |
| `exec/partials/eo_stats.html` | Stats strip (5 cards) |
| `exec/partials/eo_table.html` | Tab bar + toolbar active-filter chips + exam table + pagination |
| `exec/partials/eo_exam_drawer.html` | Exam Detail Drawer (640px) |
| `exec/partials/eo_exam_tab.html` | Inner tab content (Overview/Students/Perf/Issues/Actions) |

---

## 14a. Security Considerations

- Exam actions (Pause, Emergency End, Broadcast) restricted to `exec`, `ops`, `superadmin` roles only — institution admins cannot reach this page
- "Emergency End" requires typing "END" — guards against accidental termination of live exams with 74K students
- Bulk actions: validated server-side — `exam_ids` list filtered to confirm each exam belongs to accessible institutions (prevents IDOR)
- Export: rate-limited 5/day. Large exports (> 1,000 rows) async via Celery — prevents DoS on the reporting DB
- Student data in drawer: names and scores are visible to exec/ops but not exposed in URLs or logs — only by exam ID
- Schedule conflict warning: shown to prevent accidental double-booking, but not blocked (exec may override)
- `?part=` parameter: allowlisted server-side — unknown parts return 400

---

## 14b. Database Schema (key models)

```python
class Exam(models.Model):
    STATUS = [("draft","Draft"),("scheduled","Scheduled"),("live","Live"),
              ("paused","Paused"),("completed","Completed"),("failed","Failed"),
              ("cancelled","Cancelled"),("evaluating","Evaluating")]
    name            = models.CharField(max_length=200)
    institution     = models.ForeignKey("Institution", on_delete=models.CASCADE)
    series          = models.ForeignKey("ExamSeries", null=True, on_delete=models.SET_NULL)
    exam_type       = models.CharField(max_length=20,
                        choices=[("mcq","MCQ"),("descriptive","Descriptive"),
                                 ("mixed","Mixed"),("omr","OMR")])
    subject         = models.CharField(max_length=100)
    grade           = models.JSONField(default=list)    # ["11-Sci","12-Sci"]
    total_marks     = models.IntegerField()
    duration_minutes= models.IntegerField()
    scheduled_at    = models.DateTimeField(db_index=True)
    started_at      = models.DateTimeField(null=True)
    ended_at        = models.DateTimeField(null=True)
    status          = models.CharField(max_length=20, choices=STATUS, db_index=True)
    proctoring_enabled = models.BooleanField(default=False)
    negative_marking= models.BooleanField(default=False)
    negative_ratio  = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    shuffle_questions = models.BooleanField(default=True)
    enrolled_count  = models.IntegerField(default=0)  # denormalised for fast stats
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        indexes = [
            models.Index(fields=["status","scheduled_at"]),
            models.Index(fields=["institution","status"]),
        ]


class ExamExtension(models.Model):
    exam            = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="extensions")
    extended_by_min = models.IntegerField()
    reason          = models.TextField()
    extended_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    extended_at     = models.DateTimeField(auto_now_add=True)


class ExamIssue(models.Model):
    """Student-level technical issue during exam."""
    TYPES = [("submission_failed","Submission Failed"),("disconnected","Network Disconnected"),
             ("crash","Browser Crash"),("unknown","Unknown")]
    exam            = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="issues")
    student_id      = models.IntegerField()   # cross-schema reference
    error_type      = models.CharField(max_length=30, choices=TYPES)
    reported_at     = models.DateTimeField(auto_now_add=True)
    resolved_at     = models.DateTimeField(null=True)
    resolved_by     = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
```

Redis keys:
- `eo:stats:live` TTL 25s — live/scheduled/completed/failed counts
- `eo:live_exams` TTL 25s — list of live exam IDs for fast table query

---

## 14c. Validation Rules

| Action | Validation |
|---|---|
| Schedule Exam — Start date | Must be ≥ today (past dates blocked) |
| Schedule Exam — Duration | 10 min to 360 min (6 hours max) |
| Schedule Exam — Total marks | 10 to 1,000 |
| Schedule Exam — Institution | Must belong to accessible institutions (role check) |
| Schedule Exam — Proctoring | Only available if institution plan includes proctoring add-on |
| Extend Duration — Live exam only | Cannot extend completed/cancelled exams |
| Emergency End — Confirmation | User must type "END" exactly (case-sensitive) |
| Bulk Extend — Exam IDs | Server validates all IDs are accessible to requesting user |
| Bulk action max | Max 200 exams per bulk action |
| Export range | Default: today. Custom: max 365 days. > 90 days: async export |

---

## 14. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §5.2 stats strip |
| `TabBar` | §5.3 page tabs, §6.1 drawer tabs |
| `SearchInput` | §5.4 toolbar |
| `FilterDropdown` | §5.4 each filter |
| `ActiveFilterChips` | §5.4 below toolbar |
| `BulkActionsBar` | §5.4 when rows selected |
| `ExamTable` | §5.5 |
| `StatusBadge` | §5.5 status column |
| `PaginationStrip` | §5.6, §6.1 Students tab |
| `DrawerPanel` | §6.1 |
| `TabBar` | §6.1 drawer tabs |
| `ProgressBar` | §6.1 Overview tab |
| `ChartHistogram` | §6.1 Performance tab |
| `ModalWizard` | §7.1 Schedule modal |
| `ModalDialog` | §7.2 Bulk extend |
| `LoadingSkeleton` | Table skeleton |
| `EmptyState` | Table empty state |
