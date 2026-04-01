# B-04 — Question Paper Bank (Department)

> **URL:** `/school/academic/dept/<dept>/question-bank/`
> **File:** `b-04-question-paper-bank.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HOD (S4) — full own dept · Exam Cell Head (S4) — full all depts · Academic Coordinator (S4) — read · Subject Teacher (S3) — submit own subject · Class Teacher (S3) — submit · Principal (S6) — full

---

## 1. Purpose

The department's question repository — a structured bank of individual questions tagged by subject, class level, topic, difficulty, type, and marks. When an exam is scheduled, the Exam Cell Head (or HOD) assembles a question paper by selecting questions from this bank rather than starting from scratch each time. Over time the bank grows into an asset: hundreds of questions across topics, difficulty levels, and types (MCQ, short answer, long answer, case-based, assertion-reason). This is especially valuable for CBSE schools where question type norms are prescribed per paper.

**Indian context:** CBSE question paper formats are well-defined — for example, Class X Science: Section A (MCQ 1m each, 20 questions), Section B (Short Answer 2m, 5 questions), Section C (Short Answer 3m, 8 questions), Section D (Long Answer 5m, 3 questions), Section E (Case-based 4m, 3 questions). The question bank must be structured to support assembling papers in these exact formats.

---

## 2. Page Layout

### 2.1 Header
```
Question Paper Bank — Science Department        [+ Add Question]  [+ Bulk Import]  [Generate Paper]
Total Questions: 1,847  ·  Subjects: 6  ·  Classes: VI–XII
Search: [_______________________]  🔍
```

### 2.2 Filter Bar
```
Subject [All ▼]  Class [All ▼]  Topic [All ▼]  Type [All ▼]  Difficulty [All ▼]  Marks [All ▼]  Status [Active ▼]
```

---

## 3. Question Bank Table

| # | Question (preview) | Subject | Class | Topic | Type | Marks | Difficulty | Used Count | Status | Actions |
|---|---|---|---|---|---|---|---|---|---|---|
| Q-1204 | "A convex lens of focal length 15cm..." | Physics | XII | Ray Optics | Long Answer | 5 | Medium | 3 | ✅ Active | [View] [Edit] [Use] |
| Q-1187 | "Which of the following is NOT a property of alpha particles?" | Physics | XII | Nuclei | MCQ | 1 | Easy | 7 | ✅ Active | [View] [Edit] [Use] |
| Q-1142 | "State Huygens' principle. Using it derive the laws of refraction." | Physics | XII | Wave Optics | Long Answer | 5 | Hard | 2 | ✅ Active | [View] [Edit] [Use] |
| Q-0892 | "Explain the significance of zero error in vernier calipers." | Physics | XI | Measurement | Short Answer | 3 | Medium | 5 | ✅ Active | [View] [Edit] [Use] |

**Used Count** — how many times this question has appeared in school exams. Questions used 3+ times in recent years should be rotated out.

---

## 4. Add / Edit Question Drawer (680px)

Triggered by [+ Add Question] or [Edit] on any row:

### Section A — Question Identity

| Field | Type | Notes |
|---|---|---|
| Subject | Dropdown | Department's subjects only |
| Class Level | Dropdown | LKG–XII; multi-select for questions applicable to multiple levels |
| Topic / Chapter | Dropdown | From B-22 Topic Master; chapter + section |
| Sub-topic | Text | Optional — more specific tag within chapter |
| Question Type | Dropdown | MCQ · Assertion-Reason · Short Answer (SA1/SA2) · Long Answer (LA) · Case-Based (CB) · Practical-Based · Fill in the blank · Match the column · Diagram-based |
| Marks | Dropdown | 1, 2, 3, 4, 5, 6, 8, 10 |
| Difficulty | Dropdown | Easy · Medium · Hard |
| Bloom's Level | Dropdown | Remember · Understand · Apply · Analyse · Evaluate · Create |
| Source | Dropdown | Original · NCERT Exercise · NCERT Exemplar · Previous Board Paper · Reference Book · Teacher Created |
| Board Year (if from board paper) | Year picker | — |

### Section B — Question Content

```
Question Text:
┌─────────────────────────────────────────────────────────────────────┐
│  [Bold] [Italic] [Subscript] [Superscript] [Insert Image] [LaTeX]   │
│─────────────────────────────────────────────────────────────────────│
│  A convex lens of focal length 15 cm is placed 30 cm from           │
│  a luminous object. Find the position and nature of the image.       │
└─────────────────────────────────────────────────────────────────────┘

[+ Insert Diagram / Image]  [+ Insert LaTeX Formula]
```

*LaTeX support is critical for Physics and Mathematics — formulae like `\frac{1}{v} - \frac{1}{u} = \frac{1}{f}` must render correctly in paper.*

### Section C — Answer & Solution (for MCQ)

| Field | Notes |
|---|---|
| Option A | Text + formula/image support |
| Option B | — |
| Option C | — |
| Option D | — |
| Correct Answer | Radio: A / B / C / D |
| Solution | Explanation of why the answer is correct (shown to teachers, not students) |

### Section C — Answer & Solution (for Short/Long Answer)

```
Model Answer:
┌────────────────────────────────────────────────────────────┐
│  v = 30 cm, real and inverted image.                        │
│  Using lens formula: 1/v - 1/u = 1/f                       │
│  1/v - 1/(-30) = 1/15                                      │
│  1/v = 1/15 - 1/30 = 1/30                                  │
│  v = 30 cm (positive → real, inverted, same size)          │
└────────────────────────────────────────────────────────────┘

Marking Scheme:
  Step 1 (write formula):     1 mark
  Step 2 (substitute values): 1 mark
  Step 3 (solve):             2 marks
  Step 4 (state nature):      1 mark
```

### Section D — Metadata & Flags

| Field | Value |
|---|---|
| Confidential | Yes / No (Yes = excluded from student revision sets) |
| Repeat Protection | Block this question if used in last N exams: [2 ▼] years |
| CBSE Section Tag | Section A / B / C / D / E (for paper assembly) |
| Contributed by | Auto-filled: logged-in teacher |
| HOD Approval | Required for questions marked "Hard" or LA type |

---

## 5. Bulk Import

[+ Bulk Import] → Upload CSV/Excel with columns:
`subject, class, topic, type, marks, difficulty, question_text, option_a, option_b, option_c, option_d, correct_answer, model_answer, bloom_level`

- Preview table shown before import; validation errors highlighted
- Row-by-row accept/reject before final import
- Images referenced by filename; separate ZIP upload for images

---

## 6. Generate Paper (Paper Assembly Wizard)

[Generate Paper] → triggers a paper assembly drawer (720px) with 3 steps:

### Step 1 — Paper Parameters
| Field | Value |
|---|---|
| Exam | Select from scheduled exams (B-10) or "Create Draft Paper" |
| Subject | Dropdown |
| Class | Dropdown |
| Total Marks | Number (e.g., 80) |
| Duration | Minutes (e.g., 180) |
| Board Format | CBSE Standard / Custom |

### Step 2 — Section Builder

If CBSE Standard: sections auto-populated from CBSE format norms:

| Section | Type | Questions | Marks Each | Total |
|---|---|---|---|---|
| A | MCQ | 20 | 1 | 20 |
| B | Short Answer (SA1) | 5 | 2 | 10 |
| C | Short Answer (SA2) | 8 | 3 | 24 |
| D | Long Answer | 3 | 5 | 15 |
| E | Case-Based | 3 | 4+1 | 11 |

If Custom: user adds sections, defines type/count/marks per section.

### Step 3 — Question Selection

For each section, system suggests questions from the bank (matching type, difficulty balance, topic coverage):
- **Auto-suggest**: system selects optimally balanced set; teacher can swap individual questions
- **Manual**: browse and select from filtered list
- Topics covered: auto-checklist shows which chapters are covered, ensuring balanced coverage

**Difficulty distribution target** (CBSE norm): Easy 30% · Medium 50% · Hard 20%.

**Repeat Protection**: auto-filters out questions used in last 2 years for this class.

[Preview Paper →] → shows assembled paper as it would appear for printing.
[Save Draft] → saves draft QP to B-32 (Question Paper Workflow) for HOD review.

---

## 7. Question Analytics

Section showing usage data:
- Most used questions (risk of over-repetition)
- Least used (valid questions never used — rotation opportunity)
- Questions by Bloom's level distribution (check if bank is skewed toward Remember/Understand)
- Topic coverage gaps (topics with fewer than 5 questions in the bank)
- Year-wise paper difficulty trend

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/question-bank/?dept={dept}&subject={s}&class={c}&type={t}&difficulty={d}` | Filtered question list |
| 2 | `POST` | `/api/v1/school/{id}/question-bank/` | Add single question |
| 3 | `GET` | `/api/v1/school/{id}/question-bank/{q_id}/` | Question detail |
| 4 | `PATCH` | `/api/v1/school/{id}/question-bank/{q_id}/` | Edit question |
| 5 | `DELETE` | `/api/v1/school/{id}/question-bank/{q_id}/` | Soft-delete (archive) |
| 6 | `POST` | `/api/v1/school/{id}/question-bank/bulk-import/` | Bulk CSV import |
| 7 | `POST` | `/api/v1/school/{id}/question-bank/generate-paper/` | Paper assembly (returns draft QP) |
| 8 | `GET` | `/api/v1/school/{id}/question-bank/analytics/?dept={dept}` | Usage analytics |

---

## 9. Business Rules

- Questions cannot be permanently deleted; only archived (audit trail requirement)
- HOD must approve "Hard" difficulty long-answer questions before they enter the Active bank
- Questions marked "Confidential: Yes" are excluded from any student-facing study material export
- Repeat protection: if a question was used in the same exam type (e.g., Unit Test 1) within the last 2 academic years, it is flagged in the paper assembly step
- Images embedded in questions are stored in Cloudflare R2; questions with broken image references are flagged
- LaTeX formulae are rendered at paper-generation time using a server-side LaTeX-to-SVG renderer; output is embedded in the PDF
- Questions contributed by a teacher are visible to the HOD and Exam Cell immediately; Principal can view all
- Bulk import limits: max 500 questions per import; large imports queued as background tasks

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
