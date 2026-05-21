# Frontend Design Fix - Vue

## Quick Start

This skill helps you transform generic Vue component designs into visually distinctive interfaces using Anthropic's 5 design dimensions.

### What This Skill Does

1. **Analyzes** your current Vue components for generic design patterns
2. **Audits** against anti-patterns (bland typography, purple gradients, centered layouts, etc.)
3. **Applies** aesthetic upgrades across:
   - Typography (distinctive fonts, extreme weights, size jumps, responsive sizing)
   - Color & Theme (cohesive palettes, provide/inject, accent colors, dark mode)
   - Motion (Vue Transitions, TransitionGroup, scroll animations)
   - Spatial Composition (asymmetric layouts, broken grids, intentional overlap)
   - Backgrounds (layered gradients, textures, atmospheric depth)

### When to Use

Use this skill when you have:
- Existing Vue components that feel generic or bland
- Components using default fonts (Inter, Roboto, Arial)
- Solid color backgrounds
- No animations or transitions
- Centered, predictable layouts
- Purple/blue gradients on white

### Basic Workflow

```
1. Provide your Vue component files (.vue)
2. Skill analyzes and scores against checklist
3. Dimensions are fixed one at a time
4. Theme provider with provide/inject added
5. Vue transitions integrated
6. Before/after comparison generated
7. Accessibility verified
```

## Design Dimensions Explained

### Typography
**Problem**: Generic system fonts in limited weights, no responsive scaling
**Solution**: Distinctive pairs, extreme weights (100-900), 3x size jumps, responsive sizing with CSS

### Color & Theme
**Problem**: Purple gradients, no theming, evenly distributed colors, no dark mode
**Solution**: Provide/inject pattern, CSS custom properties, dominant + accent colors, light/dark variants

### Motion
**Problem**: No animations, abrupt transitions, no micro-interactions
**Solution**: Vue transitions, TransitionGroup, scroll-triggered, hover effects

### Spatial Composition
**Problem**: Centered, symmetrical, predictable layouts
**Solution**: Asymmetry, intentional overlap, broken grids, generous/controlled spacing

### Backgrounds
**Problem**: Solid colors, no depth
**Solution**: Layered gradients, patterns/textures, atmospheric effects, contextual depth

## Example: Before & After

### Before (Generic Vue Component)
```vue
<template>
  <div class="hero">
    <h1>Welcome</h1>
    <button>Click Me</button>
  </div>
</template>

<script setup>
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 40px 20px;
  background: white;
}

h1 {
  font-size: 2rem;
  font-family: Arial, sans-serif;
  color: purple;
}

button {
  padding: 10px 20px;
  background: #e0e0e0;
  border: none;
}
</style>
```

**Anti-pattern Score**: 5/5 items on checklist

### After (Distinctive Vue Component)
```vue
<template>
  <div
    class="hero"
    :style="themeVars"
  >
    <!-- Decorative background element -->
    <div class="background-element" />

    <!-- Content with transitions -->
    <Transition name="fade-up">
      <div v-if="isVisible" class="content">
        <h1 class="headline">Welcome to Something Remarkable</h1>

        <p class="description">
          Discover what happens when design meets intention.
        </p>

        <button
          class="cta-button"
          @click="handleClick"
          @mouseenter="isButtonHovering = true"
          @mouseleave="isButtonHovering = false"
        >
          Discover More
        </button>
      </div>
    </Transition>

    <!-- Accent line -->
    <Transition name="scale-x">
      <div v-if="isVisible" class="accent-line" />
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const isVisible = ref(false);
const isButtonHovering = ref(false);

onMounted(() => {
  isVisible.value = true;
});

const themeVars = computed(() => ({
  '--font-display': "'Playfair Display', serif",
  '--font-body': "'Inter', sans-serif",
  '--font-mono': "'IBM Plex Mono', monospace",
  '--primary': '#1a1a1a',
  '--accent': '#ff6b35',
  '--surface': '#fafafa',
}));

const handleClick = () => {
  console.log('CTA clicked');
};
</script>

<style scoped>
:root {
  --font-display: 'Playfair Display', serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
  --primary: #1a1a1a;
  --accent: #ff6b35;
  --surface: #fafafa;
}

.hero {
  background: linear-gradient(135deg, var(--surface) 0%, #e8e8e8 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

.background-element {
  position: absolute;
  top: -10%;
  right: -5%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(255, 107, 53, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  z-index: 0;
  animation: float 6s ease-in-out infinite;
}

.content {
  position: relative;
  z-index: 1;
  max-width: 600px;
}

.headline {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 8vw, 5rem);
  font-weight: 900;
  color: var(--primary);
  margin: 0 0 1rem 0;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.description {
  font-family: var(--font-body);
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: var(--primary);
  opacity: 0.7;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.cta-button {
  font-family: var(--font-body);
  background: var(--accent);
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 2px;
  font-size: 1.125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease-out;
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.2);
}

.cta-button:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(255, 107, 53, 0.3);
}

.cta-button:focus {
  outline: 3px solid var(--accent);
  outline-offset: 2px;
}

.accent-line {
  position: absolute;
  bottom: 2rem;
  right: 2rem;
  width: 120px;
  height: 2px;
  background: var(--accent);
  animation: scaleIn 0.6s ease-out 0.8s both;
}

/* Transitions */
.fade-up-enter-active,
.fade-up-leave-active {
  transition: all 0.6s ease-out;
}

.fade-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.scale-x-enter-active,
.scale-x-leave-active {
  transition: all 0.6s ease-out;
}

.scale-x-enter-from {
  transform: scaleX(0);
}

.scale-x-leave-to {
  transform: scaleX(0);
}

/* Animations */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(20px); }
}

@keyframes scaleIn {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
</style>
```

**Anti-pattern Score**: 0/5 items on checklist

### Improvements
- [x] Typography: Playfair Display (display) + Inter (body), responsive sizing with clamp()
- [x] Color: CSS custom properties, accent color (#ff6b35), layered gradient background
- [x] Motion: Vue transitions (fade-up, scale-x), animations, hover effects
- [x] Spatial: Left-aligned content (asymmetry), layered with absolute positioning
- [x] Background: Linear gradient + floating element with radial gradient

## Key Vue Patterns

### Theme Provider with Provide/Inject
```vue
<!-- ThemeProvider.vue -->
<template>
  <div :style="themeVars">
    <slot />
  </div>
</template>

<script setup>
import { computed, provide } from 'vue';

const theme = {
  colors: {
    primary: '#1a1a1a',
    accent: '#ff6b35',
    surface: '#fafafa',
  },
  fonts: {
    display: "'Playfair Display', serif",
    body: "'Inter', sans-serif",
  },
};

const themeVars = computed(() => ({
  '--primary': theme.colors.primary,
  '--accent': theme.colors.accent,
  '--surface': theme.colors.surface,
  '--font-display': theme.fonts.display,
  '--font-body': theme.fonts.body,
}));

provide('theme', theme);
</script>

<style scoped>
div {
  color: var(--primary);
  background: var(--surface);
  font-family: var(--font-body);
}
</style>
```

### Using Theme in Components
```vue
<script setup>
import { inject } from 'vue';

const theme = inject('theme');
</script>

<template>
  <button :style="{ background: theme.colors.accent }">
    Click Me
  </button>
</template>
```

### Staggered List with TransitionGroup
```vue
<template>
  <TransitionGroup
    tag="div"
    name="stagger"
    class="list"
  >
    <div
      v-for="(item, index) in items"
      :key="item.id"
      :style="{ '--stagger-index': index }"
      class="list-item"
    >
      {{ item.content }}
    </div>
  </TransitionGroup>
</template>

<script setup>
import { TransitionGroup } from 'vue';

defineProps({
  items: Array,
});
</script>

<style scoped>
.stagger-enter-active,
.stagger-leave-active {
  transition: all 0.4s ease-out;
  transition-delay: calc(var(--stagger-index, 0) * 100ms);
}

.stagger-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.stagger-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
```

### Scroll-Triggered Animations
```vue
<template>
  <div
    ref="elementRef"
    :class="{ visible: isVisible }"
    class="scroll-element"
  >
    Appears when scrolled into view
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const elementRef = ref(null);
const isVisible = ref(false);

onMounted(() => {
  const observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      isVisible.value = true;
    }
  });

  if (elementRef.value) {
    observer.observe(elementRef.value);
  }

  onUnmounted(() => observer.disconnect());
});
</script>

<style scoped>
.scroll-element {
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.6s ease-out;
}

.scroll-element.visible {
  opacity: 1;
  transform: translateY(0);
}
</style>
```

## Accessibility

```vue
<!-- Always use semantic elements -->
<button @click="handleAction">Submit</button>

<!-- Provide focus states -->
<style scoped>
button:focus {
  outline: 3px solid var(--accent);
  outline-offset: 2px;
}
</style>

<!-- Use aria-labels when needed -->
<button aria-label="Close menu">×</button>

<!-- Maintain color contrast (4.5:1 minimum for WCAG AA) -->
```

## Vue Transition Modes

```vue
<!-- Fade transition -->
<Transition name="fade">
  <div v-if="isVisible">Content</div>
</Transition>

<!-- Fade with Up movement -->
<Transition name="fade-up">
  <div v-if="isVisible">Content</div>
</Transition>

<!-- Slide transition -->
<Transition name="slide-x">
  <div v-if="isVisible">Content</div>
</Transition>
```

## Popular Vue Design Libraries

- **Tailwind CSS**: Utility-first CSS
- **Vuetify**: Material Design components
- **PrimeVue**: Enterprise UI library
- **Headless UI**: Unstyled Vue components
- **vue-observe-visibility**: Scroll-triggered animations

## Tools & Resources

- **Font Pairing**: Google Fonts, Adobe Fonts, Variable Fonts
- **Color Tools**: Coolors.co, Contrast Checker, ColorSpace
- **Animation**: Animate.css, AOS (Animate On Scroll), Scroll Reveal
- **Accessibility**: WAVE, AXLE DevTools, Lighthouse, Vue Testing Library

## Next Steps

1. **Create ThemeProvider** component with provide/inject
2. **Wrap your app** in ThemeProvider
3. **Start with typography** dimension
4. **Add Vue Transitions** for page load and interactions
5. **Implement color tokens** as CSS custom properties
6. **Test accessibility** with Vue Testing Library

See `/examples/showcase.md` for complete before/after examples with Vue.
