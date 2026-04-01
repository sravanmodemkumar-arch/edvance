# Component 12 — Command Palette (⌘K)

> The **Command Palette** is the universal keyboard-first navigation and action launcher for the EduForge Admin Portal. It is triggered by pressing `⌘K` (Mac) or `Ctrl+K` (Windows/Linux) from anywhere in the portal and allows staff to navigate to any page, execute any action, search institutions, look up students, and run admin commands — all without touching the mouse.
>
> At the scale EduForge operates (81 staff roles, 1,900+ institutions, 2.4M+ students, 31 pages in Division A alone), the command palette is not a convenience — it is a productivity multiplier. A CEO or COO who needs to jump between the WAR ROOM, an institution's detail page, and a financial report in rapid succession would lose significant time navigating the sidebar each time. The command palette collapses that friction to a single keystroke + a few characters.
>
> The palette renders as a full-overlay modal with a centered search input, categorized results, keyboard navigation, and instant filtering as the user types. All results are role-filtered — a user with access level L1 (CFO) will only see finance and compliance actions, not infrastructure commands.
>
> Both dark and light themes are fully supported using CSS custom property tokens from `00-global-layout.md`.

---

## 1. Anatomy

```
┌──────────────────────────────────────────────────────────────────────────┐
│  BACKDROP (full-screen semi-transparent overlay, click to close)         │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │  🔍  Search pages, actions, institutions...            ⌘K / Esc  │   │  ← Search input
│   ├──────────────────────────────────────────────────────────────────┤   │
│   │                                                                  │   │
│   │  RECENT                                                          │   │  ← Category header
│   │  ▸  Executive Dashboard           /portal/exec/overview         │   │  ← Result item
│   │  ▸  WAR ROOM – Live Ops           /portal/exec/war-room         │   │
│   │                                                                  │   │
│   │  PAGES                                                           │   │
│   │  ▸  Financial Overview            /portal/exec/finance          │   │
│   │  ▸  Platform Health               /portal/exec/platform-health  │   │
│   │                                                                  │   │
│   │  ACTIONS                                                         │   │
│   │  ▸  Open P0 Incident              Exec action                   │   │
│   │  ▸  Generate Platform Report      Exec action                   │   │
│   │                                                                  │   │
│   │  INSTITUTIONS (search)                                           │   │
│   │  ▸  IIT Bombay                    College · ID: COL-0042        │   │
│   │                                                                  │   │
│   ├──────────────────────────────────────────────────────────────────┤   │
│   │  ↑↓ Navigate  ↵ Open  ⌘↵ Open in new tab  Esc Close            │   │  ← Keyboard hint bar
│   └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

| Region | Purpose |
|---|---|
| **Backdrop** | Full-screen semi-transparent overlay. Click to close. |
| **Search Input** | Autofocused on open. Placeholder text explains scope. Keyboard shortcut badge at right. |
| **Result List** | Scrollable, grouped by category. Max height: 480px. |
| **Category Header** | Labels result groups (RECENT, PAGES, ACTIONS, INSTITUTIONS, PEOPLE, SETTINGS). |
| **Result Item** | Each result: icon + label + description/path + optional keyboard shortcut badge. |
| **Keyboard Hint Bar** | Fixed at bottom of palette. Shows active keyboard shortcuts. |

---

## 2. Result Categories

> Results are grouped and prioritized in this order:

| Priority | Category | Contains | Max items shown |
|---|---|---|---|
| 1 | **RECENT** | Last 5 pages/actions visited | 5 |
| 2 | **PAGES** | All pages accessible to the user's role | 10 (more on scroll) |
| 3 | **ACTIONS** | Role-gated admin actions (Open Incident, Schedule Maintenance, etc.) | 8 |
| 4 | **INSTITUTIONS** | Live search: schools, colleges, groups, coaching centers | 5 |
| 5 | **PEOPLE** | Staff directory search, student lookup | 5 |
| 6 | **SETTINGS** | System settings, feature flags, config items | 5 |

> When the user types a query, all categories filter simultaneously. Categories with 0 results are hidden entirely to reduce visual noise.

---

## 3. Result Item Structure

```html
<li class="cp-result" role="option" aria-selected="false" data-index="0">
  <span class="cp-result__icon" aria-hidden="true">📊</span>
  <span class="cp-result__body">
    <span class="cp-result__label">Executive Dashboard</span>
    <span class="cp-result__meta">/portal/exec/overview</span>
  </span>
  <kbd class="cp-result__shortcut">G D</kbd>   <!-- optional -->
</li>
```

**Highlighted state** (keyboard-selected):
```css
.cp-result[aria-selected="true"],
.cp-result:hover {
  background: var(--bg-surface-2);
  border-radius: var(--radius-md);
}

.cp-result[aria-selected="true"] .cp-result__label {
  color: var(--text-primary);
}

/* Highlight matching query text within label */
.cp-result__label mark {
  background: color-mix(in srgb, var(--primary) 25%, transparent);
  color: var(--primary);
  border-radius: 2px;
  font-style: normal;
}

[data-theme="light"] .cp-result__label mark {
  background: color-mix(in srgb, var(--primary) 15%, transparent);
  color: var(--primary);
}
```

---

## 4. Full HTML Structure

```html
<!-- Backdrop -->
<div class="cp-backdrop"
     role="dialog"
     aria-modal="true"
     aria-label="Command Palette"
     id="command-palette">

  <!-- Palette box -->
  <div class="cp-box" role="combobox" aria-expanded="true" aria-haspopup="listbox">

    <!-- Search input -->
    <div class="cp-search-wrap">
      <svg class="cp-search-icon" aria-hidden="true"><!-- search icon --></svg>
      <input
        class="cp-input"
        type="text"
        placeholder="Search pages, actions, institutions..."
        autocomplete="off"
        spellcheck="false"
        aria-autocomplete="list"
        aria-controls="cp-results"
        aria-activedescendant=""
        id="cp-input"
        autofocus
      />
      <kbd class="cp-esc-badge">Esc</kbd>
    </div>

    <!-- Results list -->
    <ul class="cp-results" id="cp-results" role="listbox" aria-label="Results">

      <!-- Category group -->
      <li class="cp-group" role="presentation">
        <span class="cp-group__header" role="separator">RECENT</span>
        <ul class="cp-group__list" role="group">
          <li class="cp-result" role="option" aria-selected="true" id="cp-result-0">
            <span class="cp-result__icon" aria-hidden="true">🏠</span>
            <span class="cp-result__body">
              <span class="cp-result__label">Executive Dashboard</span>
              <span class="cp-result__meta">/portal/exec/overview</span>
            </span>
            <kbd class="cp-result__shortcut">G D</kbd>
          </li>
        </ul>
      </li>

      <!-- Empty state (shown when query has no results) -->
      <li class="cp-empty" role="presentation" hidden>
        <span class="cp-empty__icon">🔍</span>
        <p class="cp-empty__text">No results for "<span class="cp-empty__query"></span>"</p>
        <p class="cp-empty__hint">Try searching for a page name, institution, or action</p>
      </li>

    </ul>

    <!-- Keyboard hint bar -->
    <div class="cp-hints" aria-hidden="true">
      <span><kbd>↑↓</kbd> Navigate</span>
      <span><kbd>↵</kbd> Open</span>
      <span><kbd>⌘↵</kbd> New tab</span>
      <span><kbd>Esc</kbd> Close</span>
    </div>

  </div>
</div>
```

---

## 5. Full CSS

```css
/* ============================================================
   COMMAND PALETTE — EduForge Admin Portal
   Triggered by ⌘K / Ctrl+K from anywhere in the portal
   Dark (default) + Light theme via data-theme="light"
   Z-index: var(--z-command-palette) = 900 (from 00-global-layout.md)
   Tokens: 00-global-layout.md
   ============================================================ */

/* ── Backdrop ── */
.cp-backdrop {
  position: fixed;
  inset: 0;
  z-index: var(--z-command-palette);   /* 900 */
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 10vh;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  animation: cp-backdrop-in 120ms ease-out;
}

/* Light theme backdrop is lighter */
[data-theme="light"] .cp-backdrop {
  background: rgba(15, 23, 42, 0.4);
}

@keyframes cp-backdrop-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* ── Palette box ── */
.cp-box {
  width: 100%;
  max-width: 640px;
  background: var(--bg-surface-1);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-xl);
  animation: cp-box-in 150ms cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  max-height: 80vh;
}

/* Dark theme box */
:root .cp-box {
  background: var(--bg-surface-1);     /* #0D1526 */
  border-color: var(--border-default); /* #334155 */
  box-shadow:
    0 25px 50px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(99, 102, 241, 0.1);  /* faint primary glow */
}

/* Light theme box */
[data-theme="light"] .cp-box {
  background: var(--bg-surface-1);     /* #FFFFFF */
  border-color: var(--border-default); /* #CBD5E1 */
  box-shadow:
    0 25px 50px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(79, 70, 229, 0.08);
}

@keyframes cp-box-in {
  from { opacity: 0; transform: scale(0.96) translateY(-8px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}

/* ── Search wrap ── */
.cp-search-wrap {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--border-subtle);
}

/* ── Search icon ── */
.cp-search-icon {
  width: 18px; height: 18px;
  color: var(--text-muted);
  flex-shrink: 0;
}

/* ── Input ── */
.cp-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-family: var(--font-sans);
  font-size: var(--text-base);
  color: var(--text-primary);
  caret-color: var(--primary);
}

.cp-input::placeholder {
  color: var(--text-muted);
}

:root .cp-input {
  color: var(--text-primary);   /* #F1F5F9 */
}

[data-theme="light"] .cp-input {
  color: var(--text-primary);   /* #0F172A */
}

/* ── Esc badge ── */
.cp-esc-badge {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  background: var(--bg-surface-2);
  border: 1px solid var(--border-subtle);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}

/* ── Results list ── */
.cp-results {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-2) var(--space-3);
  list-style: none;
  margin: 0;
  scrollbar-width: thin;
  scrollbar-color: var(--border-default) transparent;
}

.cp-results::-webkit-scrollbar { width: 4px; }
.cp-results::-webkit-scrollbar-track { background: transparent; }
.cp-results::-webkit-scrollbar-thumb { background: var(--border-default); border-radius: 2px; }

/* ── Category group ── */
.cp-group { margin-bottom: var(--space-2); }
.cp-group__list { list-style: none; padding: 0; margin: 0; }

.cp-group__header {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  padding: var(--space-2) var(--space-2) var(--space-1);
  text-transform: uppercase;
}

/* ── Result item ── */
.cp-result {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 80ms ease;
  user-select: none;
}

.cp-result:hover,
.cp-result[aria-selected="true"] {
  background: var(--bg-surface-2);
}

:root .cp-result:hover,
:root .cp-result[aria-selected="true"] {
  background: var(--bg-surface-2);   /* #131F38 */
}

[data-theme="light"] .cp-result:hover,
[data-theme="light"] .cp-result[aria-selected="true"] {
  background: var(--bg-surface-2);   /* #F1F5F9 */
}

/* ── Result icon ── */
.cp-result__icon {
  width: 28px; height: 28px;
  display: flex; align-items: center; justify-content: center;
  background: var(--bg-surface-2);
  border-radius: var(--radius-md);
  font-size: 14px;
  flex-shrink: 0;
}

.cp-result[aria-selected="true"] .cp-result__icon {
  background: color-mix(in srgb, var(--primary) 15%, transparent);
}

/* ── Result body ── */
.cp-result__body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.cp-result__label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cp-result__meta {
  font-size: var(--text-xs);
  color: var(--text-muted);
  font-family: var(--font-mono);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ── Highlighted match text ── */
.cp-result__label mark {
  background: color-mix(in srgb, var(--primary) 25%, transparent);
  color: var(--primary);
  border-radius: 2px;
  font-style: normal;
  padding: 0 1px;
}

[data-theme="light"] .cp-result__label mark {
  background: color-mix(in srgb, var(--primary) 15%, transparent);
  color: var(--primary);
}

/* ── Keyboard shortcut badge ── */
.cp-result__shortcut {
  font-size: 10px;
  font-weight: 600;
  font-family: var(--font-mono);
  color: var(--text-muted);
  background: var(--bg-surface-2);
  border: 1px solid var(--border-subtle);
  padding: 1px 5px;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
  margin-left: auto;
}

/* ── Keyboard hint bar ── */
.cp-hints {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-3) var(--space-5);
  border-top: 1px solid var(--border-subtle);
}

.cp-hints span {
  font-size: 11px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.cp-hints kbd {
  font-size: 10px;
  font-family: var(--font-mono);
  color: var(--text-muted);
  background: var(--bg-surface-2);
  border: 1px solid var(--border-subtle);
  border-bottom-width: 2px;
  padding: 1px 4px;
  border-radius: var(--radius-sm);
}

/* ── Empty state ── */
.cp-empty {
  text-align: center;
  padding: var(--space-10) var(--space-5);
}

.cp-empty__icon {
  font-size: 2rem;
  display: block;
  margin-bottom: var(--space-3);
  opacity: 0.4;
}

.cp-empty__text {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-1);
}

.cp-empty__hint {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

/* ── Loading state (spinner while async search fires) ── */
.cp-search-wrap--loading .cp-search-icon {
  animation: spin 800ms linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

/* ── Separator line between groups ── */
.cp-separator {
  height: 1px;
  background: var(--border-subtle);
  margin: var(--space-2) 0;
}
```

---

## 6. Keyboard Interaction Model

> The command palette is a fully keyboard-operated component. Mouse interaction is secondary. All state transitions have keyboard equivalents.

| Key | Action |
|---|---|
| `⌘K` / `Ctrl+K` | Open palette from anywhere in the portal |
| `Esc` | Close palette, restore focus to previous element |
| `↑` / `↓` | Move selection up/down through results |
| `↵ Enter` | Navigate to selected result / execute action |
| `⌘↵` / `Ctrl+Enter` | Open selected result in a new browser tab |
| `Tab` | Move to next result (same as ↓) |
| `Shift+Tab` | Move to previous result (same as ↑) |
| Any character | Types into search input, filters results instantly |
| `Backspace` | Removes last character from search input |

**Focus trap:** While the palette is open, Tab focus is trapped inside the `cp-box`. It cannot escape to the page behind.

**Restore focus:** On close, keyboard focus returns to the element that was focused when the palette was opened.

---

## 7. Role-Filtered Results

> Results are role-filtered server-side based on the JWT claims (`access_level`, `division`) in the user's session. The frontend palette component renders only what the API returns. This ensures that a CFO (L1) never sees infrastructure commands and a Platform Ops role never sees financial actions.

```
CEO (L5)         → All pages, all actions, all entities
CTO (L5)         → All pages except Finance — heavy emphasis on Infra, Platform
COO (L3)         → Ops, institutions, compliance — no raw finance figures
CFO (L1)         → Finance, compliance, billing — no infra commands
Platform Ops     → Their division's pages + cross-platform read-only
```

---

## 8. Action Items (not just navigation)

> The command palette can execute **actions** directly, not just navigate to pages. Actions trigger backend API calls or UI state changes.

**Examples of available actions (role-gated):**

| Action | Roles | What it does |
|---|---|---|
| "Open P0 Incident" | CEO, COO, CTO, Platform Ops | Opens the new incident drawer prefilled with P0 severity |
| "Schedule Maintenance Window" | CTO, Platform Ops | Opens the maintenance scheduling modal |
| "Generate Platform Report" | CEO, COO, CFO | Triggers async PDF report generation |
| "Switch Theme" | All roles | Toggles `data-theme` between dark/light |
| "Go to Keyboard Shortcuts" | All roles | Opens the `?` keyboard shortcuts modal |
| "Export Current Table" | All roles | Triggers CSV export on the currently visible table |

---

## 9. Dark + Light Theme Token Reference

| Property | Dark value | Light value |
|---|---|---|
| Backdrop | `rgba(0,0,0,0.6)` + `blur(4px)` | `rgba(15,23,42,0.4)` + `blur(4px)` |
| Box background | `--bg-surface-1` → `#0D1526` | `--bg-surface-1` → `#FFFFFF` |
| Box border | `--border-default` → `#334155` | `--border-default` → `#CBD5E1` |
| Box shadow | Dark deep shadow + primary glow | Light shadow + primary glow |
| Input text | `--text-primary` → `#F1F5F9` | `--text-primary` → `#0F172A` |
| Input placeholder | `--text-muted` → `#64748B` | `--text-muted` → `#64748B` |
| Input caret | `--primary` → `#6366F1` | `--primary` → `#4F46E5` |
| Search divider | `--border-subtle` → `#1E293B` | `--border-subtle` → `#E2E8F0` |
| Result hover bg | `--bg-surface-2` → `#131F38` | `--bg-surface-2` → `#F1F5F9` |
| Result label | `--text-primary` | `--text-primary` |
| Result meta | `--text-muted` → `#64748B` | `--text-muted` → `#64748B` |
| Match highlight | primary 25% tint | primary 15% tint |
| Shortcut badge | `--bg-surface-2` + `--border-subtle` | same (token-based) |
| Hint bar divider | `--border-subtle` | `--border-subtle` |
| Category header | `--text-muted` | `--text-muted` |

---

## 10. Usage Examples (for Page Specs)

```markdown
### Keyboard Shortcuts
> ⌘K opens the Command Palette (Component 12) from any point on this page.
> The palette is pre-seeded with RECENT entries from the user's last 5 navigation actions.
> Actions specific to this page (Export Report, Open Incident, Schedule Maintenance)
> appear in the ACTIONS section with appropriate role-gating applied.
```

---

*Component: `12-command-palette.md` | Scope: Global — all portals | Theme: Dark (default) + Light | Updated: 2026-03*
