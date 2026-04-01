# 02 — Group IT Admin Dashboard

- **URL:** `/group/it/admin/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group IT Admin (Role 54, G4)

---

## 1. Purpose

The Group IT Admin Dashboard is the most action-heavy page in Division F — the operational nerve centre where the IT Admin spends the majority of their working day. It provides direct control over all branch portals, user role provisioning, feature toggle management, and WhatsApp notification configuration across the entire group.

Unlike the IT Director Dashboard (which is executive and approval-oriented), this page is hands-on. The IT Admin uses it to respond to portal config requests from branch principals, onboard new staff onto the platform, push feature rollouts to specific branches, and configure branch-level notification channels. Every change made here is logged to the IT Audit Log with timestamp and user ID.

The pending portal config request queue is surfaced prominently so the IT Admin can action branch-initiated requests without waiting for a separate ticket workflow. User provisioning requests — where a branch wants a new role assigned or an existing user's permissions changed — are similarly queued here with a one-click review-and-approve workflow.

The dashboard also monitors WhatsApp configuration status across all branches, since misconfigured WhatsApp API keys or inactive notification triggers directly impact parent communication — one of the highest-visibility items for branch management. Any branch with a broken WhatsApp config is flagged immediately in the KPI bar.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + create/edit/configure portals | Primary role; all branches |
| Group IT Director | G4 | Full read | Cannot perform provisioning or config actions directly |
| Group IT Support Executive | G3 | Read-only (portal status only) | Cannot access config or user provisioning |
| Group EduForge Integration Manager | G4 | Read-only (integration status columns only) | Cannot modify portal config |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → IT Admin Dashboard
```

### 3.2 Page Header
- **Title:** `Group IT Admin Dashboard`
- **Subtitle:** `Portal Operations — All Branches · [Configured Portals] portals configured · [Provisioning Requests Pending] requests pending`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `+ Create Portal` · `Provisioning Requests ([count])` · `Notification Bell`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any portal config flagged as broken | "[N] portal(s) have configuration issues requiring attention." | Red |
| WhatsApp API key expired at any branch | "WhatsApp API key expired at [Branch Name]. Parent notifications disabled." | Red |
| User provisioning request > 48 hours unactioned | "[N] provisioning request(s) have been waiting more than 48 hours." | Amber |
| Feature toggle rollout pending Director approval | "[N] feature toggle change(s) are awaiting IT Director approval before they can apply." | Amber |

**Alert Notification Rules:**
- Portal config issues: IT Admin (in-app + email); escalated to IT Director if unresolved > 3 hours
- WhatsApp API key expired: IT Admin + affected Branch Principal (in-app red + email)
- Provisioning request > 48h: IT Admin (in-app amber + email)
- Feature toggle pending Director approval: IT Director (in-app + email)
- Provisioning approved: Requestor notified via in-app notification + email

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Branch Portals Configured | Total portals with complete configuration out of total created | Green if 100%, Amber < 95%, Red < 90% | Links to Branch Portal Manager (`/group/it/portals/`) |
| Users Provisioned (Total) | Total active platform users across all branches | Blue (informational) | Links to user directory |
| Feature Toggles Pending Review | Feature toggle changes awaiting IT Director approval | Green = 0, Amber 1–3, Red > 3 | Links to Feature Toggle Manager |
| User Provisioning Requests Pending | Unactioned role assignment or permission change requests | Green = 0, Amber 1–5, Red > 5 | Opens provisioning queue drawer |
| Portals with Config Issues | Portals with one or more configuration errors flagged | Green = 0, Amber 1–2, Red > 2 | Filters main table to config-issue portals |
| WhatsApp Config Status | Count of branches with active and valid WhatsApp API config | Green = all active, Amber if any inactive, Red if > 2 inactive | Opens WhatsApp config overview |

---

## 5. Main Table — Branch Portal Status

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text (link to portal config page) | Yes | Yes (multi-select) |
| Portal URL | Text with copy icon (slug or custom domain) | No | No |
| Status | Badge: Active (green) / Onboarding (blue) / Inactive (grey) / Suspended (red) | Yes | Yes (status checkbox) |
| Active Users | Integer | Yes | Yes (> N) |
| Feature Toggles | Integer count of enabled features | Yes | No |
| Domain Config | Badge: Custom (green) / Default (grey) / Error (red) | No | Yes (Custom/Default/Error) |
| Last Modified | Relative datetime | Yes | Yes (date range) |
| Actions | `Config` · `Toggle Features` · `Manage Users` icon buttons | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Portal Status | Checkbox group | Active / Onboarding / Inactive / Suspended |
| Domain Config | Checkbox | Custom / Default / Error |
| Feature Count Above | Numeric input | Integer threshold |
| Last Modified | Date range picker | From / To |
| Config Issues Only | Toggle switch | Yes / No |

### 5.2 Search
- Full-text: Branch name or portal URL slug
- 300ms debounce, triggers HTMX GET with `?search=` query param

### 5.3 Pagination
- Server-side · 20 rows/page · Shows total count and current range (e.g., "Showing 1–20 of 50")

---

## 6. Drawers

### 6.1 Drawer: `it-admin-quick-config` — Quick Portal Config
- **Trigger:** Actions → Config button on any row
- **Width:** 480px
- **Fields:** Portal name (editable), Portal status toggle (Active/Inactive), Primary contact email, Timezone dropdown, Academic year start month, Feature toggle quick switches (top 5 most-used), Save Changes button
- **Note:** Full config is available at the per-portal config editor page (`/group/it/portals/{id}/config/`); this drawer covers the most-frequently-changed settings only

**Audit:** Portal configuration changes are logged to IT Audit Log with IT Admin user ID and timestamp.

### 6.2 Drawer: `it-admin-feature-toggle` — Feature Toggle Panel
- **Trigger:** Actions → Toggle Features on any branch row
- **Width:** 560px
- **Layout:** Grid of all platform features with on/off toggle per feature for the selected branch. Features are grouped by category (Academic, Communication, Finance, Admin, AI). Each toggle shows: feature name, current state, last changed by, last changed date.
- **Save button:** HTMX POST to save all changed toggles in one batch request. Changes requiring Director approval show a yellow badge and are submitted as a pending approval rather than applying immediately.

**Audit:** Feature toggle changes are logged to IT Audit Log with IT Admin user ID and timestamp.

### 6.3 Drawer: `it-admin-provisioning-review` — User Provisioning Request Review
- **Trigger:** Click Provisioning Requests count in header or KPI card
- **Width:** 480px
- **Fields shown:** Requestor (branch principal/IT contact), request date, user's name and current role, requested role change, affected branch, justification text, Approve / Reject / Modify and Approve buttons
- **On approval:** Role is updated in PostgreSQL and a confirmation notification is sent to the requesting branch contact
- **On reject:** Rejection reason textarea (required) → notification sent to requestor

**Audit:** Provisioning decisions (approve/reject/modify) are logged to IT Audit Log with IT Admin user ID and timestamp.

### 6.4 Drawer: `it-admin-create-portal` — Create New Branch Portal

Triggered by `+ Create Portal` button in header. Width: 560px.

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Portal Name | Text | Yes | Max 100 chars, alphanumeric + spaces |
| Branch Name | Dropdown | Yes | Select from registered branches or enter new |
| Portal URL Slug | Text | Yes | Auto-generated from name; editable; alphanumeric + hyphens; unique |
| Primary Contact Email | Email | Yes | Valid email format |
| Timezone | Dropdown | Yes | IANA timezone list |
| Academic Year Start Month | Dropdown | Yes | January–December |
| SSO Enabled | Toggle | No | Default: off |
| Custom Domain | Text | No | Valid FQDN if provided |

**Footer:** `Create Portal` (primary) / `Cancel`

**On submit:** `hx-post="/api/v1/it/admin/portals/"` — portal created in Onboarding status; welcome email sent to primary contact; IT Audit Log entry written.

**Toast:** `Portal '[Name]' created successfully. Status: Onboarding.` (Success, 4s)

---

## 7. Charts

### 7.1 User Provisioning Volume by Branch (Bar Chart)
- **X-axis:** Top 15 branches by user count
- **Y-axis:** User count
- **Series:** Students (blue) / Teaching Staff (green) / Non-Teaching Staff (teal) / Admins (amber) — stacked bars
- **Data source:** GET `/api/v1/it/admin/charts/user-volume/`

### 7.2 Feature Adoption Rate — Top 10 Features (Horizontal Bar Chart)
- **Y-axis:** Feature names (top 10 by active-use rate)
- **X-axis:** % of branches where the feature is enabled AND actively used in last 30 days
- **Colour:** Green if ≥ 70%, Amber 50–69%, Red < 50%
- **Purpose:** Helps IT Admin identify under-utilised features and plan enablement campaigns
- **Data source:** GET `/api/v1/it/admin/charts/feature-adoption/`

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Portal config saved | "Portal configuration updated for [Branch Name]." | Success | 4s |
| Feature toggles saved (immediate) | "Feature settings saved for [Branch Name]." | Success | 4s |
| Feature toggles submitted for approval | "[N] feature change(s) submitted to IT Director for approval." | Info | 5s |
| Provisioning request approved | "Role updated. [User Name] is now [Role] at [Branch Name]." | Success | 4s |
| Provisioning request rejected | "Provisioning request rejected. Requestor has been notified." | Info | 4s |
| Portal created | "New portal created for [Branch Name]. Onboarding in progress." | Success | 5s |
| Config save error | "Failed to save configuration. Please check your input and try again." | Error | 6s |
| Feature toggle save error | Error: `Failed to save feature settings. Please try again.` | Error | 5s |
| Provisioning request rejection error | Error: `Failed to reject provisioning request. Please try again.` | Error | 5s |
| Provisioning modification error | Error: `Failed to modify and approve provisioning request. Please try again.` | Error | 5s |
| Portal creation error | Error: `Failed to create portal. Check that the slug is not already in use.` | Error | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No portals created | "No Branch Portals Yet" | "Create your first branch portal to begin group-wide IT administration." | + Create Portal |
| No provisioning requests | "No Pending Requests" | "All user provisioning requests have been actioned. Your queue is empty." | — |
| Search returns no results | "No Portals Match" | "No branch portals match your search or filter criteria. Try adjusting your filters." | Clear Filters |
| All portals active, no config issues | "All Portals Healthy" | "All branch portals are active and properly configured. No action required." | View Feature Toggles |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer (6 cards) + table skeleton (8 rows) + chart shimmer |
| Quick config drawer open | Drawer-scoped spinner until form fields load |
| Feature toggle panel open | Drawer spinner while feature list loads; individual toggles appear progressively |
| Provisioning request drawer open | Drawer-scoped spinner |
| Config save | Save button spinner + form fields disabled until response |
| Toggle batch save | Save button spinner; grid toggles locked during request |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | IT Support Executive (G3) | Integration Manager (G4) |
|---|---|---|---|---|
| KPI Summary Bar | All 6 cards | All 6 cards | Portal status card only | Integration-related cards only |
| Branch Portal Status Table | Visible + all Actions | Visible (no Actions) | Visible (read-only, no Actions) | Visible (no Config/User actions) |
| + Create Portal Button | Visible | Hidden | Hidden | Hidden |
| Quick Config Drawer | Visible + editable | Hidden | Hidden | Hidden |
| Feature Toggle Panel | Visible + editable | Visible (read-only) | Hidden | Hidden |
| Provisioning Review Drawer | Visible + actionable | Visible (read-only) | Hidden | Hidden |
| WhatsApp Config KPI | Visible | Visible | Hidden | Hidden |
| Alert Banners | All visible | All visible | Portal status alerts only | Integration alerts only |
| Charts | Both visible | Both visible | Hidden | Feature adoption chart only |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/admin/kpis/` | JWT (G4) | Returns all 6 KPI card values |
| GET | `/api/v1/it/admin/portals/` | JWT (G4) | Paginated branch portal status table |
| PATCH | `/api/v1/it/admin/portals/{id}/quick-config/` | JWT (G4) | Save quick portal config changes |
| GET | `/api/v1/it/admin/portals/{id}/features/` | JWT (G4) | Feature toggle list for a specific branch |
| POST | `/api/v1/it/admin/portals/{id}/features/` | JWT (G4) | Batch save feature toggle changes |
| GET | `/api/v1/it/admin/provisioning-requests/` | JWT (G4) | List pending user provisioning requests |
| POST | `/api/v1/it/admin/provisioning-requests/{id}/approve/` | JWT (G4) | Approve a provisioning request |
| POST | `/api/v1/it/admin/provisioning-requests/{id}/reject/` | JWT (G4) | Reject a provisioning request |
| POST | `/api/v1/it/admin/portals/` | JWT (G4) | Create a new branch portal |
| GET | `/api/v1/it/admin/charts/user-volume/` | JWT (G4) | User volume by branch bar chart data |
| GET | `/api/v1/it/admin/charts/feature-adoption/` | JWT (G4) | Feature adoption horizontal bar chart data |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/it/admin/kpis/` | `#kpi-bar` | `innerHTML` |
| Load portal status table | `load` | GET `/api/v1/it/admin/portals/` | `#portal-table` | `innerHTML` |
| Open quick config drawer | `click` on Config button | GET `/api/v1/it/admin/portals/{id}/quick-config/` | `#config-drawer` | `innerHTML` |
| Save quick config | `click` on Save Changes | PATCH `/api/v1/it/admin/portals/{id}/quick-config/` | `#config-result` | `innerHTML` |
| Open feature toggle panel | `click` on Toggle Features | GET `/api/v1/it/admin/portals/{id}/features/` | `#toggle-drawer` | `innerHTML` |
| Save feature toggles | `click` on Save Toggles | POST `/api/v1/it/admin/portals/{id}/features/` | `#toggle-result` | `innerHTML` |
| Open provisioning queue | `click` on Provisioning Requests count | GET `/api/v1/it/admin/provisioning-requests/` | `#provisioning-drawer` | `innerHTML` |
| Approve provisioning request | `click` on Approve | POST `/api/v1/it/admin/provisioning-requests/{id}/approve/` | `#provisioning-result` | `innerHTML` |
| Filter table | `change` on any filter control | GET `/api/v1/it/admin/portals/?status=active` | `#portal-table` | `innerHTML` |
| Search portals | `keyup[debounce:300ms]` on search | GET `/api/v1/it/admin/portals/?search=` | `#portal-table` | `innerHTML` |
| Paginate table | `click` on page button | GET `/api/v1/it/admin/portals/?page=N` | `#portal-table` | `innerHTML` |
| Refresh KPI bar after action | `htmx:afterRequest` on any POST | GET `/api/v1/it/admin/kpis/` | `#kpi-bar` | `innerHTML` |

---

**Audit Trail:** All write operations on this page are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications:** Critical alerts on this page trigger in-app notifications to the relevant role owners as specified in the alert banner conditions above.

*Page spec version: 1.0 · Last updated: 2026-03-21*
