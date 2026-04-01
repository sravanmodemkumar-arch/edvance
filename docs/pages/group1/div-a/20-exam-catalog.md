# div-a-20 — Exam Catalog

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total exams in system (all-time) | ~500,000+ |
| Active exam templates | ~50,000 |
| Exams scheduled per day | ~1,000–3,000 |
| Exams running live right now (peak) | ~500–2,000 |
| Questions in bank | ~2M+ |
| Subjects covered | 25+ (Class 6–12 + competitive) |
| Exam types | Practice / Mock / Unit Test / Board Mock / Competitive |
| Max students per exam | 15,000 (coaching centre full batch) |

**Why this matters:** The Exec team needs a platform-level view of all exam activity — not just per-institution. The Exam Catalog is the master directory: search any exam, check its results, see its proctoring status, and drill into issues. It complements the Exam Operations page (div-a-03) which focuses on operational control.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Exam Catalog |
| Route | `/exec/exams/` |
| Django view | `ExamCatalogView` |
| Template | `exec/exam_catalog.html` |
| Priority | P1 |
| Nav group | Exams |
| Required role | `exec`, `superadmin`, `ops` |
| 2FA required | No (read-only); yes for cancellation |
| HTMX poll | Stats strip: every 60s |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Exam Catalog                             [Export] [+ Schedule Exam] │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────────────────┤
│  Total   │  Live    │ Today    │ Avg      │ Failed   │  Avg Students        │
│  (30d)   │  Now     │Scheduled │ Score    │ (30d)    │  per Exam            │
│  24,420  │   842    │  1,240   │  67.4%   │   18     │   98                 │
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────────────────┤
│ [🔍 Search exam name, institution, subject...]                               │
│ [Type ▾] [Subject ▾] [Institution ▾] [Status ▾] [Date Range ▾] [Class ▾]   │
│ Active filters: Status: Live ×                                  [Clear all] │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Columns ▾]  Sort: [Start Time ▾]  Showing 1–25 / 842 live exams           │
├──────────────────────────────────────────────────────────────────────────────┤
│ Exam Name        │ Institution │ Type  │ Subject │ Start │ Students │ Status │
│ JEE Mock Test 12 │ ABC Coaching│ Mock  │ Physics │ 14:30 │ 842/1000 │ ● Live │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

**Poll:** `hx-trigger="every 60s[!document.querySelector('.drawer-open,.modal-open')]"`

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Total (30d) | Exams completed in last 30 days | — |
| 2 | Live Now | Currently running exams | — |
| 3 | Today Scheduled | Exams scheduled for today | — |
| 4 | Avg Score (30d) | Platform-wide average | < 50% = amber |
| 5 | Failed (30d) | Exams that failed to start or crashed | > 10 = red |
| 6 | Avg Students/Exam | Mean enrollment per exam (30d) | — |

---

### 4.2 Search & Filter Bar

**Search:** debounced 400ms · searches name, institution, subject, exam ID
**Filters:**
| Filter | Options |
|---|---|
| Exam Type | All / Practice / Mock / Unit Test / Board Mock / Competitive |
| Subject | Multi-select: Maths / Physics / Chemistry / Biology / English / etc. |
| Institution | Searchable dropdown |
| Status | All / Live / Scheduled / Completed / Failed / Cancelled |
| Date Range | Today / Tomorrow / This Week / This Month / Custom |
| Class / Grade | All / Class 6–12 / UG / PG |
| Proctoring | All / With proctoring / Without |

**Active filter chips** · "Clear all" link

---

### 4.3 Table Toolbar

[Columns ▾] toggle visibility · Sort dropdown · "Showing X–Y of Z"
**Columns toggle:** default visible = Exam Name, Institution, Type, Subject, Start, Students, Status · toggleable = Class, Duration, Avg Score, Proctoring, Exam ID

---

### 4.4 Exam Table

`id="exam-table"` · `hx-get="?part=exam_table"` on load

**Row click:** opens Exam Detail Drawer (div-a-21 pattern)

#### Column Specifications

| Column | Sort | Width | Detail |
|---|---|---|---|
| Exam Name | ✓ | 240px | Truncated · live exams: `●` pulsing dot + `font-semibold text-[#F87171]` |
| Institution | ✓ | 180px | Name + type icon |
| Type | ✓ | 100px | Badge: Mock `#1E3A5F` · Practice `#064E3B` · Unit `#451A03` · Board `#2E1065` |
| Subject | ✓ | 100px | Subject badge |
| Class | ✓ | 70px | Class/Grade |
| Start Time | ✓ | 120px | Relative (live: "Live now · 24 min") or datetime |
| Duration | ✓ | 80px | Minutes |
| Students | ✓ | 100px | Appeared / Registered (fraction bar) |
| Avg Score | ✓ | 90px | % · coloured bar (green ≥ 70 · amber 50–69 · red < 50) |
| Proctoring | ✓ | 90px | ✓ Proctored / — |
| Status | ✓ | 110px | Status badge with dot |
| Actions ⋯ | — | 48px | View Results / View Detail / Cancel |

**Status badges:**
- Live: `bg-[#064E3B] text-[#34D399]` + pulsing dot
- Scheduled: `bg-[#1E3A5F] text-[#60A5FA]`
- Completed: `bg-[#1E293B] text-[#94A3B8]`
- Failed: `bg-[#450A0A] text-[#F87171]`
- Cancelled: `bg-[#1E293B] text-[#475569] line-through opacity-60`

**Live exam row:** pinned to top of table regardless of sort

---

### 4.5 Pagination

Same pattern as div-a-05 §4.6 · per-page: 25/50/100 · URL pushstate

---

## 5. Drawers

### 5.1 Exam Quick-View Drawer (640 px)

`id="exam-drawer"` · `body.drawer-open`

**Header:** Exam name + Type badge + Status badge · Institution name · `[Open Full Detail →]` + `[×]`

**Tab bar (4 tabs):** Overview · Students · Results · Proctoring

**Tab A — Overview:**
- Exam ID · Type · Subject · Class
- Scheduled: start + end
- Duration · Total marks
- Institution · Created by
- Proctoring: enabled/disabled + type
- Instructions (expandable)
- Previous attempts: count (for repeat exams)

**Tab B — Students:**
Table: Name · Status (Appeared/Absent/Disconnected) · Time taken · Score
Pagination: 25/page

**Tab C — Results:**
- Score distribution histogram (5 buckets)
- Avg / Median / Top score / Lowest score
- Rank 1 student (anonymised for privacy)
- Subject-wise performance (if multi-subject)

**Tab D — Proctoring:**
- Violations count: Tab switches / Multiple faces / Phone detected
- Flagged submissions: count · [View Flags]
- Proctoring log summary

**Footer:** [View Full Detail →] [Download Results] [Cancel Exam] [Close]

---

## 6. Modals

### 6.1 Schedule Exam Modal (720 px, 4-step wizard)

**Same as div-a-03 Schedule Exam Modal** — cross-reference. See div-a-03 §6.1 for full spec.

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/exam_catalog_kpi.html` | Page load · poll 60s |
| `?part=exam_table` | `exec/partials/exam_catalog_table.html` | Load · search · filter · sort · page |
| `?part=exam_drawer&id={id}` | `exec/partials/exam_catalog_drawer.html` | Row click |

**Django view dispatch:**
```python
class ExamCatalogView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_exams"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/exam_catalog_kpi.html",
                "exam_table": "exec/partials/exam_catalog_table.html",
                "exam_drawer": "exec/partials/exam_catalog_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/exam_catalog.html", ctx)
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 300 ms | > 800 ms |
| Exam table (25 rows) | < 400 ms | > 1 s |
| Exam drawer | < 300 ms | > 800 ms |
| Full page initial load | < 1 s | > 2.5 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Failed exam row | Amber banner in drawer: "This exam failed — see Exam Operations for details" |
| Live exam with 0 students | "0 students appeared" in Live badge + alert to institution |
| Cancel live exam | Warning modal: "Cancelling a live exam will disconnect {N} students immediately." · 2FA required |
| 0 exams match filter | Empty state + [Clear filters] |
| Exam results not yet processed | Results tab: "Results processing — check back in a few minutes" |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `F` | Focus search |
| `N` | Schedule new exam |
| `E` | Export |
| `↑` / `↓` | Navigate rows |
| `Enter` | Open drawer |
| `Esc` | Close drawer |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/exam_catalog.html` | Full page shell |
| `exec/partials/exam_catalog_kpi.html` | KPI strip |
| `exec/partials/exam_catalog_table.html` | Exam table + pagination |
| `exec/partials/exam_catalog_drawer.html` | Exam quick-view drawer |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `SearchInput` | §4.2 |
| `MultiSelectDropdown` | §4.2 filters |
| `FilterChip` | §4.2 |
| `ExamTable` | §4.4 |
| `StatusBadge` | §4.4 |
| `TypeBadge` | §4.4 |
| `ScoreBar` | §4.4 Avg Score |
| `DrawerPanel` | §5.1 |
| `ScoreHistogram` | §5.1 Tab C |
| `ProctoringLog` | §5.1 Tab D |
| `PaginationStrip` | §4.5 + drawer Tab B |
| `PollableContainer` | KPI strip |
