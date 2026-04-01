# C-18 — Engineering Incident Manager

## Page Metadata

| Field | Value |
|---|---|
| Page Name | Engineering Incident Manager |
| Route | `/platform/incidents` |
| File | `c-18-incidents.md` |
| Division | Division C — Engineering & Infrastructure |
| Priority | P0 — Mission Critical |
| Status | ⬜ Amendment pending — G10 (Alert Rules tab) · G21 (Runbook Editor tab) |
| HTMX Parts | `?part=board`, `?part=active`, `?part=timeline`, `?part=runbooks`, `?part=oncall`, `?part=postmortems`, `?part=analytics`, `?part=integrations` |
| Poll Interval | `every 15s[!document.querySelector('.drawer-open,.modal-open')]` (10s during P0 active exam incident) |
| Roles Allowed | Platform Admin (full) · DevOps Engineer (full) · Security Engineer (security incidents only) |

---

## Purpose

The Engineering Incident Manager is the operational command centre for all platform incidents across the SaaS infrastructure serving 2,050 institutions and up to 7.6M students. It provides the full incident lifecycle from automated detection through acknowledgement, mitigation, resolution, and postmortem — in a single interface. It integrates with PagerDuty and OpsGenie for alerting and on-call orchestration, links to the War Room page (Div A — Page 32) for exam-day P0 coordination, and feeds MTTR analytics into the DORA metrics dashboard (C-09).

Any P0 incident during an active exam window triggers an elevated response mode: the poll interval drops from 15s to 10s, a red banner appears on all Division C pages visible to the on-call engineer, and the War Room link becomes prominent. This page is the single source of truth for incident state across the entire engineering organisation.

---

## User Roles

| Role | Access |
|---|---|
| Platform Admin | Full read and write access to all incidents, runbooks, on-call schedule, postmortems, and integrations |
| DevOps Engineer | Full read and write access to all incidents, runbooks, on-call schedule, postmortems, and integrations |
| Security Engineer | Read and write access to security-classified incidents (P0/P1/P2 with tag `security`); read-only for all others |
| All Other Roles | No access |

---

## Section-Wise Detailed Breakdown

---

### Section 1 — Page Header and Global Status Bar

**Purpose:**
Provides at-a-glance incident health for the entire platform. The header communicates current severity state to the on-call engineer the moment the page loads.

**User Interaction:**
- Status bar spans the full page width above all tabs
- During a P0 incident the bar turns red with pulsing indicator and displays the incident title, time since detection, current responder, and a direct link to the active incident timeline
- During a P1 incident the bar turns amber
- During no active incidents the bar shows green with "All Systems Operational" and the time of last check
- "War Room" button always visible top-right — links to Div A Page 32; during active P0 exam incidents it pulses red

**UI Components:**
- Full-width status banner (green · amber · red states)
- Pulsing severity dot (animated only during active P0/P1)
- Active incident quick-link (title + elapsed time)
- Current on-call engineer badge (name + avatar + phone icon)
- "War Room →" button (always visible, pulses red during exam-day P0)
- "Declare Incident" button (primary CTA — opens incident declaration modal)

**Data Flow:**
- Status bar loaded via `?part=board` on page load; polled every 15s (10s during P0)
- On-call badge pulls from OpsGenie current schedule API (cached 60s in Memcached)
- Active incident quick-link fetches `platform_incidents` where `status IN ('open','acknowledged','mitigating')` ordered by severity then detected_at
- War Room link is static; pulse animation driven by presence of P0 record with `exam_day = true` flag

**Role-Based Behavior:**
- Platform Admin and DevOps: see "Declare Incident" button
- Security Engineer: "Declare Incident" button only visible when declaring security-classified incident (dropdown pre-selects `tag=security`)

**Edge Cases:**
- Multiple simultaneous P0 incidents: banner shows highest severity and count ("2 active P0 incidents"); clicking opens filtered board
- If OpsGenie API times out after 3s: on-call badge shows "On-Call Unknown — check OpsGenie" in amber
- P0 detected during active exam: poll interval switches from 15s to 10s automatically without page refresh (HTMX swap triggers a meta re-poll directive)

**Performance:**
- Status bar part renders < 100ms (single indexed query on `platform_incidents` by status)
- OpsGenie call is non-blocking; badge renders from cache first, then live data when available

**Mobile:**
- Status banner stacks vertically; "War Room" and "Declare Incident" buttons move to bottom action bar
- Pulsing animation preserved on mobile

**Accessibility:**
- Status bar uses `role="alert"` and `aria-live="polite"` (P1) or `aria-live="assertive"` (P0)
- Colour not the sole indicator — text severity labels always present
- "Declare Incident" has `aria-keyshortcuts="Alt+D"` registered

---

### Section 2 — Incident Board (Active Incidents)

**Purpose:**
The primary working view. Shows all open, acknowledged, and mitigating incidents in a Kanban-style board grouped by severity (P0 → P1 → P2). Each card is actionable — the on-call engineer can acknowledge, escalate, update, or resolve without navigating away.

**User Interaction:**
- Board displays four columns: P0 · P1 · P2 · Resolved (last 24h, collapsed by default)
- Each incident card shows: severity badge · title · affected service(s) · detection time · time since detection (live-counting) · current assignee · status pill (Open · Acknowledged · Mitigating · Resolved)
- Click card → opens incident detail drawer (see Section 3)
- "Acknowledge" button on card (available when status = Open) — one-click, records timestamp and current user
- "Escalate" button — moves incident up one severity tier (P2→P1→P0) with mandatory reason field
- Severity filter tabs at top of board (All · P0 · P1 · P2)
- "My Incidents" toggle — filters to incidents assigned to the logged-in user
- Unacknowledged P0 cards pulse amber border every 3s until acknowledged

**UI Components:**
- Kanban board layout with severity columns
- Incident card (severity badge · title · service tags · time counters · assignee avatar · status pill · quick-action buttons)
- Live countdown timers (time since detection, time since last update)
- P0 card pulse animation (3s loop, stops on acknowledge)
- Severity filter tab bar
- "My Incidents" toggle
- "Declare Incident" FAB (floating action button on mobile)
- Empty state per column: "No active P0 incidents" with checkmark icon

**Data Flow:**
- Board loaded via `?part=active`; polled every 15s
- Query: `SELECT * FROM platform_incidents WHERE status != 'resolved' OR (status = 'resolved' AND resolved_at > NOW() - INTERVAL '24 hours') ORDER BY severity ASC, detected_at ASC`
- Acknowledge action: `PATCH /platform/api/incidents/{id}/acknowledge` — updates `status`, `acknowledged_by`, `acknowledged_at`; triggers PagerDuty acknowledge API call
- Escalate action: opens inline form; on submit updates `severity`, appends entry to `platform_incident_timeline`
- All mutations append to `platform_audit_log`

**Role-Based Behavior:**
- Security Engineer: sees only incidents tagged `security`; other cards greyed with "Restricted" overlay
- All allowed roles: can acknowledge and update any visible incident
- Escalation to P0 requires DevOps Engineer or Platform Admin role

**Edge Cases:**
- Zero active incidents: board shows all-green empty states across all columns
- 10+ P0 incidents simultaneously (e.g., cascading AWS regional outage): cards scroll within column; column header shows count badge; "Mass Acknowledge All P0" emergency button appears (requires 2FA)
- Incident auto-created by C-04 alert rule or C-07 crash threshold: card appears on board within the next poll cycle (max 15s lag)
- An incident's service is deleted before the incident is resolved: service tag shows "Decommissioned" in grey

**Performance:**
- Board renders in < 200ms (indexed on `status`, `severity`, `detected_at`)
- Live countdown timers are client-side JS — no server poll needed for second-by-second updates
- HTMX swap replaces only changed cards (morph strategy) to prevent flicker

**Mobile:**
- Kanban columns stack vertically (P0 first)
- Cards are full-width with expandable details
- Quick-action buttons ("Acknowledge", "Escalate") visible without opening drawer

**Accessibility:**
- Each card has `role="article"` with `aria-label="P0 incident: [title], open for [duration]"`
- Live countdown regions use `aria-live="off"` (too noisy if live) — screen reader reads on card focus
- Pulsing animation respects `prefers-reduced-motion`

---

### Section 3 — Incident Detail Drawer

**Purpose:**
Full incident workspace. The on-call engineer manages the entire incident lifecycle — timeline updates, responder assignment, communication, runbook linkage, and resolution — from this single drawer without leaving the board.

**User Interaction:**
- Opens from any incident card click; slides in from right (80% viewport width on desktop)
- Five tabs: Overview · Timeline · Responders · Runbook · Communications
- **Overview tab**: incident metadata (title, severity, status, affected services, affected tenants count, detection source, detection time, acknowledgement time, mitigation time, resolution time), SLA breach indicator (P0: acknowledge < 5 min · mitigate < 30 min · resolve < 4h; P1: acknowledge < 15 min · mitigate < 2h · resolve < 8h)
- **Timeline tab**: chronological event log (detection → ack → updates → mitigation → resolution); each entry shows timestamp, actor, action type, and free-text note; "Add Update" button appends new entry; entries immutable once saved
- **Responders tab**: current assignee + incident commander (P0 only) + stakeholder list; "Reassign" (self-assign or assign to another staff member); "Page Additional Responder" button (fires PagerDuty alert to named engineer)
- **Runbook tab**: search runbooks from library; attach one or more runbooks; mark runbook steps as complete (checklist within drawer); "Open Runbook in Full Page" link
- **Communications tab**: auto-generated status update template (pre-filled from incident data); send to: Slack channel selector · email list · internal status page toggle; message preview before send; history of sent communications with timestamp and recipient count
- "Resolve Incident" button at drawer bottom (red) — opens resolution modal with mandatory resolution summary and root cause classification
- "Escalate to War Room" button (P0 only) — opens War Room in new tab pre-populated with incident ID

**UI Components:**
- Slide-in drawer (80% desktop, full-width mobile)
- Tab bar: Overview · Timeline · Responders · Runbook · Communications
- SLA timer panel (green → amber → red based on thresholds)
- Timeline event list (immutable log with timestamps)
- "Add Update" inline form (text + action type selector)
- Responder cards (avatar · name · role · contact icon)
- Runbook search and checklist
- Communication composer with channel selector and preview
- "Resolve Incident" red button with confirmation modal
- "Escalate to War Room" button (P0 only, amber)

**Data Flow:**
- Drawer content loaded via `GET /platform/api/incidents/{id}?full=true`
- Timeline tab: `platform_incident_timeline` WHERE `incident_id = {id}` ORDER BY `event_at ASC`
- "Add Update" → `POST /platform/api/incidents/{id}/timeline` — appends immutable record
- Responder reassign → `PATCH /platform/api/incidents/{id}/responders`; triggers PagerDuty reassignment
- Communication send → Lambda function invokes SES (email) + Slack webhook + status page API simultaneously
- "Resolve Incident" → 2FA gate → `PATCH /platform/api/incidents/{id}` sets `status = resolved`, `resolved_at`, `resolution_summary`, `root_cause_category`; triggers PagerDuty resolve

**Role-Based Behavior:**
- Security Engineer: can view and update security incidents; "Resolve" requires Platform Admin co-approval for P0 security incidents (approval request sent via PagerDuty)
- DevOps/Platform Admin: full access; can resolve unilaterally for non-security P0

**Edge Cases:**
- Drawer closed while P0 is active: poll banner continues to show above board; closing drawer does not mean incident is resolved
- "Add Update" submitted with empty note: blocked with inline validation
- Communication send fails (SES/Slack error): error shown in Communications tab; message queued for retry (Celery); status shown as "Pending — retrying"
- Resolution attempted without root cause classification: blocked; classification is mandatory

**Performance:**
- Drawer loads within 300ms (parallel fetch: incident metadata + timeline)
- Timeline entries paginated (50 per load, older entries loaded on scroll-up)
- Communication history loads lazily on tab switch

**Mobile:**
- Drawer occupies full screen on mobile
- Tabs convert to horizontal scrollable tab strip
- SLA timers pinned at top; timeline scrolls within remaining viewport

**Accessibility:**
- Drawer has `role="dialog"` and `aria-modal="true"`
- Focus trapped within drawer while open
- Each timeline entry has `role="listitem"` with timestamp in `<time>` tag
- "Resolve Incident" button has `aria-describedby` pointing to SLA status

---

### Section 4 — Incident Timeline View (Full-Page)

**Purpose:**
Provides a full-page chronological reconstruction of a specific incident — from the first automated signal through every responder action to final resolution. Designed for real-time use during active incidents and post-incident review.

**User Interaction:**
- Accessible via "View Full Timeline" link in the incident drawer or direct URL `/platform/incidents/{id}/timeline`
- Vertical timeline chart with swimlanes by actor type (System · On-Call Engineer · Platform Admin · External — PagerDuty/OpsGenie)
- Four phases visually marked with colour bands: Detection (grey) · Acknowledgement (amber) · Mitigation (blue) · Resolution (green)
- Each event node: timestamp · actor · event type · note (expandable)
- Phase duration labels between phase boundaries (e.g., "Detection → Ack: 3m 42s")
- SLA breach markers on timeline if any phase exceeded threshold
- "Add Note to Timeline" button (only if incident still active)
- Export button: download timeline as PDF (for postmortem or audit)

**UI Components:**
- Vertical swimlane timeline chart
- Phase boundary markers with duration labels
- SLA breach red markers
- Event nodes (expandable detail on click)
- "Add Note" button (active incidents only)
- "Export PDF" button
- Legend (actor type colour coding)

**Data Flow:**
- Loads `platform_incident_timeline` for the given incident ID, ordered by `event_at ASC`
- Phase boundaries calculated from `platform_incidents` fields: `detected_at`, `acknowledged_at`, `mitigated_at`, `resolved_at`
- SLA thresholds fetched from `platform_incident_sla_config` (keyed by severity)
- PDF export: server-side Lambda renders timeline to PDF via headless rendering; returned as signed S3 download URL valid 15 minutes

**Role-Based Behavior:**
- All allowed roles: can view timeline for accessible incidents
- "Add Note" only available if user is an assigned responder or Platform Admin

**Edge Cases:**
- Incident with no acknowledgement yet: "Acknowledgement" phase shows as pending with live elapsed timer
- Events added out of order (e.g., automated system event timestamped before manual entry): sorted strictly by `event_at`, not by insertion order
- PDF export during active incident: includes watermark "LIVE — GENERATED AT {timestamp} — INCIDENT NOT YET RESOLVED"

**Performance:**
- Timeline renders in < 300ms for incidents with up to 500 timeline events
- For incidents with > 500 events (major outages): events grouped by 5-minute windows with expand option

**Mobile:**
- Swimlane collapses to single vertical stream (actor shown as tag on each node)
- Phase bands preserved as colour strips on left rail

**Accessibility:**
- Timeline uses `role="list"` with each event as `role="listitem"`
- Phase boundaries announced via hidden `aria-label` text
- PDF export button has `aria-label="Export incident timeline as PDF"`

---

### Section 5 — Runbook Library

**Purpose:**
A searchable repository of 30+ known incident types with step-by-step mitigation procedures. Runbooks are the operational memory of the engineering team — ensuring consistent, fast response regardless of which engineer is on-call.

**User Interaction:**
- Tab or sub-route: `/platform/incidents/runbooks`
- Left sidebar: category tree (Infrastructure · Database · Security · AI Pipeline · Mobile · Exam Platform · Integrations · General)
- Main panel: runbook list with search (title + tag search)
- Each runbook card: title · category · last updated · author · estimated resolution time · times used in incidents
- Click runbook card → opens runbook detail view (full-page or modal)
- Runbook detail: title · severity applicability (P0/P1/P2) · affected services · step-by-step checklist (ordered numbered list) · escalation path · rollback steps · related runbooks · linked incidents where this runbook was used
- "Edit Runbook" button (DevOps/Platform Admin only) — opens WYSIWYG editor with step reordering, step add/delete, version history
- "New Runbook" button — opens creation modal (title · category · severity · steps)
- Version history panel for each runbook: list of saved versions with diff view between versions
- "Test Runbook" tag — marks runbook as reviewed via simulation (quarterly review date shown)

**UI Components:**
- Category tree sidebar
- Search input with tag filter chips
- Runbook card grid
- Runbook detail view (checklist, escalation path, related runbooks)
- WYSIWYG step editor with drag-to-reorder
- Version history list with diff viewer
- "New Runbook" modal
- "Test Runbook" status badge

**Data Flow:**
- Runbook list: `SELECT * FROM platform_runbooks WHERE archived = false ORDER BY category, title`
- Search: full-text search on `title` + `tags` + `step_content` (PostgreSQL `tsvector` index on `platform_runbooks`)
- Runbook versions: `platform_runbook_versions` with `runbook_id`, `version`, `content_json`, `saved_by`, `saved_at`
- "Times used" count: `SELECT COUNT(*) FROM platform_incident_runbooks WHERE runbook_id = {id}`
- Edit save: inserts new version record; `platform_runbooks.current_version` incremented; old version immutable

**Role-Based Behavior:**
- All allowed roles: full read access to all runbooks
- DevOps Engineer / Platform Admin: can create, edit, archive runbooks
- Security Engineer: can edit runbooks in the Security category only

**Edge Cases:**
- Runbook referenced in an active incident is edited mid-incident: incident drawer shows "Runbook updated during incident — version pinned to v{N} at incident start time" to prevent confusion
- Search returns zero results: shows "No runbooks match — create one?" with "New Runbook" CTA
- Runbook with no steps: creation is blocked; minimum 3 steps required

**Performance:**
- Runbook list renders in < 150ms (small dataset, cached 5 minutes in Memcached)
- Full-text search returns results in < 300ms (tsvector GIN index)
- Version diff computed server-side; cached per version pair

**Mobile:**
- Category tree collapses to dropdown selector
- Runbook cards stack vertically
- Checklist in detail view is touch-friendly with large tap targets for step completion

**Accessibility:**
- Checklist steps use `<ol>` with `role="list"` and each step as `<li role="listitem">`
- Completed steps announced via `aria-checked` on checkbox equivalent
- WYSIWYG editor meets WCAG 2.1 AA for keyboard navigation

---

### Section 6 — On-Call Schedule

**Purpose:**
Displays the current and upcoming on-call rotations for all engineering roles. Ensures the incident response team always knows who is responsible and provides an interface for schedule overrides during planned events.

**User Interaction:**
- Tab: `/platform/incidents/oncall`
- Calendar view: 2-week forward-looking schedule (current week + next week)
- Rows: one per on-call role (Primary On-Call · Secondary On-Call · Incident Commander · Database On-Call · Security On-Call)
- Each cell: engineer name + avatar; current shift highlighted in blue
- "Today" button returns to current week
- "Request Override" button — allows an engineer to hand off their shift to a colleague (subject to Platform Admin approval)
- Override request form: date range · reason · replacement engineer (dropdown of eligible staff) · note
- Pending overrides shown with amber indicator on affected cells
- "My Schedule" toggle — highlights only the logged-in user's shifts
- On-call history tab: past 90 days of who was on-call (for postmortem attribution)

**UI Components:**
- 2-week calendar grid (rows = roles, columns = days)
- Current shift highlight (blue cell border + bold name)
- "Today" navigation button
- "Request Override" button + slide-in form
- Pending override amber indicator
- "My Schedule" toggle
- On-call history list (past 90 days)
- Sync indicator: "Synced from OpsGenie — last updated {time}"

**Data Flow:**
- Schedule sourced from OpsGenie Schedule API, cached in Memcached (TTL 5 minutes)
- Cache key deleted (cache.delete) via OpsGenie webhook on any schedule change (manual or automatic rotation)
- Override request: `POST /platform/api/oncall/override-requests` → Platform Admin notified via PagerDuty + email → on approval, override pushed to OpsGenie API
- On-call history: `platform_oncall_history` table updated nightly from OpsGenie API

**Role-Based Behavior:**
- All allowed roles: view schedule and request overrides for their own shifts
- Platform Admin: approve/deny override requests; can directly edit schedule (opens OpsGenie deep link)

**Edge Cases:**
- OpsGenie API unavailable: schedule loads from Memcached cache with "Showing cached schedule — last synced {time}" warning; "Request Override" form disabled with explanation
- Override requested during active P0 incident: blocked with warning "You are currently the active on-call for a P0 incident. Override requests cannot be submitted during active incidents."
- All on-call slots unfilled for a future date (scheduling gap): that cell shows "UNCOVERED" in red; Platform Admin receives daily digest alert

**Performance:**
- Schedule renders in < 200ms from Memcached cache
- OpsGenie API call is async background refresh; never blocks page render

**Mobile:**
- Calendar switches to 3-day rolling view on mobile (< 768px)
- Role rows collapse to tabs (Primary · Secondary · IC · DB · Security)
- Swipe left/right to advance days

**Accessibility:**
- Calendar cells use `role="gridcell"` within `role="grid"`
- Current shift cell has `aria-current="true"`
- On-call names readable by screen reader (no avatar-only display)

---

### Section 7 — PagerDuty and OpsGenie Integration Panel

**Purpose:**
Manages the bidirectional integration between the incident manager and external alerting platforms. Allows the engineering team to configure routing rules, escalation policies, and webhook endpoints without leaving the platform.

**User Interaction:**
- Tab: `/platform/incidents/integrations`
- Two sub-panels: PagerDuty · OpsGenie (tab switcher)
- **PagerDuty panel**: connected services list (which C-04 alert rules route to which PagerDuty service); escalation policy viewer (read-only, opens PagerDuty deep link for editing); webhook event log (last 100 events received from PagerDuty with payload preview); connection health indicator (green/red based on last successful event)
- **OpsGenie panel**: schedule sync status (last synced, next sync); team list with on-call rotation config (read-only); alert routing rules; connection health indicator
- "Test Integration" button for each platform: fires a test event and verifies round-trip receipt (confirmation shown in webhook log within 30s)
- "Reconnect" button: re-authorises OAuth token or API key for either platform (opens credential update modal — new key stored in Secrets Manager, never displayed)

**UI Components:**
- Platform sub-tab switcher (PagerDuty · OpsGenie)
- Connected service list table (alert rule → PagerDuty service mapping)
- Escalation policy viewer (read-only tree)
- Webhook event log (last 100 events, expandable payload)
- Connection health badge (green · red with last-event timestamp)
- "Test Integration" button + result toast
- "Reconnect" modal (API key entry, never redisplayed after save)

**Data Flow:**
- Connection health: checks `platform_integration_health` table (updated by PagerDuty/OpsGenie webhook receipt heartbeat every 60s)
- Webhook event log: `platform_webhook_events` where `source IN ('pagerduty', 'opsgenie')` ORDER BY `received_at DESC` LIMIT 100
- "Test Integration" → Lambda invokes PagerDuty test event API → waits for webhook receipt → updates log
- API key update → Lambda writes new key to Secrets Manager under predefined ARN → updates `platform_integration_config` with new ARN reference (key itself never stored in platform DB)

**Role-Based Behavior:**
- Platform Admin: full access including "Reconnect" (API key update)
- DevOps Engineer: view + "Test Integration"; cannot update API keys
- Security Engineer: read-only view

**Edge Cases:**
- PagerDuty webhook not received within 30s of test: "Test failed — webhook not received. Check PagerDuty service URL configuration." with link to integration settings
- OpsGenie sync returns 401 (expired API key): connection health turns red; "Reconnect" button pulses amber; daily alert to Platform Admin
- Duplicate webhook events received (PagerDuty retry): de-duplicated by `event_dedup_key` before inserting to `platform_webhook_events`

**Performance:**
- Integration panel loads in < 300ms (webhook log is paginated; only first 10 rows loaded initially)
- "Test Integration" is async; result shown via HTMX SSE event (no page block)

**Mobile:**
- Platform tabs stack to dropdown on mobile
- Webhook event log shows condensed view (timestamp + event type only; expand on tap)

**Accessibility:**
- Connection health badge has `aria-label="PagerDuty connection: healthy, last event 2 minutes ago"`
- Webhook event log is keyboard-navigable table

---

### Section 8 — Postmortem Tracker

**Purpose:**
Ensures every resolved P0 and P1 incident produces a structured postmortem with root cause analysis, contributing factors, action items, and owner assignments. Tracks postmortem completion rate as an engineering health metric.

**User Interaction:**
- Tab: `/platform/incidents/postmortems`
- Table of all resolved incidents that require a postmortem (P0 and P1 by default; P2 optional)
- Columns: incident title · severity · resolved date · postmortem status (Not Started · Draft · In Review · Published) · owner · due date (P0: 72h from resolution · P1: 5 days)
- Overdue postmortems highlighted in red with badge
- Click row → opens postmortem editor drawer
- **Postmortem editor**: structured template with sections: Incident Summary · Timeline Summary (auto-populated from incident timeline) · Root Cause (mandatory) · Contributing Factors · Impact Assessment (tenants affected · students affected · revenue impact · SLA breach) · What Went Well · What Went Wrong · Action Items (table with: item · owner · due date · priority) · Lessons Learned
- Action items table: add/edit/delete rows; each item assigned to a platform staff member; status tracked (Open · In Progress · Done)
- "Publish Postmortem" button — marks as Published; sends notification to all incident responders and Platform Admin; generates shareable internal link
- "Postmortem Review" workflow: author marks as "In Review"; Platform Admin or senior DevOps reviews and approves → status moves to "Published"
- Postmortem completion rate KPI shown at top of section: "15/18 postmortems published — 3 overdue"

**UI Components:**
- Postmortem status table with due date and overdue highlight
- "Overdue" red badge
- Postmortem editor slide-in drawer
- Structured template sections (headings + text areas + tables)
- Action items table (add/edit/delete rows)
- Owner assignment dropdown (filtered to platform staff)
- "Save Draft" and "Submit for Review" and "Publish" buttons
- Completion rate KPI bar at section top

**Data Flow:**
- Postmortem list: JOIN `platform_incidents` (status = 'resolved', severity IN ('P0','P1')) LEFT JOIN `platform_postmortems` ON `incident_id`
- Auto-populated timeline summary: formatted from `platform_incident_timeline` records for the incident
- Save draft: `UPSERT platform_postmortems` (all sections as JSONB column)
- Publish: updates `status = 'published'`; Lambda fires notification emails via SES; records in `platform_audit_log`
- Action items: `platform_postmortem_action_items` table (many per postmortem)
- Action item status updates: `PATCH /platform/api/postmortems/{id}/actions/{action_id}`

**Role-Based Behavior:**
- Any assigned incident responder: can author and edit drafts for incidents they were part of
- Platform Admin: can view, edit, and publish all postmortems; can override ownership assignment
- DevOps Engineer: can review and approve postmortems authored by others on their team
- Security Engineer: can view postmortems for security incidents

**Edge Cases:**
- Postmortem due date passes without a draft: daily automated reminder email to incident owner + Platform Admin; escalation to on-call if 5 days overdue
- Action item owner leaves the platform (account deactivated): item flagged "Unowned — reassign required" in amber
- Incident resolved and immediately re-opened (flapping): postmortem due date resets to new resolution time; previous draft preserved as v1

**Performance:**
- Postmortem list renders in < 200ms (simple JOIN on two indexed tables)
- Editor auto-saves draft every 30 seconds (debounced PATCH request)

**Mobile:**
- Postmortem editor opens full-screen on mobile
- Action items table is horizontally scrollable

**Accessibility:**
- Action items table has proper `<th scope="col">` headers
- "Overdue" badges include `aria-label="Postmortem overdue — due {date}"`
- Auto-save status announced via `aria-live="polite"` region

---

### Section 9 — MTTR Analytics and Incident Metrics

**Purpose:**
Tracks Mean Time to Acknowledge (MTTA), Mean Time to Mitigate (MTTM), and Mean Time to Resolve (MTTR) over time. Feeds into the DORA metrics dashboard on C-09 and provides the engineering leadership with a quantitative view of incident response quality.

**User Interaction:**
- Tab: `/platform/incidents/analytics`
- Date range selector (7d · 30d · 90d · custom)
- Four headline KPI cards: Total Incidents · P0 Count · MTTA (target: < 5 min P0) · MTTR (target: < 4h P0)
- MTTR trend line chart (rolling 30-day average overlaid on daily values)
- Incidents by severity donut chart (P0/P1/P2 distribution)
- Incidents by root cause category bar chart (categories: Infrastructure · Database · Deployment · Security · AI Pipeline · External Dependency · Unknown)
- Incidents by service heatmap (which services are involved in most incidents)
- Time-of-day histogram (when do incidents most commonly occur? Useful for on-call rotation planning)
- Recurring incident detector: surfaces incident patterns (same root cause category + same service, 3+ times in 90 days) with suggestion to create or improve a runbook
- "Export Analytics Report" button — generates PDF summary of all charts and KPIs for the selected date range

**UI Components:**
- Date range selector tabs + custom date picker
- 4 headline KPI cards (with delta vs prior period)
- MTTR trend line chart (daily + 30d rolling average)
- Severity donut chart
- Root cause bar chart
- Service heatmap (service × severity matrix, colour = incident count)
- Time-of-day histogram
- Recurring pattern panel (list of detected patterns)
- "Export Analytics Report" button

**Data Flow:**
- KPIs computed from `platform_incidents` filtered by date range and severity
- MTTA: AVG(`acknowledged_at` - `detected_at`) grouped by day; NULL acknowledged_at excluded
- MTTR: AVG(`resolved_at` - `detected_at`) grouped by day; NULL resolved_at excluded
- Heatmap: GROUP BY `service_tag`, `severity` — each incident can have multiple service tags (UNNEST array)
- Recurring pattern detection: server-side query identifies `(root_cause_category, primary_service)` pairs with COUNT >= 3 in 90 days
- Export PDF: Lambda generates report using chart image snapshots + metric tables; signed S3 download URL

**Role-Based Behavior:**
- All allowed roles: full read access to analytics (no write actions in this section)
- Security Engineer: analytics filtered to security-tagged incidents only (service heatmap and root cause chart scoped accordingly)

**Edge Cases:**
- Date range with zero incidents: all KPI cards show "0" or "N/A"; charts show empty states with "No incidents in this period — system healthy"
- MTTA cannot be computed (no acknowledged_at): KPI shows "N/A — unacknowledged incidents excluded" with count of such incidents
- Custom date range exceeding 365 days: warning "Analytics older than 1 year may be incomplete — archived records may not be included"

**Performance:**
- Analytics computed on-demand with results cached in Memcached (TTL 15 minutes per {date_range, role} key)
- Heatmap and trend charts rendered server-side as SVG for fast initial load; interactive overlays added via lightweight JS
- PDF export is async (Celery job); download link sent via SSE when ready (typically < 20s)

**Mobile:**
- KPI cards stack 2×2 grid on mobile, then 1-column
- Charts reflow to full-width; heatmap becomes horizontal scrollable table on mobile

**Accessibility:**
- Charts include `<title>` and `<desc>` SVG elements for screen reader context
- All chart data also available as accessible data table (hidden by default, revealed via "Show as Table" button)
- KPI delta indicators use text labels ("Up 2.3 minutes vs prior period") not just arrows

---

### Section 10 — Incident Declaration Modal

**Purpose:**
Structured intake form for declaring a new incident. Ensures every incident is created with sufficient metadata for immediate triage, proper alerting, and accurate postmortem attribution later.

**User Interaction:**
- Triggered by "Declare Incident" button on the header (Section 1) or the board (Section 2)
- Three-step modal: Step 1 — Severity & Classification · Step 2 — Details & Impact · Step 3 — Notification & Responders
- **Step 1**: severity selector (P0 · P1 · P2 with severity guide tooltip) · incident category (Infrastructure · Database · Security · AI Pipeline · Mobile · Exam Platform · External) · affected services (multi-select from service registry) · is this exam-day related? (checkbox — if yes, P0 is automatically suggested)
- **Step 2**: incident title (mandatory, < 100 chars) · description (free text, < 1,000 chars) · affected tenants (All · Specific — multi-select from tenant search) · estimated student impact (dropdown: None · < 1K · 1K–50K · 50K–500K · > 500K) · detection source (Automated Alert · Manual Discovery · External Report · Tenant Report)
- **Step 3**: notification channels (Slack channel multi-select · email list toggle) · initial responder (dropdown of current on-call staff; defaults to current on-call primary) · incident commander (P0 only — mandatory; dropdown of senior engineers)
- "Declare & Alert" button at Step 3 — creates incident record + fires PagerDuty alert + posts Slack notification simultaneously
- P0 + exam-day selected: warning banner "This will trigger War Room escalation and drop poll interval to 10s platform-wide"

**UI Components:**
- 3-step progress modal with step indicator
- Severity guide tooltip (P0: full outage · P1: degraded · P2: minor impact)
- Service registry multi-select with search
- Affected tenant multi-select (search by name or subdomain)
- Detection source dropdown
- Notification channel multi-select
- On-call staff dropdown (sorted: on-call primary first, then others)
- "Declare & Alert" primary action button
- P0 exam-day warning banner

**Data Flow:**
- Service registry dropdown: `SELECT name, id FROM platform_service_registry ORDER BY name`
- On-call staff: fetched from OpsGenie current shift (Memcached 60s TTL)
- On submit: `POST /platform/api/incidents` — creates `platform_incidents` record with all fields, initial status = 'open', `detected_at = NOW()`
- Simultaneously (parallel Lambda calls): PagerDuty trigger alert · Slack webhook post · if P0 + exam-day → notify War Room Div A page owners
- All creates appended to `platform_audit_log`

**Role-Based Behavior:**
- Security Engineer: category pre-set to "Security"; severity restricted to P0 or P1 for security incidents (cannot declare P2 security — minimum P1)
- DevOps / Platform Admin: all fields unrestricted
- P0 incident command assignment: only DevOps Engineers and Platform Admins appear in the Incident Commander dropdown

**Edge Cases:**
- "Declare & Alert" clicked with PagerDuty unavailable: incident created in local DB; PagerDuty alert queued for retry (Celery); amber warning shown "Incident created — PagerDuty alert queued, will send when connectivity restored"
- P0 declared during an existing P0: system checks for existing active P0; if found, prompts "An active P0 exists. Is this a separate incident or should it be merged?" with Merge or New Incident options
- Exam-day P0 toggle accidentally checked: Step 3 warns again before final declaration; requires explicit checkbox confirmation

**Performance:**
- Modal opens in < 150ms (service registry loaded eagerly on page load; cached in browser memory)
- Declaration API responds in < 300ms; PagerDuty and Slack calls are async (do not block modal close)

**Mobile:**
- Steps stack full-screen on mobile with swipe-left to advance
- Multi-selects use native mobile bottom sheet picker

**Accessibility:**
- Step indicator uses `aria-current="step"` on active step
- All form fields have explicit `<label>` associations
- "Declare & Alert" button disabled (with explanation) until mandatory fields in all steps are complete

---

## User Flow

### Flow A — Respond to Active P0 Incident (Exam Day)

1. On-call engineer receives PagerDuty page on mobile.
2. Opens `/platform/incidents` — red banner shows active P0 incident title and elapsed time.
3. Board shows P0 card pulsing with "Open" status; clicks card → incident detail drawer opens.
4. Overview tab shows SLA timers (acknowledge < 5 min; 2:15 elapsed — amber).
5. Clicks "Acknowledge" → status updates to "Acknowledged"; PagerDuty acknowledges; SLA timer resets for mitigation phase.
6. Timeline tab — adds first update "Investigating Lambda concurrency limits on exam-submit endpoint".
7. Runbook tab — searches "Lambda concurrency"; attaches runbook "Lambda Throttle Response"; begins working through checklist.
8. War Room button pulses red (exam day) — clicks to open War Room in second tab for stakeholder coordination.
9. After mitigation action completed — adds timeline update "Concurrency limit raised to 2,000; error rate dropping".
10. Monitors C-04 (API Health) in second tab to confirm P99 latency returning to normal.
11. When P99 < 200ms for 5 consecutive minutes: returns to incident drawer → clicks "Resolve Incident" → 2FA → enters resolution summary and root cause "Lambda concurrency — insufficient pre-warming for exam window".
12. Incident moves to Resolved; PagerDuty resolves; Slack notification sent to incident channel.
13. Postmortem entry appears in Postmortem Tracker with 72h due date.

### Flow B — Create Runbook for Recurring Pattern

1. DevOps Engineer opens Analytics tab.
2. Recurring pattern panel shows: "RDS connection pool exhaustion — 4 occurrences in 90 days — no runbook linked".
3. Clicks "Create Runbook from Pattern" → New Runbook modal pre-filled with category "Database" and title suggestion.
4. Adds 8 mitigation steps, escalation path, and rollback steps.
5. Saves; runbook immediately available in library and searchable in incident drawer.

### Flow C — Postmortem Authorship and Publish

1. Platform Admin opens Postmortem Tracker — sees 3 overdue postmortems in red.
2. Clicks oldest overdue P0 row → postmortem editor opens.
3. Timeline summary already auto-populated from incident timeline.
4. Fills in Root Cause, Contributing Factors, Impact Assessment (2 tenants · 45,000 students · 18-minute exam-submit outage).
5. Adds 4 action items: assigns 3 to DevOps Engineers; 1 infrastructure item to Platform Admin.
6. Clicks "Submit for Review" → senior DevOps receives notification.
7. Reviewer opens, reads, approves → "Publish" → postmortem published; all incident responders notified.
8. Action items now trackable; MTTR analytics updated in next cache refresh.

---

## Component Structure

| Component | Purpose |
|---|---|
| `incident-status-bar` | Global status banner; polled every 15s; drives page-wide severity state |
| `incident-board` | Kanban board; P0/P1/P2 columns; polled every 15s; morph-swap on update |
| `incident-card` | Individual incident card with quick-actions; live countdown timer (client-side) |
| `incident-detail-drawer` | 5-tab full incident workspace; `id="incident-drawer"` |
| `incident-timeline-view` | Full-page timeline with swimlane chart and phase markers |
| `runbook-library` | Category tree + search + runbook detail view |
| `runbook-editor` | WYSIWYG step editor with drag-to-reorder and version history |
| `oncall-calendar` | 2-week schedule grid; OpsGenie-synced |
| `integration-panel` | PagerDuty + OpsGenie configuration and webhook log |
| `postmortem-tracker` | Resolved incident postmortem status table |
| `postmortem-editor` | Structured template drawer with action items table |
| `mttr-analytics` | KPI cards + trend charts + heatmap + export |
| `incident-declaration-modal` | 3-step intake form with alert firing |
| `war-room-link` | Always-visible header button; pulses during exam-day P0 |

---

## Data Model

### `platform_incidents`

| Column | Type | Description |
|---|---|---|
| `id` | UUID PK | Incident identifier |
| `title` | VARCHAR(100) | Short incident title |
| `description` | TEXT | Full description |
| `severity` | ENUM | P0 · P1 · P2 |
| `status` | ENUM | open · acknowledged · mitigating · resolved |
| `category` | ENUM | infrastructure · database · security · ai_pipeline · mobile · exam_platform · external |
| `service_tags` | TEXT[] | Affected services (array) |
| `is_exam_day` | BOOLEAN | True if declared during active exam window |
| `detected_at` | TIMESTAMPTZ | When incident was first detected |
| `acknowledged_at` | TIMESTAMPTZ | When on-call acknowledged; NULL if not yet |
| `mitigated_at` | TIMESTAMPTZ | When mitigation confirmed; NULL if not yet |
| `resolved_at` | TIMESTAMPTZ | When fully resolved; NULL if active |
| `detection_source` | ENUM | automated_alert · manual · external · tenant_report |
| `assigned_to` | FK → platform_staff | Current primary responder |
| `incident_commander` | FK → platform_staff | IC for P0 incidents |
| `affected_tenants` | TEXT[] | Tenant subdomains affected; empty = all |
| `student_impact_range` | ENUM | none · lt1k · 1k_50k · 50k_500k · gt500k |
| `root_cause_category` | ENUM | Set on resolution |
| `resolution_summary` | TEXT | Written by resolver on close |
| `created_by` | FK → platform_staff | Who declared the incident |
| `created_at` | TIMESTAMPTZ | Declaration time |

---

### `platform_incident_timeline`

| Column | Type | Description |
|---|---|---|
| `id` | UUID PK | Entry identifier |
| `incident_id` | FK → platform_incidents | Parent incident |
| `event_at` | TIMESTAMPTZ | When event occurred |
| `event_type` | ENUM | detection · acknowledgement · update · escalation · mitigation · resolution · communication_sent |
| `actor_type` | ENUM | system · engineer · admin · pagerduty · opsgenie |
| `actor_id` | FK → platform_staff | NULL for system events |
| `note` | TEXT | Free-text update; immutable after insert |
| `metadata` | JSONB | Additional structured data (e.g., severity before/after escalation) |

---

### `platform_runbooks`

| Column | Type | Description |
|---|---|---|
| `id` | UUID PK | Runbook identifier |
| `title` | VARCHAR(200) | Runbook title |
| `category` | ENUM | infrastructure · database · security · ai_pipeline · mobile · exam_platform · general |
| `severity_applicability` | TEXT[] | Which severities this applies to |
| `estimated_resolution_minutes` | INT | Expected time to resolve |
| `current_version` | INT | Current active version number |
| `last_reviewed_at` | TIMESTAMPTZ | Date of last simulation review |
| `created_by` | FK → platform_staff | Author |
| `archived` | BOOLEAN | Soft-delete flag |
| `tsvector_content` | TSVECTOR | Full-text search index (auto-updated trigger) |

---

### `platform_runbook_versions`

| Column | Type | Description |
|---|---|---|
| `id` | UUID PK | Version record |
| `runbook_id` | FK → platform_runbooks | Parent runbook |
| `version` | INT | Version number |
| `content_json` | JSONB | Full runbook content (steps, escalation, rollback) |
| `saved_by` | FK → platform_staff | Who saved this version |
| `saved_at` | TIMESTAMPTZ | When saved; immutable |

---

### `platform_incident_runbooks`

| Column | Type | Description |
|---|---|---|
| `incident_id` | FK → platform_incidents | |
| `runbook_id` | FK → platform_runbooks | |
| `version_at_attachment` | INT | Snapshot of runbook version when attached |
| `attached_by` | FK → platform_staff | |
| `attached_at` | TIMESTAMPTZ | |
| Composite PK | `(incident_id, runbook_id)` | |

---

### `platform_postmortems`

| Column | Type | Description |
|---|---|---|
| `id` | UUID PK | Postmortem identifier |
| `incident_id` | FK → platform_incidents | One-to-one |
| `status` | ENUM | not_started · draft · in_review · published |
| `owner` | FK → platform_staff | Assigned postmortem author |
| `due_at` | TIMESTAMPTZ | Derived from incident resolution + SLA (P0: +72h, P1: +5d) |
| `content_json` | JSONB | All sections stored as structured JSON |
| `published_at` | TIMESTAMPTZ | When published; NULL if draft |
| `reviewed_by` | FK → platform_staff | Reviewer who approved |
| `reviewed_at` | TIMESTAMPTZ | |

---

### `platform_postmortem_action_items`

| Column | Type | Description |
|---|---|---|
| `id` | UUID PK | |
| `postmortem_id` | FK → platform_postmortems | |
| `description` | TEXT | Action item text |
| `owner` | FK → platform_staff | Assigned to |
| `priority` | ENUM | high · medium · low |
| `due_date` | DATE | Target completion date |
| `status` | ENUM | open · in_progress · done |
| `completed_at` | TIMESTAMPTZ | When marked done |

---

### `platform_oncall_history`

| Column | Type | Description |
|---|---|---|
| `id` | UUID PK | |
| `role_name` | VARCHAR(100) | On-call role (Primary, Secondary, IC, etc.) |
| `engineer_id` | FK → platform_staff | Who was on-call |
| `shift_start` | TIMESTAMPTZ | |
| `shift_end` | TIMESTAMPTZ | |
| `source` | ENUM | opsgenie · manual_override |

---

### `platform_webhook_events`

| Column | Type | Description |
|---|---|---|
| `id` | UUID PK | |
| `source` | ENUM | pagerduty · opsgenie |
| `event_type` | VARCHAR(100) | e.g., `incident.trigger`, `incident.resolve` |
| `event_dedup_key` | VARCHAR(255) | Unique key for deduplication |
| `payload` | JSONB | Full raw payload |
| `received_at` | TIMESTAMPTZ | |
| `processed` | BOOLEAN | Whether platform action was taken |

---

## Validation Rules

| Field | Rule |
|---|---|
| Incident title | Mandatory · 5–100 characters · no HTML |
| Incident description | Mandatory · max 1,000 characters |
| Severity | Mandatory · must be P0, P1, or P2 |
| Category | Mandatory · must match enum |
| Affected services | At least one service must be selected |
| Incident commander | Mandatory for P0 · must be DevOps or Platform Admin role |
| Timeline note | Mandatory when adding update · max 2,000 characters · immutable after save |
| Resolution summary | Mandatory · min 50 characters · blocked if blank |
| Root cause category | Mandatory on resolution · cannot be left as NULL |
| Postmortem content | Root Cause section mandatory before "Submit for Review" |
| Action item description | Mandatory · max 500 characters |
| Action item owner | Must be an active platform staff member |
| Runbook title | Mandatory · 5–200 characters |
| Runbook steps | Minimum 3 steps required to save |
| Override request reason | Mandatory · max 500 characters |

---

## Security Considerations

- **Incident declaration is audited**: every `platform_incidents` creation and status change is appended to `platform_audit_log` with actor, timestamp, and before/after state (JSONB diff)
- **Timeline entries are immutable**: once inserted to `platform_incident_timeline`, no UPDATE or DELETE is permitted at application layer; DB trigger enforces this
- **Resolution requires 2FA**: resolving a P0 incident requires TOTP validation to prevent accidental resolution during active remediation
- **Mass acknowledge requires 2FA**: the emergency "Mass Acknowledge All P0" action (triggered during cascading failures) requires 2FA
- **Postmortem publish notifies widely**: publish event fires SES notifications to all named incident responders; if more than 20 recipients, batch via Celery to avoid SES rate limits
- **PagerDuty/OpsGenie API keys**: stored exclusively in AWS Secrets Manager; API key values never displayed in UI; rotation managed via C-14 (Secrets Manager)
- **Communication send requires confirmation**: before sending Slack/email update from incident drawer, a preview modal shows exact message and recipient count; accidental sends prevented
- **Security incidents**: incidents tagged `security` are visible only to Platform Admin, DevOps, and Security Engineer; other roles cannot see these cards, timelines, or postmortems
- **War Room escalation**: P0 exam-day incidents trigger a notification to Div A Page 32 owners; this cross-division escalation is logged in `platform_audit_log`
- **CERT-In compliance**: any P0 security incident automatically checks whether the 6-hour CERT-In breach reporting window is relevant (cross-links to C-13 for breach tracker)

---

## Edge Cases

| Scenario | Handling |
|---|---|
| P0 incident auto-created by C-04 alert (Lambda throttle) | Appears on board within next poll cycle (max 15s); on-call receives PagerDuty page; War Room link pulses if exam-day flag set |
| P0 declared during active exam; exam ends before resolution | `is_exam_day` flag retained; War Room link no longer pulses; poll interval returns to 15s; incident continues normally |
| Incident created by automation with wrong severity (e.g., P0 for minor test run) | Any allowed role can escalate or de-escalate; every change appended to timeline with reason |
| Incident resolved but immediately re-triggers within 30 minutes | System detects related incident signature and prompts "Possible re-open of {previous incident} — link or create new?" |
| On-call engineer loses connectivity mid-incident | Board state preserved server-side; another responder can self-assign; OpsGenie escalation fires automatically after 10 minutes with no timeline updates |
| Postmortem with > 20 action items | Action items table paginates (10 per page); all items included in PDF export |
| Runbook with 100+ steps (e.g., comprehensive DR runbook) | Rendered as paginated checklist in drawer; full runbook available in full-page view |
| Security incident escalated to CERT-In | C-13 breach tracker link appears in incident drawer Overview tab; countdown timer from C-13 shown inline |
| Multiple responders simultaneously editing postmortem | Last-write-wins (UPSERT); optimistic locking: editor shows "Another user saved changes 30s ago — reload to see latest" toast |
| PagerDuty webhook delivers event for unknown incident ID | Event logged to `platform_webhook_events` with `processed = false`; Platform Admin alerted for manual review |

---

## Performance and Scaling Strategy

- **Incident board poll (15s/10s)**: uses HTMX morph-swap — only changed incident card HTML is replaced; no full board re-render; board renders in < 200ms for up to 50 concurrent incidents
- **Incident status bar poll**: separate lightweight `?part=board` part that returns only the banner state (severity + incident count); renders in < 50ms (single aggregation query)
- **Timeline immutability at scale**: `platform_incident_timeline` grows unboundedly for long incidents; paginated (50 events per load); full-page timeline view groups events by 5-minute windows when > 500 events
- **Runbook library**: small dataset (< 500 runbooks); cached in Memcached (TTL 5 minutes); full-text search on PostgreSQL tsvector GIN index returns results in < 100ms
- **MTTR analytics**: computed on-demand; results cached in Memcached keyed by `{date_range}_{role}`; TTL 15 minutes; for 90-day ranges the query touches up to ~10K incident records (fully indexed on `detected_at`, `resolved_at`, `severity`)
- **OpsGenie schedule**: cached 60s in Memcached; OpsGenie webhook triggers cache.delete on any schedule change; avoids redundant OpsGenie API calls during heavy incident periods when page is polled frequently
- **PagerDuty calls**: all outbound PagerDuty API calls are async (Lambda invocation); never block the UI response; failures queued to Celery for retry with exponential backoff (max 5 retries over 1 hour)
- **Postmortem PDF export**: Celery async job; Lambda generates PDF from headless renderer; signed S3 URL (15-minute TTL) delivered via SSE; typical generation time 10–20s for a full postmortem with all sections
- **Concurrent incident writes**: PostgreSQL row-level locking prevents concurrent status updates from conflicting; `SELECT FOR UPDATE SKIP LOCKED` pattern used in the acknowledge flow to handle simultaneous acknowledgement clicks from two responders
- **Exam-day scaling**: during exam windows, the platform_incidents board is the most actively polled page in Division C; CloudFront caches the `?part=board` response for 10s (shared cache across all on-call users viewing the page simultaneously) — individual incident queries bypass CloudFront

---

*C-18 — Engineering Incident Manager.*

---

## Amendment — G10: Alert Rules Tab

**Assigned gap:** G10 — C-18 has on-call schedule and PagerDuty integration but nobody can configure metric alert thresholds (e.g. "Lambda error rate > 5% → P1") from the portal. Alert rules are hardcoded or configured directly in PagerDuty/CloudWatch without a platform-managed audit trail.

**Where it lives:** New tab in the C-18 page tab bar (alongside Runbooks, On-Call, Analytics, Integrations).

---

### Alert Rules Tab

**Purpose:** Give DevOps Engineers and Platform Admins a single place to define, view, and manage the metric alert thresholds that drive PagerDuty pages. Every rule change is audited. Rules are linked to their incident history so the team can see which rules are noisy (many pages, few real incidents) vs effective.

**Layout:** Two panels — Active Rules Table · Rule Editor Drawer

---

**Active Rules Table:**

| Column | Description |
|---|---|
| Rule Name | Human-readable name (e.g., "Lambda Error Rate — P1") |
| Metric | CloudWatch metric namespace + metric name |
| Service | Which platform service this monitors |
| Condition | Threshold expression (e.g., "error_rate > 5% for 3 consecutive 1-min windows") |
| Severity | P0 · P1 · P2 |
| PagerDuty Routing | Which PagerDuty service + escalation policy receives this alert |
| Status | ✅ Active · ⏸ Silenced · ❌ Disabled |
| Last Triggered | Timestamp of most recent alert firing |
| Incidents Created (30d) | Count of C-18 incidents linked to this rule |
| Noise Ratio | % of alerts that resulted in acknowledged incidents (low % = noisy) |
| Actions | Edit · Silence · Disable · View history |

**Existing alert rules (representative inventory):**

| Rule | Metric | Threshold | Severity |
|---|---|---|---|
| Lambda Error Rate — P1 | Lambda `Errors` / `Invocations` | > 5% for 3 min | P1 |
| Lambda Error Rate — P0 (exam day) | Same metric | > 10% + `is_exam_day = true` | P0 |
| API P99 Latency — P1 | ALB `TargetResponseTime` P99 | > 800ms for 5 min | P1 |
| RDS CPU — P2 | RDS `CPUUtilization` | > 85% for 10 min | P2 |
| RDS Connection Pool — P1 | PgBouncer `cl_waiting` | > 50 waiting clients | P1 |
| Celery Queue Depth — P2 | `platform_celery_queue_stats.queue_depth` | > 500 for 5 min | P2 |
| Failed Auth Burst — P1 | `platform_failed_auth_stats.count_1h` | > 2,000 in 1h | P1 |
| Memcached Node Down — P1 | ElastiCache `CurrItems` sudden drop | > 90% drop in 2 min | P1 |
| ECS Task Health — P0 | ECS `TaskCount` for service | < 2 healthy tasks | P0 |
| AI Pipeline Hard Stop — P1 | `platform_ai_budget_config.hard_stop_enabled` | = true | P1 |

**Filter bar:** Service · Severity · Status (Active / Silenced / Disabled) · Noise ratio > 80% toggle

---

**Rule Editor Drawer (alert-rule-drawer, 640px)**

Opens on "Edit" or "New Rule" button.

**Tabs: Definition · Routing · History**

**Tab — Definition:**

- Rule name: text input (required)
- Description: textarea (what does this alert mean, what should the on-call do first?)
- Metric source: select (CloudWatch / ORM query / Custom Celery metric)
- For CloudWatch:
  - Namespace: dropdown (AWS/Lambda · AWS/RDS · AWS/ECS · AWS/ElastiCache · AWS/ApplicationELB · Custom)
  - Metric name: dropdown (populated based on namespace)
  - Dimension: key=value (e.g., FunctionName=auth-service-login)
  - Statistic: Average · Sum · Maximum · Minimum · p99 · p95
  - Period: 1 min · 5 min · 15 min
  - Threshold: operator (> · < · >= · <= · !=) + value
  - Consecutive periods: "for N consecutive periods" (1–10)
- Exam Day escalation: checkbox — "Escalate to P0 during active exam window (overrides severity above)"
- Silence window: optional time-of-day window when alert is suppressed (e.g., 03:00–04:00 IST for scheduled maintenance)
- Severity: P0 · P1 · P2

**Save → CloudWatch Alarm API (PutMetricAlarm)** — creates or updates the CloudWatch alarm backing this rule.

**Tab — Routing:**

- PagerDuty service: select from connected PagerDuty services (fetched from integration panel)
- Escalation policy: select (from PagerDuty API)
- Auto-create C-18 incident: toggle (yes/no) — if yes, incident is automatically created in platform DB when alert fires + PagerDuty page sent simultaneously
- Auto-incident severity: auto-filled from rule severity (editable)
- Auto-incident category: select
- Linked runbook: search and attach (if auto-create = yes, the runbook is pre-attached to auto-created incidents)

**Tab — History:**

Table of all times this alert fired:
- Fired at · Duration (how long metric stayed above threshold) · Incident created (link) · Resolved at · Resolution type (alert cleared / manual resolve / auto-resolve)
- "Noise analysis": of the last 30 firings, {n}% resulted in a created and acknowledged incident (the rest were acknowledged without an incident → noise)

**Silence an alert:**
- "Silence" action → modal: duration (1h / 4h / 12h / until next scheduled maintenance window) + reason (required)
- Silenced alerts still log to history but do not page PagerDuty
- Auto-unsilence at end of duration
- Silence shown in Active Rules Table as "⏸ Silenced until {time}"

**Data model:**

**platform_alert_rules**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| name | VARCHAR(200) | |
| description | TEXT | |
| metric_source | ENUM | cloudwatch/orm/celery_metric |
| cloudwatch_alarm_arn | VARCHAR(512) | nullable |
| metric_config | JSONB | namespace/metric/dimension/threshold/period config |
| exam_day_escalate | BOOLEAN | |
| severity | ENUM | p0/p1/p2 |
| pagerduty_service_id | VARCHAR(100) | |
| auto_create_incident | BOOLEAN | |
| linked_runbook_id | UUID FK → platform_runbooks | nullable |
| status | ENUM | active/silenced/disabled |
| silenced_until | TIMESTAMPTZ | nullable |
| silence_reason | TEXT | nullable |
| created_by | UUID FK → platform_staff | |
| created_at | TIMESTAMPTZ | |
| updated_by | UUID FK → platform_staff | |
| updated_at | TIMESTAMPTZ | |

---

## Amendment — G21: Runbook Editor Tab

**Assigned gap:** G21 — C-18 displays a runbook library but there is no editor to create, update, or version runbooks from the portal. Runbook updates require direct DB access outside the platform, creating an audit gap.

**Where it lives:** The existing Runbook Library (Section 5) is extended — it gains a full editor tab. The section becomes a two-tab panel: **Library** (existing browsing/search) · **Editor** (new — create/edit/version).

**Note:** The existing spec describes some editing capability ("Edit Runbook" button, WYSIWYG editor with version history) but it is underspecified — no drawer detail, no step-level data model, no version diff view. This amendment fully specifies the editor.

---

### Runbook Editor Tab

**Purpose:** Give DevOps Engineers and Platform Admins a fully-featured runbook creation and editing tool within the platform. All changes are versioned, auditable, and can be linked directly to alert rules (G10).

**Access:** DevOps Engineer (Role 14) + Platform Admin (Role 10) — write access. Security Engineer (Role 16) — write access for Security category runbooks only.

**Layout:** Two panels — Runbook List (left sidebar) · Editor (main panel)

---

**Left Sidebar — Runbook List:**

Same category tree as the Library tab, but with:
- "New Runbook" button at top
- Edit/Archive icons on hover per row
- Draft runbooks shown with "Draft" badge
- Archived runbooks hidden by default; "Show archived" toggle

**Main Panel — Editor:**

**Header controls:**
- Runbook title: large text input
- Category: dropdown
- Severity applicability: checkbox group (P0 · P1 · P2)
- Affected services: multi-select from service registry
- Estimated resolution time: number input (minutes)
- Tags: free text multi-tag input (for search indexing)
- Linked alert rule: search and select from platform_alert_rules (G10 integration) — optional; allows "From alert rule, open this runbook in drawer"
- Status badge: Draft / Published (toggles on Save vs Publish)

**Step Editor:**

Each step is an independent editable block:

- Step number (auto-assigned, drag-to-reorder)
- Step title: text input (short heading, e.g., "Check Lambda error logs")
- Step body: rich-text area (supports markdown — bold, code blocks, lists, links; rendered as formatted text in view mode)
- Step type: Action (engineer does something) · Check (verify a state) · Decision (branch point) · Escalation (escalate to another team)
- For Decision steps: two outcome paths (Yes/No or Pass/Fail) each pointing to a step number
- For Escalation steps: escalation target (select from platform_staff or role type) + escalation message template
- "Add step below" button between steps (+ drag handle for reorder)
- "Delete step" button (with confirmation — warns if other steps reference this step number in a Decision branch)
- Minimum 3 steps to save; system validates sequential step numbering

**Rollback section:**
- Separate collapsible section below main steps: "Rollback procedure" (free-text textarea)
- "Has rollback: Yes / No" checkbox — if No, a warning badge appears on the runbook in the library

**Escalation path section:**
- Escalation path: ordered list of escalation contacts (select from platform staff)
- Escalation conditions: text description of when to escalate beyond the runbook steps
- Linked to C-02 G30 escalation chains: optional link to a platform_escalation_chains record

**Related runbooks:**
- Multi-select search: link to other runbooks that are commonly used alongside this one

**Save / Version controls:**

- "Save Draft" → saves without incrementing version; only the author can see draft version changes
- "Publish" → increments version number; new version becomes AWSCURRENT; previous version retained in history
- "Request Review" → sends notification to a selected senior DevOps or Platform Admin for review before publish
- "Discard changes" → reverts to last published version

**Version History panel (right-side drawer or bottom panel):**

- Version table: version number · published by · published at · change summary (required field on publish)
- "View this version" → read-only preview of historical version
- "Restore this version" → creates a new draft from historical version content (does not overwrite published version; goes through draft → publish flow)
- "Diff view" → side-by-side comparison of any two versions (step-level diff: added/removed/changed steps highlighted)

**Test badge:**
- "Mark as tested (simulated)" → records who tested, when, and via what scenario (free text)
- Quarterly reminder: if last test > 90 days ago, amber badge "Overdue for simulation review" on runbook card in Library

**Audit trail:**
All runbook creates, edits, publishes, and archives logged to `platform_security_audit_log` (C-13 G24) under event_category = `platform_config`.

**Data model additions:**

The existing `platform_runbooks` and `platform_runbook_versions` tables (documented in the Data Model section) are extended:

**platform_runbooks additions:**

| Field | Type | Notes |
|---|---|---|
| linked_alert_rule_id | UUID FK → platform_alert_rules | nullable (G10 integration) |
| has_rollback | BOOLEAN | whether a rollback procedure is documented |
| escalation_chain_id | UUID FK → platform_escalation_chains | nullable (C-02 G30) |
| last_tested_at | TIMESTAMPTZ | nullable |
| last_tested_by | UUID FK → platform_staff | nullable |
| test_scenario | TEXT | nullable — description of simulation scenario |

**platform_runbook_versions additions:**

| Field | Type | Notes |
|---|---|---|
| change_summary | VARCHAR(500) | required on publish — describes what changed |
| status | ENUM | draft/published/archived |
| reviewed_by | UUID FK → platform_staff | nullable — reviewer who approved before publish |
| reviewed_at | TIMESTAMPTZ | nullable |
