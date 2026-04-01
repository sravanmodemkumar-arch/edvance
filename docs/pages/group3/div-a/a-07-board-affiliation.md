# A-07 — Board Affiliation Manager

> **URL:** `/school/admin/affiliation/`
> **File:** `a-07-board-affiliation.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full · Promoter (S7) — approve renewal · VP Academic (S5) — view

---

## 1. Purpose

Manages the school's board affiliation lifecycle — from the initial CBSE/ICSE/state board affiliation documents through annual compliance checks to renewal. Board affiliation is the school's licence to operate and examine students. Lapse means students cannot appear for board exams. This page is the Principal's tool for staying ahead of deadlines and maintaining complete, current documentation.

**Indian regulatory context:**
- **CBSE:** Affiliation renewed every 1–5 years depending on affiliation type (Provisional: 1yr, Regular: 5yr). Requires online application through CBSE's Saras portal, infrastructure compliance certificate, staff qualification compliance, and CBSE inspection visit. Failure to renew → school delisted from CBSE portal → students' board exams affected.
- **ICSE (CISCE):** Similar renewal process through CISCE portal; inspection visits mandatory.
- **State Boards:** Each state has its own renewal process (BSEAP, MSBSHSE, WBBSE, etc.); some annual, some periodic. Many state boards require physical inspection.
- **NIOS:** For open schooling; separate affiliation process for distance education.

---

## 2. Page Layout

### 2.1 Tab Bar
```
[Active Affiliations] [Renewal Tracker] [Inspection History] [Document Vault] [Compliance Checklist]
```

---

## 3. Tab: Active Affiliations

One card per board affiliation.

### Affiliation Card Structure:
```
┌─────────────────────────────────────────────────────┐
│ CBSE Affiliation                              [Edit] │
│ Affiliation No: 1234567 · School No: 41234          │
│ Type: Senior Secondary (I–XII)                      │
│ Region: Hyderabad Region                            │
│ ─────────────────────────────────────────────────── │
│ Valid From: 1 Apr 2022                              │
│ Valid Until: 31 Mar 2027   [████████░░] 4yr 0mo left│
│ Status: ✅ ACTIVE                                    │
│ ─────────────────────────────────────────────────── │
│ Documents: 8/10 complete  [View Documents]          │
│ Compliance Score: 94%                               │
└─────────────────────────────────────────────────────┘
```

- Progress bar shows time elapsed since last renewal vs total validity period
- Status: ACTIVE · EXPIRING_SOON (< 6 months) · EXPIRED · RENEWAL_IN_PROCESS
- [+ Add New Affiliation] button (for adding secondary board)

---

## 4. Tab: Renewal Tracker

Step-by-step renewal workflow for any affiliation with expiry < 12 months.

**Stage pipeline:**
```
1. PRE-CHECK → 2. DOCUMENT PREPARATION → 3. ONLINE APPLICATION → 4. INSPECTION SCHEDULED → 5. INSPECTION DONE → 6. APPROVAL PENDING → 7. RENEWED ✅
```

**Per stage — what's shown:**
- Current stage badge
- Checklist for current stage items
- Responsible person (Principal / VP Admin / EduForge support)
- Deadline for current stage
- [Mark Stage Complete] button

**Document preparation checklist (CBSE example):**
- [ ] NOC from Society/Trust (fresh, < 3 months old)
- [ ] Fire NOC from Municipal Corporation (< 1 year old)
- [ ] Building Completion Certificate
- [ ] Affidavit (prescribed format)
- [ ] Teacher qualification list (all teachers — prescribed format)
- [ ] Staff salary slips (last 3 months — for salary compliance check)
- [ ] Student enrollment data in CBSE format
- [ ] Infrastructure compliance report (playground, classrooms, library, labs)
- [ ] CBSE Saras portal login credentials for online submission

**[Generate Document Bundle]:** Creates a ZIP file with all uploaded documents, formatted for submission.

---

## 5. Tab: Inspection History

Chronological list of all inspection visits:

| Date | Inspector Name | Board | Type | Outcome | Report |
|---|---|---|---|---|---|
| 14 Jan 2023 | Mr. A K Sharma | CBSE | Periodic Inspection | ✅ Compliant | [Download] |
| 22 Aug 2021 | Dr. S Reddy | CBSE | Renewal Inspection | ✅ Approved | [Download] |
| 5 Mar 2020 | State Board Team | TS State Board | Annual Visit | ⚠️ Minor observations | [Download] |

**[+ Log Inspection Visit]** → records details when an inspector visits; generates inspection receipt record.

**Observations & Corrective Actions:**
- If an inspection report has observations, they appear as open corrective actions
- Each action: observation text · deadline · responsible person · status · evidence upload

---

## 6. Tab: Document Vault

All affiliation-related documents organized by category:

| Category | Documents | Last Updated |
|---|---|---|
| Society/Trust Documents | Registration cert, PAN, Trust Deed | 2024-08-15 |
| Infrastructure | Building cert, fire NOC, layout plan | 2025-01-20 |
| Academic Staff | Qualification list, appointment letters | 2026-01-10 |
| Finance | Audited accounts (3 years), fee structure approval | 2025-11-30 |
| Compliance | POCSO ICC cert, RTE compliance report, CCTV cert | 2026-02-14 |
| Board Certificates | All affiliation certificates (scanned) | 2022-04-01 |

- [Upload] per category
- Expiry date field for time-bound documents (NOC, fire safety, etc.)
- Auto-alert when document expires within 60 days

---

## 7. Tab: Compliance Checklist

CBSE's annual compliance checklist (approximately 80 items) adapted for ongoing monitoring:

**Categories:**
1. Infrastructure (classrooms, labs, library, playground, toilets, drinking water)
2. Academic Staff Qualifications (per CBSE/state norms for each subject)
3. Student Welfare (counsellor, POCSO, school health)
4. Safety (fire safety, CCTV, first aid, emergency drill)
5. Financial Compliance (fee as per approved structure, salary timely paid)
6. Technology (computer lab, internet for students as per CBSE norms)
7. Inclusive Education (special educator, ramp access for differently abled)

Each item: ✅ Compliant · ⚠️ Partial · ❌ Non-Compliant · N/A
Evidence upload per item.
Overall compliance score shown as % (and on KPI strip in A-01/A-02).

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/affiliations/` | All affiliations list |
| 2 | `GET` | `/api/v1/school/{id}/affiliations/{aff_id}/` | Affiliation detail |
| 3 | `PATCH` | `/api/v1/school/{id}/affiliations/{aff_id}/` | Update affiliation data |
| 4 | `GET` | `/api/v1/school/{id}/affiliations/{aff_id}/renewal/` | Renewal tracker status |
| 5 | `POST` | `/api/v1/school/{id}/affiliations/{aff_id}/renewal/stage/` | Advance renewal stage |
| 6 | `POST` | `/api/v1/school/{id}/affiliations/{aff_id}/documents/` | Upload document |
| 7 | `GET` | `/api/v1/school/{id}/affiliations/{aff_id}/documents/bundle/` | Download document ZIP |
| 8 | `GET` | `/api/v1/school/{id}/affiliations/inspections/` | Inspection history |
| 9 | `POST` | `/api/v1/school/{id}/affiliations/inspections/` | Log inspection visit |
| 10 | `GET` | `/api/v1/school/{id}/affiliations/compliance-checklist/` | Compliance checklist items |
| 11 | `PATCH` | `/api/v1/school/{id}/affiliations/compliance-checklist/{item_id}/` | Update compliance item |

---

## 9. Business Rules

- Affiliation expiry < 6 months → amber alert on all leadership dashboards (A-01, A-02)
- Affiliation expired → red alert; Platform Admin notified; school flagged in EduForge system
- Document with expiry date in past → auto-flagged as non-compliant in checklist
- Renewal stage cannot be skipped backward (linear pipeline); only Principal can reset a stage
- UDISE+ code must be set in A-06 before affiliation data can be submitted from this page

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
