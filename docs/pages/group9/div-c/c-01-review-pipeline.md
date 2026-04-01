# C-01 — Editorial Review Pipeline

> **URL:** `/content-partner/quality/pipeline/` (partner view) · `/internal/quality/pipeline/` (editor view)
> **File:** `c-01-review-pipeline.md`
> **Priority:** P1
> **Roles:** Content Partner (author) · EduForge Editor (reviewer) · EduForge QA Lead (final approval)

---

## 1. Pipeline Overview (Partner View — Batch Status)

```
EDITORIAL REVIEW PIPELINE — Dr. Venkat Rao
Partner ID: CP-00472 | Org: QuizCraft Edu Pvt Ltd | Tier: Gold

  BATCH SUBMITTED: 2026-03-28 14:30 IST
  Batch ID: BTH-2026-03-28-00472-017
  Subject: Quantitative Aptitude | Exam Tag: SSC CGL, SSC CHSL
  Questions: 50 | Language: English

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  PIPELINE STAGES                                                       │
  │                                                                        │
  │  [1] Submission       ████████████  DONE   28-Mar 14:30                │
  │      Format check, metadata validation, LaTeX rendering test           │
  │                                                                        │
  │  [2] Auto-Check       ████████████  DONE   28-Mar 14:32                │
  │      Answer key valid, no blank options, difficulty tag present         │
  │      Result: 48/50 passed | 2 flagged (see below)                      │
  │                                                                        │
  │  [3] Peer Review      ████████░░░░  IN PROGRESS   Assigned: 28-Mar 16:00│
  │      Reviewer: EduForge Editor #E-0187 (Quant specialist)              │
  │      Progress: 36/50 reviewed | ETA: 29-Mar 12:00                      │
  │                                                                        │
  │  [4] QA Lead Approval ░░░░░░░░░░░░  PENDING                           │
  │      Approver: Not yet assigned                                        │
  │                                                                        │
  │  [5] Live             ░░░░░░░░░░░░  PENDING                           │
  │      Target: 31-Mar 14:30 (72h SLA)                                    │
  │                                                                        │
  │  SLA STATUS: [ON TRACK] 48h remaining                                  │
  └─────────────────────────────────────────────────────────────────────────┘

  AUTO-CHECK FLAGS (2 questions):
  ┌──────┬────────────────────────────────────────────────────────────┐
  │ Q#   │ Issue                                                      │
  ├──────┼────────────────────────────────────────────────────────────┤
  │ Q-14 │ LaTeX render failure: \frac{3x+}{2} — incomplete expr     │
  │ Q-38 │ Answer key marks Option E but only 4 options (A-D) exist   │
  ├──────┼────────────────────────────────────────────────────────────┤
  │      │ ACTION REQUIRED: Fix & resubmit flagged questions          │
  │      │ [Edit Q-14]  [Edit Q-38]  [Resubmit Flagged]              │
  └──────┴────────────────────────────────────────────────────────────┘
```

---

## 2. Editor Review Interface (Internal — Per Question)

```
PEER REVIEW — Question Q-14 (Resubmitted after auto-check fix)
Batch: BTH-2026-03-28-00472-017 | Reviewer: Editor #E-0187

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  QUESTION TEXT:                                                         │
  │  A train 240m long crosses a pole in 16 seconds. How long will         │
  │  it take to cross a platform 360m long?                                │
  │                                                                        │
  │  (A) 36 sec   (B) 40 sec   (C) 42 sec   (D) 48 sec                   │
  │                                                                        │
  │  ANSWER KEY: (B) 40 sec                                                │
  │  EXPLANATION:                                                          │
  │  Speed = 240/16 = 15 m/s                                               │
  │  Total distance = 240 + 360 = 600m                                     │
  │  Time = 600/15 = 40 sec                                                │
  │                                                                        │
  │  METADATA:                                                             │
  │  Subject: Quant | Topic: Time, Speed & Distance | Difficulty: 3/5      │
  │  Exam Tags: SSC CGL, SSC CHSL | Source: Original                       │
  │  Language: English | LaTeX: None                                        │
  ├─────────────────────────────────────────────────────────────────────────┤
  │  REVIEWER CHECKLIST:                                                    │
  │  [x] Question text is clear and unambiguous                            │
  │  [x] All options are plausible (no obviously absurd distractor)        │
  │  [x] Answer key is correct (verified manually)                         │
  │  [x] Explanation is complete and step-by-step                          │
  │  [x] Difficulty tag matches actual difficulty                          │
  │  [ ] No copyright/plagiarism concern                                   │
  │  [ ] Exam tag is appropriate for this question                         │
  │                                                                        │
  │  REVIEWER VERDICT:                                                     │
  │  ( ) Approve   ( ) Request Changes   ( ) Reject                        │
  │                                                                        │
  │  REVIEWER NOTES:                                                       │
  │  ┌───────────────────────────────────────────────────────────────────┐ │
  │  │ "Question is clean. Answer verified. Standard TSD type — good    │ │
  │  │  for SSC CGL Tier-I level. Approving."                           │ │
  │  └───────────────────────────────────────────────────────────────────┘ │
  │                                                                        │
  │  [Approve]  [Request Changes]  [Reject]  [Flag Plagiarism]            │
  │                                                                        │
  │  NAVIGATION: [<< Prev Q-13]  Q-14 of 50  [Next Q-15 >>]              │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. QA Lead Approval Dashboard (Internal)

```
QA LEAD DASHBOARD — Pending Approvals
QA Lead: Priya Sharma (#QA-0012) | Queue: 14 batches | SLA breaches: 0

  ┌──────┬──────────────────┬────────────┬─────┬──────────┬──────────┬────────┐
  │ #    │ Batch ID         │ Partner    │ Qs  │ Peer Rev │ SLA Left │ Action │
  ├──────┼──────────────────┼────────────┼─────┼──────────┼──────────┼────────┤
  │  1   │ BTH-...-00472-017│ Dr.V.Rao   │  50 │ 50/50 OK │ 26h      │[Review]│
  │  2   │ BTH-...-00318-042│ EduPrime   │ 100 │ 98/100   │ 14h      │[Review]│
  │  3   │ BTH-...-00891-008│ QuizNinja  │  30 │ 30/30 OK │ 52h      │[Review]│
  │  4   │ BTH-...-00156-023│ AcadBridge │  75 │ 71/75    │  8h  !!  │[URGENT]│
  │  5   │ BTH-...-00644-011│ KnowledgeX │  25 │ 25/25 OK │ 38h      │[Review]│
  │ ...  │ ...              │ ...        │ ... │ ...      │ ...      │ ...    │
  ├──────┴──────────────────┴────────────┴─────┴──────────┴──────────┴────────┤
  │  CURRENT AFFAIRS FAST TRACK (24h SLA):                                    │
  │  BTH-...-00472-018 | Dr.V.Rao | 10 Qs | Current Affairs Mar 2026        │
  │  Peer Review: DONE | SLA Left: 6h | [FAST-TRACK REVIEW]                  │
  ├───────────────────────────────────────────────────────────────────────────┤
  │  BATCH SUMMARY — BTH-...-00472-017:                                       │
  │  Peer approved: 48 | Peer flagged: 2 (partner fixed, re-reviewed)        │
  │  Plagiarism check: CLEAR | Quality score (batch avg): 82/100             │
  │  Recommendation: APPROVE ALL 50                                           │
  │                                                                           │
  │  [Approve Batch]  [Approve with Exceptions]  [Send Back to Peer Review]  │
  └───────────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `POST` | `/api/v1/content-partner/quality/batches/` | Submit a new batch for review |
| 2 | `GET` | `/api/v1/content-partner/quality/batches/{batch_id}/status/` | Batch pipeline status with per-stage detail |
| 3 | `GET` | `/api/v1/content-partner/quality/batches/{batch_id}/flags/` | Auto-check flags for a batch |
| 4 | `PATCH` | `/api/v1/content-partner/quality/batches/{batch_id}/questions/{qid}/` | Resubmit a flagged question after partner fix |
| 5 | `POST` | `/api/v1/content-partner/quality/review/{qid}/verdict/` | Editor submits review verdict (approve/changes/reject) |
| 6 | `POST` | `/api/v1/content-partner/quality/batches/{batch_id}/approve/` | QA Lead approves an entire batch |
| 7 | `GET` | `/api/v1/content-partner/quality/pipeline/dashboard/` | QA Lead dashboard — all pending batches |
| 8 | `POST` | `/api/v1/content-partner/quality/batches/{batch_id}/fast-track/` | Escalate batch to fast-track (24h SLA) |

---

## 5. Business Rules

- Every question submitted by a content partner must pass through the full four-stage pipeline (auto-check, peer review, QA Lead approval, live) before becoming visible to students in any mock test or practice set. There are no exceptions to this rule regardless of the partner's tier, historical quality score, or relationship with EduForge. A Gold-tier partner like Dr. Venkat Rao with a 94/100 quality score still goes through the same pipeline as a newly onboarded Bronze-tier partner. The rationale is that a single wrong answer key reaching a student — especially in a previous-year-question mock — can cause that student to learn an incorrect fact and reproduce it in the actual exam, costing them marks and damaging EduForge's credibility. The pipeline is non-negotiable and the SLA (72 hours standard, 24 hours current affairs) is a commitment to the partner that their content will not languish indefinitely in review.

- The auto-check stage runs within 2 minutes of batch submission and validates every question against a deterministic ruleset: all options must be non-empty, the answer key must reference a valid option index (A-D for 4-option questions, A-E for 5-option), LaTeX expressions must render without errors in MathJax, difficulty tags must be in the 1-5 range, at least one exam tag must be present, and the explanation field must contain at least 50 characters. Questions that fail auto-check are flagged with a specific error code and the partner receives instant notification. The partner can fix and resubmit flagged questions without resubmitting the entire batch. Only after all questions in a batch pass auto-check does the batch advance to peer review. This stage catches approximately 12% of submitted questions on first pass, with the most common failures being incomplete LaTeX expressions (4.2%), missing explanations (3.1%), and invalid answer key references (2.8%).

- Peer review assignment uses a round-robin algorithm weighted by subject expertise and current workload. An SSC Quantitative Aptitude batch is assigned to an editor who has the "quant" specialisation tag and whose current open-review queue is below 200 questions. If no suitable editor is available within 4 hours of the batch entering the peer review stage, the system escalates to the QA Lead for manual assignment. The peer reviewer must verify every question independently — checking the answer key by solving the question themselves (for Quant and Reasoning), verifying factual accuracy against authoritative sources (for GK and Current Affairs), and confirming that the explanation is pedagogically sound. A reviewer who approves more than 3 questions later found to have incorrect answer keys in a 30-day window is flagged for retraining and temporarily removed from the reviewer pool.

- The SLA clock starts at batch submission and measures elapsed wall-clock time, not business hours. A batch submitted on Friday at 6 PM must be live by Monday 6 PM (72 hours) even though the weekend intervenes. Current affairs batches receive a 24-hour SLA because the questions lose relevance rapidly — a question about a cabinet reshuffle announced on March 28 must be live by March 29 to be useful for students preparing for exams in the following weeks. If the SLA is at risk (less than 12 hours remaining and the batch has not reached QA Lead approval), the system sends an escalation alert to the QA Lead and the Content Operations Manager. SLA breach rate is tracked as a platform KPI and the target is below 2% per month. Partners can view SLA countdown on their dashboard and receive push notifications at the 48-hour, 24-hour, and 6-hour marks.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division C*
