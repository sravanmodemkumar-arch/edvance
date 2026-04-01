# 11 — Branch Domain Manager

- **URL:** `/group/it/portals/domains/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4) and Group EduForge Integration Manager (Role 58, G4)

---

## 1. Purpose

The Branch Domain Manager handles custom domain configuration for all branch portals. By default, every branch portal is accessible at `{branch-slug}.eduforge.in`. When a branch wants to present a professionally-branded URL — such as `narayanahyd.eduforge.in` or a fully custom subdomain like `portal.narayanahyd.com` — the IT Admin or Integration Manager uses this page to add the domain, provide DNS verification instructions, and manage the associated SSL certificate.

Domain setup follows a three-step process: (1) Add the domain to the portal record in EduForge, (2) Configure the DNS CNAME record at the branch's domain registrar (pointing to EduForge's domain verification endpoint), and (3) EduForge verifies the CNAME propagation and issues an SSL certificate. The Domain Manager provides copy-ready DNS record instructions and real-time DNS propagation status to simplify this process for branch IT contacts who may not have deep DNS expertise.

SSL certificate management is critical because a portal with an expired SSL certificate will display browser security warnings to students and parents, severely damaging trust in the platform. This page surfaces SSL expiry dates prominently and sends alert banner warnings for certificates expiring within 30 days. Certificate renewal is handled by EduForge's backend (via Let's Encrypt integration) but must be triggered by the IT Admin or Integration Manager from this page.

Both the Group IT Admin and the Group EduForge Integration Manager have edit authority on this page, reflecting that domain and SSL management spans the operational (IT Admin) and technical integration (Integration Manager) concerns.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full access — add/edit/verify/remove domains | Joint primary role |
| Group EduForge Integration Manager | G4 | Full access — add/edit/verify/remove domains | Joint primary role |
| Group IT Director | G4 | Full read | No edit access; approves domain changes for suspended portals |
| Group IT Support Executive | G3 | Read-only | Domain name and DNS Verification Status columns only |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Branch Portal Manager → Domain Manager
```

### 3.2 Page Header
- **Title:** `Branch Domain Manager`
- **Subtitle:** `[Total Domains] domains configured · [Verified & Active] verified · [Pending] pending verification`
- **Role Badge:** `Group IT Admin / Group EduForge Integration Manager`
- **Right-side controls:** `+ Add Domain` · `Export Domain List (CSV)` · `Notification Bell`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any SSL certificate expired | "SSL certificate for [Domain] has expired. [Branch Name] portal users will see browser security warnings. Renew immediately." | Red (non-dismissible) |
| Any SSL certificate expiring within 30 days | "SSL certificate for [Domain] expires in [N] days. Renew before expiry to avoid user-facing warnings." | Amber |
| Any domain with DNS Verification Status = Failed | "DNS verification failed for [Domain]. Check the CNAME record at the registrar and re-verify." | Amber |
| Any domain not checked in > 24 hours | "Domain health check for [Domain] has not run in [N] hours. Check DNS configuration." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Domains Configured | Count of all custom domains across all portals | Blue (informational) | No drill-down |
| Verified & Active | Count of domains with DNS Verification Status = Verified and SSL = Valid | Green if = Total, Amber < 100%, Red if any unverified/invalid SSL | Filters table to verified+active |
| Pending DNS Verification | Count of domains with DNS Verification Status = Pending | Green = 0, Amber 1–3, Red > 3 | Filters table to Pending |
| SSL Expiring < 30 Days | Count of domains where SSL expiry is within 30 days | Green = 0, Amber 1–2, Red ≥ 3 | Filters table to expiring soon |

---

## 5. Main Table — Branch Domain List

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text (link to portal config) | Yes | Yes (multi-select) |
| Portal Slug | Text (monospace, small) | No | No |
| Custom Domain | Text (the domain being managed, e.g., `narayanahyd.eduforge.in`) | Yes | No |
| DNS Verification Status | Badge: Verified (green) / Pending (amber) / Failed (red) | Yes | Yes (checkbox group) |
| SSL Status | Badge: Valid (green) / Expiring (amber) / Expired (red) / Not Configured (grey) | Yes | Yes (checkbox group) |
| SSL Expiry Date | Date (red if < 30 days; grey if Not Configured) | Yes | Yes (date range, "expiring soon" toggle) |
| Last Checked | Relative datetime of last automated DNS/SSL health check | Yes | No |
| Actions | `Verify DNS` · `Configure SSL` · `Remove Domain` icon buttons | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| DNS Verification Status | Checkbox group | Verified / Pending / Failed |
| SSL Status | Checkbox group | Valid / Expiring / Expired / Not Configured |
| SSL Expiring Within | Quick filter: 7 days / 30 days / 60 days | |
| Branch | Multi-select dropdown | All branches |

### 5.2 Search
- Full-text: Branch name, custom domain string
- 300ms debounce, triggers HTMX GET with `?search=` query param

### 5.3 Pagination
- Server-side · 20 rows/page · Shows total count

---

## 6. Drawers

### 6.1 Drawer: `domain-add-edit` — Add / Edit Domain
- **Trigger:** `+ Add Domain` button (new) or click domain in table row (edit)
- **Width:** 360px
- **Fields:**
  - Branch Select: dropdown (required for Add; pre-filled and read-only for Edit)
  - Custom Domain: text input — the full domain or subdomain to use (e.g., `portal.narayanahyd.com`). On blur: client-side regex validation (valid domain format). Server-side uniqueness check via HTMX GET.
  - **DNS Instructions section (shown after domain is entered):**
    - Instructional text: "To verify this domain, add the following CNAME record at your DNS provider:"
    - Record Type: `CNAME` (read-only label)
    - Host / Name: `[subdomain or @]` (read-only with Copy button)
    - Target / Value: `verify.eduforge.in` (read-only with Copy button)
    - TTL: `3600` (read-only)
    - Helper note: "DNS propagation can take up to 24 hours. Click 'Save & Start Verification' when the record has been added."
- **Submit:** POST creates domain record in PostgreSQL with DNS Verification Status = Pending; backend starts polling for DNS propagation

### 6.2 Drawer: `domain-verification` — Domain Verification Status
- **Trigger:** Actions → Verify DNS
- **Width:** 480px
- **Layout:** Step-by-step status display (not a form)
  - **Step 1 — DNS Record Added:** Check icon if CNAME record is detected; waiting spinner if not yet propagated; error icon if TTL has passed without detection
  - **Step 2 — DNS Propagation:** Shows propagation check result from multiple global DNS resolvers (e.g., 8.8.8.8, 1.1.1.1, quad9); each resolver shown with pass/fail icon
  - **Step 3 — EduForge Verification:** Confirmed once all resolvers return the correct CNAME target
  - **Step 4 — SSL Certificate Issued:** Shown once Let's Encrypt certificate has been issued and installed
- **Manual Re-check button:** HTMX POST to `/api/v1/it/portals/domains/{id}/verify/` — triggers an immediate DNS check cycle rather than waiting for the next automated check
- **Copy CNAME Record button:** Copies the correct CNAME target to clipboard
- **Status refreshes automatically:** HTMX polling every 30 seconds (`hx-trigger="every 30s"`) while Status = Pending

### 6.3 Drawer: `domain-ssl` — Configure / Renew SSL
- **Trigger:** Actions → Configure SSL
- **Width:** 360px
- **Content (current cert details):** Domain, issuer (Let's Encrypt), issued date, expiry date, certificate status badge
- **Actions:**
  - Renew Certificate Now button (HTMX POST) — only active if expiry < 60 days or expired
  - Force Re-issue button (for broken certs) — requires a confirmation step
- **Note:** SSL is issued automatically by EduForge via Let's Encrypt ACME protocol when DNS verification passes. This drawer is for manual renewal or re-issue when the automatic renewal fails.

### 6.4 Modal: `domain-remove` — Remove Domain
- **Trigger:** Actions → Remove Domain
- **Width:** 400px
- **Content:** "You are about to remove the custom domain [Domain] from [Branch Name]. The branch portal will revert to its default EduForge URL ({slug}.eduforge.in). This action takes effect immediately." · Confirm Remove · Cancel
- **On confirm:** Domain record deleted from PostgreSQL; portal reverts to default URL

**Audit Trail:** All domain configuration changes are logged to IT Audit Log: user ID, timestamp, action (add/edit/remove/renew-ssl), domain name, old and new values, branch identifier.

**Notifications:**
- SSL certificates expiring < 30 days: daily email to IT Admin + branch primary contact with renewal link
- SSL expiring < 7 days: additional in-app notification badge added

---

## 7. Charts

No charts on this page. Domain status is best communicated via the table and KPI cards rather than time-series charts. SSL expiry tracking is handled via the table's SSL Expiry Date column with colour coding.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Domain added | "Custom domain [domain] added for [Branch Name]. DNS verification started." | Success | 5s |
| Domain updated | "Domain updated for [Branch Name]." | Success | 4s |
| DNS verification passed | "DNS verification successful for [domain]. SSL certificate is being issued." | Success | 5s |
| SSL certificate issued | "SSL certificate issued for [domain]. Portal is now accessible via the custom domain." | Success | 5s |
| DNS verification failed | "DNS verification failed for [domain]. CNAME record not found. Check your DNS settings." | Error | 7s |
| SSL renewal triggered | "SSL certificate renewal initiated for [domain]." | Info | 4s |
| SSL renewal complete | "SSL certificate renewed for [domain]. New expiry: [date]." | Success | 5s |
| Domain removed | "Custom domain removed. [Branch Name] now uses [slug].eduforge.in." | Info | 5s |
| Domain uniqueness error | "The domain [domain] is already associated with another portal." | Error | 5s |
| General error | "Failed to save changes. Please try again." | Error | 6s |
| SSL renewal failed | Error: `SSL certificate renewal failed. Verify DNS configuration and try again.` | Error | 7s |
| Domain update failed | Error: `Failed to update domain. Ensure the domain is not already in use.` | Error | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No custom domains configured | "No Custom Domains" | "No branch portals have custom domains configured. All branches are currently using their default EduForge URLs." | + Add Domain |
| All domains verified and SSL valid | "All Domains Healthy" | "Every configured custom domain is verified and has a valid SSL certificate." | — |
| Search returns no results | "No Domains Match" | "No domains match your search or filter criteria." | Clear Filters |
| No domains expiring soon | "No SSL Renewals Due" | "No SSL certificates are expiring within the next 30 days." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer (4 cards) + table skeleton (8 rows) |
| Add Domain drawer open | Drawer-scoped spinner while branch dropdown options load |
| Edit Domain drawer open | Drawer-scoped spinner while current domain data and SSL status load |
| Domain uniqueness check on blur | Inline spinner on domain input; green tick or red error on completion |
| Verification Status drawer open | Drawer-scoped spinner then step-by-step status loads |
| DNS polling (every 30s) | Subtle "Checking…" indicator in the verification status area; non-intrusive |
| SSL renewal request | Renew button spinner + disabled state |
| Remove domain confirmation | Confirm button spinner + disabled state |
| Table filter/search | Table area overlay shimmer |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | Integration Manager (G4) | IT Director (G4) | IT Support Executive (G3) |
|---|---|---|---|---|
| KPI Summary Bar | All 4 cards | All 4 cards | All 4 cards | Total Domains only |
| Domain Table | Visible + all Actions | Visible + all Actions | Visible (no Actions) | Branch Name + DNS Status only |
| + Add Domain Button | Visible | Visible | Hidden | Hidden |
| Verify DNS Action | Visible | Visible | Hidden | Hidden |
| Configure SSL Action | Visible | Visible | Hidden | Hidden |
| Remove Domain Action | Visible | Visible | Hidden | Hidden |
| DNS Instructions (copy-able) | Visible in drawer | Visible in drawer | Visible (read-only) | Hidden |
| Alert Banners | All | All | All | SSL Expired banner only |
| Export CSV | Visible | Visible | Visible | Hidden |

**Note:** Role 55 (DPO) and Role 56 (Cybersecurity Officer) have no access to this page (returns 403).

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/portals/domains/` | JWT (G4) | Paginated domain list |
| GET | `/api/v1/it/portals/domains/kpis/` | JWT (G4) | Returns 4 KPI card values |
| POST | `/api/v1/it/portals/domains/` | JWT (G4) | Add a custom domain to a portal |
| GET | `/api/v1/it/portals/domains/{id}/` | JWT (G4) | Domain detail (for edit drawer pre-fill) |
| PATCH | `/api/v1/it/portals/domains/{id}/` | JWT (G4) | Update domain settings |
| DELETE | `/api/v1/it/portals/domains/{id}/` | JWT (G4) | Remove a custom domain |
| POST | `/api/v1/it/portals/domains/{id}/verify/` | JWT (G4) | Trigger a manual DNS verification check |
| GET | `/api/v1/it/portals/domains/{id}/verification-status/` | JWT (G4) | Real-time DNS propagation status for polling |
| POST | `/api/v1/it/portals/domains/{id}/ssl/renew/` | JWT (G4) | Trigger SSL certificate renewal |
| GET | `/api/v1/it/portals/domains/slug-check/?domain={domain}` | JWT (G4) | Check domain uniqueness for inline validation |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/it/portals/domains/kpis/` | `#kpi-bar` | `innerHTML` |
| Load domain table | `load` | GET `/api/v1/it/portals/domains/` | `#domain-table` | `innerHTML` |
| Open Add Domain drawer | `click` on + Add Domain | GET `/api/v1/it/portals/domains/add-form/` | `#domain-drawer` | `innerHTML` |
| Domain uniqueness check on blur | `blur` on domain input | GET `/api/v1/it/portals/domains/slug-check/?domain={value}` | `#domain-validation` | `innerHTML` |
| Submit Add Domain | `click` on Save & Start Verification | POST `/api/v1/it/portals/domains/` | `#domain-result` | `innerHTML` |
| Open Verify DNS drawer | `click` on Verify DNS | GET `/api/v1/it/portals/domains/{id}/verification-status/` | `#verify-drawer` | `innerHTML` |
| Poll DNS verification status | `every 30s` (while Status = Pending) | GET `/api/v1/it/portals/domains/{id}/verification-status/` | `#verification-steps` | `innerHTML` |
| Manual re-check DNS | `click` on Re-check Now | POST `/api/v1/it/portals/domains/{id}/verify/` | `#verification-steps` | `innerHTML` |
| Open SSL drawer | `click` on Configure SSL | GET `/api/v1/it/portals/domains/{id}/` | `#ssl-drawer` | `innerHTML` |
| Renew SSL certificate | `click` on Renew Certificate Now | POST `/api/v1/it/portals/domains/{id}/ssl/renew/` | `#ssl-result` | `innerHTML` |
| Confirm remove domain | `click` on Confirm Remove | DELETE `/api/v1/it/portals/domains/{id}/` | `#domain-row-{id}` | `outerHTML` |
| Filter domain table | `change` on filter controls | GET `/api/v1/it/portals/domains/?ssl_status=expiring` | `#domain-table` | `innerHTML` |
| Search domains | `keyup[debounce:300ms]` on search | GET `/api/v1/it/portals/domains/?search=` | `#domain-table` | `innerHTML` |
| Paginate table | `click` on page button | GET `/api/v1/it/portals/domains/?page=N` | `#domain-table` | `innerHTML` |
| Refresh KPI after add/remove | `htmx:afterRequest` on POST/DELETE | GET `/api/v1/it/portals/domains/kpis/` | `#kpi-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
