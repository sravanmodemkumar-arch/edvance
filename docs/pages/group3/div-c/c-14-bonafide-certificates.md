# C-14 — Bonafide & Study Certificate

> **URL:** `/school/students/certificates/bonafide/`
> **File:** `c-14-bonafide-certificates.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Class Teacher (S3) — own class (draft) · Administrative Officer (S3) — full (draft + issue) · Principal (S6) — sign

---

## 1. Purpose

Generates Bonafide Certificates (also called Study Certificates or Bona-fide Certificates) for currently enrolled students. Bonafide certificates are among the most frequently issued school documents — a large school issues 80–200 per year. Students need them for:

- **Bank accounts:** SBI, PNB and most nationalised banks require a bonafide for a minor's savings account (Kisan/Sukanya accounts)
- **Passport application:** Ministry of External Affairs accepts school bonafide as proof of study for minor applicants
- **Competitive exam applications:** JEE, NEET, NDA, Sainik School, NTSE, KVPY — application forms ask for school certificate
- **Railway concession pass:** Indian Railways concessional pass for students requires school bonafide
- **Scholarship applications:** Pre-Matric, Post-Matric, National Means-cum-Merit scholarships
- **Visa applications:** Student visa for study abroad
- **Court proceedings:** Guardianship cases, property matters involving minors
- **Sports events:** District/state level sports participation requires school bonafide

The certificate simply attests: "Student X is a bonafide student of Class Y, Academic Year Z." Unlike TC, bonafide does not end the student's enrollment. The student continues studying.

---

## 2. Page Layout

### 2.1 Header
```
Bonafide / Study Certificates                 [+ Issue Certificate]  [Export Register]
Issued This Year: 84  ·  Pending Collection: 8
```

### 2.2 Certificate Register
| Cert No. | Student | Class | Purpose | Issued Date | Collected | Status |
|---|---|---|---|---|---|---|
| BON/2026/084 | Arjun Sharma | XI-A | Passport application | 24 Mar 2026 | ✅ 24 Mar | Collected |
| BON/2026/083 | Priya Venkat | XI-A | Bank account (SBI) | 23 Mar 2026 | ✅ 23 Mar | Collected |
| BON/2026/082 | Rohit Kumar | IX-B | Railway concession | 22 Mar 2026 | ⬜ — | Pending collection |

---

## 3. Issue Certificate

[+ Issue Certificate] → form (420px drawer):

| Field | Value | Notes |
|---|---|---|
| Student | [Search — name/roll/ID] | |
| Class | XI-A (auto from profile) | |
| Academic Year | 2026–27 | |
| Purpose | [Select ▼] | Bank Account · Passport · Railway Pass · Scholarship · Competitive Exam · Visa · Sports · Other |
| If Other | Free text | |
| Medium | English / Hindi / Regional | |
| Addressed To | "To Whomsoever It May Concern" (default) / Custom: "The Manager, State Bank of India" |
| Date Required | Today (default) | |
| Urgency | Normal (1 day) / Urgent (same day) | |
| Remarks | Optional additional line in cert | |

[Generate Certificate] → PDF generated immediately.

---

## 4. Certificate Format

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                    [SCHOOL LOGO]                                                    │
│               [SCHOOL NAME] — [Affiliation No.]                                    │
│               [Address, City, PIN — Phone — Email]                                 │
│                                                                                     │
│                        BONAFIDE CERTIFICATE                                         │
│                                                                                     │
│  Certificate No.: BON/2026/084               Date: 24 March 2026                   │
│                                                                                     │
│  To Whomsoever It May Concern                                                       │
│                                                                                     │
│  This is to certify that ARJUN SHARMA, son/daughter of Mr. RAJESH SHARMA,          │
│  is a bonafide student of this institution and is studying in                       │
│  Class XI — Section A (Science Stream) during the academic year 2026–27.            │
│                                                                                     │
│  His/Her date of birth as per school records is 12 April 2008.                     │
│                                                                                     │
│  This certificate is issued for the purpose of passport application.                │
│                                                                                     │
│  This certificate is valid for 3 months from the date of issue.                    │
│                                                                                     │
│                                                     _____________________________   │
│                                                     Principal / Head of Institution │
│                                                     [School Seal]                   │
└────────────────────────────────────────────────────────────────────────────────────┘
```

**Variants generated based on purpose:**
- **Bank account:** Adds "Date of admission to this school: 05 Apr 2026"
- **Railway pass:** Adds "The student's home address is [address]" and "Distance from school: [X] km (if configured)"
- **Scholarship:** Adds "Annual family income as declared: ₹8,50,000 (from school records)"
- **Sports:** Adds "The student is enrolled as a regular student and has no academic proceedings pending"

---

## 5. Medium Options

| Medium | Description |
|---|---|
| English | Default for most purposes |
| Hindi | For government scholarship portals, some bank branches |
| Telugu / Marathi / other | If school's state language; needs template pre-configured by school admin |

---

## 6. Bulk Certificates (Class-wise)

For exam application seasons (JEE/NEET application — October–November), 20–30 students from Class XII may need bonafides simultaneously:

[Bulk Issue] → select class + purpose → generates one certificate per student:
```
Bulk Bonafide — Class XII (All students) — Purpose: JEE Main 2027 Application
Students: 34
[Generate 34 Certificates as ZIP]
```

Each certificate has unique serial number. All logged in the register.

---

## 7. Collection Tracking

After certificate is generated:
- Parent/student collects physically at office
- Admin Officer marks [Mark as Collected] → date + "Collected by" (student / father / mother / authorised person)

```
BON/2026/084 collected by: Student himself — Arjun Sharma — 24 Mar 2026
ID verified: ✅ School ID card shown
```

For urgent certificates (same-day), a WhatsApp is sent when ready: "Your bonafide certificate BON/2026/084 for Arjun Sharma is ready for collection at the school office."

---

## 8. Character Certificate

A variant of this page issues **Character Certificates** — attesting the student's conduct and character during their period of study. Needed for:
- Armed forces application (NDA, police recruitment)
- Some college applications
- Government job applications

Format is identical to bonafide, with the key paragraph changed to:
> "This is to certify that [Name] has been a student of this school from [admission date] to [date]. During this period, his/her character and conduct have been [Excellent / Good / Satisfactory]. He/She bears a good moral character."

Character certificate template is a secondary option under [+ Issue Certificate] → Certificate Type: [Bonafide ▼ / Character ▼].

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/certificates/bonafide/?year={year}` | Certificate register |
| 2 | `POST` | `/api/v1/school/{id}/students/certificates/bonafide/` | Issue certificate |
| 3 | `GET` | `/api/v1/school/{id}/students/certificates/bonafide/{cert_id}/pdf/` | Fetch certificate PDF |
| 4 | `PATCH` | `/api/v1/school/{id}/students/certificates/bonafide/{cert_id}/collect/` | Mark as collected |
| 5 | `POST` | `/api/v1/school/{id}/students/certificates/bonafide/bulk/` | Bulk issue for class |
| 6 | `GET` | `/api/v1/school/{id}/students/certificates/bonafide/export/?year={year}` | Export certificate register |

---

## 10. Business Rules

- Bonafide certificates can only be issued for currently active (enrolled) students — not withdrawn or graduated students (they get TC or pass certificate instead)
- Certificate numbering is sequential within the academic year and certificate type; Character certificates share the same sequence as bonafides for simplicity
- A student can receive multiple bonafides in the same year for different purposes — there is no limit
- The validity clause "valid for 3 months" is standard; some schools say 6 months — configurable in school settings
- Principal's physical or digital signature is required on every certificate; if Principal is on leave, the Vice-Principal (VP Admin) can sign with "I/C Principal" notation — this is configurable in A-35 User Role Management
- Bonafide certificates are stored as PDFs in R2 for 5 years for audit/reference purposes

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
