# div-a-06 — Institution Detail

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total institutions | 2,050 |
| Max students per institution | 15,000 (coaching centres) |
| Max exams per institution (all-time) | ~2,000+ for large coaching centres |
| API keys per institution | 1–5 |
| Webhooks per institution | 1–10 |
| Invoices per institution/year | 12 (monthly) or 1 (annual) |
| Support tickets per institution/month | ~3–8 (average) |

**Why this matters:** Before a renewal call, the COO needs: usage trends, billing health, exam activity, contacts, health score — all in one page. Before a high-value coaching centre meeting, the CEO needs ARR, NPS, and recent incidents. This page replaces 6 separate admin screens with one full-context view.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Institution Detail — {Institution Name} |
| Route | `/exec/institutions/<institution_id>/` |
| Django view | `InstitutionDetailView` |
| Template | `exec/institution_detail.html` |
| Priority | P1 |
| Nav group | Institutions |
| Required role | `exec`, `superadmin`, `ops`, `support` |
| 2FA required | Editing contacts, editing plan, suspending |
| HTMX poll | Health score: every 60s |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ← Institutions   ABC Coaching Centre    [Enterprise]  [● Active]             │
│                  Hyderabad, Telangana   Joined: Jan 2022                     │
│              [Edit] [Suspend] [Login as Admin] [Export Report]               │
├────────────┬─────────────┬────────────┬────────────┬────────────────────────┤
│  Students  │  ARR        │  Health    │  Exams     │  Last Active           │
│  12,400    │  ₹42.8 L    │  82 / 100  │  842       │  2h ago                │
├────────────┴─────────────┴────────────┴────────────┴────────────────────────┤
│ TABS: [Overview] [Exams] [Students] [Billing] [Usage] [Contacts] [Settings] │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: OVERVIEW                                                                │
│ ┌───────────────────────────────┐ ┌───────────────────────────────────────┐ │
│ │ Platform Usage (12m chart)    │ │ Health Score Breakdown                │ │
│ │ Students / Exams / Logins     │ │ Gauge + factor bars                   │ │
│ └───────────────────────────────┘ └───────────────────────────────────────┘ │
│ ┌───────────────────────────────┐ ┌───────────────────────────────────────┐ │
│ │ Recent Incidents              │ │ Expansion Signals                     │ │
│ │ Last 5 affecting this inst    │ │ Usage vs Plan limits progress bars    │ │
│ └───────────────────────────────┘ └───────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Page Header

### 4.1 Breadcrumb + Identity Bar

**Breadcrumb:** `← Institutions` (links to div-a-05 preserving filters via `Referer` or back-button)
`text-sm text-[#6366F1] hover:text-[#818CF8]`

**Identity block:**
```
ABC Coaching Centre    [Enterprise badge]  [● Active badge]
Hyderabad, Telangana · CIN: U80903TG2015PTC098234 · Joined 15 Jan 2022
```
- Institution name: `text-2xl font-bold text-white`
- Sub-line: `text-sm text-[#94A3B8]`
- Plan badge: gold pill `bg-[#451A03] text-[#FCD34D] text-xs px-2 py-0.5 rounded-full font-medium`
- Status badge: `● Active` green dot + label `bg-[#064E3B] text-[#34D399] text-xs px-2 py-0.5 rounded-full`

**Action buttons (right-aligned):**
- [Edit] `bg-[#131F38] border border-[#1E2D4A] text-white px-3 py-2 rounded-lg text-sm`
- [Suspend] `bg-[#450A0A] text-[#F87171] px-3 py-2 rounded-lg text-sm` (requires 2FA)
- [Login as Admin] `bg-[#131F38] border border-[#1E2D4A] text-white px-3 py-2 rounded-lg text-sm` (requires 2FA)
- [Export Report] `bg-[#131F38] border border-[#1E2D4A] text-white px-3 py-2 rounded-lg text-sm`

---

### 4.2 KPI Strip (below header)

5 cards · `flex gap-4 p-4`
**Poll:** `hx-get="/exec/institutions/{id}/?part=kpi" hx-trigger="every 60s[!document.querySelector('.drawer-open,.modal-open')]"`

| # | Card | Format | Alert |
|---|---|---|---|
| 1 | Students | Count · `data-count-up` | — |
| 2 | ARR | `₹XX.X L` · delta vs prev year | — |
| 3 | Health Score | 0–100 · coloured | < 60 = red |
| 4 | Total Exams | All-time count | — |
| 5 | Last Active | Relative time | > 7d = amber |

---

## 5. Tab Bar

`flex border-b border-[#1E2D4A] px-6`
**Tabs:** Overview · Exams · Students · Billing · Usage · Contacts · Settings
**Active tab:** `text-white border-b-2 border-[#6366F1]`
**Inactive tab:** `text-[#94A3B8] hover:text-white`
**HTMX:** `hx-get="?part={tab_id}&institution_id={id}"` `hx-target="#tab-content"` `hx-swap="innerHTML"` `hx-push-url="?tab={tab_id}"`

---

## 6. Tab: Overview

`id="tab-overview"` · `hx-get="?part=overview"` on tab click

**2-column layout:** `grid grid-cols-2 gap-4 p-4`

### 6.1 Platform Usage Chart (left, col 1)

**Title:** "Platform Activity — Last 12 Months"
**Chart type:** Multi-line · Chart.js 4.4.2 · Canvas height 220px
**Canvas id:** `inst-activity-chart`
**Destroy-before-recreate guard:** `window._charts?.instActivity?.destroy()`

**Series:**
| Series | Colour | Y-axis |
|---|---|---|
| Active Students/month | `#6366F1` | left |
| Exams Conducted/month | `#22D3EE` | left |
| Login Sessions/month | `#10B981` | right |

**Config highlights:**
```js
scales: {
  x: { grid: { color: '#1E2D4A' }, ticks: { color: '#64748B' } },
  yLeft: { position: 'left', grid: { color: '#1E2D4A' }, ticks: { color: '#64748B' } },
  yRight: { position: 'right', grid: { drawOnChartArea: false }, ticks: { color: '#64748B' } },
}
```

### 6.2 Health Score Breakdown (right, col 2)

**Health gauge:** SVG arc gauge 180px wide · score value in center `text-3xl font-bold`
- ≥ 80: `#34D399` · 60–79: `#FCD34D` · < 60: `#F87171`

**Factor breakdown table below gauge:**
| Factor | Score | Weight | Contribution | Trend |
|---|---|---|---|---|
| Exam Frequency | 85 | 25% | 21.3 | ↑ sparkline |
| Login Activity | 90 | 20% | 18.0 | → sparkline |
| Invoice Health | 100 | 25% | 25.0 | — |
| Support Tickets | 70 | 15% | 10.5 | ↓ sparkline |
| NPS Score | 75 | 15% | 11.3 | → sparkline |
| **Total** | | | **86.1** | |

**Trend sparklines:** 7-point inline SVG sparkline `width:40px height:16px`

### 6.3 Recent Incidents (left, col 1, row 2)

Last 5 incidents that affected this institution (filtered from global incident log)
**Table:** Severity badge · Title (truncated 40 chars) · Started · Duration · Status
**Empty state:** "No incidents in the last 90 days ✓" `text-[#34D399]`
**[View All Incidents →]** link → div-a-12 with institution filter

### 6.4 Expansion Signals (right, col 2, row 2)

**Title:** "Usage vs Plan Limits"
**Progress bars for each limit:**
```
Students     ███████████░░░  12,400 / 15,000  (83%)
Exams/month  ████████░░░░░░   842 / 1,000    (84%)
API calls/d  ██████░░░░░░░░   3.2M / 5M      (64%)
Storage      ████░░░░░░░░░░   42 GB / 100 GB (42%)
```
- Progress bar: `bg-[#1E2D4A] rounded-full h-2` · fill: `bg-[#6366F1]` ≤ 80% · `bg-[#F59E0B]` 80–95% · `bg-[#EF4444]` > 95%
- "> 80% used" = upsell signal → show `⚡ Upgrade opportunity` chip `bg-[#451A03] text-[#FCD34D] text-xs px-2 py-0.5 rounded-full`

---

## 7. Tab: Exams

`id="tab-exams"` · `hx-get="?part=exams&institution_id={id}"`

**Toolbar:** Search exam name · Status filter (Live/Scheduled/Completed/Failed) · Date range · Subject filter · `[Schedule Exam]` button

**Exam table:**
| Column | Detail |
|---|---|
| Exam Name | Truncated · click → opens Exam Detail Drawer |
| Subject | Badge |
| Scheduled | Date + time |
| Duration | Minutes |
| Students | Registered / Appeared |
| Avg Score | % · bar chart cell |
| Status | Status badge |
| Actions ⋯ | View Results / Cancel / Reschedule |

**Pagination:** 25/page · sort by Scheduled Date desc default

---

## 8. Tab: Students

`id="tab-students"` · `hx-get="?part=students&institution_id={id}"`

**Summary row:** Total enrolled · Active (last 30d) · Avg score (last 3 exams) · Top performer (name + score)

**Student table:**
| Column | Detail |
|---|---|
| Student | Name + avatar initial |
| Grade / Batch | Text |
| Enrolled | Date |
| Exams taken | Count |
| Avg Score | % |
| Last active | Relative |
| Status | Active / Inactive / Suspended |
| Actions ⋯ | View Profile / Suspend |

**Search:** Debounced 400ms on name/roll number
**Filters:** Grade · Batch · Status · Last active range
**Pagination:** 50/page

---

## 9. Tab: Billing

`id="tab-billing"` · `hx-get="?part=billing&institution_id={id}"`

### 9.1 Billing Summary Row

`flex gap-6 p-4 bg-[#0D1526] rounded-xl border border-[#1E2D4A] mb-4`
- Current plan: Plan badge + price per month
- ARR: `₹XX.X L`
- Billing cycle: Monthly / Annual
- Next renewal: Date + days remaining badge
- Outstanding balance: `₹0` green or `₹X.X L` red
- [Change Plan] [Change Billing Cycle] buttons (2FA required)

### 9.2 Invoice Table

| Column | Detail |
|---|---|
| Invoice # | Clickable → Invoice Drawer |
| Period | e.g., "Feb 2025" |
| Amount | `₹XX,XXX` right-aligned |
| Due date | Date |
| Paid date | Date or "—" |
| Status | Paid (green) / Overdue (red) / Pending (amber) / Draft (grey) |
| Actions ⋯ | Download PDF / Mark Paid / Send Reminder |

**Overdue invoices:** Row background `bg-[#1A0A0A]` + red status badge
**[+ Generate Invoice]** button (manual invoice)
**Pagination:** 12/page (1 year visible at default)

---

## 10. Tab: Usage

`id="tab-usage"` · `hx-get="?part=usage&institution_id={id}"`

### 10.1 Usage Chart

Multi-metric line chart (last 90 days)
Toggle series: API Calls · Webhooks · Exam events · Login sessions
**Y-axis:** count · log scale toggle available

### 10.2 API Keys sub-tab

Compact table: Key name · Environment · Last used · Status · [Rotate] [Revoke]

### 10.3 Webhook sub-tab

Compact table: Endpoint URL (masked) · Events subscribed · Last delivery · Health · [Test] [Edit]

---

## 11. Tab: Contacts

`id="tab-contacts"` · `hx-get="?part=contacts&institution_id={id}"`

**Contact cards (grid):**
Each card `bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4`:
- Role badge (Primary / Billing / Technical / Operations)
- Name `text-base font-semibold text-white`
- Email `text-sm text-[#94A3B8]` + copy icon
- Phone `text-sm text-[#94A3B8]` + copy icon
- Last contacted: relative date
- [Edit Contact] [Remove]

**[+ Add Contact]** button → Add Contact Modal (see §13.1)

---

## 12. Tab: Settings

`id="tab-settings"` · `hx-get="?part=settings&institution_id={id}"`
**2FA required for all saves**

### 12.1 General Settings

| Setting | Type | Detail |
|---|---|---|
| Institution name | Text input | Editable |
| CIN / GST number | Text input | |
| Registered address | Textarea | |
| Timezone | Dropdown | Default: Asia/Kolkata |
| Logo | Image upload (< 2 MB, PNG/JPG) | Preview shown |

### 12.2 Feature Flags

Toggle switches (each `accent-[#6366F1]`):
- Proctoring enabled
- API access
- White-label portal
- Custom email domain
- Parent portal access
- Bulk SMS enabled

### 12.3 Notification Settings

Who gets notified for: Platform incidents · Billing alerts · Exam failures · SLA breaches
Each event: checkboxes for Primary / Billing / Technical contacts

**[Save Settings]** button · `hx-post="?part=save_settings"` · success: toast "Settings saved" · error: inline validation

---

## 13. Modals

### 13.1 Add / Edit Contact Modal (480 px)

| Field | Type | Validation |
|---|---|---|
| Full name | Text | Required |
| Role | Select | Primary / Billing / Technical / Operations |
| Email | Email | Required · unique per institution |
| Phone | Tel | Optional |
| Notes | Textarea | Optional |

**Footer:** [Cancel] [Save Contact]

---

### 13.2 Change Plan Modal (560 px)

**2FA required before opening.**

**Current plan highlighted** in plan comparison grid:
| Feature | Starter | Standard | Professional | Enterprise |
|---|---|---|---|---|
| Students | 500 | 2,000 | 10,000 | Unlimited |
| Exams/month | 10 | 50 | 200 | Unlimited |
| API access | — | — | ✓ | ✓ |
| Price/month | ₹5K | ₹15K | ₹40K | Custom |

**Proration notice:** "Switching from Professional to Enterprise will add ₹X to your next invoice."
**Footer:** [Cancel] [Confirm Plan Change]

---

### 13.3 Suspend Institution Modal (480 px)

**2FA required.** Warning banner: "Suspending this institution will immediately prevent all logins and exam access for 12,400 students."
| Field | Type |
|---|---|
| Reason | Select: Non-payment / Policy violation / Requested by institution / Other |
| Notes | Textarea |
| Notify contacts | Checkbox (default: checked) |
| Reactivation date | Date picker (optional) |

**Footer:** [Cancel] [Suspend Institution]

---

## 14. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/inst_detail_kpi.html` | Page load · poll 60s |
| `?part=overview` | `exec/partials/inst_overview.html` | Overview tab click |
| `?part=exams` | `exec/partials/inst_exams.html` | Exams tab click · filter change |
| `?part=students` | `exec/partials/inst_students.html` | Students tab click · filter change |
| `?part=billing` | `exec/partials/inst_billing.html` | Billing tab click |
| `?part=usage` | `exec/partials/inst_usage.html` | Usage tab click |
| `?part=contacts` | `exec/partials/inst_contacts.html` | Contacts tab click |
| `?part=settings` | `exec/partials/inst_settings.html` | Settings tab click |
| `?part=save_settings` | JSON | Settings form POST |

**Django view dispatch:**
```python
class InstitutionDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_institutions"

    def get(self, request, institution_id):
        institution = get_object_or_404(Institution, pk=institution_id)
        ctx = self._build_context(request, institution)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/inst_detail_kpi.html",
                "overview": "exec/partials/inst_overview.html",
                "exams": "exec/partials/inst_exams.html",
                "students": "exec/partials/inst_students.html",
                "billing": "exec/partials/inst_billing.html",
                "usage": "exec/partials/inst_usage.html",
                "contacts": "exec/partials/inst_contacts.html",
                "settings": "exec/partials/inst_settings.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/institution_detail.html", ctx)

    def post(self, request, institution_id):
        part = request.GET.get("part", "")
        institution = get_object_or_404(Institution, pk=institution_id)
        if part == "save_settings":
            return self._handle_save_settings(request, institution)
        return HttpResponseNotAllowed(["GET"])
```

**Poll pause:**
```html
<div id="inst-kpi-strip"
     hx-get="/exec/institutions/{{institution.id}}/?part=kpi"
     hx-trigger="every 60s[!document.querySelector('.drawer-open,.modal-open')]"
     hx-swap="innerHTML">
```

---

## 15. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 250 ms | > 600 ms |
| Overview tab (charts + health) | < 600 ms | > 1.5 s |
| Exams tab (25 rows) | < 400 ms | > 1 s |
| Students tab (50 rows) | < 400 ms | > 1 s |
| Billing tab (12 invoices) | < 300 ms | > 800 ms |
| Usage chart (90 days) | < 600 ms | > 1.5 s |
| Settings tab | < 200 ms | > 500 ms |
| Full page initial load | < 1.2 s | > 3 s |

---

## 16. States & Edge Cases

| State | Behaviour |
|---|---|
| Institution suspended | Header status badge = Suspended red · amber banner "This institution is currently suspended" at top |
| Institution churned | Read-only mode; all action buttons hidden except [Reactivate]; banner "Churned on {date}" |
| No exams ever | Exams tab shows "No exams scheduled yet" + [Schedule First Exam] CTA |
| No students enrolled | Students tab shows "No students enrolled yet" |
| Overdue invoice > 30 days | Billing tab shows red alert banner; KPI strip ARR card has red border |
| Health score < 60 | Health card background `bg-[#450A0A]`; risk factor table shows red rows |
| API key expiring in 7 days | Usage tab API Keys section shows amber badge "Expiring soon" |
| Webhook failing (health = Failing) | Usage tab Webhook section shows red `🔴 Failing` badge |
| Login as Admin: 2FA denied | Action blocked; toast "2FA required to login as institution admin" |

---

## 17. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`7` | Switch tabs |
| `E` | Open Edit modal (general settings) |
| `R` | Refresh current tab |
| `Esc` | Close any open drawer/modal |
| `?` | Keyboard shortcut help |

---

## 18. Template Files

| File | Purpose |
|---|---|
| `exec/institution_detail.html` | Full page shell |
| `exec/partials/inst_detail_kpi.html` | KPI strip (5 cards) |
| `exec/partials/inst_overview.html` | Overview tab (2×2 grid) |
| `exec/partials/inst_exams.html` | Exams tab table |
| `exec/partials/inst_students.html` | Students tab table |
| `exec/partials/inst_billing.html` | Billing tab |
| `exec/partials/inst_usage.html` | Usage charts + API/Webhook sub-tabs |
| `exec/partials/inst_contacts.html` | Contacts grid |
| `exec/partials/inst_settings.html` | Settings form |
| `exec/partials/inst_add_contact_modal.html` | Add/Edit Contact modal |
| `exec/partials/inst_change_plan_modal.html` | Change Plan modal |
| `exec/partials/inst_suspend_modal.html` | Suspend modal |

---

## 19. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.2 |
| `TabBar` | §5 |
| `MultiLineChart` | §6.1 |
| `HealthGauge` | §6.2 |
| `FactorBreakdownTable` | §6.2 |
| `SparklineInline` | §6.2 trends |
| `IncidentsCompact` | §6.3 |
| `UsageLimitBar` | §6.4 |
| `ExamTable` | §7 |
| `StudentTable` | §8 |
| `BillingSummaryRow` | §9.1 |
| `InvoiceTable` | §9.2 |
| `UsageLineChart` | §10.1 |
| `ContactCard` | §11 |
| `FeatureFlagToggle` | §12.2 |
| `DrawerPanel` | Exam detail drawer |
| `ModalDialog` | §13.1–13.3 |
| `PlanComparisonGrid` | §13.2 |
| `PollableContainer` | KPI strip |
