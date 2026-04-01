# div-a-15 — Scheduled Maintenance

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Scheduled maintenance windows/month | 2–4 |
| Typical duration | 30 min – 4 hours |
| Advance notice required (SLA) | Standard: 48h · Professional: 72h · Enterprise: 7 days |
| Institutions to notify | Up to 2,050 |
| Students affected per window | Up to 500,000 |
| Preferred maintenance window | Sun 2:00 AM – 6:00 AM IST |
| Blackout periods | Exam season (Oct–Nov, Feb–Mar) |

**Why this matters:** A surprise maintenance window during an exam blocks 500,000 students. The Scheduled Maintenance page manages the full lifecycle: plan → notify → execute → confirm complete. Enterprise SLAs require 7-day advance notice. Missing this is a contractual breach.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Scheduled Maintenance |
| Route | `/exec/maintenance/` |
| Django view | `ScheduledMaintenanceView` |
| Template | `exec/scheduled_maintenance.html` |
| Priority | P1 |
| Nav group | Operations |
| Required role | `exec`, `superadmin`, `ops` |
| 2FA required | Creating / cancelling maintenance |
| HTMX poll | Upcoming maintenance strip: every 5 min |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Scheduled Maintenance              [+ New Maintenance Window]        │
├──────────────────────────────────────────────────────────────────────────────┤
│ ⚠ UPCOMING: Database migration — Sun 23 Mar 02:00–04:00 IST · 4 days away  │
├──────────┬──────────┬──────────┬──────────┬──────────────────────────────── ┤
│ Upcoming │ This     │ Notified │ Blackout │  Avg Duration                   │
│    3     │ Month    │    2     │  Conflict│  2h 14m                         │
│          │    2     │          │    1     │                                  │
├──────────┴──────────┴──────────┴──────────┴──────────────────────────────── ┤
│ TABS: [Upcoming] [History] [Blackout Periods] [Notification Templates]      │
├──────────────────────────────────────────────────────────────────────────────┤
│ # │ Title          │ Scheduled    │ Duration │ Services │ Notified │ Status  │
│ 1 │ DB migration   │ Sun 23 Mar   │ 2h       │ Database │ ✓ Yes    │ Planned │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 Upcoming Maintenance Banner

Shows when any maintenance is within 7 days.
`bg-[#451A03] border border-[#FCD34D] rounded-xl p-4 mx-4 mb-2`
`⚠ UPCOMING: {title} — {date} {time} IST · {N} days away`
**Poll:** `hx-trigger="every 300s"` `hx-swap="outerHTML"`

---

### 4.2 KPI Strip

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Upcoming | Count of future maintenance windows | — |
| 2 | This Month | Scheduled this calendar month | — |
| 3 | Notified | Upcoming with notifications already sent | — |
| 4 | Blackout Conflict | Upcoming windows overlapping a blackout | > 0 = red |
| 5 | Avg Duration | Average actual duration (last 12) | > 4h = amber |

---

### 4.3 Tab: Upcoming

`id="tab-upcoming"` · `hx-get="?part=upcoming"`

**Maintenance Table:**

| Column | Width | Detail |
|---|---|---|
| # | 48px | MAINT-XXXX |
| Title | 240px | Name · click → drawer |
| Scheduled Start | 140px | Date + time IST |
| Scheduled End | 140px | Date + time IST |
| Duration | 80px | Calculated |
| Services | 160px | Badge list |
| Impact | 100px | Full / Partial / Minimal |
| Notified | 80px | ✓ Yes / ⚠ No |
| SLA Req | 100px | "7d advance" for Enterprise |
| Status | 100px | Draft / Planned / Notified / In Progress / Completed / Cancelled |
| Actions ⋯ | 48px | View/Edit / Send Notifications / Cancel / Mark Complete |

**Blackout conflict row:** `bg-[#1A0A0A]` tint + `⚠` icon in title cell + tooltip "Overlaps exam season blackout"

---

### 4.4 Tab: History

`id="tab-history"` · `hx-get="?part=history"`

Same table as upcoming but for past maintenance. Extra columns:
- Actual Start / Actual End / Actual Duration
- Status: Completed / Overran / Cancelled
- Post-maintenance notes

**Overran rows:** amber tint if actual duration > scheduled duration

---

### 4.5 Tab: Blackout Periods

`id="tab-blackouts"` · `hx-get="?part=blackouts"`

**Purpose:** Define periods when maintenance is forbidden (exam season, national holidays).

**Blackout Calendar:** month-view calendar with blackout days highlighted red `bg-[#450A0A]`

**Blackout Periods Table:**
| Period | Start | End | Reason | Type |
|---|---|---|---|---|
| Board Exam Season | 15 Oct | 30 Nov | Class 10/12 board exams | Annual |
| Final Exams | 15 Feb | 31 Mar | Year-end exams | Annual |
| Independence Day | 15 Aug | 15 Aug | National holiday | Annual |

**[+ Add Blackout Period]** button → simple form: name, start date, end date, reason, recurring toggle

---

### 4.6 Tab: Notification Templates

`id="tab-templates"` · `hx-get="?part=templates"`

**Templates list:**
- "7-day advance notice (Enterprise)"
- "48-hour advance notice (Standard)"
- "1-day reminder"
- "Maintenance started"
- "Maintenance completed"

Each template card: name + channels (email/SMS/status page) + [Edit] [Preview] [Test]

**Edit template:** markdown editor with variables: `{{title}}` `{{start_time}}` `{{end_time}}` `{{affected_services}}` `{{duration}}`

---

## 5. Drawers

### 5.1 Maintenance Detail / Edit Drawer (640 px)

`id="maintenance-drawer"` · `body.drawer-open`

**Header:** MAINT-XXXX · Status badge · Title · `[×]`

**Tab bar (3 tabs):** Details · Notifications · History

**Tab A — Details:**
| Field | Type | Detail |
|---|---|---|
| Title | Text | Required |
| Description | Textarea markdown | Full description of work |
| Affected services | Multi-select checkboxes | Auth / Database / Exam Engine / etc. |
| Impact level | Select | Full outage / Degraded / Minimal |
| Scheduled start | Datetime picker | IST timezone |
| Scheduled end | Datetime picker | Must be > start |
| Runbook | URL | Optional |
| Notify institutions | Toggle | Default: On |
| Status | Select (if editing existing) | |

**Blackout check:** on date change, `hx-get="?part=blackout_check&start={dt}&end={dt}"` · shows warning if overlap

**Footer:** [Cancel] [Save Changes] · 2FA enforced for create/save

**Tab B — Notifications:**
- Notification timeline: when each type of notification will fire (auto-calculated)
- [Send Now] button per notification type
- Log of notifications already sent

**Tab C — History:**
- Status change log: who changed what + timestamp
- Notes field per status change

---

## 6. Modals

### 6.1 New Maintenance Window Modal (560 px)

**2FA required.**
Same fields as §5.1 Tab A.
**Footer:** [Cancel] [Save as Draft] [Schedule & Notify]

---

### 6.2 Cancel Maintenance Modal (480 px)

**2FA required.**
"Cancel {title} scheduled for {date}?"
| Field | Type |
|---|---|
| Reason | Textarea (required) |
| Notify institutions | Checkbox (default: checked) |

**Footer:** [Cancel] [Confirm Cancellation]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/maint_kpi.html` | Page load · poll 5 min |
| `?part=banner` | `exec/partials/maint_banner.html` | Poll 5 min |
| `?part=upcoming` | `exec/partials/maint_upcoming.html` | Tab click |
| `?part=history` | `exec/partials/maint_history.html` | Tab click |
| `?part=blackouts` | `exec/partials/maint_blackouts.html` | Tab click |
| `?part=templates` | `exec/partials/maint_templates.html` | Tab click |
| `?part=maintenance_drawer&id={id}` | `exec/partials/maint_drawer.html` | Row click |
| `?part=blackout_check` | JSON `{conflict: bool}` | Date change in form |

**Django view dispatch:**
```python
class ScheduledMaintenanceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.manage_maintenance"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/maint_kpi.html",
                "banner": "exec/partials/maint_banner.html",
                "upcoming": "exec/partials/maint_upcoming.html",
                "history": "exec/partials/maint_history.html",
                "blackouts": "exec/partials/maint_blackouts.html",
                "templates": "exec/partials/maint_templates.html",
                "maintenance_drawer": "exec/partials/maint_drawer.html",
            }
            if part == "blackout_check":
                return self._handle_blackout_check(request)
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/scheduled_maintenance.html", ctx)
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 200 ms | > 500 ms |
| Upcoming table | < 300 ms | > 800 ms |
| Maintenance drawer | < 250 ms | > 700 ms |
| Blackout check | < 100 ms | > 300 ms |
| Full page initial load | < 800 ms | > 2 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Maintenance window overlaps blackout | Red warning in drawer + row tint; cannot schedule without override |
| Enterprise notification not sent 7 days before | Amber badge "SLA notification overdue" on row |
| Maintenance overruns | Status auto-set to "Overran" when actual end > scheduled end |
| Maintenance during peak exam hours (6AM–10PM IST) | Warning "Maintenance during peak hours will affect up to 500,000 active students" |
| Cancel after notifications sent | Cancellation notification auto-sent to all previously notified institutions |
| 0 upcoming maintenance | Empty state: "No maintenance scheduled" + [+ Schedule Maintenance] CTA |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `N` | New maintenance window |
| `1`–`4` | Switch tabs |
| `↑` / `↓` | Navigate rows |
| `Enter` | Open drawer |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/scheduled_maintenance.html` | Full page shell |
| `exec/partials/maint_kpi.html` | KPI strip |
| `exec/partials/maint_banner.html` | Upcoming banner |
| `exec/partials/maint_upcoming.html` | Upcoming maintenance table |
| `exec/partials/maint_history.html` | History table |
| `exec/partials/maint_blackouts.html` | Blackout periods tab |
| `exec/partials/maint_templates.html` | Notification templates tab |
| `exec/partials/maint_drawer.html` | Maintenance detail/edit drawer |
| `exec/partials/new_maintenance_modal.html` | New window modal |
| `exec/partials/cancel_maintenance_modal.html` | Cancel confirmation |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.2 |
| `UpcomingBanner` | §4.1 |
| `TabBar` | §4.3–4.6 |
| `MaintenanceTable` | §4.3, §4.4 |
| `BlackoutCalendar` | §4.5 |
| `BlackoutPeriodsTable` | §4.5 |
| `NotificationTemplateCard` | §4.6 |
| `MarkdownEditor` | §4.6 template edit |
| `DrawerPanel` | §5.1 |
| `DatetimePicker` | §5.1 fields |
| `ModalDialog` | §6.1–6.2 |
| `PaginationStrip` | History table |
