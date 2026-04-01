# D-01 — Eligibility Checker

> **URL:** `/exam/eligibility/check/` (guest) · inline on exam detail (B-01) for authenticated users
> **File:** `d-01-eligibility-checker.md`
> **Priority:** P1
> **Data:** User inputs OR `user_profile` → matched against `exam` rules

---

## 1. Eligibility Check Flow

```
ELIGIBILITY CHECKER — Am I eligible for this exam?

  STEP 1 — YOUR PROFILE  [pre-filled if logged in, manual entry for guest]
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Date of birth:      [ 15 / Jun / 2001 ▼]  → Age: 24 yrs 9 mo     │
  │  Gender:             [ Male ▼ ]                                     │
  │  Category:           [ OBC ▼ ]                                      │
  │  Sub-category:       [ BC-B (AP) ▼ ]                                │
  │  Domicile state:     [ Andhra Pradesh ▼ ]                           │
  │  Highest qualif.:    [ Graduate (B.Com) ▼ ]                         │
  │  Specialisation:     [ Commerce ▼ ]  (needed for subject-specific)  │
  │  Physical: Height:   [ 172 ] cm  Weight: [ 68 ] kg  (for police)   │
  │  Ex-serviceman:      [ No ▼ ]                                       │
  │  PH / Benchmark dis: [ No ▼ ]                                       │
  │                                                                      │
  │  [Check eligibility for: ___________] or [Check all exams →]        │
  └──────────────────────────────────────────────────────────────────────┘

  STEP 2 — RESULT  [computed in real time from exam rules]
  ┌──────────────────────────────────────────────────────────────────────┐
  │  CHECKING: APPSC Group 2 — 2025                                     │
  │                                                                      │
  │  ✅ Age:            24 yrs (limit: 18–42, OBC relaxation: +3 = 45)  │
  │  ✅ Qualification:  Graduate (B.Com) — meets "Graduate" requirement  │
  │  ✅ Domicile:       Andhra Pradesh — AP domicile required: ✅       │
  │  ✅ Category:       OBC (BC-B) — reservation applicable              │
  │  ⬜ Physical:       Not applicable for this exam                     │
  │                                                                      │
  │  VERDICT: ✅ YOU ARE ELIGIBLE for APPSC Group 2 — 2025              │
  │                                                                      │
  │  Posts you qualify for:  All 62 posts (no subject-specific filter)   │
  │  Reservation category:  BC-B (AP reservation roster)                │
  │  [View exam details →]  [Save to My Exams]  [Check another exam]   │
  └──────────────────────────────────────────────────────────────────────┘

  ── ANOTHER EXAMPLE (ineligible) ──────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────────┐
  │  CHECKING: TSPSC Group 1 — 2024                                     │
  │                                                                      │
  │  ✅ Age:            24 yrs (limit: 18–44) ✅                         │
  │  ✅ Qualification:  Graduate ✅                                       │
  │  ❌ Domicile:       Andhra Pradesh — TS domicile REQUIRED ❌         │
  │                                                                      │
  │  VERDICT: ❌ NOT ELIGIBLE — Reason: Telangana domicile required     │
  │           You are an AP domicile. TSPSC Group 1 requires TS domicile│
  │  [Check APPSC Group 1 instead? →] (suggested equivalent)            │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Eligibility Engine Logic

```
ELIGIBILITY ENGINE — Computation Rules

  FOR EACH exam IN active_exams:

    age_check:
      user_age = years_between(user.dob, exam.age_reference_date OR exam.application_end)
      relaxation = LOOKUP(exam.age_relaxations, user.category)
      effective_max = exam.age_max + relaxation.extra_years
      PASS if user_age >= exam.age_min AND user_age <= effective_max

    qualification_check:
      qualification_hierarchy: 10th < 12th < diploma < graduate < pg < phd
      PASS if user.qualification >= exam.qualification_required
      (special cases: B.Ed required → check user.specialisation)
      (special cases: BE/BTech required → check user.degree_type)

    domicile_check:
      IF exam.domicile_required IS NULL → PASS (no domicile requirement)
      IF exam.state_code == user.domicile_state → PASS
      ELSE → FAIL with reason "requires {state} domicile"

    physical_check (if exam has physical_requirements):
      IF exam has physical requirements AND user has physical data:
        Check height, weight, chest, running against exam_post.physical_requirements
        Apply gender + category adjustments
      IF exam has no physical requirements → SKIP

    RESULT:
      ALL checks PASS → ELIGIBLE
      ANY check FAIL → NOT ELIGIBLE (list all failure reasons)
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/exam/eligibility/check/` | Check eligibility for a specific exam (accepts profile + exam_id) |
| 2 | `POST` | `/api/v1/exam/eligibility/check-all/` | Check eligibility against ALL active exams (returns eligible list) |
| 3 | `GET` | `/api/v1/exam/{slug}/eligibility/?uid={uid}` | Quick eligibility for authenticated user on a specific exam |

---

## 5. Business Rules

- The eligibility engine is a decision-support tool, not a legal guarantee; the check result is based on the rules stored in EduForge's exam database which are entered from official notifications; if APPSC changes its age limit or category rules mid-cycle (which happens — a court order may change reservation percentages), the engine's result may be temporarily outdated until the content team updates the exam record; the result page includes the disclaimer: "Based on EduForge's data — always verify eligibility from the official notification at {conducting_body.website}"
- Age calculation uses the exam's `age_reference_date` (specified in most notifications — e.g., "age as on 1 January 2026") or falls back to `application_end` date; the difference between "age as on 1 Jan" vs "age as on date of application" can make or break eligibility for borderline candidates; the content team must enter the correct reference date from the official notification; a wrong reference date could incorrectly tell a 32-year-1-month-old candidate they are eligible for an exam with a 32-year limit
- Category relaxation varies not just by exam but by state; AP has BC-A through BC-E subcategories with different reservation rosters; Telangana has a different BC classification; Central exams use OBC (non-creamy layer) as a single category; the eligibility engine supports any category structure through the flexible `age_relaxations[]` JSON field on the exam record; the user's sub-category selection ("BC-B AP") is matched against the exam's relaxation rules specifically
- The "Check APPSC Group 1 instead?" suggestion (when a user is ineligible for TSPSC Group 1 due to domicile) is a smart recommendation: the engine detects that the failure reason is domicile-specific and searches for exams with the same type and qualification but matching the user's domicile state; this cross-exam recommendation turns a dead-end ("you're not eligible") into a constructive outcome ("but you are eligible for this equivalent exam in your state")
- Physical eligibility for police exams (height, weight, chest, running time) varies by gender, category, and state; AP Police SI requires males ≥ 167 cm (General) but ≥ 160 cm (ST); TS Police has slightly different standards; the engine stores these as per-post physical requirement records with gender and category variants; a user who enters their physical data gets a precise check: "You meet AP Police SI height requirement but your 100m running time (16.2s) exceeds the 15s requirement — you need to improve by 1.2 seconds"; this granularity is valuable for police exam aspirants planning their physical preparation

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division D*
