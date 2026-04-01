# B-37 — Accessibility (WCAG) Compliance Dashboard

> **Route:** `/product/accessibility/`
> **Division:** B — Product & Design
> **Primary Role:** UI/UX Designer (Role 8, Level 5) · PM — Institution Portal (Role 7, Level 4)
> **Read Access:** Frontend Engineer (Role 12) · Mobile Engineer (Role 13) · QA Engineer (Role 9)
> **File:** `b-37-accessibility-compliance.md`
> **Priority:** P1 — RPwD Act 2016 requires accessible digital services; 3 PwD students currently enrolled
> **Status:** ✅ New page — WCAG 2.1 AA compliance tracking for all EduForge interfaces

---

## 1. Purpose

EduForge serves students with disabilities across 2,050 institutions — PwD students who are visually impaired, hearing impaired, have locomotor disabilities, or cognitive differences. Under the RPwD Act 2016 (Section 42), public-facing digital services in India must be accessible. Additionally, NAAC Criterion 7 evaluates institutional commitment to accessibility, and NBA accreditation expects digital learning tools to be usable by all students.

This dashboard tracks WCAG 2.1 AA compliance across all EduForge web pages, mobile screens, and exam interfaces. It provides: (1) page-by-page accessibility audit scores, (2) issue tracking (violations by type: color contrast, alt text, keyboard navigation, ARIA labels, focus management), (3) screen reader compatibility testing (NVDA, VoiceOver, TalkBack), (4) exam-specific accommodations (extended time rendering, large text mode, high contrast theme, screen reader-friendly question navigation), and (5) automated + manual audit scheduling.

---

## 2. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Accessibility Compliance (WCAG 2.1 AA)    [Run Automated Audit]    │
├─────────────────────────────────────────────────────────────────────┤
│  COMPLIANCE KPI (5 tiles)                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ 82.4%    │ │ 48       │ │ 12       │ │ 91.2%    │ │ 3        │ │
│  │ Overall  │ │ Open     │ │ Critical │ │ Exam     │ │ Screen   │ │
│  │ WCAG AA  │ │ Issues   │ │ (P0/P1)  │ │ Interface│ │ Readers  │ │
│  │ ⚠️ <90%  │ │          │ │ ⚠️ Fix   │ │ ✅ >90%  │ │ Tested ✅│ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│  [By Page] [By Issue Type] [Exam A11y] [Screen Reader] [Audit Log] │
├─────────────────────────────────────────────────────────────────────┤
│  COMPLIANCE BY PAGE GROUP                                           │
│                                                                     │
│  Page Group              │ Pages │ Score  │ P0 │ P1 │ P2 │ Status  │
│  ─────────────────────────────────────────────────────────────────  │
│  Student Exam Interface  │ 8     │ 91.2%  │ 0  │ 2  │ 4  │ ✅      │
│  Parent Portal           │ 13    │ 84.6%  │ 1  │ 3  │ 8  │ ⚠️      │
│  School Admin Portal     │ 42    │ 78.4%  │ 3  │ 8  │ 14 │ ⚠️      │
│  College Admin Portal    │ 38    │ 76.2%  │ 4  │ 6  │ 12 │ ⚠️      │
│  Platform Admin (G1)     │ 225   │ 68.1%  │ 8  │ 14 │ 22 │ ❌      │
│  Mobile App (Flutter)    │ 28    │ 86.8%  │ 0  │ 4  │ 6  │ ✅      │
│                                                                     │
│  PRIORITY: Exam interface > Parent/Student > Admin portals          │
│  Exam interface at 91.2% because PwD students take exams via this   │
│  Platform admin at 68.1% — lower priority (no PwD admin users)      │
├─────────────────────────────────────────────────────────────────────┤
│  TOP ISSUES BY TYPE                                                 │
│                                                                     │
│  Issue Type                │ Count │ WCAG Criterion    │ Severity   │
│  ─────────────────────────────────────────────────────────────────  │
│  Color contrast <4.5:1     │ 18    │ 1.4.3 Contrast    │ P1         │
│  Missing alt text (images) │ 12    │ 1.1.1 Non-text    │ P1         │
│  Keyboard trap (modals)    │ 4     │ 2.1.2 No Trap     │ P0 ⚠️      │
│  Missing form labels       │ 8     │ 1.3.1 Info        │ P2         │
│  Focus not visible         │ 6     │ 2.4.7 Focus       │ P1         │
│  ARIA roles missing        │ 14    │ 4.1.2 Name/Role   │ P2         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Exam-Specific Accessibility

```
EXAM INTERFACE ACCESSIBILITY (91.2% WCAG AA)

PwD EXAM ACCOMMODATIONS SUPPORTED:
  ✅ Extended time mode: Timer adjusted per PwD allocation (I-06 JNTU norms)
  ✅ Large text mode: All text ≥18pt; question images auto-scaled
  ✅ High contrast theme: Black background, white text, yellow highlights
  ✅ Screen reader navigation: Questions announced; options read aloud (ARIA live regions)
  ✅ Keyboard-only navigation: Tab through questions, Enter to select, Ctrl+S to save
  ✅ Single-question view: One question per screen (reduces cognitive load)
  ⬜ Voice input for answers: Phase 2 (requires speech-to-text integration)
  ⬜ Braille display support: Phase 3 (requires specialized browser testing)

SCREEN READER TEST RESULTS (March 2027):
  NVDA (Windows): ✅ 94% tasks completable (2 issues: timer announcement, chart alt text)
  VoiceOver (macOS/iOS): ✅ 92% tasks completable (3 issues: dropdown navigation)
  TalkBack (Android): ✅ 88% tasks completable (Flutter accessibility labels need work)

TESTING METHODOLOGY:
  Automated: axe-core browser extension (CI/CD integrated — runs on every PR)
  Manual: Quarterly audit by accessibility specialist (external contractor)
  User testing: 1 PwD student (Arjun V., GCEH) tested exam interface — Feb 2027
    Findings: "Timer difficult to find with screen reader" → Fixed (ARIA live)
              "Submit button focus lost after answering" → Fixed (focus management)
```

---

## 4. Business Rules

- **Exam interface accessibility is P0 — it directly enables or prevents PwD students from taking exams.** A keyboard trap in the exam modal means a blind student using a screen reader literally cannot submit their exam. This is not an aesthetic issue — it is a functional exclusion. Exam interface accessibility issues are treated as P0 bugs with same-day fix SLA.
- **Color contrast ratio of 4.5:1 (WCAG 1.4.3) is the minimum for body text.** EduForge's dark theme (`#070C18` background) creates challenges — light gray text on dark backgrounds often fails the 4.5:1 ratio. The design system (B-19) must enforce contrast ratios in the color token definitions, and axe-core CI checks catch violations before merge.
- **Automated testing catches ~30% of accessibility issues; manual testing catches the rest.** axe-core is good at detecting missing alt text, contrast failures, and ARIA errors. It cannot detect: keyboard traps in complex HTMX interactions, screen reader announcement ordering, cognitive clarity of error messages, or whether focus management works after HTMX partial page swaps. Quarterly manual audits are essential.
- **RPwD Act 2016 Section 42 mandates accessibility for digital services in India.** While enforcement for EdTech platforms is currently limited, this is changing. The Rights of Persons with Disabilities (Amendment) Bill extends digital accessibility obligations. Being proactively accessible is: (a) legally prudent, (b) ethically correct, (c) a NAAC differentiator, and (d) a feature that benefits all users (large text mode is popular with non-PwD users too).
- **Platform admin pages (Group 1) at 68.1% compliance is acceptable at lower priority.** There are currently no PwD staff members using admin interfaces. However, this should not be used as an excuse to ignore admin accessibility indefinitely — it prevents hiring PwD staff in the future. Target: 80% for admin pages by December 2027.

---

*Last updated: 2026-03-30 · Group 1 — Platform Admin · Division B*
