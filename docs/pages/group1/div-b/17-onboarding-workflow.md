# Page 17 — Onboarding Workflow

**URL:** `/portal/product/onboarding-workflow/`
**Permission:** `product.manage_onboarding`
**Priority:** P2
**Roles:** PM Institution Portal, PM Platform

---

## Purpose

Manages the end-to-end onboarding experience for new institutions joining the SRAV platform. Every school, college, coaching centre, and group that signs up receives a structured onboarding workflow: a series of guided steps that walk institution admins from account creation through to their first live exam. This page allows the SRAV product team to design, configure, monitor, and optimise that onboarding journey.

Core responsibilities:
- Build and maintain onboarding workflow templates for each institution type
- Monitor real-time onboarding progress across all currently-onboarding institutions
- Identify where institutions drop off during onboarding (funnel analysis)
- Assign SRAV customer success managers to assist high-value institutions
- Track time-to-first-exam (key activation metric)
- Configure welcome emails, in-portal tips, and checklist items
- A/B test different onboarding flows to improve activation rate
- Re-onboard dormant institutions that have not used the platform in 60+ days

**Scale:**
- 1,950+ total institutions onboarded historically
- Typically 20–80 new institutions onboarding in any given month
- 4 institution types with distinct onboarding paths
- Time-to-first-exam target: < 7 days for Standard+, < 3 days for Enterprise
- Estimated activation rate target: 70% of started onboardings complete within 14 days
- 150 groups with 5–50 child institutions: groups have a special group-level onboarding before child institution onboarding

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Onboarding Workflow"           [New Workflow]  [Export Report] │
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 6 cards (auto-refresh every 120s)                  │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  Live Dashboard · Workflow Builder · Funnel Analytics           │
│  Institution Queue · Email Sequences · Audit Log                │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 6 Cards (auto-refresh every 120s)

| # | Label | Value | Delta | Click Action |
|---|---|---|---|---|
| 1 | Currently Onboarding | Institutions in active onboarding (not yet completed) | — | Opens Institution Queue |
| 2 | Completed This Month | Institutions that reached "onboarding complete" this month | vs last month | Opens Institution Queue filtered |
| 3 | Avg Days to Activation | Average days from signup to first live exam | vs last month | Opens Funnel Analytics |
| 4 | Stuck (>7 days stalled) | Institutions with no progress in 7+ days | — | Opens Institution Queue with stalled filter |
| 5 | Completion Rate | % of started onboardings that reach completion | vs last month | Opens Funnel Analytics |
| 6 | CSM Assigned | Institutions currently assigned to a customer success manager | — | Opens Institution Queue |

All values animate count-up on load. Poll guard: `every 120s[!document.querySelector('.drawer-open,.modal-open')]`.

---

## Tab 1 — Live Dashboard

Real-time view of all institutions currently in the onboarding pipeline.

### Pipeline View

Horizontal Kanban-style board with stages as columns. Each column shows institution cards in that stage. Columns are scrollable horizontally on smaller screens.

**Onboarding Stages (columns):**

| Stage | Description | Target Time | Entry Condition |
|---|---|---|---|
| Account Created | Signup complete, no steps done | Day 0 | Signup form submitted |
| Profile Setup | Basic info entered (institution name, type, logo) | Day 0–1 | Admin first login |
| User Setup | Admin users created and roles assigned | Day 1–2 | Profile complete |
| Domain Selected | At least one exam domain subscribed | Day 1–2 | User setup done |
| First Content Added | First exam or question uploaded | Day 2–4 | Domain selected |
| First Students Added | At least 10 students imported or enrolled | Day 2–5 | Content exists |
| First Exam Scheduled | An exam with a future date scheduled | Day 3–6 | Students added |
| Completed | First exam has been live (attempted by at least 1 student) | Day 3–7 | Exam held |

**Each institution card shows:**
- Institution name (bold) + type badge (School / College / Coaching / Group) + plan badge
- Days since signup (shown as "Day 5")
- Current step progress (e.g. "Step 4 of 8") with mini progress bar
- CSM assigned: avatar + name, or "Unassigned" badge (amber)
- Last activity: relative time (e.g. "2h ago" / "3 days ago")
- Warning indicator (⚠ amber) if stalled > 3 days in current stage
- Critical indicator (✗ red) if stalled > 7 days in current stage

**Card context menu (right-click or ⋮):**
- Assign CSM (opens CSM selector dropdown)
- Send nudge email (from active email sequence)
- View full profile (opens Institution Onboarding Detail Drawer)
- Override stage (force advance — logs override in audit)
- Mark as Completed (for manually-assisted onboardings)
- Archive (removes from active pipeline — not deleted, moves to Archived status)

**Stage column headers show:**
- Stage name
- Count of institutions in this stage (large number)
- Average days currently spent in this stage across all institutions in it
- vs target: (✓ on target) or (⚠ X.X days over target)

### Live Funnel Chart

Below the Kanban board. Horizontal funnel chart showing:
- Total institutions that entered each stage this month
- Drop-off count and % between each stage
- Conversion rate from first stage to completion

```
Account Created     ████████████████████████████████████  120
Profile Setup       █████████████████████████████████     104  (87%)
User Setup          ██████████████████████████████        98   (82%)
Domain Selected     ████████████████████████             86   (72%)
First Content Added ██████████████████████              78   (65%)
First Students      █████████████████████               72   (60%)
First Exam Sched.   ████████████████████                68   (57%)
Completed           ████████████████████                65   (54%)
```

Clicking any stage bar → filters Institution Queue to show institutions at that stage. Clicking the drop-off count between stages → shows which specific institutions dropped off there.

### Onboarding Health Score

A composite score (0–100) displayed below the funnel:
- Completion rate: 40%
- Avg days to activation vs target: 30%
- Stalled institution count: 20%
- CSM coverage (assigned vs unassigned): 10%

Green ≥ 75 · Amber 50–74 · Red < 50.

---

## Tab 2 — Workflow Builder

Design and edit the onboarding checklist shown inside the institution portal to new admins.

### Workflow Template Selector

Dropdown to select which workflow to edit:
- School Onboarding Workflow (12 steps)
- College Onboarding Workflow (12 steps)
- Coaching Centre Onboarding Workflow (16 steps — additional finance and test series steps)
- Group Onboarding Workflow (8 steps — group-level setup before child institution onboarding)
- Enterprise Fast-Track (6 steps — accelerated 3-day flow for Enterprise-tier accounts)
- Re-onboarding Workflow (5 steps — for dormant institutions returning after 60+ day gap)

Current default badge shown next to active default for each type.

### Workflow Step List

Ordered list of all steps in the selected workflow. Drag-and-drop to reorder.

Each step row shows:

| Field | Detail |
|---|---|
| Step Number | Auto-assigned based on order (updates on reorder) |
| Step Name | Short display name (e.g. "Upload Institution Logo") |
| Description | 2-3 sentence explanation shown to the institution admin |
| Category | Profile / Users / Content / Students / Exam / Settings / Integration / Finance |
| Required / Optional | Toggle |
| Completion Trigger | How the system detects step completion (e.g. "logo_url is not null") |
| Estimated Time | "~5 mins" label shown to admin |
| Help Link | Optional URL to help article |
| Actions | Edit (pencil) · Move (drag handle) · Delete |

### Full Step List (School/College Workflow — 12 steps)

| Step | Name | Category | Required | Completion Trigger | Estimated Time |
|---|---|---|---|---|---|
| 1 | Complete Institution Profile | Profile | Yes | all required profile fields filled | ~10 min |
| 2 | Upload Logo and Banner | Profile | No | logo_url is not null | ~3 min |
| 3 | Set Institution Timezone | Settings | Yes | timezone field set | ~1 min |
| 4 | Create Admin Users | Users | Yes | admin_user_count ≥ 1 (non-owner) | ~5 min |
| 5 | Assign Faculty Roles | Users | No | faculty_user_count ≥ 1 | ~5 min |
| 6 | Create First Student Batch | Students | Yes | batch_count ≥ 1 | ~3 min |
| 7 | Import Students | Students | Yes | student_count ≥ 10 | ~10 min |
| 8 | Select Exam Domains | Content | Yes | domain_subscription_count ≥ 1 | ~5 min |
| 9 | Upload or Select First Exam | Content | Yes | exam_count ≥ 1 (draft or scheduled) | ~15 min |
| 10 | Configure Exam Settings | Content | Yes | exam.pattern is not null | ~5 min |
| 11 | Schedule Your First Exam | Exam | Yes | exam.scheduled_date is in future | ~3 min |
| 12 | Announce to Students | Communication | No | announcement_count ≥ 1 | ~3 min |

### Coaching Centre Workflow — Additional Steps

| Step # | Name | Category | Required |
|---|---|---|---|
| 6a | Create Coaching Batches by Exam Target | Students | Yes |
| 9a | Set Up Test Series (group exam sets) | Content | No |
| 11a | Enable Student Leaderboard | Exam | No |
| 12a | Configure Fee Collection (if Finance feature enabled) | Finance | No |

### Group Onboarding Workflow — Steps

| Step | Name | Category | Required |
|---|---|---|---|
| 1 | Complete Group Profile | Profile | Yes |
| 2 | Upload Group Logo | Profile | No |
| 3 | Add Child Institutions | Settings | Yes |
| 4 | Configure Group Branding Defaults | Profile | No |
| 5 | Set Group-Level Admin Users | Users | Yes |
| 6 | Configure Shared Exam Domains | Content | No |
| 7 | Review Child Institution Onboarding Progress | Dashboard | No |
| 8 | Schedule First Group-Wide Exam | Exam | No |

### Step Edit Drawer (480px)

Opened by clicking pencil icon on any step. Fields:
- Step Name (max 60 chars)
- Description (max 300 chars, rich text — supports bold, links, numbered lists)
- Category (dropdown)
- Required toggle
- Completion trigger (dropdown of available system conditions, grouped by entity):
  - Institution: profile_complete / logo_uploaded / timezone_set
  - Users: admin_user_count ≥ N / faculty_user_count ≥ N
  - Students: student_count ≥ N / batch_count ≥ N
  - Content: exam_count ≥ N / domain_subscribed / question_count ≥ N
  - Finance: payment_gateway_configured
  - Custom: advanced raw ORM-expression field (for non-standard conditions)
- Estimated time (text, e.g. "~5 mins")
- Help article URL
- In-portal tip text (short helper tooltip shown when admin hovers the step)
- Email trigger toggle: "Send sequence email when this step completed" — links to email sequence
- Celebration message: text shown in portal when step is completed (e.g. "Great! Your students are added. 🎉")

### Add New Step

"+ Add Step" button at bottom of list opens an inline form (same fields as Step Edit Drawer but inline). Step is added at the bottom and can be dragged to its position.

---

## Tab 3 — Funnel Analytics

Detailed funnel analysis to optimise the onboarding flow. All charts segmentable by period, institution type, plan, geography.

### Funnel Summary Cards (4 cards)

| Card | Value |
|---|---|
| Overall Completion Rate | % of signups that reach "Completed" stage (last 30d) |
| Avg Time to First Exam | Mean days from signup to first live exam |
| Biggest Drop-off Step | Step name with highest abandonment %, with % shown |
| Best Performing Type | Institution type with highest completion rate (last 30d) |

### Funnel Chart (full width)

Step-by-step horizontal funnel. Period selector: last 7d / 30d / 90d / all time.

For each step:
- Entered: institutions that reached this step
- Completed: institutions that passed this step
- Drop-off: count and %
- Avg time spent: average days between entering and completing this step
- vs Target: comparison to configured target time per step

### Drop-off Analysis Table

| Step | Entered | Completed | Drop-off | Drop-off % | Avg Days in Step | Target | Status |
|---|---|---|---|---|---|---|---|
| Account Created | 120 | 104 | 16 | 13.3% | 0.2 days | 0.5 days | ✓ |
| Profile Setup | 104 | 98 | 6 | 5.8% | 0.8 days | 1 day | ✓ |
| User Setup | 98 | 86 | 12 | 12.2% | 1.4 days | 2 days | ✓ |
| Domain Selected | 86 | 78 | 8 | 9.3% | 2.1 days | 2 days | ✓ |
| First Content Added | 78 | 65 | 13 | 16.7% | 3.4 days | 2 days | ⚠ Over |
| First Students Added | 65 | 62 | 3 | 4.6% | 1.2 days | 2 days | ✓ |
| First Exam Scheduled | 62 | 60 | 2 | 3.2% | 1.8 days | 3 days | ✓ |
| Completed | 60 | 57 | 3 | 5.0% | 0.4 days | 1 day | ✓ |

Rows where drop-off % is above 15% or avg time is over target: amber/red row highlight. "Investigate" button on highlighted rows → filters Institution Queue to show institutions stuck at that step.

### Cohort Analysis Table

Shows completion rate by signup month. Enables trending — did Feb's cohort complete faster than Jan?

| Signup Month | Signups | 7-day Completion | 14-day Completion | 30-day Completion | Final Completion Rate |
|---|---|---|---|---|---|
| Mar 2026 | 42 | 28% | 54% | — (in progress) | — |
| Feb 2026 | 38 | 32% | 58% | 76% | 79% |
| Jan 2026 | 51 | 25% | 49% | 66% | 71% |
| Dec 2025 | 44 | 30% | 55% | 72% | 75% |

Colour coding: each cell coloured against the cohort average (green = above avg, amber = below).

### Segmentation Filters

All funnel charts and tables can be segmented by:
- Institution type (School / College / Coaching / Group) — separate funnel per type
- Plan tier (Starter / Standard / Professional / Enterprise)
- Geographic state (dropdown of Indian states)
- CSM assigned / Unassigned
- Signup source (organic / referral / sales-assisted / partner)
- Time period: last 7d / 30d / 90d / custom range

### A/B Test Results (if active test)

If an active A/B test is running on the onboarding flow, results shown in a comparison panel:
- Variant A: original flow (control group)
- Variant B: test flow
- Side-by-side funnel comparison
- Statistical significance indicator (p-value)
- Estimated completion rate improvement

---

## Tab 4 — Institution Queue

Full list of all institutions in active onboarding. Sortable, searchable, and filterable.

### Toolbar

| Control | Options |
|---|---|
| Search | Institution name, city, state |
| Stage filter | All stages (multi-select checkboxes) |
| Institution type | All / School / College / Coaching / Group |
| Plan tier | All / Starter / Standard / Professional / Enterprise |
| CSM filter | Unassigned / Assigned to me / Specific CSM name |
| Status | All / On Track / At Risk / Stalled / Overdue |
| Geography | State filter (dropdown, multi-select) |

**Status criteria:**
- **On Track:** last activity within 48 hours, on or ahead of expected timeline
- **At Risk:** last activity 2–4 days ago, or behind expected timeline by 1–2 days
- **Stalled:** no activity in 5–7 days
- **Overdue:** no activity in > 7 days OR total time exceeds 14 days without completion

### Institution Queue Table — 10 columns

| Column | Detail |
|---|---|
| Institution Name | Bold + type badge + plan badge |
| Type | School / College / Coaching / Group |
| Signup Date | Date |
| Current Stage | Stage name with step progress (e.g. "Step 6 / 12") |
| Days Elapsed | Since signup (colour-coded: green < 7 · amber 7–14 · red > 14) |
| Status | On Track (green) · At Risk (amber) · Stalled (orange) · Overdue (red) |
| Completion % | Progress bar (steps completed / total steps) with % label |
| CSM | Avatar + name, or "Unassigned" (amber badge) |
| Last Activity | Relative time (e.g. "2 days ago") |
| Actions | View · Assign CSM · Send Nudge · Override Stage |

**Sorting:** Default by status (Overdue first, then Stalled, etc.). Can sort by any column.

**Pagination:** Showing X–Y of Z institutions · page pills · per-page selector (10 / 25 / 50 / 100)

### Bulk Actions

Select multiple rows (checkbox per row):
- Assign CSM (dropdown to select from CSM list)
- Send bulk nudge email (from active email sequence)
- Export selected to CSV (for offline analysis)
- Mark as completed (for bulk-assisted onboardings)

### Institution Onboarding Detail Drawer (640px)

Opened by "View" action on any row.

**Drawer Header:** Institution name · type · plan · signup date · overall status badge

#### Drawer Tab 1 — Progress

- Checklist of all onboarding steps with status:
  - ✓ Completed (green) — shows completion timestamp and user who triggered it
  - → In Progress (amber) — shows when step was started
  - ○ Not Started (grey) — shows estimated time
- Overall progress bar at top (X of Y steps completed)
- "Time in current stage" shown (e.g. "3 days in First Content Added")
- Completion trigger value shown for completed steps (e.g. "student_count = 47 ≥ 10")

#### Drawer Tab 2 — Activity Log

Chronological timeline of all institution activity related to onboarding:
- Account created (signup form submitted)
- Profile edited (which fields changed)
- User added (username + role)
- Domain subscribed (domain name)
- Exam created (exam title)
- Students imported (count)
- Announcement sent
- Admin login events
- CSM assigned

Each entry: timestamp · action · user who performed it · detail.

#### Drawer Tab 3 — CSM Notes

- All CSM notes shown newest-first
- Each note: timestamp · CSM avatar + name · note text (markdown rendered)
- "Add Note" button → inline text area with save button
- Notes are private to SRAV team (not visible to institution admin)
- Note categories (tag): Call Completed / Issue Raised / Commitment Made / Follow-up Required

#### Drawer Tab 4 — Communications

All automated and manual emails sent to this institution during onboarding:

| Subject | Type | Sent Date | Opened | Clicked | Triggered By |
|---|---|---|---|---|---|
| "Welcome to SRAV" | Automated | 15 Mar 10:05 | Yes | Yes | Account Created |
| "3 quick steps to get started" | Automated | 16 Mar 10:05 | Yes | No | Day 1 drip |
| "Need help with content?" | Manual | 17 Mar 14:30 | No | No | CSM Riya Sharma |
| "Your students are waiting" | Automated | 18 Mar 10:05 | — | — | Day 3 drip |

"Send Manual Email" button: opens email compose (subject pre-filled with institution name; body from template selector).

#### Drawer Tab 5 — Institution Profile (summary)

Quick reference card showing:
- Institution name, type, plan
- City + state
- Contact: admin name + email + phone
- Student count (current)
- Exam domain subscriptions
- "Open Full Profile" link → opens full institution management page

**Footer action buttons:**
- Assign / Reassign CSM
- Send Manual Email
- Override Stage (with dropdown: which stage to move to + reason required)
- Mark as Completed
- Archive (removes from active queue with reason)

---

## Tab 5 — Email Sequences

Automated email drip sequences sent to institutions at various points in the onboarding journey.

### Sequence List

| Sequence Name | Trigger | Emails in Sequence | Status | Open Rate (avg) |
|---|---|---|---|---|
| Welcome Sequence | Account created | 4 emails | Active | 52% |
| Nudge Sequence — Profile | Profile incomplete after 24h | 2 emails | Active | 38% |
| Nudge Sequence — Students | No students after 3 days | 3 emails | Active | 34% |
| Nudge Sequence — First Exam | No exam scheduled after 5 days | 3 emails | Active | 31% |
| Stalled Institution Alert | No activity for 7 days | 1 email + CSM in-app alert | Active | 45% |
| Completion Celebration | Onboarding completed | 1 email | Active | 70% |
| Post-Completion Tips | 7 days after first exam | 3 emails | Active | 41% |
| Re-onboarding Welcome | Re-activated after 60+ day dormancy | 2 emails | Active | 55% |

Clicking any sequence → expands to show all emails in the sequence.

### Sequence Email Detail

For each email in the sequence:

| # | Email Subject | Delay After Trigger | Status | Sent (30d) | Open Rate | Click Rate | Unsubscribe Rate |
|---|---|---|---|---|---|---|---|
| 1 | "Welcome to SRAV — Your portal is ready" | Immediately | Active | 62 | 68% | 42% | 0.5% |
| 2 | "3 quick steps to get started" | 1 day | Active | 59 | 51% | 31% | 0.8% |
| 3 | "Your students are waiting — add them today" | 3 days | Active | 51 | 38% | 22% | 1.1% |
| 4 | "You're almost there — schedule your first exam" | 5 days | Active | 44 | 29% | 18% | 0.9% |

Each email: "Edit" button → opens email editor (same as notification template manager, page 18). "Preview" button → shows rendered email with sample institution data.

### A/B Test on Sequences

Any email in any sequence can be put into an A/B test:
- Variant A (control): current email
- Variant B (challenger): new subject line or body
- Split: 50/50 (default) or custom (e.g. 30/70 for safer rollout)
- Winning condition: open rate / click rate / completed onboarding rate
- Minimum duration: 7 days (default)
- Auto-winner: declared after minimum duration if winner has p < 0.05 statistical significance
- Manual winner: PM can declare winner at any time

A/B test results shown inline in sequence list: Variant A % vs Variant B % with significance indicator.

### Sequence Pause and Resume

Each sequence can be paused (e.g. during platform outage or holiday period). Paused sequences: emails are held and not sent. On resume, decide: send held emails (catch up) or discard held emails (resume from now).

---

## Tab 6 — Audit Log

### Filters
- Date range (default: last 30 days)
- Admin name
- Action type: Workflow Created / Step Added / Step Edited / Step Deleted / Sequence Modified / Stage Overridden / CSM Assigned / CSM Note Added / Email Sent (Manual) / Institution Archived

### Audit Table

| Column | Detail |
|---|---|
| Timestamp | Date and time (IST) |
| Admin | Avatar + name + role |
| Action | Colour-coded badge |
| Target | Workflow name / Institution name / Email sequence name |
| Change | 1-line summary (e.g. "Step 5 'Assign Faculty Roles' moved from Required to Optional") |
| Reason | If Override Stage or Archive: reason entered by admin |

**Pagination:** 25 / 50 / 100. CSV export.

---

## Onboarding Notification Rules

The system sends the following notifications to SRAV internal team:

| Event | Recipient | Channel |
|---|---|---|
| Institution stalled > 3 days | CSM (if assigned) / PM Institution Portal (if unassigned) | In-App |
| Institution stalled > 7 days | PM Institution Portal | In-App + Email |
| New high-value institution signed up (Enterprise plan) | PM Platform + CSM Lead | In-App + Email |
| Institution completed onboarding | PM Institution Portal | In-App |
| A/B test winner declared | PM Institution Portal | In-App |
| Monthly onboarding completion rate drops > 10% from previous month | PM Platform | Email |

---

## Re-onboarding Flow

Institutions that signed up but never completed onboarding (dropped after ≤ 3 steps) and then re-login after > 30 days are flagged for re-onboarding.

**Re-onboarding Detection Rules:**
- Institution last login > 30 days ago
- Onboarding completion < 50%
- At least 1 new admin login detected

**Re-onboarding Workflow (5 steps):**
1. Confirm institution is still active (contact admin)
2. Review what was already set up
3. Identify blocker (why did they stop?)
4. Complete remaining steps with CSM assistance
5. First exam scheduled

**CSM Re-onboarding Queue:**
Sub-section of Institution Queue tab with filter "Re-onboarding" that shows all institutions in the re-onboarding flow separately. Separate completion metrics tracked for re-onboarding vs new onboarding.

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| Kanban pipeline | 8 stages as columns | Visual representation of the onboarding funnel; easier to spot bottlenecks than a list |
| Completion trigger as system condition | Evaluated automatically, not manual checkbox | Removes need for institution to manually mark steps; reduces friction and errors |
| Status classification | On Track / At Risk / Stalled / Overdue | Actionable categories; CSM knows exactly which accounts need attention |
| Email sequence A/B test | Built into sequence management | Onboarding email optimisation is ongoing; A/B enables data-driven improvement |
| CSM notes per institution | Free text, private | Qualitative context from calls — not captured in structured data; essential for high-value accounts |
| Cohort analysis | By signup month | Enables measuring impact of onboarding flow changes over time (before/after comparison) |
| Stage override | Manual override available | Manually-assisted Enterprise onboardings may need manual stage advancement to reflect phone-call-based help |
| Completion trigger custom ORM | Advanced field | Some completion conditions are complex and not covered by dropdown options |
| Re-onboarding flow | Separate from new onboarding | Re-onboarding institutions have different context and need; separate flow and metrics prevent conflation |
| Group workflow | Separate 8-step flow | Group-level onboarding precedes child institution onboarding; different steps and completion criteria |
| Celebration message per step | Shown in institution portal | Positive reinforcement increases step completion rate; small friction reduction at each step |
| Bulk CSM assignment | Multi-select in queue | When new CSMs are assigned, batch reassignment is more efficient than one-by-one |
