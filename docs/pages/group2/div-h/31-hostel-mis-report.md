# 31 — Hostel MIS Report

> **URL:** `/group/hostel/reports/mis/`
> **File:** `31-hostel-mis-report.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Hostel Director (primary) · All hostel roles (view own section)

---

## 1. Purpose

Auto-generated monthly Management Information System (MIS) report covering all hostel KPIs for the reporting period — presented to the Group Chairman, Group CEO, Group CFO, and Group COO. The report consolidates data from all hostel sub-systems: occupancy, admissions, fees, welfare, security, medical, mess, and discipline into a single downloadable executive report.

The Hostel Director reviews and approves the MIS before it is distributed. Once approved, the report is locked (immutable) and distributed via email/WhatsApp to configured stakeholders.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Reports  ›  Hostel MIS
```

### 2.2 Page Header
- **Title:** `Hostel MIS Report`
- **Month selector:** Previous / current month toggle
- **Subtitle:** `Report for [Month Year] · Status: [Draft / Approved / Distributed]`
- **Right controls:** `Generate Report` · `Download PDF` · `Distribute to Stakeholders` (only after Approved status)

---

## 3. Report Sections (all in one page, scroll)

### 3.1 Executive Summary

| Metric | This Month | vs Last Month |
|---|---|---|
| Total Hostelers | [N] | +/- [N] |
| Occupancy Rate | [N]% | +/- [N]% |
| Fee Collection Rate | [N]% | +/- [N]% |
| Welfare Incidents (Total) | [N] | +/- [N] |
| Severity 1+2 Incidents | [N] | +/- [N] |
| Mess Hygiene Avg Score | [N]% | +/- [N]% |
| Security Incidents | [N] | +/- [N] |
| Discipline Cases Opened | [N] | +/- [N] |

---

### 3.2 Occupancy Summary

| Hostel Type | Total Capacity | Occupied | Occupancy % |
|---|---|---|---|
| Boys AC | [N] | [N] | [N]% |
| Boys Non-AC | [N] | [N] | [N]% |
| Girls AC | [N] | [N] | [N]% |
| Girls Non-AC | [N] | [N] | [N]% |
| **Total** | **[N]** | **[N]** | **[N]%** |

Chart: Occupancy bar per branch (top 10 + lowest 5).

---

### 3.3 Admission Summary

| Metric | Count |
|---|---|
| New Admissions This Month | [N] |
| Applications Pending | [N] |
| Waitlisted | [N] |
| Exits (This Month) | [N] |

---

### 3.4 Fee Collection Summary

| Category | Billed | Collected | Collection % |
|---|---|---|---|
| Accommodation | ₹[N] | ₹[N] | [N]% |
| Mess | ₹[N] | ₹[N] | [N]% |
| Extras | ₹[N] | ₹[N] | [N]% |
| **Total** | **₹[N]** | **₹[N]** | **[N]%** |

Defaulters (30d+): [N]. Outstanding > 60d: ₹[N].

---

### 3.5 Welfare Summary

| Severity | This Month | Resolved | SLA Compliance |
|---|---|---|---|
| Severity 1 | [N] | [N] | [N]% |
| Severity 2 | [N] | [N] | [N]% |
| Severity 3 | [N] | [N] | [N]% |
| Severity 4 | [N] | [N] | [N]% |

POCSO-linked incidents: [N]. Top incident type: [type].

---

### 3.6 Mess & Hygiene Summary

| Metric | Value |
|---|---|
| Audits Conducted | [N] |
| Average Score | [N]% |
| Failing Mess Halls | [N] |
| Corrective Actions Pending | [N] |
| FSSAI Alerts | [N] |

---

### 3.7 Security Summary

| Metric | Value |
|---|---|
| Security Incidents | [N] |
| Unauthorized Visitor Entries | [N] |
| CCTV Downtime Events | [N] |
| Night Roll Call Discrepancies | [N] |

---

### 3.8 Medical Summary

| Metric | Value |
|---|---|
| Medical Room Visits | [N] |
| Medical Emergencies | [N] |
| Hostelers on Medical Watch | [N] |
| Doctor Visits Conducted | [N] |

---

### 3.9 Discipline Summary

| Metric | Value |
|---|---|
| Cases Opened | [N] |
| Decisions Issued | [N] |
| Suspensions | [N] |
| Expulsions | [N] |
| Appeals Filed | [N] |

---

### 3.10 Director's Commentary (optional free text)

> Hostel Director adds a 100–500 word narrative commentary on key highlights and concerns before approval.

**Field spec:** `textarea` — resizable, full width.
- **Minimum:** 100 characters (soft guard — if the Director clicks Approve with fewer than 100 characters, a warning appears below the field: "Commentary is too brief. Please add at least 100 characters before approving.")
- **Maximum:** 3000 characters (~500 words) hard limit; input blocked beyond this.
- **Live character counter:** `[N / 3000 characters]` displayed bottom-right of the textarea in gray; turns amber when ≥ 2700 characters to warn the Director they are approaching the limit.

---

## 4. Approval & Distribution

1. Director reviews all sections → adds commentary → clicks [Approve Report]
2. Report status changes to Approved; PDF locked
3. [Distribute to Stakeholders] button enabled → sends PDF via email + WhatsApp to: Chairman / CEO / CFO / COO (as configured in group settings)
4. Distribution log recorded in audit log

---

## 5. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Report generated | "Hostel MIS for [Month] generated. Review before approving." | Info | 5s |
| Report approved | "Hostel MIS for [Month] approved and locked." | Success | 4s |
| Report distributed | "Hostel MIS distributed to [N] stakeholders." | Success | 4s |

---

## 6. Loader States

| Trigger | Loader Type |
|---|---|
| Generate Report click | Full-page overlay: "Compiling data from all hostel sub-systems… [progress bar]" |
| Download PDF | Spinner on Download button |
| Approve Report | Spinner on Approve button |

---

## 7. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/reports/mis/?month={m}&year={y}` | JWT (G3+) | Load/generate MIS data |
| POST | `/api/v1/group/{group_id}/hostel/reports/mis/{id}/generate/` | JWT (G3+) | Regenerate from source data |
| PATCH | `/api/v1/group/{group_id}/hostel/reports/mis/{id}/commentary/` | JWT (G3+) | Add director commentary |
| POST | `/api/v1/group/{group_id}/hostel/reports/mis/{id}/approve/` | JWT (G3+) | Approve report |
| POST | `/api/v1/group/{group_id}/hostel/reports/mis/{id}/distribute/` | JWT (G3+) | Distribute to stakeholders |
| GET | `/api/v1/group/{group_id}/hostel/reports/mis/{id}/pdf/` | JWT (G3+) | Download locked PDF |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
