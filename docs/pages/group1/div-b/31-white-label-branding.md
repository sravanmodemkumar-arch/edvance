# 31 — White-Label & Branding Manager

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | White-Label & Branding Manager |
| Route | `/product/white-label/` |
| Django view | `WhiteLabelBrandingView` |
| Template | `product/white_label.html` |
| Priority | **P2** |
| Nav group | Product |
| Required roles | `pm_institution_portal` · `superadmin` |
| All others | Denied — redirect |
| 2FA required | Yes — activating custom subdomain for an institution |
| HTMX poll | None (config page) |
| Cache | Per-institution brand config cached at Redis TTL 3600s (CloudFront reads this on every request) |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · success `#22C55E` · danger `#EF4444` |

---

## 2. Purpose & Business Logic

**The branding problem:**

Enterprise coaching centres (the platform's highest-value segment at ₹15 Cr ARR) want their students to feel they are using "Narayana's platform" or "Sri Chaitanya's system" — not visibly EduForge. They pay premium Enterprise pricing in part for this white-label capability. Currently, white-labelling is done manually by DevOps (DNS record + config file edit + CDN deployment) — a 3-day process per institution.

This page allows PM Institution Portal to:
1. **Provision custom subdomains** — `exams.narayana.ac.in` → points to EduForge platform, serves institution's brand
2. **Manage brand kits** — logo, primary color, secondary color, font choice per institution
3. **Configure white-label rules** — which plan tiers get which level of white-labelling
4. **Monitor subdomain health** — SSL expiry, DNS propagation status, CDN cache status

**White-label tiers:**
| Plan | White-label Level | Custom Domain | Brand Colors | Remove EduForge Logo |
|---|---|---|---|---|
| Starter | None | ❌ | ❌ | ❌ |
| Standard | Basic | ❌ | ✅ Colors + Logo | ❌ |
| Professional | Full | ✅ Subdomain | ✅ Full kit | ✅ |
| Enterprise | Complete | ✅ Custom domain | ✅ Full kit | ✅ |

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| PM Institution Portal | All | Configure rules, provision subdomains, approve brand kits |
| Superadmin | All | Same as PM Institution Portal |
| All others | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Summary Strip

```
White-Label & Branding Manager
────────────────────────────────────────────────────────────────────────────────
Custom Domains   Brand Kits Active   SSL Expiring <30d   Pending Approval   Plan Coverage
     48               186               3                    4              Enterprise: 100%
```

- "SSL Expiring <30d": amber if > 0 — click filters to those institutions
- "Pending Approval": brand kit submissions awaiting PM review

---

### Section 2 — White-Label Rules Config

**Purpose:** PM configures which plan tier unlocks which white-label features. This is the master policy.

```
WHITE-LABEL RULES (Platform Policy)                               [Edit Rules]
────────────────────────────────────────────────────────────────────────────────
Feature                    Starter    Standard   Professional  Enterprise
────────────────────────────┼──────────┼──────────┼─────────────┼──────────────
Custom logo                 ❌         ✅          ✅            ✅
Brand color scheme          ❌         ✅          ✅            ✅
Remove "Powered by EduForge"❌         ❌          ✅            ✅
Custom subdomain            ❌         ❌          ✅            ✅
Custom apex domain          ❌         ❌          ❌            ✅
White-label mobile app icon ❌         ❌          ❌            ✅
Custom email From-name      ❌         ✅          ✅            ✅
Custom SMS sender ID        ❌         ❌          ✅ (with TRAI) ✅
```

- Edit: 2FA required; change applies to all institutions on that plan immediately
- Custom apex domain (e.g., `exams.narayana.ac.in` not just `narayana.eduforge.in`): Enterprise only — requires DNS verification + SSL provisioning

---

### Section 3 — Institution Brand Kits Table

```
INSTITUTION BRAND KITS        [Status: All ▾]  [Plan ▾]  [Search institution...]
────────────────────────────────────────────────────────────────────────────────
Institution            Plan         Custom Domain            Brand Status    SSL
─────────────────────┼─────────────┼────────────────────────┼───────────────┼───────
Narayana Coaching     Enterprise   exams.narayana.ac.in     ✅ Active        ✅ 280d
Sri Chaitanya         Enterprise   test.srichaitanya.com    ✅ Active        ✅ 194d
Delhi Public School   Professional dps.eduforge.in          ✅ Active        ✅ 312d
KV Sangathan          Professional kvs.eduforge.in          ⏳ DNS Pending   —
AP Model Schools      Standard     (no custom domain)       ✅ Colors only   —
Sunrise Coaching      Enterprise   (subdomain pending)      ⏰ Pending Appr. —
```

- Click row → Brand Kit Drawer (Section 6)
- "DNS Pending" → amber; tooltip "DNS propagation in progress — may take up to 48h"
- "Pending Approval" → PM has a brand kit submission to review (logo/colors uploaded by institution)
- ⋯ menu: View Brand Kit / Edit / Revoke Custom Domain / Regenerate SSL

---

### Section 4 — Subdomain Provisioning

**Purpose:** When an institution wants a new custom subdomain, PM initiates the provisioning workflow.

```
SUBDOMAIN PROVISIONING — New Request
────────────────────────────────────────────────────────────────────────────────
Institution:  Sunrise Coaching Centre (Enterprise)
Requested:    exams.sunrisecoaching.in
Type:         Apex domain (institution owns DNS)

PROVISIONING STEPS
1. ☑ Plan eligibility verified (Enterprise ✅)
2. ☑ Domain ownership: institution added TXT record (_eduforge-verify.sunrisecoaching.in)
3. ⏳ DNS verification: checking...  [Verify Now]
4. ⬜ SSL certificate: (will auto-provision via AWS ACM after DNS verified)
5. ⬜ CloudFront distribution: (created after SSL)
6. ⬜ Platform routing: (eduforge.in → institution's custom domain)
7. ⬜ Go-live: [Activate Custom Domain]

Estimated completion: 24–48 hours (DNS propagation dependent)
```

- Step 3 "Verify Now": POST → AWS Route53 DNS TXT lookup → if found, marks step complete
- Step 4–6: automated via AWS Lambda (triggered after step 3 completes)
- Step 7 "Activate Custom Domain": 2FA required; sends confirmation email to institution
- Status updates via Celery task `check_subdomain_provisioning()` every 30 min

---

### Section 5 — SSL & Domain Health Monitor

```
SSL & DOMAIN HEALTH MONITOR
────────────────────────────────────────────────────────────────────────────────
Institution             Domain                  SSL Expiry    Status     Action
─────────────────────┼──────────────────────────┼─────────────┼──────────┼──────────
KV Sangathan           kv.eduforge.in            22 Apr 2026  ⚠ 33d     [Renew]
Delhi Saraswati        delhi.eduforge.in          11 Apr 2026  🔴 21d    [Renew Now]
Narayana               exams.narayana.ac.in       Dec 2026    ✅ 280d   —
```

- SSL certificates: managed via AWS ACM (auto-renew for `*.eduforge.in` wildcard)
- Custom apex domains: ACM sends renewal notification — PM must manually initiate
- "Renew Now": triggers ACM certificate renewal request + CloudFront association update
- Celery beat task `check_ssl_expiry()` daily at 07:00 IST — alerts PM if any cert < 30 days

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  White-Label & Branding Manager                                              ║
║  48 custom domains · 186 brand kits · 3 SSL expiring <30d · 4 pending       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  WHITE-LABEL RULES (Policy)                                                  ║
║  Standard: logo+colors  |  Professional: custom subdomain  |  Enterprise: apex ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  INSTITUTION BRAND KITS                                                      ║
║  Narayana  Enterprise  exams.narayana.ac.in  ✅  SSL 280d                    ║
║  Sri Chait Enterprise  test.srichaitanya.com ✅  SSL 194d                    ║
║  KV Sangathan Prof.    kvs.eduforge.in       ⏳ DNS Pending                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  SSL HEALTH: Delhi Saraswati — 21d ⚠  [Renew Now]                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Brand Kit Drawer (640px)

```
Narayana Coaching — Brand Kit
────────────────────────────────────────────────────────────────────────────────
[BRAND PREVIEW]                              [Logos & Assets]
  ┌─────────────────────────────────────┐    Logo (light bg): narayana_logo.png
  │  [Narayana Logo]                    │    Logo (dark bg):  narayana_dark.png
  │  exams.narayana.ac.in              │    Favicon:         narayana_fav.ico
  │  Primary: #1A237E  Secondary: #FF6F00│
  │  Font: Poppins                      │
  └─────────────────────────────────────┘

CUSTOM DOMAIN
  Domain:  exams.narayana.ac.in  ✅ Active
  SSL:     Let's Encrypt · Expires 18 Dec 2026
  CDN:     CloudFront distribution d1xyz.cloudfront.net
  Routing: ✅ All traffic routing to platform

BRAND COLORS
  Primary:   #1A237E  ████ (deep navy — Narayana corporate color)
  Secondary: #FF6F00  ████ (Narayana orange)
  Button:    #1A237E
  Text:      #FFFFFF (light) / #1A237E (dark)

MOBILE APP
  App icon:  narayana_appicon.png  ✅ Active (Play Store + App Store)
  App name:  "Narayana Test Platform"
  Bundle ID: in.narayana.exams

[Edit Brand Kit]  [Revoke Custom Domain]  [Download Assets]  [Close]
```

---

## 7. HTMX Architecture

| `?part=` | Target | Trigger |
|---|---|---|
| `summary` | `#wl-summary` | load |
| `rules` | `#wl-rules` | load |
| `brand-kits` | `#brand-kits-table` | load + filter change |
| `provisioning` | `#provisioning-status` | load + institution select |
| `ssl-health` | `#ssl-health` | load |
| `brand-drawer` | `#drawer-container` | row click |

---

## 8. Backend View & API

```python
class WhiteLabelBrandingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_white_label"

    def get(self, request):
        if request.user.role not in {"pm_institution_portal","superadmin"}:
            return redirect("product:dashboard")
        if _is_htmx(request):
            part = request.GET.get("part","")
            dispatch = {
                "summary":      "product/wl/partials/summary.html",
                "rules":        "product/wl/partials/rules.html",
                "brand-kits":   "product/wl/partials/brand_kits.html",
                "provisioning": "product/wl/partials/provisioning.html",
                "ssl-health":   "product/wl/partials/ssl_health.html",
                "brand-drawer": "product/wl/partials/brand_drawer.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], self._build_ctx(request))
        return render(request, "product/white_label.html", self._build_ctx(request))
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/product/white-label/actions/verify-dns/` | PM Portal | Run DNS TXT lookup for domain verification |
| POST | `/product/white-label/actions/activate-domain/` | PM Portal + 2FA | Activate custom domain (CloudFront routing) |
| POST | `/product/white-label/actions/renew-ssl/` | PM Portal | Trigger ACM certificate renewal |
| POST | `/product/white-label/actions/revoke-domain/` | PM Portal + 2FA | Remove custom domain routing |
| POST | `/product/white-label/actions/update-brand-kit/` | PM Portal | Save brand kit colors/logos |

---

## 9. Database Schema

```python
class InstitutionBrandKit(models.Model):
    institution     = models.OneToOneField("Institution", on_delete=models.CASCADE)
    primary_color   = models.CharField(max_length=7)    # "#1A237E"
    secondary_color = models.CharField(max_length=7, blank=True)
    button_color    = models.CharField(max_length=7, blank=True)
    logo_light_s3   = models.CharField(max_length=300, blank=True)  # S3 key
    logo_dark_s3    = models.CharField(max_length=300, blank=True)
    favicon_s3      = models.CharField(max_length=300, blank=True)
    font_family     = models.CharField(max_length=100, default="Inter")
    remove_powered_by = models.BooleanField(default=False)
    app_icon_s3     = models.CharField(max_length=300, blank=True)
    app_name        = models.CharField(max_length=100, blank=True)
    custom_email_from_name = models.CharField(max_length=100, blank=True)
    custom_sms_sender_id   = models.CharField(max_length=11, blank=True)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                         on_delete=models.SET_NULL)
    updated_at      = models.DateTimeField(auto_now=True)


class CustomDomain(models.Model):
    STATUSES = [("pending_dns","Pending DNS"),("dns_verified","DNS Verified"),
                ("ssl_provisioning","SSL Provisioning"),("active","Active"),
                ("revoked","Revoked")]
    institution     = models.OneToOneField("Institution", on_delete=models.CASCADE)
    domain          = models.CharField(max_length=253, unique=True)  # "exams.narayana.ac.in"
    is_apex         = models.BooleanField(default=False)
    dns_txt_token   = models.CharField(max_length=64)   # verification token
    dns_verified_at = models.DateTimeField(null=True)
    ssl_arn         = models.CharField(max_length=300, blank=True)   # ACM ARN
    ssl_expiry      = models.DateField(null=True)
    cloudfront_dist = models.CharField(max_length=50, blank=True)    # distribution ID
    status          = models.CharField(max_length=30, choices=STATUSES, db_index=True)
    activated_by    = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                         on_delete=models.SET_NULL)
    activated_at    = models.DateTimeField(null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
```

**Celery tasks:**
```python
@shared_task
def check_ssl_expiry():
    """Daily at 07:00 IST. Alert PM if any custom domain SSL < 30 days."""
    expiring = CustomDomain.objects.filter(
        status="active", ssl_expiry__lte=date.today() + timedelta(days=30)
    )
    if expiring.exists():
        send_mail_to_role("pm_institution_portal",
                          subject=f"SSL expiry alert: {expiring.count()} domains",
                          body=render_to_string("emails/ssl_expiry_alert.html",
                                                {"domains": expiring}))

@shared_task
def check_subdomain_provisioning():
    """Every 30 min. Check DNS + SSL status for pending domains."""
    pending = CustomDomain.objects.filter(status__in=["pending_dns","ssl_provisioning"])
    for domain in pending:
        _check_and_advance_provisioning(domain)
```

---

## 10. Validation Rules

| Action | Validation |
|---|---|
| Brand primary color | Valid hex code `#RRGGBB`; min contrast ratio 4.5:1 against white (WCAG AA) |
| Logo upload | PNG/SVG only; max 500KB; min 200×200px |
| Custom subdomain | Valid FQDN; institution must own the apex domain (verified via TXT record) |
| Custom SMS sender ID | 6–11 alphanumeric chars; TRAI DLT registration required (warning shown) |
| Activate custom domain | 2FA required; institution must be on Professional or Enterprise plan |
| Remove "Powered by EduForge" | Only for Professional/Enterprise plan — blocked with upgrade prompt for Standard |

---

## 11. Security Considerations

- Brand kit assets (logos) stored in S3 private bucket; served via CloudFront signed URLs
- Custom domain activation: 2FA-gated; logged to `AuditLog` with institution ID and domain
- DNS verification uses HMAC-signed TXT token — prevents one institution from claiming another's domain
- CloudFront distribution: per-institution WAF rules inherited from global WAF config (CTO managed)
- Revoke domain: immediate CloudFront routing update; DNS record left in place (institution must clean up their DNS)

---

## 12. Edge Cases

| State | Behaviour |
|---|---|
| Institution downgrades from Enterprise to Standard | Warning: "Custom apex domain will be deactivated in 30 days — institution reverts to `{slug}.eduforge.in`". PM receives notification. |
| DNS verification fails after 48h | Status → "DNS Verification Failed"; PM notified; troubleshooting guide shown with expected TXT record value |
| SSL auto-renewal fails (ACM issue) | Alert to PM and CTO; manual renewal trigger available; 7-day grace before domain shows SSL warning |
| Brand color fails WCAG contrast | Warning shown on save: "Primary color #FFFF00 may be hard to read — contrast ratio 1.3:1. Recommend minimum 4.5:1." Can override. |

---

*Last updated: 2026-03-20*
