# C-03 — Study Material Upload

> **URL:** `/coaching/faculty/material/`
> **File:** `c-03-study-material.md`
> **Priority:** P1
> **Roles:** Faculty (K2) · Academic Coordinator (K5) — publish/archive control

---

## 1. Material Library

```
STUDY MATERIAL — Mr. Suresh Kumar (Quantitative Aptitude)
As of 30 March 2026

  Filter: [All ▼]  [Batch: All ▼]  [Type: All ▼]  [Search...]

  ┌────┬──────────────────────────────────────────┬──────────┬────────┬──────────┬────────┐
  │ #  │ Title                                    │ Type     │ Batch  │ Uploaded │ Views  │
  ├────┼──────────────────────────────────────────┼──────────┼────────┼──────────┼────────┤
  │ 1  │ Mensuration 3D — Notes + Formulas        │ PDF      │ CGL    │ 28 Mar   │  212   │
  │ 2  │ DI Mixed Practice Set #14                │ PDF      │ CGL    │ 26 Mar   │  198   │
  │ 3  │ Quant Sprint — Algebra Shortcuts         │ Video    │ CGL    │ 22 Mar   │  386   │
  │ 4  │ Mensuration 2D — 50 Practice Qs          │ PDF      │ ALL    │ 18 Mar   │  642   │
  │ 5  │ Time & Work — Formula Sheet              │ PDF      │ CHSL   │ 15 Mar   │  174   │
  │ 6  │ Banking Quant — DI Caselet #8            │ PDF      │ Bank   │ 14 Mar   │  148   │
  │ 7  │ Approximation 100 Qs (SSC Level)         │ PDF      │ CGL    │ 10 Mar   │  224   │
  │ 8  │ Simplification Tricks — Video Lecture    │ Video    │ CGL    │ 05 Mar   │  512   │
  └────┴──────────────────────────────────────────┴──────────┴────────┴──────────┴────────┘
  Total: 48 items  │  [+ Upload New Material]
```

---

## 2. Upload New Material

```
UPLOAD STUDY MATERIAL

  Title:           [Mensuration 3D — Class Notes 30 Mar 2026        ]
  Type:            ( ) PDF/Doc   (●) PDF (scanned)   ( ) Video   ( ) Link
  File:            [Choose file...] ← mensuration_3d_notes.pdf (2.4 MB)
                   Allowed: PDF, PPT, MP4 | Max size: 50 MB (doc) / 2 GB (video)

  Access:
    Assign to batch:  [✓] SSC CGL Morning  [✓] SSC CGL Evening
                      [ ] SSC CHSL         [ ] RRB NTPC
                      [ ] Banking          [ ] All batches
    Visible from:     [30/03/2026  06:00]  (default: immediately)
    Visible until:    [ ] No expiry  / (●) Until: [30/09/2026]

  Tags:             [mensuration] [3D] [class10] [formula-sheet]  + Add tag

  Description (optional):
    [Notes from today's class — Volume and Surface Area formulas
     with shortcut methods for SSC. Includes 20 practice questions.]

  [Upload & Publish]   [Save as Draft]   [Cancel]

  ⚠️ Material is watermarked with "Toppers Coaching Centre — Confidential"
     before delivery to students — do not upload already-watermarked files.
```

---

## 3. Material Analytics

```
MATERIAL ENGAGEMENT ANALYTICS — Last 30 Days

  Most Viewed:
  ┌───────────────────────────────────────────┬───────┬──────────────────────────┐
  │ Title                                     │ Views │ Avg time open (PDF)      │
  ├───────────────────────────────────────────┼───────┼──────────────────────────┤
  │ Simplification Tricks — Video Lecture     │  512  │ 18.4 min (of 22 min)     │
  │ Mensuration 2D — 50 Practice Qs          │  642  │ 12.8 min (likely printed) │
  │ Quant Sprint — Algebra Shortcuts (video)  │  386  │ 14.2 min (of 16 min)     │
  └───────────────────────────────────────────┴───────┴──────────────────────────┘

  NOT VIEWED (uploaded > 7 days ago, views < 20):
  ⚠️ Banking Quant — Caselet #8 (148 views from 196 students — 75.5% ✅ acceptable)
  ⚠️ Time & Work Formula Sheet (174 views from 178 students — 97.8% ✅ excellent)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/material/?faculty={fid}` | Faculty's material library |
| 2 | `POST` | `/api/v1/coaching/{id}/material/` | Upload new material |
| 3 | `DELETE` | `/api/v1/coaching/{id}/material/{mid}/` | Remove material (soft delete) |
| 4 | `GET` | `/api/v1/coaching/{id}/material/{mid}/analytics/` | Views, time-open for a file |
| 5 | `PATCH` | `/api/v1/coaching/{id}/material/{mid}/access/` | Update batch visibility or expiry |

---

## 5. Business Rules

- All uploaded material is automatically watermarked with the institute name and "Confidential" before being served to students; this discourages unauthorised sharing and protects TCC's intellectual property; the watermark includes the student's name and roll number on PDFs delivered to individual students, making it traceable if a PDF is leaked to a competitor or uploaded to Telegram channels (a common problem in coaching)
- Material access must be batch-specific by default; uploading a note for "All batches" should be a deliberate choice, not the default; a Quant note designed for SSC CGL level may be inappropriate for Foundation batch students who are at Class 9–10 level; faculty must consciously select which batches see which material
- Videos uploaded to EduForge are stored in AWS S3 with signed URL delivery; videos are never directly downloadable by students — they can only be streamed; signed URLs expire after 4 hours; this prevents students from downloading videos and sharing them outside the platform, which would undermine TCC's paid course value
- Material expiry dates should be set to 6 months after the batch ends; keeping old material active indefinitely creates a cluttered library and confuses students who find outdated notes from previous years; the expiry system ensures students see only current-batch-relevant material; expired material is archived (not deleted) and remains accessible to faculty for reuse in future batches
- Faculty cannot delete material that has been viewed by more than 50 students — they can only archive it; this prevents accidental or deliberate deletion of widely-used material that students may have bookmarked or be actively studying; only the Academic Coordinator (K5+) can permanently delete such material, with an audit log entry explaining the reason

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division C*
