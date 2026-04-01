# A-32 — MIS Dashboard

> **URL:** `/school/admin/mis/`
> **File:** `a-32-mis-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Principal (S6) — full · Promoter (S7) — full · VP Academic (S5) — academic sections · VP Admin (S5) — admin/finance sections · Admin Officer (S3) — view

---

## 1. Purpose

The Management Information System (MIS) Dashboard — a comprehensive single-page view of the school's operational KPIs across all domains. Used in India's school context for:
- Monthly management review meetings (Principal presents to Promoter/Trust)
- CBSE periodic compliance submissions (CBSE requires schools to maintain performance data)
- Inter-school benchmarking within a group (if the school belongs to a chain, Group 2 pulls this data)
- Annual reports to the Board of Trustees
- Inspection preparation (CBSE/NAAC/state board inspectors review this data)

In well-run Indian schools, the Principal reviews this dashboard daily or weekly and presents a monthly MIS report to the Promoter/Board.

---

## 2. Page Layout

### 2.1 Header
```
MIS Dashboard — School Management Information System    [Generate MIS Report] [Export All Data]
Academic Year: 2025–26 ▼     Period: March 2026 ▼     As of: 26 Mar 2026
```

### 2.2 Section Tabs
```
[Overview] [Academic] [Finance] [Attendance] [Admissions] [Staff] [Compliance]
```

---

## 3. Tab: Overview (default)

**KPI Grid — 12 cards, 4 per row:**

| KPI | Value | vs Last Year | Target |
|---|---|---|---|
| Total Students | 1,048 | ↑ 4.2% | 1,100 |
| Staff Strength | 110 | ↑ 2 new | 115 |
| Seat Fill Rate | 87.3% | ↑ 3.1% | 90% |
| Fee Collection Rate (YTD) | 82.3% | ↓ 1.2% | 88% |
| Student Attendance (avg) | 88.6% | ↓ 0.4% | 90% |
| Staff Attendance (avg) | 93.2% | ↑ 0.8% | 95% |
| Pass % (Last exam) | 97.4% | ↑ 0.6% | 98% |
| Average Score (Last exam) | 74.2% | ↑ 1.4% | 75% |
| RTE Compliance | 30% (target: 25%) | ✅ | ≥25% |
| BGV Compliance | 94.5% | ↑ 2.3% | 100% |
| Compliance Score | 91.4% | ↑ 2.1% | 95% |
| Parent Satisfaction | 4.2/5 (last PTM survey) | ↑ 0.2 | 4.5/5 |

---

## 4. Tab: Academic

**4.1 Exam Results Trend (last 4 terms)**
- Line chart: Pass % by class level (Primary / Middle / Secondary / Sr. Secondary)
- Separate lines per academic year for comparison

**4.2 Subject-wise Performance**
- Heatmap: Class (row) × Subject (column) = avg score
- Red cells: avg < 50% · Amber: 50–65% · Green: >65%

**4.3 Homework Completion Rate (monthly)**
- Bar chart per month

**4.4 Syllabus Coverage (current month)**
- Gauge chart: overall % covered

---

## 5. Tab: Finance

**5.1 Monthly P&L Trend** (income vs expenditure 12 months)
**5.2 Fee Collection by Category** (tuition / transport / hostel / exam / other)
**5.3 Outstanding Dues Ageing** (< 30 / 30–60 / > 60 days)
**5.4 Salary Cost as % of Revenue** (trend — target: < 65%)

---

## 6. Tab: Attendance

**6.1 Student Attendance by Class (monthly avg)** — horizontal bar chart
**6.2 Staff Attendance by Department** — bar chart
**6.3 Chronic Absentees** — students with < 75% attendance this year (count + percentage)
**6.4 Year-to-date working days** vs 220-day CBSE minimum

---

## 7. Tab: Admissions

**7.1 Current Season Funnel** — same as A-14 funnel
**7.2 Seat Fill by Class** — comparison current vs last 3 years
**7.3 Enquiry Source Analysis** — Pie chart: walk-in / website / WhatsApp / referral / advertisement
**7.4 Conversion Rate Trend** — enquiry-to-enrollment conversion monthly

---

## 8. Tab: Staff

**8.1 Headcount by Category and Department** — bar chart
**8.2 Leave Utilisation** — average leaves taken per staff per month
**8.3 BGV Compliance** — verified / pending / expired donut
**8.4 New Joiners and Attrition** (last 12 months) — bar chart

---

## 9. Tab: Compliance

**Summary of A-29 compliance data presented in chart form:**
- Compliance score trend (line chart, last 6 months)
- Items by category: pie chart
- Overdue vs upcoming (bar chart)

---

## 10. MIS Report Generation

**[Generate MIS Report]** → opens report builder dialog:
- Select period: Month / Quarter / Half-Year / Full Year
- Select sections to include (checkboxes)
- Format: PDF (formatted) / Excel (raw data)
- [Generate] → creates background task; download link ready in 30–60 seconds
- Report header: school letterhead + Principal signature block

---

## 11. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/mis/overview/` | Overview KPI grid |
| 2 | `GET` | `/api/v1/school/{id}/mis/academic/` | Academic section data |
| 3 | `GET` | `/api/v1/school/{id}/mis/finance/` | Finance section data |
| 4 | `GET` | `/api/v1/school/{id}/mis/attendance/` | Attendance section data |
| 5 | `GET` | `/api/v1/school/{id}/mis/admissions/` | Admissions section data |
| 6 | `GET` | `/api/v1/school/{id}/mis/staff/` | Staff section data |
| 7 | `GET` | `/api/v1/school/{id}/mis/compliance/` | Compliance section data |
| 8 | `POST` | `/api/v1/school/{id}/mis/report/generate/` | Generate MIS report (async) |
| 9 | `GET` | `/api/v1/school/{id}/mis/report/{task_id}/download/` | Download generated report |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
