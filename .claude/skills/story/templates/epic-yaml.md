# Epic YAML Schema

Use this format for all epic YAML files saved to `stories/yaml-source/EP-XXXX.yaml`.

Epics are large features that require decomposition before implementation.
They are NOT implementable directly — they generate child stories via `/story decompose`.

```yaml
id: EP-XXXX
type: epic # distinguishes from story (US-XXXX)
title: "Titolo imperativo breve in italiano"
status: backlog # backlog | in-decomposition | decomposed | done

priority: critical # critical | high | medium | low

# Contesto — perché questa epica esiste
# Obbligatorio. Include: da dove viene (discovery, bando, richiesta cliente),
# link a documenti di riferimento, e cosa già esiste nel sistema.
context: |
  Derivata da [fonte] del [data].
  Riferimenti: docs/strategy/..., docs/development/...

# Il problema che risolve
# Descrizione concreta del dolore utente, con dati se disponibili.
problem: |
  [Descrizione del problema in italiano, 3-5 righe]

# Personas coinvolte (chiave: nome-kebab-case, valore: descrizione ruolo nel contesto)
personas:
  nome-persona: "Descrizione del ruolo nel contesto di questa epica"

# Obiettivo (una frase — il successo misurabile)
goal: "..."

# Metriche di successo (osservabili, non vague)
success_metrics:
  - "Metrica concreta 1"
  - "Metrica concreta 2"

# Stato attuale del sistema (AS-IS)
# Cosa esiste già, cosa manca, benchmark di riferimento
current_state: |
  [Stato attuale in italiano]

# Storie figlie da creare durante il triage/decomposizione
# Lista di titoli — verranno convertiti in US-XXXX da /story decompose
sub_stories:
  - "Titolo storia figlia 1"
  - "Titolo storia figlia 2"
  - "..."

# Dipendenze tecniche (prerequisiti infrastrutturali o architetturali)
technical_dependencies:
  - "Prerequisito 1"

# Collegamento ad altre epiche
blocked_by: [] # EP-XXXX che devono completarsi prima
blocks: [] # EP-XXXX che aspettano questa
parent_epic: null # EP-XXXX se questa è una sotto-epica
child_stories: [] # US-XXXX popolato automaticamente da /story decompose

# Bando (opzionale — solo se deliverable di un bando)
bando:
  voce: "B5.10"
  descrizione: "Nome voce bando"
  scadenza: "YYYY-MM-DD"
  budget_lordo: "€XXXX"
  rimborso: "65% (€XXXX)"
  note: "Note aggiuntive"

# Tracking
sprint: null
github_issue: null # popolato da /story sync

created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: [tag1, tag2, epica]
```

## Epic ID Convention

- Format: `EP-XXXX` (zero-padded 4 digits)
- Counter: `.epic_counter` file in project root (separato da `.story_counter`)
- Increment after each epic creation

## Differenza Epic vs Story

|                              | Epic (EP-XXXX)                      | Story (US-XXXX)      |
| ---------------------------- | ----------------------------------- | -------------------- |
| Implementabile direttamente? | No — va decomposta                  | Sì                   |
| Story points                 | Non si stima                        | Fibonacci 1-8        |
| Acceptance criteria          | No                                  | Sì (Given/When/Then) |
| Contesto richiesto           | Obbligatorio (problem, AS-IS, goal) | Opzionale            |
| Storie figlie                | `sub_stories` + `child_stories`     | —                    |

## Regola d'oro

Se una feature richiede più di 3 storie figlie per essere implementata, è un'epica.
Se stimi >8 story points, è un'epica — splittala.
