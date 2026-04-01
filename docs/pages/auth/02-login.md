# Page: Login
**Route:** `[portal-url]/login`
**Auth Stage:** 1 of 5
**Access:** Public — no auth required

---

## Overview

| Property | Value |
|---|---|
| Purpose | Mobile number entry. First step of OTP login. |
| Who sees it | Every user on every portal — first page after landing |
| Portal branding | Color, logo, portal name change per subdomain |
| No passwords | EduForge is OTP-only. No password field ever. |
| Next step | → [03-otp-verification.md](03-otp-verification.md) |

---

## Page Sections

| # | Section | Width | Visibility |
|---|---|---|---|
| 1 | Left Brand Panel | 40% | Desktop only (≥768px) |
| 2 | Login Form Panel | 60% (100% mobile) | Always |
| 3 | Footer Strip | Full width | Always |

---

## Section 1 — Left Brand Panel (Desktop only)

| Element | Type | Spec |
|---|---|---|
| Institution Logo | Image | 120×120px, rounded-12, object-fit: contain. Fallback = EduForge logo |
| Institution Name | H1 | Max 2 lines. Truncate. Primary color. |
| City, State | Body text | Secondary color. Below institution name. |
| Student count badge | Stat chip | "X,XXX Students" — only for institution portals. Not on exam domain portals. |
| Divider | Horizontal line | Thin, `--outline-variant` |
| Today's Live Stats | 3-cell grid | See stat cell spec below |
| Powered by EduForge | Footer text | Bottom of left panel. Small, muted. Links to eduforge.in |
| Panel background | Gradient | Portal primary color → 20% lighter. Subtle diagonal gradient. |
| Panel text | All white | Text contrast enforced — switch to dark text if primary is too light |

**Today's Live Stats cells (institution portals only):**

| Stat | Source | Format |
|---|---|---|
| Attendance Today | Live API | "Attendance: 94.2%" with mini progress bar |
| Tests Today | Live API | "Tests Today: 3" — count of exams scheduled/running |
| New This Month | Live API | "New Students: 12" |

> If API fails: stat cells show skeleton shimmer. Never show stale data.
> For Exam Domain portals (SSC, RRB): replace stats with "1.2L students enrolled this month" type marketing stat.

---

## Section 2 — Login Form Panel

| Element | Type | Position | Spec |
|---|---|---|---|
| Portal greeting | H2 | Top of form | "Welcome back" (returning) / "Get started" (new) |
| Portal name | H3 | Below H2 | Portal-specific subtitle, e.g., "XYZ School — Staff Portal" |
| Form card | White card | Center | `border-radius: 16px`, `box-shadow: --shadow-2`, `padding: 40px` |
| Mobile label | Form label | Above input | "Enter your mobile number" |
| Country code | Static badge | Left of input | "+91" — Phase 1 India only |
| Mobile input | Input[tel] | Center | 10 digits, `inputmode="numeric"`, auto-format with space at 5 digits |
| Send OTP — WhatsApp | Primary button | Below input | Green `#25D366`. WhatsApp icon (SVG). Full width. |
| Send via SMS | Text link | Below WhatsApp button | Secondary option. Smaller. Shows after WhatsApp button loads. |
| Divider | "── or ──" | Between options | Muted. Visual separator only. |
| First time / Register | Text link | Bottom of form | "First time here? [Register / Find Account]" |

**Mobile input field — detailed:**

| Property | Value |
|---|---|
| Width | 100% of form card |
| Height | 52px |
| Border | 1.5px solid `--outline` |
| Border (focus) | 2px solid `--primary` (portal color) |
| Border (error) | 2px solid `--error` |
| Padding | 16px horizontal |
| Left element | "+91" badge, separated by thin vertical divider |
| Font size | 18px (larger — phone number readability) |
| Max length | 10 digits |
| Auto-format | After 5 digits: insert space — "98765 43210" display only, value is raw 10 digits |

---

## Section 3 — Footer Strip

| Element | Type | Spec |
|---|---|---|
| Copyright | Text | "© 2024 EduForge Technologies Pvt Ltd" |
| Privacy Policy | Link | Opens Privacy Policy in modal — does NOT navigate away |
| Terms of Service | Link | Opens Terms in modal |
| Help | Link | "Need help? [Contact Support]" |
| Language toggle | Optional | For Telugu/Hindi portals: EN / తెలుగు / हिंदी |

---

## Platform Admin Login — Special Rules

| Rule | Detail |
|---|---|
| URL | `admin.eduforge.in/login` — no institution branding, EduForge branding only |
| Left panel | Shows EduForge platform stats (total institutions, total students, exams running) |
| "First time here" | Hidden — no self-registration. Accounts created by HR only. |
| After OTP success (Level 4/5) | Redirect to → [06-2fa.md](06-2fa.md) instead of home |

---

## States & Validation

| State | Trigger | UI Response |
|---|---|---|
| Default | Page load | Empty input, both buttons visible |
| Typing | User inputs digits | Input fills left to right |
| Invalid length | Submit with < 10 digits | Red border + inline error: "Enter valid 10-digit number" |
| Invalid start | Number starts with 0, 1, 2, 3, 4, 5 | Error: "Mobile must start with 6, 7, 8, or 9" |
| Loading | Button clicked | Button shows spinner + "Sending...". Input disabled. |
| OTP sent | API 200 | Navigate to [03-otp-verification.md](03-otp-verification.md) |
| Account not found | API 404 | Alert banner below input (see alert spec) |
| Account suspended | API 403 `SUSPENDED` | Navigate to [08-account-blocked.md](08-account-blocked.md) |
| WhatsApp failed | Delivery failure webhook | Auto-show SMS option as toast: "WhatsApp failed. [Try SMS]" |
| Rate limited | 5+ sends in 5 min | Error: "Too many attempts. Try again in [X] minutes." Countdown timer. |
| Network error | API timeout | Error toast: "Connection error. Check internet." [Retry] |

---

## Account Not Found Alert

```
┌────────────────────────────────────────────────────────────┐
│  ⚠️  No account found                                      │
│                                                            │
│  +91 98765 43210 is not registered in [Portal Name].      │
│                                                            │
│  Are you a student? → student.eduforge.in                  │
│  Are you a parent?  → parent.eduforge.in                   │
│  Wrong institution? → [Find your institution]              │
│                                                            │
│  [Try a different number]              [Contact Admin]     │
└────────────────────────────────────────────────────────────┘
```

---

## API Calls

| Action | Endpoint | Method | Payload |
|---|---|---|---|
| Send OTP via WhatsApp | `/api/v1/auth/otp/send` | POST | `{mobile, channel: "whatsapp", portal_slug}` |
| Send OTP via SMS | `/api/v1/auth/otp/send` | POST | `{mobile, channel: "sms", portal_slug}` |
| Lookup mobile | `/api/v1/auth/lookup` | POST | `{mobile, portal_slug}` — pre-check before send |

---

## Responsive Behavior

| Breakpoint | Change |
|---|---|
| Desktop ≥768px | Left brand panel (40%) + form (60%) side by side |
| Mobile <768px | Left panel hidden. Logo + portal name shown as small header strip above form. Form takes 100% width. |
| Very small <380px | Form padding reduces to 24px. Button text shortened. |
