# C-20 — Family & Sibling Linkage

> **URL:** `/school/students/families/`
> **File:** `c-20-family-sibling-linkage.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Admission Officer (S3) — full · Administrative Officer (S3) — full · Principal (S6) — full

---

## 1. Purpose

Links students from the same family into a single family unit — enabling:
- **Sibling discount computation:** Many Indian schools offer 10–15% tuition fee discount for 2nd and 3rd child from the same family; the fee module (div-d) needs this linkage to compute discounts automatically
- **Single parent view:** Parents with multiple children at the school see all children's information in one parent portal dashboard with a single login
- **Sibling admission priority:** During C-04 Seat Allocation, sibling of existing student gets priority
- **Consolidated communication:** School sends one WhatsApp message per family for common events (annual day, PTM reminder) instead of duplicate messages
- **Emergency contacts:** When one child's emergency contact is called, the same contact can be informed about the sibling too

In Indian private schools, 15–25% of students have at least one sibling enrolled in the same school — especially in schools that serve multiple classes (Nursery–XII). Getting this linkage right avoids double-billing for fee discounts and reduces parent frustration from duplicate communications.

---

## 2. Page Layout

### 2.1 Header
```
Family & Sibling Linkage                      [+ Create Family]  [Auto-detect Siblings]  [Export]
Total Families: 312  ·  Multi-child Families: 68 (22%)  ·  Discount Eligible: 52
3-child Families: 8  ·  4+ child Families: 2
```

### 2.2 Family List
| Family ID | Family Name | Children | Sibling Discount | Parent Login |
|---|---|---|---|---|
| FAM-0001 | Sharma Family | 2 children | ✅ Active (10%) | Active |
| FAM-0002 | Kumar Family | 1 child | — | Active |
| FAM-0003 | Rajan Family | 3 children | ✅ Active (15%) | Active |

---

## 3. Family Record

Clicking FAM-0001:

```
Sharma Family
────────────────────────────────────────────────────────────
Primary Parent: Rajesh Sharma  ·  9876543210  ·  rajesh@email.com
Secondary Parent: Meena Sharma  ·  9876512345

Children at School:
1. Arjun Sharma — XI-A — Roll 15 — STU-0001187  (Elder)
2. Rahul Sharma — VII-B — Roll 22 — STU-0001050  (Younger)

Sibling Discount:
  Policy: 2nd child — 10% on tuition fee
  Applied to: Rahul Sharma (2nd child — lower class)
  Monthly Discount: ₹650 (10% of ₹6,500/month)

Parent Portal:
  Father login: rajesh@email.com  [Last login: 20 Mar 2026]
  Mother login: meena@email.com   [Last login: 18 Mar 2026]
  Combined dashboard: Shows both Arjun and Rahul

Communication Log (last 5):
  24 Mar 2026 — Annual Day invite sent — 1 message (not 2)
  20 Mar 2026 — Fee reminder for Rahul (overdue Q4)
  15 Mar 2026 — Arjun — Exam schedule WhatsApp
```

---

## 4. Create Family / Link Siblings

### 4.1 Auto-detect
[Auto-detect Siblings] → system finds potential sibling matches:

```
Auto-detection based on:
  Same Father Name + Same Address → potential siblings
  Same Phone Number (primary) → potential siblings

Suggested Links:

Arjun Sharma (XI-A) + Rahul Sharma (VII-B)
  Father: Rajesh Sharma (both records)
  Address: 14, Gandhi Nagar, Hyderabad (both records)
  → Confidence: HIGH ✅  [Link as Siblings]  [Not siblings]

Priya Kumar (VIII-A) + Pooja Kumar (V-B)
  Father: Ravi Kumar (both records)
  Phone: 9876509876 (both records)
  → Confidence: HIGH ✅  [Link as Siblings]  [Not siblings]

Suresh M. (IX-B) + Sunita M. (III-A)
  Father: Mohan M. (both; but mother different)
  → Confidence: MEDIUM ⚠️  [Review]  [Not siblings]
```

### 4.2 Manual Link
[+ Create Family] → search students to add to a family unit:
```
Search student: [Arjun Sharma → STU-0001187]
Add sibling:    [Rahul Sharma → STU-0001050]
Relationship:   Elder / Younger / Twin
Family Name:    Sharma (auto from Father's surname)
[Create Family Link]
```

---

## 5. Sibling Discount Configuration

School configures the discount policy in settings (div-d Fee Settings):
| Sibling | Discount |
|---|---|
| 1st child | 0% |
| 2nd child | 10% on tuition |
| 3rd child | 15% on tuition |
| 4th+ child | 20% on tuition |

Once family is linked, the fee module automatically applies the discount. If the elder sibling leaves (C-12 Withdrawal), the younger sibling's discount is recalculated automatically.

---

## 6. Consolidated Parent View

Parent logging into the parent portal sees:

```
Welcome, Rajesh Sharma

Your Children:
[Arjun Sharma]              [Rahul Sharma]
Class XI-A                  Class VII-B
Attendance: 87%             Attendance: 92%
Last exam: 78.4%            Last exam: 82.1%
Fees: ✅ Paid               Fees: ⚠️ ₹5,850 due
[View Details]              [View Details]
```

Single login, single parent — both children visible.

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/families/?year={year}` | Family list |
| 2 | `POST` | `/api/v1/school/{id}/families/` | Create family linkage |
| 3 | `GET` | `/api/v1/school/{id}/families/{family_id}/` | Family detail |
| 4 | `PATCH` | `/api/v1/school/{id}/families/{family_id}/` | Update family (add/remove sibling) |
| 5 | `GET` | `/api/v1/school/{id}/families/auto-detect/` | Auto-detect potential sibling matches |
| 6 | `POST` | `/api/v1/school/{id}/families/{family_id}/link/` | Confirm link after auto-detect |

---

## 8. Business Rules

- A student can belong to only one family unit in EduForge; attempting to add a student to two different family units shows a conflict warning
- Sibling discount applies to the student with the lower class (younger child) — not both; school can override this policy
- When a family has students at two different EduForge tenants (e.g., elder at one school, younger at another), there is no cross-tenant linkage; the discount applies only within a single school
- Auto-detection is suggestive — staff must confirm; incorrect automatic linking could cause wrong fee discounts
- Parent portal accounts are linked at the family level; a parent whose child leaves school (C-12) retains access to their other child's portal

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
