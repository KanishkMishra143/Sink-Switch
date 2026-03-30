# Instructions for Replicating "The Digital Vault" Design System

This document provides the exhaustive technical and design blueprint for replicating the high-end, editorial landing page and multi-page wiki created for **NotionSafe**. 

---

## 1. Design Philosophy: "The Digital Vault"
The goal is an interface that feels architectural, secure, and intentionally quiet. It rejects "SaaS dashboard" clichés in favor of tactile, custom surfaces.

### The "No-Line" Rule
*   **Mandate**: Never use `1px solid` borders for sectioning or sidebars.
*   **Execution**: Use background luminance shifts. A 2-3% difference between `surface` and `surface-container` is sufficient for the eye to perceive boundaries without visual noise.

### Surface Hierarchy (Tonal Depth)
Define 5-6 levels of surfaces to create physical nesting:
1.  **Base**: `surface` (The foundation).
2.  **Secondary**: `container-low` (Alternating sections).
3.  **Active/Hover**: `container-lowest` (Highest contrast, pure white/black).
4.  **Defined**: `container-high` (Visible cards in light mode, sidebars).
5.  **Accent**: `container-highest` (Inputs, search bars).

### Elevation & Hover States
*   **Static States**: Cards should have a subtle, soft shadow (`box-shadow: 0 4px 12px rgba(0,0,0,0.08)`).
*   **Hover Behavior**: Do **not** lift or gray-out cards. Instead, make a **1px primary-colored border** appear. This signifies technical precision.

---

## 2. Visual Identity & Assets

### Image "Halo" Effect
Images should never sit flat on a background. Wrap them in a `.halo-effect` container:
*   **CSS**: Use `::after` with a `radial-gradient` of the primary color, high `blur` (40px-60px), and low `opacity` (0.15-0.35).
*   **Container**: Must have `overflow: visible` to ensure the glow isn't clipped.

### Circular Branding
*   Favicons and footer logos must be circular. 
*   **Technical Tip**: While CSS `border-radius: 50%` works for on-page images, the browser tab icon (favicon) **must** be a circular-cropped file (e.g., `logo_round.png`).

---

## 3. The Technical Blueprint (Performance & Stability)

### Robust Flash Prevention (Theme Logic)
To prevent the "white flash" during page loads in Dark Mode:
1.  **Head Script**: Place a blocking script immediately in the `<head>` before any content or CSS. 
    ```javascript
    (function() {
      const theme = localStorage.getItem('theme') || 'light';
      if (theme === 'dark') document.documentElement.classList.add('dark-theme');
    })();
    ```
2.  **Root Background**: Define `html.dark-theme { background-color: #0e1011; }` in CSS so the browser paints the dark color before the body renders.
3.  **Instant Toggle**: Toggle the class on `document.documentElement`, not `document.body`, to ensure header transparency and layout updates happen in perfect sync.

### Header Transparency
*   Use `backdrop-filter: blur(20px)` and an `rgba` background color on the sticky header.
*   **Selector**: Define specific `rgba` values for `.dark-theme header` vs default to ensure the blur matches the surface color.

---

## 4. Multi-Page Wiki Architecture

### 3-Column Layout
*   **Structure**: `[240px Sidebar] | [1fr Content] | [240px Navigator]`.
*   **Focus**: This centers the reading area while keeping tools accessible at the edges.

### Dynamic "On This Page" Navigator
*   **Logic**: Use JS to query `.docs-content` for `h2` and `h3` tags.
*   **Precision**: Use `scroll-margin-top: 100px` on all headings to prevent the sticky header from cutting off text when jumping to anchors.
*   **Active State**: Use `window.addEventListener('scroll')` to highlight the current section in the right navigator.

### Global Multi-Page Search
Instead of a simple sidebar filter, implement a **Global Indexing Search**:
1.  **Indexing**: On search trigger, use `fetch()` to grab the HTML of all wiki pages.
2.  **Parsing**: Use `DOMParser` to extract searchable content (`h2, h3, p, li`) into a JSON object.
3.  **UI**: Display results in a **Modal** with blurred background. Provide snippets and links that jump to the exact anchor (`#heading-id`).

---

## 5. Typography Standards
*   **Font**: Inter (Primary) + JetBrains Mono (Code).
*   **Display**: Large headlines (`2.5rem`) with tightened letter-spacing (`-0.02em`).
*   **Body**: Comfortable reading size (`1rem` / `16px`) with generous line-height (`1.6`).
*   **Labels**: Uppercase, tracked out (`0.05em`) labels for secondary metadata.

---

## 6. CSS Reference (The "Digital Vault" Variables)
```css
:root {
  --surface: #f9f9fb;
  --surface-container-high: #e8e8eb; /* Critical for card visibility in light mode */
  --primary: #0058a0;
  --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.dark-theme {
  --surface: #0e1011;
  --on-surface: #e2e2e6;
  --primary: #7eb6ff; /* Softer periwinkle for dark mode links */
}
```

*By following these instructions, any AI agent can replicate the specific high-fidelity look and performance-optimized behavior of the NotionSafe site.*

---

## 7. Automated Deployment (GitHub Actions)
To maintain a seamless sync between the `site/` directory and the live landing page:
*   **Workflow**: Create `.github/workflows/deploy-site.yml`.
*   **Triggers**: Set to run on `push` to `master` with a filter on the `site/**` path.
*   **Actions**:
    1.  Use `actions/checkout` to pull the code.
    2.  Use `actions/upload-pages-artifact` pointing to the `./site` directory.
    3.  Use `actions/deploy-pages` to push to the `github-pages` environment.
*   **Permissions**: Ensure the workflow has `pages: write` and `id-token: write` permissions.

---

## 8. Responsiveness Strategy: "The Fluid Vault"
While the design is architectural, it must adapt gracefully to mobile (Android/iOS) and tablets.

### Universal Container Padding
*   **Mandate**: Never let text touch the edge of a mobile screen.
*   **Execution**: In the `768px` media query, set `.container { padding: 0 var(--space-5); }`. This provides a consistent 2rem "breathing room" on small devices.

### Mobile Navigation (The Hamburger)
*   **HTML**: Add a `button#mobile-menu-toggle` with a menu icon (Lucide-style).
*   **CSS**:
    *   Hide the toggle by default (`display: none`).
    *   Show on mobile (`display: flex`) and hide standard `.nav-links`.
    *   Position `.nav-links.active` as a full-width absolute dropdown below the header with a solid background and shadow.
*   **JS**: Add a simple toggle listener that switches between `menu` and `x` (close) icons and toggles the `.active` class on the nav links.

### Solid vs. Gradient Primary Actions
*   **Guidance**: For the primary "Get Started" call-to-action, use a **solid background color** (`var(--primary)`) rather than a gradient. This ensures maximum legibility and a cleaner, more "vault-like" technical appearance across all screen types.

### Header Separation on Mobile
*   **Execution**: Add a `1px solid` border to the bottom of the header (`border-bottom: 1px solid var(--outline-variant)`) and increase background opacity to `0.9` in dark mode. This prevents the header from "melting" into the background when scrolling through content-heavy documentation or hero sections.

### Scaling Typography & Spacing
*   **Scale Down**: Reduce the base spacing variable `--space-8` from `4rem` to `3rem` on mobile to keep vertical gaps proportional.
*   **Hero Visuals**: Use `flex-direction: column` for hero images and process steps on mobile to ensure screenshots remain large and legible.

---

## 9. Evolution: "The Tonal Vault" (Professional & Colorful)
When a more vibrant, Material You-inspired design is requested, follow these supplemental rules to balance professionalism with color.

### Tonal Surface Palette
Move away from neutral grays to **Azure/Midnight Slate tints**.
*   **Light Mode**: Use a faint sapphire tint for the base (`#f8fafc`) and secondary surfaces (`#f1f5f9`).
*   **Dark Mode**: Use a deep Midnight Navy (`#0b0f1a`) instead of pure obsidian. This creates a "premium night" feel.

### Material 3 Geometry & Spacing
*   **Radii**: Increase card and button border-radius to `1.25rem` or `1.5rem` for a softer, modern appearance.
*   **Aggressive Compactness**: Reduce global spacing variables (e.g., `--space-8` at `2rem`) to eliminate dead space. 
*   **Card Padding**: Use a tighter `1rem` to `1.25rem` padding for guide cards and small callouts.

### Accent Layering (The "Pop" Factor)
*   **Multi-color Halos**: Instead of a single primary glow, use a `radial-gradient` mix of Sapphire (`--primary`), Teal (`--secondary`), and Violet (`--tertiary`) at low opacity.
*   **Cycling Borders**: For grid sections, give cards a `4px solid` top-border that cycles through the three accent colors.
*   **Vibrant Gradients**: Apply 135deg linear gradients to primary actions (Sapphire to Indigo) and the logo span (Sapphire to Violet).

### High-End Glassmorphism
*   **Header**: Increase `backdrop-filter: blur` to `24px` and use a tinted `rgba` background (80-85% opacity).
*   **Sidebars**: Use a translucent, tinted background with a subtle border and blur to make the docs feel like a physical layer above the content.
