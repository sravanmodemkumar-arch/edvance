# EduForge — Group 10: Parents & Guardians (Standalone Group)

> Parents are not just sub-roles inside schools or coaching.
> A parent's child can be in a school + coaching + exam domain simultaneously.
> They need ONE unified parent profile across all their children's institutions.

---

## Why Parents Need Their Own Group

| Problem Without Standalone Group | Solution With Group 10 |
|---|---|
| Parent has child in school + coaching — must log in twice | One login — all children, all institutions |
| Parent of 3 children in 3 different schools — 3 portals | Single dashboard — all 3 children |
| Parent pays school fee + coaching fee separately | Unified fee view + payment from one screen |
| School sends WhatsApp, coaching sends SMS — fragmented | Single notification centre |
| Parent can't see child's mock test rank (coaching) from school portal | Unified performance view across all institutions |
| Guardian change requires update in every institution separately | Update once — syncs across all institutions |

---

## Parent Types — Detailed

| # | Parent Type | Access Scope | Notes |
|---|---|---|---|
| 1 | Father | Full parent access | Primary contact by default |
| 2 | Mother | Full parent access | Equal access as Father |
| 3 | Legal Guardian | Full parent access | When neither parent available |
| 4 | Grandparent (Guardian) | Full parent access | Common in rural — grandparent raises child |
| 5 | Elder Sibling (Guardian) | Full parent access | Orphan/single parent cases |
| 6 | Court-Appointed Guardian | Restricted + flagged | POCSO-sensitive — special handling |
| 7 | Adoptive Parent | Full parent access | Legal adoption documented |
| 8 | Foster Parent | Restricted — time-limited | Access tied to foster period |
| 9 | Emergency Contact Only | Notification only — no login | Receives alerts, cannot view records |
| 10 | NRI Parent | Full parent access | Overseas — time zone, WhatsApp priority |
| 11 | Divorced Parent — Custody | Per custody order | Platform enforces who sees what per court order |
| 12 | Divorced Parent — Non-Custody | Emergency contact only | Cannot view academic records without court order |

---

## System Access Levels — Parents

| Level | Label | Who |
|---|---|---|
| P0 | Emergency Alert Only | Emergency contact — receives WhatsApp/SMS, no login |
| P1 | View Only — Own Child | Standard parent — view attendance, marks, fee, timetable |
| P2 | View + Pay | Can view all + pay fees online via Razorpay |
| P3 | View + Pay + Communicate | Can also message class teacher, book PTM slot |
| P4 | Multi-Child Dashboard | Parent with 2+ children across institutions |
| P5 | Guardian Admin | Legal guardian — can update contact details, consent |

---

## Division A — What Parents Can See Per Institution

### From School Portal (Group 3)
| Feature | Father | Mother | Guardian | Emergency |
|---|---|---|---|---|
| Daily attendance | ✅ | ✅ | ✅ | ❌ |
| Exam marks / results | ✅ | ✅ | ✅ | ❌ |
| Fee statement + pay online | ✅ | ✅ | ✅ | ❌ |
| Timetable | ✅ | ✅ | ✅ | ❌ |
| Homework / notes | ✅ | ✅ | ✅ | ❌ |
| Welfare alerts | ✅ | ✅ | ✅ | ✅ (alert only) |
| Message class teacher | ✅ | ✅ | ✅ | ❌ |
| Book PTM slot | ✅ | ✅ | ✅ | ❌ |
| Hostel welfare events | ✅ (hosteler) | ✅ | ✅ | ✅ |
| Transport live tracking | ✅ | ✅ | ✅ | ❌ |
| TC / certificate download | ✅ | ✅ | ✅ | ❌ |

### From Coaching Portal (Group 5)
| Feature | Father | Mother | Guardian | Emergency |
|---|---|---|---|---|
| Batch attendance | ✅ | ✅ | ✅ | ❌ |
| Mock test rank / score | ✅ | ✅ | ✅ | ❌ |
| Fee statement + pay | ✅ | ✅ | ✅ | ❌ |
| Batch schedule | ✅ | ✅ | ✅ | ❌ |
| Performance analytics | ✅ | ✅ | ✅ | ❌ |
| Counsellor messages | ✅ | ✅ | ✅ | ❌ |

### From Exam Domain / TSP (Groups 6 & 7)
| Feature | Parent |
|---|---|
| Mock test attempts | ✅ (if minor) |
| Rank in national test | ✅ (if minor) |
| Subscription status | ✅ |
| Performance trends | ✅ (if minor) |

> Note: Once student turns 18, parent access is automatically restricted
> unless student explicitly grants continued access.

---

## Division B — Parent Communication Channels

| Channel | When Used | Who Triggers |
|---|---|---|
| WhatsApp | Attendance alert, results, fee due, welfare | School / Coaching / Platform |
| SMS | OTP, critical alerts, emergency | Platform (MSG91) |
| In-app notification | Fee reminder, PTM booking, timetable change | Institution |
| Email | Invoice, certificates, formal reports | Platform |
| Push notification | Mobile app — daily attendance, new marks | School / Coaching |

---

## Division C — Parent-Specific Roles in the Platform (12 roles)

| # | Role | Level | Linked To | Key Actions |
|---|---|---|---|---|
| 13 | Primary Parent — School Only | P2 | 1 school | View + pay school fee |
| 14 | Primary Parent — Coaching Only | P2 | 1 coaching | View + pay coaching fee |
| 15 | Primary Parent — Multi-Institution | P4 | School + coaching | Unified dashboard |
| 16 | Primary Parent — Exam Domain | P1 | Exam domain | View mock test performance |
| 17 | Primary Parent — All Platforms | P4 | School + coaching + domain | Full unified parent dashboard |
| 18 | Secondary Parent (Mother/Father) | P3 | Same as primary | Equal access as primary |
| 19 | Legal Guardian | P5 | Any institution | Can update consent, contact |
| 20 | Grandparent / Elder Sibling | P3 | Any institution | Same as secondary parent |
| 21 | NRI Parent | P3 | Any institution | All access — WhatsApp priority |
| 22 | Emergency Contact | P0 | Any institution | Alert only — no login |
| 23 | PTA Representative | P1 | School only | School analytics — shared by Principal |
| 24 | Parent — Fee Defaulter | P1 | Any | View only — pay button highlighted |

---

## Division D — Parent Journey & Lifecycle

```
Child enrolled in school
       │
       ▼
Parent receives WhatsApp OTP → Login to EduForge parent app
       │
       ▼
Sees unified dashboard:
  ├── Child 1 — XYZ School
  │     ├── Today's attendance ✅
  │     ├── Maths test: 87/100 (Class Rank: 3)
  │     ├── Fee due: Rs.12,500 → [Pay Now]
  │     └── Timetable tomorrow
  │
  ├── Child 1 — ABC Coaching (same child)
  │     ├── Last mock test: AIR 1,243
  │     ├── Weak area: Organic Chemistry
  │     └── Next test: Sunday 10 AM
  │
  └── Child 2 — PQR School (different child)
        ├── Absent today ⚠️
        ├── Fee overdue: Rs.8,000 → [Pay Now]
        └── PTM: Saturday 10 AM → [Book Slot]
       │
       ▼
Parent pays both fees in one session via Razorpay
       │
       ▼
Receives WhatsApp receipts for both
```

---

## Division E — Special Parent Scenarios (6 roles)

| # | Scenario | Platform Handling |
|---|---|---|
| 25 | Divorced — shared custody | Both parents see child — custody % not tracked |
| 26 | Divorced — sole custody | Only custodial parent gets access |
| 27 | Child turns 18 during academic year | Auto-notify parent → access reduces to P1 after consent |
| 28 | Parent deceased — guardian takes over | Institution updates guardian → access transfers |
| 29 | Court order — parent restricted | Flagged account — institution manually restricts |
| 30 | Minor marriage (rare edge case) | Treated as adult — student self-access granted |

---

## Full Role Count — Group 10

| Division | Total |
|---|---|
| A — Parent Types | 12 |
| B — Communication (channels, not roles) | — |
| C — Platform Roles | 12 |
| D — Lifecycle (journey, not roles) | — |
| E — Special Scenarios | 6 |
| **Total** | **30** |
