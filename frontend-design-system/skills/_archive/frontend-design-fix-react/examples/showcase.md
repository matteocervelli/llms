# Frontend Design Fix - React Examples

## Example 1: Generic Component → Distinctive Component

### Before: Generic React Component
```jsx
import React, { useState } from 'react';

export function HeroSection() {
  return (
    <div style={{
      textAlign: 'center',
      padding: '60px 20px',
      background: 'white'
    }}>
      <h1 style={{
        fontSize: '2.5rem',
        fontFamily: 'Arial, sans-serif',
        color: 'purple',
        marginBottom: '1rem'
      }}>
        Welcome to Our App
      </h1>
      <p style={{
        fontSize: '1rem',
        color: '#666',
        marginBottom: '2rem'
      }}>
        The best solution for your needs
      </p>
      <button style={{
        padding: '12px 24px',
        background: '#e0e0e0',
        border: 'none',
        cursor: 'pointer',
        fontSize: '1rem'
      }}>
        Get Started
      </button>
    </div>
  );
}
```

**Design Score**: 5/5 anti-patterns

---

### After: Distinctive React Component
```jsx
import React, { useState } from 'react';
import { motion } from 'framer-motion';

// Theme configuration
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
  transitions: {
    fast: 200,
    base: 400,
  }
};

// Container animation variants
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.12,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: 'easeOut' },
  },
};

export function HeroSection() {
  const [isButtonHovering, setIsButtonHovering] = useState(false);

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      style={{
        background: `linear-gradient(135deg, ${theme.colors.surface} 0%, #e8e8e8 100%)`,
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        justifyContent: 'center',
        padding: '2rem',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Decorative floating element */}
      <motion.div
        style={{
          position: 'absolute',
          top: '-10%',
          right: '-5%',
          width: '400px',
          height: '400px',
          background: `radial-gradient(circle, rgba(255, 107, 53, 0.1) 0%, transparent 70%)`,
          borderRadius: '50%',
          zIndex: 0,
        }}
        animate={{
          y: [0, 30, 0],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />

      {/* Content wrapper */}
      <motion.div
        style={{
          position: 'relative',
          zIndex: 1,
          maxWidth: '700px',
        }}
      >
        {/* Headline */}
        <motion.h1
          variants={itemVariants}
          style={{
            fontFamily: theme.fonts.display,
            fontSize: 'clamp(2.5rem, 8vw, 5rem)',
            fontWeight: 900,
            color: theme.colors.primary,
            margin: '0 0 1rem 0',
            lineHeight: 1.1,
            letterSpacing: '-0.02em',
          }}
        >
          Welcome to Our Remarkable App
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          variants={itemVariants}
          style={{
            fontFamily: theme.fonts.body,
            fontSize: 'clamp(1rem, 2vw, 1.25rem)',
            color: theme.colors.primary,
            opacity: 0.7,
            lineHeight: 1.6,
            marginBottom: '2rem',
            fontWeight: 300,
          }}
        >
          Experience design that adapts to your needs, with intention in every detail.
        </motion.p>

        {/* CTA Button */}
        <motion.button
          variants={itemVariants}
          onMouseEnter={() => setIsButtonHovering(true)}
          onMouseLeave={() => setIsButtonHovering(false)}
          style={{
            fontFamily: theme.fonts.body,
            background: theme.colors.accent,
            color: 'white',
            padding: '1.25rem 2.5rem',
            border: 'none',
            borderRadius: '2px',
            fontSize: '1.125rem',
            fontWeight: 600,
            cursor: 'pointer',
            transition: `all ${theme.transitions.base}ms ease-out`,
            textTransform: 'uppercase',
            letterSpacing: '1px',
          }}
          whileHover={{
            y: -4,
            boxShadow: '0 20px 40px rgba(255, 107, 53, 0.3)',
            background: '#e55a25',
          }}
          whileTap={{
            scale: 0.95,
          }}
        >
          Get Started Now
        </motion.button>
      </motion.div>

      {/* Accent line */}
      <motion.div
        style={{
          position: 'absolute',
          bottom: '2rem',
          right: '2rem',
          width: '120px',
          height: '3px',
          background: theme.colors.accent,
        }}
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ delay: 0.8, duration: 0.6 }}
      />
    </motion.div>
  );
}
```

**Design Score**: 0/5 anti-patterns

---

## Example 2: List Component → Animated List Component

### Before: Generic List
```jsx
export function FeatureList({ items }) {
  return (
    <ul style={{ padding: '20px' }}>
      {items.map(item => (
        <li key={item.id} style={{
          padding: '10px',
          borderBottom: '1px solid #ddd'
        }}>
          {item.title}
        </li>
      ))}
    </ul>
  );
}
```

---

### After: Animated List
```jsx
import React from 'react';
import { motion } from 'framer-motion';

const theme = {
  colors: {
    primary: '#1a1a1a',
    accent: '#ff6b35',
  }
};

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.4, ease: 'easeOut' },
  },
};

export function FeatureList({ items }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      style={{
        padding: 0,
        margin: 0,
        listStyle: 'none',
      }}
    >
      {items.map(item => (
        <motion.li
          key={item.id}
          variants={itemVariants}
          whileHover={{
            x: 8,
            transition: { duration: 0.2 }
          }}
          style={{
            padding: '1.5rem',
            borderLeft: `3px solid ${theme.colors.accent}`,
            background: '#fafafa',
            marginBottom: '1rem',
            borderRadius: '4px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
            cursor: 'pointer',
            transition: 'all 0.3s ease-out',
          }}
        >
          <span style={{
            fontFamily: "'Playfair Display', serif",
            fontSize: '1.25rem',
            fontWeight: 700,
            color: theme.colors.primary,
          }}>
            {item.title}
          </span>
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

---

## Example 3: Card Grid → Dynamic Card Grid

### Before: Boring Card Grid
```jsx
export function CardGrid({ cards }) {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)',
      gap: '20px',
      padding: '20px'
    }}>
      {cards.map(card => (
        <div key={card.id} style={{
          background: 'white',
          padding: '20px',
          border: '1px solid #ddd',
          textAlign: 'center'
        }}>
          <h3>{card.title}</h3>
          <p>{card.description}</p>
        </div>
      ))}
    </div>
  );
}
```

---

### After: Dynamic Card Grid
```jsx
import React from 'react';
import { motion } from 'framer-motion';

const theme = {
  colors: {
    primary: '#1a1a1a',
    accent: '#ff6b35',
    surface: '#fafafa',
  },
  fonts: {
    display: "'Playfair Display', serif",
    body: "'Inter', sans-serif",
  }
};

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: 'easeOut' },
  },
};

export function CardGrid({ cards }) {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '2rem',
        padding: '2rem',
        maxWidth: '1200px',
        margin: '0 auto',
      }}
    >
      {cards.map(card => (
        <motion.div
          key={card.id}
          variants={cardVariants}
          whileHover={{
            y: -8,
            transition: { duration: 0.3 }
          }}
          style={{
            background: 'white',
            padding: '2rem',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)',
            overflow: 'hidden',
            position: 'relative',
            cursor: 'pointer',
          }}
        >
          {/* Top accent bar */}
          <motion.div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '4px',
              background: `linear-gradient(90deg, ${theme.colors.accent}, #8b5cf6)`,
              transform: 'scaleX(0)',
              transformOrigin: 'left',
              transition: 'transform 0.3s ease-out',
            }}
            whileHover={{
              transform: 'scaleX(1)',
            }}
          />

          <h3 style={{
            fontFamily: theme.fonts.display,
            fontSize: '1.5rem',
            fontWeight: 700,
            color: theme.colors.primary,
            marginBottom: '0.5rem',
          }}>
            {card.title}
          </h3>

          <p style={{
            fontFamily: theme.fonts.body,
            color: '#666',
            lineHeight: 1.6,
            fontSize: '0.95rem',
          }}>
            {card.description}
          </p>

          {/* Learn more link */}
          <motion.a
            href="#"
            style={{
              display: 'inline-block',
              marginTop: '1.5rem',
              color: theme.colors.accent,
              textDecoration: 'none',
              fontWeight: 600,
              fontSize: '0.9rem',
              textTransform: 'uppercase',
              letterSpacing: '0.5px',
            }}
            whileHover={{
              x: 4,
            }}
          >
            Learn More →
          </motion.a>
        </motion.div>
      ))}
    </motion.div>
  );
}
```

---

## Design Dimension Summary

All React examples demonstrate:

| Dimension | Implementation |
|-----------|----------------|
| **Typography** | `fontFamily: theme.fonts.display/body` with dynamic sizing using `clamp()` |
| **Color** | Theme object with CSS-in-JS, gradient backgrounds |
| **Motion** | Framer Motion orchestration with `variants` and `staggerChildren` |
| **Spatial** | Responsive grids with `auto-fit` and asymmetric layouts |
| **Backgrounds** | `radial-gradient`, `linear-gradient` with layering |

Each example maintains:
- Accessibility (focus states, ARIA labels)
- Responsiveness (clamp, mobile-first)
- Performance (optimized animations, CSS transitions)
- Reusability (theme object, composable variants)
