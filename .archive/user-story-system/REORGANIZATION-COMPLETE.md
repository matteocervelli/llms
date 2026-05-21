# User Story System - Reorganization Complete ✅

## Data: 2025-11-03

Il sistema user story è stato completamente riorganizzato seguendo le regole di Claude Code per una struttura auto-contenuta e modulare.

## Cambiamenti Principali

### 1. Struttura Directory - PRIMA

```
user-story-system/
├── scripts/                 # ❌ Directory separata
│   ├── generate_story_from_yaml.py
│   ├── validate_story_invest.py
│   ├── check_dependencies.py
│   └── [altri script...]
├── config/                  # ❌ Directory separata
│   ├── automation-config.yaml
│   ├── personas.yaml
│   └── story-statuses.yaml
├── templates/               # ❌ Directory separata
│   ├── story-template.yaml
│   └── [altri template...]
└── .claude/
    ├── skills/
    │   └── [solo SKILL.md files]
    ├── commands/
    └── agents/
```

### 2. Struttura Directory - DOPO

```
user-story-system/
├── stories/
│   ├── yaml-source/
│   ├── generated-docs/
│   └── backlog/
├── epics/
└── .claude/
    ├── skills/              # ✅ Ogni skill auto-contenuta
    │   ├── user-story-generator/
    │   │   ├── SKILL.md
    │   │   ├── scripts/     # Script specifici
    │   │   ├── config/      # Config specifiche
    │   │   └── templates/   # Template specifici
    │   ├── story-validator/
    │   │   ├── SKILL.md
    │   │   ├── scripts/
    │   │   └── config/
    │   ├── technical-annotator/
    │   │   ├── SKILL.md
    │   │   └── scripts/
    │   ├── dependency-analyzer/
    │   │   ├── SKILL.md
    │   │   └── scripts/
    │   └── sprint-planner/
    │       ├── SKILL.md
    │       └── scripts/
    ├── commands/
    │   ├── user-story-new.md
    │   ├── user-story-refine.md
    │   ├── user-story-annotate.md
    │   ├── user-story-deps.md
    │   └── user-story-sprint.md
    └── agents/
        ├── qa-validator-agent.md
        ├── technical-annotator-agent.md
        └── story-orchestrator-agent.md
```

## Distribuzione File

### user-story-generator/
**Script:**
- `generate_story_from_yaml.py` - Genera Markdown da YAML
- `batch_story_generator.py` - Elaborazione batch
- `github_sync.py` - Sincronizzazione GitHub
- `create_story.sh` - Creazione story da template
- `models.py` - Modelli dati Pydantic

**Config:**
- `automation-config.yaml` - Configurazione sistema
- `personas.yaml` - Definizioni personas

**Templates:**
- `story-template.yaml` - Template YAML story
- `story-template.md` - Template Markdown story
- `epic-template.yaml` - Template YAML epic
- `epic-template.md` - Template Markdown epic
- `github_issue_template.md` - Template issue GitHub

### story-validator/
**Script:**
- `validate_story_invest.py` - Validazione criteri INVEST

**Config:**
- `story-statuses.yaml` - Stati story e transizioni

### technical-annotator/
**Script:**
- (nessuno script dedicato - usa generate_story_from_yaml.py)

### dependency-analyzer/
**Script:**
- `check_dependencies.py` - Analisi dipendenze
- `story_map_generator.py` - Mappe visuali story

### sprint-planner/
**Script:**
- `move_to_sprint.sh` - Spostamento story a sprint
- `sync_github.sh` - Wrapper GitHub CLI

## Modifiche ai Path

### Script Python
Tutti gli script ora usano path dinamici relativi alla loro posizione:

```python
from pathlib import Path

# Directory della skill (parent di scripts/)
SKILL_DIR = Path(__file__).parent.parent

# Config files
CONFIG_PATH = SKILL_DIR / "config" / "automation-config.yaml"

# Templates
TEMPLATES_PATH = SKILL_DIR / "templates"

# Project root (3 livelli sopra)
PROJECT_ROOT = SKILL_DIR.parent.parent.parent
STORIES_DIR = PROJECT_ROOT / "stories" / "yaml-source"
```

### Script Shell
Pattern simile per bash:

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SKILL_DIR")")")"
```

### SKILL.md e Commands
Tutti i riferimenti aggiornati da:
```bash
python3 scripts/validate_story_invest.py
```

A:
```bash
python3 .claude/skills/story-validator/scripts/validate_story_invest.py
```

## Vantaggi della Nuova Struttura

### ✅ Auto-contenimento
Ogni skill ha tutto ciò di cui ha bisogno:
- Script propri
- Configurazione propria
- Template propri

### ✅ Nessuna Dipendenza Esterna
- Non serve più una directory `scripts/` root
- Non serve più una directory `config/` root
- Non serve più una directory `templates/` root

### ✅ Conforme a Claude Code
- Segue le linee guida ufficiali
- Ogni skill in una directory separata
- Script e risorse dentro la skill

### ✅ Facile Deployment
Due opzioni per usare globalmente:

**Opzione A - Symlink (consigliato):**
```bash
ln -s /path/to/user-story-system/.claude/skills/user-story-generator ~/.claude/skills/
ln -s /path/to/user-story-system/.claude/commands/user-story-new.md ~/.claude/commands/
```

**Opzione B - Copia:**
```bash
cp -r user-story-system/.claude/skills/* ~/.claude/skills/
cp user-story-system/.claude/commands/* ~/.claude/commands/
```

### ✅ Manutenibilità
- Chiara separazione delle responsabilità
- Facile trovare dove sta ogni file
- Modifiche locali a una skill non impattano le altre

### ✅ Portabilità
- Ogni skill può essere distribuita separatamente
- Facile condividere una singola skill
- Facile testare skill individualmente

## File Aggiornati

### Script Python (10 file)
1. `generate_story_from_yaml.py` - ✅ Path aggiornati
2. `batch_story_generator.py` - ✅ Path aggiornati
3. `github_sync.py` - ✅ Path aggiornati
4. `validate_story_invest.py` - ✅ Path aggiornati
5. `check_dependencies.py` - ✅ Path aggiornati
6. `story_map_generator.py` - ✅ Path aggiornati
7. `models.py` - ✅ Nessun cambio necessario

### Script Shell (3 file)
8. `create_story.sh` - ✅ Path aggiornati
9. `move_to_sprint.sh` - ✅ Path aggiornati
10. `sync_github.sh` - ✅ Path aggiornati

### SKILL.md (5 file)
11. `user-story-generator/SKILL.md` - ✅ Riferimenti aggiornati
12. `story-validator/SKILL.md` - ✅ Riferimenti aggiornati
13. `technical-annotator/SKILL.md` - ✅ Riferimenti aggiornati
14. `dependency-analyzer/SKILL.md` - ✅ Riferimenti aggiornati
15. `sprint-planner/SKILL.md` - ✅ Riferimenti aggiornati

### Commands (5 file)
16. `user-story-new.md` - ✅ Path aggiornati
17. `user-story-refine.md` - ✅ Path aggiornati
18. `user-story-annotate.md` - ✅ Path aggiornati
19. `user-story-deps.md` - ✅ Path aggiornati
20. `user-story-sprint.md` - ✅ Path aggiornati

### Documentazione (2 file)
21. `README.md` - ✅ Struttura aggiornata
22. `REORGANIZATION-COMPLETE.md` - ✅ Questo file

**Totale: 22 file aggiornati**

## Testing

### Test da Eseguire
1. ✅ Verificare che tutti gli script Python compilino
2. ✅ Verificare che tutti gli script Shell abbiano sintassi valida
3. ⏳ Testare workflow completo creazione story
4. ⏳ Testare validazione story
5. ⏳ Testare analisi dipendenze
6. ⏳ Testare pianificazione sprint

### Come Testare

```bash
# Test compilazione Python
cd .claude/skills/user-story-generator/scripts
python3 -m py_compile *.py

# Test validazione script
cd .claude/skills/story-validator/scripts
python3 validate_story_invest.py --help

# Test analisi dipendenze
cd .claude/skills/dependency-analyzer/scripts
python3 check_dependencies.py --help

# Test workflow completo (da fare)
# 1. Creare una story di test
# 2. Validarla
# 3. Analizzare dipendenze
# 4. Pianificare sprint
```

## Prossimi Passi

### 1. Testing Completo
- [ ] Creare story di test
- [ ] Eseguire tutti i comandi
- [ ] Verificare generazione file
- [ ] Verificare GitHub integration (se configurato)

### 2. Deployment Globale (opzionale)
Una volta testato e confermato che funziona:

```bash
# Creare symlink globali
./deploy-global.sh

# O manualmente
ln -s $(pwd)/.claude/skills/user-story-generator ~/.claude/skills/
ln -s $(pwd)/.claude/skills/story-validator ~/.claude/skills/
# ... altri skills

ln -s $(pwd)/.claude/commands/user-story-*.md ~/.claude/commands/
ln -s $(pwd)/.claude/agents/*.md ~/.claude/agents/
```

### 3. Documentazione
- [x] README aggiornato
- [x] Struttura documentata
- [ ] Guide d'uso per ogni skill
- [ ] Troubleshooting guide

## Note Tecniche

### Cross-Skill References
Le skills possono referenziare risorse da altre skills:

```python
# Dalla story-validator, usare modelli da user-story-generator
from pathlib import Path
GENERATOR_DIR = Path(__file__).parent.parent.parent / "user-story-generator"
sys.path.insert(0, str(GENERATOR_DIR / "scripts"))
from models import StoryModel
```

### Compatibilità
- Python 3.8+
- Bash 4.0+
- Git (per GitHub integration)
- GitHub CLI `gh` (opzionale, per GitHub integration)

### Dipendenze Python
Tutte le dipendenze sono specificate in `requirements.txt` root:
- PyYAML
- Jinja2
- pydantic
- networkx
- tqdm
- requests
- python-dateutil

## Supporto

Per domande o problemi:
1. Controllare README.md
2. Controllare docs/
3. Verificare path negli script
4. Verificare permessi esecuzione

---

**Status:** ✅ Riorganizzazione Completa
**Data:** 2025-11-03
**Versione:** 2.0 (struttura skills auto-contenute)
