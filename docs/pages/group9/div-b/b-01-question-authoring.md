# B-01 — Question Authoring Tool

> **URL:** `/content-partner/author/question`
> **File:** `b-01-question-authoring.md`
> **Priority:** P1
> **Roles:** Content Partner · EduForge Editorial Team (review queue)

---

## Overview

The Question Authoring Tool provides content partners with a rich-text editor for creating individual questions destined for EduForge's 18,42,000+ question pool. The tool supports LaTeX rendering for mathematical expressions, inline image uploads, multi-language authoring (English, Telugu, Hindi), and real-time preview. Partners like Dr. Venkat Rao (Visakhapatnam, retired Maths Professor, Andhra University) use this interface daily to craft quantitative aptitude and reasoning questions for APPSC, SSC CGL/CHSL, and Banking IBPS PO exams.

---

## Mockup 1 — Question Authoring Form (Main Editor)

```
+------------------------------------------------------------------+
| EduForge Content Partner Portal                   Dr. Venkat Rao  |
+------------------------------------------------------------------+
| Dashboard > Author > New Question                                 |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------------------------------------------------+  |
|  | QUESTION AUTHORING TOOL                        [Save Draft] |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  |  Question Type:  [ MCQ (Single Correct)        v ]          |  |
|  |                  ---------------------------                |  |
|  |                  | MCQ (Single Correct)    |                |  |
|  |                  | MCQ (Multi Correct)     |                |  |
|  |                  | Numerical Answer        |                |  |
|  |                  | Match the Column        |                |  |
|  |                  | Assertion-Reasoning     |                |  |
|  |                  | Comprehension Based     |                |  |
|  |                  ---------------------------                |  |
|  |                                                             |  |
|  |  Language:  (o) English  ( ) Telugu  ( ) Hindi               |  |
|  |                                                             |  |
|  |  Exam(s):   [x] APPSC Group 1/2  [x] SSC CGL               |  |
|  |             [ ] SSC CHSL  [x] IBPS PO  [ ] RRB NTPC        |  |
|  |                                                             |  |
|  |  Subject:   [ Quantitative Aptitude    v ]                  |  |
|  |  Topic:     [ Number Systems           v ]                  |  |
|  |  Sub-Topic: [ HCF & LCM               v ]                  |  |
|  |                                                             |  |
|  |  Difficulty: ( )1  ( )2  (o)3  ( )4  ( )5                   |  |
|  |  Expected Time (sec): [ 90 ]                                |  |
|  |                                                             |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  |  Question Text:                            [B] [I] [LaTeX] |  |
|  |  +------------------------------------------------------+  |  |
|  |  | If the HCF of two numbers is 12 and their LCM is    |  |  |
|  |  | 360, and one of the numbers is 60, find the other    |  |  |
|  |  | number.                                               |  |  |
|  |  |                                                       |  |  |
|  |  | Use: $\text{HCF} \times \text{LCM} = a \times b$     |  |  |
|  |  +------------------------------------------------------+  |  |
|  |                                                             |  |
|  |  (A) [ 72                                              ]    |  |
|  |  (B) [ 60                                              ]    |  |
|  |  (C) [ 48                                              ]    |  |
|  |  (D) [ 36                                              ]    |  |
|  |                                                             |  |
|  |  Correct Answer: [ A v ]                                    |  |
|  |                                                             |  |
|  |  Explanation:                               [B] [I] [LaTeX]|  |
|  |  +------------------------------------------------------+  |  |
|  |  | We know $\text{HCF} \times \text{LCM} = a \times b$ |  |  |
|  |  | $12 \times 360 = 60 \times b$                         |  |  |
|  |  | $b = \frac{12 \times 360}{60} = \frac{4320}{60} = 72$|  |  |
|  |  | Therefore, the other number is 72.                    |  |  |
|  |  +------------------------------------------------------+  |  |
|  |                                                             |  |
|  |  [Upload Image]  Attached: (none)                           |  |
|  |                                                             |  |
|  +------------------------------------------------------------+  |
|  |  [ Save Draft ]  [ Preview ]  [ Submit for Review ]         |  |
|  +------------------------------------------------------------+  |
|                                                                   |
+------------------------------------------------------------------+
```

---

## Mockup 2 — LaTeX Preview & Multi-Language Panel

```
+------------------------------------------------------------------+
| QUESTION PREVIEW                                      [x] Close  |
+------------------------------------------------------------------+
|                                                                   |
|  Language: [English v]  [+ Add Telugu Translation]                 |
|                                                                   |
|  +------------------------------------------------------------+  |
|  |  RENDERED PREVIEW                                          |  |
|  |                                                             |  |
|  |  Q. If the HCF of two numbers is 12 and their LCM is      |  |
|  |     360, and one of the numbers is 60, find the other      |  |
|  |     number.                                                 |  |
|  |                                                             |  |
|  |            x^2 + 3x                                         |  |
|  |     Use:  ----------  (rendered LaTeX)                      |  |
|  |               2                                             |  |
|  |                                                             |  |
|  |     HCF x LCM = a x b                                      |  |
|  |                                                             |  |
|  |  (A) 72       (B) 60       (C) 48       (D) 36             |  |
|  |   ^correct                                                  |  |
|  |                                                             |  |
|  |  EXPLANATION:                                               |  |
|  |  We know HCF x LCM = a x b                                 |  |
|  |  12 x 360 = 60 x b                                         |  |
|  |       12 x 360     4320                                     |  |
|  |  b = ----------- = ----- = 72                               |  |
|  |          60          60                                      |  |
|  |                                                             |  |
|  |  Therefore, the other number is 72.                         |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  +------------------------------------------------------------+  |
|  |  METADATA SUMMARY                                          |  |
|  |  Exam(s): APPSC Group 1/2, SSC CGL, IBPS PO               |  |
|  |  Subject: Quantitative Aptitude                             |  |
|  |  Topic: Number Systems > HCF & LCM                         |  |
|  |  Difficulty: 3/5 | Time: 90s | Language: English            |  |
|  |  Partner: Dr. Venkat Rao (VR-2024-0001)                     |  |
|  |  Status: Draft | Created: 2026-03-31 09:15 IST              |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  [ Edit ]  [ Submit for Review ]                                  |
+------------------------------------------------------------------+
```

---

## Mockup 3 — Image Upload & Advanced Options

```
+------------------------------------------------------------------+
| QUESTION AUTHORING — Advanced Options              Dr. Venkat Rao |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------------------------------------------------+  |
|  | IMAGE UPLOAD                                                |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  |  +------------------+   Upload Guidelines:                  |  |
|  |  |                  |   - Max size: 2 MB                    |  |
|  |  |   [geometry.png] |   - Formats: PNG, JPG, SVG            |  |
|  |  |   425 x 320 px   |   - Min resolution: 300x200 px       |  |
|  |  |   Size: 145 KB   |   - No watermarks allowed             |  |
|  |  |                  |                                       |  |
|  |  +------------------+   Position: [Inline with question v]  |  |
|  |                         Alt text: [Right triangle ABC___]   |  |
|  |  [Replace Image] [Remove]                                   |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | SOURCE & TAGGING                                            |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  |  Source:       [ Original                v ]                |  |
|  |                 -------------------------                   |  |
|  |                 | Original              |                   |  |
|  |                 | Previous Year (PYQ)   |                   |  |
|  |                 | Adapted               |                   |  |
|  |                 -------------------------                   |  |
|  |  PYQ Year:     [ ---- ]  (enabled if PYQ selected)         |  |
|  |  PYQ Exam:     [ ---- ]  (enabled if PYQ selected)         |  |
|  |                                                             |  |
|  |  Tags:  [ #HCF ] [ #LCM ] [ #NumberTheory ] [+ Add Tag]   |  |
|  |                                                             |  |
|  |  Internal Note (for editorial team):                        |  |
|  |  +------------------------------------------------------+  |  |
|  |  | Good foundational question for banking aspirants.     |  |  |
|  |  | Covers basic HCF-LCM relationship formula.            |  |  |
|  |  +------------------------------------------------------+  |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | QUESTION HISTORY                                            |  |
|  +------------------------------------------------------------+  |
|  | Version | Date       | Action         | By                 |  |
|  |---------|------------|----------------|--------------------|  |
|  | v1      | 2026-03-31 | Created        | Dr. Venkat Rao     |  |
|  | --      | --         | Pending review | --                 |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  [ Save Draft ]  [ Preview ]  [ Submit for Review ]              |
+------------------------------------------------------------------+
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/content-partner/author/questions` | List all authored questions for the logged-in partner |
| POST | `/api/v1/content-partner/author/questions` | Create a new question (draft or submit) |
| GET | `/api/v1/content-partner/author/questions/{id}` | Retrieve a specific question by ID |
| PUT | `/api/v1/content-partner/author/questions/{id}` | Update an existing question (draft only) |
| DELETE | `/api/v1/content-partner/author/questions/{id}` | Delete a draft question (cannot delete submitted/approved) |
| POST | `/api/v1/content-partner/author/questions/{id}/submit` | Submit a draft question for editorial review |
| POST | `/api/v1/content-partner/author/questions/{id}/images` | Upload an image attachment to a question |
| DELETE | `/api/v1/content-partner/author/questions/{id}/images/{img_id}` | Remove an image attachment |
| GET | `/api/v1/content-partner/author/questions/{id}/preview` | Render LaTeX and return HTML preview |
| POST | `/api/v1/content-partner/author/questions/{id}/translate` | Add or update a translation for a question |
| GET | `/api/v1/content-partner/author/metadata/exams` | List available exams for tagging |
| GET | `/api/v1/content-partner/author/metadata/topics` | List subjects, topics, and sub-topics tree |

---

## Business Rules

1. Every question submitted through the authoring tool must include at minimum the following metadata before it can transition from draft to submitted status: at least one target exam, a subject, a topic, a sub-topic, a difficulty rating between 1 and 5, an expected solving time in seconds, and the correct answer designation. The system will block the "Submit for Review" action and display field-level validation errors if any of these mandatory fields are left empty. For MCQ-type questions, at least two answer options must be non-empty, and the correct answer must reference a populated option. For numerical answer type questions the system enforces that the partner specifies an acceptable tolerance range (absolute or percentage) so that the auto-grading engine can evaluate student responses fairly. Dr. Venkat Rao's typical workflow involves saving multiple drafts throughout the day and only submitting a batch of 15-20 questions in the evening, so the draft state must persist reliably across browser sessions using server-side storage rather than relying on local browser state.

2. LaTeX expressions embedded within question text, answer options, or explanations are rendered using MathJax 3.x on the client side and KaTeX on the server side for preview generation and PDF export. The editor supports both inline mode (single dollar signs, e.g., `$\frac{x^2 + 3x}{2}$`) and display mode (double dollar signs, e.g., `$$\sqrt{144} = 12$$`). When a partner types a LaTeX expression, the preview panel updates within 300 milliseconds using debounced rendering to avoid performance degradation during rapid typing. The system maintains a whitelist of permitted LaTeX commands to prevent injection attacks and rejects any expression containing raw HTML, JavaScript, or disallowed macro definitions. If a LaTeX expression fails to parse, the preview panel highlights it in red with the specific parsing error message so the partner can correct it before submission. All rendered output is sanitized before storage to ensure that no executable code persists in the question bank.

3. Image uploads are restricted to PNG, JPG, and SVG formats with a maximum file size of 2 MB per image and a maximum of 4 images per question. Upon upload, the system generates a compressed thumbnail (150x150 px) for the question list view and stores the original at full resolution for the student-facing test interface. Images are scanned for embedded metadata (EXIF) and stripped of GPS coordinates and device identifiers to protect partner privacy. A SHA-256 hash of each image is computed and compared against existing images in the question bank to detect and flag duplicate uploads, which helps the editorial team identify potential content reuse or plagiarism across different partner accounts. For geometry and diagram-heavy questions common in Dr. Venkat Rao's quantitative aptitude contributions, the system recommends SVG format because it renders crisply at any zoom level on student devices ranging from mobile phones to desktop monitors.

4. Multi-language support allows a question to exist in up to three language variants (English, Telugu, Hindi) linked under a single canonical question ID. The primary language is set at creation time and determines the canonical version used for deduplication checks and editorial review. Translation variants can be added by the original partner or by a designated translation partner (e.g., Telugu Vidya Content handles Telugu translations for Dr. Venkat Rao's English-authored questions). The system enforces structural parity between translations: if the English version has four MCQ options, the Telugu version must also have exactly four options in the same order, and the correct answer index must match. Translation completeness is tracked as a percentage on the partner dashboard, and the editorial team can filter the review queue by language to prioritize translations needed for upcoming state-level exams such as APPSC or TSPSC where vernacular language availability is critical for candidate accessibility.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division B*
