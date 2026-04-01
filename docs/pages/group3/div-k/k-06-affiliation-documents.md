# K-06 — Affiliation Document Repository

> **URL:** `/school/compliance/documents/`
> **File:** `k-06-affiliation-documents.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CBSE Affiliation Coordinator (S4) — manage · Administrative Officer (S3) — upload documents · Principal (S6) — view and approve critical documents

---

## 1. Purpose

Central repository for all documents required by CBSE, state education department, RTO, and other regulatory bodies. Schools need to produce these documents on demand — during inspections, for affiliation renewal, and for regulatory queries. A single lost certificate can delay a renewal by months.

This is not just storage — it tracks expiry dates and generates reminders so documents are renewed proactively, not scrambled for at inspection time.

---

## 2. Document Repository Dashboard

```
Affiliation Document Repository                      [+ Upload Document]  [Expiry Calendar]
27 March 2026

Document health:
  Total documents: 67
  Current (not expiring in 60 days): 54 ✅
  Expiring in < 60 days: 8 ⚠️
  Expired: 1 ⛔ (fire extinguisher FE-07 — already flagged in K-03)
  Never expires: 4 (land deed, building plan, affiliation letter, etc.)

Categories:
  Statutory/Regulatory: 22
  Infrastructure & Safety: 14
  Staff qualifications: 18
  Financial/Audit: 8
  Miscellaneous: 5
```

---

## 3. Document Categories and List

### 3.1 Statutory / Regulatory Documents

```
Category: Statutory / Regulatory

Document                          Issuing Authority     Expiry         Status
CBSE Affiliation Certificate      CBSE                  31 Mar 2029    ✅ Valid
State NOC (recognition)           State Edu. Dept       31 Mar 2027    ✅ Valid
Land/building ownership deed      Sub-Registrar Office  Never expires  ✅ Permanent
Society/Trust registration cert   Registrar of Societies Never expires ✅ Permanent
FCRA registration (if applicable) MHA                   N/A            N/A
Fire NOC                          Hyderabad Fire Stn    30 Apr 2026    ⚠️ 34 days
Building safety certificate        PWD Structural Eng.  30 Jun 2026    ✅ 95 days
Electrical safety certificate     State Elec. Inspector  1 Feb 2027    ✅ Valid
Water testing report (latest)     NABL Lab              31 May 2026    ✅ Valid
FSSAI licence (canteen)           FSSAI Hyderabad       14 Sep 2026    ✅ Valid
GST registration (school trust)   GST Dept              Never expires  ✅ Permanent
PAN card (trust)                  Income Tax Dept       Never expires  ✅ Permanent
12A/80G registration (if trust)   Income Tax Dept       5-year cycle   ✅ Valid to 2028
```

### 3.2 Infrastructure & Safety Documents

```
Category: Infrastructure & Safety

Document                          Last Updated          Status
Approved building plan            2015 (original)       ✅ Filed
Occupation/Completion certificate 2016                  ✅ Filed
CBSE land area certificate        2022                  ✅ Filed
Lab safety register               2026                  ✅ Current
Fire drill register               2026 (2 drills)       ✅ Current
Transport fleet register (I-01)   Live (EduForge)       ✅
GPS compliance certificate (AIS-140) 2025               ✅ Current
CCTV system maintenance           2026                  ✅ Current
```

### 3.3 Staff Qualification Documents

```
Category: Staff Qualifications

For each staff member (45 teaching + 22 non-teaching):
  ● Education certificates (originals verified; photocopy on file)
  ● B.Ed / D.El.Ed certificate
  ● CTET / STET-TS certificate (where applicable)
  ● Appointment letter (signed copy)
  ● Service book (government-style service record)
  ● BGV police verification certificate (K-05)
  ● POCSO training attendance certificate

Status:
  All teaching staff: 45/45 files complete ✅
  Non-teaching staff: 22/22 files complete ✅
  Pending: 4 new joiner BGV certificates (in process)
```

---

## 4. Document Upload

```
[+ Upload Document]

Document name: [Fire NOC 2026 Renewal]
Category: [Statutory / Regulatory ▼]
Issuing authority: [Hyderabad Fire Station — North Zone]
Document date: [18 April 2026]  (date on the document)
Expiry date: [30 April 2027]
Uploaded by: [Administrative Officer]
File: [Upload PDF — max 20MB]

Tags: [Fire NOC] [Mandatory] [CBSE Affiliation] [Annual renewal]
Notes: [Renewed after FE-07 extinguisher was replaced and emergency lighting fixed]

[Save Document]

Document will be visible to: Compliance Officer, Principal, Administrative Officer
Document retention: Permanent (regulatory documents are never deleted from repository)
```

---

## 5. Expiry Calendar

```
Document Expiry Calendar — Next 90 Days

Date           Document                              Category    Days Left   Action
30 Apr 2026    Fire NOC                              Statutory   34 days     [Renew — in process]
15 Apr 2026    Bus PUC — AP29AB1234                 Transport   19 days     [Schedule renewal]
10 Apr 2026    Bus PUC — AP29EF9012                 Transport   14 days     [Renew immediately]
30 Jun 2026    Building safety certificate           Infra       95 days     [Schedule engineer visit]
14 Sep 2026    FSSAI canteen licence                Statutory   171 days    [Upcoming — no action]

Expired (action required):
  ⛔ Fire extinguisher FE-07 — Ground floor W — Expired 28 Feb 2026
     [Replacement ordered — K-03 tracking]

Reminders schedule:
  90 days before expiry: Email/portal notification to Compliance Officer
  30 days before expiry: Reminder + Principal alert
  7 days before expiry: Urgent alert to Principal + WhatsApp to Admin Officer
  Day 0 (expiry): P0 alert — all admin staff notified
```

---

## 6. Document Audit Trail

```
Document Audit Log

Every document action is logged with user, timestamp, and action type:

Date         User                 Action                    Document
27 Mar 2026  Admin Officer        Uploaded new file         Water test report Mar 2026
15 Mar 2026  Admin Officer        Uploaded new file         Electrical safety cert 2026
12 Mar 2026  Compliance Officer   Expiry extended           Fire NOC — extended by 30 days
                                                            (renewal application submitted)
10 Mar 2026  Principal            Viewed document           CBSE Affiliation Certificate
...

Document retention policy:
  ● Never delete compliance documents
  ● If a renewed document replaces an old one, BOTH are retained
    (old document = historical record; may be needed for audit trail)
  ● Physical originals: In Principal's office fireproof cabinet
    Digital copies: Cloudflare R2 (EduForge storage — encrypted at rest)
  ● Disaster backup: Downloads available quarterly to local school drive
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/compliance/documents/` | Document list |
| 2 | `POST` | `/api/v1/school/{id}/compliance/documents/` | Upload document |
| 3 | `GET` | `/api/v1/school/{id}/compliance/documents/{doc_id}/` | Document detail + download |
| 4 | `GET` | `/api/v1/school/{id}/compliance/documents/expiry-calendar/?days={90}` | Upcoming expiries |
| 5 | `GET` | `/api/v1/school/{id}/compliance/documents/category/{cat}/` | Documents by category |
| 6 | `GET` | `/api/v1/school/{id}/compliance/documents/audit-log/` | Document access/change log |
| 7 | `PATCH` | `/api/v1/school/{id}/compliance/documents/{doc_id}/` | Update document metadata |

---

## 8. Business Rules

- Documents in this repository are never deleted; marking a document as "superseded" replaces it in the active view but retains it in the history — regulatory documents must be available for retrospective audits
- Document storage uses Cloudflare R2 with server-side encryption; document download links are short-lived (presigned URLs — 15-minute expiry) to prevent link-sharing of sensitive documents
- Expiry alert escalation: the system auto-escalates to the Principal when a mandatory document (Fire NOC, Building Safety, CBSE Affiliation Certificate) is within 30 days of expiry or has expired; these are not silent alerts
- Document access is role-restricted: staff qualification documents are accessible to the Principal and HR/Admin only; building/fire safety documents are accessible to all admin staff; POCSO register is accessible to the DO and Principal only (J-02 handles this separately)
- During CBSE inspection: all documents in this repository can be exported as a single ZIP for the inspection team review; the system generates a "document health report" showing all documents with their status, for the Compliance Officer to review before inspection day
- Physical-digital reconciliation: at the start of every academic year, the Compliance Officer reconciles the physical document cabinet against the digital repository; any document in one but not the other is flagged for action

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division K*
