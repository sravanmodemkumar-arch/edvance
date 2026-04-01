# 40 — Deployment & Release Tracker

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Deployment & Release Tracker |
| Route | `/exec/deployments/` |
| Django view | `DeploymentTrackerView` |
| Template | `exec/deployments.html` |
| Priority | **P2** |
| Nav group | Engineering |
| Required roles | `cto` · `devops` · `sre` · `backend_engineer` · `frontend_engineer` · `superadmin` |
| COO access | Read-only (no deploy actions) |
| CEO access | Read-only |
| CFO / Others | Denied |
| HTMX poll — deployment list | Every 60s |
| Cache | Deployment list: Redis TTL 55s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · danger `#EF4444` · warn `#F59E0B` · success `#22C55E` |

---

## 2. Purpose & Business Logic

**Why deployment visibility matters at EduForge's scale:**

With 74K concurrent students and zero tolerance for exam-day failures, every production deployment is a risk event. The CTO needs to know:
- What version of each service is currently running in production?
- Who deployed it, when, and from which commit?
- Were there DB migrations? (migration failures = exam data corruption risk)
- Is there a broken deployment right now? What's the rollback path?
- Is today an exam day? (deployments should be blocked during live exams)

**The exam-day deployment lock:**

If `war:peak_active` Redis flag is set (concurrent users > 10,000), all production deployment actions are automatically blocked with: "Deployment blocked — exam peak active. {N} students in live exams. CTO can override."

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All (read-only) | None |
| CTO | All sections | Rollback (one-click), unblock deployment during peak (override) |
| DevOps / SRE | All sections | Deploy (via CI/CD, logged here), rollback |
| Backend / Frontend Engineer | All sections (read) | Cannot rollback — DevOps/CTO only |
| COO | Current version summary only | None |
| CFO | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Current Production Versions

**Purpose:** The CTO's "what is running right now" single source of truth.

**UI elements:**
```
PRODUCTION — CURRENT VERSIONS
─────────────────────────────────────────────────────────────────────────────
Service              Version    SHA        Deployed       By          Status
─────────────────────────────────────────────────────────────────────────────
API Gateway          v2.14.1    a4f8c2d    2h ago         Rahul (CI)  ✅ Healthy
Exam Engine          v3.8.4     b2e9d1a    4h ago         Rahul (CI)  ✅ Healthy
Auth Service         v1.22.0    c8f4a2b    Yesterday      Priya (CI)  ✅ Healthy
File Storage         v1.8.2     d1a4b8c    3 days ago     Kiran (CI)  ⚠ Degraded
Notification Svc     v2.4.1     e2b8c4d    Yesterday      Rahul (CI)  ✅ Healthy
Proctoring Engine    v1.6.0     f4c2d8a    1 week ago     Priya (CI)  ✅ Healthy
```

- SHA: 7-char short SHA, copyable, links to GitHub commit
- "By (CI)": deployed via CI/CD pipeline (automated)
- Status dot: pulled from Platform Health (02) — same service status
- Degraded service row: `border-l-4 border-amber-500`
- Click row → Deployment Detail Drawer (Drawer-J, 600px)

**HTMX:** `id="current-versions"` `hx-trigger="load, every 60s"` — data from `Deployment.objects.latest()` per service.

---

### Section 2 — Deployment History Table

**Purpose:** Full audit trail of all production deployments — who, when, what changed, and did it cause issues.

**UI elements:**
```
DEPLOYMENT HISTORY                    [Service: All ▾] [Status: All ▾] [🔍]
─────────────────────────────────────────────────────────────────────────────
#    Service        Version  SHA      By       Time        Status     ⋯
─────┼───────────────┼─────────┼────────┼────────┼────────────┼──────────┼──
#284 Exam Engine    v3.8.4   b2e9d1a  Rahul    2h ago      ✅ Success  ⋯
#283 API Gateway    v2.14.1  a4f8c2d  Rahul    4h ago      ✅ Success  ⋯
#282 File Storage   v1.8.3   d9f2a1b  Priya    6h ago      🔴 Failed   ⋯
#281 File Storage   v1.8.2   d1a4b8c  Priya    8h ago      ✅ Success  ⋯
#280 Auth Service   v1.22.0  c8f4a2b  Auto CI  Yesterday   ✅ Success  ⋯
```

- Failed rows: `bg-red-950/15 border-l-4 border-red-500`
- ⋯ menu: View Detail · Rollback to this version (CTO/DevOps only) · View Logs · Link to Incident
- Pagination: 20 rows per page

**"Rollback" action:**
- Modal: "Roll back {service} from v3.8.4 to v3.8.3?"
- Shows: last known stable version, migration implications ("⚠ v3.8.4 included DB migration — rollback will NOT reverse migration"), estimated impact, confirmation phrase required: "ROLLBACK {SERVICE}"
- POST `/exec/deployments/actions/rollback/` → triggers CI/CD rollback pipeline via webhook, creates `Deployment` record with `type='rollback'`, audit log, auto-creates P1 incident

**Exam peak lock:** If `war:peak_active` Redis flag is set, "Rollback" button is grey with tooltip "Blocked during exam peak — CTO override available."

**HTMX:** `id="deployment-history"` `hx-trigger="load, every 60s"` — `Deployment.objects.order_by('-deployed_at')[:20]`.

---

### Section 3 — DB Migration Log

**Purpose:** DB migrations are the highest-risk deployment artifact. A failed migration mid-exam = data corruption. This section tracks all migrations separately.

**UI elements:**
```
DB MIGRATION LOG                                      [Last 30 Days]
─────────────────────────────────────────────────────────────────────────────
Migration             Service       Run At       Duration  Status   Reversible?
──────────────────────┼─────────────┼─────────────┼─────────┼─────────┼──────────
0042_add_exam_pause   ExamEngine    2h ago        1.2s      ✅ OK     No
0041_index_attempts   ExamEngine    4h ago        8.4s      ✅ OK     Yes
0038_add_bgv_expiry   UserService   Yesterday     2.1s      ✅ OK     Yes
0036_alter_invoice    BillingService 3 days ago   14.2s     ✅ OK     No
```

- "Reversible?" column: amber "No" for irreversible migrations — CTO must acknowledge before any deploy that includes these
- Duration > 10s: amber (long migrations block table during exam = risk)
- Failed migration row: red, auto-creates P0 incident

---

### Section 4 — CI/CD Pipeline Health

**Purpose:** Shows the health of the CI/CD pipeline itself — are builds passing? Are there queued deployments blocked?

**UI elements:**
```
CI/CD PIPELINE — GitHub Actions
─────────────────────────────────────────────────────────────────────────────
Branch: main    Last build: ✅ #284 — 2h ago     Queue: 0 pending
Average build time: 4m 22s      Success rate (7d): 96.4%

RECENT PIPELINE RUNS
#284  main → API Gateway    ✅ 4m 18s  Rahul    2h ago
#283  main → Exam Engine    ✅ 3m 52s  Rahul    4h ago
#282  main → File Storage   🔴 2m 04s  Priya    6h ago  [View Logs →]
```

- Failed run: "View Logs →" links to CI/CD log (external URL — opens in new tab)
- Exam-day lock indicator: if peak active → "🔴 DEPLOYMENT LOCK ACTIVE — Live exam in progress"

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Deployment & Release Tracker                         [↺ Refresh]           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  PRODUCTION — CURRENT VERSIONS                                              ║
║  API Gateway    v2.14.1   a4f8c2d   2h ago   Rahul(CI)   ✅                 ║
║  Exam Engine    v3.8.4    b2e9d1a   4h ago   Rahul(CI)   ✅                 ║
║  File Storage   v1.8.2    d1a4b8c   3d ago   Kiran(CI)   ⚠ Degraded        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  DEPLOYMENT HISTORY          [Service ▾] [Status ▾] [🔍]                   ║
║  #284 Exam Engine   v3.8.4  b2e9d1a  Rahul  2h ago  ✅ Success  [⋯]        ║
║  #282 File Storage  v1.8.3  d9f2a1b  Priya  6h ago  🔴 Failed   [⋯]        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  DB MIGRATION LOG                  CI/CD PIPELINE HEALTH                   ║
║  0042_add_exam_pause  2h  1.2s ✅   Last build: ✅ #284  2h ago             ║
║  0036_alter_invoice   3d 14.2s ✅⚠  Success rate (7d): 96.4%               ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Drawer-J — Deployment Detail (600px)

```
┌──────────────────────────────────────────────────────────┐
│  Deployment #284 — Exam Engine v3.8.4        ✅ Success [✕]│
│  ─────────────────────────────────────────────────────── │
│  [Summary ●]  [Commit Log]  [Services Changed]  [Migrations]│
│  ─────────────────────────────────────────────────────── │
│  Deployed:    2h ago (14:22 IST)  by Rahul (CI/CD)       │
│  SHA:         b2e9d1a  [Copy]  [View on GitHub ↗]        │
│  Duration:    3m 52s                                      │
│  Environment: Production                                  │
│  ─────────────────────────────────────────────────────── │
│  MIGRATIONS                                               │
│  0042_add_exam_pause_field — 1.2s — ✅ — Irreversible     │
│  ─────────────────────────────────────────────────────── │
│  [Rollback to v3.8.3]  (CTO/DevOps only)                 │
└──────────────────────────────────────────────────────────┘
```

---

## 7. Component Architecture

| Component | File | Props |
|---|---|---|
| `CurrentVersionRow` | `components/deploy/version_row.html` | `service, version, sha, deployed_at, deployed_by, health_status` |
| `DeploymentHistoryRow` | `components/deploy/history_row.html` | `deployment, can_rollback, exam_peak_active` |
| `DeploymentStatusBadge` | `components/deploy/status_badge.html` | `status (success/failed/in_progress/rolled_back)` |
| `MigrationRow` | `components/deploy/migration_row.html` | `migration_name, service, run_at, duration_s, status, reversible` |
| `DeploymentDrawer` | `components/deploy/drawer.html` | `deployment_id, can_rollback` |
| `RollbackModal` | `components/deploy/rollback_modal.html` | `deployment_id, service, current_version, target_version, has_migrations` |
| `ExamPeakLockBanner` | `components/deploy/exam_peak_lock.html` | `is_cto (bool for override)` |

---

## 8. HTMX Architecture

| `?part=` | Target | Poll | Trigger |
|---|---|---|---|
| `current-versions` | `#current-versions` | 60s | load |
| `history` | `#deployment-history` | 60s | load + filter |
| `migrations` | `#migration-log` | None | load |
| `cicd` | `#cicd-health` | 60s | load |
| `deploy-drawer` | `#drawer-container` | None | row click |

---

## 9. Backend View & API

```python
class DeploymentTrackerView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_deployments"

    def get(self, request):
        allowed = {"cto","devops","sre","backend_engineer",
                   "frontend_engineer","ceo","coo","superadmin"}
        if request.user.role not in allowed:
            return redirect("exec:dashboard")

        r = get_redis_connection()
        exam_peak_active = bool(r.get("war:peak_active"))
        can_rollback = request.user.role in {"cto","devops","sre","superadmin"}

        if _is_htmx(request):
            part = request.GET.get("part","")
            ctx = {"exam_peak_active": exam_peak_active, "can_rollback": can_rollback}
            dispatch = {
                "current-versions": "exec/deploy/partials/current_versions.html",
                "history":          "exec/deploy/partials/history.html",
                "migrations":       "exec/deploy/partials/migrations.html",
                "cicd":             "exec/deploy/partials/cicd.html",
                "deploy-drawer":    "exec/deploy/partials/drawer.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "exec/deployments.html",
                      {"exam_peak_active": exam_peak_active, "can_rollback": can_rollback})
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/deployments/actions/rollback/` | `portal.rollback_deployment` (CTO/DevOps) | Trigger CI/CD webhook, create Deployment record (type=rollback), P1 incident, audit log |
| POST | `/exec/deployments/actions/override-lock/` | `portal.override_exam_lock` (CTO only) | Set `deploy:lock_override:{user_id}` Redis key TTL 30min |

---

## 10. Database Schema

```python
class Deployment(models.Model):
    service         = models.CharField(max_length=50, db_index=True)
    version         = models.CharField(max_length=20)
    git_sha         = models.CharField(max_length=40)
    git_sha_short   = models.CharField(max_length=7)
    branch          = models.CharField(max_length=100, default="main")
    deployed_by     = models.CharField(max_length=100)  # "Rahul" or "CI/CD"
    deployed_at     = models.DateTimeField(db_index=True)
    duration_seconds= models.FloatField(null=True)
    status          = models.CharField(max_length=20,
                          choices=[("success","Success"),("failed","Failed"),
                                   ("in_progress","In Progress"),
                                   ("rolled_back","Rolled Back")])
    deploy_type     = models.CharField(max_length=20, default="deploy",
                          choices=[("deploy","Deploy"),("rollback","Rollback"),
                                   ("hotfix","Hotfix")])
    triggered_by    = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                         on_delete=models.SET_NULL)
    cicd_run_url    = models.URLField(blank=True)
    notes           = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=["service","-deployed_at"])]


class DBMigration(models.Model):
    deployment      = models.ForeignKey(Deployment, on_delete=models.CASCADE,
                                         related_name="migrations")
    migration_name  = models.CharField(max_length=200)
    service         = models.CharField(max_length=50)
    run_at          = models.DateTimeField()
    duration_seconds= models.FloatField()
    status          = models.CharField(max_length=20)
    is_reversible   = models.BooleanField(default=True)
    rollback_sql    = models.TextField(blank=True)  # pre-written rollback SQL if any
```

---

## 11. Validation Rules

| Action | Validation |
|---|---|
| Rollback | Exam peak lock: blocked unless `deploy:lock_override:{user_id}` Redis key exists. Target version must exist in deployment history. Confirmation phrase: "ROLLBACK {SERVICE_NAME}" (case-sensitive). |
| Lock Override | CTO only. Creates `AuditLog` entry with reason. Expires in 30 minutes. |

---

## 12. Security Considerations

- Rollback triggers CI/CD webhook — webhook secret stored in AWS Secrets Manager, never in code
- Every rollback creates P1 incident automatically (rollbacks are operational events, not routine)
- All deployment actions logged in AuditLog with SHA, version, actor, timestamp
- Git SHA links to GitHub — external link, opens new tab, no sensitive data in URL

---

## 13. Edge Cases

| State | Behaviour |
|---|---|
| Exam peak active + rollback attempted | Button disabled. "EXAM PEAK ACTIVE — {N} students in live exams. CTO can override." |
| CI/CD webhook fails | Rollback record created as "failed". P1 incident upgraded to P0. Manual rollback instructions shown. |
| Migration marked irreversible + rollback requested | Extra warning modal step: "⚠ This deployment contains irreversible DB migration 0042_add_exam_pause. Rolling back the code WILL NOT reverse the migration. Data schema will remain at v3.8.4 while code rolls back to v3.8.3. This may cause errors. Are you sure?" — requires CTO confirmation. |
| Deployment in_progress | Row shows spinner. Rollback disabled: "Deployment in progress — wait for completion." |

---

## 14. Performance & Scaling

- Deployment history: bounded dataset (max ~500 deployments/year across 6 services). No pagination performance concern.
- Current versions: single `latest()` query per service — 6 queries total, fast. Cached 55s.
- CI/CD data: sourced from GitHub Actions API (webhooks push to `Deployment` model on each run) — no live API calls from this page.

---

*Last updated: 2026-03-20*
