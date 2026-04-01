# Component: Modal, Side Drawer, Bottom Sheet

> Overlays for detail views, forms, and confirmations.
> Reference this file — do not re-document per page.

---

## Modal Dialog

### When to Use
- Confirmation dialogs (delete, suspend, approve)
- Short forms (add note, change role, send message)
- Quick views that need full attention before returning to page
- Alerts that require user acknowledgement

### Layout

```
┌──────────────────────────── BACKDROP (60% black) ──────────────────┐
│                                                                      │
│            ┌────────────────────────────────────────┐               │
│            │  [Modal Title]                    [✕]  │               │
│            │  ──────────────────────────────────── │               │
│            │                                        │               │
│            │  [Modal content area]                  │               │
│            │                                        │               │
│            │  ──────────────────────────────────── │               │
│            │  [Cancel]              [Primary Action]│               │
│            └────────────────────────────────────────┘               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Size Variants

| Variant | Max Width | Use Case |
|---|---|---|
| `sm` | 400px | Confirm dialogs, simple alerts |
| `md` | 560px | Short forms (1–3 fields), detail view |
| `lg` | 720px | Longer forms, preview content |
| `xl` | 960px | Rich content, multi-step forms |
| `fullscreen` | 100vw×100vh | Document viewer, image editor |

### Behavior

| Property | Spec |
|---|---|
| Open animation | Fade in + scale from 95%→100%, 200ms ease-out |
| Close animation | Fade out + scale 100%→95%, 150ms ease-in |
| Backdrop click | Closes modal (unless `persistent=true` — for unsaved forms) |
| ESC key | Closes modal — same as backdrop click |
| Scroll | Modal content area scrolls independently if content overflows |
| Max height | 90vh. Content area scrolls, header+footer stick |
| Focus trap | Tab cycles only within modal while open |
| Z-index | `z-index: 1000` (above all page content, below critical alerts) |

### Header

| Element | Spec |
|---|---|
| Title | H2, 18px semibold, max 1 line (truncate if longer) |
| Close button [✕] | 40×40 touch target. Always present unless `hideClose=true` |
| Subtitle | Optional — small text below title in `--on-surface-variant` |
| Icon | Optional leading icon before title (24px) |

### Footer

| Layout | When |
|---|---|
| Single button (right) | Informational — "Close" or "Got it" |
| Two buttons (left: cancel, right: primary) | Form / action modals |
| Three buttons (left: delete, center: cancel, right: save) | Edit forms with delete option |
| No footer | When scrollable content has its own CTAs embedded |

### Button States (Footer)

| Button | Style | Confirm Action | Loading |
|---|---|---|---|
| Cancel | Ghost / text button | Closes without action | Never shows loader |
| Primary Save | Filled primary color | Submits form | Shows spinner, disabled |
| Delete / Destructive | Filled `--error` red | Requires confirm dialog before | Shows spinner |

### Confirm Dialog (Nested)

> For destructive actions — always confirm before executing.

```
┌────────────────────────────────────────────┐
│  ⚠️  Delete this student?                  │
│                                            │
│  This will permanently remove Ravi Kumar   │
│  and all their test history.               │
│  This action CANNOT be undone.             │
│                                            │
│  Type "DELETE" to confirm:                 │
│  [_______________]                         │
│                                            │
│  [Cancel]            [Delete Permanently] │
│                          (red, disabled    │
│                           until typed)     │
└────────────────────────────────────────────┘
```

---

## Side Drawer

### When to Use
- Detail view of a row (student profile, staff profile, exam details)
- Long forms that need to stay alongside the list
- Settings panel that overlays without leaving current page
- Contextual info that doesn't need full page navigation

### Layout

```
PAGE CONTENT (dimmed)          │  DRAWER (slides in from right)
                               │
─────────────────────────────  │  ┌─────────────────────────────┐
                               │  │ [← Close]  [Student Profile] │
  Data Table / Page Content    │  │  [⋯] [Edit] [Export]         │
                               │  │ ──────────────────────────── │
                               │  │                              │
                               │  │  [Content Area — scrollable] │
                               │  │                              │
                               │  │                              │
                               │  │                              │
                               │  │ ──────────────────────────── │
                               │  │ [Footer actions if needed]   │
─────────────────────────────  │  └─────────────────────────────┘
```

### Size Variants

| Variant | Width | Use Case |
|---|---|---|
| `narrow` | 360px | Quick preview, status change |
| `default` | 480px | Profile view, detail page |
| `wide` | 640px | Full form, analytics view |
| `extra-wide` | 800px | Exam paper preview, report view |

### Behavior

| Property | Spec |
|---|---|
| Open animation | Slide from right, 250ms ease-out |
| Close animation | Slide to right, 200ms ease-in |
| Backdrop | Semi-transparent. Click backdrop = close |
| ESC key | Closes drawer |
| Scroll | Drawer content scrolls independently |
| Stacked drawers | Max 2 drawers stacked (e.g., student profile → edit form) |
| URL | Drawer state reflected in URL: `?drawer=student&id=123` — shareable |
| Mobile | On mobile < 768px: converts to bottom sheet full-screen |

### Drawer Header

```
┌──────────────────────────────────────────────┐
│  [←]  Ravi Kumar                    [⋯] [✕] │
│        Class 12 — MPC · Roll: 1042           │
│  ──────────────────────────────────────────  │
│  [Profile] [Performance] [Fees] [Documents]  │
│  (Tab navigation within drawer)              │
└──────────────────────────────────────────────┘
```

| Element | Spec |
|---|---|
| Back arrow [←] | Closes current drawer (or goes back if stacked) |
| Title | Entity name — primary info |
| Subtitle | Secondary context (class, role, status) |
| Action buttons | Edit, Export, More (⋯) — top-right |
| Tabs | If entity has multiple sections — tabs below header |

### Tabs in Drawer

- Max 5 tabs. More than 5 → use dropdown inside drawer
- Active tab: border-bottom in primary color
- Content area below tabs scrolls per tab independently
- Tabs persisted in URL: `?drawer=student&id=123&tab=performance`

---

## Bottom Sheet

> On mobile only. Slides up from bottom. Same use cases as drawer.

### Layout (Mobile)

```
┌──────────────────────────────┐
│                              │
│  [PAGE CONTENT — DIMMED]     │
│                              │
├──────────────────────────────┤
│      ━━━ (drag handle)       │  ← Drag down to dismiss
│                              │
│  [Title]              [✕]   │
│  ──────────────────────────  │
│                              │
│  [Content Area — scrollable] │
│                              │
└──────────────────────────────┘
```

### Snap Points

| Position | Height | Trigger |
|---|---|---|
| Peek | 40vh | Initial open for preview |
| Half | 60vh | After first scroll up |
| Full | 95vh | After second scroll up |
| Closed | 0 | Drag down past 30% or tap outside |

---

## Theme Support (Dark + Light)

> Modals, drawers, and bottom sheets use CSS tokens for backgrounds, borders, and shadows. They adapt automatically between dark and light themes.

```css
/* ── Backdrop ── */
.modal-backdrop,
.drawer-backdrop {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(2px);
}

[data-theme="light"] .modal-backdrop,
[data-theme="light"] .drawer-backdrop {
  background: rgba(15, 23, 42, 0.35);
}

/* ── Modal box ── */
.modal {
  background: var(--bg-surface-1);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
}

/* Dark */
:root .modal {
  background: var(--bg-surface-1);         /* #0D1526 */
  border-color: var(--border-default);     /* #334155 */
  box-shadow: 0 25px 50px rgba(0,0,0,0.5);
}

/* Light */
[data-theme="light"] .modal {
  background: var(--bg-surface-1);         /* #FFFFFF */
  border-color: var(--border-subtle);      /* #E2E8F0 */
  box-shadow: 0 25px 50px rgba(0,0,0,0.15);
}

/* ── Modal header ── */
.modal__title {
  color: var(--text-primary);
  font-size: var(--text-xl);
  font-weight: 600;
}

.modal__subtitle { color: var(--text-secondary); }

.modal__header-divider,
.modal__footer-divider {
  border-color: var(--border-subtle);
}

/* ── Modal footer buttons ── */
.modal__btn-cancel {
  background: transparent;
  border: 1px solid var(--border-default);
  color: var(--text-secondary);
  border-radius: var(--radius-md);
}
.modal__btn-cancel:hover { border-color: var(--primary); color: var(--primary); }

.modal__btn-primary {
  background: var(--primary);
  color: white;
  border-radius: var(--radius-md);
}
.modal__btn-primary:hover { background: color-mix(in srgb, var(--primary) 85%, white); }

.modal__btn-destructive {
  background: var(--error);
  color: white;
  border-radius: var(--radius-md);
}

/* ── Side drawer ── */
.drawer {
  background: var(--bg-surface-1);
  border-left: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-xl);
}

:root .drawer {
  background: var(--bg-surface-1);         /* #0D1526 */
  border-left-color: var(--border-default);
}

[data-theme="light"] .drawer {
  background: var(--bg-surface-1);         /* #FFFFFF */
  border-left-color: var(--border-subtle); /* #E2E8F0 */
  box-shadow: -8px 0 40px rgba(0,0,0,0.12);
}

/* ── Drawer tabs ── */
.drawer__tab {
  color: var(--text-muted);
  border-bottom: 2px solid transparent;
  padding-bottom: var(--space-2);
  font-weight: 500;
  font-size: var(--text-sm);
  cursor: pointer;
}
.drawer__tab--active {
  color: var(--primary);
  border-bottom-color: var(--primary);
}
.drawer__tab:hover:not(.drawer__tab--active) {
  color: var(--text-secondary);
}

/* ── Confirm dialog (typed) ── */
.confirm-input {
  background: var(--bg-surface-2);
  border: 1px solid var(--border-default);
  color: var(--text-primary);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  font-family: var(--font-mono);
  width: 100%;
}
.confirm-input:focus {
  border-color: var(--error);
  outline: none;
}
```

### Token Quick Reference

| Property | Dark | Light |
|---|---|---|
| Modal/Drawer bg | `--bg-surface-1` → `#0D1526` | `--bg-surface-1` → `#FFFFFF` |
| Modal border | `--border-default` → `#334155` | `--border-subtle` → `#E2E8F0` |
| Title text | `--text-primary` → `#F1F5F9` | `--text-primary` → `#0F172A` |
| Divider line | `--border-subtle` | `--border-subtle` |
| Backdrop | `rgba(0,0,0,0.6)` | `rgba(15,23,42,0.35)` |
| Primary button | `--primary` → `#6366F1` | `--primary` → `#4F46E5` |
| Destructive button | `--error` → `#EF4444` | `--error` → `#DC2626` |
| Active tab | `--primary` border | `--primary` border |

---

## Usage in Page Specs

```markdown
### View Staff Profile
→ Component: [Side Drawer](../../components/02-modal-drawer.md) — width: default (480px)
  Tabs: [Profile] [Access Log] [Permissions]
  Tab: Profile
    - Avatar (96px), Name, Role badge, Division
    - Contact: Mobile (masked), Email
    - Access level: L3 — Operations
    - Status: Active | Suspended | Pending BGV
    - Created: [date] by [admin name]
    - Last login: [relative time]
  Tab: Access Log
    → Table of last 50 login events (datetime, IP, device, portal)
  Tab: Permissions
    → Permission matrix (which modules accessible)
```
