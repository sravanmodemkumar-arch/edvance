# div-a-13 — Incident Detail

## 1. Platform Scale Reference

Same as div-a-12. Key figures for single incident context:

| Dimension | Value |
|---|---|
| Max institutions affected per P0 | 2,050 |
| Max students affected per P0 | 500,000 (peak concurrent) |
| Timeline events per incident | 5–50 updates |
| Post-mortem avg length | 800–2,000 words |
| Runbook links per incident | 1–5 |

**Why this matters:** The Incident Detail page is the single source of truth during and after a crisis. The incident commander updates it in real-time; affected institutions link their escalations to it; the post-mortem is drafted here. This page must load in < 500ms even during a P0 when servers are under stress.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Incident — {INC-XXXX}: {Title} |
| Route | `/exec/incidents/<incident_id>/` |
| Django view | `IncidentDetailView` |
| Template | `exec/incident_detail.html` |
| Priority | P0 |
| Nav group | Operations |
| Required role | `exec`, `superadmin`, `ops`, `oncall` |
| 2FA required | Closing incident / Publishing post-mortem |
| HTMX poll | Timeline: every 10s · KPI strip: every 30s |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ← Incidents   INC-0041: Auth service degraded                               │
│               [P0] [● Ongoing — 24 min]                                     │
│               Auth · Started 14:32 · Commander: oncall-engineer             │
│               [Update Status ▾] [Add Update] [Assign] [PagerDuty →] [Close]│
├──────────┬──────────┬──────────┬──────────────────────────────────────────── ┤
│ Duration │ Affected │ SLA      │ Status                                      │
│  24 min  │ 24K stud │ BREACHED │ Investigating                               │
├──────────┴──────────┴──────────┴──────────────────────────────────────────── ┤
│ TABS: [Overview] [Timeline] [Affected] [Communication] [Post-Mortem]        │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: OVERVIEW                                                                │
│ [Summary markdown block]                          [Affected Services]       │
│ Root Cause: (being investigated)                  ● Auth Service            │
│ Commander: oncall-engineer                         ● API Gateway             │
│ Runbooks: [Auth Runbook →] [Gateway Runbook →]                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Page Header

### 4.1 Breadcrumb + Identity Row

**Breadcrumb:** `← Incidents` links to div-a-12 · `text-sm text-[#6366F1]`

**Identity block:**
```
INC-0041: Auth service degraded
[P0 badge]  [● Ongoing badge — 24 min]
Auth · Started 14:32 IST, 15 Mar 2025 · Incident Commander: oncall-engineer
```

**Action buttons:**
- [Update Status ▾] dropdown: Investigating / Mitigating / Resolved / Monitoring
- [Add Update] → inline form overlay (see §6.2)
- [Assign] → User picker dropdown
- [PagerDuty →] external link to PagerDuty incident
- [Close Incident] → requires 2FA · shows resolution form

---

### 4.2 KPI Strip

4 cards · poll every 30s

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Duration | Live counter `24:38` (mm:ss) | > 60 min P0 = red |
| 2 | Affected | "24,000 students · 312 institutions" | — |
| 3 | SLA Status | Breached / At Risk / Safe | Breached = red |
| 4 | Status | Investigating / Mitigating / Resolved | Ongoing = red |

**Duration counter:** `data-incident-start="{iso}"` → JavaScript `setInterval(1000)` updates display

---

## 5. Tab: Overview

`id="tab-overview"` · `hx-get="?part=overview&incident_id={id}"`

**Layout:** `grid grid-cols-3 gap-4 p-4`

**Left (2 cols) — Summary block:**
`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-6`
- **Summary:** rendered markdown · editable by ops/exec via [Edit ✎] pencil toggle
- **Root cause:** text field · "Under investigation" until populated
- **Incident commander:** avatar + name + badge
- **Runbook links:** list of linked runbooks (external URLs)

**Right (1 col) — Affected Services:**
`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4`
Checklist per service:
```
● Auth Service         [Critical]
● API Gateway          [Degraded]
○ Database             [Normal]
○ Exam Engine          [Normal]
```
Dot colours: `#EF4444` Critical · `#F59E0B` Degraded · `#34D399` Normal

**Below grid — Incident metadata table:**
Two-column grid of key/value pairs:
| Key | Value |
|---|---|
| Incident ID | INC-0041 |
| Severity | P0 |
| Status | Investigating |
| Created by | PagerDuty (auto-detect) |
| Created at | 14:32:05 IST |
| Detected via | Error rate alert (auth-service) |
| Last updated | 14:55:30 IST |
| Linked incidents | INC-0039 (related) |

---

## 6. Tab: Timeline

`id="tab-timeline"` · `hx-get="?part=incident_timeline&incident_id={id}"`
**Poll:** `hx-trigger="every 10s[!document.querySelector('.modal-open')]"`

### 6.1 Event Timeline

Full-height vertical timeline. **Newest events at top.**

**Event item anatomy:**
```
14:55:30  ┤● [Status changed to Mitigating] by oncall-engineer
          │  "Deployed auth-service hotfix to prod. Monitoring error rates."
          │
14:47:22  ┤● [Update] by oncall-engineer
          │  "Root cause identified: Redis cache flush caused auth token
          │   validation failures. Fix being deployed."
          │
14:35:00  ┤● [Status changed to Investigating → Mitigating] by system
          │
14:33:18  ┤● [Assigned] to oncall-engineer by PagerDuty
          │
14:32:05  ┤● [Incident created] by PagerDuty auto-detection
```

**Timeline item styling:**
- Timestamp: `text-xs text-[#64748B] font-mono w-20 flex-shrink-0`
- Dot: `w-3 h-3 rounded-full` · Status change: `bg-[#6366F1]` · Update: `bg-[#22D3EE]` · System: `bg-[#475569]`
- Text: `text-sm text-white font-medium` (event type) + `text-sm text-[#94A3B8]` (detail)
- Connector line: `border-l border-[#1E2D4A] ml-1.5 pl-4`

### 6.2 Add Update (inline form)

Triggered by [Add Update] header button. Expands below timeline header (not a modal — must stay in-page during P0).

```
┌─────────────────────────────────────────────────────────────┐
│ Add Incident Update                                         │
│ Status: [Keep current ▾]  [Investigating ▾]                 │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Describe the update... (markdown supported)             │ │
│ └─────────────────────────────────────────────────────────┘ │
│ [☐] Notify affected institutions                            │
│ [☐] Update status page                                      │
│ [Cancel]  [Post Update]                                     │
└─────────────────────────────────────────────────────────────┘
```

**POST:** `hx-post="?part=add_update&incident_id={id}"` · on success: new event prepended to timeline via `hx-swap="afterbegin"` on timeline container

---

## 7. Tab: Affected

`id="tab-affected"` · `hx-get="?part=affected&incident_id={id}"`

### 7.1 Impact Summary Row

`flex gap-6 p-4`
- Institutions affected: `312 of 2,050`
- Students estimated: `24,000`
- SLA tier breakdown: Enterprise `45` · Professional `82` · Standard `185`
- Geographic: States affected: `Telangana, AP, Karnataka, TN`

### 7.2 Affected Institutions Table

| Column | Detail |
|---|---|
| Institution | Name + type icon |
| SLA Tier | Badge (Enterprise first) |
| Impact Level | Critical / Degraded / Minor |
| Students affected | Count |
| Last notified | Relative time |
| Status | Affected / Recovered |
| Actions ⋯ | Send direct notification / View institution |

**Sort:** SLA tier Enterprise first, then by student count desc
**Filter:** SLA tier · Impact level · Status

---

## 8. Tab: Communication

`id="tab-communication"` · `hx-get="?part=communication&incident_id={id}"`

### 8.1 Communications Table

| Column | Detail |
|---|---|
| Channel | Email / SMS / PagerDuty / Status Page / Slack |
| Recipients | Count or "All affected institutions" |
| Sent at | Timestamp |
| Message | Truncated preview · [View full] |
| Status | Sent / Delivered / Failed |

**[Send Communication]** button → opens Send Communication Modal (§9.1)

### 8.2 Status Page Updates

List of status page updates sent during this incident (title, message, timestamp)

---

## 9. Tab: Post-Mortem

`id="tab-postmortem"` · `hx-get="?part=postmortem&incident_id={id}"`

**States:**
- Not started: "Post-mortem due by {date (resolution + 5 days)}" + [Start Post-Mortem]
- Draft: editable markdown document
- Published: read-only rendered view + [Edit] + [Export PDF]

**Post-mortem template sections (auto-filled from incident data):**

### Post-Mortem: INC-0041

**Incident Summary**
[Auto-filled: title, severity, duration, affected]

**Timeline of Events**
[Auto-filled from event timeline]

**Root Cause Analysis**
[Manual entry required]

**Contributing Factors**
[Manual entry]

**Impact Assessment**
[Auto-filled: affected institutions + students]

**Resolution**
[Auto-filled from resolution update]

**Action Items**
| Item | Owner | Due Date | Status |
| Fix Redis eviction policy | DevOps | Mar 20 | Open |
[+ Add action item]

**Editor:** markdown textarea with preview toggle · `min-h-[400px]`
**[Save Draft]** · **[Publish Post-Mortem]** (requires 2FA · notifies affected institutions)

---

## 10. Modals

### 10.1 Send Communication Modal (560 px)

| Field | Type | Detail |
|---|---|---|
| Channel | Multi-select | Email / SMS / Status Page |
| Recipients | Select | All affected / Enterprise only / Custom list |
| Subject | Text | Required (email only) |
| Message | Textarea markdown | Required |
| Schedule | Radio | Now / Schedule for later |
| Scheduled at | Datetime picker | Shown if scheduled |

**Footer:** [Cancel] [Preview] [Send]

---

### 10.2 Close Incident Modal (480 px)

**2FA required.**

| Field | Type |
|---|---|
| Resolution summary | Textarea (required) |
| Root cause (brief) | Text (required) |
| Notify affected institutions | Checkbox (default: checked) |
| Update status page | Checkbox |
| Post-mortem required | Checkbox (auto-checked for P0/P1) |
| Post-mortem due date | Date picker |

**Footer:** [Cancel] [Close Incident]

---

## 11. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/inc_detail_kpi.html` | Page load · poll 30s |
| `?part=overview` | `exec/partials/inc_overview.html` | Tab click |
| `?part=incident_timeline` | `exec/partials/inc_timeline.html` | Tab click · poll 10s |
| `?part=affected` | `exec/partials/inc_affected.html` | Tab click |
| `?part=communication` | `exec/partials/inc_communication.html` | Tab click |
| `?part=postmortem` | `exec/partials/inc_postmortem.html` | Tab click |
| `?part=add_update` | POST → prepend event | Add Update form submit |
| `?part=update_status` | POST → reload kpi + timeline | Status change |
| `?part=close_incident` | POST | Close incident modal |
| `?part=save_postmortem` | POST | Post-mortem save |

**Django view dispatch:**
```python
class IncidentDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_incidents"

    def get(self, request, incident_id):
        incident = get_object_or_404(Incident, pk=incident_id)
        ctx = self._build_context(request, incident)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/inc_detail_kpi.html",
                "overview": "exec/partials/inc_overview.html",
                "incident_timeline": "exec/partials/inc_timeline.html",
                "affected": "exec/partials/inc_affected.html",
                "communication": "exec/partials/inc_communication.html",
                "postmortem": "exec/partials/inc_postmortem.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/incident_detail.html", ctx)

    def post(self, request, incident_id):
        incident = get_object_or_404(Incident, pk=incident_id)
        part = request.GET.get("part", "")
        handlers = {
            "add_update": self._handle_add_update,
            "update_status": self._handle_update_status,
            "close_incident": self._handle_close,
            "save_postmortem": self._handle_save_pm,
        }
        if part in handlers:
            return handlers[part](request, incident)
        return HttpResponseNotAllowed(["GET"])
```

---

## 12. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 150 ms | > 400 ms |
| Overview tab | < 300 ms | > 800 ms |
| Timeline (50 events) | < 250 ms | > 700 ms |
| Add update (POST + prepend) | < 200 ms | > 500 ms |
| Affected table (300 rows) | < 400 ms | > 1 s |
| Full page initial load | < 500 ms | > 1.5 s |

---

## 13. States & Edge Cases

| State | Behaviour |
|---|---|
| Incident already resolved | Header shows green "Resolved — {duration}" · all edit actions disabled except post-mortem |
| Timeline: 100+ events | Paginated timeline (load-more pattern: `hx-get="?part=timeline_page&after={id}"`) |
| Post-mortem published | Read-only rendered view · external link shared with affected institutions |
| Affected: 0 institutions | Shows "Platform internal — no institution impact" |
| PagerDuty link: incident deleted | [PagerDuty →] button shows "PagerDuty incident not found (may be deleted)" |
| Multiple incidents for same service | Shows "Related incidents" section in overview tab |
| Close incident: post-mortem not started | Warning "A post-mortem has not been started. It will be due on {date}." |

---

## 14. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`5` | Switch tabs |
| `U` | Add update (focus inline form) |
| `S` | Update status |
| `Esc` | Close modal / cancel inline form |
| `?` | Keyboard shortcuts help |

---

## 15. Template Files

| File | Purpose |
|---|---|
| `exec/incident_detail.html` | Full page shell |
| `exec/partials/inc_detail_kpi.html` | KPI strip |
| `exec/partials/inc_overview.html` | Overview tab |
| `exec/partials/inc_timeline.html` | Timeline tab (event list) |
| `exec/partials/inc_affected.html` | Affected tab |
| `exec/partials/inc_communication.html` | Communication tab |
| `exec/partials/inc_postmortem.html` | Post-mortem tab |
| `exec/partials/inc_add_update_form.html` | Inline add-update form |
| `exec/partials/send_communication_modal.html` | Send communication modal |
| `exec/partials/close_incident_modal.html` | Close incident modal |

---

## 16. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.2 |
| `LiveDurationCounter` | §4.2 Duration card |
| `TabBar` | §5–9 |
| `MarkdownEditor` | §5 Summary · §9 Post-mortem |
| `MarkdownRenderer` | §9 Published view |
| `EventTimeline` | §6.1 |
| `InlineUpdateForm` | §6.2 |
| `AffectedTable` | §7.2 |
| `CommunicationLog` | §8.1 |
| `ActionItemsChecklist` | §9 Post-mortem |
| `ModalDialog` | §10.1–10.2 |
| `UserPicker` | §4.1 Assign |
| `PollableContainer` | KPI · timeline |
