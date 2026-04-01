# 10 — Branch Detail

> **URL:** `/group/gov/branches/<branch_id>/`
> **File:** `10-branch-detail.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Chairman G5 · MD G5 · CEO G4 (full) · President G4 (Academic tabs) · VP G4 (Ops tabs) · Trustee G1 · Advisor G1 (read)

---

## 1. Purpose

Deep-dive page for a single branch. Accessed from Branch Overview table, Chairman/CEO dashboards,
and any cross-link. Provides a comprehensive view of a branch across 9 functional tabs — each tab
is scoped to the relevant division's data for that branch.

This is a read-heavy page — most roles view, few roles edit. Edit permissions are tab-specific.

---

## 2. Role Access

| Role | Tabs Visible | Can Edit |
|---|---|---|
| Chairman G5 | All 9 tabs | All tabs |
| MD G5 | All 9 tabs | All tabs |
| CEO G4 | All 9 tabs | Overview · Config tabs only |
| President G4 | Overview · Academic | ❌ |
| VP G4 | Overview · Students · Staff · Hostel · Transport · Compliance | ❌ |
| Trustee G1 | Overview · Academic · Finance (totals only) · Compliance | ❌ |
| Advisor G1 | Overview · Academic | ❌ |
| Exec Secretary | ❌ | ❌ |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Branch Overview  ›  [Branch Name]
```

### 3.2 Branch Header Card
```
[Branch Logo / Initial Avatar]  [Branch Name] — [Branch Code]        [Edit Branch ✏]  [⋮ More Actions]
                                 [City, State]  · [Board: CBSE/BSEAP] · [Type: Day/Hostel]
                                 Principal: [Name] · [Mobile]         Status: [Active badge]
                                 Established: [Year] · Students: [N] · Staff: [N]
```

**[Edit Branch]** — opens `branch-edit` drawer (Chairman/MD/CEO only).

**[⋮ More Actions] dropdown:**
- Activate / Deactivate Portal
- Download Branch Report PDF
- View on Map
- Open Branch Portal (opens branch-level portal in new tab)

---

## 4. Tab Navigation

```
Overview  |  Academic  |  Finance  |  Students  |  Staff  |  Hostel  |  Transport  |  Health  |  Compliance
```

Tabs are rendered server-side — G1 sees only their allowed tabs. Tab with data issues shows red dot.

---

## 5. Tab Specifications

### Tab 1: Overview

**KPI Cards (6):**
| Card | Metric |
|---|---|
| Enrollment | Total enrolled + vs target |
| Fee Collection | Monthly collection rate % |
| Attendance | This month % |
| BGV Compliance | % staff verified |
| Open Escalations | Count with severity badges |
| Last Audit | Date + days since |

**Branch Info Section:**
- Address (full), Google Maps embed (iframe, 300px height)
- Principal contact: Name, mobile, email (masked for G1)
- Streams offered: tag list
- Hostel capacity (if applicable): Boys / Girls / AC / Non-AC

**Recent Activity Feed (read-only):**
- Last 10 audit log entries for this branch
- Shows: Actor, Action, Timestamp, icon by type

---

### Tab 2: Academic

**Section: Exam Performance History**

Columns: Exam Name · Class/Stream · Date · Avg Score % · Pass % · Toppers (90%+) · Submitted By · Status (Approved/Rejected/Pending)

Search: Exam name. Filters: Class, Stream, Date range, Status.

**Section: Curriculum Completion**

Table: Subject · Stream · Chapter Count · Completed · % · Teacher · Last Updated.

**Section: Topper List (current year)**

Table: Rank · Student Name · Class · Score % · Exam. Export PDF button.

**Charts:**
- Exam score trend (last 6 exams) — line chart
- Pass rate by class/stream — grouped bar chart

---

### Tab 3: Finance

**Section: Fee Structure (read for G1, edit for G5/G4)**

Table: Student Type · Fee Component · Amount ₹ · Frequency · Effective Date.

**Section: Monthly Collection Summary**

Table: Month · Day Scholar Collected · Hosteler Collected · Outstanding · Collection % · Actions.

**Section: Scholarship Summary**

Table: Scholarship Type · Students Count · Total Waiver ₹ · Source (Merit/Govt/RTE).

**Charts:**
- Monthly fee collection % (12 months) — line chart
- Fee type distribution (Day/Hosteler/Coaching) — donut chart

---

### Tab 4: Students

**Section: Enrollment Breakdown**

Table: Student Type · Count · % of Total.

Student types:
- Day Scholar Regular · Day Scholar Scholarship · Day Scholar RTE Quota
- Hosteler Boys AC · Hosteler Boys Non-AC
- Hosteler Girls AC · Hosteler Girls Non-AC
- Hosteler Scholarship
- Special Needs Day · Special Needs Hosteler
- NRI / Foreign National
- Integrated Coaching

**Section: Attendance Summary**

Table: Month · Total Students · Present Avg % · Absent Avg % · Late %.

**Charts:**
- Enrollment by type (horizontal bar)
- Attendance trend (last 6 months) — line chart

---

### Tab 5: Staff

**Section: Staff Headcount**

Table: Department · Sanctioned · Filled · Vacant · Vacancy % · BGV % · POCSO %.

Departments: Teaching (by stream) · Administration · Hostel · Transport · Support.

**Section: Staff Roster** (Chairman/MD only — PII data)

Table: Name · Designation · Department · Joined Date · BGV Status · POCSO Trained · Last Login.

Filters: Department, BGV Status, POCSO status.

**Row actions (MD/Chairman only):** View BGV Detail · Edit Role · View Profile.

---

### Tab 6: Hostel

**Shown only if branch type = Hostel or Both.**

**Section: Occupancy**

Table: Hostel Block · Type (Boys AC / Boys Non-AC / Girls AC / Girls Non-AC) · Capacity · Occupied · Available · Occupancy %.

**Section: Welfare Events (last 30 days)**

Table: Date · Type · Severity (1–4) · Description · Resolved? · Resolution.

**Section: Meal Menu (current week)**

Table: Day · Breakfast · Lunch · Dinner · Snacks.

**Charts:**
- Occupancy by block (bar chart)
- Welfare events by severity trend (line chart)

---

### Tab 7: Transport

**Shown only if branch has transport enabled.**

**Section: Routes**

Table: Route ID · Area Covered · Bus No · Driver · Conductor · Students on Route · Morning Pickup · Afternoon Drop.

**Section: Fleet Status**

Table: Bus No · Registration · Capacity · Operational Status · Last Service · GPS Active?

**Charts:**
- Route utilization % (bar — students assigned vs bus capacity per route)

---

### Tab 8: Health

**Section: Medical Room Status**

Cards: Doctor Visit Schedule · Nurse on Duty? · Medical Room Location.

**Section: Health Incidents (last 90 days)**

Table: Date · Student Name (masked for G1) · Type · Severity · Action Taken · Resolved?.

**Section: Medical Insurance**

Cards: Insurance Provider · Policy Number (masked) · Coverage Amount · Expiry Date.

---

### Tab 9: Compliance

**Section: Compliance Status per Area**

Table: Area · Status · Last Checked · Renewal Due · Evidence · Actions.

| Compliance Area | Status |
|---|---|
| CBSE Affiliation | ✅/⚠/❌ |
| State Board Affiliation | ✅/⚠/❌ |
| POCSO Training | X% |
| BGV Completion | X% |
| Fire Safety NOC | ✅/⚠/❌ |
| DPDP Compliance | ✅/⚠/❌ |
| RTE Quota | ✅/⚠/❌ |

**Row actions (G5/G4 only):** Mark Compliant · Upload Evidence · Set Renewal Reminder.

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-edit`
- **Width:** 680px
- **Tabs:** Profile · Address · Board Affiliation · Principal · Config
- Pre-filled from current branch data (same fields as `branch-create`)

### 6.2 Modal: `branch-activate-confirm`
- Same as page 09 spec

### 6.3 Modal: `branch-report-download`
- **Width:** 380px
- **Fields:** Report type (Full · Academic · Finance · Staff) · Date range
- **Buttons:** [Generate & Download PDF] + [Cancel]

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Branch updated | "Branch details updated" | Success | 4s |
| Status changed | "Branch [Name] status changed to [Active/Inactive]" | Warning | 6s |
| Report generating | "Branch report generating… download will start" | Info | 4s |
| Tab data load error | "Failed to load [tab name] data. Refresh to try again." | Error | Manual |
| Compliance updated | "Compliance status updated" | Success | 4s |

---

## 8. Empty States (per tab)

| Tab | Condition | Heading | CTA |
|---|---|---|---|
| Academic | No exams yet | "No exams recorded" | — |
| Finance | No transactions | "No fee transactions recorded" | — |
| Students | No enrollment | "No students enrolled" | — |
| Hostel | No hostel configured | "Hostel module not enabled" | [Enable in Config tab] |
| Transport | No routes | "Transport module not enabled" | [Enable in Config tab] |
| Health | No incidents | "No health incidents recorded" | — |
| Compliance | Not set up | "Compliance data not yet entered" | [Add Compliance Status] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: header card + 6 KPI cards + overview content |
| Tab switch | Skeleton matching the tab layout |
| Any table within tab | Inline skeleton rows |
| Edit drawer open | Spinner in drawer |
| Report download | Spinner in button |

---

## 10. Role-Based UI Visibility

| Element | Chairman/MD | CEO | President | VP | Trustee/Advisor |
|---|---|---|---|---|---|
| [Edit Branch] button | ✅ | ✅ | ❌ | ❌ | ❌ |
| [Activate/Deactivate] | ✅ | ✅ | ❌ | ❌ | ❌ |
| Finance tab (full) | ✅ | ✅ | ❌ | ❌ | ✅ totals only |
| Staff tab (full roster) | ✅ | ❌ | ❌ | ✅ headcount | ❌ |
| Staff PII (names) | Chairman/MD | ❌ | ❌ | ❌ | ❌ |
| Hostel tab | ✅ | ✅ | ❌ | ✅ | ❌ |
| Health incident names | Chairman/MD | ❌ | ❌ | ❌ | ❌ |
| Compliance actions | Chairman/MD/CEO | ✅ | ❌ | ❌ | ❌ |
| Download branch report | ✅ | ✅ | ❌ | ❌ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/branches/{bid}/` | JWT | Branch detail (overview tab) |
| GET | `/api/v1/group/{id}/branches/{bid}/academic/` | JWT | Academic tab data |
| GET | `/api/v1/group/{id}/branches/{bid}/finance/` | JWT | Finance tab data |
| GET | `/api/v1/group/{id}/branches/{bid}/students/` | JWT | Students tab data |
| GET | `/api/v1/group/{id}/branches/{bid}/staff/` | JWT | Staff tab data |
| GET | `/api/v1/group/{id}/branches/{bid}/hostel/` | JWT | Hostel tab data |
| GET | `/api/v1/group/{id}/branches/{bid}/transport/` | JWT | Transport tab data |
| GET | `/api/v1/group/{id}/branches/{bid}/health/` | JWT | Health tab data |
| GET | `/api/v1/group/{id}/branches/{bid}/compliance/` | JWT | Compliance tab data |
| PUT | `/api/v1/group/{id}/branches/{bid}/` | JWT (G5/G4) | Update branch |
| POST | `/api/v1/group/{id}/branches/{bid}/activate/` | JWT (G4+) | Activate/deactivate |
| GET | `/api/v1/group/{id}/branches/{bid}/report/?type=full` | JWT | Generate report PDF |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | GET `.../branches/{id}/{tab}/` | `#tab-content` | `innerHTML` |
| Table search (in tab) | `input delay:300ms` | GET `.../branches/{id}/{tab}/?q=` | `#tab-table-body` | `innerHTML` |
| Filter in tab | `click` | GET `.../branches/{id}/{tab}/?filters=` | `#tab-table-section` | `innerHTML` |
| Pagination in tab | `click` | GET `.../branches/{id}/{tab}/?page=` | `#tab-table-section` | `innerHTML` |
| Edit drawer submit | `submit` | PUT `.../branches/{id}/` | `#drawer-body` | `innerHTML` |
| Compliance action | `click` | POST `.../branches/{id}/compliance/{area}/` | `#compliance-row-{area}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
