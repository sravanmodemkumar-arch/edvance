# 33 — Collection Drive Manager

- **URL:** `/group/finance/collection/drives/`
- **Template:** `portal_base.html`
- **Priority:** P2
- **Role:** Fee Collection Head G3 (primary)

---

## 1. Purpose

The Collection Drive Manager enables the Fee Collection Head to create, track, and close targeted collection campaigns across branches. A collection drive defines a target (e.g., "Clear all Term 2 outstanding by March 15"), the branches covered, the target student segment, and the tactics used (reminders, principal escalation, payment plan offers).

Collection drives are time-bound with a clear target amount and a measurable outcome — collection rate improvement. The manager monitors daily progress and adjusts tactics mid-drive if collection is not improving.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Collection Head | G3 | Full CRUD |
| Group Finance Manager | G1 | Read |
| Group CFO | G1 | Read — summary |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Collection → Collection Drive Manager
```

### 3.2 Page Header
- **Title:** `Collection Drive Manager`
- **Subtitle:** `[N] Active Drives · [N] Completed`
- **Right-side controls:** `[+ New Drive]` `[Export ↓]`

---

## 4. Main Table

| Column | Type | Sortable |
|---|---|---|
| Drive Name | Text | ✅ |
| Target Segment | Badge | ✅ |
| Branches | Count | ✅ |
| Target Amount | ₹ | ✅ |
| Collected So Far | ₹ | ✅ |
| Achievement % | % (progress bar) | ✅ |
| Start Date | Date | ✅ |
| End Date | Date | ✅ |
| Status | Badge: Active · Completed · Overdue | ✅ |
| Actions | View · Edit · Close · Delete (draft) | — |

**Filters:** Status · Branch · Date range
**Search:** Drive name
**Pagination:** 20 rows/page

---

## 5. Drawers

### 5.1 Drawer: `drive-create` — Create Collection Drive
- **Width:** 680px

| Field | Type | Required |
|---|---|---|
| Drive Name | Text | ✅ |
| Description | Textarea | ❌ |
| Target Segment | Select: All Defaulters · Term Specific · Installment Overdue · Hostel Dues | ✅ |
| Applicable Branches | Multi-select | ✅ |
| Target Amount | Number | ✅ |
| Start Date | Date | ✅ |
| End Date | Date | ✅ |
| Tactics | Multi-select: WhatsApp Reminders · SMS · Principal Escalation · Payment Plan Offer · Penalty Waiver Incentive | ✅ |
| Reminder Frequency | Select: Daily · Every 2 days · Weekly | ❌ |

- [Cancel] [Save Draft] [Launch Drive]

### 5.2 Drawer: `drive-detail` — Drive Progress
- **Trigger:** View action
- **Width:** 720px

**Progress Summary:**
- Target: ₹[X] | Collected: ₹[Y] | Achievement: [Z]%
- Progress bar
- Days remaining: [N]

**Tab: Branch Progress**

| Branch | Target | Collected | % | Defaulters Cleared | Remaining |
|---|---|---|---|---|---|

**Tab: Daily Collection Trend**
- Mini line chart for this drive period

**Tab: Tactics Log**
- Actions taken: reminders sent (date + count), escalations, etc.

---

## 6. Charts

### 6.1 Drive Achievement % (Horizontal Bar — per drive)
### 6.2 Collection During Drive vs Before Drive (Comparison bar)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Drive launched | "Collection drive '[Name]' launched for [N] branches." | Success | 4s |
| Drive closed | "Drive '[Name]' closed. Achievement: [X]%." | Info | 4s |
| Export | "Drive report exported." | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No drives | "No collection drives" | "Create a drive to tackle outstanding dues." | [+ New Drive] |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Detail drawer | Spinner + skeleton |

---

## 10. Role-Based UI Visibility

| Element | Collection Head G3 | Finance Mgr G1 | CFO G1 |
|---|---|---|---|
| [+ New Drive] | ✅ | ❌ | ❌ |
| [Edit · Close · Delete] | ✅ | ❌ | ❌ |
| View drives | ✅ | ✅ | ✅ (summary) |
| Export | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/collection/drives/` | JWT (G1+) | Drive list |
| POST | `/api/v1/group/{id}/finance/collection/drives/` | JWT (G3) | Create drive |
| GET | `/api/v1/group/{id}/finance/collection/drives/{did}/` | JWT (G1+) | Drive detail + progress |
| PUT | `/api/v1/group/{id}/finance/collection/drives/{did}/` | JWT (G3) | Update drive |
| POST | `/api/v1/group/{id}/finance/collection/drives/{did}/close/` | JWT (G3) | Close drive |
| DELETE | `/api/v1/group/{id}/finance/collection/drives/{did}/` | JWT (G3) | Delete draft |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Create drawer | `click` | GET `.../drives/create-form/` | `#drawer-body` | `innerHTML` |
| Detail drawer | `click` | GET `.../drives/{id}/` | `#drawer-body` | `innerHTML` |
| Close drive | `click` | POST `.../drives/{id}/close/` | `#drive-row-{id}` | `outerHTML` |
| Submit create | `submit` | POST `.../drives/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
