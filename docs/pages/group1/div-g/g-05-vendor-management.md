# G-05 — Vendor Management

> **Route:** `/bgv/vendors/`
> **Division:** G — Background Verification
> **Primary Role:** BGV Manager (39) — full control over vendor setup and configuration
> **Supporting Roles:** BGV Ops Supervisor (92) — read-only; Platform Admin (10) — full
> **File:** `g-05-vendor-management.md`
> **Priority:** P1 — must be configured before BGV operations begin

---

## 1. Page Name & Route

**Page Name:** Vendor Management
**Route:** `/bgv/vendors/`
**Part-load routes:**
- `/bgv/vendors/?part=vendor-list` — vendor list
- `/bgv/vendors/{vendor_id}/?part=detail` — vendor detail drawer
- `/bgv/vendors/{vendor_id}/?part=performance` — performance chart

---

## 2. Purpose

G-05 manages all BGV verification vendors (e.g. AuthBridge, IDfy, SpringVerify). The BGV Manager configures API credentials, sets SLA expectations, monitors vendor health and performance, and controls which vendor is active for submissions.

**Who needs this page:**
- BGV Manager (39) — vendor onboarding, API configuration, performance review, SLA management
- BGV Ops Supervisor (92) — check vendor health before batch submissions; read-only

**When is it used:**
- Initial platform setup (configure first vendor)
- When adding a new vendor (contract signed, API credentials received)
- When a vendor goes DOWN — switch active vendor
- Monthly performance review

---

## 3. Layout

```
┌──────────────────────────────────────────────────────────────┐
│  Page header: "Vendor Management"    [+ Add Vendor]          │
├──────────────────────────────────────────────────────────────┤
│  Vendor Health Banner (if any vendor DOWN or DEGRADED)       │
├──────────────────────────────────────────────────────────────┤
│  Vendor Cards Grid (one card per vendor)                     │
│  ┌───────────────┐  ┌───────────────┐  ┌────────────────┐  │
│  │ VendorName    │  │ VendorName2   │  │ + Add Vendor   │  │
│  │ ACTIVE ✅     │  │ INACTIVE      │  │                │  │
│  │ SLA: 72h      │  │ SLA: 48h      │  │                │  │
│  │ Health: OK    │  │ Health: —     │  │                │  │
│  │ [Manage →]    │  │ [Manage →]    │  │                │  │
│  └───────────────┘  └───────────────┘  └────────────────┘  │
├──────────────────────────────────────────────────────────────┤
│  Vendor Detail Drawer (opens on [Manage →])                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Vendor Health Banner

Shown when any `bgv_vendor.health_status IN (DEGRADED, DOWN)`.

- **DOWN:** `🔴 {vendor_name} is DOWN — currently {N} verifications assigned to this vendor. [Reassign to Another Vendor]`
- **DEGRADED:** `⚠️ {vendor_name} is reporting degraded performance — responses may be delayed.`

[Reassign to Another Vendor] — triggers bulk reassignment modal: select target vendor; re-submits all VENDOR_SENT verifications assigned to the DOWN vendor. Requires BGV Manager (39) confirmation: "Reassign {N} active verifications from {old_vendor} to {new_vendor}? This will re-submit to new vendor API."

---

### Section B — Vendor Cards

One card per `bgv_vendor` record.

**Card content:**
- Vendor name + code badge
- Status pill: ACTIVE (green) / INACTIVE (grey) / SUSPENDED (red)
- Health status: ✅ HEALTHY / ⚠️ DEGRADED / ❌ DOWN / — UNKNOWN
- SLA: `{sla_hours}h turnaround`
- Supported checks: icon list (Criminal, Address, Employment, Education, POCSO Registry)
- Last health check: "{N} min ago" or "—"
- Active verifications: count of VENDOR_SENT verifications with this vendor
- [Manage →] — opens detail drawer

Card border colour: green (ACTIVE + HEALTHY), amber (ACTIVE + DEGRADED), red (DOWN), grey (INACTIVE).

---

### Section C — Vendor Detail Drawer

Tabbed drawer (600px) for full vendor management.

**Tabs: Details | API Configuration | Performance | Transactions**

#### Details Tab

Editable vendor profile (BGV Manager only).

| Field | Control | Notes |
|---|---|---|
| Vendor Name | Text | — |
| Code | Text (max 10 chars, uppercase) | Immutable after creation |
| Status | Select: ACTIVE / INACTIVE / SUSPENDED | Changing from ACTIVE to INACTIVE when verifications are assigned: warning modal required (see edge cases) |
| SLA (hours) | Number input | Contractual turnaround commitment |
| Supported Checks | Multi-select checkboxes | CRIMINAL · ADDRESS · EMPLOYMENT · EDUCATION · POCSO_REGISTRY · COURT_RECORD |
| Contact Name | Text | Vendor account manager |
| Contact Email | Email input | — |
| Contact Phone | Text | — |
| Notes | Textarea | Internal notes (contract terms, known limitations, escalation path) |

**[Save Details]** ✅ "Vendor details updated" toast 3s.

**Danger Zone (BGV Manager only):**
- [Suspend Vendor] — marks SUSPENDED; no new submissions allowed; existing verifications shown as needing reassignment
- [Delete Vendor] — only if zero active or historical verifications linked. Otherwise blocked: "Cannot delete vendor with {N} verification records."

#### API Configuration Tab

Sensitive fields — masked by default. BGV Manager (39) only.

| Field | Control | Notes |
|---|---|---|
| API Base URL | URL input | e.g. `https://api.authbridge.com/v2` |
| API Key | Password input (masked) | Stored AES-256 encrypted. [Show] button reveals for 10s then re-masks. [Regenerate] for new key. |
| Webhook Endpoint (inbound) | Read-only | Platform's webhook URL for this vendor: `https://api.eduforge.com/bgv/webhook/{vendor_code}/` |
| Webhook Secret | Password input (masked) | HMAC secret — used to verify webhook signature |
| Authentication Type | Select: API_KEY_HEADER · BEARER_TOKEN · BASIC_AUTH | — |
| Header Name | Text | e.g. `X-API-Key` (for API_KEY_HEADER type) |
| Timeout (seconds) | Number input | API call timeout; default 30s; max 120s |

**[Test API Connection]:**
- Sends `GET {api_base_url}/health` or equivalent ping
- Result shown inline: ✅ "Connected — {response_time}ms" or ❌ "Connection failed: {error}"
- Updates `last_health_check_at` and `health_status`

**[Send Test Verification Request]:**
- Submits a test/dummy verification payload to vendor sandbox endpoint
- Shows request payload (redacted) + response
- Confirms webhook receipt if vendor supports test webhooks
- Test transactions NOT stored in `bgv_vendor_transaction` — they are flagged `is_test = true` and stored separately

**[Save API Config]** — confirmation modal: "Updating API configuration will affect all future vendor submissions. Confirm?" ✅ "API configuration saved" toast.

**Warning:** "API credentials are encrypted at rest. Never share these credentials outside the BGV team. If you suspect a key has been compromised, [Rotate API Key] immediately and notify the vendor."

#### API Key Rotation Workflow

**[Rotate API Key]** — shown below API Key field. BGV Manager (39) and Platform Admin (10) only.

Used when: (a) vendor proactively rotates key on schedule, (b) key is suspected compromised, (c) BGV Manager is offboarding.

**Rotation modal:**
1. "Enter new API key from vendor:" — password input (masked)
2. "Confirm new API key:" — repeat field
3. "Reason:" — text (required: SCHEDULED_ROTATION / COMPROMISE_SUSPECTED / STAFF_CHANGE / OTHER)
4. [Test New Key] — mandatory before save. Sends health ping with new key. Must show ✅ before [Confirm Rotation] is enabled.
5. [Confirm Rotation] — atomically replaces encrypted key; old key is NOT retained. Logs: `VENDOR_API_KEY_ROTATED` in `bgv_audit_log`.

**During rotation (after [Confirm Rotation]):**
- In-flight VENDOR_SENT verifications are unaffected — they use the vendor's tracking ref, not the API key, for status polling.
- BGV Manager should notify DevOps (Div C) if webhook secret is also being rotated (requires server-side webhook endpoint secret update).

**Compromised key protocol:**
- Select reason: COMPROMISE_SUSPECTED
- After rotation, page shows: "Previous key may still be active at vendor side for up to 10 minutes. All new submissions use the rotated key. If vendor confirms old key is still active, contact vendor support immediately."
- BGV Manager should also notify Security Engineer (16) via out-of-band channel.

#### Vendor Result Schema

Different vendors return results in different formats. G-05 documents the normalized schema EduForge expects vendors to map to:

| Normalized Field | Expected Values | Notes |
|---|---|---|
| `result` | `CLEAR` · `FLAGGED` · `INCONCLUSIVE` | Required |
| `offense_found` | boolean | Required when result = FLAGGED |
| `offense_type` | string | Required when offense_found = true |
| `offense_date` | ISO 8601 date or null | Optional |
| `pocso_flag` | boolean | Required — must explicitly state true/false |
| `criminal_record_found` | boolean | For CRIMINAL check |
| `address_verified` | boolean | For ADDRESS check |
| `employment_verified` | boolean | For EMPLOYMENT check |
| `confidence_score` | float 0–1 | Optional — vendor's confidence in result |
| `report_url` | string (URL) | Optional — link to vendor's PDF report |

**Vendor onboarding responsibility:** BGV Manager must confirm with vendor how their fields map to this schema. Document field mapping in vendor Notes field (Details Tab). Any vendor not supporting `pocso_flag` field must be manually reviewed by BGV Executive before CLEAR result is accepted.

#### Performance Tab

Vendor performance metrics and trends.

**Summary stats (current month):**
| Metric | Value |
|---|---|
| Total submissions | Count of `bgv_vendor_transaction` with direction = OUTBOUND |
| Results received | Count with `vendor_returned_at IS NOT NULL` |
| Avg turnaround | `avg(vendor_returned_at - vendor_sent_at)` in hours |
| SLA compliance % | % where turnaround ≤ `sla_hours` |
| CLEAR rate | `CLEAR / (CLEAR + FLAGGED + INCONCLUSIVE)` |
| FLAGGED rate | — |
| Error rate | `vendor_result = ERROR / total` |

**Turnaround trend chart:**
- Bar chart: avg turnaround per month (last 12 months)
- Dashed line: contracted SLA hours
- Hover tooltip: exact avg + SLA vs actual

**SLA breach log:**
Table of verifications where turnaround exceeded `sla_hours`. Columns: Staff Ref, Institution, Sent, Returned, Hours Over SLA.

**Month filter:** dropdown to view any past 12 months.

#### Transactions Tab

Recent API call log for this vendor.

| Column | Notes |
|---|---|
| Timestamp | Datetime |
| Direction | OUTBOUND / INBOUND |
| Verification | Staff ref (linked to G-03) |
| Endpoint | API endpoint called |
| Status Code | HTTP status |
| Result | Success / Error |
| Duration | ms |
| Error | Error message if failed |

Pagination: 25 rows. Filter: Direction, Status, Date Range.

[Export Transactions CSV] — BGV Manager only.

---

### Section D — Add Vendor Modal

Triggered by [+ Add Vendor] card or button.

**Step 1 — Vendor Profile:**
- Vendor Name, Code (auto-generated from name, editable), Contact details, SLA hours, Supported checks, Notes

**Step 2 — API Configuration:**
- API Base URL, API Key, Webhook Secret, Auth Type, Timeout

**Step 3 — Test Connection:**
- [Run API Test] — required before proceeding. Must show ✅ before [Finish & Activate] is enabled.
- Status defaults to INACTIVE until test passes. BGV Manager can then manually set to ACTIVE.

**[Finish & Activate]:** Creates vendor record with status ACTIVE (if test passed and Manager confirms). ✅ "Vendor {name} added and activated" toast.

---

## 5. Celery Task — Vendor Health Check

`check_bgv_vendor_health` — runs every 30 minutes.

- Pings each ACTIVE vendor's health endpoint
- Updates `health_status` and `last_health_check_at`
- If HEALTHY → DOWN: notifies BGV Manager (39) and Supervisor (92) in-app: "⚠️ {vendor_name} is DOWN. {N} active verifications affected."
- If DEGRADED for > 2 hours: notifies BGV Manager
- Shown in G-05 vendor cards and G-02 vendor submission modal

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | BGV Manager (39), BGV Ops Supervisor (92), Platform Admin (10) |
| BGV Executive (40) | No access — API credentials are above executive scope |
| POCSO Compliance Officer (41) | No access |
| Edit vendor details | BGV Manager (39), Platform Admin (10) |
| View API Configuration tab | BGV Manager (39), Platform Admin (10) |
| [Test API Connection] | BGV Manager (39), Platform Admin (10) |
| [Suspend / Delete Vendor] | BGV Manager (39), Platform Admin (10) |
| [Reassign to Another Vendor] | BGV Manager (39), Platform Admin (10) |
| BGV Ops Supervisor (92) | Read-only: vendor cards, Details tab, Performance tab, Transactions tab. Cannot see API Configuration tab. |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Deactivating ACTIVE vendor with assigned verifications | Modal warning: "This vendor has {N} active verifications in VENDOR_SENT state. Deactivating will not automatically reassign them. Manually reassign via G-02 queue or use [Reassign to Another Vendor]. Confirm deactivation?" |
| No ACTIVE vendor configured | Banner on G-02 queue: "No active vendor configured. BGV submissions are paused. [Configure Vendor →]" |
| All vendors DOWN simultaneously | G-01 dashboard: full-width red banner. G-02: submission blocked with "All vendors currently unavailable." BGV Manager notified. Manual workaround: contact vendor directly; use [Manual Vendor Result Entry] in G-03 when result received. |
| API key changed by vendor (old key fails) | Health check shows DOWN. Manager gets alert. [Test API Connection] in G-05 → fails → Manager updates API key. |
| Vendor code collision | Code must be unique. Inline validation: "Code '{code}' is already in use." |
| Webhook signature verification fails | Transaction logged with `error = "HMAC_VERIFICATION_FAILED"`. Not processed. BGV Manager notified. Common cause: webhook secret mismatch after vendor rotation. |

---

## 8. UI Patterns

### Loading States
- Vendor cards: skeleton 3 cards
- Drawer: tab skeleton + content shimmer

### Toasts
| Action | Toast |
|---|---|
| API test successful | ✅ "Connected to {vendor_name} in {N}ms" (4s) |
| API test failed | ❌ "Connection failed — check API URL and credentials" (6s) |
| Vendor activated | ✅ "Vendor {name} is now ACTIVE" (4s) |
| Vendor suspended | ⚠️ "Vendor suspended — new submissions blocked" (4s) |
| Reassignment complete | ✅ "{N} verifications reassigned to {new_vendor}" (4s) |

---

*Page spec complete.*
*G-05 covers: vendor health banner → vendor cards grid (status + health) → detail drawer (Details / API Config / Performance / Transactions) → masked API credential management with show/hide → test connection flow → turnaround trend chart → SLA compliance metrics → add vendor 3-step wizard → Celery health check every 30 minutes → bulk reassignment on vendor DOWN.*
