# [15] — Compliance Policy Repository

> **URL:** `/group/legal/policies/`
> **File:** `n-15-compliance-policy-repository.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Compliance Manager (Role 109, G1) — versioned compliance policies, branch acknowledgements, review schedules

---

## 1. Purpose

The Compliance Policy Repository maintains the authoritative, version-controlled collection of all compliance and regulatory policies that govern the Institution Group. These policies define how the group complies with its legal obligations: the Child Protection Policy (POCSO compliance), Anti-Ragging Policy (UGC regulations), Data Privacy Policy (DPDP Act), RTI Policy (RTI Act), Whistleblower Policy (corporate governance), Staff Code of Conduct, Grievance Redressal Policy, and Fee Regulation Policy (State Fee Regulation Committee).

Each policy has a version history — when laws change (e.g., DPDP Act 2023 replacing IT Act privacy provisions), the DPO or Compliance Manager updates the Data Privacy Policy, and the new version is pushed to all branches. Branches must acknowledge receipt of the updated policy within 30 days. The Group Compliance Manager tracks which branches have acknowledged which policy versions.

This page also manages the policy review schedule — each policy has a scheduled review date, ensuring policies stay current with changing regulations. The Compliance Manager receives alerts when a policy is due for review.

Scale: 10–25 active policy types · Versioned with full history · 5–50 branches × each policy = 50–1,250 acknowledgement records

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Drafts policy text externally |
| Group Compliance Manager | 109 | G1 | Full Read + Upload + Acknowledgement Tracking | Primary user |
| Group RTI Officer | 110 | G1 | Read — RTI Policy only | Views RTI policy for reference |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Not relevant |
| Group POCSO Reporting Officer | 112 | G1 | Read — Child Protection + POCSO Policies | |
| Group Data Privacy Officer | 113 | G1 | Read — Data Privacy Policy | |
| Group Contract Administrator | 127 | G3 | Upload — New policy versions (with Compliance Mgr approval) | Upload only; no independent publish |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Policies cited in disputes | |
| Group Insurance Coordinator | 129 | G1 | No Access | Not relevant |

> **Access enforcement:** `@require_role(roles=[109,110,112,113,127,128], min_level=G1)`. G4/G5 full read.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Compliance Policy Repository
```

### 3.2 Page Header
```
Compliance Policy Repository                    [Upload Policy Version]  [Export Index ↓]
Group Compliance Manager — [Name]
[Group Name] · [N] Active Policies · [N] Review Due
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Policy review overdue (past scheduled review date) | "[N] policy(ies) are past their scheduled review date. Update to maintain compliance." | High (amber) |
| Policy updated but not acknowledged by all branches within 30 days | "[N] branches have not acknowledged the updated [Policy Name] within the 30-day window." | Medium (yellow) |
| New legal requirement detected (DPDP, UGC notification) | "New regulatory update may require policy revision. Review [Policy Name]." | Info (blue) |

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Active Policies | Count | COUNT policies WHERE status = 'active' | Blue | `#kpi-total-policies` |
| 2 | Review Due (90 Days) | Count | COUNT WHERE review_due_date BETWEEN TODAY AND TODAY+90 | Amber > 3, Green ≤ 3 | `#kpi-review-due` |
| 3 | Review Overdue | Count | COUNT WHERE review_due_date < TODAY AND status = 'active' | Red > 0, Green = 0 | `#kpi-review-overdue` |
| 4 | Pending Acknowledgements | Count | COUNT ack_records WHERE status = 'pending' | Amber > 10, Green ≤ 10 | `#kpi-ack-pending` |
| 5 | Branches with Full Acknowledgement | Count | COUNT branches where all required policies acknowledged | Green if = total | `#kpi-full-ack` |
| 6 | Policies Updated (This FY) | Count | COUNT policy_versions WHERE created_fy = current | Blue | `#kpi-updated-fy` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/policies/kpis/"` with `hx-trigger="load"`.

---

## 5. Sections

### 5.1 Policy Library Table

**Search:** Policy name, category, version. Debounced 350ms.

**Filters:**
- Category: `All` · `Child Protection` · `Anti-Ragging` · `Data Privacy` · `RTI` · `Whistleblower` · `Staff Conduct` · `Grievance` · `Fee Regulation` · `Other`
- Status: `Active` · `Under Review` · `Archived`
- Review Status: `Current` · `Due Soon` · `Overdue`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Policy Name | Text | Yes | |
| Category | Badge | Yes | |
| Current Version | Text | Yes | e.g., "v3.2" |
| Effective Date | Date | Yes | Date current version became effective |
| Next Review Date | Date | Yes | Red if overdue, amber if < 90d |
| Branches Acknowledged | Fraction | Yes | e.g., "24/28 branches" — green if all, amber if < 100% |
| Status | Badge | Yes | Active / Under Review / Archived |
| Actions | Buttons | No | [View] · [Upload New Version] (Role 109, 127) |

**Default sort:** Next Review Date ASC (overdue first)
**Pagination:** Server-side · Default 25/page

---

### 5.2 Branch Acknowledgement Matrix

Pivot view: rows = branches, columns = active policies. Each cell = acknowledged ✅ / pending ⚠️ / not required N/A.

**Columns:** Branch name + one column per active policy (up to 15 policies shown; horizontal scroll for more).

---

## 6. Drawers & Modals

### 6.1 Drawer: `policy-detail` (720px)
- **Tabs:** Overview · Current Version · Version History · Acknowledgements · Notes
- **Overview:** Policy name, category, description, legal basis, custodian (role), review frequency, next review date
- **Current Version:** PDF viewer inline + [Download]; key changes summary from previous version
- **Version History:** All past versions — version label, effective date, uploaded by, [Download Previous]
- **Acknowledgements tab:** Table per branch — branch name, policy version sent, date sent, acknowledged (Yes/No), acknowledged by, date acknowledged. Export as Excel.
- **Notes tab:** Internal notes; editable by Role 109.

### 6.2 Modal: `upload-policy-version` (580px)
| Field | Type | Required |
|---|---|---|
| Policy | Select (existing) or new | Yes |
| Version Label | Text | Yes — e.g., "v4.0" |
| Effective Date | Date | Yes |
| Key Changes | Textarea | Yes — min 30 chars |
| Policy Document | File (PDF) | Yes — max 20MB |
| Acknowledgement Required | Toggle | Yes |
| Acknowledgement Deadline | Date | Conditional |
| Notify Branches Immediately | Toggle | No |

**Footer:** Cancel · Upload Version

---

## 7. Charts

### 7.1 Acknowledgement Completion by Branch — Horizontal Bar

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Policy Acknowledgement Completion by Branch" |
| Data | Per branch: % of required policies acknowledged |
| Colour | Green ≥ 90%, Amber 70–89%, Red < 70% |
| Tooltip | "[Branch]: [X]% of policies acknowledged" |
| API endpoint | `GET /api/v1/group/{id}/legal/policies/ack-completion/` |
| HTMX | `hx-get` on load → `hx-target="#chart-ack-completion"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Policy version uploaded | "Policy '[Name]' v[X] uploaded. Acknowledgement sent to [N] branches." | Success | 5s |
| Review overdue | "[Policy Name] is past its review date." | Warning | 5s |
| Acknowledgement received | "[Branch] acknowledged [Policy Name] v[X]." | Info | 3s |
| Export triggered | "Generating policy index export…" | Info | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No policies | `book-open` | "Policy Repository Empty" | "Upload your first compliance policy." | Upload Policy |
| All reviewed and acknowledged | `check-circle` | "All Policies Current and Acknowledged" | | — |
| Filter returns no results | `search` | "No Matching Policies" | | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 6 KPI + 8-row table |
| Acknowledgement matrix | Grid shimmer |
| Chart load | Grey canvas + spinner |
| Drawer open | Right-slide skeleton |
| File upload | Progress bar |

---

## 11. Role-Based UI Visibility

| Element | Compliance Mgr (109) | DPO (113) | POCSO Officer (112) | CEO/Chairman |
|---|---|---|---|---|
| Full policy library | Visible | Data Privacy policy only | Child Protection only | Full |
| Ack matrix | Visible | Not visible | Not visible | Visible |
| [Upload New Version] | Visible | Not visible | Not visible | Visible |
| Version history | Full access | Own policy only | Own policy only | Full |
| Ack tab in drawer | Full | Not visible | Not visible | Full |
| Chart | Visible | Not visible | Not visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/policies/` | G1+ (scoped) | Policy list |
| POST | `/api/v1/group/{id}/legal/policies/{pol_id}/version/` | Role 109, 127, G4+ | Upload new version |
| GET | `/api/v1/group/{id}/legal/policies/kpis/` | G1+ | KPIs |
| GET | `/api/v1/group/{id}/legal/policies/acknowledgements/` | Role 109, G4+ | Acknowledgement matrix data |
| GET | `/api/v1/group/{id}/legal/policies/ack-completion/` | Role 109, G4+ | Chart data |
| POST | `/api/v1/group/{id}/legal/policies/export-index/` | G1+ | Async export |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | KPI container | GET `.../policies/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Table load | Table body | GET `.../policies/` | `#policies-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search/filter | Input/chips | GET with params | `#policies-table-body` | `innerHTML` | Debounce 350ms |
| Open drawer | [View] | GET `.../policies/{pol_id}/` | `#right-drawer` | `innerHTML` | |
| Upload modal | [Upload New Version] | GET `/htmx/legal/policies/{pol_id}/version-form/` | `#modal-container` | `innerHTML` | |
| Ack matrix load | Matrix container | GET `.../policies/acknowledgements/` | `#ack-matrix` | `innerHTML` | `hx-trigger="load"` |
| Chart | Chart container | GET `.../ack-completion/` | `#chart-ack-completion` | `innerHTML` | `hx-trigger="load"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
