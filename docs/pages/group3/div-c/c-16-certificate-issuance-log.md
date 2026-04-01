# C-16 — Certificate Issuance Log

> **URL:** `/school/students/certificates/log/`
> **File:** `c-16-certificate-issuance-log.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Administrative Officer (S3) — full · Principal (S6) — full

---

## 1. Purpose

A single consolidated audit log of every certificate ever issued by the school — Transfer Certificates (C-13), Bonafide/Study Certificates (C-14), Character Certificates (C-14), and Student ID Cards (C-15). This page does not generate certificates — it is the register.

CBSE inspection specifically asks for a combined certificate register showing sequential numbering and accounting for all certificates. Schools caught with gaps in TC numbering or unlogged bonafides face de-affiliation proceedings. This register provides the audit trail.

---

## 2. Page Layout

### 2.1 Header
```
Certificate Issuance Log                      [Export Full Register]  [Export by Type]
Academic Year: 2026–27
Total Certificates: 184  ·  TC: 18  ·  Bonafide: 84  ·  Character: 4  ·  ID Cards: 78
```

### 2.2 Unified Register
| Cert No. | Type | Student | Class | Issued By | Issue Date | Collected | Status |
|---|---|---|---|---|---|---|---|
| TC/2026/018 | TC | Priya Das | VIII-A | Admin Meera | 22 Mar 2026 | ✅ 24 Mar | Collected |
| BON/2026/084 | Bonafide | Arjun Sharma | XI-A | Admin Meera | 24 Mar 2026 | ✅ 24 Mar | Collected |
| CHR/2026/004 | Character | Suresh K. | XII-A | Admin Meera | 20 Mar 2026 | ✅ 20 Mar | Collected |
| IDC/2026/380 | ID Card | Kavya P. | IX-B | Admin Meera | 6 Apr 2026 | ✅ 6 Apr | Distributed |

---

## 3. Filters

```
Type: [All ▼ / TC / Bonafide / Character / ID Card]
Class: [All ▼]
Date Range: [01 Apr 2025] to [31 Mar 2026]
Status: [All ▼ / Issued / Pending Collection / Duplicate]
Search: [Name / Cert No.]
```

---

## 4. Export

**CBSE Inspection Format — Combined Certificate Register:**
```
CERTIFICATE ISSUANCE REGISTER — 2025–26
[School Name] | Affiliation: AP2000123

S.No.  Cert No.       Type        Student Name    Class  Date Issued  Issued By      Status
001    TC/2026/001    TC          Arun Kumar      XI     05 Apr 2025  Admin Meera    Collected
...
018    TC/2026/018    TC          Priya Das       VIII   22 Mar 2026  Admin Meera    Collected
019    BON/2026/001   Bonafide    Anjali Das      XI     8 Apr 2025   Admin Meera    Collected
...
102    BON/2026/084   Bonafide    Arjun Sharma    XI     24 Mar 2026  Admin Meera    Collected
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/certificates/log/?year={year}&type={type}` | Certificate log (all types) |
| 2 | `GET` | `/api/v1/school/{id}/certificates/log/export/?year={year}` | Export full register PDF/Excel |

---

## 6. Business Rules

- This is a read-only log — records are created by C-13 (TC) and C-14 (Bonafide/Character) automatically; no manual entry
- Records cannot be deleted — CBSE requires permanent register; deletion attempts are blocked and logged as a security event
- Gaps in certificate numbering (e.g., TC/2026/008 is missing) are highlighted in red — the school must add an explanation note (void/cancelled/error) for each gap before CBSE inspection

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
