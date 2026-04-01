# Page 25 — Defect Tracker

**URL:** `/portal/product/defects/`
**Permission:** `product.manage_defects`
**Priority:** P1
**Roles:** QA Engineer, PM Platform, PM Institution Portal, PM Exam Domains

---

## Purpose

Full-featured defect (bug) tracking system for the SRAV platform. All defects found through automated testing, manual QA, performance testing, production monitoring, or institution-reported issues are tracked here. Provides QA Engineers and PMs with complete visibility into the defect pipeline — from initial report through triage, assignment, fix verification, and closure.

Core responsibilities:
- Log, triage, and prioritise defects from all sources
- Assign defects to engineering teams with SLA tracking
- Track defect lifecycle: Open → Triaged → In Progress → Fixed → Verified → Closed
- Link defects to test cases, releases, and feature flags
- Measure defect density (defects per release), resolution time, and reopened rate
- Escalate P0/P1 defects automatically
- Track institution-reported production bugs separately from internal QA finds
- Provide management-level quality reports

**Scale:**
- Typically 50–150 open defects at any given time
- 15–40 new defects per sprint (2-week sprint)
- P0 defects require acknowledgement within 1 hour and resolution within 24 hours
- P1 defects require resolution within 72 hours
- Institution-reported defects (from production) get higher visibility

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Defect Tracker"              [New Defect]  [Import]  [Export] │
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 8 cards (auto-refresh every 60s)                   │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  All Defects · P0 Critical · My Defects · Release Defects       │
│  Trend Analytics · SLA Tracker · Audit Log                      │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 8 Cards (auto-refresh every 60s)

| # | Label | Value | Colour | Delta | Click Action |
|---|---|---|---|---|---|
| 1 | Open P0 | Open critical defects | Red if > 0 | — | Opens P0 Critical tab |
| 2 | Open P1 | Open high defects | Red if > 5 · Amber if > 2 | — | Filters All Defects to P1 |
| 3 | Open P2 | Open medium defects | Neutral | — | Filters All Defects to P2 |
| 4 | Total Open | All open defects | — | vs last week | Opens All Defects |
| 5 | Assigned to Me | Defects assigned to logged-in user | — | — | Opens My Defects |
| 6 | Fixed Pending Verify | Fixed but not yet verified by QA | Amber if > 5 | — | Filters to "Fixed" status |
| 7 | SLA Breaches | Defects that missed their resolution SLA | Red if > 0 | — | Opens SLA Tracker |
| 8 | Closed This Week | Defects closed in last 7 days | — | vs prev week | — |

---

## Tab 1 — All Defects

### Toolbar

| Control | Options |
|---|---|
| Search | Defect title, ID, description keyword |
| Severity | All / P0 / P1 / P2 / P3 |
| Status | All / Open / Triaged / In Progress / Fixed / Verified / Closed / Deferred / Won't Fix |
| Component | All + full feature area list |
| Environment | All / Development / Staging / UAT / Production |
| Source | All / Automated Test / Manual QA / Performance Test / Institution Reported / Monitoring Alert |
| Release | All + release version dropdown |
| Assignee | Any / Unassigned / Me / Specific engineer |
| Date range | Reported date range |

### Defect Table — 12 columns

| Column | Detail |
|---|---|
| ID | DEF-NNNN (link to detail) |
| Title | Short description (truncated at 60 chars) |
| Severity | P0 (red) · P1 (orange) · P2 (amber) · P3 (grey) badge |
| Status | Colour-coded badge |
| Component | Feature area |
| Environment | Where found |
| Source | Automated / Manual / Performance / Institution / Monitoring |
| Assigned To | Avatar + name or "Unassigned" |
| Reported By | Avatar + name |
| Reported On | Date |
| Days Open | Count (red if >SLA for severity) |
| SLA | ✓ On time · ⚠ At risk · ✗ Breached |

**Row expand:** Shows first 3 steps to reproduce and one screenshot thumbnail (if attached).

**Bulk actions (select multiple):**
- Assign to engineer (dropdown)
- Change severity
- Change status
- Link to release
- Export selected

**Pagination:** Showing X–Y of Z defects · page pills · per-page selector (25 / 50 / 100)

---

## Tab 2 — P0 Critical

Focused view for critical blocking defects only. Auto-refreshes every 30 seconds.

### P0 Defect Rules

| Criterion | Rule |
|---|---|
| Acknowledgement SLA | Within 1 hour of reporting |
| Escalation | If unacknowledged in 1 hour: Slack alert to PM + Engineering Lead |
| Resolution SLA | Within 24 hours |
| Required approvals | Fix requires sign-off from PM Platform + QA Engineer |
| Communication | Status update required every 4 hours until resolved |

### P0 Tab Layout

**Active P0 Defects** (large cards, not table rows)

Each P0 defect gets a full card showing:
- Defect ID and title (large)
- "Time since reported" counter (live, counting up) — red if > 1 hour unacknowledged
- Status: Open / Acknowledged / In Progress / Fixed / Verified
- Assigned to: avatar + name
- Reported by: avatar + name + source
- Resolution SLA countdown: "Resolve by [time] — X hours Y minutes remaining"
- One-line description
- Latest update note
- Action buttons: Acknowledge · Assign · Update Status · Add Note

If no P0 defects open:
- Green banner: "No P0 defects open. All clear."

**Resolved P0 Defects (Last 30 Days)**

Table showing recently resolved P0s:
- Defect ID · Title · Time to Acknowledge · Time to Resolve · Root Cause summary

---

## Tab 3 — My Defects

All defects where the logged-in user is the assignee, reporter, or linked QA verifier.

### Sub-sections:

**Assigned to Me:**
Defects the logged-in engineer or QA is responsible for fixing or verifying.

Table columns: ID · Title · Severity · Status · SLA · Reported On · Days Open · Action (Update Status)

**Reported by Me:**
Defects the logged-in user reported. Allows tracking of reported defects through to closure.

**Pending My Verification:**
Fixed defects where the logged-in QA engineer is the assigned verifier.

For each: ID · Title · Severity · Fixed by · Fix date · Verify by (SLA) · Action (Verify / Reopen)

---

## Tab 4 — Release Defects

Defects grouped by release. Used during release readiness assessment.

### Release Defect Summary Table

| Release | Target Date | P0 Open | P1 Open | P2 Open | Total Open | Total Fixed | QA Gate |
|---|---|---|---|---|---|---|---|
| v4.2.1 | 25 Mar 2026 | 1 | 2 | 8 | 11 | 24 | ✗ Blocked |
| v4.2.0 | 10 Mar 2026 | 0 | 0 | 3 | 3 | 31 | ✓ Passed |
| v4.1.9 | 20 Feb 2026 | 0 | 0 | 1 | 1 | 19 | ✓ Passed |

Clicking a release row → expands to show all defects for that release in a sub-table.

---

## Defect Detail Drawer (720px)

Opened by clicking any defect ID or title.

### Drawer Header

DEF-NNNN · Title · Severity badge · Status badge
"Edit" button · "Assign to Me" button · "Close" button

### Drawer Tab 1 — Details

| Field | Content |
|---|---|
| Title | Editable |
| Description | Full description (markdown rendered) |
| Severity | P0 / P1 / P2 / P3 with dropdown to change |
| Priority | Urgent / High / Normal / Low (separate from severity) |
| Status | Workflow status with transition buttons |
| Component | Feature area (editable) |
| Environment | Where found (editable) |
| Source | How discovered |
| Reported By | Name + role + date |
| Assigned To | Engineer (searchable dropdown) |
| QA Verifier | QA engineer who will verify the fix |
| Linked Test Case | TC-NNNNN (click to open test case repository) |
| Linked Release | Release version (dropdown) |
| Linked Feature Flag | If defect is related to a specific feature flag |
| Regression | Yes / No (if yes: shows which previous release this worked in) |
| Browser / Device | Affected browsers/devices (multi-select: Chrome / Firefox / Safari / Edge / iOS / Android) |
| Reproducibility | Always / Intermittent / Rare / Cannot Reproduce |
| Version Found | App version where defect was discovered |
| Version Fixed | App version where fix was deployed (filled when fixed) |

### Drawer Tab 2 — Reproduction

**Steps to Reproduce:**
Numbered list of exact steps. Each step is a separate row.

| Step | Action | Expected | Actual |
|---|---|---|---|
| 1 | Login as student test_student_01 | Dashboard loads | Dashboard loads |
| 2 | Click "Start Exam" on SSC CGL Mock 1 | Exam start page loads | Exam start page loads |
| 3 | Answer 100 questions, click Submit | Confirmation dialog appears | Confirmation dialog appears |
| 4 | Click "Confirm Submit" | Result page loads showing score | Page shows error 500: Internal Server Error |

**Environment Details:**
- OS: Windows 11 / macOS / iOS 17 / Android 14
- Browser: Chrome 122 / Firefox 123
- Screen resolution: 1920×1080
- Network: WiFi / 4G / 3G
- Server: Staging environment, region: ap-south-1

**Expected Result:**
"Result page loads showing score, rank, and exam analysis within 2 seconds."

**Actual Result:**
"HTTP 500 error. Server logs show: ValueError in result_calculation.py line 234. Division by zero when total_marks = 0 for empty exam pattern."

### Drawer Tab 3 — Attachments

List of all attached files:
- Screenshots (image thumbnails with expand to full screen)
- Screen recordings (video player inline)
- Log files (download button + inline preview for first 50 lines)
- HAR files (browser network log)
- Database query explain output

"Add Attachment" button: drag-and-drop or file picker.

### Drawer Tab 4 — Activity Timeline

Full chronological feed of all activity on this defect:

- DEF-0482 reported by Deepa Menon (20 Mar 2026, 10:24 AM)
- Severity set to P1 by Deepa Menon (20 Mar 2026, 10:24 AM)
- Assigned to Arjun Kumar (Engineering Lead) by PM Platform (20 Mar 2026, 11:05 AM)
- Status changed to "In Progress" by Arjun Kumar (20 Mar 2026, 2:30 PM)
- Comment by Arjun Kumar: "Root cause identified. Division by zero in result_calculation when exam_pattern.total_marks is null. Fix in PR #489."
- Status changed to "Fixed" by Arjun Kumar (21 Mar 2026, 9:15 AM). Fix version: v4.2.1-rc2
- Assigned to Deepa Menon (QA Verifier) (21 Mar 2026, 9:15 AM)
- Comment by Deepa Menon: "Verified on staging. Result page loads correctly in 1.4s. Closing."
- Status changed to "Verified" then "Closed" by Deepa Menon (21 Mar 2026, 3:40 PM)

**Add Comment:** Text area with markdown support. @mention teammates. "Save Comment" button.

### Drawer Tab 5 — Related

- Related defects (same component, same release, or marked as duplicate)
- Linked user story
- Linked roadmap feature
- Linked test cases (those that caught this defect)
- Duplicate of: (link to the original if this defect is a duplicate)

### Status Transition Buttons (in drawer footer)

Contextual based on current status:
| Current Status | Available Transitions |
|---|---|
| Open | → Triaged, → Deferred, → Won't Fix |
| Triaged | → In Progress, → Deferred, → Won't Fix |
| In Progress | → Fixed (requires fix version + PR link) |
| Fixed | → Verified (QA verifier only), → Reopened |
| Verified | → Closed |
| Closed | → Reopened |

---

## New Defect Modal (multi-step)

**Step 1 — Basic Info:**
- Title (required, max 120 chars)
- Severity: P0 / P1 / P2 / P3
- Component (feature area tree selector)
- Environment: Dev / Staging / UAT / Production
- Source: Automated Test / Manual QA / Performance Test / Institution Reported / Monitoring Alert

**Step 2 — Reproduction:**
- Description (markdown, required)
- Steps to reproduce (step-by-step form, minimum 2 steps)
- Expected result (required)
- Actual result (required)
- Reproducibility: Always / Intermittent / Rare
- Browser/Device (multi-select)

**Step 3 — Links:**
- Linked Test Case (optional, TC-NNNNN search)
- Linked Release (optional)
- Linked Feature Flag (optional)

**Step 4 — Attachments:**
- Drag-and-drop or file picker
- Screenshots, recordings, logs

**Submit:** Defect created as "Open". If P0: immediate Slack alert sent to engineering channel and PM.

---

## Tab 5 — Trend Analytics

### Defect Density Chart

Line chart: defects found per release over last 12 releases. Defect density = new defects found / story points delivered. Should be trending down as code quality improves.

### Open Defect Trend

Area chart: total open defects per day over last 90 days. Stacked by severity (P0/P1/P2/P3). If total is growing, quality is declining.

### Resolution Time Distribution

Histogram: how long defects took from "Open" to "Closed" (in days). Separate for each severity level. Compare against SLA targets.

| Severity | SLA Target | Actual Median | Actual P90 |
|---|---|---|---|
| P0 | 24 hours | 16 hours | 28 hours |
| P1 | 72 hours | 52 hours | 96 hours |
| P2 | 14 days | 8 days | 21 days |
| P3 | 30 days | 15 days | 40 days |

### Top Defect-Prone Components

Bar chart: component name vs defect count (last 3 months). Sorted descending. Identifies which parts of the codebase need most attention.

### Reopened Rate

Donut chart: % of defects that were reopened after closing. High reopened rate indicates insufficient fix verification or root cause not addressed.

### Engineering Team Defect Metrics

Table showing per-engineer stats (for engineering team visibility, not blame):
| Engineer | Assigned | Fixed | Avg Resolution Time | Reopened |
|---|---|---|---|---|
| Arjun Kumar | 24 | 22 | 2.1 days | 2 |
| Meera Patel | 18 | 17 | 1.8 days | 1 |

---

## Tab 6 — SLA Tracker

### SLA Definitions

| Severity | Acknowledgement | Resolution | Escalation Rule |
|---|---|---|---|
| P0 Critical | 1 hour | 24 hours | Alert PM + Eng Lead if unacknowledged after 1h |
| P1 High | 4 hours | 72 hours | Alert PM if unresolved after 48h |
| P2 Medium | 24 hours | 14 days | Reminder at 10 days |
| P3 Low | 72 hours | 30 days | Reminder at 25 days |

### SLA Compliance Table

| Defect ID | Title | Severity | Reported | SLA Deadline | Status | Time Remaining | SLA Status |
|---|---|---|---|---|---|---|---|
| DEF-0482 | Result page timeout | P1 | 20 Mar | 23 Mar | In Progress | 28h remaining | ✓ On Time |
| DEF-0479 | Leaderboard not loading | P1 | 18 Mar | 21 Mar | Fixed | — | ✓ Met |
| DEF-0471 | CSV import fails for 10K+ rows | P2 | 10 Mar | 24 Mar | Open | 4d remaining | ⚠ At Risk |
| DEF-0468 | Mobile app crash on iOS 17.4 | P1 | 16 Mar | 19 Mar | Open | BREACHED | ✗ Breached |

### SLA Breach History (last 90 days)

Table: Defect ID · Severity · Breach type (acknowledgement / resolution) · Breach duration · Root cause (why SLA was missed) · Actions taken.

---

## Tab 7 — Audit Log

Every change to every defect — immutable.

| Timestamp | User | Action | Defect | Field Changed | Before | After |
|---|---|---|---|---|---|---|
| 20 Mar 14:30 | Deepa Menon | Status change | DEF-0482 | status | Open | In Progress |
| 20 Mar 11:05 | Rahul Nair | Assignment | DEF-0482 | assigned_to | Unassigned | Arjun Kumar |
| 20 Mar 10:24 | Deepa Menon | Defect created | DEF-0482 | — | — | — |

Filters: Date range · User · Defect ID · Action type. CSV export.

---

## Import Defects

Defects can be imported in bulk from external sources.

**Import Sources:**
- CSV file (template downloadable from Import modal)
- JIRA export (XML format)
- Automated test runner output (JUnit XML format)
- Monitoring alerts export (JSON)

**CSV Import Template Columns:**
Title · Severity · Component · Environment · Source · Reported By · Steps (semicolon-separated) · Expected Result · Actual Result · Browser · Reproducibility · Linked Release

**Import Process:**
1. Upload file
2. Preview first 5 rows with column mapping
3. Validate: shows errors (missing required fields, invalid severity values)
4. Confirm import — creates all defects in "Open" status
5. Import summary: X created · Y skipped (duplicate title check) · Z errors

---

## Export Defects

"Export" button opens Export Defects modal:

**Options:**
- Format: CSV / Excel / PDF Report
- Filter: current filter (as shown in table) / all open / all / custom date range
- Include: description / steps to reproduce / attachments (PDF only) / activity log (PDF only)
- Group by: Severity / Component / Release / Assignee (for report format)

**PDF Defect Report:**
Management-level quality report format:
- Summary page: total open/closed by severity, SLA compliance %, defect density trend
- Per-severity section: list of all open defects with status
- Resolution time analysis
- Top 5 defect-prone components

PDF generation is async (Celery). Notification sent when ready.

---

## Notification and Escalation Rules

| Event | Recipients | Channel | Timing |
|---|---|---|---|
| P0 defect opened | PM Platform + Engineering Lead + QA Lead | Slack + Email | Immediately |
| P0 unacknowledged for 1h | PM Platform + Engineering Director | Email + Slack | 1h after open |
| P1 defect opened | Assigned engineer + PM | In-App + Email | Immediately |
| P1 unresolved at 48h | PM Platform | In-App + Email | At 48h mark |
| Defect assigned | Assigned engineer | In-App + Email | Immediately |
| Defect status changed to Fixed | QA Verifier | In-App + Email | Immediately |
| Defect reopened | Assignee + Reporter | In-App + Email | Immediately |
| SLA at risk (< 20% time remaining) | Assignee + PM | In-App | At threshold |
| SLA breached | PM Platform + Engineering Lead | Email | At breach |
| New institution-reported defect | PM Institution Portal | In-App + Email | Immediately |

All P0/P1 notifications bypass quiet hours (sent at any time).

---

## Institution-Reported Defects Workflow

Defects sourced from institution support tickets (Source = "Institution Reported") follow a special workflow with additional visibility:

**Additional Fields for Institution-Reported Defects:**
- Institution name (linked to institution profile)
- Institution tier (Enterprise / Professional / Standard / Starter)
- Support ticket ID (from external helpdesk system)
- Reported by (institution admin name)
- Number of affected students (if known)
- Business impact: Critical (exam affected) / High (ongoing disruption) / Medium (workaround available) / Low

**Priority Boost Rule:**
If an institution-reported defect affects an active exam session (exam currently in progress), the defect automatically receives a P0 severity and triggers the P0 escalation workflow, regardless of how it was initially classified.

**Communication Back to Institution:**
- "Acknowledge to Institution" button: sends a template email to the reporting institution admin confirming receipt
- "Update Institution" button: sends status update email using "Defect Status Update" email template
- "Resolution Email" button: sends resolution confirmation email when defect is closed

---

## Defect Triage Process

When a defect is in "Open" status, the QA Lead or PM conducts triage to assign severity and priority.

**Triage Criteria:**

| Criterion | P0 Criteria | P1 Criteria | P2 Criteria | P3 Criteria |
|---|---|---|---|---|
| Users affected | Platform-wide / All students | Large segment / all students of institution | Specific feature subset | Cosmetic / edge case |
| Business impact | Cannot take exam / results lost | Core feature broken / workaround possible | Feature degraded | Minor inconvenience |
| Data integrity | Data loss or corruption | Incorrect data displayed | Incorrect format | No data impact |
| Security | Auth bypass / data exposure | Privilege escalation | Minor security concern | No security impact |
| Frequency | Always | Often | Sometimes | Rarely |

**Triage Modal:**
Opened from "Triage" button in defect drawer.
- Current severity (editable)
- Assign to engineer (required)
- Assign QA Verifier (required)
- Link to release (required for P0/P1)
- Triage notes (optional)
- "Confirm Triage" → moves defect to "Triaged" status

---

## Performance Defects (from Performance Testing)

Defects with Source = "Performance Test" have additional performance-specific fields in the Details tab:

- Transaction: API endpoint or user action that is slow
- Baseline response time: what it was before regression
- Current response time: what performance test measured
- SLA threshold: from SLA Tracker (page 24)
- Load level: concurrent users at time of measurement
- Infrastructure metrics at time of test: CPU %, memory %, DB query time

Performance defects are automatically linked to the relevant performance test run (page 24).

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| P0 full-card view | Not table rows | P0 defects need more visual prominence; card shows live countdown and all context at a glance |
| Live countdown on P0 | Counting up since reported | Creates urgency without requiring team to calculate elapsed time manually |
| Separate QA Verifier field | Different from Assignee | The person who fixes is not the person who verifies — separation of duties required for quality |
| SLA per severity | Different targets by severity | P0 and P3 have fundamentally different urgency; same SLA for all severities is inappropriate |
| Reopened rate tracking | Separate metric | High reopened rate indicates fix quality issues — different problem than slow resolution |
| Institution-reported source | Separate source type | Production bugs from paying customers are higher visibility and directly affect retention/churn |
| Fix requires PR link | Enforced on status transition to Fixed | Creates traceability from defect to code change; cannot mark fixed without a code change reference |
| Defect density per release | Key quality metric | Shows if code quality is improving over time relative to feature work delivered |
| Priority boost for active exam | Automatic P0 elevation | An institution-reported defect during an active exam is by definition a P0 — should not require manual reclassification |
| Triage modal | Structured process | Ad-hoc triage leads to inconsistent severity assignment; modal enforces triage criteria application |
| Institution communication buttons | Template-driven emails | Consistent, professional communication to institution admins; reduces ad-hoc Slack messages |
| Performance defect additional fields | Baseline + current + SLA | Performance regression without baseline comparison is meaningless; need all three for actionable defect |

