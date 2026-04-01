# A-04 — Parent Profile & Preferences

> **URL:** `/parent/profile`
> **File:** `a-04-parent-profile.md`
> **Priority:** P2
> **Roles:** Parent · Guardian

---

## 1. Parent Profile Page

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  EduForge Parents Portal > My Profile                                        │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │   ── Personal Information ────────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   Full Name:            Mrs. Lakshmi Devi                    [Edit]   │  │
│  │   Relationship:         Mother                                        │  │
│  │   Mobile (Primary):     +91-98765-43210        [Verified]             │  │
│  │   Mobile (Secondary):   +91-90123-45678        [Add / Edit]           │  │
│  │   Email:                lakshmi.devi@gmail.com  [Not verified]        │  │
│  │                                                  [Verify now ->]      │  │
│  │   City:                 Vijayawada                                    │  │
│  │   State:                Andhra Pradesh                                │  │
│  │   PIN Code:             520010                                        │  │
│  │                                                                        │  │
│  │   ── Identity Verification ───────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   Aadhaar:              XXXX-XXXX-4832          [Verified]            │  │
│  │   Verification Date:    31-Mar-2026                                   │  │
│  │   Status:               Verified Parent Badge Active                  │  │
│  │                                                                        │  │
│  │   ── Family Account ──────────────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   Family Account ID:    FAM-AP-2026-08421                             │  │
│  │   Account Created:      31-Mar-2026                                   │  │
│  │   Children Linked:      3 (across 3 institutions)                     │  │
│  │   Account Status:       Active                                        │  │
│  │                                                                        │  │
│  │   ── Secondary Guardian (Optional) ───────────────────────────────     │  │
│  │                                                                        │  │
│  │   Name:                 Mr. Suresh Kumar (Father)     [Add / Edit]    │  │
│  │   Mobile:               +91-87654-32109               [Not linked]    │  │
│  │   Note: Secondary guardian can view the dashboard but cannot           │  │
│  │   modify profile or unlink children without primary parent approval   │  │
│  │                                                                        │  │
│  │            [ Save Changes ]         [ Download My Data (DPDP Act) ]   │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Notification Preferences

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  EduForge Parents Portal > My Profile > Notification Preferences             │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │   ── Notification Channels ───────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   Channel          Status        Priority                              │  │
│  │   ──────────────── ──────────── ──────────                             │  │
│  │   SMS              Enabled       Primary     +91-98765-43210           │  │
│  │   WhatsApp         Enabled       Secondary   +91-98765-43210           │  │
│  │   Push (App)       Enabled       Tertiary    EduForge Parent App      │  │
│  │   Email            Disabled      —           lakshmi.devi@gmail.com   │  │
│  │                                               (not verified)           │  │
│  │                                                                        │  │
│  │   [ Reorder Priority ]   Drag to set fallback order                   │  │
│  │                                                                        │  │
│  │   ── Notification Types ──────────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   Type                        SMS   WhatsApp  Push   Email             │  │
│  │   ────────────────────────── ───── ──────── ──────  ─────             │  │
│  │   Attendance (absent)         [x]    [x]     [x]    [ ]               │  │
│  │   Attendance (daily summary)  [ ]    [x]     [ ]    [ ]               │  │
│  │   Exam results published      [x]    [x]     [x]    [ ]               │  │
│  │   Fee due reminders           [x]    [x]     [x]    [ ]               │  │
│  │   Fee payment confirmation    [x]    [ ]     [x]    [ ]               │  │
│  │   PTM / event invitations     [x]    [x]     [x]    [ ]               │  │
│  │   Teacher messages            [ ]    [x]     [x]    [ ]               │  │
│  │   Report card available       [x]    [x]     [x]    [ ]               │  │
│  │   Disciplinary notices        [x]    [x]     [x]    [ ]               │  │
│  │   Mock test reminders         [ ]    [x]     [x]    [ ]               │  │
│  │   (coaching only)                                                      │  │
│  │                                                                        │  │
│  │   ── Per-Child Override ──────────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   [x] Apply same settings to all children                             │  │
│  │   [ ] Customise per child:                                             │  │
│  │       Ravi (GCEH):         [Use defaults]                             │  │
│  │       Priya (Sri Chaitanya): [Use defaults]                           │  │
│  │       Ravi (TopRank):      [Only mock test alerts]                    │  │
│  │                                                                        │  │
│  │   ── Quiet Hours ─────────────────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   Enable quiet hours:    [x] Yes                                      │  │
│  │   Quiet window:          [ 21:00 ] to [ 07:00 ]                      │  │
│  │   Exceptions:            [x] Fee payment failures bypass quiet hours  │  │
│  │                          [x] Disciplinary notices bypass quiet hours   │  │
│  │                          [ ] Attendance alerts bypass quiet hours      │  │
│  │                                                                        │  │
│  │            [ Save Notification Preferences ]                          │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Language & Accessibility Settings

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  EduForge Parents Portal > My Profile > Language & Accessibility             │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │   ── Portal Language ─────────────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   Current Language:     Telugu                                        │  │
│  │                                                                        │  │
│  │   Available Languages (based on your state: Andhra Pradesh):          │  │
│  │   (o) Telugu          ( ) English         ( ) Hindi                   │  │
│  │   ( ) Tamil           ( ) Kannada         ( ) Urdu                    │  │
│  │                                                                        │  │
│  │   Note: Changing the portal language takes effect immediately.         │  │
│  │   SMS/WhatsApp templates update within 24 hours.                      │  │
│  │                                                                        │  │
│  │   ── Notification Language ───────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   SMS Language:         [ Telugu ▼ ]                                   │  │
│  │   WhatsApp Language:    [ Telugu ▼ ]                                   │  │
│  │   Push Notifications:   [ Telugu ▼ ]                                   │  │
│  │                                                                        │  │
│  │   Preview (Telugu SMS for attendance alert):                          │  │
│  │   ┌──────────────────────────────────────────────────────────────┐    │  │
│  │   │ "EduForge: mee abbayi Priya Kumar eeroju Sri Chaitanya lo   │    │  │
│  │   │  absent ga gurtinchaaaru. — EduForge Parents"               │    │  │
│  │   └──────────────────────────────────────────────────────────────┘    │  │
│  │                                                                        │  │
│  │   ── Accessibility ───────────────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   Text Size:           [ Medium ▼ ]  (Small / Medium / Large / XL)   │  │
│  │   High Contrast Mode:  [ ] Enable                                     │  │
│  │   Screen Reader Mode:  [ ] Enable (optimises for NVDA / TalkBack)    │  │
│  │   Reduce Animations:   [x] Enabled                                   │  │
│  │                                                                        │  │
│  │   ── Linked Accounts ─────────────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   Google:              Not linked       [ Link Google Account ]       │  │
│  │   DigiLocker:          Linked           [ Manage ]                    │  │
│  │                        (for accessing Aadhaar, marksheets)            │  │
│  │   UPI (for fee pay):   Not linked       [ Link UPI ID ]              │  │
│  │                                                                        │  │
│  │   ── Account Actions ─────────────────────────────────────────────     │  │
│  │                                                                        │  │
│  │   [ Change Mobile Number ]   (requires OTP on both old and new)      │  │
│  │   [ Deactivate Account ]     (children will be unlinked; 30-day      │  │
│  │                                recovery window)                       │  │
│  │   [ Download All My Data ]   (DPDP Act 2023 compliance — ZIP file    │  │
│  │                                with all data, ready in 48 hours)      │  │
│  │   [ Delete Account ]         (permanent; requires Aadhaar re-verify  │  │
│  │                                or OTP + 14-day cooling period)        │  │
│  │                                                                        │  │
│  │            [ Save Settings ]                                          │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/parent/profile` | Retrieve full parent profile including personal info, verification status, family account |
| 2 | `PUT` | `/api/v1/parent/profile` | Update parent profile fields (name, city, PIN, secondary mobile, secondary guardian) |
| 3 | `GET` | `/api/v1/parent/preferences/notifications` | Retrieve notification preferences — channels, types, per-child overrides, quiet hours |
| 4 | `PUT` | `/api/v1/parent/preferences/notifications` | Update notification preferences with channel-type matrix and quiet hours config |
| 5 | `PUT` | `/api/v1/parent/preferences/language` | Update portal language and per-channel notification language |
| 6 | `PUT` | `/api/v1/parent/preferences/accessibility` | Update accessibility settings (text size, contrast, screen reader, animations) |
| 7 | `POST` | `/api/v1/parent/profile/change-mobile` | Initiate mobile number change; sends OTP to both old and new numbers |
| 8 | `POST` | `/api/v1/parent/profile/change-mobile/verify` | Verify OTPs from both old and new numbers to complete mobile number change |
| 9 | `POST` | `/api/v1/parent/account/deactivate` | Deactivate account; triggers 30-day recovery window; unlinks children |
| 10 | `POST` | `/api/v1/parent/account/delete` | Initiate permanent deletion; requires re-verification; 14-day cooling period |
| 11 | `GET` | `/api/v1/parent/account/data-export` | Request DPDP Act data export; returns job ID; ZIP ready within 48 hours |
| 12 | `GET` | `/api/v1/parent/account/data-export/{job_id}` | Check data export status and download link when ready |
| 13 | `POST` | `/api/v1/parent/linked-accounts/google` | Link Google account via OAuth2 for single sign-on |
| 14 | `POST` | `/api/v1/parent/linked-accounts/digilocker` | Link DigiLocker account for document access (Aadhaar, marksheets) |

---

## 5. Business Rules

- **BR-01 — Mobile Number Change Requires Dual OTP Verification:** When a parent requests to change their primary mobile number, the system sends a 6-digit OTP to both the existing number and the new number simultaneously. Both OTPs must be entered correctly within a 5-minute window for the change to take effect. This dual-verification approach prevents account takeover scenarios where an attacker who gains temporary access to the parent's session tries to redirect all notifications to a different number. After a successful mobile number change, all linked institutions are notified asynchronously via webhook so they can update the parent contact number in their local student records. The old mobile number enters a 7-day cooldown period during which it cannot be used to register a new parent account, preventing cases where someone registers with the parent's discarded SIM card. A maximum of 2 mobile number changes are permitted within a 90-day rolling window.

- **BR-02 — Notification Channel Fallback and Delivery Guarantee:** The notification system uses a waterfall delivery model based on the parent's configured channel priority. For Mrs. Lakshmi Devi, SMS is primary, WhatsApp is secondary, and push notification is tertiary. When a notification is triggered (e.g., Priya marked absent), the system first attempts SMS delivery via the configured telecom gateway (Airtel/Jio API). If the SMS delivery receipt is not received within 30 seconds, the system automatically falls back to WhatsApp using the pre-approved template message. If WhatsApp delivery also fails (e.g., parent's phone is offline), the push notification is queued. The system guarantees at least one successful delivery attempt across all channels before marking the notification as "delivery failed." Failed notifications are retried up to 3 times over 2 hours. Parents can view their complete notification history (including delivery status per channel) in the profile under a "Notification Log" section, which helps debug cases where they claim they did not receive an alert.

- **BR-03 — DPDP Act 2023 Compliance for Data Export and Deletion:** In compliance with India's Digital Personal Data Protection Act 2023, every parent has the right to export all personal data the platform holds about them and to request permanent deletion. The data export endpoint generates a ZIP file containing the parent's profile data, notification history, linked children metadata (not the children's full academic records, which belong to the institutions), login history, and consent records. The export is prepared asynchronously and is available for download within 48 hours; the parent receives a WhatsApp notification when the ZIP is ready. For account deletion, the system enforces a 14-day cooling period during which the parent can cancel the deletion request by logging in. After 14 days, all personal data is permanently erased from primary storage, and anonymised records are retained in aggregate analytics tables for a further 180 days as permitted under the DPDP Act's legitimate interest exemption. Linked institutions are notified of the deletion and must update their parent contact fields accordingly.

- **BR-04 — Per-Child Notification Customisation for Mixed Institution Types:** Parents with children across different institution types (school, college, coaching) often have very different notification needs for each child. For instance, Mrs. Lakshmi Devi wants daily attendance SMS alerts for Priya (Class 11 at Sri Chaitanya, where daily attendance matters for board exam eligibility) but does not need daily attendance alerts for Ravi's B.Tech at GCEH (where attendance is tracked monthly). She only wants mock test schedule reminders from TopRank Academy. The per-child override system allows parents to maintain a base notification configuration that applies to all children by default, and then selectively override specific notification types for individual child-institution links. Overrides are stored as JSON patches against the base configuration in the parent_preferences table, keeping storage efficient. When a notification is triggered, the system checks for a child-specific override first, and falls back to the base configuration if none exists. The override UI presents a simplified view showing only the differences from the base config, reducing cognitive load for parents managing multiple children.

---

*Last updated: 2026-03-31 · Group 8 — Parents Portal · Division A*
