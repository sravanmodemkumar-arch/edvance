# I-07 — Student Clubs, Sports & NSS/NCC

> **URL:** `/college/welfare/activities/`
> **File:** `i-07-student-activities.md`
> **Priority:** P2
> **Roles:** Student Activities Coordinator (S4) · NSS Programme Officer (S3) · NCC Officer (S3) · Principal/Director (S6)

---

## 1. Student Clubs

```
STUDENT CLUBS — GCEH 2026–27

REGISTERED CLUBS: 12

Club                        | Advisor               | Members | Events this year
──────────────────────────────────────────────────────────────────────────────────────────
CodeCraft (Coding Club)     | Dr. Ramesh D. (CSE)   | 142     | 6 events (hackathon, CTF)
Innovation Hub              | Dr. Suresh K. (CSE)   | 40      | 3 events (patent workshop)
Robomania (Robotics)        | Mr. Arun M. (CSE)     | 68      | 4 events (inter-college)
Circuit Crew (ECE Club)     | Dr. Priya M. (ECE)    | 82      | 5 events
Voltex (EEE Club)           | Dr. Anand R. (EEE)    | 54      | 4 events
CAD Crafters (Mech Club)    | Dr. Vikram S. (Mech)  | 46      | 3 events
Debate & MUN Society        | Dr. Lakshmi N.        | 38      | 2 inter-college events
Culturals Committee         | Ms. Deepa R.          | 65      | Annual fest (Zenith 2027)
Photography Club            | Mr. Kiran T.          | 28      | College magazine
Sports Committee            | PE Teacher (TBD)      | 120     | Inter-dept tournaments
Women's Cell                | Ms. Kavitha P.        | 45      | IWD events, awareness
IEEE Student Chapter        | Dr. Priya M.          | 82      | IEEE xtreme, 4 workshops

ANNUAL CULTURAL FEST (Zenith 2027):
  Date: 14–16 March 2027
  Participation: GCEH students + invited from 8 colleges
  Events: Technical (paper presentation, coding), Cultural (music, dance, drama), Sports
  Budget: ₹4.2L (college + sponsor)
  Sponsorship: ₹1.8L (local companies — Cyient, TCS, others)
  NAAC evidence: Criterion 5.3 (student participation + leadership)
```

---

## 2. NSS (National Service Scheme)

```
NSS — GCEH UNITS

UNITS: 2 NSS units (each 100 volunteers = 200 total)
  Unit I: Programme Officer — Dr. Deepa R. (Faculty, ECE)
  Unit II: Programme Officer — Dr. Ramesh D. (Faculty, CSE)

ANNUAL ACTIVITY REQUIREMENT (NSS norms):
  Regular activities: 120 hours/year (bi-weekly programmes — weekends)
  Special camp: 7-day residential camp (100 hours credit)
  Total: 240 hours for NSS certificate (NAAC criterion 3.6.2)

ACTIVITIES 2026–27:
  Regular Activities:
    ✅ Blood donation camp (August 2026 — 92 units donated at Lions Club)
    ✅ Clean campus drive (monthly — 10 sessions)
    ✅ Digital literacy (village adoption: Cheguru village, Medchal)
    ✅ Tree plantation (150 saplings — van mahotsav July 2026)
    ✅ Health awareness (diabetes + hypertension — Cheguru village, October 2026)
    ✅ Voter awareness (SVEEP campaign — January 2027)
    ✅ Swachh Bharat: Weekly cleaning programme (public areas near campus)
    ✅ COVID awareness follow-up: Vaccination documentation in village (April 2026)

  Special Camp (December 2026 — 7 days):
    Location: Cheguru village (adopted village)
    Activities: Health camp, school painting, road repair assistance, cultural programme
    Volunteers: 180 (90% of enrolled NSS students)
    District NSS Officer: Participated + certified ✅

NSS CERTIFICATE:
  Students with 240 hours: 168 / 200 (84%)
  Certificates issued: ✅ (signed by Principal + Programme Officers)
  Value: Government job preference (Group C/D); some PSUs give weightage
  NAAC: NSS activities documented for Criterion 3.6 (Extension Activities)
```

---

## 3. NCC (National Cadet Corps)

```
NCC CONTINGENT — GCEH

UNIT: 1 NCC unit (Navy Wing — Telangana Naval unit)
  Cadets enrolled: 60 (mix of B.Tech students)
  Associate NCC Officer (ANO): Mr. Kiran S. (Physical Education, commissioned)
  Senior NCC Officer: Lt. Commander at GCEH (visits weekly for training)

TRAINING ACTIVITIES:
  Weekly parade (Sundays, 6–9 AM on campus ground)
  Annual Training Camp (ATC): 10 days (January 2027 — Camp Visakhapatnam)
    GCEH cadets participated: 28 ✅
    Certificates: 'B' and 'C' certificate cadets: 18 + 8 respectively

NCC VALUE TO STUDENTS:
  'C' certificate: 5 bonus marks in Group C civil services (UPSC preference)
  NCC Navy 'B' certificate: Shortlisting advantage for Indian Navy officer entry
  Character development: Leadership, discipline, team work
  NAAC: NCC participation documented under Criterion 5.3

NCC CHALLENGES:
  Sunday training: Some students miss due to placement drives (October–March)
  Solution: ANO provides alternate training dates for students with valid excuse
  Dropout: 8 students dropped in Year 1 (time commitment); 52 continuing
```

---

## 4. Sports

```
SPORTS — GCEH

SPORTS FACILITIES:
  Cricket ground: ✅ (half pitch — space constraint on 3-acre urban campus)
  Basketball court: ✅ (outdoor)
  Badminton court: ✅ (2 indoor courts — Sports Hall)
  Volleyball court: ✅ (outdoor)
  Table tennis: ✅ (2 tables — common room)
  Gym: ✅ (20 equipment — open 6 AM – 8 PM)
  Chess/carrom: ✅ (common room)

ANNUAL SPORTS DAY (February 2027):
  Inter-department tournaments: Cricket, Basketball, Volleyball, Badminton, Table Tennis
  Winners: CSE (overall trophy 2026–27)

INTER-COLLEGIATE SPORTS:
  GCEH team at JNTU Sports Meet (December 2026):
    Badminton (men): Quarter-finals (eliminated by NIT Warangal)
    Cricket: Knocked out Round 2
    Basketball (women): Runners-up ← best performance of GCEH sports history 🏆

SPORTS SCHOLARSHIP/INCENTIVE:
  Outstanding sports performance: ₹2,000 cash award (GCEH policy)
    Recipients (2026–27): Basketball women's team (4 players) = ₹8,000 total
  NAAC: Sports achievements documented in Criterion 5.3
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/welfare/clubs/` | All clubs with activities |
| 2 | `GET` | `/api/v1/college/{id}/welfare/nss/activities/` | NSS activity register |
| 3 | `GET` | `/api/v1/college/{id}/welfare/nss/certificates/` | NSS certificate status |
| 4 | `GET` | `/api/v1/college/{id}/welfare/ncc/register/` | NCC cadet register |
| 5 | `GET` | `/api/v1/college/{id}/welfare/sports/achievements/` | Sports achievements |

---

## 6. Business Rules

- NSS hours tracking is mandatory for certificate issuance; a student who claims 240 hours but has no activity log cannot receive the certificate; the Programme Officer must maintain attendance at every NSS activity; EduForge's NSS module tracks attendance per activity, cumulates hours, and flags students when they reach 240 hours for certificate generation
- Student clubs must have a faculty advisor (not just a student president); NAAC peer teams ask who supervises student clubs; an unsupervised club can make commitments (financial, external) without institutional oversight; the faculty advisor is the institution's interface for club activities — approving events, monitoring budget (if any), and ensuring club activities are aligned with college values
- Inter-collegiate participation data (sports, technical events, MUN) is valuable NAAC evidence for Criterion 5.3 (Student Participation and Leadership); achievements should be documented with photos, certificates, and news articles; many colleges overlook this relatively easy area of NAAC improvement because they don't maintain records systematically; EduForge's activities module requires achievement uploads immediately after events
- The NCC and NSS certificates have real-world value for students pursuing government jobs; the college should communicate this clearly to students during orientation to increase enrolment; students who don't join NCC/NSS often regret it at the job-application stage; early visibility of the value increases participation rates
- Sports facilities must be accessible to all students — not monopolised by the sports teams; a college where the cricket ground is reserved for the college team and unavailable to regular students creates resentment and reduces overall student wellness; open facilities hours (6 AM – 8 AM, 5 PM – 7 PM for general students) alongside team practice slots is the correct balance

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division I*
