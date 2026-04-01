# J-03 — At-Risk Student Management

> **URL:** `/coaching/student-affairs/at-risk/`
> **File:** `j-03-at-risk-students.md`
> **Priority:** P1
> **Roles:** Student Counsellor (K3) · Batch Coordinator (K4) · Branch Manager (K6)

---

## 1. At-Risk Dashboard

```
AT-RISK STUDENTS — All Batches (Toppers Coaching Centre)
As of 30 March 2026

  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  TOTAL AT-RISK: 48  │  HIGH RISK: 12  │  MEDIUM RISK: 22  │  MONITORING: 14 │
  └──────────────────────────────────────────────────────────────────────────────┘

  BY BATCH:
    Batch              │ Enrolled │ At-Risk │ % At-Risk │ Risk Level
    ───────────────────┼──────────┼─────────┼───────────┼──────────────────────
    SSC CGL Morning    │   240    │    18   │   7.5%    │ 🟡 Moderate
    SSC CGL Evening    │   220    │    12   │   5.5%    │ ✅ Low
    Banking Morning    │   200    │    10   │   5.0%    │ ✅ Low
    RRB NTPC           │   200    │     8   │   4.0%    │ ✅ Low
    Foundation         │   150    │     4   │   2.7%    │ ✅ Low
    Others             │   274    │     6   │   2.2%    │ ✅ Low

  ALERT: SSC CGL Morning has the highest at-risk rate (7.5%)
  Reason: This batch has the largest enrollment and is closest to exam
          (SSC CGL Apr 2026) — stress + performance pressure elevated

  CRITERIA FOR AT-RISK FLAG:
    Any ONE of:   Attendance < 70% this month
    Or:           Avg score last 3 tests < 35%
    Or:           Fee overdue > 30 days
    All three:    Escalated to Branch Manager (multi-risk)
```

---

## 2. At-Risk Student Detail

```
AT-RISK PROFILE — Mohammed Riyaz Ahmed (TCC-2406)
As of 30 March 2026

  RISK FACTORS (3 of 3 — MULTI-RISK → Branch Manager escalated):
    ├─ Attendance:   57.1%  ← below 70%  🔴
    ├─ Avg score:    48.2%  ← 28.2% lower than batch avg (normally < 35% cutoff)
    └─ Fee overdue:  45 days  🔴

  INTERVENTION HISTORY:
    Jan 28:  Auto-SMS (attendance alert)
    Feb 12:  Batch coordinator call (Priya Nair): "will improve"
    Feb 28:  Counselling referral (Session #1 with Ananya Roy)
    Mar 18:  Branch Manager call (personal check-in)
    Mar 22:  Hostel warden reported 2nd smoking violation
    Mar 28:  Smoking violation → guardian notified (BM approved)
    Mar 30:  Counselling session #3 today (10 AM)

  CURRENT STATUS: Under active counselling + Branch Manager monitoring
  ACTION PLAN:
    [✓] Counselling ongoing (Sessions 1, 2 done; #3 today)
    [✓] Fee: Accounts team to discuss 2-week extension (via counsellor)
    [ ] Attendance: Target 75% in April (currently 57%)
    [ ] Hostel: 3rd smoking violation = disciplinary hearing

  RISK LEVEL:   🔴 High (multi-risk)
  LAST UPDATED: 30 Mar 2026 (counsellor: Ananya Roy)
```

---

## 3. Intervention Workflow

```
AT-RISK INTERVENTION PROTOCOL — TCC

  STAGE 1 (Auto — Any 1 risk factor):
    System auto-flag → Auto-SMS to student → Batch coordinator alerted
    Timeline: Immediate on trigger

  STAGE 2 (Coordinator — Within 48 hrs):
    Batch coordinator personal call → Document outcome → Set 2-week target
    If improved → monitor; if no improvement → Stage 3

  STAGE 3 (Counsellor — Within 1 week):
    Counselling referral → Initial session → Support plan
    Coordinator + counsellor share brief (no session notes) on progress

  STAGE 4 (Management — After 30 days / multi-risk):
    Branch Manager review → Joint intervention plan
    Decision: Continue support / fee rescheduling / enrollment decision

  STAGE 5 (Director — Critical / complex cases):
    Multi-month non-improvement / hostel safety concerns / legal risk
    Director joins the review

  CURRENT DISTRIBUTION:
    Stage 1 (auto):       22 students
    Stage 2 (coordinator): 14 students
    Stage 3 (counsellor):  8 students
    Stage 4 (BM):          4 students
    Stage 5 (Director):    0 students
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-affairs/at-risk/` | All at-risk students |
| 2 | `GET` | `/api/v1/coaching/{id}/student-affairs/at-risk/{sid}/` | At-risk profile with full history |
| 3 | `POST` | `/api/v1/coaching/{id}/student-affairs/at-risk/{sid}/intervention/` | Log an intervention action |
| 4 | `PATCH` | `/api/v1/coaching/{id}/student-affairs/at-risk/{sid}/stage/` | Update intervention stage |
| 5 | `GET` | `/api/v1/coaching/{id}/student-affairs/at-risk/summary/?batch={bid}` | Batch-level at-risk summary |

---

## 5. Business Rules

- At-risk flags are generated automatically by the system every 24 hours based on the latest attendance, test, and fee data; a student who crosses the threshold today appears in the at-risk list tomorrow morning; the coordinator receives a daily digest of new flags, not real-time alerts (to avoid alert fatigue); a student who recovers above the threshold (attendance rises back to 70%+) is automatically moved to "monitoring" status, not immediately cleared; the 2-week monitoring period confirms the improvement is sustained
- The multi-risk protocol (all 3 factors triggered simultaneously) reflects a student who is simultaneously academically disengaged, financially stressed, and possibly considering dropping out; the Branch Manager's involvement at this stage is not to pressure the student but to understand whether TCC can remove one of the barriers (e.g., fee extension for a student with a genuine hardship) that might allow the student to re-engage; the Branch Manager's call is supportive, not disciplinary
- At-risk data is reviewed in the monthly management meeting; the "% at-risk" by batch is a batch health indicator; the SSC CGL Morning batch's 7.5% at-risk rate (vs 4% for Foundation) is not alarming in isolation — SSC CGL students are under more exam pressure and are closer to the exam date; context matters; the benchmark comparison is this batch's at-risk rate vs the same batch in previous years; if it's higher than previous years, the cause is investigated
- Intervention outcome data (did the student improve after each stage?) is used to evaluate the intervention protocol's effectiveness; if Stage 2 (coordinator call) resolves 60% of cases, and Stage 3 (counselling) is needed only for 30%, the protocol is working well; if 80% require Stage 3+, it suggests the coordinator's early intervention is ineffective and needs training; this feedback loop improves the protocol over time
- Student confidentiality is maintained even in the management review; when the Branch Manager reviews the at-risk list, they see the risk factors (attendance, score, fee) but not the counselling session content; the counsellor verbally briefs the BM on "the student is dealing with a family health situation and is making progress" without sharing clinical details; this allows the BM to make an informed decision while preserving the student's privacy

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division J*
