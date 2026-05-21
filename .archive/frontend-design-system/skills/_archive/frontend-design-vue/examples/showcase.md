# Frontend Design Vue - Component Showcase

Complete working examples demonstrating distinctive, production-grade Vue 3 components with exceptional design quality.

## Example 1: Hero Section with Orchestrated Animations

A hero component that introduces the page with orchestrated, staggered animations following the 5 design dimensions.

```vue
<script setup lang="ts">
import { useMotion } from '@vueuse/motion'
import { ref } from 'vue'

const heroRef = ref()
const headlineRef = ref()
const subheadlineRef = ref()
const ctaRef = ref()

// Orchestrate animation sequence
useMotion(heroRef, {
  initial: { opacity: 0 },
  enter: { opacity: 1, transition: { duration: 0.8 } }
})

useMotion(headlineRef, {
  initial: { opacity: 0, y: -20 },
  enter: {
    opacity: 1,
    y: 0,
    transition: { delay: 200, duration: 0.8, ease: 'easeOut' }
  }
})

useMotion(subheadlineRef, {
  initial: { opacity: 0 },
  enter: {
    opacity: 1,
    transition: { delay: 400, duration: 0.6 }
  }
})

useMotion(ctaRef, {
  initial: { opacity: 0, scale: 0.95 },
  enter: {
    opacity: 1,
    scale: 1,
    transition: {
      delay: 600,
      duration: 0.5,
      ease: [0.34, 1.56, 0.64, 1] // elastic easing
    }
  }
})
</script>

<template>
  <section
    ref="heroRef"
    class="hero"
    aria-labelledby="hero-headline"
  >
    <!-- Subtle gradient background -->
    <div class="hero-background"></div>

    <div class="hero-content">
      <h1
        ref="headlineRef"
        id="hero-headline"
        class="headline"
      >
        Design That Commands Attention
      </h1>

      <p ref="subheadlineRef" class="subheadline">
        Distinctive Vue 3 components that avoid generic AI patterns.
        Intentional typography, color, and motion at every level.
      </p>

      <button
        ref="ctaRef"
        type="button"
        class="cta-button"
        aria-label="Start building distinctive interfaces"
      >
        Start Building
      </button>
    </div>
  </section>
</template>

<style scoped>
:root {
  /* Typography */
  --font-display: 'Playfair Display', serif;
  --font-body: 'IBM Plex Sans', sans-serif;

  /* Color system: Warm palette with unexpected accent */
  --color-primary: #004e89; /* Deep indigo */
  --color-accent: #ff6b35; /* Unexpected burnt orange */
  --color-background: #fffbf7; /* Warm off-white */
  --color-text: #1a1a1a;
  --color-text-secondary: #666666;

  /* Spacing scale */
  --spacing-xs: 8px;
  --spacing-sm: 12px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
}

.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: var(--color-background);
}

.hero-background {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(255, 251, 247, 1) 0%,
    rgba(240, 235, 230, 0.8) 100%
  );
  z-index: -1;
}

.hero-content {
  max-width: 800px;
  padding: var(--spacing-2xl);
  text-align: center;
}

.headline {
  font-family: var(--font-display);
  font-size: 88px; /* 5.5x body size (16px) */
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.5px;
  color: var(--color-text);
  margin: 0 0 var(--spacing-lg) 0;
  will-change: opacity, transform;
}

.subheadline {
  font-family: var(--font-body);
  font-size: 18px;
  font-weight: 400;
  line-height: 1.6;
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-2xl) 0;
  will-change: opacity;
}

.cta-button {
  display: inline-block;
  padding: var(--spacing-md) var(--spacing-xl);
  background-color: var(--color-accent);
  color: white;
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 0; /* Deliberate sharp corners */
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  will-change: opacity, transform;

  /* Accessibility: focus state */
  &:focus-visible {
    outline: 3px solid var(--color-primary);
    outline-offset: 3px;
  }

  /* Hover with delightful motion */
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(255, 107, 53, 0.2);
  }

  /* Active state */
  &:active {
    transform: translateY(-2px);
  }
}

/* Mobile-first responsive */
@media (max-width: 768px) {
  .hero {
    min-height: auto;
    padding: var(--spacing-xl) 0;
  }

  .hero-content {
    padding: var(--spacing-lg);
  }

  .headline {
    font-size: 48px; /* 3x body size for mobile */
    margin-bottom: var(--spacing-md);
  }

  .subheadline {
    font-size: 16px;
    margin-bottom: var(--spacing-lg);
  }

  .cta-button {
    padding: var(--spacing-sm) var(--spacing-lg);
    font-size: 14px;
  }
}
</style>
```

**Design Principles Demonstrated**:
- Typography: Playfair Display (elegant serif) vs IBM Plex Sans (warm humanist)
- Color: Deep indigo primary + unexpected burnt orange accent
- Motion: Orchestrated 0ms → 600ms staggered reveal with easing
- Spatial: Centered but with generous padding and clear hierarchy
- Details: Subtle gradient background, sharp corners (intentional deviation)

---

## Example 2: Feature Card Grid with Hover Surprises

Asymmetrical card grid with delightful hover animations that surprise rather than just respond.

```vue
<script setup lang="ts">
import { useMotion } from '@vueuse/motion'
import { ref, computed } from 'vue'

interface Feature {
  id: string
  icon: string
  title: string
  description: string
  color: string
}

const features = ref<Feature[]>([
  {
    id: 'typography',
    icon: '✍️',
    title: 'Intentional Typography',
    description: 'Distinctive typeface pairings that avoid generic defaults.',
    color: '#004e89'
  },
  {
    id: 'color',
    icon: '🎨',
    title: 'Custom Color Systems',
    description: 'Palettes with personality and unexpected accent colors.',
    color: '#ff6b35'
  },
  {
    id: 'motion',
    icon: '⚡',
    title: 'Orchestrated Motion',
    description: 'Animations that feel planned, not random or robotic.',
    color: '#9d4edd'
  },
  {
    id: 'layout',
    icon: '📐',
    title: 'Asymmetrical Layouts',
    description: 'Spatial composition that guides the eye intentionally.',
    color: '#3a86ff'
  },
  {
    id: 'details',
    icon: '✨',
    title: 'Visual Details',
    description: 'Subtle backgrounds, patterns, and micro-interactions.',
    color: '#fb5607'
  },
  {
    id: 'accessible',
    icon: '♿',
    title: 'Fully Accessible',
    description: 'WCAG AA compliant with semantic HTML and ARIA.',
    color: '#06d6a0'
  }
])

const cardRefs = ref<Map<string, HTMLElement>>(new Map())

const setupCardAnimation = (featureId: string, el: HTMLElement) => {
  cardRefs.value.set(featureId, el)

  const feature = features.value.find((f) => f.id === featureId)
  if (!feature) return

  useMotion(el, {
    initial: { opacity: 0, y: 20 },
    enter: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: [0.16, 0.04, 0.04, 1] // ease-out
      }
    },
    hover: {
      y: -8,
      boxShadow: '0 24px 48px rgba(0,0,0,0.15)',
      transition: {
        type: 'spring',
        stiffness: 200,
        damping: 20
      }
    }
  })
}
</script>

<template>
  <section class="features" aria-labelledby="features-heading">
    <h2 id="features-heading" class="section-heading">
      Design Dimensions
    </h2>

    <div class="grid">
      <article
        v-for="feature in features"
        :key="feature.id"
        :ref="(el: any) => setupCardAnimation(feature.id, el)"
        class="card"
        :style="{ '--accent-color': feature.color }"
      >
        <!-- Accent bar -->
        <div class="accent-bar"></div>

        <div class="card-content">
          <div class="icon" role="img" :aria-label="feature.title">
            {{ feature.icon }}
          </div>

          <h3 class="card-title">{{ feature.title }}</h3>

          <p class="card-description">
            {{ feature.description }}
          </p>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
:root {
  --font-display: 'Playfair Display', serif;
  --font-body: 'IBM Plex Sans', sans-serif;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-2xl: 48px;
  --color-background: #fffbf7;
}

.features {
  background-color: var(--color-background);
  padding: var(--spacing-2xl);
}

.section-heading {
  font-family: var(--font-display);
  font-size: 52px;
  font-weight: 700;
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  color: #1a1a1a;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--spacing-lg);
  max-width: 1200px;
  margin: 0 auto;

  /* Asymmetrical layout: offset alternating cards */
  @media (min-width: 768px) {
    grid-template-columns: repeat(3, 1fr);

    & > :nth-child(even) {
      margin-top: var(--spacing-lg);
    }
  }
}

.card {
  position: relative;
  background: white;
  border-radius: 4px; /* Subtle roundness, not completely sharp */
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  will-change: transform, box-shadow;
}

.accent-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background-color: var(--accent-color);
  transition: height 0.3s ease-out;
}

.card:hover .accent-bar {
  height: 8px; /* Expands on hover for surprise */
}

.card-content {
  padding: var(--spacing-lg);
}

.icon {
  font-size: 40px;
  margin-bottom: var(--spacing-md);
  display: inline-block;
  transition: transform 0.3s ease-out;

  /* Hover surprise: icon rotates and scales */
  .card:hover & {
    transform: rotate(12deg) scale(1.1);
  }
}

.card-title {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 var(--spacing-md) 0;
  color: #1a1a1a;
}

.card-description {
  font-family: var(--font-body);
  font-size: 14px;
  line-height: 1.6;
  color: #666;
  margin: 0;
}

/* Mobile responsive */
@media (max-width: 640px) {
  .features {
    padding: var(--spacing-lg);
  }

  .section-heading {
    font-size: 36px;
    margin-bottom: var(--spacing-lg);
  }

  .grid {
    gap: var(--spacing-md);
  }
}
</style>
```

**Design Principles Demonstrated**:
- Typography: Playfair Display headings for personality
- Color: Each card has unique accent color
- Motion: Spring-based hover animation (not linear), icon rotates with scale
- Spatial: Asymmetrical grid with alternating offset
- Details: Accent bar expands on hover (delightful surprise)

---

## Example 3: Form with Motion-Enhanced Interactions

Form component with motion-enhanced field interactions and validation feedback.

```vue
<script setup lang="ts">
import { useMotion } from '@vueuse/motion'
import { ref, reactive } from 'vue'

interface FormData {
  email: string
  password: string
  terms: boolean
}

const form = ref()
const emailInput = ref()
const passwordInput = ref()
const submitBtn = ref()

const formData = reactive<FormData>({
  email: '',
  password: '',
  terms: false
})

const errors = reactive<Partial<FormData>>({})

useMotion(form, {
  initial: { opacity: 0, y: 20 },
  enter: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6 }
  }
})

useMotion(submitBtn, {
  initial: { opacity: 0, scale: 0.95 },
  enter: {
    opacity: 1,
    scale: 1,
    transition: { delay: 300, duration: 0.5 }
  }
})

const validateEmail = (): boolean => {
  const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)
  if (!isValid) {
    errors.email = 'Please enter a valid email address'
  } else {
    delete errors.email
  }
  return isValid
}

const validatePassword = (): boolean => {
  const isValid = formData.password.length >= 8
  if (!isValid) {
    errors.password = 'Password must be at least 8 characters'
  } else {
    delete errors.password
  }
  return isValid
}

const handleSubmit = (): void => {
  const emailValid = validateEmail()
  const passwordValid = validatePassword()

  if (emailValid && passwordValid && formData.terms) {
    console.log('Form submitted:', formData)
    // Handle submission
  }
}

const handleEmailBlur = (): void => {
  if (formData.email) {
    validateEmail()
  }
}

const handlePasswordBlur = (): void => {
  if (formData.password) {
    validatePassword()
  }
}
</script>

<template>
  <form
    ref="form"
    @submit.prevent="handleSubmit"
    class="form"
    aria-labelledby="form-heading"
  >
    <h2 id="form-heading" class="form-heading">
      Create Your Account
    </h2>

    <div class="form-group">
      <label for="email-field" class="label">Email Address</label>
      <input
        id="email-field"
        ref="emailInput"
        v-model="formData.email"
        type="email"
        placeholder="you@example.com"
        class="input"
        :class="{ 'input--error': errors.email }"
        aria-required="true"
        :aria-invalid="!!errors.email"
        :aria-describedby="errors.email ? 'email-error' : 'email-help'"
        @blur="handleEmailBlur"
      >
      <p
        v-if="errors.email"
        id="email-error"
        class="error-message"
        role="alert"
      >
        {{ errors.email }}
      </p>
      <p v-else id="email-help" class="help-text">
        We'll never share your email address.
      </p>
    </div>

    <div class="form-group">
      <label for="password-field" class="label">Password</label>
      <input
        id="password-field"
        ref="passwordInput"
        v-model="formData.password"
        type="password"
        placeholder="Minimum 8 characters"
        class="input"
        :class="{ 'input--error': errors.password }"
        aria-required="true"
        :aria-invalid="!!errors.password"
        :aria-describedby="errors.password ? 'password-error' : 'password-help'"
        @blur="handlePasswordBlur"
      >
      <p
        v-if="errors.password"
        id="password-error"
        class="error-message"
        role="alert"
      >
        {{ errors.password }}
      </p>
      <p v-else id="password-help" class="help-text">
        At least 8 characters, including uppercase and symbols.
      </p>
    </div>

    <div class="form-group">
      <label for="terms-checkbox" class="checkbox-label">
        <input
          id="terms-checkbox"
          v-model="formData.terms"
          type="checkbox"
          class="checkbox"
          aria-required="true"
        >
        I agree to the terms and conditions
      </label>
    </div>

    <button
      ref="submitBtn"
      type="submit"
      class="submit-button"
      :disabled="!formData.email || !formData.password || !formData.terms"
      aria-label="Submit form to create account"
    >
      Create Account
    </button>
  </form>
</template>

<style scoped>
:root {
  --font-body: 'IBM Plex Sans', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --color-primary: #004e89;
  --color-accent: #ff6b35;
  --color-success: #06d6a0;
  --color-error: #d62828;
  --color-background: #fffbf7;
  --spacing-sm: 12px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
}

.form {
  max-width: 400px;
  margin: 0 auto;
  padding: var(--spacing-lg);
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  will-change: opacity, transform;
}

.form-heading {
  font-size: 24px;
  font-weight: 700;
  text-align: center;
  margin: 0 0 var(--spacing-lg) 0;
  color: #1a1a1a;
}

.form-group {
  margin-bottom: var(--spacing-lg);
}

.label {
  display: block;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  margin-bottom: var(--spacing-sm);
  color: #1a1a1a;
}

.input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  font-family: var(--font-body);
  font-size: 14px;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  transition: all 0.3s ease-out;

  &:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(0, 78, 137, 0.1);
  }

  &.input--error {
    border-color: var(--color-error);

    &:focus {
      box-shadow: 0 0 0 3px rgba(214, 40, 40, 0.1);
    }
  }
}

.error-message {
  margin: var(--spacing-sm) 0 0 0;
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--color-error);
  font-weight: 500;
}

.help-text {
  margin: var(--spacing-sm) 0 0 0;
  font-family: var(--font-body);
  font-size: 12px;
  color: #999;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-family: var(--font-body);
  font-size: 14px;
  cursor: pointer;
  user-select: none;

  &:focus-within {
    .checkbox {
      outline: 3px solid var(--color-primary);
      outline-offset: 2px;
    }
  }
}

.checkbox {
  width: 18px;
  height: 18px;
  margin-right: var(--spacing-sm);
  cursor: pointer;
  accent-color: var(--color-accent);
}

.submit-button {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--color-accent);
  color: white;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  will-change: background-color, transform;

  &:hover:not(:disabled) {
    background-color: #e55a2b;
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(255, 107, 53, 0.25);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
    opacity: 0.6;
  }

  &:focus-visible {
    outline: 3px solid var(--color-primary);
    outline-offset: 2px;
  }
}

/* Mobile responsive */
@media (max-width: 640px) {
  .form {
    padding: var(--spacing-md);
  }
}
</style>
```

**Design Principles Demonstrated**:
- Typography: Clean hierarchy with size variations
- Color: Accent color for CTAs, error states in red
- Motion: Smooth transitions on focus, hover states
- Spatial: Proper spacing between form elements
- Accessibility: Full ARIA support, semantic HTML, focus states

---

## Component Patterns Summary

### Common Patterns Used

1. **CSS Variables for Theming**
   ```css
   :root {
     --color-primary: #004e89;
     --spacing-base: 16px;
     --font-display: 'Playfair Display', serif;
   }
   ```

2. **@vueuse/motion for Animations**
   ```typescript
   useMotion(ref, {
     initial: { opacity: 0 },
     enter: { opacity: 1, transition: { ... } }
   })
   ```

3. **Responsive Design (Mobile-First)**
   ```css
   @media (min-width: 768px) { /* Tablet and up */ }
   @media (min-width: 1024px) { /* Desktop and up */ }
   ```

4. **Accessibility First**
   ```html
   <button
     type="button"
     aria-label="Description"
     :aria-expanded="isOpen"
   >
   </button>
   ```

5. **Semantic HTML Structure**
   ```html
   <nav role="navigation" aria-label="Main">
   <main id="main-content" role="main">
   <section aria-labelledby="section-heading">
   ```

---

## Design Validation

All examples follow the anti-generic-AI checklist:

✅ Distinctive typography (Playfair Display + IBM Plex Sans)
✅ Custom color palettes with personality
✅ Asymmetrical or intentional layouts
✅ Orchestrated, eased animations
✅ Full accessibility with ARIA and semantics
✅ Mobile-first responsive design
✅ CSS variables for theming
✅ TypeScript for type safety
✅ Composition API with `<script setup>`
✅ @vueuse/motion for sophisticated motion

---

## Next Steps

1. Copy these component structures
2. Adapt the design tokens (colors, fonts, spacing)
3. Implement the 8-phase workflow
4. Add your unforgettable design element
5. Validate against the anti-generic-AI checklist
6. Test accessibility and responsive behavior
