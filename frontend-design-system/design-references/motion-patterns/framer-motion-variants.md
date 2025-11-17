# Framer Motion Variants & Orchestrated Animations

Orchestrate complex entrance sequences with Framer Motion's variant system. Stagger children, control timing, and compose multiple animations into coordinated page loads.

## Basic Variant Pattern

```jsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.3,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

export function PageLoadStagger() {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.h1 variants={itemVariants}>Headline</motion.h1>
      <motion.p variants={itemVariants}>Description</motion.p>
      <motion.button variants={itemVariants}>CTA</motion.button>
    </motion.div>
  );
}
```

**Result**: Each child animates 0.1s after previous, starting 0.3s after parent.

## Stagger Children Examples

### Sequential Reveal (List)
```jsx
const listContainerVariants = {
  visible: {
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.2,
    },
  },
};

const listItemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.4 } },
};

export function ListReveal({ items }) {
  return (
    <motion.ul
      variants={listContainerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item) => (
        <motion.li key={item.id} variants={listItemVariants}>
          {item.text}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### Grid Stagger (Masonry)
```jsx
const gridVariants = {
  visible: {
    transition: {
      staggerChildren: 0.08,
    },
  },
};

const cardVariants = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

export function CardGrid({ cards }) {
  return (
    <motion.div
      className="grid grid-cols-3"
      variants={gridVariants}
      initial="hidden"
      animate="visible"
    >
      {cards.map((card) => (
        <motion.div key={card.id} variants={cardVariants}>
          {/* Card content */}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

## Scroll-Triggered Animation with useScroll

```jsx
import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";

export function ScrollTriggerReveal() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start 0.8", "start 0.2"],
  });

  const opacity = useTransform(scrollYProgress, [0, 1], [0, 1]);
  const y = useTransform(scrollYProgress, [0, 1], [40, 0]);

  return (
    <motion.section ref={ref} style={{ opacity, y }}>
      <h2>Revealed on scroll</h2>
      <p>This section fades in as you scroll past.</p>
    </motion.section>
  );
}
```

**Timing**: Start reveal at 80% of viewport, complete at 20%.

## Hover State Variants

```jsx
const buttonVariants = {
  rest: {
    background: "#3b82f6",
    scale: 1,
    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
  },
  hover: {
    background: "#2563eb",
    scale: 1.05,
    boxShadow: "0 12px 20px rgba(59, 130, 246, 0.4)",
    transition: {
      duration: 0.2,
      ease: "easeOut",
    },
  },
  tap: {
    scale: 0.98,
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
  },
};

export function HoverButton() {
  return (
    <motion.button
      variants={buttonVariants}
      initial="rest"
      whileHover="hover"
      whileTap="tap"
    >
      Click me
    </motion.button>
  );
}
```

## Page Load Orchestration (Complex)

```jsx
const pageVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const fadeInUp = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] },
  },
};

const scaleIn = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.5, ease: "easeOut" },
  },
};

export function HeroPage() {
  return (
    <motion.section
      variants={pageVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div className="logo" variants={scaleIn} />
      <motion.h1 variants={fadeInUp}>Hero headline</motion.h1>
      <motion.p variants={fadeInUp}>Subheading or description</motion.p>
      <motion.button variants={fadeInUp}>Primary CTA</motion.button>
    </motion.section>
  );
}
```

**Timeline**: Logo scales in first (0.2s delay), then headline, subheading, and CTA stagger in at 0.1s intervals.

## Copy-Paste Ready Snippets

### Exit Animation
```jsx
const exitVariants = {
  exit: {
    opacity: 0,
    y: -40,
    transition: { duration: 0.3 },
  },
};

<motion.div
  variants={exitVariants}
  initial="visible"
  exit="exit"
/>
```

### Entrance + Exit (AnimatePresence)
```jsx
import { AnimatePresence } from "framer-motion";

export function ModalWithAnimation({ isOpen }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          {/* Modal content */}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

## References

See **css-animations.json** for CSS-only alternatives when JavaScript animations aren't needed or when performance requires lightweight solutions.
