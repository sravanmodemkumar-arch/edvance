# div-a-26 — SLA Dashboard

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| SLA tiers | Standard (99.5%) / Professional (99.7%) / Enterprise (99.9%) |
| Standard institutions | ~1,650 (schools + colleges) |
| Professional institutions | ~300 (large colleges + groups) |
| Enterprise institutions | ~100 (coaching centres) |
| SLA measurement period | Monthly rolling |
| Current month uptime (target) | > 99.9% for Enterprise |
| Planned maintenance excluded | Yes (per contract) |
| SLA breach penalty | Service credits per contract |
| SLA breach notification | Automatic + email to institution |

**Why this matters:** SLA performance is a contractual obligation. A single Enterprise SLA breach (< 99.9% uptime) triggers service credit liability — potentially ₹1–5 Cr of coaching ARR at risk. This page gives real-time and historical visibility into SLA compliance, breach risk, and credits owed.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | SLA Dashboard |
| Route | `/exec/sla/` |
| Django view | `SLADashboardView` |
| Template | `exec/sla_dashboard.html` |
| Priority | P1 |
| Nav group | Operations |
| Required role | `exec`, `superadmin`, `ops` |
| 2FA required | Applying service credits |
| HTMX poll | Uptime cards: every 5 min |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: SLA Dashboard                         [Export Report] [Credits ▾]   │
├────────┬────────┬────────┬────────┬────────┬──────────────────────────────── ┤
│Standard│Profess │Enterpr │Breach  │Credits │  Current Month                  │
│Uptime  │Uptime  │Uptime  │Risk    │ Owed   │  Incident Minutes               │
│ 99.82% │ 99.91% │ 99.94% │  Low   │  ₹0    │  8 min 42 sec                   │
├────────┴────────┴────────┴────────┴────────┴──────────────────────────────── ┤
│ TABS: [Current Month] [History] [By Institution] [Service Credits] [Config]  │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: CURRENT MONTH                                                           │
│ Uptime gauges per tier + Incident minutes budget bar + recent incidents     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

**Poll:** `hx-trigger="every 300s[!document.querySelector('.drawer-open,.modal-open')]"`

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Standard Uptime | This month % | < 99.5% = red |
| 2 | Professional Uptime | This month % | < 99.7% = red |
| 3 | Enterprise Uptime | This month % | < 99.9% = red |
| 4 | Breach Risk | Low / Medium / High based on remaining budget | High = amber |
| 5 | Credits Owed | Cumulative this month | > 0 = amber |
| 6 | Incident Minutes | Total downtime minutes this month | — |

**Uptime percentage display:** `text-2xl font-bold font-mono` · colour:
- ≥ target: `text-[#34D399]`
- Within 0.1% of target: `text-[#FCD34D]`
- Below target: `text-[#EF4444]`

---

### 4.2 Tab: Current Month

`id="tab-current"` · `hx-get="?part=current_month"`

#### 4.2.1 SLA Tier Uptime Gauges (3 gauges side-by-side)

Each gauge: 180px SVG arc gauge · centre text = uptime %
Below gauge: "Target: 99.9%" · "Actual: 99.94%" · "Budget remaining: 26 min"

**Budget remaining calculation:** Monthly minutes = 43,200 · Budget at 99.9% = 43.2 min downtime allowed · Remaining = 43.2 − actual_downtime

**Breach indicator:** if remaining < 5 min: red ring + pulsing animation

#### 4.2.2 Incident Minutes Budget Bar

Three horizontal bars (one per tier):
```
Standard (99.5%)   [██████░░░░░░░░░░░░░░░░░░] 46m used / 216m budget
Professional (99.7%) [████░░░░░░░░░░░░░░░░░░░░] 12m used / 130m budget
Enterprise (99.9%)  [██░░░░░░░░░░░░░░░░░░░░░░]  9m used / 43m budget
```
Bar: `bg-[#1E2D4A] rounded-full h-4` · fill: `bg-[#6366F1]` ≤ 70% · `bg-[#F59E0B]` 70–90% · `bg-[#EF4444]` > 90%

#### 4.2.3 Incidents This Month Table

| Incident | Severity | Duration | Affected tier | Excluded? | SLA minutes |
|---|---|---|---|---|---|
| INC-0041 Auth degraded | P0 | 24 min | Enterprise | No | 24 min |
| Planned maintenance | — | 120 min | All | Yes | 0 min |

**Click row:** opens Incident Detail (div-a-13)

---

### 4.3 Tab: History

`id="tab-history"` · `hx-get="?part=sla_history"`

#### 4.3.1 Uptime Trend Chart (12 months)

**Chart:** Line · 3 series (Standard / Professional / Enterprise) · Y-axis: 99.0–100%
Horizontal dashed lines at each SLA target
**Click data point:** filter incidents table to that month

#### 4.3.2 Monthly SLA Table

| Month | Standard | Professional | Enterprise | Incidents | Credits Issued |
|---|---|---|---|---|---|
| Mar 2025 | 99.82% | 99.91% | 99.94% | 2 | ₹0 |
| Feb 2025 | 99.97% | 99.98% | 99.99% | 0 | ₹0 |
| Jan 2025 | 99.54% ⚠ | 99.54% ⚠ | 99.54% ⚠ | 1 P0 | ₹2.4L |

**SLA breach rows:** amber row tint + `⚠` in affected tier column

---

### 4.4 Tab: By Institution

`id="tab-institutions"` · `hx-get="?part=sla_institutions"`

**Purpose:** Per-institution SLA view. Which institutions experienced downtime this month, and did they breach their contracted SLA?

**Filters:** Plan / SLA tier / State / Institution

**Institution SLA Table:**
| Column | Detail |
|---|---|
| Institution | Name + type |
| SLA Tier | Badge |
| Uptime (month) | % |
| Target | Contract target |
| Status | ✅ Met / ⚠ At Risk / ❌ Breached |
| Downtime (min) | Total minutes |
| Credits Due | `₹X,XXX` or `₹0` |
| Actions ⋯ | Apply Credit / View Incidents / Send SLA Report |

**Pagination:** 25/page · sort by status (Breached first)

---

### 4.5 Tab: Service Credits

`id="tab-credits"` · `hx-get="?part=sla_credits"`

**Service Credits Table:**
| Column | Detail |
|---|---|
| Institution | Name |
| Month | e.g., "Jan 2025" |
| Breach Duration | Minutes over SLA |
| Credit Amount | `₹X,XXX` |
| Status | Pending / Applied / Waived |
| Applied by | User or "Auto" |
| Notes | Text |
| Actions ⋯ | Apply / Waive / View |

**[Apply Credit]:** requires 2FA · applies to next invoice

**Summary row (top):** Total credits pending: `₹X.X L` · Total applied YTD: `₹X.X L`

---

### 4.6 Tab: Config

`id="tab-config"` · `hx-get="?part=sla_config"`

**SLA targets (editable by superadmin):**
| Tier | Uptime Target | Credit Rate | Notification at |
|---|---|---|---|
| Standard | 99.5% | 5% per 0.1% breach | 90% budget used |
| Professional | 99.7% | 10% per 0.1% breach | 80% budget used |
| Enterprise | 99.9% | 15% per 0.1% breach | 70% budget used |

**Excluded event types:** planned maintenance · force majeure · institution-side outages
Toggle checkboxes per event type

**[Save Config]** · 2FA required · audit log entry

---

## 5. Drawers

### 5.1 Institution SLA Detail Drawer (560 px)

**Header:** Institution name + SLA tier + this month uptime % · `[×]`

**Section A:** Summary: target / actual / budget remaining / credits due
**Section B:** Incidents table (this month, affecting this institution)
**Section C:** Last 12 months uptime trend (mini line chart 200px)
**Footer:** [Apply Credit] [Send SLA Report] [View Institution →] [Close]

---

## 6. Modals

### 6.1 Apply Service Credit Modal (480 px)

**2FA required.**
| Field | Type |
|---|---|
| Institution | Read-only |
| Month | Read-only |
| Credit amount | Decimal (editable) |
| Apply to | Invoice # (auto-selected next invoice) |
| Notes | Required |

**Footer:** [Cancel] [Apply Credit]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/sla_kpi.html` | Page load · poll 5 min |
| `?part=current_month` | `exec/partials/sla_current.html` | Tab click |
| `?part=sla_history` | `exec/partials/sla_history.html` | Tab click |
| `?part=sla_institutions` | `exec/partials/sla_institutions.html` | Tab · filter |
| `?part=sla_credits` | `exec/partials/sla_credits.html` | Tab click |
| `?part=sla_config` | `exec/partials/sla_config.html` | Tab click |
| `?part=inst_sla_drawer&id={id}` | `exec/partials/inst_sla_drawer.html` | Row click |

**Django view dispatch:**
```python
class SLADashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_sla"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/sla_kpi.html",
                "current_month": "exec/partials/sla_current.html",
                "sla_history": "exec/partials/sla_history.html",
                "sla_institutions": "exec/partials/sla_institutions.html",
                "sla_credits": "exec/partials/sla_credits.html",
                "sla_config": "exec/partials/sla_config.html",
                "inst_sla_drawer": "exec/partials/inst_sla_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/sla_dashboard.html", ctx)
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 200 ms | > 500 ms |
| Current month tab | < 400 ms | > 1 s |
| History chart (12 months) | < 500 ms | > 1.2 s |
| Institutions table (25 rows) | < 400 ms | > 1 s |
| Full page initial load | < 1 s | > 2.5 s |

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| SLA breach this month | KPI card red + amber banner "Enterprise SLA breach detected — credits due" |
| No incidents this month | Current month tab shows "Zero downtime this month ✓" |
| Planned maintenance excluded | Maintenance minutes shown in table but excluded from uptime calc |
| Credits applied to institution already | [Apply Credit] shows "Credit already applied this month" |
| Uptime > 100% (impossible) | Data error — show "—" and log warning |

---

## 10. Template Files

| File | Purpose |
|---|---|
| `exec/sla_dashboard.html` | Full page shell |
| `exec/partials/sla_kpi.html` | KPI strip |
| `exec/partials/sla_current.html` | Current month tab |
| `exec/partials/sla_history.html` | History chart + table |
| `exec/partials/sla_institutions.html` | Per-institution SLA table |
| `exec/partials/sla_credits.html` | Service credits table |
| `exec/partials/sla_config.html` | Config form |
| `exec/partials/inst_sla_drawer.html` | Institution SLA drawer |
| `exec/partials/apply_credit_modal.html` | Apply credit modal |

---

## 11a. Credit Note Action Path (Amendment)

> **Gap fix:** The original spec had "Apply Credit" as a modal that applies credit to an invoice. This section specifies the full credit note generation flow — from breach detection → credit calculation → formal credit note document → billing system entry.

### Full Credit Note Workflow

```
STEP 1 — Detection (automatic)
  Nightly Celery task `compute_sla_credits()` at 00:30 IST:
  - For each institution: calculates actual uptime vs SLA target for current month
  - If breached: creates `ServiceCredit` record (status=pending)
  - CFO + ops email: "SLA breach detected — N institutions require credit notes"

STEP 2 — Review (Service Credits tab §4.5)
  CFO reviews pending credits in Service Credits table
  Click [Generate Credit Note] on any pending row:

STEP 3 — Generate Credit Note Modal (560px)
────────────────────────────────────────────────────────────────────────────
Generate Credit Note — Sunrise Coaching Centre
────────────────────────────────────────────────────────────────────────────
Breach period:      January 2026
SLA tier:           Enterprise (99.9%)
Actual uptime:      99.87%
Breach:             0.03% (10 min over budget)
Contract MRR:       ₹58,300
Credit rate:        15% MRR per 0.1% breach
Calculated credit:  ₹58,300 × 15% × 0.3 = ₹2,624

Credit note amount: ₹2,624  [editable — CFO may adjust with reason]
Reason:             "SLA breach Jan 2026 — Enterprise tier (99.87% vs 99.9% target)"
Apply to invoice:   INV-2026-02-0047 (Feb 2026 invoice)  [auto-selected next invoice]
Notify institution: ☑ Send email with credit note attached

[Cancel]                            [Generate & Apply Credit Note]
────────────────────────────────────────────────────────────────────────────
```

**[Generate & Apply Credit Note] → POST `/exec/sla/actions/generate-credit-note/`:**
1. Requires 2FA OTP (existing pattern)
2. Creates `CreditNote` model record with all fields
3. Generates PDF credit note (WeasyPrint): includes institution name, breach details, credit amount, invoice reference, EduForge letterhead
4. Attaches PDF to `CreditNote` record (S3 upload)
5. Updates `ServiceCredit.status` → `applied`, sets `applied_by`, `applied_at`
6. POSTs credit to billing system (Zoho Books / internal) via API: `billing_api.apply_credit(invoice_id, amount, note_pdf_url)`
7. Sends email to institution finance contact with credit note PDF attached
8. Logs `AuditLog` entry: "Credit note ₹2,624 generated for Sunrise Coaching Centre — INC-Jan2026"

**Batch credit note generation:**

When CFO clicks [Generate All Pending Credit Notes]:
- Confirmation modal: "Generate {N} credit notes totalling ₹{amount}. This cannot be undone."
- Celery task: `generate_batch_credit_notes.delay(credit_ids)` — async, each PDF generated serially
- Progress bar in modal: "3 of 8 credit notes generated…"
- Email summary to CFO when complete: "8 credit notes generated and sent"

**Database additions:**
```python
class CreditNote(models.Model):
    institution     = models.ForeignKey("Institution", on_delete=models.PROTECT)
    service_credit  = models.OneToOneField("ServiceCredit", on_delete=models.PROTECT)
    breach_month    = models.CharField(max_length=7)          # "2026-01"
    breach_pct      = models.DecimalField(max_digits=6, decimal_places=4)
    calculated_amt  = models.DecimalField(max_digits=12, decimal_places=2)
    final_amt       = models.DecimalField(max_digits=12, decimal_places=2)  # may differ if CFO edits
    adjustment_reason = models.TextField(blank=True)          # if final_amt differs
    applied_to_invoice = models.CharField(max_length=50)      # invoice ID
    pdf_s3_key      = models.CharField(max_length=300)        # S3 path to PDF
    billing_api_ref = models.CharField(max_length=100, blank=True)
    notified_at     = models.DateTimeField(null=True)
    generated_by    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    generated_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["breach_month","institution"])]
```

**Celery task:**
```python
@shared_task
def compute_sla_credits():
    """Runs at 00:30 IST on the 1st of each month for the previous month."""
    prev_month = last_month()
    for institution in Institution.objects.filter(is_active=True).select_related("plan"):
        actual_uptime = _compute_institution_uptime(institution, prev_month)
        target = institution.plan.sla_target_pct
        if actual_uptime < target:
            breach_pct = Decimal(str(target - actual_uptime))
            credit_rate = institution.plan.credit_rate_per_0_1pct
            credit_amt = institution.current_mrr * credit_rate * (breach_pct / Decimal("0.001"))
            ServiceCredit.objects.get_or_create(
                institution=institution, breach_month=prev_month,
                defaults={"calculated_amt": credit_amt, "breach_pct": breach_pct, "status": "pending"}
            )
```

---

## 11. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `UptimeGauge` | §4.2.1 |
| `BudgetBar` | §4.2.2 |
| `IncidentsThisMonth` | §4.2.3 |
| `UptimeTrendChart` | §4.3.1 |
| `MonthlySlATable` | §4.3.2 |
| `InstitutionSLATable` | §4.4 |
| `ServiceCreditsTable` | §4.5 |
| `SLAConfigForm` | §4.6 |
| `DrawerPanel` | §5.1 |
| `ModalDialog` | §6.1 |
| `PaginationStrip` | Tables |
| `PollableContainer` | KPI strip |
