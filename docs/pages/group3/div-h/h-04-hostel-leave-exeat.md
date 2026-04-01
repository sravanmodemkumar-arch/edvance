# H-04 — Hostel Leave & Exeat

> **URL:** `/school/hostel/leave/`
> **File:** `h-04-hostel-leave-exeat.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Student (via portal) — apply for leave · Warden (S3) — approve short leaves · Chief Warden (S4) — approve extended leaves · Principal (S6) — approve emergency/medical leaves · Parent (Parent Portal) — confirm/acknowledge leave

---

## 1. Purpose

Manages hostel leave — when a boarding student leaves the hostel premises for home or other approved purposes. P0 because:
- A student who has left the hostel on approved leave is accounted for in H-03; an unapproved departure is a safety emergency
- Indian boarding school regulations (state-specific) require schools to maintain a gate pass register for all student departures
- **Exeat** (Latin: "let him go out") is the traditional term for a student's leave pass from a boarding school; in Indian usage, it's the formal gate pass document
- **Parental consent required:** The school must have parent confirmation before releasing a student, especially for home visits by a student who will travel independently

Types:
- **Weekend leave (Exeat):** Typically Sat PM to Sun PM; requires parent pickup/drop
- **Home leave:** Longer school vacation; students travel home
- **Emergency leave:** Medical emergency, family death — same-day approval needed
- **Sick leave:** Student admitted to hospital; parents notified
- **Academic leave:** External exam/competition; school-sanctioned

---

## 2. Page Layout

### 2.1 Header
```
Hostel Leave & Exeat                                 [+ Apply Leave]  [Export Gate Pass Log]
Date: 27 March 2026 (Wednesday)

Tonight's leave summary:
  Students on approved leave (out of hostel): 8
  Pending approval: 3
  Emergency requests: 0

Weekend (28–30 Mar): 42 students have applied for weekend leave
```

### 2.2 Leave Register
```
Leave No.    Student         Leave Type    From          To           Status
HLV/2026/084 Vijay S. (X-B)  Weekend      28 Mar 7 PM   30 Mar 7 PM  ✅ Approved
HLV/2026/083 Priya V. (XI-A) Emergency    27 Mar 2 PM   27 Mar —     ✅ Approved (family)
HLV/2026/082 Arjun S. (XI-A) Weekend      28 Mar 7 PM   30 Mar 7 PM  ⏳ Pending (Warden)
HLV/2026/081 Meena D. (XII-A) Home leave  1 Apr         15 Apr       ✅ Approved (Principal)
```

---

## 3. Leave Application

```
[+ Apply Leave]

Student: [Arjun Sharma — XI-A — Boys' Hostel Room 101]
Leave type:
  ● Weekend leave (Sat 7 PM – Sun 7 PM)
  ○ Extended weekend (Fri evening – Mon morning)
  ○ Home leave (> 2 nights)
  ○ Emergency leave (same-day approval)
  ○ Medical leave (hospital referral)

From: [28 March 2026]  Time: [7:00 PM]
To:   [30 March 2026]  Time: [7:00 PM]

Destination: Home (Vijayawada)
Travel mode: ● Parent pickup  ○ School bus  ○ Local bus  ○ Train (student alone)
             ○ Other (specify)

If parent pickup:
  Who will collect: Father — Mr. Rajesh Sharma (+91 9876-XXXXX)
  Expected arrival at school: [28 Mar, 6:30 PM]

Parent confirmation required: ☑ Yes — WhatsApp request sent to parent:
  "Arjun Sharma has applied for weekend leave (28–30 Mar 2026).
   Please confirm: [Yes, I will collect him] [No, cancel leave]"

Reason (optional): [Going home for Ram Navami celebration]

[Submit Application]
```

---

## 4. Approval Workflow

```
Approval — HLV/2026/082 — Arjun Sharma — Weekend Leave

Parent confirmation: ✅ Father confirmed at 6:15 PM ("Yes, I will collect him")

Warden review (automatic check):
  ✅ Exam schedule: No exam on Mon 30 Mar (Annual Exam starts 1 Apr)
  ✅ Fee status: Paid up
  ✅ No outstanding conduct issues (H-10)
  ✅ Room key: Must be deposited before departure
  ⚠️ Annual Exam is 3 days away — note in approval

[Approve Leave]  [Reject with reason]  [Approve with condition: "Must return by 7 PM Sunday"]
```

After approval:
```
✅ Leave Approved — HLV/2026/082

Gate Pass issued: GP/2026/084
Valid: 28 Mar 2026 (7 PM) to 30 Mar 2026 (7 PM)

Gate Pass document:
  ┌───────────────────────────────────────────────────────┐
  │  HOSTEL EXEAT / GATE PASS                             │
  │  Student: ARJUN SHARMA  Class: XI-A  Room: 101        │
  │  Leave from: 28 Mar 2026 7:00 PM                      │
  │  Return by:  30 Mar 2026 7:00 PM                      │
  │  Destination: Home (Vijayawada)                        │
  │  Collected by: Father (Mr. Rajesh Sharma)             │
  │  Approved by: Mr. Suresh Kumar (Warden)               │
  │  Gate Pass No.: GP/2026/084                           │
  └───────────────────────────────────────────────────────┘

Gate staff notified: ✅
Parent WhatsApp: "Arjun's weekend leave is approved (GP/2026/084).
  Return by 30 Mar 7 PM. Warden contact: +91 9999-XXXXX"
```

---

## 5. Return Tracking

```
Return Tracking — Sunday 30 March 2026

Expected returns tonight: 42 students (weekend leave)
Checked in: 38 students ✅
Not yet returned (7 PM): 4 students

7:30 PM — still not returned: 2 students
  Vijay S.: Called parent — "on the way, delayed by traffic, ETA 8:30 PM"
            [Log delay — acceptable]
  Priya V.: No answer — [Alert Chief Warden]

8:00 PM — not returned: 1 student (Priya V.)
  → Chief Warden calls parent again
  → Escalate to Principal
  → 30-minute grace period then police protocol (if applicable)
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/leave/?date={date}` | Leave register for date |
| 2 | `POST` | `/api/v1/school/{id}/hostel/leave/` | Apply for leave |
| 3 | `POST` | `/api/v1/school/{id}/hostel/leave/{leave_id}/approve/` | Approve leave |
| 4 | `POST` | `/api/v1/school/{id}/hostel/leave/{leave_id}/return/` | Mark student returned |
| 5 | `GET` | `/api/v1/school/{id}/hostel/leave/{leave_id}/gate-pass-pdf/` | Gate pass PDF |
| 6 | `GET` | `/api/v1/school/{id}/hostel/leave/not-returned/?date={date}` | Overdue returns |
| 7 | `POST` | `/api/v1/school/{id}/hostel/leave/parent-confirm/{leave_id}/` | Parent confirmation webhook |

---

## 7. Business Rules

- No student leaves hostel premises without an approved gate pass — the gate staff are instructed to check GP number before allowing a student out; this is enforced procedurally (system generates GP, gate checks it)
- Parent must confirm all leaves except emergency (same-day emergency can be approved by Chief Warden with parent notification, not prior confirmation)
- If a student does not return by the approved time + 1-hour grace period, the parent is called; if unreachable in 30 minutes, police intimation (missing minor protocol applies)
- Exam period lock: No leave is approved in the 48 hours before an exam begins (configurable); emergency leave is the only exception and requires Principal approval
- Gate pass log (H-05 visitor register includes outgoing student log) is the legal record; it must be produced for police/parent disputes about when a student left the hostel
- Weekend leave frequency is monitored — a student who requests leave every weekend may be counselled (H-12 student welfare) as it may indicate hostel adjustment issues

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
