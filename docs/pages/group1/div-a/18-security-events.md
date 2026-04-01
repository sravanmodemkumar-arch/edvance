# div-a-18 — Security Events

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Security events/day | ~500–2,000 |
| High-severity events/week | ~5–20 |
| Failed login attempts/day | ~1,000–5,000 (mostly bots) |
| IP blocklist entries | ~200–500 active |
| 2FA bypass attempts/month | ~2–5 |
| API key misuse events/month | ~10–30 |
| Brute-force attack blocks/day | ~50–200 |
| SIEM integration | Optional (Splunk/Elastic) |

**Why this matters:** With 2.4M+ student accounts and 120 API keys, the platform is a high-value attack target. Security Events is the SOC (Security Operations Centre) dashboard. Every failed login, IP allowlist violation, privilege escalation, and anomalous API call is recorded here. A breach during a board exam can compromise 500,000 student records.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Security Events |
| Route | `/exec/security/` |
| Django view | `SecurityEventsView` |
| Template | `exec/security_events.html` |
| Priority | P0 |
| Nav group | Compliance |
| Required role | `exec`, `superadmin`, `security`, `ops` |
| 2FA required | Blocking IPs / revoking API keys |
| HTMX poll | Event feed: every 30s |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Security Events              [+ Block IP] [Export] [SIEM Config ▾] │
├────────┬────────┬────────┬────────┬────────┬─────────────────────────────── ┤
│ Events │ High   │ Blocked │ Active │ API Key│  Threat                       │
│ (24h)  │ Sev(7d)│ IPs     │ Threats│ Misuse │  Level                        │
│ 1,847  │   18   │   312   │    2   │    8   │  Medium                       │
├────────┴────────┴────────┴────────┴────────┴─────────────────────────────── ┤
│ TABS: [Event Feed] [IP Blocklist] [Threat Map] [API Anomalies] [Settings]   │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Severity ▾] [Event Type ▾] [IP ▾] [User ▾] [Date Range ▾]                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ Timestamp     │ Type               │ Severity │ Actor    │ IP    │ Details  │
│ 14:32:05      │ brute_force_block  │ High     │ unknown  │ x.x   │ [View]   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Events (24h) | Security events in last 24h | — |
| 2 | High Severity (7d) | High + Critical events in last 7 days | > 50 = red |
| 3 | Blocked IPs | Active IP blocklist entries | — |
| 4 | Active Threats | Currently active threat cases | > 0 = red pulse |
| 5 | API Key Misuse | Events with API key anomalies (7d) | > 10 = amber |
| 6 | Threat Level | Composite: Low / Medium / High / Critical | High = amber · Critical = red |

**Threat Level card:** coloured background:
- Low: `bg-[#064E3B]` · Medium: `bg-[#451A03]` · High: `bg-[#450A0A]` · Critical: `bg-[#450A0A] animate-pulse`

---

### 4.2 Tab: Event Feed

`id="tab-feed"` · `hx-get="?part=security_feed"`
**Poll:** `hx-trigger="every 30s[!document.querySelector('.drawer-open,.modal-open')]"`

**Filters:**
| Filter | Options |
|---|---|
| Severity | All / Critical / High / Medium / Low / Info |
| Event Type | All / Login failures / Brute force / IP violation / 2FA bypass / Privilege escalation / API misuse / Data exfiltration attempt |
| IP Address | Text input (CIDR supported) |
| User | Search by email |
| Date Range | Last 1h / 6h / 24h / 7d / Custom |

**Event Table:**

| Column | Width | Detail |
|---|---|---|
| Timestamp | 160px | `HH:MM:SS.ms` for recent, `YYYY-MM-DD HH:MM:SS` for older |
| Event Type | 200px | `snake_case` monospace · colour coded |
| Severity | 90px | Critical/High/Medium/Low/Info badge |
| Actor | 160px | User email or "anonymous" or API key name |
| Target | 160px | Institution / User / API key / etc. |
| IP Address | 110px | IPv4/v6 · `font-mono text-xs` · red if on blocklist |
| Location | 100px | City, Country (GeoIP) |
| Count | 60px | Occurrence count (for grouped events) |
| [Details] | 70px | → Event Drawer |

**Severity row colouring:**
- Critical: `bg-[#1A0A0A]` + left border `border-l-4 border-[#EF4444]`
- High: `bg-[#1A0A0A]`
- Medium: normal
- Low/Info: normal opacity-70

**Live prepend:** new events prepended via `hx-swap="afterbegin"` on `#security-event-rows` · flash animation `animate-pulse` 1s on new rows

---

### 4.3 Tab: IP Blocklist

`id="tab-blocklist"` · `hx-get="?part=ip_blocklist"`

**[+ Block IP]** button (requires 2FA)

**IP Blocklist Table:**
| Column | Detail |
|---|---|
| IP / CIDR | `font-mono` |
| Type | Temporary / Permanent |
| Reason | Brute force / API abuse / Manual / etc. |
| Events before block | Count |
| Blocked at | Timestamp |
| Expires at | Datetime or "Never" |
| Blocked by | Username or "System" |
| Status | Active / Expired |
| Actions ⋯ | Unblock / Extend / View Events |

**Block IP Modal (480px):**
- IP / CIDR input
- Block type: Temporary (select duration) / Permanent
- Reason: required text
- 2FA required

**Quick block:** from Event Feed row Actions ⋯ → "Block this IP" → same modal pre-filled

---

### 4.4 Tab: Threat Map

`id="tab-threatmap"` · `hx-get="?part=threat_map"`

**World SVG map** with attack origin dots
- Dot size: proportional to event count from that location
- Dot colour: red = Critical/High · amber = Medium · grey = Low
- India highlighted separately (domestic events vs. foreign)
- Hover: country + event count + severity breakdown
- Click: filters Event Feed to that country

**Event count by country table (below map):**
| Country | Events (24h) | % of total | Severity | Action |
|---|---|---|---|---|
| India | 1,200 | 65% | Mixed | — |
| China | 180 | 10% | High | [Block ASN] |
| USA | 140 | 8% | Low | — |

---

### 4.5 Tab: API Anomalies

`id="tab-api"` · `hx-get="?part=api_anomalies"`

**Purpose:** API keys used from unexpected IPs, unusual call patterns, rate limit abuse.

**Anomaly Table:**
| Column | Detail |
|---|---|
| API Key | Masked `sk_prod_...a7f4c2b8` + institution |
| Anomaly Type | New IP / Rate limit exceeded / Unusual endpoint / Time pattern |
| Detected at | Timestamp |
| IP Address | `font-mono` |
| Request count | Count in anomalous period |
| Risk Score | 0–100 |
| Actions ⋯ | View key / Revoke key / Block IP / Dismiss |

**[Revoke Key]:** requires 2FA · confirmation modal

---

### 4.6 Tab: Settings

`id="tab-settings"` · `hx-get="?part=security_settings"`

**Security policy configuration (2FA required to save):**

| Setting | Type | Default |
|---|---|---|
| Failed login threshold (before lock) | Number | 10 attempts |
| Account lockout duration | Select | 15 min / 30 min / 1h / Permanent |
| Brute force detection window | Select | 5 min / 15 min / 1h |
| IP auto-block threshold | Number | 50 failed attempts / hour |
| Auto-block duration | Select | 1h / 24h / 7d / Permanent |
| 2FA required for roles | Checkboxes | exec ✓ · superadmin ✓ · ops ✓ · finance ✓ |
| Session timeout | Select | 30 min / 1h / 4h / 8h |
| SIEM webhook URL | URL input | Optional |
| Alert email for Critical events | Email | compliance@... |

**[Save Security Settings]** · 2FA enforced · audit log entry created

---

## 5. Drawers

### 5.1 Security Event Drawer (560 px)

`id="security-event-drawer"` · `body.drawer-open`

**Header:** Event type + severity badge + timestamp · `[×]`

**Section A — Event Details:**
| Field | Value |
|---|---|
| Event ID | EVT-... |
| Type | `brute_force_block` |
| Severity | High |
| Timestamp | 14:32:05.418 IST |
| Actor | anonymous / user@email.com |
| Actor IP | 192.168.x.x |
| Location | Hyderabad, India (GeoIP) |
| Target | Login endpoint / Institution INST-00342 |

**Section B — Context:**
- Related events in last 1h from same IP (mini table: 5 rows)
- Same IP on blocklist? Yes/No

**Section C — Raw payload:**
`<pre>` JSON of full event payload · collapsible · max-height 200px overflow-scroll

**Section D — Actions:**
[Block this IP] [Flag as False Positive] [Create Incident] [Close]

---

## 6. Modals

### 6.1 Block IP Modal (480 px)

**2FA required.**
| Field | Type |
|---|---|
| IP / CIDR | Text · validated format |
| Duration | 1h / 6h / 24h / 7d / Permanent |
| Reason | Required text |
| Notify institution (if institution IP) | Checkbox |

**Footer:** [Cancel] [Block IP]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/security_kpi.html` | Page load · poll 30s |
| `?part=security_feed` | `exec/partials/security_feed.html` | Tab · filter · poll 30s |
| `?part=ip_blocklist` | `exec/partials/ip_blocklist.html` | Tab click |
| `?part=threat_map` | `exec/partials/threat_map.html` | Tab click |
| `?part=api_anomalies` | `exec/partials/api_anomalies.html` | Tab click |
| `?part=security_settings` | `exec/partials/security_settings.html` | Tab click |
| `?part=event_drawer&id={id}` | `exec/partials/security_event_drawer.html` | [Details] click |

**Django view dispatch:**
```python
class SecurityEventsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_security_events"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/security_kpi.html",
                "security_feed": "exec/partials/security_feed.html",
                "ip_blocklist": "exec/partials/ip_blocklist.html",
                "threat_map": "exec/partials/threat_map.html",
                "api_anomalies": "exec/partials/api_anomalies.html",
                "security_settings": "exec/partials/security_settings.html",
                "event_drawer": "exec/partials/security_event_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/security_events.html", ctx)

    def post(self, request):
        part = request.GET.get("part", "")
        handlers = {
            "block_ip": self._handle_block_ip,
            "unblock_ip": self._handle_unblock_ip,
            "save_security_settings": self._handle_save_settings,
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
| Event feed (50 rows) | < 400 ms | > 1 s |
| IP blocklist table | < 300 ms | > 800 ms |
| Threat map render | < 600 ms | > 1.5 s |
| Event drawer | < 200 ms | > 500 ms |
| Full page initial load | < 800 ms | > 2 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Critical event: data exfiltration attempt | Immediate PagerDuty alert + email to security@platform.com |
| Same IP blocked multiple times | "IP already blocked (expires {date}). Extend duration?" |
| Unblock IP: still attacking | Warning "This IP has made {N} requests in the last hour. Are you sure?" |
| 0 events matching filter | Empty state: "No security events match your filters" |
| SIEM webhook fails | Toast "SIEM delivery failed — events still logged locally" |
| Brute force: admin account targeted | Critical severity auto-classified + 2FA forced on next login |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `B` | Block IP modal |
| `F` | Focus filter |
| `L` | Toggle live feed |
| `1`–`5` | Switch tabs |
| `Enter` | Open event drawer |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/security_events.html` | Full page shell |
| `exec/partials/security_kpi.html` | KPI strip |
| `exec/partials/security_feed.html` | Event feed table |
| `exec/partials/ip_blocklist.html` | IP blocklist table |
| `exec/partials/threat_map.html` | World threat map |
| `exec/partials/api_anomalies.html` | API anomaly table |
| `exec/partials/security_settings.html` | Settings form |
| `exec/partials/security_event_drawer.html` | Event detail drawer |
| `exec/partials/block_ip_modal.html` | Block IP modal |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `ThreatLevelCard` | §4.1 Card 6 |
| `SecurityEventTable` | §4.2 |
| `SeverityBadge` | §4.2 |
| `IPBlocklistTable` | §4.3 |
| `WorldThreatMap` | §4.4 |
| `APIAnomalyTable` | §4.5 |
| `SecuritySettingsForm` | §4.6 |
| `DrawerPanel` | §5.1 |
| `JSONRawViewer` | §5.1 Section C |
| `ModalDialog` | §6.1 |
| `PollableContainer` | KPI · event feed |
