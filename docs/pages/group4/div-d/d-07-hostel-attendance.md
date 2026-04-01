# D-07 — Hostel Attendance & Gate Pass

> **URL:** `/college/hostel/attendance/`
> **File:** `d-07-hostel-attendance.md`
> **Priority:** P1
> **Roles:** Warden (S3) · Hostel Supervisor (S3) · Chief Warden (S4)

---

## 1. Hostel Attendance System

```
HOSTEL ATTENDANCE — GCEH

NOTE: Hostel attendance is SEPARATE from academic class attendance.
  Academic attendance: Tracked by class faculty → A-05 module
  Hostel attendance: Tracks physical presence in hostel (curfew compliance + safety)
  The two systems do not merge; a student can be present in class but absent from hostel
  (day scholar mode after hostel expulsion or outpass)

BIOMETRIC GATE SYSTEM:
  Entry/Exit: Fingerprint scanner at hostel gate
  3 scan points: Boys' hostel main gate, Girls' hostel main gate, Side gate (emergency)
  Data: Student ID, timestamp, direction (IN/OUT)
  Real-time dashboard: Warden sees who is IN / OUT at any moment

EVENING ROLL CALL (mandatory — 9:00 PM):
  Method: Physical roll call by floor supervisor + biometric cross-check
  Floor supervisors assigned (2 floors per supervisor)
  Process: Supervisor calls each student's name; student acknowledges in person
           Biometric confirms "IN" status; physical presence confirms biometric = correct person
  Exceptions:
    Student on approved outpass: marked "OP" (outpass)
    Student at college event (warden-approved late return): marked "LE" (late event)
    Student in medical bay: marked "MED"
    Unaccounted absent: marked "UA" → immediate parent SMS alert

ROLL CALL STATUS — Block B, 27 March 2027, 9:00 PM:
  Present: 56 / 57 (Block B students)
  Absent (UA): 1 — Deepak R. (226J1A0522)
    Action: Warden called Deepak's phone (no answer)
            Warden called parent (father answered — Deepak is coming, delayed by traffic)
            Deepak returned 9:42 PM (42-min late) → Late return log updated
            Verbal warning issued (1st instance)
```

---

## 2. Overnight Absence Tracking

```
OVERNIGHT ABSENCE TRACKING

OVERNIGHT ABSENCE = Student not present at morning (6 AM check) AND was "UA" at night roll call

CLASSIFICATION:
  Approved absence: Student on valid home outpass (OP status)
  Approved event: College trip/sports outstation (group outpass — event warden)
  Medical: Student in hospital/medical leave (warden informed)
  Unapproved (AWOL): Student missing without permission ← ALERT

AWOL PROTOCOL:
  Triggered: If student UA at 9 PM AND not reachable by 10 PM AND no outpass
  Step 1 (10:00 PM): Warden calls student (3 attempts)
  Step 2 (10:15 PM): Warden calls parent/guardian
  Step 3 (10:30 PM): Chief Warden informed
  Step 4 (11:00 PM): If still uncontactable — written in night log; security notified
  Step 5 (Next day): If student still missing — Police NC filed by college
                     (Student missing from hostel overnight without contact)
  EduForge: Automatic parent SMS at step 1 trigger; Chief Warden alert at step 3

AWOL INCIDENTS 2026–27: 2 cases (both resolved — students had gone home without outpass)
  Counselling + written warning issued; outpass privileges suspended 30 days
```

---

## 3. Gate Pass System

```
GATE PASS — Three Types

TYPE 1: LOCAL OUTPASS (Day return, within city)
  Apply: EduForge → Hostel → Outpass → Local
  Fields: Date, destination, purpose, expected return time, contact number at destination
  Approval: Warden (usually within 2 hours)
  Parent notification: Auto-SMS on approval ("Kiran has been given outpass to...")
  Return: Biometric gate scan registers return; parent SMS on safe return

  GATE PASS — Approved
  Student: Kiran S. (226J1A0312)
  Date: 28 March 2027 (Saturday)
  Destination: Dilsukhnagar (family visit)
  Expected return: 9:00 PM
  Approved by: Warden Rajesh V. (9:15 AM)
  Parent informed: ✅ (SMS to father 9849XXXXXX)
  Return recorded: 8:47 PM ✅ (early return)

TYPE 2: HOME OUTPASS (1+ nights away)
  Apply: ≥24 hours in advance
  Parent confirmation: Parent receives OTP link via SMS → parent confirms pickup plan
  Approval chain: Warden → Chief Warden (for >3 nights)
  Return date: Student must return by stated date; delay requires fresh request
  SMS on departure + SMS on return (to parent)

TYPE 3: MEDICAL OUTPASS (hospitalisation / serious illness)
  Immediate on warden discretion (no advance notice possible)
  Parent emergency contact called
  Hospital details recorded (name, ward, treating doctor)
  Warden/faculty welfare check if in-city hospital
  Return: Medical clearance required; warden inspection before readmission to room

GATE PASS STATISTICS — 2026–27 (YTD):
  Local outpass: 1,842 approved, 14 denied (destination unclear / incomplete details)
  Home outpass: 624 approved, 3 revoked (returned late without re-application)
  Medical outpass: 28 (hospitalisation / medical leave)
```

---

## 4. Vacation & Semester Break

```
VACATION MANAGEMENT

SEMESTER I END (November 2026):
  Hostel closes: 30 November 2026
  All students must vacate by: 30 November 2026, 6:00 PM
  Exceptions: Students with exams continuing (JNTU schedule clash)
              Students from far-off states (Chief Warden discretion — limited rooms kept open)
  Valuables: Students encouraged to take valuables home; college not responsible for left items
             (clearly stated in hostel rules)

REOPEN FOR SEMESTER II: 2 January 2027
  Students returning: Must check in by 3 January 2027
  New allotments: Processed during vacation period
  Room change requests: Submitted during reopen; processed in first week

VACATION MESS:
  Mess closed during vacation (no fee charged for closed period)
  Mess-leave adjustment: ₹3,200/month × (days closed / 30) credited to next semester

PROPERTY SECURITY:
  All rooms locked and sealed by housekeeping (list maintained)
  Security (2 guards retained) — perimeter patrol
  CCTV monitoring continues
  Warden (at least one) on campus throughout vacation (AICTE requirement)
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hostel/attendance/realtime/` | Real-time IN/OUT status |
| 2 | `POST` | `/api/v1/college/{id}/hostel/attendance/rollcall/` | Submit roll call (warden) |
| 3 | `GET` | `/api/v1/college/{id}/hostel/attendance/missing/` | UA/AWOL students list |
| 4 | `POST` | `/api/v1/college/{id}/hostel/gatepass/apply/` | Apply for gate pass |
| 5 | `POST` | `/api/v1/college/{id}/hostel/gatepass/{id}/approve/` | Approve gate pass |
| 6 | `GET` | `/api/v1/college/{id}/hostel/gatepass/active/` | Currently active outpasses |

---

## 6. Business Rules

- Hostel attendance tracking is a critical safety system, not just an administrative exercise; in incidents involving student injury, death, or missing persons, the first question from police and families is "when was the student last seen in hostel?" — the gate log and roll call log provide forensic-quality evidence of the student's movements; these logs must be tamper-proof and retained for at least 3 years
- Parent SMS alerts for UA (unaccounted absence) at roll call are not invasion of privacy — they are a duty of care; a 19-year-old living away from home in a college hostel is under the institution's care during that period; parents are entitled to know if their ward is unaccounted; courts have held colleges liable for negligence when they failed to notify parents of missing students
- The AWOL protocol escalating to police NC (non-cognisable complaint) must be followed consistently; a college that does not file an NC for a student who is genuinely missing (vs on outpass) and later something bad happens faces criminal charges of dereliction of duty; filing the NC protects the institution
- Hostel closure during semester break must provide adequate notice (at least 7 days); students from distant states who cannot travel home due to cost or logistics must be accommodated; charging full mess fee for days the mess is closed is impermissible — credits must be applied automatically
- Gate biometric data is personal data under DPDPA 2023; it must be retained only for the purpose of hostel safety management; it cannot be shared with third parties (e.g., parents who ask for detailed movement logs beyond standard notifications) without the student's consent; a parent's right to safety notification is different from a right to detailed surveillance data of their adult ward

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division D*
