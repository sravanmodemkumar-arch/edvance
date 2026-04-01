# F-04 — Enrollment Form & Documents

> **URL:** `/coaching/admissions/enroll/`
> **File:** `f-04-enrollment-form.md`
> **Priority:** P1
> **Roles:** Admissions Counsellor (K3) · Branch Manager (K6)

---

## 1. Enrollment Form

```
ENROLLMENT FORM — Toppers Coaching Centre
Lead: LEAD-1842 (Suresh Babu) | Counsellor: Ms. Ananya Roy | 30 Mar 2026, 10:05 AM

  ── STEP 1 OF 4: PERSONAL DETAILS ──────────────────────────────────────────

    Full Name *:          [Suresh Babu Rao                     ]
    Date of Birth *:      [14 / 08 / 2001    ]   Age: 24
    Gender *:             (●) Male  ( ) Female  ( ) Other
    Father's Name *:      [Rao Krishnamurthy                   ]
    Mobile *:             [+91-98765-4231] ✅ Verified
    Alternate Mobile:     [+91-88765-4231]
    Email:                [suresh.rao@gmail.com                ]
    Address:              [Flat 12, Sai Nagar, Dilsukhnagar, Hyd-500060]
    Aadhaar No.:          [XXXX-XXXX-3412 ] (masked; entered & encrypted) ✅
    Category:             (●) General  ( ) OBC  ( ) SC  ( ) ST  ( ) EWS

  ── STEP 2 OF 4: ACADEMIC BACKGROUND ───────────────────────────────────────

    Highest Qualification: [B.Tech — Mechanical Engineering ▼]
    Institution:           [JNTUH College of Engineering, Hyd  ]
    Year of Passing:       [2024 ▼]    Percentage/CGPA: [68.2%  ]
    Previous coaching:     ( ) Yes — where: [           ]  (●) No
    SSC/Banking exams attempted: [SSC CGL 2024 — Tier I cleared, Tier II failed]

  ── STEP 3 OF 4: COURSE & BATCH ─────────────────────────────────────────────

    Course:           [SSC CGL 2026–27 (Full Batch) ▼]
    Duration:         10 months (May 2026 – Feb 2027)
    Batch:            [SSC CGL Morning — May 2026 ▼]
    Batch timing:     Mon–Sat, 06:00–09:00 AM, Hall A
    Mode:             (●) Offline (Main Branch)  ( ) Online  ( ) Hybrid

  ── STEP 4 OF 4: FEE & PAYMENT ──────────────────────────────────────────────
    (See F-05 — Fee Collection for payment details)
```

---

## 2. Document Checklist

```
DOCUMENT UPLOAD — LEAD-1842: Suresh Babu

  REQUIRED DOCUMENTS:                              STATUS
  ────────────────────────────────────────────────────────────────────────────
  ✅ Aadhaar Card (front + back)                  Uploaded: 30 Mar 10:08 AM
  ✅ Photo (passport size, recent)                Uploaded: 30 Mar 10:09 AM
  ✅ 10th Mark Sheet (SSC/Matriculation)          Uploaded: 30 Mar 10:11 AM
  ⬜ Graduation Certificate / Degree              Pending — student to bring
  ⬜ Previous exam scorecard (SSC CGL 2024)       Pending — optional but useful
  ────────────────────────────────────────────────────────────────────────────

  DOCUMENT STORAGE:
    All documents encrypted at rest (AES-256)
    Access: Counsellor (upload only) | Accounts (fee verification) | Manager (all)
    Student can view their own documents via Student Portal (O-01)

  BACKGROUND VERIFICATION:
    Identity (Aadhaar):  ✅ Auto-verified via DigiLocker API
    Qualification:       ⏳ Manual verification pending (HR uploads confirmation within 7 days)
    BGV Status:          Provisional enrollment — full BGV within 7 days

  NOTE: Student cannot be added to WhatsApp batch group until BGV is complete
  Graduation cert. to be submitted by Apr 5 or enrollment is provisional
```

---

## 3. Enrollment Confirmation

```
ENROLLMENT SUMMARY — LEAD-1842 converted to STUDENT: TCC-2026-2501

  Student ID:     TCC-2026-2501
  Name:           Suresh Babu Rao
  Course:         SSC CGL 2026–27 Full Batch
  Batch:          SSC CGL Morning (May 2026 start)
  Enrollment date: 30 March 2026
  Status:         PROVISIONAL (pending graduation cert.)

  FEE PAID:       ₹ 9,000 (first instalment — 50% of ₹18,000)
                  Receipt No: TCC-RCP-2026-0842
  Balance due:    ₹ 9,000 (due: 1 Aug 2026 — midpoint instalment)

  ACTIONS TRIGGERED:
    ✅ Welcome SMS sent to student (+91-98765-4231)
    ✅ WhatsApp message with batch start details sent
    ✅ Student account created on EduForge portal
    ✅ Batch coordinator (Ms. Priya Nair) notified
    ✅ GST invoice (₹10,620 incl. 18% GST) sent to student email
    ⏳ Add to batch WhatsApp group — pending BGV completion

  REFERRAL:  Source = Walk-in (no referral — no reward triggered)

  [Print Enrollment Card]   [View Student Profile →]   [Return to Pipeline]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/coaching/{id}/admissions/enroll/` | Create enrollment from lead |
| 2 | `PATCH` | `/api/v1/coaching/{id}/admissions/enroll/{eid}/` | Update enrollment details |
| 3 | `POST` | `/api/v1/coaching/{id}/admissions/enroll/{eid}/documents/` | Upload enrollment document |
| 4 | `GET` | `/api/v1/coaching/{id}/admissions/enroll/{eid}/documents/` | List documents and verification status |
| 5 | `GET` | `/api/v1/coaching/{id}/admissions/enroll/{eid}/summary/` | Enrollment summary and confirmation |
| 6 | `POST` | `/api/v1/coaching/{id}/admissions/enroll/{eid}/bgv-complete/` | Mark BGV as complete (HR role) |

---

## 5. Business Rules

- Aadhaar number is collected for identity verification via DigiLocker; it is stored encrypted and never displayed in full after submission; the last 4 digits are shown for reference ("XXXX-XXXX-3412"); Aadhaar data cannot be exported in bulk, shared with franchisees, or used for any purpose other than identity verification; TCC's data processing agreement (DPA) with EduForge specifies this restriction; violation is a DPDPA 2023 offence with penalties up to ₹250 crore for data processors
- Provisional enrollment allows a student to start classes and attend their batch before all documents are submitted; however, provisional status is limited to 14 days; if the missing document is not submitted within 14 days, the enrollment is flagged and the Branch Manager reviews whether to extend or cancel; provisional students are tracked in the batch roster with a "P" indicator; they have full access to classes but limited portal access (no test history, no rank data) until BGV is complete
- The GST invoice generated at enrollment uses TCC's registered GSTIN and SAC code 9992 (educational services — coaching); the invoice shows the full amount (₹18,000), the first instalment paid (₹9,000), and the GST on the instalment (18% = ₹1,620); a fresh invoice is generated for each subsequent instalment; TCC cannot aggregate all instalments into a single invoice without a clear instalment schedule — each payment is a separate taxable supply
- Student accounts on EduForge are created at enrollment with a temporary password sent via SMS; the student must change the password on first login; accounts created by the admissions team cannot have permanent passwords set by the counsellor (preventing counsellors from logging in as students later); the student's EduForge account is their portal for results, materials, attendance, and fee receipts — it is the primary post-enrollment touchpoint
- Enrollment reversal (cancellation within 7 days for any reason, full refund policy) is tracked by the Branch Manager; a counsellor who "over-promises" in the counselling session (e.g., promising a specific faculty, specific batch, or score guarantee) often creates enrollments that get reversed quickly; reversal data by counsellor is reviewed monthly; a high reversal rate (>10% of enrollments reversed within 7 days) triggers a review of the counsellor's pitch and promises

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division F*
