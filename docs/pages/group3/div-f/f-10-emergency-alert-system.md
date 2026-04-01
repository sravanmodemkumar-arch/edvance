# F-10 — Emergency Alert System

> **URL:** `/school/emergency-alerts/`
> **File:** `f-10-emergency-alert-system.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Principal (S6) — trigger any emergency alert · Administrative Officer (S3) — trigger operational alerts (early dismissal, bus delay) · Academic Coordinator (S4) — trigger academic emergencies · Security/Warden — trigger safety alerts (any S3+) · All staff — receive alerts

---

## 1. Purpose

Mass emergency notification system for situations requiring immediate parent communication. P0 because speed is critical — a parent who doesn't know their child's school is in lockdown will call repeatedly, block office lines, and possibly arrive at school making security worse. Situations covered:

- **Fire/evacuation:** Parents notified "students safe, evacuated to [location]"
- **Lockdown (security threat):** "School under lockdown — do not come to school; students are safe; await further notice"
- **Early dismissal:** Sudden school closure (teacher strike, infrastructure failure, cyclone warning)
- **Medical emergency (individual):** Specific student has an emergency; parent to come immediately
- **Accident (bus/school):** Parents of students involved notified privately + all parents notified if major incident
- **Natural disaster (pre-emptive):** Before a cyclone/flood warning triggers school closure
- **Missing student:** If a student cannot be accounted for during roll call

Indian regulatory context:
- **NDMA (National Disaster Management Authority):** Schools must have emergency communication plans
- **POCSO:** If alert involves possible POCSO scenario — POCSO Designated Person + police notified simultaneously
- **CERT-In (Cyber Emergency):** Cyber incident at school (data breach) triggers different protocol

---

## 2. Alert Trigger Interface

The interface must be operable in under 30 seconds in an emergency:

```
🚨 EMERGENCY ALERT SYSTEM

[FIRE / EVACUATION]      [LOCKDOWN — SECURITY]    [EARLY DISMISSAL]
   → Immediate           → Immediate               → 30 min notice

[BUS ACCIDENT]           [MEDICAL EMERGENCY]       [MISSING STUDENT]
   → Selective           → Selective               → Immediate

[WEATHER CLOSURE]        [CYBER INCIDENT]          [CUSTOM MESSAGE]
   → Pre-scheduled       → Admin only              → Any
```

### 2.1 One-Tap Alert (Pre-written)

Tapping [FIRE / EVACUATION]:

```
CONFIRM EMERGENCY ALERT

⚠️ This will immediately send WhatsApp + SMS to ALL 380 parents.

Type: FIRE / EVACUATION
Message (pre-written, editable):
  "URGENT: [Greenfields School] has initiated a fire evacuation.
   All students are safe and have been moved to [Cricket Ground].
   School will contact you with further updates. DO NOT come to
   school at this time. Emergency contact: 040-23456789.
   — Principal, Greenfields School"

Audience: ● ALL PARENTS  ○ Specific classes
Channel:  ☑ WhatsApp  ☑ SMS  ☑ Push notification  ☑ Staff group

[SEND NOW — CONFIRM]   ← Red button, must tap twice (double-confirm prevents accidental send)
```

After confirmation:
```
✅ EMERGENCY ALERT SENT — 27 Mar 2026, 11:42:37 AM

Recipients: 380 parents
WhatsApp: Sending...  (380 queued)
SMS: Sending...  (380 queued)
Push: Sending...  (312 registered)

Delivery progress: ████████░░ 74% complete (2 minutes)

Staff notification: ✅ Sent to all 48 staff
Admin portal alert: ✅ Live banner displayed

[Send Update to Parents]  [Declare All-Clear]  [Log Incident]
```

---

## 3. Selective Alert (Medical / Bus Accident)

```
MEDICAL EMERGENCY ALERT

Student: [Search by name or roll] → Ravi Kumar (XI-A, Roll 08)

Notify:
  ☑ Student's parents/emergency contacts
    Primary: Father — Mr. Suresh Kumar (+91 9876-XXXXX)
    Secondary: Mother — Mrs. Priya Kumar (+91 8765-XXXXX)
    Emergency: Uncle — Mr. Vikram (+91 7654-XXXXX)

  ☑ Class Teacher: Ms. Anita Reddy
  ☐ All parents of same class
  ☐ All parents

Message:
  "URGENT: Your ward Ravi Kumar (Class XI-A) has experienced a medical emergency
   at school. He is currently receiving first aid / has been taken to [Hospital Name].
   Please contact school immediately: 040-23456789. Principal, Greenfields School"

Additional: ☑ Include school address and hospital address if applicable

[SEND NOW]
```

---

## 4. Missing Student Protocol

```
MISSING STUDENT ALERT

Student: [Name, Class]
Last seen: [Time] at [Location — class / playground / toilet]
Duration missing: [15 minutes]

Immediate actions triggered:
  ✅ CCTV review alert sent to Admin Officer
  ✅ All teachers notified to check their classes and areas
  ✅ Gate security notified (check gate log / CCTV)

If not found in 15 minutes:
  → Parent notified (phone call + WhatsApp)
  → Police informed (IPC Section 363 — mandatory within 1 hour for minors)
  → Principal notification

[Student Found — Mark Safe]  [Escalate — Notify Police]

CRITICAL NOTE: For students below 18, any disappearance > 30 minutes
requires police intimation under Juvenile Justice Act guidelines.
```

---

## 5. All-Clear Message

After an emergency is resolved:

```
ALL-CLEAR ALERT

Following the [FIRE EVACUATION] alert sent at 11:42 AM:

Message (pre-written, editable):
  "UPDATE [Greenfields School]: All students are safe. The fire drill /
   incident has been resolved. Students have returned to classes.
   Regular school schedule will resume. Thank you for your patience.
   — Principal, Greenfields School"

[SEND ALL-CLEAR TO ALL PARENTS]
```

---

## 6. Incident Log

Every emergency alert is logged:

```
Emergency Alert Log — 2026–27

Date          Type              Sent By          Recipients  Resolution
27 Mar 2026   Fire Evacuation   Principal (Dr. N) 380         All-clear at 12:05 PM (23 min)
15 Oct 2026   Early Dismissal   Admin Officer     380         School closed at 1 PM (flood warning)
3 Dec 2026    Medical Emergency Principal         2 parents   Student taken to Apollo Hospital; stable
22 Jan 2027   Bus Delay         Admin Officer     45 parents  Bus 4 delayed 45 min; arrived 8:55 AM
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/school/{id}/emergency/send/` | Trigger emergency alert |
| 2 | `POST` | `/api/v1/school/{id}/emergency/send-selective/` | Selective alert (specific students) |
| 3 | `POST` | `/api/v1/school/{id}/emergency/all-clear/` | Send all-clear message |
| 4 | `GET` | `/api/v1/school/{id}/emergency/log/?year={y}` | Incident log |
| 5 | `GET` | `/api/v1/school/{id}/emergency/delivery-status/{alert_id}/` | Real-time delivery progress |

---

## 8. Business Rules

- Emergency alerts bypass all approval workflows — any authorised user (Principal, Admin Officer, S3+) can trigger immediately; post-event review is done in the incident log
- Double-confirm (two-tap) prevents accidental mass sends; but the confirmation screen must be clearable in under 5 seconds to not delay genuine emergencies
- WhatsApp template for emergency alerts is pre-approved by Meta with URGENT category; it bypasses the 24-hour session window restriction
- Missing student alert: if police are notified from within the system, a log entry is created with the timestamp — this is the school's evidence of compliance with mandatory reporting requirements
- All emergency alert records are permanently retained (no deletion) — they may be needed for police investigation, court proceedings, or insurance claims
- Test drills (fire drill, lockdown drill) should be logged as "DRILL" type so they don't create false parent anxiety; drill alerts are sent only to staff (not parents) unless the school specifically wants to inform parents

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
