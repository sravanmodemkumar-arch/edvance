# Module 17 — Question Bank & MCQ

## Purpose
Provide a three-tier, platform-native question bank for EduForge covering all institution
types, boards, competitive exams, and vocational curricula. Every question is stored as a
unified JSON document that supports dynamic rendering of all content types — text, LaTeX
math, charts, tables, diagrams, images, code, chemical equations, audio — in any language.
No file uploads. No downloads. YouTube/video links open in-app WebView via "Watch Video"
button on every question.

---

## 1. Content Hierarchy & Source Tiers

### 1.1 Three-Tier Question Bank

| Tier | Source | Scope | Editable By |
|---|---|---|---|
| Platform | EduForge SME content team | All institutions on platform | Platform team only |
| Institution | HOD-approved teacher questions | All teachers of same subject/grade | HOD + Admin |
| Teacher | Individual teacher-created | Own section / batch only | Author teacher |

### 1.2 Six-Level Hierarchy Linkage
Every question linked to a precise location:
```
Level 1 → Board / Framework
Level 2 → Subject
Level 3 → Grade / Semester / Year
Level 4 → Unit
Level 5 → Chapter
Level 6 → Topic (and Sub-topic — Level 6b)
```
Question count visible at every node. Browse drill-down:
Board → Subject → Grade → Unit → Chapter → Topic → Sub-topic → Questions

### 1.3 Platform Question Bank Coverage

**School Boards:**
- CBSE Classes 6–12: all subjects, all chapters, all topics, all question types
- CBSE Classes 1–5: FLN activity questions, EVS, Maths, English, Hindi
- 28 State Boards: chapter-wise questions aligned to state textbooks (Hindi + Regional medium)
- ICSE/ISC Classes 9–12: all subjects
- IB DP / IGCSE: all core subjects
- NIOS: all subjects, self-study pattern

**Competitive Exams:**
- JEE Main: last 10 years all shifts, all question types
- JEE Advanced: last 10 years both papers
- NEET UG: last 10 years
- UPSC CSE Prelims: last 10 years GS1 + CSAT
- SSC CGL/CHSL: last 5 years
- IBPS PO/Clerk/SO, SBI PO/Clerk, RRB: last 5 years
- All State PSC Prelims: 28 states, last 3 years
- CTET/TET: all states, last 5 years
- GATE: all 29 papers, last 5 years
- CA Foundation/Inter/Final: last 5 attempts (May/Nov)
- CLAT/CUET: last 5 years

**Vocational / ITI:**
- NCVT theory questions: all 150+ trades, unit-wise
- PMKVY module-wise assessment questions

### 1.4 Platform Question Update Policy
- New PYQs added after each exam season (within 30 days of paper release)
- Syllabus change → question review within 7 working days
- Monthly: current affairs questions (Banking/SSC/UPSC)
- Finance Act / GST update → CA/CS questions updated within 14 days
- Each platform question carries `platform_version` and `last_updated_date`

---

## 2. Unified Question JSON Schema

Every question — regardless of type, board, subject, or language — is stored as a
single unified JSON document. The frontend renderer reads the JSON and dynamically
renders all content blocks, question types, and language variants.

### 2.1 Top-Level Structure

```json
{
  "question_id": "uuid-v4",
  "version": 1,
  "type": "MCQ_SINGLE",
  "metadata": { ... },
  "content": {
    "stem": [ ...content_blocks ],
    "stem_translations": {
      "hi": [ ...content_blocks ],
      "ta": [ ...content_blocks ],
      "te": [ ...content_blocks ]
    },
    "passage_id": null,
    "options": [ ...option_objects ],
    "answer": { ... },
    "solution": [ ...content_blocks ],
    "solution_translations": { "hi": [ ...content_blocks ] },
    "hints": [ ...hint_objects ],
    "video_links": [ ...video_link_objects ],
    "image_refs": [ ...image_ref_objects ]
  }
}
```

### 2.2 Metadata Object

```json
{
  "metadata": {
    "source_tier":          "PLATFORM | INSTITUTION | TEACHER",
    "tenant_id":            "uuid | null",
    "branch_id":            "uuid | null",
    "author_id":            "uuid | null",
    "board_code":           "CBSE",
    "subject_code":         "PHYSICS",
    "grade":                "12",
    "unit_id":              "uuid",
    "chapter_id":           "uuid",
    "topic_id":             "uuid",
    "subtopic_id":          "uuid | null",
    "bloom_level":          "REMEMBER | UNDERSTAND | APPLY | ANALYSE | EVALUATE | CREATE",
    "difficulty":           "EASY | MEDIUM | HARD | VERY_HARD",
    "difficulty_index":     null,
    "discrimination_index": null,
    "marks":                4,
    "negative_marks":       -1,
    "partial_marks":        false,
    "estimated_seconds":    120,
    "exam_tags":            ["JEE_MAIN", "CBSE_BOARD"],
    "is_pyq":               true,
    "pyq_year":             2023,
    "pyq_exam":             "JEE_MAIN",
    "pyq_paper":            "January Shift 1",
    "pyq_question_no":      14,
    "primary_language":     "en",
    "available_languages":  ["en", "hi", "ta"],
    "is_bilingual":         true,
    "co_tags":              ["CO2"],
    "nos_code":             null,
    "nipun_code":           null,
    "is_cwsn_variant":      false,
    "parent_question_id":   null,
    "is_hots":              true,
    "is_formative":         false,
    "is_olympiad":          false,
    "olympiad_tags":        [],
    "is_value_based":       false,
    "collection_ids":       ["uuid"],
    "pool_id":              "uuid | null",
    "pool_slot":            "Q3_HARD",
    "retired":              false,
    "retire_reason":        null,
    "copyright_type":       "PYQ | PLATFORM | INSTITUTION | TEACHER",
    "platform_version":     "2024-04-v1",
    "last_updated":         "2024-04-01",
    "created_at":           "2024-01-15T10:00:00Z",
    "updated_at":           "2024-01-15T10:00:00Z"
  }
}
```

### 2.3 Content Block Types

Every field that carries displayable content (stem, options, solution, hints) is an
**array of content blocks**. The renderer processes each block in sequence.

#### 2.3.1 Text Block
```json
{
  "type": "TEXT",
  "text": "The electric field due to a point charge is:",
  "style": "NORMAL | BOLD | ITALIC | HEADING | SMALL | WARNING"
}
```

#### 2.3.2 LaTeX Math Block
```json
{
  "type": "LATEX",
  "latex": "E = \\frac{1}{4\\pi\\varepsilon_0} \\cdot \\frac{q}{r^2}",
  "display": "INLINE | BLOCK"
}
```
- `INLINE`: rendered within a line of text
- `BLOCK`: centred on its own line (derivation steps, main formulas)
- Supports: fractions, integrals, summations, matrices, Greek letters, vectors,
  set notation, calculus operators, chemical equations (mhchem package)

#### 2.3.3 Table Block
```json
{
  "type": "TABLE",
  "caption": "Comparison of plant and animal cells",
  "headers": ["Feature", "Plant Cell", "Animal Cell"],
  "rows": [
    ["Cell wall",    "Present",  "Absent"],
    ["Chloroplast",  "Present",  "Absent"],
    ["Vacuole",      "Large central", "Small or absent"]
  ],
  "header_row": true,
  "header_col": false,
  "alignment": ["LEFT", "CENTER", "CENTER"]
}
```

#### 2.3.4 Chart Block
```json
{
  "type": "CHART",
  "chart_type": "BAR | LINE | PIE | SCATTER | HISTOGRAM | AREA | BOX_PLOT",
  "title": "Population growth 2000-2020",
  "x_label": "Year",
  "y_label": "Population (in crores)",
  "x_values": [2000, 2005, 2010, 2015, 2020],
  "series": [
    {
      "label": "Urban",
      "values": [28.5, 30.1, 33.2, 37.8, 42.3],
      "colour": "#4A90D9"
    },
    {
      "label": "Rural",
      "values": [71.5, 69.9, 66.8, 62.2, 57.7],
      "colour": "#7ED321"
    }
  ],
  "legend": true,
  "grid": true
}
```
Chart types supported:
- Bar (grouped/stacked), Line, Pie/Donut, Scatter, Histogram, Area, Box Plot
- Used for: Data Interpretation sets, Economics (demand/supply), Geography (climate),
  Science (experimental results), Statistics problems

#### 2.3.5 Diagram Block (In-Platform Canvas)
```json
{
  "type": "DIAGRAM",
  "canvas_data": {
    "width": 600,
    "height": 400,
    "elements": [
      {
        "id": "e1",
        "shape": "ELLIPSE",
        "x": 250, "y": 180, "w": 120, "h": 80,
        "fill": "#E8F4F8",
        "stroke": "#2C3E50"
      },
      {
        "id": "l1",
        "type": "LABEL",
        "text": "Nucleus",
        "target_id": "e1",
        "x": 250, "y": 220,
        "leader_line": true
      }
    ]
  },
  "alt_text": "Diagram of an animal cell with nucleus, mitochondria, and cell membrane labelled",
  "caption": "Fig. 1: Animal Cell Structure"
}
```

#### 2.3.6 Image Block (Platform Library Only)
```json
{
  "type": "IMAGE",
  "image_id": "platform-img-uuid",
  "category": "BIOLOGY | PHYSICS | CHEMISTRY | GEOGRAPHY | HISTORY | GENERAL",
  "alt_text": "Cross-section of a leaf showing stomata, guard cells, and mesophyll",
  "caption": "Fig. 2: Leaf Cross-Section (Source: NCERT Class 10 Science)"
}
```
- Images come from **EduForge Platform Standard Image Library** — pre-loaded by content team
- Categories: Biology specimens, Physics equipment/setups, Chemistry apparatus,
  Geography maps, Historical photos, Mathematical figures
- **No upload from user device — ever**
- Teachers select from searchable platform library

#### 2.3.7 Code Block
```json
{
  "type": "CODE",
  "language": "python | c | cpp | java | javascript | sql | html | css",
  "code": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)\n\nprint(factorial(5))",
  "line_numbers": true,
  "highlight_lines": [3, 4]
}
```

#### 2.3.8 Chemical Equation Block
```json
{
  "type": "CHEM_EQUATION",
  "equation_latex": "2H_2 + O_2 \\xrightarrow{\\Delta} 2H_2O",
  "conditions": "Heat",
  "equation_type": "COMBUSTION | SYNTHESIS | DECOMPOSITION | DISPLACEMENT | REDOX | ACID_BASE | IONIC"
}
```

#### 2.3.9 Match Columns Block
```json
{
  "type": "MATCH_COLUMNS",
  "column_a_header": "List I — Scientists",
  "column_b_header": "List II — Discoveries",
  "column_a": [
    {"id": "1", "content": [{"type": "TEXT", "text": "Faraday"}]},
    {"id": "2", "content": [{"type": "TEXT", "text": "Newton"}]},
    {"id": "3", "content": [{"type": "TEXT", "text": "Einstein"}]},
    {"id": "4", "content": [{"type": "TEXT", "text": "Bohr"}]}
  ],
  "column_b": [
    {"id": "A", "content": [{"type": "TEXT", "text": "Laws of Motion"}]},
    {"id": "B", "content": [{"type": "TEXT", "text": "Electromagnetic Induction"}]},
    {"id": "C", "content": [{"type": "TEXT", "text": "Atomic Model"}]},
    {"id": "D", "content": [{"type": "TEXT", "text": "Photoelectric Effect"}]},
    {"id": "E", "content": [{"type": "TEXT", "text": "Theory of Relativity"}]}
  ]
}
```

#### 2.3.10 Audio Block (FLN / Language Subjects)
```json
{
  "type": "AUDIO",
  "mode": "TTS | RECORDED",
  "tts_text": "एक पेड़ में कितने पत्ते होते हैं?",
  "tts_language": "hi",
  "play_label": "सुनें",
  "auto_play": false
}
```
- `TTS`: text-to-speech generated on the fly in the specified language
- `RECORDED`: platform-team-recorded audio clip (for exact pronunciation, music questions)
- Used for: Classes 1–3 FLN oral questions, Language listening comprehension,
  Music theory questions

#### 2.3.11 Sequence Block
```json
{
  "type": "SEQUENCE_ITEMS",
  "instruction": "Arrange the following steps of mitosis in correct order:",
  "items": [
    {"id": "A", "content": [{"type": "TEXT", "text": "Metaphase"}]},
    {"id": "B", "content": [{"type": "TEXT", "text": "Prophase"}]},
    {"id": "C", "content": [{"type": "TEXT", "text": "Anaphase"}]},
    {"id": "D", "content": [{"type": "TEXT", "text": "Telophase"}]}
  ]
}
```

### 2.4 Option Object

Each option in MCQ, True/False, Assertion-Reason uses option objects:
```json
{
  "id": "A",
  "content": [
    {"type": "TEXT",  "text": "The resistance increases with temperature because"},
    {"type": "LATEX", "latex": "R = \\rho \\frac{L}{A}", "display": "INLINE"}
  ],
  "content_translations": {
    "hi": [{"type": "TEXT", "text": "तापमान बढ़ने पर प्रतिरोध बढ़ता है क्योंकि"}],
    "ta": [{"type": "TEXT", "text": "வெப்பநிலை அதிகரிக்கும்போது மின்தடை அதிகரிக்கிறது"}]
  }
}
```

### 2.5 Answer Schema — Per Question Type

#### MCQ Single Correct
```json
{"type": "MCQ_SINGLE", "correct_option": "B"}
```

#### MCQ Multiple Correct (JEE Advanced)
```json
{
  "type": "MCQ_MULTIPLE",
  "correct_options": ["A", "C"],
  "partial_marks_scheme": {
    "all_correct": 4,
    "partial_3_of_3": 3,
    "partial_2_of_3": 2,
    "partial_1_of_3": 1,
    "wrong_option_included": -2
  }
}
```

#### True / False
```json
{
  "type": "TRUE_FALSE",
  "correct": true,
  "justification_required": true
}
```

#### Fill in the Blank
```json
{
  "type": "FILL_BLANK",
  "blanks": [
    {"id": 1, "answer": "Newton",   "case_sensitive": false, "tolerance": null},
    {"id": 2, "answer": "9.8",      "case_sensitive": false, "tolerance": {"abs": 0.1}},
    {"id": 3, "answer": "m/s²",     "case_sensitive": false, "tolerance": null}
  ]
}
```

#### Numerical (NEET/JEE pattern)
```json
{
  "type": "NUMERICAL",
  "value": 9.81,
  "tolerance_abs": 0.05,
  "tolerance_pct": null,
  "unit": "m/s²",
  "sig_figs": 3
}
```

#### Integer Type (JEE Advanced — 0 to 9)
```json
{"type": "INTEGER", "value": 3}
```

#### Decimal Type (JEE Main Numerical)
```json
{"type": "DECIMAL", "value": 3.14, "decimal_places": 2, "tolerance_abs": 0.01}
```

#### Match the Following
```json
{
  "type": "MATCH",
  "pairs": [
    {"a": "1", "b": "B"},
    {"a": "2", "b": "A"},
    {"a": "3", "b": "D"},
    {"a": "4", "b": "C"}
  ]
}
```

#### Matrix Match (JEE Advanced)
```json
{
  "type": "MATRIX_MATCH",
  "mappings": [
    {"row": "P", "cols": ["1", "3"]},
    {"row": "Q", "cols": ["2"]},
    {"row": "R", "cols": ["1", "2", "4"]},
    {"row": "S", "cols": ["4"]}
  ],
  "marks_per_row": 2,
  "negative_per_row": -1
}
```

#### Assertion–Reason
```json
{
  "type": "ASSERTION_REASON",
  "correct_option": "A",
  "options_schema": {
    "A": "Both A and R are true; R is the correct explanation of A",
    "B": "Both A and R are true; R is NOT the correct explanation of A",
    "C": "A is true but R is false",
    "D": "A is false but R is true",
    "E": "Both A and R are false"
  }
}
```

#### Sequence / Arrangement
```json
{"type": "SEQUENCE", "correct_order": ["B", "A", "C", "D"]}
```

#### Short / Long Answer (Text)
```json
{
  "type": "TEXT_ANSWER",
  "word_limit": 100,
  "model_answer": [
    {"type": "TEXT",  "text": "Newton's second law states that..."},
    {"type": "LATEX", "latex": "F = ma", "display": "BLOCK"}
  ],
  "rubric": [
    {"criterion": "Definition stated correctly",          "marks": 1},
    {"criterion": "Formula written with correct symbols", "marks": 1},
    {"criterion": "Units mentioned",                      "marks": 1}
  ]
}
```

#### Diagram Label
```json
{
  "type": "DIAGRAM_LABEL",
  "blank_labels": ["L1", "L2", "L3", "L4"],
  "correct_labels": {
    "L1": "Nucleus",
    "L2": "Mitochondria",
    "L3": "Cell Membrane",
    "L4": "Ribosome"
  },
  "options_per_label": ["Nucleus", "Golgi Body", "Mitochondria", "Cell Membrane",
                         "Ribosome", "Endoplasmic Reticulum"]
}
```

#### Data Interpretation Set
```json
{
  "type": "DI_SET",
  "set_id": "di-uuid",
  "question_ids": ["q-uuid-1", "q-uuid-2", "q-uuid-3", "q-uuid-4"],
  "intro_blocks": [ ...content_blocks_with_chart_or_table ]
}
```

### 2.6 Multilingual Support in JSON

Every text-bearing field supports language variants:

```json
{
  "stem": [
    {"type": "TEXT", "text": "Which of the following is a conductor?"}
  ],
  "stem_translations": {
    "hi": [{"type": "TEXT", "text": "निम्नलिखित में से कौन सा चालक है?"}],
    "ta": [{"type": "TEXT", "text": "பின்வருவனவற்றில் எது கடத்தி?"}],
    "te": [{"type": "TEXT", "text": "కింది వాటిలో ఏది వాహకం?"}],
    "mr": [{"type": "TEXT", "text": "खालीलपैकी कोणता वाहक आहे?"}],
    "gu": [{"type": "TEXT", "text": "નીચેનામાંથી કયો વાહક છે?"}],
    "bn": [{"type": "TEXT", "text": "নিচের কোনটি পরিবাহী?"}],
    "kn": [{"type": "TEXT", "text": "ಕೆಳಗಿನವುಗಳಲ್ಲಿ ಯಾವುದು ವಾಹಕ?"}],
    "ml": [{"type": "TEXT", "text": "താഴെ പറയുന്നവയിൽ ഏതാണ് ചാലകം?"}],
    "pa": [{"type": "TEXT", "text": "ਹੇਠਾਂ ਦਿੱਤਿਆਂ ਵਿੱਚੋਂ ਕਿਹੜਾ ਚਾਲਕ ਹੈ?"}],
    "or": [{"type": "TEXT", "text": "ନିମ୍ନଲିଖିତ ମଧ୍ୟରୁ କେଉଁଟି ପରିବାହକ?"}],
    "as": [{"type": "TEXT", "text": "তলত দিয়াসমূহৰ মাজত কোনটো পৰিবাহক?"}],
    "ur": [{"type": "TEXT", "text": "درج ذیل میں سے کون سا موصل ہے؟"}]
  }
}
```

Languages supported:
- `en` — English
- `hi` — Hindi (Devanagari)
- `ta` — Tamil
- `te` — Telugu
- `mr` — Marathi
- `gu` — Gujarati
- `bn` — Bengali
- `kn` — Kannada
- `ml` — Malayalam
- `pa` — Punjabi (Gurmukhi)
- `or` — Odia
- `as` — Assamese
- `ur` — Urdu (Nastaliq RTL)
- `sa` — Sanskrit (Devanagari)
- `ks` — Kashmiri
- `sd` — Sindhi
- `ne` — Nepali
- `ko` — Konkani
- `mai`— Maithili
- `doi`— Dogri
- `mni`— Manipuri (Meitei script)
- `sat`— Santali (Ol Chiki script)

Student selects preferred language from profile; question renders in that language
if translation available, else falls back to English.

### 2.7 Video Link Object

Every question can have one or more video buttons:
```json
{
  "video_links": [
    {
      "video_id":   "vl-uuid",
      "label":      "Watch: Concept Explanation — 6 min",
      "url":        "https://www.youtube.com/watch?v=XXXXXX",
      "url_type":   "YOUTUBE | PLATFORM_CDN",
      "language":   "en",
      "purpose":    "CONCEPT | SOLUTION_WALKTHROUGH | EXAM_TIP | LAB_DEMO | REVISION"
    },
    {
      "video_id":   "vl-uuid-2",
      "label":      "देखें: अवधारणा स्पष्टीकरण — 6 मिनट",
      "url":        "https://www.youtube.com/watch?v=YYYYYY",
      "url_type":   "YOUTUBE",
      "language":   "hi",
      "purpose":    "CONCEPT"
    }
  ]
}
```
- **"Watch Video" button rendered per link** — not an embed frame
- Tap → opens in in-app WebView; YouTube app never launched
- Multiple videos per question (different languages, different purposes)
- Video buttons visible in: practice mode, exam review (post-submission only — not during live exam)

### 2.8 Hint Object

Up to 3 progressive hints per question:
```json
{
  "hints": [
    {
      "level": 1,
      "label": "Hint 1",
      "content": [{"type": "TEXT", "text": "Think about which law relates force and acceleration."}]
    },
    {
      "level": 2,
      "label": "Hint 2",
      "content": [
        {"type": "TEXT", "text": "Newton's second law: "},
        {"type": "LATEX", "latex": "F = ma", "display": "INLINE"}
      ]
    },
    {
      "level": 3,
      "label": "Hint 3",
      "content": [{"type": "TEXT", "text": "Substitute F = 20 N, m = 5 kg and solve for a."}]
    }
  ]
}
```
Hints revealed one at a time by student; hint usage logged (affects practice analytics).

---

## 3. Question Types — Full Reference

| Code | Type | Answer Mode | Boards / Exams |
|---|---|---|---|
| MCQ_SINGLE | Single correct MCQ | Option select | CBSE / State / UPSC / NEET / JEE Main |
| MCQ_MULTIPLE | Multiple correct MCQ | Multi-select | JEE Advanced / GATE |
| TRUE_FALSE | True / False + justification | Toggle + text | CBSE internal / State boards |
| FILL_BLANK | Fill in the blank(s) | Text input | All boards |
| MATCH | Match the following | Pair mapping | CBSE / State / UPSC |
| ASSERTION_REASON | A+R four-option | Option select | CBSE Class 12 / NEET |
| SHORT_ANSWER | Short text answer | Text input | All boards |
| LONG_ANSWER | Long text answer + sub-parts | Text input | All boards |
| NUMERICAL | Numeric answer + tolerance | Number input | NEET / JEE Main |
| INTEGER | Integer 0–9 | Digit input | JEE Advanced |
| DECIMAL | Decimal answer | Decimal input | JEE Main Numerical |
| MATRIX_MATCH | Multi-row multi-col matching | Matrix input | JEE Advanced |
| PARAGRAPH | Passage + linked questions | Varies | CBSE / UPSC / CLAT |
| STATEMENT | Statement combo (correct/incorrect) | Option select | UPSC / NEET |
| SEQUENCE | Arrange in order | Drag/number order | UPSC / History / Biology |
| DI_SET | Data interpretation (chart/table) | Varies | Banking / SSC / UPSC |
| CASE_STUDY | Case paragraph + sub-questions | Varies | CBSE Class 10/12 (from 2021) |
| SOURCE_BASED | Primary source extract + questions | Varies | CBSE History / Political Science |
| CODE | Code snippet + question | Option/text | CS/IT papers / GATE |
| AUDIO | Audio (TTS/recorded) + question | Option/text | FLN Classes 1–3 / Language |
| DIAGRAM_LABEL | Blank diagram + label options | Dropdown select | Biology / Physics / Geography |
| CHEM_EQUATION | Partial equation completion | Text/option | Chemistry / NEET |
| HOTS | Higher Order Thinking (any type) | Varies | CBSE / Olympiad / JEE Advanced |

---

## 4. Question Metadata & Tagging

### 4.1 Bloom's Taxonomy Level
- REMEMBER / UNDERSTAND / APPLY / ANALYSE / EVALUATE / CREATE
- Auto-suggested by platform based on question type; teacher can override
- Distribution report per chapter shows Bloom's balance

### 4.2 Difficulty Levels
- EASY / MEDIUM / HARD / VERY_HARD
- Initially teacher-assigned at creation
- Auto-calibrated after 30+ student attempts using Difficulty Index (p-value)
- System shows: "Teacher-tagged: MEDIUM | System-calibrated: HARD (p=0.28)"

### 4.3 Marks & Negative Marking
- Marks: 0.5 / 1 / 2 / 3 / 4 / 5 / custom
- Negative marks: −0.25 / −0.33 / −0.5 / −1 / custom / 0 (no negative)
- Partial marks: configurable for MCQ_MULTIPLE and MATRIX_MATCH
- Estimated solving time: seconds (used in Module 18 paper builder time calculation)

### 4.4 Exam Relevance Tags
Multiple tags per question:
`CBSE_BOARD | ICSE_BOARD | STATE_BOARD | JEE_MAIN | JEE_ADVANCED | NEET_UG |
NEET_PG | UPSC_CSE | SSC_CGL | SSC_CHSL | IBPS_PO | IBPS_CLERK | SBI_PO |
RRB_NTPC | STATE_PSC | CLAT | CUET | NDA | CTET | TET | GATE | CA_FOUNDATION |
CA_INTER | CA_FINAL | CS_FOUNDATION | OLYMPIAD_NSO | OLYMPIAD_IMO | NTSE | KVPY`

### 4.5 PYQ Tagging
```json
{
  "is_pyq":         true,
  "pyq_year":       2023,
  "pyq_exam":       "JEE_MAIN",
  "pyq_paper":      "January Shift 1",
  "pyq_set":        "Set A",
  "pyq_question_no": 14,
  "pyq_marks":      4,
  "pyq_negative":   -1
}
```

### 4.6 Special Tags
- `is_hots`: true for Bloom's L4–L6 questions
- `is_formative`: true for CCE/periodic test questions
- `is_olympiad`: true for NSO/IMO/NTSE/KVPY
- `is_value_based`: CBSE value-based / life-skills questions
- `is_cwsn_variant`: simplified CWSN version of a standard question
- `is_bilingual`: question has translation in at least one regional language

---

## 5. Question Creation Interface

### 5.1 Creation Flow
1. Select: Board → Subject → Grade → Unit → Chapter → Topic → Sub-topic
2. Select question type → template pre-loaded
3. Fill question stem (rich text editor with all content block types)
4. Fill options / answer key / solution / hints
5. Add video links (paste YouTube URL → "Watch Video" button auto-generated)
6. Set metadata (marks, difficulty, Bloom's, exam tags, estimated time)
7. Add translations (optional — bilingual entry side by side)
8. Preview (see exact student rendering in all selected languages)
9. Save as Draft → Submit for HOD review / Publish to own section

### 5.2 Rich Text Editor — Full Content Support
- Text blocks with formatting
- LaTeX equations (inline + block) with live preview
- Chemical equations (mhchem LaTeX extension)
- In-platform table builder
- In-platform chart builder (select type → enter data → chart rendered)
- In-platform diagram canvas (draw, label, annotate)
- Platform image library (browse by subject → select → insert)
- Code block (syntax highlighted, language selector)
- Audio block (TTS — type text, select language → preview plays in-editor)
- Match columns builder
- Sequence items builder

### 5.3 Bilingual Entry Interface
- Two-column editor: Left = English | Right = target language
- Teacher fills both columns simultaneously
- Switch: can start in regional language and fill English second
- All 22 scheduled languages supported (Unicode input)
- RTL support for Urdu (editor auto-switches direction)

### 5.4 Bulk Question Entry
- Structured YAML/JSON paste mode for rapid import of many questions
- Platform validates format, detects type, imports as drafts
- Teacher reviews each imported question → publish
- Used for: entering question sets from coaching materials, importing from typed documents

### 5.5 Question Preview
- Before saving: full student-facing preview
- Preview shows: rendered equations, diagram, chart, table, image, video buttons
- Preview in multiple languages: toggle language to verify translations
- Preview on mobile viewport and desktop viewport

---

## 6. Question Approval & Governance

### 6.1 Approval Workflow
- Teacher creates → saves as Draft → submits to HOD
- HOD: Approve (→ Institution Bank) / Return with inline comments
- Section-scoped questions bypass approval (teacher publishes to own section directly)
- Platform questions: no institution approval; platform team owns quality

### 6.2 Platform Question Flagging
- Any teacher can flag a platform question for: Factual Error / Outdated / Wrong Answer /
  Poor Language / Syllabus Mismatch
- Flag sent to platform quality team → reviewed within 5 working days
- Teacher who flagged is notified of resolution

### 6.3 Question Versioning
- Every edit (content or metadata) creates new version
- Versions linked to question usage: which paper/assignment used version N
- Old versions accessible to HOD/Admin for audit
- If question was used in a completed exam, that exam record retains the version it used

### 6.4 Soft-Delete & Retirement
- Deleted questions: soft-deleted (hidden from bank, retained in DB)
- Retirement: HOD marks question as Retired with reason; auto-excluded from paper builder and practice mode
- Hard-delete: Admin only; only for questions never used in any exam
- Retired questions: visible to Admin in archived view; can be reactivated

### 6.5 Duplication Detection
- Before saving: similarity check against institution bank (> 75% similarity → warning)
- Teacher can override with confirmation
- Platform questions exempt (authoritative; institution may create similar by design)

---

## 7. Question Bank Organisation & Search

### 7.1 Browse by Hierarchy
- Drill-down from Board → Subject → Grade → Unit → Chapter → Topic → Sub-topic
- Question count at every node, broken down by: type / difficulty / source tier / unused

### 7.2 Filter Panel
- Question type (multi-select)
- Difficulty (multi-select)
- Bloom's level (multi-select)
- Exam tag (multi-select)
- PYQ: Yes/No + year range
- Marks range
- Estimated time range
- Language availability
- Source tier: Platform / Institution / Teacher
- Usage: Never used / Used 1–3 times / Used > 3 times
- CO tag (college)
- HOTS only
- Video attached: Yes/No

### 7.3 Full-Text Search
- Search across: question stem, options, solution (all languages)
- Results highlight matching text
- Filters applied on top of search results

### 7.4 Question Collections (Teacher)
- Named collections of starred/favourite questions
- Example: "Chapter 5 Numericals — JEE Level", "NEET Biology Assertion–Reason Set"
- Reuse across multiple tests and assignments
- Collections shareable with co-teachers

### 7.5 Pool Management
- Pool: named group of equivalent questions for one marks slot
- Paper builder picks one randomly from pool per student (reduces copying)
- Pool tagged with: chapter/topic, type, difficulty, marks (all questions in pool must match)
- Pool health: shows how many questions are in each pool (minimum 5 recommended)

---

## 8. PYQ (Previous Year Question) Bank

### 8.1 PYQ Coverage
- CBSE Board (Classes 10 + 12): last 15 years, all subjects, all sets
- JEE Main: last 10 years, all sessions, all shifts
- JEE Advanced: last 10 years, both papers
- NEET UG: last 10 years
- UPSC CSE Prelims: last 10 years GS1 + CSAT
- SSC CGL/CHSL: last 5 years, all tiers
- IBPS PO/Clerk: last 5 years
- All 28 State Boards: last 5 years
- State PSC Prelims: last 3 years (all 28 states)
- CTET/TET: last 5 papers
- GATE: last 5 years (all 29 papers)
- CA Foundation/Inter/Final: last 5 attempts

### 8.2 PYQ Filter Mode
- Student/teacher can filter to show only PYQs for a topic
- "Attempt all PYQs" practice mode: only PYQs, chronological or random order
- Per-question: "This question appeared in [Exam] [Year] [Paper]" badge shown in practice

### 8.3 PYQ Frequency Analysis
- Per topic: how many times questions have appeared from this sub-topic in last 10 years
- Shown as heatmap on topic browse view
- Feeds Module 16 PYQ Analysis notes (auto-data source)

---

## 9. Practice Mode (Student-Facing)

### 9.1 Practice Session Configuration
- Select: subject → chapter/topic/sub-topic (or full chapter)
- Source: Platform only / Institution + Teacher / All
- Question types: select specific types or mix
- Difficulty: Easy only / Medium / Hard / All / Adaptive
- PYQ only toggle
- Number of questions: 5 / 10 / 20 / 30 / custom
- Time: Untimed / Timed (student sets timer)

### 9.2 Adaptive Difficulty
- After correct answer → next question one difficulty level higher
- After wrong answer → next question same difficulty or one lower
- After 3 consecutive correct → jump two levels
- Ensures student is always appropriately challenged
- Feeds difficulty calibration data (Difficulty Index recalculated)

### 9.3 Question-Level Feedback in Practice
After each answer (immediately for MCQ; on submit for text answer):
- Correct / Incorrect indicator
- If incorrect: correct answer shown + explanation
- Full solution (all content blocks: text, LaTeX, diagrams, charts)
- Hints used: shown with "You used 2 of 3 hints"
- Video button: "Watch Video: Solution Walkthrough" (if video attached)
- "Try Similar Question" button → system serves similar question (same topic + type + difficulty)

### 9.4 Spaced Repetition
- Questions answered incorrectly scheduled for re-attempt:
  - After 1 day (first repeat)
  - After 3 days (second repeat)
  - After 7 days (third repeat)
  - After 21 days (fourth repeat — long-term retention)
- Based on Ebbinghaus forgetting curve
- "Due for Review" section in student dashboard shows scheduled questions
- Configurable per institution (on/off)

### 9.5 Practice History
- All past sessions: date, scope, questions attempted, score %, time spent, hints used
- Per-question history: how many times attempted, accuracy trend
- Weakest sub-topics: auto-identified from low accuracy; one-tap practice on weak area

### 9.6 Practice Gamification
- Daily practice streak: badge for 1 question answered per day
- Milestones: 7 / 30 / 100 / 365-day streaks
- "Question of the Day": one platform question per subject per day on student dashboard
- Chapter completion badge: all questions in a chapter attempted at least once
- Accuracy badge: 90%+ accuracy on a chapter

### 9.7 Peer Challenge
- Student picks a question from bank → sends to a classmate as in-app challenge
- Classmate answers → both see each other's result
- Score tracked privately (gamification; does not affect academic record)
- DPDPA 2023: peer challenge data retained 30 days then auto-deleted

### 9.8 "Similar Question" Generator
After wrong answer in practice:
- System finds 3 questions: same sub-topic + same question type + same difficulty
- Shown as "Try these related questions"
- Uses vector similarity on question content (embedding-based) + metadata match

---

## 10. Item Analysis & Quality Metrics

### 10.1 Difficulty Index (p-value)
- p = (students who answered correctly) / (total attempts)
- Calculated after minimum 30 attempts
- Auto-updates difficulty tag: p > 0.75 → EASY; 0.45–0.75 → MEDIUM; 0.25–0.45 → HARD; < 0.25 → VERY_HARD
- Teacher-assigned tag vs system-calibrated tag both shown

### 10.2 Discrimination Index (D-value)
- D = (% correct in top 27% scorers) − (% correct in bottom 27% scorers)
- D > 0.4: Excellent | 0.3–0.4: Good | 0.2–0.3: Acceptable | < 0.2: Poor — flag for review
- D < 0.1: Retire suggestion

### 10.3 Distractor Analysis (MCQ)
- Per wrong option: % of students who chose it
- Effective distractor: 10–40% of students choose it (discriminates well)
- Ineffective distractor: < 5% → teacher prompted to improve the option
- Attractive wrong option: > 40% → question may be ambiguous or option misleads correctly

### 10.4 Class-Wide Weakness Detection
- After any exam/practice: questions where > 60% of class answered wrong → flagged
- Teacher dashboard: "These 5 questions were answered wrong by most students"
- Links directly to Module 15 re-teach flag for that sub-topic

### 10.5 Question Bank Health Score
Per subject, per chapter — composite score (0–100):
- Question count vs recommended minimum (30% weight)
- Difficulty distribution: Easy/Medium/Hard balance (20% weight)
- Bloom's level distribution (20% weight)
- PYQ coverage % (15% weight)
- % questions with full solution (15% weight)
Green ≥ 80 | Yellow 60–79 | Red < 60

### 10.6 Recommended Question Count
Platform recommends minimum per chapter per type:
- Example: Class 12 Physics Chapter 1: MCQ ≥ 30 / Numerical ≥ 20 / Assertion-Reason ≥ 10 / Short Answer ≥ 10
- Gap shown as coloured bar per chapter in HOD dashboard

---

## 11. Competitive Exam Pattern Sets

### 11.1 JEE Main Pattern
- 3 sections: Physics / Chemistry / Maths
- Section A: 20 MCQ Single Correct (+4/−1)
- Section B: 10 Numerical (attempt any 5, no negative)
- Total: 300 marks, 180 minutes

### 11.2 JEE Advanced Pattern
- Paper 1 + Paper 2
- Question types: MCQ Single, MCQ Multiple, Integer, Matrix Match, Paragraph-based
- Complex partial scoring per type
- Full pattern stored per year (2015–present) in pattern library

### 11.3 NEET UG Pattern
- 4 sections: Physics / Chemistry / Botany / Zoology
- Each section: Q1–35 compulsory + Q36–45 (attempt any 10)
- +4/−1 for all

### 11.4 UPSC Prelims Pattern
- GS Paper 1: 100 MCQ, +2/−0.66, 120 min
- CSAT Paper 2: 80 MCQ, qualifying (33% cutoff), +2.5/−0.83, 120 min

### 11.5 State PSC Pattern Library
- Each of 28 state PSCs has its own pattern stored
- Institution selects state → paper builder uses correct pattern automatically

### 11.6 Banking Pattern Sets
- IBPS PO Prelims: English (30) + Quant (35) + Reasoning (35) = 100 marks, 60 min
- IBPS PO Mains: 5 sections, 200 questions, 180 min (sectional time limits)
- SBI PO, RRB PO, LIC AAO: separate pattern templates stored

---

## 12. Passage & Comprehension Bank

### 12.1 Passage Library
- Standalone passage objects independent of questions
- One passage linked to multiple question sets
- Passage types: Factual / Analytical / Literary / Discursive / Scientific / Legal / Government Notification / Editorial
- Difficulty: Flesch-Kincaid grade level auto-calculated
- Language: English / Hindi / Regional / Bilingual (parallel text)
- Subject tags: English Language / History / Political Science / Economics / UPSC / CLAT / Banking

### 12.2 Passage–Question Integrity
- When passage included in paper: all linked questions included together
- Partial selection of passage questions blocked in paper builder

### 12.3 Passage Translations
- Passage body supports `translations` field (same structure as question stem)
- Student reads passage in preferred language; questions rendered in same language

---

## 13. Viva-Voce & Oral Assessment Bank

### 13.1 Viva Question Bank
- Linked to lab experiments (Module 14) and syllabus topics (Module 15)
- Question types: Definition / Explain concept / State formula / Identify specimen /
  Describe procedure / Give example / Troubleshoot setup
- Difficulty: Basic / Intermediate / Advanced
- Subject scope: Science (all practicals), ITI trades, College lab subjects, Projects

### 13.2 Viva Evaluation Rubric
- Per viva question: rubric with marks split
- Example: "State Ohm's Law" → Correct statement (1 mark) + Units (0.5 mark) + Limitations (0.5 mark)
- Examiner selects rubric level per student during viva; auto-tallies score

---

## 14. Special Question Banks

### 14.1 Olympiad & Scholarship Bank
- NSO / NCO / IMO / SOF: chapter-wise
- NTSE: SAT + MAT (state-level pattern per state)
- KVPY: Stream SA/SB/SX
- State scholarship exams: Rajasthan, Maharashtra, UP, MP, Karnataka, TN
- Questions tagged: `is_olympiad: true` + specific olympiad tag

### 14.2 HOTS Bank
- All Bloom's L4–L6 questions tagged `is_hots: true`
- Separate HOTS practice mode for gifted students
- CBSE "Case Study" and "Source-Based" questions (introduced 2021 onward) auto-tagged HOTS

### 14.3 Value-Based / Life Skills Questions
- CBSE mandate: value-based questions in all board papers
- Topics: Environmental values, Constitutional values, Gender equality, Social justice,
  Scientific temper, Anti-ragging, Road safety
- Tagged: `is_value_based: true`

### 14.4 CWSN Adapted Questions
- Parallel CWSN variant per standard question
- Simplifications: plain language, reduced word count, shorter options, no time pressure flag
- Audio-read flag: question to be read aloud by examiner or TTS
- Tagged: `is_cwsn_variant: true`, `parent_question_id: original-uuid`
- CWSN students see CWSN variant automatically (Module 07 profile flag)

### 14.5 FLN / NIPUN Bharat Questions (Classes 1–3)
- Audio questions (TTS in Hindi + regional language)
- Picture-description + MCQ option (large text options)
- Oral activity prompts ("Say the word aloud", "Circle the bigger number")
- Competency code tagged per question (`nipun_code`)
- Used in formative FLN assessments; results feed NIPUN milestone tracking

### 14.6 Cross-Subject Integrated Questions
- Question linked to two subjects simultaneously
- Example: Lens formula question → Physics + Maths
- Appears in both subject banks
- Tagged: `cross_subject_ids: ["physics-uuid", "maths-uuid"]`
- Used in NEP 2020 integrated/multidisciplinary courses

---

## 15. Quick Quiz & Formative Assessment

### 15.1 Quick Quiz Builder
- Teacher selects 5–10 questions from bank in < 2 minutes
- Assign to section with one tap
- Students answer in-app; teacher sees live response count + % correct
- No exam formality; results shown to teacher only (not published to students as grade)

### 15.2 Exit Ticket
- 1–3 question end-of-period check
- Teacher publishes from question bank; students answer before leaving class
- Teacher sees: response count, % correct per option (MCQ), common wrong answers
- Feeds Module 15 topic coverage confidence metric

### 15.3 Poll Question
- Non-graded single question for engagement
- Results shown live as animated bar chart to teacher + students
- Not recorded in gradebook
- Used for: opinion polls, prior knowledge checks, icebreakers

### 15.4 Student Question Submission
- Student creates a question in-app (same editor, limited to MCQ and Short Answer)
- Submitted to teacher for review
- Approved → added to institution bank with student attribution badge
- Promotes active learning; gamification: "Question Author" badge for student

---

## 16. Analytics & Reporting

### 16.1 Per-Question Analytics (Teacher/HOD)
- Attempt count, unique students, % correct, avg time, difficulty index (auto), discrimination index
- Distractor analysis (MCQ): option-wise selection %
- Language-wise performance: if question attempted in multiple languages, compare accuracy

### 16.2 Subject-Level Question Bank Report (HOD)
- Questions by: type / difficulty / Bloom's level / exam tag / source tier
- Recommended count vs actual count per chapter (gap traffic light)
- PYQ coverage %
- Low-quality questions (poor discrimination) flagged for review

### 16.3 Student Practice Analytics (Student View)
- Accuracy per subject / chapter / topic / sub-topic
- Improvement trend (weekly)
- Time per question (vs class average)
- Spaced repetition queue: questions due for review today
- Weak sub-topics list

### 16.4 Class-Level Weakness Report (Teacher)
- Top questions answered wrong by most students
- Which sub-topics are class-wide weak spots
- Feeds Module 15 re-teach flag and Module 47 AI analytics

### 16.5 NAAC / NBA Evidence Export
- Question bank inventory: count by type / Bloom's / difficulty / CO tag
- CO-wise question distribution (for NBA attainment evidence)
- PYQ integration % (how much of platform PYQ bank is in institution's scope)
- Export as NAAC SSR Criterion 2 / NBA Criterion 5 format

### 16.6 Question Bank Analytics Export
- Excel: full question list with metadata (no content — metadata only for privacy)
- Columns: question_id, type, chapter, topic, difficulty, marks, exam_tags, attempts, % correct
- HOD uses for academic committee review

---

## 17. Data Architecture

### 17.1 CDN-First Content Storage

All question media assets (platform images, diagram renders, chart renders, audio clips)
are stored in CDN — **not in the database**. The database stores only the JSON reference
(image_id / cdn_path). The CDN is organised by subject and topic hierarchy:

```
CDN Path Structure:
/questions/
  /{board_code}/              e.g. CBSE/
    /{subject_code}/          e.g. PHYSICS/
      /{grade}/               e.g. 12/
        /{unit_code}/         e.g. UNIT_01/
          /{chapter_code}/    e.g. CH_01/
            /{topic_code}/    e.g. ELECTRIC_FIELD/
              /images/        platform image library assets
              /diagrams/      rendered diagram PNGs (cached from canvas JSON)
              /charts/        rendered chart PNGs (cached from chart JSON)
              /audio/         TTS audio clips (pre-rendered for FLN/language questions)
```

CDN rules:
- Platform assets: served from EduForge global CDN (CloudFront); immutable URLs per version
- Diagram and chart JSON → rendered server-side → PNG cached on CDN on first request
- Audio TTS → pre-rendered per language → stored at topic level on CDN
- Institution/teacher media: same CDN structure under `/tenant/{tenant_id}/questions/...`
- No media stored in PostgreSQL — DB holds only `cdn_path` and `image_id` references
- CDN cache TTL: platform assets = 1 year (immutable per version); tenant assets = 30 days

### 17.2 Tenancy
- Platform questions: `tenant_id = NULL` (global read; no tenant can edit)
- Institution questions: `tenant_id = institution_id` (RLS scoped)
- Teacher questions: `tenant_id` + `author_id` scoped
- Student practice data: tenant + student scoped; DPDPA 2023 compliant

### 17.2 Database Schema

```sql
-- Question master
questions (
  question_id       UUID PK,
  tenant_id         UUID FK tenants NULL,     -- NULL = platform question
  source_tier       VARCHAR(15),              -- PLATFORM | INSTITUTION | TEACHER
  type              VARCHAR(30),              -- MCQ_SINGLE | NUMERICAL | etc.
  board_id          UUID FK boards NULL,
  subject_id        UUID FK subjects_master NULL,
  grade             VARCHAR(20) NULL,
  unit_id           UUID FK syllabus_units NULL,
  chapter_id        UUID FK syllabus_chapters NULL,
  topic_id          UUID FK syllabus_topics NULL,
  subtopic_id       UUID FK syllabus_topics NULL,
  bloom_level       VARCHAR(20),
  difficulty_tag    VARCHAR(15),              -- teacher-assigned
  difficulty_index  NUMERIC(4,3) NULL,        -- system-calculated p-value
  discrim_index     NUMERIC(4,3) NULL,        -- system-calculated D-value
  marks             NUMERIC(4,1),
  negative_marks    NUMERIC(4,2) DEFAULT 0,
  partial_marks     BOOLEAN DEFAULT FALSE,
  estimated_seconds INTEGER,
  exam_tags         TEXT[],
  is_pyq            BOOLEAN DEFAULT FALSE,
  pyq_year          INTEGER NULL,
  pyq_exam          VARCHAR(50) NULL,
  pyq_paper         VARCHAR(100) NULL,
  pyq_question_no   INTEGER NULL,
  primary_language  VARCHAR(10) DEFAULT 'en',
  available_languages TEXT[],
  is_bilingual      BOOLEAN DEFAULT FALSE,
  co_tags           TEXT[],
  nos_code          VARCHAR(50) NULL,
  nipun_code        VARCHAR(50) NULL,
  is_cwsn_variant   BOOLEAN DEFAULT FALSE,
  parent_question_id UUID NULL,
  is_hots           BOOLEAN DEFAULT FALSE,
  is_formative      BOOLEAN DEFAULT FALSE,
  is_olympiad       BOOLEAN DEFAULT FALSE,
  olympiad_tags     TEXT[],
  is_value_based    BOOLEAN DEFAULT FALSE,
  pool_id           UUID NULL,
  pool_slot         VARCHAR(50) NULL,
  retired           BOOLEAN DEFAULT FALSE,
  retire_reason     TEXT NULL,
  copyright_type    VARCHAR(20),
  platform_version  VARCHAR(20) NULL,
  last_updated      DATE NULL,
  author_id         UUID FK users NULL,
  approved_by       UUID FK users NULL,
  approved_at       TIMESTAMPTZ NULL,
  usage_count       INTEGER DEFAULT 0,
  attempt_count     INTEGER DEFAULT 0,
  created_at        TIMESTAMPTZ,
  updated_at        TIMESTAMPTZ
)

-- Versioned question content (unified JSON)
question_versions (
  version_id        UUID PK,
  question_id       UUID FK questions,
  version_number    INTEGER,
  content_json      JSONB,                  -- full unified question JSON (stem, options, answer, solution, hints, video_links)
  edited_by         UUID FK users NULL,
  edit_reason       TEXT,
  created_at        TIMESTAMPTZ
)

-- Platform image library
platform_images (
  image_id          UUID PK,
  category          VARCHAR(50),
  subject_tags      TEXT[],
  alt_text          TEXT,
  caption           TEXT,
  cdn_path          TEXT,
  platform_version  VARCHAR(20),
  created_at        TIMESTAMPTZ
)

-- Passage bank
passages (
  passage_id        UUID PK,
  tenant_id         UUID FK tenants NULL,
  source_tier       VARCHAR(15),
  title             VARCHAR(300),
  passage_type      VARCHAR(30),
  content_json      JSONB,                  -- passage body as content blocks
  translations      JSONB,                  -- {hi: [...], ta: [...], ...}
  difficulty_grade  NUMERIC(3,1),           -- Flesch-Kincaid grade
  subject_tags      TEXT[],
  language          VARCHAR(10),
  created_at        TIMESTAMPTZ
)

passage_questions (
  pq_id             UUID PK,
  passage_id        UUID FK passages,
  question_id       UUID FK questions,
  sequence_no       INTEGER
)

-- Question collections
question_collections (
  collection_id     UUID PK,
  tenant_id         UUID FK tenants,
  created_by        UUID FK users,
  name              VARCHAR(300),
  subject_id        UUID FK subjects_master NULL,
  is_shared         BOOLEAN DEFAULT FALSE,
  created_at        TIMESTAMPTZ
)

collection_questions (
  cq_id             UUID PK,
  collection_id     UUID FK question_collections,
  question_id       UUID FK questions,
  sequence_no       INTEGER
)

-- Student practice sessions
practice_sessions (
  session_id        UUID PK,
  tenant_id         UUID FK tenants,
  student_id        UUID FK users,
  scope_type        VARCHAR(20),            -- CHAPTER | TOPIC | SUBTOPIC | CUSTOM
  scope_id          UUID NULL,
  filter_json       JSONB,                  -- recorded filters applied
  mode              VARCHAR(20),            -- UNTIMED | TIMED | ADAPTIVE | PYQ_ONLY
  total_questions   INTEGER,
  attempted         INTEGER DEFAULT 0,
  correct           INTEGER DEFAULT 0,
  total_marks       NUMERIC(6,1),
  earned_marks      NUMERIC(6,1),
  time_limit_secs   INTEGER NULL,
  time_spent_secs   INTEGER DEFAULT 0,
  completed         BOOLEAN DEFAULT FALSE,
  started_at        TIMESTAMPTZ,
  ended_at          TIMESTAMPTZ NULL
)

-- Per-question attempt in practice
practice_attempts (
  attempt_id        UUID PK,
  session_id        UUID FK practice_sessions,
  question_id       UUID FK questions,
  question_version  INTEGER,
  student_id        UUID FK users,
  tenant_id         UUID FK tenants,
  response_json     JSONB,                  -- student's answer
  is_correct        BOOLEAN,
  marks_earned      NUMERIC(4,1),
  hints_used        INTEGER DEFAULT 0,
  time_spent_secs   INTEGER,
  language_used     VARCHAR(10),
  created_at        TIMESTAMPTZ
)

-- Spaced repetition schedule
spaced_repetition (
  sr_id             UUID PK,
  tenant_id         UUID FK tenants,
  student_id        UUID FK users,
  question_id       UUID FK questions,
  next_review_date  DATE,
  interval_days     INTEGER DEFAULT 1,
  repetition_count  INTEGER DEFAULT 0,
  easiness_factor   NUMERIC(3,2) DEFAULT 2.50,
  last_attempt_at   TIMESTAMPTZ,
  created_at        TIMESTAMPTZ
)

-- Item analysis (aggregated)
question_item_analysis (
  analysis_id       UUID PK,
  question_id       UUID FK questions,
  tenant_id         UUID FK tenants NULL,   -- NULL = platform-wide analysis
  total_attempts    INTEGER,
  correct_attempts  INTEGER,
  difficulty_index  NUMERIC(4,3),
  discrim_index     NUMERIC(4,3),
  option_stats      JSONB,                  -- {A: {count, pct}, B: {count, pct}, ...}
  calculated_at     TIMESTAMPTZ
)

-- Question flag log
question_flags (
  flag_id           UUID PK,
  question_id       UUID FK questions,
  flagged_by        UUID FK users,
  tenant_id         UUID FK tenants NULL,
  flag_type         VARCHAR(30),            -- FACTUAL_ERROR | WRONG_ANSWER | OUTDATED | SYLLABUS_MISMATCH | LANGUAGE_ERROR
  description       TEXT,
  status            VARCHAR(20) DEFAULT 'OPEN',
  resolved_by       UUID FK users NULL,
  resolved_at       TIMESTAMPTZ NULL,
  created_at        TIMESTAMPTZ
)
```

### 17.3 Indexes
```sql
CREATE INDEX idx_questions_platform     ON questions(source_tier, board_id, subject_id, grade) WHERE tenant_id IS NULL;
CREATE INDEX idx_questions_tenant       ON questions(tenant_id, chapter_id, type, retired);
CREATE INDEX idx_questions_topic        ON questions(topic_id, subtopic_id, difficulty_tag, is_pyq);
CREATE INDEX idx_questions_exam_tags    ON questions USING GIN(exam_tags);
CREATE INDEX idx_questions_languages    ON questions USING GIN(available_languages);
CREATE INDEX idx_qversions_content      ON question_versions USING GIN(content_json);
CREATE INDEX idx_practice_student       ON practice_attempts(student_id, question_id, created_at);
CREATE INDEX idx_spaced_rep_due         ON spaced_repetition(student_id, next_review_date);
CREATE INDEX idx_item_analysis_question ON question_item_analysis(question_id, calculated_at DESC);
```

---

## 18. Roles & Permissions

| Action | Student | Teacher | HOD | Principal | Admin |
|---|---|---|---|---|---|
| Browse / search question bank | Practice only | ✅ | ✅ | View | ✅ |
| Create / edit questions | Submit only | Own | Dept | View | All |
| Publish to section | — | ✅ own section | ✅ | — | ✅ |
| Submit for institution bank | — | ✅ | — | — | — |
| Approve for institution bank | — | — | ✅ | ✅ | ✅ |
| Flag platform question | — | ✅ | ✅ | — | — |
| View item analysis | — | Own | Dept | All | All |
| Retire / restore question | — | — | ✅ dept | ✅ all | ✅ |
| Create question collection | — | ✅ | ✅ | — | — |
| View practice analytics | Own | Own students | Dept | All | All |
| Export question bank | — | — | ✅ | ✅ | ✅ |

---

## 19. Notifications (In-App Only)

| Trigger | Recipient |
|---|---|
| Question returned by HOD with comments | Teacher |
| Question approved for institution bank | Teacher |
| Platform question updated (new version) | Teacher (if used in recent paper) |
| Platform question flag resolved | Teacher who flagged |
| Question of the Day available | Student |
| Spaced repetition review due today | Student |
| Peer challenge received | Student |
| Low question count alert (< recommended) per chapter | HOD |
| High wrong-answer rate on question (> 70% wrong) | Teacher |
| Quick quiz published by teacher | Student |
| Exit ticket published | Student |

---

## 20. Compliance Summary

| Standard | Coverage |
|---|---|
| CBSE Curriculum Framework 2023 | CBSE PYQ bank, CCE/formative tags, value-based questions, case study/source-based types |
| NEP 2020 | HOTS questions, cross-subject integrated questions, FLN/NIPUN bank (Classes 1–3), multilingual support |
| NIPUN Bharat | Classes 1–3 FLN audio questions, competency code tags, oral activity prompts |
| UGC / AICTE OBE | CO-tagged questions, CO-wise distribution for NBA attainment evidence |
| NCVT / DGT | ITI trade theory question bank, NOS code tagged, unit-wise |
| RTE Act / RPWD Act | CWSN adapted question variants, audio-read flag, plain language, reduced complexity |
| DPDPA 2023 | Student practice data retention 2 years; deletion on request; peer challenge data 30-day auto-delete |
| Copyright Act 1957 § 52(1)(i) | PYQ bank: educational fair use; platform-authored: EduForge IP; institution: institution IP |
| IT Act 2000 | In-app copy block on question content; screenshot advisory flag |
| NAAC SSR Criterion 2 | Question bank inventory, Bloom's distribution, CO mapping for accreditation evidence |
| NBA Criterion 5 | CO-wise question count, attainment evidence export |
