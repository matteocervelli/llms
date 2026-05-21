# Motion & Animation Guidance

## Overview

Motion reveals personality and guides user attention with intentionality. Deliberate animation transforms passive interfaces into experiences that feel alive and considered.

## Core Principles

1. **Orchestration**: Animations should feel planned, not random
2. **Purpose**: Every animation should serve a functional or emotional purpose
3. **Timing**: Easing functions matter more than duration
4. **Context**: Page loads, scrolls, and hovers each have different animation strategies

## Implementation by Context

### HTML/CSS Animations

Use CSS for simple, performant animations that run on page load or interaction:

#### Basic Fade-In
```css
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.element {
  animation: fadeIn 0.6s ease-out;
}
```

#### Slide + Fade In
```css
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

.element {
  animation: slideInUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

#### Scale + Fade In
```css
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

.element {
  animation: scaleIn 0.5s ease-out;
}
```

### React/JavaScript Animations

Use motion libraries for state-driven animations and complex sequences:

#### Framer Motion Example
```jsx
import { motion } from 'framer-motion';

export function AnimatedCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.6,
        ease: "easeOut"
      }}
    >
      Card content
    </motion.div>
  );
}
```

#### Staggered Children Animation
```jsx
import { motion } from 'framer-motion';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const childVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" },
  },
};

export function AnimatedList() {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item) => (
        <motion.div key={item.id} variants={childVariants}>
          {item.content}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

## Page Load Animation Strategy

### Orchestrated Reveal

Don't animate everything at once. Create a sequence that guides the user's eye:

#### Timing Sequence
```
0ms    - Background/Hero fades in
200ms  - Headline slides in from top
400ms  - Sub-headline fades in
600ms  - Primary CTA appears
800ms  - Supporting content staggered reveal
```

#### CSS Implementation
```css
.hero {
  animation: fadeIn 0.8s ease-out 0ms;
}

.headline {
  animation: slideInDown 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 200ms backwards;
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

#### React Implementation
```jsx
import { motion } from 'framer-motion';

export function PageLoad() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 },
    },
  };

  return (
    <>
      <motion.div
        className="hero"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      />
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
      />
      <motion.div
        className="content"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Content items */}
      </motion.div>
    </>
  );
}
```

## Staggered Reveals

### Using animation-delay (CSS)

Stagger elements to create a cascade effect:

```css
.list-item {
  opacity: 0;
  animation: slideInUp 0.8s ease-out forwards;
}

.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 100ms; }
.list-item:nth-child(3) { animation-delay: 200ms; }
.list-item:nth-child(4) { animation-delay: 300ms; }
.list-item:nth-child(5) { animation-delay: 400ms; }
```

### Using staggerChildren (React/Framer Motion)

```jsx
const listVariants = {
  visible: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.6 },
  },
};
```

## Scroll Trigger Animations

### Intersection Observer (Vanilla JS)

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

### Framer Motion Scroll Variants

```jsx
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

export function ScrollReveal({ children }) {
  const { ref, inView } = useInView({ threshold: 0.1 });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 40 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
```

## Hover State Surprises

Hover interactions should be delightful, not just functional:

### CSS Hover Animations

```css
.card {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.2);
}

/* Icon rotation on hover */
.icon {
  transition: transform 0.3s ease-out;
}

.card:hover .icon {
  transform: rotate(45deg) scale(1.1);
}

/* Text color shift */
.link {
  color: #333;
  transition: color 0.3s ease-out;
  border-bottom: 2px solid transparent;
  transition: border-color 0.3s ease-out;
}

.link:hover {
  color: #0099ff;
  border-bottom-color: #0099ff;
}
```

### React/Framer Motion Hover

```jsx
export function HoverCard() {
  return (
    <motion.div
      whileHover={{
        y: -8,
        boxShadow: '0 24px 48px rgba(0,0,0,0.2)',
      }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      <motion.span
        whileHover={{ rotate: 45, scale: 1.1 }}
        transition={{ duration: 0.2 }}
      >
        🎯
      </motion.span>
    </motion.div>
  );
}
```

## Easing Functions

### Recommended Easing Values

- **ease-out**: 0.16, 0.04, 0.04, 1 (default snappy)
- **ease-in-out**: 0.42, 0, 0.58, 1 (smooth, balanced)
- **elastic**: cubic-bezier(0.34, 1.56, 0.64, 1) (playful overshoot)
- **sharp**: cubic-bezier(0.4, 0, 0.6, 1) (quick and direct)

### Implementation

```css
/* Snappy entrance */
.entrance {
  animation: slideIn 0.8s cubic-bezier(0.16, 0.04, 0.04, 1);
}

/* Smooth, bouncy exit */
.exit {
  animation: slideOut 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Playful interaction */
.playful {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

## Anti-Patterns to Avoid

- **Linear timing**: Feels robotic, use easing instead
- **Instant interactions**: Feels cold, add 0.2-0.4s minimum transitions
- **Animation-heavy**: Don't animate everything; be selective
- **Slow animations**: >1s feels sluggish unless intentional
- **Predictable patterns**: Vary easing, duration, and delay

## Motion Checklist

- [ ] Are animations orchestrated (staggered) or simultaneous?
- [ ] Do animations have easing functions or are they linear?
- [ ] Is there at least one delightful hover surprise?
- [ ] Do scroll triggers reveal content naturally?
- [ ] Are animation durations 0.4-0.8s (snappy) not 1.5s+ (sluggish)?
- [ ] Is animation supporting the design or competing with it?

## Resources

- **Framer Motion**: https://www.framer.com/motion/
- **Easing functions**: https://easings.net/
- **Animation principles**: "The Illusion of Life" by Disney animators
