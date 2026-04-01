# EduForge — Authentication Pages
## Ultra-Professional UI Specification

> **Scope:** All portals. Auth is shared across all 10 groups.
> OTP-only login (no passwords). WhatsApp primary, SMS fallback.
> This spec covers every screen, state, component, and edge case.

---

## Component References Used in Auth Pages

| Component | File | Usage |
|---|---|---|
| Form Inputs | [05-forms-inputs.md](../components/05-forms-inputs.md) | Mobile field, OTP boxes, profile setup form |
| Alerts & Toasts | [03-alerts-toasts.md](../components/03-alerts-toasts.md) | Error banners, success toasts, confirm dialogs |
| Design Tokens | [08-design-tokens.md](../components/08-design-tokens.md) | Portal colors, typography, spacing |
| Data Display | [07-data-display.md](../components/07-data-display.md) | Avatar, role badges, stat cards on brand panel |
| Modal & Drawer | [02-modal-drawer.md](../components/02-modal-drawer.md) | Privacy/Terms modal, unsaved-changes guard |

---

## Portal-to-Group URL Routing Matrix

| URL | Group | Portal Name | Audience |
|---|---|---|---|
| `admin.eduforge.in` | Group 1 | Platform Admin Portal | EduForge employees only |
| `[slug].eduforge.in/admin` | Group 2 | Institution Group Portal | Chain/trust management |
| `[slug].eduforge.in` | Group 3 | School Portal | School staff + teachers |
| `[slug].eduforge.in/college` | Group 4 | College Portal | Intermediate college staff |
| `[slug].eduforge.in/coaching` | Group 5 | Coaching Portal | Coaching staff + faculty |
| `ssc.eduforge.in` | Group 6 | SSC Exam Domain | SSC aspirants |
| `rrb.eduforge.in` | Group 6 | RRB Exam Domain | Railway aspirants |
| `[brand].testpro.in` | Group 7 | TSP Portal | Coaching's white-label test series |
| `parent.eduforge.in` | Group 8 | Parent Portal | Parents & guardians |
| `partners.eduforge.in` | Group 9 | B2B Partner Portal | API/tech partners |
| `student.eduforge.in` | Group 10 | Student Portal | Web student access |
| `eduforge.in` (root) | All | Smart Landing | Detects and routes |

> **Rule:** Every portal has its own subdomain. Login state is scoped per subdomain.
> A platform admin logged into `admin.eduforge.in` is NOT logged into `schools.eduforge.in`.

---

## Page 1 — Smart Landing (eduforge.in root)

### Route
`https://eduforge.in/`

### Purpose
Detect what the visitor needs and route them to the correct portal. Never a dead end.
First impression — must communicate credibility, scale, and purpose in under 3 seconds.

### Page Sections — Overview

| # | Section | Position | Purpose |
|---|---|---|---|
| 1 | Header / Nav Bar | Top, sticky | Logo, portal links, login shortcut |
| 2 | Hero Section | Full viewport height | Primary CTA — role selector + mobile entry |
| 3 | Trust Band | Below hero | Logo carousel of partner institutions |
| 4 | Product Cards | Mid page | Explain 4 major products |
| 5 | Stats Section | Mid-lower page | Social proof numbers |
| 6 | Footer | Bottom | Legal links, contact, sitemap |

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER                                                          │
│  [EduForge Logo]           [For Institutions ▼] [Log In ▼]     │
│                            [For Students]                        │
└─────────────────────────────────────────────────────────────────┘
│                                                                  │
│  HERO SECTION                                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Headline: "India's Most Trusted EdTech Platform"          │ │
│  │  Sub: "25 lakh+ students · 1,900+ institutions"            │ │
│  │                                                            │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │  I am a: [Student ▼] [Institution Admin ▼]          │  │ │
│  │  │          [Parent ▼]  [Exam Aspirant ▼]              │  │ │
│  │  │                                                     │  │ │
│  │  │  Mobile Number: [+91 ___________] [→ Continue]      │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  TRUST BAND                                                      │
│  [AP SCERT Logo] [TS SCERT Logo] [CBSE] [Narayana] [SR Nagar]  │
│                                                                  │
│  PRODUCT CARDS                                                   │
│  [Schools & Colleges] [Coaching Centres] [Exam Domains] [TSP]  │
│                                                                  │
│  STATS SECTION                                                   │
│  25L+ Students   1,900+ Institutions   6 Exam Domains   99.9%  │
│                                                                  │
│  FOOTER                                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Section 1 — Header / Nav Bar

| Element | Type | Position | Behavior |
|---|---|---|---|
| EduForge Logo | SVG image | Top-left | Click = reload page (no nav on root) |
| "For Institutions" | Dropdown nav | Center-right | Items: School, College, Coaching, Institution Group — each goes to portal landing |
| "For Students" | Text link | Center-right | Goes to `student.eduforge.in` |
| "Log In" | Dropdown button | Far-right | All portal links listed with icons |
| Mobile: hamburger | Icon button | Far-right (mobile) | Opens full-screen nav overlay |

> Behavior: On scroll > 60px → header background becomes white with shadow (was transparent).

### Section 2 — Hero Section

| Element | Type | Position | Behavior |
|---|---|---|---|
| Headline text | H1 | Center | "India's Most Trusted EdTech Platform" |
| Sub-headline | H2 | Below H1 | "25 lakh+ students · 1,900+ institutions" |
| "I am a" selector | Dropdown | Inside card | Options: Student, Institution Admin, Parent, Exam Aspirant. Updates routing logic. |
| Mobile input | Input[tel] | Inside card | "+91" prefix, 10-digit, Indian numbers. Auto-formats. |
| Continue button | Primary CTA | Inside card | API: `POST /api/v1/auth/lookup`. Routes based on role + found/not-found. |
| Background | Gradient image | Full section | Brand gradient — left indigo to right blue. Pattern overlay. |

> Mobile: Card takes 90% width. Role dropdown becomes stacked select above mobile input.

### Section 3 — Trust Band

| Element | Type | Behavior |
|---|---|---|
| Partner logos | 120×40px images, grayscale | Auto-scroll carousel, 6 visible at once on desktop, 3 on mobile |
| Scroll speed | CSS animation | 30-second full loop, pauses on hover |
| Logo types | Mix | AP SCERT, TS SCERT, Narayana, Sri Chaitanya, CBSE, state board logos |

### Section 4 — Product Cards

| Card | Icon | Headline | Sub | CTA |
|---|---|---|---|---|
| Schools & Colleges | 🏫 | "For Schools & Colleges" | Attendance, exams, fees in one place | [Explore →] |
| Coaching Centres | 📚 | "For Coaching Centres" | Batch management, mock tests, TSP | [Explore →] |
| Exam Domains | 📝 | "For Exam Aspirants" | SSC, RRB, UPSC, Banking mock tests | [Try Free →] |
| TSP | 🎯 | "Launch Your Own Test Series" | White-label — your brand, our engine | [Start TSP →] |

> Desktop: 4 cards in a row. Tablet: 2×2 grid. Mobile: Vertical stack.
> Hover: Card lifts with shadow (elevation 3), primary border shows.

### Section 5 — Stats Section

| Stat | Value | Sub-label |
|---|---|---|
| Students | 25L+ | on the platform |
| Institutions | 1,900+ | schools, colleges, coaching |
| Exam Domains | 6 | SSC, RRB, UPSC, Banking, AP, TS |
| Uptime | 99.9% | exam-day reliability |

> Count-up animation on scroll into view (0 → final value over 2 seconds).

### Section 6 — Footer

| Column | Content |
|---|---|
| Company | About Us, Careers, Blog, Press |
| Products | Schools, Coaching, Exam Domains, TSP, API Partners |
| Legal | Privacy Policy, Terms of Service, Refund Policy, DPDP Compliance |
| Contact | support@eduforge.in, 1800-XXX-XXXX, WhatsApp |
| Socials | YouTube, Instagram, Twitter/X, Telegram |

> Footer background: `--text-primary` (near-black). Text: white / gray.
> "Powered by EduForge" with year and version at very bottom.

### Components

| Component | Type | Behavior |
|---|---|---|
| "I am a" dropdown | Select | On change — updates placeholder and routing logic |
| Mobile field | Input (tel) | Auto-format: `+91 XXXXX XXXXX`, Indian only (Phase 1) |
| Continue button | Primary CTA | On click → lookup mobile → route to correct portal login |
| For Institutions dropdown | Nav dropdown | Links: School, College, Coaching, Institution Group |
| Log In dropdown | Nav dropdown | All portal options for direct navigation |
| Trust band logos | Static carousel | Auto-scroll, 6 visible at a time |
| Product cards | Hover cards | Each links to portal landing |

### States

| State | Trigger | UI Behavior |
|---|---|---|
| Default | Page load | Clean hero, all fields empty |
| Mobile found — 1 role | Enter mobile → Continue | Direct to that portal's login page with mobile pre-filled |
| Mobile found — multiple roles | Enter mobile → Continue | Show role selector modal (see Page 4) |
| Mobile not found | Enter mobile → Continue | Show "Register or find your institution" helper |
| Loading | Continue clicked | Spinner inside button, button disabled |

### Business Rules

- If mobile is in system → determine group → redirect to portal login (mobile pre-filled, skip re-entry)
- If mobile is NOT in system → show helper: "Are you from an institution? Ask your admin to enrol you." with option to try exam domain self-registration
- Direct URLs (admin.eduforge.in etc.) bypass this page entirely — they go straight to Page 2

---

## Page 2 — Portal Login Page

> This page is rendered differently per portal, but the component layout is identical.
> Color scheme, logo, and portal name change per domain.

### Routes

| Portal | URL | Primary Color |
|---|---|---|
| Platform Admin | `admin.eduforge.in/login` | `#1A237E` (Deep Indigo) |
| School | `[slug].eduforge.in/login` | `#1565C0` (Institutional Blue) |
| Coaching | `[slug].eduforge.in/coaching/login` | `#B71C1C` (Coaching Red) |
| SSC Exam Domain | `ssc.eduforge.in/login` | `#1B5E20` (Government Green) |
| RRB Exam Domain | `rrb.eduforge.in/login` | `#E65100` (Railway Orange) |
| Parent Portal | `parent.eduforge.in/login` | `#4A148C` (Purple) |
| Student Portal | `student.eduforge.in/login` | `#006064` (Teal) |
| B2B Partner | `partners.eduforge.in/login` | `#263238` (Dark Slate) |
| TSP | `[brand].testpro.in/login` | Operator-defined branding |

### Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  LEFT PANEL (40%)              │  RIGHT PANEL (60%)                │
│  Brand Panel                   │  Login Form Panel                 │
│                                │                                   │
│  ┌────────────────────────┐    │  ┌─────────────────────────────┐ │
│  │  [Institution Logo]    │    │  │  Welcome back                │ │
│  │                        │    │  │  [Portal Name]               │ │
│  │  "XYZ School"          │    │  │                              │ │
│  │  [City, State]         │    │  │  Enter your mobile number    │ │
│  │                        │    │  │  ┌──────────────────────┐   │ │
│  │  [Student Count badge] │    │  │  │ +91 │ [mobile input] │   │ │
│  │                        │    │  │  └──────────────────────┘   │ │
│  │  ━━━━━━━━━━━━━━━━━━━━  │    │  │                              │ │
│  │                        │    │  │  [Send OTP via WhatsApp]     │ │
│  │  Today's Stats         │    │  │                              │ │
│  │  Attendance: 94.2%     │    │  │  ── or ──                    │ │
│  │  Tests Today: 3        │    │  │                              │ │
│  │  New Students: 12      │    │  │  [Send via SMS instead]      │ │
│  │                        │    │  │                              │ │
│  │  [Powered by EduForge] │    │  │  ────────────────────────   │ │
│  └────────────────────────┘    │  │  First time here?            │ │
│                                │  │  [Register / Find Account]   │ │
│                                │  └─────────────────────────────┘ │
│                                │                                   │
│                                │  [© EduForge · Privacy · Terms]  │
└────────────────────────────────────────────────────────────────────┘
```

> **Mobile (< 768px):** Left panel hides. Only logo + portal name shown at top.
> Form takes full screen.

### Components

| Component | Type | Spec |
|---|---|---|
| Institution Logo | Image | 120×120px, rounded-12, fallback = EduForge logo |
| Portal name | H1 | Portal-specific title (e.g., "XYZ School — Staff Portal") |
| Today's Stats | 3-column stat tiles | Live data from API. Only for institution portals |
| Country code | Static badge | "+91" — Phase 1 India only. Expandable in Phase 2 |
| Mobile input | Input[tel] | maxlength=10, numeric keyboard on mobile, auto-advance |
| Send OTP WhatsApp | Primary Button | Green (#25D366), WhatsApp icon left |
| Send via SMS | Text link | Secondary, smaller — shown only after WhatsApp attempt |
| First time here | Text link | Opens registration or account-lookup flow |
| Privacy/Terms | Footer links | Opens modal overlay (no page navigation) |

### States & Validation

| State | Trigger | UI Response |
|---|---|---|
| Empty field | Focus away | No error yet |
| Invalid length | Submit with < 10 digits | Red border + "Enter valid 10-digit number" inline |
| Invalid number (starts with 0/1) | Submit | "Mobile must start with 6, 7, 8, or 9" |
| Loading — OTP sending | Submit valid number | Button shows spinner, text = "Sending..." |
| OTP sent | WhatsApp delivery confirmed | Navigate to Page 3 (OTP entry) |
| WhatsApp failed | Delivery failure | Auto-show "Didn't receive? Send via SMS" toast |
| Account not found | Mobile not in institution | Show alert: "Not enrolled in [Institution]. Contact your admin." |
| Account blocked | Flagged account | Show alert: "Your account has been suspended. Call 1800-XXX-XXXX" |
| Rate limit | 5+ failed attempts in 5 min | "Too many attempts. Try again in 15 minutes." with countdown |

### Alert Components

```
┌─────────────────────────────────────────────────────┐
│  ⚠️  Account not found                              │
│                                                     │
│  No account is linked to +91 98765 43210 in         │
│  XYZ School portal.                                 │
│                                                     │
│  Are you a student? → student.eduforge.in           │
│  Are you a parent?  → parent.eduforge.in            │
│  Wrong school?      → [Try another institution]     │
│                                                     │
│  [Try different number]              [Contact Admin]│
└─────────────────────────────────────────────────────┘
```

### Platform Admin Login — Special Rules

- URL: `admin.eduforge.in/login`
- Mobile must be in `platform_staff` table — not institution staff
- No "first time here" option — all accounts created by HR Manager
- After OTP: If access_level = 5 → Additional 2FA TOTP required (Google Authenticator)
- Session timeout: 8 hours (vs 7 days for regular users)
- Audit log entry created on every login attempt (success + fail)

---

## Page 3 — OTP Verification

### Route
`[portal-url]/verify-otp` (query param: `?channel=whatsapp|sms`)

### Purpose
Verify the one-time password delivered via WhatsApp or SMS. Secure, timed, with resend logic.

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                     [← Back to Login]                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │         [WhatsApp Icon / SMS Icon]                      │   │
│  │                                                         │   │
│  │    OTP sent to +91 98765 4XXXX                          │   │
│  │    via WhatsApp                                         │   │
│  │                                                         │   │
│  │    Enter 6-digit OTP                                    │   │
│  │                                                         │   │
│  │    ┌───┐ ┌───┐ ┌───┐   ┌───┐ ┌───┐ ┌───┐              │   │
│  │    │ _ │ │ _ │ │ _ │   │ _ │ │ _ │ │ _ │              │   │
│  │    └───┘ └───┘ └───┘   └───┘ └───┘ └───┘              │   │
│  │         [  Verify OTP  ]                                │   │
│  │                                                         │   │
│  │    ⏱ Expires in  02:47                                  │   │
│  │                                                         │   │
│  │    ─────────────────────────────────────                │   │
│  │                                                         │   │
│  │    Didn't receive it?                                   │   │
│  │    [Resend via WhatsApp] (active after 30s)             │   │
│  │    [Try SMS instead]                                    │   │
│  │    [Try a different number]                             │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### OTP Input Component — Detailed Spec

| Property | Value |
|---|---|
| Input type | 6 individual `<input type="text" maxlength="1">` in a flex row |
| Separator | Visual gap between box 3 and 4 (like Aadhaar format) |
| Auto-advance | After each digit entered, focus shifts to next box automatically |
| Paste support | Paste 6 digits → distributes across all boxes automatically |
| Backspace | Deletes current + moves focus to previous box |
| Keyboard | `inputmode="numeric"` — numeric keyboard on mobile |
| Auto-submit | When 6th digit entered → auto-trigger verify (no button click needed) |
| Active state | Box border = primary color, shadow glow |
| Filled state | Box background = light tint of primary color |
| Error state | All boxes turn red border + shake animation |
| Success state | All boxes turn green + checkmark animation before redirect |

### Timer Component

| Property | Value |
|---|---|
| Duration | 3 minutes (180 seconds) |
| Display | MM:SS countdown |
| Color change | Green (>60s) → Orange (30–60s) → Red (<30s) |
| On expire | OTP boxes disabled, "OTP expired" message, resend button activates |
| Progress ring | Circular progress indicator around timer (optional — desktop only) |

### Resend Logic

| Button | Enabled After | Max Sends | Behavior |
|---|---|---|---|
| Resend WhatsApp | 30 seconds | 3 per session | Generates new OTP, resets timer |
| Try SMS instead | Immediately (if WhatsApp) | 2 per session | Switches channel, sends OTP via MSG91 |
| Try different number | Always | — | Navigates back to login page |

### States & Error Handling

| State | Trigger | UI Response |
|---|---|---|
| Auto-submitted | All 6 digits filled | Loader overlay, verify API call |
| Wrong OTP | API returns 401 | Shake animation, red boxes, "Incorrect OTP. X attempts remaining" |
| Expired OTP | After 3 min | Boxes disabled, gray. "OTP expired. Request a new one." |
| Max attempts (3) | 3 wrong OTPs | Lock: "Too many wrong attempts. Request a new OTP." |
| Session lock (5 OTPs) | 5 OTPs in 30 min | "Account temporarily locked for 30 minutes." |
| Success | API returns 200 | Green animation → redirect to Page 4 or 5 |
| Network error | API timeout/500 | "Connection error. Check your internet." with retry button |

### Security Rules

- OTP is bcrypt-hashed in DB (never stored plain)
- Server-side: only 3 attempts per OTP code
- Server-side: only 5 OTP sends per mobile per 30 minutes
- OTP expires in 3 minutes from creation (not from send)
- Each new OTP invalidates all previous OTPs for that mobile
- All OTP events logged in `identity.otp_audit` table

---

## Page 4 — Role Selector (Multi-Role Users)

> Shown ONLY when: logged-in mobile is linked to 2+ roles across institutions.
> Example: A person who is both a Teacher at XYZ School AND a Faculty at ABC Coaching.

### Route
`[portal-url]/select-role`

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                   [EduForge Logo]                               │
│                                                                 │
│  You are registered in multiple portals.                        │
│  Choose where you want to go today.                             │
│                                                                 │
│  [Search bar: "Search institution or role..."]    [🔍]         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ PLATFORM                                                │   │
│  │                                                         │   │
│  │ ┌─────────────────────────────────────────────────┐    │   │
│  │ │ [EduForge Logo] Platform Admin Portal           │    │   │
│  │ │ Role: Content Director (Level 2)                │    │   │
│  │ │ Last login: Today 9:42 AM          [→ Go Here]  │    │   │
│  │ └─────────────────────────────────────────────────┘    │   │
│  │                                                         │   │
│  │ SCHOOLS                                                 │   │
│  │                                                         │   │
│  │ ┌─────────────────────────────────────────────────┐    │   │
│  │ │ [School Logo] XYZ Residential School, Hyd       │    │   │
│  │ │ Role: Mathematics Teacher, Class 11             │    │   │
│  │ │ Last login: Yesterday 4:15 PM      [→ Go Here]  │    │   │
│  │ └─────────────────────────────────────────────────┘    │   │
│  │                                                         │   │
│  │ ┌─────────────────────────────────────────────────┐    │   │
│  │ │ [School Logo] ABC Junior College, Vizag          │    │   │
│  │ │ Role: Physics HOD                               │    │   │
│  │ │ Last login: 3 days ago             [→ Go Here]  │    │   │
│  │ └─────────────────────────────────────────────────┘    │   │
│  │                                                         │   │
│  │ COACHING                                                │   │
│  │                                                         │   │
│  │ ┌─────────────────────────────────────────────────┐    │   │
│  │ │ [Coaching Logo] SR Nagar Coaching, Hyd          │    │   │
│  │ │ Role: Chemistry Faculty                         │    │   │
│  │ │ Last login: 1 week ago             [→ Go Here]  │    │   │
│  │ └─────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [Set a default portal for next login]                         │
└─────────────────────────────────────────────────────────────────┘
```

### Components

| Component | Type | Spec |
|---|---|---|
| Search bar | Input | Live filter of role cards as user types |
| Role cards | Card list | Grouped by institution type. Sorted: most recent first |
| Last login | Metadata | Relative time ("Today", "Yesterday", "3 days ago") |
| Go Here button | Primary | Opens that portal in same tab. Sets session for that portal |
| Set default | Checkbox | Saves preference — bypasses this page next time |
| Portal badge | Tag | Color-coded: Platform = Indigo, School = Blue, Coaching = Red |

### States

| State | Condition | Behavior |
|---|---|---|
| Only 1 role | User has single role only | Skip this page entirely, auto-redirect |
| All portals | User has 3+ portals | Full list, search enabled |
| Inactive portal | Subscription expired | Card shown grayed out with "Subscription expired" badge |
| Revoked access | Role removed by admin | Card shows "Access removed. Contact institution." — not clickable |

---

## Page 5 — First Login Profile Setup

> Shown ONLY on very first login (account created by institution, no profile yet).
> Multi-step wizard. Cannot skip steps 1–3. Step 4 optional.

### Route
`[portal-url]/setup-profile`

### Layout — Step Indicator

```
  ●━━━━━━━━○━━━━━━━━○━━━━━━━━○
 Step 1    Step 2   Step 3   Step 4
  Photo     Name    Email   Notif.
```

### Step 1 — Profile Photo

```
┌────────────────────────────────────────────────────┐
│  Add your profile photo                            │
│  (Used in your ID card, communications, reports)  │
│                                                    │
│           ┌───────────────┐                       │
│           │               │                       │
│           │   [Camera]    │                       │
│           │               │                       │
│           └───────────────┘                       │
│           128 × 128 px circle                     │
│                                                    │
│     [Upload Photo]   [Take a Selfie]              │
│                                                    │
│  Requirements:                                     │
│  ✅ Face clearly visible                          │
│  ✅ Plain background preferred                    │
│  ✅ JPG/PNG, max 5MB                              │
│                                                    │
│  [Skip for now — upload within 7 days]            │
│                          [Next →]                 │
└────────────────────────────────────────────────────┘
```

**Upload flow:**
- Click Upload → OS file picker (image/* only)
- Click Selfie → Access camera → Capture → Preview → Crop (circular)
- Crop tool: Draggable crop area, zoom slider, rotate button
- Preview: Shows how photo will appear on ID card
- Validation: Min 100×100px, max 5MB, JPG/PNG/WEBP
- Compression: Client-side compress to max 200KB before upload

### Step 2 — Name Confirmation

```
┌────────────────────────────────────────────────────┐
│  Confirm your name                                 │
│  (Pre-filled from institution records. Edit if    │
│   needed — changes require admin approval)        │
│                                                    │
│  First Name *                                      │
│  [Ravi Kumar              ]                        │
│                                                    │
│  Last Name *                                       │
│  [Sharma                  ]                        │
│                                                    │
│  Display Name (how others see you)                │
│  [Ravi Kumar Sharma        ]                       │
│  (auto-generated — editable)                      │
│                                                    │
│  Preferred Language *                              │
│  [English ▼]  options: English, Telugu, Hindi     │
│                                                    │
│  [← Back]                        [Next →]        │
└────────────────────────────────────────────────────┘
```

### Step 3 — Email Address

```
┌────────────────────────────────────────────────────┐
│  Add your email address                            │
│  (For certificates, invoices, important notices) │
│                                                    │
│  Email Address *                                   │
│  [ravikumar@gmail.com      ]                       │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │ 📧 We'll send a verification link.          │  │
│  │    Email is used for:                       │  │
│  │    • Rank certificates (PDF)                │  │
│  │    • Fee invoices                           │  │
│  │    • Important announcements                │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│  [← Back]                        [Next →]        │
└────────────────────────────────────────────────────┘
```

### Step 4 — Notification Preferences (Optional)

```
┌────────────────────────────────────────────────────┐
│  How should we notify you?                         │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │  [✅] WhatsApp alerts (recommended)         │  │
│  │       +91 98765 4XXXX — already linked      │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │  [✅] SMS — OTP and critical alerts only    │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │  [  ] Email — certificates and invoices     │  │
│  │       (add email in previous step first)    │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │  [✅] Push notifications (mobile app)       │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│  [← Back]                   [Complete Setup ✓]   │
└────────────────────────────────────────────────────┘
```

### Completion → Redirect to Home

```
┌─────────────────────────────────────────────────┐
│                                                 │
│     ✅  Profile setup complete!                 │
│                                                 │
│     Welcome to EduForge, Ravi Kumar.            │
│     Taking you to your dashboard...             │
│                                                 │
│     [████████████████░░░░░░]  75%               │
│                                                 │
└─────────────────────────────────────────────────┘
```

Auto-redirect after 2 seconds.

---

## Page 6 — Platform Admin 2FA (Group 1 Super Admins Only)

> Required for access_level = 4 or 5 on admin.eduforge.in.
> Standard OTP is step 1. TOTP app is step 2.

### Route
`admin.eduforge.in/2fa`

### Layout

```
┌────────────────────────────────────────────────────┐
│                                                    │
│        [EduForge Shield Logo]                      │
│                                                    │
│   Two-Factor Authentication Required               │
│                                                    │
│   Open your authenticator app and enter           │
│   the 6-digit code shown for EduForge Admin.      │
│                                                    │
│   ┌────────────────────────────────┐              │
│   │  [  ] [  ] [  ] – [  ] [  ] [  ] │            │
│   └────────────────────────────────┘              │
│                                                    │
│              [Verify Code]                         │
│                                                    │
│   ─────────────────────────────────────           │
│                                                    │
│   Lost your authenticator?                        │
│   [Use backup recovery code]                      │
│   [Contact Security Team]                         │
│                                                    │
│   This session will expire in 8 hours.            │
└────────────────────────────────────────────────────┘
```

### Rules

| Rule | Detail |
|---|---|
| TOTP window | ±30 second window (standard TOTP) |
| Max attempts | 5 wrong codes → account lock, security alert sent |
| Recovery codes | 8 single-use codes, generated at setup, stored hashed |
| Session | 2FA session = 8 hours; OTP session alone = invalid for Level 4/5 |
| Bypass | No bypass. Even CEO must 2FA. |
| Failed login audit | Every failed 2FA attempt logged with IP, device, timestamp |

---

## Page 7 — Session Expired / Re-Authentication

> Shown when JWT access token expires mid-session.
> Avoids losing unsaved work.

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │   [Lock Icon]   Your session has expired               │   │
│  │                                                        │   │
│  │   You've been inactive for 8 hours.                    │   │
│  │   Please verify your identity to continue.             │   │
│  │                                                        │   │
│  │   Logged in as: Ravi Kumar (+91 98765 4XXXX)           │   │
│  │                                                        │   │
│  │   [Send OTP to verify — WhatsApp]                      │   │
│  │                                                        │   │
│  │   ── or ──                                             │   │
│  │                                                        │   │
│  │   [Log out and start fresh]                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Note: Any unsaved changes on the previous page may be lost.   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Session Timeout Rules

| Role Level | Access Token | Refresh Window | Re-auth behavior |
|---|---|---|---|
| Level 0–2 | 7 days | 30 days | Mobile OTP re-verify |
| Level 3 | 24 hours | 7 days | Mobile OTP re-verify |
| Level 4 | 8 hours | 24 hours | OTP + 2FA (Group 1) |
| Level 5 | 8 hours | 24 hours | OTP + 2FA always |
| Exam Day (active test) | Never expires mid-exam | N/A | Protected by exam token |

---

## Page 8 — Account Blocked / Suspended

### Route
`[portal-url]/account-blocked`

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │   [⛔ Red Shield Icon]                                  │   │
│  │                                                        │   │
│  │   Account Suspended                                    │   │
│  │                                                        │   │
│  │   Your account has been temporarily suspended.         │   │
│  │                                                        │   │
│  │   Reason: [shown if not sensitive]                     │   │
│  │   Suspended by: [Institution Admin / Platform Admin]   │   │
│  │   Suspended on: [Date and time]                        │   │
│  │                                                        │   │
│  │   To restore access:                                   │   │
│  │   • Contact your institution admin, OR                 │   │
│  │   • Call EduForge Support: 1800-XXX-XXXX               │   │
│  │   • Email: support@eduforge.in                         │   │
│  │                                                        │   │
│  │   [Copy Reference ID: EF-2024-BLK-098765]             │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Page 9 — Logout Confirmation

> Triggered by clicking "Log Out" in any portal.

### Modal (not a full page)

```
┌───────────────────────────────────────┐
│                                       │
│   Log out of [Portal Name]?           │
│                                       │
│   You will need to verify your OTP    │
│   to log back in.                     │
│                                       │
│   ┌──────────────────────────────┐   │
│   │  ⚠️ You have 1 unsaved form  │   │
│   │     Your changes will be lost│   │
│   └──────────────────────────────┘   │
│   (shown only if unsaved changes)     │
│                                       │
│   [Cancel]      [Log Out Anyway]      │
│                                       │
└───────────────────────────────────────┘
```

### On Confirm Logout

1. Invalidate JWT refresh token on server (add to blocklist in DB)
2. Clear local storage / cookies for this subdomain only
3. Redirect to portal login page
4. Show success toast: "You've been logged out successfully"

---

## Page 10 — Self Registration (Exam Domain / TSP Only)

> Platform staff (Group 1) and institution staff CANNOT self-register.
> Accounts created by admins only for those groups.
> Self-registration is ONLY for: Exam Domain (Group 6), Student Portal (Group 10), Parent Portal (Group 8).

### Route
`ssc.eduforge.in/register` / `student.eduforge.in/register`

### Layout

```
┌────────────────────────────────────────────────────┐
│  [Domain Logo]   SSC CGL · RRB NTPC · UPSC        │
│                                                    │
│  Create your free account                          │
│                                                    │
│  Full Name *                                       │
│  [___________________________]                     │
│                                                    │
│  Mobile Number *                                   │
│  [+91 ___________]                                 │
│                                                    │
│  Date of Birth *  (Age verification — must be 18+)│
│  [DD] / [MM] / [YYYY]                              │
│                                                    │
│  State *                                           │
│  [Andhra Pradesh ▼]                                │
│                                                    │
│  I am preparing for: (multi-select)                │
│  [✅] SSC CGL    [  ] SSC CHSL   [  ] RRB NTPC    │
│  [  ] UPSC       [  ] Banking    [  ] State PSC   │
│                                                    │
│  [Create Account — Free]                           │
│                                                    │
│  Already have an account? [Log In]                 │
│                                                    │
│  ──────────────────────────────────────           │
│  By creating an account, you agree to EduForge's  │
│  [Terms of Service] and [Privacy Policy]          │
│  DPDP Act 2023 compliant — your data is safe.     │
└────────────────────────────────────────────────────┘
```

### Post-Registration Flow

1. Mobile OTP verification (same as Page 3)
2. Account created in `identity.users` table
3. Role assigned: `exam_domain_student_free` (access_level S4)
4. Welcome WhatsApp message sent
5. Redirect to student dashboard with onboarding checklist

---

## Auth Flow Summary — Decision Tree

```
User visits portal URL
         │
         ▼
Already has valid JWT?
    │           │
   YES          NO
    │           │
    ▼           ▼
  Direct    Show Login Page (Page 2)
 to Home         │
                 ▼
           Enter Mobile
                 │
                 ▼
         Mobile in DB?
          │         │
         NO         YES
          │          │
          ▼          ▼
      Show alert  Send OTP (WhatsApp)
     / register        │
                       ▼
                  OTP Page (Page 3)
                       │
                       ▼
                  OTP correct?
                  │         │
                 NO         YES
                  │          │
                  ▼          ▼
            Retry / Lock  First login?
                          │        │
                         YES       NO
                          │         │
                          ▼         ▼
                    Profile    Multiple roles?
                    Setup       │         │
                   (Page 5)    NO        YES
                                │         │
                                ▼         ▼
                           Direct to  Role Selector
                             Home      (Page 4)
                                          │
                                          ▼
                                     Selected role
                                          │
                                          ▼
                                     Go to Home
```

---

## Global Auth Design System

### Typography

| Element | Font | Size | Weight |
|---|---|---|---|
| Page title | Inter | 28px | 700 |
| Form labels | Inter | 14px | 500 |
| Input text | Inter | 16px | 400 |
| Helper text | Inter | 12px | 400 |
| Error text | Inter | 12px | 500 |
| Button text | Inter | 15px | 600 |

### Colors (Auth Pages)

| Token | Value | Usage |
|---|---|---|
| `--primary` | Portal-specific | Main buttons, active states |
| `--error` | `#D32F2F` | All error states, invalid inputs |
| `--warning` | `#F57F17` | Warnings (e.g., "3 attempts left") |
| `--success` | `#2E7D32` | OTP verified, setup complete |
| `--surface` | `#FFFFFF` | Card backgrounds |
| `--on-surface` | `#1C1B1F` | Primary text |
| `--outline` | `#79747E` | Input borders default |
| `--outline-focus` | `--primary` | Input border on focus |

### Spacing

| Token | Value | Usage |
|---|---|---|
| `--radius-sm` | `8px` | Input fields, small cards |
| `--radius-md` | `12px` | Cards, modals |
| `--radius-lg` | `16px` | Role cards |
| `--radius-full` | `9999px` | Buttons (pill style) |
| `--shadow-card` | `0 2px 8px rgba(0,0,0,0.12)` | Login form card |
| `--shadow-modal` | `0 8px 32px rgba(0,0,0,0.24)` | Role selector |

### Accessibility

| Requirement | Implementation |
|---|---|
| Keyboard navigation | Tab order: Logo → Role dropdown → Mobile → Submit |
| Screen reader | All inputs have `aria-label`. Error messages use `aria-live="polite"` |
| Contrast | Minimum 4.5:1 for body text, 3:1 for large text |
| Focus visible | `2px solid --primary` outline always visible on keyboard focus |
| OTP boxes | Each box has `aria-label="OTP digit 1 of 6"` |
| Animations | `prefers-reduced-motion` disables shake/transition animations |
| Touch targets | Minimum 44×44px for all interactive elements |

### Responsive Breakpoints

| Breakpoint | Width | Layout Change |
|---|---|---|
| Mobile | < 480px | Single column, full-width inputs |
| Tablet | 480–768px | Single column, 480px max-width centered form |
| Desktop-S | 768–1024px | Left brand panel visible at 35% |
| Desktop-L | > 1024px | Left brand panel at 40%, login form 60% |

---

## API Endpoints Used in Auth Pages

| Page | Action | Endpoint | Method |
|---|---|---|---|
| Page 1/2 | Lookup mobile | `/api/v1/auth/lookup` | POST |
| Page 2 | Send OTP | `/api/v1/auth/otp/send` | POST |
| Page 3 | Verify OTP | `/api/v1/auth/otp/verify` | POST |
| Page 3 | Resend OTP | `/api/v1/auth/otp/resend` | POST |
| Page 5 | Save profile | `/api/v1/user/profile/setup` | POST |
| Page 5 | Upload photo | `/api/v1/user/profile/photo` | POST |
| All | Refresh token | `/api/v1/auth/token/refresh` | POST |
| All | Logout | `/api/v1/auth/logout` | POST |
| 2FA | Verify TOTP | `/api/v1/auth/2fa/verify` | POST |

---

## Security Checklist (Auth Pages)

| Check | Implementation |
|---|---|
| CSRF | SameSite=Strict cookie, CSRF token in forms |
| XSS | All user inputs sanitized, CSP headers |
| Rate limiting | 5 OTP sends/30min, 3 verify attempts/OTP, IP-based throttle |
| HTTPS | TLS 1.3 only. HSTS with includeSubDomains |
| Audit logging | Every login attempt (success+fail) logged with IP, UA, timestamp |
| Mobile masking | Display as `+91 98765 4XXXX` — last 5 digits shown only |
| Token storage | Access token: memory only. Refresh token: HttpOnly cookie |
| Session isolation | Each subdomain is isolated — cross-subdomain SSO requires explicit flow |
