# C-22 — Disaster Recovery & Business Continuity

> **Route:** `/engineering/disaster-recovery/`
> **Division:** C — Engineering
> **Primary Role:** DevOps/SRE Engineer (Role 14, Level 5) · Platform Admin (Role 10, Level 4)
> **Read Access:** CTO (Role 3) · Backend Engineer (Role 11) · DBA (Role 15) · Security Engineer (Role 16)
> **File:** `c-22-disaster-recovery.md`
> **Priority:** P0 — Platform survivability for 2,050 tenants and 7.6M students
> **Status:** ✅ New page — critical gap identified

---

## 1. Purpose

Single pane of glass for EduForge's disaster recovery posture across all infrastructure layers. At 2,050 institutions serving up to 7.6M students with 74K peak concurrent exam submissions, any unplanned downtime during an exam window is a **P0 incident with legal and contractual consequences** (SLA breach → penalty clauses in institutional contracts → potential litigation for invalidated exam results).

This page provides: (1) real-time RTO/RPO compliance status for every critical service, (2) automated failover health checks (readiness ≠ tested — both tracked), (3) DR drill scheduling and execution history, (4) backup verification dashboard (backup exists ≠ backup works), (5) runbook library for incident-specific recovery procedures, and (6) business continuity plan (BCP) status for non-IT functions (finance, support, content).

**Business goals:**
- Maintain RTO < 15 minutes for exam services (exam in progress cannot be lost)
- Maintain RPO < 5 minutes for transactional data (PostgreSQL WAL shipping)
- Ensure every backup is tested monthly (untested backups are not backups)
- Track DR drill completion (CERT-In and ISO 27001 evidence)
- Satisfy DPDPA 2023 data availability obligations

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Route | `/engineering/disaster-recovery/` |
| View | `DRDashboardView` |
| Template | `engineering/disaster_recovery.html` |
| Priority | P0 |
| Roles | `devops_sre`, `platform_admin`, `cto`, `backend_eng`, `dba`, `security_eng` |

---

## 3. HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| RTO/RPO KPI strip | `?part=kpi` | Page load | `#dr-kpi` |
| Service recovery matrix | `?part=matrix` | Page load | `#dr-matrix` |
| Backup verification | `?part=backups` | Tab: backups | `#dr-backups` |
| DR drill log | `?part=drills` | Tab: drills | `#dr-drills` |
| Runbook library | `?part=runbooks` | Tab: runbooks | `#dr-runbooks` |
| BCP status | `?part=bcp` | Tab: bcp | `#dr-bcp` |
| Failover test modal | `?part=failover_modal&service={id}` | [Test Failover] | `#modal-container` |

---

## 4. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Disaster Recovery & Business Continuity                            │
│  Last DR Drill: 14 Feb 2027 (41 days ago)   [Schedule Drill]       │
├─────────────────────────────────────────────────────────────────────┤
│  RTO/RPO KPI STRIP (6 tiles)                                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ 12m 22s  │ │ 3m 14s   │ │ 100%     │ │ 97.2%    │ │ 4/4      │ │
│  │ RTO      │ │ RPO      │ │ Backup   │ │ Backup   │ │ DR Drills│ │
│  │ Actual   │ │ Actual   │ │ Complete │ │ Verified │ │ FY26-27  │ │
│  │ ✅ <15m  │ │ ✅ <5m   │ │ ✅       │ │ ⚠️ 2fail │ │ ✅ 4/yr  │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│  [Recovery Matrix] [Backups ●] [DR Drills] [Runbooks] [BCP]        │
├─────────────────────────────────────────────────────────────────────┤
│  SERVICE RECOVERY MATRIX                                           │
│                                                                     │
│  Service            │ RTO Target │ RTO Actual │ RPO    │ Status     │
│  ─────────────────────────────────────────────────────────────────  │
│  Exam Engine        │ 15 min     │ 12m 22s    │ 0 (WAL)│ ✅ Ready  │
│  Auth (Django)      │ 10 min     │ 8m 40s     │ 2m     │ ✅ Ready  │
│  PostgreSQL (RDS)   │ 15 min     │ 14m 10s    │ 5m WAL │ ✅ Ready  │
│  Cloudflare R2      │ N/A (CDN)  │ <1m        │ 0      │ ✅ Active │
│  AWS Lambda (async) │ 5 min      │ 3m 20s     │ 0 (SQS)│ ✅ Ready  │
│  SQS Queues         │ 5 min      │ 2m 40s     │ 0      │ ✅ Ready  │
│  Email (SES)        │ 30 min     │ 22m        │ N/A    │ ✅ Ready  │
│  Payment (Razorpay) │ External   │ N/A        │ N/A    │ ⚠️ Vendor │
│  SMS (Twilio/MSG91) │ External   │ N/A        │ N/A    │ ⚠️ Vendor │
│                                                                     │
│  ⚠️ 2 services depend on external vendors — failover = alternate   │
│     provider (MSG91 → Twilio; Razorpay → manual bank transfer)     │
├─────────────────────────────────────────────────────────────────────┤
│  BACKUP VERIFICATION HISTORY                                       │
│                                                                     │
│  Backup Type     │ Last Backup  │ Last Verified │ Restore Test │   │
│  ──────────────────────────────────────────────────────────────────  │
│  RDS Snapshot    │ 27 Mar 10PM │ 26 Mar (24h)  │ ✅ 12m 22s   │   │
│  WAL Archive     │ Continuous  │ 27 Mar 8AM    │ ✅ 3m 14s    │   │
│  R2 Object Store │ Continuous  │ 25 Mar        │ ✅ <1m       │   │
│  Config/Secrets  │ Daily       │ 20 Mar        │ ⚠️ 7 days ago│   │
│  Code Repos      │ GitHub      │ N/A (managed) │ N/A          │   │
│  Tenant Schemas  │ Per-tenant  │ 22 Mar        │ ⚠️ 5 days ago│   │
│  (2,050 schemas) │ nightly     │ (sample: 50)  │ 48/50 passed │   │
│                                                                     │
│  VERIFICATION POLICY:                                               │
│  Daily: RDS snapshot restore to staging (automated Celery task)     │
│  Weekly: 50 random tenant schema restores (automated)               │
│  Monthly: Full platform restore to DR environment (manual drill)    │
│  Quarterly: Business Continuity drill (BCP — includes non-IT)      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Data Models

```python
class DRService(models.Model):
    """Each critical service tracked for DR readiness."""
    name = models.CharField(max_length=100)  # "Exam Engine", "PostgreSQL RDS"
    category = models.CharField(choices=[
        ('COMPUTE', 'Compute'), ('DATABASE', 'Database'), ('STORAGE', 'Storage'),
        ('MESSAGING', 'Messaging'), ('EXTERNAL', 'External Vendor')
    ])
    rto_target_seconds = models.IntegerField()  # 900 = 15 min
    rpo_target_seconds = models.IntegerField()  # 300 = 5 min
    rto_actual_seconds = models.IntegerField(null=True)  # from last drill
    rpo_actual_seconds = models.IntegerField(null=True)
    failover_type = models.CharField(choices=[
        ('AUTO', 'Automatic'), ('MANUAL', 'Manual Runbook'), ('VENDOR', 'Vendor-Dependent')
    ])
    failover_tested_at = models.DateTimeField(null=True)
    failover_status = models.CharField(choices=[
        ('READY', 'Ready'), ('DEGRADED', 'Degraded'), ('NOT_TESTED', 'Not Tested'),
        ('FAILED', 'Last Test Failed')
    ])
    runbook_url = models.URLField(null=True)
    owner_role = models.CharField(max_length=50)  # "devops_sre"

class DRBackupRecord(models.Model):
    """Every backup event and its verification."""
    service = models.ForeignKey(DRService, on_delete=models.CASCADE)
    backup_type = models.CharField(choices=[
        ('SNAPSHOT', 'RDS Snapshot'), ('WAL', 'WAL Archive'), ('OBJECT', 'Object Store'),
        ('CONFIG', 'Config/Secrets'), ('SCHEMA', 'Tenant Schema')
    ])
    backup_started_at = models.DateTimeField()
    backup_completed_at = models.DateTimeField(null=True)
    backup_size_bytes = models.BigIntegerField()
    backup_location = models.CharField(max_length=500)  # S3 ARN or path
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True)
    restore_test_duration_seconds = models.IntegerField(null=True)
    restore_test_result = models.CharField(choices=[
        ('PASS', 'Pass'), ('FAIL', 'Fail'), ('NOT_TESTED', 'Not Tested')
    ], default='NOT_TESTED')
    failure_reason = models.TextField(null=True)

class DRDrill(models.Model):
    """DR drill execution records — CERT-In and ISO 27001 evidence."""
    drill_type = models.CharField(choices=[
        ('AUTOMATED', 'Automated Restore Test'), ('TABLETOP', 'Tabletop Exercise'),
        ('PARTIAL', 'Partial Failover'), ('FULL', 'Full Platform DR'),
        ('BCP', 'Business Continuity Plan')
    ])
    scheduled_date = models.DateField()
    executed_at = models.DateTimeField(null=True)
    duration_minutes = models.IntegerField(null=True)
    participants = models.JSONField(default=list)  # [{"name": "...", "role": "..."}]
    scenario = models.TextField()  # "RDS primary failure during peak exam"
    findings = models.JSONField(default=list)  # [{"issue": "...", "severity": "HIGH", "action": "..."}]
    rto_achieved_seconds = models.IntegerField(null=True)
    rpo_achieved_seconds = models.IntegerField(null=True)
    result = models.CharField(choices=[
        ('PASS', 'Pass'), ('PARTIAL', 'Partial Pass'), ('FAIL', 'Fail'),
        ('CANCELLED', 'Cancelled')
    ])
    report_url = models.URLField(null=True)  # PDF report stored in R2
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)

class DRRunbook(models.Model):
    """Recovery runbooks for specific failure scenarios."""
    title = models.CharField(max_length=200)
    scenario = models.CharField(max_length=200)  # "RDS Primary Failure"
    severity = models.CharField(choices=[('P0','P0'),('P1','P1'),('P2','P2')])
    services_affected = models.ManyToManyField(DRService)
    steps = models.JSONField()  # [{"order": 1, "action": "...", "owner": "...", "estimated_minutes": 5}]
    last_reviewed = models.DateField()
    review_frequency_days = models.IntegerField(default=90)  # quarterly review
    version = models.IntegerField(default=1)
    tested_in_drill = models.ForeignKey(DRDrill, null=True, on_delete=models.SET_NULL)
```

---

## 6. Celery Tasks

| Task ID | Task | Schedule | Description |
|---|---|---|---|
| C-DR-1 | `verify_rds_snapshot` | Daily 2 AM | Restore latest RDS snapshot to staging; validate row counts; record result |
| C-DR-2 | `verify_tenant_schemas` | Daily 3 AM | Randomly select 50/2,050 tenant schemas; restore to staging; verify |
| C-DR-3 | `check_wal_lag` | Every 5 min | Alert if WAL replication lag >5 min (RPO breach risk) |
| C-DR-4 | `dr_readiness_score` | Every 15 min | Recompute overall DR readiness score; alert CTO if <90% |
| C-DR-5 | `runbook_review_alert` | Weekly | Flag runbooks not reviewed in >90 days; notify DevOps lead |
| C-DR-6 | `backup_retention_cleanup` | Daily 4 AM | Delete backups older than retention policy (RDS: 35 days, WAL: 7 days, Config: 90 days) |

---

## 7. Integration Points

| System | Integration | Direction |
|---|---|---|
| C-08 (Infrastructure) | Infrastructure health feeds into DR readiness | Inbound |
| C-11 (Database) | RDS health, replication lag, snapshot status | Inbound |
| C-18 (Incidents) | DR incidents link to incident manager | Bidirectional |
| C-14 (Secrets) | Secrets backup verification | Inbound |
| A-02 (Platform Health) | DR readiness score shown on exec dashboard | Outbound |
| F-02 (Live Exam Monitor) | Exam-in-progress flag prevents DR drill during peak | Inbound |
| CERT-In | DR drill reports as compliance evidence | Outbound |
| ISO 27001 Auditor | Annual DR evidence package | Outbound |

---

## 8. Business Rules

- **Exam-in-progress lockout:** Automated DR drills (C-DR-1, C-DR-2) must not run when live exams are in progress; the Celery tasks check `exam_schedule` for active exams and defer to the next safe window; a DR drill that disrupts a live exam serving 74K students is itself a P0 incident
- **Untested backups are not backups:** A backup that exists but has never been restored and verified provides false confidence; the 97.2% verification rate (with 2 failures) is more honest than 100% backup completion with 0% verification; the 2 failures (tenant schema restores) must be investigated — corrupt backups are worse than no backups because teams assume they're safe
- **Vendor failover planning:** Razorpay and MSG91 are external dependencies with no direct failover; the DR plan must include manual alternatives (bank NEFT for payments; alternate SMS provider pre-contracted); vendor SLAs must be reviewed quarterly and their actual uptime tracked against their promised SLA
- **DR drill frequency:** CERT-In recommends annual DR testing; ISO 27001 Annex A.17 requires it; EduForge's policy of quarterly drills exceeds the minimum; each drill must test a different scenario (not the same "RDS failure" every time) — the scenario list comes from the runbook library, rotated systematically
- **RPO for exam data:** During a live exam, RPO must effectively be 0 — no student responses can be lost; PostgreSQL WAL shipping with synchronous replication to a standby achieves this; if WAL lag exceeds 30 seconds during an active exam, a P0 alert must fire to the on-call DevOps engineer; the exam engine's write-ahead-of-commit pattern ensures responses are durable before acknowledging to the student's browser
- **BCP (non-IT):** Business continuity extends beyond infrastructure — if the finance team cannot process payroll, if customer support cannot access tickets, if the content team cannot author questions — these are business continuity failures even if servers are running; the BCP tab tracks readiness of each business function for a major disruption (e.g., office inaccessible, key person unavailable)

---

*Last updated: 2026-03-30 · Group 1 — Platform Admin · Division C*
