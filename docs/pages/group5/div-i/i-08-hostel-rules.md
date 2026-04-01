# I-08 — Hostel Rules & Disciplinary

> **URL:** `/coaching/hostel/rules/`
> **File:** `i-08-hostel-rules.md`
> **Priority:** P3
> **Roles:** Hostel Warden (K3) · Branch Manager (K6) · POCSO Contact (K5)

---

## 1. Hostel Rules Reference

```
HOSTEL RULES — Toppers Coaching Centre (AY 2026–27)
Signed by student and guardian at admission

  GENERAL CONDUCT:
    1. Curfew: 10:30 PM daily. Late-pass required for exceptions.
    2. Visitors only in common room, 10 AM–1 PM and 4 PM–6 PM.
    3. Male visitors not permitted in Block B (female) at any time.
    4. Smoking, alcohol, and drugs strictly prohibited in hostel premises.
    5. Loud music/noise after 9:00 PM is prohibited (study hours).
    6. No cooking in rooms (fire safety — hot plates, induction prohibited).

  SECURITY:
    7. All entries/exits must be logged at the security desk.
    8. Room keys must not be duplicated; loss = ₹300 replacement fee.
    9. CCTV recording on common areas; rooms are not monitored.
    10. Any suspicious person/activity must be reported to warden immediately.

  STUDY ENVIRONMENT:
    11. Mandatory study hours: 9:00 PM – 10:30 PM (warden supervised).
    12. Mobile phones on silent during study hours.
    13. Study room (Block A ground floor) available 6 AM – 11 PM.
    14. No online gaming during study hours (wifi usage monitored).

  MESS:
    15. Meals served at fixed times; no food in rooms (pest control).
    16. Special dietary needs must be registered with warden.
    17. Meal tokens for skips must be submitted by 9 AM.

  PROPERTY:
    18. Damages to TCC property will be charged at replacement cost.
    19. Rooms must be kept clean; weekly inspection by warden.
    20. No personal appliances (heaters, kettles) without written warden approval.
```

---

## 2. Disciplinary Log

```
DISCIPLINARY CASES — AY 2026–27 (Active)

  Case ID  │ Student        │ Room  │ Violation              │ Date    │ Action Taken     │ Status
  ─────────┼────────────────┼───────┼────────────────────────┼─────────┼──────────────────┼──────────────
  DISC-0021│ Mohammed R.    │ A-12  │ Smoking in room (Rule 4)│ 15 Feb  │ Written warning  │ 1st warning ✅
  DISC-0028│ Kiran Naidu    │ A-05  │ Late return (curfew+35m)│ 22 Mar  │ Verbal warning   │ Noted ✅
  DISC-0031│ Sravya Rao     │ B-08  │ Noise after 9 PM        │ 25 Mar  │ Verbal warning   │ Noted ✅
  DISC-0032│ Mohammed R.    │ A-12  │ 2nd smoking incident    │ 28 Mar  │ Guardian notified│ 2nd warning ⚠️

  ESCALATION THRESHOLD:
    3rd warning within 90 days → Disciplinary committee hearing (warden + Branch Mgr)
    Outcome of hearing: suspension (1–7 days) or permanent hostel exit
    POCSO-sensitive violations (harassment, gender boundary violations): immediate
    hearing regardless of warning count

  MOHAMMED R. STATUS:
    2nd warning for smoking (28 Mar)
    Guardian called (father): Acknowledged, assured it won't recur
    Monitoring: Warden to do unannounced room check weekly for 30 days
    1 more violation in 90 days → Disciplinary hearing → hostel exit risk
```

---

## 3. Monthly Inspection Report

```
MONTHLY INSPECTION — March 2026
Conducted by: Ms. Sunitha Verma (Warden) | Date: 28 March 2026

  BLOCK A — INSPECTION SUMMARY:
    Rooms inspected:  20/20 ✅
    Clean rooms:      18 (90%)
    Needs attention:   2 (A-06: dusty surfaces; A-12: smell of smoke confirmed)
    Structural issues: 1 (A-12 — tube light)

  BLOCK B — INSPECTION SUMMARY:
    Rooms inspected:  20/20 ✅
    Clean rooms:      19 (95%)
    Needs attention:   1 (B-08: excessive personal items on floor — fire safety)
    Structural issues: 1 (B-03 — leaking tap)

  COMMON AREAS:
    Study room: ✅ Clean and functional (projector bulb was replaced Mar 28)
    Mess: ✅ Kitchen hygiene checked; contractor FSSAI displayed ✅
    Gate/CCTV: ✅ Repaired Mar 28

  OVERALL HOSTEL CONDITION: Good  (March rating: 8.2/10)
  Report submitted to: Branch Manager — 29 March 2026 ✅
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/hostel/rules/` | Hostel rules reference |
| 2 | `GET` | `/api/v1/coaching/{id}/hostel/disciplinary/` | Disciplinary case log |
| 3 | `POST` | `/api/v1/coaching/{id}/hostel/disciplinary/` | Log a new disciplinary incident |
| 4 | `PATCH` | `/api/v1/coaching/{id}/hostel/disciplinary/{did}/` | Update case (action taken, escalation) |
| 5 | `POST` | `/api/v1/coaching/{id}/hostel/inspection/` | Submit monthly inspection report |
| 6 | `GET` | `/api/v1/coaching/{id}/hostel/inspection/?month=2026-03` | Inspection report |

---

## 5. Business Rules

- The disciplinary process follows a graduated response: verbal warning → written warning (with guardian notification for minors) → disciplinary committee hearing → suspension or hostel exit; no student is expelled from the hostel without a hearing where they have the opportunity to explain their side; the hearing record is documented; for adult students, guardian notification is at the warden's discretion unless the violation involves safety or POCSO concerns; for minor students, guardian notification is mandatory at the written warning stage
- POCSO-relevant violations (any incident involving a minor student of opposite gender, or any incident of harassment, inappropriate photography, or gender boundary violations) bypass the standard warning process and trigger an immediate disciplinary hearing with the Branch Manager and POCSO-designated contact within 24 hours; TCC's POCSO compliance policy (N-02) requires all such incidents to be reported regardless of outcome; even if the incident is determined to be minor after investigation, the documentation must exist
- The "3 warnings = hearing" rule has a 90-day reset; a student who received 2 warnings in October and November, and then was incident-free until March, does not face a hearing for a March incident (the October warning is outside the 90-day window); however, the warden notes the pattern; a student with 6 incidents over 1 year (each more than 90 days apart) still demonstrates a pattern of disregard for hostel rules; this persistent pattern is raised in the annual renewal of hostel accommodation (not automatic renewal for rule violators)
- Monthly hostel inspections are documented and filed; inspection reports serve as evidence in deposit deduction disputes (student claims the damage was pre-existing, inspection report shows otherwise); the inspection report rating (8.2/10 in March) is shared with the Director quarterly as a hostel quality KPI; persistent low ratings (< 7.0) indicate either maintenance neglect or inadequate enforcement of cleanliness rules — both are addressed by the Branch Manager
- Students with smoking, alcohol, or drug violations are referred to the student counsellor (not just disciplinarily warned); these behaviours are often stress responses to exam pressure; a student who smokes in their room despite a warning is likely anxious or stressed, not merely rule-defiant; the counsellor referral (combined with the disciplinary warning) addresses the root cause; if the behaviour continues, the hostel exit follows, but the counsellor's engagement may have already helped the student find healthier coping strategies before that point

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division I*
