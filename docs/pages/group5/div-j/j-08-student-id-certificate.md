# J-08 — Student ID & Certificates

> **URL:** `/coaching/student-affairs/certificates/`
> **File:** `j-08-student-id-certificate.md`
> **Priority:** P3
> **Roles:** Student Counsellor (K3) · Branch Manager (K6) · Accounts (K5)

---

## 1. Student ID Card

```
STUDENT ID CARD — Toppers Coaching Centre

  ┌────────────────────────────────────────────────────┐
  │  [TCC LOGO]  TOPPERS COACHING CENTRE               │
  │              Hyderabad Main Branch                 │
  │  ─────────────────────────────────────────────     │
  │  [PHOTO]                                           │
  │  NAME:    AKHIL KUMAR                              │
  │  ROLL NO: TCC-2401                                 │
  │  BATCH:   SSC CGL Morning 2025–26                  │
  │  VALID:   Aug 2025 – Mar 2026                      │
  │  PHONE:   +91-98765-12345                          │
  │  ─────────────────────────────────────────────     │
  │  [QR CODE — links to student profile (portal)]     │
  │  If found, return to TCC: +91-40-XXXXXXXX          │
  └────────────────────────────────────────────────────┘

  ISSUE PROCESS:
    Issued at enrollment → physical card (printed in-house)
    Photo: Uploaded at enrollment or taken at reception desk
    QR code: Links to EduForge student profile (access requires login)
    Replacement (lost): ₹50 fee | processing: 24 hours

  DIGITAL ID (in-app):
    Available in student portal (O-01) — same details as physical card
    Digital ID accepted at libraries, railway concessions in some states
```

---

## 2. Certificate Types

```
CERTIFICATE TYPES — Issued by TCC

  Type                      │ Purpose                          │ Processing │ Fee
  ──────────────────────────┼──────────────────────────────────┼────────────┼────────
  Enrollment Certificate    │ Proof of enrollment (visa, bank) │ 1 day      │ Free
  Course Completion         │ After batch completion           │ 7 days     │ Free
  Merit Certificate         │ Top 10% rank holders             │ At result  │ Free
  Rank Certificate          │ Any rank (student request)       │ 2 days     │ ₹100
  Attendance Certificate    │ Minimum 75% attendance           │ 2 days     │ Free
  Character Certificate     │ Students in good standing        │ 3 days     │ Free
  No-Due Certificate        │ Fee fully paid, ready to exit    │ 1 day      │ Free
  ──────────────────────────┴──────────────────────────────────┴────────────┴────────
```

---

## 3. Certificate Request

```
CERTIFICATE REQUEST — TCC-2401: Akhil Kumar
Requested: 30 March 2026, 10:22 AM

  Certificate Type:    [Rank Certificate ▼]
  Purpose:             [Railway concession application ▼]
  Details:             Mock #25 Rank: 1/1,183 students (TCC SSC CGL batch)

  ELIGIBILITY CHECK:
    Fee fully paid: ✅ (no dues)
    BGV complete:   ✅
    Attendance:     95.4% ✅

  CERTIFICATE PREVIEW:
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │                      TOPPERS COACHING CENTRE                                │
  │                       Hyderabad Main Branch                                 │
  │                    Certificate of Merit & Rank                              │
  │                                                                             │
  │  This is to certify that AKHIL KUMAR (Roll No: TCC-2401), enrolled in the  │
  │  SSC CGL Morning Batch 2025–26 at Toppers Coaching Centre, achieved         │
  │  Rank 1 out of 1,183 students in the SSC CGL Full Mock Test #25             │
  │  conducted on 5th April 2026 with a score of 186/200.                      │
  │                                                                             │
  │  This certificate is issued for informational purposes. Actual government   │
  │  exam results are the sole authority for selection.                         │
  │                                                                             │
  │  Date: 30 March 2026          [Signature] Ms. Sunitha Verma, Branch Manager│
  │  [Branch Stamp]               [QR Code for verification]                   │
  └──────────────────────────────────────────────────────────────────────────────┘

  Fee: ₹100 → [Collected via UPI ✅ — Receipt TCC-RCP-2026-0901]

  [Generate & Download PDF]   [Send to Email]   [Print Certified Copy]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-affairs/certificates/types/` | Certificate types and fees |
| 2 | `POST` | `/api/v1/coaching/{id}/student-affairs/certificates/request/` | Request a certificate |
| 3 | `GET` | `/api/v1/coaching/{id}/student-affairs/certificates/{cid}/` | Certificate PDF download |
| 4 | `GET` | `/api/v1/coaching/{id}/student-affairs/certificates/verify/?qr={code}` | Verify certificate via QR |
| 5 | `GET` | `/api/v1/coaching/{id}/student-affairs/id-cards/student/{sid}/` | Student ID card (digital) |
| 6 | `POST` | `/api/v1/coaching/{id}/student-affairs/id-cards/reissue/` | Reissue lost ID card |

---

## 5. Business Rules

- Certificates issued by TCC are not government-recognised qualification certificates; they are internal institutional documents confirming enrollment, attendance, or rank within TCC's mock test series; TCC clearly states on every certificate: "This certificate is issued for informational purposes. Actual government exam results are the sole authority for selection"; this disclaimer protects TCC from students misrepresenting a TCC rank certificate as a government exam result; students who misuse a TCC certificate (e.g., claiming it as proof of exam clearance to an employer) are solely responsible for that misrepresentation
- The QR code on each certificate links to a verification page on TCC's website; scanning the QR confirms the certificate's authenticity (student name, roll number, certificate type, date of issue); third parties (banks, employers, embassies accepting enrollment certificates) can verify the certificate online; this reduces the burden on TCC's administrative staff for manual verification calls; the verification page shows a read-only view — it does not expose the student's full profile
- The No-Due Certificate is the most operationally important certificate; it confirms the student has no pending fee obligations; this is required before a student officially completes their course and is important for franchise branches (the franchise's own accounts team needs to confirm all dues are cleared before issuing completion records); the accounts team generates the No-Due Certificate after confirming zero balance; the certificate is auto-issued to the student's email on the date of final payment if the course is complete
- Character certificates are issued only to students who are in "good standing" — no outstanding disciplinary actions, no pending grievances against them, and fee fully paid; a student with 2 hostel rule violations (Mohammed R.) is not in good standing and would not receive a character certificate until the violations are resolved and 3 months have passed without further incidents; this policy is stated in the hostel rules agreement signed at admission
- Certificate printing and issuance is handled by the Branch Manager's office; the Branch Manager's signature and the branch stamp are required on physical copies; digital certificates use a digital signature; TCC maintains a register of all certificates issued with the student's ID, certificate type, date, purpose, and fee paid; this register is auditable; issuance of a backdated certificate ("make it say I enrolled in June, not August") is fraud and is not permissible regardless of any pressure applied

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division J*
