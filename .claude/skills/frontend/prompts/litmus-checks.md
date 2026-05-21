# Page Litmus Checks

Quick yes/no validation for the page as a whole. Run these after completing all dimensions
and before handing off for review. If any answer is No, fix before proceeding.

## Design System Continuity

- [ ] Is `.design/system.md` present in the project root?
      → If No: run Phase 1 (design thinking) first and generate it.
- [ ] Do the current page decisions match the loaded design system?
      → If changed: log the change in Decisions Log with rationale.

## Composition Checks

- [ ] Is the brand or product name unmistakable in the first viewport?
- [ ] Is there exactly one strong visual anchor in the hero?
- [ ] Does the hero contain only: brand, headline, supporting sentence, CTA, image?
- [ ] Could each section be described in 5 words ("show product in use", "prove credibility")?
- [ ] Does each section have only one job?

## Brand Hierarchy

- [ ] Remove the nav mentally. Is the brand still the loudest signal?
      → If No: strengthen brand signal in the first viewport.
- [ ] Does the headline overpower the brand name?
      → If Yes: reduce headline scale or increase brand weight.

## Cards

- [ ] Are there cards anywhere? (border + shadow + background-color)
- [ ] For each card: does removing border/shadow/bg hurt interaction or understanding?
      → If No to either: convert to plain layout — column, section, or list.
- [ ] Are there cards in the hero?
      → If Yes: remove them unconditionally.

## Copy

- [ ] Can the page be understood by scanning headlines only?
- [ ] If 30% of body copy were deleted, would the page improve?
      → If Yes: delete that 30%.
- [ ] For dashboards/app UI: are any headings in marketing/brand voice?
      → If Yes: rewrite as orientation/status/action language.

## Visual Anchor

- [ ] Does the hero image do narrative work (product, place, atmosphere)?
      → If it could be replaced by a gradient: find a stronger image.
- [ ] If the image is removed, is the page meaningfully worse?
      → If barely worse: the image is not pulling its weight.

## Motion

- [ ] Does the motion improve hierarchy or atmosphere?
- [ ] Are there 2-3 intentional motion beats (entrance, scroll, hover)?
- [ ] Would the page feel cold or broken without the motion?
      → If No: the motion may be ornamental. Consider removing.

## Structural Soundness

- [ ] Would the design still feel premium with all decorative shadows removed?
- [ ] Is there a single clear CTA in the final section?
- [ ] On mobile: does every section still read correctly?

## Mode-Specific Checks

Run only the section matching the detected design mode.

### Brand Mode

- [ ] Does the page have a clear narrative arc (hero → support → proof → CTA)?
- [ ] Are type scale jumps dramatic enough (3x+ between display and body)?
- [ ] Would removing the motion make the page feel cold or static?
- [ ] Is there one element so unexpected it could appear in a portfolio?

### Product Mode

- [ ] Are all headings in functional language — no marketing or brand voice?
- [ ] Is information density appropriate — not too sparse for the use case?
- [ ] Are interactive patterns consistent across all views (same hover, same depth, same spacing)?
- [ ] Can a user reach any feature in ≤2 clicks from the primary nav?
