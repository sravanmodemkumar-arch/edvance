# B-22 — Topic Master (Subject-Class)

> **URL:** `/school/academic/curriculum/topics/`
> **File:** `b-22-topic-master.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HOD (S4) — own dept · Academic Coordinator (S4) — full · Subject Teacher (S3) — update own · Principal (S6) — full

---

## 1. Purpose

The master list of all chapters and topics for every subject in every class. This is the granular syllabus database that feeds B-03 (Syllabus Tracker) — teachers mark individual topics as "Done" against this list. It also feeds B-02 (Lesson Plan Review) — teachers reference specific topic IDs when writing lesson plans. The Topic Master is set up at the start of the academic year (by importing from the CBSE/board syllabus via B-21) and then fine-tuned by HODs to reflect the school's actual teaching sequence. Having a clean, accurate Topic Master is the prerequisite for meaningful syllabus tracking.

---

## 2. Page Layout

### 2.1 Header
```
Topic Master                                      [+ Add Topic]  [Bulk Import]  [Reorder]  [Export]
Subject: [Science ▼]  Class: [IX ▼]  Academic Year: [2025–26 ▼]
Total Topics: 89  ·  Active: 89  ·  Term 1: 44  ·  Term 2: 45
```

---

## 3. Topic List

Hierarchical list: Chapters → Topics → Sub-topics (optional third level)

```
Chapter 1 — Matter in Our Surroundings                    [+ Add Topic]  [Edit Chapter]
  1.1  Physical nature of matter                          P1  T1  ✅ Active  [Edit] [Move]
  1.2  Characteristics of particles of matter             P1  T1  ✅ Active  [Edit] [Move]
  1.3  States of matter                                   P1  T1  ✅ Active  [Edit] [Move]
  1.4  Evaporation                                        P1  T1  ✅ Active  [Edit] [Move]

Chapter 2 — Is Matter Around Us Pure?                     [+ Add Topic]  [Edit Chapter]
  2.1  Mixtures                                           P1  T1  ✅ Active  [Edit] [Move]
  2.2  Solutions                                          P1  T1  ✅ Active  [Edit] [Move]
  2.3  Separation of components of a mixture             P1  T1  ✅ Active  [Edit] [Move]
  2.4  Physical and chemical changes                      P1  T1  ✅ Active  [Edit] [Move]
  2.5  Types of pure substances                           P1  T1  ✅ Active  [Edit] [Move]

Chapter 3 — Atoms and Molecules                           [+ Add Topic]  [Edit Chapter]
  3.1  Laws of chemical combination                       P1  T1  ✅ Active
  3.2  What is an atom?                                   P1  T1  ✅ Active
  ...

Chapter 8 — Motion                                        [+ Add Topic]  [Edit Chapter]
  8.1  Describing motion                                  P1  T2  ✅ Active
  8.2  Measuring the rate of motion                       P1  T2  ✅ Active
  8.3  Rate of change of velocity                         P1  T2  ✅ Active
  8.4  Graphical representation of motion                 P1  T2  ✅ Active
  8.5  Equations of motion                               P1  T2  ✅ Active
  8.6  Uniform circular motion                            P1  T2  ✅ Active
```

Column headers: **P** = Priority (P0/P1/P2 for exam weightage) · **T** = Term (T1/T2/T3) · Status · Actions

---

## 4. Topic Edit Drawer

Clicking [Edit] on any topic:

| Field | Value |
|---|---|
| Topic Name | "States of matter" |
| Chapter | Chapter 1 — Matter in Our Surroundings |
| NCERT Reference | "Class IX Science, Chapter 1, Page 4–14" |
| CBSE Weightage | Medium (typically 1–2 marks MCQ or part of 3-mark SA) |
| Term | Term 1 |
| Estimated Periods | 2 (takes approximately 2 class periods to complete) |
| Difficulty Level | Easy / Medium / Hard |
| Bloom's Level | Remember · Understand · Apply · Analyse |
| Lab Activity | Yes/No — "Demonstration: states of matter transformation" |
| NEP Activity Tag | "Real-world connection: water cycle" |
| Status | Active / Inactive |

**[Add Sub-topic]** → e.g., "1.3.1 Solid state", "1.3.2 Liquid state", "1.3.3 Gaseous state"

---

## 5. Bulk Import

[Bulk Import] → for importing topic lists from:
- **EduForge CBSE Library** (pre-built, curated topic lists for all CBSE subjects)
- **CSV Upload** (columns: chapter_no, chapter_name, topic_no, topic_name, term, estimated_periods)

**From CBSE Library:**
- Select board: CBSE
- Select class: IX
- Select subject: Science
- Preview: shows all 89 topics with chapter structure
- [Import] → creates topics in bulk; existing topics are not overridden (deduplication by NCERT reference)

---

## 6. Topic Sequencing / Reorder

[Reorder] → drag-and-drop interface to reorder topics within a chapter or chapters within the subject.

Teachers often teach chapters out of NCERT order — e.g., "Motion" before "Forces" even though NCERT has them in a different order. The sequence here defines the order in which the Syllabus Tracker expects topics to be covered.

Note: Reordering changes the "expected completion by week" calculation in B-03.

---

## 7. Term Mapping

Topics can be assigned to Term 1, Term 2, or Term 3. This determines:
- Which topics the Half-Yearly exam (Term 1) covers
- Which topics the Annual exam (full year) covers
- The "target %" line in B-03 (Syllabus Tracker) is computed from term boundaries

| Term | Chapters | Topics | % of Total |
|---|---|---|---|
| Term 1 | Ch 1–8 | 44 | 49.4% |
| Term 2 | Ch 9–15 | 45 | 50.6% |

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/curriculum/topics/?subject={s}&class={c}&year={y}` | Topic list |
| 2 | `POST` | `/api/v1/school/{id}/curriculum/topics/` | Add single topic |
| 3 | `PATCH` | `/api/v1/school/{id}/curriculum/topics/{topic_id}/` | Edit topic |
| 4 | `DELETE` | `/api/v1/school/{id}/curriculum/topics/{topic_id}/` | Soft-delete (archive) |
| 5 | `POST` | `/api/v1/school/{id}/curriculum/topics/bulk-import/` | Bulk import |
| 6 | `PATCH` | `/api/v1/school/{id}/curriculum/topics/reorder/` | Reorder (sequence update) |
| 7 | `GET` | `/api/v1/school/{id}/curriculum/topics/cbse-library/?subject={s}&class={c}` | CBSE topic library |

---

## 9. Business Rules

- A topic that has been marked "Done" in B-03 by at least one teacher cannot be deleted — only archived (with a warning)
- NCERT reference is not mandatory but strongly recommended — it links the topic to the official textbook page for teachers who want to verify scope
- Estimated periods per topic is used for pace calculation in B-03 (if 1.3 is estimated at 2 periods, the system expects it to be done ~2 days after 1.2 was marked done)
- Topics without a term assignment are treated as "Any term" and don't affect term-specific target calculations
- The Topic Master must have at least 1 topic before B-03 (Syllabus Tracker) will show a progress bar for that subject-class

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
