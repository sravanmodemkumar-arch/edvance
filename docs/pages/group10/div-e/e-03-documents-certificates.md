# E-03 — Documents & Certificates

> **URL:** `/student/documents`
> **File:** `e-03-documents-certificates.md`
> **Priority:** P2
> **Roles:** Student (S2–S6) · Institution (issues documents) · EduForge (issues platform certificates)

---

## Overview

Centralised document vault for all student documents — institution-issued (ID cards, bonafide certificates, hall tickets, mark sheets) and EduForge-issued (topper certificates, streak badges, course completion, rank cards). Documents are downloadable as PDFs, include verification QR codes, and are available from any device (no more losing physical copies). Institutions upload documents via their admin portal; EduForge auto-generates platform certificates based on achievement triggers.

---

## 1. Documents Dashboard

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MY DOCUMENTS                                    [Search...] [Request New]   │
│                                                                              │
│  [All ●] [Institution Docs] [Certificates] [ID Cards] [Fee Receipts]      │
│                                                                              │
│  ── INSTITUTION DOCUMENTS ───────────────────────────────────────────────   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  🏫 Sri Chaitanya Junior College                                      │  │
│  │                                                                       │  │
│  │  📄 Student ID Card (2025-26)              [Download ↓] [View →]     │  │
│  │  📄 Bonafide Certificate                    [Download ↓] [View →]     │  │
│  │  📄 Hall Ticket — SA-2 Exams (Feb 2026)    [Download ↓] [View →]     │  │
│  │  📄 SA-1 Mark Sheet (Oct 2025)             [Download ↓] [View →]     │  │
│  │  📄 Transfer Certificate                   Not issued yet             │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  🎓 TopRank JEE Academy                                               │  │
│  │                                                                       │  │
│  │  📄 Coaching ID Card (2025-26)             [Download ↓] [View →]     │  │
│  │  📄 Fee Receipt — Mar 2026                 [Download ↓]              │  │
│  │  📄 Attendance Certificate (Q1 2026)       [Download ↓] [View →]     │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ── EDUFORGE CERTIFICATES ───────────────────────────────────────────────   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  🏆 City Topper — JEE Mock #23 (Hyderabad)        [Download ↓]      │  │
│  │  📊 Consistent Performer — JEE Q1 2026             [Download ↓]      │  │
│  │  🔥 28-Day Study Streak — March 2026               [Download ↓]      │  │
│  │  📝 100 Mock Tests Completed                       [Download ↓]      │  │
│  │  ⭐ Premium Member Certificate                     [Download ↓]      │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ── ALL FEE RECEIPTS ────────────────────────────────────────────────────   │
│  [View payment history with downloadable receipts →]                        │
│                                                                              │
│  ── REQUEST A DOCUMENT ──────────────────────────────────────────────────   │
│  Need a document not listed? Request from your institution:                 │
│  Document type: [ Bonafide Certificate ▼ ]                                  │
│  Purpose: [ Exam application ▼ ]                                            │
│  [Submit Request →]  (institution admin will process within 3 business days)│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Document Viewer & Verification

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  DOCUMENT — Student ID Card 2025-26                                          │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │                                                                  │ │  │
│  │  │  SRI CHAITANYA JUNIOR COLLEGE, KUKATPALLY                       │ │  │
│  │  │  ─────────────────────────────────────────                      │ │  │
│  │  │                                                                  │ │  │
│  │  │  ┌──────┐  Name:     Ravi Kumar                                │ │  │
│  │  │  │      │  Class:    XII MPC — Section A                       │ │  │
│  │  │  │PHOTO │  Roll No:  42                                         │ │  │
│  │  │  │      │  Adm. No:  SC-KPY-2025-1042                         │ │  │
│  │  │  └──────┘  DOB:      15-Aug-2007                               │ │  │
│  │  │            Blood:    O+                                         │ │  │
│  │  │            Valid:    2025-26                                     │ │  │
│  │  │                                                                  │ │  │
│  │  │  ┌──────────┐                                                   │ │  │
│  │  │  │ QR CODE  │  Scan to verify: eduforge.in/verify/DOC-SC-1042  │ │  │
│  │  │  └──────────┘                                                   │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                        │  │
│  │  [Download PDF ↓]  [Print 🖨️]  [Share →]                             │  │
│  │  Issued: 15-Jun-2025 · Verified ✅ · Signed by: Principal, SCJC     │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/student/documents` | List all documents (institution + EduForge) |
| 2 | `GET` | `/api/v1/student/documents/{doc_id}` | Document metadata |
| 3 | `GET` | `/api/v1/student/documents/{doc_id}/pdf` | Download document PDF |
| 4 | `POST` | `/api/v1/student/documents/request` | Request a document from institution |
| 5 | `GET` | `/api/v1/student/certificates` | List EduForge achievement certificates |
| 6 | `GET` | `/api/v1/student/certificates/{cert_id}/pdf` | Download certificate PDF |
| 7 | `GET` | `/api/v1/verify/{verification_code}` | Public verification endpoint |

---

## 4. Business Rules

- All documents (institution-issued and EduForge-issued) include a verification QR code and URL — the verification endpoint is public (no login required) and shows: document type, student name, issuing institution, issue date, and validity status; this prevents document forgery — institutions can verify bonafide certificates, coaching centres can verify school ID cards, and employers can verify EduForge achievement certificates by simply scanning the QR code.

- Institution documents are uploaded by the institution admin via their portal (Group 2/3/4/5) and appear in the student's document vault within 5 minutes; the student cannot edit or delete institution-issued documents — they are read-only with "Issued by [Institution Name]" stamp; documents remain accessible even after the student leaves the institution (alumni access) unless the institution explicitly revokes them.

- EduForge certificates are auto-generated based on achievement triggers: (a) Topper — rank 1 in any scope for any test, (b) Consistent Performer — top 5% for 3+ consecutive months, (c) Study Streak — 30/60/90/365 consecutive days, (d) Milestone — 100/500/1000 mock tests completed, (e) Premium Member — annual membership active; certificates use a standard template with the student's name, achievement, date, and a unique verification code.

- Document request workflow: the student selects a document type (bonafide, character certificate, migration certificate, etc.) and purpose (exam application, job application, bank account opening), and the request is routed to the institution admin's queue; the institution has a 3-business-day SLA to process; upon issuance, the student receives a WhatsApp notification with a download link; this digitises what was traditionally a physical process requiring the student to visit the institution office.

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division E*
