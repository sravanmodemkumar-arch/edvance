# EduForge — Shared UI Component Library

> These components are REUSABLE across all 10 groups and all portals.
> Every page spec references these files. Never re-document a component — just link it.
> Update these files when the component design evolves.

---

## Component Files Index

| File | Component | Used In |
|---|---|---|
| [01-table-pagination.md](01-table-pagination.md) | Data Table, Pagination, Column config | All group admin pages |
| [02-modal-drawer.md](02-modal-drawer.md) | Modal Dialog, Side Drawer, Bottom Sheet | All groups — detail views, forms |
| [03-alerts-toasts.md](03-alerts-toasts.md) | Alert Banner, Toast, Confirm Dialog, Empty State | All groups |
| [04-filters-search.md](04-filters-search.md) | Search Bar, Filter Bar, Advanced Filter Panel | All listing pages |
| [05-forms-inputs.md](05-forms-inputs.md) | Text, Select, Date, File, OTP, Toggle inputs | All forms |
| [06-navigation.md](06-navigation.md) | Sidebar, Top Nav, Tabs, Breadcrumb, Step Progress | All portals |
| [07-data-display.md](07-data-display.md) | Stat Card, Badge, Avatar, Tag, Progress Bar, Chart | All dashboards |
| [08-design-tokens.md](08-design-tokens.md) | Colors, Typography, Spacing, Shadows, Breakpoints | All pages |
| [09-charts-graphs.md](09-charts-graphs.md) | Chart variants, axes config, empty states | Dashboard panels |
| [10-stat-cards.md](10-stat-cards.md) | KPI cards — Standard, Hero, Status, Sparkline, Mini | All dashboards |
| [11-timeline.md](11-timeline.md) | Activity feed, incident timeline, grouped timeline | Activity panels |
| [12-command-palette.md](12-command-palette.md) | ⌘K palette — role-filtered, keyboard nav | All portals |


## How to Reference Components in Page Specs

Instead of re-documenting, use this pattern in any group page spec:

```
### Student List Table
→ See [Table Component](../../components/01-table-pagination.md)
  Columns: Name, Class, Roll No, Attendance %, Last Login, Actions
  Default sort: Attendance % ascending
  Row action: [View Profile] [Edit] [Suspend]
```

---

## Update Policy

- When a component behavior changes — update the component file directly
- All page specs that reference it automatically inherit the update
- Add a `> ⚠️ Updated: [date] — [what changed]` note at top of changed component file
- Never have two different descriptions of the same component across files
