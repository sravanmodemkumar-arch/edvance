# 05 — Counselling Head Dashboard

> **URL:** `/group/welfare/counselling/`
> **File:** `05-counselling-head-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Counselling Head (Role 94, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Counselling Head. Command centre for counselling services across all branches — peer counselling programs, individual counselling sessions, college and career guidance, and mental health referral intake from the branch medical team. Tracks session volumes by branch, counsellor availability and certification status, student referral pipelines from health to counselling, and college admission guidance outcomes for Class 11–12 students.

The Group Counselling Head is accountable for ensuring every branch has at least one qualified and certified counsellor at all times, that the mandated minimum monthly group counselling sessions are delivered at each branch, that students referred by the medical team for mental health support receive intake within 48 hours, and that high-risk students flagged as urgent cases receive same-day intervention. They also compile the annual college placement guidance report for the Chairman, tracking the pipeline from career counselling through college applications to admission offers. Any branch missing a counsellor, any urgent high-risk student case open without update for 7 days, or any medical referral pending intake for more than 48 hours triggers an immediate action obligation.

Scale: 20–50 branches · 1–3 qualified counsellors per branch · 500–3,000 individual counselling sessions/year · 1,000–10,000 students in college guidance pipeline.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Counselling Head | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group Medical Coordinator | G3 | View — referrals section only | Cannot see session notes or case details |
| Group Chairman / CEO | G5 / G4 | View — urgent cases and college guidance outcomes | Not this URL |
| Branch Counsellor | G2 | View — own branch sessions, cases, college guidance | Branch-scoped, not this URL |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('counselling_head')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Counselling Head Dashboard
```

### 3.2 Page Header
```
Welcome back, [Head Name]                    [Export Counselling Report ↓]  [Settings ⚙]
[Group Name] — Group Counselling Head · Last login: [date time]
AY [current academic year]  ·  [N] Branches  ·  [N] Counsellors Active  ·  [N] Sessions This Month
```

### 3.3 Alert Banner (conditional — critical items requiring same-day action)

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with no counsellor assigned | "[N] branch(es) have no counsellor assigned: [Branch list]. Student wellbeing at risk." | Red |
| Urgent / high-risk case open > 7 days with no update | "High-risk student [Case ID] at [Branch] has had no case update in [N] days. Immediate review required." | Red |
| Medical referral pending intake > 48 hours | "[N] medical referral(s) have been waiting for counselling intake for over 48 hours. Contact branch counsellor immediately." | Amber |
| Monthly group session not held at a branch | "[Branch] has not held its mandatory monthly group counselling session for [Month]. Reschedule immediately." | Amber |
| Counsellor certification expiring within 30 days | "Counsellor [Name] at [Branch] has certification expiring on [date]. Renewal required." | Amber |

Max 5 alerts visible. Alert links route to the relevant branch, case, or referral record. "View all counselling events → Counselling Audit Log" always shown below alerts.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Branches with Active Counsellor | Branches with at least one assigned and certified counsellor / total branches | Green = all · Red if any branch missing | → Section 5.1 |
| Sessions This Month | Total individual and group counselling sessions across all branches this calendar month | Blue always (informational) | → Section 5.2 |
| Students on Active Counselling Plan | Students currently on a structured multi-session plan, group-wide | Blue always (informational) | → Section 5.1 |
| Referrals from Medical Team | Referrals received from branch medical staff pending counselling intake | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.1 |
| College Guidance Coverage % | Class 11–12 students who have received at least one college guidance session this AY | Green ≥ 80% · Yellow 60–79% · Red < 60% | → Section 5.3 |
| Peer Counselling Programs This Month | Group peer counselling sessions conducted this calendar month across all branches | Blue always (informational) | → Section 5.1 |
| Urgent Cases | Students currently flagged as high-risk requiring elevated monitoring | Green = 0 · Red if any | → Section 5.4 |
| Counsellors Due for Certification Renewal | Counsellors whose professional certification expires within next 60 days | Green = 0 · Amber if any | → Section 5.1 |

**HTMX:** `hx-trigger="every 5m"` → Referrals from Medical Team and Urgent Cases auto-refresh.

---

## 5. Sections

### 5.1 Branch Counselling Matrix

> Per-branch summary of counselling readiness, session activity, and pending work.

**Search:** Branch name, city, counsellor name. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Counsellor Assigned | Radio | All / Assigned / Not Assigned |
| Pending Referrals | Checkbox | Show branches with pending medical referrals only |
| Monthly Session | Radio | All / Session Held / Session Not Held |
| High-Risk Cases | Checkbox | Show branches with urgent cases only |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → `branch-counselling-detail` drawer |
| Counsellor Assigned | ✅ | Name(s) or ❌ None (Red) |
| Certification Status | ✅ | Valid ✅ / Expiring Soon ⚠ / Expired ❌ |
| Sessions This Month | ✅ | Count (individual + group) |
| Pending Referrals | ✅ | Count; Red if > 0 |
| High-Risk Students | ✅ | Count; Red if any |
| College Guidance % | ✅ | % of Class 11–12 counselled; colour-coded |
| Monthly Session Held | ✅ | ✅ Yes / ❌ No (Red if not held for current month) |
| Actions | ❌ | View · Send Reminder · Log Session |

**Default sort:** Counsellor Assigned (Not Assigned first), then Pending Referrals descending.
**Pagination:** Server-side · 25/page.

---

### 5.2 Session Volume Chart

> Visual breakdown of counselling session volumes by branch and monthly trend.

**Display:** Two charts side-by-side on desktop, stacked on mobile.

**Chart 1 — Bar Chart (branch-wise):**
- X-axis: Branch names
- Y-axis: Session count this month
- Dual series: Individual Sessions (Blue solid) + Group/Peer Sessions (Teal outline)
- Tooltip: Branch · Individual count · Group count · Total
- Click bar → `branch-counselling-detail` drawer at Sessions tab

**Chart 2 — Line Chart (monthly trend, past 6 months):**
- X-axis: Last 6 months (abbreviated month-year)
- Y-axis: Session count
- Two lines: Individual (Blue) + Group (Teal)
- Tooltip: Month · Individual sessions · Group sessions · Total
- Reference line: Monthly target (if configured) as dotted horizontal line

---

### 5.3 College Guidance Pipeline

> Funnel chart tracking Class 11–12 students through the college guidance journey this AY.

**Funnel stages (top to bottom — count and % of total Class 11–12 students):**
1. Total Class 11–12 Students enrolled
2. Students Counselled at Least Once (career / college guidance session completed)
3. Colleges Shortlisted (student has shortlisted ≥ 3 colleges)
4. Applications Submitted (at least one college application submitted)
5. Offers Received (at least one admission offer)
6. Admissions Confirmed (student has accepted an offer)

- Each stage shows: Count · % of total · Drop-off from previous stage
- Colour: Stages progress from Light Blue → Dark Blue
- Click on any stage → filtered student list (name · branch · class · counsellor · stage status)
- Below funnel: "Export college guidance report →" downloads per-student CSV

---

### 5.4 Urgent Cases

> High-risk students flagged for elevated monitoring — requires same-day review by Group Counselling Head.

**Display:** Card-style list — each urgent case as a card with key details. Maximum 10 cards visible; "View all [N] urgent cases →" if more exist.

**Card content:**
- Student name (masked to initials for non-counselling viewers) + Case ID
- Branch · Counsellor assigned
- Risk reason: e.g., "Self-harm ideation" / "Severe anxiety" / "Family crisis" / "Referred by medical team"
- Date flagged as urgent · Days since last update
- Status: Active Monitoring / Escalated to Medical / Escalated to Principal / Referred to External
- [View Full Case →] button → `urgent-case-detail` drawer

**Colour rule:** Card border — Red if no update in > 7 days · Orange if 3–7 days · White if updated within 3 days.

---

## 6. Drawers / Modals

### 6.1 Drawer: `branch-counselling-detail`
- **Trigger:** Branch name link in Section 5.1 table
- **Width:** 640px
- **Tabs:** Counsellors · Sessions · College Guidance · Peer Programs

**Counsellors tab:**
- List of counsellors at this branch: Name · Qualification · Certification body · Certification expiry · Specialisation (Child / Adolescent / Career / CBT) · Status (Active / On Leave / Expired)
- [Add Counsellor] button

**Sessions tab:**
- This month summary: Individual sessions [N] · Group sessions [N] · Unique students seen [N]
- Session log: Date · Type (Individual / Group) · Counsellor · Attendee count · Theme/Focus · Duration
- Pending referrals from medical: Referral date · Student (masked) · Referred by · Days waiting

**College Guidance tab:**
- Branch-level funnel: stages with counts (same structure as Section 5.3 but branch-scoped)
- Per-student pipeline list (Name · Class · Counsellor · Current stage · Last session date)

**Peer Programs tab:**
- Peer counsellors trained at this branch: Name · Class · Training Date · Status (Active/Graduated)
- Sessions this month: Date · Type · Attendees · Referrals raised
- "Manage Peer Program →" link → `/group/welfare/counselling/peer-programs/?branch={id}` (Page 30)

---

### 6.2 Drawer: `urgent-case-detail`
- **Trigger:** "View Full Case →" button on urgent case card in Section 5.4
- **Width:** 560px
- **Mode:** Read-only summary with action buttons

**Content:**
| Field | Notes |
|---|---|
| Case ID | System-generated |
| Branch | |
| Student (masked) | Initials + grade only for non-assigned counsellors |
| Assigned Counsellor | Name · Contact |
| Date Flagged | When case was escalated to urgent status |
| Risk Reason | Category + brief description |
| Current Status | Active Monitoring / Escalated / Referred |
| Case Notes Timeline | Chronological notes: date · author · note text (max 10 shown) |
| Last Update | Date and brief summary |
| Days Since Last Update | With colour coding |
| External Referrals | If referred to external psychologist/hospital — name, date, outcome |

- Footer action buttons (visible to Counselling Head only): [Add Case Note] · [Change Status] · [Escalate to Medical] · [Close Case]

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Session logged | "Counselling session logged at [Branch] — [N] student(s)." | Success | 4s |
| Referral intake confirmed | "Medical referral for [Case ID] intake confirmed. Session booked." | Success | 4s |
| Urgent case status updated | "Urgent case [ID] status updated to [Status]." | Success | 4s |
| Case note added | "Case note added to [Case ID]." | Info | 4s |
| Counsellor reminder sent | "Monthly session reminder sent to counsellor at [Branch]." | Info | 4s |
| College guidance report exported | "College guidance report export prepared. Download ready." | Info | 4s |
| Urgent case escalated | "Urgent case [ID] escalated to [Medical Team / Principal]." | Warning | 6s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No urgent cases | "No Urgent Cases" | "No students are currently flagged as high-risk across any branch." | — |
| No pending referrals | "No Pending Medical Referrals" | "All medical referrals have been accepted for counselling intake." | — |
| No sessions this month | "No Sessions Logged Yet This Month" | "No counselling sessions have been recorded for this month yet." | [Log Session] |
| Search returns no results | "No Results Found" | "No branches or cases match your search or filters." | [Clear Filters] |
| All branches have counsellor | "All Branches Covered" | "Every branch has an active, certified counsellor assigned for this academic year." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + branch matrix table (15 rows × 9 columns) + session charts + funnel + urgent cases list + alerts |
| Table filter/search | Inline skeleton rows (8 rows) |
| KPI auto-refresh | Shimmer on individual card values; labels preserved |
| Session volume chart load | Chart area skeleton with animated gradient |
| College guidance funnel load | Funnel skeleton (6 stage bars with grey fill) |
| Urgent cases list load | Card skeletons (3 cards × 2 rows) |
| Branch detail drawer open | 640px drawer skeleton; tabs load lazily on first click |
| Urgent case drawer open | 560px drawer skeleton with timeline (8 rows) |

---

## 10. Role-Based UI Visibility

| Element | Counselling Head G3 | Medical Coordinator G3 | Chairman / CEO G5 | Branch Counsellor G2 |
|---|---|---|---|---|
| View All Branches | ✅ | Referrals section only | Urgent + guidance | Own branch only |
| Log Session | ✅ | ❌ | ❌ | ✅ (own branch) |
| View Session Details | ✅ | ❌ | ❌ | ✅ (own branch) |
| View Urgent Case Full Notes | ✅ | ❌ | ❌ | ✅ (own cases) |
| Add Case Note | ✅ | ❌ | ❌ | ✅ (own cases) |
| Change Case Status | ✅ | ❌ | ❌ | ✅ (own cases) |
| Escalate Urgent Case | ✅ | ❌ | ❌ | ❌ |
| Confirm Referral Intake | ✅ | ✅ | ❌ | ✅ (own branch) |
| View College Guidance Pipeline | ✅ | ❌ | ✅ | ✅ (own branch) |
| Export Counselling Report | ✅ | ❌ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/counselling/dashboard/` | JWT (G3+) | Full dashboard data payload |
| GET | `/api/v1/group/{group_id}/welfare/counselling/kpi-cards/` | JWT (G3+) | KPI auto-refresh values |
| GET | `/api/v1/group/{group_id}/welfare/counselling/branch-matrix/` | JWT (G3+) | Branch counselling matrix; params: `counsellor_assigned`, `pending_referrals`, `page` |
| GET | `/api/v1/group/{group_id}/welfare/counselling/sessions/` | JWT (G3+) | Session volume data; params: `branch_id`, `month`, `type` |
| POST | `/api/v1/group/{group_id}/welfare/counselling/sessions/` | JWT (G3) | Log new counselling session |
| GET | `/api/v1/group/{group_id}/welfare/counselling/referrals/pending/` | JWT (G3+) | Pending medical referrals awaiting intake |
| PATCH | `/api/v1/group/{group_id}/welfare/counselling/referrals/{referral_id}/intake/` | JWT (G3) | Confirm referral intake |
| GET | `/api/v1/group/{group_id}/welfare/counselling/urgent-cases/` | JWT (G3+) | Urgent / high-risk student cases |
| GET | `/api/v1/group/{group_id}/welfare/counselling/urgent-cases/{case_id}/` | JWT (G3+) | Single urgent case detail with notes timeline |
| POST | `/api/v1/group/{group_id}/welfare/counselling/urgent-cases/{case_id}/notes/` | JWT (G3) | Add case note |
| PATCH | `/api/v1/group/{group_id}/welfare/counselling/urgent-cases/{case_id}/status/` | JWT (G3) | Update case status or escalate |
| GET | `/api/v1/group/{group_id}/welfare/counselling/college-guidance/funnel/` | JWT (G3+) | College guidance funnel data |
| GET | `/api/v1/group/{group_id}/welfare/branches/{branch_id}/counselling-detail/` | JWT (G3+) | Branch counselling detail drawer payload |
| GET | `/api/v1/group/{group_id}/welfare/counselling/export/` | JWT (G3+) | Async counselling / guidance report export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../counselling/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Urgent cases auto-refresh | `every 5m` | GET `.../counselling/urgent-cases/` | `#urgent-cases-list` | `innerHTML` |
| Branch matrix search | `input delay:300ms` | GET `.../counselling/branch-matrix/?q={val}` | `#branch-matrix-body` | `innerHTML` |
| Branch matrix filter | `click` | GET `.../counselling/branch-matrix/?{filters}` | `#branch-matrix-section` | `innerHTML` |
| Branch matrix pagination | `click` | GET `.../counselling/branch-matrix/?page={n}` | `#branch-matrix-section` | `innerHTML` |
| Open branch drawer | `click` on branch name | GET `.../welfare/branches/{id}/counselling-detail/` | `#drawer-body` | `innerHTML` |
| Open urgent case drawer | `click` View Full Case | GET `.../counselling/urgent-cases/{id}/` | `#drawer-body` | `innerHTML` |
| Add case note | `click` Save Note | POST `.../counselling/urgent-cases/{id}/notes/` | `#case-notes-timeline` | `innerHTML` |
| Update case status | `click` Save | PATCH `.../counselling/urgent-cases/{id}/status/` | `#urgent-case-card-{id}` | `outerHTML` |
| Confirm referral intake | `click` | PATCH `.../counselling/referrals/{id}/intake/` | `#referral-row-{id}` | `outerHTML` |
| Session chart load | `load` | GET `.../counselling/sessions/?month=current` | `#session-chart-section` | `innerHTML` |
| College guidance funnel load | `load` | GET `.../counselling/college-guidance/funnel/` | `#guidance-funnel-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
