# 26 — Stream-wise Fee Setup

- **URL:** `/group/finance/fee-structure/stream-fees/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Fee Structure Manager G3 (primary) · CFO G1 (view)

---

## 1. Purpose

Stream-wise fee setup manages fee components that vary by academic stream: MPC students may pay extra lab fees for physics/chemistry practicals, BiPC students for biology labs, and MEC/CEC students for commerce lab/computer lab. Integrated JEE/NEET coaching fees and IIT Foundation fees are also configured here as stream-specific additions to the base tuition fee.

This page ensures the platform enforces stream-based billing accurately — a MPC student is automatically billed the correct lab fees without manual intervention by the branch accountant.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Structure Manager | G3 | Full CRUD + publish |
| Group CFO | G1 | Read-only |
| Group CAO (Academic) | G4 | Read — stream definitions |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Structure → Stream-wise Fee Setup
```

### 3.2 Page Header
- **Title:** `Stream-wise Fee Setup`
- **Subtitle:** `AY [Year] · [N] Streams Configured`
- **Right-side controls:** `[AY ▾]` `[Branch ▾]` `[Export ↓]`

---

## 4. Main Table — Stream Fee Status

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| MPC | Badge: Configured · Missing | ✅ |
| BiPC | Badge | ✅ |
| MEC | Badge | ✅ |
| CEC | Badge | ✅ |
| HEC | Badge | ✅ |
| IIT Foundation (Cl.6-10) | Badge | ✅ |
| JEE/NEET Integrated | Badge | ✅ |
| Actions | Configure · View | — |

---

## 5. Drawers

### 5.1 Drawer: `stream-fee-config` — Configure Stream Fees for Branch
- **Trigger:** Configure
- **Width:** 800px

**Tabs:** One per stream (MPC · BiPC · MEC · CEC · HEC · IIT Foundation · JEE/NEET)

Each tab:

| Fee Component | Amount (₹) | Frequency | Notes |
|---|---|---|---|
| Stream Lab Fee | Input | Annual | Physics/Chemistry/Biology etc. |
| Practical Exam Fee | Input | Per exam | |
| Stream Material Fee | Input | Annual | Books + printouts |
| Coaching Additional Fee | Input | Monthly | JEE/NEET only |
| Foundation Program Fee | Input | Monthly | IIT Foundation only |
| [+ Add Custom Component] | | | |

**Note field:** "Why does this stream charge differently?" — stored in audit trail.

- [Save Draft] [Publish for This Stream]

---

## 6. Charts

### 6.1 Stream Fee Comparison Across Branches (Grouped Bar)
- **Groups:** MPC · BiPC · MEC · CEC · JEE/NEET Integrated
- **Sort:** By branch

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Stream fees configured | "Stream fees configured for [Branch] — [Stream]." | Success | 4s |
| Published | "Stream fees published for [Branch] — [Stream]." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| No streams configured | "No stream fees" | "Configure stream-wise fees for this academic year." |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Config drawer | Spinner + skeleton tabs |

---

## 10. Role-Based UI Visibility

| Element | Fee Struct Mgr G3 | CFO G1 |
|---|---|---|
| [Configure] | ✅ | ❌ |
| [Publish] | ✅ | ❌ |
| View | ✅ | ✅ |
| Export | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/fee-structure/stream-fees/` | JWT (G1+) | Stream fee status |
| GET | `/api/v1/group/{id}/finance/fee-structure/stream-fees/{bid}/{stream}/` | JWT (G1+) | Stream fee detail |
| PUT | `/api/v1/group/{id}/finance/fee-structure/stream-fees/{bid}/{stream}/` | JWT (G3) | Update |
| POST | `/api/v1/group/{id}/finance/fee-structure/stream-fees/{bid}/{stream}/publish/` | JWT (G3) | Publish |
| GET | `/api/v1/group/{id}/finance/fee-structure/stream-fees/export/` | JWT (G1+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Config drawer | `click` | GET `.../stream-fees/{bid}/config-form/` | `#drawer-body` | `innerHTML` |
| Tab switch | `click` | GET `.../stream-fees/{bid}/{stream}/` | `#stream-tab-body` | `innerHTML` |
| Publish stream | `click` | POST `.../stream-fees/{bid}/{stream}/publish/` | `#stream-status-{stream}` | `outerHTML` |
| AY switch | `change` | GET `.../stream-fees/?ay=` | `#stream-fee-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
