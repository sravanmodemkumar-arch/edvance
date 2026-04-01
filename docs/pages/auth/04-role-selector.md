# Page: Role Selector
**Route:** `[portal-url]/select-role`
**Auth Stage:** 3 of 5 (conditional)
**Access:** Shown ONLY when authenticated user has 2+ roles across portals
**Previous:** [03-otp-verification.md](03-otp-verification.md)
**Next:** Home page of selected portal

---

## Overview

| Property | Value |
|---|---|
| Purpose | Let user pick which portal/role to enter when they have multiple |
| Trigger | User's mobile number is linked to 2+ active roles across institutions |
| Skip condition | Single role → this page is bypassed entirely |
| URL entry point | `admin.eduforge.in/login` or any portal → redirects here if multi-role |

---

## Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Page Header | Logo, "you are registered in multiple portals" message |
| 2 | Search Bar | Live filter of role cards |
| 3 | Role Cards List | Grouped list of all portals/roles for this mobile number |
| 4 | Footer Strip | "Set as default" + Privacy/Terms |

---

## Section 1 — Page Header

| Element | Type | Spec |
|---|---|---|
| Logo | EduForge logo | 40px height, centered on mobile, left-aligned on desktop |
| Headline | H1 | "You are registered in multiple portals." |
| Sub-text | Body | "Choose where you want to go today." |
| Greeting | Personalized | "Welcome back, [First Name]." — above headline |
| User avatar | 48px circle | Top-right corner. Shows user's photo or initials. |
| Page layout | Card-based | Max-width 640px, centered. No sidebar. Auth layout. |

---

## Section 2 — Search Bar

| Element | Type | Spec |
|---|---|---|
| Search input | Text input | Placeholder: "Search institution or role..." |
| Search icon | [🔍] | Left inside input |
| Clear button | [✕] | Appears when text entered |
| Live filter | Behavior | Filters role cards in real-time as user types. Searches: institution name, city, role title. |
| No results | Empty state | "No portals match '[search]'. [Clear search]" |

---

## Section 3 — Role Cards List

### Grouping
Cards are grouped by institution type with section headers:

```
PLATFORM                          ← Group 1
SCHOOL                            ← Group 3
COLLEGE                           ← Group 4
COACHING                          ← Group 5
EXAM DOMAINS                      ← Group 6
PARENTS                           ← Group 8
```

### Role Card Layout

```
┌─────────────────────────────────────────────────────────┐
│  [Logo 48px]  XYZ Residential School, Hyderabad         │
│               Mathematics Teacher — Class 11 & 12       │
│               Last login: Today 9:42 AM          [→]   │
└─────────────────────────────────────────────────────────┘
```

| Element | Type | Spec |
|---|---|---|
| Logo | 48×48px image | Institution logo with rounded-8. Fallback = initials colored circle. |
| Institution name | Title | Bold, 16px. Max 1 line with ellipsis. |
| City | Subtitle | Muted, 13px. After institution name on same line or below. |
| Role title | Role text | 14px, `--on-surface-variant`. E.g., "Mathematics Teacher" |
| Role scope | Sub-role | 13px, muted. E.g., "Class 11 & 12" or "JEE Batch". |
| Last login | Timestamp | Right-aligned. Relative: "Today 9:42 AM", "Yesterday", "3 days ago", "Never". |
| Go arrow [→] | Primary button | Pill shaped. "Go Here" text on desktop. Arrow icon only on mobile. |
| Card border | Default | 1px `--outline-variant` |
| Card hover | Hover | Border → `--primary`. Shadow lifts. |
| Card active | Clicking | Brief scale(0.99) press effect |

### Card Status Variants

| Status | Visual Change | Reason |
|---|---|---|
| Active (default) | Full color, clickable | Normal active role |
| Subscription expired | Grayed out 60%. Badge: "Subscription expired" | Institution's plan lapsed |
| Access revoked | Grayed out. Badge: "Access removed". Not clickable. | Admin removed this role |
| BGV pending | Orange warning dot on logo. | Staff role — BGV not completed |
| Currently active session | Green dot on logo. Badge: "Active session" | User already logged in there |

### Sort Order
1. Most recently accessed portals first
2. Never-logged portals at bottom
3. Inactive/expired portals always last

---

## Section 4 — Footer Strip

| Element | Type | Spec |
|---|---|---|
| Default portal toggle | Checkbox | "Remember my choice — go here directly next time" |
| Default portal info | Helper text | "You can change this anytime in your Profile settings" |
| Divider | Horizontal line | |
| Privacy / Terms | Links | Same as login page — open in modal |

### Set as Default Behavior
- When checked: saves `{mobile, portal_slug}` preference to `identity.user_preferences`
- Next login: After OTP verification, skip this page → go directly to default portal
- Override: User can still visit this page via Profile → "Switch Portal"

---

## States

| State | Condition | Behavior |
|---|---|---|
| Loading | Page first loads | Skeleton cards (3–5 shimmer cards) while API fetches |
| All portals active | Normal | Full list, sorted by recency |
| Only 1 active portal | Others expired | Still show page with 1 card + note about expired ones |
| All portals expired | Subscription lapsed | Show message: "Your portal subscriptions have expired. Contact your admin." |
| No roles found | Error state | "Something went wrong. Try logging in again." [Back to Login] |

---

## API Calls

| Action | Endpoint | Method | Response |
|---|---|---|---|
| Fetch user portals | `/api/v1/auth/portals` | GET | Array of: `{portal_slug, role, institution_name, logo_url, last_login, status}` |
| Select portal | `/api/v1/auth/session/start` | POST | `{portal_slug}` → JWT scoped to that portal |
| Save default portal | `/api/v1/user/preferences/default-portal` | POST | `{portal_slug}` |
