---
paths:
  - "pyproject.toml"
  - "uv.lock"
  - "pnpm-lock.yaml"
  - "package-lock.json"
  - "yarn.lock"
  - "package.json"
---

# Lockfile Safety and Audit-Before-Install Policy

## Regola fondamentale

**Nessuna risoluzione dipendenze senza protezione.** `uv sync --frozen` e `pnpm install --frozen-lockfile` sono permessi (nessuna risoluzione, usano il lockfile committato). Comandi di risoluzione (`uv lock`, `uv add`, `pnpm add`) richiedono Socket Firewall o audit preventivo.

## Comandi permessi (nessuna risoluzione)

- `uv sync --frozen` / `uv sync --locked` — usa lockfile esistente, nessun fetch di rete
- `pnpm install --frozen-lockfile` — usa lockfile esistente
- `npm ci` — usa package-lock.json esistente

## Flusso per comandi di risoluzione (uv lock, uv add, pnpm add)

**Opzione A (raccomandato):** Esegui nel terminale con Socket Firewall:

- `sfw uv lock` / `sfw uv add <package>`
- `sfw pnpm add <package>` / `sfw pnpm install`

**Opzione B:** Audit preventivo poi installazione manuale:

1. **Esegui l'audit** sulle dipendenze transitive prima di installare
2. **Mostra i risultati** all'utente
3. **Attendi approvazione** esplicita — l'utente esegue l'install nel terminale

```
# npm / pnpm
pnpm audit --audit-level=moderate
osv-scanner --lockfile ./pnpm-lock.yaml

# Python / uv
osv-scanner --lockfile ./uv.lock
pip-audit -r <(uv export --no-hashes 2>/dev/null)
```

Se l'audit fallisce: non procedere. Spiega il problema all'utente.

## Cosa è bloccato (hook automatico PreToolUse)

- Risoluzione senza protezione: `uv lock`, `uv add`, `pnpm add`, `pnpm install` (senza `--frozen-lockfile`), `npm install`, `pip install`, `yarn install/add`
- Lockfile deletion: `rm pnpm-lock.yaml` / `uv.lock` / ecc.

## Cosa è permesso

- **Tutti i comandi prefissati `sfw`**: `sfw uv lock`, `sfw pnpm add`, `sfw npm install` — Socket Firewall attivo
- **Frozen installs**: `uv sync --frozen`, `uv sync --locked`, `pnpm install --frozen-lockfile`, `npm ci`
- **Audit**: `pnpm audit`, `npm audit`, `osv-scanner`, `pip-audit`

## Lockfile

Mai cancellare, rigenerare con `--force`, o sovrascrivere pnpm-lock.yaml, package-lock.json, yarn.lock, uv.lock.

`rm pnpm-lock.yaml`: NEVER — solo l'utente nel terminale.
