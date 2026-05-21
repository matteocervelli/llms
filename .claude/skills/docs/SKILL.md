---
name: docs
description: Build and publish project documentation — Starlight (Astro) for apps, markdown for libraries/services, with IT+EN i18n and VPS deploy. Use when writing user guides, scaffolding a docs site, or publishing docs. Trigger on "write docs", "documentation site", "user guide", "publish docs".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# /docs — Documentation Pipeline

Unified pipeline for documentation across all project types. **Dual mode:**

- **App mode** (app-ratio, app-himalaia, app-levero) → Starlight (Astro) in `site/`, deploy su VPS

**Mode detection:** automatic from repo name and structure:

- `app-*` or `site/` exists → **app mode** (Starlight)
- `private-lib-*` → **internal mode** (library markdown)
- Override: `/docs scaffold --mode app` or `/docs scaffold --mode internal`

**Future:** Atrium gets a unified Starlight site aggregating all internal docs from libs/services.

## Architecture — App Mode (locked)

- SSG: Starlight (Astro) — MIT, i18n IT+EN native, Pagefind search built-in
- Structure: `site/` folder inside each app repo (marketing + docs unified Astro project)
- URL: `{app-domain}/docs` (subfolder, not subdomain) — SEO unificato
- Auth: `nginx auth_request → FastAPI /auth/verify` finché l'app non è pubblica
- Deploy: `make deploy-site` oggi; Forgejo Actions staging/stable in futuro
- Language: Italiano first, i18n EN configurato da day-0

## Architecture — Internal Mode

- Output: plain markdown in `docs/user-guide/` (non deployato, letto da sviluppatori e integratori)
- Stessi template concettuali di Starlight ma senza MDX/components
- Registry: `docs/docs-registry.yaml` (stesso formato, stessa skill)
- Nessun `site/`, nessun npm, nessun Astro

## Quick Start

```
/docs                          # stato docs + mode auto-detect
/docs scaffold                 # app mode: site/ | internal mode: docs/user-guide/
/docs create getting-started   # crea pagina da template (adattato al mode)
/docs audit                    # trova stale, mancanti, link rotti
/docs update                   # aggiorna pagine stale da git diff + CHANGELOG
/docs translate it             # EN→IT (solo app mode)
/docs publish                  # deploy su VPS (solo app mode)
/docs publish staging          # deploy ambiente staging (solo app mode)
/docs review-drafts            # lancia N agent paralleli per completare e verificare le draft
/docs registry                 # mostra stato registry docs del progetto
/docs features                 # estrae feature list da CHANGELOG + routes/API
/docs migrate                  # audit strutturale repo + propone migrazione a convenzione
/docs full                     # scaffold → audit → create missing → review-drafts → (translate → publish se app mode)
```

---

## Subcommand: `/docs` (summary)

Auto-detect progetto corrente e mostra stato docs.

**Steps:**

1. Auto-detect mode (app vs internal)
2. App mode: verifica `site/` + `site/docs-registry.yaml` + staleness + language parity
   Internal mode: verifica `docs/user-guide/` + `docs/docs-registry.yaml` + staleness
3. Output report con status per dimensione
4. **Proponi il prossimo passo concreto e chiedi se eseguirlo**

**Step 4 — Next action routing (obbligatorio):**

Dopo il report, identifica l'azione con priorità più alta e proponi di eseguirla:

| Condizione (in ordine di priorità)               | Prossima azione                                                                      |
| ------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Né `site/` né `docs/user-guide/` esistono        | "Eseguo `/docs scaffold`?"                                                           |
| scaffold esiste ma 0 pagine                      | "Eseguo `/docs create getting-started`?"                                             |
| pagine in status draft (anche senza placeholder) | "Eseguo `/docs review-drafts`?" (N agent paralleli VERIFICANO accuratezza vs codice) |
| draft completate, modifiche non committate       | "Eseguo `/pre-commit` → `/ship`?" (valida + commit + push + PR)                      |
| pagine stale >30 giorni                          | "Eseguo `/docs update <file più stale>`?"                                            |
| pagine EN mancanti (solo app mode)               | "Eseguo `/docs translate en`?"                                                       |
| tutto OK ma non deployato (solo app mode)        | "Eseguo `/docs publish`?"                                                            |
| tutto published, non video (app mode)            | "Video guide da esplorare — `/docs video` (sessione dedicata)"                       |
| tutto published, tutto deployato                 | "Docs in ordine. Nessuna azione necessaria."                                         |

Chiedi sempre conferma con `AskUserQuestion` prima di eseguire. Se l'utente dice sì,
esegui l'azione e poi ricicla al punto 4 (proponi il passo successivo).
Questo crea un loop guidato: report → proposta → esecuzione → report → proposta → ...
fino a quando tutto è PASS o l'utente dice stop.

**Step 4b — Parallel draft review (quando ci sono multiple draft):**

Quando ci sono ≥2 pagine draft, proponi di lanciare agent paralleli:

```
"Hai N pagine draft. Lancio N agent Explore in parallelo per completarle?"
```

Se l'utente conferma:

1. Per ogni pagina draft, lancia un Agent (subagent_type: `general-purpose`, model: `sonnet`):
   - **Input**: il file draft + CHANGELOG.md + codice sorgente rilevante (backend/, app/, src/)
   - **Istruzioni**: "Leggi il template, sostituisci tutti i placeholder con contenuto reale basato sul codice e CHANGELOG. Mantieni la struttura del template. Non inventare funzionalità — documenta solo ciò che esiste."
   - **Output**: il file completato

2. Dopo che tutti gli agent finiscono:
   - Mostra diff per ogni file modificato
   - Chiedi conferma: "Marco tutte come published?"
   - Se sì: `/docs registry update <page> status=published` per ognuna

Questo parallelizza il lavoro più pesante (compilare N draft) senza richiedere intervento umano per ogni singola pagina.

**Output example:**

```

Mode         internal   private-lib-* library → markdown
user-guide/  [MISS]     docs/user-guide/ assente
Registry     [MISS]     docs/docs-registry.yaml assente
Staleness    [WARN]     code 19 giorni più recente dei docs

───────────────────────────────────
Prossimo passo: /docs scaffold (crea docs/user-guide/ + registry)
Eseguo?
```

---

## Subcommand: `/docs scaffold`

Inizializza la struttura docs nel repo corrente. Dual mode.

**Pre-condizioni:**

- Siamo nella root del repo (`pyproject.toml` o `package.json` presente)
- Mode auto-detect: `app-*` → app mode, `private-lib-*` o services → internal mode
- Override: `--mode app` o `--mode internal`

### App Mode (Starlight)

Condizione: repo name `app-*` oppure `--mode app`

> **Stack locked (2026-03-17):** Starlight 0.32 + Astro 5 + pnpm workspace.
> Il locale default IT va alla root di `docs/` (NON in `it/` subdir) — vedi sotto.

**Steps:**

1. Crea struttura directory:

```
site/
├── src/
│   ├── content/
│   │   └── docs/
│   │       ├── index.md         ← homepage IT (root locale = IT)
│   │       ├── getting-started.md
│   │       ├── features/        ← feature guides IT
│   │       └── en/              ← SOLO EN in subdir
│   │           ├── getting-started.md
│   │           └── features/
│   └── content.config.ts        ← OBBLIGATORIO in Astro 5
├── public/
└── docs-registry.yaml
```

**CRITICO — Struttura i18n corretta per Starlight 0.32 + Astro 5:**

- Locale default (IT) = `root`: i file IT vivono direttamente in `docs/` (NO `it/` subdirectory)
- Locale EN = `en/`: i file EN vivono in `docs/en/`
- Se metti IT in `docs/it/` il build genera solo 1 pagina — il sito non funziona

2. Genera `site/package.json`:

```json
{
  "name": "app-{name}-site",
  "type": "module",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "dev": "astro dev --port 4321",
    "build": "astro build",
    "preview": "astro preview",
    "astro": "astro"
  },
  "dependencies": {
    "@astrojs/starlight": "^0.32.0",
    "astro": "^5.4.0"
  },
  "devDependencies": {
    "sharp": "^0.33.0"
  }
}
```

3. Genera `site/src/content.config.ts` — **OBBLIGATORIO in Astro 5, senza questo le pagine non vengono trovate:**

```typescript
import { defineCollection } from "astro:content";
import { docsLoader } from "@astrojs/starlight/loaders";
import { docsSchema } from "@astrojs/starlight/schema";

export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
};
```

4. Genera `site/astro.config.mjs`:

```javascript
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

export default defineConfig({
  base: "/docs",
  integrations: [
    starlight({
      title: "{APP_NAME} — Guida Utente",
      description: "Documentazione ufficiale di {APP_NAME}",
      defaultLocale: "root", // 'root' = IT a root level, NON 'it'
      locales: {
        root: { label: "Italiano", lang: "it" },
        en: { label: "English", lang: "en" },
      },
      sidebar: [
        {
          label: "Inizia qui",
          translations: { en: "Start here" },
          items: [{ slug: "getting-started" }],
        },
        {
          label: "Funzionalità",
          translations: { en: "Features" },
          autogenerate: { directory: "features" },
        },
      ],
    }),
  ],
});
```

**Nota sidebar slugs:** con `docsLoader()` i slug NON hanno prefisso locale. `{ slug: 'getting-started' }` punta a `docs/getting-started.md` (IT root) E a `docs/en/getting-started.md` (EN) — Starlight gestisce l'i18n internamente.

5. Genera `site/src/content/docs/index.md` — homepage IT (template splash)

6. Genera `site/docs-registry.yaml` vuoto

7. Aggiorna `pnpm-workspace.yaml` nella root (se il progetto usa pnpm):

```yaml
packages:
  - "frontend"
  - "site" # ← aggiungere
```

8. Aggiorna `package.json` root per permettere build scripts di esbuild/sharp (richiesti da Astro):

```json
{
  "pnpm": {
    "onlyBuiltDependencies": ["esbuild", "sharp"]
  }
}
```

Poi esegui `pnpm install` per aggiornare il lockfile.

9. Aggiungi a `.gitignore` root:

```
site/dist/
site/.astro/
```

10. Aggiungi target Makefile (usa `pnpm`, NON `npm ci`):

```makefile
site-dev: ## Start docs site development server (localhost:4321/docs)
	cd site && $(PNPM) run dev

site-build: ## Build docs site for production
	cd site && $(PNPM) install --frozen-lockfile && $(PNPM) run build

deploy-site: site-build ## Build and deploy docs site to VPS
	rsync -avz --delete site/dist/ {vps-host}:/opt/{app}/site/dist/
```

11. Aggiungi snippet nginx a `docs/deployment/nginx-site.conf` (o crea il file):
    Usa template `templates/nginx-site.conf` con auth_request configurato

12. Aggiungi endpoint FastAPI `GET /auth/verify` (controlla se già esiste):
    Cerca in `backend/` per `auth/verify` → se assente, propone aggiunta

13. Output:

```
✓ site/ creata con Starlight 0.32 + Astro 5 (IT root + EN)
✓ src/content.config.ts creato (docsLoader)
✓ pnpm-workspace.yaml aggiornato
✓ docs-registry.yaml inizializzato
✓ Makefile aggiornato con target site-dev, site-build, deploy-site
✓ Snippet nginx generato in docs/deployment/nginx-site.conf
⚠ Aggiungi manualmente endpoint /auth/verify a backend/app/api/auth.py

Prossimi passi:
  pnpm install && make site-dev   # preview locale su localhost:4321/docs
  /docs create getting-started    # crea prima pagina
```

### Internal Mode (Markdown)

Condizione: repo name `private-lib-*` oppure service noto oppure `--mode internal`

**Steps:**

1. Crea struttura directory:

```
docs/
├── user-guide/
│   ├── getting-started.md
│   └── README.md         ← indice delle guide
└── docs-registry.yaml
```

`docs/user-guide/` è separata dai dev docs esistenti (`docs/architecture/`, `docs/deployment/`, ecc.).

2. Genera `docs/user-guide/README.md` — indice delle guide con link

3. Genera `docs/docs-registry.yaml` (stesso formato dell'app mode, senza campi deploy)

4. Output:

```
✓ docs/user-guide/ creata
✓ docs/docs-registry.yaml inizializzato
  Mode: internal (no Starlight, no deploy)

Prossimi passi:
  /docs create getting-started   # crea prima guida utente
  /docs features                  # estrae feature list da CHANGELOG + API
```

---

## Subcommand: `/docs create <type>`

Crea una nuova pagina docs da template. **Adattato al mode corrente:**

- App mode → MDX con Starlight components (Steps, Cards, Aside)
- Internal mode → plain markdown (stessi contenuti, senza MDX)

**Tipi disponibili:**
| Tipo | Template app | Template interno | Cartella target (app) | Cartella target (interno) |
|---|---|---|---|---|
| `getting-started` | `templates/getting-started.md` | `templates/internal/getting-started.md` | `site/src/content/docs/{lang}/` | `docs/user-guide/` |
| `feature-guide` | `templates/feature-guide.md` | `templates/internal/feature-guide.md` | `site/src/content/docs/{lang}/features/` | `docs/user-guide/features/` |
| `how-to` | `templates/how-to.md` | `templates/internal/how-to.md` | `site/src/content/docs/{lang}/guides/` | `docs/user-guide/guides/` |
| `faq` | `templates/faq.md` | `templates/internal/faq.md` | `site/src/content/docs/{lang}/` | `docs/user-guide/` |
| `release-notes` | `templates/release-notes.md` | `templates/internal/release-notes.md` | `site/src/content/docs/{lang}/` | `docs/user-guide/` |
| `api-reference` | — | `templates/internal/api-reference.md` | — | `docs/user-guide/` |
| `feature-guide` | `templates/feature-guide.md` | `site/src/content/docs/{lang}/features/` |
| `how-to` | `templates/how-to.md` | `site/src/content/docs/{lang}/guides/` |
| `faq` | `templates/faq.md` | `site/src/content/docs/{lang}/` |
| `release-notes` | `templates/release-notes.md` | `site/src/content/docs/{lang}/` |

**Steps:**

1. Chiedi (o rileva da args): tipo, lingua (default: `it`), nome/slug pagina
2. Leggi template corrispondente
3. Sostituisci placeholder: `{{APP_NAME}}`, `{{DATE}}`, `{{VERSION}}` (da CHANGELOG)
4. Scrivi file in cartella target
5. Aggiorna `site/docs-registry.yaml` con la nuova pagina (status: `draft`)
6. Output: path creato + prossimo passo (`/docs audit` o `npm run dev`)

---

## Subcommand: `/docs review-drafts`

Lancia N agent paralleli per **verificare l'accuratezza** e completare le pagine draft.

**CRITICO: Lanciare SEMPRE gli agent.** Non shortcuttare mai questa fase. Anche se non ci sono
placeholder `{{...}}`, la review verifica che il contenuto sia **accurato rispetto al codice sorgente**.
Zero placeholder NON significa "già verificato" — significa solo "qualcuno ha scritto del testo".

**Pre-condizioni:**

- `docs-registry.yaml` esiste con almeno 1 pagina in status `draft`
- Se 0 draft: "Nessuna draft da revisionare. Tutte le pagine sono published o missing."

**Steps:**

1. Leggi `docs-registry.yaml` → filtra pagine con `status: draft`
2. Per ogni draft, verifica che il file esista su disco (skip se missing)
3. Chiedi conferma: "Hai N pagine draft. Lancio N agent in parallelo per verificarle?"
4. Se confermato, per ogni draft lancia un **Agent** in parallelo:

```
Agent(
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Review and verify draft doc: <filename>",
  prompt: """
    Sei un technical reviewer. Il tuo compito è VERIFICARE l'accuratezza di questa
    pagina di documentazione rispetto al codice sorgente reale.

    FILE DA VERIFICARE: <path-to-draft>
    PROGETTO: <project-name>

    ISTRUZIONI:
    1. Leggi il file docs da verificare
    2. Leggi il codice sorgente corrispondente in backend/ o app/ o src/
    3. Leggi CHANGELOG.md per le feature documentate
    4. Per ogni affermazione nella docs, VERIFICA che corrisponda al codice reale:
       - I nomi delle classi/funzioni sono corretti?
       - I parametri e i return type corrispondono?
       - Gli esempi di codice funzionerebbero se eseguiti?
       - Le versioni citate sono corrette?
       - Mancano funzionalità importanti non documentate?
    5. Se trovi placeholder ({{...}}, [Passo X], TODO, TBD): sostituiscili con contenuto reale
    6. Se trovi errori: correggili con Edit tool
    7. Se trovi funzionalità mancanti: aggiungile
    8. Non inventare funzionalità — documenta solo ciò che esiste nel codice

    Output finale:
    - VERDICT: ACCURATE / NEEDS_FIXES / INACCURATE
    - Lista di ciò che hai verificato
    - Lista di ciò che hai corretto (se NEEDS_FIXES)
    - Lista di funzionalità mancanti aggiunte (se presenti)
  """
)
```

5. Attendi completamento di tutti gli agent
6. Per ogni file, mostra il verdetto dell'agent:

```
  ✓ getting-started.md     — ACCURATE (verified 12 code refs, 0 fixes)
  ⚠ features/audio.md      — NEEDS_FIXES (2 wrong param names corrected)
  ✓ guides/router-pattern.md — ACCURATE (verified 8 code refs, added 1 missing feature)
```

7. Chiedi conferma finale: "Agent hanno verificato N pagine. Le marco come published?"
8. Se confermato: aggiorna `docs-registry.yaml`:
   - `status: draft → published`
   - `last_updated: <today>`
   - `linked_version: <latest-from-changelog>`

**Output:**

```
## Review Drafts — <project> — <date>

Lancio 6 agent in parallelo...

  ✓ getting-started.md     — 12 placeholder → contenuto reale (agent 1, 45s)
  ✓ feature-guide-media.md — 8 placeholder → contenuto reale (agent 2, 38s)
  ✓ feature-guide-audio.md — 9 placeholder → contenuto reale (agent 3, 41s)
  ✓ how-to-upload.md       — 6 placeholder → contenuto reale (agent 4, 32s)
  ✓ faq.md                 — 10 placeholder → contenuto reale (agent 5, 35s)
  ✓ api-reference.md       — 15 placeholder → contenuto reale (agent 6, 52s)

Tutti completati. Marco come published? [Sì / No / Revisiono prima]
```

Se l'utente sceglie "Revisiono prima": mostra il contenuto di ogni file per review manuale prima di marcare published.

**Invocato da:**

- Direttamente: `/docs review-drafts`
- Step 4b del routing di `/docs` (summary) quando ci sono ≥1 draft
- `/docs full` dopo la fase create

---

## Subcommand: `/docs audit`

Trova pagine stale, mancanti, link rotti. Usato da `/health docs`.

**Steps:**

1. **Registry delta** — confronta `docs-registry.yaml` con file effettivi in `site/src/content/docs/`
   - File nel registry ma non su disco → `missing`
   - File su disco ma non nel registry → `unregistered` (aggiunge al registry come `draft`)

2. **Staleness check** — per ogni pagina `published`:

   ```bash
   PAGE_TS=$(git log -1 --format="%ct" -- site/src/content/docs/it/getting-started.md)
   CODE_TS=$(git log -1 --format="%ct" -- backend/ src/ 2>/dev/null)
   DIFF_DAYS=$(( (CODE_TS - PAGE_TS) / 86400 ))
   # Se DIFF_DAYS > 30 → stale
   ```

3. **Link check** — grep per `[text](url)` e `href="..."` nelle pagine IT e EN
   - Link interni (`/docs/...`) → verifica file esista in `site/src/content/docs/`
   - Link esterni → skip (troppo lenti per audit locale)

4. **Language parity** — per ogni pagina IT, verifica esista controparte EN e viceversa
   - Mancante → `status: missing` nel registry

5. **Output:**

```
## Docs Audit — <project> — <date>

Pages: 8 total (5 published, 2 draft, 1 stale, 0 missing)
Links: 12 internal (all OK), 0 broken
Languages: IT 8 pages | EN 3 pages | 5 EN missing

Stale (>30 days behind code):
  ⚠ it/features/invoices.md — last updated 45 days ago

Missing EN translations:
  ⚠ en/getting-started.md
  ⚠ en/features/invoices.md
  ... 3 more

Suggested actions:
  /docs update it/features/invoices.md
  /docs translate en
```

**Gate (usato da `/health docs`):**

- `PASS`: 0 stale, 0 missing, 0 broken links
- `WARN`: stale > 30 giorni OR missing EN pages
- `FAIL`: pagine required mancanti (getting-started) OR broken links interni

---

## Subcommand: `/docs update`

Aggiorna una pagina stale basandosi su git diff + CHANGELOG.

**Steps:**

1. Leggi il file docs da aggiornare
2. `git log --oneline -- backend/ src/` dall'ultima modifica del file docs → lista commit recenti
3. Controlla CHANGELOG per entry aggiunte dall'ultima modifica docs
4. Propone aggiornamenti specifici: nuove feature da documentare, comportamenti cambiati
5. Applica aggiornamenti con conferma utente
6. Aggiorna `last_updated` e `linked_version` nel registry

---

## Subcommand: `/docs translate <lang>`

Traduce pagine mancanti da lingua source a lingua target.

**Default:** `it → en` (IT è la lingua primaria)

**Steps:**

1. Identifica pagine con status `missing` per la lingua target (da audit)
2. Per ogni pagina source:
   - Leggi contenuto IT
   - Traduci con Claude (istruzioni: mantieni struttura MDX, non tradurre codice, mantieni slug frontmatter)
   - Scrivi file EN equivalente
   - Aggiorna registry: status `draft` (richiede review umana)
3. Output: N pagine tradotte, lista path creati

**Nota:** traduzioni auto hanno status `draft` — richiedono review prima di `published`.

---

## Subcommand: `/docs publish [env]`

Deploya `site/dist/` sul VPS.

**Env disponibili:** `staging` (default durante sviluppo), `stable` (default senza args)

**Steps:**

1. Verifica `site/` esiste e `npm run build` funziona localmente
2. Build: `cd site && npm ci && npm run build`
3. Deploy:
   - **Oggi (make):** `make deploy-site` — rsync su `/opt/{app}/site/dist/`
   - **Futuro (Forgejo Actions):** push su branch `docs/staging` o `docs/stable` → trigger CI
4. Verifica: `curl -s https://{domain}/docs/` → controlla 200 OK
5. Aggiorna registry: `last_deployed: <date>` per tutte le pagine `published`

---

## Subcommand: `/docs registry`

CRUD su `site/docs-registry.yaml`.

**Operazioni:**

```
/docs registry              # mostra tutte le pagine con status
/docs registry stale        # solo pagine stale (>30 giorni)
/docs registry missing      # pagine nel registry ma non su disco
/docs registry update <file> status=published
```

---

## Subcommand: `/docs features`

Estrae feature list da CHANGELOG.md + FastAPI routes.

**Steps:**

1. Leggi `CHANGELOG.md` → estrai sezioni `### Added` per tutte le versioni
2. Grep `backend/` o `src/` per route FastAPI (`@router.get`, `@router.post`, etc.)
3. Merge e deduplicazione → lista feature con versione di introduzione
4. Genera file `site/src/content/docs/it/features.md` con tabella feature

---

## Subcommand: `/docs migrate`

Audit strutturale del repo corrente e proposta di migrazione alla convenzione standard.

**Convenzione target:**

```
{repo}/
├── backend/     ← FastAPI (o app/ per HTMX)
├── frontend/    ← Next.js/React/Vite (se esiste)
├── site/        ← Astro (marketing + docs, NUOVO)
├── docs/        ← dev docs interni (invariata)
└── Makefile
```

**Steps:**

1. Scansiona struttura root del repo
2. Identifica deviazioni:
   - `src/` invece di `backend/` o `frontend/` → suggerisci rename
   - `docs/` contiene contenuto user-facing → suggerisci spostamento in `site/`
   - `site/` o `docsite/` assente → suggerisci `/docs scaffold`
   - `www/` separata da `site/` → suggerisci merge
3. Presenta tabella di migrazione proposta con impatto (rename, move, create)
4. Esegue solo le azioni approvate dall'utente
5. Aggiorna `docs/development/architecture.md` con la nuova struttura

---

## Subcommand: `/docs video` (P3)

Crea video guide automatizzate.

**Stack:** Playwright (registrazione headful) → Fabrica FFmpeg (captions overlay) → `/tts` (narrazione)

_Da implementare in DOCS-0.2 milestone._

---

## Subcommand: `/docs full`

Esegue pipeline completa.

```
1. /docs scaffold      (se site/ non esiste)
2. /docs audit         (trova gap)
3. /docs create        (per ogni pagina missing required)
4. /docs translate en  (se pagine EN mancanti)
5. /docs publish       (deploy)
```

---

## Registry Format

`site/docs-registry.yaml` — una entry per ogni pagina docs:

```yaml
meta:
  project: appratio
  domain: appratio.it
  docs_base: /docs
  last_audit: 2026-03-16

docs:
  getting-started-it:
    file: src/content/docs/it/getting-started.md
    type: getting-started # getting-started | feature-guide | how-to | faq | release-notes | reference | video
    language: it
    feature: onboarding
    last_updated: 2026-03-16
    status: published # draft | published | stale | missing
    linked_version: "1.0.0"
  getting-started-en:
    file: src/content/docs/en/getting-started.md
    type: getting-started
    language: en
    status: missing
```

**Valori status:**

- `draft` — creata ma non review-ata
- `published` — live in produzione
- `stale` — code più recente del docs di >30 giorni
- `missing` — nel registry ma file non su disco

---

## Integrazione `/health docs`

`/health docs` delega a `/docs audit` e ne eredita il gate:

```
Invoke: /docs audit
Gate:
  PASS  → /docs audit restituisce 0 stale, 0 missing required, 0 broken links
  WARN  → stale > 30 giorni OR missing EN pages OR pagine opzionali mancanti
  FAIL  → getting-started mancante OR broken links interni OR site/ assente
```

Sostituisce il check base attuale (CLAUDE.md/README staleness rimane in `/health docs` come check separato).

---

## Thresholds

| Check           | WARN                          | FAIL                                              |
| --------------- | ----------------------------- | ------------------------------------------------- |
| Staleness       | >30 giorni codice più recente | >60 giorni                                        |
| Missing pages   | pagine opzionali mancanti     | getting-started mancante                          |
| Language parity | EN pages < 50% delle IT       | EN getting-started mancante                       |
| Broken links    | -                             | qualsiasi link interno 404                        |
| site/ presenza  | -                             | `site/` assente (FAIL solo se progetto ha utenti) |
