# Module 29 — Transport & GPS Tracking

## 1. Purpose

Module 29 owns the complete student transport lifecycle within EduForge institutions — from fleet configuration and route design through live GPS tracking, student boarding, driver management, safety compliance, and fee integration. It serves schools, colleges, coaching centres, and polytechnics that operate their own fleet or contracted vehicles.

The module is designed against the Motor Vehicles Act 1988, MV Amendment 2019, CBSE transport safety guidelines, Supreme Court orders on school bus safety, FSSAI (for vehicle hygiene where refreshments are provided), and state RTO rules. It integrates with Module 07 (Student Profile), Module 24 (Fee Structure), Module 25 (Fee Collection), Module 26 (Fee Defaulters), Module 08 (Staff & BGV), Module 11 (Attendance), Module 35 (Notifications), and Module 42 (Audit Log).

---

## 2. Fleet Configuration & Vehicle Master

### 2.1 Vehicle Types

| Type | Notes |
|------|-------|
| School bus (yellow) | MV Act school bus permit required; yellow colour mandatory |
| Mini-van | Up to 12 seater; contract carriage permit |
| Tempo traveller | 13–20 seater; contract carriage permit |
| E-bus (electric) | Battery SOH monitoring; charging schedule |
| Staff transport car | Staff-only; separate route set |
| Ambulance | Medical college / hostel emergency use |

### 2.2 Vehicle Master Record

Each vehicle carries:

| Field | Details |
|-------|---------|
| Registration number | State + RTO + series + number (e.g., TS09UA1234) |
| Make, model, year | Manufacturer + model name + year of manufacture |
| Seating capacity | Per RC book; used for overloading check |
| Fuel type | Diesel / CNG / Petrol / Electric |
| Colour | Yellow (school bus MV Act requirement) |
| GPS device IMEI | Linked to SIM number + network operator |
| Odometer reading | Updated per trip; used for service scheduling |
| Assigned driver (primary) | Linked to driver profile |
| Assigned driver (backup) | Auto-activated when primary absent |
| Assigned conductor | Optional; linked to staff profile |
| Assigned route | Primary route; additional routes per shift configurable |

### 2.3 Document Register Per Vehicle

| Document | Frequency | Alert Days |
|----------|-----------|-----------|
| Registration Certificate (RC) | Lifetime / Transfer | — |
| Fitness Certificate (FC) | Annual | 90 / 60 / 30 / 7 |
| Insurance policy | Annual | 90 / 60 / 30 / 7 |
| Pollution Under Control (PUC) | Quarterly (diesel) / Annual (CNG) | 30 / 15 / 7 |
| School bus permit (Form 7B) | Annual or biennial (state-specific) | 90 / 60 / 30 |
| Contract carriage permit | 5-year; state RTO | 90 / 60 / 30 |
| Speed governor certificate | At fitment; re-certified after repair | — |
| CCTV installation certificate | At fitment | — |
| Fire extinguisher service | 6-monthly | 30 / 15 |

**Compliance lock**: a vehicle cannot be dispatched on any trip if FC, Insurance, or PUC is expired. System blocks trip assignment and alerts transport manager.

### 2.4 Safety Equipment Audit

Monthly audit checklist per vehicle:
- First aid kit: items present, none expired
- Fire extinguisher: pin intact, pressure gauge green
- Emergency exit hammer: present at marked location
- Seat belts: all student seats functional
- CCTV cameras: operational, recording
- Speed governor: sealed, set at ≤40 km/h
- Reflective strips: present on all four sides
- SCHOOL BUS lettering: visible front and rear
- Driver emergency contact number: displayed on vehicle exterior

Audit log: auditor name, date, pass/fail per item, corrective action raised.

---

## 3. Route & Stop Management

### 3.1 Route Master

| Field | Detail |
|-------|--------|
| Route ID | Auto-generated alphanumeric |
| Route name | Descriptive (e.g., "Kukatpally–Miyapur–Madhapur") |
| Shift | Morning / Afternoon / Evening / Night (coaching late) |
| Total distance (km) | Auto-computed from GPS coordinates of stops |
| Estimated duration | Computed from stop sequence + average speed |
| Capacity | Max students enrolled on route |
| Status | Active / Suspended / Holiday-suppressed |

### 3.2 Stop Sequence

Each route has an ordered list of stops:

| Field | Detail |
|-------|--------|
| Stop number | Sequence order (1 = first pickup) |
| Stop name | Human-readable name |
| Landmark | Adjacent reference point (e.g., "near HDFC Bank") |
| GPS coordinates | Latitude + longitude (used for geo-fence) |
| Expected arrival time | Morning pickup time / afternoon drop time |
| Stop type | Pickup-only / Drop-only / Both / Optional |

Stop geo-fence radius: 50 metres. When GPS device enters this radius, stop-arrival event fires → boarding scan window opens → parent ETA update sent.

### 3.3 Zone Mapping

Institution draws geographic service zones (polygon on map or pin-radius). Each zone served by one primary route. System checks student's home address against zones during transport enrolment. Dead zones (students > 3 km from any stop) are flagged to transport manager for route extension consideration.

### 3.4 Route Variants & Holiday Suppression

- Same route with different timings for different shifts (Shift A: 7:00 AM, Shift B: 9:00 AM) configured as route variants
- On declared holidays (from Module 05 academic calendar), all routes auto-suppressed
- Transport manager can reinstate specific routes for exam-only days
- Parent notified when route is suppressed or reinstated

### 3.5 Nearest Stop Suggestion

At student enrolment, system computes Haversine distance from student's home address to every stop on every active route. Top 3 nearest stops suggested to student/parent. Stop assignment confirmed by transport manager.

### 3.6 Route Consolidation Engine (Strategic Feature)

At each academic year start, after all students have enrolled:
- Algorithm ingests all enrolled students' home coordinates + stop locations
- Identifies routes with <60% utilisation
- Suggests merges: "Route A and Route B can be merged — 12 km saving, 0 students added >400m walk"
- Identifies stops with 0 enrolled students → candidate for removal
- Output: draft revised route plan → transport manager reviews → approves or discards

---

## 4. Student Transport Enrolment

### 4.1 Enrolment Flow

```
Student opts into transport (in-app during admission or separately)
  → Home address confirmed (GPS pin or manual entry)
  → Nearest stops shown → student selects preferred stop
  → Transport manager assigns stop (may override)
  → Route assigned based on stop → capacity check
  → If over-capacity → waitlist
  → Fee component created in Module 24
  → Transport ID card generated (QR code)
  → Parent notified of route + stop + driver details
```

### 4.2 Transport ID Card

- Student name, photo, class/batch, route name, stop name
- QR code (unique per student per academic year)
- Emergency contact number (parent)
- Bus number and driver name
- Valid from–to dates

Used for boarding scan (driver tablet / RFID reader at bus door).

### 4.3 Fee Slab Configuration

| Distance Slab | Monthly Rate |
|--------------|--------------|
| 0 – 5 km | Configured per institution (e.g., ₹600/month) |
| 5 – 10 km | (e.g., ₹900/month) |
| 10 – 15 km | (e.g., ₹1,200/month) |
| 15+ km | (e.g., ₹1,500/month) |

Distance calculated from student's assigned stop to institution gate (not home to school). Configurable per institution. Linked to Module 24 fee structure.

### 4.4 Special Fee Rules

| Rule | Detail |
|------|--------|
| Sibling discount | 2nd+ sibling on same route: configurable % discount |
| RTE free transport | Section 12(1)(c); zero-rated invoice; govt reimbursement tracked |
| Staff transport | Same route, different cost tier or free (per policy) |
| Annual pass discount | Pay 10 months, get 12 (configurable discount) |
| Mid-year opt-out | 30-day notice; prorated refund; Module 25 processes |

### 4.5 Annual Re-enrollment

Each academic year, all transport opt-ins require re-confirmation:
- Existing student: app notification to re-confirm or change stop
- Default: auto-renew on same stop if no action taken (configurable)
- New stop requests routed to transport manager for approval

---

## 5. GPS Tracking & Live Location

### 5.1 GPS Device Integration

EduForge connects to GPS tracking devices via:
- **REST polling**: API call every 30 seconds to device SIM data endpoint
- **MQTT push**: device publishes to topic; server subscribes (preferred for real-time)

Device payload includes: vehicle ID, timestamp, latitude, longitude, speed, ignition status, battery %, signal strength.

### 5.2 Live Tracking Dashboard (Transport Manager)

Single map view showing all active vehicles simultaneously:
- Vehicle icon with direction arrow
- Colour by status: Green (on-route) / Yellow (idle) / Red (speed violation or deviation) / Grey (offline)
- Click vehicle: current speed, driver name, route name, next stop, last event
- Filter by route, shift, status
- Trip list: all active trips with start time, current progress (stops completed / total)

### 5.3 Parent App — Live Tracking

Parents of transport-enrolled students see:
- Bus icon on map (moving in near-real-time; 30-second refresh)
- "Bus is X stops away" / "Bus arriving in ~N minutes"
- Last known stop reached + timestamp
- Driver name (contact via masked call button)
- Trip status: Not started / En route / Completed

Push notification triggers:
- Bus departs school/depot (trip started)
- Bus is 3 stops away from student's stop
- Bus arrived at student's stop
- Child boarded (morning) / Child dropped (afternoon)
- Trip completed

### 5.4 Geo-fence Events

| Geo-fence | Radius | Event Triggered |
|-----------|--------|----------------|
| School campus entry | 100 m | "Bus arrived at school" notification |
| School campus exit | 100 m | "Bus departed school" notification |
| Stop arrival | 50 m | Boarding scan window opened; parent ETA updated |
| Restricted zone | Custom | Alert to transport manager |

### 5.5 Alerts & Violations

| Alert | Threshold | Recipient |
|-------|-----------|-----------|
| Speed violation | > 40 km/h (school bus) | Transport manager + logged |
| Route deviation | > 500 m from planned route | Transport manager |
| Night movement | 10 PM – 5 AM | Principal + transport manager |
| Vehicle stopped >10 min mid-route | Configurable | Transport manager (possible breakdown) |
| GPS signal lost | > 5 minutes | Transport manager |
| Overloading | Boarders > vehicle capacity | Driver + transport manager; trip blocked |
| Geo-fence breach (restricted zone) | Custom polygon | Transport manager |

Speed violation log: driver ID, vehicle, location, speed recorded, timestamp. Cumulative violations feed driver performance score.

### 5.6 Driver Panic Button

Driver app has one-tap SOS:
- Alert sent to: transport manager + Principal + security room
- Alert contains: driver name, vehicle number, GPS location, timestamp
- Manager app shows response buttons: Responding / Calling Police / Sending Help
- Auto-escalates to Principal if no manager response in 5 minutes
- SOS event stored in incident log

### 5.7 Trip History & Replay

All GPS tracks stored for 180 days. Transport manager can:
- Select any vehicle + any past date → see full trip route on map
- Replay at 10×/20× speed with speed overlay
- See all stop arrival times vs scheduled times → on-time performance per stop
- Export trip report: stops, arrival times, boarding counts, speed violations

### 5.8 Predictive Late-Arrival Alert (Strategic Feature)

ML model trained on 90+ days of historical trip data:
- Features: time of day, day of week, stop sequence, distance remaining, historical average at this point
- Output: predicted arrival time at each future stop
- If predicted arrival > scheduled + 5 min → proactive push notification to all affected parents: "Bus running approximately N minutes late today"
- Model retrains weekly; accuracy improves over time
- Weather category tag (rainy / festival / exam day) as feature input

---

## 6. Student Boarding & Attendance

### 6.1 Boarding Scan Process

**Morning pickup:**
1. Driver arrives at stop → stop geo-fence fires → boarding window opens
2. Student presents QR code on student app → driver tablet scans
3. Boarding recorded: student ID + stop + timestamp + GPS coordinates
4. Parent notification: "Ravi has boarded the bus at Kukatpally Stop at 7:42 AM"
5. Driver proceeds to next stop

**Afternoon drop:**
1. Bus approaching drop zone → boarding/drop window opens
2. Driver taps student name as dropped → drop recorded
3. Parent notification: "Ravi has been dropped at Kukatpally Stop at 4:18 PM"

**RFID alternative:** Student RFID card tapped on reader at bus door; same flow.
**Manual fallback:** Driver marks boarding manually if scan fails; flagged for review.

### 6.2 No-Show Alerts

- Morning: if student not scanned at their stop by departure + 3 minutes → auto-alert to parent: "Ravi did not board the bus at Kukatpally Stop today"
- Afternoon: if student not dropped by expected time + 30 minutes → alert to parent + transport manager
- Consistent no-show (5+ consecutive days) → prompt transport manager to check opt-out status

### 6.3 Escort Requirement

For students below Class 3 or flagged as special-needs:
- Escort name list stored per student (parent, sibling, registered guardian)
- Driver must visually confirm escort at drop point before releasing child
- Driver taps "Escort confirmed" on app → logged with timestamp
- If no escort present at drop: driver must not release child → call parent → alert transport manager
- Unaccompanied minor drop incident: logged; escalated to Principal

### 6.4 Transport Attendance Report

- Per student: days boarded (morning) / days dropped (afternoon) / no-shows / days school open
- Per route: average utilisation per trip
- Monthly transport attendance summary exportable for fee verification
- Reconcile: students billed but consistently not boarding → opt-out conversation

### 6.5 Academic Attendance Integration

- If morning boarding scan confirmed but student absent in academic attendance (Module 11) → flag (possible truancy after boarding)
- If bus delay (GPS confirms bus arrived late) → academic late mark auto-excused for all students on that route

---

## 7. Driver & Conductor Management

### 7.1 Driver Profile

| Field | Detail |
|-------|--------|
| Name, photo | Personal details |
| Driving licence number | DL number; class (LMV/HMV); state RTO |
| DL expiry | Alert at 90/60/30 days |
| Licence classes held | Must hold HMV or PSV for school bus |
| Medical fitness certificate | Annual; CMV (Commercial Motor Vehicle) medical form |
| Police verification | Character certificate; renewed every 3 years |
| Date of joining | Employment start date |
| BGV status | Linked to Module 08 |

### 7.2 Mandatory Compliance for School Bus Drivers

Per MV Amendment 2019 and CBSE transport guidelines:
- Must hold valid HMV / PSV driving licence
- Minimum 5 years' driving experience
- No criminal record (police verification mandatory)
- Medical fitness certified annually by authorised doctor
- Must not be under influence of alcohol or drugs at any time (breathalyser check log)
- Trained in child safety, emergency evacuation, first aid

### 7.3 Driver Training Log

| Training | Frequency | Certificate Stored |
|----------|-----------|-------------------|
| Defensive driving course | Every 2 years | Yes |
| Child safety training | Annual | Yes |
| First aid certification | Every 3 years | Yes |
| Emergency evacuation drill | Annual | Yes |
| Anti-ragging sensitisation | Annual | Yes |
| Traffic rules refresher | Annual | Attendance log |

Certificate expiry tracked; alert 60/30 days before.

### 7.4 Driver Attendance & Backup

- Driver checks in via app before first trip of day (with GPS location stamp)
- Absent → backup driver auto-notified; route reassigned
- Parent notified: "Today's bus for your child's route will be operated by [Backup Driver Name]"
- Driver cannot start trip without completing in-app pre-trip checklist (tyres, brakes, lights, fuel, CCTV, first aid)

### 7.5 Breathalyser Test Log

- Random tests conducted by transport in-charge
- Date, time, driver, result (Pass/Fail), administered by
- Fail → driver immediately suspended from duty; Principal + HR notified
- Repeat fail → termination proceeding; Module 08 flag

### 7.6 Driver Performance Score

Monthly composite score:
- Speed violations count (40%)
- On-time performance (30%)
- Parent feedback rating average (20%)
- Vehicle incidents/damage (10%)

Score: 0–100. Published to transport manager. Top 3 drivers: incentive (configurable amount ₹500–₹1,000). Bottom 10%: mandatory refresher training.

### 7.7 Driver Fatigue Policy

- System tracks total trip hours per driver per day from trip log
- > 8 hours driving in a day → alert to transport manager; no new trip assignment
- Weekly: > 48 hours → mandatory rest day before next week
- Long-distance trips > 4 hours → co-driver mandatory (configurable)

### 7.8 Conductor Role

- Conductor profile mirrors driver profile (without DL requirements)
- Responsible for: stop management, boarding scan on driver behalf, student safety during journey
- Incident reporting via conductor app
- Conductor attendance tracked; replacement protocol same as driver

---

## 8. Safety & Compliance

### 8.1 Regulatory Compliance Matrix

| Regulation | Obligation | How Tracked |
|-----------|-----------|-------------|
| MV Act 1988 S. 66 | Contract carriage permit required | Permit in document register |
| MV Act 1988 S. 92 | School bus = yellow, special permit | Colour + permit stored |
| MV Amendment 2019 | Speed governor ≤ 40 km/h; CCTV; first aid | Monthly audit checklist |
| SC Order 2018 (Writ 13029/1985) | Seat belts in all school vehicles | Audit checklist |
| CBSE Circular F.CE/Transport/2017 | Driver police verification; medical; training | Driver profile + alerts |
| State Motor Vehicle Rules | State-specific school bus norms | State field per institution |
| National Road Safety Policy 2010 | Road safety training for students | Annual session logged |

### 8.2 CCTV in Vehicle

- Camera locations: entry door + rear cabin
- Footage retention: 30 days on device / 7 days backed up to cloud
- Access to footage: Principal, transport manager, police (with written request)
- CCTV operational check: part of pre-trip checklist (driver confirms working)
- CCTV failure: vehicle cannot operate school route until repaired

### 8.3 Overloading Prevention

- Enrolled student count per trip vs vehicle seating capacity
- If boarders expected to exceed capacity at any stop → route capacity warning raised
- Driver cannot mark boarding for students beyond capacity — app blocks + alert
- Emergency overloading override: transport manager authorises with reason; logged

### 8.4 Accident & Incident Management

**Accident log captures:**
- Date, time, location (GPS coordinates + address)
- Vehicle number, driver name
- Students on board (names auto-populated from boarding scan)
- Nature of accident (minor damage / injury / major / fatality)
- Injuries: student names, nature of injury
- Third party involved: vehicle number, contact
- FIR number (if filed)
- Insurance claim number
- Witnesses

**On accident:**
1. Driver triggers SOS / calls transport manager
2. All parents of students on that vehicle notified immediately
3. Medical assistance triggered (if injuries)
4. Principal + management notified
5. Insurance company informed (Module 25 / accounts)
6. RTO report (Form 54) where required

### 8.5 Child Safety Final Check

Before closing each trip, driver completes in-app "end of trip" checklist:
- All students dropped: Yes
- Bus checked for left-behind children: Yes
- Bus doors locked: Yes
- Engine off: Yes
- Fuel level noted: Yes

"Left child on bus" incident: immediately triggers SOS protocol + police notification.

---

## 9. Fee & Billing

### 9.1 Transport Fee Flow

Transport fee is a Module 24 fee component:
- Component: "Transport Fee — Route [Name]"
- Amount: distance slab rate × months enrolled
- Billing frequency: Monthly / Quarterly / Annual (per institution setting)
- Invoice generated by Module 25; collected through Module 25 payment flow

### 9.2 Prorated Billing

| Scenario | Billing Rule |
|----------|-------------|
| Joins on day 1–10 | Full month billed |
| Joins on day 11–20 | Half month billed (configurable) |
| Joins on day 21+ | Not billed for that month; next month onwards |
| Opts out (30-day notice) | Last full month after notice period |
| Mid-month exit (emergency) | Prorated to last day |

### 9.3 RTE Transport Waiver

- Students under RTE Section 12(1)(c) within 1–3 km: school provides free transport
- Zero-rated transport invoice created in Module 25
- Government reimbursement claim: per-student per-day reimbursement tracked
- Claim filing date + reimbursement receipt logged for reconciliation

### 9.4 Transport Fee Defaulter

- Outstanding > 30 days → flagged in Module 26 (Fee Defaulters)
- Unlike hostel: transport service may be suspended after 60 days of default (configurable; not applicable for RTE students)
- Suspension notice: 7-day prior notice to parent via Module 35
- Reinstatement: automatic on fee clearance; parent notified

### 9.5 Group/Staff Transport Billing

- Staff transport on institutional vehicle: cost allocation per department
- External group booking (sports trip, field trip): trip cost allocated to event budget
- Single trip invoice: generated with route, date, student count, driver, distance

---

## 10. Maintenance & Fleet Health

### 10.1 Preventive Maintenance Schedule

| Service | Trigger | Alert Before |
|---------|---------|-------------|
| Engine oil change | Every 5,000 km or 3 months | 500 km or 15 days |
| Oil filter change | Every 10,000 km | 500 km |
| Air filter | Every 20,000 km | 1,000 km |
| Tyre rotation | Every 10,000 km | 500 km |
| Brake inspection | Every 15,000 km | 500 km |
| Battery check (diesel) | Every 6 months | 30 days |
| Battery SOH (EV) | Monthly reading | Alert < 70% SOH |
| Annual fitness inspection | 45 days before FC expiry | 60/45/30 days |
| AC service | Every 6 months | 30 days |

Odometer reading updated by driver at end of each trip → system computes km since last service → triggers maintenance alert when threshold approached.

### 10.2 Repair Request Flow

Driver or transport manager raises repair request:
- Vehicle, category (Engine / Electrical / Tyres / Body / AC / CCTV / Other)
- Description; priority (Emergency / High / Medium / Low)
- Assigned to: in-house mechanic or authorised service centre
- SLA: Emergency = same day; High = 24 hours; Medium = 72 hours
- Status tracking: Raised → Assigned → In Workshop → Repaired → Tested → Closed
- Vehicle blocked from trips while in Emergency or High repair status
- Repair cost logged for fleet cost reporting

### 10.3 Tyre Management

- Each tyre has a record: position (FL/FR/RL/RR/Spare), brand, fitment date, tread depth at fitment
- Tread depth checked at each rotation; recorded
- Alert: tread depth < 2 mm → replacement triggered immediately
- Tyre age > 5 years → replacement regardless of tread (rubber degradation)
- Tyre change log: date, position, old tyre disposed, new tyre fitted

### 10.4 Spare Parts Inventory

Critical spares stocked in transport store:
- Engine belts, oil filters, air filters, spark plugs (petrol), glow plugs (diesel)
- Bulbs (headlamp, indicator, brake)
- Wiper blades, brake pads
- Minimum stock level: configurable; low-stock alert when below threshold
- Issue log: part issued, to which vehicle, for which repair, date

### 10.5 Vehicle Replacement Trigger

Vehicle flagged for replacement when:
- Age > 8 years from manufacture, OR
- Odometer > 4,00,000 km, OR
- 3 major repairs (engine / transmission) in any 12-month period, OR
- Failed fitness inspection twice consecutively

Replacement flag visible in fleet health dashboard; budget estimate auto-generated.

### 10.6 Fleet Utilisation Report

| Metric | Description |
|--------|-------------|
| Trips per vehicle per month | Active utilisation |
| Average occupancy % per route | Students boarded / capacity |
| km per vehicle per month | From odometer |
| Fuel cost per km per vehicle | Fill-ups ÷ km |
| Maintenance cost per km | Repair cost ÷ km |
| Vehicle downtime days | Days off-road for repairs |
| Cost per student per month | Total fleet cost ÷ enrolled students |

---

## 11. Parent & Student Experience

### 11.1 Parent App Transport Features

| Feature | Detail |
|---------|--------|
| Live bus map | Real-time vehicle position; 30-second refresh |
| ETA countdown | "Bus arriving in ~8 minutes" |
| Stop-level arrival notification | Push when bus 3 stops away |
| Boarding confirmation | Push when child scanned |
| Drop confirmation | Push when child dropped |
| Driver contact | Masked call button |
| Trip history | Last 30 days of boarding/drop records |
| Transport attendance | Monthly summary |
| Pass validity | Current pass dates + route details |
| Fee status | Outstanding + payment shortcut |
| Feedback | Rate last trip (1–5 stars) |

### 11.2 Driver Contact Masking

Parent app shows "Call Driver" button. Actual driver mobile number is not exposed. System routes call through a masked number (telephony integration) or displays institution transport office number. Driver gets an incoming call notification in driver app. This prevents direct driver–parent relationships bypassing school oversight.

### 11.3 ETA Accuracy & Refinement

- ETA computed from: current vehicle position → remaining stops → historical average time per stop segment
- Displayed as "~N minutes" (not exact time) to set appropriate expectations
- ETA accuracy tracked: predicted vs actual at each stop; accuracy % reported monthly
- Machine-learned correction applied after 90 days of data

### 11.4 Trip Cancellation & Substitute Notification

If bus breaks down mid-route or route cancelled:
1. Transport manager marks trip as cancelled/disrupted
2. All affected parents notified: "Route [Name] bus is unavailable today. Please arrange alternate transport. Apologies for the inconvenience."
3. If substitute vehicle arranged: "Substitute vehicle [Reg No] will complete the route. Estimated delay: N minutes."
4. SOS-triggered breakdown: auto-message sent; manual override for wording

### 11.5 Bus Buddy System

For students in Std 1–5 (or any student flagged as needing support):
- Senior student (Std 9–11) assigned as bus buddy
- Bus buddy name and photo visible to parent in app
- Bus buddy responsible for: seating, safety, drop-point confirmation, reporting issues
- Bus buddy recognition: certificate at end of year; extra-curricular credit

### 11.6 Safe Arrival Confirmation

Optional feature: after drop notification, parent taps "Safely Received" within 15 minutes. System tracks confirmation rate. If no confirmation received and it is first time → gentle reminder push. If parent has consistently not confirmed → wellbeing check flag raised (parent may not be receiving child).

### 11.7 Student Incident Report

Student (or parent) can report unsafe behaviour on bus:
- Anonymous option available
- Categories: Rash driving, Harassment by driver/conductor, Bullying by co-passenger, Safety equipment missing, Other
- Routed to: transport manager + Principal
- Response committed within 48 hours; resolution tracked
- Anonymous report: identity not revealed; reporter can check status via token

---

## 12. Emergency Re-routing (Strategic Feature)

### 12.1 Breakdown Detection

Trigger: GPS shows vehicle stopped > 10 minutes at a non-stop location during active trip.

Auto-actions:
1. Transport manager alerted: "Vehicle [No] on Route [Name] has been stationary for 10+ minutes near [Location]. Possible breakdown."
2. Manager app shows: current vehicle position, students on board, remaining stops, distance to depot

### 12.2 Re-routing Flow

Manager options in app:
1. **Dispatch substitute vehicle**: select available vehicle from depot list → assign to remaining stops → driver app updated → all affected parents notified of delay
2. **Mark trip as completed**: if breakdown after all students dropped → close trip
3. **Request parent pickup**: if no substitute available → parent notification with apology and refund trigger
4. **Call mechanic**: roadside assistance; trips blocked for vehicle

### 12.3 Parent Communication During Disruption

All parents of students on the disrupted vehicle receive:
- Immediate alert: "Bus [No] has stopped near [Location]. We are arranging alternate transport."
- Follow-up (within 15 minutes): ETA of substitute or pickup request
- Resolution confirmation: "All students have been safely transported. Apologies for the delay."

---

## 13. Regulatory Compliance Automation

### 13.1 Compliance Calendar

Auto-generated compliance calendar for all vehicles:

| Task | Due | Owner | Alert Days |
|------|-----|-------|-----------|
| FC renewal | Per vehicle | Transport manager | 90/60/30/7 |
| Insurance renewal | Per vehicle | Transport manager | 90/60/30/7 |
| PUC renewal | Per vehicle | Transport manager | 30/15/7 |
| Speed governor certification | After repair | Transport in-charge | — |
| Driver DL renewal | Per driver | Transport manager | 90/60/30 |
| Driver medical fitness | Annual | HR + Transport | 60/30 |
| Driver police verification | Every 3 years | HR | 90/60 |
| First aid kit audit | Monthly | Conductor | 7 days before |
| Fire extinguisher service | 6-monthly | Maintenance | 30/15 |
| CCTV check | Monthly | Driver + Transport | 7 days before |
| School bus permit | Annual/biennial | Transport manager | 90/60/30 |
| Annual fire drill (depot) | Annual | Transport manager | 30 days before |

Overdue items turn red in compliance dashboard; escalate to Principal if > 7 days overdue.

### 13.2 Annual Compliance Dashboard (Principal View)

Single-page view:
- Fleet total / FC valid % / Insurance valid % / PUC valid %
- Drivers: DL valid % / Police verification current % / Medical certificate current %
- Training: first aid certified % / child safety trained %
- Incidents YTD: accidents, speed violations, complaints filed
- On-time performance: last 30 days average across all routes

### 13.3 State-Specific RTO Rules

- State field per institution; state-specific norm overlay applied
- Examples: Maharashtra requires two attendants for school buses; Karnataka requires GPS + panic button; Delhi requires AC for school buses > 25 km route
- Rule set updatable by platform admin per state notification

---

## 14. Analytics & Reporting

### 14.1 Operational Reports

| Report | Frequency | Audience |
|--------|-----------|---------|
| Daily trip summary | Daily | Transport manager |
| On-time performance per route | Weekly | Transport manager + Principal |
| Speed violation log | Weekly | Transport manager |
| Driver performance scorecard | Monthly | Transport manager + HR |
| Student transport attendance | Monthly | Transport manager + Accounts |
| Fleet cost analysis | Monthly | Management |
| Maintenance pending list | Weekly | Maintenance supervisor |
| Compliance status report | Monthly | Principal |
| Parent feedback summary | Monthly | Transport manager |
| Annual fleet health report | Annually | Management |

### 14.2 On-Time Performance

Per route, per driver:
- Scheduled departure time vs actual departure
- Scheduled stop arrival vs actual arrival (per stop)
- School gate arrival vs scheduled
- % trips on time (within ±5 minutes)
- Average delay per route
- Delay cause analysis: traffic, breakdown, driver late, road closure

### 14.3 Route Efficiency

| Metric | Formula |
|--------|---------|
| Actual km per route vs planned | GPS distance ÷ planned distance |
| Fuel efficiency per route | Litres consumed ÷ km |
| Cost per km per vehicle | (Fuel + maintenance) ÷ km |
| Cost per student per month | Total route cost ÷ enrolled students |
| Carbon footprint | km × emission factor (CO₂ per km per fuel type) |

### 14.4 Carbon Footprint Report (Optional ESG)

- Diesel: 2.68 kg CO₂ per litre × litres consumed
- CNG: 2.04 kg CO₂ per litre equivalent
- Electric: state grid emission factor × kWh consumed
- Annual CO₂ per student transported; year-on-year trend
- Used for institution ESG reporting or NAAC sustainability criteria

---

## 15. Driver App Features

| Feature | Detail |
|---------|--------|
| Login | Driver ID + PIN |
| Today's trips | List of assigned trips with route, shift, start time |
| Pre-trip checklist | Mandatory before trip start |
| Live route map | Turn-by-turn navigation to each stop |
| Boarding list per stop | Expected students; scan or mark manually |
| Fuel log | Fill-up entry: litres, station, odometer |
| Odometer update | End of trip |
| Incident report | Category, description, photo (camera) |
| SOS button | One tap emergency |
| End of trip checklist | All students dropped, bus checked |
| Maintenance request | Raise from app |

Driver app works on low-end Android (Go edition compatible). Offline queue: boarding scans stored locally and synced when connectivity restored.

---

## 16. Integration Map

| Module | Integration |
|--------|------------|
| Module 07 — Student Profile | Student photo, home address, emergency contact, class/batch |
| Module 08 — Staff Management | Driver + conductor profile, BGV status |
| Module 11 — Attendance | Bus delay → late mark auto-excused; boarding scan optional input |
| Module 24 — Fee Structure | Transport fee component defined here |
| Module 25 — Fee Collection | Transport fee invoiced and collected |
| Module 26 — Fee Defaulters | Transport fee default flagged |
| Module 35 — Notifications | All parent/driver notifications dispatched through Module 35 |
| Module 41 — POCSO Compliance | Incidents involving minors in transport logged |
| Module 42 — DPDPA & Audit Log | GPS data access, student location logs audited |

---

## 17. Data Model (Key Tables)

```
transport_vehicles
  id, tenant_id, registration_no, make, model, year, fuel_type,
  seating_capacity, gps_device_imei, gps_sim_no, status,
  primary_driver_id, backup_driver_id, conductor_id,
  current_route_id, odometer_km, created_at

transport_vehicle_docs
  id, vehicle_id, doc_type, doc_number, issue_date, expiry_date,
  alert_90_sent, alert_60_sent, alert_30_sent, alert_7_sent, status

transport_routes
  id, tenant_id, name, shift, total_distance_km, est_duration_min,
  capacity, status, created_at

transport_route_stops
  id, route_id, sequence_no, stop_name, landmark, lat, lng,
  expected_arrival_time_morning, expected_arrival_time_afternoon,
  stop_type, geo_fence_radius_m

transport_student_enrolments
  id, student_id, route_id, stop_id, academic_year, distance_km,
  fee_slab, enrolled_on, opted_out_on, status, pass_number

transport_trips
  id, vehicle_id, route_id, driver_id, conductor_id, trip_date,
  shift, planned_start, actual_start, actual_end, status,
  total_students_expected, total_boarded, total_dropped

transport_boarding_log
  id, trip_id, student_id, stop_id, event_type, scanned_at,
  scan_method, gps_lat, gps_lng, parent_notified_at

transport_gps_log
  id, vehicle_id, timestamp, lat, lng, speed_kmph, ignition,
  battery_pct, signal_strength, trip_id

transport_gps_alerts
  id, vehicle_id, trip_id, alert_type, triggered_at, location_lat,
  location_lng, value_recorded, threshold, resolved_at, notified_to

transport_driver_profiles
  id, staff_id, dl_number, dl_class, dl_expiry, medical_cert_expiry,
  police_verification_date, police_verification_expiry,
  years_experience, performance_score, status

transport_driver_attendance
  id, driver_id, trip_date, checkin_time, checkin_lat, checkin_lng,
  status, backup_driver_id

transport_breathalyser_tests
  id, driver_id, test_date, result, administered_by, notes

transport_incidents
  id, vehicle_id, driver_id, incident_date, incident_type,
  location_lat, location_lng, location_address, students_on_board,
  injured_students, fir_number, insurance_claim_no, description,
  created_by, created_at

transport_maintenance_requests
  id, vehicle_id, raised_by, raise_date, category, description,
  priority, assigned_to, sla_due, resolved_at, cost, status

transport_fuel_log
  id, vehicle_id, driver_id, fill_date, litres, fuel_station,
  odometer_at_fill, cost_per_litre, total_cost

transport_tyre_log
  id, vehicle_id, position, brand, fitment_date, tread_depth_mm,
  last_rotation_date, last_check_date, status

transport_pre_trip_checklist
  id, trip_id, driver_id, checked_at, tyres_ok, brakes_ok,
  lights_ok, fuel_ok, cctv_ok, first_aid_ok, fire_ext_ok,
  seatbelts_ok, notes

transport_sos_events
  id, vehicle_id, driver_id, triggered_at, lat, lng,
  trip_id, alert_sent_to, manager_responded_at,
  resolution_type, students_on_board
```

---

## Cross-Module References

- **Module 07**: Student home address (GPS pin for nearest stop), emergency contacts, class/batch — read-only
- **Module 08**: Driver and conductor staff profiles, BGV status — read-only
- **Module 11**: Bus delay causes late academic mark to be auto-excused — event write
- **Module 24**: Transport fee component (distance slab, rate) defined there — read-only reference
- **Module 25**: Fee invoices and collection processed there — write via Module 25 API
- **Module 26**: Transport fee default (>30 days) event sent to Module 26 — event write
- **Module 35**: All parent/driver push notifications, SMS dispatched via Module 35 — write
- **Module 41**: Incidents involving minors in transport — write to Module 41 log
- **Module 42**: GPS location data access, boarding scans, incident logs all audited — write

---

*Module 29 complete. Next: Module 30 — Library Management.*
