# 21 — Mess Vendor Management

> **URL:** `/group/hostel/mess/vendors/`
> **File:** `21-mess-vendor-management.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Mess Manager (primary) · Hostel Director (view)

---

## 1. Purpose

Management of caterer/vendor contracts for all hostel mess halls. Each branch mess is managed by either an in-house team or an outsourced caterer under a time-bound contract. This page tracks all active and historical caterer contracts, payment status, FSSAI license validity, and performance ratings from audit scores.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Mess Operations  ›  Vendor Management
```

### 2.2 Page Header
- **Title:** `Mess Vendor Management`
- **Subtitle:** `[N] Active Contracts · [N] Expiring in 30 Days · [N] FSSAI Alerts`
- **Right controls:** `+ New Vendor` · `Advanced Filters` · `Export`

### 2.3 Alert Banner
| Condition | Banner | Severity |
|---|---|---|
| Contract expiring ≤ 30 days | "[N] caterer contracts expiring within 30 days. Initiate renewal." | Amber |
| FSSAI license expired | "[N] caterers have expired FSSAI licenses. Compliance breach — suspend mess operations." | Red |
| Performance score < 60% for 2+ consecutive audits | "[Branch] caterer has failed hygiene audits 2 consecutive times. Review contract." | Amber |

---

## 3. Vendor Table

**Search:** Vendor name, FSSAI license number, branch. 300ms debounce.

**Filters:** Branch · Contract Status (Active/Expired/Pending/Terminated) · FSSAI Valid · Expiring in 30 days.

**Columns:**
| Column | Sortable |
|---|---|
| Vendor Name | ✅ |
| Branch | ✅ |
| Contract Start | ✅ |
| Contract End | ✅ (amber if ≤ 30d, red if expired) |
| FSSAI License # | ✅ |
| FSSAI Valid Until | ✅ (red if expired) |
| Avg Hygiene Score | ✅ |
| Monthly Rate (₹) | ✅ |
| Payment Status | ✅ |
| Status | ✅ |
| Actions | ❌ |

---

## 4. Drawers

### 4.1 Drawer: `vendor-create`
- **Trigger:** + New Vendor
- **Width:** 640px
- **Tabs:** Profile · Contract · Rate Card · Documents · Payment
- **Profile:** Vendor name, contact person, mobile, email, address, PAN, GST number
- **Contract:** Branch(es) covered, contract start/end dates, contract type (exclusive/shared), renewal clause
- **Rate Card:** Per-meal rates (breakfast/lunch/snacks/dinner) · Per-month lump sum option · Number of students covered
- **Documents:** FSSAI license (upload + expiry date) · Contract PDF · Pan copy · Bank details
- **Payment:** Payment frequency · Bank details · Payment terms

### 4.2 Drawer: `vendor-detail`
- **Width:** 640px
- **Tabs:** Overview · Performance · Payment History · Documents · Contract History
- **Performance tab:** Last 12 audits with scores (bar chart) + average score + trend
- **Payment History:** Month-by-month payments made + pending

### 4.3 Modal: Terminate Contract
- **Type:** Centred modal (480px)
- **Fields:** Termination date · Reason (required) · Notice period compliance (checkbox) · Final payment amount

---

## 5. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Vendor added | "Vendor '[Name]' added for [Branch]." | Success | 4s |
| Contract renewed | "Contract for [Vendor] at [Branch] renewed until [date]." | Success | 4s |
| Contract terminated | "Contract terminated. [Vendor] removed from active list." | Warning | 5s |
| FSSAI updated | "FSSAI license for [Vendor] updated. Valid until [date]." | Success | 4s |

---

## 6. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/mess/vendors/` | JWT (G3+) | Vendor list |
| POST | `/api/v1/group/{group_id}/hostel/mess/vendors/` | JWT (G3+) | Create vendor |
| GET | `/api/v1/group/{group_id}/hostel/mess/vendors/{id}/` | JWT (G3+) | Vendor detail |
| PATCH | `/api/v1/group/{group_id}/hostel/mess/vendors/{id}/` | JWT (G3+) | Update vendor |
| POST | `/api/v1/group/{group_id}/hostel/mess/vendors/{id}/terminate/` | JWT (G3+) | Terminate contract |
| GET | `/api/v1/group/{group_id}/hostel/mess/vendors/{id}/performance/` | JWT (G3+) | Performance audit history |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
