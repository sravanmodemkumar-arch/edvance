# Group 2 — Division B: Group Academic Leadership — Pages Reference

> **Division:** B — Group Academic Leadership
> **Roles:** 15 roles (see Role Summary)
> **Base URL prefix:** `/group/acad/`
> **Theme:** Light (`portal_base.html`)
> **Status key:** ✅ Spec done · ⬜ Not started

---

## Scale Context

| Dimension | Value |
|---|---|
| Institution Groups on Platform | 150 |
| Branches per group | 5–50 (large: 20–50 · small: 5–10) |
| Students per large group | 20,000–1,00,000 |
| Students per small group | 2,000–8,000 |
| Streams | MPC · BiPC · MEC · CEC · HEC · IIT Foundation (Cl.6–10) · Integrated JEE/NEET |
| Academic year | April 1 – March 31 |
| Subject-topic pairs per stream | ~80–120 per stream |
| Central question bank (group-level) | 10,000–50,000 MCQs |
| Teachers across large group | 2,000–5,000 |
| Concurrent branch exams | All 50 branches may run simultaneously |
| Olympiad exams tracked | NTSE · NMMS · NSO · IMO · KVPY · JEE · NEET · KCET |
| Special needs students (large group) | 100–500 with active IEPs |
| IIT Foundation classes | Class 6–10 (5 levels × multiple sections) |

---

## Division B — Role Summary

| # | Role | Level | Large | Small | Post-Login URL |
|---|---|---|---|---|---|
| 9 | Chief Academic Officer (CAO) | G4 | ✅ Dedicated | ✅ (Principal covers) | `/group/acad/cao/` |
| 10 | Group Academic Director | G3 | ✅ Dedicated | ❌ | `/group/acad/director/` |
| 11 | Group Curriculum Coordinator | G2 | ✅ Dedicated | ✅ shared | `/group/acad/curriculum-coord/` |
| 12 | Group Exam Controller | G3 | ✅ Dedicated | ✅ shared | `/group/acad/exam-controller/` |
| 13 | Group Results Coordinator | G3 | ✅ Dedicated | ❌ | `/group/acad/results-coord/` |
| 14 | Group Stream Coord — MPC | G3 | ✅ Dedicated | ❌ | `/group/acad/stream/mpc/` |
| 15 | Group Stream Coord — BiPC | G3 | ✅ Dedicated | ❌ | `/group/acad/stream/bipc/` |
| 16 | Group Stream Coord — MEC/CEC | G3 | ✅ Dedicated | ❌ | `/group/acad/stream/mec-cec/` |
| 16a | Group Stream Coord — HEC *(2nd-audit addition)* | G3 | ✅ Dedicated | ❌ | `/group/acad/stream/hec/` |
| 17 | Group JEE/NEET Integration Head | G3 | ✅ Dedicated | ❌ | `/group/acad/jee-neet/` |
| 18 | Group IIT Foundation Director | G3 | ✅ Dedicated | ❌ | `/group/acad/iit-foundation/` |
| 19 | Group Olympiad & Scholarship Coord | G3 | ✅ Dedicated | ✅ shared | `/group/acad/olympiad/` |
| 20 | Group Special Education Coordinator | G3 | ✅ Dedicated | ✅ shared | `/group/acad/special-ed/` |
| 21 | Group Academic MIS Officer | G1 | ✅ Dedicated | ✅ shared | `/group/acad/mis/` |
| 22 | Group Academic Calendar Manager | G3 | ✅ Dedicated | ✅ shared | `/group/acad/cal-manager/` |

---

## Section 1 — Role Dashboards (post-login landing, one per role)

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 01 | CAO Dashboard | `/group/acad/cao/` | `01-cao-dashboard.md` | P0 | ⬜ |
| 02 | Academic Director Dashboard | `/group/acad/director/` | `02-academic-director-dashboard.md` | P0 | ⬜ |
| 03 | Curriculum Coordinator Dashboard | `/group/acad/curriculum-coord/` | `03-curriculum-coord-dashboard.md` | P0 | ⬜ |
| 04 | Exam Controller Dashboard | `/group/acad/exam-controller/` | `04-exam-controller-dashboard.md` | P0 | ⬜ |
| 05 | Results Coordinator Dashboard | `/group/acad/results-coord/` | `05-results-coord-dashboard.md` | P0 | ⬜ |
| 06 | Stream Coordinator MPC Dashboard | `/group/acad/stream/mpc/` | `06-stream-mpc-dashboard.md` | P0 | ⬜ |
| 07 | Stream Coordinator BiPC Dashboard | `/group/acad/stream/bipc/` | `07-stream-bipc-dashboard.md` | P0 | ⬜ |
| 08 | Stream Coordinator MEC/CEC Dashboard | `/group/acad/stream/mec-cec/` | `08-stream-mec-cec-dashboard.md` | P0 | ⬜ |
| 09 | JEE/NEET Integration Head Dashboard | `/group/acad/jee-neet/` | `09-jee-neet-dashboard.md` | P0 | ⬜ |
| 10 | IIT Foundation Director Dashboard | `/group/acad/iit-foundation/` | `10-iit-foundation-dashboard.md` | P0 | ⬜ |
| 11 | Olympiad & Scholarship Coord Dashboard | `/group/acad/olympiad/` | `11-olympiad-dashboard.md` | P0 | ⬜ |
| 12 | Special Education Coordinator Dashboard | `/group/acad/special-ed/` | `12-special-ed-dashboard.md` | P0 | ⬜ |
| 13 | Academic MIS Officer Dashboard | `/group/acad/mis/` | `13-mis-dashboard.md` | P0 | ⬜ |
| 14 | Academic Calendar Manager Dashboard | `/group/acad/cal-manager/` | `14-cal-manager-dashboard.md` | P0 | ⬜ |

### Dashboard Widget Inventory — by Role

**01 — CAO Dashboard (G4)**
> Full academic command centre. All streams, all branches, all functions visible.

| Widget | Type | Description |
|---|---|---|
| Academic Health Score | Gauge chart (0–100) | Composite: attendance × result % × curriculum adherence × teacher performance |
| Curriculum Coverage by Branch | Horizontal bar chart | % syllabus completed this term per branch — red < 70%, amber < 85% |
| Exam Calendar Conflicts | Alert banner | Live count of unresolved scheduling conflicts — links to Exam Conflict Monitor |
| Pending Approvals Queue | Counter cards | Exam papers (n) · Result releases (n) · IEP reviews (n) · Policy changes (n) |
| Stream Result Summary | 4-column stat grid | MPC / BiPC / MEC-CEC / Foundation — group avg this term vs last term |
| Top 5 / Bottom 5 Branches | Split table | Ranked by academic health score with delta arrows |
| Teacher Performance Alerts | List with severity dots | Branches where avg teacher rating < 3.0 — action required |
| Upcoming Major Exams | Timeline | Next 14 days — branch count, exam type, approval status |
| Special Ed IEP Due | Alert counter | IEPs with review overdue — links to Special Ed section |
| Result Publication Queue | Status strip | Results approved and awaiting publication across branches |
| Recent Academic Decisions | Audit trail | Last 10 CAO actions with timestamp and branch |

**02 — Academic Director Dashboard (G3)**
> Syllabus design, teacher performance, and academic MIS daily operations.

| Widget | Type | Description |
|---|---|---|
| Syllabus Completion Rate | Multi-line chart | By branch and stream — term-to-date |
| Teacher Performance Distribution | Histogram | Rating bands 1–5 across all branches |
| Lesson Plan Submission Rate | Branch table | Branches with < 90% submission flagged amber/red |
| Teacher Observations Due | Alert counter | Observations scheduled but not logged this month |
| Academic MIS Summary | KPI strip | Attendance % · Avg marks · Dropout rate · Teacher absenteeism |
| CPD Completion Rate | Donut chart | Teaching staff who completed mandatory CPD this year |
| Low-performing Subjects | Table | Subject × Branch pairs where avg marks < pass threshold |
| Upcoming Lesson Plan Deadlines | Calendar strip | Deadlines for lesson plan uploads next 7 days |

**03 — Curriculum Coordinator Dashboard (G2)**
> Content upload, lesson plan standards, and curriculum library status.

| Widget | Type | Description |
|---|---|---|
| Content Library Stats | Stat cards | Total resources · Added this month · Pending approval · Rejected |
| Upload Queue Status | Progress list | Files uploaded today — Processing / Approved / Rejected |
| Lesson Plan Coverage | Branch × Subject heatmap | Colour-coded coverage: red = no plan, green = complete |
| Pending Content Reviews | Action queue | Content submitted by branches awaiting group-level approval |
| Subject-Topic Gaps | Alert list | Topics with zero lesson plans across any branch |
| Content Downloads by Branch | Bar chart | Most-accessed resources this term |
| Recent Uploads | Table | Last 20 uploads — name, subject, uploader, status |

**04 — Exam Controller Dashboard (G3)**
> Question bank, exam papers, scheduling, and result moderation hub.

| Widget | Type | Description |
|---|---|---|
| Question Bank Health | Stat cards | Total MCQs · Per stream · Added this month · Flagged/review |
| Exam Schedule Status | Kanban counts | Draft · Pending Approval · Approved · Live · Completed |
| Papers in Draft | Action list | Exam papers not yet submitted for approval — creator + deadline |
| Result Moderation Queue | Counter | Results uploaded by branches awaiting moderation |
| Answer Key Publication | Status table | Papers with answer key pending publication |
| Exam Conflicts Unresolved | Alert banner | Red if > 0 · Counts conflicts per date |
| Recent Paper Activity | Audit trail | Last 10 paper actions — create/edit/approve/publish |
| Branch Readiness | Table | Branches who have NOT confirmed exam setup < 48 hrs before exam |

**05 — Results Coordinator Dashboard (G3)**
> Cross-branch rank engine, topper tracking, and result publication control.

| Widget | Type | Description |
|---|---|---|
| Rank Computation Queue | Status list | Exams awaiting rank computation — marks uploaded Y/N |
| Results Published Today | Counter | Links to published result pages |
| Topper Update | Stat cards | Group rank #1–10 names + scores — current term |
| Branch-wise Average Score | Bar chart | All branches for most recent group exam |
| Subject Rank Distribution | Stacked bar | Score band breakdown per subject (A/B/C/D/F) |
| Cross-branch Rank Leaderboard | Top 10 table | Roll no, name, branch, stream, score, rank |
| Result Archive Quick-access | Recent list | Last 5 published exams |
| Rank Computation Status | Progess bar | % branches whose marks are uploaded for ongoing computation |

**06–08 — Stream Coordinator Dashboards (MPC / BiPC / MEC-CEC) (G3)**
> Identical layout, data filtered to respective stream only.

| Widget | Type | Description |
|---|---|---|
| Stream Syllabus Completion | Per-subject progress bars | Physics / Chemistry / [Maths or Biology or Commerce] by branch |
| Stream Average Score Trend | Line chart | Term-over-term group average per subject |
| Teacher Load by Subject | Bar chart | Teachers per subject × branch — identify understaffed subjects |
| Lesson Plan Submission | Heatmap | Branch × Subject — colour-coded status |
| Top & Bottom Branch (Stream) | Split table | Ranked by stream avg |
| Upcoming Stream Exams | Timeline | Next 14 days for this stream only |
| Content Gap Alerts | Alert list | Topics with no study material in library |
| Stream Announcement Drafts | Draft list | Communications to stream teachers not yet sent |

**09 — JEE/NEET Integration Head Dashboard (G3)**

| Widget | Type | Description |
|---|---|---|
| JEE/NEET Test Series Progress | Milestone tracker | Tests planned vs conducted vs results published |
| Integrated Student Count | Stat cards | JEE stream (MPC+coaching) · NEET stream (BiPC+coaching) per branch |
| Mock Test Score Trend | Line chart | Group avg per mock test across JEE / NEET series |
| Topic Coverage vs JEE Syllabus | % heatmap | NTA syllabus topics covered vs not yet covered |
| High Performers (AIR Potential) | Table | Students in top-5% nationally by mock percentile |
| Coaching Schedule Conflicts | Alert list | Integrated coaching clashing with regular timetable |
| Result Moderation — Coaching Tests | Queue counter | Coaching test results awaiting approval |
| Parent Communication Queue | Counter | Coaching fee or schedule-related parent queries pending |

**10 — IIT Foundation Director Dashboard (G3)**

| Widget | Type | Description |
|---|---|---|
| Foundation Program Coverage | By class (6–10) progress bars | Syllabus completion per class level |
| Foundation Test Scores by Class | Grouped bar chart | Avg score per class — this term |
| Class-wise Enrollment | Stat cards | Students enrolled per class, branch |
| Top Foundation Students | Leaderboard table | Rank within group by foundation score |
| Teacher Qualification Flag | Alert list | Branches where foundation teacher lacks IIT background |
| Upcoming Foundation Tests | Timeline | Next 14 days |
| Scholarship Eligibility Tracker | Counter | Foundation students eligible for internal merit scholarship |

**11 — Olympiad & Scholarship Coordinator Dashboard (G3)**

| Widget | Type | Description |
|---|---|---|
| Olympiad Calendar | Event strip | All upcoming olympiads with registration deadline |
| Registrations by Exam | Stat cards | NTSE · NMMS · NSO · IMO · KVPY — students registered |
| Results Tracker | Status table | Submitted / Awaiting / Results Received per olympiad |
| Medals & Ranks | Highlight cards | Gold/Silver/Bronze counts this year across all branches |
| Branch Participation Rate | Bar chart | % eligible students registered per olympiad per branch |
| Scholarship Exam Pipeline | Kanban | Announced · Registration · Exam · Results · Award |
| Follow-up Due | Alert list | Students who qualified but not yet awarded scholarship |

**12 — Special Education Coordinator Dashboard (G3)**

| Widget | Type | Description |
|---|---|---|
| Active IEPs | Stat card | Total · Due for review this month · Overdue |
| Student Type Breakdown | Donut chart | Learning disability · Physical disability · Hearing/Vision impairment |
| Accommodation Request Status | Table | Pending / Approved / Implemented per branch |
| IEP Review Compliance | Branch heatmap | Branches with overdue IEP reviews highlighted |
| Exam Accommodation Queue | Alert list | Students with approved accommodations — upcoming exams need setup |
| POCSO / Welfare Coordination | Alert strip | Special needs incidents flagged from branch level |
| Branch Caseload | Bar chart | Count of special needs students per branch |

**13 — Academic MIS Officer Dashboard (G1 — read-only)**
> No write controls. Data-dense read-only view.

| Widget | Type | Description |
|---|---|---|
| Monthly MIS Summary | Stat cards | Avg attendance · Avg result · Dropout count · Teacher absenteeism |
| Subject-wise Performance Table | Full sortable table | All subjects × all branches — avg marks, pass %, rank |
| Branch-wise MIS Report | Quick-download links | Download branch MIS as PDF/XLSX |
| Teacher Performance by Branch | Bar chart | Avg teacher rating per branch |
| Trend Chart | Multi-line chart | Last 6 terms — attendance, avg marks, dropout |
| Report Scheduler | Upcoming list | Scheduled auto-reports and next-run times |

**14 — Academic Calendar Manager Dashboard (G3)**

| Widget | Type | Description |
|---|---|---|
| Calendar Coverage | Stat cards | Working days set · PTM dates set · Holidays declared · Events pending |
| Branch Calendar Sync Status | Branch table | Confirmed / Pending / Conflict per branch |
| Upcoming Events (14 days) | Timeline | All group-level academic events across all branches |
| Holiday Approval Queue | Counter | Branch-submitted holiday requests awaiting group approval |
| PTM Schedule | List | PTM dates per branch — parent notification sent Y/N |
| Calendar Conflict Alerts | Alert banner | Branches with overlapping events |
| Academic Year Progress | Progress bar | Day X of Y in academic year — working days elapsed |

---

## Section 2 — Curriculum & Content Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 15 | Syllabus Manager | `/group/acad/syllabus/` | `15-syllabus-manager.md` | P0 | ⬜ |
| 16 | Lesson Plan Standards | `/group/acad/lesson-plans/` | `16-lesson-plan-standards.md` | P1 | ⬜ |
| 17 | Shared Content Library | `/group/acad/content-library/` | `17-shared-content-library.md` | P0 | ⬜ |
| 18 | Subject-Topic Master | `/group/acad/subject-topic/` | `18-subject-topic-master.md` | P0 | ⬜ |
| 19 | Stream Configuration | `/group/acad/streams/` | `19-stream-configuration.md` | P1 | ⬜ |
| 20 | Textbook & Resource Mapping | `/group/acad/textbooks/` | `20-textbook-resource-mapping.md` | P2 | ⬜ |
| 21 | Content Upload Queue | `/group/acad/content-uploads/` | `21-content-upload-queue.md` | P1 | ⬜ |

### Page Specs — Section 2

**15 — Syllabus Manager** `/group/acad/syllabus/`
> Group-wide syllabus master. Branches inherit — can view but not override.

| Element | Spec |
|---|---|
| **Table** | Columns: Stream · Class · Subject · Total Topics · Covered % · Last Updated · Board · Status · Actions |
| **Filters** | Stream (MPC/BiPC/MEC/CEC/HEC/Foundation) · Class · Subject · Board (CBSE/State) · Status (Active/Draft/Archived) |
| **Search** | Subject name, topic keyword |
| **Pagination** | Server-side, 25/page |
| **Row Actions** | View Topics · Edit · Archive · Clone for Another Stream |
| **Drawer: syllabus-create** | 640px · Tabs: Stream & Class · Subjects · Topic List · Board Mapping · Publish |
| **Drawer: syllabus-view** | 560px · Tabs: Overview · Topics · Branch Adherence · History |
| **Drawer: topic-edit** | 480px · Fields: Topic name, subtopics, sequence no., difficulty, hours to teach, linked resources |
| **Charts** | Curriculum completion by branch (bar) · Topic coverage heatmap by subject |
| **Role visibility** | CAO/Academic Dir: Full edit · Curriculum Coord: Upload/edit topics · Stream Coords: View own stream · MIS: Read-only · Others: No access |
| **Empty state** | "No syllabus defined for this stream. Start by selecting a stream and board." + Create CTA |

**16 — Lesson Plan Standards** `/group/acad/lesson-plans/`
> Standardised lesson plan templates all branches must follow. CAO sets format; branches submit.

| Element | Spec |
|---|---|
| **Table** | Columns: Subject · Topic · Class · Stream · Template Type · Branch Submissions · Compliance % · Last Updated · Status |
| **Filters** | Stream · Subject · Class · Compliance Band (< 70% / 70–90% / ≥ 90%) · Status |
| **Search** | Topic name |
| **Drawer: plan-template-create** | 640px · Tabs: Template Structure · Required Sections · Assessment Checklist · Publish |
| **Drawer: branch-submission-view** | 560px · Tabs: Submitted Plans · Missing Submissions · Feedback sent |
| **Bulk action** | "Send reminder to non-compliant branches" → generates WhatsApp/email |
| **Role visibility** | CAO: Full · Academic Dir: Full · Curriculum Coord: Create/edit templates · Stream Coords: View own stream · Branches: Submit only (via branch portal) |

**17 — Shared Content Library** `/group/acad/content-library/`
> Central repository. Notes (PDF/text), videos (YouTube URL), MCQ sets, revision sheets.

| Element | Spec |
|---|---|
| **Table** | Columns: Title · Type (PDF/Video/MCQ Set/Revision) · Subject · Topic · Stream · Class · Uploaded By · Date · Downloads · Status · Actions |
| **Filters** | Content Type · Stream · Subject · Class · Status (Active/Pending Review/Rejected/Archived) · Date range |
| **Search** | Title, topic keyword — full-text, 300ms debounce |
| **Pagination** | Server-side, 25/page with total count badge |
| **Row Actions** | View · Download · Edit Metadata · Archive · Move to Stream |
| **Drawer: content-upload** | 680px · Tabs: File/Link · Metadata (subject/topic/class/stream) · Access Scope · Preview · Submit |
| **Drawer: content-review** | 560px · Tabs: Preview · Metadata · Reviewer Notes · Approve / Reject |
| **Bulk actions** | Archive selected · Move to subject · Change stream |
| **Charts** | Downloads by subject (bar) · Content additions per month (line) · Coverage by topic (% complete) |
| **Role visibility** | CAO/Academic Dir: Full + approve · Curriculum Coord: Upload + edit own · Stream Coords: Upload for own stream · MIS: Read-only · Branches: Read-only (via branch portal) |
| **Empty state** | "No content for this subject yet. Upload the first resource." + Upload CTA |

**18 — Subject-Topic Master** `/group/acad/subject-topic/`
> The canonical subject → topic → subtopic hierarchy. All other modules reference this master.

| Element | Spec |
|---|---|
| **Tree view** | Expand/collapse: Stream → Class → Subject → Chapter → Topic → Subtopic |
| **Table view** | Flat table with above columns sortable |
| **Filters** | Stream · Class · Subject · Chapter |
| **Drawer: subject-create** | 480px · Fields: Name, stream, class, board mapping, passing marks |
| **Drawer: topic-create** | 480px · Fields: Chapter, topic name, subtopics (add/remove rows), sequence, estimated hours, difficulty (1–5), NCERT reference |
| **Bulk import** | CSV template download + upload with validation error report |
| **Export** | Full hierarchy XLSX export |
| **Role visibility** | CAO: Full · Academic Dir: Full · Curriculum Coord: Edit · Stream Coords: View own · All others: No access |

**19 — Stream Configuration** `/group/acad/streams/`
> Defines what a stream IS — subjects, subject weightages, eligibility, passing criteria.

| Element | Spec |
|---|---|
| **Stream cards** | One card per stream — MPC/BiPC/MEC/CEC/HEC/Foundation/Integrated JEE/Integrated NEET |
| **Card content** | Subjects list · Min marks per subject · Aggregate pass % · Class range · Active branches count · Edit button |
| **Drawer: stream-edit** | 640px · Tabs: Identity · Subjects & Weights · Pass Criteria · Eligible Classes · Branch Toggle |
| **Role visibility** | CAO: Full edit · Academic Dir: View + propose changes · Stream Coords: View own only · Others: No access |

**20 — Textbook & Resource Mapping** `/group/acad/textbooks/`
> Maps prescribed textbooks per subject per class per board. Used by branches for procurement.

| Element | Spec |
|---|---|
| **Table** | Columns: Board · Class · Subject · Textbook Name · Publisher · ISBN · Year · Price · Status |
| **Filters** | Board · Class · Subject · Year · Publisher |
| **Drawer: textbook-add** | 480px · Fields: Board, class, subject, title, publisher, ISBN, edition year, approx price, alternate text |
| **Export** | Branch-ready procurement list XLSX |
| **Role visibility** | CAO/Academic Dir/Curriculum Coord: Full · Others: Read-only |

**21 — Content Upload Queue** `/group/acad/content-uploads/`
> Workflow page: branch-submitted content awaiting group review/approval before going live.

| Element | Spec |
|---|---|
| **Table** | Columns: Title · Type · Subject · Branch · Submitted By · Submitted At · Assigned Reviewer · Status · Actions |
| **Filters** | Status (Pending/In Review/Approved/Rejected) · Stream · Subject · Branch · Date range |
| **Search** | Title |
| **Row Actions** | Preview · Assign Reviewer · Approve · Reject with reason |
| **Drawer: content-review** | 560px · Tabs: Preview · Metadata · Reviewer Notes · Decision |
| **Bulk actions** | Approve selected · Assign all pending to reviewer |
| **Empty state** | "No content pending review." (different from "no uploads ever") |
| **Role visibility** | CAO: Full · Curriculum Coord: Review + approve · Stream Coords: Review own stream · Academic Dir: Approve/reject · Branch: Submit only via branch portal |

---

## Section 3 — Exam Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 22 | Group Exam Calendar | `/group/acad/exam-calendar/` | `22-group-exam-calendar.md` | P0 | ⬜ |
| 23 | Question Bank | `/group/acad/question-bank/` | `23-question-bank.md` | P0 | ⬜ |
| 24 | Exam Paper Builder | `/group/acad/exam-papers/` | `24-exam-paper-builder.md` | P0 | ⬜ |
| 25 | Branch Exam Schedule | `/group/acad/branch-exam-schedule/` | `25-branch-exam-schedule.md` | P1 | ⬜ |
| 26 | Exam Conflict Monitor | `/group/acad/exam-conflicts/` | `26-exam-conflict-monitor.md` | P1 | ⬜ |
| 27 | Result Moderation | `/group/acad/result-moderation/` | `27-result-moderation.md` | P0 | ⬜ |
| 28 | Mark Scheme & Answer Keys | `/group/acad/answer-keys/` | `28-answer-keys.md` | P1 | ⬜ |

### Page Specs — Section 3

**22 — Group Exam Calendar** `/group/acad/exam-calendar/`
> Master exam schedule — pushed to all branches. Branches cannot override group exam dates.

| Element | Spec |
|---|---|
| **Calendar view** | Month/Week/List toggle · Events colour-coded by exam type (Unit Test / Mid-term / Annual / Olympiad / Mock / Coaching) |
| **Table view** | Columns: Exam Name · Stream · Class · Date · Duration · Branches · Status · Paper Status · Conflicts |
| **Filters** | Exam Type · Stream · Class · Branch · Status · Date range |
| **Search** | Exam name |
| **Row Actions** | View Details · Edit · Cancel · Resolve Conflict · Publish to Branches |
| **Drawer: exam-schedule-create** | 680px · Tabs: Identity (name/type/stream/class) · Date & Time · Branch Scope · Paper Assignment · Notification |
| **Drawer: exam-schedule-edit** | 680px · same tabs · Edit all fields before publication |
| **Drawer: exam-schedule-view** | 560px · Tabs: Overview · Branches · Paper Status · Conflicts · History |
| **Modal: cancel-confirm** | Confirm + mandatory cancellation reason (audited) + select notification channel |
| **Conflict badge** | Red badge on any exam row with ≥ 1 conflict |
| **Charts** | Exam density per month (bar) · Branch load over calendar year |
| **Role visibility** | CAO: Full create/edit/publish/cancel · Exam Controller: Full · Results Coord: View · Stream Coords: View own stream · Calendar Mgr: View + coordinate · MIS: Read-only |

**23 — Question Bank** `/group/acad/question-bank/`
> Group-level MCQ and subjective question repository. 10,000–50,000 questions.

| Element | Spec |
|---|---|
| **Table** | Columns: Q# · Subject · Topic · Subtopic · Type (MCQ/Short/Long/Numerical) · Difficulty (1–5) · Bloom Level · Last Used · Status · Actions |
| **Filters** | Subject · Topic · Difficulty · Type · Bloom Level (Remember/Understand/Apply/Analyse) · Status (Active/Review/Retired) · Last used date |
| **Search** | Question text partial match (full-text) |
| **Pagination** | Server-side, 25/page |
| **Row Actions** | Preview · Edit · Clone · Retire · Add to Paper |
| **Drawer: question-create** | 680px · Tabs: Question Text (rich text + LaTeX) · Options (MCQ: 4 options + correct) · Explanation · Classification (subject/topic/difficulty/bloom) · Tags |
| **Drawer: question-edit** | 680px · same structure |
| **Drawer: question-preview** | 480px · Renders exactly as student sees it including LaTeX |
| **Bulk import** | XLSX template (question, options A–D, answer, difficulty, topic) + upload with row-level error report |
| **Bulk actions** | Retire selected · Move to subject · Tag selected |
| **Charts** | Questions per subject (bar) · Difficulty distribution (donut) · Questions added per month (line) |
| **Role visibility** | CAO: Full · Exam Controller: Full CRUD · Stream Coords: Create/edit for own stream · Curriculum Coord: Create · Others: No access |
| **LaTeX support** | Inline LaTeX rendering for maths/science questions |
| **Empty state** | Per-stream: "No questions yet for [Subject]. Add your first question." + Create CTA |

**24 — Exam Paper Builder** `/group/acad/exam-papers/`
> Build and finalise central question papers from question bank. Version-controlled.

| Element | Spec |
|---|---|
| **Table** | Columns: Paper ID · Exam Name · Stream · Class · Subject · Total Q · Total Marks · Duration · Status · Created By · Created At · Actions |
| **Filters** | Exam Name · Stream · Class · Status (Draft/Pending Approval/Approved/Published/Archived) · Date range |
| **Search** | Paper name, exam name |
| **Row Actions** | Open Builder · View Preview · Submit for Approval · Publish Answer Key · Archive · Clone |
| **Drawer/Full-page: paper-builder** | Full-page builder: Left panel (question bank browse + filter) · Right panel (paper structure + questions added) · Section management (Section A/B/C) · Mark allocation per question · Shuffle toggle · Print preview |
| **Drawer: paper-view** | 640px · Tabs: Paper Preview (student view) · Structure Summary · Approval History |
| **Modal: submit-for-approval** | Confirm checklist: answer key attached? · total marks match? · duration set? |
| **Modal: publish-confirm** | Confirm paper publish — triggers branch notification |
| **Charts** | Difficulty distribution of selected questions (donut — auto-updates as questions added) · Bloom level coverage (radar) |
| **Version history** | Every save creates a version — can diff any two versions |
| **Role visibility** | Exam Controller: Full build + submit + publish · CAO: Approve/reject · Stream Coords: Create draft for own stream, submit to Exam Controller · Others: No access |

**25 — Branch Exam Schedule** `/group/acad/branch-exam-schedule/`
> Per-branch view of all exams. Branches confirm readiness. Group monitors status.

| Element | Spec |
|---|---|
| **Table** | Columns: Branch · Exam Name · Date · Time · Venue · Invigilator Assigned · Students Expected · Hall Tickets Generated · Readiness Status · Actions |
| **Filters** | Branch · Exam Name · Date · Readiness Status (Confirmed/Pending/At Risk) |
| **Search** | Exam name, branch name |
| **Row Actions** | View Branch Detail · Send Reminder · Mark Override (CAO only) |
| **Bulk action** | Send readiness reminder to all Pending branches |
| **Drawer: branch-exam-detail** | 560px · Tabs: Setup · Invigilators · Hall Tickets · Venue · Issues |
| **Status badge logic** | Confirmed = all fields set + branch acknowledged · Pending = not yet confirmed · At Risk = < 24 hrs and still Pending |
| **Auto-alert** | Email/WhatsApp trigger to branch principal if Pending 48 hrs before exam |
| **Role visibility** | CAO/Exam Controller: Full view + override · Results Coord: View · Calendar Mgr: View |

**26 — Exam Conflict Monitor** `/group/acad/exam-conflicts/`
> Automated detection of overlapping exams across branches. Zero scheduling conflicts allowed.

| Element | Spec |
|---|---|
| **Conflict list** | Grouped by conflict type: Same branch same date/time · Same stream same date (different branches—allowed) · Same class + branch overlapping window |
| **Table** | Columns: Conflict ID · Type · Exams Involved · Branches · Date · Severity (Hard/Soft) · Status · Actions |
| **Filters** | Conflict Type · Severity · Status (Open/Resolved/Ignored with reason) · Date range |
| **Drawer: conflict-detail** | 560px · Tabs: Affected Exams · Timeline · Proposed Resolution · Action |
| **Actions** | Reschedule Exam A · Reschedule Exam B · Merge · Ignore (reason required) |
| **Auto-detect** | Runs on every exam schedule create/edit — results shown within 2 seconds |
| **Alert badge** | Header banner if unresolved hard conflicts exist — persists across all acad pages |
| **Role visibility** | CAO: Full resolve · Exam Controller: Full · Calendar Mgr: View + propose resolution |

**27 — Result Moderation** `/group/acad/result-moderation/`
> Branch uploads raw marks → group moderates → group approves → results published to students.

| Element | Spec |
|---|---|
| **Table** | Columns: Exam · Branch · Stream · Class · Marks Uploaded · Upload Date · Moderator · Status · Actions |
| **Filters** | Exam Name · Branch · Stream · Status (Awaiting Upload / Uploaded / Under Moderation / Approved / Published / Rejected) |
| **Search** | Exam name, branch |
| **Row Actions** | Download Raw Marks · Open Moderation View · Approve · Reject with Reason · Request Re-upload |
| **Drawer: moderation-view** | 680px · Tabs: Raw Marks Table · Statistical Checks (mean/median/SD · Z-score outliers) · Moderation Adjustments · Approval |
| **Statistical checks** | Auto-flag: avg < 25% (possible error) · SD > 30 (unusual spread) · Missing roll numbers · Marks > max marks |
| **Bulk approve** | "Approve all branches for this exam" if all pass statistical checks |
| **Drawer: reject-reason** | 480px · Required rejection reason · Notify branch principal checkbox |
| **Charts** | Marks distribution histogram per branch (rendered inside drawer) |
| **Role visibility** | CAO: Full approve/override · Exam Controller: Full moderation · Results Coord: Approve + publish · Stream Coords: View own stream · MIS: Read-only |

**28 — Mark Scheme & Answer Keys** `/group/acad/answer-keys/`
> Central answer key management. Published after exam ends — not before.

| Element | Spec |
|---|---|
| **Table** | Columns: Exam Name · Paper ID · Stream · Subject · Key Status · Published At · Challenge Window · Challenges · Actions |
| **Filters** | Exam Name · Stream · Subject · Status (Not Uploaded / Uploaded / Published / Challenge Open / Finalized) |
| **Row Actions** | Upload Key · Preview · Publish · Open Challenge Window · View Challenges · Finalize |
| **Drawer: key-upload** | 480px · File upload (PDF) + Q-by-Q answer entry (MCQ: A/B/C/D, Numerical: value, range) |
| **Drawer: challenge-list** | 560px · Student challenges table: Q# · Student claim · Branch · Status (Open/Reviewed/Accepted/Rejected) |
| **Drawer: challenge-review** | 480px · Question text · Official answer · Student claim · Reviewer decision + reason |
| **Role visibility** | Exam Controller: Upload + publish · CAO: Finalize after challenges · Stream Coords: View own stream · Others: No access |

---

## Section 4 — Results & Rankings

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 29 | Cross-Branch Results Publisher | `/group/acad/results/` | `29-cross-branch-results-publisher.md` | P0 | ⬜ |
| 30 | Group Rank Computation | `/group/acad/rankings/` | `30-group-rank-computation.md` | P0 | ⬜ |
| 31 | Topper Lists & Leaderboard | `/group/acad/toppers/` | `31-topper-lists-leaderboard.md` | P1 | ⬜ |
| 32 | Subject Performance Heatmap | `/group/acad/subject-performance/` | `32-subject-performance-heatmap.md` | P1 | ⬜ |
| 33 | Branch Result Comparison | `/group/acad/branch-results/` | `33-branch-result-comparison.md` | P1 | ⬜ |
| 34 | Result Archive | `/group/acad/results/archive/` | `34-result-archive.md` | P2 | ⬜ |

### Page Specs — Section 4

**29 — Cross-Branch Results Publisher** `/group/acad/results/`
> The publication control room. Governs what gets published, to whom, and when.

| Element | Spec |
|---|---|
| **Table** | Columns: Exam · Stream · Class · Branches Uploaded · Moderation Status · Rank Computed · Publication Status · Published At · Actions |
| **Filters** | Exam · Stream · Status · Date |
| **Row Actions** | Trigger Rank Computation · Preview Results · Publish to Students · Publish to Parents · Unpublish (reason required) |
| **Drawer: publish-detail** | 640px · Tabs: Summary Stats · Per-Branch Status · Rank Distribution · Publish Channels (student portal / parent SMS / WhatsApp) |
| **Modal: publish-confirm** | Checklist: all branches uploaded · moderation approved · rank computed · answer key finalized |
| **Audit trail** | Every publish/unpublish action logged with actor and timestamp — immutable |
| **Role visibility** | CAO: Full override · Results Coordinator: Publish/Unpublish · Exam Controller: View · MIS: Read-only |

**30 — Group Rank Computation** `/group/acad/rankings/`
> Compute and validate All-Group ranks after all branches upload marks.

| Element | Spec |
|---|---|
| **Computation trigger** | "Compute Rankings" button — disabled until all branches have uploaded + moderated |
| **Status table** | Branch · Marks Uploaded · Moderated · Students Count · Included in Computation |
| **Computation results** | Table: Roll No · Student Name · Branch · Stream · Subject marks · Total · Percentile · Group Rank |
| **Filters** | Stream · Class · Branch · Rank range |
| **Export** | XLSX with all computation details |
| **Re-computation** | Allowed if a branch re-uploads corrected marks (reason + audit log required) |
| **Drawer: student-rank-detail** | 480px · All subject marks · Group rank · Branch rank · Percentile · AIR estimate (if JEE/NEET) |
| **Charts** | Score distribution bell curve · Percentile bands (P10/P25/P50/P75/P90) |
| **Role visibility** | Results Coordinator: Full · CAO: Override · Exam Controller: Trigger only · MIS: Read after compute |

**31 — Topper Lists & Leaderboard** `/group/acad/toppers/`
> Official topper records — input for marketing, scholarships, and press releases.

| Element | Spec |
|---|---|
| **Leaderboard tabs** | Group Overall · Per Stream · Per Subject · Per Branch · Per Class |
| **Table** | Rank · Roll No · Student Name · Branch · Class · Stream · Score · Percentile · Photo (if uploaded) · Actions |
| **Filters** | Exam · Stream · Class · Branch · Rank range (Top 10 / Top 50 / Top 100 / Custom) |
| **Drawer: topper-profile** | 480px · All exam history ranks · Current rank · Contact (branch admin sees) · Scholarship eligibility |
| **Actions** | Nominate for Scholarship · Send to Marketing (triggers Div-O flow) · Export Certificate Data |
| **Export** | PDF topper list (formatted for notice board / WhatsApp broadcast) · XLSX for admin |
| **Historical view** | Previous exams/terms topper comparison — who was consistent |
| **Role visibility** | CAO/Results Coord: Full + nominate · Marketing (Div-O): Read-only export · MIS: Read-only |

**32 — Subject Performance Heatmap** `/group/acad/subject-performance/`
> Topic-level performance gaps visible across all branches simultaneously.

| Element | Spec |
|---|---|
| **Heatmap view** | X-axis: Topics (within selected subject) · Y-axis: Branches · Cell: Avg marks % — Red < 50%, Amber 50–70%, Green > 70% |
| **Filters** | Exam · Stream · Subject · Class · Branch (multi-select) |
| **Drill-down** | Click cell → drawer showing branch+topic detail: question-level performance |
| **Drawer: topic-branch-drill** | 480px · Questions from this topic in exam · Avg marks · Most wrong option · Difficulty vs result correlation |
| **Export** | PNG heatmap · XLSX raw data per cell |
| **Charts** | Pass rate trend per subject (line, 6 terms) |
| **Role visibility** | CAO: Full · Academic Dir: Full · Stream Coords: Own stream only · Exam Controller: Full · MIS: Read-only |

**33 — Branch Result Comparison** `/group/acad/branch-results/`
> Side-by-side comparison of any two to five branches on a selected exam.

| Element | Spec |
|---|---|
| **Branch selector** | Multi-select up to 5 branches |
| **Comparison table** | Metric rows: Avg score · Pass % · Top 10% count · Fail count · Dropout before exam · Attendance day-of |
| **Per-subject comparison** | Grouped bar chart — each subject, branches side by side |
| **Score distribution overlay** | Line chart — kernel density estimate per branch on same axis |
| **Export** | PDF comparison report (board-ready format) |
| **Filters** | Exam · Stream · Class · Subject |
| **Role visibility** | CAO: Full · Academic Dir: Full · Stream Coords: Own stream · Results Coord: Full · MIS: Read-only |

**34 — Result Archive** `/group/acad/results/archive/`
> Immutable historical result store. Past exams + ranks + published results — never deletable.

| Element | Spec |
|---|---|
| **Table** | Exam · Year · Term · Stream · Class · Branches · Published Date · Download |
| **Filters** | Academic Year · Exam Type · Stream · Class |
| **Row Actions** | View Summary · Download Full Results (XLSX) · Download Rank List (PDF) |
| **Access** | Read-only for all roles — no edit or delete controls shown to anyone |
| **Retention** | Configurable — default 10 years |
| **Role visibility** | All Div-B roles: Read-only |

---

## Section 5 — JEE/NEET Integration

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 35 | JEE/NEET Test Series Manager | `/group/acad/jee-neet/test-series/` | `35-jee-neet-test-series.md` | P1 | ⬜ |
| 36 | Integrated Coaching Schedule | `/group/acad/jee-neet/schedule/` | `36-integrated-coaching-schedule.md` | P1 | ⬜ |
| 37 | JEE/NEET Performance Tracker | `/group/acad/jee-neet/performance/` | `37-jee-neet-performance.md` | P1 | ⬜ |
| 38 | JEE/NEET NTA Syllabus Coverage | `/group/acad/jee-neet/syllabus-coverage/` | `38-jee-neet-syllabus-coverage.md` | P2 | ⬜ |

### Page Specs — Section 5

**35 — JEE/NEET Test Series Manager** `/group/acad/jee-neet/test-series/`
> Manages the full mock test series cycle — from paper creation to result publication.

| Element | Spec |
|---|---|
| **Table** | Columns: Test # · Type (JEE/NEET/Both) · Date · Total Q · Total Marks · Duration · Branch Scope · Status · Actions |
| **Filters** | Type · Status · Date range · Branch |
| **Row Actions** | View Paper · Results · Performance Analysis · Mark as Official |
| **Drawer: test-create** | 640px · Tabs: Test Identity · Paper (link to exam paper builder) · Branch scope · Schedule · Notification |
| **Drawer: test-result** | 560px · Per-student percentile · AIR estimate · Subject-wise breakdown |
| **Charts** | Score trend across all mocks (line — group avg) · AIR prediction band over series |
| **Role visibility** | JEE/NEET Head: Full · CAO: View + approve · Exam Controller: Paper assignment · Results Coord: Publish |

**36 — Integrated Coaching Schedule** `/group/acad/jee-neet/schedule/`
> Timetable where JEE/NEET coaching periods overlap with regular college timetable.

| Element | Spec |
|---|---|
| **Weekly timetable grid** | Branch selector → shows day × period grid · Coaching slots highlighted in blue · Regular class in grey · Conflicts in red |
| **Conflict detection** | Auto-detect: coaching period overlapping a mandatory regular period |
| **Drawer: slot-create** | 480px · Day · Period · Subject · Faculty · Branch · Week range · Type (Coaching/Regular/Both) |
| **Drawer: conflict-resolve** | 480px · Shows overlapping slots · Options: shift coaching slot · notify faculty |
| **Filters** | Branch · Week · Subject |
| **Role visibility** | JEE/NEET Head: Full · CAO: View · Stream Coord MPC/BiPC: View |

**37 — JEE/NEET Performance Tracker** `/group/acad/jee-neet/performance/`
> Per-student tracking across the full test series.

| Element | Spec |
|---|---|
| **Table** | Student · Branch · Class · Total Tests · Avg Score · Latest Percentile · AIR Estimate · Improvement Trend · Actions |
| **Filters** | Branch · Class · Percentile band · Improvement trend (Improving/Stable/Declining) |
| **Search** | Student name / roll number |
| **Drawer: student-detail** | 560px · Tabs: All Tests History · Subject-wise · Weak Topics · AIR Trend chart |
| **Charts** | Group percentile trend (line) · Subject radar (Phy/Chem/Math or Bio) per student |
| **Alerts** | Flag students showing declining trend for 3+ consecutive tests |
| **Role visibility** | JEE/NEET Head: Full · CAO: View · Academic Dir: View · Branch sees own students only (via branch portal) |

**38 — JEE/NEET NTA Syllabus Coverage** `/group/acad/jee-neet/syllabus-coverage/`
> Maps group curriculum to official NTA JEE/NEET syllabus. Shows uncovered topics.

| Element | Spec |
|---|---|
| **Coverage matrix** | NTA topic list vs group syllabus — Covered / Partially / Not covered |
| **Filters** | Subject (Physics/Chemistry/Maths/Biology) · Coverage status |
| **Bulk assign** | Mark multiple topics as covered — links to content library resource |
| **Export** | Gap report PDF |
| **Role visibility** | JEE/NEET Head: Full · CAO/Curriculum Coord: Edit |

---

## Section 6 — IIT Foundation

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 39 | IIT Foundation Program Manager | `/group/acad/iit-foundation/program/` | `39-foundation-program-manager.md` | P1 | ⬜ |
| 40 | Foundation Test Series | `/group/acad/iit-foundation/tests/` | `40-foundation-test-series.md` | P1 | ⬜ |
| 41 | Foundation Performance Tracker | `/group/acad/iit-foundation/performance/` | `41-foundation-performance.md` | P2 | ⬜ |

### Page Specs — Section 6

**39 — IIT Foundation Program Manager** `/group/acad/iit-foundation/program/`
> Manages the Class 6–10 IIT Foundation curriculum, batches, and faculty.

| Element | Spec |
|---|---|
| **Class tabs** | Class 6 · 7 · 8 · 9 · 10 — each with subject breakdown |
| **Content table** | Subject · Topics Covered · Study Material · Test Count · Enrolled Students · Status |
| **Drawer: class-config** | 560px · Subjects offered · Hours per week · Faculty assignment · Branch scope |
| **Batch management** | Table: Batch · Branch · Class · Students · Faculty · Schedule |
| **Role visibility** | IIT Foundation Director: Full · CAO: View · Curriculum Coord: Upload content |

**40 — Foundation Test Series** `/group/acad/iit-foundation/tests/`
> Test series specifically for Foundation classes — separate from main exam pipeline.

| Element | Spec |
|---|---|
| **Table** | Test # · Class · Subject · Date · Status · Branch Scope · Results Published |
| **Same structure as JEE/NEET test series** but filtered to Classes 6–10 |
| **Drawer: foundation-test-create** | 640px · Class · Subjects · Paper · Branch · Schedule |
| **Role visibility** | IIT Foundation Director: Full · Exam Controller: Paper |

**41 — Foundation Performance Tracker** `/group/acad/iit-foundation/performance/`
> Per-student performance tracking across foundation test series.

| Element | Spec |
|---|---|
| **Table** | Student · Class · Branch · Tests Taken · Avg Score · Improvement · Actions |
| **Scholarship eligibility auto-flag** | Students scoring in top 10% over 3+ tests flagged for scholarship nomination |
| **Drawer: student-detail** | 480px · Test history · Subject breakdown · Trend chart |
| **Role visibility** | IIT Foundation Director: Full · CAO: View · MIS: Read-only |

---

## Section 7 — Olympiad & Scholarships

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 42 | Olympiad Exam Registry | `/group/acad/olympiad/exams/` | `42-olympiad-exam-registry.md` | P1 | ⬜ |
| 43 | Olympiad Registration Manager | `/group/acad/olympiad/registrations/` | `43-olympiad-registrations.md` | P1 | ⬜ |
| 44 | Olympiad Results & Awards | `/group/acad/olympiad/results/` | `44-olympiad-results-awards.md` | P1 | ⬜ |
| 45 | Scholarship Exam Manager | `/group/acad/olympiad/scholarship-exams/` | `45-scholarship-exam-manager.md` | P1 | ⬜ |

### Page Specs — Section 7

**42 — Olympiad Exam Registry** `/group/acad/olympiad/exams/`
> Master list of all external olympiad and competitive exams the group participates in.

| Element | Spec |
|---|---|
| **Table** | Exam Name · Body (NCERT/HRD/Private) · Eligible Classes · Eligible Streams · Registration Deadline · Exam Date · Fee · Status (Active/Closed/Results Out) |
| **Filters** | Body · Class · Exam Status · Year |
| **Drawer: olympiad-add** | 480px · Fields: Name, body, eligible classes/streams, reg deadline, exam date, fee per student, result expected date, official site |
| **Reminder automation** | Set reminder N days before registration deadline → auto-notification to coordinators |
| **Role visibility** | Olympiad Coordinator: Full · CAO: View · Others: No access |

**43 — Olympiad Registration Manager** `/group/acad/olympiad/registrations/`
> Track student registrations per olympiad per branch. Centrally coordinated.

| Element | Spec |
|---|---|
| **Table** | Olympiad · Branch · Class · Eligible Students · Registered · Registration Form Submitted · Fee Paid · Hall Ticket · Actions |
| **Filters** | Olympiad · Branch · Class · Registration Status |
| **Drill-down** | Click branch row → student-level registration list |
| **Drawer: student-registration-list** | 560px · Student · Roll · Class · Registered Y/N · Fee Y/N · Hall Ticket Y/N |
| **Bulk actions** | Remind branches to complete registration · Download registration report |
| **Export** | Branch-wise registration XLSX for submitting to exam body |
| **Role visibility** | Olympiad Coordinator: Full · CAO: View · MIS: Read-only |

**44 — Olympiad Results & Awards** `/group/acad/olympiad/results/`
> Record and celebrate olympiad results — feeds into topper lists and scholarship nominations.

| Element | Spec |
|---|---|
| **Table** | Olympiad · Branch · Student · Class · Score · Rank (State/National) · Medal/Award · Scholarship Nominated Y/N |
| **Filters** | Olympiad · Branch · Class · Award Level (Gold/Silver/Bronze/Merit/Qualifier) |
| **Drawer: result-entry** | 480px · Student lookup · Olympiad · Score · Rank type · Award level · Certificate upload |
| **Bulk import** | XLSX import of results when official scorecards arrive |
| **Highlight wall** | Visual medal wall — top performers with photo, name, olympiad, award |
| **Actions** | Nominate for Scholarship · Send to Marketing (Div-O press release flow) |
| **Charts** | Medals per olympiad (bar) · Branch performance comparison |
| **Role visibility** | Olympiad Coordinator: Full · CAO: View + nominate · Marketing/Div-O: Read-only export |

**45 — Scholarship Exam Manager** `/group/acad/olympiad/scholarship-exams/`
> Internal group-run scholarship entrance exams (separate from external olympiads).

| Element | Spec |
|---|---|
| **Kanban pipeline** | Announced → Registration Open → Exam Scheduled → Results Published → Awards Given |
| **Table** | Scholarship Exam · Type (Merit/Need/Sport) · Date · Eligible · Registered · Appeared · Results · Awarded |
| **Drawer: scholarship-exam-create** | 640px · Tabs: Identity · Eligibility Criteria · Registration Window · Exam Paper · Award Structure |
| **Drawer: award-list** | 480px · Awardees with award amount, duration, conditions |
| **Modal: award-revoke-confirm** | Confirm + reason (e.g. student left institution) |
| **Integration** | Links to Div-C (Group Scholarship Manager) for disbursement |
| **Role visibility** | Olympiad Coordinator: Full · CAO: Approve · Results Coord: Publish results · Finance Div-D: View disbursement data |

---

## Section 8 — Special Education

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 46 | Special Needs Student Registry | `/group/acad/special-ed/students/` | `46-special-needs-registry.md` | P1 | ⬜ |
| 47 | IEP Manager | `/group/acad/special-ed/iep/` | `47-iep-manager.md` | P1 | ⬜ |
| 48 | Accommodation Request Tracker | `/group/acad/special-ed/accommodations/` | `48-accommodation-tracker.md` | P1 | ⬜ |
| 49 | Special Ed Progress Reports | `/group/acad/special-ed/reports/` | `49-special-ed-reports.md` | P2 | ⬜ |

### Page Specs — Section 8

**46 — Special Needs Student Registry** `/group/acad/special-ed/students/`
> Centralised cross-branch registry of all special needs students. DPDP Act 2023 sensitive data — strict access control.

| Element | Spec |
|---|---|
| **Table** | Student ID · Name (masked for G1/G2) · Branch · Class · Disability Type · IEP Status · Last Review · Support Staff Assigned |
| **Filters** | Branch · Disability Type · IEP Status (Active/Review Due/Inactive) · Class |
| **Search** | Student ID only for G1/G2 — name search only for G3+ |
| **Drawer: student-add** | 640px · Tabs: Identity · Disability Details (type, severity, medical cert) · Support Needs · Initial Accommodations · Guardian Contact |
| **Drawer: student-view** | 560px · Tabs: Profile · IEP · Accommodations · Progress · Incident History |
| **Data masking** | Name/contact visible only to Special Ed Coord (G3) and CAO (G4) — MIS officer sees anonymized stats |
| **DPDP notice** | Consent banner on drawer open: "Accessing sensitive student data — access is logged." |
| **Role visibility** | Special Ed Coordinator: Full · CAO: View · Academic Dir: View summary · MIS: Anonymized count/stats only |

**47 — IEP Manager** `/group/acad/special-ed/iep/`
> Individual Education Plan lifecycle: create → review → update → close.

| Element | Spec |
|---|---|
| **Table** | IEP ID · Student · Branch · Class · Created Date · Last Review · Next Review Due · Goals Met % · Status (Active/Review Due/Completed/Discontinued) |
| **Filters** | Branch · Status · Review Due (Overdue / Due this month / Upcoming) |
| **Overdue badge** | Red badge count in nav if any IEPs overdue |
| **Drawer: iep-create** | 680px · Tabs: Student Link · Learning Goals (add/edit goals with measurable targets) · Teaching Strategies · Support Hours · Assessment Accommodations · Review Schedule · Sign-off |
| **Drawer: iep-review** | 640px · Tabs: Progress on Each Goal · Updated Strategies · Review Notes · Next Review Date · Approve |
| **Drawer: iep-view** | 560px · Full plan read-only with version history |
| **Auto-reminder** | Email to Special Ed Coord + branch counsellor when IEP review is due in 14 days |
| **Export** | IEP PDF — formatted for sharing with parents (redacts internal notes) |
| **Role visibility** | Special Ed Coordinator: Full · CAO: View + sign-off · Academic Dir: View · Branch counsellor: View own branch IEPs (via branch portal) |

**48 — Accommodation Request Tracker** `/group/acad/special-ed/accommodations/`
> Branch submits accommodation needs for special students in upcoming exams. Group approves and coordinates with Exam Controller.

| Element | Spec |
|---|---|
| **Table** | Request ID · Student · Branch · Exam · Accommodation Type · Requested By · Status · Actions |
| **Accommodation types** | Extra time (30/60 min) · Scribe · Separate room · Large font paper · Oral exam · Reader |
| **Filters** | Branch · Exam · Status (Pending / Approved / Implemented / Denied) · Accommodation Type |
| **Drawer: accommodation-request-view** | 480px · Student disability details · Requested accommodation · Supporting medical doc · Decision + reason |
| **Actions** | Approve · Deny (reason required) · Partially approve (e.g. approve extra time, deny scribe) |
| **Integration** | Approved accommodations auto-flag in Branch Exam Schedule (page 25) for the relevant exam |
| **Role visibility** | Special Ed Coordinator: Full · Exam Controller: View approved accommodations · CAO: Override |

**49 — Special Ed Progress Reports** `/group/acad/special-ed/reports/`
> Aggregated progress reporting for NCPCR compliance, parent meetings, and board reporting.

| Element | Spec |
|---|---|
| **Report types** | Branch summary · IEP goal achievement · Accommodation usage · Incident log |
| **Table** | Report Type · Branch · Term · Generated At · Download |
| **Filters** | Report type · Branch · Term · Year |
| **Generate report** | Select type + branch + date range → renders inline preview → download PDF/XLSX |
| **Auto-reports** | Quarterly NCPCR-format report auto-generated and stored |
| **Role visibility** | Special Ed Coordinator: Generate + download · CAO: Download · MIS: Download |

---

## Section 9 — Teacher Performance & CPD

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 50 | Teacher Performance Tracker | `/group/acad/teacher-performance/` | `50-teacher-performance-tracker.md` | P1 | ⬜ |
| 51 | Classroom Observation Log | `/group/acad/teacher-observations/` | `51-classroom-observation-log.md` | P1 | ⬜ |
| 52 | CPD Tracker | `/group/acad/cpd/` | `52-cpd-tracker.md` | P1 | ⬜ |
| 53 | Teaching Load Monitor | `/group/acad/teacher-load/` | `53-teaching-load-monitor.md` | P2 | ⬜ |

### Page Specs — Section 9

**50 — Teacher Performance Tracker** `/group/acad/teacher-performance/`
> Group-wide teacher appraisal across all branches — feeds into Div-E (HR) for annual review.

| Element | Spec |
|---|---|
| **Table** | Teacher ID · Name · Branch · Subject · Stream · Student Result Avg (their classes) · Attendance % · Lesson Plan Compliance % · Observation Rating (1–5) · Composite Score · Status |
| **Filters** | Branch · Subject · Stream · Score band · Status (Active/On Leave/Transferred/Exited) |
| **Search** | Teacher name / ID |
| **Pagination** | Server-side, 25/page |
| **Drawer: teacher-profile** | 560px · Tabs: Personal · Performance History (per term) · Observations · CPD · Appraisal |
| **Drawer: appraisal-create** | 640px · Tabs: Results Score · Attendance Score · Lesson Plan Score · Peer Review · Composite + Recommendation (Promote / Hold / PIP / Transfer) |
| **Charts** | Score distribution by branch (box plot) · Subject-wise average score |
| **Integration** | Recommendation syncs to Div-E Group Performance Review Officer |
| **Role visibility** | Academic Director: Full · CAO: View + override recommendation · Stream Coords: View own stream teachers · MIS: Read-only anonymised summary |

**51 — Classroom Observation Log** `/group/acad/teacher-observations/`
> Structured observation records from branch-level academic observers and group-level inspectors.

| Element | Spec |
|---|---|
| **Table** | Observation ID · Teacher · Branch · Subject · Class · Observer · Date · Rating · Strengths · Areas for Improvement · Follow-up Due |
| **Filters** | Branch · Subject · Rating band · Observer type (Group/Branch) · Date range |
| **Search** | Teacher name |
| **Drawer: observation-create** | 640px · Teacher lookup · Subject · Class observed · Date · Rubric (10 criteria × 1–5 rating) · Strengths (text) · Improvements (text) · Follow-up plan · Share with teacher Y/N |
| **Drawer: observation-view** | 560px · Full rubric scores + comments · Teacher acknowledgement status |
| **Rubric criteria** | Subject knowledge · Lesson structure · Student engagement · Questioning technique · Assessment for learning · Classroom management · Differentiation · Use of materials · Time management · Professional conduct |
| **Role visibility** | Academic Director: Full · Group Inspection Officer (Div-P): Create · CAO: View · Stream Coords: View own stream · Teachers: View own observations only (via branch portal) |

**52 — CPD Tracker** `/group/acad/cpd/`
> Continuous Professional Development — mandatory hours tracking and training records.

| Element | Spec |
|---|---|
| **Table** | Teacher · Branch · Subject · CPD Hours Completed · CPD Hours Required · % Complete · Last Training · Status (On Track / At Risk / Overdue) |
| **Filters** | Branch · Subject · Status · Academic Year |
| **Search** | Teacher name |
| **Drawer: cpd-record-add** | 480px · Teacher lookup · Training name · Provider · Date · Hours · Type (Online/Offline/Workshop/Certification) · Certificate upload |
| **Drawer: teacher-cpd-history** | 480px · All CPD records chronological · Total hours · Certificate downloads |
| **Bulk action** | Send reminder to all "At Risk" teachers |
| **Integration** | CPD completion feeds into Teacher Performance composite score (page 50) |
| **Charts** | Completion rate by branch (bar) · Hours by training type (donut) |
| **Role visibility** | Academic Director: Full · Training & Development Mgr (Div-E): Full · CAO: View · MIS: Read-only |

**53 — Teaching Load Monitor** `/group/acad/teacher-load/`
> Periods per week per teacher — detects overload and underload across all branches.

| Element | Spec |
|---|---|
| **Table** | Teacher · Branch · Subject · Periods/Week · Students per Class · Sections Covered · Total Students · Load Status (Overloaded / Normal / Underloaded) |
| **Filters** | Branch · Subject · Load Status · Stream |
| **Thresholds** | Configurable by CAO: normal range 18–28 periods/week; overloaded > 32; underloaded < 12 |
| **Alert** | Branches with > 20% teachers overloaded flagged in CAO dashboard |
| **Drawer: teacher-load-detail** | 480px · Period-by-period weekly timetable (read from branch portal data) |
| **Role visibility** | Academic Director: Full · CAO: View · Stream Coords: Own stream |

---

## Section 10 — Academic MIS & Analytics

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 54 | Group Academic MIS Report | `/group/acad/mis/report/` | `54-academic-mis-report.md` | P0 | ⬜ |
| 55 | Branch Academic Health Dashboard | `/group/acad/branch-health/` | `55-branch-academic-health.md` | P1 | ⬜ |
| 56 | Dropout Signal Monitor | `/group/acad/dropout-signals/` | `56-dropout-signal-monitor.md` | P1 | ⬜ |
| 57 | Attendance vs Performance Correlator | `/group/acad/attendance-performance/` | `57-attendance-performance-correlator.md` | P2 | ⬜ |
| 58 | Academic Trend Analytics | `/group/acad/trends/` | `58-academic-trend-analytics.md` | P2 | ⬜ |

### Page Specs — Section 10

**54 — Group Academic MIS Report** `/group/acad/mis/report/`
> Monthly MIS — the standard report sent to Chairman/Board. Also on-demand for any date range.

| Element | Spec |
|---|---|
| **Report builder** | Select: Report type (Monthly/Term/Annual/Custom) · Date range · Scope (Group / Zone / Branch) · Sections to include |
| **Sections** | Attendance summary · Exam results · Curriculum completion · Teacher performance · Dropout count · Olympiad outcomes · Special needs summary |
| **Preview** | Inline HTML preview before download |
| **Export** | PDF (A4, branded letterhead) · XLSX |
| **Scheduled reports** | Set recurring: Monthly → auto-email to CAO + Chairman |
| **Drawer: report-schedule** | 480px · Frequency · Recipients · Format · Next run date |
| **Report history table** | Past reports — date, scope, download link |
| **Role visibility** | MIS Officer: Full generate + schedule · CAO: View + approve distribution · Academic Dir: Generate · All G4+: Download |

**55 — Branch Academic Health Dashboard** `/group/acad/branch-health/`
> Composite health score per branch — early warning system.

| Element | Spec |
|---|---|
| **Table** | Branch · Health Score (0–100) · Attendance % · Result Avg % · Curriculum Completion % · Teacher Rating · Dropout Rate · Trend (↑↓→) |
| **Filters** | Zone · Health Score Band (Critical < 50 / Warning 50–70 / Healthy > 70) · Date range |
| **Health score formula** | Configurable by CAO: weighted average of 5 components |
| **Drawer: branch-health-detail** | 560px · Tabs: Score Breakdown · Historical Trend · Component Drill-downs · Recommended Actions |
| **Charts** | Health score trend (line, 6 terms) · Component radar chart |
| **Alert integration** | Branches in Critical zone auto-escalated to CAO dashboard |
| **Role visibility** | CAO: Full · Academic Dir: Full · Stream Coords: Own stream view · MIS: Full |

**56 — Dropout Signal Monitor** `/group/acad/dropout-signals/`
> Early intervention system — identifies at-risk students before they leave.

| Element | Spec |
|---|---|
| **Algorithm signals** | Attendance < 75% for 2 consecutive weeks · Marks below pass threshold in 2+ subjects · Fee payment overdue 30+ days · No login to student portal in 30 days |
| **Table** | Student · Branch · Class · Signal Count · Signals Triggered · Risk Level (Low/Medium/High) · Counsellor Assigned · Actions |
| **Filters** | Branch · Risk Level · Signal type · Class |
| **Search** | Student name / roll |
| **Drawer: student-risk-detail** | 560px · Tabs: Signal History · Performance Graph · Fee Status · Counsellor Notes · Intervention Log |
| **Actions** | Assign Counsellor · Mark as Resolved · Escalate to Principal |
| **Charts** | Dropout signal count per branch (bar) · Risk level distribution (donut) |
| **Role visibility** | Academic Dir: Full · CAO: View · Special Ed Coord: View own students · MIS: Read-only |

**57 — Attendance vs Performance Correlator** `/group/acad/attendance-performance/`
> Scatter plot and correlation analysis — proves (or disproves) attendance drives results.

| Element | Spec |
|---|---|
| **Scatter chart** | X: Attendance % · Y: Exam score % · One point per student · Colour by branch |
| **Filters** | Branch · Stream · Class · Exam · Date range |
| **Correlation stats** | Pearson r displayed · Regression line overlaid |
| **Branch breakdown** | Same scatter per branch — tab for each branch |
| **Export** | PNG chart + XLSX raw data |
| **Role visibility** | Academic Dir: Full · CAO: View · MIS: Full |

**58 — Academic Trend Analytics** `/group/acad/trends/`
> Long-term trend analysis — 6 terms and beyond. Used by CAO and Strategic Advisor.

| Element | Spec |
|---|---|
| **Metrics tracked** | Avg result % · Attendance % · Dropout rate · CPD completion · Teacher rating · Olympiad medals |
| **Charts** | Line chart per metric across terms · Year-over-year comparison bars |
| **Filters** | Metric · Branch / Zone / Group · Date range |
| **Annotations** | Add events (e.g. "New principal in Branch X" / "COVID disruption") to context the trend |
| **Export** | PDF with all charts + narrative placeholder |
| **Role visibility** | CAO: Full + annotate · Academic Dir: Full · MIS: Full · Strategic Advisor (Div-A): Read-only |

---

## Section 11 — Academic Calendar Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 59 | Group Academic Calendar | `/group/acad/calendar/` | `59-group-academic-calendar.md` | P0 | ⬜ |
| 60 | PTM Schedule Manager | `/group/acad/ptm/` | `60-ptm-schedule-manager.md` | P1 | ⬜ |
| 61 | Holiday & Working Day Manager | `/group/acad/holidays/` | `61-holiday-working-day-manager.md` | P1 | ⬜ |
| 62 | Branch Calendar Compliance | `/group/acad/calendar-compliance/` | `62-branch-calendar-compliance.md` | P1 | ⬜ |

### Page Specs — Section 11

**59 — Group Academic Calendar** `/group/acad/calendar/`
> Master academic calendar — all events across all branches. Branches inherit mandatory events.

| Element | Spec |
|---|---|
| **Calendar view** | Month/Week/List toggle · Event types colour-coded: Exam (red) / PTM (blue) / Holiday (grey) / Sports (green) / Cultural (orange) / CPD (purple) |
| **Table view** | Event · Type · Date · Duration · Branch Scope · Mandatory Y/N · Notification Sent Y/N |
| **Filters** | Event Type · Branch · Mandatory/Optional · Month |
| **Row Actions** | Edit · Cancel · Duplicate · Notify Branches |
| **Drawer: calendar-event-create** | 520px · Fields: Name · Type · Date/Time · Duration · Branches (all/zone/specific) · Mandatory Y/N · Notify (email/WhatsApp) |
| **Drawer: event-view** | 480px · Full details + branch confirmation status |
| **Mandatory events lock** | Mandatory events — branch portal cannot delete these |
| **Role visibility** | Calendar Manager: Full create/edit · CAO: Approve mandatory events · Academic Dir: View · All Div-B: View · Branches: View + add local events (non-mandatory) |

**60 — PTM Schedule Manager** `/group/acad/ptm/`
> Parent-Teacher Meeting scheduling across all branches — ensures every branch holds PTMs on schedule.

| Element | Spec |
|---|---|
| **Table** | Branch · PTM Type (Term 1/2/Annual/Emergency) · Scheduled Date · Parent Notification Sent · Attendance % · Report Generated Y/N |
| **Filters** | Branch · PTM Type · Month · Notification Status |
| **Bulk action** | "Schedule PTM for all branches" → generates date-per-branch (respects branch working calendar) · Auto-sends parent notification |
| **Drawer: ptm-create** | 480px · Branch(es) · Date/Time · Type · Agenda · Parent notification channel + template |
| **Drawer: ptm-report** | 480px · Attendance count · Feedback summary · Issues raised |
| **Auto-reminder** | 7 days + 1 day before PTM → WhatsApp/SMS to registered parents |
| **Role visibility** | Calendar Manager: Full · Academic Dir: View · CAO: View · Branches: Report attendance (via branch portal) |

**61 — Holiday & Working Day Manager** `/group/acad/holidays/`
> Official holiday list for the academic year — national + state + local + group-declared.

| Element | Spec |
|---|---|
| **Table** | Date · Day · Holiday Name · Type (National/State/Group/Branch-requested) · Branches · Status |
| **Filters** | Holiday Type · Month · Status (Approved/Pending/Rejected) |
| **Drawer: holiday-add** | 480px · Date · Name · Type · Branch scope · Reason (if local/branch) · Compensatory working day Y/N |
| **Branch holiday requests** | Branch submits → Calendar Manager reviews → Approve/Reject → Approved syncs to branch calendar |
| **Working days counter** | Total working days per branch per term — updated dynamically as holidays are approved |
| **Export** | Annual holiday list PDF (for display on branch notice board) |
| **Role visibility** | Calendar Manager: Full · CAO: Approve national/group holidays · Branches: Request local holidays only (via branch portal) |

**62 — Branch Calendar Compliance** `/group/acad/calendar-compliance/`
> Ensures branches are following the group academic calendar — not diverging on their own.

| Element | Spec |
|---|---|
| **Table** | Branch · Mandatory Events Scheduled Y/N · PTMs Held Y/N · Working Days Count · Deviation Count · Compliance Score |
| **Filters** | Compliance Score band · Zone · Month |
| **Drawer: branch-calendar-detail** | 480px · All events side-by-side: Group Calendar vs Branch Calendar · Deviations highlighted |
| **Auto-alert** | Branch with > 3 deviations triggers alert to Calendar Manager and CAO |
| **Role visibility** | Calendar Manager: Full · CAO: View · Academic Dir: View |

---

## Section 12 — Gap-Fill Additions

> Three genuine functional gaps identified that fall outside the natural home of any single section
> above but are essential to complete academic governance.

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 63 | Academic Standardisation Audit | `/group/acad/standardisation-audit/` | `63-standardisation-audit.md` | P1 | ⬜ |
| 64 | Exam Paper Distribution Pipeline | `/group/acad/paper-distribution/` | `64-paper-distribution.md` | P1 | ⬜ |
| 65 | Academic Policy Manager | `/group/acad/academic-policies/` | `65-academic-policy-manager.md` | P2 | ⬜ |

### Page Specs — Section 12

**63 — Academic Standardisation Audit** `/group/acad/standardisation-audit/`
> Gap: No mechanism existed to verify branches are ACTUALLY following group standards — only to set them.
> This page audits compliance with the group curriculum, lesson plan format, and assessment standards.

| Element | Spec |
|---|---|
| **Audit schedule table** | Branch · Last Audit Date · Auditor · Score · Next Audit Due · Status |
| **Filters** | Branch · Score band · Audit Status |
| **Drawer: audit-create** | 640px · Branch · Auditor · Date · Checklist: Syllabus alignment · Lesson plan format · Assessment type · Student feedback collected |
| **Checklist rubric** | 15 items × Compliant/Partial/Non-compliant — auto-computes score |
| **Corrective action** | Non-compliant items auto-generate action items with due dates + owner (branch principal) |
| **Follow-up tracking** | Action items from previous audits — open/closed status |
| **Charts** | Audit scores trend per branch (line) · Compliance % by criterion (bar) |
| **Role visibility** | Academic Dir: Full · CAO: View + initiate · Inspection Officer (Div-P): Full |

**64 — Exam Paper Distribution Pipeline** `/group/acad/paper-distribution/`
> Gap: Once a paper is approved and ready, there was no secure, tracked delivery workflow to branches.
> This page manages the end-to-end secure distribution of question papers.

| Element | Spec |
|---|---|
| **Pipeline status** | Paper Approved → Distributed to Branch → Branch Acknowledged → Sealed (until exam start) → Released |
| **Table** | Paper ID · Exam · Stream · Branch · Distributed At · Branch Acknowledged At · Sealed Until · Released At · Status |
| **Filters** | Exam · Branch · Status · Date |
| **Security controls** | Paper download only within 24 hrs of exam · One-time download link · Acknowledgement required before download |
| **Drawer: distribution-detail** | 480px · Download log (who, when, IP) · Acknowledgement trail |
| **Alert** | Branch that has NOT acknowledged 12 hrs before exam → red alert to Exam Controller |
| **Role visibility** | Exam Controller: Full · CAO: View · Branch Principal: Acknowledge + download (via branch portal) |

**65 — Academic Policy Manager** `/group/acad/academic-policies/`
> Gap: Academic policies (result policy, re-exam policy, grace marks) were shared informally.
> Version-controlled academic policy management, separate from governance policies (Div-A page 19).

| Element | Spec |
|---|---|
| **Table** | Policy Name · Category (Result/Assessment/Promotion/Re-exam/Scholarship) · Version · Status (Draft/Published/Archived) · Last Updated · Branches Acknowledged |
| **Filters** | Category · Status · Year |
| **Drawer: policy-create** | 640px · Tabs: Content (rich text) · Category · Effective Date · Branch Scope · Acknowledgement Required Y/N |
| **Drawer: policy-view** | 560px · Tabs: Current Version · Version History (diff view) · Branch Acknowledgements |
| **Acknowledgement tracking** | Branch-by-branch acknowledgement status — send reminder to non-acknowledged |
| **Version diff** | Side-by-side diff of any two versions |
| **Export** | PDF for branch notice board / parent handbook inclusion |
| **Role visibility** | CAO: Full create/publish/archive · Academic Dir: Draft + propose · Curriculum Coord: View · All Div-B: View published policies · Branches: Read + acknowledge |

---

## Section 13 — Second Audit Gap-Fill (Pages 66–74)

> Added during second deep audit (2026-03-21). These pages close functional gaps not covered by the initial 65-page set.

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 66 | Stream Coordinator HEC Dashboard | `/group/acad/stream/hec/` | `66-stream-hec-dashboard.md` | P0 | ✅ |
| 67 | Academic Year Setup Wizard | `/group/acad/year-setup/` | `67-academic-year-setup-wizard.md` | P0 | ✅ |
| 68 | Board Exam Tracker | `/group/acad/board-exams/` | `68-board-exam-tracker.md` | P1 | ✅ |
| 69 | Student Academic Profile Viewer | `/group/acad/student-profile/` | `69-student-academic-profile.md` | P1 | ✅ |
| 70 | Teacher Adequacy & Vacancy Monitor | `/group/acad/teacher-vacancies/` | `70-teacher-vacancy-monitor.md` | P1 | ✅ |
| 71 | Result Re-evaluation Request Manager | `/group/acad/reevaluation/` | `71-result-reevaluation-requests.md` | P1 | ✅ |
| 72 | Remedial Programme Manager | `/group/acad/remedial/` | `72-remedial-programme-manager.md` | P1 | ✅ |
| 73 | Inter-Branch Academic Events Manager | `/group/acad/inter-branch-events/` | `73-inter-branch-academic-events.md` | P2 | ✅ |
| 74 | Group Timetable Standards | `/group/acad/timetable-standards/` | `74-group-timetable-standards.md` | P1 | ✅ |

---

**66 — Stream Coordinator HEC Dashboard** `/group/acad/stream/hec/`
> Role: Group Stream Coordinator — HEC (Humanities, Economics, Commerce) · G3 · Large groups only.
> HEC covers streams where core subjects include History/Economics/Civics and/or Commerce/Accounts.
> Identical functional scope to pages 06 (MPC) and 07 (BiPC) but scoped to HEC subjects and branches.

| Widget | Type | Description |
|---|---|---|
| HEC Branches | Count card | Branches offering HEC stream |
| Enrolled Students | Count card | Total HEC-stream students across group |
| Syllabus Coverage | Horizontal bar | % HEC syllabus completed per branch — red < 70% |
| Subject Performance | Heatmap | Branch × HEC subject (Economics, History, Commerce, Civics, Accounts) |
| Toppers in HEC | Table | Top 10 HEC students across group this term |
| Low Performers | Alert list | Students below 40% in any HEC subject |
| Teacher Vacancies | Alert badge | Unfilled HEC subject teacher positions |

| Element | Spec |
|---|---|
| **Role** | G3 — view and manage HEC stream data across all branches |
| **Quick actions** | Upload lesson plan template · Flag branch underperformance · View subject heatmap |
| **Filters** | Branch · Class · Subject · Term |

---

**67 — Academic Year Setup Wizard** `/group/acad/year-setup/`
> Gap: No platform workflow for year-end rollover — done ad-hoc across branches, causing data inconsistency.
> One-time wizard per academic year that configures the new year and promotes students.

| Element | Spec |
|---|---|
| **Access** | CAO G4 (initiate) · Academic Director G3 (review) |
| **Wizard steps** | 1 — Confirm year dates · 2 — Promote students (class-wise, with exceptions) · 3 — Activate new syllabus version · 4 — Reset exam calendar · 5 — Configure fee structure handoff · 6 — Notify branches + confirm |
| **Step 2 — Promotion** | Table: Class → next class · Exception list (detained students) · Rule: minimum marks required for promotion (configurable) |
| **Step 3 — Syllabus** | Confirm new syllabus version per stream/class · Option to clone from previous year with edits |
| **Step 4 — Calendar** | Import mandatory events into new year calendar |
| **Step 5 — Handoff** | Marks the fee module rollover as initiated (branch-level fee setup follows) |
| **Step 6 — Notify** | Sends branch portal notification to all Principals: "AY [year] setup complete — review and confirm your branch" |
| **Branch confirmation** | Branch Principal must confirm receipt — tracked in wizard dashboard |
| **Draft save** | Wizard can be paused and resumed — partial state saved |
| **Guard** | Cannot initiate if previous year still has unresolved result moderation (alert + link) |
| **Role visibility** | CAO: Full initiate + submit · Academic Dir: Review + comment on each step · MIS Officer: Read final confirmation |

---

**68 — Board Exam Tracker** `/group/acad/board-exams/`
> Gap: CBSE/State Board Class 10 and 12 board exam logistics tracked in spreadsheets — no central platform view.
> Covers registration, hall ticket distribution, exam centre coordination, and result entry.

| Element | Spec |
|---|---|
| **Access** | Exam Controller G3 (full) · CAO G4 (view + approve) · Academic Director G3 (view) |
| **Table columns** | Branch · Board · Class (10/12) · Students Appearing · Registration Status · Hall Tickets Distributed · Centre Allotted · Results Entered |
| **Filters** | Board (CBSE/State) · Class · Branch · Stream · Status |
| **Phases** | Registration → Hall Tickets → Exam Day → Result Entry → Mark Verification |
| **Alert types** | Branch missing registration deadline · Hall tickets not distributed 7 days before exam · Result not entered 30 days after exam |
| **Drawer: board-exam-detail** | 640px · Branch · Students list · Board registration numbers · Hall ticket status · Centre info · Result entry |
| **Integration** | Results entered here flow into Result Archive (page 34) with board-exam tag |
| **Charts** | Board pass % by branch · Subject-wise board vs internal exam correlation |
| **Export** | Centre-wise student list (CSV) · Board registration summary (CSV) |

---

**69 — Student Academic Profile Viewer** `/group/acad/student-profile/`
> Gap: No group-level cross-branch view of individual student academic history — only branch portals had this.
> Read-only viewer for group academic roles to audit any student's academic record.

| Element | Spec |
|---|---|
| **Access** | CAO G4 (full) · Academic Director G3 · Exam Controller G3 · Results Coordinator G3 · Stream Coordinators G3 (own-stream students) · MIS G1 (anonymised) |
| **Search** | Search by student name, roll number, or branch |
| **Profile sections** | Identity · Current Enrolment · Subject-wise Marks (all exams, all terms) · Attendance Record · Rank History · Olympiad Entries · IEP flag (if applicable — masked per DPDP) |
| **Marks table** | Exam name · Date · Subject · Max · Scored · % · Branch rank · Group rank |
| **Trend charts** | Subject performance trend across terms · Attendance trend |
| **Drawer: profile-full** | 680px · All sections in tabs: Overview · Marks · Attendance · Events · Flags |
| **DPDP controls** | IEP/Special-needs flag visible only to Special Ed Coordinator and CAO · G1 MIS sees anonymised profile only |
| **Audit log** | Every profile view is logged — visible to CAO and Data Protection Officer |
| **Export** | PDF student academic report (watermarked, one-time link, auto-expires 48 hrs) |

---

**70 — Teacher Adequacy & Vacancy Monitor** `/group/acad/teacher-vacancies/`
> Gap: Page 53 covers overload (too many periods). This page covers shortages — unfilled positions and subject-level adequacy.
> Distinct from teaching load monitor: focuses on vacancies, not workload distribution.

| Element | Spec |
|---|---|
| **Access** | Academic Director G3 (full) · CAO G4 (view + escalate) · Stream Coordinators G3 (own stream) |
| **Summary stats** | Total sanctioned posts · Filled posts · Vacant posts · Vacancy % · Branches with critical vacancy (>20%) |
| **Table columns** | Branch · Subject · Required Teachers · Filled · Vacant · Vacancy % · Days Vacant (longest) · Covering Arrangement |
| **Filters** | Branch · Subject · Stream · Vacancy severity (Critical >20% / Moderate 10–20% / Low <10%) |
| **Alert logic** | Vacancy >20% in core subject → red alert to Academic Director + CAO |
| **Covering arrangement** | Track how vacancy is covered: Guest faculty / Peer cover / No cover (critical) |
| **Drawer: vacancy-detail** | 560px · Subject · Branch · Sanctioned posts · Filled · Vacant since · Job description link · Covering plan · Escalation history |
| **Charts** | Vacancy by subject (bar) · Vacancy by branch (map/bar) · Vacancy trend (line) |
| **Export** | CSV for HR team · Branch-wise vacancy report PDF |

---

**71 — Result Re-evaluation Request Manager** `/group/acad/reevaluation/`
> Gap: Students disputing subjective marks had no formal platform workflow — emails/calls only.
> Manages the complete re-evaluation lifecycle from student request to final mark update.

| Element | Spec |
|---|---|
| **Access** | Exam Controller G3 (full) · Results Coordinator G3 (view + decision) · CAO G4 (override) |
| **Request sources** | Branch portal (student submits) → reaches group Exam Controller |
| **Table columns** | Student · Branch · Exam · Subject · Original Mark · Requested By · Submitted Date · Assigned To · Status · Decision |
| **Status flow** | Submitted → Assigned → Under Review → Decision Pending → Resolved |
| **Filters** | Branch · Exam · Subject · Status · Date range |
| **Drawer: request-review** | 680px · Tabs: Request Details · Original answer (scanned upload) · Reviewer Notes · Mark Comparison · Decision |
| **Decision options** | No change (with reason) · Mark revised (new mark entered) · Re-paper (exam repeated) |
| **Audit** | Full change log — original mark, reviewer, reason, new mark — immutable |
| **Integration** | Approved mark changes propagate back to Result Moderation (page 27) and re-trigger rank recomputation (page 30) |
| **SLA tracking** | Request must be resolved within 15 working days — escalation alert if breached |

---

**72 — Remedial Programme Manager** `/group/acad/remedial/`
> Gap: Remedial classes run ad-hoc at branch level — no group coordination, no tracking of which branches have programmes.
> Provides group-level oversight and standardisation of remedial academic support.

| Element | Spec |
|---|---|
| **Access** | Academic Director G3 (full) · Stream Coordinators G3 (own stream) · CAO G4 (view) |
| **Table columns** | Branch · Stream · Subject · Target Group (criteria: <40%) · Sessions Scheduled · Sessions Completed · Students Enrolled · Pre/Post Assessment |
| **Filters** | Branch · Stream · Subject · Status (Active/Completed/Not Started) |
| **Trigger logic** | Auto-flag: if branch has >15% students below 40% in a subject, prompt creation of remedial programme |
| **Drawer: remedial-create** | 640px · Branch · Stream · Subject · Target criteria · Schedule (days/periods) · Assigned teacher · Duration · Assessment plan |
| **Progress tracking** | Session attendance % · Pre-assessment score vs post-assessment score (improvement metric) |
| **Charts** | Remedial programme coverage by branch (bar) · Pre vs post assessment improvement (grouped bar) |
| **Group templates** | Academic Director can publish a remedial session template — branches can clone |
| **Export** | Branch-wise remedial progress report (PDF) |

---

**73 — Inter-Branch Academic Events Manager** `/group/acad/inter-branch-events/`
> Gap: Quiz Bowls, Science Fairs, Debate Competitions organized informally — no central registration, results, or recognition tracking.
> Covers group-owned competitive academic events across branches.

| Element | Spec |
|---|---|
| **Access** | Academic Director G3 (full) · Olympiad Coordinator G3 (full) · CAO G4 (view + approve) |
| **Event types** | Quiz Bowl · Science Fair · Debate · Essay Competition · Maths Olympiad (group-internal) · Spelling Bee · GK Championship |
| **Table columns** | Event Name · Type · Date · Branches Participating · Students Registered · Status · Winner Branch |
| **Filters** | Event type · Date range · Branch · Stream · Status |
| **Drawer: event-create** | 640px · Name · Type · Date & Venue · Branch scope (invite all / select) · Class eligibility · Registration deadline · Judging criteria · Prize |
| **Drawer: event-detail** | 640px · Tabs: Overview · Registrations (student list) · Schedule · Results · Gallery link |
| **Registration management** | Branch staff registers students via branch portal · Group side sees all registrations |
| **Results entry** | Enter team/individual ranks · Auto-generate winner certificate (PDF) |
| **Charts** | Events per term (bar) · Branch participation rate (heatmap) · Winning branch history |
| **Export** | Participation certificates (bulk PDF) · Results report |

---

**74 — Group Timetable Standards** `/group/acad/timetable-standards/`
> Gap: Each branch built its own timetable — no group-mandated minimum periods per subject per week.
> Sets and monitors group-wide timetable standards; branches audit against them.

| Element | Spec |
|---|---|
| **Access** | CAO G4 (full) · Curriculum Coordinator G2 (edit standards) · Academic Director G3 (view + audit) · Stream Coordinators G3 (own stream) |
| **Standards definition** | Min periods per week per subject per class/stream — e.g. "MPC Class 11 — Maths: 8 periods/week min" |
| **Standards table** | Stream · Class · Subject · Min Periods/Week · Recommended · Is Mandatory |
| **Compliance audit** | Upload branch timetable (CSV or PDF) → system checks against standards → deviation report |
| **Branch compliance table** | Branch · Standard · Actual · Gap · Status (Compliant/Non-Compliant) |
| **Filters** | Stream · Class · Subject · Branch · Compliance status |
| **Alert** | Branch with >3 non-compliant subjects → alert to Academic Director |
| **Drawer: standard-edit** | 480px · Stream · Class · Subject · Min periods · Mandatory Y/N · Effective from |
| **Drawer: branch-compliance-detail** | 560px · Branch timetable vs standards side-by-side · Deviations list · Action required |
| **Charts** | Compliance rate by branch (bar) · Non-compliant subjects (sorted bar) |
| **Export** | Standards document (PDF for branch notice board) · Compliance audit report (CSV) |

---

## Section 14 — Third Audit Gap-Fill (Pages 75–79)

> Added during third deep audit (2026-03-21). Five functional gaps identified as forcing spreadsheet/email workarounds for group academic leadership.

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 75 | Chapter / Unit Progress Tracker | `/group/acad/chapter-progress/` | `75-chapter-progress-tracker.md` | P1 | ✅ |
| 76 | Teacher-Subject-Class Assignment Matrix | `/group/acad/teacher-assignments/` | `76-teacher-subject-class-matrix.md` | P1 | ✅ |
| 77 | Supplementary / Make-Up Exam Manager | `/group/acad/supplementary-exams/` | `77-supplementary-exam-manager.md` | P1 | ✅ |
| 78 | Academic Awards & Recognition Manager | `/group/acad/awards/` | `78-academic-awards-manager.md` | P2 | ✅ |
| 79 | Study Material Dispatch Tracker | `/group/acad/material-dispatch/` | `79-study-material-dispatch.md` | P2 | ✅ |

---

**75 — Chapter / Unit Progress Tracker** `/group/acad/chapter-progress/`
> Gap: Syllabus Manager (page 15) holds the plan; no live tracking of actual chapter completion per branch per class.
> Allows branches to log chapter completion dates; group leadership sees pacing vs. planned timeline.

| Element | Spec |
|---|---|
| **Access** | CAO G4 (view + override) · Academic Director G3 (full) · Curriculum Coordinator G2 (view) · Stream Coordinators G3 (own stream) · MIS Officer G1 (read) |
| **Summary stats bar** | Branches On Track · Branches Behind (>1 chapter) · Branches Critical (>2 chapters behind) · % Group-wide completion |
| **Main table columns** | Branch · Stream · Class · Subject · Expected Chapter (today) · Actual Chapter · Gap · Last Updated · Status |
| **Status logic** | On Track (actual ≥ expected) · Behind (1 chapter behind) · Critical (2+ chapters behind, red) |
| **Filters** | Branch · Stream · Class · Subject · Status (On Track / Behind / Critical) |
| **Pacing source** | Linked to Syllabus Manager (page 15) — chapter sequence + planned completion dates are pulled from syllabus |
| **Branch input** | Branch portal: Subject teacher logs "Completed Chapter N on [date]" — feeds this tracker |
| **Drawer: branch-subject-detail** | 560px · All chapters with planned vs actual dates · Chapter-level completion log |
| **Alerts** | Auto-alert to Stream Coordinator when branch falls behind · Escalation to Academic Director if critical for >7 days |
| **Charts** | Pacing trend (line: planned vs actual completion % over time) · Behind-by-subject bar chart |
| **Export** | Branch × Subject pacing report (CSV) |
| **Role visibility** | Stream Coordinators see own-stream data only · MIS Officer read-only |

---

**76 — Teacher-Subject-Class Assignment Matrix** `/group/acad/teacher-assignments/`
> Gap: Teaching Load (page 53) shows periods/week; no page shows which teacher is assigned to which class-section per subject.
> Master assignment grid: Branch × Class × Section × Subject → Assigned Teacher, with completeness validation.

| Element | Spec |
|---|---|
| **Access** | Academic Director G3 (full) · Stream Coordinators G3 (own stream) · CAO G4 (view + escalate) |
| **Matrix view** | Row: Branch + Class + Section · Column: Subject · Cell: Assigned Teacher name or ⚠ Unassigned |
| **Filters** | Branch · Stream · Class · Subject · Status (Assigned / Unassigned / Guest Faculty) |
| **Summary stats** | Total class-subject slots · Filled · Unassigned · Covered by guest faculty |
| **Alert logic** | Any unassigned slot in a core subject → alert to Academic Director and Stream Coordinator |
| **Assignment types** | Regular teacher · Guest faculty (temporary) · Shared from another branch |
| **Drawer: slot-assign** | 480px · Branch · Class · Section · Subject · Search teacher · Type (Regular / Guest / Shared) · Effective date |
| **Bulk assign** | Select multiple class-sections → assign same teacher (e.g. for common subjects) |
| **Validation** | System warns if teacher already has >max periods/week (linked to Teaching Load Monitor, page 53) |
| **Export** | Branch-wise assignment sheet (CSV / PDF for branch notice board) |
| **Role visibility** | Stream Coordinators: own-stream classes only · CAO: aggregate unassigned count by branch |

---

**77 — Supplementary / Make-Up Exam Manager** `/group/acad/supplementary-exams/`
> Gap: Page 22 (Exam Calendar) manages main exams only. Students who fail or were absent need a structured re-exam workflow.
> End-to-end: identify eligible students → schedule exam → assign paper → upload marks → integrate into ranks.

| Element | Spec |
|---|---|
| **Access** | Exam Controller G3 (full) · Results Coordinator G3 (view + publish) · CAO G4 (view + override) |
| **Eligibility source** | Auto-populated from main result uploads: students below pass % → eligible for supplementary |
| **Table columns** | Student · Branch · Stream · Class · Subject(s) · Main Exam · Fail Reason · Supplementary Exam Date · Paper Assigned · Marks Uploaded · Status |
| **Status flow** | Eligible → Scheduled → Paper Assigned → Conducted → Marks Uploaded → Result Published |
| **Filters** | Branch · Stream · Class · Subject · Status · Date range |
| **Drawer: supplementary-schedule** | 640px · Select eligible students (multi-select) · Exam date · Centre (branch or group exam centre) · Assign paper (from Question Bank page 23) · Notify branches |
| **Drawer: marks-upload** | 480px · Subject-wise marks entry per student (or CSV upload) |
| **Result integration** | On publish: marks flow to Result Archive (page 34) with "Supplementary" tag · Rank recomputation triggered if policy allows |
| **SLA tracking** | Supplementary exam must be scheduled within 30 days of main result publish — alert if not |
| **Charts** | Pass rate: main vs supplementary (bar) · Subject-wise supplementary failure rate |
| **Export** | Eligible students list (CSV) · Supplementary result sheet (PDF) |

---

**78 — Academic Awards & Recognition Manager** `/group/acad/awards/`
> Gap: Page 31 (Topper Lists) shows rank-based recognition only. No mechanism for effort awards, subject excellence, or improvement-based recognition.
> Structured group-level recognition workflow: define award → auto-generate eligible list → approve → issue certificates.

| Element | Spec |
|---|---|
| **Access** | CAO G4 (full — approve and publish) · Academic Director G3 (create + manage) · Stream Coordinators G3 (own-stream nominees) · MIS Officer G1 (read) |
| **Award types** | Subject Excellence (top scorer per subject) · Most Improved (largest % improvement term-on-term) · Merit Scholarship (composite score threshold) · Perfect Attendance + Pass · Olympiad Champion (linked from page 44) · Effort Award (manual nomination) |
| **Award definition** | Name · Type · Eligibility criteria (auto or manual) · Number of awardees · Prize (cash / certificate / medal) · Term/Year |
| **Auto-eligibility** | System computes eligible students from existing data (results, attendance, improvement) — reviewed before approval |
| **Manual nomination** | Branch staff can nominate for Effort Award — goes to Academic Director for approval |
| **Table columns** | Award · Term · Type · Eligible Students · Approved Awardees · Certificates Issued · Status |
| **Certificate generation** | Bulk PDF certificates (name, award, date, group signature) — one-time download link |
| **Drawer: award-create** | 640px · Name · Type · Criteria · Scope (branches/streams) · Prize · Certificate template |
| **Drawer: award-nominees** | 640px · Auto-generated + manual nominees · Approve/Reject per student · Bulk approve |
| **Export** | Awardee list (CSV) · Certificate batch (PDF) |
| **Charts** | Awards by branch (heatmap) · Award type distribution (pie) |

---

**79 — Study Material Dispatch Tracker** `/group/acad/material-dispatch/`
> Gap: Content Library (page 17) manages digital files. No tracking of physical printed study materials dispatched to branches.
> Tracks print orders, dispatch quantities, branch receipt acknowledgements.

| Element | Spec |
|---|---|
| **Access** | Curriculum Coordinator G2 (full — create dispatch) · CAO G4 (view) · Academic Director G3 (view) |
| **Table columns** | Material Name · Type (Workbook / Question Sheet / Reference / Lab Manual) · Term · Total Copies · Branches · Dispatched Date · Acknowledged · Outstanding |
| **Dispatch workflow** | Curriculum Coord creates dispatch record → enters quantity per branch → branch Principal acknowledges receipt via branch portal |
| **Filters** | Term · Material type · Branch · Acknowledgement status (Acknowledged / Pending / Overdue) |
| **Alert** | Dispatch not acknowledged by branch within 7 days → alert to Curriculum Coordinator |
| **Drawer: dispatch-create** | 640px · Material name · Type · Linked content (from page 17, optional) · Quantity per branch (table entry) · Dispatch date · Vendor/Printer |
| **Drawer: dispatch-detail** | 480px · Per-branch: quantity sent · acknowledged date · acknowledgement proof (upload) |
| **Reorder tracking** | Note when a branch requests additional copies — tracked as reorder request |
| **Export** | Dispatch register (PDF) · Acknowledgement status (CSV) · Material consumption report |
| **Charts** | Dispatch completion % by branch (bar) · Outstanding acknowledgements (sorted bar) |

---

## Shared Drawers & Overlays (all div-b pages)

| Drawer | Trigger | Width | Tabs | Description |
|---|---|---|---|---|
| `syllabus-create` | Syllabus Manager → + New | 640px | Stream & Class · Subjects · Topic List · Board Mapping · Publish | Full syllabus creation form |
| `syllabus-view` | Syllabus row → View | 560px | Overview · Topics · Branch Adherence · History | Read-only syllabus with branch compliance |
| `topic-edit` | Syllabus → topic row | 480px | — | Topic name, subtopics, sequence, difficulty, hours, resources |
| `lesson-plan-template-create` | Lesson Plans → + New | 640px | Structure · Required Sections · Assessment Checklist · Publish | Template builder |
| `content-upload` | Content Library → Upload | 680px | File/Link · Metadata · Access Scope · Preview · Submit | Upload + tag content |
| `content-review` | Upload Queue → row | 560px | Preview · Metadata · Notes · Decision | Approve/reject with reason |
| `question-create` | Question Bank → + New | 680px | Question Text · Options · Explanation · Classification · Tags | LaTeX-enabled question creation |
| `question-preview` | Question Bank → preview icon | 480px | — | Student-view render of question |
| `exam-schedule-create` | Exam Calendar → + New | 680px | Identity · Date & Time · Branch Scope · Paper · Notification | Full exam scheduling |
| `exam-schedule-view` | Exam Calendar → row | 560px | Overview · Branches · Paper Status · Conflicts · History | Exam detail read-only |
| `paper-builder` | Exam Papers → Open Builder | Full-page | — | Left: question bank · Right: paper structure |
| `moderation-view` | Result Moderation → row | 680px | Raw Marks · Statistical Checks · Adjustments · Approval | Full moderation workspace |
| `result-publish-detail` | Results Publisher → row | 640px | Summary Stats · Per-Branch · Rank Distribution · Publish Channels | Publication control |
| `student-rank-detail` | Rankings → student row | 480px | All subject marks · Rank · Percentile · AIR estimate | Individual student rank |
| `topper-profile` | Topper Lists → row | 480px | Exam history · Current rank · Scholarship eligibility | Topper detail |
| `topic-branch-drill` | Subject Heatmap → cell | 480px | Questions · Avg marks · Common errors | Heatmap cell drill-down |
| `test-create` (JEE/NEET) | Test Series → + New | 640px | Identity · Paper · Branch scope · Schedule · Notification | Mock test creation |
| `coaching-slot-create` | Coaching Schedule → + New | 480px | Day · Period · Subject · Faculty · Branch · Week range | Timetable slot |
| `olympiad-add` | Olympiad Registry → + New | 480px | Name · Body · Classes · Deadline · Fee | Olympiad registration |
| `olympiad-result-entry` | Olympiad Results → + New | 480px | Student lookup · Olympiad · Score · Rank · Award | Result recording |
| `iep-create` | IEP Manager → + New | 680px | Student Link · Goals · Strategies · Support Hours · Accommodations · Review Schedule | Full IEP creation |
| `iep-review` | IEP Manager → Review due | 640px | Goal Progress · Updated Strategies · Notes · Next Review · Approve | Periodic IEP review |
| `accommodation-request-view` | Accommodations → row | 480px | Student · Disability · Request · Decision | Approve/deny accommodation |
| `teacher-appraisal-create` | Teacher Performance → row | 640px | Results Score · Attendance · Lesson Plans · Peer Review · Composite · Recommendation | Annual appraisal |
| `observation-create` | Observation Log → + New | 640px | Teacher lookup · Rubric (10 criteria) · Strengths · Improvements · Follow-up | Structured observation |
| `cpd-record-add` | CPD Tracker → + Record | 480px | Teacher lookup · Training details · Hours · Certificate upload | CPD record |
| `calendar-event-create` | Group Calendar → + New | 520px | Name · Type · Date · Branches · Mandatory · Notify | Calendar event |
| `ptm-create` | PTM Schedule → + New | 480px | Branch(es) · Date · Type · Agenda · Notification | PTM scheduling |
| `holiday-add` | Holiday Manager → + New | 480px | Date · Name · Type · Branch scope · Reason | Holiday declaration |
| `branch-calendar-detail` | Calendar Compliance → row | 480px | Group vs Branch side-by-side · Deviations | Compliance drill-down |
| `audit-create` (standardisation) | Standardisation Audit → + New | 640px | Branch · Auditor · Date · Checklist | Audit with rubric |
| `paper-distribution-detail` | Paper Distribution → row | 480px | Download log · Acknowledgement trail | Distribution tracking |
| `academic-policy-create` | Academic Policy → + New | 640px | Content · Category · Effective Date · Scope · Acknowledgement | Policy creation |
| `academic-policy-view` | Academic Policy → row | 560px | Current Version · History · Acknowledgements | Policy detail |
| `branch-health-detail` | Branch Health → row | 560px | Score Breakdown · Historical Trend · Drill-downs · Recommendations | Health drill-down |
| `student-risk-detail` | Dropout Signals → row | 560px | Signals · Performance Graph · Fee Status · Counsellor Notes | Dropout risk detail |
| `scholarship-exam-create` | Scholarship Exam → + New | 640px | Identity · Eligibility · Registration · Paper · Award Structure | Scholarship exam setup |

---

## UI Component Standard (applied to every page in div-b)

| Component | Specification |
|---|---|
| **Tables** | Sortable all columns · Checkbox row select + select-all · Responsive (card on mobile < 768px) · Column visibility toggle · Row count badge |
| **Search** | Full-text, 300ms debounce, highlights match |
| **Advanced Filters** | Slide-in filter drawer · Active filters as dismissible chips · "Clear All" · Filter count badge on filter button |
| **Pagination** | Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z results" · Page jump input |
| **Drawers** | Slide from right · Widths: 400/480/520/560/640/680px · Full-page for paper builder · Backdrop click closes (unsaved-changes guard) · ESC closes |
| **Modals** | Centred overlay · Used for confirm/delete only · Max width 480px · Primary + cancel buttons |
| **Forms** | Inline validation on blur · Required field `*` · Character counter on textareas · Disabled submit until valid · Server error summary at top |
| **Toasts** | Bottom-right · Success 4s auto-dismiss · Error manual dismiss · Warning 6s · Info 4s · Max 3 stacked |
| **Loaders** | Skeleton screens matching layout · Spinner on action buttons · Full-page overlay for critical ops (rank computation) |
| **Empty States** | Illustration + heading + description + CTA button · Separate state for "no data" vs "no search results" |
| **Charts** | Chart.js 4.x · Responsive · Colorblind-safe palette · Legend · Tooltip · PNG export |
| **LaTeX** | KaTeX for question rendering in question bank and exam papers |
| **Role-based UI** | Every button/column/section rendered server-side based on role level — G1 never sees write controls · G2 sees upload but not approve |

---

## Role → Page Access Matrix

| Page | CAO G4 | Acad Dir G3 | Curr Coord G2 | Exam Ctrl G3 | Results Coord G3 | Stream MPC G3 | Stream BiPC G3 | Stream MEC/CEC G3 | Stream HEC G3 | JEE/NEET G3 | IIT Found G3 | Olympiad G3 | Special Ed G3 | MIS G1 | Cal Mgr G3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 CAO Dashboard | ✅ Full | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| 02 Acad Dir Dashboard | — | ✅ Full | — | — | — | — | — | — | — | — | — | — | — | — | — |
| 03 Curr Coord Dashboard | — | — | ✅ Full | — | — | — | — | — | — | — | — | — | — | — | — |
| 04 Exam Ctrl Dashboard | — | — | — | ✅ Full | — | — | — | — | — | — | — | — | — | — | — |
| 05 Results Coord Dashboard | — | — | — | — | ✅ Full | — | — | — | — | — | — | — | — | — | — |
| 06 Stream MPC Dashboard | — | — | — | — | — | ✅ Full | — | — | — | — | — | — | — | — | — |
| 07 Stream BiPC Dashboard | — | — | — | — | — | — | ✅ Full | — | — | — | — | — | — | — | — |
| 08 Stream MEC/CEC Dashboard | — | — | — | — | — | — | — | ✅ Full | — | — | — | — | — | — | — |
| 09 JEE/NEET Dashboard | — | — | — | — | — | — | — | — | — | ✅ Full | — | — | — | — | — |
| 10 IIT Found Dashboard | — | — | — | — | — | — | — | — | — | — | ✅ Full | — | — | — | — |
| 11 Olympiad Dashboard | — | — | — | — | — | — | — | — | — | — | — | ✅ Full | — | — | — |
| 12 Special Ed Dashboard | — | — | — | — | — | — | — | — | — | — | — | — | ✅ Full | — | — |
| 13 MIS Dashboard | ✅ View | ✅ View | — | — | — | — | — | — | — | — | — | — | — | ✅ Full | — |
| 14 Cal Mgr Dashboard | ✅ View | — | — | — | — | — | — | — | — | — | — | — | — | — | ✅ Full |
| 15 Syllabus Manager | ✅ Full | ✅ Full | ✅ Edit topics | — | — | ✅ MPC view | ✅ BiPC view | ✅ MEC/CEC view | ✅ HEC view | ✅ view | ✅ view | — | — | ✅ Read | — |
| 16 Lesson Plan Standards | ✅ Full | ✅ Full | ✅ Create templates | — | — | ✅ MPC | ✅ BiPC | ✅ MEC/CEC | ✅ HEC | — | — | — | — | ✅ Read | — |
| 17 Content Library | ✅ Full + approve | ✅ Full | ✅ Upload + edit own | — | — | ✅ Upload MPC | ✅ Upload BiPC | ✅ Upload MEC | ✅ Upload HEC | ✅ Upload JEE | ✅ Upload Found | ✅ Upload Olympiad | — | ✅ Read | — |
| 18 Subject-Topic Master | ✅ Full | ✅ Full | ✅ Edit | — | — | ✅ MPC view | ✅ BiPC view | ✅ MEC view | ✅ HEC view | ✅ view | ✅ view | — | — | — | — |
| 19 Stream Configuration | ✅ Full | ✅ View + propose | — | — | — | ✅ MPC view | ✅ BiPC view | ✅ MEC view | ✅ HEC view | ✅ view | ✅ view | — | — | — | — |
| 20 Textbook Mapping | ✅ Full | ✅ Full | ✅ Edit | — | — | ✅ MPC | ✅ BiPC | ✅ MEC | ✅ HEC | — | ✅ Foundation | — | — | ✅ Read | — |
| 21 Content Upload Queue | ✅ Full + approve | ✅ Approve/reject | ✅ Review + approve | — | — | ✅ Review MPC | ✅ Review BiPC | ✅ Review MEC | ✅ Review HEC | ✅ Review JEE | ✅ Review Found | — | — | — | — |
| 22 Exam Calendar | ✅ Full | ✅ View | — | ✅ Full | — | ✅ MPC view | ✅ BiPC view | ✅ MEC view | ✅ HEC view | ✅ JEE view | ✅ Found view | ✅ Olympiad view | — | ✅ Read | ✅ Coordinate |
| 23 Question Bank | ✅ Full | — | ✅ Create | ✅ Full | — | ✅ MPC | ✅ BiPC | ✅ MEC | ✅ HEC | ✅ JEE/NEET | ✅ Foundation | — | — | — | — |
| 24 Exam Paper Builder | ✅ Approve | — | — | ✅ Full | — | ✅ Draft MPC | ✅ Draft BiPC | ✅ Draft MEC | ✅ Draft HEC | ✅ Draft JEE | ✅ Draft Found | — | — | — | — |
| 25 Branch Exam Schedule | ✅ Full | — | — | ✅ Full | ✅ View | ✅ MPC view | ✅ BiPC view | ✅ MEC view | ✅ HEC view | ✅ JEE view | ✅ Found view | — | — | — | ✅ View |
| 26 Exam Conflict Monitor | ✅ Resolve | — | — | ✅ Full | — | ✅ MPC view | ✅ BiPC view | ✅ MEC view | ✅ HEC view | ✅ JEE view | ✅ Found view | — | — | — | ✅ View + propose |
| 27 Result Moderation | ✅ Full + override | — | — | ✅ Full | ✅ Approve + publish | ✅ MPC view | ✅ BiPC view | ✅ MEC view | ✅ HEC view | ✅ JEE view | ✅ Found view | — | — | ✅ Read | — |
| 28 Answer Keys | ✅ Finalize | — | — | ✅ Full | — | ✅ MPC view | ✅ BiPC view | ✅ MEC view | ✅ HEC view | ✅ JEE view | — | — | — | — | — |
| 29 Results Publisher | ✅ Full override | — | — | ✅ View | ✅ Full publish | — | — | — | — | ✅ JEE results | ✅ Found results | — | — | ✅ Read | — |
| 30 Rank Computation | ✅ Override | — | — | ✅ Trigger | ✅ Full | — | — | — | — | ✅ JEE | ✅ Found | — | — | ✅ Read after compute | — |
| 31 Topper Lists | ✅ Full | ✅ View | — | — | ✅ Full | ✅ MPC toppers | ✅ BiPC toppers | ✅ MEC toppers | ✅ HEC toppers | ✅ JEE toppers | ✅ Found toppers | ✅ Olympiad toppers | — | ✅ Read | — |
| 32 Subject Heatmap | ✅ Full | ✅ Full | — | ✅ Full | ✅ Full | ✅ MPC | ✅ BiPC | ✅ MEC | ✅ HEC | ✅ JEE | ✅ Found | — | — | ✅ Read | — |
| 33 Branch Comparison | ✅ Full | ✅ Full | — | ✅ Full | ✅ Full | ✅ MPC | ✅ BiPC | ✅ MEC | ✅ HEC | — | — | — | — | ✅ Read | — |
| 34 Result Archive | ✅ Read | ✅ Read | — | ✅ Read | ✅ Read | ✅ Read | ✅ Read | ✅ Read | ✅ Read | ✅ Read | ✅ Read | ✅ Read | — | ✅ Read | — |
| 35 JEE/NEET Test Series | ✅ Approve | — | — | ✅ Paper assign | ✅ Publish results | — | — | — | — | ✅ Full | — | — | — | ✅ Read | — |
| 36 Coaching Schedule | ✅ View | — | — | — | — | ✅ MPC view | ✅ BiPC view | — | — | ✅ Full | — | — | — | — | ✅ View |
| 37 JEE/NEET Performance | ✅ View | ✅ View | — | — | — | — | — | — | — | ✅ Full | — | — | — | ✅ Read | — |
| 38 NTA Syllabus Coverage | ✅ View | — | ✅ Edit | — | — | — | — | — | — | ✅ Full | — | — | — | — | — |
| 39 Foundation Program Mgr | ✅ View | — | ✅ Content upload | — | — | — | — | — | — | — | ✅ Full | — | — | — | — |
| 40 Foundation Test Series | ✅ Approve | — | — | ✅ Paper | ✅ Publish | — | — | — | — | — | ✅ Full | — | — | — | — |
| 41 Foundation Performance | ✅ View | ✅ View | — | — | — | — | — | — | — | — | ✅ Full | — | — | ✅ Read | — |
| 42 Olympiad Registry | ✅ View | — | — | — | — | — | — | — | — | — | — | ✅ Full | — | — | — |
| 43 Olympiad Registrations | ✅ View | — | — | — | — | — | — | — | — | — | — | ✅ Full | — | ✅ Read | — |
| 44 Olympiad Results | ✅ View | — | — | — | — | — | — | — | — | — | — | ✅ Full | — | ✅ Read | — |
| 45 Scholarship Exam Mgr | ✅ Approve | — | — | ✅ Paper | ✅ Publish results | — | — | — | — | — | — | ✅ Full | — | — | — |
| 46 Special Needs Registry | ✅ View | ✅ View summary | — | — | — | — | — | — | — | — | — | — | ✅ Full | ✅ Anon stats | — |
| 47 IEP Manager | ✅ View + sign-off | ✅ View | — | — | — | — | — | — | — | — | — | — | ✅ Full | ✅ Anon count | — |
| 48 Accommodation Tracker | ✅ Override | — | — | ✅ View approved | — | — | — | — | — | — | — | — | ✅ Full | — | — |
| 49 Special Ed Reports | ✅ Download | ✅ Download | — | — | — | — | — | — | — | — | — | — | ✅ Generate | ✅ Download | — |
| 50 Teacher Performance | ✅ View + override | ✅ Full | — | — | — | ✅ MPC view | ✅ BiPC view | ✅ MEC view | ✅ HEC view | — | — | — | — | ✅ Anon read | — |
| 51 Observation Log | ✅ View | ✅ Full | — | — | — | ✅ MPC | ✅ BiPC | ✅ MEC | ✅ HEC | — | — | — | — | — | — |
| 52 CPD Tracker | ✅ View | ✅ Full | — | — | — | ✅ MPC | ✅ BiPC | ✅ MEC | ✅ HEC | — | — | — | — | ✅ Read | — |
| 53 Teaching Load | ✅ View | ✅ Full | — | — | — | ✅ MPC | ✅ BiPC | ✅ MEC | ✅ HEC | — | — | — | — | — | — |
| 54 Academic MIS Report | ✅ Approve dist | ✅ Generate | — | — | — | — | — | — | — | — | — | — | — | ✅ Full | — |
| 55 Branch Health | ✅ Full | ✅ Full | — | — | — | ✅ MPC view | ✅ BiPC view | ✅ MEC view | ✅ HEC view | — | — | — | — | ✅ Full | — |
| 56 Dropout Signals | ✅ View | ✅ Full | — | — | — | — | — | — | — | — | — | — | ✅ Own students | ✅ Read | — |
| 57 Attendance Correlator | ✅ View | ✅ Full | — | — | — | — | — | — | — | — | — | — | — | ✅ Full | — |
| 58 Trend Analytics | ✅ Full | ✅ Full | — | — | — | — | — | — | — | — | — | — | — | ✅ Full | — |
| 59 Group Academic Calendar | ✅ Approve mandatory | ✅ View | — | ✅ View | — | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | — | — | ✅ Full |
| 60 PTM Schedule | ✅ View | ✅ View | — | — | — | — | — | — | — | — | — | — | — | — | ✅ Full |
| 61 Holiday Manager | ✅ Approve | — | — | — | — | — | — | — | — | — | — | — | — | — | ✅ Full |
| 62 Calendar Compliance | ✅ View | ✅ View | — | — | — | — | — | — | — | — | — | — | — | — | ✅ Full |
| 63 Standardisation Audit | ✅ Initiate | ✅ Full | — | — | — | ✅ MPC | ✅ BiPC | ✅ MEC | ✅ HEC | — | — | — | — | — | — |
| 64 Paper Distribution | ✅ View | — | — | ✅ Full | — | — | — | — | — | — | — | — | — | — | — |
| 65 Academic Policy | ✅ Full | ✅ Draft + propose | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ Read | ✅ View |
| 66 HEC Stream Dashboard | — | — | — | — | — | — | — | — | ✅ Full | — | — | — | — | — | — |
| 67 AY Setup Wizard | ✅ Full | ✅ Review | — | — | — | — | — | — | — | — | — | — | — | ✅ Read | — |
| 68 Board Exam Tracker | ✅ View | ✅ View | — | ✅ Full | — | — | — | — | — | — | — | — | — | ✅ Read | — |
| 69 Student Acad Profile | ✅ Full | ✅ Full | — | ✅ Full | ✅ Full | ✅ Own str | ✅ Own str | ✅ Own str | ✅ Own str | — | — | — | — | ✅ Anon | — |
| 70 Teacher Vacancy Monitor | ✅ View | ✅ Full | — | — | — | ✅ Own str | ✅ Own str | ✅ Own str | ✅ Own str | — | — | — | — | — | — |
| 71 Re-evaluation Requests | ✅ Override | — | — | ✅ Full | ✅ View + decide | — | — | — | — | — | — | — | — | — | — |
| 72 Remedial Programme Mgr | ✅ View | ✅ Full | — | — | — | ✅ Own str | ✅ Own str | ✅ Own str | ✅ Own str | — | — | — | — | — | — |
| 73 Inter-Branch Events | ✅ View + approve | ✅ Full | — | — | — | — | — | — | — | — | — | ✅ Full | — | — | — |
| 74 Timetable Standards | ✅ Full | ✅ View + audit | ✅ Edit standards | — | — | ✅ Own str | ✅ Own str | ✅ Own str | ✅ Own str | — | — | — | — | — | — |
| 75 Chapter Progress Tracker | ✅ View | ✅ Full | ✅ View | — | — | ✅ Own str | ✅ Own str | ✅ Own str | ✅ Own str | — | — | — | — | ✅ Read | — |
| 76 Teacher Assignment Matrix | ✅ View | ✅ Full | — | — | — | ✅ Own str | ✅ Own str | ✅ Own str | ✅ Own str | — | — | — | — | — | — |
| 77 Supplementary Exam Mgr | ✅ Override | — | — | ✅ Full | ✅ View + publish | — | — | — | — | — | — | — | — | — | — |
| 78 Academic Awards Mgr | ✅ Full | ✅ Create + manage | — | — | — | ✅ Own str nominees | ✅ Own str nominees | ✅ Own str nominees | ✅ Own str nominees | — | — | — | — | ✅ Read | — |
| 79 Material Dispatch Tracker | ✅ View | ✅ View | ✅ Full | — | — | — | — | — | — | — | — | — | — | — | — |

---

## Full Functional Coverage Audit — Zero Gaps

| # | Job to Be Done | Role | Page(s) |
|---|---|---|---|
| 1 | See group-wide academic health at a glance | CAO | 01 |
| 2 | Act on pending approvals (papers, results, IEPs, policies) | CAO | 01, 17 (Div-A) |
| 3 | Configure and maintain the group's full curriculum | CAO / Academic Dir | 15, 18, 19 |
| 4 | Standardise lesson plan format across all branches | Curriculum Coord | 16 |
| 5 | Manage central group content library (notes, PDFs, videos) | Curriculum Coord | 17, 21 |
| 6 | Map subjects and topics to a canonical hierarchy | CAO / Curriculum Coord | 18 |
| 7 | Configure what subjects and pass criteria a stream has | CAO | 19 |
| 8 | Map textbooks to class/subject/board for procurement | Curriculum Coord | 20 |
| 9 | Schedule all group-level exams without conflicts | Exam Controller | 22, 26 |
| 10 | Build question bank (10,000–50,000 MCQs) | Exam Controller / Stream Coords | 23 |
| 11 | Create question papers from question bank | Exam Controller / Stream Coords | 24 |
| 12 | Detect and resolve exam scheduling conflicts automatically | Exam Controller | 26 |
| 13 | Monitor branch readiness for each exam | Exam Controller | 25 |
| 14 | Moderate branch-submitted results statistically | Exam Controller | 27 |
| 15 | Publish and manage answer keys + challenge window | Exam Controller | 28 |
| 16 | Compute cross-branch ranks after all marks are uploaded | Results Coordinator | 30 |
| 17 | Publish results to students and parents | Results Coordinator | 29 |
| 18 | Maintain official topper lists, nominate for scholarships | Results Coordinator | 31 |
| 19 | Identify topic-level weaknesses per branch | Academic Dir / Exam Ctrl | 32 |
| 20 | Compare any set of branches on exam performance | Academic Dir | 33 |
| 21 | Access historical result archive (up to 10 years) | All Div-B | 34 |
| 22 | Standardise MPC stream curriculum and teaching quality | Stream Coord MPC | 06, 15, 16, 23, 50 |
| 23 | Standardise BiPC stream curriculum and teaching quality | Stream Coord BiPC | 07, 15, 16, 23, 50 |
| 24 | Standardise MEC/CEC stream curriculum | Stream Coord MEC/CEC | 08, 15, 16, 23, 50 |
| 25 | Manage JEE/NEET mock test series end-to-end | JEE/NEET Head | 35, 37 |
| 26 | Build integrated coaching timetable without conflicts | JEE/NEET Head | 36 |
| 27 | Track JEE/NEET student performance and AIR estimates | JEE/NEET Head | 37 |
| 28 | Verify NTA syllabus fully covered by group curriculum | JEE/NEET Head / Curriculum Coord | 38 |
| 29 | Manage IIT Foundation program Classes 6–10 | IIT Foundation Director | 39, 40, 41 |
| 30 | Track foundation student performance + scholarship eligibility | IIT Foundation Director | 41 |
| 31 | Register students for NTSE, NMMS, NSO, IMO, KVPY | Olympiad Coordinator | 42, 43 |
| 32 | Record and celebrate olympiad results | Olympiad Coordinator | 44 |
| 33 | Run group-owned scholarship entrance exams | Olympiad Coordinator | 45 |
| 34 | Maintain DPDP-compliant registry of special needs students | Special Ed Coordinator | 46 |
| 35 | Create, track, and review Individual Education Plans | Special Ed Coordinator | 47 |
| 36 | Approve exam accommodations (extra time, scribe, etc.) | Special Ed Coordinator | 48 |
| 37 | Generate NCPCR-format special education compliance reports | Special Ed Coordinator | 49 |
| 38 | Track teacher performance across all branches | Academic Director | 50 |
| 39 | Log structured classroom observations | Academic Dir / Inspection Officer | 51 |
| 40 | Track mandatory CPD hours for all teachers | Academic Dir | 52 |
| 41 | Monitor teaching load — detect overloaded/underloaded teachers | Academic Dir | 53 |
| 42 | Generate monthly MIS report for Chairman/Board | MIS Officer | 54 |
| 43 | View composite academic health score per branch | CAO / Academic Dir | 55 |
| 44 | Detect early dropout signals before students leave | Academic Dir | 56 |
| 45 | Prove attendance drives results (or investigate why it doesn't) | Academic Dir / CAO | 57 |
| 46 | View 6-term academic trend for board strategy | CAO / Strategic Advisor | 58 |
| 47 | Publish group academic calendar; mandate events to branches | Calendar Manager | 59 |
| 48 | Schedule PTMs across all branches + notify parents | Calendar Manager | 60 |
| 49 | Declare and approve holidays (group + branch-requested) | Calendar Manager | 61 |
| 50 | Audit branch compliance with group calendar | Calendar Manager | 62 |
| 51 | Audit whether branches actually follow group standards | Academic Dir | 63 |
| 52 | Securely distribute question papers to branches with audit trail | Exam Controller | 64 |
| 53 | Maintain versioned academic policies (result/re-exam/promotion) | CAO | 65 |
| 54 | Manage HEC stream curriculum, teaching quality, and performance | Stream Coord HEC | 66 |
| 55 | Roll over the academic year — promote students, reset syllabus, calendar | CAO / Academic Dir | 67 |
| 56 | Track Class 10/12 board exam registration, hall tickets, and results | Exam Controller | 68 |
| 57 | View any student's full cross-branch academic history | CAO / Academic Dir / Exam Ctrl | 69 |
| 58 | Detect unfilled teacher posts before they impact teaching quality | Academic Director | 70 |
| 59 | Manage student requests to have subjective marks re-checked | Exam Controller | 71 |
| 60 | Coordinate group-level remedial classes for weak students | Academic Director | 72 |
| 61 | Organise and track inter-branch academic competitions | Academic Director | 73 |
| 62 | Set and audit minimum periods-per-subject across all branches | CAO / Curriculum Coord | 74 |
| 63 | Track actual chapter completion per branch vs. planned pacing | Academic Director / Stream Coords | 75 |
| 64 | Validate every class-section has an assigned teacher per subject | Academic Director | 76 |
| 65 | Manage supplementary exams for failed/absent students end-to-end | Exam Controller | 77 |
| 66 | Recognise students beyond rank — effort, improvement, subject excellence | CAO / Academic Dir | 78 |
| 67 | Track dispatch and branch receipt of physical study materials | Curriculum Coordinator | 79 |

---

## Functional Gaps — Fully Resolved

| Gap | Resolution |
|---|---|
| No role-specific post-login dashboards for any of 14 academic roles | Pages 01–14 — each role has a dedicated, data-rich dashboard |
| No group-level syllabus master — branches each had their own | Page 15 — Syllabus Manager: group sets, branches inherit |
| No canonical subject-topic hierarchy — inconsistent naming across branches | Page 18 — Subject-Topic Master: single source of truth for all modules |
| Lesson plan format inconsistent across branches | Page 16 — Lesson Plan Standards with branch compliance tracking |
| No central content library — materials shared via WhatsApp/email | Page 17 — Shared Content Library with approval workflow |
| No group question bank — each branch set its own papers | Page 23 — Question Bank with 10,000–50,000 MCQs, LaTeX support |
| Exam papers created informally — no builder, no version control | Page 24 — Exam Paper Builder with paper versioning and approvals |
| No automated exam conflict detection | Page 26 — Exam Conflict Monitor with auto-detect on every schedule change |
| Branch readiness for exams never tracked until day-of | Page 25 — Branch Exam Schedule with readiness status and auto-alerts |
| Result moderation done in Excel and email — no statistical checks | Page 27 — Result Moderation with Z-score outlier detection |
| Answer keys and challenge windows handled outside platform | Page 28 — Mark Scheme & Answer Keys with challenge workflow |
| Cross-branch rank computation done manually in Excel | Page 30 — Group Rank Computation with automated engine |
| Topper lists compiled ad-hoc — no single source for marketing/scholarships | Page 31 — Topper Lists & Leaderboard with scholarship nomination flow |
| No topic-level performance analysis — only overall marks | Page 32 — Subject Performance Heatmap with branch × topic drill-down |
| JEE/NEET mock series managed separately from main platform | Pages 35–38 — Full JEE/NEET integration including NTA syllabus coverage |
| Integrated coaching timetable conflicts with regular timetable — no detection | Page 36 — Integrated Coaching Schedule with conflict detection |
| IIT Foundation (Cl.6–10) had no program management | Pages 39–41 — Full Foundation program and performance tracking |
| Olympiad registrations tracked in spreadsheets | Pages 42–44 — Olympiad Registry + Registration + Results |
| No group-owned scholarship exam workflow | Page 45 — Scholarship Exam Manager |
| Special needs registry existed only at branch level — no group visibility | Page 46 — Special Needs Registry with DPDP data masking |
| IEPs tracked in Word documents — no review reminders | Page 47 — IEP Manager with goal tracking and auto-reminders |
| Exam accommodations for special students coordinated by phone | Page 48 — Accommodation Request Tracker with exam-controller integration |
| Teacher performance appraisals informal — no composite scoring | Page 50 — Teacher Performance Tracker with composite score |
| Classroom observations not standardised — rubric varied by observer | Page 51 — Observation Log with 10-criterion standardised rubric |
| CPD hours tracked in HR Excel — not visible to academic leadership | Page 52 — CPD Tracker integrated with teacher performance score |
| Teaching overload not detected — some teachers had 35+ periods | Page 53 — Teaching Load Monitor with configurable thresholds |
| Monthly MIS report manually compiled — error-prone and late | Page 54 — Academic MIS Report with scheduled auto-generation |
| No composite branch academic health metric | Page 55 — Branch Academic Health Dashboard with configurable formula |
| Dropout signals noticed only after student stopped attending | Page 56 — Dropout Signal Monitor with 4-signal early-warning system |
| Group academic calendar existed as a PDF — branches ignored it | Page 59 — Group Academic Calendar with mandatory event locks |
| PTM scheduling uncoordinated — some branches skipped terms | Page 60 — PTM Schedule Manager with parent notification automation |
| Holiday approvals done by phone — no audit trail | Page 61 — Holiday & Working Day Manager with request/approve workflow |
| No check whether branches actually follow group calendar | Page 62 — Branch Calendar Compliance with deviation alerts |
| No mechanism to verify branches follow group curriculum | Page 63 — Academic Standardisation Audit |
| Question papers emailed to branches — no distribution audit trail | Page 64 — Exam Paper Distribution Pipeline with one-time download links |
| Academic policies (re-exam, grace marks) shared informally | Page 65 — Academic Policy Manager with versioning and acknowledgements |
| HEC stream (Humanities, Economics, Commerce) had no dedicated stream coordinator dashboard | Page 66 — Stream Coordinator HEC Dashboard |
| Academic year rollover done ad-hoc — no platform wizard, causing data inconsistency | Page 67 — Academic Year Setup Wizard |
| Board exam (CBSE/State) logistics tracked in spreadsheets — no central visibility | Page 68 — Board Exam Tracker |
| No group-level view of individual student academic history across branches | Page 69 — Student Academic Profile Viewer |
| Teacher vacancies not tracked centrally — shortages discovered only at branch level | Page 70 — Teacher Adequacy & Vacancy Monitor |
| Mark dispute emails/calls only — no formal re-evaluation workflow | Page 71 — Result Re-evaluation Request Manager |
| Remedial classes run ad-hoc at branch level — no group coordination | Page 72 — Remedial Programme Manager |
| Inter-branch academic competitions (Quiz, Debate, Science Fair) managed outside platform | Page 73 — Inter-Branch Academic Events Manager |
| Each branch built its own timetable — no group-mandated subject period minimums | Page 74 — Group Timetable Standards |
| Syllabus defined but no live chapter pacing — branches fell behind undetected | Page 75 — Chapter / Unit Progress Tracker |
| Teaching Load Monitor showed periods; no class-section assignment completeness check | Page 76 — Teacher-Subject-Class Assignment Matrix |
| Students who fail exams had no structured platform workflow for re-exams | Page 77 — Supplementary / Make-Up Exam Manager |
| Topper lists only captured rank-based recognition — no effort or improvement awards | Page 78 — Academic Awards & Recognition Manager |
| Physical study material dispatch tracked by email/phone — no dispatch or receipt log | Page 79 — Study Material Dispatch Tracker |

---

## Full Page Count by Section

| Section | Pages | Priority Range |
|---|---|---|
| 1 — Role Dashboards | 14 | P0 |
| 2 — Curriculum & Content | 7 | P0–P2 |
| 3 — Exam Management | 7 | P0–P1 |
| 4 — Results & Rankings | 6 | P0–P2 |
| 5 — JEE/NEET Integration | 4 | P1–P2 |
| 6 — IIT Foundation | 3 | P1–P2 |
| 7 — Olympiad & Scholarships | 4 | P1 |
| 8 — Special Education | 4 | P1–P2 |
| 9 — Teacher Performance & CPD | 4 | P1–P2 |
| 10 — Academic MIS & Analytics | 5 | P0–P2 |
| 11 — Academic Calendar | 4 | P0–P1 |
| 12 — Gap-Fill Additions | 3 | P1–P2 |
| 13 — Second Audit Gap-Fill | 9 | P0–P2 |
| 14 — Third Audit Gap-Fill | 5 | P1–P2 |
| **Total** | **79** | |

---

## Implementation Priority

```
P0 — Before group academic portal goes live
  01–15   All 15 role dashboards (including HEC stream coord, page 66)
  15      Syllabus Manager
  17      Shared Content Library
  18      Subject-Topic Master
  22      Group Exam Calendar
  23      Question Bank
  24      Exam Paper Builder
  27      Result Moderation
  29      Cross-Branch Results Publisher
  30      Group Rank Computation
  54      Academic MIS Report
  59      Group Academic Calendar
  67      Academic Year Setup Wizard

P1 — Sprint 2
  16, 19, 20, 21, 25, 26, 28, 31, 32, 33, 35, 36, 37, 39, 40,
  42, 43, 44, 45, 46, 47, 48, 50, 51, 52, 55, 56, 60, 61, 62, 63, 64,
  68, 69, 70, 71, 72, 74, 75, 76, 77

P2 — Sprint 3
  34, 38, 41, 49, 53, 57, 58, 65, 73, 78, 79
```

---

*Last updated: 2026-03-21 · Total pages: 79 · Roles: 15 · Gaps resolved: 49*
