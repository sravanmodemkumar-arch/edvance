# div-a-14 — Alerting Rules

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total alerting rules | ~80–120 active rules |
| Alert channels | PagerDuty / Email / SMS / Slack / Webhook |
| Rules per service | 5–15 |
| Alert fires/day (platform avg) | ~20–50 |
| Silences active at any time | 0–5 |
| On-call rotation members | 4–8 engineers |
| Runbook links per rule | 0–3 |

**Why this matters:** Alerting Rules is the platform's nervous system configuration. A misconfigured threshold means either alert fatigue (too noisy) or missed incidents (too quiet). The ops team manages rules here. Every rule change is audited.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Alerting Rules |
| Route | `/exec/alerting/` |
| Django view | `AlertingRulesView` |
| Template | `exec/alerting_rules.html` |
| Priority | P1 |
| Nav group | Operations |
| Required role | `exec`, `superadmin`, `ops` |
| 2FA required | Creating / editing / deleting rules |
| HTMX poll | Alert status column: every 30s |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Alerting Rules              [+ New Rule] [Silences ▾] [Test All]    │
├──────────┬──────────┬──────────┬──────────┬──────────────────────────────── ┤
│  Total   │ Active   │ Firing   │ Silenced │  Channels                       │
│  Rules   │ Rules    │ Now      │          │  Configured                     │
│   94     │   88     │    3     │    2     │  5                              │
├──────────┴──────────┴──────────┴──────────┴──────────────────────────────── ┤
│ [🔍 Search rules...]                                                         │
│ [Service ▾] [Severity ▾] [Channel ▾] [Status ▾]                            │
├──────────────────────────────────────────────────────────────────────────────┤
│ TABS: [All Rules] [Currently Firing] [Silences] [Channels] [Alert History]  │
├──────────────────────────────────────────────────────────────────────────────┤
│ Rule Name       │ Service  │ Sev │ Condition           │ Status  │ ⋯       │
│ High error rate │ Auth     │ P0  │ error_rate > 5%     │ 🔴 Firing│         │
│ Slow query      │ Database │ P1  │ p95_latency > 500ms │ ✓ OK    │         │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Total Rules | All rules (active + disabled) | — |
| 2 | Active Rules | Enabled rules | — |
| 3 | Firing Now | Rules currently in firing state | > 5 = red |
| 4 | Silenced | Rules currently silenced | > 10 = amber |
| 5 | Channels Configured | Distinct alert channels | — |

---

### 4.2 Tab: All Rules

`id="tab-all-rules"` · `hx-get="?part=rules_table"`

**Search + filters:**
- Search: debounced 400ms on rule name / condition text
- Filters: Service · Severity (P0/P1/P2/P3) · Channel · Status (Active/Disabled/Firing/Silenced)

**Rules Table:**

| Column | Width | Detail |
|---|---|---|
| Rule Name | 220px | Name · click → opens Rule Drawer |
| Service | 120px | Service badge |
| Severity | 70px | P0/P1/P2/P3 badge |
| Condition | 240px | e.g., `error_rate > 5% for 2m` · monospace |
| Channels | 120px | Icons: 📧 email / 📱 SMS / 🔔 PD / 💬 Slack |
| Last Fired | 100px | Relative time or "Never" |
| Status | 110px | 🔴 Firing / ✓ OK / 🔇 Silenced / ⚪ Disabled |
| Actions ⋯ | 48px | Edit / Disable / Silence / Test / Delete |

**Firing rows:** `bg-[#1A0A0A]` tint · status cell pulses

**Sort:** Status (Firing first) then by Service, then Name

**Pagination:** 25/page · poll status column every 30s via `hx-swap-oob` on status cells

---

### 4.3 Tab: Currently Firing

`id="tab-firing"` · `hx-get="?part=firing_rules"` · `hx-trigger="load, every 30s"`

Filtered view showing only rules in Firing state with:
- Time firing (live counter)
- Notification count (how many alerts sent)
- [Silence for 1h] quick action button per row
- [Create Incident] quick action → pre-fills New Incident modal from rule metadata

---

### 4.4 Tab: Silences

`id="tab-silences"` · `hx-get="?part=silences"`

**[+ New Silence]** button

| Column | Detail |
|---|---|
| Silence ID | `SIL-XXXX` |
| Rules silenced | N rules matching pattern |
| Created by | Username |
| Starts at | Datetime |
| Ends at | Datetime |
| Reason | Text |
| Status | Active / Expired / Upcoming |
| Actions ⋯ | Expire Now / Extend / Delete |

**New Silence Modal (480px):**
- Rule selector (search + multi-select)
- Start datetime (default: now)
- Duration: 1h / 4h / 8h / 24h / Custom
- Reason: required text

---

### 4.5 Tab: Channels

`id="tab-channels"` · `hx-get="?part=channels"`

**Channel configuration cards (grid):**

```
┌─────────────────────────────┐
│ 📧 Email                    │
│ Configured                  │
│ Alerts sent (30d): 142      │
│ Failure rate: 0.2%          │
│ [Edit Config] [Test]        │
└─────────────────────────────┘
```

Channels: Email · SMS (Twilio) · PagerDuty · Slack · Webhook

**Edit config:** opens Channel Config Drawer (480px) with channel-specific fields (API keys, webhook URLs, etc.)

**[Test]:** sends test alert to channel · shows result inline

---

### 4.6 Tab: Alert History

`id="tab-history"` · `hx-get="?part=alert_history"`

Chronological log of all alert fires.

| Column | Detail |
|---|---|
| Timestamp | Absolute · most recent first |
| Rule | Rule name |
| Severity | Badge |
| Value at fire | e.g., "error_rate: 7.2%" |
| Duration | How long it fired |
| Resolved at | Datetime |
| Linked Incident | INC-XXXX or `—` |
| Notifications | Count sent |

**Filter:** Rule / Service / Severity / Date range
**Pagination:** 50/page

---

## 5. Drawers

### 5.1 Rule Detail / Edit Drawer (640 px)

`id="rule-drawer"` · `body.drawer-open` · **2FA required to save.**

**Header:** Rule name + service badge + severity badge · `[×]`

**Tab bar (3 tabs):** Configuration · History · Runbooks

**Tab A — Configuration:**
| Field | Type | Detail |
|---|---|---|
| Rule name | Text | Required |
| Service | Select | Auth / Database / Exam Engine / etc. |
| Severity | Select | P0 / P1 / P2 / P3 |
| Metric | Select from catalogue | e.g., `error_rate`, `p95_latency` |
| Condition | Expression builder | `metric` `operator` `threshold` `for` `duration` |
| Evaluation interval | Select | 10s / 30s / 1m / 5m |
| Notification channels | Multi-select | Email / SMS / PagerDuty / Slack / Webhook |
| Notify repeat interval | Select | 0 (once) / 5m / 15m / 30m / 1h |
| Runbooks | URL list (repeatable) | Optional |
| Enabled | Toggle | `accent-[#6366F1]` |
| Description | Textarea | Optional |

**Condition expression builder (inline):**
```
[ error_rate  ▾ ] [ > ▾ ] [ 5 ] [ % ] for [ 2 ] [ minutes ▾ ]
```
Input fields inline `bg-[#131F38] border border-[#1E2D4A] rounded px-2 py-1`

**[Test Rule]** button: evaluates current condition against live metrics · shows result "Would fire: YES (current value: 7.2%)" or "Would fire: NO (current value: 0.8%)"

**Tab B — History:**
Last 20 fire events for this rule. Same columns as §4.6 but filtered.

**Tab C — Runbooks:**
List of linked runbook URLs with title + description. [+ Add Runbook] / [Remove]

**Footer:** [Cancel] [Save Rule] (2FA enforced)

---

## 6. Modals

### 6.1 New Alerting Rule Modal (640 px)

Same fields as §5.1 Tab A. **2FA required.**
**Footer:** [Cancel] [Create Rule]

---

### 6.2 Delete Rule Confirmation Modal (480 px)

**2FA required.**
"Delete rule '{Rule Name}'?"
Warning: "This rule has fired {N} times in the last 30 days and is linked to {M} incidents."
**Footer:** [Cancel] [Delete Rule]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/alert_kpi.html` | Page load |
| `?part=rules_table` | `exec/partials/alert_rules_table.html` | Tab · search · filter · poll 30s |
| `?part=firing_rules` | `exec/partials/alert_firing.html` | Tab · poll 30s |
| `?part=silences` | `exec/partials/alert_silences.html` | Tab click |
| `?part=channels` | `exec/partials/alert_channels.html` | Tab click |
| `?part=alert_history` | `exec/partials/alert_history.html` | Tab · filter |
| `?part=rule_drawer&id={id}` | `exec/partials/rule_drawer.html` | Row click |

**Django view dispatch:**
```python
class AlertingRulesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.manage_alerting"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/alert_kpi.html",
                "rules_table": "exec/partials/alert_rules_table.html",
                "firing_rules": "exec/partials/alert_firing.html",
                "silences": "exec/partials/alert_silences.html",
                "channels": "exec/partials/alert_channels.html",
                "alert_history": "exec/partials/alert_history.html",
                "rule_drawer": "exec/partials/rule_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/alerting_rules.html", ctx)

    def post(self, request):
        part = request.GET.get("part", "")
        handlers = {
            "create_rule": self._handle_create,
            "save_rule": self._handle_save,
            "delete_rule": self._handle_delete,
            "create_silence": self._handle_silence,
        }
        if part in handlers:
            return handlers[part](request)
        return HttpResponseNotAllowed(["GET"])
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 200 ms | > 500 ms |
| Rules table (94 rows) | < 400 ms | > 1 s |
| Firing tab (real-time) | < 200 ms | > 500 ms |
| Rule drawer | < 250 ms | > 700 ms |
| Test rule evaluation | < 500 ms | > 2 s |
| Full page initial load | < 800 ms | > 2 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Rule fires during editing | Toast "This rule is currently firing" + highlight |
| All rules silenced | Banner "All alerting rules are silenced" amber warning |
| Channel test fails | Toast "PagerDuty test failed: API key invalid" red error |
| Rule with no channel | Warning badge "No notification channel — rule fires silently" |
| Duplicate rule condition | Warning "A similar rule already exists: {name}" |
| Delete rule currently firing | Additional confirmation: "This rule is currently firing. Deleting it will not auto-resolve the alert." |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `N` | New rule |
| `F` | Focus search |
| `1`–`5` | Switch tabs |
| `↑` / `↓` | Navigate rows |
| `Enter` | Open rule drawer |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/alerting_rules.html` | Full page shell |
| `exec/partials/alert_kpi.html` | KPI strip |
| `exec/partials/alert_rules_table.html` | Rules table |
| `exec/partials/alert_firing.html` | Currently firing tab |
| `exec/partials/alert_silences.html` | Silences tab + table |
| `exec/partials/alert_channels.html` | Channels tab |
| `exec/partials/alert_history.html` | Alert history table |
| `exec/partials/rule_drawer.html` | Rule detail/edit drawer |
| `exec/partials/new_rule_modal.html` | New rule modal |
| `exec/partials/new_silence_modal.html` | New silence modal |
| `exec/partials/delete_rule_modal.html` | Delete confirmation |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `SearchInput` | §4.2 |
| `RulesTable` | §4.2 |
| `SeverityBadge` | §4.2, §5.1 |
| `StatusIndicator` | §4.2 Status column |
| `FiringRulesTable` | §4.3 |
| `SilencesTable` | §4.4 |
| `ChannelCard` | §4.5 |
| `AlertHistoryTable` | §4.6 |
| `DrawerPanel` | §5.1 |
| `ConditionExpressionBuilder` | §5.1 Tab A |
| `TabBar` | §5.1 drawer + page |
| `ModalDialog` | §6.1–6.2 |
| `PaginationStrip` | Tables |
| `PollableContainer` | Rules table status column |
