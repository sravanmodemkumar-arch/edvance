# 34 — Data Breach Incident Register

- **URL:** `/group/it/privacy/breaches/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Data Privacy Officer (Role 55, G1) — Read-only; Group IT Admin (Role 54, G4) — Full access; Group IT Director (Role 53, G4) — Full access

---

## 1. Purpose

The Data Breach Incident Register is the group's statutory record of all personal data breaches. Under DPDP Act 2023, a data breach is defined as any unauthorised access to, disclosure of, alteration, loss, or destruction of personal data. The Act mandates two key obligations when a breach occurs: first, affected data subjects must be notified; second, the Data Protection Board of India must be notified within 72 hours of the breach being discovered (for significant breaches). Failure to notify within 72 hours is itself a violation and can result in substantial penalties.

This page is therefore one of the highest-stakes pages in the entire EduForge platform. Every breach — from a staff member accidentally emailing student records to the wrong recipient, to a ransomware attack affecting a branch server, to a database misconfiguration that exposed student data publicly — must be logged here within minutes of discovery. The clock starts at discovery time, not the time of the breach occurrence.

The severity classification drives the response urgency. Severity 1 (Critical) incidents — involving large-scale exposure (>1,000 individuals), sensitive data categories (health, financial, special categories), or active ongoing compromise — trigger immediate in-app notifications to the IT Director, Data Privacy Officer, and Group Chairman. The 72-hour notification requirement applies to all Severity 1 and Severity 2 incidents. Severity 3 incidents are logged for the record but may not require Board notification depending on the nature.

The IT Director and IT Admin can create and update incidents (they are on the operational response team). The Data Privacy Officer is read-only with one exception: the File 72h Notification action, which is performed by the DPO as the legally responsible officer for regulatory notification.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Data Privacy Officer | G1 | Read-only + can file 72h notification | Regulatory notification is DPO's legal responsibility |
| Group IT Admin | G4 | Full read + create + update + file notification | Operational incident management |
| Group IT Director | G4 | Full read + create + update + file notification | Incident command; notified for Severity 1 |
| Group Cybersecurity Officer | G1 | Read-only | Incident awareness for security posture |
| All other Division F roles | — | Hidden | No access |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Data Privacy → Breach Incident Register
```

### 3.2 Page Header
- **Title:** `Data Breach Incident Register`
- **Subtitle:** `DPDP Act 2023 — 72h Board Notification Obligation · [N] Open Incidents`
- **Role Badge:** `Group Data Privacy Officer` / `Group IT Admin` / `Group IT Director`
- **Right-side controls (IT Admin / IT Director):** `+ Report New Incident` · `Export`

### 3.3 Alert Banner (conditional — ALL non-dismissible by design)

| Condition | Banner | Severity |
|---|---|---|
| 72h deadline approaching within 4h | "CRITICAL: 72-hour Board notification deadline for Breach #[N] is in [N] hours. File notification IMMEDIATELY." | Red (non-dismissible) |
| 72h deadline already passed and not filed | "OVERDUE: 72h notification for Breach #[N] was due at [datetime]. Notification has NOT been filed. File immediately — this is a DPDP Act violation." | Red (non-dismissible) |
| Severity 1 breach currently open | "SEVERITY 1 BREACH: Incident #[N] is a Critical breach affecting [N] individuals. Group Chairman and IT Director have been notified." | Red (non-dismissible) |
| Severity 2 breach open >24h without update | "Severity 2 breach #[N] has had no status update in more than 24 hours. Update incident status." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open Incidents | Count of incidents with status Open or Investigating | Red if > 0, Green if 0 | Filter by Open/Investigating |
| Severity 1 (Critical) | Open incidents classified as Severity 1 | Red if > 0, Green if 0 | Filter by Severity 1 |
| 72h Notification Due | Open incidents where 72h notification has not been filed and deadline is approaching or past | Red if > 0, Green if 0 | Filter by notification pending |
| Resolved This Month | Incidents resolved in current calendar month | Green | Filter by Resolved + current month |
| Avg Resolution Time (Days) | Average days from discovery to resolution (last 6 months) | Informational | Informational |

---

## 5. Main Table — Breach Incidents

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Incident # | Auto-generated (e.g., BRK-0001) | No | No |
| Discovery Date | Datetime | Yes | Yes (date range) |
| Breach Type | Badge (Unauthorized Access / Data Loss / Ransomware / Accidental Disclosure / System Misconfiguration / Insider Threat / Other) | Yes | Yes (multi-select) |
| Data Types Affected | Tag list (Student PII / Staff PII / Financial / Medical / Academic) | No | Yes (multi-select) |
| Individuals Affected | Number — red if >1,000 | Yes | No |
| Branch | Branch name(s) | Yes | Yes (multi-select) |
| Severity | Badge (1-Critical / 2-High / 3-Medium) — critical rows highlighted red | Yes | Yes (multi-select) |
| 72h Notification | Badge (Filed / Overdue / Pending / Not Required) — Overdue = red | Yes | Yes |
| Status | Badge (Open / Investigating / Notified / Resolved) | Yes | Yes (multi-select) |
| Actions | View / Update / File Notification | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Severity | Multi-select checkbox | 1-Critical / 2-High / 3-Medium |
| Status | Multi-select checkbox | Open / Investigating / Notified / Resolved |
| Breach Type | Multi-select checkbox | All breach types |
| 72h Notification | Multi-select | Filed / Overdue / Pending / Not Required |
| Data Types | Multi-select | Student PII / Staff PII / Financial / Medical / Academic |
| Discovery Date | Date range picker | Any range |
| Branch | Multi-select | All branches |

### 5.2 Search
- Incident # search
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

### 5.4 Default Sort
- Open Severity 1 first → Open Severity 2 → all other open → resolved/notified by date descending

---

## 6. Drawers

### 6.1 Drawer: `breach-view` — View Incident
- **Trigger:** Actions → View
- **Width:** 720px
- **Tabs:**
  - **Incident Details:** Full incident record — incident number, discovery datetime (who discovered and how), breach type, detailed description, data types affected, estimated individual count, branches affected, severity and reasoning, immediate actions taken, containment status
  - **Timeline:** Chronological action log — each update: who, when, what action, notes
  - **72h Notification:** Notification filing status, deadline countdown (or filed datetime and reference), filed notification document (download from Cloudflare R2 if filed), Board response (if received)
  - **Subject Notification:** Tracks whether affected data subjects have been notified of the breach, as required by DPDP Act 2023. Fields displayed:
    - Notification Required (Yes / No / To Be Determined — based on severity and data type)
    - Notification Status (Not Started / In Progress / Sent / Not Required)
    - Notification Method (WhatsApp / Email / Physical Letter / Portal Notice)
    - Date Notification Sent (datetime — recorded when notification dispatched)
    - Notification Content Summary (textarea — what was communicated to subjects)
    - Number of Subjects Notified (count)
    - Subjects Unable to Reach (count + reason — e.g., "Contact details outdated for 12 students")
    - Subject Responses Received (count and brief notes on any responses/complaints)
    - **Actions (IT Admin / IT Director only):** "Mark Notifications Sent" button (records date + method); "Upload Notification Evidence" button (upload notification dispatch report to Cloudflare R2)

**Audit Trail:** All incident creations, status updates, and 72h notification filings are automatically logged to the IT Audit Log with actor user ID, timestamp, and action details.

### 6.2 Drawer: `breach-create` — Report New Incident (IT Admin / IT Director)
- **Trigger:** `+ Report New Incident` button
- **Width:** 560px
- **Instruction note at top:** "Report a breach immediately. You can update details later as the investigation progresses. The 72-hour notification clock starts from the discovery date/time entered below."
- **Fields:**
  - Discovery Date (required, date picker)
  - Discovery Time (required, time picker — HH:MM format)
  - Discovered By (required, text — name/role of person who discovered)
  - How Discovered (dropdown: System Alert / User Report / External Notification / Audit / Other)
  - Breach Type (required, dropdown — all types)
  - Description (required, textarea — initial description of what happened; can be brief at this stage)
  - Data Types Affected (required, multi-select checkboxes)
  - Estimated Individuals Affected (required, number — enter best estimate; can refine later)
  - Branches Affected (required, multi-select)
  - Severity Assessment (required, radio: 1-Critical / 2-High / 3-Medium)
  - Severity Reasoning (required, textarea)
  - Immediate Actions Taken (required, textarea — what was done immediately to contain the breach)
  - Is breach still ongoing? (radio: Yes / No / Unknown)
  - Does this require 72h Board notification? (radio: Yes / No — auto-populated based on severity but overrideable)
- On submit:
  - Incident # generated (BRK-XXXX)
  - If Severity 1: IT Director and Group Chairman notified immediately via in-app notification
  - If 72h notification required: timer begins from discovery datetime

### 6.3 Drawer: `breach-update` — Update Incident Status (IT Admin / IT Director)
- **Trigger:** Actions → Update
- **Width:** 560px
- **Fields:**
  - Status (dropdown: Open → Investigating → Notified → Resolved)
  - Updated Individuals Affected (number — refine from initial estimate)
  - Investigation Notes (required, textarea)
  - Containment Measures (textarea)
  - Attachments (optional — evidence, logs, reports)
  - If moving to Resolved: Resolution summary (required, textarea — what happened, what was done, what controls were improved)

### 6.4 Drawer: `breach-notify` — File 72h Notification (DPO / IT Admin / IT Director)
- **Trigger:** Actions → File Notification
- **Width:** 560px
- **Countdown shown at top:** "72h deadline: [datetime] · [N hours remaining or N hours overdue]"
- **Fields:**
  - Notification Reference Number (from Data Protection Board — if filing externally and entering the reference here)
  - Date/Time of Filing (required, datetime picker)
  - Filing Method (dropdown: Online Portal / Physical / Email to Board)
  - Summary of notification content (required, textarea — description of breach as filed)
  - Notification Document Upload (required — upload the notification document to Cloudflare R2)
  - Board Acknowledgement Received (checkbox + datetime)
- On submit: 72h_notification_status → Filed; timestamp recorded

---

## 7. Charts

No standalone charts. Trend data shown on the Compliance Dashboard (page 31).

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Incident created | "Breach incident BRK-[N] reported. 72h notification clock is running. IT Director and DPO notified." | Warning | 6s |
| Severity 1 created | "SEVERITY 1 BREACH REPORTED (BRK-[N]). IT Director, DPO, and Group Chairman have been notified." | Error | 8s |
| Incident updated | "Incident BRK-[N] updated." | Success | 3s |
| Resolved | "Incident BRK-[N] resolved. Resolution summary logged." | Success | 4s |
| 72h notification filed | "72h Board notification filed for BRK-[N]. Filing reference recorded." | Success | 5s |
| Export triggered | "Breach incident register export prepared." | Info | 3s |
| 72h notification filing failed | Error: `Failed to file 72h notification for BRK-[N]. Verify document and Board details.` | Error | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No incidents | "No Breach Incidents Recorded" | "No personal data breach incidents have been reported. If a breach occurs, report it immediately using the button above." | + Report New Incident |
| All incidents resolved | "All Incidents Resolved" | "All recorded breach incidents have been resolved with required notifications filed." | — |
| No filter results | "No Matching Incidents" | "No incidents match the selected filters." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 5 KPI shimmer cards + table skeleton (10 rows) |
| Filter / search | Table skeleton shimmer |
| View incident drawer | Drawer spinner; Timeline and 72h Notification tabs lazy-load |
| Create incident submit | Button spinner: "Logging incident…" |
| Update incident submit | Button spinner |
| File notification submit | Button spinner: "Filing notification…" |

---

## 11. Role-Based UI Visibility

| Element | DPO (G1) | IT Admin (G4) | IT Director (G4) | Cybersecurity (G1) |
|---|---|---|---|---|
| + Report New Incident | Hidden | Visible | Visible | Hidden |
| Update Action | Hidden | Visible | Visible | Hidden |
| File Notification Action | Visible | Visible | Visible | Hidden |
| View Action | Visible | Visible | Visible | Visible |
| Investigation notes | Visible (read-only) | Visible (editable) | Visible (editable) | Visible (read-only) |
| Full incident details | Visible | Visible | Visible | Status + type only |
| 72h Notification tab | Visible | Visible | Visible | Hidden |
| Export | Hidden | Visible | Visible | Hidden |
| Severity 1 alerts | Visible | Visible | Visible | Visible |
| Resolution summary | Visible (read-only) | Visible (editable) | Visible (editable) | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/privacy/breaches/` | JWT (G1+) | Paginated breach incident list |
| POST | `/api/v1/it/privacy/breaches/` | JWT (G4) | Report new breach incident |
| GET | `/api/v1/it/privacy/breaches/{id}/` | JWT (G1+) | Full incident detail |
| PATCH | `/api/v1/it/privacy/breaches/{id}/` | JWT (G4) | Update incident |
| POST | `/api/v1/it/privacy/breaches/{id}/file-notification/` | JWT (G1 DPO + G4) | File 72h Board notification |
| GET | `/api/v1/it/privacy/breaches/kpis/` | JWT (G1+) | KPI card values |
| GET | `/api/v1/it/privacy/breaches/{id}/timeline/` | JWT (G1+) | Incident action timeline |
| GET | `/api/v1/it/privacy/breaches/export/` | JWT (G4 — IT Admin / IT Director) | Export incident register |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/privacy/breaches/kpis/` | `#kpi-bar` | `innerHTML` |
| Load breach table | `load` | GET `/api/v1/it/privacy/breaches/` | `#breach-table` | `innerHTML` |
| Apply filters | `change` on filter controls | GET `/api/v1/it/privacy/breaches/?severity=...` | `#breach-table` | `innerHTML` |
| Search by incident # | `input` (300ms debounce) | GET `/api/v1/it/privacy/breaches/?q=...` | `#breach-table` | `innerHTML` |
| Open view drawer | `click` on View | GET `/api/v1/it/privacy/breaches/{id}/` | `#breach-drawer` | `innerHTML` |
| Load timeline tab | `click` on Timeline tab | GET `/api/v1/it/privacy/breaches/{id}/timeline/` | `#drawer-tab-content` | `innerHTML` |
| Submit new incident | `click` on Submit | POST `/api/v1/it/privacy/breaches/` | `#breach-table` | `innerHTML` |
| Submit update | `click` on Save Update | PATCH `/api/v1/it/privacy/breaches/{id}/` | `#breach-drawer` | `innerHTML` |
| File notification | `click` on Confirm File | POST `/api/v1/it/privacy/breaches/{id}/file-notification/` | `#breach-drawer` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/it/privacy/breaches/?page=N` | `#breach-table` | `innerHTML` |
| Export incident register | `click` on Export | GET `/api/v1/it/privacy/breaches/export/` | `#export-result` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
