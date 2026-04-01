# Page: Session Expired / Re-Authentication
**Route:** `[portal-url]/reauth` (overlay, not full page)
**Access:** Shown mid-session when JWT access token expires
**Type:** Modal overlay — page content behind is preserved

---

## Overview

| Property | Value |
|---|---|
| Purpose | Re-verify identity without losing current page or unsaved work |
| Trigger | Access token expiry detected (API returns 401 `TOKEN_EXPIRED`) |
| Display type | Full-screen semi-transparent overlay over current page |
| User identity | Pre-known — mobile shown masked, no re-entry needed |

---

## Session Timeout Rules

| Role Level | Access Token | Refresh Window |
|---|---|---|
| Level 0–2 (Staff, read-only) | 7 days | 30 days |
| Level 3 (Operations) | 24 hours | 7 days |
| Level 4 (Infrastructure) | 8 hours | 24 hours |
| Level 5 (Super Admin) | 8 hours | 24 hours |
| Active exam session | Never expires mid-exam | Protected by exam token |

---

## Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Backdrop | Blurs current page, preserves it behind |
| 2 | Re-auth card | Identity confirmation card |
| 3 | Action options | Verify identity or full logout |

---

## Section 1 — Backdrop

| Element | Spec |
|---|---|
| Background | Current page content blurred (`backdrop-filter: blur(4px)`) + darkened (50% overlay) |
| Z-index | 9000 — above everything including nav and modals |
| Interaction | Page content NOT clickable behind overlay |
| Scroll | Page scroll locked while overlay is open |

---

## Section 2 — Re-auth Card

```
┌────────────────────────────────────────────────────┐
│                                                    │
│              🔒                                    │
│                                                    │
│   Your session has expired                         │
│                                                    │
│   You've been inactive for 8 hours.                │
│   Verify your identity to continue where you       │
│   left off.                                        │
│                                                    │
│   ─────────────────────────────────────────────   │
│                                                    │
│   Logged in as:                                    │
│   +91 98765 4XXXX  ·  [Portal Name]               │
│   Role: Content Director                           │
│                                                    │
│   ─────────────────────────────────────────────   │
│                                                    │
│   [Send OTP via WhatsApp — Verify]                 │
│                                                    │
│   [Not you? Log out and switch user]               │
│                                                    │
└────────────────────────────────────────────────────┘
```

| Element | Type | Spec |
|---|---|---|
| Lock icon | SVG | 48px, `--primary` color |
| Headline | H2 | "Your session has expired" |
| Body text | Body | Explains inactivity duration |
| Identity panel | Info card | Shows masked mobile + portal name + current role |
| Primary button | CTA | "Send OTP via WhatsApp — Verify" — sends OTP to known mobile |
| Logout link | Text link | Below primary button. Red text. Opens logout confirm. |

---

## Section 3 — After OTP Sent (Inline OTP Entry)

> OTP entry happens inline in the same card — no page navigation.

```
┌────────────────────────────────────────────────────┐
│              🔒                                    │
│   Verify your identity                             │
│                                                    │
│   OTP sent to +91 98765 4XXXX via WhatsApp         │
│                                                    │
│   ┌───┐ ┌───┐ ┌───┐   ┌───┐ ┌───┐ ┌───┐          │
│   │ _ │ │ _ │ │ _ │   │ _ │ │ _ │ │ _ │          │
│   └───┘ └───┘ └───┘   └───┘ └───┘ └───┘          │
│                                                    │
│   ⏱ Expires in 02:47                              │
│                                                    │
│   [Resend OTP]              [Log out instead]      │
│                                                    │
└────────────────────────────────────────────────────┘
```

| On Success | Behavior |
|---|---|
| OTP verified | Overlay closes. User returns to exact same page + scroll position. New session token set. |
| Level 4/5 | After OTP: must also verify 2FA (same inline card → shows TOTP input) |

---

## Unsaved Changes Warning

> If user has unsaved form data when session expires — shown additional notice.

```
┌──────────────────────────────────────────────────────────┐
│  ⚠️  You have unsaved changes                            │
│                                                          │
│  Verify your session to save your work.                  │
│  If you log out, your changes will be lost.              │
└──────────────────────────────────────────────────────────┘
```

Shown inside the re-auth card, above the identity panel.

---

## API Calls

| Action | Endpoint | Method |
|---|---|---|
| Send re-auth OTP | `/api/v1/auth/reauth/otp/send` | POST |
| Verify re-auth OTP | `/api/v1/auth/reauth/otp/verify` | POST |
| Full logout | `/api/v1/auth/logout` | POST |
