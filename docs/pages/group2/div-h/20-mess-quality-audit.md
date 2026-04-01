# 20 — Mess Quality Audit

> **URL:** `/group/hostel/mess/quality/`
> **File:** `20-mess-quality-audit.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Mess Manager (primary) · Hostel Director (view + override) · Welfare Officer (view)

---

## 1. Purpose

Structured hygiene and food quality audit system for all hostel mess halls. The Group Mess Manager conducts or reviews audits from branch visits; branch-level supervisors can submit self-audits that are reviewed here. Each audit generates a score (0–100) against a standardized checklist, and failing scores (< 60) automatically alert the Hostel Director and flag the branch in the Director's dashboard.

FSSAI (Food Safety and Standards Authority of India) compliance is tracked as part of the audit — caterer FSSAI license validity is checked at each audit.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Mess Operations  ›  Quality Audit
```

### 2.2 Page Header
- **Title:** `Mess Quality Audit`
- **Subtitle:** `[N] Audits This Month · Avg Score: [N]% · [N] Failing Mess Halls · [N] FSSAI Alerts`
- **Right controls:** `+ New Audit` · `Advanced Filters` · `Export`

---

## 3. Audit Table

**Search:** Branch name, auditor name. 300ms debounce.

**Filters:** Branch · Audit Type (Physical/Self) · Result (Pass/Fail) · Date range · Auditor.

**Columns:**
| Column | Sortable |
|---|---|
| Audit # | ✅ |
| Branch | ✅ |
| Audit Date | ✅ |
| Auditor | ✅ |
| Type | ✅ (Physical / Self-audit) |
| Overall Score | ✅ |
| Result | ✅ (Pass ≥ 60% / Fail < 60%) |
| FSSAI Valid | ✅ |
| Corrective Action | ✅ (Required / Completed / N/A) |
| Actions | ❌ (View · Download Report) |

---

## 4. Audit Checklist (used in Create drawer)

| Category | Items | Max Score |
|---|---|---|
| Kitchen Cleanliness | Floors / Walls / Equipment / Exhaust | 20 |
| Food Storage | Temperature / Segregation / Expiry dates | 15 |
| Food Preparation | Hygiene practices / Cross-contamination / PPE | 20 |
| Serving Area | Utensil cleanliness / Counter hygiene / Food covers | 15 |
| Staff Hygiene | Medical fitness certificates / Handwashing / Uniform | 15 |
| Waste Management | Disposal / Pest control / Drainage | 10 |
| FSSAI Compliance | License displayed / Valid / Cert current | 5 |
| **Total** | | **100** |

Each item: ✅ Compliant / ❌ Non-compliant / N/A.

Score = (compliant items / applicable items) × 100.

---

## 5. Drawers

### 5.1 Drawer: `quality-audit-create`
- **Trigger:** + New Audit
- **Width:** 600px
- **Tabs:** Details · Checklist · Photos · Summary
- **Details tab:** Branch · Audit date · Auditor name · Audit type · Caterer on duty
- **Checklist tab:** Full checklist (above) with Per-item: ✅/❌/N/A + Notes field
- **Photos tab:** Multi-photo upload (kitchen, storage, serving area — min 2 photos required for physical audit)
- **Summary tab:** Auto-calculated score + Pass/Fail badge + Corrective actions required (auto-listed from failed items) + Corrective action deadline (date picker) + Notify Branch Mess Supervisor (checkbox)
- **On submit:** Audit saved; if score < 60 → Hostel Director and Mess Manager alerted; corrective action deadline set

### 5.2 Drawer: `quality-audit-detail`
- **Trigger:** Table → View
- **Width:** 640px
- **Tabs:** Overview · Checklist Results · Photos · Corrective Actions · Comparison
- **Comparison tab:** This audit score vs previous 3 audits for same branch (trend line)

---

## 6. Corrective Action Tracker

> Section below audit table listing all unresolved corrective actions.

**Columns:** Branch · Audit Date · Failed Items (count) · Corrective Action Deadline · Status (Open/Closed) · [View →]

Red rows for overdue corrective actions.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit submitted (Pass) | "Hygiene audit for [Branch] submitted. Score: [N]% — PASS." | Success | 4s |
| Audit submitted (Fail) | "HYGIENE FAIL: [Branch] scored [N]%. Hostel Director notified." | Warning | 6s |
| Corrective action closed | "Corrective action for [Branch] audit #[ID] marked complete." | Success | 4s |

---

## 8. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/mess/audits/` | JWT (G3+) | All audits (paginated, filtered) |
| GET | `/api/v1/group/{group_id}/hostel/mess/audits/{id}/` | JWT (G3+) | Audit detail |
| POST | `/api/v1/group/{group_id}/hostel/mess/audits/` | JWT (G3+) | Submit audit |
| PATCH | `/api/v1/group/{group_id}/hostel/mess/audits/{id}/corrective-action/` | JWT (G3+) | Update corrective action status |
| GET | `/api/v1/group/{group_id}/hostel/mess/audits/corrective-actions/` | JWT (G3+) | All open corrective actions |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
