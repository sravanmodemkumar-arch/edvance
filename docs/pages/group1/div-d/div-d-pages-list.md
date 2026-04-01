# Group 1 — Division D: Content & Academics — Pages Reference

> **Division:** D — Content & Academics
> **Roles:** Content Director (18) · SME ×9 subjects (19–27) · Question Reviewer (28) · Question Approver (29) · Notes Editor (30)
> **Base URL prefix:** `/content/`
> **Access Level:** Level 2 (Content Manager — create, edit, approve content)
> **Status key:** ✅ Spec done · 🔨 In progress · ⬜ Not started

---

## Architectural Context — Why This Division Exists

Content is the core product of EduForge. Not the platform, not the infrastructure — the question bank. Every student interaction — every exam, every test series, every mock — depends entirely on the quality and integrity of Division D's output. A wrong published question does not fail one student. It fails every student across every institution that uses that question simultaneously.

The division operates a precision two-gate quality pipeline:

```
SME Authors → Reviewer Validates → Approver Publishes
```

No shortcut exists. No override is possible. No role other than the Question Approver (Role 29) can publish an MCQ — enforced at model layer, not just UI layer.

---

## Scale Context

| Dimension | Value | Implication for Content |
|---|---|---|
| Schools | 1,000 institutions · 200–5,000 students each · avg ~1,000 | ~1M school students needing Board-aligned question sets |
| Colleges (Intermediate) | 800 institutions · 150–2,000 students · avg ~500 | ~400K students; SSC/RRB/State Board overlap |
| Institution Groups | 150 groups · 5–50 colleges/schools each | Content access must respect group-level licensing |
| Coaching Centres | 100 institutions · 5,000–15,000 members · avg ~10,000 | ~1M coaching students; premium exclusive content required |
| **Total students** | **2.4M (avg) → 7.6M (max)** | Questions must never repeat across test series at this scale |
| Peak concurrent exam | **74,000 simultaneous submissions** | 1 wrong published question = 74K rank distortions in one instant |
| Question bank target | 2M+ questions at steady state | ~15,000–20,000 new questions/month across all 9 SMEs |
| Exam types served | 8 (SSC CGL · SSC CHSL · RRB NTPC · RRB Group D · AP Board · TS Board · UPSC Prelims · Online) | Each exam type has its own difficulty distribution and topic weights |
| AI generation | 500–2,000 questions per batch · ~15% hallucination rate | Human triage gate (D-08) is mandatory — AI output is raw material, not finished product |
| Notes library target | ~10,000 structured notes across all subjects | Faculty uploads → Notes Editor structures → institution students study |
| Review SLA | Reviewer: 3 days · Approver: 2 days · GK Reviewer: 1 day | SLA breach = pipeline stall = content drought before exams |
| DPDPA 2023 | Author identity is PII — stored in ap-south-1 only, never in exports | Audit logs must not export SME names/emails to CSV/PDF |
| **Critical constraint** | **Only Question Approver (Role 29) can publish MCQs — no exception, no override** | Double-gate protects 74K concurrent students from defective content |

---

## Division D — Role Summary

| # | Role | Level | Subject / Scope | Publish MCQs? | Publish Notes? | Cannot Do |
|---|---|---|---|---|---|---|
| 18 | Content Director | 2 | All subjects · all exam types · pipeline oversight | No — Approver gate is absolute | No (can approve notes if toggle enabled) | Publish MCQs directly · infra · billing |
| 19 | SME — Mathematics | 2 | Arithmetic · Algebra · Geometry · Data Interpretation · Calculus | No | No | Publish · review others' questions |
| 20 | SME — Physics | 2 | Mechanics · Optics · Electricity · Modern Physics | No | No | Publish · review others' questions |
| 21 | SME — Chemistry | 2 | Organic · Inorganic · Physical Chemistry | No | No | Publish · review others' questions |
| 22 | SME — Biology | 2 | Botany · Zoology · Human Physiology | No | No | Publish · review others' questions |
| 23 | SME — English | 2 | Grammar · Reading Comprehension · Vocabulary · Error Spotting | No | No | Publish · review others' questions |
| 24 | SME — General Knowledge | 2 | Current Affairs · Polity · History · Geography · Economy | No | No | Publish · review others' questions |
| 25 | SME — Reasoning | 2 | Verbal · Non-Verbal · Logical · Analytical Reasoning | No | No | Publish · review others' questions |
| 26 | SME — Computer Science | 2 | IT Fundamentals · Programming · Digital Literacy | No | No | Publish · review others' questions |
| 27 | SME — Regional Language | 2 | Telugu · Hindi · Urdu (State Board exams) | No | No | Publish · review others' questions |
| 28 | Question Reviewer | 2 | All subjects — quality · accuracy · language · formatting | No | No | Publish · create questions |
| 29 | Question Approver | 2 | All subjects — **final publish gate** | **Yes — sole MCQ publish authority** | No | Create questions |
| 30 | Notes Editor | 2 | All faculty-uploaded notes — structure · tag · publish | No | **Yes — notes only** | Publish MCQs · create MCQs |

---

## Content Pipeline Flows

```
── MCQ AUTHORING PIPELINE ──────────────────────────────────────────────────────

  SME creates (D-02) or bulk imports (D-07)
           │
           ▼
      DRAFT  ←─────────────────────────────────────────────────────┐
      (D-01 My Questions tab)                                      │
           │  SME submits for review                               │
           ▼                                                        │
    UNDER_REVIEW                                                    │
    (D-03 Review Queue)                                            │
           │                                                        │
     ┌─────┴──────────────────┐                                    │
     │ Pass to Approver        │ Return to SME (with comment        │
     │                         │ + reason category)                │
     ▼                         ▼                                    │
 PENDING_APPROVAL       RETURNED (D-01 Returned Tab)               │
 (D-04 Queue)                  │ SME revises in D-02               │
     │                         │ (split-view: old vs new)          │
     │                         └───→ UNDER_REVIEW (marked Revision)│
     │                                                             │
     │  Approve + Publish                                          │
     ▼                                                             │
  PUBLISHED → MCQ Bank (D-11)                                      │
     │                                                             │
     ├──► post-publish error discovered                            │
     │         │                                                   │
     │         ▼  Unpublish (D-04 · D-11 · Amendment G2)          │
     │    AMENDMENT_REVIEW (fast-track in D-03 + D-04)            │
     │         └──► SME revises → Reviewer → Approver re-publishes│
     │                                                             │
     └──► student flags (D-16 Feedback Queue)                     │
               └──► ≥10 flags → auto-escalate → Unpublish + G2 ──┘


── AI-GENERATED MCQ PIPELINE ───────────────────────────────────────────────────

  AI Batch (Div C · C-15) → AI Triage Queue (D-08)
           │
     ┌─────┼──────────────┐
     │     │              │
   Accept  Edit+Accept   Reject (reason logged → AI pipeline feedback)
     │     │
     └──┬──┘
        ▼
   UNDER_REVIEW in D-03 (marked as AI-source or AI-Edited-source)
        └──► follows same pipeline as human-authored above


── NOTES PIPELINE ──────────────────────────────────────────────────────────────

  Faculty uploads (institution portal) → S3 notes-raw/
           │
     Format conversion Celery task (PPTX/DOCX → PDF via LibreOffice)
           │
     D-06 Incoming Queue — Notes Editor structures metadata
           │
     ┌─────┴──────────────────────────────────────────────┐
     │ Director Review Toggle OFF (default)                │ Toggle ON (per subject)
     ▼                                                     ▼
  PUBLISHED immediately                          PENDING_DIRECTOR_REVIEW
  → Notes Library (D-11 Notes tab)                        │
                                               Director reviews in D-05 Notes Review tab
                                                         │
                                               Approve → PUBLISHED  /  Return with comment
```

---

## SME Dashboard & Authoring — Pages (Roles 19–27) · 2 pages

> All 9 SME roles share the same two pages. Subject scope is enforced at ORM level via `sme_profile.assigned_subjects[]` — never via URL restriction alone. SMEs never see questions outside their assigned subjects anywhere on the platform.

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| D-01 | SME Personal Dashboard | `/content/sme/dashboard/` | `d-01-sme-dashboard.md` | P0 | ⬜ | Personal workspace for every SME (Roles 19–27). **KPI strip**: questions authored this month · in review · returned · approved · published (lifetime) · quota achieved % vs target set in D-10 · unread director announcements badge (Amendment G11). **My Questions tab** (default): full table of all questions with Status column (Draft / Under Review / Returned / Pending Approval / Published), Days-in-Pipeline badge (amber >2 days, red >5 days), Edit link for drafts, view-only link for submitted. **Returned Questions tab**: prominent yellow banner when count > 0 — table with inline reviewer comment, reason category (Factual Error · Calculation Error · Language · Formatting · Duplicate · Off-Syllabus · Image Quality), return count (questions returned 2+ times flagged red). Direct Edit button opens D-02 in split-view. **Coverage Gaps tab**: read-only view of SME's subject(s) from D-14 data — topic nodes with < 10 published questions shown amber, < 3 shown red — "Create Question for This Topic" quick action. **Performance Data tab** (Amendment G6): per published question — % students who answered correctly · A/B/C/D answer distribution · realized difficulty vs tagged difficulty · discrimination index. Data from Div F exam results. Questions with >20% divergence between tagged and realized difficulty flagged for SME to update tag. **Announcements tab** (Amendment G11): all active announcements from Content Director targeted to this SME's subject — Title · Urgency badge (Info/Warning/Action Required) · date posted · expiry date · body text. Action Required announcements appear as a non-dismissible amber top banner until the SME clicks "Acknowledged". Info announcements dismissible. **My Media tab**: all images/diagrams uploaded by this SME — thumbnail grid, copy-URL for reuse, delete if unreferenced. Subject-scoped throughout. HTMX poll every 60s on My Questions table only. |
| D-02 | Question Authoring & Editor | `/content/sme/question/new/` and `/content/sme/question/<uuid>/edit/` | `d-02-question-editor.md` | P0 | ⬜ | Full question creation and edit workspace for all 9 SME roles. **Subject-specific editor toolbars** loaded from `sme_profile.assigned_subjects`: Math — LaTeX equation builder (MathJax preview) with fraction/integral/summation/matrix shortcuts · Physics — LaTeX + SVG circuit diagram draw tool + ray diagram tool · Chemistry — chemical formula builder (H₂SO₄, [CuSO₄]²⁻) with subscript/superscript shortcuts + SMILES molecular structure renderer · Biology — annotated diagram upload with label overlay tool · CS — code block with syntax highlighting (Python/C/Java/SQL) · English — rich text only · Reasoning — pattern/matrix image upload · GK — rich text + image · Regional Language (27) — Unicode-aware input with Telugu/Devanagari/Urdu IME + script validation (error if non-target Unicode block detected). **Question body**: rich editor + inline image upload (PNG/SVG/JPG ≤ 2MB → S3 `content-media/` → CloudFront URL embedded in question). **Answer options**: minimum 4 options, one correct answer selector, each option supports same rich editing. **Explanation**: mandatory, min 30 characters, same rich editing. **Tagging panel** (right rail, always visible): Subject (locked to SME's assigned subject) → Topic (cascading from D-09 taxonomy) → Subtopic (cascading) · Difficulty (Easy/Medium/Hard) · Bloom's Taxonomy Level (Recall/Understand/Apply/Analyse) · Exam Type(s) multi-select · Content Type (Evergreen/Current Affairs/Time-Sensitive) · Valid Until date (required if not Evergreen — Amendment G5) · Access Level (Platform-Wide/School Only/College Only/Coaching Only — Amendment G4) · High Stakes flag (Amendment G7) · Source Attribution (Original/Adapted from Textbook [text input]/Past Exam Paper [year + name]). **Duplicate detection** (Amendment G1): on every save-draft, async Celery task computes cosine similarity against `content_schema.question_embeddings` pgvector HNSW index. If ≥ 0.80 similarity found, non-blocking orange banner with links to matched questions — SME acknowledges and can proceed. **Passage / Linked Question Set mode** (Amendment G9): toggle from standalone-MCQ to "Create Passage Set" — Passage editor (rich text + images, 50–2,000 word limit, subject tags, exam type tags); SME then creates 2–8 linked MCQs under the passage, each with its own options + answer + explanation + tags. All questions in the set share a `content_question_set` parent. Questions submitted as a unit: all move to `UNDER_REVIEW` together; Reviewer sees the full passage + all linked MCQs in a single review view. If Reviewer returns any question in the set, the specific questions are returned (not the whole set unless passage itself has errors). Approver approves questions individually but cannot publish any set question until all have `PENDING_APPROVAL` status. Data models: `content_question_set`, `content_question_set_items`. English and GK exam types show passage-set option by default; all other subjects can optionally enable. **Revision history panel** (edit mode on returned question): left shows previous submitted version (read-only, reviewer comment highlighted) · right is live edit. **Actions**: Save as Draft · Submit for Review (validates all required fields). Content freeze check: if question's exam type is in freeze period (D-10), Submit button disabled with reason displayed. |

---

## Question Reviewer — Pages (Role 28) · 1 page

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| D-03 | Question Review Workspace | `/content/review/queue/` | `d-03-review-queue.md` | P0 | ⬜ | Primary workspace for Question Reviewer (Role 28). **KPI strip**: total pending · assigned to me · reviewed today · avg days-in-queue (alert if >3) · my return rate this month · amendment reviews pending. **Tabs**: Pending Review · Amendment Reviews (fast-track, yellow-badged) · Assigned to Me · My Review History. **Pending Review table**: all `UNDER_REVIEW` questions — ID · Subject · Topic · Content Type · Difficulty · SME Author · Submitted Date · Days Waiting (red if > SLA) · Revision # (shows "Revision 2" if returned before) · AI Source badge (if AI-generated). **Amendment Reviews tab**: questions in `AMENDMENT_REVIEW` state — shown separately with amber "Amendment" badge, same columns plus Previous Publish Date and Unpublish Reason — prioritised above regular queue. **Batch self-assign**: Reviewer self-assigns up to 50 questions from unassigned pool (atomic DB row lock prevents double-assignment). **Review Drawer** (720px): full subject-specific rendering (LaTeX/circuit diagrams/code blocks/Telugu script), all options, correct answer, explanation, SME notes, full prior return history. Drawer tabs: Question Preview · Reviewer Notes (free-text + Quick Templates: reviewer's saved return-reason templates) · Return History. **Drawer actions**: `Pass to Approver` (one-click, logs reviewer + timestamp) · `Return to SME` (comment ≥ 20 chars OR template selection + reason category: Factual Error · Calculation Error · Language/Grammar · Formatting · Incomplete Explanation · Duplicate · Off-Syllabus · Image Quality · Script Error) · `Flag for Committee Review` (Amendment G7 — marks question for 2-reviewer consensus, returns to unassigned pool). **Inline Duplicate Check**: "Check Duplicates" button in drawer searches D-11 published bank via pgvector — top 5 matches with similarity score shown inline. Filters: Subject · Difficulty · Content Type · SME · Exam Type · Days Waiting ≥ N · Revision # ≥ 2 · AI Source. HTMX auto-refresh every 30s (suspended when drawer open). |

---

## Question Approver — Pages (Role 29) · 1 page

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| D-04 | Question Approval & Publish | `/content/approve/queue/` | `d-04-approval-queue.md` | P0 | ⬜ | Final publish gate — **only Question Approver (Role 29) can publish MCQs**. **KPI strip**: pending approval · amendment reviews pending · bulk-approved today · published all-time · unpublished this month. **Tabs**: Pending Approval · Amendment Reviews · Published Questions · Sent Back History. **Pending Approval table**: all `PENDING_APPROVAL` questions — ID · Subject · Topic · Reviewer Name · Review Date · Difficulty · Content Type · Access Level · Exam Types · Revision #. Per-row: `Approve + Publish` · `Send Back to Reviewer` (note ≥ 15 chars + reason) · `Open Detail`. **Approval Drawer** (720px) — tabs: Question Preview (full subject-specific render) · Review Trail (full chain of custody — reviewer notes, SME revision history, all timestamps) · Tags (Approver can correct Difficulty or Access Level without triggering re-review — logged as Tag Amendment in D-12) · Exam Usage (if amendment: which active exams used this question before unpublish). **Bulk Approve + Publish**: select up to 200 rows → confirm modal (type "PUBLISH") → Celery async batch publish → live HTMX progress bar → completion notification. Amendment approvals always require 2FA re-prompt regardless of bulk/single. **Amendment Reviews tab**: `AMENDMENT_REVIEW` questions — orange "Amendment" badge · Previous Publish Date · Unpublish Reason · Flagged By. **Published Questions tab**: full searchable published bank with Approver-only actions — `Unpublish` (reason ≥ 20 chars + category: Paper Leak/Factual Error/Copyright/Court Order/Other + 2FA → triggers Amendment G2 workflow) · `Difficulty Re-Tag` (update tag without unpublish — logged as Tag Amendment in D-12) · `Access Level Change` (logs Access Amendment in D-12) · `Extend Valid Until` (for Current Affairs — Amendment G5). **Emergency Bulk Unpublish** (Amendment G8): multi-select up to 500 questions → reason category (Paper Leak/Critical Factual Error/Court Order/Copyright Infringement) → type "EMERGENCY" + 2FA → Celery high-priority task removes all from exam engine active pool immediately (< 60s for 500 questions) → Content Director auto-notified + Div F Exam Operations notified if active exam affected → per-question D-12 audit entry. **Sent Back History tab**: all questions Approver sent back to Reviewer — reason and outcome. HTMX auto-refresh every 60s. |

---

## Content Director — Pages (Role 18) · 4 pages

> Content Director (Level 2) has cross-subject read access to the entire content pipeline. Cannot publish MCQs directly — the Approver gate is absolute and has no override. Can approve notes when Director Review Toggle is enabled per subject (Amendment G3).

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| D-05 | Content Director Command Center | `/content/director/` | `d-05-director-dashboard.md` | P0 | ⬜ | Platform-wide content health overview for Content Director. **KPI strip**: total published questions · published this week · in review now · awaiting approval · returned (stuck > 3 days) · notes pending director review · AI triage queue depth. **Pipeline Funnel widget**: Draft → Under Review → Pending Approval → Published — live counts with Δ vs yesterday. **Subject Coverage Matrix** (9 subjects × 8 exam types grid): each cell shows published question count, colour-coded green (≥ target) / amber (50–99%) / red (< 50%); click drills to D-14 for that subject+exam combination. **SME Production Table**: per-SME — quota set (from D-10) · authored this month · in pipeline · returned count · published · return rate — sortable — inline "Set Quota" action (notifies SME). **Stale Alerts panel**: questions in review > SLA threshold (from D-15 config), questions in approval > 2 days, amendment reviews > 1 day — per-row "Escalate" button sends in-app notification to Reviewer/Approver. **Reviewer Load strip**: per reviewer — current queue depth · oldest question age · 7-day avg throughput · return rate — "Reassign N Questions" action. **Notes Review tab** (Amendment G3): notes in `PENDING_DIRECTOR_REVIEW` — Title · Subject · Institution source · Notes Editor · Submitted Date — Approve or Return with comment actions. **Expiry Monitor tab** (Amendment G5): published Current Affairs questions expiring within 30 days — Question ID · Subject · Topic · Valid Until · used-in-upcoming-exams flag — Extend/Archive actions. **Announcements tab** (Amendment G11): Director creates announcements to communicate syllabus changes, quality policy updates, and production guidance to Div D staff. New announcement form: Title · Body (rich text) · Target Audience (All Div D / specific subjects — multi-select checkboxes for Math/Physics/Chemistry/Biology/English/GK/Reasoning/CS/Regional) · Urgency (Info / Warning / Action Required) · Expiry Date (auto-dismisses after date). Published announcements list: Title · Audience · Urgency · Sent Date · Expiry · Read Count (how many target recipients have seen it) · Edit / Retract. Action Required announcements shown as persistent amber banner in D-01 for target SMEs until each SME acknowledges. Data model: `content_director_announcements`, `content_announcement_reads`. **AI Pipeline Summary widget**: today's batch status, acceptance rate, avg confidence score, questions entering D-03 — link to D-08. Tabs: Overview · Pipeline Detail · SME Productivity · Reviewer Load · Stale Alerts · Notes Review · Expiry Monitor · Announcements. HTMX poll every 60s. |
| D-09 | Subject-Topic Taxonomy Manager | `/content/director/taxonomy/` | `d-09-taxonomy.md` | P1 | ⬜ | Authoritative Subject → Topic → Subtopic hierarchy used by all SMEs for tagging (D-02), syllabus mapping (D-14), notes tagging (D-06), and Div B exam pattern configuration. **Tree panel** (left 35%): collapsible 3-level tree — 9 subjects → ~300 topics → ~1,500 subtopics. Each node: name · published question count badge · Active/Archived status. **Edit panel** (right 65%): Name · Description · Official Syllabus Reference (e.g. "SSC CGL 2024 Notification §3.2.1") · Active/Archived toggle · Parent node (move to different parent allowed). Add child node at any level. **Gap View tab**: topic nodes with < 10 published questions (amber) or < 3 (red) — "Assign SME to this topic" action. **Exam Type Mapping tab**: for selected topic, multi-select which exam types include it — feeds D-14 coverage analysis. **Style Guide tab**: per-subject writing standards — difficulty calibration rubrics (what constitutes Easy/Medium/Hard per subject), formatting conventions (LaTeX standards, image quality, code block rules for CS), common mistake patterns, example high-quality questions at each difficulty level — read-only for all Div D roles, editable by Content Director only. **Bulk Retag action** (Amendment G10): available when archiving or restructuring a topic/subtopic node that has published questions tagged to it. Archive node → system shows count of affected questions (published + in-pipeline) → "Bulk Retag to..." (select target topic/subtopic from same subject, cannot reassign across subjects) → confirmation modal showing: question count · target node · estimated Celery task duration → "Retag N questions" button → Celery async task updates `content_question.topic` and `content_question.subtopic` for all affected questions → live HTMX progress bar → completion notification. Re-tag does not trigger re-review; logged as "Taxonomy Retag" in D-12 per question. Questions in `UNDER_REVIEW` or `PENDING_APPROVAL` states are also retagged (metadata only — no workflow interruption). Director and Approver can trigger; SMEs cannot. Data model: `content_taxonomy_retag_job`. Archive constraints: cannot archive a node unless Bulk Retag completes for all tagged questions first. Cannot hard-delete any node — soft-archive only. Data model: `content_taxonomy_subject`, `content_taxonomy_topic`, `content_taxonomy_subtopic`, `content_style_guide`. Memcached 10-min TTL for taxonomy tree (cache.delete on any node change). |
| D-10 | Content Calendar & Quota Planner | `/content/director/calendar/` | `d-10-calendar.md` | P1 | ⬜ | Monthly and quarterly production planning. **Calendar View** (month grid): each day cell — production target · actual published count (bar fill) · exam/freeze dates as event markers. **Quota Config table**: SME × Subject × Month matrix — editable integer target cells. Save triggers in-app + email to SME. **Actual vs Target chart**: stacked bar per SME per month — Published (green) / In Pipeline (amber) / Quota (outline) — 6-month rolling. **SME-to-Subject Assignment panel**: assign SMEs to Subject+Exam-Type combinations (one SME can cover multiple subjects; one subject can have multiple SMEs for volume). **Upcoming Exam Dates panel**: key exam dates listed — highlights months needing content surge or freeze. **Content Freeze Config**: per exam type, set Freeze Date — after this date no new questions for that exam type's pool accepted. Freeze enforced in D-02 (Submit disabled for frozen exam type, reason shown) and D-04 (Approve+Publish blocked for questions tagged to frozen exam types). Freeze lifted only by Content Director. **Content Type Targets**: per subject per month — target breakdown for Evergreen vs Current Affairs vs Time-Sensitive (GK SME needs weekly Current Affairs targets; Math SME needs Evergreen only). Data models: `content_sme_quota`, `content_exam_freeze`, `content_calendar_event`. |
| D-14 | Exam Type & Syllabus Coverage | `/content/director/syllabus/` | `d-14-syllabus.md` | P2 | ⬜ | Coverage and distribution analysis per exam type. **Exam Type selector** (left): SSC CGL · SSC CHSL · RRB NTPC · RRB Group D · AP State Board · TS State Board · UPSC Prelims · Online Domains. **Coverage tab** (right, default): syllabus topic tree for selected exam type — per topic: published count · target · coverage % (colour-coded green/amber/red). Gap subtab: topics below target sorted by gap size — Export CSV. **Difficulty Distribution tab**: per topic per exam type — stacked bar Easy/Medium/Hard published counts. Target ratio configurable by Content Director (SSC CGL Math: 30% Easy / 50% Medium / 20% Hard). Cells below target ratio shown amber/red. Export distribution gap report. Without this view, exam engine cannot build balanced papers — a P0 functional gap in exam quality. **Access Level Distribution tab** (Amendment G4): per subject, breakdown of Platform-Wide vs School-Only vs College-Only vs Coaching-Only questions — ensures no exam type is accidentally all-restricted. **Content Freshness tab** (Amendment G5): for GK and Current Affairs subjects — published question count by valid_until date range: "Expiring ≤30 days" · "Expiring ≤90 days" · "Already expired (archived)" — bulk-archive expired questions action. **Exam Date Config panel**: set official exam date and content freeze date per exam type — propagated to D-10 calendar and D-05 stale alerts. **Syllabus Change Management**: Content Director marks topics as removed/added for next exam cycle — triggers D-09 taxonomy archive flow for removed topics. |

---

## Notes Editor — Pages (Role 30) · 1 page

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| D-06 | Notes Management | `/content/notes/` | `d-06-notes-management.md` | P0 | ⬜ | Full workspace for Notes Editor (Role 30). **Incoming Queue tab**: faculty-uploaded notes (PDF/DOCX/PPTX ≤ 50MB) waiting to be processed — uploaded via institution portal, landed in S3 `notes-raw/`, format conversion Celery task runs immediately (PPTX/DOCX → PDF via LibreOffice headless). Per-row: file name · institution source · subject · upload date · file size · Conversion Status (Processing spinner / ✅ Ready / ❌ Failed + Retry / manual replacement upload) · Download button. Multi-select batch tagging: apply common Subject+Topic tags to multiple notes. Open a note → **Note Structuring Drawer** (860px): PDF preview panel (left 55%) + structured metadata form (right 45%). Metadata fields: Title (required) · Subject (required, from D-09 taxonomy) · Topic(s) (multi-select from D-09, cascading subtopics) · Class/Standard · Exam Type(s) multi-select · Chapter Reference · Academic Year · Difficulty Level (Introductory/Standard/Advanced) · Tags (free text). **Director Review Toggle** (Amendment G3): if enabled for this subject by Content Director in D-05, Publish action → `PENDING_DIRECTOR_REVIEW` with "Awaiting Director Approval" badge; if disabled (default), Publish goes live immediately → S3 key moved from `notes-raw/` to `notes-published/`. **Published Library tab**: all published notes — searchable by subject/topic/exam type/year. Per-row: Title · Subject · Topics · Published Date · View Count (30d) · Version badge (v1, v2, etc.). Edit metadata (no unpublish — just updates tags, logged). Unpublish + Edit: moves back to incoming queue, previous version preserved in S3 with -v1/-v2 suffix. Version History icon per note: all publish events with date, Notes Editor name, "Restore to this version". **In Progress tab**: notes currently being structured (saved metadata drafts). **Director Review panel** (if enabled): notes pending Director review with Director's comment if returned. HTMX poll on incoming queue every 60s. Data models: `content_notes`, `content_notes_versions`, `content_notes_audit_log`. |

---

## Bulk Operations & AI Triage — Pages · 2 pages

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| D-07 | Bulk MCQ Import | `/content/import/` | `d-07-bulk-import.md` | P1 | ⬜ | Import questions in bulk via CSV/Excel. Accessible to all SMEs (own subjects only, ORM-enforced) and Content Director (all subjects). **Step 1 — Upload**: drag-drop CSV/XLSX, max 500 rows per file. Template download per subject (pre-populated with all required columns: question, option A-D, correct answer, explanation, topic code, subtopic code, difficulty, bloom level, exam types, content type, access level, valid_until, source attribution). **Step 2 — Validation Report**: Celery task validates every row (required fields · valid taxonomy codes · ≥4 options · exactly 1 correct answer · explanation ≥ 30 chars · valid content_type value · valid_until present if not Evergreen · valid access_level value). Live HTMX progress bar. Results: ✅ Valid rows / ❌ Error rows with per-cell inline error messages. Inline fix: user edits errors directly in preview table without re-uploading — validated on-change via HTMX. **Step 3 — Duplicate Check** (Amendment G1): all valid rows pass through pgvector HNSW cosine similarity — rows with ≥ 0.80 match flagged in "Possible Duplicates" section. SME reviews matches and acknowledges (non-blocking). **Step 4 — Submit**: valid rows saved as `DRAFT` attributed to uploading SME. Invalid rows excluded with "Download Errors CSV". Batch logged: batch ID · uploader · row count · valid · errors · subject · timestamp. Content Director imports for any subject; SME restricted to assigned subjects — mismatched subject rows auto-rejected. Data model: `content_import_batch`, `content_import_batch_rows`. |
| D-08 | AI-Generated MCQ Triage | `/content/ai-triage/` | `d-08-ai-triage.md` | P1 | ⬜ | Human screening queue for AI-generated MCQs from Div C AI Pipeline (C-15). Accessible to Content Director (full access including batch reject) and Question Reviewer (screen only — no batch-reject-all). **KPI strip**: total in triage · accepted today · rejected today · acceptance rate this batch · avg AI confidence score · auto-rejected by AI pipeline before human triage. **Batch selector**: dropdown of all AI generation jobs — batch ID · model used (Claude Sonnet 4.6/GPT-4o/Gemini 1.5 Pro) · prompt version · exam domain · generation date · total questions · auto-rejected count · awaiting human count. **Triage table**: Question text (truncated, expandable) · Subject · Difficulty (AI-assigned) · AI Confidence Score (0–100) · AI Flags (none / Hallucination Risk / Possible Duplicate / Formatting Issue / Off-Syllabus / Copyright Risk) · Days in Triage. Flagged rows auto-sorted to bottom. **Per-row actions**: `Accept` (→ `UNDER_REVIEW` in D-03, marked AI-source) / `Edit + Accept` (opens edit drawer identical to D-02 edit mode → saved → `UNDER_REVIEW` marked AI-Edited-source) / `Reject` (reason: Factual Error · Hallucination · Duplicate · Off-Syllabus · Poor Quality · Copyright Risk). **Batch actions** (Content Director only): `Accept All Clean` (accepts all rows with no AI flags, up to 200 at once) / `Reject All Flagged` (rejects all flagged rows in batch with bulk reason). Integration: reads from Div C C-15 AI job output · sends accepted questions to D-03 · acceptance rate fed back to C-16 AI Cost Monitor as quality signal. Data models: `content_ai_question_queue`, `content_ai_triage_log`. |

---

## Cross-Role Search, Analytics & Reporting — Pages · 3 pages

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| D-11 | Published MCQ Bank | `/content/bank/` | `d-11-published-bank.md` | P1 | ⬜ | Searchable master bank of all published questions. Read access for all Div D roles; Approver has additional write actions. **Advanced search**: full-text on question body + all four options (PostgreSQL `tsvector` GIN index). **Filters**: Subject · Topic · Subtopic · Difficulty · Exam Type · Author SME · Published Date range · Bloom's Level · Content Type (Evergreen/Current Affairs/Time-Sensitive) · Access Level (Platform-Wide/School Only/College Only/Coaching Only — Amendment G4) · Expiry Status (All/Expiring ≤30 days/Expiring ≤90 days/Expired-Archived — Amendment G5). Results: 50 rows/page — ID · Subject · Topic · Difficulty · Content Type · Access Level · Valid Until · Exam Types · Author · Published Date · Used In Exams count. **Question Preview Drawer** (640px): Preview (full render — LaTeX/images/code blocks/Telugu script, never raw markdown) · Tags (all metadata) · Version History (link to D-12) · Exam Usage (exam papers that used this question: institution name · exam date · marks allotted). **Approver-only drawer actions**: `Unpublish` (reason ≥ 20 chars + category + 2FA → triggers Amendment G2) · `Difficulty Re-Tag` (logged as Tag Amendment in D-12) · `Access Level Change` (logged as Access Amendment in D-12 — Amendment G4) · `Extend Valid Until` (Amendment G5). **Export**: filtered selection to CSV (raw data, max 2,000 questions) or PDF (formatted question paper layout, max 500 questions) — async Celery generation, download-ready notification. PDF: EduForge watermark per page. Export action logged in D-12 per question (who exported, filter used, timestamp). Questions tagged to future exam papers blocked from export until exam date passes (DPDPA + exam secrecy). **Notes tab**: published notes library searchable by same filters — Notes Editor's Unpublish+Edit available for own notes; Director has full access. Memcached 5-min cache for question count aggregates (cache.delete on any publish/unpublish). |
| D-12 | Question Audit & Version History | `/content/audit/<uuid>/` | `d-12-audit-history.md` | P2 | ⬜ | Full lifecycle audit for any individual question. Accessed from D-11 drawer "Version History" link or D-04 Published tab. Accessible to Content Director and Question Approver. **Timeline view** (newest → oldest): state transition cards — Created · Saved Draft · Submitted · Under Review (assigned to Reviewer) · Returned (reviewer comment + reason, highlighted) · Resubmitted · Pending Approval · Approved + Published · [if applicable] Unpublished (reason + actor) · Amendment Review · Re-approved + Re-published. Also captures: Tag Amendment (difficulty/access level change by Approver) · Export Event (who exported, filter, timestamp). Each card: actor name · role · timestamp · IP address · before-state → after-state diff (field-level). **Version Compare**: select any two version snapshots → side-by-side diff (question text · each option · explanation · all tags — changes highlighted green/red). **Restore Version**: Approver can restore any prior version (question moves to `DRAFT` attributed to original SME, restoration reason logged, 2FA required). Audit entries are immutable: INSERT-only, no UPDATE or DELETE permitted on `content_question_audit_log` at application layer. Author identity (name, email, IP) never exported to CSV/PDF — DPDPA compliance. |
| D-13 | Content Quality Analytics | `/content/analytics/quality/` | `d-13-quality-analytics.md` | P2 | ⬜ | Quality intelligence dashboard. Content Director (full access) · Question Reviewer (own metrics only, ORM-scoped). **SME Quality Table**: per-SME — questions authored · published · return rate (returned/submitted) · avg review cycles per question · error type breakdown (expandable sparkline: Factual vs Language vs Formatting vs Duplicate) · avg days from draft to publish. **Reviewer Performance Table**: per-reviewer — questions reviewed per day (7-day avg) · avg time-per-question · pass-to-approver rate · return-to-SME rate · return reason breakdown. **Pipeline Age Distribution**: histogram of current queue items by days-in-review and days-in-approval — shows where the bottleneck is. **Post-Publish Issues table**: questions unpublished by month — reason distribution · which SME authored · which reviewer approved. **Difficulty Calibration tab** (Amendment G6): published questions where realized difficulty (% students correct from Div F) diverges > 20% from tagged difficulty — table with question ID · tagged · realized · gap % — Approver can re-tag directly from this table. **Trend charts**: 12-month rolling — publication rate · return rate · acceptance rate · avg review cycle time — with anomaly markers. **AI vs Human quality**: if AI-sourced questions tracked separately — acceptance rate, post-publish issue rate for AI vs human-authored. Filters: Subject · SME · Reviewer · Date range · Source (Human/AI/Bulk Import). Export to CSV. HTMX poll every 5 min (aggregated). |

---

## Specialized & Operational Pages · 3 pages

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| D-15 | Reviewer Assignment Manager | `/content/director/reviewers/` | `d-15-reviewer-assignments.md` | P2 | ⬜ | Content Director configures and rebalances reviewer workloads. **Assignment Matrix**: Reviewer × Subject grid — primary / backup checkboxes per cell. Save → future questions of those subjects auto-assigned to primary; if primary queue > threshold, auto-routes to backup. **Live Queue Depth panel**: per reviewer — current queue size · oldest question age · questions past SLA · 7-day avg throughput — colour-coded. **Rebalance Action**: select N questions assigned to one reviewer → reassign to another — modal listing which questions will move. **SLA Config panel**: review SLA per subject (GK Current Affairs: 1 day · Math: 3 days · Science: 3 days · English: 2 days) — threshold drives overdue indicators in D-03, D-05 stale alerts, D-13 pipeline age. **Out-of-Office toggle**: mark reviewer as OOO with start/end date — questions auto-route to configured backup for OOO period. **Committee Review Config** (Amendment G7): toggle "Enable Committee Review for [Subject]" — when enabled, questions in that subject flagged as High Stakes require 2 independent sequential reviewer passes before Pending Approval. Second reviewer sees question only after first has passed it. Data models: `content_reviewer_assignment`, `content_reviewer_oof`, `content_sla_config`, `content_committee_review_config`. |
| D-16 | Student Question Feedback Queue | `/content/feedback/` | `d-16-feedback-queue.md` | P2 | ⬜ | Questions flagged by students during or after exams. Data source: Div F exam results module pushes flag events via internal API to `content_student_question_flag` table. Accessible to Content Director (full) and Question Approver (triage + action). **KPI strip**: new flags today · total open · auto-escalated (≥10 flags, same question) · resolved this week. **Incoming Feedback table**: Question ID · Question Text (truncated, expandable) · Flag Type (Wrong Answer/Unclear Wording/Multiple Correct/Typo/Image Quality/Other) · Source Exam · Institution · Flag Count (bold if ≥10) · Date First Flagged. Sorted by Flag Count descending. **Per-row actions**: `Mark Invalid — Dismiss` (reason logged) / `Mark Valid — Trigger Unpublish + Amendment Review` (Amendment G2: immediately unpublishes, creates AMENDMENT_REVIEW task, notifies original SME with flag details, notifies Approver). **Auto-escalation**: Flag Count reaches 10 → system auto-creates escalation record → Content Director in-app notification + email → question flagged red → Approver prompted to review. **History tab**: all resolved feedback — action taken · resolution date · content change made · whether re-published. Student IDs masked in UI (only flag count shown); full student ID available only in audit log (DPDPA compliance). Div F sends flag events within 5 minutes of exam session close. Data models: `content_student_question_flag`, `content_flag_resolution_log`. |
| D-17 | Notes Analytics & Usage | `/content/notes/analytics/` | `d-17-notes-analytics.md` | P3 | ⬜ | Usage analytics for the Notes Library. Notes Editor (own published notes only) · Content Director (all). **Usage Table**: per note — Title · Subject · View Count (30d) · Download Count (30d) · Institution Count (institutions that accessed it) · Student Count (approx from access logs). **Subject Coverage Chart**: published notes count vs target per subject — target set by Content Director in this page's config. **Syllabus Gap tab**: topics from D-09 taxonomy with 0 notes — sorted by exam exposure frequency (topics with high exam usage but zero notes = highest priority gap). "Create Note Request" action per row (flags topic as notes-wanted priority for Notes Editor). **Content Type breakdown**: Introductory vs Standard vs Advanced notes per subject — bar chart. **Most/Least Accessed**: top 10 + bottom 10 per subject. **Notes Freshness**: notes older than 2 years flagged for review (academic content changes annually). Export to CSV. HTMX poll every 10 min. Data model: `content_notes_access_log`. |

---

## Question Export & Reports — 1 page

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| D-18 | Question Export & Content Reports | `/content/reports/` | `d-18-reports.md` | P3 | ⬜ | Content Director export and reporting hub.

---

## Notifications & System Configuration — 2 pages

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| D-19 | Notifications Inbox | `/content/notifications/` | `d-19-notifications.md` | P1 | ⬜ | Unified notification center for all Div D roles. Every in-app notification referenced throughout D-01 to D-18 lands here. **Notification types:** Question Returned (SME) · Question Passed to Approver (SME via question audit) · Quota Updated (SME from D-10) · Director Announcement (SME from D-05) · Question Escalated (Reviewer from D-05) · OOO Confirmed (Reviewer from D-15) · Critical Feedback Escalation (Approver from D-16) · Amendment Review Created (Approver from D-04) · Note Request Assigned (Notes Editor from D-17) · SME Question Reassignment (SME from D-05 reassign workflow) · Import Batch Ready / Failed (SME from D-07). **Bell icon** in top nav bar: badge shows unread count (red badge, max "99+"). **Notification list:** newest first · unread = white background + blue left border · read = grey background. Each notification: icon (type) + title + short body text + "N minutes ago" relative time + action button (e.g. "View Question", "Go to Review Queue", "Acknowledge"). **Mark All Read** button. **Filter by type** (dropdown multi-select). **Notification Preferences** (per role): toggle which event types generate in-app notifications. Email notification opt-in per type. Data models: `content_notification`, `content_notification_read`, `content_notification_preference`. DPDPA: notifications never contain personal names — always role labels. |
| D-20 | Content Configuration | `/content/director/config/` | `d-20-config.md` | P2 | ⬜ | Platform-wide configuration managed by Content Director only. **Exam Type Manager tab:** Create/Edit/Deprecate exam type codes (SSC CGL, SSC CHSL, RRB NTPC, RRB Group D, AP Board, TS Board, UPSC Prelims, Online + any new exam types). Fields: Code (unique, uppercase, used in ORM) · Display Name · Active/Deprecated toggle. Deprecated exam types no longer appear in D-02 tagging dropdowns but historical data preserved. **Subject Manager tab:** Create/Edit/Archive subject codes (Math, Physics, Chemistry, Biology, English, GK, Reasoning, CS, Regional Language + new subjects). Fields: Code · Display Name · SME Role (creates role association) · Active/Archived toggle. Archiving requires all questions and notes re-tagged to another subject first (same Bulk Retag flow as D-09 G10). **AI Triage Thresholds tab:** Configure auto-rejection thresholds for D-08: Hallucination confidence score threshold (default 0.75 — questions below this score auto-rejected before human triage) · Duplicate similarity threshold (default 0.95 for auto-reject vs 0.80 for human-flag) · Formatting issue threshold. Changes take effect on the next AI batch processed. **Reviewer Performance Targets tab:** Set per-reviewer or global targets: Questions reviewed per day target (default 20) · Max acceptable avg time per question (default 30 min) · Max acceptable return rate (default 40%). D-13 uses these targets for actual vs target comparison. Data models: `content_exam_type_config`, `content_subject_config`, `content_ai_threshold_config`, `content_reviewer_performance_target`. | **Question Set Export**: apply filters (Subject · Topic · Difficulty · Content Type · Access Level · Exam Type · Date range · Bloom's Level) → preview count → export to PDF (formatted question paper layout with EduForge watermark, correct answers in separate appendix, max 500 questions) or Excel (raw data with all tag fields, max 2,000 questions). Celery async generation → download-ready notification + email link. Export event logged in D-12 audit per question (actor, filter used, timestamp). Questions tagged to future exam papers blocked from export until exam date passes. **Coverage Gap Report**: automated PDF — per exam type per subject: published vs target, difficulty distribution vs required, coverage % per topic, overdue SME quotas. Auto-generated monthly on 1st of each month, emailed to Content Director. **Production Velocity Report**: 12-month rolling — questions created/reviewed/approved/published/rejected/amended per month per subject per SME. **Content Freshness Report**: Current Affairs and Time-Sensitive questions expiring in next 90 days — count per subject + list of expiring questions. **Scheduled Reports config**: Content Director sets frequency (weekly/monthly), recipients (up to 10 email addresses), report type, filter preset. Author identity (SME names, emails) excluded from all exported reports per DPDPA 2023. Data model: `content_scheduled_reports`, `content_report_export_log`. |

---

## Global UI Standards — Division D

> These patterns apply to **every page and every table in Division D** unless a page spec explicitly overrides one. Developers implement these once via shared components; page specs reference them by name without repeating the spec.

---

### 1. Toast Notifications

Every user-triggered action produces a toast. No action is silent.

| Variant | Colour | Auto-dismiss | Use for |
|---|---|---|---|
| Success | Green | 4 seconds | Save · Submit · Publish · Assign · Export queued · Freeze lifted |
| Error | Red | Persistent (manual ✕) | Server validation fail · Permission denied · Celery task failed |
| Warning | Amber | 8 seconds | Partial success · SLA breach · Upcoming freeze · Approaching quota limit |
| Info | Blue | 6 seconds | Background task started · Sync in progress · Re-route to backup reviewer |

**Placement:** Top-right corner, stacked (max 3 visible at once). New toasts slide in from right. Each toast: icon + short title (≤ 6 words) + optional detail line (≤ 60 chars). ARIA role="alert" for screen readers.

**Key toast messages per action type (applies globally):**
- Save draft → "Draft saved" (Success, 4s)
- Submit for review → "Submitted for review" (Success, 4s)
- Publish → "Question published" (Success, 4s) or "N questions published" for bulk
- Export queued → "Export started — you'll be notified when ready" (Info, 6s)
- Network error → "Connection lost — changes not saved. Retry?" (Error, persistent)
- Permission denied → "You don't have permission to do this" (Error, persistent)
- Celery task failed → "{Action} failed — {summary reason}. Please retry." (Error, persistent)

---

### 2. Skeleton Loaders

Every section that fetches data asynchronously (page load, tab switch, filter apply, drawer open) shows a skeleton before content arrives. Never show a blank area or layout shift.

| Context | Skeleton type |
|---|---|
| Table rows | Grey shimmer bars matching table row height — show 5–10 skeleton rows |
| KPI strip tiles | Grey shimmer rectangles matching tile dimensions |
| Chart area | Grey shimmer rectangle at chart height with a subtle pulse |
| Drawer content | Left column: shimmer text lines. Right column: shimmer form fields |
| Tree panel (D-09) | Grey shimmer indented tree structure (3 levels) |
| Calendar grid (D-10) | Grey shimmer cells matching day-cell dimensions |

**HTMX indicator:** Every `hx-get` and `hx-post` request sets `hx-indicator` on the triggering element, showing a spinner on the button/link while the request is in flight. For table refreshes, the entire table body fades to 40% opacity with a spinner overlay — content remains visible but dimmed, preventing layout shift.

**Timeout state:** If any HTMX request takes > 8 seconds, show: "This is taking longer than expected. [Retry]" in place of the skeleton. Log the event server-side for C-11 slow query monitoring.

---

### 3. Server-Side Pagination

All data tables use server-side pagination. Never load > 100 rows into the browser in one request.

**Standard controls (rendered below every table):**
```
← Previous   Page [3] of 47   Next →   |   Showing 101–150 of 2,341 results   |   [50 per page ▾]
```

- Page size selector: 25 / 50 / 100 rows. Default: **50 rows**. Preference stored in session (not DB).
- "Showing X–Y of N results" always visible — updates on every filter/search/page change.
- `← Previous` and `Next →` disabled at first/last page (not hidden).
- Page number input: click the "[3]" to type a page number directly — HTMX GET to `?page={n}`.
- URL reflects current page and filters: `?page=3&subject=math&difficulty=hard` — bookmarkable and shareable.
- When a filter or search changes, page resets to 1 automatically.

**Load More pattern** (used instead of page controls for infinite-scroll sections like D-01 My Questions): HTMX `hx-swap="beforeend"` appends next 50 rows. "Load More" button shows remaining count: "Load 50 more (1,247 remaining)". Disabled when all rows loaded.

---

### 4. Search Bar

Every page that lists more than one entity type or more than ~20 rows has a keyword search bar.

**Standard behaviour:**
- Debounced 300ms — HTMX GET fires 300ms after user stops typing, not on every keystroke.
- Search icon (🔍) left of input. Clear button (✕) appears when input is non-empty.
- Placeholder: "Search questions…" / "Search notes…" / "Search feedback…" (page-specific).
- Results update the table in place via HTMX (`hx-target="#table-body"`).
- Page resets to 1 on search.
- Empty search = restore full list (no separate "clear search" button needed — ✕ clears and triggers re-fetch).
- Search is full-text against specified fields (defined per page in Section 9).
- "N results for '{query}'" shown below the search bar when filtering is active.

---

### 5. Advanced Filter Panel

**Standard layout:** Collapsible panel, collapsed by default. "Filters" button shows active filter count badge: "Filters (3)".

When expanded:
- All filter controls visible (dropdowns, date pickers, checkboxes, sliders)
- "Apply Filters" button (primary) + "Reset All" link
- Active filters shown as dismissible pills below the search bar: `Subject: Maths ×` `Difficulty: Hard ×` — each pill dismissible individually
- Filter state persists in URL params — bookmarkable
- HTMX: filter apply triggers table reload, not full page reload

**Date range filter:** Two date pickers (From / To) with "Last 7 days / 30 days / 90 days / Custom" quick-select buttons.

---

### 6. Empty States

Every table or list section has a defined empty state. Never show a blank table with just column headers.

**Standard empty state structure:**
- Neutral illustration (SVG, monochrome, relevant to context)
- Heading: e.g. "No questions in review" (≤ 5 words)
- Subtext: e.g. "Questions submitted by SMEs will appear here. They'll be auto-assigned to you based on your subject assignments." (1–2 sentences, helpful context)
- Primary CTA button (when applicable): e.g. "Assign Questions from Queue" or "Create Your First Question"

**Filtered empty state** (table has data but filters return zero results):
- Heading: "No results match your filters"
- Subtext: "Try broadening your search or clearing some filters."
- "Clear All Filters" button

**Error state** (network failure loading table data):
- Heading: "Couldn't load data"
- Subtext: "Check your connection and try again."
- "Retry" button (re-fires the HTMX request)

---

### 7. Sortable Columns

All data table column headers are sortable unless the column contains non-comparable data (e.g. action buttons, sparklines, status icons).

**Visual treatment:**
- Default state: column header text only (no arrow)
- Hover: faint ↕ icon appears
- Active ascending sort: ↑ icon, column header text bold
- Active descending sort: ↓ icon, column header text bold
- Only one column active at a time
- Sort state in URL: `?sort=return_rate&dir=desc` — bookmarkable
- HTMX: clicking a header fires GET with updated sort params, swaps table body

**Default sort per page defined in each page's Section 9.**

---

### 8. Row Selection for Bulk Actions

Any table that supports bulk actions has a checkbox column.

**Standard behaviour:**
- Column 1: checkbox (hidden until row hover or at least 1 row selected — avoids clutter on read-heavy tables)
- Select all on current page: header row checkbox
- "Select all N results" banner (appears when all rows on current page are checked): "All 50 rows on this page are selected. Select all 2,341 results? [Select All Results] [Cancel]" — cross-page select for bulk operations
- Bulk action bar (appears at bottom of viewport when ≥ 1 row selected, sticky):
  - "{N} selected" count · available bulk actions (context-specific) · "Clear Selection" link
- Selecting rows does not navigate away or open drawers — row click and checkbox are separate interaction targets

---

### 9. Drawers & Modals

**Drawers (right-side panel):**
- Open: slide in from right (300ms ease)
- Close: X button top-right + click backdrop + Escape key
- Widths: 480px (compact) · 640px (standard) · 720px (review/approval) · 860px (notes editor) — see Shared Drawers table
- Mobile (< 768px): drawers take **full viewport width** with a close handle at top
- Tab memory: last active tab within a drawer remembered for the session
- Drawer URL: opening a drawer does NOT change the page URL (avoids browser-back confusion for list pages)

**Modals (center overlay):**
- Used for: destructive confirmations · 2FA prompts · alert escalations
- Width: 480px (desktop) · full width minus 32px margins (mobile)
- Backdrop: 50% dark overlay, click backdrop does NOT close destructive modals (prevents accidental dismiss of "type PUBLISH" confirms)
- Always have: Title · Body text · Cancel button · Confirm button (primary, often destructive red or warning amber)
- Confirm buttons in destructive modals are **disabled until the required text input is typed correctly**

**Form fields within drawers/modals:**
- Required fields marked with asterisk `*`
- Inline error messages appear below each field on blur (not just on submit)
- Field border turns red on validation failure, green on valid input
- Submit button disabled until all required fields are valid

---

### 10. Role-Based UI Visibility

**Principle:** Hidden ≠ Secure. All access control enforced at the Django view layer (PermissionRequiredMixin + ORM scoping). UI hiding is for UX, not security.

| Scenario | Treatment |
|---|---|
| Action button user cannot perform | Hidden entirely (not greyed out) — reduces cognitive load |
| Feature visible but temporarily unavailable | Greyed out + tooltip on hover: "Only the Question Approver can publish questions." |
| Entire tab user cannot access | Tab not rendered in HTML (403 on direct URL access) |
| Field user can view but not edit | Shown as read-only text, not input element |
| ORM-scoped data | Server filters data before rendering — user never sees other users' data in the DOM |

---

### 11. Responsive Breakpoints

| Breakpoint | Width | Layout Behaviour |
|---|---|---|
| Desktop | ≥ 1280px | Full layout — all columns, side panels, drawers at specified widths |
| Tablet | 768px – 1279px | Drawers reduce to 80% viewport width. Tables show 5–7 priority columns, hide secondary columns (revealed via "More" expand). Filter panel collapses to icon-only sidebar. |
| Mobile | < 768px | Single column layout. Tables horizontal-scroll with sticky first column (ID/title). Drawers are full-screen. Modals are full-width. Filter panel is a bottom sheet. Charts stack vertically. Calendar is single-day view. |

**Table priority columns on tablet/mobile** (defined per page in Section 9 — typically: ID, primary status, primary action button. All other columns in a horizontal scroll or expandable row detail).

---

### 12. Charts — Standard Behaviour

All charts in Division D follow these rules:

- **Responsive container:** Charts fill their parent container width. On resize, charts re-render (not just scale). Use Recharts `<ResponsiveContainer>`.
- **Loading state:** Chart area shows a skeleton shimmer before data arrives.
- **No-data state:** Chart area shows "No data available for the selected filters" with a neutral icon. No empty axes.
- **Tooltips:** All data points have hover tooltips with exact values. Mobile: tap tooltips.
- **Legends:** Always shown. Clickable to toggle data series on/off.
- **Colour system:** Consistent palette across all charts — Green (positive/published), Amber (warning/in-pipeline), Red (alert/overdue), Blue (informational). Never rely on colour alone — pattern or label always differentiates series.
- **Export:** Every chart has a "Download PNG" icon (top-right of chart card). Data tables downloadable as CSV from same menu.

---

### 13. HTMX Loading Patterns

| Pattern | Implementation |
|---|---|
| Table refresh (filter/sort/page) | `hx-get` on filter form submission, `hx-target="#results-table"`, `hx-swap="innerHTML"`, `hx-indicator="#table-spinner"` |
| Background poll (KPI strip, alerts) | `hx-trigger="every 60s"` on strip element, `hx-swap="outerHTML"` — replaces entire strip, not just values |
| Drawer content load | `hx-get="/...?part=drawer-content"`, `hx-target="#drawer-body"`, `hx-swap="innerHTML"` — drawer skeleton shown immediately, content replaces on load |
| Celery job progress | Poll `?part=job-status&task_id=X` every 3s with `hx-trigger="every 3s [jobRunning]"` — stops polling when server returns `HX-Trigger: job-complete` response header |
| Inline form submission | `hx-post` on form, `hx-target="#form-feedback"` for validation errors, `hx-swap="innerHTML"` |
| Auto-save | `hx-trigger="change delay:2s"` on all form inputs in D-02 — debounced save-draft on every field change |

---

## Role-to-Page Access Matrix

| Page | Director (18) | SME ×9 (19–27) | Reviewer (28) | Approver (29) | Notes Editor (30) |
|---|---|---|---|---|---|
| D-01 SME Dashboard | 👁 Read-all SMEs | ✅ Own subject only | — | — | — |
| D-02 Question Editor | — | ✅ Own subject | — | — | — |
| D-03 Review Queue | 👁 Read | — | ✅ Full | — | — |
| D-04 Approval Queue | 👁 Read | — | — | ✅ Full + emergency unpublish | — |
| D-05 Director Dashboard | ✅ Full | — | 👁 Own queue metrics only | — | — |
| D-06 Notes Management | 👁 Read + Director review actions | — | — | — | ✅ Full |
| D-07 Bulk Import | ✅ Full (all subjects) | ✅ Own subject only | — | — | — |
| D-08 AI Triage | ✅ Full + batch reject | — | ✅ Screen only (no batch reject) | — | — |
| D-09 Taxonomy Manager | ✅ Full + Style Guide edit | 👁 Read (tagging + Style Guide) | 👁 Read + Style Guide | 👁 Read | 👁 Read (tagging only) |
| D-10 Calendar & Quota | ✅ Full | 👁 Own quota + freeze status | — | — | — |
| D-11 Published Bank | ✅ Full | 👁 Own subject MCQs · Notes tab read | 👁 Read (duplicate check) | ✅ Full + unpublish + re-tag | 👁 Notes tab only |
| D-12 Audit & Version | ✅ Full | — | — | ✅ Full + restore | — |
| D-13 Quality Analytics | ✅ Full | — | 👁 Own metrics only | — | — |
| D-14 Syllabus Coverage | ✅ Full | 👁 Read own subject | — | — | — |
| D-15 Reviewer Assignments | ✅ Full | — | 👁 Own assignment + OOO toggle | — | — |
| D-16 Feedback Queue | ✅ Full | — | — | ✅ Triage + trigger amendment | — |
| D-17 Notes Analytics | ✅ Full | — | — | — | 👁 Own notes only |
| D-18 Reports & Export | ✅ Full | — | — | — | — |
| D-19 Notifications | ✅ Own notifications | ✅ Own notifications | ✅ Own notifications | ✅ Own notifications | ✅ Own notifications |
| D-20 Content Config | ✅ Full | — | — | — | — |

> ✅ Full = read + write + destructive actions where applicable
> 👁 Read = read-only, scoped as noted — ORM-enforced, not CSS-hidden
> — = no access (route guard + Django permission check — 403 returned, not redirect)

---

## Shared Drawers (reused across div-d pages)

| Drawer | Trigger | Width | Tabs |
|---|---|---|---|
| question-detail-drawer | Any question row in D-03, D-04, D-11 | 720px | Preview · Tags · Version History · Exam Usage |
| question-review-drawer | Reviewer opens question in D-03 | 720px | Question Preview · Reviewer Notes + Quick Templates · Return History |
| question-approve-drawer | Approver opens question in D-04 | 720px | Question Preview · Full Review Trail · Tags (Approver-editable) · Exam Usage |
| revision-compare-drawer | SME edits returned question in D-02 | Full split-screen | Previous Version (read-only, left) · Current Draft (editable, right) |
| note-structuring-drawer | Notes Editor opens note in D-06 | 860px | Document Preview · Metadata Form · Version History · Publish |
| ai-question-triage-drawer | Row click in D-08 | 720px | AI Question Preview · AI Flags + Confidence · Accept / Edit / Reject |
| audit-timeline-drawer | D-11 → Version History link | 720px | Timeline · Version Compare · Restore (Approver only) |
| sme-stats-drawer | SME row in D-05 Director Dashboard | 560px | Pipeline · Quality Metrics · Quota Progress · Coverage Gaps |
| duplicate-check-panel | Check Duplicates button in D-03 review drawer | 480px inline | Similarity Results (top 5 matches with score + preview) |
| feedback-detail-drawer | Feedback row in D-16 | 560px | Flag Details · Question Preview · Action (Dismiss / Trigger Amendment) |
| bulk-import-error-drawer | Error row in D-07 validation report | 480px | Error Details · Inline Fix · Re-validate |
| taxonomy-edit-panel | Node click in D-09 tree | Right panel 65% | Name · Description · Syllabus Ref · Active/Archive · Move |
| export-progress-drawer | Export triggered in D-11 or D-18 | 480px | Generation Progress · Download Link · Audit Trail |
| committee-review-drawer | Committee-flagged question in D-03 | 720px | Reviewer 1 Decision · Reviewer 2 (sequential) · Consensus Log |

---

## Functional Gap Analysis

> All 8 gaps resolved via amendments to existing pages — no new pages required.

### G1 — Duplicate Question Detection on Authoring
**Gap:** SME authors a question with no check against the 2M+ bank. At scale, repeated questions across test series compromise exam integrity and enable leakage.
**Resolution:** Amendment to D-02 and D-07. On save-draft (D-02) or batch submit (D-07), async Celery task computes cosine similarity via pgvector HNSW index on `content_question_embeddings`. Similarity ≥ 0.80 → non-blocking orange warning banner with links to matched questions. SME acknowledges and can still proceed. Embeddings pre-computed by Celery within 30 seconds of save.

### G2 — Edit-Published-Question Re-Review Workflow (Amendment Review)
**Gap:** After publish, discovered errors have no defined correction workflow. Direct edits to published questions would bypass the entire review pipeline — at 74K concurrent, even 5 minutes of a wrong question live causes mass rank distortion.
**Resolution:** Amendment to D-04 and D-11. Unpublish action → `AMENDMENT_REVIEW` state. Question immediately removed from exam engine active pool via Celery high-priority task. Original SME notified with reason. SME revises in D-02 (split-view). Revised question enters fast-track Amendment Reviews tab in D-03. Approver approves in D-04 Amendment Reviews tab with mandatory 2FA. Full chain documented in D-12.

### G3 — Notes Content Director Review Toggle
**Gap:** Notes Editor publishes notes directly with no oversight gate. An incorrect Physics formula or Biology diagram used by millions of students has significant educational damage potential.
**Resolution:** Amendment to D-06. Content Director enables per-subject "Notes Require Director Approval" toggle in D-05 Notes Review tab. When enabled, Notes Editor's Publish action → `PENDING_DIRECTOR_REVIEW`. Director reviews in D-05 and approves or returns with comment. Toggle is per-subject, default OFF for all subjects.

### G4 — Question Access Restriction / Content Tiers
**Gap:** All published questions available to all 2,050 tenants. Coaching centres pay for premium exclusive content; Board-specific questions must not appear in coaching exams; exclusive contracts cannot be honoured without access restriction.
**Resolution:** Amendment to D-02 (add `access_level`: Platform-Wide / School Only / College Only / Coaching Only), D-11 (filter by access level, Approver can update access level post-publish without triggering re-review — logged as "Access Amendment" in D-12). Exam engine enforces access level at question-fetch time — not a UI-only filter.

### G5 — Question Expiry for Time-Sensitive Content
**Gap:** GK Current Affairs questions ("Who is the current Finance Minister?") become factually wrong after events change. No expiry mechanism means stale questions remain in active exam pools. At 74K concurrent, one outdated Current Affairs question = mass wrong "correct" answers and rank distortion.
**Resolution:** Amendment to D-02 (add `content_type`: Evergreen/Current Affairs/Time-Sensitive; `valid_until` date required if not Evergreen), D-05 (Expiry Monitor tab), D-11 (expiry filters), D-14 (Content Freshness tab). Celery beat task runs nightly: questions past `valid_until` → auto-archived (removed from exam pool, not deleted), Content Director notified.

### G6 — SME Question Performance Insights
**Gap:** SMEs author questions with no feedback loop on how students actually performed. A SME marks a question "Medium" but 85% get it wrong. No feedback loop means difficulty calibration never improves, exam papers remain unbalanced.
**Resolution:** Amendment to D-01 (add "Performance Data" tab: per published question — % correct, A/B/C/D distribution, realized difficulty vs tagged difficulty, discrimination index). Data from Div F exam results API (Celery task runs after each exam result publication). Questions with >20% divergence between realized and tagged difficulty flagged for SME attention and auto-listed in D-13 Difficulty Calibration tab for Approver re-tagging.

### G7 — Committee Review for High-Stakes Questions
**Gap:** Single reviewer for UPSC/State Board questions affecting students' futures. If one reviewer misses a nuanced error in History/Polity, it goes straight to Approver and publishes.
**Resolution:** Amendment to D-02 (SME can flag question as "High Stakes"), D-03 (Reviewer can flag; committee-flagged questions show "Requires 2 Reviewers" badge; second reviewer sees question only after first has passed — sequential, not parallel; D-04 receives only when both have passed), D-15 (Content Director enables committee review for entire subject).

### G8 — Emergency Bulk Unpublish (Paper Leak Response)
**Gap:** If an exam paper is leaked, 50–500 questions must be immediately withdrawn from all active and upcoming exam pools. Single-question unpublish would take hours at this volume.
**Resolution:** Amendment to D-04. "Emergency Bulk Unpublish": multi-select up to 500 questions → reason category (Paper Leak/Critical Factual Error/Court Order/Copyright Infringement) → type "EMERGENCY" + 2FA re-prompt → Celery high-priority task removes all from exam engine active pool and upcoming exam paper assignments in < 60 seconds → Content Director auto-notified → Div F Exam Operations Manager notified if active exam affected → per-question D-12 audit entry. Available to Question Approver (Role 29) only.

### G9 — Comprehension Passage & Linked Question Sets
**Gap:** SSC CGL, UPSC Prelims, CHSL, and State Board exams all include Reading Comprehension passages with 4–6 MCQs linked to a single passage. D-02 only supports standalone MCQs. English SME (23) and GK SME (24) cannot author a significant portion of their required exam content — comprehension-type questions — without a passage/stimulus concept. Without this, the question bank is structurally incomplete for 3 of the 8 supported exam types.
**Resolution:** Amendment to D-02. Add "Create Passage Set" mode: passage editor (rich text + images, 50–2,000 words, subject + exam type tags), SME attaches 2–8 MCQs to the passage. All questions in a set share a `content_question_set` parent. Set questions move to `UNDER_REVIEW` together; Reviewer sees passage + all linked MCQs in one unified view. Reviewer returns specific questions (not necessarily the whole set) unless the passage itself has errors. Approver approves questions individually but cannot publish any until all in the set reach `PENDING_APPROVAL`. Data models: `content_question_set`, `content_question_set_items`. English and GK subjects show passage-set mode by default; all other subjects can optionally enable.

### G10 — Bulk Retag on Taxonomy Restructure
**Gap:** D-09 correctly blocks archiving a taxonomy node that has published questions tagged to it ("must reassign first") but provides no UI to perform the bulk reassignment. Every annual exam syllabus revision (UPSC restructures its GK pattern, RRB NTPC adds new topic clusters) requires bulk-moving thousands of questions to restructured subtopics. Without a bulk retag tool, taxonomy restructuring is impossible in practice — all 8 exam syllabi change annually to some degree.
**Resolution:** Amendment to D-09. Archive node → system shows count of affected questions (all states: published + in-pipeline) → "Bulk Retag to..." target node selector (same subject only, cross-subject retag blocked) → confirmation modal → Celery async task retagging all affected questions → live HTMX progress bar → completion notification + D-12 audit entry ("Taxonomy Retag") per question. Re-tag is metadata-only: no re-review triggered, no workflow interruption for questions already in review or pending approval. Content Director and Question Approver can trigger; SMEs cannot. Data model: `content_taxonomy_retag_job`.

### G11 — Director Broadcast Announcements to Content Team
**Gap:** Content Director has no mechanism to broadcast communications to SMEs or other Div D staff. Syllabus change notifications, quality policy updates, production target revisions, and urgent content alerts (e.g. "All GK SMEs: avoid Current Affairs questions about Election Commission until verdict") currently happen outside the platform (WhatsApp/email). These out-of-band communications are not audited, not tracked for acknowledgement, and create no paper trail for compliance or disputes.
**Resolution:** Amendment to D-05 (add Announcements tab) + Amendment to D-01 (add Announcements tab + KPI strip badge). Director creates announcements with target audience (All Div D / specific subjects), urgency (Info / Warning / Action Required), and expiry date. SMEs see Action Required announcements as a persistent amber banner in D-01 until explicitly acknowledged. Read count tracked per announcement. Data models: `content_director_announcements`, `content_announcement_reads`.

### G12 — Concurrent Exam Pool Adequacy Monitor
**Gap:** D-14 (Syllabus Coverage) tracks *question count per topic vs a static target* — but at 74,000 simultaneous exam submissions, each consuming questions from the shared pool, the real question is not "do we have 500 questions on this topic?" but "do we have enough questions that, when 74K exams each pick 5 questions from this topic, the same question does not appear in more than 1% of simultaneous papers?" A question repeated across 74K concurrent exams is a paper integrity failure — at school level (1,000 schools × 1,000 students), students from the same institution could be sitting adjacent and sharing the same paper. Static count targets cannot capture this risk. No page currently shows the pool adequacy ratio vs concurrent exam demand.
**Resolution:** Amendment to D-14. Add **"Pool Adequacy" tab**: per exam type, per topic — shows: Published Pool Size · Estimated Concurrent Exam Demand (from Div F's upcoming exam schedule API) · Questions Per Paper allocated to this topic · Minimum Pool Required (= concurrent_exams × questions_per_topic × reuse_safety_factor, where safety_factor default = 3: each question appears in at most 1-in-3 concurrent papers) · Current Adequacy % (Pool Size / Minimum Required) — green ≥ 100%, amber 70–99%, red < 70%. Director can adjust safety_factor per exam type. Produces "Content Production Priority" view: topics ranked by adequacy deficit (largest gap first) — direct input into SME quota setting in D-10. Celery task refreshes adequacy data from Div F's exam schedule API nightly. Red topics auto-added to D-05 Stale Alerts panel. This converts content production from a count-based target to a demand-responsive target — the operationally correct metric at 74K peak concurrent load.

---

## Implementation Priority Order

```
P0 — Before any content enters the exam engine
  D-01  SME Personal Dashboard       (SMEs need workspace from day 1)
  D-02  Question Authoring & Editor  (source of all MCQ content — the core tool)
  D-03  Question Review Workspace    (quality gate 1 — nothing ships without this)
  D-04  Question Approval & Publish  (quality gate 2 — sole publish authority)
  D-05  Director Command Center      (pipeline visibility before content volume grows)
  D-06  Notes Management             (notes go live in institution portals from onboarding day 1)

P1 — Sprint 2 (before AI pipeline activates + legacy content import begins)
  D-09  Subject-Topic Taxonomy       (taxonomy must exist before SMEs tag any questions)
  D-07  Bulk MCQ Import              (legacy content migration — institutions bring existing banks)
  D-08  AI MCQ Triage               (required before Div C C-15 AI pipeline goes live)
  D-10  Content Calendar & Quota     (needed once ≥ 2 SMEs are producing content)
  D-11  Published MCQ Bank           (reference bank needed by Exam Ops, QA, all SMEs)

P2 — Sprint 3 (quality, oversight, compliance layer)
  D-12  Audit & Version History      (mandatory once first unpublish/amendment occurs)
  D-13  Quality Analytics            (once > 500 questions — patterns become meaningful)
  D-14  Syllabus Coverage            (needed before first exam series is configured by Div F)
  D-15  Reviewer Assignments         (when > 1 reviewer + SLA management critical)
  D-16  Student Feedback Queue       (goes live with first published exam results from Div F)

P3 — Sprint 4
  D-17  Notes Analytics              (when notes library has > 200 published items)
  D-18  Reports & Export             (when Content Director needs scheduled offline reporting)
```

---

## Key Architectural Decisions

| Decision | Approach | Why |
|---|---|---|
| Single shared `content` schema (not per-tenant) | Questions are platform assets, not tenant assets | Tenants get access to questions, not ownership. 2M+ question bank cannot be replicated across 2,050 schemas |
| Only Approver can publish MCQs | `content.publish_question` permission assigned to Role 29 only — checked at view AND model layer | One wrong question at 74K concurrent = mass rank distortion. Double-gate (Review + Approve) is the only acceptable control |
| Duplicate detection via pgvector (not external API) | Cosine similarity on `content_question_embeddings` with HNSW index | No per-query API cost. 2M questions × ~1,536-dim embeddings feasible in PostgreSQL. Embeddings pre-computed by Celery on save-draft, adds < 500ms latency async |
| AI questions enter via D-08 triage, not directly to review queue | Human screening layer before review | AI hallucination rate ~15% on Indian exam content. Without triage, Reviewer queue floods with bad questions and SLA collapses |
| Question expiry for Current Affairs | `valid_until` date field + nightly Celery archive task | GK questions about "current" events become factually wrong. Expired questions in active exams = wrong "correct" answers at scale |
| Access restriction at question level | `access_level` field enforced by exam engine at question-fetch time — not a UI filter | Commercial viability: coaching centres pay for exclusive content; Board-specific questions must not appear in coaching exams |
| Committee review as optional per-subject config | D-15 toggle — not hardcoded into pipeline | Not all subjects need it. UPSC/State Board do. Math/CS probably do not. Config avoids over-engineering the default pipeline |
| Emergency bulk unpublish via Celery high-priority queue | Dedicated high-priority Celery queue, not default | Paper leak response window is minutes. Default queue has other jobs ahead. Dedicated queue ensures bulk unpublish completes in < 60s for 500 questions |
| Amendment review as a distinct state | `AMENDMENT_REVIEW` state, fast-track queue in D-03 and D-04 | Published questions with errors cannot go through normal pipeline — they need immediate attention above all other queue items |
| No Redis anywhere | ORM-first + Memcached (django.core.cache) for taxonomy and aggregate snapshots | Taxonomy tree (~1,800 nodes): Memcached TTL 10 min. Pipeline counts: annotated ORM queries. Question bank search: PostgreSQL GIN index on `tsvector`. Zero Redis |
| Question embeddings in shared schema | `content_question_embeddings` table with pgvector HNSW index (ef_construction=400, m=16) | ~2M questions × 1,536 dims = ~18GB index. Shared schema means all SMEs, Reviewers, and Approvers use the same duplicate detection pool |

---

## Cross-Division Integration Points

| Integration | Direction | What Flows | Via | Div D Page |
|---|---|---|---|---|
| Div C C-15 (AI Pipeline) | C-15 → D-08 | AI-generated question batches | Internal API → `content_ai_question_queue` table | D-08 AI Triage |
| Div C C-16 (AI Cost Monitor) | D-08 → C-16 | Acceptance rate per batch (quality signal for cost optimisation) | Shared DB read by C-16 | D-08 |
| Div F Exam Operations | D-11 → Div F | Published question pool (access-level enforced) | Div F reads from shared `content` schema | D-11, D-04 |
| Div F Results module | Div F → D-16 | Student question flag events | Internal API push → `content_student_question_flag` | D-16 Feedback Queue |
| Div F Results module | Div F → D-01 | Per-question exam performance data | Aggregated by Celery after each exam result publish | D-01 Performance Tab, D-13 Difficulty Calibration |
| Div B Syllabus Builder (B-10) | B-10 → D-09 | Official exam syllabus topic structures | Shared taxonomy reference table | D-09 Taxonomy |
| Div B Exam Pattern Builder (B-12) | D-14 → B-12 | Difficulty distribution targets per exam type | Shared DB read | D-14 Syllabus Coverage |
| Div B Test Series Manager (B-11) | D-11 → B-11 | Published question bank (access-controlled) | Shared DB read | D-11 |
| Institution portal (all 2,050 tenants) | Institution → D-06 | Faculty-uploaded notes files | S3 `notes-raw/` landing bucket | D-06 Incoming Queue |
| Div H Data Analytics | D-11, D-13 → Div H | Content quality metrics, publication rates | Shared DB read by EventBridge pipeline | D-13, D-18 |

---

## Compliance Obligations for Division D

| Regulation | Obligation | Deadline / Trigger | Owner | Covered In |
|---|---|---|---|---|
| DPDPA 2023 | SME identity (name, email, IP) in audit logs is PII — stored in ap-south-1 only, never in CSV/PDF exports | Always | Content Director | D-12, D-18 |
| DPDPA 2023 | Student-flagged content in D-16 shows flag count only in UI — full student ID in audit log only | Always | Content Director | D-16 |
| POCSO Act 2012 | Question and note content involving minors must not be explicit — content moderation flag in D-02 and D-06 for any content mentioning minors | On every submission | Content Director + Approver | D-02, D-06 |
| IT Act 2000 §43A | All question bank content is EduForge IP — PDF exports carry watermark, every export action audit-logged per question | On every export | Content Director | D-18, D-12 |
| Copyright compliance | `source_attribution` field mandatory in D-02 — "Adapted from textbook" or "Past exam paper" tracked, never published as "Original" if adapted | On every question | Content Director | D-02 |
| Exam paper secrecy | Questions tagged to upcoming future exams are not exportable until exam date passes | Always | Content Director + Approver | D-18, D-04 |

---

## Functional Coverage Matrix — All 13 Roles

| Role | All Jobs Covered? | Pages | Gaps Resolved |
|---|---|---|---|
| Content Director (18) | ✅ Complete | D-05 · D-09 · D-10 · D-14 · D-15 · D-13 · D-08 · D-16 · D-18 · D-11 · D-12 | G3 · G4 · G5 (monitor) · G7 (config) · G8 (notify) |
| SME — Mathematics (19) | ✅ Complete | D-01 · D-02 (LaTeX toolbar) · D-07 · D-11 · D-09 (read) | G1 · G5 (Evergreen) · G6 (performance) |
| SME — Physics (20) | ✅ Complete | D-01 · D-02 (circuit+optics toolbar) · D-07 · D-11 · D-09 (read) | G1 · G6 |
| SME — Chemistry (21) | ✅ Complete | D-01 · D-02 (formula+molecular toolbar) · D-07 · D-11 · D-09 (read) | G1 · G6 |
| SME — Biology (22) | ✅ Complete | D-01 · D-02 (annotated diagram) · D-07 · D-11 · D-09 (read) | G1 · G6 |
| SME — English (23) | ✅ Complete | D-01 · D-02 (rich text) · D-07 · D-11 · D-09 (read) | G1 · G6 |
| SME — General Knowledge (24) | ✅ Complete | D-01 · D-02 (rich text + valid_until) · D-07 · D-11 · D-09 (read) | G1 · G5 · G6 |
| SME — Reasoning (25) | ✅ Complete | D-01 · D-02 (pattern/matrix image upload) · D-07 · D-11 · D-09 (read) | G1 · G6 |
| SME — Computer Science (26) | ✅ Complete | D-01 · D-02 (code block + syntax highlight) · D-07 · D-11 · D-09 (read) | G1 · G6 |
| SME — Regional Language (27) | ✅ Complete | D-01 · D-02 (Telugu/Hindi/Urdu IME + script validation) · D-07 · D-11 · D-09 (read) | G1 · G6 |
| Question Reviewer (28) | ✅ Complete | D-03 · D-08 · D-11 (duplicate check) · D-15 (own assignment + OOO) · D-13 (own metrics) | G7 (committee review) |
| Question Approver (29) | ✅ Complete | D-04 · D-11 · D-12 · D-16 · D-13 | G2 · G4 (re-tag) · G5 (extend) · G7 · G8 (emergency) |
| Notes Editor (30) | ✅ Complete | D-06 · D-17 | G3 (director toggle) |

---

*Last updated: 2026-03-20*
*Total pages: 20 (D-01 to D-20)*
*Roles covered: 13 (Roles 18–30)*
*Gaps identified (original): 12 (G1–G12) — all resolved via amendments to existing pages*
*Additional gaps found in deep review: 22 (8 Critical · 10 Important · 4 Minor) — resolved via D-19, D-20 (new pages) + amendments to existing specs (see individual page Section 9 and inline amendment notes)*
*Amendments per page: D-01 (G6, G11, SME-OOO, Import-History-tab) · D-02 (G1, G4, G5, G7, G9, Autosave-conflict) · D-03 (G7, Quick-Template-CRUD, Passage-Set-review, Committee-deadlock) · D-04 (G2, G7, G8, Archive-action, Passage-Set-approval) · D-05 (G3, G5, G11, Escalation-tracking, SME-reassign) · D-06 (G3, Notes-audit-view, Multi-subject-toggle-rule) · D-07 (G1, Session-persistence) · D-08 (AI-threshold-visible) · D-09 (G10, Exam-type-mgmt, Subject-mgmt) · D-11 (G2, G4, G5, Notes-tab-full-spec, Archive-action) · D-13 (G6, Edge-cases) · D-14 (G5, G12) · D-15 (G7, Reviewer-perf-targets, Committee-deadlock) · D-19 (new) · D-20 (new)*
*Status: Pages list complete — all 20 individual page spec files complete*
