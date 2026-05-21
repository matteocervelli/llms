# Frontend Design HTML Skill

Create distinctive, production-grade HTML/CSS + vanilla JavaScript frontends with exceptional design quality. This skill combines the 5-dimension aesthetic framework with semantic HTML5, modern CSS, and CSS-only animations.

## Overview

This skill enables you to:

- Design interfaces with intentional, non-generic aesthetics
- Build semantic HTML5 structures for accessibility
- Implement sophisticated CSS layouts (Grid, Flexbox)
- Create orchestrated CSS animations without JavaScript libraries
- Ensure WCAG 2.1 Level AA accessibility compliance
- Develop responsive, mobile-first interfaces
- Apply the complete 5-dimension design framework

## Quick Start

### Before Coding: Complete Design Thinking

Use the design thinking worksheet in SKILL.md to establish:

1. **Purpose**: What problem are you solving? Who are the users?
2. **Tone**: What emotional response should the design evoke?
3. **Constraints**: What are your technical, temporal, and business limits?
4. **Differentiation**: What one unforgettable element makes this uniquely yours?

### Project Structure

```html
<!-- Semantic HTML5 -->
<header><!-- Logo, primary nav --></header>
<nav><!-- Navigation --></nav>
<main>
  <article>
    <section><!-- Content --></section>
  </article>
  <aside><!-- Secondary content --></aside>
</main>
<footer><!-- Footer content --></footer>
```

```css
/* CSS Custom Properties for theming */
:root {
  --color-primary: #2d3748;
  --font-display: 'Playfair Display', serif;
  --space-md: 1rem;
}

/* CSS Grid for layout */
body {
  display: grid;
  grid-template-columns: 1fr minmax(0, 64rem) 1fr;
}

/* CSS Animations */
@keyframes slideInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

## The 5 Aesthetic Dimensions

### 1. Typography Dimension

**Distinctive typeface selection** is the foundation of personality.

**Do**:
- Playfair Display + IBM Plex Sans (elegant + warm)
- Crimson Pro + Space Grotesk (literary + geometric)
- Bricolage Grotesque + JetBrains Mono (handcrafted + technical)
- Use weight extremes (300, 700, 900)
- Use size jumps of 3x+ (96px display, 48px headline, 16px body)

**Don't**:
- Inter, Roboto, Open Sans (all generic defaults)
- Mid-range weights only (400, 500, 600)
- Incremental size scaling (48px, 40px, 32px)

### 2. Color & Theme Dimension

**Cohesive, unexpected color palettes** create mood and personality.

**Do**:
- Define color intent (warm, cool, energetic, calm)
- Use CSS variables for theming
- Reserve one unexpected accent color
- Create contrast through saturation

**Don't**:
- Material Design trinity (blue, red, green)
- Pure grays without personality (#999999, #CCCCCC)
- Oversaturated accents at 100%
- Monochrome everything

### 3. Motion Dimension

**Orchestrated animations** guide attention and reveal personality.

**Do**:
- CSS-only animations (no JS libraries)
- Staggered page loads with animation-delay
- Easing functions (ease-out, cubic-bezier)
- Scroll triggers with Intersection Observer
- Delightful hover states

**Don't**:
- Linear timing (feels robotic)
- Instant interactions (feels cold)
- Animation-heavy design that distracts
- Slow animations >1s

### 4. Spatial Composition Dimension

**Asymmetrical, intentional layouts** create visual rhythm.

**Do**:
- Asymmetrical layouts (more interesting)
- Generous whitespace
- Consistent spacing scale (8px, 16px, 24px, etc.)
- Grid-breaking elements
- Odd-numbered layouts (3, 5, 7)

**Don't**:
- Everything centered
- Uniform padding everywhere
- "Generic SaaS" arrangements
- Cramped whitespace

### 5. Backgrounds & Visual Details Dimension

**Atmospheric foundations** transform generic designs into memorable ones.

**Do**:
- Subtle gradients (2-3 colors, 40-60° angle)
- Texture overlays (2-5% opacity)
- Custom patterns or illustrations
- Micro-details that reward observation

**Don't**:
- Bland white backgrounds
- Obvious, high-contrast gradients
- Busy patterns that compete with content
- Decorative elements without purpose

## Implementation Examples

### Typography Implementation

```html
<h1 class="h1">Elegant Headline</h1>
<p class="body">Body copy goes here...</p>
<code class="mono">const x = 42;</code>
```

```css
:root {
  --font-display: 'Playfair Display', serif;
  --font-body: 'IBM Plex Sans', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

.h1 {
  font-family: var(--font-display);
  font-size: 48px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.25px;
}

.body {
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 400;
  line-height: 1.6;
}

.mono {
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 400;
  line-height: 1.5;
}
```

### Orchestrated Page Load Animation

```html
<div class="hero"></div>
<h1 class="headline">Welcome</h1>
<p class="subheadline">The future is now</p>
<button class="cta">Get Started</button>
<div class="content">
  <div class="content-item">Item 1</div>
  <div class="content-item">Item 2</div>
  <div class="content-item">Item 3</div>
</div>
```

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.hero {
  animation: fadeIn 0.8s ease-out 0ms;
}

.headline {
  animation: slideInUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 200ms backwards;
}

.subheadline {
  animation: fadeIn 0.6s ease-out 400ms backwards;
}

.cta {
  animation: scaleIn 0.5s ease-out 600ms backwards;
}

.content-item {
  animation: slideInUp 0.8s ease-out backwards;
}

.content-item:nth-child(1) { animation-delay: 800ms; }
.content-item:nth-child(2) { animation-delay: 900ms; }
.content-item:nth-child(3) { animation-delay: 1000ms; }
```

### Responsive Grid Layout

```html
<div class="grid">
  <article class="card">
    <h2>Feature One</h2>
    <p>Description...</p>
  </article>
  <article class="card">
    <h2>Feature Two</h2>
    <p>Description...</p>
  </article>
</div>
```

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-lg);
  padding: var(--space-xl);
}

.card {
  background: var(--color-surface);
  padding: var(--space-lg);
  border-radius: 8px;
  transition: all var(--transition-base);
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
}

/* Mobile-first */
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
```

### Scroll Trigger Animation

```html
<section data-animate>
  <h2>Section appears on scroll</h2>
</section>
```

```css
[data-animate] {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s ease-out;
}

[data-animate].animate-in {
  opacity: 1;
  transform: translateY(0);
}
```

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
      observer.unobserve(entry.target);
    }
  });
});

document.querySelectorAll('[data-animate]').forEach((el) => {
  observer.observe(el);
});
```

## Accessibility Best Practices

### Semantic HTML

```html
<!-- Use semantic elements -->
<header>
  <nav aria-label="Main navigation">
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>
</header>

<main>
  <article>
    <h1>Article Title</h1>
    <section>
      <h2>Section</h2>
    </section>
  </article>
</main>

<footer>
  <p>&copy; 2025 Company Name</p>
</footer>
```

### WCAG 2.1 Level AA Compliance

```css
/* Sufficient color contrast (4.5:1 for normal text) */
body {
  color: #1a1a1a;
  background-color: #f7f5f2;
}

/* Visible focus indicators */
:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* Sufficient line height (minimum 1.5 for body) */
.body {
  line-height: 1.6;
}

/* Touch targets minimum 44x44px */
button {
  min-height: 44px;
  min-width: 44px;
  padding: var(--space-sm) var(--space-md);
}

/* Readable font size (minimum 16px for body) */
.body {
  font-size: 16px;
}
```

### ARIA Attributes

```html
<!-- Meaningful labels -->
<button aria-label="Close menu">✕</button>

<!-- Live regions for dynamic content -->
<div aria-live="polite" role="status">
  3 items added to cart
</div>

<!-- Current page indicator -->
<a href="/about" aria-current="page">About</a>

<!-- Expanded/collapsed state -->
<button aria-expanded="false" aria-controls="menu">Menu</button>
<div id="menu" hidden>Content</div>
```

## Performance Optimization

```css
/* Use hardware acceleration for animations */
.animated {
  transform: translateZ(0);
  will-change: transform;
}

/* Avoid layout thrashing */
/* Instead of: top, left, width, height
   Use: transform, opacity */

/* Optimize for paint performance */
.card {
  contain: layout style paint;
}

/* Reduce animation complexity */
/* Instead of animating width
   Use: transform: scaleX() */
```

## Testing Checklist

- [ ] Responsive design (mobile 320px, tablet 768px, desktop 1024px+)
- [ ] Color contrast (4.5:1 for normal text, 3:1 for large text)
- [ ] Keyboard navigation (Tab, Shift+Tab, Enter)
- [ ] Focus indicators (visible and intentional)
- [ ] Alt text on images
- [ ] Proper heading hierarchy (h1, h2, h3, etc.)
- [ ] Form labels (associated with inputs)
- [ ] Animation performance (60fps on scroll)
- [ ] Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- [ ] Touch-friendly (44x44px minimum tap targets)

## When to Use This Skill

Use this skill when you need to:

- Build distinctive frontends with intentional design (not generic defaults)
- Create semantic, accessible HTML interfaces
- Implement sophisticated CSS layouts and animations
- Ensure WCAG 2.1 AA compliance
- Build responsive, mobile-first interfaces
- Create orchestrated page load animations
- Apply a comprehensive design framework to frontend development

## When NOT to Use This Skill

- Building simple landing pages (use templates instead)
- Rapid prototyping without design thinking
- Projects with strict Material Design requirements
- Interfaces requiring complex state-driven animations (use React + Framer Motion)

## Further Reading

- **SKILL.md**: Complete skill documentation with all frameworks
- **Typography Guidance**: Detailed font selection and pairing strategies
- **Motion & Animation**: CSS animation patterns and best practices
- **Anti-Patterns**: What to avoid when creating intentional design
- **Design Thinking**: Pre-coding workflow to establish design foundation

## Support

For questions or examples, see `examples/showcase.md` for working implementations.
