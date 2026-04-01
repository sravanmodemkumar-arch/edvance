# Component 11 — Timeline / Activity Feed

> **Timeline** (also called Activity Feed, Audit Log Stream, or Event Feed) is the component used wherever the EduForge Admin Portal needs to display a chronological sequence of events, actions, changes, or notifications. Timelines appear in incident response pages (WAR ROOM, P0 tracking), audit logs, institution activity feeds, user session history, billing event history, and compliance change logs.
>
> Unlike a data table (which is optimized for sorting, filtering, and bulk operations), a Timeline is optimized for **reading a story** — understanding what happened, in what order, by whom, and why. Every entry on a Timeline is a moment in time with an actor, an action, an outcome, and optional metadata.
>
> The component supports both static (paginated REST) and real-time (WebSocket streamed) modes. In real-time mode, new events slide in from the top with an animated entrance.
>
> All colors use CSS custom property tokens. Both dark and light themes are fully supported.

---

## 1. Anatomy of a Timeline Entry

> Each entry (also called an "event node" or "feed item") is a self-contained unit. It consists of a vertical track (the timeline rail), a node marker (dot or icon), a timestamp, an actor, an action summary, and optional expanded detail.

```
  │
  ●  ── 14:32:05  Arjun Mehta (CEO)                          [BADGE: CONFIG]
  │     Updated exam slot capacity: JEE Main 2026 → 74,000 seats
  │     Previous: 70,000  ·  New: 74,000  ·  Reason: "Peak season demand"
  │
  ●  ── 14:28:41  System (Auto-scale)                        [BADGE: INFRA]
  │     Scaled exam cluster to 12 nodes (was 8)
  │     Trigger: CPU > 80% for 3 consecutive minutes
  │
  ●  ── 14:15:00  Priya Sharma (Platform Ops)                [BADGE: INCIDENT]
  │     Opened P1 Incident: "Elevated API latency in South region"
  │     Incident ID: INC-2026-0312  ·  Duration so far: 17m  [View →]
  │
```

| Region | Purpose | Required |
|---|---|---|
| **Rail** | Vertical line connecting entries. Color is neutral by default; turns status color during incidents | Yes |
| **Node marker** | Circle dot (default) or icon badge. Color = event category | Yes |
| **Timestamp** | Exact time (HH:MM:SS) with relative time on hover (e.g., "3 minutes ago") | Yes |
| **Actor** | Who triggered the event — human (name + role) or system (service name) | Yes |
| **Action summary** | One-line plain-English description of what happened | Yes |
| **Detail block** | Key:Value pairs giving context. Collapsible on long entries | Optional |
| **Category badge** | Pill tag classifying the event type (CONFIG, INFRA, INCIDENT, BILLING, etc.) | Optional |
| **Action link** | Link to a related page, incident, or entity | Optional |

---

## 2. Event Category System

> Categories visually classify the type of event. This lets an operator scanning a busy activity feed immediately filter by visual color without reading every entry.

| Category | Badge text | Node color | Use case |
|---|---|---|---|
| `config` | CONFIG | `--primary` (indigo) | Settings changes, feature flags, capacity edits |
| `incident` | INCIDENT | `--error` (red) | P0/P1 incidents opened or updated |
| `infra` | INFRA | `--warning` (amber) | Scaling events, deployments, cluster changes |
| `billing` | BILLING | `--success` (green) | Payments, invoices, subscription changes |
| `auth` | AUTH | `--secondary` (purple) | Login, role changes, permission grants |
| `exam` | EXAM | `#06B6D4` (cyan) | Exam creation, slot changes, result publish |
| `compliance` | COMPLIANCE | `#F59E0B` (amber) | Policy changes, audit triggers, legal flags |
| `institution` | INSTITUTION | `#8B5CF6` (violet) | School/college onboard, suspend, merge |
| `system` | SYSTEM | `--text-muted` (gray) | Cron jobs, auto-scale, scheduled tasks |

---

## 3. Timeline Variants

### 3.1 Compact Feed (Default)

> The most common variant. One line per event with no expanded detail block. Used in sidebars, dashboard activity widgets, and notification panels where vertical space is limited.

```
  ●  14:32  Arjun Mehta · Updated exam capacity  [CONFIG]
  ●  14:28  System · Auto-scaled cluster          [INFRA]
  ●  14:15  Priya Sharma · Opened P1 incident     [INCIDENT]
  ●  13:50  Meera Nair · CFO approved Q1 budget   [BILLING]
```

**CSS:**
```css
.timeline--compact .timeline__entry {
  padding: var(--space-2) 0;
  min-height: 32px;
}

.timeline--compact .timeline__summary {
  font-size: var(--text-sm);
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.timeline--compact .timeline__detail { display: none; }
```

---

### 3.2 Detailed Feed

> Full entries with actor, action summary, detail block, and action links. Used on incident pages, audit log views, institution activity history, and compliance audit trails.

```
  ●  ── 14:32:05  [CONFIG]
  │     Arjun Mehta (CEO, L5) updated exam slot capacity
  │     JEE Main 2026: 70,000 → 74,000 seats
  │     Reason: "Peak season demand forecast"           [View Exam →]
  │
  ●  ── 14:28:41  [INFRA]
  │     System (Auto-Scaler) scaled exam cluster
  │     Nodes: 8 → 12  ·  Trigger: CPU > 80% / 3 min
  │
```

---

### 3.3 Grouped Feed (by Date / Session)

> Events are clustered under date dividers. Used on audit log pages, user session history, and anywhere a multi-day event stream needs scanning by day.

```
  ── TODAY, 20 MARCH 2026 ──────────────────────────────
  ●  14:32  Arjun Mehta · Updated exam capacity
  ●  14:28  System · Auto-scaled cluster
  ●  14:15  Priya · Opened P1

  ── YESTERDAY, 19 MARCH 2026 ─────────────────────────
  ●  23:45  System · Daily backup completed
  ●  18:02  Rohan · Published JEE Results (87,342 students)
```

**CSS:**
```css
.timeline__date-divider {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin: var(--space-5) 0 var(--space-3);
}

.timeline__date-divider-label {
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  white-space: nowrap;
}

.timeline__date-divider-line {
  flex: 1;
  height: 1px;
  background: var(--border-subtle);
}
```

---

### 3.4 Incident Timeline (WAR ROOM Mode)

> Specialized variant for the WAR ROOM and P0 incident pages. Entries represent incident milestones: opened, escalated, assigned, update posted, resolved. The rail turns red during open incidents. Time deltas between entries are shown.

```
  [OPENED]  14:15:00  INC-2026-0312 opened by Priya Sharma
     │       ↕ +4m
  [UPDATE]  14:19:22  Root cause identified — DB connection pool exhausted
     │       ↕ +9m
  [ASSIGN]  14:28:41  Assigned to Ravi Kumar (L4 Infra Lead)
     │       ↕ +11m
 [RESOLVE]  14:39:05  Resolved — connection pool limit raised to 500
```

```css
.timeline--incident .timeline__rail {
  background: var(--error);
  opacity: 0.4;
}

.timeline--incident.timeline--resolved .timeline__rail {
  background: var(--success);
  opacity: 0.4;
}

.timeline--incident .timeline__delta {
  font-size: var(--text-xs);
  font-family: var(--font-mono);
  color: var(--text-muted);
  padding-left: var(--space-8);
  margin: var(--space-1) 0;
}
```

---

## 4. Full HTML Structure

```html
<!-- Timeline container -->
<div class="timeline timeline--detailed" role="feed" aria-label="Platform Activity Feed">

  <!-- Real-time live indicator (shown when WS is connected) -->
  <div class="timeline__live-bar">
    <span class="timeline__live-dot"></span>
    <span>LIVE · Updates every 5s</span>
  </div>

  <!-- Date group divider -->
  <div class="timeline__date-divider" role="separator">
    <span class="timeline__date-divider-label">Today, 20 March 2026</span>
    <span class="timeline__date-divider-line"></span>
  </div>

  <!-- Single timeline entry -->
  <article class="timeline__entry" data-category="config">

    <!-- Left column: rail + node -->
    <div class="timeline__track" aria-hidden="true">
      <div class="timeline__rail"></div>
      <div class="timeline__node timeline__node--config" title="Config change"></div>
    </div>

    <!-- Right column: content -->
    <div class="timeline__content">

      <!-- Header row -->
      <div class="timeline__header">
        <time class="timeline__timestamp"
              datetime="2026-03-20T14:32:05"
              title="20 Mar 2026, 14:32:05 IST">
          14:32:05
        </time>
        <span class="timeline__actor">Arjun Mehta <span class="timeline__actor-role">(CEO)</span></span>
        <span class="timeline__badge timeline__badge--config">CONFIG</span>
      </div>

      <!-- Summary line -->
      <p class="timeline__summary">
        Updated exam slot capacity — JEE Main 2026
      </p>

      <!-- Detail block (collapsible) -->
      <div class="timeline__detail">
        <span class="timeline__kv"><b>Previous:</b> 70,000 seats</span>
        <span class="timeline__kv"><b>New:</b> 74,000 seats</span>
        <span class="timeline__kv"><b>Reason:</b> "Peak season demand forecast"</span>
        <a class="timeline__link" href="/exams/jee-main-2026">View Exam →</a>
      </div>

    </div>
  </article>

  <!-- Load more (paginated mode) -->
  <button class="timeline__load-more">Load 50 more events</button>

</div>
```

---

## 5. Full CSS

```css
/* ============================================================
   TIMELINE / ACTIVITY FEED — EduForge Admin Portal
   Dark (default) + Light theme via data-theme="light"
   Tokens: 00-global-layout.md
   ============================================================ */

/* ── Container ── */
.timeline {
  display: flex;
  flex-direction: column;
  padding: 0;
  list-style: none;
}

/* ── Live bar ── */
.timeline__live-bar {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--success);
  margin-bottom: var(--space-4);
  padding: var(--space-2) var(--space-3);
  background: color-mix(in srgb, var(--success) 8%, transparent);
  border: 1px solid color-mix(in srgb, var(--success) 20%, transparent);
  border-radius: var(--radius-full);
  align-self: flex-start;
}

.timeline__live-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--success);
  animation: live-pulse 1.5s ease-in-out infinite;
}

/* ── Entry ── */
.timeline__entry {
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 0 var(--space-3);
  padding: var(--space-1) 0 var(--space-4);
  position: relative;
}

/* Entrance animation for new real-time entries */
.timeline__entry--new {
  animation: timeline-entry-in 400ms ease-out;
}

@keyframes timeline-entry-in {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Track (rail + node) ── */
.timeline__track {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 4px;
}

.timeline__rail {
  flex: 1;
  width: 2px;
  background: var(--border-subtle);
  margin-top: 4px;
  min-height: 20px;
}

/* Dark theme rail */
:root .timeline__rail {
  background: var(--border-subtle);   /* #1E293B */
}

/* Light theme rail */
[data-theme="light"] .timeline__rail {
  background: var(--border-subtle);   /* #E2E8F0 */
}

/* ── Node markers ── */
.timeline__node {
  width: 10px; height: 10px;
  border-radius: 50%;
  border: 2px solid;
  background: var(--bg-base);
  flex-shrink: 0;
  z-index: 1;
}

/* Node color by category */
.timeline__node--config      { border-color: var(--primary); background: color-mix(in srgb, var(--primary) 20%, var(--bg-base)); }
.timeline__node--incident    { border-color: var(--error);   background: color-mix(in srgb, var(--error)   20%, var(--bg-base)); }
.timeline__node--infra       { border-color: var(--warning); background: color-mix(in srgb, var(--warning) 20%, var(--bg-base)); }
.timeline__node--billing     { border-color: var(--success); background: color-mix(in srgb, var(--success) 20%, var(--bg-base)); }
.timeline__node--auth        { border-color: #8B5CF6;        background: color-mix(in srgb, #8B5CF6 20%, var(--bg-base)); }
.timeline__node--exam        { border-color: #06B6D4;        background: color-mix(in srgb, #06B6D4 20%, var(--bg-base)); }
.timeline__node--compliance  { border-color: #F59E0B;        background: color-mix(in srgb, #F59E0B 20%, var(--bg-base)); }
.timeline__node--institution { border-color: #8B5CF6;        background: color-mix(in srgb, #8B5CF6 20%, var(--bg-base)); }
.timeline__node--system      { border-color: var(--text-muted); background: var(--bg-surface-2); }

/* ── Content column ── */
.timeline__content {
  min-width: 0;
}

/* ── Header row ── */
.timeline__header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-wrap: wrap;
  margin-bottom: var(--space-1);
}

/* ── Timestamp ── */
.timeline__timestamp {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-muted);
  flex-shrink: 0;
}

/* Light theme */
[data-theme="light"] .timeline__timestamp {
  color: var(--text-muted);   /* #64748B */
}

/* ── Actor ── */
.timeline__actor {
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--text-primary);
}

.timeline__actor-role {
  font-weight: 400;
  color: var(--text-secondary);
}

:root .timeline__actor { color: var(--text-primary); }   /* #F1F5F9 */
[data-theme="light"] .timeline__actor { color: var(--text-primary); }   /* #0F172A */

/* ── Category badge ── */
.timeline__badge {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  margin-left: auto;
  flex-shrink: 0;
}

.timeline__badge--config      { color: var(--primary); background: color-mix(in srgb, var(--primary) 12%, transparent); }
.timeline__badge--incident    { color: var(--error);   background: color-mix(in srgb, var(--error)   12%, transparent); }
.timeline__badge--infra       { color: var(--warning); background: color-mix(in srgb, var(--warning) 12%, transparent); }
.timeline__badge--billing     { color: var(--success); background: color-mix(in srgb, var(--success) 12%, transparent); }
.timeline__badge--auth        { color: #8B5CF6;        background: color-mix(in srgb, #8B5CF6 12%, transparent); }
.timeline__badge--exam        { color: #06B6D4;        background: color-mix(in srgb, #06B6D4 12%, transparent); }
.timeline__badge--compliance  { color: #F59E0B;        background: color-mix(in srgb, #F59E0B 12%, transparent); }
.timeline__badge--institution { color: #8B5CF6;        background: color-mix(in srgb, #8B5CF6 12%, transparent); }
.timeline__badge--system      { color: var(--text-muted); background: var(--bg-surface-2); }

/* ── Summary line ── */
.timeline__summary {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0 0 var(--space-1);
}

:root .timeline__summary { color: var(--text-secondary); }       /* #94A3B8 */
[data-theme="light"] .timeline__summary { color: var(--text-secondary); }   /* #475569 */

/* ── Detail block ── */
.timeline__detail {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2) var(--space-4);
  margin-top: var(--space-1);
  padding: var(--space-2) var(--space-3);
  background: var(--bg-surface-2);
  border-left: 2px solid var(--border-subtle);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}

:root .timeline__detail {
  background: var(--bg-surface-2);    /* #131F38 */
  border-left-color: var(--border-subtle);
}

[data-theme="light"] .timeline__detail {
  background: var(--bg-surface-2);    /* #F1F5F9 */
  border-left-color: var(--border-subtle);
}

.timeline__kv {
  font-size: var(--text-xs);
  color: var(--text-secondary);
}

.timeline__kv b {
  color: var(--text-primary);
  font-weight: 600;
}

.timeline__link {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--primary);
  text-decoration: none;
  margin-left: auto;
}

.timeline__link:hover { text-decoration: underline; }

/* ── Date divider ── */
.timeline__date-divider {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin: var(--space-5) 0 var(--space-3);
}

.timeline__date-divider-label {
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  white-space: nowrap;
}

.timeline__date-divider-line {
  flex: 1;
  height: 1px;
  background: var(--border-subtle);
}

/* ── Incident variant (WAR ROOM) ── */
.timeline--incident .timeline__rail {
  background: color-mix(in srgb, var(--error) 40%, transparent);
  width: 2px;
}

.timeline--incident.timeline--resolved .timeline__rail {
  background: color-mix(in srgb, var(--success) 40%, transparent);
}

.timeline--incident .timeline__delta {
  font-size: var(--text-xs);
  font-family: var(--font-mono);
  color: var(--text-muted);
  padding-left: var(--space-8);
  margin: var(--space-1) 0;
  opacity: 0.7;
}

/* ── Milestone nodes (incident) ── */
.timeline__node--milestone {
  width: 14px; height: 14px;
  border-radius: var(--radius-sm);
  background: var(--error);
  border-color: var(--error);
}

.timeline__node--milestone-resolve {
  background: var(--success);
  border-color: var(--success);
}

/* ── Load more button ── */
.timeline__load-more {
  align-self: center;
  margin-top: var(--space-4);
  padding: var(--space-2) var(--space-5);
  background: transparent;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: border-color 150ms, color 150ms;
}

.timeline__load-more:hover {
  border-color: var(--primary);
  color: var(--primary);
}

[data-theme="light"] .timeline__load-more {
  border-color: var(--border-default);
  color: var(--text-secondary);
}

/* ── Compact variant ── */
.timeline--compact .timeline__entry {
  padding: var(--space-1) 0 var(--space-2);
}
.timeline--compact .timeline__detail { display: none; }
.timeline--compact .timeline__summary {
  font-size: var(--text-xs);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.timeline--compact .timeline__rail { min-height: 8px; }
.timeline--compact .timeline__node {
  width: 8px; height: 8px;
}

/* ── Empty state ── */
.timeline__empty {
  text-align: center;
  padding: var(--space-10) var(--space-5);
  color: var(--text-muted);
}
.timeline__empty-icon {
  font-size: 2rem;
  margin-bottom: var(--space-3);
  opacity: 0.4;
}
.timeline__empty-text { font-size: var(--text-sm); }
```

---

## 6. Real-Time Streaming Behavior

> When the Timeline is connected to a WebSocket, new events arrive and are inserted at the top of the feed. The entry slides down with an animation. If the user has scrolled down more than 200px, a "Jump to latest" pill button appears instead of auto-scrolling (avoiding unwanted position jumps).

```javascript
// Pseudocode — component JS layer
socket.on('activity:event', (event) => {
  const entry = renderEntry(event);
  entry.classList.add('timeline__entry--new');

  const container = document.querySelector('.timeline');
  const scrolledAway = container.scrollTop > 200;

  if (scrolledAway) {
    pendingNewEntries.push(event);
    showJumpToLatest(pendingNewEntries.length);
  } else {
    container.prepend(entry);
  }
});
```

**"Jump to latest" pill:**
```css
.timeline__jump-latest {
  position: sticky;
  top: var(--space-3);
  z-index: var(--z-sticky);
  align-self: center;
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: var(--primary);
  color: white;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 700;
  cursor: pointer;
  box-shadow: var(--shadow-lg);
  animation: timeline-entry-in 200ms ease-out;
}
```

---

## 7. Dark + Light Theme Token Reference

| Property | Dark value | Light value |
|---|---|---|
| Rail color | `--border-subtle` → `#1E293B` | `--border-subtle` → `#E2E8F0` |
| Node background | `--bg-base` → `#070C18` | `--bg-base` → `#F8FAFC` |
| Summary text | `--text-secondary` → `#94A3B8` | `--text-secondary` → `#475569` |
| Actor text | `--text-primary` → `#F1F5F9` | `--text-primary` → `#0F172A` |
| Timestamp text | `--text-muted` → `#64748B` | `--text-muted` → `#64748B` |
| Detail block bg | `--bg-surface-2` → `#131F38` | `--bg-surface-2` → `#F1F5F9` |
| Detail block border | `--border-subtle` → `#1E293B` | `--border-subtle` → `#E2E8F0` |
| Date divider line | `--border-subtle` | `--border-subtle` |
| Config badge | `--primary` indigo | `--primary` indigo |
| Incident badge/rail | `--error` red | `--error` red |
| Infra badge | `--warning` amber | `--warning` amber |
| Billing badge | `--success` green | `--success` green |

---

## 8. Usage Examples (for Page Specs)

```markdown
### Section: Activity Feed
> Uses the Timeline component (Component 11, §3.2 Detailed Feed) with WebSocket streaming.
> Events are categorized using the badge system (§2) — CONFIG changes appear in indigo, INCIDENT
> updates in red. Supports real-time "Jump to latest" pill (§6) during active incidents.
> On the WAR ROOM page, uses the Incident variant (§3.4) with red rail and delta timestamps.
```

---

*Component: `11-timeline.md` | Scope: Global | Theme: Dark (default) + Light | Updated: 2026-03*
