# Page 40: Security Incident Register

**URL:** `/group/it/security/incidents/`
**Roles:** Group Cybersecurity Officer (Role 56, G1) — read + recommend; Group IT Admin (Role 54, G4) — full CRUD; Group IT Director (Role 53, G4) — full CRUD
**Priority:** P0
**Division:** F — Group IT & Technology

---

## 1. Purpose

Central log and tracking system for all cybersecurity incidents across the EduForge group. An incident is any event that threatens the confidentiality, integrity, or availability of EduForge systems or student/staff data.

Incident types covered:
- **Unauthorised Access** — login from unknown IP, brute force, credential theft
- **Account Compromise** — staff account taken over by external actor
- **Ransomware** — malware encrypting systems or data
- **Data Theft** — exfiltration of student or financial records
- **Social Engineering** — manipulation of staff into taking harmful actions
- **Phishing Attacks** — targeted email/WhatsApp campaigns against branch staff
- **Other** — catch-all for novel or undefined incidents

Each incident has a severity level (1–4), affected branches, a timeline of response actions, and a resolution status. Incidents that involve personal data breaches are flagged as DPDP-notifiable and linked to the Data Breach Register (managed by the Group Data Privacy Officer, Role 55).

The Cybersecurity Officer (Role 56) can view all incidents and add recommendations, but cannot create or modify records. IT Admin (Role 54) and IT Director (Role 53) have full CRUD.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Director (Role 53, G4) | Full CRUD | Create, update, escalate, link to breach register |
| Group IT Admin (Role 54, G4) | Full CRUD | Create, update, escalate, link to breach register |
| Group Cybersecurity Officer (Role 56, G1) | Read + recommend | View all incidents; can add recommendation notes; cannot create/update status |
| Group Data Privacy Officer (Role 55, G1) | Read-only | Can view DPDP-notifiable incidents only (filtered view) |
| All other roles | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > Cybersecurity > Security Incident Register`

**Page Header:**
- Title: `Security Incident Register`
- Subtitle: `Log and track all cybersecurity incidents across the group`
- Right side: `+ Log New Incident` button (Role 53/54 only), `Export (CSV)` button

**Alert Banners:**

1. **Active Severity 1 Incident** (red, non-dismissible):
   - Condition: any incident with severity = 1 (Critical) and status ≠ Resolved/Closed
   - Text: `CRITICAL SECURITY INCIDENT ACTIVE — [Incident #] — [Type] — [Branch(es)] — Open for [X] hours. [View →]`
   - Cannot be dismissed while incident is open. Only dismissed automatically when incident is resolved.

2. **Incident Stale — No Update >72h** (red, non-dismissible):
   - Condition: any open incident with last updated timestamp > 72 hours ago
   - Text: `Incident [#] has had no update in [X] hours. Assign a handler and add an update immediately.`

3. **DPDP Notifiable Incident** (amber, dismissible per session):
   - Condition: any open incident with dpdp_notifiable = Yes
   - Text: `[X] incident(s) are flagged as DPDP-notifiable. Review breach notification obligations under DPDP Act 2023.`

---

## 4. KPI Summary Bar

Five KPI cards in a 5-column responsive grid.

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Total Open | Incidents with status in (Open, Investigating, Contained) | Large number, red if > 0 |
| 2 | Severity 1 Critical | Open incidents where severity = 1 | Number, red badge always |
| 3 | Severity 2 High | Open incidents where severity = 2 | Number, orange badge |
| 4 | Resolved This Month | Incidents resolved in current calendar month | Number, green |
| 5 | Avg Resolution Time | Average hours from detected_date to resolved_date for incidents resolved this month | Hours value, amber if > 48h |

---

## 5. Main Table — Incident Register

**Table Title:** `Security Incident Register`

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Incident # | Text | Auto-generated: `INC-YYYY-NNN` format |
| Incident Type | Badge | Unauthorized Access / Phishing / Ransomware / Account Compromise / Social Engineering / Other |
| Severity | Badge | 1-Critical (red) / 2-High (orange) / 3-Medium (amber) / 4-Low (grey) |
| Branch(es) Affected | Text | Comma-separated branch names; truncated at 2 with `+N more` tooltip |
| Detected Date | Date | Date/time the incident was first detected |
| Status | Badge | Open (red) / Investigating (orange) / Contained (amber) / Resolved (green) / Closed (grey) |
| DPDP Notifiable | Badge | Yes (red) / No (green) / Unknown (grey) |
| Assigned To | Text | Name of incident handler; `Unassigned` (red) if not yet assigned |
| Actions | Buttons | `View` / `Update` (Role 54/53) / `Escalate` (Role 54/53) / `Link to Breach` (Role 54/53) |

### Filters

- **Incident Type:** All / Unauthorized Access / Phishing / Ransomware / Account Compromise / Social Engineering / Other
- **Severity:** All / 1-Critical / 2-High / 3-Medium / 4-Low
- **Status:** All / Open / Investigating / Contained / Resolved / Closed
- **Branch:** Multi-select dropdown
- **DPDP Notifiable:** All / Yes / No / Unknown
- **Assigned To:** Dropdown of IT staff
- **Date Range:** Detected date from/to

### Search

Search on Incident #, type description, or affected branch name. `hx-trigger="keyup changed delay:400ms"`, targets `#incident-table`.

### Pagination

Server-side, 20 rows per page. `hx-get="/group/it/security/incidents/table/?page=N"`, targets `#incident-table`.

### Sorting

Sortable: Severity, Detected Date, Status. Default sort: Severity ascending (Critical first), then Detected Date descending.

---

## 6. Drawers

### A. Create Incident Drawer (640px, right-side — Role 53/54 only)

Triggered by `+ Log New Incident` button.

**Drawer Header:** `Log New Security Incident`

**Fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Incident Type | Dropdown | Yes | Unauthorized Access / Phishing / Ransomware / Account Compromise / Social Engineering / Other |
| Severity | Dropdown | Yes | 1-Critical / 2-High / 3-Medium / 4-Low |
| Incident Title | Text input | Yes | Short descriptive title |
| Description | Textarea | Yes | Detailed description of what happened |
| Branch(es) Affected | Multi-select | Yes | Select all affected branches |
| Detected Date/Time | DateTime | Yes | When incident was first detected |
| Detection Method | Dropdown | Yes | Automated monitoring / Staff report / External notification / Security scan / Vendor alert |
| Initial Impact Assessment | Textarea | Yes | What systems/data may be affected |
| DPDP Notifiable | Dropdown | Yes | Yes / No / Unknown (review needed) |
| Assigned Handler | Dropdown | No | IT staff member responsible; leave blank if unassigned |
| Initial Actions Taken | Textarea | No | Any immediate response steps already taken |

**Footer:** `Log Incident` (red — signals urgency) / `Cancel`

On submit: `hx-post="/api/v1/it/security/incidents/"`. Table refreshes. Toast: `Incident [INC-YYYY-NNN] logged. Handler notified.`

**Audit:** Incident creation is logged to the IT Audit Log. If Severity = 1 (Critical), IT Director (Role 53) is notified immediately via in-app alert + email.

---

### B. Update Incident Drawer (640px, right-side — Role 53/54 only)

Triggered by `Update` button in table.

**Two-tab layout:**
- Tab 1: `Add Timeline Entry`
- Tab 2: `Update Incident Details`

**Tab 1 — Add Timeline Entry:**

| Field | Type | Required |
|-------|------|----------|
| Update Type | Dropdown | Yes — Progress Update / Status Change / New Evidence / Containment Action / Resolution / Escalation |
| Status (new) | Dropdown | Yes — Open / Investigating / Contained / Resolved / Closed |
| Update Details | Textarea | Yes |
| DPDP Notifiable (revised) | Dropdown | No |

**Tab 2 — Update Incident Details:**
- Severity (editable)
- Assigned Handler (editable)
- Additional Branches Affected (add to existing list)
- Resolution Summary (if status = Resolved)
- Root Cause (if status = Resolved)

**Footer:** `Save Update` / `Cancel`

On submit: `hx-post="/api/v1/it/security/incidents/{id}/updates/"`. Toast: `Incident [#] updated. Timeline entry added.`

---

### C. Incident Detail Drawer (720px, right-side — all permitted roles)

Triggered by `View` button. Read-only for Role 56; Role 56 has additional `Add Recommendation` button.

**Drawer Header:** `[Incident #] — [Type] — [Severity badge]`

**Sections:**

**Summary Section:**
- Status badge, DPDP Notifiable badge
- Branch(es) affected
- Detected: [date/time]
- Assigned to: [handler]
- Opened by: [actor]

**Impact Assessment:**
- Initial impact description (rendered markdown)

**Detection & Cause:**
- Detection method
- Root cause (if resolved)

**Timeline (chronological):**
- Each entry: timestamp, actor, type, details — displayed as vertical timeline
- Latest entry at top

**Linked Breach Report (if DPDP-notifiable):**
- Shows linked breach report # with link → navigates to breach register (Role 55 page)

**Add Recommendation (Role 56 only — within view drawer):**
- Textarea: `Your recommendation to IT Admin/Director`
- `Submit Recommendation` button → `hx-post="/api/v1/it/security/incidents/{id}/recommendations/"`

**Footer:** `Close` | `Update Incident` (Role 54/53 only) | `Escalate` (Role 54/53 only) | `Link to Breach` (Role 54/53 only)

---

### D. Escalate Drawer (440px, right-side — Role 54/53 only)

**Fields:**
- Escalate To: Group IT Director (if current handler is IT Admin) / External Security Firm / CERT-In / Management Board
- Escalation Reason (textarea, required)
- Priority justification (textarea)
- Notify via: Email / WhatsApp

**Footer:** `Escalate` / `Cancel`

On submit: Toast: `Incident [#] escalated to [target].`

**Notifications:** Escalation target receives in-app notification + email immediately upon escalation submission.

---

### E. Link to Breach Register Drawer (440px — Role 54/53 only)

**Fields:**
- Link to Existing Breach Report (search/select) OR Create New Breach Report
- Linkage Reason (textarea)

**Footer:** `Link Breach Record` / `Cancel`

---

## 7. Charts

No dedicated chart section on this page (charts are on the Cybersecurity Dashboard, Page 38). However, the page includes a mini inline summary strip below the KPI bar:

**Incident Type Distribution (current month):** Small horizontal bar showing incident count by type. Read-only. Data from `/api/v1/it/security/incidents/summary/type-breakdown/`.

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Incident logged | Success: `Incident [INC-YYYY-NNN] logged. Assigned handler notified.` |
| Incident updated | Success: `Incident [#] updated. Timeline entry added.` |
| Escalation sent | Success: `Incident [#] escalated to [target].` |
| Breach linked | Success: `Incident [#] linked to Breach Report [BR-YYYY-NNN].` |
| Recommendation added (Role 56) | Success: `Your recommendation has been submitted to IT Admin.` |
| Validation error | Error: `Please complete all required fields.` |
| Severity 1 auto-alert | System alert: `CRITICAL: Severity 1 incident logged. IT Director notified automatically.` |
| Export complete | Info: `Incident register exported.` |

---

**Audit Trail:** All incident lifecycle actions (create, update, escalate, resolve, close) are logged to the IT Audit Log with actor user ID, timestamp, incident ID, and action details.

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No incidents ever logged | Icon + `No security incidents have been logged. Use "Log New Incident" to record incidents when they occur.` |
| No incidents match filters | `No incidents match your filters. Try adjusting the date range or severity.` |
| No timeline entries yet | `No timeline entries yet. Add the first update using "Update Incident".` |
| No open incidents (all resolved) | Green banner: `All logged incidents are resolved. Current security posture: Clear.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI bar | 5 skeleton shimmer cards |
| Incident table | 5 skeleton rows with shimmer |
| Incident detail drawer | Spinner while loading timeline; sections appear progressively |
| Timeline in drawer | Spinner while fetching update history |
| Submit buttons in drawers | Shows `Saving...` text + disabled state during `hx-request` |

---

## 11. Role-Based UI Visibility

| UI Element | Role 56 (G1) | Role 54 (G4) | Role 53 (G4) |
|------------|-------------|-------------|-------------|
| Log New Incident button | Hidden | Visible | Visible |
| Update button in table | Hidden | Visible | Visible |
| Escalate button | Hidden | Visible | Visible |
| Link to Breach button | Hidden | Visible | Visible |
| View button | Visible | Visible | Visible |
| Add Recommendation (in detail) | Visible | Hidden | Hidden |
| DPDP filter | Visible | Visible | Visible |
| Export CSV | Hidden | Visible | Visible |
| Delete incident | Never shown | Never shown | Never shown (audit integrity) |

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/security/incidents/` | Fetch incidents (paginated, filtered) |
| POST | `/api/v1/it/security/incidents/` | Create new incident (Role 54/53) |
| GET | `/api/v1/it/security/incidents/{id}/` | Fetch incident detail |
| PUT | `/api/v1/it/security/incidents/{id}/` | Update incident header fields |
| POST | `/api/v1/it/security/incidents/{id}/updates/` | Add timeline entry |
| POST | `/api/v1/it/security/incidents/{id}/escalate/` | Escalate incident |
| POST | `/api/v1/it/security/incidents/{id}/link-breach/` | Link to breach register |
| POST | `/api/v1/it/security/incidents/{id}/recommendations/` | Add recommendation (Role 56) |
| GET | `/api/v1/it/security/incidents/kpis/` | Fetch KPI counts |
| GET | `/api/v1/it/security/incidents/summary/type-breakdown/` | Incident type distribution |
| GET | `/api/v1/it/security/incidents/export/csv/` | Export CSV |
| GET | `/api/v1/it/security/incidents/{id}/recommendations/` | JWT (G1+) | Fetch recommendations added by Cybersecurity Officer |

---

## 13. HTMX Patterns

```html
<!-- Incident table with filters -->
<div id="incident-table"
     hx-get="/group/it/security/incidents/table/"
     hx-trigger="load"
     hx-target="#incident-table"
     hx-include="#incident-filter-form">
</div>

<!-- Log new incident drawer -->
<button hx-get="/group/it/security/incidents/create-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  + Log New Incident
</button>

<!-- Create incident submit -->
<form id="create-incident-form"
      hx-post="/api/v1/it/security/incidents/"
      hx-target="#incident-table"
      hx-swap="outerHTML"
      hx-on::after-request="closeDrawer(); refreshKPIs()">
  <!-- fields -->
  <button type="submit">Log Incident</button>
</form>

<!-- View incident detail -->
<button hx-get="/group/it/security/incidents/{{ incident.id }}/detail/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  View
</button>

<!-- Add timeline entry -->
<form hx-post="/api/v1/it/security/incidents/{{ incident.id }}/updates/"
      hx-target="#incident-timeline"
      hx-swap="outerHTML">
  <button type="submit">Save Update</button>
</form>

<!-- Add recommendation (Role 56) -->
<form hx-post="/api/v1/it/security/incidents/{{ incident.id }}/recommendations/"
      hx-target="#recommendation-section"
      hx-swap="innerHTML">
  <button type="submit">Submit Recommendation</button>
</form>

<!-- KPI refresh after incident creation -->
<div id="incident-kpis"
     hx-get="/group/it/security/incidents/kpis/"
     hx-trigger="load, incidentCreated from:body"
     hx-target="#incident-kpis">
</div>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
