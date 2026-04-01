# Page 20 — UI Review Board

**URL:** `/portal/product/ui-review/`
**Permission:** `product.manage_ui_reviews`
**Priority:** P2
**Roles:** UI/UX Designer, PM Institution Portal, PM Platform, QA Engineer

---

## Purpose

Structured workflow for reviewing, annotating, approving, and tracking all UI design changes before they reach production. Every screen design, component change, and interaction update passes through this board. Replaces ad-hoc Figma comment threads and Slack design feedback with a traceable, auditable process.

Core responsibilities:
- Submit designs for review with context (user story, acceptance criteria)
- Track review status from Draft → In Review → Changes Requested → Approved → Implemented
- Annotate designs with specific feedback pinned to design areas
- Link UI reviews to product roadmap features and releases
- Measure cycle time from design submission to approval and to implementation
- Maintain a historical archive of all design decisions and rationale
- Enforce design system compliance checks before review approval
- Coordinate multi-surface reviews (same flow on desktop + mobile requiring separate review)

**Scale:**
- 10–30 active design reviews at any given time
- 4 reviewers minimum per review (PM, QA, dev lead, UI/UX peer)
- Covers all 4 surfaces: admin portal · institution portal · student portal · mobile app
- Full history retained indefinitely for institutional design decision audit
- Review cycle target: Draft → Approved in ≤ 5 business days

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "UI Review Board"          [New Review]  [My Reviews]  Filters │
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 5 cards                                            │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  Board (Kanban) · All Reviews · My Pending · Analytics          │
│  Design Tokens · Audit Log                                      │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 5 Cards

| # | Label | Value | Delta | Click Action |
|---|---|---|---|---|
| 1 | Active Reviews | Reviews in Draft / In Review / Changes Requested | — | Switches to Board tab |
| 2 | Awaiting My Approval | Reviews where logged-in user is a required approver | — | Switches to My Pending |
| 3 | Approved This Month | Reviews that reached Approved status this month | vs last month | Filters All Reviews |
| 4 | Avg Cycle Time | Average days from submission to approval (last 30d) | vs last month | Opens Analytics |
| 5 | Overdue Reviews | Reviews in "In Review" for > 5 days with no action | — | Filters board to overdue |

KPI values animate count-up 0 → final over 600ms on page load. Guard: `data-animated="true"` prevents re-animation on partial HTMX swaps.

---

## Tab 1 — Board (Kanban)

Visual board showing all active reviews as cards in workflow-stage columns.

### Columns (5 stages)

| Stage | Description | Card Colour Border | WIP Advisory |
|---|---|---|---|
| Draft | Design submitted but review not yet started | Grey | No limit |
| In Review | Active review in progress, reviewers assigned | Blue | Alert if > 8 |
| Changes Requested | Reviewer(s) have requested changes | Amber | Alert if > 5 |
| Approved | All required approvers have approved | Green | Auto-archive after 30d |
| Implemented | Corresponding code is deployed | Indigo | Auto-archive after 7d |

Column header shows: stage name + count of cards in stage. If WIP advisory threshold is exceeded the count badge turns amber.

### Review Card (on the board)

Each card shows:
- Review title (truncated at 45 chars)
- Surface badge: Admin Portal / Institution Portal / Student Portal / Mobile App
- Priority: P0 / P1 / P2 / P3 badge
- Component(s) affected (first 2, "+N more" if more)
- Submitter avatar + name
- Reviewer avatars (up to 3, "+N" if more)
- Days in current stage (warning icon if > 3 days; red if > 5 days)
- Linked feature / release badge (if linked)
- Comment count (speech bubble icon + number)
- Design system compliance badge: ✓ Compliant / ⚠ Check Required / ✗ Non-compliant
- Actions (⋮): Edit · View · Assign Reviewer · Archive

**Card click** → opens Review Detail Drawer.

**Drag-and-drop:** Cards can be dragged between columns (with permission). Business rules:
- Moving to "In Review": requires at least 2 required reviewers assigned
- Moving to "Approved": blocked unless all required approvers have individually approved (tooltip shows who is pending)
- Moving to "Implemented": requires a linked PR or deploy reference field (opens inline prompt if missing)
- Moving backwards (e.g. Approved → Changes Requested): allowed with mandatory change reason

### Board Filter Bar

Filters applied to the board view (sticky, persists per user session):
- Surface: All / Admin Portal / Institution Portal / Student Portal / Mobile App
- Priority: All / P0 / P1 / P2 / P3
- My reviews only: toggle (shows only cards where logged-in user is submitter or reviewer)
- Linked release: dropdown
- Overdue only: toggle (cards in current stage > 5 days)

---

## Tab 2 — All Reviews

Table view of all reviews (active + archived).

### Toolbar

| Control | Options |
|---|---|
| Search | Review title, component name, submitter name |
| Stage | All / Draft / In Review / Changes Requested / Approved / Implemented / Archived |
| Surface | All / Admin Portal / Institution Portal / Student Portal / Mobile App |
| Priority | All / P0 / P1 / P2 / P3 |
| Submitter | Filter by submitter name |
| Date range | Submitted date range |
| Linked release | Dropdown of all releases |
| Design system | All / Compliant / Check Required / Non-Compliant |

### Review Table — 10 columns

| Column | Detail |
|---|---|
| Review Title | Link to review detail drawer |
| Surface | Badge |
| Priority | Badge |
| Components | First 2 component names + count badge |
| Submitter | Avatar + name |
| Stage | Status badge |
| Reviewers | Avatar stack (up to 4) + approval status (✓ approved / ⏳ pending / ✗ changes requested per avatar) |
| Submitted | Date |
| Last Activity | Relative time |
| Cycle Time | Days from submission to current date (or to approval date if approved) |

**Bulk actions** (select multiple rows):
- Assign reviewer to selected
- Change priority of selected
- Archive selected
- Export selected to CSV / PDF report

**Pagination:** Showing X–Y of Z reviews · page pills · per-page selector (10 / 25 / 50 / 100)

---

## Tab 3 — My Pending

Focused view for the logged-in user. Shows only reviews where action is needed from them.

### Sub-sections:

**Awaiting My Review:**
Reviews where the logged-in user is listed as a required reviewer and has not yet approved or commented. Sorted by days in stage descending (most urgent first). Colour-coded: green (< 2 days) · amber (2–4 days) · red (> 4 days). Quick-action buttons inline:
- "Approve" (green) — opens approval confirmation with optional comment
- "Request Changes" (amber) — opens Request Changes Response Drawer
- "View" (opens Review Detail Drawer to Design tab)

**My Submitted — Awaiting Others:**
Reviews submitted by the logged-in user that are waiting for others to review. Shows:
- Review title
- Stage
- Who is still pending (avatar + name)
- Days waiting
- "Nudge" button → sends an in-app notification to pending reviewers (max once per 24h to prevent spam)

**Changes Requested on My Reviews:**
Reviews submitted by the logged-in user where a reviewer has requested changes. Sorted by oldest change request first. Shows:
- Review title
- Reviewer who requested changes
- Summary of change request (first 80 chars)
- "Resubmit" button → opens Resubmit Drawer

**My Optional Reviews:**
Reviews where the logged-in user is listed as an optional (FYI) reviewer. Shown collapsed by default with count badge. Same card format but "Approve" button shown as "Mark as Reviewed (Optional)".

---

## Tab 4 — Analytics

Performance metrics for the design review process. All charts use the 30-day default view with selector: 7d / 30d / 90d / All time.

### Summary Cards (4 cards)

| Card | Value |
|---|---|
| Avg Time: Submission → In Review | Hours/days — how long designs sit in Draft before someone picks them up |
| Avg Time: In Review → Approved | Hours/days — how long the actual review takes |
| Avg Time: Approved → Implemented | Hours/days — delay between design approval and code deployment |
| Total Cycle Time (End-to-End) | Days — full journey from first submission to code deployed |

### Cycle Time Trend Chart

Line chart: average cycle time (submission to approval) per week over last 12 weeks. X-axis: weeks. Y-axis: days. Two lines: Approved reviews and all reviews (including those still in progress). Shows if review process is getting faster or slower. Reference line at 5 days (target SLA).

### Bottleneck Analysis

Bar chart: average time spent in each stage across all completed reviews in the period. Sorted by time descending. Immediately shows which stage is the bottleneck.

| Stage | Avg Days | vs Previous Month | Count of Reviews |
|---|---|---|---|
| Draft | 0.4 days | ↓ 0.1 | 42 |
| In Review | 3.2 days | ↑ 0.5 | 38 |
| Changes Requested | 2.1 days | ↓ 0.3 | 21 |
| Approved → Implemented | 4.8 days | ↑ 1.2 | 31 |

### Reviewer Turnaround Table

All reviewers who received at least 1 review in the period:

| Reviewer | Role | Reviews Assigned | Avg Response Time | Approval Rate | Changes Requested Rate | Overdue Reviews |
|---|---|---|---|---|---|---|
| Priya Sharma (UI/UX) | UI/UX Designer | 28 | 1.2 days | 78% | 22% | 0 |
| Rahul Nair (PM Portal) | PM Institution Portal | 24 | 2.4 days | 83% | 17% | 1 |
| Deepa Menon (QA) | QA Engineer | 31 | 0.9 days | 91% | 9% | 0 |
| Arun Kumar | Dev Lead | 19 | 3.1 days | 74% | 26% | 2 |

Sorted by avg response time ascending by default. Clicking a reviewer row → filters All Reviews to show only that reviewer's reviews.

### Rejection Rate by Component Type

Bar chart: % of reviews that received "Changes Requested" at least once, grouped by component type (from component library). Helps identify which components have the highest design revision rate. Expected high-revision areas: Exam Interface, Results Page, Mobile Navigation.

### Review Volume by Surface

Stacked bar chart per week: count of new reviews by surface (Admin Portal / Institution Portal / Student Portal / Mobile App). Identifies which surface has the most design activity and whether it's trending up or down.

### Review Status Distribution

Donut chart: current counts by stage (Draft / In Review / Changes Requested / Approved / Implemented). Quick snapshot of pipeline health.

---

## Tab 5 — Design Tokens

Quick-reference view of all current design tokens, synced from the Design System page (page 19). This tab provides a design-review-focused lens: when reviewing a design in this board, reviewers can quickly verify that the design uses the correct token values.

### Token Categories

**Colour Tokens:**
- Brand colours: primary, success, warning, danger, info (full hex values and token names)
- Dark theme surface stack: 4 levels with hex values
- Light theme surface stack: 4 levels with hex values
- Chart palette: 8 categorical colours

**Typography Tokens:**
Complete table: token name · font family · weight · size · line height · usage guidance.

**Spacing Tokens:**
Token name → px value → when to use.

**Shadow Tokens:**
Token name → CSS value → use case.

**Border Radius Tokens:**
Token name → px value → use case.

### Component Checklist

For each review, a reviewer can open the Design Tokens tab and verify a checklist:
- "Uses only approved colour tokens" (yes / no / N/A)
- "Typography follows type scale" (yes / no / N/A)
- "Spacing follows spacing scale" (yes / no / N/A)
- "Touch targets ≥ 44px on mobile surfaces" (yes / no / N/A)
- "Contrast ratio meets WCAG 2.1 AA" (yes / no / N/A)
- "States documented (hover, focus, disabled, error)" (yes / no / N/A)

This checklist is saved per review and contributes to the design system compliance badge on the review card.

---

## Tab 6 — Audit Log

Complete immutable audit trail of all actions taken on the review board.

### Filters

- Date range (default: last 30 days)
- Admin / reviewer name
- Review title or ID
- Action type: Created / Reviewer Added / Approved / Changes Requested / Resubmitted / Stage Changed / Archived / Annotation Added / Annotation Resolved / Marked Implemented
- Surface
- Priority

### Audit Table

| Column | Detail |
|---|---|
| Timestamp | Full date and time (IST) |
| Actor | Avatar + name + role |
| Action | Colour-coded badge |
| Review | Review title with link to review |
| Detail | 1-line summary of what changed (e.g. "Stage moved from In Review → Approved") |
| Surface | Badge |
| IP Address | For security audit purposes |

**Pagination:** 25 / 50 / 100 per page. CSV export.

---

## Review Detail Drawer (840px)

Opens when clicking any review card. Largest drawer in the system — provides full review workspace.

### Drawer Header

- Review title (editable if submitter or admin)
- Stage badge (with stage transition buttons in a row)
- Priority badge (P0/P1/P2/P3 — editable by PM)
- Surface badge
- Submitter avatar + submitted date
- "Linked to:" feature/release/roadmap item badge (clickable → opens linked item in new tab)
- Design system compliance badge (auto-calculated from token checklist)
- "Share" button: copies a deep link to this review

### Stage Transition Buttons (shown inline in header)

Contextual based on current stage and role of logged-in user:
- In Draft: "Submit for Review" button (available to submitter). Requires at least 2 required reviewers and a Figma/design URL assigned.
- In Review: "Approve" (green) + "Request Changes" (amber) — available only to required reviewers. If logged-in user is the submitter, buttons are greyed out with tooltip "Submitters cannot approve their own reviews."
- In Changes Requested: "Resubmit" button (available to submitter). Disabled until all open blocker annotations are resolved.
- Approved: "Mark as Implemented" (requires PR link) — available to submitter or PM.
- Any stage: "Archive" (PM only) — available if review is superseded or cancelled.

### Drawer Tab 1 — Design

**Design Preview Area (main content):**
- Embedded Figma frame (or uploaded image/PNG/PDF) in a responsive viewer
- Zoom controls: 50% / 75% / 100% / Fit to window
- Device frame toggle: Browser frame / Mobile frame (iOS) / Mobile frame (Android) / Tablet frame / No frame
- Full-screen expand button (opens preview in a new window at full resolution)
- Annotation pin overlay: numbered pins (A1, A2…) overlaid on the design. Pins are clickable → jumps to that annotation in Tab 3.

**Design File Links:**
- Primary design file (Figma URL, opens in new tab)
- Prototype link (if available — shows "Play" icon, opens interactive prototype in Figma)
- Redline / spec link (if available — for developer handoff specs)
- Accessibility audit link (optional — links to WCAG audit document)

**Version selector:**
If design has been revised (after "Request Changes"), a version dropdown shows all versions:
- v1 (original, date) · v2 (after first revision, date) · v3 (current, date)
- "Compare v2 vs v3" button → opens side-by-side comparison view. Left panel shows older version, right panel shows newer. Annotation pins from both versions shown simultaneously.
- Version notes shown below selector (what changed in each revision)

---

### Drawer Tab 2 — Context

Provides reviewers with the full context needed to evaluate the design. All fields are editable by the submitter until the review moves to "Approved".

| Field | Content |
|---|---|
| User Story | Full user story: "As a [role], I want [action] so that [outcome]" |
| Acceptance Criteria | Numbered list of AC items with checkboxes (reviewers tick criteria as verified; tickboxes are per-reviewer so all reviewers independently verify) |
| Design Goals | What this design aims to achieve (max 5 bullet points) |
| Scope | What is in scope / out of scope for this review |
| Design Decisions | Key decisions made with rationale (markdown text, unlimited length) |
| Alternatives Considered | Other approaches explored and why they were rejected (table: Option · Reason Rejected) |
| Related Reviews | Links to related past or concurrent reviews (searchable dropdown of all reviews) |
| Technical Constraints | Known technical limitations the designer was working within (e.g. "HTMX constraint: cannot use browser history API for tab state") |
| Accessibility Notes | Known accessibility considerations and how they were addressed |
| Internationalisation Notes | Whether design accommodates RTL, Hindi text, longer translated strings |

---

### Drawer Tab 3 — Annotations

Structured review comments linked to specific areas of the design.

**Annotation List:**

Each annotation:
- Sequence number (A1, A2, …) matching pin overlay on the design
- Area (e.g. "Navigation bar" / "Submit button" / "Error state" — free text)
- Comment text (markdown supported — bold, italic, inline code, numbered lists)
- Reviewer avatar + name
- Timestamp
- Status: Open / Resolved / Won't Fix / Deferred
- Reply thread (nested replies, up to 3 levels; same markdown support)
- Priority: Blocker (red, must be resolved before resubmit) / Major (orange) / Minor (yellow) / Suggestion (blue, non-blocking)
- Design system related: Yes/No badge (Yes = token violation or pattern violation)

**"Add Annotation" button:** Opens a compact form:
- Area field (text, with autocomplete from common area names)
- Comment field (markdown textarea)
- Priority selector (Blocker / Major / Minor / Suggestion)
- Design system related toggle
- Submit

**Bulk actions on annotations:**
- Select multiple → "Mark as Resolved" (available to submitter)
- Select multiple → "Defer to next sprint" (changes status to Deferred)

**Filter annotations:**
- All / Open / Resolved / Deferred / Won't Fix
- By reviewer
- Blockers only
- Design system issues only

**Annotation export:**
"Export Annotations" → downloads CSV with all annotations, their status, and resolution notes. Used for tracking design debt across multiple reviews.

---

### Drawer Tab 4 — Approval Status

Shows the approval status of all required reviewers.

**Required Reviewers Table:**

| Reviewer | Role | Status | Response Date | Comment |
|---|---|---|---|---|
| Priya Sharma | UI/UX Designer | ✓ Approved | 15 Mar 2026, 2:34 PM | "Looks great, approved" |
| Rahul Nair | PM Institution Portal | ✓ Approved | 15 Mar 2026, 4:12 PM | — |
| Deepa Menon | QA Engineer | ⏳ Pending | — | — |
| Arun Kumar | Dev Lead | ✓ Approved | 14 Mar 2026, 11:20 AM | "Feasible, noted the interaction" |

**Optional Reviewers:**
Same table but labelled "Optional — FYI only". Their approval is not required and not blocking.

**Overall status:** "3 of 4 required approvals received"

**Progress bar:** Visual fill showing approval progress.

**Add Reviewer button:** PM or submitter can add more required or optional reviewers after submission. Adding a required reviewer after some have already approved does not invalidate existing approvals but does block Approved status until new reviewer responds.

**Remove Reviewer button:** Available to PM only. Requires confirmation. Cannot remove a reviewer who has already approved or requested changes (audit trail must be maintained).

**Approve button** (if logged-in user is a required reviewer and has not approved): large green button with optional comment field. Clicking prompts: "Add a comment with your approval (optional)" → "Confirm Approval".

**Request Changes button** (amber): opens Request Changes Response Drawer.

---

### Drawer Tab 5 — Activity

Full activity feed for this review, most recent first:

- Review submitted (submitter, date)
- Reviewer A added as required reviewer (by submitter)
- Reviewer B added as optional reviewer (by submitter)
- Reviewer A commented on design (annotation A1 added)
- Reviewer B requested changes (annotation A2: "Navigation layout — Blocker")
- Submitter uploaded v2 (with revision notes)
- Reviewer B resolved annotation A2
- Reviewer A approved v2
- Reviewer B approved v2
- Reviewer C approved (3 of 4 approvals)
- Reviewer D approved (all 4 approved → stage auto-moved to Approved)
- Linked to Release 4.2.1
- PR #482 link added
- Marked as Implemented (by submitter)

Each entry: avatar + name + action + timestamp. Activity feed is append-only; nothing is deleted.

---

## New Review Modal

**Step 1 — Basic Info:**
- Review Title (required, max 80 chars)
- Surface: Admin Portal / Institution Portal / Student Portal / Mobile App
- Priority: P0 (Critical UX change) / P1 (Significant change) / P2 (Minor change) / P3 (Cosmetic)
- Components affected (multi-select from component library — grouped by category)
- Design file URL (Figma URL, required if no file upload; or upload PNG/PDF up to 20MB)
- Prototype URL (optional)

**Step 2 — Context:**
- User Story (required, pre-filled template: "As a [role], I want [action] so that [outcome]")
- Acceptance Criteria (required, at least 1 item; + Add Item button for multiple)
- Design Goals (optional, up to 5 bullet points)
- Linked Feature / Release / Roadmap Item (optional, searchable dropdown of roadmap items and releases)

**Step 3 — Reviewers:**
- Required Reviewers (multi-select from team member directory; at least 2 required)
- Optional Reviewers (multi-select)
- Due date (optional; if set, overdue badge appears after this date)
- Notify on submission: Yes / No toggle (sends in-app + email notification to all assigned reviewers)

**Submit:** Creates review in Draft stage. Confirmation shown: "Review created. Submit for review when your design is ready."

**"Submit for Review" shortcut:** Checkbox on the modal to immediately move from Draft → In Review on creation (skips the extra step for ready designs).

---

## Request Changes Response Drawer (480px)

Opened when reviewer clicks "Request Changes."

- Review summary (title + current version + submitter name)
- "Describe your requested changes" text area (required, markdown supported, min 20 chars)
- Category of changes: Layout / Colour / Typography / Interaction / Accessibility / Content / Design System Violation / Other (multi-select)
- Priority: Blocker (prevents resubmit until resolved) / Major / Minor / Suggestion
- "Add specific annotation" link: shortcuts to Add Annotation form after drawer submission
- "Submit Request" button → sends notification to submitter, moves review to "Changes Requested" stage

---

## Resubmit Drawer (560px)

Opened by submitter when resubmitting after "Changes Requested."

- Updated design file URL (required — must be different from previous version's URL)
- New Figma prototype URL (optional — if interaction changed)
- Version notes: "What changed in this version?" (required, min 50 chars, markdown supported)
- Annotation checklist: shows all annotations currently Open or Blocker — submitter marks each one:
  - "Resolved in this revision" → moves annotation to Resolved
  - "Won't Fix — with reason" → moves to Won't Fix (reason required)
  - "Deferred" → moves to Deferred (future revision)
- Warning: "Resubmit is blocked until all Blocker annotations are marked as Resolved or Won't Fix."
- "Resubmit for Review" button → returns review to "In Review" stage, notifies all required reviewers

---

## Mark as Implemented Modal

Opened when submitter clicks "Mark as Implemented."

- Review summary (title + approved date)
- PR link (required — GitHub PR URL; system validates URL format)
- Deploy date (date picker — when was/will be deployed to production)
- Release version (dropdown: selects which release this is part of; pre-populated if review is linked to a release)
- Deploy environment: Staging / UAT / Production (badge shown)
- Notes (optional — e.g. "A/B tested on 10% of institutions first")
- "Mark as Implemented" button → moves review to "Implemented" stage

After marking: review archived from active board automatically after 7 days but remains fully accessible in All Reviews with full history.

---

## Notification Rules

The review board sends the following notifications (in-app + email):

| Event | Recipients | Channel |
|---|---|---|
| Review submitted for review | All required reviewers | In-App + Email |
| Reviewer added to review | New reviewer | In-App |
| Reviewer approved | Submitter + other reviewers | In-App |
| Reviewer requested changes | Submitter | In-App + Email |
| All approvals received → Approved | Submitter + PM | In-App + Email |
| Review overdue (> 5 days in In Review) | Submitter + PM | In-App |
| Annotation added | Submitter | In-App |
| Annotation resolved | Annotation author | In-App |
| Review marked as implemented | All reviewers | In-App |

All notifications respect the global quiet hours (10pm–7am IST) except P0 priority reviews.

---

## SLA and Escalation Rules

| Review Priority | Target Response Time | Target Approval Time | Escalation |
|---|---|---|---|
| P0 | Required reviewer must respond within 4 hours | Approved within 1 business day | Auto-alert PM Platform + email if missed |
| P1 | Required reviewer must respond within 1 business day | Approved within 3 business days | Alert PM if not approved by day 4 |
| P2 | No formal SLA | Approved within 5 business days | Advisory warning if > 5 days |
| P3 | No formal SLA | No SLA | No escalation |

"Response" means any action: approve, request changes, or add an annotation — not just approving.

Escalation recipients: PM Institution Portal for institution surface reviews; PM Platform for admin/backend surface reviews.

---

## Integration Points

| Page | Integration |
|---|---|
| Page 19 — Design System | Design Tokens tab synced from design system. Compliance badge derived from token checklist. Deprecated component warnings shown on review cards. |
| Page 03 — Release Manager | Reviews can be linked to a release. Release detail shows pending UI reviews as a blocking gate criterion. |
| Page 01 — Product Roadmap | Reviews can be linked to a roadmap feature. Roadmap feature detail shows associated review status. |
| Page 22 — Test Tenant Manager | "Test on Test Tenant" button in Dashboard Layouts drawer pushes preview to a test tenant. |
| Page 21 — QA Dashboard | QA engineer's review approvals count in reviewer turnaround metrics. |

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| 840px drawer | Largest in system | Design review needs space for design preview + annotations side-by-side without crowding |
| Annotation as structured data | Area + priority + status + threads | Unstructured comments in Figma are hard to track and resolve; structured annotations are trackable to closure |
| Version history | All design versions retained | Enables comparison between original and revised design; documents evolution of decisions |
| Required vs optional reviewers | Separate lists | Required = blocking. Optional = FYI. Prevents blocking review on absent optional reviewer. |
| "Mark as Implemented" requires PR link | Enforced | Creates a traceable link from design decision to code commit — closes the loop |
| Cycle time analytics | Tracked per review and aggregated | Design process needs data-driven improvement; cycle time is the key metric to optimise |
| Acceptance criteria checkboxes | Reviewers tick criteria as verified | Makes approval meaningful — reviewer confirms each AC, not just visual aesthetics |
| Annotation pins on design | Overlaid on Figma frame | Keeps feedback spatially relevant rather than a disconnected text list |
| Resubmit blocked on open Blockers | Enforced by business rule | Prevents submitters from ignoring critical feedback and re-requesting review without addressing issues |
| Nudge cooldown (once per 24h) | Rate-limited | Prevents review board from becoming a nagging tool; preserves reviewer experience |
| Design system compliance badge | Auto-calculated from token checklist | Surfaces compliance issues early in the review process before reaching engineering |
| Multi-surface review linking | Related Reviews field in Context tab | Same user flow may need separate reviews for desktop + mobile; links keep them connected without merging |
| P0 review SLA | 4h response / 1 business day approval | P0 priority designs (critical UX changes) need fast-track review to avoid blocking sprint delivery |

---

## Figma Design Handoff Tracker

**Purpose:** Bridges the gap between design completion and engineering implementation. A design approved in the review board needs to be handed off to Engineering (Division C Frontend Engineer, Role 12). Without tracking, designs get "done" in Figma but implementation is never started, delayed, or done incorrectly. The UI/UX Designer (read-only in all other operations) uses this tracker to know the status of their delivered designs.

**Who can update:** QA Engineer (confirming implementation verified) · Frontend Engineer (updating implementation status) · UI/UX Designer (uploading Figma link, read-only otherwise)

---

### Handoff Status Table

| # | Feature / Screen | Figma Link | Review ID | Handoff Date | Engineer | Implementation Status | QA Verified |
|---|---|---|---|---|---|---|---|
| 1 | Exam Timer Redesign | [Figma ↗] | UIR-142 | Mar 18 | Ravi (FE) | ✅ Implemented | ✅ Verified Mar 20 |
| 2 | Result Page v2 | [Figma ↗] | UIR-139 | Mar 10 | Priya (FE) | 🔨 In Progress | — |
| 3 | Mobile Onboarding Flow | [Figma ↗] | UIR-136 | Feb 28 | Kiran (Mobile) | 🔨 In Progress | — |
| 4 | Notification Settings Panel | [Figma ↗] | UIR-131 | Feb 15 | Ravi (FE) | ⬜ Not Started | — |
| 5 | Dark Mode Token Update | [Figma ↗] | UIR-128 | Feb 5 | Design (global) | ✅ Implemented | ✅ Verified Feb 18 |

**Implementation Status values:**
- ⬜ Not Started — Handoff delivered but Engineering hasn't started
- 🔨 In Progress — Engineering is actively implementing
- 👁 Ready for Review — Implementation complete, awaiting QA verification
- ✅ Implemented — QA verified against Figma spec
- ❌ Deferred — Implementation postponed (reason required)

**Stale alert:** If a handoff has been "Not Started" for > 10 working days, an amber badge appears on the row and the Designer is notified: "Handoff for 'Notification Settings Panel' has been pending for 12 days. Check with engineering."

---

### Figma Spec Compliance Check

After Engineering marks an implementation "Ready for Review", QA runs a **pixel/behaviour comparison** against the Figma spec and marks each criterion:

| Criterion | Status | Notes |
|---|---|---|
| Colours match design tokens | ✅ | — |
| Typography scale matches | ✅ | — |
| Spacing / padding correct | ⚠ | Result card padding is 16px, Figma shows 20px |
| Hover/focus states match | ✅ | — |
| Animation timing matches | ✅ | 300ms ease-in-out — confirmed |
| Mobile breakpoint correct | ❌ | Mobile view wraps incorrectly at 375px |
| Dark mode correct | ✅ | — |

**Overall verdict:** Partial match → returned to Engineering with specific notes. QA marks status back to "In Progress" until all criteria pass.

---

### Design Debt Dashboard

**Purpose:** Tracks designs that were approved in UI Review Board but are still NOT implemented after 30+ days. These represent design debt — accumulated gap between designed and built state.

| Design | Age (days unimplemented) | Priority | Last nudge | Actions |
|---|---|---|---|---|
| Notification Settings Panel | 33 days | P2 | Mar 15 | [Escalate to PM] [Mark Deferred] |
| Password Reset Flow Redesign | 28 days | P1 | Mar 18 | [Escalate to PM] |

**[Escalate to PM]:** notifies PM Platform (Role 5) and the feature's assigned PM that a design is overdue for implementation. PM decides to prioritise, defer, or cancel.

**Design debt threshold:** If total unimplemented approved designs > 15, the UI Review Board KPI strip card "Design Debt" turns amber.
