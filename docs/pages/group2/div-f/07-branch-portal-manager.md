# 07 — Branch Portal Manager

- **URL:** `/group/it/portals/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group IT Admin (Role 54, G4)

---

## 1. Purpose

The Branch Portal Manager is the master registry and lifecycle management page for all branch portals in the group. Every branch that uses EduForge has exactly one portal — a tenant-isolated instance of the platform with its own URL, user base, feature set, and branding. This page is where those portals are created, activated, deactivated, configured, and monitored.

For groups operating 5 to 50 branches, this page provides the central view that answers the question: "What is the current state of every branch portal?" The IT Admin uses this page as a daily check-in to verify all portals are active, identify any portals with configuration issues, and respond to requests from branch principals to adjust portal settings.

Portal lifecycle states: A portal begins in "Onboarding" state when first created, during which the IT Admin configures domain, feature set, and initial user roles. Once the configuration is validated, the IT Admin activates the portal (moves it to "Active"). An "Inactive" portal exists in the system but is not accessible to branch users. A "Suspended" portal has been temporarily blocked — typically due to non-payment or a policy violation — and users see a suspension notice when they attempt to access the portal URL.

The IT Admin has exclusive authority to create new portals and permanently delete them. Branch-level admins cannot create or delete portals. They can only configure settings within their existing portal, subject to group-level constraints.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full CRUD — create, configure, activate, deactivate, suspend portals | Primary role |
| Group IT Director | G4 | Full read + approve portal deactivation | Cannot create portals; approves suspend/deactivate |
| Group EduForge Integration Manager | G4 | Read-only + domain-related actions | Can verify domains but cannot manage portal lifecycle |
| Group IT Support Executive | G3 | Read-only (status column and active user count) | No config access |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Branch Portal Manager
```

### 3.2 Page Header
- **Title:** `Branch Portal Manager`
- **Subtitle:** `[Total Portals] portals · [Active] active · [Inactive] inactive · [Onboarding] onboarding`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `+ Create Portal` · `Export Portal List (CSV)` · `Notification Bell`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any portal in "Suspended" state | "[N] portal(s) are currently suspended. Users at these branches cannot access EduForge." | Red |
| Any portal with SSL Status = Expired | "SSL certificate expired for [Branch Name]. Users will see browser security warnings." | Red |
| Any portal with Config Issues flag | "[N] portal(s) have configuration issues. Review and resolve before branch operations are impacted." | Amber |
| Portal in Onboarding state > 7 days | "[Branch Name] portal has been in Onboarding state for [N] days. Complete configuration or deactivate." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Portals | Total count of all portals regardless of status | Blue (informational) | No drill-down |
| Active | Count of portals with Status = Active | Green if = Total, Amber if < 100%, Red if < 90% | Filters table to Active |
| Inactive | Count of portals with Status = Inactive | Blue (informational) | Filters table to Inactive |
| Portals with Config Issues | Count of portals with one or more configuration errors | Green = 0, Amber 1–2, Red > 2 | Filters table to config-issue portals |

---

## 5. Main Table — Branch Portal List

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text (link to portal config editor) | Yes | Yes (multi-select) |
| Portal URL | Text with copy icon (e.g., `narayan-hyd.eduforge.in` or custom) | No | No |
| Status | Badge: Active (green) / Onboarding (blue) / Inactive (grey) / Suspended (red) | Yes | Yes (checkbox group) |
| Custom Domain | Badge: Yes (green) / No (grey) | No | Yes (Yes/No) |
| SSL Status | Badge: Valid (green) / Expiring (amber) / Expired (red) / Not Configured (grey) | Yes | Yes (status) |
| Feature Count | Integer (count of enabled features) | Yes | No |
| Active Users | Integer | Yes | No |
| Last Config Change | Relative datetime | Yes | Yes (date range) |
| Created Date | Date | Yes | Yes (date range) |
| Actions | `Configure` · `Toggle Status` · `View Users` · `Copy Portal` icon buttons | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Status | Checkbox group | Active / Onboarding / Inactive / Suspended |
| Custom Domain | Checkbox | Yes / No |
| SSL Status | Checkbox group | Valid / Expiring / Expired / Not Configured |
| Created Date Range | Date range picker | From / To |
| Config Issues Only | Toggle switch | Shows only portals with config errors |

### 5.2 Search
- Full-text: Branch name, portal URL slug
- 300ms debounce, triggers HTMX GET with `?search=` query param

### 5.3 Pagination
- Server-side · 20 rows/page · Shows total count and current range (e.g., "Showing 1–20 of 50")

---

## 6. Drawers

### 6.1 Drawer: `portal-create` — Create Portal
- **Trigger:** `+ Create Portal` button in header
- **Width:** 480px
- **Fields:**
  - Branch Select: dropdown of existing branch records not yet associated with a portal (required)
  - Portal Slug: text input (auto-suggested from branch name; URL-safe slug; uniqueness validated on blur via HTMX GET)
  - Custom Domain: text input (optional; leave blank to use default `{slug}.eduforge.in`)
  - Initial Feature Set: multi-select of feature categories (Academic Core / Communication / Finance / Analytics / AI Features)
  - Assign IT Admin Contact: user select (group user with G3+ role)
  - Timezone: dropdown (defaults to IST)
  - Academic Year Start: month select
- **Submit:** POST creates portal in "Onboarding" state. IT Admin contact receives onboarding notification.

### 6.2 Drawer: `portal-view` — View Portal Detail
- **Trigger:** Click branch name link in table
- **Width:** 560px
- **Content:** Portal summary — Branch name, slug, status badge, active user count, feature count, custom domain and SSL status, created date, last config change date and by whom, config issue list (if any), quick-links to Configure and Domain Manager

### 6.3 Drawer: `portal-edit-status` — Toggle Status
- **Trigger:** Actions → Toggle Status
- **Width:** 480px
- **Content:** Current status badge, new status selector (Active / Inactive / Suspended), Reason for change (textarea — required for Inactive and Suspended), Impact warning (auto-calculated: "This will prevent [N] active users from accessing the portal"), Notify Branch Contact (checkbox — checked by default), Confirm Change button
- **For Suspended status:** Additional confirmation step with IT Director notification auto-sent

### 6.4 Drawer: `portal-copy` — Copy Portal Configuration
- **Trigger:** Actions → Copy Portal
- **Width:** 480px
- **Purpose:** Copy the feature set and settings from one portal to a newly-onboarding portal
- **Fields:** Source Portal (dropdown — the portal to copy from), Target Portal (dropdown — the portal to apply the copy to, must be in Onboarding state), What to Copy (checkboxes: Feature Toggles / Notification Config / Role Templates / Branding), Confirm Copy button
- **Note:** Does not copy user data or academic records — configuration only

### 6.5 Modal: `portal-deactivate` — Deactivate Portal (Confirm)
- **Trigger:** Toggle Status → Inactive → Confirm Change
- **Width:** Full-screen modal overlay (420px centred)
- **Content:** "You are about to deactivate the portal for [Branch Name]. [N] active users will lose access. This action is reversible — the portal can be reactivated at any time." · Confirm · Cancel

**Audit Trail:** All portal status changes (create, activate, deactivate, suspend, config copy) are logged to IT Audit Log with IT Admin user ID, timestamp, and change description.

**Notifications:**
- Portal deactivation: IT Director notified via email + in-app alert immediately; Branch contact notified via email if "Notify Branch Contact" checkbox selected
- Portal suspension: IT Director notified via email + in-app alert; Branch contact notified via email

---

## 7. Charts

No dedicated charts on this page. Portal status distribution is represented through the 4-card KPI bar. Detailed technology health charts are available on the IT Director Dashboard.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Portal created | "Portal created for [Branch Name]. Status: Onboarding." | Success | 5s |
| Portal status updated to Active | "[Branch Name] portal is now Active. Users can log in." | Success | 4s |
| Portal deactivated | "[Branch Name] portal deactivated. Users notified." | Info | 4s |
| Portal suspended | "[Branch Name] portal suspended. IT Director notified." | Warning | 5s |
| Portal copy complete | "Configuration from [Source Branch] applied to [Target Branch]." | Success | 4s |
| Portal copy failed | Error: `Failed to copy configuration. Verify target portal is in Onboarding status.` | Error | 5s |
| Portal slug taken | "The portal slug '[slug]' is already in use. Choose a different slug." | Error | 5s |
| Create error | "Failed to create portal. Please check your input and try again." | Error | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No portals exist | "No Branch Portals" | "No branch portals have been created yet. Create your first portal to begin onboarding branches." | + Create Portal |
| No portals match filters | "No Portals Match" | "No portals match your filter criteria. Try adjusting your filters." | Clear Filters |
| Search returns no results | "No Portals Found" | "No portals match your search term." | Clear Search |
| All portals active, no issues | "All Portals Operational" | "Every branch portal is active and properly configured." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer (4 cards) + table skeleton (8 rows) |
| Create portal drawer open | Drawer-scoped spinner while branch dropdown options load |
| Slug uniqueness check | Inline spinner on slug input field; green tick or red error on completion |
| Copy portal drawer open | Drawer-scoped spinner |
| Status change submission | Confirm button spinner + disabled state |
| Table filter/search | Table area overlay shimmer |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | Integration Manager (G4) | IT Support Executive (G3) |
|---|---|---|---|---|
| KPI Summary Bar | All 4 cards | All 4 cards | All 4 cards | Active count only |
| Portal List Table | Visible + all Action buttons | Visible (no Create, no Toggle Status) | Visible (no lifecycle actions) | Visible (Branch + Status + Users only) |
| + Create Portal Button | Visible | Hidden | Hidden | Hidden |
| Configure Action | Visible | Hidden | Hidden | Hidden |
| Toggle Status Action | Visible | Read-only (can approve, not initiate) | Hidden | Hidden |
| View Users Action | Visible | Visible | Hidden | Hidden |
| Copy Portal Action | Visible | Hidden | Hidden | Hidden |
| Alert Banners | All banners | All banners | Domain/SSL banners only | Status banners only |
| Export CSV | Visible | Visible | Hidden | Hidden |

**Note:** Role 55 (DPO) and Role 56 (Cybersecurity Officer) have no access to this page (returns 403). All UI elements hidden.

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/portals/` | JWT (G4) | Paginated branch portal list |
| POST | `/api/v1/it/portals/` | JWT (G4) | Create a new branch portal |
| GET | `/api/v1/it/portals/{id}/` | JWT (G4) | Portal detail for view drawer |
| PATCH | `/api/v1/it/portals/{id}/` | JWT (G4) | Update portal settings |
| DELETE | `/api/v1/it/portals/{id}/` | JWT (G4) | Permanently delete a portal (hard delete, G4 only) |
| POST | `/api/v1/it/portals/{id}/activate/` | JWT (G4) | Set portal status to Active |
| POST | `/api/v1/it/portals/{id}/deactivate/` | JWT (G4) | Set portal status to Inactive |
| POST | `/api/v1/it/portals/{id}/suspend/` | JWT (G4) | Set portal status to Suspended |
| POST | `/api/v1/it/portals/{id}/copy-config/` | JWT (G4) | Copy config from source portal to this portal |
| GET | `/api/v1/it/portals/slug-check/?slug={slug}` | JWT (G4) | Check slug availability (for inline validation) |
| GET | `/api/v1/it/portals/kpis/` | JWT (G4) | Returns 4 KPI card values |
| GET | `/api/v1/it/portals/pending-approvals/` | JWT (G4) | List portal lifecycle changes awaiting IT Director approval |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/it/portals/kpis/` | `#kpi-bar` | `innerHTML` |
| Load portal table | `load` | GET `/api/v1/it/portals/` | `#portal-table` | `innerHTML` |
| Open create portal drawer | `click` on + Create Portal | GET `/api/v1/it/portals/create-form/` | `#create-drawer` | `innerHTML` |
| Validate slug on blur | `blur` on slug input | GET `/api/v1/it/portals/slug-check/?slug={value}` | `#slug-validation` | `innerHTML` |
| Submit create portal | `click` on Submit | POST `/api/v1/it/portals/` | `#create-result` | `innerHTML` |
| Open portal detail drawer | `click` on branch name | GET `/api/v1/it/portals/{id}/` | `#view-drawer` | `innerHTML` |
| Open toggle status drawer | `click` on Toggle Status | GET `/api/v1/it/portals/{id}/status-form/` | `#status-drawer` | `innerHTML` |
| Submit status change | `click` on Confirm Change | POST `/api/v1/it/portals/{id}/activate/` (or deactivate/suspend) | `#portal-row-{id}` | `outerHTML` |
| Filter table | `change` on filter controls | GET `/api/v1/it/portals/?status=active` | `#portal-table` | `innerHTML` |
| Search portals | `keyup[debounce:300ms]` on search | GET `/api/v1/it/portals/?search=` | `#portal-table` | `innerHTML` |
| Paginate table | `click` on page button | GET `/api/v1/it/portals/?page=N` | `#portal-table` | `innerHTML` |
| Refresh KPI after status change | `htmx:afterRequest` on status POST | GET `/api/v1/it/portals/kpis/` | `#kpi-bar` | `innerHTML` |

---

**Audit Trail:** All write operations on this page are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications:** Critical alerts on this page trigger in-app notifications to the relevant role owners as specified in the alert banner conditions above.

*Page spec version: 1.0 · Last updated: 2026-03-21*
