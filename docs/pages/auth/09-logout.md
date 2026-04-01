# Page: Logout (Confirm Modal)
**Type:** Modal overlay — not a full page
**Trigger:** User clicks "Log Out" from profile dropdown or sidebar
**Previous page:** Any page inside portal

---

## Overview

| Property | Value |
|---|---|
| Purpose | Confirm logout intent. Warn about unsaved changes. Clear session. |
| Display type | Modal (400px, centered) — over current page |
| Smart behavior | Detects unsaved changes and shows extra warning |

---

## Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Modal header | "Log out of [Portal Name]?" |
| 2 | Unsaved changes warning | Shown only if unsaved form data detected |
| 3 | Confirmation text | What happens after logout |
| 4 | Action buttons | Cancel + Log out |

---

## Section 1 — Modal Header

| Element | Type | Spec |
|---|---|---|
| Title | H2 | "Log out of [Portal Name]?" |
| Portal name | Dynamic | Current portal name. e.g., "Log out of XYZ School Portal?" |
| Close [✕] | Icon button | Closes modal. Same as Cancel. |
| Icon | Optional | Exit door icon — 24px, muted color |

---

## Section 2 — Unsaved Changes Warning

> Shown ONLY if `window.beforeunload` detects unsaved form state.

```
┌────────────────────────────────────────────────────┐
│  ⚠️  You have unsaved changes                      │
│                                                    │
│  The form you were editing has unsaved data.       │
│  Logging out will discard these changes.           │
└────────────────────────────────────────────────────┘
```

| Condition | Warning shown? |
|---|---|
| No active form | ❌ Not shown |
| Form with unsaved data | ✅ Shown — orange warning panel inside modal |
| Form already saved | ❌ Not shown |

---

## Section 3 — Confirmation Text

| Text | Condition |
|---|---|
| "You will need to verify your OTP to log back in." | Standard — always shown |
| "Your active exam session will be lost." | Only if user is currently in an active test |
| "All other portals remain logged in." | Only if user has multiple active portal sessions |

---

## Section 4 — Action Buttons

| Button | Style | Action |
|---|---|---|
| [Cancel] | Ghost/text button | Closes modal. Returns to previous page. |
| [Log Out] | Filled — default style | Proceeds with logout |
| [Log Out] (with unsaved) | Filled — `--error` red | When unsaved changes exist — red to emphasize risk |
| [Log Out] (exam session) | Filled — `--error` red + confirm text | "Log Out & End Exam" — extra severity |

---

## Logout Process (After Confirmation)

| Step | Action |
|---|---|
| 1 | POST `/api/v1/auth/logout` with refresh token |
| 2 | Server invalidates refresh token (added to `identity.token_blocklist`) |
| 3 | Server deletes active session from `identity.sessions` table |
| 4 | Client clears: localStorage, sessionStorage, all auth cookies for this subdomain |
| 5 | Redirect to `[portal-url]/login` |
| 6 | Show success toast on login page: "You've been logged out successfully." |

---

## Special Cases

| Scenario | Behavior |
|---|---|
| Admin impersonation active | Log out ends impersonation + actual admin session both. Warning shown. |
| Active exam (student) | Extra confirmation: "Your exam will be submitted with current answers." |
| Multi-device active | Only this device session ends. Other device sessions unaffected. |
| "Log out all devices" | Available in Profile → Security. Invalidates ALL refresh tokens for this mobile. |
