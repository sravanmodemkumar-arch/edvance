# 21 — Group Announcements

> **URL:** `/group/gov/announcements/`
> **File:** `21-group-announcements.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Exec Secretary G3 (compose) · Chairman G5 (approve) · MD G5 (approve) · CEO G4 (approve) · Others view published only

---

## 1. Purpose

Multi-channel announcement broadcasting to students, parents, or staff across all branches.
Unlike circulars (which are for principals only), announcements can target students and parents
via WhatsApp Broadcast, SMS, Email, and In-app notifications.

The Exec Secretary drafts and schedules; Chairman or CEO must approve before broadcast.

Channels: WhatsApp Broadcast · SMS · Email · In-app Notification.

Targeting: By branch · by class · by student type · by role.

---

## 2. Role Access

| Role | Compose/Draft | Approve | View Published |
|---|---|---|---|
| Exec Secretary | ✅ | ❌ | ✅ |
| Chairman | ❌ | ✅ | ✅ |
| MD | ❌ | ✅ | ✅ |
| CEO | ❌ | ✅ | ✅ |
| President/VP | ❌ | ❌ | ✅ |
| Trustee/Advisor | ❌ | ❌ | Titles only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Group Announcements
```

### 3.2 Page Header
```
Group Announcements                                    [+ New Announcement]  [Export ↓]
[N] published this month · [N] pending approval        (Exec Secretary only)
```

### 3.3 Tabs
```
Pending Approval ([N])  |  Scheduled ([N])  |  Published  |  Drafts
```

**Pending Approval tab** — visible to Chairman/CEO for approval actions.

---

## 4. Announcements Table

**Search:** Title, announcement type. Debounce 300ms.

**Filters:** Channel · Targeting · Status · Date range.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Title | Text + link | ✅ | Opens `announcement-view` drawer |
| Channel | Icon group | ❌ | WhatsApp/SMS/Email/In-app icons |
| Targeting | Badge | ✅ | All Students · By Branch · By Class |
| Recipient Count | Number | ✅ | Estimated reach |
| Status | Badge | ✅ | Draft · Pending Approval · Scheduled · Published |
| Scheduled / Sent | Datetime | ✅ | |
| Approved By | Text | ✅ | |
| Delivered | Progress | ✅ | For published: delivery % |
| Actions | — | ❌ | View · Edit (drafts) · Approve/Reject · Delete |

**Default sort:** Status (Pending first) then Scheduled date.

---

## 5. Drawers & Modals

### 5.1 Drawer: `announcement-compose`
- **Trigger:** [+ New Announcement]
- **Width:** 680px
- **Tabs:** Compose · Targeting · Channel · Schedule · Preview

#### Tab: Compose
| Field | Type | Required | Validation |
|---|---|---|---|
| Title | Text | ✅ | Min 5, max 200 |
| Type | Select | ✅ | Exam Notice · Fee Reminder · Event · Holiday · Emergency · General |
| Priority | Radio | ✅ | Normal · Urgent |
| Message Body | Textarea | ✅ | Min 10, max 1000 chars · Character counter (SMS: 160 hard limit shown) |
| Attachments | File | ❌ | For Email/In-app only · PDF/Image · Max 5MB |

#### Tab: Targeting
| Field | Type | Required | Validation |
|---|---|---|---|
| Target Group | Radio | ✅ | All Students · All Parents · All Staff · All Students + Parents · By Branch · By Class · By Student Type |
| Branches | Multi-select | Conditional | |
| Classes | Multi-select | Conditional | |
| Student Types | Multi-select | Conditional | Day Scholar · Hosteler · etc. |
| Estimated Reach | Read-only | — | Auto-calculated: "~X,XXX recipients" |

#### Tab: Channel
| Channel | Toggle | Notes |
|---|---|---|
| WhatsApp Broadcast | Default ON | Requires WhatsApp Business API |
| SMS | Toggle | 160 char limit enforced |
| Email | Toggle | HTML email generated from message |
| In-app Notification | Toggle | Shows in student/parent app |

Character limit indicator: If SMS selected and message >160 chars → warning badge "SMS will be truncated at 160 chars".

#### Tab: Schedule
| Field | Type | Required | Validation |
|---|---|---|---|
| Send Timing | Radio | ✅ | Send Immediately · Schedule |
| Scheduled Date & Time | Datetime | Conditional | Future datetime required |

#### Tab: Preview
- WhatsApp preview: shows message as WhatsApp chat bubble
- SMS preview: plain text, character count
- Email preview: styled HTML email preview
- In-app preview: shows push notification mockup
- Tabs per channel selected

**Submit:** [Submit for Approval] button — saves as "Pending Approval" and notifies Chairman/CEO.

### 5.2 Drawer: `announcement-view`
- **Width:** 640px
- **Tabs:** Content · Analytics (published only)
- **Content tab:** Full announcement details — all fields read-only
- **Analytics tab** (only when Status = Published):
  - Delivered count per channel
  - Open rate (Email) / Read receipts (WhatsApp where available)
  - Click rate (if links in message)

### 5.3 Modal: `announcement-approve`
- **Trigger:** Chairman/MD/CEO row action or Pending Approval tab
- **Width:** 480px
- **Content:** Full announcement preview (title, message, targeting, channels, schedule)
- **Buttons:** [Approve & Schedule] (green) · [Reject with Reason] (red) · [Request Changes] (yellow) · [Cancel]

### 5.4 Modal: `announcement-reject`
- **Width:** 420px
- **Fields:** Reason (required, min 20 chars) — sent to Exec Secretary
- **Buttons:** [Reject] + [Cancel]

---

## 6. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Announcement submitted | "Announcement submitted for approval. Chairman/CEO notified." | Info | 4s |
| Approved and scheduled | "Announcement approved and scheduled for [datetime]" | Success | 4s |
| Approved and sent | "Announcement sent to [N] recipients" | Success | 4s |
| Rejected | "Announcement rejected. Reason sent to Secretary." | Warning | 4s |
| Draft saved | "Draft saved" | Info | 3s |
| Channel limit warning | "SMS message exceeds 160 chars and will be truncated" | Warning | 6s |

---

## 7. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No pending approvals | "Nothing pending approval" | "Draft announcements will appear here for review" | — |
| No published | "No announcements published" | "Approved announcements will appear here" | — |
| No drafts | "No drafts" | "Create a new announcement to get started" | [+ New Announcement] |

---

## 8. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 4 tab headers + table (8 rows) |
| Tab switch | Inline skeleton rows |
| Compose drawer | Spinner in drawer |
| Preview tab load | Spinner per channel preview panel |
| Announcement send | Full-page overlay "Broadcasting to [N] recipients…" |

---

## 9. Role-Based UI Visibility

| Element | Exec Secretary | Chairman/MD/CEO | President/VP | Trustee |
|---|---|---|---|---|
| [+ New Announcement] | ✅ | ❌ | ❌ | ❌ |
| [Approve/Reject] in Pending tab | ❌ | ✅ | ❌ | ❌ |
| Edit draft | ✅ | ❌ | ❌ | ❌ |
| Delete draft | ✅ | ❌ | ❌ | ❌ |
| Analytics tab (view) | ✅ | ✅ | ✅ | ❌ |
| Pending Approval tab | ✅ (view own) | ✅ (approve) | ❌ | ❌ |
| Published announcements | ✅ | ✅ | ✅ | Titles only |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/announcements/` | JWT | Announcements list |
| POST | `/api/v1/group/{id}/announcements/` | JWT (G3 Sec) | Create draft |
| GET | `/api/v1/group/{id}/announcements/{aid}/` | JWT | Announcement detail |
| PUT | `/api/v1/group/{id}/announcements/{aid}/` | JWT (G3 Sec) | Update draft |
| POST | `/api/v1/group/{id}/announcements/{aid}/submit/` | JWT (G3 Sec) | Submit for approval |
| POST | `/api/v1/group/{id}/announcements/{aid}/approve/` | JWT (G4 CEO/G5) | Approve |
| POST | `/api/v1/group/{id}/announcements/{aid}/reject/` | JWT (G4/G5) | Reject with reason |
| DELETE | `/api/v1/group/{id}/announcements/{aid}/` | JWT (G3 Sec) | Delete draft |
| GET | `/api/v1/group/{id}/announcements/{aid}/analytics/` | JWT | Delivery analytics |

---

## 11. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | GET `.../announcements/?tab=pending\|scheduled\|published\|drafts` | `#announcements-tab-content` | `innerHTML` |
| Search | `input delay:300ms` | GET `.../announcements/?q=` | `#announcements-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../announcements/?channel=&status=&date=` | `#announcements-table-section` | `innerHTML` |
| Open view drawer | `click` | GET `.../announcements/{aid}/` | `#drawer-body` | `innerHTML` |
| Open compose drawer | `click` | GET `.../announcements/new/` | `#drawer-body` | `innerHTML` |
| Approve (modal confirm) | `click` | POST `.../announcements/{aid}/approve/` | `#announcement-row-{aid}` | `outerHTML` |
| Reject (modal confirm) | `click` | POST `.../announcements/{aid}/reject/` | `#announcement-row-{aid}` | `outerHTML` |
| Estimated reach (targeting change) | `change` | GET `.../announcements/reach-estimate/?target=` | `#reach-estimate` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
