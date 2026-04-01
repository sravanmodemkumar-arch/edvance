# div-a-25 — Usage Analytics

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Platform events tracked/day | ~50M–200M |
| Feature adoption tracked | ~30 features |
| API calls/day | ~2M–5M |
| Page views/day | ~2M–10M |
| Unique platform staff users | ~20–50 |
| Institution admin users | ~4,000 |
| Student sessions/day | ~500K–2M |

**Why this matters:** Usage Analytics shows where institutions and students actually spend their time. The product team uses it to kill unused features and prioritise roadmap. The COO uses it to spot "low-engagement" institutions before they churn. This is the product health cockpit.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Usage Analytics |
| Route | `/exec/usage-analytics/` |
| Django view | `UsageAnalyticsView` |
| Template | `exec/usage_analytics.html` |
| Priority | P2 |
| Nav group | Analytics |
| Required role | `exec`, `superadmin` |
| 2FA required | No |
| HTMX poll | KPI strip: every 5 min |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Usage Analytics                      [Export] [Date Range ▾]        │
├────────┬────────┬────────┬────────┬────────┬──────────────────────────────── ┤
│ Active │ Page   │ API    │ Feature│ Avg    │  Top Feature                   │
│ Users  │ Views  │ Calls  │ Adopt. │Session │  This Month                    │
│ (30d)  │ (30d)  │ (30d)  │ Rate   │ Time   │                                │
│ 42,180 │ 8.4M   │ 84.2M  │ 62%    │ 18 min │  Exam Analytics                │
├────────┴────────┴────────┴────────┴────────┴──────────────────────────────── ┤
│ TABS: [Platform Usage] [Feature Adoption] [API Usage] [User Activity]       │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Institution Type ▾] [Plan ▾] [State ▾] [Date Range ▾]                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Active Users (30d) | Unique users who logged in | — |
| 2 | Page Views (30d) | Total page views | — |
| 3 | API Calls (30d) | Total API calls | — |
| 4 | Feature Adoption Rate | % of features used by avg institution | < 40% = amber |
| 5 | Avg Session Time | Mean session duration | < 5 min = amber |
| 6 | Top Feature | Most used feature this month | — |

---

### 4.2 Tab: Platform Usage

`id="tab-platform"` · `hx-get="?part=platform_usage"`

#### 4.2.1 Daily Active Users (line chart, 90 days)

**Series:** Platform staff / Institution admins / Students (separate Y-axis)
**Colours:** Staff `#6366F1` · Admin `#22D3EE` · Students `#10B981`
**Toggle Y-axis log scale** for viewing staff vs students on same chart

#### 4.2.2 Page Views Breakdown (bar chart, stacked by section)

**Sections:** Dashboard / Exam / Student / Billing / Reports / Settings / Other
**X-axis:** last 30 days

#### 4.2.3 Top Pages Table

| Page | Views (30d) | Unique Users | Avg Time on Page |
|---|---|---|---|
| Exam Catalog | 842,000 | 3,240 | 4:32 |
| Dashboard | 612,000 | 4,180 | 2:18 |

---

### 4.3 Tab: Feature Adoption

`id="tab-features"` · `hx-get="?part=feature_adoption"`

#### 4.3.1 Feature Adoption Heatmap

**Rows:** 30 features (sorted by adoption % desc)
**Columns:** Institution type (School / College / Coaching / Group)
**Cell:** adoption % · coloured same as cohort heatmap (green = high · red = low)

#### 4.3.2 Feature Adoption Trend

Line chart (3 series) for selected feature · Adoption % over 12 months

**Feature selector:** dropdown at top

#### 4.3.3 Low Adoption Alert Table

Institutions with feature adoption < 30% (churn risk signal)
| Institution | Type | Features used | % | Last active |
|---|---|---|---|---|

---

### 4.4 Tab: API Usage

`id="tab-api"` · `hx-get="?part=api_usage"`

Links to div-a-31 for deep API detail. Shows summary here:

#### 4.4.1 API Calls Trend (line chart, 30 days)

**Series:** Total calls / Error calls / Rate-limited calls
**Y-axis:** count (K suffix)

#### 4.4.2 Top Endpoints Table

| Endpoint | Calls (30d) | Error rate | Avg latency |
|---|---|---|---|
| GET /api/exams/ | 18.4M | 0.2% | 42ms |
| POST /api/results/ | 8.2M | 0.4% | 128ms |

#### 4.4.3 Top API Consumers Table

| Institution | API calls (30d) | Error rate | Rate limit hits |
|---|---|---|---|

---

### 4.5 Tab: User Activity

`id="tab-users"` · `hx-get="?part=user_activity"`

#### 4.5.1 Login Activity Heatmap

7 days × 24 hours · value = login count · same heatmap style as student analytics

#### 4.5.2 User Activity Table

Platform staff activity log (last 30 days)
| User | Role | Last login | Page views | Actions taken | Sessions |
|---|---|---|---|---|---|

**Filter:** Role · Date range

---

## 5. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/usage_kpi.html` | Page load · poll 5 min |
| `?part=platform_usage` | `exec/partials/usage_platform.html` | Tab · filter change |
| `?part=feature_adoption` | `exec/partials/usage_features.html` | Tab · filter change |
| `?part=api_usage` | `exec/partials/usage_api.html` | Tab · filter change |
| `?part=user_activity` | `exec/partials/usage_users.html` | Tab · filter change |

**Django view dispatch:**
```python
class UsageAnalyticsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_exec_analytics"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/usage_kpi.html",
                "platform_usage": "exec/partials/usage_platform.html",
                "feature_adoption": "exec/partials/usage_features.html",
                "api_usage": "exec/partials/usage_api.html",
                "user_activity": "exec/partials/usage_users.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/usage_analytics.html", ctx)
```

---

## 6. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 300 ms | > 800 ms |
| Platform usage tab (3 charts) | < 600 ms | > 1.5 s |
| Feature adoption heatmap | < 500 ms | > 1.2 s |
| API usage tab | < 400 ms | > 1 s |
| Full page initial load | < 1.2 s | > 3 s |

---

## 7. States & Edge Cases

| State | Behaviour |
|---|---|
| Feature adoption < 20% platform-wide | Amber banner "Low platform feature adoption — consider onboarding review" |
| API error rate > 2% | Red alert on API Usage KPI card |
| 0 API calls in period | API Usage tab shows "No API usage in selected period" |

---

## 8. Template Files

| File | Purpose |
|---|---|
| `exec/usage_analytics.html` | Full page shell |
| `exec/partials/usage_kpi.html` | KPI strip |
| `exec/partials/usage_platform.html` | Platform usage tab |
| `exec/partials/usage_features.html` | Feature adoption tab |
| `exec/partials/usage_api.html` | API usage tab |
| `exec/partials/usage_users.html` | User activity tab |

---

## 9. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `TabBar` | §4.2–4.5 |
| `GlobalFilterBar` | §4 |
| `DailyActiveChart` | §4.2.1 |
| `StackedBarChart` | §4.2.2 |
| `TopPagesTable` | §4.2.3 |
| `FeatureAdoptionHeatmap` | §4.3.1 |
| `AdoptionTrendLine` | §4.3.2 |
| `LowAdoptionTable` | §4.3.3 |
| `APITrendChart` | §4.4.1 |
| `TopEndpointsTable` | §4.4.2 |
| `LoginHeatmap` | §4.5.1 |
| `UserActivityTable` | §4.5.2 |
| `PollableContainer` | KPI strip |
