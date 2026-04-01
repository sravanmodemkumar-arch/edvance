# P-02 — Exam Body Links & Resources

> **URL:** `/coaching/partners/exam-bodies/`
> **File:** `p-02-exam-body-links.md`
> **Priority:** P2
> **Roles:** Academic Director (K5) · Student Counsellor (K3) · Branch Manager (K6)

---

## 1. Exam Body Reference Hub

```
EXAM BODY REFERENCE HUB — Toppers Coaching Centre
Key Government Exam Authorities | Updated: 31 March 2026

  SSC (STAFF SELECTION COMMISSION):
    Website:          ssc.nic.in
    SSC CGL 2026:     Notification expected: April 2026
                      Tier-I: July–August 2026 (tentative)
                      Tier-II: November 2026 (tentative)
    TCC action:       Academic team monitoring SSC calendar weekly
    SSC Results:      SSC CGL 2024 Final: Feb 2026 — 28 TCC selections ✅

  IBPS (INSTITUTE OF BANKING PERSONNEL SELECTION):
    Website:          ibps.in
    IBPS PO 2026:     Notification: June 2026 (tentative)
                      Prelims: October 2026, Mains: November 2026
    IBPS Clerk 2026:  Notification: July 2026 (tentative)
    TCC action:       IBPS PO batch curriculum updated for 2026 pattern ✅

  RRB (RAILWAY RECRUITMENT BOARD):
    Website:          indianrailways.gov.in (each zone has own RRB)
    RRB PO 2026:      Notification: August 2026 (tentative, cycle)
    RRB NTPC:         Ongoing (CEN 05/2024 in progress)
    TCC action:       RRB PO batch aligned to CEN 05/2024 pattern

  TSPSC (TELANGANA STATE PSC):
    Website:          tspsc.gov.in
    Group 1 (2026):   Notification pending (delayed — student counsellor monitoring)
    Group 2:          Results expected Q2 2026
    TCC action:       State PSC batch students updated on delay via counsellor

  UPSC (planned — not current):
    Website:          upsc.gov.in
    CSE 2026:         Prelims: June 2026
    TCC status:       UPSC batch planned from Oct 2026 (L-07 initiative)
```

---

## 2. Exam Calendar

```
EXAM CALENDAR — TCC Relevant Exams (AY 2025–26 / 2026–27)

  UPCOMING EXAMS (Apr–Dec 2026):
    Date              │ Exam                  │ TCC Batch      │ Students  │ Action
    ──────────────────┼───────────────────────┼────────────────┼───────────┼──────────────
    Apr 2026          │ SSC CHSL Tier-I 2025  │ SSC CHSL Batch │   108     │ Revision mode
    Apr 5, 2026       │ TCC Mock #26 (internal)│ SSC CGL Morn  │   276     │ Scheduled ✅
    May 2026          │ IBPS RRB 2026 notif   │ RRB PO Batch  │    90     │ Monitor SSC site
    Jun 2026          │ UPSC CSE Prelims 2026 │ (Not current)  │   N/A     │ Future batch
    Jul–Aug 2026      │ SSC CGL 2026 Tier-I   │ SSC CGL batches│   274     │ Prep intensive
    Oct 2026          │ IBPS PO Prelims 2026  │ IBPS PO Batch  │   121     │ Batch continues
    Nov 2026          │ IBPS PO Mains         │ IBPS PO Batch  │    —      │ Post-prelims

  EXAM REGISTRATION REMINDERS (student portal notification):
    SSC CGL 2026:     Alert set — 15 days before notification expected (April)
    IBPS PO 2026:     Alert set — 15 days before notification (June)
    TSPSC Group 1:    Alert set — immediate on notification (monitoring)
```

---

## 3. Student Exam Registration Support

```
EXAM REGISTRATION SUPPORT — TCC Services

  SERVICES PROVIDED (at no extra charge):
    ✅ Notification alerts (WhatsApp + app) when exam notification published
    ✅ Eligibility check assistance (age, qualification, category criteria)
    ✅ Application fee payment guidance (online payment help at reception)
    ✅ Admit card download assistance (if student has trouble)
    ✅ Exam centre preference guidance (known TCC alumni suggestions)

  SERVICES NOT PROVIDED (TCC scope boundary):
    ❌ TCC does not fill the application on behalf of the student
    ❌ TCC does not handle documents for the student's government application
    ❌ TCC does not provide its computers for exam registration (security risk)
    ❌ TCC does not guarantee exam eligibility determination — student is responsible

  FORM-FILLING SUPPORT (counsellor session, optional):
    Counsellor schedules 30-min sessions during SSC notification period
    Assists students who are confused about: category selection, preference order,
    educational qualification entry, photograph/signature upload
    Individual guidance, not bulk form-filling — student must do it themselves

  EXAM TRACKER (for enrolled students):
    Students log their exam registration in the portal (self-declared)
    TCC uses this data to: track expected selection counts, plan post-exam support,
    identify students who haven't registered (counsellor follow-up)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/partners/exam-bodies/` | Exam body list and links |
| 2 | `GET` | `/api/v1/coaching/{id}/partners/exam-bodies/calendar/` | Upcoming exam calendar |
| 3 | `POST` | `/api/v1/coaching/{id}/partners/exam-bodies/student-registration/` | Student logs their exam registration |
| 4 | `GET` | `/api/v1/coaching/{id}/partners/exam-bodies/student-registrations/` | Registered students per exam |
| 5 | `POST` | `/api/v1/coaching/{id}/partners/exam-bodies/alerts/` | Set exam date alert |

---

## 5. Business Rules

- TCC's academic calendar is fundamentally dependent on government exam notification dates; SSC, IBPS, and RRB dates are published by the respective authorities without a fixed schedule and can be delayed by months; TCC's batch curriculum must be paced to peak 2 months before the expected exam date but must be flexible enough to extend if exams are delayed; a batch that completes its curriculum 6 months before the exam (because the exam was delayed) needs revision modules and additional mocks to keep students engaged and sharp; the Academic Director monitors exam calendars weekly and adjusts batch pacing accordingly
- TCC provides exam registration support as a value-added service, not a core obligation; the legal responsibility for accurate exam registration (correct personal details, correct category, correct qualification entry) rests entirely with the student; if a student provides wrong information in their application (e.g., claiming OBC when they are General, to get lower cutoff) and is rejected at the DV (Document Verification) stage, TCC has no liability; TCC's assistance is in guiding the process, not in guaranteeing outcomes; students must be clearly told (in writing, during orientation) that they are responsible for their own government applications
- Exam body websites (ssc.nic.in, ibps.in, tspsc.gov.in) are the only authoritative sources for exam dates, admit cards, results, and selection lists; unofficial sources (coaching centre YouTube channels, Telegram groups claiming "insider information") often publish incorrect or speculative dates; TCC's academic team relies on official government publications only; publishing speculative exam dates on TCC's portal or WhatsApp ("SSC CGL notification expected next week — unofficial") would spread misinformation and create false expectations; TCC's exam calendar is clearly labelled "tentative" where official notification has not been released
- Exam tracker data (students who have logged their exam registration) is used by TCC for planning purposes — the counsellor follows up with students who haven't registered for exams they are supposed to appear for ("Akhil hasn't registered for SSC CGL 2026 yet — his batch is SSC CGL"); this is a welfare intervention, not surveillance; a student who chooses not to appear for the exam (family emergency, personal decision) is not penalised; the counsellor's role is to ensure the student made an informed decision, not to compel exam registration
- UPSC CSE (Civil Services Exam) is a fundamentally different exam from SSC/banking; it requires a different pedagogy (essay writing, optional subject, interview preparation), a different type of faculty (often retired IAS/IPS officers or subject experts), and different study material; TCC's current faculty have deep SSC/banking expertise and are not equipped to teach UPSC without specific training or hiring; the planned UPSC batch (Oct 2026 — L-07) requires TCC to hire qualified UPSC faculty before the batch launch; borrowing SSC faculty to teach UPSC topics (because they are available) will produce poor academic outcomes and damage TCC's credibility in a new market segment

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division P*
