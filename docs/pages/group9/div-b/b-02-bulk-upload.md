# B-02 — Bulk Upload

> **URL:** `/content-partner/author/bulk-upload`
> **File:** `b-02-bulk-upload.md`
> **Priority:** P1
> **Roles:** Content Partner · EduForge Editorial Team (review queue)

---

## Overview

The Bulk Upload module allows content partners to upload large batches of questions via CSV or Excel files, significantly accelerating content ingestion compared to one-at-a-time authoring. Dr. Venkat Rao regularly uses this feature to upload sets of 200-500 quantitative aptitude questions he has prepared offline in spreadsheet format. The system validates every row against schema rules, flags errors with row-level detail, and provides real-time progress tracking for uploads that may take several minutes to process.

---

## Mockup 1 — Bulk Upload Landing & File Selection

```
+------------------------------------------------------------------+
| EduForge Content Partner Portal                   Dr. Venkat Rao  |
+------------------------------------------------------------------+
| Dashboard > Author > Bulk Upload                                  |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------------------------------------------------+  |
|  | BULK UPLOAD — Questions                                     |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  |  Step 1 of 3: Select File                                   |  |
|  |                                                             |  |
|  |  +------------------------------------------------------+  |  |
|  |  |                                                       |  |  |
|  |  |          Drag & drop your CSV or Excel file           |  |  |
|  |  |                   here, or click                      |  |  |
|  |  |                                                       |  |  |
|  |  |             [ Browse Files... ]                       |  |  |
|  |  |                                                       |  |  |
|  |  |  Accepted: .csv, .xlsx (max 10 MB, max 2000 rows)    |  |  |
|  |  |                                                       |  |  |
|  |  +------------------------------------------------------+  |  |
|  |                                                             |  |
|  |  [Download CSV Template]  [Download Excel Template]         |  |
|  |  [View Column Guide]                                        |  |
|  |                                                             |  |
|  |  TEMPLATE COLUMNS (15 required + 3 optional):               |  |
|  |  +------------------------------------------------------+  |  |
|  |  | #  | Column Name     | Required | Example            |  |  |
|  |  |----|-----------------|----------|--------------------|  |  |
|  |  | 1  | exam            | Yes      | SSC CGL            |  |  |
|  |  | 2  | subject         | Yes      | Quantitative Apt.  |  |  |
|  |  | 3  | topic           | Yes      | Number Systems     |  |  |
|  |  | 4  | sub_topic       | Yes      | HCF & LCM         |  |  |
|  |  | 5  | question_type   | Yes      | MCQ_SINGLE         |  |  |
|  |  | 6  | question_text   | Yes      | Find the HCF of..  |  |  |
|  |  | 7  | option_a        | Yes*     | 12                 |  |  |
|  |  | 8  | option_b        | Yes*     | 18                 |  |  |
|  |  | 9  | option_c        | Yes*     | 24                 |  |  |
|  |  | 10 | option_d        | Yes*     | 36                 |  |  |
|  |  | 11 | correct_option  | Yes      | A                  |  |  |
|  |  | 12 | explanation     | Yes      | HCF of 48 and...  |  |  |
|  |  | 13 | difficulty      | Yes      | 3                  |  |  |
|  |  | 14 | expected_time   | Yes      | 90                 |  |  |
|  |  | 15 | language        | Yes      | English            |  |  |
|  |  | 16 | source          | No       | Original           |  |  |
|  |  | 17 | pyq_year        | No       | 2024               |  |  |
|  |  | 18 | tags            | No       | HCF;LCM;Numbers    |  |  |
|  |  +------------------------------------------------------+  |  |
|  |  * option_a to option_d required for MCQ types only         |  |
|  |                                                             |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  RECENT UPLOADS:                                                  |
|  +------------------------------------------------------------+  |
|  | File Name            | Date       | Rows | Status          |  |
|  |----------------------|------------|------|-----------------|  |
|  | appsc_maths_mar.csv  | 2026-03-28 |  312 | Completed (4e)  |  |
|  | ssc_quant_feb.xlsx   | 2026-02-15 |  487 | Completed (0e)  |  |
|  | ibps_reason_jan.csv  | 2026-01-20 |  198 | Completed (12e) |  |
|  +------------------------------------------------------------+  |
|                                                                   |
+------------------------------------------------------------------+
```

---

## Mockup 2 — Validation Results & Error Detail

```
+------------------------------------------------------------------+
| BULK UPLOAD — Validation Results                                  |
+------------------------------------------------------------------+
|                                                                   |
|  Step 2 of 3: Review Validation                                   |
|                                                                   |
|  File: appsc_quant_apr_2026.csv                                   |
|  Total Rows: 250 | Valid: 237 | Errors: 13 | Warnings: 5         |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | VALIDATION SUMMARY                                          |  |
|  |                                                             |  |
|  |  [####################################----]  94.8% valid    |  |
|  |                                                             |  |
|  |  Errors (must fix before upload):                           |  |
|  |  - 6 rows: Missing correct_option                           |  |
|  |  - 3 rows: Invalid difficulty (must be 1-5)                 |  |
|  |  - 2 rows: Unknown topic for given subject                  |  |
|  |  - 1 row:  question_text exceeds 2000 chars                 |  |
|  |  - 1 row:  Duplicate of existing question (QID: 847291)     |  |
|  |                                                             |  |
|  |  Warnings (upload allowed but review flagged):              |  |
|  |  - 3 rows: expected_time below 30s (unusually fast)         |  |
|  |  - 2 rows: LaTeX expression may not render (unmatched $)    |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | ERROR DETAIL (Row-by-Row)                      [Export CSV] |  |
|  |                                                             |  |
|  | Row | Column          | Value      | Error                 |  |
|  |-----|-----------------|------------|-----------------------|  |
|  | 14  | correct_option  | (empty)    | Required field        |  |
|  | 14  | difficulty      | 7          | Must be 1-5           |  |
|  | 28  | correct_option  | (empty)    | Required field        |  |
|  | 45  | topic           | Algebrra   | Unknown topic; did    |  |
|  |     |                 |            | you mean "Algebra"?   |  |
|  | 67  | correct_option  | (empty)    | Required field        |  |
|  | 89  | question_text   | (2145 ch.) | Max 2000 characters   |  |
|  | 102 | correct_option  | (empty)    | Required field        |  |
|  | 115 | difficulty      | 0          | Must be 1-5           |  |
|  | 130 | topic           | Trigo      | Unknown topic; did    |  |
|  |     |                 |            | you mean "Trigon..."? |  |
|  | 155 | correct_option  | (empty)    | Required field        |  |
|  | 178 | difficulty      | -1         | Must be 1-5           |  |
|  | 201 | correct_option  | (empty)    | Required field        |  |
|  | 223 | question_text   | (dup)      | Duplicate QID 847291  |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  [ Download Error Report ]                                        |
|  [ Upload Valid Rows Only (237) ]  [ Fix & Re-upload All ]        |
|                                                                   |
+------------------------------------------------------------------+
```

---

## Mockup 3 — Upload Progress & Completion Summary

```
+------------------------------------------------------------------+
| BULK UPLOAD — Processing                                          |
+------------------------------------------------------------------+
|                                                                   |
|  Step 3 of 3: Upload Progress                                     |
|                                                                   |
|  File: appsc_quant_apr_2026.csv                                   |
|  Uploading 237 valid questions...                                  |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | PROGRESS                                                    |  |
|  |                                                             |  |
|  |  [########################-----------]  168/237  (70.9%)    |  |
|  |                                                             |  |
|  |  Elapsed: 1m 42s | Estimated remaining: 0m 41s              |  |
|  |                                                             |  |
|  |  Current: Row 168 — "If the ratio of two numbers is 3:5    |  |
|  |           and their HCF is 4, find their LCM..."           |  |
|  |                                                             |  |
|  |  Processing stages per row:                                 |  |
|  |  [x] Parse & validate         (done)                        |  |
|  |  [x] Deduplication check      (done)                        |  |
|  |  [x] LaTeX rendering test     (done)                        |  |
|  |  [ ] Store to question bank   (in progress)                 |  |
|  |  [ ] Index for search         (pending)                     |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | UPLOAD LOG (live)                                           |  |
|  |                                                             |  |
|  |  09:42:15  Row 165 — QID VR-2026-18321 created             |  |
|  |  09:42:16  Row 166 — QID VR-2026-18322 created             |  |
|  |  09:42:16  Row 167 — QID VR-2026-18323 created (warn: low  |  |
|  |                       expected_time 25s)                     |  |
|  |  09:42:17  Row 168 — Processing...                          |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  [ Cancel Upload ]                                                |
|                                                                   |
|  --- After completion: ---                                        |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | UPLOAD COMPLETE                                             |  |
|  |                                                             |  |
|  |  Total processed:  237                                      |  |
|  |  Successfully created: 235                                  |  |
|  |  Failed during insert:   2 (network timeout, queued retry)  |  |
|  |  Batch ID: BATCH-VR-2026-0331-001                           |  |
|  |  Status: Submitted for Review                               |  |
|  |                                                             |  |
|  |  QID Range: VR-2026-18154 to VR-2026-18390                  |  |
|  |  Dr. Venkat Rao's Total Pool: 18,500 + 235 = 18,735        |  |
|  |                                                             |  |
|  |  [ View Uploaded Questions ]  [ Download Receipt ]          |  |
|  |  [ Start New Upload ]                                       |  |
|  +------------------------------------------------------------+  |
|                                                                   |
+------------------------------------------------------------------+
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/content-partner/author/bulk-upload/template` | Download CSV or Excel template with headers and sample rows |
| POST | `/api/v1/content-partner/author/bulk-upload/validate` | Upload file for validation only (returns row-level errors) |
| POST | `/api/v1/content-partner/author/bulk-upload` | Upload and process validated file (creates questions) |
| GET | `/api/v1/content-partner/author/bulk-upload/{batch_id}` | Get status and progress of a bulk upload batch |
| GET | `/api/v1/content-partner/author/bulk-upload/{batch_id}/errors` | Get detailed error report for a batch |
| POST | `/api/v1/content-partner/author/bulk-upload/{batch_id}/retry` | Retry failed rows within a batch |
| DELETE | `/api/v1/content-partner/author/bulk-upload/{batch_id}` | Cancel an in-progress upload or delete a completed batch record |
| GET | `/api/v1/content-partner/author/bulk-upload/history` | List all past bulk uploads for the logged-in partner |
| GET | `/api/v1/content-partner/author/bulk-upload/{batch_id}/receipt` | Download a PDF receipt summarizing the upload results |

---

## Business Rules

1. The bulk upload system enforces a maximum file size of 10 MB and a maximum of 2,000 rows per upload to ensure server stability and predictable processing times. Files exceeding either limit are rejected at the upload stage before any validation begins. The system accepts CSV files encoded in UTF-8 (with or without BOM) and Excel files in .xlsx format only; legacy .xls files are not supported due to security concerns with the older binary format. Column headers must exactly match the template specification (case-insensitive), and any unrecognized columns are silently ignored rather than causing a rejection, which allows partners like Dr. Venkat Rao to maintain additional personal columns (such as his own internal numbering scheme) in their spreadsheets without needing to strip them before upload. The first row is always treated as the header row, and completely empty rows are skipped during processing.

2. Validation runs as a two-phase process: structural validation checks column presence, data types, and value ranges (difficulty 1-5, expected_time 15-600 seconds, language in the allowed set), while semantic validation checks referential integrity against EduForge's master data (exam names, subject-topic-subtopic hierarchy, question type codes). When a topic name has a Levenshtein distance of 2 or fewer from a known topic, the system suggests the correction in the error report rather than simply rejecting the row, because partners frequently make minor spelling mistakes when typing topic names in spreadsheets without autocomplete assistance. Duplicate detection compares the normalized question text (stripped of whitespace and punctuation) against all questions in the partner's own pool and a sample of the global pool using a trigram similarity threshold of 0.85, and flagged duplicates are treated as errors that block upload unless the partner explicitly acknowledges them by setting a force_duplicate flag on the re-upload request.

3. Upload processing is handled asynchronously via a background task queue (Celery with Redis broker) to avoid HTTP request timeouts for large batches. When the partner initiates the upload, the API immediately returns a batch ID and a WebSocket channel URL for real-time progress updates. The client subscribes to this channel and receives events for each row processed, including the assigned question ID, any warnings, and the running success/failure count. If the partner closes the browser during upload, the processing continues on the server and the completion status is visible on the next login. Failed rows due to transient errors (database timeouts, storage service unavailability) are automatically retried up to 3 times with exponential backoff, and only after all retries are exhausted is the row marked as failed. Partners can trigger a manual retry for failed rows without re-uploading the entire file, and the system preserves the original row numbers so the partner can cross-reference errors against their source spreadsheet.

4. Upon successful completion of a bulk upload, all questions in the batch are assigned a status of "submitted" and enter the editorial review queue as a single batch unit rather than as individual questions. This batch grouping allows the editorial team to review Dr. Venkat Rao's 237-question upload as a coherent set, applying consistent quality standards across the entire batch and spotting patterns such as repeated difficulty levels or missing topic coverage. The batch receipt PDF includes a summary table with question counts by subject and topic, difficulty distribution histogram data, and the partner's running total contribution to the EduForge pool. If the editorial team rejects more than 20 percent of questions in a batch, the entire batch is flagged for partner revision with a consolidated feedback report, because high rejection rates typically indicate a systemic issue with the source material (wrong template version, misunderstood topic taxonomy) that the partner should address holistically rather than fixing individual questions in isolation.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division B*
