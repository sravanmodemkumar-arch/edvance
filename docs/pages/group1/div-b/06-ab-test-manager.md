# 06 — A/B Test Manager

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total institutions available for experiments | 2,050 |
| Students indirectly affected | 2.4M–7.6M |
| Active experiments at any time | 5–10 |
| Minimum experiment duration | 14 days (to reach statistical significance) |
| Minimum sample per variant | 30 institutions (for 80% power at p=0.05) |
| Experiment types | UI variant · Feature flag rollout · Pricing display · Onboarding flow · Notification copy |
| Primary metrics | Exam creation rate · Student enrollment · Feature adoption % · Support ticket rate |

**Why this page matters at scale:** At 2,050 institutions, PMs cannot rely on intuition alone. A/B tests replace opinion with evidence. When testing a new exam creation UI on 5% of coaching centres (5 centres, avg 10K students = 50K students in test), statistical significance can be reached in 14 days. Without this tooling, PMs either roll out to everyone (high risk) or never validate (stagnation). Feature flags (page 02) handle deployment; A/B tests handle measurement.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | A/B Test Manager |
| Route | `/product/experiments/` |
| Django view class | `ABTestManagerView` |
| Template | `product/ab_test_manager.html` |
| Permission — view | `portal.view_ab_tests` (all div-b roles) |
| Permission — manage | `portal.manage_ab_tests` (PM Platform only) |
| Permission — publish winner | `portal.publish_ab_test` (PM Platform + 2FA) |
| 2FA required | Yes — declare winner, end experiment early, push winner to 100% |
| HTMX poll — running experiments | Every 120s (paused when drawer/modal open) |
| Nav group | Product |
| Nav icon | `flask` |
| Priority | P2 |

---

## 3. Wireframe

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: A/B Test Manager                    [+ New Experiment]  [Archive] [Docs ↗] │
├────────┬────────┬────────┬────────┬────────────────────────────────────────────────┤
│ Total  │Running │Completed│ Draft  │ Statistical Significance                      │
│  28    │   6    │  18     │   4    │  4/6 running have reached significance ✓      │
├────────┴────────┴────────┴────────┴────────────────────────────────────────────────┤
│ TABS: [Running (6)] [Completed (18)] [Draft (4)] [Archived]                        │
├────────────────────────────────────────────────────────────────────────────────────┤
│ FILTER: [Search...] [Type ▾] [Domain ▾] [PM Owner ▾] [Apply]                     │
├────────────────────────────────────────────────────────────────────────────────────┤
│ EXPERIMENT CARDS GRID (2 columns)                                                  │
│                                                                                    │
│ ┌─ new_exam_ui_v3 ─────────────────┐  ┌─ onboarding_step_order ──────────────┐  │
│ │ New Exam Interface v3             │  │ Onboarding Step Reorder              │  │
│ │ Running · Day 8/14 · ██████░░     │  │ Running · Day 3/14 · ██░░░░░░        │  │
│ │ Control: 90% · Variant: 10%       │  │ Control: 95% · Variant: 5%           │  │
│ │ Primary: Exam creation rate       │  │ Primary: Onboarding completion %     │  │
│ │ Control: 3.2/wk  Variant: 4.1/wk │  │ Control: 67%  Variant: 71%           │  │
│ │ Lift: +28.1% ✓ Significant        │  │ Lift: +6.0% — Not yet significant    │  │
│ │ [View Details] [Declare Winner]   │  │ [View Details]                       │  │
│ └──────────────────────────────────┘  └──────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Value | Detail |
|---|---|---|---|
| 1 | Total Experiments | `28` | All time |
| 2 | Running | `6` | Currently collecting data |
| 3 | Completed | `18` | Results declared |
| 4 | Draft | `4` | Configured but not started |
| 5 | Significance Reached | `4/6` | Running experiments with p < 0.05 |

**Significance card:** `4/6` — fraction format
When all running experiments have reached significance: `bg-[#064E3B] border border-[#10B981]`
When any running experiment is overdue (> 60 days without significance): `bg-[#451A03] border border-[#F59E0B]`

---

### 4.2 Tab Bar

| Tab | Badge | Description |
|---|---|---|
| Running | `6` | Active experiments collecting data — auto-poll every 120s |
| Completed | `18` | Finished experiments with declared results |
| Draft | `4` | Configured, not yet started |
| Archived | — | Old experiments (> 1 year) |

---

### 4.3 Experiment Card (Running)

`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-5`
**Border colour by significance:**
- Significant (p < 0.05): `border-[#10B981]`
- Not yet significant: `border-[#1E2D4A]`
- Running too long (> 60d): `border-[#F59E0B]`

**Card header:**
```
Experiment key (font-mono · text-xs)          [Status badge]
Experiment name (text-base font-semibold)
Domain badge · PM owner · Started N days ago
```

**Duration progress bar:**
`bg-[#1E2D4A] rounded-full h-2`
Fill: `bg-[#6366F1]`
Label: "Day 8 of 14" · `text-xs text-[#94A3B8]`

**Variant split display:**
`flex justify-between text-xs text-[#94A3B8]`
"Control: 90% (1,845 institutions) · Variant A: 10% (205 institutions)"

**Primary metric comparison:**
```
Primary Metric: Exam creation rate (exams/week/institution)
Control:   3.2 /wk  ████████████
Variant A: 4.1 /wk  ████████████████
Lift: +28.1%   p-value: 0.021   ✓ Statistically significant
```

Lift colour:
- Positive + significant: `text-[#34D399]`
- Positive + not significant: `text-[#FCD34D]`
- Negative: `text-[#F87171]`

**Statistical significance badge:**
- Significant: `bg-[#064E3B] text-[#34D399]` "✓ p < 0.05"
- Not significant: `bg-[#1E2D4A] text-[#94A3B8]` "p = 0.12 (not yet)"

**Card footer:**
[View Details] `text-[#6366F1] text-sm` → opens Experiment Detail Drawer
[Declare Winner] `bg-[#6366F1] text-sm` (enabled only when significant) → 2FA modal
[Stop Early] `text-[#F87171] text-sm` → confirmation modal

---

### 4.4 Experiment Detail Drawer (720px)

**Trigger:** [View Details] on card
**Header:** Experiment name + Status badge + Start date + `[×]`

**Tab bar (5 tabs):**

---

#### Tab A — Overview

**Experiment configuration (read-only when running):**
```
Experiment Key:   new_exam_ui_v3
Type:             UI Variant
Domain:           PM Institution Portal
PM Owner:         Priya S.
Started:          Mar 12, 2026
Target end date:  Mar 26, 2026 (14 days)
Hypothesis:       New exam creation flow (3 steps vs 5) will increase weekly exam creation rate by ≥20%
```

**Targeting:**
```
Institution types:  Coaching Centres only (100 institutions)
Plan tiers:         Standard · Professional · Enterprise
Variant split:      Control 90% (90 inst) · Variant A 10% (10 inst)
Minimum sample:     30 institutions per variant (reached: ✓)
```

**Feature flag linked:** `new_exam_ui` flag — Variant A = flag enabled, Control = flag disabled
Link: [View Flag →] opens flag drawer

---

#### Tab B — Results

**Primary Metric Chart:**
Canvas id: `ab-primary-chart` · height 280px · Chart.js line chart
X-axis: Days 1–N
Y-axis: Primary metric value
Series:
- Control: `#6366F1` solid line
- Variant A: `#10B981` solid line
- Dashed CI bands: `#6366F1`/`#10B981` with opacity 20%

**Statistical Summary Table:**

| Metric | Control (N=90) | Variant A (N=10) | Lift | p-value | Significant? |
|---|---|---|---|---|---|
| Exam creation rate | 3.2/wk | 4.1/wk | +28.1% | 0.021 | ✅ Yes |
| Time to create exam | 8.4 min | 6.2 min | -26.2% | 0.003 | ✅ Yes |
| Support tickets/wk | 0.8 | 0.6 | -25.0% | 0.08 | ❌ No |
| Student enrollment/wk | 42 | 44 | +4.8% | 0.31 | ❌ No |

**Power analysis panel:**
`bg-[#0D1526] rounded p-3 text-sm`
- Statistical power: 87% (target: 80% ✓)
- Sample size achieved: 10 institutions (minimum: 30 ⚠ underpowered)
- Confidence level: 95%
- Effect size (Cohen's d): 0.62 (medium)

**[Export Results CSV]** · **[Export as PDF Report]**

---

#### Tab C — Segment Breakdown

**Purpose:** See if results differ by institution type, plan tier, or state.

**Segment selector:** [By Institution Type] [By Plan Tier] [By State]

**Segment table for "By Institution Type":**

| Segment | N (Control) | N (Variant) | Primary Metric (C) | Primary Metric (V) | Lift |
|---|---|---|---|---|---|
| Coaching (all) | 90 | 10 | 3.2 | 4.1 | +28.1% ✓ |
| (No other types in this experiment) | — | — | — | — | — |

Note: If experiment were run on all institution types, breakdown would show each type separately.

---

#### Tab D — Guardrail Metrics

**Purpose:** Ensure the variant doesn't accidentally harm other metrics even while improving primary.

| Guardrail Metric | Control | Variant | Change | Status |
|---|---|---|---|---|
| Error rate (exam submit) | 0.12% | 0.14% | +16.7% | ⚠ Borderline |
| Page load time (P99) | 1.8s | 1.7s | -5.6% | ✅ OK |
| Student complaints | 2.1/wk | 1.9/wk | -9.5% | ✅ OK |
| Session abandonment | 8.3% | 8.1% | -2.4% | ✅ OK |

**Guardrail breach warning:**
If any guardrail metric worsens by > 20%:
`bg-[#1A0A0A] border border-[#EF4444] rounded p-3`
"⚠ Error rate guardrail is at risk. Consider pausing this experiment."

---

#### Tab E — Configuration (editable when Draft only)

Fields:
- Experiment name (editable)
- Hypothesis (editable)
- Type: UI Variant · Feature Variant · Pricing Display · Copy/Text · Onboarding Flow
- Primary metric (select from list of 20 tracked metrics)
- Secondary metrics (multi-select)
- Guardrail metrics (multi-select)
- Target institution type (multi-select)
- Target plan tier (multi-select)
- Variant split % slider
- Duration: number of days (min 7, max 90)
- Feature flag to toggle for variant
- Start date / auto-start option

**[Start Experiment]** button (Draft tab): `bg-[#6366F1]`
**[Edit Configuration]** (Running tab): disabled — config locked once running

---

**Drawer footer:**
[Declare Winner] (significant only · 2FA) · [Stop Early] · [Close]

---

## 5. Modals

### 5.1 New Experiment Modal

**Width:** 600px

| Field | Type | Validation |
|---|---|---|
| Experiment Key | Text · font-mono | slug format · unique · required |
| Name | Text | required · max 100 chars |
| Hypothesis | Textarea | required · "We believe that [change] will [outcome] for [audience] because [reason]" template |
| Type | Select | UI Variant · Feature · Pricing · Copy · Onboarding |
| Domain | Select | PM Platform · PM Exam · PM Portal |
| Primary Metric | Select | 20 options |
| Secondary Metrics | Multi-select | |
| Guardrail Metrics | Multi-select | Required: at least error rate + load time |
| Institution Type | Multi-select | |
| Plan Tiers | Multi-select | |
| Variant Split | Slider 1–50% | Variant gets 1–50%; Control gets remainder. Max variant 50% (safety) |
| Min Duration | Number · days | Min 7 · Recommended 14 |
| Linked Feature Flag | Search | Connects experiment to existing feature flag |

**Sample size estimator** (live, below split slider):
`hx-get="?part=sample_estimate" hx-trigger="change from:#variant-split, change from:#institution-type"`
"At 10% variant split with Coaching Centres (100 institutions): ~10 variant, 90 control. Estimated days to significance: ~18 days (based on historical variance)."

**Footer:** [Create & Save as Draft] · [Create & Start Now] · [Cancel]

---

### 5.2 Declare Winner Modal

**Trigger:** [Declare Winner] on card or drawer
**Width:** 520px

**Results summary (read-only):**
Primary metric lift, p-value, power, sample size

**Winner selection:**
`[○ Declare Control as Winner]`
`[○ Declare Variant A as Winner]`
`[○ No Winner — End Experiment (tie/inconclusive)]`

**Rollout plan (if Variant A wins):**
"After declaring Variant A as winner, what should happen?"
`[○ Immediately roll out to 100% of target institutions`
`[○ Gradually: increase to 50% now, 100% in 7 days`
`[○ Do nothing — manually manage via feature flag`

**2FA verification:** required

**Learning summary (required):**
Textarea: "What did we learn from this experiment?"
Min 30 chars

**Footer:** [Confirm & Declare Winner] `bg-[#6366F1]` · [Cancel]

---

### 5.3 Stop Early Modal

**Width:** 480px
**Warning:** `bg-[#1A0A0A] border border-[#EF4444]`
"Stopping an experiment early introduces bias and invalidates statistical conclusions. Only stop if there is a compelling safety or business reason."

Reason dropdown: P0 Bug · Business priority change · Guardrail breach · Other
Reason text: textarea (required if Other)

**Footer:** [Confirm Stop] `bg-[#EF4444]` · [Cancel]

---

## 6. Django View

```python
class ABTestManagerView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_ab_tests"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":              "product/partials/ab_kpi.html",
                "running":          "product/partials/ab_running.html",
                "completed":        "product/partials/ab_completed.html",
                "draft":            "product/partials/ab_draft.html",
                "experiment_drawer":"product/partials/ab_drawer.html",
                "results_chart":    "product/partials/ab_results_chart.html",
                "sample_estimate":  "product/partials/ab_sample_estimate.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "product/ab_test_manager.html", ctx)

    def post(self, request):
        action = request.POST.get("action")
        if action in {"declare_winner", "publish_winner"}:
            if not request.session.get("2fa_verified"):
                return JsonResponse({"error": "2FA required"}, status=403)
        if not request.user.has_perm("portal.manage_ab_tests"):
            return JsonResponse({"error": "Permission denied"}, status=403)
        dispatch = {
            "create_experiment":  self._create_experiment,
            "start_experiment":   self._start_experiment,
            "stop_early":         self._stop_early,
            "declare_winner":     self._declare_winner,
        }
        handler = dispatch.get(action)
        if handler:
            return handler(request)
        return JsonResponse({"error": "Unknown action"}, status=400)

    def _build_context(self, request):
        from portal.apps.product.models import ABExperiment
        from django.core.cache import cache

        kpi = cache.get_or_set("product:ab:kpi", lambda: {
            "total":        ABExperiment.objects.count(),
            "running":      ABExperiment.objects.filter(status="running").count(),
            "completed":    ABExperiment.objects.filter(status="completed").count(),
            "draft":        ABExperiment.objects.filter(status="draft").count(),
            "significant":  ABExperiment.objects.filter(status="running", is_significant=True).count(),
        }, 120)
        return {"kpi": kpi}
```

---

## 7. Statistical Calculation Reference

```python
# portal/apps/product/stats.py

from scipy import stats
import numpy as np

def compute_significance(control_values, variant_values):
    """
    Two-sample t-test for continuous metrics.
    Returns t-stat, p-value, lift %, power estimate.
    """
    t_stat, p_value = stats.ttest_ind(control_values, variant_values)
    control_mean = np.mean(control_values)
    variant_mean = np.mean(variant_values)
    lift_pct = ((variant_mean - control_mean) / control_mean) * 100 if control_mean else 0

    # Effect size (Cohen's d)
    pooled_std = np.sqrt(
        (np.var(control_values) + np.var(variant_values)) / 2
    )
    cohens_d = (variant_mean - control_mean) / pooled_std if pooled_std else 0

    return {
        "p_value":      round(p_value, 4),
        "is_significant": p_value < 0.05,
        "lift_pct":     round(lift_pct, 2),
        "cohens_d":     round(cohens_d, 3),
        "control_mean": round(control_mean, 4),
        "variant_mean": round(variant_mean, 4),
    }
```

---

## 8. Empty States

| Section | Copy |
|---|---|
| No running experiments | "No experiments running. Create one to start measuring feature impact." |
| No completed experiments | "No completed experiments yet. Results will appear here when experiments finish." |
| No draft experiments | "No drafts. Click '+ New Experiment' to configure your first A/B test." |

---

## 9. Multi-Variant Support (A/B/C Tests)

The platform supports up to 3 variants per experiment (A/B/C split). This is used when PM wants to test two variants simultaneously against control — e.g., testing 3 different onboarding step orders at once.

**Variant configuration (in New Experiment modal):**

| Field | Single Variant (A/B) | Multi-Variant (A/B/C) |
|---|---|---|
| Variant count | 1 variant + control | 2 variants + control |
| Split example | Control 90% / Variant A 10% | Control 80% / A 10% / B 10% |
| Significance test | Two-sample t-test | ANOVA + pairwise post-hoc (Tukey HSD) |
| Declare winner | Control vs Variant A | Control vs A vs B — best variant declared |
| Minimum sample | 30 per group | 30 per group (90 total minimum) |

**Multi-variant card UI:**
```
Control: 3.2/wk  (80%)
Variant A: 4.1/wk (10%)  +28.1% ✓
Variant B: 3.6/wk (10%)  +12.5% ✗ not significant
Winner: Variant A (when significance reached for A, B, or both)
```

**Why max 3 variants:** At 2,050 institutions, splitting into more than 3 groups gives too few institutions per variant to reach statistical power in a reasonable timeframe. A 4-variant test would need 120 institutions minimum — restricting targeting to coaching centres only (100 institutions) would be underpowered.

---

## 10. Experiment Pause and Resume

**Pause:** Temporarily stops collecting data without ending the experiment.
- Use case: A related production incident distorts results (e.g., a bug disproportionately affects Variant A group). PM pauses until incident is resolved.
- Pause adds a "DATA PAUSED" annotation on the Results timeline chart.
- Experiment duration clock does NOT pause — only data collection pauses.
- Maximum pause: 7 days. After 7 days, system auto-sends a reminder: "Experiment paused for 7 days — resume or stop."

**Trigger:** [Pause Collection] in drawer footer (running experiments only)
**Confirmation modal:** "Pause data collection for this experiment? The duration clock will continue running." Reason required (dropdown).

**Resume:** [Resume Collection] in drawer footer (paused experiments only)
Resumes data collection. Annotation added: "Collection resumed — [date]"

**Peeking Warning:** A yellow banner shown in Tab B — Results if the PM opens results before 50% of the experiment duration has elapsed:
> ⚠ **Early peeking inflates false positives.** Checking results on Day 3 of a 14-day experiment at p=0.04 does not mean significance. Wait until at least Day 7 before making decisions. Current power: ~42% (target: 80%).

---

## 11. Notification Rules

| Event | Recipients | Channel | Trigger |
|---|---|---|---|
| Experiment reaches statistical significance | PM owner · PM Platform | In-app + email | p < 0.05 reached |
| Experiment running > 60 days without significance | PM owner · PM Platform | Email + in-app warning | Day 61 |
| Guardrail metric breach > 20% | PM owner | Email + in-app alert (amber) | Threshold crossed |
| Experiment stopped early | PM Platform | In-app | Any early stop |
| Winner declared + rollout complete | PM owner · QA Lead | Email | Rollout to 100% confirmed |
| Underpowered experiment (sample < minimum after 7 days) | PM owner | Email | Day 7 check |

---

## 12. Integration Points

| Page | Direction | What flows |
|---|---|---|
| 02 — Feature Flags | Both | Experiments link to feature flags; flag rollout % is controlled by experiment targeting |
| 03 — Release Manager | Inbound | Experiment results feed into release notes as "validated by experiment EXP-XXX" |
| 16 — Portal Templates | Inbound | UI variant experiments reference portal templates being tested |
| 17 — Onboarding Workflow | Inbound | Onboarding flow experiments reference step sequences defined in page 17 |
| 28 — Revenue & Billing | Inbound | Pricing display experiments (plan page variants) originate from revenue team input |
| 13 — Domain Analytics | Outbound | Experiment results (enrollment lift, dropout reduction) appear in domain analytics as attributed changes |

---

## 13. Key Design Decisions

| Decision | Chosen approach | Why |
|---|---|---|
| Maximum 3 variants | Hard limit enforced in UI | Statistical power at 2,050 institutions requires ≥ 30 per group; > 3 variants demand too many institutions for coaching-only or school-only experiments |
| p < 0.05 threshold | Fixed — not configurable by PM | Configurable significance thresholds invite p-hacking (PM sets threshold after seeing data); fixed threshold prevents this |
| Experiment configuration locked when running | Cannot edit targeting or split after start | Changing split mid-experiment invalidates all pre-change data and introduces selection bias |
| Winner rollout uses feature flags (page 02) | Not a separate mechanism | DRY — flags already handle rollout %; reusing flags means audit trail, kill-switch, and dependency management come for free |
| Peeking warning | Non-blocking (advisory only) | Blocking would frustrate PMs with legitimate reasons to check (e.g., guardrail monitoring); advisory preserves PM autonomy while surfacing the risk |
| RICE scoring for backlog (integrated with page 05) | Shared scoring model | Keeps PM Platform and roadmap aligned on priority; experiment outcomes auto-update the Reach field of linked roadmap features |

---

## 14. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `N` | New Experiment modal |
| `1–4` | Switch tabs |
| `R` | Refresh running experiments |
| `Esc` | Close drawer/modal |
