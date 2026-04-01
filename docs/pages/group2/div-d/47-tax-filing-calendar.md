# 47 — Tax Filing Calendar

- **URL:** `/group/finance/tax/calendar/`
- **Template:** `portal_base.html`
- **Priority:** P2
- **Role:** GST/Tax Officer G1 (primary) · CFO G1

---

## 1. Purpose

The Tax Filing Calendar is a visual compliance calendar showing all statutory tax filing deadlines for the group across the financial year. It covers GST (GSTR-1, GSTR-3B, GSTR-9), TDS (26Q, 24Q, challan deposits), Income Tax (advance tax instalments), and Profession Tax (state-specific). Each event is linked to its source module so the Tax Officer can navigate directly to file.

The calendar surfaces overdue filings, approaching deadlines (within 7 days), and filed items in a single view — eliminating the need to track deadlines in a spreadsheet.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group GST/Tax Officer | G1 | Full read + mark filed |
| Group CFO | G1 | Read |
| Group Finance Manager | G1 | Read |
| Group Internal Auditor | G1 | Read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → GST & Tax → Tax Filing Calendar
```

### 3.2 Page Header
- **Title:** `Tax Filing Calendar`
- **Subtitle:** `FY [Year] · [N] Upcoming in 30 days · [X] Overdue`
- **Right-side controls:** `[FY ▾]` `[View: Calendar / List ▾]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| Any overdue filing | "[N] filing(s) overdue — penalty accruing." | Red |
| Filing due within 7 days | "[N] filing(s) due within 7 days." | Amber |

---

## 4. Calendar View

**Month navigator:** `[< Prev]` Month Year `[Next >]`

**Calendar Grid:** Standard month grid (Mon–Sun)

**Event types (colour-coded):**

| Colour | Type |
|---|---|
| 🔴 Red | Overdue / Not filed |
| 🟠 Orange | Due within 7 days |
| 🟢 Green | Filed on time |
| 🔵 Blue | Upcoming (> 7 days) |
| ⚫ Grey | Not applicable this month |

**Event tile format:**
```
[Icon] GSTR-3B — All GSTINs
       Due: 20-[Month]
       [Filed ✅ / Pending ⏳ / Overdue 🔴]
```

Clicking an event tile opens a detail drawer.

---

## 5. List View (alternate)

| Column | Type | Sortable |
|---|---|---|
| Filing | Text | ✅ |
| Type | Badge: GST · TDS · IT · PT | ✅ |
| GSTIN / Entity | Text | ✅ |
| Due Date | Date | ✅ |
| Status | Badge: Filed · Pending · Overdue | ✅ |
| Days Until Due | Number (red if negative) | ✅ |
| Last Filed | Date | ✅ |
| Actions | View Filing · Mark Filed | — |

### 5.1 Filters
- Type · Status · Month · Entity/GSTIN

### 5.2 Pagination
- 30 rows/page · Sort: Due Date asc

---

## 6. Filing Deadlines Master

| Filing | Period | Due Date | Notes |
|---|---|---|---|
| GSTR-1 (monthly) | Monthly | 11th of next month | Per GSTIN |
| GSTR-3B (monthly) | Monthly | 20th of next month | Per GSTIN |
| GSTR-9 (annual) | Annual FY | 31 December | Per GSTIN |
| TDS Deposit (non-March) | Monthly | 7th of next month | Per deductor |
| TDS Deposit (March) | March | 30 April | Per deductor |
| Form 26Q (TDS return) | Quarterly | 31 Jul / 31 Oct / 31 Jan / 31 May | Non-salary |
| Form 24Q (TDS return) | Quarterly | 31 Jul / 31 Oct / 31 Jan / 31 May | Salary |
| Advance Tax — 15% | Q1 | 15 June | Corporate |
| Advance Tax — 45% | Q2 | 15 September | Cumulative |
| Advance Tax — 75% | Q3 | 15 December | Cumulative |
| Advance Tax — 100% | Q4 | 15 March | Cumulative |
| Profession Tax (state) | Monthly | State-specific | Varies |

---

## 7. Drawer: `filing-detail` — Filing Event Detail
- **Width:** 640px

**Filing Summary:**
- Filing Type · Period · Due Date · Status

**Action Links:**
- [Go to GSTR-3B Dashboard] / [Go to TDS Tracker] (navigates to relevant page)

**Mark Filed Panel (if status = Pending):**

| Field | Type | Required |
|---|---|---|
| Filed Date | Date | ✅ |
| Reference No (ARN/ACK) | Text | ✅ |
| Notes | Textarea | ❌ |

- [Mark as Filed]

**Penalty Calculator (if overdue):**
- Days overdue: [N]
- Applicable penalty rate: ₹[X]/day
- Estimated penalty so far: ₹[Y]

---

## 8. Charts

### 8.1 Filing Compliance by Type (Donut)
- **Segments:** Filed on time · Filed late · Pending · Overdue

### 8.2 Upcoming Deadlines — Next 30 Days (Timeline/Gantt-style bar)
- Each filing as a horizontal bar on the timeline

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Filing marked | "[Filing] for [Period] marked as filed. Ref: [No]." | Success | 4s |
| Overdue alert | "[N] filings are overdue. Check calendar." | Warning | 5s |
| Export | "Tax calendar exported." | Info | 3s |

---

## 10. Empty States

| Condition | Heading | Description |
|---|---|---|
| All filed | "All filings complete" | "All tax filings for this period are done." |
| No filings this month | "Nothing due this month" | "No statutory filings due in the selected period." |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton calendar grid |
| Month switch | Calendar skeleton |
| Drawer | Spinner |

---

## 12. Role-Based UI Visibility

| Element | Tax Officer G1 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [Mark Filed] | ✅ | ❌ | ❌ |
| View all filings | ✅ | ✅ | ✅ |
| Penalty calculator | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/tax/calendar/` | JWT (G1+) | Filing calendar |
| GET | `/api/v1/group/{id}/finance/tax/calendar/?month=YYYY-MM` | JWT (G1+) | Filter by month |
| POST | `/api/v1/group/{id}/finance/tax/calendar/{fid}/mark-filed/` | JWT (G1) | Mark filing done |
| GET | `/api/v1/group/{id}/finance/tax/calendar/export/` | JWT (G1+) | Export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month navigation | `click` | GET `.../calendar/?month=YYYY-MM` | `#calendar-grid` | `innerHTML` |
| Event tile click | `click` | GET `.../calendar/{id}/` | `#drawer-body` | `innerHTML` |
| View toggle (Cal/List) | `click` | GET `.../calendar/?view=list` | `#calendar-container` | `innerHTML` |
| Mark filed | `submit` | POST `.../calendar/{id}/mark-filed/` | `#event-tile-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
