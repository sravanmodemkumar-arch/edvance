# div-a-24 — Executive Reports

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Report types | ~15 pre-built report templates |
| Scheduled reports | ~30–50 active schedules |
| Report recipients | Up to 20 (board members, VCs, advisors) |
| Report generation time | < 30 s (standard) · < 5 min (large datasets) |
| Export formats | PDF · XLSX · CSV · JSON |
| Data freshness | Reports use Redis cache (max 1h stale) |
| Archive retention | 2 years |

**Why this matters:** The board wants a PDF every month. The CFO wants an ARR waterfall every week. The CEO wants a one-pager before every investor call. Executive Reports is the self-service report generator — no waiting for the data team, no Excel. All reports pull from the same data that powers the live dashboards.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Executive Reports |
| Route | `/exec/reports/` |
| Django view | `ExecutiveReportsView` |
| Template | `exec/executive_reports.html` |
| Priority | P2 |
| Nav group | Analytics |
| Required role | `exec`, `superadmin`, `finance` |
| 2FA required | Exporting sensitive reports |
| HTMX poll | None (on-demand) |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Executive Reports                   [+ New Schedule] [Report Archive]│
├──────────────────────────────────────────────────────────────────────────────┤
│ TABS: [Report Templates] [Scheduled Reports] [Report History]               │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: REPORT TEMPLATES                                                        │
│                                                                              │
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐              │
│ │ Monthly P&L      │ │ Institution Growth│ │ Board Pack       │              │
│ │ Finance · PDF    │ │ Analytics · PDF   │ │ All-in-one · PDF │              │
│ │ Last generated:  │ │ Last: Mar 2025   │ │ Last: Q4 2024   │              │
│ │ Mar 2025        │ │                  │ │                  │              │
│ │ [Generate] [Sch] │ │ [Generate] [Sch] │ │ [Generate] [Sch] │              │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 Tab: Report Templates

`id="tab-templates"` · `hx-get="?part=report_templates"`

**Report template cards grid:** `grid grid-cols-3 gap-4 p-4`

| Report | Category | Description | Format |
|---|---|---|---|
| Monthly P&L | Finance | MRR/ARR, collections, overdue | PDF + XLSX |
| ARR Waterfall | Finance | MRR movement waterfall | PDF |
| Board Pack | Executive | Full platform summary (15 pages) | PDF |
| Institution Growth | Analytics | Growth trend, map, cohort | PDF |
| Student Analytics | Analytics | Engagement, scores, retention | PDF |
| Exam Performance | Exams | Exam stats, question analysis | PDF + XLSX |
| Churn Risk Report | Analytics | At-risk institutions list | PDF + XLSX |
| Compliance Summary | Compliance | DPDPA, checks, DSAR status | PDF |
| SLA Report | Operations | SLA performance per tier | PDF |
| Top Institutions | Finance | Top 20 by ARR + growth | PDF + XLSX |
| Invoice Aging | Finance | Overdue analysis | XLSX |
| API Usage Report | Technical | API calls, errors, webhooks | PDF + XLSX |
| Platform Health | Operations | Service health, incidents | PDF |
| Cohort Analysis | Analytics | Student cohort retention | PDF |
| Custom Report | Custom | Build your own | PDF + XLSX |

**Each template card anatomy (180px × 240px):**
```
┌─────────────────────────────┐
│ 📊 Monthly P&L              │  ← icon + name
│ Finance                     │  ← category badge
│ Revenue, collections, ARR   │  ← description text-xs
│                             │
│ Last generated:             │
│ 15 Mar 2025                 │  ← relative time
│ By: CFO                     │
│                             │
│ [Generate Now] [Schedule]   │  ← action buttons
└─────────────────────────────┘
```

**[Generate Now]:** opens Generate Report Modal (§6.1)
**[Schedule]:** opens Schedule Report Modal (§6.2)

---

### 4.2 Tab: Scheduled Reports

`id="tab-scheduled"` · `hx-get="?part=scheduled_reports"`

**[+ New Schedule]** button

**Schedules Table:**
| Column | Detail |
|---|---|
| Report | Template name |
| Frequency | Daily / Weekly / Monthly / Quarterly |
| Next run | Datetime |
| Recipients | Email list (truncated) |
| Format | PDF / XLSX |
| Status | Active / Paused |
| Actions ⋯ | Edit / Pause / Run Now / Delete |

**Pause toggle:** instant `hx-patch="?part=toggle_schedule&id={id}"`

---

### 4.3 Tab: Report History

`id="tab-history"` · `hx-get="?part=report_history"`

**History Table:**
| Column | Detail |
|---|---|
| Report | Template name |
| Period | e.g., "March 2025" |
| Generated at | Datetime |
| Generated by | User or "Scheduled" |
| Format | PDF/XLSX badge |
| Size | File size |
| Status | Completed / Failed / Processing |
| [Download] | Download link (expires 7 days) |
| [Resend] | Resend to original recipients |

**Pagination:** 25/page

---

## 5. Drawers

### 5.1 Custom Report Builder Drawer (800 px)

`id="report-builder"` · `w-[800px]` · `body.drawer-open`

**Header:** "Custom Report Builder" · `[×]`

**Step 1 — Sections:**
Checkbox list of available sections (drag to reorder):
- ☑ Executive Summary
- ☑ KPI Summary (6 cards)
- ☑ Revenue Overview (MRR/ARR trend)
- ☑ Institution Growth
- ☑ Student Analytics
- ☐ Exam Performance
- ☐ Compliance Summary
- ☐ Incident Summary
- ☐ API Usage

**Step 2 — Filters:**
- Date range
- Institution type filter
- State filter

**Step 3 — Recipients:**
Email list (multi-input)

**Step 4 — Format & Branding:**
- Format: PDF / XLSX
- Include platform logo: toggle
- Cover page title: text input
- Subtitle/notes: textarea

**Preview pane (right):** shows page count estimate + section outline

**Footer:** [Cancel] [Save as Template] [Generate Now]

---

## 6. Modals

### 6.1 Generate Report Modal (480 px)

**Header:** "Generate — {Report Name}"

**Fields:**
| Field | Type | Detail |
|---|---|---|
| Period | Date range picker | Depends on report type |
| Filters | Context-specific | e.g., institution type for institution reports |
| Format | PDF / XLSX / CSV | Default: PDF |
| Email to | Multi-email input | Optional (default: current user) |
| Include in archive | Checkbox | Default: On |

**Footer:** [Cancel] [Generate Report]

**After submit:** toast "Generating report... you'll receive an email when ready"
For reports < 10s: opens download immediately in new tab
For reports > 10s: background job → email delivery

---

### 6.2 Schedule Report Modal (560 px)

**Fields:**
| Field | Type |
|---|---|
| Report template | Read-only (pre-filled) |
| Frequency | Daily / Weekly (day picker) / Monthly (day of month) / Quarterly |
| Time | Time picker (IST) |
| Recipients | Multi-email input |
| Format | PDF / XLSX |
| Period | Auto (last completed period) / Custom offset |
| Start date | Date picker |
| Notes | Textarea |

**Footer:** [Cancel] [Save Schedule]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=report_templates` | `exec/partials/report_templates.html` | Tab click |
| `?part=scheduled_reports` | `exec/partials/report_scheduled.html` | Tab click |
| `?part=report_history` | `exec/partials/report_history.html` | Tab · page |
| `?part=report_builder` | `exec/partials/report_builder.html` | Custom Report card click |
| `?part=toggle_schedule&id={id}` | PATCH → JSON | Pause/resume schedule |
| `?part=generate` | POST → trigger background job | Generate modal submit |

**Django view dispatch:**
```python
class ExecutiveReportsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_exec_reports"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "report_templates": "exec/partials/report_templates.html",
                "scheduled_reports": "exec/partials/report_scheduled.html",
                "report_history": "exec/partials/report_history.html",
                "report_builder": "exec/partials/report_builder.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/executive_reports.html", ctx)

    def post(self, request):
        part = request.GET.get("part", "")
        if part == "generate":
            return self._handle_generate(request)
        if part == "schedule":
            return self._handle_schedule(request)
        return HttpResponseNotAllowed(["GET"])
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| Template catalog tab | < 300 ms | > 800 ms |
| Schedule table | < 300 ms | > 800 ms |
| History table | < 300 ms | > 800 ms |
| Report generation (standard) | < 30 s | > 2 min |
| Report generation (board pack) | < 3 min | > 10 min |
| Full page initial load | < 800 ms | > 2 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Report generation fails | Email notification "Report generation failed: {reason}" + retry option in history |
| Download link expired (> 7 days) | [Download] shows "Expired" with [Regenerate] option |
| Schedule with 0 recipients | Validation error "At least one recipient required" |
| Custom report: no sections selected | [Generate] disabled + "Select at least one section" |
| Large report (board pack) | Shows "Generating in background — you'll receive an email" immediately |
| Schedule conflicts (two reports same time) | Warning "Another report is scheduled at this time — this may delay delivery" |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`3` | Switch tabs |
| `N` | New schedule |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/executive_reports.html` | Full page shell |
| `exec/partials/report_templates.html` | Report template cards |
| `exec/partials/report_scheduled.html` | Scheduled reports table |
| `exec/partials/report_history.html` | Report history table |
| `exec/partials/report_builder.html` | Custom report builder drawer |
| `exec/partials/generate_report_modal.html` | Generate modal |
| `exec/partials/schedule_report_modal.html` | Schedule modal |

---

## 12. Component References

| Component | Used in |
|---|---|
| `TabBar` | §4.1–4.3 |
| `ReportTemplateCard` | §4.1 |
| `ScheduledReportsTable` | §4.2 |
| `ReportHistoryTable` | §4.3 |
| `DrawerPanel` | §5.1 |
| `DragSortableList` | §5.1 sections |
| `MultiEmailInput` | §5.1 + §6.1–6.2 |
| `ModalDialog` | §6.1–6.2 |
| `PaginationStrip` | History table |
