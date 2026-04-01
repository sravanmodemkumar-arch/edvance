# A-03 — VP Academic Dashboard

> **URL:** `/school/admin/vp-academic/`
> **File:** `a-03-vp-academic-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Vice-Principal (Academic) (S5) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the VP Academic. This role owns everything related to learning and assessment: the academic calendar, syllabus coverage, exam scheduling, results quality, teacher performance, and academic standards alignment with the board (CBSE/ICSE/State Board). The VP Academic is the Principal's right hand for anything pedagogical.

**Indian school context:** In larger schools (>1,000 students), the academic VP is distinct from the administrative VP. They directly supervise all HODs, approve lesson plans, manage academic competitions (Olympiad, NTSE, Science Fair registrations), coordinate with the board's regional office during inspection visits, and prepare the school's data submissions for UDISE+ (Unified District Information System for Education).

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| VP Academic | S5 | Full — all sections |
| Principal | S6 | Read — can view this dashboard |
| VP Administration | S5 | — |
| HOD | S4 | — (has own section dashboard) |

---

## 3. Page Layout

### 3.1 Page Header
```
Good morning, [VP Academic Name]                        [Quick Action ▼]  [⚙]
VP Academic · [School Name] · Year [2025–26 ▼]
```

**[Quick Action ▼]:**
- View Today's Timetable Gaps
- Review Pending Leave (Teaching Staff)
- Check Syllabus Coverage Alerts
- Upcoming Exam Calendar

### 3.2 Alert Banner (conditional)
- Red: Any class without teacher for current/next period
- Amber: Syllabus coverage < 70% for any class/subject, with exam < 21 days away
- Amber: Any HOD leave pending > 2 days

---

## 4. KPI Strip (6 cards)

> HTMX refresh every 5m on `#vpa-kpi-strip`

| # | Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|---|
| 1 | Teaching Staff Present | `72 / 78 today (92.3%)` | Green ≥95% · Amber 85–94% · Red <85% | → A-17 Staff Attendance |
| 2 | Timetable Gaps Today | `2 periods uncovered` | Green = 0 · Amber 1–3 · Red >3 | → Timetable (div-b) |
| 3 | Syllabus Coverage | `81% avg` across all classes | Green ≥80% · Amber 60–79% · Red <60% | → div-b Syllabus Tracker |
| 4 | Pending Leave (Teaching) | `6 requests` awaiting approval | Badge if >0 | → A-18 Leave Management |
| 5 | Upcoming Exams (7 days) | `4 exams` | Blue if any | → A-12 Exam Calendar |
| 6 | Homework Completion | `74% avg` last week | Green ≥80% · Amber 65–79% · Red <65% | → div-b Homework |

---

## 5. Main Sections

### 5.1 Tab: Academic Health

**5.1.1 Syllabus Coverage Heatmap**
- Grid: rows = classes (I to XII), columns = departments/subjects
- Cell colour: Green ≥80% · Amber 60–79% · Red <60%
- Cell value: % covered
- Hover tooltip: "Class XI Physics — 76% covered (38/50 topics) · Last updated: 24 Mar 2026"
- Click cell → opens subject-class detail drawer with topic-by-topic breakdown
- API: `GET /api/v1/school/{id}/syllabus/coverage-heatmap/`

**5.1.2 Last Exam Results Summary (per class)**
- Table: Class · Exam Name · Date · Avg % · Pass % · >90% Count · <35% Count
- Filter: by class range (I–V / VI–VIII / IX–X / XI–XII)
- [View Full Results →] link

---

### 5.2 Tab: Staff Academic Performance

**5.2.1 Teaching Staff Attendance (last 30 days)**
- Bar chart: staff on X-axis, attendance % on Y-axis
- Sort by: lowest attendance first
- Click bar → staff leave history drawer

**5.2.2 Class Coverage Tracker** (for HODs to VP escalations)
- Shows which teachers have uncovered periods in the last 7 days
- Column: Teacher · Classes Covered · Periods Skipped · Reason
- [Send Reminder] per row

**5.2.3 Lesson Plan Submission Status**
- Table: HOD · Submission Due Date · Submitted On Time · Pending Teachers
- [Remind Pending] button (sends WhatsApp to overdue teachers)

---

### 5.3 Tab: Exam & Results

**5.3.1 Exam Calendar (next 30 days)**
- Timeline view: each exam as a block with class and subject
- Colour: Internal Assessment · Unit Test · Pre-board · Board Practical

**5.3.2 Result Publishing Queue**
- Table: Exam · Class · Marks Entered (%) · Verification Status · Publish Status
- [Review & Publish] → opens results drawer (sends to A-23 Approval if not VP authority)

**5.3.3 Academic Competition Tracker**
- Table: Competition · Participants · Level (School/District/State/National) · Date · Result
- Competitions: NTSE · Olympiad (Maths/Science/English/Computer) · CBSE Science Challenge · State-level talent exams
- [Add Competition] button

---

### 5.4 Tab: Pending Actions

- All leave requests for teaching staff: approve/reject inline
- Lesson plan review queue
- HOD report review (monthly HOD reports pending VP approval)

---

## 6. Drawers

### `syllabus-detail` (from heatmap cell click)
- Class + Subject + Teacher
- Topic list: [✅ Done | ⬜ Pending] per topic
- Estimated completion date vs exam date
- [Mark topics done] (VP can override teacher markings)

### `result-review` (from Result Publishing Queue)
- Exam details, class, marks entered by each class teacher
- Outliers: students with unexpectedly high/low marks flagged
- [Approve Publish] → sends result to students/parents
- [Return for Re-check] → notifies class teacher

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/vp-academic/dashboard/` | Full dashboard data |
| 2 | `GET` | `/api/v1/school/{id}/vp-academic/kpi-strip/` | KPI cards |
| 3 | `GET` | `/api/v1/school/{id}/syllabus/coverage-heatmap/` | Syllabus heatmap data |
| 4 | `GET` | `/api/v1/school/{id}/exams/calendar/?days=30` | Upcoming exams |
| 5 | `GET` | `/api/v1/school/{id}/results/publish-queue/` | Pending result publications |
| 6 | `POST` | `/api/v1/school/{id}/results/{id}/publish/` | Publish results |
| 7 | `GET` | `/api/v1/school/{id}/staff/teaching-attendance/?days=30` | Teaching staff attendance |
| 8 | `GET` | `/api/v1/school/{id}/homework/completion-summary/` | Homework completion |
| 9 | `GET` | `/api/v1/school/{id}/competitions/` | Academic competitions list |
| 10 | `POST` | `/api/v1/school/{id}/competitions/` | Add competition |

---

## 8. HTMX Patterns

### KPI Strip Refresh
```html
<div id="vpa-kpi-strip"
     hx-get="/api/v1/school/{{ school_id }}/vp-academic/kpi-strip/"
     hx-trigger="every 5m"
     hx-target="#vpa-kpi-strip"
     hx-swap="outerHTML">
</div>
```

### Inline Leave Approval
```html
<form hx-post="/api/v1/school/{{ school_id }}/approvals/{{ leave_id }}/decide/"
      hx-target="#leave-row-{{ leave_id }}"
      hx-swap="outerHTML">
  <input type="hidden" name="decision" value="APPROVED">
  <button type="submit" class="btn-sm-success">Approve</button>
</form>
```

---

## 9. Security & Performance

- VP Academic can approve results for internal exams; board exam results require Principal sign-off
- All result publication events logged in `school_audit_log`
- Syllabus heatmap data cached per school per day; invalidated on syllabus update events
- Lesson plan data loaded on tab click (lazy HTMX), not on dashboard load

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
