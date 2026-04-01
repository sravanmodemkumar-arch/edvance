# C-08 — Faculty Profile & Settings

> **URL:** `/coaching/faculty/profile/`
> **File:** `c-08-faculty-profile.md`
> **Priority:** P3
> **Roles:** Faculty (K2) — self-view and edit; Academic Director (K5) — full view

---

## 1. Faculty Profile Overview

```
FACULTY PROFILE — Mr. Suresh Kumar
As of 30 March 2026

  ┌─────────────────────────────────────────────────────────────────────────────┐
  │  [Photo]  Suresh Kumar                                                     │
  │           Quantitative Aptitude Faculty                                    │
  │           Toppers Coaching Centre — Hyderabad Main Branch                  │
  │           Employee ID: TCC-FAC-042  |  Joined: 12 Aug 2021                │
  │           Contact: suresh.kumar@tcc.in  |  +91-98765-43210                 │
  │           Status: ✅ Active  |  Contract: Full-time Permanent               │
  └─────────────────────────────────────────────────────────────────────────────┘

  PERSONAL DETAILS:
    Full Name:       Suresh Kumar Reddy
    Date of Birth:   14 March 1988  (Age: 38)
    Gender:          Male
    PAN:             ABCDE1234F  (masked: XXXXX1234F)
    Aadhaar:         ████-████-3421  (masked)
    Address:         Flat 204, Srinivasa Apts, Dilsukhnagar, Hyd — 500060

  EDUCATIONAL QUALIFICATIONS:
    B.Sc. Mathematics    │ Osmania University, 2009           │ 72.4%
    M.Sc. Mathematics    │ University of Hyderabad, 2011      │ 78.8%
    NET (Maths)          │ UGC-NET — June 2012 (Qualified)    │ JRF eligible

  PROFESSIONAL CERTIFICATIONS:
    [✅] SSC CGL Cleared (2013, Rank 142)   — validates exam domain knowledge
    [✅] IBPS PO Cleared (2014, Rank 88)    — validates Banking exam knowledge
    [⬜] RRB NTPC — not attempted

  BANK ACCOUNT (for salary):
    Bank: State Bank of India  |  A/C: XXXXXX7890  |  IFSC: SBIN0020387
    Verified: ✅  |  Salary mode: Direct Transfer (1st of every month)
```

---

## 2. Professional Stats (Read-Only)

```
PROFESSIONAL PERFORMANCE — Suresh Kumar (TCC-FAC-042)
Academic Year 2025–26 (Apr 2025 – Mar 2026)

  TEACHING LOAD:
    Batches assigned:   4 (SSC CGL Morning, Evening; CHSL; Banking Quant)
    Weekly hours:       38 hrs/week (avg; TCC standard: 36)
    Classes delivered:  198 / 204 scheduled  (97.1% attendance rate — faculty)
    Classes cancelled:  6 (medical: 4, personal: 2)

  QUESTION BANK CONTRIBUTION:
    Questions submitted (YTD):    342
    Approved:                     318  (92.9% approval rate)
    Rejected:                      12  (3.5% — mostly difficulty mislabelling)
    Avg quality rating:           4.2 / 5.0

  DOUBT RESOLUTION:
    Total doubts answered:        386
    Avg response time:            14.2 hours
    Avg rating from students:     4.3 / 5.0
    Reopen rate:                   8.4%

  STUDENT PERFORMANCE (Quant, across all batches):
    SSC CGL Morning:  Avg 16.4/25 (↑ +2.2 pts over last 5 tests) ✅
    SSC CGL Evening:  Avg 15.8/25 (↑ +1.8 pts) ✅
    CHSL Batch:       Avg 18.2/30 (↑ +0.6 pts) ✅
    Banking Quant:    Avg 22.4/50 (↓ -1.1 pts) ⚠️ Declining — review flagged

  QUARTERLY REVIEW SCORE (Q3 2025–26):
    Academic Quality:   4.1 / 5.0  (student ratings, verified)
    Teaching Output:    4.4 / 5.0  (classes, question bank, doubt SLA)
    Student Improvement: 4.2 / 5.0 (score trend across batches)
    Overall:            4.2 / 5.0  ✅ Good Standing
    Next review:        Jun 2026
```

---

## 3. Notification & Schedule Preferences

```
PROFILE SETTINGS — Suresh Kumar

  NOTIFICATION PREFERENCES:
    New doubt submitted:           (●) Immediate  ( ) Hourly digest  ( ) Daily digest
    Doubt approaching SLA (24h):   (●) Push + SMS  ( ) Push only
    Test published/rejected:       (●) Immediate
    Attendance reminder (15 min):  (●) Push notification
    Salary slip available:         (●) Email
    Student below 60% in my subj:  (●) Weekly digest (Mondays)

  SCHEDULE PREFERENCES:
    Preferred class time:          Morning (before 10:00)
    Preferred off day:             Sunday ✅ (currently assigned off)
    Max hours/day:                 8 hours (system enforced: no batch > 8 hrs/day)
    Substitute preference:         Ms. Kavitha (Banking Quant) — available Mon/Wed

  DISPLAY PREFERENCES:
    Default view:                  My Dashboard (C-01)
    Date format:                   DD/MM/YYYY
    Score display:                 Fractions (22/25) not percentage
    Language:                      English

  [Save Preferences]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/faculty/{fid}/profile/` | Full faculty profile |
| 2 | `PATCH` | `/api/v1/coaching/{id}/faculty/{fid}/profile/` | Update editable profile fields |
| 3 | `GET` | `/api/v1/coaching/{id}/faculty/{fid}/stats/?year=2025-26` | Annual professional stats |
| 4 | `GET` | `/api/v1/coaching/{id}/faculty/{fid}/preferences/` | Notification and schedule preferences |
| 5 | `PATCH` | `/api/v1/coaching/{id}/faculty/{fid}/preferences/` | Update preferences |
| 6 | `GET` | `/api/v1/coaching/{id}/faculty/{fid}/salary-slips/` | Salary slip history |

---

## 5. Business Rules

- Faculty can edit their own contact information, bank account, and notification preferences; they cannot edit their employment type, joining date, salary, or performance scores; any change to bank account details triggers a re-verification workflow (finance team receives an alert and must re-confirm the new account via OTP to the registered mobile before the next salary cycle) to prevent fraud
- Professional qualifications (degrees, certifications, NET/GATE scores) are entered by faculty but must be verified by the HR team against original documents; unverified qualifications are shown with a ⚠️ "Pending verification" tag; a faculty who lists a qualification they do not have is subject to immediate termination; TCC's BGV process (A-04 staff directory) covers qualification verification during onboarding
- Personal identifiers (PAN, Aadhaar) are stored encrypted and displayed in masked form even to the faculty member; the full PAN is only visible to the Finance team for TDS processing; the full Aadhaar is only visible to HR for EPFO/ESIC registration; masking in the UI prevents shoulder-surfing in shared computer environments (many faculty use the admin PC in the faculty room)
- The "Cleared SSC/IBPS" certification field is not just a résumé item — it is a teaching credibility signal shown on TCC's marketing materials and batch introduction sessions; a faculty who has personally cleared the exam they are coaching has higher student confidence and retention; TCC's brand promise includes "Taught by exam qualifiers"; faculty who haven't cleared the relevant exam are not penalised but are encouraged to attempt it within 2 years
- Faculty profile data (contact, qualifications, performance stats) is accessible to the Academic Director (K5) in full, to the Branch Manager in summary, and to other faculty members only in name and subject — individual performance scores are never visible peer-to-peer; this prevents performance score comparisons and competition that damages team cohesion; the Academic Director uses the data in the quarterly review (B-07) privately with each faculty member

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division C*
