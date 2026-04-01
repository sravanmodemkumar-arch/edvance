# 15 — Hostel Admission Pipeline

> **URL:** `/group/hostel/admissions/pipeline/`
> **File:** `15-hostel-admission-pipeline.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Hostel Admission Coordinator (primary) · Boys/Girls Coordinators · Hostel Director

---

## 1. Purpose

End-to-end hostel admission pipeline for all branches. Tracks every hostel application from submission through document verification, seat allocation, parent consent, and final confirmation — or waitlisting and rejection. The pipeline is the single source of truth for hostel admission status and integrates with the Hosteler Registry (Page 12) to auto-create records upon confirmation.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Admissions  ›  Admission Pipeline
```

### 2.2 Page Header
- **Title:** `Hostel Admission Pipeline`
- **Subtitle:** `AY [current] · [N] Applications · [N] Pending · [N] Confirmed · [N] Waitlisted`
- **Right controls:** `+ New Application` · `Bulk Import CSV` · `Export` · `Advanced Filters`

---

## 3. Kanban / Stage View (default)

> Applications shown as cards in column stages.

**Stages (horizontal scroll):**
```
Received → Document Verification → Seat Allocation → Parent Consent → Confirmed
[N cards]      [N cards]               [N cards]          [N cards]       [N cards]
```

Also: **Waitlisted** column · **Rejected** column (collapsed, expandable).

**Card mini-view:**
- Name + gender badge
- Class / Stream
- Branch + hostel type preference
- Days in this stage
- [View] [Move →]

**Drag-to-move** between stages (updates status via PATCH API).

---

## 4. Table View (toggle)

**Same data as Kanban but in a sortable table.**

**Columns:**
| Column | Sortable |
|---|---|
| Application ID | ✅ |
| Student Name | ✅ |
| Gender | ✅ |
| Branch | ✅ |
| Stream | ✅ |
| Hostel Type Pref | ✅ |
| Applied On | ✅ |
| Stage | ✅ |
| Documents | ✅ (✅ Complete / ⚠ Pending) |
| Days in Stage | ✅ |
| Seat Assigned | ✅ |
| Actions | ❌ |

**Advanced Filters:** Branch · Gender · Stage · Document Status · Days in Stage > N · Hostel Type.

**Pagination:** Server-side · 25/page.

---

## 5. Document Verification Checklist

> Required documents per application (visible in application drawer).

| Document | Required | Status |
|---|---|---|
| Birth Certificate / Transfer Certificate | Yes | ✅ / ❌ / ⚠ Pending |
| Parent ID Proof (Aadhaar) | Yes | |
| Medical Fitness Certificate | Yes | |
| Fee Advance Receipt | Yes | |
| Parent Consent Form (signed) | Yes | |
| Special Needs Certificate | Only if applicable | |

Applications with incomplete documents cannot move past "Document Verification" stage.

---

## 6. Drawers

### 6.1 Drawer: `application-detail`
- **Width:** 640px
- **Tabs:** Applicant · Documents · Stage History · Actions
- **Actions tab:** Move to next stage · Allocate Seat · Add to Waitlist · Reject
- **Stage History:** Immutable log of all stage changes with actor + timestamp

### 6.2 Drawer: `application-create`
- **Width:** 640px
- **Fields:** (Detailed — see Page 06 Admission Coordinator Dashboard Section 6.2)

### 6.3 Modal: Bulk Import CSV
- **Type:** Centred modal (520px)
- **Content:** File upload + template download link
- **Validation:** Required columns listed; preview before import; row-level error report

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Application moved to next stage | "Application #[ID] moved to [Stage]." | Info | 3s |
| Document verified | "Documents for [Name] marked complete." | Success | 3s |
| Seat allocated | "Seat allocated: [Room#/Bed] at [Branch] for [Name]." | Success | 4s |
| Waitlisted | "[Name] added to waitlist at position [N]." | Info | 4s |
| Rejected | "Application #[ID] rejected." | Warning | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No applications | "No Hostel Applications" | "No applications have been submitted for this academic year." | [+ New Application] |
| Stage empty | "No Applications in [Stage]" | — | — |

---

## 9. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/admissions/applications/` | JWT (G3+) | All applications (paginated, filtered) |
| POST | `/api/v1/group/{group_id}/hostel/admissions/applications/` | JWT (G3+) | Create |
| PATCH | `/api/v1/group/{group_id}/hostel/admissions/applications/{id}/` | JWT (G3+) | Update stage / status |
| POST | `/api/v1/group/{group_id}/hostel/admissions/applications/{id}/allocate/` | JWT (G3+) | Allocate seat |
| POST | `/api/v1/group/{group_id}/hostel/admissions/applications/bulk-import/` | JWT (G3+) | CSV import |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
