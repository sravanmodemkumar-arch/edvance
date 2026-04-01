# C-13 — Security Operations Dashboard

> **Route:** `/engineering/security/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · Security Engineer (Role 16)
> **Read Access:** DevOps/SRE (Role 14)
> **File:** `c-13-security-ops.md`
> **Priority:** P0 — Required before first institution goes live
> **Status:** ⬜ Amendment pending — G6 (VAPT Schedule tab) · G16 (Data Localization Audit tab) · G17 (CERT-In Report tab) · G24 (Security Audit Log tab)

---

## 1. Page Name & Route

**Page Name:** Security Operations Dashboard
**Route:** `/engineering/security/`
**Part-load routes:**
- `/engineering/security/?part=kpi` — security health KPI
- `/engineering/security/?part=waf` — AWS WAF rules panel
- `/engineering/security/?part=auth-heatmap` — failed auth heatmap
- `/engineering/security/?part=lockout-log` — account lockout event log
- `/engineering/security/?part=jwt-anomaly` — JWT anomaly detection
- `/engineering/security/?part=cve` — CVE tracker
- `/engineering/security/?part=certIn` — CERT-In incident log
- `/engineering/security/?part=dpdpa` — DPDPA breach tracker
- `/engineering/security/?part=vapt` — VAPT results
- `/engineering/security/?part=dependency-scan` — dependency vulnerability scanner
- `/engineering/security/?part=threats` — active threat alerts

---

## 2. Purpose (Business Objective)

The Security Operations Dashboard is the Security Engineer's command centre for protecting all 2,050 institution portals and the platform's internal engineering surface. With 7.6M potential student accounts and all their exam data, PII, and payment history, the platform is a high-value target.

The page provides both real-time threat detection (failed auth bursts, suspicious JWT patterns, WAF block events) and compliance management (CERT-In 6-hour incident reporting countdown, DPDPA 72-hour breach notification tracking). Any data breach that is not reported to CERT-In within 6 hours is a regulatory violation with criminal liability for the company.

**Business goals:**
- Detect credential-stuffing, brute-force, and session hijacking attempts in near-real-time
- Control AWS WAF rules (block/rate-limit/geo-restrict) without AWS console access
- Track CVEs in platform dependencies with severity triage
- Manage CERT-In and DPDPA incident reporting with automated countdown timers
- Maintain VAPT findings tracker with remediation status

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full view + all write actions |
| Security Engineer (16) | Level 4 | Full view + all write actions |
| DevOps / SRE (14) | Level 4 — Read | View WAF · threat alerts · cannot modify |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Security Posture

**Purpose:** Instant overall security health verdict.

**Security Posture Score:**
- Calculated composite score (0–100): based on unresolved critical CVEs · active threats · WAF bypasses · overdue VAPT findings
- Display: large circular gauge, colour: green (80–100) · amber (60–79) · red (< 60)
- Trend: "↑ improved from 74 last week"

**Active Alerts Banner:**
- Red pulsing if any: P0 active threat · CERT-In countdown active · Critical CVE with no remediation plan
- Example: "🚨 CERT-In breach countdown active: 4h 12m remaining"

**Header elements:**
- H1 "Security Operations Dashboard"
- Security Posture Score gauge
- Active alerts count: "3 active alerts"
- "Create Security Incident" button → pre-fills C-18
- Last full security scan: "OWASP ZAP scan: 3 days ago"

---

### Section 2 — KPI Strip

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Failed Logins (1h) | Count of failed authentication attempts | > 500 amber · > 2,000 red |
| Locked Accounts (24h) | Count of auto-locked accounts | > 10 amber |
| WAF Blocks (1h) | Count of requests blocked by WAF | spike > 200% baseline = amber |
| Critical CVEs | Unresolved CVSS > 9.0 CVEs | > 0 = red |
| CERT-In Incidents | Open incidents (not yet reported) | > 0 = red (immediate action) |
| DPDPA Notifications | Open breach notifications pending | > 0 = red |

---

### Section 3 — AWS WAF Rules Panel

**Purpose:** View, add, modify, and reorder AWS WAF rules protecting all platform endpoints.

**WAF Rules Table:**

| Priority | Rule Name | Type | Action | Scope | Hit Rate (24h) | Last Modified | Status |
|---|---|---|---|---|---|---|---|
| 1 | Block known bad IPs | IP Set | Block | All | 842 blocks | 2 days ago | ✅ Active |
| 2 | Rate limit auth endpoints | Rate-based | Count → Block after 100/5min | /api/auth/* | 124 triggers | 1 week ago | ✅ Active |
| 3 | Rate limit exam submit | Rate-based | Block after 200/min | /api/exams/*/submit/ | 12 triggers | 3 days ago | ✅ Active |
| 4 | Geo-restrict admin routes | Geo match | Block if not IN/SG/US | /engineering/* | 34 blocks | 1 month ago | ✅ Active |
| 5 | AWS Managed (CommonRuleSet) | Managed | Block | All | 1,240 blocks | Auto | ✅ Active |
| 6 | AWS Managed (SQLi) | Managed | Block | All | 84 blocks | Auto | ✅ Active |
| 7 | Block TOR exit nodes | IP Set | Block | All | 192 blocks | Auto | ✅ Active |

**Add Rule (Security Engineer / Admin):**
- Rule type: IP Set match · Rate-based · Geo match · String match · SQL injection · XSS · Custom regex
- Action: Block · Count · CAPTCHA challenge
- Scope: path pattern (e.g., `/api/exams/*`) · all requests
- Priority: number (lower = evaluated first)

**Edit/Delete Rule:**
- Edit: inline form; changes take effect within 1 min (CloudFront distribution update)
- Delete: confirmation modal; "Are you sure? Deleting a blocking rule may expose endpoints."
- Reorder: drag-and-drop priority reordering (or edit priority number)

**IP Block List:**
- Dedicated sub-panel: manually blocked IPs + block reason + blocked by + expires at
- "Add IP to block list" → CIDR notation input + reason + expiry (1h / 6h / 24h / 7d / permanent)
- "Emergency IP block" → one-click block from failed-auth heatmap (feeds directly into WAF IP set)

**WAF Metrics Charts:**
- Requests blocked per hour (last 24h) — by rule name (stacked bars)
- Geographic distribution of blocked IPs

**Data Flow:**
- WAF rules from AWS WAFV2 API (GetWebACL + ListWebACLs)
- Hit rate from CloudWatch WAF metrics
- Cached in Memcached 5 min; full refresh on page load
- Rule changes applied via WAFV2 UpdateWebACL API

---

### Section 4 — Failed Auth Heatmap

**Purpose:** Visual detection of credential-stuffing, brute-force, and distributed attack patterns.

**Heatmap View:**
- X axis: time (last 24h in 15-min buckets)
- Y axis: source IP / country / tenant portal
- Cell colour: green (normal) → amber → red (high failure rate)

**View toggles:**
- By IP address: shows which IPs are generating most failures
- By country: geographic distribution (useful for detecting offshore attack waves)
- By tenant portal: which portals are being targeted (useful for targeted attacks)
- By time of day: when failures cluster (typical: overnight for automated attacks)

**Top offenders table:**

| IP Address | Country | Failed Attempts (1h) | Targeted Accounts | Unique IPs in subnet | Action |
|---|---|---|---|---|---|
| 45.142.212.100 | Russia | 842 | 124 | 48 (coordinated) | Block IP · Block /24 subnet |
| 104.21.18.42 | USA | 124 | 12 | 1 | Block IP · Monitor |

**Actions per row:**
- "Block IP" → immediately adds to WAF IP block set (30-day expiry default)
- "Block /24 subnet" → blocks the /24 CIDR (wider block) — 2FA required (higher blast radius)
- "Investigate" → jumps to auth-service CloudWatch logs filtered to this IP

**Pattern detection:**
- Distributed attack detection: if 50+ IPs from same /24 subnet with synchronized attempts → amber banner "Coordinated attack detected from subnet {x.x.x.0/24}"
- Credential stuffing pattern: many different accounts, low per-account failure rate from same IP → flag raised

**Data Flow:**
- Source: auth-service Lambda CloudWatch logs (`failed_login` events)
- Aggregated by Celery job every 15 min into `platform_failed_auth_stats` ORM table (keyed by IP + 15-min bucket)
- Real-time feed: last 100 failed login events (15s poll)

---

### Section 5 — Account Lockout Event Log

**Purpose:** Log of all student and staff account lockouts with investigation links.

**Columns:**

| Column | Description |
|---|---|
| Timestamp | When account was locked |
| Account Type | Student · Staff |
| Account Email | Masked: `jo**@gmail.com` |
| Tenant | Institution portal (for student accounts) |
| Lock Reason | Too many failed logins · Admin manual lock · Suspicious pattern |
| Failed Attempts | Count of failures that triggered lock |
| Source IPs | List of IPs that generated failures |
| Lock Duration | Until unlocked by admin or auto-expires (30 min default) |
| Status | Locked · Auto-unlocked · Admin unlocked |

**Filters:** Account type · Date range · Lock reason · Still locked (toggle)

**Quick unlock (Security/Admin):**
- Per-row "Unlock" action → immediate unlock without 2FA (speed for legitimate user support)
- Unlock logged with actor + timestamp

**Mass unlock:**
- "Unlock all accounts locked in last 1h" → for mass false-positive lockout events (e.g., SES IP changed causing all password-reset emails to bounce → users retry → lockout)
- 2FA required

---

### Section 6 — JWT Anomaly Detection

**Purpose:** Detect suspicious JWT token usage patterns that may indicate session hijacking or token theft.

**Anomaly Types Detected:**

| Anomaly | Description | Risk Level |
|---|---|---|
| Token reuse from multiple IPs | Same JWT used from 2+ geographically distinct IPs within 5 min | Critical |
| Token used after logout | JWT used after explicit logout event (token should be in deny-list) | High |
| Algorithm confusion | JWT decoded with algorithm other than expected HS256/RS256 | Critical |
| Future iat claim | JWT with `issued_at` in the future (replay or forged token) | Critical |
| Expired token accepted | JWT with exp in past being accepted (server-side validation bug) | Critical |
| Staff JWT from student endpoint | Staff JWT used on student-facing endpoints | High |

**Anomaly Events Table:**

| Timestamp | Anomaly Type | User | JWT ID (jti) | IP(s) Involved | Action Taken |
|---|---|---|---|---|---|
| 5 min ago | Token reuse from multiple IPs | `student_48291` | jti:abc123 | 45.1.2.3 (IN) + 192.20.1.1 (RU) | Token revoked · Account locked |
| 2h ago | Token used after logout | `staff_priya@...` | jti:def456 | 10.0.0.1 | Token revoked |

**Automatic responses (configured):**
- Token reuse from different country: automatic token revocation + account lock
- Algorithm confusion: automatic token revocation + security incident created in C-18
- Expired token accepted: automatic alert to Backend team (indicates server-side bug) + C-18 incident

**Manual actions per event:**
- "Revoke token" → adds `jti` to `platform_jwt_denied_tokens` ORM table (with `expires_at` field; Celery nightly cleanup removes expired entries)
- "Lock account" → locks the associated account
- "View full JWT payload" → decoded (non-sensitive fields only; signature not exposed)
- "Create security incident" → pre-fills C-18

**Data Flow:**
- JWT validation middleware logs anomalies to CloudWatch
- Celery job aggregates from CloudWatch every 5 min into `platform_jwt_anomalies` table
- Real-time: 30s HTMX poll

---

### Section 7 — CVE Tracker

**Purpose:** Track security vulnerabilities in all platform dependencies.

**Data Sources:**
- Python: `pip-audit` (run in CI/CD C-09 on every commit) + Snyk for continuous monitoring
- JavaScript: `npm audit` (CI/CD)
- System packages: Amazon Inspector (EC2/Lambda)

**CVE Summary Table:**

| Severity | Count | Change from last week |
|---|---|---|
| Critical (CVSS 9.0–10.0) | 2 | +1 (new) |
| High (CVSS 7.0–8.9) | 8 | -1 (fixed) |
| Medium (CVSS 4.0–6.9) | 24 | +3 |
| Low (CVSS 0.1–3.9) | 42 | +2 |

**CVE Details Table:**

| CVE ID | Severity | Package | Version | CVSS | Affected Service | Status | Remediation |
|---|---|---|---|---|---|---|---|
| CVE-2025-12345 | 🔴 Critical | `cryptography` | 41.0.3 | 9.8 | auth-service | ⏳ In progress | Upgrade to 42.0.0 |
| CVE-2025-67890 | 🔴 Critical | `pillow` | 10.0.0 | 9.1 | content-service | ✅ Fixed | Upgraded to 10.3.0 |
| CVE-2024-98765 | 🟠 High | `django` | 4.2.8 | 7.5 | All services | ⏳ In progress | Upgrade to 4.2.15 |

**Status workflow:**
- New → Triaged → In Progress → Fixed · Accepted Risk (with written justification)

**Actions per CVE:**
- "Mark as triaged" → assign to engineer + set target fix date
- "Accept risk" → Security Engineer only · 2FA · written justification (min 100 chars) · review date set
- "View in pip-audit report" → CI/CD run that first detected this CVE
- "Create fix PR" → auto-opens GitHub issue in affected repo (links to CVE ID)

**Accepted risk policy:**
- Accepted CVEs auto-expire after 30 days — must be re-accepted (prevents permanent ignoring)
- Critical CVEs cannot be accepted at risk without Platform Admin co-approval

**Dependency scanner (on-demand):**
- "Run full dependency scan" button → triggers Celery job: runs pip-audit + npm audit + Snyk API scan across all services
- Estimated 10–15 min; results update CVE table

---

### Section 8 — CERT-In Incident Log

**Purpose:** Track all security incidents that require CERT-In (Indian Computer Emergency Response Team) notification within 6 hours.

**CERT-In Reportable Events (as per CERT-In guidelines 2022):**
- Data breach (any PII of Indian citizens)
- Ransomware attacks
- DDoS attacks
- Malware spread
- Unauthorised access to critical information infrastructure
- Compromise of identity management systems

**Active Incidents Countdown:**
- For each open incident: large countdown timer "Report to CERT-In in: 4h 12m 05s"
- Background turns red when < 1 hour remaining
- Overdue: pulsing red "OVERDUE: CERT-In notification required immediately"

**Incident Table:**

| Incident | Detected At | Severity | Type | CERT-In Status | Time Remaining | Actions |
|---|---|---|---|---|---|---|
| Unauthorised access attempt — tenant_042 | 2h ago | P1 | Auth breach attempt | ⏳ Not yet submitted | 4h 12m | Submit report · View details |
| Credential stuffing attack — 842 accounts | 6h ago | P2 | Auth attack | ✅ Submitted 4h ago | — | View report |

**CERT-In Report Submission:**
- "Submit report" → opens CERT-In report form pre-filled with incident details:
  - Incident type (from CERT-In category list)
  - Date/time of discovery
  - Affected systems
  - Suspected attack vector
  - Data potentially compromised (type + estimated count)
  - Immediate actions taken
- "Download report as PDF" → formatted for CERT-In submission
- "Mark as submitted" → records submission timestamp + acknowledgement number from CERT-In portal

**Report templates:**
- Pre-built templates for each incident type
- Auto-populates: affected systems (from C-18 incident linked data) · timeline of events

---

### Section 9 — DPDPA Breach Tracker

**Purpose:** Track personal data breaches requiring notification to the Data Protection Board under DPDPA 2023 within 72 hours.

**DPDPA Breach Criteria (as per DPDPA 2023):**
- Unauthorised access to or disclosure of personal data
- Accidental destruction or loss of personal data
- Alteration of personal data without authorisation

**Active Breach Countdown:**
- Large countdown timer: "Notify Data Protection Board in: 68h 24m"
- Background amber → red when < 12h remaining

**Breach Record Table:**

| Breach | Detected | Data Type | Affected Users | DPB Status | Deadline | Action |
|---|---|---|---|---|---|---|
| Exam result data exposed via API bug | 6h ago | Exam results (non-PII) | ~840 students | ⏳ Notification draft | 66h remaining | Submit notification |

**DPB Notification Form:**
- Nature of the breach
- Data principal categories affected (students · teachers · parents)
- Approximate number affected
- Likely consequences
- Measures taken/proposed
- Contact of Data Protection Officer

**Data Localisation verification:**
- Confirms primary data storage: ap-south-1 (Mumbai) ✅
- Confirms no PII replication outside India: ✅
- If cross-border data transfer detected: immediate red flag

---

### Section 10 — VAPT Results

**Purpose:** Track Vulnerability Assessment and Penetration Testing findings with remediation status.

**VAPT Engagement History:**

| Engagement | Vendor | Type | Date | Total Findings | Open | Fixed | Status |
|---|---|---|---|---|---|---|---|
| Annual VAPT 2026 | SecureIndia Pvt Ltd | External VAPT | Jan 2026 | 42 | 8 | 34 | In remediation |
| Bug Bounty Program | HackerOne | Continuous | Ongoing | 124 (all time) | 3 | 121 | Active |
| OWASP ZAP Scan | Internal | Automated | Weekly | Last: 12 findings | 4 | 8 | Ongoing |

**Findings Table (filtered by status: Open):**

| Finding ID | Severity | Title | OWASP Category | Found By | Found At | Assigned To | Fix Deadline | Status |
|---|---|---|---|---|---|---|---|---|
| VAPT-2026-007 | 🔴 Critical | JWT algorithm not validated server-side | A02 (Auth Failures) | SecureIndia | Jan 2026 | Rohan (Backend) | Mar 15 | In Progress |
| VAPT-2026-012 | 🟠 High | Missing HSTS header on portal | A05 (Misconfiguration) | SecureIndia | Jan 2026 | Priya (Frontend) | Mar 30 | In Progress |

**Finding detail (expandable):**
- Full description · reproduction steps (masked for external findings) · CVSS score · OWASP category
- Remediation notes (engineer who owns it)
- Fix evidence (PR link · test results showing fix)

**OWASP ZAP Integration:**
- Auto-triggered weekly by CI/CD (C-09)
- Latest scan results imported automatically
- "Run OWASP ZAP scan now" button (on-demand)
- Last scan: 3 days ago · 12 findings · 4 open

---

### Section 11 — Active Threat Alerts

**Purpose:** Centralised real-time feed of all active security alerts requiring attention.

**Alert Feed:**

| Time | Alert | Severity | Source | Status | Action |
|---|---|---|---|---|---|
| 5 min ago | Credential stuffing: 842 failed logins from 48 IPs | P1 | Failed Auth Heatmap | ⚡ Active | Block IPs · Create incident |
| 22 min ago | New CVE detected: cryptography 9.8 CVSS | P2 | pip-audit CI run | ⏳ Triaging | View CVE |
| 1h ago | JWT anomaly: token reuse from RU IP | P1 | JWT Detector | ✅ Resolved | View details |
| 2h ago | WAF spike: 2,400 blocked requests in 5 min | P2 | AWS WAF | ✅ Resolved | View WAF |

**Alert filtering:** Severity · Source · Status (Active / Resolved / Acknowledged)

**Alert acknowledgement:** "Acknowledge" button → removes from active count but keeps in log

**Integration with C-18:** "Create incident" per alert → pre-fills incident with alert context

---

## 5. User Flow

### Flow A — Responding to Credential Stuffing Attack

1. KPI strip: "Failed Logins (1h): 3,200" (red alert)
2. Security Engineer opens Failed Auth Heatmap
3. Heatmap shows: 48 IPs from 45.142.212.0/24 (Russia) — coordinated attack
4. "Distributed attack detected" banner shown
5. Security Engineer clicks "Block /24 subnet" → 2FA confirmation
6. WAF rule added: block 45.142.212.0/24 (24h expiry)
7. Failed login rate drops to baseline within 2 min
8. CERT-In assessment: credential stuffing is reportable if accounts compromised
9. Runs investigation: no successful logins from attack IPs → no breach
10. Incident logged in C-18 as "Attack contained — no breach"

### Flow B — CERT-In Breach Reporting

1. Security breach detected: SQL injection exposed 420 student exam records
2. CERT-In incident auto-created from anomaly detection
3. Countdown timer starts: 6h from detection
4. Security Engineer navigates to CERT-In Incident Log
5. Opens incident → fills report form (pre-filled from C-18 incident data)
6. Reviews: affected systems · attack vector · data type · count (420 records)
7. Downloads PDF report
8. Submits to CERT-In portal (external) → enters acknowledgement number
9. Marks as "Submitted" in platform → countdown stops
10. DPDPA assessment: exam results not PII — no DPB notification needed

### Flow C — CVE Triage

1. Weekly CI/CD run detects: new CVE-2025-12345 in `cryptography` package (CVSS 9.8)
2. CVE Tracker: new critical CVE in red
3. Security Engineer reviews: auth-service uses `cryptography` for JWT signing
4. Risk: CVE allows private key extraction → JWT forgery risk
5. Security Engineer creates fix ticket → assigns to Backend Engineer
6. Target fix date: 3 days (critical SLA)
7. CI/CD (C-09) deploys fix → CVE marked as "Fixed" with PR link as evidence
8. Security posture score improves +8 points

---

## 6. Component Structure (Logical)

```
SecurityOpsDashboardPage
├── PageHeader
│   ├── SecurityPostureScore (gauge)
│   ├── ActiveAlertsBanner
│   ├── PageTitle
│   └── CreateIncidentButton
├── KPIStrip × 6
├── WAFRulesPanel
│   ├── WAFRulesTable (priority order)
│   ├── IPBlockList
│   └── WAFMetricsCharts
├── FailedAuthHeatmap
│   ├── HeatmapVisualization (IP/country/tenant/time views)
│   ├── TopOffendersTable
│   └── PatternDetectionBanner
├── AccountLockoutLog
├── JWTAnomalyDetection
│   ├── AnomalyEventsTable
│   └── AutoResponseConfig
├── CVETracker
│   ├── CVESummaryCards × 4
│   ├── CVEDetailsTable
│   └── DependencyScannerPanel
├── CERTInIncidentLog
│   ├── ActiveCountdownTimers
│   ├── IncidentTable
│   └── ReportSubmissionModal
├── DPDPABreachTracker
│   ├── ActiveBreachCountdown
│   └── BreachRecordTable
├── VAPTResultsPanel
│   ├── EngagementHistory
│   └── OpenFindingsTable
└── ActiveThreatAlerts
```

---

## 7. Data Model (High-Level)

### platform_security_incidents

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| incident_type | ENUM | data_breach/auth_attack/ddos/malware/jwt_anomaly/vapt_finding |
| severity | ENUM | p0/p1/p2/p3 |
| title | VARCHAR(200) | |
| description | TEXT | |
| detected_at | TIMESTAMPTZ | |
| certIn_required | BOOLEAN | |
| certIn_submitted_at | TIMESTAMPTZ | nullable |
| certIn_ack_number | VARCHAR(50) | nullable |
| certIn_deadline | TIMESTAMPTZ | computed: detected_at + 6h |
| dpdpa_required | BOOLEAN | |
| dpdpa_submitted_at | TIMESTAMPTZ | nullable |
| dpdpa_deadline | TIMESTAMPTZ | computed: detected_at + 72h |
| status | ENUM | active/contained/resolved/reported |
| resolved_at | TIMESTAMPTZ | nullable |
| resolved_by | UUID FK → platform_staff | nullable |

### platform_cve_registry

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| cve_id | VARCHAR(30) | e.g., CVE-2025-12345 |
| severity | ENUM | critical/high/medium/low |
| cvss_score | DECIMAL(3,1) | |
| package_name | VARCHAR(100) | |
| affected_version | VARCHAR(50) | |
| fixed_version | VARCHAR(50) | nullable |
| affected_services | JSONB | array of service names |
| status | ENUM | new/triaged/in_progress/fixed/accepted_risk |
| accepted_risk_reason | TEXT | nullable |
| accepted_risk_expires_at | DATE | nullable |
| assigned_to | UUID FK → platform_staff | nullable |
| fix_deadline | DATE | nullable |
| fix_pr_url | VARCHAR(512) | nullable |
| first_detected_at | TIMESTAMPTZ | |
| fixed_at | TIMESTAMPTZ | nullable |

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| WAF rule priority | Must be unique per WebACL; system auto-adjusts conflicts |
| Block /24 subnet | 2FA required · max CIDR: /16 (cannot block entire ISP) |
| Accept CVE risk (critical) | Requires Platform Admin co-approval · justification min 100 chars · max acceptance period: 30 days |
| CERT-In report | Must submit within 6h of breach detection; overdue triggers escalation email to CTO |
| DPDPA notification | Must submit within 72h; overdue triggers legal team notification |
| JWT deny-list | Token revocation entries stored in `platform_jwt_denied_tokens` ORM table with `expires_at` set to 15 days (longer than any valid JWT lifespan); Celery nightly task deletes expired rows |
| VAPT finding close | Requires evidence attachment (PR link / test result) before marking as Fixed |
| IP block permanent | Admin + Security only · 2FA · reason required |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| WAF WAFV2 API | Server-side only; `wafv2:UpdateWebACL` scoped to platform WebACL ARN; cannot modify other WAF resources |
| CERT-In report data | Contains breach details; access restricted to Security Engineer + Platform Admin; not visible to other roles |
| Account lockout details | Student emails masked in UI (`jo**@gmail.com`); full email visible in audit log (Security/Admin only) |
| JWT anomaly data | `jti` values logged; actual JWT signatures never exposed; payload decoded server-side only |
| CVE data | pip-audit results stored in S3 encrypted; only summary shown in UI; full report downloadable by Security/Admin |
| This page itself | Security Ops page behind Level 4 auth; no public routes; 2FA re-challenge after 15 min idle |
| VAPT reproduction steps | Masked/redacted for external-vendor findings; shown only to Security Engineer after "view sensitive details" 2FA challenge |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| Multiple CERT-In incidents open simultaneously | Each has independent countdown; most urgent shown first; "3 incidents open — 2 overdue" escalation |
| CERT-In portal (external) unavailable at deadline | System recommends email submission as fallback; email template auto-generated with all required fields |
| WAF rule conflicts (same path in multiple rules) | AWS WAF evaluates in priority order; system warns if conflicting rules detected: "Rule #3 and Rule #7 both match /api/exams/*. Rule #3 will take precedence." |
| False positive CVE (package version incorrect in dependency graph) | "Mark as false positive" option; Security Engineer provides reason; excluded from future scans until acknowledged |
| Mass lockout event (exam day network issue) | Mass unlock available; Security Engineer must review pattern first to confirm it's not a real attack |
| DPDPA breach involving minors (school students < 18) | Separate "Data Principal: Minor" flag; parental guardian notification also required; system prompts Security Engineer to add guardian contact details to breach report |
| Security incident during CERT-In reporting window | C-18 incident linked to CERT-In record; any updates to incident status auto-update CERT-In report draft |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| Failed auth aggregation | CloudWatch Logs Insights query aggregated every 15 min by Celery; UI shows last-computed result (not real-time) + live event stream (last 100 events) |
| WAF metrics | CloudWatch WAF namespace; batched with other CloudWatch calls; 5-min cache |
| JWT anomaly detection | Lambda middleware writes anomaly events to SQS; Celery consumer processes and writes to DB; 30s processing lag acceptable |
| Heatmap rendering | Pre-aggregated buckets (15-min × IP/country/tenant) stored in `platform_failed_auth_stats` ORM table; heatmap rendered server-side as SVG; no D3 in browser |
| CVE database | pip-audit + Snyk run in CI/CD (not on this page); results webhook into platform; page reads from DB; no on-demand scanning except "Run scan" button |
| CERT-In/DPDPA countdowns | Client-side countdown (JS) seeded from server-provided `deadline_at` timestamp; no server polling for countdown itself |
| Security posture score | Computed by Celery beat every hour; stored in Memcached (1h TTL); page load reads from cache < 5ms |

---

## 12. Amendment — G6: VAPT Schedule Tab

**Assigned gap:** G6 — VAPT scheduling and vendor management is missing; C-13 shows VAPT results but the Security Engineer cannot schedule engagements, track scope, or log vendor communications.

**Where it lives:** New tab added to the VAPT Results Panel (Section 10). The panel gets two tabs: **Findings** (existing) and **Schedule** (new, described here).

---

### VAPT Schedule Tab

**Purpose:** Allow the Security Engineer to plan and manage VAPT engagements end-to-end — from scheduling the engagement and defining scope, to tracking vendor communications and closing the engagement when all findings are remediated. This ensures the platform always has an up-to-date, documented VAPT programme rather than ad-hoc one-off assessments.

**Layout:** Three panels — Upcoming Engagements · Engagement Detail Drawer · Vendor Directory

---

**Panel 1 — Engagement Calendar & List**

A combined list + mini-calendar showing all past, active, and upcoming VAPT engagements. Each engagement card shows:

- Engagement name (e.g., "Annual VAPT 2026 — External")
- Vendor name + contact
- Type: External VAPT · Internal Red Team · Bug Bounty · Automated (OWASP ZAP) · Cloud Config Review
- Scope summary: "Web application — all public endpoints + /engineering/* internal routes"
- Date range: start → end (or recurring for automated scans)
- Status: Scheduled · In Progress · Findings Review · Remediation · Closed
- Open findings count badge (links to Findings tab filtered by this engagement)
- Next milestone: "Kickoff call: 2026-04-01 09:00 IST"

**Actions:**
- "New Engagement" button → vapt-schedule-drawer (see below)
- "View details" → vapt-schedule-drawer opens for existing engagement
- Status filter: All / Upcoming / In Progress / Remediation / Closed

---

**vapt-schedule-drawer (720px)**

Tabs: **Details · Scope · Communications · Milestones**

**Tab 1 — Details:**
- Engagement name (text input)
- Type selector (dropdown)
- Vendor: select from vendor directory or add new
- Lead contact at vendor: name + email
- Internal owner: select from platform staff (Security Engineer / Admin)
- Date range: start date + end date
- Cost (₹): budgeted + actual (actual filled after close)
- Status: managed via milestones (auto-advances)
- Notes: free-text textarea

**Tab 2 — Scope:**
- Scope definition: checklist + free text
  - Public web app endpoints (/api/*)
  - Internal engineering routes (/engineering/*)
  - Mobile apps (iOS + Android)
  - Cloud infrastructure (AWS: RDS, ECS, Lambda, S3, WAF)
  - CI/CD pipeline (GitHub Actions)
  - Third-party integrations (Razorpay, Firebase, SES)
- Out-of-scope exclusions: free text (e.g., "student data — no live data access; use anonymised staging only")
- Data sensitivity note: required field — describes what data vendor may encounter and what access controls are in place
- NDA signed: checkbox + upload NDA document (stored in S3)
- Rules of engagement: agreed testing window hours, notification contacts for emergencies during testing

**Tab 3 — Communications:**
- Log of all communications with the vendor during the engagement:
  - Each entry: timestamp · direction (inbound/outbound) · channel (email/call/Slack) · summary · attachments
  - "Add communication log" → inline form
  - Upload: vendor scope confirmation · interim report · final report · remediation verification letter
- Documents uploaded are stored in S3 (encrypted); displayed as download links with uploaded-by and timestamp

**Tab 4 — Milestones:**
- Pre-defined milestone sequence per engagement type:
  - External VAPT: Contract signed → NDA signed → Kickoff call → Testing in progress → Draft report received → Findings reviewed → Remediation started → Re-test → Closed
  - Automated scan: Scheduled → Running → Results imported → Findings reviewed → Closed
- Each milestone: checkbox (mark complete) + completion date + notes
- Completion of all milestones auto-sets engagement status to "Closed"
- Overdue milestones (target date passed, not complete): highlighted amber

**Data model:**

**platform_vapt_engagements**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| name | VARCHAR(200) | |
| type | ENUM | external/internal_red_team/bug_bounty/automated/cloud_config |
| vendor_id | UUID FK → platform_vapt_vendors | nullable (automated = null) |
| internal_owner_id | UUID FK → platform_staff | |
| status | ENUM | scheduled/in_progress/findings_review/remediation/closed |
| start_date | DATE | |
| end_date | DATE | nullable |
| scope_definition | JSONB | scope checklist + free text |
| cost_budgeted | DECIMAL | nullable |
| cost_actual | DECIMAL | nullable |
| nda_s3_key | VARCHAR(512) | nullable |
| created_at | TIMESTAMPTZ | |
| created_by | UUID FK → platform_staff | |

---

## 13. Amendment — G16: Data Localization Audit Tab

**Assigned gap:** G16 — No dashboard verifies that all student PII (S3 buckets, RDS, Lambda environments, CloudFront origins) remains within ap-south-1 (Mumbai). A DPDPA 2023 violation would go undetected until an external audit or breach.

**Where it lives:** New standalone tab in the Security Operations Dashboard page header tab bar. The page gains a top-level tab strip: **Overview** (all existing sections) · **Data Localization** (new) · **CERT-In Report** (G17) · **Security Audit Log** (G24).

---

### Data Localization Audit Tab

**Purpose:** Continuously verify that all AWS resources holding student PII are located in ap-south-1 (Mumbai) as required by DPDPA 2023. Surface any drift — a new S3 bucket created in us-east-1, a Lambda environment variable referencing a cross-region resource — before it becomes a compliance violation.

**Compliance header:**

A summary banner showing overall data localization status:
- Green: "All PII resources confirmed in ap-south-1 ✅ — Last audited: 2h ago"
- Amber: "1 resource flagged for review — non-PII resource in us-east-1 (CloudFront distribution)"
- Red: "⚠ DPDPA VIOLATION RISK: PII resource detected outside ap-south-1. Immediate action required."

Last audit run timestamp + "Run audit now" button (triggers on-demand Celery task; takes 5–10 min).

---

**Resource Audit Table:**

Rows are AWS resources; columns indicate localization status:

| Resource Type | Resource Name / ARN | Region | PII Classification | Status | Last Checked |
|---|---|---|---|---|---|
| RDS — Primary | platform-rds-primary | ap-south-1 | PII (student data, exam results) | ✅ Compliant | 2h ago |
| RDS — Replica 1 | platform-rds-replica-1 | ap-south-1 | PII | ✅ Compliant | 2h ago |
| RDS — Replica 2 | platform-rds-replica-2 | ap-south-1 | PII | ✅ Compliant | 2h ago |
| S3 — Student uploads | platform-student-uploads | ap-south-1 | PII (question images, answer sheets) | ✅ Compliant | 2h ago |
| S3 — Audit logs | platform-audit-logs | ap-south-1 | PII (audit trail of student actions) | ✅ Compliant | 2h ago |
| S3 — CDN assets | platform-cdn-assets | us-east-1 | Non-PII (static JS/CSS) | ✅ Exempt (CDN assets — no PII) | 2h ago |
| Lambda — auth-service | auth-service-prod | ap-south-1 | PII-processing | ✅ Compliant | 2h ago |
| Lambda — exam-service | exam-service-prod | ap-south-1 | PII-processing | ✅ Compliant | 2h ago |
| ElastiCache — Memcached | platform-cache | ap-south-1 | Non-PII (transient cache) | ✅ Compliant | 2h ago |
| SES — Email sending | SES identity | ap-south-1 | PII (student email addresses used) | ✅ Compliant | 2h ago |
| S3 Glacier — Archive | platform-archive | ap-south-1 | PII (archived exam data) | ✅ Compliant | 2h ago |

**PII Classification rules** (used by the audit Celery task):
- PII: any resource storing or processing student name · email · phone · exam results · payment data · login history
- PII-processing: any compute resource (Lambda, ECS) that handles PII in transit (even if no storage)
- Non-PII: static assets, CI/CD artifacts, build caches (no student data)
- Exempt: CloudFront distributions (edge by design) and CDN asset S3 buckets (no PII)

**Filter:** All / PII only / PII-processing only / Non-compliant only

**Audit detail drawer (localization-audit-drawer):**
- Per-resource: full ARN · creation date · encryption status (KMS key region verified) · cross-region replication status (if any) · last-modified date
- For flagged resources: specific violation detail + recommended remediation action

**Cross-region replication check:**
S3 cross-region replication is separately verified: any S3 bucket with CRR enabled that replicates PII to a non-ap-south-1 region is flagged as a violation even if the source bucket is in ap-south-1.

**Environment variable scan:**
Lambda environment variables are scanned for cross-region ARN references (e.g., an RDS endpoint in eu-west-1). Any PII-processing Lambda with a cross-region dependency is flagged.

**Audit schedule:** Celery beat runs the full audit every 6 hours. Results written to `platform_data_localization_audit` table. On any new violation detected: security incident auto-created in C-18 + security-alert Slack notification to Security Engineer.

**Data model:**

**platform_data_localization_audit**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| resource_arn | VARCHAR(512) | |
| resource_type | VARCHAR(100) | rds/s3/lambda/elasticache/ses/glacier |
| resource_name | VARCHAR(200) | |
| region | VARCHAR(50) | |
| pii_classification | ENUM | pii/pii_processing/non_pii/exempt |
| is_compliant | BOOLEAN | |
| violation_detail | TEXT | nullable |
| audited_at | TIMESTAMPTZ | |
| run_id | UUID | groups all resources in one audit run |

---

## 14. Amendment — G17: CERT-In Report Tab

**Assigned gap:** G17 — Security Engineer must file CERT-In 6-hour incident reports but has no structured template or generator. Reports are drafted manually under time pressure, risking non-compliance with the statutory 6-hour deadline.

**Where it lives:** New top-level tab in the Security Operations Dashboard (alongside Data Localization, described in G16).

---

### CERT-In Report Tab

**Purpose:** Generate structured, CERT-In-compliant incident reports from existing incident data in the platform. Remove the manual drafting burden so the Security Engineer can focus on response rather than paperwork, while ensuring the statutory 6-hour deadline is never missed.

**Layout:** Two panels — Active Report Queue · Completed Reports Archive

---

**Panel 1 — Active Report Queue**

All security incidents that require CERT-In reporting but have not yet been submitted, sorted by deadline (most urgent first).

**Incident card (per incident):**

- Incident title and severity
- Detected at timestamp
- Countdown timer (large, colour-coded): "Report in 4h 22m 08s" → amber at 2h → red at 1h → pulsing "OVERDUE" if past deadline
- Report status: Not started · Draft in progress · Ready to submit · Submitted
- "Generate Report" / "Edit Draft" / "Submit" button based on status

---

**Report Generator (cert-in-report-drawer, 800px)**

Opens on "Generate Report". Pulls data from the linked C-18 incident record and pre-fills all CERT-In mandatory fields.

**Pre-filled from C-18 incident:**
- Incident reference number (platform internal ID)
- Date and time of detection
- Date and time of first evidence (if earlier than detection)
- Affected systems (from C-18 affected services list)
- Attack timeline (from C-18 event log)

**Fields the Security Engineer must complete or verify:**

Section A — Incident Identification:
- Official incident name (as it will appear in the CERT-In report — editable text)
- CERT-In incident category: select from dropdown (Phishing / Compromise of Critical Systems / Data Breach / Ransomware / DDoS / Malware / Brute Force / SQL Injection / Other — per CERT-In 2022 guidelines)
- Date/time of first occurrence (may differ from detection)
- Date/time organisation became aware

Section B — Technical Details:
- Attack vector: select (Network / Email / Web application / Insider / Unknown)
- Indicators of compromise (IOCs): text area for IP addresses, domains, hashes detected
- Affected systems: pre-filled from C-18 — editable list of services/servers
- Data types potentially compromised: checkboxes (Student PII / Exam data / Payment data / Staff credentials / System configuration / None — under investigation)
- Estimated number of affected data principals (individuals)
- Whether attacker had persistence: Yes / No / Unknown

Section C — Impact Assessment:
- Was student exam continuity affected: Yes / No
- Estimated financial impact: optional
- Is the incident ongoing or contained: Ongoing / Contained / Unknown

Section D — Actions Taken:
- Immediate response actions (pre-filled from C-18 timeline): editable
- Containment measures applied
- Whether law enforcement has been notified: Yes / No / In progress

Section E — Organisation Details (pre-filled from platform config — not editable in report):
- Organisation name
- CIN / PAN
- Sector: EdTech
- SPOC (Single Point of Contact): name + email + phone (from platform_system_config)
- Reporting officer designation

**Validation:** All mandatory CERT-In fields must be filled before enabling "Generate PDF". Optional fields flagged with "(optional)" label.

**Generate PDF:**
- Produces a formatted PDF matching CERT-In's standard incident report template
- PDF preview shown in drawer before download
- "Download PDF" button
- PDF stored in S3 (encrypted); accessible from Completed Reports Archive

**Submit workflow:**
- "Mark as submitted to CERT-In" → modal: enter CERT-In acknowledgement number + submission timestamp + submission channel (CERT-In portal / email at incident@cert-in.org.in)
- On submit: incident record updated; countdown timer stopped; security incident in C-18 updated with "CERT-In reported" status
- If submitted past deadline: system records the delay + reason (for internal audit trail)

**DPO Notification (if DPDPA-applicable):**
- If incident is flagged as a DPDPA data breach (set in C-18): a second "Generate DPB Notification" button appears
- Same workflow but uses Data Protection Board notification template (72h deadline)
- DPO email generated with statutory language pre-filled

---

**Panel 2 — Completed Reports Archive**

Table of all submitted and closed CERT-In reports:

| Incident | Reported By | Submitted At | Within Deadline | Ack Number | CERT-In Category | PDF |
|---|---|---|---|---|---|---|
| Credential stuffing — 842 accounts | Arjun (Security) | 4h after detection | ✅ Yes (within 6h) | CERT-IN-2026-04782 | Brute Force | Download |
| API data exposure — tenant_042 | Arjun (Security) | 7h after detection | ❌ No (1h overdue) | CERT-IN-2026-03291 | Data Breach | Download |

Overdue submissions permanently flagged in archive (non-editable after close — audit trail).

---

## 15. Amendment — G24: Security Audit Log Tab

**Assigned gap:** G24 — No dedicated, append-only security audit trail for WAF rule changes, secret view events, 2FA bypass events, OAuth app registrations, and permission escalations. External auditors have no single source of truth.

**Where it lives:** New top-level tab in the Security Operations Dashboard (alongside Data Localization and CERT-In Report).

---

### Security Audit Log Tab

**Purpose:** Provide an append-only, tamper-evident log of all security-relevant actions taken within the platform — covering WAF changes, secrets access, 2FA events, access level changes, and escalation triggers. This log is the primary evidence artefact for external security audits and CERT-In/DPDPA investigations.

**Immutability guarantee:** Entries in `platform_security_audit_log` are never updated or deleted by the application layer. The table has a `CHECK` constraint rejecting UPDATE and DELETE at the database role level used by the platform. The DBA superuser role can delete rows but this action itself is captured by PostgreSQL audit logging. Entries older than 7 years are archived to S3 Glacier (WORM Object Lock) before deletion.

---

**Audit Log Table:**

| Column | Description |
|---|---|
| Timestamp | UTC timestamp (precision: millisecond) |
| Actor | Staff name + role + email |
| Event Type | Category (see event type taxonomy below) |
| Action | Specific action taken |
| Target | What was affected (resource name / user / IP / rule ID) |
| IP Address | Actor's source IP |
| Result | Success · Failure · Blocked |
| Detail | JSON payload expandable on row click |

**Event Type Taxonomy:**

| Category | Events Captured |
|---|---|
| WAF | Rule added · Rule modified · Rule deleted · IP block added · IP block removed · Rule reorder |
| Secrets | Secret viewed (masked — view event only, not value) · Secret rotated · Secret created · Secret deleted · Secret ARN retrieved |
| Authentication | 2FA bypass used · 2FA code failure (staff) · Emergency access activated · Session terminated by admin |
| Access Control | Role assigned · Role revoked · Access level changed · Permission override applied |
| OAuth | OAuth app registered · OAuth app secret rotated · OAuth app deleted · Scope granted |
| JWT | Token manually revoked · Deny-list entry added · JWT anomaly action taken |
| Escalation | Escalation chain triggered · OOO toggle set · Test alert sent · Escalation acknowledged |
| CERT-In / DPDPA | Incident created · Report generated · Report submitted · DPB notification sent |
| Data Localization | Audit run triggered · Violation flagged · Violation resolved |
| Platform Config | System config changed · Maintenance mode toggled · Feature flag changed |

**Filtering:**
- Event category (multi-select)
- Actor (staff name or role search)
- Date range (from/to — exact timestamps)
- Result: All / Success / Failure / Blocked
- Target: free text search (e.g., WAF rule name, secret ARN)
- Free-text search across Action and Detail fields

**Export:**
- "Export to CSV" — filtered results exported to S3 and download link returned (large exports async via Celery)
- "Export to PDF" — formatted audit report for external auditors: date range header, filtered events, platform name, exported-by name and timestamp, SHA-256 hash of export for integrity verification

**Immutability indicators:**
- "Append-only" badge on the tab
- Footer: "This log is append-only. No entry can be modified or deleted by any application-layer action. Entries are retained for 7 years per CERT-In and IT Act requirements."
- Each row has a row-level SHA-256 hash (computed at insert time from: timestamp + actor_id + event_type + action + target + result) — displayed on row expand; auditors can re-verify hash against exported data

**Integration points:**
- WAF rule changes in Section 3 → written here automatically
- Secret view in C-14 → written here automatically
- 2FA events in C-02 staff auth → written here automatically
- Role/permission changes in C-02 → written here automatically
- Escalation triggers in C-02 G30 → written here automatically
- JWT revocation in Section 6 → written here automatically

**Data model:**

**platform_security_audit_log**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| timestamp | TIMESTAMPTZ | millisecond precision; set by DB trigger (not application) |
| actor_id | UUID FK → platform_staff | nullable for system-initiated events |
| actor_role | SMALLINT | role at time of action (denormalised — role may change later) |
| actor_ip | INET | |
| event_category | VARCHAR(50) | waf/secrets/authentication/access_control/oauth/jwt/escalation/certIn/data_localization/platform_config |
| event_type | VARCHAR(100) | specific event name |
| action | TEXT | human-readable action description |
| target | VARCHAR(512) | resource identifier |
| result | ENUM | success/failure/blocked |
| detail | JSONB | full event payload (never contains secret values) |
| row_hash | CHAR(64) | SHA-256 of (timestamp + actor_id + event_type + action + target + result) — computed at insert |
