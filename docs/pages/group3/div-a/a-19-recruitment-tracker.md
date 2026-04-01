# A-19 — Recruitment & Vacancy Tracker

> **URL:** `/school/admin/staff/recruitment/`
> **File:** `a-19-recruitment-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** VP Admin (S5) — full · Principal (S6) — full · Promoter (S7) — view + final approval

---

## 1. Purpose

Tracks open vacancies and the recruitment pipeline for filling them. In Indian private schools, recruitment is largely informal (word of mouth, newspaper ads, teaching job portals like TeacherOn, Shine, Naukri Education), but the formal record-keeping for CBSE compliance requires the school to demonstrate that all teachers have prescribed qualifications and are paid at least minimum norms. This page manages the process from vacancy identification to offer letter.

---

## 2. Page Layout

### 2.1 Header
```
Recruitment & Vacancy Tracker               [+ New Vacancy]  [Export]
Open Vacancies: 6 · In Recruitment: 4 · Offers Pending: 2
```

---

## 3. Vacancies Table

| Designation | Subject(s) | Qualification Required | Open Since | Reason | Stage | Actions |
|---|---|---|---|---|---|---|
| PGT Chemistry | Chemistry XI–XII | M.Sc Chem + B.Ed | 15 Feb 2026 | Resignation | Shortlisting | [View Pipeline] |
| PRT English | English I–V | B.A Eng + B.Ed/D.El.Ed | 1 Mar 2026 | New section | Applications open | [View Pipeline] |
| Accountant | Finance | B.Com + Tally exp | 20 Mar 2026 | Retirement | Draft | [Open Vacancy] |
| PT Teacher | Sports | B.P.Ed | 1 Jan 2026 | Transfer | Interview Scheduled | [View Pipeline] |

---

## 4. Recruitment Pipeline (per vacancy)

Kanban stages:
1. **Draft** — vacancy created, JD not yet published
2. **Applications Open** — JD published; applications being collected
3. **Screening** — applications shortlisted by VP
4. **Demo Class Scheduled** — for teaching positions, demo lesson is standard practice
5. **Interview** — formal panel interview
6. **Reference Check** — previous employer verification
7. **Offer** — offer letter generated + sent
8. **Joined** — new staff joined; create EduForge account

---

## 5. Job Description Builder

**[+ New Vacancy] drawer (560px):**
- Designation, department, type (permanent/contract), salary range
- Required qualifications (mapped to CBSE norms for teaching positions)
- Subject(s) to teach + classes
- Publishing channels: School notice board · EduForge internal referral · External portal (Naukri/Shine)
- Application deadline
- [Publish JD] → makes vacancy visible on school website portal and internal referral link

---

## 6. Applicant List (per vacancy)

| Applicant | Qualification | Experience | Applied On | Source | Stage | Score | Action |
|---|---|---|---|---|---|---|---|
| Ms. Anitha Rao | M.Sc + B.Ed | 4 yrs | 18 Mar 2026 | Naukri | Demo Scheduled | — | [View] [Move] |
| Mr. Vikram | M.Sc | 1 yr | 20 Mar 2026 | Walk-in | Rejected (no B.Ed) | — | [View] |

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/recruitment/vacancies/` | Vacancy list |
| 2 | `POST` | `/api/v1/school/{id}/recruitment/vacancies/` | Create vacancy |
| 3 | `GET` | `/api/v1/school/{id}/recruitment/vacancies/{id}/applicants/` | Applicants for vacancy |
| 4 | `POST` | `/api/v1/school/{id}/recruitment/applicants/{id}/move-stage/` | Advance pipeline stage |
| 5 | `POST` | `/api/v1/school/{id}/recruitment/applicants/{id}/offer/` | Generate offer letter |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
