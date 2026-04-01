# div-a-22 — Question Bank

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total questions | ~2M+ |
| Subjects | 25+ |
| Question types | MCQ / Numerical / Fill-in / Match / Assertion-Reason |
| Languages | English / Hindi / Telugu / Tamil / Kannada |
| Questions added/day | ~500–2,000 |
| Questions used in exams/day | ~50,000–200,000 |
| Difficulty distribution | Easy 30% / Medium 50% / Hard 20% |
| Questions flagged for review | ~5,000 active flags |
| Version history per question | Full changelog |

**Why this matters:** The Question Bank is the intellectual property core of the platform. At 2M+ questions across 25 subjects, quality and searchability are critical. Duplicate questions, incorrect answers, or quality degradation directly impacts exam integrity and institutional trust.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Question Bank |
| Route | `/exec/question-bank/` |
| Django view | `QuestionBankView` |
| Template | `exec/question_bank.html` |
| Priority | P2 |
| Nav group | Exams |
| Required role | `exec`, `superadmin`, `ops`, `content` |
| 2FA required | Bulk delete / Archive |
| HTMX poll | Stats strip: on load only |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Question Bank                    [+ Add Question] [Bulk Import ▾]   │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────────────────┤
│  Total   │ Active   │ Flagged  │ Today    │ Hard     │  Used (30d)          │
│  2.1M    │  1.98M   │  4,821   │  +842    │  420K    │  1.2M                │
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────────────────┤
│ [🔍 Search question text, tags, ID...]                                       │
│ [Subject ▾] [Type ▾] [Difficulty ▾] [Language ▾] [Status ▾] [Class ▾]      │
├──────────────────────────────────────────────────────────────────────────────┤
│ TABS: [All Questions] [Flagged] [Recently Added] [Question Sets]            │
├──────────────────────────────────────────────────────────────────────────────┤
│ [☐] [Bulk ▾]  Showing 1–25 / 2.1M  Sort: [Last Used ▾]  [Columns ▾]       │
├──────────────────────────────────────────────────────────────────────────────┤
│ ☐ │ Q ID     │ Preview           │ Subject │ Type │ Difficulty│ Used │ ⋯  │
│   │ Q-184291 │ A body of mass m…  │ Physics │ MCQ  │ Medium    │  842 │     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Total | All questions (active + archived) | — |
| 2 | Active | Status = Active | — |
| 3 | Flagged | Questions flagged for quality review | > 10K = amber |
| 4 | Today | New questions added today | — |
| 5 | Hard | Difficulty = Hard | — |
| 6 | Used (30d) | Questions used in exams in last 30 days | — |

---

### 4.2 Search & Filter Bar

**Search:** Full-text search on question text · debounced 500ms (expensive query on 2M+ rows)
Uses: DB full-text index (`tsvector`) or Elasticsearch if available

**Filters:**
| Filter | Options |
|---|---|
| Subject | Multi-select: 25+ subjects grouped by category |
| Type | MCQ / Numerical / Fill-in / Match / Assertion-Reason |
| Difficulty | Easy / Medium / Hard |
| Language | English / Hindi / Telugu / Tamil / Kannada |
| Status | Active / Flagged / Archived / Draft |
| Class | Class 6–12 / JEE / NEET / UPSC / etc. |
| Source | Institution name (contributed questions) |

---

### 4.3 Table Toolbar

Select-all · Bulk actions: [Archive] [Flag] [Export] [Delete] (2FA for delete)
Sort: Last Used / Date Added / Usage Count · Columns toggle

---

### 4.4 Question Table

`id="question-table"` · `hx-get="?part=question_table"`

| Column | Width | Detail |
|---|---|---|
| ☐ | 40px | Checkbox |
| Q ID | 90px | `Q-XXXXXX` monospace |
| Preview | 320px | First 80 chars of question text (LaTeX rendered to text) |
| Subject | 100px | Badge |
| Class | 70px | Badge |
| Type | 80px | MCQ / Numerical / etc. |
| Difficulty | 90px | Easy (green) / Medium (amber) / Hard (red) |
| Language | 80px | Language flag + name |
| Usage (total) | 80px | Times used in exams |
| Usage (30d) | 80px | Times used last 30 days |
| Status | 100px | Badge |
| Actions ⋯ | 48px | View / Edit / Flag / Archive / Delete |

**Row click:** opens Question Detail Drawer (§5.1)
**Pagination:** 25/page · URL pushstate

---

### 4.5 Tab: Flagged

`id="tab-flagged"` · `hx-get="?part=flagged_questions"`

Filtered to flagged questions. Extra columns:
- Flag reason: Incorrect answer / Poor quality / Duplicate / Outdated
- Flagged by: Username
- Flagged at: Date
- [Review] quick button

---

### 4.6 Tab: Question Sets

`id="tab-sets"` · `hx-get="?part=question_sets"`

**Purpose:** Named collections of questions (reusable exam templates).

| Column | Detail |
|---|---|
| Set name | Name |
| Subject | Badge |
| Questions | Count |
| Created | Date |
| Used in exams | Count |
| Actions ⋯ | View / Edit / Use in Exam / Archive |

**[+ Create Set]** button

---

## 5. Drawers

### 5.1 Question Detail Drawer (720 px)

`id="question-drawer"` · `w-[720px]` · `body.drawer-open`

**Header:** Q ID + Type badge + Difficulty badge + Status · `[×]`

**Tab bar (3 tabs):** Question · Analytics · History

**Tab A — Question:**
Full question rendered (with LaTeX math, images)
- Question text (full)
- Options (for MCQ): each option with correct answer highlighted
- Answer: correct answer + explanation (if available)
- Tags: subject, chapter, concept, difficulty
- Language
- Source: institution or "Platform"
- Created by / Created at

**Edit mode:** [Edit ✎] pencil button → transforms display into editable form (markdown/LaTeX editor)
Fields: question text · options (A/B/C/D) · correct answer · explanation · tags · difficulty
**[Save Changes]** · creates version in history

**Tab B — Analytics:**
- Total times used
- Usage by exam type (bar chart)
- Avg score when this question appears: % correct
- Question difficulty index (empirical, from usage data)
- Institutions that used it most (top 5 table)

**Tab C — History:**
Version history: date + changed by + diff summary
[View version] for any entry

**Footer:** [Save Changes] [Flag Question] [Archive] [Close]

---

## 6. Modals

### 6.1 Add Question Modal (720 px)

**Fields:**
| Field | Type |
|---|---|
| Question type | Radio: MCQ / Numerical / Fill-in / Match |
| Subject | Dropdown |
| Class/Grade | Dropdown |
| Chapter | Dropdown (loaded by subject) |
| Difficulty | Radio: Easy / Medium / Hard |
| Language | Dropdown |
| Question text | Rich textarea (markdown + LaTeX) |
| Options (MCQ) | 4 text inputs (A–D) |
| Correct answer (MCQ) | Radio A/B/C/D |
| Answer (Numerical) | Decimal input + tolerance |
| Explanation | Textarea (optional) |
| Tags | Tag input |

**Preview panel:** live preview of rendered question (right side of modal)
**Footer:** [Cancel] [Save as Draft] [Publish]

---

### 6.2 Bulk Import Modal (480 px)

**Formats:** CSV template / Excel template / JSON
**[Download Template]** button
**Upload zone:** drag-and-drop `border-dashed border-2 border-[#1E2D4A]`
**Validation:** pre-import validation shows: total questions / validation errors / warnings
**Footer:** [Cancel] [Start Import]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/qbank_kpi.html` | Page load |
| `?part=question_table` | `exec/partials/qbank_table.html` | Load · search · filter · page |
| `?part=flagged_questions` | `exec/partials/qbank_flagged.html` | Tab click |
| `?part=question_sets` | `exec/partials/question_sets.html` | Tab click |
| `?part=question_drawer&id={id}` | `exec/partials/question_drawer.html` | Row click |

**Django view dispatch:**
```python
class QuestionBankView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.manage_question_bank"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/qbank_kpi.html",
                "question_table": "exec/partials/qbank_table.html",
                "flagged_questions": "exec/partials/qbank_flagged.html",
                "question_sets": "exec/partials/question_sets.html",
                "question_drawer": "exec/partials/question_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/question_bank.html", ctx)
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 300 ms | > 800 ms |
| Question table (25 rows) | < 600 ms | > 1.5 s |
| Full-text search | < 800 ms | > 2 s |
| Question drawer | < 300 ms | > 800 ms |
| Bulk import (1,000 questions) | < 30 s | > 2 min |
| Full page initial load | < 1.2 s | > 3 s |

**Full-text search note:** Use PostgreSQL `tsvector` GIN index or Elasticsearch. Avoid `LIKE '%...%'` on 2M rows.

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| 0 results for search | "No questions match" + [Clear search] |
| LaTeX rendering failure | Show raw LaTeX text + warning "Math rendering unavailable" |
| Bulk import with errors | Show import log: N imported / M failed + downloadable error report |
| Duplicate question detected (on add) | Warning "A similar question exists: Q-XXXXXX. View →" |
| Archive question used in active exam | Error "Cannot archive — used in {N} active exams" |
| Flag already flagged question | "Already flagged. Update reason?" |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `N` | Add question |
| `F` | Focus search |
| `↑` / `↓` | Navigate rows |
| `Enter` | Open question drawer |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/question_bank.html` | Full page shell |
| `exec/partials/qbank_kpi.html` | KPI strip |
| `exec/partials/qbank_table.html` | Question table + pagination |
| `exec/partials/qbank_flagged.html` | Flagged questions tab |
| `exec/partials/question_sets.html` | Question sets tab |
| `exec/partials/question_drawer.html` | Question detail drawer |
| `exec/partials/add_question_modal.html` | Add question modal |
| `exec/partials/bulk_import_modal.html` | Bulk import modal |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `SearchInput` | §4.2 |
| `MultiSelectDropdown` | §4.2 filters |
| `QuestionTable` | §4.4 |
| `DifficultyBadge` | §4.4 |
| `FlaggedTable` | §4.5 |
| `QuestionSetsTable` | §4.6 |
| `DrawerPanel` | §5.1 |
| `LaTeXRenderer` | §5.1 Tab A |
| `RichTextEditor` | §5.1 Edit mode |
| `QuestionAnalyticsChart` | §5.1 Tab B |
| `VersionHistory` | §5.1 Tab C |
| `ModalDialog` | §6.1–6.2 |
| `BulkUploadZone` | §6.2 |
| `PaginationStrip` | §4.4 |
