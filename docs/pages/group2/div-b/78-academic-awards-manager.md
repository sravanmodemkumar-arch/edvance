# 78 — Academic Awards & Recognition Manager

> **URL:** `/group/acad/awards/`
> **File:** `78-academic-awards-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** CAO G4 (full — approve and publish) · Academic Director G3 (create + manage) · Stream Coordinators G3 (own-stream nominees) · MIS Officer G1 (read)

---

## 1. Purpose

Structured group-level recognition workflow that goes beyond rank-based topper lists (Page 31).
Supports effort awards, improvement awards, subject excellence awards, and perfect attendance awards.

**Why beyond toppers?** Topper lists recognise absolute rank. Awards recognise:
- Students who improved the most (not necessarily ranked high)
- Students who excel in a specific subject despite average overall rank
- Students who attended every day and passed
- Students nominated by branch for exceptional effort

Awards feed the group's marketing material and student motivation initiatives.

---

## 2. Role Access

| Role | Level | Can Create Award | Can Approve Nominees | Can Issue Certificates | Notes |
|---|---|---|---|---|---|
| CAO | G4 | ❌ | ✅ Final approve | ✅ | Final authority |
| Academic Director | G3 | ✅ | ✅ (first-level) | ✅ | Day-to-day manager |
| Stream Coordinators | G3 | ❌ | ✅ Own stream nominees | ❌ | |
| MIS Officer | G1 | ❌ | ❌ | ❌ | Read awardee list |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Academic Awards & Recognition
```

### 3.2 Page Header
```
Academic Awards & Recognition Manager                 [+ Create Award]  [Export ↓]
AY 2025–26 · Term [N] · [M] Awards Defined · [P] Certificates Issued
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Awards Defined (AY) | 12 |
| Total Awardees | 487 |
| Certificates Issued | 412 |
| Awards Pending Approval | 3 |
| Branches with 0 Awardees | 2 |

---

## 4. Main Table — Awards List

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Award Name | Text + link | ✅ | |
| Type | Badge | ✅ | Subject Excellence · Most Improved · Merit Scholarship · Perfect Attendance · Effort · Olympiad |
| Term / Year | Text | ✅ | |
| Stream Scope | Badge | ✅ | All / MPC / BiPC / etc. |
| Eligible Students | Number | ✅ | Auto-computed |
| Approved Awardees | Number | ✅ | |
| Certificates Issued | Number | ✅ | |
| Status | Badge | ✅ | Draft · Nominees Pending · Approved · Certificates Issued |
| Actions | — | ❌ | View · Edit · Approve · Issue Certificates |

---

## 5. Award Types

| Type | Eligibility Criteria | How Computed |
|---|---|---|
| Subject Excellence | Top N scorers per subject (configurable N) | From Result Archive — top marks per subject |
| Most Improved | Highest % improvement term-on-term (configurable threshold) | Compare T-1 and T avg marks per student |
| Merit Scholarship | Composite score ≥ threshold (configurable) | From Group Rank Computation |
| Perfect Attendance + Pass | 100% attendance in term + pass all subjects | Attendance + results cross-check |
| Effort Award | Manual nomination by branch | No auto-computation — branch nominations |
| Olympiad Champion | Linked from Olympiad Results (Page 44) | Auto-populated from Page 44 data |

---

## 6. Drawers

### 6.1 Drawer: `award-create` — Create Award
- **Trigger:** [+ Create Award] header button
- **Width:** 640px

| Field | Type | Required | Notes |
|---|---|---|---|
| Award Name | Text | ✅ | |
| Award Type | Select | ✅ | |
| Term / Year | Select | ✅ | |
| Stream Scope | Multi-select | ✅ | All / specific streams |
| Branch Scope | Multi-select | ✅ | All branches or select |
| Eligibility Criteria | Dynamic | ✅ | Changes based on type |
| Number of Awardees | Number | Conditional | For Subject Excellence, Most Improved, Merit |
| Threshold | Number | Conditional | For Merit Scholarship |
| Prize | Text | ❌ | e.g. "Certificate + ₹2,000" |
| Certificate Template | Select | ✅ | From template library |
| Two-level approval? | Toggle | ❌ | Academic Dir → CAO |

**Eligibility criteria (dynamic by type):**
- Subject Excellence: Subject · Top N students
- Most Improved: Min improvement % · Term comparison
- Merit Scholarship: Min composite score %
- Perfect Attendance: Min attendance % (default 95%) + pass all subjects
- Effort: Manual nomination only

### 6.2 Drawer: `award-nominees` — Review & Approve Nominees
- **Trigger:** View or Approve row action
- **Width:** 680px

**Tab: Auto-Nominees** (for non-manual award types)
- System-computed eligible students based on criteria
- **Table:** Student (masked) · Branch · Score / Improvement · Eligible Since
- **Actions per student:** Approve · Override Exclude (with reason)
- **Bulk approve all**

**Tab: Manual Nominations** (for Effort Award)
- Nominations submitted by branch staff
- **Table:** Student · Branch · Nominated By · Reason
- **Actions:** Approve · Reject (with reason)

**Tab: Approved Awardees**
- Final approved list before certificate issuance
- **[Issue Certificates]** button — only when status = All nominees reviewed

**Tab: Certificates**
- Generated certificates list with download status
- **[Regenerate]** if template was updated after generation

---

## 7. Certificate Generation

| Feature | Detail |
|---|---|
| Template fields | Student name · Award name · Term · Date · Group seal · Signatures |
| Bulk generation | All approved awardees in one batch |
| Output | ZIP containing individual PDFs |
| Naming convention | `[AwardName]_[StudentInitials]_[BranchCode].pdf` |
| Download link | Time-limited (7 days) ZIP download link |
| Branch distribution | Each branch gets a filtered ZIP of their students' certificates |

---

## 8. Branch Nominations Portal

Branch staff submit Effort Award nominations via branch portal:
- Student name · Class · Section · Reason (min 100 chars)
- Supporting evidence upload (optional)
- Routes to Academic Director for review

---

## 9. Charts

### 9.1 Awards by Branch (Heatmap)
- **Rows:** Branches
- **Columns:** Award types
- **Cell:** Number of awardees from that branch in that award
- **Export:** PNG

### 9.2 Award Type Distribution (Pie)
- **Data:** Number of awardees per award type
- **Export:** PNG

---

## 10. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Award created | "Award '[Name]' created. Computing eligible students…" | Success | 4s |
| Nominees approved | "[N] nominees approved for '[Award]'." | Success | 4s |
| Certificates issued | "Certificates generated for [N] students. Download link ready." | Success | 5s |
| Nomination received | "New Effort Award nomination from [Branch]." | Info | 4s |
| Nominee rejected | "Nominee removed from '[Award]' with reason recorded." | Warning | 4s |

---

## 11. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No awards | "No awards defined" | "Create the first academic award for this term." | [+ Create Award] |
| No nominees | "No eligible students found" | "Check eligibility criteria or results data availability." | — |
| No nominations | "No branch nominations received" | "Nominations will appear once branch staff submit them." | — |

---

## 12. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton: stats + award table |
| Auto-nominees compute | Spinner "Computing eligible students…" in drawer |
| Certificate generation | Full-page overlay "Generating certificates…" |
| Chart render | Spinner in chart area |

---

## 13. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Stream Coords G3 | MIS G1 |
|---|---|---|---|---|
| [+ Create Award] | ❌ | ✅ | ❌ | ❌ |
| [Approve Nominees] (final) | ✅ | ✅ (first-level) | ✅ (own stream) | ❌ |
| [Issue Certificates] | ✅ | ✅ | ❌ | ❌ |
| [Reject Nominee] | ✅ | ✅ | ✅ (own stream) | ❌ |
| Awardee list | ✅ | ✅ | ✅ (own stream) | ✅ (anon) |
| Charts | ✅ | ✅ | ✅ (own stream) | ✅ |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/awards/` | JWT (G1+) | Awards list |
| POST | `/api/v1/group/{id}/acad/awards/` | JWT (G3, AcadDir) | Create award |
| GET | `/api/v1/group/{id}/acad/awards/{aid}/` | JWT (G1+) | Award detail |
| GET | `/api/v1/group/{id}/acad/awards/{aid}/nominees/` | JWT (G3+) | Nominees (auto + manual) |
| POST | `/api/v1/group/{id}/acad/awards/{aid}/nominees/{nid}/approve/` | JWT (G3+) | Approve nominee |
| POST | `/api/v1/group/{id}/acad/awards/{aid}/nominees/{nid}/reject/` | JWT (G3+) | Reject nominee |
| POST | `/api/v1/group/{id}/acad/awards/{aid}/certificates/generate/` | JWT (G3+) | Generate certificates |
| GET | `/api/v1/group/{id}/acad/awards/{aid}/certificates/download/` | JWT (G3+) | ZIP download link |
| GET | `/api/v1/group/{id}/acad/awards/nominations/` | JWT (G3+) | Branch nominations inbox |
| GET | `/api/v1/group/{id}/acad/awards/stats/` | JWT (G1+) | Summary stats |
| GET | `/api/v1/group/{id}/acad/awards/export/?format=csv` | JWT (G1+) | Export awardee list |

---

## 15. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Awards table filter | `click` | GET `.../awards/?filters=` | `#awards-section` | `innerHTML` |
| Open award detail | `click` | GET `.../awards/{id}/` | `#drawer-body` | `innerHTML` |
| Create award submit | `submit` | POST `.../awards/` | `#drawer-body` | `innerHTML` |
| Load nominees tab | `click` | GET `.../awards/{id}/nominees/` | `#nominees-tab-body` | `innerHTML` |
| Approve nominee | `click` | POST `.../nominees/{nid}/approve/` | `#nominee-row-{id}` | `outerHTML` |
| Reject nominee | `click` | POST `.../nominees/{nid}/reject/` | `#nominee-row-{id}` | `outerHTML` |
| Generate certificates | `click` | POST `.../certificates/generate/` | `#cert-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
