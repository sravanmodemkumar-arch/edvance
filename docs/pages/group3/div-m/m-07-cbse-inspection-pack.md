# M-07 — CBSE Inspection Package Generator

> **URL:** `/school/mis/cbse-pack/`
> **File:** `m-07-cbse-inspection-pack.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — generate and download package · Compliance Officer (S4) — prepare and review · MIS Coordinator (S4) — generate on Principal instruction

---

## 1. Purpose

CBSE inspections can be announced (scheduled 2–4 weeks in advance) or unannounced (surprise inspection by CBSE Regional Officer or state-level inspection team). In either case, the school must produce a comprehensive set of documents and registers on demand.

This module generates a complete, ready-to-present inspection package — a ZIP archive or printable PDF set — containing all CBSE-required documents, registers, reports, and verification data. What historically took 2–3 days of scrambling is reduced to a 20-minute generation and review.

---

## 2. CBSE Inspection Checklist

```
CBSE INSPECTION PACKAGE — GREENFIELDS SCHOOL
Generation date: 27 March 2026
Readiness: 87/100

SECTION A: SCHOOL PROFILE
  ✅ Affiliation certificate (K-06)
  ✅ School registration / trust deed (K-06)
  ✅ Land documents (K-06)
  ✅ Building plan and completion certificate (K-04)
  ✅ Fire NOC (K-03) — valid until Sep 2026
  ✅ Water supply certificate (K-04)
  ⚠ Structural stability certificate — annual (last: Jan 2025; next: Jan 2026 — OVERDUE 2 months)

SECTION B: ACADEMIC RECORDS
  ✅ Academic calendar 2025–26 (K-11)
  ✅ Timetable — Master and teacher-wise (L-12)
  ✅ Curriculum compliance statement (CBSE Affiliation Bye-Laws)
  ✅ Class-wise enrolment register (A-series)
  ✅ Attendance registers (Class-wise, last 3 years) (E-01)
  ✅ Board examination results (2023, 2024, 2025) (M-02)
  ✅ Assessment records — Unit test, half-yearly, annual (B-series)

SECTION C: STAFF RECORDS
  ✅ Staff register (L-14 — CBSE format)
  ✅ Qualification certificates — all teachers (K-06)
  ✅ TET/CTET certificates (K-02)
  ⚠ Service books — 87 staff (L-11) — 3 books pending annual Principal certification
  ✅ Staff attendance register (L-02)
  ✅ Training records — CBSE i-EXCEL, POCSO (L-07)
  ✅ Salary register (L-04)

SECTION D: INFRASTRUCTURE
  ✅ Lab register (science labs, computer lab) (K-07)
  ✅ Library register (book inventory, member register) (K-07)
  ✅ Sports equipment register (K-07)
  ✅ Fire drill records (2 drills this year) (K-03)
  ⚠ First aid register — minor updates needed (K-07)

SECTION E: COMPLIANCE
  ✅ POCSO register (J-02) — 0 cases this year
  ✅ Anti-ragging register (J-03) — 0 cases this year
  ✅ Grievance register (J-05)
  ✅ Student welfare committee records (J-series)
  ✅ Parent-Teacher Committee / SMC records (RTE K-02)
  ✅ BGV register — 124/127 staff (K-05)

SECTION F: FINANCIAL
  ✅ Fee structure (D-02) — approved by Principal
  ✅ Fee receipt register (D-01)
  ✅ Accounts — audited statements (last 3 years)
  ✅ 12A/80G exemption certificate

ISSUES TO RESOLVE BEFORE GENERATION:
  🔴 Structural certificate (Section A): Overdue — initiate renewal immediately
  🟡 Service books (Section C): 3 principal certifications pending — complete today
  🟡 First aid register (Section D): Minor updates needed
```

---

## 3. Package Generation

```
GENERATE CBSE INSPECTION PACKAGE

When generated, this package contains:
  ● Cover page with school details, affiliation number, inspection date
  ● Table of contents with clickable links
  ● Section A–F documents (PDFs pulled from K-06, B-series, L-series, J-series, D-series)
  ● All statutory registers in printable format (K-07)
  ● Staff register in CBSE Schedule V format (L-14)
  ● Board results last 3 years (M-02)
  ● Compliance score card (M-04)
  ● Inspection readiness self-assessment (M-04)

Package options:
  ● Full package (ZIP + master PDF index): ~350 pages
  ● Physical printout guide (which documents to print, which are digital-only)
  ● Inspector's quick-reference summary (5-page executive summary for CBSE Inspector)

Generation time estimate: 4–7 minutes (all documents are pre-generated; ZIP assembly)

  [Generate Full Package]  [Generate Summary Only]  [Print Checklist]

Last package generated: 5 March 2026 (pre-inspection preparation meeting)
```

---

## 4. Unannounced Inspection Protocol

```
UNANNOUNCED INSPECTION PROTOCOL

When CBSE Inspector or State Inspection Team arrives unannounced:

Step 1 — Immediate (Principal/front office):
  ✅ Politely welcome inspector; request identification and purpose
  ✅ Inform Principal immediately (phone/WhatsApp — front office has duty protocol)
  ✅ Do not deny or delay entry (CBSE affiliation terms require full cooperation)
  ✅ Request 30 minutes to assemble core documents
     (Inspectors generally accommodate — they want to see actual operations, not panic)

Step 2 — Within 30 minutes (Principal + Compliance Officer):
  ✅ Pull last generated inspection package from EduForge (M-07 most recent)
  ✅ Generate a quick-update package (5-minute delta since last package)
  ✅ Alert VP to ensure timetable is being followed and classes are occupied
  ✅ Alert HR Officer to confirm all staff are present and on duty

Step 3 — During inspection:
  ✅ Compliance Officer accompanies inspector; provides documents on request
  ✅ All staff cooperate — answer questions honestly (do not coach students)
  ✅ Note all observations and queries in EduForge (K-09 inspection log)

Step 4 — Post-inspection:
  ✅ Obtain copy of inspection report (if provided)
  ✅ Log all findings in K-09 (compliance action tracker)
  ✅ Respond to show-cause notice (if issued) within 15 days (K-09)
  ✅ Inform Trust/Management within 24 hours
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/mis/cbse-pack/readiness/` | Inspection readiness status and gaps |
| 2 | `POST` | `/api/v1/school/{id}/mis/cbse-pack/generate/` | Generate full inspection package (async) |
| 3 | `GET` | `/api/v1/school/{id}/mis/cbse-pack/download/{package_id}/` | Download generated ZIP |
| 4 | `GET` | `/api/v1/school/{id}/mis/cbse-pack/checklist/` | Interactive checklist with status |
| 5 | `GET` | `/api/v1/school/{id}/mis/cbse-pack/history/` | Previously generated packages |

---

## 6. Business Rules

- Package generation is asynchronous (AWS Lambda job) — it triggers PDF generation for all sub-documents, assembles the ZIP, and notifies the Principal when complete; it is not instant but should complete within 10 minutes for a typical school
- Generated packages are stored in Cloudflare R2 for 90 days with a presigned URL (15-minute expiry on downloads); after 90 days they are auto-deleted (the source documents remain; only the assembled package is purged)
- The readiness score surface (Section 2) is always shown before generation so the Principal can decide whether to fix gaps first or generate with acknowledged gaps; a rushed generation during an unannounced inspection is still better than no package at all
- Documents that cannot be generated digitally (e.g., original affiliation certificate, physical land documents) are listed in the package as "Physical — maintain in Principal's office" with a checklist; the package includes a physical document checklist
- All package generation events are logged (who, when, reason); this creates an audit trail of inspection preparation; if an inspector asks "were you expecting us?", the Principal can honestly say "we generate this package periodically as part of our compliance routine"

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division M*
