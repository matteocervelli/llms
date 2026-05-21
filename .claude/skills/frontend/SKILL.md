---
name: frontend
description: Design UI, build components, write Playwright E2E tests, run WCAG accessibility audits, and do visual review. Use when building or testing frontend/UI work. Trigger on "build a component", "frontend", "E2E test", "accessibility audit", "a11y", "visual review", "make this look good".
tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Frontend — Design, Build & Verify

Unified frontend skill for visual design, component creation, E2E testing, accessibility audits, and visual review. Composes five design dimensions with tech-specific implementations.

## Usage

```
/frontend                        # Show dimensions, suggest next action
/frontend design                 # 6 design dimensions + 9-phase workflow
/frontend component <name>       # Create UI component with variants, tests, preview
/frontend e2e                    # Write Playwright E2E tests (page object model)
/frontend a11y                   # WCAG 2.1 AA accessibility audit
/frontend review                 # Gemini visual review (screenshot + code)
/frontend verify                 # Quick verification decision tree
```

## Workflow

### Step 1: Determine Mode

Parse `$ARGUMENTS` for explicit subcommand. If no arguments:

1. Check for recent frontend file changes (`*.html`, `*.css`, `*.ts`, `*.tsx`, `*.jinja2`, `*.scss`)
2. If changes found → suggest `/frontend verify`
3. If new project → suggest `/frontend design`
4. Otherwise → show all modes

### Step 1.5: Load Design System

Before routing to any subcommand, check for a persistent design system file:

1. Look for `.design/system.md` in the project root (search from CWD upward, stop at git root)
2. If found: read it and announce → `Design system loaded: [list the Mode + Typography + Color + Depth values]`
3. Treat the loaded values as hard constraints throughout the session — do not contradict them without explicitly noting you're changing a decision and logging it

On `/frontend design` Phase 1 completion:

- Create `.design/system.md` if it does not exist (use the Design Brief output as seed)
- If it exists: update only the fields changed in this session; preserve existing Decisions Log entries
- Note: `.design/system.md` should be committed to version control (it is a project artifact)

After each design phase (typography, color, spatial, etc.):

- Update the corresponding section in `.design/system.md` with the decisions made

### Step 1b: Detect Design Mode

Determine whether this is a **brand** or **product** context. Detection priority:

1. `.design/system.md` `## Mode` field — use it if present
2. Explicit user statement ("build a landing page", "build a dashboard")
3. Project signals — scan for: `/app/`, `/dashboard/`, `/admin/` routes; auth middleware; data table components → **product**. Hero sections, CTA buttons, marketing copy, no auth → **brand**
4. If ambiguous: ask — "Is this a brand/marketing page or a product/app UI?"

**Brand mode** — marketing pages, landing pages, portfolios, editorial. Prioritize: personality, differentiation, emotional impact, dramatic hierarchy.

**Product mode** — dashboards, app UI, admin panels, tools. Prioritize: clarity, information density, consistency, functional hierarchy.

Record the detected mode in `.design/system.md` `## Mode` field.

### Step 2: Route to Subcommand

---

## `/frontend design` — Visual Design

The 6 Design Dimensions:

1. **Typography** — Typeface selection, font pairings, weights, sizing, hierarchy
2. **Color & Theme** — Emotional intent, color systems, unexpected accents
3. **Motion** — Orchestrated animations, easing, interaction choreography
4. **Spatial Composition** — Layout, spacing systems, asymmetrical design
5. **Backgrounds & Details** — Subtle textures, gradients, visual rewards
6. **UI Polish** — Micro-details: text wrapping, concentric radii, shadow borders, optical alignment

**Tech implementations** (choose one, loaded from `sub-skills/`):

| Sub-skill            | Stack                         |
| -------------------- | ----------------------------- |
| `react-vite.md`      | React + Vite + Framer Motion  |
| `htmx.md`            | HTMX + Jinja2 + hyperscript   |
| `jinja2.md`          | Jinja2 template patterns      |
| `sass.md`            | Sass/SCSS design tokens       |
| `vue.md`             | Vue (Options/Composition API) |
| `svelte.md`          | Svelte custom animations      |
| `html.md`            | HTML/CSS/SCSS fundamentals    |
| `tailwind.md`        | Tailwind CSS                  |
| `shadcn-ui.md`       | shadcn/ui design system       |
| `radix-ui.md`        | Radix UI primitives           |
| `material-design.md` | Material Design               |
| `hugo.md`            | Hugo static site              |
| `typescript.md`      | TypeScript patterns           |
| `css-scss.md`        | Advanced CSS/SCSS             |

**11-Phase Workflow**:

1. Design thinking + working model (`sub-skills/design-thinking.md`)
2. Typography dimension (`sub-skills/typography.md`)
3. Color & theme dimension (`sub-skills/color-theme.md`)
4. Motion dimension (`sub-skills/motion.md`)
5. Spatial composition (`sub-skills/spatial.md`)
6. Page composition — hero, narrative, cards (`sub-skills/page-composition.md`)
7. Imagery & visual anchors (`sub-skills/imagery.md`)
8. Backgrounds & details (`sub-skills/backgrounds.md`)
9. UI polish pass (`sub-skills/ui-polish.md`)
   9.5. Delight pass — run `/impeccable delight` to add one unexpected element. If Impeccable is not installed, apply patterns from `sub-skills/ui-polish.md` Interaction Polish section instead.
10. Implementation with chosen tech sub-skill
11. Litmus checks (`prompts/litmus-checks.md`) → run `bash scripts/design-lint.sh . --mode [brand|product]` → fix `warn` findings → Visual validation → `/frontend review` (optional)

Additional resources in `design-references/`, `design-systems/`, `prompts/`, `tools/`.

---

## `/frontend component <name>` — UI Components

Create production-ready UI components with TypeScript, variants, tests, and preview.

```
/frontend component Button "Primary action button with variants"
/frontend component Modal "Dialog component for user interactions"
```

**Creates**:

- `src/components/ui/[name]/[name].tsx` — Component with variants (primary/secondary/success/danger/warning), sizes (sm/md/lg), states (disabled/hover/focus/active)
- `src/components/ui/[name]/[name].test.tsx` — Tests for all variants, states, keyboard nav
- Preview integration in `src/app/preview/page.tsx`

**Requirements**:

- Semantic HTML (no div/span for interactive elements)
- ARIA attributes (`aria-label`, `aria-disabled`, `aria-describedby`)
- Keyboard navigation (Tab, Enter/Space, Escape, Arrow keys)
- Focus indicators (`outline: 2px solid`, `:focus-visible`)
- WCAG 2.1 AA color contrast (4.5:1 minimum)

Reference: `templates/component-scaffold.md`

---

## `/frontend e2e` — Playwright E2E Tests

Write comprehensive E2E tests using Playwright with page object model pattern.

**Templates** (in `templates/e2e/`):

| Template               | Purpose                           |
| ---------------------- | --------------------------------- |
| `playwright-config.ts` | Multi-browser configuration       |
| `page-object-model.ts` | BasePage class + page objects     |
| `custom-fixtures.ts`   | Test data + authenticated state   |
| `responsive-tests.ts`  | Desktop/tablet/mobile viewports   |
| `visual-regression.ts` | Screenshot comparison + snapshots |
| `api-mocking.ts`       | Mock API responses with MSW       |
| `auth-setup.ts`        | Authentication state reuse        |

**Structure**: `tests/e2e/{auth,features,workflows}/`, `tests/pages/`

---

## `/frontend a11y` — Accessibility Audit

Validate WCAG 2.1 Level AA compliance combining automated + manual testing.

**WCAG 2.1 Principles**:

- **Perceivable**: Alt text, contrast, adaptable content
- **Operable**: Keyboard nav, navigation, input modalities
- **Understandable**: Readable, predictable, input assistance
- **Robust**: Valid HTML, ARIA, compatibility

**Workflow**:

1. Automated scan (axe-core catches ~30%)
2. Manual keyboard testing (Tab through all interactive elements)
3. Screen reader testing (VoiceOver/NVDA)
4. Zoom to 200% (text resizable)
5. Generate report using `templates/a11y/accessibility-report.md`

Reference: `templates/a11y/wcag-checklist.md`

---

## `/frontend review` — Visual Design Review

Capture screenshot + source code → send to Gemini for visual design analysis against 5 dimensions.

**Requires**: Gemini API (vision-capable model). Does not work with Claude.

```
/frontend review                           # Auto-detect localhost
/frontend review http://localhost:3000     # Specific URL
/frontend review /path/to/screenshot.png   # Existing screenshot
/frontend review --full-page               # Full scrollable page
/frontend review --color-scheme dark       # Dark mode
```

Uses shared screenshot utility at `~/.claude/shared/companions/lib/screenshot.sh`.

---

## `/frontend verify` — Quick Verification

Decision tree for verifying frontend changes after implementation using `playwright-cli`:

1. **Is the dev server running?**
   - Yes → Use `playwright-cli` for visual check + interaction
   - No → Start dev server first

2. **What needs verification?**
   - Visual appearance → `playwright-cli screenshot`
   - Page structure → `playwright-cli snapshot` (YAML with element refs)
   - User flow → `playwright-cli open` → `fill`/`click`/`type` with refs
   - Console errors → `playwright-cli console`
   - Network issues → `playwright-cli network`
   - Responsive → `playwright-cli resize` at multiple viewports

3. **Tool selection**:
   - Quick screenshot → `playwright-cli screenshot`
   - Interactive exploration → `playwright-cli` commands (open, snapshot, click, fill)
   - E2E test suite → `npx playwright test` or `uv run pytest tests/e2e/`

## Canvas Mode (Claude Code + Pencil MCP)

When the `pencil` MCP server is connected (`claude mcp list` shows `pencil: ✓ Connected`), design phases 6–9 can run directly on a live canvas instead of writing code:

- `read_canvas` — inspect current canvas state (frames, layers, tokens)
- `get_selected_frame` — work on the frame selected in Pencil
- `get_style_guide` — extract or apply design tokens from the canvas

Canvas mode replaces the code-first approach for visual iteration: design on canvas → extract tokens → implement. Use it for early-phase exploration before committing to code. Falls back to normal file-based workflow when Pencil is not connected.

---

## Integration

**Invoked by**: User directly (`/frontend`)
**Connected skills**:

- `/frontend design` → implement → `/frontend verify` → `/frontend review` (validate)
- `/frontend component` → `/frontend e2e` (test the component)
- `/frontend a11y` → standalone audit, often after `/frontend verify`

**External tools** (Claude Code only):

- `/impeccable` — 23-command design skill at `~/.local/share/skills/impeccable`. Use `/impeccable delight` in Phase 9.5, `/impeccable audit` for a full anti-pattern scan, `/impeccable detect` for CI-gatable output.
- `pencil` MCP — Canvas-based design iteration. Check with `claude mcp list`.

**Agents**:

- `browser-tester` — Interactive testing with playwright-cli (auto-scales from quick verification to full-app discovery + fix)
