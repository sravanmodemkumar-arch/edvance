# Module 21 — Results & Report Cards

## 1. Purpose
Consolidate marks from all upstream modules (exams, assignments, attendance, practicals) into a
verified, board-compliant result record; generate digital report cards, transcripts, and official
documents; publish to students and parents with full audit trail; integrate with DigiLocker, NAD,
NSP, and AISHE; and enforce every applicable CBSE, UGC, AICTE, state board, NCVT, NIOS, and NEP
2020 rule without manual intervention.

---

## 2. Result Consolidation Engine

### 2.1 Upstream Data Sources
| Source Module | Data Pulled |
|---|---|
| Module 20 — Exam Submission & Auto-Grading | Theory marks, practical marks, auto-grade, manual evaluation result, moderation-adjusted marks |
| Module 14 — Homework & Assignments | Assignment scores, project marks, FA component |
| Module 11/12/13 — Attendance | Attendance %, eligible/ineligible flag per subject |
| Module 15 — Syllabus & Curriculum Builder | Syllabus completion %, CO mapping |
| Module 19 — Exam Session & Proctoring | Exam attempt metadata, absent/present flag per paper |
| Institution config | Weightage splits, pass criteria, grading scale selection |

### 2.2 Subject-wise Marks Ledger
Each student-subject pair produces one ledger row:

```
theory_marks (raw) → after_moderation
+ practical_marks
+ internal_assessment_marks  (FA1+FA2 or assignment aggregate)
+ project_marks
+ viva_marks
─────────────────────────────────────────
= total_marks_obtained / total_marks_max
→ percentage, grade, grade_point, credit_points
```

### 2.3 Weightage Engine
- Institution configures % split per board rule (e.g., CBSE Class 12: Theory 70% + Practical 30%;
  UGC semester: Internal 25% + End-Sem 75%).
- Weightage formula locked after Academic Director approval; cannot be changed after result
  computation starts.
- Formula audit log: every weightage application stored with formula string + input values + output.

### 2.4 Multi-Exam Aggregation
- Term 1 + Term 2 + Annual weighted combination per board rule (e.g., CBSE CCE: SA1 + SA2 + FA
  components).
- Pre-board marks excluded from final result; used only for analytics and weak-area identification.
- Configurable formula per institution for coaching/custom term structures.

### 2.5 Attendance-Linked Eligibility
- CBSE/UGC: <75% attendance → subject-wise ineligible flag; attendance shortage recorded on
  result card.
- State boards: board-specific threshold (Karnataka 75%, Tamil Nadu 80%, Rajasthan 75%) —
  configurable per board.
- Medical leave deduction: certified ML days excluded from denominator before % calculation.
- Condonation request: up to 10% condonation allowed by Principal; logged with reason.
- Auto-fail enforcement: system blocks result publication for ineligible student unless Principal
  explicitly grants condonation with documented reason.

### 2.6 Co-curricular & Extra-curricular Marks Import
- Sports, cultural events, NCC, NSS, Scout/Guide — marks entered by respective in-charge.
- District/State/National level participation grades: A/B/C/D.
- NCC 'B' / 'C' certificate: grade noted on result; counts toward co-curricular GPA (institution
  configurable).
- NSS 240-hour completion: noted on result card and transcript.

### 2.7 Grace Marks Application
- Grace marks applied by system after moderation (Module 20) and before ledger computation.
- Grace applied only to eligible subjects (as per board circular); system checks board rules.
- Grace log: grace_amount, subject, reason, applied_by, timestamp — immutable audit entry.

---

## 3. Grading Scales

### 3.1 CBSE Class 10 (CCE Format)
| Marks Range | Grade | Grade Point |
|---|---|---|
| 91–100 | A1 | 10 |
| 81–90 | A2 | 9 |
| 71–80 | B1 | 8 |
| 61–70 | B2 | 7 |
| 51–60 | C1 | 6 |
| 41–50 | C2 | 5 |
| 33–40 | D | 4 |
| 21–32 | E1 | — (fail) |
| 00–20 | E2 | — (fail) |

- CGPA = average of best 5 subject grade points.
- CGPA → percentage indicative: CGPA × 9.5 (CBSE formula).
- Pass criteria: grade D or above in all subjects (33% each).

### 3.2 CBSE Class 12
- Marks + grade per subject displayed; no CGPA.
- Aggregate percentage = total marks obtained / total max marks × 100.
- Pass criteria: 33% in each subject separately; no overall aggregate minimum.
- Compartment: fail in 1 subject → compartment eligibility letter auto-generated.
- Fail: fail in 2+ subjects → result status = FAIL; re-appear in all failed subjects next year.

### 3.3 UGC Semester System (10-Point Scale)
| Grade | Grade Point | Performance |
|---|---|---|
| O | 10 | Outstanding |
| A+ | 9 | Excellent |
| A | 8 | Very Good |
| B+ | 7 | Good |
| B | 6 | Above Average |
| C | 5 | Average |
| P | 4 | Pass |
| F | 0 | Fail |
| Ab | 0 | Absent |

- SGPA = Σ(credit × grade point) / Σ(credits) for the semester.
- CGPA = Σ(semester credits × SGPA) / Σ(all semester credits) across all semesters completed.
- Percentage equivalent: CGPA × 9.5 (UGC formula per 2023 gazette).
- Backlog subject: grade F recorded; 0 credit points included in CGPA denominator until cleared.

### 3.4 State Board Scales (28 Boards)
| Board | Scale |
|---|---|
| Karnataka SSLC/PUC | A+/A/B+/B/C/D (marks + grade) |
| Maharashtra SSC/HSC | Marks + grade (A1–E2) |
| Tamil Nadu SSLC | Grade A+/A/B+/B/C (500-mark system) |
| Andhra Pradesh SSC | GPA 10-point |
| Telangana SSC | GPA 10-point |
| Rajasthan Board | Marks + division (Distinction/First/Second/Third) |
| UP Board | Marks + division system |
| Bihar Board | Marks + division |
| West Bengal Board | Marks + letter grade |
| Madhya Pradesh Board | Marks + grade |
| Gujarat Board | Marks + grade (SSC/HSC) |
| Odisha Board | Marks + grade (CGPA for +2) |
| Punjab Board | Marks + grade |
| Haryana Board | Marks + grade + division |
| Himachal Pradesh Board | Marks + division |
| Uttarakhand Board | Marks + division |
| Kerala Board | Marks + grade (A+/A/B+/B/C+/C/D+/D/E) |
| Goa Board | Marks + grade |
| Assam Board | Marks + division |
| Manipur Board | Marks + division |
| Meghalaya Board | Marks + grade |
| Mizoram Board | Marks + grade |
| Nagaland Board | Marks + grade |
| Tripura Board | Marks + grade |
| Sikkim Board | Marks + grade |
| J&K Board (JKBOSE) | Marks + grade |
| Chhattisgarh Board | Marks + grade |
| Jharkhand Board | Marks + division |

- All 28 state board templates pre-loaded; institution selects applicable board at setup.
- Custom grading scale builder: coaching institutes and pre-schools define own scale (A-F, 1-10,
  percentage bands) with institution-configured pass marks.

### 3.5 IB (International Baccalaureate)
- Diploma Programme: 1–7 per subject (6 subjects); Theory of Knowledge + Extended Essay (up to 3
  bonus points) → max 45 points.
- Predicted grade: entered by subject teacher; shown on result card separately.
- Bilingual diploma flag: if two languages assessed at HL/SL level.
- Pass: minimum 24 points + pass in core (TOK + EE) + no grade 1 in any subject.

### 3.6 IGCSE / Cambridge
- A*–G grading per subject; U = Ungraded.
- Core curriculum vs Extended curriculum noted per subject.
- EAL (English as Additional Language) support flag.
- AS and A Level: A*–E; AS marks contribute 40% to A Level (Cambridge rules).

### 3.7 ICSE / ISC
- ICSE (Class 10): best-of-5 percentage; English compulsory + 4 best subjects.
- ISC (Class 12): theory + practical per subject; aggregate = best 4 subjects (English mandatory).
- Pass: 33% in each subject + 33% aggregate.

### 3.8 Vocational — NCVT / NSQF
- National Trade Certificate (NTC): theory + practical + viva; each component pass mandatory.
- NSQF Level 1–8: grade A/B/C/D; Level noted on certificate.
- Failing practical alone → compartment in practical only (theory mark preserved).

### 3.9 Professional & Competitive Courses
- Engineering/Medical (AICTE): OGPA 10-point; branch rank; backlog subject count.
- Law (Bar Council): percentage per paper; pass in each paper separately (45% for LLB).
- CA Foundation/Inter/Final (ICAI): 40% per paper + 50% aggregate per group.
- CS/CMA (ICSI/ICMAI): same group aggregate logic as CA.
- B.Ed / D.El.Ed (NCTE): internal + external + teaching practice marks; result per NCTE norms.
- Pharmacy (PCI): OGPA + internship marks.

---

## 4. Report Card Builder

### 4.1 Template Engine
- Dynamic report card template engine: institution configures layout once in Academic Settings;
  fields auto-populated from result ledger on every result compute cycle.
- Template versioning: if board changes format, old template archived; new template applied from
  specified academic year; historical report cards always render using template version active at
  time of issue.
- Multi-format types: School Progress Report, Interim Term Slip, Annual Report Card, College Grade
  Card, Transcript, Provisional Mark Sheet, Consolidated Mark Sheet.

### 4.2 CBSE Prescribed Format
- Strict field positions as per CBSE circular — institution name, affiliation number, centre
  number, logo, address exactly as registered with CBSE.
- Scholastic Areas table: FA1 + FA2 + SA1 (Term 1); FA3 + FA4 + SA2 (Term 2); Scholastic Grade.
- Co-scholastic Areas: Work Education, Art Education, Health & Physical Education — A/B/C/D grade.
- Discipline/Values: A/B/C/D per term.
- Attendance row: Term 1 working days + present; Term 2 working days + present; total.
- Remarks: Class Teacher + Principal remarks (free text, 200 chars each).
- Promotion / Detained / Compartment status in bold.
- Any deviation from CBSE prescribed format blocked unless Principal + Academic Director jointly
  override with documented justification.

### 4.3 State Board Format Library
- 28 state board report card templates pre-loaded by EduForge content team.
- Institution assigns applicable template; template auto-applied on result generation.
- Templates updated when boards revise formats (EduForge platform update cycle).

### 4.4 Standard Report Card Sections
| Section | Content |
|---|---|
| Institution Header | Name, logo (CDN), address, affiliation/recognition number, academic year, board |
| Student Block | Name (as per admission record), roll number, class, section, date of birth, Aadhaar (masked), photo (CDN) |
| Subject Marks Table | Subject name, theory/practical/internal/total marks, max marks, percentage, grade, grade point |
| Attendance Summary | Working days, present days, attendance %, eligibility status |
| Co-curricular | Activity name, level (School/District/State/National), grade |
| Health & Physical Education | Activity marks / grade (CBSE) |
| Remarks | Class teacher + Principal remarks |
| Conduct/Discipline | Grade A/B/C/D |
| Result Status | PROMOTED / DETAINED / COMPARTMENT / FAIL / WITHHELD / ABSENT / MEDICAL LEAVE |
| Special Mentions | Rank (section/class/institution), topper badge, merit certificate reference |
| Signature Block | Class Teacher + HOD + Principal — eSign (DigiLocker Aadhaar-linked) |
| School Seal | CDN image configured once by institution admin |
| QR Code | Links to live result verification page (tamper-proof, no login required for verifier) |
| Watermark | ORIGINAL / DUPLICATE / FOR REFERENCE ONLY — configurable per issue purpose |

### 4.5 Coaching-Specific Report Card
- Test date, test name, total marks, marks obtained, percentile, All-India Rank.
- Subject-wise marks breakdown: Physics / Chemistry / Maths (or Bio) separately.
- Chapter-wise accuracy table: chapter name, attempted, correct, wrong, accuracy %.
- Attempt analysis: attempted / skipped / wrong; negative marking deducted marks.
- Time management: avg time per question; flag if >3 min on MCQ.
- JEE/NEET score projection: predicted range based on mock trend + historical conversion.
- Target vs actual trajectory chart (text representation: Target 650, Current trajectory 610).
- Weak area flags: "Physics — Mechanics: Needs Attention" from item analysis.

### 4.6 Digital Report Card Delivery
- Report card generated as PDF; stored on CDN; `cdn_path` + SHA-256 hash stored in DB.
- Student receives in-app notification → "My Results" section → PDF rendered in-app viewer.
- Parent receives same view in parent dashboard.
- No download option — view-only in-app; "Save to DigiLocker" button available (triggers DigiLocker
  push workflow, Section 13).
- Physical print: institution admin can trigger batch print; printer-optimised A4 PDF generated
  from CDN; printed in-house.

---

## 5. Rank & Merit List

### 5.1 Rank Computation
- Section rank, class rank, branch rank (for colleges), institution rank — all computed
  simultaneously after result publish.
- Tie-breaking order (configurable; default CBSE rule):
  1. Highest marks in English / first language.
  2. Highest marks in Mathematics / Science.
  3. Highest marks in remaining subjects (sequential).
- Tie-break log: every tie-break decision stored with rule applied.

### 5.2 Segment-wise Ranks
| Rank Type | Applies To |
|---|---|
| Gender-wise rank | Male / Female / Transgender — separate rank list for scholarship schemes requiring it |
| Category-wise rank | General / OBC / SC / ST / EWS — for reservation-aware scholarships |
| PWD/CWSN rank | Separate merit list (RPWD Act 2016) |
| Board rank simulation | Estimated district/state rank based on historical board result data |
| Subject topper | Highest marks per subject per class/section |

### 5.3 Merit List Generation
- Top N students per class (N configurable by institution): PDF merit list generated.
- Merit list includes: rank, student name, aggregate marks, percentage, category.
- Posted on institution notice board (in-app announcement linked to merit list PDF).
- Exportable: Principal can share merit list PDF with trust/management via in-app document share.
- Merit list freeze: once published, immutable; corrections require Principal + Academic Director
  joint approval and version a new merit list (v1, v2 tracked).

### 5.4 Aggregate Percentile
- Percentile = (number of students scoring below this student / total students) × 100.
- Computed across all exams in the academic year for coaching analytics.
- JEE/NEET percentile calculated per NTA formula for mock test simulation.

---

## 6. Transcript & Official Document Generation

### 6.1 Document Types
| Document | Trigger | Content |
|---|---|---|
| Term Slip | After each term result | Interim marks; stamped "TERM SLIP — NOT A FINAL RESULT" |
| Annual Report Card | After final result publish | Full year result; promotion/detention status |
| Transcript (College) | On demand by student | SGPA per semester + CGPA + credits earned + backlog count |
| Provisional Mark Sheet | Immediately after result | Stamped "PROVISIONAL"; valid until official mark sheet |
| Consolidated Mark Sheet | Final year, all semesters | All semesters in one document; for job/further study |
| Character Certificate | Linked to conduct grade | Auto-populated; Principal eSign |
| Migration Certificate | On TC request | Result eligibility confirmed; issued with TC (Module 39) |
| Scholarship Recommendation Letter | Top 10% of class | Auto-generated; Principal eSign; CDN PDF |

### 6.2 Document Registry
- Every document: unique `document_id`, issue date, `issued_by` (staff_id), `purpose` ENUM
  (ADMISSION / SCHOLARSHIP / EMPLOYMENT / RTI / PERSONAL).
- SHA-256 hash of PDF stored in DB; verifier portal re-computes hash to confirm authenticity.
- Document expiry: provisional mark sheet expires 6 months from issue date; system shows
  "EXPIRED" watermark after expiry.
- Re-issue: student can request re-issue (purpose = DUPLICATE); watermark changes to DUPLICATE;
  original not invalidated.

### 6.3 DigiLocker Push
- Student taps "Save to DigiLocker" → system calls NIC DigiLocker Issued Documents API.
- Supported document types pushed: Report Card, Transcript, Provisional Mark Sheet, Character
  Certificate.
- DigiLocker URI returned → stored against `document_id` in DB; student can share DigiLocker
  URI directly with employer or university.
- DigiLocker push log: `push_timestamp`, `status` (SUCCESS / FAILED / PENDING), `ack_ref`.
- Retry on failure: up to 3 retries with exponential backoff; alert to institution admin on
  persistent failure.

### 6.4 NAD (National Academic Depository)
- College marksheets and degree certificates pushed to NAD via NSDL API on result finalisation.
- NAD reference number stored against result record; student can use NAD reference for
  verification by employers/universities.
- AICTE-affiliated institutions: NAD push mandatory per AICTE circular 2021.

### 6.5 Verifier Portal
- Public URL: `verify.eduforge.in/doc/{document_id}` — no login required.
- Verifier enters document_id + student date of birth → sees: student name, institution name,
  class/programme, result status, CGPA/percentage, issue date.
- Full marks not exposed to verifier — only summary fields.
- Verification log: every verification event recorded with verifier IP, timestamp, document_id
  (for audit and anti-fraud).

---

## 7. Publish & Access Control

### 7.1 Result Publish Workflow
```
Class Teacher finalises marks
        ↓
HOD reviews (spot checks) → VERIFIED
        ↓
Academic Director approves moderation (Module 20)
        ↓
Principal gives final publish approval
        ↓
System timestamps result → PUBLISHED (immutable timestamp)
        ↓
Student + Parent notified (FCM + SMS)
        ↓
Result card visible in-app
```

### 7.2 Phased Publish
- Publish by class → section → individual student (all configurable).
- Re-publish blocked after correction window closes (Section 7.5).
- Partial publish: Principal can publish Class 10 result before Class 12 result independently.

### 7.3 Pre-publish Preview
- Class teacher and HOD see draft result card before Principal publish.
- Preview watermarked "DRAFT — NOT FOR DISTRIBUTION."
- Preview access logged; not accessible to student or parent.

### 7.4 Result PIN Protection
- Institution-configurable: parent sets 4-digit PIN at first result access.
- PIN stored as bcrypt hash (cost factor 12); never in plaintext.
- PIN reset via OTP to registered parent mobile number.
- Enabled/disabled per institution — default OFF.

### 7.5 Post-Publish Correction Window
- Principal opens correction window: max 48 hours (configurable 24–72 hrs).
- During window: class teacher can correct marks with mandatory reason entry.
- Every correction logged: old_value, new_value, reason, corrected_by, corrected_at.
- Correction triggers re-computation of grade, rank, CGPA automatically.
- After window closes: result frozen; no edits via normal UI.
- Post-freeze correction: only via RTI/legal process — requires Academic Director + Principal +
  Platform Admin triple approval; full audit trail.

### 7.6 Withheld Result
- Principal can withhold result for individual student (e.g., fee default, disciplinary action,
  pending documents).
- Withheld result: computed and stored but not published to student/parent.
- Staff view: result status shows "WITHHELD" with reason.
- Student view: "Result not yet available" — no indication of withhold reason.
- Auto-release: Principal sets auto-release date; on that date result publishes automatically if
  not manually released earlier.

### 7.7 Historical Results
- All past academic years' results accessible in-app to student and parent indefinitely.
- Soft-archive after 10 years: accessible but not in primary result list; searchable on demand.
- Never deleted: retention = permanent (regulatory + legal requirement).

### 7.8 Role-Based Access (RLS)
| Role | Visible Results |
|---|---|
| Student | Own result only |
| Parent/Guardian | Linked child's result only |
| Class Teacher | Own class/section only |
| Subject Teacher | Own subject marks across assigned sections |
| HOD | Own department students |
| Academic Director | All academic results across institution |
| Principal | All results across institution |
| Institution Admin | All results (admin view, no marks editing) |
| Platform Admin | Cross-tenant only for support; audit-logged |

---

## 8. Supplementary / Compartment / Backlog

### 8.1 CBSE Compartment
- System auto-identifies: fail in exactly 1 subject → compartment; 2+ → FAIL.
- Compartment eligibility letter: auto-generated PDF — student details, subject, next exam date
  (from CBSE schedule), centre; available in-app for student.
- Carry-forward: internal assessment marks (FA components) carried forward to compartment attempt;
  student re-appears only in theory.
- Compartment result merged with original result on pass; CGPA/grade recalculated.
- Compartment attempt cap: 2 attempts (CBSE rule); system blocks third compartment entry and
  prompts school to mark student as FAIL.

### 8.2 State Board Supplementary
- State board supplementary exam schedule imported into Module 19.
- Eligible students auto-enrolled in supplementary exam session.
- State board specific rules: UP Board — 3 supplementary attempts; Karnataka — 1 attempt; etc.
- System applies board-specific rules based on board selection in institution config.

### 8.3 Improvement Exam
- Passed student who wants to improve marks: separate improvement exam session.
- Both original and improvement marks stored; best-of shown on result card (CBSE rule).
- Improvement attempt noted on result card: "Appeared for Improvement — Best marks considered."

### 8.4 Backlog Tracking (College / UGC)
- Per-subject backlog: fail in a subject → backlog entry created with (subject_id, semester_id,
  attempt_number).
- Max attempts per paper: configurable per state university / UGC rule (typically 3–5).
- Auto-fail after max attempts: system blocks further registration and alerts Academic Director.
- Backlog cleared: student passes → backlog entry marked CLEARED; CGPA recalculated.
- ATKT (Maharashtra/Gujarat): allowed if failed ≤2 subjects in a semester; system checks and
  grants ATKT or blocks based on institution's state.

### 8.5 KT (Keep Terms) — Maharashtra
- KT subject tracked with attempt number.
- KT fee auto-generated in Module 25 (Fee Collection).
- KT result merged after clearing; SGPA recalculated retroactively for the semester.

### 8.6 Dead Semester
- Student who appeared in no exam that semester → semester marked DEAD.
- No SGPA computed for dead semester; CGPA shows gap.
- Dead semester reason required (medical / personal / disciplinary); logged with evidence ref.

---

## 9. CGPA / GPA Computation (Higher Education)

### 9.1 Credit-Based Semester System
- Each subject has credit structure: L (Lecture) + T (Tutorial) + P (Practical) = total credits.
- Credit points per subject = grade point × credits.
- SGPA = Σ(credit × grade point across all subjects in semester) / Σ(credits in semester).
- CGPA = Σ(all semester credit points earned) / Σ(all registered credits).
- Failed subjects: 0 grade point × credit included in denominator (penalises CGPA until cleared).

### 9.2 Lateral Entry
- CGPA computed from entry semester; semesters before lateral entry not included.
- Transcript shows "Lateral Entry — Semesters 1 & 2 not applicable."

### 9.3 NEP 2020 Credit Integration
- Multidisciplinary courses (major + minor + ability enhancement + skill enhancement) — all
  included in credit computation per UGC NEP guidelines.
- MOOC credits (SWAYAM, Coursera, edX — if UGC recognised): imported on Academic Director
  approval; max 40% of total credits via MOOC (UGC rule).
- Internship credits (NAPS/NATS portal data imported): credit hours mapped to equivalent academic
  credits per institution policy.
- Research project marks (4-year UG research programme): imported from guide + external examiner.

### 9.4 Academic Bank of Credits (ABC)
- Earned credits synced with NAD/DigiLocker via ABC API.
- Student's ABC account updated on each semester result finalisation.
- Credit mobility: student transferring institution — transferred credits imported from ABC into
  new institution's ledger.
- ABC ID stored in student profile; linked to Aadhaar.

### 9.5 4-Year UG Exit Options (NEP 2020)
| Exit Point | Award | Result Card Label |
|---|---|---|
| After Year 2 | UG Diploma | "UG Diploma (2-Year Exit)" |
| After Year 3 | UG Degree | "Bachelor of [Science/Arts/Commerce]" |
| After Year 4 | UG Degree with Honours/Research | "Bachelor of [Subject] Honours" |

- Result card clearly labels exit type.
- Transcript for honours students includes research project details.

---

## 10. Government Scheme Integration

### 10.1 National Scholarship Portal (NSP)
- Auto-generate NSP-eligible student list per scheme:
  - Post-Matric Scholarship SC: marks proof + caste certificate cross-reference.
  - Post-Matric Scholarship ST: same.
  - Central Sector Scholarship (top 20 percentile, CBSE/state board): percentile auto-computed.
  - NMMS Class 8: marks >55%, family income <1.5L/year.
- Export: NSP format CSV with required fields; institution uploads to NSP portal.

### 10.2 NMMS Eligibility
- Auto-identify Class 8 students: marks >55% (50% for SC/ST) + family income <1.5L.
- Eligibility report PDF: student list with marks, category, income band (from profile).
- NMMS exam result (external): imported and stored against student record.

### 10.3 Pradhan Mantri Scholarship Scheme
- CGPA ≥ 6.0 for professional courses check; auto-generate eligibility list.
- Export format compatible with PMSS portal requirement.

### 10.4 State Scholarship Schemes
| Scheme | State | Eligibility Check |
|---|---|---|
| Karnataka Rajyotsava | Karnataka | Marks threshold + Kannada medium |
| Dr. Ambedkar Post-Matric | Tamil Nadu | SC/ST + marks threshold |
| Mukhyamantri Scholarship | Rajasthan | Marks + income |
| Swami Vivekananda Merit-cum-Means | West Bengal | Marks + income + category |
| Jai Bhim Mukhyamantri Pratibha Vikas | Delhi | SC/ST marks threshold |
| Pre-Matric / Post-Matric OBC | All states | OBC certificate + marks |

- Eligibility auto-computed from result data + student profile.
- Institution admin reviews and submits to state scholarship portal.

### 10.5 RTE Act §12 Tracking
- 25% EWS/DG seats in private unaided schools: result of RTE students flagged separately.
- Government annual report: RTE student result summary auto-generated for submission to district
  education officer.
- RTE student result: same quality as other students; no separate grading.

### 10.6 Government Residential School Formats
- NVS (Navodaya Vidyalaya Samiti): result sheets in NVS prescribed format.
- KGBV (Kasturba Gandhi Balika Vidyalaya): girl student result export for state nodal officer.
- EMRS (Eklavya Model Residential Schools): tribal student result; ST-specific format.
- Sainik School: RIMC-format result card.

### 10.7 AISHE & U-DISE+ Export
- AISHE annual return data: pass percentage, dropout rate, gender-wise results per programme —
  in AISHE data format for upload to Ministry of Education portal.
- U-DISE+ data: result-linked indicators (pass rate, retention rate) in U-DISE+ XML format.
- Export scheduled: auto-generated in January each year (AISHE reference period Oct–Sep).

### 10.8 Earn-While-You-Learn (EWL)
- Work performance score imported from employer (NSDC/DDU-GKY partner API or manual entry by
  institution placement coordinator).
- Merged with academic marks for vocational stream final result.
- EWL component: shows separately on transcript as "Workplace Performance: X/100."

---

## 11. Analytics & Performance Insights

### 11.1 Heatmaps
- Class/section performance heatmap: student × subject matrix; colour-coded by percentage range
  (Red <40%, Amber 40–60%, Yellow 60–75%, Green >75%).
- Accessible to class teacher, HOD, and Academic Director.
- Exportable as PDF for academic committee meetings.

### 11.2 Subject Difficulty Analysis
- Average marks per subject across class/institution; identifies weak subjects.
- Year-on-year subject average trend: this year vs last 3 academic years.
- Difficulty Index compared with question bank p-values (Module 17 item analysis linkage).

### 11.3 Teacher Effectiveness Index
- Class average marks vs institution average for same subject → teacher effectiveness indicator.
- Internal staff view only (Principal + Academic Director); never shown to students or parents.
- Not used as sole performance metric; advisory only.

### 11.4 Failure Pattern Analysis
- Which questions / topics caused most failures → feeds back to Module 17 (question bank difficulty
  flag) and Module 15 (syllabus emphasis).
- Failure hotspot report: top 10 topics with highest failure rate, per class, per subject.

### 11.5 Gender & Category Gap Analysis
- Average marks by gender per subject (NEP 2020 equity reporting requirement).
- SC/ST/OBC/General average comparison per class (for post-matric scholarship targeting).
- Reports accessible to Principal and Academic Director; exportable for NAAC/AISHE submission.

### 11.6 CGPA Distribution
- Bell curve visualisation (text/ASCII chart in spec; rendered as bar chart in app) for
  Principal/Academic Director dashboard.
- Semester-wise CGPA trend for each student — progression or regression flag.

### 11.7 Coaching Performance Dashboard
- All-India Test Rank trend per student across test series.
- Percentile progression chart (per week for intensive batches).
- JEE/NEET target achievement probability (based on current trajectory).
- Batch average vs top-10 average — identifies batch quality gap.

---

## 12. Re-evaluation & RTI

### 12.1 Re-evaluation Request
- Student / parent submits re-evaluation request in-app → selects subject(s).
- Fee payable: auto-generated challan in Module 25; request proceeds only after payment confirmed.
- Request routed to HOD → HOD assigns different evaluator (not original evaluator).
- Re-evaluated marks entered in separate field; reconciliation with original:
  - Difference ≤ 10%: original marks retained; re-eval marks noted in log only.
  - Difference > 10%: triggers academic committee review; committee decides final marks.
- Re-evaluation result communicated to student in-app within 30 days (institution-configurable
  SLA).

### 12.2 Re-totalling Request
- Only marks addition verified (no answer quality re-evaluation).
- System auto-computes total from stored per-question marks; discrepancy flagged automatically.
- If discrepancy found: corrected total applied; student notified; correction log entry created.
- Re-totalling fee: lower than re-evaluation; refundable if discrepancy found (institution policy).

### 12.3 RTI Photocopy Request (RTI Act 2005 §6)
- Student / parent / legal guardian submits RTI request in-app or via institution admin.
- RTI fee: ₹10 per application (Central RTI Act); state RTI fee as applicable.
- Response deadline: 30 days from receipt (RTI Act §7).
- Scanned answer sheet PDF: retrieved from CDN (stored per Module 20 evaluation workflow);
  shared with applicant in-app — view-only in-app viewer.
- RTI log: request_date, applicant_id, subject, response_date, cdn_path, responded_by.
- RTI refusal: if exemption applies (e.g., fiduciary relationship, third-party data) — refusal
  with written reason sent in-app; applicant can appeal to First Appellate Authority.

### 12.4 Marks Revision Immutability
- Every change to a published result: immutable log entry (result_corrections table).
- Log fields: old_value, new_value, reason, changed_by, changed_at, approval_chain.
- No deletion of correction log records ever.

---

## 13. DigiLocker & External Integration

### 13.1 DigiLocker Issued Documents API
- Documents pushed: Report Card, Transcript, Provisional Mark Sheet, Character Certificate.
- Push trigger: student taps "Save to DigiLocker" OR institution admin initiates batch push.
- API: NIC DigiLocker Issued Documents v2 API (OAuth2 + client credentials).
- DigiLocker URI stored in `digilocker_push_log`; shown in student document wallet in-app.

### 13.2 NAD Push
- College marksheets + degree certificates → NAD via NSDL DigiLocker ABC API.
- NAD reference number displayed in student document wallet.
- NAD push mandatory for AICTE-affiliated colleges per AICTE circular.

### 13.3 B2B API (Module 51)
- Partner portals (employers, universities) can fetch verified result with student consent.
- Consent token: student generates single-use token (valid 72 hours); shares with partner.
- Partner API call: GET /api/v1/results/{document_id}?consent_token={token}.
- Response: summary fields only (name, institution, programme, CGPA, result status).
- DPDPA 2023 §7 compliance: every data share via B2B API logged with consent reference.

### 13.4 State Board API Integration
- CBSE Result API (when available): auto-fetch board exam marks and merge with internal marks.
- State board portals: marks import via file upload (CSV/Excel) from board portal; parsed and
  merged with internal ledger; discrepancy auto-flagged if >5%.
- Maharashtra HSC/SSC Board API (pilot): direct API integration where available.

---

## 14. CWSN / Special Needs

### 14.1 Scribe Accommodation Notation
- Report card and transcript: "Appeared with Scribe (CBSE CWSN Circular [ref])" notation.
- Extra time granted: noted on result record internally; not shown on public-facing report card.
- Exempted subjects (CBSE CWSN — e.g., third language exemption): automatically excluded from
  aggregate and CGPA computation; report card shows "EXEMPTED" for that subject.

### 14.2 Accessible Report Card Formats
- Braille-format report card: structured text file generated alongside PDF; sent to institution's
  Braille printer or shared with state resource centre.
- Large-print format: A3 PDF with 18pt font; generated on request.
- Same data source as standard report card; no separate data entry required.

### 14.3 RPWD Act 2016 Compliance
- Separate PWD merit list generated on demand (for scholarship schemes).
- Disability type noted on result record (visual / hearing / locomotor / intellectual / autism /
  multiple) — as per RPWD Act disability categories.
- Result record flags: scribe_used, extra_time_granted, exempted_subjects[], disability_type.

---

## 15. Minority / Open School / Special Boards

### 15.1 Madrasa Board
- Dakhil (Class 10), Alim (Class 12), Fazil (Post-graduation) grading per state Madrasa Board.
- Applicable boards: UP Madrasa Education Board, Bihar State Madrasa Education Board, WB Board of
  Madrasa Education, Rajasthan Madrasa Board.
- Subjects: Arabic, Urdu, Islamic Studies + general subjects; grading per board circular.

### 15.2 Sanskrit Board
- Rashtriya Sanskrit Sansthan: Prathama / Madhyama / Shastri / Acharya grading.
- State Sanskrit boards (UP, Rajasthan): separate grade scale configured per board.

### 15.3 NIOS (National Institute of Open Schooling)
- Credit accumulation model: student can pass subjects across multiple attempts within 5-year
  window (Secondary) or 5-year window (Sr. Secondary).
- Per-subject pass status tracked independently; aggregate computed only when all required
  subjects passed.
- On Demand Exam (ODE): result per attempt stored; credit accumulated on pass.
- NIOS transfer certificate: issued when student has cleared all required subjects.

### 15.4 State Open Schools
- Maharashtra State Board of Open Schooling (MSBOS).
- Rajasthan State Open School (RSOS).
- Same credit accumulation model as NIOS; board-specific pass criteria applied.
- Templates pre-loaded for applicable state open school formats.

---

## 16. Exam Type–Specific Result Handling

### 16.1 Unit Test
- Simple marks card; no grade computed.
- Marks fed into FA / internal assessment ledger for term aggregation.
- Not published as standalone result card; visible in student's "Exam History" only.

### 16.2 Pre-Board
- Separate ledger; not included in final result.
- Used for analytics and weak-area identification only.
- Pre-board result card generated for student view (stamped "PRE-BOARD — NOT FINAL").

### 16.3 Board Exam Integration
- External board marks (CBSE/state board) fetched via API or manual import.
- Merged with internal marks for complete consolidated result view.
- Discrepancy alert: if imported board marks differ from internal estimate by >10 marks per
  subject — flag to Academic Director.

### 16.4 Practical / Viva / Project
- Practical: lab teacher entry; HOD verification; merged into subject total.
- Viva/oral: evaluator marks + remarks; remarks visible to HOD and Academic Director only
  (not on student result card).
- Project/dissertation: external examiner marks + internal guide marks → weighted average;
  external examiner marks entry via guest evaluator login (limited access).

### 16.5 Online Proctored Exam (Module 19 Linkage)
- Auto-populated from Module 19 submission.
- Proctoring violation flag visible on staff result view.
- Flag NOT shown on student-facing or parent-facing report card (only available via HOD/Principal
  result dashboard with full audit details).

### 16.6 Internship / Industrial Training
- Mentor marks (from employer/industry partner): entered by institution placement coordinator
  after receiving offline report.
- Institute coordinator marks: separate entry.
- Weighted average per institution policy; shown on transcript as "Internship: X/100 — [Company
  Name]."

---

## 17. Notification & Communication

### 17.1 Result Announcement Broadcast
- Principal sends in-app announcement (Module 34 hook) linked to result publish event.
- Announcement: "Class 10 Results are now available. Check your result card in the Results
  section."

### 17.2 Result SMS Template
```
[SchoolName] | [StudentName] | Class [X]-[Section] | Total: [marks]/[max]
| Grade: [grade] | Rank: [rank] | eduforge.in
```
- 160-character compliant; multi-part SMS if student name is long.
- SMS sent via Module 38 (SMS & OTP) hook.

### 17.3 Parent FCM Push
- Push notification: "Results Published — Tap to view [StudentName]'s result."
- Deep link: opens result card directly in parent app.

### 17.4 Low Marks Alert
- Pre-publish alert (internal only): if any subject <40% (configurable threshold).
- Alert sent to: class teacher + HOD + parent only.
- Not visible to student peer group; private notification with counselling helpline number.
- Counselling referral: auto-create counselling record in Module 32 (Student Welfare) on alert.

### 17.5 Topper Congratulation Notification
- Auto-sent to top 3 students per class on result publish.
- Template: "Congratulations [Name]! You are Rank [1/2/3] in [Class] with [marks]/[max].
  Keep it up!"

### 17.6 Compartment / Fail Alert
- Sensitive notification: sent to parent only (not peer group).
- Template uses empathetic language; includes counselling helpline and next steps.
- Counselling record auto-created in Module 32 on fail/compartment notification.

---

## 18. Scholarship & Welfare Automation

### 18.1 Auto Scholarship Recommendation Letter
- Top 10% of class per section (configurable): PDF recommendation letter.
- Letter content: student name, class, marks, percentage, rank, institution letterhead.
- Principal eSign applied; CDN PDF generated; shared with student in-app.

### 18.2 Free/Concessional Seat Eligibility
- Institution maps its scholarship seats (merit / need-based / category) in Academic Settings.
- System identifies eligible students by rank + category + income band.
- Eligibility report: student list with eligibility reason; reviewed by institution admin before
  award.

### 18.3 Post-Matric Scholarship Automation
- SC/ST/OBC post-matric scholarship: auto-generate student list with marks proof.
- Export: NSP-format CSV; institution uploads to NSP portal.
- Scholarship receipt tracking: once scholarship awarded (entered by admin), shown in student
  financial profile.

### 18.4 Merit-cum-Means Cross-Reference
- CBSE merit list generated from result data.
- Crossed with family income data from student profile (income declared at admission).
- Combined eligibility list for merit-cum-means scholarships.
- Income data sensitivity: only Principal and institution admin can access income field.

---

## 19. Edge Cases & Integrity

### 19.1 Result Cancellation (Mass Malpractice)
- Batch result cancelled on Academic Director + Principal joint order.
- All result records for affected batch: soft-deleted with cancellation_reason and order reference.
- Exam re-scheduled via Module 18/19; new result cycle begins.
- Students notified in-app: "Your result has been cancelled due to [reason]. Re-exam scheduled on
  [date]."

### 19.2 Posthumous Result
- If student is deceased: result completed and mark sheet / certificate issued to legal guardian.
- System flags record: `is_deceased = true`; auto-notifications suppressed.
- Sensitive handling: all communications via institution admin (no automated parent/student push).
- Record retained permanently; never deleted.

### 19.3 Married / Legal Name Change
- Result always issued in name as per board records at time of examination.
- Legal name change noted in student profile but certificate always matches board name.
- Both names stored: `name_as_per_board` (immutable after exam) and `current_legal_name`.

### 19.4 Board Exam Absentee
- Student absent in board exam → that subject marked `AB` (Absent).
- AB treated as 0 marks for aggregate; compartment/fail triggered per subject count.
- Medical absentee: `ML` (Medical Leave) tag; board-specific rule applied (CBSE: best-of-remaining
  subjects rule where applicable).

### 19.5 Board Exam Roll Number Mismatch
- If internal roll number and board roll number differ: admin reconciliation step required before
  board marks import.
- System flags unmatched records; admin maps manually; match logged.

### 19.6 Tie-breaking for Same Aggregate
- Default CBSE tie-break: (1) English marks, (2) Maths marks, (3) first-language marks.
- Coaching: (1) Physics, (2) Chemistry, (3) Maths/Bio — for JEE/NEET orientation.
- Custom tie-break: institution can configure subject priority in Academic Settings.
- Tie remains after all tie-break subjects: joint rank assigned (e.g., two students at Rank 3;
  next student gets Rank 5).

### 19.7 Board Rank Simulation
- Estimated district/state rank based on last 3 years of historical board result data
  (EduForge platform-level aggregate).
- Shown as range: "Estimated State Rank: 2,000–3,000" — clearly labelled as ESTIMATED.
- Not shown on official result card; visible only in analytics dashboard.

---

## 20. NAAC / NBA Accreditation Support

### 20.1 NAAC Self-Study Report Data
- Criterion II (Teaching-Learning-Evaluation) data auto-exported:
  - Pass percentage per programme per year.
  - Dropout rate per year.
  - Average CGPA per programme.
  - Gender-wise pass percentage.
- Export format: NAAC SSR Excel template (Criterion II worksheets).
- Scheduled export: auto-generated in December for annual SSR submission.

### 20.2 NBA Programme-Level Outcome Attainment
- CO attainment (from Module 20 calculation) → PO attainment → PSO attainment cascade.
- CO-PO mapping matrix: populated in Module 15 (Curriculum Builder); used here for attainment
  cascade.
- Attainment levels: Level 1 (<60% students achieving target), Level 2 (60–70%), Level 3 (>70%).
- NBA Tier I/II Self-Assessment Report (SAR): attainment data exported in NBA SAR format.
- Accreditation committee dashboard: CO/PO/PSO attainment trends across semesters; gap analysis.

---

## 21. Data Retention & Audit (DPDPA 2023)

### 21.1 Retention Policy
| Data Type | Retention Period |
|---|---|
| Result records (ledger) | Permanent — never deleted |
| Report card PDFs (CDN) | Permanent |
| Proctoring snapshots (Module 19) | 90 days (DPDPA 2023 minimal retention) |
| Re-evaluation papers | 1 year after re-evaluation completion |
| RTI request logs | 5 years |
| Correction logs | Permanent |
| DigiLocker push logs | 5 years |
| Verification logs | 3 years |

### 21.2 Computation Audit Trail
- Every result computation: input values (raw marks per component) + formula string + output
  stored in immutable audit log.
- Enables full reconstruction of any result at any point in time.
- Accessible to: Principal, Academic Director, Platform Admin (cross-tenant audit access requires
  elevated approval).

### 21.3 DPDPA 2023 Compliance
- Result data shared with parent only after parental consent (collected at admission — Module 09).
- Third-party API access (B2B): student consent token required per data share event.
- Data minimisation: verifier portal exposes only summary fields, not full marks.
- Right to correction: student/parent can request data correction through RTI / correction window
  workflow; all corrections logged.
- Data breach protocol: if result data is compromised, DPO notified within 72 hours (DPDPA §8).

---

## 22. DB Schema

### Table: `result_ledger`
```
result_ledger_id     UUID PRIMARY KEY
student_id           UUID REFERENCES students(student_id)
subject_id           UUID REFERENCES subjects(subject_id)
academic_year_id     UUID
semester_id          UUID NULL
exam_type            VARCHAR(30)   -- ANNUAL | SEMESTER | TERM1 | TERM2 | UNIT_TEST
theory_marks_raw     NUMERIC(6,2)
theory_marks_final   NUMERIC(6,2)  -- after moderation/grace
practical_marks      NUMERIC(6,2)
internal_marks       NUMERIC(6,2)
project_marks        NUMERIC(6,2)
viva_marks           NUMERIC(6,2)
total_marks_obtained NUMERIC(6,2)
total_marks_max      NUMERIC(6,2)
percentage           NUMERIC(5,2)
grade                VARCHAR(5)
grade_point          NUMERIC(4,2)
credits              NUMERIC(4,2)
credit_points        NUMERIC(6,2)
status               VARCHAR(20)   -- PASS | FAIL | ABSENT | MEDICAL_LEAVE | COMPARTMENT | EXEMPTED
grace_applied        NUMERIC(4,2) DEFAULT 0
attendance_eligible  BOOLEAN DEFAULT TRUE
tenant_id            UUID NOT NULL
created_at           TIMESTAMPTZ DEFAULT NOW()
updated_at           TIMESTAMPTZ
```

### Table: `result_header`
```
result_header_id     UUID PRIMARY KEY
student_id           UUID REFERENCES students(student_id)
academic_year_id     UUID
semester_id          UUID NULL
sgpa                 NUMERIC(4,2) NULL
cgpa                 NUMERIC(4,2) NULL
aggregate_marks      NUMERIC(7,2)
aggregate_max        NUMERIC(7,2)
percentage           NUMERIC(5,2)
rank_section         INT NULL
rank_class           INT NULL
rank_institution     INT NULL
rank_category        INT NULL      -- category-wise rank
result_status        VARCHAR(30)   -- PROMOTED | DETAINED | COMPARTMENT | FAIL | WITHHELD | PASS
published_at         TIMESTAMPTZ NULL
published_by         UUID NULL     -- Principal staff_id
correction_window_open BOOLEAN DEFAULT FALSE
correction_window_closes_at TIMESTAMPTZ NULL
is_withheld          BOOLEAN DEFAULT FALSE
withheld_reason      TEXT NULL
is_deceased          BOOLEAN DEFAULT FALSE
tenant_id            UUID NOT NULL
created_at           TIMESTAMPTZ DEFAULT NOW()
updated_at           TIMESTAMPTZ
```

### Table: `report_cards`
```
report_card_id       UUID PRIMARY KEY
student_id           UUID
academic_year_id     UUID
semester_id          UUID NULL
document_type        VARCHAR(30)   -- REPORT_CARD | TRANSCRIPT | PROVISIONAL | CONSOLIDATED | CHARACTER_CERT
cdn_path             VARCHAR(500)
document_hash        CHAR(64)      -- SHA-256
issued_at            TIMESTAMPTZ
issued_by            UUID          -- staff_id
purpose              VARCHAR(30)   -- ORIGINAL | DUPLICATE | FOR_REFERENCE
digilocker_uri       VARCHAR(500) NULL
nad_reference        VARCHAR(100) NULL
is_expired           BOOLEAN DEFAULT FALSE
expires_at           TIMESTAMPTZ NULL
tenant_id            UUID NOT NULL
created_at           TIMESTAMPTZ DEFAULT NOW()
```

### Table: `merit_list`
```
merit_list_id        UUID PRIMARY KEY
class_id             UUID
section_id           UUID NULL
academic_year_id     UUID
version              INT DEFAULT 1
rank                 INT
student_id           UUID
aggregate_marks      NUMERIC(7,2)
percentage           NUMERIC(5,2)
category             VARCHAR(20)   -- GENERAL | OBC | SC | ST | EWS | PWD
published_at         TIMESTAMPTZ
cdn_path             VARCHAR(500)  -- merit list PDF
tenant_id            UUID NOT NULL
created_at           TIMESTAMPTZ DEFAULT NOW()
```

### Table: `result_corrections`
```
correction_id        UUID PRIMARY KEY
result_ledger_id     UUID REFERENCES result_ledger(result_ledger_id)
field_name           VARCHAR(50)
old_value            NUMERIC(7,2)
new_value            NUMERIC(7,2)
reason               TEXT NOT NULL
corrected_by         UUID          -- staff_id
correction_window_id UUID NULL
approved_by          UUID NULL
corrected_at         TIMESTAMPTZ DEFAULT NOW()
tenant_id            UUID NOT NULL
```

### Table: `reeval_requests`
```
reeval_request_id    UUID PRIMARY KEY
student_id           UUID
subject_id           UUID
academic_year_id     UUID
request_type         VARCHAR(20)   -- REEVAL | RETOTALLING | RTI_PHOTOCOPY
status               VARCHAR(20)   -- PENDING | FEE_PENDING | IN_PROGRESS | COMPLETED | REJECTED
fee_challan_id       UUID NULL
original_marks       NUMERIC(6,2)
reeval_marks         NUMERIC(6,2) NULL
final_marks          NUMERIC(6,2) NULL
assigned_evaluator   UUID NULL
response_cdn_path    VARCHAR(500) NULL  -- scanned sheet / RTI response
requested_at         TIMESTAMPTZ DEFAULT NOW()
responded_at         TIMESTAMPTZ NULL
tenant_id            UUID NOT NULL
```

### Table: `backlog_tracker`
```
backlog_id           UUID PRIMARY KEY
student_id           UUID
subject_id           UUID
semester_id          UUID
attempt_number       INT DEFAULT 1
max_attempts         INT
status               VARCHAR(20)   -- ACTIVE | CLEARED | LAPSED
cleared_at           TIMESTAMPTZ NULL
clearing_exam_id     UUID NULL
atkt_granted         BOOLEAN DEFAULT FALSE
kt_fee_challan_id    UUID NULL
tenant_id            UUID NOT NULL
created_at           TIMESTAMPTZ DEFAULT NOW()
```

### Table: `digilocker_push_log`
```
push_log_id          UUID PRIMARY KEY
document_id          UUID REFERENCES report_cards(report_card_id)
student_id           UUID
push_timestamp       TIMESTAMPTZ
status               VARCHAR(20)   -- SUCCESS | FAILED | PENDING | RETRY
ack_ref              VARCHAR(200) NULL
retry_count          INT DEFAULT 0
error_message        TEXT NULL
tenant_id            UUID NOT NULL
```

### Table: `scholarship_eligibility`
```
eligibility_id       UUID PRIMARY KEY
student_id           UUID
academic_year_id     UUID
scheme_name          VARCHAR(100)
scheme_type          VARCHAR(50)   -- NMMS | NSP_SC | NSP_ST | CENTRAL_SECTOR | STATE | RTE | PMSS
eligible             BOOLEAN
eligibility_reason   TEXT
marks_snapshot       JSONB         -- {percentage, rank, category, income_band}
export_status        VARCHAR(20)   -- PENDING | EXPORTED | SUBMITTED
exported_at          TIMESTAMPTZ NULL
tenant_id            UUID NOT NULL
created_at           TIMESTAMPTZ DEFAULT NOW()
```

---

## 23. Integration Map

```
Module 14 (Assignments)  ──→┐
Module 11/12/13 (Attendance)→┤
Module 20 (Auto-Grading)  ──→┤  Module 21 — Results & Report Cards
Module 15 (Curriculum) ───→─┤
Module 19 (Exam Session) ──→┘
         │
         ├──→ Module 32 (Counselling) — low marks / fail alert
         ├──→ Module 34 (Announcements) — result broadcast
         ├──→ Module 35/38 (FCM/SMS) — push + SMS
         ├──→ Module 39 (Certificates & TC) — SLC / migration trigger
         ├──→ Module 24/25 (Fee) — re-evaluation fee, KT fee
         ├──→ Module 51 (B2B API) — employer/university verification
         ├──→ DigiLocker / NAD (NIC API)
         ├──→ NSP / AISHE / U-DISE+ (government portals)
         └──→ NAAC/NBA dashboards (accreditation exports)
```

---

## 24. Compliance Checklist

| Regulation | Compliance Point |
|---|---|
| CBSE Examination Bye-laws | Pass criteria, compartment rules, grace marks, correction window |
| UGC Grading Policy 2023 | 10-point CGPA scale, credit system, SGPA/CGPA formula |
| AICTE | OGPA computation, NAD push mandatory |
| RTE Act §16 | No detention Classes 1–8; system blocks detention entry |
| RTI Act 2005 §6 & §7 | 30-day response; photocopy of answer sheet on request |
| DPDPA 2023 | Consent for data share; minimal retention; breach protocol 72 hrs |
| RPWD Act 2016 | Separate PWD merit list; scribe notation; accessible formats |
| NEP 2020 | 4-year UG exit options; ABC credit sync; MOOC credit integration |
| NCVT/NSQF | Trade certificate grading; practical pass mandatory |
| NIOS Rules | Credit accumulation; 5-year window; ODE result handling |
| POCSO Act | No student data exposed to unverified external parties |
| Copyright Act 1957 §52(1)(i) | Exam papers and answer sheets: educational fair use |
| NAAC/NBA | Criterion II data export; CO/PO/PSO attainment for accreditation |
| AISHE Annual Return | Pass rate, dropout, gender-wise — auto-export format |
| NSP Guidelines | Post-matric scholarship eligibility format compliance |
