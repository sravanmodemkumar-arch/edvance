# A-04 — Settings & Preferences

> **URL:** `/student/settings`
> **File:** `a-04-settings-preferences.md`
> **Priority:** P2
> **Roles:** Student (S2–S6) · Parent (limited settings for minor's account)

---

## Overview

Central settings page for students to customise their EduForge experience — notification preferences, language, dark mode, exam domain ordering, accessibility features, session management, and account actions. The settings adapt dynamically based on access level: S2 students (Class 9–10) see limited settings, S4+ students see full settings including privacy controls. Working professionals see a "Commute Mode" toggle. Special-needs students see accessibility options prominently.

---

## 1. Settings Page Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  SETTINGS                                                                    │
│                                                                              │
│  ┌────────────────────┐  ┌────────────────────────────────────────────────┐ │
│  │                     │  │                                                │ │
│  │  General         ● │  │  GENERAL SETTINGS                              │ │
│  │  Notifications     │  │                                                │ │
│  │  Display & Theme   │  │  Preferred Language                            │ │
│  │  Exam Preferences  │  │  [ Telugu ▼ ]                                  │ │
│  │  Accessibility     │  │  App language + content language where avail.  │ │
│  │  Sessions          │  │                                                │ │
│  │  Privacy       [S4]│  │  Default Exam Domain                          │ │
│  │  Account           │  │  [ SSC CGL ▼ ]                                │ │
│  │                     │  │  Dashboard opens to this domain by default    │ │
│  │                     │  │                                                │ │
│  │                     │  │  Domain Display Order (drag to reorder)       │ │
│  │                     │  │  1. ≡ SSC CGL                                 │ │
│  │                     │  │  2. ≡ IBPS Clerk                              │ │
│  │                     │  │  3. ≡ APPSC Group 2                           │ │
│  │                     │  │                                                │ │
│  │                     │  │  Time Zone                                    │ │
│  │                     │  │  [ IST (UTC+5:30) ▼ ]                        │ │
│  │                     │  │  (NRI students: select your local time zone)  │ │
│  │                     │  │                                                │ │
│  └────────────────────┘  └────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Notification Preferences

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  NOTIFICATION PREFERENCES                                                    │
│                                                                              │
│  ┌────────────────────────────┬──────┬──────────┬──────────┬─────────────┐  │
│  │ Notification Type          │ Push │ WhatsApp │ SMS      │ Email       │  │
│  ├────────────────────────────┼──────┼──────────┼──────────┼─────────────┤  │
│  │ Test reminders (1hr before)│ [x]  │ [x]      │ [ ]      │ [ ]         │  │
│  │ Test results published     │ [x]  │ [x]      │ [x]      │ [x]         │  │
│  │ Rank updates               │ [x]  │ [ ]      │ [ ]      │ [ ]         │  │
│  │ Fee due reminders          │ [x]  │ [x]      │ [x]      │ [x]         │  │
│  │ AI study plan (daily)      │ [x]  │ [ ]      │ [ ]      │ [ ]         │  │
│  │ Current affairs (daily)    │ [x]  │ [x]      │ [ ]      │ [ ]         │  │
│  │ New notes/videos added     │ [x]  │ [ ]      │ [ ]      │ [x]         │  │
│  │ Institution announcements  │ [x]  │ [x]      │ [ ]      │ [x]         │  │
│  │ Doubt responses            │ [x]  │ [x]      │ [ ]      │ [ ]         │  │
│  │ Streak & motivation        │ [x]  │ [ ]      │ [ ]      │ [ ]         │  │
│  │ Promotional / offers       │ [ ]  │ [ ]      │ [ ]      │ [x]         │  │
│  └────────────────────────────┴──────┴──────────┴──────────┴─────────────┘  │
│                                                                              │
│  Quiet hours:  [ 10:00 PM ] to [ 6:00 AM ]  (no push/WhatsApp)             │
│  During exams: Auto-mute all non-critical notifications                     │
│                                                                              │
│  [Save Preferences]                                                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Display & Theme

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  DISPLAY & THEME                                                             │
│                                                                              │
│  Theme:         (o) Light  ( ) Dark  ( ) System default                     │
│                                                                              │
│  Font Size:     [A-] ──────●────── [A+]    Current: Medium                  │
│                 Small · Medium · Large · Extra Large                         │
│                                                                              │
│  Commute Mode:  [ OFF ─── toggle ─── ON ]                                   │
│                 Larger text, offline-first, 10-question practice sets.       │
│                 Auto-enables on mobile when moving > 15 km/h.               │
│                 (shown only for working professionals / S4+ with mobile)     │
│                                                                              │
│  Compact View:  [ OFF ─── toggle ─── ON ]                                   │
│                 Condenses dashboard cards for faster scanning.               │
│                                                                              │
│  Show Streak:   [ ON ─── toggle ─── OFF ]                                   │
│                 Display daily study streak on dashboard.                     │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Accessibility Settings

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ACCESSIBILITY                                                               │
│                                                                              │
│  Screen Reader Support:   [ ON ─── toggle ─── OFF ]                         │
│                           ARIA labels on all interactive elements.           │
│                                                                              │
│  High Contrast Mode:      [ OFF ─── toggle ─── ON ]                        │
│                           Black/white with high contrast colours.            │
│                                                                              │
│  Reduced Motion:          [ OFF ─── toggle ─── ON ]                        │
│                           Disables animations and transitions.               │
│                                                                              │
│  Dyslexia-Friendly Font:  [ OFF ─── toggle ─── ON ]                        │
│                           Uses OpenDyslexic typeface across all content.     │
│                                                                              │
│  Extra Time in Tests:     [ OFF ─── toggle ─── ON ]                        │
│                           Adds 33% extra time to all mock tests.            │
│                           ⚠️ Requires institution/admin approval.            │
│                           Currently: Not approved  [Request →]              │
│                                                                              │
│  Keyboard Navigation:     [ ON ─── toggle ─── OFF ]                        │
│                           Tab through all elements, Enter to select.        │
│                                                                              │
│  Text-to-Speech (Notes):  [ OFF ─── toggle ─── ON ]                        │
│                           Read notes aloud using device TTS engine.          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Session Management

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ACTIVE SESSIONS                                                             │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  📱 Samsung Galaxy M32 (Android 14)               THIS DEVICE        │  │
│  │     Hyderabad, Telangana · Last active: now                           │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  💻 Chrome on Windows 11                                              │  │
│  │     Hyderabad, Telangana · Last active: 2 hours ago                  │  │
│  │     [Logout this device]                                              │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Max concurrent sessions: 3 (Free) / 5 (Premium)                           │
│  [Logout all other devices]                                                  │
│                                                                              │
│  ── LOGIN HISTORY ───────────────────────────────────────────────────────   │
│  31-Mar-2026 08:42 AM  Samsung Galaxy M32  Hyderabad  ✅                    │
│  30-Mar-2026 10:15 PM  Chrome Windows      Hyderabad  ✅                    │
│  30-Mar-2026 06:30 PM  Samsung Galaxy M32  Hyderabad  ✅                    │
│  29-Mar-2026 11:00 AM  Unknown device       Mumbai    ⚠️ [Not you? →]      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Account Actions

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ACCOUNT ACTIONS                                                             │
│                                                                              │
│  Change Mobile Number                                                        │
│  Current: +91 98765-43210                                                   │
│  [Change →]  (requires OTP on both old and new numbers)                     │
│                                                                              │
│  Change Email                                                                │
│  Current: ravi.kumar2007@gmail.com                                          │
│  [Change →]                                                                  │
│                                                                              │
│  Export My Data                                                              │
│  Download all your data: profile, test results, analytics, notes.           │
│  Format: JSON + PDF summary · Delivered to email within 24 hours.           │
│  [Request Data Export →]                                                     │
│                                                                              │
│  ── DANGER ZONE ─────────────────────────────────────────────────────────   │
│                                                                              │
│  Deactivate Account                                                          │
│  Temporarily hide your profile. You can reactivate by logging in.           │
│  Institution links and subscriptions are paused.                            │
│  [Deactivate →]                                                              │
│                                                                              │
│  Delete Account Permanently (DPDP Act 2023)                                 │
│  ⚠️ This permanently deletes ALL your data — test history, analytics,       │
│  certificates, institution links. This cannot be undone.                    │
│  Processing time: 30 days. Active subscriptions refunded pro-rata.          │
│  [Request Deletion →]  (requires OTP confirmation)                          │
│                                                                              │
│  ── MINOR ACCOUNTS ──────────────────────────────────────────────────────   │
│  (shown only for S2/S3 — under 18)                                          │
│  Account deletion for minors requires parent/guardian approval.             │
│  Your parent (Mrs. Lakshmi Devi) will receive an approval request.          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/student/settings` | All settings (general, notifications, display, accessibility) |
| 2 | `PUT` | `/api/v1/student/settings` | Update settings (partial update supported) |
| 3 | `GET` | `/api/v1/student/sessions` | List all active sessions |
| 4 | `DELETE` | `/api/v1/student/sessions/{id}` | Logout a specific session |
| 5 | `DELETE` | `/api/v1/student/sessions/all` | Logout all sessions except current |
| 6 | `POST` | `/api/v1/student/change-mobile/send-otp` | Send OTP to old mobile for change verification |
| 7 | `POST` | `/api/v1/student/change-mobile/verify` | Verify old + new OTP and update mobile |
| 8 | `POST` | `/api/v1/student/data-export` | Request full data export (async, emailed) |
| 9 | `POST` | `/api/v1/student/deactivate` | Deactivate account (requires OTP) |
| 10 | `POST` | `/api/v1/student/delete` | Request permanent deletion (DPDP Act) |

---

## 8. Business Rules

- Notification preferences default to "essential only" for new registrations — test results and fee reminders are ON, promotional notifications are OFF; the system respects quiet hours by queuing non-critical notifications and delivering them at the start of the next active window; WhatsApp is the primary notification channel for Indian students (82% open rate vs 12% for email) and uses the Meta Business API with approved templates; SMS is reserved for critical alerts (exam in 1 hour, fee overdue) and OTP because WhatsApp delivery can be unreliable in areas with poor data connectivity.

- Dark mode is not just a theme toggle — it changes the test-taking interface (white text on dark background with reduced eye strain), adjusts chart colours for readability, and switches the PDF viewer to sepia mode; 34% of students study between 10 PM and 2 AM, making dark mode a genuine usability feature rather than a cosmetic preference; the "System default" option follows the device OS setting and is the recommended choice for students who study both day and night.

- Accessibility features comply with WCAG 2.1 AA standards; the extra-time accommodation for tests requires a formal request with supporting documentation (disability certificate from a registered medical practitioner or institution recommendation); the institution admin or EduForge support team approves the request and the 33% extra time is applied automatically to all timed assessments — this matches the standard accommodation provided by Indian exam bodies (UPSC, SSC, IBPS) for PwBD candidates.

- Account deletion under DPDP Act 2023 triggers a 30-day processing window: during the first 14 days, the student can cancel the deletion request by logging in; after 14 days, all personal data is anonymised in analytics (test attempts become anonymous data points contributing to question difficulty calibration) and personal identifiers are permanently erased from all databases; institution-linked academic records (marks, attendance) are retained by the institution per education record-keeping requirements but the student's personal profile is de-linked; active subscriptions are refunded pro-rata to the original payment method.

- Session management enforces device limits to prevent credential sharing at scale — a Free account allows 3 concurrent sessions and a Premium account allows 5; if a student exceeds the limit, the oldest session is force-logged-out with a push notification ("You were logged out on Samsung Galaxy M32 because you logged in on a new device"); this balances security (preventing one Premium account being shared by a hostel room of 8 students) with genuine multi-device usage (phone + laptop + tablet).

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division A*
