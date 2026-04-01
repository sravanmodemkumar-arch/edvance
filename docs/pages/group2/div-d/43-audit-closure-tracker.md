# 43 — Audit Closure Tracker

- **URL:** `/group/finance/audit/closure/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Internal Auditor G1 (primary) · Finance Manager G1

---

## 1. Purpose

The Audit Closure Tracker monitors the end-to-end lifecycle of all audits from scheduling to closure — tracking each step: scheduled → in progress → findings raised → management response → sign-off → formally closed. It provides the Internal Auditor and Finance Manager with a clear view of which audits are stuck, which findings remain open, and whether the closure quality (response adequacy) meets audit standards.

This is the master governance view for the audit function — complementing the planner (scheduling) and findings report (individual findings). It answers: "Is the audit complete, and are we done?"

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Internal Auditor | G1 | Full read + close audits |
| Group Finance Manager | G1 | Read + sign off |
| Group CFO | G1 | Read — summary |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Internal Audit → Audit Closure Tracker
```

### 3.2 Page Header
- **Title:** `Audit Closure Tracker`
- **Subtitle:** `FY [Year] · [N] Audits · [X] Closed · [Y] Pending Closure`
- **Right-side controls:** `[FY ▾]` `[Quarter ▾]` `[Branch ▾]` `[Export ↓]`

---

## 4. Main Table

| Column | Type | Sortable |
|---|---|---|
| Audit ID | Text | ✅ |
| Branch | Text | ✅ |
| Quarter | Text | ✅ |
| Audit Period | Date range | ✅ |
| Total Findings | Count | ✅ |
| Open Findings | Count (red if >0) | ✅ |
| Closed Findings | Count | ✅ |
| Checklist Completion | % | ✅ |
| Management Response | Badge: Complete · Partial · Pending | ✅ |
| Finance Mgr Sign-off | Badge: Signed Off · Pending | ✅ |
| Audit Status | Badge: In Progress · Pending Closure · Closed | ✅ |
| Days Since Audit End | Number (red if >30 and not closed) | ✅ |
| Actions | View · Close Audit | — |

### 4.1 Filters
- Branch · Quarter · Status · Days overdue range

### 4.2 Pagination
- 20 rows/page · Sort: Days since audit end desc

---

## 5. Drawers

### 5.1 Drawer: `audit-closure-detail` — Audit Closure Detail
- **Width:** 760px

**Closure Readiness Checklist:**

| Item | Status |
|---|---|
| Audit conducted (dates) | ✅ [Date] – [Date] |
| Checklist completed | [X%] (require ≥ 95%) |
| All findings have management response | ✅ / ❌ [N pending] |
| Critical findings closed | ✅ / ❌ |
| Finance Manager sign-off | ✅ / ❌ |
| Audit report uploaded | ✅ / ❌ |

**[Close Audit]** — enabled only when all items ✅

Closure requires:
- Closure note
- Auditor sign-off
- Finance Manager sign-off (separate toggle)

---

## 6. Summary Panel

| Metric | Value |
|---|---|
| Avg Days to Close (FY) | [N] days |
| % Audits Closed within 30 days | [X]% |
| Longest Open Audit | [Branch] — [N] days |

---

## 7. Charts

### 7.1 Audit Closure Status (Donut)
### 7.2 Avg Days to Closure by Branch (Bar)

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit closed | "Audit for [Branch] — Q[N] formally closed." | Success | 4s |
| Sign-off recorded | "Finance Manager sign-off recorded for [Branch] audit." | Success | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| All audits closed | "All audits closed" | "All branch audits are formally closed for this quarter." |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/audit/closure/` | JWT (G1+) | Closure tracker list |
| GET | `/api/v1/group/{id}/finance/audit/closure/{aid}/` | JWT (G1+) | Audit closure detail |
| POST | `/api/v1/group/{id}/finance/audit/closure/{aid}/close/` | JWT (G1) | Close audit |
| POST | `/api/v1/group/{id}/finance/audit/closure/{aid}/sign-off/` | JWT (G1, Finance Mgr) | Finance sign-off |
| GET | `/api/v1/group/{id}/finance/audit/closure/export/` | JWT (G1+) | Export |

---

## 11. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../closure/?quarter=&status=` | `#closure-table` | `innerHTML` |
| Detail drawer | `click` | GET `.../closure/{id}/` | `#drawer-body` | `innerHTML` |
| Close audit | `click` | POST `.../closure/{id}/close/` | `#audit-row-{id}` | `outerHTML` |
| Sign-off | `click` | POST `.../closure/{id}/sign-off/` | `#closure-signoff-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
