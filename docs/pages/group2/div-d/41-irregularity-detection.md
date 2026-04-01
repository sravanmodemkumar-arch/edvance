# 41 — Irregularity Detection Dashboard

- **URL:** `/group/finance/audit/irregularities/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Internal Auditor G1 (primary) · CFO G1 (view)

---

## 1. Purpose

The Irregularity Detection Dashboard uses rule-based analytics to surface financial anomalies across all branches that may indicate errors, unauthorised transactions, or fraud. Unlike the Audit Findings page (which captures investigator-raised findings), this page runs automated checks on transaction data and flags patterns that warrant investigation.

Detection rules include: duplicate receipts (same student, same amount, close dates), fee collection without corresponding fee demand, large cash transactions above threshold, vendor payments without linked PO, payroll amount spikes (>20% month-on-month), and bank reconciliation discrepancies.

The auditor reviews each alert, classifies it (false positive / genuine irregularity), and either dismisses or converts it to a formal finding.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Internal Auditor | G1 | Full read + classify + convert to finding |
| Group CFO | G1 | Read — high severity alerts only |
| Group Finance Manager | G1 | Read — all alerts |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Internal Audit → Irregularity Detection
```

### 3.2 Page Header
- **Title:** `Irregularity Detection Dashboard`
- **Subtitle:** `[N] Active Alerts · [X] High Severity · Last Scan: [Datetime]`
- **Right-side controls:** `[Branch ▾]` `[Severity ▾]` `[Type ▾]` `[Run Scan Now ↻]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| High-severity alert > 48 hours unreviewed | "[N] high-severity alert(s) not reviewed for 48+ hours." | Red |
| Scan not run in > 24 hours | "Irregularity scan last run [X] hours ago. Run now." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Active Alerts | Count | Red if > 0 high severity |
| High Severity | Count | Red if > 0 |
| Medium Severity | Count | Amber if > 0 |
| Converted to Findings | Count (AY) | Informational |
| False Positives | Count (AY) | Informational |

---

## 5. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Alert ID | Text | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Alert Type | Badge: Duplicate Receipt · Cash Threshold · PO Missing · Payroll Spike · Bank Discrepancy · Other | ✅ | ✅ |
| Severity | Badge: High · Medium · Low | ✅ | ✅ |
| Description | Text | — | — |
| Amount | ₹ | ✅ | — |
| Detected Date | Date | ✅ | — |
| Status | Badge: Open · Under Review · Converted to Finding · Dismissed | ✅ | ✅ |
| Actions | Review · Convert to Finding · Dismiss | — | — |

### 5.1 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select |
| Alert Type | Multi-select |
| Severity | Multi-select |
| Status | Multi-select |
| Date Range | Date picker |

### 5.2 Search
- Alert ID · Branch · Description text

### 5.3 Pagination
- 25 rows/page · Sort: Severity + Detected Date (oldest high first)

---

## 6. Drawers

### 6.1 Drawer: `alert-review` — Review Alert
- **Trigger:** Review action
- **Width:** 720px

**Alert Details:**
- Type · Branch · Amount · Detected On

**Evidence Section:**
- Auto-generated evidence: "Receipt [R1] — ₹5,000 on 2026-01-15 · Receipt [R2] — ₹5,000 on 2026-01-15 (same student, same day)"
- Link to relevant records (receipts, PO, payroll entries)

**Classification:**
| Field | Type | Required |
|---|---|---|
| Verdict | Radio: Genuine Irregularity · False Positive · Needs More Investigation | ✅ |
| Notes | Textarea | ✅ |

**Actions (based on verdict):**
- Genuine → [Convert to Finding] — opens Finding Raise form pre-populated
- False Positive → [Dismiss Alert]
- More Investigation → [Mark Under Review] + set reminder

### 6.2 Drawer: `detection-rules` — View Active Detection Rules
- List of all automated rules with description, threshold, and enabled/disabled toggle

---

## 7. Detection Rules (Visible in the drawer)

| Rule | Threshold | Enabled |
|---|---|---|
| Duplicate fee receipt | Same student + same amount within 7 days | ✅ |
| Cash receipt above threshold | > ₹50,000 in single receipt | ✅ |
| Vendor payment without PO | Any payment > ₹10,000 without linked PO | ✅ |
| Payroll spike | Month-on-month increase > 20% for any branch | ✅ |
| Bank recon discrepancy | Difference > ₹5,000 for > 15 days | ✅ |
| Fee collection without demand | Receipt exists but no fee demand record | ✅ |

---

## 8. Charts

### 8.1 Alert Volume by Type (Bar — Monthly)
### 8.2 Alert Resolution Rate (Donut: Converted · Dismissed · Open)

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Alert converted | "Alert [ID] converted to Finding [F-ID]." | Warning | 4s |
| Alert dismissed | "Alert [ID] dismissed as false positive." | Info | 3s |
| Scan triggered | "Irregularity scan running. Refresh in 60 seconds." | Info | 5s |
| Export | "Irregularity report exported." | Info | 3s |

---

## 10. Empty States

| Condition | Heading | Description |
|---|---|---|
| No active alerts | "No irregularities detected" | "No anomalies found in the last scan." |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table |
| Scan running | Progress bar: "Scanning [N] branches..." |
| Alert drawer | Spinner + skeleton |

---

## 12. Role-Based UI Visibility

| Element | Internal Auditor G1 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [Run Scan Now] | ✅ | ❌ | ❌ |
| [Convert to Finding] | ✅ | ❌ | ❌ |
| [Dismiss] | ✅ | ❌ | ❌ |
| View high severity | ✅ | ✅ | ✅ |
| View all alerts | ✅ | ❌ | ✅ |
| Export | ✅ | ❌ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/audit/irregularities/` | JWT (G1+) | Alert list |
| POST | `/api/v1/group/{id}/finance/audit/irregularities/scan/` | JWT (G1) | Run scan |
| GET | `/api/v1/group/{id}/finance/audit/irregularities/{aid}/` | JWT (G1+) | Alert detail |
| PUT | `/api/v1/group/{id}/finance/audit/irregularities/{aid}/classify/` | JWT (G1) | Classify alert |
| POST | `/api/v1/group/{id}/finance/audit/irregularities/{aid}/convert/` | JWT (G1) | Convert to finding |
| GET | `/api/v1/group/{id}/finance/audit/irregularities/export/` | JWT (G1+) | Export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../irregularities/?type=&severity=` | `#alerts-section` | `innerHTML` |
| Review drawer | `click` | GET `.../irregularities/{id}/` | `#drawer-body` | `innerHTML` |
| Classify | `submit` | PUT `.../irregularities/{id}/classify/` | `#drawer-body` | `innerHTML` |
| Run scan | `click` | POST `.../irregularities/scan/` | `#scan-status` | `outerHTML` |
| Scan status poll | `every 10s` (while running) | GET `.../audit/irregularities/scan-status/` | `#scan-status` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
