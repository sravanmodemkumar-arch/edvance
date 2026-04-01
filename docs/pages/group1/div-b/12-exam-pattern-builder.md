# 12 — Exam Pattern Builder

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total exam patterns defined | ~80–120 patterns across all domains |
| SSC patterns | ~15 (CGL T1/T2/T3/T4, CHSL T1/T2, CPO T1/T2, MTS T1/T2, Steno T1/T2, GD Constable) |
| RRB patterns | ~10 (NTPC CBT1/CBT2, Group D, JE, ALP Stage1/2, Paramedical, NTPC Jr Clerk) |
| NEET/JEE patterns | ~5 (NEET UG, NEET PG, JEE Main P1, JEE Main P2, JEE Advanced) |
| State Board patterns | ~8 (AP Class 10, AP Inter, EAPCET, TS Class 10, TS Inter, TSEAMCET) |
| Banking patterns | ~10 (IBPS PO, IBPS Clerk, IBPS RRB, SBI PO, SBI Clerk, RBI, NABARD) |
| Peak concurrent exams using same pattern | 74,000 students using SSC CGL T1 pattern simultaneously |

**Why this page matters at scale:** Exam patterns are the blueprint for every exam generated on the platform. When SSC CGL Tier 1 has 100 questions across 4 sections with 2 marks for correct and -0.5 for wrong, that pattern must be defined exactly once and reused across thousands of mock tests. At 74K concurrent, a pattern error (e.g., wrong time limit) means 74K exams with incorrect timing. This page is the single source of truth for all exam structural rules — separate from syllabus content (what questions) and test series (which exams are bundled).

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Exam Pattern Builder |
| Route | `/product/exam-patterns/` |
| Django view class | `ExamPatternBuilderView` |
| Template | `product/exam_pattern_builder.html` |
| Permission — view | `portal.view_exam_patterns` (all div-b roles) |
| Permission — manage | `portal.manage_exam_patterns` (PM Exam Domains only) |
| Permission — publish | `portal.publish_exam_pattern` (PM Exam Domains + 2FA) |
| 2FA required | Yes — publish pattern, modify published pattern marks scheme |
| HTMX poll | None |
| Nav group | Product |
| Nav icon | `layout-grid` |
| Priority | P1 |

---

## 3. Wireframe

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Exam Pattern Builder              [+ New Pattern]  [Clone]  [Export All]  │
├────────┬────────┬────────┬────────────────────────────────────────────────────────┤
│ Total  │ Active │ Draft  │  Used in exams                                         │
│Patterns│   95   │   20   │   40,820 exams use platform patterns                  │
│  115   │        │        │                                                        │
├────────┴────────┴────────┴────────────────────────────────────────────────────────┤
│ TABS: [All Patterns] [SSC (15)] [RRB (10)] [NEET/JEE (5)] [Boards (8)] [Banking] │
├────────────────────────────────────────────────────────────────────────────────────┤
│ TOOLBAR: [🔍 Search...] [Domain ▾] [Status ▾] [Multi-shift ▾] [Apply]            │
├────────────────────────────────────────────────────────────────────────────────────┤
│ TABLE                                                                              │
│ Pattern Name          │ Domain │ Sections │ Qs  │ Marks │ Time  │ Status │ ⋯    │
│ SSC CGL Tier 1        │ SSC    │   4      │ 100 │  200  │ 60min │ Active │ ⋯    │
│ SSC CHSL Tier 1       │ SSC    │   4      │ 100 │  200  │ 60min │ Active │ ⋯    │
│ RRB NTPC CBT 1        │ RRB    │   3      │ 100 │  100  │ 90min │ Active │ ⋯    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Value | Alert |
|---|---|---|---|
| 1 | Total Patterns | `115` | — |
| 2 | Active | `95` | — |
| 3 | Draft | `20` | > 30 days in draft = amber |
| 4 | Exams using patterns | `40,820` | — |

---

### 4.2 Pattern Table

| Column | Width | Sortable |
|---|---|---|
| Pattern Name | 220px | Yes |
| Domain | 80px | Yes |
| Sections | 70px | Yes |
| Total Questions | 80px | Yes |
| Total Marks | 80px | Yes |
| Duration (min) | 90px | Yes |
| Negative Marking | 80px | No |
| Normalization | 100px | No |
| Exams Using | 90px | Yes |
| Status | 90px | Yes |
| Version | 60px | No |
| Actions ⋯ | 48px | — |

**Multi-shift badge:** `text-[10px] bg-[#312E81] text-[#A5B4FC]` "Multi-shift" shown if normalization enabled

**Exams Using column:** linked number — click → filters exam catalog to this pattern

**Kebab menu (⋯):**
- Edit / Configure → opens Pattern Editor Drawer (720px)
- Clone Pattern → clone modal
- View Usage → shows which exams use this pattern
- Publish → 2FA modal
- Deprecate
- Delete (only if Exams Using = 0)

---

## 5. Pattern Editor Drawer (720px)

**Trigger:** Row click or [Edit] from kebab
**Header:** Pattern name + Domain badge + Status badge + Version badge + `[×]`

**Read-only banner if Active and used in > 0 exams:**
`bg-[#451A03] border border-[#F59E0B] rounded p-3 mb-4`
"This pattern is used by {N} exams. Changes will be staged as v{N+1} and require 2FA to publish. Existing published exams will not be affected — only new exams created after publish."

**Tab bar (5 tabs):** Basic Info · Section Builder · Marks Scheme · Normalization · Preview

---

### Tab A — Basic Info

| Field | Type | Notes |
|---|---|---|
| Pattern Code | Text · font-mono | e.g., `SSC_CGL_T1` · required · unique |
| Pattern Name | Text | e.g., "SSC CGL Tier 1 CBT" |
| Domain | Select | From active exam domains |
| Exam Type | Select (within domain) | e.g., SSC CGL |
| Year Introduced | Year | When this pattern was officially introduced |
| Source | Text | "Official SSC notification 2024-25" |
| Multi-shift | Toggle | Yes = normalization applies |
| Conducting Mode | Select | Online CBT · Offline OMR · Online+OMR Hybrid |
| Language Options | Multi-select | English · Hindi · Telugu (languages exam is offered in) |
| Negative Marking | Toggle | On/Off overall |
| Calculator allowed | Toggle | Per paper (some SSC Tier 2 papers allow) |
| Status | Active / Draft |

---

### Tab B — Section Builder

**Purpose:** Define the sections within this exam pattern. SSC CGL Tier 1 has 4 sections. JEE Advanced Paper 1 has 3 sections with different question types per section.

#### Section List

`id="sections-list"` · Drag-and-drop to reorder sections

Each section card:
`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4 mb-3`

**Section card header:**
```
[≡]  Section {N}: [Section Name ▾]       [Duplicate] [Delete]
Subject: [Quantitative Aptitude ▾]
```

**Section fields (inline editable):**

| Field | Type | Example |
|---|---|---|
| Section Name | Text | "Quantitative Aptitude" |
| Subject | Select from syllabus | Quantitative Aptitude |
| Total Questions | Number | 25 |
| Compulsory | Toggle | If No → optional section |
| Min Questions to Attempt | Number | 20 (if optional sections allowed) |
| Time Limit | Number · minutes | 20 (if sectional timer) or blank (shared timer) |
| Question Types | Checkbox group | MCQ (4 options) · MSQ (multiple select) · Fill blank · Integer |
| MCQ questions | Number | 20 |
| MSQ questions | Number | 5 (if MSQ enabled) |
| Integer type questions | Number | 0 |

**Section Summary bar (auto-computed):**
`flex gap-6 text-xs text-[#94A3B8] border-t border-[#1E2D4A] pt-3 mt-3`
- Total marks for section: `50 marks`
- Marks/correct: `2`
- Marks/wrong: `-0.5`
- Time per question (avg): `1.2 min`

**[+ Add Section]** button: adds new section card at bottom

**Total pattern summary (sticky footer within tab):**
`bg-[#131F38] rounded p-3 flex gap-8 text-sm`
- Sections: `4`
- Total Questions: `100`
- Total Marks: `200`
- Total Duration: `60 min`
- Avg time per question: `36 sec`

---

### Tab C — Marks Scheme

**Purpose:** Detailed marks configuration per section and per question type. Overrides the domain-level marks scheme for this specific pattern.

#### Global Marks Config

| Setting | Value | Editable |
|---|---|---|
| Marks per correct answer (MCQ) | `+2.00` | ✅ Yes |
| Negative marking (MCQ) | `-0.50` | ✅ Yes |
| Marks per correct (MSQ — all correct) | `+4.00` | ✅ Yes |
| Partial marks (MSQ — some correct) | `+1.00 per correct option` | ✅ Yes |
| Wrong option in MSQ | `-1.00 per wrong selected` | ✅ Yes |
| Integer type correct | `+3.00` | ✅ Yes |
| Integer type wrong | `0.00` (no negative) | ✅ Yes |
| Unattempted | `0.00` | Read-only |

**Per-section override:**
Toggle: `[ ] Apply different marks scheme for specific sections`
If enabled, table shows overrides per section (e.g., SSC CGL Tier 2 Paper 2 Math has different marks)

**Bonus marks rules:**
`textarea` for special rules:
"If official answer key has ≥ 2 correct options: award marks to all attempting students regardless of answer selected."

**Tie-breaking rule:**
Select: Marks → then Accuracy (fewer wrongs) → then Age (younger preferred) · Order configurable

---

### Tab D — Normalization

**Shown only when multi-shift = enabled**

**Formula selector:**

`[○ Railway Board Formula (Adjusted Mean & SD)`
`[○ NTA Normalization (Percentile-based)`
`[○ SSC Min-Max Method`
`[○ Custom Formula`

**Selected formula parameters (Railway Board):**

```
Formula:
Normalized_Score_i = ((M_t_q - M_b_q) / (S_t_q)) × S_b_q + M_b_q

Where:
  M_t_q = Mean score of top 0.1% in shift t
  M_b_q = Mean score of top 0.1% in best shift
  S_t_q = Standard deviation of shift t
  S_b_q = Standard deviation of best shift
```

Parameters (editable):
- Top % used for mean computation: `[0.1]`%
- Minimum raw score floor: `[0]` (scores below this not normalized)
- Maximum normalized score cap: `[Total Marks]`

**[Run Test Normalization]** button:
Upload sample CSV of raw scores from 2 shifts → shows normalized scores comparison table

| Student | Shift | Raw Score | Normalized Score |
|---|---|---|---|
| #1 | Shift 1 | 142.5 | 156.2 |
| #2 | Shift 2 | 148.0 | 144.8 |

---

### Tab E — Preview

**Purpose:** Renders what the exam looks like to a student based on this pattern. Shows section structure, timer display, question count per section.

**Exam interface preview (read-only):**
`bg-[#070C18] rounded-xl border border-[#1E2D4A] p-6 max-w-[700px] mx-auto`

```
SSC CGL Tier 1 Mock Exam
─────────────────────────────
Sections: [QA] [GI] [EL] [GA]      Time: 60:00  ←countdown

Section: Quantitative Aptitude (25 Questions · 50 Marks)
─────────────────────────────
Q.1. [Sample MCQ question based on section subject]
  ○ (A) Option text
  ○ (B) Option text
  ○ (C) Option text
  ○ (D) Option text

[Previous] [Mark for Review] [Save & Next]
─────────────────────────────
Section Status: 0/25 Attempted · 0 Marked for Review
```

**[Send Preview to Test Institution]** — deploys a preview exam to a designated test institution

---

**Drawer footer:**
[Save as Draft] · [Publish Pattern] `bg-[#6366F1]` (2FA required) · [Close]

---

## 6. Modals

### 6.1 New Pattern Modal

**Width:** 520px

| Field | Type |
|---|---|
| Pattern Code | Text · font-mono · required |
| Pattern Name | Text · required |
| Domain | Select |
| Copy from existing pattern | Select (optional — clone structure without publishing) |
| Initial status | Draft |

---

### 6.2 Clone Pattern Modal

**Width:** 440px

- Source pattern: read-only
- New pattern code: text
- New pattern name: text
- Copy normalization config: `[✓]`

---

### 6.3 Publish Pattern Modal

**Width:** 500px
**2FA required**

**Impact display:**
"Publishing SSC CGL Tier 1 v5 will:
- Apply to all NEW exams created with this pattern from today
- NOT affect {N} exams already created with v4"

"What changed in v5 vs v4:"
```
- Section 1 Questions: 25 → 30 (+5)
- Total Questions: 100 → 110 (+10)
- Total Duration: 60min → 75min (+15min)
```

**2FA code field** + **[Confirm Publish]** · [Cancel]

---

### 6.4 View Usage Modal

**Trigger:** kebab → View Usage
**Width:** 600px

Table: Exam Name · Series · Domain · Status · Created by Institution · Students attempted

Sorted by student count desc.
Pagination: 25/page.

---

## 7. Django View

```python
class ExamPatternBuilderView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_exam_patterns"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":              "product/partials/patterns_kpi.html",
                "table":            "product/partials/patterns_table.html",
                "pattern_drawer":   "product/partials/pattern_drawer.html",
                "norm_test":        "product/partials/pattern_norm_test.html",
                "pattern_preview":  "product/partials/pattern_preview.html",
                "pattern_usage":    "product/partials/pattern_usage.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "product/exam_pattern_builder.html", ctx)

    def post(self, request):
        action = request.POST.get("action")
        if action in {"publish_pattern", "update_marks_scheme"}:
            if not request.session.get("2fa_verified"):
                return JsonResponse({"error": "2FA required"}, status=403)
        if not request.user.has_perm("portal.manage_exam_patterns"):
            return JsonResponse({"error": "Permission denied"}, status=403)
        dispatch = {
            "create_pattern":       self._create_pattern,
            "update_basic_info":    self._update_basic_info,
            "update_sections":      self._update_sections,
            "update_marks_scheme":  self._update_marks_scheme,
            "update_normalization": self._update_normalization,
            "publish_pattern":      self._publish_pattern,
            "clone_pattern":        self._clone_pattern,
            "run_norm_test":        self._run_norm_test,
        }
        handler = dispatch.get(action)
        if handler:
            return handler(request)
        return JsonResponse({"error": "Unknown action"}, status=400)
```

---

## 8. Data Model Reference

```python
class ExamPattern(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("draft", "Draft"), ("deprecated", "Deprecated")]
    CONDUCT_CHOICES = [
        ("online_cbt", "Online CBT"),
        ("offline_omr", "Offline OMR"),
        ("hybrid", "Online + OMR Hybrid"),
    ]

    code             = models.SlugField(max_length=40, unique=True)
    name             = models.CharField(max_length=120)
    domain           = models.ForeignKey("ExamDomain", on_delete=models.PROTECT)
    exam_type        = models.ForeignKey("ExamType", on_delete=models.PROTECT, null=True, blank=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft", db_index=True)
    version          = models.PositiveSmallIntegerField(default=1)
    is_multi_shift   = models.BooleanField(default=False)
    normalization    = models.CharField(max_length=30, default="none")
    conduct_mode     = models.CharField(max_length=20, choices=CONDUCT_CHOICES, default="online_cbt")
    total_duration_min = models.PositiveSmallIntegerField()
    year_introduced  = models.PositiveSmallIntegerField(null=True, blank=True)
    source_reference = models.CharField(max_length=200, blank=True)
    negative_marking = models.BooleanField(default=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    @property
    def total_questions(self):
        return self.sections.aggregate(total=models.Sum("total_questions"))["total"] or 0

    @property
    def total_marks(self):
        # Sum across sections: questions × marks_per_correct
        total = Decimal("0")
        for s in self.sections.all():
            total += Decimal(str(s.total_questions)) * s.marks_correct
        return total


class ExamPatternSection(models.Model):
    pattern          = models.ForeignKey(ExamPattern, on_delete=models.CASCADE, related_name="sections")
    order            = models.PositiveSmallIntegerField(default=0)
    name             = models.CharField(max_length=80)
    subject          = models.ForeignKey("SyllabusNode", on_delete=models.SET_NULL, null=True)
    total_questions  = models.PositiveSmallIntegerField()
    mcq_count        = models.PositiveSmallIntegerField(default=0)
    msq_count        = models.PositiveSmallIntegerField(default=0)
    integer_count    = models.PositiveSmallIntegerField(default=0)
    is_compulsory    = models.BooleanField(default=True)
    time_limit_min   = models.PositiveSmallIntegerField(null=True, blank=True)
    marks_correct    = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("2.00"))
    marks_negative   = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("-0.50"))
    marks_unattempted= models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["order"]
        unique_together = [("pattern", "order")]
```

---

## 9. Pattern Reference: Key Exams

### SSC CGL Tier 1

| Section | Qs | Marks | Time |
|---|---|---|---|
| General Intelligence | 25 | 50 | — |
| General Awareness | 25 | 50 | — |
| Quantitative Aptitude | 25 | 50 | — |
| English Comprehension | 25 | 50 | — |
| **Total** | **100** | **200** | **60 min** |
Negative: -0.5 · Multi-shift: Yes (SSC normalization)

### RRB NTPC CBT 1

| Section | Qs | Marks |
|---|---|---|
| Mathematics | 30 | 30 |
| General Intelligence | 30 | 30 |
| General Awareness | 40 | 40 |
| **Total** | **100** | **100** |
Time: 90 min · Negative: -1/3 · Multi-shift: Yes (Railway formula)

### NEET UG

| Section | Qs | Marks |
|---|---|---|
| Physics (Sec A: 35, Sec B: 15 opt/attempt 10) | 45 | 180 |
| Chemistry (Sec A: 35, Sec B: 15 opt/attempt 10) | 45 | 180 |
| Biology (Sec A: 35, Sec B: 15 opt/attempt 10) | 45 | 180 |
| **Total** | **135 (attempt 180)** | **540** |
Time: 200 min · Negative: -1 for wrong · Single shift

---

## 10. Empty States & Error States

| State | Display |
|---|---|
| No patterns | "No exam patterns yet. Create your first pattern." |
| Pattern in use — trying to delete | "Cannot delete — {N} exams use this pattern. Deprecate instead." |
| Normalization test upload failed | "Could not parse uploaded CSV. Expected columns: student_id, shift, raw_score." |
| Section marks sum mismatch | Amber warning: "Section marks × questions = {N} but Total Marks field says {M}. Auto-fix?" |

---

## 11. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `N` | New Pattern modal |
| `C` | Clone Pattern |
| `1–5` | Switch drawer tabs |
| `P` | Publish pattern (2FA modal) |
| `Esc` | Close drawer/modal |
