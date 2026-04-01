# N-01 — Parent Home Dashboard

> **URL:** `/parent/dashboard/`
> **File:** `n-01-parent-dashboard.md`
> **Template:** `parent_portal.html` (Flutter app primary; web fallback)
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P) — own child(ren) only

---

## 1. Purpose

The Parent Dashboard is the first screen a parent sees after login. It is designed for a 60-second daily check — "Is my child okay? Is there anything I need to do today?" It surfaces the most relevant information first and provides navigation to all other parent functions.

Multi-child support: Parents with multiple children at the school see a child selector at the top; tapping a child switches the entire dashboard context to that child.

---

## 2. Dashboard Layout

```
PARENT DASHBOARD — Mrs. Sunita Rao
Logged in as parent of: [● Rahul (Class X-A)] | [Priya (Class VII-C)]

┌─────────────── RAHUL — TODAY ──────────────────────────────────────────────┐
│  Class X-A  |  Roll No. 14  |  Class Teacher: Mr. Deepak C.               │
│                                                                             │
│  TODAY (27 March 2026, Friday):                                             │
│  ✅ Present (marked 8:02 AM)                                               │
│                                                                             │
│  🔔 NOTIFICATIONS (2 new):                                                 │
│    📚 Homework: Mathematics — Chapter 12 Ex 12.3 (due Monday)             │
│    📋 Report card available: Unit Test 1 — [View →]                       │
│                                                                             │
│  UPCOMING:                                                                  │
│    Tue 31 Mar: Term 3 fee due — ₹8,400 outstanding [Pay →]                │
│    Mon 6 Apr: PTM — Class X (book slot → [Book →])                        │
│    Sat 5 Apr: Annual Day rehearsal (2–4 PM)                                │
└─────────────────────────────────────────────────────────────────────────────┘

QUICK ACCESS:
  [Attendance] [Marks] [Fee] [Diary] [Bus] [PTM] [Leave] [Calendar] [Grievance]

─────────────────────────────────────────────────────────────────────────────
THIS MONTH SNAPSHOT:
  Attendance (March): 20/23 school days attended (87.0%)
  Last test (Unit Test 1): Overall 74.2% — [View subject breakdown →]
  Fee: ₹8,400 due by 31 March — [Pay now →]
  Bus: Route 3 — 7:42 AM pick-up today ✅
─────────────────────────────────────────────────────────────────────────────

RECENT ACTIVITY:
  24 Mar  Diary: Science project submission reminder (Mr. Ravi K.)
  22 Mar  Attendance: Absent (Saturday — school closed)
  20 Mar  Fee: ₹42,000 paid (Term 2 + 3 advance) — Receipt #RCP-2026-1842
  15 Mar  Report card released: Half-Yearly — [Download PDF]
```

---

## 3. Multi-Child Toggle

```
CHILD SELECTOR (top navigation)

  ● Rahul Rao — Class X-A  |  Roll No. 14
    Pending: 1 fee, 1 PTM booking
  ○ Priya Rao — Class VII-C  |  Roll No. 24
    Pending: 0 items — All good ✅

Tap to switch child → entire dashboard refreshes for selected child
```

---

## 4. Notification Centre

```
NOTIFICATIONS — Rahul Rao (last 7 days)

  27 Mar  📋 Unit Test 1 report card available [View]
  27 Mar  📚 Homework: Mathematics Ex 12.3 (deadline: 30 Mar)
  26 Mar  🚌 Bus delayed 12 minutes — Route 3 (traffic near Dilsukhnagar) [Resolved ✅]
  25 Mar  💰 Fee reminder: ₹8,400 due 31 March
  22 Mar  📢 School: Annual Day rehearsal — Sat 5 April, 2–4 PM
  20 Mar  ✅ Payment confirmed: ₹42,000 received
  18 Mar  📋 Homework: Social Science — Map work Chapter 6

Notification preferences [Manage →]:
  ✅ Attendance alerts (absence / late arrival)
  ✅ Fee reminders
  ✅ Report card releases
  ✅ Homework / diary messages
  ✅ Bus delays (>10 minutes)
  ☐ General school announcements (opt-in, currently off)
  ✅ Safety alerts (non-opt-outable — DPDPA legitimate interest)

[View all notifications →]  [Mark all read]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/parent/{parent_id}/dashboard/` | Parent dashboard (auto-selects primary child) |
| 2 | `GET` | `/api/v1/parent/{parent_id}/children/` | List of linked children |
| 3 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/dashboard/` | Dashboard for specific child |
| 4 | `GET` | `/api/v1/parent/{parent_id}/notifications/` | All notifications |
| 5 | `PATCH` | `/api/v1/parent/{parent_id}/notifications/preferences/` | Update notification preferences |
| 6 | `POST` | `/api/v1/parent/{parent_id}/notifications/{n_id}/read/` | Mark notification read |

---

## 6. Business Rules

- Parent can only see data for children linked to their account; sibling linking is done by the school (HR/Admissions module) during admission; a parent cannot self-link additional children — they must request the school to verify and link
- Safety alerts (accident, SOS, school emergency) are non-opt-outable under DPDPA legitimate interest exception; all other notifications respect the parent's preference settings
- A parent login is distinct from a student login; both may access the same data (attendance, marks) but from different views; a student login has additional features (assignments, peer interaction) while a parent login has fee payment and leave application
- For multi-child parents, the notification count on the child selector tab shows pending actions so parents don't miss an action for a less-checked child
- Session duration: Parent sessions expire after 24 hours of inactivity; sensitive actions (fee payment, consent) require re-authentication (OTP to registered mobile) regardless of session state

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
