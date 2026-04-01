# Page 32 — Integration Hub

**Role:** PM Platform
**Route:** `/platform/integrations/`
**Django View:** `IntegrationHubView`
**Template:** `platform/integrations/hub.html`
**Access:** `PermissionRequiredMixin` → `platform.manage_integrations`

---

## 1. Purpose

Central catalog and management console for all third-party integrations available to institutions. PMs configure available connectors, manage credential templates, set per-plan availability, and monitor sync health. Institutions activate integrations from their own portal; this page controls what they can activate and how.

---

## 2. URL & Routing

```
/platform/integrations/                     → IntegrationHubView (catalog)
/platform/integrations/<slug>/              → IntegrationDetailView
/platform/integrations/<slug>/credentials/  → IntegrationCredentialView
/platform/integrations/<slug>/sync-log/     → IntegrationSyncLogView (HTMX partial)
/platform/integrations/health/              → IntegrationHealthView (HTMX partial, polls every 30s)
```

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Integration Hub                               [+ Add Integration] [Export Report] │
│ Manage third-party connectors available to institutions                          │
├──────────────┬──────────────────────────────────────────────────────────────────┤
│ Filter Bar   │ Search: [___________] Category: [All ▼] Status: [All ▼] Plan: [All ▼] │
├──────────────┴──────────────────────────────────────────────────────────────────┤
│ Summary Strip                                                                    │
│  [32 Connectors] [24 Active] [8 Pending Config] [3 Sync Errors] [99.1% Uptime] │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Tabs: [Catalog] [Sync Health] [Credentials] [Audit Log] [Plan Matrix]           │
├─────────────────────────────────────────────────────────────────────────────────┤
│ CATALOG TAB                                                                     │
│                                                                                 │
│ ── LMS & Collaboration ──────────────────────────────────────────────────────── │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Google   │  │Microsoft │  │  Zoom    │  │  Slack   │  │  Teams   │         │
│  │Classroom │  │  Teams   │  │Webinar   │  │ Alerts   │  │ Calendar │         │
│  │ [Active] │  │ [Active] │  │[Inactive]│  │[Beta]    │  │[Inactive]│         │
│  │Plan: Pro+│  │Plan: Pro+│  │Plan: Ent │  │Plan: All │  │Plan: Pro+│         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
│                                                                                 │
│ ── Automation & Workflow ────────────────────────────────────────────────────── │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│  │  Zapier  │  │  Make    │  │  n8n     │  │Webhook   │                       │
│  │Workflows │  │(Integrat)│  │ (self-   │  │ (Native) │                       │
│  │ [Active] │  │ [Active] │  │ hosted)  │  │ [Active] │                       │
│  │Plan: Pro+│  │Plan: Ent │  │Plan: Ent │  │Plan: All │                       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘                       │
│                                                                                 │
│ ── Content & Assessment ─────────────────────────────────────────────────────── │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│  │ Embibe   │  │ Learnyst │  │ PaperSet │  │ Custom   │                       │
│  │ Content  │  │  LMS     │  │   API    │  │Content   │                       │
│  │ [Active] │  │[Inactive]│  │ [Active] │  │   API    │                       │
│  │Plan: Ent │  │Plan: Ent │  │Plan: Pro │  │Plan: All │                       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘                       │
│                                                                                 │
│ ── Communication ────────────────────────────────────────────────────────────── │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│  │WhatsApp  │  │  Twilio  │  │ SendGrid │  │ Firebase │                       │
│  │Business  │  │  SMS     │  │  Email   │  │   Push   │                       │
│  │ [Active] │  │ [Active] │  │ [Active] │  │ [Active] │                       │
│  │Plan: All │  │Plan: All │  │Plan: All │  │Plan: All │                       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘                       │
│                                                                                 │
│ ── Analytics & BI ───────────────────────────────────────────────────────────── │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                                     │
│  │  Google  │  │ Mixpanel │  │ Metabase │                                     │
│  │Analytics │  │ Events   │  │Dashboards│                                     │
│  │ [Active] │  │ [Active] │  │[Beta]    │                                     │
│  │Plan: All │  │Plan: Pro+│  │Plan: Ent │                                     │
│  └──────────┘  └──────────┘  └──────────┘                                     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Sync Health Tab
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ SYNC HEALTH                            Refresh: every 30s  [Pause] [Refresh Now]│
├────────────────────────┬──────────────┬──────────────┬────────────┬────────────┤
│ Integration            │ Last Sync    │ Status       │ Latency    │ Error Rate │
├────────────────────────┼──────────────┼──────────────┼────────────┼────────────┤
│ Google Classroom       │ 2 min ago    │ ✅ Healthy   │ 342ms      │ 0.0%       │
│ Microsoft Teams        │ 5 min ago    │ ✅ Healthy   │ 518ms      │ 0.1%       │
│ Zapier                 │ 1 min ago    │ ✅ Healthy   │ 201ms      │ 0.0%       │
│ Embibe Content API     │ 22 min ago   │ ⚠️ Delayed  │ 1,240ms    │ 0.8%       │
│ WhatsApp Business      │ 8 min ago    │ ✅ Healthy   │ 389ms      │ 0.0%       │
│ PaperSet API           │ 3 hrs ago    │ 🔴 Error     │ Timeout    │ 42.3%      │
│ Google Analytics       │ 30 min ago   │ ✅ Healthy   │ 789ms      │ 0.0%       │
│ Mixpanel               │ 4 min ago    │ ✅ Healthy   │ 156ms      │ 0.0%       │
├────────────────────────┴──────────────┴──────────────┴────────────┴────────────┤
│ Error details for PaperSet API:                                                 │
│  Last error: Connection timeout after 30s (2026-03-20 09:14:32)                │
│  Consecutive failures: 47  |  Auto-retry: paused (exceeded threshold)          │
│  [View Full Log] [Trigger Manual Retry] [Notify PaperSet Support]              │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Plan Matrix Tab
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PLAN AVAILABILITY MATRIX                              [Edit Matrix] [Export CSV] │
├───────────────────────────────────┬──────────┬──────────┬──────────┬────────────┤
│ Integration                       │ Starter  │ Growth   │ Pro      │ Enterprise │
├───────────────────────────────────┼──────────┼──────────┼──────────┼────────────┤
│ Native Webhook                    │    ✅    │    ✅    │    ✅    │     ✅     │
│ Firebase Push                     │    ✅    │    ✅    │    ✅    │     ✅     │
│ WhatsApp Business                 │    ✅    │    ✅    │    ✅    │     ✅     │
│ Twilio SMS                        │    ✅    │    ✅    │    ✅    │     ✅     │
│ SendGrid Email                    │    ✅    │    ✅    │    ✅    │     ✅     │
│ Google Analytics                  │    ✅    │    ✅    │    ✅    │     ✅     │
│ Custom Content API                │    ✅    │    ✅    │    ✅    │     ✅     │
│ Google Classroom                  │    ❌    │    ❌    │    ✅    │     ✅     │
│ Microsoft Teams                   │    ❌    │    ❌    │    ✅    │     ✅     │
│ Zoom Webinar                      │    ❌    │    ❌    │    ❌    │     ✅     │
│ Zapier                            │    ❌    │    ❌    │    ✅    │     ✅     │
│ Mixpanel                          │    ❌    │    ❌    │    ✅    │     ✅     │
│ PaperSet API                      │    ❌    │    ❌    │    ✅    │     ✅     │
│ Embibe Content API                │    ❌    │    ❌    │    ❌    │     ✅     │
│ Learnyst LMS                      │    ❌    │    ❌    │    ❌    │     ✅     │
│ Make (Integromat)                 │    ❌    │    ❌    │    ❌    │     ✅     │
│ Metabase                          │    ❌    │    ❌    │    ❌    │     ✅     │
└───────────────────────────────────┴──────────┴──────────┴──────────┴────────────┘
```

---

## 4. Integration Detail View

Clicking any integration card opens a detail drawer (640px right):

```
┌────────────────────────────────────────────────────┐
│ Google Classroom                    [Edit] [×]      │
│ LMS & Collaboration                                  │
├────────────────────────────────────────────────────┤
│ Status: Active  |  Plan: Pro+  |  Version: v2.0     │
│ Active on: 143 institutions                         │
├────────────────────────────────────────────────────┤
│ DESCRIPTION                                         │
│ Sync exam schedules, results, and student rosters   │
│ between Srav platform and Google Classroom.         │
│                                                     │
│ CAPABILITIES                                        │
│  ✅ Roster sync (students, teachers)               │
│  ✅ Exam schedule export to Google Calendar        │
│  ✅ Result push to Classroom gradebook             │
│  ✅ OAuth 2.0 per-institution authorization        │
│  ❌ Real-time grade sync (coming Q2 2026)          │
│                                                     │
│ SETUP REQUIREMENTS                                  │
│  • Institution must have Google Workspace           │
│  • Admin must grant OAuth scopes                    │
│  • Sync runs every: 15 min (configurable)          │
│                                                     │
│ CREDENTIAL TEMPLATE                                 │
│  Required fields for institution setup:             │
│  • OAuth Client ID     [masked]                    │
│  • OAuth Client Secret [masked]                    │
│  • Domain whitelist    [e.g., myschool.edu]        │
│                                                     │
│ WEBHOOK EVENTS EMITTED                              │
│  exam.scheduled → pushes to Google Calendar        │
│  result.published → pushes to gradebook            │
│  student.enrolled → syncs to Classroom roster      │
│                                                     │
│ RATE LIMITS                                         │
│  Google API quota: 50 req/s per institution        │
│  Burst allowed: 100 req in 10s                     │
│                                                     │
│ [View Sync Log] [Edit Config] [Disable]            │
└────────────────────────────────────────────────────┘
```

---

## 5. Add Integration Flow

PM adds a new connector:

```
Step 1 — Basic Info
  Name, Slug (auto-generated), Category, Description
  Icon Upload (SVG/PNG, max 128×128px, transparent bg)
  Documentation URL, Support Contact

Step 2 — Plan Availability
  Checkbox matrix (Starter / Growth / Pro / Enterprise)
  Can be changed later without restart

Step 3 — Credential Schema
  JSON Schema builder for credentials required from institution
  Field types: text, password (masked), url, select, boolean
  Mark fields as: required / optional / platform-managed

Step 4 — Webhook Configuration
  Events this integration consumes (inbound)
  Events this integration emits (outbound)
  Retry policy: attempts (default 3), backoff (exp: 10s, 30s, 120s)
  Signature method: HMAC-SHA256 / OAuth / None

Step 5 — Health Check
  Endpoint URL for ping check (GET, expects 200)
  Check interval: 1 / 5 / 15 / 30 min
  Failure threshold before alert: 3 (default)
  Alert recipients: comma-separated emails / Slack channel

Step 6 — Review & Publish
  Status: Draft / Beta / Active / Deprecated
  Release notes (markdown textarea)
  [Save as Draft] [Publish]
```

---

## 6. Credential Manager

Institutions store credentials per-integration. PM side shows:

```
/platform/integrations/<slug>/credentials/
```

- Read-only list of which institutions have configured credentials
- PM cannot see raw secret values (only last-4 characters of masked values)
- PM can trigger "Force Re-authorize" — invalidates current token, institution sees re-auth prompt
- PM can view OAuth token expiry dates and trigger pre-emptive refresh
- Credential rotation: PM uploads new platform-level API keys; institutions' tokens remain valid until TTL

**Credential Storage Architecture:**
- Institution credentials encrypted with AES-256 using per-institution key in AWS Secrets Manager
- Key path: `srav/integrations/{integration_slug}/{institution_id}/credentials`
- PM platform keys stored at: `srav/integrations/{integration_slug}/platform`
- Zero-knowledge model: credentials decrypted only at sync execution time

---

## 7. Sync Health Monitor

```
Poll: hx-get="/platform/integrations/health/" hx-trigger="every 30s[!document.querySelector('.modal-open')]"
      hx-target="#health-table-body" hx-swap="innerHTML"
```

**Health States:**
| State | Condition | Display |
|---|---|---|
| Healthy | Last sync < 15 min ago, error rate < 1% | ✅ green |
| Delayed | Last sync 15–60 min ago OR latency > 1000ms | ⚠️ amber |
| Error | Consecutive failures ≥ 3 OR error rate > 10% | 🔴 red |
| Paused | Manually paused or auto-paused after threshold | ⏸️ grey |
| Inactive | Integration disabled for all institutions | — grey |

**Auto-pause logic:**
```python
if consecutive_failures >= INTEGRATION_FAILURE_THRESHOLD:  # default 10
    integration.sync_status = 'auto_paused'
    integration.save(update_fields=['sync_status'])
    send_alert_to_pm.delay(integration.id, reason='threshold_exceeded')
```

**Sync Log Entry (per institution, per run):**
```
Timestamp | Institution | Direction | Records | Status | Latency | Error
```

---

## 8. Django View

```python
class IntegrationHubView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'platform.manage_integrations'
    template_name = 'platform/integrations/hub.html'

    def get(self, request):
        if self._is_htmx(request):
            part = request.GET.get('part')
            handlers = {
                'health': self._render_health,
                'sync_log': self._render_sync_log,
            }
            return handlers.get(part, self._render_full)(request)
        return self._render_full(request)

    def _render_full(self, request):
        integrations = Integration.objects.select_related(
            'category'
        ).prefetch_related(
            'plan_entitlements', 'sync_health'
        ).order_by('category__order', 'name')

        grouped = {}
        for intg in integrations:
            cat = intg.category.name
            grouped.setdefault(cat, []).append(intg)

        ctx = {
            'grouped': grouped,
            'summary': self._get_summary(),
        }
        return render(request, self.template_name, ctx)

    def _get_summary(self):
        qs = Integration.objects.filter(status='active')
        return {
            'total': Integration.objects.count(),
            'active': qs.count(),
            'pending_config': Integration.objects.filter(status='draft').count(),
            'sync_errors': IntegrationSyncHealth.objects.filter(
                state='error'
            ).count(),
        }

    def _render_health(self, request):
        health = IntegrationSyncHealth.objects.select_related(
            'integration'
        ).order_by('state', 'integration__name')
        return render(request, 'platform/integrations/_health_table.html',
                      {'health': health})

    @staticmethod
    def _is_htmx(request):
        return request.headers.get('HX-Request') == 'true'
```

---

## 9. Models

```python
class IntegrationCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']


class Integration(models.Model):
    STATUS = [
        ('draft', 'Draft'),
        ('beta', 'Beta'),
        ('active', 'Active'),
        ('deprecated', 'Deprecated'),
    ]
    SYNC_STATUS = [
        ('enabled', 'Enabled'),
        ('auto_paused', 'Auto-Paused'),
        ('manually_paused', 'Manually Paused'),
        ('disabled', 'Disabled'),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        IntegrationCategory, on_delete=models.PROTECT, related_name='integrations'
    )
    description = models.TextField()
    icon_s3_key = models.CharField(max_length=500, blank=True)
    docs_url = models.URLField(blank=True)
    support_email = models.EmailField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    sync_status = models.CharField(
        max_length=20, choices=SYNC_STATUS, default='enabled'
    )
    version = models.CharField(max_length=20, default='v1.0')
    credential_schema = models.JSONField(
        default=dict,
        help_text='JSON Schema defining credentials required from institutions'
    )
    webhook_events_inbound = models.JSONField(default=list)
    webhook_events_outbound = models.JSONField(default=list)
    retry_attempts = models.PositiveSmallIntegerField(default=3)
    health_check_url = models.URLField(blank=True)
    health_check_interval_min = models.PositiveSmallIntegerField(default=15)
    failure_threshold = models.PositiveSmallIntegerField(default=10)
    alert_emails = models.JSONField(default=list)
    release_notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='integrations_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__order', 'name']


class IntegrationPlanEntitlement(models.Model):
    PLANS = [
        ('starter', 'Starter'),
        ('growth', 'Growth'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    integration = models.ForeignKey(
        Integration, on_delete=models.CASCADE, related_name='plan_entitlements'
    )
    plan = models.CharField(max_length=20, choices=PLANS)
    enabled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('integration', 'plan')


class IntegrationSyncHealth(models.Model):
    STATE = [
        ('healthy', 'Healthy'),
        ('delayed', 'Delayed'),
        ('error', 'Error'),
        ('paused', 'Paused'),
        ('inactive', 'Inactive'),
    ]
    integration = models.OneToOneField(
        Integration, on_delete=models.CASCADE, related_name='sync_health'
    )
    state = models.CharField(max_length=20, choices=STATE, default='inactive')
    last_sync_at = models.DateTimeField(null=True, blank=True)
    last_latency_ms = models.IntegerField(null=True, blank=True)
    error_rate_pct = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.00')
    )
    consecutive_failures = models.IntegerField(default=0)
    last_error_message = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class IntegrationSyncLog(models.Model):
    DIRECTION = [('inbound', 'Inbound'), ('outbound', 'Outbound')]
    STATUS = [('success', 'Success'), ('partial', 'Partial'), ('failed', 'Failed')]

    integration = models.ForeignKey(
        Integration, on_delete=models.CASCADE, related_name='sync_logs'
    )
    institution = models.ForeignKey(
        'institutions.Institution', on_delete=models.CASCADE, null=True, blank=True
    )
    direction = models.CharField(max_length=10, choices=DIRECTION)
    records_processed = models.IntegerField(default=0)
    records_failed = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS)
    latency_ms = models.IntegerField(null=True)
    error_detail = models.TextField(blank=True)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['integration', '-started_at']),
            models.Index(fields=['institution', '-started_at']),
        ]


class InstitutionIntegrationCredential(models.Model):
    """
    Stores per-institution credentials for an integration.
    Raw secrets are NOT stored here — only metadata.
    Actual secrets are in AWS Secrets Manager.
    """
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    institution = models.ForeignKey('institutions.Institution', on_delete=models.CASCADE)
    secrets_manager_key = models.CharField(max_length=500)
    oauth_token_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('integration', 'institution')
```

---

## 10. Celery Tasks

```python
@shared_task(queue='integrations')
def run_integration_health_checks():
    """Runs every 5 minutes via Celery beat."""
    active = Integration.objects.filter(
        status='active', sync_status='enabled'
    ).select_related('sync_health')

    for integration in active:
        if not integration.health_check_url:
            continue
        try:
            start = time.time()
            resp = requests.get(integration.health_check_url, timeout=10)
            latency_ms = int((time.time() - start) * 1000)

            health = integration.sync_health
            if resp.status_code == 200:
                health.consecutive_failures = 0
                health.state = 'healthy' if latency_ms < 1000 else 'delayed'
            else:
                health.consecutive_failures += 1
                health.last_error_message = f"HTTP {resp.status_code}"
                health.state = 'error'

            health.last_latency_ms = latency_ms
            health.last_sync_at = timezone.now()
            health.save()

            if health.consecutive_failures >= integration.failure_threshold:
                integration.sync_status = 'auto_paused'
                integration.save(update_fields=['sync_status'])
                notify_integration_failure.delay(integration.id)

        except requests.Timeout:
            health = integration.sync_health
            health.consecutive_failures += 1
            health.last_error_message = "Connection timeout"
            health.state = 'error'
            health.save()


@shared_task(queue='integrations')
def notify_integration_failure(integration_id: int):
    integration = Integration.objects.get(id=integration_id)
    for email in integration.alert_emails:
        send_mail(
            subject=f"[Srav] Integration Error: {integration.name}",
            message=(
                f"{integration.name} has been auto-paused after "
                f"{integration.failure_threshold} consecutive failures.\n\n"
                f"Last error: {integration.sync_health.last_error_message}\n\n"
                f"Review: https://app.srav.in/platform/integrations/{integration.slug}/"
            ),
            from_email='noreply@srav.in',
            recipient_list=[email],
        )
```

---

## 11. Redis Caching

```python
# Integration catalog cache (rebuilt on save)
INTEGRATION_CATALOG_KEY = 'integrations:catalog:grouped'
INTEGRATION_CATALOG_TTL = 300  # 5 min

# Health summary cache (rebuilt by Celery every 5 min)
INTEGRATION_HEALTH_SUMMARY_KEY = 'integrations:health:summary'
INTEGRATION_HEALTH_SUMMARY_TTL = 60  # 1 min

# Per-integration plan entitlement (used at institution activation time)
# Key: integrations:entitlements:{slug}
INTEGRATION_ENTITLEMENT_TTL = 600  # 10 min
```

Cache busted on:
- Integration save/update (`post_save` signal)
- Plan matrix edit (explicit `cache.delete()` in view)

---

## 12. Security

- `manage_integrations` permission required for all write actions
- PM cannot view raw institution credentials (zero-knowledge architecture)
- All credential operations routed through AWS Secrets Manager — never stored in Django DB
- Force re-authorize action logged to `IntegrationAuditLog` with actor, timestamp, reason
- Integration webhooks signed with HMAC-SHA256 using integration-specific secret
- Inbound webhook signature verified before processing: `HMAC-SHA256(payload, secret) == X-Srav-Signature`
- Rate limit: 60 requests/min per PM user on write endpoints (DRF throttle)
- Deprecated integrations cannot be re-activated; must create new slug

---

## 13. DB Schema

```sql
-- Core tables
integrations_integrationcategory (id, name, slug, order)
integrations_integration (id, name, slug, category_id, description, icon_s3_key,
  docs_url, support_email, status, sync_status, version, credential_schema jsonb,
  webhook_events_inbound jsonb, webhook_events_outbound jsonb,
  retry_attempts, health_check_url, health_check_interval_min, failure_threshold,
  alert_emails jsonb, release_notes, created_by_id, created_at, updated_at)
integrations_integrationplanentitlement (id, integration_id, plan, enabled)
integrations_integrationsynchealth (id, integration_id, state, last_sync_at,
  last_latency_ms, error_rate_pct, consecutive_failures, last_error_message, updated_at)
integrations_integrationsynclog (id, integration_id, institution_id, direction,
  records_processed, records_failed, status, latency_ms, error_detail,
  started_at, completed_at)
integrations_institutionintegrationcredential (id, integration_id, institution_id,
  secrets_manager_key, oauth_token_expiry, is_active, last_verified_at,
  created_at, updated_at)

-- Indexes
CREATE INDEX ON integrations_integrationsynclog (integration_id, started_at DESC);
CREATE INDEX ON integrations_integrationsynclog (institution_id, started_at DESC);
CREATE INDEX ON integrations_integration (status, sync_status);
```

---

## 14. Validation Rules

| Rule | Detail |
|---|---|
| Slug uniqueness | Case-insensitive, alphanumeric + hyphens only, validated on creation |
| Icon dimensions | Max 128×128px, SVG or PNG, transparent background enforced |
| Health check URL | Must be HTTPS; HTTP rejected |
| Credential schema | Must be valid JSON Schema draft-07; validated server-side on save |
| Plan matrix | Cannot remove plan access if > 0 institutions currently use on that plan |
| Deprecation | Requires `reason` text; notifies all active institutions via email |
| Failure threshold | Min 1, max 100; validated `PositiveSmallIntegerField` |
| Sync log retention | Auto-deleted after 90 days via nightly Celery task |
