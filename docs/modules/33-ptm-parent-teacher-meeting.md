# Module 33 — PTM (Parent-Teacher Meeting)

## 1. Purpose

Module 33 owns the complete Parent-Teacher Meeting lifecycle within EduForge institutions — from PTM scheduling and parent slot booking through teacher preparation, meeting conduct, notes, follow-up commitments, and outcome tracking. It ensures every parent has structured, time-boxed access to their child's teachers, and every concern raised is tracked to resolution.

The module serves all institution types — schools (where PTM is a mandatory CBSE/state board expectation), colleges (where it is less common but valuable for first-year students and at-risk cases), coaching centres (batch performance reviews), and residential institutions (where warden participates alongside class teacher). It aligns with NAAC Criterion 5.2 (Parent–Institution Interface) and integrates with Module 05 (Academic Calendar), Module 10 (Timetable), Module 11 (Attendance), Module 21 (Results), Module 26 (Fee Defaulters), Module 28 (Hostel), Module 32 (Counselling), Module 35 (Notifications), Module 37 (Email), and Module 42 (Audit Log).

---

## 2. PTM Configuration & Scheduling

### 2.1 PTM Types

| Type | When | Format |
|------|------|--------|
| Regular (quarterly/half-yearly) | After results or at calendar milestone | All parents; all class teachers |
| Subject-specific | When subject performance needs discussion | Parents of concerned students + subject teacher |
| One-on-one (on request) | Any time; parent or teacher requests | Single parent–teacher meeting |
| Emergency PTM | Acute concern (discipline, crisis, sudden decline) | Parent + class teacher + Principal |
| Online PTM | For outstation / NRI / working parents | Video meeting; same slot structure |
| Pre-board PTM | 4–6 weeks before Class 10/12 boards | Class teacher + subject teachers + counsellor |
| CWSN PTM | Quarterly; IEP review | Special educator + class teacher + parent + counsellor |
| Coaching batch review | Post-test series performance | Batch teacher + parent; rank and strategy discussed |
| Hostel PTM | For residential students | Class teacher + warden; parent or local guardian |

### 2.2 PTM Calendar

- PTM dates defined in Module 05 academic calendar
- Minimum: 2 PTMs per academic year (CBSE expectation); 4 recommended for schools
- PTM calendar visible to parents in app in advance
- Reminders sent 14, 7, and 2 days before PTM date

### 2.3 Teacher Slot Configuration

Each participating teacher defines available time blocks for the PTM day:
- Start time, end time, breaks
- Slot duration: 5 / 10 / 15 minutes (institution-configured)
- Maximum slots auto-computed: available time ÷ slot duration
- Lunch/break slots blocked automatically
- Timetable conflict check: if teacher has a scheduled class during PTM → resolved before booking opens (Module 10 integration)

### 2.4 Booking Window

Parent booking opens X days before PTM (configurable: 3–10 days):
- Parents see all teachers + available slots
- Class teacher slot: auto-booked for every parent (mandatory)
- Subject teacher slots: optional; parent selects which subjects to discuss
- Online/in-person preference: parent selects per slot (if online option enabled)
- Booking closes: 24 hours before PTM (or configurable)

---

## 3. Parent Notification & Booking

### 3.1 PTM Announcement

Sent via Module 35 (push notification) + Module 37 (email):
- PTM date, time, venue
- Booking window open/close dates
- "Book your slot" deep link
- Language: parent's preferred language (from Module 09 profile)

### 3.2 Slot Booking Interface

Parent sees:
- Grid of teachers × available slots
- Teacher name, subject, room number (or "Online" badge)
- Slot availability: green (available) / grey (booked by others)
- "Reason for meeting" optional text box (visible only to teacher; helps teacher prepare)
- Booking confirmation: instant; confirmation notification sent

### 3.3 Multi-Child Booking

Parent with 2+ children in the same institution:
- Child selector shown first; parent books slots for each child separately
- Combined view: all booked slots across children in one timeline view
- No overlap: system prevents double-booking same time slot for different children

### 3.4 Reminders

| When | Channel | Recipient |
|------|---------|----------|
| D-2 | App notification | Parent + teacher |
| D-0 (morning) | SMS + app | Parent + teacher |
| 30 minutes before slot | App notification | Parent |
| 2 minutes before slot | App notification | Parent (next in queue) |

### 3.5 Cancellation & Reschedule

- Parent cancels: slot released; available to other parents; teacher notified
- Teacher cancels: all affected parents notified; slots released or reassigned to substitute teacher
- Reschedule: parent or teacher requests; both parties confirm new slot via app

### 3.6 Non-Attending Parent Follow-up

- No-show logged per slot
- Class teacher sends message post-PTM to non-attending parent: "We missed you at PTM. Here's a brief summary of [Student Name]'s progress — [summary]. Please schedule a call if you'd like to discuss."
- 3 consecutive PTMs missed → flagged to Principal; home visit or certified letter considered

---

## 4. Teacher Preparation

### 4.1 Pre-PTM Student Brief (Auto-generated)

30 minutes before PTM start, teacher receives student-wise prep card per booked slot:

| Section | Data Source |
|---------|------------|
| Attendance % (term) | Module 11 |
| Last 3 exam scores | Module 21 |
| Homework submission rate | Module 14 |
| Disciplinary flags (if any) | Module 28 / class teacher notes |
| Counsellor flag (anonymised: "Well-being concern noted") | Module 32 |
| Previous PTM commitments | Module 33 (this module) |
| Current academic rank vs class | Module 21 |

Brief available on teacher app; no manual preparation required.

### 4.2 Red-Flag Auto-Highlight

Students auto-highlighted for teacher attention:
- Attendance < 60% (term)
- Score < 35% in any subject
- Score decline > 15 percentage points from last PTM
- Disciplinary incidents ≥ 2 in term
- Counselling referral pending or active
- Fee default (parent directed to accounts — teacher does not discuss financials)

### 4.3 Positive Highlights

System also surfaces achievements:
- Score improvement > 15 percentage points from last PTM
- Perfect attendance month
- Top 5 rank in class
- Homework submission rate 100%

Teachers encouraged to open every meeting with a strength before concerns.

### 4.4 Previous PTM History

Teacher sees per-student summary of last PTM:
- Concerns raised then
- Commitments made (teacher + parent)
- Were commitments met? (marked at current PTM)
- Continuity of conversation: parent feels heard across PTMs

### 4.5 Subject Teacher Coordination

Before PTM, class teacher aggregates:
- Each subject teacher's concern flags per student
- Creates a holistic one-page summary per student
- Subject teachers' individual notes not shared across peers; only class teacher sees the aggregate
- Prevents contradictory messages to same parent from different teachers

---

## 5. Meeting Conduct & Notes

### 5.1 Meeting Flow (In-person)

```
Parent arrives → checks in at front desk (name + child class)
  → Directed to teacher's room / table
  → Teacher marks slot as "Started" on app
  → Timer begins (slot duration countdown)
  → Discussion:
      → Attendance + academics
      → Behaviour / well-being
      → Parent's concerns
      → Commitments agreed (both sides)
  → T-2 minutes: gentle alert to teacher
  → Teacher marks slot "Ended"
  → Next parent in queue notified: "Your slot starts in 2 minutes"
```

### 5.2 Discussion Checklist

Structured checklist teacher works through:
- Academic performance: subject-wise; comparison to class average
- Attendance: absences reviewed; reasons if known
- Homework / assignment completion
- Classroom behaviour and participation
- Extracurricular involvement (if any)
- Health concern raised by parent
- Well-being / emotional state (without breaching counselling confidentiality)
- Parent's specific concerns (pre-filled reason from booking if provided)
- Next steps and commitments

### 5.3 Commitment Recording

| Commitment Type | Recorded By | Due Date | Tracking |
|----------------|------------|---------|---------|
| Parent will arrange tutoring | Teacher | 2 weeks | Reminder to parent at due date |
| Parent will take child to doctor | Teacher | 1 week | Reminder to parent at due date |
| Teacher will give extra attention | Teacher | Next exam | Auto-task in teacher's list |
| Teacher will refer to counsellor | Teacher | 3 days | Auto-referral to Module 32 |
| Student will complete pending work | Teacher | 1 week | Teacher follow-up task |
| Parent will attend next PTM | Teacher | Next PTM | Auto-reminder added |

Each commitment: owner, action, due date, status (Open / Met / Not met / Rescheduled).

### 5.4 Meeting Notes

| Field | Visibility |
|-------|-----------|
| Discussion summary | Teacher + class teacher + Principal |
| Parent concerns raised | Teacher + class teacher + Principal |
| Commitments (parent) | Teacher + parent (via app summary) |
| Commitments (teacher) | Teacher + Principal |
| Outcome code | Teacher + Principal |
| Referral actions | Teacher + counsellor (if applicable) |

Notes encrypted at rest. Cross-teacher visibility: subject teacher notes visible only to that teacher + class teacher. Not shared across subject teachers.

### 5.5 Outcome Codes

- Satisfactory — no concerns; routine update
- Requires follow-up — concern noted; commitments made; next check-in scheduled
- Escalated to Principal — serious concern requires Principal intervention
- Counselling referred — student referred to Module 32 during/after meeting
- Medical referred — health concern noted; referred to health room
- Academic warning issued — formal warning letter generated (see §5.6)
- Fee concern flagged — parent directed to accounts (no discussion in PTM)

### 5.6 Academic Warning Letter

If student at serious risk of fail or detention:
- Teacher raises "Academic warning" outcome
- Formal letter generated (WeasyPrint PDF): student name, academic status, improvement required, consequences of non-improvement, next review date
- Principal digital approval required before sending
- Sent to parent via Module 37 (email) + Module 35 (notification)
- Delivery confirmation tracked; acknowledgement requested from parent

---

## 6. Online PTM

### 6.1 Video Meeting Setup

- Unique video meeting link generated per slot (valid ±15 minutes from slot start time)
- Link sent to parent 30 minutes before slot via app + SMS
- Teacher joins from teacher app; parent joins from parent app (or browser link)
- Waiting room: if teacher is in previous meeting, parent sees "Meeting in progress — estimated wait: N minutes"

### 6.2 Meeting Features

| Feature | Detail |
|---------|--------|
| Screen share | Teacher shares student's report card, attendance graph, or exam paper scan |
| Recording | Only with explicit consent from both parties; prompted before start |
| Chat | In-meeting text chat for sharing links or typing names |
| Language | Both parties' language; interpreter can join as third participant |
| Connection quality | Good / Fair / Poor logged; affects NPS for online PTM |
| Fallback | If video fails → app prompts phone call; phone number auto-dialled |

### 6.3 Online PTM Security

- Link time-locked: valid only during booked slot window ± 15 minutes
- Expired link: shows "This slot has expired" screen
- Unique per slot: cannot use same link for different meeting
- Recording stored in R2; accessible to Principal on documented request; DPDPA-compliant

### 6.4 Accessibility for Online PTM

- Encouraged for: NRI parents, outstation parents, working parents who cannot take leave
- Specifically promoted to: hostel parents (Module 28), parents who missed in-person PTM
- Technical help: in-app chat support during PTM hours

---

## 7. PTM Summary & Parent Communication

### 7.1 Post-Meeting Summary

Within 24 hours of PTM:
- Teacher completes meeting summary in app per student met
- Summary structure:
  - Attendance status (Good / Needs improvement)
  - Academic summary (subject-wise brief)
  - Key strengths mentioned
  - Areas for improvement
  - Concerns discussed
  - Commitments: parent's + teacher's
  - Next review date

### 7.2 Summary Delivery

- Sent to parent via in-app notification + email (Module 37)
- Available in parent app → child profile → PTM history
- Multilingual: auto-translated to parent's preferred language; teacher reviews before sending
- Parent acknowledgement: parent taps "Acknowledged" in app; timestamp stored
- Non-acknowledgement after 72 hours → SMS nudge

### 7.3 Parent Disagreement

If parent disagrees with summary content:
- "Flag disagreement" button in app
- Reason field: parent describes specific disagreement
- Flagged to Principal + class teacher
- Mediation scheduled within 3 days: class teacher + parent + Principal
- Mediation outcome recorded; summary amended or upheld with note

### 7.4 PTM History Archive

- Full history of all PTMs per student accessible to:
  - Parent: their child's PTM summaries only
  - Teacher: their own meeting notes for their students
  - Class teacher: all summaries for their class
  - Principal: all summaries institution-wide
  - Counsellor: only summaries that include counselling referral flag
- 3-year retention; DPDPA-compliant archive

---

## 8. Follow-up & Commitment Tracking

### 8.1 Commitment Dashboard

Teacher's task list view:
- All open commitments from all PTMs across all students
- Filter: by student, by due date, by status
- Overdue commitments highlighted red
- One-tap mark as Complete / Not met / Rescheduled

### 8.2 Parent Commitment Reminders

When parent commits to an action:
- Due date stored
- At due date − 2 days: "Reminder: You committed to [action] for [student]. Due: [date]."
- At due date: reminder if not marked complete
- If not completed: class teacher follows up at next opportunity

### 8.3 Next PTM Pre-fill

At the next PTM cycle:
- Previous commitments auto-loaded per student
- Teacher reviews with parent: was each commitment met?
- Commitment resolution marked: Met ✓ / Not met — reason / Ongoing
- Unmet pattern (3+ consecutive PTMs same commitment unmet) → escalated to Principal

### 8.4 30-Day Academic Sprint

For students with academic concern raised in PTM:
- Counsellor + teacher jointly create a 3-action micro-plan (e.g., daily 30-min revision, weekly teacher check-in, tutoring arranged)
- Plan shared with student + parent in app
- 30-day progress check-in: teacher sends brief update to parent
- Outcome: improved / stable / further declined (next action varies)

### 8.5 Academic Outcome Correlation

System tracks:
- Students with academic concern raised in PTM
- Their next exam score vs PTM-date baseline
- Improvement rate: % of concerned students who improved after PTM + follow-up
- Used as evidence of PTM effectiveness for NAAC + management reporting

---

## 9. Special PTM Protocols

### 9.1 Emergency PTM

Triggered by: sudden academic decline, critical incident, disciplinary matter, parental request, counsellor escalation.

- Formal notice generated: sent via SMS + email + app; delivery confirmation required
- Required attendees: parent(s) + class teacher + Principal; counsellor if welfare concern
- Held within 48 hours of trigger
- Minutes recorded; outcome code; action plan with named owners + deadlines

### 9.2 CWSN Quarterly PTM

- Held every term (not just twice per year)
- Participants: parent + student (if appropriate) + class teacher + special educator + counsellor
- Agenda: IEP goals review, progress against accommodations, next term goals, exam support plan
- IEP updated at meeting; parent signs off on updated IEP
- Minutes stored in Module 32 (counselling) case file + Module 33 PTM record

### 9.3 Pre-Board PTM (Class 10 / 12)

- Held 4–6 weeks before board exams
- Participants: parent + student + all subject teachers + counsellor
- Focus: exam strategy, time table, stress management, last-minute preparation
- Counsellor presents exam anxiety management resources to all parents collectively (group session first, then individual slots)
- Action: identify high-risk students; intensive support plan for final weeks

### 9.4 Transfer/Withdrawal PTM

Before any TC is issued (Module 39):
- Mandatory meeting: parent + class teacher + counsellor
- Goal: understand reason for leaving; retention attempt if appropriate
- Record: reason for withdrawal, retention conversation outcome, referral if needed
- If staying: concerns addressed; action plan
- If leaving: smooth exit; positive relationship maintained (alumni potential)

### 9.5 Hostel PTM

For residential students:
- Participants: parent (in-person / online) + class teacher + warden (Module 28)
- Warden's input: hostel well-being, room behaviour, meal patterns, outpass usage
- Integration: Module 28 well-being score + meal skip data shown to teacher + parent
- For outstation parents: online format; warden joins teacher's video call

### 9.6 Coaching Centre PTM

Post-test series:
- Test scores, rank, percentile compared to institute target and last-year AIR/state rank
- Weak areas identified; study plan adjusted
- Parent motivation management: counsellor present for stressed batches
- Rank prediction: based on trend; realistic target range shown to parent

---

## 10. Analytics & Reporting

### 10.1 PTM Participation Dashboard

| Metric | View Level |
|--------|-----------|
| Overall attendance % (parents attended ÷ invited) | Institution, class, subject |
| Slots utilised % (slots booked ÷ available) | Per teacher |
| No-shows | Per PTM, per class |
| Online vs in-person split | Institution-wide |
| Average rating (parent feedback) | Per teacher, per PTM |
| Concerns raised count | Per category, per PTM |
| Commitments made | Open / Met / Overdue |
| Counselling referrals from PTM | Count per PTM |

### 10.2 Concern Frequency Analysis

Most common parent concerns per PTM cycle:
- Academic performance (subject-wise: which subjects concern parents most)
- Attendance
- Bullying / peer conflict
- Teacher feedback (teaching quality)
- Infrastructure (facilities)
- Transport / timing

Top 3 concerns each cycle reported to Principal; institutional improvement tracked.

### 10.3 Teacher PTM Quality Score

| Metric | Weight |
|--------|--------|
| % slots with notes completed within 24 hours | 30% |
| Average parent feedback rating | 40% |
| Commitment completion rate (teacher's own) | 30% |

Score visible to Principal. Low scores: Principal coaching conversation scheduled.

### 10.4 Parent Engagement Score

Composite score per family:
- PTM attendance (40%)
- App notification read rate (20%)
- Fee payment punctuality (20%)
- Response to teacher messages (20%)

Low-engagement families: flagged to class teacher + counsellor (Module 32 EWS input). Students from low-engagement families given extra institutional support.

### 10.5 NAAC Criterion 5.2 Data

Auto-populated:
- Number of PTMs conducted per year
- Parent participation % per PTM
- Parent satisfaction score (from feedback)
- Issues resolved through PTM
- PTM-linked academic improvement rate

---

## 11. Strategic Features

### 11.1 Smart Slot Recommendation

Before parent books slots:
- System analyses: student's red-flag status per subject, previous PTM history, parent's history of skipping subject slots
- Recommendation shown: "Based on [Student Name]'s performance, we recommend meeting [Math Teacher] and [Science Teacher] this PTM."
- Parent can follow or override recommendation
- Uptake of recommendations tracked: do parents who follow recommendations have better outcomes?

### 11.2 PTM Attendance Prediction

ML model (trained on historical PTM data):
- Predicts which parents are likely to not attend
- Features: past attendance, distance from school, employment type (from school records), time of PTM, number of children
- 5 days before PTM: high no-show-risk parents receive personal call from class teacher ("We really value meeting you…")
- Targeted outreach reduces no-show rate measurably

### 11.3 Multilingual Summary Generation

- Post-PTM summary written by teacher in English or Hindi
- Auto-translated to parent's preferred language before sending
- Teacher reviews translation (one-click approve or edit)
- Languages: Hindi, Telugu, Tamil, Kannada, Malayalam, Bengali, Marathi, Gujarati
- Improves parent comprehension; especially critical for first-generation education families

### 11.4 Anonymous Parent Concern Box

Pre-PTM:
- Parents submit concerns anonymously via app (open 2 weeks before PTM)
- Concern type: teaching method / bully allegation / infrastructure / peer issue / other
- Counsellor + Principal see; addressed without identifying parent
- Aggregate theme from anonymous concerns shared at PTM opening address by Principal
- Reduces fear of being "labelled a difficult parent"

### 11.5 Sibling Family Coordination View

For institutions with multiple siblings from the same family:
- Class teachers of siblings can see a "family context" flag (e.g., "Parent also has child in Class 7")
- Cross-sibling insights shared with consent: family hardship, illness, domestic difficulty
- Prevents one teacher giving very different feedback from another to the same parent on the same day
- Coordinated family support plan if needed

### 11.6 Post-PTM Academic Sprint

For every student with "Requires follow-up" outcome:
- System creates shared action plan (visible to student + parent + teacher in app)
- 3 specific, measurable actions with owners and deadlines
- 30-day check-in auto-scheduled for teacher
- Success metric: next exam score vs baseline
- Sprint completion certificate (symbolic; encourages follow-through)

---

## 12. Integration Map

| Module | Integration |
|--------|------------|
| Module 05 — Academic Calendar | PTM dates configured; holidays excluded from scheduling |
| Module 10 — Timetable | Teacher PTM slots cross-checked against class schedule |
| Module 11 — Attendance | Attendance % loaded in pre-PTM student brief |
| Module 14 — Homework & Assignments | Submission rate loaded in pre-PTM brief |
| Module 21 — Results | Exam scores + rank loaded for teacher prep |
| Module 26 — Fee Defaulters | Fee default flag shown to teacher (direct to accounts; no discussion) |
| Module 28 — Hostel | Warden participates in hostel PTM; well-being data shared |
| Module 32 — Counselling | Referrals raised; CWSN PTM coordinated; EWS flags informed |
| Module 35 — Notifications | All parent + teacher reminders and notifications |
| Module 37 — Email | Academic warning letters; post-PTM summaries |
| Module 39 — Certificates & TC | Transfer/withdrawal PTM mandatory before TC |
| Module 42 — DPDPA & Audit Log | Meeting notes access, summary delivery audited |

---

## 13. Data Model (Key Tables)

```
ptm_events
  id, tenant_id, ptm_name, ptm_type, ptm_date, academic_year,
  booking_opens_on, booking_closes_on, slot_duration_min,
  venue, online_enabled, status, created_by, created_at

ptm_teacher_slots
  id, ptm_event_id, teacher_id, subject_id, date, slot_start,
  slot_end, modality, room_no, video_link, status

ptm_bookings
  id, ptm_event_id, slot_id, parent_id, student_id,
  booked_at, booking_reason, status, attended,
  cancellation_reason, cancelled_at

ptm_meeting_notes
  id, booking_id, teacher_id, student_id, conducted_at,
  discussion_items_json, red_flags_discussed, positives_noted,
  outcome_code, referral_raised, notes_text, completed_at

ptm_commitments
  id, meeting_note_id, owner_type, owner_id, action_description,
  due_date, status, met_at, not_met_reason, created_at

ptm_summaries
  id, meeting_note_id, student_id, parent_id, summary_text,
  language, sent_at, acknowledged_at, disagreement_raised,
  disagreement_reason, mediation_scheduled

ptm_feedback
  id, booking_id, parent_id, rating, comment, submitted_at

ptm_emergency_events
  id, tenant_id, student_id, triggered_by, trigger_reason,
  notice_sent_at, scheduled_date, attendees, minutes,
  outcome_code, action_plan_json

ptm_online_sessions
  id, booking_id, video_link, join_time_parent, join_time_teacher,
  leave_time_parent, leave_time_teacher, duration_min,
  connection_quality, recorded, recording_r2_key, fallback_used

ptm_family_flags
  id, tenant_id, family_id, siblings_json, family_context_note,
  counsellor_aware, created_at

ptm_parent_engagement_scores
  id, parent_id, academic_year, ptm_attendance_score,
  notification_read_score, fee_punctuality_score,
  response_rate_score, composite_score, computed_at
```

---

## Cross-Module References

- **Module 05**: PTM dates in academic calendar; holiday exclusion for scheduling — read-only
- **Module 10**: Teacher timetable for PTM slot conflict check — read-only
- **Module 11**: Attendance % for teacher prep brief — read-only
- **Module 14**: Homework submission rate for prep brief — read-only
- **Module 21**: Exam scores + rank for prep brief — read-only
- **Module 26**: Fee default flag visible to teacher (redirect to accounts) — read-only
- **Module 28**: Warden input to hostel PTM; well-being score shown — read + event
- **Module 32**: Counselling referral raised from PTM; CWSN PTM coordinated; parent engagement feeds EWS — write
- **Module 35**: All PTM notifications, reminders, summaries dispatched — write
- **Module 37**: Academic warning letters, post-PTM summaries emailed — write
- **Module 39**: Withdrawal PTM mandatory before TC issued — event trigger read
- **Module 42**: Notes access, summary delivery, commitment tracking audited — write

---

*Module 33 complete. Next: Module 34 — Announcements & Circulars.*
