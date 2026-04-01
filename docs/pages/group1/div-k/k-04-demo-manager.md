# K-04 — Demo Manager

**Route:** `GET /group1/k/demos/`
**Method:** Django `ListView` + HTMX part-loads + modal wizard
**Primary role:** Demo Manager (#62)
**Also sees:** B2B Sales Manager (#57 — view + extend expiry only), Sales Executives #58–60 (own linked demos, view only)

Sales Manager (#57) has full read access to all demo tenant records (not just linked demos). They can view usage stats and trigger expiry extension but cannot create new demo tenants, reset demo data, or generate access links — those actions are restricted to Demo Manager (#62) only.

---

## Purpose

Lifecycle management of all free trial and demo tenants. The Demo Manager controls creation, data seeding, resets, and expiry of sandbox environments linked to sales leads. At any given time there are 10–30 active trials across different institution types. This page gives Demo Manager a consolidated view to prevent expired trials from going unnoticed, track prospect engagement (login counts), and maintain a healthy demo estate so Sales Executives always have a ready sandbox to show. It is also the provisioning interface for new trials requested by the sales team.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `sales_demo_tenant` aggregates + `sales_lead` join | 5 min |
| Demo tenant table | `sales_demo_tenant` JOIN `sales_lead` JOIN `tenant` | 2 min |
| Expiring soon count | `sales_demo_tenant` WHERE expires_at BETWEEN now() AND now()+7d | 10 min |
| Usage stats in drawer | `sales_demo_tenant` + login event count | 2 min auto-refresh |
| Demo config defaults | `demo_config` settings table | 10 min |

---

## URL Parameters

| Param | Values | Effect |
|---|---|---|
| `?status` | `active`, `expired`, `all` | Filter by is_active; default `active` |
| `?type` | `school_demo`, `college_demo`, `coaching_demo`, `blank` | Filter by data_template |
| `?expiry_within` | Integer days | Filter to tenants expiring within N days |
| `?q` | String | ILIKE search on institution_name from joined sales_lead |
| `?page` | Integer | Pagination; 25 rows per page default |

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/k/demos/table/` | Demo table | Filter/page change | `#k-demos-table` |
| `htmx/k/demos/<id>/usage/` | Usage stats card | Drawer open, 2-min refresh | `#k-demo-usage-{id}` |
| `htmx/k/demos/kpi/` | KPI strip | After create/expire (5-min refresh) | `#k-demos-kpi` |
| `htmx/k/demos/provision-status/<job_id>/` | Provisioning status poll | Every 3s during wizard Step 3 | `#k-provision-status` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────┐
│  DEMO TENANT MANAGER              [+ Create Demo Tenant]    │
├──────────┬──────────────┬──────────────┬────────────────────┤
│ Active   │ Expiring in  │ Expired      │ Avg Prospect       │
│ Trials   │ 7 Days       │ This Month   │ Logins per Trial   │
│ 18       │ 4            │ 6            │ 3.2                │
├──────────┴──────────────┴──────────────┴────────────────────┤
│  [Active▼] [Type▼] [Expiry Within▼]  🔍 Search institution  │
├────────────┬────────────┬──────────┬──────┬────────┬────────┤
│ Institution│ Type       │ Expires  │Login │Resets  │Actions │
├────────────┼────────────┼──────────┼──────┼────────┼────────┤
│ KIMS School│ SCHOOL_DEMO│ 5 days   │ 4    │ 1      │[···]   │
│ SR College │COLLEGE_DEMO│ 12 days  │ 0    │ 0      │[···]   │
│ Speed Coach│COACHING_DEM│ 2 days ⚠│ 7    │ 2      │[···]   │
├────────────┴────────────┴──────────┴──────┴────────┴────────┤
│  Showing 1–25 of 18 active                        ← 1 2 →  │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. KPI Strip

Four metric tiles updated together via HTMX after any create/expire/deactivate action.

```
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ 18               │ │ 4                │ │ 6                │ │ 3.2              │
│ Active Trials    │ │ Expiring in 7d   │ │ Expired This Mth │ │ Avg Logins/Trial │
│                  │ │ ⚠ 2 with 0 logins│ │ (incl. deactive) │ │ (active only)    │
└──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘
```

- **Active Trials:** COUNT `is_active=True`
- **Expiring in 7 Days:** COUNT `expires_at BETWEEN now() AND now()+7d AND is_active=True`. Amber tile if count > 0. Sub-label: "N with 0 logins" in amber if any expiring tenants have `total_logins < 2` (prospect has barely engaged)
- **Expired This Month:** COUNT `is_active=False AND expires_at` in current calendar month
- **Avg Prospect Logins:** AVG `total_logins` WHERE `is_active=True`. Green if ≥ 3.0, amber if 1.0–2.9, red if < 1.0

---

### 2. Filter Bar

```
[Active ▼]  [Type ▼]  [Expiry Within ▼]  [🔍 Search institution name...]  [Clear All]
```

- **Status toggle:** Active / Expired / All (single-select dropdown)
- **Type:** Multi-select checkbox: SCHOOL_DEMO / COLLEGE_DEMO / COACHING_DEMO / BLANK
- **Expiry Within:** Dropdown — 3 days / 7 days / 14 days / Any (default Any)
- **Search:** ILIKE on `sales_lead.institution_name`; 300ms debounce before HTMX fire
- **Clear All:** Resets all filters to defaults; visible only when any filter is non-default

---

### 3. Demo Tenant Table

25 rows per page. Sortable by institution name, expires_at, total_logins, reset_count.

| Column | Detail |
|---|---|
| Institution Name | Linked to K-03 account profile; shows institution type as small sub-label |
| Demo Type | Badge: STANDARD=blue / CUSTOM=violet / ENTERPRISE_POC=indigo |
| Linked Lead Stage | Stage badge pulled from joined sales_lead.stage |
| Expires At | Formatted relative: "19 days" if >3d / "2 days ⚠" (amber) if ≤3d / "Expired" (red) if past |
| Total Logins | Integer count from sales_demo_tenant.total_logins |
| Reset Count | Integer from sales_demo_tenant.reset_count |
| Actions | 3-dot menu: View Details / Reset Data / Extend Expiry / Deactivate |

Row background: amber tint if expires within 3 days; red tint if expired; white/grey-50 otherwise.

**Row click** opens Demo Detail Drawer.

**Pagination:** "Showing X–Y of Z [status]" + previous/next page links via HTMX.

---

### 4. Create Demo Tenant Wizard

Modal, 3 steps. Accessible via [+ Create Demo Tenant] button. Visible to #62 only.

**Step 1 — Link to Lead**

```
┌──────────────────────────────────────────────────────────────────┐
│  Create Demo Tenant (1 of 3) — Link to Lead                      │
├──────────────────────────────────────────────────────────────────┤
│  Search Lead*     [Type institution name to search...    ]       │
│                   ┌──────────────────────────────────┐          │
│                   │ KIMS High School — Hyderabad      │          │
│                   │ Stage: DEMO_DONE  Owner: Rahul    │          │
│                   └──────────────────────────────────┘          │
│  Selected:        KIMS High School (lead_id: 4028)               │
│                   Institution Type auto-detected: SCHOOL         │
│                                                                  │
│  ℹ Lead not found? Create the lead first in the Pipeline.        │
│                                                                  │
│  [Cancel]                                   [Next: Configure →] │
└──────────────────────────────────────────────────────────────────┘
```

- Search queries `sales_lead` ILIKE on institution_name (minimum 2 chars)
- Leads that already have an active `sales_demo_tenant` are shown with "(Demo active)" label — can still proceed to create a replacement, with warning
- Institution type auto-populated from selected lead

**Existing active demo detection:** If the selected lead already has an active `sales_demo_tenant` record, Step 1 shows a warning banner:
"⚠ This lead already has an active demo tenant (Tenant ID: #T1234, expires in 12 days). Creating a new tenant will automatically deactivate the existing one. Do you want to continue?"
[Continue — deactivate existing] [Cancel]
If confirmed: existing tenant's `is_active` set to `False` and `expires_at` backdated to `now()` before new tenant provisioning begins. Old tenant appears in Expired Demos accordion.

**Step 2 — Configuration**

```
┌──────────────────────────────────────────────────────────────────┐
│  Create Demo Tenant (2 of 3) — Configuration                     │
├──────────────────────────────────────────────────────────────────┤
│  Demo Type*       ○ STANDARD (auto-provisioned, 30 min setup)    │
│                   ○ CUSTOM (manual setup, contact infra team)    │
│                   ○ ENTERPRISE_POC (extended trial, >30 days)    │
│                                                                  │
│  Data Template*   [SCHOOL_DEMO  ▼]  (auto-selected from lead)    │
│                   Options: SCHOOL_DEMO / COLLEGE_DEMO /          │
│                   COACHING_DEMO / BLANK                          │
│                                                                  │
│  Student Seed     [50   ]  (range: 10–500)                       │
│  Exam Seed Count  [5    ]  (range: 1–20)                         │
│                                                                  │
│  Trial Duration*  ○ 14 days  ○ 30 days  ● 30 days  ○ 60 days    │
│                   ○ 90 days  (default: 30)                       │
│  Note: ENTERPRISE_POC requires Sales Manager approval for >30d.  │
│                                                                  │
│  Demo Admin Email [ramesh@kims.edu  ]  (auto-filled from lead)   │
│                                                                  │
│  [← Back]                               [Next: Review →]        │
└──────────────────────────────────────────────────────────────────┘
```

**ENTERPRISE_POC duration > 30 days — approval gate:**
When demo_type = ENTERPRISE_POC and trial duration > 30 days is selected:
- Form shows amber banner: "Trials over 30 days for Enterprise PoC require Sales Manager approval."
- "Provision" button changes to "Submit for Approval" — sends in-app + email notification to Sales Manager (#57).
- Demo Manager dashboard shows the request as "Pending Approval" badge on that lead row.
- Sales Manager sees approval request in K-07 or via notification: [Approve] [Reject] buttons.
- On approval: provisioning proceeds automatically. On rejection: Demo Manager notified with rejection reason.
- Maximum allowed: 90 days regardless of approval.

**Step 3 — Confirm and Provision**

```
┌──────────────────────────────────────────────────────────────────┐
│  Create Demo Tenant (3 of 3) — Confirm & Provision               │
├──────────────────────────────────────────────────────────────────┤
│  Institution:     KIMS High School, Hyderabad                    │
│  Demo Type:       STANDARD                                       │
│  Template:        SCHOOL_DEMO                                    │
│  Students seeded: 50   Exams seeded: 5                           │
│  Trial duration:  30 days (expires 20 Apr 2026)                  │
│  Admin email:     ramesh@kims.edu                                │
│                                                                  │
│  Provisioning typically takes 30–90 seconds.                     │
│                                                                  │
│  [← Back]                            [Provision Demo Tenant]    │
└──────────────────────────────────────────────────────────────────┘
```

On "Provision Demo Tenant": POST to `/group1/k/demos/create/` → async tenant provisioning via Platform Admin API (#10) → webhook callback sets `tenant_id` on `sales_demo_tenant`.

During provisioning: spinner overlay "Setting up sandbox environment..." with animated indicator. Modal stays open. If provisioning takes > 120 seconds, shows: "This is taking longer than usual. You can close this modal — the demo will appear in the list when ready."

On success: modal closes, table refreshes, KPI strip refreshes, toast shown.

**Provisioning lifecycle:**
- On "Provision" button click: (1) POST /group1/k/demos/create/ → immediate 202 Accepted. (2) Modal stays open with animated spinner "Setting up your sandbox environment..." (3) HTMX polls `htmx/k/demos/provision-status/<job_id>/` every 3 seconds. (4) Typical completion: 30–90 seconds.

**Provisioning success:** Polling returns `status: "complete"` with `tenant_id`. Modal auto-closes. Table refreshes via HTMX OOB swap. Success toast: "Demo tenant provisioned for [Institution]. [View Details]"

**Provisioning failure:** Polling returns `status: "failed"` with `error_reason`. Modal shows error card: "Provisioning failed: [reason]. This has been reported to the platform team." [Retry] [Cancel] buttons. Retry re-triggers the same POST. If 3 retries fail: "Provisioning requires manual intervention. Engineering team notified." — creates alert in Div-C Engineering dashboard. In-app + email notification sent to Demo Manager (#62) and Sales Manager (#57).

**Provisioning timeout (>120s):** If polling reaches 120s without completion, shows: "This is taking longer than usual. You can leave this page — we'll email you when the sandbox is ready." Modal can be closed; provisioning continues in background. Email sent to Demo Manager on completion.

---

### 5. Demo Detail Drawer

Opens on row click or via 3-dot "View Details". Full-width slide-in from right.

**Demo expiry and prospect engagement:**
When Celery Task K-4 deactivates an expired demo tenant, it does NOT automatically move the linked lead's stage. The lead remains in whatever stage it was in (e.g., DEMO_SCHEDULED). The prospect loses portal access silently at the backend.

On the next Demo Manager login, the expired tenant appears in the "Expired Demos" accordion. If the lead is still active (not CLOSED_WON or CLOSED_LOST), an amber alert shows next to the expired record: "Lead still active — consider reactivating or scheduling a follow-up."

What if prospect tries to log in after expiry? Tenant shows "Access expired. Contact EduForge sales team." page (rendered by Platform layer, not Sales module). No error page — graceful messaging. Demo Manager can reactivate from the Expired Demos accordion within 30 days; after 30 days, tenant data is purged by infra team.

**Header:**
```
KIMS High School                                         [ACTIVE]
edu-demo-4821   ·   STANDARD  ·  SCHOOL_DEMO
```

**Usage Stats section:**
| Metric | Value |
|---|---|
| Total Logins | 4 |
| Last Login | 20 Mar 2026 · 4:12 PM |
| Created | 10 Mar 2026 (11 days ago) |
| Expires | 9 Apr 2026 (19 days remaining) |
| Days Active | 11 of 30 |
| Reset Count | 1 (last reset: 15 Mar 2026) |

**Admin credentials (masked):**
- Admin email: "ram***@kims.edu"
- [Copy Access Link] button — generates one-time 24h token, copies to clipboard, sends email to contact_email

**Login activity sparkline:**
- Chart.js bar chart showing logins per day for last 14 days
- HTMX auto-refreshes every 2 minutes while drawer is open
- X-axis: day labels (e.g., "Mar 8 … Mar 21")
- Y-axis: login count
- Zero-login days shown in grey; login days in blue

**Action Buttons (Demo Manager #62; #57 can extend only):**

*Reset Demo Data:*
Confirm modal: "Reset all data? Student progress, exam results, and customisations will be lost. This is irreversible." POST `/group1/k/demos/<id>/reset/` — increments `reset_count`, triggers re-seed from data_template, updates `last_reset_at=now()`.

*Extend Expiry:*
Dropdown options: +7 days / +14 days / +30 days. Guard: `expires_at + extension` must not exceed `created_at + 90 days`. If over 90 days: "Cannot extend beyond 90 days from creation. Contact Sales Manager for an exception." PATCH `sales_demo_tenant.expires_at`.

**ENTERPRISE_POC approval gate on extensions:** For demo_type=ENTERPRISE_POC, extensions beyond the approved original duration require the same Sales Manager approval as initial creation (see Create Demo Tenant Wizard, Step 2). The "Extend Expiry" button for ENTERPRISE_POC tenants shows "Submit Extension Request" instead of immediate options, triggering the same approval workflow. Once approved, the tenant's expires_at is updated. Maximum 90 days from creation_date regardless of extension approvals.

*Deactivate:*
Confirm: "Are you sure? The prospect will lose access immediately." PATCH `is_active=False`. Row turns red in table. KPI strip recalculates.

*Generate Access Link:*
Creates a time-limited (24 hours) login token for prospect. Copies URL to clipboard. Sends email notification to `sales_lead.contact_email`. Button shows "Generating..." spinner during async token creation.

---

### 6. Expired Demos Section

Collapsed accordion at the bottom of the main page, below the active table. Title: "Expired Demos (last 30 days)" with count badge.

Columns same as main table. Actions per row:

- **Reactivate:** Creates new 14-day trial starting from today; increments `reset_count`. Available to #62 only.
- **Archive:** Marks tenant as archived; removes from this list. Physical tenant deletion from infra scheduled 7 days after archive (background Celery task). Confirmation: "Archive this demo? The tenant will be deleted from the server in 7 days."

Empty state in accordion: "No demos expired in the last 30 days."

---

### 7. Demo Config Tab

Second top-level tab on the page (alongside main tenant list). Accessible to #62 only. Title: "Demo Configuration".

**Default Settings panel:**

| Setting | School | College | Coaching | Blank |
|---|---|---|---|---|
| Default Trial Duration | 30 days | 30 days | 14 days | 14 days |
| Default Student Seed | 50 | 200 | 30 | 0 |
| Default Exam Seed | 5 | 10 | 3 | 0 |

All cells editable inline (click to edit). PATCH on change. Affects future demo creations only — no retroactive change.

**Template Refresh panel:**
- "Last template refresh: 15 Feb 2026"
- [Trigger Template Refresh] button — pulls latest product features from production snapshot into SCHOOL_DEMO / COLLEGE_DEMO / COACHING_DEMO templates. Async operation; shows last status.
- Warning: "Template refresh affects all future resets. Existing active demos are not affected until next reset."

**Demo Admin Password Policy:**
- Default password format: "EduDemo@[year]" or custom pattern
- [Change Pattern] opens text field with preview

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| Active demos table | No active demo tenants | "No active demo tenants. Create the first trial to start demonstrating EduForge." |
| Filter results | Query returns 0 rows | "No demo tenants match the current filters. Try clearing some filters." |
| Expiring soon | No tenants expiring in 7 days | "No demos expiring in the next 7 days." |
| Expired section | No expired tenants in last 30 days | "No demos expired in the last 30 days." |

---

## Toast Messages

| Action | Toast |
|---|---|
| Demo tenant created | "Demo tenant provisioned for KIMS High School" (green) |
| Provisioning started | "Sandbox is being set up for KIMS High School. Check back in a moment." (blue) |
| Demo data reset | "Demo data reset for KIMS High School. Seed data reloaded." (green) |
| Expiry extended | "Expiry extended to 19 Apr 2026 for KIMS High School" (green) |
| Cannot extend beyond 90d | "Cannot extend beyond 90 days from creation. Contact Sales Manager." (amber) |
| Demo deactivated | "Demo tenant deactivated for KIMS High School" (amber) |
| Demo reactivated | "Demo tenant reactivated for KIMS High School (14-day trial)" (green) |
| Demo archived | "Demo archived. Tenant will be deleted in 7 days." (grey) |
| Access link generated | "Access link copied to clipboard. Valid for 24 hours." (blue) |
| Config saved | "Demo configuration updated" (green) |
| Template refresh triggered | "Template refresh started. This may take a few minutes." (blue) |

---

---

## Authorization

**Route guard:** `@division_k_required(allowed_roles=[62, 57, 58, 59, 60])` applied to `DemoManagerView`.

| Scenario | Behaviour |
|---|---|
| Demo Manager (#62) | Full CRUD access |
| Sales Manager (#57) | Read all + extend expiry only. POST to `/demos/create/` returns 403. POST to `/demos/<id>/reset/` returns 403. |
| Sales Execs (#58–60) | Read own linked demos only (queryset: `WHERE lead_id IN (SELECT id FROM sales_lead WHERE owner_id = request.user.id)`). No write access. |
| Any other role | 403 Forbidden |
| Provisioning webhook callback | Authenticated via `X-Provisioning-Secret` header (shared secret stored in AWS Secrets Manager); not user-session-based. |

---

## Role-Based View Summary

| Feature | Demo Manager (#62) | #57 Sales Manager | #58 Schools | #59 Colleges | #60 Coaching | #63/#95/#96/#97 |
|---|---|---|---|---|---|---|
| View active demo list | Yes (all) | Yes (all) | Own linked | Own linked | Own linked | No access |
| View demo detail drawer | Yes | Yes | Own linked | Own linked | Own linked | No access |
| Create demo tenant | Yes | No | No | No | No | No |
| Reset demo data | Yes | No | No | No | No | No |
| Extend expiry | Yes | Yes | No | No | No | No |
| Deactivate | Yes | No | No | No | No | No |
| Reactivate expired | Yes | No | No | No | No | No |
| Archive expired | Yes | No | No | No | No | No |
| Generate access link | Yes | No | No | No | No | No |
| Demo config tab | Yes | No | No | No | No | No |
| Trigger template refresh | Yes | No | No | No | No | No |
