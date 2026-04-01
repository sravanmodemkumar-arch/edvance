# 03 — CEO Dashboard

> **URL:** `/group/gov/ceo/`
> **File:** `03-ceo-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group CEO (G4) — exclusive landing page

---

## 1. Purpose

Operational command centre for the Group CEO. The CEO activates/deactivates branches, monitors
daily group operations, signs off operational approvals, and tracks fee collection vs targets.
This dashboard gives real-time visibility of every branch's operational status — a live operations
room for a group running 48–50 branches simultaneously.

Key CEO responsibilities surfaced here:
- Branch activation / deactivation with audit trail
- Daily fee collection monitoring (₹ crores across branches)
- Escalations requiring CEO decision
- Operational approvals queue (CEO-level items only)
- Branch grievance and SLA status

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group CEO | G4 | Full — all sections, all actions | Exclusive dashboard |
| Chairman / MD | G5 | — | Have their own dashboards |
| President / VP | G4 | — | Have their own dashboards |
| Trustee / Advisor | G1 | — | Have their own dashboards |
| Exec Secretary | G3 | — | Has own dashboard |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  CEO Dashboard
```

### 3.2 Page Header
```
CEO Operations Centre — [CEO Name]                     [Activate Branch ▼]  [View Approvals]
[Group Name] · Last login: [date time]                 [Export Today's Report ↓]
```

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Branch Activation | `48 Active / 50 Total` · `2 deactivated` | Green = all active · Yellow = 1–2 · Red = 3+ | → Branch Overview page 09 |
| Today's Fee Collection | `₹12.4L collected today` · live update | Info | → Fee Revenue Dashboard page 31 |
| Monthly Collection Rate | `94.2% of ₹8.2Cr target` | Green ≥95% · Yellow 85–95% · Red <85% | → Fee Revenue Dashboard page 31 |
| Operational Alerts | `3 open alerts` · pulsing if Critical | Red if any Sev-1 open | → Escalation Centre page 33 |
| CEO Pending Approvals | `5 items` awaiting CEO | Red badge if >0 | → Approval Hub page 17 |
| Grievances Open | `12 open · 3 overdue` | Red if any overdue | → Compliance Overview page 27 |

**HTMX auto-refresh:** Every 3 minutes (fee data) · `hx-trigger="every 3m"` on `#kpi-bar`.

---

## 5. Sections

### 5.1 CEO Approval Queue

> CEO-level operational approvals — not Chairman/MD items.

**Display:** Card list — max 5, "View All in Approval Hub →" link.

**Approval types for CEO:**
- Branch fee structure change (≤15% variance — larger goes to Chairman)
- Staff transfer between branches (proposed by Group HR)
- Operational policy waiver for a specific branch
- Branch infrastructure emergency spend request
- Grievance escalation requiring CEO directive

**Card fields:** Type badge · Subject · Branch · Submitted by · Days pending · [Approve] [Reject] [View Details]

**Approve:** `hx-post` → success toast · card removed · audit log entry.

**Reject:** 420px modal with required reason field.

---

### 5.2 Branch Operations Status Table

> Real-time operational health of every branch.

**Search:** Branch name, city, district. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| State | Multi-select | All states |
| Status | Multi-select | Active · Inactive · Onboarding |
| Fee Status | Select | On track (≥90%) · Warning (75–90%) · Critical (<75%) |
| Grievances | Checkbox | Show only branches with open grievances |
| SLA | Checkbox | Show only SLA-breached branches |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch Name | Text + link | ✅ | → Branch Detail page 10 |
| City | Text | ✅ | |
| Status | Badge | ✅ | Active · Inactive · Onboarding |
| Students Today | Number | ✅ | Today's attendance headcount |
| Today Fee ₹ | Currency | ✅ | Live — collected today |
| Monthly Fee % | Progress bar | ✅ | Red if <85% |
| Open Issues | Number | ✅ | Linked to escalations for that branch |
| SLA Status | Badge | ✅ | On Track · Warning · Breached |
| Last Sync | Timestamp | ✅ | Red if >2h ago |
| Actions | — | ❌ | View · Activate/Deactivate · Escalate |

**Default sort:** SLA Status (Breached first), then Monthly Fee % ascending.

**Pagination:** Server-side · Default 25/page.

**Row select + bulk action:** Export selected branches as CSV.

**Row actions:**
| Action | Trigger | Notes |
|---|---|---|
| View | Opens Branch Detail page 10 | |
| Activate / Deactivate | `branch-activate-confirm` modal | Requires reason — audited |
| Escalate Issue | `escalation-create` drawer | Pre-fills branch context |

---

### 5.3 Fee Collection Summary Cards

> Fee by type for the current month — CEO monitors split between student categories.

**Display:** 4 horizontal metric cards.

| Card | Metric |
|---|---|
| Day Scholar Fees | ₹X.XCr collected / ₹X.XCr expected |
| Hosteler Fees | ₹X.XCr collected / ₹X.XCr expected |
| Integrated Coaching Fees | ₹X.XCr collected / ₹X.XCr expected |
| Transport Fees | ₹X.XCr collected / ₹X.XCr expected |

Each card shows progress bar + collection % + trend arrow vs last month.

**"View Full Fee Dashboard →"** link to page 31.

---

### 5.4 Today's Escalations (incoming)

> Operational incidents needing CEO decision — bubbled up from branch level.

**Display:** Priority-sorted card list (Severity 1 first) — max 5, "View All →" link to page 33.

**Card fields:** Severity badge (1–4) · Type · Branch · Reported by · Hours open · SLA countdown · [Assign to VP] [Handle Myself] [View Details]

**Handle Myself:** Opens `escalation-detail` drawer.

**Assign to VP:** 380px modal — confirm + optional note → assigns to VP, sends VP notification.

---

### 5.5 Quick Actions Grid

| Tile | Link |
|---|---|
| Branch Overview | page 09 |
| Fee Revenue Dashboard | page 31 |
| Approval Workflow Hub | page 17 |
| Escalation & Incident Centre | page 33 |
| Compliance Overview | page 27 |
| Group Audit Log | page 26 |

---

## 6. Drawers & Modals

### 6.1 Modal: `branch-activate-confirm`
- **Width:** 420px
- **Fields:** Warning + reason (required, min 20 chars) + confirmation checkbox "I understand this action is audited"
- **For Deactivate:** Additional warning: "This will prevent all staff and students at [Branch] from accessing the platform"
- **Buttons:** [Confirm] (danger for deactivate) + [Cancel]
- **On confirm:** Branch status changed · MD and Chairman notified via WhatsApp · audit entry

### 6.2 Drawer: `escalation-create` (see also page 33)
- **Width:** 640px
- **Pre-filled:** Branch name from row context
- **Tabs:** Details · Severity · Assignment · Evidence
- **Details tab:** Title · Branch (pre-filled) · Type · Description (textarea, 500 chars)
- **Severity tab:** Severity selector 1–4 with descriptions · SLA auto-calculated
- **Assignment tab:** Assign to (dropdown of G4 roles) · Notify list (multi-select)
- **Evidence tab:** File upload (PDF, JPG — max 5 files, 10MB each)

### 6.3 Drawer: `approval-reject` (inline in approval queue)
- **Width:** 400px
- **Fields:** Reason (required, min 30 chars, 500 char limit with counter)
- **Buttons:** [Submit Rejection] + [Cancel]

---

## 7. Charts

### 7.1 Daily Fee Collection Trend (last 30 days)
- **Type:** Area line chart
- **Data:** Daily fee collected in ₹L (Lakhs)
- **X-axis:** Last 30 days (date labels every 5 days)
- **Y-axis:** Amount in ₹L
- **Tooltip:** Date · Amount: ₹X.XL · Branches reporting: N/50
- **Benchmark line:** Average daily target (horizontal dashed)
- **Export:** PNG

### 7.2 Branch Fee Performance Distribution
- **Type:** Horizontal bar chart
- **Data:** Branches sorted by collection % (ascending)
- **X-axis:** Collection % (0–120%)
- **Y-axis:** Branch names (top 10 + bottom 10 shown)
- **Colour:** Green >95% · Yellow 85–95% · Red <85%
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Branch deactivated | "Branch [Name] deactivated. MD and Chairman notified." | Warning | 6s |
| Branch activated | "Branch [Name] activated successfully" | Success | 4s |
| Approval approved | "Approval recorded and submitter notified" | Success | 4s |
| Approval rejected | "Rejection submitted with reason" | Success | 4s |
| Escalation created | "Escalation #[ID] created and assigned" | Success | 4s |
| Escalation assigned to VP | "Escalation assigned to VP. VP notified." | Info | 4s |
| Fee data stale | "Fee data hasn't refreshed in 2+ hours. Data may be outdated." | Warning | 6s |
| API error | "Failed to load branch data. Refresh the page." | Error | Manual |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No CEO approvals pending | "Nothing pending from you" | "All CEO-level approvals are up to date" | — |
| No escalations today | "No active escalations" | "All incidents from branches are resolved or assigned" | — |
| No branches found (search) | "No branches match" | "Try different search terms or clear filters" | [Clear Filters] |
| No branches active | "All branches inactive" | "All branches are currently deactivated" | [View Branch Overview] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 6 KPI cards + table rows (8) + chart placeholders |
| KPI auto-refresh | Shimmer on card values only |
| Branch table filter/search | Inline skeleton rows |
| Branch status change (confirm) | Full-page overlay "Updating branch status…" |
| Approval action | Spinner in button + button disabled |
| Chart data load | Spinner centred in chart area |

---

## 11. Role-Based UI Visibility

| Element | CEO G4 | President G4 | VP G4 | Trustee G1 |
|---|---|---|---|---|
| Page | ✅ | ❌ redirect | ❌ redirect | ❌ redirect |
| [Activate/Deactivate] in table | ✅ | ❌ | ❌ | ❌ |
| [Approve] / [Reject] in queue | ✅ | ❌ | ❌ | ❌ |
| [Handle Myself] on escalations | ✅ | ❌ | ❌ | ❌ |
| Fee cards (view) | ✅ | ❌ | ✅ (own widget only) | ❌ |
| Export | ✅ | ❌ | ❌ | ❌ |
| Quick Actions grid | ✅ | ❌ | ❌ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/ceo/dashboard/` | JWT (G4 CEO) | Full CEO dashboard data |
| GET | `/api/v1/group/{id}/ceo/kpi-cards/` | JWT (G4 CEO) | KPI refresh (auto-refresh) |
| GET | `/api/v1/group/{id}/branches/operations/` | JWT (G4) | Branch operations table data |
| GET | `/api/v1/group/{id}/fee/summary/today/` | JWT (G4) | Today's fee by type |
| GET | `/api/v1/group/{id}/approvals/?role=ceo` | JWT (G4 CEO) | CEO approval queue |
| POST | `/api/v1/group/{id}/approvals/{id}/approve/` | JWT (G4 CEO) | Approve |
| POST | `/api/v1/group/{id}/approvals/{id}/reject/` | JWT (G4 CEO) | Reject with reason |
| POST | `/api/v1/group/{id}/branches/{id}/activate/` | JWT (G4 CEO) | Activate/deactivate |
| GET | `/api/v1/group/{id}/escalations/?status=open` | JWT (G4) | Today's open escalations |
| POST | `/api/v1/group/{id}/escalations/` | JWT (G4 CEO) | Create escalation |
| POST | `/api/v1/group/{id}/escalations/{id}/assign/` | JWT (G4 CEO) | Assign to VP |
| GET | `/api/v1/group/{id}/fee/trend/?days=30` | JWT (G4) | 30-day daily fee trend |
| GET | `/api/v1/group/{id}/fee/branch-performance/` | JWT (G4) | Branch fee collection % |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Branch search | `input delay:300ms` | GET `.../branches/operations/?q=` | `#branch-ops-body` | `innerHTML` |
| Filter apply | `click` | GET `.../branches/operations/?filters=` | `#branch-ops-section` | `innerHTML` |
| KPI auto-refresh | `every 3m` | GET `.../ceo/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Pagination | `click` | GET `.../branches/operations/?page=` | `#branch-ops-section` | `innerHTML` |
| Approve button | `click` | POST `.../approvals/{id}/approve/` | `#approval-queue` | `innerHTML` |
| Open escalation drawer | `click` | GET `.../escalations/{id}/` | `#drawer-body` | `innerHTML` |
| Submit escalation form | `submit` | POST `.../escalations/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
