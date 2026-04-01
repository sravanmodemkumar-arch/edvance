# Page: OTP Verification
**Route:** `[portal-url]/verify-otp?channel=whatsapp|sms&mobile=XXXXXXXXXX`
**Auth Stage:** 2 of 5
**Access:** Public — reached after login page sends OTP
**Previous:** [02-login.md](02-login.md)
**Next:** [04-role-selector.md](04-role-selector.md) or [05-profile-setup.md](05-profile-setup.md) or Home

---

## Overview

| Property | Value |
|---|---|
| Purpose | Verify 6-digit OTP. Authenticate the user. |
| OTP channel | WhatsApp (primary) or SMS (fallback) |
| OTP validity | 3 minutes from creation time |
| Max attempts | 3 wrong codes per OTP. 5 OTPs per 30 minutes per mobile. |
| Auto-submit | Yes — after entering 6th digit, form auto-submits |

---

## Page Sections

| # | Section | Position | Purpose |
|---|---|---|---|
| 1 | Back Navigation | Top | Return to login page |
| 2 | OTP Card | Center | Main OTP entry form |
| 3 | OTP Input | Inside card | 6 individual digit boxes |
| 4 | Timer | Inside card | Countdown — 3 minutes |
| 5 | Resend Options | Inside card | Resend WhatsApp / SMS / Different number |
| 6 | Footer | Bottom | Privacy, Terms |

---

## Section 1 — Back Navigation

| Element | Type | Spec |
|---|---|---|
| Back link | Icon + text | "[← Back to Login]" — left aligned, top of page |
| Behavior | Navigation | Navigates back to [02-login.md](02-login.md). Mobile pre-filled. |
| Warn on click | None | No warning — user just goes back. OTP is not invalidated. |

---

## Section 2 — OTP Card

| Element | Type | Spec |
|---|---|---|
| Card container | White card | `border-radius: 16px`, `padding: 40px`, `box-shadow: --shadow-2` |
| Channel icon | SVG icon | WhatsApp green logo (if WhatsApp) or SMS envelope icon (if SMS) |
| Sent-to message | Body text | "OTP sent to +91 98765 4XXXX via WhatsApp" — mobile masked last 6 digits shown |
| Instruction | Body text | "Enter the 6-digit code sent to your number" |
| Card max-width | Layout | 420px, centered on page |

---

## Section 3 — OTP Input Boxes

### Layout
```
┌───┐ ┌───┐ ┌───┐   ┌───┐ ┌───┐ ┌───┐
│ _ │ │ _ │ │ _ │   │ _ │ │ _ │ │ _ │
└───┘ └───┘ └───┘   └───┘ └───┘ └───┘
    Box 1-3            Box 4-6
    (visual gap between group of 3 and group of 3)
```

### Component Spec

| Property | Value |
|---|---|
| HTML element | 6 individual `<input type="text" maxlength="1" inputmode="numeric">` |
| Box size | 52×60px each. Gap 8px between boxes. Extra 12px gap between box 3 and 4. |
| Font | `--font-mono` (JetBrains Mono), 28px, bold |
| Text align | Center |
| Border default | 1.5px solid `--outline` |
| Border focus | 2px solid `--primary`, `box-shadow: 0 0 0 3px --primary-container` |
| Border filled | 1.5px solid `--outline-variant` |
| Background filled | `--primary-container` (light tint) |
| Border error | 2px solid `--error` on all 6 boxes simultaneously |
| Background error | `--error-container` on all 6 boxes |
| Border success | 2px solid `--success` on all 6 boxes |
| Background success | `--success-container` |

### Behavior

| Action | Result |
|---|---|
| Type digit 1–6 | Focus auto-advances to next box |
| Backspace on filled box | Clears current digit, focus moves to previous box |
| Backspace on empty box | Focus moves to previous box without clearing |
| Paste 6 digits | Distributes across all 6 boxes. Triggers auto-submit. |
| Paste partial (< 6) | Fills from cursor position. No auto-submit. |
| Type non-numeric | Input ignored. Box stays empty. |
| 6th digit entered | Auto-submit — no button click needed |
| Auto-submit | Loading overlay on card. All boxes disabled. |

### Submit Button (Manual fallback)

| Property | Value |
|---|---|
| Text | "Verify OTP" |
| Visibility | Shown below boxes. Useful if auto-submit fails. |
| State | Disabled (gray) until all 6 boxes filled |
| On click | Same as auto-submit |
| Loading | Button shows spinner + "Verifying...". Disabled. |

---

## Section 4 — Countdown Timer

| Property | Value |
|---|---|
| Duration | 3 minutes = 180 seconds |
| Format | "Expires in MM:SS" |
| Position | Below submit button, centered |
| Color: >60s | `--success` green |
| Color: 30–60s | `--warning` orange |
| Color: <30s | `--error` red + subtle pulse animation |
| On expire | OTP boxes disabled + grayed. "OTP expired. Request a new one." message. |
| Progress ring | Optional — circular SVG ring around timer digits (desktop only) |

---

## Section 5 — Resend Options

| Element | Visible After | Max Uses | Action |
|---|---|---|---|
| "Resend via WhatsApp" | 30 seconds | 3 per session | New OTP sent. Timer resets. Counter shown: "Sent (2/3)". |
| "Try SMS instead" | Immediately (if channel=whatsapp) | 2 per session | Switches to SMS channel. New OTP. |
| "Try a different number" | Always | — | Navigate back to [02-login.md](02-login.md). |
| "Resend in X seconds" | First 30s | — | Countdown before resend button activates |

### Resend Button States

| State | Visual |
|---|---|
| Locked (before 30s) | Gray text. "Resend in 24s". Not clickable. Countdown shown. |
| Active | Primary text link. Underline on hover. |
| Clicked | Brief "Sent!" confirmation text for 2 seconds, then resets |
| Exhausted (3/3 used) | Grayed out. "Maximum resends reached. Try different number." |

---

## States & Error Handling

| State | Trigger | UI Response |
|---|---|---|
| Default | Page load | Empty boxes. Timer running. |
| Filling | User types | Boxes fill left to right. |
| Auto-submitting | 6th digit entered | Overlay spinner on card. Boxes locked. "Verifying..." |
| Wrong OTP | API 401 `INVALID_OTP` | Shake animation on all 6 boxes. Red state. Error message: "Incorrect OTP. X attempt(s) remaining." Auto-clear all boxes after 600ms. Focus returns to box 1. |
| OTP expired | API 401 `EXPIRED_OTP` | Error message: "This OTP has expired. Request a new one." Resend button activates immediately. |
| Max attempts (3) | API 401 `MAX_ATTEMPTS` | Error: "Too many wrong attempts. Request a new OTP." All boxes disabled. Only resend/back options. |
| Session locked | API 429 | "Too many OTP requests. Try again in 30 minutes." Full lock. No resend. Only "Try different number". |
| Network error | API timeout | Toast: "Connection error." [Retry] button restores. |
| OTP verified | API 200 | All boxes turn green. Checkmark animation. Brief "Verified ✅" text. Then redirect. |

### Shake Animation (on wrong OTP)
- CSS: `@keyframes shake { 0%{x:0} 25%{x:-4px} 50%{x:4px} 75%{x:-4px} 100%{x:0} }`
- Duration: 400ms
- Applied to all 6 boxes simultaneously

### Error Message Display
```
┌────────────────────────────────────────────┐
│  ❌  Incorrect OTP. 2 attempts remaining.  │
└────────────────────────────────────────────┘
```
- Position: Below OTP boxes, above submit button
- Color: `--error` text on `--error-container` background
- Disappears when user starts re-typing

---

## Redirect Logic (After Successful OTP)

| Condition | Next Page |
|---|---|
| First-ever login (no profile) | [05-profile-setup.md](05-profile-setup.md) |
| Returning user, 1 role | Home page for that portal |
| Returning user, 2+ roles | [04-role-selector.md](04-role-selector.md) |
| Level 4/5 (Platform Admin) | [06-2fa.md](06-2fa.md) |
| Redirect param in URL | Honour `?next=/path` — redirect to original destination |

---

## API Calls

| Action | Endpoint | Method | Payload |
|---|---|---|---|
| Verify OTP | `/api/v1/auth/otp/verify` | POST | `{mobile, otp_code, session_token}` |
| Resend OTP | `/api/v1/auth/otp/resend` | POST | `{mobile, channel, session_token}` |

---

## Security Notes

| Rule | Implementation |
|---|---|
| OTP stored hashed | bcrypt hash in `identity.otps` table — never plain text |
| Server-side attempt count | 3 attempts per OTP code — enforced server-side, not just client |
| Rate limit | 5 OTP sends per mobile per 30 minutes — IP + mobile combined |
| Session token | Each OTP send creates a server-side session token. Verify endpoint validates token + code together. |
| Old OTP invalidated | Each new OTP send invalidates all previous codes for that mobile |
| Audit log | Every verify attempt logged: mobile, result, IP, timestamp |
