# B-01 — Attendance Tracker

> **URL:** `/parent/academics/attendance/`
> **File:** `b-01-attendance-tracker.md`
> **Priority:** P1
> **Roles:** Parent (read-only) · Institution Admin (marks attendance, configures alert thresholds)

---

## 1. Multi-Child Attendance Overview

```
ATTENDANCE TRACKER — Mrs. Lakshmi Devi's Children
31 Mar 2026, Monday

  ── SELECT CHILD ─────────────────────────────────────────────────────────────

  [*] Priya Kumar — Sri Chaitanya Jr College   [ ] Ravi Kumar — GCEH (B.Tech)
      Class 11 MPC, Vijayawada                     B.Tech CSE 3rd Yr, Hyderabad
      AP State Board                                JNTU-H Affiliated

  [ ] Ravi Kumar — TopRank Academy
      GATE CSE Prep (Coaching)

  ── PRIYA KUMAR — DAILY ATTENDANCE (March 2026) ─────────────────────────────

  Month: [ < Feb ]  March 2026  [ Apr > ]

   Mon   Tue   Wed   Thu   Fri   Sat
                 1P    2P    3P    4A
    6P    7P    8P    9P   10P   11-
   13P   14P   15A   16P   17P   18-
   20P   21P   22P   23P   24P   25-
   27P   28P   29P   30P   31P

   P = Present (green)  A = Absent (red)  L = Leave (yellow)  - = Holiday/Sunday

  MONTHLY SUMMARY
  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
  │  WORKING DAYS    │  │  DAYS PRESENT    │  │  ATTENDANCE %    │
  │       26         │  │       24         │  │     92.3%        │
  │                  │  │                  │  │  [OK — Above 75%]│
  └──────────────────┘  └──────────────────┘  └──────────────────┘

  Absences this month:  04 Mar (Sat — sick, medical cert uploaded)
                        15 Mar (Wed — family function, leave approved)

  YEAR-TO-DATE (Jun 2025 – Mar 2026):  Working: 248  |  Present: 228  |  92.0%
```

---

## 2. College Attendance — Semester & Subject View (Ravi Kumar, GCEH)

```
ATTENDANCE — Ravi Kumar | B.Tech CSE, 3rd Year, Sem 5
GCEH, Hyderabad | JNTU-H Affiliated | Academic Year 2025-26

  ── SEMESTER ATTENDANCE SUMMARY ──────────────────────────────────────────────

  Overall Attendance:  78.2%   [!! WARNING — Below 80% threshold]
  JNTU-H Exam Eligibility Requires: 75% minimum
  Status: ELIGIBLE (but at risk — 3.2% buffer remaining)

  ┌───────────────────────────────────────────────────────────────────────────┐
  │  Subject               │ Theory  │ Lab     │ Combined │ Status           │
  ├────────────────────────┼─────────┼─────────┼──────────┼──────────────────┤
  │  Data Structures       │ 82%     │ 88%     │ 84.0%    │ OK               │
  │  Database Systems      │ 76%     │ 80%     │ 77.5%    │ WARNING (< 80%)  │
  │  Computer Networks     │ 74%     │ 82%     │ 76.8%    │ WARNING (< 80%)  │
  │  Operating Systems     │ 80%     │ 85%     │ 81.6%    │ OK               │
  │  Software Engineering  │ 72%     │ --      │ 72.0%    │ CRITICAL (< 75%) │
  │  Environmental Science │ 78%     │ --      │ 78.0%    │ WARNING (< 80%)  │
  └────────────────────────┴─────────┴─────────┴──────────┴──────────────────┘

  [!] ALERT: Software Engineering at 72.0% — 4 more absences will drop below
      JNTU-H 75% eligibility. Ravi must attend ALL remaining SE classes.

  CLASSES REMAINING THIS SEMESTER: 22 (Theory) + 8 (Lab)
  CLASSES NEEDED TO REACH 80%:    Must attend 20 of next 22 theory classes

  ── LAB ATTENDANCE (Separate Tracking per JNTU-H Rule) ──────────────────────

  Data Structures Lab    :  22/25 sessions  = 88.0%  [OK]
  Database Systems Lab   :  20/25 sessions  = 80.0%  [OK]
  Computer Networks Lab  :  18/22 sessions  = 81.8%  [OK]
  Operating Systems Lab  :  17/20 sessions  = 85.0%  [OK]

  ── COACHING ATTENDANCE — TopRank Academy (GATE CSE Prep) ────────────────────

  Mock Tests Attended  :  14 / 18 scheduled  =  77.8%
  Practice Sessions    :  22 / 30 available  =  73.3%
  Live Doubt Classes   :   8 / 10 conducted  =  80.0%
  Last Mock Attended   :  28 Mar 2026 — GATE Mock #14 (scored 78/100)
```

---

## 3. Absence Alerts & Leave Request History

```
ALERTS & NOTIFICATIONS — Attendance

  ── ACTIVE ALERTS ────────────────────────────────────────────────────────────

  [!!] URGENT  31 Mar 2026  Ravi Kumar — Software Engineering attendance
       10:15 AM             dropped to 72.0%. Risk of JNTU-H exam debarment
                            if 3 more classes missed. SMS sent to parent.
                            Action: Contact institution  [ View Details ]

  [!]  WARNING  28 Mar 2026  Ravi Kumar — Overall attendance 78.2%.
       08:00 AM              Below 80% institutional warning threshold.
                             Parent-teacher meeting recommended.
                             [ Request PTM ]  [ Acknowledge ]

  [i]  INFO     15 Mar 2026  Priya Kumar — Marked absent today.
       09:30 AM              Reason: Leave application (family function).
                             Leave status: Approved by class teacher.

  ── LEAVE REQUEST HISTORY ────────────────────────────────────────────────────

  Child          Date         Reason              Status      Approved By
  ─────────────  ───────────  ──────────────────  ──────────  ────────────────
  Priya Kumar    15 Mar 2026  Family function     Approved    Mrs. Rani (CT)
  Priya Kumar    04 Mar 2026  Sick (medical cert) Approved    Mrs. Rani (CT)
  Ravi Kumar     22 Feb 2026  Unwell              Approved    Dr. Rao (HOD)
  Ravi Kumar     10 Feb 2026  Personal            Rejected    Dr. Rao (HOD)
  Priya Kumar    18 Jan 2026  Family emergency    Approved    Mrs. Rani (CT)

  ── SUBMIT NEW LEAVE REQUEST ─────────────────────────────────────────────────

  Child:     [ Priya Kumar       v ]
  Date(s):   [ 05 Apr 2026 ] to [ 05 Apr 2026 ]
  Reason:    [ ________________________________ ]
  Attachment:[ Upload medical certificate / letter ]

                                            [ Cancel ]  [ Submit Request ]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/parent/academics/attendance/{child_id}/summary/` | Monthly and yearly attendance summary for a child |
| 2 | `GET` | `/api/v1/parent/academics/attendance/{child_id}/daily/?month=2026-03` | Day-by-day attendance calendar for a given month |
| 3 | `GET` | `/api/v1/parent/academics/attendance/{child_id}/subjects/` | Subject-wise attendance breakdown (college/coaching) |
| 4 | `GET` | `/api/v1/parent/academics/attendance/{child_id}/labs/` | Lab-specific attendance (JNTU-H separate lab tracking) |
| 5 | `GET` | `/api/v1/parent/academics/attendance/{child_id}/alerts/` | Active attendance alerts and warnings for a child |
| 6 | `POST` | `/api/v1/parent/academics/attendance/{child_id}/leave/` | Submit a leave request on behalf of the child |
| 7 | `GET` | `/api/v1/parent/academics/attendance/{child_id}/leave/history/` | Leave request history with status and approver details |
| 8 | `GET` | `/api/v1/parent/academics/attendance/overview/` | All children attendance summary for the logged-in parent |

---

## 5. Business Rules

- Attendance percentage calculation follows the institution's affiliated university or board rules, not a single platform-wide formula; for Ravi Kumar at GCEH, JNTU-H mandates that attendance is computed as (classes attended / classes conducted) per subject, and a student scoring below 75% in any individual subject is debarred from the external examination for that subject — this is not an overall average but a per-subject gate; the parent portal displays both the overall and per-subject figures because parents frequently confuse the two, and showing only the overall 78.2% would mask the fact that Software Engineering is at a critical 72.0%; for Priya Kumar at Sri Chaitanya Junior College under AP State Board, the 75% rule applies to overall attendance across all subjects combined, so the per-subject breakdown is informational but not a debarment trigger; the platform reads the attendance rule configuration from the institution's setup (configured during onboarding in Group 8, Division A) and adapts the warning thresholds accordingly

- Attendance alerts are dispatched to parents through three channels — push notification, SMS, and in-app alert — with configurable thresholds set by the institution admin; the default thresholds are: informational alert at 85% (early warning), warning at 80% (parent-teacher meeting recommended), and critical at 76% (one percentage point above the typical 75% debarment line); when Ravi Kumar's Software Engineering attendance dropped to 72.0%, the system escalated to a critical alert because it had already breached the 75% threshold, and the institution's academic office was simultaneously notified so that the HOD can initiate the condonation process if applicable; SMS alerts use the DLT-registered template mandated by TRAI for transactional messages, and the parent's registered mobile number receives the alert within 30 seconds of the attendance being marked by the faculty; the platform does not send attendance SMSes between 9 PM and 8 AM IST to comply with TRAI's time-of-day restrictions

- Leave requests submitted by parents through the portal enter the institution's approval workflow and do not automatically update attendance records; when Mrs. Lakshmi Devi submits a leave request for Priya Kumar, it is routed to the class teacher (Mrs. Rani) who can approve, reject, or request additional documentation such as a medical certificate; approved leave converts the absence from "absent" to "leave" in the attendance register, but the day still counts as a non-attendance day for percentage calculation unless the institution's policy grants attendance credit for approved medical leave (some JNTU-H affiliated colleges grant condonation of up to 10% for medical leave with valid documentation); the parent can upload supporting documents (medical certificate, travel tickets) as PDF or image attachments up to 5 MB each; the leave request status (pending, approved, rejected) is visible in real-time on the parent portal, and a push notification is sent when the status changes

- Coaching centre attendance (TopRank Academy for Ravi Kumar's GATE preparation) is tracked differently from formal institutional attendance because coaching sessions are optional and do not carry a regulatory attendance requirement; the platform tracks three metrics — mock test attendance, practice session attendance, and live doubt-clearing class attendance — and presents them as engagement indicators rather than compliance metrics; however, the parent portal still shows these figures prominently because parents paying for coaching subscriptions (typically Rs.5,000 to Rs.15,000 per quarter) need visibility into whether their child is actually utilizing the service; if a coaching student's mock test attendance drops below 50%, the system generates a "low engagement" alert to the parent, and the coaching admin can configure an auto-generated WhatsApp message to the parent explaining the upcoming test schedule and encouraging participation; this engagement tracking is a key differentiator for EduForge's coaching partners because it directly addresses the Indian parent's concern of "is my child actually studying or just wasting the subscription fee"

---

*Last updated: 2026-03-31 · Group 8 — Parents Portal · Division B*
