# H-11 — Hostel Inventory

> **URL:** `/school/hostel/inventory/`
> **File:** `h-11-hostel-inventory.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Chief Warden (S4) — manage inventory · Administrative Officer (S3) — data entry · Matron (S3) — girls' hostel inventory · Principal (S6) — approve write-offs

---

## 1. Purpose

Tracks hostel assets assigned to students (bedding, mattress, pillow, locker, study table items) and common area assets (furniture, TV, washing machines). Ensures accountability for hostel property and enables damage charge recovery.

---

## 2. Page Layout

### 2.1 Stock Overview
```
Hostel Inventory                                     [Issue Items]  [Log Return]  [Stock Check]
Academic Year: [2026–27 ▼]

Total inventory items: 1,240
Issued to students: 840  ·  In stock: 380  ·  Damaged/written off: 20
```

### 2.2 Inventory Categories
```
Category          Total   Issued  Available  Damaged  Condition
Mattress          200     180     20         0        Good: 180, Fair: 0
Bedding set       200     180     20         2        Good: 178
Pillow            210     180     28         2        Good: 178, Fair: 2
Pillow cover      600     540     60         5        —
Locker key        300     280     20         0        —
Study light       180     165     15         5        —
Mosquito net      180     160     20         10       10 need replacement
```

---

## 3. Issue Items to Student

```
Issue Items — Chandana Rao (New move-in — Room 201)

Issue date: 28 March 2026

Items issued:
  ☑ Mattress (M-142) — Condition: Good
  ☑ Bedding set (BS-87) — Condition: Good
  ☑ Pillow (P-201) — Condition: Good
  ☑ Pillow covers (×2)
  ☑ Locker key (Locker 42-B)
  ☑ Study light (SL-58)

Student/Parent acknowledgement:
  "I acknowledge receiving the above items in the stated condition.
   I will return them in the same condition at the time of departure."
  Signature: _______________  Date: 28 Mar 2026

[Record Issue]  [Print Acknowledgement Form]
```

---

## 4. Return & Damage Assessment

```
Return Items — [Student exiting hostel]

Student: Vijay S. (X-B)  ·  Date: 15 Apr 2026

Items returned:
  Mattress (M-089): Condition on return: ● Good  ○ Fair  ○ Damaged
  Bedding (BS-042): Condition: ○ Good  ● Fair (minor staining — no charge below threshold)
  Pillow (P-104): ○ Good  ○ Fair  ● Damaged (torn cover — charge ₹200)
  Locker key: ✅ Returned
  Study light: ✅ Returned

Damage charges:
  Pillow replacement: ₹200 → deducted from caution deposit (D-14)

[Record Return]  [Generate Damage Invoice]
```

---

## 5. Annual Stock Verification

```
Annual Stock Check — April 2026

Mattresses:
  Records show: 200  ·  Physically counted: 198  ·  Missing: 2
  Investigation: 2 mattresses condemned in Oct 2025 — already written off in records ✅

Mosquito nets:
  Records show: 180  ·  Physically counted: 170  ·  Missing: 10
  Condition of counted: 10 damaged (need replacement)
  Action: Write off 10 missing + 10 damaged = 20 → Purchase order needed (D-19)

[Generate Stock Verification Report]  [Raise Purchase Order for Replacements]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/inventory/` | Inventory overview |
| 2 | `POST` | `/api/v1/school/{id}/hostel/inventory/issue/` | Issue items to student |
| 3 | `POST` | `/api/v1/school/{id}/hostel/inventory/return/` | Record return + condition |
| 4 | `GET` | `/api/v1/school/{id}/hostel/inventory/student/{student_id}/` | Student's issued items |
| 5 | `GET` | `/api/v1/school/{id}/hostel/inventory/stock-check/` | Current stock levels |

---

## 7. Business Rules

- Every item issued to a student is tracked with a unique item ID and condition; the acknowledgement form (student/parent signed) is the basis for damage charge disputes
- Items returned in "Fair" condition below a threshold (e.g., minor staining ≤ ₹100 cost) are not charged; this threshold is configurable
- Annual stock verification must reconcile physical count with digital records; discrepancies > 2% trigger a detailed investigation
- Replacement purchases are raised via D-19 vendor payment; item IDs for new stock are generated and added to inventory
- TC clearance (C-13) requires all hostel inventory items to be returned

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
