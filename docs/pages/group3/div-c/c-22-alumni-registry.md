# C-22 — Alumni Registry

> **URL:** `/school/alumni/`
> **File:** `c-22-alumni-registry.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Administrative Officer (S3) — full · Principal (S6) — full

---

## 1. Purpose

Maintains records of all students who have graduated or passed out from the school. The Alumni Registry serves:
- **School reputation:** "Our alumni include IIT toppers, civil servants, doctors" — schools prominently display their distinguished alumni
- **Student reference:** Future students (applying for college/jobs) may need the school to confirm their study period; the alumni record is the permanent reference
- **Reunion planning:** Schools conduct alumni meets; alumni database is essential
- **Placement tracking:** Particularly for Class XII boards — tracking how many students made it to IIT, AIIMS, NLU, etc.
- **Historical compliance:** CBSE inspection asks for records of passed-out batches; the alumni registry provides this

Class XII students who pass their boards are automatically moved here from the active student list (via C-10 Class Promotion Manager's graduation process).

---

## 2. Page Layout

### 2.1 Header
```
Alumni Registry                               [Search Alumni]  [Export Batch]  [Add Achievement]
Total Alumni: 1,842  (all years since school establishment)
Latest Batch: 2025–26 (34 students)
```

### 2.2 Batch Filter
```
Batch Year: [2025–26 ▼]  |  Stream: [All ▼]  |  Search: [Name / Admission No.]
```

### 2.3 Alumni List (Batch 2025–26)
| S.No. | Name | Stream | CBSE% | Current | Contact | Achievement |
|---|---|---|---|---|---|---|
| 1 | Priya Venkat | Science (PCB) | 94.8% | MBBS — AIIMS Delhi | ✅ Updated | ⭐ Distinguished |
| 2 | Arjun Sharma | Science (PCM) | 91.2% | B.Tech CSE — IIT Bombay | ✅ Updated | ⭐ Distinguished |
| 3 | Rohit Kumar | Commerce | 88.4% | B.Com — SRCC Delhi | ✅ Updated | — |
| 4 | Anjali Das | Arts | 82.1% | BA English — JNU | ✅ Updated | — |

---

## 3. Alumni Record

### 3.1 School History
```
Arjun Sharma — Alumni ID: ALM-2026-0012

Batch: 2025–26 | Admission: GVS/2015/0024 | Student ID: STU-0000024
Admitted: 5 Apr 2015 (Class VI)  ·  Graduated: 31 Mar 2026 (Class XII)
Years at School: 11 years
Stream: Science — PCM
CBSE Class XII: 91.2% (Mathematics: 98, Physics: 92, Chemistry: 88, English: 86, CS: 94)
```

### 3.2 Post-School (Updatable by Admin or Alumni themselves if portal is enabled)
```
College / University: IIT Bombay
Course: B.Tech — Computer Science Engineering
Year of Joining: 2026
Current Status: Student
City: Mumbai
Mobile: 9876543210 (can opt out of sharing)
Email: arjun@example.com

Career/Achievement Notes:
  JEE Advanced 2026: AIR 842
  ⭐ Distinguished Alumni (school criteria: JEE Top 1000 / NEET Top 1000 / UPSC selection)
```

### 3.3 Achievement Badges (for school website/display)
| Badge | Criteria | Awarded |
|---|---|---|
| ⭐ IIT Selection | JEE Advanced rank < 5000 | ✅ |
| ⭐ AIIMS Selection | NEET rank < 1000 | — |
| ⭐ NIT Selection | JEE rank < 50000 | — |
| ⭐ Civil Services | UPSC selected | — |
| 🏅 School Topper | Highest CBSE % in batch | — |
| 🏅 Sports | State/National level selection | — |

---

## 4. Batch Summary

```
Batch 2025–26 — Summary (34 students)

CBSE Class XII Results:
  Average: 84.2%  ·  Highest: 94.8%  ·  Pass Rate: 97% (33/34; 1 compartment)

Post-School Placement (tracked — 28/34 updated):
  IIT/NIT/IIIT:         4 students
  NEET MBBS:            3 students
  Other Engineering:   10 students
  Commerce (CA/BBA):    6 students
  Arts (BA/MA):         4 students
  Undecided/Gap Year:   1 student
```

---

## 5. Alumni Batch Export

[Export Batch] → for:
- **CBSE inspection:** List of Class XII pass-outs for the year with roll numbers and result
- **Alumni newsletter / reunion:** Names, contact, achievements
- **School brochure/website:** Distinguished alumni list

---

## 6. Distinguished Alumni Display

Principal can mark alumni as "Distinguished" for display on school website/notice board:

```
Distinguished Alumni of [School Name]

🎓 Priya Venkat (Batch 2026) — MBBS, AIIMS Delhi — NEET AIR 48
🎓 Arjun Sharma (Batch 2026) — B.Tech CSE, IIT Bombay — JEE Advanced AIR 842
🎓 Dr. Kavita Rao (Batch 2018) — IAS 2023 — UPSC AIR 14
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/alumni/?batch_year={year}` | Alumni list by batch |
| 2 | `GET` | `/api/v1/school/{id}/alumni/{alumni_id}/` | Alumni detail |
| 3 | `PATCH` | `/api/v1/school/{id}/alumni/{alumni_id}/` | Update post-school info / achievements |
| 4 | `GET` | `/api/v1/school/{id}/alumni/batch-summary/?batch_year={year}` | Batch summary stats |
| 5 | `GET` | `/api/v1/school/{id}/alumni/distinguished/` | Distinguished alumni list |
| 6 | `GET` | `/api/v1/school/{id}/alumni/export/?batch_year={year}` | Export batch data |

---

## 8. Business Rules

- Alumni records are permanent — they are never deleted; they may be anonymised after 20 years if no further activity (DPDPA long-retention clause)
- Class XII graduates are auto-moved here when graduation is confirmed in C-10; no manual action needed
- Alumni do not have login access to the school portal (per RBAC: alumni = record only); if the school enables an alumni portal add-on, that is a separate feature flag
- Contact information in alumni records is voluntary — alumni or their parents can request removal of contact details under DPDPA 2023 right-to-erasure; only the contact information is removed; the academic record (what class they studied, CBSE marks) is retained permanently as it is a public record

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
