# Component: Forms & Input Fields

---

## Input Field (Text)

### Layout — States
```
Default:    ┌─────────────────────────────┐
            │ Placeholder text            │
            └─────────────────────────────┘
            Helper text or hint

Focused:    ┌─────────────────────────────┐  ← Primary color border
            │ User is typing here         │
            └─────────────────────────────┘
            Helper text

Filled:     ┌─────────────────────────────┐  ← Default border color
            │ Entered value               │
            └─────────────────────────────┘

Error:      ┌─────────────────────────────┐  ← Red border
            │ Invalid value               │
            └─────────────────────────────┘
            ❌ Error message here

Disabled:   ┌─────────────────────────────┐  ← Gray, no interaction
            │ Field is disabled           │
            └─────────────────────────────┘

Read-only:  ┌─────────────────────────────┐  ← Shows value, no edit
            │ Read-only value             │
            └─────────────────────────────┘  ← No border, tinted bg
```

### Label Position
- **Floating label (default):** Label starts as placeholder, floats up on focus/fill
- **Fixed label above:** For dense forms. Label always above, never placeholder
- **No label:** Only for obvious inputs (search bar, inline edit)

### Required Indicator
- Required fields: Red asterisk `*` after label
- Optional fields: "(optional)" text in gray after label — use sparingly
- Error: Inline below field in red, `font-size: 12px`

### Input Variants

| Type | Behavior | Usage |
|---|---|---|
| `text` | Plain text | Name, address |
| `tel` | `+91` prefix, numeric on mobile | Mobile numbers |
| `email` | Lowercase transform, @ validation | Email address |
| `number` | Arrow controls, min/max/step | Age, marks, count |
| `password` | Toggle show/hide icon | Passwords (if any) |
| `search` | 🔍 icon left, ✕ to clear | Search inputs |
| `url` | Auto-prepend https:// | YouTube URLs, website |
| `textarea` | Multi-line. Resizable vertically only. | Notes, descriptions |

---

## Select / Dropdown

### Single Select
```
┌─────────────────────────────────────────────┐
│  Select Class                          [▼]  │
└─────────────────────────────────────────────┘

On open:
┌─────────────────────────────────────────────┐
│  [🔍 Search classes...]                     │
│  ─────────────────────────────────────────  │
│  Class 6                                    │
│  Class 7                                    │
│  ● Class 8  ← (selected)                   │
│  Class 9                                    │
│  Class 10                                   │
│  Class 11                                   │
│  Class 12                                   │
└─────────────────────────────────────────────┘
```

### Multi-Select
```
┌──────────────────────────────────────────────────┐
│  [Class 11 ✕] [Class 12 ✕]  Subjects...  [▼]   │
└──────────────────────────────────────────────────┘

Selected values shown as chips inside field.
Max visible chips: 3. More = "[+2 more]" chip.
```

### Behavior

| Property | Spec |
|---|---|
| Search | Inline search if > 7 options |
| Keyboard | Arrow up/down navigate, Enter select, Esc close |
| Clear | `[✕]` appears when selected. Clears selection |
| Groups | Options can be grouped with section headers |
| Create new | "Add '[typed value]'" option at bottom (if enabled) |
| Max height | Dropdown max 280px, scrollable |
| Loading | "Loading options..." skeleton while async options load |
| Empty | "No options found" when search returns nothing |

---

## Checkbox & Radio

### Checkbox Group
```
What does this staff access?

[✅] Student records
[✅] Fee management
[  ] Exam results
[  ] User management
[  ] System settings
```

### Radio Group
```
Hostel status:

[◉] Day Scholar (default)
[○] Hosteler
[○] Both (for multi-campus)
```

### Toggle (Switch)
```
OFF:  [○──────]   grey bg
ON:   [──────●]   primary color bg
```
- Toggle with label always to the right of switch
- Use for settings that take immediate effect (no submit needed)
- For form-level choices that need submit: use checkbox instead

---

## Date & Time Picker

### Date Input
```
┌─────────────────────────────────────────┐
│  [DD] / [MM] / [YYYY]          [📅]    │
└─────────────────────────────────────────┘
```
- Three separate number inputs for DD/MM/YYYY
- Auto-advance: after DD filled → focus moves to MM → YYYY
- Calendar icon opens date picker popup (see [04-filters-search.md](04-filters-search.md))
- Validation: real date check (no Feb 30 etc.), age constraints

### Time Input
```
┌──────────────────────────────────────┐
│  [HH] : [MM]  [AM ▼]        [⏰]   │
└──────────────────────────────────────┘
```

### Date-Time Combined
```
┌────────────────────────────────────────────────────┐
│  [DD] / [MM] / [YYYY]    [HH] : [MM]  [AM ▼]     │
└────────────────────────────────────────────────────┘
```

---

## File Upload

### Layout
```
┌──────────────────────────────────────────────────────┐
│                                                      │
│     [⬆️ Upload Icon]                                │
│                                                      │
│     Drag & drop files here                           │
│     or [Browse files]                                │
│                                                      │
│     Supported: JPG, PNG, PDF · Max 10MB each        │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Upload States
```
Uploading:  ████████████░░░░  75%   filename.pdf  [✕]
Success:    ✅  filename.pdf  (1.2 MB)             [✕]
Error:      ❌  Too large (15MB). Max is 10MB.     [Retry]
```

### Multi-file Upload
```
┌────────────────────────────────────────────────────────────┐
│  ✅  aadhaar_front.jpg     (2.1 MB)              [✕]       │
│  ✅  degree_certificate.pdf (3.4 MB)             [✕]       │
│  ⏳  experience_letter.pdf  Uploading... 45%     [✕]       │
│                                                            │
│  [+ Add another file]            Total: 3 files / 5 max   │
└────────────────────────────────────────────────────────────┘
```

---

## OTP Input

> See [01-authentication.md](../auth/01-authentication.md) for full OTP spec.

Quick reference:
- 6 individual `<input>` boxes in flex row
- Auto-advance on digit entry
- Paste distributes across boxes
- Backspace clears current + moves back

---

## Form Layout Patterns

### Single Column (Default for drawers, mobile)
```
Field Label *
[_________________________]
Helper text

Field Label *
[_________________________]
```

### Two Column (Desktop forms)
```
First Name *              Last Name *
[______________]          [______________]

Mobile *                  Email (optional)
[______________]          [______________]
```

### Form Section Groups
```
┌──────────────────────────────────────────────┐
│  Personal Information                   [▼]  │  ← Collapsible section
│  ──────────────────────────────────────────  │
│  [fields...]                                 │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  Academic Details                       [▼]  │
│  ──────────────────────────────────────────  │
│  [fields...]                                 │
└──────────────────────────────────────────────┘
```

### Form Footer (Standard)
```
                        [Cancel]  [Save Changes]
```
- Cancel: Ghost/text button, left or second-from-right
- Save: Primary filled button, rightmost
- Destructive action (Delete): Left-aligned, red text button

### Unsaved Changes Guard
> When user tries to leave form with unsaved changes:
```
┌─────────────────────────────────────────┐
│  Unsaved changes                        │
│                                         │
│  You have unsaved changes.              │
│  What would you like to do?             │
│                                         │
│  [Discard changes]  [Keep editing]      │
└─────────────────────────────────────────┘
```

---

## Theme Support (Dark + Light)

```css
/* ── Text input ── */
.input {
  background: var(--bg-surface-2);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-sm);
  transition: border-color 150ms, box-shadow 150ms;
  width: 100%;
}
.input::placeholder { color: var(--text-muted); }

.input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--primary) 20%, transparent);
  outline: none;
}

.input--error {
  border-color: var(--error);
}
.input--error:focus {
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--error) 20%, transparent);
}

.input:disabled {
  background: var(--bg-surface-2);
  color: var(--text-muted);
  cursor: not-allowed;
  opacity: 0.5;
}

/* Dark */
:root .input {
  background: var(--bg-surface-2);      /* #131F38 */
  border-color: var(--border-default);  /* #334155 */
  color: var(--text-primary);           /* #F1F5F9 */
}

/* Light */
[data-theme="light"] .input {
  background: var(--bg-surface-1);      /* #FFFFFF */
  border-color: var(--border-default);  /* #CBD5E1 */
  color: var(--text-primary);           /* #0F172A */
}

/* ── Label ── */
.input-label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: var(--space-1);
  display: block;
}
.input-label--required::after { content: ' *'; color: var(--error); }

/* ── Helper / error text ── */
.input-helper { font-size: var(--text-xs); color: var(--text-muted); margin-top: var(--space-1); }
.input-error  { font-size: var(--text-xs); color: var(--error); margin-top: var(--space-1); }

/* ── Select / dropdown ── */
.select-trigger {
  background: var(--bg-surface-2);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  padding: var(--space-3) var(--space-4);
  cursor: pointer;
}

.select-dropdown {
  background: var(--bg-surface-1);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}

.select-option:hover,
.select-option--highlighted {
  background: var(--bg-surface-2);
}
.select-option--selected { color: var(--primary); }

[data-theme="light"] .select-trigger { background: #FFFFFF; }
[data-theme="light"] .select-dropdown { background: #FFFFFF; box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
[data-theme="light"] .select-option:hover { background: var(--bg-surface-2); }

/* ── Checkbox ── */
.checkbox {
  width: 16px; height: 16px;
  border: 2px solid var(--border-default);
  border-radius: var(--radius-xs);
  background: transparent;
  cursor: pointer;
  transition: all 120ms;
}
.checkbox:checked {
  background: var(--primary);
  border-color: var(--primary);
}

/* ── Toggle switch ── */
.toggle-track {
  width: 40px; height: 22px;
  border-radius: var(--radius-full);
  background: var(--bg-surface-2);
  border: 1px solid var(--border-default);
  transition: background 200ms;
  cursor: pointer;
}
.toggle-track--on { background: var(--primary); border-color: var(--primary); }

/* ── File upload drop zone ── */
.file-drop {
  background: var(--bg-surface-2);
  border: 2px dashed var(--border-default);
  border-radius: var(--radius-lg);
  color: var(--text-muted);
  text-align: center;
  padding: var(--space-8);
  transition: border-color 150ms;
}
.file-drop:hover,
.file-drop--dragover {
  border-color: var(--primary);
  background: color-mix(in srgb, var(--primary) 5%, var(--bg-surface-2));
}

[data-theme="light"] .file-drop {
  background: var(--bg-surface-2);    /* #F1F5F9 */
  border-color: var(--border-default);
}
```

### Token Quick Reference

| Property | Dark | Light |
|---|---|---|
| Input bg | `--bg-surface-2` → `#131F38` | `#FFFFFF` |
| Input border | `--border-default` → `#334155` | `--border-default` → `#CBD5E1` |
| Input text | `--text-primary` → `#F1F5F9` | `--text-primary` → `#0F172A` |
| Input focus ring | `--primary` 20% glow | `--primary` 20% glow |
| Error border | `--error` → `#EF4444` | `--error` → `#DC2626` |
| Label | `--text-secondary` → `#94A3B8` | `--text-secondary` → `#475569` |
| Toggle on | `--primary` | `--primary` |
| Checkbox checked | `--primary` | `--primary` |
| Dropdown bg | `--bg-surface-1` | `#FFFFFF` |

---

## Validation Rules (Standard)

| Field | Validation |
|---|---|
| Mobile | 10 digits, starts with 6/7/8/9 |
| Email | Standard regex, lowercase |
| Name | Min 2 chars, max 100, no special chars except `.` `-` `'` |
| Date of birth | Valid date, not future, age within context range |
| Percentage | 0–100 |
| Pin code | 6 digits, valid Indian pincode |
| Aadhaar | 12 digits (display masked: `XXXX XXXX 1234`) |
| File size | Configurable per field, shown in helper text |
