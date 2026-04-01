# 69 — Student Academic Profile Viewer

> **URL:** `/group/acad/student-profile/`
> **File:** `69-student-academic-profile.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 · Academic Director G3 · Exam Controller G3 · Results Coordinator G3 · Stream Coordinators G3 (own stream) · MIS Officer G1 (anonymised)

---

## 1. Purpose

Group-level read-only viewer for any enrolled student's complete academic history. Allows academic leadership
to pull up a student record without logging into a specific branch portal.

Use cases:
- CAO reviewing a topper's progress before nominating for a scholarship
- Academic Director investigating a student flagged in the dropout monitor
- Exam Controller verifying a student's eligibility for a supplementary exam
- Stream Coordinator assessing a student's subject-specific performance pattern

**DPDP Compliance:** All IEP/special-needs flags are masked based on role. Student names are masked
to initials for MIS Officer G1 access. Every profile view is logged in an audit trail.

---

## 2. Role Access

| Role | Level | View Name | View Marks | View IEP Flag | View Attendance | Audit Logged |
|---|---|---|---|---|---|---|
| CAO | G4 | ✅ Full | ✅ Full | ✅ Visible | ✅ | ✅ |
| Academic Director | G3 | ✅ Full | ✅ Full | ✅ Visible | ✅ | ✅ |
| Exam Controller | G3 | ✅ Full | ✅ Full | ❌ Masked | ✅ | ✅ |
| Results Coordinator | G3 | ✅ Full | ✅ Full | ❌ Masked | ✅ | ✅ |
| Stream Coordinators | G3 | ✅ Full | ✅ Own stream only | ❌ Masked | ✅ | ✅ |
| MIS Officer | G1 | ❌ Initials only | ❌ Anonymised % | ❌ | ✅ Anon | ✅ |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Student Academic Profile
```

### 3.2 Page Header
```
Student Academic Profile Viewer
Search by name, roll number, or branch to view a student's academic record.
```

### 3.3 Search Panel
- **Search bar:** Full name, roll number, or branch
- **Filters:** Branch · Stream · Class · AY
- **300ms debounce** on input
- **Results list:** Student name (masked for G1) · Branch · Class · Stream · Roll No
- **Click result:** Opens full profile panel

---

## 4. Profile Panel

### 4.1 Profile Header

| Field | Display |
|---|---|
| Student Name | Full name (masked to initials for G1) |
| Photo | Branch portal avatar or placeholder |
| Branch | Branch name + code |
| Stream | MPC / BiPC / MEC / CEC / HEC / IIT Foundation |
| Class | Current class (e.g. Class 11) |
| Roll Number | Branch roll number |
| Admission No. | Group-level admission number |
| Academic Year | Active AY |
| IEP Flag | 🟡 "Special Needs" badge — visible to CAO/AcadDir only |

---

### 4.2 Tab: Overview

| Section | Content |
|---|---|
| **Enrolment Timeline** | Joined [Branch] on [Date] · Previous branch (if transferred) |
| **Attendance Summary** | This term: N% · Last term: N% · Trend: ↑↓ |
| **Rank** | Group rank: [N] / [Total] · Branch rank: [N] / [Branch total] |
| **Subject Scores** | Current term — bar chart: Subject → Score % |
| **Alerts** | Active dropout risk flags (linked from Page 56) · Remedial enrolled (linked from Page 72) |

---

### 4.3 Tab: Marks History

**Table — All exams taken:**

| Column | Type | Notes |
|---|---|---|
| Exam Name | Text | |
| Date | Date | |
| Type | Badge | Internal · Board · JEE Mock · Foundation · Supplementary |
| Subject | Text | |
| Max Marks | Number | |
| Scored | Number | |
| % | Number | |
| Grade | Badge | A1 / A2 / B1 / B2 / C / D / E / F |
| Branch Rank | Number | |
| Group Rank | Number | |

- **Filters:** Exam type · Subject · Term · AY
- **Sortable:** Date · % · Group Rank
- **Export:** PDF academic transcript (watermarked · one-time download · 48hr expiry link)

---

### 4.4 Tab: Attendance

| Column | Type |
|---|---|
| Month | Text |
| Working Days | Number |
| Days Present | Number |
| Attendance % | Progress bar |
| Leave Type | Text (Medical / Hostel Leave / Unexplained) |

- **Trend line:** Monthly attendance % over current AY
- **Alert threshold:** Red if < 75% in any month

---

### 4.5 Tab: Academic Events

| Column | Type |
|---|---|
| Event | Text |
| Type | Badge (Olympiad / Scholarship Exam / Inter-branch Event / Board Exam) |
| Date | Date |
| Result | Text |
| Certificate | Link (if issued) |

---

### 4.6 Tab: Flags & Notes

| Flag | Source | Visibility |
|---|---|---|
| Dropout Risk | Page 56 | CAO · AcadDir |
| Remedial Enrolled | Page 72 | CAO · AcadDir · Stream Coord |
| IEP Active | Page 47 | CAO · AcadDir only |
| Re-evaluation Pending | Page 71 | Exam Controller · Results Coord |
| Accommodation Approved | Page 48 | Exam Controller · CAO |

- **Notes field:** G3+ can add a private note on the student record (visible to G3+ roles, not branch staff)

---

## 5. Audit Log

Every profile view is recorded:

| Field | Value |
|---|---|
| Viewer | Role + username |
| View Date + Time | Timestamp |
| Student Viewed | Student ID (not name, for DPDP) |
| Data Sections Accessed | Overview / Marks / Attendance / Events / Flags |

- **Accessible by:** CAO · Data Protection Officer (Div-A roles)
- **Retention:** 2 years

---

## 6. Export

| Export Type | Format | Security |
|---|---|---|
| Academic Transcript | PDF | Watermarked with viewer's name + date · One-time download link · 48hr expiry |
| Marks Summary | CSV | Role-restricted — G3+ only |

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Profile loaded | "Showing profile for [Initials/Name]" | Info | 3s |
| Transcript exported | "Transcript link generated — expires in 48 hours." | Success | 5s |
| Note saved | "Note saved." | Success | 3s |
| IEP masked | "IEP details masked — contact Special Ed Coordinator for access." | Info | 5s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| No search entered | "Search for a Student" | "Enter name, roll number, or branch to begin." |
| No results found | "No students found" | "Try different search terms or check the branch." |
| No marks history | "No exam records found" | "This student has not appeared in any group-level exam." |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Search results | Inline skeleton list items |
| Profile panel open | Skeleton: header + 4 tab placeholders |
| Marks history tab | Skeleton table rows |
| Transcript export | Spinner on export button |

---

## 10. Role-Based UI Visibility

| Element | CAO/AcadDir G4/G3 | Exam/Results Coord G3 | Stream Coord G3 | MIS G1 |
|---|---|---|---|---|
| Full student name | ✅ | ✅ | ✅ | ❌ Initials |
| IEP Flag | ✅ | ❌ | ❌ | ❌ |
| All subjects marks | ✅ | ✅ | Own stream | ❌ Anon % |
| Flags & Notes tab | ✅ | ✅ (partial) | ✅ (partial) | ❌ |
| Add note | ✅ | ✅ | ✅ | ❌ |
| Export transcript | ✅ | ✅ | ✅ | ❌ |
| Audit log visible | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/student-profile/?q=` | JWT (G1+) | Search students |
| GET | `/api/v1/group/{id}/acad/student-profile/{sid}/` | JWT (G1+) | Full profile (role-filtered) |
| GET | `/api/v1/group/{id}/acad/student-profile/{sid}/marks/` | JWT (G3+) | Marks history |
| GET | `/api/v1/group/{id}/acad/student-profile/{sid}/attendance/` | JWT (G3+) | Attendance history |
| GET | `/api/v1/group/{id}/acad/student-profile/{sid}/events/` | JWT (G3+) | Academic events |
| GET | `/api/v1/group/{id}/acad/student-profile/{sid}/flags/` | JWT (G3+) | Active flags |
| POST | `/api/v1/group/{id}/acad/student-profile/{sid}/notes/` | JWT (G3+) | Add note |
| GET | `/api/v1/group/{id}/acad/student-profile/{sid}/transcript.pdf` | JWT (G3+) | One-time transcript link |
| GET | `/api/v1/group/{id}/acad/student-profile/audit-log/` | JWT (G4) | Audit log of all profile views |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Student search | `input delay:300ms` | GET `.../student-profile/?q=` | `#student-search-results` | `innerHTML` |
| Select student | `click` | GET `.../student-profile/{sid}/` | `#student-profile-panel` | `innerHTML` |
| Tab: Marks | `click` | GET `.../student-profile/{sid}/marks/` | `#profile-tab-body` | `innerHTML` |
| Tab: Attendance | `click` | GET `.../student-profile/{sid}/attendance/` | `#profile-tab-body` | `innerHTML` |
| Tab: Events | `click` | GET `.../student-profile/{sid}/events/` | `#profile-tab-body` | `innerHTML` |
| Tab: Flags | `click` | GET `.../student-profile/{sid}/flags/` | `#profile-tab-body` | `innerHTML` |
| Add note | `submit` | POST `.../notes/` | `#notes-section` | `innerHTML` |
| Export transcript | `click` | GET `.../transcript.pdf` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
