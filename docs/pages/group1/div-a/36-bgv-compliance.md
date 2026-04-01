# 36 — BGV & POCSO Compliance

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | BGV & POCSO Compliance |
| Route | `/exec/bgv-compliance/` |
| Django view | `BGVComplianceView` |
| Template | `exec/bgv_compliance.html` |
| Priority | **P1** |
| Nav group | Compliance |
| Required roles | `coo` · `bgv_manager` · `bgv_executive` · `pocso_officer` · `ceo` · `superadmin` |
| CFO / CTO | Denied |
| HTMX poll — summary strip | Every 300s |
| HTMX poll — institution table | Every 600s |
| Cache | Summary: Redis TTL 290s · Table: Redis TTL 590s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · danger `#EF4444` · warn `#F59E0B` · success `#22C55E` |

---

## 2. Purpose & Business Logic

**Legal context — why this page cannot be optional:**

The **Protection of Children from Sexual Offences (POCSO) Act 2012** mandates that any organization employing staff with access to minors must conduct Background Verification (BGV). EduForge's institutions collectively employ **~100,000 staff** across 1,000 schools and 800 colleges — all of whom have daily access to students under 18.

If EduForge fails to enforce BGV and a verified-unclean staff member commits an offence:
- EduForge faces **criminal liability** under POCSO Section 19 (failure to report) and Section 21 (failure to comply)
- The institution faces license revocation
- Directors face up to 6 months imprisonment

**What this page tracks:**
1. BGV coverage % per institution — is every staff member verified?
2. BGV status per staff member — pending / cleared / flagged / expired
3. POCSO incident log — any reported incidents, NCPCR filing status
4. Vendor SLA — is the BGV vendor completing checks within the contracted 7-day window?
5. Overdue escalation queue — institutions that have been reminded but still not submitted BGV data

**Scale:**
- 100,000 staff across 1,800 institutions (schools + colleges)
- BGV vendor processes ~500 requests/month
- BGV validity: 3 years (after which re-verification required)
- POCSO reporting window: 24 hours to NCPCR from incident knowledge

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All sections | Read-only |
| COO | All sections | Trigger escalation, assign BGV executive |
| BGV Manager | All sections | All BGV actions, vendor management |
| BGV Executive | Institution table + BGV queue | Update BGV status, request re-verification |
| POCSO Officer | All sections + POCSO incident log | File NCPCR report, close incident |
| CFO / CTO | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — Compliance Alert Bar

**Purpose:** POCSO incidents and critical BGV gaps surface immediately — before any other content.

**UI elements:**
```
🔴 POCSO INCIDENT — ABC School, Hyderabad · Reported 2h ago · NCPCR filing DUE in 22h [View →]
🟡 47 institutions have BGV coverage < 80% · 12 have not responded to 3 reminders [Review →]
```

- Red bar: active POCSO incident with countdown timer to 24h NCPCR filing deadline
- Amber bar: BGV gap summary
- Both bars link to relevant section below

**Data flow:** Computed at page load from `POCSOnIncident.objects.filter(status='open')` + BGV coverage query. Alert bar is not cached — always fresh.

**Accessibility:** `role="alert" aria-live="assertive"` on POCSO incident bar.

---

### Section 2 — Summary Strip

**UI elements — 5 cards:**

```
╔══════════════╦══════════════╦══════════════╦══════════════╦══════════════╗
║ TOTAL STAFF  ║ BGV COVERAGE ║ PENDING BGV  ║ FLAGGED      ║ EXPIRING 90d ║
║  ~1,00,000   ║   84.2%      ║   7,240      ║    128       ║   4,100      ║
║ 1,800 inst.  ║ ▼ was 85.1%  ║ 312 inst.    ║ action req.  ║ notify soon  ║
╚══════════════╩══════════════╩══════════════╩══════════════╩══════════════╝
```

| Card | Alert condition |
|---|---|
| Total Staff | None |
| BGV Coverage | < 90%: amber · < 80%: red |
| Pending BGV | > 5,000: amber · > 10,000: red |
| Flagged | Any > 0: amber (these staff must not have student access until cleared) |
| Expiring 90d | > 2,000: amber (re-verification pipeline at risk) |

**HTMX:** `id="bgv-summary"` poll every 300s.

---

### Section 3 — Institution BGV Coverage Table

**Purpose:** The operational list — which institutions are compliant and which need follow-up.

**UI elements:**
```
INSTITUTION BGV COVERAGE          [Type: All ▾] [Status: All ▾] [🔍 Search]
──────────────────────────────────────────────────────────────────────────────
Institution      │Type   │Staff│Submitted│Cleared│Flagged│Coverage│Last Remind│ ⋯
─────────────────┼───────┼─────┼─────────┼───────┼───────┼────────┼───────────┼──
ABC School       │School │ 48  │  48     │  46   │   2   │ 95.8%✅│ —         │ ⋯
DEF College      │College│ 112 │  72     │  70   │   0   │ 62.5%🔴│ 3 Mar     │ ⋯
XYZ School       │School │ 38  │   0     │   0   │   0   │  0.0%🔴│ Not sent  │ ⋯
```

**Column details:**

| Column | Detail |
|---|---|
| Staff | Total staff count on record |
| Submitted | BGV requests sent to vendor |
| Cleared | Verified clean |
| Flagged | Adverse finding — `text-red-400 font-bold` |
| Coverage | Cleared / Staff %. Red < 80%, Amber 80–95%, Green 95%+ |
| Last Remind | Date of last automated reminder email/WhatsApp. "Not sent" = never contacted |
| ⋯ | View Detail · Send Reminder · Assign BGV Executive · Escalate |

**"Send Reminder" action:**
- Single confirm modal: "Send BGV reminder to {institution} admin via WhatsApp + Email?"
- POST `/exec/bgv-compliance/actions/send-reminder/` → Celery task → logs reminder in `BGVReminder` model

**HTMX:** `id="bgv-table"` poll every 600s. Filter chips trigger swap.

**Row click:** Opens Drawer-H (520px) — institution BGV drill-down.

---

### Section 4 — BGV Vendor SLA Tracker

**Purpose:** Is the BGV vendor completing checks within the contracted 7-day SLA?

**UI elements:**
```
VENDOR SLA — AuthBridge / IDfy            Contracted: 7 business days
─────────────────────────────────────────────────────────────────────
SLA Met (< 7d)    │  Breached (7–14d)  │  Critical (> 14d)  │ Avg TAT
   4,820 (91.2%)  │    320 (6.1%)      │    148 (2.8%)      │ 5.2 days
─────────────────────────────────────────────────────────────────────
⚠ 148 checks outstanding > 14 days — [Escalate to Vendor →]
```

- TAT = Turnaround Time
- Stacked bar chart: SLA Met (green) / Breached (amber) / Critical (red)
- "Escalate to Vendor" → creates `VendorEscalation` record + sends email template to vendor account manager

---

### Section 5 — POCSO Incident Log

**Purpose:** Every POCSO incident must be logged, tracked, and reported to NCPCR within 24 hours. This is the legal paper trail.

**UI elements:**
```
POCSO INCIDENT LOG                                    [+ Report Incident]
──────────────────────────────────────────────────────────────────────────────
INC#   │Institution    │Reported   │Status        │NCPCR Filed │POCSO Officer
───────┼───────────────┼───────────┼──────────────┼────────────┼─────────────
POC-01 │ABC School     │2h ago     │🔴 Open-22h   │ Pending    │ Smt. Radha
POC-02 │XYZ College    │15 Mar     │✅ Closed      │ 16 Mar     │ Smt. Radha
```

- "Open" rows: countdown timer `text-red-400` showing hours remaining to 24h NCPCR deadline
- "Report Incident" → modal: Institution, Date/Time, Nature of Incident (select: Physical / Online / Other), Description, Alleged Perpetrator Staff ID (links to BGV record), Immediate Action Taken
- POST `/exec/bgv-compliance/actions/report-pocso/` → creates `POCSoIncident`, triggers 24h deadline timer, notifies POCSO Officer + COO + CEO

**NCPCR filing tracker:**
- "Mark NCPCR Filed" action per open incident (POCSO Officer only) → uploads reference number + date

**Accessibility:** Countdown timer has `aria-live="assertive"` — screen reader announces when < 2 hours remain.

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  BGV & POCSO Compliance                                                      ║
║  🔴 POCSO INCIDENT — ABC School · NCPCR due in 22h [View →]                 ║
║  🟡 47 institutions < 80% BGV coverage [Review →]                           ║
╠══════════╦══════════╦══════════╦══════════╦══════════════════════════════════╣
║ STAFF    ║ COVERAGE ║ PENDING  ║ FLAGGED  ║ EXPIRING 90d                    ║
║ 1,00,000 ║  84.2%   ║  7,240   ║   128    ║  4,100                          ║
╠══════════╩══════════╩══════════╩══════════╩══════════════════════════════════╣
║  INSTITUTION BGV COVERAGE    [Type ▾] [Status ▾] [🔍]                       ║
║  Institution  │Type  │Staff│Cleared│Flagged│Coverage│Last Remind            ║
║  ABC School   │School│  48 │  46   │   2   │ 95.8%✅│ —                    ║
║  DEF College  │College│ 112│  70   │   0   │ 62.5%🔴│ 3 Mar                ║
║  XYZ School   │School│  38 │   0   │   0   │  0.0%🔴│ Not sent             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  VENDOR SLA — AuthBridge          Met: 91.2%  │ Breach: 6.1%  │ Crit: 2.8%  ║
║  ████████████████████████████░░░░░░░░░░░░░░░░░░   Avg TAT: 5.2 days         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  POCSO INCIDENT LOG                                    [+ Report Incident]  ║
║  POC-01 │ ABC School │ 2h ago │ 🔴 Open — 22h left │ Pending NCPCR         ║
║  POC-02 │ XYZ College│ 15 Mar │ ✅ Closed           │ Filed 16 Mar          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Drawer-H — Institution BGV Detail (520px)

```
┌──────────────────────────────────────────────────────┐
│  DEF College — BGV Detail          62.5% 🔴      [✕] │
│  [Overview ●] [Staff List] [History] [POCSO Log]      │
│  ───────────────────────────────────────────────────  │
│  Staff: 112  Submitted: 72  Cleared: 70  Flagged: 0   │
│  Pending (not submitted): 40 staff                    │
│  Last reminder: 3 Mar 2026                            │
│  Assigned BGV Executive: —                            │
│  ───────────────────────────────────────────────────  │
│  [Send Reminder]  [Assign BGV Exec]  [Escalate COO]   │
└──────────────────────────────────────────────────────┘
```

**Staff List tab:** Table of individual staff records — Name, Role, BGV Status, Submitted Date, Cleared Date, Expiry Date. Flagged staff shown with red row + reason summary.

**History tab:** All reminders sent, escalations raised, BGV executive assignments — timestamped.

---

## 7. Component Architecture

| Component | File | Props |
|---|---|---|
| `BGVSummaryCard` | `components/bgv/summary_card.html` | `label, value, subline, alert_level` |
| `InstitutionBGVRow` | `components/bgv/institution_row.html` | `institution, staff_count, cleared, flagged, coverage_pct, last_reminder` |
| `CoverageBar` | `components/bgv/coverage_bar.html` | `pct` |
| `VendorSLAStrip` | `components/bgv/vendor_sla.html` | `met_count, breach_count, critical_count, avg_tat` |
| `POCSoIncidentRow` | `components/bgv/pocso_row.html` | `incident, hours_remaining, ncpcr_status` |
| `BGVDrawer` | `components/bgv/drawer.html` | `institution_id` |
| `ReportIncidentModal` | `components/bgv/report_modal.html` | (no props — form only) |

---

## 8. HTMX Architecture

| `?part=` | Target | Poll | Trigger |
|---|---|---|---|
| `summary` | `#bgv-summary` | 300s | load |
| `table` | `#bgv-table` | 600s | load + filter |
| `vendor-sla` | `#vendor-sla` | None | load |
| `pocso-log` | `#pocso-log` | 60s | load |
| `bgv-drawer` | `#drawer-container` | None | row click |

---

## 9. Backend View & API

```python
class BGVComplianceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_bgv_compliance"

    def get(self, request):
        allowed = {"coo","bgv_manager","bgv_executive","pocso_officer","ceo","superadmin"}
        if request.user.role not in allowed:
            return redirect("exec:dashboard")

        if _is_htmx(request):
            part = request.GET.get("part","")
            ctx = self._build_context(request)
            dispatch = {
                "summary":    "exec/bgv/partials/summary.html",
                "table":      "exec/bgv/partials/table.html",
                "vendor-sla": "exec/bgv/partials/vendor_sla.html",
                "pocso-log":  "exec/bgv/partials/pocso_log.html",
                "bgv-drawer": "exec/bgv/partials/drawer.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "exec/bgv_compliance.html", self._build_context(request))
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/bgv-compliance/actions/send-reminder/` | `portal.manage_bgv` | Celery WhatsApp+Email task, log `BGVReminder` |
| POST | `/exec/bgv-compliance/actions/report-pocso/` | `portal.report_pocso` | Create `POCSoIncident`, notify COO+CEO+POCSO Officer, start 24h timer |
| POST | `/exec/bgv-compliance/actions/mark-ncpcr-filed/` | `portal.manage_pocso` | Update `POCSoIncident.ncpcr_filed=True`, log reference |
| POST | `/exec/bgv-compliance/actions/escalate-vendor/` | `portal.manage_bgv` | Create `VendorEscalation`, email vendor |

---

## 10. Database Schema

```python
class StaffBGVRecord(models.Model):
    institution   = models.ForeignKey("Institution", on_delete=models.CASCADE, db_index=True)
    staff_name    = models.CharField(max_length=200)
    staff_role    = models.CharField(max_length=100)
    id_type       = models.CharField(max_length=30)  # Aadhaar / PAN / Passport
    id_number     = models.CharField(max_length=50)  # encrypted at rest
    status        = models.CharField(max_length=20,
                        choices=[("pending","Pending"),("submitted","Submitted"),
                                 ("cleared","Cleared"),("flagged","Flagged"),
                                 ("expired","Expired")])
    submitted_at  = models.DateTimeField(null=True)
    cleared_at    = models.DateTimeField(null=True)
    expiry_date   = models.DateField(null=True)
    vendor_ref    = models.CharField(max_length=100, blank=True)
    flag_reason   = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["institution","status"])]


class POCSoIncident(models.Model):
    institution       = models.ForeignKey("Institution", on_delete=models.CASCADE)
    reported_by       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    incident_datetime = models.DateTimeField()
    nature            = models.CharField(max_length=20,
                            choices=[("physical","Physical"),("online","Online"),("other","Other")])
    description       = models.TextField()
    alleged_staff     = models.ForeignKey(StaffBGVRecord, null=True, on_delete=models.SET_NULL)
    immediate_action  = models.TextField()
    ncpcr_filed       = models.BooleanField(default=False)
    ncpcr_reference   = models.CharField(max_length=100, blank=True)
    ncpcr_filed_at    = models.DateTimeField(null=True)
    pocso_officer     = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                           on_delete=models.SET_NULL,
                                           related_name="pocso_assignments")
    status            = models.CharField(max_length=20, default="open")
    created_at        = models.DateTimeField(auto_now_add=True, db_index=True)
```

---

## 11. Validation Rules

| Action | Validation |
|---|---|
| Report POCSO Incident | Institution required. Datetime required (cannot be future). Description min 50 chars. Nature required. Immediate action required. |
| Mark NCPCR Filed | Reference number required. Filed date required, cannot be > today or before incident date. Only POCSO Officer role. |
| Send Reminder | Cannot send reminder to same institution more than once per 24h (rate limit). Institution must have BGV coverage < 100%. |
| Send Reminder (manual) | BGV Manager / COO / BGV Executive only. |

---

## 12. Security Considerations

| Concern | Implementation |
|---|---|
| Staff ID numbers | Stored encrypted at rest (AES-256 via Django's encrypted field). Never displayed in full — last 4 chars only shown in UI. |
| POCSO incident sensitivity | Only POCSO Officer + COO + CEO can view incident descriptions. BGV Executive sees incident exists but not details. |
| Incident immutability | `POCSoIncident` records cannot be deleted or edited after creation. Status can only progress forward (open → closed). |
| Audit trail | Every BGV status change logged in `AuditLog`. Every POCSO action logged. |
| BGV vendor data | Vendor sends results via secure webhook (HMAC-signed). Signature validated before processing. |

---

## 13. Edge Cases

| State | Behaviour |
|---|---|
| POCSO incident 24h deadline < 1h | Alert bar turns full red pulsing. Push notification sent to POCSO Officer's mobile via FCM. |
| Flagged BGV staff still active | `ComplianceAlert` created. Institution admin notified: "Staff member {name} has adverse BGV finding. Immediate action required." |
| BGV vendor API down | Sync fails → `VendorAPIError` logged. Page shows "Vendor sync unavailable — status last updated X hours ago." |
| Institution with 0 staff records | Coverage shows "No data" (not 0%) — data not yet submitted by institution. Prompt to contact. |
| Staff BGV expiring in < 30 days | Row highlighted amber in Drawer-H staff list. Bulk "Send Re-verification Request" action available. |

---

## 14. Performance & Scaling

| Endpoint | Target |
|---|---|
| Page shell | < 500ms |
| `?part=summary` | < 150ms (Redis) |
| `?part=table` (50 rows) | < 400ms |
| `?part=pocso-log` | < 200ms |
| BGV drawer | < 300ms |

- BGV coverage % pre-computed nightly by Celery beat: `InstitutionBGVCoverage` materialized view updated at 01:00 IST
- 100,000 staff records: table queries always scoped by institution — never full-table scans
- Staff ID numbers: never included in any query result set unless explicitly needed (encryption overhead minimized)

---

*Last updated: 2026-03-20*
