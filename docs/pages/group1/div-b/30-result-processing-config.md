# 30 — Result Processing & Rank Config

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Result Processing & Rank Config |
| Route | `/product/result-config/` |
| Django view | `ResultProcessingConfigView` |
| Template | `product/result_config.html` |
| Priority | **P1** |
| Nav group | Product |
| Required roles | `pm_exam_domains` · `superadmin` |
| Results Coordinator (div-F role 36) | Read-only (views config, cannot edit) |
| 2FA required | Yes — publishing any normalization formula change or result release |
| HTMX poll | None (config page; not real-time) |
| Cache | Config cached at Redis TTL 3600s; busted on save |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` · warn `#F59E0B` |

---

## 2. Purpose & Business Logic

**The result accuracy problem:**

After 74,000 students complete an exam, the result pipeline runs:
1. Raw answers collected → `ExamAttempt` records
2. Scores computed (marks per correct − penalty per wrong)
3. **Normalization applied** (for multi-shift exams: RRB CBT, SSC CGL Tier 1)
4. Ranks computed (overall + category-wise: UR/OBC/SC/ST/EWS/PwD)
5. Result published to students and institutions

**Why this page exists:**

The normalization formula parameters, rank band definitions, cutoff thresholds, and result release rules are currently hardcoded in the exam engine. Any change requires a backend deployment. This page externalises all configurable parameters into DB-backed config, allowing PM Exam Domains to adjust them without engineering intervention.

**Key computations configured here:**

**RRB Multi-Shift Normalization (most complex):**
```
Normalized Score = Mq + (Mmt - Mqt) × σq / σt

Where:
  Mq = candidate's actual score in their shift
  Mmt = mean score of top 0.1% candidates across all shifts (reference)
  Mqt = mean score of top 0.1% candidates in candidate's shift
  σq = std deviation of candidate's shift
  σt = std deviation of top 0.1% reference group
```

**JEE Percentile:**
```
Percentile = (100 × number of candidates scoring ≤ candidate's NTA score) / total candidates
```

**NEET Rank:**
```
Tie-breaking order: Biology > Chemistry > Physics > older candidate
```

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| PM Exam Domains | All | Edit config, publish (with 2FA) |
| Superadmin | All | Same as PM Exam Domains |
| Results Coordinator | All (read-only) | No edits |
| All others | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Domain Selector & Status

```
Result Processing & Rank Config
────────────────────────────────────────────────────────────────────────────────
[Domain: SSC ▾]   [Exam Type: CGL Tier 1 ▾]

Config Status:  ✅ Published  ·  Last updated: 15 Mar 2026  ·  By: @pm_exam_domains_1
Pending changes: None
```

- Domain selector: SSC / RRB / NEET / JEE / AP Board / TS Board / Banking
- Exam type changes sub-sections shown (each exam type may have different config)
- "Pending changes" shows staged but unpublished changes

---

### Section 2 — Scoring Rules

```
SCORING RULES — SSC CGL Tier 1
────────────────────────────────────────────────────────────────────────────────
Total Questions:  100
Total Marks:      200
Marks per correct: 2
Marks per wrong:  -0.50   (negative marking)
Marks for unattempted: 0

Section-wise Rules:
Section         Questions   Marks   Negative   Time limit
────────────────┼───────────┼────────┼──────────┼──────────
General Intel.   25          50      -0.50      No separate
Quant Aptitude  25          50      -0.50
English          25          50      -0.50
GK               25          50      -0.50

[Edit Scoring Rules]   (2FA required to save)
```

- Changing scoring rules: warning shown "This will affect all future exams using this pattern. Historical results are NOT retroactively updated."
- Section-wise time limits: optional (for NEET-style section locks)

---

### Section 3 — Normalization Config

```
NORMALIZATION CONFIG — RRB NTPC CBT 1
────────────────────────────────────────────────────────────────────────────────
Normalization:  ✅ Enabled   (Multi-shift exam — normalization required)
Formula:        Equi-Percentile   [Absolute Percentile ▾]

Parameters:
Reference group:    Top 0.1% of candidates across all shifts  [Edit]
Min candidates/shift: 100 (minimum to include shift in normalization)
Score floor:        0 (normalized score cannot go below 0)
Score ceiling:      None (normalized score can exceed raw max)
Rounding:           2 decimal places

FORMULA PREVIEW (for current config):
Normalized_Score = Mq + (Mmt - Mqt) × (σq / σt)
Where: Mmt = 89.42 (last exam reference), σt = 8.21
[Recalculate preview with last exam data]

SINGLE-SHIFT EXAMS (normalization disabled):
SSC CGL Tier 2 · NEET UG · JEE Main (single date) — no normalization
```

- Formula options: Equi-Percentile (RRB standard), Absolute Mean (older SSC), None
- "Recalculate preview" runs the formula on the last actual exam's data and shows result distribution — validation tool for PM
- 2FA required to change normalization formula
- Audit trail: every formula change logged with old/new values

---

### Section 4 — Rank Band & Category Config

```
RANK BANDS & CATEGORY CONFIG — SSC CGL Tier 1
────────────────────────────────────────────────────────────────────────────────
Categories:
Code   Name           Reservation %   Cutoff adjustment   Status
UR     Unreserved     —               —                   ✅ Active
OBC    OBC-NCL        27%             -2.5 marks          ✅ Active
SC     Scheduled Caste 15%            -5.0 marks          ✅ Active
ST     Scheduled Tribe 7.5%           -5.0 marks          ✅ Active
EWS    Eco. Weak Sec.  10%            -2.5 marks          ✅ Active
PwD    Disability      3%             -5.0 marks (addl.)  ✅ Active
ExSM   Ex-Servicemen   —              -5.0 marks          ✅ Active

Rank computation order:
1. Normalized score (descending)
2. Tie-break: General Intelligence score (descending)
3. Tie-break: DOB (older candidate gets higher rank)
4. Tie-break: Alphabetical by name

[Edit Category Config]   [Edit Tie-breaking Rules]
```

- Reservation %: informational (not used for platform rank calculation — used for cutoff generation)
- Cutoff adjustment: shown on rank card but not enforced by platform (institutions set their own cutoffs)
- Category fields collected at student registration time; PM configures which categories are applicable per exam type

---

### Section 5 — Cutoff Config

```
CUTOFF CONFIG — SSC CGL Tier 1 (2025 Batch)
────────────────────────────────────────────────────────────────────────────────
Mode:  Institution-defined  (each institution sets their own cutoffs)
       [Switch to Platform-defined ▾]

Platform-defined cutoff (if enabled):
Category   Cutoff Marks   Source
UR         140.00         [Manual entry] / [Auto from last year +5%]
OBC        130.00
SC         120.00
ST         115.00
EWS        128.00

Publish cutoffs: ☐ Show cutoff to students at result time
                 ☑ Show cutoff to institution admins only

[Edit Cutoffs]   [Import from SSC Official Notification]
```

- "Institution-defined" mode: institutions set their own pass mark — platform just ranks, doesn't filter
- "Platform-defined" mode: platform cutoff is applied; students below cutoff see "Not Qualified"
- "Import from SSC Official": manual CSV import of official cutoff notification

---

### Section 6 — Result Release Config

```
RESULT RELEASE CONFIG
────────────────────────────────────────────────────────────────────────────────
Release mode:         Scheduled (auto-release at set time)
Default delay:        Rank computation + 30 min (result finalization buffer)
Institution override: ✅ Allowed (institution admin can delay release by up to 72h)

RESULT VISIBILITY
Student can see:      ✅ Score · ✅ Rank (overall) · ✅ Rank (category) · ✅ Percentile
                      ☐ Answers (answer key visible separately)
Institution sees:     ✅ All student scores · ✅ Rank distribution · ✅ Section-wise analysis
Score rounding:       2 decimal places (display)
Percentile display:   4 decimal places (e.g., 99.9874)

RESULT LOCKING
Lock results after:   90 days (prevent any further changes after this period)
Re-attempt policy:    ☐ Students can see past attempt scores on new attempt
```

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Result Processing & Rank Config    [Domain: SSC ▾]  [Exam: CGL Tier 1 ▾]  ║
║  Config Status: ✅ Published  ·  Last updated: 15 Mar 2026                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  SCORING RULES                       NORMALIZATION CONFIG                   ║
║  100Q · 200M · +2 correct · -0.5 W   ✅ Enabled · Equi-Percentile formula   ║
║  4 sections, equal weight            Ref: Top 0.1% · Floor: 0               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  RANK BANDS & CATEGORY CONFIG        CUTOFF CONFIG                          ║
║  UR / OBC(-2.5) / SC(-5) / ST(-5)   Mode: Institution-defined               ║
║  EWS(-2.5) / PwD(-5) / ExSM(-5)     [Import from SSC Official]              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  RESULT RELEASE CONFIG                                                      ║
║  Auto-release: rank + 30min  ·  Student sees: score + rank + percentile     ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `ScoringRulesForm` | `components/result/scoring_rules.html` | `domain, exam_type, rules, can_edit` |
| `NormalizationConfig` | `components/result/normalization.html` | `formula, params, preview_data, can_edit` |
| `CategoryConfigTable` | `components/result/categories.html` | `categories (list), tie_break_rules, can_edit` |
| `CutoffConfig` | `components/result/cutoffs.html` | `mode, cutoffs (list), can_edit` |
| `ResultReleaseConfig` | `components/result/release.html` | `config, can_edit` |

---

## 7. HTMX Architecture

| `?part=` | Target | Trigger |
|---|---|---|
| `scoring` | `#scoring-rules` | load + domain/exam change |
| `normalization` | `#normalization-config` | load + domain/exam change |
| `categories` | `#category-config` | load + domain/exam change |
| `cutoffs` | `#cutoff-config` | load + domain/exam change |
| `release` | `#result-release` | load + domain/exam change |

---

## 8. Backend View & API

```python
class ResultProcessingConfigView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_result_config"

    MANAGE_ROLES = {"pm_exam_domains","superadmin"}
    READ_ROLES   = {"results_coordinator"}

    def get(self, request):
        if request.user.role not in self.MANAGE_ROLES | self.READ_ROLES:
            return redirect("product:dashboard")
        can_edit = request.user.role in self.MANAGE_ROLES
        domain = request.GET.get("domain","ssc")
        exam_type = request.GET.get("exam_type","cgl_tier1")

        r = get_redis_connection()
        cache_key = f"result_config:{domain}:{exam_type}"
        ctx = json.loads(r.get(cache_key) or "{}")
        if not ctx:
            ctx = self._build_ctx(domain, exam_type)
            r.setex(cache_key, 3600, json.dumps(ctx))
        ctx["can_edit"] = can_edit

        if _is_htmx(request):
            part = request.GET.get("part","")
            dispatch = {
                "scoring":         "product/result/partials/scoring.html",
                "normalization":   "product/result/partials/normalization.html",
                "categories":      "product/result/partials/categories.html",
                "cutoffs":         "product/result/partials/cutoffs.html",
                "release":         "product/result/partials/release.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "product/result_config.html", ctx)

    def post(self, request):
        if request.user.role not in self.MANAGE_ROLES:
            return HttpResponseForbidden()
        # 2FA verified via middleware before POST handler
        section = request.POST.get("section","")
        handlers = {
            "scoring":       self._save_scoring,
            "normalization": self._save_normalization,
            "categories":    self._save_categories,
            "cutoffs":       self._save_cutoffs,
            "release":       self._save_release,
        }
        if section in handlers:
            result = handlers[section](request)
            # Bust cache
            r = get_redis_connection()
            r.delete(f"result_config:{request.POST.get('domain')}:{request.POST.get('exam_type')}")
            return result
        return HttpResponseBadRequest()
```

---

## 9. Database Schema

```python
class ExamResultConfig(models.Model):
    """Per domain + exam type result processing configuration."""
    domain_slug     = models.CharField(max_length=50)    # "ssc", "rrb", "neet"
    exam_type_slug  = models.CharField(max_length=50)    # "cgl_tier1", "ntpc_cbt1"
    scoring_rules   = models.JSONField()
    # {total_q, total_marks, marks_correct, marks_wrong, sections: [...]}
    normalization_enabled = models.BooleanField(default=False)
    normalization_formula = models.CharField(max_length=50,
        choices=[("equi_percentile","Equi-Percentile"),
                 ("absolute_mean","Absolute Mean"),("none","None")])
    normalization_params  = models.JSONField(default=dict)
    # {ref_group_pct: 0.001, min_candidates_per_shift: 100, score_floor: 0}
    category_config = models.JSONField(default=list)
    # [{code, name, cutoff_adj, is_active}, ...]
    tie_break_rules = models.JSONField(default=list)
    # [{"field": "section_score", "section": "general_intelligence", "order": "desc"}, ...]
    cutoff_mode     = models.CharField(max_length=20,
        choices=[("institution","Institution-defined"),("platform","Platform-defined")])
    platform_cutoffs = models.JSONField(default=dict)  # {UR: 140.0, OBC: 130.0, ...}
    result_release_config = models.JSONField(default=dict)
    # {delay_minutes: 30, allow_institution_override: true, max_override_hours: 72, ...}
    published_at    = models.DateTimeField(null=True)
    published_by    = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                         on_delete=models.SET_NULL)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("domain_slug","exam_type_slug")
        indexes = [models.Index(fields=["domain_slug","exam_type_slug"])]


class ResultConfigAuditLog(models.Model):
    """Every change to result config is logged."""
    config          = models.ForeignKey(ExamResultConfig, on_delete=models.PROTECT)
    section         = models.CharField(max_length=50)  # "normalization", "scoring"
    old_value       = models.JSONField()
    new_value       = models.JSONField()
    changed_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    changed_at      = models.DateTimeField(auto_now_add=True)
    change_reason   = models.TextField()
```

---

## 10. Validation Rules

| Action | Validation |
|---|---|
| Marks per correct | Positive number; integer or .5 increments |
| Marks per wrong | Negative number; magnitude ≤ marks per correct |
| Normalization formula | Cannot change if exam with this config is currently live |
| Category cutoff adjustment | Between -20 and 0 marks |
| Result release delay | 0–480 minutes |
| Publish (any change) | 2FA required; change reason mandatory (min 20 chars) |
| Retroactive change | Blocked if any exam using this config has already published results |

---

## 11. Security Considerations

- 2FA-gated for any config publish — a wrong normalization formula at 74K submissions affects 74K student ranks
- `ResultConfigAuditLog` is immutable (no delete on this table) — full historical trail
- Results Coordinator (div-F) has read-only access for operational verification before result release
- Config used by exam engine (Lambda) fetched from Redis cache + DB fallback — cache busted on any publish
- Formula changes cannot be applied retroactively to published results — enforced at view level

---

## 12. Edge Cases

| State | Behaviour |
|---|---|
| Normalization enabled but only 1 shift exists | Warning: "Single shift detected — normalization will be skipped for this exam. Enable only for multi-shift exam days." |
| Tie-break exhausted (all criteria equal) | Alphabetical by name used as final fallback — always resolves |
| Config changed while exam is live | Blocked: "Cannot modify result config while exam `{name}` is live. Wait for exam to complete." |
| Platform cutoff import — official PDF | OCR-based import (Tesseract); extracted values shown for manual review before saving |

---

*Last updated: 2026-03-20*
