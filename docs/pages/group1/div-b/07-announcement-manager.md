# 07 — Announcement Manager

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Institutions to reach | 2,050 |
| Institution admin contacts | ~6,000–8,000 (avg 3 admins per institution) |
| Students indirectly informed via institution admins | 2.4M–7.6M |
| Announcement channels | In-app banner · Email digest · WhatsApp (admin) · SMS (admin) |
| Announcements per month | ~8–15 (feature releases, maintenance, policy updates) |
| Email delivery infrastructure | AWS SES (transactional) |
| WhatsApp | Meta Business API · Sender ID: EDUFGE |
| SMS | TRAI-registered sender ID EDUFGE via SMS gateway |
| Peak delivery volume | 8,000 emails + 8,000 WhatsApp + 8,000 SMS per announcement |

**Why this page matters at scale:** When a major feature ships, 2,050 institution admins need to know. When a plan price changes, affected institutions need advance notice (contractually and legally). When the platform is down for maintenance, a scheduled banner prevents 74K students from attempting to join exams during the window. This is distinct from incident alerts (Division A handles P0 incidents) — this page handles product-level communications owned by PM Platform.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Announcement Manager |
| Route | `/product/announcements/` |
| Django view class | `AnnouncementManagerView` |
| Template | `product/announcements.html` |
| Permission — view | `portal.view_announcements` (all div-b roles) |
| Permission — manage | `portal.manage_announcements` (PM Platform only) |
| 2FA required | No (announcements are not destructive) |
| HTMX poll — delivery status | Every 60s while an announcement is actively sending |
| Nav group | Product |
| Nav icon | `megaphone` |
| Priority | P2 |

---

## 3. Wireframe

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Announcement Manager             [+ New Announcement]  [Templates] [Audit] │
├────────┬────────┬────────┬────────┬────────┬────────────────────────────────────────┤
│ Total  │ Active │Scheduled│ Sent   │ Draft  │ Avg Open Rate                         │
│  142   │   2    │   3     │  134   │   3    │  68.4% (email)                        │
├────────┴────────┴────────┴────────┴────────┴────────────────────────────────────────┤
│ TABS: [Active (2)] [Scheduled (3)] [Sent (134)] [Drafts (3)] [Templates]            │
├────────────────────────────────────────────────────────────────────────────────────┤
│ FILTER: [Search...] [Type ▾] [Channel ▾] [Audience ▾] [Date Range ▾] [Apply]      │
├────────────────────────────────────────────────────────────────────────────────────┤
│ TABLE                                                                              │
│ Title                    │ Type      │ Channels │ Audience   │ Status │ Date  │ ⋯  │
│ v2.4.1 Feature Update    │ Release   │ 📧 💬 📱 │ All (2050) │ Active │ Now   │ ⋯  │
│ Maintenance Mar 28 1AM   │ Maintenanc│ 📧 📱     │ All (2050) │ Sched  │ Mar27 │ ⋯  │
│ Professional Plan Price  │ Pricing   │ 📧        │ Pro (410)  │ Sched  │ Apr 1 │ ⋯  │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Value | Delta | Alert |
|---|---|---|---|---|
| 1 | Total Sent | `142` | +8 this month | — |
| 2 | Active (showing now) | `2` | — | Any active = `border-[#6366F1]` pulsing |
| 3 | Scheduled | `3` | — | — |
| 4 | Sent (all time) | `134` | — | — |
| 5 | Draft | `3` | — | Draft > 7 days old = amber |
| 6 | Avg Email Open Rate | `68.4%` | `↑2.1%` | < 40% = amber |

---

### 4.2 Tab Bar

| Tab | Badge | Description |
|---|---|---|
| Active | `2` | Currently showing in-app banners |
| Scheduled | `3` | Queued to send at a future time |
| Sent | `134` | Delivered announcements with delivery reports |
| Drafts | `3` | Unpublished drafts |
| Templates | — | Reusable announcement templates |

---

### 4.3 Announcement Table

**Columns:**

| Column | Width | Detail |
|---|---|---|
| Title | 280px | Announcement title |
| Type | 120px | Badge: Release · Maintenance · Pricing · Policy · Feature · Survey |
| Channels | 100px | Channel icons: 📧 email · 💬 WhatsApp · 📱 SMS · 🖥 In-App |
| Audience | 140px | "All (2,050)" or segment: "Pro+ (590)" or "Coaching (100)" |
| Status | 100px | Badge: Draft · Active · Scheduled · Sent · Cancelled |
| Reach | 80px | Number of institutions reached |
| Open Rate | 80px | Email open % (shown for Sent) |
| Scheduled / Sent On | 130px | Date + time |
| Actions ⋯ | 48px | — |

**Type badge colours:**
- Release: `bg-[#312E81] text-[#A5B4FC]`
- Maintenance: `bg-[#451A03] text-[#FCD34D]`
- Pricing: `bg-[#064E3B] text-[#34D399]`
- Policy: `bg-[#0C4A6E] text-[#7DD3FC]`
- Feature: `bg-[#3B1764] text-[#D8B4FE]`
- Survey: `bg-[#1E2D4A] text-[#94A3B8]`

**Status badge colours:**
- Active: `bg-[#312E81] text-[#A5B4FC] animate-pulse`
- Scheduled: `bg-[#451A03] text-[#FCD34D]`
- Sent: `bg-[#064E3B] text-[#34D399]`
- Draft: `bg-[#1E2D4A] text-[#94A3B8]`
- Cancelled: `bg-[#450A0A] text-[#F87171] opacity-60`

**Kebab menu (⋯):**
- View Details / Preview → Announcement Detail Drawer
- Edit → (Draft/Scheduled only)
- Duplicate → creates Draft copy
- Schedule / Reschedule
- Cancel → Scheduled only
- Send Now → (Draft/Scheduled → overrides schedule)
- View Delivery Report → (Sent only)

**Row click:** opens Announcement Detail Drawer (600px)

**Pagination:** 10/25/50 per page · "Showing X–Y of Z"

---

## 5. Drawers

### 5.1 Announcement Detail Drawer (600px)

**Trigger:** Row click
**Header:** Announcement title + Type badge + Status badge + `[×]`

**Tab bar (4 tabs):**

---

#### Tab A — Content

**Channel previews (sub-tabs):** [In-App Banner] [Email] [WhatsApp] [SMS]

**In-App Banner Preview:**
`bg-[#0D1526] rounded-xl border border-[#6366F1] p-4`
Renders the actual banner as it appears to institution admins in their portal:
```
┌────────────────────────────────────────────────┐
│ [Icon] [Title]                             [×] │
│ Body text (max 2 lines shown, expandable)      │
│ [CTA Button]           [Learn More]            │
└────────────────────────────────────────────────┘
```
Banner placement: top of institution dashboard (below main nav)
Duration: shown for N days or until dismissed

**Email Preview:**
`bg-[#1A1A2E] rounded-xl p-6 max-w-[560px]`
Renders full HTML email with EduForge branding:
- Logo header
- Subject line (bold)
- Hero image (if uploaded)
- Body (Markdown rendered to HTML)
- CTA button
- Footer with unsubscribe link

**WhatsApp Preview:**
`bg-[#075E54] rounded-xl p-4`
WhatsApp-style chat bubble view:
- Profile: "EduForge (EDUFGE)"
- Message in WhatsApp bubble format
- Template ID shown: `eduforge_feature_update`
- Max 1024 chars for body

**SMS Preview:**
`bg-[#131F38] rounded-xl p-4 font-mono text-sm`
Plain text, max 160 chars (1 SMS unit) or up to 480 chars (3 units)
Sender ID: `EDUFGE`
Character count shown: `142/160 chars (1 SMS unit)`

---

#### Tab B — Targeting

**Audience configuration (read-only if Sent/Active):**

**Institution Type:**
`☑ Schools (1,000)  ☑ Colleges (800)  ☑ Coaching (100)  ☑ Groups (150)`

**Plan Tier:**
`☑ Starter  ☑ Standard  ☑ Professional  ☑ Enterprise`

**State filter:** "All states" or specific states multi-select

**Specific institutions:** list if any are excluded or specifically included

**Audience summary:**
`bg-[#0D1526] rounded p-3 text-sm`
"This announcement will reach 2,050 institutions (6,150 admin contacts)"
Breakdown: Schools: 1,000 · Colleges: 800 · Coaching: 100 · Groups: 150

**Channel targeting:**
- In-App Banner: `☑` shown to all institution admin users at login
- Email: `☑` sent to primary admin email of each institution
- WhatsApp: `☑` sent to registered WhatsApp number (if available)
- SMS: `☐` (opt-in — send only if explicitly chosen)

---

#### Tab C — Schedule & Send

**Status:** Draft / Scheduled / Sent

**Schedule settings (editable if Draft/Scheduled):**
- Send time: Date + Time picker
- Timezone: IST (fixed — India only, DPDPA §16)
- `[○ Send immediately]` · `[○ Schedule for later]`

**Delivery tracking (shown for Sent/Active):**

| Channel | Sent | Delivered | Opened | Clicked | Failed |
|---|---|---|---|---|---|
| In-App Banner | 2,050 institutions | 2,050 | N/A | 312 (15.2%) | 0 |
| Email | 6,150 contacts | 6,024 (97.9%) | 4,203 (68.4%) | 891 (14.5%) | 126 (2.1%) |
| WhatsApp | 1,840 contacts | 1,812 (98.5%) | 1,102 (59.9%) | N/A | 28 |
| SMS | N/A (not sent) | — | — | — | — |

**Failed deliveries:** [View Failed List] → shows institutions with failed delivery + reason

**Bounce reasons** (email):
- Hard bounce (invalid email): N
- Soft bounce (mailbox full): N
- Spam complaint: N
- [Export Failed List CSV]

---

#### Tab D — History

Timeline of all events:
```
● Created by Priya S. — Mar 20, 14:30
● Scheduled for Mar 25 09:00 IST — Mar 20, 14:35
● In-App banner went live — Mar 25, 09:00
● Email sent to 6,150 contacts — Mar 25, 09:02
● WhatsApp sent to 1,840 contacts — Mar 25, 09:05
● 500 email opens recorded — Mar 25, 11:00
● 4,203 email opens at 24h mark — Mar 26, 09:02
```

---

**Drawer footer:**
[Edit] (Draft/Scheduled only) · [Duplicate] · [Cancel Announcement] (Scheduled only) · [Close]

---

## 6. Modals

### 6.1 New Announcement Modal (multi-step)

**Width:** 680px
**Steps:** [1. Type & Audience] → [2. Content] → [3. Channels & Schedule] → [4. Preview & Send]

---

**Step 1 — Type & Audience:**

| Field | Type |
|---|---|
| Announcement Type | Select: Release · Maintenance · Pricing · Policy · Feature · Survey |
| Title | Text · required · max 120 chars |
| Institution Types | Checkbox group |
| Plan Tiers | Checkbox group |
| State filter | Multi-select dropdown (optional) |
| Specific institution overrides | Search + add (include/exclude specific institutions) |

**Audience preview counter:** updates live as selections change
"Will reach: 2,050 institutions (6,150 contacts)"

---

**Step 2 — Content:**

| Field | Type |
|---|---|
| In-App Banner Title | Text · required · max 80 chars |
| In-App Banner Body | Textarea · required · max 300 chars · Markdown |
| CTA Button Text | Text · optional · max 30 chars |
| CTA URL | URL · optional |
| Banner dismiss behaviour | Select: User dismisses · Auto-dismiss after N days |
| Email Subject | Text · required · max 120 chars |
| Email Body | Rich text (Markdown toolbar) · required |
| Hero Image | File upload (optional) · PNG/JPG · max 1MB · 600×300px |
| WhatsApp Message | Textarea · max 1024 chars · character counter |
| WhatsApp Template ID | Select from approved Meta templates |
| SMS Text | Textarea · max 480 chars · character counter (160/unit) |

**Use Template** button: loads content from saved template
**[Auto-generate from Release]** (Type=Release only): pulls from Release Manager changelog

---

**Step 3 — Channels & Schedule:**

| Field | Type |
|---|---|
| In-App Banner | Toggle |
| Email | Toggle |
| WhatsApp | Toggle |
| SMS | Toggle (off by default — high-cost channel) |
| Send Time | Date + Time picker or [Send Immediately] |
| Expiry (In-App Banner) | Date picker — banner auto-hides after this date |

**Cost estimate** (WhatsApp + SMS):
`bg-[#0D1526] rounded p-3 text-sm`
"WhatsApp: ~1,840 messages × ₹0.75 = ₹1,380"
"SMS: disabled (₹0)"
(Costs are approximate — actual billed by gateway)

---

**Step 4 — Preview & Send:**

Shows rendered preview of each channel side-by-side:
`grid grid-cols-2 gap-4`

Confirmation checklist:
- `[✓]` Title and body reviewed
- `[✓]` Audience correct (N institutions)
- `[✓]` Channels selected
- `[✓]` Schedule confirmed

**[Send Now / Schedule]** `bg-[#6366F1]` — button active only when all checklist items checked

---

### 6.2 Cancel Announcement Modal

**Width:** 400px
"Cancel this scheduled announcement? Institution admins who have already seen the in-app banner will no longer see it."
Reason textarea (optional)
[Confirm Cancel] `bg-[#EF4444]` · [Keep]

---

## 7. Tab: Templates

**Purpose:** Reusable content templates for common announcement types. Reduces PM effort for repeat announcements (monthly feature digests, maintenance windows, etc.)

**Template list:**

| Template | Type | Channels | Last used | Actions |
|---|---|---|---|---|
| Monthly Feature Digest | Release | Email + In-App | Mar 1 | [Use] [Edit] [Delete] |
| Maintenance Window Notice | Maintenance | All channels | Feb 28 | [Use] [Edit] |
| Plan Price Change Notice | Pricing | Email | Jan 15 | [Use] [Edit] |
| New Feature Available | Feature | In-App + Email | Feb 20 | [Use] [Edit] |
| Survey Request | Survey | Email | Dec 10 | [Use] [Edit] |

**[Use]:** creates a new Draft pre-populated with template content (Step 2 of New Announcement Modal)
**[+ New Template]** button: opens template editor (same as Step 2 of modal but saves as template)

---

## 8. Django View

```python
class AnnouncementManagerView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_announcements"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":               "product/partials/announce_kpi.html",
                "active":            "product/partials/announce_active.html",
                "scheduled":         "product/partials/announce_scheduled.html",
                "sent":              "product/partials/announce_sent.html",
                "drafts":            "product/partials/announce_drafts.html",
                "tmpl_list":         "product/partials/announce_templates.html",
                "announce_drawer":   "product/partials/announce_drawer.html",
                "delivery_report":   "product/partials/announce_delivery.html",
                "audience_preview":  "product/partials/announce_audience.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "product/announcements.html", ctx)

    def post(self, request):
        if not request.user.has_perm("portal.manage_announcements"):
            return JsonResponse({"error": "Permission denied"}, status=403)
        action = request.POST.get("action")
        dispatch = {
            "create_announcement":  self._create_announcement,
            "update_announcement":  self._update_announcement,
            "send_now":             self._send_now,
            "schedule":             self._schedule,
            "cancel_announcement":  self._cancel_announcement,
            "create_template":      self._create_template,
            "update_template":      self._update_template,
            "delete_template":      self._delete_template,
        }
        handler = dispatch.get(action)
        if handler:
            return handler(request)
        return JsonResponse({"error": "Unknown action"}, status=400)

    def _send_now(self, request):
        from portal.tasks import send_announcement_task
        announcement_id = request.POST.get("announcement_id")
        # Celery async task — do not block HTTP response
        send_announcement_task.delay(announcement_id)
        return JsonResponse({"success": True, "message": "Delivery started"})
```

---

## 9. Celery Task: Announcement Delivery

```python
# portal/tasks.py

@shared_task(bind=True, max_retries=3)
def send_announcement_task(self, announcement_id):
    from portal.apps.product.models import Announcement
    announcement = Announcement.objects.get(id=announcement_id)
    announcement.status = "sending"
    announcement.save(update_fields=["status"])

    try:
        audience = announcement.get_audience_queryset()  # returns Institution QS

        if announcement.channels_inapp:
            _send_inapp(announcement, audience)

        if announcement.channels_email:
            _send_email_batch(announcement, audience)  # uses AWS SES bulk send

        if announcement.channels_whatsapp:
            _send_whatsapp_batch(announcement, audience)  # Meta Business API

        if announcement.channels_sms:
            _send_sms_batch(announcement, audience)  # SMS gateway

        announcement.status = "sent"
        announcement.sent_at = timezone.now()
        announcement.save(update_fields=["status", "sent_at"])

    except Exception as exc:
        announcement.status = "failed"
        announcement.save(update_fields=["status"])
        raise self.retry(exc=exc, countdown=60)
```

---

## 10. Empty States

| Section | Copy |
|---|---|
| No active announcements | "No announcements currently showing. All clear!" |
| No scheduled | "No announcements scheduled. Draft one now to prepare." |
| No sent | "No announcements sent yet." |
| No drafts | "No drafts. Click '+ New Announcement' to create one." |
| No templates | "No templates saved. Create templates for faster repeat announcements." |

---

## 11. Opt-Out and Unsubscribe Management

**Purpose:** DPDPA 2023 and TRAI regulations require recipients to be able to opt out of non-transactional communications. Institution admins must be able to stop receiving non-critical announcements.

**Opt-out categories:**
- **Cannot opt out:** Maintenance window notices (operational necessity) · Plan change notices (contractual requirement) · Legal/policy notices
- **Can opt out:** Feature update announcements · Survey requests · Product newsletters

**Opt-out mechanism:**
- Every email has a one-click "Unsubscribe" link in the footer (DPDPA-compliant)
- WhatsApp: standard Meta Business API opt-out via "STOP" reply — handled automatically by gateway
- In-App Banner: dismissing the banner is considered a preference signal; admins with 5+ consecutive dismissals are shown a preference panel: "You keep dismissing announcements. Would you like to reduce notifications?"

**Opt-out registry table** (visible to PM in Targeting tab of Announcement Drawer — Sent):
| Institution | Admin contact | Opted Out Channels | Opt-out Date |
|---|---|---|---|
| Delhi Public School | admin@dps.edu | Email | Mar 10, 2026 |
| Narayana Coaching | mgr@narayana.in | Email + WhatsApp | Feb 28, 2026 |

**Impact on audience count:** The Audience preview in Step 1 of New Announcement Modal shows:
"Will reach: 2,048 institutions (2 excluded due to opt-out)"

**Re-opt-in:** Institutions can re-enable communications from their institution settings portal. PM cannot manually override an opt-out.

---

## 12. Regulatory Compliance

### TRAI DLT Registration (SMS)
All SMS announcement templates must be pre-registered on the Distributed Ledger Technology (DLT) portal as mandated by TRAI. The Announcement Manager shows:
- **Template DLT ID:** each SMS template must carry its registered DLT Template ID
- If an SMS template has no DLT ID: it is blocked from sending with an error: "SMS template not DLT-registered. Submit to telecom operator before using."
- New SMS templates go through a 2–7 day DLT approval process before they can be used.

### Meta WhatsApp Business API Approval
WhatsApp templates must be approved by Meta before use. Status per template:
- Approved: `bg-[#064E3B] text-[#34D399]` — can send
- Pending: `bg-[#451A03] text-[#FCD34D]` — cannot send yet
- Rejected: `bg-[#450A0A] text-[#F87171]` — requires revision and resubmission

### DPDPA 2023 Compliance
- All announcement emails include the platform Data Fiduciary name and contact: "EduForge Technologies Pvt. Ltd. | Hyderabad | dpo@eduforge.in"
- Student PII is never included in announcements to institution admins — only aggregate data (e.g., "your institution has 1,240 enrolled students") is allowed
- Opt-out records are retained for 3 years (DPDPA audit requirement)

---

## 13. Integration Points

| Page | Direction | What flows |
|---|---|---|
| 03 — Release Manager | Inbound | [Auto-generate from Release] pulls changelog text from the linked release record in page 03 |
| 18 — Notification Template Manager | Sibling | Page 18 manages student-facing notification templates sent by institutions; this page manages platform-to-institution comms. Channels are shared (SES, WhatsApp Business API) but audiences and content are distinct |
| 16 — Portal Templates | Inbound | In-app banners rendered on institution portals use the layout defined in portal templates (page 16) |
| 04 — Plan Config | Inbound | Pricing change announcements (Type: Pricing) are triggered when plan pricing is published from page 04; the audience is auto-set to affected institutions |
| 25 — Defect Tracker | Inbound | When a P0 incident is resolved, PM Platform uses this page to send a "Resolution Notice" announcement to all affected institutions |

---

## 14. Key Design Decisions

| Decision | Chosen approach | Why |
|---|---|---|
| SMS off by default | Toggle must be explicitly enabled per announcement | SMS costs ₹0.12–0.15 per message; 8,000 admins × ₹0.13 = ₹1,040 per announcement. High-volume thoughtless sending would be wasteful. Default off forces PM to consciously choose SMS |
| Separate from Notification Template Manager (page 18) | Two distinct systems | Page 18 is for institution-to-student transactional notifications; this page is for platform-to-institution broadcast comms. Merging them would create role confusion (PM Portal manages page 18; PM Platform manages page 07) |
| [Auto-generate from Release] pulls from Release Manager | Cross-page data pull | Keeps release notes and announcement content in sync; prevents PM writing announcement that contradicts the actual shipped features |
| 4-step wizard for new announcements | Step-by-step with preview | Announcements to 2,050 institutions cannot be reversed after sending. The 4-step wizard with a mandatory confirmation checklist reduces "accidental send" incidents |
| Audience preview counter in Step 1 | Live, updates on filter change | PM needs to know if a filter misconfiguration results in 0 or wrong audience before spending time writing content in Step 2 |
| Cost estimate for WhatsApp + SMS | Displayed in Step 3 | PM Platform has a comms budget; cost transparency prevents budget overruns and encourages using in-app banner (zero marginal cost) as primary channel |

---

## 15. Error States

| Error | Display |
|---|---|
| Email delivery failure > 10% | Amber banner: "Email delivery rate is below 90%. Check SES sending limits." |
| WhatsApp template not approved | "WhatsApp template '{id}' is not approved by Meta. Announcements will skip WhatsApp." |
| Audience = 0 institutions | Inline warning in Step 1: "Current targeting matches 0 institutions. Adjust filters." |
| Scheduling conflict with maintenance | "⚠ Scheduled time overlaps with planned maintenance window (Mar 28, 1–3 AM)." |
