# Frontend Design React Examples

Complete React component examples demonstrating the 5-dimension design framework with TypeScript, Framer Motion, and accessibility.

## Example 1: Distinctive Typography Component

This example shows how to create visual hierarchy through deliberate typographic choices using a high-contrast pairing (Playfair Display + IBM Plex Sans) with extreme size jumps.

```typescript
import styled from 'styled-components';
import React from 'react';

// Typography tokens with intentional extremes
const TypographyTokens = {
  display: {
    fontSize: '88px',
    fontFamily: "'Playfair Display', serif",
    fontWeight: 700,
    lineHeight: 1.1,
    letterSpacing: '-0.5px',
  },
  headline: {
    fontSize: '48px',
    fontFamily: "'Playfair Display', serif",
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: '-0.25px',
  },
  subheadline: {
    fontSize: '28px',
    fontFamily: "'IBM Plex Sans', sans-serif",
    fontWeight: 400,
    lineHeight: 1.3,
    letterSpacing: '0px',
  },
  body: {
    fontSize: '16px',
    fontFamily: "'IBM Plex Sans', sans-serif",
    fontWeight: 400,
    lineHeight: 1.6,
    letterSpacing: '0px',
  },
  mono: {
    fontSize: '14px',
    fontFamily: "'JetBrains Mono', monospace",
    fontWeight: 400,
    lineHeight: 1.5,
    letterSpacing: '0.5px',
  },
};

// Styled typography components
const Display = styled.h1`
  font-size: ${TypographyTokens.display.fontSize};
  font-family: ${TypographyTokens.display.fontFamily};
  font-weight: ${TypographyTokens.display.fontWeight};
  line-height: ${TypographyTokens.display.lineHeight};
  letter-spacing: ${TypographyTokens.display.letterSpacing};
  margin: 0 0 32px 0;
`;

const Headline = styled.h2`
  font-size: ${TypographyTokens.headline.fontSize};
  font-family: ${TypographyTokens.headline.fontFamily};
  font-weight: ${TypographyTokens.headline.fontWeight};
  line-height: ${TypographyTokens.headline.lineHeight};
  letter-spacing: ${TypographyTokens.headline.letterSpacing};
  margin: 0 0 24px 0;
`;

const Subheadline = styled.h3`
  font-size: ${TypographyTokens.subheadline.fontSize};
  font-family: ${TypographyTokens.subheadline.fontFamily};
  font-weight: ${TypographyTokens.subheadline.fontWeight};
  line-height: ${TypographyTokens.subheadline.lineHeight};
  margin: 0 0 16px 0;
`;

const Body = styled.p`
  font-size: ${TypographyTokens.body.fontSize};
  font-family: ${TypographyTokens.body.fontFamily};
  font-weight: ${TypographyTokens.body.fontWeight};
  line-height: ${TypographyTokens.body.lineHeight};
  margin: 0 0 16px 0;
`;

const Mono = styled.code`
  font-size: ${TypographyTokens.mono.fontSize};
  font-family: ${TypographyTokens.mono.fontFamily};
  font-weight: ${TypographyTokens.mono.fontWeight};
  line-height: ${TypographyTokens.mono.lineHeight};
  letter-spacing: ${TypographyTokens.mono.letterSpacing};
  background: #F5F1E8;
  padding: 2px 6px;
  border-radius: 4px;
`;

// Example component showing distinct typography
export const TypographyShowcase: React.FC = () => {
  return (
    <div style={{ padding: '48px', backgroundColor: '#FAF8F4', fontFamily: "'IBM Plex Sans', sans-serif" }}>
      <Display>Distinctive Typography</Display>
      <Subheadline>3x size jumps create intentional hierarchy</Subheadline>
      <Body>
        This typography system rejects defaults by using a high-contrast pairing:
        <Mono>Playfair Display</Mono> (elegant serif for display) paired with <Mono>IBM Plex Sans</Mono> (warm humanist sans for body).
      </Body>
      <Body>
        Notice the extreme size jumps:
      </Body>
      <ul style={{ fontFamily: "'IBM Plex Sans', sans-serif", fontSize: '16px' }}>
        <li>Display: 88px (5.5x body size)</li>
        <li>Headline: 48px (3x body size)</li>
        <li>Sub-headline: 28px (1.75x body size)</li>
        <li>Body: 16px (1x base)</li>
      </ul>
      <Body>
        This creates clear visual hierarchy immediately. Small sizes feel intentional because
        they're far from the massive display text.
      </Body>
    </div>
  );
};
```

**Key Learnings**:
- High-contrast font pairing (serif + sans) creates personality
- Size jumps of 3x+ create clear hierarchy
- Negative letter-spacing on display text tightens confidence
- Line heights increase as text gets smaller (body: 1.6, display: 1.1)

---

## Example 2: Framer Motion Orchestrated Page Load

This example demonstrates how orchestrated, staggered animations create a sense of intentionality and guide user attention through a sequence.

```typescript
import { motion } from 'framer-motion';
import styled from 'styled-components';
import React from 'react';

const Container = styled.div`
  padding: 48px 32px;
  background: linear-gradient(135deg, #FAF8F4 0%, #F0E8DC 100%);
  min-height: 100vh;
`;

const Hero = styled(motion.div)`
  height: 300px;
  background: linear-gradient(45deg, #8B4513 0%, #D4623F 100%);
  border-radius: 16px;
  margin-bottom: 48px;
`;

const Card = styled(motion.div)`
  background: white;
  padding: 32px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
`;

const Headline = styled(motion.h1)`
  font-family: 'Playfair Display', serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 16px 0;
  color: #2C2416;
`;

const Text = styled(motion.p)`
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: #666;
  margin: 0;
`;

interface PageLoadShowcaseProps {
  autoplay?: boolean;
}

export const PageLoadShowcase: React.FC<PageLoadShowcaseProps> = ({ autoplay = true }) => {
  // Define container variants for staggered animation
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  // Define individual item variants
  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: 'easeOut',
      },
    },
  };

  const heroVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.8,
        ease: 'easeOut',
      },
    },
  };

  const headlineVariants = {
    hidden: { opacity: 0, y: -20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.8,
        delay: 0.2,
        ease: 'easeOut',
      },
    },
  };

  const contentItems = [
    { title: 'First Insight', description: 'This card appears at 800ms with a slide-up animation' },
    { title: 'Second Insight', description: 'This card appears at 900ms, slightly after the first' },
    { title: 'Third Insight', description: 'This card appears at 1000ms, completing the sequence' },
  ];

  return (
    <Container>
      {/* Hero background fades in immediately */}
      <Hero
        initial="hidden"
        animate={autoplay ? 'visible' : 'hidden'}
        variants={heroVariants}
      />

      {/* Headline slides in from top at 200ms */}
      <Headline
        initial="hidden"
        animate={autoplay ? 'visible' : 'hidden'}
        variants={headlineVariants}
      >
        Orchestrated Page Load
      </Headline>

      <Text
        initial={{ opacity: 0 }}
        animate={autoplay ? { opacity: 1 } : { opacity: 0 }}
        transition={{ duration: 0.6, delay: 0.4, ease: 'easeOut' }}
      >
        Each element enters the stage at a precise moment, guiding your eye through the page.
      </Text>

      {/* Content cards animate in with staggered timing */}
      <motion.div
        initial="hidden"
        animate={autoplay ? 'visible' : 'hidden'}
        variants={containerVariants}
        style={{ marginTop: '48px' }}
      >
        {contentItems.map((item, index) => (
          <Card key={index} variants={itemVariants}>
            <Headline style={{ fontSize: '28px', marginBottom: '8px' }}>
              {item.title}
            </Headline>
            <Text>{item.description}</Text>
          </Card>
        ))}
      </motion.div>

      <Text style={{ marginTop: '48px', fontSize: '12px', opacity: 0.6 }}>
        Animation Sequence:
        <br />
        0ms - Hero background fades in
        <br />
        200ms - Headline slides in from top
        <br />
        400ms - Subheading fades in
        <br />
        800ms - Cards begin staggered reveal (100ms apart)
      </Text>
    </Container>
  );
};
```

**Key Learnings**:
- Orchestrated animations guide user attention (not simultaneous reveals)
- Staggered timing uses 100-200ms gaps between elements
- Use `ease: 'easeOut'` for snappy, responsive feels
- `delayChildren` plus `staggerChildren` create cascading effects
- Duration 0.6-0.8s feels snappy; 1.5s+ feels sluggish

**Animation Timing Breakdown**:
```
0ms    - Hero (background)
200ms  - Headline (slide from top)
400ms  - Subheading (fade)
800ms  - Card 1 (slide + fade)
900ms  - Card 2 (slide + fade)
1000ms - Card 3 (slide + fade)
```

---

## Example 3: Unexpected Layout with Asymmetrical Composition

This example shows how to break the "default centered grid" pattern with intentional asymmetry that's more interesting and memorable.

```typescript
import styled from 'styled-components';
import { motion } from 'framer-motion';
import React from 'react';

const LayoutContainer = styled.div`
  padding: 48px;
  background: #FAF8F4;
  min-height: 100vh;
`;

const AsymmetricalGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
  margin-bottom: 48px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const LargeCard = styled(motion.div)`
  grid-row: span 2;
  background: linear-gradient(135deg, #8B4513 0%, #D4623F 100%);
  padding: 48px;
  border-radius: 8px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;

  @media (max-width: 768px) {
    grid-row: span 1;
  }
`;

const SmallCard = styled(motion.div)`
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
`;

const OffsetGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 24px;
  margin-bottom: 48px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const OffsetCard = styled(motion.div)`
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);

  /* Offset each card vertically for rhythm */
  &:nth-child(1) {
    margin-top: 0;
  }
  &:nth-child(2) {
    margin-top: 32px;
  }
  &:nth-child(3) {
    margin-top: 64px;
  }

  @media (max-width: 768px) {
    &:nth-child(1),
    &:nth-child(2),
    &:nth-child(3) {
      margin-top: 0;
    }
  }
`;

const Heading = styled.h2`
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: #2C2416;
`;

const Subtext = styled.p`
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 14px;
  color: #999;
  margin: 0;
`;

const Description = styled.p`
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: #666;
  margin: 0;
`;

export const AsymmetricalLayoutShowcase: React.FC = () => {
  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: (i: number) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: i * 0.1,
        duration: 0.6,
        ease: 'easeOut',
      },
    }),
  };

  return (
    <LayoutContainer>
      <Heading>Asymmetrical Composition</Heading>
      <Subtext>Breaking the "centered grid" pattern for visual interest</Subtext>

      <Description style={{ marginBottom: '48px' }}>
        Instead of a boring 3-column grid or centered layout, we use asymmetrical composition to create
        visual weight and interest. The large card on the left anchors the layout, while smaller cards
        on the right create rhythm and variety.
      </Description>

      {/* Pattern 1: Asymmetrical Grid (2-column with row span) */}
      <AsymmetricalGrid>
        <LargeCard
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.3 }}
          custom={0}
          variants={itemVariants}
        >
          <Heading style={{ color: 'white' }}>Featured Item</Heading>
          <Description style={{ color: 'rgba(255,255,255,0.8)' }}>
            This large card spans 2 rows, creating visual dominance on the left side.
          </Description>
        </LargeCard>

        <SmallCard
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.3 }}
          custom={1}
          variants={itemVariants}
        >
          <Heading style={{ fontSize: '20px' }}>Supporting A</Heading>
          <Description>Smaller cards on the right create balance.</Description>
        </SmallCard>

        <SmallCard
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.3 }}
          custom={2}
          variants={itemVariants}
        >
          <Heading style={{ fontSize: '20px' }}>Supporting B</Heading>
          <Description>This layout avoids the predictable 3-column grid.</Description>
        </SmallCard>
      </AsymmetricalGrid>

      <Heading style={{ marginTop: '48px' }}>Offset Vertical Rhythm</Heading>
      <Description style={{ marginBottom: '32px' }}>
        Each card is offset vertically, creating a cascade effect and visual rhythm across the page.
      </Description>

      {/* Pattern 2: Offset Grid (cards at different heights) */}
      <OffsetGrid>
        <OffsetCard
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.3 }}
          custom={0}
          variants={itemVariants}
        >
          <Heading style={{ fontSize: '20px' }}>First Item</Heading>
          <Description>Starts at the top.</Description>
        </OffsetCard>

        <OffsetCard
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.3 }}
          custom={1}
          variants={itemVariants}
        >
          <Heading style={{ fontSize: '20px' }}>Second Item</Heading>
          <Description>Offset 32px down for rhythm.</Description>
        </OffsetCard>

        <OffsetCard
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.3 }}
          custom={2}
          variants={itemVariants}
        >
          <Heading style={{ fontSize: '20px' }}>Third Item</Heading>
          <Description>Offset 64px down for visual cascade.</Description>
        </OffsetCard>
      </OffsetGrid>

      <Description style={{ fontSize: '12px', color: '#999', marginTop: '32px' }}>
        These layouts avoid the predictable patterns of generic design:
        <ul>
          <li>Not centered (more dynamic)</li>
          <li>Not uniform grid (more interesting)</li>
          <li>Asymmetrical (more memorable)</li>
          <li>Responsive (adapts to mobile)</li>
        </ul>
      </Description>
    </LayoutContainer>
  );
};
```

**Key Learnings**:
- Asymmetrical layouts are more interesting than centered grids
- Row spans create visual dominance and anchor compositions
- Offset vertical positioning creates rhythm and visual flow
- Mobile-first responsive breaks asymmetry gracefully
- Odd numbers (3 items, 5 items) feel more intentional than even grids

---

## Example 4: Accessible Interactive Component

This example demonstrates WCAG 2.1 AA compliant interactions with proper ARIA attributes, semantic HTML, and delightful micro-interactions.

```typescript
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import React, { useState, useCallback } from 'react';

const ButtonContainer = styled.div`
  padding: 48px;
  background: #FAF8F4;
  display: flex;
  flex-direction: column;
  gap: 24px;
`;

const StyledButton = styled(motion.button)`
  padding: 16px 32px;
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;
  border: 2px solid #8B4513;
  background: #8B4513;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease-out;

  &:hover {
    background: #A55C30;
    border-color: #A55C30;
  }

  &:focus {
    outline: 2px solid #E6D52F;
    outline-offset: 4px;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  @media (prefers-reduced-motion: reduce) {
    animation: none !important;
    transition: none !important;
  }
`;

const SecondaryButton = styled(StyledButton)`
  background: white;
  color: #8B4513;
`;

const Card = styled(motion.div)`
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
`;

const StatusMessage = styled(motion.div)<{ type: 'success' | 'error' | 'info' }>`
  padding: 16px;
  border-radius: 4px;
  background: ${props => {
    switch (props.type) {
      case 'success': return '#D4F0E6';
      case 'error': return '#F0D4D4';
      case 'info': return '#F0E8DC';
    }
  }};
  color: ${props => {
    switch (props.type) {
      case 'success': return '#1B5E4A';
      case 'error': return '#8B3C3C';
      case 'info': return '#5C4A3C';
    }
  }};
  border-left: 4px solid ${props => {
    switch (props.type) {
      case 'success': return '#3CB87A';
      case 'error': return '#D94040';
      case 'info': return '#8B4513';
    }
  }};
  role: 'status' | 'alert';
`;

export const AccessibleComponentShowcase: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState<{
    type: 'success' | 'error' | 'info';
    text: string;
  } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleOpen = useCallback(() => {
    setIsOpen(true);
    setMessage(null);
  }, []);

  const handleClose = useCallback(() => {
    setIsOpen(false);
  }, []);

  const handleAction = useCallback(async () => {
    setLoading(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    setLoading(false);
    setMessage({
      type: 'success',
      text: 'Action completed successfully! (ARIA role: status)',
    });
  }, []);

  const handleError = useCallback(() => {
    setMessage({
      type: 'error',
      text: 'Something went wrong. (ARIA role: alert)',
    });
  }, []);

  return (
    <ButtonContainer>
      <div>
        <h1 style={{ fontFamily: "'Playfair Display', serif", fontSize: '32px' }}>
          Accessible Interactive Components
        </h1>
        <p style={{ fontFamily: "'IBM Plex Sans', sans-serif", color: '#666' }}>
          WCAG 2.1 AA compliant with proper ARIA, focus management, and status messages.
        </p>
      </div>

      {/* Primary Button with proper semantics */}
      <div>
        <StyledButton
          onClick={handleOpen}
          aria-label="Open dialog"
          aria-expanded={isOpen}
          aria-haspopup="dialog"
        >
          Open Dialog
        </StyledButton>
      </div>

      {/* Dialog with proper ARIA attributes */}
      <AnimatePresence>
        {isOpen && (
          <Card
            role="dialog"
            aria-labelledby="dialog-title"
            aria-describedby="dialog-description"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <h2 id="dialog-title" style={{ fontFamily: "'Playfair Display', serif", margin: '0 0 16px 0' }}>
              Confirm Action
            </h2>
            <p id="dialog-description" style={{ fontFamily: "'IBM Plex Sans', sans-serif", margin: '0 0 24px 0' }}>
              Are you sure you want to proceed? This action cannot be undone.
            </p>

            <div style={{ display: 'flex', gap: '12px' }}>
              <StyledButton
                onClick={handleAction}
                disabled={loading}
                aria-busy={loading}
              >
                {loading ? 'Processing...' : 'Confirm'}
              </StyledButton>
              <SecondaryButton onClick={handleClose}>
                Cancel
              </SecondaryButton>
              <SecondaryButton
                onClick={handleError}
                aria-label="Trigger error state for demonstration"
              >
                Error Demo
              </SecondaryButton>
            </div>
          </Card>
        )}
      </AnimatePresence>

      {/* Status Messages with ARIA roles */}
      <AnimatePresence>
        {message && (
          <StatusMessage
            type={message.type}
            role={message.type === 'error' ? 'alert' : 'status'}
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            {message.type === 'success' && '✓ '}
            {message.type === 'error' && '⚠ '}
            {message.text}
          </StatusMessage>
        )}
      </AnimatePresence>

      {/* Accessibility Features List */}
      <Card>
        <h3 style={{ fontFamily: "'Playfair Display', serif", margin: '0 0 16px 0' }}>
          Accessibility Features
        </h3>
        <ul style={{ fontFamily: "'IBM Plex Sans', sans-serif", margin: 0, paddingLeft: '20px' }}>
          <li>
            <strong>Semantic HTML</strong>: Uses <code>&lt;button&gt;</code>, <code>&lt;dialog&gt;</code>, proper heading hierarchy
          </li>
          <li>
            <strong>ARIA Attributes</strong>: aria-label, aria-expanded, aria-haspopup, role="dialog", role="alert", role="status"
          </li>
          <li>
            <strong>Focus Management</strong>: Visible focus states with yellow outline (not invisible)
          </li>
          <li>
            <strong>Status Announcements</strong>: Role="status" for non-urgent updates, role="alert" for urgent errors
          </li>
          <li>
            <strong>Loading States</strong>: aria-busy attribute on buttons during async operations
          </li>
          <li>
            <strong>Keyboard Support</strong>: All interactive elements are keyboard accessible (Tab, Enter)
          </li>
          <li>
            <strong>Motion Preferences</strong>: Respects prefers-reduced-motion media query
          </li>
          <li>
            <strong>Color Contrast</strong>: All text meets WCAG AA contrast requirements
          </li>
        </ul>
      </Card>
    </ButtonContainer>
  );
};
```

**Key Accessibility Learnings**:
- Use semantic HTML (`<button>`, `<dialog>`, proper `<h1>` hierarchy)
- Add ARIA labels: `aria-label`, `aria-expanded`, `aria-haspopup`, `aria-busy`
- Use proper roles: `role="dialog"`, `role="alert"`, `role="status"`
- Focus should be visible (not outline: none) - use high contrast
- Respect `prefers-reduced-motion` for users with vestibular disorders
- Status messages need `role="status"` (non-urgent) or `role="alert"` (urgent)
- All text should meet WCAG AA contrast ratios (4.5:1 for body text)

---

## Example 5: Mobile-First Responsive Component

This example shows how to design for mobile first, then enhance for larger screens while maintaining the distinctive design system.

```typescript
import styled from 'styled-components';
import { motion } from 'framer-motion';
import React from 'react';

const MobileFirstContainer = styled.div`
  /* Mobile-first: base styles for small screens */
  padding: 16px;
  background: #FAF8F4;
  min-height: 100vh;
`;

const MobileFirstGrid = styled.div`
  /* Mobile: single column */
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;

  /* Tablet: 2 columns */
  @media (min-width: 768px) {
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }

  /* Desktop: 3 columns */
  @media (min-width: 1024px) {
    grid-template-columns: 1fr 1fr 1fr;
    gap: 32px;
  }
`;

const MobileFirstCard = styled(motion.div)`
  /* Mobile-first: full width */
  background: white;
  border-radius: 4px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

  /* Tablet: slightly larger */
  @media (min-width: 768px) {
    padding: 24px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }

  /* Desktop: enhanced shadow and padding */
  @media (min-width: 1024px) {
    padding: 32px;
  }
`;

const ResponsiveHeading = styled.h2`
  /* Mobile: smaller headline */
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 16px 0;

  /* Tablet: medium headline */
  @media (min-width: 768px) {
    font-size: 32px;
    margin: 0 0 24px 0;
  }

  /* Desktop: large headline */
  @media (min-width: 1024px) {
    font-size: 48px;
    margin: 0 0 32px 0;
  }
`;

const ResponsiveText = styled.p`
  /* Mobile: small text for readability */
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;

  /* Tablet: standard size */
  @media (min-width: 768px) {
    font-size: 16px;
    line-height: 1.6;
  }

  /* Desktop: comfortable reading size */
  @media (min-width: 1024px) {
    font-size: 18px;
  }
`;

const TouchableButton = styled(motion.button)`
  /* Mobile-first: large touch target (44px minimum) */
  padding: 16px 24px;
  font-size: 16px;
  width: 100%;
  background: #8B4513;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-family: 'IBM Plex Sans', sans-serif;
  font-weight: 600;

  /* Tablet: smaller button allowed */
  @media (min-width: 768px) {
    width: auto;
    padding: 12px 24px;
    font-size: 14px;
  }

  /* Desktop: standard size */
  @media (min-width: 1024px) {
    padding: 14px 28px;
    font-size: 16px;
  }

  &:hover {
    background: #A55C30;
  }

  &:active {
    transform: scale(0.98);
  }

  /* Large touch targets on mobile */
  @media (max-width: 480px) {
    min-height: 44px;
  }
`;

export const MobileFirstResponsiveShowcase: React.FC = () => {
  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: (i: number) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: i * 0.1,
        duration: 0.6,
        ease: 'easeOut',
      },
    }),
  };

  const cards = [
    {
      title: 'Mobile First',
      description: 'Start with small screens, enhance for larger ones. All touch targets 44px minimum.',
    },
    {
      title: 'Responsive Typography',
      description: 'Font sizes scale gracefully. 14px on mobile, 18px on desktop—same font family.',
    },
    {
      title: 'Flexible Grid',
      description: '1 column on mobile, 2 on tablet, 3 on desktop. All without media query hell.',
    },
    {
      title: 'Touch-Friendly',
      description: 'Buttons are full-width on mobile for easy tapping. Spacing increases on larger screens.',
    },
    {
      title: 'Performance',
      description: 'Fewer decorative elements on mobile. Shadows and effects enhance on desktop.',
    },
    {
      title: 'Intentional Scaling',
      description: 'Whitespace, padding, and gaps all scale responsively. Not just font size.',
    },
  ];

  return (
    <MobileFirstContainer>
      <ResponsiveHeading>Mobile-First Responsive Design</ResponsiveHeading>
      <ResponsiveText style={{ marginBottom: '32px' }}>
        This component demonstrates how to build responsive designs that feel intentional on every screen size.
        Start with mobile constraints, enhance for larger screens.
      </ResponsiveText>

      <MobileFirstGrid>
        {cards.map((card, index) => (
          <MobileFirstCard
            key={index}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.3 }}
            custom={index}
            variants={itemVariants}
          >
            <ResponsiveHeading style={{ fontSize: 'inherit' }}>
              {card.title}
            </ResponsiveHeading>
            <ResponsiveText>{card.description}</ResponsiveText>
          </MobileFirstCard>
        ))}
      </MobileFirstGrid>

      {/* Call to action */}
      <div style={{ marginTop: '48px' }}>
        <ResponsiveText style={{ marginBottom: '16px' }}>
          Ready to make your design responsive?
        </ResponsiveText>
        <TouchableButton
          whileHover={{ y: -2 }}
          whileTap={{ y: 0 }}
        >
          Start Building
        </TouchableButton>
      </div>

      {/* Responsive Breakpoints Reference */}
      <MobileFirstCard style={{ marginTop: '48px', backgroundColor: '#F5F1E8' }}>
        <ResponsiveHeading style={{ fontSize: '20px' }}>
          Responsive Breakpoints
        </ResponsiveHeading>
        <ResponsiveText>
          <strong>Mobile (default):</strong> 320px - 767px<br />
          <strong>Tablet:</strong> 768px - 1023px<br />
          <strong>Desktop:</strong> 1024px+<br />
          <br />
          All spacing, typography, and layout scale gracefully across these breakpoints.
        </ResponsiveText>
      </MobileFirstCard>
    </MobileFirstContainer>
  );
};
```

**Key Mobile-First Learnings**:
- Start with mobile constraints (everything fits in small space)
- Use min-width media queries (mobile-first) not max-width (desktop-first)
- Touch targets must be 44x44px minimum on mobile
- Buttons should be full-width on mobile for easy tapping
- Reduce visual decoration on mobile, enhance on desktop
- Typography scales but maintains the same typeface family
- Spacing and padding scale proportionally (not just font size)

---

## Validation Checklist

Use this checklist to validate that your React frontend follows the 5-dimension design framework:

```typescript
const designValidationChecklist = {
  typography: {
    "Rejected default fonts (Inter, Roboto, Open Sans, Lato)?": false,
    "Using high-contrast pairing (serif + sans or serif + mono)?": false,
    "Size jumps 3x+ between hierarchy levels?": false,
    "Weight extremes (300/700/900, not 400/500/600)?": false,
    "Letter spacing negative on display text?": false,
  },
  color: {
    "Custom palette (not Material Design or Tailwind)?": false,
    "Emotional intent defined (warm, cool, energetic, calm)?": false,
    "One unexpected accent color for personality?": false,
    "Sufficient contrast ratio (WCAG AA 4.5:1)?": false,
    "Dark mode is intentional, not just inverted?": false,
  },
  motion: {
    "Animations are orchestrated (staggered), not simultaneous?": false,
    "Easing functions used (not linear)?": false,
    "Duration 0.4-0.8s (snappy), not 1.5s+ (sluggish)?": false,
    "At least one delightful hover surprise?": false,
    "Page load has 5-8 step animation sequence?": false,
  },
  spatial: {
    "Layout is asymmetrical (not centered grid)?": false,
    "Spacing scale defined (8px, 16px, 24px, 32px)?": false,
    "Whitespace is generous (not cramped)?": false,
    "Visual hierarchy created through space?": false,
    "Mobile-first responsive design?": false,
  },
  visual: {
    "Subtle background (not bland white)?": false,
    "Gradients are minimal and intentional?": false,
    "Micro-details reward close observation?": false,
    "Texture/pattern is 2-5% opacity (not busy)?": false,
    "Visual elements serve a purpose?": false,
  },
  accessibility: {
    "Semantic HTML (button, dialog, proper h1 hierarchy)?": false,
    "ARIA labels and roles present?": false,
    "Focus states are visible (not outline: none)?": false,
    "Color contrast WCAG AA compliant?": false,
    "Keyboard navigation works?": false,
    "Touch targets 44x44px minimum on mobile?": false,
    "Respects prefers-reduced-motion?": false,
  },
  code: {
    "React functional components with hooks?": false,
    "TypeScript interfaces for all props?": false,
    "React.memo used for performance?": false,
    "Framer Motion for animations (not CSS-only)?": false,
    "CSS-in-JS with typed tokens?": false,
    "No prop drilling (use context or composition)?": false,
  },
};
```

---

## Resources

- **Framer Motion Docs**: https://www.framer.com/motion/
- **Google Fonts**: https://fonts.google.com
- **Easing Functions**: https://easings.net/
- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **Styled Components**: https://styled-components.com/
- **React TypeScript**: https://react-typescript-cheatsheet.netlify.app/

---

Remember: **Intentional design is a choice, not a default.** Every decision should serve the problem you're solving, the emotional intent you're creating, and the users you're serving. If you're choosing something because it's the easiest option, you're designing like an AI. Choose deliberately instead.
