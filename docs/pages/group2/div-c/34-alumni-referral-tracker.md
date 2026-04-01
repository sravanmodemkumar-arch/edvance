# Page 34: Alumni Referral Tracker

**URL:** `/group/adm/alumni/referrals/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions
**Module:** Alumni

---

## 1. Purpose

The Alumni Referral Tracker manages the end-to-end pipeline for student admissions generated through alumni referrals — consistently one of the most cost-effective and high-trust enrollment channels available to any educational institution. When a former student recommends their coaching institute to a prospective student and that prospect enrolls, the institute gains an enrollment with near-zero marketing cost, from a source whose credibility far exceeds any advertisement. This page operationalizes that channel: capturing referral submissions from alumni, routing prospects to counsellors, tracking conversion progress, and processing rewards for alumni whose referrals convert.

The referral lifecycle begins when an alumni submits a prospect's details — typically via a WhatsApp message, a branch visit, or the alumni portal. The Demo/Counselling team then follows up with the referred prospect, takes them through the standard admissions funnel (enquiry, demo, application, counselling, enrollment), and upon enrollment, the system marks the referral as converted and triggers reward processing. This page makes every step of that lifecycle visible to the Alumni Manager and Admissions Director, ensuring that no referred prospect falls through the cracks due to assignment gaps or follow-up delays.

The reward management function is a meaningful operational component: alumni who have referred successfully expect to receive their agreed reward — a cash payment, a fee waiver for a sibling, or a gift voucher — in a timely manner. Delayed rewards discourage future referrals from both the rewarded alumni and others who observe the process. The Referral Reward Queue surfaces confirmed enrollments awaiting reward processing, enabling the Alumni Manager to clear the queue promptly and maintain the referral program's credibility. The Top Referring Alumni Leaderboard publicly recognizes the group's most active referrers and supports a culture of active alumni advocacy.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Alumni Relations Manager (28) | G3 | Full — create, edit, assign counsellors, process rewards, view all | Primary owner |
| Group Admission Coordinator (24) | G3 | View all + assign counsellors to referrals; no reward processing | Operational support |
| Group Admission Counsellor (25) | G3 | View own assigned referrals only; log follow-up notes | Cannot see other counsellors' referrals |
| Group Admissions Director (23) | G3 | View all + approve reward processing above threshold | Strategic oversight |

Access enforcement: All views protected with `@login_required` and `@role_required(['alumni_manager', 'admission_coordinator', 'admission_counsellor', 'admissions_director'])`. Counsellor scope enforced by filtering referral queryset to `assigned_counsellor = request.user` in the Django view. Reward approval above threshold requires `request.user.has_perm('approve_alumni_reward')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal → Admissions → Alumni → Referral Tracker`

### 3.2 Page Header
**Title:** Alumni Referral Tracker
**Subtitle:** Track referral pipeline, conversions, and alumni reward processing
**Actions (right-aligned):**
- `[+ New Referral]` — primary button, opens new-referral-form drawer
- `[Export Referral Report CSV]` — secondary button

### 3.3 Alert Banner

| Condition | Banner Type | Message |
|---|---|---|
| Unassigned referrals > 0 (new referral without counsellor) | Warning (amber) | "N new referrals have no counsellor assigned. [Assign Now →]" |
| Reward queue > 0 (confirmed enrollments awaiting reward) | Warning (amber) | "N referral rewards are pending processing. [View Reward Queue →]" |
| High-converting alumni added a new referral | Info (blue) | "[Alumni Name] (5 previous conversions) submitted a new referral. [View →]" |
| Reward marked as processed | Success (green) | "Reward for [Alumni Name]'s referral marked as processed." |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Active Referrals | COUNT referrals WHERE status NOT IN (Enrolled, Lost) | `referrals` | Blue always | Filters table to active |
| Referrals Converted (This Cycle) | COUNT referrals WHERE status = Enrolled AND cycle = current | `referrals` | Green always | Filters to enrolled |
| Referral Conversion Rate % | Enrolled / (Enrolled + Lost) × 100 for closed referrals | `referrals` | Green if ≥ 40%; amber if 25–39%; red if < 25% | No drill-down |
| Top Referring Alumni | Name of alumni with most conversions this cycle | `referrals` GROUP BY alumni | Blue always | Scrolls to leaderboard |
| Rewards Pending Processing | COUNT referrals WHERE status = Enrolled AND reward_status = Pending | `referrals` | Red if > 0; green if 0 | Scrolls to Section 5.4 |
| Revenue from Referral Enrollments (₹) | SUM fees_collected WHERE referral_source = alumni | `enrollments` | Blue always | No drill-down |

**HTMX auto-refresh pattern (every 5 minutes):**
```html
<div id="kpi-bar"
     hx-get="/group/adm/alumni/referrals/kpis/"
     hx-trigger="load, every 300s"
     hx-target="#kpi-bar"
     hx-swap="outerHTML">
  <!-- KPI cards rendered here -->
</div>
```

---

## 5. Sections

### 5.1 Referral Pipeline Table

**Display:** Full-width sortable, selectable, server-side paginated table (20 rows/page). Default sort: referral_date descending.

**Columns:**

| Column | Notes |
|---|---|
| Referral ID | Auto-generated, e.g. REF-0118 |
| Prospect Name | Referred student name |
| Class | e.g. Class 10 / Inter 1st year |
| Stream | MPC / BiPC / MEC / CEC / Undecided |
| Referring Alumni | Alumni name (linked to alumni profile) |
| Alumni Batch | Year of passing |
| Branch | Target branch |
| Referral Date | Date alumni submitted referral |
| Status | New / Contacted / Counselled / Applied / Enrolled / Lost (colour-coded badge) |
| Reward Status | N/A / Pending / Processed (badge) — shows only for Enrolled |
| Actions | `[View →]` opens referral-detail drawer; `[Assign Counsellor →]` opens assignment dropdown |

**Filters:**
- Status (multi-select)
- Branch (dropdown)
- Alumni batch year (from / to)
- Reward status (Pending / Processed / N/A / All)

**Bulk actions:**
- `[Assign Counsellor to Selected]` — dropdown of counsellors
- `[Export Selected]`

**HTMX:** Filter changes → `hx-get="/group/adm/alumni/referrals/table/"` with `hx-trigger="change"`, `hx-target="#referral-table"`. Pagination: `hx-get` with `?page=N`.

**Empty state:** "No referrals match the selected filters."

---

### 5.2 Referral Conversion Funnel

**Display:** Chart.js 4.x horizontal funnel (implemented as horizontal bar chart with decreasing values per stage). Shows current cycle referrals progressing through each stage.

**Stages:**
1. Referral Submitted
2. Contacted
3. Counselled
4. Application Submitted
5. Enrolled

**Each stage:** Bar with absolute count and % of stage-1 total. Drop-off count between stages annotated.

**Period toggle:** This cycle / Last cycle / All time (above chart).

**HTMX:** `hx-get="/group/adm/alumni/referrals/funnel/?period=P"` on period change, `hx-target="#referral-funnel"`.

---

### 5.3 Top Referring Alumni Leaderboard

**Display:** Sortable table of alumni ranked by total referrals submitted. Default sort: converted count descending.

**Columns:**

| Column | Notes |
|---|---|
| Rank | # |
| Alumni Name | Name (linked to alumni profile) |
| Batch Year | Year of passing |
| Branch | Branch attended |
| Referrals Submitted | Total submitted this cycle |
| Converted | Count enrolled from their referrals |
| Reward Earned | Cumulative reward value (₹ or descriptor) |
| Action | `[Send Thank-you Message →]` — opens WhatsApp message modal |

**HTMX:** `hx-get="/group/adm/alumni/referrals/leaderboard/"` on load.

**Empty state:** "No referrals with conversions yet. Leaderboard will populate as referrals are enrolled."

---

### 5.4 Referral Reward Queue

**Display:** Table of all confirmed enrollments from referrals where reward has not yet been processed.

**Columns:**

| Column | Notes |
|---|---|
| Alumni Name | Referring alumni |
| Referral ID | REF-XXXX |
| Enrolled Prospect | Enrolled student name |
| Enrollment Date | Date of enrollment |
| Reward Type | Cash / Fee waiver for sibling / Gift voucher |
| Amount / Value | Cash amount (₹) or description |
| Days Pending | Days since enrollment (red if > 14 days) |
| Action | `[Mark Rewarded →]` — opens reward-mark-modal |

**HTMX:** `hx-get="/group/adm/alumni/referrals/reward-queue/"` on section load. After `[Mark Rewarded →]` action, row removed from queue via `hx-swap="outerHTML"` on the row.

**Empty state:** "No referral rewards are pending. All confirmed referral rewards have been processed."

---

### 5.5 New Referral Capture Form

**Display:** Prominent card at the bottom of the page with a `[+ New Referral]` button that opens the new-referral-form drawer. The card also shows a quick-stat: "N referrals captured this week."

No inline form on this section — action always routes to the drawer for data quality consistency.

---

## 6. Drawers & Modals

### 6.1 `referral-detail` Drawer
**Width:** 640px
**Trigger:** `[View →]` in referral pipeline table
**HTMX endpoint:** `hx-get="/group/adm/alumni/referrals/detail/{referral_id}/"` lazy-loaded
**Tabs:**
1. **Prospect Profile** — Name, class, stream, contact details, branch, source of referral
2. **Referring Alumni** — Alumni name, batch, branch, contact, total referrals, conversion history
3. **Follow-up Timeline** — Vertical log of all contact attempts, outcomes, and notes; `[Add Note]` inline form at bottom
4. **Counselling Notes** — Notes from counselling sessions; attached by assigned counsellor
5. **Enrollment Details** — Enrollment date, branch, stream, fee paid (visible once status = Enrolled)
6. **Reward** — Reward type, value, status, processed date, processed by

---

### 6.2 `new-referral-form` Drawer
**Width:** 560px
**Trigger:** `[+ New Referral]` header button or from Section 5.5
**HTMX endpoint:** `hx-get="/group/adm/alumni/referrals/create/"` lazy-loaded
**Fields:**
- Referring alumni (searchable autocomplete from alumni directory)
- Alumni contact verification (auto-populated from alumni record; editable)
- Prospect name (required)
- Prospect class (dropdown)
- Preferred stream (dropdown)
- Prospect phone (required)
- Preferred branch (dropdown)
- How does the alumni know this prospect? (dropdown: Family / Friend / Neighbour / Student / Other)
- Additional notes (textarea)
- `[Submit Referral]` — `hx-post="/group/adm/alumni/referrals/create/"`

---

### 6.3 `reward-mark-modal` Modal
**Width:** 400px
**Trigger:** `[Mark Rewarded →]` in reward queue
**HTMX endpoint:** `hx-get="/group/adm/alumni/referrals/reward/{referral_id}/"` lazy-loaded
**Content:**
- Alumni name and referral summary
- Reward type (pre-populated from referral)
- Amount / description (editable)
- Payment method (if cash): NEFT / Cash / Cheque
- Transaction reference / voucher number
- Date of reward processing (date picker, default today)
- Notes
- `[Confirm Reward Processed]` — `hx-post="/group/adm/alumni/referrals/reward/{id}/mark/"`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Referral created | "Referral REF-XXXX created for [Prospect Name] from [Alumni Name]." | Success | 4s |
| Counsellor assigned | "Counsellor [Name] assigned to REF-XXXX." | Success | 3s |
| Referral status updated | "Referral REF-XXXX moved to [Status]." | Success | 3s |
| Reward marked as processed | "Reward for [Alumni Name]'s referral marked as processed." | Success | 4s |
| Thank-you message sent | "Thank-you WhatsApp message sent to [Alumni Name]." | Success | 3s |
| Bulk assign completed | "Counsellor assigned to N selected referrals." | Success | 4s |
| Export triggered | "Referral report export is being prepared." | Info | 3s |
| Referral marked lost | "Referral REF-XXXX marked as lost. Reason recorded." | Warning | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No referrals at all | Arrow-path icon | "No referrals yet" | "Start capturing alumni referrals to track them through to enrollment." | `[+ New Referral →]` |
| No referrals matching filters | Filter icon | "No referrals match your filters" | "Try adjusting the status, branch, or alumni batch year filters." | `[Clear Filters]` |
| Reward queue empty | Checkmark circle | "No rewards pending" | "All referral rewards have been processed." | None |
| Leaderboard empty | Trophy outline | "No conversions yet" | "The leaderboard will show alumni whose referrals have enrolled." | None |
| Referral detail — no follow-up notes | Empty timeline | "No follow-up history" | "No contact attempts have been logged for this referral yet." | `[Add Note]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load (KPI bar) | Skeleton cards (6 cards, grey shimmer) |
| Referral pipeline table loading | Skeleton rows (5 rows, column placeholders) |
| Referral funnel chart loading | Skeleton horizontal bars (5 stages) |
| Leaderboard loading | Skeleton rows (4 rows) |
| Reward queue loading | Skeleton rows (3 rows) |
| Drawer opening | Spinner centred in drawer body |
| Bulk assign in progress | Button spinner + "Assigning…" label |
| Reward mark processing | Button spinner + disabled state |
| KPI auto-refresh | Subtle pulse on KPI cards |
| Filter / search change | Table body skeleton (3 rows) during HTMX fetch |

---

## 10. Role-Based UI Visibility

All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Alumni Manager (28) | Admission Coordinator (24) | Admission Counsellor (25) | Admissions Director (23) |
|---|---|---|---|---|
| `[+ New Referral]` button | Visible | Visible | Hidden | Hidden |
| `[Assign Counsellor →]` action | Visible | Visible | Hidden | Visible |
| Referral table — all referrals | Visible | Visible | Own assigned only | Visible |
| Reward queue section | Visible | Hidden | Hidden | Visible |
| `[Mark Rewarded →]` action | Visible | Hidden | Hidden | Visible (approval required if > threshold) |
| Revenue from referrals KPI | Visible | Hidden | Hidden | Visible |
| `[Export Referral Report CSV]` | Visible | Visible | Hidden | Visible |
| Leaderboard — all alumni | Visible | Visible | Hidden | Visible |
| `[Send Thank-you Message →]` | Visible | Hidden | Hidden | Hidden |
| Referral detail — Reward tab | Visible | Hidden | Hidden | Visible |
| Referral detail — Enrollment tab | Visible | Visible | Visible | Visible |
| Bulk assign action | Visible | Visible | Hidden | Visible |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/alumni/referrals/kpis/` | JWT G3+ | KPI bar metrics |
| GET | `/api/v1/group/{group_id}/adm/alumni/referrals/` | JWT G3+ | List referrals with filters |
| POST | `/api/v1/group/{group_id}/adm/alumni/referrals/` | JWT G3 write | Create new referral |
| GET | `/api/v1/group/{group_id}/adm/alumni/referrals/{id}/` | JWT G3+ | Referral detail |
| PATCH | `/api/v1/group/{group_id}/adm/alumni/referrals/{id}/` | JWT G3 write | Update referral (status, notes) |
| POST | `/api/v1/group/{group_id}/adm/alumni/referrals/{id}/assign-counsellor/` | JWT G3 write | Assign counsellor to referral |
| POST | `/api/v1/group/{group_id}/adm/alumni/referrals/bulk-assign/` | JWT G3 write | Bulk assign counsellor |
| GET | `/api/v1/group/{group_id}/adm/alumni/referrals/funnel/` | JWT G3+ | Funnel stage data |
| GET | `/api/v1/group/{group_id}/adm/alumni/referrals/leaderboard/` | JWT G3+ | Top referring alumni |
| GET | `/api/v1/group/{group_id}/adm/alumni/referrals/reward-queue/` | JWT G3+ | Pending reward queue |
| POST | `/api/v1/group/{group_id}/adm/alumni/referrals/reward/{id}/mark/` | JWT G3 write | Mark reward as processed |
| POST | `/api/v1/group/{group_id}/adm/alumni/referrals/{id}/follow-up/` | JWT G3 write | Log follow-up note |
| POST | `/api/v1/group/{group_id}/adm/alumni/referrals/thank-you-message/` | JWT G3 write | Send thank-you WhatsApp to alumni |
| GET | `/api/v1/group/{group_id}/adm/alumni/referrals/export/` | JWT G3+ | Export referral report CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 300s` | GET `/group/adm/alumni/referrals/kpis/` | `#kpi-bar` | `outerHTML` |
| Filter change → reload table | `change` on filter inputs | GET `/group/adm/alumni/referrals/table/` | `#referral-table` | `innerHTML` |
| Table pagination | `click` on page link | GET `/group/adm/alumni/referrals/table/?page=N` | `#referral-table` | `innerHTML` |
| Open referral detail drawer | `click` on `[View →]` | GET `/group/adm/alumni/referrals/detail/{id}/` | `#drawer-container` | `innerHTML` |
| Open new referral drawer | `click` on `[+ New Referral]` | GET `/group/adm/alumni/referrals/create/` | `#drawer-container` | `innerHTML` |
| Submit new referral | `submit` in form | POST `/group/adm/alumni/referrals/` | `#referral-table` | `innerHTML` |
| Funnel period toggle | `click` on period button | GET `/group/adm/alumni/referrals/funnel/?period=P` | `#referral-funnel` | `innerHTML` |
| Load leaderboard | `load` | GET `/group/adm/alumni/referrals/leaderboard/` | `#referring-leaderboard` | `innerHTML` |
| Load reward queue | `load` | GET `/group/adm/alumni/referrals/reward-queue/` | `#reward-queue` | `innerHTML` |
| Open reward mark modal | `click` on `[Mark Rewarded →]` | GET `/group/adm/alumni/referrals/reward/{id}/` | `#modal-container` | `innerHTML` |
| Confirm reward processed | `click` on `[Confirm Reward Processed]` | POST `/group/adm/alumni/referrals/reward/{id}/mark/` | `#reward-row-{id}` | `outerHTML` |
| Add follow-up note in drawer | `submit` in timeline form | POST `/group/adm/alumni/referrals/{id}/follow-up/` | `#follow-up-timeline` | `beforeend` |
| Bulk assign counsellor | `click` (after confirm) | POST `/group/adm/alumni/referrals/bulk-assign/` | `#referral-table` | `innerHTML` |
| Assign counsellor (single) | `click` on `[Assign Counsellor →]` | POST `/group/adm/alumni/referrals/{id}/assign-counsellor/` | `#assignment-cell-{id}` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
