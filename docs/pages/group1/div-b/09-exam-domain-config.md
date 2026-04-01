# 09 — Exam Domain Config

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Exam domains (active) | 6 primary + IBPS/SBI/Banking as additional |
| SSC exams | CGL Tier 1/2/3/4 · CHSL Tier 1/2 · CPO · MTS · Stenographer |
| RRB exams | NTPC CBT 1/2 · Group D · JE · ALP · Paramedical |
| NEET | NEET-UG · NEET-PG (2 variants) |
| JEE | JEE Main (Paper 1 & 2) · JEE Advanced |
| AP Board | Class 10 (SSC) · Class 12 (Intermediate) · EAPCET · ECET |
| TS Board | Class 10 · Class 12 · TSEAMCET · TSICET |
| Coaching centres using exam domains | 100 (all domains) |
| Schools using domains | 1,000 (State Board primarily) |
| Colleges using domains | 800 (State Board + JEE/NEET) |
| Questions per domain | SSC: ~400K · RRB: ~350K · NEET: ~280K · JEE: ~200K · Boards: ~150K each |
| Students enrolled per domain | SSC: ~420K · RRB: ~380K · NEET: ~280K · JEE: ~190K |

**Why this page matters at scale:** Exam domain config is the foundational metadata layer. Every question, test series, syllabus, and result computation depends on correct domain configuration. A misconfigured domain (wrong marks scheme, wrong normalization formula) at 74K concurrent submissions means 74K incorrect scores. PM Exam Domains is accountable for this accuracy. This page separates structural config (owned by PM) from content (owned by Division D SMEs).

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Exam Domain Config |
| Route | `/product/exam-domains/` |
| Django view class | `ExamDomainConfigView` |
| Template | `product/exam_domain_config.html` |
| Permission — view | `portal.view_exam_domains` (all div-b roles) |
| Permission — manage | `portal.manage_exam_domains` (PM Exam Domains only) |
| Permission — publish | `portal.publish_exam_domain` (PM Exam Domains + 2FA) |
| 2FA required | Yes — publish domain changes, disable domain, change marks scheme |
| HTMX poll | None — on-demand config page |
| Nav group | Product |
| Nav icon | `graduation-cap` |
| Priority | P1 |

---

## 3. Wireframe

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Exam Domain Config              [+ New Domain]  [Export Config]  [Audit]   │
├────────┬────────┬────────┬────────┬────────────────────────────────────────────────┤
│ Total  │Active  │Disabled│Pending │ Total Enrolled Students                        │
│Domains │  8     │   0    │Config  │  1.72M across all domains                     │
│  8     │        │        │   2    │                                                │
├────────┴────────┴────────┴────────┴────────────────────────────────────────────────┤
│ TABS: [All Domains] [SSC] [RRB] [NEET/JEE] [State Boards] [Banking & Others]      │
├────────────────────────────────────────────────────────────────────────────────────┤
│ DOMAIN CARDS GRID (2 columns)                                                      │
│                                                                                    │
│ ┌─ SSC ──────────────────────────┐  ┌─ RRB ──────────────────────────────────┐  │
│ │ Staff Selection Commission      │  │ Railway Recruitment Board               │  │
│ │ ● Active · 9 exam types        │  │ ● Active · 7 exam types                │  │
│ │ Questions: 400K  Students: 420K │  │ Questions: 350K  Students: 380K        │  │
│ │ Last updated: Mar 15            │  │ Last updated: Feb 28                   │  │
│ │ [Configure] [View Syllabus]     │  │ [Configure] [View Syllabus]            │  │
│ └────────────────────────────────┘  └────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Domain Cards Grid

**Layout:** `grid grid-cols-2 gap-4 p-4`

### 4.1 Domain Card

`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-5 hover:border-[#6366F1] cursor-pointer`

**Card structure:**
```
[Domain abbreviation badge]  [Status badge]         [Pending changes ⚠ if any]
Domain full name
Conducting body / authority

────────────────────────────────────────────────
Exam types:    9                  Questions: 400K
Students:    420K                 Test Series:  42
Last updated: Mar 15, 2026        Coverage: 87%

[Configure →]   [View Syllabus]   [Domain Analytics ↗]
```

**Domain abbreviation badge:** `text-xl font-bold text-white bg-[#6366F1] rounded-lg w-10 h-10 flex items-center justify-center`

**Status badge:**
- Active: `bg-[#064E3B] text-[#34D399]`
- Disabled: `bg-[#450A0A] text-[#F87171]`
- Pending Config: `bg-[#451A03] text-[#FCD34D]`
- Draft (new, not published): `bg-[#1E2D4A] text-[#94A3B8]`

**Pending changes dot:** `w-2 h-2 bg-[#F59E0B] rounded-full animate-pulse` top-right corner

**Card click:** opens Domain Config Drawer (720px)

---

### 4.2 All Domains Reference

| Domain | Full Name | Authority | Active Exams | Students | Status |
|---|---|---|---|---|---|
| SSC | Staff Selection Commission | Union Public Service / SSC HQ | 9 exam types | ~420K | Active |
| RRB | Railway Recruitment Board | Ministry of Railways | 7 exam types | ~380K | Active |
| NEET | National Eligibility cum Entrance Test | NTA | 2 variants | ~280K | Active |
| JEE | Joint Entrance Examination | NTA / IITs | 3 variants | ~190K | Active |
| AP Board | Andhra Pradesh State Board | BSEAP / APSCHE | 4 exam types | ~240K | Active |
| TS Board | Telangana State Board | BSETS / TSCHE | 4 exam types | ~210K | Active |
| IBPS | Institute of Banking Personnel Selection | IBPS | 5 exam types | ~80K | Active |
| SBI | State Bank of India | SBI | 3 exam types | ~40K | Active |

---

## 5. Domain Config Drawer (720px)

**Trigger:** [Configure →] on domain card or card click
**Header:** Domain abbreviation badge + full name + status badge + `[×]`

**Tab bar (6 tabs):** Metadata · Exam Types · Subjects · Marks Scheme · Normalization · Settings

---

### Tab A — Metadata

**Fields (editable):**

| Field | Type | Value |
|---|---|---|
| Domain Key | Text · font-mono · slug | `ssc` (read-only) |
| Display Name | Text | "SSC — Staff Selection Commission" |
| Short Name | Text | "SSC" |
| Conducting Authority | Text | "Staff Selection Commission, India" |
| Official Website | URL | `https://ssc.nic.in` |
| Application Base URL | URL | URL where students can apply |
| Description | Textarea | Rich description for institution-facing display |
| Category | Select | Central Govt · State Govt · Medical · Engineering · Banking |
| Eligibility summary | Textarea | e.g., "10+2 to Graduate depending on post" |
| Target institutions | Checkbox | Schools · Colleges · Coaching · All |
| Featured order | Number | Display order on domain landing page (1 = first) |
| Logo upload | File | SVG/PNG · max 100KB · transparent background |
| Colour accent | Hex picker | Domain-specific accent colour for UI (e.g., SSC: `#1D4ED8`) |

**Status controls:**
`flex gap-3 items-center`
[Activate] / [Disable] button — 2FA required for disable
Disable warning: "Disabling this domain will hide it from 100 coaching centres and their students."

---

### Tab B — Exam Types

**Purpose:** Define all exam types within this domain (e.g., within SSC: CGL Tier 1, CGL Tier 2, CHSL, etc.)

#### Exam Types Table

| # | Exam Code | Exam Name | Status | Pattern | Questions | Linked Series | Actions ⋯ |
|---|---|---|---|---|---|---|---|
| 1 | SSC-CGL-T1 | SSC CGL Tier 1 | Active | 4 sections · 100Q · 60min | 85K | 18 series | ⋯ |
| 2 | SSC-CGL-T2 | SSC CGL Tier 2 | Active | 4 papers · varies | 72K | 12 series | ⋯ |
| 3 | SSC-CHSL-T1 | SSC CHSL Tier 1 | Active | 4 sections · 100Q · 60min | 45K | 8 series | ⋯ |
| 4 | SSC-CPO | SSC CPO | Active | 2 papers | 38K | 6 series | ⋯ |
| 5 | SSC-MTS | SSC MTS | Active | 2 tiers | 28K | 4 series | ⋯ |

**Kebab menu (⋯):**
- Edit → inline row edit or opens Exam Type Edit Modal
- View in Exam Pattern Builder → links to page 12
- View in Syllabus Builder → links to page 10 with filter
- Disable Exam Type
- Delete (only if no linked content)

**[+ Add Exam Type]** button → New Exam Type Modal

---

#### New Exam Type Modal (from domain drawer)

**Width:** 520px

| Field | Type |
|---|---|
| Exam Code | Text · font-mono · e.g., `SSC-CGL-T3` |
| Exam Name | Text |
| Full Name | Text · official name |
| Year (first conducted) | Year picker |
| Frequency | Select: Annual · Biannual · Irregular |
| Status | Active / Disabled / Draft |
| Default Pattern | Select from Exam Pattern Builder patterns |
| Copy syllabus from | Select existing exam type in this domain (optional) |

---

### Tab C — Subjects

**Purpose:** Configure which subjects are part of this domain. This feeds into the Syllabus Builder (page 10).

**Subject Table:**

| Subject | Code | Topic Count | Q count | Required? | Display Order | Actions |
|---|---|---|---|---|---|---|
| Quantitative Aptitude | QA | 48 topics | 85K | ✅ Yes | 1 | Edit · Disable |
| General Intelligence | GI | 32 topics | 62K | ✅ Yes | 2 | Edit · Disable |
| English Language | EL | 40 topics | 78K | ✅ Yes | 3 | Edit · Disable |
| General Awareness | GA | 55 topics | 90K | ✅ Yes | 4 | Edit · Disable |
| Statistics (Tier 2) | STAT | 28 topics | 18K | ✗ Optional | 5 | Edit · Disable |

**[+ Add Subject]** → adds subject to domain

**Subject row click** → shows topic summary inline (collapsed accordion)

---

### Tab D — Marks Scheme

**Purpose:** Configure scoring rules for this domain. This is the authoritative marks scheme used by the result computation engine.

**Per-exam-type marks scheme:**

Exam type selector dropdown at top: `[SSC CGL Tier 1 ▾]`

**Marks scheme form:**

| Field | Type | Example |
|---|---|---|
| Total questions | Number | 100 |
| Total marks | Number | 200 |
| Marks per correct answer | Decimal (Decimal(5,2)) | 2.00 |
| Negative marking | Decimal | -0.50 |
| No negative for | Checkbox | `[ ] Mathematics section exempt from negative marking` |
| Unattempted question marks | Decimal | 0.00 (always) |
| Bonus marks rules | Textarea | "If ≥ 2 incorrect options in official key, award marks to all" |
| Normalization | Checkbox | `[ ] Apply normalization (multi-shift exams)` → links to Tab E |

**Per-section override:**
If exam has multiple sections with different marks schemes:
Table: Section Name · Questions · Marks/Correct · Negative · Time Limit

Example (SSC CGL Tier 1):
| Section | Questions | Marks/Q | Negative |
|---|---|---|---|
| General Intelligence & Reasoning | 25 | 2 | -0.5 |
| General Awareness | 25 | 2 | -0.5 |
| Quantitative Aptitude | 25 | 2 | -0.5 |
| English Comprehension | 25 | 2 | -0.5 |
| **Total** | **100** | — | — |

**[Save Marks Scheme]** — 2FA required (marks scheme change affects all result computations)

---

### Tab E — Normalization

**Purpose:** RRB and some SSC exams are conducted in multiple shifts. Raw scores must be normalized across shifts to be fair.

**Normalization toggle:**
`[ ] Enable normalization for multi-shift exams`
(Enabled for RRB NTPC, RRB Group D, SSC CGL Tier 1 when multi-shift)

**Normalization formula selector:**

| Formula | Used by | Description |
|---|---|---|
| NTA Normalization | NEET, JEE Main | Based on percentile of candidates |
| Railway Board Formula | RRB NTPC, Group D | Adjusted mean + adjusted standard deviation method |
| SSC Normalization | SSC CGL T1 multi-shift | Min/Max method with floor adjustment |
| None | Single shift exams | Raw score = final score |

**Selected formula parameters (editable):**

For Railway Board Formula:
```
Adjusted Score Formula:
Score_i_j = {
  (M_t - M_b) / (M_g_b - M_b) × (M_g_t - M_t) + M_t   if raw_score ≠ 0
  0                                                       if raw_score = 0
}

Where:
  M_t  = mean of shift t             [auto-computed from results]
  M_b  = best shift mean             [auto-computed]
  M_g_t = mean of global best        [auto-computed]
  M_g_b = global best mean           [auto-computed]
```

**[View Normalization Test]** button: runs normalization on a sample dataset and shows before/after comparison table (QA validation tool)

---

### Tab F — Settings

**Domain-level settings:**

| Setting | Type | Value |
|---|---|---|
| Allow free practice (non-registered) | Toggle | On/Off |
| Show domain on student registration | Toggle | On/Off (hide inactive domains) |
| Minimum subscription plan to access | Select | Starter / Standard / Professional |
| Show cut-off history | Toggle | On/Off |
| Allow institution to create domain exams | Toggle | On/Off (coaching only: yes; schools: limited) |
| Result visibility | Select | Immediate / After all submit / Manual release |
| Rank computation method | Select | All-India rank / Institution rank / Both |
| Question shuffle | Toggle | On/Off (per exam — overridable per exam) |
| Option shuffle | Toggle | On/Off |

**[Save Settings]** — standard save (no 2FA for settings changes)
**[Publish Domain Changes]** — 2FA required — publishes all Tab D (marks scheme) and Tab E (normalization) staged changes

---

## 6. Modals

### 6.1 New Domain Modal

**Width:** 600px

| Field | Type |
|---|---|
| Domain Key | Text · slug · unique |
| Display Name | Text |
| Short Name | Text · max 10 chars |
| Conducting Authority | Text |
| Category | Select |
| Target Institutions | Checkbox group |
| Copy config from | Select (optional — clone from existing domain) |
| Initial Status | Draft / Active |

**Footer:** [Create Domain] · [Cancel]

---

### 6.2 Disable Domain Modal

**Width:** 480px
**Warning:** `bg-[#1A0A0A] border border-[#EF4444]`

Impact assessment:
- "100 coaching centres have this domain enabled"
- "~420K students are enrolled in SSC prep"
- "18 active test series will be hidden"
- "42 upcoming exams will be postponed"

2FA + reason required.

---

## 7. Django View

```python
class ExamDomainConfigView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_exam_domains"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":             "product/partials/domains_kpi.html",
                "domain_cards":    "product/partials/domains_cards.html",
                "domain_drawer":   "product/partials/domain_drawer.html",
                "marks_scheme":    "product/partials/domain_marks.html",
                "normalization":   "product/partials/domain_norm.html",
                "exam_types":      "product/partials/domain_exam_types.html",
                "subjects":        "product/partials/domain_subjects.html",
                "norm_test":       "product/partials/domain_norm_test.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "product/exam_domain_config.html", ctx)

    def post(self, request):
        action = request.POST.get("action")
        if action in {"publish_domain", "update_marks_scheme", "disable_domain", "update_normalization"}:
            if not request.session.get("2fa_verified"):
                return JsonResponse({"error": "2FA required"}, status=403)
        if not request.user.has_perm("portal.manage_exam_domains"):
            return JsonResponse({"error": "Permission denied"}, status=403)
        dispatch = {
            "create_domain":          self._create_domain,
            "update_domain_metadata": self._update_metadata,
            "create_exam_type":       self._create_exam_type,
            "update_exam_type":       self._update_exam_type,
            "update_marks_scheme":    self._update_marks_scheme,
            "update_normalization":   self._update_normalization,
            "publish_domain":         self._publish_domain,
            "disable_domain":         self._disable_domain,
            "add_subject":            self._add_subject,
            "update_settings":        self._update_settings,
        }
        handler = dispatch.get(action)
        if handler:
            return handler(request)
        return JsonResponse({"error": "Unknown action"}, status=400)
```

---

## 8. Data Model Reference

```python
class ExamDomain(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"), ("disabled", "Disabled"), ("draft", "Draft"),
    ]
    key            = models.SlugField(max_length=20, unique=True, db_index=True)
    display_name   = models.CharField(max_length=100)
    short_name     = models.CharField(max_length=10)
    authority      = models.CharField(max_length=100)
    category       = models.CharField(max_length=30)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    description    = models.TextField(blank=True)
    colour_accent  = models.CharField(max_length=7, default="#6366F1")
    featured_order = models.PositiveSmallIntegerField(default=99)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["featured_order", "short_name"]


class ExamType(models.Model):
    domain      = models.ForeignKey(ExamDomain, on_delete=models.CASCADE, related_name="exam_types")
    code        = models.CharField(max_length=30, unique=True, db_index=True)
    name        = models.CharField(max_length=100)
    full_name   = models.CharField(max_length=200)
    frequency   = models.CharField(max_length=20)
    status      = models.CharField(max_length=20, default="active")
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("domain", "code")]


class MarksScheme(models.Model):
    exam_type        = models.OneToOneField(ExamType, on_delete=models.CASCADE, related_name="marks_scheme")
    total_questions  = models.PositiveSmallIntegerField()
    total_marks      = models.DecimalField(max_digits=7, decimal_places=2)
    marks_correct    = models.DecimalField(max_digits=5, decimal_places=2)
    marks_negative   = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0"))
    marks_unattempted= models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0"))
    normalization    = models.CharField(max_length=30, default="none")
    updated_at       = models.DateTimeField(auto_now=True)
    updated_by       = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
```

---

---

## G2 Amendment — Localization / i18n Config per Domain

### Purpose

The platform serves students in AP Board (Telugu-medium), TS Board (Telugu/Urdu), NEET (English/Hindi), SSC (Hindi/English), and Banking (English). Question content, UI labels, exam instructions, and result messages must be available in the correct language per domain. Without an explicit i18n config per domain, the frontend cannot know which locales to load or which content versions to display.

---

### Localization Tab (added to Domain Config Drawer — Tab 6 after Analytics)

**Tab label:** 🌐 Localization

**Why in the drawer and not a separate page:** Localization settings are tightly coupled to a specific exam domain — the supported languages for SSC Hindi are fundamentally different from AP Board Telugu. A single i18n page would require constant domain context-switching; attaching the tab to the domain drawer keeps context intact.

---

### Localization Tab — Content

**Section 1: Supported Locales**

| Language | Code | Script | Status | Default? | Content Coverage |
|---|---|---|---|---|---|
| English | `en` | Latin | Active | ✅ (for SSC/Banking/JEE/NEET) | 100% |
| Hindi | `hi` | Devanagari | Active | ✅ (for SSC/RRB) | 94% |
| Telugu | `te` | Telugu | Active | ✅ (for AP Board/TS Board) | 88% |
| Urdu | `ur` | Nastaliq (RTL) | Active | — | 71% |
| Tamil | `ta` | Tamil | Beta | — | 43% |
| Kannada | `kn` | Kannada | Planned | — | 12% |

- **Default locale:** The locale loaded when a student has not set a personal language preference. Only one locale can be the default per domain. Changing the default triggers a warning: "This will change the language for ~{N} students who have not set a preference."
- **Status options:** Active · Beta (available but marked "preview") · Planned (visible in admin but not served to students) · Disabled
- **Content coverage %:** Computed automatically from the question bank — (questions with translation in this locale / total questions in this domain) × 100. Updates nightly.

**Section 2: UI String Translations**

UI labels, error messages, exam instructions, and button text are separate from question content. This section shows translation completeness for portal UI strings.

| String Category | Total Strings | Telugu | Hindi | Urdu |
|---|---|---|---|---|
| Exam instructions | 48 | 48 ✅ | 48 ✅ | 42 ⚠ |
| Result page labels | 32 | 32 ✅ | 32 ✅ | 28 ⚠ |
| Error messages | 120 | 110 ⚠ | 118 ✅ | 89 ⚠ |
| Navigation & buttons | 86 | 86 ✅ | 86 ✅ | 79 ⚠ |
| Notification templates | 24 | 22 ⚠ | 24 ✅ | 18 ⚠ |

Missing strings shown with a ⚠ badge and a "View Missing →" link that opens a modal listing all untranslated strings with an inline text area for PM to submit draft translations (routed to content team for review).

**Section 3: RTL Support**

For Urdu (`ur`) and any future Arabic/RTL locale:
- Toggle: "Enable RTL layout for this domain" — when ON, all portal UI elements mirror for RTL rendering (text direction, icon placement, table column order)
- RTL status indicator: "RTL layout is currently Active / Inactive for Urdu users on this domain"
- Warning: "RTL requires design review — submit a review request to UI Review Board (page 20) before enabling in production"

**Section 4: Language Switcher Config**

Controls what students see in the language picker at the top of the exam portal:
- Show language switcher: Yes / No (per domain)
- Switcher position: Top-right navbar / Exam start screen only / Both
- Languages shown in switcher: checkboxes matching Supported Locales above (only Active locales can be shown to students)
- Mid-exam language switch: Allow / Block — if "Block": language can only be selected at exam start screen; "Allow": student can switch anytime (question text reloads in new locale)

**Section 5: Locale Publish**

Changes to locale config follow the same staged-changes workflow as domain metadata:
- "Stage Changes" button → amber banner: "Localization changes pending publication"
- Review modal: shows each change (e.g., "Telugu set as default locale for AP Board — affects 4,200 students")
- 2FA → Publish

---

## 9. Empty States

| Section | Copy |
|---|---|
| No domains | "No exam domains configured. Add your first domain to get started." |
| No exam types for domain | "No exam types for this domain. Add exam types in the Exam Types tab." |
| No subjects | "No subjects linked. Configure subjects via the Syllabus Builder." |

---

## 10. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `N` | New Domain modal |
| `1–6` | Switch domain category tabs |
| `Esc` | Close drawer/modal |
| `P` | Publish staged domain changes (2FA) |
