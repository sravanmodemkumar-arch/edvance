# J-10 — Student Achievements & Awards

> **URL:** `/school/welfare/achievements/`
> **File:** `j-10-student-achievements.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Class Teacher (S3) — log class achievements · Academic Coordinator (S4) — academic awards · Principal (S6) — approve major awards and publications · Administrative Officer (S3) — certificate generation

---

## 1. Purpose

Records student achievements across academic, sports, arts, and co-curricular domains. Uses:
- **Recognition:** Motivates students; builds school pride
- **TC/Transfer Certificate:** Achievements are part of the TC record (C-13)
- **Scholarship applications:** Achievement evidence for merit scholarships (J-09)
- **CBSE affiliation:** CBSE asks for details of student achievements in inspection
- **School publications:** Annual magazine, website, PTM showcases
- **Character certificate:** Achievements inform the principal's character certificate

---

## 2. Page Layout

### 2.1 Header

```
Student Achievements & Awards                        [+ Log Achievement]  [Awards Ceremony Prep]
Academic Year: [2026–27 ▼]

Total achievements logged: 247
  Academic (ranks, merit): 84
  Sports (district/state/national): 48
  Arts & Cultural: 62
  Co-curricular (debate, quiz, Olympiad): 53

School toppers (Class XII 2026): 3 students >95%
State-level achievement: 4 students
National-level achievement: 1 student
```

### 2.2 Achievement Log

```
Filter: Category [All ▼]  Class [All ▼]  Level [All ▼]

Achievement No.  Student          Class  Category      Achievement                Level     Date
ACH/2627/001     Sunita K.        XII-A  Academics     School topper (97.4%)      School    Mar 2026
ACH/2627/002     Kiran V.         XI-B   Sports        State Basketball — captain State     Feb 2026
ACH/2627/003     Priya L.         X-A    Arts          First prize — state dance  State     Jan 2026
ACH/2627/004     Arjun S.         XII-A  Academics     JEE Advanced rank 1,842    National  Jun 2026
ACH/2627/005     Rahul Group      IX-B   Co-curricular CBSE Science Exhibition    National  Nov 2025
...
```

---

## 3. Log Achievement

```
[+ Log Achievement]

Achievement No.: ACH/2627/248 (auto-generated)
Date of achievement: [22 March 2026]

Student: [Vikram G. — XI-B]
Achievement category:
  ○ Academic (marks, rank, Board result)
  ● Co-curricular (debate, quiz, Olympiad, science fair)
  ○ Sports (inter-school, district, state, national)
  ○ Arts & Culture (dance, music, drama, art)
  ○ Social/Community (NSS award, Scouts, volunteer)
  ○ External recognition (award by outside body)

Achievement details:
  Name: First Place — Regional Level Quiz Competition (Science & Technology)
  Organiser: CBSE Regional Office — Hyderabad
  Level: ● District  ○ State  ○ National  ○ International
  Position/Result: First Place
  Participated with: ● Solo  ○ Team — [Team members: Arjun S. (XI-A)] [+ Add]

Certificate/proof:
  [Upload certificate PDF]  ← Required for national/state level; optional for school level

Publish on school website: ● Yes  ○ No (parent preference)
Publish in school magazine: ● Yes  ○ No

[Save Achievement]
```

---

## 4. Annual Awards and Ranks

```
Annual Awards — 2025–26

Academic Awards:
  School Topper (Class XII): Sunita K. — 97.4%
  School Topper (Class X): Deepa R. — 94.8%
  Subject Excellence Awards (highest marks per subject, Class XII):
    English: Priya V. — 98/100
    Physics: Arjun S. — 96/100
    Mathematics: Kiran M. — 97/100
    Biology: Sunita K. — 95/100
    Chemistry: Rahul P. — 94/100

Sports Awards:
  Best Sportsperson: Kiran V. (state basketball captain)
  Best Sportsperson (Girls): Meena S. (national athletics — 400m)

Co-curricular Excellence:
  Best Debater: Vikram G. (XI-B)
  Best Science Student: Arjun S. + Rahul Group (CBSE Science Exhibition — national)

Principal's Special Award:
  Ananya R. (IX-A) — volunteer work at NGO for 200+ hours

[Generate awards list]  [Prepare awards ceremony programme]  [Print certificates]
```

---

## 5. Certificate Generation

```
Achievement Certificate — Vikram G.

Certificate type: Co-Curricular Achievement
Achievement: First Place — Regional Level Science & Technology Quiz
Organiser: CBSE Regional Office
Date: 22 March 2026

Certificate format:
  ┌──────────────────────────────────────────────────────┐
  │           GREENFIELDS SCHOOL                         │
  │        Certificate of Achievement                    │
  │                                                      │
  │  This is to certify that Vikram G.                   │
  │  of Class XI-B has secured                           │
  │  First Place                                         │
  │  in the Regional Level Quiz Competition              │
  │  (Science & Technology) organised by                 │
  │  CBSE Regional Office, Hyderabad                     │
  │  on 22 March 2026.                                   │
  │                                                      │
  │  We are proud of this achievement.                   │
  │                                                      │
  │  Principal: ____________    Date: __________         │
  └──────────────────────────────────────────────────────┘

[Print Certificate]  [Download PDF]  [Save to student record for TC]
```

---

## 6. TC Integration

```
Achievement Summary for TC (Transfer Certificate)

Student: Arjun S. (XI-A)
[This section populates the "Co-curricular Activities / Achievements" field in C-13 TC]

Achievements on record (2022–2026):
  2026: JEE Advanced Rank 1,842 (National)
  2026: CBSE Science Exhibition — National level — participant
  2025: District Quiz — First Place
  2024: School debate competition — second place
  Sports: Chess club president (2024–25)
  NSS: 80 hours logged (J-14 NSS tracker)

Note: Only achievements logged in this register with supporting documentation
  (for state/national) appear on the TC achievement field.
  Minor/informal achievements are excluded to maintain credibility.

[Generate TC achievement summary]
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/welfare/achievements/` | Achievement list |
| 2 | `POST` | `/api/v1/school/{id}/welfare/achievements/` | Log achievement |
| 3 | `GET` | `/api/v1/school/{id}/welfare/achievements/{ach_id}/` | Achievement detail |
| 4 | `GET` | `/api/v1/school/{id}/welfare/achievements/student/{student_id}/` | Student achievement history |
| 5 | `POST` | `/api/v1/school/{id}/welfare/achievements/{ach_id}/certificate/` | Generate certificate |
| 6 | `GET` | `/api/v1/school/{id}/welfare/achievements/annual-awards/` | Annual awards summary |
| 7 | `GET` | `/api/v1/school/{id}/welfare/achievements/tc-summary/{student_id}/` | TC-ready achievement summary |

---

## 8. Business Rules

- State and national level achievements must have documentary proof (certificate from the organiser) uploaded before being marked as verified; unverified achievements are shown as "pending verification" and do not appear on TC or publications
- Publication consent: before any achievement is published on the school website, annual magazine, or social media, explicit consent from the parent (for minor students) must be on file; by default, achievements are NOT published without consent
- Group achievements: all team members must be logged individually; the achievement appears in each team member's record
- Achievements are part of the TC (C-13) record; once a TC is issued, the achievement list is frozen; retrospective additions require TC amendment (Principal's order)
- DPDPA: student photographs used in achievement-related publications require separate photo consent; the achievement consent does not automatically cover photographs
- School awards ceremony: the EduForge system helps generate the awards programme but the actual ceremony management is outside the system scope; this module provides the data for programme generation

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division J*
