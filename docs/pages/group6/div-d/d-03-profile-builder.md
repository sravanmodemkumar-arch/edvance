# D-03 — Aspirant Profile Builder

> **URL:** `/exam/profile/`
> **File:** `d-03-profile-builder.md`
> **Priority:** P1
> **Data:** `user_aspirant_profile` — the data that powers eligibility, recommendations, and personalisation

---

## 1. Profile Builder

```
ASPIRANT PROFILE — Build your exam profile
This powers your eligibility checks, recommendations, and personalised study plan

  ── PERSONAL ──────────────────────────────────────────────────────────
  Full Name:           [ Ravi Kumar                          ]
  Date of Birth:       [ 15 / Jun / 2001 ▼ ]  Age: 24 yrs 9 mo
  Gender:              (●) Male  (○) Female  (○) Transgender
  Marital Status:      [ Unmarried ▼ ]

  ── CATEGORY & DOMICILE ───────────────────────────────────────────────
  Category:            [ OBC ▼ ]
  Sub-category:        [ BC-B ▼ ]  (state-specific — auto-filtered by domicile)
  Domicile State:      [ Andhra Pradesh ▼ ]
  Domicile District:   [ Guntur ▼ ]  (auto-populated from state)
  Local / Non-local:   [ Local ▼ ]  (relevant for AP/TS reservation)
  Ex-Serviceman:       (○) Yes  (●) No
  PH / Benchmark Dis.: (○) Yes  (●) No   If Yes: [ Type ▼ ]

  ── EDUCATION ─────────────────────────────────────────────────────────
  10th Standard:       Board: [ AP State Board ▼ ]  Year: [ 2017 ]  Marks: [ 86% ]
  12th / Intermediate: Board: [ AP State Board ▼ ]  Year: [ 2019 ]  Marks: [ 82% ]
                       Stream: [ MPC ▼ ]
  Graduation:          Degree: [ B.Com ▼ ]  University: [ Acharya Nagarjuna ▼ ]
                       Year: [ 2022 ]  Marks: [ 68.4% ]
  Post-Graduation:     [ Not applicable ▼ ]
  Professional:        [ None ▼ ]  (B.Ed / D.El.Ed / LLB / CA / etc.)

  ── PHYSICAL (optional — for Police / Defence exams) ──────────────────
  Height:              [ 172 ] cm
  Weight:              [ 68  ] kg
  Chest (male):        [ 87  ] cm unexpanded  /  [ 92 ] cm expanded
  Running 100m:        [ 15.8 ] seconds
  Running 1600m:       [ 6:20 ] min:sec
  Vision:              [ 6/6 ] (if applicable)

  ── EXAM PREFERENCES ──────────────────────────────────────────────────
  Target exam types:   [✅] Central  [✅] State  [  ] PSU  [✅] Banking  [  ] Defence
  Target states:       [✅] AP  [✅] Telangana  [  ] Karnataka  [  ] National
  Preferred language:  [ Telugu ▼ ]
  Willing to relocate: (●) Yes  (○) No  (○) Within state only

  [Save Profile]   [Save & Check Eligibility →]
```

---

## 2. Data Model

```
user_aspirant_profile {
  user_id,
  full_name, dob, gender, marital_status,
  category, sub_category,
  domicile_state, domicile_district, local_status,
  ex_serviceman, ph_status, ph_type,
  education: {
    tenth: { board, year, marks_pct },
    twelfth: { board, year, marks_pct, stream },
    graduation: { degree, university, year, marks_pct },
    post_graduation: { degree, university, year, marks_pct } (nullable),
    professional: { type } (nullable)  ← B.Ed, D.El.Ed, LLB, CA, etc.
  },
  physical: {
    height_cm, weight_kg, chest_unexpanded, chest_expanded,
    running_100m_sec, running_1600m_sec, vision
  } (nullable),
  preferences: {
    target_types[], target_states[], preferred_language, willing_to_relocate
  },
  completed: bool,          ← true when all mandatory fields are filled
  updated_at
}
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/profile/` | Get aspirant profile |
| 2 | `PUT` | `/api/v1/exam/profile/` | Create or update full profile |
| 3 | `PATCH` | `/api/v1/exam/profile/` | Partial update (e.g., just physical data) |
| 4 | `GET` | `/api/v1/exam/profile/completeness/` | Profile completeness score and missing fields |

---

## 5. Business Rules

- The aspirant profile is the foundation of all personalisation; an incomplete profile produces incomplete eligibility results; the system computes a "profile completeness" score: 100% = all fields filled; 80% = education + personal + domicile filled (sufficient for most civilian exams); 60% = personal + education only (insufficient for state exam eligibility, police/defence matching); users are prompted to complete their profile when they attempt an eligibility check with missing fields: "Add your domicile state to check APPSC eligibility"
- Sub-category selection is dynamically filtered by domicile state; AP's BC categories (BC-A, BC-B, BC-C, BC-D, BC-E) are different from Telangana's; Central exams use just "OBC (non-creamy layer)"; the UI shows state-relevant sub-categories only: a user who selects "Andhra Pradesh" domicile sees AP-specific BC categories; switching to "Telangana" updates the sub-category dropdown to TS-specific categories; this prevents users from selecting an invalid state + category combination
- Physical data is optional because most exams (SSC CGL, APPSC Group 2, IBPS PO) do not have physical requirements; collecting height/weight from all users would create unnecessary friction; physical fields are prompted only when the user checks eligibility for a police or defence exam, or when they add a police/defence exam to their targets; this progressive profiling approach collects data only when needed
- The profile data is personal and sensitive (DOB, category, disability status); it is encrypted at rest and accessible only to the user themselves; EduForge does not share profile data with coaching institutions, employers, or any third party; the profile is used only for eligibility computation and personalisation within the platform; the privacy notice on the profile page states exactly what the data is used for and how it is stored, per DPDPA 2023 requirements
- Profile updates trigger an immediate re-computation of the eligible exams cache (D-02); a user who adds a B.Ed qualification immediately sees 12 additional teaching exams in their eligible list; a user who corrects their DOB (previously entered wrong) may see eligibility changes for age-sensitive exams; the re-computation runs asynchronously (user does not wait for it) and the new eligible list is ready within 2 minutes of the profile save

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division D*
