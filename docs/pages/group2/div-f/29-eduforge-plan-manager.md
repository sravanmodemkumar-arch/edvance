# 29 — EduForge Plan Manager

- **URL:** `/group/it/eduforge/plan/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group EduForge Integration Manager (Role 58, G4) — Primary; Group IT Director (Role 53, G4) — Read + Approve

---

## 1. Purpose

The EduForge Plan Manager is the group's administrative interface for managing its subscription to the EduForge SaaS platform itself. Plan creation and major upgrades are initiated via the Request Plan Upgrade workflow but finalized by EduForge support team. It is the place where the group views what plan it is on, how much of its allocated capacity it has consumed, when the subscription renews, what add-on modules are active, and how billing has gone historically. It also provides the channel for raising support tickets with the EduForge support team and tracking open issues.

This page is distinct from the financial billing managed in Division D — it is not about the group's own fee collections, but about what the group pays to EduForge for the platform. The Integration Manager maintains visibility over usage against plan limits to preempt overages. When student count approaches the plan limit, the system raises an alert so the Integration Manager can request an upgrade before branches face access denial.

The page is structured as a VIEW/MANAGE page rather than a table-and-drawer layout, because the content is singular (one group has one plan). It uses a card-and-section layout: the top shows the current plan and key renewal information, followed by a usage dashboard with progress bars, followed by add-on module management, then billing history, and finally the support section.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group EduForge Integration Manager | G4 | Full read + manage add-ons + raise tickets | Cannot finalise plan upgrades without IT Director |
| Group IT Director | G4 | Full read + approve upgrade requests | Has authority to approve plan changes |
| Group IT Admin | G4 | Read-only | Can view plan and usage; cannot manage |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → EduForge Account → Plan Manager
```

### 3.2 Page Header
- **Title:** `EduForge Plan Manager`
- **Subtitle:** `[Group Name] · [Plan Name] · Renews [renewal date]`
- **Role Badge:** `Group EduForge Integration Manager`
- **Right-side controls:** `Raise Support Ticket` button · `Request Plan Upgrade` button (Integration Manager only)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Plan renewal <30 days | "Your EduForge subscription renews on [date] ([N] days away). Ensure payment is arranged to avoid service disruption." | Amber |
| Plan renewal <7 days | "URGENT: EduForge subscription renews in [N] days. Contact your EduForge account manager immediately." | Red |
| Any usage dimension >90% | "Usage warning: [Dimension] is at [N]% of plan limit. Contact EduForge to upgrade before limit is reached." | Red |
| Any usage dimension >80% | "[Dimension] is at [N]% of plan limit. Monitor closely and plan for upgrade if needed." | Amber |
| Open Severity 1 support ticket | "Critical support ticket #[N] is open and pending resolution. Last update: [time]." | Red |

---

## 4. KPI Summary Bar

No traditional KPI card bar on this page. The plan overview cards (Section 1 below) serve the same function.

---

## 5. Main Content Sections

This page uses a section-based layout rather than a main table.

### Section 1: Current Plan

**Layout:** Single card spanning full width, with sub-sections

| Field | Display |
|---|---|
| Plan Name | Large text — e.g., "Enterprise 50-Branch" |
| Subscription Status | Badge (Active / Grace Period / Suspended) |
| Billing Cycle | Monthly / Annual |
| Current Period | e.g., "01 Apr 2026 – 31 Mar 2027" |
| Renewal Date | Date + countdown (e.g., "31 Mar 2027 · 376 days") |
| Monthly Equivalent Amount | Currency — e.g., "₹2,40,000/month" |
| Annual Commitment | Currency — e.g., "₹28,80,000/year" |
| GST Rate | e.g., "18% GST additional" |
| Contract Term | e.g., "3-year contract (Year 2 of 3)" |
| Dedicated Account Manager | Name + contact email + phone (read-only) |
| Features Included | Tag list — all features in the current plan |

**Action buttons (Integration Manager only):**
- `Request Plan Upgrade` — opens upgrade request form drawer
- `Download Contract PDF` — fetches contract PDF from Cloudflare R2

---

### Section 2: Usage Dashboard

**Layout:** 4 progress bar cards in a 2×2 grid

| Dimension | Display |
|---|---|
| Student Count | Used: [N] / Limit: [N] · [% bar] · colour: green <80%, amber 80–89%, red ≥90% |
| Branch Count | Used: [N] / Limit: [N] · [% bar] |
| Storage (Cloudflare R2) | Used: [N] GB / Limit: [N] GB · [% bar] |
| API Calls (Monthly) | Used: [N] / Limit: [N] · [% bar] · resets on [date] |

Each card also shows: last updated timestamp (data pulled from PostgreSQL usage aggregation table).

---

### Section 3: Add-on Modules

**Layout:** Table of optional modules

| Column | Content |
|---|---|
| Module Name | e.g., "Hostel Management", "Transport Management", "AI Engine (Smart Insights)", "Biometric Integration", "Custom Report Builder", "Parent Mobile App" |
| Description | One-line description of module purpose |
| Status | Badge (Active / Inactive) |
| Monthly Cost | Currency (₹) per month |
| Activated Date | Date or "—" if inactive |
| Actions | Activate / Deactivate (Integration Manager only; IT Director must approve Activate) |

**Activate workflow:** Click Activate → opens confirmation drawer showing cost impact → Integration Manager submits → IT Director receives approval request → on IT Director approval → module activated → EduForge billed at next cycle.

**Deactivate workflow:** Click Deactivate → confirm modal → effective end-of-current-billing-period note → on confirm, deactivation scheduled.

---

### Section 4: Billing History

**Layout:** Paginated table (server-side, 10 rows/page)

| Column | Content |
|---|---|
| Invoice # | Text (link to download) |
| Invoice Date | Date |
| Period | Billing period covered |
| Description | Plan name + any add-ons billed |
| Amount (excl. GST) | Currency |
| GST Amount | Currency |
| Total Amount | Currency |
| Payment Status | Badge (Paid / Pending / Overdue / Waived) |
| Payment Date | Date or "—" |
| Actions | Download PDF |

---

### Section 5: Support & Account

**Layout:** Two columns

**Left: Support Ticket Form**
- Subject (required, text)
- Ticket Type (dropdown: Feature Issue / Billing Query / Performance / Security Incident / Feature Request / Other)
- Priority (dropdown: Critical / High / Medium / Low)
- Description (required, textarea — min 50 characters)
- Attachments (optional, file upload — screenshots, log files; stored to Cloudflare R2)
- Submit Ticket button

**Right: Open Tickets Table**
| Column | Content |
|---|---|
| Ticket # | Text |
| Subject | Text (truncated) |
| Type | Badge |
| Priority | Badge |
| Status | Badge (Open / In Progress / Awaiting Response / Resolved) |
| Opened Date | Date |
| Last Update | Datetime |
| Actions | View Thread |

**View Thread drawer (720px):** Full conversation thread with EduForge support, with ability to add reply and attach files.

---

## 6. Drawers

### 6.1 Drawer: `plan-upgrade-request` — Request Plan Upgrade
- **Trigger:** `Request Plan Upgrade` button
- **Width:** 560px
- **Fields:**
  - Current Plan (read-only)
  - Requested Upgrade (dropdown: available plan tiers from EduForge plan catalog)
  - Reason for Upgrade (required, textarea — which limit is being approached and why)
  - Requested Effective Date (date picker)
  - Additional notes (optional)
- On submit: Request sent to IT Director for approval via in-app notification; EduForge account manager emailed

### 6.2 Drawer: `module-activate-confirm` — Activate Add-on Module
- **Trigger:** Actions → Activate (on add-on module)
- **Width:** 480px
- Shows: Module name, description, monthly cost, annual impact, effective date
- IT Director approval required note
- Confirm request / Cancel buttons

### 6.3 Drawer: `support-ticket-thread` — View Support Ticket Thread
- **Trigger:** Actions → View Thread
- **Width:** 720px
- Full ticket details + conversation thread (messages from both sides)
- Add Reply text area + file attachment
- Ticket status management (mark resolved, escalate)

---

## 7. Charts

No standalone charts on this page. Usage progress bars in Section 2 serve the visual data representation function.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Support ticket raised | "Support ticket #[N] submitted to EduForge. You will receive a response within [SLA] hours." | Success | 5s |
| Plan upgrade requested | "Plan upgrade request submitted. IT Director has been notified for approval." | Info | 4s |
| Module deactivation scheduled | "Module '[Name]' deactivation scheduled for end of current billing period ([date])." | Warning | 5s |
| Module activation approved | "Module '[Name]' activated. Billing updated from next cycle." | Success | 4s |
| Invoice downloaded | "Invoice #[N] downloaded." | Info | 3s |
| Reply sent | "Reply sent to EduForge support for ticket #[N]." | Success | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No billing history | "No Invoices Yet" | "Billing history will appear here once invoices are generated." | — |
| No support tickets | "No Support Tickets" | "No support tickets have been raised. Use the form to contact EduForge if you need help." | — |
| No add-on modules available | "No Add-on Modules" | "No optional modules are available for your current plan tier." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Current Plan card skeleton + 4 usage bar skeletons + add-on table skeleton + billing table skeleton |
| Billing history pagination | Table skeleton (5 rows) |
| View ticket thread | Drawer spinner; messages load progressively |
| Plan upgrade request submit | Button spinner |
| Module activate/deactivate | Button spinner + row shimmer |
| Contract PDF download | Button spinner "Preparing download…" |

---

## 11. Role-Based UI Visibility

| Element | Integration Manager (G4) | IT Director (G4) | IT Admin (G4) |
|---|---|---|---|
| Request Plan Upgrade | Visible | Visible (approve only) | Hidden |
| Module Activate/Deactivate | Visible (submit request) | Visible (approve request) | Hidden |
| Raise Support Ticket form | Visible | Visible | Hidden |
| View/Reply to ticket thread | Visible | Visible | Visible (view only) |
| Download Contract PDF | Visible | Visible | Hidden |
| Download Invoice PDF | Visible | Visible | Visible |
| Account Manager contact | Visible | Visible | Hidden |
| Add Reply to ticket | Visible | Visible | Hidden |

> Roles 55 (DPO), 56 (Cybersecurity Officer), and 57 (IT Support Executive) have no access to this page (returns 403).

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/plan/` | JWT (G4+) | Current plan details, usage, and add-on list |
| GET | `/api/v1/it/plan/usage/` | JWT (G4+) | Real-time usage values (students, branches, storage, API calls) |
| GET | `/api/v1/it/plan/addons/` | JWT (G4+) | List of available and active add-on modules |
| POST | `/api/v1/it/plan/addons/{id}/activate/` | JWT (G4 — Integration Manager) | Request module activation |
| POST | `/api/v1/it/plan/addons/{id}/deactivate/` | JWT (G4 — Integration Manager) | Schedule module deactivation |
| POST | `/api/v1/it/plan/addons/{id}/approve/` | JWT (G4 — IT Director) | Approve module activation request |
| GET | `/api/v1/it/plan/billing/` | JWT (G4+) | Paginated billing history |
| GET | `/api/v1/it/plan/billing/{invoice_id}/pdf/` | JWT (G4+) | Download invoice PDF (from Cloudflare R2) |
| GET | `/api/v1/it/plan/contract/pdf/` | JWT (G4) | Download contract PDF |
| POST | `/api/v1/it/plan/upgrade-request/` | JWT (G4 — Integration Manager) | Submit plan upgrade request |
| GET | `/api/v1/it/support/tickets/` | JWT (G4+) | Paginated support ticket list |
| POST | `/api/v1/it/support/tickets/` | JWT (G4) | Create support ticket |
| GET | `/api/v1/it/support/tickets/{id}/` | JWT (G4+) | Ticket detail + thread |
| POST | `/api/v1/it/support/tickets/{id}/reply/` | JWT (G4) | Add reply to ticket |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load plan details | `load` | GET `/api/v1/it/plan/` | `#plan-details-section` | `innerHTML` |
| Load usage bars | `load` | GET `/api/v1/it/plan/usage/` | `#usage-dashboard` | `innerHTML` |
| Load add-on modules | `load` | GET `/api/v1/it/plan/addons/` | `#addons-section` | `innerHTML` |
| Load billing history | `load` | GET `/api/v1/it/plan/billing/` | `#billing-table` | `innerHTML` |
| Load open tickets | `load` | GET `/api/v1/it/support/tickets/` | `#tickets-table` | `innerHTML` |
| Paginate billing | `click` on page control | GET `/api/v1/it/plan/billing/?page=N` | `#billing-table` | `innerHTML` |
| Open ticket thread | `click` on View Thread | GET `/api/v1/it/support/tickets/{id}/` | `#support-drawer` | `innerHTML` |
| Submit support ticket | `click` on Submit Ticket | POST `/api/v1/it/support/tickets/` | `#tickets-table` | `innerHTML` |
| Submit upgrade request | `click` on Submit | POST `/api/v1/it/plan/upgrade-request/` | `#upgrade-result` | `innerHTML` |
| Module activate request | `click` on Confirm Activate | POST `/api/v1/it/plan/addons/{id}/activate/` | `#addons-section` | `innerHTML` |
| Module deactivate | `click` on Confirm Deactivate | POST `/api/v1/it/plan/addons/{id}/deactivate/` | `#addons-section` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- Usage approaching plan limit (> 80%): IT Admin + IT Director (in-app amber + email)
- Plan renewal < 30 days: IT Admin + IT Director (in-app amber + email) at 30, 14, and 7 days
- Plan upgrade request approved: IT Admin + IT Director (in-app success + email)
- Support ticket status change: IT Admin (in-app notification)

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
