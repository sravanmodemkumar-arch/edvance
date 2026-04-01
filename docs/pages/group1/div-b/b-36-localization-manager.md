# B-36 — Localization & i18n Manager

> **Route:** `/product/localization/`
> **Division:** B — Product & Design
> **Primary Role:** PM — Institution Portal (Role 7, Level 5) · UI/UX Designer (Role 8, Level 4)
> **Read Access:** Content Director (Role 18) · Frontend Engineer (Role 12) · Mobile Engineer (Role 13)
> **File:** `b-36-localization-manager.md`
> **Priority:** P1 — India's 22 scheduled languages; NEP 2020 mother-tongue education mandate
> **Status:** ✅ New page — critical for pan-India deployment across 16 institution types

---

## 1. Purpose

Centralized management console for all translatable strings, UI labels, exam content language variants, notification templates, and regional formatting rules across EduForge's multi-tenant platform. At 2,050 institutions spanning 28 Indian states and 8 UTs, the platform must support **at minimum 10 languages** for student-facing content and **3 languages** for admin/staff interfaces.

NEP 2020 mandates mother-tongue instruction through Class 5 and recommends it through Class 8. CBSE now offers board exams in Hindi + English. State boards (AP, TS, Tamil Nadu, Karnataka, etc.) require vernacular-medium support. Coaching centres serving regional markets (e.g., Kota Hindi-medium, Kerala Malayalam-medium) need fully localized student experiences.

This page manages: (1) string catalogue with translation status per language, (2) translation workflow (source → translate → review → publish), (3) regional formatting (date formats, number formats, currency, calendar systems), (4) RTL support management (Urdu), (5) exam content language variant tracking (linked to D-02 question editor), (6) mobile app string bundles (Flutter ARB files), and (7) AI-assisted translation with human review gate.

---

## 2. Language Support Matrix

```
LANGUAGE SUPPORT — EduForge Platform

TIER 1 (Full support — all interfaces + content):
  English (en)     — Default; all strings authored in English first
  Hindi (hi)       — 42% of institutions; CBSE Hindi-medium; coaching centre primary
  Telugu (te)      — 18% of institutions; TS/AP state boards; GCEH college portal

TIER 2 (Student-facing + notifications; admin in English):
  Tamil (ta)       — TN state boards; coaching centres
  Kannada (kn)     — Karnataka state boards
  Malayalam (ml)   — Kerala state boards
  Marathi (mr)     — Maharashtra state boards
  Bengali (bn)     — WB state boards; pan-India coaching
  Gujarati (gu)    — Gujarat state boards

TIER 3 (Exam content only; UI in English/Hindi):
  Urdu (ur)        — RTL support required; minority institutions; CBSE Urdu medium
  Odia (or)        — Odisha boards
  Punjabi (pa)     — Punjab boards
  Assamese (as)    — Assam boards

CURRENT STATUS (March 2027):
  Strings in catalogue: 4,842 (platform UI + notifications + error messages)
  English: 4,842 / 4,842 (100%) ✅
  Hindi:   4,218 / 4,842 (87.1%) — 624 untranslated (mostly new features)
  Telugu:  3,986 / 4,842 (82.3%)
  Tamil:   2,412 / 4,842 (49.8%) — ⚠️ below threshold
  Others:  <40% — in progress
```

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Localization & i18n Manager            [Import Strings] [Export]    │
├─────────────────────────────────────────────────────────────────────┤
│  LANGUAGE COVERAGE KPI (6 tiles)                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ 4,842    │ │ 87.1%    │ │ 82.3%    │ │ 49.8%    │ │ 124      │ │
│  │ Total    │ │ Hindi    │ │ Telugu   │ │ Tamil    │ │ Pending  │ │
│  │ Strings  │ │ Coverage │ │ Coverage │ │ Coverage │ │ Review   │ │
│  │          │ │ ✅ >80%  │ │ ✅ >80%  │ │ ⚠️ <50%  │ │          │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│  [String Catalogue] [Translation Queue] [Regional Config] [Exam i18n] │
├─────────────────────────────────────────────────────────────────────┤
│  STRING CATALOGUE                                                   │
│  Module: [All ▼] Language: [Hindi ▼] Status: [Untranslated ▼]      │
│  Search: [________________]                                         │
│                                                                     │
│  Key                      │ English            │ Hindi        │ ✏️  │
│  ─────────────────────────────────────────────────────────────────  │
│  dashboard.welcome        │ Welcome, {name}    │ स्वागत, {name}│ ✅ │
│  exam.submit_confirm      │ Submit exam?       │ —            │ ⬜ │
│  fee.overdue_notice       │ Fee overdue by...  │ शुल्क बकाया...│ ✅ │
│  attendance.absent_alert  │ Your ward was...   │ आपका बच्चा...│ ✅ │
│                                                                     │
│  Showing 1–50 of 624 untranslated strings [Load more...]            │
├─────────────────────────────────────────────────────────────────────┤
│  TRANSLATION WORKFLOW                                               │
│  Source (EN) → AI Translate (GPT-4/Gemini) → Human Review → Publish │
│                                                                     │
│  AI Queue: 312 strings pending AI translation                       │
│  Review Queue: 124 strings pending human review                     │
│  Published today: 48 strings                                        │
│  Reviewers: Priya (Hindi) · Lakshmi (Telugu) · Karthik (Tamil)      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Models

```python
class LocaleString(models.Model):
    """Master string catalogue — source of truth for all translatable text."""
    key = models.CharField(max_length=200, unique=True)  # "dashboard.welcome"
    module = models.CharField(max_length=50)  # "dashboard", "exam", "fee", "attendance"
    context = models.TextField(null=True)  # "Shown on student dashboard after login"
    source_text = models.TextField()  # English source
    placeholders = models.JSONField(default=list)  # ["{name}", "{amount}"]
    max_length = models.IntegerField(null=True)  # UI constraint (button labels)
    screenshot_url = models.URLField(null=True)  # R2 URL of UI screenshot with string
    platform = models.CharField(choices=[
        ('WEB', 'Web'), ('MOBILE', 'Mobile'), ('BOTH', 'Both'), ('EMAIL', 'Email/SMS')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Translation(models.Model):
    """Each translation of a source string into a target language."""
    locale_string = models.ForeignKey(LocaleString, on_delete=models.CASCADE)
    language = models.CharField(max_length=5)  # "hi", "te", "ta"
    translated_text = models.TextField()
    status = models.CharField(choices=[
        ('AI_DRAFT', 'AI Draft'), ('HUMAN_REVIEW', 'In Review'),
        ('APPROVED', 'Approved'), ('PUBLISHED', 'Published'),
        ('REJECTED', 'Rejected — Re-translate')
    ])
    ai_model = models.CharField(max_length=50, null=True)  # "gpt-4-turbo"
    ai_confidence = models.FloatField(null=True)  # 0.0–1.0
    reviewer = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)
    reviewed_at = models.DateTimeField(null=True)
    reviewer_notes = models.TextField(null=True)
    version = models.IntegerField(default=1)

class RegionalConfig(models.Model):
    """Regional formatting rules per language/locale."""
    language = models.CharField(max_length=5, unique=True)
    date_format = models.CharField(max_length=20)  # "DD/MM/YYYY" (India standard)
    time_format = models.CharField(max_length=10)  # "12h" or "24h"
    number_format = models.CharField(max_length=20)  # "##,##,###.##" (Indian lakhs/crores)
    currency_symbol = models.CharField(max_length=5, default="₹")
    currency_position = models.CharField(choices=[('BEFORE','₹100'),('AFTER','100₹')])
    text_direction = models.CharField(choices=[('LTR','LTR'),('RTL','RTL')], default='LTR')
    font_family = models.CharField(max_length=100)  # "Noto Sans Devanagari"
    calendar_system = models.CharField(default='GREGORIAN')
    first_day_of_week = models.IntegerField(default=1)  # 1=Monday (Indian standard)
```

---

## 5. Business Rules

- **AI translation must NEVER be published without human review for exam-facing content.** A mistranslated exam question that says "which is NOT correct" but the Hindi translation drops the "NOT" creates a catastrophic assessment error affecting thousands of students. The review gate is mandatory and non-bypassable. Low-risk strings (footer text, "Loading...") can use AI-only for Tier 3 languages with PM approval.
- **Placeholder preservation is critical.** `{name}`, `{amount}`, `{date}` must appear in translated strings exactly as in the source. Hindi translators sometimes translate the placeholder itself. EduForge validates: translated text must contain every placeholder from `locale_string.placeholders`; missing placeholders → auto-reject back to translator with error highlight.
- **Indian number formatting (lakhs/crores) is non-negotiable for all Indian languages.** Displaying `₹1,234,567` (Western) instead of `₹12,34,567` (Indian) is incorrect for Indian users. `RegionalConfig.number_format` must use `##,##,###.##` for all Indian locales. This applies to fee amounts, salary, revenue — every monetary display.
- **RTL support for Urdu requires separate CSS and testing.** Urdu (`ur`) is RTL; all flexbox layouts must reverse; form labels must be right-aligned; icons that imply direction (arrows, progress bars) must mirror. This is not achievable with `dir="rtl"` alone — each component needs RTL testing. The WCAG and i18n testing checklist tracks RTL verification per page.
- **String extraction from code must be automated.** Developers writing `"Submit Exam"` as a hardcoded string instead of `{% trans "exam.submit" %}` creates untranslatable UI. The CI/CD pipeline (C-09) must include a linting step that flags hardcoded user-facing strings in templates and Dart code (Flutter). This is enforced as a pre-merge check.
- **Mobile (Flutter) string bundles must be version-synced.** Flutter uses ARB files for localization; web uses Django `gettext` `.po` files. The `LocaleString` table is the single source; export scripts generate both ARB and PO formats. A mismatch between mobile and web translations for the same key creates user confusion.

---

*Last updated: 2026-03-30 · Group 1 — Platform Admin · Division B*
