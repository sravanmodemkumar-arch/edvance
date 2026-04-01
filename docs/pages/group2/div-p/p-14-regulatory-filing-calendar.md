# P-14 — Regulatory Filing Calendar

> **URL:** `/group/audit/regulatory/filings/`
> **File:** `p-14-regulatory-filing-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Affiliation Compliance Officer (Role 125, G1) — primary operator

---

## 1. Purpose

The Regulatory Filing Calendar tracks every mandatory filing, return, and submission that the Institution Group's branches must make to government bodies, education boards, regulatory authorities, and statutory agencies. In Indian education, the number of regulatory filings is staggering — a single CBSE-affiliated school must submit UDISE+ data (October), AISHE returns (February, if offering higher education), RTE compliance returns (quarterly in some states), fire safety renewal applications (annual), building stability certificate renewal (every 5 years), state education department returns (annual), income tax returns (annually for the trust), GST returns (monthly/quarterly), EPF/ESI returns (monthly), professional tax (half-yearly), and more. A 30-branch group is tracking 300–500 individual filings per year.

The problems this page solves:

1. **Deadline invisibility:** Each filing has a different deadline, different frequency, and different authority. Branch principals know about some deadlines (UDISE+ because CBSE sends reminders) but miss others (building stability certificate renewal has no reminder system — the school must track it themselves). The calendar consolidates ALL deadlines across ALL branches into a single view.

2. **Penalty exposure:** Missing the UDISE+ deadline means the school's data is not reflected in government statistics — affecting grant allocation. Missing RTE returns can lead to ₹1 lakh/day penalty. Missing fire safety NOC renewal means the school is technically operating without fire clearance — criminal liability for the chairman. Missing GST returns means ₹50/day late fee + interest. The platform shows penalty implications for each filing.

3. **Multi-branch multiplication:** A filing that's due once a year becomes 30 filings when the group has 30 branches. The UDISE+ submission window is September–October — during the same 6-week window, the compliance officer must ensure 30 branches have submitted their data. The calendar shows filing status per branch with branch-level tracking.

4. **Filing dependencies:** Some filings depend on others — AISHE requires UDISE+ code, CBSE affiliation renewal requires fire NOC + building stability certificate + audited accounts. The platform maps these dependencies so a delayed upstream filing triggers alerts for all dependent filings.

5. **State-specific variations:** Education regulation varies by state. In Telangana, the school recognition renewal process differs from Andhra Pradesh. In Maharashtra, fire safety NOC follows a different protocol than in Karnataka. The calendar supports state-specific filing templates.

**Scale:** 5–50 branches · 15–25 filing types per branch · 300–500 total filings per year · 12 regulatory authorities · State-specific variations across 5–10 states

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Affiliation Compliance Officer | 125 | G1 | Full — manage filings, track status, set reminders | Primary operator |
| Group Internal Audit Head | 121 | G1 | Read — filing compliance in audit scope | Cross-functional |
| Group Inspection Officer | 123 | G3 | Read + Update — verify filings during branch visits | Field verification |
| Group ISO / NAAC Coordinator | 124 | G1 | Read — regulatory filings as quality evidence | Coordination |
| Group Compliance Data Analyst | 127 | G1 | Read — filing metrics for MIS | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read + CAPA — overdue filings become CAPA items | Remediation |
| Group CEO / Chairman | — | G4/G5 | Read — filing compliance oversight | Executive |
| Branch Principal | — | G3 | Read (own branch) + Update status (own branch) | Branch-level execution |
| Branch Admin / Accountant | — | G2 | Read (own branch) + Upload proof | Supports filing execution |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Branch staff see only own branch filings. Status update: 125, 123, Branch Principal. Filing template management: 125, G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Regulatory Filings
```

### 3.2 Page Header
```
Regulatory Filing Calendar                       [+ Add Filing]  [Import Filing Template]  [Export]
Affiliation Compliance Officer — S. Padmavathi
Sunrise Education Group · 28 branches · 412 filings this FY · 38 due in next 30 days · 3 overdue
```

### 3.3 Filter Bar
```
Branch: [All / Select ▼]    Authority: [All / CBSE / State Board / RTE / Fire Dept / Municipal / Tax / Labour ▼]
Category: [All / Education / Safety / Financial / Labour / Infrastructure ▼]
Status: [All / Upcoming / Due Soon / Overdue / Completed / Not Applicable ▼]
Frequency: [All / One-time / Monthly / Quarterly / Half-yearly / Annual / Multi-year ▼]
FY: [2025-26 ▼]                                                                    [Reset Filters]
```

### 3.4 KPI Summary Bar

| # | KPI | Source | Colour Logic |
|---|---|---|---|
| 1 | Total Filings (FY) | Count of all filings for current FY | Neutral blue |
| 2 | Completed | Count with status = Completed | Neutral green |
| 3 | Due in 30 Days | Filings due within next 30 days | ≤ 5 green · 6–15 amber · > 15 red |
| 4 | Due in 7 Days | Filings due within next 7 days (urgent) | 0 green · 1–3 amber · > 3 red |
| 5 | Overdue | Past deadline, not completed | 0 green · 1–3 amber · > 3 red |
| 6 | Compliance Rate | % completed on time / total due so far | ≥ 95% green · 80–94% amber · < 80% red |
| 7 | Penalty Exposure | Estimated penalty for overdue filings | ₹0 green · ₹1–50K amber · > ₹50K red |
| 8 | Branches 100% Current | Branches with zero overdue filings | = total green · else amber |

### 3.5 Tab Navigation

```
[Calendar View]    [Filing List]    [Branch Status Matrix]    [Filing Templates]
```

---

### Tab 1 — Calendar View (default)

FullCalendar.js month view showing all filing deadlines.

**Calendar event types:**

| Event Type | Colour | Meaning |
|---|---|---|
| 🔴 Red | Overdue | Past deadline, not completed |
| 🟠 Orange | Due ≤ 7 days | Filing due within 7 days |
| 🟡 Yellow | Due ≤ 30 days | Filing due within 30 days |
| 🟢 Green | Completed | Filed on or before deadline |
| 🔵 Blue | Upcoming (> 30 days) | Future filing |
| ⚫ Grey | Not Applicable | Filing not required for this branch |

**Event label format:** `[Authority] Filing Name — Branch (N branches)`

When multiple branches have the same filing due on the same date, they collapse into one event with branch count: `[CBSE] UDISE+ Submission — 28 branches`.

**Event click:** Opens Filing Detail Drawer.

**Right sidebar panel:**

**Urgency Summary:**
```
🔴 Overdue (3)
  • Fire NOC Renewal — Sunrise Miyapur — 12 days overdue
  • Trade Licence — Sunrise Kukatpally — 5 days overdue
  • EPF Return (Feb) — Sunrise Begumpet — 3 days overdue

🟠 Due This Week (5)
  • GST Return (Mar) — All branches — due 20-Mar-2026
  • UDISE+ Correction Window — 8 branches — due 22-Mar-2026
  ...

🟡 Due This Month (15)
  ...
```

Each item is clickable → opens Filing Detail Drawer.

---

### Tab 2 — Filing List

Flat table of all filings with comprehensive column detail.

**Table columns:**

| # | Column | Width | Content |
|---|---|---|---|
| 1 | Filing Name | 200px | e.g., "UDISE+ Data Submission" |
| 2 | Authority | 120px | CBSE / State Education Dept / Fire Dept / Municipal Corp / Income Tax / EPFO |
| 3 | Category | 100px | Education / Safety / Financial / Labour / Infrastructure |
| 4 | Branch | 140px | Branch name (or "All 28 branches" for group-level filings) |
| 5 | Frequency | 80px | Monthly / Quarterly / Annual / One-time / Multi-year |
| 6 | Deadline | 100px | dd-MMM-yyyy · red if overdue · amber if ≤ 30 days |
| 7 | Days Remaining | 80px | "+5 days" (green) or "-12 days" (red for overdue) |
| 8 | Status | 90px | Badge: Completed (green) · In Progress (blue) · Not Started (grey) · Overdue (red) |
| 9 | Filed Date | 90px | When actually filed (if completed) |
| 10 | Proof | 60px | 📎 icon if proof uploaded, ❌ if not |
| 11 | Penalty | 100px | Penalty for non-compliance (e.g., "₹50/day", "Affiliation risk") |
| 12 | Assigned To | 110px | Person responsible |
| 13 | Actions | 80px | [Update] · [Upload Proof] |

**Sorting:** By deadline (soonest first, default), status, branch, category.

**Bulk actions toolbar:**
```
☐ Select All    [Mark as Completed]  [Assign To]  [Export Selected]
```

**Pagination:** 50 rows per page.

---

### Tab 3 — Branch Status Matrix

Matrix view: branches as rows, filing types as columns. Shows which filings each branch has completed vs pending.

**Matrix structure:**

| Branch | UDISE+ | Fire NOC | Building Cert | GST (Mar) | EPF (Mar) | RTE Return (Q4) | Trade Licence | … | Completion % |
|---|---|---|---|---|---|---|---|---|---|
| Sunrise Begumpet | ✅ | ✅ | ✅ | ⏳ Due 20-Mar | ❌ Overdue | ✅ | ✅ | … | 85% |
| Sunrise Kukatpally | ✅ | ✅ | ⚠️ Due Apr | ⏳ Due 20-Mar | ✅ | ✅ | ❌ Overdue | … | 78% |
| Sunrise Miyapur | ✅ | ❌ Overdue | ✅ | ⏳ Due 20-Mar | ✅ | ⏳ Due 31-Mar | ✅ | … | 72% |

**Cell states:**
- ✅ **Completed** (green) — Filed on time
- ⏳ **Due** (amber) — Due within 30 days, not yet filed
- ❌ **Overdue** (red) — Past deadline
- ➖ **Not Applicable** (grey) — Filing not required for this branch
- 🔵 **In Progress** (blue) — Partially completed

**Cell click:** Opens quick-update popover — mark complete, upload proof, add notes.

**Column summary (bottom row):** Group-wide completion percentage per filing type.

**Row summary (rightmost column):** Branch completion percentage across all filings.

---

### Tab 4 — Filing Templates

Template library defining what filings exist, their deadlines, authorities, and applicability rules.

**Template table:**

| # | Column | Content |
|---|---|---|
| 1 | Filing Name | e.g., "UDISE+ Data Submission" |
| 2 | Authority | CBSE / State Board / Fire / Municipal / Tax |
| 3 | Category | Education / Safety / Financial / Labour |
| 4 | Frequency | Annual / Quarterly / Monthly / One-time |
| 5 | Default Deadline | e.g., "31-Oct every year" or "20th of every month" |
| 6 | Penalty | Description of non-compliance consequence |
| 7 | Applicable To | Rules: "All CBSE branches" / "All branches" / "Colleges only" / "Telangana branches" |
| 8 | Dependencies | Other filings that must be completed first |
| 9 | Documents Required | List of documents needed for filing |
| 10 | Status | Active / Deprecated |
| 11 | Actions | [Edit] · [Duplicate] · [Deactivate] |

**Pre-loaded templates (common Indian education filings):**

| Filing | Authority | Frequency | Deadline | Penalty |
|---|---|---|---|---|
| UDISE+ Data Submission | MHRD / State | Annual | 31-Oct | School data missing from national database; grant allocation affected |
| AISHE Returns | UGC / MHRD | Annual | 28-Feb | College data missing; UGC grant processing delayed |
| RTE Compliance Return | State Education Dept | Quarterly | End of quarter | ₹1,00,000/day penalty for non-compliance |
| Fire Safety NOC Renewal | State Fire Dept | Annual | Before expiry | School cannot operate without valid NOC; criminal liability |
| Building Stability Certificate | Empanelled Structural Engineer | Every 5 years | Before expiry | CBSE affiliation risk; safety liability |
| Trade Licence Renewal | Municipal Corporation | Annual | 31-Mar | Fine + closure notice |
| Income Tax Return (Trust) | Income Tax Dept | Annual | 31-Oct (for trusts) | Late fee ₹5,000; penalty up to ₹10,000; exemption risk |
| GST Returns (GSTR-3B) | GST Council | Monthly | 20th of next month | ₹50/day late fee + 18% interest on tax due |
| EPF Return | EPFO | Monthly | 15th of next month | ₹5,000 damages + interest; prosecution for repeat offenders |
| ESI Return | ESIC | Half-yearly | 12-May / 12-Nov | 12% interest on delayed contribution |
| Professional Tax | State Govt | Half-yearly / Annual | Varies by state | Fine + interest |
| Society Registration Renewal | Registrar of Societies | Every 5 years | Before expiry | Trust/society status lapses; cannot operate |
| FSSAI Licence Renewal | FSSAI | Every 5 years | Before expiry | Cannot operate canteen/mess; fine up to ₹5L |
| Pollution Control Certificate | State PCB | Varies | Before expiry | Closure direction; fine |
| CBSE Affiliation Renewal | CBSE | Every 5 years | 12 months before expiry | Affiliation lapse — students cannot appear for board exams |

**`[+ Add Custom Filing]` button** — for group-specific filings not in the pre-loaded list.

---

## 4. KPI Summary Bar

(Defined in Section 3.4 above)

---

## 5. Sections

| # | Section | Location | Purpose |
|---|---|---|---|
| 1 | Calendar View | Tab 1 | Visual deadline calendar with urgency colour coding |
| 2 | Filing List | Tab 2 | Comprehensive flat list of all filings |
| 3 | Branch Status Matrix | Tab 3 | Branch × filing type completion matrix |
| 4 | Filing Templates | Tab 4 | Master list of filing types with rules and penalties |
| 5 | Filing Detail Drawer | Right drawer | Full filing detail with history and proof |
| 6 | Add/Edit Filing Modal | Modal | Create or modify a filing instance |
| 7 | Bulk Status Update Modal | Modal | Update multiple filings at once |
| 8 | Add Filing Template Modal | Modal | Define a new filing type template |

---

## 6. Drawers & Modals

### Drawer 1 — Filing Detail Drawer (right, 780px)

**Trigger:** Click any filing event on calendar, any row in filing list, or any cell in branch matrix.

**Header:**
```
Filing Detail — UDISE+ Data Submission                         [✕]
Sunrise Begumpet · CBSE · Education · Annual · Due: 31-Oct-2026
```

**Sections within drawer:**

**Section A — Status & Timeline**
```
Status: ✅ Completed
Filed On: 28-Oct-2026 (3 days before deadline)
Filed By: R. Suresh (Branch Principal)
Verified By: S. Padmavathi (Compliance Officer) · 29-Oct-2026
```

Or if overdue:
```
Status: ❌ Overdue — 12 days past deadline
Deadline: 31-Oct-2026
Days Overdue: 12
Penalty Exposure: School data missing from national database; grant allocation affected
Assigned To: R. Suresh (Branch Principal)
Last Reminder: 25-Oct-2026 (no response)
```

**Section B — Filing Details**

| Field | Value |
|---|---|
| Filing Name | UDISE+ Data Submission |
| Authority | MHRD via State Education Department |
| Category | Education |
| Frequency | Annual |
| Deadline | 31-Oct-2026 |
| Applicable Regulation | Section 27 of RTE Act; UDISE+ portal mandatory |
| Branch | Sunrise Begumpet |
| UDISE Code | 36110300501 |
| Filing Portal | udiseplus.gov.in |
| Documents Required | School data (enrolment, infrastructure, teachers), previous year report card |

**Section C — Proof of Filing**
- Uploaded screenshot/PDF of filed return
- Acknowledgement number / reference number
- `[Upload Proof]` `[Download Proof]`

**Section D — History**

| Date | Event | By |
|---|---|---|
| 28-Oct-2026 | Filed — Ack# UDISE/TS/2026/4523 | R. Suresh |
| 29-Oct-2026 | Verified | S. Padmavathi |
| 25-Oct-2026 | Reminder sent | System (auto) |
| 15-Oct-2026 | Reminder sent | System (auto) |
| 01-Oct-2026 | Filing window opened | System |

**Section E — Dependencies**
```
Required for: CBSE Affiliation Renewal (P-11)
Depends on: None
Linked filings: AISHE Returns (if college)
```

**Section F — Actions**
```
[Mark as Completed]  [Upload Proof]  [Send Reminder]  [Reassign]  [Create CAPA]
```

---

### Modal 1 — Add/Edit Filing

**Trigger:** `[+ Add Filing]` button or `[Edit]` from drawer.

**Form fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Filing Template | Dropdown (searchable) | Yes | Select from template library or "Custom" |
| Branch | Dropdown (multi-select or "All") | Yes | Which branches this filing applies to |
| Financial Year | Dropdown | Yes | 2025-26, 2026-27 |
| Deadline | Date picker | Yes | Auto-filled from template; editable |
| Assigned To | Dropdown | Yes | Branch Principal / Admin / Accountant / Compliance Officer |
| Portal URL | URL | No | Where to submit (e.g., udiseplus.gov.in) |
| Login Credentials Reference | Text | No | "Credentials in group password vault — entry #45" (NEVER store actual passwords) |
| Notes | Textarea | No | Special instructions |
| Reminder Schedule | Multi-select | No | 30 days before / 15 days / 7 days / 3 days / 1 day / On deadline |
| Auto-escalation | Checkbox | No | If overdue, escalate to Zone Director → CEO |

**Batch creation:** If "All branches" selected, system creates one filing instance per branch — all sharing the same deadline.

**Actions:** `[Create Filing]` `[Cancel]`

---

### Modal 2 — Bulk Status Update

**Trigger:** Select multiple rows in Tab 2 + `[Mark as Completed]`.

**Content:**
```
Update 12 filings to "Completed"

Filed Date: [Today ▼]  (or custom date picker)
Proof Upload: [Upload ZIP with proof files]  (optional)
Reference Number: [________________]  (optional — applies to all)
Notes: [________________]

⚠️ These filings will be marked as completed:
  • GST Return (Mar) — 28 branches
  • ...

[Confirm]  [Cancel]
```

---

### Modal 3 — Add Filing Template

**Trigger:** `[+ Add Custom Filing]` from Tab 4.

**Form fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Filing Name | Text | Yes | e.g., "Water Quality Test Report" |
| Authority | Text / Dropdown | Yes | Regulatory body |
| Category | Dropdown | Yes | Education / Safety / Financial / Labour / Infrastructure |
| Frequency | Dropdown | Yes | One-time / Monthly / Quarterly / Half-yearly / Annual / Multi-year |
| Default Deadline | Text | Yes | "31-Oct every year" / "20th of every month" / "Before expiry" |
| Penalty for Non-Compliance | Textarea | Yes | What happens if missed |
| Applicable To | Multi-select rules | Yes | "All branches" / "CBSE branches only" / "Colleges only" / State filter |
| Documents Required | Tag input | No | List of required documents |
| Dependencies | Multi-select | No | Other filings that must be done first |
| Portal URL | URL | No | Government portal for submission |
| Reference Regulation | Text | No | Act/section number |

**Actions:** `[Save Template]` `[Cancel]`

---

### Modal 4 — Send Reminder

**Trigger:** `[Send Reminder]` from drawer or urgency sidebar.

**Form:**
```
To:         [R. Suresh (Branch Principal)]  [K. Latha (Admin)]  [+ Add]
Subject:    Auto-filled: "URGENT: UDISE+ Submission Due 31-Oct-2026 — Sunrise Begumpet"
Message:    Auto-template with filing details, deadline, penalty, and portal link
Priority:   [Normal / Urgent / Critical]
Escalate:   ☐ Copy Zone Director   ☐ Copy CEO   ☐ Copy Audit Head
```

**Actions:** `[Send]` `[Cancel]`

---

## 7. Charts

### Chart 1 — Filing Compliance Rate by Month (line)
- **Type:** Line chart (Chart.js 4.x)
- **X-axis:** Months (Apr–Mar, current FY)
- **Y-axis:** Compliance rate (%) — filings completed on time / total due
- **Series:** Group average (solid line) + target (dashed line at 100%)
- **Colour:** Green when ≥ 95%, amber 80–94%, red < 80%
- **Hover:** Month, count completed, count due, rate
- **Location:** Tab 1 sidebar bottom or above calendar
- **API:** `GET /api/v1/group/{id}/audit/regulatory/filings/charts/compliance-rate/`

### Chart 2 — Filings by Category (doughnut)
- **Type:** Doughnut chart (Chart.js 4.x)
- **Segments:** Education (blue), Safety (red), Financial (green), Labour (purple), Infrastructure (orange)
- **Centre text:** Total filings count + overall compliance %
- **Hover:** Category, count, completed count, compliance %
- **Location:** Tab 2 sidebar or KPI expansion
- **API:** `GET /api/v1/group/{id}/audit/regulatory/filings/charts/by-category/`

### Chart 3 — Branch Compliance Heatmap (matrix/heatmap)
- **Type:** Matrix heatmap (Chart.js 4.x with chartjs-chart-matrix plugin)
- **X-axis:** Filing categories
- **Y-axis:** Branches
- **Cell colour:** Green (100% compliant) → Yellow → Red (overdue filings)
- **Purpose:** Instantly identify which branches are falling behind on which filing categories
- **Location:** Tab 3 top
- **API:** `GET /api/v1/group/{id}/audit/regulatory/filings/charts/branch-heatmap/`

### Chart 4 — Overdue Ageing (horizontal bar)
- **Type:** Horizontal bar chart (Chart.js 4.x)
- **X-axis:** Count of overdue filings
- **Y-axis:** Age buckets: 1–7 days, 8–14 days, 15–30 days, 31–60 days, 60+ days
- **Colour:** Amber for 1–14 days, red for 15+ days
- **Purpose:** Shows how old the overdue filings are — fresh overdue vs chronic non-compliance
- **Location:** Tab 2 sidebar or KPI drill-down
- **API:** `GET /api/v1/group/{id}/audit/regulatory/filings/charts/overdue-ageing/`

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Filing marked complete | "UDISE+ Submission for Sunrise Begumpet marked as completed — proof uploaded" | Success (green) |
| Bulk filings completed | "12 filings marked as completed across 28 branches" | Success (green) |
| Filing created | "Fire NOC Renewal filing created for Sunrise Miyapur — due: 15-Apr-2026" | Success (green) |
| Reminder sent | "Reminder sent to R. Suresh — UDISE+ due in 5 days" | Info (blue) |
| Auto-escalation triggered | "OVERDUE: Fire NOC Renewal for Sunrise Miyapur escalated to Zone Director" | Warning (amber) |
| Proof uploaded | "Filing proof uploaded for GST Return (Mar) — Sunrise Begumpet" | Success (green) |
| Template created | "Filing template 'Water Quality Test Report' added — applicable to all branches" | Success (green) |
| Overdue alert | "3 filings are overdue — immediate attention required" | Error (red) |
| Deadline approaching | "38 filings due in the next 30 days — review recommended" | Warning (amber) |
| Filing dependency warning | "CBSE Affiliation Renewal depends on Fire NOC — Fire NOC is expired" | Warning (amber) |
| Batch filings generated | "412 filing instances generated for FY 2026-27 from 15 templates across 28 branches" | Success (green) |

---

## 9. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No filings created (fresh setup) | Calendar with dotted outline | "No regulatory filings tracked yet. Import filing templates to auto-generate filings for all branches." | `[Import Filing Templates]` `[+ Add Filing Manually]` |
| No filings for selected branch | Empty checklist | "No filings found for {branch name}. This branch may not have been included in the filing schedule." | `[+ Add Filing for This Branch]` |
| No overdue filings | Calendar with green checkmark | "No overdue filings — all submissions are on time. Excellent compliance!" | — (positive state) |
| No templates (Tab 4) | Template with dotted outline | "No filing templates configured. Templates define what filings exist and when they're due." | `[+ Add Filing Template]` `[Load Pre-built Templates]` |
| Filter returns zero | Magnifying glass | "No filings match your filters. Try adjusting the branch, authority, or status filter." | `[Reset Filters]` |
| Calendar — no events this month | Blank calendar | "No filings due this month. Check other months or review upcoming deadlines." | — |

---

## 10. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Page initial load | Skeleton: KPI cards + calendar grid | < 1s |
| KPI bar | 8 grey pulse cards → populated | < 500ms |
| Calendar view (FullCalendar.js) | Calendar skeleton with grey blocks | < 1s |
| Filing list table | 10 skeleton rows → data | < 1s |
| Branch status matrix | Grid skeleton with pulsing cells | < 1.5s (large matrix) |
| Filing detail drawer | Drawer skeleton → populated | < 500ms |
| Batch filing generation | Progress bar: "Generating filings… 15/28 branches" | 3–10s |
| Reminder sending | Spinner on button + "Sending…" | < 2s |
| Export | Spinner on button + "Preparing download…" | 2–5s |
| Chart rendering | Grey chart placeholder → Chart.js render | < 500ms |

---

## 11. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/regulatory/filings/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | List all filings (paginated, filterable by branch/authority/status/FY) | G1+ |
| 2 | GET | `/{filing_id}/` | Filing detail with history and proof | G1+ |
| 3 | POST | `/` | Create new filing instance | 125, G4+ |
| 4 | PATCH | `/{filing_id}/` | Update filing (status, assigned to, deadline) | 125, Branch Principal |
| 5 | POST | `/{filing_id}/complete/` | Mark filing as completed with proof | 125, 123, Branch Principal |
| 6 | POST | `/{filing_id}/proof/` | Upload proof of filing | 125, 123, Branch Principal, Branch Admin |
| 7 | GET | `/{filing_id}/proof/download/` | Download filing proof | G1+ |
| 8 | GET | `/{filing_id}/history/` | Filing activity history | G1+ |
| 9 | POST | `/bulk-complete/` | Mark multiple filings as completed | 125 |
| 10 | GET | `/calendar/` | Calendar event data (date range, filterable) | G1+ |
| 11 | GET | `/branch-matrix/` | Branch × filing type completion matrix | G1+ |
| 12 | GET | `/overdue/` | All overdue filings | G1+ |
| 13 | GET | `/upcoming/?days={n}` | Filings due within N days | G1+ |
| 14 | POST | `/reminders/` | Send filing reminder | 125, 128 |
| 15 | POST | `/generate-fy/` | Auto-generate filings for new FY from templates | 125, G4+ |
| 16 | GET | `/templates/` | List filing templates | G1+ |
| 17 | POST | `/templates/` | Create new filing template | 125, G4+ |
| 18 | PATCH | `/templates/{template_id}/` | Update filing template | 125, G4+ |
| 19 | DELETE | `/templates/{template_id}/` | Deactivate filing template | G4+ |
| 20 | GET | `/charts/compliance-rate/` | Chart 1 data | G1+ |
| 21 | GET | `/charts/by-category/` | Chart 2 data | G1+ |
| 22 | GET | `/charts/branch-heatmap/` | Chart 3 data | G1+ |
| 23 | GET | `/charts/overdue-ageing/` | Chart 4 data | G1+ |
| 24 | GET | `/kpis/` | KPI bar aggregates | G1+ |
| 25 | GET | `/export/` | Export filings as Excel | G1+ |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../filings/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#filing-content` | `innerHTML` | `hx-trigger="click"` |
| Calendar view | Tab 1 load | `hx-get=".../filings/calendar/?month={}&year={}"` | `#calendar-content` | `innerHTML` | FullCalendar.js init |
| Calendar month nav | Prev/Next click | `hx-get=".../filings/calendar/?month={}"` | `#calendar-content` | `innerHTML` | FullCalendar nav |
| Filing list table | Tab 2 load | `hx-get=".../filings/?page=1"` | `#filing-table-body` | `innerHTML` | Paginated |
| Filter change | Select/input change | `hx-get=".../filings/?branch={}&status={}"` | `#filing-table-body` | `innerHTML` | `hx-trigger="change"` debounced |
| Filing detail drawer | Row/event click | `hx-get=".../filings/{id}/"` | `#right-drawer` | `innerHTML` | 780px drawer |
| Mark complete | Button click | `hx-post=".../filings/{id}/complete/"` | `#filing-{id}-status` | `innerHTML` | Toast + inline update |
| Upload proof | Form submit | `hx-post=".../filings/{id}/proof/"` | `#proof-section` | `innerHTML` | Toast + proof display |
| Branch matrix | Tab 3 load | `hx-get=".../filings/branch-matrix/"` | `#matrix-content` | `innerHTML` | Large grid |
| Matrix cell update | Cell click → popover submit | `hx-patch=".../filings/{id}/"` | `#cell-{branch}-{filing}` | `innerHTML` | Inline cell update |
| Filing templates | Tab 4 load | `hx-get=".../filings/templates/"` | `#templates-content` | `innerHTML` | — |
| Add filing | Form submit | `hx-post=".../filings/"` | `#add-result` | `innerHTML` | Toast + table refresh |
| Send reminder | Form submit | `hx-post=".../filings/reminders/"` | `#reminder-result` | `innerHTML` | Toast |
| Generate FY filings | Button click | `hx-post=".../filings/generate-fy/"` | `#generate-result` | `innerHTML` | Progress bar → toast |
| Chart load | Tab/section shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |
| Pagination | Page click | `hx-get` with page param | `#filing-table-body` | `innerHTML` | — |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
