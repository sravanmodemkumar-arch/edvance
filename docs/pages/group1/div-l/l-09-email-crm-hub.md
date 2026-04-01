# L-09 — Email & CRM Hub

**Route:** `GET /marketing/email/`
**Method:** Django `TemplateView` + HTMX part-loads; server-side pagination
**Primary role:** Email & CRM Marketing Executive (#100)
**Also sees:** Marketing Manager (#64) — full access + approval gate; Marketing Analyst (#98) — read-only analytics

> See [L-00 Global Spec](l-00-global-spec.md) for toasts, loaders, error states, notification triggers, and DPDP compliance rules.

---

## Purpose

Dedicated workspace for email drip campaign operations. The Email Exec designs sequences (multi-step drip campaigns triggered by lead events), authors templates, monitors active sends, and analyses open/click performance. Contact lists are sourced exclusively from Division K `sales_lead` records with `contact_consent = true` — no manual list uploads allowed (DPDP compliance). Sends exceeding 10,000 contacts require Marketing Manager approval before queuing.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Sequence list | `mktg_email_sequence` + step count + enrolled count | 5 min |
| Sequence analytics | `mktg_email_send` aggregate per sequence (sent, opened, clicked, bounced, unsubscribed) | 15 min |
| Template list | `mktg_email_template` (new table; see below) | 10 min |
| Send queue | `mktg_email_send` WHERE status='QUEUED' ORDER BY queued_at | Live |
| Recent sends (7 days) | `mktg_email_send` WHERE sent_at > now()-7d | 10 min |
| Pending approval | `mktg_bulk_send_approval` WHERE status='PENDING' | 5 min |
| Opt-out rate | `sales_lead` WHERE email_opt_out=true / total contact leads | 30 min |
| Deliverability metrics | `mktg_email_send` aggregate for last 30 days (bounce, unsub, open, click rates) | 30 min |

Cache keyed on `(user_id, sequence_id, period)`.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?tab` | `sequences`, `templates`, `queue`, `analytics`, `approvals` | `sequences` | Active tab |
| `?status` | `draft`, `active`, `paused`, `archived` | `all` | Filter sequences by status |
| `?segment` | segment enum | `all` | Filter by target_segment |
| `?q` | string ≥ 2 chars | — | Search sequence name |
| `?page` | integer ≥ 1 | `1` | Pagination |
| `?period` | `7d`, `30d`, `90d` | `30d` | Analytics window |

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/l/email-sequence-list/` | Sequence list | Filter / sort / page | `#l-email-seq-list` |
| `htmx/l/email-template-list/` | Template list | Tab switch | `#l-email-tmpl-list` |
| `htmx/l/email-queue/` | Send queue | Tab switch; auto-refresh 2 min | `#l-email-queue` |
| `htmx/l/email-analytics/` | Analytics section | Tab switch + period | `#l-email-analytics` |
| `htmx/l/email-deliverability/` | Deliverability strip | Page load | `#l-email-deliverability` |
| `htmx/l/email-approvals/` | Pending approvals | Page load; auto-refresh 5 min | `#l-email-approvals` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  EMAIL & CRM HUB                                   [+ Create Sequence]  │
├─────────────────────────────────────────────────────────────────────────┤
│  DELIVERABILITY STRIP (4 KPI tiles)                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  [Sequences]  [Templates]  [Send Queue]  [Analytics]  [Approvals (N)]  │
├─────────────────────────────────────────────────────────────────────────┤
│  (Active tab content — see below)                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Deliverability Strip (Always Visible, All Tabs)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 38.2%        │ │ 14.6%        │ │ 0.9%         │ │ 0.4%         │
│ Avg Open     │ │ Avg Click    │ │ Bounce Rate  │ │ Unsub Rate   │
│ Rate (30d)   │ │ Rate (30d)   │ │ (30d)        │ │ (30d)        │
│ ↑+2.4% vs PM │ │ ↑+1.1% vs PM │ │ Target < 2%  │ │ Target < 0.5%│
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

- Bounce Rate: amber if 1.5–2%; red if > 2% + triggers alert (see L-00 §7)
- Unsub Rate: amber if 0.4–0.5%; red if > 0.5%
- Click tile shows CTOR (Click-to-Open Rate) in sub-label: "CTOR: 38.2%"
- Data from `mktg_email_send` aggregate last 30 days across ALL sequences

---

## Tab 1 — Sequences

### Sequence List

Status tabs: All · Active · Paused · Draft · Archived (count badges).

| Column | Description |
|---|---|
| Sequence Name | Click → opens Sequence Detail Drawer |
| Segment | Target audience badge (SCHOOL / COLLEGE / COACHING / GROUP / ALL) |
| Trigger | When leads enrol (LEAD_CREATED / DEMO_DONE / PROPOSAL_SENT / TRIAL_EXPIRY / MANUAL) |
| Steps | Number of email steps in the sequence |
| Enrolled | Current count of leads actively progressing through sequence |
| Open Rate | Avg open rate across all steps (last 30d) |
| Click Rate | Avg click rate across all steps (last 30d) |
| Status | Badge: DRAFT (grey) · ACTIVE (green) · PAUSED (amber) · ARCHIVED (grey-dark) |
| Last Sent | Relative time of most recent email send from this sequence |
| Actions | [Edit] [Pause/Resume] [Duplicate] [Archive] — role-dependent |

**[Create Sequence]:** Opens Create Sequence Drawer.

**[Pause]:** PATCH `/marketing/email/sequences/{id}/status/`. All enrolled leads stop receiving further steps. Leads remain in `mktg_email_send` with status `QUEUED` (not deleted; can resume). Toast: "Sequence paused. Enrolled leads will not receive further steps."

**[Resume]:** Resumes from where each lead left off — next queued step is sent at its scheduled interval from enrollment.

**Contact count warning:** When activating a sequence, the system estimates total recipients = `sales_lead` count matching `target_segment` with `contact_consent=true` and `email_opt_out=false`. If > 10,000, [Activate] is replaced with [Request Approval] (see L-00 §8.4).

---

### Sequence Detail Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  School Admin Welcome Drip               [Status: ACTIVE]        │
│                                          [Edit] [Pause] [Close]  │
├──────────────────────────────────────────────────────────────────┤
│  Target: SCHOOL · Trigger: LEAD_CREATED                          │
│  Enrolled: 280 · Sent MTD: 840 · Open rate: 38% · Click: 14%    │
├──────────────────────────────────────────────────────────────────┤
│  STEPS                                                           │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │ Step 1 — Welcome Email         Day 0 (immediate)          │   │
│  │ Template: "Welcome to EduForge" · Opens: 62% · Clicks: 22%│   │
│  ├───────────────────────────────────────────────────────────┤   │
│  │ Step 2 — Platform Tour         Day 3                      │   │
│  │ Template: "Getting Started Guide" · Opens: 44% · Clicks: 18%│ │
│  ├───────────────────────────────────────────────────────────┤   │
│  │ Step 3 — Case Study            Day 7                      │   │
│  │ Template: "School Success Story" · Opens: 38% · Clicks: 12%│  │
│  ├───────────────────────────────────────────────────────────┤   │
│  │ Step 4 — Trial CTA             Day 14                     │   │
│  │ Template: "Start Your Free Trial" · Opens: 28% · Clicks: 9%│  │
│  └───────────────────────────────────────────────────────────┘   │
│  [+ Add Step]  (drag to reorder)                                 │
├──────────────────────────────────────────────────────────────────┤
│  ENROLLED LEADS (sample)                                         │
│  Ramesh Kumar (DPS Hyderabad) — enrolled 3 Jan, at Step 3        │
│  Priya Nair (Sunrise Academy) — enrolled 5 Jan, at Step 1        │
│  … [View all 280 →]                                              │
└──────────────────────────────────────────────────────────────────┘
```

**`mktg_email_sequence_step` table:**

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| sequence_id | FK mktg_email_sequence | ON DELETE CASCADE |
| step_number | int | NOT NULL; display order |
| template_id | FK mktg_email_template | NOT NULL |
| delay_days | int | NOT NULL DEFAULT 0; send N days after enrollment (step 1: 0 = immediate) |
| subject_override | varchar(500) | NULL = use template's default subject |
| condition | jsonb | NULL = always send; otherwise conditional logic e.g. `{"opened_step": 2}` = only send if step 2 was opened |

---

### Create / Edit Sequence Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  Create Email Sequence                               [Close ×]   │
├──────────────────────────────────────────────────────────────────┤
│  Sequence name*   [School Admin Welcome Drip            ]        │
│  Target segment*  [School                             ▼]         │
│  Trigger event*   [Lead Created                       ▼]         │
│                   (When should leads be enrolled?)               │
│                                                                  │
│  STEPS                                                           │
│  Step 1  Day: [0 ] Template: [Select template        ▼] [×]    │
│  Step 2  Day: [3 ] Template: [Select template        ▼] [×]    │
│  [+ Add step]                                                    │
│                                                                  │
│  ⚠ Estimated recipients: 420 (within consent + opt-in rules)    │
│                                                                  │
│  [Cancel]                      [Save as Draft]  [Activate]       │
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Name: required, max 300 chars
- Segment: required
- Trigger: required
- Steps: minimum 1 step; each step requires a template; delay_days ≥ 0 and must be strictly increasing across steps (Step 2 delay > Step 1 delay)
- If estimated recipients > `email_bulk_send_threshold` (from `mktg_config`): [Activate] → [Request Approval]; see L-00 §8.4

**Estimated recipient count logic:**
```sql
SELECT COUNT(*) FROM sales_lead
WHERE institution_type = '{segment}'
  AND contact_consent = true
  AND email_opt_out = false
  AND stage NOT IN ('CLOSED_WON', 'CLOSED_LOST');
```
Shown live as the user selects segment. Note: actual enrolled count may differ (trigger fires per-lead event, not batch).

---

## Tab 2 — Templates

### Template List

```
┌────────────────────────────────────────────────────────────────────────┐
│  TEMPLATES                                       [+ Create Template]   │
│  [🔍 Search template name...]   [Type ▼]   [Domain ▼]                  │
├──────────────────┬──────────────────┬──────────┬──────────┬────────────┤
│ Template Name    │ Type             │ Domain   │ Used In  │ Last Edit  │
├──────────────────┼──────────────────┼──────────┼──────────┼────────────┤
│ Welcome to Edu…  │ DRIP_WELCOME     │ Corporate│ 2 seqs   │ 10 Mar     │
│ SSC CGL Update   │ NEWSLETTER       │ SSC      │ —        │ 05 Mar     │
│ Trial Expiry…    │ DRIP_CTA         │ Corporate│ 1 seq    │ 20 Feb     │
└──────────────────┴──────────────────┴──────────┴──────────┴────────────┘
```

**`mktg_email_template` table:**

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| name | varchar(300) | NOT NULL |
| template_type | varchar(30) | NOT NULL; enum `DRIP_WELCOME` · `DRIP_FOLLOWUP` · `DRIP_CTA` · `NEWSLETTER` · `ANNOUNCEMENT` · `TRANSACTIONAL` |
| exam_domain | varchar(30) | enum from standard list; NULL = corporate/cross-domain |
| subject_default | varchar(500) | NOT NULL |
| html_body | text | NOT NULL; stored as full HTML with merge tags |
| text_fallback | text | Plain-text version for email clients that block HTML |
| merge_tags | jsonb | DEFAULT `[]`; list of available merge tags e.g. `["{{first_name}}", "{{institution_name}}"]` |
| used_in_sequences | int | Computed: count of `mktg_email_sequence_step` rows referencing this template |
| created_by_id | FK auth_user | |
| updated_at | timestamptz | NOT NULL DEFAULT now() |

### Template Editor

Click template name or [Create Template] → opens full-page template editor (not a drawer).

```
Route: GET /marketing/email/templates/{id}/
```

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Back to templates                                                    │
│  Welcome to EduForge                                                    │
├──────────────────────────────────┬──────────────────────────────────────┤
│  EDITOR (left panel)             │  PREVIEW (right panel)               │
│                                  │                                      │
│  Subject*  [Welcome to EduForge  │  [Desktop preview]  [Mobile preview] │
│  —Your Exam-Ready Portal]        │                                      │
│                                  │  ┌────────────────────────────────┐  │
│  Template type* [DRIP_WELCOME ▼] │  │  EduForge Logo                 │  │
│  Domain [Corporate ▼]            │  │                                │  │
│                                  │  │  Dear {{first_name}},          │  │
│  HTML body                       │  │                                │  │
│  [Rich text editor / HTML mode ↔]│  │  Welcome to EduForge! Your     │  │
│                                  │  │  institution {{institution_    │  │
│  Merge tags available:           │  │  name}} is now active.         │  │
│  {{first_name}}                  │  │                                │  │
│  {{institution_name}}            │  │  [Get Started →]               │  │
│  {{institution_type}}            │  │                                │  │
│  {{sender_name}}                 │  │  Unsubscribe | View in browser │  │
│  {{unsubscribe_link}} ← required │  └────────────────────────────────┘  │
│                                  │                                      │
│  Plain text fallback             │  [Send Test Email]                   │
│  [Plain text version of above]   │  To: [your.email@eduforge.com  ]    │
│                                  │  [Send Test]                         │
├──────────────────────────────────┴──────────────────────────────────────┤
│  [Discard changes]                          [Save Template]             │
└─────────────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Subject: required, max 500 chars
- HTML body: must contain `{{unsubscribe_link}}` merge tag — enforced server-side before save (DPDP compliance)
- HTML body: cannot contain external script tags (XSS prevention — sanitised by server using `bleach` library)
- Text fallback: required if template_type is `DRIP_*` or `NEWSLETTER`
- Merge tags: validated — any `{{variable}}` used in the body must be in the `merge_tags` list or is a known system tag

**[Send Test]:** Sends a rendered test email to the logged-in user's email address. Merge tags populated with sample data: `{{first_name}}` → "Test User", `{{institution_name}}` → "Sample Institution".

**[Save Template]:** PUT `/marketing/email/templates/{id}/`. Auto-save drafts every 2 minutes (stores in `mktg_email_template.draft_html_body`; not persisted to live `html_body` until explicit save).

---

## Tab 3 — Send Queue

Live view of emails currently queued and recently sent.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SEND QUEUE                                   [Pause all sends] (Mgr)  │
│                                                                         │
│  QUEUED (84 emails)                                                     │
│  Sequence: School Admin Drip — Step 2                                   │
│  Sending to: DPS Hyderabad (Step 2, Day 3), Sunrise Academy, …         │
│  Scheduled for: Next batch: 12:00 IST today                             │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  SENDING NOW (3 emails)                                                  │
│  [spinner] Dispatch in progress…                                        │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  SENT TODAY (420 emails)  Open: 38%  Click: 14%  Bounce: 0.8%           │
│  View by sequence: [School Drip (280)] [Trial Nudge (140)]              │
└─────────────────────────────────────────────────────────────────────────┘
```

**[Pause all sends]:** Marketing Manager only. Emergency stop. Sets all QUEUED `mktg_email_send` rows to `CANCELLED` for active sequences. Confirmation: "Pause all outgoing emails? {N} emails will be cancelled across {M} sequences."

Email sends are batched to avoid rate-limiting. Batch size and send rate configured in `mktg_config['email_batch_size']` (default: 500 per hour) via F-06 Notification Manager dispatcher.

---

## Tab 4 — Analytics

Per-sequence performance analytics.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ANALYTICS   Period: [Last 30 Days ▼]                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  SEQUENCE PERFORMANCE TABLE                                             │
│                                                                         │
│  Sequence           Enrolled  Sent  Open%  Click%  Bounce%  Unsub%     │
│  School Admin Drip    280      840  38.2%  14.6%   0.8%     0.3%       │
│  Trial Expiry Nudge   48       144  61.0%  18.0%   0.4%     0.0%       │
│  Post-Demo Follow-up  142      426  52.0%  22.0%   0.8%     0.7%       │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  STEP-LEVEL BREAKDOWN  (click sequence row to expand)                   │
│                                                                         │
│  School Admin Drip — Step Performance                                   │
│  Step 1 (Day 0)  280 sent · 62% open · 22% click (best performing)     │
│  Step 2 (Day 3)  280 sent · 44% open · 18% click                       │
│  Step 3 (Day 7)  222 sent · 38% open · 12% click (62 unsubscribed)     │
│  Step 4 (Day 14) 180 sent · 28% open · 9%  click                       │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  OPEN RATE TREND (line chart — weekly, last 12 weeks, by sequence)      │
└─────────────────────────────────────────────────────────────────────────┘
```

**Step-level breakdown:** Reveals which step has the highest drop-off. If a step has < 50% of the previous step's send count, it means many leads exited the sequence (unsubscribed, bounced, or opted out). Highlighted in amber.

**Opt-out impact:** "62 unsubscribed after Step 3" → shown as red text if > 5% of step recipients unsubscribed. Tooltip: "High unsubscribe rate — consider revising Step 3 copy."

---

## Tab 5 — Approvals

Visible to Marketing Manager (#64) and Email Exec (#100) (exec sees own requests only).

```
┌─────────────────────────────────────────────────────────────────────────┐
│  BULK SEND APPROVALS                                                    │
│                                                                         │
│  PENDING (2)                                                            │
│  ─────────────────────────────────────────────────────────────────────  │
│  Sequence: School Year-Start Campaign                                   │
│  Requested by: Priya N. (Email Exec) · 2h ago                           │
│  Recipients: 14,200 (SCHOOL segment, consent + opt-in)                  │
│  Reason: "Q1 onboarding campaign for all school leads"                  │
│                                                                         │
│  [Preview sequence]  [Approve]  [Deny — enter reason]                   │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  RECENT DECISIONS (last 30 days)                                        │
│  ✓ Coaching Q1 Nurture (12,400) — Approved by Vandana M. · 5 Jan       │
│  ✗ Ad Hoc All-Leads Blast (28,000) — Denied: "Too broad, segment it"    │
└─────────────────────────────────────────────────────────────────────────┘
```

**[Deny — enter reason]:** Opens inline text input. Required. PATCH to `mktg_bulk_send_approval.status = DENIED` + `review_note`. Toast to Manager: "Request denied." Email + in-app notification to Email Exec.

**[Preview sequence]:** Opens Sequence Detail Drawer (read-only) so Manager can review steps and templates before approving.

---

## Contact Management

Email Exec cannot build ad-hoc contact lists. All contacts sourced from `sales_lead` with constraints:
- `sales_lead.contact_consent = true`
- `sales_lead.email_opt_out = false`
- Segment filter per sequence's `target_segment`
- Stage filter: `stage NOT IN ('CLOSED_LOST', 'CLOSED_WON')` by default (configurable per sequence via `mktg_email_sequence.exclude_closed = true/false`)

**Contact view** (accessible from Sequence Detail Drawer → "View all enrolled leads"):

Route: `GET /marketing/email/sequences/{id}/contacts/`

Table: lead name · institution name · segment · stage · enrolled_at · current step · last email sent · last email status

**Export contacts:** Marketing Analyst (#98) + Marketing Manager (#64) can export. Export EXCLUDES email addresses unless Manager explicitly approves PII export (checkbox in export dialog). Column `email_address` replaced with `[redacted]` in standard export.

---

## Role-Based UI

| Element | 64 Manager | 98 Analyst | 100 Email Exec |
|---|---|---|---|
| View all sequences | Yes | Read | Yes |
| Create / edit sequence | Yes | No | Yes |
| Activate sequence (< threshold) | Yes | No | Yes |
| Request approval (> threshold) | — | — | Yes |
| Approve bulk send request | Yes | No | No |
| Deny bulk send request | Yes | No | No |
| Pause all sends (emergency) | Yes | No | No |
| Create / edit templates | Yes | No | Yes |
| Send test email | Yes | No | Yes |
| View send queue | Yes | No | Yes |
| View analytics | Yes | Yes (read) | Yes |
| Export contacts (with PII) | Yes (approve for self) | With Manager approval | No |
| Export contacts (without PII) | Yes | Yes | Yes |
| View approvals tab | Yes (all) | No | Own requests |

---

## Empty States

| Condition | Message |
|---|---|
| No sequences | "No email sequences yet. [+ Create Sequence →]" |
| No templates | "No templates yet. [+ Create Template →]" |
| No emails in queue | "All caught up — no emails queued." |
| No analytics data | "Send your first sequence to see analytics." |
| No pending approvals | "No pending approval requests." with green checkmark |
| Sequence with 0 eligible contacts | "No eligible contacts for this segment (consent + opt-in required)." with link to DPDP compliance note |
