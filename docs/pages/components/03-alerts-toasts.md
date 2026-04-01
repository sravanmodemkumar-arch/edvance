# Component: Alerts, Toasts, Banners, Empty States

---

## Toast Notification

> Temporary message. Auto-dismisses. Does not block interaction.

### Position
Top-right corner on desktop. Top-center on mobile. Z-index: 1200.

### Layout
```
┌────────────────────────────────────────┐
│  [✅ Icon]  Message text here   [✕]   │
│             Optional sub-text          │
└────────────────────────────────────────┘
```

### Variants

| Type | Icon | Color token | Dark hex | Light hex | Auto-dismiss |
|---|---|---|---|---|---|
| `success` | ✅ | `--success` | `#10B981` | `#059669` | 4 seconds |
| `error` | ❌ | `--error` | `#EF4444` | `#DC2626` | 8 seconds |
| `warning` | ⚠️ | `--warning` | `#F59E0B` | `#D97706` | 6 seconds |
| `info` | ℹ️ | `--primary` | `#6366F1` | `#4F46E5` | 4 seconds |
| `loading` | ⏳ spinner | `--text-muted` | `#64748B` | `#64748B` | Never |

### Behavior

| Property | Spec |
|---|---|
| Stack | Max 3 toasts visible. 4th pushes oldest off. |
| Hover pause | Mouse hover pauses auto-dismiss timer |
| Dismiss | [✕] button always present. Click = immediate dismiss |
| Action | Optional action link inside toast: "Undo", "View", "Retry" |
| Animation | Slide in from right (desktop) / top (mobile), 200ms |
| Queue | Rapid triggers queue — each waits for previous to dismiss |

### Usage
```markdown
→ Toast: success — "Student enrolled successfully"
→ Toast: error — "Failed to send OTP. Retry?" [Retry action]
→ Toast: loading — "Exporting 1,247 records..."
```

---

## Alert Banner

> Persistent, inline. Does not auto-dismiss. Requires user action or stays until condition resolves.

### When to Use
- Form validation summary (multiple errors)
- Page-level warnings (subscription expiring, BGV pending)
- Informational notices (exam in progress, maintenance window)

### Layout
```
┌────────────────────────────────────────────────────────────────┐
│ [⚠️]  15 staff members have pending BGV verification.          │
│        Complete before 31 March or access will be suspended.   │
│                         [Review Now]           [Dismiss] [✕]  │
└────────────────────────────────────────────────────────────────┘
```

### Variants

| Type | Left border token | Background (dark) | Background (light) | Icon |
|---|---|---|---|---|
| `error` | `--error` | `error` 6% tint | `#FEF2F2` | ❌ |
| `warning` | `--warning` | `warning` 6% tint | `#FFFBEB` | ⚠️ |
| `info` | `--primary` | `primary` 6% tint | `#EEF2FF` | ℹ️ |
| `success` | `--success` | `success` 6% tint | `#F0FDF4` | ✅ |
| `neutral` | `--border-default` | `--bg-surface-2` | `#F8FAFC` | 📋 |

### Placement
- **Page-level:** Below page header, above page content. Full-width.
- **Section-level:** Inside a card or form section. Scoped width.
- **Form inline:** Below the specific field with error. Not full-width.

---

## Confirm Dialog

> Blocking modal. User MUST respond before continuing.
> See also [02-modal-drawer.md](02-modal-drawer.md) for modal specs.

### Variants

| Type | Icon | Primary button | Use Case |
|---|---|---|---|
| `confirm` | ❓ | Blue "Confirm" | Non-destructive — change role, send notification |
| `danger` | ⚠️ | Red "Delete" / "Suspend" | Destructive — irreversible actions |
| `typed-confirm` | ⚠️ | Red, disabled until typed | Highly destructive — permanent delete, data wipe |

### Typed Confirm Pattern (Destructive)
```
┌────────────────────────────────────────────┐
│  ⚠️  Permanently delete XYZ School?        │
│                                            │
│  This will delete 1,247 students,          │
│  all exam records, and fee history.        │
│  This action CANNOT be undone.             │
│                                            │
│  Type the institution name to confirm:     │
│  ┌──────────────────────────────────────┐  │
│  │  XYZ School                          │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  [Cancel]          [Delete — IRREVERSIBLE] │
│                    (red, enabled only when │
│                     text matches exactly)  │
└────────────────────────────────────────────┘
```

---

## Empty State

> Shown when a list/table has no data.

### Layout
```
┌────────────────────────────────────────────────────┐
│                                                    │
│          [Context-appropriate illustration]        │
│                                                    │
│          No [entity] found                         │
│                                                    │
│     [Contextual message — why it's empty]          │
│     e.g. "No students match your current filters"  │
│                                                    │
│     [Primary CTA]          [Secondary CTA]         │
│     e.g. "Add Student"     "Clear Filters"         │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Empty State Types

| Scenario | Heading | Primary CTA |
|---|---|---|
| No data at all (fresh) | "No [items] yet" | "Add first [item]" |
| Filtered with no results | "No results for '[query]'" | "Clear filters" |
| No permission to view | "You don't have access to this" | "Request access" |
| Error loading | "Failed to load [items]" | "Retry" |
| Feature not enabled | "[Feature] is not enabled" | "Contact admin" |
| Search no results | "No results for '[search term]'" | "Try different keywords" |

---

## Theme Support (Dark + Light)

```css
/* ── Toast ── */
.toast {
  background: var(--bg-surface-1);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  color: var(--text-primary);
}

/* Dark */
:root .toast {
  background: var(--bg-surface-1);    /* #0D1526 */
  border-color: var(--border-default);
}

/* Light */
[data-theme="light"] .toast {
  background: #FFFFFF;
  border-color: var(--border-subtle);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

/* Toast variants — left accent bar */
.toast--success { border-left: 3px solid var(--success); }
.toast--error   { border-left: 3px solid var(--error); }
.toast--warning { border-left: 3px solid var(--warning); }
.toast--info    { border-left: 3px solid var(--primary); }

.toast__icon--success { color: var(--success); }
.toast__icon--error   { color: var(--error); }
.toast__icon--warning { color: var(--warning); }
.toast__icon--info    { color: var(--primary); }

/* ── Alert Banner ── */
.alert-banner {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  border-left-width: 4px;
  border-left-style: solid;
}

.alert-banner--error {
  border-left-color: var(--error);
  background: color-mix(in srgb, var(--error) 6%, var(--bg-surface-1));
}
.alert-banner--warning {
  border-left-color: var(--warning);
  background: color-mix(in srgb, var(--warning) 6%, var(--bg-surface-1));
}
.alert-banner--info {
  border-left-color: var(--primary);
  background: color-mix(in srgb, var(--primary) 6%, var(--bg-surface-1));
}
.alert-banner--success {
  border-left-color: var(--success);
  background: color-mix(in srgb, var(--success) 6%, var(--bg-surface-1));
}
.alert-banner--neutral {
  border-left-color: var(--border-default);
  background: var(--bg-surface-2);
}

/* Light theme banners use same token system — lighter tints look correct */
[data-theme="light"] .alert-banner--error {
  background: #FEF2F2;
}
[data-theme="light"] .alert-banner--warning {
  background: #FFFBEB;
}
[data-theme="light"] .alert-banner--info {
  background: #EEF2FF;
}
[data-theme="light"] .alert-banner--success {
  background: #F0FDF4;
}
[data-theme="light"] .alert-banner--neutral {
  background: #F8FAFC;
}

/* Alert text */
.alert-banner__message { color: var(--text-primary); font-size: var(--text-sm); }
.alert-banner__subtext { color: var(--text-secondary); font-size: var(--text-xs); margin-top: var(--space-1); }

/* ── Empty state ── */
.empty-state {
  text-align: center;
  padding: var(--space-12) var(--space-6);
}
.empty-state__heading {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}
.empty-state__message { color: var(--text-secondary); font-size: var(--text-sm); }
```

### Token Quick Reference

| Property | Dark | Light |
|---|---|---|
| Toast bg | `--bg-surface-1` → `#0D1526` | `#FFFFFF` |
| Toast border | `--border-default` | `--border-subtle` |
| Success color | `--success` → `#10B981` | `--success` → `#059669` |
| Error color | `--error` → `#EF4444` | `--error` → `#DC2626` |
| Warning color | `--warning` → `#F59E0B` | `--warning` → `#D97706` |
| Info color | `--primary` → `#6366F1` | `--primary` → `#4F46E5` |
| Banner bg (error) | `error` 6% tint on surface | `#FEF2F2` |
| Banner bg (warning) | `warning` 6% tint on surface | `#FFFBEB` |

---

## Usage in Page Specs

```markdown
→ Alert: warning — "3 staff members have no BGV. Required by POCSO Act."
   Action: [Review BGV List]
   Placement: Page-level banner, below header

→ Toast: success — "Attendance saved for 124 students"
→ Toast: error — "Failed to save. Check your connection." [Retry]

→ Empty state: No students match filter
   Heading: "No students found"
   Message: "No Class 12 students match 'Fee Defaulter' status."
   CTA: [Clear Filters]
```
