# 21 — Email Notification Config

- **URL:** `/group/it/notifications/email/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4) — Primary owner

---

## 1. Purpose

The Email Notification Config page manages EduForge's outbound email delivery infrastructure. While WhatsApp is the primary real-time communication channel and SMS the fallback, email serves a distinct, irreplaceable function: formal and document-heavy communications. Admission confirmation letters, fee receipts, result report cards, staff onboarding welcome emails, compliance notices, and DPDP-related privacy notifications are all delivered via email. These documents require formatting fidelity, attachment support, and a delivery record suitable for legal correspondence — requirements that WhatsApp and SMS cannot fully meet.

Email delivery in EduForge is configured at the group level exclusively. Branches do not configure their own email settings; they inherit the group email configuration and use templates from the Notification Template Library (File 22). This centralisation ensures consistent sender identity (the school group's verified domain), avoids spam classification due to multiple sender configurations, and simplifies bounce management.

The page covers five concerns. Provider configuration handles SMTP credentials or transactional email provider API keys. Domain verification ensures the sender domain has correctly published SPF, DKIM, and DMARC DNS records — without these, emails land in spam regardless of content quality. The email templates section manages the HTML and plain-text templates used for different notification types. Bounce and unsubscribe management tracks deliverability health — a bounce rate above 5% will damage the sender reputation of the group's domain. Delivery logs provide operational transparency into recent sends.

A critical design principle: the domain verification section must show each required DNS record and its current verified state, refreshable on demand. IT Admins who are not DNS experts need enough context to understand what is broken and copy-paste the correct record values to their DNS provider.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + write (all sections) | Primary operator |
| Group IT Director | G4 | Full read + write | Strategic oversight |
| Group EduForge Integration Manager | G4 | Read-only + template management | Can view; can create/edit email templates |
| Group IT Support Executive | G3 | Read-only (Delivery Logs only) | For diagnosing email delivery issues in support tickets |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Notifications → Email Config
```

### 3.2 Page Header
- **Title:** `Email Notification Configuration`
- **Subtitle:** `Provider: [SMTP / AWS SES / SendGrid] · From: [from@domain.com] · Domain Verified: [Yes / No]`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `Send Test Email` · `Re-verify Domain`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Sender domain SPF/DKIM not verified | "Sender domain '[domain]' is not fully verified. Emails are likely being delivered to spam folders. Complete DNS verification immediately." | Red (non-dismissible) |
| Bounce rate > 5% (last 7 days) | "Email bounce rate is [N]% over the last 7 days — above the 5% warning threshold. High bounce rates damage sender reputation." | Amber |
| Bounce rate > 10% | "Email bounce rate is [N]% — critically high. Email delivery to some recipients may be blocked." | Red |
| No email templates active for a critical category (e.g., Fee Receipt) | "No active email template exists for [Category]. Notifications of this type will fail silently." | Amber |
| SMTP connection test failed (last saved) | "Email provider connection failed. Outbound emails are non-functional. Check credentials." | Red (non-dismissible) |

---

## 4. KPI Summary Bar

No traditional KPI cards. Provider status and domain verification state are displayed in the page header subtitle. Bounce rate and unsubscribe rate are shown as inline metrics within Section 4.

---

## 5. Main Table — Email Templates (Section 3)

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Template Name | Text | Yes | Yes (text search) |
| Subject Line | Text (truncated to 60 chars) | No | No |
| Category | Badge (Admission / Fee / Exam / HR / General / Auth / DPDP Compliance) | No | Yes |
| HTML | Badge (Yes / No — whether template has HTML version) | No | No |
| Last Modified | Date | Yes | No |
| Actions | Preview / Edit / Test Send / Duplicate / Archive | No | No |

### 5.1 Filters
- Category: Multi-select (all template categories)
- HTML: Checkbox (HTML / Plain Text)
- Status: Checkbox (Active / Archived)

### 5.2 Search
- Template Name, Subject Line
- 300ms debounce

### 5.3 Pagination
- Server-side · 15 rows/page

---

## 6. Drawers

### 6.1 Section 1: Provider Configuration (Form Panel)

**Fields:**
- Provider Type (radio: SMTP / AWS SES / SendGrid / Mailgun / Other)
- **If SMTP:**
  - SMTP Host (text; e.g., smtp.gmail.com)
  - SMTP Port (number; e.g., 587)
  - Encryption (dropdown: TLS / SSL / None)
  - SMTP Username (text)
  - SMTP Password (masked; show/hide toggle)
- **If AWS SES:**
  - AWS Region (dropdown: ap-south-1 / us-east-1 / etc.)
  - AWS Access Key ID (text)
  - AWS Secret Access Key (masked)
- **If SendGrid / Mailgun:**
  - API Key (masked)
- **Common fields (all providers):**
  - From Email Address (required; must match verified domain; validation error: "Email domain must match verified domain")
  - From Name (text; e.g., "EduForge — [Group Name]")
  - Reply-To Address (optional)

**Send Test Email button (inline):** Sends a plain-text test email to a test address input field. Returns delivered / failed inline status.

---

### 6.2 Section 2: Domain Verification (Status Panel)

Displays the DNS verification status for the sender domain. This is read-only — the IT Admin takes action in their DNS provider's dashboard, not in EduForge.

**DNS Records Required Table:**

| Record Type | Name | Value | Status |
|---|---|---|---|
| SPF (TXT) | @ | `v=spf1 include:amazonses.com ~all` | Verified / Not Found / Mismatch |
| DKIM (CNAME) | `selector._domainkey` | `[dkim value].dkim.amazonses.com` | Verified / Not Found / Mismatch |
| DMARC (TXT) | `_dmarc` | `v=DMARC1; p=quarantine; rua=mailto:dmarc@domain` | Verified / Not Found |

- Each row shows the record type, the exact value to publish, a copy button, and the verified status (green tick / red cross / amber warning)
- **Re-verify Domain button** (top right): triggers fresh DNS lookup for all three records; button spins during check; table updates on completion

---

### 6.3 Drawer: `email-template-preview` — Preview Template
- **Trigger:** Actions → Preview
- **Width:** 560px
- **Content:** Renders the HTML template in an iframe (sandboxed) at desktop and mobile widths (toggle). Shows subject line, from name, and full HTML body with sample variable substitution (e.g., `{{student_name}}` renders as "Arjun Kumar"). Plain text version tab also available.

### 6.4 Drawer: `email-template-edit` — Edit Template
- **Trigger:** Actions → Edit
- **Width:** 560px
- **Fields:**
  - Template Name (text)
  - Subject Line (text; supports `{{variables}}`)
  - Category (dropdown)
  - HTML Body (rich-text / code editor with toggle; supports Tailwind-compatible inline styles)
  - Plain Text Body (textarea; fallback for email clients that do not render HTML)
  - Variable Reference Panel (right side of drawer): list of available `{{variables}}` by category (Student, Fee, Exam, etc.) with click-to-insert
- **Save / Save as Duplicate buttons**

### 6.5 Modal: Archive Template
- **Trigger:** Actions → Archive
- **Type:** Centered modal (400px)
- **Content:** "Archive template '[Name]'? Archived templates will no longer be sent. If this template is in active use by a notification trigger, those notifications will fail."
- **Buttons:** Confirm Archive · Cancel

### 6.6 Section 4: Bounce & Unsubscribe Management (Information + Action Panel)

**Metrics displayed:**
- Bounce Rate (last 7 days): [N]% (colour-coded — green < 2%, amber 2–5%, red > 5%)
- Hard Bounces: [N] (permanent delivery failures — invalid email addresses)
- Soft Bounces: [N] (temporary failures — full mailbox, server unavailable)
- Unsubscribes (last 30 days): [N]
- Suppression List: [N] addresses suppressed (will never receive emails)

**Actions:**
- View Suppression List: Opens 360px drawer with paginated list of suppressed emails. Each row has Remove from Suppression button (for addresses that were accidentally suppressed).
- Download Hard Bounce List (CSV): Download for manual follow-up
- Clear Soft Bounces button: Clears soft bounce counter (provider-dependent)

---

### 6.7 Section 5: Delivery Logs (Table Panel)

Most recent 100 emails sent:

| Column | Notes |
|---|---|
| To Address | Partially masked (first 2 chars + domain: ar***@gmail.com) |
| Template Used | Template name |
| Branch | Originating branch |
| Status | Badge (Sent / Delivered / Bounced / Failed / Opened) |
| Timestamp | DateTime |

Pagination: 20 rows/page.

---

## 7. Charts

No dedicated chart section. Deliverability metrics in Section 4 serve as the primary quality indicators.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Provider config saved + connection OK | "Email configuration saved. Test email sent successfully." | Success | 4s |
| Provider config saved + connection failed | "Settings saved but email connection failed. Check SMTP/API credentials." | Error | 7s |
| Domain re-verify complete (all verified) | "Domain verification complete. All DNS records verified." | Success | 4s |
| Domain re-verify complete (issues found) | "Domain verification complete. [N] record(s) have issues. Check Section 2 for details." | Warning | 5s |
| Template saved | "Email template '[Name]' saved." | Success | 3s |
| Template archived | "Template '[Name]' archived." | Warning | 3s |
| Suppression list address removed | "[email] removed from suppression list." | Success | 3s |
| Test email sent | "Test email sent to [address]. Check inbox (and spam folder)." | Info | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No email templates | "No Email Templates" | "No email templates have been created. Create the first template to begin sending formatted emails." | Create Template |
| Delivery Logs — no emails sent | "No Email Delivery Logs" | "No emails have been sent through this configuration yet." | — |
| Suppression list drawer — empty | "Suppression List is Empty" | "No email addresses are currently suppressed." | — |
| Templates filter — no results | "No Templates Match" | "No email templates match the selected category or status." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Section 1 form skeleton + Domain verification table skeleton + Templates table skeleton (8 rows) + Delivery Logs skeleton |
| Re-verify Domain button click | Button spinner; DNS status table rows shimmer then update |
| Template preview drawer open | 560px drawer skeleton; iframe renders after skeleton |
| Template edit drawer open | 560px drawer skeleton; rich-text editor loads |
| Suppression list drawer open | 360px skeleton; list rows load |
| Section save | Section Save button spinner only |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | Integration Manager (G4) | IT Support Executive (G3) |
|---|---|---|---|---|
| Section 1 (Provider Config) edit | Visible | Visible | Hidden | Hidden |
| Send Test Email | Visible | Visible | Visible | Hidden |
| Section 2 (Domain Verification) | Visible | Visible | Visible (read) | Hidden |
| Re-verify Domain button | Visible | Visible | Hidden | Hidden |
| Templates table | Visible | Visible | Visible | Hidden |
| Template Preview | Visible | Visible | Visible | Hidden |
| Template Edit / Archive | Visible | Visible | Visible | Hidden |
| Section 4 (Bounce Management) | Visible | Visible | Visible (read) | Hidden |
| Remove from Suppression | Visible | Visible | Hidden | Hidden |
| Section 5 (Delivery Logs) | Visible | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/notifications/email/config/` | JWT (G3+) | Retrieve provider config (credentials masked) |
| PATCH | `/api/v1/it/notifications/email/config/` | JWT (G4) | Update provider configuration |
| POST | `/api/v1/it/notifications/email/config/test/` | JWT (G4) | Send test email |
| GET | `/api/v1/it/notifications/email/domain-verification/` | JWT (G3+) | DNS record verification status |
| POST | `/api/v1/it/notifications/email/domain-verification/reverify/` | JWT (G4) | Trigger fresh DNS lookup for all records |
| GET | `/api/v1/it/notifications/email/templates/` | JWT (G3+) | Paginated email template list |
| GET | `/api/v1/it/notifications/email/templates/{id}/` | JWT (G3+) | Single template detail with full HTML body |
| POST | `/api/v1/it/notifications/email/templates/` | JWT (G4) | Create new email template |
| PATCH | `/api/v1/it/notifications/email/templates/{id}/` | JWT (G4) | Update template |
| POST | `/api/v1/it/notifications/email/templates/{id}/archive/` | JWT (G4) | Archive a template |
| GET | `/api/v1/it/notifications/email/bounce-stats/` | JWT (G3+) | Bounce rate, hard/soft bounces, unsubscribes |
| GET | `/api/v1/it/notifications/email/suppression/` | JWT (G4) | Paginated suppression list |
| DELETE | `/api/v1/it/notifications/email/suppression/{id}/` | JWT (G4) | Remove address from suppression list |
| GET | `/api/v1/it/notifications/email/delivery-logs/` | JWT (G3+) | Paginated email delivery log |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load provider config | `load` | GET `/api/v1/it/notifications/email/config/` | `#email-provider-section` | `innerHTML` |
| Load domain verification section | `load` | GET `/api/v1/it/notifications/email/domain-verification/` | `#domain-verify-section` | `innerHTML` |
| Load templates table | `load` | GET `/api/v1/it/notifications/email/templates/` | `#email-templates-table` | `innerHTML` |
| Load delivery logs | `load` | GET `/api/v1/it/notifications/email/delivery-logs/` | `#email-delivery-logs` | `innerHTML` |
| Re-verify domain | `click` on Re-verify | POST `/api/v1/it/notifications/email/domain-verification/reverify/` | `#domain-verify-table` | `innerHTML` |
| Filter templates | `change` | GET `/api/v1/it/notifications/email/templates/?category=...` | `#email-templates-table` | `innerHTML` |
| Search templates | `input` (300ms debounce) | GET `/api/v1/it/notifications/email/templates/?q=...` | `#email-templates-table` | `innerHTML` |
| Open preview drawer | `click` on Preview | GET `/api/v1/it/notifications/email/templates/{id}/` | `#email-template-drawer` | `innerHTML` |
| Open template preview drawer | `click` on Preview | GET `/api/v1/it/notifications/email/templates/{id}/` | `#template-drawer` | `innerHTML` |
| Open suppression list drawer | `click` on View Suppression List | GET `/api/v1/it/notifications/email/suppression/` | `#suppression-drawer` | `innerHTML` |
| Save provider config | `click` on Save | PATCH `/api/v1/it/notifications/email/config/` | `#email-provider-section` | `outerHTML` |
| Archive template confirm | `click` on Confirm Archive | POST `/api/v1/it/notifications/email/templates/{id}/archive/` | `#email-templates-table` | `innerHTML` |
| Remove from suppression | `click` on Remove | DELETE `/api/v1/it/notifications/email/suppression/{id}/` | `#suppression-list` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- Email provider connection failed: IT Admin + IT Director (in-app red non-dismissible + email) immediately
- Domain verification failed: IT Admin (in-app amber + email)
- Bounce rate > 5%: IT Admin + IT Director (in-app amber + email)
- Suppression list growth > 100 new entries/day: IT Admin (in-app amber + email)

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
