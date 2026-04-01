# C-03 — Plagiarism & Duplicate Detection

> **URL:** `/content-partner/quality/plagiarism/` (partner view) · `/internal/quality/plagiarism/` (admin view)
> **File:** `c-03-plagiarism-detection.md`
> **Priority:** P1
> **Roles:** Content Partner (author) · EduForge Editor (reviewer) · EduForge QA Lead (final approval)

---

## 1. Plagiarism Scan Results (Per-Batch Report)

```
PLAGIARISM & DUPLICATE SCAN — Batch BTH-2026-03-28-00472-017
Partner: Dr. Venkat Rao (CP-00472) | Questions: 50 | Scan completed: 28-Mar 14:34

  SCAN ENGINES:
  [1] Normalised Text Hash — exact/near-exact match against 18,42,000+ pool
  [2] Semantic Similarity  — transformer embedding cosine similarity (>= 0.92)
  [3] Cross-Partner Dedup  — matches against all other partners' content
  [4] Source Citation Check — verifies declared source matches known publications

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  SCAN SUMMARY:                                                         │
  │  Total questions scanned:  50                                          │
  │  Clean (no match):         44   ██████████████████████████████████████ │
  │  Duplicate (own content):   2   ██                                    │
  │  Cross-partner duplicate:   1   █                                     │
  │  Source flagged:            2   ██                                    │
  │  Semantic near-match:       1   █                                     │
  │                                                                        │
  │  OVERALL STATUS: 6 FLAGS — review required before peer review stage   │
  └─────────────────────────────────────────────────────────────────────────┘

  DETAILED FLAGS:
  ┌──────┬────────┬──────────────────────────────────────────────────────────┐
  │ Q#   │ Type   │ Detail                                                   │
  ├──────┼────────┼──────────────────────────────────────────────────────────┤
  │ Q-07 │ SELF   │ Exact match with QID-671204 (your batch BTH-...-014).   │
  │      │ DUP    │ Same question text, same options, same answer.           │
  │      │        │ Action: Remove duplicate or modify significantly.        │
  ├──────┼────────┼──────────────────────────────────────────────────────────┤
  │ Q-22 │ SELF   │ Near-exact match with QID-671340 (your batch BTH-014).  │
  │      │ DUP    │ Hash distance: 3 (only numbers changed: 240->250m).     │
  │      │        │ Action: Acceptable if intentional variant. Confirm.      │
  ├──────┼────────┼──────────────────────────────────────────────────────────┤
  │ Q-31 │ CROSS  │ 97.4% text match with QID-442018 by partner EduPrime   │
  │      │ DUP    │ (CP-00318). Submitted 2025-11-02. Already live.         │
  │      │        │ Action: REJECTED — cannot publish duplicate of another  │
  │      │        │ partner's content. Remove or rewrite substantially.      │
  ├──────┼────────┼──────────────────────────────────────────────────────────┤
  │ Q-39 │ SOURCE │ Question matches R.S. Aggarwal "Quantitative Aptitude"  │
  │      │ FLAG   │ Ch. 17, Problem 42 (2023 edition). Source declared:     │
  │      │        │ "Original". Hash match: 94.1% after normalisation.      │
  │      │        │ Action: Cite source or confirm original. If from book   │
  │      │        │ without license, REJECT.                                 │
  ├──────┼────────┼──────────────────────────────────────────────────────────┤
  │ Q-44 │ SOURCE │ Question matches Arihant "SSC Mathematics" Ch. 9,       │
  │      │ FLAG   │ Example 14. Source declared: "Adapted". Similarity:     │
  │      │        │ 89.3%. Adaptation: only changed train length values.    │
  │      │        │ Action: Insufficient adaptation. Rewrite with different │
  │      │        │ problem structure or provide Arihant license proof.      │
  ├──────┼────────┼──────────────────────────────────────────────────────────┤
  │ Q-48 │ SEM    │ Semantic similarity 0.934 with QID-118702 (pool).       │
  │      │ MATCH  │ Different wording but identical mathematical concept    │
  │      │        │ and answer. Not plagiarism but low incremental value.   │
  │      │        │ Action: Advisory only. Partner may keep or replace.      │
  └──────┴────────┴──────────────────────────────────────────────────────────┘

  PARTNER ACTIONS:
  [Resolve Q-07]  [Confirm Q-22]  [Remove Q-31]  [Cite Q-39]  [Rewrite Q-44]
  [Keep Q-48]

  Note: Batch cannot advance to Peer Review until all REJECT-level flags
  (Q-31, Q-39 if uncited, Q-44 if not rewritten) are resolved.
```

---

## 2. Normalised Text Hashing Pipeline (Technical Detail)

```
NORMALISATION & HASHING PIPELINE
Processing: Question Q-39 from Batch BTH-2026-03-28-00472-017

  STEP 1 — RAW TEXT:
  "A train 240 metres long running at 54 km/hr crosses a bridge
   in 20 seconds. What is the length of the bridge?"

  STEP 2 — NORMALISE:
  Remove punctuation, lowercase, strip whitespace, replace numbers
  with placeholders, remove stop words, stem remaining words
  Result: "train NUM metr long run NUM km hr cross bridg NUM second
           length bridg"

  STEP 3 — GENERATE HASH:
  SimHash (64-bit locality-sensitive hash):
  Raw:   0xA3F2 1B4C 7D8E 09F1
  Pool match search: Hamming distance <= 5 from all 18,42,000 hashes

  STEP 4 — MATCHES FOUND:
  ┌────────────┬──────────┬─────────────────────────────────────┐
  │ QID        │ Distance │ Source                               │
  ├────────────┼──────────┼─────────────────────────────────────┤
  │ QID-331045 │ 2        │ R.S. Aggarwal Ch.17 P.42 (indexed) │
  │ QID-772018 │ 4        │ Partner: MathGuru (CP-00211)        │
  │ QID-118702 │ 8        │ Partner: EduPrime (CP-00318)        │
  └────────────┴──────────┴─────────────────────────────────────┘

  STEP 5 — SEMANTIC VERIFICATION (for distance <= 5):
  Compute sentence-transformer embedding (all-MiniLM-L6-v2)
  Cosine similarity with QID-331045: 0.941 — CONFIRMED MATCH
  Cosine similarity with QID-772018: 0.887 — BELOW THRESHOLD (0.92)

  VERDICT: Q-39 matches known publication (R.S. Aggarwal). Flag as SOURCE.

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  REFERENCE DATABASE:                                                    │
  │  18,42,000+ questions in EduForge pool (all partners)                  │
  │  1,24,000+ indexed questions from known publications:                  │
  │    R.S. Aggarwal (12 books)    — 18,400 questions indexed              │
  │    Arihant Publications (28)   — 42,200 questions indexed              │
  │    Kiran Prakashan (15)        — 22,800 questions indexed              │
  │    Lucent's GK                 — 8,600 questions indexed               │
  │    NCERT (Class 6-12)          — 32,000 questions indexed              │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Cross-Partner Deduplication Dashboard (Admin View)

```
CROSS-PARTNER DEDUPLICATION — Admin Dashboard
Period: March 2026 | Scanned: 48,200 new questions | Flagged: 1,840 (3.8%)

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DEDUP SUMMARY BY TYPE:                                                │
  │                                                                        │
  │  Exact duplicates (hash distance 0-2):      420   ███████              │
  │  Near duplicates (hash distance 3-5):        680   ███████████         │
  │  Semantic matches (cosine >= 0.92):          340   ██████              │
  │  Source publication matches:                  400   ███████             │
  │                                                                        │
  │  RESOLUTION STATUS:                                                    │
  │  Auto-resolved (self-dup, partner removed):  980   53.3%               │
  │  Under partner review:                       420   22.8%               │
  │  Escalated to editorial:                     280   15.2%               │
  │  Rejected (confirmed plagiarism):            160    8.7%               │
  ├─────────────────────────────────────────────────────────────────────────┤
  │  TOP OFFENDING PARTNERS (plagiarism rejections this month):            │
  │  ┌──────┬────────────────┬──────┬──────────┬──────────────────────┐    │
  │  │ Rank │ Partner        │ Rej  │ % of Sub │ Status               │    │
  │  ├──────┼────────────────┼──────┼──────────┼──────────────────────┤    │
  │  │  1   │ FastQuiz Edu   │  34  │  8.2%    │ WARNING ISSUED       │    │
  │  │  2   │ PrepKing       │  28  │  6.1%    │ WARNING ISSUED       │    │
  │  │  3   │ StudyMitra     │  22  │  5.5%    │ UNDER INVESTIGATION  │    │
  │  │  4   │ QuizFactory    │  18  │  4.2%    │ WARNING ISSUED       │    │
  │  │  5   │ AcadBridge     │  14  │  2.8%    │ FIRST OFFENSE        │    │
  │  └──────┴────────────────┴──────┴──────────┴──────────────────────┘    │
  │                                                                        │
  │  POLICY: 3 warnings → 30-day suspension → repeat → permanent ban      │
  │                                                                        │
  │  [View Full Report]  [Export CSV]  [Send Warning Letters]              │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `POST` | `/api/v1/content-partner/quality/plagiarism/scan/` | Trigger plagiarism scan for a batch |
| 2 | `GET` | `/api/v1/content-partner/quality/plagiarism/batches/{batch_id}/report/` | Full plagiarism scan report for a batch |
| 3 | `GET` | `/api/v1/content-partner/quality/plagiarism/questions/{qid}/matches/` | Detailed match results for a single question |
| 4 | `POST` | `/api/v1/content-partner/quality/plagiarism/questions/{qid}/resolve/` | Partner resolves a flag (cite source, confirm variant, remove) |
| 5 | `GET` | `/api/v1/content-partner/quality/plagiarism/dashboard/` | Admin deduplication dashboard with monthly stats |
| 6 | `GET` | `/api/v1/content-partner/quality/plagiarism/partners/{partner_id}/history/` | Partner's plagiarism flag history and warning status |
| 7 | `POST` | `/api/v1/content-partner/quality/plagiarism/reference-db/index/` | Admin: index a new publication into the reference database |
| 8 | `GET` | `/api/v1/content-partner/quality/plagiarism/reference-db/stats/` | Reference database statistics (books indexed, question count) |

---

## 5. Business Rules

- Every question submitted to EduForge undergoes a mandatory plagiarism and duplicate detection scan before it can advance from the auto-check stage to peer review. The scan runs four detection engines in parallel: normalised text hashing against the entire pool of 18,42,000+ questions (using SimHash with a Hamming distance threshold of 5 or fewer bits), semantic similarity using sentence-transformer embeddings with a cosine similarity threshold of 0.92, cross-partner deduplication that specifically checks whether the same question has already been submitted by a different partner, and source citation verification against a reference database of 1,24,000+ indexed questions from known competitive exam publications. A question that triggers any engine at the REJECT level (cross-partner exact duplicate, unattributed match with a copyrighted publication) cannot proceed through the pipeline until the partner resolves the flag. Advisory flags (semantic near-match with low incremental value) are informational and do not block the pipeline.

- Questions copied verbatim or near-verbatim from published books such as R.S. Aggarwal, Arihant, Kiran Prakashan, or Lucent's GK are rejected unless the partner holds a valid licensing agreement with the publisher and uploads proof of that agreement to their partner profile. Changing only the numerical values in a problem (e.g., replacing "240 metres" with "300 metres" in a train problem while keeping the identical structure, option pattern, and solution method) is classified as insufficient adaptation and is treated the same as verbatim copying. Genuine adaptation requires changing the problem structure, context, or solution approach — for example, converting a train-platform problem into a boat-stream problem using the same mathematical principle but a fundamentally different scenario. The reference database is continuously expanded by the content operations team, who index new editions of popular competitive exam books within 30 days of publication. Partners are encouraged to declare "Adapted from [Source]" when they use a published problem as inspiration, which triggers a lighter review (the editor verifies the adaptation is substantial) rather than an automatic rejection.

- Cross-partner deduplication ensures that the content pool does not accumulate redundant questions from different partners who independently submit the same or nearly identical content. When Partner A submits a question that matches Partner B's existing live question at a hash distance of 2 or fewer, the submission is rejected for Partner A regardless of which partner wrote the question first — the pool already has that question and adding a duplicate provides no value to students. In the case where two partners submit the same question in overlapping batches (both currently in the pipeline), priority is given to the batch that entered the auto-check stage first based on timestamp. The rejected partner receives a detailed notification showing the matching question ID, the matching partner's anonymised identifier (not their name, to prevent inter-partner disputes), and the match score. If the partner believes the match is a false positive (e.g., two genuinely different questions about the same topic that happen to use similar phrasing), they can file a dispute that is reviewed by an EduForge editor within 48 hours.

- The plagiarism detection system maintains a three-strike policy for partners who repeatedly submit copyrighted or duplicated content. The first offense results in a written warning with specific guidance on content originality requirements. The second offense within a 6-month window triggers a second warning and places the partner on "enhanced scrutiny" status where every question in their subsequent batches receives manual plagiarism review by an editor (in addition to the automated scan), which increases review time by approximately 24 hours. The third offense within a 12-month window results in a 30-day suspension during which the partner cannot submit new batches, though their existing live content remains in the pool. A fourth offense results in permanent partnership termination — all their content is reviewed and any confirmed plagiarised questions are removed from the pool. The partner's quality score is also impacted: each plagiarism rejection reduces the Accuracy component by 5 points for the affected batch, reflecting that submitting copied content indicates a lack of diligence in the partner's content creation process.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division C*
