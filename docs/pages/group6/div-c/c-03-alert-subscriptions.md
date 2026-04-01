# C-03 — Alert Subscriptions & Preferences

> **URL:** `/exam/alerts/` (user settings)
> **File:** `c-03-alert-subscriptions.md`
> **Priority:** P1
> **Data:** `notification_subscription` + `user_alert_preference`

---

## 1. Subscription Management

```
MY ALERT SUBSCRIPTIONS — Ravi Kumar
Manage what notifications you receive and how

  EXAM-LEVEL SUBSCRIPTIONS  [from notification_subscription WHERE user_id]
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Exam / Body                │ Events Subscribed        │ Actions     │
  ├─────────────────────────────┼──────────────────────────┼─────────────┤
  │  APPSC Group 2 2025         │ All events ✅            │ [Edit] [✕]  │
  │  SSC CGL 2026               │ All events ✅            │ [Edit] [✕]  │
  │  TS Police Constable 2025   │ Result + Admit Card only │ [Edit] [✕]  │
  │  All APPSC exams (body)     │ Notifications only       │ [Edit] [✕]  │
  │  All TSPSC exams (body)     │ Notifications only       │ [Edit] [✕]  │
  ├─────────────────────────────┴──────────────────────────┴─────────────┤
  │  [+ Subscribe to a new exam]   [+ Subscribe to a conducting body]    │
  └──────────────────────────────────────────────────────────────────────┘

  DELIVERY CHANNELS:
    (●) Push notification (app):   ✅ Enabled — Primary
    (●) WhatsApp (+91-9876XXXXX):  ✅ Enabled
    (○) Email (ravi@email.com):    ✅ Enabled (receipts + important only)
    (○) SMS (+91-9876XXXXX):       ❌ Disabled (user preference)

  ALERT FREQUENCY:
    Application deadlines:     D-7, D-3, D-1 reminders ✅ (cannot disable)
    Notification released:     Immediate ✅
    Result declared:           Immediate ✅
    Admit card available:      Immediate ✅
    Exam schedule change:      Immediate ✅
    Weekly exam digest:        Every Monday 8 AM ✅ (new notifications summary)
    Do Not Disturb:            10 PM – 7 AM (no push/WA during this time)

  LANGUAGE PREFERENCE:
    Alerts in: (●) Telugu  (○) English  (○) Hindi
```

---

## 2. Subscription Data Model

```
notification_subscription {
  id,
  user_id,
  exam_id (nullable),              ← specific exam subscription
  conducting_body_id (nullable),   ← body-level subscription (all exams under this body)
  event_types[],                   ← ["all"] or ["result", "admit_card"] etc.
  active,
}

user_alert_preference {
  user_id,
  channels: { push: true, whatsapp: true, email: true, sms: false },
  language,
  dnd_start, dnd_end,             ← Do Not Disturb window
  digest_enabled,                 ← weekly summary email
  digest_day,                     ← "monday"
}
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/alerts/subscriptions/` | User's active subscriptions |
| 2 | `POST` | `/api/v1/exam/alerts/subscriptions/` | Subscribe to exam or body |
| 3 | `PATCH` | `/api/v1/exam/alerts/subscriptions/{sid}/` | Update event types |
| 4 | `DELETE` | `/api/v1/exam/alerts/subscriptions/{sid}/` | Unsubscribe |
| 5 | `GET` | `/api/v1/exam/alerts/preferences/` | Channel and frequency preferences |
| 6 | `PATCH` | `/api/v1/exam/alerts/preferences/` | Update channel/frequency prefs |

---

## 5. Business Rules

- Application deadline reminders (D-7, D-3, D-1) are non-disableable for subscribed exams; an aspirant who subscribes to SSC CGL alerts implicitly agrees to receive deadline reminders; a missed application deadline is irreversible — no amount of "I didn't want too many notifications" justifies letting a subscribed user miss a 3-year-wait deadline; other event types (notification released, result declared) can be individually toggled off
- WhatsApp alerts require DPDPA-compliant opt-in; the subscription page explicitly states "I agree to receive exam alerts on WhatsApp" with a separate checkbox; pre-checked boxes are non-compliant; opt-out is immediate — the system stops sending within 24 hours of opt-out; WhatsApp delivery uses Meta Business API templates (pre-approved); a template for "Application deadline reminder" is different from "Result declared" — each event type has its own approved template
- Do Not Disturb (DND) window (10 PM – 7 AM default) suppresses push notifications and WhatsApp messages during sleeping hours; alerts generated during DND are queued and delivered at DND end (7 AM); however, a "Breaking: Exam cancelled / rescheduled" alert overrides DND because the urgency justifies the interruption; the system classifies alerts as `critical` (overrides DND) or `normal` (respects DND); only content team-flagged alerts are marked critical
- Body-level subscriptions (e.g., "All APPSC exams") are powerful for aspirants who take multiple exams from the same body; when APPSC releases a new exam notification (e.g., APPSC AEE 2026), all users subscribed to "All APPSC exams" receive the alert even though they never explicitly subscribed to that specific exam; this discovery mechanism helps aspirants learn about exams they are eligible for but weren't aware of; body subscriptions are merged with exam-level subscriptions — a user subscribed to both "APPSC Group 2" (specific) and "All APPSC" (body) does not receive duplicate alerts
- Telugu-language alerts are generated from notification templates that have bilingual versions; the alert says "APPSC Group 2 2025 — ఫలితాలు ప్రకటించబడ్డాయి" (Results declared) for Telugu-preference users and "APPSC Group 2 2025 — Results declared" for English-preference users; the core data (exam name, dates, vacancy counts) is the same — only the template text changes; the content team maintains bilingual templates for Telugu, English, and Hindi; new language support requires adding templates in that language

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division C*
