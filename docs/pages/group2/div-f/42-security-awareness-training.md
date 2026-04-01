# Page 42: Security Awareness Training

**URL:** `/group/it/security/training/`
**Roles:** Group Cybersecurity Officer (Role 56, G1) — read + recommend; Group IT Admin (Role 54, G4) — manage; Group Training & Development Manager — view only
**Priority:** P1
**Division:** F — Group IT & Technology

---

## 1. Purpose

Track mandatory security awareness training completion for all staff members who have EduForge access across the group. Security awareness training ensures staff understand their responsibilities in protecting student data, preventing cyber incidents, and complying with the DPDP Act 2023.

**Mandatory Training Modules (all staff with EduForge access must complete annually):**
1. Password Hygiene — strong passwords, password managers, no sharing
2. Phishing Awareness — recognising and reporting phishing attempts
3. Data Handling — handling student personal data securely, least privilege access
4. Social Engineering — recognising manipulation tactics used against staff
5. DPDP Basics — understanding obligations under the Digital Personal Data Protection Act 2023

**Policy:**
- All staff with G1+ EduForge access must complete all 5 mandatory modules within 30 days of account creation
- Re-certification required annually (within 12 months of last completion)
- Branches are considered compliant if ≥80% of their staff hold current training
- Group-wide compliance target: 90%

The Cybersecurity Officer (Role 56, G1) monitors completion rates and recommends actions. The IT Admin (Role 54, G4) manages training assignments, sends reminders, and can manually mark exceptions. The Training & Development Manager role can view the page to coordinate with HR-led training programmes.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Admin (Role 54, G4) | Full management | View, assign, send reminders, mark exceptions |
| Group IT Director (Role 53, G4) | Read + export | View all data |
| Group Cybersecurity Officer (Role 56, G1) | Read + recommend | View with masked staff names; add recommendations |
| Group Training & Dev Manager | View only | Read-only access — view completion rates by branch/role |
| All other roles | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > Cybersecurity > Security Awareness Training`

**Page Header:**
- Title: `Security Awareness Training`
- Subtitle: `Mandatory security training completion tracking for all EduForge staff`
- Right side: `Export Training Report (CSV)` button (Role 54/53) | `Send Bulk Reminder` button (Role 54)

**Alert Banners:**

1. **Group Completion Below Threshold** (amber, dismissible per session):
   - Condition: group-wide overall completion rate < 80%
   - Text: `Group security training completion is [X]% — below the 80% mandatory threshold. [X] staff overdue across [Y] branches.`

2. **New Staff Untrained** (amber, dismissible per session):
   - Condition: staff accounts created >30 days ago with 0 modules completed
   - Text: `[X] staff members joined more than 30 days ago but have not started mandatory security training.`

3. **Annual Re-certification Overdue** (amber, dismissible per session):
   - Condition: staff whose training expired > 30 days ago
   - Text: `[X] staff members have overdue annual re-certification. Their access remains active but is at policy risk.`

---

## 4. KPI Summary Bar

Four KPI cards in a 4-column grid.

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Overall Completion Rate % | staff_with_all_current_modules / total_staff_with_access × 100 | % with ring — red < 80%, amber 80–89%, green ≥ 90% |
| 2 | Overdue (>1 year since training) | Count where last_training_date < today - 365 days | Number — red if > 0 |
| 3 | Completed This Month | Count who completed all required modules in current calendar month | Number, green |
| 4 | Branches at 100% | Count of branches where all staff have current training | Number out of total branches |

---

## 5. Main Table — Staff Training Status

**Table Title:** `Staff Training Status`
**Description:** One row per staff member with EduForge access.

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Name | Text | Masked format `J*** D***` for Role 56; full name for Role 54/53 |
| Branch | Text | Branch name |
| Role Category | Badge | Academic / Administrative / Finance / Operations / IT / Management |
| Modules Completed / Total | Progress | e.g., `3/5` with mini progress bar |
| Last Training Date | Date | Most recent module completion date; `Never` if no modules |
| Next Due Date | Date | next_due = last_training_date + 365 days; `Overdue` (red) if past due |
| Status | Badge | Current (green) / Overdue (red) / Never Trained (red) / In Progress (amber) |
| Actions | Buttons | `View Details` / `Send Reminder` (Role 54) |

### Filters

- **Branch:** Multi-select dropdown
- **Role Category:** All / Academic / Administrative / Finance / Operations / IT / Management
- **Status:** All / Current / Overdue / Never Trained / In Progress
- **Due Date Range:** From / To date picker
- **Module:** Filter by staff missing a specific module (Dropdown: all 5 module names)

### Search

Search on name (masked for Role 56 — searches underlying data, returns masked results). `hx-trigger="keyup changed delay:400ms"`, targets `#training-table`.

### Pagination

Server-side, 25 rows per page. `hx-get="/group/it/security/training/table/?page=N"`, targets `#training-table`.

### Sorting

Sortable: Name, Branch, Status, Next Due Date, Modules Completed %. Default sort: Status (Never Trained first, then Overdue, then In Progress, then Current).

---

## 6. Drawers

### A. View Training Record Drawer (560px, right-side — all roles)

Triggered by `View Details` button. Read-only.

**Drawer Header:** `[Masked Name / Full Name] — Training Record`

**Summary:**
- Staff ID (masked for Role 56)
- Branch, Role Category
- Overall Status badge
- Completion: X/5 modules (progress bar)
- Last Training Date, Next Due Date

**Module Completion Table:**

| Module | Status | Completion Date | Quiz Score | Certificate |
|--------|--------|-----------------|------------|-------------|
| Password Hygiene | Completed | 2025-08-12 | 92% | Download |
| Phishing Awareness | Completed | 2025-08-12 | 88% | Download |
| Data Handling | Completed | 2025-08-15 | 95% | Download |
| Social Engineering | In Progress | — | — | — |
| DPDP Basics | Not Started | — | — | — |

**Certificates:** Download links point to Cloudflare R2 signed URLs (time-limited). Role 56 cannot download individual certificates (privacy — no staff PII).

**Training History (chronological):**
- Previous completion cycles listed (year, completion date, overall score)

**Add Exception Note (Role 54 only):**
- Reason for exemption (e.g., long-term leave) + Apply Exception button

**Audit:** Exceptions are logged to the IT Audit Log with reason and actor.

**Training Record Lifecycle:** Training records are immutable for audit purposes. Exceptions cannot be deleted — they can only be superseded by new exceptions.

**Footer:** `Close` | `Send Reminder` (Role 54 only)

---

### B. Send Reminder Drawer (440px, right-side — Role 54 only)

Triggered by `Send Reminder` button in table or `Send Bulk Reminder` from header.

**For single staff member:**
- Displays name (full — Role 54 view), branch, status, modules outstanding
- Channel: WhatsApp / SMS / Both
- Custom message (optional textarea — pre-filled with default reminder text)

**For bulk reminder (multiple overdue staff):**
- Filter: Branch (optional), Status = Overdue/Never Trained
- Shows count: `[X] staff members will receive this reminder`
- Channel selection
- Custom message (optional)

**Footer:** `Send Reminder(s)` / `Cancel`

On submit: `hx-post="/api/v1/it/security/training/reminders/"`. Toast: `Reminder sent to [X] staff member(s).`

---

## 7. Charts

Three charts below the main table, responsive 2-column grid (first chart full width, second and third side by side).

### Chart 1: Completion Rate by Branch (Full Width)
- **Type:** Horizontal bar chart
- **Y-axis:** Branch names
- **X-axis:** Completion % (0–100%)
- **Colour:** Green ≥ 80%, amber 60–79%, red < 60%
- **Reference line:** 80% threshold (dashed)
- **Purpose:** Identify branches requiring immediate intervention
- **Data endpoint:** `/api/v1/it/security/training/charts/by-branch/`

### Chart 2: Training Completion Trend (12 Months)
- **Type:** Line chart (2 series)
- **Series:** Overall completion % (solid), Target 90% (dashed reference)
- **X-axis:** Last 12 months
- **Y-axis:** Completion % (0–100%)
- **Purpose:** Track whether group-wide compliance is improving over time
- **Data endpoint:** `/api/v1/it/security/training/charts/trend/`

### Chart 3: Module-wise Completion Rate
- **Type:** Horizontal bar chart
- **Y-axis:** Module names (5 modules)
- **X-axis:** Completion % (0–100%)
- **Colour:** Green ≥ 80%, amber 60–79%, red < 60%
- **Purpose:** Identify which specific modules have the lowest completion — informs training prioritisation and reminder targeting
- **Data endpoint:** `/api/v1/it/security/training/charts/by-module/`

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Reminder sent (single) | Success: `Security training reminder sent to [Name/Masked] via [channel].` |
| Bulk reminder sent | Success: `Reminder sent to [X] staff members.` |
| Exception applied | Success: `Training exception recorded for [Name]. Reason logged.` |
| Export initiated | Info: `Generating training report — please wait.` |
| Recommendation submitted (Role 56) | Success: `Recommendation submitted to IT Admin.` |
| Reminder failed | Error: `Failed to send reminder to [X] staff. Check contact details.` |
| Exception saved | Success: `Exception saved for [staff member].` |

---

**Audit Trail:** All training module assignments, reminder sends, exception grants, and completion records are logged to the IT Audit Log.

**Notifications for Critical Events:**
- Training deadline approaching (< 7 days) and staff incomplete: Individual staff (WhatsApp/email reminder — channel per notification config)
- Training overdue (deadline passed): Branch Principal (email) + Cybersecurity Officer (in-app amber)
- Training completion rate < 70% group-wide: Cybersecurity Officer (in-app amber + email) + IT Admin (email)

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No staff with EduForge access | Icon + `No staff accounts found. Training records appear once staff are provisioned.` |
| No staff match filters | `No staff members match the selected filters. Try adjusting branch or status.` |
| All staff current | Green success state: `All staff training is current. Group compliance: 100%.` |
| No training records for a staff member | In view drawer: `This staff member has not started any training modules.` |
| Chart insufficient data | `Insufficient data for trend. Check back after training records are recorded.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI bar | 4 skeleton shimmer cards |
| Training table | 6 skeleton rows with shimmer |
| View Training Record drawer | Spinner then progressive section render |
| Module table (in drawer) | 5 skeleton rows |
| Charts | Spinner in chart container |
| Send Reminder button | `Sending...` text + disabled state |
| Bulk reminder preview | Spinner while fetching count |

---

## 11. Role-Based UI Visibility

| UI Element | Role 56 (G1) | Role 54 (G4) | Role 53 (G4) | Training Mgr |
|------------|-------------|-------------|-------------|------------|
| Staff names | Masked | Full names | Full names | Full names |
| View Details button | Visible | Visible | Visible | Visible |
| Send Reminder button | Hidden | Visible | Hidden | Hidden |
| Send Bulk Reminder | Hidden | Visible | Hidden | Hidden |
| Add Exception | Hidden | Visible | Hidden | Hidden |
| Certificate Download | Hidden | Visible | Visible | Hidden |
| Export CSV | Hidden | Visible | Visible | Hidden |
| Add Recommendation | Visible | Hidden | Hidden | Hidden |
| Module filter | Visible | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/security/training/` | Fetch staff training list (paginated) |
| GET | `/api/v1/it/security/training/{staff_id}/` | Fetch individual training record |
| POST | `/api/v1/it/security/training/reminders/` | Send training reminders |
| POST | `/api/v1/it/security/training/{staff_id}/exception/` | Apply training exception (Role 54) |
| GET | `/api/v1/it/security/training/kpis/` | Fetch KPI values |
| GET | `/api/v1/it/security/training/charts/by-branch/` | Completion by branch |
| GET | `/api/v1/it/security/training/charts/trend/` | 12-month completion trend |
| GET | `/api/v1/it/security/training/charts/by-module/` | Module-wise completion rate |
| GET | `/api/v1/it/security/training/export/csv/` | Export training report |
| GET | `/api/v1/it/security/training/{staff_id}/certificate/{module_id}/` | Generate R2 signed URL for certificate |

---

## 13. HTMX Patterns

```html
<!-- Training table with filters -->
<div id="training-table"
     hx-get="/group/it/security/training/table/"
     hx-trigger="load"
     hx-target="#training-table"
     hx-include="#training-filter-form">
</div>

<!-- Search with debounce -->
<input type="text" name="search" placeholder="Search staff..."
       hx-get="/group/it/security/training/table/"
       hx-trigger="keyup changed delay:400ms"
       hx-target="#training-table"
       hx-include="#training-filter-form" />

<!-- Filter change — instant reload -->
<select name="status"
        hx-get="/group/it/security/training/table/"
        hx-trigger="change"
        hx-target="#training-table"
        hx-include="#training-filter-form">
</select>

<!-- View training record drawer -->
<button hx-get="/group/it/security/training/{{ staff_id }}/record/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  View Details
</button>

<!-- Send reminder (single) -->
<button hx-get="/group/it/security/training/{{ staff_id }}/reminder-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  Send Reminder
</button>

<!-- Send bulk reminder -->
<button hx-get="/group/it/security/training/bulk-reminder-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  Send Bulk Reminder
</button>

<!-- Reminder submit -->
<form hx-post="/api/v1/it/security/training/reminders/"
      hx-target="#reminder-status"
      hx-swap="innerHTML"
      hx-on::after-request="closeDrawer()">
  <button type="submit">Send Reminder(s)</button>
</form>

<!-- Charts — independent loads -->
<div id="chart-by-branch"
     hx-get="/group/it/security/training/charts/by-branch/"
     hx-trigger="load"
     hx-target="#chart-by-branch">
</div>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
