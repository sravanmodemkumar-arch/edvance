# div-a-28 — Platform Settings

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Platform-wide feature flags | ~40 |
| Email templates | ~30 (system + transactional) |
| Integration webhooks (outbound) | ~20 (PagerDuty, Slack, SIEM, etc.) |
| Configured SSO providers | 0–3 (per deployment) |
| Timezone | Asia/Kolkata (IST) — platform-wide |
| Supported languages | English · Hindi · Telugu · Tamil |
| Logo/branding variants | Platform + white-label per institution |

**Why this matters:** Platform Settings is the master control panel. A wrong feature flag can disable API access for all 100 coaching centres. An incorrect email template silently breaks student notifications. These settings require careful change management and full audit logging.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Platform Settings |
| Route | `/exec/settings/platform/` |
| Django view | `PlatformSettingsView` |
| Template | `exec/platform_settings.html` |
| Priority | P2 |
| Nav group | Settings |
| Required role | `superadmin` only |
| 2FA required | All saves |
| HTMX poll | None |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Platform Settings                                                    │
│ ⚠ All changes here require 2FA and are permanently audit-logged.            │
├──────────────────────────────────────────────────────────────────────────────┤
│ TABS: [General] [Feature Flags] [Email Templates] [Integrations] [Advanced] │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: GENERAL                                                                 │
│ Platform name / Logo / Timezone / Language / Support email / etc.           │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 Warning Banner

`bg-[#451A03] border border-[#FCD34D] rounded-xl p-4 mx-4 mb-2 text-sm text-[#FCD34D]`
"⚠ All changes on this page affect the entire platform (2,050 institutions). Changes are audit-logged and require 2FA confirmation."

---

### 4.2 Tab: General

`id="tab-general"` · `hx-get="?part=general_settings"`

**Form sections:**

**Platform Identity:**
| Field | Type | Detail |
|---|---|---|
| Platform name | Text | "Srav Platform" |
| Platform URL | URL (read-only) | |
| Logo | Image upload | PNG/SVG · max 2MB · shown in all emails |
| Favicon | Image upload | 32×32 ICO/PNG |
| Support email | Email | "support@srav.in" |
| Grievance officer | Text | Name for DPDPA |
| Grievance officer email | Email | |

**Defaults:**
| Field | Type | Default |
|---|---|---|
| Timezone | Select | Asia/Kolkata |
| Language | Select | English |
| Date format | Select | DD/MM/YYYY |
| Currency | Read-only | INR (₹) |
| Academic year start | Month picker | June |

**Contact & Social:**
- Support phone · WhatsApp support number · LinkedIn URL · Twitter URL

**[Save General Settings]** · 2FA required · toast confirmation

---

### 4.3 Tab: Feature Flags

`id="tab-flags"` · `hx-get="?part=feature_flags"`

**Feature flags table:**
`bg-[#0D1526] rounded-xl border border-[#1E2D4A]`

| Feature | Description | Enabled | Scope | Last changed | Changed by |
|---|---|---|---|---|---|
| API Access | Enable API keys platform-wide | ✓ | All plans | 15 Jan 2025 | admin |
| Proctoring | AI proctoring globally | ✓ | All | 01 Jan 2025 | admin |
| Parent Portal | Parent dashboard | ✓ | Pro + Enterprise | 20 Feb 2025 | admin |
| White-label | Custom domain + branding | ✓ | Enterprise | 01 Jan 2025 | admin |
| Bulk SMS | SMS notifications | ✓ | All | 15 Mar 2025 | admin |
| NEET Mode | NEET-specific exam format | ✗ | — | — | — |
| Experimental Dashboard | Beta dashboard UI | ✗ | Staff only | — | — |

**Toggle switch:** `accent-[#6366F1]` · clicking opens Confirm Feature Change Modal (§6.1) before saving

**Scope column:** which plans/institutions this flag applies to (editable inline)

---

### 4.4 Tab: Email Templates

`id="tab-emails"` · `hx-get="?part=email_templates"`

**Template list:**
| Template | Trigger | Last edited | Actions |
|---|---|---|---|
| Welcome (institution) | Institution created | 15 Jan 2025 | [Edit] [Preview] [Send Test] |
| Invoice generated | Invoice created | 01 Feb 2025 | [Edit] [Preview] [Send Test] |
| Exam reminder | 24h before exam | 10 Mar 2025 | [Edit] [Preview] [Send Test] |
| Results published | Results ready | 01 Jan 2025 | [Edit] [Preview] [Send Test] |
| SLA breach | SLA miss | 15 Feb 2025 | [Edit] [Preview] [Send Test] |
| Maintenance notice | Maintenance scheduled | 01 Jan 2025 | [Edit] [Preview] [Send Test] |
| ... (30 templates total) | | | |

**[Edit]:** opens Email Template Drawer (§5.1)
**[Send Test]:** sends to current user email · toast confirmation

---

### 4.5 Tab: Integrations

`id="tab-integrations"` · `hx-get="?part=integrations"`

**Integration cards grid:**

```
┌──────────────────────────────┐
│ PagerDuty          [Connected]│
│ Incidents + alerts           │
│ API key: sk_pd_...8f4a (edit)│
│ [Test] [Disconnect]          │
└──────────────────────────────┘
```

Integrations: PagerDuty / Slack / Razorpay / Twilio / Cloudflare / AWS (read-only) / SIEM Webhook / Custom Webhook

**[Test]:** sends test event · shows result inline
**[Disconnect]:** requires 2FA + confirmation

**[+ Add Integration]:** opens integration picker

---

### 4.6 Tab: Advanced

`id="tab-advanced"` · `hx-get="?part=advanced_settings"`
**Superadmin only. All fields 2FA-gated.**

**Dangerous Settings (red section border):**
```
bg-[#1A0A0A] border border-[#EF4444] rounded-xl p-6
"⚠ These settings can break the platform for all users."
```

| Setting | Type | Detail |
|---|---|---|
| Maintenance mode | Toggle | Blocks all institution logins · shows maintenance page |
| API rate limit global override | Number | Overrides plan limits globally |
| Max concurrent exams | Number | Platform-wide limit |
| Session timeout (all roles) | Select | Default: 8h |
| Force 2FA for all roles | Toggle | Enforces 2FA even for basic roles |
| Data export allow-list | IP CIDRs | Which IPs can download bulk exports |

**[Save Advanced Settings]:** 2FA required · shows impact preview: "Enabling maintenance mode will affect {N} active sessions"

---

## 5. Drawers

### 5.1 Email Template Drawer (800 px)

`id="email-template-drawer"` · `w-[800px]` · `body.drawer-open`

**Header:** Template name + trigger event · `[×]`

**Left panel (480px) — Editor:**
- Subject line: text input
- Body: markdown/HTML editor with toolbar (Bold / Italic / Link / List / Table)
- Available variables: `{{institution_name}}` `{{contact_name}}` `{{invoice_amount}}` etc. (clickable to insert)
- Language tabs: English / Hindi / Telugu / Tamil (separate content per language)

**Right panel (280px) — Preview:**
- Real-time preview (re-renders on keyup, debounced 800ms)
- "Preview as: institution admin / student / billing contact" toggle
- Mobile preview toggle (320px width frame)

**Footer:** [Discard Changes] [Send Test Email] [Save Template] (2FA required)

---

## 6. Modals

### 6.1 Confirm Feature Flag Change Modal (480 px)

**2FA required.**
"Enable/Disable {Feature Name}?"
Impact statement: "This will affect {N} institutions and {M} students."
| Field | Type |
|---|---|
| Reason | Required text |
| Scheduled at | Datetime (optional — schedule for off-peak) |
| 2FA code | OTP |
**Footer:** [Cancel] [Confirm Change]

---

### 6.2 Integration Disconnect Modal (480 px)

**2FA required.**
"Disconnect {Integration Name}?"
Warning: "Disconnecting PagerDuty will stop all automated incident alerts."
**Footer:** [Cancel] [Disconnect]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=general_settings` | `exec/partials/settings_general.html` | Tab click |
| `?part=feature_flags` | `exec/partials/settings_flags.html` | Tab click |
| `?part=email_templates` | `exec/partials/settings_emails.html` | Tab click |
| `?part=integrations` | `exec/partials/settings_integrations.html` | Tab click |
| `?part=advanced_settings` | `exec/partials/settings_advanced.html` | Tab click |
| `?part=email_drawer&id={id}` | `exec/partials/email_template_drawer.html` | Edit button |

**Django view dispatch:**
```python
class PlatformSettingsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.manage_platform_settings"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "general_settings": "exec/partials/settings_general.html",
                "feature_flags": "exec/partials/settings_flags.html",
                "email_templates": "exec/partials/settings_emails.html",
                "integrations": "exec/partials/settings_integrations.html",
                "advanced_settings": "exec/partials/settings_advanced.html",
                "email_drawer": "exec/partials/email_template_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/platform_settings.html", ctx)

    def post(self, request):
        # All POSTs require 2FA verified in session
        if not request.session.get("2fa_verified"):
            return JsonResponse({"error": "2FA required"}, status=403)
        part = request.GET.get("part", "")
        handlers = {
            "save_general": self._handle_save_general,
            "toggle_flag": self._handle_toggle_flag,
            "save_email": self._handle_save_email,
            "save_advanced": self._handle_save_advanced,
        }
        if part in handlers:
            return handlers[part](request)
        return HttpResponseNotAllowed(["GET"])
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| General tab | < 300 ms | > 800 ms |
| Feature flags tab (40 rows) | < 300 ms | > 800 ms |
| Email template drawer | < 300 ms | > 800 ms |
| Email preview re-render | < 500 ms | > 1.5 s |
| Settings save | < 500 ms | > 1.5 s |
| Full page initial load | < 800 ms | > 2 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Maintenance mode ON | Orange banner on ALL pages "Maintenance mode active — only superadmins can log in" |
| Feature flag change during exam | Warning: "This will affect {N} live exams. Schedule for off-peak?" |
| Email template: missing required variable | [Save] blocked + "Missing required variable: {{institution_name}}" |
| Integration test fails | Toast "PagerDuty test failed: Invalid API key" + [Fix Config] link |
| 2FA fails on save | Toast "Incorrect 2FA code — please try again" · form not saved |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`5` | Switch tabs |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/platform_settings.html` | Full page shell |
| `exec/partials/settings_general.html` | General settings form |
| `exec/partials/settings_flags.html` | Feature flags table |
| `exec/partials/settings_emails.html` | Email templates list |
| `exec/partials/settings_integrations.html` | Integration cards |
| `exec/partials/settings_advanced.html` | Advanced dangerous settings |
| `exec/partials/email_template_drawer.html` | Email template editor |
| `exec/partials/flag_confirm_modal.html` | Feature flag change modal |
| `exec/partials/integration_disconnect_modal.html` | Disconnect modal |

---

## 12. Component References

| Component | Used in |
|---|---|
| `TabBar` | §4.2–4.6 |
| `SettingsForm` | §4.2 |
| `FeatureFlagTable` | §4.3 |
| `FeatureToggle` | §4.3 |
| `EmailTemplateList` | §4.4 |
| `IntegrationCard` | §4.5 |
| `DangerZoneSettings` | §4.6 |
| `DrawerPanel` | §5.1 |
| `RichTextEditor` | §5.1 |
| `EmailPreviewFrame` | §5.1 |
| `ModalDialog` | §6.1–6.2 |
