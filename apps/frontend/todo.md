# UILove Style Improvement TODO

## 🎨 Global Styles

### Colors & Theme
- [ ] Update background color from plain black to rich dark: `#09090b`
- [ ] Add CSS variables for consistent color palette:
  ```
  --bg-primary: #09090b
  --bg-secondary: #141416
  --bg-tertiary: #1c1c1f
  --accent: #8b5cf6
  --accent-hover: #a78bfa
  --text-primary: #fafafa
  --text-secondary: #a1a1aa
  --text-muted: #71717a
  --border-subtle: rgba(255,255,255,0.06)
  --border-hover: rgba(255,255,255,0.12)
  ```

### Typography
- [ ] Import modern font: Inter, Satoshi, or General Sans
- [ ] Set base font-size: 14px
- [ ] Set line-height: 1.6
- [ ] Add letter-spacing: -0.01em for headings
- [ ] Define typography scale (xs, sm, base, lg, xl, 2xl, 3xl, 4xl, 5xl)

### Transitions & Animations
- [ ] Add global transition: `transition: all 0.2s ease-out`
- [ ] Create fade-in animation for page loads
- [ ] Create slide-up animation for elements
- [ ] Create skeleton shimmer animation for loading states
- [ ] Add subtle hover scale: `transform: scale(1.02)`

### Spacing System
- [ ] Define spacing scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96px
- [ ] Set consistent container max-width: 1400px
- [ ] Set container padding: 24px (mobile), 48px (desktop)

---

## 📄 Page 1: Login Page (`/admin/login`)

### Layout
- [ ] Center card vertically AND horizontally (use min-h-screen + flex)
- [ ] Add max-width to card: 400px
- [ ] Add padding to card: 40px (currently too tight)
- [ ] Add margin around card for mobile: 20px

### Card Styling
- [ ] Add background: `rgba(255,255,255,0.02)`
- [ ] Add backdrop-blur: `backdrop-filter: blur(20px)`
- [ ] Add border: `1px solid rgba(255,255,255,0.06)`
- [ ] Add border-radius: 16px
- [ ] Add subtle box-shadow: `0 25px 50px -12px rgba(0,0,0,0.5)`

### Logo & Header
- [ ] Increase logo size: 48px icon
- [ ] Add margin-bottom to logo: 32px
- [ ] Style "Admin Panel" text: text-sm, text-zinc-500, letter-spacing: 0.1em
- [ ] Add subtle glow to sparkle icon

### Form Inputs
- [ ] Increase input height: 48px (currently too short)
- [ ] Add padding: 16px horizontal
- [ ] Add background: `#1c1c1f`
- [ ] Add border: `1px solid rgba(255,255,255,0.06)`
- [ ] Add border-radius: 10px
- [ ] Add focus state: `border-color: #8b5cf6; box-shadow: 0 0 0 3px rgba(139,92,246,0.1)`
- [ ] Add transition on focus: 0.2s ease
- [ ] Add placeholder color: `#52525b`
- [ ] Add spacing between inputs: 16px
- [ ] Add spacing between label and input: 8px
- [ ] Style labels: text-sm, font-medium, text-zinc-300

### Sign In Button
- [ ] Increase height: 48px
- [ ] Add gradient background: `linear-gradient(135deg, #8b5cf6, #7c3aed)`
- [ ] Add hover state: brighten + subtle scale(1.01)
- [ ] Add active state: scale(0.99)
- [ ] Add box-shadow: `0 4px 14px rgba(139,92,246,0.4)`
- [ ] Add font-weight: 600
- [ ] Add border-radius: 10px
- [ ] Add margin-top: 24px

### Back to Site Link
- [ ] Add margin-top: 24px
- [ ] Style: text-sm, text-zinc-500
- [ ] Add hover: text-zinc-300, underline
- [ ] Add transition: 0.2s

### Background Enhancement
- [ ] Add subtle gradient mesh or grid pattern
- [ ] OR add animated gradient blob in background (low opacity)

---

## 📄 Page 2: Admin Dashboard (`/admin/websites`)

### Sidebar
- [ ] Add padding: 20px
- [ ] Add gap between nav items: 4px
- [ ] Style nav items: padding 12px 16px, border-radius 8px
- [ ] Add hover state: background rgba(255,255,255,0.04)
- [ ] Add active state: background rgba(139,92,246,0.1), text accent color
- [ ] Add left border on active: 2px solid #8b5cf6
- [ ] Add icon size: 18px
- [ ] Add gap between icon and text: 12px
- [ ] Add section dividers if needed

### Header Bar
- [ ] Add padding: 24px 32px
- [ ] Add border-bottom: 1px solid rgba(255,255,255,0.06)
- [ ] Style breadcrumb: text-sm, text-zinc-500, arrow icon smaller
- [ ] Move user email/logout to right side properly
- [ ] Add avatar placeholder circle before email
- [ ] Style logout button: text-zinc-500, hover text-red-400

### Page Title Section
- [ ] Add padding: 32px
- [ ] Add margin-bottom: 24px
- [ ] Style "Websites" heading: text-2xl, font-semibold
- [ ] Add description text below if needed

### Add Website Button
- [ ] Add padding: 10px 20px
- [ ] Add border-radius: 8px
- [ ] Add gradient or solid accent background
- [ ] Add hover brightness
- [ ] Add icon size: 16px
- [ ] Add gap: 8px
- [ ] Add font-weight: 500

### Search Input
- [ ] Add width: 300px (or responsive)
- [ ] Add height: 40px
- [ ] Add padding: 12px 16px
- [ ] Add search icon inside (left)
- [ ] Add background: #141416
- [ ] Add border: 1px solid rgba(255,255,255,0.06)
- [ ] Add border-radius: 8px
- [ ] Add placeholder: "Search websites..."
- [ ] Add focus ring

### Data Table
- [ ] Add margin: 0 32px 32px 32px
- [ ] Add background to table container: #0d0d0f
- [ ] Add border: 1px solid rgba(255,255,255,0.06)
- [ ] Add border-radius: 12px
- [ ] Add overflow: hidden

### Table Header
- [ ] Add background: rgba(255,255,255,0.02)
- [ ] Add padding: 16px 20px
- [ ] Style text: text-xs, uppercase, letter-spacing 0.05em, text-zinc-500
- [ ] Add border-bottom: 1px solid rgba(255,255,255,0.06)

### Table Rows
- [ ] Add padding: 16px 20px
- [ ] Add min-height: 72px
- [ ] Add border-bottom: 1px solid rgba(255,255,255,0.04)
- [ ] Remove border on last row
- [ ] Add hover background: rgba(139,92,246,0.03)
- [ ] Add transition: background 0.15s ease
- [ ] Add left border on hover: 3px solid #8b5cf6 (with padding adjust)

### Thumbnail Images
- [ ] Add width/height: 56px x 40px (or 64x45 for 16:10)
- [ ] Add border-radius: 6px
- [ ] Add object-fit: cover
- [ ] Add border: 1px solid rgba(255,255,255,0.06)
- [ ] Add hover: ring-2 ring-accent/30

### Website Name Cell
- [ ] Style name: font-medium, text-zinc-100
- [ ] Style slug: text-xs, text-zinc-500
- [ ] Add gap: 4px

### Status Badge
- [ ] Add padding: 4px 10px
- [ ] Add border-radius: 9999px (pill)
- [ ] Add background: rgba(34,197,94,0.1) for Normal
- [ ] Add text color: #4ade80 for Normal
- [ ] Add font-size: 12px
- [ ] Add font-weight: 500

### Views Count
- [ ] Add tabular-nums font feature
- [ ] Style: text-zinc-400

### Date
- [ ] Style: text-sm, text-zinc-500
- [ ] Format: "Feb 10, 2026" (nice format)

### Action Buttons
- [ ] Add icon size: 18px
- [ ] Add padding: 8px
- [ ] Add border-radius: 6px
- [ ] Add hover background: rgba(255,255,255,0.06)
- [ ] Add gap between buttons: 4px
- [ ] Add transition: 0.15s
- [ ] Add tooltip on hover

### Empty State (if no data)
- [ ] Design empty state with illustration
- [ ] Add "No websites yet" message
- [ ] Add CTA button to add first website

### Pagination (if exists)
- [ ] Add padding: 16px 20px
- [ ] Add border-top: 1px solid rgba(255,255,255,0.06)
- [ ] Style page numbers with hover states
- [ ] Style prev/next buttons

---

## 📄 Page 3: Homepage / Gallery (`/`)

### Navigation Bar
- [ ] Add height: 64px
- [ ] Add padding: 0 48px
- [ ] Add position: sticky, top: 0
- [ ] Add background on scroll: rgba(9,9,11,0.8)
- [ ] Add backdrop-blur on scroll: 12px
- [ ] Add border-bottom on scroll: 1px solid rgba(255,255,255,0.06)
- [ ] Add z-index: 50
- [ ] Add transition for scroll effects

### Logo
- [ ] Add size: 32px icon
- [ ] Add gap from text: 10px
- [ ] Add font-weight: 700 for "UILove"
- [ ] Add hover: subtle glow/opacity change

### Nav Links
- [ ] Add gap between links: 32px
- [ ] Add font-size: 14px
- [ ] Add font-weight: 500
- [ ] Add color: text-zinc-400
- [ ] Add hover: text-white
- [ ] Add active: text-white + underline accent
- [ ] Add transition: 0.2s

### Search Icon
- [ ] Add size: 20px
- [ ] Add padding: 8px
- [ ] Add hover: background rgba(255,255,255,0.06), border-radius 6px

### Hero Section
- [ ] Add padding: 80px 48px 48px
- [ ] Add text-align: center
- [ ] Add max-width: 800px, margin: auto

### Hero Title
- [ ] Add font-size: 56px (or clamp for responsive)
- [ ] Add font-weight: 700
- [ ] Add letter-spacing: -0.02em
- [ ] Add line-height: 1.1
- [ ] Add gradient text for "Landing Pages": accent gradient
- [ ] Add margin-bottom: 20px

### Hero Subtitle
- [ ] Add font-size: 18px
- [ ] Add color: text-zinc-400
- [ ] Add max-width: 600px
- [ ] Add margin: 0 auto 40px

### Category Tags Row
- [ ] Add padding: 0 48px
- [ ] Add gap: 12px
- [ ] Add flex-wrap: wrap
- [ ] Add justify-content: center
- [ ] Add margin-bottom: 48px

### Category Tag Pills
- [ ] Add padding: 8px 16px
- [ ] Add border-radius: 9999px
- [ ] Add background: rgba(255,255,255,0.04)
- [ ] Add border: 1px solid rgba(255,255,255,0.06)
- [ ] Add font-size: 13px
- [ ] Add color: text-zinc-400
- [ ] Add hover: background rgba(139,92,246,0.1), border-color rgba(139,92,246,0.3), color white
- [ ] Add active state: background accent, color white
- [ ] Add transition: 0.2s

### Sidebar Categories
- [ ] Add width: 220px
- [ ] Add padding: 24px
- [ ] Add position: sticky, top: 80px
- [ ] Add max-height: calc(100vh - 100px)
- [ ] Add overflow-y: auto
- [ ] Add custom scrollbar styling

### Category List Items
- [ ] Add padding: 10px 12px
- [ ] Add border-radius: 6px
- [ ] Add font-size: 14px
- [ ] Add display: flex, justify-content: space-between
- [ ] Add hover: background rgba(255,255,255,0.04)
- [ ] Add active: background rgba(139,92,246,0.1), text accent

### Category Count
- [ ] Add font-size: 12px
- [ ] Add color: text-zinc-600
- [ ] Add tabular-nums

### Website Grid
- [ ] Add display: grid
- [ ] Add grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))
- [ ] Add gap: 24px
- [ ] Add padding: 0 24px 48px

### Website Card
- [ ] Add background: #141416
- [ ] Add border: 1px solid rgba(255,255,255,0.06)
- [ ] Add border-radius: 12px
- [ ] Add overflow: hidden
- [ ] Add transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s
- [ ] Add hover: transform translateY(-4px)
- [ ] Add hover: box-shadow 0 20px 40px rgba(0,0,0,0.4)
- [ ] Add hover: border-color rgba(139,92,246,0.3)

### Card Image
- [ ] Add aspect-ratio: 16/10
- [ ] Add object-fit: cover
- [ ] Add width: 100%
- [ ] Add transition: transform 0.3s
- [ ] Add hover (parent): transform scale(1.03)

### Card Image Overlay (on hover)
- [ ] Add gradient overlay: linear-gradient(transparent 50%, rgba(0,0,0,0.8))
- [ ] Add opacity: 0 → 1 on hover
- [ ] Add transition: 0.3s

### Card Content
- [ ] Add padding: 16px
- [ ] Add display: flex
- [ ] Add justify-content: space-between
- [ ] Add align-items: center

### Card Title
- [ ] Add font-size: 15px
- [ ] Add font-weight: 600
- [ ] Add color: white
- [ ] Add truncate if too long

### Card Meta (views, date)
- [ ] Add display: flex
- [ ] Add gap: 12px
- [ ] Add font-size: 12px
- [ ] Add color: text-zinc-500
- [ ] Add align-items: center

### View Icon
- [ ] Add size: 14px
- [ ] Add margin-right: 4px

### Loading Skeleton
- [ ] Add skeleton cards while loading
- [ ] Add shimmer animation
- [ ] Add same dimensions as real cards

### Scroll Animations
- [ ] Add fade-in-up animation on scroll for cards
- [ ] Add stagger delay: each card 50ms
- [ ] Use Intersection Observer

---

## 📱 Responsive Design

### Mobile (< 768px)
- [ ] Stack sidebar below header on admin
- [ ] Full-width cards on gallery
- [ ] Hamburger menu for navigation
- [ ] Reduce padding: 16-20px
- [ ] Reduce font sizes slightly
- [ ] Hide category sidebar, show as dropdown

### Tablet (768px - 1024px)
- [ ] 2-column grid for gallery
- [ ] Collapsible sidebar on admin
- [ ] Adjust padding: 24-32px

### Desktop (> 1024px)
- [ ] 3-4 column grid for gallery
- [ ] Full sidebar on admin
- [ ] Max-width containers

---

## ✨ Nice-to-Have Enhancements

### Micro-interactions
- [ ] Button press effect (scale 0.98)
- [ ] Input focus ring animation
- [ ] Card hover lift effect
- [ ] Checkbox/toggle animations
- [ ] Toast notification animations

### Loading States
- [ ] Skeleton screens for all pages
- [ ] Button loading spinners
- [ ] Progress indicators

### Dark Mode Polish
- [ ] Subtle noise texture overlay (very low opacity)
- [ ] Gradient accent glows
- [ ] Smooth color transitions

### Accessibility
- [ ] Focus visible states
- [ ] Proper contrast ratios
- [ ] Keyboard navigation
- [ ] ARIA labels

---

## 📦 Implementation Priority

### Phase 1: Foundation (Do First)
1. Global CSS variables
2. Typography system
3. Spacing system
4. Base transitions

### Phase 2: Critical Pages
1. Login page (quick win, high visibility)
2. Homepage hero + cards
3. Admin table

### Phase 3: Polish
1. Hover states everywhere
2. Animations
3. Loading states
4. Responsive fixes

### Phase 4: Extras
1. Micro-interactions
2. Empty states
3. Error states
4. Final polish

---

## 🛠 Suggested Tech/Tools

- **CSS Framework**: Tailwind CSS (if not using already)
- **Animations**: Framer Motion (React) or CSS keyframes
- **Icons**: Lucide Icons or Phosphor Icons
- **Fonts**: Google Fonts (Inter) or Fontshare (Satoshi)
