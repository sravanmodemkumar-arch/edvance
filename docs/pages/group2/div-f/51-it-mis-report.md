# Page 51: IT MIS Report Builder

**URL:** `/group/it/reports/mis/`
**Role:** Group IT Director (Role 53, G4)
**Priority:** P1
**Division:** F — Group IT & Technology

---

## 1. Purpose

Monthly IT Management Information System (MIS) report builder. The IT Director compiles data from all IT sub-functions — support tickets, system health, integrations, security posture, user management, assets, and licenses — into a consolidated monthly report for the Group CEO, Chairman, and Board.

The report replaces the need for the IT Director to manually assemble metrics from multiple pages into a presentation or spreadsheet. It auto-populates section data from live PostgreSQL queries and allows the IT Director to:
- Select which sections to include in the report
- Preview the report before publishing
- Customise the distribution list
- Publish the report (which triggers email dispatch to stakeholders)
- Download past reports as PDF

**Report Audience:** Group CEO, Chairman, Group CFO (optional), Board members (optional)

**Report Cadence:** Monthly — typically generated in the first week of each month for the previous month's data.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Director (Role 53, G4) | Full access | Build, preview, publish, re-send reports |
| Group IT Admin (Role 54, G4) | View history only | Can view past published reports; cannot build or publish |
| All other roles | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > Reports > IT MIS Report`

**Page Header:**
- Title: `IT MIS Report Builder`
- Subtitle: `Monthly consolidated IT report for Group leadership`
- Right side: `+ Build New Report` button

**Page Structure:**

This page has two views:

**View 1: Report History (default)** — shows the history table of past reports
**View 2: Report Builder (active when building)** — three-pane layout

---

### View 1: Report History

**Table Title:** `Published MIS Reports`

Columns:
| Column | Notes |
|--------|-------|
| Month | e.g., `February 2026` |
| Sections Included | Count + brief list: `8 sections (System Health, Support, Security...)` |
| Published Date | Date/time published |
| Sent To | `CEO, Chairman + 2 others` (truncated) |
| Status | `Published` (green) / `Draft` (grey) |
| Actions | `View` / `Re-send` / `Download PDF` |

Pagination: Server-side, 12 rows per page (one year per page visually).

---

### View 2: Report Builder (Three-Pane Layout)

**Layout:** Full-width, three equal-ish columns.

**Left Pane (280px): Sections Checklist**
- Report Month selector (dropdown — current month default)
- Checklist of all available sections (checkboxes):
  - [ ] Executive Summary *(auto-generated)*
  - [ ] System Health Summary
  - [ ] Support Ticket Summary
  - [ ] Security Summary
  - [ ] Integration Health Summary
  - [ ] Privacy/DPDP Compliance Summary
  - [ ] User Management Summary
  - [ ] Assets & Licenses Summary
- `Select All` / `Deselect All` links
- `Generate Preview` button (primary)

**Middle Pane (flex-grow): Report Preview**
- Renders selected sections as a formatted document preview
- Header: EduForge Group IT — MIS Report — [Month Year]
- Each section renders with auto-populated data from the selected month
- Sections appear in the order listed in the checklist
- Preview updates when sections are toggled or `Generate Preview` is clicked
- Export button: `Download as PDF` (top right of preview pane)

**Right Pane (280px): Distribution Settings**
- **Always include:**
  - Group CEO (pre-checked, cannot uncheck)
  - Group Chairman (pre-checked, cannot uncheck)
- **Optional add:**
  - Group CFO (toggle)
  - Board Members (toggle — sends to all board member emails on file)
  - Other: add email addresses (text input, comma-separated)
- **Cover note (optional):**
  - Textarea for a brief personal note from the IT Director (appears at top of email)
- `Publish & Send Report` button (primary, green)
- `Save as Draft` button (secondary)

---

## 4. KPI Summary Bar

No traditional KPI bar — this is a report-builder interface, not a data monitoring page.

**Inline stats above the sections checklist (in builder mode):**
- Report Month: `[Selected Month]`
- Sections selected: `[X] of 8`
- Last published: `[Date]` or `Never published`

---

## 5. Report Sections — Auto-Generated Content

Each section pulls data from PostgreSQL for the selected report month.

### Section 1: Executive Summary (auto-generated)
- 3–5 bullet points summarising the month's IT highlights
- Auto-generated from KPI data: system uptime %, support tickets resolved, open incidents, security score, active users
- IT Director can edit the auto-generated text before publishing

### Section 2: System Health Summary
- Overall uptime % per service (table)
- Any downtime incidents in the month
- Response time averages
- Data from: `service_health_checks` table

### Section 3: Support Ticket Summary
- Total tickets raised, resolved, SLA compliance %, avg resolution time
- Top 3 ticket categories
- Branch with most tickets
- Open tickets carried forward
- Data from: `support_tickets` table

### Section 4: Security Summary
- Security score (group average)
- Open incidents count
- Phishing simulation results (if any campaigns ran in month)
- Security training completion %
- Vulnerabilities status (open critical/high)
- Data from: incident_register, phishing_campaigns, training_records, vulnerability_register tables

### Section 5: Integration Health Summary
- Active integrations count
- Integration errors in month (count + error rate %)
- API calls processed
- SSO login count
- Data from: `integration_logs` table

### Section 6: Privacy / DPDP Compliance Summary
- DSR requests received and resolved
- Data breach incidents (if any) — DPDP notifiable
- Consent records updated
- Data from: privacy-related tables (managed by Role 55 pages)

### Section 7: User Management Summary
- New accounts created (by role category)
- Accounts deactivated
- Role changes (upgrades/downgrades)
- Provisioning requests completed
- Access reviews completed
- Data from: user_accounts, access_review tables

### Section 8: Assets & Licenses Summary
- Total active assets (by category — summary counts)
- Warranties expiring next 90 days
- Active software licenses
- Licenses renewed in month
- License cost summary (total annual spend)
- Data from: asset_register, license_register tables

---

## 6. Drawers

**Note:** Published reports cannot be edited. To create a new version, use "+ Build New Report". Draft configurations auto-expire after 30 days of inactivity.

### A. View Past Report Drawer (720px, right-side)

Triggered by `View` in history table.

**Content:**
- Rendered version of the report (same format as builder preview)
- Shows all sections included in that report
- Metadata: Published date, sent to, sent by

**Footer:** `Close` | `Re-send` | `Download PDF`

---

### B. Re-send Report Drawer (440px)

Triggered by `Re-send` button.

**Fields:**
- Report: [Month Year] (read-only)
- Current recipients: [list from original send] (read-only)
- Add additional recipients: email input (optional)
- Cover note: textarea (optional)

**Footer:** `Re-send Report` / `Cancel`

On submit: `hx-post="/api/v1/it/reports/mis/{id}/resend/"`. Toast: `Report re-sent to [X] recipients.`

---

## 7. Charts

No standalone charts on this page. Charts are embedded within the report preview itself (rendered as static image snapshots when the PDF is generated):

- System Health: uptime bar chart (inline in Section 2 preview)
- Support: ticket volume trend mini-chart (inline in Section 3)
- Security: security score trend mini-chart (inline in Section 4)

These charts render as live HTML in the preview pane and are converted to static images during PDF generation.

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Report preview generated | Info: `Preview generated for [Month]. Review sections before publishing.` |
| Report saved as draft | Info: `Report draft saved.` |
| Report published and sent | Success: `IT MIS Report for [Month] published and sent to [X] recipients.` |
| Re-send complete | Success: `Report re-sent to [X] recipients.` |
| PDF download | Info: `Preparing PDF download...` |
| PDF ready | Success: `PDF ready. Download starting.` |
| Validation — no sections selected | Error: `Please select at least one section before generating the report.` |
| Section data unavailable | Warning: `No data available for [Section Name] in the selected month. Section will show "No data available".` |
| Preview generation failed | Error: `Failed to generate report preview. Please try again.` | Error | 5s |
| Report publish failed | Error: `Failed to publish report. Check email recipients and try again.` | Error | 5s |
| Report resend failed | Error: `Failed to re-send report. Please try again.` | Error | 5s |

---

**Audit Trail:** Report publish and resend actions are logged to the IT Audit Log with actor, timestamp, recipients, and sections included.

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No past reports | `No reports published yet. Build your first IT MIS report using "+ Build New Report".` |
| Section has no data for selected month | Section in preview shows: `No data available for [Month]. Data may not have been recorded for this period.` |
| Preview not yet generated | Middle pane: `Select sections and click "Generate Preview" to see the report.` |
| Distribution list empty | Warning in right pane: `CEO and Chairman are always included. Add optional recipients as needed.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| Report history table | 5 skeleton rows |
| Preview pane (generating) | Full pane spinner with `Compiling report data...` message |
| Each section within preview | Sections load progressively with skeleton loaders per section |
| PDF generation | Progress indicator: `Generating PDF (this may take 10–15 seconds)...` |
| Publish button | `Publishing...` text + disabled; resolves when email dispatch confirmed |
| View past report drawer | Spinner then full report renders |

---

## 11. Role-Based UI Visibility

| UI Element | Role 53 (G4) | Role 54 (G4) |
|------------|-------------|-------------|
| Build New Report button | Visible | Hidden |
| Sections checklist | Visible | Hidden |
| Distribution settings | Visible | Hidden |
| Generate Preview | Visible | Hidden |
| Publish & Send | Visible | Hidden |
| Save as Draft | Visible | Hidden |
| Report History table | Visible | Visible |
| View past report | Visible | Visible |
| Re-send button | Visible | Hidden |
| Download PDF | Visible | Visible |
| Edit executive summary text | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/reports/mis/` | Fetch report history (paginated) |
| POST | `/api/v1/it/reports/mis/preview/` | Generate report preview for selected sections/month |
| POST | `/api/v1/it/reports/mis/` | Save report as draft |
| POST | `/api/v1/it/reports/mis/{id}/publish/` | Publish and send report |
| POST | `/api/v1/it/reports/mis/{id}/resend/` | Re-send published report |
| GET | `/api/v1/it/reports/mis/{id}/` | Fetch past report content |
| GET | `/api/v1/it/reports/mis/{id}/pdf/` | Generate and return PDF |
| GET | `/api/v1/it/reports/mis/section-data/{section}/` | Fetch auto-populated section data for a month |

**Section Data Query Parameter:** `month=YYYY-MM`

---

## 13. HTMX Patterns

```html
<!-- Report history table -->
<div id="report-history-table"
     hx-get="/group/it/reports/mis/history/"
     hx-trigger="load"
     hx-target="#report-history-table">
</div>

<!-- Section toggle — update preview on checkbox change -->
<input type="checkbox" name="section" value="system_health"
       hx-post="/group/it/reports/mis/preview/"
       hx-trigger="change"
       hx-target="#report-preview"
       hx-swap="innerHTML"
       hx-include="#report-builder-form"
       hx-indicator="#preview-loader" />

<!-- Generate Preview button -->
<button hx-post="/group/it/reports/mis/preview/"
        hx-target="#report-preview"
        hx-swap="innerHTML"
        hx-include="#report-builder-form"
        hx-indicator="#preview-loader">
  Generate Preview
</button>

<!-- Preview pane -->
<div id="report-preview" class="flex-grow border rounded p-4 overflow-y-auto">
  <div id="preview-loader" class="htmx-indicator text-center py-8">
    <span>Compiling report data...</span>
  </div>
</div>

<!-- Save as draft -->
<form hx-post="/api/v1/it/reports/mis/"
      hx-include="#report-builder-form"
      hx-target="#report-history-table"
      hx-swap="outerHTML">
  <button type="submit" name="action" value="draft">Save as Draft</button>
</form>

<!-- Publish and send -->
<form hx-post="/api/v1/it/reports/mis/"
      hx-include="#report-builder-form"
      hx-target="#report-history-table"
      hx-swap="outerHTML"
      hx-indicator="#publish-loader"
      hx-confirm="Publish this report and send to all selected recipients?">
  <button type="submit" name="action" value="publish">Publish & Send Report</button>
</form>

<!-- View past report -->
<button hx-get="/group/it/reports/mis/{{ report.id }}/view/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  View
</button>
```

| Report month selector change | `change` on month select | POST `/group/it/reports/mis/preview/` | `#report-preview` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
