# 19 — Procurement Request Manager

> **URL:** `/group/ops/procurement/requests/`
> **File:** `19-procurement-request-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full) · Operations Manager G3 (approve ≤₹1L, view all)

---

## 1. Purpose

Manages the full lifecycle of procurement requests from branches. Branch admins submit
requests via their portal; Group COO/Ops Manager reviews, approves or rejects, and may
consolidate multiple similar requests into a single bulk Purchase Order for cost savings.

---

## 2. Request Lifecycle

```
Branch Submits → Group Review → [Approve / Reject / Consolidate] → PO Created → Delivered
```

**Consolidation:** Multiple branches requesting the same item (e.g., 8 branches need graph
paper) → consolidated into single PO to get bulk discount.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Procurement  ›  Request Manager
```

### 3.2 Page Header
```
Procurement Request Manager            [+ Log Request]  [Consolidate Selected]  [Export ↓]
[N] pending · [N] approved · [N] rejected this month
```

### 3.3 Status Tabs
```
[All]  [Pending (N)]  [Under Review (N)]  [Approved (N)]  [Rejected (N)]  [Consolidated (N)]
```

---

## 4. Search & Filters

**Search:** Request ID, branch, item description, category. 300ms debounce.

**Advanced Filters:**
| Filter | Options |
|---|---|
| Category | Books · Uniforms · Lab Equipment · IT Hardware · Stationery · Furniture · Other |
| Branch | Multi-select |
| Zone | Multi-select |
| Status | Pending · Under Review · Approved · Rejected · Consolidated |
| Amount | ≤₹1L · ₹1L–₹5L · ₹5L–₹10L · >₹10L |
| Priority | Urgent · Normal |
| Date Range | Custom |

---

## 5. Requests Table

**Default sort:** Submitted date descending (newest first) for Pending tab.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| ☐ | Checkbox | For bulk consolidation |
| REQ ID | ✅ | REQ-YYYY-NNNNN |
| Category | ✅ | Colour badge |
| Branch | ✅ | |
| Zone | ✅ | |
| Items Summary | ✅ | "5 items — see details" |
| Est. Amount | ✅ | ₹ |
| Priority | ✅ | Urgent / Normal |
| Submitted | ✅ | Date |
| Days Pending | ✅ | Red if >7 days for Urgent, >14 for Normal |
| Status | ✅ | |
| Actions | — | View · Approve · Reject · Add to PO |

**Bulk actions:** Consolidate Selected (min 2 items, same category) · Bulk Approve · Export CSV.

**Pagination:** Server-side · 25/page.

---

## 6. Request Detail Drawer

- **Width:** 640px
- **Tabs:** Items · Budget · Branch Info · History

**Items tab:**
Table of requested items:
| Item | Description | Quantity | Unit | Est. Unit Price | Est. Total |
|---|---|---|---|---|---|
| Textbooks (Maths Cl.10) | XYZ Publisher | 150 | copies | ₹180 | ₹27,000 |

**Budget tab:**
- Category budget remaining: `₹4.2L of ₹10L remaining`
- Impact of this request: `-₹27,000`
- Similar approved requests this month: list

**Branch Info tab:**
- Branch details, past request history, approval rate

**History tab:**
- Timeline: submitted → reviewed → approved/rejected

**Actions (in drawer):**
- [Approve] · [Reject with Reason] · [Add to Existing PO] · [Create New PO for This Request]

---

## 7. Consolidation Workflow

**Trigger:** Select 2+ requests with same category → [Consolidate Selected]

**Consolidation drawer (520px):**
- Lists selected requests: Request IDs, branches, items, amounts
- Shows combined item list (merged quantities)
- Estimated bulk discount: `5% assumed for >₹1L same-vendor order`
- Combined total: `₹1.4L (estimated)`
- [Create Consolidated PO →] → Pre-fills Page 21 PO form with consolidated items

---

## 8. Log Request Drawer (manual entry)

> For requests received offline or from branches without portal access.

- **Width:** 560px
- **Fields:** Branch · Category · Priority · Items (add line items) · Justification · Requested by · Urgent toggle

---

## 9. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Approved | "Request [ID] approved — branch notified" | Success · 4s |
| Rejected | "Request [ID] rejected with reason" | Warning · 4s |
| Consolidated | "Requests consolidated — PO creation started" | Success · 4s |
| Bulk approved | "[N] requests approved" | Success · 4s |

---

## 10. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No pending | "No pending requests" | — |
| No results | "No requests match search" | [Clear Filters] |

---

## 11. Loader States

Page load: Skeleton status tabs + summary + table.
Filter/search: Inline skeleton rows.
Drawer: Spinner in body.

---

## 12. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 |
|---|---|---|
| [Approve] any amount | ✅ | ≤₹1L only |
| [Reject] any amount | ✅ | ≤₹1L only |
| [Consolidate] | ✅ | ✅ |
| [Log Request] | ✅ | ✅ |
| Export | ✅ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/procurement/requests/` | JWT (G3+) | List with filters |
| GET | `/api/v1/group/{id}/procurement/requests/{req_id}/` | JWT (G3+) | Detail |
| POST | `/api/v1/group/{id}/procurement/requests/` | JWT (G3+) | Create request |
| POST | `/api/v1/group/{id}/procurement/requests/{req_id}/approve/` | JWT (G3+) | Approve |
| POST | `/api/v1/group/{id}/procurement/requests/{req_id}/reject/` | JWT (G3+) | Reject |
| POST | `/api/v1/group/{id}/procurement/requests/consolidate/` | JWT (G3+) | Consolidate selected |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | `/api/.../requests/?status={}` | `#req-table-section` | `innerHTML` |
| Search | `input delay:300ms` | `/api/.../requests/?q={}` | `#req-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../requests/?filters={}` | `#req-table-section` | `innerHTML` |
| Open detail | `click` | `/api/.../requests/{id}/` | `#drawer-body` | `innerHTML` |
| Approve | `click` | POST `/api/.../requests/{id}/approve/` | `#req-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
