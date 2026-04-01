# div-a-23 — Proctoring Overview

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Proctored exams/day | ~500–1,500 |
| Students proctored/day | ~50,000–150,000 |
| Proctoring events/day | ~5M–15M (snapshots, tab-switch, etc.) |
| Violation flags auto-generated/day | ~5,000–20,000 |
| Manual review queue | ~200–500 items |
| Proctoring types | Webcam only / Screen only / Full (webcam + screen) |
| AI proctoring models | Face detection / Multiple face / Phone detection |
| Storage: proctoring recordings | ~100 TB |

**Why this matters:** Proctoring integrity is the platform's exam validity guarantee. Coaching centres pay premium (₹15 Cr ARR) partly for the proctoring. If the proctoring system has a high false-positive rate (flagging honest students) or a high miss rate (missing cheaters), both are contract-level issues.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Proctoring Overview |
| Route | `/exec/proctoring/` |
| Django view | `ProctoringOverviewView` |
| Template | `exec/proctoring_overview.html` |
| Priority | P1 |
| Nav group | Exams |
| Required role | `exec`, `superadmin`, `ops` |
| 2FA required | Disqualifying students |
| HTMX poll | Live violations: every 30s |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Proctoring Overview                         [Export] [Settings ▾]  │
├────────┬────────┬────────┬────────┬────────┬──────────────────────────────── ┤
│Proctored│Flags  │ Pending│ False+ │ Disqual│  Violation                     │
│ Today  │ Today  │ Review │ Rate   │ (30d)  │  Rate                          │
│  842   │  3,120 │  184   │  2.1%  │   12   │  3.7%                          │
├────────┴────────┴────────┴────────┴────────┴──────────────────────────────── ┤
│ TABS: [Live Monitor] [Review Queue] [Violation Analytics] [Settings]        │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: LIVE MONITOR                                                            │
│ Active proctored exams grid (cards per exam)                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Proctored Today | Students proctored today | — |
| 2 | Flags Today | Auto-generated violation flags | — |
| 3 | Pending Review | Flags awaiting human review | > 500 = amber |
| 4 | False Positive Rate | False flags / total flags (30d) | > 5% = amber |
| 5 | Disqualified (30d) | Students disqualified | > 50 = amber |
| 6 | Violation Rate | Students with ≥1 flag / total proctored (30d) | > 10% = amber |

---

### 4.2 Tab: Live Monitor

`id="tab-live"` · `hx-get="?part=live_exams"` · `hx-trigger="every 30s"`

**Active proctored exams grid:** `grid grid-cols-3 gap-4 p-4`
Each exam card:
```
┌─────────────────────────────────────┐
│ JEE Mock Test 12                    │
│ ABC Coaching · Class 12             │
│                                     │
│ Students: 842 active                │
│ Flags (live): 12 🔴                 │
│ Violations: 3 high-risk             │
│                                     │
│ [Live: 24 min]    [View Exam →]     │
└─────────────────────────────────────┘
```
Card border: `border-[#34D399]` (normal) · `border-[#EF4444] animate-pulse` (if > 5 flags/min)

**Live violation feed (right sidebar, 320px):**
Real-time stream of violation events:
```
14:32:05  ABC Coaching — Q.12345 — Multiple face detected [High]
14:31:58  XYZ College — Q.18821 — Tab switch detected [Low]
14:31:45  ABC Coaching — Q.09882 — Phone detected [High]
```
Scrolling feed · newest at top · max 100 entries in DOM
**Poll:** `hx-trigger="every 15s"` `hx-swap="afterbegin"` on feed container

---

### 4.3 Tab: Review Queue

`id="tab-queue"` · `hx-get="?part=review_queue"`

**Purpose:** Human review of auto-flagged violations. Proctoring team (or ops) reviews each flag and either clears or confirms.

**Review Queue Table:**
| Column | Detail |
|---|---|
| # | Queue position |
| Student | Name + exam |
| Violation type | Badge |
| Detected at | Timestamp |
| Severity | High / Medium / Low |
| Preview | Thumbnail screenshot (if webcam) |
| Status | Pending / Under Review / Cleared / Confirmed |
| Reviewer | Assigned reviewer name |
| Actions ⋯ | Review / Assign / Clear / Confirm |

**[Review]:** opens Review Drawer (§5.1) for side-by-side decision

**Batch actions:** [Assign to me] [Batch clear low-severity] [Export queue]

**Filter:** Severity · Exam · Institution · Violation type · Date

---

### 4.4 Tab: Violation Analytics

`id="tab-analytics"` · `hx-get="?part=violation_analytics"`

#### 4.4.1 Violation Trend (30-day line chart)

**Series:**
- Total flags: `#6366F1`
- High severity: `#EF4444`
- Confirmed violations: `#F59E0B`
- Disqualifications: `#EF4444` dashed

#### 4.4.2 Violation Type Breakdown (donut chart)

Segments: Tab switch / Multiple face / Phone detected / No face / Screen share / Audio anomaly

#### 4.4.3 Violation by Institution Type (bar chart)

4 groups · sorted by violation rate

#### 4.4.4 False Positive Trend (line chart)

`#F59E0B` line · target line < 3% dashed `#34D399`

#### 4.4.5 Top Flagged Exams (table, 10 rows)

| Exam | Institution | Date | Flags | Violation rate | Disqualified |
|---|---|---|---|---|---|

---

### 4.5 Tab: Settings

`id="tab-settings"` · `hx-get="?part=proctoring_settings"`

**Proctoring policy settings:**
| Setting | Type | Default |
|---|---|---|
| Tab switch tolerance | Number (N switches allowed) | 3 |
| Face detection confidence threshold | Slider 0–100% | 85% |
| Multiple face detection | Toggle | On |
| Phone detection | Toggle | On |
| Auto-flag threshold | Number (flags before auto-flag) | 5 |
| Auto-disqualify threshold | Number (flags before auto-disqualify) | 10 |
| Proctoring recording retention | Select: 30d / 60d / 90d / 180d | 90d |
| Default proctoring type | Select: Webcam only / Screen / Full | Full |

**[Save Settings]** · 2FA required

---

## 5. Drawers

### 5.1 Violation Review Drawer (800 px wide)

`id="review-drawer"` · `w-[800px]` · `body.drawer-open`

**Header:** Student name + Exam name + Violation type + Severity badge · `[×]`

**Left panel (480px) — Evidence:**
- Webcam snapshot grid (4 snapshots around violation event) · each 160px × 120px
- Video clip playback (10s before + 10s after event) · if available
- Screen recording thumbnail

**Right panel (280px) — Violation details:**
- Event timestamp
- Violation type
- AI confidence score: e.g., "Phone detected: 94% confidence"
- Student answer at time of violation: Q{N} answered {A}
- Prior flags for this student (this exam): N

**Decision buttons (prominent):**
- [Clear — Not a violation] `bg-[#064E3B] text-[#34D399] px-6 py-3 rounded-lg font-semibold`
- [Confirm — Violation] `bg-[#450A0A] text-[#F87171] px-6 py-3 rounded-lg font-semibold`
- [Escalate for disqualification] `bg-[#451A03] text-[#FCD34D] px-4 py-2 rounded-lg`

**Reviewer notes:** textarea `<100 chars`
**[Previous in queue]** [Next in queue] navigation at bottom

**POST:** `hx-post="?part=review_decision&flag_id={id}"` · on success: next item loads automatically

---

## 6. Modals

### 6.1 Disqualify Student (from review drawer) (480 px)

Same as div-a-21 §11.3. **2FA required.**

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/proctor_kpi.html` | Page load · poll 30s |
| `?part=live_exams` | `exec/partials/proctor_live.html` | Tab · poll 30s |
| `?part=live_feed` | `exec/partials/proctor_feed_rows.html` | Feed poll 15s |
| `?part=review_queue` | `exec/partials/proctor_queue.html` | Tab · filter |
| `?part=violation_analytics` | `exec/partials/proctor_analytics.html` | Tab click |
| `?part=proctoring_settings` | `exec/partials/proctor_settings.html` | Tab click |
| `?part=review_drawer&id={id}` | `exec/partials/review_drawer.html` | Row click |
| `?part=review_decision&flag_id={id}` | POST → next item | Review decision |

**Django view dispatch:**
```python
class ProctoringOverviewView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_proctoring"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/proctor_kpi.html",
                "live_exams": "exec/partials/proctor_live.html",
                "live_feed": "exec/partials/proctor_feed_rows.html",
                "review_queue": "exec/partials/proctor_queue.html",
                "violation_analytics": "exec/partials/proctor_analytics.html",
                "proctoring_settings": "exec/partials/proctor_settings.html",
                "review_drawer": "exec/partials/review_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/proctoring_overview.html", ctx)
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 200 ms | > 500 ms |
| Live exams grid | < 300 ms | > 800 ms |
| Review queue (50 rows) | < 400 ms | > 1 s |
| Review drawer (with screenshots) | < 600 ms | > 1.5 s |
| Violation analytics charts | < 600 ms | > 1.5 s |
| Full page initial load | < 1 s | > 2.5 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| No live proctored exams | "No live proctored exams right now" with scheduled next exam |
| Review queue empty | "Review queue is clear ✓" green success state |
| False positive rate > 5% | Analytics tab amber banner + settings suggestion |
| Webcam data unavailable | "Webcam recording unavailable for this event" in review drawer |
| Auto-disqualify trigger | Student auto-disqualified + notification sent + exam status updated + audit log entry |
| Student disputes disqualification | Re-check request appears in review queue |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`4` | Switch tabs |
| `C` | Clear violation (in review drawer) |
| `V` | Confirm violation (in review drawer) |
| `N` | Next in review queue |
| `P` | Previous in review queue |
| `Esc` | Close drawer |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/proctoring_overview.html` | Full page shell |
| `exec/partials/proctor_kpi.html` | KPI strip |
| `exec/partials/proctor_live.html` | Live exam cards grid |
| `exec/partials/proctor_feed_rows.html` | Live violation feed rows |
| `exec/partials/proctor_queue.html` | Review queue table |
| `exec/partials/proctor_analytics.html` | Violation analytics charts |
| `exec/partials/proctor_settings.html` | Settings form |
| `exec/partials/review_drawer.html` | Violation review drawer |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `LiveExamCard` | §4.2 |
| `ViolationFeed` | §4.2 right panel |
| `ReviewQueueTable` | §4.3 |
| `ViolationTrendChart` | §4.4.1 |
| `ViolationDonut` | §4.4.2 |
| `FalsePosChart` | §4.4.4 |
| `DrawerPanel` | §5.1 |
| `ViolationSnapshotGrid` | §5.1 |
| `VideoPlayer` | §5.1 |
| `ReviewDecisionButtons` | §5.1 |
| `ModalDialog` | §6.1 |
| `PollableContainer` | KPI · live exams · feed |
