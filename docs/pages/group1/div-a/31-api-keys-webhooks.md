# div-a-31 — API Keys & Webhooks

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Active API integrations | ~42 institutions using API access (Enterprise + selected Professional) |
| API keys per institution | 1–5 (per environment: test/prod) |
| Total active API keys | ~120 |
| API requests/day (platform) | ~2M–5M (high-usage coaching integrations) |
| Webhook endpoints | ~80 active webhooks |
| Webhook events/day | ~500K (exam events, student events, billing events) |
| API rate limits | Enterprise: 10,000 req/min · Professional: 1,000 req/min |
| Webhook retry | 3 retries at T+1 min, T+5 min, T+15 min |
| API key rotation recommendation | Every 90 days |
| Webhook delivery success rate target | > 99.5% |

**Why this matters:** API Keys & Webhooks is the integration control plane. Coaching centres (₹15 Cr ARR) build their own apps on top of the platform API — student portals, parent apps, leaderboard integrations. A revoked key or webhook misconfiguration can silently break their student experience. This page must clearly show key usage, webhook delivery health, and allow safe rotation without disruption.

---

## 2. Institution Taxonomy — API Context

| Type | Typical API use case | Integration depth |
|---|---|---|
| School | None (basic plan) | N/A |
| College | Result export, student sync | Occasional |
| Coaching centre | Real-time leaderboard, parent app, batch management | Deep; high volume |
| Group | Cross-institution reporting | Moderate |

---

## 3. Page Metadata

| Field | Value |
|---|---|
| Page title | API Keys & Webhooks |
| Route | `/exec/settings/api/` |
| Django view | `APIKeysWebhooksView` |
| Template | `exec/api_settings_page.html` |
| Priority | P2 |
| Nav group | Settings |
| Required role | `exec`, `superadmin`, `ops` |
| 2FA required | Creating API keys · revoking keys |
| HTMX poll | Webhook health: every 2 min |

---

## 4. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: API Keys & Webhooks          [+ New API Key] [+ New Webhook]        │
├────────┬────────┬────────┬────────┬────────┬──────────────────────────────── ┤
│ Total  │ Active │Req/day │ Error  │Webhook │  Webhook                       │
│ Keys   │ Keys   │ (avg)  │ Rate   │ Count  │  Delivery %                    │
│  120   │  112   │ 3.2M   │ 0.4%   │   80   │  99.7 %                        │
├────────┴────────┴────────┴────────┴────────┴──────────────────────────────── ┤
│ TABS: [API Keys] [Webhooks] [Usage & Logs]                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: API KEYS                                                                │
│ [Search] [Institution ▾] [Status ▾] [Environment ▾]                        │
│ # │ Key name │ Institution │ Env │ Rate limit │ Last used │ Status │ ⋯     │
│ ...                              Paginated 25/page                           │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: WEBHOOKS                                                                │
│ [Search] [Institution ▾] [Event type ▾] [Status ▾]                         │
│ # │ Endpoint URL │ Institution │ Events │ Last delivery │ Health │ ⋯        │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Sections — Deep Specification

### 5.1 KPI Cards

**Container:** `flex gap-4 p-4` · 6 cards · `bg-[#0D1526] rounded-xl border border-[#1E2D4A]`
**Webhook health poll:** `hx-trigger="every 120s[!document.querySelector('.drawer-open,.modal-open')]"` on KPI wrapper

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Total Keys | All API keys (active + revoked) | — |
| 2 | Active Keys | Currently active | — |
| 3 | Requests/day | Avg API requests in last 7 days | > 10M = capacity alert |
| 4 | Error Rate | (4xx + 5xx) ÷ Total requests | > 2% = red |
| 5 | Webhook Count | Active webhook endpoints | — |
| 6 | Webhook Delivery % | Successful deliveries in last 24h | < 99% = red |

**Error Rate card:** `> 2%` = `bg-[#450A0A]` background + alert icon
**Webhook Delivery %:** `< 99%` = `bg-[#450A0A]` · `< 99.5%` = `bg-[#451A03]`

---

### 5.2 Tab: API Keys

`id="tab-api-keys"` · `hx-get="?part=keys"`

**Toolbar (below tab bar):**
`flex gap-3 p-4`
- `[🔍 Search key name, institution...]` debounced 400ms
- [Institution ▾] searchable dropdown
- [Status ▾] multi-select: Active / Revoked / Expired
- [Environment ▾] Production / Test

**API Keys Table:**
`id="api-keys-table"` · `hx-get="?part=keys"` on load

| Column | Sort | Width | Detail |
|---|---|---|---|
| Key name | ✓ | 200px | Descriptive name e.g., "ABC Coaching — Prod" |
| Institution | ✓ | 180px | Name + type badge |
| Environment | ✓ | 100px | Production `bg-[#064E3B] text-[#34D399]` · Test `bg-[#1E293B] text-[#94A3B8]` |
| Rate limit | ✓ | 100px | Requests/minute |
| Last used | ✓ | 120px | Relative time or "Never" · red if > 30 days |
| Created | ✓ | 100px | Date |
| Expires | ✓ | 110px | Date or "Never expires" |
| Status | ✓ | 100px | Active (green) / Revoked (red) / Expired (grey) |
| Actions ⋯ | — | 48px | View Detail / Rotate Key / Revoke / Delete |

**Key display security:**
- Key shown in full **only once** at creation time
- After creation, only last 8 chars shown: `sk_prod_...a7f4c2b8` · monospace `font-mono`
- Hover on masked key: tooltip "Full key not stored — use Rotate Key to generate new key"

**[Rotate Key]:** Generates new key · old key remains valid for 24h grace period
**Grace period active:** amber badge on key row "Old key expires in {N}h"

**Key never used (> 30 days old, 0 requests):** amber badge "Never used — revoke if not needed"
**Institution churned but key active:** red badge "Institution {name} is suspended — key should be revoked"

**Row click:** opens API Key Detail Drawer (§6.1)
**Pagination:** 25/page

---

### 5.3 Tab: Webhooks

`id="tab-webhooks"` · `hx-get="?part=webhooks"`
**Poll:** `hx-trigger="every 120s[!document.querySelector('.drawer-open,.modal-open')]"` — webhook health auto-refreshes

**Toolbar:**
- [Search endpoint URL, institution...] debounced 400ms
- [Institution ▾] · [Event type ▾] multi-select · [Status ▾] Active / Disabled

**Webhook Table:**
`id="webhooks-table"` · `hx-get="?part=webhooks"` `hx-trigger="every 120s"`

| Column | Sort | Width | Detail |
|---|---|---|---|
| Endpoint URL | ✓ | 260px | Truncated to 40 chars · hover tooltip shows full URL · `font-mono text-xs` |
| Institution | ✓ | 180px | Name + type badge |
| Events | — | 160px | Comma list of subscribed event types · truncated with "+N more" |
| Last delivery | ✓ | 120px | Relative time + status icon (✓/✗) |
| Delivery rate (7d) | ✓ | 110px | Success % with coloured bar |
| Health | ✓ | 100px | ✅ Healthy / ⚠ Degraded / 🔴 Failing |
| Status | ✓ | 80px | Active / Disabled |
| Actions ⋯ | — | 48px | Test / Edit / Disable / Delete / View Logs |

**Health definition:**
- ✅ Healthy: > 99% delivery in last 24h
- ⚠ Degraded: 90–99% delivery · `text-[#FCD34D]`
- 🔴 Failing: < 90% delivery OR last 3 deliveries all failed · `text-[#F87171]` + pulsing dot

**Failing webhook row:** `bg-[#1A0A0A]` tint

**Row click:** opens Webhook Detail Drawer (§6.2)
**Pagination:** 25/page

---

### 5.4 Tab: Usage & Logs

`id="tab-usage"` · `hx-get="?part=usage"`

#### 5.4.1 API Usage Chart (line, last 30 days)

**Chart:** Multi-line · Chart.js 4.4.2 · Canvas height 260px
**Canvas id:** `api-usage-chart`
**Series:**
| Series | Colour | Y-axis |
|---|---|---|
| Total requests/day | `#6366F1` | left |
| Error requests/day | `#EF4444` | left |
| Rate-limited requests/day | `#F59E0B` | left |

**Toggle:** [By institution] stacked bars / [By endpoint] breakdown

#### 5.4.2 Top Institutions by API Usage Table

| Institution | Requests (30d) | Error rate | Rate limit hits | Status |
|---|---|---|---|---|
| ABC Coaching | 42.1M | 0.2% | 0 | ✅ |
| XYZ Institute | 18.4M | 0.8% | 12 | ⚠ |

**Rate limit hits > 0:** amber badge → upsell signal for higher rate limit add-on

#### 5.4.3 API Error Log (last 100 errors)

`id="error-log-table"` · `hx-get="?part=error_log"`
Paginated table: timestamp · institution · endpoint · HTTP status · error message · [View request] (opens raw request/response drawer)

---

## 6. Drawers

### 6.1 API Key Detail Drawer (560 px)

`id="api-key-drawer"` · `body.drawer-open`

**Header:** Key name + Environment badge + Status badge · `[×]`

**Section A — Key Info:**
| Field | Value |
|---|---|
| Name | ABC Coaching — Prod |
| Institution | ABC Coaching Centre |
| Environment | Production |
| Rate limit | 10,000 req/min |
| Created | 15 Jan 2025 by admin@platform.com |
| Expires | Never |
| Key | `sk_prod_...a7f4c2b8` [Copy] (masked) |
| Scopes | Read Exams · Read Students · Read Analytics |

**Section B — Usage stats (last 30 days):**
- Requests/day line chart (Canvas height 140px)
- Success rate line chart (Canvas height 120px)
- Top 10 endpoints called table: method + path + count
- Error breakdown by HTTP status code: pie chart

**Section C — IP Allowlist:**
`bg-[#131F38] rounded-lg p-4`
- IPs/CIDRs allowed to use this key (empty = all IPs)
- Listed IPs as chips: `text-xs bg-[#1E2D4A] font-mono px-2 py-1 rounded`
- [Edit Allowlist] button → inline editable list

**Section D — Actions (footer 56px):**
`flex gap-3 px-6 py-4 border-t border-[#1E2D4A]`
[Rotate Key] [Revoke Key] [Download Usage Report] [Close]

---

### 6.2 Webhook Detail Drawer (560 px)

`id="webhook-drawer"` · `body.drawer-open`

**Header:** Health badge + Institution + "Webhook" · `[×]`

**Section A — Configuration (editable):**
| Field | Type |
|---|---|
| Endpoint URL | Text · HTTPS required |
| Secret (HMAC) | Masked · [Regenerate] button |
| Subscribed events | Toggle switches grouped by category |
| Retry policy | Select: 3 retries (default) / 0 / 1 / 5 |
| Timeout | Select: 30s (default) / 10s / 60s |

**Event categories with toggles:**
```
Exam events
  ☑ exam.created        ☑ exam.started
  ☑ exam.completed      ☐ exam.cancelled
Student events
  ☑ student.enrolled    ☑ student.score.published
Billing events
  ☐ invoice.created     ☐ invoice.paid     ☐ invoice.overdue
Institution events
  ☐ institution.created ☐ institution.suspended
Incident events
  ☐ incident.created    ☐ incident.resolved
```

**Section B — Delivery Logs (last 50):**

| Column | Detail |
|---|---|
| Delivered at | Timestamp |
| Event type | e.g., `exam.completed` |
| Status | 200 OK (green) / 4xx (amber) / 5xx (red) / Timeout (red) |
| Response time | ms |
| Retry # | 0 = first attempt |
| [View payload] | Expandable code block |

`[View payload]` expands inline:
```html
<details class="mt-1">
  <summary class="text-xs text-[#6366F1] cursor-pointer">View payload</summary>
  <pre class="bg-[#070C18] rounded p-2 text-xs font-mono text-[#94A3B8] overflow-x-auto mt-1">
    { "event": "exam.completed", ... }
  </pre>
</details>
```

**Footer (56px):**
`flex gap-3 px-6 py-4 border-t border-[#1E2D4A]`
[Test Webhook] [Save Changes] [Close]

**[Test Webhook]:** sends a `ping` event to the endpoint · shows result:
- Success: toast "✓ Webhook responded 200 in 142ms"
- Failure: toast "✗ Webhook returned 502 (Bad Gateway)"

---

## 7. Modals

### 7.1 Create API Key Modal (480 px)

**2FA required.**

| Field | Type | Validation |
|---|---|---|
| Key name | Text | Required · min 3 chars |
| Institution | Searchable dropdown | Required |
| Environment | Radio: Production / Test | Required |
| Rate limit | Number (req/min) | Default by plan |
| Expiry | Select: Never / 90 days / 1 year / Custom | |
| Scopes | Multi-select checkboxes | At least one required |
| IP allowlist | CIDR input list | Optional |

**Scopes:**
- Read Exams · Write Exams · Read Students · Read Billing · Read Analytics

**Footer:** [Cancel] [Generate Key]

**After generation — Key Reveal Modal (480px):**
`bg-[#451A03] border border-[#FCD34D] rounded-xl p-4 mb-4`
"⚠ This is the only time this key will be shown in full. Copy and store it securely."
`sk_prod_abc123...xyz789` `text-lg font-mono text-white`
[Copy] button · [I've copied the key — Close]

---

### 7.2 Create Webhook Modal (480 px)

| Field | Type | Validation |
|---|---|---|
| Endpoint URL | URL input | Required · HTTPS required |
| Institution | Dropdown | Required |
| Secret | Text (auto-generated) | User can override |
| Events | Multi-select checkboxes by category | At least 1 required |
| Active | Toggle | Default: On |

**Footer:** [Cancel] [Create Webhook]

**After creation:** [Test Webhook] button appears in success toast

---

### 7.3 Rotate Key Modal (480 px)

**2FA required.**

| Field | Value |
|---|---|
| Current key | `...a7f4c2b8` (masked) |
| Grace period | 24h (default; old key valid for 24h after rotation) |
| Reason | Required text |

"The new key will be generated. The current key will remain valid for 24 hours."
**Footer:** [Cancel] [Rotate Key]

**After rotation:** same Key Reveal Modal as §7.1

---

### 7.4 Revoke Key Modal (480 px)

**2FA required.**
"Revoke API key '{key_name}'?"
Warning: "Revoking immediately breaks all integrations using this key. Prefer 'Rotate Key' for zero-downtime replacement."
| Field | Type |
|---|---|
| Reason | Required text |
| Notify institution | Checkbox (default: checked) |
**Footer:** [Cancel] [Revoke Key]

---

## 8. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/api_kpi.html` | Page load · poll 2 min |
| `?part=keys` | `exec/partials/api_keys_table.html` | Tab click · filter · page |
| `?part=webhooks` | `exec/partials/api_webhooks_table.html` | Tab click · filter · page · poll 2 min |
| `?part=usage` | `exec/partials/api_usage.html` | Tab click |
| `?part=error_log` | `exec/partials/api_error_log.html` | Tab click · page |
| `?part=key_drawer&id={id}` | `exec/partials/api_key_drawer.html` | Row click |
| `?part=webhook_drawer&id={id}` | `exec/partials/api_webhook_drawer.html` | Row click |

**Django view dispatch:**
```python
class APIKeysWebhooksView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.manage_api_keys"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/api_kpi.html",
                "keys": "exec/partials/api_keys_table.html",
                "webhooks": "exec/partials/api_webhooks_table.html",
                "usage": "exec/partials/api_usage.html",
                "error_log": "exec/partials/api_error_log.html",
                "key_drawer": "exec/partials/api_key_drawer.html",
                "webhook_drawer": "exec/partials/api_webhook_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/api_settings_page.html", ctx)

    def post(self, request):
        part = request.GET.get("part", "")
        handlers = {
            "create_key": self._handle_create_key,
            "rotate_key": self._handle_rotate,
            "revoke_key": self._handle_revoke,
            "create_webhook": self._handle_create_webhook,
            "save_webhook": self._handle_save_webhook,
            "test_webhook": self._handle_test_webhook,
        }
        if part in handlers:
            return handlers[part](request)
        return HttpResponseNotAllowed(["GET"])
```

**Webhook health poll:**
```html
<div id="webhooks-table"
     hx-get="/exec/settings/api/?part=webhooks"
     hx-trigger="every 120s[!document.querySelector('.drawer-open,.modal-open')]"
     hx-swap="innerHTML">
```

---

## 9. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI cards | < 400 ms | > 1 s |
| API keys table (25 rows) | < 400 ms | > 1 s |
| Webhooks table (25 rows) | < 400 ms | > 1 s |
| Webhook health poll | < 300 ms | > 800 ms |
| API key generation | < 500 ms | > 1.5 s |
| Key rotation | < 800 ms | > 2 s |
| Webhook test (send + response) | < 35 s total (30s timeout) | > 40 s |
| Usage chart (30 days) | < 800 ms | > 2 s |
| Delivery logs (50 entries) | < 400 ms | > 1 s |
| Full page initial load | < 1.5 s | > 4 s |

---

## 10. States & Edge Cases

| State | Behaviour |
|---|---|
| Webhook endpoint returns 4xx consistently | Health = Failing · alert email to institution API contact + ops |
| API key rate limit hit | 429 response to client · logged in error log · amber badge on institution |
| Key rotation grace period active | Row shows "Old key expires in {N}h" amber badge |
| Webhook endpoint SSL cert expired | Auto-detected on delivery · health = Failing · note "SSL cert invalid" |
| API key never used (> 30d) | Amber badge "Never used — revoke if not needed" |
| Institution churned but key active | Red badge: "Institution suspended — key should be revoked" |
| Webhook payload > 1 MB | Truncated · log shows "Payload truncated" warning |
| IP allowlist violation | Key used from unlisted IP → 403 · security event logged (div-a-18) |
| 100% webhook failure (endpoint down) | PagerDuty alert if Enterprise institution affected |

---

## 11. Keyboard Shortcuts

| Key | Action |
|---|---|
| `N` | New API key |
| `W` | New webhook |
| `F` | Focus search |
| `R` | Refresh all |
| `1`–`3` | Switch tabs (Keys / Webhooks / Usage) |
| `↑` / `↓` | Navigate table rows |
| `Enter` | Open detail drawer |
| `T` (on webhook row) | Test webhook |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcut help |

---

## 12. Template Files

| File | Purpose |
|---|---|
| `exec/api_settings_page.html` | Full page shell |
| `exec/partials/api_kpi.html` | KPI cards |
| `exec/partials/api_keys_table.html` | API keys table |
| `exec/partials/api_webhooks_table.html` | Webhooks table |
| `exec/partials/api_usage.html` | Usage & logs tab |
| `exec/partials/api_error_log.html` | Error log table |
| `exec/partials/api_key_drawer.html` | API Key Detail Drawer (560px) |
| `exec/partials/api_webhook_drawer.html` | Webhook Detail Drawer (560px) |
| `exec/partials/api_create_key_modal.html` | Create API Key Modal (480px) |
| `exec/partials/api_create_webhook_modal.html` | Create Webhook Modal (480px) |
| `exec/partials/api_rotate_modal.html` | Rotate Key Modal (480px) |
| `exec/partials/api_revoke_modal.html` | Revoke Key Modal (480px) |
| `exec/partials/api_key_reveal.html` | One-time key reveal modal |

---

## 13. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §5.1 |
| `TabBar` | §5.2–5.4 |
| `SearchFilterBar` | §5.2, §5.3 toolbars |
| `APIKeyTable` | §5.2 |
| `WebhookTable` | §5.3 |
| `WebhookHealthBadge` | §5.3 health column |
| `UsageLineChart` | §5.4.1 |
| `TopInstitutionsTable` | §5.4.2 |
| `ErrorLogTable` | §5.4.3 |
| `DrawerPanel` | §6.1–6.2 |
| `UsageStatsCharts` | §6.1 Section B |
| `IPAllowlistEditor` | §6.1 Section C |
| `EventTypesToggles` | §6.2 Section A |
| `DeliveryLogsTable` | §6.2 Section B |
| `JsonCodeBlock` | §6.2 payload viewer |
| `ModalDialog` | §7.1–7.4 |
| `KeyRevealModal` | §7.1 post-creation |
| `ScopesChecklist` | §7.1 |
| `EventTypesChecklist` | §7.2 |
| `PaginationStrip` | All tables |
| `PollableContainer` | KPI + webhooks table |
