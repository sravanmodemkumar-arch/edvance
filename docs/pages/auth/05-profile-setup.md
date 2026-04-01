# Page: First Login — Profile Setup (Wizard)
**Route:** `[portal-url]/setup-profile`
**Auth Stage:** 4 of 5 (first login only)
**Access:** Authenticated — shown only on very first login
**Previous:** [03-otp-verification.md](03-otp-verification.md)
**Next:** Home page of portal

---

## Overview

| Property | Value |
|---|---|
| Purpose | Collect basic profile info on first login. One-time wizard. |
| Trigger | `user.profile_completed = false` after OTP verification |
| Skip condition | Returning user with profile → bypassed |
| Total steps | 4 steps. Steps 1–3 required. Step 4 optional. |
| Cannot skip | Steps 1, 2, 3. Step 4 has "Skip" option. |
| Mobile | Already verified — shown as read-only, not re-asked |

---

## Page Layout (Shared Across All Steps)

```
┌──────────────────────────────────────────────────────┐
│  [Portal Logo]                                       │
│                                                      │
│  Complete your profile                               │
│  Step X of 4                                         │
│                                                      │
│  ●━━━━━━━━●━━━━━━━━○━━━━━━━━○                        │
│  Photo    Name    Email   Notif.                      │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │                                                │  │
│  │    [Step-specific content]                     │  │
│  │                                                │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  [← Back]                          [Next →]         │
└──────────────────────────────────────────────────────┘
```

---

## Section: Step Progress Bar

| Element | Type | Spec |
|---|---|---|
| Progress dots | 4-step indicator | See [06-navigation.md](../components/06-navigation.md) — Step Progress component |
| Step labels | Text below dots | "Photo", "Name", "Email", "Notifications" |
| Completed steps | Filled circle with ✓ | Primary color |
| Active step | Filled circle (no ✓) | Primary color, pulsing glow |
| Future steps | Empty outline circle | Gray |
| Connector line | Horizontal line | Solid primary (completed), dashed gray (future) |
| Position | Top of white card | Centered |

---

## Step 1 — Profile Photo

### Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Step header | "Add your profile photo" + why it's needed |
| 2 | Photo upload area | Current photo (blank) + upload options |
| 3 | Requirements | Size/format guidelines |
| 4 | Skip notice | "Skip for now — must upload within 7 days" |
| 5 | Next button | Proceeds to Step 2 |

### Section 2 — Photo Upload Area

| Element | Type | Spec |
|---|---|---|
| Current photo circle | 128×128px | Circular. Default = gray circle with camera icon. |
| Upload photo button | Secondary button | "[📁 Upload Photo]" — opens OS file picker |
| Take selfie button | Secondary button | "[📷 Take Selfie]" — opens camera (mobile/laptop cam) |
| Crop tool | Modal overlay | Opens after file selected. Circular crop only. Zoom slider. Rotate 90°. |
| Preview | After crop | Shows cropped photo in 128px circle + "Looks like your ID card" |

### File Upload Validation

| Rule | Value |
|---|---|
| Accepted formats | JPG, JPEG, PNG, WEBP |
| Max file size | 5 MB |
| Min dimensions | 100 × 100px |
| Max upload (after compress) | 200 KB (client-side compression before upload) |
| Face detection | Optional soft check — "Make sure your face is clearly visible" (not enforced) |

### States

| State | UI |
|---|---|
| No photo | Gray placeholder circle + camera icon |
| File selected | Opens crop modal |
| Cropping | Crop tool active. "Apply Crop" button. |
| Photo ready | Shows preview. "Retake" link below. |
| Uploading | Progress ring on photo circle |
| Upload error | Error toast. "Upload failed. Try again." |
| Skip clicked | Stores skip flag. Shows "⚠ Upload photo within 7 days" reminder on dashboard. |

---

## Step 2 — Name Confirmation

### Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Step header | "Confirm your name" + note about admin-approval for changes |
| 2 | Name form | First name, Last name, Display name fields |
| 3 | Language preference | Preferred UI language |
| 4 | Navigation | Back + Next |

### Section 2 — Name Form

| Field | Type | Pre-filled? | Editable? | Rules |
|---|---|---|---|---|
| First Name | Text input | Yes — from institution records | Yes | Min 2, max 50 chars. Letters + `.` `-` `'` only. |
| Last Name | Text input | Yes | Yes | Min 1, max 50 chars. |
| Display Name | Text input | Auto-generated: First + Last | Yes | Max 100 chars. Used in all UI references. |
| Language | Select dropdown | Default: English | Yes | Options: English, Telugu (తెలుగు), Hindi (हिंदी) |

> **Note:** Name changes are flagged for admin review. Changes take effect immediately, but admin receives notification.

### Section 3 — Language Preference

| Option | Value | Effect |
|---|---|---|
| English | `en` | Default UI language |
| Telugu (తెలుగు) | `te` | UI translates to Telugu (where supported) |
| Hindi (हिंदी) | `hi` | UI translates to Hindi (where supported) |

---

## Step 3 — Email Address

### Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Step header | "Add your email" + why it matters |
| 2 | Email input | Single email field |
| 3 | Purpose explanation | What email is used for |
| 4 | Navigation | Back + Next |

### Section 2 — Email Input

| Element | Type | Spec |
|---|---|---|
| Email field | Input[email] | Full width. Lowercase auto-transform. |
| Validation | Inline | Real-time format check. Error below field on blur. |
| Error | Inline | "Enter a valid email address" |
| Duplicate check | API | On blur: "This email is already linked to another account" if duplicate |

### Section 3 — Purpose Panel

```
┌──────────────────────────────────────────────────────┐
│  📧  Your email is used for:                         │
│      • Rank certificates (PDF download link)         │
│      • Fee invoices and receipts                     │
│      • Important platform announcements              │
│      • Account recovery (if needed)                  │
└──────────────────────────────────────────────────────┘
```

---

## Step 4 — Notification Preferences (Optional)

### Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Step header | "How should we notify you?" |
| 2 | Notification toggles | 4 channel options |
| 3 | Skip option | Skip — set preferences later in settings |
| 4 | Complete setup button | Finish wizard |

### Section 2 — Notification Toggles

| Channel | Default | Details |
|---|---|---|
| WhatsApp | ON ✅ | "+91 [mobile] — already linked". Cannot turn off (required for OTP). |
| SMS | ON ✅ | "Critical alerts and OTP only" |
| Email | OFF (until email added) | Enabled only if Step 3 email was provided |
| Push (mobile app) | ON ✅ | "Daily attendance, new results" |
| In-app | Always ON | Cannot be turned off — platform notifications |

> WhatsApp toggle: Shown as ON but cannot be toggled off — it's required for OTP delivery. Helper text explains why.

---

## Completion Screen

| Element | Spec |
|---|---|
| Checkmark animation | Large green ✅ with bounce-in animation |
| Message | "Profile setup complete! Welcome to EduForge, [First Name]." |
| Sub-message | "Taking you to your dashboard..." |
| Progress bar | Linear, 0→100% over 2 seconds |
| Auto-redirect | After 2 seconds → home page of portal |
| Manual link | "Go now →" for impatient users |

---

## API Calls

| Step | Action | Endpoint | Method |
|---|---|---|---|
| Step 1 | Upload photo | `/api/v1/user/profile/photo` | POST (multipart) |
| Step 2 | Save name + language | `/api/v1/user/profile/basic` | PATCH |
| Step 3 | Save email | `/api/v1/user/profile/email` | PATCH |
| Step 4 | Save notification prefs | `/api/v1/user/notifications/preferences` | PATCH |
| Any | Mark profile complete | `/api/v1/user/profile/complete` | POST |
