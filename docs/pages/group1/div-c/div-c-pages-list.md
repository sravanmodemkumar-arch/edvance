# Group 1 — Division C: Engineering — Pages Reference

> **Division:** C — Engineering
> **Roles:** Platform Admin · Backend Engineer · Frontend Engineer · Mobile Engineer · DevOps/SRE · Database Administrator · Security Engineer · AI/ML Engineer
> **Base URL prefix:** `/engineering/`
> **Access Level:** Level 4 (Engineering) · Level 5 (Platform Admin — unrestricted)
> **Status key:** ✅ Spec done · 🔨 In progress · ⬜ Not started

---

## Scale Context (always keep in mind when designing every page)

| Dimension | Value |
|---|---|
| Total institution tenants | 2,050 (each = isolated PostgreSQL schema) |
| Total PostgreSQL schemas | 2,051 (2,050 tenant + 1 shared platform schema) |
| Peak concurrent users | **74,000 simultaneous exam submissions** |
| Lambda functions | ~60–80 across all services |
| Total students | 2.4M–7.6M |
| Mobile installs | 3M+ (Flutter iOS + Android) |
| Questions in bank | 2M+ |
| AWS primary region | ap-south-1 (Mumbai) · DR: ap-southeast-1 (Singapore) |
| Active CI/CD repos | ~12 (portal · mobile · infra · content · AI pipeline) |
| RDS instance | PostgreSQL 15 · Multi-AZ · db.r6g.2xlarge + 2 read replicas |
| Cache layer | Memcached (django.core.cache) — no Redis |
| CloudFront distributions | 3 (portal · static assets · API edge) |
| Monthly AI API spend | ₹8L–₹15L (LLM for MCQ generation) |
| Monthly AWS infra spend | ₹70K–₹90K (Lambda + RDS + CloudFront + ECS) |
| CERT-In breach reporting window | **6 hours** from discovery |
| DPDPA 2023 breach notification | **72 hours** to Data Protection Board |

---

## Division C — Role Summary

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 10 | Platform Admin | 5 | All tenant mgmt · user provisioning · system config · emergency overrides | Nothing blocked |
| 11 | Backend Engineer | 4 | API config · Lambda deployments · env vars · DB migrations · Celery beat · service health | Billing config |
| 12 | Frontend Engineer | 4 | HTMX templates · CDN cache invalidation · R2/S3 static assets · Core Web Vitals | DB access |
| 13 | Mobile Engineer — Flutter | 4 | Flutter builds · Hive encryption · FCM server config · App Store submission · Hive key schedule (read) | DB access · secret rotation |
| 14 | DevOps / SRE Engineer | 4 | AWS Lambda · ECS · RDS · CI/CD · auto-scaling · rollbacks · on-call · AWS costs · DNS/SSL | Content · billing |
| 15 | Database Administrator | 4 | PostgreSQL all 2,051 schemas · backups · migrations · query tuning · PITR · RDS params · PgBouncer config | Business config |
| 16 | Security Engineer | 4 | JWT secrets · KMS · WAF rules · CERT-In reports · DPDPA breach · VAPT scheduling · OAuth app registry | Content · billing |
| 17 | AI / ML Engineer | 4 | MCQ generation pipeline · LLM model config · prompt versioning · AI API cost · rejection thresholds | Content approval |

---

## Platform Admin — Pages (Role 10) · 3 pages (+ 2 tabs via G29, G30)

> Level 5 — no restrictions. Highest blast radius in system. Every action 2FA-gated and audit-logged with IP.

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| C-01 | Tenant Manager | `/engineering/tenants/` | `c-01-tenant-manager.md` | P0 | ⬜ | Full CRUD for all 2,050 institution tenants: schema provisioning · plan assignment · suspension (read-only mode) · hard delete with 30-day grace period · emergency data wipe · Celery async provisioning with live progress bar · schema health check · tenant impersonation (Platform Admin only) · **[G29] Tenant Storage Quota**: storage column in tenant list (current size · quota · % used — green <70% / amber 70–90% / red >90%) · per-plan defaults (Starter: 2GB · Growth: 10GB · Pro: 25GB · Enterprise: custom) · quota editor in tenant-detail-drawer → Storage tab (top-10 tables by size · index sizes · quota edit field) · daily Celery alert at 80% threshold · read-only mode auto-activated at 100% · bulk quota adjustment for plan upgrades |
| C-02 | Staff Account Manager | `/engineering/staff/` | `c-02-staff-accounts.md` | P1 | ⬜ | All 81 platform staff accounts across 15 divisions: role assignment · 2FA enforcement per level · account suspension · login history · failed login tracking · quarterly access review workflow · SSO (Google Workspace SAML) config · emergency account lock · **[G30] Escalation Tree tab**: on-call escalation chains for 5 incident types (P0 Exam Day / P1 Degradation / Security Breach / Data Breach-DPDPA / DB Emergency) · per chain: primary → secondary → tech lead → CTO/DPO with phone + Signal + WhatsApp + email · "Out of Office" toggle per person (auto-skips to next in chain) · "Send Test Alert" verifies full chain is reachable · last-tested timestamp per tree (monthly recommended) · integration with C-18: P0 incident creation auto-triggers P0 escalation tree |
| C-03 | System Configuration | `/engineering/system-config/` | `c-03-system-config.md` | P1 | ⬜ | Global platform settings: maintenance mode toggle (affects all 2,050 portals simultaneously) · session timeouts per access level · global rate limit overrides · CORS allowed origins · AWS SES sender domain config · cache TTL defaults · emergency master kill switches · feature flag master override |

---

## Backend Engineer — Pages (Role 11) · 3 pages (+ 2 tabs via G1, G2)

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| C-04 | API Health Monitor | `/engineering/api-health/` | `c-04-api-health.md` | P0 | ✅ | All Lambda endpoints: P50/P95/P99 latency per endpoint · error rate by HTTP status code · cold start frequency · throttle events · exam-critical SLA tracking (exam submit < 200ms · result fetch < 500ms) · API version registry (v1/v2/v3) · deprecation tracker with sunset countdowns · endpoint dependency map |
| C-21 | Feature Flag Manager | `/engineering/feature-flags/` | `c-21-feature-flags.md` | P1 | ⬜ | Per-feature-flag enable/disable per environment (staging/production) without code deploy · flag types: boolean · percentage rollout (0–100% of tenants) · variant value · per-tenant override for beta testing · flag groups: Frontend / Backend / Mobile / AI / Experimental · flag expiry date (auto-disables temporary features) · flag history (who changed · what value · when) · rollout safety: shows affected tenant count before applying >0% rollout · integration with C-05: new deployment can auto-enable specific flags · all production flag changes 2FA-gated · rollout >50% requires Platform Admin approval |
| C-05 | Service Deployment Manager | `/engineering/deployments/` | `c-05-deployments.md` | P1 | ⬜ | Lambda function version history · blue/green weighted routing (e.g. 95%/5% canary) · Lambda alias management ($LATEST vs named versions) · one-click rollback to any previous version · pre/post-deploy health check automation · deployment log with actor + timestamp · integration with CI/CD (C-09) and Release Manager (Div B page 03) · **[G1] Environment Variables tab**: per-function env var viewer + editor (value references AWS Secrets Manager ARN — raw values never stored in Django DB) · diff view between deployed vs pending env vars · deploy-on-save with health check · **[G2] Scheduled Jobs tab**: full Celery beat task registry — task name · queue · schedule (cron/interval) · last run time · next run time · last run status (success/failure) · average duration · pause/resume per task · trigger manual run now · execution history (last 30 runs per task) |

---

## Frontend Engineer — Pages (Role 12) · 1 page (+ 1 tab via G3)

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| C-06 | CDN & Asset Manager | `/engineering/cdn/` | `c-06-cdn-assets.md` | P2 | ⬜ | CloudFront cache invalidation (path patterns · wildcard `/static/*` · emergency full purge) · R2/S3 static asset browser (CSS · JS · images · fonts · WOFF2) · cache hit rate per distribution · asset version registry (content-hash file names) · Brotli/gzip compression status · HTMX template deployment log · CDN cost per GB · **[G3] Performance Monitor tab**: real-user Core Web Vitals per page path (LCP · FID · CLS · TTFB) sourced from CloudWatch RUM · P75 / P95 percentiles · JS error rate and top error messages · page load time trend (7-day) · device/OS breakdown · alert threshold config (LCP > 2.5s → amber, > 4s → red) |

---

## Mobile Engineer — Pages (Role 13) · 1 page (+ 1 tab via G28)

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| C-07 | Mobile Build Pipeline | `/engineering/mobile-builds/` | `c-07-mobile-builds.md` | P2 | ⬜ | Flutter build status iOS + Android · GitHub Actions build logs (live tail) · code signing management (iOS provisioning profiles · Apple certificates · Android keystore) · App Store Connect + Google Play submission tracker · Firebase App Distribution for beta · Crashlytics deep analysis (crash-free rate · ANR rate · affected device models · OS version breakdown) · build artifact registry with version tagging · dSYM/ProGuard symbol upload status · **[G28] FCM Delivery Monitor tab**: push notification delivery rate % (sent / delivered / failed by platform) · iOS vs Android delivery split · device token health (valid vs expired/unregistered — high % invalid = uninstalled apps) · active FCM topics with subscriber counts · recent notification log (last 50: topic · sent · delivered · failed · timestamp) · notification template manager (predefined payloads: question_returned · exam_starting · key_rotation_reminder · app_update) · "Send Test" per topic to verify routing |

---

## DevOps / SRE Engineer — Pages (Role 14) · 5 pages (+ 2 tabs via G11, G23)

> Most operationally critical role. Owns the platform at 74K peak exam day.

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| C-08 | Infrastructure Monitor | `/engineering/infrastructure/` | `c-08-infrastructure.md` | P0 | ⬜ | Real-time AWS: Lambda total + reserved concurrency per function · ECS cluster CPU/memory/task count · RDS primary + replicas (CPU · connections · IOPS · storage · replica lag) · Memcached hit-rate/evictions · ALB request rate + 5xx · CloudFront bandwidth + cache ratio · S3 bucket sizes · All with WRITE controls: change concurrency · restart ECS tasks · promote read replica · drain ALB target · **[G4] Celery Queues tab**: per-queue worker count (active/idle) · queue depth (messages waiting) · processed/failed tasks per hour (24h chart) · average task duration per queue · dead-letter queue (DLQ) item count with retry-all action · individual worker detail (worker hostname · current task · uptime) · worker restart action (graceful/hard) · queue-level pause/resume · **[G23] ECS Task Definition Editor** (drawer from ECS service row): current task definition (family · revision · Docker image URI + tag · CPU vCPUs · memory limit) · edit image tag (deploy new container version without full CI/CD) · edit CPU/memory with cost impact estimate · "Force New Deployment" rolling update · task definition revision history (last 10: image tag · who deployed · timestamp · status) |
| C-09 | CI/CD Pipeline Manager | `/engineering/cicd/` | `c-09-cicd.md` | P0 | ⬜ | GitHub Actions runs across all 12 repos · pipeline stages (Test → Lint → Build → Deploy Staging → QA Gate → Pre-Prod → Prod) · manual approval gate for production · parallel pipeline grid view · rollback (re-run last passing workflow) · failed pipeline log tail · integration with QA sign-off (Div B page 21) and Release Manager (Div B page 03) · deployment frequency + DORA metrics |
| C-10 | Auto-scaling & Capacity Planner | `/engineering/scaling/` | `c-10-scaling.md` | P1 | ⬜ | Lambda reserved + provisioned concurrency config per function · scheduled scaling rules (pre-warm 30 min before exam start) · ECS task min/max per service · RDS read replica add/remove · cache node scaling · exam calendar integration: upcoming peak events with estimated load · capacity simulation: "at 80K VUs — which service throttles first?" · cost impact of scaling decisions · **[G11] Exam Day Mode tab**: one-click "Activate Exam Day Mode" (2FA-gated) that simultaneously sets all exam-endpoint Lambda provisioned concurrency to max · scales ECS tasks to configured max per service · switches CloudFront to no-cache for API responses · locks production CI/CD deployments for the day (C-09 deploy button disabled) · sends Slack + email confirmation with timestamp · shows cost impact estimate before activation · "Deactivate" button reverses all effects · activation history with duration and peak metrics |
| C-19 | AWS Infrastructure Cost Monitor | `/engineering/aws-costs/` | `c-19-aws-costs.md` | P1 | ⬜ | Per-service monthly AWS spend via Cost Explorer API: Lambda invocations · RDS storage + I/O · CloudFront egress · ECS compute · S3 storage · SES · ACM · month-over-month trend · budget vs actual · cost anomaly alerts · Reserved Instance coverage % · cost breakdown per exam peak event · ₹ spend forecast |
| C-20 | DNS & Certificate Manager | `/engineering/dns-certs/` | `c-20-dns-certs.md` | P1 | ⬜ | Route53 DNS record management (A · CNAME · TXT · MX) for platform domains + 2,050 institution custom subdomains · ACM SSL certificate inventory (domain · expiry date · auto-renewal status · validation method) · expiry calendar (30/14/7 day alerts) · DNS propagation checker · certificate request workflow · CloudFront distribution ↔ cert mapping · Security Engineer read access |

---

## Database Administrator — Pages (Role 15) · 2 pages (+ 5 tabs/actions via G5, G12, G13, G20, G26)

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| C-11 | Database Admin Dashboard | `/engineering/database/` | `c-11-database.md` | P0 | ⬜ | All 2,051 PostgreSQL schemas: slow query log (> 1s) · active connections per schema · PgBouncer pool status · table sizes top-20 · index health (unused / missing / bloated indexes) · autovacuum status per table (last autovacuum time · dead tuple count · live tuple count) · lock monitoring (long-running locks with kill option) · replication lag primary → replicas · query EXPLAIN analyzer · schema size growth trend · **[G5] DB Configuration tab**: RDS parameter group editor (work_mem · shared_buffers · max_connections · autovacuum_vacuum_scale_factor · checkpoint_completion_target — all with current value · pending value · requires-restart flag) · apply changes (immediate or pending-reboot) · PgBouncer config editor (pool_size per database · max_client_conn · pool_mode · server_idle_timeout) · PostgreSQL role/grant manager per tenant schema (view GRANT tree · grant/revoke role · create read-only reporting user) · all changes 2FA-gated + logged in DB audit table · **[G20] Manual VACUUM action** (table context menu): "Trigger VACUUM ANALYZE" confirmation modal showing table name + estimated duration + last autovacuum time → Celery task executes VACUUM ANALYZE via direct RDS superuser connection bypassing PgBouncer · progress polling via HTMX · result: rows processed · dead tuples removed · index pages reclaimed · logged in DBA audit table · schema-wide VACUUM available to Platform Admin only · **[G26] Index Create/Drop actions** (index health table context menu): Create Index — enter columns + index type (btree/hash/gin/gist/brin) + optional partial WHERE condition + name · uses CREATE INDEX CONCURRENTLY (no table lock) · estimated build time + size shown before creation · progress polling via HTMX · Drop Index — shows size on disk + last used timestamp · requires typing index name to confirm · 2FA-gated · REINDEX action for corrupted indexes · all DDL logged in DBA audit table |
| C-12 | Backup & Migration Manager | `/engineering/db-migrations/` | `c-12-db-migrations.md` | P1 | ⬜ | RDS automated snapshot schedule (daily · 30-day retention) · manual snapshot on demand (before risky migrations) · PITR restore to any second in retention window · Django migration status across all 2,051 schemas · pending unapplied migrations list · selective schema migration execution · migration rollback (`migrate app 000X`) · data archival to S3 Glacier (data > 2 years old) · backup cost tracking · **[G12] Migration Matrix tab**: all 2,051 schemas in a grid — schema name · latest applied migration per app · pending migration count (0 = green · 1–3 = amber · >3 = red) · last migration timestamp · bulk "Apply pending to all schemas" action with live HTMX progress modal · filter by pending-only / healthy / specific app · selective apply: pick N schemas + apply · failures isolated per schema with error log · **[G13] Restore Verification tab**: trigger test restores from RDS snapshots to an isolated ephemeral RDS instance (db.t3.medium) — select source snapshot · verification checks: table count match · row count sample per 10 tables · referential integrity check on 5 key FK chains · Pass/Fail result with detail · auto-decommission ephemeral instance after verification · restore test history (last 12 months) · configurable monthly schedule · estimated cost shown before trigger |

---

## Security Engineer — Pages (Role 16) · 2 pages (+ 8 tabs/sections via G6, G7, G8, G16, G17, G18, G19, G24)

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| C-13 | Security Operations Dashboard | `/engineering/security/` | `c-13-security-ops.md` | P0 | ⬜ | AWS WAF rules (block · rate-limit · geo-restrict) · failed auth heatmap (IP · country · time-of-day) · account lockout event log · suspicious JWT anomaly detection · CVE tracker (pip audit + npm audit) · CERT-In incident log with 6h countdown timer · DPDPA breach tracker with 72h notification countdown · full VAPT results · dependency vulnerability scanner · active threat alerts · **[G6] VAPT Schedule tab**: penetration test engagement tracker — schedule test (date · vendor name · scope: in/out of scope URL/IP ranges · test type: black-box/grey-box/white-box) · engagement status (Scheduled → In Progress → Report Received → Findings Triaged → Closed) · findings log per engagement (severity: Critical/High/Medium/Low · CVE ref if applicable · affected component · remediation owner · due date · status) · findings import via CSV or manual entry · integration with CVE tracker: critical findings auto-create CVE tracker items · vendor NDA expiry tracking · **[G16] Data Localization Audit tab**: compliance dashboard verifying all student PII is in ap-south-1 — S3 bucket list with region column (green = ap-south-1 · red = other) · RDS + Lambda region check · "Run Audit Now" triggers Celery task calling AWS Config + S3 getBucketLocation for all buckets · violation log: out-of-region resource auto-creates DPDPA incident linked to C-18 · automated monthly audit schedule · DPO compliance export (PDF) · **[G17] CERT-In Report tab**: structured CERT-In 6-hour incident report generator — select active incident from C-18 board · pre-populated template with 12 CERT-In incident categories · fields: discovery timestamp · affected systems · estimated affected user count · attack vector · containment actions · evidence file upload · generate PDF + submission tracking number · 6-hour countdown timer from incident discovery · submission history with PDF download · DPDPA §31 72-hour DPO notification sub-workflow (draft notification → DPO email send) · **[G24] Security Audit Log tab**: structured security-specific audit trail — WAF rule changes · secret view/rotation events · OAuth app registrations/revocations · 2FA bypass events · permission escalation events · admin impersonation events · JWT compromise workflow executions · each entry: actor + role + action type + timestamp + IP + affected resource + before/after values · filter by action type / actor / date range / resource type · append-only (no delete route) · CSV export for external audit · Security Engineer + Platform Admin only |
| C-14 | Secret & Key Manager | `/engineering/secrets/` | `c-14-secrets.md` | P0 | ⬜ | Complete secret inventory: JWT signing keys · AWS KMS CMKs · RDS master credentials · Razorpay API keys (test + live) · FCM server keys · Hive AES-256 keys · S3 presign keys · SMTP credentials · OAuth client secrets · rotation schedule per secret · 2FA-gated rotation trigger · rotation history audit · AWS Secrets Manager sync status · expiry countdowns · **[G7] OAuth App Registry tab**: all OAuth 2.0 applications registered on the platform — app name · client ID (masked, last-4 visible) · allowed scopes (checkboxes) · redirect URI list · app owner (staff account) · creation date · last-used date · revoke action (2FA-gated, immediate) · new app registration wizard · scope change requires Security Engineer 2FA · **[G8] Mobile Keys tab** *(accessible to Mobile Engineer — read-only)*: Hive AES-256 key rotation schedule (current key version · rotation date · next scheduled rotation) · FCM server key expiry date · iOS APNs certificate expiry · Android keystore alias and expiry — Mobile Engineer can see dates only, no raw values, no rotation trigger · **[G18] Rotation Compliance tab**: aggregate compliance view across all 47 tracked secrets — rotation SLA per secret type (JWT: 30d · KMS CMK: 365d · RDS password: 90d · API keys: 90d · FCM: 365d) · compliance status per secret (On Track / Due Soon <7d / Overdue) · overall compliance % (target ≥ 95%) · secrets never-rotated flagged as critical · bulk rotation trigger for all overdue secrets (2FA-gated) · exportable compliance report (PDF) for security audit · next 30-day rotation calendar · **[G19] JWT Compromise Response section** *(Security Engineer + Platform Admin only)*: guided 6-step runbook — Step 1: revoke current JWT key + generate new key in AWS Secrets Manager · Step 2: bulk invalidate all active sessions across 2,050 schemas (Celery task with progress bar) · Step 3: force re-login for all active users via FCM push notification · Step 4: log incident to C-13 CERT-In tracker (pre-filled) · Step 5: email DPO with breach summary · Step 6: verify new key active in all Lambda environments — each step requires explicit confirmation · type "REVOKE-JWT" to unlock the workflow · full timestamped action log |

---

## AI / ML Engineer — Pages (Role 17) · 2 pages (+ 5 tabs/sections via G9, G14, G15, G25, G27)

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| C-15 | AI Pipeline Dashboard | `/engineering/ai-pipeline/` | `c-15-ai-pipeline.md` | P2 | ⬜ | MCQ generation pipeline: batch job status · questions generated vs target · auto-rejection funnel (hallucination · duplicate · formatting · copyright) · prompt version A/B performance comparison · LLM model tracking (Claude · GPT-4o · Gemini) · human review queue depth · review-to-approval rate · per-domain generation stats · error classification breakdown · **[G9] Pipeline Config tab**: auto-rejection threshold editor — hallucination confidence score cutoff (default 0.75, range 0–1) · duplicate cosine similarity cutoff (default 0.80) · formatting rule toggles (enforce option count ≥ 4 · explanation min length · LaTeX syntax check) · per-domain quality thresholds (e.g. GK domain stricter copyright check) · AI provider fallback order (if Claude quota exceeded → fallback to GPT-4o) · batch size per job (10–2000) · max concurrent batch jobs · all threshold changes versioned with before/after values in audit log · **[G14] Prompt Version Manager tab**: create/edit/deploy prompt versions — version label (e.g. v1.4.2) · prompt body editor with syntax highlighting (markdown/LaTeX-aware) · associated LLM model · system message · temperature + top_p config · activation state: Prod / Canary / Archived · promotion workflow: promote canary to prod requires ≥ 500 approved questions generated by the canary version · side-by-side diff between any two versions · auto-archive after 90 days inactive · all changes DB-versioned with author + timestamp + before/after diff · **[G25] Embedding Model Manager section**: active model name + version (e.g. text-embedding-3-large) + deployment date + vector dimension · embedding coverage: total questions vs questions with embeddings (progress bar — unembedded questions invisible to duplicate check) · trigger re-embedding job (select model version → shows ₹ cost estimate + duration estimate) · progress polling: questions processed / total · HNSW index rebuild status (current / stale) + "Notify DBA" button (creates C-18 task for index rebuild) · past re-embedding history (model · date · duration · cost · question count) |
| C-16 | AI Cost & Usage Monitor | `/engineering/ai-costs/` | `c-16-ai-costs.md` | P2 | ⬜ | LLM token consumption: input + output per model per day · cost per exam domain · cost per question type · monthly budget with 80% alert / 95% hard stop · wasted spend (cost of rejected questions) · model cost comparison · optimization flags (expensive prompts with high rejection rate) · ₹ spend trend MoM · cost per approved question metric · **[G15] Cost Forecast section**: month-to-date spend + projected month-end based on current daily burn rate · "Run N more batches" cost simulator (enter batch count → shows estimated token cost + whether it breaches ₹15L monthly cap) · daily burn rate trend (7 days) · days until monthly cap at current rate · budget cap editor (₹/month with 95% hard-stop config) · overage alert recipients list · model cost comparison forecast (cost differential if switching all batches to GPT-4o vs Claude) · **[G27] API Rate Limits section**: per-provider quota table (Anthropic: RPM + TPM per model · OpenAI: RPM + TPM · Google: QPM per model) · current usage % of quota (last 1-minute window) · time until quota window resets (countdown per provider) · colour indicators: green <70% · amber 70–90% · red >90% · 7-day hourly consumption chart (identify peak patterns) · overage alerts: 80% → amber + email · 95% → red + auto-pause new batch jobs · provider API status (Anthropic/OpenAI/Google: operational/degraded/outage) |

---

## Cross-Role Shared Pages · 2 pages (+ 2 tabs via G10, G21)

| # | Page Name | URL | File | Priority | Status | Description | Roles |
|---|---|---|---|---|---|---|---|
| C-17 | Centralized Log Viewer | `/engineering/logs/` | `c-17-logs.md` | P1 | ✅ | CloudWatch Logs aggregation: structured JSON search · correlation ID trace (single exam submission across all Lambda hops) · log level filter · service filter · tenant filter · time range picker · saved search queries · alert rules (log pattern → PagerDuty) · log retention policy per service | All Div C roles |
| C-18 | Engineering Incident Manager | `/engineering/incidents/` | `c-18-incidents.md` | P0 | ⬜ | Active incident board (P0–P2) · incident timeline (detection→ack→mitigate→resolve) · runbook library (30+ known incident types) · on-call schedule (current + 2 weeks) · PagerDuty + OpsGenie integration · postmortem tracker with action items · MTTR analytics · links to War Room (Div A page 32) for exam-day P0s · **[G10] Alert Rules tab**: metric alert configuration — rule builder (metric name · condition: >, >=, <, <= · threshold value · evaluation window: 1/5/15 min · consecutive breaches before alert: 1–5) · severity assignment (P0/P1/P2) · notification routing (PagerDuty policy · OpsGenie team · Slack channel · email list) · snooze policy (auto-snooze after N alerts in M hours) · active alert rules list with enable/disable per rule · alert rule test: fire a test alert to verify routing · per-rule history: last triggered · times triggered (30d) · **[G21] Runbook Editor tab**: create/edit operational runbooks — title · incident type tag (P0/P1/P2/Security Breach/Data Leak/Performance) · category tags (Lambda/ECS/RDS/Network/Security/Celery/etc.) · markdown editor with preview (headers · bullet lists · code blocks · numbered steps) · standard sections template: Symptoms · Probable Causes · Diagnostic Steps · Resolution Steps · Rollback Steps · Escalation Path · Post-Incident Actions · version history (each save = new version · diff view · restore to previous) · associate runbook with alert rules from G10 (alert auto-suggests matched runbooks in incident drawer) · search/filter by tag · Platform Admin + DevOps + Security full CRUD · other roles read-only | Platform Admin · DevOps · Security |

---

## Role-to-Page Access Matrix

| Page | Admin (10) | Backend (11) | Frontend (12) | Mobile (13) | DevOps (14) | DBA (15) | Security (16) | AI/ML (17) |
|---|---|---|---|---|---|---|---|---|
| C-01 Tenant Manager | ✅ Full | 👁 Read | — | — | 👁 Read | 👁 Read | 👁 Read | — |
| C-02 Staff Accounts | ✅ Full | — | — | — | — | — | 👁 Read | — |
| C-03 System Config | ✅ Full | — | — | — | ✅ Full | — | 👁 Read | — |
| C-04 API Health | ✅ Full | ✅ Full | 👁 Read | — | ✅ Full | — | 👁 Read | — |
| C-05 Deployments | ✅ Full | ✅ Full | 👁 Read | — | ✅ Full | — | — | — |
| C-06 CDN & Assets | ✅ Full | — | ✅ Full | — | ✅ Full | — | — | — |
| C-07 Mobile Builds | ✅ Full | — | — | ✅ Full | 👁 Read | — | — | — |
| C-08 Infrastructure | ✅ Full | 👁 Read | — | — | ✅ Full | 👁 Read | 👁 Read | — |
| C-09 CI/CD Pipeline | ✅ Full | 👁 Read | 👁 Read | 👁 Read | ✅ Full | — | — | 👁 Read |
| C-10 Auto-scaling | ✅ Full | — | — | — | ✅ Full | 👁 Read | — | — |
| C-11 Database Admin | ✅ Full | 👁 Read | — | — | 👁 Read | ✅ Full | — | — |
| C-12 DB Migrations | ✅ Full | ✅ Full | — | — | 👁 Read | ✅ Full | — | — |
| C-13 Security Ops | ✅ Full | — | — | — | 👁 Read | — | ✅ Full | — |
| C-14 Secrets | ✅ Full | — | — | 👁 Mobile tab only | ✅ Full | — | ✅ Full | — |
| C-15 AI Pipeline | ✅ Full | 👁 Read | — | — | 👁 Read | — | — | ✅ Full |
| C-16 AI Costs | ✅ Full | — | — | — | 👁 Read | — | — | ✅ Full |
| C-17 Log Viewer | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full |
| C-18 Incidents | ✅ Full | 👁 Read | — | — | ✅ Full | 👁 Read | ✅ Full | — |
| C-19 AWS Costs | ✅ Full | — | — | — | ✅ Full | — | 👁 Read | — |
| C-20 DNS & Certs | ✅ Full | — | — | — | ✅ Full | — | 👁 Read | — |
| C-21 Feature Flags | ✅ Full | ✅ Full | 👁 Read | — | ✅ Full | — | — | — |

> ✅ Full = read + write + destructive · 👁 Read = read-only · — = no access

---

## Shared Drawers (reused across div-c pages)

| Drawer | Trigger | Width | Tabs |
|---|---|---|---|
| tenant-detail-drawer | Tenant Manager row click | 720px | Config · Schema · Usage · Audit |
| lambda-function-drawer | API Health / Deployments row | 640px | Metrics · Versions · Live Logs · Config |
| lambda-envvar-drawer | C-05 Environment Variables → function row | 560px | Current Vars · Pending Changes · Deploy History |
| scheduled-job-drawer | C-05 Scheduled Jobs → task row | 560px | Schedule · Last 30 Runs · Execution Log · Config |
| migration-detail-drawer | DB Migrations row | 560px | SQL Preview · Affected Schemas · History |
| secret-detail-drawer | Secret Manager row | 560px | Current (masked) · History · Rotation Schedule |
| oauth-app-drawer | C-14 OAuth App Registry → app row | 560px | App Details · Scopes · Redirect URIs · Usage · Revoke |
| mobile-keys-drawer | C-14 Mobile Keys → key row | 480px | Rotation Schedule · Expiry Dates (read-only) |
| incident-detail-drawer | Incident Manager row | 720px | Timeline · Runbook · Communications · Postmortem |
| alert-rule-drawer | C-18 Alert Rules → rule row | 560px | Rule Config · Routing · Snooze Policy · Trigger History |
| pipeline-run-drawer | CI/CD row | 720px | Stages · Logs · Artifacts · Approvals |
| ai-job-drawer | AI Pipeline row | 640px | Job Config · Sample Questions · Errors · Cost |
| ai-config-drawer | C-15 Pipeline Config → threshold row | 480px | Current Value · History · Test Threshold |
| db-query-drawer | Database slow query row | 640px | Explain Plan · Index Suggestions · Historical Trend |
| db-param-drawer | C-11 DB Configuration → parameter row | 480px | Current Value · Pending Value · Restart Required · History |
| vapt-engagement-drawer | C-13 VAPT Schedule → engagement row | 640px | Scope · Findings · Status Timeline · Vendor Comms |
| celery-queue-drawer | C-08 Celery Queues → queue row | 560px | Workers · Queue Depth Trend · DLQ Items · Task History |
| cdn-perf-drawer | C-06 Performance Monitor → page path row | 560px | Web Vitals Trend · Error Log · Device Breakdown |
| aws-cost-drawer | C-19 → service row | 560px | Daily Spend Chart · Top Cost Drivers · Forecast |
| dns-record-drawer | C-20 → DNS record row | 480px | Record Details · Edit · Propagation Status · History |
| cert-detail-drawer | C-20 → certificate row | 480px | Domain · Expiry · Validation · CloudFront Mapping |
| runbook-editor-drawer | C-18 Runbook Editor → runbook row | 720px | Edit Content · Version History · Associated Alert Rules |
| feature-flag-drawer | C-21 → flag row | 480px | Flag Config · Tenant Overrides · Rollout % · History |
| ecs-task-def-drawer | C-08 ECS section → service row | 640px | Current Definition · Edit Image Tag · CPU/Memory · Deployment History |
| security-audit-drawer | C-13 Security Audit Log → event row | 560px | Event Detail · Actor · Before/After Values · IP |
| embedding-model-drawer | C-15 Embedding Model → job row | 560px | Model Config · Job Progress · Cost · HNSW Rebuild Status |
| index-action-drawer | C-11 Index Health → index row | 480px | Index Stats · Create/Drop Confirmation · Build Progress |
| api-quota-drawer | C-16 API Rate Limits → provider row | 480px | Quota Details · Usage Trend · Alert Config |
| fcm-delivery-drawer | C-07 FCM Delivery → notification row | 560px | Delivery Stats · Device Breakdown · Failed Tokens |
| tenant-storage-drawer | C-01 → tenant row Storage tab | 480px | Schema Size Breakdown · Quota Editor · Alert Config |
| escalation-tree-drawer | C-02 Escalation Tree → person row | 480px | Contact Details · OOO Status · Last Test Timestamp |
| exam-day-activation-drawer | C-10 Exam Day Mode → activate button | 600px | Pre-flight Checklist · Cost Estimate · Activation History |
| migration-matrix-drawer | C-12 Migration Matrix → schema row | 560px | Pending Migrations · Apply Log · Error Detail |
| restore-verification-drawer | C-12 Restore Verification → history row | 640px | Snapshot Details · Verification Checks · Pass/Fail Report |
| prompt-version-drawer | C-15 Prompt Version Manager → version row | 720px | Prompt Body · Config · A/B Stats · Diff View |
| data-localization-drawer | C-13 Data Localization Audit → resource row | 560px | Resource Details · Region · Violation Log · Remediation |
| cert-in-report-drawer | C-13 CERT-In Report → submission row | 720px | Report Fields · Evidence Files · PDF Preview · Submission Status |
| rotation-compliance-drawer | C-14 Rotation Compliance → secret row | 480px | Rotation SLA · History · Overdue Reason · Trigger Rotation |
| jwt-compromise-drawer | C-14 JWT Compromise Response | 640px | Step Checklist · Action Log · Confirmation Input |
| vacuum-progress-drawer | C-11 table row VACUUM action | 480px | Table Info · Progress · Result Stats · Audit Log |

---

## Implementation Priority Order

```
P0 — Before any institution goes live
  C-01  Tenant Manager          (platform cannot run without tenant provisioning)
                                 + G29 amendment: Tenant Storage Quota (per-tenant quota column + quota editor + daily Celery alert)
  C-04  API Health Monitor      (exam submit < 200ms SLA — must track from day 1)
  C-08  Infrastructure Monitor  (74K exam day — real-time AWS with write controls)
                                 + G4 amendment: Celery Queues tab
                                 + G23 amendment: ECS Task Definition Editor drawer (image tag · CPU/memory · force-deploy)
  C-09  CI/CD Pipeline Manager  (every deploy goes through this)
  C-11  Database Admin          (2,051 schemas — DBA needs live monitoring)
                                 + G5 amendment: DB Configuration tab
                                 + G20 amendment: Manual VACUUM ANALYZE action (audit-safe)
                                 + G26 amendment: Index Create/Drop actions (CREATE INDEX CONCURRENTLY · DDL audit)
  C-13  Security Operations     (WAF · CERT-In 6h · DPDPA 72h — compliance from day 1)
                                 + G6 amendment: VAPT Schedule tab
                                 + G16 amendment: Data Localization Audit tab (DPDPA ap-south-1 check)
                                 + G17 amendment: CERT-In Report tab (6h statutory report generator)
                                 + G24 amendment: Security Audit Log tab (append-only WAF/secret/2FA/escalation events)
  C-14  Secret & Key Manager    (JWT rotation · KMS — security foundation)
                                 + G7 amendment: OAuth App Registry tab
                                 + G8 amendment: Mobile Keys tab
                                 + G18 amendment: Rotation Compliance tab (47 secrets · SLA tracking)
                                 + G19 amendment: JWT Compromise Response section (guided 6-step)
  C-18  Incident Manager        (P0 incidents need runbooks before first exam)
                                 + G10 amendment: Alert Rules tab
                                 + G21 amendment: Runbook Editor tab (create/edit/version runbooks linked to alert rules)

P1 — Sprint 2
  C-02  Staff Account Manager   (all 81 roles need accounts before platform opens)
                                 + G30 amendment: Escalation Tree tab (P0/Security/DataBreach/DB chains with OOO toggle)
  C-03  System Configuration    (maintenance mode · rate limits · session config)
  C-05  Service Deployment Mgr  (Lambda version control and rollback)
                                 + G1 amendment: Environment Variables tab
                                 + G2 amendment: Scheduled Jobs tab (Celery beat)
  C-10  Auto-scaling Planner    (pre-warm for exam peaks — needed before first 74K event)
                                 + G11 amendment: Exam Day Mode tab (one-click 74K readiness)
  C-12  Backup & Migration Mgr  (snapshot + PITR before data grows large)
                                 + G12 amendment: Migration Matrix tab (2,051 schema grid)
                                 + G13 amendment: Restore Verification tab (backup integrity)
  C-17  Log Viewer              (debugging needs logs from day 1)
  C-19  AWS Infrastructure Cost Monitor  (track ₹70K–90K/month infra spend)
  C-20  DNS & Certificate Manager        (2,050+ custom domain SSL expiry management)
  C-21  Feature Flag Manager    (enable/disable flags per environment without code deploy)
                                 + G22: new page — boolean/rollout/variant flags · per-tenant overrides · 2FA-gated prod changes

P2 — Sprint 3
  C-06  CDN & Asset Manager     (when static assets are significant in scale)
                                 + G3 amendment: Performance Monitor tab (Core Web Vitals)
  C-07  Mobile Build Pipeline   (when Flutter app goes to stores)
                                 + G28 amendment: FCM Delivery Monitor tab (delivery rate · device split · token health)
  C-15  AI Pipeline Dashboard   (when MCQ AI generation is active)
                                 + G9 amendment: Pipeline Config tab (rejection thresholds)
                                 + G14 amendment: Prompt Version Manager tab (create/deploy/rollback)
                                 + G25 amendment: Embedding Model Manager section (re-embed 2M+ · HNSW rebuild)
  C-16  AI Cost Monitor         (when AI spend reaches ₹8L+/month)
                                 + G15 amendment: Cost Forecast section (month-end projection + simulator)
                                 + G27 amendment: API Rate Limits section (RPM/TPM per provider · auto-pause at 95%)
```

---

## Key Architectural Decisions

| Decision | Approach | Why |
|---|---|---|
| 2,051 separate PostgreSQL schemas | Schema-level multi-tenancy | Row-level tenancy risks cross-tenant leaks from ORM bugs; schema isolation = impossible cross-tenant access |
| Lambda for all API | Serverless | Auto-scales 0 → 74K concurrent without pre-provisioning; at 74K simultaneous exam submits, fixed servers require massive over-provisioning |
| Provisioned concurrency on exam endpoints | Warm Lambdas always ready | Cold starts at 74K = 3–5s delay for first request; provisioned concurrency guarantees < 200ms response |
| Multi-AZ RDS + 2 read replicas | High availability | Primary failure during exam → 74K students lose connection; Multi-AZ auto-failover < 60s |
| Shared RDS, separate schemas | Cost vs isolation balance | 2,050 separate RDS instances = ₹3 Cr/month; shared RDS with schema isolation = ₹80K/month |
| Memcached (django.core.cache) | Application-level cache | ORM-first approach; Memcached added only where ORM query latency is unacceptable at scale |
| PgBouncer transaction-mode pooling | Connection management | 2,050 tenants × 10 Django workers = 20,500 potential connections; PostgreSQL max_connections ≈ 500 |
| Celery for async tenant provisioning | Non-blocking | Provisioning 15,000 students takes 15–25 min; Celery offloads to workers, HTTP responds immediately |
| Prompt versioning for AI | Git-tracked, A/B testable | Prompt changes directly affect question quality; bad prompts increase hallucination; rollback must be instant |

---

## Compliance Obligations for Division C

| Regulation | Obligation | Deadline | Owner | Page |
|---|---|---|---|---|
| CERT-In 2022 Directions | Report cybersecurity incidents | **6 hours** from discovery | Security Engineer (16) | C-13 |
| DPDPA 2023 §31 | Notify Data Protection Board of breach | **72 hours** | Security (16) + DPO (Div N) | C-13 |
| DPDPA — data localisation | Indian student PII stored in India only | Always | DevOps (14) | C-08 |
| IT Act 2000 §43A | Reasonable security for sensitive personal data | Always | Security (16) | C-13, C-14 |
| RBI tokenisation | No raw card data — Razorpay tokens only | Always | Security (16) | C-14 |

---

## Functional Coverage Matrix — All 8 Roles

| # | Job to Be Done | Role | Pages Covering It |
|---|---|---|---|
| 1 | Create, suspend, delete institution tenants | Platform Admin | C-01 |
| 2 | Provision and manage all 81 staff accounts | Platform Admin | C-02 |
| 3 | Configure global platform settings + kill switches | Platform Admin | C-03 |
| 4 | Monitor Lambda SLA: exam submit < 200ms | Backend + DevOps | C-04 |
| 5 | Deploy Lambda versions, canary routing, rollback | Backend + DevOps | C-05 |
| 6 | Manage Lambda environment variables | Backend | C-05 (G1) |
| 7 | View and control Celery beat scheduled jobs | Backend | C-05 (G2) |
| 8 | Invalidate CDN cache, manage static assets | Frontend | C-06 |
| 9 | Monitor Core Web Vitals and JS error rate | Frontend | C-06 (G3) |
| 10 | Build Flutter iOS/Android, manage code signing | Mobile | C-07 |
| 11 | Submit to App Store / Google Play | Mobile | C-07 |
| 12 | View Hive AES-256 key rotation schedule | Mobile | C-14 (G8) |
| 13 | Monitor all AWS infrastructure in real-time with write controls | DevOps | C-08 |
| 14 | Monitor Celery queue depth and worker health | DevOps | C-08 (G4) |
| 15 | Manage CI/CD pipeline across 12 repos | DevOps | C-09 |
| 16 | Configure auto-scaling and pre-warm for exam peaks | DevOps | C-10 |
| 17 | Track AWS infrastructure spend per service | DevOps | C-19 |
| 18 | Manage DNS records and SSL certificate inventory | DevOps | C-20 |
| 19 | Configure metric alert thresholds → PagerDuty routing | DevOps | C-18 (G10) |
| 20 | Monitor 2,051 schema health, slow queries, locks | DBA | C-11 |
| 21 | Change RDS parameter groups and PgBouncer config | DBA | C-11 (G5) |
| 22 | Manage backups, PITR, Django migrations, archival | DBA | C-12 |
| 23 | Manage WAF rules, CERT-In incidents, DPDPA breach | Security | C-13 |
| 24 | Schedule and track VAPT engagements | Security | C-13 (G6) |
| 25 | Rotate JWT keys, KMS CMKs, API credentials | Security | C-14 |
| 26 | Manage OAuth app registry (scopes, redirect URIs) | Security | C-14 (G7) |
| 27 | Manage MCQ AI generation pipeline and prompt versions | AI/ML | C-15 |
| 28 | Configure auto-rejection thresholds | AI/ML | C-15 (G9) |
| 29 | Monitor AI API token spend and budget | AI/ML | C-16 |
| 30 | Search and trace logs across all services | All roles | C-17 |
| 31 | Manage P0–P2 incidents with runbooks | Admin + DevOps + Security | C-18 |
| 32 | Activate exam day mode (pre-warm Lambda, scale ECS, lock prod deploys) | DevOps | C-10 (G11) |
| 33 | View all 2,051 schemas' Django migration status in one aggregated grid | DBA | C-12 (G12) |
| 34 | Verify backup integrity via test restore to ephemeral RDS instance | DBA | C-12 (G13) |
| 35 | Create, edit, and promote AI prompt versions with A/B gates | AI/ML | C-15 (G14) |
| 36 | Forecast month-end LLM cost and simulate additional batch spend | AI/ML | C-16 (G15) |
| 37 | Audit student PII data localization (verify all resources in ap-south-1) | Security + DevOps | C-13 (G16) |
| 38 | Generate structured CERT-In 6-hour incident reports and DPO notifications | Security | C-13 (G17) |
| 39 | View secrets rotation compliance % and bulk-trigger overdue rotations | Security | C-14 (G18) |
| 40 | Execute JWT signing key compromise response workflow (6-step guided) | Security | C-14 (G19) |
| 41 | Trigger manual VACUUM ANALYZE on tables or schemas from the portal | DBA | C-11 (G20) |
| 42 | Create, edit, version, and publish operational runbooks linked to alert rules | Admin + DevOps + Security | C-18 (G21) |
| 43 | Enable/disable feature flags per environment without code deploy | Admin + Backend + DevOps | C-21 (G22) |
| 44 | Edit ECS task definition (Docker image tag · CPU · memory) and force-deploy from portal | DevOps | C-08 (G23) |
| 45 | View security-specific append-only audit trail (WAF changes · secret views · 2FA bypass · escalation) | Security | C-13 (G24) |
| 46 | Manage embedding model version and trigger re-embedding of 2M+ questions | AI/ML | C-15 (G25) |
| 47 | Create and drop database indexes from portal using CREATE INDEX CONCURRENTLY (no table lock) | DBA | C-11 (G26) |
| 48 | Monitor third-party LLM API quotas (RPM/TPM per provider) with auto-pause at 95% | AI/ML | C-16 (G27) |
| 49 | Monitor FCM push notification delivery rates, token health, and topic subscriber counts | Mobile | C-07 (G28) |
| 50 | Monitor and enforce per-tenant schema storage quotas with daily threshold alerts | Platform Admin | C-01 (G29) |
| 51 | View and test staff on-call escalation trees for P0, Security Breach, Data Breach, and DB Emergency incidents | Platform Admin | C-02 (G30) |

---

## Known Functional Gaps — Amendment Required

| Gap ID | Gap Description | Severity | Resolution |
|---|---|---|---|
| G1 | **Lambda Env Vars missing** — Backend Engineer cannot view or edit Lambda environment variables (DB connection strings, API key refs, feature toggles). C-05 covers version/routing only | High | Add "Environment Variables" tab to C-05 |
| G2 | **Celery Beat Schedule missing** — No page shows scheduled background jobs (nightly aggregations, health checks, archival). Nobody can pause, trigger, or audit beat tasks | High | Add "Scheduled Jobs" tab to C-05 |
| G3 | **Frontend Performance Monitor missing** — Frontend Engineer has no view of Core Web Vitals (LCP/FID/CLS), JS error rate, or real-user latency percentiles | Medium | Add "Performance Monitor" tab to C-06 |
| G4 | **Celery Queue Health missing** — DevOps has no visibility into worker count per queue, queue depth, failed task rate, dead-letter queue items, or worker restart | High | Add "Celery Queues" tab to C-08 |
| G5 | **DB Configuration missing** — DBA can monitor but cannot change RDS parameter groups (work_mem, max_connections, autovacuum settings) or PgBouncer pool sizes | High | Add "DB Configuration" tab to C-11 |
| G6 | **VAPT Scheduling missing** — C-13 shows VAPT results but Security Engineer cannot schedule engagements, track scope, or log vendor communications | Medium | Add "VAPT Schedule" tab to C-13 |
| G7 | **OAuth App Registry missing** — C-14 stores OAuth client secrets but has no registry of OAuth apps (scopes, redirect URIs, owner, last used, revoke) | Medium | Add "OAuth App Registry" tab to C-14 |
| G8 | **Mobile Engineer locked out of key schedule** — Access matrix gives Mobile Engineer zero access to C-14 but they own Hive AES-256 and FCM keys. Must see rotation dates to plan releases | Medium | Add "Mobile Keys" read-only tab to C-14 + grant Mobile Eng access to that tab only |
| G9 | **AI rejection thresholds read-only** — C-15 shows the rejection funnel but AI/ML Engineer cannot configure hallucination score cutoff, duplicate similarity %, or formatting rules | Medium | Add "Pipeline Config" tab to C-15 |
| G10 | **Alert rules config missing** — C-18 has on-call schedule and PagerDuty integration but nobody can configure metric alert thresholds (e.g. Lambda error rate > 5% → P1) | High | Add "Alert Rules" tab to C-18 |
| G11 | **Exam Day Mode controls missing** — DevOps cannot manually activate "exam day mode": simultaneously pre-warm all Lambda provisioned concurrency, scale ECS to max, lock production deploys, and confirm team readiness before a 74K-peak exam event | High | Add "Exam Day Mode" tab to C-10 |
| G12 | **Mass migration status dashboard missing** — DBA can execute migrations schema-by-schema but has no aggregated view of which of the 2,051 schemas are behind, how many pending migrations exist per app, or a bulk "apply to all" action | High | Add "Migration Matrix" tab to C-12 |
| G13 | **Backup restore verification missing** — No workflow to test-restore a snapshot to an isolated ephemeral RDS instance to verify data integrity. Backups are taken but never verified, creating undetected silent corruption risk | High | Add "Restore Verification" tab to C-12 |
| G14 | **Prompt version management UI missing** — C-15 shows A/B comparison results but AI/ML Engineer cannot create, edit, label, or deploy new prompt versions from the portal. All prompt changes are untracked and cannot be rolled back | High | Add "Prompt Version Manager" tab to C-15 |
| G15 | **LLM cost forecasting missing** — C-16 shows historical spend but has no month-end forecast, no "cost if we run N more batches" simulator, and no burn-rate visibility. AI/ML Engineer cannot predict whether ₹15L monthly cap will be breached before end of month | Medium | Add "Cost Forecast" section to C-16 |
| G16 | **Data localization compliance audit missing** — No dashboard verifying that all student PII (S3 buckets, RDS, Lambda environments) remains in ap-south-1. DPDPA 2023 violation goes undetected until an audit or breach | Critical | Add "Data Localization Audit" tab to C-13 |
| G17 | **CERT-In report generator missing** — Security Engineer must file CERT-In 6-hour incident reports but has no structured template or generator. Reports are drafted manually under time pressure, risking non-compliance with the statutory 6-hour deadline | Critical | Add "CERT-In Report" tab to C-13 |
| G18 | **Secrets rotation compliance dashboard missing** — C-14 shows per-secret rotation history but has no aggregate view: which secrets are overdue, overall compliance %, secrets that have never been rotated. No bulk rotation trigger for overdue items | High | Add "Rotation Compliance" tab to C-14 |
| G19 | **JWT compromise response workflow missing** — No guided workflow for responding to JWT signing key compromise. Security Engineer must manually execute 6 steps (revoke, bulk-invalidate sessions, force re-login, CERT-In log, DPO email, verify rollout) with no coordination or audit trail | Critical | Add "JWT Compromise Response" section to C-14 |
| G20 | **Manual VACUUM ANALYZE missing** — DBA can see autovacuum status per table but cannot trigger a manual VACUUM ANALYZE from the portal. Must SSH directly into RDS, creating an audit gap and access control risk | Medium | Add "Manual VACUUM" context-menu action to C-11 |
| G21 | **Runbook Editor missing** — C-18 displays a runbook library but there is no editor to create, update, or version runbooks from the portal. Runbook updates require direct file/DB access outside the platform, creating an audit gap | High | Add "Runbook Editor" tab to C-18 |
| G22 | **Feature Flag Manager missing** — No page exists to toggle feature flags per environment without a code deploy. Backend and DevOps engineers must push code to toggle any flag, slowing safe rollout and making emergency disables require a deploy | Critical | Create new page C-21: Feature Flag Manager |
| G23 | **ECS Task Definition Editor missing** — DevOps cannot update a container's Docker image tag, CPU, or memory from the portal. Every container update requires a full CI/CD pipeline run even when only the image tag changes | High | Add ECS Task Definition Editor drawer to C-08 ECS section |
| G24 | **Security Audit Log missing** — General CloudWatch logs are available in C-17 but there is no dedicated, append-only security audit trail covering WAF rule changes, secret view events, 2FA bypass events, OAuth app registrations, and permission escalations. External auditors have no single source of truth | High | Add "Security Audit Log" tab to C-13 |
| G25 | **Embedding Model Manager missing** — AI/ML Engineer cannot view embedding coverage, trigger re-embedding of the 2M+ question bank when switching models, or monitor HNSW index rebuild status. Questions without embeddings are invisible to the duplicate cosine similarity check | High | Add "Embedding Model Manager" section to C-15 |
| G26 | **Index Create/Drop from portal missing** — DBA cannot create or drop indexes from the portal. Must access RDS directly, bypassing audit controls. CREATE INDEX CONCURRENTLY (no table lock) is the safe method but is not surfaced anywhere in the UI | Medium | Add Index Create/Drop context-menu actions to C-11 index health table |
| G27 | **Third-party API Quota Monitor missing** — AI/ML Engineer cannot see current RPM/TPM consumption versus quota for Anthropic, OpenAI, or Google providers. Quota exhaustion silently stops the MCQ generation pipeline until discovered manually | Medium | Add "API Rate Limits" section to C-16 |
| G28 | **FCM Delivery Monitor missing** — Mobile Engineer cannot see push notification delivery rates, iOS vs Android split, device token health (expired/unregistered = uninstalled apps), or active FCM topic subscriber counts. Delivery failures go undetected | Medium | Add "FCM Delivery Monitor" tab to C-07 |
| G29 | **Tenant Schema Storage Quota missing** — Platform Admin has no visibility into per-tenant schema storage size or quota thresholds. No alerts exist when a tenant approaches storage limits; the first signal is a hard disk-full error affecting all tenants sharing the RDS instance | High | Add storage quota column + quota editor + daily Celery alert to C-01 |
| G30 | **Staff Escalation Tree missing** — On-call escalation chains for P0 Exam Day, Security Breach, Data Breach-DPDPA, and DB Emergency incidents exist only in a shared document outside the platform. "Out of Office" status is never reflected, leading to calls to unavailable engineers during incidents | High | Add "Escalation Tree" tab to C-02 |

---

*Last updated: 2026-03-20*
*Total pages: 23 (C-01 to C-18 original · C-19 AWS Costs · C-20 DNS & Certs · C-21 Feature Flags · C-22 Disaster Recovery & BCP · C-23 Rate Limiting & Abuse Prevention)*

### New Pages Added (March 2027 Review)

| # | Page | Priority | Purpose |
|---|---|---|---|
| C-22 | Disaster Recovery & Business Continuity | P0 | RTO/RPO monitoring, backup verification, DR drill records, runbook library, BCP status — CERT-In and ISO 27001 evidence |
| C-23 | API Rate Limiting & Abuse Prevention | P0 | Per-tenant/endpoint/IP rate limiting, abuse detection, exam-day burst scheduling, throttle event logging — prevents noisy-neighbour DoS in multi-tenant platform |
*Total tabs/sections/actions/new-pages added via amendments: 30 (G1–G30)*
*Roles covered: 8 (Roles 10–17)*
*Functional coverage: 51 jobs mapped across all 8 roles*
*All 30 functional gaps documented — descriptions updated in page table above*
*Compliance gaps resolved: G16 (DPDPA data localisation) · G17 (CERT-In 6h report) · G19 (JWT compromise workflow) · G24 (Security Audit Log)*
*Status: Pages list complete with all amendments — individual page spec files pending*
