# div-a-27 — Cohort Analysis

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Institution cohorts (by join month) | ~36 monthly cohorts (3 years of data) |
| Student cohorts (by first exam month) | ~36 monthly cohorts |
| Min cohort size for display | 10 institutions / 100 students |
| Cohort retention data lag | 24h (nightly computation) |
| Max cohort lookback | 24 months |

**Why this matters:** Cohort analysis answers the CEO's most important question: "Are the institutions we onboard in Year 2 performing better than Year 1 cohorts?" It separates platform maturity trends from raw growth numbers. A declining retention curve in recent cohorts = product problem. An improving curve = successful onboarding improvements.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Cohort Analysis |
| Route | `/exec/cohort-analysis/` |
| Django view | `CohortAnalysisView` |
| Template | `exec/cohort_analysis.html` |
| Priority | P2 |
| Nav group | Analytics |
| Required role | `exec`, `superadmin` |
| 2FA required | No |
| HTMX poll | None (nightly data) |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Cohort Analysis                              [Export] [Date Range ▾] │
├──────────────────────────────────────────────────────────────────────────────┤
│ TABS: [Institution Cohorts] [Student Cohorts] [Revenue Cohorts]             │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Cohort group: Monthly ▾] [Institution Type ▾] [Plan ▾]                    │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: INSTITUTION COHORTS                                                     │
│ Cohort heatmap (rows = cohort month, columns = M+0 to M+24)                 │
│ Retention line chart (multiple cohorts overlaid)                             │
│ Cohort comparison table                                                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 Global Filter Bar

`id="cohort-filters"` · `flex flex-wrap gap-3 p-4 border-b border-[#1E2D4A]`

| Filter | Options |
|---|---|
| Cohort grouping | Monthly / Quarterly / Annual |
| Institution type | All / School / College / Coaching / Group |
| Plan | All / Starter / Standard / Professional / Enterprise |
| Cohort range | Start month – End month (date pickers) |
| Metric | Retention % / Revenue retention / Exam activity |

---

### 4.2 Tab: Institution Cohorts

`id="tab-inst-cohorts"` · `hx-get="?part=inst_cohorts"`

#### 4.2.1 Retention Heatmap

Same component as div-a-04 §4.5.2 but with institution cohorts.

**Rows:** each cohort (Jan 2023, Feb 2023, ..., current)
**Columns:** M+0 (100%), M+1, M+3, M+6, M+12, M+18, M+24

**Cell definition:** Retention = institution still active (ran at least 1 exam in period) / institutions in cohort at M+0

**Cell colour:**
- 100%: `bg-[#064E3B]`
- 90–99%: `bg-[#065F46]`
- 75–89%: `bg-[#047857]`
- 50–74%: `bg-[#D97706]`
- < 50%: `bg-[#991B1B]`
- N/A (future): `bg-[#1E293B] text-[#475569]`

**Click cell:** opens Cohort Cell Drawer (§5.1)

#### 4.2.2 Retention Line Chart (cohort overlay)

**Chart:** Multi-line · Chart.js · Canvas height 260px
**Each line:** one cohort · max 12 lines visible · toggle cohorts via legend
**X-axis:** months since joining (0–24)
**Y-axis:** retention % (0–100)
**Platform average:** thick dashed line `#6366F1`
**Tooltip:** cohort name + retention % + absolute count

**Cohort selector:** pill buttons below chart to toggle individual cohort lines on/off

#### 4.2.3 Cohort Summary Table

| Cohort | Size | M+1 | M+3 | M+6 | M+12 | Best month | Worst month |
|---|---|---|---|---|---|---|---|
| Jan 2023 | 48 | 96% | 90% | 85% | 79% | M+1 | M+12 |
| Feb 2023 | 52 | 94% | 88% | 82% | 75% | M+1 | M+12 |

**Click cohort row:** highlights that cohort in heatmap + line chart

---

### 4.3 Tab: Student Cohorts

`id="tab-student-cohorts"` · `hx-get="?part=student_cohorts"`

**Same layout as §4.2** but:
- Metric = student retention (took exam in period / total in cohort)
- Row = month of first exam
- Cohort sizes: 1,000–500,000 students per cohort

#### 4.3.1 Student Retention Heatmap

Same pattern · cells may be N/A if cohort size < 100 (privacy)

#### 4.3.2 Student Retention by Institution Type

Tab selector within this tab: All / School / College / Coaching / Group
Separate heatmaps or overlay lines per type

---

### 4.4 Tab: Revenue Cohorts

`id="tab-rev-cohorts"` · `hx-get="?part=rev_cohorts"`

**Metric:** Revenue retention = ARR from cohort in month / ARR from cohort at M+0

**Revenue retention is often > 100% (expansion MRR from upsells)**

#### 4.4.1 Net Revenue Retention Heatmap

Same heatmap pattern but values can be > 100%
- > 110%: `bg-[#1D4ED8]` (dark blue = strong expansion)
- 100–110%: `bg-[#064E3B]`
- 90–99%: `bg-[#065F46]`
- < 90%: `bg-[#991B1B]`

#### 4.4.2 NRR Trend Chart

**Chart:** Line · NRR % over last 12 months · benchmark line at 100% (break-even)

#### 4.4.3 Revenue Cohort Table

| Cohort | M+0 ARR | M+6 NRR | M+12 NRR | Churn MRR | Expansion MRR |
|---|---|---|---|---|---|

---

## 5. Drawers

### 5.1 Cohort Cell Drawer (560 px)

Same as div-a-04 §5.2 but with more detail for this dedicated page.

**Header:** "Cohort {MMM YYYY} — Month {N} ({metric}%)"

**Section A — Active institutions:**
Table: Name · Type · Plan · Students · ARR
Sorted by ARR desc

**Section B — Churned this period:**
Table: Name · Type · Churn date · ARR lost · Reason

**Section C — Cohort trend:**
Mini line chart showing this cohort's retention over all available months

**Footer:** [Export] [View in Institution List →] [Close]

---

## 6. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=inst_cohorts` | `exec/partials/cohort_inst.html` | Tab · filter |
| `?part=student_cohorts` | `exec/partials/cohort_students.html` | Tab · filter |
| `?part=rev_cohorts` | `exec/partials/cohort_revenue.html` | Tab · filter |
| `?part=cohort_drawer&cohort={id}&month={n}` | `exec/partials/cohort_cell_drawer.html` | Cell click |

**Django view dispatch:**
```python
class CohortAnalysisView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_exec_analytics"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "inst_cohorts": "exec/partials/cohort_inst.html",
                "student_cohorts": "exec/partials/cohort_students.html",
                "rev_cohorts": "exec/partials/cohort_revenue.html",
                "cohort_drawer": "exec/partials/cohort_cell_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/cohort_analysis.html", ctx)
```

---

## 7. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| Heatmap (36 rows × 7 cols) | < 400 ms | > 1 s |
| Retention line chart | < 400 ms | > 1 s |
| Revenue cohort heatmap | < 500 ms | > 1.2 s |
| Cohort cell drawer | < 300 ms | > 800 ms |
| Full page initial load | < 1.2 s | > 3 s |

**Data note:** All cohort aggregates pre-computed nightly via Celery. No live aggregation during page load. Stored in `cohort_retention_cache` table.

---

## 8. States & Edge Cases

| State | Behaviour |
|---|---|
| Cohort size < 10 (institutions) | Cell shows "—" (insufficient data) |
| Cohort size < 100 (students) | Cell shows "—" (privacy protection) |
| Future months (N/A) | `bg-[#1E293B]` grey cell + "—" text |
| NRR > 150% | Cap display at 150% with "+" indicator |
| All cohorts selected in chart | Warn "Showing too many lines — select fewer cohorts for clarity" |

---

## 9. Template Files

| File | Purpose |
|---|---|
| `exec/cohort_analysis.html` | Full page shell |
| `exec/partials/cohort_inst.html` | Institution cohorts tab |
| `exec/partials/cohort_students.html` | Student cohorts tab |
| `exec/partials/cohort_revenue.html` | Revenue cohorts tab |
| `exec/partials/cohort_cell_drawer.html` | Cell detail drawer |

---

## 10. Component References

| Component | Used in |
|---|---|
| `TabBar` | §4.2–4.4 |
| `GlobalFilterBar` | §4.1 |
| `CohortHeatmap` | §4.2.1, §4.3.1, §4.4.1 |
| `RetentionLineChart` | §4.2.2, §4.3.2 |
| `CohortSummaryTable` | §4.2.3 |
| `NRRHeatmap` | §4.4.1 |
| `NRRTrendChart` | §4.4.2 |
| `RevenueCohortTable` | §4.4.3 |
| `DrawerPanel` | §5.1 |
| `CohortTogglePills` | §4.2.2 (chart cohort selector) |
