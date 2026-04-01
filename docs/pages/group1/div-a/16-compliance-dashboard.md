# div-a-16 — Compliance Dashboard

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Compliance frameworks | DPDPA 2023 (India) · ISO 27001 · SOC 2 Type II |
| Data subjects (students) | 2.4M–7.6M |
| Data retention policy | Student data: 7 years · Logs: 2 years · Audit: 5 years |
| DSAR requests (Data Subject Access Requests)/month | ~5–20 |
| Consent records | One per student per institution |
| Data residency | India-only (all servers in ap-south-1 Mumbai) |
| Compliance checks automated | 48 checks across 6 domains |
| Last audit | SOC 2 — Nov 2024 |

**Why this matters:** With 2.4M+ student records (minors included), DPDPA compliance is not optional — it is a legal obligation. A breach or non-compliance finding can trigger regulatory fines and institutional contract terminations. This page gives the exec team real-time compliance posture across all 48 automated checks.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Compliance Dashboard |
| Route | `/exec/compliance/` |
| Django view | `ComplianceDashboardView` |
| Template | `exec/compliance_dashboard.html` |
| Priority | P1 |
| Nav group | Compliance |
| Required role | `exec`, `superadmin`, `compliance` |
| 2FA required | Exporting compliance reports |
| HTMX poll | Compliance score: every 5 min |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Compliance Dashboard               [Export Report] [Run All Checks] │
├────────┬────────┬────────┬────────┬────────┬───────────────────────────────  ┤
│ Overall│ DPDPA  │ ISO    │ SOC 2  │ Open   │ Last Full                      │
│ Score  │ Score  │ 27001  │ Score  │ Findings│ Audit                         │
│ 94/100 │ 96/100 │ 91/100 │ 94/100 │   3    │ Nov 2024                      │
├────────┴────────┴────────┴────────┴────────┴───────────────────────────────  ┤
│ TABS: [Overview] [DPDPA] [Data Residency] [DSAR Requests] [Findings]        │
│       [Audit History]                                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: OVERVIEW                                                                │
│ Compliance checks grid (48 checks, status per check)                        │
│ Domain breakdown: Data Collection / Storage / Access / Retention / Breach   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Overall Score | 0–100 composite | < 80 = red |
| 2 | DPDPA Score | 0–100 | < 90 = amber |
| 3 | ISO 27001 Score | 0–100 | < 85 = amber |
| 4 | SOC 2 Score | 0–100 | < 90 = amber |
| 5 | Open Findings | Count of unresolved findings | > 5 = red |
| 6 | Last Full Audit | Date (relative) | > 12 months ago = amber |

---

### 4.2 Tab: Overview

`id="tab-overview"` · `hx-get="?part=compliance_overview"`

#### 4.2.1 Compliance Checks Grid

48 checks displayed as a grid of status tiles (6 columns × 8 rows).
Each tile: `bg-[#0D1526] rounded-lg p-3 text-xs` · border colour by status:
- Pass: `border-[#34D399]` · Fail: `border-[#EF4444]` · Warning: `border-[#F59E0B]` · N/A: `border-[#475569]`

Tile content: check name (2 lines max) + status dot + last checked time
**Click tile:** opens Check Detail Drawer (§5.1)

**Domain grouping:** checks grouped by domain with domain header row:
- Data Collection (8 checks)
- Data Storage (10 checks)
- Access Control (10 checks)
- Data Retention (8 checks)
- Breach Management (7 checks)
- Consent Management (5 checks)

#### 4.2.2 Domain Score Bars

`flex flex-col gap-3 p-4`
Each domain: label + progress bar + score `/100` + pass/fail/warning count chips

---

### 4.3 Tab: DPDPA

`id="tab-dpdpa"` · `hx-get="?part=dpdpa"`

**DPDPA 2023 compliance checklist** (India's Digital Personal Data Protection Act)

**Section breakdown table:**
| DPDPA Section | Requirement | Status | Evidence | Last Reviewed |
|---|---|---|---|---|
| §7 — Consent | Valid consent for all data processing | ✓ Pass | Consent records DB | Mar 2025 |
| §8 — Accuracy | Data accuracy obligations | ✓ Pass | Student data validation | Feb 2025 |
| §9 — Retention | Data not retained beyond necessity | ⚠ Warning | Retention policy gap | — |
| §11 — Erasure | Right to erasure (students) | ✓ Pass | DSAR process | Mar 2025 |
| §13 — Grievances | Grievance officer appointed | ✓ Pass | Appointed: Name | — |

**[+ Log Review]** for each row to record review evidence

---

### 4.4 Tab: Data Residency

`id="tab-residency"` · `hx-get="?part=residency"`

**Linked to div-a-19 for detail.** Shows summary view:
- All data in India: ✓ Confirmed
- Data centres: Mumbai (primary) + Chennai (DR)
- Last verified: date
- Cross-border data: None
- CDN: Cloudflare (India PoPs only for student data)

**Data flow diagram:** SVG diagram showing data flow: Institution → API Gateway → Application → Database (India) → Backup (India)

---

### 4.5 Tab: DSAR Requests

`id="tab-dsar"` · `hx-get="?part=dsar"`

**DSAR = Data Subject Access Requests** (students requesting their data)

**Summary cards:**
- Open DSARs · Overdue (> 30 days) · Completed (30d) · Avg resolution time

**DSAR Table:**
| Column | Detail |
|---|---|
| Request ID | DSAR-XXXX |
| Requested by | Student name (anonymised in display) |
| Institution | Name |
| Type | Access / Erasure / Correction / Portability |
| Submitted | Date |
| Due Date | 30 days from submission (DPDPA requirement) |
| Status | Open / In Progress / Completed / Rejected |
| Assigned to | Ops team member |
| Actions ⋯ | View / Process / Close |

**[+ New DSAR]** button (for manual entry of written/offline requests)

**Overdue DSAR rows:** red tint `bg-[#1A0A0A]`

---

### 4.6 Tab: Findings

`id="tab-findings"` · `hx-get="?part=findings"`

**Purpose:** Compliance findings from automated checks or audits. Track remediation.

| Column | Detail |
|---|---|
| Finding ID | FIND-XXXX |
| Title | Short description |
| Severity | Critical / High / Medium / Low |
| Framework | DPDPA / ISO 27001 / SOC 2 / Internal |
| Opened | Date |
| Due Date | Remediation target |
| Owner | Assigned person |
| Status | Open / In Remediation / Resolved / Accepted Risk |
| Actions ⋯ | View / Update / Close |

**[+ Log Finding]** button

**Finding Detail Drawer (560px):** Description · Root cause · Remediation steps · Evidence · Status history

---

### 4.7 Tab: Audit History

`id="tab-audits"` · `hx-get="?part=audits"`

| Column | Detail |
|---|---|
| Audit ID | AUDIT-XXXX |
| Type | SOC 2 / ISO 27001 / DPDPA / Internal |
| Auditor | Name / Firm |
| Period | e.g., "Jan–Dec 2024" |
| Report date | Date |
| Result | Clean / Qualified / Adverse |
| Findings | Count |
| [View Report] | Opens PDF or drawer |

---

## 5. Drawers

### 5.1 Compliance Check Drawer (480 px)

**Header:** Check name · Status badge · Framework · `[×]`

**Content:**
- Description (what this check validates)
- Current status: Pass / Fail / Warning
- Last run: timestamp
- Check logic: code reference or description
- Evidence: linked records or screenshots
- If failing: remediation guidance
- History: last 10 check results with timestamps

**Footer:** [Run Check Now] [Add Evidence] [Close]

---

## 6. Modals

### 6.1 Run All Checks Modal (480 px)

"Run all 48 compliance checks?"
"This will take approximately 2–3 minutes. Results will update in real-time."
**Footer:** [Cancel] [Run All Checks]

**Progress display (after confirm):** inline progress bar `hx-get="?part=check_progress"` `hx-trigger="every 5s"` updates until complete

---

### 6.2 Export Compliance Report Modal (480 px)

**2FA required.**
| Field | Type |
|---|---|
| Report type | DPDPA / ISO 27001 / SOC 2 / Full |
| Period | Date range |
| Format | PDF / XLSX |
| Recipient email | Optional |

**Footer:** [Cancel] [Generate Report]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/compliance_kpi.html` | Page load · poll 5 min |
| `?part=compliance_overview` | `exec/partials/compliance_overview.html` | Tab click |
| `?part=dpdpa` | `exec/partials/compliance_dpdpa.html` | Tab click |
| `?part=residency` | `exec/partials/compliance_residency.html` | Tab click |
| `?part=dsar` | `exec/partials/compliance_dsar.html` | Tab click |
| `?part=findings` | `exec/partials/compliance_findings.html` | Tab click |
| `?part=audits` | `exec/partials/compliance_audits.html` | Tab click |
| `?part=check_drawer&id={id}` | `exec/partials/check_drawer.html` | Tile click |
| `?part=check_progress` | `exec/partials/check_progress.html` | Poll during run |

**Django view dispatch:**
```python
class ComplianceDashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_compliance"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/compliance_kpi.html",
                "compliance_overview": "exec/partials/compliance_overview.html",
                "dpdpa": "exec/partials/compliance_dpdpa.html",
                "residency": "exec/partials/compliance_residency.html",
                "dsar": "exec/partials/compliance_dsar.html",
                "findings": "exec/partials/compliance_findings.html",
                "audits": "exec/partials/compliance_audits.html",
                "check_drawer": "exec/partials/check_drawer.html",
                "check_progress": "exec/partials/check_progress.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/compliance_dashboard.html", ctx)
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 300 ms | > 800 ms |
| Overview checks grid (48 tiles) | < 400 ms | > 1 s |
| DSAR table | < 400 ms | > 1 s |
| Check drawer | < 250 ms | > 700 ms |
| Run all checks (background) | < 3 min | > 5 min |
| Full page initial load | < 1 s | > 2.5 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Critical failing check | Overall score drops · red banner "Critical compliance failure: {check name}" |
| DSAR overdue (> 30 days) | Red row + alert sent to compliance officer |
| All checks passing | Green "All compliance checks passed" success banner |
| Audit report expired (> 12 months) | Amber banner "SOC 2 audit due — last: Nov 2024" |
| Run all checks: check fails during run | Live progress shows red for that check; others continue |
| Finding with "Accepted Risk" status | Requires compliance officer sign-off + reason + review date |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`6` | Switch tabs |
| `R` | Run all checks |
| `E` | Export report |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/compliance_dashboard.html` | Full page shell |
| `exec/partials/compliance_kpi.html` | KPI strip |
| `exec/partials/compliance_overview.html` | Overview checks grid |
| `exec/partials/compliance_dpdpa.html` | DPDPA tab |
| `exec/partials/compliance_residency.html` | Data residency summary |
| `exec/partials/compliance_dsar.html` | DSAR requests table |
| `exec/partials/compliance_findings.html` | Findings table |
| `exec/partials/compliance_audits.html` | Audit history |
| `exec/partials/check_drawer.html` | Check detail drawer |
| `exec/partials/check_progress.html` | Run checks progress |
| `exec/partials/run_checks_modal.html` | Run all modal |
| `exec/partials/export_compliance_modal.html` | Export modal |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `TabBar` | §4.2–4.7 |
| `ComplianceCheckTile` | §4.2.1 |
| `DomainScoreBar` | §4.2.2 |
| `DPDPAChecklist` | §4.3 |
| `DataFlowDiagram` | §4.4 |
| `DSARTable` | §4.5 |
| `FindingsTable` | §4.6 |
| `AuditHistoryTable` | §4.7 |
| `DrawerPanel` | §5.1 |
| `ModalDialog` | §6.1–6.2 |
| `ProgressBar` | §6.1 run progress |
| `PaginationStrip` | Tables |
| `PollableContainer` | KPI · check progress |
