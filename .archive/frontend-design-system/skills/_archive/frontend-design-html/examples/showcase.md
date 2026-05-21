# Frontend Design HTML - Showcase

This document contains working examples demonstrating the skill in action. Each example shows intentional design decisions and implementation patterns.

## Example 1: Warm Typography Pairing

### Design Brief

- **Fonts**: Crimson Pro (display) + IBM Plex Sans (body)
- **Color Palette**: Warm neutrals with burnt orange accent
- **Motion**: Orchestrated page load, snappy hover states
- **Layout**: Asymmetrical card arrangement
- **Target**: Luxury product landing page

### HTML

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Artisan Crafts</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;700;900&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="site-header">
    <div class="container">
      <h1 class="logo">ARTISAN</h1>
      <nav aria-label="Main navigation">
        <a href="#about">About</a>
        <a href="#collections">Collections</a>
        <a href="#contact">Contact</a>
      </nav>
    </div>
  </header>

  <main>
    <!-- Hero Section -->
    <section class="hero" aria-label="Hero section">
      <div class="container">
        <div class="hero-content">
          <h1 class="display">Handcrafted Excellence</h1>
          <p class="subtitle">Where tradition meets contemporary design</p>
          <button class="cta">Explore Collection</button>
        </div>
      </div>
    </section>

    <!-- Collections -->
    <section id="collections" class="collections">
      <div class="container">
        <h2 class="section-title">Featured Collections</h2>

        <div class="collection-grid">
          <article class="collection-card" data-animate>
            <div class="card-image">
              <img src="ceramic-1.jpg" alt="Ceramic artware collection">
            </div>
            <div class="card-content">
              <h3 class="h2">Ceramic Series</h3>
              <p class="body-small">Hand-thrown ceramic pieces with glaze finishes</p>
              <a href="#" class="link">View Collection →</a>
            </div>
          </article>

          <article class="collection-card" data-animate>
            <div class="card-image">
              <img src="textile-1.jpg" alt="Textile artware collection">
            </div>
            <div class="card-content">
              <h3 class="h2">Textile Art</h3>
              <p class="body-small">Woven patterns inspired by nature and geometry</p>
              <a href="#" class="link">View Collection →</a>
            </div>
          </article>

          <article class="collection-card" data-animate>
            <div class="card-image">
              <img src="wood-1.jpg" alt="Wood artware collection">
            </div>
            <div class="card-content">
              <h3 class="h2">Wood Turning</h3>
              <p class="body-small">Sculptural wood forms finished with natural oils</p>
              <a href="#" class="link">View Collection →</a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- About -->
    <section id="about" class="about">
      <div class="container">
        <div class="about-grid">
          <div class="about-text">
            <h2 class="h1">About Our Craft</h2>
            <p class="body">Each piece is created by hand, reflecting our commitment to quality and attention to detail.</p>
            <p class="body">We believe in sustainable materials, ethical production, and timeless design that endures.</p>
          </div>
          <div class="about-stats">
            <div class="stat">
              <div class="stat-number">15+</div>
              <div class="stat-label">Years Crafting</div>
            </div>
            <div class="stat">
              <div class="stat-number">2,400+</div>
              <div class="stat-label">Pieces Created</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>&copy; 2025 Artisan Crafts. All rights reserved.</p>
    </div>
  </footer>

  <script src="main.js"></script>
</body>
</html>
```

### CSS

```css
:root {
  /* Typography */
  --font-display: 'Crimson Pro', serif;
  --font-body: 'IBM Plex Sans', sans-serif;

  /* Colors - Warm palette */
  --color-primary: #2d2520;
  --color-accent: #d4753c; /* Burnt orange */
  --color-background: #f9f6f1; /* Warm cream */
  --color-surface: #ffffff;
  --color-text: #3d3d3d;
  --color-text-light: #6d6d6d;

  /* Spacing */
  --space-xs: 0.5rem;
  --space-sm: 0.75rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  --space-3xl: 4rem;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 12px 24px rgba(0, 0, 0, 0.12);

  /* Transitions */
  --transition-fast: 0.2s ease-out;
  --transition-base: 0.3s ease-out;
  --transition-slow: 0.6s ease-out;

  /* Easing */
  --ease-elastic: cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: var(--font-body);
  font-size: 16px;
  color: var(--color-text);
  background-color: var(--color-background);
  line-height: 1.6;
}

/* Typography */
.display {
  font-family: var(--font-display);
  font-size: 88px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.5px;
  margin-bottom: var(--space-lg);
}

.h1 {
  font-family: var(--font-display);
  font-size: 48px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.25px;
  margin-bottom: var(--space-lg);
}

.h2 {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: var(--space-md);
}

.body {
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: var(--space-md);
}

.body-small {
  font-size: 14px;
  color: var(--color-text-light);
  line-height: 1.6;
}

.subtitle {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 400;
  color: var(--color-text-light);
  margin-bottom: var(--space-lg);
  letter-spacing: 0.5px;
}

.section-title {
  font-family: var(--font-display);
  font-size: 56px;
  font-weight: 700;
  text-align: center;
  margin-bottom: var(--space-3xl);
  letter-spacing: -0.25px;
}

/* Layout */
.container {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 var(--space-lg);
}

/* Header */
.site-header {
  background: var(--color-surface);
  padding: var(--space-xl) 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}

.site-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--color-primary);
}

.site-header nav {
  display: flex;
  gap: var(--space-2xl);
}

.site-header nav a {
  color: var(--color-text);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: color var(--transition-base);
}

.site-header nav a:hover {
  color: var(--color-accent);
}

/* Hero Section */
.hero {
  padding: var(--space-3xl) 0;
  text-align: center;
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  animation: fadeIn 0.8s ease-out 0ms;
}

.hero .display {
  animation: slideInUp 0.8s var(--ease-elastic) 200ms backwards;
}

.hero .subtitle {
  animation: fadeIn 0.6s ease-out 400ms backwards;
}

.hero .cta {
  animation: scaleIn 0.5s ease-out 600ms backwards;
}

/* CTA Button */
.cta {
  background: var(--color-accent);
  color: white;
  border: none;
  padding: var(--space-md) var(--space-2xl);
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all var(--transition-base);
  min-height: 44px;
  display: inline-block;
}

.cta:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(212, 117, 60, 0.3);
}

.cta:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Collections Section */
.collections {
  padding: var(--space-3xl) 0;
  background: var(--color-surface);
}

.collection-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--space-2xl);
}

/* Collection Cards */
.collection-card {
  background: var(--color-background);
  border-radius: 8px;
  overflow: hidden;
  transition: all var(--transition-base);
  display: flex;
  flex-direction: column;
  opacity: 0;
  transform: translateY(20px);
}

.collection-card.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.collection-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
}

.card-image {
  width: 100%;
  aspect-ratio: 4/3;
  overflow: hidden;
  background: linear-gradient(135deg, #e8d5c4 0%, #d4c4b0 100%);
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-base);
}

.collection-card:hover .card-image img {
  transform: scale(1.05);
}

.card-content {
  padding: var(--space-xl);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-content .h2 {
  margin-bottom: var(--space-sm);
}

.collection-card p {
  flex: 1;
  margin-bottom: var(--space-md);
}

.link {
  color: var(--color-accent);
  text-decoration: none;
  font-weight: 600;
  transition: all var(--transition-fast);
  display: inline-block;
}

.link:hover {
  transform: translateX(4px);
}

.link:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* About Section */
.about {
  padding: var(--space-3xl) 0;
}

.about-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3xl);
  align-items: start;
}

.about-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-2xl);
}

.stat {
  background: var(--color-surface);
  padding: var(--space-2xl);
  border-left: 4px solid var(--color-accent);
  border-radius: 4px;
}

.stat-number {
  font-family: var(--font-display);
  font-size: 42px;
  font-weight: 700;
  color: var(--color-accent);
  margin-bottom: var(--space-sm);
}

.stat-label {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--color-text-light);
}

/* Footer */
.site-footer {
  background: var(--color-primary);
  color: white;
  padding: var(--space-2xl) 0;
  text-align: center;
}

.site-footer p {
  font-size: 13px;
  letter-spacing: 0.5px;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .display {
    font-size: 52px;
  }

  .h1 {
    font-size: 36px;
  }

  .h2 {
    font-size: 24px;
  }

  .section-title {
    font-size: 36px;
  }

  .site-header nav {
    gap: var(--space-lg);
    font-size: 12px;
  }

  .about-grid {
    grid-template-columns: 1fr;
  }

  .collection-grid {
    grid-template-columns: 1fr;
  }

  .hero {
    padding: var(--space-2xl) 0;
  }
}

@media (max-width: 480px) {
  .display {
    font-size: 36px;
  }

  .hero {
    min-height: auto;
    padding: var(--space-2xl) 0;
  }

  .site-header nav {
    display: none;
  }
}
```

### JavaScript

```javascript
// Scroll trigger animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
      observer.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.1,
});

document.querySelectorAll('[data-animate]').forEach((el) => {
  observer.observe(el);
});

// Smooth navigation
document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});
```

### Design Decisions

**Typography**:
- Crimson Pro (serif) for headlines creates elegance and tradition
- IBM Plex Sans (sans) for body provides warmth and readability
- Size jumps of 3x+ (88px, 48px, 32px, 16px) create clear hierarchy

**Color**:
- Warm cream background (#f9f6f1) creates inviting atmosphere
- Burnt orange accent (#d4753c) unexpected in "artisan" context
- Warm neutrals throughout (creams, browns) support handcrafted message

**Motion**:
- Orchestrated hero load (0ms, 200ms, 400ms, 600ms)
- Scroll-triggered card reveals for engagement
- Subtle hover effects (lift + shadow) for interactivity

**Spatial**:
- Asymmetrical card grid (responsive, not uniform)
- Generous whitespace (3rem spacing sections)
- Left-aligned stat boxes create visual rhythm

**Backgrounds**:
- Subtle gradient in card images (not obvious)
- Warm color palette throughout (no stark whites)
- Minimal decoration (borders, shadows) for elegance

---

## Example 2: Geometric Sans + Monospace for Tech

### Design Brief

- **Fonts**: Space Grotesk (display) + JetBrains Mono (body)
- **Color Palette**: Cool grays with electric blue accent
- **Motion**: Snappy interactions, minimal animation
- **Layout**: Structured grid with asymmetrical emphasis
- **Target**: Developer tools platform

### Key Elements

```html
<!-- Header with code snippet -->
<header>
  <h1 class="display">Build APIs Faster</h1>
  <code class="code-snippet">$ npm install @platform/sdk</code>
</header>

<!-- Feature cards with different layout -->
<div class="features-grid">
  <div class="feature-large">
    <h2>Full-Featured CLI</h2>
    <pre><code>deploy --production</code></pre>
  </div>
  <div class="feature">
    <h3>Type Safe</h3>
    <p>Built with TypeScript</p>
  </div>
  <div class="feature">
    <h3>Fast</h3>
    <p>Optimized performance</p>
  </div>
</div>
```

```css
:root {
  --font-display: 'Space Grotesk', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --color-accent: #0099ff;
  --color-background: #0f1419;
  --color-text: #e0e0e0;
}

.display {
  font-family: var(--font-display);
  font-size: 64px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 1rem;
}

.code-snippet {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--color-accent);
  background: rgba(0, 153, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 4px;
  display: inline-block;
}

.features-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 2rem;
  margin-top: 3rem;
}

.feature-large {
  background: rgba(0, 153, 255, 0.05);
  border: 1px solid rgba(0, 153, 255, 0.2);
  padding: 2rem;
  grid-row: span 2;
}

.feature {
  background: rgba(255, 255, 255, 0.05);
  padding: 1.5rem;
  border-radius: 8px;
}
```

### Characteristics

- **Type asymmetry**: Large feature takes 2 rows, others single row
- **Minimal animation**: Hover lift on cards only
- **Code-focused**: Monospace font prominent
- **Cool palette**: Electric blue on dark background
- **High contrast**: Ensures readability for code

---

## Key Takeaways

### What Makes These Distinctive

1. **Typography Choices**
   - Example 1: Serif + Sans (elegant pairing)
   - Example 2: Geometric Sans + Monospace (modern pairing)
   - Both avoid Inter, Roboto, generic defaults

2. **Color Intentionality**
   - Example 1: Warm palette with burnt orange (unexpected)
   - Example 2: Cool palette with electric blue (familiar but intentional)
   - Custom CSS variables enable consistent theming

3. **Motion Strategy**
   - Example 1: Orchestrated reveals with staggered delays
   - Example 2: Minimal but snappy (no slow animations)
   - Both use easing functions, not linear timing

4. **Spatial Decisions**
   - Example 1: Asymmetrical card grid, left-aligned stats
   - Example 2: Asymmetrical feature grid (2fr/1fr columns)
   - Both avoid "generic SaaS" centered layouts

5. **Accessibility Built-In**
   - Semantic HTML5 (header, nav, main, footer, article, section)
   - WCAG-compliant color contrast
   - Focus indicators on interactive elements
   - Proper heading hierarchy

### Common Patterns

- **Font Loading**: Google Fonts with preconnect for performance
- **CSS Variables**: Define all colors, spacing, transitions once
- **Intersection Observer**: Scroll-triggered animations with CSS classes
- **Responsive Design**: Mobile-first with media queries for tablet/desktop
- **Accessibility**: Always include focus states and semantic markup

---

## Design Thinking Applied

Both examples followed the pre-design thinking:

1. **Purpose**: What are we solving? (Product showcase vs. developer tools)
2. **Tone**: What emotional response? (Luxury/crafted vs. technical/fast)
3. **Constraints**: What are our limits? (Color palette, animation budget)
4. **Differentiation**: What's unforgettable? (Warm serif styling vs. geometric asymmetry)

This approach ensures intentional, distinctive design that stands out from generic AI defaults.
