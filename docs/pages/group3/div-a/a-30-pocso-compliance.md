# A-30 — POCSO Compliance Centre

> **URL:** `/school/admin/compliance/pocso/`
> **File:** `a-30-pocso-compliance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full · ICC Chairperson (S4 Welfare, if designated) — full · Promoter (S7) — view summary only

---

## 1. Purpose

Manages the school's compliance with the Protection of Children from Sexual Offences (POCSO) Act 2012 — specifically the obligations of educational institutions. All private schools are required to:
1. Form an Internal Complaints Committee (ICC)
2. Display the ICC charter in prominent locations
3. Conduct POCSO awareness sessions for students and staff annually
4. Receive and investigate complaints within the mandated timelines
5. Maintain a register of all POCSO-related complaints and their outcomes
6. Report complaints to local police/Child Welfare Committee within 24 hours

**This page is access-restricted:** Only Principal and designated ICC Chairperson. No other staff. Promoter sees only aggregate summary (no case details). DPDPA compliance: case files contain sensitive personal data about minors.

---

## 2. Page Layout

### 2.1 Header
```
POCSO Compliance Centre                                  ⚠️ CONFIDENTIAL
Access restricted to: Principal · ICC Chairperson
ICC Members: [Principal], [Ms. R. Sharma (VP Academic)], [Mr. J. Kumar (External Member)]
```

---

## 3. Main Sections

### 3.1 Compliance Status Overview

| Requirement | Status | Last Updated | Action |
|---|---|---|---|
| ICC Constitution | ✅ 3 members (incl. 1 external) | 1 Aug 2024 | [View Charter] |
| ICC Charter Displayed | ✅ Main entrance + notice board | 1 Aug 2024 | [View Proof] |
| Student Awareness (current year) | ✅ Conducted 15 Jan 2026 | 15 Jan 2026 | [View Records] |
| Staff POCSO Training | ⚠️ 101/110 trained (92%) | 20 Jan 2026 | [View List] [Schedule Training] |
| Visitor Register maintained | ✅ Daily | Today | [View Register] |
| Open Cases | 0 | — | — |

---

### 3.2 ICC Members Register

| Role | Name | Designation | Contact | Term From | Term Until |
|---|---|---|---|---|---|
| Presiding Officer | [Principal Name] | Principal | [phone] | 1 Aug 2024 | 31 Jul 2026 |
| Member | Ms. R. Sharma | VP Academic | [phone] | 1 Aug 2024 | 31 Jul 2026 |
| External Member (mandatory) | Mr. J. Kumar | Social Worker / NGO | [phone] | 1 Aug 2024 | 31 Jul 2026 |

External member requirement: must be from an NGO or organization involved in child protection (POCSO Act mandate).

[Edit Members] — Principal only. Change requires fresh charter publication.

---

### 3.3 Complaint Register

| Case ID | Date Received | Type | Complainant (code) | Accused (code) | Status | Days Since Filing | Action |
|---|---|---|---|---|---|---|---|
| No active or recent cases | | | | | | | |

**Note:** Actual names are stored encrypted; the table shows only case codes. Only ICC members can view full names. All data access logged.

**Complaint Types (as defined by POCSO Act):**
- Penetrative Sexual Assault (Section 3/4)
- Aggravated Penetrative Sexual Assault (Section 5/6)
- Sexual Assault (Section 7/8)
- Aggravated Sexual Assault (Section 9/10)
- Sexual Harassment (Section 11/12)
- Use of Child for Pornographic Purposes (Section 13–16)

**[+ Register New Complaint]** — sensitive form; access logged; immediately alerts Principal and VP Academic.

---

### 3.4 POCSO Training Register

Table of all staff × training status:

| Staff | Dept | Training Date | Training Mode | Acknowledgement | Next Due |
|---|---|---|---|---|---|
| Ms. Sudha Rani | Science | 15 Jan 2026 | Workshop (in-school) | ✅ Signed | Jan 2027 |
| Mr. Rajan T | Maths | 15 Jan 2026 | Workshop | ✅ Signed | Jan 2027 |
| Mr. XYZ | PE | ❌ Not trained | — | — | Overdue |

[Export Training Report] — for CBSE / inspection submission.
[Schedule Training Session] — opens calendar + staff invitation form.

---

### 3.5 Student Awareness Programme Records

| Date | Programme Type | Classes Covered | Facilitator | Students Attended | Report |
|---|---|---|---|---|---|
| 15 Jan 2026 | Classroom session (age-appropriate) | IV–XII | School Counsellor + External NGO | 842 | [View Report] |
| 15 Jan 2025 | Prior year session | IV–XII | Counsellor | 788 | [View Report] |

---

### 3.6 Emergency Contacts & Protocols

- Local Police Station (registered): [Name] · [Number]
- Child Welfare Committee (CWC) contact: [Name] · [Number]
- CHILDLINE (1098): posted in school
- Mandatory reporting: within 24 hours of receiving complaint to police/CWC (POCSO Act Section 19)

[Report to Police] button — generates the mandatory written complaint in prescribed format (FIR-ready), with case details. Only active when a case is in OPEN state.

---

## 4. API Endpoints

| # | Method | Endpoint | Description | Access Log |
|---|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/pocso/status/` | Compliance overview | Logged |
| 2 | `GET` | `/api/v1/school/{id}/pocso/icc-members/` | ICC members list | Logged |
| 3 | `PATCH` | `/api/v1/school/{id}/pocso/icc-members/` | Update ICC members | Logged + Principal 2FA |
| 4 | `GET` | `/api/v1/school/{id}/pocso/complaints/` | Case register (codes only) | Logged + role-gated |
| 5 | `POST` | `/api/v1/school/{id}/pocso/complaints/` | Register new complaint | Logged + Principal 2FA + immediate alert |
| 6 | `GET` | `/api/v1/school/{id}/pocso/complaints/{case_id}/` | Case detail (full names) | Logged + ICC role only |
| 7 | `GET` | `/api/v1/school/{id}/pocso/training/` | Training register |Logged |
| 8 | `POST` | `/api/v1/school/{id}/pocso/complaints/{case_id}/report-to-police/` | Generate police report | Logged + Principal 2FA |

---

## 5. Security & Data Protection

- All access to this page is logged in `school_audit_log` (mandatory, non-deletable)
- Case data encrypted at rest (AES-256); encrypted keys in AWS KMS
- Case files accessible only to ICC members (Principal + designated ICC role)
- Student names in cases are pseudonymised in all exports except the formal police complaint
- Promoter Dashboard (A-01) and Principal Dashboard (A-02) show ONLY the count of open cases (0 or N) — never names, never details
- Page inaccessible in parent portal; inaccessible to all non-ICC staff
- DPDPA Article 7/8: processing of children's sensitive data requires explicit consent chain; all POCSO data handling logged with legal basis = "Public Interest / Legal Obligation"

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
