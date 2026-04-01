# I-11 — Contract Transport

> **URL:** `/school/transport/contracts/`
> **File:** `i-11-contract-transport.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Transport In-Charge (S3) — manage contracts · Administrative Officer (S3) — documentation · Accounts Officer (S3) — vendor payments · Principal (S6) — approve new contracts

---

## 1. Purpose

Many schools hire buses or vans from private operators instead of (or in addition to) owning their own fleet. Contract transport management covers:
- Vendor/operator contracts with terms, rates, and compliance requirements
- Hired vehicle documentation (PUC, insurance, fitness — same as owned fleet)
- Payment processing and invoice verification
- Ensuring hired operators meet the same safety standards as the school's own vehicles
- Route assignments for hired vehicles

Key regulatory context:
- **Supreme Court 2012 order:** All school buses — owned or hired — must comply with yellow colour, speed governor, GPS, CCTV, and driver BGV requirements
- **CBSE Affiliation Bye-Laws:** School is responsible for transport safety even if it outsources to a contractor; the school cannot shift liability to the operator
- **Motor Vehicles Act:** The hiring school is a "principal employer" and shares liability for accidents involving hired school transport

---

## 2. Page Layout

### 2.1 Header

```
Contract Transport Management                        [+ New Contract]  [Renewal Alerts]
Academic Year: [2026–27 ▼]

Active contracts: 3 operators  ·  6 hired vehicles
Monthly contract expenditure: ₹1,84,000
Contracts expiring in 60 days: 1 (Operator: Venkatesh Transport — expires 30 Apr 2026)
Document non-compliance: 0
```

### 2.2 Operator List

```
Operator               Vehicles  Routes   Monthly Rate   Contract Exp   Compliance  Status
Venkatesh Transport    2 buses   R03,R04  ₹62,000        30 Apr 2026    ✅ OK       ⚠️ Renew soon
Sri Balaji Tours       3 buses   R01,R02  ₹90,000        31 Oct 2026    ✅ OK       ✅ Active
Sai Travels            1 van     Staff    ₹32,000        30 Jun 2026    ⚠️ BGV      ⚠️ Non-compliant
```

---

## 3. Operator Contract Detail

```
Operator: Venkatesh Transport
Proprietor: Mr. Venkatesh Reddy
GST No.: 36AAAAA1234B1Z5
Contact: +91 9876-XXXXX  ·  Address: Dilsukhnagar, Hyderabad

Contract:
  Contract No.: CTRN/2526/003
  Signed: 1 May 2025
  Valid until: 30 April 2026  ⚠️ Renew before 30 April
  Routes covered: R03 (Dilsukhnagar), R04 (Vanasthalipuram)

Rate structure:
  R03: ₹28,000/month (30 students × ₹933 cost/student/month — school charges ₹1,600/student)
  R04: ₹34,000/month (55 students × ₹618 cost — school charges ₹1,667/student)
  Total: ₹62,000/month
  Escalation clause: ≤5% annual increase on renewal (agreed)

Contract terms:
  ✅ Operator provides fuel and driver
  ✅ School provides escort (female escort is school's own staff per CBSE mandate)
  ✅ Operator complies with all Supreme Court/CBSE bus requirements
  ✅ Operator provides driver with HMV license and BGV before first duty
  ✅ 15-day notice for route suspension or contract termination (either party)
  ✅ Performance penalty: ₹500/day for routes abandoned without 6-hour notice
  ✅ Insurance: Operator maintains own insurance; school is additional insured
  ✅ Sub-letting prohibited: Operator cannot sub-contract routes without school approval

Payment terms:
  Monthly invoice by 1st of month
  Payment by 10th of month
  GST applicable: ✅ 5% GST (SAC 996411 — passenger transport service)
  TDS: 2% (Section 194C — contractor payment)

Vehicles assigned:
  AP29GH3456 — Bus 40 seats → R03
  AP29IJ7890 — Bus 52 seats → R04
```

---

## 4. Hired Vehicle Compliance Tracking

```
Hired Vehicle Compliance — Venkatesh Transport

Vehicle AP29GH3456 (Route R03):
  Document           Expiry         Status     Action
  PUC               20 Mar 2026    ⚠️ EXPIRED  [Remind operator — ground vehicle]
  Insurance         31 Mar 2027    ✅ Valid    —
  Fitness Cert      30 Jun 2026    ✅ Valid    —
  School Bus Permit 30 Sep 2026    ✅ Valid    —
  Speed governor    Installed      ✅          Last calibration: Jan 2026
  GPS               Active         ✅          Device: GPS-BUS-003
  CCTV              2 cameras      ✅          Checked 15 Mar 2026

  Driver (AP29GH3456): Dinesh P.
  HMV License: AP3456EF7890 — valid until 20 Mar 2027 ✅
  BGV: ✅ Completed 15 Apr 2023 — next due Apr 2028
  Medical fitness: ✅ Feb 2026

⚠️ PUC EXPIRED — Vehicle AP29GH3456 is GROUNDED
  Operator notified: ✅ 21 Mar 2026 (automated expiry alert)
  Operator response: "Renewing today"
  School action: Route R03 suspended until PUC renewed and document uploaded
  [Upload renewed PUC]  [Clear grounding]

Vehicle AP29IJ7890 (Route R04):
  All documents: ✅ Valid
  Driver (Kishore R.): ✅ All documents valid
```

---

## 5. Add New Contract

```
[+ New Contract]

Operator details:
  Operator name: [________________________]
  Proprietor/Contact person: [________________________]
  GST Registration No.: [________________________]  [Verify GSTIN →]
  Address: [________________________]
  Phone: [________________________]

Vehicles to be hired (add each):
  Vehicle 1: Reg No. [AP29MN5678]
    Type: ● Bus (specify capacity: [52])  ○ Van/Mini-bus  ○ Car
    Documents: [Upload PUC] · Expiry [___]  [Upload Insurance] · Expiry [___]
               [Upload Fitness Cert] · Expiry [___]  [Upload Permit] · Expiry [___]
    Safety: ☑ Speed governor installed  ☑ GPS (Device ID: [___])  ☑ CCTV (2 cameras)

  Driver for this vehicle:
    Name: [____________]  License No.: [____________]  License Exp: [___]
    BGV status: ● BGV completed (upload certificate)  ○ BGV in process (BLOCKED — cannot deploy)

Contract terms:
  Routes: [R06 (new route) ▼]
  Monthly rate: ₹[_____]
  Start date: [___]  End date: [___]
  GST: ● 5% applicable  ○ Exempt (attach justification)
  TDS rate: 2% (Section 194C — auto-applied)

Approval required: Principal (S6) sign-off for new contracts
[Submit for Principal Approval]
```

---

## 6. Contract Invoice and Payment

```
Invoice Processing — Venkatesh Transport — April 2026

Invoice No.: VT/INV/2627/004
Invoice date: 1 April 2026
Due date: 10 April 2026

Invoice items:
  Route R03 (Dilsukhnagar): ₹28,000
  Route R04 (Vanasthalipuram): ₹34,000
  Sub-total: ₹62,000
  GST @ 5% (SAC 996411): ₹3,100
  Total: ₹65,100
  TDS @ 2% (Sec. 194C) deducted: ₹1,240
  Net payable by school: ₹63,860

Verification:
  Routes operated this month: ✅ R03 — 22 days  ✅ R04 — 22 days (full month)
  Penalty deductions (route abandonment): Nil
  Verified by Transport In-Charge: ✅ Ravi Sharma — 3 Apr 2026

Payment:
  Payment from: D-19 Vendor Payments module
  [Approve for payment — Accounts Officer]
  [Process payment — bank transfer / cheque]
  Payment ref: Will generate after Accounts Officer approval
```

---

## 7. Contract Renewal Workflow

```
Contract Renewal — Venkatesh Transport — Expiring 30 Apr 2026

Current rate: ₹62,000/month
Operator's renewal proposal: ₹65,000/month (4.8% increase)

Rate negotiation:
  CPI inflation (Mar 2026): 4.2%
  Fuel price increase (last 12 months): +6.5%
  Operator's ask of 4.8%: Within agreed escalation clause (≤5%) ✅

Transport In-Charge recommendation: Accept ₹65,000/month
Principal review: [Approve renewal]  [Counter-propose]  [Reject and re-tender]

If approved:
  New contract: 1 May 2026 to 30 April 2027
  Updated rate: ₹65,100/month (including GST consideration)

Documents to re-verify on renewal:
  ☑ All vehicle documents (PUC/insurance/fitness) — current
  ☑ Driver BGV and license — current
  ☑ Speed governor calibration certificate
  ☑ GPS device registration

[Generate renewal contract draft]  [Send for Principal approval]
```

---

## 8. Performance Monitoring

```
Operator Performance Report — 2025–26

Operator: Venkatesh Transport  ·  Routes R03, R04

On-time performance:
  Days routes completed on time: 196/218 (89.9%)
  Days with delays >15 min: 22
  Major delays (>30 min): 4 (all due to traffic — documented)

Breakdowns:
  Total breakdowns: 3 (I-08 incident records)
  Backup bus arranged within 1 hour: 3/3 ✅
  Routes abandoned (no backup): 0 ✅

Compliance:
  BGV violations (deploying unverified driver): 0 ✅
  Document expiry violations: 1 (PUC R03 — expired 3 days before renewal)
  Penalty applied: ₹500 × 3 days = ₹1,500 (deducted from March invoice)

Overall rating: ⭐⭐⭐⭐ (4/5) — Good operator, minor compliance lapse

[Generate performance report PDF]  [Attach to renewal review]
```

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/transport/contracts/` | Contract list |
| 2 | `POST` | `/api/v1/school/{id}/transport/contracts/` | Add new contract |
| 3 | `GET` | `/api/v1/school/{id}/transport/contracts/{contract_id}/` | Contract detail |
| 4 | `PATCH` | `/api/v1/school/{id}/transport/contracts/{contract_id}/renew/` | Renew contract |
| 5 | `GET` | `/api/v1/school/{id}/transport/contracts/{contract_id}/vehicles/` | Vehicles under contract |
| 6 | `POST` | `/api/v1/school/{id}/transport/contracts/{contract_id}/invoice/` | Log invoice |
| 7 | `GET` | `/api/v1/school/{id}/transport/contracts/compliance-alerts/` | Operator compliance issues |
| 8 | `GET` | `/api/v1/school/{id}/transport/contracts/{contract_id}/performance/` | Operator performance report |

---

## 10. Business Rules

- A hired vehicle cannot be deployed on any school route until all statutory documents (PUC, insurance, fitness certificate, school bus permit) are uploaded and verified; the system hard-blocks route assignment for non-compliant vehicles
- The school is legally responsible for student safety on hired transport; the contract cannot transfer this liability — the school must verify operator compliance actively, not just contractually
- Hired vehicle drivers must meet the same requirements as school-employed drivers (HMV license, BGV, annual medical fitness, POCSO awareness training); the operator is required to provide these documents; the school verifies before deployment
- Female escort on hired buses: CBSE mandate applies equally — the school provides the female escort (this cannot be outsourced to the operator because the escort submits attendance in EduForge I-05 and is accountable to the school)
- Contract payments are processed through D-19 (vendor payments); TDS at 2% under Section 194C is applied automatically and tracked for TDS returns
- GST input tax credit: If the school is registered for GST (some private schools may be for other services), the 5% GST on transport services paid to operators can be claimed as ITC; school's CA should advise — EduForge tracks GST paid but does not auto-claim ITC
- Operator performance rating feeds into contract renewal decision; an operator with repeated non-compliance (BGV violations, persistent document expiry) must be replaced

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
