# C-20 — DNS & Certificate Manager

> **Route:** `/engineering/dns-certs/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · DevOps/SRE (Role 14)
> **Read Access:** Security Engineer (Role 16)
> **File:** `c-20-dns-certs.md`
> **Priority:** P1
> **Status:** ✅ Spec done

---

## 1. Page Name & Route

**Page Name:** DNS & Certificate Manager
**Route:** `/engineering/dns-certs/`
**Part-load routes:**
- `/engineering/dns-certs/?part=kpi` — DNS and certificate health KPI strip
- `/engineering/dns-certs/?part=cert-inventory` — ACM certificate inventory table
- `/engineering/dns-certs/?part=expiry-calendar` — certificate expiry calendar
- `/engineering/dns-certs/?part=dns-records` — Route53 DNS record manager
- `/engineering/dns-certs/?part=propagation` — DNS propagation checker
- `/engineering/dns-certs/?part=cloudfront-map` — CloudFront distribution ↔ certificate mapping
- `/engineering/dns-certs/?part=drawer&cert_id={id}` — certificate detail drawer (cert-detail-drawer)
- `/engineering/dns-certs/?part=drawer&record_id={id}` — DNS record drawer (dns-record-drawer)

---

## 2. Purpose (Business Objective)

The DNS & Certificate Manager is the operational control centre for the platform's domain infrastructure — the invisible layer that connects 2,050 institution custom subdomains to the platform, routes traffic through CloudFront, and ensures every user connection is encrypted via a valid SSL/TLS certificate.

A single expired SSL certificate causes browser security warnings that immediately block all student access to that institution's portal. With 2,050+ certificates across custom domains (plus platform certificates for shared routes), manual tracking in spreadsheets is not viable. This page provides proactive expiry alerts 30, 14, and 7 days before any certificate expires, and enables DevOps to manage DNS records and request new certificates without AWS console access.

The DNS layer is equally critical: a wrong A record or missing CNAME takes a portal offline. This page provides a safe, audited interface for DNS changes with propagation verification built in.

**Business goals:**
- Zero expired SSL certificates — proactive renewal alerts and one-click renewal workflow
- Route53 DNS record management for platform domains and all 2,050 institution subdomains
- ACM certificate inventory with auto-renewal status verification
- CloudFront distribution ↔ certificate mapping to confirm every distribution has a valid attached cert
- DNS propagation checker for changes that need to be verified globally
- Certificate request workflow for new institutions and custom domain migrations

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full: create · edit · delete DNS records · request/renew certs · manage CloudFront mappings |
| DevOps / SRE (14) | Level 4 | Full: create · edit DNS records · request/renew certs · view all |
| Security Engineer (16) | Level 4 — Read | View certificate inventory + expiry calendar; cannot modify |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Certificate Health

**Purpose:** Instant security posture for all SSL certificates.

**Certificate Health Banner:**

| State | Colour | Text |
|---|---|---|
| ✅ All certs healthy | Green | "2,058 active certificates · 0 expiring in < 30 days · Auto-renewal active" |
| ⚠ Renewal due | Amber | "4 certificates expiring in < 30 days · Action required" |
| 🚨 Cert expiring in < 7 days | Red | "1 certificate expiring in 5 days — IMMEDIATE renewal required" |
| 💀 Cert expired | Red pulsing | "1 certificate EXPIRED — portal {subdomain} showing browser security warnings" |

**Header elements:**
- H1 "DNS & Certificate Manager"
- Certificate health banner
- Total certificates: "2,058 active ACM certificates"
- Total DNS records: "4,280 Route53 records across 3 hosted zones"
- "Request New Certificate" button (Admin/DevOps)
- "Add DNS Record" button (Admin/DevOps)
- Last sync: "Synced from AWS ACM + Route53: 15 min ago"

---

### Section 2 — KPI Strip

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Total Certificates | Count of all active ACM certs | — |
| Auto-renewal Active | % of certs with auto-renewal enabled | < 95% = amber |
| Expiring < 30 days | Certs expiring within 30 days | > 0 = amber |
| Expiring < 7 days | Certs expiring within 7 days | > 0 = red |
| Expired | Certs past expiry date | > 0 = red (immediate action) |
| DNS Record Changes (7d) | Count of DNS modifications in last 7 days | — |

---

### Section 3 — ACM Certificate Inventory

**Purpose:** Complete list of all SSL/TLS certificates managed in AWS Certificate Manager.

**Certificate Inventory Table:**

| Column | Description | Sortable |
|---|---|---|
| Domain | Primary domain name on the certificate | ✅ |
| SANs | Subject Alternative Names count (additional domains on same cert) | — |
| Type | Wildcard (*.example.com) · Single-domain · Multi-domain (SAN) | ✅ |
| Validation Method | DNS validation · Email validation | ✅ |
| Issued By | AWS ACM (auto-renewed) · Third-party (manually managed) | ✅ |
| Issued Date | When cert was last issued/renewed | ✅ |
| Expiry Date | When cert expires | ✅ |
| Days to Expiry | Number (colour: green > 60 · amber 14–60 · red 7–14 · pulsing red < 7) | ✅ |
| Auto-renewal | ✅ Enabled · ⚠ DNS validation pending · ❌ Disabled | — |
| CloudFront | Count of distributions using this cert | — |
| Status | Issued ✅ · Pending validation ⏳ · Expired ❌ · Revoked 🚫 | ✅ |
| Actions | View detail · Renew · Revoke |

**Certificate categories (filter tabs):**
- Platform certs: certs for platform-owned domains (srav.io, api.srav.io, admin.srav.io, etc.)
- Institution certs: certs for institution custom subdomains (e.g., *.vibrantacademy.com)
- Wildcard certs: *.{domain} covering all subdomains of an institution
- Expiring soon: filter to certs with < 30 days

**Filter bar:**
- Type: All / Wildcard / Single / SAN
- Status: All / Issued / Pending / Expiring / Expired
- Validation method: All / DNS / Email
- Domain search: text search on domain name

**"View detail" → opens cert-detail-drawer (480px)**

---

### Section 4 — Certificate Detail Drawer (cert-detail-drawer)

**Purpose:** Full detail for a single ACM certificate.

**Drawer Width:** 480px
**Tabs:** Domain · Expiry · Validation · CloudFront Mapping

---

#### Tab 1 — Domain

**Fields:**

| Field | Value |
|---|---|
| Certificate ARN | Full ARN (click to copy) |
| Primary Domain | `*.vibrantacademy.com` |
| Subject Alternative Names | `vibrantacademy.com` · `www.vibrantacademy.com` (2 SANs) |
| Type | Wildcard |
| Key Algorithm | RSA 2048 |
| Signature Algorithm | SHA-256 with RSA |
| Serial Number | Masked (first 8 chars + `••••`) |
| Issued By | Amazon |
| Region | ap-south-1 |
| Certificate Transparency | Logged ✅ |

---

#### Tab 2 — Expiry

**Fields:**

| Field | Value |
|---|---|
| Issued Date | Jan 15, 2026 |
| Expiry Date | Jan 15, 2027 |
| Days Remaining | 302 days |
| Auto-renewal | ✅ Enabled (ACM auto-renews 60 days before expiry) |
| Renewal Status | Not yet due (auto-renewal runs at 60-day mark) |
| Last Renewed | Jan 15, 2026 (previous cert expired Jan 15, 2025) |

**Renewal countdown (only shown when < 60 days to expiry):**
- Large countdown: "Auto-renewal begins in: 242 days"
- Manual renewal button: "Renew Now" — triggers ACM RequestCertificate API; useful when auto-renewal has failed

**Renewal failure handling:**
- If ACM auto-renewal fails (DNS validation record missing → common issue when institution changes their DNS provider): amber alert "Auto-renewal failed — DNS validation record missing. Add the required CNAME record below."
- CNAME record to add shown inline with "Copy value" button

---

#### Tab 3 — Validation

**Fields:**

| Field | Value |
|---|---|
| Validation Method | DNS validation |
| Validation Status | ✅ Success |
| Validation Domain | `_acme-challenge.vibrantacademy.com` |
| Validation CNAME | `_acme-challenge.vibrantacademy.com → {random-string}.acm-validations.aws` |
| Validation Record in Route53 | ✅ Present |

**If validation pending (new cert request or renewal failure):**
- Amber banner: "Certificate pending DNS validation"
- Required CNAME record shown with copy buttons for name and value
- "Add to Route53 automatically" button (only for domains where Route53 is the DNS provider) → calls Route53 ChangeResourceRecordSets API to add the validation CNAME
- "I've added it externally" button (for institution domains with external DNS) → triggers ACM DescribeCertificate polling
- Validation propagation check: "CNAME detected globally ✅" / "CNAME not yet propagating ⏳ (check DNS propagation tab)"

**Email validation (for certs using email method):**
- List of email addresses where validation emails were sent
- "Resend validation email" button
- Status per email: Sent · Clicked · Not responded

---

#### Tab 4 — CloudFront Mapping

**Purpose:** Show which CloudFront distributions are using this certificate.

**Mapping Table:**

| Distribution | Domain | Origin | Status | Last Deploy |
|---|---|---|---|---|
| E1ABCDEF (vibrantacademy CDN) | `*.vibrantacademy.com` | ALB: platform-alb | ✅ Deployed | 3 days ago |
| E2GHIJKL (vibrantacademy assets) | `assets.vibrantacademy.com` | S3: vibrant-assets | ✅ Deployed | 1 week ago |

**Alert:** If a cert is within 30 days of expiry and is attached to a CloudFront distribution: red banner "This certificate is attached to {n} CloudFront distributions. Expiry will affect all distributions. Renew immediately."

**"Update distribution to use new cert" action:** After a manual cert renewal, if the new cert ARN is different, this button updates each distribution's SSL settings to point to the new cert ARN.

---

### Section 5 — Certificate Expiry Calendar

**Purpose:** Visual calendar showing all upcoming certificate renewals and expirations.

**Route:** `/engineering/dns-certs/?part=expiry-calendar`

**Calendar view:** Month view (default) · 3-month view · List view

**Calendar entries:**
- Each expiring certificate shown as a chip on its expiry date
- Chip colour: green (> 60 days away) · amber (30–60 days) · red (< 30 days) · black (overdue)
- Chip text: domain name + days remaining

**Upcoming expirations summary card:**
- "Next expiration: `*.sunriseacademy.com` — Apr 28, 2026 (38 days)"
- "This month: 3 certs expire — all have auto-renewal active"
- "Certs requiring manual action: 0"

**Notification settings (Admin):**
- Email alert schedule: 30 days before · 14 days before · 7 days before · day of expiry
- Recipients: configurable (default: DevOps + Platform Admin)
- Configured per-certificate or platform-wide default

---

### Section 6 — Route53 DNS Record Manager

**Purpose:** View and manage all DNS records across all Route53 hosted zones without AWS console access.

**Hosted Zones:**
The platform manages 3 Route53 hosted zones:
1. `srav.io` — platform-owned main domain
2. `api.srav.io` — API subdomain (separate zone for finer control)
3. Institution custom domains — a separate hosted zone per institution that has delegated DNS to the platform (institutions that use Route53; most use external DNS providers)

**Hosted Zone Selector:**
Dropdown at top of the DNS record table — select which zone to view.

**DNS Record Table:**

| Column | Description | Filterable |
|---|---|---|
| Record Name | Full DNS name (e.g., `vibrant.srav.io`) | ✅ |
| Type | A · AAAA · CNAME · MX · TXT · NS · SOA · ALIAS | ✅ |
| Value | Record value (IP, hostname, or text — truncated to 80 chars) | — |
| TTL | Time to live in seconds | ✅ |
| Routing Policy | Simple · Weighted · Latency · Failover · Geolocation | ✅ |
| CloudFront Alias | Whether this is a CloudFront ALIAS record | ✅ |
| Health Check | AWS health check linked (for failover routing) | — |
| Last Modified | Timestamp | ✅ |
| Modified By | Actor | — |
| Actions | Edit · Delete · View history |

**Key record categories:**

Platform infrastructure records:
- `srav.io` A record → CloudFront distribution (ALIAS)
- `api.srav.io` A record → ALB (ALIAS)
- `admin.srav.io` A record → CloudFront admin distribution (ALIAS)
- Wildcard `*.srav.io` CNAME → CloudFront

Institution subdomain records (one per active institution):
- `vibrant.srav.io` CNAME → CloudFront institution distribution

ACM validation records:
- `_acme-challenge.{domain}` CNAME records for certificate validation
- Shown with "ACM Validation" tag; managed automatically via cert workflow

**Filter bar:**
- Type: All / A / CNAME / TXT / MX
- Routing policy: All / Simple / Weighted / Failover
- CloudFront alias: All / Yes / No
- Search: record name text search

**"Add DNS Record" → inline form or dns-record-drawer:**
- Record name: text input
- Type: dropdown
- Value: text input (with format validation per type — IP format for A, hostname format for CNAME, etc.)
- TTL: number input (default: 300s; range: 60–86400)
- Routing policy: Simple (default) / Weighted / Failover
- Confirmation: "Preview change" before applying

**"Edit DNS Record" → dns-record-drawer**
**"Delete DNS Record" → confirmation modal with propagation warning**

---

### Section 7 — DNS Record Drawer (dns-record-drawer)

**Purpose:** Full detail, edit, propagation status, and history for a single DNS record.

**Drawer Width:** 480px
**Tabs:** Record Details · Edit · Propagation Status · History

---

#### Tab 1 — Record Details

All fields from the table, plus:
- Full value (not truncated)
- AWS Route53 Change ID (for the last change — for troubleshooting)
- Health check status (if linked): Healthy ✅ / Unhealthy ❌ / Unknown
- DNSSEC signed: ✅ / ❌ (DNSSEC not yet enabled — shown as info note)

---

#### Tab 2 — Edit

Editable fields:
- Value (most common change)
- TTL
- Comment (internal note — not part of DNS record; stored in `platform_dns_records.notes`)

Non-editable after creation:
- Record name (must delete + recreate to change name)
- Record type (must delete + recreate to change type)

**"Apply change" button:**
- Confirmation: "This change will propagate globally within TTL ({n} seconds). Are you sure?"
- For critical records (platform apex, wildcard): additional warning "This is a platform-critical record. Changes affect all traffic routing."
- 2FA required for: A records on platform domains + wildcard records
- On apply: Route53 ChangeResourceRecordSets API → change propagates globally

---

#### Tab 3 — Propagation Status

**Purpose:** Verify that a recent DNS change has propagated to global resolvers.

**Propagation checker:**
After any DNS change (or on manual "Check now"):
- Platform queries the record from 8 global DNS resolvers:
  - Google (8.8.8.8, 8.8.4.4)
  - Cloudflare (1.1.1.1, 1.0.0.1)
  - OpenDNS (208.67.222.222)
  - AWS Route53 resolver (ap-south-1)
  - Quad9 (9.9.9.9)
  - Comodo (8.26.56.26)

**Propagation table:**

| Resolver | Returned Value | Expected Value | Status | Last Checked |
|---|---|---|---|---|
| Google 8.8.8.8 | 3.7.8.4 | 3.7.8.4 | ✅ Propagated | 2 min ago |
| Cloudflare 1.1.1.1 | 3.7.8.4 | 3.7.8.4 | ✅ Propagated | 2 min ago |
| OpenDNS | Old IP: 3.7.8.2 | 3.7.8.4 | ⏳ Stale | 2 min ago |
| AWS Route53 | 3.7.8.4 | 3.7.8.4 | ✅ Propagated | 2 min ago |

**Overall propagation status:** 6/8 resolvers propagated · "Expected full propagation in ~3 min (TTL: 300s)"

**"Re-check" button:** Triggers a fresh DNS query to all 8 resolvers.

---

#### Tab 4 — History

**Immutable log of all changes to this record:**

| Timestamp | Actor | Action | Before | After |
|---|---|---|---|---|
| 2h ago | Priya (Admin) | Edit value | `3.7.8.2` | `3.7.8.4` |
| 6 months ago | Arjun (DevOps) | Created | — | `3.7.8.2` |

---

### Section 8 — DNS Propagation Checker (Standalone)

**Purpose:** Ad-hoc propagation check for any domain — not just records managed in Route53.

**Route:** `/engineering/dns-certs/?part=propagation`

**Use case:** Checking propagation of changes made externally (e.g., institution's DNS provider, MX records for SES verification).

**Input:** Domain name + record type (A · CNAME · MX · TXT)

**Output:** Same 8-resolver table as the record drawer propagation tab, but for any domain.

**Common use cases:**
- Verify ACM validation CNAME propagated after institution added it to their external DNS
- Verify new institution subdomain CNAME is resolving correctly
- Verify SES MX/TXT records for new sender domain

---

### Section 9 — CloudFront Distribution ↔ Certificate Mapping

**Purpose:** Confirm that every CloudFront distribution has a valid, non-expiring SSL certificate attached.

**Route:** `/engineering/dns-certs/?part=cloudfront-map`

**Distribution-Certificate Mapping Table:**

| Distribution ID | Domain | Purpose | Attached Certificate | Cert Expiry | Cert Status | Actions |
|---|---|---|---|---|---|---|
| E1ABCDEF | `*.srav.io` | Platform portal CDN | ACM: *.srav.io | Jan 2027 | ✅ Healthy | View cert |
| E2GHIJKL | `assets.srav.io` | Static asset CDN | ACM: *.srav.io | Jan 2027 | ✅ Healthy | View cert |
| E3MNOPQR | `*.vibrantacademy.com` | Vibrant CDN | ACM: *.vibrantacademy.com | Apr 28, 2026 | ⚠ 38 days | Renew cert |
| E4STUVWX | `*.alphacoaching.com` | Alpha CDN | ACM: *.alphacoaching.com | Jan 2027 | ✅ Healthy | View cert |

**Filters:** All / Healthy / Warning (< 60 days) / Critical (< 30 days) / Expired

**"Renew cert" action:** Opens cert-detail-drawer for the attached certificate, pre-selected on the Expiry tab.

**Unmapped distributions:** Any CloudFront distribution without a certificate → red "No certificate" badge → critical alert (HTTPS not configured).

**Orphaned certificates:** ACM certificates not attached to any CloudFront distribution or load balancer → amber badge "Unused certificate — consider deleting" (reduces clutter and annual cost if applicable).

---

### Section 10 — Certificate Request Workflow

**Purpose:** Guided flow for requesting a new ACM certificate for a new institution or domain migration.

**Trigger:** "Request New Certificate" button in page header.

**Step 1 — Domain Information:**
- Primary domain: text input (e.g., `*.sunsetacademy.com`)
- Additional SANs: optional multi-tag input (e.g., `sunsetacademy.com`, `www.sunsetacademy.com`)
- Wildcard: checkbox (if checked, prepends `*.` to domain)
- Estimated purpose: dropdown (Institution portal · API domain · Asset CDN · Internal tool)

**Step 2 — Validation Method:**
- DNS validation (recommended): ACM creates a CNAME record that must be added to the domain's DNS
  - For Route53-managed domains: "Add automatically to Route53" option (one-click)
  - For external DNS: CNAME record details shown for institution to add
- Email validation (fallback): for domains where DNS cannot be modified by the platform

**Step 3 — CloudFront Assignment (optional):**
- Attach to existing distribution: select from distribution list
- Create new distribution: link to infrastructure provisioning (C-08)
- Skip for now: cert created in pending state; assigned later

**Step 4 — Review & Request:**
- Summary of all details
- "Request Certificate" button → AWS ACM RequestCertificate API
- Certificate appears in inventory with "Pending validation" status

**Post-request workflow:**
- System monitors validation status (polls ACM DescribeCertificate every 5 min)
- When DNS validation CNAME is detected and cert is issued: notification to DevOps + page-level alert banner "New certificate issued: *.sunsetacademy.com"
- Cert automatically moves to "Issued" status in inventory

---

## 5. User Flow

### Flow A — Certificate Expiry Alert and Renewal

1. DevOps Engineer receives email: "Certificate `*.alphacoaching.com` expiring in 30 days"
2. Opens `/engineering/dns-certs/` → amber health banner
3. Clicks cert row → cert-detail-drawer → Expiry tab
4. Auto-renewal: ⚠ DNS validation pending (institution changed DNS provider last month)
5. Validation tab: shows required CNAME — "Add to Route53 automatically" not available (external DNS)
6. DevOps copies CNAME values, sends to institution IT contact with instructions
7. Institution adds CNAME to their Cloudflare DNS
8. 30 min later: Propagation Status shows CNAME detected globally
9. ACM auto-renews within 24h; cert issued status updates
10. Expiry date updates to next year; health banner returns to green

### Flow B — New Institution Custom Domain Setup

1. New institution (Sunrise Academy) wants custom domain `*.sunriseacademy.com`
2. DevOps clicks "Request New Certificate"
3. Step 1: primary domain `*.sunriseacademy.com` · SAN `sunriseacademy.com`
4. Step 2: DNS validation — external DNS (institution uses GoDaddy)
5. Step 3: Assign to existing wildcard CloudFront distribution (E1ABCDEF reused via SNI)
6. Step 4: Certificate requested → pending validation
7. CNAME record details copied and sent to institution IT team
8. After CNAME added by institution: platform detects propagation; ACM issues cert in ~10 min
9. Certificate attached to CloudFront distribution
10. DNS CNAME: `sunrise.srav.io → cloudfront-distribution` added via "Add DNS Record"
11. DNS propagation checked via propagation checker — all 8 resolvers green within 5 min

### Flow C — Emergency DNS Rollback

1. DevOps updates A record for `api.srav.io` to new ALB IP
2. Propagation checker: 8/8 resolvers updated within 3 min
3. 10 min later: C-04 API Health shows error rate spike — new ALB misconfigured
4. DevOps opens dns-record-drawer → Edit tab → restores previous IP value → "Apply change"
5. 2FA confirmed (platform-critical record)
6. Rollback propagates in < 300s (TTL)
7. Propagation confirmed; error rate drops back to normal
8. History tab: both changes logged with actors and timestamps

---

## 6. Component Structure (Logical)

```
DNSCertManagerPage
├── PageHeader
│   ├── CertHealthBanner
│   ├── PageTitle
│   ├── SyncStatusNote
│   ├── RequestCertButton
│   └── AddDNSRecordButton
├── KPIStrip × 6
├── CertInventoryTable
│   ├── FilterBar (tabs: Platform / Institution / Wildcard / Expiring)
│   └── CertRow × 2,058
├── CertDetailDrawer (480px)
│   └── DrawerTabs
│       ├── DomainTab
│       ├── ExpiryTab
│       ├── ValidationTab
│       └── CloudFrontMappingTab
├── ExpiryCalendar
│   ├── MonthView / 3MonthView / ListView
│   └── UpcomingExpirySummaryCard
├── DNSRecordManager
│   ├── HostedZoneSelector
│   ├── FilterBar
│   └── DNSRecordTable
├── DNSRecordDrawer (480px)
│   └── DrawerTabs
│       ├── RecordDetailsTab
│       ├── EditTab
│       ├── PropagationStatusTab
│       └── HistoryTab
├── PropagationChecker (standalone)
│   ├── DomainInput
│   └── ResolverResultsTable × 8
├── CloudFrontCertMappingTable
└── CertRequestWorkflow (modal, 4 steps)
    ├── Step1_DomainInfo
    ├── Step2_ValidationMethod
    ├── Step3_CloudFrontAssignment
    └── Step4_ReviewAndRequest
```

---

## 7. Data Model (High-Level)

### platform_acm_certificates (synced from AWS ACM API)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| aws_cert_arn | VARCHAR(512) | unique |
| primary_domain | VARCHAR(253) | |
| sans | JSONB | array of additional domain names |
| cert_type | ENUM | wildcard/single/san |
| validation_method | ENUM | dns/email |
| issued_at | TIMESTAMPTZ | nullable (pending certs have null) |
| expires_at | TIMESTAMPTZ | nullable |
| status | ENUM | pending_validation/issued/expired/revoked/inactive |
| auto_renewal | BOOLEAN | |
| renewal_status | ENUM | not_due/pending/success/failed |
| category | ENUM | platform/institution/wildcard |
| institution_id | UUID FK → platform_tenants | nullable |
| cloudfront_distribution_ids | JSONB | array of distribution IDs using this cert |
| synced_at | TIMESTAMPTZ | |
| requested_by | UUID FK → platform_staff | nullable (auto-renewed = null) |

### platform_dns_records (synced from Route53 + local audit)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| hosted_zone_id | VARCHAR(50) | Route53 hosted zone ID |
| record_name | VARCHAR(253) | fully-qualified domain name |
| record_type | ENUM | A/AAAA/CNAME/MX/TXT/NS/SOA/ALIAS |
| record_value | TEXT | record value(s) — JSONB for multi-value records |
| ttl | INTEGER | seconds |
| routing_policy | ENUM | simple/weighted/latency/failover/geolocation |
| is_cloudfront_alias | BOOLEAN | |
| health_check_id | VARCHAR(100) | nullable |
| notes | TEXT | internal notes (not part of DNS record) |
| last_route53_change_id | VARCHAR(50) | Route53 change batch ID |
| synced_at | TIMESTAMPTZ | |
| last_modified_by | UUID FK → platform_staff | nullable |
| last_modified_at | TIMESTAMPTZ | |

### platform_dns_change_log (immutable)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| record_id | UUID FK → platform_dns_records | |
| record_name | VARCHAR(253) | denormalised |
| actor_id | UUID FK → platform_staff | |
| action | ENUM | created/updated/deleted |
| before_value | TEXT | nullable |
| after_value | TEXT | nullable |
| twofa_verified | BOOLEAN | |
| route53_change_id | VARCHAR(50) | |
| created_at | TIMESTAMPTZ | set by DB trigger |

### platform_cert_request_log

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| cert_id | UUID FK → platform_acm_certificates | nullable (pending) |
| primary_domain | VARCHAR(253) | |
| requested_by | UUID FK → platform_staff | |
| requested_at | TIMESTAMPTZ | |
| validation_method | ENUM | dns/email |
| validation_cname_name | VARCHAR(253) | nullable (DNS validation) |
| validation_cname_value | VARCHAR(253) | nullable |
| validation_detected_at | TIMESTAMPTZ | nullable |
| issued_at | TIMESTAMPTZ | nullable |
| status | ENUM | pending_validation/issued/failed |

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| DNS record name format | Must be valid FQDN; max 253 chars; no spaces; validated against FQDN regex |
| A record value | Must be a valid IPv4 address; `0.0.0.0` blocked |
| CNAME cannot coexist with other types | Route53 rule: CNAME at apex blocked (must use ALIAS instead); system enforces this |
| Delete ACM validation record | Blocked if certificate using that validation CNAME is not yet expired; validation records cannot be deleted while cert is pending renewal |
| 2FA for production DNS changes | Required for: A records on platform domains · wildcard CNAME records · any record affecting > 100 tenants |
| Certificate deletion | Only allowed for expired or revoked certs; cannot delete active cert attached to CloudFront distribution (must detach first) |
| New cert validation | Must complete DNS validation within 72 hours or cert request expires; system reminds every 24h |
| Wildcard cert scope | `*.example.com` covers one subdomain level only (covers `sub.example.com` but not `sub.sub.example.com`) — note shown in cert detail |
| TTL minimum | 60 seconds minimum; values below 60 rejected |
| SOA/NS record edits | Blocked — Route53 SOA and NS records are managed by AWS; editing attempted triggers: "This record type is managed by AWS and cannot be modified" |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| Route53 IAM | `route53:ListResourceRecordSets` + `route53:ChangeResourceRecordSets` + `route53:GetHostedZone` — scoped to specific hosted zone ARNs; cannot modify DNS for zones not in the platform's account |
| ACM IAM | `acm:ListCertificates` + `acm:DescribeCertificate` + `acm:RequestCertificate` + `acm:DeleteCertificate` — scoped to ap-south-1; no wildcard resource access |
| DNS change audit | Every DNS change goes through `platform_dns_change_log` (immutable); before/after values stored; Route53 Change ID for AWS CloudTrail correlation |
| Certificate private keys | ACM private keys are never exposed; the platform only handles metadata (ARN, domain, expiry, status) via ACM API — no access to key material |
| 2FA for critical records | Platform-critical DNS records (those affecting all 2,050 portals if misconfigured) require TOTP confirmation before any edit is applied |
| Cert expiry monitoring | Celery beat checks expiry daily; alerts sent 30, 14, 7 days before expiry; P0 incident auto-created if a cert expires without renewal |
| DNS propagation check | Platform makes outbound DNS queries to 8 resolvers; these queries use the record name only (no sensitive data in query) |
| External validation CNAMEs | ACM validation CNAME values shown in platform are generated by AWS; the platform displays them but never generates or stores key material |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| Certificate expires during exam | Celery beat fires 1h before expiry if cert is near-expired; P0 incident auto-created; DevOps receives PagerDuty page; manual renewal triggered immediately |
| Route53 API throttled | Route53 has a 5 req/s default limit on ChangeResourceRecordSets; platform queues DNS changes with 200ms delay between requests; bulk operations (e.g., adding records for 50 new institutions) use exponential backoff |
| ACM auto-renewal fails silently | Celery checks cert status daily; if expiry < 60 days and `renewal_status != success`: alert fired; DevOps investigated within 24h |
| Institution changes DNS provider mid-renewal | ACM renewal fails (CNAME not found); platform detects via `renewal_status = failed`; sends email to DevOps + institution IT contact with new CNAME values for their new DNS provider |
| Wildcard cert covers too many subdomains (CN mismatch) | `*.srav.io` does not cover `sub.sub.srav.io`; system warns if a CloudFront distribution domain doesn't match the cert's domains at assignment time |
| Two DevOps engineers edit same DNS record simultaneously | Route53 ChangeResourceRecordSets is atomic; last write wins; both changes logged in `platform_dns_change_log`; no partial state |
| DNS record deleted that is required by ACM validation | System checks if record is an ACM validation CNAME before allowing delete; blocks deletion if cert is active and using this validation record |
| Certificate issued in wrong region | ACM certs for CloudFront must be in `us-east-1` (global); for ALB use in ap-south-1, cert must be in ap-south-1; system validates region at request time and shows error if wrong region selected |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| 2,058 certificates in inventory | Loaded with server-side pagination (50 per page); filter queries use PostgreSQL index on `expires_at` + `status`; initial load < 100ms |
| Route53 DNS record table (4,280 records) | Paginated 100 per page; indexed on `hosted_zone_id` + `record_type`; name search uses PostgreSQL LIKE with index on first 50 chars |
| ACM sync | Celery beat job every 30 min; calls ACM ListCertificates (paginated, 100 per call) + DescribeCertificate for certs with status changes; incremental — only fetches changed certs |
| Route53 sync | Celery beat job every 15 min; ListResourceRecordSets per hosted zone; stores changes to `platform_dns_records` |
| Propagation checker | Platform makes 8 concurrent DNS queries (asyncio); all 8 results returned in < 2s (DNS query timeout: 5s each) |
| Expiry calendar | Pre-computed from `platform_acm_certificates` ORDER BY `expires_at`; trivial query; calendar rendering server-side |
| CloudFront mapping | Maintained in `platform_acm_certificates.cloudfront_distribution_ids` JSONB field; updated at sync time; no separate join needed for mapping table |
