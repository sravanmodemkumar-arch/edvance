# Page 33 — API Testing Dashboard

**Role:** QA Engineer
**Route:** `/qa/api-testing/`
**Django View:** `APITestingDashboardView`
**Template:** `qa/api_testing/dashboard.html`
**Access:** `PermissionRequiredMixin` → `qa.run_api_tests`

---

## 1. Purpose

Centralized functional API testing console for QA engineers. Run named test suites against staging/production endpoints, validate response schemas, perform contract testing, integrate with Postman/Newman CI pipelines, diff API changelogs, and trigger regression runs on every deploy. Complements the load-testing capabilities of page 24 (Performance Test Orchestrator) — this page focuses on correctness, not concurrency.

---

## 2. URL & Routing

```
/qa/api-testing/                             → APITestingDashboardView (suite list)
/qa/api-testing/<suite-id>/                  → APITestSuiteDetailView
/qa/api-testing/<suite-id>/run/              → APITestRunView (POST, triggers Celery)
/qa/api-testing/<suite-id>/results/<run-id>/ → APITestResultView
/qa/api-testing/changelog/                   → APIChangelogView
/qa/api-testing/contracts/                   → ContractTestView
/qa/api-testing/ci-config/                   → CIIntegrationConfigView
/qa/api-testing/runs/live/                   → LiveRunStatusView (HTMX partial, polls every 5s)
```

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ API Testing Dashboard                    [+ New Suite] [Run All] [CI Config]    │
│ Functional API test management · endpoint validation · contract testing          │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Summary Strip                                                                    │
│  [18 Suites] [1,240 Tests] [Last Run: 6m ago] [97.3% Pass Rate] [3 Failing]    │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Tabs: [Test Suites] [Live Runs] [Changelog Diff] [Contracts] [CI / Newman]      │
├─────────────────────────────────────────────────────────────────────────────────┤
│ TEST SUITES TAB                                                                  │
│                                                                                 │
│ Filter: [All Tags ▼] [All Envs ▼] Status: [All ▼] [Search suites...]           │
│                                                                                 │
│ ┌───────────────────────────────────────────────────────────────────────────┐   │
│ │ Suite: Auth & Sessions          Tag: auth  Env: staging  Tests: 48        │   │
│ │ Last Run: 2026-03-20 11:02  Pass: 48/48 (100%)  Duration: 4.2s           │   │
│ │ [Run Now] [Edit] [View Results] [Schedule] [Export Postman]               │   │
│ ├───────────────────────────────────────────────────────────────────────────┤   │
│ │ Suite: Exam CRUD & Lifecycle    Tag: exams  Env: staging  Tests: 112      │   │
│ │ Last Run: 2026-03-20 10:58  Pass: 109/112 (97.3%)  Duration: 12.8s  ⚠️   │   │
│ │ [Run Now] [Edit] [View Results] [Schedule] [Export Postman]               │   │
│ ├───────────────────────────────────────────────────────────────────────────┤   │
│ │ Suite: Billing & Subscriptions  Tag: billing  Env: staging  Tests: 87     │   │
│ │ Last Run: 2026-03-20 08:30  Pass: 87/87 (100%)  Duration: 9.1s           │   │
│ │ [Run Now] [Edit] [View Results] [Schedule] [Export Postman]               │   │
│ ├───────────────────────────────────────────────────────────────────────────┤   │
│ │ Suite: Result Processing API    Tag: results  Env: staging  Tests: 64     │   │
│ │ Last Run: 2026-03-20 09:15  Pass: 61/64 (95.3%)  Duration: 8.7s  ⚠️     │   │
│ │ [Run Now] [Edit] [View Results] [Schedule] [Export Postman]               │   │
│ ├───────────────────────────────────────────────────────────────────────────┤   │
│ │ Suite: Institution Onboarding   Tag: onboarding  Env: staging  Tests: 38  │   │
│ │ Last Run: 2026-03-19 23:00  Pass: 38/38 (100%)  Duration: 6.4s           │   │
│ │ [Run Now] [Edit] [View Results] [Schedule] [Export Postman]               │   │
│ └───────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Live Runs Tab (polls every 5s)
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ LIVE RUNS                                             [Stop All] [Refresh Now]  │
│ hx-trigger="every 5s[!document.querySelector('.modal-open')]"                   │
├────────────────────┬──────────┬───────────┬───────────────────┬────────────────┤
│ Suite              │ Env      │ Triggered │ Progress          │ Actions        │
├────────────────────┼──────────┼───────────┼───────────────────┼────────────────┤
│ Exam CRUD          │ staging  │ CI Push   │ ████████░░ 45/112 │ [View] [Stop]  │
│ Auth & Sessions    │ prod     │ Manual    │ ██████████ Done ✅│ [View]         │
│ Result Processing  │ staging  │ Scheduled │ ███░░░░░░░ 18/64  │ [View] [Stop]  │
└────────────────────┴──────────┴───────────┴───────────────────┴────────────────┘
```

### Changelog Diff Tab
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ API CHANGELOG DIFF                         Compare: [v2.3.1 ▼] vs [v2.4.0 ▼]  │
│ Auto-generated from OpenAPI spec on each deploy                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│ BREAKING CHANGES (2)                                              ⚠️ action req │
│  ❌ POST /exams/{id}/publish — removed field: `notify_sms` (was optional)      │
│     Affected suites: [Exam CRUD] [Notification Tests]                           │
│  ❌ GET /results/{id}/ — response field renamed: `score` → `raw_score`         │
│     Affected suites: [Result Processing API]                                    │
│                                                                                 │
│ ADDITIONS (5)                                                                   │
│  ✅ POST /exams/{id}/reschedule — new endpoint                                 │
│  ✅ GET /institutions/{id}/usage-stats/ — new endpoint                         │
│  ✅ PATCH /billing/subscriptions/{id}/ — new optional field: `billing_day`     │
│  ✅ GET /users/{id}/activity-log/ — new endpoint                               │
│  ✅ POST /promos/{code}/validate/ — new endpoint                               │
│                                                                                 │
│ MODIFICATIONS (3)                                                               │
│  🔵 GET /exams/ — added filter param: `?domain=`                               │
│  🔵 POST /institutions/ — `subdomain` field now required (was optional)        │
│  🔵 GET /reports/sla/ — rate limit changed: 30→10 req/min                     │
│                                                                                 │
│ [Generate Regression Suite for Breaking Changes] [Export Diff PDF]             │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Contract Tests Tab
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ CONTRACT TESTS                                        [+ Add Contract] [Run All]│
│ Provider-consumer contracts validated on every deploy                           │
├──────────────────────┬──────────────────┬───────────────┬──────────┬───────────┤
│ Contract             │ Provider         │ Consumer      │ Status   │ Last Run   │
├──────────────────────┼──────────────────┼───────────────┼──────────┼───────────┤
│ Exam → Results API   │ Exam Service     │ Result Engine │ ✅ PASS  │ 11:02     │
│ Billing → Institution│ Billing API      │ Portal API    │ ✅ PASS  │ 10:58     │
│ Auth → All Services  │ Auth Service     │ All           │ ✅ PASS  │ 11:02     │
│ Notification → Events│ Event Bus        │ Notif Service │ ⚠️ WARN  │ 08:30     │
│ Content → Assessment │ Content API      │ Assessment Eng│ ✅ PASS  │ 09:15     │
└──────────────────────┴──────────────────┴───────────────┴──────────┴───────────┘
│ ⚠️ Notification → Events: Consumer expects `exam.scheduled.v2` but provider    │
│    still emitting `exam.scheduled.v1`. Update consumer or provider.             │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Test Suite Detail View

```
/qa/api-testing/<suite-id>/
```

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Exam CRUD & Lifecycle                           [Run Now] [Edit Suite] [Back ←] │
│ 112 tests · Tag: exams · Env: staging · Last run: 10:58                        │
├──────────────────────────────────────┬──────────────────────────────────────────┤
│ Test Cases                           │ Last Run Results                         │
│                                      │                                          │
│ + Create Exam (valid payload) ✅     │ Run ID: #4821                            │
│ + Create Exam (missing title) ✅     │ Started: 10:58:02  Duration: 12.8s      │
│ + Create Exam (past start_time) ✅   │ Pass: 109  Fail: 3  Skip: 0            │
│ + Create Exam (invalid domain) ✅    │                                          │
│ + Get Exam by ID ✅                  │ FAILURES:                               │
│ + Get Exam (not found) ✅           │                                          │
│ + Update Exam metadata ✅           │ ❌ PATCH /exams/{id}/extend/            │
│ + Publish Exam ✅                   │    Expected: 200, Got: 422              │
│ + Publish Exam (already live) ✅    │    Body: {"error":"extend_locked_live"} │
│ + Extend Exam duration ❌           │    Test expected 200 OK on live exam    │
│ + End Exam early ✅                 │    Fix: update assertion or API         │
│ + Delete Exam (draft) ✅            │                                          │
│ + Delete Exam (live) ✅             │ ❌ GET /exams/?domain=Banking           │
│ + List Exams (paginated) ✅         │    Expected: 200, Got: 400             │
│ + List Exams (filter by domain) ❌  │    New filter param not supported yet   │
│ + List Exams (filter by status) ✅  │                                          │
│ ...                                  │ ❌ POST /exams/{id}/publish            │
│                                      │    Expected: field `notify_sms` in req │
│                                      │    Breaking change from v2.4.0 diff     │
│                                      │                                          │
│                                      │ [Fix Assertions] [Create Bug Ticket]    │
└──────────────────────────────────────┴──────────────────────────────────────────┘
```

---

## 5. New / Edit Test Suite

```
Suite Name: [________________________]
Tags: [auth] [exams] [billing] [+Add]
Target Environment: [Staging ▼] / [Production ▼]
Base URL: [https://api-staging.srav.in]   (overridden per env in config)

TEST CASES
Each test case:
  Name: [________________________]
  Method: [GET ▼]  URL Path: [/exams/{id}/]
  Path Variables: id = {exam_id_from_fixture}
  Headers: Authorization: Bearer {token}
  Request Body (JSON):
    { ... }
  Expected Status: [200 ▼]
  Response Assertions:
    • response.json.id == {exam_id_from_fixture}   [+ Add Assertion]
    • response.json.status in ["draft","live"]
    • response.time < 800ms                         ← latency assertion
  Schema Validation: [Link OpenAPI Schema ▼] → validates full response shape
  On Failure: [Continue ▼] / [Abort Suite]

[+ Add Test Case] [Import from Postman Collection] [Import from OpenAPI]

Test Fixtures:
  exam_id_from_fixture → created by: "Create Exam (valid payload)"
  token               → from: suite-level auth setup step

[Save Suite] [Save & Run]
```

---

## 6. CI / Newman Integration Tab

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ CI / NEWMAN INTEGRATION                                                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│ How it works:                                                                   │
│  On every deploy → CI pipeline calls POST /qa/api/ci-trigger/                  │
│  → Celery runs selected suites against the new deploy                           │
│  → Results posted back to CI pipeline via webhook                               │
│  → Deploy blocked if pass rate < threshold                                      │
│                                                                                 │
│ CI TRIGGER ENDPOINT                                                             │
│  POST /qa/api/ci-trigger/                                                       │
│  Headers: X-CI-Token: {api_token}                                               │
│  Body: { "env": "staging", "deploy_id": "abc123",                              │
│          "suites": ["all"] | ["auth", "exams"] }                                │
│  Response: { "run_id": "4821", "status": "queued" }                            │
│  Webhook result: POST {your_webhook_url}                                        │
│    { "run_id": "4821", "pass": 109, "fail": 3,                                 │
│      "pass_rate": 97.3, "blocking": false }                                     │
│                                                                                 │
│ PASS RATE THRESHOLD                                                             │
│  Block deploy if pass rate < [95 %]   (configurable per env)                   │
│  Suites that always block on fail: [auth] [billing] [+Add]                     │
│  Suites that warn but don't block:  [exams] [results]                          │
│                                                                                 │
│ YOUR CI TOKEN                                                                   │
│  sk-qa-ci-████████████████  [Regenerate] [Copy]                                │
│  Last used: 2026-03-20 10:58 from IP 10.0.1.45                                 │
│                                                                                 │
│ POSTMAN / NEWMAN                                                                │
│  Export any suite as Postman Collection v2.1:                                   │
│  → From suite list click [Export Postman]                                       │
│  → Run with: newman run srav-exam-crud.json --env-var baseUrl=...              │
│  → Results auto-reported to dashboard via `newman-reporter-srav`               │
│  npm install -g newman newman-reporter-srav                                     │
│                                                                                 │
│ GITHUB ACTIONS SNIPPET                                                          │
│  ┌───────────────────────────────────────────────────────────┐                 │
│  │ - name: Trigger Srav API Tests                            │                 │
│  │   run: |                                                   │                 │
│  │     curl -s -X POST https://app.srav.in/qa/api/ci-trigger/│                 │
│  │       -H "X-CI-Token: ${{ secrets.SRAV_QA_TOKEN }}"      │                 │
│  │       -H "Content-Type: application/json"                 │                 │
│  │       -d '{"env":"staging","suites":["all"]}'             │                 │
│  └───────────────────────────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Django Views

```python
class APITestingDashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'qa.run_api_tests'
    template_name = 'qa/api_testing/dashboard.html'

    def get(self, request):
        if self._is_htmx(request):
            part = request.GET.get('part')
            handlers = {
                'live_runs': self._render_live_runs,
                'changelog': self._render_changelog,
            }
            return handlers.get(part, self._render_full)(request)
        return self._render_full(request)

    def _render_full(self, request):
        suites = APITestSuite.objects.prefetch_related(
            'last_run'
        ).order_by('-last_run__started_at')

        ctx = {
            'suites': suites,
            'summary': self._get_summary(suites),
        }
        return render(request, self.template_name, ctx)

    def _get_summary(self, suites):
        total_tests = APITestCase.objects.count()
        last_run = APITestRun.objects.order_by('-started_at').first()
        failing = APITestRun.objects.filter(
            status='failed',
            started_at__gte=timezone.now() - timedelta(hours=24)
        ).count()

        return {
            'suite_count': suites.count(),
            'test_count': total_tests,
            'last_run_ago': last_run,
            'failing_count': failing,
        }

    def _render_live_runs(self, request):
        runs = APITestRun.objects.filter(
            status__in=['queued', 'running']
        ).select_related('suite').order_by('-started_at')
        return render(request, 'qa/api_testing/_live_runs.html', {'runs': runs})

    @staticmethod
    def _is_htmx(request):
        return request.headers.get('HX-Request') == 'true'


class APITestRunView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'qa.run_api_tests'

    def post(self, request, suite_id):
        suite = get_object_or_404(APITestSuite, id=suite_id)
        run = APITestRun.objects.create(
            suite=suite,
            triggered_by=request.user,
            trigger_source='manual',
            env=suite.target_env,
            status='queued',
        )
        execute_api_test_suite.delay(run.id)
        if self._is_htmx(request):
            return HttpResponse(
                f'<div class="alert-success">Suite queued. Run #{run.id}</div>'
            )
        return redirect(f'/qa/api-testing/{suite_id}/results/{run.id}/')

    @staticmethod
    def _is_htmx(request):
        return request.headers.get('HX-Request') == 'true'


@require_POST
def ci_trigger_view(request):
    """Called by CI pipeline. Returns immediately; results sent via webhook."""
    token = request.headers.get('X-CI-Token')
    try:
        config = CIIntegrationConfig.objects.get(ci_token_hash=hashlib.sha256(
            token.encode()
        ).hexdigest())
    except CIIntegrationConfig.DoesNotExist:
        return JsonResponse({'error': 'invalid_token'}, status=401)

    data = json.loads(request.body)
    env = data.get('env', 'staging')
    suite_slugs = data.get('suites', ['all'])
    deploy_id = data.get('deploy_id', '')

    if suite_slugs == ['all']:
        suites = APITestSuite.objects.filter(target_env=env, is_active=True)
    else:
        suites = APITestSuite.objects.filter(
            slug__in=suite_slugs, target_env=env, is_active=True
        )

    run_ids = []
    for suite in suites:
        run = APITestRun.objects.create(
            suite=suite,
            trigger_source='ci',
            deploy_id=deploy_id,
            env=env,
            status='queued',
        )
        execute_api_test_suite.delay(run.id)
        run_ids.append(run.id)

    return JsonResponse({'run_ids': run_ids, 'status': 'queued'})
```

---

## 8. Models

```python
class APITestSuite(models.Model):
    ENV = [('staging', 'Staging'), ('production', 'Production'), ('local', 'Local')]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    tags = models.JSONField(default=list)
    target_env = models.CharField(max_length=20, choices=ENV, default='staging')
    base_url_override = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    auth_setup = models.JSONField(
        default=dict,
        help_text='Suite-level auth setup step (e.g., obtain JWT before running)'
    )
    # CI settings
    blocks_deploy_on_fail = models.BooleanField(default=False)
    pass_rate_threshold = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('95.00')
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def last_run(self):
        return self.runs.order_by('-started_at').first()


class APITestCase(models.Model):
    HTTP_METHODS = [
        ('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'),
        ('PATCH', 'PATCH'), ('DELETE', 'DELETE'),
    ]
    ON_FAIL = [('continue', 'Continue'), ('abort', 'Abort Suite')]

    suite = models.ForeignKey(
        APITestSuite, on_delete=models.CASCADE, related_name='test_cases'
    )
    name = models.CharField(max_length=300)
    order = models.PositiveSmallIntegerField(default=0)
    method = models.CharField(max_length=10, choices=HTTP_METHODS)
    path = models.CharField(max_length=500, help_text='e.g. /exams/{exam_id}/')
    path_variables = models.JSONField(default=dict)
    headers = models.JSONField(default=dict)
    request_body = models.JSONField(null=True, blank=True)
    expected_status = models.PositiveSmallIntegerField()
    assertions = models.JSONField(
        default=list,
        help_text='List of {type, path, operator, value} assertion objects'
    )
    openapi_schema_ref = models.CharField(max_length=200, blank=True)
    max_latency_ms = models.IntegerField(null=True, blank=True)
    on_fail = models.CharField(max_length=10, choices=ON_FAIL, default='continue')
    # Fixture: output of this test available as named variable
    exports_fixture = models.CharField(max_length=100, blank=True)
    export_json_path = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['suite', 'order']


class APITestRun(models.Model):
    STATUS = [
        ('queued', 'Queued'),
        ('running', 'Running'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('aborted', 'Aborted'),
    ]
    TRIGGER = [
        ('manual', 'Manual'),
        ('ci', 'CI Pipeline'),
        ('scheduled', 'Scheduled'),
        ('newman', 'Newman/Postman'),
    ]

    suite = models.ForeignKey(
        APITestSuite, on_delete=models.CASCADE, related_name='runs'
    )
    triggered_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    trigger_source = models.CharField(max_length=20, choices=TRIGGER)
    deploy_id = models.CharField(max_length=100, blank=True)
    env = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS, default='queued')
    total_tests = models.IntegerField(default=0)
    passed_tests = models.IntegerField(default=0)
    failed_tests = models.IntegerField(default=0)
    pass_rate_pct = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    duration_ms = models.IntegerField(null=True, blank=True)
    ci_webhook_sent = models.BooleanField(default=False)
    ci_webhook_payload = models.JSONField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['suite', '-started_at']),
            models.Index(fields=['status', 'started_at']),
        ]


class APITestCaseResult(models.Model):
    STATUS = [('pass', 'Pass'), ('fail', 'Fail'), ('skip', 'Skip')]

    run = models.ForeignKey(
        APITestRun, on_delete=models.CASCADE, related_name='case_results'
    )
    test_case = models.ForeignKey(
        APITestCase, on_delete=models.CASCADE, related_name='results'
    )
    status = models.CharField(max_length=5, choices=STATUS)
    actual_status_code = models.IntegerField(null=True)
    actual_latency_ms = models.IntegerField(null=True)
    response_body = models.JSONField(null=True, blank=True)
    assertion_results = models.JSONField(
        default=list,
        help_text='List of {assertion, passed, actual_value} objects'
    )
    schema_validation_errors = models.JSONField(default=list)
    error_message = models.TextField(blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['run', 'test_case__order']


class APIContractTest(models.Model):
    STATUS = [('pass', 'Pass'), ('warn', 'Warn'), ('fail', 'Fail')]

    name = models.CharField(max_length=200)
    provider = models.CharField(max_length=100)
    consumer = models.CharField(max_length=100)
    contract_spec = models.JSONField(
        help_text='Pact-compatible contract specification'
    )
    current_status = models.CharField(max_length=5, choices=STATUS, default='pass')
    last_run_at = models.DateTimeField(null=True, blank=True)
    last_failure_reason = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)


class APIChangelogEntry(models.Model):
    CHANGE_TYPE = [
        ('breaking', 'Breaking Change'),
        ('addition', 'Addition'),
        ('modification', 'Modification'),
        ('deprecation', 'Deprecation'),
    ]

    version_from = models.CharField(max_length=20)
    version_to = models.CharField(max_length=20)
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE)
    endpoint = models.CharField(max_length=300)
    description = models.TextField()
    affected_suite_slugs = models.JSONField(default=list)
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-detected_at']


class CIIntegrationConfig(models.Model):
    name = models.CharField(max_length=100)
    ci_token_hash = models.CharField(max_length=64, unique=True)
    result_webhook_url = models.URLField()
    pass_rate_threshold = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('95.00')
    )
    blocking_suite_slugs = models.JSONField(default=list)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    last_used_from_ip = models.GenericIPAddressField(null=True, blank=True)
```

---

## 9. Celery Tasks

```python
@shared_task(queue='qa_tests', bind=True, max_retries=0)
def execute_api_test_suite(self, run_id: int):
    """Executes all test cases in a suite sequentially, with fixture sharing."""
    run = APITestRun.objects.select_related('suite').get(id=run_id)
    suite = run.suite
    run.status = 'running'
    run.save(update_fields=['status'])

    test_cases = suite.test_cases.order_by('order')
    run.total_tests = test_cases.count()
    run.save(update_fields=['total_tests'])

    base_url = suite.base_url_override or ENV_BASE_URLS.get(suite.target_env)
    fixtures = {}  # shared across test cases in this run

    # Auth setup step
    if suite.auth_setup:
        auth_token = _execute_auth_setup(suite.auth_setup, base_url)
        fixtures['auth_token'] = auth_token

    passed = 0
    failed = 0
    aborted = False

    for tc in test_cases:
        if aborted:
            APITestCaseResult.objects.create(
                run=run, test_case=tc, status='skip'
            )
            continue

        result = _execute_test_case(tc, base_url, fixtures)
        case_result = APITestCaseResult.objects.create(
            run=run,
            test_case=tc,
            status='pass' if result['passed'] else 'fail',
            actual_status_code=result['status_code'],
            actual_latency_ms=result['latency_ms'],
            response_body=result['response_body'],
            assertion_results=result['assertion_results'],
            schema_validation_errors=result['schema_errors'],
            error_message=result.get('error', ''),
        )

        if result['passed']:
            passed += 1
            # Export fixture for downstream test cases
            if tc.exports_fixture and tc.export_json_path:
                fixtures[tc.exports_fixture] = _extract_json_path(
                    result['response_body'], tc.export_json_path
                )
        else:
            failed += 1
            if tc.on_fail == 'abort':
                aborted = True

    pass_rate = (Decimal(passed) / Decimal(run.total_tests) * 100) if run.total_tests else Decimal('0')
    run.passed_tests = passed
    run.failed_tests = failed
    run.pass_rate_pct = pass_rate
    run.status = 'passed' if failed == 0 else 'failed'
    run.completed_at = timezone.now()
    run.duration_ms = int(
        (run.completed_at - run.started_at).total_seconds() * 1000
    )
    run.save()

    # Send CI webhook if triggered by CI
    if run.trigger_source == 'ci':
        send_ci_webhook.delay(run.id)


@shared_task(queue='qa_tests')
def send_ci_webhook(run_id: int):
    run = APITestRun.objects.select_related('suite').get(id=run_id)
    config = CIIntegrationConfig.objects.first()  # or look up by token
    if not config or not config.result_webhook_url:
        return

    is_blocking = run.suite.slug in config.blocking_suite_slugs
    payload = {
        'run_id': run.id,
        'suite': run.suite.name,
        'env': run.env,
        'deploy_id': run.deploy_id,
        'pass': run.passed_tests,
        'fail': run.failed_tests,
        'pass_rate': float(run.pass_rate_pct),
        'blocking': is_blocking and run.status == 'failed',
        'duration_ms': run.duration_ms,
    }
    resp = requests.post(
        config.result_webhook_url,
        json=payload,
        headers={'X-Srav-Signature': _sign_payload(payload)},
        timeout=15,
    )
    run.ci_webhook_sent = True
    run.ci_webhook_payload = payload
    run.save(update_fields=['ci_webhook_sent', 'ci_webhook_payload'])


@shared_task(queue='qa_tests')
def generate_api_changelog(version_from: str, version_to: str, spec_from: dict, spec_to: dict):
    """
    Called after each deploy. Diffs two OpenAPI specs and stores changelog entries.
    Marks affected suites based on endpoint matching.
    """
    changes = diff_openapi_specs(spec_from, spec_to)
    for change in changes:
        affected = _find_affected_suites(change['endpoint'])
        APIChangelogEntry.objects.create(
            version_from=version_from,
            version_to=version_to,
            change_type=change['type'],
            endpoint=change['endpoint'],
            description=change['description'],
            affected_suite_slugs=[s.slug for s in affected],
        )
```

---

## 10. Assertion Engine

Each test case assertion is a JSON object:

```json
{
  "type": "json_path",
  "path": "$.data.id",
  "operator": "equals",
  "value": "{exam_id_from_fixture}"
}
```

Supported assertion types:

| Type | Operators | Example |
|---|---|---|
| `json_path` | `equals`, `not_equals`, `contains`, `in`, `exists`, `not_exists` | `$.data.status == "live"` |
| `status_code` | `equals`, `in` | `status_code in [200, 201]` |
| `latency` | `less_than` | `response.time < 800ms` |
| `header` | `equals`, `contains`, `exists` | `Content-Type contains "application/json"` |
| `schema` | `valid_against` | `response validates $.components.schemas.Exam` |

Assertion processing:

```python
def _run_assertion(assertion: dict, response, fixtures: dict) -> dict:
    value = _resolve_fixture_refs(assertion['value'], fixtures)
    actual = _extract_value(assertion['type'], assertion.get('path'), response)
    passed = _evaluate_operator(actual, assertion['operator'], value)
    return {
        'assertion': assertion,
        'actual_value': actual,
        'passed': passed,
    }
```

---

## 11. Redis Caching

```python
# Live run status cache (rebuilt every 5s by Celery update)
LIVE_RUNS_KEY = 'qa:api_tests:live_runs'
LIVE_RUNS_TTL = 10  # seconds

# Suite summary cache (rebuilt on run completion)
SUITE_SUMMARY_KEY = 'qa:api_tests:suite:{suite_id}:summary'
SUITE_SUMMARY_TTL = 300  # 5 min

# CI config cache (rebuilt on save)
CI_CONFIG_KEY = 'qa:api_tests:ci_config'
CI_CONFIG_TTL = 600  # 10 min
```

---

## 12. Security

- `qa.run_api_tests` permission required for all test execution
- CI token stored as SHA-256 hash only; raw token shown once at generation time
- Test runs against production require additional `qa.run_api_tests_production` permission
- Response bodies from production runs: truncated to 10KB, PII fields auto-redacted per `PII_FIELDS` setting
- Webhook signature: `HMAC-SHA256(json.dumps(payload, sort_keys=True), SRAV_INTERNAL_SECRET)`
- Rate limit: CI trigger endpoint 10 req/min per token (prevents CI loop storms)
- Test case path validated: must match `^/[a-zA-Z0-9/_{}?=&%-]+$`; no external URLs allowed (prevents SSRF from test cases calling arbitrary URLs)
- `base_url_override` validated against allowlist `ALLOWED_TEST_BASE_URLS` in Django settings

---

## 13. DB Schema

```sql
qa_apitestsuite (id, name, slug, tags jsonb, target_env, base_url_override,
  is_active, auth_setup jsonb, blocks_deploy_on_fail, pass_rate_threshold,
  created_by_id, created_at, updated_at)

qa_apitestcase (id, suite_id, name, order, method, path, path_variables jsonb,
  headers jsonb, request_body jsonb, expected_status, assertions jsonb,
  openapi_schema_ref, max_latency_ms, on_fail, exports_fixture,
  export_json_path)

qa_apitestrun (id, suite_id, triggered_by_id, trigger_source, deploy_id, env,
  status, total_tests, passed_tests, failed_tests, pass_rate_pct,
  duration_ms, ci_webhook_sent, ci_webhook_payload jsonb,
  started_at, completed_at)

qa_apitestcaseresult (id, run_id, test_case_id, status, actual_status_code,
  actual_latency_ms, response_body jsonb, assertion_results jsonb,
  schema_validation_errors jsonb, error_message, executed_at)

qa_apicontracttest (id, name, provider, consumer, contract_spec jsonb,
  current_status, last_run_at, last_failure_reason, is_active)

qa_apichangelogentry (id, version_from, version_to, change_type, endpoint,
  description, affected_suite_slugs jsonb, detected_at, resolved)

qa_ciintegrationconfig (id, name, ci_token_hash, result_webhook_url,
  pass_rate_threshold, blocking_suite_slugs jsonb,
  created_by_id, created_at, last_used_at, last_used_from_ip)

-- Indexes
CREATE INDEX ON qa_apitestrun (suite_id, started_at DESC);
CREATE INDEX ON qa_apitestrun (status, started_at);
CREATE INDEX ON qa_apitestcaseresult (run_id, test_case_id);
CREATE INDEX ON qa_apichangelogentry (detected_at DESC, resolved);
```

---

## 14. Validation Rules

| Rule | Detail |
|---|---|
| Suite slug | Unique, alphanumeric + hyphens, auto-generated from name |
| Test case path | Must begin with `/`; no absolute URLs (SSRF prevention) |
| Expected status | 100–599 only |
| Max latency assertion | Must be positive integer in ms |
| Run concurrency | Max 5 simultaneous suite runs per environment; 6th queued |
| Production runs | Require `qa.run_api_tests_production` permission |
| Response body retention | Truncated to 10KB; PII fields redacted before storage |
| Sync log retention | Auto-deleted after 60 days via nightly Celery task |
| CI token | Minimum 32-character random string; SHA-256 hashed before storage |
| Export path (fixture) | JSONPath syntax validated; must resolve to scalar or array |
