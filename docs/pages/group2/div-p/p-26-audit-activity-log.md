# P-26 — Audit Activity Log

> **URL:** `/group/audit/activity-log/`
> **File:** `p-26-audit-activity-log.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** G4/G5 (CEO / Chairman) — primary consumer; all Division P roles can read

---

## 1. Purpose

The Audit Activity Log is the immutable, tamper-proof record of every action taken within Division P — every finding raised, every CAPA status change, every escalation sent, every policy update, every report generated, every template modified, every assignment made, every compliance score recorded, every acknowledgement given. It is the meta-audit: the audit of the auditors.

In Indian education governance — particularly for multi-branch groups — the Chairman and Board need assurance that the audit function is operating correctly and independently. If an Audit Head is overriding conflict-of-interest flags without proper documentation, the log shows it. If a CAPA item status was manually changed from "Overdue" to "Closed" without verification, the log shows it. If a compliance score was edited after the fact to improve a branch's ranking, the log shows it. No action within Division P happens without a log entry, and no log entry can be deleted or modified.

The problems this page solves:

1. **Audit function accountability:** The people who audit the branches must themselves be subject to audit. This log provides that accountability — it records what every Division P role did, when, and on what data.

2. **Manual override tracking:** Several pages in Division P allow authorised overrides — CAPA deadline extensions, conflict-of-interest overrides, rotation rule overrides, score adjustments. Every override is logged with the user, timestamp, and mandatory reason. This creates a transparent record of exceptions.

3. **Potential data manipulation detection:** If a compliance score or CAPA status changes in a way that benefits a particular branch without a corresponding audit event (inspection visit, CAPA closure), the log's anomaly detection flags it.

4. **Regulatory compliance:** CBSE, RTE, and POCSO-related audit activities require documentation that proper processes were followed. The activity log serves as audit-grade evidence that Division P operated per its published policies.

5. **Incident investigation:** When something goes wrong — a POCSO complaint that should have been escalated wasn't, an overdue Critical CAPA was not escalated for 45 days, a branch's compliance score suddenly dropped — the activity log provides a forensic timeline to reconstruct what happened and identify where the process failed.

**Scale:** 1,000–10,000 log entries per month · All Division P users · All Division P pages · Immutable storage · 7-year retention (aligned to Indian educational institution record-keeping standards)

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group CEO / Chairman | — | G4/G5 | Full read — all entries, all users, all branches | Primary consumer |
| Group Internal Audit Head | 121 | G1 | Read all entries — operational oversight | Oversight |
| Group Compliance Data Analyst | 127 | G1 | Read — activity metrics for MIS and anomaly detection | Reporting |
| All other Division P roles | 122–128 | G1/G3 | Read own actions only — cannot see other users' entries | Self-audit |
| Branch Principal | — | G3 | Read entries related to own branch (actions taken on their branch data) | Branch transparency |

> **Immutability enforcement:** No user — including G5 / Chairman — can delete, edit, or reverse a log entry. The log is append-only. A G5 attempting to edit a log entry receives: "Audit log entries cannot be modified. This is an immutable audit trail per Group Policy POL-AUD-005." If a log entry is incorrect due to a system error, a correction entry is appended with reference to the original.

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Branch staff see only log entries for their branch. G1 roles see own entries + entries related to all branches. G4+ see all entries.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Activity Log
```

### 3.2 Page Header
```
Audit Activity Log                                          [Export]  [Anomaly Report]
Internal Audit Head — T. Subramaniam  /  CEO — P. Ramaiah
Sunrise Education Group · 2,847 entries this month · Last entry: 2 minutes ago
```

### 3.3 Filter Bar
```
User: [All / Select ▼]    Action Type: [All / Finding Raised / CAPA Updated / Score Changed / Escalation / Policy Change / Override / Assignment / Report Generated / Template Modified / Acknowledgement ▼]
Branch: [All / Select ▼]    Severity Impact: [All / Critical / Major / Minor / Administrative ▼]
Date Range: [This Month ▼]  [Custom: From ___ To ___]
Override Only: ☐ Show overrides only
Anomaly Flagged: ☐ Show flagged entries only
                                                                        [Apply]  [Reset]
```

### 3.4 KPI Summary Bar

| # | KPI | Colour Logic |
|---|---|---|
| 1 | Log Entries (Period) | Neutral blue |
| 2 | Unique Active Users | Neutral |
| 3 | Override Actions | ≤ 5 amber · > 10 red |
| 4 | Anomaly Flags | 0 green · ≥ 1 red |
| 5 | Critical Actions (last 24 hrs) | Neutral |
| 6 | Last Audit Activity | Timestamp (red if > 48 hrs — audit function may be inactive) |

---

## 4. Log Entry Table

Primary view — chronological log of all entries.

**Table columns:**

| # | Column | Width | Content |
|---|---|---|---|
| 1 | Timestamp | 140px | dd-MMM-yyyy HH:mm:ss |
| 2 | User | 130px | Name + Role |
| 3 | Action Type | 140px | Colour-coded badge (see below) |
| 4 | Entity | 120px | CAPA ID / Branch / Policy / Report / Assignment |
| 5 | Branch | 120px | Affected branch name |
| 6 | Description | 280px | Auto-generated description (e.g., "CAPA-2026-00289 status changed from In Progress to Verification Pending") |
| 7 | Override | 60px | ⚠️ if this entry is an override action |
| 8 | Anomaly | 60px | 🔴 if system flagged as anomalous |
| 9 | Actions | 60px | [Detail] |

**Action Type badge colours:**

| Action Type | Badge Colour |
|---|---|
| Finding Raised | Blue |
| CAPA Status Changed | Purple |
| CAPA Closed | Green |
| CAPA Overdue (auto-flag) | Amber |
| Escalation Sent | Orange |
| Escalation Response Recorded | Blue |
| Compliance Score Recorded | Teal |
| Score Edited (post-record) | Red |
| Policy Published | Green |
| Policy Updated | Blue |
| Override Action | Red |
| Assignment Created | Blue |
| Conflict Override | Red |
| Rotation Override | Orange |
| Report Generated | Teal |
| Report Distributed | Green |
| Template Published | Green |
| Acknowledgement | Green |

**Pagination:** 100 rows per page. Infinite scroll option available.

**Default sort:** Timestamp descending (newest first).

---

## 5. Log Entry Examples

```
26-Mar-2026 14:23:11  K. Venkatesh (128)    CAPA Status Changed      CAPA-2026-00289  Sunrise Miyapur
  Description: CAPA-2026-00289 status changed from In Progress → Verification Pending.
               Action items 1–3 marked complete. Action item 4 (staff training) still pending.
               Verification requested from S. Reddy (123).

26-Mar-2026 14:18:34  T. Subramaniam (121)  Override Action ⚠️        CAPA-2026-00289  Sunrise Miyapur
  Description: CAPA closure deadline extended by 15 days (from 20-Mar-2026 to 04-Apr-2026).
               Override reason: "Training workshop delayed due to trainer unavailability.
               Confirmed new date 25-Mar-2026. One remaining action item only."
               Approved by: T. Subramaniam (121)

26-Mar-2026 11:02:45  S. Reddy (123)        Finding Raised            CAPA-2026-00415  Sunrise KPHB
  Description: New finding raised — Category: Fire Safety, Severity: Critical.
               Source: Inspection Visit #112. Fire NOC expired 01-Feb-2026 (53 days overdue).
               Auto-escalated to CEO per POL-CAPA-004.

26-Mar-2026 09:15:22  System (auto)         Escalation Sent           ESC-2026-00121   Sunrise KPHB
  Description: Auto-escalation triggered for CAPA-2026-00415 (Critical finding).
               Escalated to: P. Ramaiah (CEO). Rule: POL-CAPA-001 Section 1.1 — Critical
               severity findings auto-escalate to CEO on day 1.

25-Mar-2026 18:44:01  P. Sunitha (127)      Compliance Score Recorded  Score Q3 FY26   Sunrise HITEC City
  Description: Quarterly compliance score recorded — Q3 FY 2025-26.
               Score: 97% (Band A+). Dimensions: Financial 98%, Academic 99%, Safety 95%,
               Affiliation 100%, CAPA 96%, Grievance 94%. Prior quarter: 95%.

25-Mar-2026 16:30:15  T. Subramaniam (121)  Report Distributed        MIS-Q3-2025-26   All branches
  Description: Q3 FY 2025-26 MIS Report distributed to 9 recipients.
               Recipients: CEO, Chairman, 3 Zone Directors, CFO, Process Improvement Coordinator.
               Distribution method: Platform email with PDF attachment.

25-Mar-2026 10:12:44  T. Subramaniam (121)  Conflict Override ⚠️       Assignment       Sunrise KPHB
  Description: Conflict-of-interest override approved for inspection assignment.
               Auditor: S. Reddy (123). Conflict type: Previously employed (2020–2022).
               Override reason: "Only qualified fire safety inspector available for Q4 visit.
               K. Ravi on extended leave. Exception approved for this quarter only."
               Second approver: P. Ramaiah (CEO) — verbal approval recorded.
```

---

## 6. Anomaly Detection

The system auto-flags log entries that match anomaly patterns:

**Anomaly rules:**

| Anomaly Type | Trigger | Severity |
|---|---|---|
| Score edited after recording | A compliance score is edited more than 30 minutes after initial recording | 🔴 High |
| CAPA closed without verification step | CAPA moved to Closed without a Verification Pending status in history | 🔴 High |
| Multiple status changes in < 10 minutes | Same CAPA item changed status 3+ times in 10 minutes | 🟠 Medium |
| Override without documented reason | Override action with empty reason field | 🔴 High (blocked — cannot proceed without reason) |
| Critical CAPA not escalated within 24 hrs | Critical finding raised; no escalation log entry within 24 hours | 🔴 High |
| Branch score improved without recent audit | Branch compliance score increased > 10 pts without a corresponding inspection or audit entry | 🟠 Medium |
| High-severity grievance not acknowledged | High-severity complaint > 48 hours without Grievance Audit Officer acknowledgement entry | 🔴 High |
| User activity outside business hours (volume spike) | A user performs 50+ actions between midnight and 6am | 🟡 Low (informational) |

**Anomaly flags are displayed:**
- In the log table (red 🔴 icon in Anomaly column)
- In the `[Anomaly Report]` view
- In the monthly MIS report (Section — Audit Integrity, auto-included)

**Anomaly Report view:**
List of all flagged entries for selected period with:
- Entry detail
- Anomaly type
- Resolution: Investigated & explained / False positive / Referred to CEO

---

## 7. Log Detail Drawer

**Trigger:** `[Detail]` on any row.

**Content:**
```
Log Entry Detail                                                        [✕]
26-Mar-2026 14:18:34 · T. Subramaniam (121) · Override Action

Entity: CAPA-2026-00289 · Sunrise Miyapur
Override Type: CAPA Deadline Extension

Before: Due date 20-Mar-2026
After: Due date 04-Apr-2026 (+15 days)

Override Reason:
  "Training workshop delayed due to trainer unavailability. Confirmed new date 25-Mar-2026.
  Only action item 4 (staff training) remains. Items 1–3 verified complete.
  Risk assessment: Low — safety-critical items already resolved."

Second Approver Required: No (Minor deadline extension; Audit Head authority per POL-CAPA-001)

Preceding Entry: 26-Mar-2026 14:14:11 — K. Venkatesh — Update Action Item 4 status:
  "Training workshop rescheduled to 25-Mar-2026. Trainer confirmed."

Subsequent Entry: 26-Mar-2026 14:23:11 — K. Venkatesh — CAPA Status Changed (In Progress → Verification Pending)

Entry Hash: sha256:9f8b2c1a...  (immutability verification)
```

---

## 8. Export

**Format options:**
- Excel (CSV) — full log with all columns
- PDF — filtered log with summary and anomaly flags
- JSON — API-compatible format for external audit tools

**Retention note displayed:**
```
ℹ️ Audit activity logs are retained for 7 years per Group Policy POL-AUD-002.
   Exported logs are subject to the same confidentiality classification as the originals.
```

---

## 9. Charts

### Chart 1 — Activity Volume by Day (bar chart)
- **Type:** Bar (Chart.js 4.x)
- **X-axis:** Days in period
- **Y-axis:** Log entry count
- **Colour:** Blue for normal · Orange for days with override actions · Red for days with anomaly flags
- **Purpose:** Shows audit function activity pattern — are auditors active daily?
- **API:** `GET /api/v1/group/{id}/audit/activity-log/charts/daily-volume/`

### Chart 2 — Action Type Distribution (doughnut)
- **Type:** Doughnut (Chart.js 4.x)
- **Segments:** Finding Raised · CAPA Update · Score Recorded · Escalation · Override · Report · Other
- **Purpose:** What proportion of activity is proactive (findings, scores) vs reactive (overrides, escalations)?
- **API:** `GET /api/v1/group/{id}/audit/activity-log/charts/action-distribution/`

### Chart 3 — User Activity Heatmap (matrix)
- **Type:** Matrix heatmap
- **X-axis:** Days of week (Mon–Sun)
- **Y-axis:** Hours of day (0–23)
- **Cell colour:** White (0 actions) → Blue → Red (high volume)
- **Purpose:** Identifies unusual patterns (late-night activity clusters)
- **API:** `GET /api/v1/group/{id}/audit/activity-log/charts/user-activity-heatmap/`

---

## 10. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Filter applied | "Showing 847 log entries for March 2026 · 8 users" | Info (blue) |
| Export started | "Exporting 2,847 audit log entries — March 2026 · Excel" | Info (blue) |
| Anomaly report opened | "4 anomalies flagged for March 2026 — review recommended" | Warning (amber) |
| Anomaly resolved | "Anomaly ANO-2026-023 marked as investigated and explained" | Info (blue) |
| Edit attempt blocked | "Audit log entries cannot be modified — this is an immutable audit trail" | Error (red) |

---

## 11. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No entries for period | Activity stream empty | "No audit activity recorded for this period. This may indicate the audit function was inactive." | — |
| No anomalies | Green shield | "No anomalies detected for this period — audit activity patterns are within normal parameters." | — |
| Filter returns zero | Magnifying glass | "No log entries match your filters." | `[Reset Filters]` |

---

## 12. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Log table initial load | 20 skeleton rows → data | < 1s |
| Filter apply | "Loading…" on table → refresh | < 500ms |
| Log detail drawer | Drawer skeleton → populated | < 500ms |
| Anomaly report | Skeleton list → anomaly entries | < 500ms |
| Charts | Grey placeholders → Chart.js | < 500ms each |
| Export preparation | "Preparing export… N entries" progress | 2–10s |

---

## 13. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/activity-log/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | List log entries (paginated, filterable) | G1+ (own scope per role) |
| 2 | GET | `/{entry_id}/` | Single entry detail with hash verification | G1+ |
| 3 | GET | `/anomalies/` | Anomaly-flagged entries only | 121, G4+ |
| 4 | POST | `/anomalies/{entry_id}/resolve/` | Mark anomaly as investigated | 121, G4+ |
| 5 | GET | `/kpis/` | KPI bar aggregates | G1+ |
| 6 | GET | `/charts/daily-volume/` | Chart 1 data | G1+ |
| 7 | GET | `/charts/action-distribution/` | Chart 2 data | G1+ |
| 8 | GET | `/charts/user-activity-heatmap/` | Chart 3 data | 121, G4+ |
| 9 | GET | `/export/` | Export log entries (Excel/PDF/JSON) | G1+ |

> **System-generated entries:** Every state change in Division P automatically writes a log entry via the platform's internal `AuditLogger` service. This is not a user-facing API — it is backend infrastructure. The entries are written atomically with the underlying state change (database transaction). If the state change succeeds, the log entry always succeeds. There is no mechanism to make a state change without generating a log entry.

> **Immutability implementation:** Log entries are stored in an append-only table with a database-level trigger that rejects UPDATE and DELETE operations. Entry integrity is verified by a SHA-256 hash of (entry_id + timestamp + user_id + action_type + entity_id + description). Hash is stored in the entry and can be independently verified.

---

## 14. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Log table load | Page load | `hx-get=".../activity-log/"` | `#log-table` | `innerHTML` | 100 rows paginated |
| Filter apply | `[Apply]` click | `hx-get` with filters | `#log-table` | `innerHTML` | Re-render table |
| Log detail drawer | Row `[Detail]` click | `hx-get=".../activity-log/{id}/"` | `#right-drawer` | `innerHTML` | 720px |
| Pagination | Page click | `hx-get` with page param | `#log-table-body` | `innerHTML` | — |
| Anomaly view | `[Anomaly Report]` click | `hx-get=".../activity-log/anomalies/"` | `#log-content` | `innerHTML` | Anomaly sub-view |
| Resolve anomaly | Button click | `hx-post=".../activity-log/anomalies/{id}/resolve/"` | `#anomaly-{id}-status` | `innerHTML` | Toast + badge |
| KPI load | Page load | `hx-get=".../activity-log/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Charts load | Section shown | `hx-get` chart endpoints | `#chart-{name}` | `innerHTML` | Chart.js |
| Export | `[Export]` click | `hx-get=".../activity-log/export/"` | `#export-frame` | `innerHTML` | File download |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
