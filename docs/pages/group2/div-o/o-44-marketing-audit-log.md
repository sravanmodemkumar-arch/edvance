# O-44 — Marketing Audit Log

> **URL:** `/group/marketing/admin/audit-log/`
> **File:** `o-44-marketing-audit-log.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group CEO / Chairman (G4/G5) — primary consumer; immutable business audit trail

---

## 1. Purpose

The Marketing Audit Log is the immutable, comprehensive business audit trail for every action performed across all 43 pages in Division O — Marketing & Admissions Campaigns. This is NOT a technical system log (those live in CloudWatch); this is a business-readable record designed for three audiences who cannot read JSON or parse server logs: trust board members conducting annual reviews, Chartered Accountant firms performing statutory audits, and internal compliance officers investigating specific incidents.

In Indian education groups — particularly trusts and societies registered under the Indian Trusts Act 1882 or the Societies Registration Act 1860 — marketing spend is a perennial area of financial irregularity and governance concern. The audit log addresses five specific scenarios that Indian education group auditors routinely investigate:

1. **Unauthorised discount investigation:** A branch principal gave a 35% fee concession to a "VIP family" without CEO approval. The trust board wants to know: who created the discount record, what was the original amount, who approved it (if anyone), when did it happen, and was any policy (O-43) in effect at the time that was violated? Without an audit trail, the principal claims "the system allowed it" and nobody can prove otherwise. The audit log records the exact before-and-after values, the logged-in user, their IP address, and the timestamp — providing incontrovertible evidence for the disciplinary committee.

2. **Vendor payment inflation:** The marketing vendor manager (O-41) shows a newspaper ad cost of Rs. 2.5L, but the actual published rate card was Rs. 1.8L. The CA firm performing the annual audit wants to trace: who entered the vendor payment, who approved it, was the amount modified after initial entry, and is there a pattern of inflated payments with the same vendor? The audit log captures every CREATE and UPDATE on vendor payment records with full field-level before/after tracking.

3. **Lead data export compliance (DPDPA):** Under DPDPA 2023, exporting a list of 50,000 parent phone numbers from the lead database (O-15) is a data processing activity that requires lawful purpose. If a parent complains to the Data Protection Board that they received unsolicited marketing calls, the group must demonstrate: who exported the data, when, for what stated purpose, and what consent basis was used. The audit log marks every data export as a "flagged action" that appears in the high-risk actions panel for proactive review.

4. **Campaign budget diversion:** The marketing budget for Branch A was Rs. 12L, but the actual spend recorded is Rs. 18L. Meanwhile, Branch B's budget was Rs. 10L with only Rs. 4L spent. An internal auditor suspects the Campaign Manager shifted Branch B's budget to Branch A to favour a branch run by a trustee's relative. The audit log traces every budget modification (O-09): original allocation, each modification with reason, who approved the change, and the final state.

5. **Topper data misuse:** A Topper Relations Manager (O-28) downloads topper photos and marks for use in an external coaching centre's marketing material — a direct conflict of interest and data breach. The audit log records every access to the topper database, every export, and every download, enabling the trust to identify the breach and take disciplinary action.

The audit log is **append-only**: no record can be edited, deleted, or modified after creation. Even Platform Admins (G5) cannot alter audit entries. Retention is 7 years per Indian audit requirements (Income Tax Act Section 44AA, Companies Act 2013 Section 128 for registered societies, and DPDPA Section 8 data processing records). All timestamps are IST (UTC+5:30). Every entry links back to the source page, the specific entity affected, and the user who performed the action.

**Flagged actions** are automatically marked for entries that meet high-risk criteria: discounts exceeding 25%, single payments exceeding Rs. 1,00,000, data exports containing more than 100 records, bulk operations (deleting, reassigning, or modifying more than 10 records at once), role assignment changes, and policy modifications. These flagged actions appear in a dedicated high-risk panel and can be subscribed to via email/WhatsApp alerts by G4/G5 users.

**Scale:** 500-5,000 audit entries per day (large group during peak season) . 150-500 entries per day (small group) . 7-year retention . 1M-10M total entries per group over lifecycle

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group CEO / Chairman | — | G4/G5 | Full read — all actions, all users, all pages, all time; set alert rules; export | Primary audit consumer |
| Group Admissions Campaign Manager | 119 | G3 | Read — own actions + team actions (roles 130, 131 reporting to them) | Cannot see G4/G5 actions; cannot see other G3 users' actions |
| Group Topper Relations Manager | 120 | G3 | Read — own actions only | Self-audit reference |
| Group Admission Data Analyst | 132 | G1 | Read — all actions (analytics scope) + export for MIS | Full visibility for reporting; cannot modify anything |
| Group Campaign Content Coordinator | 131 | G2 | Read — own actions only | Self-audit reference |
| Group Admission Telecaller Executive | 130 | G3 | No access | Telecallers should not be able to review audit trails |
| External Auditor (CA Firm) | — | G1 | Read — all actions + export | Time-limited access granted by G5; auto-expires after 30 days; logged |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. G4/G5 see all entries. G3 users see own + direct reports only (except role 132 who has full read for analytics). No user at any level can create, edit, or delete audit entries. The audit log API has no POST/PUT/DELETE endpoints for entries — entries are created exclusively by system triggers. External auditor access requires G5 invitation with explicit expiry date.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Administration  >  Marketing Audit Log
```

### 3.2 Page Header
```
Marketing Audit Log                                    [Advanced Filters]  [Flagged Actions]  [Export Report]  [Alert Settings]
CEO — Rajendra Prasad Reddy
Sunrise Education Group . 30-day summary: 12,847 actions . 23 flagged . 8 unique users . Last action: 2 min ago
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Actions (30d) | Integer | COUNT(audit_entries) WHERE created_at >= NOW() - 30 days | Static blue | `#kpi-total` |
| 2 | Unique Users (30d) | Integer | COUNT(DISTINCT user_id) WHERE created_at >= NOW() - 30 days | Static indigo | `#kpi-users` |
| 3 | Flagged Actions (30d) | Integer | COUNT WHERE flagged = true AND created_at >= NOW() - 30 days | Red > 10, Amber 1-10, Green = 0 | `#kpi-flagged` |
| 4 | Data Exports (30d) | Integer | COUNT WHERE action_category = 'access' AND action_type = 'export' AND created_at >= NOW() - 30 days | Amber > 20, Red > 50, Green <= 20 | `#kpi-exports` |
| 5 | High-Value Actions | Integer | COUNT WHERE (discount_pct > 25 OR amount > 100000) AND created_at >= NOW() - 30 days | Red > 5, Amber 1-5, Green = 0 | `#kpi-high-value` |
| 6 | Audit Alerts | Integer | COUNT unacknowledged alert notifications for current user | Red > 0, Green = 0 | `#kpi-alerts` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/admin/audit-log/kpis/"` -> `hx-trigger="load"`

---

## 5. Sections

### 5.1 Tab Navigation

Three tabs:
1. **Activity Log** — Chronological feed of all actions with filters
2. **Flagged Actions** — High-risk entries requiring review
3. **User Activity Summary** — Per-user action counts, patterns, and anomalies

### 5.2 Tab 1: Activity Log

**Filter bar:** Date range (preset: Today / Last 7d / Last 30d / Last 90d / Custom) . User (dropdown — all Division O users) . Role (dropdown) . Page/Module (dropdown — all 44 O-pages) . Action type (Create/Read/Update/Delete/Approve/Publish/Export/Assign/Bulk) . Action category (Lead Management/Campaign Operations/Financial/Content/Access/Configuration) . Entity type (Lead/Campaign/Budget/Vendor Payment/Policy/Material/Topper Record/etc.) . Flagged only (toggle) . Search (keyword — matches entity name, user name, or description)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Timestamp | DateTime | Yes | IST format: "DD MMM YYYY HH:MM:SS IST"; precision to seconds |
| User | Text + avatar | Yes | Full name + role badge; click -> user activity drawer |
| Role | Badge | Yes | Campaign Mgr / Topper Mgr / Telecaller / Content Coord / Analyst / CEO / Chairman |
| Action | Badge | Yes | Create (green) / Read (grey) / Update (blue) / Delete (red) / Approve (emerald) / Publish (indigo) / Export (amber) / Assign (violet) / Bulk (rose) |
| Category | Badge | Yes | Lead Mgmt (blue) / Campaign Ops (indigo) / Financial (amber) / Content (violet) / Access (rose) / Configuration (slate) |
| Page | Text | Yes | Source page: "O-15 Lead Pipeline" / "O-09 Budget Manager" / etc. |
| Entity | Text (link) | Yes | Affected entity: "Lead #4521 — Priya Sharma" / "Campaign: JEE 2026 Phase 1" / "Vendor Payment: Eenadu ₹2.5L" |
| Description | Text | No | Human-readable: "Updated lead status from 'Contacted' to 'Interested'" / "Exported 2,340 leads to CSV" / "Approved ₹3.2L budget increase for Branch Kukatpally" |
| Flag | Icon | Yes | 🚩 if flagged (high-risk); blank otherwise; click -> flag detail |
| IP Address | Text | No | Source IP; displayed only to G4/G5 |
| Actions | Button | No | [View Details ->] |

**Default sort:** Timestamp DESC (most recent first)
**Pagination:** Server-side . 50/page
**Auto-refresh:** `hx-trigger="every 30s"` — new entries prepended with slide-down animation

**Action category definitions:**

| Category | Tracked Actions | Source Pages |
|---|---|---|
| Lead Management | Create lead, update lead status, assign lead, convert lead, merge leads, delete lead, import leads, add lead note, schedule follow-up | O-15, O-16, O-17, O-18, O-19, O-20, O-21 |
| Campaign Operations | Create campaign, launch campaign, pause campaign, stop campaign, edit campaign, archive campaign, create event, update event, create drive, update seat targets | O-07, O-08, O-10, O-11, O-12, O-13, O-14, O-22, O-23, O-24, O-25, O-26 |
| Financial | Apply discount, modify discount, approve discount, create vendor payment, approve vendor payment, modify budget allocation, approve budget change, process referral payout, create ad booking | O-09, O-23, O-24, O-41 |
| Content | Upload material, delete material, publish prospectus, update brand standard, upload creative, create press release, publish press release, update social media post | O-02, O-03, O-04, O-06, O-31, O-32, O-33, O-34 |
| Access | Export leads, export reports, download topper data, export campaign analytics, download acknowledgment report, generate MIS report, external auditor login | O-15, O-28, O-35, O-36, O-37, O-39, O-40, O-43 |
| Configuration | Create/update policy, publish policy, change role assignment, update feature toggle, modify audit alert rule, update category settings, change approval workflow | O-02, O-42, O-43, O-44 |

### 5.3 Tab 2: Flagged Actions

Dedicated view for high-risk entries that require G4/G5 review.

**Auto-flag rules:**

| # | Rule | Threshold | Risk Level | Rationale |
|---|---|---|---|---|
| 1 | Discount exceeds limit | > 25% concession | High | Potential unauthorised fee waiver; most groups cap at 15-20% without CEO |
| 2 | High-value payment | Single payment > Rs. 1,00,000 | High | Vendor payment inflation risk |
| 3 | Large data export | Export containing > 100 records | Medium | DPDPA compliance — bulk PII movement |
| 4 | Bulk operation | Modify/delete > 10 records in single action | Medium | Mass data manipulation risk |
| 5 | Budget modification | Budget increased by > 20% from original | High | Budget diversion risk |
| 6 | After-hours action | Action between 10 PM and 6 AM IST | Low | Unusual activity pattern |
| 7 | Lead deletion | Any lead record deleted (not archived) | Medium | Data destruction risk |
| 8 | Policy change | Any modification to published policy | High | Governance control change |
| 9 | Role assignment | Any Division O role granted or revoked | High | Access control change |
| 10 | Topper data download | Export from O-28 Topper Database | Medium | Student data misuse risk |
| 11 | Failed action attempt | Permission denied on attempted action | Low | Potential unauthorised access attempt |
| 12 | Repeat high-value | Same user performs > 3 flagged actions in 24h | Critical | Pattern of suspicious activity |

**Flagged Actions Table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Timestamp | DateTime | Yes | IST |
| User | Text | Yes | Who performed the action |
| Flag Rule | Badge | Yes | Which auto-flag rule triggered; e.g., "Discount > 25%" / "High-Value Payment" |
| Risk Level | Badge | Yes | Critical (red pulse) / High (red) / Medium (amber) / Low (yellow) |
| Description | Text | No | Full action description with before/after values |
| Page | Text | Yes | Source page |
| Entity | Text (link) | Yes | Affected entity with link |
| Investigation Status | Badge | Yes | Unreviewed (red) / Under Investigation (amber) / Cleared (green) / Escalated (rose) |
| Reviewed By | Text | Yes | G4/G5 who reviewed; blank if unreviewed |
| Notes | Text | No | Investigation notes (added by G4/G5) |
| Actions | Buttons | No | [View Details] [Mark Cleared] [Escalate] [Add Note] |

**Default sort:** Timestamp DESC; Unreviewed entries highlighted with left red border
**Pagination:** Server-side . 25/page

### 5.4 Tab 3: User Activity Summary

Aggregated view of per-user action patterns for anomaly detection.

**Filter bar:** Date range . Role . Minimum actions (slider)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| User | Text | Yes | Full name |
| Role | Badge | Yes | Role name + level |
| Total Actions (period) | Integer | Yes | Total actions in selected date range |
| Creates | Integer | Yes | Count of CREATE actions |
| Updates | Integer | Yes | Count of UPDATE actions |
| Deletes | Integer | Yes | Count of DELETE actions; red if > 0 |
| Exports | Integer | Yes | Count of EXPORT actions; amber if > 5 |
| Flagged | Integer | Yes | Count of flagged actions; red if > 0 |
| Avg Actions/Day | Decimal | Yes | Total actions / working days in period |
| Peak Day | Date + count | Yes | Day with highest activity |
| After-Hours Actions | Integer | Yes | Actions between 10 PM - 6 AM IST; amber if > 0 |
| Last Active | DateTime | Yes | Most recent action timestamp |
| Actions | Button | No | [View Activity ->] |

**Default sort:** Total Actions DESC
**Anomaly highlight:** Users with activity > 2x the group average get an amber left-border; > 3x gets red

---

## 6. Drawers & Modals

### 6.1 Drawer: `action-detail` (720px, right-slide)

- **Title:** "Audit Entry — [Action Type] — [Entity]"
- **Sections:**
  - **Action summary:**
    - Action: [Create/Update/Delete/etc.] badge
    - Category: [Lead Mgmt/Financial/etc.] badge
    - Timestamp: DD MMM YYYY HH:MM:SS IST
    - User: Full name, role, role ID
    - IP address: [IP] (G4/G5 only)
    - Session ID: [UUID] (G4/G5 only — for correlating multiple actions in same session)
    - Page: [O-XX Page Name] (clickable link to source page)
    - Entity: [Entity type + ID + name] (clickable link to entity, if still exists)
  - **Before/After values (for UPDATE actions):**
    - Field-level diff table:

    | Field | Before | After |
    |---|---|---|
    | Status | Contacted | Interested |
    | Assigned To | Ravi Kumar | Meena Sharma |
    | Follow-up Date | 15 Mar 2026 | 20 Mar 2026 |
    | Notes | — | "Parent interested, wants hostel info" |

  - **For CREATE actions:** Full snapshot of created entity fields
  - **For DELETE actions:** Full snapshot of deleted entity fields (preserved at time of deletion)
  - **For EXPORT actions:** Export parameters (filters used, record count, file format, stated purpose)
  - **Related actions:** Other audit entries for the same entity within +-24 hours (shows context — e.g., lead created, then immediately exported)
  - **Flag information (if flagged):**
    - Flag rule triggered
    - Risk level
    - Investigation status
    - Investigation notes (editable by G4/G5)
- **Footer:** [Mark as Reviewed] [Escalate] [Add Investigation Note] [Export Entry] — G4/G5 only

### 6.2 Modal: `advanced-filter` (640px)

- **Title:** "Advanced Audit Log Filters"
- **Filter groups:**
  - **Time:**
    - Date range: Start date -> End date (calendar pickers)
    - Time range: Start time -> End time (for isolating after-hours activity)
    - Presets: Today / Yesterday / Last 7d / Last 30d / Last Quarter / Custom
  - **Actor:**
    - User (multi-select dropdown with search)
    - Role (multi-select)
    - IP address (text — supports wildcard: "192.168.*")
  - **Action:**
    - Action type (multi-select): Create / Read / Update / Delete / Approve / Publish / Export / Assign / Bulk
    - Action category (multi-select): Lead Mgmt / Campaign Ops / Financial / Content / Access / Configuration
  - **Target:**
    - Page (multi-select — all 44 O-pages)
    - Entity type (multi-select): Lead / Campaign / Budget / Vendor Payment / Policy / Material / Topper Record / Press Release / Event / Drive
    - Entity ID (text — exact match)
    - Entity name (text — partial match search)
  - **Risk:**
    - Flagged only (toggle)
    - Risk level (multi-select): Critical / High / Medium / Low
    - Investigation status (multi-select): Unreviewed / Under Investigation / Cleared / Escalated
  - **Value:**
    - Amount range: Min Rs. -> Max Rs. (for financial actions)
    - Discount percentage range: Min % -> Max %
    - Record count range: Min -> Max (for export actions)
- **Buttons:** Reset All . Apply Filters . Save as Preset
- **Saved presets:** Up to 10 saved filter presets per user (e.g., "Financial irregularities", "Data exports this quarter", "After-hours activity")
- **Access:** G1+ (filters respect role-based visibility — G3 users cannot filter for G4/G5 actions they cannot see)

### 6.3 Modal: `export-audit-report` (560px)

- **Title:** "Export Audit Report"
- **Fields:**
  - Report scope (radio): Current filtered view / Full date range / Custom selection
  - Date range (if custom): Start -> End
  - Format (dropdown): Excel (.xlsx) / CSV / PDF (formatted report with summary statistics)
  - Include (checkboxes):
    - [ ] Action details (default ON)
    - [ ] Before/after values (default OFF — increases file size significantly)
    - [ ] IP addresses (G4/G5 only)
    - [ ] Session IDs (G4/G5 only)
    - [ ] Summary statistics (default ON)
    - [ ] Flagged actions highlight (default ON)
  - Purpose (textarea, required — logged in the audit trail itself: "why are you exporting audit data?")
  - Recipient (optional — email address to send the report to; must be @group domain)
- **Buttons:** Cancel . Generate Report
- **Access:** G1+ (but IP/session fields only for G4/G5)
- **Note:** The export action itself is recorded in the audit log as a meta-entry: "Exported audit report: [date range], [N] entries, purpose: [stated purpose]"

### 6.4 Drawer: `flag-investigation` (640px, right-slide)

- **Title:** "Flag Investigation — [Entity] — [Flag Rule]"
- **Sections:**
  - **Flag summary:** Rule triggered, risk level, timestamp, user, action description
  - **Full action detail:** (same as action-detail drawer Section 6.1)
  - **Investigation timeline:**
    - Chronological list of investigation actions:
      - [Timestamp] Flag auto-created by system
      - [Timestamp] Reviewed by [G4/G5 Name]
      - [Timestamp] Note added: "[investigation note text]"
      - [Timestamp] Status changed to [Under Investigation / Cleared / Escalated]
  - **Investigation notes** (rich text editor — G4/G5 can add timestamped notes)
  - **Related flags:** Other flagged actions by the same user in the last 90 days (pattern detection)
  - **Entity history:** Complete audit trail for the affected entity (all actions, not just flagged ones)
- **Footer:** [Mark Cleared] [Escalate to Board] [Add Note] [Assign Investigator]
- **Access:** G4/G5 only

### 6.5 Modal: `alert-settings` (560px, G4/G5 only)

- **Title:** "Audit Alert Settings"
- **Sections:**
  - **Real-time alerts (toggle per flag rule):**
    - [ ] Discount > 25% — WhatsApp + In-App
    - [ ] Payment > Rs. 1L — WhatsApp + In-App
    - [ ] Data export > 100 records — Email + In-App
    - [ ] Bulk operation > 10 records — In-App
    - [ ] Budget increase > 20% — WhatsApp + In-App
    - [ ] After-hours action — Email (daily digest)
    - [ ] Lead deletion — In-App
    - [ ] Policy change — WhatsApp + Email + In-App
    - [ ] Role assignment change — WhatsApp + In-App
    - [ ] Topper data download — In-App
    - [ ] Repeat flagged user — WhatsApp + Email + In-App (immediate)
  - **Digest settings:**
    - Daily summary email: ON/OFF (default ON for G4/G5)
    - Weekly audit digest: ON/OFF
    - Monthly compliance report: ON/OFF
  - **Alert recipients:** Current user + additional G4/G5 users (multi-select)
- **Buttons:** Cancel . Save Settings
- **Access:** G4/G5 only

---

## 7. Charts

### 7.1 Daily Activity Volume (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Daily Audit Actions — Last 30 Days" |
| Data | COUNT(audit_entries) per day |
| X-axis | Date (DD MMM) |
| Y-axis | Action count |
| Colour | `#3B82F6` blue line; flagged actions as red dots overlaid |
| Annotation | Peak admission months (Feb-Apr) typically show 2-3x normal volume |
| Tooltip | "[Date]: [N] total actions, [M] flagged" |
| API | `GET /api/v1/group/{id}/marketing/admin/audit-log/analytics/daily-volume/` |

### 7.2 Action Category Distribution (Doughnut)

| Property | Value |
|---|---|
| Chart type | Doughnut (Chart.js 4.x) |
| Title | "Actions by Category — Last 30 Days" |
| Data | COUNT per action category |
| Colour | Lead Mgmt `#3B82F6`, Campaign Ops `#6366F1`, Financial `#F59E0B`, Content `#8B5CF6`, Access `#F43F5E`, Configuration `#64748B` |
| Centre text | Total action count |
| Tooltip | "[Category]: [N] actions ([X]%)" |
| API | `GET /api/v1/group/{id}/marketing/admin/audit-log/analytics/by-category/` |

### 7.3 Top Users by Action Count (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Top 10 Users by Activity — Last 30 Days" |
| Data | COUNT per user, top 10 |
| X-axis | Action count |
| Y-axis | User name + role badge |
| Colour | Standard blue; red border if user has any flagged actions |
| Tooltip | "[User] ([Role]): [N] actions, [M] flagged" |
| API | `GET /api/v1/group/{id}/marketing/admin/audit-log/analytics/top-users/` |

### 7.4 Flagged Actions Trend (Stacked Bar)

| Property | Value |
|---|---|
| Chart type | Stacked bar (Chart.js 4.x) |
| Title | "Flagged Actions by Risk Level — Last 12 Weeks" |
| Data | COUNT flagged actions per week, stacked by risk level |
| X-axis | Week number (W1, W2, ... W12) |
| Y-axis | Count |
| Colour | Critical `#DC2626`, High `#EF4444`, Medium `#F59E0B`, Low `#FBBF24` |
| Tooltip | "Week [N]: [X] critical, [Y] high, [Z] medium, [W] low" |
| API | `GET /api/v1/group/{id}/marketing/admin/audit-log/analytics/flagged-trend/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Filter applied | "Showing [N] entries matching filters" | Info | 2s |
| Flag reviewed | "Flagged action marked as reviewed — [Cleared/Escalated/Under Investigation]" | Success | 3s |
| Investigation note added | "Investigation note saved for [Entity]" | Success | 3s |
| Alert settings saved | "Audit alert settings updated" | Success | 3s |
| Export started | "Generating audit report — [N] entries. You'll be notified when ready." | Info | 4s |
| Export ready | "Audit report ready for download ([format], [size])" | Success | 5s |
| Escalated to board | "Flagged action escalated to Board — notification sent to [N] trustees" | Warning | 5s |
| External auditor access granted | "External auditor access granted to [Name] — expires [Date]" | Info | 4s |
| Auto-refresh | "[N] new actions since last refresh" | Info | 2s |
| Saved preset | "Filter preset '[Name]' saved" | Success | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No audit entries (impossible in practice) | 📋 | "No Activity Recorded" | "The audit log will automatically capture all actions across Marketing & Admissions pages." | — |
| No results for current filter | 🔍 | "No Matching Entries" | "No audit entries match your current filters. Try broadening the date range or removing filters." | Clear Filters |
| No flagged actions | ✅ | "No Flagged Actions" | "No high-risk actions detected in the selected period. All operations within normal parameters." | — |
| No entries for selected user | 👤 | "No Activity for [User]" | "This user has no recorded actions in the selected date range." | Expand Date Range |
| External auditor — no access yet | 🔒 | "Access Not Configured" | "External auditor access must be granted by the Chairman (G5) with an explicit expiry date." | Request Access |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + filter bar + table skeleton (15 rows) |
| Tab switch | Content skeleton matching target tab layout |
| Action detail drawer | 720px right-slide skeleton: summary card + before/after table + related actions |
| Advanced filter modal | Form skeleton with filter group sections |
| Export generation | Progress bar: "Processing [N] entries..." with percentage |
| Flag investigation drawer | 640px skeleton: flag summary + timeline + notes editor |
| Chart load | Grey canvas placeholder with axis labels |
| Auto-refresh (30s) | Subtle shimmer on table header only (no full skeleton — avoid layout shift) |
| Filter apply | Table body skeleton (15 rows) with filter bar remaining visible |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/` | G1+ | List audit entries (paginated, filterable); G3 users filtered to own + direct reports |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/{entry_id}/` | G1+ | Single audit entry detail with before/after values |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/kpis/` | G1+ | KPI values for summary bar |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/flagged/` | G4+ | List flagged actions (paginated, filterable by risk level, investigation status) |
| PATCH | `/api/v1/group/{id}/marketing/admin/audit-log/flagged/{entry_id}/review/` | G4+ | Update investigation status (Cleared/Under Investigation/Escalated) |
| POST | `/api/v1/group/{id}/marketing/admin/audit-log/flagged/{entry_id}/notes/` | G4+ | Add investigation note to flagged entry |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/users/` | G1+ | User activity summary (aggregated counts per user) |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/users/{user_id}/` | G1+ | Detailed activity for a specific user (respects role visibility) |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/entity/{entity_type}/{entity_id}/` | G1+ | Complete audit history for a specific entity |
| POST | `/api/v1/group/{id}/marketing/admin/audit-log/export/` | G1+ | Generate audit report export (async — returns job ID) |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/export/{job_id}/` | G1+ | Check export status / download completed export |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/analytics/daily-volume/` | G1+ | Daily action count for line chart |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/analytics/by-category/` | G1+ | Action category distribution for doughnut |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/analytics/top-users/` | G1+ | Top 10 users by action count |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/analytics/flagged-trend/` | G4+ | Weekly flagged actions trend |
| GET | `/api/v1/group/{id}/marketing/admin/audit-log/alert-settings/` | G4+ | Get current user's alert settings |
| PUT | `/api/v1/group/{id}/marketing/admin/audit-log/alert-settings/` | G4+ | Update alert settings |
| POST | `/api/v1/group/{id}/marketing/admin/audit-log/external-access/` | G5 | Grant time-limited external auditor access |
| DELETE | `/api/v1/group/{id}/marketing/admin/audit-log/external-access/{access_id}/` | G5 | Revoke external auditor access |

> **Note:** There are deliberately NO POST/PUT/DELETE endpoints for audit entries themselves. Audit entries are created exclusively by system-level triggers when any action occurs across Division O pages. This ensures immutability — no human can create, modify, or delete an audit record.

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../admin/audit-log/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#audit-content` | `innerHTML` | `hx-trigger="click"` |
| Activity log load | Tab 1 active | `hx-get=".../admin/audit-log/?page=1"` | `#audit-table-body` | `innerHTML` | `hx-trigger="load"` |
| Auto-refresh | Timer | `hx-get=".../admin/audit-log/?since={last_timestamp}"` | `#audit-table-body` | `afterbegin` | `hx-trigger="every 30s"` — prepends new entries; counter badge shows "[N] new" |
| Filter apply | Filter controls | `hx-get` with query params | `#audit-table-body` | `innerHTML` | `hx-trigger="change"` for dropdowns; `hx-trigger="keyup changed delay:300ms"` for search |
| Advanced filter | Filter form submit | `hx-get` with all filter params | `#audit-table-body` | `innerHTML` | Closes modal, applies filters |
| Action detail drawer | Row click | `hx-get=".../admin/audit-log/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Flag review | Review form submit | `hx-patch=".../admin/audit-log/flagged/{id}/review/"` | `#flag-row-{id}` | `outerHTML` | Updates investigation status badge in-place |
| Add investigation note | Note form submit | `hx-post=".../admin/audit-log/flagged/{id}/notes/"` | `#investigation-timeline` | `beforeend` | Appends note to timeline |
| Export trigger | Export form submit | `hx-post=".../admin/audit-log/export/"` | `#export-status` | `innerHTML` | Shows progress bar; polls for completion |
| Export poll | Auto | `hx-get=".../admin/audit-log/export/{job_id}/"` | `#export-status` | `innerHTML` | `hx-trigger="every 3s [status != 'complete']"` — stops polling when done |
| User activity drill | User name click | `hx-get=".../admin/audit-log/users/{user_id}/"` | `#right-drawer` | `innerHTML` | Opens user activity drawer |
| Entity history | Entity link click | `hx-get=".../admin/audit-log/entity/{type}/{id}/"` | `#right-drawer` | `innerHTML` | Full entity audit trail in drawer |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#audit-table-body` | `innerHTML` | 50/page for activity log; 25/page for flagged |
| Alert settings save | Settings form | `hx-put=".../admin/audit-log/alert-settings/"` | `#alert-result` | `innerHTML` | Toast on success |

---

*Page spec version: 1.0 . Last updated: 2026-03-26*
