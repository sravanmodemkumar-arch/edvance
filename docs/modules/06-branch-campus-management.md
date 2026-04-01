# EduForge — Module 06: Branch & Campus Management

> Every institution on EduForge can have one or multiple branches and campuses.
> Each branch is independently managed — own principal, own admin, own facilities —
> while the group admin maintains a consolidated view across all branches.

---

## Branch vs Campus Distinction

| Term | Meaning | Example |
|---|---|---|
| Institution | Registered legal entity | DPS Society |
| Branch | Administrative unit — separate school/college under same group | DPS Dwarka, DPS RK Puram |
| Campus | Physical location of a branch | DPS Dwarka — Sector 10 building |
| Building | Structure within a campus | Block A, Block B, Science Block |
| Floor | Level within building | Ground Floor, First Floor |
| Room | Individual space | Room 101, Lab 3, Auditorium |

- A branch can have one or multiple campuses (main + sub-campus)
- Single campus institution = branch and campus are same
- Each branch independently managed — own principal, own admin
- Indian standard: CBSE / State Board affiliations issued per branch — not per group

---

## Branch Hierarchy

```
Institution Group (DPS Society)
       │
       ├── Branch 1 — DPS Dwarka
       │     ├── Main Campus — Sector 10
       │     │     ├── Block A (Building)
       │     │     │     ├── Ground Floor
       │     │     │     │     ├── Room 101 (Classroom)
       │     │     │     │     ├── Room 102 (Classroom)
       │     │     │     │     └── Lab 1 (Science Lab)
       │     │     │     └── First Floor
       │     │     └── Block B (Building)
       │     └── Sub Campus — Sector 23
       │
       ├── Branch 2 — DPS RK Puram
       │
       └── Branch 3 — DPS Noida
```

| Level | Who Manages | Indian Standard |
|---|---|---|
| Group | Group admin / Chairman | Trust / Society level |
| Branch | Branch Principal + Admin | CBSE affiliation per branch |
| Campus | Campus in-charge | Physical address per campus |
| Building | Admin | Block management |
| Room | Admin | Room registry |

---

## Branch Types

| # | Branch Type | Description | Indian Example |
|---|---|---|---|
| 1 | Main Campus | Primary branch — full facilities | DPS RK Puram main school |
| 2 | Satellite Campus | Secondary branch — same city | DPS Dwarka Sector 10 + Sector 23 |
| 3 | Extension Centre | Smaller outpost — limited courses | College extension centre in rural area |
| 4 | Study Centre | Distance education delivery point | IGNOU study centre |
| 5 | Training Centre | Skill / vocational training only | ITI trade training centre |
| 6 | Exam Centre | Only conducts exams — no teaching | Board registered exam centre |
| 7 | Research Centre | PG / PhD research facility | University research campus |
| 8 | Off-Campus Centre | University approved off-campus | UGC approved off-campus |

- Each type has different module requirements
- Exam centre type: only exam + attendance modules enabled
- Admin selects branch type at creation — affects available modules

---

## Branch Code

| Item | Details |
|---|---|
| Format | Institution code + Branch sequence number |
| Example | DPS-001 (main), DPS-002 (Dwarka), DPS-003 (Noida) |
| Auto-generated | System generates on branch creation — admin cannot change |
| Used in | Student ID, Staff ID, fee receipts, reports, hall tickets |
| Indian standard | Matches affiliation number pattern |
| Affiliation number | Admin enters official board/university affiliation number separately |
| Unique | No two branches can have same code — platform-wide |
| Immutable | Cannot change after first student enrolled |

---

## Branch Status Lifecycle

| Status | Trigger | Access |
|---|---|---|
| Pipeline | Branch approved — setup in progress | EduForge + group admin only |
| Active | Setup complete — classes running | Full access — all users |
| Under Construction | New building / renovation | Active + restricted areas marked |
| Temporarily Closed | Natural disaster, legal issue, renovation | Group admin + Principal — read only |
| Permanently Closed | Institution decision | No access — data archived |
| Suspended | Regulatory action (CBSE / State Board) | Group admin only — read only |
| Reactivated | After suspension / closure lifted | Full access restored |

- Status change: Group admin + Management approval
- Students + parents notified via in-app on any status change
- Suspended branch: board/university affiliation flagged in system

---

## Branch Capacity

| Item | Details |
|---|---|
| Max students | Per branch — per academic year |
| Max staff | Per branch |
| Max classrooms | Physical rooms available |
| Per class capacity | Max students per section |
| CBSE norm | Max 40 students per section — platform enforces if CBSE branch |
| State board norm | Varies by state — admin configures |
| Soft limit (90%) | Warning shown to branch admin |
| Hard limit | New admission blocked — admin notified |
| Capacity review | Annual — admin updates before new academic year |

---

## Branch Capacity Utilization

| Item | Details |
|---|---|
| Shown on | Group admin dashboard |
| Metrics | Students enrolled / max capacity — % utilization |
| Color indicator | Green (below 75%) / Yellow (75–90%) / Red (above 90%) |
| Room utilization | Occupied vs available rooms |
| Staff utilization | Current vs sanctioned strength |
| Generated by | Python analytics — real-time |
| Trend | Monthly utilization trend per branch |
| Decision support | Group admin uses to plan expansion |

---

## Physical Infrastructure Mapping

| Level | What is Mapped |
|---|---|
| Campus | Total area (sq ft), GPS coordinates, address |
| Building | Name, floors, construction year, type |
| Floor | Floor number, total rooms |
| Room | Room number, type, capacity, condition, facilities |
| Outdoor | Sports ground, parking, garden, playground |
| Utilities | Generator, water tank, canteen, library building |

### Room Types — Indian Standard

| Room Type | Examples |
|---|---|
| Classroom | Standard teaching room |
| Science Lab | Physics, Chemistry, Biology |
| Computer Lab | Desktop lab, programming lab |
| Language Lab | English / Hindi language lab |
| Smart Classroom | Projector, smart board, internet |
| Library | Reading room, book stacks |
| Auditorium | Assembly hall, seminar hall |
| Staff Room | Teachers common room |
| Principal Office | Administrative office |
| Medical Room | First aid, nurse room |
| Sports Room | Equipment storage |

---

## Room / Hall Registry

| Field | Details |
|---|---|
| Room number | Unique per building — e.g. A-101, B-204 |
| Building | Which block / building |
| Floor | Ground / 1st / 2nd etc. |
| Room type | From standard types above |
| Seating capacity | Max students |
| Current condition | Good / Needs Repair / Under Maintenance / Condemned |
| Facilities | AC, projector, smart board, CCTV, fan, whiteboard |
| Accessible | Wheelchair accessible — yes / no |
| Assigned to | Class / lab / office — current assignment |
| Available from | Date available if under maintenance |

- Admin manages room registry — Principal approves new room additions
- Room registry used by: timetable, exam hall allocation, room booking modules

### Room Condition Tracking

| Condition | Meaning |
|---|---|
| Good | Fully functional — no issues |
| Needs Repair | Minor issues — still usable |
| Under Maintenance | Blocked — not available |
| Condemned | Unsafe — permanently blocked until renovated |

- Condemned status: Principal approval required
- Full condition history per room — required for NAAC
- Alert: admin notified if repair pending beyond 7 days
- Condemned room: class auto-reassigned — admin gets alert

---

## Room Allocation

| Item | Details |
|---|---|
| Allocation | Admin assigns class + section to room for academic year |
| Example | Class 10-A → Room A-101, Class 10-B → Room A-102 |
| Timetable link | Room shown on timetable for each period |
| Conflict check | System blocks if same room assigned to two classes same period |
| Temporary swap | Teacher requests — admin approves |
| Exam period | Overridden by exam hall allocation |
| Maintenance | Admin must reassign if room under maintenance |
| Indian standard | One class = one home room — students stay, teachers move |

### Room Occupancy Real-Time

| Item | Details |
|---|---|
| View | Admin sees all rooms — occupied / free / maintenance |
| Color coding | Green (free) / Red (occupied) / Yellow (maintenance) |
| Source | Linked to timetable — current period |
| After hours | All rooms show free |
| Exam days | Shows exam hall allocation |
| View scope | Branch admin — own branch only / Group admin — all branches |

---

## Exam Hall Allocation

| Item | Details |
|---|---|
| Generation | Python auto-generates seating arrangement |
| Input | Exam name, eligible students, available rooms, room capacity |
| Indian standard | Students from same class NOT seated together — mixed seating |
| Seating order | Roll number order within mixed arrangement |
| Output | Room number + seat number per student — on hall ticket |
| Invigilator | Auto-assigned — one per 30 students (CBSE norm) |
| Spare seats | 10% spare per room — for late additions |
| Seating chart | Generated per room — invigilator carries it |
| Override | Admin manually changes seat — logged |

---

## Lab Scheduling

| Item | Details |
|---|---|
| Lab types | Science lab, computer lab, language lab |
| Scheduling | Admin assigns lab slots per class per subject — timetable linked |
| Conflict check | System blocks double booking |
| Lab capacity | May differ from classroom capacity |
| Lab teacher | Subject teacher + lab assistant both assigned |
| Practical exam | Lab booked exclusively during practical exam period |
| Maintenance slot | Admin blocks for cleaning / maintenance |
| Indian standard | CBSE — separate practical periods in timetable |
| Lab register | Each session logged — class, teacher, topic, date |

---

## Room Booking

| Item | Details |
|---|---|
| Who books | Any staff — requests room |
| Approval | Admin approves |
| Purpose | PTM, extra class, counselling, staff meeting, event, practice |
| Conflict check | System blocks if already booked or allocated |
| Duration | Start time + end time |
| Recurring | Can book recurring slot |
| Cancellation | Requester cancels — room freed immediately |
| View | Admin sees full room booking calendar per building |
| Notification | In-app on approval / rejection |

---

## Asset Management

| Item | Details |
|---|---|
| Asset types | Computer, projector, smart board, printer, AC, fan, furniture, lab equipment |
| Asset record | Asset ID, name, purchase date, warranty expiry, room, condition |
| Asset ID | Auto-generated — tagged physically on asset |
| Condition | Working / Needs Repair / Out of Order |
| Assignment | Asset assigned to specific room — tracked |
| Movement | Room change logged |
| Repair request | Staff raises — admin assigns to vendor |
| Warranty alert | System alerts admin 30 days before warranty expires |
| Indian standard | Required for NAAC / NABET audit — asset register mandatory |

### Smart Classroom Tracking

| Item | Details |
|---|---|
| Smart features | Smart board, projector, internet, speakers, visualiser, webcam |
| Registry | Each smart classroom listed — facilities tagged per room |
| Allocation | Preferred for tech-heavy subjects |
| Maintenance | Malfunction — repair request raised |
| Indian standard | CBSE ICT infrastructure requirement — documented for affiliation |
| Group report | Group admin sees smart classroom count per branch |

---

## Maintenance Scheduling

| Item | Details |
|---|---|
| Who schedules | Admin — Principal approves |
| Types | Annual painting, electrical work, plumbing, deep cleaning, AC servicing |
| Room blocked | Unavailable during maintenance |
| Class affected | Admin reassigns to another room |
| Duration | Start date + end date |
| Notification | Affected teachers notified in-app |
| Preferred time | Summer vacation — avoids disruption |
| Vendor | Name + contact logged |
| Completion | Admin marks complete — room available again |
| History | Full maintenance history per room — required for NAAC |

---

## Branch Operations

### Branch Opening Process

```
Step 1 — Admin requests new branch
  Name, type, location, campus address, GPS coordinates

Step 2 — Principal approves

Step 3 — Management final approval

Step 4 — System auto-provisions
  Branch code generated
  Infrastructure mapping ready
  Module enablement — inherits group settings

Step 5 — Admin configures
  Buildings, rooms, branding
  Staff and students added

Step 6 — Branch goes live
```

- EduForge not involved — fully internal process
- Affiliation number: admin enters separately
- Auto-provisioning: instant after Management approval

### Branch Closure Process

| Step | Action |
|---|---|
| 1 | Admin initiates — reason mandatory |
| 2 | Principal approves |
| 3 | Management final approval |
| 4 | Pre-closure checklist — pending fees, results, active students, staff contracts |
| 5 | All pending items cleared |
| 6 | Students transferred or TC issued |
| 7 | Staff transferred or relieved |
| 8 | Status → Permanently Closed |
| 9 | Data archived — 5 years accessible |

| Data Type | Retention |
|---|---|
| Student records | 5 years accessible |
| Staff records | Service certificates issued |
| Fee records | 7 years — GST compliance |
| Reversal | Cannot reopen — new branch creation needed |

### Branch Suspension

| Item | Details |
|---|---|
| Who initiates | Admin — Principal approves — Management confirms |
| Types | Renovation, legal dispute, natural disaster, regulatory action |
| Access | Group admin + Principal — read only |
| Fee cycle | Paused during suspension |
| Data | Fully preserved — no archival |
| Reactivation | Admin initiates — Principal + Management approve |

### Branch Reactivation

| Item | Details |
|---|---|
| Pre-checklist | Compliance clearance, inspection certificate, staff in place |
| Status | Temporarily Closed / Suspended → Active |
| Fee cycle | Resumes from reactivation date |
| Indian standard | Regulatory clearance from board/university before reopening |
| Notification | Parents notified via in-app |

### Branch Rename

| Item | Details |
|---|---|
| Approval | Principal + Management |
| Effect | Display name changes — branch code unchanged |
| Historical data | Audit log retains old name |
| ID cards | Re-issued on next renewal only |
| Subdomain | Unchanged |
| Indian standard | Common when schools rebrand |
| Notification | Staff + parents via in-app |

### Branch Merge

| Step | Action |
|---|---|
| 1 | Admin initiates — source + target branch defined |
| 2 | Principal approves |
| 3 | Management final approval |
| 4 | Pre-merge checklist — active exams, pending fees, contracts |
| 5 | Student records migrated to target branch |
| 6 | Staff reassigned to target branch |
| 7 | Historical data retained under source branch code — read only |
| 8 | Source branch → Permanently Closed |

### Branch Split

| Step | Action |
|---|---|
| 1 | Admin initiates — defines student/staff allocation |
| 2 | Principal approves |
| 3 | Management final approval |
| 4 | New branch auto-provisioned — new branch code generated |
| 5 | Students + staff allocated |
| 6 | Historical data stays with original branch |
| 7 | Original branch continues with remaining students |

---

## Student & Staff Management

### Student Branch Transfer

| Step | Action |
|---|---|
| 1 | Parent submits request — reason mandatory |
| 2 | Source branch Principal approves |
| 3 | Target branch Principal confirms seat availability |
| 4 | Management approves |
| 5 | Student record migrated |
| 6 | New roll number issued |
| 7 | Academic history carried forward |

| Item | Details |
|---|---|
| Fee | Pending fees cleared before transfer |
| Attendance % | Carried forward from source branch |
| ID card | New card with new branch code |
| Indian standard | No TC required within same group |

### Staff Branch Transfer

| Step | Action |
|---|---|
| 1 | Admin initiates — reason mandatory |
| 2 | Source branch Principal approves |
| 3 | Target branch Principal confirms vacancy |
| 4 | Management final approval |
| 5 | Record migrated — new employee ID issued |
| 6 | Service history preserved |

| Item | Details |
|---|---|
| Salary | Continues — payroll updated to target branch |
| BGV | No re-BGV required |
| Indian standard | Transfer order issued — stored in staff record |

### Visiting Faculty

| Item | Details |
|---|---|
| Definition | Teacher assigned to 2+ branches — different days |
| Assignment | Group admin assigns — both Principals approve |
| Timetable | Appears on both branch timetables |
| Salary | Single salary — allocated across branches by % |
| Travel allowance | Per institution policy — logged |
| Indian standard | Common in rural areas — one teacher covers multiple schools |
| Conflict check | Not scheduled at two branches same time |
| ID card | Single card — lists all branches |

### Branch-Level Backup Principal

| Item | Details |
|---|---|
| Designation | Vice Principal or Senior HOD |
| Who assigns | Group admin — Principal recommends |
| Approval | Management |
| Active when | Principal on leave / travel / emergency |
| Powers | Full Principal access during backup period |
| Audit | All actions logged separately |
| Indian standard | CBSE norm — designated in-charge mandatory at all times |

---

## Branch-Specific Admission Quota

| Item | Details |
|---|---|
| Set by | Admin — Principal + Management approves |
| Per class | Class 1: 80 seats (2 sections × 40) |
| Per course | B.Tech CSE: 60 seats, B.Tech ECE: 60 seats |
| CBSE norm | Max 40 per section, max 4 sections per class |
| Hard limit | Admissions blocked once quota reached |
| Waitlist | Admin enables — parents notified if seat opens |
| Reserved quota | SC/ST/OBC reservation % — per Indian law |
| Group view | Quota utilization across all branches |

---

## Branch Financial Management

### Branch-Level Fee Structure

| Item | Details |
|---|---|
| Independent | Each branch sets own fee |
| Example | Urban branch ₹80,000/yr, rural branch ₹65,000/yr |
| Approval | Principal + Management |
| Group view | Consolidated fee structures |
| Applies from | New academic year — no mid-year revision |

### Branch-Level Fee Collection

| Item | Details |
|---|---|
| Collection | Own payment gateway credentials per branch |
| Tracking | Transactions tagged to branch — separate ledger |
| GST | Each branch may have own GSTIN |
| Reconciliation | Daily per branch — admin reviews |
| Group view | Consolidated + branch-wise breakup |
| Indian standard | GST law — separate invoicing per registered branch |
| Audit | Immutable — 7 year retention |

### Branch-Level Payment Tracking

| Item | Details |
|---|---|
| Ledger | Separate per branch |
| Refunds | Tracked per branch — Principal approves |
| Group view | Consolidated + branch breakup |
| Audit | All transactions immutable — 7 year retention |

---

## Branch Infrastructure

### GPS Coordinates

| Item | Details |
|---|---|
| Fields | Latitude + longitude + full address |
| Used by | Transport module — bus routes, driver app |
| Parent app | Campus location on map |
| Multiple campuses | Each has own coordinates |
| Accuracy | Exact campus gate location |

### Campus Map

| Item | Details |
|---|---|
| Format | Image upload — floor plan or layout diagram |
| Content | Buildings, labs, library, sports ground, parking, gates |
| Emergency | Exit routes marked |
| Indian standard | Required for NAAC — campus documentation |

### Sub-Campus Relationship

| Item | Details |
|---|---|
| Definition | One branch — two physical locations |
| Example | College main campus + hostel campus 2 km away |
| Same branch code | Sub-campus linked to main |
| Transport | Shuttle between campuses tracked |
| Indian standard | Engineering colleges — theory at main, labs at sub-campus |

### Digital Infrastructure

| Item | Details |
|---|---|
| Internet | ISP name, bandwidth (Mbps), connection type per campus |
| WiFi zones | Coverage areas mapped — admin/library/classrooms/hostel |
| WiFi access | Staff WiFi separate from student WiFi |
| Student WiFi | Login with student credentials — bandwidth limited |
| Exam halls | WiFi disabled during exams |
| Server room | Location, UPS, cooling — noted per branch |
| CCTV | Camera count + coverage areas logged |
| Internet outage | Admin logs outages |
| Indian standard | CBSE ICT circular — campus WiFi recommended |

### Power Backup Tracking

| Item | Details |
|---|---|
| Types | Generator (KVA) + UPS (KVA) |
| Coverage | Which buildings covered |
| Fuel log | Generator fuel consumption — admin updates |
| Maintenance | Scheduled servicing logged |
| Exam halls | Power backup mandatory during exams |
| Indian standard | CBSE safety norm — uninterrupted power for exam halls |
| Alert | Admin notified if service overdue 30 days |

### Parking Management

| Item | Details |
|---|---|
| Zones | Staff / student / visitor / bus parking |
| Registration | Staff vehicles — number plate + owner name |
| Entry log | Vehicle entry/exit by security |
| Two-wheeler | Separate zone — common in Indian colleges |
| Indian standard | NAAC requirement — designated parking |

---

## Branch Facilities

### Canteen / Cafeteria Management

| Item | Details |
|---|---|
| Vendor registration | Name, contact, licence number |
| Menu | Weekly menu — visible to students + parents |
| FSSAI licence | Licence number + expiry — alert before expiry |
| Hygiene inspection | Date + result logged |
| Complaints | Students/parents raise — admin reviews |
| Indian standard | CBSE circular — no junk food, FSSAI mandatory |
| Renewal alert | 30 days before FSSAI expiry |

### Sports Facilities

| Item | Details |
|---|---|
| Facility types | Cricket ground, football field, basketball court, badminton, swimming pool, gym |
| Registry | Name, type, capacity, condition, indoor/outdoor |
| Scheduling | Sports period per class — timetable linked |
| Booking | Extra practice — admin approves |
| Inter-school | Facility booked for events |
| Indian standard | CBSE — minimum sports infrastructure for affiliation |
| Equipment | Tracked under asset management |

### Branch-Level Library

| Item | Details |
|---|---|
| Types | Own library / shared with twin branch / no library |
| Catalog | Books, journals, magazines tracked |
| Student access | Search + reserve online — collect at counter |
| Fine | Overdue fine — added to student fee account |
| Indian standard | CBSE — minimum books per student ratio required |

---

## Branch Compliance & Safety

### Compliance Status

| Compliance Item | Alert Threshold |
|---|---|
| Fire NOC | 30 days before expiry |
| Building completion certificate | On expiry |
| Affiliation certificate | 30 days before expiry |
| FSSAI licence | 30 days before expiry |
| Water quality certificate | 30 days before expiry |
| Electrical safety certificate | 30 days before expiry |
| POCSO compliance | Annual review |
| Insurance | 30 days before expiry |

- Expired: red flag on branch — Principal + Group admin alerted
- Indian standard: CBSE affiliation renewal requires all documents
- Retention: 10 years

### Branch-Level POCSO Officer

| Item | Details |
|---|---|
| Mandatory | Yes — POCSO Act 2012 |
| One per branch | Must be senior staff |
| Display | Name + contact on branch portal |
| Complaints | All child safety complaints routed here |
| Escalation | Branch → EduForge POCSO officer |
| Training record | Maintained in system |
| Annual review | Group admin confirms officer still in role |
| Indian standard | CBSE mandatory circular — all affiliated schools must comply |

### Branch Inspection Records

| Item | Details |
|---|---|
| Inspection types | NAAC, NABET, CBSE, State Board, UGC, Fire, Health |
| Record fields | Date, body, inspector, findings, grade, next due |
| Follow-up | Compliance actions tracked |
| Alert | 30 days before next inspection due |
| Indian standard | CBSE affiliation renewal requires inspection clearance |
| Retention | 10 years |

### Emergency Drill Records

| Item | Details |
|---|---|
| Drill types | Fire drill, earthquake drill, lockdown drill |
| Frequency | Minimum twice per year |
| Record fields | Date, type, duration, participants, observations |
| Evacuation plan | Linked to campus map |
| Indian standard | CBSE safety circular — drill records mandatory |
| Alert | Reminder if drill not conducted in 6 months |
| Retention | 5 years |

### Branch Emergency Contacts

| Item | Details |
|---|---|
| Internal | Principal, Vice Principal, Admin, Security in-charge |
| External | Police station, fire station, hospital — per campus |
| Visible to | All staff after login |
| Parent app | Emergency contact shown |
| Indian standard | CBSE safety circular — emergency register mandatory |

### Security Management

| Item | Details |
|---|---|
| Guard shifts | Morning / afternoon / night — per campus |
| Entry log | Every visitor, vendor, contractor logged |
| Student entry/exit | Barcode scan on ID card |
| Staff entry | Linked to attendance |
| After hours | Any entry → Principal notified |
| Indian standard | CBSE safety circular — security register mandatory |

---

## Branch Communication

### Branch-Specific Announcements

| Item | Details |
|---|---|
| Scope | Visible only to that branch |
| Approval | Principal approves before publishing |
| Group announcement | Group admin sends to all or selected branches |
| No cross-visibility | Branch A cannot see Branch B announcements |
| Channel | In-app only |
| Expiry | Auto-archived after set date |

### Branch Contact Details

| Field | Details |
|---|---|
| Phone numbers | Primary + secondary |
| Email | Branch official email |
| Address | Full postal address |
| Social media | Facebook, Instagram, YouTube, LinkedIn per branch |
| Fax | Optional — some government institutions |
| Visible to | Public — on institution homepage |

### Branch-Level Branding

| Item | Details |
|---|---|
| Group master | Logo, colors, fonts — fixed by group |
| Branch customization | Branch name display, tagline, homepage banner |
| Cannot change | Group logo, primary color, font |
| Lock | Group admin can lock all branding |
| Indian standard | Common in franchise schools — DPS branding standard |

---

## Branch Analytics & Reports

### Cross-Branch Consolidated Reports

| Report | Details |
|---|---|
| Student strength | Total enrolled per branch + group total |
| Attendance summary | Branch-wise daily + monthly % |
| Fee collection | Collected vs due per branch |
| Result summary | Pass % per branch per exam |
| Staff strength | Sanctioned vs actual |
| Defaulter summary | Fee defaulters per branch |
| Admission pipeline | Enquiries + admissions per branch |
| Compliance status | Per branch |

- Generated by Python — in-app only, no download

### Branch Performance Benchmarking

| KPI | Details |
|---|---|
| Attendance % | Branch-wise average |
| Fee collection % | Collected vs total due |
| Result % | Pass percentage |
| Admission conversion | Enquiries vs admissions |
| Capacity utilization | Enrolled vs max |
| Syllabus completion | % completed |

- Branches ranked by each KPI
- Group admin drill-down to full branch detail

### Inter-Branch Student Comparison

| Item | Details |
|---|---|
| Comparison | Same class/subject marks across branches |
| Example | Class 10 Maths avg — Branch A: 78%, Branch B: 65% |
| Privacy | Individual marks not shared — averages only |
| Indian standard | Common in DPS, KV groups — central academic monitoring |

---

## Special Branch Features

### Branch Expansion Tracking

| Stage | Details |
|---|---|
| Planned → Land Acquired → Construction → Fit-out → Ready → Active | Admin updates stage |
| Affiliation | Pending application status tracked |
| Staff pipeline | Pre-recruitment before branch opens |
| Indian standard | CBSE new affiliation — 2 year process |

### Twinning Branches

| Item | Details |
|---|---|
| Definition | Two branches sharing specific resources |
| Setup | Group admin — both Principals agree |
| Shared resources | Library, lab, sports ground, auditorium |
| Conflict check | No double booking across both branches |
| Indian standard | Common in group institutions sharing campus buildings |

### Guest Lectures / Visiting Experts

| Item | Details |
|---|---|
| Fields | Expert name, qualification, topic, date, class, duration |
| BGV | Basic ID verification — not full BGV |
| Gate pass | Visitor gate pass issued |
| Certificate | Appreciation letter — Python generates |
| Feedback | Students rate session |
| Indian standard | Required for NAAC — guest lecture log mandatory |

### Visiting Faculty

| Item | Details |
|---|---|
| Definition | Teacher assigned to 2+ branches |
| Conflict check | Not at two branches simultaneously |
| Salary | Single — allocated across branches by % |
| Indian standard | Common in rural India — one teacher covers multiple schools |

---

## Branch Audit Log

| Item | Details |
|---|---|
| What is logged | Status changes, room changes, capacity changes, compliance updates, transfers |
| Logged fields | Who, what, old value, new value, date/time, reason |
| Immutable | Cannot be edited or deleted |
| Visible to | Principal + Group admin + EduForge super-admin |
| Retention | Per criticality tiers — Module 04 |
| Change reason | Mandatory for critical changes |
