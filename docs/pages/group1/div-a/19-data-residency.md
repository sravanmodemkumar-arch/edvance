# div-a-19 — Data Residency

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total data (student records + exam data) | ~50–200 TB |
| Primary region | ap-south-1 (Mumbai, India) |
| DR region | ap-south-2 (Hyderabad, India) |
| CDN nodes (student-facing) | Indian PoPs only |
| Cross-border data transfers | None (DPDPA §16 compliance) |
| Database: RDS PostgreSQL | Multi-AZ in Mumbai |
| Object storage: S3 | Versioned, Mumbai region |
| Backup retention | 30 days incremental + annual snapshots |
| RPO (Recovery Point Objective) | < 1 hour |
| RTO (Recovery Time Objective) | < 4 hours |

**Why this matters:** DPDPA §16 requires that personal data of Indian citizens be stored only in India. A CDN misconfiguration that routes student data through Singapore violates the Act. This page gives the compliance officer a live map of where every byte lives.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Data Residency |
| Route | `/exec/data-residency/` |
| Django view | `DataResidencyView` |
| Template | `exec/data_residency.html` |
| Priority | P2 |
| Nav group | Compliance |
| Required role | `exec`, `superadmin`, `compliance` |
| 2FA required | Exporting data residency report |
| HTMX poll | Residency checks: every 10 min |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Data Residency                    [Export Report] [Run Checks Now]  │
├──────────┬──────────┬──────────┬──────────┬──────────────────────────────── ┤
│ Residency│ Storage  │ Backup   │ Cross-   │  Last Verified                  │
│ Status   │ (India)  │ (India)  │ Border   │                                 │
│ ✅ Compl │ ✅ 100%  │ ✅ 100%  │ ✅ None  │  15 min ago                     │
├──────────┴──────────┴──────────┴──────────┴──────────────────────────────── ┤
│ TABS: [Overview] [Data Inventory] [Transfer Log] [Checks] [Certificates]    │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: OVERVIEW                                                                │
│ ┌──────────────────────────────────────────────────────────────────────────┐ │
│ │ Data Flow Diagram (India-only)                                           │ │
│ │  [Institution] → [API GW Mumbai] → [App Server Mumbai] → [RDS Mumbai]   │ │
│ │               → [S3 Mumbai] → [Backup Mumbai/Hyderabad]                 │ │
│ └──────────────────────────────────────────────────────────────────────────┘ │
│ Infrastructure table: each component + region + status                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Residency Status | Compliant / Non-Compliant | Non-compliant = red |
| 2 | Storage (India) | % of total storage in India | < 100% = red |
| 3 | Backup (India) | % of backups in India | < 100% = red |
| 4 | Cross-Border Transfers | None / N detected | Any detected = red |
| 5 | Last Verified | Relative time of last automated check | > 1h = amber |

---

### 4.2 Tab: Overview

`id="tab-overview"` · `hx-get="?part=residency_overview"`

#### 4.2.1 Data Flow Diagram

SVG diagram showing complete data path.
**Nodes:** Institution (browser) → Cloudflare CDN (India PoP only) → API Gateway (Mumbai) → App Server (Mumbai) → PostgreSQL RDS (Mumbai, Multi-AZ) → S3 (Mumbai) → Backup (Mumbai primary + Hyderabad DR)

**Node styling:**
- India nodes: `fill: #064E3B border: #34D399` (green)
- Any non-India node: `fill: #450A0A border: #EF4444` (red) + alert badge
- Arrow labels: data type (PII / Exam data / Logs / Backups)

#### 4.2.2 Infrastructure Table

| Component | Type | Region | Zone | Status | Last Verified |
|---|---|---|---|---|---|
| PostgreSQL Primary | Database | ap-south-1 | ap-south-1a | ✅ India | 15 min ago |
| PostgreSQL Standby | Database | ap-south-1 | ap-south-1b | ✅ India | 15 min ago |
| S3 Student Data | Object Storage | ap-south-1 | — | ✅ India | 15 min ago |
| S3 Exam Media | Object Storage | ap-south-1 | — | ✅ India | 15 min ago |
| S3 Backups | Object Storage | ap-south-1 | — | ✅ India | 15 min ago |
| S3 DR Backups | Object Storage | ap-south-2 | — | ✅ India | 15 min ago |
| Cloudflare CDN | CDN | India PoPs | — | ✅ India | 15 min ago |
| Redis Cache | Cache | ap-south-1 | — | ✅ India | 15 min ago |
| Celery Workers | Compute | ap-south-1 | — | ✅ India | 15 min ago |

**Click row:** opens Infrastructure Detail Drawer (§5.1)

---

### 4.3 Tab: Data Inventory

`id="tab-inventory"` · `hx-get="?part=data_inventory"`

**Purpose:** Catalogue of all data categories, their classification, and storage location.

| Data Category | Classification | Volume (approx) | Storage | Location | Encryption |
|---|---|---|---|---|---|
| Student personal data | PII — Sensitive | ~500 GB | PostgreSQL | Mumbai | AES-256 at rest |
| Student exam answers | Confidential | ~20 TB | S3 | Mumbai | AES-256 |
| Exam question bank | Proprietary | ~5 TB | S3 | Mumbai | AES-256 |
| Proctoring videos | Sensitive PII | ~100 TB | S3 | Mumbai | AES-256 |
| Audit logs | Internal | ~2 TB | PostgreSQL | Mumbai | AES-256 |
| Invoice documents | Financial | ~50 GB | S3 | Mumbai | AES-256 |
| Application logs | Internal | ~5 TB | CloudWatch | Mumbai | AWS managed |

**[Edit Classification]** for each row (compliance officer only)

---

### 4.4 Tab: Transfer Log

`id="tab-transfers"` · `hx-get="?part=transfer_log"`

**Purpose:** Log of any data transfers (backups, exports, API calls that moved data). Proves no cross-border transfers occurred.

| Column | Detail |
|---|---|
| Timestamp | Datetime |
| Transfer type | Backup / Export / API / Replication |
| Source | Source system + region |
| Destination | Destination system + region |
| Data category | PII / Exam / Logs |
| Volume | MB / GB |
| Authorised by | User or "Automated" |
| Status | Completed / Failed / In Progress |

**Filter:** Transfer type · Region · Data category · Date range
**Pagination:** 25/page

**Any non-India destination row:** `bg-[#1A0A0A]` red tint + `⚠ Cross-border!` badge → auto-creates compliance finding

---

### 4.5 Tab: Checks

`id="tab-checks"` · `hx-get="?part=residency_checks"`

**15 automated data residency checks:**

| Check | Frequency | Last Run | Status |
|---|---|---|---|
| RDS region = ap-south-1 | Every 10 min | 15 min ago | ✅ Pass |
| S3 buckets region = ap-south-1/ap-south-2 | Every 10 min | 15 min ago | ✅ Pass |
| S3 replication rules: India-only | Every 1h | 40 min ago | ✅ Pass |
| CloudFront: India-only edge locations | Every 1h | 40 min ago | ✅ Pass |
| No cross-region replication detected | Every 10 min | 15 min ago | ✅ Pass |
| Encryption at rest enabled (all buckets) | Every 1h | 40 min ago | ✅ Pass |
| Backup copy in Hyderabad DR | Every 6h | 3h ago | ✅ Pass |
| ... (15 total) | | | |

**[Run All Checks Now]** button · progress inline

---

### 4.6 Tab: Certificates

`id="tab-certs"` · `hx-get="?part=certs"`

**SSL/TLS certificates and compliance certificates:**

| Certificate | Domain / Entity | Issued by | Valid From | Valid Until | Status |
|---|---|---|---|---|---|
| TLS — platform.com | platform.com | Let's Encrypt | Jan 2025 | Apr 2025 | ✅ Valid (42d) |
| TLS — api.platform.com | api.platform.com | Let's Encrypt | Jan 2025 | Apr 2025 | ✅ Valid (42d) |
| SOC 2 Type II | Platform Pvt Ltd | Deloitte | Jan 2024 | Dec 2024 | ⚠ Expired |
| ISO 27001 | Platform Pvt Ltd | BSI | Mar 2023 | Mar 2026 | ✅ Valid |

**TLS cert expiring < 30 days:** amber badge
**TLS cert expiring < 7 days:** red badge + auto-alert to ops

---

## 5. Drawers

### 5.1 Infrastructure Component Drawer (480 px)

**Header:** Component name · Region badge · Status badge · `[×]`

**Content:**
- AWS ARN / Resource ID
- Region + Availability Zone
- Encryption status (at-rest + in-transit)
- Data categories stored
- Backup policy
- Last health check
- Recent check history (5 rows)

**Footer:** [Run Check] [View in AWS Console →] [Close]

---

## 6. Modals

### 6.1 Export Data Residency Report Modal (480 px)

**2FA required.**
| Field | Type |
|---|---|
| Report type | DPDPA §16 / Full / Summary |
| Include checks history | Checkbox |
| Include transfer log (N days) | Number |
| Format | PDF / XLSX |

**Footer:** [Cancel] [Generate Report]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/residency_kpi.html` | Page load · poll 10 min |
| `?part=residency_overview` | `exec/partials/residency_overview.html` | Tab click |
| `?part=data_inventory` | `exec/partials/data_inventory.html` | Tab click |
| `?part=transfer_log` | `exec/partials/transfer_log.html` | Tab click · filter |
| `?part=residency_checks` | `exec/partials/residency_checks.html` | Tab click · manual run |
| `?part=certs` | `exec/partials/residency_certs.html` | Tab click |
| `?part=infra_drawer&id={id}` | `exec/partials/infra_drawer.html` | Row click |

**Django view dispatch:**
```python
class DataResidencyView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_compliance"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/residency_kpi.html",
                "residency_overview": "exec/partials/residency_overview.html",
                "data_inventory": "exec/partials/data_inventory.html",
                "transfer_log": "exec/partials/transfer_log.html",
                "residency_checks": "exec/partials/residency_checks.html",
                "certs": "exec/partials/residency_certs.html",
                "infra_drawer": "exec/partials/infra_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/data_residency.html", ctx)
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 300 ms | > 800 ms |
| Overview tab | < 500 ms | > 1.2 s |
| Checks tab | < 400 ms | > 1 s |
| Transfer log table | < 400 ms | > 1 s |
| Infrastructure drawer | < 250 ms | > 700 ms |
| Full page initial load | < 1 s | > 2.5 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Non-India storage detected | Residency Status card = red "Non-Compliant" · alert email sent · compliance finding auto-created |
| TLS cert expired | Certs tab shows critical badge; ops alert sent |
| Check fails (infrastructure unreachable) | Check status = Warning "Could not verify — AWS API timeout" |
| Transfer log: cross-border transfer found | Red row + auto-creates FIND-XXXX compliance finding |
| All checks passing | Green "All residency checks passed" status in overview |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`5` | Switch tabs |
| `R` | Run all checks |
| `E` | Export report |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/data_residency.html` | Full page shell |
| `exec/partials/residency_kpi.html` | KPI strip |
| `exec/partials/residency_overview.html` | Data flow diagram + infra table |
| `exec/partials/data_inventory.html` | Data catalogue table |
| `exec/partials/transfer_log.html` | Transfer log |
| `exec/partials/residency_checks.html` | Automated checks list |
| `exec/partials/residency_certs.html` | Certificates table |
| `exec/partials/infra_drawer.html` | Infrastructure component drawer |
| `exec/partials/export_residency_modal.html` | Export report modal |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `DataFlowDiagram` | §4.2.1 |
| `InfrastructureTable` | §4.2.2 |
| `DataInventoryTable` | §4.3 |
| `TransferLogTable` | §4.4 |
| `ResidencyChecksTable` | §4.5 |
| `CertificatesTable` | §4.6 |
| `DrawerPanel` | §5.1 |
| `ModalDialog` | §6.1 |
| `PaginationStrip` | Transfer log |
| `PollableContainer` | KPI + checks |
