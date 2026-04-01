# Component: Navigation — Sidebar, Top Nav, Tabs, Breadcrumb

---

## Portal Layout (Master Template)

### Desktop Layout (≥ 1024px)
```
┌──────────────────────────────────────────────────────────────────┐
│  TOP NAV BAR                                                     │
│  [☰] [Portal Logo + Name]    [🔍 Search]  [🔔] [👤 Profile ▼]  │
├──────────────┬───────────────────────────────────────────────────┤
│              │  PAGE HEADER                                      │
│   SIDEBAR    │  [Breadcrumb]              [Page Action buttons]  │
│   (240px)    │  [Page Title]                                     │
│              │  [Quick filter chips — if applicable]             │
│   [Nav       ├───────────────────────────────────────────────────┤
│    Items]    │                                                   │
│              │  PAGE CONTENT AREA                                │
│              │                                                   │
│              │  (Table / Dashboard / Form etc.)                  │
│              │                                                   │
│              │                                                   │
└──────────────┴───────────────────────────────────────────────────┘
```

### Mobile Layout (< 768px)
```
┌──────────────────────────────────────┐
│  [☰]  Portal Name    [🔔] [👤]      │  ← Top nav (fixed)
├──────────────────────────────────────┤
│  [Breadcrumb]                        │
│  Page Title                          │
├──────────────────────────────────────┤
│                                      │
│  Page Content                        │
│                                      │
└──────────────────────────────────────┘
    [☰ Menu slides in from left as overlay]
```

---

## Top Navigation Bar

### Layout
```
┌─────────────────────────────────────────────────────────────────┐
│ [☰]  [EduForge Logo] [Portal Name]   [🔍]  [🔔 3] [ℹ] [👤 ▼] │
└─────────────────────────────────────────────────────────────────┘
```

### Elements

| Element | Spec | Behavior |
|---|---|---|
| Hamburger [☰] | 40×40 touch target | Toggles sidebar collapsed/expanded |
| Logo | 32px height, portal-specific | Click = go to home dashboard |
| Portal name | 14px medium, hidden on mobile | Shows institution name |
| Search [🔍] | Expands to full search bar on click | Global search across portal |
| Notifications [🔔] | Badge shows unread count (max 99+) | Opens notification drawer |
| Info [ℹ] | | Opens help / keyboard shortcuts panel |
| Profile [👤] | Avatar (32px) + name (desktop only) [▼] | Dropdown: Profile, Settings, Logout |

### Profile Dropdown
```
┌───────────────────────────────┐
│  [Avatar 48px]                │
│  Ravi Kumar Sharma            │
│  Content Director             │
│  admin.eduforge.in            │
│  ──────────────────────────── │
│  👤  My Profile               │
│  ⚙️  Preferences              │
│  🔒  Security & Sessions      │
│  ──────────────────────────── │
│  🔄  Switch Portal            │  ← Shows if multi-portal user
│  ──────────────────────────── │
│  🚪  Log Out                  │
└───────────────────────────────┘
```

---

## Sidebar Navigation

### Layout (Expanded — 240px)
```
┌──────────────────────────────────────────┐
│                                          │
│  🏠  Dashboard          ← active item   │  ← filled primary bg
│                                          │
│  ─── CONTENT ───────────────────────    │  ← section divider
│  📝  MCQ Bank                            │
│  📋  Notes                               │
│  🎬  Videos                              │
│  ▼ Content sub-menu is open              │
│       All Questions                      │
│       Pending Review                     │
│       Published                          │
│                                          │
│  ─── OPERATIONS ────────────────────    │
│  🏫  Institutions                        │
│  👥  Users                               │
│  📅  Exams                               │
│                                          │
│  ─── REPORTS ───────────────────────    │
│  📊  Analytics                           │
│  💰  Billing                             │
│                                          │
│  ─── ADMIN ─────────────────────────    │
│  ⚙️  Settings                            │
└──────────────────────────────────────────┘
```

### Collapsed Sidebar (64px — icons only)
```
┌────────┐
│  🏠    │  ← tooltip on hover: "Dashboard"
│        │
│  📝    │
│  📋    │
│  🎬    │
│        │
│  🏫    │
│  👥    │
│  📅    │
│        │
│  📊    │
│  💰    │
│        │
│  ⚙️    │
└────────┘
```

### Nav Item States

| State | Background | Text | Icon |
|---|---|---|---|
| Default | Transparent | `--text-secondary` | `--text-muted` |
| Hover | `--bg-surface-2` | `--text-primary` | `--primary` |
| Active (current page) | primary 12% tint | `--primary` | `--primary` |
| Active (parent of current) | primary 6% tint | `--primary` | `--primary` |
| Disabled | Transparent | 40% opacity | 40% opacity |

### Sub-menu (Nested nav)
- Indent: 16px from parent
- Expand/collapse: Chevron [▼/▶] on parent item
- Open by default if current page is in this group
- Max 2 levels deep (nav item → sub-item). No 3rd level

### Nav Badges
```
📅  Exams            [3]   ← red badge = pending actions
👥  BGV              [15]  ← warning badge = action required
```

---

## Breadcrumb

### Layout
```
Dashboard  /  Institutions  /  XYZ School  /  Students  /  Ravi Kumar
```

### Behavior

| Property | Spec |
|---|---|
| Separator | `/` in `--on-surface-variant` |
| Last item | Not a link. Current page. Bold. `--on-surface` |
| All others | Links. `--primary` color. Underline on hover |
| Overflow | On mobile: show only last 2 items. First item = `…` with dropdown |
| Max length | Each segment max 24 chars. Truncate with tooltip |
| Dynamic | Auto-generated from URL structure + page title |

---

## Page Tabs

### Layout
```
┌─────────────────────────────────────────────────────────┐
│  [Overview]  [Students]  [Staff]  [Exams]  [Finance]   │
│  ──────────────────────────────────────────             │
│                                            ↑ active tab │
│  Tab content below                                      │
└─────────────────────────────────────────────────────────┘
```

### Behavior

| Property | Spec |
|---|---|
| Active indicator | 2px bottom border in `--primary` color |
| Inactive | No border, `--on-surface-variant` text |
| Hover | `--surface-variant` background, `--on-surface` text |
| Overflow | > 6 tabs → show 5 + "More [▼]" dropdown |
| URL | Tab change reflected in URL: `?tab=students` |
| Keyboard | Left/right arrow keys navigate between tabs |
| Loading | Spinner in tab content area while loading |
| Count badge | Tab can show count: `Students (1,247)` |

### Tab Variants

| Type | Use Case |
|---|---|
| Page tabs | Major sections of a page — always visible |
| Drawer tabs | Sections within a detail drawer |
| Pill tabs | Compact filter-like tabs in cards |

---

## Theme Support (Dark + Light)

> The full App Shell (top bar + sidebar) is documented in `00-global-layout.md`. This section covers the token mappings for navigation elements on pages: tabs, breadcrumbs, and step indicators.

```css
/* ── Top navigation bar ── */
.top-nav {
  background: var(--bg-surface-1);
  border-bottom: 1px solid var(--border-subtle);
  height: 56px;
}

:root .top-nav { background: var(--bg-surface-1); }        /* #0D1526 */
[data-theme="light"] .top-nav { background: var(--bg-surface-1); box-shadow: 0 1px 3px rgba(0,0,0,0.08); }  /* #FFFFFF */

/* ── Sidebar ── */
.sidebar {
  background: var(--bg-surface-1);
  border-right: 1px solid var(--border-subtle);
}

:root .sidebar { background: var(--bg-surface-1); }       /* #0D1526 */
[data-theme="light"] .sidebar { background: var(--bg-surface-1); border-right-color: var(--border-subtle); }  /* #FFFFFF */

/* ── Sidebar nav items ── */
.nav-item {
  color: var(--text-secondary);
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-3);
  display: flex; align-items: center; gap: var(--space-3);
  font-size: var(--text-sm); font-weight: 500;
  transition: background 120ms, color 120ms;
  cursor: pointer;
}
.nav-item:hover {
  background: var(--bg-surface-2);
  color: var(--text-primary);
}
.nav-item--active {
  background: color-mix(in srgb, var(--primary) 12%, transparent);
  color: var(--primary);
}
.nav-item--active .nav-item__icon { color: var(--primary); }

.nav-item__icon { color: var(--text-muted); width: 18px; height: 18px; flex-shrink: 0; }

/* ── Section divider in sidebar ── */
.nav-section-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  padding: var(--space-4) var(--space-3) var(--space-1);
}

/* ── Page tabs ── */
.page-tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid var(--border-subtle);
}
.page-tab {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-sm); font-weight: 500;
  color: var(--text-muted);
  border-bottom: 2px solid transparent;
  cursor: pointer; transition: color 120ms, border-color 120ms;
}
.page-tab:hover { color: var(--text-primary); }
.page-tab--active {
  color: var(--primary);
  border-bottom-color: var(--primary);
}

/* ── Breadcrumb ── */
.breadcrumb { display: flex; align-items: center; gap: var(--space-1); font-size: var(--text-sm); }
.breadcrumb__item { color: var(--text-muted); }
.breadcrumb__item--link { color: var(--text-secondary); text-decoration: none; }
.breadcrumb__item--link:hover { color: var(--primary); }
.breadcrumb__item--current { color: var(--text-primary); font-weight: 500; }
.breadcrumb__sep { color: var(--border-default); }

/* ── Step progress ── */
.step-circle--done    { background: var(--primary); border-color: var(--primary); color: white; }
.step-circle--active  { background: var(--primary); border-color: var(--primary); color: white; }
.step-circle--todo    { background: transparent; border: 2px solid var(--border-default); color: var(--text-muted); }
.step-circle--error   { background: var(--error); border-color: var(--error); color: white; }
.step-line--done      { background: var(--primary); }
.step-line--todo      { background: var(--border-subtle); }

/* ── Profile dropdown ── */
.profile-dropdown {
  background: var(--bg-surface-1);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}
:root .profile-dropdown { background: var(--bg-surface-1); }    /* #0D1526 */
[data-theme="light"] .profile-dropdown { background: #FFFFFF; box-shadow: 0 8px 24px rgba(0,0,0,0.12); }

.profile-dropdown__item {
  color: var(--text-secondary);
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  cursor: pointer;
  display: flex; align-items: center; gap: var(--space-3);
}
.profile-dropdown__item:hover {
  background: var(--bg-surface-2);
  color: var(--text-primary);
}
```

### Token Quick Reference

| Property | Dark | Light |
|---|---|---|
| Topbar bg | `--bg-surface-1` → `#0D1526` | `--bg-surface-1` → `#FFFFFF` |
| Sidebar bg | `--bg-surface-1` → `#0D1526` | `--bg-surface-1` → `#FFFFFF` |
| Nav item text | `--text-secondary` → `#94A3B8` | `--text-secondary` → `#475569` |
| Nav item hover bg | `--bg-surface-2` → `#131F38` | `--bg-surface-2` → `#F1F5F9` |
| Active nav bg | primary 12% tint | primary 12% tint |
| Active nav text | `--primary` → `#6366F1` | `--primary` → `#4F46E5` |
| Active tab border | `--primary` | `--primary` |
| Breadcrumb link | `--text-secondary` | `--text-secondary` |
| Step done | `--primary` fill | `--primary` fill |

---

## Step Progress (Wizard)

> For multi-step forms: onboarding, exam creation, bulk upload.

### Layout
```
  ●━━━━━━━━●━━━━━━━━○━━━━━━━━○
 Step 1    Step 2   Step 3   Step 4
  Done     Active   Todo     Todo
```

### States

| State | Circle | Line | Label |
|---|---|---|---|
| Completed | Filled primary with ✓ | Solid primary | Dark text |
| Active (current) | Filled primary (no ✓) | — | Bold primary text |
| Upcoming | Empty circle (outlined) | Dashed gray | Gray text |
| Error | Red circle with ✕ | Red solid | Red text |

### Navigation
- Previous/Next buttons below form (not inside step indicator)
- Clicking completed step = navigate back to that step
- Cannot skip ahead to future steps (unless explicitly allowed)
- Browser back button = go to previous step (not leave wizard)

---

## Notification Drawer

> Opens from bell icon [🔔] in top nav.

### Layout
```
┌────────────────────────────────────────────┐
│  Notifications                 [Mark all ✓]│
│  ──────────────────────────────────────── │
│  [Filters: All | Unread | Mentions]        │
│                                            │
│  TODAY                                     │
│  ┌────────────────────────────────────┐   │
│  │ 🔴 [Icon] BGV pending for 3 staff  │   │  ← Unread
│  │         XYZ School · 2 hours ago   │   │
│  └────────────────────────────────────┘   │
│                                            │
│  ┌────────────────────────────────────┐   │
│  │    [Icon] Exam published: JEE Mock │   │  ← Read
│  │         4 hours ago                │   │
│  └────────────────────────────────────┘   │
│                                            │
│  YESTERDAY                                 │
│  ┌────────────────────────────────────┐   │
│  │    [Icon] 1,247 results computed   │   │
│  │         Yesterday 6:42 PM          │   │
│  └────────────────────────────────────┘   │
│                                            │
│  [Load more notifications]                 │
└────────────────────────────────────────────┘
```
