# C-02 — Application Form Manager

> **URL:** `/school/admissions/applications/`
> **File:** `c-02-application-form-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Admission Officer (S3) — full · Administrative Officer (S3) — full · Academic Coordinator (S4) — read · Principal (S6) — full

---

## 1. Purpose

Manages application forms issued to prospective students — the formal step between initial enquiry and the admission test/interview. An application form in Indian schools collects the complete student and family profile, previous academic record, document checklist, and any special declarations (disability, RTE category, sibling). When submitted, it becomes the school's primary record of a prospective student before they are enrolled. This page tracks every form issued, the associated documents received, and the processing status.

Schools charge a non-refundable application form fee (₹200–₹1,000 depending on school prestige and class). This fee collection is logged here (the actual financial transaction is in div-d). Forms are numbered sequentially (e.g., ADM/2026/0284) — the CBSE inspection checklist specifically asks whether form numbers are sequential and whether all issued forms have been accounted for.

---

## 2. Page Layout

### 2.1 Header
```
Application Forms — 2026–27                  [+ Issue New Form]  [Bulk Import]  [Export Register]
Forms Issued: 124  ·  Returned: 86  ·  Pending Return: 38  ·  Processing: 42  ·  Completed: 22
Application Fee Collected: ₹1,24,000  ·  Outstanding: ₹38,000
```

### 2.2 Filter Bar
```
Class: [All ▼]  Status: [All ▼]  Date: [Mar 2026 ▼]  Search: [Name / Form No. / Mobile]
```

### 2.3 Application List
| Form No. | Applicant | Class | Issued Date | Returned Date | Documents | Status | Action |
|---|---|---|---|---|---|---|---|
| ADM/2026/0124 | Arjun Sharma | Class I | 10 Mar | 15 Mar | 6/8 docs ⚠️ | Processing | [View] |
| ADM/2026/0123 | Priya Venkat | XI-Science | 10 Mar | 12 Mar | 8/8 ✅ | Interview Scheduled | [View] |
| ADM/2026/0122 | Rohit Kumar | Class V | 9 Mar | — | 0/7 | Pending Return | [Remind] |

---

## 3. Issue New Form

[+ Issue New Form] → links to C-01 lead or creates fresh:

| Field | Value |
|---|---|
| Form Number | ADM/2026/0125 (auto-generated sequential) |
| Linked Enquiry | Search from C-01 (auto-populates fields) OR new |
| Student Full Name | As per birth certificate |
| Date of Birth | |
| Class Applying For | |
| Parent Names | Father, Mother |
| Address | Current residential address |
| Mobile | |
| Application Form Fee | ₹500 (class-configured default) |
| Fee Paid | ✅ Cash · ✅ Online · ✅ Demand Draft |
| Fee Receipt No. | |
| Form Handed Over | Date + Admission Officer name |
| Return Deadline | (default: 10 days from issue) |

On save: form number assigned, stage in C-01 auto-updated to "Form Issued".

---

## 4. Application Form — Returned Form Entry

When the parent returns the completed form with documents:

### 4.1 Student Information Tab
```
Student Details (from filled form):
Full Name:        Arjun Sharma
DOB:              12 Apr 2019 (Class I — meets age criterion ✅)
Gender:           Male
Mother Tongue:    Telugu
Nationality:      Indian
Religion:         Hindu
Category:         OBC
Aadhaar No.:      XXXX XXXX 4521 (masked; full entered)
Blood Group:      B+
Special Needs:    None declared
```

### 4.2 Family Information Tab
```
Father:   Mr. Rajesh Sharma  |  Occupation: Software Engineer  |  Qualification: B.E.
Mother:   Mrs. Meena Sharma  |  Occupation: Teacher  |  Qualification: M.A.
Annual Income: ₹8,50,000
Address: 14, Gandhi Nagar, Hyderabad — 500032
```

### 4.3 Academic Background Tab
```
Previous School:     St. Mary's English Medium School, Hyderabad
Board:               CBSE
Last Class Attended: LKG
Academic Year:       2025–26
Result:              Pass
Reason for Change:   Proximity to new residence
TC Received:         ✅ (TC No.: SM/TC/2026/0089)
```

### 4.4 Document Checklist Tab

| Document | Required | Received | Verified | Notes |
|---|---|---|---|---|
| Birth Certificate | ✅ | ✅ | ✅ Verified | GHMC birth cert |
| Aadhaar Card (Student) | ✅ | ✅ | ✅ | |
| Aadhaar Card (Father) | ✅ | ✅ | ✅ | |
| Transfer Certificate | ✅ (Class II+) | ✅ | ⬜ Pending | Needs HOD countersign |
| Previous Year Report Card | ✅ | ✅ | ✅ | |
| Passport Photos (4) | ✅ | ✅ | ✅ | |
| Caste Certificate | If OBC/SC/ST | ✅ | ⬜ | Original to verify |
| Medical Fitness Certificate | P1 only | ⬜ | — | Reminder sent |

6/8 documents received. System shows warning icon in list view.

### 4.5 Declarations Tab
```
☑ Parent declares all information is correct
☑ Parent accepts school's code of conduct
☑ Parent accepts fee structure (2026–27)
☐ Sibling at school: [Link sibling]
```

---

## 5. Application Status Workflow

```
Form Issued → Form Returned → Documents Verified → Ready for Test/Interview
                                                           ↓
                                        (C-03 Admission Test & Interview)
```

| Status | Meaning |
|---|---|
| **Pending Return** | Form issued but not yet returned by parent |
| **Returned - Incomplete Docs** | Form returned; some documents missing |
| **Returned - Complete** | All required documents received and verified |
| **Processing** | Under review by Admission Officer |
| **Interview Scheduled** | Shortlisted; call letter issued |
| **Admitted** | Confirmed; fee paid |
| **Rejected** | Did not qualify |
| **Withdrawn** | Parent withdrew application |

---

## 6. Document Upload (Digital)

For each document in the checklist:
- [Upload] → stores in Cloudflare R2 at path `school/{id}/admissions/2026/{form_no}/{doc_type}.pdf`
- Max size: 2MB per document
- Formats accepted: PDF, JPG, PNG
- Physical original: checkmark "Original seen and verified by [Officer Name] on [Date]"

---

## 7. Reminders for Pending Returns

[Remind] button on any "Pending Return" row:
- Sends WhatsApp message: "Dear [Parent], Your application form ADM/2026/0122 for [Student Name] (Class [X]) is due for return by [Date]. Kindly submit at the school office before [Date] to avoid forfeiture of seat."
- Logged in enquiry follow-up history (C-01)

Auto-reminder sent 2 days before return deadline.

---

## 8. Age Eligibility Validation

CBSE/State board rules for class-wise age at admission:

| Class | Minimum Age (as of 31 Mar) | System Check |
|---|---|---|
| Nursery | 3 years | Auto-computed from DOB |
| LKG | 4 years | Auto-computed |
| UKG | 5 years | Auto-computed |
| Class I | 6 years | Auto-computed |
| Class XI | Min 15 years, Max 17 years | Auto-computed |

If DOB entered and class selected, the system immediately shows: ✅ Age eligible (7 years, 2 months) or ⚠️ Age ineligible — DOB: 12 Apr 2020, minimum age for Class I is 6 years (by 31 Mar 2026).

---

## 9. Export

[Export Register] → options:
- **Application Register PDF** — sequential list of all forms issued (CBSE inspection format)
- **Pending Documents Report** — students with incomplete document checklist
- **Application Fee Collection Summary** — total fees collected vs pending
- **Class-wise Application Status** — how many applications in each status per class

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/admissions/applications/?year={year}&status={status}` | Application list |
| 2 | `POST` | `/api/v1/school/{id}/admissions/applications/` | Issue new application form |
| 3 | `GET` | `/api/v1/school/{id}/admissions/applications/{form_id}/` | Application detail |
| 4 | `PATCH` | `/api/v1/school/{id}/admissions/applications/{form_id}/` | Update application (documents, status) |
| 5 | `POST` | `/api/v1/school/{id}/admissions/applications/{form_id}/documents/` | Upload document |
| 6 | `GET` | `/api/v1/school/{id}/admissions/applications/{form_id}/documents/{doc_id}/` | Get document (signed R2 URL) |
| 7 | `POST` | `/api/v1/school/{id}/admissions/applications/{form_id}/remind/` | Send WhatsApp reminder |
| 8 | `GET` | `/api/v1/school/{id}/admissions/applications/export/?year={year}` | Export application register |

---

## 11. Business Rules

- Application form numbers must be sequential within a year; gaps in sequence must be explained in the register (e.g., "Form 0045 voided — duplicate print")
- Application fee collected is non-refundable; if parent withdraws after admission, the application fee is not refunded (admission fee is a separate larger amount which may have partial refund policy)
- Incomplete documents: a student can be shortlisted for interview with "pending" documents, but cannot be formally enrolled in C-05 until all mandatory documents are verified
- Original Transfer Certificate (from previous school) must be physically collected and logged before enrollment in Classes II–XII; CBSE inspection specifically verifies TC register
- Age eligibility errors are hard blocks — the system will not allow form processing for age-ineligible applications without Principal override with explicit note

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
