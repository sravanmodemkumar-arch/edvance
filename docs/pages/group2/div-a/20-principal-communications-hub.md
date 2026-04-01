# 20 — Principal Communications Hub

> **URL:** `/group/gov/communications/`
> **File:** `20-principal-communications-hub.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exec Secretary G3 (full) · Chairman G5 · MD G5 · CEO G4 · President G4 · VP G4 (view) · Trustee G1 (read)

---

## 1. Purpose

Central repository of all circulars and communications sent from Group HQ to branch principals.
The Executive Secretary composes and sends here; all G4/G5 roles can view the history and
delivery status. Per-principal delivery tracking ensures no principal can claim they "didn't receive"
a circular — the platform records Sent, Delivered, and Opened timestamps per principal.

---

## 2. Role Access

| Role | Access | Notes |
|---|---|---|
| Exec Secretary | Full — compose, send, track, resend | Primary owner |
| Chairman/MD | View all circulars + delivery status | Oversight |
| CEO/President/VP | View all circulars | No compose |
| Trustee | Read — circular titles and dates only (no body) | Governance view |
| Advisor | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Principal Communications Hub
```

### 3.2 Page Header
```
Principal Communications Hub                           [+ Compose Circular]  [Export Log ↓]
[N] circulars this month · [N] pending reads          (Exec Secretary only)
```

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Circulars Sent (Month) | N |
| Delivered to All | N (green badge) |
| Partially Delivered | N (yellow) |
| Pending (not opened) | N (red if >0) |
| Templates Saved | N |

---

## 4. Circulars Table

**Search:** Circular title, sender name. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Month | Month picker | Last 12 months |
| Type | Multi-select | Circular · Notice · Reminder · Emergency Alert · Event |
| Status | Multi-select | All Delivered · Partial · None Opened · Draft |
| Channel | Multi-select | WhatsApp · Email · In-app |
| Reply Required | Checkbox | Show circulars that requested a reply |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Title | Text + link | ✅ | Opens `circular-detail` drawer |
| Type | Badge | ✅ | |
| Sent Date | Date + time | ✅ | |
| Channels | Icon group | ❌ | WhatsApp/Email/In-app icons |
| Total Recipients | Number | ✅ | Count of principals targeted |
| Delivered | Number + bar | ✅ | Green when = Total |
| Opened / Read | Number + bar | ✅ | |
| Replied | Number | ✅ | Only if reply was requested |
| Pending (not opened) | Number | ✅ | Red if >0 |
| Status | Badge | ✅ | Fully Read · Partial · Draft · Scheduled |
| Actions | — | ❌ | View · Resend to Pending · Download Report |

**Default sort:** Sent Date descending.

**Pagination:** 25/page.

**Row actions:**
| Action | Visible To | Notes |
|---|---|---|
| View | All | Opens `circular-detail` drawer |
| Resend to Pending | Exec Secretary | Sends WhatsApp to unopened principals |
| Download Report | Exec Secretary/Chairman/MD | PDF delivery audit report per circular |

---

## 5. Drawers & Modals

### 5.1 Drawer: `communications-compose` — Compose & Send Circular
- **Trigger:** [+ Compose Circular] header button
- **Width:** 680px
- **Tabs:** Compose · Template · Recipients · Schedule

#### Tab: Compose
| Field | Type | Required | Validation |
|---|---|---|---|
| Subject / Title | Text | ✅ | Min 5, max 200 chars |
| Circular Type | Select | ✅ | Circular · Notice · Reminder · Emergency Alert · Event |
| Priority | Radio | ✅ | Normal · Urgent |
| Body | Rich text editor (TipTap) | ✅ | Min 20 chars · Char counter |
| Attachments | File upload | ❌ | PDF/DOCX/JPG · Max 5 files · 10MB each |
| Request Reply? | Toggle | ❌ | Default off |
| Reply Deadline | Date | Conditional | Required if reply requested |
| Reply Instructions | Textarea | Conditional | What should principals reply with |

#### Tab: Template
- List of saved templates: Name · Category · Last Used Date · [Use] [Edit] [Delete]
- [Save Current as Template] button — saves Compose tab content
- Template categories: Term Start · Exam Notice · Fee Reminder · Holiday · Emergency · PTM · Event

#### Tab: Recipients
| Field | Type | Required | Validation |
|---|---|---|---|
| Send To | Radio | ✅ | All Principals · Select Branches · Select Individuals |
| Branches | Multi-select | Conditional | Shows all active branches |
| Individuals | Search + multi-select | Conditional | Search principals by name |
| Preview | Read-only | — | "Will send to [N] principals" + list preview |
| Exclude | Multi-select | ❌ | Exclude specific principals |

#### Tab: Schedule
| Field | Type | Required | Validation |
|---|---|---|---|
| Send Timing | Radio | ✅ | Send Now · Schedule for Later |
| Scheduled Date & Time | Datetime | Conditional | Required if scheduled · Must be future |
| Delivery Channel | Checkbox | ✅ | WhatsApp (default on) · Email · In-app |
| WhatsApp Message | Read-only preview | — | Shows how circular will appear on WhatsApp (truncated) |

**Submit:** [Send Circular] or [Schedule Circular] — disabled until all required fields valid.
**Unsaved changes guard:** Backdrop click triggers "Unsaved changes — are you sure?" modal.

### 5.2 Drawer: `circular-detail` — View Circular + Delivery Tracking
- **Trigger:** Circular title click or View action
- **Width:** 680px
- **Tabs:** Content · Per-Principal Status · Replies · Audit

#### Tab: Content
- Full circular body (rendered rich text or PDF viewer)
- All metadata: type, priority, channels, sent date, attachments
- Reply requirement details (if applicable)

#### Tab: Per-Principal Status
**Table:**
| Column | Type | Sortable | Notes |
|---|---|---|---|
| Principal Name | Text | ✅ | |
| Branch | Text | ✅ | |
| Channel | Badge | ❌ | WhatsApp/Email |
| Status | Badge | ✅ | Delivered · Opened · Not Opened · Failed |
| Delivered At | Datetime | ✅ | |
| Opened At | Datetime | ✅ | |
| Reply | Yes/No | ✅ | If reply requested |
| Actions | — | ❌ | [Resend] per row |

**Bulk:** [Resend to All Not-Opened] button at top.

#### Tab: Replies
- Table: Principal · Branch · Reply Date · Reply Content
- Only shown if "Request Reply" was enabled
- [Download Replies CSV] button

#### Tab: Audit
- Delivery audit log: timestamp, event (sent/delivered/opened/failed), channel, message ID

---

## 6. Template Management (accessible from Compose → Template tab)

**Templates table:** Name · Category · Last Modified · [Use] [Edit] [Delete].

Saved templates reduce compose time from 10+ minutes to 2 minutes for routine communications.

---

## 7. Charts

### 7.1 Circular Delivery Performance (last 6 months)
- **Type:** Grouped bar — Sent count · Fully Delivered % · Opened % per month
- **X-axis:** Months
- **Y-axis:** Count (bars) · % (line overlay)
- **Export:** PNG

### 7.2 Channel Effectiveness
- **Type:** Horizontal bar — WhatsApp vs Email open rates
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Circular sent | "Circular sent to [N] principals" | Success | 4s |
| Circular scheduled | "Circular scheduled for [date time]" | Info | 4s |
| Resend triggered | "Reminder sent to [N] principals who haven't opened" | Success | 4s |
| Template saved | "Template saved as [Name]" | Success | 4s |
| Report downloaded | "Delivery report downloading…" | Info | 4s |
| Send failed | "Failed to send circular. Check your connection." | Error | Manual |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No circulars | "No circulars sent" | "Compose your first circular to branch principals" | [+ Compose Circular] |
| All opened | "All principals have opened this circular" | "100% delivery confirmed" | — |
| No replies | "No replies received" | "Principals haven't replied yet" | — |
| No templates | "No saved templates" | "Save a circular as a template to speed up future communications" | [Compose & Save] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) |
| Table filter | Inline skeleton rows |
| Compose drawer open | Spinner in drawer |
| Circular send | Full-page overlay "Sending to [N] principals…" |
| Per-Principal Status tab | Table skeleton rows |
| Resend | Spinner in Resend button |

---

## 11. Role-Based UI Visibility

| Element | Exec Secretary | Chairman/MD | CEO/Pres/VP | Trustee |
|---|---|---|---|---|
| [+ Compose Circular] | ✅ | ❌ | ❌ | ❌ |
| [Resend to Pending] | ✅ | ❌ | ❌ | ❌ |
| [Download Report] | ✅ | ✅ | ❌ | ❌ |
| Circular body content | ✅ | ✅ | ✅ | ❌ (titles only) |
| Per-Principal Status tab | ✅ | ✅ | ❌ | ❌ |
| Replies tab | ✅ | ✅ | ❌ | ❌ |
| Template management | ✅ | ❌ | ❌ | ❌ |
| [Export Log] | ✅ | ✅ | ❌ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/communications/circulars/` | JWT | Circular list |
| POST | `/api/v1/group/{id}/communications/circulars/` | JWT (G3 Sec) | Create + send circular |
| GET | `/api/v1/group/{id}/communications/circulars/{cid}/` | JWT | Circular detail |
| GET | `/api/v1/group/{id}/communications/circulars/{cid}/delivery/` | JWT | Per-principal delivery |
| POST | `/api/v1/group/{id}/communications/circulars/{cid}/resend/` | JWT (G3 Sec) | Resend to pending |
| GET | `/api/v1/group/{id}/communications/circulars/{cid}/replies/` | JWT (G3 Sec) | Replies list |
| GET | `/api/v1/group/{id}/communications/templates/` | JWT (G3 Sec) | Templates list |
| POST | `/api/v1/group/{id}/communications/templates/` | JWT (G3 Sec) | Save template |
| GET | `/api/v1/group/{id}/communications/circulars/{cid}/report/` | JWT | Download report |
| GET | `/api/v1/group/{id}/communications/charts/delivery/` | JWT | Delivery performance chart |

---

## HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search circulars | `input delay:300ms` | GET `.../communications/?q=` | `#communications-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../communications/?status=&date=&branch=` | `#communications-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../communications/?sort=&dir=` | `#communications-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../communications/?page=` | `#communications-table-section` | `innerHTML` |
| Open compose drawer | `click` | GET `.../communications/new/` | `#drawer-body` | `innerHTML` |
| Open circular detail drawer | `click` | GET `.../communications/{cid}/` | `#drawer-body` | `innerHTML` |
| Detail drawer tab switch | `click` | GET `.../communications/{cid}/?tab=content\|delivery\|replies` | `#circular-drawer-tab` | `innerHTML` |
| Delivery status refresh | `click` | GET `.../communications/{cid}/delivery/` | `#delivery-tab-content` | `innerHTML` |
| Resend to not-opened | `click` | POST `.../communications/{cid}/resend-unopened/` | `#resend-result` | `innerHTML` |
| Delivery stats auto-refresh | `every 5m` | GET `.../communications/stats/` | `#comms-stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
