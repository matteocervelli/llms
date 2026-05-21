---
name: supply-chain-audit
description: 'Forensic scan for npm/PyPI supply-chain compromise (Shai-Hulud/TeamPCP campaigns) — checks persistence, hook injection, compromised packages, IOC strings, C2, dead-man switches. Use when auditing a machine or repo for malicious dependencies. Trigger on "supply chain audit", "check for compromised packages", "Shai-Hulud", "scan for malicious deps".'
triggers:
  - /supply-chain-audit
---

# Supply Chain Audit Skill

Scanner forense completo per rilevare compromissioni da attacchi supply-chain npm/PyPI.

## Campagne coperte

| Campagna                      | Data       | Vettori principali                                |
| ----------------------------- | ---------- | ------------------------------------------------- |
| Shai-Hulud SAP/BUN wave       | 2026-04-29 | mbt, @cap-js/\*, SessionStart hook injection      |
| Mini Shai-Hulud TanStack wave | 2026-05-11 | @tanstack/\*, mistralai, guardrails-ai, lightning |
| Varianti in corso             | continuo   | @opensearch-project, @squawk/_, @uipath/_         |

## Utilizzo

```
/supply-chain-audit              # scan macchina corrente
/supply-chain-audit --quick      # scan rapido (salta scan git e IOC string)
/supply-chain-audit remediate    # guida remediation interattiva
```

## Subcommand: scan

**Esegui sempre questo prima di revocare qualsiasi token** (dead-man's switch).

Passi:

1. Individua il detection script:

```bash
SCRIPT="$HOME/.claude/scripts/supply-chain-audit.sh"
[ ! -f "$SCRIPT" ] && echo "ERROR: script non trovato — aggiorna ~/.claude con git pull" && exit 1
```

2. Esegui localmente:

```bash
bash "$SCRIPT"
```

3. Se `--quick`:

```bash
QUICK=true bash "$SCRIPT"
```

4. Se `--all-machines`, esegui in parallelo via SSH su tutte le macchine:

```bash
for host in studio mini macbook; do
  echo "=== $host ==="
  ssh "$host" "bash -s" < "$SCRIPT" &
done


wait
```

5. Interpreta il risultato:
   - **Exit 0 / PULITO**: nessun IOC trovato → macchina sicura
   - **Exit 2 / ATTENZIONE**: warning non critici → revisione manuale consigliata
   - **Exit 1 / COMPROMESSO**: IOC critici trovati → seguire remediation immediatamente

## Subcommand: remediate

Guida interattiva passo-per-passo. **L'ordine è critico** — non saltare fase.

### FASE 1 — Containment (PRIMA di revocare qualsiasi token)

⚠️ Il malware pianta un dead-man's switch: se revochi il token GitHub rubato **prima** di aver rimosso il watcher, il processo wipe la home directory.

```bash
# 1a. Termina il processo watcher se attivo
pkill -f gh-token-monitor 2>/dev/null || true
pkill -f tanstack_runner 2>/dev/null || true
pkill -f router_runtime 2>/dev/null || true

# 1b. Rimuovi file di persistenza
rm -f ~/.claude/router_runtime.js ~/.claude/setup.mjs ~/.claude/tanstack_runner.js
rm -f ~/.vscode/setup.mjs ~/.local/bin/gh-token-monitor.sh
rm -rf ~/.config/gh-token-monitor ~/.dev-env

# 1c. Disabilita systemd / LaunchAgent
systemctl --user disable --now gh-token-monitor 2>/dev/null || true
launchctl unload ~/Library/LaunchAgents/com.user.gh-token-monitor.plist 2>/dev/null || true
rm -f ~/.config/systemd/user/gh-token-monitor.service
rm -f ~/Library/LaunchAgents/com.user.gh-token-monitor.plist

# 1d. Se il malware ha creato un repo GitHub: NON eliminarlo subito
# → privatizzalo su GitHub (Settings → Danger Zone → Make private)
# → rimuovi tutti i runner auto-registrati (Settings → Actions → Runners)
```

### FASE 2 — Eradication

```bash
# 2a. Rimuovi node_modules e cache npm
find ~/dev -name "node_modules" -maxdepth 5 -type d \
  -exec rm -rf {} + 2>/dev/null || true
npm cache clean --force 2>/dev/null || true

# 2b. Rimuovi workflow iniettati
find ~/dev -name "codeql_analysis.yml" -path "*/.github/workflows/*" -delete 2>/dev/null
find ~/dev -name "formatter_*.yml" -path "*/.github/workflows/*" -delete 2>/dev/null
find ~/dev -name "discussion.y*ml" -path "*/.github/workflows/*" -delete 2>/dev/null

# 2c. Verifica hook in .claude/settings.json
# Apri ~/.claude/settings.json e rimuovi qualsiasi hook non riconosciuto
# Hook legittimi: hook_handler.py, supply-chain-guard.py, session_start_memory.py, jq docker

# 2d. Reinstalla dipendenze in modo sicuro
# pnpm install --frozen-lockfile    (usa lockfile esistente)
# uv sync --locked                  (usa lockfile esistente)
```

### FASE 3 — Credential Rotation (DOPO la rimozione del malware)

Solo dopo aver completato le fasi 1 e 2, ruota nell'ordine:

1. **npm tokens**: `npm token revoke <token>` — poi crea nuovo con scope minimo
2. **GitHub PAT**: Settings → Developer Settings → Tokens → revoca tutti
4. **AWS keys**: IAM → revoca access key, crea nuova con scope minimo
5. **Altri cloud credentials** (GCP, Azure, etc.)
6. **SSH keys**: se `~/.ssh/` è stato letto, rigenera tutte le chiavi

### FASE 4 — Verifica finale

```bash
bash ~/.claude/scripts/supply-chain-audit.sh
```

Deve terminare con **EXIT 0 / PULITO**.

## IOC Reference completo

### File malware noti

- `~/.claude/router_runtime.js` — stealer principale
- `~/.claude/setup.mjs` — loader
- `~/.claude/tanstack_runner.js` — worm propagation
- `~/.vscode/setup.mjs` — VS Code persistence
- `~/.local/bin/gh-token-monitor.sh` — dead-man's switch
- `~/.config/gh-token-monitor/` — config watcher
- `~/.dev-env/` — fake runner directory

### Domìni C2

- `api.masscan.cloud` — exfiltration
- `filev2.getsession.org` — encrypted dead-drop
- `git-tanstack.com` — attacker infra
- `seed1.getsession.org` — session protocol node

### IOC strings nel codice

- `"A Mini Shai-Hulud has Appeared"`
- `"OhNoWhatsGoingOnWithGitHub"`
- `"ctf-scramble-v2"`
- `"IfYouRevokeThisToken"`
- `"SHA1HULUD"`
- `"voicproducoes"`

### Versioni npm compromesse (selezionate)

- `@tanstack/react-router`: 1.169.5, 1.169.8
- `@opensearch-project/opensearch`: 3.5.3, 3.6.2, 3.7.0, 3.8.0

### Versioni PyPI compromesse

- `mistralai`: 2.4.6
- `guardrails-ai`: 0.10.1
- `lightning`: 2.6.2, 2.6.3

## Protezioni preventive già in place (non rieseguire)

- `~/.claude/hooks/supply-chain-guard.py`: PreToolUse hook — permette frozen installs e sfw-prefixed, blocca risoluzione senza protezione
- `~/.claude/rules/lockfile-safety.md`: policy aggiornata per flusso sfw

## Fonti

- [JFrog — Shai-Hulud Remediation Guide](https://research.jfrog.com/post/shai-hulud-the-second-coming-remediation-guidance/)
- [StepSecurity — Mini Shai-Hulud TanStack](https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem)
- [Phoenix Security — SAP/BUN wave](https://phoenix.security/mini-shai-hulud-sap-cap-mbt-npm-supply-chain-bun-credential-stealer/)
- [Snyk — TanStack compromise](https://snyk.io/blog/tanstack-npm-packages-compromised/)
- [Mend — 172 packages list](https://www.mend.io/blog/mini-shai-hulud-is-back-172-npm-and-pypi-packages-compromised-in-latest-wave/)
