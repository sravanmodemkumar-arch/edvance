# E-02 — Mock Test Schedule

> **URL:** `/coaching/tests/schedule/`
> **File:** `e-02-mock-test-schedule.md`
> **Priority:** P1
> **Roles:** Test Series Coordinator (K4) · Academic Director (K5)

---

## 1. Monthly Test Calendar

```
MOCK TEST SCHEDULE — April 2026
All Batches | Toppers Coaching Centre

  DATE      │ TEST NAME                      │ SERIES          │ BATCHES     │ TIME     │ MODE
  ──────────┼────────────────────────────────┼─────────────────┼─────────────┼──────────┼──────────
  Apr 3 Fri │ RRB NTPC Sprint #8            │ RRB NTPC        │ RRB batches │ 2:00 PM  │ Online
  Apr 4 Sat │ Banking Full Mock #14          │ Banking PO      │ Banking     │ 9:00 AM  │ Online
  Apr 5 Sun │ SSC CGL Full Mock #25          │ SSC CGL Full    │ CGL batches │ 9:00 AM  │ Hybrid
  Apr 6 Sun │ Quant Sprint #18              │ SSC CGL Sect.   │ CGL Morn.   │ 10:00 AM │ Online
  Apr 7 Mon │ English Sprint #12             │ SSC CGL Sect.   │ CGL Eve.    │ 10:00 AM │ Online
  Apr 9 Wed │ SSC CHSL Full Mock #15         │ SSC CHSL        │ CHSL batch  │ 9:00 AM  │ Online
  Apr 11 Fri│ Reasoning Sprint #10          │ SSC CGL Sect.   │ CGL batches │ 10:00 AM │ Online
  Apr 13 Sun│ GK Weekly #18                  │ GK Series       │ All batches │ 8:00 AM  │ Online
  Apr 14 Sun│ SSC CGL Full Mock #26          │ SSC CGL Full    │ CGL batches │ 9:00 AM  │ Hybrid
  Apr 18 Sat│ Banking Sectional — GA/GK      │ Banking Clerk   │ Banking     │ 10:00 AM │ Online

  ⚠️ BLACKOUT: No tests scheduled Apr 19–30 (SSC CGL exam proximity)

  CONFLICT CHECK:
    ✅ No two tests for the same batch on the same day
    ✅ All tests scheduled at least 3 days after creation
    ⚠️ Apr 5 and Apr 6 are back-to-back for CGL Morning — coordinator note added
```

---

## 2. Test Scheduling Rules & Calendar Control

```
SCHEDULING CONSTRAINTS

  GLOBAL RULES (enforced by system):
    • No two tests for same batch on same calendar day
    • Minimum 48-hour gap between full mocks for same batch
    • No tests within 5 days of government exam date (auto-blocked from B-05)
    • Test must be published ≥ 24 hrs before scheduled time (system enforced)

  EXAM PROXIMITY BLACKOUTS (auto-generated from B-05):
    Apr 19–30 2026:   SSC CGL Tier-I — CGL batch blackout ✅
    Apr 12–18 2026:   IBPS RRB PO — Banking batch warning (not hard block)

  GAP ANALYSIS (SSC CGL Morning — April):
    Full mocks:         Apr 5, Apr 14  → 9-day gap ✅
    Subject sprints:    Apr 6, 7, 11   → every 3–4 days ✅
    Total tests/week:   2–3 (recommended max: 3) ✅

  ADD TEST TO CALENDAR:
    [Select Series ▼]  [Select Date 📅]  [Select Time ▼]  [Mode: Online/Offline ▼]
    [Conflict Check]   [Add to Schedule]
```

---

## 3. Batch-Specific Calendar

```
BATCH TEST CALENDAR — SSC CGL MORNING (April 2026)
Enrolled: 240 students

  Week 1 (Apr 1–5):
    Apr 5 Sun — SSC CGL Full Mock #25 (60 min, 200 marks, 9:00 AM)
    Coverage: All 4 subjects (Quant, English, Reasoning, GK)
    Venue: Hall A (offline) + Zoom link (for absentees — makeup within 48 hrs)

  Week 2 (Apr 6–12):
    Apr 6 Sun  — Quant Sprint #18 (45 min, 50 marks)
    Apr 7 Mon  — English Sprint #12 (45 min, 50 marks)
    Apr 11 Fri — Reasoning Sprint #10 (45 min, 50 marks)

  Week 3 (Apr 13–18):
    Apr 13 Sun — GK Weekly #18 (15 min, 25 marks, all batches)
    Apr 14 Sun — SSC CGL Full Mock #26 (60 min, 200 marks — Pre-exam final)

  Week 4 (Apr 19–30):
    🔴 BLACKOUT — SSC CGL 2025 Tier-I exam period
    No tests. Revision support only.
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/tests/schedule/?month=2026-04` | Full test calendar for the month |
| 2 | `GET` | `/api/v1/coaching/{id}/tests/schedule/?batch={bid}&month=2026-04` | Batch-specific test calendar |
| 3 | `POST` | `/api/v1/coaching/{id}/tests/schedule/` | Add a test to the schedule |
| 4 | `DELETE` | `/api/v1/coaching/{id}/tests/schedule/{sid}/` | Remove a scheduled test slot |
| 5 | `GET` | `/api/v1/coaching/{id}/tests/schedule/conflicts/?batch={bid}&date=2026-04-05` | Check scheduling conflicts |
| 6 | `GET` | `/api/v1/coaching/{id}/tests/schedule/blackouts/?month=2026-04` | Government exam blackout dates |

---

## 5. Business Rules

- The government exam blackout is auto-enforced from the exam calendar maintained in Division B (B-05); when SSC CGL exam dates are added to the government exam calendar, the system automatically blocks test creation for CGL batches in the 5-day window before the exam; this cannot be overridden by the Test Series Coordinator and requires Academic Director approval; the intent is to give students revision time and prevent exam-day anxiety from a poorly-timed mock result
- A "hybrid" test (SSC CGL Full Mock #25) means students can take it either offline in the hall or online from home; offline students are invigilated and their attendance is physical; online students use the EduForge portal with screen-proctoring enabled; results are released together 3 hours after the test window closes; hybrid tests require the coordinator to set up both a physical hall booking and an online Zoom monitoring session simultaneously
- The test calendar is published to students at least 14 days in advance; students who work out their preparation schedule around the test calendar cannot adapt to last-minute changes; the 14-day notice rule creates predictability; the system prevents adding a test to the calendar with less than 14 days' notice without Academic Director approval; this is separate from the 24-hour publication rule (a test can be added to the calendar 14 days ahead but only published 24 hours before)
- GK Weekly tests are scheduled for all batches on the same day (Sunday mornings at 8 AM) regardless of batch type; this is intentional — GK and Current Affairs are common to SSC, RRB, and Banking exams; a shared GK test allows TCC to compare GK performance across all batches and assess the effectiveness of the GK faculty who teaches all batches; the shared test also saves question bank effort (one GK paper serves all)
- "Makeup" tests for students who missed a scheduled test must be taken within 48 hours of the original test; the makeup version uses the same paper with question order randomised; makeup results are flagged in the analytics with a "makeup" tag and are excluded from batch-level performance comparisons (since the makeup taker had 48 extra hours of preparation); however, they count for individual student performance tracking

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division E*
