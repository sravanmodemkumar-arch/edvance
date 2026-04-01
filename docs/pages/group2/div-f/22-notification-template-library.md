# 22 — Notification Template Library

- **URL:** `/group/it/notifications/templates/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4) — Primary owner

---

## 1. Purpose

The Notification Template Library is the central repository for every notification template used across all channels — WhatsApp, SMS, Email, and In-App — in the entire EduForge group. While individual channel configuration pages (Files 19–21) manage provider credentials and delivery settings, this page is the single authoritative source for the message content itself. Branch portals cannot create their own notification templates; they can only use templates published from this library. This ensures consistency of communication, brand voice, and legal compliance (e.g., DLT-registered SMS templates, Meta-approved WhatsApp templates) across every branch in the group.

The library serves two audiences. First, the IT Admin who configures and maintains templates — creating new templates, editing variable mappings, testing before activation, and archiving obsolete ones. Second, the IT Support Executive and Integration Manager who need to verify which template is active for a specific notification type and test delivery to diagnose issues.

Template variable substitution is the technical heart of this library. Every template contains placeholders — `{{student_name}}`, `{{fee_amount}}`, `{{exam_date}}` — that EduForge's notification engine replaces with live values at send time. The create/edit drawer includes a variable reference panel: a categorised list of every available variable, what data it maps to, and which modules supply it. This prevents IT Admins from inventing variable names that do not exist in the backend and makes the template authoring experience self-documenting.

The Duplicate action is a key productivity feature: creating a similar template for a different language or a slightly different use case is done by duplicating an existing template and editing only the changed fields, rather than building from scratch. Archiving retires templates without deleting them — archived templates are retained in the library for audit and can be re-activated if needed.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + write (create, edit, test, archive) | Primary operator |
| Group IT Director | G4 | Full read + write | Strategic oversight |
| Group EduForge Integration Manager | G4 | Full read + write (templates only; no channel config) | Manages template content |
| Group IT Support Executive | G3 | Read-only + Test only | Verify and test templates for support diagnosis |
| Group Cybersecurity Officer | G1 | Read-only (Auth category only) | Reviews OTP and authentication templates |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Notifications → Template Library
```

### 3.2 Page Header
- **Title:** `Notification Template Library`
- **Subtitle:** `[Total] Templates · [N] WhatsApp · [N] SMS · [N] Email · [N] In-App`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `+ Create Template` · `Advanced Filters` · `Export`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| OTP/Authentication template is inactive or archived | "No active Authentication template found for [Channel]. OTP delivery for that channel will fail." | Red (non-dismissible) |
| Templates with variables referencing deprecated fields | "[N] template(s) use variables that are no longer available in the system. Edit to fix broken variables." | Amber |
| SMS templates with missing DLT ID | "[N] SMS template(s) are missing DLT registration IDs and cannot be delivered in India." | Amber |
| WhatsApp templates with Rejected Meta status | "[N] WhatsApp template(s) have been rejected by Meta and are not deliverable." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Templates | All templates regardless of channel or status | Blue | No filter |
| WhatsApp Templates | Templates with channel = WhatsApp | Blue | Filtered by WhatsApp |
| SMS Templates | Templates with channel = SMS | Blue | Filtered by SMS |
| Email Templates | Templates with channel = Email | Blue | Filtered by Email |

**KPI Colour Rules:** Total Templates — Blue (informational); WhatsApp Templates — Blue if > 0, Grey if none; SMS Templates — Blue if > 0, Grey if none; Email Templates — Blue if > 0, Grey if none.

---

## 5. Main Table — Notification Template Library

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Template Name | Text (link opens View drawer) | Yes | Yes (text search) |
| Channel | Badge (WhatsApp / SMS / Email / In-App) | No | Yes (multi-select) |
| Category | Badge (Auth / Fee / Exam / Attendance / Admission / HR / General) | No | Yes (multi-select) |
| Language | Badge (English / Telugu / Hindi / Tamil / Kannada) | No | Yes (multi-select) |
| Status | Badge (Active / Draft / Archived) | No | Yes |
| Last Modified | Date | Yes | No |
| Usage Count (30d) | Number | Yes | No |
| Actions | View / Edit / Test / Duplicate / Archive | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Channel | Multi-select dropdown | WhatsApp / SMS / Email / In-App |
| Category | Multi-select dropdown | Auth / Fee / Exam / Attendance / Admission / HR / General |
| Language | Multi-select dropdown | All configured languages |
| Status | Checkbox | Active / Draft / Archived |

### 5.2 Search
- Full-text: Template Name
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `template-create` — Create New Template
- **Trigger:** `+ Create Template` button
- **Width:** 560px
- **Layout:** Two-column within drawer — left column (form fields) and right column (variable reference panel)
- **Left column fields:**
  - Template Name (required, text, unique per channel)
  - Channel (required, dropdown: WhatsApp / SMS / Email / In-App)
  - Category (required, dropdown: Auth / Fee / Exam / Attendance / Admission / HR / General)
  - Language (required, dropdown)
  - **If WhatsApp:**
    - Template Type (dropdown: Text / Text + Header / Text + Header + Footer / Text + Buttons)
    - Header (optional, text — 60 chars max)
    - Body (required, textarea — 1024 chars max; `{{variable}}` syntax for placeholders)
    - Footer (optional, text — 60 chars max)
    - Buttons (optional; up to 3; type: Quick Reply or URL with label and value)
    - Meta Template Category (radio: Authentication / Utility / Marketing)
  - **If SMS:**
    - Body (required, textarea — 160 chars guidance with counter)
    - DLT Template ID (text; required before Status can be set to Active)
  - **If Email:**
    - Subject Line (required, text; supports `{{variables}}`)
    - HTML Body (rich-text / code editor toggle)
    - Plain Text Body (textarea; fallback)
  - **If In-App:**
    - Title (required, text — 80 chars max)
    - Body (required, textarea — 300 chars max)
    - Link / Action (optional; label + URL or internal page path)
  - Status (dropdown: Active / Draft)
- **Right column — Variable Reference Panel:**
  - Categorised accordion list of all available variables:
    - Student: `{{student_name}}`, `{{student_id}}`, `{{student_class}}`, `{{student_section}}`
    - Parent: `{{parent_name}}`, `{{parent_mobile}}`
    - Fee: `{{fee_amount}}`, `{{fee_due_date}}`, `{{fee_type}}`, `{{receipt_number}}`
    - Exam: `{{exam_name}}`, `{{exam_date}}`, `{{exam_hall}}`, `{{subject_name}}`
    - Attendance: `{{attendance_date}}`, `{{attendance_status}}`, `{{arrival_time}}`
    - Admission: `{{admission_number}}`, `{{admission_date}}`, `{{branch_name}}`
    - Auth: `{{otp}}`, `{{otp_expiry_minutes}}`, `{{username}}`
    - General: `{{school_name}}`, `{{group_name}}`, `{{current_date}}`, `{{academic_year}}`
  - Each variable is clickable — clicking inserts it at the cursor position in the active body textarea
- **Bottom actions:** Save as Draft · Save and Activate · Cancel

### 6.2 Drawer: `template-view` — View Template (Read-Only)
- **Trigger:** Click Template Name or Actions → View
- **Width:** 560px
- **Content:**
  - All template fields in read-only display
  - Variable substitution preview: a "Preview with Sample Data" toggle fills all `{{variables}}` with sample values so the rendered message is visible
  - Metadata: Created by, created date, last modified by, last modified date, 30-day usage count
  - For WhatsApp: Meta approval status with date; if Rejected, shows Meta's rejection reason
  - For SMS: DLT registration ID, DLT status
  - For Email: HTML preview rendered in sandboxed iframe (desktop/mobile toggle)

### 6.3 Drawer: `template-edit` — Edit Template
- **Trigger:** Actions → Edit
- **Width:** 560px
- **Content:** Identical to Create drawer but pre-populated with existing values
- **Important:** If the template is Active and used by live notification triggers, a warning is shown: "This template is currently in active use. Changes will apply immediately to all future sends. Test before saving."
- **Channel field is read-only** (cannot change channel of an existing template — create a new one instead)

### 6.4 Modal: Test Template
- **Trigger:** Actions → Test
- **Type:** Centered modal (480px)
- **Content:** "Send a test notification using '[Template Name]' via [Channel]."
- **Fields:**
  - Test Recipient: Mobile number (for WhatsApp/SMS) or email address (for Email) or "In-App test user" dropdown (for In-App)
  - Variable values: one input per variable in the template body (pre-filled with sample values; editable)
- **Buttons:** Send Test · Cancel
- **On send:** Result shown inline in modal — Sent (green), Delivered (green), Failed (red with error message), or In-App notification previewed inline

### 6.5 Modal: Duplicate Template
- **Trigger:** Actions → Duplicate
- **Type:** Small modal (400px)
- **Fields:**
  - New Template Name (pre-filled as "[Original Name] — Copy"; editable)
  - Language (dropdown; pre-filled with original language; change to quickly create a translated version)
  - Status of Copy (radio: Draft / Active)
- **Buttons:** Duplicate · Cancel
- **On confirm:** New template record created with status Draft (or Active); opens Edit drawer immediately for the new template

### 6.6 Modal: Archive Template
- **Trigger:** Actions → Archive
- **Type:** Centered modal (440px)
- **Content:** "Archive '[Template Name]'? Archived templates will no longer be sent. If this template is currently linked to an active notification trigger, those notifications will silently fail. Confirm all triggers have been reassigned before archiving."
- **Fields:** Reason for archiving (optional textarea)
- **Buttons:** Confirm Archive · Cancel
- **Note:** Archives are permanent. To restore, duplicate the archived template and activate the copy.

---

## 7. Charts

No dedicated chart section. The Usage Count (30d) column in the main table provides a quick at-a-glance usage ranking. Full notification analytics (send volume, delivery rates by template) are on the IT Analytics page.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Template created and activated | "Template '[Name]' created and is now Active." | Success | 4s |
| Template saved as draft | "Template '[Name]' saved as Draft. Activate it when ready." | Info | 4s |
| Template updated | "Template '[Name]' updated." | Success | 3s |
| Template duplicated | "Template '[Name] — Copy' created as Draft. Edit it to customise." | Success | 4s |
| Template archived | "Template '[Name]' archived and removed from active use." | Warning | 4s |
| Test message sent | "Test [Channel] notification sent to [recipient]." | Info | 4s |
| Test message failed | "Test failed: [error message]." | Error | 6s |
| Template test failed (SMS) | Error: `SMS test failed: [error message].` | Error | 5s |
| Template test failed (Email) | Error: `Email test failed: [error message].` | Error | 5s |
| Duplicate template name conflict | "A template named '[Name]' already exists for this channel. Choose a different name." | Error | 5s |
| Export triggered | "Template library export is being prepared." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No templates exist | "Template Library is Empty" | "No notification templates have been created yet. Create the first template to begin sending notifications." | + Create Template |
| No results for filter | "No Templates Match" | "No templates match the selected channel, category, or language filters." | Clear Filters |
| No results for search | "No Templates Found" | "No templates match '[search term]'. Check the template name and try again." | Clear Search |
| In-App channel — no templates | "No In-App Templates" | "No in-app notification templates have been created. Create one to send in-portal notifications." | + Create Template |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 4 KPI shimmer cards + table skeleton (15 rows × 8 columns) |
| Filter or search applied | Table rows shimmer; KPI bar does not reload |
| Create / Edit drawer open | 560px drawer skeleton; variable reference panel loads lazily after main form |
| Variable reference panel expand (accordion) | Section-level spinner; variables load from API |
| View drawer open (Email template with HTML preview) | 560px skeleton; iframe loads after text fields |
| Test modal send | Modal send button spinner; inline result replaces spinner |
| Archive confirm | Button spinner; modal closes; table row removed or status badge updates |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | Integration Manager (G4) | IT Support Executive (G3) | Cybersecurity Officer (G1) |
|---|---|---|---|---|---|
| KPI bar | Visible | Visible | Visible | Visible | Visible |
| Full table | Visible | Visible | Visible | Visible | Auth category only |
| + Create Template | Visible | Visible | Visible | Hidden | Hidden |
| View action | Visible | Visible | Visible | Visible | Visible |
| Edit action | Visible | Visible | Visible | Hidden | Hidden |
| Test action | Visible | Visible | Visible | Visible | Hidden |
| Duplicate action | Visible | Visible | Visible | Hidden | Hidden |
| Archive action | Visible | Visible | Hidden | Hidden | Hidden |
| Export | Visible | Visible | Visible | Hidden | Hidden |
| Variable Reference Panel | Visible | Visible | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/notifications/templates/` | JWT (G1+) | Paginated template library with filters |
| POST | `/api/v1/it/notifications/templates/` | JWT (G4) | Create new template |
| GET | `/api/v1/it/notifications/templates/{id}/` | JWT (G1+) | Full template detail |
| PATCH | `/api/v1/it/notifications/templates/{id}/` | JWT (G4) | Update template |
| POST | `/api/v1/it/notifications/templates/{id}/duplicate/` | JWT (G4) | Duplicate a template |
| POST | `/api/v1/it/notifications/templates/{id}/archive/` | JWT (G4) | Archive a template |
| POST | `/api/v1/it/notifications/templates/{id}/test/` | JWT (G3+) | Send test notification |
| GET | `/api/v1/it/notifications/templates/variables/` | JWT (G4) | All available template variables by category |
| GET | `/api/v1/it/notifications/templates/kpis/` | JWT (G1+) | KPI card values |
| GET | `/api/v1/it/notifications/templates/export/` | JWT (G4) | Export template library as CSV/XLSX |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/notifications/templates/kpis/` | `#kpi-bar` | `innerHTML` |
| Load templates table | `load` | GET `/api/v1/it/notifications/templates/` | `#templates-table` | `innerHTML` |
| Search templates | `input` (300ms debounce) | GET `/api/v1/it/notifications/templates/?q=...` | `#templates-table` | `innerHTML` |
| Apply filters | `change` on any filter | GET `/api/v1/it/notifications/templates/?channel=...&category=...` | `#templates-table` | `innerHTML` |
| Paginate | `click` on page control | GET `/api/v1/it/notifications/templates/?page=N` | `#templates-table` | `innerHTML` |
| Open view drawer | `click` on Template Name | GET `/api/v1/it/notifications/templates/{id}/` | `#template-drawer` | `innerHTML` |
| Load variable reference panel | `click` on accordion category | GET `/api/v1/it/notifications/templates/variables/?category=...` | `#var-panel-{category}` | `innerHTML` |
| Submit create / edit form | `click` on Save | POST or PATCH `/api/v1/it/notifications/templates/` | `#templates-table` | `innerHTML` |
| Confirm duplicate | `click` on Duplicate | POST `/api/v1/it/notifications/templates/{id}/duplicate/` | `#templates-table` | `innerHTML` |
| Confirm archive | `click` on Confirm Archive | POST `/api/v1/it/notifications/templates/{id}/archive/` | `#templates-table` | `innerHTML` |
| Send test notification | `click` on Send Test | POST `/api/v1/it/notifications/templates/{id}/test/` | `#test-result` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- OTP template set Inactive: IT Admin + IT Director (in-app red non-dismissible) immediately
- All templates for a channel inactive: IT Admin (in-app amber + email)

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
