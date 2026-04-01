# O-05 — Payroll & Compliance

**Route:** `GET /hr/payroll/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** Payroll & Compliance Executive (#105)
**Also sees:** HR Manager (#79) — full access + approval authority; Finance Manager (#69) — read-only payroll summary for P&L reconciliation (via cross-portal link from M-01)

---

## Purpose

Monthly payroll processing for 100–150 EduForge employees across multiple cities and states, combined with statutory compliance management (PF, ESI, PT, TDS, Form 16, LWF). The Payroll Exec runs the monthly cycle: pull attendance data → compute gross/net → apply statutory deductions → lock → submit for HR Manager approval → disburse. The Compliance tab tracks every statutory obligation with due dates, filing reference numbers, and challan uploads — ensuring no deadline is missed.

The payroll model handles: multi-state Professional Tax slabs, ESIC wage ceiling (₹21,000/month), PF voluntary contribution option, proration for mid-month joiners and leavers, and LOP deduction integration from attendance data.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Payroll runs list | `hr_payroll_run` ORDER BY month_year DESC | 5 min |
| Current run detail | `hr_payroll_run` JOIN `hr_payroll_slip` for current month | No cache |
| Payslip table | `hr_payroll_slip` JOIN `hr_employee` for selected run | No cache |
| Salary register | `hr_payroll_slip` JOIN `hr_employee` for selected month (all components) | No cache |
| Statutory filings | `hr_statutory_filing` ORDER BY due_date ASC | 5 min |
| Filing detail | `hr_statutory_filing` single row + documents | No cache |
| LOP inputs | `hr_attendance_record` + `hr_leave_request WHERE status='LOP_APPROVED'` for month | No cache |
| Analytics — payroll trend | `hr_payroll_run` last 12 months: total_gross, total_net, headcount | 30 min |
| Analytics — statutory timeline | `hr_statutory_filing` last 12 months by type | 30 min |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?tab` | `runs`, `salary_register`, `filings`, `analytics` | `runs` | Active section |
| `?month` | `YYYY-MM` | current month | Selects payroll run period |
| `?filing_type` | `pf_ecr`, `esi`, `pt_karnataka`, `pt_telangana`, `tds_24q`, `form_16`, `lwf`, `all` | `all` | Filter filings |
| `?filing_status` | `upcoming`, `in_progress`, `filed`, `overdue`, `all` | `all` | Filter by filing status |
| `?employee_id` | UUID | — | Jump to specific employee's payslip in salary register |
| `?export` | `salary_register_csv`, `payslip_pdf`, `pf_ecr_txt` | — | Export formats |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| Payroll runs list | `?part=runs_list` | Page load + tab click | `#o5-runs-list` |
| Run detail | `?part=run_detail&month={YYYY-MM}` | Run row click | `#o5-run-detail` |
| Payslip table | `?part=payslip_table&month={YYYY-MM}` | Run select + filter | `#o5-payslip-table` |
| Salary register | `?part=salary_register&month={YYYY-MM}` | Tab click | `#o5-salary-register` |
| Filings list | `?part=filings_list` | Tab click + filter | `#o5-filings-list` |
| Filing detail drawer | `?part=filing_drawer&id={id}` | Row click | `#o5-filing-drawer` |
| Payslip drawer | `?part=payslip_drawer&id={slip_id}` | Row click in salary register | `#o5-payslip-drawer` |
| Analytics charts | `?part=analytics` | Tab click | `#o5-analytics` |
| New run modal | `?part=new_run_modal&month={YYYY-MM}` | [Start Payroll Run] click | `#modal-container` |
| Approve run modal | `?part=approve_modal&run_id={id}` | [Approve Run] click (HR Mgr only) | `#modal-container` |
| New filing modal | `?part=new_filing_modal` | [+ Log Filing] click | `#modal-container` |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  Payroll & Compliance   Month: [March 2026 ▼]                        │
├──────────────────────────────────────────────────────────────────────┤
│  PAYROLL STATUS STRIP (current month's run status)                   │
├──────────────────────────────────────────────────────────────────────┤
│  [Payroll Runs] [Salary Register] [Statutory Filings] [Analytics]   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Payroll Status Strip

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ LOCKED       │ │ 112          │ │ ₹1,24,80,000 │ │ ₹1,08,22,000 │ │ 3 filings    │
│ March 2026   │ │ Employees    │ │ Total Gross  │ │ Total Net    │ │ due this     │
│ Payroll      │ │ Processed    │ │              │ │              │ │ month        │
│ [Approve →]  │ │              │ │ +₹3.2L vs    │ │              │ │ PF/ESI/TDS   │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

Run status badge colours:
- DRAFT (grey) → PROCESSING (blue spinning) → LOCKED (amber — awaiting approval) → APPROVED (teal) → DISBURSED (green)

[Approve →] visible to HR Manager (#79) only when status is LOCKED.

---

## Payroll Runs Tab

### Runs List

| Column | Description |
|---|---|
| Month | `MMM YYYY` |
| Status | Badge: DRAFT / PROCESSING / LOCKED / APPROVED / DISBURSED |
| Employees | Count of employees in this run |
| Total Gross | Sum of all gross salary in ₹ |
| Total Net | Sum of all net (take-home) in ₹ |
| Run By | Who processed the payroll |
| Approved By | HR Manager who approved |
| Disbursed At | Date of bank transfer / null if not yet disbursed |
| Actions | [View Details] [Download Salary Register] [···] |

### Run Detail Panel

Shown when a run is selected (right panel or full-width):

```
  March 2026 Payroll Run
  ─────────────────────────────────────────────────────────
  Status:         LOCKED (awaiting approval)
  Processed by:   Payroll Exec on 28 Mar 2026, 11:30 IST
  Employees:      112  (108 regular + 3 new joiners proration + 1 exit proration)
  ─────────────────────────────────────────────────────────
  Total Gross:    ₹1,24,80,000
  Total PF (EE):    ₹5,04,000   (12% of PF wages for 98 PF-eligible employees)
  Total PF (ER):    ₹5,04,000   (12% split: 3.67% PF + 8.33% EPS)
  Total ESIC (EE):  ₹0           (0 employees below ₹21,000 wage ceiling)
  Total PT:         ₹22,400      (112 employees × state slab)
  Total TDS Advance:₹4,12,000   (projected annual TDS / 12, adjusted for declarations)
  Total Deductions: ₹14,42,400
  Total Net:       ₹1,08,22,000 (Total Gross + ER PF - Deductions; ER PF is company cost not deducted from net)
  ─────────────────────────────────────────────────────────
  [Download Salary Register (CSV)]  [Download PF ECR File (.txt)]  [Download ESI Contribution File]
  [Approve Run] (HR Manager only)   [Unlock Run] (if HR Manager rejects — Payroll Exec can edit)
```

**Proration logic for new joiners and leavers:**

For employees with `join_date` or `last_working_date` within the month:
`prorated_days = working_days_present / total_working_days_in_month`
`prorated_gross = (monthly_gross × prorated_days)`
Working days = calendar days in month minus Sundays minus public holidays from `hr_attendance_record` holiday master.

**PF wage ceiling:** PF computed on a maximum wage of ₹15,000/month (current EPFO statutory wage ceiling). Employees can voluntarily contribute on full wages — stored as a flag in `hr_employee`.

**ESIC eligibility:** Employees with monthly gross ≤ ₹21,000 are ESIC-eligible. Employee contribution: 0.75%. Employer contribution: 3.25%. At typical EduForge salary bands (most roles > ₹21K/month), ESIC coverage is minimal — but interns and entry-level roles may be eligible.

### Start Payroll Run Modal

Payroll Exec initiates monthly run:

```
┌──────────────────────────────────────────────────────────────────┐
│  Start Payroll Run — April 2026                                  │
├──────────────────────────────────────────────────────────────────┤
│  Pay Period*          April 2026 (Apr 1 – Apr 30)                │
│  Pay Date*            [30 Apr 2026                ]               │
│  LOP Days (confirm)   Pulled from attendance: [View LOP list →]  │
│  New Joiners          3 employees (prorated)   [Review →]        │
│  Exits (F&F)          1 employee               [Review →]        │
│                                                                  │
│  ⚠ Salary revision for 2 employees pending (increments Mar 26)   │
│     [Review revisions before proceeding →]                       │
│                                                                  │
│  [Cancel]                          [Start Processing]            │
└──────────────────────────────────────────────────────────────────┘
```

On [Start Processing]: system sets `status='PROCESSING'`, runs the payroll computation asynchronously (Celery task). Once complete, transitions to `LOCKED`. Payroll Exec reviews individual slips, can make corrections (by unlocking individual rows), then re-locks and submits for HR Manager approval.

### Approve Payroll Modal (HR Manager only)

```
  Payroll Run: March 2026
  Total Net Payable: ₹1,08,22,000
  Employees: 112

  ⚠ I confirm that I have reviewed the salary register and
    authorise disbursement of ₹1,08,22,000 to employee bank
    accounts by 31 Mar 2026.

  [Cancel]                      [Approve & Authorise Disbursement]
```

On approval: `hr_payroll_run.status='APPROVED'`, `approved_by = HR Manager user_id`. Finance Manager (#69) notified via O-01 dashboard strip (for P&L entry).

---

## Salary Register Tab

Detailed per-employee payslip table for selected month.

### Salary Register Table

| Column | Description |
|---|---|
| Emp ID | EF-XXXX |
| Name | Employee name |
| Designation | |
| Basic | Basic salary component in ₹ |
| HRA | House Rent Allowance |
| Special Allowance | Flexible component |
| LTA | Leave Travel Allowance (monthly accrual) |
| Bonus | Variable/incentive (if applicable) |
| Gross | Total earnings |
| PF (EE) | Employee PF deduction |
| ESIC (EE) | Employee ESIC deduction (if applicable) |
| PT | Professional Tax |
| TDS | Advance TDS deduction |
| Other Ded. | Loan EMI, recovery etc. |
| LOP | Loss of Pay deduction (₹/day × LOP days) |
| Net Pay | Final take-home |
| Status | PROCESSED / PENDING / REVISED |
| Actions | [View Payslip] [Download PDF] |

Sortable by all columns. Search by name or employee ID. Export as CSV.

### Individual Payslip Drawer

```
  PAYSLIP — March 2026
  ─────────────────────────────────────────────────────────
  Employee:   Rohan Verma (EF-0047)
  Designation: Backend Engineer · Division C
  Work Location: Hyderabad · PT State: Telangana

  EARNINGS                        DEDUCTIONS
  ─────────────────────           ─────────────────────────
  Basic             ₹60,000      PF (Employee)    ₹1,800
  HRA               ₹24,000      PT (Telangana)   ₹200
  Special Allowance ₹30,000      TDS Advance      ₹8,400
  LTA (monthly)     ₹5,000       LOP (0 days)     ₹0
  ─────────────────             ─────────────────────────
  Gross Salary      ₹1,19,000    Total Deductions ₹10,400
                                Net Pay          ₹1,08,600
  ─────────────────────────────────────────────────────────
  PF Employer:      ₹1,800  (3.67% PF + 8.33% EPS on ₹15,000 ceiling)
  Total CTC Impact: ₹1,20,800 (Gross + Employer PF)

  [Download Payslip PDF]  [Email Payslip to Employee]
```

All payslip PDFs are KMS-encrypted at rest in Cloudflare R2. Employee self-serve payslip download available at `/hr/my-payslips/` (accessible by all employees, own slips only — not part of Division O access control).

---

## Statutory Filings Tab

### Filings Overview

```
  Upcoming this month:  3   |   Filed YTD: 18   |   Overdue: 0

  ☐ │ Filing Type │ Period │ Due Date │ Status │ Filed At │ Ref # │ Actions
```

| Column | Description |
|---|---|
| Filing Type | PF_ECR / ESI_RETURN / PT_CHALLAN / TDS_24Q / FORM_16 / LWF / TDS_DEPOSIT |
| Period | Month/quarter/year the filing covers |
| Due Date | Statutory deadline. Red if overdue or < 3 days. Amber if ≤ 7 days. |
| Status | UPCOMING / IN_PROGRESS / FILED / ACKNOWLEDGED / OVERDUE |
| Filed At | Date + time of submission |
| Ref # | Government portal acknowledgement number |
| Actions | [View] [Update Status] [Upload Challan] |

### Filing Detail Drawer

```
  PF ECR — March 2026
  ─────────────────────────────────────────────────────────
  Filing Type:    PF Electronic Challan cum Return (ECR)
  Portal:         EPFO Unified Portal (unifiedportal-emp.epfindia.gov.in)
  Period:         March 2026 (wages paid in March)
  Due Date:       15 April 2026 (statutory deadline)
  Status:         IN_PROGRESS

  Challan Summary:
    Employees covered:     98
    Total EE contribution: ₹1,76,400   (12% of capped wages)
    Total ER PF:           ₹64,680     (3.67% of capped wages)
    Total ER EPS:          ₹1,24,200   (8.33% of capped wages)
    Admin charges:         ₹8,820      (0.50% EDLI + 0.50% EPF admin)
    Total payable:         ₹3,74,100

  Documents:
    ○ ECR file (.txt)   [Download ECR File]  (generated from payroll run)
    ○ Challan (TRRN)    [Upload Challan]     (after EPFO portal payment)
    ○ Acknowledgement   [Upload ACK]

  Notes:
  "ECR file generated on 1 Apr. Will upload to EPFO portal by 12 Apr."

  [Mark as Filed]  [Upload Challan PDF]  [Add Note]  [Set Reminder]
```

**PF ECR File Generation:** The system generates the standard ECR 2.0 format `.txt` file from `hr_payroll_slip` data. File format: UAN, wage month, gross wages, EPF wages, EPS wages, EPF contribution, EPS contribution, EPF miscellaneous, NCP days (Non-Contribution Period days = LOP days). This file is uploaded directly to the EPFO Unified Portal.

**ESI Half-Yearly Return:** Covers April–September (due by 11 November) and October–March (due by 11 May). Generated from ESIC contribution data. Filed on ESIC portal (esic.in). Only relevant if any employees are below the ₹21,000 ESIC wage ceiling.

**PT Challan — Multi-State:**
- Telangana: ₹200/month for salaries > ₹15,000. Filed monthly. Portal: ctd.telangana.gov.in
- Karnataka: Slab-based (₹0 up to ₹14,999 / ₹150 for ₹15K–₹29,999 / ₹200 for ≥ ₹30,000). Filed monthly. Portal: ptax.kar.nic.in
- Annual return: 30 April each year for both states

**TDS on Salaries (Section 192):**
- TDS deposit: 7th of next month (e.g., March TDS deposited by 7 April)
- Quarterly return (Form 24Q): Due 31 July, 31 October, 31 January, 31 May
- TDS computation: based on projected annual income − declared deductions (80C, 80D, HRA, LTA) submitted by employees in December
- System stores `hr_employee.tds_declaration` (JSONB): 80C investments, 80D premium, declared HRA rent, LTA claims

**Form 16 Generation:**
- Annual; issued by 15 June after each financial year
- System generates Form 16 Part A (TDS summary from TRACES) + Part B (salary breakup from payslip data)
- PDF generated per employee, stored in R2, employee notified via email with download link
- Bulk generation: HR Manager clicks [Generate All Form 16s] → Celery task processes all employees for the FY

### Add Filing Log Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Log Statutory Filing                                            │
├──────────────────────────────────────────────────────────────────┤
│  Filing Type*    [PF ECR                              ▼]         │
│  Period*         [March 2026                          ]          │
│  Due Date*       [15 Apr 2026                         ]          │
│  Status*         [IN_PROGRESS                         ▼]         │
│  Reference No.   [                                    ]          │
│  Notes           [                                    ]          │
│  Upload Challan  [Choose file...                       ]         │
│                                                                  │
│  [Cancel]                                  [Save Filing Log]     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Analytics Tab

### Payroll Trend Chart

Line + bar chart — 12 months of payroll data.

- **Primary bars (grey-200):** Headcount per month
- **Secondary line (blue-500):** Total gross salary (₹, left Y-axis)
- **Tertiary line (green-400):** Total net salary (₹, left Y-axis)
- **Right Y-axis:** Headcount count (0–200)
- **X-axis:** month labels (MMM YY)
- **Hover tooltip:** month · headcount · gross · net · avg gross per employee · avg net per employee

### Compensation Distribution Chart

Box plot or violin chart (if data sufficient) — distribution of monthly gross salary across all active employees.

- Shows: min, Q1, median, Q3, max
- Breakdown by division (colour-coded)
- Shows outliers (extremely high or low salaries relative to peer group)
- **Visible to:** HR Manager (#79) only (sensitive compensation data)

### Statutory Filing Compliance Chart

Heatmap or status grid — 12 months × filing types.

```
              Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec
PF ECR         ✓    ✓    ✓    ···
ESI            ✓    ✓    ✓    ···
PT (TG)        ✓    ✓    ✓    ···
PT (KA)        ✓    ✓    ✓    ···
TDS Deposit    ✓    ✓    ✓    ···
24Q Return     —    —    ✓    ···   (quarterly, only one per quarter)
Form 16        —    —    —    ···
```

Green ✓ = FILED/ACKNOWLEDGED. Red ✗ = OVERDUE. Amber ⚠ = IN_PROGRESS. Grey — = not applicable in that month.

---

## Empty States

| Condition | Message |
|---|---|
| No payroll run for month | "No payroll run for [month]. [Start Payroll Run]" |
| No filings due | "No statutory filings due in the next 30 days." |
| No overdue filings | "All filings are up to date." with green shield |
| Form 16 not yet generated | "Form 16 for FY [year] not yet generated. [Generate All]" |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Payroll run started | "Payroll processing started for [month]. Estimated completion: 2–3 minutes." | Blue |
| Payroll locked | "[Month] payroll locked. Awaiting HR Manager approval." | Amber |
| Payroll approved | "[Month] payroll approved. Disbursement authorised." | Green |
| Filing marked as filed | "[Filing type] for [period] marked as FILED." | Green |
| Challan uploaded | "Challan uploaded for [filing type] — [period]." | Green |
| Form 16 generation started | "Form 16 generation started for FY [year]. [N] employees. Estimated: 5 minutes." | Blue |
| Form 16 ready | "Form 16 for [N] employees generated. Employees notified via email." | Green |
| Overdue filing detected | "⚠ [Filing type] for [period] is now overdue (due: [date])." | Red |

---

## Authorization

**Route guard:** `@division_o_payroll_required(allowed_roles=[79, 105])` applied to `PayrollView`. Finance Manager (#69) accesses payroll summary via a cross-portal read-only API endpoint used by M-01 Finance Dashboard — not direct portal access.

| Scenario | Behaviour |
|---|---|
| [Approve Run] | HR Manager (#79) only; Payroll Exec (#105) sees disabled button with tooltip |
| Compensation Distribution chart | HR Manager (#79) only; Payroll Exec (#105) does not see this chart |
| [Generate All Form 16s] | HR Manager (#79) only |
| Export salary register CSV | Both HR Manager and Payroll Exec |
| Finance Manager (#69) cross-link | Read-only API returns: month, headcount, total_gross, total_net, status — no individual-level data |

---

## Salary Revision Workflow (Post-Calibration)

**Triggered by O-07 performance calibration lock.** When HRBP locks calibration and HR Manager approves increments in O-07, this page receives the pending revisions.

**How Payroll Exec sees pending revisions:**

In the Payroll Runs tab, before starting a new payroll run, a prominent alert shows:

```
  ⚠ 14 salary revisions pending for April 2026 payroll
  ─────────────────────────────────────────────────────────────
  Employee              Old CTC          New CTC          Effective
  Rohan V.    (Div C)   ₹14,40,000 p.a.  ₹16,80,000 p.a.  1 Apr 2026
  Priya S.    (Div D)   ₹12,00,000 p.a.  ₹13,44,000 p.a.  1 Apr 2026
  Kavya R.    (Div I)   ₹10,80,000 p.a.  ₹11,88,000 p.a.  1 Apr 2026
  ... 11 more
  [Review All Revisions]   [Apply to Next Payroll Run]
```

**[Apply to Next Payroll Run]:** Updates `hr_employee.ctc` and `hr_employee.grade` for each employee with approved revision. Logs to `hr_salary_revision_history` with `revision_type='ANNUAL_INCREMENT'`, `effective_date`, `source_cycle_id`. On confirm: "14 salary revisions applied. April 2026 payroll run will use revised CTCs." Payroll run auto-picks up new CTC for affected employees.

**Mid-month revision edge case:** If revision is approved on, say, 25 March for effective date 25 March (correction or joining scenario), the current month's payroll (March) is either:
- Already DISBURSED: revision takes effect next month; no retroactive adjustment unless HR Manager explicitly creates a [Supplementary Payroll Run] (available via [···] menu on run, HR Manager only)
- LOCKED or PROCESSING: HR Manager can unlock the run, Payroll Exec re-processes with new CTC, re-locks and re-submits for approval

**LOP Calculation Edge Cases:**

- **Second Saturday:** EduForge follows 5-day work week (Mon–Fri). Saturdays are non-working — they count as weekends (same as Sunday) for LOP calculation. No "second Saturday is working" variant.
- **Public holiday on Sunday:** If a national holiday falls on Sunday, EduForge policy is NO compensatory holiday (holiday is on a non-working day and does not carry over). This is consistent with the holiday master (`hr_holiday.is_compensatory=false` for Sunday-holidays).
- **Half-day LOP:** `hr_leave_request.days = 0.5` → LOP deduction = `(gross_monthly / 26) × 0.5` days. 26 is the convention for average paid days per month under the Payment of Wages Act (not 30 or working days in month). This applies consistently for both full-day and half-day LOP.
- **Multiple part-day absences:** If employee has 3 half-day LOPs in a month, LOP total = 1.5 days. Payroll deduction = `(gross / 26) × 1.5`.

---

## Employee Self-Service: `/hr/my-payslips/`

All EduForge employees access own payslips at this route (`@login_required`):

| Feature | Description |
|---|---|
| Payslip list | All months since join date, most recent first |
| Download PDF | Individual payslip PDF from R2 (KMS decrypted on-demand) |
| Form 16 download | Available from 15 June each year for prior FY |
| Month filter | Filter by financial year |
| Gross/Net trend | Simple line chart: last 12 months' gross and net pay |

No admin actions. Strictly own-data. Route is `/hr/my-payslips/` — not under `/hr/payroll/` to avoid confusion with payroll management.

---

## Role-Based UI Visibility Summary

| Element | 79 HR Manager | 105 Payroll Exec | 69 Finance Mgr (cross-portal only) |
|---|---|---|---|
| Payroll runs list | Yes | Yes | Summary via API only |
| [Start Payroll Run] | No | Yes | No |
| [Approve Run] | Yes | No (disabled) | No |
| [Unlock Run] (after rejection) | Yes | No | No |
| Salary register — individual slip view | Yes | Yes | No |
| Salary register — all employees | Yes | Yes | No |
| Pending salary revisions panel | Yes | Yes (view + apply) | No |
| [Apply to Next Payroll Run] | Yes | Yes | No |
| Compensation distribution chart | Yes | No | No |
| Statutory filings — full view | Yes | Yes | No |
| Filing [Update Status] / [Upload Challan] | Yes | Yes | No |
| [Generate All Form 16s] | Yes | No | No |
| PF ECR file download | Yes | Yes | No |
| Export salary register CSV | Yes | Yes | No |
| Analytics — payroll trend | Yes | Yes | No |
| Analytics — compensation distribution | Yes | No | No |
| Analytics — statutory compliance heatmap | Yes | Yes | No |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Payroll runs list | < 600ms P95 (cache: 5 min) | Simple list of < 24 records |
| Payslip table (150 rows) | < 800ms P95 (no cache) | Critical path — live data |
| Payroll computation (Celery) | < 3 min for 150 employees | Background task — UI polls every 10s |
| Salary register export (CSV, 150 rows) | < 5s | Stream generation |
| PF ECR file generation | < 10s | Text file; 98 employee records |
| Form 16 bulk generation (150 PDFs) | < 15 min (background) | Celery task; user notified on completion |
| Statutory filings list | < 500ms P95 (cache: 5 min) | ~20–30 filing records max |

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `p` | Go to Payroll & Compliance (O-05) |
| `t` `r` | Switch to Payroll Runs tab |
| `t` `s` | Switch to Salary Register tab |
| `t` `f` | Switch to Statutory Filings tab |
| `t` `a` | Switch to Analytics tab |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |
