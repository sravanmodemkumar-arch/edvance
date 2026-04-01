# D-04 — Smart Exam Recommender

> **URL:** `/exam/recommendations/`
> **File:** `d-04-exam-recommender.md`
> **Priority:** P2
> **Data:** `user_aspirant_profile` + `exam` + `mock_attempt` + `exam_cycle` (cut-offs, competition) — ML-driven scoring

---

## 1. Smart Recommendations

```
SMART EXAM RECOMMENDER — Ravi Kumar
Beyond eligibility — which exams should you actually focus on?

  YOUR RECOMMENDATION SCORE  [computed from: eligibility + competition + prep level + preference]
  ┌──────────────────────────────────────────────────────────────────────┐
  │  #  │ Exam                   │ Match │ Why recommended                │
  ├─────┼────────────────────────┼───────┼────────────────────────────────┤
  │ 🏆1 │ APPSC Group 2 2025     │  94%  │ AP domicile, already prepping, │
  │     │                        │       │ mock score trending above cutoff│
  ├─────┼────────────────────────┼───────┼────────────────────────────────┤
  │  2  │ SSC CGL 2026           │  88%  │ High vacancies, national scope, │
  │     │                        │       │ mock score at 69th percentile   │
  ├─────┼────────────────────────┼───────┼────────────────────────────────┤
  │  3  │ IBPS PO 2026           │  82%  │ Graduate eligible, banking sector│
  │     │                        │       │ high salary, syllabus overlaps CGL│
  ├─────┼────────────────────────┼───────┼────────────────────────────────┤
  │  4  │ APPSC Group 3 2026     │  78%  │ AP domicile, lower competition, │
  │     │                        │       │ your profile > typical qualifier│
  ├─────┼────────────────────────┼───────┼────────────────────────────────┤
  │  5  │ VRO/VRA AP 2025        │  76%  │ AP domicile, application open  │
  │     │                        │       │ NOW, low qualification bar      │
  └─────┴────────────────────────┴───────┴────────────────────────────────┘

  SCORING FACTORS:
    Eligibility:       Pass/Fail (must pass to be recommended)
    Competition fit:   Your mock performance vs expected cut-off
    Syllabus overlap:  % overlap with exams you're already preparing for
    Deadline urgency:  Exams with imminent deadlines get a boost
    User preference:   Target types & states from profile (D-03)
    Career alignment:  Salary, posting location vs user's willingness to relocate

  ──────────────────────────────────────────────────────────────────────
  EXAMS YOU MIGHT NOT KNOW ABOUT:
    🆕 APSRTC Conductor 2026 — AP state, 12th pass eligible, 420 vacancies
       Match: 72% — you're overqualified (graduate) but it's a quick govt job
    🆕 LIC AAO 2026 — National, graduate, high salary, application expected Aug
       Match: 68% — banking+insurance sector; similar quant syllabus to CGL
```

---

## 2. Recommendation Algorithm

```
RECOMMENDATION SCORING — How the match % is computed

  FOR EACH eligible_exam:
    score = 0

    # Factor 1: Competition Fit (0–30 points)
    IF user has mock data for this exam or overlapping syllabus:
      predicted_score = extrapolate from mock trend
      distance_from_cutoff = predicted_score - projected_cutoff
      IF distance > +10%:  score += 30 (likely to clear)
      IF distance 0 to +10%: score += 20 (competitive chance)
      IF distance -10% to 0: score += 10 (needs improvement)
      ELSE: score += 0 (unlikely without significant improvement)

    # Factor 2: Syllabus Overlap (0–20 points)
    overlap_pct = common syllabus_nodes between this exam and user's active exams
    score += overlap_pct * 0.2  (max 20 if 100% overlap)

    # Factor 3: Deadline Urgency (0–15 points)
    IF application_open AND days_to_deadline < 15: score += 15
    IF application_open AND days_to_deadline < 30: score += 10
    IF notification expected within 60 days: score += 5

    # Factor 4: User Preference (0–20 points)
    IF exam.type IN user.target_types: score += 10
    IF exam.state_code IN user.target_states OR exam is national: score += 10

    # Factor 5: Career Quality (0–15 points)
    salary_score = normalise(exam.salary_range.max) → 0–10
    posting_fit = user.willing_to_relocate matches exam.posting_scope → 0–5
    score += salary_score + posting_fit

    match_pct = score  (out of 100)
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/recommendations/?uid={uid}&limit=10` | Top N recommended exams |
| 2 | `GET` | `/api/v1/exam/recommendations/discover/` | "Exams you might not know about" |

---

## 5. Business Rules

- The recommender goes beyond eligibility (which answers "can I apply?") to strategic fit (which answers "should I invest my prep time in this exam?"); an aspirant eligible for 62 exams cannot prepare for all of them; they need to focus on 3–5 exams; the recommender's job is to surface the 3–5 best fits based on the aspirant's current readiness, exam timing, and career preferences; this is the highest-value personalisation EduForge can offer
- The "Competition Fit" factor uses the user's mock test performance to estimate their chance of clearing each exam; this requires the mock engine (E-01) to tag mocks to exams and the system to maintain historical cut-off data (F-02); a student scoring 138/200 in SSC CGL mocks with a projected cut-off of 144–148 is slightly below the threshold — the system gives a moderate competition fit score; a student scoring 168/200 is well above — high fit; this signal helps aspirants avoid wasting time on exams they are very unlikely to clear with their current performance
- Syllabus overlap scoring encourages strategic multi-exam preparation; if a student is already preparing for APPSC Group 2 (which includes Indian Polity, Economy, History) and SSC CGL (Quant, English, Reasoning, GK), the recommender scores IBPS PO highly because its syllabus overlaps significantly with SSC CGL; studying for 2 exams with 60% syllabus overlap is more efficient than studying for 2 exams with 10% overlap; this is practical strategy advice delivered through algorithmic recommendation
- The "Exams you might not know about" section deliberately surfaces niche or less-known exams (APSRTC Conductor, LIC AAO, GENCO JE) that the user might not have discovered through browsing; many aspirants from AP/TS focus exclusively on APPSC or SSC and miss opportunities in PSU, insurance, or municipal exams; the discovery section runs a broader search than the main recommendations — it includes exams with lower match scores (60–75%) but adds a novelty factor for exams the user has never viewed or searched
- Recommendations are refreshed weekly and after significant user events: completing a new mock test (changes competition fit), updating profile (changes eligibility), or a new exam being added to the platform; the computation is expensive (eligibility check + overlap analysis + mock score extrapolation for each eligible exam) and is computed asynchronously, not on page load; the cached result is returned on page load; a user who just took a mock and improved by 20 points sees their recommendations update within 4 hours

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division D*
