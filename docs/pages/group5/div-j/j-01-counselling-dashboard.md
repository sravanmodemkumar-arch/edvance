# J-01 — Counselling Dashboard

> **URL:** `/coaching/student-affairs/counselling/`
> **File:** `j-01-counselling-dashboard.md`
> **Priority:** P1
> **Roles:** Student Counsellor (K3) · Branch Manager (K6)

---

## 1. Counsellor Overview

```
COUNSELLING DASHBOARD — Toppers Coaching Centre
As of 30 March 2026  |  Counsellor: Ms. Ananya Roy

  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  ACTIVE CASELOAD: 28  │  SESSIONS THIS MONTH: 42  │  PENDING FOLLOW-UPS: 8 │
  └──────────────────────────────────────────────────────────────────────────────┘

  CASE STATUS BREAKDOWN:
    Active counselling (ongoing):     18 students
    Monitoring (improved, check-ins):  8 students
    Closed (resolved / exam cleared):  2 students
    Escalated to Branch Manager:       2 students

  REFERRAL SOURCES (how students came to counselling):
    Academic at-risk flag (batch coordinator):   14 (50%)
    Fee default + academic risk (dual):           6 (21%)
    Self-referred (student sought help):          5 (18%)
    Hostel warden referral:                       3 (11%)

  TODAY'S SCHEDULE:
    10:00 AM — Mohammed R. (TCC-2406) — ongoing (3rd session — attendance/fee)
    11:30 AM — Sravya Rao (TCC-2418) — new (referred by coordinator yesterday)
    02:00 PM — Pavan Reddy (TCC-2428) — ongoing (6th session — performance anxiety)
    04:30 PM — Kiran Naidu (TCC-2419) — check-in (previously at-risk, monitoring)
```

---

## 2. At-Risk Case Summary

```
AT-RISK CASELOAD — Counsellor View (Ms. Ananya Roy)
As of 30 March 2026

  Priority  │ Student          │ Batch       │ Risk Factors                    │ Next Session
  ──────────┼──────────────────┼─────────────┼─────────────────────────────────┼──────────────
  🔴 High   │ Pavan Reddy      │ CGL Morning │ Att 58%, Score 38%, Fee 60d OD  │ Today 2 PM
  🔴 High   │ Mohammed R.      │ CGL Morning │ Att 57%, Fee 45d OD, Smoking 2x │ Today 10 AM
  🔴 High   │ Kiran Naidu      │ CGL Morning │ Att 32% online, Fee default      │ Today 4:30 PM
  🟡 Medium │ Sravya Rao       │ CGL Morning │ Att 64%, Score declining         │ Today 11:30 AM
  🟡 Medium │ Deepak V.        │ Banking     │ Score < 35% last 3 tests         │ Apr 2
  🟡 Medium │ Anita M.         │ RRB NTPC    │ Frequently absent — no reason    │ Apr 2
  🟡 Medium │ Renu S.          │ SSC CHSL    │ Self-referred — exam anxiety      │ Apr 1
  ...  (21 more)

  CLOSED THIS MONTH:
    Akhil Kumar: Resolved — scores improved, no longer at-risk ✅
    Divya Sharma: Resolved — attendance stabilised ✅
```

---

## 3. Quick Referral

```
QUICK REFERRAL — Refer a Student to Counselling

  Student:          [TCC-2403 — Ravi Singh ▼]
  Referred by:      [Ms. Priya Nair (Batch Coordinator) ▼]
  Reason:           [Academic at-risk: attendance + score ▼]
  Urgency:          (●) Normal (within 48 hrs)  ( ) Urgent (within 24 hrs)
  Notes:            "Ravi has been missing classes and scores are declining.
                     He seems withdrawn. Possible personal issue."

  [Submit Referral]   →  Assigned to: Ms. Ananya Roy (least-loaded counsellor)
  Student notified:  WhatsApp: "TCC would like to schedule a quick check-in with you.
                     No cause for concern — just a routine welfare session.
                     Your counsellor will contact you soon."
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-affairs/counselling/dashboard/` | Counsellor dashboard |
| 2 | `GET` | `/api/v1/coaching/{id}/student-affairs/counselling/caseload/?counsellor={uid}` | Active caseload |
| 3 | `POST` | `/api/v1/coaching/{id}/student-affairs/counselling/referral/` | Refer a student |
| 4 | `GET` | `/api/v1/coaching/{id}/student-affairs/counselling/schedule/?date=2026-03-30` | Counsellor's daily schedule |
| 5 | `GET` | `/api/v1/coaching/{id}/student-affairs/counselling/stats/?month=2026-03` | Monthly counselling stats |

---

## 5. Business Rules

- Counselling referrals are confidential; a referred student's case details (reason for referral, session notes, counsellor's assessment) are visible only to the counsellor and the Branch Manager; the referring coordinator sees only "referral accepted" status, not the counsellor's notes; the student must not feel that their personal struggles are shared openly in the staff room; this confidentiality is stated in TCC's student welfare policy and in the referral notification sent to the student
- The counsellor's role is student welfare support, not academic instruction or fee collection; a counsellor who uses a session to pressure a student about fee payment or attendance targets is misusing the therapeutic relationship; if the counsellor identifies fee-related stress as the root cause of academic disengagement, they liaise with the Accounts team separately (not in the session); the counsellor's job is to understand, support, and refer to the right resource — not to solve every problem directly
- Counselling sessions for minor students require guardian consent for ongoing counselling (one initial session is permitted without explicit consent as a welfare check); a parent who objects to their child receiving counselling cannot be overridden; however, the counsellor may recommend to the Branch Manager that the parent be briefed about their child's welfare situation, with the student's knowledge; this transparent approach is better than a confrontational one
- The counsellor's caseload maximum is 30 active students; beyond 30, new referrals are queued for a second counsellor (if available) or to an external counsellor TCC contracts; overloading a single counsellor reduces session quality and creates burnout risk; the Branch Manager monitors caseload monthly and adds capacity before the queue builds; exam season (February–April for SSC CGL) is the peak demand period for counselling — advance planning is necessary
- Monthly counselling statistics (number of sessions, cases closed, referral sources) are shared with the Director quarterly as part of the student welfare review; the counselling load is an indicator of overall student stress level; a month with 42 sessions is significantly higher than the 28-session baseline, indicating elevated stress (exam approaching, fee defaults, academic pressure coinciding); the Director uses this to assess whether batch timings, academic pressure, or financial difficulty is the dominant stressor

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division J*
