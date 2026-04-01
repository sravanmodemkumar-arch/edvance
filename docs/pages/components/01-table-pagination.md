# Component: Data Table + Pagination

> Used on every listing page across all groups.
> Reference this file in any page spec — do not re-document.

---

## Data Table

### Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  TABLE HEADER ROW                                                   │
│  ┌──────┬─────────────────┬───────────┬────────────┬────────────┐  │
│  │ [☐]  │ Column A ↕      │ Column B  │ Column C ↕ │ Actions    │  │
│  └──────┴─────────────────┴───────────┴────────────┴────────────┘  │
│                                                                     │
│  DATA ROWS                                                          │
│  ┌──────┬─────────────────┬───────────┬────────────┬────────────┐  │
│  │ [☐]  │ Row 1 Value     │ Value     │ Value      │ [⋯ Actions]│  │
│  ├──────┼─────────────────┼───────────┼────────────┼────────────┤  │
│  │ [☐]  │ Row 2 Value     │ Value     │ Value      │ [⋯ Actions]│  │
│  ├──────┼─────────────────┼───────────┼────────────┼────────────┤  │
│  │ [☐]  │ Row 3 Value     │ Value     │ Value      │ [⋯ Actions]│  │
│  └──────┴─────────────────┴───────────┴────────────┴────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Column Header

| Feature | Spec |
|---|---|
| Sort indicator | ↕ = unsorted, ↑ = asc, ↓ = desc. Click cycles: asc → desc → none |
| Multi-sort | Shift+click adds secondary sort. Max 2 sort columns |
| Resize | Drag column edge to resize. Min width 80px |
| Reorder | Drag column header to reorder. Persisted per user per page |
| Hide/show | Right-click header → "Hide column". Gear icon → column chooser |
| Sticky | First column (checkbox + ID/name) always sticky-left on scroll |
| Actions column | Always sticky-right, min 80px, not sortable, not hideable |
| Tooltip | Long text truncated with ellipsis + hover tooltip with full text |

### Row Behavior

| Feature | Spec |
|---|---|
| Hover | Background: `--surface-variant` (subtle highlight) |
| Selected | Background: `--primary-container` (tinted) |
| Checkbox | Select row. Header checkbox = select all visible rows |
| Click row | Opens detail view — either in drawer (default) or new page |
| Right-click | Context menu: View, Edit, Duplicate, Export row, Suspend |
| Striped | Alternate rows: even rows get `--surface-variant` at 50% opacity |
| Density | Default: 56px row height. Compact: 40px. Comfortable: 72px. User toggle |
| Inline edit | Double-click on editable cell → inline edit mode (not all columns) |
| Status badge | Status columns use color badges (see [07-data-display.md](07-data-display.md)) |
| Avatar | Name columns with photo: 32px circular avatar + name side by side |

### Bulk Actions Bar

> Appears ONLY when 1+ rows selected. Floats above table.

```
┌───────────────────────────────────────────────────────────┐
│  ✅ 14 rows selected        [Export CSV] [Suspend] [Delete]│
│  [Deselect all]                              [More ▼]     │
└───────────────────────────────────────────────────────────┘
```

| Action | Icon | Behavior |
|---|---|---|
| Export CSV | Download icon | Exports only selected rows |
| Suspend | Lock icon | Opens confirm modal before action |
| Delete | Trash icon | Opens confirm modal. Red destructive button |
| More | Ellipsis | Dropdown: Change role, Send notification, Assign to batch, etc. |

### Empty State (No Data)

```
┌───────────────────────────────────────────────────────────┐
│                                                           │
│              [Illustration: empty box / person]           │
│                                                           │
│           No [items] found                                │
│                                                           │
│   [context-aware message based on current filters]        │
│   E.g.: "No students match 'Class 12 + Fee Defaulter'"    │
│                                                           │
│        [Clear filters]   [Add new student]                │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Loading State

- Skeleton rows: 10 gray shimmer rows replace real rows
- Skeleton columns match current column widths
- Spinner in top-right of table (not blocking full page)

### Error State

```
⚠️  Failed to load data. [Retry]   (inline, not full page)
```

---

## Pagination

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Rows per page: [25 ▼]          1–25 of 1,247   [< 1 2 3…>]│
└─────────────────────────────────────────────────────────────┘
```

### Component Spec

| Feature | Spec |
|---|---|
| Rows per page | Options: 10, 25, 50, 100. Default: 25. Persisted per user |
| Total count | Shows "X–Y of Z total" — Z updates after filters applied |
| Page buttons | Show: first 3 pages, current±1, last 3 pages. Ellipsis between gaps |
| First / Last | Keyboard: Home key = page 1. End key = last page |
| Prev / Next | `[<]` `[>]` buttons. Disabled when at boundary |
| Jump to page | Click current page number → editable input → Enter to jump |
| URL sync | Current page reflected in URL: `?page=3&per_page=25` |
| Scroll | On page change: scroll table back to top |

### Page Button States

| State | Visual |
|---|---|
| Default | Gray bordered square button |
| Current page | Primary color fill, white text, no hover effect |
| Hover | Light primary tint background |
| Disabled (at boundary) | 40% opacity, no cursor |
| Ellipsis | `…` — not clickable |

---

## Column Chooser (Gear Panel)

> Opens from gear icon (⚙) in top-right of table.

```
┌───────────────────────────────────┐
│  Show/Hide Columns                │
│  ──────────────────────────────── │
│  [✅] Name          (required)    │
│  [✅] Roll Number                 │
│  [✅] Class                       │
│  [  ] Date of Birth               │
│  [✅] Attendance %                │
│  [  ] Fee Status                  │
│  [✅] Last Login                  │
│  ──────────────────────────────── │
│  [Reset to default]   [Apply]     │
└───────────────────────────────────┘
```

- Required columns: cannot be hidden (shown but checkbox disabled)
- Settings persisted in user preferences (localStorage + server sync)
- "Reset to default" restores factory column config for that page

---

## Export

> Available on all tables via toolbar button.

| Format | Columns | Rows |
|---|---|---|
| CSV | Currently visible columns only | All rows (ignoring pagination), filtered |
| Excel (.xlsx) | All columns (including hidden) | All rows, filtered |
| PDF | Currently visible columns | Current page only (for large datasets) |

- Export respects active filters — only exports filtered dataset
- Filename: `[institution]_[entity]_[YYYY-MM-DD].csv`
- For > 10,000 rows: export is async — user gets WhatsApp/email when ready
- Row limit per export: 50,000. Above that → split into multiple files

---

## Theme Support (Dark + Light)

> All table and pagination elements use CSS custom property tokens from `00-global-layout.md`. The table automatically adapts to dark and light themes — no logic changes required.

### Dark Theme (Default)

```css
/* ── Table container ── */
.data-table-wrap {
  background: var(--bg-surface-1);          /* #0D1526 */
  border: 1px solid var(--border-subtle);   /* #1E293B */
  border-radius: var(--radius-lg);
}

/* ── Header row ── */
.data-table thead th {
  background: var(--bg-surface-2);          /* #131F38 */
  color: var(--text-muted);                 /* #64748B */
  border-bottom: 1px solid var(--border-subtle);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

/* ── Body rows ── */
.data-table tbody tr {
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-primary);               /* #F1F5F9 */
}

.data-table tbody tr:hover {
  background: var(--bg-surface-2);          /* #131F38 */
}

.data-table tbody tr.selected {
  background: color-mix(in srgb, var(--primary) 10%, var(--bg-surface-1));
  border-color: color-mix(in srgb, var(--primary) 20%, transparent);
}

/* Striped rows */
.data-table--striped tbody tr:nth-child(even) {
  background: color-mix(in srgb, var(--bg-surface-2) 50%, transparent);
}

/* ── Bulk actions bar ── */
.bulk-actions-bar {
  background: var(--primary);
  color: white;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
}

/* ── Pagination ── */
.pagination__btn {
  background: transparent;
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
}

.pagination__btn--active {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.pagination__btn:hover:not(.pagination__btn--active):not(:disabled) {
  border-color: var(--primary);
  color: var(--primary);
}

.pagination__btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* ── Loading skeleton ── */
.data-table--loading tbody tr td {
  background: linear-gradient(
    90deg,
    var(--bg-surface-2) 25%,
    color-mix(in srgb, var(--text-muted) 15%, var(--bg-surface-2)) 50%,
    var(--bg-surface-2) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
  color: transparent;
  border-radius: var(--radius-sm);
}

@keyframes skeleton-shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}
```

### Light Theme Overrides

```css
[data-theme="light"] .data-table-wrap {
  background: var(--bg-surface-1);          /* #FFFFFF */
  border-color: var(--border-subtle);       /* #E2E8F0 */
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

[data-theme="light"] .data-table thead th {
  background: var(--bg-surface-2);          /* #F1F5F9 */
  color: var(--text-muted);                 /* #64748B */
  border-bottom-color: var(--border-subtle);
}

[data-theme="light"] .data-table tbody tr {
  color: var(--text-primary);               /* #0F172A */
  border-bottom-color: var(--border-subtle);
}

[data-theme="light"] .data-table tbody tr:hover {
  background: var(--bg-surface-2);          /* #F1F5F9 */
}

[data-theme="light"] .data-table tbody tr.selected {
  background: color-mix(in srgb, var(--primary) 8%, var(--bg-surface-1));
}

[data-theme="light"] .data-table--loading tbody tr td {
  background: linear-gradient(90deg, #E2E8F0 25%, #F1F5F9 50%, #E2E8F0 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
}
```

### Token Quick Reference

| Property | Dark | Light |
|---|---|---|
| Table bg | `--bg-surface-1` → `#0D1526` | `--bg-surface-1` → `#FFFFFF` |
| Header bg | `--bg-surface-2` → `#131F38` | `--bg-surface-2` → `#F1F5F9` |
| Row hover | `--bg-surface-2` | `--bg-surface-2` |
| Row selected | primary 10% tint | primary 8% tint |
| Cell text | `--text-primary` → `#F1F5F9` | `--text-primary` → `#0F172A` |
| Header text | `--text-muted` → `#64748B` | `--text-muted` → `#64748B` |
| Row divider | `--border-subtle` → `#1E293B` | `--border-subtle` → `#E2E8F0` |
| Active page btn | `--primary` → `#6366F1` | `--primary` → `#4F46E5` |

---

## Usage in Page Specs

```markdown
### Staff List
→ Component: [Data Table](../../components/01-table-pagination.md)
  Columns:
  | Column | Width | Sortable | Description |
  |---|---|---|---|
  | Name + Avatar | 220px | Yes | Staff full name, 32px photo |
  | Role | 160px | Yes | Role badge (color-coded by division) |
  | Division | 140px | Yes | A–O division label |
  | Access Level | 100px | Yes | Level 0–5 badge |
  | Status | 100px | No | Active / Suspended / Pending |
  | Last Login | 140px | Yes | Relative time + abs on hover |
  | Actions | 80px | No | [⋯] context menu |

  Default sort: Last Login DESC
  Row click: Opens Staff Detail Drawer (see Division A page)
  Bulk actions: Export, Suspend, Change Role
```
