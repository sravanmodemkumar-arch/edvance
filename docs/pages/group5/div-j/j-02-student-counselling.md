# J-02 — Student Counselling Sessions

> **URL:** `/coaching/student-affairs/sessions/`
> **File:** `j-02-student-counselling.md`
> **Priority:** P1
> **Roles:** Student Counsellor (K3) · Branch Manager (K6 — escalation only)

---

## 1. Counselling Session Record

```
SESSION RECORD — Pavan Reddy (TCC-2428)
Session #6 | Date: 30 March 2026, 2:00 PM | Counsellor: Ms. Ananya Roy

  STUDENT BACKGROUND:
    Batch:          SSC CGL Morning (May 2025 start)
    Attendance:     58.3% (below 60% cutoff)
    Avg Test Score: 38.2/100 (declining — was 52 in Dec 2025)
    Fee Status:     ₹9,000 overdue (60+ days)
    Hostel:         Block A, Room A-04
    First session:  18 Jan 2026

  SESSION NOTES:
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │ Pavan came on time. Seemed more relaxed than last session.                  │
  │                                                                               │
  │ He shared that his father's illness (mentioned in Session 4) has improved.  │
  │ He's been able to focus more this week — attended 4 of 5 classes (vs 2/5   │
  │ in the previous week). Expressed guilt about fee — says the money was used  │
  │ for father's treatment. Understands the situation and wants to pay.         │
  │                                                                               │
  │ Academic discussion: Identified that Caselet DI (which is his weakest area) │
  │ is causing him to feel overwhelmed. Agreed to focus on one topic at a time  │
  │ rather than trying to cover everything.                                       │
  │                                                                               │
  │ Action plan agreed:                                                           │
  │   1. Attend all classes this week (target: 5/5)                             │
  │   2. Complete Caselet DI recording (Mar 26) before next session             │
  │   3. Speak to Accounts team about ₹9,000 — ask for 2-week extension         │
  │                                                                               │
  │ Mood at session end: Cautiously optimistic. Not in crisis.                  │
  └──────────────────────────────────────────────────────────────────────────────┘

  SESSION OUTCOME:  ✅ Productive
  RISK LEVEL:       🟡 Medium (improving — was High in Jan)
  NEXT SESSION:     Apr 7, 2:00 PM
  LIAISON NEEDED:   Accounts team — fee extension request (counsellor to brief BM)
```

---

## 2. Session Log (History)

```
SESSION HISTORY — Pavan Reddy (TCC-2428)

  #  │ Date      │ Duration │ Topics                          │ Risk Level │ Outcome
  ───┼───────────┼──────────┼─────────────────────────────────┼────────────┼──────────────
  1  │ 18 Jan 26 │ 45 min   │ Referral, initial assessment    │ 🔴 High    │ Baseline set
  2  │ 28 Jan 26 │ 40 min   │ Father's illness disclosed      │ 🔴 High    │ Support plan
  3  │ 10 Feb 26 │ 50 min   │ Attendance plan, fee stress     │ 🔴 High    │ Partial progress
  4  │ 25 Feb 26 │ 45 min   │ Father hospitalised — crisis pt │ 🔴 High    │ Referred to BM
  5  │ 12 Mar 26 │ 40 min   │ Post-crisis stabilisation       │ 🟡 Medium  │ Improving
  6  │ 30 Mar 26 │ 45 min   │ Progress review, action plan    │ 🟡 Medium  │ Productive ✅
  Next: 7 Apr 26

  TOTAL SESSIONS: 6 | Active since: 18 Jan 2026 (10 weeks)
```

---

## 3. Session Booking

```
BOOK COUNSELLING SESSION

  Student:       [TCC-2406 — Mohammed Riyaz Ahmed ▼]
  Counsellor:    [Ms. Ananya Roy ▼]
  Session type:  (●) Scheduled (●) Walk-in  ( ) Emergency
  Date:          [30 March 2026 ▼]   Time: [10:00 AM ▼]
  Duration:      [45 minutes ▼]
  Location:      [Counselling Room 1 (private) ▼]
  Agenda:        [Attendance, fee default, hostel smoking violation]

  PRIVACY SETTINGS:
    Session notes visible to: Counsellor + Branch Manager only
    Student can see: Session date and outcome summary only (not full notes)
    Parent notification: Not required (adult student, no POCSO concern)

  [Book Session]   [Mark as Emergency]   [Cancel]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-affairs/sessions/?student={sid}` | All sessions for a student |
| 2 | `POST` | `/api/v1/coaching/{id}/student-affairs/sessions/` | Book a new session |
| 3 | `POST` | `/api/v1/coaching/{id}/student-affairs/sessions/{sid}/notes/` | Add session notes (counsellor only) |
| 4 | `GET` | `/api/v1/coaching/{id}/student-affairs/sessions/{sid}/` | Session record (role-gated) |
| 5 | `PATCH` | `/api/v1/coaching/{id}/student-affairs/sessions/{sid}/risk/` | Update risk level |
| 6 | `GET` | `/api/v1/coaching/{id}/student-affairs/sessions/upcoming/` | Counsellor's upcoming sessions |

---

## 5. Business Rules

- Session notes are the most sensitive data in TCC's system; they contain a student's personal disclosures (family illness, financial hardship, mental health struggles); access is restricted to the counsellor and the Branch Manager (for escalated cases only); the Branch Manager does not routinely read session notes — they are briefed verbally by the counsellor about the student's situation and action needed; the Branch Manager accesses notes directly only when making a high-stakes decision (hostel continuation, enrollment continuation) and only the relevant session
- A student can request to see their own counselling records; under DPDPA 2023 (data principal's right of access), TCC must provide the student their personal data upon request; however, session notes written by the counsellor are part of TCC's professional record; TCC may provide a summary (outcome, risk level, action items) rather than the raw session notes, which contain the counsellor's professional judgments; legal advice should be sought if a student demands the complete raw notes — this is a nuanced area of DPDPA interpretation
- Risk level categorisation (High/Medium/Low) is the counsellor's professional assessment, not a formulaic calculation; the risk level informs the frequency of sessions (High = weekly, Medium = biweekly, Low = monthly check-in) and the Branch Manager's involvement (High cases are briefed to BM); a student who moves from High to Medium has improved but is not discharged — they continue on a lower-intensity monitoring plan; discharge from counselling caseload happens when the student has been stable for 4+ consecutive weeks and is approaching exam period with confidence
- The counsellor must not establish personal relationships with students outside the professional context; counselling students should not be added as social media contacts, contacted via personal WhatsApp, or met outside TCC premises; this professional boundary prevents dual-relationship conflicts and maintains the integrity of the therapeutic relationship; a counsellor who develops a friendship with a counselling student is in a conflict of interest; the Branch Manager should be informed if such a boundary issue arises
- Session records are retained for 5 years after the student's last interaction with TCC (longer than the standard DPDPA 2-year retention for general data); the extended retention is justified because: (a) a student who re-enrolls for a follow-on course needs continuity of welfare support, and (b) a student who files a welfare-related complaint years later may require TCC to demonstrate its duty of care; the 5-year retention is documented in TCC's data retention policy

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division J*
