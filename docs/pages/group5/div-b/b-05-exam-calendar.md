# B-05 — Exam & Test Calendar

> **URL:** `/coaching/academic/exam-calendar/`
> **File:** `b-05-exam-calendar.md`
> **Priority:** P1
> **Roles:** Academic Director (K6) · Course Head (K5) · Academic Coordinator (K5) · All Staff (K2+) — read only

---

## 1. Exam Calendar — Government Exams

```
GOVERNMENT EXAM CALENDAR 2026 — TRACKED BY TCC

  Exam                  │ Conducting  │ Tier/Stage    │ Expected Date   │ Status
  ──────────────────────┼─────────────┼───────────────┼─────────────────┼──────────────
  SSC CGL Tier-I        │ SSC         │ Preliminary   │ 20 Apr 2026     │ ⚠️ 21 days
  SSC CGL Tier-II       │ SSC         │ Mains         │ Jul 2026        │ ⬜ Post Tier-I
  SSC CHSL Tier-I       │ SSC         │ Preliminary   │ Jun 2026        │ ⬜ 3 months
  SSC MTS               │ SSC         │ Paper I       │ May 2026        │ ⬜ 7 weeks
  RRB NTPC CBT-I        │ RRB         │ Stage 1       │ Aug 2026        │ ⬜ 5 months
  RRB Group D           │ RRB         │ CBT           │ Sep 2026        │ ⬜ 6 months
  IBPS PO Prelim        │ IBPS        │ Preliminary   │ Oct 2026        │ ⬜ 7 months
  IBPS Clerk Prelim     │ IBPS        │ Preliminary   │ Dec 2026        │ ⬜ 9 months
  SBI PO Prelim         │ SBI         │ Preliminary   │ May 2026        │ ⬜ 7 weeks
  SBI Clerk Prelim      │ IBPS/SBI    │ Preliminary   │ Feb 2027        │ ⬜ 11 months
  UPSC CSE Prelim       │ UPSC        │ Preliminary   │ 25 May 2026     │ ⬜ 8 weeks
  TS Police SI          │ TSLPRB      │ Written       │ Jun 2026        │ ⬜ 3 months
  JEE Main Session 3    │ NTA         │ Attempt 3     │ Apr 2026        │ ⚠️ 2 weeks

  ⚠️ SSC CGL Tier-I in 21 days — SSC CGL batches in final revision mode
  Source: Official notifications tracked. Dates auto-update when SSC/IBPS/RRB notifies.
```

---

## 2. TCC Internal Test Schedule

```
TCC INTERNAL TEST SCHEDULE — April 2026

  Date    │ Test Name                      │ Batches           │ Duration │ Marks │ Mode
  ────────┼────────────────────────────────┼───────────────────┼──────────┼───────┼────────
  Apr 2   │ SSC CGL Full Mock #24          │ CGL Morn + Eve    │ 60 min   │  200  │ Online
  Apr 3   │ RRB NTPC Sprint #8             │ RRB NTPC Weekend  │ 90 min   │  100  │ Online
  Apr 5   │ Banking Full Mock #18          │ Banking Morn + Eve│ 60 min   │  100  │ Online
  Apr 8   │ Foundation Chapter Test 12     │ Foundation 9-10   │ 45 min   │   60  │ OMR
  Apr 10  │ JEE Mock #18 (Full)            │ Dropper JEE       │ 3 hrs    │  300  │ Online
  Apr 12  │ GK Weekly #16                  │ All SSC batches   │ 15 min   │   50  │ Online
  Apr 14  │ SSC CGL Revision Mock #25      │ CGL All batches   │ 60 min   │  200  │ Online
  Apr 16  │ Banking Sprint — Reasoning     │ Banking batches   │ 30 min   │   50  │ Online
  Apr 18  │ RRB NTPC Full Mock #9          │ RRB NTPC          │ 90 min   │  100  │ Online
  Apr 20  │ SSC CGL FINAL MOCK #26         │ CGL All batches   │ 60 min   │  200  │ Online
  ────────────────────────────────────────────────────────────────────────────────────────
  ⚠️ No new tests after Apr 20 for SSC CGL — SSC CGL actual exam on Apr 20 (estimated)
  ℹ️ Dropper JEE continues normal schedule — JEE Main S3 after Apr 10
```

---

## 3. Exam Notification Tracker

```
EXAM NOTIFICATION TRACKER — Official Sources

  Source              │ Last Checked  │ Latest Update                    │ Alert Sent
  ────────────────────┼───────────────┼──────────────────────────────────┼────────────
  ssc.nic.in          │ 30 Mar 07:14  │ CGL 2026 admit cards: 10 Apr     │ ✅ WhatsApp
  rrbapply.gov.in     │ 30 Mar 07:14  │ NTPC CBT-I: August 2026 confirm. │ ✅ App Push
  ibps.in             │ 30 Mar 07:14  │ PO cycle: notification Oct 2026   │ ✅ App Push
  sbi.co.in           │ 30 Mar 07:14  │ SBI PO: notification May 2026    │ ✅ App Push
  upsc.gov.in         │ 30 Mar 07:14  │ CSE 2026 notification: 5 Feb     │ ✅ App Push
  nta.ac.in           │ 30 Mar 07:14  │ JEE Main S3: April 7–12 2026    │ ✅ App Push

  Auto-check: Every 6 hours | Manual refresh: [Refresh Now]
  Student notification: Auto WhatsApp when admit card / date confirmed
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/exams/calendar/` | Government exam calendar |
| 2 | `GET` | `/api/v1/coaching/{id}/exams/internal-tests/?month=2026-04` | Internal test schedule |
| 3 | `POST` | `/api/v1/coaching/{id}/exams/internal-tests/` | Schedule a new internal test |
| 4 | `GET` | `/api/v1/coaching/{id}/exams/notifications/` | Exam notification tracker |
| 5 | `POST` | `/api/v1/coaching/{id}/exams/notify-students/` | Push exam date alert to students |

---

## 5. Business Rules

- The exam calendar drives every other academic decision; batch end dates, revision schedules, crash course windows, and test frequency are all derived from government exam dates; when SSC announces the CGL exam date, TCC must immediately recalibrate the remaining batch calendar; EduForge's exam notification tracker auto-detects official notifications and prompts the Academic Coordinator to update the batch calendar within 24 hours
- Internal mock tests must be scheduled in decreasing density as the actual exam approaches; in the 4 weeks before the exam, full mock tests should be conducted every 4–5 days to simulate exam-day stamina; in the 1 week before, only 1 revision mock is advised — too many tests in the final week cause fatigue and anxiety; TCC's April schedule correctly shows the last full mock on Apr 20 (same day as the estimated exam, as a final benchmark)
- Test-free weeks must be planned once a month to allow students to consolidate learning; a continuous test schedule without consolidation weeks creates test fatigue — students start attempting tests mechanically without learning from mistakes; the Academic Coordinator must ensure at least one week per month has no full mock test (spot tests and chapter tests are acceptable)
- Exam date tracking from official sources must be automated because SSC and IBPS frequently postpone or prepone exam dates with short notice; a coaching centre relying on manual tracking will miss a date change and fail to alert students in time; TCC's 6-hourly auto-check of SSC, IBPS, RRB, and NTA websites, with immediate student push notification on any change, is a student-trust driver — students rely on TCC to keep them informed
- Students who are preparing for multiple exams simultaneously (e.g., SSC CGL + RRB NTPC) must have a personalised exam calendar in their student portal; the Institute-level exam calendar shows all tracked exams; each student's "My Exams" section shows only the exams they have registered for, with countdown timers and batch-specific test schedules; this prevents a Banking student from being confused by SSC CGL countdown notices irrelevant to them

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division B*
