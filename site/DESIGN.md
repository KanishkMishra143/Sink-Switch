# Sink-Switch Design System: "The Tonal Vault"

This document defines the professional yet colorful design system used for Sink-Switch. It combines architectural precision with Material 3 (M3) inspiration to create an interface that feels secure, modern, and vibrant.

---

## 1. Color Palette: Tonal Azure & Midnight Slate

Instead of neutral grays, we use **Tonal Surfaces** tinted with sapphire to create depth and cohesion.

### Light Mode
*   **Surface (Base)**: `#f8fafc` (Faint Azure tint)
*   **Surface Low**: `#f1f5f9` (Tinted slate for section backgrounds)
*   **Primary (Action)**: `#2563eb` (Sapphire Blue)
*   **Secondary (Accent)**: `#0d9488` (Teal)
*   **Tertiary (Accent)**: `#7c3aed` (Violet)

### Dark Mode
*   **Surface (Base)**: `#0b0f1a` (Midnight Navy)
*   **Surface Low**: `#161e2e` (Deep Navy tint)
*   **Primary (Action)**: `#60a5fa` (Azure Blue)
*   **Secondary (Accent)**: `#2dd4bf` (Teal)

---

## 2. Geometry & Spacing

### M3 Geometry
*   **Radii**: Larger, softer corners for a friendly, modern feel.
    *   `--radius-sm`: `0.75rem` (Internal elements)
    *   `--radius-md`: `1.25rem` (Cards, Buttons)
    *   `--radius-lg`: `2rem` (Sections, Hero containers)

### Aggressive Compactness
To eliminate "dead space," vertical gaps are kept tight:
*   **Small Gaps**: `0.75rem` to `1rem`
*   **Medium Gaps**: `1.25rem`
*   **Large Section Gaps**: `2rem`
*   **Card Padding**: Tight `1rem` for documentation guides and sidebars.

---

## 3. UI Components & Patterns

### Tonal Card System
*   **Execution**: Cards use a `4px solid` top border that cycles through the accent colors (Sapphire, Teal, Violet).
*   **Hover State**: Cards translate `-4px` vertically and transition from `Surface Low` to `Surface Lowest` (pure white/black) for an "active" feel.

### Multi-Accent Gradients
*   **Primary Buttons**: `135deg` gradient from Sapphire Blue to Indigo.
*   **Logo Text**: `135deg` gradient from Sapphire Blue to Violet.
*   **Halo/Glow Effects**: Multi-color `radial-gradients` using both Primary and Secondary colors at low opacity (15-25%) with high blur (50px+).

### Glassmorphism
*   **Sticky Header**: `24px` backdrop blur with an `rgba` background (80% opacity) of the surface color.
*   **Wiki Sidebars**: Translucent backgrounds with subtle `backdrop-filter` and tinted borders to separate tools from the main reading area.

---

## 4. Typography Standards

*   **Font Family**: Inter (Primary) + JetBrains Mono (Code).
*   **Headlines**: High-contrast weights (`800`) with tightened letter-spacing (`-0.03em`).
*   **Badges**: Pill-shaped, uppercase labels with `700` weight and `0.05em` tracking.

---

## 5. Spacing Refinements (Doc Specific)

*   **Heading Gaps**: Documentation headings (`h2, h3`) use a compact `1.25rem` top margin.
*   **Footer Clearance**: The `.docs-container` maintains a `2rem` bottom padding to ensure content never feels merged with the footer.
