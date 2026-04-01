# F-11 — Offline Exam Manager

## 1. Page Metadata

| Field | Value |
|---|---|
| **Route** | `GET /ops/exam/offline/` |
| **Django View** | `OfflineExamDashboardView` (main) · `OfflinePackageDetailView` (`/ops/exam/offline/packages/<package_id>/`) · `OfflineDistributionView` (`/ops/exam/offline/packages/<package_id>/distributions/`) |
| **Template** | `portal_base_dark.html` → `ops/offline_exam_dashboard.html` |
| **Primary Role** | Exam Configuration Specialist (90, Level 3) |
| **Also Accessible** | Exam Operations Manager (34, full access) · Results Coordinator (36, sync + results integration) · Platform Admin (10, full access) |
| **Priority** | P1 |
| **Status** | ⬜ Not started |
| **Indian Context** | Rural government schools (UP, Bihar, Jharkhand, Odisha) · Tier-3 coaching centres · District exam centres with unreliable 2G connectivity · State PSC exam remote venues · Institutions preferring air-gapped exams for security |

---

## 2. Purpose & Business Logic

Offline exam capability is not an edge case in India — it is a core product requirement driven by the country's infrastructure reality:

**Why offline exams are essential for Indian EdTech at scale:**
- **Rural government schools:** UP, Bihar, Jharkhand, MP, Odisha, Chhattisgarh have thousands of government schools with no broadband — only intermittent 2G/3G. A live online exam is impossible.
- **District-level competitive exam centres:** State PSC exams (BPSC, MPPSC, UPPSC) are often conducted at district headquarters where even 4G is unreliable. Centres may have 50–200 students with shared bandwidth.
- **Coaching institutes in Tier-3 cities:** Kota, Patna, Sikar, Gorakhpur — these have coaching markets but frequent power outages and poor internet. An offline package + sync model is preferred.
- **Security-conscious institutions:** Some premium institutions (IAS coaching, CA prep centres) deliberately prefer air-gapped exams to prevent internet-assisted cheating during high-stakes tests.
- **Contingency fallback:** Even urban centres can lose internet during exams (ISP outage, building-level router failure). Offline mode ensures exam continuity with zero student disruption.

**EduForge Offline Exam Workflow (end-to-end):**
1. **Exam Config Specialist (90)** creates an exam with mode `OFFLINE_PACKAGE` on F-01
2. **Config Specialist** generates an encrypted offline exam package via this page (F-11)
3. Package is encrypted (AES-256), time-locked (only openable within ±30 min of exam window), and contains question paper JSON, marking scheme, student list (optional), session tokens
4. **Institution Admin** (from institution portal — Group 3) downloads the package `.efpkg` file to their local exam server or PC
5. Students log in to the **EduForge Offline Client** (PWA in offline mode or desktop app) — authenticates against locally cached credentials in the package
6. Exam runs 100% locally — no internet required during exam
7. Student responses are stored locally in the offline client as an encrypted response archive
8. After exam ends, **Institution Admin** uploads the response package `.efrpkg` from institution portal
9. EduForge receives the response package → validates signature → decrypts → creates `exam_submission` records identical to digital online submissions
10. Results pipeline (F-04) processes normally — students and institutions see results the same way as for online exams
11. **Config Specialist / Results Coordinator** monitors sync status on F-11

**Critical business rules:**
- A package can only be downloaded by the institution(s) it is assigned to — verified via institution JWT in the download request
- A package expires 48 hours after its exam end time; expired packages cannot be synced (manual override by Exam Ops Manager + Platform Admin only)
- If the same student submits both via online fallback and offline package sync → offline response takes precedence if it was submitted within the exam window; otherwise the online response is kept; a conflict flag is raised for manual review
- Package generation is irreversible once distributed — a new package version must be generated if question paper changes after distribution; old packages are automatically revoked
- All package files are signed with HMAC-SHA256 using institution-specific keys — tampered packages are rejected at sync time
- Maximum 5 active offline packages per exam at any time (prevents version sprawl across institutions)

**Package lifecycle states:**
```
DRAFT → GENERATING → READY → DISTRIBUTED → PARTIALLY_SYNCED → FULLY_SYNCED → EXPIRED → REVOKED
```

---

## 3. User Roles & Access

| Role | Access Level | Capabilities |
|---|---|---|
| Exam Config Specialist (90) | Full + Manage | Create, generate, distribute, revoke packages; configure offline exam settings; view sync status; download distribution report |
| Exam Operations Manager (34) | Full + Override | All Config Specialist actions + approve expired-package manual sync overrides; emergency revoke; view all institution distribution details |
| Results Coordinator (36) | Read + Trigger | View sync status; trigger response processing into results pipeline; view conflict flags; download sync summary |
| Platform Admin (10) | Full + System | All above + access encryption key management; system-level package settings; force-expire all packages for a given exam |
| Exam Integrity Officer (91) | Read | View package distribution status; flag institutions with suspicious sync patterns (submitted too fast, sync time mismatch) |

---

## 4. Page Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ portal_base_dark.html — top nav + left sidebar (Division F active)   │
├──────────────────────────────────────────────────────────────────────┤
│ Page Header                                                           │
│  "Offline Exam Manager"                                               │
│  [+ Create Offline Package]  [Sync Status ▼]  [Export Report]        │
├──────────────────────────────────────────────────────────────────────┤
│ KPI Strip (4 cards, icon + number + label)                           │
│  [Active Packages: 12] [Pending Sync: 7] [Synced Today: 34]         │
│  [Conflict Flags: 2]                                                  │
├──────────────────────────────────────────────────────────────────────┤
│ Tab Bar                                                               │
│  [Active Packages ●] [Package Builder] [Sync Monitor] [Audit Log]   │
├──────────────────────────────────────────────────────────────────────┤
│ Tab Content Area (changes per tab)                                   │
│                                                                       │
│  Active Packages: filterable table of all in-flight packages         │
│  Package Builder: step wizard for generating a new offline package   │
│  Sync Monitor: institution-wise sync progress, conflict resolution   │
│  Audit Log: all package actions with actor, timestamp, IP            │
├──────────────────────────────────────────────────────────────────────┤
│ Detail Panel (slides in from right — package or distribution detail) │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 5. Main Sections

### 5.1 KPI Strip

Four stat cards rendered at page top, polled every 60 seconds via HTMX:

| Card | Value Source | Colour | Action on Click |
|---|---|---|---|
| Active Packages | `offline_exam_package` where status IN (READY, DISTRIBUTED, PARTIALLY_SYNCED) | Blue | Filters Active Packages tab to status=active |
| Pending Sync | `package_distribution` where sync_status = PENDING, exam_end_at < now | Amber | Opens Sync Monitor tab filtered to pending |
| Synced Today | `package_distribution` where synced_at::date = today | Green | Opens Sync Monitor tab filtered to today |
| Conflict Flags | `offline_response_conflict` where resolved = false | Red (if > 0) | Opens conflict resolution drawer |

---

### 5.2 Tab: Active Packages

**Purpose:** Table of all offline exam packages that are not yet fully processed. Default view excludes EXPIRED and REVOKED (toggle to show all).

**Filters (horizontal filter bar, HTMX-driven):**
- Exam Domain (SSC · RRB · NEET · JEE · State Board · All)
- Institution (searchable dropdown — type 3 chars to search)
- Status (All · READY · DISTRIBUTED · PARTIALLY_SYNCED · FULLY_SYNCED)
- Exam Date (date range picker)

**Table columns:**

| Column | Description |
|---|---|
| Package ID | Short UUID, copyable |
| Exam Name | Exam name + domain badge |
| Exam Window | Start date–time to end date–time (IST) |
| Institutions | Count of assigned institutions (clickable → distribution list) |
| Synced / Total | e.g., `14 / 20` institutions synced (progress bar) |
| Status | Badge: READY / DISTRIBUTED / PARTIALLY_SYNCED / FULLY_SYNCED / EXPIRED |
| Package Version | v1, v2 (incremented if question paper changed after initial generation) |
| Expires At | Countdown timer if within 24 hours; otherwise date |
| Actions | [Detail] [Revoke ▼] [Download Report] |

**Row expand:** Click any row → inline accordion expands to show per-institution sync status table (institution name, download time, sync time, responses received count, conflict flag count).

**Bulk actions (checkbox + toolbar):**
- Revoke selected packages
- Export distribution report (CSV)

---

### 5.3 Tab: Package Builder

A 4-step wizard for creating a new offline exam package. Each step validated before advancing.

#### Step 1: Select Exam

- Search and select an exam from the schedule (F-01) that has mode = `OFFLINE_PACKAGE` or `HYBRID` (online + offline fallback)
- Shows exam details: name, domain, question paper, duration, marking scheme, scheduled date/time
- Warning banner if exam is less than 2 hours away: "Short lead time — ensure institutions download package immediately"
- If the exam already has an active package → show existing package info and offer "Generate New Version" (which revokes old)

#### Step 2: Assign Institutions

- Multi-select list of institutions enrolled in this exam
- Columns: Institution Name · City · State · Internet Reliability Tag (Poor / Moderate / Good — set by institution profile) · Download Status (if a prior package version exists)
- Quick filter: "Show only POOR internet institutions" auto-selects all of them
- Optional: include student list in package (toggles between "Open access" — any student with session token vs "Restricted" — only listed students can attempt)
- Set package expiry override (default: exam end time + 48 hours; max: + 7 days with Exam Ops Manager approval)

#### Step 3: Package Configuration

| Setting | Default | Description |
|---|---|---|
| Encryption Strength | AES-256-GCM | Non-editable (always maximum) |
| Time Lock Window | ±30 minutes | Package can only be opened within 30 min before exam start to exam end |
| Allow Partial Sync | Yes | If institution loses connectivity mid-upload, they can resume sync |
| Response Submission Window | Exam end + 15 min | How long after exam end a student can still submit on the offline client |
| Include Answer Key | No | If Yes, answer key is embedded (only for practice exams — blocked for evaluation exams) |
| Allow Late Sync Override | No | If Yes, expired packages can be synced with Exam Ops Manager approval |
| Offline Client Version | Latest (auto-detect) | Minimum client version required to open this package |

#### Step 4: Review & Generate

- Summary of all settings
- Question paper checksum (SHA-256 hash of question paper JSON — institution can verify integrity)
- Estimated package size (based on number of questions + images)
- [Generate Package] button → calls `POST /api/v1/offline-packages/` → starts async Lambda task
- After generation starts: progress indicator (GENERATING status); page polls every 3 sec; when READY, shows download link

---

### 5.4 Tab: Sync Monitor

**Purpose:** Real-time view of which institutions have downloaded packages, started syncing, completed syncing, and whether any conflicts arose.

**Layout:** Two-column layout — left column is institution list, right column is detail panel for selected institution.

**Left column — Institution sync list:**

Each institution card shows:
- Institution name + city/state
- Package downloaded: Yes (timestamp) / No (red)
- Sync status: PENDING / UPLOADING / PROCESSING / COMPLETED / FAILED
- Student count: expected vs received
- Conflicts: count of response conflicts (red badge if > 0)
- [View Detail] button

**Right column — Selected institution detail:**

When an institution is selected:
- **Download log:** when package was downloaded, IP address, client version
- **Sync log:** when sync was initiated, file size received, processing time
- **Response summary table:**
  - Student ID | Student Name | Responses Received | Submission Time (offline) | Sync Time | Status
  - Colour-coded: green = clean, amber = submitted near exam end, red = conflict/missing
- **Conflict resolution panel** (if conflicts exist):
  - Lists each conflicting student
  - Shows both online and offline responses side by side
  - Resolution buttons: [Accept Offline Response] [Accept Online Response] [Flag for Manual Review]
  - Resolved conflicts feed directly into F-04 results pipeline

**Refresh:** Sync monitor auto-refreshes every 15 seconds (HTMX polling) while any institution is in UPLOADING or PROCESSING state.

---

### 5.5 Tab: Audit Log

Complete audit trail for all package operations. Non-editable, append-only.

| Column | Description |
|---|---|
| Timestamp | IST datetime |
| Actor | Staff name + role + role ID |
| Action | PACKAGE_CREATED · PACKAGE_GENERATED · PACKAGE_DISTRIBUTED · PACKAGE_DOWNLOADED · SYNC_INITIATED · SYNC_COMPLETED · CONFLICT_RESOLVED · PACKAGE_REVOKED · PACKAGE_EXPIRED · OVERRIDE_APPROVED |
| Package ID | Short UUID |
| Institution | Institution name (for distribution/download/sync events) |
| Details | JSON diff or summary (e.g., "Late sync override approved by Exam Ops Manager for XYZ Institute") |
| IP Address | Actor's IP |

Filters: date range, action type, actor, institution.
Export: CSV (last 90 days max).

---

## 6. Drawers

### 6.1 Package Detail Drawer

Triggered by [Detail] button on any package row.

**Header:** Package ID · Exam name · Status badge · [Revoke Package] (if READY or DISTRIBUTED)

**Sections:**
- **Package Info:** generated by, generated at, question paper version, question count, total marks, duration, encryption checksum
- **Exam Window:** start time (IST), end time (IST), time lock window, expiry time
- **Distribution Summary:** table of all assigned institutions with download + sync status; per-institution [Resend Download Link] button
- **Version History:** if multiple versions exist, shows timeline with reason for each version bump

---

### 6.2 Conflict Resolution Drawer

Triggered from Sync Monitor when a student has both online and offline responses.

**Layout:**
- Student info: name, roll number, institution
- Exam: name + exam window
- **Online response** (left panel): submission time, source IP, answers grid (Q1–Qn with selected options marked)
- **Offline response** (right panel): recorded timestamp from offline client, answers grid
- **Diff highlights:** questions where online and offline answers differ (highlighted in amber)
- **Context signals:**
  - "Online submission at: 14:58:23 (2 min before exam end)"
  - "Offline sync at: 16:32:17 (90 min after exam end)"
  - "Offline client session duration: 2h 14m 38s (matches exam duration)"
- **Resolution action:**
  - [Accept Offline Response] — offline is usually more reliable if the student was in offline mode throughout
  - [Accept Online Response] — if online submission appears legitimate
  - [Flag for Manual Integrity Review] — sends to F-07 Exam Integrity queue
- Notes field for Exam Ops Manager to record rationale before resolving

---

### 6.3 Late Sync Override Drawer

Triggered when institution tries to sync an expired package.

**Shows:**
- Package details (exam, institution, expiry time)
- Why expired: how many hours/days past expiry
- Institution explanation (free-text field the institution admin filled in the institution portal)
- Attachment slot: institution can upload evidence (e.g., screenshot of ISP outage notice)
- **Override decision:**
  - [Approve Late Sync] — requires Exam Operations Manager (34) role or above
  - [Reject — Package Expired] — package remains EXPIRED; institution must use paper-based evidence
- On approval: package status → LATE_SYNC_OVERRIDE; sync proceeds normally; audit log entry created

---

## 7. Charts & Visualisations

### 7.1 Sync Progress Donut (per package)

Visible in Package Detail Drawer:
- Segments: Synced · Pending · Failed · Not Downloaded
- Centre label: `X of Y institutions synced`
- Updates live while sync is in progress

### 7.2 Submission Timeline Scatter (Sync Monitor detail panel)

For a selected institution, after sync completes:
- X-axis: time (exam start to exam end + 15 min buffer)
- Y-axis: cumulative student submissions count
- Scatter points: each student's offline submission timestamp
- Expected normal curve overlaid in grey (based on typical submission patterns)
- Outliers flagged: submissions all at the exact same time = potential bulk-copy risk (integrity flag)
- Rendered: Chart.js 4.x, canvas element, no server-side image generation

### 7.3 Platform-Wide Offline Exam Trend (bottom of Active Packages tab)

Line chart — last 30 days:
- Line 1: Total offline packages generated
- Line 2: Packages fully synced on time
- Line 3: Packages with conflict flags
- Tooltip: hover on any day → breakdown of exam names and institution counts
- Rendered: Chart.js 4.x

---

## 8. Toast Notifications

| Trigger | Toast Type | Message |
|---|---|---|
| Package generation started | Info | "Generating offline package for [Exam Name]. This takes 30–60 seconds." |
| Package generation complete | Success | "Package ready — [X] institutions can now download." |
| Package generation failed | Error | "Package generation failed — [reason]. Retry or contact DevOps." |
| Institution downloads package | Info (admin view) | "[Institution Name] downloaded offline package at [time]." |
| Sync initiated by institution | Info | "[Institution Name] has started syncing offline responses." |
| Sync completed | Success | "[Institution Name] sync complete — [X] student responses received." |
| Sync failed | Error | "[Institution Name] sync failed — [reason]. Institution must retry." |
| Conflict flag raised | Warning | "[N] response conflicts detected for [Institution Name]. Review required." |
| All conflicts resolved | Success | "All conflicts resolved. F-04 results pipeline updated." |
| Package revoked | Warning | "Package [ID] revoked. All institutions notified." |
| Package expiring in 2 hours | Warning | "[N] institutions have not synced. Package expires at [time] IST." |
| Late sync override approved | Info | "Late sync approved by [Manager Name]. Sync will proceed." |

---

## 9. API Endpoints

All endpoints: `/api/v1/`; JWT auth required; roles enforced at view level.

| # | Method | Endpoint | Description | Auth |
|---|---|---|---|---|
| 1 | `GET` | `offline-packages/` | List all offline packages (paginated, filterable) | Role 90/34/36/10 |
| 2 | `POST` | `offline-packages/` | Create package config (Step 1–3 of wizard) | Role 90/34/10 |
| 3 | `GET` | `offline-packages/<id>/` | Package detail (all metadata, distribution list) | Role 90/34/36/91/10 |
| 4 | `POST` | `offline-packages/<id>/generate/` | Trigger async package generation (Lambda task) | Role 90/34/10 |
| 5 | `GET` | `offline-packages/<id>/download/` | Secure download of `.efpkg` file (institution portal only, HMAC-verified) | Institution JWT |
| 6 | `POST` | `offline-packages/<id>/sync/` | Institution uploads `.efrpkg` file; triggers async processing | Institution JWT |
| 7 | `GET` | `offline-packages/<id>/distributions/` | Per-institution distribution + sync status list | Role 90/34/36/10 |
| 8 | `GET` | `offline-packages/<id>/distributions/<inst_id>/` | Single institution distribution detail | Role 90/34/36/10 |
| 9 | `POST` | `offline-packages/<id>/revoke/` | Revoke package (READY or DISTRIBUTED only) | Role 34/10 |
| 10 | `GET` | `offline-packages/<id>/results/` | Results integration status (how many responses processed by F-04) | Role 36/34/10 |
| 11 | `POST` | `offline-packages/<id>/process-responses/` | Manually trigger response → exam_submission conversion | Role 36/34/10 |
| 12 | `GET` | `offline-packages/<id>/conflicts/` | List all response conflicts for this package | Role 90/34/36/10 |
| 13 | `POST` | `offline-packages/<id>/conflicts/<conflict_id>/resolve/` | Resolve a response conflict (accept online/offline/flag) | Role 34/10 |
| 14 | `POST` | `offline-packages/<id>/late-sync-override/` | Request or approve late sync for expired package | Role 34/10 |
| 15 | `GET` | `offline-packages/<id>/audit-log/` | Audit log for this specific package | Role 90/34/10 |
| 16 | `GET` | `offline-packages/stats/` | KPI strip data: active, pending, synced today, conflicts | Role 90/34/36/10 |
| 17 | `GET` | `offline-packages/trend/` | 30-day trend data for chart | Role 34/36/10 |

**Async task endpoints (internal, SQS-triggered):**
- `POST /internal/offline-packages/generate-task/` — Lambda generates `.efpkg` from exam data
- `POST /internal/offline-packages/process-sync-task/` — Lambda decrypts `.efrpkg`, creates exam_submissions

---

## 10. HTMX Patterns

### 10.1 KPI Strip Auto-Refresh

```html
<div id="offline-kpi-strip"
     hx-get="/ops/exam/offline/kpi/"
     hx-trigger="every 60s"
     hx-target="#offline-kpi-strip"
     hx-swap="outerHTML">
  <!-- 4 KPI cards rendered here -->
</div>
```

### 10.2 Package Generation Progress Polling

After [Generate Package] click — starts Lambda; page polls for status:

```html
<div id="package-gen-status"
     hx-get="/ops/exam/offline/packages/{{ package_id }}/gen-status/"
     hx-trigger="every 3s [#package-gen-status.getAttribute('data-status') === 'GENERATING']"
     hx-target="#package-gen-status"
     hx-swap="outerHTML"
     data-status="{{ package.status }}">
  <!-- Spinner + "Generating package…" text shown while status=GENERATING -->
  <!-- On READY: replaces with download link + distribution table -->
</div>
```

When status reaches `READY`, Django view renders the "Package Ready" block with download instructions instead of the spinner. The `hx-trigger` condition stops polling automatically.

### 10.3 Sync Monitor Live Refresh

```html
<div id="sync-monitor-institutions"
     hx-get="/ops/exam/offline/packages/{{ package_id }}/sync-status/"
     hx-trigger="every 15s"
     hx-target="#sync-monitor-institutions"
     hx-swap="outerHTML">
  <!-- Institution card list; polling stops once all institutions reach COMPLETED or FAILED -->
</div>
```

Server-side view returns `HX-Trigger: stopPolling` response header once all institutions in terminal state → HTMX stops the interval without client-side JavaScript.

### 10.4 Tab Navigation

```html
<div class="tab-nav">
  <button hx-get="/ops/exam/offline/tab/active-packages/"
          hx-target="#tab-content"
          hx-push-url="?tab=active-packages"
          class="tab-btn active">Active Packages</button>
  <button hx-get="/ops/exam/offline/tab/builder/"
          hx-target="#tab-content"
          hx-push-url="?tab=builder">Package Builder</button>
  <button hx-get="/ops/exam/offline/tab/sync-monitor/"
          hx-target="#tab-content"
          hx-push-url="?tab=sync-monitor">Sync Monitor</button>
  <button hx-get="/ops/exam/offline/tab/audit/"
          hx-target="#tab-content"
          hx-push-url="?tab=audit">Audit Log</button>
</div>
<div id="tab-content">
  <!-- Tab content loaded here -->
</div>
```

### 10.5 Conflict Resolution Inline

```html
<form hx-post="/api/v1/offline-packages/{{ pkg_id }}/conflicts/{{ conflict_id }}/resolve/"
      hx-target="#conflict-row-{{ conflict_id }}"
      hx-swap="outerHTML"
      hx-confirm="Resolve this conflict? This will update the student's submitted response.">
  <input type="hidden" name="resolution" value="ACCEPT_OFFLINE">
  <button type="submit">Accept Offline Response</button>
</form>
```

On success: server returns updated row HTML with "Resolved" badge; no full page reload.

### 10.6 Wizard Step Navigation

```html
<!-- Step 1 form submit goes to Step 2 -->
<form hx-post="/ops/exam/offline/builder/step/1/"
      hx-target="#wizard-body"
      hx-swap="innerHTML"
      hx-indicator="#wizard-spinner">
  <!-- Step 1 fields -->
  <button type="submit">Next: Assign Institutions →</button>
</form>
```

Each step posts to its own view, server validates, returns next step HTML. State held in Django session — no client-side state management needed.

---

## 11. DB Models

```python
class OfflineExamPackage(models.Model):
    """
    One package = one offline exam for one set of institutions.
    Multiple versions possible if question paper changes after generation.
    """
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('GENERATING', 'Generating'),
        ('READY', 'Ready for Download'),
        ('DISTRIBUTED', 'Distributed'),
        ('PARTIALLY_SYNCED', 'Partially Synced'),
        ('FULLY_SYNCED', 'Fully Synced'),
        ('EXPIRED', 'Expired'),
        ('REVOKED', 'Revoked'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    exam_schedule = models.ForeignKey('ExamSchedule', on_delete=models.PROTECT, related_name='offline_packages')
    version = models.PositiveSmallIntegerField(default=1)  # Increments if question paper changes after generation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    generated_by = models.ForeignKey('StaffUser', on_delete=models.PROTECT)
    generated_at = models.DateTimeField(null=True, blank=True)

    # Package contents metadata
    question_paper_checksum = models.CharField(max_length=64)  # SHA-256 of question paper JSON
    question_count = models.PositiveSmallIntegerField()
    estimated_size_kb = models.PositiveIntegerField()

    # Time locks
    lock_open_before_minutes = models.PositiveSmallIntegerField(default=30)  # Open N min before exam start
    lock_close_at = models.DateTimeField()  # Exam end time + response submission buffer
    expires_at = models.DateTimeField()  # When sync is no longer accepted (default: exam end + 48h)

    # Encryption
    encryption_key_hash = models.CharField(max_length=128)  # Salted hash of AES key; actual key in AWS KMS
    hmac_signing_key_ref = models.CharField(max_length=200)  # AWS KMS key ARN for package HMAC

    # Configuration flags
    student_list_embedded = models.BooleanField(default=False)  # True = restricted to listed students
    answer_key_embedded = models.BooleanField(default=False)  # True only for practice mode exams
    allow_late_sync = models.BooleanField(default=False)  # Set to True by override approval

    # File references (Cloudflare R2)
    package_file_key = models.CharField(max_length=500, blank=True)  # .efpkg file in R2

    class Meta:
        db_table = 'offline_exam_package'
        unique_together = [('exam_schedule', 'version')]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['expires_at']),
        ]


class PackageDistribution(models.Model):
    """
    Tracks which institution was assigned which package, and their download + sync status.
    """
    DOWNLOAD_STATUS = [
        ('PENDING', 'Not Downloaded'),
        ('DOWNLOADED', 'Downloaded'),
    ]
    SYNC_STATUS = [
        ('PENDING', 'Sync Pending'),
        ('UPLOADING', 'Upload In Progress'),
        ('PROCESSING', 'Processing Responses'),
        ('COMPLETED', 'Sync Completed'),
        ('FAILED', 'Sync Failed'),
        ('LATE_OVERRIDE', 'Synced via Late Override'),
    ]
    package = models.ForeignKey(OfflineExamPackage, on_delete=models.CASCADE, related_name='distributions')
    institution = models.ForeignKey('Institution', on_delete=models.PROTECT)

    # Download tracking
    download_status = models.CharField(max_length=20, choices=DOWNLOAD_STATUS, default='PENDING')
    downloaded_at = models.DateTimeField(null=True, blank=True)
    download_ip = models.GenericIPAddressField(null=True, blank=True)
    offline_client_version = models.CharField(max_length=20, blank=True)

    # Sync tracking
    sync_status = models.CharField(max_length=20, choices=SYNC_STATUS, default='PENDING')
    sync_initiated_at = models.DateTimeField(null=True, blank=True)
    sync_completed_at = models.DateTimeField(null=True, blank=True)
    sync_file_size_kb = models.PositiveIntegerField(null=True, blank=True)
    response_file_key = models.CharField(max_length=500, blank=True)  # .efrpkg in R2

    # Response counts
    expected_student_count = models.PositiveIntegerField(default=0)
    received_response_count = models.PositiveIntegerField(default=0)
    conflict_count = models.PositiveIntegerField(default=0)

    # Error tracking
    last_error = models.TextField(blank=True)

    class Meta:
        db_table = 'package_distribution'
        unique_together = [('package', 'institution')]
        indexes = [
            models.Index(fields=['sync_status']),
        ]


class OfflineResponse(models.Model):
    """
    Individual student responses extracted from a synced offline package.
    After processing, creates a corresponding exam_submission record.
    """
    distribution = models.ForeignKey(PackageDistribution, on_delete=models.CASCADE, related_name='responses')
    student = models.ForeignKey('Student', on_delete=models.PROTECT)

    # Offline session data
    session_token = models.CharField(max_length=200)  # Session token embedded in package
    offline_start_time = models.DateTimeField()  # When student opened exam on offline client
    offline_submit_time = models.DateTimeField()  # When student submitted on offline client

    # Response data
    answers = models.JSONField()  # {question_id: selected_option} — same format as online submission

    # Integration status
    exam_submission = models.OneToOneField(
        'ExamSubmission', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='offline_source'
    )
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'offline_response'
        unique_together = [('distribution', 'student')]


class OfflineResponseConflict(models.Model):
    """
    Raised when the same student has both an online submission and an offline response.
    Must be manually resolved before results can be finalized.
    """
    RESOLUTION_CHOICES = [
        ('PENDING', 'Pending Resolution'),
        ('ACCEPTED_OFFLINE', 'Offline Response Accepted'),
        ('ACCEPTED_ONLINE', 'Online Submission Accepted'),
        ('FLAGGED_INTEGRITY', 'Flagged for Integrity Review'),
    ]
    distribution = models.ForeignKey(PackageDistribution, on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.PROTECT)
    offline_response = models.ForeignKey(OfflineResponse, on_delete=models.CASCADE)
    online_submission = models.ForeignKey('ExamSubmission', on_delete=models.CASCADE)

    resolution = models.CharField(max_length=25, choices=RESOLUTION_CHOICES, default='PENDING')
    resolved_by = models.ForeignKey('StaffUser', on_delete=models.SET_NULL, null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_note = models.TextField(blank=True)

    # Context signals computed at conflict detection time
    online_submit_minutes_before_end = models.SmallIntegerField()  # Negative = after exam end
    offline_session_duration_seconds = models.PositiveIntegerField()
    answer_diff_count = models.PositiveSmallIntegerField()  # Number of questions with different answers

    class Meta:
        db_table = 'offline_response_conflict'
        indexes = [
            models.Index(fields=['resolution']),
        ]


class OfflinePackageAuditLog(models.Model):
    """Append-only audit trail. Never updated, never deleted."""
    ACTION_CHOICES = [
        ('PACKAGE_CREATED', 'Package Created'),
        ('PACKAGE_GENERATED', 'Package Generated'),
        ('PACKAGE_DISTRIBUTED', 'Package Distributed'),
        ('PACKAGE_DOWNLOADED', 'Package Downloaded'),
        ('SYNC_INITIATED', 'Sync Initiated'),
        ('SYNC_COMPLETED', 'Sync Completed'),
        ('SYNC_FAILED', 'Sync Failed'),
        ('CONFLICT_RESOLVED', 'Conflict Resolved'),
        ('PACKAGE_REVOKED', 'Package Revoked'),
        ('PACKAGE_EXPIRED', 'Package Expired'),
        ('LATE_SYNC_REQUESTED', 'Late Sync Override Requested'),
        ('LATE_SYNC_APPROVED', 'Late Sync Override Approved'),
        ('LATE_SYNC_REJECTED', 'Late Sync Override Rejected'),
    ]
    package = models.ForeignKey(OfflineExamPackage, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    actor = models.ForeignKey('StaffUser', on_delete=models.SET_NULL, null=True, blank=True)
    institution = models.ForeignKey('Institution', on_delete=models.SET_NULL, null=True, blank=True)
    actor_ip = models.GenericIPAddressField(null=True)
    details = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'offline_package_audit_log'
        indexes = [
            models.Index(fields=['package', 'created_at']),
            models.Index(fields=['action']),
        ]
```

**Background Tasks (SQS-triggered Lambda + Celery):**

| Task | Trigger | Description |
|---|---|---|
| `generate_offline_package` | SQS (on POST to `/generate/`) | Fetches exam data, encrypts question paper + marking scheme, embeds student list if required, uploads `.efpkg` to Cloudflare R2, updates package status to READY |
| `process_offline_sync` | SQS (on sync upload) | Validates HMAC, decrypts `.efrpkg`, extracts per-student response objects, creates `OfflineResponse` records, detects conflicts, creates `ExamSubmission` records for clean responses, queues F-04 for results processing |
| `expire_stale_packages` | Celery beat (every 30 min) | Sets status=EXPIRED for all packages where `expires_at < now` and status not in terminal states; sends notification to institutions with unsynced distributions |
| `alert_unsynced_institutions` | Celery beat (every hour) | Finds distributions where exam ended > 2 hours ago and sync_status = PENDING; sends WhatsApp alert to institution admin |
| `check_submission_timeline_anomalies` | Post-sync (after `process_offline_sync`) | Analyses per-student submission timestamps; flags if >70% of students submitted within a 60-second window (potential bulk copy); creates integrity flag on F-07 |

---

## 12. Security & Compliance

### 12.1 Package Encryption

- Question paper JSON encrypted with AES-256-GCM before being written to `.efpkg`
- Encryption key generated per-package, stored in AWS KMS (not in application DB)
- Package HMAC signed with institution-specific key (institution cannot open another institution's package)
- Time-lock enforced at decryption layer: offline client checks system clock; packages reject decryption outside the `lock_open_before_minutes` window
- Tampered packages detected by HMAC validation on sync upload; rejected with audit log entry

### 12.2 Response Package Integrity

- Student responses encrypted at rest on the offline client using session-bound key
- `.efrpkg` upload validated against package HMAC signature before processing
- Individual student response records contain a cryptographic hash of the student's session token — verifies that responses came from a legitimate session

### 12.3 DPDPA Compliance

- Student responses in `.efpkg` and `.efrpkg` are personal data; retention policy: 7 years for evaluation exams, 1 year for practice
- Package files in Cloudflare R2 have lifecycle policy: auto-delete after retention period
- Students can request their offline response data via right-to-access mechanisms same as online submissions
- No personally identifiable data outside the encrypted package files except student IDs in `OfflineResponse` table

### 12.4 Access Control

- Package download endpoint validates that the requesting institution JWT matches a `PackageDistribution` record for this package — prevents cross-institution package access
- Late sync override requires dual approval in production: Exam Ops Manager (34) approves, Platform Admin (10) must countersign for packages expired > 7 days
- All conflict resolution actions are logged with actor, IP, and timestamp; non-repudiable

### 12.5 Audit Trail

- `OfflinePackageAuditLog` is append-only at DB level (no UPDATE/DELETE permissions in application DB user for this table)
- All actions by all actors (staff + institutions) are logged
- Audit log retained for 7 years (exam integrity legal requirement)

---

## 13. Performance

| Concern | Approach |
|---|---|
| Package generation (large exams with images) | Lambda async — question paper JSON + images pre-fetched from R2; estimated 15–45 sec for a 100-question paper with diagrams; status polled by HTMX every 3 sec |
| Concurrent sync uploads | SQS queue for processing tasks; max 50 concurrent Lambda sync processors; 5 MB/sec per institution upload via presigned R2 URL (upload directly to R2, not through Django) |
| Sync Monitor live updates | HTMX polling at 15-sec interval only while active syncs in progress; server sends `HX-Trigger: stopPolling` header when all distributions reach terminal state — no unnecessary long-polling |
| Conflict detection | Runs in sync processing Lambda (not in Django request cycle); detected conflicts written to DB; UI loads them lazily on demand |
| KPI strip | Materialised counts updated by sync processing Lambda and package generation Lambda after each state change; Django view serves pre-computed values; no aggregation query on page load |
| Package download speed | `.efpkg` served via Cloudflare R2 presigned URL with 15-minute expiry — no Django in the download path; full CDN delivery speed globally |
| Audit log queries | Indexed on `(package_id, created_at)` and `action`; paginated; no full-table scans; large exports (> 1000 rows) queued as CSV generation task, emailed when ready |

---

*Last updated: 2026-03-26*
*Division: F — Exam Day Operations*
*Spec version: 1.0*
