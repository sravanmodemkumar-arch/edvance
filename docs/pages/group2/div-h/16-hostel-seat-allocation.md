# 16 — Hostel Seat Allocation

> **URL:** `/group/hostel/admissions/seats/`
> **File:** `16-hostel-seat-allocation.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Hostel Admission Coordinator (primary) · Boys/Girls Coordinators · Hostel Director

---

## 1. Purpose

Cross-branch seat allocation planning tool. While the Admission Pipeline (Page 15) handles individual applications, this page provides a macro view for planning how many seats to allocate per branch, per gender, per room type at the start of each academic year — and for managing waitlists and reallocations when capacity shifts. This is the strategic planning layer on top of the operational pipeline.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Admissions  ›  Seat Allocation
```

### 2.2 Page Header
- **Title:** `Hostel Seat Allocation — AY [current]`
- **Subtitle:** `[N] Total Seats · [N] Allocated · [N] Available · [N] Waitlisted`
- **Right controls:** `+ Configure Seat Plan` · `Manage Waitlist` · `Export`

---

## 3. Seat Allocation Matrix

> Cross-branch seat plan — configurable at start of academic year.

**Table format:**
| Branch | Boys AC Seats | Boys Non-AC Seats | Girls AC Seats | Girls Non-AC Seats | Total Configured | Total Filled | Available |
|---|---|---|---|---|---|---|---|
| [Branch 1] | [N] | [N] | [N] | [N] | [N] | [N] | [N] |

**Editable cells** (only before academic year intake starts — locked after first admission):
- Seat count per cell configurable by Admission Coordinator or Hostel Director
- Cell turns amber when > 90% filled
- Cell turns red when fully allocated (0 available)

**Action column:** [View Applications] · [View Rooms] · [Adjust Seats]

---

## 4. Waitlist Management

> Prioritized waitlist for each hostel type per branch.

**Display:** Tabbed by hostel type: Boys AC | Boys Non-AC | Girls AC | Girls Non-AC

**Per-tab table:**
| Position | Student Name | Branch Requested | Applied On | Days Waiting | Actions |
|---|---|---|---|---|---|
| 1 | [Name] | [Branch] | [Date] | [N] | [Notify] [Allocate if seat opens] [Remove] |

**When a seat becomes available:** System shows a banner "1 seat now available in [Branch] Boys AC. [N] students on waitlist. [Allocate Next →]" with one-click allocation to the top waitlist position.

---

## 5. Drawers

### 5.1 Drawer: `seat-plan-configure`
- **Trigger:** + Configure Seat Plan
- **Width:** 560px
- **Fields:** Branch · AY · Boys AC capacity · Boys Non-AC capacity · Girls AC capacity · Girls Non-AC capacity · Notes (e.g., "20 seats reserved for scholarship hostelers")
- **On submit:** Seat plan saved; all fields locked until coordinator requests unlock

### 5.2 Drawer: `seat-adjust`
- **Trigger:** Branch row → Adjust Seats
- **Width:** 480px
- **Fields:** Which seat type to adjust · New count · Reason for adjustment (required)
- **Validation:** Cannot reduce below currently allocated count

---

## 6. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Seat plan saved | "Seat plan for [Branch] configured for AY [year]." | Success | 4s |
| Seat adjusted | "[Branch] Boys AC seats adjusted from [N] to [N]." | Info | 4s |
| Waitlist seat allocated | "Seat allocated to [Name] from waitlist position [N]." | Success | 4s |
| Student removed from waitlist | "[Name] removed from waitlist. Parent notified." | Info | 4s |

---

## 7. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/admissions/seat-plan/` | JWT (G3+) | Seat allocation matrix |
| POST | `/api/v1/group/{group_id}/hostel/admissions/seat-plan/` | JWT (G3+) | Configure seat plan per branch |
| PATCH | `/api/v1/group/{group_id}/hostel/admissions/seat-plan/{id}/` | JWT (G3+) | Adjust seat count |
| GET | `/api/v1/group/{group_id}/hostel/admissions/waitlist/` | JWT (G3+) | Waitlist (paginated, by hostel type) |
| POST | `/api/v1/group/{group_id}/hostel/admissions/waitlist/{id}/allocate/` | JWT (G3+) | Allocate from waitlist |
| DELETE | `/api/v1/group/{group_id}/hostel/admissions/waitlist/{id}/` | JWT (G3+) | Remove from waitlist |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
