# 77 — Supplementary / Make-Up Exam Manager

> **URL:** `/group/acad/supplementary-exams/`
> **File:** `77-supplementary-exam-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Controller G3 (full) · Results Coordinator G3 (view + publish) · CAO G4 (view + override)

---

## 1. Purpose

End-to-end workflow for managing supplementary (make-up) exams for students who failed or were absent
from a main internal or board exam.

**Distinction from Page 22 (Group Exam Calendar):** The main exam calendar is for exams all students
appear in. Supplementary exams are for a subset of students (failed/absent) and are scheduled after
main results are published.

**Integration:** Eligible students are auto-populated from main result uploads. Supplementary marks,
once published, flow to Result Archive (Page 34) and optionally re-trigger rank recomputation (Page 30).

---

## 2. Role Access

| Role | Level | Can Schedule | Can Assign Paper | Can Upload Marks | Can Publish | Notes |
|---|---|---|---|---|---|---|
| Exam Controller | G3 | ✅ | ✅ | ✅ | ✅ | Primary owner |
| Results Coordinator | G3 | ❌ | ❌ | ❌ | ✅ | Publish + integrate |
| CAO | G4 | ❌ | ❌ | ❌ | ❌ | View + override rank integration |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Supplementary Exam Manager
```

### 3.2 Page Header
```
Supplementary / Make-Up Exam Manager                  [+ Schedule Exam]  [Export ↓]
AY 2025–26 · [N] Exams Scheduled · [M] Students Eligible · [P] Results Pending
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Students Eligible (total, AY) | 1,247 |
| Supplementary Exams Scheduled | 18 |
| Exams Completed | 12 |
| Results Uploaded | 10 |
| Students Cleared (passed supp.) | 834 |
| Students Still Failing | 413 |
| SLA Overdue (not scheduled in 30 days) | 4 |

---

## 4. Eligibility Pool

### 4.1 Eligible Students Table

Automatically populated from main exam results:

| Column | Type | Notes |
|---|---|---|
| Student | Text (masked) | |
| Branch | Text | |
| Exam | Text | Main exam they failed/missed |
| Subject(s) | Badge | Subject(s) requiring supplementary |
| Reason | Badge | Failed · Absent · Medical Leave |
| Main Mark | Number | Score in main exam |
| Eligibility Status | Badge | Eligible · Scheduled · Completed · Waived |
| SLA Days | Number | Days since main result published |
| Actions | — | Schedule · View |

### 4.2 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | |
| Subject | Multi-select | |
| Reason | Multi-select | Failed · Absent · Medical |
| Eligibility Status | Multi-select | Eligible · Scheduled · Completed · Waived |
| SLA | Select | Within SLA · Overdue |

---

## 5. Scheduled Exams Table

| Column | Type | Notes |
|---|---|---|
| Exam Name | Text | e.g. "Supp. Chemistry Term 2 — Batch A" |
| Main Exam | Text | Linked original exam |
| Branch(es) | Text | |
| Subject | Badge | |
| Date | Date | |
| Students | Number | |
| Paper Status | Badge | Not Assigned · Assigned |
| Marks Uploaded | Badge | Yes / Pending |
| Published | Badge | Yes / No |
| Actions | — | View · Upload Marks · Publish |

---

## 6. Drawers

### 6.1 Drawer: `supplementary-schedule` — Schedule Exam
- **Trigger:** [+ Schedule Exam] or [Schedule] in eligibility table
- **Width:** 640px

| Field | Type | Required |
|---|---|---|
| Select Students | Multi-select from eligible pool | ✅ |
| Group by | Option | By branch · By subject · Combined |
| Exam Date | Date | ✅ |
| Exam Time | Time | ✅ |
| Centre | Select | Branch exam centre or group-level centre |
| Subject(s) | Read-only from selection | — |
| Paper Assignment | Select | From Question Bank (Page 23) or Upload custom | ✅ |
| Duration (minutes) | Number | ✅ |
| Notify students? | Toggle | Default: On (via branch portal) |
| Invigilator | Search select | ❌ |

### 6.2 Drawer: `marks-upload` — Upload Marks
- **Trigger:** [Upload Marks] row action
- **Width:** 480px

| Field | Type |
|---|---|
| Exam | Read-only |
| Marks entry | Per student: Name · Roll No · Subject · Max Marks · Scored |
| CSV upload option | Alternative to manual entry |
| Result integration | Toggle: "Integrate into main ranks?" — requires Results Coordinator approval |

### 6.3 Drawer: `supplementary-detail`
- **Trigger:** View row action
- **Width:** 640px

**Tab: Students**
- List of students in this exam: Attendance · Marks · Result (Pass/Fail)

**Tab: Paper**
- Paper details: Name · Questions · From Question Bank / custom
- Download link (Exam Controller only)

**Tab: Marks**
- All marks entered · Pass/Fail status per student
- [Publish Results] button

**Tab: Integration**
- Status: Marks integrated into Result Archive (Page 34)? Yes/No
- Rank recomputation: Triggered? Yes/No/Pending
- [Trigger Recomputation] button (Results Coordinator)

---

## 7. SLA Tracking

| Rule | Detail |
|---|---|
| Schedule deadline | Supplementary must be scheduled within 30 days of main result publish |
| At Risk | 25–29 days elapsed without scheduling |
| Overdue | 30+ days — red badge, alert to CAO |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Exam scheduled | "Supplementary exam scheduled for [N] students on [Date]." | Success | 4s |
| Paper assigned | "Paper '[Name]' assigned to [Exam]." | Success | 3s |
| Marks uploaded | "Marks uploaded. [N] students passed." | Success | 4s |
| Results published | "Supplementary results published. Integrated into archive." | Success | 5s |
| SLA overdue | "[N] supplementary exams are overdue for scheduling." | Error | Manual |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No eligible students | "No eligible students" | "All students passed their main exams." |
| No scheduled exams | "No supplementary exams scheduled" | "Schedule exams for eligible students." |
| No pending results | "All results published" | "No supplementary results pending." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton: stats bar + eligibility table |
| Schedule drawer | Spinner in student selector |
| Marks upload | Spinner on submit |
| Recomputation trigger | Full-page overlay "Re-computing group ranks…" |

---

## 11. Role-Based UI Visibility

| Element | Exam Ctrl G3 | Results Coord G3 | CAO G4 |
|---|---|---|---|
| [+ Schedule Exam] | ✅ | ❌ | ❌ |
| [Assign Paper] | ✅ | ❌ | ❌ |
| [Upload Marks] | ✅ | ❌ | ❌ |
| [Publish Results] | ✅ | ✅ | ❌ |
| [Trigger Recomputation] | ❌ | ✅ | ❌ |
| [CAO Override Rank Integration] | ❌ | ❌ | ✅ |
| Eligibility table | ✅ | ✅ | ✅ |
| Scheduled exams table | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/supplementary-exams/eligible/` | JWT (G3+) | Eligible students pool |
| GET | `/api/v1/group/{id}/acad/supplementary-exams/` | JWT (G3+) | Scheduled exams list |
| POST | `/api/v1/group/{id}/acad/supplementary-exams/` | JWT (G3, ExamCtrl) | Schedule exam |
| GET | `/api/v1/group/{id}/acad/supplementary-exams/{eid}/` | JWT (G3+) | Exam detail |
| PUT | `/api/v1/group/{id}/acad/supplementary-exams/{eid}/assign-paper/` | JWT (G3, ExamCtrl) | Assign paper |
| POST | `/api/v1/group/{id}/acad/supplementary-exams/{eid}/marks/` | JWT (G3, ExamCtrl) | Upload marks |
| POST | `/api/v1/group/{id}/acad/supplementary-exams/{eid}/publish/` | JWT (G3) | Publish results |
| POST | `/api/v1/group/{id}/acad/supplementary-exams/{eid}/recompute-ranks/` | JWT (G3, ResultsCoord) | Trigger recomputation |
| GET | `/api/v1/group/{id}/acad/supplementary-exams/stats/` | JWT (G3+) | Summary stats |
| GET | `/api/v1/group/{id}/acad/supplementary-exams/export/?format=csv` | JWT (G3+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Eligibility table filter | `click` | GET `.../eligible/?filters=` | `#eligible-table` | `innerHTML` |
| Schedule drawer open | `click` | GET `.../supplementary-exams/create-form/` | `#drawer-body` | `innerHTML` |
| Schedule submit | `submit` | POST `.../supplementary-exams/` | `#drawer-body` | `innerHTML` |
| Exam detail drawer | `click` | GET `.../supplementary-exams/{id}/` | `#drawer-body` | `innerHTML` |
| Upload marks submit | `submit` | POST `.../marks/` | `#marks-tab-body` | `innerHTML` |
| Publish results | `click` | POST `.../publish/` | `#exam-row-{id}` | `outerHTML` |
| Trigger recomputation | `click` | POST `.../recompute-ranks/` | `#integration-tab-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
