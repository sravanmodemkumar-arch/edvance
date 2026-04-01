# F-16 — Communication Analytics

> **URL:** `/school/comm-analytics/`
> **File:** `f-16-communication-analytics.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Communication Coordinator (S3) — view · Academic Coordinator (S4) — full access · Principal (S6) — full access

---

## 1. Purpose

Gives the school a data-driven view of communication effectiveness. Answers questions like:
- "Which channel works best for our parent population — WhatsApp or SMS?"
- "What time of day do parents read our messages?"
- "Which classes have the lowest parent engagement?"
- "Is our PTM communication strategy effective?"
- "Are we over-communicating? (causing notification fatigue)"
- "Which types of messages get acted upon vs just read?"

---

## 2. Page Layout

### 2.1 KPI Strip
```
Communication Analytics — 2026–27 (Year to date)

Total messages sent: 18,420
  WhatsApp: 14,200 (77%)  ·  SMS: 2,850 (15%)  ·  Email: 1,370 (7%)
Overall delivery rate: 97.3%  ·  Overall read rate: 84.1% (WhatsApp read receipts)
Parent engagement score: 82/100  ·  Target: 85/100
```

### 2.2 Channel Performance
```
Channel Comparison — March 2026

          WhatsApp     SMS         Email
Sent      2,841        342         89
Delivered 2,790 (98%)  334 (97%)   86 (97%)
Read      2,340 (82%)  N/A         52 (58%)  ← email open rate
Cost      ₹994 (₹0.35) ₹205 (₹0.6) ₹45 (₹0.5)
Best for  Primary      Fallback    Documents/records

Recommendation: WhatsApp delivers best engagement at Rs 0.35/msg vs SMS Rs 0.60/msg.
Reduce SMS to strictly non-WhatsApp parents (currently 45 parents).
```

### 2.3 Message Type Performance
```
Message Type         Sent    Read %   Action Taken %   Notes
Daily absent alert   1,240   79%      N/A (no CTA)
Attendance warning     84   91%      45% (parent replied or booked appt)  ← high engagement
Fee reminder          380   87%      68% (paid within 3 days)  ← effective
Exam reminder         490   95%      N/A
PTM invitation        380   84%      82% confirmed slot  ← very effective
Holiday notice        380   78%      N/A
Circular shared       380   72%      —                    ← lower than others
```

### 2.4 Time-of-Day Read Patterns
```
Best times to send (by read rate within 1 hour):

WhatsApp:
  7:00–8:00 AM: 91%  ★★★★★  ← Parents checking phone before/during school drop
  6:00–7:00 PM: 87%  ★★★★★  ← Evening after work
  12:00–1:00 PM: 71% ★★★★☆  ← Lunch hour
  10:00–11:00 PM: 62% ★★★☆☆ ← Late night, lower priority

Recommendation: Schedule routine messages for 7:30 AM or 6:30 PM.
Emergency alerts: Send immediately regardless of time.
```

### 2.5 Class-wise Parent Engagement
```
Class-wise Engagement Score (WhatsApp read rate + PTM attendance + diary sign rate)

Class       Engagement  WhatsApp Read  PTM Attend  Diary Sign
Nursery-A   96/100      98%            96%         95%
Class I-A   94/100      97%            94%         93%
Class VI-A  88/100      88%            85%         82%  ← slight drop
Class IX-A  79/100      82%            78%         72%  ← dip in secondary
Class XI-A  74/100      79%            89%         62%  ← diary sign drops for secondary
Class XII-A 78/100      84%            92%         55%  ← PTM high (exam stress)

Insight: Secondary class parents engage less on diary but more on PTM.
Consider reducing diary sign requirement for Classes IX–XII and increasing PTM sessions.
```

### 2.6 Opt-Out Trend
```
WhatsApp Opt-Outs — 2026–27 (cumulative)

April 2026:     1 (0.3% of parents)
May–August:     0
September:      2
October:        4  ← spike after multiple Oct flood alerts + fee reminder bunching
November:       1
December:       2
January:        1
February:       0
March:          1

Total: 12/380 parents opted out (3.2%)
→ Review October communication volume — 18 messages sent in Oct vs avg 7/month
→ Reduce to max 10 messages/month per parent (notification fatigue threshold)
```

---

## 3. Homework Assignment Analytics (F-09 Feed)

```
Homework Workload Monitor — March 2026

Subject     Avg assignments/week   Avg completion rate   Parent acknowledgement
Physics          4.2                    73%                     81%
Chemistry        3.8                    78%                     83%
Mathematics      5.1  ⚠️ High          65%  ← drop in completion   79%
English          2.9                    88%                     91%
Phy. Edu.        1.0                    95%                     88%

Insight: Mathematics assignment volume is high (5.1/week) and completion rate is low (65%).
Coordinator to discuss with Maths teacher.
```

---

## 4. Grievance Analytics

```
Grievance Resolution Analytics — 2026–27

Category        Total   Avg Resolution  SLA Met  Common root cause
Academic          18      4.2 days        100%   Marks disputes (8), syllabus (5)
Fee               12      3.1 days        100%   Late fee waiver requests
Attendance         8      2.0 days        100%   Correction requests
Staff conduct      3      3.5 days        100%   Homework burden, tone
Transport          5      1.8 days        100%   Bus delays (Route 4 — chronic)
RTE                1     28 days           98%   Refund delay
POCSO              1    Restricted        N/A    Restricted

Transport Route 4 issues: 3 of 5 transport complaints. Action flagged for management.
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/comm-analytics/kpi/?year={y}&month={m}` | KPI strip data |
| 2 | `GET` | `/api/v1/school/{id}/comm-analytics/channel/?year={y}` | Channel performance comparison |
| 3 | `GET` | `/api/v1/school/{id}/comm-analytics/message-types/?year={y}` | Message type effectiveness |
| 4 | `GET` | `/api/v1/school/{id}/comm-analytics/timing/?year={y}` | Time-of-day read patterns |
| 5 | `GET` | `/api/v1/school/{id}/comm-analytics/class-engagement/?year={y}` | Class-wise parent engagement |
| 6 | `GET` | `/api/v1/school/{id}/comm-analytics/opt-outs/?year={y}` | Opt-out trend |
| 7 | `GET` | `/api/v1/school/{id}/comm-analytics/homework/?year={y}&month={m}` | Homework analytics |
| 8 | `GET` | `/api/v1/school/{id}/comm-analytics/grievances/?year={y}` | Grievance resolution analytics |
| 9 | `GET` | `/api/v1/school/{id}/comm-analytics/export-pdf/?year={y}` | Annual communication report PDF |

---

## 6. Business Rules

- Communication analytics data is aggregated — individual parent message timestamps are available in F-13 communication log; F-16 shows only aggregate patterns
- Notification fatigue threshold is configurable by the school (default: 10 messages/month per parent; alert when exceeded)
- The Parent Engagement Score is a composite: WhatsApp read rate (40%) + PTM attendance (30%) + diary signature rate (20%) + grievance response rate (10%); weights are configurable
- Analytics data is retained for 3 years for trend comparison
- POCSO and sensitive grievance categories are excluded from analytics reports that non-DP staff can see

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
