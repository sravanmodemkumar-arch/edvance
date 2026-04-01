# G-07 — Compliance Reports

> **Route:** `/bgv/reports/`
> **Division:** G — Background Verification
> **Primary Role:** POCSO Compliance Officer (41) — NCPCR reports; BGV Manager (39) — all reports
> **Supporting Roles:** POCSO Reporting Officer (78) — full; DPO (76) — read; Legal Officer (75) — read; Platform Admin (10) — full
> **File:** `g-07-compliance-reports.md`
> **Priority:** P1 — regulatory and audit reporting

---

## 1. Page Name & Route

**Page Name:** Compliance Reports
**Route:** `/bgv/reports/`
**Part-load routes:**
- `/bgv/reports/?part=coverage-report` — coverage report tab
- `/bgv/reports/?part=ncpcr-report` — NCPCR report tab
- `/bgv/reports/?part=vendor-performance` — vendor performance tab
- `/bgv/reports/?part=renewal-pipeline` — renewal pipeline tab

---

## 2. Purpose

G-07 is the reporting hub for Division G. It produces the four primary reports needed for internal operations and regulatory compliance: BGV coverage by institution, NCPCR mandatory annual report, vendor SLA performance, and renewal pipeline forecasting.

**Who needs this page:**
- BGV Manager (39) — internal operations review; board-level compliance reporting
- POCSO Compliance Officer (41) / POCSO Reporting Officer (78) — NCPCR mandatory annual report
- DPO (76) — privacy compliance audit (verifying data handling in BGV process)
- Legal Officer (75) — for legal review and regulatory submissions

---

## 3. Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Page header: "Compliance Reports"                               │
├──────────────────────────────────────────────────────────────────┤
│  Tabs: Coverage Report | NCPCR Report | Vendor Performance |     │
│        Renewal Pipeline                                          │
├──────────────────────────────────────────────────────────────────┤
│  Tab content area + Export controls                              │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Tab-Wise Detailed Breakdown

---

### Tab 1 — Coverage Report

BGV coverage status across all institutions, by institution type, and over time.

#### Section A — Report Filters

| Filter | Control | Default |
|---|---|---|
| As of Date | Date picker | Today |
| Institution Type | Multiselect | All |
| State / Region | Multiselect | All |
| Compliance Status | Multiselect | All |
| Include Deactivated Institutions | Toggle | OFF |

**[Generate Report]** — computes report from database (not cache). Shows spinner with "Generating…". Large reports may take 5–10s.

#### Section B — Platform Coverage Summary

| Metric | Value |
|---|---|
| Total institutions with BGV requirements | Count |
| Compliant institutions (100% coverage) | Count + % |
| At-Risk institutions | Count + % |
| Non-Compliant institutions | Count + % |
| Total staff requiring BGV | Sum across all institutions |
| Total verifications CLEAR | Count |
| Total verifications in progress | Count |
| Platform-wide coverage % | Weighted average |
| Verifications expiring next 30 days | Count |
| Verifications expiring next 90 days | Count |

#### Section C — By Institution Type Breakdown

| Institution Type | Total Staff | Verified | In Progress | Coverage % | Compliant |
|---|---|---|---|---|---|
| Schools | — | — | — | — | N / Total |
| Colleges | — | — | — | — | N / Total |
| Coaching Centres | — | — | — | — | N / Total |
| **Total** | — | — | — | — | — |

#### Section D — Institution-Level Table

Full table of all institutions with their metrics.

Same columns as G-04 institution table. Sorted by coverage % ascending.

Pagination: 50 rows. Full data included in export.

#### Section E — Export Controls

| Export | Format | Notes |
|---|---|---|
| [Export Coverage Report CSV] | CSV | All institutions, all metrics, as of selected date |
| [Export Coverage Report PDF] | PDF | Formatted: summary + by-type breakdown + institution table. Includes EduForge letterhead + report date. |
| [Export Non-Compliant Institutions CSV] | CSV | Only NON_COMPLIANT and AT_RISK institutions |

**Access:** BGV Manager (39), POCSO Compliance Officer (41), POCSO Reporting Officer (78), DPO (76), Legal Officer (75), Platform Admin (10).

---

### Tab 2 — NCPCR Report

Mandatory annual report for submission to NCPCR (National Commission for Protection of Child Rights).

**Legal context:** EduForge must submit an annual BGV compliance report to NCPCR covering: total staff with minor access, verification status, POCSO cases identified, actions taken.

#### Section A — Report Period

| Field | Control | Notes |
|---|---|---|
| Financial Year | Select: FY 2024–25 / FY 2025–26 / etc. | Generates report for April 1 – March 31 |
| Custom Date Range | Date range picker | For ad-hoc submissions |

**[Generate NCPCR Report]** — compiles data for selected period.

#### Section B — NCPCR Report Sections

**Part 1 — Platform Overview:**
| Field | Value |
|---|---|
| Platform Name | EduForge |
| Platform Type | EdTech — Schools, Colleges, Coaching Centres |
| Reporting Period | {FY or date range} |
| Total Institutions on Platform | Count |
| Total Students (approximate) | From roles file scale context |
| Report Generated By | POCSO Officer / Reporting Officer name |
| Report Generated At | Datetime |

**Part 2 — Staff Verification Summary:**
| Metric | Count |
|---|---|
| Total staff with minor access (across all institutions) | — |
| BGV initiated during period | — |
| BGV completed CLEAR during period | — |
| BGV completed FLAGGED (non-POCSO) during period | — |
| BGV INCONCLUSIVE during period | — |
| BGV expired (not renewed) during period | — |
| BGV not yet initiated | — |
| Platform-wide coverage % at end of period | — |

**Part 3 — POCSO Cases:**
| Metric | Value |
|---|---|
| Total POCSO cases identified during period | Count |
| Cases from BGV vendor results | Count |
| Cases from manual flags | Count |
| Cases reported to NCPCR | Count |
| Cases where employment suspended | Count |
| Cases closed (resolved) | Count |
| Cases pending at end of period | Count |

**Part 4 — POCSO Case Details Table:**

One row per POCSO case identified during the period.

| Column | Notes |
|---|---|
| Case Ref | `POCSO-{YYYYMMDD}-{seq}` |
| Institution Type | SCHOOL / COLLEGE / COACHING |
| Offense Type | Full text |
| Offense Date | Date or "Unknown" |
| Date Identified | `bgv_pocso_case.created_at` date |
| Date Reported to NCPCR | `ncpcr_reported_at` date |
| NCPCR Ref | — |
| Action Taken | Closure type / current status |
| Institution Notified | Yes / No |

**Note on privacy:** Staff names and staff refs are NOT included in the NCPCR export. NCPCR receives case refs and institutional details only. Individual identities are shared only if NCPCR specifically requests them through formal channels.

**Part 5 — Non-Compliant Institutions:**

Institutions where coverage < 100% at end of period. Shows institution type only (not name) in export — to protect commercial sensitivity. BGV Manager can toggle to include institution names if required for regulatory submission.

#### Section C — Export Controls

| Export | Format |
|---|---|
| [Export NCPCR Report PDF] | PDF — formatted as official report with page numbers, EduForge letterhead, signing section |
| [Export NCPCR Report CSV (Detailed)] | CSV — all case details for machine-readable submission |
| [Download Report as Word Document] | .docx — for manual editing before official submission |

**Access:** POCSO Compliance Officer (41), POCSO Reporting Officer (78), BGV Manager (39), Legal Officer (75), Platform Admin (10).
DPO (76) read-only — cannot export.

---

### Tab 3 — Vendor Performance

Comparative performance report across all BGV vendors.

#### Section A — Filters

| Filter | Control | Default |
|---|---|---|
| Date Range | Date picker | Last 90 days |
| Vendor | Multiselect: All / specific vendors | All active vendors |
| Institution Type | Multiselect | All |

#### Section B — Performance Comparison Table

| Metric | Vendor A | Vendor B | Vendor C |
|---|---|---|---|
| Total submissions in period | — | — | — |
| Results received | — | — | — |
| Avg turnaround (hours) | — | — | — |
| SLA compliance % | — | — | — |
| CLEAR rate | — | — | — |
| FLAGGED rate | — | — | — |
| INCONCLUSIVE rate | — | — | — |
| Error / failed submission rate | — | — | — |
| Uptime % (health check) | — | — | — |

**Best performer highlight:** Column of best-performing vendor per metric highlighted in green.

#### Section C — Turnaround Trend Chart

Line chart. One line per vendor. X-axis: month (last 12 months). Y-axis: avg turnaround hours. Dashed line: contracted SLA.

#### Section D — SLA Breach Detail

Table of all verifications where turnaround exceeded contracted SLA, grouped by vendor.

| Column | Notes |
|---|---|
| Vendor | — |
| Staff Ref | — |
| Institution | — |
| Sent At | — |
| Returned At | — |
| Hours Over SLA | Red if > 50% of SLA |
| Breach Reason | Vendor-provided or "Unknown" |

#### Section E — Export Controls

[Export Vendor Performance CSV] — BGV Manager, Platform Admin only.

---

### Tab 4 — Renewal Pipeline

Forward-looking report: which staff verifications expire in the next 30/60/90 days.

#### Section A — Renewal Summary

| Period | Staff Due | Initiated | % Initiated |
|---|---|---|---|
| Next 30 days | Count | Count | % |
| 31–60 days | Count | Count | % |
| 61–90 days | Count | Count | % |

**Alert if:** Next 30 days count > 50 and `% Initiated < 50%`: ⚠️ "High renewal volume due — {N} renewals in 30 days with only {%}% initiated. Increase team capacity or initiate renewals now."

#### Section B — Renewal Pipeline Table

| Column | Notes |
|---|---|
| Staff Ref | — |
| Institution | — |
| Verification Expiry | Date |
| Days Until Expiry | Countdown — red if ≤ 30 |
| Renewal Status | NOT_INITIATED / DOCUMENTS_REQUESTED / IN_PROGRESS |
| Assigned To | BGV Executive or "—" |
| Action | [View Record →] → G-03 |

Pagination: 25 rows. Sort: expiry date ascending (soonest first) by default.

**Filter:** Next 30 / 60 / 90 days | Institution Type | Status.

#### Section C — Export Controls

| Export | Notes |
|---|---|
| [Export Renewal Pipeline CSV] | Full renewal list with expiry dates |
| [Send Batch Renewal Reminders] | Sends in-app notifications to institution admins for all NOT_INITIATED renewals in selected period. BGV Manager confirmation required. |

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | BGV Manager (39), POCSO Officer (41), POCSO Reporting Officer (78), DPO (76), Legal Officer (75), Platform Admin (10) |
| BGV Executive (40) | No access |
| BGV Ops Supervisor (92) | No access — reporting is above supervisor scope |
| Tab 1 Coverage Report full access | All with page access |
| Tab 2 NCPCR Report export | POCSO Officer (41), Reporting Officer (78), BGV Manager (39), Legal Officer (75), Platform Admin (10) |
| DPO (76) | Read-only — no export buttons |
| Tab 3 Vendor Performance export | BGV Manager (39), Platform Admin (10) |
| Tab 4 [Send Batch Renewal Reminders] | BGV Manager (39), Supervisor (92 — exception for this action), Platform Admin (10) |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| NCPCR report generated for period with 0 POCSO cases | Part 3 shows all zeros. Part 4 case table empty. Normal — still a valid report to submit (shows due diligence). |
| Report generation for large dataset takes > 15s | Progress bar + "Generating report — this may take a moment." If > 30s: background task; email/in-app notification when ready. |
| Vendor with no submissions in selected period | Included in comparison table with all zeros and note "No submissions in period." |
| DPO requests report with staff names included | DPO role cannot export — they review content for privacy compliance. If name export needed, BGV Manager exports and coordinates with DPO. |
| Financial year boundary (renewals spanning years) | Renewal pipeline uses absolute expiry dates; financial year boundary does not affect calculation. |

---

## 7. UI Patterns

### Loading States
- Tab content: shimmer (summary stats + table skeleton)
- Export PDF: "Generating PDF…" spinner with progress

### Toasts
| Action | Toast |
|---|---|
| Coverage report generated | ✅ "Coverage report generated for {date}" (3s) |
| NCPCR report PDF exported | ✅ "NCPCR report PDF downloaded" (3s) |
| Renewal reminders sent | ✅ "{N} institution admins notified about pending renewals" (4s) |

---

*Page spec complete.*
*G-07 covers: 4-tab report hub → Coverage Report (platform summary / by-type / per-institution / CSV+PDF export) → NCPCR Mandatory Report (5-part structured report / FY selector / privacy-safe staff anonymisation / Word+PDF+CSV export) → Vendor Performance (comparison table / turnaround trend / SLA breach detail) → Renewal Pipeline (30/60/90-day forecast / batch reminder send).*
