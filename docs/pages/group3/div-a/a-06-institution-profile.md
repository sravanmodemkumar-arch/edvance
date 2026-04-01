# A-06 — Institution Profile & Settings

> **URL:** `/school/admin/profile/`
> **File:** `a-06-institution-profile.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Principal (S6) — full · VP Admin (S5) — view + edit non-critical · Promoter (S7) — view · Admin Officer (S3) — view

---

## 1. Purpose

The single source of truth for the institution's identity, configuration, and contact information. Every other module reads from this profile: circulars pull the school letterhead, CBSE reports pull the affiliation number, student certificates pull the logo, fee receipts pull the address. Getting this right at onboarding is critical — wrong information here propagates to every document the school produces.

---

## 2. Page Layout

### 2.1 Page Header
```
Institution Profile & Settings                          [Edit Profile]  [Preview Letterhead]
Last updated: 22 Mar 2026 by Principal [Name]
```

### 2.2 Tab Bar
```
[Basic Info] [Board & Affiliation] [Academic Structure] [Contact & Address] [Branding & Documents] [System Settings]
```

---

## 3. Tab: Basic Info

| Field | Value | Editable By |
|---|---|---|
| School Full Name (English) | Sri Vivekananda High School | Principal |
| School Short Name / Display Name | SVHS | Principal |
| School Registration No | TS/SOC/12345/2003 | Principal (approval required) |
| Type | Secondary + Senior Secondary | Principal |
| Medium(s) of Instruction | English · Telugu | Principal |
| Year of Establishment | 1998 | Principal (approval required) |
| Management Type | Private Unaided · Society-managed | Principal (approval required) |
| Total Sanctioned Strength (students) | 1,200 | Principal |
| Hostel Facility | Yes — Boys · Girls · Co-ed (specify) | Principal |
| Transport Facility | Yes — Own Buses · Hired Buses | Principal |
| Canteen / Cafeteria | Yes | Principal |

---

## 4. Tab: Board & Affiliation

Displays current board affiliations. Schools can be affiliated to multiple boards (e.g., CBSE for IX–XII + State Board for I–VIII in some states).

| Field | Value |
|---|---|
| Primary Board | CBSE |
| Affiliation No | 1234567 |
| Affiliation Type | Senior Secondary (I–XII) |
| Affiliation Region | Hyderabad Region |
| Affiliation Valid Until | 31 Mar 2027 |
| CBSE School No | 41234 |
| State Board Secondary | Telangana State Board (Class IX–X parallel) |
| State Board Affiliation No | TS-SEC-56789 |

**Affiliation Renewal Tracker:**
- Shows days remaining to renewal deadline
- Documents required checklist with upload status
- [Upload Document] per item
- [Submit Renewal Application] button → generates application bundle PDF + queues to Principal for sign-off
- Document types: NOC from Society · Fire NOC (Municipal) · Building Completion Certificate · Teacher qualification register · Infrastructure compliance certificate

**UDISE+ Code:**
- UDISE+ Code field (mandatory — all Indian schools must have a UDISE code for government data reporting)
- Link to UDISE+ portal for code verification

---

## 5. Tab: Academic Structure

**Class Configuration (read-only on this page; edit via A-08 Class Manager):**
| Level | Classes | No. of Classes |
|---|---|---|
| Pre-Primary | LKG · UKG | 2 classes, 3 sections each |
| Primary | I to V | 5 classes, 4 sections each |
| Upper Primary | VI to VIII | 3 classes, 4 sections each |
| Secondary | IX to X | 2 classes, 5 sections each |
| Senior Secondary | XI to XII | 2 classes — Science/Commerce/Arts |

**Academic Year Configuration:**
- Academic year: April 1 – March 31 (default)
- First working day: 1 Apr 2025
- Last working day: 31 Mar 2026
- [Override dates] for boards with different calendars (Tamil Nadu: June start)

**Working Days Configuration:**
- Working days per week: Mon–Fri (Sat optional)
- School hours: 8:30 AM – 3:30 PM (configurable per level: Primary/Secondary)
- Total school hours per year: computed automatically

---

## 6. Tab: Contact & Address

| Field | Value |
|---|---|
| Full Address (English) | Plot No 45, Sector 12, Madhapur, Hyderabad — 500081 |
| City | Hyderabad |
| District | Rangareddy |
| State | Telangana |
| PIN Code | 500081 |
| Main Phone | 040-29876543 |
| Secondary Phone | +91-9876543210 |
| Principal's Direct Email | principal@svhs.edu.in |
| School Official Email | info@svhs.edu.in |
| Website | www.svhs.edu.in |
| Google Maps Link | [Verified location] |
| Emergency Contact | +91-9876543211 (VP Admin) |

---

## 7. Tab: Branding & Documents

**Logo & Identity:**
- School Logo (PNG/SVG, min 300×300px): upload + preview
- Logo used on: fee receipts, hall tickets, report cards, circulars, letterhead
- Tagline / Motto: "Knowledge is Power"
- School Seal / Stamp (scanned image): upload (used on TC, migration certificate)

**Letterhead Preview:**
- Live preview of how the school letterhead looks with current logo + name + address + affiliation
- [Print Test Letterhead] button

**Key Documents Repository:**
- Society/Trust Registration Certificate
- PAN Card (Society)
- CBSE/Board Affiliation Certificate
- Fire NOC
- Building Completion Certificate
- Audited Accounts (last 3 years)
- NAAC/Quality Certification (if any)
- Each document: upload · expiry date · [Download] · status badge (VALID / EXPIRING SOON / EXPIRED)

---

## 8. Tab: System Settings

**Communication Settings:**
- Default notification channel: WhatsApp (primary) · SMS (fallback)
- WhatsApp Business number linked: +91-XXXXXXXXXX
- SMS sender ID: SVHYDS (6-char DLT registered sender ID)
- Email From Name: "SVHS School Office"

**Time Zone:** Asia/Kolkata (IST +05:30) — non-editable; set at platform level

**Language / Locale:**
- Number format: Indian (1,00,000 format) — default
- Date format: DD-MM-YYYY — default

**Role & Access Settings:**
- Enable/disable specific modules: e.g., "Hostel module enabled: Yes"
- Two-factor authentication requirement: Principal role — mandatory · VP — optional · Others — off
- Session timeout: configurable per role (default: Principal 4h, VP 3h, Teacher 2h, Staff 1h)

**Integration Settings** (Platform Admin-managed, read-only for school staff):
- Payment gateway: Razorpay / PhonePe / PayU (as configured)
- WhatsApp gateway: (Platform-managed)
- SMS gateway: (Platform-managed)

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/profile/` | Full profile data |
| 2 | `PATCH` | `/api/v1/school/{id}/profile/basic/` | Update basic info |
| 3 | `PATCH` | `/api/v1/school/{id}/profile/contact/` | Update contact/address |
| 4 | `PATCH` | `/api/v1/school/{id}/profile/branding/` | Update logo/tagline |
| 5 | `GET` | `/api/v1/school/{id}/profile/affiliation/` | Affiliation details + renewal status |
| 6 | `POST` | `/api/v1/school/{id}/profile/affiliation/documents/` | Upload affiliation document |
| 7 | `GET` | `/api/v1/school/{id}/profile/letterhead-preview/` | Generated letterhead PNG |
| 8 | `GET` | `/api/v1/school/{id}/profile/documents/` | Key documents list |
| 9 | `POST` | `/api/v1/school/{id}/profile/documents/` | Upload key document |
| 10 | `PATCH` | `/api/v1/school/{id}/profile/settings/` | Update system settings |

---

## 10. HTMX Patterns

### Tab Navigation
```html
<button hx-get="/school/admin/profile/tab/basic/"
        hx-target="#profile-tab-content"
        hx-push-url="?tab=basic">Basic Info</button>
```

### Inline Document Upload
```html
<form hx-post="/api/v1/school/{{ school_id }}/profile/documents/"
      hx-target="#document-row-{{ doc_type }}"
      hx-swap="outerHTML"
      hx-encoding="multipart/form-data">
  <input type="hidden" name="doc_type" value="fire_noc">
  <input type="file" name="file" accept=".pdf,.jpg,.png">
  <input type="date" name="expiry_date">
  <button type="submit">Upload</button>
</form>
```

### Affiliation Renewal Days-Remaining Countdown
```html
<div id="affiliation-countdown"
     hx-get="/api/v1/school/{{ school_id }}/profile/affiliation/"
     hx-trigger="every 1h"
     hx-target="#affiliation-countdown"
     hx-swap="outerHTML">
  <!-- "Affiliation expires in X days" badge -->
</div>
```

---

## 11. Business Rules

- School name, registration number, and management type changes require Platform Admin countersign (these are affiliation-linked fields)
- Logo changes: Principal approves; new logo propagates to all documents from next generation
- UDISE+ code is validated against the UDISE database pattern (State code + District code + 11-digit serial)
- Documents with expired validity trigger compliance alerts in A-29
- Session settings changes take effect on next login (existing sessions unaffected)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
