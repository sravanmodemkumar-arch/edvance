# 44 — Mobile App Analytics

---

## 1. Page Metadata

| Field | Value |
|---|---|
| Page title | Mobile App Analytics |
| Route | `/exec/mobile-analytics/` |
| Django view | `MobileAnalyticsView` |
| Template | `exec/mobile_analytics.html` |
| Priority | **P2** |
| Nav group | Engineering |
| Required roles | `cto` · `mobile_engineer` · `ceo` · `superadmin` |
| COO / CFO | Denied |
| HTMX poll — live metrics | Every 300s |
| Cache | Redis TTL 290s |
| Theme tokens | bg-base `#040810` · surface-1 `#08101E` · accent `#6366F1` · danger `#EF4444` · warn `#F59E0B` · success `#22C55E` |

---

## 2. Purpose & Business Logic

**EduForge's Flutter mobile app (iOS + Android):**
- ~3M+ installs
- Students use it for exam participation, results, study materials
- Institution admins use it for monitoring and quick actions

Key mobile-specific risks:
1. **Crash rate** — a crash during exam submission = lost attempt (student must contact support)
2. **FCM delivery** — exam notifications via Firebase Cloud Messaging. Failed delivery = student misses exam
3. **Force-update compliance** — security patches require force-update. Students on old versions = security risk
4. **App store ratings** — falling below 4.0 stars = reduced organic downloads = slower institution growth

---

## 3. User Roles & Access

| Role | Can View | Can Act |
|---|---|---|
| CEO | All (read-only) | None |
| CTO | All | Trigger force-update, view crash reports |
| Mobile Engineer | All | Same as CTO |
| Others | No access | Redirect |

---

## 4. Section-wise UI Breakdown

---

### Section 1 — App Health Summary Strip

```
╔══════════════╦══════════════╦══════════════╦══════════════╦══════════════╗
║ CRASH RATE   ║ DAU          ║ FCM DELIVERY ║ FORCE UPDATE ║ APP RATING   ║
║  0.24%       ║  1,84,200    ║   96.8%      ║  91.2%       ║  4.3 ⭐      ║
║  ▼ was 0.31% ║  MAU: 8,42K  ║  iOS: 97.2%  ║  iOS: 94.1%  ║  iOS: 4.4   ║
║  ● OK        ║              ║  And: 96.4%  ║  And: 88.3%  ║  And: 4.2   ║
╚══════════════╩══════════════╩══════════════╩══════════════╩══════════════╝
```

| Card | Alert |
|---|---|
| Crash Rate | > 1%: amber · > 3%: red |
| DAU | — (informational) |
| FCM Delivery | < 95%: amber · < 90%: red |
| Force Update Compliance | < 85%: amber (students on old version) |
| App Rating | < 4.0: amber · < 3.5: red |

---

### Section 2 — Crash Rate by Version

**Purpose:** Identify if a specific app version introduced a crash. After a new release, crash rate should be monitored on the new version.

**UI elements:**
```
CRASH RATE BY VERSION                           [Platform: All ▾]
─────────────────────────────────────────────────────────────────────────────
Version        Platform  Users     Crash Rate  Crashes/Day  Status
─────────────────┼──────────┼──────────┼────────────┼─────────────┼──────────
v4.2.1 (latest) Android   82,400    0.24%       197          ✅ OK
v4.2.1 (latest) iOS       64,200    0.18%       116          ✅ OK
v4.2.0          Android   18,100    0.42%       76           🟡 Elevated
v4.1.8          Android    4,200    1.82%       77           🔴 High — [Force Update]
v4.1.8          iOS          800    0.91%       7            🟡 Elevated
```

- Old versions with high crash rate: "Force Update" button (CTO/Mobile Engineer) → triggers immediate force-update for that version + platform combination
- Chart: stacked area, last 14 days, crash rate per version

---

### Section 3 — FCM Delivery Analytics

```
FCM DELIVERY — Last 24 Hours
─────────────────────────────────────────────────────────────────────────────
Notification Type     Sent      Delivered  Delivery%  Avg Latency
──────────────────────┼──────────┼──────────┼───────────┼──────────────
Exam Reminder         48,200    46,520     96.5%       1.2s
Result Published      12,400    12,018     96.9%       0.8s
OTP (app-native)       8,420     8,312     98.7%       0.4s
Announcement           4,200     3,948     94.0%       2.1s ⚠
```

- Delivery% < 95%: amber
- Failed delivery reasons breakdown: pie chart — Token expired / Device offline / App backgrounded / FCM error

---

### Section 4 — Version Adoption Curve

**Purpose:** After a new app release, how quickly do users update? Slow adoption = more users on vulnerable old versions.

**UI elements:**
- Chart.js Stacked Area: X = last 30 days, series = each app version
- Shows how v4.2.1 is replacing v4.2.0 and v4.1.x over time
- Target line: "90% on latest within 14 days of release" — dashed green line

**Version distribution today:**
```
v4.2.1  82.1%  ████████████████████████████████████████  [Latest]
v4.2.0  14.3%  ████████  [Force update in 7 days]
v4.1.8   2.8%  ██        [🔴 Force update active]
v4.1.x   0.8%  ░         [Legacy — cannot receive exams]
```

---

### Section 5 — App Store Ratings Tracker

```
APP STORE RATINGS
─────────────────────────────────────────────────────────────────────────────
             iOS App Store         Google Play Store
Current:         4.4 ⭐                4.2 ⭐
30d change:    ▲ +0.1               ▼ -0.1 ⚠
Total reviews:    2,840               8,420
1-star reviews:   4.8%                7.2%

RECENT 1-STAR REVIEWS (last 7 days)
"App crashes during exam submission on Android 14"  — 2d ago  [Crash confirmed ✓]
"OTP not received on app"  — 3d ago                           [OTP issue ✓]
```

- Recent 1-star reviews: fetched from App Store Connect + Google Play APIs via Celery task
- "Crash confirmed ✓": linked to a crash report in the crash tracker
- CTO can tag review: "Under investigation" / "Fixed in v4.2.2" / "User error"

---

### Section 6 — Force Update Manager

```
FORCE UPDATE CONFIGURATION
─────────────────────────────────────────────────────────────────────────────
Platform   Min Required Version   Current Latest   Users Below Min   Action
───────────┼──────────────────────┼─────────────────┼──────────────────┼──────
iOS        v4.1.9                 v4.2.1            800 (0.5%)        [Update min]
Android    v4.2.0                 v4.2.1            4,200 (2.3%)      [Update min]
```

- "Update min required version" → modal: new minimum version, message to users ("Your app version is no longer supported. Please update to continue."), grace period in hours (0 = immediate)
- POST `/exec/mobile-analytics/actions/set-force-update/` → writes to `AppConfig` model + Redis flag `app:force_update:{platform}:{version}` → app checks this on launch

---

## 5. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  Mobile App Analytics                                 [↺ Refresh]           ║
╠══════════╦══════════╦══════════╦══════════╦══════════════════════════════════╣
║ CRASH    ║ DAU      ║ FCM DEL  ║ FORCE UP ║ APP RATING                      ║
║  0.24%   ║ 1,84,200 ║  96.8%   ║  91.2%   ║  4.3 ⭐                         ║
╠══════════╩══════════╩══════════╩══════════╩══════════════════════════════════╣
║  CRASH RATE BY VERSION            FCM DELIVERY (24h)                       ║
║  v4.2.1 (latest)  0.24% ✅         Exam Reminder: 96.5%                    ║
║  v4.2.0           0.42% 🟡         Result Published: 96.9%                 ║
║  v4.1.8           1.82% 🔴 [Force Update]                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  VERSION ADOPTION CURVE (30d)     APP STORE RATINGS                        ║
║  [Stacked area chart]             iOS: 4.4 ▲  Android: 4.2 ▼ ⚠             ║
║  v4.2.1: 82.1%                    Recent 1-star: "crashes during exam"      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  FORCE UPDATE MANAGER                                                       ║
║  iOS     min: v4.1.9   800 below min   [Update min required version]       ║
║  Android min: v4.2.0  4,200 below min  [Update min required version]       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Component Architecture

| Component | File | Props |
|---|---|---|
| `AppHealthCard` | `components/mobile/health_card.html` | `label, value, ios_value, android_value, alert_level` |
| `CrashVersionRow` | `components/mobile/crash_row.html` | `version, platform, users, crash_rate, crashes_per_day, can_force_update` |
| `FCMDeliveryRow` | `components/mobile/fcm_row.html` | `notif_type, sent, delivered, delivery_pct, avg_latency_s` |
| `VersionAdoptionChart` | `components/mobile/adoption_chart.html` | `days (list of {date, version_distribution})` |
| `RatingCard` | `components/mobile/rating_card.html` | `platform, rating, delta_30d, total_reviews, one_star_pct` |
| `ForceUpdateRow` | `components/mobile/force_update_row.html` | `platform, min_version, latest_version, users_below_min, can_act` |

---

## 7. HTMX Architecture

| `?part=` | Target | Poll | Trigger |
|---|---|---|---|
| `summary` | `#app-summary` | 300s | load |
| `crash-versions` | `#crash-versions` | 300s | load + platform filter |
| `fcm` | `#fcm-delivery` | 300s | load |
| `adoption` | `#version-adoption` | None | load |
| `ratings` | `#app-ratings` | None | load |
| `force-update` | `#force-update` | None | load |

---

## 8. Backend View & API

```python
class MobileAnalyticsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_mobile_analytics"

    def get(self, request):
        allowed = {"cto","mobile_engineer","ceo","superadmin"}
        if request.user.role not in allowed:
            return redirect("exec:dashboard")
        can_act = request.user.role in {"cto","mobile_engineer","superadmin"}
        if _is_htmx(request):
            part = request.GET.get("part","")
            ctx = {"can_act": can_act}
            dispatch = {
                "summary":       "exec/mobile/partials/summary.html",
                "crash-versions":"exec/mobile/partials/crash_versions.html",
                "fcm":           "exec/mobile/partials/fcm.html",
                "adoption":      "exec/mobile/partials/adoption.html",
                "ratings":       "exec/mobile/partials/ratings.html",
                "force-update":  "exec/mobile/partials/force_update.html",
            }
            if part in dispatch:
                return render(request, dispatch[part], ctx)
        return render(request, "exec/mobile_analytics.html", {"can_act": can_act})
```

**Action endpoints:**

| Method | URL | Permission | Action |
|---|---|---|---|
| POST | `/exec/mobile-analytics/actions/set-force-update/` | `portal.manage_app_config` (CTO/Mobile Eng) | Update `AppConfig.min_version`, write Redis key, audit log |

---

## 9. Database Schema

```python
class AppVersionMetrics(models.Model):
    """Daily snapshot per version + platform from Firebase/Crashlytics."""
    date            = models.DateField(db_index=True)
    version         = models.CharField(max_length=20)
    platform        = models.CharField(max_length=10, choices=[("ios","iOS"),("android","Android")])
    active_users    = models.IntegerField()
    crash_count     = models.IntegerField()
    crash_rate      = models.FloatField()
    fcm_sent        = models.IntegerField(default=0)
    fcm_delivered   = models.IntegerField(default=0)

    class Meta:
        unique_together = ("date","version","platform")


class AppStoreReview(models.Model):
    platform        = models.CharField(max_length=10)
    rating          = models.IntegerField()  # 1–5
    body            = models.TextField()
    author          = models.CharField(max_length=100, blank=True)
    review_date     = models.DateField()
    version         = models.CharField(max_length=20)
    tagged_issue    = models.CharField(max_length=50, blank=True)
    fetched_at      = models.DateTimeField(auto_now_add=True)


class AppConfig(models.Model):
    platform        = models.CharField(max_length=10, unique=True)
    min_required_version = models.CharField(max_length=20)
    latest_version  = models.CharField(max_length=20)
    force_update_message = models.TextField()
    grace_period_hours = models.IntegerField(default=0)
    updated_by      = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                         on_delete=models.SET_NULL)
    updated_at      = models.DateTimeField(auto_now=True)
```

---

## 10. Validation Rules

| Action | Validation |
|---|---|
| Set Force Update | New min version must be ≤ latest version. Cannot downgrade min version (must be ≥ current min). Message required (max 200 chars). Grace period 0–72 hours. |

---

## 11. Security Considerations

- Force update affects all users on that platform — logged as a `SecurityAuditLog` entry (it is a security action when applied to old vulnerable versions)
- App Store credentials (App Store Connect API, Google Play API): in AWS Secrets Manager
- Crash reports may contain stack traces with internal paths — only CTO/Mobile Engineer can view

---

## 12. Edge Cases

| State | Behaviour |
|---|---|
| Crash rate spikes > 3% on new version | Auto-creates P1 incident. CTO email notification. Suggestion shown: "Consider force-update to previous stable version." |
| FCM delivery drops during exam | Triggers same alert path as War Room OTP card. Exam Ops Manager notified. |
| App Store API rate limit | Reviews sync fails silently. Page shows "Reviews last synced X hours ago" if > 6h stale. |
| Force update with 0 grace period during exam | Warning shown: "⚠ {N} students are currently in a live exam on this version. Applying force update will interrupt them. Are you sure?" Requires CTO to type confirmation. |

---

## 13. Performance & Scaling

- All metrics sourced from Firebase/Crashlytics webhooks → `AppVersionMetrics` model (no live Firebase API calls from this page)
- App store reviews: synced daily at 06:00 IST via Celery beat (App Store Connect API + Google Play API)
- Adoption chart: 30 days × 5 versions × 2 platforms = 300 data points — trivial
- Redis TTL 290s for all live metrics — acceptable for operational monitoring

---

*Last updated: 2026-03-20*
