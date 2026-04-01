# Module 24 — Fee Structure & Management

## 1. Purpose
Define, version, and govern all fee structures across every institution type on EduForge —
schools (CBSE/state board/KVS/NVS/government), colleges (UGC/AICTE/university-affiliated),
coaching institutes (JEE/NEET/UPSC/Banking/SSC), skill centres (NCVT/PMKVY/DDU-GKY), and
online programmes. Enforce GST compliance (SAC codes, 18% coaching, exempt education),
RTE §12 free-seat enforcement, state Fee Regulatory Authority (FRA) ceiling checks, UGC
refund rules, concession workflows, late fee rules, education loan facilitation, government
scheme zero-fee enforcement, and full statutory audit trail (7-year retention, Income Tax §10(23C),
SFT reporting). Module 24 owns structure and configuration only; Module 25 owns collection
and receipts; Module 26 owns defaulter tracking.

---

## 2. Fee Structure Entity

### 2.1 Structure Definition
- Fee structure: name, academic year, class/grade or programme, branch, student category
  (Day Scholar / Hosteller / NRI / Management / RTE / Distance / Exchange / Lateral Entry),
  effective date, version number, status (DRAFT → APPROVED → ACTIVE → ARCHIVED).
- Multiple structures per academic year per class: Day Scholar + Hosteller structures coexist;
  student auto-assigned based on admission category (Module 07).
- Programme-wise (college): B.Tech CSE, B.Com, MBA — different amounts per programme; aided
  vs unaided sections have separate structures.
- Coaching batch-wise: JEE Long-term vs Short-term vs Crash Course vs Weekend batch — each
  gets own structure; test series as add-on product billed separately.
- Branch-wise override: urban campus fee ≠ rural campus fee; branch admin overrides specific
  heads; override requires institution Principal approval; both amounts tracked.
- Section-wise (coaching): morning batch vs evening batch vs weekend batch — different amounts
  even within same programme.

### 2.2 Version Control
- Every approved change creates a new version (v1, v2, v3…).
- Old version archived; accessible for historical billing and audit.
- Active version always tagged; only one ACTIVE version per structure per academic year.
- Academic year rollover: structure cloned to new year at year-end; staff review amounts;
  previous year unchanged.
- Mid-year new batch: new structure for that batch only; does not disturb existing students.

### 2.3 Template Library
- EduForge pre-loads templates for: CBSE Day School, CBSE Residential School, State Board
  School (28 state variants), Degree College (Arts/Science/Commerce), Engineering College,
  Polytechnic, ITI, Medical College, Law College, B.Ed / D.El.Ed, JEE Coaching, NEET
  Coaching, UPSC Coaching, Banking/SSC Coaching, Skill Centre (PMKVY), Distance/ODL.
- Institution starts from template; modifies amounts and heads; template is starting point only.
- Internal template: institution saves own structure as template for next year or new branch;
  one-click clone.

---

## 3. Fee Heads

### 3.1 Core Academic Fee Heads
| Head | Type | Frequency | Notes |
|---|---|---|---|
| Tuition Fee | Recurring | Monthly/Quarterly/Annual | GST exempt (school/college); 18% GST (coaching) |
| Admission Fee | One-time | On admission | Non-refundable (configurable) |
| Registration/Prospectus Fee | One-time | At enquiry | Module 31 CRM link |
| Annual Charges | Recurring | Annual | Miscellaneous annual levy |
| Development/Building Fund | One-time or Annual | Annual | State FRA regulated |
| Examination Fee | Recurring | Per exam / Annual | Internal exam fee |

### 3.2 Infrastructure Fee Heads
| Head | Notes |
|---|---|
| Laboratory Fee | Per-semester or annual; subject to GST rules |
| Computer Lab Fee | May attract GST if not core education |
| Library Deposit | Refundable; liability ledger entry |
| Library Annual Fee | Recurring; GST exempt |
| Smart Class / Digital Fee | Annual; infrastructure levy |
| Sports / Gymnasium Fee | Annual; optional membership |

### 3.3 Welfare & Activity Fee Heads
| Head | Notes |
|---|---|
| Student Accident Insurance Premium | Annual; collected + remitted to insurer |
| PTA / Alumni Fund | Voluntary configurable; institution sets mandatory/optional |
| Activity / Cultural Fee | Annual |
| NCC / NSS Fund | Nominal; state regulation |
| Annual Day / Picnic / Excursion | Event-specific; optional participation |
| Summer Camp / Winter Camp | Vacation programmes; optional |
| School Magazine / Yearbook | Annual; collected December |
| Anti-Ragging Fund | Some states mandate; nominal; separate head |

### 3.4 Facility Fee Heads
| Head | Notes |
|---|---|
| Transport Fee | Zone-linked (Module 29); different per zone |
| Hostel Fee | Room-type-linked (Module 28); single/double/dormitory |
| Mess / Canteen Fee | Monthly; separate from hostel fee |
| Lab Breakage Deposit | Semester start; refunded on lab clearance certificate |
| Sports Complex / Gym Membership | Optional; annual; student opts in at enrolment |

### 3.5 Document Fee Heads
| Head | Notes |
|---|---|
| Identity Card | Annual or one-time |
| Uniform | One-time per year |
| Books / Stationery | If institution collects; optional |
| Report Card Reprinting | Nominal; Module 21 link |
| TC Issuance Fee | Module 39 link; waived for RTE students |
| Migration Certificate Fee | College; one-time at exit |
| Convocation Fee | College final year; degree + ceremony |
| Thesis / Dissertation Submission | Ph.D./PG; one-time |

### 3.6 Board / Regulatory Passthrough Fee Heads
- CBSE Board Exam Fee, NTA Application Fee, University Exam Fee, Affiliation Fee,
  CBSE Migration Fee, State Board Exam Fee — collected by institution; remitted to board.
- Tracked separately; NOT institution revenue; flagged as `is_passthrough = TRUE`.
- Passthrough authority: CBSE / NTA / State Board / University — stored for reconciliation.
- Passthrough remittance log: amount collected vs amount remitted; difference = reconciliation
  variance; flagged for Finance Head review.

### 3.7 Liability Fee Heads
- Caution Deposit: refundable at course end / TC; `is_liability = TRUE`; separate liability
  ledger entry; not shown as fee income.
- Security Deposit: refundable; building/lab damage security; separate liability entry.
- Lab Breakage Deposit: semester-level; refunded on lab in-charge clearance.
- No-dues certificate (Module 39) prerequisite for all liability refunds.

### 3.8 Coaching-Specific Heads
- Study Material Fee: per module/subject; charged per item; not flat annual.
- Test Series Fee: Module 22 add-on product; subscription-style; auto-expires on package end.
- Crash Course Fee: full upfront or 2 instalments only; no monthly option.
- Course Upgrade Fee: differential fee when student moves from Basic to Advanced batch.
- Demo / Trial Class Refund: 48-hour full refund window enforced; system blocks partial refund
  claim after 48 hours.

### 3.9 College-Specific Heads
- Semester Registration Fee: separate from tuition; non-payment blocks module registration.
- Re-appear / Back Paper Fee: per paper; auto-generated on backlog identification (Module 21).
- KT / ATKT Fee: Maharashtra/Gujarat; per-subject; auto-generated on KT eligibility flag.
- Alumni Association Lifetime Membership: graduation; optional; one-time.

### 3.10 Custom Fee Heads
- Institution creates unlimited custom heads (e.g., "Robotics Club Fee", "Smart Uniform Chip",
  "Digital Lab Subscription").
- No system restriction on custom head creation; only regulatory heads are system-protected.
- Custom head inherits all properties (GST tagging, frequency, refundability).

---

## 4. Fee Frequency & Instalment Plans

### 4.1 Frequency Options (Per Head)
| Frequency | Due Dates |
|---|---|
| Monthly | 1st or 5th or 10th of each month (configurable) |
| Quarterly | April / July / October / January (standard) or custom |
| Half-Yearly | April + October (standard) |
| Annual | April (academic year start) |
| One-Time | On admission / on event / on demand |
| Per-Semester | August + January (college) |

- Each fee head configured with its own frequency independently.
- Mixed-frequency plan: tuition monthly + exam fee annual + transport quarterly — all on one
  invoice calendar; system merges into per-month due amounts.

### 4.2 Instalment Plan Builder
- Number of instalments: 1 to 12 per academic year.
- Per instalment: due date, amount, grace period (days), fee heads included.
- Fee heads split across instalments: e.g., Admission Fee only in Instalment 1; Tuition in
  Instalments 1–10; Exam Fee in Instalment 6 only.
- Instalment lock: once student pays Instalment 1, schedule locked; change requires Finance
  Head approval with reason.

### 4.3 Custom Instalment Per Student
- Hardship accommodation: student gets personalised instalment dates and amounts.
- Academic Director approval required; reason documented.
- Custom plan displayed only to that student; class-level plan unaffected.

### 4.4 Advance & Partial Payment
- Partial: student pays less than due amount; accepted; balance carried forward to next cycle.
- Advance: student pays 2–3 instalments together; excess shown as advance credit; auto-adjusted
  in next instalment generation; advance credit never expires within academic year.

### 4.5 Fee Calendar
- Student/parent view: full-year visual calendar with due dates + amounts per instalment.
- Colour coding: PAID (green) / DUE (orange) / OVERDUE (red) / UPCOMING (grey).
- Export: parent can export fee calendar as PDF for bank/employer records.

---

## 5. GST Compliance

### 5.1 Exemption Rules
| Institution Type | Service | GST Status |
|---|---|---|
| School (up to Class 12) | Tuition, Exam, Library | EXEMPT — CGST Schedule III |
| College / University | Tuition, Exam, Library | EXEMPT |
| Coaching Institute (JEE/NEET/UPSC/Banking) | ALL services | 18% GST — SAC 9992 |
| Any institution | Transport | 5% GST — SAC 9966 |
| Any institution | Hostel (per day >₹1000) | 12% GST — SAC 9963 |
| Any institution | Hostel (per day ≤₹1000) | EXEMPT |
| Any institution | Uniform, Books, Stationery | Applicable HSN rate |
| Any institution | Insurance Premium | 18% GST (passed through) |

### 5.2 Per-Head GST Tagging
- Each fee head tagged: GST_EXEMPT / 5% / 12% / 18%.
- SAC/HSN code stored per head; pre-mapped defaults; institution overrides with CA note.
- Coaching institute type = COACHING: system enforces 18% on ALL heads; cannot set exempt
  (except pure passthrough board fees).
- Composite supply: if institution bundles taxable + exempt services — system identifies
  principal supply; applies GST per composite supply rule (GST Act §8).

### 5.3 GSTIN & Invoice
- Institution GSTIN: 15-digit alphanumeric; stored in institution profile; validated on entry.
- Printed on all taxable invoices; absent on exempt-only receipts.
- Sequential GST invoice number: `INV/{YYYY-YY}/{BRANCH_CODE}/{00001}` — no gaps, no
  duplicates; mandatory per GST Invoice Rules 2017 Rule 46.
- B2B invoice: if parent has GSTIN (corporate-sponsored student) — CGST+SGST (intra-state)
  or IGST (inter-state) split correctly.
- B2C invoice: standard for individual parents.

### 5.4 SAC / HSN Code Pre-Mapping
| Service | SAC/HSN | Rate |
|---|---|---|
| Educational services (tuition/library/exam) | SAC 9992 | EXEMPT or 18% (coaching) |
| Hostel / accommodation | SAC 9963 | EXEMPT / 12% |
| Transport | SAC 9966 | 5% |
| Uniform (school) | HSN 6211 | 5% |
| Stationery / notebooks | HSN 4820 | 12% |
| Insurance premium | SAC 9971 | 18% |

### 5.5 GSTR-1 Export
- Taxable receipts aggregated by SAC code per month.
- Exported in GSTR-1 JSON format (NIC GSTN schema) and Excel; for CA upload on GST portal.
- B2B invoices: listed with GSTIN, invoice number, taxable value, GST amount.
- B2C large invoices (>₹2.5L): listed individually.
- B2C small invoices: consolidated state-wise.

### 5.6 Input Tax Credit (ITC)
- Educational institutions (exempt services): ITC not claimable on inputs; tracked separately
  as blocked credit for financial reporting.
- Coaching institutes (taxable services): ITC claimable on business inputs; system tracks
  eligible vs ineligible inputs.

### 5.7 Statement of Financial Transactions (SFT)
- If institution collects fee >₹2L per student per year in cash — reportable under IT Rule
  114E (SFT — Form 61A).
- System flags: cash receipts >₹2L per student; generates SFT data for Income Tax filing.

---

## 6. RTE & Government Fee Regulations

### 6.1 RTE Act §12 Free Seats
- 25% EWS/DG seats in private unaided schools — tuition fee auto-zeroed for RTE-flagged
  students.
- System block: any attempt to charge tuition to RTE student raises error; Finance Head cannot
  override without Platform Admin escalation and documented justification.
- TC issuance fee also waived for RTE students automatically.
- All other fee heads (transport, uniform) remain chargeable unless institution voluntarily
  waives.

### 6.2 RTE Reimbursement Claim
- Claim = EWS/DG student count × state government notified per-student reimbursement rate.
- State rates pre-loaded per state (updated annually by EduForge content team).
- Claim report PDF: student list, category, days attended, reimbursement amount per student,
  total — in District Education Officer (DEO) prescribed format.
- Claim status tracked: DRAFT → SUBMITTED → ACKNOWLEDGED → REIMBURSED.
- Reimbursement receipt from state government entered by Finance team; reconciled against claim.

### 6.3 State Fee Regulatory Authority (FRA) Compliance
| State | Regulatory Body | Key Rule |
|---|---|---|
| Tamil Nadu | Private Schools Fee Determination Committee (PSFDC) | Fee ceiling per school category (A/B/C) |
| Maharashtra | Cap Fee Act 1987 + Private University Act | No capitation fee; regulated hike % |
| Rajasthan | RPEIRA | Annual fee approval required |
| Gujarat | Self-Financed Schools Fee Act 2017 | 15% hike ceiling without FRA approval |
| Karnataka | Karnataka Educational Institutions Act 1983 | Fee approval by committee |
| Andhra Pradesh | AP Cap Fee Act 1983 | No capitation; regulated professional college fee |
| Telangana | TS Private Schools Regulation Act | Regulated fee; annual declaration |
| Uttarakhand | State Private University Fee Rules | Per-programme ceiling |
| Chhattisgarh | CG Private University Act | Fee approval |
| Uttar Pradesh | UP Self-Financed Independent Schools Act | Registration + fee approval |

- Institution selects applicable regulatory framework; fee ceiling per category stored.
- HARD_REGULATED mode: system blocks activation of any fee structure exceeding regulatory
  ceiling without Platform Admin override + documentation.
- SOFT_REGULATED mode: system warns; allows override with Academic Director + Principal
  approval + reason; logged for FRA inspection.

### 6.4 FRA Submission Report
- Fee structure in state FRA prescribed format (PDF + Excel); generated one-click.
- Annual submission: institution downloads, signs (Aadhaar eSign), submits to FRA.
- Previous year submission archived on CDN; accessible for 7 years.

### 6.5 Capitation Fee Block
- System prevents creating fee head with name containing: "Donation", "Capitation",
  "Development Contribution (Compulsory)", "Building Contribution (Mandatory)" in regulated
  states.
- Override: Academic Director + Platform Admin joint approval + documentation uploaded to CDN.
- Audit trail: all override attempts logged with requestor, approver, documentation reference.

### 6.6 AICTE Fee Regulation
- AICTE-affiliated colleges: fee ceiling set by State Fee Fixation Committee (each state has
  own committee — AP, Telangana, Karnataka, Tamil Nadu, Maharashtra, etc.).
- Institution inputs AICTE approval letter reference + approved fee amount per programme.
- System alerts if fee structure exceeds approved amount; blocks in HARD_REGULATED mode.
- AICTE Fee Compliance Report: proposed fee vs approved ceiling; exported per programme.

### 6.7 University Fee Order
- State universities fix fee for affiliated colleges (BoS recommendation → Academic Council
  → Executive Council → fee circular).
- Institution inputs university fee order reference number + approved amounts.
- System cross-checks on fee structure activation; alerts on breach.

### 6.8 KVS / NVS Fee Structure
- KVS: centrally determined; very low; system pre-loads and locks core fee heads; institution
  cannot modify tuition and mandatory heads.
- NVS: free education; zero tuition; only nominal material charges permissible.
- Institution type = KVS / NVS: system enforces pre-loaded structure; deviations blocked.

### 6.9 Government School
- Institution type = GOVERNMENT: tuition fee auto-zeroed; system blocks any tuition entry.
- Only nominal charges permissible: uniform, mid-day meal contribution (some states), materials.
- Mid-Day Meal programme: no fee; tracked as government scheme benefit; not in fee module.

### 6.10 Minority Institution
- Minority institutions (linguistic/religious) have different regulatory regime per state.
- Flagged in institution profile: MINORITY_STATUS + linguistic/religious minority type.
- Relevant state exemptions applied; FRA ceiling may not apply to minority institutions
  in some states (per Supreme Court rulings — TMA Pai Foundation, Inamdar case).

---

## 7. Concession & Discount Management

### 7.1 Concession Types
| Type | Trigger | Approval Level |
|---|---|---|
| Merit Scholarship | Auto — Module 21 rank (top N%) | Auto-activated; Finance Head confirms |
| Need-Based | Manual — income proof submitted | Academic Director → Principal |
| Sibling Discount | Auto — 2nd/3rd child same institution | Finance Head confirms |
| Staff Ward | Manual — staff employment verified | HR → Finance Head |
| Management Quota Waiver | Manual | Principal → Finance Head |
| Trustee / Founder Ward | Manual | Finance Head |
| Sports Quota | Manual — sports achievement proof | Sports Teacher → Academic Director |
| NCC / NSS Concession | Manual — certificate | HOD → Academic Director |
| CWSN / Divyang | Auto — CWSN flag in profile | Finance Head confirms |
| EWS / DG (above RTE) | Manual — income + category proof | Academic Director → Principal |
| RTE §12 | Auto — RTE flag in Module 07 | System-enforced; no approval needed |
| Govt Scholarship Deduction | Auto — NSP disbursement entered | Finance team |
| Alumni / Ex-Student Child | Manual — parent alumni status verified | Finance Head |
| Girl Student (Beti Bachao) | Manual — gender + state scheme | Academic Director |
| First-Generation Learner | Manual — profile flag | Academic Director |

### 7.2 Concession Mechanics
- Basis: PERCENTAGE of fee head amount OR FLAT amount — per head; configurable.
- Applicable heads: concession can apply to selected heads only (e.g., 50% tuition + 0%
  transport + 100% exam fee).
- Stacking: multiple concessions applicable to same student; applied in configured priority
  order; total capped at 100% per head (student never gets negative fee).
- Stacking example: Merit 20% + Need-based 30% + Sibling 10% = 60% total; if cap is 70%,
  all three applied; if another concession would exceed cap, it is applied only up to cap.

### 7.3 Concession Approval Workflow
```
Teacher / Counsellor proposes concession
        ↓
HOD reviews → RECOMMENDED
        ↓
Academic Director reviews → APPROVED_BY_AD
        ↓
Principal gives final approval → APPROVED
        ↓
Finance Head activates → ACTIVE
        ↓
System applies from configured instalment
        ↓
Parent notified via FCM + SMS — "Concession of ₹X applied from [date]"
```

### 7.4 Concession Effective Date
- From which instalment concession applies: retroactive application requires Principal
  approval; future-dated application default.
- Retroactive: recalculate previously issued demand notices; revised notices re-sent.

### 7.5 Concession Auto-Expiry
- Merit-based: expires at academic year end; fresh rank check from Module 21 triggers renewal.
- Finance team alerted 30 days before expiry; action required to renew or lapse.
- Need-based: valid 1 year; income proof re-submission required for renewal.
- RTE: never expires while student is enrolled in RTE seat.

### 7.6 Government Scholarship Deduction
- NSP/state scholarship disbursed → Finance team enters disbursement amount + reference.
- Amount deducted from student's outstanding fee ledger; scholarship source tagged.
- Parent notified: "Scholarship of ₹X credited to your fee account."
- Remaining balance after scholarship deduction = net payable; demand notices updated.

### 7.7 Sibling Auto-Detection
- When second sibling enrolled: system detects same parent_id (Module 09); sibling discount
  auto-proposed; Finance Head confirms.
- Third sibling: higher discount tier auto-applied on confirmation.
- Sibling discount lapses if elder sibling graduates/withdraws (configurable institution policy).

### 7.8 Concession Audit Log
- Every concession grant / modification / expiry / renewal: immutable log with reason,
  approver, date, old/new value.
- RTI-defensible: full trail accessible to statutory auditor and FRA inspector.

---

## 8. Late Fee Rules

### 8.1 Late Fee Configuration
| Type | Description |
|---|---|
| Fixed per day | ₹X per day after grace period expires |
| Fixed per week | ₹X per week |
| Percentage per month | Y% of outstanding per month |

- Configured per fee head per structure; different rates for different heads permissible.

### 8.2 Grace Period
- N days after due date before late fee accrues; configurable per instalment.
- Default: 7 days.
- Grace period extended by Principal for natural disasters, exam periods, holidays — documented
  decision; applies institution-wide or to specific classes.

### 8.3 Late Fee Cap
- Maximum late fee: absolute amount (₹X) or % of instalment principal — whichever lower.
- Prevents late fee exceeding principal debt (legally and ethically problematic).

### 8.4 Late Fee Exemption Categories
- Auto-exempt: RTE students (zero late fee), CWSN students, students with active bereavement
  flag, students in disaster-affected districts (district-level flag by Platform Admin).
- Manual exempt: Principal waives late fee for individual student with mandatory reason entry.
- Waiver logged: late_fee_waiver_id, student, amount, reason, waived_by, date — immutable.

### 8.5 GST on Late Fee
- Coaching institutes: late fee attracts 18% GST (same rate as principal service).
- Schools/colleges (exempt): late fee is also exempt.
- System applies GST on late fee automatically per institution type.

### 8.6 Late Fee Reversal
- Parent disputes late fee → Finance team reviews → Finance Head approves reversal.
- Reversal credit applied to ledger; GST adjustment note generated if applicable.
- Full audit trail: original charge, reversal, reason, approver.

---

## 9. Refund Policy

### 9.1 Per-Head Refund Configuration
| Policy | Description |
|---|---|
| FULLY_REFUNDABLE | 100% refund on request within policy period |
| PARTIALLY_REFUNDABLE | Schedule-based refund % (configured) |
| NON_REFUNDABLE | Zero refund; disclosed at admission |

### 9.2 UGC Fee Refund Rules (Colleges — UGC 2018 Notification)
| Withdrawal Timing | Refund % | Processing Fee Cap |
|---|---|---|
| >15 days before course start | 100% | ≤₹1,000 deductible |
| 15 to 7 days before start | 90% | — |
| 7 to 1 day before start | 80% | — |
| On/after start, within 30 days | 50% | — |
| After 30 days from start | 0% | — |

- System enforces UGC minimum; institution cannot configure below UGC floor.
- Institution can configure more generous policy (e.g., 100% up to 7 days) but not stricter.
- Applied automatically on withdrawal request based on date comparison.

### 9.3 Liability Refund (Caution / Security Deposit)
- Tracked in separate liability ledger; not fee income.
- Refunded at TC issuance / graduation after No-Dues clearance (Module 39 link).
- No-dues dependencies: library (Module 30), hostel (Module 28), lab, transport (Module 29),
  finance — all clearance flags required before refund processed.
- Refund mode: original payment mode wherever possible; cheque/bank transfer for cash deposits.

### 9.4 Refund Request Workflow
```
Student/Parent submits refund request in-app
        ↓
Finance team reviews (within 3 working days)
        ↓
Principal approves (within 2 working days)
        ↓
Finance team processes refund — bank transfer / cheque / UPI reversal
        ↓
Refund reference number entered in system
        ↓
Parent notified: "Refund of ₹X processed. Reference: [ref]"
```

### 9.5 Refund Ledger
- All refunds tracked separately: refund_id, student, amount, mode, reference, status.
- Reconciled against fee receipt ledger monthly by Finance team.
- Refund register: statutory auditor requirement.

---

## 10. Special Student Category Fee

### 10.1 Lateral Entry (College)
- Fee prorated from entry semester; not full-year fee.
- System computes pro-rata: (remaining semesters / total semesters) × annual fee.
- Transcript: "Lateral Entry — Semesters 1 & 2 not applicable" (Module 21 link).

### 10.2 NRI Quota
- Higher fee as per AICTE/UGC/state NRI quota notification.
- Separate NRI fee structure; FRA/AICTE reporting mandatory for NRI fee collection.
- Foreign currency conversion: if parent pays in USD/GBP — Finance team converts at RBI
  reference rate; INR amount entered; original currency noted in remarks.

### 10.3 Management Quota
- State-regulated higher fee; separate structure; FRA compliance required.
- FRA reports management quota fee separately from merit quota in annual return.

### 10.4 Ph.D. / M.Phil.
- Per-semester fee; thesis submission fee (one-time at submission).
- Extension semester fee: if thesis not submitted within programme duration; auto-generated
  at programme duration expiry + 1 month.

### 10.5 Distance / ODL
- Lower fee structure; separate fee head set.
- NAAC/UGC ODL compliance: fee not to exceed on-campus fee (UGC ODL regulations).

### 10.6 Exchange / Visiting Students
- Fee waiver or reduction per MOU; institution configures per student.
- Guest student flag in profile; fee structure customised; no standard structure applies.

### 10.7 Re-admitted / Detained Students
- Fee structure of current academic year applies; not prior year.
- Arrears from previous academic year tracked separately in arrears ledger.
- Arrears must be cleared before new academic year registration (configurable institution policy).

---

## 11. Coaching Institute Fee Specifics

### 11.1 Batch Transfer Adjustment
- Student moves from JEE Long-term to Short-term mid-year: fee difference computed.
- Credit (if moving to cheaper batch) applied to ledger; debit (if upgrading) generates
  differential charge.
- Transfer approval: Academic Director; fee adjustment auto-computed; Finance Head activates.

### 11.2 Course Upgrade
- Adding a subject or moving from Basic to Advanced batch: differential fee generated as
  one-time charge.
- Upgrade request: student/parent in-app → Academic Director approval → Finance Head activates.

### 11.3 GST Enforcement (Coaching)
- 18% GST on ALL coaching fee heads without exception.
- System enforces at fee head creation for institution type = COACHING; cannot be set to
  exempt (except pure passthrough board/NTA fees).
- SAC 9992 — "Other education and training services not elsewhere classified."
- GST registration mandatory for coaching institutes with turnover >₹20L (₹10L for North-East
  special category states).

### 11.4 Franchise / Centre Fee Sharing
- Franchised coaching centre: platform tracks centre share vs franchisor share of collected fee.
- Franchisee financial view: shows own share only.
- Franchisor view: aggregate across all franchised centres.
- Revenue sharing formula: configured at institution setup; e.g., 70% centre + 30% franchisor.

### 11.5 Demo / Trial Class Refund
- 48-hour full refund window from demo class date: system enforces.
- After 48 hours: refund blocked via system; Finance Head manual override with reason.
- Demo refund receipt: generated with "DEMO REFUND" label; separate from academic refund.

---

## 12. Fee Revision Workflow

### 12.1 Revision Process
```
Finance team proposes revision (new amounts per head)
        ↓
Regulatory ceiling check (FRA/AICTE/University) — PASS or WARN/BLOCK
        ↓
Academic Director reviews
        ↓
Principal approves with Aadhaar eSign
        ↓
Effective date set (future date only; minimum 21-day notice in most states)
        ↓
Parent notification (FCM + SMS + email — Modules 35/37/38)
        ↓
New version ACTIVE from effective date
        ↓
Old version ARCHIVED; historical billing uses old version
```

### 12.2 Parent Notification Template
```
[Institution Name] — Fee Revision Notice
Dear [Parent Name],
The fee structure for [Class/Programme] will be revised
effective [Date].
New amounts: [Fee Head 1: ₹X | Fee Head 2: ₹Y]
Please view full details in the EduForge app under Fees section.
For queries: [Finance contact]
```

### 12.3 Emergency Fee Freeze
- Platform Admin or state government can flag institution as FEE_FROZEN (court order, COVID
  relief, regulatory investigation).
- System blocks any new fee structure activation during freeze.
- Existing structures continue; no new charges; no revisions.
- Freeze lifted only by Platform Admin with justification.

---

## 13. Demand Notice & Invoice Management

### 13.1 Demand Notice Generation
- Auto-generated 15 days before each instalment due date.
- Content: institution logo, student name + class + roll number, instalment breakdown (head-wise
  amounts), GST amounts, total due, due date, payment modes, late fee warning.
- Language: English + regional language per institution's state (Hindi/Marathi/Tamil/Telugu/
  Kannada/Bengali/Gujarati/Punjabi/Malayalam — configurable).
- Channels: FCM (push) + SMS (Module 38) + in-app notification.

### 13.2 Proforma Invoice
- Generated at admission before actual payment; used for: employer reimbursement, education
  loan application, company sponsorship.
- Stamped "PROFORMA INVOICE — NOT A RECEIPT."
- Valid 30 days from issue; expiry noted on document.

### 13.3 Revised Demand Notice
- If concession applied after initial demand notice: revised notice generated and sent; original
  demand notice voided (status = SUPERSEDED).
- Parent notified: "Your fee demand has been revised. New amount: ₹X."

### 13.4 Bulk Generation
- Finance team generates demand notices for entire class/branch in one action.
- Individual delivery via configured channels.
- Bulk generation log: timestamp, generated_by, count, class/branch.

### 13.5 Parent Acknowledge / Snooze
- Parent can "acknowledge" reminder: stops duplicate reminders for 48 hours.
- Snooze: does not waive payment or late fee; only suppresses notification repetition.

---

## 14. Fee Waiver & Write-off

### 14.1 Fee Waiver
- Full or partial waiver of already-billed outstanding amount (distinct from concession on
  structure).
- Requires: Principal + Finance Head dual approval; reason mandatory.
- Waiver types: GOODWILL / HARDSHIP / ADMINISTRATIVE_ERROR / MANAGEMENT_DECISION.
- Applied as credit against outstanding; reduces net payable immediately.

### 14.2 Fee Write-off
- Outstanding fee deemed unrecoverable: student left without paying, untraceable, deceased
  without estate.
- Approval: Academic Director + Principal + Finance Head triple approval; documentation uploaded.
- Write-off ledger: separate from fee income ledger; tracked for statutory audit.
- Write-off register: maintained per Income Tax requirements; accessible to statutory auditor.

### 14.3 Waiver vs Write-off Distinction
| | Waiver | Write-off |
|---|---|---|
| Student status | Current enrolled student | Left / untraceable / deceased |
| Purpose | Goodwill / hardship | Bad debt recovery |
| Approval | Principal + Finance Head | AD + Principal + Finance Head |
| Ledger | Credit against outstanding | Write-off ledger (separate) |
| Tax treatment | Reduced income | Bad debt deduction |

### 14.4 Court Order / Legal Settlement
- Fee dispute reaches court: settlement amount entered by Platform Admin.
- Overrides normal workflow; court order reference + scanned PDF stored on CDN.
- Immutable record; no further modification without Platform Admin.

---

## 15. Education Loan Facilitation

### 15.1 Education Loan Support Letter
- System generates letter: institution confirms student admission, programme, total fee per
  year, course duration — on institution letterhead with Principal Aadhaar eSign.
- Issued in-app to student; stored on CDN; valid 3 months.
- Banks: SBI Vidyalakshmi, Punjab National Bank, Canara Bank, Bank of Baroda, HDFC, Axis
  (institution empanels banks in settings).

### 15.2 Loan Disbursement Tracking
- Bank disburses loan directly to institution: Finance team enters disbursement amount,
  bank reference, date.
- Credited to student's fee ledger with source = LOAN_DISBURSEMENT.
- Partial disbursement: accepted; balance outstanding remains.

### 15.3 Vidyalakshmi Portal
- Vidyalakshmi portal loan application reference linked to student profile.
- Disbursement status imported when available; reduces manual entry.

### 15.4 Fee Receipt for Loan Documentation
- Receipt generated in bank's required format (educational loan receipt format).
- Separate from standard fee receipt; includes: loan reference, student admission number,
  programme, academic year, amount, bank name.

---

## 16. Government Scheme Zero-Fee Enforcement

### 16.1 PMKVY 4.0
- Government-funded skill training: student fee = ZERO; training cost reimbursed by NSDC
  to institution.
- PMKVY enrolment flag (from student profile / Module 07) → system auto-zeroes ALL fee heads
  for that student.
- Reimbursement tracking: NSDC disbursement entered; grant amount tracked separately from
  student fee income.

### 16.2 DDU-GKY
- Rural skill training; government-funded; institution cannot charge student any fee.
- DDU-GKY beneficiary flag → all fees zeroed; same enforcement as PMKVY.

### 16.3 NAPS / NATS (Apprenticeship)
- Student receives stipend from employer during apprenticeship period.
- Institution fee during apprenticeship: zero or nominal (per MoU with employer).
- Stipend optionally offset against fee if institution so decides (institution policy).

### 16.4 Pradhan Mantri Kaushal Kendras (PMKK)
- Government-funded; zero student fee; grant tracking same as PMKVY.

### 16.5 State Government Schemes
- Kerala IT@School, Karnataka Mukhyamantri Kaushal Abhivrudhi Yojana, MP Mukhyamantri
  Kaushal Samvardhan Yojana, Rajasthan Kaushal Mission, AP Skill Development Corporation,
  TS TASK — each scheme tagged; fee auto-zeroed for enrolled students; reimbursement claim
  generated per state format.

### 16.6 Earn-While-You-Learn
- Student's work-linked stipend optionally offset against fee payable.
- Institution configures: YES (stipend reduces fee) or NO (stipend separate).
- If YES: stipend amount entered monthly → deducted from fee outstanding.

---

## 17. Fee Dispute Resolution

### 17.1 Dispute Workflow
```
Parent raises dispute in-app
→ selects instalment / fee head → enters reason
        ↓
Finance team reviews (3 working days SLA)
        ↓
Resolution decision:
  FAVOUR_PARENT → correction applied to ledger; revised demand notice
  FAVOUR_INSTITUTION → reason communicated to parent
  PARTIAL → partial correction applied
        ↓
If unresolved in 7 days → auto-escalated to Principal
        ↓
Parent notified of outcome
```

### 17.2 Dispute Categories
- Wrong amount charged / Already paid but not reflected / Concession not applied /
  Wrong late fee / Double charge / GST incorrectly applied / Scheme deduction not applied.

### 17.3 FRA Escalation Flag
- Parent notes intent to escalate to state FRA.
- Flag alerts institution management automatically.
- Document trail (all communications, corrections, decisions) preserved and exportable for
  FRA inspection.

---

## 18. Audit & Statutory Compliance

### 18.1 CA / Auditor Access Role
- Read-only access to fee structure, collection reports, GST data, concession log, write-off
  register.
- No edit rights; every CA access logged with timestamp, user, report accessed.
- Useful for statutory audit, GST audit, FRA inspection.

### 18.2 Annual Fee Structure Certification
- Principal digitally signs (Aadhaar eSign via DigiLocker API) the fee structure document
  each academic year.
- Signed PDF stored on CDN; submitted to FRA/AICTE as evidence of declared fee.

### 18.3 Statutory Audit Trail
- All changes: fee structure revisions, concession grants/expiry, waivers, write-offs,
  passthrough remittances — immutable log with timestamps.
- Retention: 7 years (Income Tax requirement + Companies Act for institutional trusts).

### 18.4 Income Tax Compliance
- Educational institution income exempt under IT Act §10(23C) if conditions met (not-for-profit,
  registered under relevant provision).
- System tracks: fee income per academic year; coaching income (taxable); passthrough
  remittances (not income).
- Corpus / capital receipts vs revenue receipts: separate ledger categories.
- Section 80G donations (if applicable): tracked separately; not in fee module.

---

## 19. Notification & Reminder Engine

### 19.1 Reminder Schedule (Configurable)
| Trigger | Channel | Recipient |
|---|---|---|
| T−15 days | Demand notice — FCM + SMS + email | Parent + Student (18+) |
| T−7 days | First reminder — FCM + SMS | Parent |
| T−3 days | Second reminder — FCM | Parent |
| T−0 (due date) | Final reminder — FCM + SMS | Parent |
| T+1 | Late fee warning — FCM + SMS | Parent |
| T+7 | Defaulter flag — internal alert | Class teacher + HOD (no external SMS) |
| T+30 | Escalation — internal | Finance Head + Principal |

### 19.2 Reminder Channels
- FCM (Module 35), SMS (Module 38), WhatsApp (Module 36 — if institution add-on enabled),
  email (Module 37).
- Do-Not-Disturb: no reminders between 9 PM and 7 AM (configurable window).

### 19.3 Reminder Templates
- SMS (160 chars): "Fee due: [Institution] | [Student] | ₹[Amount] | Due: [Date] | Pay via EduForge app."
- FCM: "Fee Reminder — ₹[X] due on [Date] for [Student]. Tap to pay."
- Email: full instalment breakdown + payment link + late fee notice.

### 19.4 Escalation (Internal Only)
- T+7: class teacher + HOD in-app alert: "5 students have outstanding fee >7 days."
- No SMS/WhatsApp to teacher — internal system alert only (avoids teacher embarrassment).

---

## 20. Integration Map

```
Module 07 (Student Enrolment)  → student category → fee structure auto-assignment
Module 09 (Parent) ────────────→ sibling detection → sibling discount auto-proposal
Module 21 (Results) ───────────→ merit rank → merit concession auto-trigger
Module 22 (Test Series) ───────→ test series fee as add-on subscription
Module 25 (Fee Collection) ────→ fee structure drives invoice + collection
Module 26 (Fee Defaulters) ────→ structure × collection = outstanding → defaulter
Module 28 (Hostel) ────────────→ hostel fee head auto-linked to room type
Module 29 (Transport) ─────────→ transport fee auto-linked to route/zone
Module 30 (Library) ───────────→ library deposit; no-dues clearance for refund
Module 31 (Admission CRM) ─────→ registration / prospectus fee at enquiry stage
Module 35/37/38 (Notifications)→ demand notice, reminder, revision notification
Module 39 (TC & Certificates) ─→ caution deposit refund on TC + no-dues
Module 50 (Subscriptions) ─────→ EduForge platform fee (separate from student fee)
NSP / State Scholarship Portal ─→ scholarship deduction linked to disbursement
DigiLocker ────────────────────→ Principal eSign for FRA certification
```

---

## 21. DB Schema

### Table: `fee_structures`
```
structure_id           UUID PRIMARY KEY
name                   VARCHAR(200)
academic_year_id       UUID
class_id               UUID NULL
programme_id           UUID NULL
branch_id              UUID NULL
student_category       VARCHAR(30)    -- DAY_SCHOLAR | HOSTELLER | NRI | MANAGEMENT | RTE |
                                      -- DISTANCE | EXCHANGE | LATERAL | GOVT_SCHEME
version                INT DEFAULT 1
effective_date         DATE
end_date               DATE NULL
status                 VARCHAR(20)    -- DRAFT | APPROVED | ACTIVE | ARCHIVED | FROZEN
fra_ceiling_ref        VARCHAR(200) NULL
aicte_approval_ref     VARCHAR(200) NULL
university_fee_ref     VARCHAR(200) NULL
approved_by            UUID NULL
principal_esign_cdn    VARCHAR(500) NULL
regulatory_mode        VARCHAR(20) DEFAULT 'SOFT_REGULATED'  -- HARD_REGULATED | SOFT_REGULATED | UNREGULATED
institution_type       VARCHAR(30)    -- SCHOOL | COLLEGE | COACHING | SKILL | GOVT | KVS | NVS
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
updated_at             TIMESTAMPTZ
```

### Table: `fee_heads`
```
head_id                UUID PRIMARY KEY
structure_id           UUID REFERENCES fee_structures(structure_id)
name                   VARCHAR(150)
description            TEXT NULL
head_category          VARCHAR(30)    -- ACADEMIC | INFRASTRUCTURE | WELFARE | FACILITY | DOCUMENT |
                                      -- PASSTHROUGH | LIABILITY | COACHING | CUSTOM
frequency              VARCHAR(20)    -- MONTHLY | QUARTERLY | HALF_YEARLY | ANNUAL | ONE_TIME | PER_SEMESTER
amount                 NUMERIC(10,2)
gst_exempt             BOOLEAN DEFAULT TRUE
gst_rate               NUMERIC(5,2) DEFAULT 0   -- 0 | 5 | 12 | 18
sac_code               VARCHAR(10) NULL
hsn_code               VARCHAR(10) NULL
is_refundable          BOOLEAN DEFAULT FALSE
refund_type            VARCHAR(20) NULL          -- FULLY | PARTIALLY | NON_REFUNDABLE
is_passthrough         BOOLEAN DEFAULT FALSE
passthrough_authority  VARCHAR(100) NULL         -- CBSE | NTA | STATE_BOARD | UNIVERSITY
is_liability           BOOLEAN DEFAULT FALSE     -- caution deposit, security deposit
is_optional            BOOLEAN DEFAULT FALSE     -- student opts in/out
sort_order             INT DEFAULT 0
active                 BOOLEAN DEFAULT TRUE
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `instalment_plans`
```
plan_id                UUID PRIMARY KEY
structure_id           UUID REFERENCES fee_structures(structure_id)
instalment_number      INT
due_date               DATE
amount                 NUMERIC(10,2)
grace_days             INT DEFAULT 7
fee_heads_included     JSONB          -- [{head_id, amount}]
tenant_id              UUID NOT NULL
```

### Table: `concessions`
```
concession_id          UUID PRIMARY KEY
student_id             UUID REFERENCES students(student_id)
structure_id           UUID REFERENCES fee_structures(structure_id)
concession_type        VARCHAR(40)    -- MERIT | NEED_BASED | SIBLING | STAFF_WARD | RTE | CWSN |
                                      -- NRI_WAIVER | SPORTS | NCC_NSS | GOVT_SCHOLARSHIP | ALUMNI_CHILD |
                                      -- GIRL_STUDENT | FIRST_GEN | MANAGEMENT | TRUSTEE
basis                  VARCHAR(10)    -- PERCENT | FLAT
value                  NUMERIC(8,2)   -- % or ₹ amount
applicable_heads       JSONB          -- [{head_id, basis, value}] per-head override
valid_from             DATE
valid_to               DATE NULL
stacking_priority      INT DEFAULT 1
govt_scheme_ref        VARCHAR(200) NULL
approval_chain         JSONB          -- [{role, staff_id, approved_at, remarks}]
status                 VARCHAR(20)    -- PENDING | APPROVED | ACTIVE | EXPIRED | REVOKED
auto_trigger           BOOLEAN DEFAULT FALSE
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
updated_at             TIMESTAMPTZ
```

### Table: `late_fee_config`
```
config_id              UUID PRIMARY KEY
structure_id           UUID REFERENCES fee_structures(structure_id)
head_id                UUID NULL      -- NULL = applies to all heads
grace_days             INT DEFAULT 7
late_fee_type          VARCHAR(20)    -- PER_DAY | PER_WEEK | PERCENT_PER_MONTH
late_fee_value         NUMERIC(8,2)
max_late_fee           NUMERIC(10,2)
gst_on_late_fee        BOOLEAN DEFAULT FALSE
exempt_categories      TEXT[]         -- ['RTE','CWSN','BEREAVEMENT','DISASTER']
tenant_id              UUID NOT NULL
```

### Table: `refund_policy`
```
policy_id              UUID PRIMARY KEY
head_id                UUID REFERENCES fee_heads(head_id)
refund_type            VARCHAR(20)    -- FULLY | PARTIALLY | NON_REFUNDABLE
schedule               JSONB          -- [{days_before_start, refund_percent}] for UGC
processing_fee_max     NUMERIC(8,2) DEFAULT 1000
ugc_compliant          BOOLEAN DEFAULT TRUE
tenant_id              UUID NOT NULL
```

### Table: `fee_revisions`
```
revision_id            UUID PRIMARY KEY
old_structure_id       UUID REFERENCES fee_structures(structure_id)
new_structure_id       UUID REFERENCES fee_structures(structure_id)
reason                 TEXT NOT NULL
proposed_by            UUID
reviewed_by            UUID NULL
approved_by            UUID NULL
effective_date         DATE
notification_sent      BOOLEAN DEFAULT FALSE
fra_check_result       JSONB          -- {status: PASS|WARN|BLOCK, details}
freeze_active          BOOLEAN DEFAULT FALSE
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `rte_reimbursement_claims`
```
claim_id               UUID PRIMARY KEY
academic_year_id       UUID
branch_id              UUID
rte_student_count      INT
govt_rate_per_student  NUMERIC(8,2)
total_claim            NUMERIC(12,2)
claim_period           VARCHAR(50)
submitted_date         DATE NULL
status                 VARCHAR(20)    -- DRAFT | SUBMITTED | ACKNOWLEDGED | REIMBURSED | REJECTED
deo_reference          VARCHAR(200) NULL
reimbursed_amount      NUMERIC(12,2) NULL
reimbursed_date        DATE NULL
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `fee_waivers`
```
waiver_id              UUID PRIMARY KEY
student_id             UUID
instalment_id          UUID NULL
head_id                UUID NULL      -- NULL = waiver on total outstanding
waiver_amount          NUMERIC(10,2)
waiver_type            VARCHAR(30)    -- GOODWILL | HARDSHIP | ADMIN_ERROR | MANAGEMENT | LEGAL
reason                 TEXT NOT NULL
approval_chain         JSONB
status                 VARCHAR(20)    -- PENDING | APPROVED | APPLIED | REJECTED
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `fee_writeoffs`
```
writeoff_id            UUID PRIMARY KEY
student_id             UUID
total_outstanding      NUMERIC(12,2)
writeoff_amount        NUMERIC(12,2)
reason                 TEXT NOT NULL
approval_chain         JSONB
court_order_ref        VARCHAR(200) NULL
court_order_cdn        VARCHAR(500) NULL
writeoff_date          DATE
status                 VARCHAR(20)    -- PENDING | APPROVED | WRITTEN_OFF
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `fee_disputes`
```
dispute_id             UUID PRIMARY KEY
student_id             UUID
instalment_id          UUID NULL
head_id                UUID NULL
dispute_category       VARCHAR(40)    -- WRONG_AMOUNT | NOT_REFLECTED | CONCESSION_MISSING |
                                      -- WRONG_LATE_FEE | DOUBLE_CHARGE | GST_ERROR | SCHEME_MISSING
description            TEXT
status                 VARCHAR(20)    -- OPEN | UNDER_REVIEW | RESOLVED | ESCALATED
resolution             VARCHAR(30) NULL  -- FAVOUR_PARENT | FAVOUR_INSTITUTION | PARTIAL
resolved_by            UUID NULL
resolution_note        TEXT NULL
resolution_date        TIMESTAMPTZ NULL
fra_escalation_flag    BOOLEAN DEFAULT FALSE
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `education_loan_tracking`
```
loan_id                UUID PRIMARY KEY
student_id             UUID
bank_name              VARCHAR(100)
loan_amount            NUMERIC(12,2)
disbursement_date      DATE NULL
disbursed_to           VARCHAR(20)    -- INSTITUTION | STUDENT
reference_number       VARCHAR(200)
vidyalakshmi_ref       VARCHAR(200) NULL
linked_academic_year   UUID
status                 VARCHAR(20)    -- SANCTIONED | PARTIALLY_DISBURSED | FULLY_DISBURSED | CLOSED
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `govt_scheme_tracking`
```
scheme_id              UUID PRIMARY KEY
student_id             UUID
academic_year_id       UUID
scheme_name            VARCHAR(150)
scheme_type            VARCHAR(30)    -- PMKVY | DDU_GKY | NAPS | NATS | PMKK | STATE_SCHEME | RTE | EWL
grant_amount           NUMERIC(12,2)
reimbursement_status   VARCHAR(20)    -- PENDING | CLAIMED | REIMBURSED
claim_reference        VARCHAR(200) NULL
reimbursed_amount      NUMERIC(12,2) NULL
reimbursed_date        DATE NULL
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `fee_reminder_log`
```
log_id                 UUID PRIMARY KEY
student_id             UUID
instalment_id          UUID
channel                VARCHAR(20)    -- FCM | SMS | WHATSAPP | EMAIL
reminder_type          VARCHAR(20)    -- T_MINUS_15 | T_MINUS_7 | T_MINUS_3 | DUE_DATE |
                                      -- LATE_FEE_WARNING | DEFAULTER_INTERNAL | ESCALATION
sent_at                TIMESTAMPTZ
status                 VARCHAR(20)    -- SENT | FAILED | ACKNOWLEDGED | SNOOZED
acknowledged_at        TIMESTAMPTZ NULL
snoozed_until          TIMESTAMPTZ NULL
tenant_id              UUID NOT NULL
```

---

## 22. Compliance Checklist

| Regulation / Authority | Compliance Point |
|---|---|
| CGST Act Schedule III | Core education services GST exempt; coaching 18% enforced |
| GST Invoice Rules 2017 Rule 46 | Sequential invoice number; GSTIN on taxable invoices |
| GSTR-1 | Monthly taxable receipt export in NIC GSTN schema |
| IT Act §10(23C) | Fee income categorised; exempt vs taxable tracked |
| IT Rule 114E (SFT) | Cash receipts >₹2L per student flagged; Form 61A data generated |
| RTE Act §12 | 25% free seats; tuition auto-zeroed; reimbursement claim generated |
| UGC Fee Refund Notification 2018 | Refund schedule enforced; institution cannot go stricter |
| AICTE Fee Regulation | Programme-wise ceiling check; alert/block on breach |
| State FRA (TN/MH/RJ/GJ/KA/AP/TS) | Ceiling stored; HARD/SOFT regulated mode; FRA report |
| Maharashtra Cap Fee Act 1987 | Capitation fee head blocked |
| RPWD Act 2016 | CWSN late fee exempt; CWSN flag auto-applies exemption |
| PMKVY 4.0 Guidelines | Student fee auto-zeroed; NSDC grant tracked |
| DDU-GKY Framework | Zero student fee enforced |
| Education Loan (IBA Guidelines) | Proforma invoice + loan letter in IBA-compatible format |
| Companies Act / Trust Act | 7-year audit trail retention; write-off register |
| DPDPA 2023 | Fee data shared with parent only; CA access logged; data minimisation |
