# 41 — Security Posture

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Security Posture |
| Route | `/exec/security-posture/` |
| Django view | `SecurityPostureView` |
| Template | `exec/security_posture.html` |
| Priority | **P2** |
| Nav group | Engineering |
| Required roles | `cto` · `security_engineer` · `ceo` · `superadmin` |
| COO / CFO / Others | Denied |
| HTMX poll — cert expiry + CVEs | Every 3600s (1 hour) |
| Cache | Redis TTL 3590s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · danger `#EF4444` · warn `#F59E0B` · success `#22C55E` |

---

## 2. Purpose & Business Logic

**Why a dedicated security posture page:**

At 2.5M+ students and Rs.60 Cr ARR, EduForge is a high-value target:
- Student PII (Aadhaar-linked, DPDP Act 2023 applies)
- Exam content (paper leak = catastrophic reputational damage)
- Payment data (Razorpay integration)
- BGV data (sensitive staff records)

The CTO and Security Engineer need a single page that answers:
- Are all SSL certs valid and not expiring in the next 30 days?
- Are KMS keys being rotated on schedule?
- What open CVEs exist in our dependencies — what's the CVSS score?
- When was the last penetration test, and are all critical findings closed?
- Is our WAF covering all production endpoints?
- Are we DPDP Act 2023 compliant on data residency and consent?

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All sections (read-only) | None |
| CTO | All sections | Acknowledge CVE, mark pen test finding closed, rotate KMS key |
| Security Engineer | All sections | All security actions |
| Others | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Security Summary Strip

```
╔══════════════╦══════════════╦══════════════╦══════════════╦══════════════╗
║ SECURITY     ║ SSL CERTS    ║ OPEN CVEs    ║ PEN TEST     ║ WAF          ║
║ SCORE        ║ EXPIRING     ║              ║ FINDINGS     ║ COVERAGE     ║
║    84/100    ║  2 (< 30d)   ║  3 High      ║  1 Critical  ║   96.2%      ║
║  ▼ was 88   ║  ⚠ Review    ║  8 Medium    ║  2 High open ║  ● OK        ║
╚══════════════╩══════════════╩══════════════╩══════════════╩══════════════╝
```

**Security score (0–100) computed from:**
- SSL cert health (20%)
- KMS rotation compliance (15%)
- CVE severity (25%)
- Pen test finding closure rate (20%)
- WAF coverage (10%)
- DPDP compliance (10%)

Score drop > 5 pts: CTO email notification. Score < 70: P2 incident created.

---

### Section 2 — SSL Certificate Tracker

```
SSL CERTIFICATE TRACKER
─────────────────────────────────────────────────────────────────────────────
Domain                      Issuer        Expires        Days Left  Status
─────────────────────────────────────────────────────────────────────────────
*.eduforge.in               Let's Encrypt  15 Apr 2026      26d     ⚠ Expiring
api.eduforge.in             Let's Encrypt  15 Apr 2026      26d     ⚠ Expiring
portal.eduforge.in          Let's Encrypt  12 Jul 2026     114d     ✅ OK
cdn.eduforge.in             AWS ACM        Auto-renew       —       ✅ Managed
```

- < 30 days: amber ⚠
- < 7 days: red 🔴 + auto-creates P1 incident
- "Auto-renew" (ACM/Let's Encrypt with certbot): shows "Managed" in green
- Manual renewal certs: show days countdown
- Click row → drawer with cert details: SANs, issuer chain, fingerprint, renewal steps

**HTMX:** `id="ssl-tracker"` `hx-trigger="load, every 3600s"` — Celery beat checks cert expiry daily via `ssl` Python module.

---

### Section 3 — KMS Key Rotation Schedule

```
KMS KEY ROTATION
─────────────────────────────────────────────────────────────────────────────
Key Alias              Purpose             Last Rotated   Next Rotation  Status
─────────────────────────────────────────────────────────────────────────────
alias/eduforge-jwt     JWT signing         15 Jan 2026    15 Apr 2026    ✅ OK
alias/eduforge-db      DB encryption       10 Feb 2026    10 May 2026    ✅ OK
alias/eduforge-bgv     BGV data encryption  1 Mar 2026     1 Jun 2026    ✅ OK
alias/eduforge-exam    Exam content encrypt 14 Oct 2025   14 Jan 2026    🔴 OVERDUE
```

- Rotation schedule: 90 days (configurable per key)
- Overdue: red + auto-creates P1 incident + CTO email alert
- [Rotate Now] button (CTO/Security Engineer): POST `/exec/security-posture/actions/rotate-kms/` → boto3 `enable_key_rotation()` + audit log

---

### Section 4 — CVE Tracker

**Purpose:** Open CVEs in EduForge's dependency stack. Sourced from automated dependency scan (GitHub Dependabot or OWASP Dependency-Check, results pushed to `CVERecord` model via webhook).

```
OPEN CVEs                                  [Severity: All ▾] [Acknowledged: No ▾]
─────────────────────────────────────────────────────────────────────────────
CVE ID          Package          CVSS  Severity  Affected Service  Acknowledged
────────────────┼─────────────────┼──────┼──────────┼──────────────────┼─────────
CVE-2026-12481  pillow 9.4.0     9.8   Critical  File Storage      No     [Ack]
CVE-2026-09142  cryptography 41  7.5   High      Auth Service      No     [Ack]
CVE-2025-88421  django 4.2.8     6.1   Medium    All services      Yes    —
```

- Critical (CVSS > 9): red row + `animate-pulse` border + auto-created P1 incident if not acknowledged within 24h
- "Ack" button: opens modal: acknowledge reason + target fix date + assignee
- Click row → CVE detail drawer: description, affected endpoints, recommended fix, NVD link

---

### Section 5 — Pen Test Findings

```
PEN TEST FINDINGS
─────────────────────────────────────────────────────────────────────────────
Last test: 15 Jan 2026 (by: Appsecco Security)  Next test: 15 Jul 2026
─────────────────────────────────────────────────────────────────────────────
Finding                        Severity  Status       Due Date    Owner
───────────────────────────────┼──────────┼─────────────┼────────────┼───────
Insecure direct object ref.   Critical  🔴 Open       15 Apr 2026  Priya M.
Missing rate limit on OTP     High      🟡 In Progress 1 May 2026   Rahul G.
Verbose error messages        High      🟡 In Progress 1 May 2026   Kiran S.
Outdated TLS 1.0 on CDN       Medium    ✅ Closed      12 Mar 2026  —
```

- Critical open findings: `border-l-4 border-red-500` + included in security score deduction
- [Mark Closed] action (CTO/Security Engineer): requires resolution description + CTO acknowledgment
- Next test date: amber if < 90 days until next test and findings still open

---

### Section 6 — WAF Coverage Map

```
WAF (AWS WAF) COVERAGE                              96.2% endpoints covered
─────────────────────────────────────────────────────────────────────────────
Endpoint Group           Total   WAF Protected  Gap
─────────────────────────┼────────┼──────────────┼────────────────────────────
Exam submission APIs     24      24             ✅ 100%
Auth / OTP APIs          12      12             ✅ 100%
Institution portal APIs  180     168            ⚠ 12 unprotected [Review →]
Admin/exec APIs          48      48             ✅ 100%
Static asset endpoints   62      62             ✅ 100%
```

- Unprotected endpoints: amber + count. Click → drill-down list of unprotected paths
- WAF rules summary: "SQL injection: ✅ · XSS: ✅ · Rate limiting: ✅ · Geo-block: ✅ · Bot control: ✅"

---

### Section 7 — DPDP Act 2023 Compliance Checklist

```
DPDP ACT 2023 COMPLIANCE
─────────────────────────────────────────────────────────────────────────────
Requirement                                    Status      Last Verified
─────────────────────────────────────────────────────────────────────────────
Consent notices in place (all 2,050 inst.)    ✅ Complete   15 Mar 2026
Data Principal Rights mechanism (erasure)     ✅ Complete   10 Mar 2026
Data Fiduciary registration with DPB          ⚠ Pending    —
72-hour breach notification process           ✅ Complete   20 Jan 2026
Data Localization (ap-south-1 only)           ✅ Complete   —
Cross-border transfer contracts               🔴 Incomplete  —
Annual data audit completion                  ✅ Complete   1 Feb 2026
```

- Each item: toggle "Mark Verified" (Security Engineer/CTO) with date picker + evidence upload
- Red / ⚠ items: included in security score deduction
- Auto-creates `ComplianceAlert` if `status='incomplete'` for critical items

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Security Posture                                     [↺ Refresh]           ║
╠══════════╦══════════╦══════════╦══════════╦══════════════════════════════════╣
║ SCORE    ║ SSL CERTS║ CVEs     ║ PEN TEST ║ WAF COVERAGE                    ║
║  84/100  ║  2 (30d) ║ 3 High   ║ 1 Crit   ║  96.2%                          ║
╠══════════╩══════════╩══════════╩══════════╩══════════════════════════════════╣
║  SSL CERTS                     KMS KEY ROTATION                             ║
║  *.eduforge.in   26d ⚠          JWT key    → 15 Apr 2026 ✅                  ║
║  portal.         114d ✅          Exam key   → 14 Jan 2026 🔴 OVERDUE         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  CVE TRACKER                   PEN TEST FINDINGS                            ║
║  CVE-2026-12481 CVSS 9.8 🔴     Insecure IDOR    Critical 🔴 Open            ║
║  CVE-2026-09142 CVSS 7.5 High   Missing OTP RL   High    🟡 In Progress     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  WAF COVERAGE — 96.2%           DPDP ACT 2023                               ║
║  Institution APIs: 12 uncovered  DPB Registration: ⚠ Pending               ║
║  All exam APIs: ✅ 100%           Cross-border transfers: 🔴 Incomplete       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `SecurityScoreCard` | `components/security/score_card.html` | `score, prev_score, dimension_breakdown` |
| `SSLCertRow` | `components/security/ssl_row.html` | `domain, issuer, expires_date, days_left, is_managed` |
| `KMSKeyRow` | `components/security/kms_row.html` | `alias, purpose, last_rotated, next_rotation, is_overdue, can_rotate` |
| `CVERow` | `components/security/cve_row.html` | `cve_id, package, cvss, severity, service, acknowledged, can_ack` |
| `PenTestFindingRow` | `components/security/pentest_row.html` | `finding, severity, status, due_date, owner, can_close` |
| `WAFCoverageRow` | `components/security/waf_row.html` | `endpoint_group, total, protected, gap_count` |
| `DPDPChecklistRow` | `components/security/dpdp_row.html` | `requirement, status, last_verified, can_mark` |

---

## 7. HTMX Architecture

| `?part=` | Target | Poll | Trigger |
|---|---|---|---|
| `summary` | `#security-summary` | 3600s | load |
| `ssl` | `#ssl-tracker` | 3600s | load |
| `kms` | `#kms-rotation` | 3600s | load |
| `cves` | `#cve-tracker` | 3600s | load + filter |
| `pentest` | `#pentest-findings` | None | load |
| `waf` | `#waf-coverage` | 3600s | load |
| `dpdp` | `#dpdp-checklist` | None | load |

---

## 8. Backend View & API

```python
class SecurityPostureView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_security_posture"

    def get(self, request):
        allowed = {"cto","security_engineer","ceo","superadmin"}
        if request.user.role not in allowed:
            return redirect("exec:dashboard")
        can_act = request.user.role in {"cto","security_engineer","superadmin"}

        if _is_htmx(request):
            part = request.GET.get("part","")
            ctx = {"can_act": can_act}
            dispatch = {
                "summary": "exec/security/partials/summary.html",
                "ssl":     "exec/security/partials/ssl.html",
                "kms":     "exec/security/partials/kms.html",
                "cves":    "exec/security/partials/cves.html",
                "pentest": "exec/security/partials/pentest.html",
                "waf":     "exec/security/partials/waf.html",
                "dpdp":    "exec/security/partials/dpdp.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "exec/security_posture.html", {"can_act": can_act})
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/security-posture/actions/rotate-kms/` | `portal.rotate_kms` | boto3 `enable_key_rotation()`, audit log |
| POST | `/exec/security-posture/actions/acknowledge-cve/` | `portal.manage_security` | Update `CVERecord.acknowledged=True`, set fix date + assignee |
| POST | `/exec/security-posture/actions/close-finding/` | `portal.manage_security` | Update `PenTestFinding.status='closed'`, require resolution description |
| POST | `/exec/security-posture/actions/mark-dpdp/` | `portal.manage_security` | Update `DPDPChecklistItem.status`, record verifier + date |

---

## 9. Database Schema

```python
class CVERecord(models.Model):
    cve_id         = models.CharField(max_length=20, unique=True)
    package        = models.CharField(max_length=100)
    cvss_score     = models.FloatField()
    severity       = models.CharField(max_length=10)  # critical/high/medium/low
    affected_service = models.CharField(max_length=100)
    description    = models.TextField()
    nvd_url        = models.URLField()
    acknowledged   = models.BooleanField(default=False)
    acknowledged_by= models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                        on_delete=models.SET_NULL)
    acknowledged_at= models.DateTimeField(null=True)
    target_fix_date= models.DateField(null=True)
    resolved_at    = models.DateTimeField(null=True)
    detected_at    = models.DateTimeField(auto_now_add=True)


class PenTestFinding(models.Model):
    test_date      = models.DateField()
    vendor         = models.CharField(max_length=100)
    title          = models.CharField(max_length=200)
    severity       = models.CharField(max_length=10)
    description    = models.TextField()
    status         = models.CharField(max_length=20, default="open",
                         choices=[("open","Open"),("in_progress","In Progress"),
                                  ("closed","Closed")])
    owner          = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                        on_delete=models.SET_NULL)
    due_date       = models.DateField()
    closed_at      = models.DateTimeField(null=True)
    resolution     = models.TextField(blank=True)


class SSLCertRecord(models.Model):
    domain         = models.CharField(max_length=200, unique=True)
    issuer         = models.CharField(max_length=100)
    expires_at     = models.DateField()
    is_managed     = models.BooleanField(default=False)
    last_checked   = models.DateTimeField(auto_now=True)


class DPDPChecklistItem(models.Model):
    requirement    = models.CharField(max_length=200)
    category       = models.CharField(max_length=50)
    status         = models.CharField(max_length=20,
                         choices=[("complete","Complete"),("pending","Pending"),
                                  ("incomplete","Incomplete")])
    last_verified  = models.DateField(null=True)
    verified_by    = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                        on_delete=models.SET_NULL)
    evidence_url   = models.URLField(blank=True)
    notes          = models.TextField(blank=True)
```

---

## 10. Validation Rules

| Action | Validation |
|---|---|
| Acknowledge CVE | Reason required (min 20 chars). Target fix date required (must be in future). Assignee required. |
| Close pen test finding | Resolution description required (min 50 chars). CTO must be the final acknowledger for Critical findings. |
| Mark DPDP item | Status must progress forward (cannot re-open closed item without reason). Evidence URL encouraged for critical items. |
| Rotate KMS key | AWS key alias must exist. Not allowed during exam peak (same lock as deployments). |

---

## 11. Security Considerations

- KMS rotation action: calls boto3 with IAM role limited to `kms:EnableKeyRotation` on specific key ARNs only
- CVE data sourced via GitHub Dependabot webhook — HMAC-validated before processing
- All security actions are double-logged: `AuditLog` (general) + `SecurityAuditLog` (security-specific, immutable, fed to SIEM)
- Page itself protected by 2FA gate: if CTO/Security Engineer does not have 2FA active, redirected to 2FA setup before viewing

---

## 12. Edge Cases

| State | Behaviour |
|---|---|
| Critical CVE unacknowledged > 24h | Auto-creates P1 incident, CTO and Security Engineer paged via PagerDuty |
| SSL cert expires within 7 days | P1 incident auto-created. "CERT EXPIRY IMMINENT" banner above page. |
| KMS key overdue for rotation | P1 incident auto-created on next Celery daily check |
| Pen test overdue (> 6 months since last) | Security score drops by 15 pts. COO (not CTO) notified — scheduling a pen test is a management decision |
| DPDP critical item "incomplete" | `ComplianceAlert` created. Legal Officer + COO + CTO notified. |

---

## 13. Performance & Scaling

- All data is infrequently changing (certs, CVEs, pen test findings) — 1-hour Redis TTL is appropriate
- Celery beat tasks:
  - Daily at 03:00 IST: `check_ssl_expiry()` (ssl module), `check_kms_rotation_schedule()` (boto3)
  - On webhook push: `process_dependabot_alert()` (GitHub webhook → CVE record)
- Page has no high-frequency polling — lowest-frequency page in Division A

---

*Last updated: 2026-03-20*
