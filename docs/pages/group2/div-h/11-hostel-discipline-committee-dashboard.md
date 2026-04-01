# 11 — Hostel Discipline Committee Dashboard

> **URL:** `/group/hostel/discipline/`
> **File:** `11-hostel-discipline-committee-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Hostel Discipline Committee (Role 78, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Hostel Discipline Committee. Manages discipline cases for hostelers across all branches — from initial incident reporting through investigation, hearing scheduling, decision, sanctions (warning / suspension from hostel / permanent expulsion from hostel), and appeal. Boys and girls discipline cases are always handled by gender-appropriate committee members; all cases are documented with a full immutable audit trail.

The Hostel Discipline Committee operates at the group level for escalated or serious cases. Minor hostel misconduct is handled by the Branch Warden; escalated or repeat offences come to the group committee. The group committee's decisions override the branch.

**Case types covered:**
- Physical altercation between hostelers
- Bullying (physical, verbal, cyber)
- Substance use on hostel premises
- Theft or damage to hostel property
- Violation of hostel rules (repeated / serious)
- POCSO-related misconduct (auto-linked to POCSO Coordinator)
- Unauthorized absence from hostel

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Hostel Discipline Committee | G3 | Full — all cases, all genders | Exclusive dashboard |
| Group Boys Hostel Coordinator | G3 | View — boys discipline cases | Via own dashboard |
| Group Girls Hostel Coordinator | G3 | View — girls discipline cases | Via own dashboard |
| Group Hostel Welfare Officer | G3 | View — cases linked to welfare incidents | Read-only |
| Group Hostel Security Coordinator | G3 | View — security-linked cases | Read-only |
| Group Hostel Director | G3 | View — all cases + approve final sanctions | Via own dashboard |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Discipline Committee Dashboard
```

### 3.2 Page Header
```
Welcome back, [Committee Name]          [+ New Case]  [Export Cases ↓]  [Settings ⚙]
Group Hostel Discipline Committee · AY [current academic year]
Open Cases: [N]  ·  Pending Hearing: [N]  ·  Pending Decision: [N]  ·  Closed (AY): [N]
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| POCSO-linked case open | "POCSO CONCERN: Case #[ID] at [Branch] is linked to a POCSO concern. POCSO Coordinator has been notified." | Red |
| Case open > 30 days with no hearing | "Case #[ID] has been open for > 30 days without a hearing scheduled." | Amber |
| Appeal filed and pending > 7 days | "[N] discipline case appeals pending review for > 7 days." | Amber |

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open Cases (Total) | Active cases requiring action | Green = 0 · Yellow 1–5 · Red > 5 | → Page 28 |
| Pending Hearing | Cases where hearing is not yet scheduled | Green = 0 · Yellow 1–3 · Red > 3 | → Page 28 (hearing pending) |
| POCSO-linked Cases | Cases with POCSO flag | Green = 0 · Red > 0 | → Page 28 (POCSO filter) |
| Sanctions This Month | Decisions issued (warnings + suspensions + expulsions) | Blue always | → Page 28 (decisions filter) |
| Pending Appeal | Appeals filed awaiting committee response | Yellow > 0 | → Page 28 (appeal filter) |
| Cases Closed (AY) | Total cases closed this academic year | Blue always | → Page 28 (closed filter) |

**HTMX:** `hx-trigger="every 10m"` → KPI auto-refresh.

---

## 5. Sections

### 5.1 Active Cases Table

> All open discipline cases — Committee's working table.

**Search:** Case #, hosteler name, branch. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Gender | Radio | All / Boys / Girls |
| Case Type | Checkbox | Physical Altercation / Bullying / Substance / Theft / Rule Violation / POCSO / Unauthorized Absence |
| Status | Checkbox | Investigation / Hearing Scheduled / Pending Decision / Decision Issued / Appeal / Closed |
| POCSO Flag | Checkbox | POCSO-linked cases only |
| Age | Radio | Any / > 7 days / > 15 days / > 30 days |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Case # | ✅ | Auto ID — link → case detail drawer |
| Hosteler Name | ✅ | |
| Gender | ✅ | M/F badge |
| Branch | ✅ | |
| Case Type | ✅ | Badge |
| Opened | ✅ | Date |
| Age | ✅ | Days (red if > 30) |
| Status | ✅ | Stage badge |
| Hearing Date | ✅ | Date or "Not Scheduled" (amber) |
| POCSO | ✅ | ✅ if linked |
| Actions | ❌ | View · Schedule Hearing · Issue Decision |

**Default sort:** POCSO-flagged first, then age descending.

**Pagination:** Server-side · 25/page.

---

### 5.2 Upcoming Hearings

> Scheduled discipline hearings in the next 14 days.

**Display:** Timeline / list — Case # · Hosteler · Branch · Date & Time · Committee Members · Room/Mode (physical/video) · [View →]

---

### 5.3 Case Outcome Summary (This AY)

> High-level outcomes chart.

**Pie chart:** Warning / Hostel Suspension (1–7 days) / Hostel Suspension (8–30 days) / Permanent Hostel Expulsion / Case Dismissed.

**Bar chart:** Cases by type per month (last 12 months).

---

### 5.4 Pending Appeals

> Hosteler or parent appeals against committee decisions.

**Columns:** Appeal # · Case # · Hosteler · Branch · Original Decision · Appeal Reason · Appeal Date · Days Pending · [Review →]

---

## 6. Drawers

### 6.1 Drawer: `discipline-case-detail`
- **Trigger:** Case table → case # or row
- **Width:** 680px
- **Tabs:** Overview · Investigation · Hearings · Evidence · Decision · Appeal
- **Overview:** Hosteler details, case type, branch, welfare/security incident links, POCSO flag
- **Investigation:** Investigation notes, initial report, warden's statement, witness list
- **Hearings:** Scheduled and past hearings (date, committee members present, summary)
- **Evidence:** Uploaded files (photos, CCTV clip references, written statements)
- **Decision tab:** Final ruling, sanction type, effective dates, signed by, parent notified
- **Appeal tab:** Appeal history with each review and outcome

### 6.2 Drawer: `discipline-case-create`
- **Trigger:** + New Case
- **Width:** 640px
- **Fields:**
  - Branch
  - Hosteler (search autocomplete — gender locks Boys/Girls context)
  - Case Type (dropdown — if POCSO selected → mandatory POCSO Coordinator notification flag auto-set)
  - Incident Date + Time
  - Incident Description (textarea, min 100 chars)
  - Witnesses (repeatable name + role)
  - Warden's Initial Report (textarea)
  - Evidence Attachments (multi-file upload)
  - Initial Action Taken (textarea)
  - Linked Welfare Incident # (optional)
  - Linked Security Alert # (optional)
- **On submit:** Case created; audit log; if POCSO → POCSO Coordinator notified immediately

### 6.3 Modal: Issue Decision
- **Trigger:** Case detail → Issue Decision (only when investigation complete and hearing done)
- **Type:** Centred modal (520px)
- **Fields:**
  - Decision: Warning / Hostel Suspension (N days) / Permanent Hostel Expulsion / Case Dismissed
  - Effective From (date)
  - Decision Rationale (textarea, min 100 chars, required — immutable once saved)
  - Notify Parent (checkbox, mandatory for suspension/expulsion)
  - Notify Branch Principal (checkbox, default checked)
  - Signed by (committee member name — auto-filled from session)
- **On confirm:** Decision saved as immutable record; notifications sent; audit log

### 6.4 Modal: Schedule Hearing
- **Trigger:** Case table → Schedule Hearing
- **Type:** Centred modal (480px)
- **Fields:** Date · Time · Mode (Physical / Video) · Room/Link · Committee Members (multi-select from group staff) · Notify Hosteler (checkbox) · Notify Parent (checkbox)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Case created | "Discipline case #[ID] opened for [Hosteler Name]." | Success | 4s |
| POCSO case created | "Discipline case #[ID] created. POCSO Coordinator notified automatically." | Warning | 6s |
| Hearing scheduled | "Hearing for case #[ID] scheduled for [date time]." | Success | 4s |
| Decision issued | "Decision for case #[ID] issued. Parent and Branch Principal notified." | Success | 4s |
| Suspension active | "Hostel suspension for [Hosteler Name] is now active until [date]." | Warning | 6s |
| Case closed | "Discipline case #[ID] closed." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open cases | "No Active Discipline Cases" | "All hostel discipline cases are resolved." | — |
| No upcoming hearings | "No Hearings Scheduled" | "No discipline hearings are scheduled in the next 14 days." | — |
| No pending appeals | "No Pending Appeals" | — | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + case table (10 rows) + hearing list + charts |
| Table filter/search | Inline skeleton rows |
| KPI auto-refresh | Shimmer on card values |
| Decision modal confirm | Spinner + "Saving decision…" overlay (immutable write) |
| Case create drawer submit | Spinner on Submit; table row appended on success |

---

## 10. Role-Based UI Visibility

| Element | Discipline Committee G3 | Boys Coordinator G3 | Girls Coordinator G3 | Hostel Director G3 |
|---|---|---|---|---|
| Create Case | ✅ | ✅ Boys | ✅ Girls | ✅ |
| Schedule Hearing | ✅ | ❌ | ❌ | ✅ |
| Issue Decision | ✅ (requires Director co-sign for expulsion) | ❌ | ❌ | ✅ |
| View all genders | ✅ | ❌ Boys only | ❌ Girls only | ✅ |
| Review Appeal | ✅ | ❌ | ❌ | ✅ |
| Export cases | ✅ | ✅ | ✅ | ✅ |

> **Hostel Expulsion**: requires both Discipline Committee AND Hostel Director sign-off. Modal enforces dual approval.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/discipline/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/hostel/discipline/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/discipline/cases/` | JWT (G3+) | All cases (paginated, filtered) |
| GET | `/api/v1/group/{group_id}/hostel/discipline/cases/{id}/` | JWT (G3+) | Case detail |
| POST | `/api/v1/group/{group_id}/hostel/discipline/cases/` | JWT (G3+) | Create case |
| POST | `/api/v1/group/{group_id}/hostel/discipline/cases/{id}/schedule-hearing/` | JWT (G3+) | Schedule hearing |
| POST | `/api/v1/group/{group_id}/hostel/discipline/cases/{id}/decision/` | JWT (G3+) | Issue decision (immutable) |
| POST | `/api/v1/group/{group_id}/hostel/discipline/cases/{id}/close/` | JWT (G3+) | Close case |
| GET | `/api/v1/group/{group_id}/hostel/discipline/hearings/upcoming/` | JWT (G3+) | Upcoming hearings |
| GET | `/api/v1/group/{group_id}/hostel/discipline/appeals/` | JWT (G3+) | Pending appeals |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 10m` | GET `.../discipline/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Case search | `input delay:300ms` | GET `.../cases/?q={val}` | `#case-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../cases/?{filters}` | `#case-table-section` | `innerHTML` |
| Open case detail | `click` on case # | GET `.../cases/{id}/` | `#drawer-body` | `innerHTML` |
| Create case submit | `click` | POST `.../discipline/cases/` | `#case-table-section` | `innerHTML` |
| Issue decision confirm | `click` | POST `.../cases/{id}/decision/` | `#case-detail-decision-tab` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
