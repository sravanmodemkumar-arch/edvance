# 35 — Government Grant Tracker

- **URL:** `/group/finance/scholarship/grants/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Scholarship Finance Officer G3 (primary) · CFO G1 · Finance Manager G1

---

## 1. Purpose

The Government Grant Tracker manages all government scholarship and grant claims submitted to central and state agencies: National Scholarship Portal (NSP) Post-Matric scholarships, PRERANA (Andhra Pradesh), Kalyanamalai (Tamil Nadu), Central sector scholarships, and minority welfare scholarships. Each scheme has a distinct application process, eligibility criteria, claim submission deadline, and payment cycle.

The Finance Officer tracks: how many students are enrolled under each scheme, the total claim amount submitted, the amount received, and any rejected or pending claims. Government grants are often delayed by months — this page keeps the claim pipeline visible so follow-ups are timely.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Scholarship Finance Officer | G3 | Full read + update claim status |
| Group CFO | G1 | Read — amounts received |
| Group Finance Manager | G1 | Read |
| Group Internal Auditor | G1 | Read — audit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Scholarship Finance → Government Grant Tracker
```

### 3.2 Page Header
- **Title:** `Government Grant Tracker`
- **Subtitle:** `AY [Year] · [N] Schemes · ₹[Total Claimed] · ₹[Received]`
- **Right-side controls:** `[AY ▾]` `[Scheme ▾]` `[Branch ▾]` `[+ New Claim]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| Claim submission deadline within 15 days | "Claim deadline for [Scheme] on [Date]. [N] students not yet enrolled." | Red |
| Claim pending response > 90 days | "[Scheme] claim submitted [Date] with no response in 90 days. Follow up." | Amber |

---

## 4. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Scheme Name | Text | ✅ | ✅ |
| Agency | Text (NSP / State Dept / UGC) | ✅ | ✅ |
| Branch | Text | ✅ | ✅ |
| Students Enrolled | Count | ✅ | — |
| Claim Amount | ₹ | ✅ | — |
| Claim Submitted Date | Date | ✅ | — |
| Claim Deadline | Date | ✅ | — |
| Amount Received | ₹ | ✅ | — |
| Amount Pending | ₹ | ✅ | — |
| Status | Badge: Draft · Submitted · Partial Receipt · Fully Received · Rejected | ✅ | ✅ |
| Actions | View · Update Status | — | — |

### 4.1 Filters

| Filter | Type |
|---|---|
| Scheme | Multi-select |
| Status | Multi-select |
| Branch | Multi-select |
| AY | Select |

### 4.2 Search
- Scheme name

### 4.3 Pagination
- 20 rows/page

---

## 5. Drawers

### 5.1 Drawer: `claim-create` — New Grant Claim
- **Trigger:** [+ New Claim]
- **Width:** 680px

| Field | Type | Required |
|---|---|---|
| Scheme Name | Select (from master list) or Text | ✅ |
| Government Agency | Text | ✅ |
| Branch | Select (multi) | ✅ |
| AY | Select | ✅ |
| Number of Students | Number | ✅ |
| Claim Amount (total) | Number | ✅ |
| Claim Submission Date | Date | ✅ |
| Claim Deadline | Date | ✅ |
| Reference Number | Text | ❌ |
| Supporting Documents | File upload (PDF) | ❌ |
| Notes | Textarea | ❌ |

- [Cancel] [Save Draft] [Mark as Submitted]

### 5.2 Drawer: `claim-detail` — Claim Detail
- All claim metadata
- Receipt history (partial payments)
- Student list under this claim
- **[Update Status]** form: Status select + Amount Received + Reference

---

## 6. Scheme Master (Side panel)

Common government schemes pre-loaded:
- NSP Post-Matric (Central)
- PRERANA (Andhra Pradesh)
- Mukhyamantri Scholarship (State)
- Minority Welfare Scholarship
- SC/ST Scholarship (State)
- OBC Scholarship (Central)
- EWS Scholarship

---

## 7. Charts

### 7.1 Grant Claimed vs Received (Bar — by scheme)
### 7.2 Monthly Grant Receipt (Bar — last 12 months)

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Claim created | "Grant claim for '[Scheme]' created. [N] students · ₹[X]." | Success | 4s |
| Status updated | "Claim status updated: [Scheme] — ₹[X] received." | Success | 4s |
| Export | "Grant tracker exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No claims | "No grant claims" | "Record government scholarship claims." | [+ New Claim] |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Create drawer | Spinner + form |

---

## 11. Role-Based UI Visibility

| Element | Scholarship Finance G3 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [+ New Claim] | ✅ | ❌ | ❌ |
| [Update Status] | ✅ | ❌ | ❌ |
| View all | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/scholarship/grants/` | JWT (G1+) | Grant list |
| POST | `/api/v1/group/{id}/finance/scholarship/grants/` | JWT (G3) | Create claim |
| GET | `/api/v1/group/{id}/finance/scholarship/grants/{gid}/` | JWT (G1+) | Claim detail |
| PUT | `/api/v1/group/{id}/finance/scholarship/grants/{gid}/status/` | JWT (G3) | Update status |
| GET | `/api/v1/group/{id}/finance/scholarship/grants/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../grants/?scheme=&status=` | `#grant-section` | `innerHTML` |
| Create drawer | `click` | GET `.../grants/create-form/` | `#drawer-body` | `innerHTML` |
| Detail drawer | `click` | GET `.../grants/{id}/` | `#drawer-body` | `innerHTML` |
| Update status | `submit` | PUT `.../grants/{id}/status/` | `#grant-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
