# J-02 — POCSO Register & Case Management

> **URL:** `/school/welfare/pocso/`
> **File:** `j-02-pocso-register.md`
> **Template:** `portal_base.html` (light theme — restricted access page, minimal chrome)
> **Priority:** P0
> **Roles:** POCSO Designated Officer/DO (S5 — Vice Principal or nominated senior teacher) — full access · Principal (S6) — full access · NO OTHER ROLE may access this register

---

## 1. Purpose

The POCSO register is the most legally sensitive record in the school system. It records all disclosures, complaints, and investigations related to the Protection of Children from Sexual Offences Act 2012. POCSO creates mandatory reporting obligations on schools:

- **Section 19:** Any person with knowledge of a POCSO offence MUST report to the Special Juvenile Police Unit (SJPU) or local police — failure to report is a criminal offence (Section 21: punishment up to 6 months imprisonment + fine)
- **Section 19A:** Principal is a "mandated reporter" for schools
- **Section 21:** Punishes both failure to report AND false complaints
- The school cannot investigate a POCSO case — it can only report to police/DCPU; investigation is the domain of law enforcement
- **DCPU (District Child Protection Unit):** Reports go here too; DCPU coordinates with CWC (Child Welfare Committee) for child protection measures

This register is COMPLETELY RESTRICTED — it is not visible to Transport In-Charge, Class Teachers, Counsellor, Administrative staff, or any other role. Only the Designated POCSO Officer (DO) and Principal.

---

## 2. Access Restriction Banner

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  RESTRICTED — POCSO REGISTER                                │
│                                                                 │
│  This register is accessible only to the POCSO Designated       │
│  Officer and the Principal.                                     │
│                                                                 │
│  All access to this page is logged with timestamp and user ID.  │
│  Unauthorised access is a violation of POCSO Act Section 23     │
│  (media/disclosure restrictions) and DPDPA 2023.               │
│                                                                 │
│  You are logged in as: [Designated Officer — Ms. Sunita Rao]   │
│  Access logged at: 27 March 2026, 10:14 AM                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Page Layout

### 3.1 Case Register

```
POCSO Case Register — GREENFIELDS SCHOOL                [+ New Entry]
Academic Year: [2026–27 ▼]

Case No.        Date Reported   Student (masked)   Source          Status         DCPU Filed
POCSO/2627/001  15 Sep 2025     Student A (IX-A)   Counsellor      ✅ Reported    ✅ Filed
POCSO/2627/002  3 Dec 2025      Student B (VIII-B) Teacher         ✅ Reported    ✅ Filed
POCSO/2627/003  12 Feb 2026     Student C (XI-A)   Self-disclosed  ⏳ Follow-up   ✅ Filed

Display note: Student names shown as "Student A/B/C" in the list view;
full name visible only in the individual case detail. This protects identity
even within the DO's own summary view.
```

---

## 4. New POCSO Entry

```
[+ New POCSO Entry]

Case No.: POCSO/2627/004 (auto-generated)
Date of disclosure/complaint: [27 March 2026]
Time: [11:45 AM]

Student (victim):
  Name: [Select from roll — encrypted display]
  Class: [___]  Age: [___]  Gender: [___]
  Student is a resident: ○ Day scholar  ○ Hostel resident
    If hostel: H-01 room allocation checked? [Yes/No]

Source of disclosure:
  ○ Student disclosed during counselling session (J-01)
  ○ Student reported directly to teacher/principal
  ● Student complained to another student (peer told class teacher)
  ○ Parent complaint
  ○ Hostel warden observation (H-08)
  ○ Anonymous complaint

Nature of complaint (select all applicable — do not use explicit terms in dropdown):
  ☑ Inappropriate physical contact by an adult
  ☐ Inappropriate digital/online contact
  ☐ Exposure to inappropriate material
  ☐ Other POCSO-defined offence

Alleged perpetrator:
  ● School staff  ○ Non-school adult (relative/outsider)  ○ Student (peer — different POCSO provision)
  If school staff: [Select from staff directory — name masked in system until police confirm identity]
  Relationship to student: [_________________]

Immediate actions already taken:
  ☑ Student removed from contact with alleged perpetrator — ✅ Done at 11:50 AM
  ☑ If school staff: suspended from duty — ✅ Done (verbal order; formal order by EOD)
  ☑ Principal informed: ✅ 11:46 AM
  ☐ Parent informed (in person/call by Principal — not WhatsApp): ← to be done today

Mandatory reporting deadline: 28 March 2026 (11:45 AM) — within 24 hours
  → Report to: SJPU (Special Juvenile Police Unit) or local police station
  → Report to: DCPU (District Child Protection Unit)

[Save Entry — Generate POCSO Section 19 Report]
```

---

## 5. POCSO Section 19 Mandatory Report

```
POCSO Section 19 Report — Auto-Generated

[For submission to SJPU/Police and DCPU]

To,
The Officer In-Charge,
Special Juvenile Police Unit / [Local Police Station],
[District], [State]

Subject: Mandatory Report under Section 19 of the POCSO Act 2012

Dear Sir/Madam,

I, [Principal Name], Principal of [School Name] (CBSE Affiliation No. XXXXXXX),
am filing this mandatory report in accordance with Section 19(1) of the Protection
of Children from Sexual Offences Act, 2012.

Details:

1. Date and time of disclosure/complaint: 27 March 2026, 11:45 AM
2. Student (victim): [Name withheld in this draft — full name to be disclosed to police only]
   Age: [__]  Class: [__]  Date of birth: [__]
3. Nature of complaint: Inappropriate physical contact by a school staff member
4. Identity of alleged perpetrator: [Name withheld pending police instruction on disclosure]
   Designation: [__]
5. Immediate actions taken by school:
   a. Student removed from contact with alleged perpetrator
   b. Alleged perpetrator suspended from duty
   c. Parent informed personally by Principal
6. This report is filed within 24 hours of the school receiving the complaint.
7. The school undertakes full cooperation with the investigation.

Please contact:
  Principal: [Name] — [Phone]
  POCSO Designated Officer: [Name] — [Phone]

Yours faithfully,
[Principal signature]
[School stamp]
Date: 27 March 2026

[Print Report]  [Download PDF]  [Log submission time]
```

---

## 6. Case Follow-Up

```
Case POCSO/2627/003 — Follow-Up Log

Student C (XI-A) — Case opened 12 February 2026

Timeline:
  12 Feb — Disclosure received from student (self-disclosed to counsellor)
  12 Feb 4:30 PM — Principal informed; perpetrator (non-school, family context) identified
  12 Feb 6:00 PM — Parents informed (Principal called personally)
  12 Feb 6:45 PM — SJPU report filed (FIR No. XXXX/2026 — withheld here)
  13 Feb — DCPU informed; DCPU officer visited school 14 Feb
  14 Feb — Student transferred to peer counselling support; class teacher given welfare flag
            (reason unknown to CT — only "welfare support" flag)
  25 Feb — Police investigation ongoing; school is cooperating
  10 Mar — DCPU follow-up visit; student confirmed safe and attending school
  27 Mar — ⏳ Investigation ongoing; FIR status: under investigation

School's role after reporting:
  ✅ Reported to police ✅
  ✅ Cooperated with DCPU ✅
  ✅ Provided safe environment for student ✅
  The school's obligation ends at reporting + cooperation — investigation is police domain

Confidentiality:
  This case is NOT in any school newsletter, notice, WhatsApp, or staff meeting
  POCSO Section 23: Media/public disclosure of victim identity is prohibited
  Only DO, Principal, and the directly engaged DCPU/police officer are aware

[Update follow-up log]  [Log DCPU communication]
```

---

## 7. Annual POCSO Compliance Activities

```
Annual POCSO Compliance Checklist — 2026–27

Mandatory at start of each year (POCSO + CBSE):
  ☑ Anti-sexual harassment policy displayed on school notice board ✅
  ☑ POCSO Designated Officer nominated and notified to staff: Ms. Sunita Rao (VP) ✅
  ☑ POCSO awareness training for all staff: 22 Jun 2026 (2 hrs) ✅
  ☑ Good touch/bad touch session for students (Class I–VIII): Jul 2026 ✅
  ☑ Age-appropriate POCSO awareness for Class IX–XII: Aug 2026 ✅
  ☑ Internal Complaints Committee (ICC) for staff: constituted ✅
  ☑ Parent awareness (PTM — F-05 agenda item): done Sep 2025 ✅
  ☑ Counsellor trained in trauma-informed counselling: ✅ Certificate on file
  ☑ Helpline numbers displayed: iCall, CHILDLINE (1098) — all floors ✅

CHILDLINE 1098: National child helpline — must be displayed in school premises;
  students should know they can call directly without going through school

POCSO Annual Report to DCPU: Due 30 April every year
  Cases this year: 3
  All reported within 24 hours: ✅
  Convictions/outcomes (where known): [DCPU provides update]

[Generate POCSO annual report]  [Submit to DCPU]
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/welfare/pocso/` | Case list (DO/Principal only — enforced at API layer) |
| 2 | `POST` | `/api/v1/school/{id}/welfare/pocso/` | Log new case |
| 3 | `GET` | `/api/v1/school/{id}/welfare/pocso/{case_id}/` | Case detail |
| 4 | `POST` | `/api/v1/school/{id}/welfare/pocso/{case_id}/followup/` | Add follow-up log entry |
| 5 | `GET` | `/api/v1/school/{id}/welfare/pocso/{case_id}/section19-report/` | Generate Section 19 report PDF |
| 6 | `GET` | `/api/v1/school/{id}/welfare/pocso/compliance-checklist/` | Annual compliance checklist |
| 7 | `GET` | `/api/v1/school/{id}/welfare/pocso/annual-report/` | Annual POCSO report for DCPU |

---

## 9. Business Rules

- Every API call to J-02 endpoints is logged with user ID, timestamp, and IP address — this audit log is immutable and is produced on demand for police/court
- The POCSO register is completely isolated from all other school data exports, analytics, and reports; it does not appear in any dashboard except the DO's and Principal's
- Student identity in this register uses a case pseudonym (Student A, B, C) in all list views; full identity is revealed only within the individual case detail (access-controlled)
- 24-hour mandatory reporting clock begins from the moment the school first receives the disclosure, not from when the DO reviews it — the DO must be contactable at all times; if the DO is unavailable, the Principal reports directly
- Once a case is opened, it cannot be deleted — only updated; closing a case requires a mandatory reason and the DO's digital signature
- If a teacher or staff member attempts to access the POCSO register without authorisation, the system denies access AND generates an automatic security alert to the Principal with the staff member's identity and timestamp
- POCSO cases are retained permanently (no deletion); they may be submitted to court as evidence years later
- EduForge does not transmit POCSO data to the EduForge SaaS platform operators (Anthropic infrastructure team) — the database rows for POCSO cases are encrypted with a key held by the school institution only; even EduForge engineers cannot read POCSO data

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division J*
