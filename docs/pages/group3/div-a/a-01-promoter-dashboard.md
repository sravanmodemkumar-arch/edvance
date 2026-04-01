# A-01 — Promoter / Correspondent Dashboard

> **URL:** `/school/admin/promoter/`
> **File:** `a-01-promoter-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** School Promoter / Correspondent (S7) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the School Promoter, Correspondent, or Trustee — the financial and governance authority above the Principal. The Promoter typically checks this once or twice a day, not continuously. The dashboard answers three questions immediately: Is the school collecting fees on time? Is the school filling seats for the next year? Is there anything that could cause legal/compliance trouble?

**Indian context:** In privately managed Indian schools — under Society, Trust, or Section 8 Company structures — the Correspondent (as CBSE calls this role) or Trustee Representative has ultimate financial authority. They approve fee structures before the academic year, sanction capital expenditures, and are legally named in CBSE/state board affiliation documents. The Principal operates within the framework the Correspondent approves. This dashboard gives the Correspondent just enough operational visibility to make governance decisions, without exposing the full operational complexity that the Principal manages.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| School Promoter / Correspondent | S7 | Full — all sections, all actions |
| Principal | S6 | — (has own dashboard `/school/admin/principal/`) |
| VP Academic | S5 | — |
| VP Administration | S5 | — |
| Administrative Officer | S3 | — |

> **Access enforcement:** Django `@require_role_min('promoter')` decorator. Any other role hitting this URL → redirected to their own dashboard URL.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
[School Name]  ›  Promoter Dashboard
```

### 3.2 Page Header
```
Good morning, [Promoter Name]                           [Download Monthly Report ↓]  [⚙]
[School Full Name] · [Board Badge: CBSE/ICSE/State]    Academic Year: [2025–26 ▼]
```

- School logo + board affiliation badge (CBSE = blue, ICSE = maroon, State Board = amber)
- Academic year selector persists across all pages in the session

### 3.3 Critical Alert Banner (conditional)

Shown only when high-priority alerts exist. Red for CRITICAL, amber for WARNING.

```
🔴  CRITICAL: CBSE Affiliation renewal document expires in 18 days. Action required.  [View →]
⚠️  WARNING:  Fee collection rate dropped to 71% this month (target: 90%).             [View →]
```

Alert triggers:
- CBSE/state board affiliation expiry < 30 days
- Fee collection rate < 75% for current month
- RTE non-compliance — 25% EWS seats not filled
- POCSO Severity 1 incident open for >24 hours
- Any approval pending Promoter signature for >7 days
- Staff salary disbursement overdue by >5 days

---

## 4. KPI Summary Strip (6 cards)

> HTMX auto-refresh: every 5 minutes via `hx-trigger="every 5m"` on `#promoter-kpi-strip`

| # | Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|---|
| 1 | Fee Collection | `₹42.3L / ₹54L` this month + `78.3%` rate | Green ≥90% · Amber 75–89% · Red <75% | → A-20 Fee Dashboard |
| 2 | Annual Fee Dues | `₹12.1L` outstanding (this academic year) | Green <5% total dues · Amber 5–15% · Red >15% | → div-e Defaulters |
| 3 | Seat Fill (Admissions) | `634 / 800 seats` = `79.3%` + trend vs last year | Green ≥85% · Amber 70–84% · Red <70% | → A-14 Admission Pipeline |
| 4 | Pending Approvals | `3` requiring Promoter signature | Always shows count; badge pulses if >0 | → A-23 Approval Hub |
| 5 | Total Staff | `82 active` · `4 vacancies` · `BGV: 94%` | Red badge if BGV < 98% (POCSO risk) | → A-16 Staff Directory |
| 6 | Compliance | `3 items` requiring attention | Green = all compliant · Red = any critical | → A-29 Compliance Dashboard |

---

## 5. Main Sections

### 5.1 Fee & Finance (primary section — full width initially, collapsible)

**Sub-sections in a 2-col layout:**

**Left: Monthly Fee Collection Trend (chart)**
- Bar chart — last 12 months
- X-axis: Month (Apr–Mar)
- Y-axis: ₹ collected
- Bar colour: Green = met target · Red = missed target
- Target line overlay (dashed)
- Tooltip: "Apr 2025 — ₹48.2L collected (96.4% of ₹50L target)"
- Chart.js 4.x, responsive

**Right: Collection by Fee Type (current month)**
- Table:
  - Tuition Fee: ₹32.4L / ₹38L (85.3%)
  - Exam Fee: ₹4.1L / ₹4.5L (91.1%)
  - Transport Fee: ₹3.2L / ₹4L (80.0%)
  - Hostel Fee: ₹2.6L / ₹3.5L (74.3%)
  - Misc / Other: ₹0.8L / ₹4L (20.0%) — red flag
- [View Fee Dashboard →] link

**Below the 2-col: Top 5 Defaulter Classes** (students with fee dues > 60 days)
- Table: Class · Section · Student Count · Total Outstanding · Days Overdue
- [View All Defaulters →] link

---

### 5.2 Admissions & Seat Fill

**2-col layout:**

**Left: Admission Funnel (current admission season)**
- Funnel chart (top to bottom):
  - Enquiries: 1,240
  - Applications: 680
  - Interviews/Test: 420
  - Offers: 380
  - Confirmed: 312
  - Reported: 287
- Conversion rate at each step
- Comparison: "Last year same period: 334 confirmed"

**Right: Class-wise Seat Fill**
- Table: Class · Total Seats · Filled · % Fill · Status
- Colour code rows: ≥90% green · 70–89% amber · <70% red
- [View Admission Pipeline →] link

---

### 5.3 Pending Approvals (Promoter's items only)

**Table:**
| # | Item | Requested By | Date | Amount (if financial) | Action |
|---|---|---|---|---|---|
| 1 | Fee Structure Revision — 2026-27 | Principal | 20 Mar 2026 | ₹8,400/student avg increase | [Review & Approve] |
| 2 | New AC Purchase — VP Admin | VP Admin | 22 Mar 2026 | ₹1.8L | [Review & Approve] |
| 3 | Staff Salary Revision — Sr. Staff | Principal | 24 Mar 2026 | ₹2.3L/month additional | [Review & Approve] |

**Clicking [Review & Approve]:** Opens `approval-action` drawer with full details, budget impact, and approve/reject/return buttons.

---

### 5.4 Compliance Snapshot

**Card grid (3 cards per row):**

| Item | Status | Last Checked | Action |
|---|---|---|---|
| CBSE Affiliation | ⚠️ Expires in 18 days | 2026-02-01 | [Renew Documents] |
| RTE 25% Compliance | ✅ 27% EWS seats | 2026-03-15 | [View Details] |
| POCSO Training | ⚠️ 91% trained (target: 100%) | 2026-03-10 | [View Staff] |
| Fire NOC (Municipal) | ✅ Valid till Dec 2026 | 2025-12-01 | — |
| DPDPA Data Register | ✅ Updated | 2026-03-20 | — |
| Annual Returns (State Board) | ✅ Filed | 2026-02-28 | — |

[View Full Compliance Dashboard →] link

---

### 5.5 Academic Performance Snapshot (read-only)

- Last exam result summary: Class X/XII board results, pass percentage, merit count
- Attendance rate last month: Students X% · Staff Y%
- "No edit rights on this section — contact Principal for details"

---

## 6. Drawers

### `approval-action`
Triggered from Pending Approvals section.

- **Tabs:** Details · Budget Impact · History · Action
- **Details tab:** Full description of what is being requested, supporting documents
- **Budget Impact tab:** Current budget vs proposed; surplus/deficit after approval
- **History tab:** Prior similar approvals (last 3 years)
- **Action tab:**
  - [✅ Approve] — records Promoter approval with TOTP 2FA confirmation for financial items > ₹1L
  - [↩ Return for Revision] — text field for reason, sends back to requester
  - [❌ Reject] — reason field, notifies Principal

### `compliance-detail`
Triggered from Compliance Snapshot items.

- Status, regulation reference, evidence uploaded, renewal deadline
- Document upload slot for evidence
- [Mark as Resolved] button

---

## 7. Charts

### 7.1 Monthly Fee Collection Trend (Section 5.1)
- Type: Bar (grouped: collected vs target)
- Library: Chart.js 4.x
- Data: 12 months rolling
- API: `GET /api/v1/school/{id}/finance/fee-trend/?months=12`

### 7.2 Admission Funnel (Section 5.2)
- Type: Funnel (Chart.js horizontal bar, top-down)
- Data: current admission season stages
- API: `GET /api/v1/school/{id}/admissions/funnel/`

---

## 8. Toast Notifications

| Trigger | Type | Message |
|---|---|---|
| Approval submitted | Success | "Approved. Principal has been notified." |
| Approval returned | Info | "Returned to Principal with your comments." |
| Approval rejected | Warning | "Rejected. Principal notified of reason." |
| TOTP required | Info | "Please enter your authenticator code to approve this financial action." |
| Report download ready | Success | "Monthly report downloaded." |

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/promoter/dashboard/` | Full dashboard data load |
| 2 | `GET` | `/api/v1/school/{id}/promoter/kpi-strip/` | KPI cards data (HTMX refresh) |
| 3 | `GET` | `/api/v1/school/{id}/finance/fee-trend/?months=12` | Monthly fee trend chart data |
| 4 | `GET` | `/api/v1/school/{id}/finance/collection-by-type/` | Current month fee type breakdown |
| 5 | `GET` | `/api/v1/school/{id}/finance/top-defaulters/?days=60` | Top defaulter classes/students |
| 6 | `GET` | `/api/v1/school/{id}/admissions/funnel/` | Admission funnel data |
| 7 | `GET` | `/api/v1/school/{id}/admissions/seat-fill/` | Class-wise seat fill table |
| 8 | `GET` | `/api/v1/school/{id}/approvals/?role=promoter&status=pending` | Pending approvals for Promoter |
| 9 | `POST` | `/api/v1/school/{id}/approvals/{approval_id}/decide/` | Approve/return/reject action |
| 10 | `GET` | `/api/v1/school/{id}/compliance/snapshot/` | Compliance status cards |
| 11 | `GET` | `/api/v1/school/{id}/academic/performance-snapshot/` | Last exam result summary |
| 12 | `GET` | `/api/v1/school/{id}/promoter/alerts/` | Critical alert banner items |

---

## 10. HTMX Patterns

### 10.1 KPI Strip Auto-Refresh
```html
<div id="promoter-kpi-strip"
     hx-get="/api/v1/school/{{ school_id }}/promoter/kpi-strip/"
     hx-trigger="every 5m"
     hx-target="#promoter-kpi-strip"
     hx-swap="outerHTML">
  <!-- 6 KPI cards rendered here -->
</div>
```

### 10.2 Approval Action (HTMX form)
```html
<form hx-post="/api/v1/school/{{ school_id }}/approvals/{{ approval_id }}/decide/"
      hx-target="#approval-row-{{ approval_id }}"
      hx-swap="outerHTML"
      hx-confirm="Approve this request? This action is logged and cannot be undone.">
  <input type="hidden" name="decision" value="APPROVED">
  <input type="text" name="totp_code" placeholder="2FA code" required>
  <button type="submit" class="btn-primary">Approve</button>
</form>
```

### 10.3 Alert Banner Dismiss
```html
<button hx-post="/api/v1/school/{{ school_id }}/promoter/alerts/{{ alert_id }}/dismiss/"
        hx-target="#alert-{{ alert_id }}"
        hx-swap="outerHTML">
  Dismiss
</button>
```

---

## 11. Security

- **TOTP enforcement:** All financial approvals > ₹50,000 require TOTP 2FA (configured in school settings; can be set to any threshold)
- **Session:** Promoter sessions timeout after 30 minutes of inactivity (configurable by Platform Admin)
- **Audit:** Every approval/rejection logged in `school_audit_log` with actor, IP, decision, and timestamp — immutable
- **Data access:** Promoter can only see their own institution's data; multi-institution Promoters (e.g., Trustee for 3 schools) have an institution picker in the top bar
- **Read-only enforcement:** Academic operations sections are server-side rendered without any edit controls for Promoter role

---

## 12. Performance

| Concern | Approach |
|---|---|
| Dashboard load | Computed KPIs cached in Memcached per school per day; stale if fee/admission events happen after cache; 5-minute TTL |
| Fee trend chart | Aggregated query runs at midnight; result cached; HTMX refresh every 5 min serves cached data |
| Approval list | Direct DB query (no cache) — must be real-time; paginated to 10 items |
| Alert banner | Checked on every load; lightweight query on `compliance_status` and `approval_queue` |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
