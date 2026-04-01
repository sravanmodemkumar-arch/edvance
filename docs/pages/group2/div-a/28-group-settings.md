# 28 — Group Settings

> **URL:** `/group/gov/settings/`
> **File:** `28-group-settings.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Chairman G5 · MD G5 · CEO G4 (full) — others cannot access

---

## 1. Purpose

Master configuration for the institution group on EduForge. Controls group identity (name, logo,
branding), academic year settings, feature module toggles, notification defaults, EduForge
subscription details, and external integrations.

Changes here affect all branches. High-impact changes (feature disabling, integration changes)
require Chairman or MD confirmation.

---

## 2. Role Access

| Role | Access | Notes |
|---|---|---|
| Chairman | Full — all settings | |
| MD | Full | |
| CEO | Full | |
| All others | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Group Settings
```

### 3.2 Page Header
```
Group Settings                                         [Save Changes]  [Discard Changes]
[Group Name] · Last updated: [date time] by [Name]
```

**Unsaved changes indicator:** Yellow bar at top of page when there are unsaved changes.

### 3.3 Tab Navigation (settings organised by area)
```
Group Profile  |  Branding  |  Academic Year  |  Feature Toggles  |  Notifications  |  EduForge Subscription  |  Integrations
```

---

## 4. Tab Specifications

### Tab 1: Group Profile

| Field | Type | Required | Validation |
|---|---|---|---|
| Group Name (Legal) | Text | ✅ | Min 3, max 200 |
| Group Name (Display) | Text | ✅ | Max 100 chars — shown to users |
| Group Type | Select | ✅ | Large (20+ branches) · Small (5–19 branches) |
| Registered Address | Textarea | ✅ | Max 500 chars |
| District | Text | ✅ | |
| State | Select | ✅ | |
| PIN Code | Text | ✅ | 6 digits |
| Trust / Society Reg. Number | Text | ❌ | |
| Year Established | Year | ✅ | 1900–current |
| Primary Contact Name | Text | ✅ | |
| Primary Contact Mobile | Tel | ✅ | 10-digit |
| Primary Contact Email | Email | ✅ | |
| Website URL | URL | ❌ | |

**[Save Profile] button** (inline — saves this tab's changes separately from other tabs).

---

### Tab 2: Branding

| Field | Type | Required | Notes |
|---|---|---|---|
| Group Logo | Image upload | ❌ | PNG/JPG · Max 2MB · Min 200×200px · Shown in all portals |
| Favicon | Image upload | ❌ | PNG/ICO · Max 1MB · 32×32px |
| Primary Colour | Colour picker | ❌ | Hex colour — used for buttons, badges |
| Secondary Colour | Colour picker | ❌ | Hex colour — accents |
| WhatsApp Business Name | Text | ❌ | Shown in WhatsApp messages |
| WhatsApp Business Number | Tel | ❌ | Registered WA Business number |
| Email Sender Name | Text | ❌ | "From" name in emails e.g. "EduForge – [Group Name]" |
| Email Reply-To | Email | ❌ | |

**Preview panel:** Live preview of login page with the selected logo and colours.

**[Save Branding] button.**

---

### Tab 3: Academic Year

| Field | Type | Required | Notes |
|---|---|---|---|
| Academic Year Start | Date | ✅ | Default: April 1 |
| Academic Year End | Date | ✅ | Default: March 31 |
| Term 1 Start | Date | ✅ | |
| Term 1 End | Date | ✅ | |
| Term 2 Start | Date | ✅ | |
| Term 2 End | Date | ✅ | |
| Term 3 Start | Date | ❌ | Some groups have 3 terms |
| Term 3 End | Date | ❌ | |
| Working Days per Week | Number | ✅ | 5 or 6 |
| Default Holiday List | Multi-select | ❌ | National holidays (pre-populated) |

**Note:** Branch-level academic calendars inherit these dates. Branch can override with Group approval.

**[Save Academic Year] button.**

---

### Tab 4: Feature Toggles

**Display:** Group of toggle switches, organized by feature area.

| Feature | Default | Notes |
|---|---|---|
| Hostel Module | ON if group has hostels | Disabling removes hostel tabs everywhere |
| Transport Module | ON | Disabling removes transport management |
| Integrated Coaching | OFF for small groups | JEE/NEET integrated track |
| IIT Foundation (Class 6–10) | OFF for most | Foundation program tracking |
| Zone Management | ON for large, OFF for small | Based on group type |
| WhatsApp Notifications | ON | Requires WA Business API configured |
| SMS Notifications | ON | Requires SMS gateway configured |
| Parental App Access | ON | Parents can access student portal |
| Student Self-Registration | OFF | Students can self-register |
| Multi-Board Affiliation | OFF | Branch can have multiple board affiliations |

**Warning dialog for disabling critical features:** "Disabling [Feature] will hide [Feature] functionality for all [N] branches immediately. Are you sure?"

**[Save Toggles] button.**

---

### Tab 5: Notifications

**Display:** Per-event notification configuration.

| Event | WhatsApp | SMS | Email | In-App |
|---|---|---|---|---|
| Fee Reminder | ON | ON | OFF | ON |
| Exam Schedule Notification | ON | OFF | ON | ON |
| Attendance Alert (low) | ON | ON | OFF | OFF |
| BGV Expiry Alert | ON | OFF | ON | OFF |
| Circular from HQ | ON | OFF | ON | ON |
| Escalation Created | ON | OFF | ON | ON |
| Policy Published | ON | OFF | ON | ON |
| Board Meeting Reminder | ON | OFF | ON | ON |

**Per-channel toggle per event.**

**Advance notice settings:** For reminders — how many days before event to send.

**[Save Notification Defaults] button.**

---

### Tab 6: EduForge Subscription

**Display:** Read + limited edit (billing contact editable, plan/seats managed by EduForge support).

| Field | Value | Editable? |
|---|---|---|
| Current Plan | Growth · Enterprise · Custom | No — contact support |
| Branches | 48 / 50 included | No |
| Active Users | 1,247 / 2,000 seats | No |
| Renewal Date | [date] | No |
| Annual Contract Value | ₹[amount] | No |
| Billing Contact Name | [Name] | ✅ |
| Billing Contact Email | [email] | ✅ |
| Billing Contact Mobile | [mobile] | ✅ |
| Support Tier | Standard / Priority / Dedicated | No |
| Raise Support Ticket | [button] | Opens EduForge support portal |
| Plan Upgrade Request | [button] | Triggers account manager contact |

**[Save Billing Contact] button.**

---

### Tab 7: Integrations

| Integration | Status | Actions |
|---|---|---|
| WhatsApp Business API | Connected / Not Connected | [Configure] [Disconnect] |
| SMS Gateway (e.g. MSG91) | Connected | [Configure] [Test] [Disconnect] |
| Email (SMTP / SendGrid) | Connected | [Configure] [Test] |
| Google Maps API | Connected | [Configure] |
| Payment Gateway | Not Connected | [Connect] |
| Biometric Attendance | Connected (2 branches) | [Manage] |
| CCTV Integration | Not Connected | [Connect] |

**[Configure] button:** Opens configuration drawer for that integration.

---

## 5. Drawers & Modals

### 5.1 Modal: `feature-disable-warning`
- **Width:** 480px
- **For critical feature disabling (Hostel, WhatsApp, Zone)**
- **Content:** Impact summary — "Disabling [Feature] will affect [N] branches and [N] users immediately"
- **Buttons:** [Disable Feature] (danger) + [Cancel]

### 5.2 Drawer: `integration-configure`
- **Width:** 560px
- **Specific to each integration** (different fields per integration)
- **WhatsApp:** API Key, Phone number, Webhook URL, Test Message button
- **SMS:** Provider (dropdown), API Key, Sender ID, Test SMS button
- **Email:** SMTP host/port/user/pass OR SendGrid API key, [Test Email] button

### 5.3 Modal: `integration-test`
- **Width:** 380px
- **Content:** "Send a test [WhatsApp/SMS/Email]?" + destination field (mobile/email)
- **Buttons:** [Send Test] + [Cancel]
- **On result:** "Test delivered successfully" or "Test failed: [error]" shown inline

---

## 6. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Settings saved | "[Section] settings saved" | Success | 4s |
| Feature toggled | "[Feature] enabled/disabled for all branches" | Warning | 6s |
| Branding updated | "Branding updated — may take a few minutes to appear everywhere" | Info | 6s |
| Integration connected | "[Integration] connected successfully" | Success | 4s |
| Integration test passed | "Test message sent and delivered successfully" | Success | 4s |
| Integration test failed | "Test failed: [error]. Check your configuration." | Error | Manual |
| Unsaved changes | "You have unsaved changes. Save before leaving." | Warning | 6s |

---

## 7. Empty States

No empty states — Settings is always pre-populated (group exists, settings have defaults).

If a section is not configured: Shows a "Not configured" badge + prompt to configure.

---

## 8. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: tab headers + current tab content form skeleton |
| Tab switch | Form field skeleton for new tab |
| Image upload | Progress bar in upload area |
| Integration configure drawer | Spinner in drawer |
| Integration test | Spinner in Test button |
| Settings save | Spinner in Save button + "Saving…" text |

---

## 9. Role-Based UI Visibility

| Element | Chairman/MD | CEO |
|---|---|---|
| All tabs | ✅ | ✅ |
| Feature disable (critical) | ✅ (warning modal) | ✅ (warning modal) |
| EduForge Subscription fields | ✅ | ✅ |
| [Plan Upgrade Request] | Chairman/MD | ❌ |
| Integration [Disconnect] | ✅ | ✅ |
| Integration [Configure] | ✅ | ✅ |
| Branding changes | ✅ | ✅ |
| Academic Year changes | ✅ | ✅ |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/settings/` | JWT (G4/G5) | All settings |
| PUT | `/api/v1/group/{id}/settings/profile/` | JWT (G4/G5) | Update profile |
| PUT | `/api/v1/group/{id}/settings/branding/` | JWT (G4/G5) | Update branding |
| POST | `/api/v1/group/{id}/settings/branding/logo/` | JWT (G4/G5) | Upload logo |
| PUT | `/api/v1/group/{id}/settings/academic-year/` | JWT (G4/G5) | Update academic year |
| PUT | `/api/v1/group/{id}/settings/features/` | JWT (G4/G5) | Update feature toggles |
| PUT | `/api/v1/group/{id}/settings/notifications/` | JWT (G4/G5) | Update notification defaults |
| PUT | `/api/v1/group/{id}/settings/billing-contact/` | JWT (G4/G5) | Update billing contact |
| GET | `/api/v1/group/{id}/settings/integrations/` | JWT (G4/G5) | Integration status |
| PUT | `/api/v1/group/{id}/settings/integrations/{name}/` | JWT (G4/G5) | Configure integration |
| POST | `/api/v1/group/{id}/settings/integrations/{name}/test/` | JWT (G4/G5) | Test integration |
| DELETE | `/api/v1/group/{id}/settings/integrations/{name}/` | JWT (G4/G5) | Disconnect integration |

---

## 11. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | GET `.../settings/?tab=profile\|branding\|academic-year\|features\|notifications\|subscription\|integrations` | `#settings-tab-content` | `innerHTML` |
| Save profile tab | `submit` | PUT `.../settings/profile/` | `#settings-tab-content` | `innerHTML` |
| Save branding tab | `submit` | PUT `.../settings/branding/` | `#settings-tab-content` | `innerHTML` |
| Logo upload | `change` | POST `.../settings/branding/logo/` | `#logo-preview` | `innerHTML` |
| Save academic year | `submit` | PUT `.../settings/academic-year/` | `#settings-tab-content` | `innerHTML` |
| Feature toggle change | `change` | PUT `.../settings/features/` | `#feature-toggle-{name}` | `outerHTML` |
| Save notification defaults | `submit` | PUT `.../settings/notifications/` | `#settings-tab-content` | `innerHTML` |
| Save billing contact | `submit` | PUT `.../settings/billing-contact/` | `#billing-form-result` | `innerHTML` |
| Open integration configure drawer | `click` | GET `.../settings/integrations/{name}/` | `#drawer-body` | `innerHTML` |
| Integration test | `click` | POST `.../settings/integrations/{name}/test/` | `#test-result-{name}` | `innerHTML` |
| Disconnect integration (confirm) | `click` | DELETE `.../settings/integrations/{name}/` | `#integration-row-{name}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
