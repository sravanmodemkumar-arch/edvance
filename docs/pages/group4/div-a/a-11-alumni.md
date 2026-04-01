# A-11 — Alumni Records

> **URL:** `/college/students/alumni/`
> **File:** `a-11-alumni.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Alumni Coordinator (S3) · Dean of Students (S5) · Alumni (S1-Alumni — self-update) · Principal/Director (S6) — view

---

## 1. Purpose

Alumni management is a NAAC criterion (criterion 5.2) and increasingly important for college reputation. Alumni networks bring:
- Placement support (alumni employers and referrals)
- Guest lectures and mentorship
- Endowments and CSR contributions
- Reputation and NIRF ranking (alumni outcome data)

---

## 2. Alumni Directory

```
ALUMNI DIRECTORY — GCEH CSE Batch 2022–26 (First batch)

Total alumni (all batches): 1,842
  Batch 2022–26 (CSE): 112 graduates  |  Employment: 87 known
  Batch 2021–25 (CSE + ECE): 245 graduates
  [Earlier batches...]

SAMPLE ENTRY:
  Name: Mr. Rohan S.  |  Batch: 2022–26  |  Programme: B.Tech CSE
  Current employer: TCS, Hyderabad (placed via campus)
  Designation: Software Engineer — Associate
  Email: rohan.s@alumni.gceh.ac.in (alumni email active for 3 years post-graduation)
  LinkedIn: linkedin.com/in/rohans-gceh [self-updated]

ALUMNI OUTCOMES (NAAC criterion 5.2 — used in rankings):
  Employed within 6 months: 84/112 (75%) ✅ (batch 2022–26 CSE)
  Pursuing higher education: 18/112 (16%)
  Entrepreneurship: 4/112 (4%)
  Unknown/not tracked: 6/112 (5%)

[Generate NAAC alumni outcome report]  [Export for NIRF submission]
```

---

## 3. Alumni Engagement

```
ALUMNI ENGAGEMENT ACTIVITIES:

Guest lectures by alumni (last year):
  12 guest lectures by alumni in core subjects ✅
  Average attendance: 78% ✅

Alumni mentorship programme:
  48 students mentored by alumni (1:1) ✅

Alumni contributions:
  Scholarship contribution (alumni endowment): ₹4,20,000 (2025–26) ✅
  Lab equipment donation: 2 servers (₹1,80,000 value) ✅

Alumni chapter:
  GCEH Alumni Association (registered) ✅
  Annual meet: October 2026 (planned)

[Invite alumni for guest lecture]  [Send alumni newsletter]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/alumni/` | Alumni directory |
| 2 | `PATCH` | `/api/v1/college/{id}/alumni/{alumni_id}/` | Update alumni profile (self or coordinator) |
| 3 | `GET` | `/api/v1/college/{id}/alumni/outcomes/` | Employment/higher education outcome summary |
| 4 | `GET` | `/api/v1/college/{id}/alumni/naac-report/` | NAAC criterion 5.2 data |

---

## 5. Business Rules

- Alumni contact information is DPDPA-protected; post-graduation, the individual becomes the data principal (no longer a minor under guardian); consent for continued contact must be renewed at graduation; alumni who opt out cannot be contacted for college promotions but may be contacted for official purposes (NAAC survey, verification requests)
- NAAC requires specific evidence of alumni engagement (not just a directory); documented guest lectures, mentorship programmes, and contribution data are what assessors verify; EduForge's engagement tracking directly feeds NAAC criterion reports
- Alumni outcome tracking must begin within 6 months of graduation; the college must make a reasonable effort to track every graduate's status (employed/higher studies/entrepreneur/unknown); NIRF ranking calculations include placement and higher education rates; poor tracking leads to lower NIRF scores even if actual outcomes are good

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division A*
