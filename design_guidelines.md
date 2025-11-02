# Fashion Outfit Recommendation App - Design Guidelines

## Design Approach: Reference-Based (Fashion & Visual Discovery)
Drawing inspiration from **Pinterest's** visual discovery patterns, **Instagram's** photo-centric UX, and modern fashion e-commerce platforms. This creates a trendy, image-first experience that celebrates visual content while maintaining clean usability.

**Key Principles:**
- Image-first hierarchy: Clothing photos are the hero
- Clean, minimal UI that doesn't compete with fashion imagery
- Modern, on-trend aesthetic suitable for fashion context
- Smooth micro-interactions for premium feel

---

## Core Design Elements

### A. Color Palette

**Dark Mode (Primary):**
- Background: 220 15% 8% (deep charcoal with blue undertone)
- Surface: 220 12% 12% (elevated cards/panels)
- Surface hover: 220 10% 15%
- Primary brand: 280 65% 62% (vibrant purple - fashion-forward)
- Primary hover: 280 65% 58%
- Accent: 340 75% 58% (warm pink for CTAs)
- Text primary: 0 0% 98%
- Text secondary: 220 10% 65%
- Border: 220 15% 20%

**Light Mode:**
- Background: 0 0% 100%
- Surface: 0 0% 98%
- Primary brand: 280 70% 55%
- Accent: 340 70% 52%
- Text primary: 220 20% 12%
- Text secondary: 220 10% 45%
- Border: 220 15% 88%

### B. Typography

**Font Families:**
- Headlines: 'Inter' (Google Fonts) - 600-700 weight
- Body: 'Inter' (Google Fonts) - 400-500 weight
- Accent/CTAs: 'Inter' (Google Fonts) - 600 weight

**Scale:**
- Hero headline: text-5xl md:text-6xl font-bold
- Section headers: text-3xl md:text-4xl font-semibold
- Card titles: text-xl font-semibold
- Body text: text-base
- Labels/metadata: text-sm
- Captions: text-xs text-secondary

### C. Layout System

**Spacing Primitives:** Use Tailwind units of **2, 4, 6, 8, 12, 16, 20, 24** (p-4, gap-6, mb-8, py-12, etc.)

**Container Strategy:**
- Max-width: max-w-7xl for main content
- Section padding: px-4 md:px-8 lg:px-12
- Vertical rhythm: py-12 md:py-16 lg:py-20 for sections

**Grid Systems:**
- Clothing gallery: grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4
- Form sections: Single column on mobile, 2-column split on md+
- Recommendation display: grid-cols-1 md:grid-cols-2 lg:grid-cols-3

### D. Component Library

**Image Upload Zone:**
- Large dropzone area (min-h-64) with dashed border (border-2 border-dashed)
- Icon: Upload icon from Heroicons (cloud-arrow-up)
- Drag-and-drop active state with primary border and subtle background tint
- Image preview cards with rounded corners (rounded-2xl), aspect-square
- Delete button overlay on hover (top-right corner, small circular button)

**Input Forms:**
- Text inputs: h-12, rounded-xl, px-4, border with focus:ring-2 ring-primary
- Dropdowns/Selects: Custom styled with chevron-down icon, same styling as text inputs
- Gender selection: Pill-style toggle buttons (rounded-full, px-6 py-3)
- Occasion picker: Card-based selection grid with icons (Party, Work, Casual, Formal, Date, Sport)

**Clothing Type Tags:**
- Chip/badge style: rounded-full, px-4 py-2, text-sm
- Optional manual entry with autocomplete dropdown
- Auto-detected tags appear with subtle animation, different color treatment

**Action Buttons:**
- Primary CTA: Large (h-12 px-8), rounded-xl, font-semibold, accent gradient background
- Secondary: outline variant with border-2, same size
- Icon buttons: square (w-10 h-10), rounded-lg

**Outfit Recommendation Cards:**
- Large cards (rounded-2xl) with outfit combination images
- Multi-image layout showing 2-4 clothing items arranged visually
- Occasion badge at top-right
- Match score indicator (percentage or star rating)
- "Save combination" heart icon button

**Navigation:**
- Top nav: Sticky header with logo left, profile icon right
- Progress indicator: Step-based (1. Upload → 2. Details → 3. Recommendations)
- Back button always visible for multi-step flow

### E. Micro-Interactions

**Minimize animations** - use only for:
- Image upload: Subtle scale-up on drag-over
- Form validation: Smooth error message slide-in
- Card hover: Slight lift (translate-y-1) with shadow increase
- Loading states: Spinner or skeleton screens (no elaborate animations)

---

## Page Structure

### Hero/Welcome Section
- Full-width background with subtle gradient (primary to accent, 10% opacity)
- Centered content: Headline "Find Your Perfect Outfit" + tagline
- Primary CTA button: "Get Started"
- Hero decorative element: Abstract fashion illustration or geometric pattern (not photo)

### Main Workflow (Multi-step form):

**Step 1 - Upload Clothes:**
- Image upload grid (2x2 or 3x3 layout)
- Each slot is a distinct upload zone
- Preview grid below showing all uploaded items

**Step 2 - User Details:**
- Two-column layout (md+): Left = personal info, Right = occasion selector
- Name, age fields stacked
- Gender pills horizontally arranged
- Occasion cards in grid (2 columns on md, 3 on lg)

**Step 3 - Recommendations:**
- Header with user greeting and occasion context
- Grid of outfit combination cards
- Filter/sort options (Best Match, Most Casual, Most Formal)

---

## Images

**Hero Section:** Abstract fashion illustration or geometric pattern background (not realistic photo) - gives modern, editorial feel without competing with user-uploaded clothing images

**Occasion Cards:** Icon-based (not photos) - use Heroicons: briefcase (Work), sparkles (Party), sun (Casual), academic-cap (Formal), heart (Date), bolt (Sport)

**Clothing Items:** User-uploaded photos displayed in square aspect ratio cards with subtle shadow and rounded corners

**Outfit Recommendations:** Composite view showing 2-4 clothing items arranged in outfit formation (e.g., top over bottom, with accessories)

---

## Key UX Patterns

- **Progressive disclosure:** Show complexity gradually through multi-step form
- **Immediate feedback:** Show image previews instantly, validate inputs in real-time
- **Empty states:** Friendly illustrations/messages when no clothes uploaded or no recommendations yet
- **Mobile-first:** All interactions optimized for touch (44px minimum tap targets)
- **Accessibility:** High contrast ratios, clear focus states, keyboard navigation support