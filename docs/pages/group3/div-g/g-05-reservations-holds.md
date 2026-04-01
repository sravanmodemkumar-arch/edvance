# G-05 — Reservations & Holds

> **URL:** `/school/library/reservations/`
> **File:** `g-05-reservations-holds.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Librarian (S3) — manage queue · Library Assistant (S2) — view · Students/Parents — reserve via portal

---

## 1. Purpose

Allows members to reserve a book that is currently issued. When the book is returned, the next person in the reservation queue is notified and given a 2-day window to collect it.

---

## 2. Page Layout

### 2.1 Reservation Queue
```
Active Reservations                                  [View All Reservations]

Book                   Copies  All Issued  Queue  Next Available   Next in Queue
Atomic Habits          2       2           1      10 Apr 2026      Priya Venkat (XI-A)
Wings of Fire          3       3           3      15 Apr 2026      Ravi Kumar (IX-A)
```

---

## 3. Place Reservation

```
Student portal / Librarian on behalf:

Book: Wings of Fire (A.P.J. Abdul Kalam) — 3 copies, all issued
Current queue: 2 members ahead

[Place Reservation for Ravi Kumar (IX-A)]

Estimated wait: ~15 days (based on current due dates + queue position)
Notification: WhatsApp when book becomes available

[Confirm Reservation]

Ravi Kumar now in queue position 3.
```

---

## 4. Notification on Return

```
When a reserved book is returned:

Book: Wings of Fire (copy LIB2023012) returned on 12 Apr 2026

Reservation queue:
  Position 1: Priya Venkat (XI-A) — waiting since 20 Feb 2026

Auto-notification sent:
  WhatsApp to Priya's parent:
  "Good news! 'Wings of Fire' is now available at the library.
   Please collect within 2 days (by 14 Apr 2026). — School Library"

Book status: 🔒 Reserved for Priya (2-day hold window)
If not collected by 14 Apr 2026 → moves to next in queue (Ravi Kumar)
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/reservations/` | Active reservation queues |
| 2 | `POST` | `/api/v1/school/{id}/library/reservations/` | Place reservation |
| 3 | `DELETE` | `/api/v1/school/{id}/library/reservations/{res_id}/` | Cancel reservation |
| 4 | `GET` | `/api/v1/school/{id}/library/catalogue/{book_id}/queue/` | Queue for specific book |

---

## 6. Business Rules

- A member can reserve a maximum of 3 books at a time (configurable); reserving does not count against the borrowing limit
- The hold window after a reserved book becomes available is 2 school days; if not collected, the reservation moves to the next person in queue
- A member already at their borrowing limit (e.g., 2/2 issued) can still reserve but will be notified only when they have capacity to borrow
- Reserved copies cannot be issued to other members even if a non-reserving member asks at the counter during the hold window
- If no copies of a book exist in the catalogue, the reservation system suggests requesting the book via G-02 Acquisition

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
