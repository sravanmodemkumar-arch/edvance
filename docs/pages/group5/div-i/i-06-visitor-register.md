# I-06 — Visitor Register

> **URL:** `/coaching/hostel/visitors/`
> **File:** `i-06-visitor-register.md`
> **Priority:** P2
> **Roles:** Hostel Warden (K3) · Security Guard (K1) · Branch Manager (K6)

---

## 1. Visitor Log

```
VISITOR REGISTER — 30 March 2026
Toppers Coaching Centre Hostel

  Time In  │ Visitor Name    │ Relation    │ Student Visited│ Room  │ Purpose       │ Time Out
  ─────────┼─────────────────┼─────────────┼────────────────┼───────┼───────────────┼──────────
  09:18 AM │ Krishnamurthy R │ Father      │ Suresh Babu    │ A-13  │ Visit / fruits│ 10:02 AM
  10:44 AM │ Laxmi Devi      │ Mother      │ Priya Reddy    │ B-11  │ Monthly visit │ 11:28 AM
  11:12 AM │ Ravi Kumar R.   │ Brother     │ Kiran Naidu    │ A-05  │ Drop materials│ 11:18 AM
  02:30 PM │ Anand Sharma    │ Uncle       │ Ravi Singh     │ A-04  │ Visit         │ 03:15 PM
  04:00 PM │ [BLOCKED]        │ Unrelated M │ Divya Sharma   │ B-08  │ Asked for Divya│ N/A

  BLOCKED VISIT (4:00 PM):
    Visitor: Unknown male, ~25 years, claimed "friend from hometown"
    Action: Warden required college ID — could not produce
    Divya Sharma (B-08) was called; confirmed she did not expect this visitor
    Visitor asked to leave ✅ | Security escorted to gate ✅
    Incident logged: VIS-2026-84

  VISITOR RULES DISPLAYED AT GATE:
    ✅ Visitors allowed only in designated visiting area (ground floor common room)
    ✅ No visitors in student rooms (Block B female — strictly no male visitors)
    ✅ All visitors must show govt ID (Aadhaar / DL / Passport)
    ✅ Visiting hours: 10 AM – 1 PM, 4 PM – 6 PM only
    ✅ Maximum 2 visitors per student simultaneously
```

---

## 2. Gate Pass & Student Exit

```
STUDENT EXIT LOG — 30 March 2026

  Time Out │ Student         │ Room  │ Destination           │ Expected Return │ Gate Pass
  ─────────┼─────────────────┼───────┼───────────────────────┼─────────────────┼──────────────
  2:00 PM  │ Ravi Singh      │ A-04  │ Apollo Hospital (appt)│ 5:00 PM         │ GP-1284 ✅
  4:00 PM  │ Priya Reddy     │ B-11  │ Dilsukhnagar (errand) │ 6:30 PM         │ GP-1285 ✅
  4:30 PM  │ Akhil Kumar     │ A-01  │ Branch campus (study) │ 8:00 PM         │ GP-1286 ✅

  RETURN LOG:
    Ravi Singh: Returned 4:48 PM ✅ (before 5 PM)
    Priya Reddy: Not yet returned (expected 6:30 PM — on time as of 5 PM)

  LATE RETURN (previous day):
    Mohammed R.: Expected 9:00 PM, returned 10:18 PM (18 min before curfew)
    No pass violation (within 10:30 PM curfew) — logged for awareness

  OVERNIGHT / LEAVE:
    No overnight leaves approved this week
    Upcoming leave requests:
      Sravya Rao (B-08): Apr 4–5 (home for family function) — approved by warden ✅
      Kiran Naidu (A-05): Apr 4–5 (hometown trip) — pending warden approval
```

---

## 3. Visitor Analytics

```
VISITOR PATTERN — March 2026

  Total visitor entries:       124
  Total blocked/denied:          4  (2 unknown males at Block B, 2 outside hours)
  Avg visitors per day:          4.1
  Peak visitor days:             Sundays (avg 8.4 visitors)
  Most visited students:
    Akhil Kumar (A-01):  12 visits (popular with family)
    Priya Reddy (B-11):  10 visits

  INCIDENT LOG (March 2026):
    VIS-2026-82: Unknown visitor refused at Block B (Mar 8) — no incident
    VIS-2026-83: Visitor attempted to enter after visiting hours (Mar 21) — refused
    VIS-2026-84: Unknown male refused at Block B (Mar 30 today) — logged above

  All 3 incidents: POCSO-relevant (Block B, female students) — forwarded to
  designated POCSO contact for monthly review ✅
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/hostel/visitors/?date=2026-03-30` | Visitor log for a day |
| 2 | `POST` | `/api/v1/coaching/{id}/hostel/visitors/` | Log a new visitor entry or exit |
| 3 | `POST` | `/api/v1/coaching/{id}/hostel/visitors/block/` | Log a blocked/denied visitor |
| 4 | `GET` | `/api/v1/coaching/{id}/hostel/exit/?date=2026-03-30` | Student exit and return log |
| 5 | `POST` | `/api/v1/coaching/{id}/hostel/exit/gate-pass/` | Issue a gate pass |
| 6 | `GET` | `/api/v1/coaching/{id}/hostel/visitors/incidents/` | Visitor incident log |

---

## 5. Business Rules

- All hostel visitors must produce government-issued photo ID (Aadhaar, Driving Licence, Passport, or Voter ID); the visitor's name, ID number, and relation to the student are recorded in the register; the student must be contacted and must confirm they are expecting the visitor before entry is permitted; a visitor who cannot produce ID or whom the student does not recognise is denied entry; the security guard has the authority to refuse entry and call the warden; this process is firm and consistent, not left to discretion
- Male visitors are strictly prohibited in Block B (female) residential areas; this is a safety rule, not a courtesy; the visiting area on the ground floor is gender-neutral; a father or brother visiting a female student meets in the common room, not in the student's room; this rule is enforced by both the warden and the security guard; a male visitor who enters Block B without authorisation (even if the student invited him) is subject to an incident report, and the student faces a hostel rule violation; the POCSO contact is notified of any blocked unknown male at Block B within 24 hours
- Visiting hours (10 AM–1 PM and 4 PM–6 PM on weekdays) are calibrated around class schedules; morning batch students are in class 6–9 AM; evening batch students are in class 4–7 PM; the visiting hours minimise disruption to class and study time; on Sundays, visiting hours are extended to 10 AM–5 PM as students have more free time; unexpected visits outside hours are directed to the warden, who may allow a brief meeting in the reception if there is a genuine emergency (bereavement, medical)
- Overnight leave requests must be submitted 48 hours in advance; the warden approves based on: (a) is it the student's legitimate family/personal event, (b) is there an upcoming test/class that will be missed, and (c) is there any safety concern; the warden cannot deny leave without reason for an adult student; for minor students, the leave request must come from the guardian (not just the student), and the warden may contact the guardian to confirm; leave approved after the fact (student left without approval) is a hostel rule violation
- The visitor incident log is reviewed monthly by the Branch Manager and the designated POCSO contact; all incidents involving unknown males at Block B are POCSO-relevant and must be escalated regardless of outcome; the POCSO contact may recommend additional security measures (cameras at entrance, additional guard shift) based on incident patterns; TCC's duty-of-care under POCSO for minor female students extends to the hostel premises and is documented in the annual compliance review (N-01)

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division I*
