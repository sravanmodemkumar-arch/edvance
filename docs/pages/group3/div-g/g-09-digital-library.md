# G-09 — Digital Library

> **URL:** `/school/library/digital/`
> **File:** `g-09-digital-library.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Librarian (S3) — manage resources · Academic Coordinator (S4) — approve access · All Students and Staff — access via portal

---

## 1. Purpose

Aggregates and manages access to digital library resources — e-books, educational videos, digital encyclopaedias, and government education portals. NEP 2020 mandates digital library integration in schools; EduForge provides a curated access hub rather than a standalone digital library platform.

Key resources for Indian schools:
- **DIKSHA (National Platform):** NCERT content, textbooks, worksheets, QR-linked material; government-mandated for all CBSE schools
- **e-Pathshala:** NCERT e-books (free access)
- **National Digital Library of India (NDLI):** 90M+ educational resources; free for registered users
- **Spoken Tutorial IIT Bombay:** Free programming/software tutorials for Class IX–XII
- **INFLIBNET Shodhganga:** Research theses (relevant for senior teachers and Class XII projects)
- **School-purchased e-books:** Schools can buy licenses for specific digital books

---

## 2. Page Layout

### 2.1 Header
```
Digital Library                                      [+ Add Resource]  [Access Logs]
Resources: 42 active links  ·  Categories: 8
DIKSHA Integration: ✅ Connected  ·  NDLI Registration: ✅ Active
Student access this month: 284 sessions
```

### 2.2 Resource Catalogue
```
Category         Resources  Students Accessed  Description
DIKSHA           15 links   142 this month     NCERT content, QR codes, textbooks
e-Pathshala       8 links    98 this month     NCERT e-books (free)
NDLI              2 links    22 this month     National digital library portal
Spoken Tutorial   5 links    34 this month     Free programming tutorials (IIT Bombay)
School e-Books   10 titles   28 this month     Licensed e-books (Oxford, Macmillan)
YouTube (curated) 2 playlists 40 this month   Verified educational YouTube channels
Government Portals 3 links    12 this month   CBSE, Samagra Shiksha, e-Prashikshan
```

---

## 3. Add Resource

```
[+ Add Resource]

Resource Type:
  ● External Link (government portal, free resource)
  ○ Purchased e-Book (with license key/access code)
  ○ School-created PDF (uploaded to R2 storage)
  ○ YouTube playlist (curated)

Title: [NCERT Physics Part I — Class XI                    ]
URL: [https://epathshala.nic.in/...]
Category: [DIKSHA / e-Pathshala ▼]
Subject: [Physics ▼]  Class Level: [XI ▼]
Description: [NCERT e-book for Class XI Physics Part 1 — free access via e-Pathshala]

Access: ● All students and staff  ○ Specific classes  ○ Staff only
License: ● Free (no license needed)  ○ Licensed (school account)

[Add Resource]
```

---

## 4. DIKSHA Integration

```
DIKSHA (National Platform) — Integration Status

School DIKSHA Code: AP12345678
Status: ✅ Connected — Content synced

DIKSHA books linked to this school (CBSE-AP):
  Class I–XII NCERT textbooks: 88 books (QR-linked)
  Lesson worksheets: 240
  Video lessons: 1,840 (CBSE Teacher Training + NCERT)
  Assessment items: 3,200

QR Code Usage:
  Students can scan QR codes printed in NCERT textbooks → opens DIKSHA content
  This integration allows tracking of QR scans from school devices.

Student usage this month: 142 unique students, 1,840 page views
Most accessed: Class X Maths (320 views), Class XII Physics (280 views)

[View DIKSHA Reports]  [Update School Profile on DIKSHA]
```

---

## 5. School e-Book Licenses

```
Licensed e-Books

Title                  Publisher    License Type  Seats  Used   Expiry
Oxford English Grammar  Oxford       Annual school  50    34/50  31 Mar 2027
Macmillan Science XI   Macmillan    Annual school  30    18/30  31 Mar 2027

License management:
  → Students access via unique login (school provides credentials)
  → Concurrent seat limit enforced by publisher
  → Usage tracked per seat
  → Renewal reminder sent 30 days before expiry

[Renew License]  [Add Seats]  [View Usage]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/digital/` | Digital resource list |
| 2 | `POST` | `/api/v1/school/{id}/library/digital/` | Add resource |
| 3 | `GET` | `/api/v1/school/{id}/library/digital/access-logs/?month={m}` | Usage logs |
| 4 | `GET` | `/api/v1/school/{id}/library/digital/diksha/stats/` | DIKSHA usage stats |
| 5 | `GET` | `/api/v1/school/{id}/library/digital/licenses/` | License management |

---

## 7. Business Rules

- DIKSHA integration is mandatory for all CBSE-affiliated schools under NEP 2020/CBSE digital initiative; the school's DIKSHA registration code is stored in the school profile (from C-17 UDISE)
- Free government resources (DIKSHA, e-Pathshala, NDLI) are added without approval; purchased licenses require Academic Coordinator approval and D-19 vendor payment
- Student access to external URLs is via the school's digital library portal — EduForge serves as a curated link hub; the actual content is on external platforms and EduForge does not host it
- Digital resource access logs (URL + student + timestamp) are retained for 1 year for reporting; longer retention for licensed content (to prove license utilisation)
- YouTube links are reviewed by the Academic Coordinator before adding (to ensure content is age-appropriate and curriculum-aligned); general YouTube is not accessible through this portal

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
