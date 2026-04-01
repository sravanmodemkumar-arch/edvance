# E-01 — Test Series Dashboard

> **URL:** `/coaching/tests/dashboard/`
> **File:** `e-01-test-series-dashboard.md`
> **Priority:** P1
> **Roles:** Test Series Coordinator (K4) · Academic Director (K5) · Branch Manager (K6)

---

## 1. Test Series Overview

```
TEST SERIES DASHBOARD — Toppers Coaching Centre
As of 30 March 2026  |  Coordinator: Ms. Reshma Iyer

  ┌─────────────────────────────────────────────────────────────────────────────┐
  │  ACTIVE TEST SERIES         TOTAL TESTS    ENROLLED     AVG COMPLETION     │
  │  8 Series                   186 tests      4,240 seats  82.4%              │
  └─────────────────────────────────────────────────────────────────────────────┘

  SERIES OVERVIEW:
  Series                    │ Tests  │ Done │ Remaining │ Enrolled │ Status
  ──────────────────────────┼────────┼──────┼───────────┼──────────┼──────────────
  SSC CGL Full Mock 2026    │  30    │  23  │    7      │  1,240   │ ✅ Active
  SSC CHSL Mock 2026        │  20    │  14  │    6      │   640    │ ✅ Active
  SSC CGL Sectional Sprints │  48    │  36  │   12      │   880    │ ✅ Active
  Banking PO Full Mock      │  24    │  17  │    7      │   720    │ ✅ Active
  Banking Clerk Mock        │  20    │  12  │    8      │   480    │ ✅ Active
  RRB NTPC Full Mock        │  20    │  10  │   10      │   560    │ ✅ Active
  RRB Group D Mock          │  16    │   8  │    8      │   320    │ ✅ Active
  Foundation Test Series    │   8    │   4  │    4      │   400    │ ✅ Active

  UPCOMING THIS WEEK:
    Apr 3 (Fri):   RRB NTPC Sprint #8 (cross-batch, online, 2 PM)
    Apr 4 (Sat):   Banking Full Mock #14 (banking batches, online, 9 AM)
    Apr 5 (Sun):   SSC CGL Full Mock #25 (CGL batches, online + offline, 9 AM)
```

---

## 2. Test Pipeline Status

```
TEST PIPELINE — April 2026

  #   │ Test Name                  │ Series         │ Date     │ Status        │ Action
  ────┼────────────────────────────┼────────────────┼──────────┼───────────────┼──────────────────
  1   │ RRB NTPC Sprint #8        │ RRB NTPC       │ Apr 3    │ ✅ Published   │ [View] [Monitor]
  2   │ Banking Full Mock #14     │ Banking PO     │ Apr 4    │ ✅ Published   │ [View] [Monitor]
  3   │ SSC CGL Full Mock #25     │ SSC CGL Full   │ Apr 5    │ ✅ Published   │ [View] [Monitor]
  4   │ Quant Sprint #18          │ SSC CGL Sect.  │ Apr 6    │ ⬜ Draft       │ [Edit] [Publish]
  5   │ English Sprint #12        │ SSC CGL Sect.  │ Apr 7    │ ✅ Published   │ [View]
  6   │ SSC CHSL Full Mock #15   │ SSC CHSL       │ Apr 9    │ ⬜ Not started │ [Create]
  7   │ Reasoning Sprint #10      │ SSC CGL Sect.  │ Apr 11   │ ⬜ Not started │ [Create]
  8   │ SSC CGL Full Mock #26     │ SSC CGL Full   │ Apr 14   │ ⬜ Not started │ [Create]

  PIPELINE HEALTH:
    Tests published on schedule:  68 / 74 so far (91.9%) ✅
    Avg lead time (create→publish): 4.2 days ✅ (target: 3+ days)
    ⚠️ SSC CHSL Mock #15 not started — 9 days to exam. Urgent.
```

---

## 3. Quick Actions

```
QUICK ACTIONS

  [+ Create New Test]              → Opens C-05 Test Creation
  [📅 View Full Schedule]          → Opens E-02 Mock Test Schedule
  [🔴 Monitor Live Test]           → Opens E-03 Live Monitor
  [📊 View Latest Analysis]        → Opens E-05 Test Analysis
  [📦 Manage Packages]             → Opens E-09 Test Series Packages

  COORDINATOR ALERTS:
    🔴 Quant Sprint #18 in DRAFT — publish before Apr 5 deadline
    🟡 SSC CHSL Full Mock #15 — not started (9 days away)
    ✅ Banking Full Mock #14 — all checks passed, ready for exam day
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/test-series/` | All active test series with summary |
| 2 | `GET` | `/api/v1/coaching/{id}/test-series/{sid}/pipeline/?month=2026-04` | Test pipeline for a series |
| 3 | `GET` | `/api/v1/coaching/{id}/test-series/upcoming/?days=7` | Tests scheduled in next N days |
| 4 | `GET` | `/api/v1/coaching/{id}/test-series/dashboard/` | Full coordinator dashboard data |
| 5 | `GET` | `/api/v1/coaching/{id}/test-series/alerts/` | Coordinator alerts (draft, overdue, upcoming) |

---

## 5. Business Rules

- The Test Series Dashboard is the single source of truth for all mock test operations at TCC; test coordinators use it to track every test from creation to result publication; a test that is not tracked in the dashboard has no audit trail and cannot be used for faculty performance evaluation (B-07), batch performance analytics (D-05), or student rank prediction (E-06); all tests, regardless of batch or subject, must be created and published through EduForge
- The "pipeline health" metric (% of tests published on schedule vs planned date) is a coordinator performance indicator; a health score below 85% means tests are being created too close to their exam date, leaving insufficient time for quality review; the Academic Director reviews pipeline health monthly as part of the quality review (B-07); coordinators who consistently publish tests less than 48 hours before the exam date are flagged for process coaching
- Test series are sold as packages (E-09) to both enrolled students (included in course fee) and external students (standalone purchase); the dashboard shows enrollment counts for both types; enrolled batch students and external package buyers are tracked separately in analytics to allow TCC to measure whether standalone test series buyers eventually enroll in classroom courses (a key sales funnel metric)
- An upcoming test with "Not started" status 7 or fewer days before the scheduled date triggers an automatic alert to the Academic Director; the coordinator must either complete the test or reschedule it; the system prevents creating a test with less than 48 hours of lead time without Academic Director override (which is logged); this minimum lead time allows students to see the upcoming test and prepare their schedule
- The test pipeline must be updated in real time; a test moved from "Draft" to "Published" is immediately visible to enrolled students in their portal (O-01); the coordinator must verify the test details, timing, and question paper before publishing; once published and visible to students, unpublishing a test within 48 hours of its scheduled time requires Branch Manager approval and triggers an automated apology notification to enrolled students

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division E*
