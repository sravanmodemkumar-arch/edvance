# G-01 — BGV Dashboard

> **Route:** `/bgv/`
> **Division:** G — Background Verification
> **Primary Role:** BGV Manager (39) — command centre view; BGV Ops Supervisor (92) — operational overview
> **Supporting Roles:** POCSO Compliance Officer (41) — compliance tiles only; Platform Admin (10) — full
> **File:** `g-01-bgv-dashboard.md`
> **Priority:** P0 — primary entry point; shows compliance health at a glance

---

## 1. Page Name & Route

**Page Name:** BGV Dashboard
**Route:** `/bgv/`
**Part-load routes:**
- `/bgv/?part=kpi-tiles` — KPI summary tiles
- `/bgv/?part=compliance-trend` — trend chart
- `/bgv/?part=institution-snapshot` — institution compliance table
- `/bgv/?part=pending-actions` — action queue

---

## 2. Purpose

G-01 is the command centre for the BGV division. It gives the BGV Manager and Supervisor an immediate read on overall compliance health across all 1,900+ institutions, surfaces institutions requiring attention, and flags open POCSO cases that need urgent action.

**Who needs this page:**
- BGV Manager (39) — daily status check; escalation decisions
- BGV Ops Supervisor (92) — queue load visibility; SLA breach monitoring
- POCSO Compliance Officer (41) — compliance coverage read-only tiles

**When is it used:**
- Start of each working day — overall health check
- After new institution onboarding — check coverage has started
- After vendor turnaround batch — how many COMPLETEd overnight
- Before regulatory audit — compliance coverage snapshot

---

## 3. Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  POCSO ALERT BANNER (if open POCSO cases > 0) — full-width red  │
├─────────────────────────────────────────────────────────────────┤
│  Page header: "BGV Dashboard"   [Export Snapshot PDF]           │
├──────────┬──────────┬──────────┬──────────┬─────────┬──────────┤
│ Total    │Compliant │ At Risk  │Non-Comp. │ POCSO   │ Overdue  │
│ Inst.    │(100%)    │(<100%)   │(<80%)    │ Open    │ SLA      │
│  KPI     │  KPI     │  KPI     │  KPI     │  KPI    │  KPI     │
├──────────┴──────────┴──────────┴──────────┴─────────┴──────────┤
│  Compliance Trend Chart (30-day, line chart)                    │
├───────────────────────────────┬─────────────────────────────────┤
│  Institution Compliance Table │  Pending Actions Queue          │
│  (top non-compliant, paginated│  (overdue docs, vendor late,    │
│   server-side)                │   flagged awaiting approval)    │
└───────────────────────────────┴─────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — POCSO Alert Banner

Shown only when `bgv_pocso_case.action_status IN ('OPEN', 'UNDER_REVIEW')` count > 0.

**Banner content:** `⚠️ {N} POCSO case(s) require attention. [Review POCSO Cases →]`

- Red background, full-width, sticky below top nav
- Links to G-06 POCSO Case Management
- Dismissible per session — reappears on next page load if cases still open
- Critical: this is never hidden by default. POCSO Compliance Officer (41) sees this even though they have limited dashboard access.

---

### Section B — KPI Tiles

Six tiles. Each is clickable — click navigates to relevant filtered view.

| Tile | Value | Click Destination | Colour Rule |
|---|---|---|---|
| Total Institutions | Count of all institutions with ≥1 staff requiring BGV | G-04 Institutions list | Neutral |
| Compliant | Count where `compliance_status = COMPLIANT` | G-04 filtered: COMPLIANT | Green |
| At Risk | Count where `compliance_status = AT_RISK` | G-04 filtered: AT_RISK | Amber |
| Non-Compliant | Count where `compliance_status = NON_COMPLIANT` | G-04 filtered: NON_COMPLIANT | Red |
| POCSO Cases Open | Count where `action_status IN (OPEN, UNDER_REVIEW)` | G-06 POCSO queue | Red if > 0, else grey |
| Overdue SLA | Count of `bgv_verification` where `sla_due_at < now()` and `final_result = PENDING` | G-02 queue filtered: SLA_BREACHED | Red if > 0, else grey |

Secondary row (smaller tiles):
- **Verifications in Progress** — `bgv_verification.final_result = PENDING` count
- **Cleared This Month** — verifications completed CLEAR in current calendar month
- **Renewals Due (30 days)** — staff with `expiry_date ≤ today + 30`
- **Documents Pending** — verifications at status `DOCUMENTS_REQUESTED` for > 5 days

All tiles refresh on page load. HTMX auto-refresh every 5 minutes.

---

### Section C — Compliance Trend Chart

Line chart showing platform-wide BGV compliance coverage % over the past 30 days.

**Chart spec:**
- X-axis: Date (30 days, daily data points)
- Y-axis: Coverage % (0–100)
- Line 1: Platform-wide `bgv_complete_clear / total_staff_with_minor_access × 100`
- Line 2 (dashed): 100% compliance target line
- Hover tooltip: exact % and date
- Chart library: Chart.js (consistent with rest of platform)
- Data source: daily snapshot stored by Celery `snapshot_bgv_compliance_trend` (runs at 23:30 IST)
- Colour: green when ≥ 95%, amber 80–95%, red < 80%

**Filters above chart:**
- Institution type: All | Schools | Colleges | Coaching
- Date range: Last 30 / 60 / 90 days

Breakdowns by institution type shown as separate lines when filter is set.

---

### Section D — Institution Compliance Table

Top 20 non-compliant/at-risk institutions sorted by urgency.

**Default sort:** `compliance_status` (NON_COMPLIANT first, then AT_RISK) then `coverage_pct` ascending (lowest coverage at top).

| Column | Sortable | Notes |
|---|---|---|
| Institution Name | Yes | — |
| Type | Yes | SCHOOL / COLLEGE / COACHING |
| Total Staff | Yes | `total_staff_with_minor_access` |
| Verified | No | `bgv_complete_clear` count |
| Coverage % | Yes | Progress bar + % value |
| Status | No | Pill badge: COMPLIANT (green) / AT_RISK (amber) / NON_COMPLIANT (red) / ESCALATED (purple) |
| Expired BGV | No | Count of staff with `bgv_status = EXPIRED` |
| Last Activity | No | `max(bgv_verification.updated_at)` for this institution |
| Action | No | [View →] links to G-04 institution detail |

**Inline action per row (BGV Manager only):** [Escalate] — marks institution as ESCALATED; prompts for escalation note.

**Table filters:**
- Status: All / COMPLIANT / AT_RISK / NON_COMPLIANT / ESCALATED
- Institution type: All / Schools / Colleges / Coaching
- Search: institution name

Pagination: 20 rows. [View All Institutions →] links to full G-04 page.

---

### Section E — Pending Actions Queue

Right-side panel. Shows items requiring BGV Manager or Supervisor attention.

**Action categories (tabs):**

| Tab | Description | Badge count |
|---|---|---|
| Awaiting Approval | FLAGGED verifications awaiting Supervisor (92) approval | Count |
| SLA Breached | Verifications where `sla_due_at < now()` | Count |
| Documents Stale | Verifications at DOCUMENTS_REQUESTED for > 5 days (configurable) | Count |
| Vendor Overdue | Sent to vendor but `vendor_returned_at` is NULL and `vendor_sent_at + sla_hours` < now() | Count |

**Per row:**
- Staff ref (anonymised)
- Institution name
- Verification type (INITIAL / RENEWAL)
- Days overdue or waiting
- [View →] → G-03 Staff Record

Sorted by urgency: SLA breach days (most overdue first).

---

## 5. Data Model Reference

Reads from:
- `bgv_institution_compliance` — compliance aggregate per institution
- `bgv_verification` — pending/active verifications
- `bgv_pocso_case` — open POCSO cases
- `bgv_staff` — staff counts

All reads are from Memcached (TTL: 5 min) backed by the above tables. BGV Manager can force-refresh with `?nocache=true`.

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | BGV Manager (39), BGV Ops Supervisor (92), POCSO Compliance Officer (41), Platform Admin (10) |
| Full dashboard | BGV Manager (39), BGV Ops Supervisor (92), Platform Admin (10) |
| POCSO Compliance Officer (41) | Sees: POCSO alert banner + compliance KPI tiles (covered %, POCSO open, non-compliant count) + trend chart. Does NOT see institution names or pending actions queue. |
| [Export Snapshot PDF] | BGV Manager (39), Platform Admin (10) |
| [Escalate] inline action | BGV Manager (39), Platform Admin (10) only |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| No institutions onboarded yet | KPI tiles show 0. Trend chart shows flat 0% line. Table empty state: "No institutions have BGV data yet. BGV requests start when institutions onboard staff." |
| All institutions COMPLIANT | Non-compliant/at-risk tiles show 0 in green. Pending actions queue shows empty state per tab. Compliance trend chart shows 100% flat line. |
| Chart data missing for some days (Celery job failed) | Missing data points shown as gaps (not interpolated). Tooltip on gap: "Data unavailable for this date." |
| POCSO case auto-resolved | Banner disappears on next page load. No retrospective hiding. |
| BGV Ops Supervisor (92) login | Does not see [Export Snapshot PDF]. Does not see [Escalate] inline action. Sees full dashboard otherwise. |

---

## 8. UI Patterns

### Loading States
- KPI tiles: 6-tile skeleton shimmer
- Trend chart: chart area shimmer with axes placeholder
- Institution table: 8-row shimmer
- Pending actions: 5-row shimmer per tab

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Two-column layout (table + queue side by side) |
| Tablet | Single column; queue moves below table |
| Mobile | KPI tiles stack 2×3; chart collapses to 60-day simplified version; table shows Name + Coverage % + Status only (tap to expand row) |

### Toasts
| Action | Toast |
|---|---|
| Export PDF triggered | ✅ "Snapshot PDF generating — download will start shortly" (4s) |
| Escalation saved | ✅ "Institution escalated. Customer Success notified." (4s) |

---

*Page spec complete.*
*G-01 covers: POCSO alert banner → compliance KPI tiles (6 primary + 4 secondary) → 30-day compliance trend chart (by institution type) → top non-compliant institution table with inline escalation → pending actions queue (awaiting approval / SLA breached / documents stale / vendor overdue).*
