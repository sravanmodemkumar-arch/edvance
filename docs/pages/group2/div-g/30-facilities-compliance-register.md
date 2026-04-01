# 30 — Facilities Compliance Register

> **URL:** `/group/ops/facilities/compliance/`
> **File:** `30-facilities-compliance-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full) · Operations Manager G3 (full) · Branch Coordinator G3 (own branches) · Zone Ops Mgr G3 (zone)

---

## 1. Purpose

Tracks all mandatory safety certificates, permits, and compliance documents for every
branch campus. Manages renewal timelines, alerts before expiry, and maintains an audit
trail of all compliance actions. A lapsed fire NOC is a legal and safety risk — this
page prevents that.

---

## 2. Certificate / Permit Types

| Code | Certificate | Authority | Validity | Critical? |
|---|---|---|---|---|
| FC-01 | Fire NOC | Fire Department | Annual | ✅ |
| FC-02 | Building Use Permission (BUP) | Municipal Corp | 3–5 years | ✅ |
| FC-03 | Electrical Safety Certificate | Electrical Inspector | Annual | ✅ |
| FC-04 | Lift Inspection Certificate | Boiler/Lift Inspector | Annual (if lift) | ✅ |
| FC-05 | Generator Consent | Pollution Control Board | Annual | ❌ |
| FC-06 | Water Tank Hygiene Certificate | Health Authority | Annual | ❌ |
| FC-07 | Environmental Clearance | State PCB | 5 years | ❌ |
| FC-08 | Occupancy Certificate | Local Authority | Permanent (new builds) | ✅ |
| FC-09 | Pest Control Certificate | Licensed exterminator | Quarterly | ❌ |
| FC-10 | Fire Extinguisher Service | Approved agency | Annual | ✅ |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Facilities  ›  Compliance Register
```

### 3.2 Summary Strip
| Card | Value |
|---|---|
| Total Certificates | Count (across all branches) |
| Valid | Count (green) |
| Expiring 30d | Count (yellow) |
| Expired | Count (red, pulsing if critical expired) |
| Critical Lapsed | Count (red badge) |

---

## 4. Search & Filters

**Search:** Branch name, certificate type. 300ms debounce.
**Filters:** Certificate Type · Branch · Zone · Status (Valid/Expiring/Expired) · Critical only.

---

## 5. Certificate Table

**Default sort:** Status (Expired first, then Expiring, then Valid), then Expiry Date.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | |
| Zone | ✅ | |
| Certificate Type | ✅ | Code + full name |
| Critical | ❌ | ⚠ badge if critical |
| Certificate Number | ✅ | |
| Issuing Authority | ✅ | |
| Issue Date | ✅ | |
| Expiry Date | ✅ | Red if expired · Yellow if <30d |
| Days to Expiry | ✅ | Negative = already expired |
| Status | ✅ | Valid · Expiring Soon · Expired |
| Document | ❌ | [View PDF] link |
| Actions | — | View · Renew · Upload · Raise Alert |

**Pagination:** 25/page.

---

## 6. Branch Compliance Summary View (toggle)

> One row per branch with count of valid/expiring/expired certs.

**Columns:** Branch · Valid Certs · Expiring · Expired · Compliance % · [View Details →]

---

## 7. Certificate Renewal Drawer

- **Width:** 520px
- **Trigger:** Certificate row → [Renew]
- **Fields:**
  - Certificate Type (pre-filled)
  - Branch (pre-filled)
  - New Certificate Number
  - New Issue Date
  - New Expiry Date
  - Issuing Authority
  - Upload Certificate PDF
  - Notes (optional)
- **On save:** Old certificate archived with end date · New certificate active

---

## 8. Expiry Alerting

| Days to Expiry | Alert |
|---|---|
| 60 days | Email to COO + Ops Manager |
| 30 days | EduForge notification + WhatsApp to COO |
| 7 days | Daily reminder to COO + pulsing badge on dashboard |
| 0 (expired) — Critical | Immediate P1 escalation to COO |
| 0 (expired) — Non-critical | P3 alert |

---

## 9. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Certificate renewed | "Certificate renewed — valid until [Date]" | Success · 4s |
| Alert raised | "Expiry alert escalated — COO notified" | Warning · 4s |
| Document uploaded | "Certificate document uploaded" | Success · 4s |
| Critical expired | "CRITICAL: Fire NOC expired at [Branch] — immediate action required" | Error · manual dismiss |

---

## 10. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No expired | "All certificates valid" | — |
| No expiring | "No certificates expiring in 30 days" | — |
| No certificates for branch | "No certificates registered" | [Upload Certificate] |

---

## 11. Loader States

Page load: Skeleton summary strip + table. Critical badge: always visible.

---

## 12. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Coordinator G3 | Zone Ops G3 |
|---|---|---|---|---|
| All branches | ✅ | ✅ | Own only | Zone only |
| [Renew] | ✅ | ✅ | ❌ | ✅ |
| [Upload Document] | ✅ | ✅ | ❌ | ✅ |
| [Raise Alert] | ✅ | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ | ❌ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/facilities/compliance/` | JWT (G3+) | Certificate list |
| GET | `/api/v1/group/{id}/facilities/compliance/summary/` | JWT (G3+) | Summary strip |
| GET | `/api/v1/group/{id}/facilities/compliance/branch-view/` | JWT (G3+) | Branch summary view |
| POST | `/api/v1/group/{id}/facilities/compliance/{cert_id}/renew/` | JWT (G3+) | Renew certificate |
| POST | `/api/v1/group/{id}/facilities/compliance/{cert_id}/document/` | JWT (G3+) | Upload doc |
| GET | `/api/v1/group/{id}/facilities/compliance/export/?format=pdf` | JWT (G3+) | Export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-get | hx-target | hx-swap |
|---|---|---|---|---|
| View toggle | `click` | `/api/.../compliance/branch-view/` | `#compliance-view` | `innerHTML` |
| Search | `input delay:300ms` | `/api/.../compliance/?q={}` | `#cert-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../compliance/?filters={}` | `#cert-table-section` | `innerHTML` |
| Critical badge poll | `every 60s` | `/api/.../facilities/compliance/summary/` | `#critical-cert-badge` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
