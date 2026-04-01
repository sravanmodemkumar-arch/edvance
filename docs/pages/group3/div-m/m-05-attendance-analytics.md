# M-05 — Student & Staff Attendance Analytics

> **URL:** `/school/mis/attendance/`
> **File:** `m-05-attendance-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full view · Vice Principal (S5) — full view · Academic Coordinator (S4) — student attendance · HR Officer (S4) — staff attendance · Class Teacher (S3) — own class only

---

## 1. Purpose

Attendance analytics goes beyond the daily register — it identifies patterns, chronic absenteeism, section-level disparities, and early warning signals before they become academic or welfare problems. CBSE requires 75% minimum attendance for board exam eligibility; the analytics module tracks every student's percentage throughout the year and auto-flags those approaching the threshold.

This module aggregates from:
- E-01 (Student Attendance — daily class-wise)
- L-02 (Staff Attendance — daily biometric + manual)

---

## 2. Student Attendance — School-Wide Overview

```
STUDENT ATTENDANCE — 2025–26
School working days completed: 220 (as of 27 March 2026 = year-end)

OVERALL ATTENDANCE RATE: 92.4%
(Total student-days present ÷ Total student-days expected × 100)

CLASS-WISE ATTENDANCE SUMMARY:
  Class   Students  Avg Att%  <75% count  75-85% count  >85% count
  VI       156       93.8%       1          12             143
  VII      162       92.7%       2          18             142
  VIII     158       92.1%       3          21             134
  IX       156       91.4%       4          24             128
  X        156       90.8%       6          28             122 ← pre-board pressure
  XI        92       91.2%       3          19              70
  XII       92       90.1%       5          22              65 ← board year stress
  ─────────────────────────────────────────────────────────────
  TOTAL   1,072      92.0%      24         144             804

CRITICAL (< 75% attendance — CBSE board eligibility risk):
  Students <75% (Classes I–XII): 24 students
  Students <65% (serious risk):   7 students
  [Class-wise list → CT notified; parent letter initiated for <75%]

RTE NOTE: Under RTE Act, a child cannot be detained (failed) in Classes I–VIII solely
for low attendance; however, school must document and inform parents.
```

---

## 3. Chronic Absenteeism Analysis

```
CHRONIC ABSENTEEISM (>15% absence = at risk)

ABSENTEEISM PATTERN CATEGORIES:
  Pattern               Count   Likely Cause                Action
  Monday/Friday peaks     8     Weekend extension           Parent call (CT)
  Festival/holiday ext.  12     Family travel               Noted; within acceptable
  Medical (SL-supported) 34     Illness — documented ✅      Monitor
  Undocumented            7     Unknown — welfare risk ⚠    Welfare flag (J-11)
  Transport-related        3     Rural distance — bus delay  Transport review (I-series)
  Post-exam dips          22     Exam fatigue pattern        Normal; monitor closely

TOP 10 CHRONIC ABSENTEES (students with >20% absence):
  Student ID  Class   Absence%  Last Parent Contact   Action Taken
  STU-0421    XI-A    24.1%     8 Feb 2026            Counsellor referral J-01 ✅
  STU-0618    XII-A   22.8%     15 Feb 2026           Welfare flag J-11 ✅
  STU-0734    X-B     21.4%     1 Mar 2026            Parent meeting arranged ✅
  STU-0891    IX-B    20.9%     22 Feb 2026           In counselling J-01 ✅
  [Full list: Principal + VP view]

SOS THRESHOLD: Students below 65% attendance in Classes X or XII trigger immediate
  Principal alert (board exam eligibility at serious risk — condonation from CBSE
  requires medical evidence + special application; condonation not guaranteed)
```

---

## 4. Section-Level Attendance Comparison

```
SECTION COMPARISON — Class IX (156 students)

  Section  Avg Att%  <75% count  Notes
  IX-A     93.2%     1           Highest — strong class teacher engagement
  IX-B     90.1%     2           Average
  IX-C     92.4%     1           Good
  IX-D     89.8%     3           Slightly below — 2 known welfare cases

  ⚠ IX-D: 3 students below 75% — two are J-11 welfare flags; attendance linked to
    home situation (welfare team aware)

INTER-CLASS PATTERN:
  Class X and XII have measurably lower attendance in October–November (pre-board
  stress, private coaching overlaps) — expected pattern, documented.
  Class VI has highest attendance (93.8%) — new students, engaged parents.
```

---

## 5. Staff Attendance Analytics

```
STAFF ATTENDANCE — 2025–26
Working days: 220

OVERALL STAFF ATTENDANCE RATE: 94.7%

STAFF ATTENDANCE BY CATEGORY:
  Category           Headcount  Avg Att%  LOP days  High-Absence (>12%)
  Teaching             52        95.2%      180       3 staff
  Non-teaching         38        94.8%      142       2 staff
  Transport (drivers)  15        93.4%       98       3 staff
  Transport (escorts)   9        92.1%       72       2 staff
  Hostel staff          8        94.0%       52       0

HIGH-ABSENCE TEACHING STAFF (>12% absence this year):
  Staff ID   Name           Absence%   LOP days  Pattern        HR Flag
  TCH-044    Mr. Vijay P.   18.2%       8 days   Irregular ⚠   PIP + welfare referral
  TCH-028    Ms. Radha N.   14.1%       3 days   Cluster around personal events ⚠
  TCH-046    Ms. Anita Rao   8.2%       0 days   New joiner (some onboarding absences) ✅

TRANSPORT DRIVER HIGH ABSENCE: 3 drivers (DRV-07, DRV-11, DRV-13) — requires
  HR review; transport safety risk if drivers substituting frequently (I-series)

MONDAY/FRIDAY PATTERN FLAGS: None this year ✅

SUBSTITUTE DEMAND CORRELATION:
  High staff absence months → high substitute demand (L-13)
  Peak: December 2025 (12 substitutes/day average) vs annual average 4.2/day
```

---

## 6. CBSE 75% Eligibility Tracker

```
CBSE 75% ATTENDANCE ELIGIBILITY — Board Classes

CLASS X (156 students — CBSE Board March 2026):
  Total working days (Apr 2025 – Mar 2026): 220

  Eligibility status:
    >85% attendance: 122 students ✅ (fully eligible)
    75–85%:           28 students ✅ (eligible — above minimum)
    65–75%:            5 students ⚠ (eligible but condonation may be needed
                                     if final count is below 75%)
    <65%:              1 student  🔴 CRITICAL (condonation required)

  CONDONATION CASE — STU-0734 (X-B):
    Attendance: 63.2% (139/220 days)
    Required for eligibility: 165 days (75%)
    Shortfall: 26 days
    Reason: Medical (hospitalisation 21 days documented + 5 family travel)
    CBSE condonation application: Being prepared by Principal
    Documents needed: Medical certificates, hospitalisation record
    Application due: 15 October 2025 (CBSE deadline for Medical Condonation)

CLASS XII (92 students — CBSE Board March 2026):
  >75%: 87 students ✅
  <75%:  5 students ⚠ (all have documented medical reasons; condonation in process)
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/mis/attendance/student-overview/` | School-wide student attendance |
| 2 | `GET` | `/api/v1/school/{id}/mis/attendance/chronic/?threshold=15` | Chronic absenteeism report |
| 3 | `GET` | `/api/v1/school/{id}/mis/attendance/section-comparison/?class={grade}` | Section-level comparison |
| 4 | `GET` | `/api/v1/school/{id}/mis/attendance/staff/` | Staff attendance analytics |
| 5 | `GET` | `/api/v1/school/{id}/mis/attendance/eligibility-tracker/` | CBSE 75% eligibility status |
| 6 | `GET` | `/api/v1/school/{id}/mis/attendance/at-risk/` | Students at risk of ineligibility |
| 7 | `POST` | `/api/v1/school/{id}/mis/attendance/condonation/` | Initiate CBSE condonation case |

---

## 8. Business Rules

- The 75% attendance threshold for CBSE Board examinations is hard — a student below 75% cannot sit for board exams without a CBSE condonation; the system proactively alerts from 80% downwards (not just at 75%) so there is time to act; waiting until 75% is crossed leaves no room for intervention
- Chronic absenteeism without documentation (undocumented pattern) triggers a welfare flag, not just an attendance flag — undocumented absences may indicate family problems, child labour, or other safeguarding concerns (especially in EWS/DG category students)
- Staff attendance analytics integration with substitute demand (L-13) is intentional — schools with high staff absence tend to over-rely on substitutes, degrading teaching quality; the correlation helps management address root causes rather than treating symptoms
- The section comparison view surfaces a common school management problem — same-grade sections with dramatically different attendance rates often reflect section-level culture issues (a strong class teacher vs a disengaged one); this is a coaching opportunity, not a punishment finding
- Condonation applications to CBSE require supporting documents to be filed with the Regional Office; EduForge helps generate the application letter and checklist, but the Principal must physically file it; the deadline is typically October for the same academic year

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division M*
