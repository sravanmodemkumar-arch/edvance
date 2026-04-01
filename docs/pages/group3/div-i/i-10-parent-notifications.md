# I-10 — Parent Transport Notifications

> **URL:** `/school/transport/notifications/`
> **File:** `i-10-parent-notifications.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Transport In-Charge (S3) — configure and send · Administrative Officer (S3) — view log · Parent (via Parent Portal N-09 + WhatsApp) — receive only

---

## 1. Purpose

Proactive communication with parents about transport events. Parents are anxious about child safety on the bus — a timely "bus is delayed by 15 minutes" message prevents panic, avoids dozens of phone calls, and builds trust. Notification triggers:
- **Bus late alerts:** Automatic when GPS shows ETA > configured threshold
- **Route changes:** Advance notice when stops/timings change
- **Bus not operating:** Emergency closure, maintenance day, driver absent
- **Safe arrival confirmation:** "Your child has reached school" — optional but valued
- **Evening pickup reminder:** "Bus leaving school in 10 minutes"
- **Student not on bus:** When escort marks a student absent at their stop

All parent notifications use WhatsApp (F-03 templates) as primary channel; SMS as fallback.

---

## 2. Notification Configuration Panel

```
Parent Transport Notification Settings                [Save Settings]
Academic Year: [2026–27 ▼]

Auto-Alert Thresholds:
  Late alert trigger: Bus delayed by [15] minutes from scheduled stop time
  Morning arrival alert: Send "reached school" confirmation: ● Yes  ○ No
  Evening departure alert: Send "bus leaving school" message: ● Yes  ○ No
    Evening alert lead time: [10] minutes before departure

Notification channels (in priority order):
  1. WhatsApp Business (Meta API via Interakt) — Primary
  2. SMS (Twilio/TRAI-registered) — Fallback if WhatsApp fails
  3. Parent Portal push notification — Supplementary

Auto-triggers enabled:
  ☑ Bus late alert (>15 min delay)
  ☑ Student not at stop (escort marks absent — parent not pre-informed)
  ☑ Bus breakdown alert
  ☑ Route suspension (vehicle in maintenance — no bus today)
  ☑ Emergency: SOS activated on bus
  ☑ Reached school confirmation
  ☑ Evening departure alert
  ☐ Route change (admin triggers manually — 5 days advance)
  ☐ Stop timing change (admin triggers manually — 5 days advance)
```

---

## 3. Notification Types and Templates

### 3.1 Bus Late Alert (Auto-triggered)

```
Trigger: GPS-calculated ETA exceeds scheduled arrival by ≥15 minutes

Template (WhatsApp DLT-approved): TRANSPORT_LATE_ALERT

Message sent to: All parents of students on Route R01

WhatsApp Message:
─────────────────────────────────────────
Dear {Parent Name},

School bus Route R01 (Chaitanyapuri) is running approximately
*{delay_minutes} minutes late* today ({date}).

Current location: {current_location}
Estimated arrival at school: {eta}
Reason: {reason}  [Traffic near Kothapet flyover]

Your child is safe. We will update you if there are further delays.

— GREENFIELDS SCHOOL Transport Team
─────────────────────────────────────────

Sent to: 44 parents (Route R01)
Delivered: 43/44 ✅  ·  1 failed (WhatsApp not active → SMS fallback sent)
Sent at: 7:19 AM (trigger: 13 min delay detected at 7:18 AM)
```

### 3.2 Student Not at Stop (Escort-triggered)

```
Trigger: Escort marks student as "not at stop" and parent has NOT pre-informed

Template: TRANSPORT_STUDENT_ABSENT_STOP

Message sent to: Parent of the specific student only

WhatsApp Message:
─────────────────────────────────────────
Dear {Parent Name},

Your child *{student_name}* was not at their bus stop
({stop_name}) at {stop_time} today.

If your child is unwell or not travelling today, please confirm:
  ✅ [Tap here — Not travelling today]
  🏠 [Tap here — Coming by own arrangement]

If your child was dropped at the stop and you expect them to be there,
please call the school immediately: 040-23456789
Transport In-Charge: +91 9876-XXXXX

— GREENFIELDS SCHOOL Transport
─────────────────────────────────────────

Time sent: 6:47 AM (2 min after scheduled stop time, student not found)
Parent response: ✅ Replied "Not travelling today — unwell" at 6:49 AM
Escort informed in app: ✅ (I-05 attendance updated: "Absent — parent confirmed")
```

### 3.3 Reached School Confirmation

```
Trigger: All buses have arrived at school gate; submitted by escort/Transport In-Charge

Template: TRANSPORT_REACHED_SCHOOL

Message sent to: Parents of all students who were on the bus

WhatsApp Message:
─────────────────────────────────────────
Dear {Parent Name},

{student_name} has safely reached school on Route {route_name}.
Arrival time: {arrival_time}

Have a great day!
— GREENFIELDS SCHOOL
─────────────────────────────────────────

Route R01 arrival: 7:22 AM — 42 parents notified ✅
Route R02 arrival: 7:31 AM — 36 parents notified ✅
Route R04 arrival: 7:18 AM — 51 parents notified ✅
```

### 3.4 Bus Not Operating Today

```
Trigger: Transport In-Charge marks route as suspended for the day

Template: TRANSPORT_BUS_NOT_OPERATING

WhatsApp Message:
─────────────────────────────────────────
Dear {Parent Name},

*Important: Route R03 bus is NOT operating today ({date}).*

Reason: {reason}  [Vehicle sent for scheduled maintenance]

Please make alternate transport arrangements for your child today.

We apologise for the inconvenience.
Transport helpline: 040-23456789 (available 6:30 AM – 8:00 AM)

— GREENFIELDS SCHOOL Transport
─────────────────────────────────────────

Sent to: 30 Route R03 parents  ·  Sent at: 5:50 AM (early morning)
Note: Early morning sends (before 8 AM) are permitted for operational alerts
  (TRAI DLT exception for transactional/service messages — not promotional)
```

### 3.5 Evening Departure Alert

```
Trigger: 10 minutes before evening departure (auto, configurable)

Template: TRANSPORT_EVENING_DEPARTURE

WhatsApp Message:
─────────────────────────────────────────
Dear {Parent Name},

Route R01 school bus is leaving school in approximately *10 minutes*
(departure time: {departure_time}).

Your child {student_name} will be dropped at: *{stop_name}*
Estimated drop time: {drop_eta}

Please ensure someone is available to receive your child at the stop.

— GREENFIELDS SCHOOL Transport
─────────────────────────────────────────

Sent at: 4:00 PM (for 4:10 PM departure)
```

### 3.6 Route Change Advance Notice

```
Trigger: Manual by Transport In-Charge — 5 days before change effective

Template: TRANSPORT_ROUTE_CHANGE_NOTICE

WhatsApp Message:
─────────────────────────────────────────
Dear {Parent Name},

Please note that Route R01 will have a *stop timing change* effective
*{effective_date}*.

Change: Stop at Kothapet Bus Stop timing changes from 6:55 AM to 7:00 AM.

Reason: Traffic congestion analysis — adjusted for smoother route.

No other changes. Your child's stop remains the same.
If you have questions: 040-23456789

— GREENFIELDS SCHOOL Transport
─────────────────────────────────────────
```

---

## 4. Notification Log

```
Transport Notification Log — 27 March 2026

Time    Route  Type                         Recipients  Delivered  Failed
6:47 AM  R01   Student not at stop (Meena V.) 1 parent   1 ✅       0
6:52 AM  R01   Student not at stop (Vijay S.)  1 parent   1 ✅       0
7:19 AM  R01   Bus late alert (13 min)        44 parents  43 ✅      1 → SMS sent
7:22 AM  R01   Reached school               42 parents  42 ✅       0
7:08 AM  R05   Reached school               32 parents  32 ✅       0
4:00 PM  R01   Evening departure (10 min)    42 parents  42 ✅       0
5:03 PM  R01   Last student dropped (Arjun)  42 parents  42 ✅       0

Total today: 7 notification batches  ·  245 individual messages  ·  244 delivered ✅

[Export log]  [View failed messages]  [Retry failed deliveries]
```

---

## 5. Manual Transport Alert (Transport In-Charge)

```
Send Manual Transport Alert

Routes: ☑ R01  ☑ R02  ☑ R03  ☑ R04  ☑ R05  (select all or specific)

Alert type:
  ● Emergency (bus breakdown / accident)
  ○ Delay (manual override of auto-delay)
  ○ Route change
  ○ Operational update

Message:
  [Route R04 bus has experienced a tyre puncture near Vanasthalipuram.
   A backup bus has been dispatched. Your child is safe. Expected delay: 25 minutes.
   No need to call — we will send an update when students board the backup bus.]

Send via: ☑ WhatsApp  ☐ SMS  ☑ Parent portal push

Preview:
  Recipients: 51 R04 parents

[Send Now]  [Schedule for 5 min]
```

---

## 6. Opt-Out Management

```
Transport Notification Opt-Out Register

DPDPA 2023 compliance: Parents may opt out of non-safety notifications.
Safety alerts (student not at stop, SOS, accident) CANNOT be opted out — these are
operational safety communications, not marketing.

Category            Opt-out allowed  Parents opted out
─────────────────────────────────────────────────────
Reached school      ✅ Yes           12 parents (don't need this)
Evening departure   ✅ Yes           8 parents
Route change        ✅ Yes           0 parents
Bus late alert      ❌ No (safety)   —
Student not at stop ❌ No (safety)   —
SOS/Emergency       ❌ No (safety)   —
Bus not operating   ❌ No (operational) —

Parent to opt out: Parent Portal → Settings → Transport Notifications → preferences
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/transport/notifications/settings/` | Notification configuration |
| 2 | `PATCH` | `/api/v1/school/{id}/transport/notifications/settings/` | Update thresholds/channels |
| 3 | `POST` | `/api/v1/school/{id}/transport/notifications/send/` | Manual alert send |
| 4 | `GET` | `/api/v1/school/{id}/transport/notifications/log/?date={date}` | Notification log |
| 5 | `POST` | `/api/v1/school/{id}/transport/notifications/trigger/{type}/` | Auto-trigger specific notification |
| 6 | `GET` | `/api/v1/school/{id}/transport/notifications/opt-out/` | Parent opt-out list |
| 7 | `PATCH` | `/api/v1/school/{id}/transport/notifications/opt-out/{parent_id}/` | Update opt-out preferences |

---

## 8. Business Rules

- Safety transport alerts (student not at stop, SOS, bus breakdown) are sent immediately without a human approval step — every minute matters when a child is unaccounted for
- Late alerts are auto-triggered by GPS (I-06); threshold is configurable but default is 15 minutes — below that, the delay resolves before parents start calling
- "Reached school" confirmation is sent only when all students on the route have boarded at school gate and been confirmed by the escort — not when the bus merely enters the campus
- All WhatsApp transport templates require DLT registration under UTILITY category (parent has opted in to school communications via enrollment agreement); MARKETING category is not used for safety/operational messages
- Evening departure alert timing is adjustable (10, 15, 20 min) — schools near urban traffic find 15 min gives parents enough time to reach the drop stop
- If both WhatsApp and SMS fail for a parent: the parent portal push notification is sent; if that also fails, a manual call-back list is generated for the Transport In-Charge
- DPDPA: delivery receipts (message delivered/read timestamps) are stored for 180 days — this log is evidence that the school notified parents in a timely manner in case of dispute
- Parents cannot disable safety-category transport alerts; this is a condition of using school transport (stated in transport enrollment agreement I-03)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
