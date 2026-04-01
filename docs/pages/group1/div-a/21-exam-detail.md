# div-a-21 — Exam Detail

## 1. Platform Scale Reference

Single-exam context:

| Dimension | Value |
|---|---|
| Max students per exam | 15,000 (coaching centre) |
| Questions per exam | 10–200 |
| Proctoring events per student | ~50–200 (snapshots, tab switches, etc.) |
| Results processing time | < 5 min post-submission |
| Result re-checking window | 72 hours post-publication |
| Answer key versions | 1–3 (preliminary + revised) |

**Why this matters:** Exam Detail is the authoritative record for a single exam. It shows who attempted, their scores, proctoring flags, answer key, question-wise analysis, and any disputes. Institution admins need it for result re-checking; the COO needs it when coaching centres escalate score disputes.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Exam: {Exam Name} |
| Route | `/exec/exams/<exam_id>/` |
| Django view | `ExamDetailView` |
| Template | `exec/exam_detail.html` |
| Priority | P1 |
| Nav group | Exams |
| Required role | `exec`, `superadmin`, `ops` |
| 2FA required | Publishing results / Answer key revision |
| HTMX poll | Live exams: every 15s · Completed: none |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ← Exam Catalog  JEE Mock Test 12 — Physics   [Mock] [● Completed]          │
│                 ABC Coaching Centre · Class 12 · 23 Mar 2025, 14:30–16:30  │
│            [Publish Results] [Revise Answer Key] [Download Report] [Cancel] │
├────────────┬──────────┬──────────┬──────────┬──────────────────────────────  ┤
│ Registered │ Appeared │ Avg Score│ Top Score│  Pass Rate                    │
│  1,000     │   842    │  67.4%   │  98.2%   │  78.4%                        │
├────────────┴──────────┴──────────┴──────────┴──────────────────────────────  ┤
│ TABS: [Overview] [Students] [Results] [Questions] [Proctoring] [Timeline]   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Page Header

### 4.1 Breadcrumb + Identity

`← Exam Catalog` · `text-[#6366F1]`

**Exam identity:**
```
JEE Mock Test 12 — Physics         [Mock badge]  [● Completed badge]
ABC Coaching Centre · Class 12 · Exam ID: EXM-00842
23 Mar 2025, 14:30–16:30 IST · Duration: 120 min · 100 questions · 400 marks
```

**Action buttons:**
- [Publish Results] (if not yet published) · 2FA required
- [Revise Answer Key] · 2FA required
- [Download Report] → PDF/CSV
- [Cancel Exam] (if scheduled/live) · 2FA required

---

### 4.2 KPI Strip

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Registered | Total enrolled students | — |
| 2 | Appeared | Submitted at least 1 answer | — |
| 3 | Avg Score | % of max marks | < 40% = amber |
| 4 | Top Score | Highest score | — |
| 5 | Pass Rate | % scoring ≥ pass mark | < 50% = amber |

**For live exams:** poll every 15s · Appeared count updates live · Registered = total enrolled

---

## 5. Tab: Overview

`id="tab-overview"` · `hx-get="?part=overview&exam_id={id}"`

**2-column grid:**

**Left — Exam Metadata:**
`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-6`
| Field | Value |
|---|---|
| Exam type | Mock |
| Subject(s) | Physics |
| Class/Grade | Class 12 |
| Total questions | 100 |
| Total marks | 400 |
| Marking scheme | +4 / -1 |
| Pass mark | 50% (200 marks) |
| Proctoring | Enabled (webcam + screen) |
| Shuffle questions | Yes |
| Shuffle options | Yes |
| Instructions | Expandable text |

**Right — Score Distribution:**
Histogram (10 bins, 0–400 marks) · Canvas height 200px
- X-axis: marks range
- Y-axis: student count
- Annotations: avg line (dashed `#6366F1`) + pass mark (dashed `#34D399`)

---

## 6. Tab: Students

`id="tab-students"` · `hx-get="?part=students&exam_id={id}"`

**Toolbar:** Search by name/roll · Status filter · Sort dropdown

**Students Table:**
| Column | Width | Detail |
|---|---|---|
| Rank | 60px | #1, #2... (shown after publish) |
| Student | 180px | Name (anonymised if privacy mode) |
| Roll No | 80px | `font-mono` |
| Status | 100px | Appeared / Absent / Disconnected / Flagged |
| Marks | 100px | Raw score / Max marks |
| Score % | 80px | Percentage + coloured bar |
| Correct | 70px | Count |
| Wrong | 70px | Count |
| Unattempted | 80px | Count |
| Time taken | 80px | Minutes |
| Violations | 80px | Proctoring flag count (amber if > 0) |
| Actions ⋯ | 48px | View Answers / View Proctoring / Re-check / Disqualify |

**Pagination:** 50/page

---

## 7. Tab: Results

`id="tab-results"` · `hx-get="?part=results&exam_id={id}"`

### 7.1 Summary Statistics

Grid of stat cards:
- Mean: 67.4% · Median: 70.2% · Std Dev: 15.3 · P90: 88% · P10: 42%
- Pass count: 660 (78.4%) · Fail count: 182 (21.6%)
- Topper: (shown after publish)
- Lowest scorer: (shown after publish)

### 7.2 Percentile Chart (cumulative distribution)

**Chart:** Line chart · X = score % · Y = cumulative % of students
- Score at P50 highlighted with vertical dashed line
- Hover: "At {score}%, student is in the {P}th percentile"

### 7.3 Subject/Section-wise Performance Table

| Section | Questions | Max Marks | Avg Marks | Avg % | Difficulty |
|---|---|---|---|---|---|
| Mechanics | 25 | 100 | 68.4 | 68.4% | Medium |
| Electrostatics | 25 | 100 | 54.2 | 54.2% | Hard |
| Optics | 25 | 100 | 72.1 | 72.1% | Easy |
| Modern Physics | 25 | 100 | 74.7 | 74.7% | Easy |

---

## 8. Tab: Questions

`id="tab-questions"` · `hx-get="?part=questions&exam_id={id}"`

### 8.1 Question Analysis Table

| Column | Detail |
|---|---|
| Q # | Question number |
| Question | Truncated text (expand on hover) |
| Type | MCQ / Numerical / Match |
| Correct Answer | Answer key (masked until published) |
| Correct % | % of students who answered correctly |
| Wrong % | % who answered incorrectly |
| Unattempted % | % who skipped |
| Difficulty | Easy (> 70% correct) / Medium / Hard (< 40% correct) |
| Discriminating Index | Statistical quality metric (0–1) |
| Actions ⋯ | View detail / Flag for revision / Exclude from scoring |

**Click row:** opens Question Detail Drawer (480px) showing full question text + options + answer distribution bar chart

### 8.2 Answer Key Panel

Shown after publish (or for ops/exec always):
Answer key as grid: Q1=A, Q2=C, Q3=3.14, ...
[Revise Answer Key] button opens revision modal

---

## 9. Tab: Proctoring

`id="tab-proctoring"` · `hx-get="?part=proctoring&exam_id={id}"`

### 9.1 Summary

| Metric | Count |
|---|---|
| Total students proctored | 842 |
| Students with violations | 45 (5.3%) |
| Total violation events | 312 |
| Auto-flagged for review | 12 |
| Disqualified | 2 |

Violation type breakdown (bar chart):
- Tab switch: 180
- Multiple faces: 42
- No face: 38
- Phone detected: 28
- Screen share: 24

### 9.2 Flagged Students Table

| Column | Detail |
|---|---|
| Student | Name |
| Violations | Count by type |
| Risk Level | High / Medium / Low (auto-classified) |
| Status | Pending Review / Cleared / Disqualified |
| Actions ⋯ | View Proctoring / Clear / Disqualify |

---

## 10. Tab: Timeline

`id="tab-timeline"` · `hx-get="?part=exam_timeline&exam_id={id}"`

**Event timeline (vertical):**
```
14:30:00  Exam started — 842 students connected
14:45:22  [Warning] 12 students disconnected (network issue)
14:50:00  Reconnection window opened
14:52:10  8 of 12 students reconnected
15:45:00  First submission received
16:28:54  Last submission received
16:30:00  Exam ended — 842 of 1000 appeared
16:32:00  Auto-grading started
16:36:22  Grading complete — results ready for review
16:40:00  Results published by admin@abc.com
```

For live exams: live updates via poll every 15s

---

## 11. Modals

### 11.1 Revise Answer Key Modal (560 px)

**2FA required.**

**Reason:** required text
**Key revision grid:** editable answer per question
**Impact preview:** "Revising Q12 answer from A to B will change scores for {N} students. Average score will increase by {X}%."
**Footer:** [Cancel] [Apply Revision]

---

### 11.2 Publish Results Modal (480 px)

**2FA required.**

"Publish results for {N} students?"
- Notify students via email: Checkbox
- Notify institution admin: Checkbox (default: checked)
- Include rank: Checkbox (default: off)

**Footer:** [Cancel] [Publish Results]

---

### 11.3 Disqualify Student Modal (480 px)

| Field | Type |
|---|---|
| Student | Read-only |
| Reason | Select: Cheating / Proctoring violation / Identity fraud / Other |
| Evidence | Textarea |
| Notes | Textarea |
| Notify student | Checkbox |

**Footer:** [Cancel] [Disqualify]

---

## 12. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/exam_detail_kpi.html` | Page load · poll 15s (live) |
| `?part=overview` | `exec/partials/exam_overview.html` | Tab click |
| `?part=students` | `exec/partials/exam_students.html` | Tab · filter · page |
| `?part=results` | `exec/partials/exam_results.html` | Tab click |
| `?part=questions` | `exec/partials/exam_questions.html` | Tab click |
| `?part=proctoring` | `exec/partials/exam_proctoring.html` | Tab click |
| `?part=exam_timeline` | `exec/partials/exam_timeline.html` | Tab · poll 15s (live) |

**Django view dispatch:**
```python
class ExamDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_exams"

    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, pk=exam_id)
        ctx = self._build_context(request, exam)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/exam_detail_kpi.html",
                "overview": "exec/partials/exam_overview.html",
                "students": "exec/partials/exam_students.html",
                "results": "exec/partials/exam_results.html",
                "questions": "exec/partials/exam_questions.html",
                "proctoring": "exec/partials/exam_proctoring.html",
                "exam_timeline": "exec/partials/exam_timeline.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/exam_detail.html", ctx)
```

---

## 13. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 200 ms | > 500 ms |
| Overview tab | < 400 ms | > 1 s |
| Students table (50 rows) | < 400 ms | > 1 s |
| Questions table (100 rows) | < 500 ms | > 1.2 s |
| Live timeline poll | < 200 ms | > 500 ms |
| Full page initial load | < 1 s | > 2.5 s |

---

## 14. States & Edge Cases

| State | Behaviour |
|---|---|
| Live exam | KPI strip + timeline poll every 15s |
| Exam not yet started | Students tab shows "Exam not started yet" |
| Results not published | Results/Questions/Students tabs show scores only to exec/ops |
| Answer key revised | Banner "Answer key revised on {date} — scores updated" |
| Student re-check request | Appears in Students tab Actions as "Re-check pending" badge |
| 0 appeared | "No students appeared for this exam" empty state across all tabs |

---

## 15. Template Files

| File | Purpose |
|---|---|
| `exec/exam_detail.html` | Full page shell |
| `exec/partials/exam_detail_kpi.html` | KPI strip |
| `exec/partials/exam_overview.html` | Overview tab |
| `exec/partials/exam_students.html` | Students table |
| `exec/partials/exam_results.html` | Results + stats |
| `exec/partials/exam_questions.html` | Question analysis |
| `exec/partials/exam_proctoring.html` | Proctoring summary |
| `exec/partials/exam_timeline.html` | Timeline events |
| `exec/partials/revise_answer_key_modal.html` | Answer key revision |
| `exec/partials/publish_results_modal.html` | Publish modal |
| `exec/partials/disqualify_modal.html` | Disqualify modal |

---

## 16. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.2 |
| `TabBar` | §5–10 |
| `ScoreHistogram` | §5 |
| `StudentsTable` | §6 |
| `PercentileChart` | §7.2 |
| `SectionPerformanceTable` | §7.3 |
| `QuestionAnalysisTable` | §8.1 |
| `AnswerKeyGrid` | §8.2 |
| `ViolationSummary` | §9.1 |
| `FlaggedStudentsTable` | §9.2 |
| `EventTimeline` | §10 |
| `ModalDialog` | §11.1–11.3 |
| `PaginationStrip` | Students + Questions tables |
