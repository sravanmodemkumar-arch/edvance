# 18 — Visitor Management Log

> **URL:** `/group/welfare/security/visitors/`
> **File:** `18-visitor-management-log.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group CCTV & Security Head (Role 93, G3)

---

## 1. Purpose

Group-wide visitor management system tracking all visitor entries across all branches. All visitors must be logged at the gate: name, ID proof type and number, person being visited, purpose, date/time in, and date/time out. For hostel blocks: additional parent/guardian verification is required against the registered guardian list — only registered guardians may visit hostelers; no unregistered visitor may enter hostel blocks.

The Group CCTV & Security Head uses this page to: set visitor policy standards applicable to all branches, review any branch deviations from policy, investigate incidents involving visitors, audit log completeness (branches that have not logged any visitors for more than 3 days are likely not complying with the entry logging requirement), and flag unauthorised hostel visitor attempts.

Scale: 50–500 visitors per branch per week · 1,000–25,000 visitor entries per month across all branches.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group CCTV & Security Head | G3 | Full — view all branches, set policies, flag incidents, export | Primary owner |
| Group COO | G4 | View — KPI summary and branch non-compliance flags only; read-only | Cannot edit records or set policies |
| Branch Security Supervisor | G2 | View own branch visitor log; can log new visitors and sign out visitors for own branch | Cannot access other branches or set policies |
| Branch Principal | G2 | View — own branch summary: today's count, overstays, hostel compliance | Read-only; no individual visitor details |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('cctv_security_head', 'branch_security_supervisor')` with branch-scope filter for G2. ID number field masked to last 4 digits for all roles except G3.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Security  ›  Visitor Management Log
```

### 3.2 Page Header
```
Visitor Management Log                  [Policy Manager ⚙]  [Export Log ↓]  [Flag Incident]
[Group Name] — Group CCTV & Security Head · Last refreshed: [timestamp]
[N] Visitors Today (All Branches)  ·  [N] Still On Campus  ·  [N] Overstays  ·  [N] Branches Not Logged Today
```

### 3.3 Alert Banner (conditional — policy violations and non-compliance)

| Condition | Banner Text | Severity |
|---|---|---|
| Unauthorised hostel entry attempt | "Unauthorised hostel entry attempt logged at [Branch] — Visitor: [Name], attempted to access [Hostel Block] at [time]. Guard: [Name]." | Red |
| Visitor overstay > 3 hours past expected exit | "Visitor [Name] at [Branch] has been on campus for [N] hours with no sign-out recorded. Expected out by [time]." | Red |
| Branch not logged any visitor > 3 days | "[N] branch(es) have no visitor log entries for more than 3 consecutive days — possible non-compliance: [Branch list]." | Amber |
| Visitor still on campus after 10PM | "Visitor [Name] is still recorded as on campus at [Branch] after 10:00 PM. Security check required." | Red |
| Hostel visitor without pre-approval | "Visitor [Name] accessed [Hostel Block] at [Branch] without pre-approval. Review required." | Amber |

Max 5 alerts visible. Alert links route to the specific visitor record or branch log. "View full visitor incident history →" shown below alerts.

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Visitors Today (All Branches) | Total visitor entries logged today across all branches | Blue always (informational) | → Main table filtered to today |
| Hostel Visitor Compliance % | Hostel visitor entries with pre-approval verified / total hostel entries × 100 | Green = 100% · Yellow 90–99% · Red < 90% | → Main table filtered to Campus Area = Hostel Block |
| Overstay Incidents This Month | Visitor entries where time-out not recorded within 2 hours of expected exit | Green = 0 · Yellow 1–5 · Red > 5 | → Main table filtered to Status = Overstay |
| Branches with No Log Today | Branches that have zero visitor entries for today (non-compliance flag) | Green = 0 · Yellow 1–3 · Red > 3 | → Section 5.2 |
| Unauthorised Hostel Entry Attempts | Visitor entries flagged as unauthorised hostel access attempt (this month) | Green = 0 · Red if any | → Main table filtered to unauthorised flag |
| Visitors Still On Campus | Entries with Time In recorded but no Time Out | Green = 0–10 · Yellow 11–30 · Red > 30 | → Main table filtered to Status = Still In |
| Avg Daily Visitors (7-Day Rolling) | Average daily visitor count across all branches, last 7 days | Blue always (informational) | → Section 5.3 chart |
| Log Completeness This Week | Branches that logged visitors at least once each day this week / total branches × 100 | Green ≥ 90% · Yellow 70–89% · Red < 70% | → Section 5.2 |

**HTMX:** `hx-trigger="every 3m"` → Visitors Today, Visitors Still On Campus, and Branches with No Log Today auto-refresh.

---

## 5. Sections

### 5.1 Visitor Log Table (Primary Table)

> Complete log of all visitor entries across all branches.

**Search:** Visitor name, ID number (last 4 digits), person visited, branch name. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Date Range | Date range picker | Default: Today; max range 90 days |
| Campus Area | Checkbox | Main Gate / Hostel Block / Admin / Sports Block / Other |
| Status | Checkbox | Signed Out / Still In / Overstay |
| Purpose Category | Checkbox | Parent Meeting / Guardian Visit (Hostel) / Official / Vendor / Interview / Other |
| Overstay Flag | Toggle | Show only overstay entries |
| Unauthorised Hostel Flag | Toggle | Show only flagged unauthorised hostel entries |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Date | ✅ | Date of visit |
| Time In | ✅ | HH:MM format |
| Time Out | ✅ | HH:MM or "—" if not signed out; Red if overdue |
| Visitor Name | ✅ | Full name; link → `visitor-detail` drawer |
| ID Type | ✅ | Aadhar / PAN / Passport / Driving Licence / Voter ID |
| ID Number | ❌ | Last 4 digits shown (e.g., ●●●●●●4521); full number visible to G3 only |
| Branch | ✅ | Branch name |
| Campus Area | ✅ | Badge: Main Gate (Blue) · Hostel Block (Purple) · Admin (Grey) · Other |
| Person Visited | ✅ | Name of staff/student being visited |
| Purpose | ✅ | Purpose category badge |
| Guard On Duty | ✅ | Guard name at time of entry |
| Status | ✅ | Signed Out (Green) / Still In (Blue) / Overstay (Red) |
| Actions | ❌ | View · Sign Out · Flag Incident |

**Default sort:** Date descending, then Time In descending (most recent first).
**Pagination:** Server-side · 25/page.

---

### 5.2 Branch Log Compliance Panel

> Branch-by-branch overview of visitor log completeness and compliance metrics.

**Display:** Table.

**Columns:**
| Column | Notes |
|---|---|
| Branch | Branch name |
| Today's Entries | Count of visitor entries logged today |
| Last Log Date | Date of most recent any visitor entry; Red if > 3 days ago |
| Days Since Last Log | Number of days; Red if > 3 |
| Overstays This Week | Count; Red if > 2 |
| Hostel Compliance % | Hostel entries with pre-approval / total hostel entries this week × 100 |
| Log Compliance Status | Green: Logged within last 3 days · Red: No log > 3 days · Grey: No hostel (N/A for hostel metric) |
| Actions | View Branch Log · Send Compliance Reminder |

**Default sort:** Days Since Last Log descending (most non-compliant first).
**Pagination:** Server-side · 25/page.

---

### 5.3 Charts

**Chart 1 — Bar Chart: Daily Visitor Volume per Branch (7-day rolling)**
- X-axis: Last 7 days (date labels).
- Y-axis: Visitor count.
- Grouped bars: one bar per branch per day (stacked if > 10 branches; show top-10 and "Others" group).
- Tooltip: Date · Branch · Count.

**Chart 2 — Pie Chart: Visitor Purpose Distribution**
- Segments: Parent Meeting / Guardian Visit (Hostel) / Official / Vendor / Interview / Other.
- Period: Current month, all branches.
- Centre label: Total visitors this month.
- Tooltip: Purpose · Count · % of total.

---

## 6. Drawers / Modals

### 6.1 Drawer: `visitor-detail`
- **Trigger:** Visitor Name link in Section 5.1 table
- **Width:** 560px

**Content:**
| Field | Notes |
|---|---|
| Visitor Entry ID | System-generated |
| Branch | Read-only |
| Date | Read-only |
| Time In | Read-only |
| Time Out | Read-only (or "Not yet signed out") |
| Duration On Campus | Calculated: Time Out − Time In; or "Still on campus — [N] hours [M] minutes" |
| Visitor Name | Read-only |
| ID Type | Read-only |
| ID Number | Full number visible to G3 only; masked to last 4 for G2 |
| Campus Area | Read-only badge |
| Person Visited | Full name |
| Department / Class | Department or class of person visited |
| Purpose | Read-only category |
| Purpose Details | Freetext notes added by guard at entry |
| Guard On Duty | Guard name + shift |
| Hostel Pre-Approval | Yes / No / N/A — with guardian verification status if applicable |
| Registered Guardian | If hostel visit: name and relationship from guardian list (Verified ✅ / Not on list ❌) |
| Status | Signed Out / Still In / Overstay badge |
| Guard Exit Notes | Notes added at sign-out (if any) |
| Incident Flag | Yes (Red) / No — link to incident record if flagged |
| Guard Notes | Any freetext notes added by guard |

**Actions (G3 only):**
- [Sign Out Visitor] — records current timestamp as Time Out (for "Still In" records only)
- [Flag as Incident] — opens `flag-incident` drawer prefilled with this entry
- [Mark as Unauthorised Hostel Entry] — quick flag for hostel compliance tracking

---

### 6.2 Drawer: `policy-manager`
- **Trigger:** [Policy Manager ⚙] button in page header
- **Width:** 640px
- **Tabs:** General Rules · Hostel Visitor Rules · ID Requirements · Reporting

**General Rules tab:**
| Field | Type | Validation |
|---|---|---|
| Permitted Visitor Hours (Weekdays) | Time range picker | Required; e.g., 08:00 AM – 05:00 PM |
| Permitted Visitor Hours (Weekends) | Time range picker | Required |
| Maximum Stay Duration (hours) | Number · 1–12 | Required; default 2 hours |
| Overstay Alert After (hours) | Number · 1–6 | Required; default 2 hours |
| Apply to All Branches | Toggle | ON: applies group-wide; OFF: per-branch override enabled |
| Branch-Specific Overrides | Expandable section — list branches with customised rules (visible only if above toggle is OFF) | — |

**Hostel Visitor Rules tab:**
| Field | Type | Validation |
|---|---|---|
| Require Pre-Approval for Hostel Visitors | Toggle | Default: ON; Required |
| Pre-Approval Required From | Radio | Hostel Warden / Branch Principal / Either | Required |
| Pre-Approval Notice Period (hours) | Number · 0–48 | Default: 24 hours; 0 means same-day allowed |
| Only Registered Guardians Allowed | Toggle | Default: ON; when ON, system checks visitor against guardian registry |
| Permitted Hostel Visit Hours | Time range picker | Required; e.g., 10:00 AM – 04:00 PM |
| Girls Hostel — Female Visitors Only | Toggle | Default: OFF (male relatives may be permitted) |
| Document Check Required | Checkbox | ID proof · Guardian verification letter · Both |

**ID Requirements tab:**
| Field | Type | Validation |
|---|---|---|
| Accepted ID Types | Multi-select checkbox | Aadhar / PAN / Passport / Driving Licence / Voter ID |
| ID Required for All Visitors | Toggle | Default: ON; Required |
| ID Photocopy Required | Toggle | Default: OFF |

**Reporting tab:**
| Field | Type | Validation |
|---|---|---|
| Non-Compliance Alert Threshold (days without log) | Number · 1–7 | Default: 3 days; Required |
| Auto-Notify Branch Principal on Non-Compliance | Toggle | Default: ON |
| Auto-Notify Group COO on Incident Flag | Toggle | Default: ON |
| Weekly Visitor Report Recipients | Email list | Comma-separated email addresses |

**Footer:** [Cancel] [Save Policy →]

---

### 6.3 Drawer: `flag-incident`
- **Trigger:** [Flag Incident] button in page header, or "Flag Incident" action in table row, or button in `visitor-detail` drawer
- **Width:** 440px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Visitor Entry ID | Read-only pre-filled (or searchable if opened from header) | — |
| Branch | Read-only pre-filled | — |
| Visitor Name | Read-only pre-filled | — |
| Incident Type | Select | Unauthorised Entry Attempt / Overstay — Refused to Leave / Suspicious Behaviour / Verbal Altercation / Unauthorised Hostel Access / Visitor Used Fake ID / Other · Required |
| Incident Severity | Radio | Low / Medium / High / Critical · Required |
| Incident Description | Textarea · max 600 chars | Required · min 50 chars |
| CCTV Reference | Text · max 100 chars | Optional; camera ID + timestamp (e.g., "CAM-BRN-042 · 2026-03-21 14:32") |
| Guard On Duty | Read-only pre-filled (from visitor entry) | — |
| Additional Guards Involved | Text · max 200 chars | Optional |
| Immediate Action Taken | Textarea · max 400 chars | Required |
| Police Reported | Toggle | Default: OFF |
| Police Station | Text · max 100 chars | Required if Police Reported = ON |
| FIR Number | Text · max 50 chars | Optional; conditional on Police Reported = ON |
| Link to Security Incident Register | Checkbox | "Also log this in the Security Incident Register (Page 19)" · Default: ON for High/Critical severity |

**Validation:**
- Incident Description minimum 50 characters.
- If Severity is Critical, "Link to Security Incident Register" is forced ON and cannot be unchecked.
- If Police Reported is ON, Police Station is required.

**Footer:** [Cancel] [Flag Incident →]

**On submit:** POST to visitor incident endpoint · if linked to incident register, auto-creates incident record in Page 19 register with cross-reference · toast warning · visitor entry row updated with incident flag badge.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Visitor signed out | "Visitor [Name] signed out at [Branch] at [time]." | Success | 3s |
| Incident flagged | "Security incident flagged for visitor [Name] at [Branch]. Incident ID: [ID]." | Warning | 6s |
| Incident linked to register | "Incident also logged in Security Incident Register as [Incident ID]." | Info | 5s |
| Policy saved | "Visitor policy updated and applied to [all branches / [Branch name]]." | Success | 4s |
| Compliance reminder sent | "Visitor log compliance reminder sent to Branch Principal at [Branch]." | Info | 4s |
| Log exported | "Visitor log export is being prepared. Download will begin shortly." | Info | 4s |
| Unauthorised hostel flag set | "Visitor entry [ID] flagged as unauthorised hostel access attempt." | Warning | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No visitor entries today | "No Visitors Logged Today" | "No visitor entries have been logged for today across all branches." | — |
| No entries for selected filters | "No Visitor Records Found" | "No visitor entries match the selected date range, branch, or filters." | [Clear Filters] |
| No overstays | "No Overstay Incidents" | "No visitors are currently overstaying or have overstayed this month." | — |
| No hostel compliance violations | "Hostel Visitor Compliance at 100%" | "All hostel visitor entries this week have pre-approval verified." | — |
| All branches logging visitors | "All Branches Compliant" | "All branches have logged visitor entries within the last 3 days." | — |
| No incident flags | "No Flagged Incidents" | "No visitor entries have been flagged as security incidents this month." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + visitor log table (15 rows × 12 columns) + branch compliance panel + chart areas + alerts |
| Table filter/search | Inline skeleton rows (8 rows × 12 columns) |
| KPI auto-refresh | Shimmer on Visitors Today, Still On Campus, Branches No Log Today card values |
| Visitor detail drawer open | 560px drawer skeleton with all field rows |
| Policy manager drawer open | 640px drawer skeleton with 4-tab bar; each tab loads lazily |
| Flag incident drawer open | 440px drawer with 12 field skeletons |
| Branch compliance panel | Table skeleton (10 rows × 8 columns) |
| Bar chart load | Chart area skeleton (full-width, 240px tall, animated shimmer) |
| Pie chart load | Circle skeleton (200px diameter, animated shimmer) |

---

## 10. Role-Based UI Visibility

| Element | CCTV & Security Head G3 | Group COO G4 | Branch Security Supervisor G2 | Branch Principal G2 |
|---|---|---|---|---|
| View All Branches Log | ✅ | ❌ (KPI + non-compliance only) | Own branch only | Own branch summary only |
| View Full ID Number | ✅ | ❌ | ❌ (last 4 only) | ❌ |
| Sign Out Visitor | ✅ | ❌ | ✅ (own branch) | ❌ |
| Flag Incident | ✅ | ❌ | ✅ (own branch) | ❌ |
| Policy Manager | ✅ | ❌ | ❌ | ❌ |
| Mark Unauthorised Hostel | ✅ | ❌ | ✅ (own branch) | ❌ |
| View Hostel Pre-Approval Details | ✅ | ❌ | ✅ (own branch) | ❌ |
| Send Compliance Reminder | ✅ | ❌ | ❌ | ❌ |
| Export Log | ✅ | ✅ (aggregate) | ✅ (own branch) | ❌ |
| KPI Summary Bar | ✅ (all cards) | ✅ (Branches No Log + Overstay) | ✅ (own branch metrics) | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/security/visitors/` | JWT (G3+) | Visitor log table; params: `branch_id`, `date_from`, `date_to`, `area`, `status`, `purpose`, `overstay`, `unauthorised_hostel`, `q`, `page` |
| GET | `/api/v1/group/{group_id}/welfare/security/visitors/kpi-cards/` | JWT (G3+) | KPI auto-refresh payload |
| GET | `/api/v1/group/{group_id}/welfare/security/visitors/branch-compliance/` | JWT (G3+) | Branch log compliance panel |
| GET | `/api/v1/group/{group_id}/welfare/security/visitors/charts/daily-volume/` | JWT (G3+) | 7-day rolling daily volume bar chart data |
| GET | `/api/v1/group/{group_id}/welfare/security/visitors/charts/purpose-distribution/` | JWT (G3+) | Purpose distribution pie chart data |
| GET | `/api/v1/group/{group_id}/welfare/security/visitors/{entry_id}/` | JWT (G3+) | Single visitor entry detail drawer payload |
| POST | `/api/v1/group/{group_id}/welfare/security/visitors/{entry_id}/sign-out/` | JWT (G3, G2-branch) | Record visitor sign-out timestamp |
| POST | `/api/v1/group/{group_id}/welfare/security/visitors/{entry_id}/flag-incident/` | JWT (G3, G2-branch) | Flag visitor entry as security incident |
| GET | `/api/v1/group/{group_id}/welfare/security/visitors/policy/` | JWT (G3) | Get current visitor policy settings |
| PUT | `/api/v1/group/{group_id}/welfare/security/visitors/policy/` | JWT (G3) | Save visitor policy settings |
| GET | `/api/v1/group/{group_id}/welfare/security/visitors/export/` | JWT (G3+) | Async export of visitor log (CSV/XLSX) |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 3m` | GET `.../visitors/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Visitor log search | `input delay:300ms` | GET `.../visitors/?q={val}` | `#visitor-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../visitors/?{filters}` | `#visitor-table-section` | `innerHTML` |
| Date range change | `change` | GET `.../visitors/?date_from={d1}&date_to={d2}` | `#visitor-table-section` | `innerHTML` |
| Overstay toggle | `change` | GET `.../visitors/?overstay=true` | `#visitor-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../visitors/?page={n}` | `#visitor-table-section` | `innerHTML` |
| Open visitor detail drawer | `click` on Visitor Name | GET `.../visitors/{id}/` | `#drawer-body` | `innerHTML` |
| Sign out visitor | `click` | POST `.../visitors/{id}/sign-out/` | `#visitor-row-{id}` | `outerHTML` |
| Flag incident submit | `click` | POST `.../visitors/{id}/flag-incident/` | `#visitor-row-{id}` | `outerHTML` |
| Policy manager save | `click` | PUT `.../visitors/policy/` | `#policy-status-bar` | `innerHTML` |
| Branch compliance panel load | `load` | GET `.../visitors/branch-compliance/` | `#compliance-panel` | `innerHTML` |
| Daily volume chart load | `load` | GET `.../visitors/charts/daily-volume/` | `#daily-volume-chart` | `innerHTML` |
| Purpose chart load | `load` | GET `.../visitors/charts/purpose-distribution/` | `#purpose-chart` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
