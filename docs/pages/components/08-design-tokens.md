# Component 08 — Design Tokens

> **Design Tokens** are the single source of truth for every visual decision in the EduForge Portal system. Every color, spacing value, shadow, radius, and typography value is defined here as a CSS custom property. All 12 component files and all 31 Division A page specs reference these token names — never raw hex values.
>
> The token system supports **two themes**: Dark (default for the Admin Portal) and Light (user-toggleable, also the default for School/Parent/Student portals). Themes are switched by setting `data-theme="dark"` or `data-theme="light"` on the `<html>` element.
>
> Full theme implementation, App Shell layout, and switching logic are documented in `00-global-layout.md`.

---

## 1. Theme Architecture

```css
/* ── Dark theme (default for admin portal) ── */
:root {
  /* Applied when no data-theme attribute is set, or when data-theme="dark" */
}

/* ── Light theme override ── */
[data-theme="light"] {
  /* Overrides every token that differs between dark and light */
}

/* ── System preference (respects OS setting when no explicit override) ── */
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    /* Same values as [data-theme="light"] */
  }
}
```

---

## 2. Background Color Tokens

> Backgrounds use a layered system. Base is the furthest-back surface; each surface level brings content progressively forward.

```css
:root {
  --bg-base:       #070C18;   /* Page background — darkest layer */
  --bg-surface-1:  #0D1526;   /* Cards, sidebar, top bar */
  --bg-surface-2:  #131F38;   /* Hover states, table header, input bg */
  --bg-surface-3:  #1A2744;   /* Nested cards, code blocks */
  --bg-overlay:    rgba(7, 12, 24, 0.8);  /* Modal/drawer backdrop base */
}

[data-theme="light"] {
  --bg-base:       #F8FAFC;
  --bg-surface-1:  #FFFFFF;
  --bg-surface-2:  #F1F5F9;
  --bg-surface-3:  #E2E8F0;
  --bg-overlay:    rgba(15, 23, 42, 0.35);
}
```

---

## 3. Text Color Tokens

```css
:root {
  --text-primary:    #F1F5F9;   /* Main content text, headings */
  --text-secondary:  #94A3B8;   /* Sub-text, descriptions, captions */
  --text-muted:      #64748B;   /* Placeholders, labels, metadata */
  --text-disabled:   #334155;   /* Disabled state text */
  --text-inverse:    #0F172A;   /* Text on light-colored backgrounds */
  --text-on-primary: #FFFFFF;   /* Text on primary-color backgrounds */
}

[data-theme="light"] {
  --text-primary:    #0F172A;
  --text-secondary:  #475569;
  --text-muted:      #64748B;
  --text-disabled:   #CBD5E1;
  --text-inverse:    #F8FAFC;
  --text-on-primary: #FFFFFF;
}
```

---

## 4. Border Color Tokens

```css
:root {
  --border-subtle:   #1E293B;   /* Between sections, card borders (inactive) */
  --border-default:  #334155;   /* Standard interactive borders */
  --border-strong:   #475569;   /* Emphasized borders, focused inputs */
  --border-focus:    var(--primary);   /* Focus ring */
}

[data-theme="light"] {
  --border-subtle:   #E2E8F0;
  --border-default:  #CBD5E1;
  --border-strong:   #94A3B8;
  --border-focus:    var(--primary);
}
```

---

## 5. Primary / Brand Color Tokens

> Each portal has its own primary color. The admin portal uses Indigo. All 11 portals listed below.

```css
/* ── Platform Admin Portal (Indigo) ── */
:root {
  --primary:            #6366F1;
  --primary-hover:      #818CF8;
  --primary-active:     #4F46E5;
  --primary-subtle:     color-mix(in srgb, #6366F1 12%, transparent);
  --primary-on:         #FFFFFF;   /* text on --primary background */
}

[data-theme="light"] {
  --primary:            #4F46E5;
  --primary-hover:      #4338CA;
  --primary-active:     #3730A3;
  --primary-subtle:     color-mix(in srgb, #4F46E5 10%, transparent);
  --primary-on:         #FFFFFF;
}
```

### Portal Primary Color Map

| Portal | Dark primary | Light primary | Identity |
|---|---|---|---|
| Platform Admin | `#6366F1` | `#4F46E5` | Indigo |
| School | `#3B82F6` | `#2563EB` | Blue |
| College | `#6366F1` | `#4F46E5` | Indigo |
| Coaching | `#EF4444` | `#DC2626` | Red |
| SSC Domain | `#10B981` | `#059669` | Green |
| RRB Domain | `#F59E0B` | `#D97706` | Orange |
| UPSC Domain | `#8B5CF6` | `#7C3AED` | Purple |
| Banking Domain | `#14B8A6` | `#0D9488` | Teal |
| Parent Portal | `#A78BFA` | `#7C3AED` | Violet |
| Student Portal | `#06B6D4` | `#0891B2` | Cyan |
| B2B Partner | `#64748B` | `#475569` | Slate |

---

## 6. Semantic / Status Color Tokens

```css
:root {
  /* Success — green */
  --success:            #10B981;
  --success-subtle:     color-mix(in srgb, #10B981 12%, transparent);
  --success-on:         #FFFFFF;

  /* Warning — amber */
  --warning:            #F59E0B;
  --warning-subtle:     color-mix(in srgb, #F59E0B 12%, transparent);
  --warning-on:         #000000;

  /* Error — red */
  --error:              #EF4444;
  --error-subtle:       color-mix(in srgb, #EF4444 12%, transparent);
  --error-on:           #FFFFFF;

  /* Info — same as primary */
  --info:               var(--primary);
  --info-subtle:        var(--primary-subtle);

  /* Special */
  --whatsapp:           #25D366;
  --whatsapp-dark:      #128C7E;
}

[data-theme="light"] {
  --success:            #059669;
  --success-subtle:     color-mix(in srgb, #059669 10%, transparent);

  --warning:            #D97706;
  --warning-subtle:     color-mix(in srgb, #D97706 10%, transparent);

  --error:              #DC2626;
  --error-subtle:       color-mix(in srgb, #DC2626 10%, transparent);
}
```

---

## 7. Typography Tokens

```css
:root {
  /* Font families */
  --font-sans:   'Inter', system-ui, -apple-system, sans-serif;
  --font-mono:   'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  --font-telugu: 'Noto Sans Telugu', sans-serif;
  --font-hindi:  'Noto Sans Devanagari', sans-serif;

  /* Type scale */
  --text-xs:     0.75rem;    /* 12px */
  --text-sm:     0.875rem;   /* 14px */
  --text-base:   1rem;       /* 16px */
  --text-lg:     1.125rem;   /* 18px */
  --text-xl:     1.25rem;    /* 20px */
  --text-2xl:    1.5rem;     /* 24px */
  --text-3xl:    1.875rem;   /* 30px */
  --text-4xl:    2.25rem;    /* 36px */
  --text-5xl:    3rem;       /* 48px */

  /* Line heights */
  --leading-tight:   1.2;
  --leading-snug:    1.375;
  --leading-normal:  1.5;
  --leading-relaxed: 1.625;
}
/* Typography tokens do not change between dark and light themes */
```

---

## 8. Spacing Tokens

```css
:root {
  --space-0:  0px;
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  20px;
  --space-6:  24px;
  --space-7:  28px;
  --space-8:  32px;
  --space-9:  36px;
  --space-10: 40px;
  --space-12: 48px;
  --space-14: 56px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
}
/* Spacing tokens do not change between themes */
```

---

## 9. Border Radius Tokens

```css
:root {
  --radius-xs:   2px;
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-xl:   16px;
  --radius-2xl:  24px;
  --radius-3xl:  32px;
  --radius-full: 9999px;
}
/* Border radius tokens do not change between themes */
```

---

## 10. Shadow / Elevation Tokens

```css
/* Dark theme shadows — brighter, more visible against dark surfaces */
:root {
  --shadow-sm:  0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md:  0 4px 12px rgba(0, 0, 0, 0.4);
  --shadow-lg:  0 8px 24px rgba(0, 0, 0, 0.5);
  --shadow-xl:  0 16px 48px rgba(0, 0, 0, 0.6);
  --shadow-2xl: 0 24px 64px rgba(0, 0, 0, 0.7);

  /* Primary glow (used on focused elements, active cards) */
  --shadow-primary: 0 0 0 3px color-mix(in srgb, var(--primary) 30%, transparent);
  --shadow-error:   0 0 0 3px color-mix(in srgb, var(--error)   30%, transparent);
}

/* Light theme shadows — softer, more subtle */
[data-theme="light"] {
  --shadow-sm:  0 1px 2px rgba(0, 0, 0, 0.06), 0 1px 3px rgba(0, 0, 0, 0.04);
  --shadow-md:  0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04);
  --shadow-lg:  0 8px 24px rgba(0, 0, 0, 0.10), 0 4px 8px rgba(0, 0, 0, 0.06);
  --shadow-xl:  0 16px 40px rgba(0, 0, 0, 0.12), 0 8px 16px rgba(0, 0, 0, 0.08);
  --shadow-2xl: 0 24px 64px rgba(0, 0, 0, 0.14), 0 12px 24px rgba(0, 0, 0, 0.08);
}
```

---

## 11. Z-Index Layer Tokens

```css
:root {
  --z-page:             0;
  --z-raised:           10;
  --z-sticky:           100;
  --z-dropdown:         200;
  --z-topbar:           300;
  --z-sidebar:          400;
  --z-drawer:           600;
  --z-modal:            800;
  --z-command-palette:  900;
  --z-toast:            1000;
  --z-critical:         9999;
}
/* Z-index tokens do not change between themes */
```

---

## 12. Motion / Animation Tokens

```css
:root {
  --duration-instant:   0ms;
  --duration-fast:      100ms;
  --duration-default:   200ms;
  --duration-medium:    300ms;
  --duration-slow:      500ms;
  --duration-page:      400ms;

  --ease-out:           cubic-bezier(0.0, 0.0, 0.2, 1);
  --ease-in:            cubic-bezier(0.4, 0.0, 1, 1);
  --ease-in-out:        cubic-bezier(0.4, 0.0, 0.2, 1);
  --ease-spring:        cubic-bezier(0.16, 1, 0.3, 1);
  --ease-bounce:        cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Respect reduced-motion preference */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration:  0.01ms !important;
    animation-duration:   0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
```

---

## 13. Breakpoint Tokens

```css
/* Used as min-width values in @media queries */
:root {
  --bp-sm:   480px;     /* Mobile landscape */
  --bp-md:   768px;     /* Tablet */
  --bp-lg:   1024px;    /* Desktop S — sidebar appears */
  --bp-xl:   1280px;    /* Desktop M — sidebar 240px default */
  --bp-2xl:  1536px;    /* Desktop L — max content width 1400px */
}
```

---

## 14. Complete Token Diff: Dark vs Light

> This table shows every token that differs between dark and light themes. Tokens not listed here are identical in both themes.

| Token | Dark | Light |
|---|---|---|
| `--bg-base` | `#070C18` | `#F8FAFC` |
| `--bg-surface-1` | `#0D1526` | `#FFFFFF` |
| `--bg-surface-2` | `#131F38` | `#F1F5F9` |
| `--bg-surface-3` | `#1A2744` | `#E2E8F0` |
| `--bg-overlay` | `rgba(7,12,24,0.8)` | `rgba(15,23,42,0.35)` |
| `--text-primary` | `#F1F5F9` | `#0F172A` |
| `--text-secondary` | `#94A3B8` | `#475569` |
| `--text-disabled` | `#334155` | `#CBD5E1` |
| `--border-subtle` | `#1E293B` | `#E2E8F0` |
| `--border-default` | `#334155` | `#CBD5E1` |
| `--border-strong` | `#475569` | `#94A3B8` |
| `--primary` | `#6366F1` | `#4F46E5` |
| `--primary-hover` | `#818CF8` | `#4338CA` |
| `--primary-active` | `#4F46E5` | `#3730A3` |
| `--success` | `#10B981` | `#059669` |
| `--warning` | `#F59E0B` | `#D97706` |
| `--error` | `#EF4444` | `#DC2626` |
| `--shadow-sm` | `rgba(0,0,0,0.3)` based | `rgba(0,0,0,0.06)` based |
| `--shadow-md` | `rgba(0,0,0,0.4)` based | `rgba(0,0,0,0.08)` based |
| `--shadow-lg` | `rgba(0,0,0,0.5)` based | `rgba(0,0,0,0.10)` based |
| `--shadow-xl` | `rgba(0,0,0,0.6)` based | `rgba(0,0,0,0.12)` based |

---

## 15. Full :root Block (Copy-Paste Ready)

```css
/* ============================================================
   EDUFORGE PORTAL DESIGN TOKENS
   Dark theme (default) + Light theme override
   Apply to global CSS file loaded by all portals.
   ============================================================ */

:root {
  /* Backgrounds */
  --bg-base:       #070C18;
  --bg-surface-1:  #0D1526;
  --bg-surface-2:  #131F38;
  --bg-surface-3:  #1A2744;
  --bg-overlay:    rgba(7, 12, 24, 0.8);

  /* Text */
  --text-primary:    #F1F5F9;
  --text-secondary:  #94A3B8;
  --text-muted:      #64748B;
  --text-disabled:   #334155;
  --text-inverse:    #0F172A;
  --text-on-primary: #FFFFFF;

  /* Borders */
  --border-subtle:   #1E293B;
  --border-default:  #334155;
  --border-strong:   #475569;

  /* Primary (Admin Portal — Indigo) */
  --primary:          #6366F1;
  --primary-hover:    #818CF8;
  --primary-active:   #4F46E5;
  --primary-subtle:   color-mix(in srgb, #6366F1 12%, transparent);
  --primary-on:       #FFFFFF;

  /* Status */
  --success:          #10B981;
  --success-subtle:   color-mix(in srgb, #10B981 12%, transparent);
  --warning:          #F59E0B;
  --warning-subtle:   color-mix(in srgb, #F59E0B 12%, transparent);
  --error:            #EF4444;
  --error-subtle:     color-mix(in srgb, #EF4444 12%, transparent);
  --info:             var(--primary);
  --info-subtle:      var(--primary-subtle);
  --whatsapp:         #25D366;

  /* Shadows */
  --shadow-sm:  0 1px 2px rgba(0,0,0,0.3);
  --shadow-md:  0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg:  0 8px 24px rgba(0,0,0,0.5);
  --shadow-xl:  0 16px 48px rgba(0,0,0,0.6);
  --shadow-2xl: 0 24px 64px rgba(0,0,0,0.7);
  --shadow-primary: 0 0 0 3px color-mix(in srgb, var(--primary) 30%, transparent);
  --shadow-error:   0 0 0 3px color-mix(in srgb, var(--error) 30%, transparent);

  /* Typography */
  --font-sans:  'Inter', system-ui, -apple-system, sans-serif;
  --font-mono:  'JetBrains Mono', 'Fira Code', monospace;
  --text-xs:    0.75rem;
  --text-sm:    0.875rem;
  --text-base:  1rem;
  --text-lg:    1.125rem;
  --text-xl:    1.25rem;
  --text-2xl:   1.5rem;
  --text-3xl:   1.875rem;
  --text-4xl:   2.25rem;
  --text-5xl:   3rem;

  /* Spacing */
  --space-1: 4px;  --space-2: 8px;   --space-3: 12px; --space-4: 16px;
  --space-5: 20px; --space-6: 24px;  --space-7: 28px; --space-8: 32px;
  --space-10: 40px; --space-12: 48px; --space-16: 64px; --space-20: 80px;

  /* Border radius */
  --radius-xs: 2px;  --radius-sm: 4px;  --radius-md: 8px;
  --radius-lg: 12px; --radius-xl: 16px; --radius-2xl: 24px;
  --radius-full: 9999px;

  /* Z-index */
  --z-page: 0;        --z-raised: 10;    --z-sticky: 100;
  --z-dropdown: 200;  --z-topbar: 300;   --z-sidebar: 400;
  --z-drawer: 600;    --z-modal: 800;    --z-command-palette: 900;
  --z-toast: 1000;    --z-critical: 9999;

  /* Motion */
  --duration-fast: 100ms; --duration-default: 200ms;
  --duration-medium: 300ms; --duration-slow: 500ms;
  --ease-out: cubic-bezier(0.0, 0.0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0.0, 0.2, 1);
  --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
}

/* ── Light theme overrides ── */
[data-theme="light"] {
  --bg-base:       #F8FAFC;
  --bg-surface-1:  #FFFFFF;
  --bg-surface-2:  #F1F5F9;
  --bg-surface-3:  #E2E8F0;
  --bg-overlay:    rgba(15, 23, 42, 0.35);

  --text-primary:   #0F172A;
  --text-secondary: #475569;
  --text-disabled:  #CBD5E1;
  --text-inverse:   #F8FAFC;

  --border-subtle:  #E2E8F0;
  --border-default: #CBD5E1;
  --border-strong:  #94A3B8;

  --primary:        #4F46E5;
  --primary-hover:  #4338CA;
  --primary-active: #3730A3;
  --primary-subtle: color-mix(in srgb, #4F46E5 10%, transparent);

  --success: #059669;  --success-subtle: color-mix(in srgb, #059669 10%, transparent);
  --warning: #D97706;  --warning-subtle: color-mix(in srgb, #D97706 10%, transparent);
  --error:   #DC2626;  --error-subtle:   color-mix(in srgb, #DC2626 10%, transparent);

  --shadow-sm:  0 1px 2px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04);
  --shadow-md:  0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
  --shadow-lg:  0 8px 24px rgba(0,0,0,0.10), 0 4px 8px rgba(0,0,0,0.06);
  --shadow-xl:  0 16px 40px rgba(0,0,0,0.12), 0 8px 16px rgba(0,0,0,0.08);
  --shadow-2xl: 0 24px 64px rgba(0,0,0,0.14), 0 12px 24px rgba(0,0,0,0.08);
}

/* ── System preference fallback ── */
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) {
    --bg-base: #F8FAFC; --bg-surface-1: #FFFFFF; --bg-surface-2: #F1F5F9;
    --bg-surface-3: #E2E8F0; --bg-overlay: rgba(15, 23, 42, 0.35);
    --text-primary: #0F172A; --text-secondary: #475569;
    --text-disabled: #CBD5E1; --text-inverse: #F8FAFC;
    --border-subtle: #E2E8F0; --border-default: #CBD5E1; --border-strong: #94A3B8;
    --primary: #4F46E5; --primary-hover: #4338CA; --primary-active: #3730A3;
    --success: #059669; --warning: #D97706; --error: #DC2626;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.06); --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
    --shadow-lg: 0 8px 24px rgba(0,0,0,0.10); --shadow-xl: 0 16px 40px rgba(0,0,0,0.12);
  }
}

/* ── Reduced motion ── */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
```

---

*Component: `08-design-tokens.md` | Scope: Global — all portals | Updated: 2026-03*
