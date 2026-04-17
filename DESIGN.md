# Biyuyo ERP - Design System

## 1. Design Tokens

### Colors

| Token               | Value     | Usage                                       |
| ------------------- | --------- | ------------------------------------------- |
| `--color-primary`   | `#004f39` | Primary color, primary buttons, headings    |
| `--color-secondary` | `#4da167` | Secondary color, accents, active states     |
| `--color-white`     | `#fffaca` | Light backgrounds, text on dark backgrounds |
| `--color-dark`      | `#151613` | Primary text, dark backgrounds              |

### Typography

| Token                   | Value                                         | Usage                     |
| ----------------------- | --------------------------------------------- | ------------------------- |
| `--default-font-family` | `Work Sans, Helvetica, sans-serif, monospace` | Body, general text        |
| `--font-heading`        | `Plus Jakarta Sans`                           | Headings, headers (h1-h3) |

### Radii

| Token         | Value  | Usage                    |
| ------------- | ------ | ------------------------ |
| `--radius`    | `1rem` | Standard rounded corners |
| `--radius-lg` | `2rem` | Large cards, modals      |
| `--radius-xl` | `3rem` | Special containers       |

### Transitions

| Token                           | Value  | Usage               |
| ------------------------------- | ------ | ------------------- |
| `--default-transition-duration` | `0.2s` | Default transitions |

---

## 2. Existing Base Components

### BaseButton

Versatile button with color variants.

**Props:**

```typescript
interface Props {
	text: string;
	variant?: "primary" | "secondary" | "outlined" | "inverted";
	type?: "button" | "submit" | "reset";
	width?: "full" | "auto";
	to?: string;
}
```

**Variants:**

- `primary`: `bg-primary text-white hover:bg-secondary` (default)
- `secondary`: `bg-secondary text-white hover:bg-primary`
- `outlined`: `border border-secondary text-primary hover:bg-secondary hover:text-white`
- `inverted`: `bg-dark text-white hover:bg-white hover:text-dark`

**Base class:** `py-2 px-4 rounded-full cursor-pointer`

---

### BaseInput

Basic form input.

**Props:**

```typescript
interface Props {
	type?: "text" | "email" | "password";
	placeholder?: string;
	name?: string;
	modelValue?: string | number;
}
```

**Base class:** `py-2 px-4 rounded-xl border border-secondary text-primary`

**Events:** `update:modelValue`

---

### BaseCard

Versatile container with color variants.

**Props:**

```typescript
interface Props {
	variant?: "primary" | "secondary" | "outlined" | "inverted";
}
```

**Variants:**

- `primary`: `bg-primary` (default)
- `secondary`: `bg-secondary`
- `outlined`: `border border-secondary bg-white`
- `inverted`: `bg-dark text-white`

**Base class:** `rounded-xl p-8 shadow-sm`

---

### BaseNav

Flexbox navigation container.

**Base class:** `w-full flex justify-start items-center gap-8`

**Slots:** default

---

### NavItem

Navigation item.

**Base class:** `flex justify-start items-center gap-4`

**Slots:** default

---

## 3. Naming Conventions

### Components

- Prefix `Base` for fundamental components: `BaseButton`, `BaseInput`, `BaseTable`
- PascalCase names: `PageHeader`, `FormField`
- Suffix for types: `ListView`, `ShowView`, `CreateView`, `EditView`

### Props

- Use `modelValue` for v-model (Vue 3)
- camelCase names
- Boolean props with `?` suffix in TypeScript

### CSS Classes

- Prefer Tailwind utility classes
- Create custom classes only for complex cases
- Use CSS variables defined in tokens
