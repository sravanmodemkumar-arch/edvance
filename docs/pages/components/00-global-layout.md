# Component: Global App Shell Layout

> This file is the single source of truth for the application shell — the persistent structural frame
> that wraps every page across every portal in EduForge. It defines how the top navigation,
> sidebar, content area, and overlay layers are assembled, how they respond to screen sizes,
> and how they behave during critical states like live exams, active incidents, and maintenance.
> Every page spec in every group references this file for layout — nothing is re-documented per page.

---

## What Is the App Shell?

The App Shell is the permanent chrome surrounding every page. It loads once at login and persists
across all navigation — only the content area re-renders on route change. This means:
- The sidebar never flickers when navigating
- Notifications are always visible
- Live exam alerts persist regardless of which page you are on
- The command palette (⌘K) is always one keystroke away

The shell is portal-aware: the same structural layout is used across all 11 portals, but the
color scheme, sidebar items, branding, and navigation links change based on the portal context.

---

## Portal Identity Map

> Each portal has a distinct visual identity anchored to its primary color. The shell reads the
> portal context from the JWT and applies the correct theme on load — no flash of wrong color.

| Portal | Audience | Primary Color | Theme Mode | Sidebar Style |
|---|---|---|---|---|
| `admin.eduforge.in` | EduForge Staff (81 roles) | Indigo `#6366F1` | Dark | Dense data sidebar |
| `school.eduforge.in` | School admin staff | Blue `#1565C0` | Light | Icon + label |
| `college.eduforge.in` | College admin staff | Indigo `#283593` | Light | Icon + label |
| `coaching.eduforge.in` | Coaching centre staff | Red `#B71C1C` | Light | Icon + label |
| `student.eduforge.in` | Students | Teal `#006064` | Light | Bottom tab nav |
| `parent.eduforge.in` | Parents | Purple `#4A148C` | Light | Minimal |
| `ssc.eduforge.in` | SSC exam candidates | Green `#1B5E20` | Light | Icon + label |
| `rrb.eduforge.in` | RRB exam candidates | Orange `#E65100` | Light | Icon + label |
| `upsc.eduforge.in` | UPSC candidates | Purple `#4A148C` | Light | Icon + label |
| `banking.eduforge.in` | Banking exam candidates | Teal `#004D40` | Light | Icon + label |
| `[slug].eduforge.in` | Institution-specific | Custom | Custom | Custom |

> **This document primarily specs the Admin Portal (`admin.eduforge.in`) dark theme.**
> All other portals use the same structural layout with their respective light themes.

---

## Admin Portal — Dark Theme Design System

> The admin portal uses a dark-first design because EduForge staff work long hours in
> operations centers and support desks. Dark backgrounds reduce eye strain during extended
> sessions, improve contrast for data-dense tables, and give the platform a premium,
> professional appearance that signals the gravity of managing 25 lakh student records.

### Color Tokens — Admin Dark Theme

```css
/* ── Core Background Surfaces ── */
--bg-base:          #070C18;   /* Deepest background — page root */
--bg-surface-1:     #0D1526;   /* Primary card/panel background */
--bg-surface-2:     #141F35;   /* Elevated panel, sidebar hover */
--bg-surface-3:     #1C2A42;   /* Drawers, modals, tooltips */
--bg-surface-4:     #243350;   /* Selected row, active states */

/* ── Borders & Dividers ── */
--border-subtle:    #1E2D45;   /* Hairline dividers, table row borders */
--border-default:   #263954;   /* Card borders, input borders */
--border-strong:    #2E4468;   /* Focused input, active panel border */
--border-accent:    rgba(99,102,241,0.35);  /* Indigo-tinted hover borders */

/* ── Primary Brand — Indigo ── */
--primary:          #6366F1;   /* Primary CTA, active nav item */
--primary-hover:    #818CF8;   /* Hover state for primary elements */
--primary-muted:    rgba(99,102,241,0.15);  /* Tinted backgrounds, selection */
--primary-dim:      rgba(99,102,241,0.08);  /* Subtle tint for rows */

/* ── Semantic Status Colors ── */
--status-success:   #10B981;   /* Emerald — healthy, passing, GO */
--status-success-bg:rgba(16,185,129,0.12);
--status-warning:   #F59E0B;   /* Amber — caution, pending, expiring */
--status-warning-bg:rgba(245,158,11,0.12);
--status-error:     #EF4444;   /* Red — critical, failing, NO-GO */
--status-error-bg:  rgba(239,68,68,0.12);
--status-info:      #3B82F6;   /* Blue — informational, in progress */
--status-info-bg:   rgba(59,130,246,0.12);
--status-neutral:   #94A3B8;   /* Gray — inactive, archived */
--status-neutral-bg:rgba(148,163,184,0.10);

/* ── Text ── */
--text-primary:     #F0F4FF;   /* Primary readable text */
--text-secondary:   #94A3B8;   /* Secondary labels, metadata */
--text-muted:       #5B6B8A;   /* Placeholder, disabled, timestamps */
--text-accent:      #818CF8;   /* Indigo-tinted links and highlights */
--text-inverse:     #0D1526;   /* Text on light backgrounds */

/* ── Data / Metrics ── */
--data-font:        'JetBrains Mono', monospace;
--data-positive:    #34D399;   /* ↑ positive trends */
--data-negative:    #F87171;   /* ↓ negative trends */
--data-neutral:     #94A3B8;   /* — flat trends */

/* ── Live / Real-time ── */
--live-pulse:       #10B981;   /* Pulsing dot for live data */
--live-critical:    #EF4444;   /* Red pulse for live emergency */
--live-warning:     #F59E0B;   /* Amber pulse for live warning */

/* ── Gradients ── */
--gradient-primary: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
--gradient-success: linear-gradient(135deg, #059669 0%, #10B981 100%);
--gradient-danger:  linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
--gradient-surface: linear-gradient(180deg, #0D1526 0%, #070C18 100%);
--gradient-hero:    linear-gradient(135deg, rgba(99,102,241,0.15) 0%, transparent 60%);
```

---

## Admin Portal — Light Theme Design System

> The light theme is the secondary option for the admin portal. It is provided for
> executives who prefer working in bright environments, for presentations on projectors,
> and for accessibility use cases where dark backgrounds cause visual difficulty.
> The same structural layout is used — only the color tokens change. Switching themes
> applies instantly via CSS custom property swap — no page reload required.

### Color Tokens — Admin Light Theme

```css
/* ── Core Background Surfaces ── */
--bg-base:          #F8FAFC;   /* Page root background */
--bg-surface-1:     #FFFFFF;   /* Primary card/panel background */
--bg-surface-2:     #F1F5F9;   /* Elevated panel, sidebar hover */
--bg-surface-3:     #E2E8F0;   /* Drawers, modals, secondary panels */
--bg-surface-4:     #CBD5E1;   /* Selected state, active elements */

/* ── Borders & Dividers ── */
--border-subtle:    #E2E8F0;   /* Hairline dividers */
--border-default:   #CBD5E1;   /* Card borders, input borders */
--border-strong:    #94A3B8;   /* Focused input, active panel border */
--border-accent:    rgba(99,102,241,0.40);  /* Indigo-tinted hover borders */

/* ── Primary Brand — Indigo ── */
--primary:          #4F46E5;   /* Primary CTA (slightly darker for light bg contrast) */
--primary-hover:    #4338CA;   /* Hover state */
--primary-muted:    rgba(99,102,241,0.10);  /* Tinted backgrounds */
--primary-dim:      rgba(99,102,241,0.05);  /* Very subtle row tint */

/* ── Semantic Status Colors ── */
--status-success:   #059669;   /* Darker emerald for light theme contrast */
--status-success-bg:#D1FAE5;
--status-warning:   #D97706;   /* Darker amber */
--status-warning-bg:#FEF3C7;
--status-error:     #DC2626;   /* Darker red */
--status-error-bg:  #FEE2E2;
--status-info:      #2563EB;   /* Darker blue */
--status-info-bg:   #DBEAFE;
--status-neutral:   #64748B;   /* Darker gray */
--status-neutral-bg:#F1F5F9;

/* ── Text ── */
--text-primary:     #0F172A;   /* Primary readable text */
--text-secondary:   #475569;   /* Secondary labels, metadata */
--text-muted:       #94A3B8;   /* Placeholder, disabled, timestamps */
--text-accent:      #4F46E5;   /* Indigo links and highlights */
--text-inverse:     #F8FAFC;   /* Text on dark/colored backgrounds */

/* ── Data / Metrics ── */
--data-font:        'JetBrains Mono', monospace;
--data-positive:    #059669;   /* ↑ positive trends */
--data-negative:    #DC2626;   /* ↓ negative trends */
--data-neutral:     #64748B;   /* — flat trends */

/* ── Gradients ── */
--gradient-primary: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
--gradient-success: linear-gradient(135deg, #047857 0%, #059669 100%);
--gradient-danger:  linear-gradient(135deg, #B91C1C 0%, #DC2626 100%);
--gradient-surface: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
--gradient-hero:    linear-gradient(135deg, rgba(99,102,241,0.08) 0%, transparent 60%);
```

### Elevation — Light Theme

```css
/* ── Shadows use standard drop-shadow approach on light backgrounds ── */
--shadow-sm:   0 1px 3px rgba(15,23,42,0.08), 0 1px 2px rgba(15,23,42,0.04);
--shadow-md:   0 4px 12px rgba(15,23,42,0.10), 0 2px 4px rgba(15,23,42,0.06);
--shadow-lg:   0 10px 30px rgba(15,23,42,0.12), 0 4px 8px rgba(15,23,42,0.06);
--shadow-xl:   0 20px 60px rgba(15,23,42,0.16);
--shadow-glow-primary:  0 0 0 3px rgba(99,102,241,0.20);
--shadow-glow-success:  0 0 0 3px rgba(16,185,129,0.20);
--shadow-glow-error:    0 0 0 3px rgba(239,68,68,0.20);
```

---

## Theme Switching System

> Themes are applied via a `data-theme` attribute on the `<html>` element.
> All CSS custom properties are scoped to `[data-theme="dark"]` and `[data-theme="light"]`.
> The switch is instant — no page reload, no flash. Theme preference is stored in
> both localStorage (immediate) and the user's server-side profile (persistent across devices).

### Implementation

```css
/* Default: dark theme */
:root {
  --bg-base:       #070C18;
  --bg-surface-1:  #0D1526;
  /* ... all dark tokens ... */
}

/* Light theme override */
[data-theme="light"] {
  --bg-base:       #F8FAFC;
  --bg-surface-1:  #FFFFFF;
  /* ... all light tokens ... */
}

/* System preference fallback (if no explicit choice) */
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    --bg-base:       #F8FAFC;
    --bg-surface-1:  #FFFFFF;
    /* ... all light tokens ... */
  }
}
```

### Theme Toggle in Profile Menu

```
┌──────────────────────────────────────────────┐
│  [🎨] Theme                                  │
│                                              │
│  (●) Dark    ○  Light    ○  System           │
│                                              │
│  Dark    — Deep navy, easy on eyes           │
│  Light   — Clean white, presentation-ready  │
│  System  — Follows OS preference             │
└──────────────────────────────────────────────┘
```

| Option | Token set used | Best for |
|---|---|---|
| Dark | Dark theme tokens | Extended use, operations centers, night |
| Light | Light theme tokens | Presentations, bright environments, print |
| System | Follows `prefers-color-scheme` | Automatic based on OS/device setting |

### Component Appearance by Theme

> Every component in the design system uses only CSS custom property tokens — never
> hardcoded hex values. This means all components automatically switch themes with zero
> additional code. The table below shows how key elements appear in each theme.

| Element | Dark Theme | Light Theme |
|---|---|---|
| Page background | `#070C18` (deep navy) | `#F8FAFC` (near-white) |
| Card background | `#0D1526` with indigo border | `#FFFFFF` with gray border |
| Primary button | `#6366F1` fill, white text | `#4F46E5` fill, white text |
| Table row hover | `#141F35` | `#F1F5F9` |
| Table row selected | `#1C2A42` | `#EEF2FF` (indigo tint) |
| Sidebar | `#0D1526` | `#FFFFFF` with border |
| Top bar | `rgba(7,12,24,0.85)` blur | `rgba(255,255,255,0.90)` blur |
| Input field | `#141F35` bg, `#1E2D45` border | `#FFFFFF` bg, `#CBD5E1` border |
| Badge (success) | `#10B981` text, `rgba(16,185,129,0.12)` bg | `#059669` text, `#D1FAE5` bg |
| Badge (error) | `#EF4444` text, `rgba(239,68,68,0.12)` bg | `#DC2626` text, `#FEE2E2` bg |
| Chart grid lines | `#1E2D45` | `#E2E8F0` |
| Data text | `#F0F4FF` (JetBrains Mono) | `#0F172A` (JetBrains Mono) |

---

### Typography — Admin Portal

```css
/* ── Font Stack ── */
--font-ui:    'Inter', system-ui, -apple-system, sans-serif;
--font-data:  'JetBrains Mono', 'Fira Code', monospace;  /* All metric values */
--font-brand: 'Inter', sans-serif;

/* ── Scale ── */
--text-2xs:  10px / 400;  /* Micro labels, badge counts */
--text-xs:   11px / 400;  /* Timestamps, captions */
--text-sm:   12px / 400;  /* Table cell data, helper text */
--text-base: 14px / 400;  /* Body text, form labels */
--text-md:   15px / 500;  /* Section sub-headers */
--text-lg:   18px / 600;  /* Card headings, drawer titles */
--text-xl:   22px / 700;  /* Page headings, H2 */
--text-2xl:  28px / 700;  /* Page titles, H1 */
--text-3xl:  36px / 700;  /* Hero metrics, KPI values */
--text-4xl:  48px / 700;  /* Full-screen countdowns (exam timer) */

/* ── Data values always use JetBrains Mono ── */
/* e.g. 74,320 students, 99.94% uptime, ₹2.47 Cr — always mono for readability */
```

### Elevation & Depth

```css
/* ── Shadows for dark theme (lighter glow-style, not heavy drop shadows) ── */
--shadow-sm:   0 1px 3px rgba(0,0,0,0.4), 0 1px 2px rgba(0,0,0,0.3);
--shadow-md:   0 4px 12px rgba(0,0,0,0.4), 0 2px 4px rgba(0,0,0,0.3);
--shadow-lg:   0 10px 30px rgba(0,0,0,0.5), 0 4px 8px rgba(0,0,0,0.3);
--shadow-xl:   0 20px 60px rgba(0,0,0,0.6);
--shadow-glow-primary:  0 0 20px rgba(99,102,241,0.25);   /* Indigo glow on focus */
--shadow-glow-success:  0 0 20px rgba(16,185,129,0.20);   /* Green glow on GO state */
--shadow-glow-error:    0 0 20px rgba(239,68,68,0.25);    /* Red glow on critical state */
```

### Border Radius

```css
--radius-xs:    4px;    /* Badges, chips, small tags */
--radius-sm:    6px;    /* Input fields, small buttons */
--radius-md:    10px;   /* Cards, dropdowns */
--radius-lg:    14px;   /* Large cards, panels */
--radius-xl:    20px;   /* Drawers, modals */
--radius-2xl:   28px;   /* Full command palette, bottom sheets */
--radius-full:  9999px; /* Pills, avatars, toggle switches */
```

---

## Global Layout Structure

> The layout is a CSS Grid shell: a fixed top bar (56px), a fixed left sidebar (variable width),
> and a fluid main content area. Drawers and modals layer on top via z-index. The shell never
> scrolls — only the content area scrolls. This ensures the navigation and alerts are always
> visible regardless of how long the page content is.

### Desktop Layout (≥1024px)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  TOP BAR  (fixed, 56px, z-index: 200, backdrop-blur: 20px)                     │
│  ┌─────────────┬────────────────────────────────────────┬─────────────────────┐ │
│  │ 🔷 EduForge │  [⌘K  Search anything...]              │ [ENV] [🔔] [⚡] [👤]│ │
│  └─────────────┴────────────────────────────────────────┴─────────────────────┘ │
├──────────┬──────────────────────────────────────────────────────────────────────┤
│          │                                                                       │
│ SIDEBAR  │  CONTENT AREA (scrollable)                                           │
│ (fixed)  │  ┌─────────────────────────────────────────────────────────────────┐ │
│          │  │  CRITICAL ALERT BANNER (when active — sticky within content)    │ │
│ 240px    │  ├─────────────────────────────────────────────────────────────────┤ │
│ expanded │  │  BREADCRUMB  +  PAGE HEADER  +  PAGE ACTIONS                    │ │
│          │  ├─────────────────────────────────────────────────────────────────┤ │
│ 64px     │  │                                                                  │ │
│ collapsed│  │  PAGE CONTENT                                                    │ │
│          │  │  (each page defines its own layout within this zone)            │ │
│          │  │                                                                  │ │
│          │  │                                                                  │ │
│          │  └─────────────────────────────────────────────────────────────────┘ │
└──────────┴──────────────────────────────────────────────────────────────────────┘
```

### Tablet Layout (768px–1023px)

```
┌─────────────────────────────────────────────────────────┐
│  TOP BAR  (56px)                                        │
│  [☰] [🔷] [⌘K Search...]          [🔔] [⚡] [👤]      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CONTENT AREA (full width, sidebar hidden by default)   │
│  Sidebar opens as overlay on ☰ tap (320px wide)         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Mobile Layout (<768px)

```
┌───────────────────────────────┐
│  TOP BAR (48px)               │
│  [☰] [🔷]           [🔔] [👤]│
├───────────────────────────────┤
│                               │
│  CONTENT AREA                 │
│  (full width, single column)  │
│                               │
├───────────────────────────────┤
│  BOTTOM NAV (56px, fixed)     │
│  [🏠] [📊] [🔔] [⚙] [👤]    │
└───────────────────────────────┘
```

---

## Section A — Top Navigation Bar

> The top navigation bar is the most persistent and most-read element on the screen.
> It is always visible, always responsive, and carries three critical responsibilities:
> (1) brand identity and portal context, (2) global search via command palette, and
> (3) real-time alerts and user state. It uses backdrop-blur so page content scrolling
> beneath it is visible but does not compete with the navigation content.

### Anatomy

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ bg: rgba(7,12,24,0.85) · backdrop-filter: blur(20px) · border-bottom: 1px solid  │
│ var(--border-subtle) · height: 56px · position: fixed · top: 0 · z-index: 200    │
│                                                                                   │
│ ┌──────────────────┐ ┌───────────────────────────────┐ ┌───────────────────────┐ │
│ │  BRAND ZONE      │ │  SEARCH ZONE                  │ │  ACTION ZONE          │ │
│ │  width: 240px    │ │  flex: 1, max-width: 640px     │ │  width: auto          │ │
│ │  (matches sidebar│ │                               │ │                       │ │
│ │  width exactly)  │ │                               │ │                       │ │
│ └──────────────────┘ └───────────────────────────────┘ └───────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Brand Zone (left, 240px)

> The brand zone is sized to exactly match the sidebar width, creating a visually aligned
> left column. When the sidebar collapses to 64px, the brand zone also collapses to show
> only the logomark. The portal label under the logo changes based on portal context.

| Element | Spec | Behavior |
|---|---|---|
| Logo mark | 28×28px SVG — indigo gradient hexagon | Always visible even when sidebar collapsed |
| Portal name | "EduForge Admin" — 14px/600, `--text-primary` | Hidden when sidebar collapsed (64px mode) |
| Portal badge | "ADMIN" pill — 10px, indigo background | Always visible |
| Collapse toggle | `[◀]` / `[▶]` icon button, 32×32px | Toggles sidebar expand/collapse. Persisted in localStorage |

### Search Zone (center, flex)

> The search zone is the entry point to the command palette — the single most powerful
> navigation tool in the admin portal. It appears as a styled input field but clicking
> or pressing ⌘K opens the full command palette overlay. The placeholder text cycles
> through suggestions to educate users about what they can search.

```
┌─────────────────────────────────────────────────────────────┐
│  [🔍]  Search institutions, staff, exams, invoices...  ⌘K  │
│        bg: var(--bg-surface-2)                              │
│        border: 1px solid var(--border-default)              │
│        border-radius: var(--radius-md)                      │
│        width: min(640px, 100%)                              │
└─────────────────────────────────────────────────────────────┘
```

| State | Visual |
|---|---|
| Default | Muted placeholder text, no cursor |
| Hover | Border color → `--border-strong` |
| Click / ⌘K | Command palette overlay opens (see component 12-command-palette.md) |
| Focus (keyboard) | `box-shadow: var(--shadow-glow-primary)` |

### Action Zone (right)

> The action zone carries the user's operational context: the current environment, live exam
> alerts, notifications, quick actions, and profile. Each element is role-filtered so a CFO
> never sees the WAR ROOM button and a CTO never sees the financial alert bell.

#### Environment Badge

> Always visible. Critical for preventing accidental production changes during staging tests.
> The badge color immediately communicates the risk level of the current environment.

| Environment | Label | Color | Style |
|---|---|---|---|
| Production | `PROD` | `--status-error` red | Filled pill, pulsing ring |
| Staging | `STAGING` | `--status-warning` amber | Filled pill, no pulse |
| Development | `DEV` | `--status-neutral` gray | Outlined pill |
| Preview | `PREVIEW #42` | `--status-info` blue | Outlined pill with PR number |

#### WAR ROOM Button

> Only appears when any exam has ≥1,000 concurrent students. This button is the emergency
> entry point to the Exam Day War Room page. It disappears automatically when all exams
> drop below 1,000 concurrent. Its pulsing red animation makes it impossible to miss.

```
┌───────────────────────────────────────────┐
│  ●  WAR ROOM  ·  74,320 live             │
│  bg: var(--status-error-bg)               │
│  border: 1px solid var(--status-error)    │
│  border-radius: var(--radius-sm)          │
│  animation: pulse-ring 1.5s infinite      │
│  text: 12px/600, var(--status-error)      │
└───────────────────────────────────────────┘
```

| State | Trigger | Behavior |
|---|---|---|
| Hidden | No exam ≥1,000 concurrent | Not rendered |
| Visible (warning) | Exam 1,000–10,000 concurrent | Amber tint, slower pulse |
| Visible (critical) | Exam >10,000 concurrent | Red, fast pulse, glow shadow |
| Clicked | Any state | Navigate to `/exam/war-room` |

#### Notification Bell

> The notification bell aggregates all platform alerts scoped to the logged-in user's
> role and access level. A CEO sees everything; a CFO sees only financial alerts.
> The badge count is a live WebSocket counter — it updates in real time without page reload.

```
┌─────────────────────────┐
│  🔔  [badge: 7]         │
│  badge: --status-error   │
│  badge position: top-right│
│  badge size: 18px        │
└─────────────────────────┘
```

**Notification Bell Click → Notification Panel (right-side overlay, 400px wide)**

```
┌────────────────────────────────────────────────────────┐
│  Notifications                    [Mark all read] [✕]  │
│  ──────────────────────────────────────────────────── │
│  TABS: [All (7)] [Critical (2)] [Warnings (3)] [Info]  │
│  ──────────────────────────────────────────────────── │
│  ● 2m ago  🔴  P0 Incident — Lambda cold start spike  │
│              INC-2026-0142  [Open →]                   │
│  ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──  │
│  ● 8m ago  🟡  BGV Expired: 62 staff, 31 institutions │
│              [View Compliance →]                        │
│  ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──  │
│  ● 14m ago 🟠  Subscription expiring: 18 institutions  │
│              ₹8.4L revenue at risk  [View →]           │
│  ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──  │
│  ● 1h ago  🟢  JEE Mock #47 complete. 74,312 ranked.  │
│  ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──  │
│  [View all notifications →]                            │
└────────────────────────────────────────────────────────┘
```

| Notification type | Icon | Color | Auto-dismiss |
|---|---|---|---|
| P0/Critical incident | ⚡ | `--status-error` | No — requires acknowledgement |
| BGV/Compliance risk | 🛡 | `--status-warning` | No |
| Subscription expiry | 💳 | `--status-warning` | Yes — after 7 days |
| Exam completed | ✅ | `--status-success` | Yes — after 24h |
| System update | ℹ | `--status-info` | Yes — after 3 days |

#### Quick Actions Button (⚡)

> Role-specific shortcut launcher. Shows 6 actions most relevant to the logged-in role.
> Faster than opening the command palette for frequently used actions.

```
┌──────────────────────────────────────────────┐
│  Quick Actions                          [✕]  │
│  ──────────────────────────────────────────  │
│  (CTO)                                       │
│  ┌──────────────┐  ┌──────────────┐          │
│  │ ⚡ Scale     │  │ 🔑 Rotate    │          │
│  │    Lambda    │  │    JWT Key   │          │
│  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐          │
│  │ 📋 Platform  │  │ 🚨 Create    │          │
│  │    Health    │  │    Incident  │          │
│  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐          │
│  │ 🔐 Security  │  │ 📄 Audit     │          │
│  │    Console   │  │    Log       │          │
│  └──────────────┘  └──────────────┘          │
└──────────────────────────────────────────────┘
```

#### Profile Menu

> The profile menu surfaces identity, session context, and account management options.
> It shows the user's name, role, and access level so any executive can immediately
> confirm which account they are operating on — critical for shared-device environments.

```
┌──────────────────────────────────────────────┐
│  ┌────────┐  Priya Sharma                    │
│  │  PS   │  Platform COO  ·  Level 3         │
│  │ avatar │  priya@eduforge.in               │
│  └────────┘  Last login: Today 9:02 AM IST   │
│  ──────────────────────────────────────────  │
│  [👤] View Profile                           │
│  [🔐] Security & 2FA Settings               │
│  [🌐] Language: English ▼                   │
│  [📱] Active sessions: 1                     │
│  [🎨] Theme: Dark ● / Light ○               │
│  ──────────────────────────────────────────  │
│  [↩ Logout]                                  │
└──────────────────────────────────────────────┘
```

---

## Section B — Sidebar Navigation

> The sidebar is the primary navigation system for the admin portal. It is organized by
> functional domain rather than by division, because executives navigate by task (e.g., "I need
> to check compliance") not by org chart. The sidebar supports two modes — expanded (240px with
> text labels) and collapsed (64px with icons only) — and remembers the user's preference.
> Each nav item shows a live badge count for actionable items (open incidents, pending BGV, etc.)
> so executives can triage from the sidebar without opening each page.

### Sidebar Structure

```
┌──────────────────────────────────────────────┐
│  bg: var(--bg-surface-1)                     │
│  border-right: 1px solid var(--border-subtle) │
│  width: 240px (expanded) / 64px (collapsed)  │
│  position: fixed                             │
│  top: 56px (below top bar)                   │
│  height: calc(100vh - 56px)                  │
│  overflow-y: auto                            │
│  overflow-x: hidden                          │
│  transition: width 250ms ease-in-out         │
│                                              │
│  ──────────────────────────────────────────  │
│  SECTION: COMMAND                            │
│  ──────────────────────────────────────────  │
│  🏠 Dashboard           [active indicator]  │
│  📊 Platform Health                         │
│  🔴 War Room            [● LIVE]            │
│  ──────────────────────────────────────────  │
│  SECTION: INCIDENTS                          │
│  ──────────────────────────────────────────  │
│  🚨 Incidents           [7]                 │
│  ⬆  Escalations         [2]                 │
│  📋 Audit Log                               │
│  ──────────────────────────────────────────  │
│  SECTION: OPERATIONS                         │
│  ──────────────────────────────────────────  │
│  ⚙  Operations Center   [12]                │
│  📅 SLA Management                          │
│  📢 Announcements                           │
│  ──────────────────────────────────────────  │
│  SECTION: INSTITUTIONS                       │
│  ──────────────────────────────────────────  │
│  🏫 Institution Overview                    │
│  👥 Institution Groups                      │
│  ❤  Customer Health                        │
│  ──────────────────────────────────────────  │
│  SECTION: ANALYTICS                          │
│  ──────────────────────────────────────────  │
│  📈 Growth Analytics                        │
│  🧪 Exam Analytics                          │
│  📚 Content Pipeline    [47]                │
│  ──────────────────────────────────────────  │
│  SECTION: COMPLIANCE                         │
│  ──────────────────────────────────────────  │
│  🛡 Compliance          [62]                │
│  🔒 Data Privacy        [3]                 │
│  🔑 Access Control                          │
│  ──────────────────────────────────────────  │
│  SECTION: FINANCE                            │
│  ──────────────────────────────────────────  │
│  💰 Financial Overview                      │
│  📊 Revenue Analytics                       │
│  📋 Subscriptions                           │
│  🔌 Vendor Hub                              │
│  📄 Board Reports                           │
│  ──────────────────────────────────────────  │
│  SECTION: PLATFORM                           │
│  ──────────────────────────────────────────  │
│  ⚙  Settings                                │
│  🚀 Deployments         [1 active]          │
│  📱 Mobile Apps                             │
│  🔁 Disaster Recovery                       │
│  ──────────────────────────────────────────  │
│  SECTION: PEOPLE                             │
│  ──────────────────────────────────────────  │
│  👤 Staff Directory                         │
│  ──────────────────────────────────────────  │
│  SECTION: EXAM (dynamic — exam day only)     │
│  ──────────────────────────────────────────  │
│  ✅ Exam Readiness      [pending]           │
│  🔔 Notifications                           │
└──────────────────────────────────────────────┘
```

### Nav Item Anatomy

> Each nav item is a 44px touch-target row with consistent internal spacing.
> The active item has a left-border accent and a filled background. Inactive items
> show the border only on hover. Badge counts update via WebSocket without page reload.

```
Expanded mode (240px):
┌─────────────────────────────────────────────────────┐
│  │ [icon 20px]  [Label text 14px/500]   [badge]    │
│  ↑ 3px left border (active: --primary, inactive: none)│
└─────────────────────────────────────────────────────┘

Collapsed mode (64px):
┌──────────────────┐
│  │  [icon 20px]  │  ← tooltip on hover: full label
│  ↑ 3px border    │
└──────────────────┘
```

| State | Background | Left Border | Text | Icon |
|---|---|---|---|---|
| Default | transparent | none | `--text-secondary` | `--text-muted` |
| Hover | `--bg-surface-2` | none | `--text-primary` | `--text-secondary` |
| Active | `--primary-muted` | 3px `--primary` | `--text-accent` | `--primary` |
| Disabled | transparent | none | `--text-muted` | `--text-muted` (50%) |
| Badge | — | — | Red/amber pill, 18px height | — |

### Section Headers (Collapsed sidebar)

> When expanded: section label shown as `--text-muted` 11px/600 uppercase.
> When collapsed: section label hidden, only a thin hairline divider separates sections.

### Sidebar Role Filtering

> The sidebar items rendered depend on the logged-in user's access level and division.
> This filtering happens server-side and is embedded in the JWT claims — the sidebar
> never renders items the user cannot access, preventing the confusion of greyed-out links.

| Role | Sections Visible |
|---|---|
| CEO (L5) | All sections |
| CTO (L5) | Command · Incidents · Platform · Access Control · Compliance (security only) |
| COO (L3) | Command · Incidents · Operations · Institutions · Compliance · Analytics |
| CFO (L1) | Command (dashboard only) · Finance |

---

## Section C — Critical Alert Banner

> The Critical Alert Banner is a full-width dismissible band that appears at the top of the
> content area (below top bar, above page header) when there are active platform alerts that
> require executive attention. Unlike regular notifications (which are passive), alert banners
> are active interruptions — they push down the page content and cannot be ignored.
> Critical-severity banners cannot be dismissed until the underlying incident is resolved.

### Anatomy

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ CRITICAL BANNER — persistent, not dismissible                                    │
│ bg: rgba(239,68,68,0.10) · border-bottom: 1px solid rgba(239,68,68,0.30)        │
│ padding: 12px 24px · display: flex · align-items: center · gap: 12px            │
│                                                                                  │
│  🔴  P0 Incident: Lambda cold start spike — 3,200 submissions failing.           │
│      INC-2026-0142  ·  Assigned to: Arun Sharma  ·  Open 4 minutes              │
│      [Open War Room →]   [View Incident →]                [⚡ Scale Lambda Now]  │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────┐
│ WARNING BANNER — dismissible                                                     │
│ bg: rgba(245,158,11,0.10) · border-bottom: 1px solid rgba(245,158,11,0.30)      │
│                                                                                  │
│  ⚠  BGV expired for 62 staff across 31 institutions — POCSO risk.               │
│     [View Compliance →]                                              [Dismiss ✕] │
└──────────────────────────────────────────────────────────────────────────────────┘
```

| Severity | Background tint | Left accent | Dismiss? | Example |
|---|---|---|---|---|
| 🔴 Critical | `--status-error-bg` | 4px solid `--status-error` | No — resolve first | P0 incident, active breach |
| 🟠 High | `rgba(245,101,19,0.10)` | 4px solid `#F97316` | Yes | P1 incident, BGV mass expiry |
| 🟡 Warning | `--status-warning-bg` | 4px solid `--status-warning` | Yes | Subscription expiry, slow API |
| 🟢 Info | `--status-success-bg` | 4px solid `--status-success` | Yes | Exam completed, rank published |

**Banner stacking:** Multiple active banners stack vertically, critical at top.
**Banner collapse:** After 3+ banners, a `[+2 more alerts]` collapser is shown to prevent
the entire viewport from being consumed by banners.

---

## Section D — Page Header

> The page header is the first element inside the content area. It provides orientation
> (breadcrumb + page title), contextual metadata (when the page was last refreshed),
> and the page-level actions that apply to the entire page (not individual rows).
> Keeping all primary actions here — rather than floating them throughout the page —
> makes the interface predictable: executives always know where to look for major actions.

### Anatomy

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│  BREADCRUMB STRIP  (12px / --text-muted)                                        │
│  Dashboard  /  Platform  /  Security Console                                     │
├──────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐  ┌────────────────────────┐│
│  │  PAGE TITLE (28px / 700 / --text-primary)       │  │  PAGE ACTIONS          ││
│  │  Security Console                               │  │  [+ Create] [Export ▼] ││
│  │  ─────────────────────────────────────────────  │  │  [Settings ⚙]         ││
│  │  SUBTITLE (14px / --text-secondary)             │  └────────────────────────┘│
│  │  Last updated: 8s ago · 3 active threats        │                            │
│  └─────────────────────────────────────────────────┘                            │
└──────────────────────────────────────────────────────────────────────────────────┘
```

| Element | Spec | Notes |
|---|---|---|
| Breadcrumb | 12px, `--text-muted`, chevron `›` separator | Clickable except last item |
| Page title | 28px/700, `--text-primary` | H1, always present |
| Subtitle / meta | 14px, `--text-secondary` | Optional — last updated, count, status |
| Page actions | Right-aligned, gap: 8px | Max 4 visible, rest in `[⋯]` overflow |
| Refresh indicator | "Updated 8s ago" — auto-increments | Turns amber >30s, red >60s |
| Live badge | `● LIVE` — emerald pulse | Shown when page has real-time WebSocket data |

---

## Section E — Content Area

> The content area is where each individual page renders its unique UI. This zone has no
> fixed internal structure — each page defines its own layout using the design system
> components. However, all pages must adhere to the content area padding and grid
> specifications below to maintain visual consistency across all 31 admin pages.

### Content Area Specifications

| Property | Value |
|---|---|
| Padding | `24px` on all sides (desktop) · `16px` on mobile |
| Max content width | `1400px` centered (prevents ultra-wide monitors from stretching tables) |
| Background | `--bg-base` (`#070C18`) |
| Overflow | `auto` — scrolls independently of sidebar and top bar |
| Top padding | Adds `56px` to account for fixed top bar |

### Content Zone Grid

> Most pages use one of three standard grid arrangements. Page specs declare which grid
> they use rather than specifying custom layouts.

**Grid A — Full Width (single column)**
Used by: Audit Log, Incident Management, Staff Directory, Institution Overview
```
┌────────────────────────────────────────────────────────┐
│  [FILTER BAR]                                          │
│  [FULL-WIDTH TABLE]                                    │
│  [PAGINATION]                                          │
└────────────────────────────────────────────────────────┘
```

**Grid B — Split (60/40 or 70/30)**
Used by: Platform Health, Institution Groups, Deployment Pipeline
```
┌───────────────────────────┬────────────────────────┐
│  PRIMARY PANEL            │  SECONDARY PANEL        │
│  (main data / charts)     │  (detail / controls)    │
└───────────────────────────┴────────────────────────┘
```

**Grid C — Dashboard (KPI row + 2-col content)**
Used by: Executive Dashboard, Compliance Dashboard, Financial Overview
```
┌────────────────────────────────────────────────────────┐
│  [KPI STAT CARD ROW — 4 to 6 cards]                   │
├──────────────────────────┬─────────────────────────────┤
│  LEFT COLUMN             │  RIGHT COLUMN               │
│  (primary content)       │  (secondary / charts)       │
└──────────────────────────┴─────────────────────────────┘
```

**Grid D — Analytics (header charts + table)**
Used by: Growth Analytics, Exam Analytics, Revenue Analytics
```
┌────────────────────────────────────────────────────────┐
│  [KPI ROW]                                             │
├──────────────────────────────────────────────────────  │
│  [CHART GRID — 2×2]                                    │
├──────────────────────────────────────────────────────  │
│  [DATA TABLE with filters]                             │
└────────────────────────────────────────────────────────┘
```

---

## Section F — Overlay Layers

> The overlay layer system manages the z-index stacking of all temporary UI elements.
> Layers are numbered by z-index and each has a clear purpose. Nothing should live at
> an arbitrary z-index — all overlays must use one of the defined layer values below.

| Layer Name | Z-Index | Components | Notes |
|---|---|---|---|
| Page base | 0 | Normal content | All static elements |
| Raised | 10 | Card hover state, table row hover | |
| Sticky elements | 100 | Sticky table headers, filter bars | |
| Dropdowns | 200 | Select menus, date pickers, autocomplete | Closes on ESC or click-outside |
| Top bar | 300 | Fixed top navigation | Persists over all page content |
| Sidebar | 400 | Fixed sidebar | Below drawers |
| Drawer | 600 | Right-side detail drawers | Backdrop: `rgba(0,0,0,0.5)` |
| Modal | 800 | Confirmation dialogs, forms | Backdrop: `rgba(0,0,0,0.7)` |
| Command palette | 900 | ⌘K overlay | Backdrop: `rgba(0,0,0,0.8)` |
| Toast | 1000 | Success/error notifications | No backdrop, corner-anchored |
| Critical overlay | 9999 | Exam lockdown, session expired, emergency | Blocks all interaction |

---

## Section G — Critical State Modes

> The admin portal has four special global states that override the normal layout.
> These states are triggered by platform-level events and affect every executive
> regardless of which page they are currently viewing.

### Mode 1: WAR ROOM Active

> Triggered: Any exam reaches ≥1,000 concurrent students.
> Effect: Red pulsing banner injected at top of all pages. WAR ROOM button appears in top bar.
> The normal page remains accessible — executives can still use other pages.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│  ●  WAR ROOM ACTIVE — JEE Mock #48: 74,320 students online  [Open War Room →]   │
│  bg: rgba(239,68,68,0.12) · animation: pulse-border 2s infinite                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Mode 2: P0 Incident Active

> Triggered: A P0 incident is created (manually or by auto-monitoring).
> Effect: Critical alert banner appears on all pages. Incident is linked to War Room if exam is live.

### Mode 3: Session Expiry Warning

> Triggered: Session will expire in <15 minutes (L5: 8h sessions, L3: 24h sessions).
> Effect: Non-blocking bottom-right toast with countdown. Clicking extends session via re-auth.

```
┌────────────────────────────────────────────┐
│  🔐 Session expiring in 12 minutes         │
│  [Extend Session]   [Logout Now]            │
│  bottom-right corner, z-index: 1000         │
└────────────────────────────────────────────┘
```

### Mode 4: Maintenance Mode

> Triggered: CTO puts platform into scheduled maintenance via Platform Settings.
> Effect: Full-screen overlay for all non-executive users. Executive portal remains accessible.
> Yellow banner shown to all executives indicating maintenance window is active.

---

## Section H — Responsive Behavior

> All 31 admin pages are primarily designed for desktop (1280px+). The layout degrades
> gracefully to tablet (768px+) and mobile (<768px), but the admin portal is not
> optimized for mobile — executives are expected to use desktop or large tablets.

| Breakpoint | Sidebar | Top bar | Content | Tables |
|---|---|---|---|---|
| 1536px+ (2xl) | 260px expanded | Full | Max 1400px centered | Full columns |
| 1280–1535px (xl) | 240px expanded | Full | Full | Full columns |
| 1024–1279px (lg) | 64px icon-only | Full | Full | Some columns hidden |
| 768–1023px (md) | Overlay on hamburger | Compact | Full | Horizontal scroll |
| <768px (sm/xs) | Overlay on hamburger | Minimal | Full width | Horizontal scroll + sticky first col |

---

## Section I — Animation & Motion Principles

> All animations in the admin portal follow a "purposeful motion" principle: animations
> convey meaning (a drawer slides in from the right to indicate it came from that direction;
> a modal scales up from center to indicate it appeared over the current context).
> No decorative animations. Every animation has a functional reason.

| Element | Animation | Duration | Easing | Why |
|---|---|---|---|---|
| Page transition | Fade in (opacity 0→1) | 150ms | ease-out | Fast — executives navigate frequently |
| Drawer open | Slide from right (translateX 100%→0) + fade | 250ms | cubic-bezier(0.32,0,0.67,0) | Direction indicates source |
| Drawer close | Slide to right + fade | 200ms | ease-in | Faster close feels responsive |
| Modal open | Scale 0.96→1 + fade | 200ms | ease-out | Appears "in front" of page |
| Modal close | Scale 1→0.96 + fade | 150ms | ease-in | Disappears back |
| Toast enter | Slide from right + fade | 300ms | spring | Grabs attention without jarring |
| Toast exit | Slide to right + fade | 200ms | ease-in | Leaves quickly |
| Skeleton loader | Shimmer (left→right) | 1500ms | linear infinite | Indicates loading in progress |
| Tab switch | Underline slides left/right | 200ms | ease-in-out | Indicates direction of navigation |
| Accordion expand | Height 0→auto + fade | 200ms | ease-out | Smooth content reveal |
| Pulse (live) | Ring expands + fades | 1500ms | ease-out infinite | Signals live/real-time data |
| Number count-up | Tween from 0→value | 800ms | ease-out | Makes KPI updates feel alive |

**Reduced motion:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Section J — Keyboard Navigation (Global)

> Keyboard shortcuts are a first-class feature of the admin portal. Executives running
> live exams or managing incidents need to act in seconds — mouse navigation is too slow.
> All shortcuts are discoverable via ⌘K → type "keyboard shortcuts".

| Shortcut | Action | Available On |
|---|---|---|
| `⌘K` / `Ctrl+K` | Open command palette | All pages |
| `⌘/` | Focus search input | All pages |
| `ESC` | Close drawer/modal/palette | Any overlay open |
| `⌘B` | Toggle sidebar expand/collapse | All pages |
| `⌘.` | Open notification panel | All pages |
| `⌘⇧W` | Open/close War Room (when exam live) | All pages |
| `G then D` | Go to Dashboard | All pages |
| `G then H` | Go to Platform Health | All pages |
| `G then I` | Go to Incidents | All pages |
| `G then S` | Go to Security Console | All pages |
| `G then A` | Go to Audit Log | All pages |
| `?` | Show keyboard shortcuts modal | All pages |
| `Tab` / `Shift+Tab` | Navigate focusable elements | All pages |
| `Enter` / `Space` | Activate focused element | All pages |
| `Arrow keys` | Navigate table rows / list items | Table focused |
| `⌘A` | Select all rows (in table) | Table focused |
| `⌘E` | Export current view | Table focused |

---

## Section K — Loading & Error States (Global)

### Page Load State
> On every route change, the content area shows a skeleton of the target page's layout
> (not a full-page spinner). The skeleton uses the same grid as the actual page, with
> shimmer rectangles replacing real content. The sidebar and top bar remain fully interactive.

```
Skeleton shimmer style:
background: linear-gradient(
  90deg,
  var(--bg-surface-2) 0%,
  var(--bg-surface-3) 50%,
  var(--bg-surface-2) 100%
);
background-size: 400% 100%;
animation: shimmer 1.5s linear infinite;
```

### API Error State
> When an API call fails, the affected section shows an inline error state — not a full page error.
> Other sections on the same page continue to function normally.

```
┌────────────────────────────────────────────────────┐
│  ⚠  Failed to load incident data                   │
│  Network error — check connection                  │
│  [Retry]   [View cached data]                      │
└────────────────────────────────────────────────────┘
```

### 404 / Unauthorized State

```
┌────────────────────────────────────────────────────┐
│  🔒  Access denied                                 │
│  Your role does not have permission to view this.  │
│  Contact your administrator.                       │
│  [Back to Dashboard]                               │
└────────────────────────────────────────────────────┘
```

---

## Section L — Toast Notification System

> Toast notifications provide non-blocking feedback for user actions across the entire
> application. They appear in the bottom-right corner, stack vertically (max 3 visible),
> and auto-dismiss after their configured duration. Destructive action confirmations
> always show a toast — both on success ("Incident resolved") and on failure ("Save failed").

### Toast Variants

```
┌──────────────────────────────────────────────────┐
│  ✅  Incident INC-2026-0142 resolved              │  SUCCESS — auto-dismiss: 4s
│      [View Incident]                        [✕]  │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  ❌  Failed to rotate JWT key                     │  ERROR — auto-dismiss: 8s
│      Network error. Try again.              [✕]  │  (longer — user needs to act)
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  ⚠  Lambda scale in progress...                  │  WARNING — auto-dismiss: 6s
│      Takes ~90 seconds to complete         [✕]  │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  ℹ  Export is being prepared                     │  INFO — auto-dismiss: 5s
│      You'll receive a WhatsApp notification [✕]  │
└──────────────────────────────────────────────────┘
```

| Variant | Icon | Border color | Auto-dismiss | Use case |
|---|---|---|---|---|
| Success | ✅ | `--status-success` | 4s | Action completed |
| Error | ❌ | `--status-error` | 8s | Action failed |
| Warning | ⚠ | `--status-warning` | 6s | Partial success, caveat |
| Info | ℹ | `--status-info` | 5s | Background process started |
| Loading | ⟳ | `--primary` | Never | Operation in progress |

---

## Section M — Data Density Modes

> The admin portal supports three data density modes, switchable from the profile menu.
> Dense mode is the default because executives and operations staff prefer seeing more
> data at once. Comfortable mode is for users who prefer larger touch targets.

| Mode | Row height | Font size | Padding | Suitable for |
|---|---|---|---|---|
| Compact | 36px | 12px | 8px | Power users, large datasets |
| Default | 48px | 14px | 12px | Standard daily use |
| Comfortable | 60px | 15px | 16px | Accessibility, larger monitors |

---

## Related Component Files

| File | What it defines |
|---|---|
| [01-table-pagination.md](01-table-pagination.md) | Data tables, sorting, bulk actions, pagination |
| [02-modal-drawer.md](02-modal-drawer.md) | Modals, side drawers, confirmation dialogs |
| [03-alerts-toasts.md](03-alerts-toasts.md) | Alert banners, toast notifications |
| [04-filters-search.md](04-filters-search.md) | Filter bars, search inputs, saved filters |
| [05-forms-inputs.md](05-forms-inputs.md) | Form fields, validation, input variants |
| [06-navigation.md](06-navigation.md) | Breadcrumbs, tabs, sub-navigation |
| [07-data-display.md](07-data-display.md) | Stat cards, badges, charts |
| [08-design-tokens.md](08-design-tokens.md) | Full color, typography, spacing token reference |
| [09-charts-graphs.md](09-charts-graphs.md) | Chart types, real-time graphs, sparklines |
| [10-stat-cards.md](10-stat-cards.md) | KPI cards, metric tiles, trend indicators |
| [11-timeline.md](11-timeline.md) | Event timelines, activity feeds |
| [12-command-palette.md](12-command-palette.md) | ⌘K command palette |
