# E-12 — Attendance Certificate Generator

> **URL:** `/school/attendance/certificates/`
> **File:** `e-12-attendance-certificate.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Administrative Officer (S3) — full · Class Teacher (S3) — request for own class · Principal (S6) — sign

---

## 1. Purpose

Generates certified attendance certificates for students — needed for:
- **Government scholarship applications** (PM Yashasvi, NSP — require certified 75% attendance)
- **Sports nominations** (district/state sports authority requires 75% attendance certificate)
- **NDA / Sainik School applications** (require attendance certificate from Class X school)
- **Visa applications** (student visa requires attendance proof)
- **Employment / apprenticeship** (some ITI-linked programmes)
- **Court affidavits** (child welfare cases)

These are different from bonafide certificates (C-14) — bonafide says the student is enrolled; attendance certificate specifically certifies the attendance percentage.

---

## 2. Page Layout

### 2.1 Header
```
Attendance Certificate Register              [+ Issue Certificate]  [Export Register]
Issued This Year: 28
```

### 2.2 Certificate Register
| Cert No. | Student | Class | Period | % | Purpose | Issued Date | Status |
|---|---|---|---|---|---|---|---|
| ATC/2026/028 | Arjun Sharma | XI-A | Apr–Mar 2026 | 87.8% | NSP Scholarship | 26 Mar 2026 | Collected |
| ATC/2026/027 | Priya Venkat | XI-A | Apr–Mar 2026 | 91.4% | Sports nomination | 24 Mar 2026 | Collected |

---

## 3. Issue Certificate

[+ Issue Certificate] → drawer:

| Field | Value |
|---|---|
| Student | [Search] |
| Period | Full Academic Year / Term 1 / Term 2 / Custom date range |
| Custom From | (if custom) |
| Custom To | (if custom) |
| Purpose | NSP Scholarship · Sports · NDA · Visa · Apprenticeship · Court · Other |
| Minimum Attendance | Auto-checked: student's actual attendance for the period |

**Validation:**
- If purpose requires ≥ 75% and student's attendance < 75% → warning: "Student has [X%] attendance — certificate will state actual %; recipient organisation may reject"

---

## 4. Certificate Format

```
┌──────────────────────────────────────────────────────────────────────┐
│  [School Logo]        ATTENDANCE CERTIFICATE        [School Name]    │
│                       Affiliation No.: AP2000123                      │
│  Certificate No.: ATC/2026/028             Date: 26 March 2026       │
│                                                                        │
│  To Whomsoever It May Concern                                          │
│                                                                        │
│  This is to certify that ARJUN SHARMA, son of Mr. RAJESH SHARMA,     │
│  is a bonafide student of this institution studying in                 │
│  Class XI-A during the academic year 2026–27.                         │
│                                                                        │
│  His attendance details are as follows:                                │
│                                                                        │
│  Period:           1 April 2026 to 27 March 2026                      │
│  Total Working Days: 198                                               │
│  Days Present:       174 (including 2 On-duty days)                   │
│  Attendance %:       87.87%                                            │
│                                                                        │
│  This certificate is issued for the purpose of                         │
│  National Scholarship Portal (NSP) application.                        │
│                                                                        │
│  This certificate is valid for 3 months from date of issue.           │
│                                                                        │
│                                          ____________________________  │
│                                          Principal / Head of School    │
│                                          [School Seal]                 │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/certificates/?year={year}` | Certificate register |
| 2 | `POST` | `/api/v1/school/{id}/attendance/certificates/` | Issue certificate |
| 3 | `GET` | `/api/v1/school/{id}/attendance/certificates/{cert_id}/pdf/` | Certificate PDF |
| 4 | `PATCH` | `/api/v1/school/{id}/attendance/certificates/{cert_id}/collect/` | Mark collected |

---

## 6. Business Rules

- Certificate states actual attendance — the school must not issue a certificate claiming higher attendance than actual (misrepresentation for scholarship purposes is a criminal offence under IPC 420)
- Certificate numbers are sequential within the year; registered in the certificate issuance log (C-16)
- Only active students (C-05 Status = Active) can get attendance certificates; withdrawn students get their record via TC or separate request

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
