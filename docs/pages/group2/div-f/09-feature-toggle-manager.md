# 09 — Feature Toggle Manager

- **URL:** `/group/it/portals/features/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4)

---

## 1. Purpose

The Feature Toggle Manager provides group-wide control over which EduForge platform features are enabled. It operates at two levels: the group-level default (which applies to all branches unless overridden), and per-branch overrides (which allow specific branches to deviate from the group default for a specific feature).

This two-tier architecture is essential for a multi-branch EdTech group where different branches may have different operational maturity, different subscription tiers, or different pedagogical requirements. A branch running its first year of EduForge may not be ready for AI features, while a flagship campus may have all features active. The Feature Toggle Manager allows the IT Admin to manage this without maintaining 50 separate configuration files.

The group-level default is the baseline. When a feature is turned ON at the group level, it becomes enabled for all branches that have not set an override. When it is turned OFF at the group level, it is disabled for all branches that have not set an override. A branch override — either ON or OFF — always takes precedence over the group default for that branch/feature combination.

The page uses a two-pane layout: the left pane lists all platform features with their group-level defaults and adoption metrics; the right pane shows branch-level override detail for whichever feature is currently selected. This design allows the IT Admin to see both the macro picture (group-wide default) and the micro picture (per-branch deviations) without navigating away.

All feature toggle changes are recorded in the IT Audit Log. Changes that require IT Director approval (designated high-impact features such as AI Question Generator or Advanced Analytics) are submitted as pending approval requests rather than applying immediately.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + edit group defaults + set branch overrides | Primary role |
| Group IT Director | G4 | Full read + approve high-impact toggle changes | Reviews and approves pending approvals |
| Group IT Support Executive | G3 | Read-only (feature name, group default, branch count only) | Cannot edit |
| Group EduForge Integration Manager | G4 | Read-only | Cannot edit feature toggles |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Branch Portal Manager → Feature Toggle Manager
```

### 3.2 Page Header
- **Title:** `Feature Toggle Manager`
- **Subtitle:** `Group-wide Feature Control · [Total Features] features · [Pending Approvals] pending Director approval`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `Pending Approvals ([count])` · `Audit Log` · `Notification Bell`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Feature toggle change pending Director approval > 48 hours | "[N] feature toggle change(s) have been awaiting IT Director approval for more than 48 hours." | Amber |
| High-impact feature enabled globally (first time) | "Alert: [Feature Name] has been enabled globally. All branches without an override will now have access." | Info (dismissible) |

---

## 4. KPI Summary Bar

No KPI Summary Bar on this management page. Summary metrics are embedded in the page header subtitle and in the feature list table's adoption column.

---

## 5. Main Content — Two-Pane Layout

### 5.1 Left Pane — Feature List (Master Table)

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Feature Name | Text (click to load branch override panel on right) | Yes | No |
| Category | Badge: Academic / Communication / Finance / Admin / AI | No | Yes (category checkbox) |
| Group Default | Toggle switch: On (green) / Off (grey) | No | Yes (All On / All Off / Mixed) |
| Branches Override Count | Integer (count of branches with an override set) | Yes | No |
| Enabled In | "X / Y Branches" text (X = branches where feature is effectively ON) | Yes | No |
| Last Changed By | User name (brief) | No | No |
| Last Changed Date | Relative datetime | Yes | Yes (date range) |
| Actions | `Set Group Default` toggle (inline) · `View Overrides` text link | No | No |

**Feature list (all platform features — exhaustive):**
1. Mock Test Engine (Academic) — Create timed mock tests with auto-grading
2. MCQ Engine (Academic) — Question bank and MCQ assessment creation
3. Notes Upload (Academic) — Allow teachers to upload PDF/DOCX study notes
4. Video Learning (Academic) — YouTube embed player for lesson videos
5. Live Classes (Academic) — Schedule and host live class sessions
6. Assignment Submission (Academic) — Online assignment submission and grading
7. Attendance Tracking (Academic) — Digital attendance with biometric/manual entry
8. WhatsApp OTP Login (Communication) — WhatsApp-based OTP for student/parent login
9. Parent Portal Access (Communication) — Separate parent-facing portal view
10. WhatsApp Notifications (Communication) — Automated WhatsApp messages for alerts
11. SMS Notifications (Communication) — SMS fallback for critical notifications
12. Email Digest (Communication) — Weekly summary email to parents
13. Fee Management (Finance) — Fee collection, receipts, due tracking
14. Online Payment Gateway (Finance) — Razorpay/PayU integration for online fees
15. Scholarship Portal (Finance) — Scholarship application and management
16. Payroll Module (Finance) — Staff salary processing
17. Hostel Management Module (Admin) — Hostel room allocation and billing
18. Transport Tracking (Admin) — Bus route and student tracking
19. Library Management (Admin) — Book issue/return tracking
20. Timetable Builder (Admin) — Drag-and-drop timetable creation
21. HR Module (Admin) — Staff onboarding, leave management
22. Advanced Analytics (Admin) — Custom report builder (requires Director approval)
23. AI Question Generator (AI) — AI-assisted question paper generation (requires Director approval)
24. AI Performance Prediction (AI) — Student performance forecast (requires Director approval)
25. AI Chatbot (AI) — AI helpdesk for students and parents (requires Director approval)

**Feature Lifecycle:** Features cannot be deleted. To retire a feature, set group default to Off and migrate branch overrides to Inherit. Deprecated features display a "Deprecated" badge.

### 5.2 Right Pane — Branch Override Table (shown when a feature is selected in left pane)

- **Header:** "[Feature Name] — Branch Overrides"
- **No feature selected state:** "Select a feature from the list to view and manage branch-level overrides."

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text | Yes | Yes (multi-select) |
| Override | Toggle: On / Off / Inherit (grey = inheriting group default) | No | Yes (On / Off / Inherit) |
| Effective State | Badge showing the actual state for this branch (considering group default + override) | No | No |
| Changed By | User name | No | No |
| Date | Relative datetime | Yes | No |

- **Bulk Actions:** "Set All to Inherit Group Default" button (clears all overrides for this feature)
- **Save:** Each toggle change auto-saves via HTMX PATCH without a Save button

### 5.3 Filters (Left Pane)

| Filter | Type | Options |
|---|---|---|
| Category | Checkbox group | Academic / Communication / Finance / Admin / AI |
| Group Default Status | Checkbox group | All On / All Off / Mixed (branches have overrides) |
| Requires Director Approval | Checkbox | Yes / No |
| Last Changed | Date range picker | From / To |

### 5.4 Search (Left Pane)
- Full-text: Feature name
- 300ms debounce, triggers HTMX GET with `?search=` query param

### 5.5 Pagination (Left Pane)
- All 25 features fit on one page — no pagination needed. Server-side filtering still applies.

---

## 6. Drawers

**Audit Trail:** All feature toggle changes are logged to IT Audit Log including: user ID, timestamp, feature name, old value, new value, change type (group default vs. branch override), approval status if applicable.

### 6.1 Drawer: `feature-pending-approval` — Pending Director Approval Review
- **Trigger:** Click "Pending Approvals ([count])" in page header
- **Width:** 560px
- **Content:** List of feature toggle changes pending IT Director approval. Per item: Feature name, proposed change (group default or branch override), submitted by, date submitted, rationale, IT Director Approve / Reject buttons (visible only to IT Director)
- **IT Admin view:** Shows items submitted by self, with status (Pending / Approved / Rejected) and Director's notes on rejected items

---

## 7. Charts

No dedicated charts on this page. The "Enabled In X/Y Branches" column in the feature list provides the adoption data inline. The IT Admin Dashboard's horizontal bar chart (Feature Adoption Rate — Top 10) provides the visual summary.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Group default changed (immediate) | "[Feature Name] group default set to [On/Off]. [N] branches now affected." | Success | 5s |
| Group default submitted for approval | "[Feature Name] change submitted to IT Director for approval." | Info | 5s |
| Branch override set | "[Feature Name] override set to [On/Off] for [Branch Name]." | Success | 3s |
| Branch override cleared (Inherit) | "[Branch Name] will now inherit the group default for [Feature Name]." | Info | 3s |
| All overrides cleared | "All branch overrides for [Feature Name] cleared. All branches inherit group default." | Info | 4s |
| Approval approved (Director action) | "Feature change approved. [Feature Name] is now [On/Off] group-wide." | Success | 5s |
| Approval rejected (Director action) | "Feature change rejected. IT Admin has been notified." | Info | 4s |
| Error saving toggle | "Failed to save toggle state. Please try again." | Error | 5s |
| Approval request submission error | Error: `Failed to submit feature change for approval. Provide a reason and try again.` | Error | 6s |
| Feature change approval error | Error: `Failed to approve feature change. Verify branch licensing and try again.` | Error | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No feature selected (right pane) | "Select a Feature" | "Click on any feature in the list to view and manage per-branch overrides." | — |
| Feature selected, no overrides set | "No Branch Overrides" | "All branches are inheriting the group default for this feature. You can set individual branch overrides here." | — |
| Feature search returns no results | "No Features Match" | "No features match your search term." | Clear Search |
| No pending approvals | "No Pending Approvals" | "All feature toggle changes have been reviewed by the IT Director." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: left pane feature list shimmer (8 rows) + right pane "select a feature" placeholder |
| Feature selected (right pane load) | Right pane shimmer while branch override table loads |
| Group default toggle change | Toggle shows loading spinner animation while PATCH request is in flight |
| Branch override toggle change | Individual row toggle shows spinner during PATCH |
| Pending approvals drawer open | Drawer-scoped spinner |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | IT Support Executive (G3) | Integration Manager (G4) |
|---|---|---|---|---|
| Left Pane Feature List | Visible + Group Default toggle editable | Visible (read-only) | Feature Name + Group Default + Enabled In columns only | Visible (read-only) |
| Group Default Toggle | Editable (standard features) / Submit for Approval (high-impact) | Read-only (approve via Pending Approvals) | Hidden | Hidden |
| Right Pane Branch Overrides | Visible + editable | Visible (read-only) | Hidden | Hidden |
| Pending Approvals Button | Visible (submitter view) | Visible (approver view — can Approve/Reject) | Hidden | Hidden |
| Bulk "Clear All Overrides" | Visible | Hidden | Hidden | Hidden |
| Audit Log Button | Visible | Visible | Hidden | Hidden |
| Alert Banners | All | All | Hidden | Hidden |

**Note:** Role 55 (DPO) and Role 56 (Cybersecurity Officer) have no access to this page (returns 403).

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/features/` | JWT (G4) | Paginated feature list with group defaults and adoption counts |
| PATCH | `/api/v1/it/features/{feature_id}/group-default/` | JWT (G4) | Set group-level default for a feature |
| GET | `/api/v1/it/features/{feature_id}/overrides/` | JWT (G4) | Branch override table for a specific feature |
| PATCH | `/api/v1/it/features/{feature_id}/overrides/{branch_id}/` | JWT (G4) | Set or clear branch override for a feature |
| DELETE | `/api/v1/it/features/{feature_id}/overrides/` | JWT (G4) | Clear all branch overrides for a feature |
| GET | `/api/v1/it/features/pending-approvals/` | JWT (G4) | List of feature toggle changes pending IT Director approval |
| POST | `/api/v1/it/features/pending-approvals/{id}/approve/` | JWT (G4) | IT Director approves a feature change |
| POST | `/api/v1/it/features/pending-approvals/{id}/reject/` | JWT (G4) | IT Director rejects a feature change |
| GET | `/api/v1/it/features/audit-log/?feature_id={id}&date_range={range}` | JWT (G4) | Retrieve audit trail for feature toggle changes |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load feature list on page ready | `load` | GET `/api/v1/it/features/` | `#feature-list` | `innerHTML` |
| Select feature → load right pane | `click` on feature row | GET `/api/v1/it/features/{id}/overrides/` | `#override-pane` | `innerHTML` |
| Toggle group default (standard feature) | `change` on group default toggle | PATCH `/api/v1/it/features/{id}/group-default/` | `#feature-row-{id}` | `outerHTML` |
| Toggle group default (high-impact → submit) | `change` on locked toggle (approval required) | POST `/api/v1/it/features/approval-requests/` | `#pending-badge` | `innerHTML` |
| Set branch override | `change` on override toggle | PATCH `/api/v1/it/features/{id}/overrides/{branch_id}/` | `#override-row-{branch_id}` | `outerHTML` |
| Clear all overrides for feature | `click` on Clear All Overrides | DELETE `/api/v1/it/features/{id}/overrides/` | `#override-pane` | `innerHTML` |
| Open pending approvals drawer | `click` on Pending Approvals count | GET `/api/v1/it/features/pending-approvals/` | `#approvals-drawer` | `innerHTML` |
| Approve feature change (Director) | `click` on Approve | POST `/api/v1/it/features/pending-approvals/{id}/approve/` | `#approval-item-{id}` | `outerHTML` |
| Filter feature list | `change` on category filter | GET `/api/v1/it/features/?category=AI` | `#feature-list` | `innerHTML` |
| Search features | `keyup[debounce:300ms]` on search | GET `/api/v1/it/features/?search=` | `#feature-list` | `innerHTML` |

---

**Audit Trail:** All write operations on this page are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications:** Critical alerts on this page trigger in-app notifications to the relevant role owners as specified in the alert banner conditions above.

*Page spec version: 1.0 · Last updated: 2026-03-21*
