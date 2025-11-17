# Motion & Animation Fixes

Add orchestrated page loads, staggered reveals, hover surprises, and scroll triggers to static designs.

## Quick Fixes

### Fix 1: Orchestrated Page Load

**Timing:**
- Stagger elements 100–150ms apart
- Total sequence: 500–1000ms
- Easing: cubic-bezier (not linear)

**React (Framer Motion):**
```jsx
const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
};
```

### Fix 2: Staggered Reveals (Lists/Grids)

**Pattern:** 0ms → 80–120ms → 160–240ms...

```jsx
const itemVariant = {
  hidden: { opacity: 0, y: 40 },
  visible: {
    opacity: 1, y: 0,
    transition: { duration: 0.5, ease: [0.34, 1.56, 0.64, 1] }
  }
};
```

### Fix 3: Hover Surprises

**Techniques:** Scale 1.05x, shadow lift, color shift, rotate icon

**CSS:**
```css
button {
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}
button:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
button:active {
  transform: scale(0.98);
}
```

### Fix 4: Scroll Trigger Animations

```jsx
const [isVisible, setIsVisible] = useState(false);

useEffect(() => {
  const observer = new IntersectionObserver(
    ([entry]) => setIsVisible(entry.isIntersecting),
    { threshold: 0.2 }
  );
  observer.observe(ref.current);
}, []);

<motion.section
  initial={{ opacity: 0, y: 60 }}
  animate={isVisible ? { opacity: 1, y: 0 } : {}}
/>
```

### Fix 5: Consistent Easing

```css
:root {
  --ease-out: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-snappy: cubic-bezier(0.4, 0, 0.2, 1);
}

button { transition: all 0.2s var(--ease-snappy); }
.card { transition: all 0.4s var(--ease-out); }
```

---

## Checklist

- [ ] Page load orchestrated (500–1000ms, staggered)
- [ ] List/grid items reveal staggered
- [ ] Hover states have scale, shadow, color
- [ ] Scroll triggers animate into viewport
- [ ] Consistent cubic-bezier easing (not linear)
- [ ] Duration snappy (< 600ms)
- [ ] `prefers-reduced-motion` respected
- [ ] 60fps performance maintained

---

See: `/skills/frontend-design/sub-skills/motion.md` for full principles
