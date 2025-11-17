# Svelte Component Showcase

Real-world Svelte component examples demonstrating the integration of design thinking, typography, motion, accessibility, and responsive design.

## Example 1: Orchestrated Page Load with Staggered Animations

This example demonstrates Phase 4 (Interaction & Motion Design) with orchestrated reveals that guide the user's eye.

```svelte
<!-- lib/components/HeroSection.svelte -->
<script lang="ts">
  import { fade, fly } from 'svelte/transition'
  import { cubicOut } from 'svelte/easing'

  const headerDelay = 200
  const subheaderDelay = 400
  const ctaDelay = 600
  const contentDelay = 800
</script>

<section class="hero">
  <!-- Background with fade in -->
  <div
    class="hero-background"
    in:fade={{ duration: 800, easing: cubicOut }}
  />

  <!-- Headline with slide from top -->
  <h1
    class="hero-headline"
    in:fly={{
      y: -30,
      duration: 800,
      delay: headerDelay,
      easing: cubicOut,
    }}
  >
    Design with Intention
  </h1>

  <!-- Subheadline with fade in -->
  <p
    class="hero-subheading"
    in:fade={{ duration: 600, delay: subheaderDelay, easing: cubicOut }}
  >
    Create distinctive, production-grade frontends that stand out
  </p>

  <!-- CTA button with scale in -->
  <button
    class="cta-button"
    in:fly={{
      y: 20,
      duration: 600,
      delay: ctaDelay,
      easing: cubicOut,
    }}
  >
    Get Started
  </button>

  <!-- Featured content with staggered reveals -->
  <ul class="hero-features">
    {#each ['Typography', 'Color', 'Motion', 'Accessibility'] as feature, i (feature)}
      <li
        in:fly={{
          y: 20,
          duration: 600,
          delay: contentDelay + i * 100,
          easing: cubicOut,
        }}
      >
        <span class="feature-dot" />{feature}
      </li>
    {/each}
  </ul>
</section>

<style>
  .hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: calc(var(--spacing-unit) * 4);
    background: var(--color-bg);
    overflow: hidden;
  }

  .hero-background {
    position: absolute;
    inset: 0;
    background: linear-gradient(
      135deg,
      var(--color-bg) 0%,
      rgba(212, 165, 116, 0.05) 100%
    );
    pointer-events: none;
  }

  .hero-headline {
    font-family: var(--font-display);
    font-size: clamp(48px, 8vw, 96px);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -1px;
    text-align: center;
    color: var(--color-text);
    margin: 0 0 calc(var(--spacing-unit) * 2) 0;
    max-width: 90%;
    position: relative;
    z-index: 1;
  }

  .hero-subheading {
    font-family: var(--font-body);
    font-size: clamp(16px, 2vw, 24px);
    line-height: 1.6;
    color: rgba(42, 42, 42, 0.7);
    text-align: center;
    margin: 0 0 calc(var(--spacing-unit) * 4) 0;
    max-width: 600px;
    position: relative;
    z-index: 1;
  }

  .cta-button {
    position: relative;
    z-index: 1;
    padding: calc(var(--spacing-unit) * 2) calc(var(--spacing-unit) * 4);
    background: var(--color-accent);
    color: white;
    border: none;
    border-radius: 8px;
    font-family: var(--font-body);
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    margin-bottom: calc(var(--spacing-unit) * 4);
  }

  .cta-button:hover {
    background: var(--color-accent-dark);
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(139, 69, 19, 0.2);
  }

  .hero-features {
    position: relative;
    z-index: 1;
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    gap: calc(var(--spacing-unit) * 3);
    flex-wrap: wrap;
    justify-content: center;
    font-family: var(--font-body);
    font-size: 14px;
    color: rgba(42, 42, 42, 0.6);
  }

  .hero-features li {
    display: flex;
    align-items: center;
    gap: calc(var(--spacing-unit));
  }

  .feature-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--color-accent);
  }

  @media (max-width: 640px) {
    .hero {
      padding: calc(var(--spacing-unit) * 2);
      min-height: auto;
      padding-top: calc(var(--spacing-unit) * 8);
      padding-bottom: calc(var(--spacing-unit) * 4);
    }

    .hero-headline {
      margin-bottom: calc(var(--spacing-unit) * 1.5);
    }

    .hero-subheading {
      margin-bottom: calc(var(--spacing-unit) * 2);
    }

    .hero-features {
      flex-direction: column;
      gap: calc(var(--spacing-unit) * 1.5);
    }
  }
</style>
```

## Example 2: Motion-Rich Card with Reactive Hover State

This example demonstrates Phase 3 (Component Architecture) with TypeScript typing, Phase 4 (Motion Design) with Svelte transitions, and Phase 6 (Theming) with CSS variables.

```svelte
<!-- lib/components/FeatureCard.svelte -->
<script lang="ts">
  import { scale, fly } from 'svelte/transition'
  import { elasticOut, cubicOut } from 'svelte/easing'

  interface Props {
    icon: string
    title: string
    description: string
    index?: number
  }

  let { icon, title, description, index = 0 }: Props = $props()

  let isHovered = $state(false)

  // Reactive computed shadow intensity
  let shadowOpacity = $derived(isHovered ? 0.15 : 0.08)
  let translateY = $derived(isHovered ? -12 : 0)
</script>

<article
  class="card"
  in:fly={{
    y: 40,
    duration: 500,
    delay: index * 75,
    easing: cubicOut,
  }}
  on:mouseenter={() => (isHovered = true)}
  on:mouseleave={() => (isHovered = false)}
  on:focus={() => (isHovered = true)}
  on:blur={() => (isHovered = false)}
  role="article"
  tabindex="0"
>
  <!-- Icon section with scale animation -->
  <div class="card-icon">
    <div
      in:scale={{
        start: 0.8,
        duration: 500,
        delay: index * 75 + 100,
        easing: elasticOut,
      }}
    >
      {icon}
    </div>
  </div>

  <!-- Content -->
  <div class="card-content">
    <h3>{title}</h3>
    <p>{description}</p>
  </div>

  <!-- Reveal action on hover -->
  {#if isHovered}
    <div
      class="card-action"
      in:scale={{
        start: 0.9,
        duration: 300,
        easing: elasticOut,
      }}
    >
      <button aria-label="Learn more about {title}">
        Explore →
      </button>
    </div>
  {/if}
</article>

<style>
  .card {
    display: flex;
    flex-direction: column;
    padding: calc(var(--spacing-unit) * 3);
    background: var(--color-bg);
    border-radius: 12px;
    border: 1px solid rgba(0, 0, 0, 0.08);
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
  }

  .card:hover,
  .card:focus {
    transform: translateY(var(--translate-y, 0));
    box-shadow: 0 24px 48px rgba(0, 0, 0, var(--shadow-opacity, 0.08));
    --translate-y: -12px;
    --shadow-opacity: 0.15;
  }

  .card-icon {
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-accent);
    border-radius: 8px;
    font-size: 32px;
    margin-bottom: calc(var(--spacing-unit) * 2);
    color: white;
  }

  .card-content {
    flex: 1;
  }

  h3 {
    font-family: var(--font-display);
    font-size: 24px;
    font-weight: 700;
    margin: 0 0 calc(var(--spacing-unit)) 0;
    color: var(--color-text);
  }

  p {
    font-family: var(--font-body);
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
    color: rgba(42, 42, 42, 0.7);
  }

  .card-action {
    margin-top: calc(var(--spacing-unit) * 2);
  }

  button {
    padding: calc(var(--spacing-unit) * 1.5) calc(var(--spacing-unit) * 2);
    background: var(--color-accent);
    color: white;
    border: none;
    border-radius: 6px;
    font-family: var(--font-body);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease-out;
    width: 100%;
  }

  button:hover {
    background: var(--color-accent-dark);
    transform: translateY(-2px);
  }

  @media (max-width: 640px) {
    .card {
      padding: calc(var(--spacing-unit) * 2);
    }

    h3 {
      font-size: 20px;
    }

    p {
      font-size: 13px;
    }
  }
</style>
```

## Example 3: Theme-Aware Component with Reactive Store

This example demonstrates Phase 6 (Theming) with Svelte stores and Phase 7 (Accessibility) with proper ARIA attributes.

```svelte
<!-- lib/components/ThemeToggle.svelte -->
<script lang="ts">
  import { isDarkMode } from '$lib/stores/theme'
  import { fly } from 'svelte/transition'

  let isFocused = $state(false)
</script>

<button
  class="theme-toggle"
  aria-label="Toggle dark mode ({$isDarkMode ? 'dark' : 'light'} mode)"
  aria-pressed={$isDarkMode}
  on:click={() => isDarkMode.update((v) => !v)}
  on:focus={() => (isFocused = true)}
  on:blur={() => (isFocused = false)}
>
  <!-- Sun icon for light mode -->
  {#if !$isDarkMode}
    <span
      in:fly={{ x: -10, duration: 300 }}
      aria-hidden="true"
    >
      ☀️
    </span>
  {:else}
    <span
      in:fly={{ x: 10, duration: 300 }}
      aria-hidden="true"
    >
      🌙
    </span>
  {/if}
  <span class="sr-only">
    {$isDarkMode ? 'Light mode' : 'Dark mode'}
  </span>
</button>

<style>
  .theme-toggle {
    position: relative;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--color-accent);
    color: white;
    border: none;
    cursor: pointer;
    font-size: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease-out;
  }

  .theme-toggle:hover {
    transform: scale(1.1);
    box-shadow: 0 8px 16px rgba(212, 165, 116, 0.3);
  }

  .theme-toggle:focus {
    outline: 2px solid var(--color-accent-dark);
    outline-offset: 2px;
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }
</style>

<!-- lib/stores/theme.ts -->
import { writable, derived } from 'svelte/store'

export const isDarkMode = writable(false)

export const theme = derived(isDarkMode, ($isDarkMode) => ({
  colors: {
    bg: $isDarkMode ? '#1a1a1a' : '#faf8f3',
    text: $isDarkMode ? '#f5f5f5' : '#2a2a2a',
    accent: '#d4a574',
    accentDark: '#8b4513',
    border: $isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)',
  },
  shadows: {
    small: $isDarkMode
      ? 'rgba(0,0,0,0.3)'
      : 'rgba(0,0,0,0.1)',
    medium: $isDarkMode
      ? 'rgba(0,0,0,0.4)'
      : 'rgba(0,0,0,0.15)',
  },
}))
```

## Example 4: Accessible Form with Validation

This example demonstrates Phase 7 (Accessibility) with proper semantic HTML, ARIA attributes, and keyboard navigation.

```svelte
<!-- lib/components/Form.svelte -->
<script lang="ts">
  import { slide } from 'svelte/transition'
  import { cubicOut } from 'svelte/easing'

  interface FormData {
    email: string
    message: string
  }

  let formData: FormData = $state({
    email: '',
    message: '',
  })

  let errors: Partial<FormData> = $state({})
  let isSubmitting = $state(false)
  let isSubmitted = $state(false)

  async function handleSubmit(e: SubmitEvent) {
    e.preventDefault()
    errors = {}

    // Validation
    if (!formData.email) {
      errors.email = 'Email is required'
    } else if (!formData.email.includes('@')) {
      errors.email = 'Please enter a valid email'
    }

    if (!formData.message) {
      errors.message = 'Message is required'
    }

    if (Object.keys(errors).length > 0) return

    isSubmitting = true
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000))
    isSubmitting = false
    isSubmitted = true
  }
</script>

<form on:submit={handleSubmit} novalidate aria-label="Contact form">
  <fieldset disabled={isSubmitting}>
    <!-- Email input -->
    <div class="form-group">
      <label for="email">Email address</label>
      <input
        id="email"
        type="email"
        bind:value={formData.email}
        required
        aria-required="true"
        aria-describedby={errors.email ? 'email-error' : 'email-hint'}
        aria-invalid={!!errors.email}
      />
      <small id="email-hint">We'll never share your email.</small>
      {#if errors.email}
        <div
          id="email-error"
          class="error-message"
          role="alert"
          in:slide={{ duration: 300, easing: cubicOut }}
        >
          {errors.email}
        </div>
      {/if}
    </div>

    <!-- Message textarea -->
    <div class="form-group">
      <label for="message">Message</label>
      <textarea
        id="message"
        bind:value={formData.message}
        required
        aria-required="true"
        aria-describedby={errors.message ? 'message-error' : 'message-hint'}
        aria-invalid={!!errors.message}
        rows="5"
      />
      <small id="message-hint">Maximum 500 characters.</small>
      {#if errors.message}
        <div
          id="message-error"
          class="error-message"
          role="alert"
          in:slide={{ duration: 300, easing: cubicOut }}
        >
          {errors.message}
        </div>
      {/if}
    </div>

    <!-- Submit button -->
    <button type="submit" aria-busy={isSubmitting}>
      {#if isSubmitting}
        <span>Sending...</span>
      {:else}
        <span>Send Message</span>
      {/if}
    </button>
  </fieldset>

  <!-- Success message -->
  {#if isSubmitted}
    <div
      class="success-message"
      role="status"
      aria-live="polite"
      in:slide={{ duration: 400, easing: cubicOut }}
    >
      ✓ Message sent successfully!
    </div>
  {/if}
</form>

<style>
  form {
    max-width: 500px;
    margin: 0 auto;
  }

  fieldset {
    border: none;
    padding: 0;
    margin: 0;
  }

  fieldset:disabled {
    opacity: 0.6;
    pointer-events: none;
  }

  .form-group {
    margin-bottom: calc(var(--spacing-unit) * 3);
  }

  label {
    display: block;
    font-family: var(--font-body);
    font-weight: 600;
    font-size: 14px;
    margin-bottom: calc(var(--spacing-unit));
    color: var(--color-text);
  }

  input,
  textarea {
    width: 100%;
    padding: calc(var(--spacing-unit) * 1.5);
    font-family: var(--font-body);
    font-size: 14px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 6px;
    transition: all 0.3s ease-out;
    box-sizing: border-box;
  }

  input:focus,
  textarea:focus {
    outline: none;
    border-color: var(--color-accent);
    box-shadow: 0 0 0 2px rgba(212, 165, 116, 0.1);
  }

  input[aria-invalid='true'],
  textarea[aria-invalid='true'] {
    border-color: #d32f2f;
  }

  small {
    display: block;
    font-size: 12px;
    color: rgba(42, 42, 42, 0.6);
    margin-top: calc(var(--spacing-unit) * 0.5);
  }

  .error-message {
    font-size: 12px;
    color: #d32f2f;
    margin-top: calc(var(--spacing-unit));
    font-weight: 500;
  }

  button {
    width: 100%;
    padding: calc(var(--spacing-unit) * 2);
    background: var(--color-accent);
    color: white;
    border: none;
    border-radius: 6px;
    font-family: var(--font-body);
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease-out;
  }

  button:hover:not(:disabled) {
    background: var(--color-accent-dark);
    transform: translateY(-2px);
  }

  button:focus {
    outline: 2px solid var(--color-accent-dark);
    outline-offset: 2px;
  }

  button:disabled {
    opacity: 0.7;
  }

  .success-message {
    padding: calc(var(--spacing-unit) * 2);
    background: #4caf50;
    color: white;
    border-radius: 6px;
    text-align: center;
    font-weight: 500;
    margin-top: calc(var(--spacing-unit) * 2);
  }
</style>
```

## Example 5: Mobile-First Responsive Navigation

This example demonstrates Phase 5 (Responsive Design) with Svelte state management and mobile-first approach.

```svelte
<!-- lib/components/Navigation.svelte -->
<script lang="ts">
  import { slide } from 'svelte/transition'
  import { fly } from 'svelte/transition'
  import { cubicOut } from 'svelte/easing'

  let isOpen = $state(false)
  let isMobile = $state(false)

  let windowWidth = $state(0)

  $effect(() => {
    isMobile = windowWidth < 768
    if (!isMobile) {
      isOpen = false
    }
  })

  function toggleMenu() {
    isOpen = !isOpen
  }

  function closeMenu() {
    isOpen = false
  }
</script>

<svelte:window bind:innerWidth={windowWidth} />

<nav class="navigation" aria-label="Main navigation">
  <div class="nav-container">
    <a href="/" class="nav-logo">Design</a>

    <!-- Mobile menu button -->
    {#if isMobile}
      <button
        class="menu-button"
        aria-expanded={isOpen}
        aria-controls="nav-menu"
        on:click={toggleMenu}
        aria-label="Toggle navigation menu"
      >
        <span class="menu-icon" />
      </button>
    {/if}

    <!-- Navigation menu -->
    <ul
      id="nav-menu"
      class="nav-menu"
      class:is-open={isOpen && isMobile}
      hidden={isMobile && !isOpen}
    >
      {#each ['Features', 'Docs', 'Examples', 'Contact'] as item (item)}
        {#if isMobile}
          <li
            in:slide={{
              duration: 300,
              easing: cubicOut,
            }}
          >
            <a href="/{item.toLowerCase()}" on:click={closeMenu}>
              {item}
            </a>
          </li>
        {:else}
          <li>
            <a href="/{item.toLowerCase()}">
              {item}
            </a>
          </li>
        {/if}
      {/each}
    </ul>
  </div>
</nav>

<style>
  .navigation {
    background: var(--color-bg);
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: calc(var(--spacing-unit) * 2) calc(var(--spacing-unit) * 4);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .nav-logo {
    font-family: var(--font-display);
    font-size: 24px;
    font-weight: 700;
    color: var(--color-accent);
    text-decoration: none;
    transition: color 0.3s ease-out;
  }

  .nav-logo:hover {
    color: var(--color-accent-dark);
  }

  .menu-button {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: calc(var(--spacing-unit));
    width: 44px;
    height: 44px;
    position: relative;
  }

  .menu-icon {
    display: block;
    width: 24px;
    height: 2px;
    background: var(--color-text);
    position: relative;
    transition: all 0.3s ease-out;
  }

  .menu-icon::before,
  .menu-icon::after {
    content: '';
    position: absolute;
    width: 24px;
    height: 2px;
    background: var(--color-text);
    transition: all 0.3s ease-out;
  }

  .menu-icon::before {
    top: -8px;
  }

  .menu-icon::after {
    bottom: -8px;
  }

  .menu-button[aria-expanded='true'] .menu-icon {
    background: transparent;
  }

  .menu-button[aria-expanded='true'] .menu-icon::before {
    transform: rotate(45deg);
    top: 0;
  }

  .menu-button[aria-expanded='true'] .menu-icon::after {
    transform: rotate(-45deg);
    bottom: 0;
  }

  .nav-menu {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: calc(var(--spacing-unit) * 4);
  }

  .nav-menu a {
    font-family: var(--font-body);
    color: var(--color-text);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease-out;
    position: relative;
  }

  .nav-menu a:hover {
    color: var(--color-accent);
  }

  .nav-menu a::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--color-accent);
    transition: width 0.3s ease-out;
  }

  .nav-menu a:hover::after {
    width: 100%;
  }

  /* Mobile styles */
  @media (max-width: 767px) {
    .nav-container {
      padding: calc(var(--spacing-unit) * 2);
    }

    .menu-button {
      display: block;
    }

    .nav-menu {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      flex-direction: column;
      gap: calc(var(--spacing-unit) * 2);
      padding: calc(var(--spacing-unit) * 2);
      background: var(--color-bg);
      border-bottom: 1px solid rgba(0, 0, 0, 0.08);
      max-height: 0;
      overflow: hidden;
    }

    .nav-menu.is-open {
      max-height: 400px;
    }

    .nav-menu a::after {
      display: none;
    }

    .nav-menu a:active {
      color: var(--color-accent);
    }
  }
</style>
```

## Design System Files

All examples assume these design tokens are defined in your CSS:

```css
/* $lib/styles/tokens.css */
:root {
  /* Typography */
  --font-display: 'Playfair Display', serif;
  --font-body: 'IBM Plex Sans', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Font sizes */
  --size-display: 88px;
  --size-h1: 48px;
  --size-h2: 28px;
  --size-h3: 20px;
  --size-body: 16px;
  --size-small: 13px;

  /* Colors */
  --color-bg: #faf8f3;
  --color-text: #2a2a2a;
  --color-accent: #d4a574;
  --color-accent-dark: #8b4513;

  /* Spacing */
  --spacing-unit: 8px;

  /* Motion */
  --easing-out: cubic-bezier(0.16, 0.04, 0.04, 1);
  --easing-elastic: cubic-bezier(0.34, 1.56, 0.64, 1);
  --duration-quick: 200ms;
  --duration-standard: 400ms;
  --duration-slow: 600ms;
}
```

## Key Takeaways

1. **Orchestrated Motion**: Use staggered delays and easing functions for sophisticated animations
2. **Reactive Styling**: Use `$derived` for computed style values
3. **Component Typing**: Always type component props with interfaces
4. **Scoped Styles**: Let Svelte's default scoping handle style isolation
5. **CSS Variables**: Store design tokens in CSS variables for theming
6. **Accessibility**: Include ARIA attributes, semantic HTML, and keyboard navigation
7. **Mobile-First**: Build mobile experience first, enhance for larger screens
8. **Store Management**: Use stores for theme switching and global UI state

All these examples follow the 8-phase workflow and anti-generic-AI checklist from SKILL.md.
