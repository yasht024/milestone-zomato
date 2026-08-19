---
name: Nocturne Dining
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#e4bebc'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#ab8987'
  outline-variant: '#5b403f'
  surface-tint: '#ffb3b1'
  primary: '#ffb3b1'
  on-primary: '#680011'
  primary-container: '#ff535a'
  on-primary-container: '#5b000e'
  inverse-primary: '#bb162c'
  secondary: '#c4c7c9'
  on-secondary: '#2d3133'
  secondary-container: '#464a4b'
  on-secondary-container: '#b6b9bb'
  tertiary: '#b9c8de'
  on-tertiary: '#233143'
  tertiary-container: '#8392a6'
  on-tertiary-container: '#1c2b3c'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#e0e3e5'
  secondary-fixed-dim: '#c4c7c9'
  on-secondary-fixed: '#191c1e'
  on-secondary-fixed-variant: '#444749'
  tertiary-fixed: '#d4e4fa'
  tertiary-fixed-dim: '#b9c8de'
  on-tertiary-fixed: '#0d1c2d'
  on-tertiary-fixed-variant: '#39485a'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1200px
  gutter: 24px
  margin-mobile: 20px
  margin-desktop: 40px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style

The design system is centered on a premium, late-night aesthetic designed for the discerning diner. It leverages a **Glassmorphic** design style underpinned by **Minimalism** to ensure the AI-driven recommendations remain the focal point. The atmosphere is sophisticated and high-fidelity, evoking the feeling of a dimly lit, high-end bistro.

The emotional response should be one of confidence, exclusivity, and technological ease. By combining deep, obsidian-like surfaces with vibrant crimson accents, the UI creates a high-contrast environment that feels both cutting-edge and inviting.

## Colors

The palette is anchored in a "Deep Slate" spectrum to provide maximum depth.
- **Primary (#E23744):** Used sparingly for critical calls to action, active states, and AI-highlighted recommendations.
- **Neutral/Background:** The foundation uses Slate-950 (#020617) for the base canvas to allow glass layers to pop.
- **Glass Surfaces:** A translucent Slate-800 mix with a 12px to 20px backdrop blur creates the signature high-end feel.
- **Accents:** Use pure white (#FFFFFF) for primary text and Slate-400 (#94A3B8) for secondary metadata to maintain a clean hierarchy.

## Typography

This design system utilizes **Outfit** for all display and headline roles to provide a modern, geometric character. **Inter** is utilized for body copy and UI labels to ensure maximum legibility and a systematic feel. 

Large headlines should use tighter letter-spacing to appear more "editorial." For mobile screens, headlines scale down to prevent awkward line breaks, while body text remains legible at 16px. Use the "uppercase" label style for category tags or small metadata headers to add a premium touch.

## Layout & Spacing

The layout follows a **Fluid Grid** model with a focus on generous negative space to emphasize high-quality food photography.
- **Desktop:** 12-column grid with a 1200px max-width container. 24px gutters.
- **Tablet:** 8-column grid with 20px margins.
- **Mobile:** 4-column grid with 20px margins.

Spacing follows an 8px base unit. Vertical rhythm is established using "Stack" variables: 12px for related elements (title/subtitle), 24px for component groups (card content), and 48px for section separation.

## Elevation & Depth

Depth is achieved through **Glassmorphism** rather than traditional heavy shadows.
- **Base Layer:** Pure dark background (Slate-950).
- **Surface Layer:** 70% opacity Slate-800 with a 20px `backdrop-filter: blur()`.
- **Borders:** "Ghost borders"—1px solid lines with 10% white opacity—define the edges of glass containers without adding visual weight.
- **Active Elevation:** When hovered, cards should transition to a 15% white border opacity and trigger a subtle primary color outer glow (`box-shadow: 0 0 20px rgba(226, 55, 68, 0.2)`).

## Shapes

The shape language is consistently **Rounded**, striking a balance between approachable and professional. 
- Elements like cards and input fields use a `0.5rem` radius.
- Interactive elements like badges, chips, and primary buttons use **Pill-shaped** (Full radius) geometry to distinguish them from structural containers.
- High-fidelity images should mirror the card's 0.5rem radius or use a slightly smaller 0.25rem radius when nested.

## Components

### Buttons
Primary buttons are pill-shaped, using the Primary Red hex with white text. Apply a subtle "inner-glow" effect (white 10% overlay) on top to simulate a physical sheen. Secondary buttons are ghost-style with a semi-transparent white border.

### Glass Cards
The core of the experience. Cards should have a 1px border (`rgba(255,255,255,0.1)`) and a background blur. On hover, the card should lift 4px upward with a smooth 300ms transition.

### Pill Badges
Used for cuisine types or AI tags (e.g., "Highly Rated"). These are small, pill-shaped elements with a low-opacity Primary Red background and solid Primary Red text.

### Input Fields
Dark, semi-transparent backgrounds with a 1px border that glows Primary Red when focused. Typography inside inputs should be Inter Body-MD.

### AI-Recommendation Highlighting
Special "Hero" cards for AI picks should feature a subtle, slow-moving radial gradient border in Primary Red to signify "intelligence" and premium value.

### Micro-animations
- **Hover Lifts:** 4px Y-axis translation for cards.
- **Glow States:** Soft Primary Red outer glow for active navigation items.
- **Fade-in:** Glass elements should use a staggered fade-in with a slight blur reduction for entry transitions.