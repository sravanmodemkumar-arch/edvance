# F-10 — OMR Sheet Processing Manager

## 1. Page Metadata

| Field | Value |
|---|---|
| **Route** | `GET /ops/exam/omr/` |
| **Django View** | `OMRDashboardView` (main) · `OMRBatchDetailView` (`/ops/exam/omr/batches/<batch_id>/`) |
| **Template** | `portal_base_dark.html` → `ops/omr_dashboard.html` |
| **Primary Role** | OMR Processing Specialist (109, Level 3) |
| **Also Accessible** | Exam Configuration Specialist (90) · Exam Operations Manager (34) · Results Coordinator (36, results integration) · Platform Admin (10) |
| **Priority** | P1 |
| **Status** | ⬜ Not started |
| **Indian Context** | Critical for Indian schools and coaching institutes using OMR-based assessments alongside digital exams |

---

## 2. Purpose & Business Logic

OMR (Optical Mark Recognition) is deeply embedded in Indian education:

**Why OMR still matters in 2026:**
- All major national competitive exams (UPSC Prelims, SSC, RRB Group D, NEET, JEE Main Shift 2 centres, IBPS) are OMR-based
- Most district-level government schools use OMR for internal assessments — no reliable internet for online exams
- Board exam practice papers in most coaching institutes are conducted on OMR sheets to simulate actual exam conditions
- CBSE/state board practical exams use OMR for subjective mark entry
- Rural coaching centres use physical OMR + scanner rather than digital exam servers

**EduForge's OMR workflow:**
1. **PM Exam Domains (B-34/B-09)** configures an exam that allows OMR mode
2. **Exam Config Specialist (90)** schedules the exam with mode = `OFFLINE_OMR`
3. **OMR Specialist (109)** creates the OMR template (bubble layout matching the question paper)
4. Institution conducts the exam on printed OMR sheets
5. Institution admin scans sheets using scanner/phone and uploads batch (via institution portal)
6. EduForge processes the scanned images — reads bubble positions, generates responses
7. **OMR Specialist (109)** reviews flagged ambiguous bubbles
8. Processed responses feed into **F-04 Results Management** exactly like digital exam submissions

**Scale:**
- Up to 300 simultaneous scheduled OMR exams on peak exam days (NEET practice, SSC prelims mock)
- Each exam: 50–500 students' OMR sheets per institution
- Typical coaching institute: 200–2,000 OMR sheets per exam event
- Peak: ~50,000 OMR sheets in a single day across all institutions

**Critical constraint:** OMR results must integrate seamlessly with F-04 Results Management. From the results pipeline's perspective, a processed OMR submission is identical to a digital online submission.

---

## 3. User Roles & Access

| Role | Access | Notes |
|---|---|---|
| OMR Processing Specialist (109) | Full — create templates · review batches · QA ambiguous marks · reject batches · escalate | Cannot modify exam schedule (F-01) or publish results (F-04) |
| Exam Config Specialist (90) | Read + configure OMR mode on exams · assign template to exam schedule | Cannot review individual OMR sheets |
| Exam Operations Manager (34) | Read + approve rejected batches + emergency re-process | Oversight role |
| Results Coordinator (36) | Read (batch processing status only) · receives notification when batch is Results-Ready | Triggers result compute in F-04 once OMR batch is READY |
| Platform Admin (10) | Full | — |

---

## 4. Page Layout — Dashboard

### 4.1 Header

```
Exam Ops / OMR Sheet Processing
[+ Create OMR Template]    [View All Batches]    [OMR Config Settings]
```

---

### 4.2 KPI Strip (4 tiles, updated every 60s via HTMX poll)

| Tile | Metric | Colour |
|---|---|---|
| Batches In Progress | Count batches at status UPLOADING/PROCESSING/REVIEW | Amber if > 5 |
| Sheets Awaiting Review | Count ambiguous/flagged sheets across all open batches | Red if > 50 |
| Batches Results-Ready | Count batches PROCESSED and ready for F-04 | Green if > 0 |
| Processing Error Rate | % of sheets with processing failure (last 7 days) | Red if > 5% |

---

### 4.3 Tabs

**Tab 1: Active Batches** (default)
**Tab 2: OMR Templates**
**Tab 3: Completed Batches**
**Tab 4: Processing Stats**

---

### Tab 1: Active Batches

All OMR scan batches currently in workflow (not yet results-ready or failed).

**Batch table:**

| Batch ID | Exam Name | Institution | Sheets Uploaded | Processed | Flagged | Status | Uploaded | Actions |
|---|---|---|---|---|---|---|---|---|
| OMR-2026-03890 | SSC CGL Mock Test 3 | Vidya Coaching Centre | 248 | 236 | 12 | 🔴 Review | 2h ago | [Review] [Reject] |
| OMR-2026-03889 | NEET Practice 2026 #5 | Apex Institute | 320 | 320 | 0 | ✅ Results-Ready | 4h ago | [Push to Results] |
| OMR-2026-03888 | RRB NTPC Mock Round 2 | Rail Coaching Hyderabad | 156 | 0 | 0 | ⏳ Processing | 6min ago | [View Progress] |
| OMR-2026-03887 | Class 10 CBSE Mock | Delhi Public School | 89 | 89 | 4 | 🔴 Review | 8h ago | [Review] [Reject] |

**Status pipeline:**
```
UPLOADING → QUEUED → PROCESSING → REVIEW_PENDING → REVIEWED → RESULTS_READY
                                                              ↓
                                                     REJECTED (with reason → institution notified)
```

**Batch Status details:**
- **UPLOADING**: Institution is still uploading scan files
- **QUEUED**: Upload complete; waiting for processing Lambda
- **PROCESSING**: Lambda is reading bubbles from scanned images (typically 30–120s per 100 sheets)
- **REVIEW_PENDING**: Processing complete; some sheets flagged for manual review
- **REVIEWED**: All flags resolved by OMR Specialist
- **RESULTS_READY**: Clean batch; Results Coordinator can trigger F-04 result compute
- **REJECTED**: Batch rejected due to quality issues; institution re-submits

**[Push to Results]** — for RESULTS_READY batches: sends batch data to F-04 Results Management queue → Results Coordinator receives in-app notification.

---

### Tab 2: OMR Templates

Master library of OMR sheet layouts for different exam types.

**Template table:**

| Template Name | Questions | Options per Q | Sections | Used In Exams | Created By | Status |
|---|---|---|---|---|---|---|
| SSC-CGL-100Q-4OPT | 100 | 4 (A/B/C/D) | Single | 234 exams | OMR Specialist | ✅ Active |
| NEET-200Q-4OPT | 200 | 4 (A/B/C/D) | Physics/Chemistry/Biology | 89 exams | OMR Specialist | ✅ Active |
| UPSC-100Q-4OPT-ROLLNO | 100 | 4 + Roll No field | Single | 12 exams | OMR Specialist | ✅ Active |
| CLASS10-CBSE-40Q-MIXED | 40 | 4 MCQ + 6 Short Answer marks | 3 subjects | 8 exams | OMR Specialist | ✅ Active |
| JEE-90Q-4OPT-INT | 90 | 4 MCQ + Integer-Type grid | Chemistry/Physics/Maths | 156 exams | OMR Specialist | ✅ Active |

**[+ Create OMR Template]** → opens template builder (full-page or wide drawer — see section 5).

**Template card (on click):**
- Preview: rendered OMR sheet layout (A4, grayscale, shows bubble positions, roll number field, booklet code boxes)
- Linked exams list
- Calibration data (anchor points used for scan alignment)
- [Download Sample Sheet PDF] — printable blank OMR sheet based on this template
- [Edit] (only if no active batches use this template) · [Duplicate] · [Archive]

---

### Tab 3: Completed Batches

Paginated history of all processed batches.

**Filters**: Institution · Exam Name · Date range · Status (Results-Pushed / Rejected / All)

**Table** same structure as Tab 1 plus: Completion Time · Processing Duration · Flagged/Total ratio.

**[Download Batch Report]** per row: PDF with all processed responses (anonymised, exam-standard format).

---

### Tab 4: Processing Stats

**Key metrics dashboard (Chart.js, 30-day rolling):**

1. **Processing Volume chart**: Sheets processed per day (bar chart) — peaks visible on exam days
2. **Error Rate trend**: % flagged (ambiguous + failed) per day — alert line at 5%
3. **Turnaround Time**: Avg minutes from upload to RESULTS_READY per batch (target ≤ 30 min)
4. **Processing Errors by Type**: Pie chart — Ambiguous Mark / Incomplete Fill / Multi-Mark / Low Scan Quality / Template Mismatch
5. **Institution Reliability table**: per-institution — Avg scan quality score · rejection rate · avg sheets/batch · most common error type

**Resolution SLA**: Flagged sheets must be reviewed by OMR Specialist within 2 hours of flagging during exam hours. SLA breach shown in amber after 1h.

---

## 5. OMR Template Builder

Full-page template builder (routed as `/ops/exam/omr/templates/new/` and `/ops/exam/omr/templates/<id>/edit/`).

### 5.1 Template Configuration

**Basic settings (left rail, 300px):**
- Template Name
- Sheet Size: A4 / A4 Landscape / Letter
- Questions Count (10–300)
- Options per Question: 4 / 5 (A/B/C/D/E) / Custom
- Sections (add sections with Q range: Section A: Q1–25 · Section B: Q26–50)
- Roll Number Field: Yes (N-digit) / No
- Booklet Series Field: Yes (A/B/C/D) / No — for multi-version papers
- Test Booklet Number Field: Yes (6-digit) / No
- Photo Capture Area: Yes / No (some coaching institutes require student photo on OMR)
- Special Answer Types:
  - Integer-type grid (for JEE-style 0-9 fill): specify which questions use this
  - Matching question grid: specify which questions use two-column matching
- Bubble Shape: Circle (standard) / Square / Diamond
- Bubble Size: 6mm (standard) / 8mm (for Class 5 and below — larger for children)

**Visual preview (right 70% — live rendered A4 sheet):**
Updates in real-time as settings change. Shows:
- Roll number boxes at top
- Booklet code circles
- Questions grid with bubbles
- Section dividers
- EduForge watermark (light, bottom corner)
- Calibration anchor squares at corners and midpoints (used by processing algorithm)

**[Save Template]** · **[Download Sample PDF]** · **[Test with Sample Scan]** (upload a sample scan to verify alignment works)

### 5.2 Calibration Test

After creating a template:
1. Download the sample blank sheet
2. Print it, fill some bubbles manually as test
3. Scan and upload the test scan
4. System processes it and shows detected responses
5. OMR Specialist verifies detected responses match actual filled bubbles
6. If alignment is off: adjust calibration offset parameters (fine-tune anchor detection sensitivity)

This calibration step is mandatory before the template can be marked Active.

---

## 6. Batch Review Workspace

Triggered from Tab 1 → [Review] on a REVIEW_PENDING batch.

Route: `/ops/exam/omr/batches/<batch_id>/review/`

### 6.1 Batch Header

```
Batch OMR-2026-03890 — SSC CGL Mock Test 3 — Vidya Coaching Centre
248 sheets uploaded · 236 processed · 12 flagged for review
[← Back to Dashboard]  [Reject Entire Batch]  [Mark Batch Complete]
```

### 6.2 Review Queue (left panel, 35%)

List of flagged sheets. Each row:
- Sheet thumbnail (greyscale, A4 preview)
- Student roll number (if detected) OR "Roll No. Unreadable"
- Flag reason: `AMBIGUOUS_MARK` · `MULTI_MARK` · `INCOMPLETE_SCAN` · `ROLL_NO_UNCLEAR` · `BOOKLET_MISMATCH`
- Sheet sequence number in batch (e.g. Sheet 89 of 248)
- Click to load in main review panel

### 6.3 Review Panel (right panel, 65%)

**For selected flagged sheet:**

```
Sheet 89 of 248 — Student Roll: Unreadable — Flag: AMBIGUOUS_MARK (Q47, Q83)

[High-res scan image of full OMR sheet]
─────────────────────────────────────
Zoomed panels for flagged bubbles:
  Q47: [zoomed image showing bubble almost-filled between B and C]
  Q83: [zoomed image showing faint mark on A]

OMR Specialist Resolution:
  Q47: ○ A  ○ B  ● C  ○ D  ○ Blank
  Q83: ● A  ○ B  ○ C  ○ D  ○ Blank

Roll Number: [__________]  (type manually if unreadable)

[Save & Next →]  [Mark as Invalid — Skip Sheet]
```

**Zoomed panel logic:**
- System highlights the exact bubble regions with a red rectangle
- OMR Specialist chooses the correct answer based on visual inspection
- All resolutions logged with specialist ID + timestamp + original detected value + resolved value

**Mark as Invalid — Skip Sheet:**
- This student's sheet is not processed
- Results for this student will show `OMR_INVALID` status in F-04
- Institution notified to re-administer for this student if needed
- Counted in batch summary (skipped count)

**Multi-mark resolution:**
When two bubbles are marked for the same question:
- Show both marked bubbles highlighted
- OMR Specialist selects which one was intended (often the darker/fuller mark)
- Or marks as `AMBIGUOUS_BLANK` (treated as blank/no attempt, same as unanswered)

---

## 7. Batch Detail View — `/ops/exam/omr/batches/<batch_id>/`

Full batch drill-down accessible from any batch row.

### 7.1 Summary Panel

| Metric | Value |
|---|---|
| Exam | SSC CGL Mock Test 3 |
| Institution | Vidya Coaching Centre |
| Scheduled Exam Date | 2026-03-26 09:00 IST |
| OMR Template Used | SSC-CGL-100Q-4OPT |
| Total Sheets Uploaded | 248 |
| Successfully Processed | 236 |
| Flagged (Manual Review) | 12 |
| Invalidated (Skipped) | 0 |
| Rejected Sheets | 0 |
| Upload Time | 2026-03-26 11:45 IST |
| Processing Start | 2026-03-26 11:46 IST |
| Processing Complete | 2026-03-26 11:52 IST (6 min, 2.4 sec/sheet avg) |
| Review Completed | 2026-03-26 12:31 IST |
| Results Push | — (pending) |

### 7.2 Student Response Table

| Student Roll No. | Sheet # | Q1 | Q2 | Q3 | ... | Q100 | Processing Status |
|---|---|---|---|---|---|---|---|
| SC2026-001 | 1 | A | C | B | ... | D | ✅ Clean |
| SC2026-002 | 2 | B | A | D | ... | A | ✅ Clean |
| SC2026-089 | 89 | A | C | C | ... | B | ✅ Reviewed (Q47: C, Q83: A) |

Download: [Export Responses CSV] (roll_number + all question responses)

### 7.3 Batch Quality Metrics

- Avg scan quality score (0–100, computed by OCR confidence on bubble fills)
- % ambiguous marks
- % multi-marks
- Most common error: "Q47 most flagged across sheets" (suggests poor printing of that question's bubble column)

---

## 8. OMR Processing Pipeline — Technical

The actual image processing runs as an AWS Lambda function triggered via SQS:

```
Institution Portal → Upload scans to S3 (batch_id/ folder)
                              ↓
          SQS message: {batch_id, template_id, sheet_count}
                              ↓
     Lambda: omr_processor (Node.js + Sharp + custom bubble detection)
     ┌─────────────────────────────────────────────────────────┐
     │ For each image in batch:                                 │
     │  1. Load image from S3                                  │
     │  2. Detect calibration anchors (corner squares)         │
     │  3. Perspective-correct image (removes scan skew)       │
     │  4. For each question region:                           │
     │     a. Extract bubble area pixels                       │
     │     b. Compute fill percentage per bubble (A/B/C/D)     │
     │     c. If max fill > 0.65 AND only 1 bubble > 0.65:     │
     │        → CLEAN (assign that option)                     │
     │     d. If max fill 0.35–0.65 (unclear):                 │
     │        → AMBIGUOUS_MARK (queue for human review)        │
     │     e. If 2+ bubbles > 0.65:                            │
     │        → MULTI_MARK (queue for human review)            │
     │     f. If all bubbles < 0.20:                           │
     │        → BLANK (treated as no attempt)                  │
     │  5. Roll number OCR (7-segment digit recognition)       │
     │  6. Booklet series OCR (circle detection: A/B/C/D)      │
     │  7. Write result to omr_sheet_result table              │
     └─────────────────────────────────────────────────────────┘
                              ↓
          Update batch status in DB (via SQS completion message)
          Notify OMR Specialist if flags > 0
```

**Supported file formats:** JPEG (minimum 200 DPI) · PNG · TIFF · PDF (single-page OCR split). Maximum file size: 10MB per sheet image.

**Mobile phone scanning support:** Most institutions use a flatbed scanner or phone. For phone scans, the Lambda applies additional preprocessing:
- Shadow removal
- Contrast enhancement
- Perspective distortion correction (more aggressive for phone shots)
- Noise reduction

**Failure handling:**
- If template anchor detection fails (severely misaligned or wrong template): sheet flagged as `TEMPLATE_MISMATCH`
- If image quality too low (< 50 DPI equivalent): `LOW_QUALITY`
- Both failures require human intervention (re-scan or manual entry)

---

## 9. Integration with F-04 Results Management

When OMR Specialist marks a batch as REVIEWED:

1. Celery task `push_omr_batch_to_results` fires
2. For each clean/reviewed sheet in the batch:
   - Creates `exam_submission` record in tenant schema (same model as online exam submission)
   - `submission_type = OMR`
   - Responses populated from OMR processing output
   - `submitted_at` = exam scheduled end time (standardized for fairness, not scan upload time)
3. Results Coordinator in F-04 sees this exam in their Results Management queue with status `SUBMISSIONS_READY`
4. From F-04's perspective, OMR submissions and online submissions are identical — same scoring engine runs

**Rejected sheets appear in F-04 as:**
`result_status = OMR_INVALID` with `score = null` and note "OMR sheet invalid — please re-contact institution"

---

## 10. Toasts & Notifications

| Action | Toast | Type |
|---|---|---|
| Batch upload complete | "Batch OMR-{id} received — {N} sheets. Processing started." | Info 6s |
| Processing complete | "OMR-{id} processed — {N} clean, {M} flagged for review" | Info 6s |
| Review complete | "Batch OMR-{id} review done — all flags resolved. Ready for results." | Success 4s |
| Batch rejected | "Batch OMR-{id} rejected — institution notified to re-submit" | Warning 8s |
| Sheet marked invalid | "Sheet {roll_no} marked invalid — {count} of {total} sheets invalid in this batch" | Warning 8s |
| Results pushed to F-04 | "OMR-{id} pushed to Results — Results Coordinator notified" | Success 4s |
| Processing error | "Processing failed for {N} sheets in OMR-{id} — manual review required" | Error persistent |
| SLA breach (>2h unreviewed flags) | "⚠️ {N} flagged sheets unreviewed for >2 hours in batch OMR-{id}" | Error persistent |

**In-app notifications to OMR Specialist:**
- New batch with flagged sheets: "Batch OMR-{id} has {N} flagged sheets for review"
- SLA warning at 90 minutes: "Flagged sheets in OMR-{id} approaching 2-hour review SLA"

**In-app notifications to Results Coordinator:**
- "OMR batch OMR-{id} for {exam_name} at {institution} is Results-Ready — {N} valid, {M} invalid sheets"

---

## 11. Empty States

| Scenario | Message |
|---|---|
| No active batches | "No OMR batches in progress. Batches appear when institutions upload scan files for OMR-mode exams." |
| No OMR templates | "No templates yet. Create an OMR template before scheduling OMR-mode exams." |
| No flagged sheets | "No sheets awaiting review. All batches are processing cleanly." |
| Batch processing — all clean | "All {N} sheets processed without flags. Push to Results to proceed." |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/ops/omr/batches/` | List batches (paginated, filterable) |
| GET | `/api/v1/ops/omr/batches/<id>/` | Batch detail |
| PATCH | `/api/v1/ops/omr/batches/<id>/status/` | Update batch status (review complete / reject) |
| GET | `/api/v1/ops/omr/batches/<id>/sheets/` | All sheets in batch |
| GET | `/api/v1/ops/omr/batches/<id>/sheets/flagged/` | Flagged sheets only |
| PATCH | `/api/v1/ops/omr/batches/<id>/sheets/<sheet_id>/resolve/` | Resolve flagged sheet |
| POST | `/api/v1/ops/omr/batches/<id>/push-results/` | Push to F-04 results queue |
| POST | `/api/v1/ops/omr/batches/<id>/reject/` | Reject batch (reason required) |
| GET | `/api/v1/ops/omr/templates/` | List templates |
| POST | `/api/v1/ops/omr/templates/` | Create template |
| GET | `/api/v1/ops/omr/templates/<id>/` | Template detail + preview |
| PATCH | `/api/v1/ops/omr/templates/<id>/` | Edit template |
| POST | `/api/v1/ops/omr/templates/<id>/test-scan/` | Upload test scan for calibration |
| GET | `/api/v1/ops/omr/dashboard/kpi/` | KPI strip data |
| GET | `/api/v1/ops/omr/stats/` | Processing stats (Tab 4) |

---

## 13. Database Models

```python
class OMRTemplate(models.Model):
    name              = models.CharField(max_length=100)
    sheet_size        = models.CharField(max_length=20, default='A4')  # A4/A4_LANDSCAPE/LETTER
    question_count    = models.PositiveSmallIntegerField()
    options_per_question = models.PositiveSmallIntegerField(default=4)  # 4/5/custom
    sections          = models.JSONField(default=list)  # [{name: "A", from_q: 1, to_q: 25}, ...]
    has_roll_no_field = models.BooleanField(default=True)
    roll_no_digits    = models.PositiveSmallIntegerField(default=8)
    has_booklet_series = models.BooleanField(default=False)
    has_test_booklet_no = models.BooleanField(default=False)
    integer_type_questions = models.JSONField(default=list)  # list of Q numbers using integer grid
    bubble_shape      = models.CharField(max_length=10, default='CIRCLE')
    bubble_size_mm    = models.PositiveSmallIntegerField(default=6)
    calibration_params = models.JSONField(default=dict)  # anchor detection params
    preview_url       = models.URLField(blank=True)  # R2 CDN URL of rendered preview PDF
    status            = models.CharField(max_length=10, default='DRAFT')  # DRAFT/CALIBRATED/ACTIVE/ARCHIVED
    created_by        = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at        = models.DateTimeField(auto_now_add=True)

class OMRBatch(models.Model):
    batch_id          = models.CharField(max_length=20, unique=True)  # OMR-YYYY-NNNNN
    exam_schedule_id  = models.UUIDField()  # FK to exam_schedule (F-01)
    institution_id    = models.PositiveIntegerField()
    template          = models.ForeignKey(OMRTemplate, on_delete=models.PROTECT)
    sheet_count       = models.PositiveSmallIntegerField()
    processed_count   = models.PositiveSmallIntegerField(default=0)
    flagged_count     = models.PositiveSmallIntegerField(default=0)
    invalid_count     = models.PositiveSmallIntegerField(default=0)
    status            = models.CharField(max_length=20, default='UPLOADING')
    uploaded_at       = models.DateTimeField(null=True)
    processing_start  = models.DateTimeField(null=True)
    processing_end    = models.DateTimeField(null=True)
    review_start      = models.DateTimeField(null=True)
    review_end        = models.DateTimeField(null=True)
    results_pushed_at = models.DateTimeField(null=True)
    rejection_reason  = models.TextField(blank=True)
    s3_folder_key     = models.CharField(max_length=200)  # S3 folder containing scan files
    avg_scan_quality  = models.DecimalField(max_digits=5, decimal_places=2, null=True)  # 0-100
    reviewed_by       = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

class OMRSheetResult(models.Model):
    batch             = models.ForeignKey(OMRBatch, related_name='sheets', on_delete=models.PROTECT)
    sheet_sequence    = models.PositiveSmallIntegerField()
    roll_number       = models.CharField(max_length=20, blank=True)
    booklet_series    = models.CharField(max_length=2, blank=True)  # A/B/C/D
    scan_file_key     = models.CharField(max_length=200)  # S3 key of this sheet's scan
    processing_status = models.CharField(max_length=20)  # CLEAN/REVIEW_PENDING/REVIEWED/INVALID/FAILED
    responses         = models.JSONField(default=dict)  # {q_no: detected_option, ...}
    reviewed_responses = models.JSONField(default=dict)  # overridden by OMR Specialist
    flags             = models.JSONField(default=list)  # [{q_no: 47, reason: "AMBIGUOUS_MARK", ...}]
    scan_quality_score = models.PositiveSmallIntegerField(null=True)
    reviewed_by       = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    reviewed_at       = models.DateTimeField(null=True)
    processed_at      = models.DateTimeField(null=True)

class OMRBatchLog(models.Model):
    """Immutable audit trail for all OMR batch actions."""
    batch             = models.ForeignKey(OMRBatch, on_delete=models.PROTECT)
    action            = models.CharField(max_length=50)
    detail            = models.JSONField(default=dict)
    performed_by      = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    performed_at      = models.DateTimeField(auto_now_add=True)
```

---

## 14. HTMX Patterns

```
Dashboard KPI (60s refresh)
  → hx-get="/api/v1/ops/omr/dashboard/kpi/" hx-target="#omr-kpi"
    hx-trigger="every 60s" hx-swap="innerHTML"

Active Batches table (60s refresh while any batch in PROCESSING status)
  → hx-get="/ops/exam/omr/tab/active-batches/" hx-target="#active-batches-table"
    hx-trigger="every 60s" hx-swap="innerHTML"
  → Pause trigger: if no PROCESSING batches, pause to "every 300s"

Review workspace — Sheet navigation
  → hx-get="/ops/exam/omr/batches/<id>/sheets/<sheet_id>/"
    hx-target="#sheet-review-panel" hx-swap="innerHTML"
    hx-trigger="click from:.sheet-list-row, keydown[key=='ArrowDown'] from:body"

Save resolution + load next
  → hx-patch="/api/v1/ops/omr/batches/<id>/sheets/<sheet_id>/resolve/"
    hx-target="#sheet-review-panel"
    hx-swap="innerHTML"
    hx-vals="js:{responses: collectResolutions(), roll_number: rollInput.value}"
    hx-on::after-request="loadNextSheet()"

Batch reject confirmation modal
  → After type-in confirmation:
    hx-post="/api/v1/ops/omr/batches/<id>/reject/"
    hx-target="closest tr" hx-swap="outerHTML"
    hx-vals="js:{reason: rejectReason.value}"

Push to Results
  → hx-post="/api/v1/ops/omr/batches/<id>/push-results/"
    hx-confirm="Push {N} processed sheets to F-04 Results Management? This cannot be undone."
    hx-target="closest tr" hx-swap="outerHTML"
```

---

## 15. Performance & Scaling

- OMR processing Lambda: 3–5 seconds per sheet (depends on scan quality) → 100-sheet batch = ~5–8 min total
- Lambda concurrency: max 20 concurrent OMR processing functions (below exam-submission Lambda priority)
- On peak exam days (exam day mode active), OMR processing Lambda concurrency reduced to 10 to protect exam submission throughput
- Batch review sessions: no heavy DB queries — sheet data is pre-loaded when batch enters REVIEW_PENDING
- Sheet image delivery: served via CloudFront CDN with signed URLs (5-min expiry per sheet, renewable while drawer open)
- Database: OMRSheetResult rows are small (< 500 bytes each) — 50,000 sheets/day = 25MB/day, well within capacity
- Retention: scan images purged from S3 after 90 days (results data retained per institution's standard retention policy)

---

## 16. Security Considerations

- Scan images: stored in private S3 bucket under `omr-scans/<batch_id>/` — signed URLs only, never public CDN
- Roll number data: treated as student PII — visible to OMR Specialist and Exam Ops Manager only; Results Coordinator sees aggregated counts
- Batch logs: append-only; no update or delete routes in the API
- Resolution audit: every manual override by OMR Specialist logged with original detected value — prevents undetected data manipulation
- Institution notification on rejection: automated, logged — institution receives reason code (not internal technical details)

---

*Page spec version: 1.0 · Created: 2026-03-26 · Division F — Exam Day Operations*
*Indian Education Addition: OMR processing is critical for SSC/NEET/JEE mock exams in coaching institutes and for government schools that cannot conduct fully digital exams due to connectivity constraints*
