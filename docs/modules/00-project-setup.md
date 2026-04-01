# EduForge — Project Setup

## Tech Stack (All Free / Open Source)

| Layer | Technology | Version | Cost |
|---|---|---|---|
| Language | Python | 3.12 | Free |
| Package Manager | uv (Astral) | latest | Free |
| Auth API | FastAPI + Mangum | 0.111 | Free |
| Staff Portals | Django + HTMX | 4.2 + 1.9 | Free |
| Mobile | Flutter + Riverpod | 3.x | Free |
| ORM | SQLAlchemy | 2.0 | Free |
| Migrations | Alembic | 1.13 | Free |
| Database | PostgreSQL | 16 | Free |
| Connection Pooling | PgBouncer | latest | Free — essential at scale |
| Async DB Driver | asyncpg | 0.29 | Free |
| Queue | AWS SQS | — | Pay per use (near zero) |
| Storage | Cloudflare R2 | — | Free 10GB / zero egress |
| CDN | Cloudflare | — | Free tier |
| Runtime (Lambda) | AWS Lambda ARM (Graviton) | — | Free 1M req/month · 20% cheaper |
| Runtime (Portal) | ECS Fargate | — | Pay per use |
| Password Hashing | passlib + bcrypt | 1.7 | Free |
| JWT | python-jose | 3.3 | Free |
| HTTP Client | httpx | 0.27 | Free |
| Validation | Pydantic | 2.7 | Free |
| PDF Generation | WeasyPrint | latest | Free — fee invoice + progress report ONLY |
| Linting | ruff | latest | Free |
| Formatting | ruff format | latest | Free |
| Type Check | mypy | latest | Free |
| Testing | pytest + pytest-asyncio | latest | Free |
| Container | Docker + Docker Compose | — | Free |
| CI/CD | GitHub Actions | — | Free (2000 min/month) |

---

## Storage Strategy — CDN-First

```
DB (PostgreSQL)    → user activity only (attendance, fees, marks, sessions)
Cloudflare R2/CDN  → all content (notes, MCQs, timetables, results)
IndexedDB (device) → user photos, offline exam questions, offline content
PDF                → ONLY 2: fee invoice + progress report card
Everything else    → in-app view, share via WhatsApp app link
```

## Page Rendering — CDN + API Hybrid (Option C)

Every page = **1 CDN call** (shared content) + **1 API call** (personal data).
Same CDN JSON powers both Flutter and HTMX web — no duplication.

```
Page load
    │
    ├── CDN call → shared.json / shared.html  (timetable, syllabus, announcements)
    │             └─ Flutter reads JSON directly
    │             └─ HTMX fetches HTML partial directly from CDN (zero Django compute)
    │
    └── API call → /api/v1/pages/{slug}/personal  (attendance %, fee due, marks)
                  └─ Flutter reads JSON response
                  └─ HTMX swaps HTML fragment from Django
```

### CDN File Layout per Page

```
cdn.eduforge.in/
  {tenant_id}/
    pages/
      student-dashboard/
        shared.json     ← Flutter reads this
        shared.html     ← HTMX hx-get points here directly
      class-timetable/
        shared.json
        shared.html
      syllabus/
        shared.json
        shared.html
```

### CDN JSON Structure (Flutter + source of truth)

```json
// cdn.eduforge.in/{tenant_id}/pages/student-dashboard/shared.json

{
  "page":    "student_dashboard",
  "version": 14,
  "flag":    "NORMAL",
  "blocks": {
    "timetable": {
      "today": [
        { "period": 1, "subject": "Maths",   "teacher": "Sharma Sir", "time": "08:00" },
        { "period": 2, "subject": "Physics",  "teacher": "Rao Sir",    "time": "09:00" }
      ]
    },
    "announcements": [
      { "id": "ann_01", "title": "PTM Saturday 10 AM", "date": "2026-03-23" }
    ],
    "syllabus_progress": {
      "Maths":   72,
      "Physics": 58,
      "Chemistry": 81
    }
  }
}
```

### CDN HTML Partial (Celery pre-renders from same JSON — HTMX reads directly)

```python
# services/notification/bundle_generator.py — Celery task

@shared_task
def regenerate_page_bundle(tenant_id: str, page_slug: str, data: dict):
    """Runs on data change. Generates JSON + HTML from same data source."""

    # 1. Build JSON (for Flutter + IndexedDB)
    json_bundle = {
        "page":    page_slug,
        "version": data["version"],
        "flag":    data["flag"],
        "blocks":  data["blocks"],
    }
    r2_put(f"{tenant_id}/pages/{page_slug}/shared.json", json_bundle)

    # 2. Render HTML partial from same data (for HTMX web — no Django compute at read time)
    html_partial = render_jinja_template(
        template=f"bundles/{page_slug}_shared.html",
        context=data["blocks"],
    )
    r2_put(f"{tenant_id}/pages/{page_slug}/shared.html", html_partial)

    # 3. Purge CDN cache + FCM push to logged-in users
    process_cdn_flag.delay(
        content_id=f"{tenant_id}/{page_slug}",
        flag=data["flag"],
        urls=[
            f"{CDN_URL}/{tenant_id}/pages/{page_slug}/shared.json",
            f"{CDN_URL}/{tenant_id}/pages/{page_slug}/shared.html",
        ],
        version_bump=True,
        module=page_slug,
        new_version=data["version"],
        tenant_id=tenant_id,
    )
```

### HTML Partial Template (Jinja — rendered by Celery, stored on CDN)

```html
<!-- services/notification/templates/bundles/student-dashboard_shared.html -->
<!-- This is pre-rendered by Celery and stored as static HTML on CDN -->

<div id="timetable-block">
  <h3 class="font-semibold text-gray-700">Today's Timetable</h3>
  <ul class="divide-y">
    {% for period in timetable.today %}
    <li class="py-2 flex justify-between">
      <span>{{ period.subject }}</span>
      <span class="text-gray-500">{{ period.time }} · {{ period.teacher }}</span>
    </li>
    {% endfor %}
  </ul>
</div>

<div id="announcements-block" class="mt-4">
  {% for ann in announcements %}
  <div class="bg-blue-50 rounded p-3 mb-2">
    <p class="font-medium">{{ ann.title }}</p>
    <p class="text-sm text-gray-500">{{ ann.date }}</p>
  </div>
  {% endfor %}
</div>
```

### HTMX Shell Page (Django returns shell — zero data queries)

```html
<!-- portal/templates/pages/student_dashboard.html -->
<!-- Django only checks auth + returns this shell. No DB queries for page data. -->

{% extends "base.html" %}
{% block content %}

<div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">

  <!-- Shared block: fetched directly from CDN — zero Django compute -->
  <div id="shared-blocks"
       hx-get="{{ cdn_url }}/{{ tenant_id }}/pages/student-dashboard/shared.html"
       hx-trigger="load"
       hx-swap="innerHTML">
    <div class="animate-pulse h-32 bg-gray-100 rounded"></div>  <!-- skeleton -->
  </div>

  <!-- Personal block: one API call — attendance, fee, marks -->
  <div id="personal-block"
       hx-get="/api/v1/pages/student-dashboard/personal"
       hx-trigger="load"
       hx-swap="innerHTML">
    <div class="animate-pulse h-32 bg-gray-100 rounded"></div>
  </div>

</div>
{% endblock %}
```

### Personal Data API — One Call, Returns HTML for HTMX or JSON for Flutter

```python
# identity/api/pages.py

@router.get("/api/v1/pages/{page_slug}/personal")
async def personal_page_data(
    page_slug: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Single endpoint — returns JSON for Flutter, HTML fragment for HTMX."""

    # One DB query — only personal live data
    data = await get_personal_data(db, current_user, page_slug)

    # Flutter sends Accept: application/json
    if "application/json" in request.headers.get("accept", ""):
        return data

    # HTMX web — return rendered HTML fragment
    return HTMLResponse(
        render_jinja_template(f"partials/{page_slug}_personal.html", data)
    )
```

### Flutter — Same CDN JSON + API Call

```dart
// Flutter page loader — 1 CDN call + 1 API call

Future<StudentDashboard> loadDashboard(String tenantId) async {
  // 1. Shared block — CDN/IndexedDB first
  final shared = await cdnOrIndexedDB(
    cdnUrl: '$CDN_URL/$tenantId/pages/student-dashboard/shared.json',
    cacheKey: 'student-dashboard-shared',
  );

  // 2. Personal block — API call (live data, not cached)
  final personal = await api.get('/api/v1/pages/student-dashboard/personal');

  return StudentDashboard.fromJson(shared: shared, personal: personal);
}
```

### Rule Summary

| Block Type | Examples | Source | Flutter | HTMX Web |
|---|---|---|---|---|
| Shared / static | Timetable, announcements, syllabus | CDN JSON+HTML | Read JSON | `hx-get` CDN HTML direct |
| Personal / live | Attendance %, fee due, marks | API | Read JSON | `hx-get` API HTML |
| Write ops | Pay fee, submit attendance | API (POST) | POST API | HTMX POST |

---

## What Goes Where

| Data | Storage | Why |
|---|---|---|
| Notes / PDFs | Cloudflare R2 → CDN | Static, generated once, free to serve |
| MCQ questions | R2 JSON → CDN | Content doesn't change after approval |
| Timetable | R2 JSON → CDN | Regenerated only on change |
| Published results | R2 JSON → CDN | Immutable after publish |
| Announcements | R2 JSON → CDN | Low-frequency updates |
| Current affairs | R2 → CDN | Published once daily |
| Exam questions (offline) | IndexedDB (device) | Zero network during exam |
| Analytics dashboards | Pre-computed JSON → R2 → CDN | Nightly refresh |
| Institution branding | R2 JSON → CDN | Rarely changes |
| **Profile photos** | **IndexedDB (device only)** | No CDN cost — device cache |
| **Personal photos** | **IndexedDB (device only)** | High storage — keep on device |
| **User credentials** | **DB only** | Security |
| **Attendance records** | **DB only** | Queryable |
| **Fee payments** | **DB only** | Financial source of truth |
| **Exam submissions** | **DB only** | Audit trail |
| **Active workflows** | **DB only** | Live state |

---

## PDF Policy — Minimal Generation

> **Only 2 PDFs are ever generated. Everything else is in-app view only.**

| Document | PDF? | How Shared |
|---|---|---|
| Fee invoice | ✅ YES — parent needs payment proof | Download button + WhatsApp |
| Progress report / report card | ✅ YES — academic record | Download + WhatsApp |
| Transfer Certificate (TC) | ❌ NO — in-app view | Share via app link |
| Bonafide certificate | ❌ NO — in-app view | Share via app link |
| Attendance report | ❌ NO — in-app table | Screenshot / share link |
| Salary slip | ❌ NO — in-app view | In-app only |
| Hall ticket / admit card | ❌ NO — in-app view | In-app only |
| ID card | ❌ NO — in-app view | In-app only |
| All other certificates | ❌ NO — in-app view | Share via app link |

**Why:** Parent and student get everything through the app. Sharing = WhatsApp deep link that opens in-app view. No PDF = no generation cost, no R2 storage, no Celery job.

---

## CDN Flag System — 10 Priority Flags

Every content update carries a flag. Flag determines when CDN cache is invalidated.

| # | Flag | Purge Time | Use Case |
|---|---|---|---|
| 1 | `CRITICAL` | **Instant (seconds)** | Exam error, safety alert, system breach |
| 2 | `IMMEDIATE` | **5 min** | Urgent notice, exam cancelled, emergency |
| 3 | `FAST` | **15 min** | Results published, hall ticket released |
| 4 | `NORMAL` | **30 min** | Timetable update, homework assigned |
| 5 | `STANDARD` | **1 hour** | Notes updated, new MCQs added |
| 6 | `BATCH_DAY` | **End of day (6 PM)** | Non-urgent daytime updates |
| 7 | `SCHEDULED` | **Night 2 AM** | Bulk updates — syllabus, mass MCQ, report cards |
| 8 | `LAZY` | **On TTL expiry only** | Gallery, minor text edits — no active purge |
| 9 | `VERSION_BUMP` | **Combined with any above** | Forces IndexedDB version update on all clients |
| 10 | `MANUAL` | **Platform admin triggers** | Admin purges specific URL/path manually |

---

## CDN TTL — Time-Based Intervals

| Interval | TTL Name | Applied To |
|---|---|---|
| 5 min | `TTL_5MIN` | Emergency content, live exam questions |
| 15 min | `TTL_15MIN` | Results, fast-changing notices |
| 30 min | `TTL_30MIN` | Timetable, homework |
| 1 hour | `TTL_1HR` | Notes, MCQs, institution branding |
| 6 hours | `TTL_6HR` | Syllabus, course structure |
| 1 day | `TTL_DAY` | Current affairs, published reports |
| 7 days | `TTL_WEEK` | Approved MCQ banks, static content |
| 30 days | `TTL_MONTH` | Archived results, old certificates |

---

## Content → Flag + TTL Mapping

| Content | Priority Flag | TTL | VERSION_BUMP |
|---|---|---|---|
| Safety / emergency | `CRITICAL` | `TTL_5MIN` | ❌ |
| Exam question error | `CRITICAL` | `TTL_5MIN` | ✅ |
| Results published | `FAST` | `TTL_15MIN` | ✅ |
| Timetable change | `NORMAL` | `TTL_30MIN` | ✅ |
| New homework | `NORMAL` | `TTL_30MIN` | ✅ |
| Notes / PDF updated | `STANDARD` | `TTL_1HR` | ✅ |
| Institution branding | `IMMEDIATE` | `TTL_1HR` | ❌ |
| New MCQs added | `SCHEDULED` | `TTL_DAY` | ✅ |
| Current affairs | `SCHEDULED` | `TTL_DAY` | ❌ |
| Report cards | `SCHEDULED` | `TTL_DAY` | ✅ |
| Gallery / photos | `LAZY` | `TTL_MONTH` | ❌ |
| Syllabus update | `SCHEDULED` | `TTL_DAY` | ✅ |

---

## Peak Hour Awareness — When CDN Purges Run

```
PEAK HOURS (NO batch purge)      08:00 AM → 09:00 PM
LOW PEAK (batch purge runs)      09:00 PM → 07:00 AM
DEAD NIGHT (heavy batch jobs)    01:00 AM → 04:00 AM
```

```
Flag behaviour during peak hours:
  CRITICAL    → runs immediately regardless of peak hours
  IMMEDIATE   → runs immediately regardless of peak hours
  FAST        → runs immediately regardless of peak hours
  NORMAL      → queued if peak hours → runs at 9 PM
  STANDARD    → queued if peak hours → runs at 9 PM
  BATCH_DAY   → always runs at 6 PM
  SCHEDULED   → always runs at 2 AM
  LAZY        → waits for TTL to expire naturally — no active purge
```

```python
# services/notification/cdn_purge_worker.py (Celery beat)

from celery import shared_task
from datetime import datetime

def is_peak_hour() -> bool:
    hour = datetime.now().hour
    return 8 <= hour <= 21           # 8 AM to 9 PM

@shared_task
def process_cdn_flag(content_id: str, flag: str, urls: list[str]):
    if flag in ("CRITICAL", "IMMEDIATE", "FAST"):
        purge_now(urls)              # always immediate, ignore peak hours

    elif flag in ("NORMAL", "STANDARD"):
        if is_peak_hour():
            queue_for_low_peak(content_id, flag, urls)   # queue → purge at 9 PM
        else:
            purge_now(urls)

    elif flag == "BATCH_DAY":
        queue_for_6pm(content_id, urls)

    elif flag == "SCHEDULED":
        queue_for_2am(content_id, urls)

    elif flag == "LAZY":
        pass                         # do nothing — TTL handles it

@shared_task(name="purge_batch_6pm")
def purge_batch_6pm():
    pending = CdnPurgeQueue.objects.filter(scheduled_for="6PM", purged=False)
    urls = [item.url for item in pending]
    cloudflare_purge(urls)           # batch — one API call for all
    pending.update(purged=True)

@shared_task(name="purge_batch_2am")
def purge_batch_2am():
    pending = CdnPurgeQueue.objects.filter(scheduled_for="2AM", purged=False)
    urls = [item.url for item in pending]
    cloudflare_purge(urls)
    pending.update(purged=True)
```

---

## 2-Day Inactive User — CDN File Cleanup

If a user has not logged in for 2+ days, their personal CDN-cached files are deleted. When they return, files are re-fetched and re-cached.

```
User last_login_at > 2 days ago
         ↓
Celery beat job (runs nightly at 3 AM)
         ↓
Delete user's CDN files:
  cdn.eduforge.in/users/{user_id}/           ← personal content
  cdn.eduforge.in/cache/{tenant_id}/{user_id}/
         ↓
Keep in DB (source of truth — can always regenerate):
  Attendance records    ✅ DB
  Fee records           ✅ DB
  Results               ✅ DB
  Profile data          ✅ DB
         ↓
User returns after 2 days
         ↓
Files re-fetched from source → cached again → served from CDN

Cost saving: inactive users pay ₹0 CDN storage
```

```python
# Celery beat — runs nightly 3 AM
@shared_task(name="cleanup_inactive_user_cdn")
def cleanup_inactive_user_cdn():
    two_days_ago = datetime.utcnow() - timedelta(days=2)
    inactive_users = (
        db.query(User)
        .filter(User.last_login_at < two_days_ago)
        .all()
    )
    for user in inactive_users:
        # Purge user-specific CDN paths
        cloudflare_purge_prefix(f"users/{user.id}/")
        # IndexedDB on device is NOT cleared — user clears it or it expires
```

---

## Photos — IndexedDB Only (Not CDN)

High-storage content like photos are NOT stored in CDN. They live on the user's device in IndexedDB.

```
User profile photo uploaded
         ↓
Lambda → compress to WebP (max 200KB) → store in R2 as source
         ↓
First time app loads photo:
  Fetch from R2 → store in IndexedDB (device storage)
         ↓
Every subsequent load:
  Serve from IndexedDB directly → zero network → zero CDN cost
         ↓
Photo updated:
  New version uploaded → VERSION_BUMP flag set
  App detects version change → re-fetches from R2 → updates IndexedDB

Benefits:
  ✅ Zero CDN egress cost for photos
  ✅ Faster repeat loads (local device)
  ✅ Works offline
  ✅ No CDN storage cost for personal files
```

```javascript
// Flutter / PWA — IndexedDB photo service

class PhotoService {
  static Future<Uint8List> getPhoto(String userId, int version) async {
    final cached = await IndexedDB.get('photo_${userId}_v${version}');
    if (cached != null) return cached;           // serve from device

    // Not in IndexedDB — fetch from R2 source
    final bytes = await http.get('${R2_URL}/users/${userId}/photo.webp');
    await IndexedDB.put('photo_${userId}_v${version}', bytes);
    return bytes;
  }
}
```

---

## IndexedDB Update — Server-Push Model (Not Client Poll)

```
OLD (avoid):  Every client checks manifest.json on every app load
              → N users × M loads/day = thousands of CDN requests doing nothing

NEW (use):    Server pushes FCM notification only when content actually changes
              → 1 push per update × only affected users = near-zero CDN polling cost
```

**Primary path: Server Push via FCM**
```
Content updated → CDN purge → VERSION_BUMP flag fires
                                      ↓
                    Celery queries: who has an active session right now?
                    (Session.is_active = true AND expires_at > now)
                                      ↓
                    FCM push sent ONLY to currently logged-in users
                    Offline users → skipped (manifest fallback on next login)
                                      ↓
                    Client receives silent push payload:
                    { module: "timetable", version: 14, update: "idle" }
                                      ↓
                    Client fetches ONLY that module from CDN
                    → stores in IndexedDB → done
```

**Fallback path: Manifest JSON (offline users / fresh install)**
```
manifest.json checked ONCE on:
  - First app install / fresh login after being offline
  - After session was expired (missed all pushes while offline)
  NOT on every app load
```

```json
// cdn.eduforge.in/versions/{tenant_id}/manifest.json
// Updated by Celery when VERSION_BUMP flag fires — fallback reference only

{
  "manifest_version": "2026.03.22.001",
  "updated_at": "2026-03-22T02:00:00Z",
  "modules": {
    "timetable":          { "v": 13, "flag": "NORMAL",    "update": "idle" },
    "notes_grade10":      { "v": 9,  "flag": "STANDARD",  "update": "idle" },
    "exam_questions":     { "v": 5,  "flag": "CRITICAL",  "update": "immediate" },
    "syllabus":           { "v": 4,  "flag": "SCHEDULED", "update": "overnight" },
    "mcq_bank_physics":   { "v": 22, "flag": "SCHEDULED", "update": "overnight" }
  }
}
```

```
update: "immediate"  → fetch right now (CRITICAL / IMMEDIATE flags)
update: "idle"       → fetch in background when user is idle (NORMAL / STANDARD)
update: "overnight"  → fetch when device on charge + Wi-Fi at night (SCHEDULED)
```

### Server Side — Celery Sends FCM Push on VERSION_BUMP

```python
# services/notification/cdn_push.py

import firebase_admin
from firebase_admin import messaging

@shared_task
def push_version_update(tenant_id: str, module: str, version: int, update_type: str):
    """Called by Celery when VERSION_BUMP flag fires after CDN purge.
    Pushes ONLY to users with an active session right now — not all tenant users.
    Offline users get the update via manifest.json fallback on next login.
    """

    # Only users with a valid non-expired session (currently logged in)
    active_tokens = (
        db.query(UserDevice.fcm_token)
        .join(Session, Session.user_id == UserDevice.user_id)
        .filter(
            Session.tenant_id == tenant_id,
            Session.is_active == True,
            Session.expires_at > datetime.utcnow(),     # session not expired
        )
        .distinct()
        .all()
    )
    tokens = [row.fcm_token for row in active_tokens if row.fcm_token]

    if not tokens:
        return   # no one logged in right now — manifest fallback handles it

    message = messaging.MulticastMessage(
        tokens=tokens,
        data={
            "type":    "CDN_VERSION_UPDATE",
            "module":  module,
            "version": str(version),
            "update":  update_type,    # "immediate" | "idle" | "overnight"
        },
        # Silent push — no banner, no sound — background data only
        android=messaging.AndroidConfig(priority="normal"),
        apns=messaging.APNSConfig(
            headers={"apns-push-type": "background", "apns-priority": "5"},
        ),
    )
    messaging.send_each_for_multicast(message)
```

```python
# In cdn_purge_worker.py — trigger push after purge when VERSION_BUMP set

@shared_task
def process_cdn_flag(content_id: str, flag: str, urls: list[str],
                     version_bump: bool = False, module: str = None,
                     new_version: int = None, tenant_id: str = None):

    # 1. Purge CDN cache (existing logic)
    if flag in ("CRITICAL", "IMMEDIATE", "FAST"):
        purge_now(urls)
    elif flag in ("NORMAL", "STANDARD"):
        if is_peak_hour():
            queue_for_low_peak(content_id, flag, urls)
        else:
            purge_now(urls)
    elif flag == "BATCH_DAY":
        queue_for_6pm(content_id, urls)
    elif flag == "SCHEDULED":
        queue_for_2am(content_id, urls)

    # 2. If VERSION_BUMP — push to affected users (server-driven, not client poll)
    if version_bump and module and tenant_id:
        update_type = {
            "CRITICAL": "immediate", "IMMEDIATE": "immediate", "FAST": "immediate",
            "NORMAL": "idle",        "STANDARD": "idle",
            "BATCH_DAY": "overnight", "SCHEDULED": "overnight",
        }.get(flag, "idle")

        push_version_update.delay(tenant_id, module, new_version, update_type)

        # Update manifest.json on CDN (fallback for offline users)
        update_version_manifest.delay(tenant_id, module, new_version, update_type)
```

### Client Side — Flutter handles incoming FCM push

```dart
// Flutter — FCM background message handler

@pragma('vm:entry-point')
Future<void> onBackgroundMessage(RemoteMessage message) async {
  if (message.data['type'] != 'CDN_VERSION_UPDATE') return;

  final module    = message.data['module']!;
  final version   = int.parse(message.data['version']!);
  final updateHow = message.data['update']!;        // immediate | idle | overnight

  switch (updateHow) {
    case 'immediate':
      await updateModuleInIndexedDB(module, version);   // fetch + store now
      break;
    case 'idle':
      scheduleIdleUpdate(module, version);              // fetch when UI is idle
      break;
    case 'overnight':
      scheduleOvernightUpdate(module, version);         // charge + Wi-Fi only
      break;
  }
}

Future<void> updateModuleInIndexedDB(String module, int version) async {
  final data = await http.get('${CDN_URL}/modules/$module/v$version.json');
  await IndexedDB.put('module_$module', data.body);
  await IndexedDB.put('version_$module', version);
}
```

### Cost Comparison

| Approach | CDN requests/day (50K users, 3 opens/day) | Cost |
|---|---|---|
| Client polls manifest on every open | 150,000 requests/day | High |
| Server push — only on actual change | ~10–50 pushes/day × affected users | Near zero |
| **Saving** | **~149,950 requests/day avoided** | **₹3,000–10,000/month** |

---

## Auto-Cleanup — Lambda, CloudWatch, DB, SQS

### CloudWatch Logs Retention (AWS Lambda)

```python
# infra/lambda/log_retention.py (AWS CDK)

from aws_cdk import aws_logs as logs

LOG_RETENTION = {
    # DB-stored ops → 1 day (can regenerate from DB anytime)
    "fee-service":          logs.RetentionDays.ONE_DAY,
    "invoice-service":      logs.RetentionDays.ONE_DAY,
    "pdf-generator":        logs.RetentionDays.ONE_DAY,
    "notification-sent":    logs.RetentionDays.ONE_DAY,
    "report-generator":     logs.RetentionDays.ONE_DAY,

    # General operations
    "identity-info":        logs.RetentionDays.THREE_DAYS,    # DEBUG
    "portal-info":          logs.RetentionDays.ONE_WEEK,      # INFO
    "exam-info":            logs.RetentionDays.ONE_WEEK,

    # Warnings
    "portal-warnings":      logs.RetentionDays.TWO_WEEKS,

    # Errors — need investigation time
    "identity-errors":      logs.RetentionDays.ONE_MONTH,
    "exam-errors":          logs.RetentionDays.ONE_MONTH,
    "billing-errors":       logs.RetentionDays.ONE_MONTH,

    # Critical
    "system-critical":      logs.RetentionDays.THREE_MONTHS,

    # Security — cannot regenerate, evidence required
    "auth-security":        logs.RetentionDays.ONE_YEAR,      # login fails, OTP abuse
    "audit-trail":          logs.RetentionDays.ONE_YEAR,      # who changed what
}
```

**Cost saving:** Default = never expire = ₹∞. With retention = ₹2,000-5,000/month saved at scale.

### Lambda Right-Sizing

```python
# infra/lambda/function_config.py

LAMBDA_CONFIG = {
    # Simple lookups — 128MB is enough
    "tenant-config":    {"memory": 128,  "timeout": 3},
    "user-lookup":      {"memory": 128,  "timeout": 3},
    "otp-verify":       {"memory": 128,  "timeout": 5},

    # Standard API operations
    "auth-token":       {"memory": 256,  "timeout": 10},
    "attendance-mark":  {"memory": 256,  "timeout": 10},
    "fee-record":       {"memory": 256,  "timeout": 10},

    # Heavy operations
    "exam-submit":      {"memory": 512,  "timeout": 30},
    "analytics-report": {"memory": 512,  "timeout": 60},

    # AI operations
    "ai-mcq-generate":  {"memory": 1024, "timeout": 120},
}

# Use ARM (Graviton2) for all Lambda — 20% cheaper than x86
ARCHITECTURE = "arm64"   # cheaper + faster
```

### DB Auto-Cleanup — Celery Beat Jobs

```python
# Nightly cleanup jobs — run at 3 AM daily

@shared_task(name="cleanup_expired_sessions")
def cleanup_expired_sessions():
    # Sessions older than 7 days + inactive
    db.execute("""
        DELETE FROM platform.sessions
        WHERE expires_at < now() - interval '1 day'
        AND is_active = false
    """)

@shared_task(name="cleanup_expired_otps")
def cleanup_expired_otps():
    # OTPs expire in 10 min — clean up after 1 day
    db.execute("""
        DELETE FROM platform.otps
        WHERE expires_at < now() - interval '1 day'
    """)

@shared_task(name="cleanup_expired_password_tokens")
def cleanup_expired_password_tokens():
    db.execute("""
        DELETE FROM platform.password_reset_tokens
        WHERE expires_at < now() - interval '1 day'
    """)

@shared_task(name="cleanup_otp_rate_limits")
def cleanup_otp_rate_limits():
    # Rate limit windows expire after 10 min — clean after 1 day
    db.execute("""
        DELETE FROM platform.otp_rate_limits
        WHERE window_start < now() - interval '1 day'
    """)

@shared_task(name="cleanup_old_cdn_purge_queue")
def cleanup_old_cdn_purge_queue():
    # Already purged CDN queue entries — keep 1 day for debug
    db.execute("""
        DELETE FROM platform.cdn_purge_queue
        WHERE purged = true
        AND purged_at < now() - interval '1 day'
    """)

@shared_task(name="hibernate_inactive_institutions")
def hibernate_inactive_institutions():
    # Institutions with no activity for 90 days → hibernate shard
    inactive = get_institutions_inactive_since(days=90)
    for institution in inactive:
        move_shard_to_cold_storage(institution.tenant_id)
```

### Celery Beat Schedule

```python
# celery_config.py

CELERYBEAT_SCHEDULE = {
    # Every 5 min — health checks
    "shard-health-check": {
        "task": "check_shard_health",
        "schedule": crontab(minute="*/5"),
    },
    # Hourly — capacity monitoring
    "capacity-check": {
        "task": "check_shard_capacity",
        "schedule": crontab(minute=0),
    },
    # 6 PM — batch CDN purge (daytime queued updates)
    "cdn-purge-6pm": {
        "task": "purge_batch_6pm",
        "schedule": crontab(hour=18, minute=0),
    },
    # 9 PM — low-peak queued purges
    "cdn-purge-low-peak": {
        "task": "purge_low_peak_queue",
        "schedule": crontab(hour=21, minute=0),
    },
    # 2 AM — nightly scheduled purges + IndexedDB version updates
    "cdn-purge-night": {
        "task": "purge_batch_2am",
        "schedule": crontab(hour=2, minute=0),
    },
    # 3 AM — DB cleanup
    "db-cleanup": {
        "task": "cleanup_all_expired",
        "schedule": crontab(hour=3, minute=0),
    },
    # 3:30 AM — inactive user CDN cleanup
    "cdn-user-cleanup": {
        "task": "cleanup_inactive_user_cdn",
        "schedule": crontab(hour=3, minute=30),
    },
    # Nightly — analytics pre-aggregation
    "analytics-aggregate": {
        "task": "aggregate_daily_analytics",
        "schedule": crontab(hour=1, minute=0),
    },
    # Weekly Sunday 4 AM — hibernate inactive institutions
    "hibernate-inactive": {
        "task": "hibernate_inactive_institutions",
        "schedule": crontab(hour=4, minute=0, day_of_week=0),
    },
}
```

### SQS Dead Letter Queue Cleanup

```python
# infra/sqs/queues.py (AWS CDK)

# Dead letter queues — messages that failed 3 retries
# Keep for 1 day only — investigate + delete
DLQ_RETENTION_SECONDS = 86400    # 1 day

# Main queues
MAIN_QUEUE_RETENTION = 345600    # 4 days max
MAIN_QUEUE_VISIBILITY = 30       # 30 seconds processing window
MAIN_QUEUE_MAX_RETRIES = 3       # before moving to DLQ
```

---

## Log Retention Rules — Final

| Log Type | Retention | Reason |
|---|---|---|
| `DEBUG` | **3 days** | Dev only, no value after fix |
| `INFO` | **7 days** | Short-lived operational value |
| `WARNING` | **14 days** | Investigation window |
| `ERROR` | **30 days** | Fix + verify resolution |
| `CRITICAL` | **90 days** | Full investigation trail |
| `SECURITY` (login fail, OTP abuse, breach) | **1 year** | Cannot regenerate — evidence |
| `AUDIT` (data changes, deletions) | **1 year** | Compliance |
| **DB-stored ops** (fee, invoice, PDF, notifications, reports) | **1 day** | Data in DB = regenerate anytime |

> **Rule:** If the operation's result is stored in DB → log has zero long-term value → 1 day only.
> Only keep logs for events that **cannot be reconstructed** from DB (security, audit).

---

## Exam Peak — 74K Concurrent Submissions

### The Problem

```
74K students hit Submit at the same second
         ↓
74K simultaneous DB writes → PostgreSQL crashes
74K Lambda invocations     → concurrency limit hit
74K rank calculations      → impossible in real time
App crash mid-exam         → answers lost (if not persisted locally)
```

### Solution: IndexedDB as Write-Ahead Log + SQS Buffer + Adaptive Batch

```
Every answer change → IndexedDB immediately  ← zero data loss, works offline
         ↓
Student hits Submit
         ↓
Read complete answer sheet from IndexedDB → ONE API call
         ↓
Lambda validates → writes to SQS → 202 Accepted  (DB: zero)
         ↓
SQS queue depth checked → adaptive batch size set
         ↓
Celery bulk INSERT → DB
         ↓
Exam closes → score + rank → CDN → FCM push
```

---

### IndexedDB — Every Answer Change Saved (Zero Data Loss)

Every time a student selects or changes an answer, it is saved to IndexedDB **immediately** — before any API call. IndexedDB is the source of truth during the exam.

```dart
// Flutter — ExamAnswerStore (IndexedDB via Hive / shared_preferences)

class ExamAnswerStore {
  static const _boxName = 'exam_answers';

  // Called on EVERY answer tap — synchronous, instant, zero network
  static Future<void> saveAnswer(
      String examId, int questionNo, String answer) async {
    final box  = await Hive.openBox(_boxName);
    final key  = 'exam_${examId}';

    // Read current state, update one answer, write back
    final Map current = box.get(key, defaultValue: {
      'exam_id':    examId,
      'answers':    {},
      'started_at': DateTime.now().toIso8601String(),
      'submitted':  false,
    });

    current['answers'][questionNo.toString()] = answer;
    current['last_saved'] = DateTime.now().toIso8601String();

    await box.put(key, current);   // persisted on device — survives crash/reload
  }

  // On app reload mid-exam — restore exactly where student left off
  static Future<Map?> resumeExam(String examId) async {
    final box  = await Hive.openBox(_boxName);
    final data = box.get('exam_${examId}');
    if (data == null) return null;
    if (data['submitted'] == true) return null;   // already submitted
    return data;   // restore answers, re-render UI
  }

  // On Submit — read from IndexedDB, mark submitted
  static Future<Map> getForSubmission(String examId) async {
    final box  = await Hive.openBox(_boxName);
    final data = box.get('exam_${examId}')!;
    data['submitted']    = true;
    data['submitted_at'] = DateTime.now().toIso8601String();
    await box.put('exam_${examId}', data);   // mark before API call
    return data;
  }

  // After confirmed 202 from server — safe to clear
  static Future<void> clearAfterConfirm(String examId) async {
    final box = await Hive.openBox(_boxName);
    await box.delete('exam_${examId}');
  }
}
```

```
Answer change flow:
  Student taps option B for Q12
          ↓
  ExamAnswerStore.saveAnswer(examId, 12, 'B')  ← instant, local
          ↓
  IndexedDB: { answers: { "12": "B", ... }, submitted: false }
          ↓
  UI updates immediately — no network wait

Crash / reload flow:
  App reopens during exam window
          ↓
  ExamAnswerStore.resumeExam(examId)
          ↓
  All 38 answered questions restored → student continues from Q39
  Zero answers lost

Submit flow:
  Student taps Submit
          ↓
  ExamAnswerStore.getForSubmission(examId)  ← reads full answer sheet
          ↓
  ONE API call with all answers
          ↓
  202 received → ExamAnswerStore.clearAfterConfirm(examId)
```

---

### Adaptive Batch Size — Based on SQS Queue Depth

Batch size is **not hardcoded**. Celery checks SQS queue depth before each poll and scales the batch size up or down automatically.

```python
# services/exam/consumers/submission_consumer.py

import boto3

sqs = boto3.client('sqs', region_name='ap-south-1')

BATCH_RULES = [
    # (queue_depth_threshold, batch_size, celery_workers)
    (500,    50,  2),    # low load    — small batches, 2 workers
    (2_000,  100, 4),    # normal      — standard batches, 4 workers
    (10_000, 200, 8),    # high load   — larger batches, 8 workers
    (30_000, 300, 12),   # exam surge  — fast drain, 12 workers
    (float('inf'), 500, 16),   # peak burst — max throughput
]

def get_adaptive_batch_config() -> tuple[int, int]:
    """Check SQS queue depth → return (batch_size, worker_count)."""
    attrs = sqs.get_queue_attributes(
        QueueUrl=EXAM_SUBMISSION_QUEUE_URL,
        AttributeNames=['ApproximateNumberOfMessages'],
    )
    depth = int(attrs['Attributes']['ApproximateNumberOfMessages'])

    for threshold, batch_size, workers in BATCH_RULES:
        if depth <= threshold:
            return batch_size, workers

    return 500, 16   # fallback max


@shared_task(name="poll_exam_submissions")
def poll_exam_submissions():
    """Celery beat runs every 5 sec during exam window.
    Checks queue depth → adapts batch size → processes."""

    batch_size, _ = get_adaptive_batch_config()

    messages = sqs.receive_message(
        QueueUrl=EXAM_SUBMISSION_QUEUE_URL,
        MaxNumberOfMessages=min(batch_size, 10),  # SQS max per call = 10
        WaitTimeSeconds=1,
    ).get('Messages', [])

    if not messages:
        return

    # For batch_size > 10: loop to collect full batch before inserting
    collected = messages
    while len(collected) < batch_size:
        more = sqs.receive_message(
            QueueUrl=EXAM_SUBMISSION_QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=0,
        ).get('Messages', [])
        if not more:
            break
        collected.extend(more)

    process_exam_submissions_batch.delay(collected)


@shared_task(name="process_exam_submissions_batch")
def process_exam_submissions_batch(messages: list[dict]):
    """Bulk INSERT whatever batch was collected — size varies."""

    rows = [
        {
            "exam_id":      m["Body"]["exam_id"],
            "student_id":   m["Body"]["student_id"],
            "answers":      m["Body"]["answers"],
            "submitted_at": m["Body"]["submitted_at"],
            "checksum":     m["Body"]["checksum"],
        }
        for m in messages
    ]

    # One bulk INSERT regardless of batch size (50 / 100 / 200 / 300 / 500)
    db.execute(
        """
        INSERT INTO exam_domain.submissions
            (exam_id, student_id, answers, submitted_at, checksum)
        VALUES
            (:exam_id, :student_id, :answers, :submitted_at, :checksum)
        ON CONFLICT (exam_id, student_id) DO NOTHING
        """,
        rows,
    )

    # Delete processed messages from SQS
    sqs.delete_message_batch(
        QueueUrl=EXAM_SUBMISSION_QUEUE_URL,
        Entries=[
            {"Id": str(i), "ReceiptHandle": m["ReceiptHandle"]}
            for i, m in enumerate(messages)
        ],
    )
```

### Adaptive Batch — How It Scales

```
Queue depth    Batch size   Workers   DB writes/sec   Drain time (74K)
──────────────────────────────────────────────────────────────────────
< 500          50           2         ~100/sec         12 min
500–2K         100          4         ~400/sec         3 min
2K–10K         200          8         ~1,600/sec       46 sec
10K–30K        300          12        ~3,600/sec       21 sec
30K+           500          16        ~8,000/sec       9 sec
```

---

### SQS Queue Config

```python
# infra/sqs/queues.py (AWS CDK)

EXAM_SUBMISSION_QUEUE = {
    "queue_name":          "exam-submissions",
    "visibility_timeout":  60,       # 60s to process a batch before re-queue
    "retention_seconds":   86400,    # 1 day — if consumer dies, messages safe
    "max_retries":         3,        # before DLQ
    # No hardcoded batch_size here — Celery decides dynamically
}

EXAM_SUBMISSION_DLQ = {
    "queue_name":          "exam-submissions-dlq",
    "retention_seconds":   86400,    # alert + manual review
}
```

### Lambda — Reserved Concurrency

```python
LAMBDA_CONFIG = {
    "exam-submit": {
        "memory":               512,
        "timeout":              30,
        "reserved_concurrency": 500,   # hard cap — SQS absorbs overflow
    },
}
```

### Score + Rank Calculation (after exam closes)

```python
@shared_task(name="calculate_exam_results")
def calculate_exam_results(exam_id: str):
    # 1. Answer key from CDN
    answer_key = cdn_get(f"exams/{exam_id}/answer_key.json")

    # 2. Bulk score all submissions
    db.execute(
        "UPDATE exam_domain.submissions SET score = calculate_score(answers, :key) WHERE exam_id = :id",
        {"key": answer_key, "id": exam_id},
    )

    # 3. Rank — single PostgreSQL window function query
    results = db.execute(
        """
        SELECT student_id, score,
               RANK()         OVER (ORDER BY score DESC)                     AS rank,
               PERCENT_RANK() OVER (ORDER BY score DESC)                     AS percentile,
               RANK()         OVER (PARTITION BY state ORDER BY score DESC)  AS state_rank,
               RANK()         OVER (PARTITION BY city  ORDER BY score DESC)  AS city_rank
        FROM exam_domain.submissions WHERE exam_id = :id
        """,
        {"id": exam_id},
    ).fetchall()

    # 4. Result JSON per student → R2 → CDN
    for row in results:
        r2_put(f"results/{exam_id}/{row.student_id}.json", {
            "score": row.score, "rank": row.rank,
            "percentile": round((1 - row.percentile) * 100, 1),
            "state_rank": row.state_rank, "city_rank": row.city_rank,
        })

    # 5. CDN purge + FCM push (only logged-in students)
    process_cdn_flag.delay(
        content_id=f"results/{exam_id}", flag="FAST",
        urls=[f"{CDN_URL}/results/{exam_id}/*"],
        version_bump=True, module=f"results_{exam_id}",
        new_version=1, tenant_id="exam_domain",
    )
```

### Load Profile — What Actually Hits DB

```
During exam (2 hrs):    ZERO DB writes — every answer in IndexedDB on device
                        ZERO DB reads  — questions served from IndexedDB

App crash mid-exam:     ZERO data loss — IndexedDB has all answers
                        Student reopens → auto-resume from last saved answer

Submit window (5 min):  74K SQS messages → adaptive bulk INSERTs
                        Queue spikes → batch grows → clears fast
                        DB peak: ~8,000 writes/sec max (batch 500 × 16 workers)

After exam (+5 min):    1 score UPDATE, 1 rank SELECT, 74K R2 writes (async)
```

### Cost for One 74K-Student Exam

| Operation | Count | Cost |
|---|---|---|
| Lambda invocations (exam-submit) | 74,000 × 50ms × 512MB | ~₹50 |
| SQS messages | 74,000 sent + adaptive reads | ~₹1 |
| DB bulk INSERTs | adaptive (min 148, max 1,480 ops) | minimal |
| Score + rank query | 1 query | ₹0 |
| R2 result files | 74,000 × ~1KB = 74MB | ~₹5 |
| FCM push (logged-in only) | < 74,000 messages | ~₹25 |
| **Total per exam** | | **~₹81** |

---

## Exam Session Lock — Restrict Navigation

Once a student starts an exam they must stay until one of these **unlock conditions** is met:

```
Unlock condition 1 — Time gate:      50% of exam duration elapsed
Unlock condition 2 — Attempt gate:   100% of questions attempted
Unlock condition 3 — Timer expired:  Auto-submit, no student action needed

Submit button is DISABLED until condition 1 OR condition 2 is true.
```

### Scenarios Handled

| Scenario | Restriction |
|---|---|
| Student submits before 50% time AND < 100% attempted | Submit blocked — button disabled, reason shown |
| Student attempts all questions before 50% time | Submit allowed immediately — condition 2 met |
| 50% time elapsed, not all questions attempted | Submit allowed — condition 1 met |
| Student opens Exam A → tries to open Exam B | Blocked — "You have an active exam" |
| Student opens Exam A → presses Back | Cannot leave — back button blocked |
| Student closes app mid-exam | On return → force-navigated back to Exam A |
| Student device restarts mid-exam | IndexedDB restores session → resumes Exam A |
| Timer hits zero | Auto-submit from IndexedDB — no student action needed |
| Student opens exam on second device | Second device blocked — session tied to first device |

---

### DB — Exam Session Table

```sql
-- Only 1 active session per student at a time (enforced by UNIQUE partial index)

CREATE TABLE exam_domain.exam_sessions (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id   UUID NOT NULL,
    exam_id      UUID NOT NULL,
    started_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at   TIMESTAMPTZ NOT NULL,          -- started_at + exam duration
    status       TEXT NOT NULL DEFAULT 'active',
                 -- 'active' | 'submitted' | 'auto_submitted' | 'expired'
    device_id    TEXT NOT NULL,                 -- block second device
    tab_switches INT  NOT NULL DEFAULT 0,       -- proctoring: count app switches
    flagged      BOOLEAN NOT NULL DEFAULT false
);

-- Only 1 active session per student at a time
CREATE UNIQUE INDEX uq_student_active_session
    ON exam_domain.exam_sessions (student_id)
    WHERE status = 'active';
```

---

### Server — Start Exam (Session Lock)

```python
# services/exam/api/session.py

@router.post("/api/v1/exam/{exam_id}/start")
async def start_exam(
    exam_id: str,
    device_id: str,
    db: AsyncSession = Depends(get_db),
    student: User = Depends(get_current_user),
):
    # 1. Check if student already has an active session
    active = await db.execute(
        """
        SELECT exam_id, expires_at
        FROM exam_domain.exam_sessions
        WHERE student_id = :sid AND status = 'active'
        """,
        {"sid": student.id},
    )
    existing = active.fetchone()

    if existing:
        # Student has active exam — block
        raise HTTPException(status_code=409, detail={
            "code":       "ACTIVE_EXAM_EXISTS",
            "exam_id":    str(existing.exam_id),
            "expires_at": existing.expires_at.isoformat(),
            "message":    "You have an active exam. Submit it before starting another.",
        })

    # 2. Fetch exam config from CDN (duration, allowed_attempts)
    exam_config = cdn_get(f"exams/{exam_id}/config.json")

    # 3. Create session — locks student to this exam
    expires_at = datetime.utcnow() + timedelta(minutes=exam_config["duration_minutes"])
    await db.execute(
        """
        INSERT INTO exam_domain.exam_sessions
            (student_id, exam_id, expires_at, device_id)
        VALUES (:sid, :eid, :exp, :did)
        """,
        {"sid": student.id, "eid": exam_id, "exp": expires_at, "did": device_id},
    )

    return {"session_locked": True, "expires_at": expires_at.isoformat()}
```

```python
# Nightly Celery job — expire sessions where timer ran out but student didn't submit
@shared_task(name="expire_old_exam_sessions")
def expire_old_exam_sessions():
    db.execute(
        """
        UPDATE exam_domain.exam_sessions
        SET status = 'expired'
        WHERE status = 'active' AND expires_at < now()
        """
    )
    # Score calculation treats 'expired' same as 'auto_submitted'
```

---

### Submit Gate — Server Validation

```python
# services/exam/api/session.py

@router.post("/api/v1/exam/{exam_id}/submit")
async def submit_exam(
    exam_id: str,
    payload: SubmitPayload,
    db: AsyncSession = Depends(get_db),
    student: User = Depends(get_current_user),
):
    # 1. Fetch active session
    session = await db.execute(
        """
        SELECT started_at, expires_at
        FROM exam_domain.exam_sessions
        WHERE student_id = :sid AND exam_id = :eid AND status = 'active'
        """,
        {"sid": student.id, "eid": exam_id},
    ).fetchone()

    if not session:
        raise HTTPException(status_code=404, detail="No active exam session found.")

    # 2. Fetch exam config from CDN
    exam_config    = cdn_get(f"exams/{exam_id}/config.json")
    total_q        = exam_config["total_questions"]       # e.g. 50
    duration_min   = exam_config["duration_minutes"]      # e.g. 120

    # 3. Check unlock conditions
    now              = datetime.utcnow()
    elapsed_minutes  = (now - session.started_at).total_seconds() / 60
    half_time        = duration_min * 0.5                 # 60 min for 2hr exam
    answered_count   = len([a for a in payload.answers if a is not None])

    time_gate        = elapsed_minutes >= half_time       # 50% time elapsed
    attempt_gate     = answered_count  >= total_q         # 100% attempted

    if not time_gate and not attempt_gate:
        remaining_min = int(half_time - elapsed_minutes)
        raise HTTPException(status_code=403, detail={
            "code":             "SUBMIT_LOCKED",
            "reason":           "Neither submit condition met",
            "time_gate":        f"Submit allowed after {remaining_min} more minutes",
            "attempt_gate":     f"Attempt all {total_q - answered_count} remaining questions to submit now",
        })

    # 4. Conditions met — write to SQS
    await sqs_send("exam-submissions", {
        "exam_id":      exam_id,
        "student_id":   str(student.id),
        "answers":      payload.answers,
        "submitted_at": now.isoformat(),
        "checksum":     payload.checksum,
    })

    # 5. Mark session submitted
    await db.execute(
        "UPDATE exam_domain.exam_sessions SET status = 'submitted' WHERE student_id = :sid AND exam_id = :eid",
        {"sid": student.id, "eid": exam_id},
    )

    return {"submitted": True}
```

---

### Submit Gate — Flutter (Client-Side Button State)

Submit button state is computed locally from IndexedDB — no API call needed to decide enabled/disabled.

```dart
// Flutter — SubmitButton watches timer + answered count

class SubmitButtonController extends StateNotifier<SubmitButtonState> {
  final String examId;
  final DateTime startedAt;
  final int totalQuestions;
  final int durationMinutes;

  SubmitButtonController({
    required this.examId,
    required this.startedAt,
    required this.totalQuestions,
    required this.durationMinutes,
  }) : super(SubmitButtonState.locked());

  // Called every second by the exam timer tick
  void tick(int answeredCount) {
    final elapsed      = DateTime.now().difference(startedAt).inMinutes;
    final halfTime     = durationMinutes * 0.5;     // 50% of duration

    final timeGate     = elapsed >= halfTime;        // 60 min of 120
    final attemptGate  = answeredCount >= totalQuestions;  // all 50 answered

    if (timeGate || attemptGate) {
      state = SubmitButtonState.unlocked(
        reason: timeGate ? 'time_gate' : 'attempt_gate',
      );
    } else {
      final minsLeft    = (halfTime - elapsed).ceil();
      final questLeft   = totalQuestions - answeredCount;
      state = SubmitButtonState.locked(
        timeMessage:    'Submit unlocks in $minsLeft min',
        attemptMessage: 'OR attempt $questLeft more questions to submit now',
      );
    }
  }
}
```

```dart
// Submit button UI — shows unlock progress to student

Consumer(builder: (context, ref, _) {
  final btn = ref.watch(submitButtonProvider);

  return Column(children: [
    if (btn.isLocked) ...[
      // Show both unlock paths clearly
      LinearProgressIndicator(value: btn.timeProgress),   // time %
      Text(btn.timeMessage,    style: TextStyle(color: Colors.grey)),
      Text('OR', style: TextStyle(fontWeight: FontWeight.bold)),
      LinearProgressIndicator(value: btn.attemptProgress), // attempt %
      Text(btn.attemptMessage, style: TextStyle(color: Colors.grey)),
    ],

    ElevatedButton(
      onPressed: btn.isLocked ? null : _onSubmit,   // disabled if locked
      style: ElevatedButton.styleFrom(
        backgroundColor: btn.isLocked ? Colors.grey : Colors.green,
      ),
      child: Text(btn.isLocked ? 'Submit (locked)' : 'Submit Exam'),
    ),
  ]);
})
```

---

### Client — Flutter Navigation Lock

```dart
// Flutter — ExamSessionGuard wraps the entire exam screen

class ExamSessionGuard extends StatefulWidget {
  final String examId;
  final Widget child;
  const ExamSessionGuard({required this.examId, required this.child});
}

class _ExamSessionGuardState extends State<ExamSessionGuard>
    with WidgetsBindingObserver {

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);  // detect app going background
  }

  // Block Android back button
  Future<bool> _onWillPop() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Leave exam?'),
        content: const Text(
          'Your answers are saved. You cannot start another exam '
          'until this one is submitted or time expires.',
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false),
              child: const Text('Stay')),
          // No "Leave" button — student cannot exit without submitting
        ],
      ),
    );
    return confirmed ?? false;   // always false — cannot pop
  }

  // Detect app going to background (student switches app)
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused) {
      _recordTabSwitch();   // log to DB for proctoring
    }
    if (state == AppLifecycleState.resumed) {
      _checkSessionStillValid();   // confirm session not expired
    }
  }

  Future<void> _recordTabSwitch() async {
    // Increment tab_switch counter in DB (fire and forget)
    api.post('/api/v1/exam/${widget.examId}/tab-switch');

    // Warn student
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('⚠️ Leaving the exam screen has been recorded.'),
        backgroundColor: Colors.orange,
      ),
    );
  }

  Future<void> _checkSessionStillValid() async {
    final session = await ExamAnswerStore.resumeExam(widget.examId);
    if (session == null) {
      // Session expired or already submitted — navigate away
      Navigator.of(context).pushReplacementNamed('/exam-result/${widget.examId}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: _onWillPop,
      child: widget.child,
    );
  }
}
```

```dart
// On app launch — check if student has an active exam session
// If yes → force navigate to that exam regardless of where they try to go

class AppRouter {
  static Future<String> getInitialRoute() async {
    final activeSession = await ExamAnswerStore.getActiveSession();

    if (activeSession != null &&
        activeSession['submitted'] == false &&
        DateTime.parse(activeSession['expires_at']).isAfter(DateTime.now())) {

      // Student has an unfinished exam — force them back
      return '/exam/${activeSession['exam_id']}/resume';
    }

    return '/home';
  }
}
```

---

### Auto-Submit on Timer Expiry

```dart
// Flutter exam timer — auto-submits when it hits zero

class ExamTimer extends StatefulWidget {
  final DateTime expiresAt;
  final String examId;
}

class _ExamTimerState extends State<ExamTimer> {
  late Timer _timer;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), _tick);
  }

  void _tick(Timer t) {
    final remaining = widget.expiresAt.difference(DateTime.now());

    if (remaining.isNegative || remaining.inSeconds == 0) {
      _timer.cancel();
      _autoSubmit();   // time up — submit whatever is in IndexedDB
    }
  }

  Future<void> _autoSubmit() async {
    // Read from IndexedDB — same as manual submit
    final answers = await ExamAnswerStore.getForSubmission(widget.examId);
    await ExamSubmitService.submit(answers);   // → SQS → Celery → DB

    if (mounted) {
      Navigator.of(context).pushReplacementNamed(
        '/exam-result/${widget.examId}',
        arguments: {'auto_submitted': true},
      );
    }
  }
}
```

---

### Session Lock — Full Flow

```
Student starts Exam A (2 hr, 50 questions)
        ↓
Session created · Submit button DISABLED
        │
        ├── Path 1: Student answers all 50 questions at 40 min
        │          attempt_gate = true → Submit button ENABLED immediately
        │          Student submits at 40 min → session released
        │
        ├── Path 2: Student answers 30 questions, waits till 60 min (50% time)
        │          time_gate = true → Submit button ENABLED at 60 min mark
        │          Student submits → session released
        │
        ├── Path 3: Student tries to submit at 5 min (10 questions answered)
        │          Neither gate met → 403 SUBMIT_LOCKED
        │          UI shows: "Submit unlocks in 55 min OR attempt 40 more questions"
        │
        ├── Path 4: Timer hits zero (app open)
        │          Flutter auto-submit → IndexedDB → SQS → session = auto_submitted
        │
        └── Path 5: Timer hits zero (app closed)
                   Celery marks session 'expired'
                   Score calculated from last IndexedDB state

─────────────────────────────────────────────────────────
Student opens Exam B while Exam A is active:
  POST /api/v1/exam/{examB}/start → 409 ACTIVE_EXAM_EXISTS
  "Complete Exam A before starting another"

Student reopens app mid-exam:
  AppRouter finds active IndexedDB session → force-navigate to Exam A
  All previous answers restored → continues from last question
```

---

## Notification Strategy — Minimum Cost

### WhatsApp — Optional Paid Add-On Per Institution

```
Default (all institutions):   FCM push + in-app only → ₹0/month

WhatsApp add-on (opt-in):     Institution enables WhatsApp in settings
                               Institution pays per message (MSG91 rate)
                               EduForge charges: MSG91 cost + 10% commission
                               EduForge pays ₹0 — institution pays everything

Revenue for EduForge:         10% of all WhatsApp spend across all institutions
                               If institutions spend ₹10L/month → EduForge earns ₹1L
```

### Institution WhatsApp Billing Model

```
MSG91 WhatsApp rate:          ₹0.35/message (utility)
EduForge bills institution:   ₹0.385/message (₹0.35 + 10% commission)

Monthly billing:
  Institution A sent 10,000 WhatsApp messages
  MSG91 cost:     ₹3,500
  Commission:     ₹350
  Invoice to A:   ₹3,850

EduForge cost:    ₹0 (MSG91 bill goes to institution's wallet)
EduForge earns:   ₹350 (commission only)
```

### Two WhatsApp Plans for Institutions

| Plan | How it works | EduForge role |
|---|---|---|
| **Platform plan** | Institution uses EduForge's MSG91 pool · billed monthly | Routes messages · bills cost + 10% · earns commission |
| **BYOC** (Bring Your Own Credentials) | Institution provides own MSG91 API key · routes through EduForge platform | Routes only · charges flat ₹0.035/message platform fee (10% of ₹0.35) |

### Channel Rules

```
WhatsApp   → OPTIONAL per institution (disabled by default)
             Institution pays cost + 10% commission to EduForge
             Institution configures which triggers send WhatsApp
             EduForge platform earns commission, pays ₹0

SMS OTP    → ONLY for admin/lecturer first-time registration
             One SMS per staff account, lifetime

Email OTP  → ALL users forgot password (SES ₹0.007/email)
             Admins, lecturers, students, parents — same channel

FCM push   → ONLY board/entrance exam results
             One-time big event — student + parent notified immediately

In-app     → ALL other notifications (₹0)
             Fee due, attendance, academic results, mock results,
             PTM, announcements, absence alerts, work alerts
             Permanent record — user reads when they open app
```

### Who Gets Notified — Parent Only for Child Events

```
Student absent day 1–2  → in-app only
Student absent day 3    → in-app alert to parent (no FCM)
Fee due / overdue       → in-app only
PTM scheduled           → in-app only

Academic result         → notify PARENT only — digest
                           CONDITIONS (both must be true):
                           1. result_type = 'academic'  (school/coaching internal exam)
                           2. student appeared in that exam (has a result row)
                           NOT sent for: board exams, entrance exams, college results

Student gets FCM for:
  → Their own upcoming exam reminder
  → Study material updated (CDN bundle push)
  → Their own account/OTP actions only

Staff / Admin:
  → Their own work alerts (timetable, reports)
  → No student/parent events
```

### Result Handling — Notify vs Update Only

```
board     →  CBSE / ICSE / State board result
             ACTION: store result + FCM immediate to parent + student

entrance  →  JEE / NEET / CUET / CAT
             ACTION: store result + FCM immediate to student (+ parent if minor)

academic  →  school unit test, class test, term exam
             ACTION: store result only — visible in portal, NO notification

mock      →  coaching mock test / practice test
             ACTION: store result only — visible in portal, NO notification

college   →  university semester result
             ACTION: nothing — not stored, not notified
```

```
External results (board + entrance) = BIG events → FCM immediate
  → Board result: parent + student both notified immediately
  → Entrance result: student notified immediately, parent if student is minor

Academic / mock = routine → no FCM noise
  → Stored in portal, parent/student checks when they open app

College results → not handled by EduForge
```

```python
# services/notification/result_notifier.py

FCM_IMMEDIATE = {'board', 'entrance'}   # big events → immediate FCM
STORE_ONLY    = {'academic', 'mock'}    # routine → store, no notification
IGNORE_TYPES  = {'college'}             # do nothing

async def handle_result_published(
    exam_id:     str,
    result_type: str,
    tenant_id:   str,
    db:          AsyncSession,
):
    if result_type in IGNORE_TYPES:
        return   # college → do nothing

    # Store result for all result types (board, entrance, academic, mock)
    await store_results(exam_id, tenant_id, db)

    if result_type in STORE_ONLY:
        # academic / mock → stored, visible in portal, no FCM
        return

    # board / entrance → FCM immediate to student + parent
    appeared = await db.execute(
        """
        SELECT r.student_id, r.marks, r.total_marks, r.rank,
               s.name AS student_name, s.is_minor,
               p.id   AS parent_id
        FROM school_shard.results      r
        JOIN school_shard.students     s ON s.id     = r.student_id
        LEFT JOIN platform.parent_children p ON p.child_id = r.student_id
        WHERE r.exam_id  = :eid
        AND   r.marks    IS NOT NULL
        """,
        {"eid": exam_id},
    ).fetchall()

    for row in appeared:
        exam_label = "Board" if result_type == 'board' else "Entrance exam"

        # Always notify student directly (FCM immediate — bypass digest)
        await send_fcm_now(
            user_id=row.student_id,
            title=f"{exam_label} result published",
            body=f"Score: {row.marks}/{row.total_marks} · Rank: {row.rank}",
            data={"type": "external_result", "exam_id": exam_id,
                  "deep_link": f"/results/{exam_id}"},
        )

        # Notify parent if student is minor
        if row.parent_id and row.is_minor:
            await send_fcm_now(
                user_id=row.parent_id,
                title=f"{row.student_name} — {exam_label} result",
                body=f"Score: {row.marks}/{row.total_marks} · Rank: {row.rank}",
                data={"type": "external_result", "exam_id": exam_id,
                      "deep_link": f"/children/{row.student_id}/results"},
            )

        # Store in in-app inbox for both
        await store_notification_inbox(
            tenant_id, row.student_id, "external_result",
            f"{exam_label} result published",
            f"Score: {row.marks}/{row.total_marks} · Rank: {row.rank}",
        )
```

    # Only notify parents of students who actually appeared + have a result
    appeared = await db.execute(
        """
        SELECT r.student_id, r.marks, r.total_marks, r.subject,
               r.class_rank, p.id AS parent_id, s.name AS student_name
        FROM school_shard.results      r
        JOIN school_shard.students     s ON s.id = r.student_id
        JOIN platform.parent_children  p ON p.child_id = r.student_id
        WHERE r.exam_id = :eid
        AND   r.marks   IS NOT NULL     -- student has a result (appeared + marked)
        """,
        {"eid": exam_id},
    ).fetchall()

    # Queue notification for each parent (combined with other events at digest time)
    for row in appeared:
        await queue_notification(
            tenant_id=tenant_id,
            child_id=row.student_id,
            notif_type='result',
            data={
                "subject":    row.subject,
                "marks":      row.marks,
                "total":      row.total_marks,
                "rank":       row.class_rank,
                "exam_id":    exam_id,
            },
        )
    # Parent receives this in evening digest (6 PM) — not immediate
    # Combined with other events of the day in one FCM push
```

### Absence Escalation — Full Chain

```
Day 1–2   →  in-app record only. No FCM. No noise.
Day 3     →  FCM to PARENT immediately. Escalation level = 1.
Day 5     →  In-app alert to CLASS TEACHER. Level = 2.
Day 7     →  In-app alert to PRINCIPAL. Level = 3.
Day 10+   →  Welfare concern flag in DB. Shows on admin dashboard. Level = 4.

Present   →  Reset ALL: consecutive_absent_days = 0, escalation_level = 0
Teacher acknowledges (day 5) → pause escalation, no further alerts
```

### DB — Student Columns

```sql
ALTER TABLE school_shard.students
    ADD COLUMN consecutive_absent_days  INT     DEFAULT 0,
    ADD COLUMN absence_escalation_level INT     DEFAULT 0,
    -- 0=none 1=parent_notified 2=teacher_alerted 3=principal_alerted 4=welfare_concern
    ADD COLUMN absence_paused           BOOLEAN DEFAULT false,
    -- true when teacher acknowledges — stops further escalation
    ADD COLUMN welfare_concern          BOOLEAN DEFAULT false;
    -- true at level 4 — shows on admin welfare dashboard

CREATE INDEX idx_students_welfare
    ON school_shard.students (tenant_id, welfare_concern)
    WHERE welfare_concern = true;
```

### Attendance Service — Mark + Escalate

```python
# services/attendance/service.py

ESCALATION_THRESHOLDS = {
    3:  'parent',     # FCM to parent
    5:  'teacher',    # in-app to class teacher
    7:  'principal',  # in-app to principal
    10: 'welfare',    # flag on admin dashboard
}

async def mark_attendance(
    student_id: str,
    tenant_id:  str,
    status:     str,
    db:         AsyncSession,
):
    # 1. Write attendance record
    await db.execute(
        "INSERT INTO school_shard.attendance (student_id, date, status) VALUES (:sid, today(), :s)",
        {"sid": student_id, "s": status},
    )

    if status == 'present':
        # Reset everything on present
        await db.execute(
            """
            UPDATE school_shard.students
            SET consecutive_absent_days  = 0,
                absence_escalation_level = 0,
                absence_paused           = false,
                welfare_concern          = false
            WHERE id = :sid
            """,
            {"sid": student_id},
        )
        return

    # Absent — increment counter
    result = await db.execute(
        """
        UPDATE school_shard.students
        SET consecutive_absent_days = consecutive_absent_days + 1
        WHERE id = :sid
        RETURNING consecutive_absent_days, absence_escalation_level, absence_paused
        """,
        {"sid": student_id},
    )
    row  = result.fetchone()
    days = row.consecutive_absent_days

    # If teacher paused escalation → do nothing further
    if row.absence_paused:
        return

    # Trigger escalation only at exact thresholds (not every day)
    if days not in ESCALATION_THRESHOLDS:
        return

    student_name = await get_student_name(student_id, db)
    level        = ESCALATION_THRESHOLDS[days]

    await _escalate(
        student_id=student_id, tenant_id=tenant_id,
        student_name=student_name, days=days, level=level, db=db,
    )


async def _escalate(student_id, tenant_id, student_name, days, level, db):

    if level == 'parent':
        # Day 3 — in-app only (no FCM)
        parent = await get_parent(student_id, db)
        await store_notification_inbox(
            tenant_id, parent.id, "absence_alert",
            f"{student_name} absent {days} days in a row",
            "Please inform school if unwell. Contact class teacher.",
            deep_link=f"/children/{student_id}/attendance",
        )
        await db.execute(
            "UPDATE school_shard.students SET absence_escalation_level = 1 WHERE id = :sid",
            {"sid": student_id},
        )

    elif level == 'teacher':
        # Day 5 — in-app alert to class teacher (no FCM, no cost)
        teacher = await get_class_teacher(student_id, db)
        await store_notification_inbox(
            tenant_id, teacher.id, "absence_teacher_alert",
            f"{student_name} absent {days} days",
            "Parent notified on day 3. Please follow up.",
            actions=[
                {"label": "Mark as known absence", "action": "pause_escalation"},
                {"label": "Welfare check needed",  "action": "flag_welfare"},
            ],
        )
        await db.execute(
            "UPDATE school_shard.students SET absence_escalation_level = 2 WHERE id = :sid",
            {"sid": student_id},
        )

    elif level == 'principal':
        # Day 7 — in-app alert to principal (no FCM)
        principal = await get_principal(tenant_id, db)
        await store_notification_inbox(
            tenant_id, principal.id, "absence_principal_alert",
            f"{student_name} absent {days} days",
            "Teacher notified on day 5. Review required.",
            actions=[
                {"label": "Assign welfare officer", "action": "assign_welfare"},
                {"label": "Mark under review",      "action": "mark_review"},
            ],
        )
        await db.execute(
            "UPDATE school_shard.students SET absence_escalation_level = 3 WHERE id = :sid",
            {"sid": student_id},
        )

    elif level == 'welfare':
        # Day 10 — flag on admin welfare dashboard
        await db.execute(
            """
            UPDATE school_shard.students
            SET absence_escalation_level = 4,
                welfare_concern          = true
            WHERE id = :sid
            """,
            {"sid": student_id},
        )
        # Admin sees this on welfare dashboard — no notification sent
        # Dashboard query: SELECT * FROM students WHERE welfare_concern = true
```

### Teacher Acknowledge — Pause Escalation

```python
# Teacher marks "known absence" from in-app notification action

@router.post("/api/v1/attendance/pause-escalation")
async def pause_escalation(
    student_id: str,
    reason:     str,   # 'known_absence' | 'welfare_check_done'
    db:         AsyncSession = Depends(get_db),
    teacher:    User = Depends(get_current_user),
):
    await db.execute(
        """
        UPDATE school_shard.students
        SET absence_paused = true
        WHERE id = :sid
        """,
        {"sid": student_id},
    )
    # Log the acknowledgement
    await db.execute(
        """
        INSERT INTO school_shard.absence_acknowledgements
            (student_id, acknowledged_by, reason, acknowledged_at)
        VALUES (:sid, :uid, :reason, now())
        """,
        {"sid": student_id, "uid": teacher.id, "reason": reason},
    )
    return {"paused": True}
```

### Admin Welfare Dashboard Query

```python
# portal/apps/school/views/welfare.py
# Django view — fetches welfare concern students

def welfare_dashboard(request):
    concerns = db.execute(
        """
        SELECT s.name, s.consecutive_absent_days,
               s.absence_escalation_level, s.class_id,
               t.name AS teacher_name
        FROM school_shard.students s
        JOIN school_shard.classes c ON c.id = s.class_id
        JOIN school_shard.teachers t ON t.id = c.class_teacher_id
        WHERE s.tenant_id    = :tid
        AND   s.welfare_concern = true
        ORDER BY s.consecutive_absent_days DESC
        """,
        {"tid": request.tenant_id},
    ).fetchall()
    return render(request, "welfare/dashboard.html", {"concerns": concerns})
```

### Full Escalation — Cost

| Day | Action | Channel | Cost |
|---|---|---|---|
| 1–2 | In-app record | In-app | ₹0 |
| 3 | FCM to parent | FCM | ₹0 |
| 5 | In-app to teacher | In-app | ₹0 |
| 7 | In-app to principal | In-app | ₹0 |
| 10+ | DB flag → dashboard | DB write | ₹0 |
| **Total** | | | **₹0** |

### Combined Notification — One Push Covers All Events

```
Never send multiple FCM pushes to same parent for same day.
Collect all events → combine → ONE push.

Parent with 2 children — all events in one message:

  ┌─────────────────────────────────────┐
  │ 4 updates today                     │
  │                                     │
  │ Rahul (DPS Noida)                   │
  │  • Absent today                     │
  │  • Maths: 87/100 · Class rank: 3   │
  │                                     │
  │ Priya (ABC Coaching)                │
  │  • Fee ₹8,000 due in 3 days        │
  │  • Mock test AIR 1,243             │
  └─────────────────────────────────────┘

= 1 FCM push (not 4 separate pushes)
```

### Send Windows — When Combined Push is Sent

```
CRITICAL (emergency, safety, exam error)
  → Send immediately, bypass queue, no combining

All other events collected in queue:
  → Morning digest    8:00 AM  (previous night + morning events)
  → Afternoon digest  1:00 PM  (morning events)
  → Evening digest    6:00 PM  (full day summary)

Max 3 FCM pushes per parent per day regardless of how many events
```

### Full Channel Matrix

| Recipient | Trigger | Channel | Cost |
|---|---|---|---|
| Any user | Forgot password | Email OTP — AWS SES | ₹0.007/email |
| Admin / Lecturer | First registration | SMS OTP — MSG91 | ₹0.15 (once per account) |
| Student + Parent | Board / entrance result | **FCM immediate** | ₹0 |
| Parent | Fee due, attendance, PTM, academic result, mock result | **In-app only** | ₹0 |
| Student | Exam reminder, study bundle, OTP | **In-app only** | ₹0 |
| Admin / Lecturer | Work alerts, reports | **In-app only** | ₹0 |

> **FCM used for ONE event only: board/entrance result.**
> **Everything else: in-app notification only.**
> **WhatsApp: optional paid add-on per institution.**
> **SMS: ₹0.15 × new staff first registration only.**

### Institution WhatsApp Config — DB

```sql
-- Per-institution WhatsApp settings
ALTER TABLE platform.tenants ADD COLUMN IF NOT EXISTS
    whatsapp_enabled      BOOLEAN DEFAULT false,
    whatsapp_plan         TEXT    DEFAULT 'none',
    -- 'none' | 'platform' | 'byoc'
    whatsapp_api_key      TEXT,       -- encrypted, only for BYOC plan
    whatsapp_wallet       NUMERIC(10,2) DEFAULT 0,  -- prepaid balance
    whatsapp_triggers     TEXT[]  DEFAULT '{}';
    -- e.g. ['fee_due', 'fee_paid', 'result', 'emergency']
    -- institution chooses which events trigger WhatsApp

-- Track usage per tenant per month for billing
CREATE TABLE platform.whatsapp_usage (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id    UUID NOT NULL,
    month        DATE NOT NULL,        -- first day of month
    messages_sent INT DEFAULT 0,
    msg91_cost   NUMERIC(10,2) DEFAULT 0,   -- ₹0.35 × messages
    commission   NUMERIC(10,2) DEFAULT 0,   -- 10% of msg91_cost
    total_billed NUMERIC(10,2) DEFAULT 0,   -- msg91_cost + commission
    invoiced     BOOLEAN DEFAULT false,
    UNIQUE (tenant_id, month)
);
```

### Notification Queue + Combiner

```sql
-- Pending notifications waiting to be combined and sent
CREATE TABLE platform.notification_queue (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id   UUID NOT NULL,           -- always parent for child events
    tenant_id   UUID NOT NULL,
    child_id    UUID,                    -- which child this is about
    child_name  TEXT,
    type        TEXT NOT NULL,
    -- 'absent' | 'fee_due' | 'result' | 'ptm' | 'exam_result'
    data        JSONB NOT NULL,          -- event details
    is_critical BOOLEAN DEFAULT false,  -- critical = send immediately
    sent        BOOLEAN DEFAULT false,
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_notif_queue_unsent
    ON platform.notification_queue (parent_id, sent, created_at)
    WHERE sent = false;
```

### Notification Router — Queue + Combine

```python
# services/notification/router.py

# Events that go to PARENT (not student)
PARENT_EVENTS = {'absent', 'fee_due', 'fee_overdue', 'result',
                 'ptm', 'exam_result', 'welfare_alert'}

# Events that go to STUDENT directly
STUDENT_EVENTS = {'exam_reminder', 'bundle_update', 'otp'}

# FCM used ONLY for board/entrance results — handled separately in result_notifier.py
# Everything else → in-app only


async def queue_notification(
    tenant_id:  str,
    child_id:   str,
    notif_type: str,
    data:       dict,
):
    """All notifications → in-app only. No FCM. No combining needed.
    FCM is only used for board/entrance results (separate flow)."""

    if notif_type in PARENT_EVENTS:
        parent       = await get_parent(child_id)
        recipient_id = parent.id
        child_name   = await get_student_name(child_id)
    elif notif_type in STUDENT_EVENTS:
        recipient_id = child_id
        child_name   = None
    else:
        return   # unknown type — drop

    # In-app inbox only — no FCM
    await store_notification_inbox(tenant_id, recipient_id, notif_type, data)
```

### WhatsApp Combiner — School Days Only, Only If Events Exist

No FCM combining needed — all notifications are in-app only.
WhatsApp combiner runs only if institution has WhatsApp add-on enabled.

```python
# services/notification/whatsapp_combiner.py
# Only needed for institutions that paid for WhatsApp add-on

def is_school_day(tenant_id: str) -> bool:
    today = date.today()
    if today.weekday() == 6:          # Sunday
        return False
    is_holiday = db.execute(
        "SELECT 1 FROM platform.holidays WHERE tenant_id=:tid AND holiday_date=:d LIMIT 1",
        {"tid": tenant_id, "today": today},
    ).fetchone()
    return not is_holiday


@shared_task(name="send_whatsapp_digest")
def send_whatsapp_digest():
    """Runs at 6 PM Mon–Sat. Only for institutions with WhatsApp enabled.
    Skips holidays. Skips if no pending events."""

    # Only tenants with WhatsApp enabled
    tenants = db.execute(
        "SELECT id FROM platform.tenants WHERE whatsapp_enabled = true AND whatsapp_wallet > 0"
    ).fetchall()

    for tenant in tenants:
        if not is_school_day(tenant.id):
            continue

        pending = db.execute(
            """
            SELECT parent_id, array_agg(row_to_json(notification_queue.*)) AS events
            FROM platform.notification_queue
            WHERE tenant_id = :tid AND sent = false
            GROUP BY parent_id
            """,
            {"tid": tenant.id},
        ).fetchall()

        if not pending:
            continue   # nothing to send — skip this tenant

        tenant_cfg = get_tenant_config(tenant.id)

        # Calculate total cost before sending any message
        triggered_all = [
            e for row in pending
            for e in row.events
            if e['type'] in tenant_cfg.whatsapp_triggers
        ]
        total_messages   = len(set(row.parent_id for row in pending
                                   if any(e['type'] in tenant_cfg.whatsapp_triggers
                                          for e in row.events)))
        estimated_cost   = round(total_messages * 0.385, 2)   # ₹0.35 + 10% commission

        # Check wallet balance BEFORE sending — if insufficient, skip all
        if tenant_cfg.whatsapp_wallet < estimated_cost:
            # Log low balance — admin sees it in dashboard
            db.execute(
                """
                INSERT INTO platform.whatsapp_alerts
                    (tenant_id, alert_type, wallet_balance, required_cost, created_at)
                VALUES (:tid, 'insufficient_balance', :bal, :cost, now())
                """,
                {"tid": tenant.id,
                 "bal": tenant_cfg.whatsapp_wallet,
                 "cost": estimated_cost},
            )
            continue   # skip — don't send partial batch

        for row in pending:
            triggered = [e for e in row.events
                         if e['type'] in tenant_cfg.whatsapp_triggers]
            if not triggered:
                continue

            msg_cost = 0.385   # ₹0.35 MSG91 + ₹0.035 EduForge commission

            # Show cost in admin audit log before sending
            db.execute(
                """
                INSERT INTO platform.whatsapp_send_log
                    (tenant_id, parent_id, message_count, cost, created_at)
                VALUES (:tid, :pid, :cnt, :cost, now())
                """,
                {"tid": tenant.id, "pid": row.parent_id,
                 "cnt": 1, "cost": msg_cost},
            )

            body = "\n".join(f"• {format_event_line(e)}" for e in triggered)
            send_whatsapp(tenant_cfg, row.parent_id,
                          f"{len(triggered)} updates today", body)
            track_whatsapp_usage(tenant.id, cost=0.35, commission=0.035)

            # Deduct from wallet immediately after each send
            db.execute(
                "UPDATE platform.tenants SET whatsapp_wallet = whatsapp_wallet - :cost WHERE id = :tid",
                {"cost": msg_cost, "tid": tenant.id},
            )

        db.execute(
            "UPDATE platform.notification_queue SET sent=true WHERE tenant_id=:tid AND sent=false",
            {"tid": tenant.id},
        )
```

### Monthly Invoice — Celery Job (1st of every month)

```python
@shared_task(name="generate_whatsapp_invoices")
def generate_whatsapp_invoices():
    """Runs 1st of every month at 9 AM.
    Generates invoice for each institution that used WhatsApp last month."""

    last_month = (date.today().replace(day=1) - timedelta(days=1)).replace(day=1)

    usage_records = db.execute(
        """
        SELECT tenant_id, messages_sent, msg91_cost, commission, total_billed
        FROM platform.whatsapp_usage
        WHERE month = :month AND invoiced = false AND messages_sent > 0
        """,
        {"month": last_month},
    ).fetchall()

    for record in usage_records:
        # Deduct from institution's prepaid wallet
        db.execute(
            "UPDATE platform.tenants SET whatsapp_wallet = whatsapp_wallet - :amount WHERE id = :tid",
            {"amount": record.total_billed, "tid": record.tenant_id},
        )
        # Mark invoiced
        db.execute(
            "UPDATE platform.whatsapp_usage SET invoiced = true WHERE tenant_id = :tid AND month = :month",
            {"tid": record.tenant_id, "month": last_month},
        )
        # Generate PDF invoice → R2 (fee invoice pattern)
        generate_whatsapp_invoice_pdf.delay(record)

        # If wallet low → FCM alert to institution admin
        tenant = get_tenant(record.tenant_id)
        if tenant.whatsapp_wallet < 500:
            send_fcm(tenant.admin_user_id,
                title="WhatsApp wallet low",
                body=f"Balance ₹{tenant.whatsapp_wallet:.0f} — recharge to continue WhatsApp notifications")
```

### EduForge Revenue from WhatsApp Commission

| Institutions using WhatsApp | Avg messages/month | EduForge commission (10%) |
|---|---|---|
| 10 institutions × 5K messages | 50,000 msgs × ₹0.35 = ₹17,500 | ₹1,750/month |
| 50 institutions × 10K messages | 5L msgs × ₹0.35 = ₹1.75L | ₹17,500/month |
| 200 institutions × 20K messages | 40L msgs × ₹0.35 = ₹14L | ₹1.4L/month |

> EduForge infrastructure cost for WhatsApp: **₹0**
> All MSG91 costs pass through to institutions.
> Commission = pure revenue.

### Admin Cost Preview — Before Sending

Institution admin sees cost estimate **before** confirming a WhatsApp send.

```python
# services/notification/whatsapp_preview.py

@router.get("/api/v1/admin/whatsapp/cost-preview")
async def whatsapp_cost_preview(
    trigger: str,                           # 'fee_due' | 'result' | 'emergency'
    tenant_id: UUID = Depends(get_tenant),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns estimated cost BEFORE admin confirms the send.
    Admin sees: 'Sending to 480 parents will cost ₹184.80 · Wallet: ₹1,200'
    """
    cfg = await get_tenant_whatsapp_config(db, tenant_id)
    if not cfg.whatsapp_enabled or trigger not in cfg.whatsapp_triggers:
        return {"enabled": False, "reason": "trigger_not_configured"}

    # Count unique parents who will receive this message
    recipient_count = await db.scalar(
        """
        SELECT COUNT(DISTINCT parent_id)
        FROM platform.notification_queue
        WHERE tenant_id  = :tid
          AND event_type = :trigger
          AND sent_at    IS NULL
        """,
        {"tid": tenant_id, "trigger": trigger},
    )

    cost_per_msg    = 0.385                          # ₹0.35 MSG91 + 10% commission
    estimated_cost  = round(recipient_count * cost_per_msg, 2)
    wallet_balance  = cfg.whatsapp_wallet
    can_send        = wallet_balance >= estimated_cost

    return {
        "trigger":          trigger,
        "recipient_count":  recipient_count,
        "cost_per_message": cost_per_msg,
        "estimated_cost":   estimated_cost,          # ₹184.80
        "wallet_balance":   wallet_balance,          # ₹1,200.00
        "can_send":         can_send,                # true / false
        "shortfall":        round(max(0, estimated_cost - wallet_balance), 2),
    }
```

**Admin portal shows before confirm button:**

```
┌─────────────────────────────────────────────────┐
│  Send WhatsApp — Fee Due Reminder               │
│                                                 │
│  Recipients  :  480 parents                     │
│  Cost/msg    :  ₹0.385                          │
│  Total cost  :  ₹184.80                         │
│  Wallet      :  ₹1,200.00  ✅ Sufficient        │
│                                                 │
│  [ Cancel ]          [ Confirm & Send → ]       │
└─────────────────────────────────────────────────┘

-- If wallet is low: --

│  Wallet      :  ₹100.00  ⚠️ Insufficient        │
│  Shortfall   :  ₹84.80  — recharge first        │
│  [ Recharge Wallet ]     [ Cancel ]             │
```

---

### Holiday Calendar — DB Table

```sql
-- Institution uploads their holiday list once per year
-- Combiner checks this before sending any notification

CREATE TABLE platform.holidays (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id    UUID NOT NULL,
    holiday_date DATE NOT NULL,
    name         TEXT,           -- 'Diwali', 'Republic Day', 'Summer Break'
    UNIQUE (tenant_id, holiday_date)
);

-- Sunday check is in code (weekday() == 6) — no DB entry needed
```

### Celery Beat Schedule for Combiner

```python
# celery_config.py — notification combiner schedule

CELERYBEAT_SCHEDULE = {
    # ... existing schedules ...

    # 8 AM — morning digest (previous night + early morning events)
    "notify-morning": {
        "task":     "send_combined_notifications",
        "schedule": crontab(hour=8, minute=0),
        # Celery runs it — but task itself checks is_school_day() per tenant
        # Runs Mon–Sat only at OS level as extra guard:
        # crontab(hour=8, minute=0, day_of_week='1-6')
    },
    # 1 PM — afternoon digest (morning school events)
    "notify-afternoon": {
        "task":     "send_combined_notifications",
        "schedule": crontab(hour=13, minute=0, day_of_week='1-6'),
    },
    # 6 PM — evening digest (full day summary)
    "notify-evening": {
        "task":     "send_combined_notifications",
        "schedule": crontab(hour=18, minute=0, day_of_week='1-6'),
    },
}
```

```
day_of_week='1-6'  →  Mon–Sat only at scheduler level
                       Sunday: Celery never triggers the task
                       Holiday: task triggers but is_school_day() returns False → skips
                       No events: pending query returns [] → returns immediately

Result: zero FCM pushes on Sundays, holidays, or days with no events
```

---

### In-App Notification Inbox

Every FCM push has a matching record in DB — parent/student sees full history in app.

```sql
CREATE TABLE platform.notifications (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      UUID NOT NULL,
    tenant_id    UUID NOT NULL,
    type         TEXT NOT NULL,
    -- 'fee_due' | 'fee_paid' | 'attendance' | 'result' | 'ptm' | 'announcement'
    title        TEXT NOT NULL,
    body         TEXT NOT NULL,
    deep_link    TEXT,               -- opens specific screen in app
    is_read      BOOLEAN DEFAULT false,
    created_at   TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_notifications_user_unread
    ON platform.notifications (user_id, is_read, created_at DESC)
    WHERE is_read = false;
```

### Fee Notification — FCM + In-App (replaces WhatsApp)

```python
# services/notification/fee_reminder.py

@shared_task(name="send_fee_reminders")
def send_fee_reminders():
    """Celery beat — runs every Monday 8 AM.
    FCM push to parents with fee due in ≤ 7 days.
    No WhatsApp. No SMS. Zero cost."""

    due_soon = db.execute(
        """
        SELECT f.parent_id, f.student_name, f.amount_due,
               f.due_date, u.fcm_token
        FROM platform.fee_records f
        JOIN platform.users u ON u.id = f.parent_id
        WHERE f.status     = 'unpaid'
        AND   f.due_date  <= now() + interval '7 days'
        AND   f.due_date   > now()
        """
    ).fetchall()

    # Group by parent — one notification covers all children
    by_parent = group_by_parent(due_soon)

    for parent_id, records in by_parent.items():
        if len(records) == 1:
            title = f"Fee due in {records[0].days_left} days"
            body  = f"{records[0].student_name}: ₹{records[0].amount_due:,}"
        else:
            total = sum(r.amount_due for r in records)
            title = f"Fee due for {len(records)} children"
            body  = " · ".join(
                f"{r.student_name} ₹{r.amount_due:,}" for r in records
            ) + f" · Total ₹{total:,}"

        # 1. FCM push (free)
        send_fcm(
            token=records[0].fcm_token,
            title=title,
            body=body,
            data={"type": "fee_due", "deep_link": "/fees/pay"},
        )

        # 2. Store in notification inbox (free)
        db.execute(
            """
            INSERT INTO platform.notifications
                (user_id, tenant_id, type, title, body, deep_link)
            VALUES (:uid, :tid, 'fee_due', :title, :body, '/fees/pay')
            """,
            {"uid": parent_id, "tid": records[0].tenant_id,
             "title": title, "body": body},
        )
```

### Forgot Password — Email OTP via SES (All Users)

```python
# services/identity/password.py

@router.post("/api/v1/auth/forgot-password")
async def forgot_password(email: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email)
    if not user:
        return {"message": "If email exists, OTP sent."}  # don't leak existence

    otp  = generate_otp()
    await store_otp(db, user.id, otp, expires_minutes=10)

    # AWS SES — ₹0.007 per email (all users: admin, lecturer, student, parent)
    ses.send_email(
        Source="noreply@eduforge.in",
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": "EduForge — Password Reset OTP"},
            "Body": {"Text": {"Data":
                f"Your OTP to reset password: {otp}\n"
                f"Valid for 10 minutes. Do not share."
            }},
        },
    )
    return {"message": "OTP sent to your email."}
```

### Cost Comparison

| Item | Old | New | Saving/month (1L users) |
|---|---|---|---|
| Fee reminders (WhatsApp) | ₹0.35 × weekly × parents | ₹0 (FCM) | ₹1.4L+ |
| Fee paid confirmation | ₹0.35 × each payment | ₹0 (FCM) | ₹35,000+ |
| Forgot password (SMS OTP) | ₹0.15 × resets | ₹0.007 × resets (SES) | 95% cheaper |
| Staff registration OTP | ₹0.15 × new staff | ₹0.15 × new staff | unchanged |
| **WhatsApp total** | **₹2–5L/month** | **₹0** | **₹2–5L/month** |

---

## Cost Impact Summary

| Optimisation | Monthly Saving |
|---|---|
| Photos in IndexedDB (not CDN) | ₹15,000–50,000 |
| 2-day inactive user CDN cleanup | ₹10,000–30,000 |
| PDF only for fee + progress report | ₹5,000–20,000 |
| Peak-hour batch purge (fewer Cloudflare API calls) | ₹2,000–5,000 |
| CloudWatch 1-day retention for DB-ops logs | ₹3,000–8,000 |
| Lambda ARM (Graviton) 20% cheaper | ₹5,000–15,000 |
| Lambda right-sizing (128MB for simple ops) | ₹8,000–20,000 |
| DB nightly cleanup (smaller DB = cheaper storage) | ₹2,000–5,000 |
| **Total saving** | **₹50,000–1,53,000/month** |

---

## Scaling Tiers — Infrastructure & Cost

> CDN-first: ~35KB per student in DB (user activity only). 300K students per shard.
> All costs in ₹/month · AWS ap-south-1 (Mumbai) · on-demand pricing.
> Cloudflare R2 + CDN = ₹0 egress at all tiers. SQS = near ₹0 (critical ops only).

| Tier | Students | DB Shards | DB Instance | PgBouncer | Fargate Tasks | Lambda | Total/month | Per student/yr |
|---|---|---|---|---|---|---|---|---|
| **10K** | 10,000 | 1 shared | db.t3.small | ❌ | 1 × 0.25vCPU | free tier | **₹3,000** | ₹3.6 |
| **20K** | 20,000 | 1 shared | db.t3.small | ❌ | 1 × 0.25vCPU | ₹200 | **₹3,500** | ₹2.1 |
| **30K** | 30,000 | 1 | db.t3.medium | ❌ | 1 × 0.5vCPU | ₹300 | **₹5,500** | ₹2.2 |
| **40K** | 40,000 | 1 | db.t3.medium | ❌ | 2 × 0.5vCPU | ₹400 | **₹7,000** | ₹2.1 |
| **50K** | 50,000 | 1 | db.t3.medium | ✅ t3.micro | 2 × 0.5vCPU | ₹500 | **₹8,000** | ₹1.9 |
| **1L** | 1,00,000 | 1 | db.t3.large | ✅ t3.micro | 2 × 1vCPU | ₹1,000 | **₹12,000** | ₹1.4 |
| **2L** | 2,00,000 | 1 | db.t3.large | ✅ t3.small | 3 × 1vCPU | ₹2,000 | **₹16,000** | ₹0.96 |
| **3L** | 3,00,000 | 1 (full) | db.t3.large | ✅ t3.small | 3 × 1vCPU | ₹3,000 | **₹18,000** | ₹0.72 |
| **4L** | 4,00,000 | 2 | 2 × db.t3.large | ✅ 2 × t3.micro | 4 × 1vCPU | ₹4,000 | **₹28,000** | ₹0.84 |
| **10L** | 10,00,000 | 4 | 4 × db.t3.large | ✅ 4 × t3.micro | 8 × 1vCPU | ₹8,000 | **₹58,000** | ₹0.70 |

### Per-Tier Infrastructure Notes

```
10K–20K   → 1 shared shard · no PgBouncer · 1 Fargate task · Lambda free tier
            Aurora Serverless v2 option: ₹0 idle (schools with long holidays)

30K–50K   → 1 dedicated shard · db.t3.medium · PgBouncer from 50K
            2 Fargate tasks for HA

1L–3L     → 1 large shard (db.t3.large handles up to 300K CDN-first)
            PgBouncer mandatory · 2–3 Fargate tasks

4L        → shard split: 2 × db.t3.large · 2 PgBouncer nodes
            Separate shard per institution cluster

10L       → 4 shards · 4 PgBouncer · 8 Fargate tasks
            Switch to reserved instances → 40% cheaper
            10L on-demand ₹58,000 → reserved ₹35,000/month
```

### At 5 Crore (500L) Users

```
Old approach (80K/shard):     625 shards → ₹10.5L/month
CDN-first (300K/shard):       167 shards → ₹2.0L/month
+ Reserved instances:                    → ₹1.2L/month
Saving: ₹9.3L/month
```

---

## PgBouncer — Connection Pooling (Required at Scale)

```
Without PgBouncer:
  Peak 50K concurrent users → 50K DB connections → PostgreSQL crashes

With PgBouncer:
  50K app connections → PgBouncer → 50 actual DB connections (transaction mode)
  100x reduction · DB handles 10x more users · smaller instance class

Deploy: 1 × EC2 t3.micro per shard cluster (₹600/month)
```

---

## Monorepo Structure

```
eduforge/
│
├── identity/                        ← Auth service (FastAPI · Lambda · port 8001)
├── portal/                          ← Staff + student portals (Django · Fargate · port 8002)
├── services/
│   ├── exam/                        ← Exam engine (FastAPI · Lambda · port 8003)
│   ├── notification/                ← WhatsApp/SMS/Email (FastAPI · Lambda · port 8004)
│   ├── billing/                     ← Fees + Razorpay (FastAPI · Lambda · port 8005)
│   ├── ai/                          ← AI engine (FastAPI · Lambda · port 8006)
│   └── analytics/                   ← Reports + dashboards (FastAPI · Lambda · port 8007)
│
├── packages/                        ← Shared Python packages (imported by all services)
│   ├── core/                        ← Base classes, exceptions, constants
│   ├── db/                          ← Shard router, DB connection factory
│   ├── auth_client/                 ← JWT validation utility (used by all services)
│   ├── sqs_client/                  ← SQS producer/consumer wrapper
│   ├── storage/                     ← Cloudflare R2 client
│   ├── pdf/                         ← PDF generation (salary slips, certificates)
│   ├── excel/                       ← Bulk CSV/Excel import-export
│   ├── permissions/                 ← Permission check utilities
│   ├── observability/               ← Structured logging + trace IDs
│   ├── event_schemas/               ← SQS event schema definitions
│   └── ui/                          ← Shared Tailwind config, design tokens
│
├── apps/
│   ├── mobile/                      ← Flutter monorepo
│   │   ├── student_app/             ← Student Flutter app
│   │   ├── parent_app/              ← Parent Flutter app
│   │   └── packages/
│   │       ├── core/                ← Shared Riverpod providers
│   │       ├── ui_kit/              ← Shared Flutter widgets
│   │       └── api_client/          ← Auto-generated API client
│   └── marketing_site/              ← eduforge.in public website
│
├── infra/                           ← AWS CDK / Terraform
│   ├── lambda/
│   ├── fargate/
│   ├── rds/
│   ├── sqs/
│   ├── cloudflare/
│   ├── vpc/
│   ├── monitoring/
│   └── secrets/
│
├── tests/
│   ├── e2e/                         ← Playwright end-to-end tests
│   └── load/                        ← k6 load tests (74K concurrent exam peak)
│
├── docs/
│   └── modules/                     ← Module specifications (this folder)
│
├── scripts/
│   ├── bootstrap.sh                 ← First-time setup
│   ├── create_module.sh             ← Scaffold new module
│   └── migrate.sh                   ← Run Alembic migrations
│
├── docker-compose.yml               ← Local development (all services + DB)
├── Makefile                         ← Root commands
├── pyproject.toml                   ← Root uv workspace config
├── ruff.toml                        ← Shared Python linting
├── .pre-commit-config.yaml          ← Pre-commit hooks
└── .github/
    └── workflows/
        ├── ci.yml                   ← Test only changed modules
        └── deploy.yml               ← Deploy only changed modules
```

---

## Quick Start — Local Development

```bash
# 1. Prerequisites
#    Python 3.12, Docker Desktop, Flutter 3.x, Git

# 2. Install uv (fast free Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Clone repo
git clone https://github.com/sravanmodemkumar-arch/mocktest.git eduforge
cd eduforge

# 4. Copy environment file
cp .env.example .env
# Edit .env — add your DB URL, SQS queue URLs, Cloudflare keys

# 5. Start PostgreSQL + local services
docker-compose up -d

# 6. Run identity service (auth)
cd identity
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8001

# 7. Run portal service (Django)
cd ../portal
uv sync
uv run python manage.py migrate
uv run python manage.py runserver 8002

# 8. API docs
# Identity: http://localhost:8001/docs
# Portal:   http://localhost:8002/
```

---

## docker-compose.yml

```yaml
version: "3.9"

services:

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB:       eduforge
      POSTGRES_USER:     eduforge
      POSTGRES_PASSWORD: eduforge_local
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init_schemas.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U eduforge"]
      interval: 5s
      timeout: 5s
      retries: 5

  identity:
    build: ./identity
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
    ports:
      - "8001:8001"
    environment:
      DATABASE_URL: postgresql+asyncpg://eduforge:eduforge_local@db:5432/eduforge
      JWT_SECRET:   local_dev_secret_change_in_production
      ENVIRONMENT:  development
    volumes:
      - ./identity:/app
    depends_on:
      db:
        condition: service_healthy

  portal:
    build: ./portal
    command: python manage.py runserver 0.0.0.0:8002
    ports:
      - "8002:8002"
    environment:
      DATABASE_URL:    postgresql://eduforge:eduforge_local@db:5432/eduforge
      IDENTITY_URL:    http://identity:8001
      ENVIRONMENT:     development
    volumes:
      - ./portal:/app
    depends_on:
      - db
      - identity

  exam:
    build: ./services/exam
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8003
    ports:
      - "8003:8003"
    environment:
      DATABASE_URL: postgresql+asyncpg://eduforge:eduforge_local@db:5432/eduforge
      IDENTITY_URL: http://identity:8001
    volumes:
      - ./services/exam:/app
    depends_on:
      - db
      - identity

volumes:
  postgres_data:
```

---

## .env.example

```bash
# Environment
ENVIRONMENT=development          # development | staging | production

# Database
DATABASE_URL=postgresql+asyncpg://eduforge:eduforge_local@localhost:5432/eduforge

# JWT
JWT_SECRET=change_this_to_256_bit_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# AWS
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

# SQS Queue URLs (critical ops only)
SQS_NOTIFICATIONS_OTP_URL=https://sqs.ap-south-1.amazonaws.com/xxx/notifications-otp
SQS_NOTIFICATIONS_ALERT_URL=https://sqs.ap-south-1.amazonaws.com/xxx/notifications-alert
SQS_DATA_DELETION_URL=https://sqs.ap-south-1.amazonaws.com/xxx/data-deletion

# Cloudflare R2
CF_ACCOUNT_ID=your_cloudflare_account_id
CF_R2_ACCESS_KEY=your_r2_access_key
CF_R2_SECRET_KEY=your_r2_secret_key
CF_R2_BUCKET_NAME=eduforge-storage
CF_CDN_URL=https://cdn.eduforge.in

# Google OAuth2 (social login)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8001/api/v1/auth/google/callback

# MSG91 (WhatsApp / SMS for critical OTPs)
MSG91_AUTH_KEY=your_msg91_key
MSG91_TEMPLATE_OTP=your_template_id

# Internal service URLs (local dev)
IDENTITY_URL=http://localhost:8001
PORTAL_URL=http://localhost:8002
EXAM_URL=http://localhost:8003
```

---

## Identity Service Setup

```
identity/
├── app/
│   ├── main.py                ← FastAPI app + Mangum Lambda handler
│   ├── core/
│   │   ├── config.py          ← Settings from env vars (pydantic-settings)
│   │   └── deps.py            ← Shared FastAPI dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py            ← OAuth2 token endpoints
│   │   ├── otp.py             ← OTP send + verify (critical ops)
│   │   ├── password.py        ← forgot, reset, change password
│   │   ├── profile.py         ← me, update, sessions
│   │   ├── oauth2.py          ← B2B OAuth2 flows
│   │   └── social.py          ← Google OAuth2
│   ├── models/
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── otp.py
│   │   └── oauth2_client.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── otp.py
│   │   └── user.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── otp_service.py
│   │   ├── password_service.py
│   │   ├── session_service.py
│   │   └── google_auth_service.py
│   ├── middleware/
│   │   └── tenant.py          ← subdomain → tenant_id
│   └── utils/
│       ├── jwt.py
│       └── security.py
├── migrations/
│   ├── env.py
│   └── versions/
│       └── 001_auth_tables.py
├── tests/
│   ├── conftest.py
│   ├── test_login.py
│   ├── test_otp.py
│   └── test_oauth2.py
├── handler.py                 ← Lambda entrypoint (Mangum)
├── pyproject.toml
└── Dockerfile
```

```toml
# identity/pyproject.toml
[project]
name = "eduforge-identity"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi==0.111.0",
    "mangum==0.17.0",
    "python-jose[cryptography]==3.3.0",
    "passlib[bcrypt]==1.7.4",
    "sqlalchemy==2.0.30",
    "alembic==1.13.1",
    "asyncpg==0.29.0",
    "httpx==0.27.0",
    "pydantic==2.7.0",
    "pydantic-settings==2.2.0",
    "boto3==1.34.0",
    "python-multipart",
    "uvicorn[standard]==0.29.0",
]

[tool.uv]
dev-dependencies = [
    "pytest==8.2.0",
    "pytest-asyncio==0.23.0",
    "pytest-cov==5.0.0",
    "httpx==0.27.0",
    "ruff",
    "mypy",
]
```

```python
# identity/app/main.py

from fastapi import FastAPI
from mangum import Mangum
from app.api import auth, otp, password, profile, oauth2, social
from app.middleware.tenant import TenantMiddleware
from app.core.config import settings

app = FastAPI(
    title="EduForge Identity Service",
    version="0.1.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
)

# Middleware — resolves subdomain to tenant_id on every request
app.add_middleware(TenantMiddleware)

# Routers
app.include_router(auth.router,     tags=["auth"])
app.include_router(otp.router,      tags=["otp"])
app.include_router(password.router, tags=["password"])
app.include_router(profile.router,  tags=["profile"])
app.include_router(oauth2.router,   tags=["oauth2"])
app.include_router(social.router,   tags=["social"])

@app.get("/health")
async def health():
    return {"status": "ok", "service": "identity"}

# Lambda handler — wraps FastAPI for AWS Lambda + API Gateway
handler = Mangum(app, lifespan="off")
```

```python
# identity/app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT:                str  = "development"
    DATABASE_URL:               str
    JWT_SECRET:                 str
    JWT_ALGORITHM:              str  = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS:  int  = 7
    AWS_REGION:                 str  = "ap-south-1"
    SQS_NOTIFICATIONS_OTP_URL:  str  = ""
    CF_CDN_URL:                 str  = "https://cdn.eduforge.in"
    GOOGLE_CLIENT_ID:           str  = ""
    GOOGLE_CLIENT_SECRET:       str  = ""

    class Config:
        env_file = ".env"

settings = Settings()
```

```python
# identity/app/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    echo=settings.ENVIRONMENT == "development",
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

```python
# identity/app/middleware/tenant.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host", "")
        # abc-school.schools.eduforge.in → "sch_0501"
        tenant_id = await resolve_tenant_from_host(host)
        request.state.tenant_id = tenant_id
        response = await call_next(request)
        return response

async def resolve_tenant_from_host(host: str) -> str | None:
    parts = host.split(".")
    if len(parts) >= 4:
        subdomain = parts[0]          # "abc-school"
        inst_type = parts[1]          # "schools" | "colleges" | "coaching"
        return await lookup_tenant_id(subdomain, inst_type)
    return None                       # platform root domain
```

---

## Portal Service Setup (Django)

```
portal/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   └── urls.py
├── apps/
│   ├── school/                ← School portal pages (HTMX)
│   ├── college/               ← College portal pages
│   ├── coaching/              ← Coaching portal pages
│   ├── exam_domain/           ← Exam domain portal
│   ├── parent/                ← Parent portal
│   └── shared/                ← Shared views, components
├── templates/
│   ├── base.html              ← Tenant-branded base template
│   ├── components/            ← Reusable HTMX partials
│   └── pages/                 ← Full page templates
├── static/
│   ├── css/                   ← Tailwind (CDN only — no build step)
│   └── js/                    ← HTMX 1.9, Alpine.js
├── manage.py
└── pyproject.toml
```

```python
# portal/config/settings/base.py

INSTALLED_APPS = [
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "apps.school",
    "apps.college",
    "apps.coaching",
    "apps.exam_domain",
    "apps.parent",
    "apps.shared",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "apps.shared.middleware.TenantMiddleware",    # subdomain → tenant
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# No Redis — Django sessions in PostgreSQL
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_HTTPONLY  = True
SESSION_COOKIE_SECURE    = True   # HTTPS only
SESSION_COOKIE_SAMESITE  = "Strict"
```

```html
<!-- portal/templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ tenant.institution_name }}</title>
  <link rel="icon" href="{{ tenant.favicon_url }}">

  <!-- Tailwind CDN — no build step needed -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: "{{ tenant.primary_color }}",
            secondary: "{{ tenant.secondary_color }}",
          }
        }
      }
    }
  </script>

  <!-- HTMX 1.9 CDN -->
  <script src="https://unpkg.com/htmx.org@1.9.12"></script>
</head>
<body class="bg-gray-50">
  {% include "components/navbar.html" %}
  {% block content %}{% endblock %}
  {% include "components/toast.html" %}
</body>
</html>
```

---

## Alembic Setup (Migrations)

```python
# identity/migrations/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from alembic import context
from app.models import *          # import all models to register metadata
from app.database import Base

config = context.config
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section))
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema="platform",   # migrations table in platform schema
            include_schemas=True,
        )
        with context.begin_transaction():
            context.run_migrations()
```

```bash
# Run migrations
cd identity
uv run alembic upgrade head

# Create new migration
uv run alembic revision --autogenerate -m "add_users_table"

# Rollback
uv run alembic downgrade -1
```

---

## Makefile — Root Commands

```makefile
.PHONY: setup dev test lint migrate

# First-time setup
setup:
	cp .env.example .env
	docker-compose up -d db
	cd identity && uv sync && uv run alembic upgrade head
	cd portal && uv sync && uv run python manage.py migrate
	@echo "Setup complete. Run 'make dev' to start."

# Start all services locally
dev:
	docker-compose up

# Run tests for a specific service
test:
	cd identity && uv run pytest tests/ -v --cov=app

# Lint all Python
lint:
	uv run ruff check .
	uv run ruff format --check .

# Run migrations
migrate:
	cd identity && uv run alembic upgrade head
	cd portal && uv run python manage.py migrate

# Create a new module scaffold
module:
	@read -p "Module name (e.g. 02-tenancy): " name; \
	bash scripts/create_module.sh $$name
```

---

## ruff.toml — Shared Linting Config

```toml
line-length = 100
target-version = "py312"

[lint]
select = ["E", "F", "I", "N", "UP", "S", "B", "A", "C4", "PT"]
ignore = ["S101"]   # allow assert in tests

[lint.isort]
known-first-party = ["app", "packages"]

[format]
quote-style = "double"
indent-style = "space"
```

---

## GitHub Actions — CI

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop, "feature/*"]
  pull_request:
    branches: [main, develop]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      identity: ${{ steps.changes.outputs.identity }}
      portal:   ${{ steps.changes.outputs.portal }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: changes
        with:
          filters: |
            identity: ['identity/**']
            portal:   ['portal/**']

  test-identity:
    needs: detect-changes
    if: needs.detect-changes.outputs.identity == 'true'
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: eduforge_test
          POSTGRES_USER: eduforge
          POSTGRES_PASSWORD: test
        ports: ["5432:5432"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: cd identity && uv sync
      - run: cd identity && uv run pytest tests/ -v --cov=app
        env:
          DATABASE_URL: postgresql+asyncpg://eduforge:test@localhost:5432/eduforge_test
          JWT_SECRET: test_secret_32_chars_minimum_here
```

---

## Git Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Production — protected, requires PR |
| `develop` | Integration branch |
| `feature/module-specs` | Module documentation (current) ← |
| `feature/01-auth` | Auth service implementation |
| `feature/02-tenancy` | Tenancy service implementation |
| `feature/portal-school` | School portal pages |
| `feature/mobile-student` | Student Flutter app |

```bash
# Start work on a new module
git checkout develop
git checkout -b feature/01-auth

# After implementation
git push origin feature/01-auth
# Open PR → develop → review → merge → deploy
```

---

## Database Schemas (PostgreSQL)

```sql
-- scripts/init_schemas.sql
-- Run once on fresh DB

CREATE SCHEMA IF NOT EXISTS platform;       -- auth, users, tenants, billing
CREATE SCHEMA IF NOT EXISTS school_shard;   -- school institutions (dynamic)
CREATE SCHEMA IF NOT EXISTS college_shard;  -- college institutions (dynamic)
CREATE SCHEMA IF NOT EXISTS coaching_shard; -- coaching centers (dynamic)
CREATE SCHEMA IF NOT EXISTS exam_domain;    -- B2C exam domains (SSC, RRB etc.)
CREATE SCHEMA IF NOT EXISTS analytics;      -- pre-aggregated analytics data
```

---

## Services Summary

| Service | Port | Runtime | Framework | DB Schema |
|---|---|---|---|---|
| identity | 8001 | Lambda | FastAPI | platform |
| portal | 8002 | Fargate | Django + HTMX | (calls other services) |
| exam | 8003 | Lambda | FastAPI | exam_domain |
| notification | 8004 | Lambda | FastAPI | platform |
| billing | 8005 | Lambda | FastAPI | platform |
| ai | 8006 | Lambda | FastAPI | platform |
| analytics | 8007 | Lambda | FastAPI | analytics |

---

## Current Branch

```
feature/module-specs   ← all 57 module spec .md files go here
```

Module spec files created here, reviewed, then merged to `develop` before implementation branches start.
