# Page 20: Scholarship Exam Results

**URL:** `/group/adm/scholarship-exam/results/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions · Scholarship Section

---

## 1. Purpose

The Scholarship Exam Results page manages the complete post-exam pipeline from raw score upload to final published results. After a scholarship exam is physically or digitally conducted across multiple branches, the Scholarship Exam Manager uploads answer sheets or OMR scan data, finalises the answer key (resolving any objections raised by candidates), computes scores, runs rank computation across all branches simultaneously, and ultimately publishes results to candidates. This pipeline must be executed carefully — errors in answer key finalisation or score computation directly affect scholarship award eligibility and can trigger disputes.

Moderation is mandatory before publication. Once results are uploaded and an answer key is finalised, a moderation step requires the Director or the Exam Manager to review the computed scores, check for statistical anomalies (unusually high/low branch averages, suspiciously identical scores), and confirm no technical errors exist in the upload. Moderation produces an audit log entry. Only after moderation is completed can results be published. Published results feed automatically into the Scholarship Manager's approval queue, where auto-recommendations are generated for candidates meeting scheme cut-offs.

The re-evaluation request module allows candidates (via their branch) to flag specific questions or their computed score for review. These objections are tracked and resolved before result finalisation. The Answer Key Manager additionally handles question-level objections raised during or after the exam — where a question may have been ambiguous or incorrectly typed. Accepting an objection updates the answer key and triggers automatic recomputation of affected candidates' scores.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Exam Manager (26) | G3 | Full — upload, moderate, key management, publish | Primary operator |
| Group Admissions Director (23) | G3 | View all + approve publication | Cannot upload or edit keys |
| Group Scholarship Manager (27) | G3 | View published results only | To identify scholarship candidates |
| Chief Academic Officer | G2 | View published results | Read-only |
| Group Admission Coordinator (24) | G3 | No access | Excluded |

**Enforcement:** Upload, key management, and moderation endpoints require JWT with `function == scholarship_exam` and `role == scholarship_exam_manager`. Publication requires either Exam Manager or Director approval via a two-step confirmation. The Scholarship Manager's view is filtered to `status = published` only at the Django queryset level.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarship Exams → Results
```

### 3.2 Page Header
- **Title:** Scholarship Exam Results
- **Subtitle:** Upload, moderate, and publish scholarship exam results
- **Action Buttons:** `[Upload Results →]` (Exam Manager only) · `[Export Results PDF]`

### 3.3 Alert Banner
Triggers:
- **Red — Exams Awaiting Upload (>7 days since conduct):** "Results for {Exam Name} are overdue. Exam was conducted {n} days ago. [Upload Now →]"
- **Amber — Moderation Required:** "{Exam Name} results uploaded and awaiting moderation before publication. [Moderate →]"
- **Amber — Open Re-evaluation Requests:** "{n} re-evaluation requests are unresolved. [Review →]"
- **Green — Results Published:** "Results for {Exam Name} published. {n} scholarship auto-recommendations generated."
- **Blue — Recomputation in Progress:** "Score recomputation in progress after answer key update. Do not publish until complete."

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Exams Pending Result Upload | COUNT of exams with status = 'conducted' and no result record | `scholarship_exam` + `exam_result` | Red > 0 · Green = 0 | → Section 5.1 |
| Results Uploaded (Awaiting Moderation) | COUNT of result records with status = 'uploaded' | `exam_result` table | Amber > 0 · Green = 0 | → Section 5.2 |
| Results Moderated (Awaiting Publication) | COUNT of result records with status = 'moderated' | `exam_result` table | Amber > 0 · Green = 0 | → Section 5.2 |
| Results Published | COUNT of result records with status = 'published' | `exam_result` table | Green always | → published results list |
| Toppers Identified | COUNT of distinct candidates with rank ≤ 10 across published results | `exam_result_candidate` | Blue always | → Section 5.6 topper analysis |
| Scholarships Auto-Recommended | COUNT of auto-recommendations generated from published results | `scholarship_recommendation` | Green > 0 · Blue = 0 | → Scholarship Approval page |

**HTMX Refresh:** Every 5 minutes via `hx-trigger="every 5m"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Result Upload Queue

**Display:** Table — conducted exams with no uploaded results. Sorted by exam_date ASC (oldest first).

**Columns:**

| Column | Notes |
|---|---|
| Exam Name | Linked |
| Date Conducted | DD-MMM-YYYY |
| Branches | Count |
| Candidates | Total registered who appeared |
| Upload Status | Not Started (grey) / In Progress (blue) / Partial (amber — some branches uploaded) |
| Answer Key Status | Not Set (red) / Draft (amber) / Finalized (green) |
| Actions | `[Upload Results →]` · `[Finalize Answer Key →]` |

**HTMX Pattern:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/results/upload-queue/` targeting `#upload-queue-table`.

**Empty State:** No pending uploads. Icon: check-circle. Heading: "All Results Uploaded". Description: "No conducted exams are waiting for result upload."

---

### 5.2 Results Under Moderation

**Display:** Table — result records with status in ('uploaded', 'moderated') awaiting final publication.

**Columns:**

| Column | Notes |
|---|---|
| Exam | Exam name + date |
| Uploaded by | Staff name |
| Upload Date | DD-MMM-YYYY HH:MM |
| Candidates | Total candidates in result |
| Score Range | Min – Max (e.g., 12 – 98) |
| Re-evaluation Requests | Count — linked to Section 5.6 |
| Actions | `[Moderate →]` (opens moderation-drawer) · `[Publish →]` (only if status = moderated) |

**Empty State:** No results under moderation. Heading: "No Results Pending Moderation."

---

### 5.3 Result Details View

**Display:** Appears when an exam is selected from Section 5.2 (or from a published results list). Sub-table — one row per candidate. Server-side paginated (20/page).

**Columns:**

| Column | Notes |
|---|---|
| Rank (Group-wide) | Computed rank across all branches combined |
| Roll No | Candidate's roll number |
| Candidate Name | Full name |
| Branch | Branch where appeared |
| Total Score | Numeric |
| Subject-wise Scores | Per-subject columns (dynamic — based on exam subjects) |
| % | Percentage |
| Grade | A+ / A / B / C / D / F |
| Scholarship Eligible? | Yes (green) / No (grey) — based on scheme cut-offs |
| Actions | `[View →]` (opens result-detail-drawer) |

**Filters:** Branch (multi-select), Score range (from–to), Scholarship Eligible (Yes/No/All), Grade

**Empty State:** Select an exam to view result details.

---

### 5.4 Answer Key Manager

**Display:** For a selected exam — table of all questions in the paper.

**Columns:** Question # · Question Text (truncated) · Correct Option (A/B/C/D or Integer) · Objection Count · Objection Status (None/Open/Accepted/Rejected) · `[Accept Objection → Update Key]`

**Accepting an Objection:** Opens an inline confirmation + new correct answer field. On confirm → `hx-post` to update key → triggers background score recomputation.

**Lock Button:** `[Lock Answer Key]` — once locked, no further edits; required before moderation can be completed.

**HTMX Pattern:** `hx-trigger="change"` on exam selector → `GET /api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/answer-key/` targeting `#answer-key-table`.

**Empty State:** No exam selected or answer key not yet created.

---

### 5.5 Publication Control

**Display:** Wizard-style step bar for selected exam — sequential steps that must be completed in order.

**Steps:**
1. Answer Key Finalized ✓ / Pending
2. Scores Computed ✓ / Pending
3. Moderation Complete ✓ / Pending
4. `[Compute Final Ranks]` — button active after step 3
5. `[Preview Toppers List]` — active after rank computation
6. `[Publish Results]` — active after preview confirmation (requires Director acknowledgement)
7. `[Notify Candidates via WhatsApp]` — active after publication

**HTMX Pattern:** Each button posts to its respective endpoint. After each action, step bar refreshes via `hx-trigger="htmx:afterRequest"`.

**Empty State (no exam selected):** "Select a result from the moderation table to use Publication Control."

---

### 5.6 Re-evaluation Requests

**Display:** Table — candidates who submitted re-evaluation requests.

**Columns:**

| Column | Notes |
|---|---|
| Candidate Name | Full name |
| Branch | Branch name |
| Roll No | Roll number |
| Subject | Subject of concern |
| Question # | Specific question if applicable |
| Reason | Text summary |
| Status | Pending (amber) / Accepted (green) / Rejected (red) |
| Actions | `[Review →]` |

**HTMX Pattern:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/re-evaluations/`.

**Empty State:** No re-evaluation requests. Icon: inbox. Heading: "No Re-evaluation Requests."

---

## 6. Drawers & Modals

### 6.1 Result Detail Drawer
- **Width:** 560px
- **Trigger:** `[View →]` in Section 5.3
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/candidates/{candidate_id}/detail/`
- **Content:** Full scorecard — candidate name, roll no, branch, rank, total score, subject-wise score breakdown table, grade, scholarship eligibility status. Timeline of events (appeared, scored, rank computed, published).
- **Footer:** `[Download Scorecard PDF]` · `[Close]`

### 6.2 Moderation Drawer
- **Width:** 640px
- **Trigger:** `[Moderate →]` in Section 5.2
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/moderate/`
- **Content:** Score statistics summary (mean, median, SD per subject), anomaly flags (e.g., "Branch A avg 78% vs group avg 52%"), moderator notes text area, checklist of moderation criteria (answer key locked, score range plausible, no duplicate roll numbers, re-evaluations resolved). `[Complete Moderation]` button — records moderator name + timestamp.
- **Submit:** `hx-post` → `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/moderate/complete/` · updates result status to 'moderated'

### 6.3 Answer Key Objection Review Drawer
- **Width:** 480px
- **Trigger:** `[Accept Objection → Update Key]` in Section 5.4
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/answer-key/objection/{objection_id}/`
- **Content:** Full question text + options, original correct answer, objecting candidate names + reasons, updated correct answer selector, moderator note. `[Accept — Update Key]` / `[Reject Objection]` buttons.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Results uploaded successfully | "Results uploaded for {Exam Name}. {n} candidate records imported." | Success | 4 s |
| Results upload failed | "Upload failed: {reason}. Check file format and retry." | Error | 6 s |
| Answer key locked | "Answer key locked for {Exam Name}. No further edits allowed." | Info | 4 s |
| Objection accepted, key updated | "Objection accepted. Answer key updated. Scores being recomputed." | Warning | 5 s |
| Objection rejected | "Objection rejected. Original answer retained." | Info | 3 s |
| Moderation completed | "Moderation completed by {name}. Results ready for publication." | Success | 4 s |
| Ranks computed | "Final ranks computed for {n} candidates across {b} branches." | Success | 4 s |
| Results published | "Results for {Exam Name} published. {n} candidates notified." | Success | 5 s |
| WhatsApp notification sent | "Candidate notifications dispatched to {n} candidates via WhatsApp." | Success | 4 s |
| Re-evaluation resolved | "Re-evaluation request for {Candidate Name} resolved — {status}." | Success | 3 s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No conducted exams pending upload | Check-circle icon | "No Results Pending Upload" | "All conducted exam results have been uploaded." | None |
| No results under moderation | Check-shield icon | "Nothing to Moderate" | "All uploaded results have been moderated." | None |
| No re-evaluation requests | Inbox icon | "No Re-evaluation Requests" | "No candidates have submitted re-evaluation requests." | None |
| No exam selected (Result Details) | Select icon | "Select an Exam" | "Choose an exam from the moderation table to view detailed results." | None |
| No candidates match filters | Filter-x icon | "No Candidates Match Filters" | "Adjust filter criteria to see results." | `[Clear Filters]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | KPI shimmer (6 cards) + section skeletons |
| KPI auto-refresh | In-place spinner per card |
| Upload queue table load | Table skeleton (5 row shimmer) |
| Moderation table load | Table skeleton (3 row shimmer) |
| Result details table load (exam select) | Table skeleton (10 row shimmer) with column headers |
| Answer key table load | Table skeleton (variable rows) |
| Re-evaluation table load | Table skeleton (5 row shimmer) |
| Moderation drawer open | 640px drawer skeleton with statistics shimmer |
| Result detail drawer open | 560px drawer skeleton with score breakdown table shimmer |
| Objection review drawer open | 480px drawer skeleton |
| Rank computation in progress | Full section overlay with spinner + "Computing ranks…" |
| WhatsApp dispatch | Progress bar with "Sending {n}/{total}" live counter |

---

## 10. Role-Based UI Visibility

| Element | Exam Manager (26) | Director (23) | Scholarship Manager (27) | CAO | Coordinator (24) |
|---|---|---|---|---|---|
| `[Upload Results →]` button | Visible | Hidden | Hidden | Hidden | No access |
| Section 5.1 Upload Queue | Visible | Visible | Hidden | Hidden | No access |
| Section 5.2 Moderation table | Visible | Visible | Hidden | Hidden | No access |
| `[Moderate →]` button | Visible | Hidden | Hidden | Hidden | No access |
| `[Publish →]` button | Visible | Visible (approve) | Hidden | Hidden | No access |
| Section 5.3 Result Details | Visible (all) | Visible (all) | Visible (published only) | Visible (published) | No access |
| Section 5.4 Answer Key Manager | Visible (full) | Visible (read) | Hidden | Hidden | No access |
| `[Accept Objection]` button | Visible | Hidden | Hidden | Hidden | No access |
| Section 5.5 Publication Control | Visible (all steps) | Visible (approve step) | Hidden | Hidden | No access |
| Section 5.6 Re-evaluation | Visible (full) | Visible (read) | Hidden | Hidden | No access |
| `[Export Results PDF]` | Visible | Visible | Visible | Visible | No access |

*All UI visibility decisions made server-side in Django template. No client-side JS role checks.*

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/results/kpis/` | JWT G3 | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/results/upload-queue/` | JWT G3 | Upload queue table |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/upload/` | JWT G3 write | Upload result file |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/results/moderation-list/` | JWT G3 | Moderation table |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/candidates/` | JWT G3 | Paginated result detail |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/candidates/{candidate_id}/detail/` | JWT G3 | Result detail drawer fragment |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/answer-key/` | JWT G3 | Answer key table |
| PUT | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/answer-key/` | JWT G3 write | Update answer key |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/answer-key/lock/` | JWT G3 write | Lock answer key |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/answer-key/objection/{objection_id}/` | JWT G3 | Objection review drawer |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/answer-key/objection/{objection_id}/accept/` | JWT G3 write | Accept objection |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/answer-key/objection/{objection_id}/reject/` | JWT G3 write | Reject objection |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/moderate/` | JWT G3 | Moderation drawer fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/moderate/complete/` | JWT G3 write | Complete moderation |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/compute-ranks/` | JWT G3 write | Compute final ranks |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/publish/` | JWT G3 write | Publish results |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/notify-candidates/` | JWT G3 write | WhatsApp notifications |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/re-evaluations/` | JWT G3 | Re-evaluation requests table |
| PUT | `/api/v1/group/{group_id}/adm/scholarship-exam/results/{exam_id}/re-evaluations/{req_id}/` | JWT G3 write | Resolve re-evaluation request |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `.../results/kpis/` | `#kpi-bar` | `innerHTML` |
| Load upload queue | `load` on section | GET `.../results/upload-queue/` | `#upload-queue-table` | `innerHTML` |
| Load moderation list | `load` on section | GET `.../results/moderation-list/` | `#moderation-table` | `innerHTML` |
| Filter result details table | `change` on filters | GET `.../results/{exam_id}/candidates/?{filters}` | `#result-details-table-body` | `innerHTML` |
| Paginate result details | `click` on page link | GET `.../results/{exam_id}/candidates/?page={n}` | `#result-details-table-container` | `innerHTML` |
| Open result detail drawer | `click` on `[View →]` | GET `.../results/{exam_id}/candidates/{id}/detail/` | `#drawer-container` | `innerHTML` |
| Load answer key for exam | `change` on exam selector | GET `.../results/{exam_id}/answer-key/` | `#answer-key-table` | `innerHTML` |
| Accept answer key objection | `click` on `[Accept Objection]` | GET `.../results/{exam_id}/answer-key/objection/{id}/` | `#drawer-container` | `innerHTML` |
| Submit objection accept | `click` on `[Accept — Update Key]` | POST `.../results/{exam_id}/answer-key/objection/{id}/accept/` | `#answer-key-table` | `innerHTML` |
| Lock answer key | `click` on `[Lock Answer Key]` | POST `.../results/{exam_id}/answer-key/lock/` | `#publication-steps` | `innerHTML` |
| Open moderation drawer | `click` on `[Moderate →]` | GET `.../results/{exam_id}/moderate/` | `#drawer-container` | `innerHTML` |
| Submit moderation complete | `click` on `[Complete Moderation]` | POST `.../results/{exam_id}/moderate/complete/` | `#publication-steps` | `innerHTML` |
| Compute final ranks | `click` on `[Compute Final Ranks]` | POST `.../results/{exam_id}/compute-ranks/` | `#publication-steps` | `innerHTML` |
| Publish results | `click` on `[Publish Results]` | POST `.../results/{exam_id}/publish/` | `#publication-steps` | `innerHTML` |
| Notify candidates | `click` on `[Notify Candidates via WhatsApp]` | POST `.../results/{exam_id}/notify-candidates/` | `#publication-steps` | `innerHTML` |
| Load re-evaluation table | `load` on section | GET `.../results/{exam_id}/re-evaluations/` | `#re-evaluation-table` | `innerHTML` |
| Refresh re-evaluation after resolve | `htmx:afterRequest` from resolve call | GET `.../results/{exam_id}/re-evaluations/` | `#re-evaluation-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
