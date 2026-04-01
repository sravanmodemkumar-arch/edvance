# 11 — Test Series Manager

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Active test series | ~800+ across all domains |
| Exams per series | 5–150 exams per series |
| Total exams across all series | ~40,000+ |
| Students enrolled in test series | ~100K+ active enrollments |
| Coaching centres running their own series | 100 (use platform-hosted series) |
| Schools running domain-aligned series | ~400 schools |
| Colleges running board exam series | ~600 colleges |
| Peak exam submissions per series exam | 50,000+ (national SSC series) |
| Series types | Free · Paid · Institution-exclusive · Domain-wide |

**Why this page matters at scale:** Test series are the primary monetisation vehicle for coaching centres — 100 coaching centres build their reputation on how well their test series prepares students. At 100K+ enrollments, a misconfigured series (wrong exam count, broken schedule, missing exam) destroys trust. PM Exam Domains designs series structures and schedules; institutions clone or subscribe to them. This page is the master template manager — not the per-institution exam scheduler (that lives in institution portals).

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Test Series Manager |
| Route | `/product/test-series/` |
| Detail route | `/product/test-series/<series_id>/` |
| Django view class | `TestSeriesManagerView` |
| Template | `product/test_series_manager.html` |
| Permission — view | `portal.view_test_series` (all div-b roles) |
| Permission — manage | `portal.manage_test_series` (PM Exam Domains only) |
| 2FA required | No |
| HTMX poll — enrollment stats | Every 300s (5 min) |
| Nav group | Product |
| Nav icon | `list-ordered` |
| Priority | P1 |

---

## 3. Wireframe

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Test Series Manager          [+ New Series]  [Clone Series]  [Export CSV] │
├────────┬────────┬────────┬────────┬────────┬────────────────────────────────────────┤
│ Total  │ Active │ Draft  │ Archivd│ Total  │ Total Enrollments                     │
│ Series │  620   │   80   │  100   │ Exams  │  1,04,280                            │
│  800   │        │        │        │ 40,820 │  +2,340 this week                     │
├────────┴────────┴────────┴────────┴────────┴────────────────────────────────────────┤
│ TABS: [All Series] [Active (620)] [Draft (80)] [Archived (100)] [Series Analytics] │
├────────────────────────────────────────────────────────────────────────────────────┤
│ TOOLBAR: [🔍 Search series...] [Domain ▾] [Type ▾] [Status ▾] [Sort ▾] [Apply]   │
│ Active chips: Domain: SSC ×  [Clear all]                                          │
├────────────────────────────────────────────────────────────────────────────────────┤
│ TABLE                                                                              │
│ Series Name              │ Domain │ Type     │ Exams │ Enrolled │ Status │ ⋯     │
│ SSC CGL 2026 Full Series │ SSC    │ Full     │  150  │  28,400  │ Active │ ⋯     │
│ SSC CHSL Mock Test Pack  │ SSC    │ Mock     │   30  │  12,300  │ Active │ ⋯     │
│ RRB NTPC CBT1 Series     │ RRB    │ Full     │  120  │  22,100  │ Active │ ⋯     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Value | Delta | Alert |
|---|---|---|---|---|
| 1 | Total Series | `800` | — | — |
| 2 | Active | `620` | — | — |
| 3 | Draft | `80` | — | > 30 days in draft = amber |
| 4 | Archived | `100` | — | — |
| 5 | Total Exams | `40,820` | — | — |
| 6 | Total Enrollments | `1,04,280` | `+2,340 this week` | — |

---

### 4.2 Toolbar

| Control | Type | Options |
|---|---|---|
| Search | Text · debounce 300ms | Series name search |
| Domain | Multi-select | SSC · RRB · NEET · JEE · AP Board · TS Board · IBPS · SBI · All |
| Type | Multi-select | Full Series · Mock Tests · Chapter-wise · Previous Year · Speed Tests · Subject-wise |
| Status | Multi-select | Active · Draft · Archived · Scheduled |
| Sort | Dropdown | Enrollment (desc) · Name · Created date · Exam count |
| [Apply] | Button | `bg-[#6366F1]` |

---

### 4.3 Series Table

| Column | Width | Sortable |
|---|---|---|
| Series Name | 260px | Yes |
| Domain | 80px | Yes |
| Type | 120px | Yes |
| Exam Count | 80px | Yes |
| Enrolled | 100px | Yes (default sort desc) |
| Avg Score | 80px | No (shown for completed series) |
| Status | 100px | Yes |
| Created | 100px | Yes |
| Updated | 100px | Yes |
| Actions ⋯ | 48px | — |

**Domain badge colours:**
- SSC: `bg-[#1D4ED8] text-white`
- RRB: `bg-[#0369A1] text-white`
- NEET: `bg-[#15803D] text-white`
- JEE: `bg-[#7C3AED] text-white`
- AP Board: `bg-[#B45309] text-white`
- TS Board: `bg-[#BE185D] text-white`
- IBPS: `bg-[#0F766E] text-white`

**Type badge:** `text-xs px-2 py-0.5 rounded-full`
- Full Series: `bg-[#312E81] text-[#A5B4FC]`
- Mock Tests: `bg-[#064E3B] text-[#34D399]`
- Chapter-wise: `bg-[#451A03] text-[#FCD34D]`
- Previous Year: `bg-[#1E2D4A] text-[#94A3B8]`

**Enrolled column:** number with comma formatting · `text-[#F1F5F9] font-medium`

**Kebab menu (⋯):**
- View / Edit → opens Series Detail Drawer (720px)
- Clone Series → Clone Modal
- Archive → confirmation
- Delete → only if enrolled = 0 and status = draft
- View Analytics → opens Series Analytics tab pre-filtered

---

## 5. Series Detail Drawer (720px)

**Trigger:** Row click or kebab → View/Edit
**Header:** Series name + Domain badge + Type badge + Status badge + `[×]`

**Tab bar (5 tabs):** Overview · Exams · Schedule · Enrollment · Analytics

---

### Tab A — Overview

**Two-column layout:**

Left column (editable fields):
| Field | Type |
|---|---|
| Series Name | Text · required · max 120 chars |
| Short Description | Textarea · max 300 chars |
| Domain | Select (from active exam domains) |
| Type | Select: Full · Mock · Chapter-wise · PYQ · Speed · Subject-wise |
| Target Exam Type | Multi-select (e.g., SSC CGL Tier 1) |
| Difficulty Level | Select: Beginner · Intermediate · Advanced · Mixed |
| Language | Multi-select: English · Telugu · Hindi |
| Is Free | Toggle |
| Price (if paid) | Decimal input · ₹ |
| Max Enrollments | Number or Unlimited |
| Enrollment deadline | Date picker (optional) |

Right column (computed/read-only):
- Exam count: `N exams`
- Total marks: auto-computed from all exam marks schemes
- Total duration: auto-computed
- Enrolled: count
- Completion rate: % of enrolled who have attempted all exams
- Avg score across series: %

**[Save Changes]** · **[Publish Series]** (Draft → Active)

---

### Tab B — Exams

**Purpose:** Manage the ordered list of exams within this series.

**Exam list (drag-and-drop reorderable):**

Each row (draggable):
```
[≡ drag handle]  [#N]  [Exam Name]  [Domain/Section]  [Q count]  [Marks]  [Duration]  [Status]  [⋯]
```

**Drag handle:** `cursor-grab text-[#475569]` · `≡` icon
After drag: `hx-post="?action=reorder_exams" hx-vals='{...new_order_array}'`

**Status per exam in series:**
- Active: `text-[#34D399]`
- Draft: `text-[#94A3B8]`
- Scheduled: `text-[#FCD34D]`

**Kebab per exam row:**
- Edit exam metadata
- Replace with different exam
- Move to position (enter number)
- Remove from series

**[+ Add Exam]** button:
- Search and add from existing exam pool: `hx-get="?part=exam_search"` autocomplete
- Create new exam → links to Exam Pattern Builder (page 12) to create pattern first
- Add Previous Year Paper → special modal with year picker + source upload

**Pagination if > 50 exams:** 25/page within drawer

**Series exam stats footer:**
`bg-[#0D1526] rounded p-3 flex gap-6 text-sm`
- Total: `150 exams`
- Total marks: `30,000`
- Total duration: `150 hours`
- Avg questions per exam: `100`

---

### Tab C — Schedule

**Purpose:** Define when each exam in the series becomes available.

#### Schedule Types

`[○ Sequential (unlock after previous)]  [○ Calendar schedule]  [○ All available at once]`

**Sequential mode:**
- Exam N+1 unlocks X days after student completes Exam N
- X: `input[type=number]` days · default: 1
- Or: unlocks immediately after submit (no waiting)

**Calendar schedule mode:**
Release date table:

| # | Exam Name | Release Date | Release Time | Auto-close | Actions |
|---|---|---|---|---|---|
| 1 | SSC CGL Full Mock 1 | Mar 25, 2026 | 10:00 AM IST | — | Edit |
| 2 | SSC CGL Full Mock 2 | Apr 1, 2026 | 10:00 AM IST | — | Edit |

**[Set Release Dates in Bulk]** button: date arithmetic tool
"Set Mock 1 to [start date], then every [7] days thereafter"
Computes all 150 release dates automatically — preview table shown before confirming.

**Bulk date shift:** [Shift All Dates by +N days] — useful when a scheduled exam date needs to move.

---

### Tab D — Enrollment

**Filter row:** Status · Institution type · Date range

**Enrollment summary stats:**
`grid grid-cols-3 gap-4 mb-4`
- Total enrolled: `28,400`
- Active (attempted ≥ 1 exam): `22,100 (77.8%)`
- Completed all exams: `1,840 (6.5%)`

**Enrollment table:**

| Column | Detail |
|---|---|
| Institution | Name + type badge |
| Students Enrolled | Count |
| Avg Exams Attempted | N of 150 |
| Avg Score | % |
| Completion % | Progress bar |
| Enrolled On | Date |
| Actions ⋯ | View Institution · Revoke Access |

**[Export Enrollment CSV]** · **Pagination:** 25/page

---

### Tab E — Analytics

**Canvas id:** `series-analytics-chart` · height 280px

**Chart 1 — Enrollment over time (line chart):**
X-axis: months since series creation
Y-axis: cumulative enrollments
Series: `#6366F1` total · `#10B981` completions

**Chart 2 — Exam attempt rate by exam number (bar chart):**
X-axis: exam number (1–150)
Y-axis: % of enrolled who attempted
Shows drop-off clearly — exam where students disengage is visible as a bar-height drop

**Chart 3 — Score distribution across series (histogram):**
X-axis: score buckets (0–10%, 10–20%, etc.)
Y-axis: student count
Comparison: series avg vs top 10% vs bottom 10%

**Key insights panel:**
`bg-[#0D1526] rounded p-4 text-sm`
- "Highest drop-off at Exam #42 (Geometry Hard) — 23% of students stopped here"
- "Average completion time: 68 days (for students who complete all 150 exams)"
- "Top institution: SR Coaching Centre · 2,400 students · 89% completion"

---

## 6. Modals

### 6.1 New Series Modal

**Width:** 600px · 2-step

**Step 1 — Basic Info:**
- Series Name, Domain, Type, Description, Target Exam Type, Difficulty, Language

**Step 2 — Exam Selection:**
- Method: [Build from scratch] [Clone from existing series] [Import exam list CSV]

"Build from scratch" leads to empty series → user adds exams in Exams tab after creation.
"Clone from existing" → series search dropdown → copies exam list + schedule structure.

---

### 6.2 Clone Series Modal

**Trigger:** Header [Clone Series] or kebab → Clone
**Width:** 520px

| Field | Type |
|---|---|
| Source Series | Read-only display of selected series |
| New Series Name | Text · required |
| Copy exams? | `[✓]` Yes (default) |
| Copy schedule? | `[✓]` Yes |
| Copy enrollments? | `[ ]` No (default — enrollments are institution-specific) |
| Set status to | Draft (default for safety) |

---

### 6.3 Bulk Release Date Modal

**Trigger:** [Set Release Dates in Bulk] in Schedule tab
**Width:** 480px

- Start date: date picker
- Interval: `[7]` days
- Start time: `[10:00 AM IST]`
- Preview: table showing first 10 computed dates
- [Apply to All N Exams] · [Cancel]

---

## 7. Tab: Series Analytics (page-level tab)

**Purpose:** Cross-series comparison analytics for all 800 series.

### 7.1 Top Series by Enrollment

**Chart:** Horizontal bar chart · Top 20 series · `#6366F1`
Click bar → opens Series Detail Drawer

### 7.2 Enrollment Trend (all series)

**Chart:** Line chart · 12 months · total enrollments across all series

### 7.3 Domain Distribution

**Doughnut chart:** enrollment by domain
SSC · RRB · NEET · JEE · AP Board · TS Board · IBPS · SBI

### 7.4 Completion Rate Table

| Series | Enrolled | Completed | Completion % | Avg Score | Days to Complete |
|---|---|---|---|---|---|
| SSC CGL 2026 Full | 28,400 | 1,840 | 6.5% | 62.4% | 68d |
| NEET Mock Pack | 12,100 | 3,400 | 28.1% | 58.2% | 42d |

Sort: Completion % desc

---

## 8. Django View

```python
class TestSeriesManagerView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_test_series"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":             "product/partials/series_kpi.html",
                "table":           "product/partials/series_table.html",
                "series_drawer":   "product/partials/series_drawer.html",
                "exam_search":     "product/partials/series_exam_search.html",
                "enrollment_table":"product/partials/series_enrollment.html",
                "analytics":       "product/partials/series_analytics.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "product/test_series_manager.html", ctx)

    def post(self, request):
        if not request.user.has_perm("portal.manage_test_series"):
            return JsonResponse({"error": "Permission denied"}, status=403)
        action = request.POST.get("action")
        dispatch = {
            "create_series":      self._create_series,
            "update_series":      self._update_series,
            "clone_series":       self._clone_series,
            "archive_series":     self._archive_series,
            "delete_series":      self._delete_series,
            "add_exam":           self._add_exam,
            "remove_exam":        self._remove_exam,
            "reorder_exams":      self._reorder_exams,
            "set_schedule":       self._set_schedule,
            "bulk_release_dates": self._bulk_release_dates,
            "publish_series":     self._publish_series,
        }
        handler = dispatch.get(action)
        if handler:
            return handler(request)
        return JsonResponse({"error": "Unknown action"}, status=400)
```

---

## 9. Data Model Reference

```python
class TestSeries(models.Model):
    TYPE_CHOICES = [
        ("full",       "Full Series"),
        ("mock",       "Mock Tests"),
        ("chapter",    "Chapter-wise"),
        ("pyq",        "Previous Year"),
        ("speed",      "Speed Tests"),
        ("subject",    "Subject-wise"),
    ]
    STATUS_CHOICES = [
        ("draft", "Draft"), ("active", "Active"), ("archived", "Archived"),
    ]
    name          = models.CharField(max_length=120, db_index=True)
    domain        = models.ForeignKey("ExamDomain", on_delete=models.PROTECT)
    series_type   = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft", db_index=True)
    description   = models.TextField(blank=True)
    is_free       = models.BooleanField(default=True)
    price         = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0"))
    max_enrollments = models.IntegerField(default=-1)  # -1 = unlimited
    enrollment_deadline = models.DateField(null=True, blank=True)
    schedule_type = models.CharField(max_length=20, default="all_at_once")
    schedule_interval_days = models.PositiveSmallIntegerField(default=7)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["domain", "status"])]


class TestSeriesExam(models.Model):
    series    = models.ForeignKey(TestSeries, on_delete=models.CASCADE, related_name="exams")
    exam      = models.ForeignKey("Exam", on_delete=models.PROTECT)
    order     = models.PositiveSmallIntegerField(default=0)
    release_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [("series", "exam")]
        ordering = ["order"]


class TestSeriesEnrollment(models.Model):
    series      = models.ForeignKey(TestSeries, on_delete=models.CASCADE)
    institution = models.ForeignKey("Institution", on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    student_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [("series", "institution")]
```

---

## 10. Empty States

| Section | Copy |
|---|---|
| No series | "No test series yet. Create one to start organising exams." |
| No exams in series | "This series has no exams yet. Add exams in the Exams tab." |
| No enrollments | "No institutions enrolled in this series yet." |

---

## G1 Amendment — Exam Schedule Calendar View

### Purpose

At 800+ active test series across 8+ exam domains with 2,050 institutions, PM Exam Domains needs a capacity planning view to answer: "Which weeks are overloaded with scheduled exams? Will 74,000 concurrent students be attempted in the same 2-hour window on Thursday?"

The calendar view sits alongside the existing list view as a toggle — no separate page needed.

---

### Calendar View Toggle

Located in the page header toolbar, to the right of the filter bar:

```
[☰ List]  [📅 Calendar]          ← toggle, only one active
```

Switching to Calendar view does NOT lose the current filter state (domain, status, institution type filters carry over).

---

### Calendar View Layout

**Weekly view (default):** 7-column grid (Mon–Sun). Each day column shows all exams scheduled to start that day, sorted by start time.

**Monthly view:** Standard month grid. Exams shown as compact colour-coded chips. Click a chip to open the Series Drawer.

**View switcher:** Week · Month · Day (Day view used when zooming into a single high-load day).

---

### Exam Chip — Colour Coding

| Colour | Meaning |
|---|---|
| `bg-[#3B82F6]` Blue | SSC / RRB domain |
| `bg-[#10B981]` Green | NEET / JEE domain |
| `bg-[#F59E0B]` Amber | AP Board / TS Board |
| `bg-[#8B5CF6]` Purple | IBPS / SBI / Banking |
| `bg-[#EF4444]` Red | Exam overdue (scheduled but not published) |
| `bg-[#6B7280]` Grey | Draft — not yet scheduled |

Each chip shows: **Series name (abbreviated) · Start time · Enrolled count**
Hover tooltip: full series name · institution count · exam type · domain.

---

### Concurrent Load Indicator

**Purpose:** The most critical capacity planning signal. At 74K peak concurrent users, the PM must know when two or more high-enrollment exams overlap.

Above the calendar grid: a **load bar** per half-hour time slot for the visible week. Bar height = estimated concurrent submissions in that slot.

- Green bar: < 40,000 concurrent (safe)
- Amber bar: 40,000–65,000 (approaching limit)
- Red bar: > 65,000 (potential SLA breach — warning banner shown)

Calculation: sum of enrolled students across all exams whose window includes that time slot × an estimated submission rate of 80%.

If a red bar is detected, a warning card appears at the top of the calendar:
> ⚠ **Capacity warning — Thursday 27 Mar, 10:00–11:30 AM:** Estimated 71,200 concurrent submissions. This exceeds the safe 65,000 threshold. Consider rescheduling one exam to reduce overlap.

---

### Calendar Filters (carry over from list view)

| Filter | Type |
|---|---|
| Domain | Multi-select chip (SSC · RRB · NEET · JEE · AP Board · TS Board · IBPS/SBI) |
| Institution Type | Multi-select (School · College · Coaching · Group) |
| Status | Multi-select (Draft · Scheduled · Live · Completed · Cancelled) |
| Date Range | Date picker (custom or quick: This Week / Next Week / This Month) |

---

### Calendar Interactions

| Action | Result |
|---|---|
| Click an exam chip | Opens Series Detail Drawer (same drawer as list view) |
| Drag an exam chip to another day | Reschedule modal: "Reschedule [Series Name] to [New Date]? This will notify all enrolled institutions." Confirm → updates schedule |
| Right-click an exam chip | Context menu: View Details · Reschedule · Cancel Exam · Copy Link |
| Click empty day slot | New Series modal pre-filled with that date as start date |
| Hover a load bar | Tooltip: "Estimated X concurrent users · Y exams overlapping · Top 3 series by enrollment: …" |

---

### Data Source

Calendar data is fetched via `GET /api/v1/test-series/calendar/?week_start=2026-03-23&domain=all&status=scheduled,live` — returns all series with scheduled windows in the requested range.

Poll interval: **120 seconds** (same Redis cache as KPI strip) — guarded by `[!document.querySelector('.drawer-open,.modal-open')]`.

---

## 11. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `N` | New Series modal |
| `C` | Clone Series modal |
| `1–5` | Switch drawer tabs |
| `/` | Focus search |
| `Esc` | Close drawer/modal |
