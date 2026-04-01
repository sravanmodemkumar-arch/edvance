# 30 — Custom Domain Per Branch (Setup Wizard)

- **URL:** `/group/it/integrations/domains/setup/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group EduForge Integration Manager (Role 58, G4) — Full access

---

## 1. Purpose

The Custom Domain Setup Wizard guides the Integration Manager through the complete end-to-end process of assigning a custom domain to a branch portal. By default, each branch portal is accessible via a subdomain of EduForge's platform (e.g., `branchname.eduforge.in`). When a branch has its own branded web presence, the institution may want their portal accessible at `portal.branchname.edu.in` or `student.branchname.com`. This wizard handles the full technical setup flow.

This page is intentionally different from the Branch Domain Manager (page 11 in Division A), which is the admin table showing the status of all configured domains. That page is for operations and oversight. This wizard page is for the step-by-step guided setup of a new domain, designed to minimise errors and ensure the Integration Manager completes all required steps in the correct order: select the branch, enter and validate the domain, add the correct DNS records, verify propagation, provision an SSL certificate, and go live.

The wizard uses HTMX polling in Step 4 (DNS verification) to check propagation automatically every 30 seconds, so the Integration Manager does not need to manually hit Refresh repeatedly. SSL provisioning in Step 5 is handled by Let's Encrypt via Cloudflare's certificate authority integration — certificates are auto-renewed before expiry. Once a domain goes live, the branch's portal URL is updated in the branch configuration and all internal links and emails use the new domain.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group EduForge Integration Manager | G4 | Full access to run wizard and view history | Sole operator |
| Group IT Director | G4 | Read-only (history table only) | Can view past setup sessions; cannot run wizard |
| Group IT Admin (Role 54, G4) | Full access | Configure and verify custom domains |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Integrations → Domain Setup Wizard
```

### 3.2 Page Header
- **Title:** `Custom Domain Setup Wizard`
- **Subtitle:** `Set up a branded domain for a branch portal — 5 guided steps`
- **Role Badge:** `Group EduForge Integration Manager`
- **Right-side controls:** (none — wizard is the primary interaction)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| A domain SSL certificate expiring <30 days for any live domain | "SSL certificate for [domain] expires in [N] days. Run the renewal flow or it will auto-renew if Cloudflare integration is active." | Amber |
| A setup session stuck >24h in verification step | "Domain setup for [Branch Name] has been waiting for DNS verification for [N] hours. DNS propagation may be slow — check your registrar." | Amber |
| A live domain's SSL cert has expired | "SSL certificate for [domain] has EXPIRED. The branch portal is now showing security warnings to users." | Red (non-dismissible) |

---

## 4. KPI Summary Bar

No KPI cards — this is a wizard page. Usage statistics are in the history table below the wizard.

---

## 5. Wizard — 5-Step Flow

The wizard is displayed as a stepped progress indicator at the top with numbered steps. Completed steps show a checkmark; the current step is highlighted; future steps are greyed out.

```
Step 1: Select Branch → Step 2: Enter Domain → Step 3: DNS Configuration → Step 4: Verification → Step 5: SSL & Go Live
```

---

### Step 1: Select Branch

- **Component:** Dropdown — "Select branch to configure domain for"
  - Populated from PostgreSQL with branches that do NOT yet have a live custom domain
  - Branches already live with custom domain shown as disabled options with "(Domain Live)" label
  - Branches with a pending/in-progress setup shown with "(Setup In Progress)" label
- **Branch info card** (shown after selection): Branch name, current URL (`branchname.eduforge.in`), Principal name, location
- **Next button:** Active once branch is selected

---

### Step 2: Enter Domain

- **Input:** "Custom Domain" (text input — e.g., `portal.somervilleacademy.edu.in`)
  - Validates format on blur: must be a valid FQDN
  - Validates no leading/trailing spaces
  - Validates not already in use by another branch
- **Domain check:** On Next click, triggers API call to check:
  - Domain format valid (client-side)
  - Domain not already registered in EduForge system (server-side)
  - Domain resolves in DNS (NXDOMAIN check — warns if domain doesn't exist in DNS at all, meaning the registrar hasn't created it yet)
- **Error states:**
  - Invalid format → inline error "Please enter a valid fully-qualified domain name"
  - Already in use → inline error "This domain is already configured for [Other Branch Name]. Each domain can only be assigned to one branch."
  - Domain not found in DNS → amber warning "This domain does not currently have any DNS records. Please create the domain at your registrar first, then continue."
- **Next button:** Active once domain passes validation

---

### Step 3: DNS Configuration

This step provides the DNS records the Integration Manager must add at the domain's registrar/DNS provider.

**Records to add (shown in a configuration panel):**

| Record Type | Name | Value | TTL | Purpose |
|---|---|---|---|---|
| CNAME | `portal.branchname.edu.in` | `custom.eduforge.in` | 300 | Routes domain to EduForge edge |
| TXT | `_eduforge-verification.branchname.edu.in` | `eduforge-verify=[unique token]` | 300 | Proves domain ownership |

Each record row has a copy button for Name and Value fields.

**Instructions panel:**
1. Log in to your domain registrar or DNS provider (Cloudflare, GoDaddy, BigRock, Namecheap, etc.)
2. Navigate to DNS settings for `branchname.edu.in`
3. Add the CNAME record shown above
4. Add the TXT verification record shown above
5. Save the records
6. DNS propagation typically takes 5–30 minutes (up to 24h in some regions)

**Checkbox:** "I have added the DNS records at my registrar" (required to enable Next)

**Next button:** Active once checkbox is ticked. This does NOT verify the records — verification happens in Step 4.

---

### Step 4: Verification

The wizard polls for DNS propagation automatically.

- **Polling:** HTMX auto-polling every 30 seconds (`hx-trigger="every 30s"`) against the DNS verification endpoint
- **Status display:**
  - Animated spinner with "Checking DNS propagation…"
  - Last checked: [timestamp]
  - CNAME record status: Pending / Detected (green) / Mismatch (red)
  - TXT verification record status: Pending / Verified (green) / Not Found (red)
  - Propagation percentage (estimated from checking multiple resolver locations — uses EduForge backend DNS lookup, not client-side)

**Verification results:**
  - Both records verified → green success banner "DNS verified. Both records detected. Proceed to SSL provisioning."
  - CNAME detected but TXT not found → amber "CNAME record found. Awaiting TXT verification record."
  - Neither found after 1h → amber warning "DNS propagation is taking longer than expected. Check that records were saved correctly at your registrar." + "Manual Check Now" button

**Manual Refresh button:** Forces an immediate check outside the polling interval

**Next button:** Only active once BOTH records are verified. Cannot be bypassed.

---

### Step 5: SSL & Go Live

**Step 5a — SSL Provisioning:**
- "Provisioning SSL certificate via Let's Encrypt…" progress indicator
- Certificate provisioned automatically (API call to Cloudflare/Let's Encrypt)
- On success: green banner "SSL certificate provisioned. Domain is now secured with HTTPS."
- On failure: red banner with error and fallback instruction

**Step 5b — Go Live Confirmation:**
- Summary card showing:
  - Branch: [Branch Name]
  - Custom Domain: [domain]
  - SSL: Active (valid until [date])
  - Previous URL: `branchname.eduforge.in` (will continue to redirect)
  - New URL: `[custom domain]`
- "What happens when you go live:" informational list:
  - Branch portal will be accessible at the custom domain
  - Old subdomain will 301-redirect to the new domain for 90 days
  - All system-generated emails will use the new domain
  - SSL will auto-renew 30 days before expiry
- **Go Live button** (green, prominent)
- On click: confirmation modal "Are you ready to make [domain] the live URL for [Branch Name]?"

**On successful go-live:**
- Full-page success screen: "Domain is live! [Branch Name] portal is now accessible at [domain]."
- IT Director notified via in-app notification
- Wizard resets to Step 1 for new setup

---

## 6. History Table (Below Wizard)

A read-only table of all past and in-progress domain setup sessions:

| Column | Content |
|---|---|
| Branch | Branch name |
| Domain | Domain configured |
| Status | Badge (Live / In Progress / Failed / Cancelled) |
| Step Reached | e.g., "Step 4 — DNS Verification" |
| Started By | Staff name |
| Started Date | Date |
| Completed Date | Date or "—" |
| Actions | Resume (if In Progress) / View (if Live or Failed) |

### 6.1 History Table Filters
- Status: Live / In Progress / Failed / Cancelled
- Date range

### 6.2 History Pagination
- Server-side · 15 rows/page

---

## 7. Drawers

### 7.1 Drawer: `domain-session-view` — View Setup Session
- **Trigger:** History table → View
- **Width:** 560px
- Full session log: each step, timestamp when entered, timestamp when completed, any errors encountered
- DNS check log (all poll results from verification step)
- SSL certificate details (if reached Step 5)
- Actions taken by whom and when

---

## 8. Charts

No charts on this page.

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Step completed | "Step [N] complete. Proceed to the next step." | Success | 3s |
| Domain validation passed | "Domain format valid and available." | Success | 3s |
| DNS verified | "DNS records verified. Both CNAME and TXT records detected." | Success | 4s |
| SSL provisioned | "SSL certificate successfully provisioned for [domain]." | Success | 4s |
| Domain went live | "[Domain] is now LIVE for [Branch Name]. IT Director has been notified." | Success | 6s |
| Verification polling found records | "DNS records detected! Click Next to proceed to SSL provisioning." | Success | 5s |
| Wizard reset | "Wizard reset. You can begin a new domain setup." | Info | 3s |

---

## 10. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches without domain | "All Branches Have Custom Domains" | "Every branch already has a custom domain configured. Use the history table to review existing domains." | — |
| No history records | "No Setup Sessions" | "No domain setup sessions have been run yet." | — |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Wizard skeleton + history table skeleton (5 rows) |
| Branch dropdown load | Spinner inside dropdown |
| Domain validation (Step 2) | Inline spinner next to Next button: "Checking domain…" |
| DNS polling (Step 4) | Animated spinner + "Last checked [time]" updating every 30s |
| Manual check (Step 4) | Spinner: "Checking DNS records now…" |
| SSL provisioning (Step 5) | Progress bar with label: "Provisioning SSL certificate…" |
| History table load | Table skeleton shimmer |

---

## 12. Role-Based UI Visibility

| Element | Integration Manager (G4) | IT Director (G4) | IT Admin (G4) |
|---|---|---|---|
| Full wizard (all 5 steps) | Visible + interactive | Hidden | Visible + interactive |
| History table | Visible + Resume action | Visible (view only) | Visible + Resume action |
| View setup session drawer | Visible | Visible (read-only) | Visible |
| Go Live button | Visible | Hidden | Visible |
| DNS records copy buttons | Visible | Visible | Visible |
| Alert banners | Visible | Visible | Visible |

> Roles 55 (DPO), 56 (Cybersecurity Officer), and 57 (IT Support Executive) have no access to this page (returns 403).

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/domains/setup/branches/` | JWT (G4 — Integration Manager) | List branches eligible for custom domain setup |
| POST | `/api/v1/it/domains/setup/validate-domain/` | JWT (G4 — Integration Manager) | Validate domain format, availability, and DNS existence |
| POST | `/api/v1/it/domains/setup/session/` | JWT (G4 — Integration Manager) | Create new domain setup session (records step 1 completion) |
| PATCH | `/api/v1/it/domains/setup/session/{id}/step/` | JWT (G4 — Integration Manager) | Update session to next step |
| GET | `/api/v1/it/domains/setup/session/{id}/verify-dns/` | JWT (G4 — Integration Manager) | Check DNS propagation status (used by HTMX polling) |
| POST | `/api/v1/it/domains/setup/session/{id}/provision-ssl/` | JWT (G4 — Integration Manager) | Trigger SSL certificate provisioning |
| POST | `/api/v1/it/domains/setup/session/{id}/go-live/` | JWT (G4 — Integration Manager) | Activate custom domain for branch |
| GET | `/api/v1/it/domains/setup/history/` | JWT (G4+) | Paginated history of domain setup sessions |
| GET | `/api/v1/it/domains/setup/session/{id}/` | JWT (G4+) | Full session detail + step log |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load branch dropdown | `load` | GET `/api/v1/it/domains/setup/branches/` | `#branch-select-options` | `innerHTML` |
| Branch selection → show info card | `change` on branch dropdown | GET `.../branches/{id}/` | `#branch-info-card` | `innerHTML` |
| Domain validation on Next | `click` on Step 2 Next | POST `.../validate-domain/` | `#domain-validation-result` | `innerHTML` |
| DNS polling (Step 4) | `every 30s` | GET `.../session/{id}/verify-dns/` | `#dns-status-panel` | `innerHTML` |
| Manual DNS check | `click` on Check Now | GET `.../session/{id}/verify-dns/` | `#dns-status-panel` | `innerHTML` |
| SSL provisioning | `click` on Provision SSL | POST `.../session/{id}/provision-ssl/` | `#ssl-status-panel` | `innerHTML` |
| Go Live confirm | `click` on Confirm Go Live | POST `.../session/{id}/go-live/` | `#wizard-container` | `innerHTML` |
| Load history table | `load` | GET `/api/v1/it/domains/setup/history/` | `#setup-history-table` | `innerHTML` |
| Paginate history | `click` on page control | GET `.../history/?page=N` | `#setup-history-table` | `innerHTML` |
| Open session view drawer | `click` on View | GET `.../session/{id}/` | `#domain-drawer` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- Domain setup session stalled > 24h: IT Admin + IT Director (in-app amber + email)
- SSL certificate expiry < 30 days: IT Admin + Branch Primary Contact (email daily)
- Domain go-live completed: IT Admin + Branch Principal (in-app success + email)
- DNS verification failed after 48h: IT Admin (in-app amber + email)

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
