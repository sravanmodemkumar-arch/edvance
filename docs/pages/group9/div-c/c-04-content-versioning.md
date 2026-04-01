# C-04 — Content Versioning & Updates

> **URL:** `/content-partner/quality/versions/` (partner view) · `/internal/quality/versions/` (admin view)
> **File:** `c-04-content-versioning.md`
> **Priority:** P2
> **Roles:** Content Partner (author) · EduForge Editor (reviewer) · EduForge QA Lead (final approval)

---

## 1. Correction Submission (Partner View)

```
SUBMIT CORRECTION — Question QID-884210 (Currently Live — Version 1)
Partner: Dr. Venkat Rao (CP-00472) | Published: 2026-03-30

  CURRENT VERSION (v1 — LIVE):
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Q: A cistern can be filled by pipe A in 12 hours and by pipe B       │
  │     in 15 hours. A third pipe C can empty the full cistern in         │
  │     10 hours. If all three pipes are opened together, how long        │
  │     will it take to fill the cistern?                                  │
  │                                                                        │
  │  (A) 20 hours   (B) 30 hours   (C) 40 hours   (D) 60 hours          │
  │                                                                        │
  │  ANSWER KEY: (A) 20 hours                                              │
  │  EXPLANATION: Rate A = 1/12, Rate B = 1/15, Rate C = -1/10            │
  │  Combined = 1/12 + 1/15 - 1/10 = 5/60 + 4/60 - 6/60 = 3/60 = 1/20  │
  │  Time = 20 hours                                                       │
  │  STATUS: LIVE | Attempts: 6,840 | Student Reports: 14                  │
  └─────────────────────────────────────────────────────────────────────────┘

  STUDENT REPORTS (14 total):
  ┌──────────────────────────────────────────────────────────────────────┐
  │  "Answer key says 20 hours but I calculated 60 hours. The net      │
  │   rate is 1/12 + 1/15 - 1/10 = (5+4-6)/60 = 3/60 = 1/20.         │
  │   Wait, that IS 20 hours. Hmm, but option D says 60 hours and      │
  │   the official SSC 2019 key says 60 hours for a similar question   │
  │   with different values. I think this is fine actually."            │
  │   — Student report #1 (RESOLVED: answer key correct)               │
  │                                                                     │
  │  "The explanation says 5/60 + 4/60 - 6/60 = 3/60. But actually    │
  │   the LCM approach gives: in 1 hr A fills 5 parts, B fills 4      │
  │   parts, C empties 6 parts. Net = 3 parts. Total capacity = 60.   │
  │   Time = 60/3 = 20. So the answer IS correct. But the             │
  │   explanation should show the LCM method too for clarity."         │
  │   — Student report #7 (VALID: explanation improvement needed)      │
  └──────────────────────────────────────────────────────────────────────┘

  CORRECTION FORM:
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  CORRECTION TYPE:                                                      │
  │  ( ) Wrong answer key    (x) Explanation improvement                   │
  │  ( ) Question text fix   ( ) Option text fix   ( ) Metadata fix       │
  │                                                                        │
  │  SEVERITY:                                                             │
  │  ( ) CRITICAL — wrong answer key (fast-track 24h review)              │
  │  (x) MODERATE — explanation/clarity fix (standard 72h review)         │
  │  ( ) MINOR    — typo/formatting (auto-approve if no logic change)     │
  │                                                                        │
  │  PROPOSED CHANGES (v2):                                                │
  │  ┌───────────────────────────────────────────────────────────────────┐ │
  │  │  Answer Key: (A) 20 hours  [NO CHANGE]                          │ │
  │  │                                                                   │ │
  │  │  Explanation (UPDATED):                                          │ │
  │  │  Method 1 (Rate): 1/12 + 1/15 - 1/10 = 5/60 + 4/60 - 6/60     │ │
  │  │  = 3/60 = 1/20. Time = 20 hours.                                │ │
  │  │                                                                   │ │
  │  │  Method 2 (LCM): LCM(12,15,10) = 60. In 1 hour: A fills 5     │ │
  │  │  parts, B fills 4 parts, C empties 6 parts. Net = 3 parts/hr.  │ │
  │  │  Total capacity = 60 parts. Time = 60/3 = 20 hours.            │ │
  │  └───────────────────────────────────────────────────────────────────┘ │
  │                                                                        │
  │  CHANGE REASON: "Adding LCM method to explanation per student         │
  │  feedback. Many SSC aspirants prefer the LCM shortcut over the        │
  │  fractional rate method."                                              │
  │                                                                        │
  │  [Submit Correction]  [Preview Diff]  [Cancel]                         │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Version History (Per-Question Timeline)

```
VERSION HISTORY — Question QID-770438
Partner: EduPrime (CP-00318) | Subject: General Awareness | Exam: SSC CGL

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  CURRENT: Version 3 (LIVE since 2026-03-15)                           │
  │                                                                        │
  │  TIMELINE:                                                             │
  │                                                                        │
  │  v1  2025-09-10  ARCHIVED                                             │
  │  ├─ Published in batch BTH-2025-09-10-00318-028                       │
  │  ├─ Q: "Who was the first Speaker of Lok Sabha?"                      │
  │  ├─ Answer: (B) G.V. Mavalankar                                       │
  │  ├─ Attempts: 12,400 | Quality Score: 74                              │
  │  ├─ Issue: Option (C) listed "Hukam Singh" but misspelled as          │
  │  │  "Hukum Singh". 8 student reports.                                  │
  │  └─ Correction submitted: 2025-11-22                                   │
  │                                                                        │
  │  v2  2025-11-24  ARCHIVED                                             │
  │  ├─ Fast-track review: 18 hours (MINOR correction — typo fix)         │
  │  ├─ Change: Option (C) "Hukum Singh" → "Hukam Singh"                  │
  │  ├─ Approved by: QA Lead #QA-0008                                      │
  │  ├─ Attempts (after v2): 3,200 | Quality Score: 78                    │
  │  ├─ Issue: Answer key (B) G.V. Mavalankar is correct for "first       │
  │  │  Speaker" but explanation did not mention he served 1952-1956.      │
  │  │  Also, question could be confused with "first pro-tem Speaker"     │
  │  │  (which was also Mavalankar). 4 student reports.                    │
  │  └─ Correction submitted: 2026-03-12                                   │
  │                                                                        │
  │  v3  2026-03-15  LIVE                                                  │
  │  ├─ Standard review: 62 hours (MODERATE — explanation enhancement)    │
  │  ├─ Change: Explanation updated to clarify "first elected Speaker      │
  │  │  of Lok Sabha (1952-1956)" and distinguish from pro-tem role       │
  │  ├─ Approved by: QA Lead #QA-0012                                      │
  │  ├─ Attempts (after v3): 1,800 | Quality Score: 84                    │
  │  └─ Student reports since v3: 0                                        │
  │                                                                        │
  │  VERSION DIFF (v2 → v3):                                               │
  │  ┌───────────────────────────────────────────────────────────────────┐ │
  │  │  - Explanation: "G.V. Mavalankar was the first Speaker of the   │ │
  │  │    Lok Sabha."                                                    │ │
  │  │  + Explanation: "G.V. Mavalankar was the first elected Speaker  │ │
  │  │    of the Lok Sabha, serving from 15 May 1952 to 27 February   │ │
  │  │    1956. He also served as the pro-tem Speaker before his       │ │
  │  │    formal election. He should not be confused with the first    │ │
  │  │    Deputy Speaker, M. Ananthasayanam Ayyangar."                 │ │
  │  └───────────────────────────────────────────────────────────────────┘ │
  │                                                                        │
  │  [View v1]  [View v2]  [View v3 (Current)]  [Compare Any Two]         │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Bulk Correction Workflow (Partner & Admin View)

```
BULK CORRECTION — Partner: QuizNinja (CP-00891)
Reason: SSC CGL 2025 Tier-I official answer key released on 2026-03-25

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  CONTEXT:                                                              │
  │  SSC released the official answer key for CGL 2025 Tier-I on          │
  │  25-Mar-2026. QuizNinja has 340 questions tagged to SSC CGL           │
  │  that were written before the official key was available. After        │
  │  cross-referencing, 7 questions have answer keys that conflict        │
  │  with the official SSC position.                                       │
  │                                                                        │
  │  BULK CORRECTION REQUEST:                                              │
  │  Correction ID: CORR-BULK-2026-03-26-00891-001                        │
  │  Type: CRITICAL — Wrong answer keys (fast-track 24h)                   │
  │  Questions affected: 7                                                 │
  │                                                                        │
  │  ┌──────────────┬────────────┬────────────┬──────────────────────────┐ │
  │  │ QID          │ Current Key│ Correct Key│ SSC Reference            │ │
  │  ├──────────────┼────────────┼────────────┼──────────────────────────┤ │
  │  │ QID-990112   │ (B)        │ (C)        │ CGL 2025 T1 Q.42        │ │
  │  │ QID-990118   │ (A)        │ (D)        │ CGL 2025 T1 Q.78        │ │
  │  │ QID-990134   │ (D)        │ (A)        │ CGL 2025 T1 Q.103       │ │
  │  │ QID-990141   │ (C)        │ (B)        │ CGL 2025 T1 Q.117       │ │
  │  │ QID-990155   │ (A)        │ (C)        │ CGL 2025 T1 Q.129       │ │
  │  │ QID-990162   │ (B)        │ (A)        │ CGL 2025 T1 Q.141       │ │
  │  │ QID-990178   │ (D)        │ (B)        │ CGL 2025 T1 Q.148       │ │
  │  └──────────────┴────────────┴────────────┴──────────────────────────┘ │
  │                                                                        │
  │  IMPACT ANALYSIS (auto-computed):                                      │
  │  Total student attempts on affected questions: 28,400                  │
  │  Students who answered "correctly" per old key but wrong per new: ~18% │
  │  Mock tests containing affected questions: 12                          │
  │  Student notifications required: YES (students who attempted these)    │
  │                                                                        │
  │  REVIEW STATUS:                                                        │
  │  [x] Partner submitted bulk correction          26-Mar 09:00           │
  │  [x] Auto-validation: SSC official key uploaded  26-Mar 09:02          │
  │  [x] Editor fast-track review                    26-Mar 14:30          │
  │  [x] QA Lead approval                            26-Mar 16:00          │
  │  [x] v2 published for all 7 questions            26-Mar 16:05          │
  │  [x] Student notification sent                   26-Mar 16:10          │
  │  [x] Mock test scores recalculated               26-Mar 16:30          │
  │                                                                        │
  │  TOTAL TIME: 7 hours (within 24h fast-track SLA)                       │
  └─────────────────────────────────────────────────────────────────────────┘

  STUDENT NOTIFICATION (sent to 28,400 students):
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  "Important: 7 questions in SSC CGL mock tests have been updated      │
  │   with corrected answer keys based on the official SSC CGL 2025       │
  │   Tier-I answer key released on 25-Mar-2026. Your scores on           │
  │   affected mock tests have been automatically recalculated.           │
  │   [View Updated Scores]  [View Affected Questions]"                   │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `POST` | `/api/v1/content-partner/quality/versions/questions/{qid}/corrections/` | Submit a correction for a published question |
| 2 | `GET` | `/api/v1/content-partner/quality/versions/questions/{qid}/history/` | Full version history for a question |
| 3 | `GET` | `/api/v1/content-partner/quality/versions/questions/{qid}/diff/{v1}/{v2}/` | Diff between two versions of a question |
| 4 | `POST` | `/api/v1/content-partner/quality/versions/bulk-corrections/` | Submit a bulk correction request (multiple questions) |
| 5 | `GET` | `/api/v1/content-partner/quality/versions/bulk-corrections/{corr_id}/status/` | Bulk correction status and impact analysis |
| 6 | `POST` | `/api/v1/content-partner/quality/versions/bulk-corrections/{corr_id}/approve/` | QA Lead approves a bulk correction |
| 7 | `GET` | `/api/v1/content-partner/quality/versions/partners/{partner_id}/corrections/` | All corrections submitted by a partner |
| 8 | `POST` | `/api/v1/content-partner/quality/versions/questions/{qid}/rollback/` | Rollback to a previous version (admin only) |

---

## 5. Business Rules

- When a published question is found to have a wrong answer key, the correction follows a fast-track review path with a 24-hour SLA from the moment the correction is submitted. Wrong answer keys are classified as CRITICAL severity because every student who attempts that question between now and when the correction goes live is potentially learning the wrong answer. The fast-track path skips peer review and goes directly to QA Lead approval, since the correction is typically backed by an authoritative source (official answer key from the conducting body, or a clear mathematical proof). The QA Lead must approve within 8 hours of receiving the fast-track request. Once approved, version 2 of the question goes live immediately, version 1 is archived (not deleted — it remains in the version history for audit purposes), and all student attempts on version 1 are flagged for score recalculation. Students who previously attempted mock tests containing the corrected question receive a notification explaining the change and a link to view their updated scores. The partner's quality score is not penalised for self-reported corrections (since self-reporting is the desired behaviour), but if the wrong answer key was discovered by EduForge's editorial team or through student reports rather than the partner, the Accuracy component for that question is set to 0/100.

- Every edit to a published question — whether it changes the answer key, question text, options, explanation, metadata, or difficulty tag — creates a new immutable version. Versions are numbered sequentially (v1, v2, v3...) and each version records the timestamp, the author of the change, the QA Lead who approved it, the specific fields that changed (stored as a JSON diff), and the reason for the change. No version is ever deleted; archived versions remain accessible to editors and admins for audit purposes. This immutability is critical for two reasons: first, if a student disputes their mock test score, EduForge can determine which version of the question was live at the time the student attempted the test and verify that scoring was correct against that version's answer key; second, if a partner makes a correction that introduces a new error (e.g., changes the answer from B to C but the correct answer was actually D), the system can roll back to any previous version without data loss. Rollback is an admin-only action that itself creates a new version (e.g., v4 with a note "rollback to v2") rather than deleting v3.

- Bulk corrections are designed for scenarios where an external authoritative source (such as an official answer key released by SSC, UPSC, or a state public service commission) invalidates multiple questions simultaneously. The partner uploads the official answer key document, maps each affected question ID to its corrected answer, and submits the entire batch as a single bulk correction request. The system auto-validates the mapping (ensuring all QIDs exist and belong to the submitting partner, the new answer key references valid options, and the correction actually changes something), computes an impact analysis (how many students attempted the affected questions, how many mock tests are impacted, estimated score changes), and routes the request to the QA Lead for fast-track approval. After approval, all corrected versions go live simultaneously in a single atomic transaction — this prevents a scenario where some questions in a mock test are on v2 while others are still on v1, which would produce inconsistent scoring. The mock test scoring engine then runs a background recalculation job for all affected mock attempts, updating stored scores and generating student notifications.

- MINOR corrections (typo fixes, formatting improvements, LaTeX rendering adjustments) that do not change any answer key, option content, or the logical meaning of the question text or explanation are eligible for auto-approval. The system determines auto-approval eligibility by computing a semantic diff: if the sentence-transformer embedding cosine similarity between the old and new text exceeds 0.98 and no answer key or option has changed, the correction is classified as cosmetic and is approved by the system without human review. This pathway reduces the editorial burden for trivial fixes — a partner correcting "recieve" to "receive" or fixing a broken LaTeX fraction should not need to wait 72 hours for a human reviewer. However, if the cosmetic change alters a number, a proper noun, or any term that could affect the question's meaning (detected via named-entity-recognition and numerical-value extraction), the system reclassifies the correction as MODERATE and routes it through the standard review pipeline. The auto-approval rate for MINOR corrections is approximately 85%, with the remaining 15% escalated due to detected semantic changes that the partner may not have intended.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division C*
