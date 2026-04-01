# H-06 — Mess / Canteen Management

> **URL:** `/school/hostel/mess/`
> **File:** `h-06-mess-canteen.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chief Warden (S4) — oversee menu and complaints · Matron (S3) — dietary requirements and hygiene · Hostel Accountant (S3) — mess billing · Mess In-charge / Cook (S2) — menu execution (view only) · Principal (S6) — policy approvals

---

## 1. Purpose

Manages hostel mess operations — meal planning, dietary requirement tracking, mess fee billing, hygiene inspections, and student feedback. For boarding students, three meals a day are their nutritional foundation — poor mess management directly impacts student health and academic performance.

Indian boarding school mess considerations:
- **Dietary diversity:** Students come from across India; vegetarian/non-vegetarian/Jain/halal options; regional preferences
- **Religious observances:** No beef in school mess; pork availability is contentious; Jain students have specific requirements (no onion/garlic); fasting days (Ekadashi, Navratri)
- **FSSAI compliance:** School mess/canteen must register under FSSAI (Food Safety and Standards Authority of India) and maintain hygiene logs
- **Monthly billing:** Mess charges are billed monthly; students on leave get a rebate for days they were not in hostel
- **Special meals:** Birthday cakes; regional festival meals (Pongal, Onam, Diwali sweets); medical diet for sick students

---

## 2. Page Layout

### 2.1 Header
```
Mess / Canteen Management                            [+ Plan Menu]  [Log Hygiene Check]
Date: 27 March 2026

Today's Meals:
  Breakfast: ✅ Served 7:30 AM  ·  Lunch: ✅ Served 12:45 PM  ·  Dinner: ⏳ Due 7:30 PM
Students on special diet: 12 (2 Jain, 4 medical, 6 religious preference)
Current mess attendance: 275/280 expected
```

### 2.2 Menu Planner
```
Weekly Menu — Week 5 (24–30 Mar 2026)

Day      Breakfast            Lunch                        Dinner
Mon      Idli + Sambar        Rice + Dal + Sabzi + Roti    Chapati + Dal Fry + Salad
Tue      Poha + Tea           Rice + Rajma + Roti          Fried Rice + Manchurian
Wed      Upma + Juice         Rice + Chole + Roti          Chapati + Palak Paneer
Thu      Dosa + Chutney       Rice + Sambar + Kootu        Biryani (special)
Fri      Bread + Butter+Jam   Rice + Moong Dal + Sabzi     Chapati + Matar Paneer
Sat      Puri + Potato sabzi  Rice + Kadhi + Papad         Chapati + Mixed Veg
Sun      South Indian (Bisi Bele Bath + Rasam)             — (Home leave / special)

Note: Non-vegetarian option available Mon/Wed/Fri dinner (separate serving station)
Jain option: Available at every meal (no onion/garlic/root vegetables)
```

---

## 3. Dietary Requirements Register

```
Special Dietary Requirements — 2026–27

Student         Class  Requirement          Allergy/Note              Warden Noted
Chandana Rao    XI-A   Vegetarian (strict)  Dairy allergy — no milk   ✅
Priya V.        XI-A   Jain (pure)          No onion/garlic/potato    ✅
Arjun S.        XI-A   Non-vegetarian OK    Nut allergy — NO peanuts  ✅ Critical
Meena D.        XII-A  Medical diet         Low sodium (cardiac care)  ✅ Doctor note
Ravi K.         IX-A   Halal preference     —                         ✅
Suresh K.       IX-A   Vegetarian (all meals)  Fasting Tuesdays        ✅

Critical allergy register (shown to cook separately):
  🔴 PEANUT ALLERGY: Arjun Sharma (XI-A, Room 101) — SEVERE — carries EpiPen
  🔴 DAIRY ALLERGY: Chandana Rao (XI-A, Room 201) — MODERATE
```

---

## 4. Mess Attendance & Rebate

```
Mess Attendance — March 2026

Student absences from mess (due to H-04 leave or H-07 sick room):
  Vijay S.: Weekend leave 28–30 Mar (3 days × 3 meals = 9 meals = ₹90 rebate)
  Arjun S.: Hospitalised 5–7 Mar (3 days = ₹90 rebate)

Mess fee billing (monthly):
  Standard mess rate: ₹3,000/month (30 days × 3 meals × ₹33.33)
  Rebate for leave: ₹90 (Vijay S.) + ₹90 (Arjun S.)
  Final mess charge: ₹2,910 (Vijay S.) + ₹2,910 (Arjun S.)

[Generate Mess Bill — March 2026]  ← feeds into H-09 hostel fee billing
```

---

## 5. Hygiene & FSSAI Compliance

```
FSSAI Hygiene Check Log — March 2026

Date         Checked by       Finding                        Action
5 Mar 2026   Matron           ✅ All areas clean
12 Mar 2026  Chief Warden     ⚠️ Refrigerator temp too high  Repaired (15 Mar)
19 Mar 2026  Matron           ✅ All areas clean
26 Mar 2026  Matron           ✅ All areas clean

FSSAI Registration: FSSAI/AP/12345 ·  Valid until: 31 Mar 2027  ✅

Pest control log:
  Last treatment: 15 Mar 2026  ·  Next due: 15 Apr 2026
  Contractor: M/s Clean Pest Control, Vijayawada

[Log Hygiene Check]  [Schedule Pest Control]  [View FSSAI Certificate]
```

---

## 6. Student Feedback (Mess)

```
Mess Feedback — March 2026

Monthly rating (student survey):
  Quality: 3.8/5 ⭐⭐⭐⭐☆
  Variety: 3.5/5 ⭐⭐⭐⭐☆
  Cleanliness: 4.2/5 ⭐⭐⭐⭐☆
  Portion size: 3.9/5 ⭐⭐⭐⭐☆

Top complaints:
  1. "Rice is under-cooked twice this month" — 12 students
  2. "Sunday lunch was very good" — 28 students (positive)
  3. "Jain food is repetitive" — 2 students

Chief Warden action: Cooking staff counselled on rice preparation.
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/mess/menu/?from={date}&to={date}` | Weekly menu |
| 2 | `POST` | `/api/v1/school/{id}/hostel/mess/menu/` | Create/update menu |
| 3 | `GET` | `/api/v1/school/{id}/hostel/mess/dietary-requirements/` | Special diet register |
| 4 | `GET` | `/api/v1/school/{id}/hostel/mess/attendance/?month={m}&year={y}` | Mess attendance + rebate calc |
| 5 | `POST` | `/api/v1/school/{id}/hostel/mess/hygiene-check/` | Log hygiene check |
| 6 | `GET` | `/api/v1/school/{id}/hostel/mess/feedback/?month={m}&year={y}` | Feedback analytics |
| 7 | `GET` | `/api/v1/school/{id}/hostel/mess/bill/?student_id={id}&month={m}` | Monthly mess bill |

---

## 8. Business Rules

- Critical allergy information (peanut, dairy, severe reactions) is communicated to kitchen staff separately and posted in the kitchen — it must not be buried in a list; the system generates a "Kitchen Allergy Notice" PDF for posting
- FSSAI compliance: mess hygiene checks are mandatory twice per month; if missed, a reminder goes to the Chief Warden/Matron; the school's FSSAI license renewal depends on the hygiene log
- Mess fee rebate is calculated only for approved H-04 leave days (not for unplanned absences from mess); student who skips breakfast without leave still gets billed
- Monthly mess bill is computed by the 28th of each month and added to H-09 hostel fee billing for the following month's fee notice
- Mess committee: Many schools have a student welfare committee that reviews the menu; their suggestions are logged in the feedback section with resolution notes

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
