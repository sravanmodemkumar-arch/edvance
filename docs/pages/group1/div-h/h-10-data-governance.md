# H-10 — Data Governance & Quality Console

> **Route:** `/analytics/data-governance/`
> **Division:** H — Data & Analytics
> **Primary Role:** Data Analyst (Role 39, Level 5) · CTO (Role 3, Level 4)
> **Read Access:** DBA (Role 15) · Security Engineer (Role 16) · Platform Admin (Role 10)
> **File:** `h-10-data-governance.md`
> **Priority:** P1 — 2M+ questions, 2,050 tenant schemas, 7.6M student records demand governed data
> **Status:** ✅ New page — prevents data drift, PII leakage, and analytics corruption

---

## 1. Purpose

At EduForge's scale (2,050 tenants × ~3,000 students avg = 7.6M student records, 2M+ questions, 800+ test series, ₹60Cr+ ARR in financial transactions), data quality issues compound into business failures. A duplicate student record inflates placement statistics. An incorrectly tagged question appears in the wrong exam domain. A PII field (Aadhaar) exposed in an analytics export triggers a DPDPA breach notification.

This page provides: (1) schema governance — tracking every table, column, owner, PII classification, and retention policy across shared + tenant schemas, (2) data quality rules — automated checks that flag anomalies (NULL rates, duplicate detection, referential integrity), (3) PII inventory — every column containing personal data, its purpose justification, and access audit trail, (4) data lineage — where data flows from (source) through (transformations) to (consumption), and (5) data freshness monitoring — alerting when materialized views or aggregation tables are stale.

---

## 2. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Data Governance & Quality Console                                  │
├─────────────────────────────────────────────────────────────────────┤
│  DATA HEALTH KPI (5 tiles)                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ 94.2%    │ │ 12       │ │ 847      │ │ 0        │ │ 2,050    │ │
│  │ Quality  │ │ Active   │ │ PII      │ │ PII      │ │ Schema   │ │
│  │ Score    │ │ DQ Alerts│ │ Columns  │ │ Breaches │ │ Health   │ │
│  │ ✅ >90%  │ │ ⚠️ 12    │ │ Tracked  │ │ ✅ 0     │ │ ✅ 100%  │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│  [Schema Catalog] [Data Quality] [PII Registry] [Lineage] [Freshness]│
├─────────────────────────────────────────────────────────────────────┤
│  SCHEMA CATALOG                                                     │
│                                                                     │
│  Schema: [shared ▼]  Table: [__________]  PII: [All ▼]             │
│                                                                     │
│  Table                │ Columns │ PII Cols │ Owner     │ Retention  │
│  ─────────────────────────────────────────────────────────────────  │
│  shared.institution   │ 28      │ 4        │ Platform  │ Permanent  │
│  shared.platform_user │ 22      │ 8        │ Platform  │ DPDPA 3yr  │
│  tenant.student       │ 34      │ 12       │ Tenant    │ DPDPA 3yr  │
│  tenant.exam_response │ 18      │ 2        │ Tenant    │ 7 years    │
│  tenant.fee_payment   │ 24      │ 6        │ Tenant    │ 8yr (IT Act)│
│                                                                     │
│  [Click table → Column detail with PII classification]              │
├─────────────────────────────────────────────────────────────────────┤
│  DATA QUALITY RULES — Active Alerts                                 │
│                                                                     │
│  Rule                          │ Table              │ Status │ Alert│
│  ─────────────────────────────────────────────────────────────────  │
│  Duplicate student email       │ tenant.student     │ ⚠️ 342 │ P2  │
│  NULL phone in parent table    │ tenant.parent      │ ⚠️ 1.2%│ P3  │
│  Orphan exam_response (no exam)│ tenant.exam_response│ ✅ 0  │ —   │
│  Fee amount = 0 (suspicious)   │ tenant.fee_payment │ ⚠️ 18  │ P2  │
│  Question without topic tag    │ shared.question    │ ⚠️ 4.1%│ P2  │
│  Stale materialized view       │ shared.analytics_* │ ⚠️ 2hr │ P1  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Models

```python
class DataCatalogTable(models.Model):
    """Registry of every table in the platform — shared + tenant template."""
    schema_type = models.CharField(choices=[('SHARED','Shared'),('TENANT','Tenant Template')])
    table_name = models.CharField(max_length=100)
    description = models.TextField()
    owner_team = models.CharField(max_length=50)  # "platform", "content", "exam", "finance"
    row_count_estimate = models.BigIntegerField(null=True)  # updated daily
    pii_column_count = models.IntegerField(default=0)
    retention_policy = models.CharField(max_length=100)  # "DPDPA 3yr", "IT Act 8yr", "Permanent"
    last_schema_change = models.DateTimeField(null=True)

class DataCatalogColumn(models.Model):
    """Column-level metadata including PII classification."""
    table = models.ForeignKey(DataCatalogTable, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=50)
    nullable = models.BooleanField()
    pii_classification = models.CharField(choices=[
        ('NONE', 'Not PII'), ('DIRECT', 'Direct PII — Aadhaar, phone, email'),
        ('INDIRECT', 'Indirect PII — DOB, address, caste'),
        ('SENSITIVE', 'Sensitive — health, disability, religion'),
        ('FINANCIAL', 'Financial — bank, salary, fee')
    ], default='NONE')
    purpose_justification = models.TextField(null=True)  # DPDPA: why this data is collected
    access_roles = models.JSONField(default=list)  # roles that can query this column
    masking_rule = models.CharField(null=True, max_length=50)  # "LAST_4", "HASH", "REDACT"

class DataQualityRule(models.Model):
    """Automated data quality checks."""
    name = models.CharField(max_length=200)
    table = models.ForeignKey(DataCatalogTable, on_delete=models.CASCADE)
    rule_type = models.CharField(choices=[
        ('NULL_RATE', 'NULL Rate Check'), ('DUPLICATE', 'Duplicate Detection'),
        ('REFERENTIAL', 'Referential Integrity'), ('RANGE', 'Value Range Check'),
        ('FRESHNESS', 'Data Freshness'), ('CUSTOM_SQL', 'Custom SQL Check')
    ])
    sql_expression = models.TextField()  # The actual check SQL
    threshold = models.FloatField()  # e.g., 0.01 = 1% NULL rate is acceptable
    severity = models.CharField(choices=[('P1','P1'),('P2','P2'),('P3','P3')])
    last_run_at = models.DateTimeField(null=True)
    last_result = models.JSONField(null=True)  # {"passed": false, "value": 0.042, "details": "..."}
    alert_channel = models.CharField(max_length=50)  # "slack_#data-alerts", "email_cto"
    enabled = models.BooleanField(default=True)

class PIIAccessLog(models.Model):
    """Immutable audit log for every PII column access — DPDPA 2023 evidence."""
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    table_name = models.CharField(max_length=100)
    column_name = models.CharField(max_length=100)
    access_type = models.CharField(choices=[('SELECT','Read'),('EXPORT','Export'),('ADMIN','Admin Console')])
    purpose = models.CharField(max_length=200)
    row_count_accessed = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
```

---

## 4. Celery Tasks

| Task ID | Task | Schedule | Description |
|---|---|---|---|
| H-DG-1 | `run_data_quality_checks` | Hourly | Execute all enabled DQ rules; update results; fire alerts |
| H-DG-2 | `update_table_statistics` | Daily 1 AM | Row counts, PII column counts, schema change detection |
| H-DG-3 | `freshness_monitor` | Every 15 min | Check materialized views refresh timestamps; alert if stale |
| H-DG-4 | `pii_column_scan` | Weekly | Scan all columns for potential unclassified PII (regex: Aadhaar, email, phone patterns) |
| H-DG-5 | `retention_enforcement` | Daily 2 AM | Delete data past retention policy (DPDPA 3yr, IT Act 8yr) with audit log |

---

## 5. Business Rules

- **PII classification is mandatory for every column in the catalog.** A column classified as `NONE` that actually contains phone numbers is a DPDPA violation waiting to happen. The weekly PII scan (H-DG-4) uses regex patterns to detect unclassified PII columns and creates P1 alerts. New columns added by migrations must be classified in the same PR (enforced by CI check).
- **Data quality score (94.2%) is computed as: (rules passed / total rules enabled) × 100.** Individual rule failures don't cause the same damage — a 4.1% untagged question rate is annoying; a stale materialized view during exam results processing is catastrophic. The severity-weighted score gives P1 failures 10× weight of P3 failures.
- **Retention enforcement must be auditable.** When H-DG-5 deletes student records older than 3 years (DPDPA), it logs: what was deleted, how many rows, under which retention policy, and timestamp. This log is the DPDPA compliance evidence showing the institution practices data minimisation. The deletion log itself is retained for 7 years (longer than the deleted data — for legal protection).
- **Cross-tenant data leakage is the most severe data governance failure possible.** If a query accidentally returns Student A (from Institution X) in Institution Y's results, this is a privacy breach + potential DPDPA penalty + trust destruction. Every analytics query must include `WHERE tenant_id = {current_tenant}` — the governance console monitors query patterns for missing tenant filters.
- **Export operations on PII columns require purpose justification.** A data analyst exporting 50,000 student phone numbers "for analysis" without stating the specific purpose violates DPDPA's purpose limitation principle. The PIIAccessLog captures the stated purpose; the DPDPA compliance officer (N-03) reviews these logs monthly.

---

*Last updated: 2026-03-30 · Group 1 — Platform Admin · Division H*
