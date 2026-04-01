# EduForge — Module 09: Parent & Guardian Management

> Parents and guardians are first-class citizens on EduForge — not an afterthought.
> One login covers all children across all institutions.
> Indian realities — joint families, NRI parents, court orders, illiterate parents,
> low-connectivity areas — all handled at the platform level.

---

## Parent Types — 12 Types

| # | Type | Access Level | Notes |
|---|---|---|---|
| 1 | Father | Full parent access | Primary contact by default |
| 2 | Mother | Full parent access | Equal access as Father |
| 3 | Legal Guardian | Full parent access | When neither parent available |
| 4 | Grandparent (Guardian) | Full parent access | Common in rural India — grandparent raises child |
| 5 | Elder Sibling (Guardian) | Full parent access | Orphan / single parent cases |
| 6 | Court-Appointed Guardian | Restricted + POCSO flagged | Special handling — court order enforced |
| 7 | Adoptive Parent | Full parent access | Legal adoption documented |
| 8 | Foster Parent | Restricted — time-limited | Access tied to foster period |
| 9 | Emergency Contact Only | Alert only — no login | Receives critical alerts, cannot view records |
| 10 | NRI Parent | Full parent access | Overseas — WhatsApp priority, timezone-aware |
| 11 | Divorced Parent — Custody | Per custody order | Platform enforces access per court order |
| 12 | Divorced Parent — Non-Custody | Emergency contact only | Cannot view academic records without court order |

---

## Parent Access Levels

| Level | Label | Who | Permissions |
|---|---|---|---|
| P0 | Emergency Alert Only | Emergency contact | Receives alerts — no login |
| P1 | View Only | Standard parent | View attendance, marks, fee, timetable |
| P2 | View + Pay | Fee-paying parent | All P1 + pay fees online |
| P3 | View + Pay + Communicate | Active parent | P2 + message teacher, book PTM |
| P4 | Multi-Child Dashboard | Parent with 2+ children | Unified view across all children/institutions |
| P5 | Guardian Admin | Legal guardian | Can update contact, consent, health info |

---

## Parent Account Creation

### Admin-Created (Default)

```
Step 1 — Student enrolled (Module 07)
       │
Step 2 — Admin enters parent details during enrolment
  Name, phone, email, relationship to student
       │
Step 3 — System creates parent account
  Username = phone number or email
  Password = auto-generated
       │
Step 4 — Credentials sent to parent via email
       │
Step 5 — Parent receives OTP on email — verifies account
       │
Step 6 — Parent sets own password on first login
       │
Step 7 — Parent linked to student — appears on dashboard
```

### Self-Registration (Optional — Institution Decides)

```
Step 1 — Parent visits institution portal
Step 2 — Enters student admission number + own phone/email
Step 3 — System verifies admission number exists
Step 4 — Email OTP sent — parent verifies
Step 5 — Admin approves link — Principal notified
Step 6 — Parent account activated
```

- Self-registration: institution can disable — admin-only creation then
- Phone verification: OTP to email (no SMS — as decided)
- Duplicate check: same phone/email not linked to multiple unrelated students

---

## Parent Profile — Complete Data Fields

### Personal Information

| Field | Required | Notes |
|---|---|---|
| Full name | Mandatory | As per Aadhaar preferred |
| Relationship to student | Mandatory | Father / Mother / Guardian / etc. |
| Date of birth | Optional | For identity verification |
| Gender | Optional | |
| Aadhaar number | Optional | For KYC, scholarship verification |
| PAN number | Optional | For fee receipts, income tax |
| Religion | Optional | |
| Occupation | Optional | Farmer / Govt / Private / Business / Self-employed / Daily wage / Unemployed |
| Annual income | Optional | For EWS / fee concession / scholarship eligibility |
| Education level | Optional | Illiterate / Primary / Secondary / Graduate / Post-graduate (NAAC data) |
| Social background | Optional | Urban / Rural / Tribal (NAAC requirement) |
| First generation parent | Optional | First in family with child in school — NAAC |

### Contact Information

| Field | Required | Notes |
|---|---|---|
| Primary mobile | Mandatory | WhatsApp also used if WhatsApp enabled |
| Secondary mobile | Optional | Alternate contact |
| Email address | Mandatory | OTP, formal communication |
| WhatsApp number | Optional | If different from primary mobile |
| NRI — overseas phone | If NRI | Country code + number |

### Address Details

| Field | Required | Notes |
|---|---|---|
| Permanent address | Mandatory | |
| Correspondence address | Optional | If different |
| City, district, state, PIN | Mandatory | |
| Country | Mandatory | India / Overseas for NRI |
| Overseas address | If NRI | Full overseas address |

### Financial Details

| Field | Required | Notes |
|---|---|---|
| Bank account number | Optional | For fee refunds |
| IFSC code | Optional | For refunds |
| Income certificate number | If EWS / concession | Govt issued |
| Scholarship application | Optional | Merit / income based |

---

## Parent-Student Linking

| Scenario | Handling |
|---|---|
| One child, one institution | Simple link — parent sees one child |
| One parent, multiple children, same institution | All children on one dashboard |
| One parent, multiple children, different institutions | Unified cross-institution dashboard (P4) |
| Two parents, one child | Both linked — independent accounts |
| Two parents, divorced — shared custody | Both linked — access per custody order |
| Two parents, divorced — sole custody | Only custodial parent linked — non-custodial as emergency only |
| Guardian (no parent) | Guardian linked as P5 |
| Multiple guardians, one student | Priority order set — primary + secondary |

### Linking Process

| Step | Action |
|---|---|
| 1 | Admin links parent to student at enrolment |
| 2 | Relationship confirmed — parent verifies via email OTP |
| 3 | Parent account activated |
| 4 | Parent sees student on dashboard |

### Unlinking

| Scenario | Process |
|---|---|
| Student exits (TC) | Parent access auto-deactivated |
| Guardian change | Old guardian unlinked — new guardian linked — Principal approves |
| Court order change | Admin updates per new order — Principal + Management approve |
| Temporary unlink | Admin blocks parent access — Principal approves |

---

## Multi-Institution Parent

| Item | Details |
|---|---|
| Child in school + coaching | Same parent account — both institutions visible |
| Different tenants | Cross-tenant parent view — read only per institution |
| Fee payment | Per institution separately — no cross-institution payment |
| Notifications | All institutions' notifications in one notification centre |
| Calendar | Each institution's calendar shown separately |
| Indian reality | Very common — school + coaching simultaneously |

---

## Parent Authentication

| Item | Details |
|---|---|
| Login | Phone number or email + password |
| OTP | Email OTP for critical actions |
| No TOTP | Not required for parents |
| No SMS OTP | Email only — as decided |
| 2FA | Not mandatory for parents |
| Device limit | No limit for parents — as decided |
| Session | 30-minute timeout for web / 8 hours for mobile app |
| Failed login | 5 attempts → account locked → email OTP to unlock |

---

## Parent Verification

| Item | Details |
|---|---|
| Phone verification | Email OTP at registration |
| Aadhaar verification | Optional — shown as verified badge if done |
| KYC | Not mandatory — EduForge super-admin approves if done |
| Annual data verification | Parent asked to confirm details each year |

---

## Parent Communication Preferences

### Channel Preferences

| Channel | Default | Parent Can Change |
|---|---|---|
| In-app notification | Always ON | Cannot turn off |
| Email | ON | Can opt out of non-critical |
| WhatsApp | ON (if institution has add-on) | Can opt out |
| Push notification | ON | Can turn off |

### Notification Threshold Settings

| Alert Type | Default Threshold | Parent Can Change |
|---|---|---|
| Attendance alert | Below 75% | Yes — can set 80% or 85% |
| Fee reminder | 7 days before due | Yes — can set 3 or 14 days |
| Result published | Immediate | Cannot change |
| Emergency closure | Immediate | Cannot change |
| Welfare alert | Immediate | Cannot change |

### Language Preference

| Item | Details |
|---|---|
| Default | English |
| Options | Hindi, Tamil, Telugu, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi |
| Saved | Per parent account |
| Notification language | Follows parent's language preference |

### Parent Progress Subscription

| Item | Details |
|---|---|
| Weekly summary | Parent opts in — receives weekly child performance summary |
| Daily attendance | Auto-sent each day after attendance marked |
| Monthly report | End of month summary — attendance %, pending fees, upcoming exams |

---

## Parent Consent Management — DPDPA 2023

| Consent Type | Who Gives | When | How |
|---|---|---|---|
| Data storage consent | Parent (for minor) | At account creation | Digital e-signature |
| Photo consent | Parent (for minor) | At account creation | Digital e-signature |
| Media / video consent | Parent (for minor) | At account creation | Digital e-signature |
| Online class recording consent | Parent (for minor) | At account creation | Digital e-signature |
| Third-party sharing consent | Parent (for minor) | At account creation | Digital e-signature |
| WhatsApp communication consent | Parent | At account creation | Checkbox |

### Consent Withdrawal

| Item | Details |
|---|---|
| Who can withdraw | Parent at any time |
| Process | Parent submits request via app → admin processes |
| Effect | Specific data use stopped from withdrawal date |
| Photo consent withdrawn | Student photos removed from public areas |
| Audit | Consent + withdrawal timestamped — immutable |

### Parent Acknowledgment

| Item | Details |
|---|---|
| When | Important circulars, fee revision, policy changes |
| How | Parent reads → taps Acknowledge button |
| Tracked | System records which parents acknowledged + timestamp |
| Reminder | In-app reminder to unacknowledged parents |
| Report | Admin sees acknowledgment % per notice |

---

## Parent Access for 18+ Students

| Item | Details |
|---|---|
| Trigger | Student turns 18 during academic year |
| Action | System auto-notifies parent — access review required |
| Student consent | Student must grant continued parent access |
| If consent given | Parent continues with same access level |
| If consent not given | Parent access reduced to P0 (emergency only) |
| Exception | Indian colleges — most allow parent access regardless of age |
| Institution control | Institution admin can override — allow full parent access for all ages |
| Competitive exams | No parent access (SSC, RRB, UPSC, JEE, NEET adults) |

---

## Special Parent / Guardian Scenarios

### Divorced Parents

| Scenario | Platform Handling |
|---|---|
| Shared custody | Both parents linked — both see child |
| Sole custody | Only custodial parent linked — other as P0 emergency |
| Court order received | Admin uploads court order note — enforces access |
| Custody change | New court order → admin updates — Principal approves |
| Conflict | Both parents trying to change child's institution → escalate to Principal |

### Deceased Parent

| Step | Action |
|---|---|
| 1 | Institution notified — admin marks parent as deceased |
| 2 | Guardian designation changed — new guardian assigned |
| 3 | New guardian linked to student — verification done |
| 4 | POCSO officer informed — welfare check initiated |
| 5 | Old parent account deactivated |

### Foster Parent

| Item | Details |
|---|---|
| Access | Tied to foster period — start date + end date |
| Auto-expiry | Access removed on foster period end date |
| Renewal | Admin extends if foster period extended |
| Records | Child's records not transferred — remain with institution |

### Court-Appointed Guardian

| Item | Details |
|---|---|
| Flag | Account marked POCSO-sensitive |
| POCSO officer | Informed at time of linking |
| Access | Per court order — admin configures |
| Document | Court order document reference noted |

### NRI Parent

| Item | Details |
|---|---|
| Timezone | Parent sets own timezone — notifications sent at appropriate time |
| WhatsApp | Priority channel — in-app secondary |
| Overseas address | Stored — fee receipts sent to overseas address |
| Emergency | NRI parent marked — local guardian also designated |
| Video PTM | Online PTM preferred — timezone accommodated |

### Grandparent / Elder Sibling as Guardian

| Item | Details |
|---|---|
| Common in | Rural India, tribal areas, migrant worker families |
| Access | Full parent access (P3/P5) |
| Simple UI | Platform shows simplified interface |
| Language | Regional language priority |
| Verification | Admin verifies relationship at enrolment |

### Stepparent

| Item | Details |
|---|---|
| Linked as | Secondary parent or guardian |
| Access | Full access if primary parent designates |
| Legal adoption | If legally adopted — treated as adoptive parent |
| Not adopted | Stepparent access requires biological parent consent |

### Single Parent Household

| Item | Details |
|---|---|
| One guardian | Only one parent linked — system accommodates |
| Emergency contact | Single parent designates alternate emergency contact |
| Communication | All communication to single parent |
| Verified | Admin marks single parent — no second parent required |

### Joint Family — Primary Contact Decision

| Item | Details |
|---|---|
| Common in India | Father, grandfather, uncle — multiple adults involved |
| Primary contact | Institution designates one person as primary |
| Secondary | Others as secondary or emergency contacts |
| Decision | Family decides — admin records |

---

## Illiterate Parent Handling

| Item | Details |
|---|---|
| UI | Simple icons — minimal text |
| Language | Regional language — auto-detected from device |
| Voice | Not in V1 — future consideration |
| Assisted | Field worker / teacher helps parent set up account |
| Offline | Key info cached — accessible without internet |
| WhatsApp | Primary channel — easier than app for some parents |

---

## Low-Connectivity Parent

| Item | Details |
|---|---|
| Offline support | Key pages cached — attendance, timetable, results viewable offline |
| Sync | Auto-syncs when connection returns |
| WhatsApp | Works on 2G — primary channel for low-connectivity areas |
| Lightweight app | Minimal data usage — optimized for slow connections |

---

## Parents Sharing One Phone

| Item | Details |
|---|---|
| Reality | Common in India — one smartphone per household |
| Handling | Both parents have separate accounts — same device |
| Login | Each logs in separately — sessions don't conflict |
| Notification | Both receive — whoever opens app sees their dashboard |
| No merge | Platform does not merge accounts — keeps separate records |

---

## Parent Academic Access

### Student Attendance

| Item | Details |
|---|---|
| View | Daily attendance — present / absent / late |
| Calendar view | Month-wise attendance calendar — green/red |
| % summary | Monthly and term attendance % |
| Alert | Threshold-based alert (configurable) |
| Multi-child | All children's attendance on one screen |

### Student Results & Marks

| Item | Details |
|---|---|
| View | Marks per subject per exam |
| Trend | Week-over-week improvement / decline |
| Class comparison | Child vs class average — anonymous |
| Weak subjects | Python analytics — identified weak areas |
| Report card | Shown as in-app page — no download |
| AI insights | Python-generated performance insights |

### Answer Script View

| Item | Details |
|---|---|
| When available | After results published — institution decides |
| Who can see | Student + parent |
| Duration | Available for 7 days after result |
| Re-evaluation | Parent can request re-evaluation — process in Module 21 |

### Syllabus Tracking

| Item | Details |
|---|---|
| View | % syllabus completed per subject |
| Teacher-marked | Teacher marks topic done — parent sees real-time |
| Purpose | Parent plans home study based on syllabus coverage |

### Homework & Assignments

| Item | Details |
|---|---|
| View | Pending + submitted + overdue homework |
| MCQ tests | Upcoming tests assigned by teacher |
| Reminder | Parent notified when new homework assigned |

### Teacher Remarks

| Item | Details |
|---|---|
| View | Teacher's written remarks about child's progress |
| Positive | Achievement, improvement notes |
| Concern | Academic / behavioral concern noted |
| Visible to | Parent + student — not other parents |

### Disciplinary Record

| Item | Details |
|---|---|
| View | If child has any warning, detention, suspension |
| Parent notified | Immediately on any disciplinary action |
| Context | Reason + action taken shown |
| Confidential | Not visible to other parents |

---

## Parent Financial Access

### Fee View

| Item | Details |
|---|---|
| Outstanding dues | Total pending per child per institution |
| Installment plan | All future due dates in one view |
| Multi-child | All children's fees on one screen |
| Sibling discount | Shown if applicable |
| Concession | Applied concession shown |

### Fee Payment

| Item | Details |
|---|---|
| Gateway | Institution's BYOG — Razorpay / PhonePe / PayU |
| Access | Login required — portal / app only |
| Per institution | One institution per payment session |
| Receipt | Email + PDF |
| History | All past payments in receipt archive |

### Fee Concession Application

| Step | Action |
|---|---|
| 1 | Parent applies online — reason + income details |
| 2 | Income certificate uploaded reference noted |
| 3 | Admin reviews — Principal approves |
| 4 | Concession applied to fee account |
| 5 | Parent notified |

### Scholarship Application

| Item | Details |
|---|---|
| Types | Government / merit / income based |
| Apply | Parent applies via portal |
| Documents | Income certificate, merit marks |
| Bank account | Parent enters student bank account for disbursement |
| Tracking | Status visible in parent app |

### Fee Refund Request

| Item | Details |
|---|---|
| When | On withdrawal, overpayment, policy change |
| Process | Parent submits request → admin processes → Principal approves |
| Bank | Refunded to parent bank account |
| Timeline | 7 working days |
| Tracking | Status visible in parent app |

---

## Parent Safety & Welfare

### Authorized Pickup List

| Item | Details |
|---|---|
| Who enters | Parent via app → admin confirms |
| Fields | Name, relationship, phone, photo (optional) |
| Purpose | Security checks before releasing child |
| Change | Parent requests → admin updates |
| Indian standard | Common in CBSE schools — child safety protocol |

### Unauthorized Pickup Alert

| Item | Details |
|---|---|
| Trigger | Person not on authorized list attempts to collect child |
| Action | Security raises alert → parent notified in-app immediately |
| Institution | Principal + admin notified simultaneously |
| Response | Parent confirms / denies authorization in real-time |

### Parent SOS Button

| Item | Details |
|---|---|
| Location | Prominent on parent app dashboard |
| Action | Sends emergency alert to institution — Principal + Admin |
| Purpose | Child safety concern, medical emergency, unreachable child |
| Response | Institution acknowledges within 5 minutes |
| Log | All SOS events logged — immutable |

### Parent POCSO Reporting

| Item | Details |
|---|---|
| Direct channel | Parent can report child safety concern directly |
| Routes to | Institution POCSO officer + EduForge POCSO officer |
| Anonymous | Option available |
| Mandatory follow-up | POCSO officer must respond within 24 hours |
| Indian standard | POCSO Act 2012 — direct reporting mechanism |

### Hostel Outing Permission

| Item | Details |
|---|---|
| Request | Hostel warden sends outing request to parent |
| Parent action | Approve / Deny in app |
| Time limit | Parent must respond within 2 hours |
| Default | If no response — warden decides per policy |
| Log | All permissions logged — date, time, destination |

### Hostel Leave Application

| Item | Details |
|---|---|
| Who initiates | Parent or student |
| Approval | Parent approves if student initiates — warden approves both |
| Dates | From date + to date + reason |
| Pickup | Parent confirms pickup details |
| Return | Student marks return — warden confirms |

---

## Parent Communication

### Parent-Teacher Messaging

| Item | Details |
|---|---|
| Channel | In-app messaging only |
| Who can message | Parent → Class teacher only |
| Not to | Individual subject teachers directly |
| Response time | Teacher responds within 24 hours |
| Escalate | If no response — message goes to HOD |
| Log | All messages logged — admin can view |
| Inappropriate | Admin can delete + warn |

### Parent-Admin Communication

| Item | Details |
|---|---|
| Purpose | Fee queries, document requests, profile updates |
| Channel | In-app messaging |
| Response time | Admin responds within 48 hours |

### Parent-Counsellor Chat

| Item | Details |
|---|---|
| Purpose | Student welfare discussion |
| Confidential | Chat not visible to other staff |
| Initiate | Parent or counsellor can start |
| Log | Maintained for 5 years — welfare record |

### Parent Complaint Mechanism

| Item | Details |
|---|---|
| Categories | Academic / Fee / Staff behavior / Facility / Safety |
| Submit | Via parent app |
| Routes to | Admin → HOD → Principal (escalation) |
| Timeline | 2 working days per level — auto-escalates |
| Status | Submitted / In Review / Resolved / Escalated |
| Anonymous | Option available |
| POCSO | Child safety complaints → direct to POCSO officer |

### Parent Escalation

| Level | Escalates To |
|---|---|
| L1 | Admin |
| L2 | HOD / Dean |
| L3 | Principal |
| L4 | Management |
| L5 | EduForge Customer Support |

### Parent Feedback About Institution

| Item | Details |
|---|---|
| Frequency | Once per term |
| Anonymous | Yes |
| Parameters | Teaching quality, communication, facilities, fee transparency |
| Visible to | Principal + Management |
| Indian standard | NAAC — parent satisfaction survey |

### Parent Poll / Survey

| Item | Details |
|---|---|
| Created by | Admin — Principal approves |
| Topics | PTM timing, holiday preference, event RSVP |
| Response | Parent responds in app |
| Results | Admin sees aggregated results |

### Parent Event RSVP

| Item | Details |
|---|---|
| Events | Annual day, sports day, parent orientation, PTM |
| How | Parent confirms attending via app |
| Admin | Sees expected headcount for event planning |
| Reminder | In-app reminder 2 days before event |

---

## PTA — Parent Teacher Association

| Item | Details |
|---|---|
| Representatives | Selected parents per class — admin assigns |
| Access | P1 level + school analytics shared by Principal |
| Meetings | Meeting dates on calendar |
| Role | Feedback channel between parents and institution |
| Indian standard | CBSE recommends active PTA — NAAC requirement |

---

## Parent Welfare Concern Flag

| Item | Details |
|---|---|
| Who flags | Parent flags concern about child |
| Reason | Bullying, health issue, stress, unsafe situation |
| Routes to | Counsellor + POCSO officer (if safety) |
| Response | Within 24 hours |
| Log | Confidential — 5 years retention |

---

## Parent Privacy Settings

| Item | Details |
|---|---|
| Control | Parent controls what teachers see about them |
| Hide | Occupation, income, religion — optional fields hidden |
| Always visible | Name, phone, relationship — cannot hide |
| Teacher view | Teacher sees only: name, relationship, contact — not financial details |

---

## Parent Account Management

### Account Deactivation

| Trigger | Action |
|---|---|
| Student exits (TC issued) | Parent access auto-removed after 30 days |
| All children exit | Parent account deactivated |
| Manual | Admin deactivates — Principal approves |

### Account Reactivation

| Trigger | Action |
|---|---|
| Student re-joins | Parent account reactivated |
| New child enrolled | Same parent account linked to new child |
| Process | Admin reactivates — email OTP re-verification |

### Account Merge (Duplicate Resolution)

| Item | Details |
|---|---|
| Detection | Same phone + same student = duplicate |
| Resolution | Admin merges — keeps more complete profile |
| Audit | Merge logged — original records preserved |

### Parent Session Management

| Item | Details |
|---|---|
| View | Parent sees all active sessions — device, location, time |
| Logout | Remote logout from specific device |
| Suspicious | Parent reports suspicious login — account locked |

### Parent Data Portability — DPDPA

| Item | Details |
|---|---|
| Right | Parent can request copy of their own data |
| Process | Submits request → admin generates → 72 hours |
| Format | Structured data view in app |

### Parent Account Deletion — DPDPA Right to Erasure

| Item | Details |
|---|---|
| Request | Parent submits deletion request |
| Condition | Only if student has exited institution |
| Process | Admin reviews → EduForge approves → data deleted |
| Retention | Some data retained for legal compliance (fee records 7 years) |
| Confirmation | Parent notified on completion |

---

## Parent Historical Records Access

| Item | Details |
|---|---|
| Previous years | Parent can view child's data from archived academic years |
| Duration | 5 years accessible |
| After 5 years | Cold storage — not accessible via app |
| TC'd students | Parent loses access 30 days after TC issued |

---

## Parent Notification History

| Item | Details |
|---|---|
| Retention | 90 days — as decided in Module 04 |
| Filter | By date, category, child |
| Mark read | Individual or all |
| Critical alerts | Retained separately — 1 year |

---

## Parent Identity for Child Pickup — Gate Security

| Item | Details |
|---|---|
| ID required | Parent shows government ID at gate |
| QR code | Parent app generates QR for gate scanner |
| Security | Scans QR — confirms authorized pickup |
| Log | Pickup logged — time, date, person |
| Indian standard | Common in CBSE schools — child release protocol |

---

## Parent Geo-Fencing Alert

| Item | Details |
|---|---|
| Trigger | School bus enters / exits geofenced zone |
| Parent notified | Child's bus approaching / departed school |
| Zone | Defined around school campus |
| Used with | Transport module (Module 29) |
| No extra cost | Uses driver's phone GPS — ₹0 additional cost |

---

## Parent Data Accuracy Verification — Annual

| Item | Details |
|---|---|
| Trigger | Start of new academic year |
| What verified | Phone, email, address, emergency contact, income info |
| How | Parent reviews pre-filled form → confirms or updates |
| Mandatory | Required before new year enrolment confirmed |
| Approval | Updates go to admin for confirmation |

---

## Parent Audit Log

| Item | Details |
|---|---|
| What is logged | Login, logout, fee payment, consent actions, messages, profile updates |
| Logged fields | Action, timestamp, device, IP |
| Immutable | Cannot be edited or deleted |
| Visible to | Admin + Principal + EduForge super-admin |
| Retention | Per criticality tiers — Module 04 |

---

## Parent Profile — DB Schema Reference

**platform.parents** (Central DB — cross-tenant)

| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| full_name | TEXT | |
| phone | TEXT | Primary contact |
| email | TEXT | |
| aadhaar_hash | TEXT | Encrypted — optional |
| pan_number | TEXT | Encrypted — optional |
| occupation | TEXT | |
| annual_income | NUMERIC | Nullable |
| education_level | TEXT | |
| social_background | TEXT | urban/rural/tribal |
| nri | BOOLEAN | |
| overseas_phone | TEXT | Nullable |
| bank_account | TEXT | Encrypted — nullable |
| ifsc_code | TEXT | Nullable |
| language_preference | TEXT | Default English |
| whatsapp_optin | BOOLEAN | Default true |
| status | TEXT | active/deactivated/blocked |
| created_at | TIMESTAMPTZ | |

**platform.parent_student_links** (Central DB)

| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| parent_id | UUID | |
| student_id | UUID | |
| tenant_id | UUID | Which institution |
| relationship | TEXT | father/mother/guardian/etc. |
| access_level | TEXT | P0/P1/P2/P3/P4/P5 |
| is_primary | BOOLEAN | Primary or secondary |
| custody_order | BOOLEAN | If court order involved |
| foster_end_date | DATE | Nullable |
| created_at | TIMESTAMPTZ | |
| deactivated_at | TIMESTAMPTZ | Nullable |
