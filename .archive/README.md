# .archive/

Contenuto delle versioni precedenti del repo. Non attivamente mantenuto.

## Struttura

| Directory                         | Contenuto                                                                                      | Versione |
| --------------------------------- | ---------------------------------------------------------------------------------------------- | -------- |
| `claude-v1/`                      | Feature-Implementer v2 — 14 agenti, 13 comandi, 40+ skill (v0.1.x)                             | v0.1.0   |
| `builders/`                       | CLI Python: skill_builder, command_builder, agent_builder, doc_fetcher, catalog_system + tests | v0.1.0   |
| `claude_sync/`                    | Tool per sincronizzare configurazioni Claude tra macchine                                      | v0.1.0   |
| `user-story-system/`              | Sistema standalone user story (superseded da `/story`, `/story-verify`)                        | v0.1.0   |
| `frontend-design-system/`         | Design system v1 (superseded dalle skill `frontend`)                                           | v0.1.0   |
| `agents/`, `commands/`, `skills/` | Artefatti Feature-Implementer v2 originali                                                     | v0.1.0   |

## Perché è qui e non eliminato

Questi componenti hanno richiesto un investimento significativo e potrebbero avere valore
come riferimento o punto di partenza per chi vuole costruire tooling simile.

## Non usare in produzione

Il codice in `.archive/` non è mantenuto e potrebbe avere dipendenze stale o pattern superati.
