# D-19 — Notifications Inbox

> **Route:** `/content/notifications/`
> **Division:** D — Content & Academics
> **All Roles:** Content Director (18) · SME ×9 (19–27) · Question Reviewer (28) · Question Approver (29) · Notes Editor (30)
> **File:** `d-19-notifications.md`
> **Priority:** P1 — Required before first SME produces content (workflow feedback loop depends on it)
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Notifications Inbox
**Route:** `/content/notifications/`
**Part-load routes:**
- `/content/notifications/?part=unread-count` — badge count only (polled by nav bar bell icon every 60s)
- `/content/notifications/?part=notification-list` — full list (HTMX into page body)
- `/content/notifications/?part=preferences` — notification preferences panel

---

## 2. Purpose (Business Objective)

Every significant event in Division D triggers a notification: a question is returned, a batch import completes, a quota is updated, an escalation is sent. Without a central inbox, these notifications scatter across the platform — SMEs rely on the Returned tab in D-01, Reviewers rely on the 30s poll in D-03, Directors watch D-05 manually.

D-19 consolidates every notification into one inbox, accessible from any page via the bell icon in the top navigation bar. It is the connective tissue between all 20 Division D pages.

**Business goals:**
- Ensure no workflow event is missed regardless of which page the user is currently on
- Provide a complete history of notifications per user (read and unread)
- Allow users to configure which notification types they receive in-app vs email
- Maintain DPDPA compliance — notifications never contain personal names

---

## 3. Navigation — Bell Icon (Global Nav)

The bell icon lives in the top navigation bar on **every page in Division D** (and platform-wide).

- **Badge:** Red circle with unread count. Shows exact count 1–99. Shows "99+" when > 99 unread.
- **Click bell:** Opens a **notification popover** (mini inbox, 400px wide, max 8 notifications shown with "View All" link → D-19 full page).
- **Popover contents:** 8 most recent unread notifications, each with icon + title + "N min ago" relative time + one-line action button.
- **Mark All Read:** in the popover footer.
- **"View All Notifications":** full page → D-19.

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Filters

- H1: "Notifications"
- Filter bar:
  - Type filter (multi-select dropdown): All Types · Questions · Announcements · Feedback · Import · Quota · Escalations · Notes · System
  - Status: All · Unread · Read
  - Date range (default: last 30 days)
- "Mark All as Read" button (top-right)
- "Notification Preferences" link → Section 4

---

### Section 2 — Notification List

**Layout:** Vertical list, newest first. Each notification is a card.

**Unread notification card:**
- Left border: 3px blue accent
- Background: white
- Blue dot indicator (left of icon)

**Read notification card:**
- No border accent
- Background: light grey (#F8F9FA)
- No blue dot

**Card structure:**

```
[Icon]  [Title — bold]                           [Relative time]
        [Body — one line summary, truncated]
        [Action Button]                           [Mark Read ×]
```

**Action button:** Context-specific — navigates directly to the relevant resource:

| Notification Type | Action Button Label | Destination |
|---|---|---|
| Question Returned | "View Feedback" | D-01 Returned Questions tab (filtered to this question) |
| Question Passed to Approver | "View in Bank" | D-11 (for SME — their published question) |
| Quota Updated | "View Quota" | D-10 SME view |
| Director Announcement | "View Announcement" | D-01 Announcements tab |
| Review Escalation | "View Queue" | D-03 Assigned to Me tab |
| OOO Confirmed | "View Assignments" | D-15 Reviewer view |
| OOO Request Pending | "Confirm Backup" | D-15 Reviewer Assignments page |
| Critical Feedback Escalation | "Review Now" | D-16 (filtered to critical question) |
| Amendment Review Created | "Go to Queue" | D-04 Amendment Reviews tab |
| Note Request Assigned | "View Request" | D-17 Note Request List |
| SME Question Reassigned to Me | "View Questions" | D-01 My Questions tab |
| Import Batch Complete | "View Batch" | D-07 Import History |
| Import Batch Failed | "View Errors" | D-07 Import History (failed batch) |
| Bulk Retag Complete | "View Taxonomy" | D-09 |
| Pool Adequacy Alert | "View Pool Data" | D-14 Pool Adequacy tab |
| Bulk Archive Complete | "View Bank" | D-11 |
| Conversion Complete (Notes) | "Structure Note" | D-06 Incoming Queue |

**Dismissing a notification:** "Mark Read ×" button on each card (does not delete — marks as read).

**Pagination:** 25 notifications per page, numbered controls. "Showing X–Y of N".

---

### Section 3 — Notification Types by Role

**SME (Roles 19–27) receive:**
- ✅ Question returned by Reviewer — includes reason category (not reviewer's personal name)
- ✅ Quota updated by Director (from D-10)
- ✅ Director Announcement posted (from D-05) — Action Required announcements appear as sticky banner
- ✅ Question reassigned to them (if Director reassigns an SME's OOO queue)
- ✅ Bulk import batch completed (from D-07)
- ✅ Bulk import batch failed (from D-07)
- ✅ Version restored by Approver (from D-12)

**Reviewer (Role 28) receives:**
- ✅ Escalation notification (question past SLA, from D-05 Director escalate action)
- ✅ OOO period confirmed by Director (from D-15)
- ✅ Self-OOO request acknowledged (pending Director confirmation)
- ✅ Committee review question assigned to them as Reviewer 2

**Approver (Role 29) receives:**
- ✅ Critical feedback escalation (≥ 50 flags, from D-16)
- ✅ Amendment review created (from D-04/D-16 unpublish flow)
- ✅ Emergency bulk unpublish request requires their attention (from D-05 if Director requests)
- ✅ Pool adequacy critical alert (from D-14)

**Notes Editor (Role 30) receives:**
- ✅ Note request assigned to them (from D-17)
- ✅ Note returned by Director (from D-05 Notes Review tab)
- ✅ Note request deadline approaching (3 days before deadline)
- ✅ Conversion complete for uploaded note (from D-06)
- ✅ Conversion failed for uploaded note (from D-06)

**Content Director (Role 18) receives:**
- ✅ Critical feedback escalation (from D-16)
- ✅ Pool adequacy red alert (from D-14)
- ✅ Reviewer self-OOO request (requires Director confirmation)
- ✅ SME OOO set (confirming the system received it)
- ✅ Scheduled report completed (from D-18)
- ✅ Scheduled report failed (from D-18)
- ✅ Bulk retag job completed (from D-09 G10)
- ✅ Import batch completed for any SME (summary)

---

### Section 4 — Notification Preferences

**Route:** Accessible via "Notification Preferences" link on D-19 page + user profile menu.

**Two columns per notification type:**

| Notification Type | In-App (Toggle) | Email (Toggle) |
|---|---|---|
| Question Returned | ON (locked — cannot disable) | OFF |
| Quota Updated | ON | ON |
| Director Announcement — Info | ON | OFF |
| Director Announcement — Warning | ON | ON |
| Director Announcement — Action Required | ON (locked) | ON (locked) |
| Escalation Notification | ON (locked) | ON |
| OOO Confirmed | ON | OFF |
| Import Batch Complete | ON | OFF |
| Import Batch Failed | ON | ON |
| Note Request Assigned | ON (locked) | ON |
| Note Request Deadline Approaching | ON | ON |
| Pool Adequacy Alert | ON (locked — Director only) | ON |
| Amendment Review Created | ON (locked) | ON |

**"Locked" notifications:** Cannot be disabled. These are operational workflow notifications that users MUST receive (returned questions, action-required announcements, amendment reviews). The system enforces these regardless of preference.

**Email delivery:** Emails sent via platform email service (SES). Email content mirrors notification body. Author identity (personal name) excluded — role labels only (DPDPA).

**Digest mode:** Option to batch non-critical notifications into a daily digest email (sent at 8:00 AM IST). Reduces email noise for users who prefer minimal interruption.

---

### Section 5 — SME Out-of-Office (OOO) — Integrated Here

SME OOO is managed from D-19 (not D-15, which handles Reviewer OOO). This keeps it accessible to SMEs without navigating to a Director-level page.

**"Set Out-of-Office" section (below preferences, SME roles only):**

| Field | Description |
|---|---|
| OOO From | Date picker — start of OOO |
| OOO Until | Date picker — end of OOO (inclusive) |
| Note to Director | Optional free text — reason or context |

**On save:**
- `content_sme_oof` record created
- Director notified (D-19 notification + D-05 alert): "SME [role label] has set OOO from {date} to {date}. Review their pending DRAFT and RETURNED questions."
- D-05 shows a "SME OOO Actions Needed" panel where Director can:
  - View all DRAFT and RETURNED questions for the OOO SME
  - "Reassign to Another SME" action per question (reassigns within same subject — target SME notified)
  - "Keep in Queue" (leave questions with original SME — they'll complete on return)

**What changes during SME OOO:**
- D-01 shows an "Out of Office" banner for that SME (Director only — SMEs don't see each other's OOO)
- D-10 Quota Config shows OOO badge next to SME row — Director can set their quota to 0 for OOO months
- RETURNED questions remain visible to the original SME but a note shows: "You are OOO — these questions are awaiting your return. Your Director has been notified."

---

## 5. Data Models

### `content_notification`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `recipient_user_id` | FK → auth.User | — |
| `notification_type` | varchar | Enum: QuestionReturned · QuotaUpdated · DirectorAnnouncement · ReviewEscalation · OOOConfirmed · CriticalFeedback · AmendmentReview · NoteRequestAssigned · ImportComplete · ImportFailed · VersionRestored · BulkRetagComplete · PoolAdequacyAlert · SMEReassignment · NoteConversionComplete · NoteConversionFailed · NoteRequestDeadline · ScheduledReportReady · ScheduledReportFailed |
| `title` | varchar(120) | Short notification title |
| `body` | varchar(300) | One-paragraph body |
| `action_url` | varchar | Relative URL for action button |
| `action_label` | varchar(60) | Button label |
| `related_object_id` | UUID | Nullable — FK to the triggering object (question, note, batch) |
| `related_object_type` | varchar | question · note · import_batch · announcement · escalation |
| `is_read` | boolean | Default False |
| `read_at` | timestamptz | Nullable |
| `created_at` | timestamptz | — |

### `content_notification_preference`
| Field | Type | Notes |
|---|---|---|
| `user_id` | FK → auth.User | — |
| `notification_type` | varchar | — |
| `in_app_enabled` | boolean | Default True |
| `email_enabled` | boolean | Default varies by type |
| `digest_mode` | boolean | Default False — if True, batches into daily digest |

### `content_sme_oof`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `sme_user_id` | FK → auth.User | — |
| `oof_from` | date | — |
| `oof_until` | date | Inclusive |
| `note_to_director` | text | Nullable |
| `created_at` | timestamptz | — |

### `content_sme_question_reassignment`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_id` | FK → content_question | — |
| `from_sme_id` | FK → auth.User | Original SME |
| `to_sme_id` | FK → auth.User | New SME (same subject) |
| `reassigned_by` | FK → auth.User | Director |
| `reason` | varchar(300) | Nullable |
| `reassigned_at` | timestamptz | — |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | All authenticated Div D roles (Roles 18–30) — each sees only own notifications (ORM-scoped: `recipient_user_id = request.user.id`) |
| Notification creation | Server-side only — notifications are created by application events (Celery tasks, view actions). No user can create a notification for another user via the UI. |
| Preference edit | Each user can only edit their own preferences. |
| SME OOO | SME roles (19–27) can set own OOO. Director cannot set OOO on behalf of an SME (they use D-15 for Reviewer OOO only). |
| Locked notification types | Application enforces these regardless of preference record. Even if a user sets `in_app_enabled=False` for a locked type, the system ignores it and delivers anyway. |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Email delivery fails (SES bounce) | Notification is still created in `content_notification`. Email failure is logged. In-app notification is always reliable — email is best-effort. |
| User has > 10,000 unread notifications | Badge shows "99+". List shows last 25. Bulk "Mark All Read" clears the count. System archives notifications older than 90 days (marks as read, retains for audit, removes from active list). |
| Notification references a deleted object | Action button shows "Item no longer available" (grey, disabled). Notification body still shows the historical context. |
| SME OOO covers a month with high exam volume | Director sees a warning in D-10: "GK SME is OOO for {month} — quota target of {N} is at risk. Consider reassigning questions or adjusting quota." |
| Director sets SME OOO on behalf | Not supported — SMEs control their own OOO. Director can only respond (reassign questions). This prevents Directors from locking SMEs out of their own accounts. |
| Duplicate notifications for same event | Application-level deduplication: before creating a notification, check `content_notification` for same `(recipient_user_id, notification_type, related_object_id)` within the last 5 minutes. If found: skip creation. Prevents Celery retry loops from flooding inbox. |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-03 Review Queue | D-03 → D-19 | "Question returned to SME" notification | Celery task after Reviewer Return action |
| D-05 Director Dashboard | D-05 → D-19 | "Escalation" notification to Reviewer | Celery task after Director clicks Escalate |
| D-07 Bulk Import | D-07 → D-19 | "Import complete/failed" notification to SME | Celery on_success/on_failure callbacks |
| D-10 Calendar | D-10 → D-19 | "Quota updated" notification to SME | Synchronous: notification created in same request as quota save |
| D-14 Syllabus | D-14 → D-19 | "Pool adequacy critical" notification to Director | Celery nightly adequacy refresh task |
| D-15 Reviewer Assignments | D-15 → D-19 | "OOO confirmed" to Reviewer · "OOO request" to Director | Synchronous on OOO save |
| D-16 Feedback Queue | D-16 → D-19 | "Critical feedback escalation" to Director + Approver | Celery `sync_question_flags` task when threshold crossed |
| D-17 Notes Analytics | D-17 → D-19 | "Note request assigned" to Notes Editor | Celery task on note request creation |

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- Placeholder: "Search notifications…". Searches: title, body text. Debounced 300ms.

### Pagination
- 25 per page, numbered controls. Filter changes reset to page 1.

### Empty States
| State | Heading | Subtext |
|---|---|---|
| All read | "All caught up ✓" | "No unread notifications. Check back after your next workflow action." |
| No notifications | "No notifications yet" | "Workflow events will appear here as you and your team work." |
| Filter returns zero | "No notifications match these filters" | "Try clearing the type filter or extending the date range." |

### Toast Messages
| Action | Toast |
|---|---|
| Mark All Read | ✅ "All notifications marked as read" (Success 4s) |
| Set SME OOO | ✅ "Out-of-office period saved — Content Director notified" (Success 4s) |
| OOO From > OOO Until | ❌ "OOO start date must be before end date" (Error inline) |

### Loading States
- Notification list: 5-card skeleton (shimmer cards with icon placeholder + text lines).
- Bell popover: 3-card skeleton while loading.
- Unread count badge: no skeleton — shows last cached count until refresh completes.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Full-width notification list. Preferences panel: two-column grid. OOO section below preferences. |
| Tablet | Same layout, slightly narrower. |
| Mobile | Bell icon visible in mobile nav. Popover becomes a bottom sheet (full-width, 70% screen height). Full page list: single column cards. Preferences: single column toggle list. |

### Role-Based UI
- SME OOO section: SME roles (19–27) only. Hidden for other roles.
- Locked notification type labels: show "(required)" in grey next to the toggle — toggle greyed out, not interactive.
- "Mark All Read" affects only the current user's notifications (never other users').

---

*Page spec complete.*
*This page resolves: Critical Gap 1 (Notification Inbox) · Critical Gap 2 (SME OOO mechanism integrated here)*
