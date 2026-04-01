# 28 — Hostel Discipline Cases

> **URL:** `/group/hostel/discipline/cases/`
> **File:** `28-hostel-discipline-cases.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Hostel Discipline Committee (primary) · Hostel Director · Boys/Girls Coordinators (view)

---

## 1. Purpose

Complete discipline case management — the full-detail page for all hostel discipline cases. While the Discipline Committee Dashboard (Page 11) shows the active case queue with quick actions, this page is the searchable archive of all cases (open, closed, appealed, historical) with complete case records, immutable decision logs, and appeal management.

All discipline decisions once issued are immutable — they create an audit trail entry and cannot be edited or deleted. Appeals are tracked as a separate linked record.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Discipline  ›  Cases
```

### 2.2 Page Header
- **Title:** `Hostel Discipline Cases`
- **Subtitle:** `AY [current] · Open: [N] · Pending Decision: [N] · POCSO-linked: [N] · Closed: [N]`
- **Right controls:** `+ New Case` · `Advanced Filters` · `Export`

---

## 3. Case Table

**Search:** Case #, hosteler name, branch, keyword. 300ms debounce.

**Advanced Filters:**
| Filter | Type |
|---|---|
| Branch | Multi-select |
| Gender | Radio: All/Boys/Girls |
| Case Type | Multi-select (all types) |
| Status | Checkbox: Investigation/Hearing Scheduled/Pending Decision/Decision Issued/Appeal/Closed |
| POCSO Linked | Checkbox |
| Decision Type | Checkbox: Warning/Suspension/Expulsion/Dismissed |
| Date Range | Date picker (opened between) |

**Columns:**
| Column | Sortable |
|---|---|
| Case # | ✅ |
| Hosteler Name | ✅ |
| Gender | ✅ |
| Branch | ✅ |
| Case Type | ✅ |
| Opened | ✅ |
| Status | ✅ |
| POCSO | ✅ |
| Decision | ✅ (blank if pending) |
| Effective Date | ✅ |
| Actions | ❌ |

**Pagination:** Server-side · 25/page.

---

## 4. Drawers

### 4.1 Drawer: `discipline-case-detail`
- **Width:** 680px
- **Tabs:** Overview · Investigation · Hearings · Evidence · Decision · Appeal
- **Overview:** Hosteler details (name, gender, branch, class, room number), case type, POCSO flag, linked welfare incident, linked security alert
- **Investigation tab:**
  - Initial incident report (from warden or coordinator)
  - Investigation notes (added by committee)
  - Witness statements (viewable)
  - Timeline of investigation actions
- **Hearings tab:**
  - Scheduled and past hearings: Date · Time · Mode · Committee present · Summary notes
  - [+ Schedule Hearing] button
- **Evidence tab:**
  - Uploaded files: CCTV clip references, photos, written statements
  - [+ Add Evidence] button (only before decision issued)
- **Decision tab:**
  - Final ruling (immutable once issued): Decision type · Rationale · Effective period · Signed by · Issued at
  - Notification log (parent notified at / Principal notified at)
  - If pending: [Issue Decision →] button
- **Appeal tab:**
  - Appeal submissions with reason, filed by, filed at
  - Committee response with decision (Upheld / Overturned / Modified)
  - [File Appeal →] button (if decision issued and appeal window open — 7 days after decision)

### 4.2 Drawer: `discipline-case-create` (see Page 11 Section 6.2 for full spec)

### 4.3 Modal: `schedule-hearing` (see Page 11 Section 6.4)

### 4.4 Modal: `issue-decision` (see Page 11 Section 6.3)

### 4.5 Modal: `review-appeal`
- **Trigger:** Appeal tab → Review Appeal
- **Type:** Centred modal (520px)
- **Fields:** Appeal outcome (Upheld / Overturned / Modified) · Revised decision (if Modified) · Rationale (required) · Notify hosteler and parent (checkbox)
- **Note:** Appeal review is also immutable once submitted.

---

## 5. Case Outcome Analytics

> Bottom section of page — summary charts for the current academic year.

**Chart 1 — Cases by Type (Pie):** Distribution of case types.

**Chart 2 — Cases by Branch (Bar):** Branch-wise case count.

**Chart 3 — Case Outcomes (Pie):** Warning / Suspension (1–7d) / Suspension (8–30d) / Expulsion / Dismissed.

**Chart 4 — Monthly Cases (Line):** Cases opened per month for current AY.

---

## 6. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Case created | "Discipline case #[ID] opened." | Success | 4s |
| Hearing scheduled | "Hearing for case #[ID] scheduled for [date]." | Success | 4s |
| Decision issued | "Decision issued for case #[ID]. Notifications sent." | Success | 4s |
| Appeal reviewed | "Appeal for case #[ID] reviewed. Decision: [outcome]." | Info | 5s |
| Case closed | "Case #[ID] closed." | Success | 4s |

---

## 7. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/discipline/cases/` | JWT (G3+) | All cases (paginated, filtered) |
| POST | `/api/v1/group/{group_id}/hostel/discipline/cases/` | JWT (G3+) | Create case |
| GET | `/api/v1/group/{group_id}/hostel/discipline/cases/{id}/` | JWT (G3+) | Case full detail |
| POST | `/api/v1/group/{group_id}/hostel/discipline/cases/{id}/add-evidence/` | JWT (G3+) | Upload evidence |
| POST | `/api/v1/group/{group_id}/hostel/discipline/cases/{id}/schedule-hearing/` | JWT (G3+) | Schedule hearing |
| POST | `/api/v1/group/{group_id}/hostel/discipline/cases/{id}/decision/` | JWT (G3+) | Issue decision (immutable) |
| POST | `/api/v1/group/{group_id}/hostel/discipline/cases/{id}/appeal/` | JWT (G3+) | File appeal |
| POST | `/api/v1/group/{group_id}/hostel/discipline/cases/{id}/appeal/review/` | JWT (G3+) | Review appeal (immutable) |
| POST | `/api/v1/group/{group_id}/hostel/discipline/cases/{id}/close/` | JWT (G3+) | Close case |
| GET | `/api/v1/group/{group_id}/hostel/discipline/cases/analytics/` | JWT (G3+) | Outcome analytics |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
