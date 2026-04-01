# 17 — Security Guard Roster

> **URL:** `/group/welfare/security/guards/`
> **File:** `17-security-guard-roster.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group CCTV & Security Head (Role 93, G3)

---

## 1. Purpose

Manages security guard deployment across all branches — guard profiles, shift assignments, attendance, vendor details, and compliance with minimum guard requirements. Guards are typically hired from security agencies under contract. Each branch has minimum guard requirements based on campus type:

- **Day School:** 2 guards minimum — 1 at gate, 1 roving.
- **Residential Campus:** 4 guards minimum — gate + boys hostel + girls hostel + perimeter.
- **Large Campus with separate blocks:** 6+ guards required.

The CCTV & Security Head ensures: every shift is filled with a guard possessing a valid license, guard PSARA (Private Security Agencies Regulation Act) licenses are current, agency contracts are active, and any substitution or absence is immediately flagged and covered. A shift without a guard or a guard deployed without a valid PSARA license is a legal and welfare compliance failure.

Scale: 2–10 guards per branch · 40–500 guards total · 24/7 shift coverage across all branches.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group CCTV & Security Head | G3 | Full — view, add, edit, mark absent, assign replacement, view agency contracts | Primary owner |
| Group COO | G4 | View — branch compliance summary and vacancies only; read-only | Cannot edit guard records |
| Branch Security Supervisor | G2 | View own branch guards; can mark attendance for own branch only | Cannot add guards or modify agency contracts |
| Branch Principal | G2 | View — own branch guard count and shift coverage summary only | No individual guard details |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('cctv_security_head', 'branch_security_supervisor')` with branch-scope filter applied for G2.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Security  ›  Security Guard Roster
```

### 3.2 Page Header
```
Security Guard Roster                  [+ Add Guard]  [Export Roster ↓]  [Settings ⚙]
[Group Name] — Group CCTV & Security Head · Last refreshed: [timestamp]
[N] Total Guards  ·  [N] Branches  ·  [N] On Duty Now  ·  [N] Absent Today  ·  [N] Vacancies
```

### 3.3 Alert Banner (conditional — operational gaps requiring immediate action)

| Condition | Banner Text | Severity |
|---|---|---|
| Shift unfilled at any branch | "[N] shift(s) across [N] branch(es) have no guard assigned for today. Unfilled shifts: [list of Branch + Post + Shift]." | Red |
| Guard absent with no replacement | "Guard [Name] at [Branch] — [Post] is marked absent with no replacement assigned for [Shift]." | Red |
| PSARA license expired | "[N] guard(s) have expired PSARA licenses and are currently deployed: [names]. Immediate action required." | Red |
| PSARA license expiring within 7 days | "[N] guard(s) have PSARA licenses expiring within 7 days. Initiate renewal immediately." | Amber |
| Agency contract expired | "Agency contract with [Agency Name] for [Branch] has expired. Guards cannot be deployed under an expired contract." | Red |
| Branch below minimum guard requirement | "[N] branch(es) are below the minimum guard requirement for their campus type: [Branch list]." | Amber |

Max 5 alerts visible. Alert links route to filtered table rows or the relevant guard profile. "View full security log →" shown below alerts.

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Guards | Total registered guards across all branches (active + on leave) | Blue always (informational) | → Main table (no filter) |
| Branches Below Minimum | Branches not meeting the minimum guard count for their campus type | Green = 0 · Yellow 1–3 · Red > 3 | → Section 5.2 |
| Guards On Duty Now | Guards marked as Present Today and currently in an active shift window | Green = adequate · Yellow = 1–3 posts uncovered · Red = any critical post uncovered | → Main table filtered to Present Today = Yes |
| License Expiring Within 30 Days | Guards with PSARA license expiry within 30 days | Green = 0 · Yellow 1–5 · Red > 5 | → Main table filtered to expiry ≤ 30 days |
| Absent Today | Guards marked absent today across all branches | Green = 0 · Yellow 1–5 · Red > 5 | → Main table filtered to Present Today = No |
| Vacancies Unfilled | Defined guard posts with no guard currently assigned | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.2 |
| Expired PSARA Licenses (Active Guards) | Guards currently deployed with an expired PSARA license | Green = 0 · Red if any | → Main table filtered to License Expiry < today and Present = Yes |
| Agency Contracts Expiring ≤ 30 Days | Contracts with agencies expiring within 30 days | Green = 0 · Yellow 1–2 · Red > 2 | → Section 5.3 |

**HTMX:** `hx-trigger="every 5m"` → Guards On Duty Now, Absent Today, and Vacancies Unfilled auto-refresh.

---

## 5. Sections

### 5.1 Guard Roster Table (Primary Table)

> Full roster of all security guards across all branches with shift and compliance status.

**Search:** Guard name, agency, PSARA license number, branch name. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Agency / Vendor | Multi-select | All registered agencies |
| Post | Checkbox | Gate / Boys Hostel / Girls Hostel / Perimeter / Admin Block |
| Shift | Checkbox | Morning (6AM–2PM) / Afternoon (2PM–10PM) / Night (10PM–6AM) |
| License Expiry Status | Radio | All · Valid · Expiring ≤ 30 Days · Expired |
| Present Today | Radio | All · Yes · No · On Leave |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Guard Name | ✅ | Full name; link → `guard-profile` drawer |
| Branch | ✅ | Branch name |
| Agency / Vendor | ✅ | Agency name |
| Post | ✅ | Gate / Boys Hostel / Girls Hostel / Perimeter / Admin Block — badge |
| Shift | ✅ | Morning (Blue) / Afternoon (Green) / Night (Dark) badge |
| PSARA License No. | ✅ | License number |
| License Valid Until | ✅ | Date; Red if expired · Orange if ≤ 30 days · Green if > 30 days |
| Present Today | ✅ | Yes (Green ✅) / No (Red ❌) / On Leave (Grey) |
| Agency Contract Status | ✅ | Active (Green) / Expiring Soon (Amber) / Expired (Red) |
| Actions | ❌ | View · Mark Absent/Present · Replace |

**Default sort:** License Valid Until ascending (expired first), then Present Today (absent first), then Branch.
**Pagination:** Server-side · 25/page.

---

### 5.2 Branch Guard Compliance Panel

> Per-branch view of guard deployment vs minimum requirements.

**Display:** Summary table.

**Columns:**
| Column | Notes |
|---|---|
| Branch | Branch name |
| Campus Type | Day School / Residential / Large Multi-Block |
| Required Guards | Minimum count per campus type |
| Assigned Guards | Currently assigned and active count |
| On Duty Today | Guards present and in an active shift |
| Vacancies | Required − Assigned; Red if > 0 |
| PSARA Compliance | % of assigned guards with valid license |
| Overall Status | Badge: Compliant (Green) · Understaffed (Red) · License Gap (Amber) |
| Actions | View Guards · Assign · View Contract |

**Default sort:** Overall Status (Understaffed first, then License Gap, then Compliant).
**Pagination:** Server-side · 25/page.

---

### 5.3 Agency Contract Overview

> Summary of all security agency contracts, renewal dates, and compliance.

**Display:** Card list — one card per agency.

**Each card shows:**
- Agency name · State registration number
- Branches covered (count and names in tooltip)
- Contract start date · Contract expiry date · Days until expiry (Red if ≤ 30 days)
- Number of guards deployed under this agency
- Contract status badge: Active / Expiring Soon / Expired
- Actions: [View Contract Detail] [Renew/Extend]

**Trigger:** "View Contract Detail" → opens `agency-contract-detail` drawer.

---

## 6. Drawers / Modals

### 6.1 Drawer: `guard-profile`
- **Trigger:** Guard name link in Section 5.1 table
- **Width:** 560px
- **Tabs:** Profile · License · Assignments · Attendance · Incidents · Leave

**Profile tab:**
| Field | Notes |
|---|---|
| Guard Name | Read-only |
| Employee / Guard ID | System-generated or agency-assigned |
| Branch | Current branch assignment |
| Agency | Agency name |
| Post | Current post assignment |
| Shift | Current shift |
| Date of Joining | Date with this agency at this branch |
| Date of Birth | Read-only |
| Contact Number | Phone number |
| Emergency Contact | Name and phone |
| Address | Residential address |
| Photo | Profile photo (if uploaded) |

**License tab:**
| Field | Notes |
|---|---|
| PSARA License Number | Read-only |
| Issuing Authority | State/District |
| License Valid From | Date |
| License Valid Until | Date; Red badge if expired or within 30 days |
| Training Certifications | List: Certification name · Issuing body · Expiry |
| Upload License Document | [Upload PDF/Image] — G3 only |
| Renewal Reminder | Toggle — auto-send reminder 60 days before expiry |

**Assignments tab:**
- Assignment history: Branch · Post · Shift · Start Date · End Date (or "Current") · Reason for transfer
- Paginated if > 10 records

**Attendance tab:**
- Last 30 days attendance calendar view: Present (Green) / Absent (Red) / On Leave (Grey) / Holiday (Light Grey)
- Summary: Present [N] days · Absent [N] days · On Leave [N] days

**Incidents tab:**
- Security incidents this guard was on duty for: Incident ID · Date · Type · Severity · Status
- Link to full incident record → Page 19

**Leave tab:**
- Leave balance: Annual / Sick / Emergency
- Leave history: Start Date · End Date · Type · Status (Approved / Pending / Rejected) · Approved By

---

### 6.2 Drawer: `add-guard`
- **Trigger:** [+ Add Guard] button in page header
- **Width:** 560px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Searchable dropdown | Required |
| Post | Select | Gate / Boys Hostel / Girls Hostel / Perimeter / Admin Block · Required |
| Shift | Select | Morning / Afternoon / Night · Required |
| Agency / Vendor | Searchable dropdown (registered agencies) | Required |
| Guard Full Name | Text · max 100 chars | Required |
| Date of Birth | Date picker | Required; must be 18+ years |
| Contact Number | Text · 10-digit mobile | Required; validated format |
| Emergency Contact Name | Text · max 100 chars | Required |
| Emergency Contact Phone | Text · 10-digit mobile | Required |
| PSARA License Number | Text · max 50 chars | Required; uniqueness check across group |
| License Issuing Authority | Text · max 100 chars | Required |
| License Valid From | Date picker | Required |
| License Valid Until | Date picker | Required; must be future date |
| Date of Joining | Date picker | Required; cannot be future date |
| Annual Leave Entitlement | Number | Required; default 15 days |
| Photo | File upload · JPG/PNG · max 2MB | Optional |

**Validation:**
- PSARA License Number must be unique across the group.
- Guard must be 18+ years based on date of birth.
- License Valid Until must be after joining date.
- If license is already expired at time of adding, show error: "Cannot add a guard with an expired PSARA license. Renewal required before registration."

**Footer:** [Cancel] [Save Guard →]

---

### 6.3 Drawer: `mark-absent-replacement`
- **Trigger:** "Mark Absent" action in table row or from alert banner link
- **Width:** 440px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Guard Name | Read-only pre-filled | — |
| Branch | Read-only pre-filled | — |
| Post | Read-only pre-filled | — |
| Shift | Read-only pre-filled | — |
| Date | Date picker | Required; defaults to today |
| Absence Type | Radio | Sick / Personal / Unauthorised · Required |
| Absence Note | Textarea · max 300 chars | Required for Unauthorised |
| Replacement Guard | Searchable dropdown | Filters to: same branch, same shift, Available (not already assigned for this slot) |
| Replacement Confirmation | Checkbox | "I confirm the replacement guard has been notified and has a valid PSARA license" · Required if replacement selected |
| Replacement Note | Textarea · max 200 chars | Optional |
| Notify Agency | Toggle | Default: ON — sends notification to agency supervisor |
| Notify Branch Principal | Toggle | Default: ON |

**Validation:**
- If no replacement is selected, system shows a warning: "This post will be unmanned for this shift. This creates a security gap. Confirm to proceed without replacement?"
- Replacement guard must have a valid (non-expired) PSARA license — enforced server-side.

**Footer:** [Cancel] [Save Absence Record →]

---

### 6.4 Drawer: `agency-contract-detail`
- **Trigger:** "View Contract Detail" in Section 5.3 agency cards or from guard profile Agency field link
- **Width:** 520px

**Fields (read-only unless editing):**
| Field | Notes |
|---|---|
| Agency Name | Full legal name |
| State PSARA Registration Number | Agency's registration |
| Branches Covered | Multi-select list of branches |
| Contract Start Date | Date |
| Contract End Date | Date; Red if expired or within 30 days |
| Contract Value (Annual) | Amount in INR |
| Pay Rate Per Guard Per Day | INR |
| Escalation Clause | Text — e.g., "5% annual increment on renewal" |
| Notice Period for Termination | Days |
| Renewal Contact Name | Name |
| Renewal Contact Phone | Phone |
| Renewal Contact Email | Email |
| Contract Document | [View PDF] link if uploaded |
| Notes | Freetext contract notes |

**Actions (G3 only):**
- [Edit Contract Details] — inline edit of editable fields
- [Mark as Renewed] — date picker for new end date + upload new document
- [Terminate Contract] — confirm dialog with reason field

**Guard List sub-section:**
- List of all guards at this agency currently deployed: Name · Branch · Post · Shift · License Status
- Paginated if > 10 guards

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Guard added successfully | "Guard [Name] added at [Branch] — [Post], [Shift] shift." | Success | 4s |
| Attendance marked — Present | "Guard [Name] marked present for [date]." | Success | 3s |
| Absence recorded — with replacement | "Absence recorded for [Name]. [Replacement Name] assigned as replacement." | Success | 4s |
| Absence recorded — no replacement | "Absence recorded for [Name]. Warning: [Post] post is unmanned for [Shift] shift at [Branch]." | Warning | 6s |
| PSARA license uploaded | "PSARA license document uploaded for [Name]. Expiry: [date]." | Success | 4s |
| Agency contract renewed | "Contract with [Agency Name] renewed until [date]." | Success | 4s |
| License expiry reminder set | "Automatic renewal reminder set for [Name] — 60 days before [expiry date]." | Info | 4s |
| Roster exported | "Guard roster export is being prepared. Download will begin shortly." | Info | 4s |
| Guard deactivated | "Guard [Name] has been deactivated and removed from active roster." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No guards registered | "No Guards in Roster" | "No security guards have been registered. Add guards to begin tracking shift coverage and compliance." | [+ Add Guard] |
| No guards at selected branch | "No Guards at This Branch" | "No guards are currently assigned to the selected branch." | [+ Add Guard] |
| No absent guards today | "Full Attendance Today" | "All guards across all branches are marked present for today's shifts." | — |
| No vacancies | "All Posts Filled" | "All guard posts across all branches are currently filled." | — |
| No expiring licenses | "All PSARA Licenses Valid" | "No guard licenses are expiring within the next 30 days." | — |
| Search returns no results | "No Guards Found" | "No guards match your search terms or applied filters." | [Clear Filters] |
| No agency contracts | "No Agency Contracts Registered" | "No security agency contracts have been added. Register an agency before adding guards." | [Register Agency] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + guard roster table (15 rows × 10 columns) + branch compliance panel + agency cards (3 skeletons) + alerts |
| Table filter/search | Inline skeleton rows (8 rows × 10 columns) |
| KPI auto-refresh | Shimmer on Guards On Duty Now, Absent Today, Vacancies Unfilled card values |
| Guard profile drawer open | 560px drawer skeleton with 6-tab bar and field skeletons |
| Attendance tab | Calendar skeleton (30 cells, 5×6 grid) |
| Add guard form open | 560px drawer with 16 field skeletons |
| Mark absent/replacement drawer | 440px drawer with 8 field skeletons |
| Agency contract drawer open | 520px drawer with field skeletons + guard list table (5 rows) |
| Branch compliance panel | Table skeleton (10 rows × 8 columns) |

---

## 10. Role-Based UI Visibility

| Element | CCTV & Security Head G3 | Group COO G4 | Branch Security Supervisor G2 | Branch Principal G2 |
|---|---|---|---|---|
| View All Branches Roster | ✅ | ❌ (compliance summary only) | Own branch only | Own branch summary only |
| Add Guard | ✅ | ❌ | ❌ | ❌ |
| Mark Attendance | ✅ | ❌ | ✅ (own branch) | ❌ |
| Assign Replacement | ✅ | ❌ | ✅ (own branch) | ❌ |
| View Guard Personal Details | ✅ | ❌ | ✅ (own branch) | ❌ |
| View Agency Contracts | ✅ | ✅ (read-only) | ❌ | ❌ |
| Edit Agency Contract | ✅ | ❌ | ❌ | ❌ |
| Upload PSARA Document | ✅ | ❌ | ❌ | ❌ |
| Export Roster | ✅ | ✅ (aggregate) | ✅ (own branch) | ❌ |
| Alert Banner | ✅ (all alerts) | ✅ (read-only) | ✅ (own branch alerts) | ❌ |
| Deactivate Guard | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/security/guards/` | JWT (G3+) | Guard roster table; params: `branch_id`, `agency_id`, `post`, `shift`, `license_status`, `present_today`, `q`, `page` |
| GET | `/api/v1/group/{group_id}/welfare/security/guards/kpi-cards/` | JWT (G3+) | KPI auto-refresh payload |
| GET | `/api/v1/group/{group_id}/welfare/security/guards/branch-compliance/` | JWT (G3+) | Branch guard compliance panel |
| GET | `/api/v1/group/{group_id}/welfare/security/guards/agencies/` | JWT (G3+) | Agency contract overview cards |
| GET | `/api/v1/group/{group_id}/welfare/security/guards/{guard_id}/` | JWT (G3+) | Guard profile drawer payload |
| POST | `/api/v1/group/{group_id}/welfare/security/guards/` | JWT (G3) | Create new guard record |
| PATCH | `/api/v1/group/{group_id}/welfare/security/guards/{guard_id}/` | JWT (G3) | Update guard details |
| POST | `/api/v1/group/{group_id}/welfare/security/guards/{guard_id}/attendance/` | JWT (G3, G2-branch) | Mark attendance (present / absent / leave) |
| POST | `/api/v1/group/{group_id}/welfare/security/guards/{guard_id}/replace/` | JWT (G3, G2-branch) | Record absence and assign replacement |
| GET | `/api/v1/group/{group_id}/welfare/security/agencies/{agency_id}/` | JWT (G3+) | Agency contract detail drawer payload |
| PATCH | `/api/v1/group/{group_id}/welfare/security/agencies/{agency_id}/` | JWT (G3) | Update agency contract |
| POST | `/api/v1/group/{group_id}/welfare/security/agencies/{agency_id}/renew/` | JWT (G3) | Mark contract as renewed with new end date |
| GET | `/api/v1/group/{group_id}/welfare/security/guards/export/` | JWT (G3+) | Async roster export (CSV/XLSX) |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../guards/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Guard table search | `input delay:300ms` | GET `.../guards/?q={val}` | `#guard-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../guards/?{filters}` | `#guard-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../guards/?page={n}` | `#guard-table-section` | `innerHTML` |
| Open guard profile drawer | `click` on Guard Name | GET `.../guards/{id}/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch (lazy) | `click` on tab | GET `.../guards/{id}/?tab={name}` | `#drawer-tab-content` | `innerHTML` |
| Mark absent + replacement | `click` confirm | POST `.../guards/{id}/replace/` | `#guard-row-{id}` | `outerHTML` |
| Mark present | `click` | POST `.../guards/{id}/attendance/` | `#guard-row-{id}` | `outerHTML` |
| Open agency contract drawer | `click` on agency card | GET `.../agencies/{id}/` | `#drawer-body` | `innerHTML` |
| Branch compliance panel load | `load` | GET `.../guards/branch-compliance/` | `#compliance-panel` | `innerHTML` |
| Agency cards load | `load` | GET `.../guards/agencies/` | `#agency-panel` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
