# Page 19 — Design System

**URL:** `/portal/product/design-system/`
**Permission:** `product.view_design_system`
**Priority:** P2
**Roles:** UI/UX Designer, PM Platform, QA Engineer

---

## Purpose

Living documentation and governance hub for the SRAV platform design system. Centralises all visual design decisions, component specifications, interaction patterns, and accessibility standards used across the institution portal, student portal, mobile app, and admin portal. Serves as the single source of truth for both designers and frontend engineers.

Core responsibilities:
- Document all UI components with specifications, states, and usage guidelines
- Manage the design token library (colours, typography, spacing, shadows)
- Enforce consistency across portal pages and mobile app
- Track which pages are compliant with the current design system version
- Flag component usage in production that deviates from the specification
- Manage component deprecation and migration paths

**Scale:**
- 60+ UI components in the system
- 4 surfaces: institution portal · student portal · mobile app (Flutter) · admin portal
- 1,950+ institution portals all themed from the same base component library
- Component updates need to be backward-compatible

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Design System"    v2.4.1      [New Component]  [Export Tokens]│
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 4 cards                                            │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  Foundations · Components · Patterns · Compliance              │
│  Mobile (Flutter) · Changelog · Tokens Export                  │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 4 Cards

| # | Label | Value | Click Action |
|---|---|---|---|
| 1 | Design System Version | Current version (e.g. v2.4.1) | Opens Changelog |
| 2 | Components | Total components in system | Opens Components tab |
| 3 | Compliant Pages | Count / Total portal pages that pass compliance check | Opens Compliance tab |
| 4 | Deprecated Components | Components deprecated but still in use somewhere | Opens Compliance tab filtered |

---

## Tab 1 — Foundations

Core design decisions that underpin all components.

### Section 1.1 — Colour Tokens

**Colour Token Table:**

Each token documented with:
- Token name (CSS variable format: `--color-primary-500`)
- Hex value
- Preview swatch
- Semantic meaning
- Usage guidance
- Surfaces it applies to

#### Brand Colours

| Token | Hex | Preview | Usage |
|---|---|---|---|
| --color-primary-400 | #818CF8 | ▓ | Primary interactive elements (light theme hover) |
| --color-primary-500 | #6366F1 | ▓ | Primary buttons, active states, links |
| --color-primary-600 | #5558E8 | ▓ | Primary button hover, pressed states |
| --color-primary-700 | #4338CA | ▓ | Primary button active/pressed |
| --color-success-400 | #34D399 | ▓ | Success hover |
| --color-success-500 | #10B981 | ▓ | Success badges, positive deltas, completed states |
| --color-success-600 | #059669 | ▓ | Success hover |
| --color-warning-400 | #FBBF24 | ▓ | Warning hover |
| --color-warning-500 | #F59E0B | ▓ | Warning badges, caution states |
| --color-danger-400 | #F87171 | ▓ | Danger hover |
| --color-danger-500 | #EF4444 | ▓ | Error states, destructive actions, negative deltas |
| --color-info-500 | #3B82F6 | ▓ | Informational badges, help text |

#### Dark Theme Surface Stack

| Token | Hex | Preview | Usage |
|---|---|---|---|
| --color-bg-base | #070C18 | ▓ | Page background |
| --color-bg-surface-1 | #0D1526 | ▓ | Cards, panels, modals |
| --color-bg-surface-2 | #131F38 | ▓ | Table rows, input fields, secondary cards |
| --color-bg-surface-3 | #1E2D4A | ▓ | Borders, dividers, hover states |
| --color-bg-surface-4 | #243358 | ▓ | Active row highlight, selected state |
| --color-text-primary | #F1F5F9 | ▓ | Headings, primary text |
| --color-text-secondary | #94A3B8 | ▓ | Labels, meta text, placeholder |
| --color-text-disabled | #475569 | ▓ | Disabled field text |
| --color-border-default | #1E2D4A | ▓ | Default border colour |
| --color-border-focus | #6366F1 | ▓ | Focus ring on interactive elements |

#### Light Theme Surface Stack

| Token | Hex | Preview | Usage |
|---|---|---|---|
| --color-bg-base | #F8FAFC | ▓ | Page background |
| --color-bg-surface-1 | #FFFFFF | ▓ | Cards, panels, modals |
| --color-bg-surface-2 | #F1F5F9 | ▓ | Table rows, input fields |
| --color-bg-surface-3 | #E2E8F0 | ▓ | Borders, dividers, hover states |
| --color-text-primary | #0F172A | ▓ | Headings |
| --color-text-secondary | #475569 | ▓ | Labels, meta |
| --color-text-disabled | #94A3B8 | ▓ | Disabled text |
| --color-border-default | #E2E8F0 | ▓ | Default border |
| --color-border-focus | #6366F1 | ▓ | Focus ring |

#### Chart Palette (8 categorical colours)

| Token | Hex | Usage |
|---|---|---|
| --color-chart-1 | #6366F1 | First dataset (SSC, primary series) |
| --color-chart-2 | #10B981 | Second dataset |
| --color-chart-3 | #F59E0B | Third dataset |
| --color-chart-4 | #EF4444 | Fourth dataset |
| --color-chart-5 | #3B82F6 | Fifth dataset |
| --color-chart-6 | #8B5CF6 | Sixth dataset |
| --color-chart-7 | #14B8A6 | Seventh dataset |
| --color-chart-8 | #F97316 | Eighth dataset |

Chart grid colour: dark theme `#1E2D4A` · light theme `#E2E8F0`

---

### Section 1.2 — Typography

| Token | Font | Weight | Size | Line Height | Usage |
|---|---|---|---|---|---|
| --text-display | Inter | 800 | 36px | 1.2 | Page titles (rare) |
| --text-heading-1 | Inter | 700 | 24px | 1.3 | Section headings |
| --text-heading-2 | Inter | 600 | 20px | 1.4 | Card headings |
| --text-heading-3 | Inter | 600 | 16px | 1.5 | Subsection headings |
| --text-body | Inter | 400 | 14px | 1.6 | Body text, table cells |
| --text-body-sm | Inter | 400 | 13px | 1.6 | Secondary content |
| --text-caption | Inter | 400 | 12px | 1.5 | Labels, meta, captions |
| --text-mono | JetBrains Mono | 400 | 13px | 1.5 | Code, transaction IDs, OTP |
| --text-label | Inter | 500 | 12px | 1.4 | Form labels, table headers |
| --text-badge | Inter | 600 | 11px | 1 | Badge text |

**Font loading:** Inter loaded from Google Fonts with `display=swap`. JetBrains Mono loaded for monospace contexts only.

---

### Section 1.3 — Spacing Scale

Token format: `--space-{n}` where n is 1–16 (1 = 4px).

| Token | Value | Usage |
|---|---|---|
| --space-1 | 4px | Micro gap (icon + label) |
| --space-2 | 8px | Compact padding |
| --space-3 | 12px | Input padding |
| --space-4 | 16px | Card padding (default) |
| --space-5 | 20px | Section padding |
| --space-6 | 24px | Page section gap |
| --space-8 | 32px | Large section gap |
| --space-10 | 40px | Page-level padding |
| --space-12 | 48px | Hero padding |
| --space-16 | 64px | Extra large (drawer headers) |

**Grid:** 12-column grid. Gutter: 16px (mobile) / 24px (desktop). Container max-width: 1440px.

---

### Section 1.4 — Shadow Scale

| Token | Value | Usage |
|---|---|---|
| --shadow-xs | 0 1px 2px rgba(0,0,0,0.05) | Subtle lift (badge, chip) |
| --shadow-sm | 0 2px 4px rgba(0,0,0,0.1) | Card default |
| --shadow-md | 0 4px 12px rgba(0,0,0,0.15) | Dropdown, popover |
| --shadow-lg | 0 8px 24px rgba(0,0,0,0.2) | Modal, drawer |
| --shadow-xl | 0 16px 48px rgba(0,0,0,0.25) | Fullscreen overlay |
| --shadow-primary | 0 4px 12px rgba(99,102,241,0.3) | Primary button glow |

---

### Section 1.5 — Border Radius Scale

| Token | Value | Usage |
|---|---|---|
| --radius-sm | 4px | Input fields, table cells |
| --radius-md | 8px | Buttons, small cards |
| --radius-lg | 12px | Cards, panels |
| --radius-xl | 16px | Large cards, modals |
| --radius-2xl | 20px | Drawers |
| --radius-full | 9999px | Badges, pills, avatars |

---

## Tab 2 — Components

Complete library of all UI components. Each component has its own documentation card.

### Component Categories:

- **Data Input:** Button · Input · Select · Textarea · Checkbox · Radio · Toggle · Slider · Date Picker · File Upload · Search Input · OTP Input
- **Data Display:** Table · Badge · Tag · Avatar · Progress Bar · Gauge (semicircle) · Stat Card · Chart wrapper · Tooltip · Empty State · Skeleton Loader
- **Navigation:** Tab Bar · Sidebar Nav · Breadcrumb · Pagination · Step Indicator
- **Feedback:** Alert · Toast · Modal · Drawer · Confirmation Dialog · Loading Spinner · Progress Overlay
- **Layout:** Card · Divider · Grid · Section Header · Page Header · Sticky Header
- **Special:** Code Block · Diff Viewer · Drag-and-drop List · Kanban Board · Gantt Bar · Coverage Heatmap cell

### Component Documentation Card (for each component)

Each component is documented with:

**Overview section:**
- Component name and version
- One-line description
- When to use / when not to use
- Surfaces where used (admin portal / institution portal / student portal / mobile)

**Anatomy diagram:**
- Labelled wireframe showing all parts (e.g. Button: container · icon · label · loading spinner)

**States:**
- Default
- Hover
- Focus (focus ring specification)
- Active / Pressed
- Disabled
- Loading (if applicable)
- Error (if applicable)
- Success (if applicable)
- Empty (if applicable)

**Variants:**
Documented as a table. Example for Button:

| Variant | Use Case | Notes |
|---|---|---|
| Primary | Main CTA (one per section) | Indigo background |
| Secondary | Alternative action | Outlined, no fill |
| Ghost | Tertiary action | No border, text colour only |
| Destructive | Delete/remove actions | Red background |
| Icon-only | Compact toolbars | Tooltip required |
| Loading | Async action in progress | Spinner replaces icon/text |

**Size variants:**
- xs / sm / md (default) / lg for most components

**Spacing specifications:**
- Padding (horizontal + vertical per size)
- Gap between icon and label
- Minimum touch target (44px × 44px — mobile accessibility requirement)

**Colour tokens used:**
- Which tokens map to which visual element

**Accessibility requirements:**
- ARIA role
- Keyboard navigation
- Screen reader announcement
- Focus order
- Contrast ratio: must meet WCAG 2.1 AA (4.5:1 for text, 3:1 for non-text)

**Usage examples:**
- Do / Don't illustrations (static descriptions)

---

### Key Component Specifications

#### Table Component
- Header: sticky when table > 400px tall
- Row hover: `--color-bg-surface-2`
- Row selected: `--color-bg-surface-4` + left border in primary colour (3px)
- Column sorting: up/down chevron in header, active column shows primary colour chevron
- Column resize: drag handle on right edge of header cell
- Pagination: always visible below table (even if 1 page)
- Empty state: centred message + illustration + CTA
- Loading state: skeleton rows (3 rows of varying width skeletons)
- Cell types: Text · Badge · Progress bar · Avatar · Date · Number (right-aligned) · Actions column (right-aligned)

#### Modal Component
- Width: sm=400px · md=560px · lg=640px · xl=720px · full=90vw max 900px
- Backdrop: rgba(0,0,0,0.5) + blur(4px)
- Animation: fade + scale-up (150ms ease-out)
- Close: × button top-right + backdrop click + Escape key
- Footer buttons: right-aligned, destructive action on left when present
- Scroll: modal body scrolls, header and footer stay fixed

#### Drawer Component
- Width: sm=400px · md=480px · lg=560px · xl=640px · xxl=720px · full=800px
- Position: right side (default) or left side
- Animation: slide in from right (200ms ease-out)
- Backdrop: rgba(0,0,0,0.5)
- Body class added: `drawer-open` (used by HTMX poll guards)
- Close: × button in drawer header + backdrop click + Escape key
- Nested drawers: second drawer stacks at right offset (transforms body class to `drawer-open-2`)

#### Badge Component
- Shape: pill (radius-full)
- Sizes: sm (10px text) / md (12px text, default) / lg (13px text)
- Colour variants: success / warning / danger / info / primary / neutral / muted
- With dot: 6px coloured dot + label (for status badges)
- Count badge: circular, positioned top-right of parent (for notification bell counts)

#### KPI Stat Card Component
- Structure: icon (top-right) · label (small, secondary colour) · value (large, bold) · delta (small, colour-coded) · optional mini sparkline or bar
- Hover: subtle ring border in primary colour (2px, 50% opacity)
- Click: ripple effect + navigation action
- Count-up animation: value animates 0 → final over 600ms using requestAnimationFrame. Guard: `data-animated="true"` prevents re-animation on partial page swaps.

#### Progress Bar Component
- Variants: linear (full width) · compact (fixed width, e.g. in tables) · mini (1px, used in domain grid cards)
- Colour: green ≥70% · amber 40–69% · red <40% (configurable thresholds per use case)
- Animated: smooth width transition 400ms ease-out on value change
- Label options: percentage inside bar · percentage outside (right) · hidden

#### Skeleton Loader
- Used for: cards, tables, charts during HTMX partial load
- Style: `animate-pulse` with `--color-bg-surface-3` fill
- Shape mimics actual component (narrow rect for labels, wide rect for titles, full-height for chart areas)
- Auto-replaced by real content on HTMX swap

---

## Tab 3 — Patterns

Documents recurring interaction patterns used across multiple pages.

### Pattern List

| Pattern | Description | Pages Using |
|---|---|---|
| HTMX Partial Refresh | All page sections load via `?part=` URL and swap target divs | All pages |
| Poll Auto-pause Guard | `every Xs[!document.querySelector('.drawer-open,.modal-open')]` | All pages with polling |
| Count-up Animation | KPI values animate from 0 on load | All pages with KPI strips |
| Staged Changes Workflow | Edit → Stage → Review → 2FA Publish | Feature Config, Plan Config, Exam Domain Config |
| Drawer Stack | Primary drawer (640px) → secondary nested drawer (480px) | Release Manager, Feature Flags |
| Search + Filter + Sort | Toolbar pattern: search (300ms debounce) + multiple filters + sort indicator | All table pages |
| Pagination | Showing X–Y of Z + page pills + per-page selector | All table pages |
| Kanban Board | Drag-and-drop column board with WIP limits | Roadmap, Release Manager, Onboarding Dashboard |
| Chart Destroy-Recreate | `if window._charts[id] exists: destroy; new Chart(...)` | All Chart.js pages |
| 2FA Gate | Server-side `session.get("2fa_verified")` check before destructive actions | Feature flags kill-switch, deploy, rollback, publish |
| Empty State | Centred illustration + message + CTA button | All table and list views |
| Confirmation Dialog | "Are you sure?" with typed confirmation for high-risk actions | Delete, rollback, bulk operations |
| Optimistic UI | Show change immediately, revert on server error | Toggle switches (feature flags, status badges) |

### Pattern Documentation (per pattern)

Each pattern documented with:
- Problem it solves
- When to use
- When not to use
- Implementation reference (links to existing page that implements it)
- Keyboard accessibility consideration
- Animation/transition specification
- Error handling

---

## Tab 4 — Compliance

Tracks which portal pages are compliant with the current design system version.

### Compliance Summary Cards

| Card | Value |
|---|---|
| Fully Compliant Pages | Count |
| Partially Compliant | Count (minor deviations) |
| Non-Compliant | Count (significant deviations) |
| Last Audit | Date |

### Compliance Table

| Page | Path | Design System Version | Status | Issues | Last Audited | Actions |
|---|---|---|---|---|---|---|
| Product Dashboard | /portal/product/ | v2.4.1 | ✓ Compliant | 0 | 3 days ago | View |
| Feature Flags | /portal/product/feature-flags/ | v2.4.0 | ⚠ Partial | 2 minor | 5 days ago | View Issues |
| Domain Analytics | /portal/product/domain-analytics/ | v2.4.1 | ✓ Compliant | 0 | 1 day ago | View |

**Compliance issues logged per page:**
- Severity: Minor (style deviation) / Moderate (pattern violation) / Critical (accessibility failure)
- Description
- Component affected
- Recommended fix
- Assigned to (engineer)
- Status: Open / In Progress / Fixed

---

## Tab 5 — Mobile (Flutter)

Design system documentation specific to the Flutter mobile app.

### Flutter Component Map

Maps web design tokens to Flutter equivalents:

| Web Token | Flutter Property | Value |
|---|---|---|
| --color-primary-500 | `Color(0xFF6366F1)` | Indigo |
| --color-bg-base (dark) | `Color(0xFF070C18)` | Page scaffold background |
| --text-body | `TextStyle(fontSize: 14, fontFamily: 'Inter')` | — |
| --radius-lg | `BorderRadius.circular(12)` | Card corners |
| --space-4 | `EdgeInsets.all(16)` | Default card padding |

### Flutter Widget Library

Documents which Flutter widgets correspond to web components:
- Web Table → Flutter `DataTable` / Custom `ListView.builder`
- Web Modal → Flutter `showModalBottomSheet` / `showDialog`
- Web Drawer → Flutter `Drawer` + `Scaffold.endDrawer`
- Web Badge → Custom `Container` + `ClipRRect` + `Text`
- Web KPI Card → Custom `Card` widget
- Web Progress Bar → `LinearProgressIndicator` with custom colour

### Flutter Navigation Patterns
- Bottom tab bar: 5 tabs (Home / Exams / Results / Leaderboard / Profile)
- Push navigation for exam flow (timed screens)
- Modal bottom sheet for quick actions
- Hero animation for exam card → full exam view

---

## Tab 6 — Changelog

Version history of design system changes.

### Changelog Table

| Version | Date | Summary | Breaking Changes | Pages Affected |
|---|---|---|---|---|
| v2.4.1 | 15 Mar 2026 | Added Coverage Heatmap cell component | None | Syllabus Builder, Domain Analytics |
| v2.4.0 | 28 Feb 2026 | Redesigned KPI Stat Card with mini sparkline support | None | All pages with KPI strips |
| v2.3.2 | 12 Feb 2026 | Updated Drawer animation to 200ms | None | All pages with drawers |
| v2.3.1 | 3 Feb 2026 | Deprecated old Tab Bar component — replaced with new | Tab Bar API changed | All tab pages |
| v2.3.0 | 20 Jan 2026 | Added dark/light theme token system | — | All pages |

Each row expandable to show full change notes, migration guide, and affected components.

---

## Tab 7 — Tokens Export

Allows exporting design tokens in various formats for use in code.

### Export Formats Available

| Format | Use Case |
|---|---|
| CSS custom properties (:root variables) | Web portal (Tailwind integration) |
| Tailwind config (tailwind.config.js) | Direct Tailwind usage |
| JSON (Style Dictionary format) | Cross-platform token management |
| Dart constants | Flutter mobile app |
| Figma Tokens plugin format | Design handoff |

**Export button:** Triggers download of selected format. Includes version number in filename (e.g. `srav-tokens-v2.4.1.css`).

---

## Component Deprecation Policy

When a component is deprecated in favour of a replacement:

1. PM or UI/UX Designer marks component as "Deprecated" in the component library
2. Deprecated badge shown on component card
3. Migration guide added: "Replace X with Y. Key differences: …"
4. Warning shown in Compliance tab for any page still using deprecated component
5. Grace period: 30 days to migrate all usages before component is archived
6. After archiving: component removed from design system but documented in Changelog

No component is silently removed. All removals have a migration path.

---

## Accessibility Standards

The design system enforces WCAG 2.1 Level AA accessibility across all components.

### Colour Contrast Requirements

| Use Case | Minimum Ratio | Check Method |
|---|---|---|
| Normal text (< 18pt) | 4.5:1 | Automated in compliance scan |
| Large text (≥ 18pt) | 3:1 | Automated |
| Non-text (icons, borders, input outlines) | 3:1 | Manual review |
| Focus indicators | 3:1 | Automated |
| Disabled text | No requirement (exempt) | N/A |

Dark theme primary text (`--color-text-primary #F1F5F9`) on base background (`--color-bg-base #070C18`): contrast ratio 18.5:1 (exceeds AA requirement).

### Keyboard Navigation Standards

All interactive components must support:
- Tab: move focus to next interactive element
- Shift+Tab: move focus to previous
- Enter / Space: activate button, toggle checkbox, open dropdown
- Escape: close modal, drawer, dropdown
- Arrow keys: navigate within dropdown, radio group, tab bar
- Home/End: jump to first/last item in list

### Focus Ring Specification

- Colour: `--color-border-focus #6366F1`
- Width: 2px solid
- Offset: 2px (outside element border)
- Border radius: matches element border radius + 2px
- Must not be hidden with `outline: none` — only replaced with an equivalent custom focus ring

### Screen Reader Announcements

| Component | ARIA Role | Announcement on Focus |
|---|---|---|
| Button | button | "[Label] button" |
| Modal | dialog | "[Title] dialog, [description]" |
| Drawer | complementary | "[Title] panel" |
| Badge | status | "[colour] [text] status" |
| KPI Card | region | "[label]: [value], [delta]" |
| Progress bar | progressbar | "[label]: [value]%" |
| Table | grid | "[column header]" on each cell |
| Tab bar | tablist / tab | "[tab name] tab, [N] of [M], selected/unselected" |

---

## Component Usage Guidelines

### When to Use Each Button Variant

| Variant | Use | Restriction |
|---|---|---|
| Primary | Main call to action | Maximum 1 per section; never more than 1 Primary button in the same visual area |
| Secondary | Alternative action equal to Primary | Use when user has a real choice between two paths |
| Ghost | Tertiary action less important than above | Table row actions, inline subtle CTAs |
| Destructive | Delete, remove, irreversible actions | Always show confirmation dialog; never label as "Delete" without context (e.g. "Delete Exam, not just Delete") |
| Icon-only | Toolbars with space constraints | Must have tooltip (aria-label) — never used without accessible label |

### When NOT to Use Modals

Modals should not be used:
- To show success messages (use Toast instead)
- For long multi-step forms > 4 steps (use a full page or multi-step form)
- When the user is mid-task and would lose context by opening a modal
- For non-critical information that doesn't require immediate attention (use inline messaging)

### Drawer vs Modal Decision

| Use Drawer When | Use Modal When |
|---|---|
| Viewing/editing a record while keeping list visible | Confirming a destructive action |
| Multi-tab detail view requiring screen space | Collecting 3–5 fields for a quick creation |
| Design review, test case details, defect details | 2FA verification |
| Any content > 3 form fields | Simple confirmation (are you sure?) |

---

## Design Review Integration

The Design System page integrates with the UI Review Board (page 20):

- **"Check Compliance" button** on any review in UI Review Board opens this design system and shows the token checklist for that review
- **Deprecated component warnings** shown on review cards in UI Review Board when the submitted design uses a deprecated component
- **Version tag** on each review shows which design system version the design was created against
- **Component change notifications:** when a component is updated in a minor or major way, all open UI reviews that use that component receive an in-app notification: "Component X was updated in v2.5.0. Please verify your review design is compatible."

---

## Design System Governance

### Versioning Scheme

- **Major version (X.0.0):** Breaking changes — component API changed, token renamed, component removed. Requires migration guide.
- **Minor version (M.X.0):** New components or tokens added, non-breaking. No migration required.
- **Patch version (M.M.X):** Bug fixes, documentation corrections, minor visual tweaks. No migration required.

### Contribution Process

Team members can propose changes to the design system:
1. Open a "Design System Proposal" in the UI Review Board (category: Design Tokens)
2. UI/UX Designer and PM Platform review the proposal
3. If approved: PM increments the appropriate version number
4. Component added/updated in the system and documented
5. Affected pages flagged for compliance review

No change is made to the design system without a proposal and approval. This prevents fragmentation.

### Who Can Approve Design System Changes

| Change Type | Approver Required |
|---|---|
| Colour token addition | UI/UX Designer |
| Colour token change | UI/UX Designer + PM Platform |
| New component | UI/UX Designer + QA sign-off |
| Component deprecation | PM Platform |
| Major breaking change | PM Platform + Engineering Lead |

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| Token naming | Semantic names (--color-bg-surface-1) not descriptive (--color-dark-blue) | Semantic names work across themes; descriptive names break in light theme |
| Surface stack depth | 4 surface levels in dark theme | 4 levels enough for card-inside-drawer-inside-modal nesting without inventing more levels |
| Chart grid colour | Separate token from border colour | Chart grids should be subtler than UI borders; using same colour makes charts look heavy |
| Skeleton loaders | Always present in HTMX partials | Prevents layout shift during async loads; user sees structure before data |
| Compliance audit | Automated check + manual review | Automated catches colour/spacing violations; manual catches semantic/pattern violations |
| Flutter token map | Documented in design system | Ensures mobile app stays visually consistent with web without manual pixel-checking |
| Count-up animation guard | `data-animated="true"` | HTMX partial swaps can trigger re-animation; guard prevents jarring repeated animations |
| 44px minimum touch target | Mobile accessibility requirement | Apple HIG and Material Design both specify 44×44px minimum; needed for all mobile users |
| Modal vs Drawer decision | Documented use criteria | Without guidance, developers use modals for everything; drawer decision table prevents this |
| Component deprecation policy | 30-day grace period | Components cannot be removed without migration path; prevents surprise breakage |
| Design system versioning | Semver (major.minor.patch) | Standard versioning enables consuming code to pin to a compatible version |
| Contribution process | Proposal → Review → Approval | Prevents fragmentation; every design system change is deliberate and reviewed |

