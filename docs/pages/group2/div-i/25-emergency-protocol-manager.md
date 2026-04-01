# 25 — Emergency Protocol Manager

> **URL:** `/group/transport/safety/emergency-protocols/`
> **File:** `25-emergency-protocol-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Transport Safety Officer (primary) · Transport Director

---

## 1. Purpose

Manages emergency response protocols for all transport scenarios — vehicle breakdown, accident, medical emergency, fire, flood route, student missing, and SOS activation. Each protocol defines the response steps, responsible personnel, contact numbers, and escalation chain.

Every branch and every driver must have access to the applicable protocols. The Safety Officer creates and updates protocols; branch transport in-charges must acknowledge receipt. Emergency contacts must be verified quarterly.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Safety Officer | G3 | Full — create, edit, publish | Primary owner |
| Group Transport Director | G3 | Approve protocols | Approval authority |
| Branch Transport In-Charge | Branch G3 | Read + acknowledge | View only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Emergency Protocol Manager
```

### 3.2 Page Header
- **Title:** `Emergency Protocol Manager`
- **Subtitle:** `[N] Active Protocols · [N] Pending Acknowledgement · Last Review: [date]`
- **Right controls:** `+ New Protocol` · `Review Emergency Contacts` · `Export All Protocols`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Protocol not reviewed in > 90 days | "[N] protocols have not been reviewed in > 90 days." | Amber |
| Branch acknowledgement pending > 30 days | "[N] branches have not acknowledged updated protocols." | Amber |
| Emergency contacts not verified in > 90 days | "Emergency contact list not verified in > 90 days. Review required." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Active Protocols | Total published | Blue |
| Branches Fully Acknowledged | % | Green = 100% · Red < 90% |
| Protocols Pending Review | Past 90-day review cycle | Yellow > 0 |
| Emergency Contacts Verified | Last verified date | Green < 30d · Red > 90d |

---

## 5. Sections

### 5.1 Protocol Library Table

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Protocol Type | Checkbox | Accident / Breakdown / Medical / Fire / Missing Student / SOS / Flood / Other |
| Status | Radio | Active / Draft / Retired |
| Acknowledgement | Radio | All / Pending / Fully Acknowledged |

**Columns:** Protocol Name · Type · Version · Last Updated · Applicable Branches · Acknowledgement Status · Actions (View · Edit · Publish · Retire)

---

### 5.2 Emergency Contact Directory

> Key contacts to be called during any transport emergency — verified quarterly.

**Columns:** Contact Name · Role · Phone Number · Branch / Organisation · Last Verified · [Verify Now]

Contacts include: Nearest hospital (per branch) · Police station · Fire station · Group COO · Transport Director · Branch Principal · Ambulance.

---

## 6. Drawers

### 6.1 Drawer: `protocol-create`
- **Width:** 680px
- **Fields:** Protocol Name · Type · Version · Applicable Branches (multi-select) · Response Steps (multi-row: step number, action description, responsible person role, time target) · Emergency Contacts referenced · Review Cycle (days) · Notes

### 6.2 Drawer: `protocol-detail`
- **Width:** 680px
- **Tabs:** Protocol Content · Acknowledgements · Version History
- **Protocol Content:** All steps, contacts, version
- **Acknowledgements:** Which branches have acknowledged, pending branches, send reminder button
- **Version History:** All past versions with dates and author

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Protocol published | "Protocol [Name] published to [N] branches." | Success | 4s |
| Publish failed | "Failed to publish protocol. Please retry." | Error | 5s |
| Acknowledgement reminder | "Acknowledgement reminder sent to [N] branches." | Info | 4s |
| Reminder failed | "Failed to send acknowledgement reminder. Please retry." | Error | 5s |
| Emergency contacts verified | "Emergency contacts verified. Next review in 90 days." | Info | 4s |
| Verification failed | "Failed to mark contacts as verified. Please retry." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No protocols | "No Emergency Protocols" | "Create emergency response protocols for all transport scenarios." | [+ New Protocol] |
| All acknowledged | "All Branches Acknowledged" | "All branches have acknowledged current protocols." | — |
| No filter results | "No Protocols Match Filters" | "Adjust protocol type, status, or acknowledgement filters." | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 4 KPI cards + protocol table + contact directory |
| Protocol detail drawer | 680px skeleton |

---

## 10. Role-Based UI Visibility

| Element | Safety Officer G3 | Transport Director G3 | Branch Transport In-Charge |
|---|---|---|---|
| Create Protocol | ✅ | ✅ (approve) | ❌ |
| Edit Protocol | ✅ | ❌ | ❌ |
| Publish Protocol | ✅ | ✅ (approve) | ❌ |
| Acknowledge Protocol | ❌ | ❌ | ✅ |
| View All Protocols | ✅ | ✅ | ✅ (own branch) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/safety/protocols/` | JWT (G3+) | Protocol list |
| POST | `/api/v1/group/{group_id}/transport/safety/protocols/` | JWT (G3+) | Create protocol |
| GET | `/api/v1/group/{group_id}/transport/safety/protocols/{id}/` | JWT (G3+) | Protocol detail |
| PATCH | `/api/v1/group/{group_id}/transport/safety/protocols/{id}/` | JWT (G3+) | Update protocol |
| POST | `/api/v1/group/{group_id}/transport/safety/protocols/{id}/publish/` | JWT (G3+) | Publish to branches |
| POST | `/api/v1/group/{group_id}/transport/safety/protocols/{id}/acknowledge/` | JWT (Branch) | Branch acknowledge |
| GET | `/api/v1/group/{group_id}/transport/safety/emergency-contacts/` | JWT (G3+) | Contact directory |
| PATCH | `/api/v1/group/{group_id}/transport/safety/emergency-contacts/{id}/verify/` | JWT (G3+) | Verify emergency contact |
| GET | `/api/v1/group/{group_id}/transport/safety/protocols/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/safety/protocols/export/` | JWT (G3+) | Export all protocols |

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Protocol table filter | `click` | GET `.../protocols/?{filters}` | `#protocol-table-section` | `innerHTML` |
| Protocol table sort | `click` on header | GET `.../protocols/?sort={col}&dir={asc/desc}` | `#protocol-table-section` | `innerHTML` |
| Protocol table pagination | `click` | GET `.../protocols/?page={n}` | `#protocol-table-section` | `innerHTML` |
| Open protocol detail drawer | `click` on Protocol Name | GET `.../protocols/{id}/` | `#drawer-body` | `innerHTML` |
| Create protocol submit | `click` | POST `.../protocols/` | `#protocol-table-section` | `innerHTML` |
| Publish confirm | `click` | POST `.../protocols/{id}/publish/` | `#protocol-row-{id}` | `outerHTML` |
| Send acknowledgement reminder | `click` | POST `.../protocols/{id}/reminder/` | `#reminder-btn-{id}` | `outerHTML` |
| Verify emergency contact | `click` | PATCH `.../emergency-contacts/{id}/verify/` | `#contact-row-{id}` | `outerHTML` |
| Export | `click` | GET `.../protocols/export/` | `#export-btn` | `outerHTML` |

> **Audit trail:** All write actions (create, publish, acknowledge protocol; verify contacts) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
