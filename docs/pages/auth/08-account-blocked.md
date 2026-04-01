# Page: Account Blocked / Suspended
**Route:** `[portal-url]/account-blocked`
**Access:** Redirected automatically when blocked account tries to login
**Type:** Full page — no sidebar, no auth layout

---

## Overview

| Property | Value |
|---|---|
| Purpose | Inform user their account is suspended and provide clear resolution path |
| Trigger | Login attempt returns API 403 with `status: SUSPENDED` or `BLOCKED` |
| Who sees it | Any user across any portal whose account is suspended |
| Resolution | Contact institution admin or EduForge support |

---

## Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Status Icon + Headline | Visual confirmation of suspension |
| 2 | Reason Panel | Why the account is blocked (if disclosable) |
| 3 | Resolution Steps | What the user should do |
| 4 | Contact Info | Support contact details |
| 5 | Reference ID | Ticket reference for support calls |

---

## Section 1 — Status Icon + Headline

| Element | Type | Spec |
|---|---|---|
| Icon | SVG | 80×80px shield with ⛔ or 🔒. Red (`--error`) color. |
| Headline | H1 | "Account Suspended" |
| Sub-headline | H2 | Context-based (see variants below) |
| Animation | Entry | Icon drops in with subtle bounce. No repeat animation. |

### Suspension Type Variants

| Type | Icon | Headline | Sub-headline |
|---|---|---|---|
| Admin suspended | 🔒 | "Account Suspended" | "Your access has been suspended by your institution." |
| Platform suspended | ⛔ | "Account Suspended" | "Your account has been suspended by EduForge." |
| BGV not completed | ⚠️ | "Access Restricted" | "Complete your background verification to restore access." |
| Fee defaulter lock | 💳 | "Access Restricted" | "Clear your outstanding fees to restore full access." |
| Rate limit lock (OTP) | ⏱ | "Temporarily Locked" | "Too many failed attempts. Try again in X minutes." |
| POCSO/Legal hold | 🔒 | "Account Under Review" | "Your account is under review. Contact support for details." |

---

## Section 2 — Reason Panel

| Element | Type | Spec |
|---|---|---|
| Reason card | Info card | Shown only if reason is disclosable |
| Reason label | Label | "Reason for suspension:" |
| Reason text | Body | e.g., "Suspended by Principal on [date]" |
| Suspended by | Meta | "By: [Admin name] — [Institution]" |
| Suspended on | Meta | "Date: [DD MMM YYYY, HH:MM]" |
| Sensitive reasons | Hidden | POCSO/legal investigations: "Your account is under review." — no details shown |

---

## Section 3 — Resolution Steps

| Scenario | Resolution Steps Shown |
|---|---|
| Admin suspended (institution) | 1. Contact your class teacher or HOD. 2. Or call institution front desk. 3. Or email institution admin. |
| Platform suspended | 1. Call EduForge support: 1800-XXX-XXXX. 2. Email: support@eduforge.in |
| BGV pending | 1. Submit your BGV documents. [Submit BGV →] button. |
| Fee defaulter | 1. Clear your outstanding fees. [Pay Now →] button (opens payment with limited access). |
| Temp lock (rate limit) | Countdown timer: "You can try again in [X minutes]." |
| Legal hold | "Contact EduForge support for assistance." |

---

## Section 4 — Contact Info

```
┌──────────────────────────────────────────────────┐
│  Need help?                                      │
│                                                  │
│  📞  1800-XXX-XXXX  (toll-free, 9AM–6PM)        │
│  📧  support@eduforge.in                         │
│  💬  WhatsApp: +91 XXXXX XXXXX                   │
│                                                  │
│  Response time: < 4 hours on business days       │
└──────────────────────────────────────────────────┘
```

---

## Section 5 — Reference ID

| Element | Spec |
|---|---|
| Reference ID | Auto-generated: `EF-2024-BLK-XXXXXX` |
| Copy button | "[📋 Copy Reference ID]" — copies to clipboard |
| Purpose | "Mention this ID when contacting support for faster resolution" |
| Visibility | Always shown — helps support team locate the account |

---

## Actions Available

| Action | When | Behavior |
|---|---|---|
| [Try Different Number] | Always | Goes back to [02-login.md](02-login.md) |
| [Contact Support] | Always | Opens WhatsApp chat with pre-filled message |
| [Submit BGV] | BGV pending only | Opens BGV submission form |
| [Pay Now] | Fee defaulter only | Opens fee payment page with limited session |
| [Try again in X min] | Rate limit only | Countdown. Button activates after timer. |

---

## API Calls

| Action | Endpoint | Notes |
|---|---|---|
| Get suspension details | `/api/v1/auth/account-status` | Returns reason, date, contact info |
| Check rate limit status | `/api/v1/auth/rate-limit-status` | Returns remaining wait time |
