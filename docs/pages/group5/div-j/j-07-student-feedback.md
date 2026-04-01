# J-07 — Student Feedback & Surveys

> **URL:** `/coaching/student-affairs/feedback/`
> **File:** `j-07-student-feedback.md`
> **Priority:** P2
> **Roles:** Student Counsellor (K3) · Academic Director (K5) · Branch Manager (K6)

---

## 1. Active Surveys

```
ACTIVE SURVEYS — March 2026

  Survey                      │ Batch Target       │ Sent  │ Responded │ Rate  │ Status
  ────────────────────────────┼────────────────────┼───────┼───────────┼───────┼──────────────
  Q3 Faculty Rating (Mar)     │ All batches (856)  │  856  │    642    │ 75.0% │ ✅ Closed
  Hostel Satisfaction (Mar)   │ Hostel residents   │  108  │     84    │ 77.8% │ ✅ Closed
  Online Batch Experience     │ Online students    │  392  │    286    │ 73.0% │ ⏳ Open (due Apr 5)
  Study Material Quality      │ SSC CGL batches    │  460  │    —      │  —    │ 📅 Scheduled Apr 1

  RESPONSE RATE TARGET: 70%  |  Current avg: 75.2% ✅
```

---

## 2. Q3 Faculty Rating Results

```
Q3 FACULTY RATINGS — March 2026 (642 responses)
Scale: 1–5 | Aggregated and anonymised

  FACULTY PERFORMANCE:
    Faculty         │ Subject    │ Avg Rating │ Responses │ Key Feedback
    ────────────────┼────────────┼────────────┼───────────┼──────────────────────────────
    Mr. Suresh K.   │ Quant      │  4.3/5.0  │    184    │ "Explains well, but sometimes
                    │            │            │           │  dismissive with basic Qs"  ⚠️
    Ms. Kavita M.   │ English    │  4.6/5.0  │    168    │ "Excellent grammar teaching,
                    │            │            │           │  exam tricks very helpful" ✅
    Mr. Mohan R.    │ Reasoning  │  4.1/5.0  │    176    │ "Good content but slightly fast
                    │            │            │           │  pace for weak students" 🟡
    Mr. Ravi S.     │ GK/CA      │  3.8/5.0  │    114    │ "GK coverage good but less
                    │            │            │           │  current affairs depth" 🟡
    ────────────────┴────────────┴────────────┴───────────┴──────────────────────────────

  BATCH OVERALL RATING:
    Teaching quality:     4.2/5.0 ✅
    Study material:       4.0/5.0 ✅
    Test series quality:  4.4/5.0 ✅ (highest rated)
    Doubt resolution:     3.8/5.0 🟡 (room for improvement — SLA breaches noted)
    Counselling support:  4.1/5.0 ✅
    Overall TCC rating:   4.2/5.0 ✅

  ACTION ITEMS (from Q3 feedback):
    Suresh K. note: GRV-0041 aligned — "dismissive with basic questions" pattern ✅
    Mohan R.: Academic Director to discuss pacing for weaker students
    Ravi S.: Dedicate 15 min/session to recent CA from last 30 days
    Doubt resolution: SLA enforcement reminder to all faculty (Apr 1 meeting)
```

---

## 3. Survey Builder

```
CREATE SURVEY — Study Material Quality (SSC CGL Batches)

  Title:       [Study Material Quality — Q4 2026                  ]
  Target:      [SSC CGL Morning + Evening (460 students) ▼]
  Open date:   [1 April 2026 ▼]   Close date: [8 April 2026 ▼]
  Reminder:    [Auto-send to non-responders on Apr 5 ▼]

  QUESTIONS (drag to reorder):
    1. How would you rate the quality of PDF notes provided?  [1–5 ★ rating]
    2. How would you rate the question bank difficulty?        [1–5 ★ rating]
    3. Are study materials updated to reflect recent exams?    [1–5 ★ rating]
    4. Which material type do you find most useful?            [MCQ: Video/PDF/Notes/Quizzes]
    5. What material improvement would you suggest?            [Text — 200 chars max]

  ANONYMITY:   (●) Anonymous responses  (no student name attached to answers)
  Results:     Branch Manager + Academic Director + relevant Faculty

  [Publish Survey]   [Preview Student View]   [Save Draft]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-affairs/surveys/` | All surveys |
| 2 | `POST` | `/api/v1/coaching/{id}/student-affairs/surveys/` | Create new survey |
| 3 | `GET` | `/api/v1/coaching/{id}/student-affairs/surveys/{sid}/results/` | Survey results and analytics |
| 4 | `POST` | `/api/v1/coaching/{id}/student-affairs/surveys/{sid}/reminder/` | Send reminder to non-responders |
| 5 | `GET` | `/api/v1/coaching/{id}/student-affairs/surveys/faculty-ratings/?quarter=Q3-2026` | Quarterly faculty ratings |

---

## 5. Business Rules

- Faculty ratings are always anonymised — no individual student's rating for a specific faculty is visible to the faculty; faculty see their aggregate score and themes from free-text responses, not individual responses; this protects students from retaliation (real or perceived) for giving honest feedback; the Academic Director shares the aggregated feedback with faculty in their quarterly review (B-07) as a professional development input, not as a punitive measure; a faculty with a 3.8 rating is not disciplined but is coached on the specific issue identified
- The minimum response rate for a survey to be considered statistically meaningful for individual faculty ratings is 60% of the faculty's students; Mr. Ravi S.'s 114 responses from an estimated 190 students (60%) meets the threshold; a faculty with only 20% response rate (40 responses from 200 students) should have their rating treated with caution and not used for performance decisions; the Academic Director flags low response rates when presenting feedback
- Surveys are anonymous by design; TCC does not collect student IDs with survey responses; however, the survey platform must ensure that a student cannot submit multiple responses (which would skew results); the system uses the student's login session to verify one-submission-per-survey, but strips the student identity before storing the response; this is a technical implementation of anonymous survey best practice
- Survey cadence is quarterly for faculty ratings, semester for hostel satisfaction, and as-needed for specific issues (study material quality, new batch feedback); over-surveying causes fatigue and reduces response rates; a student who receives a survey every week will stop responding; the 4–5 surveys per academic year is near the upper limit; the counsellor reviews survey fatigue metrics (declining response rates over time) and recommends reducing survey frequency if needed
- Survey results that reveal a systemic issue (doubt resolution SLA at 3.8/5.0 with multiple comments about slow responses) trigger an action item that is documented, assigned to an owner (Academic Director: enforce SLA at next faculty meeting), and tracked to completion; the next quarter's survey should show improvement; if the same issue appears in 3 consecutive quarterly surveys, it is escalated to the Director as a chronic unresolved quality problem; the survey becomes a quality management tool, not just a data collection exercise

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division J*
