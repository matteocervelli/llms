# Guida introduttiva — {{APP_TITLE}}

> Inizia a usare {{APP_TITLE}} in 5 minuti.

## Cosa imparerai

- Come installare/configurare {{APP_TITLE}}
- Come eseguire la prima operazione
- Dove trovare le guide successive

---

## Prerequisiti

- [ ] Python 3.11+ installato
- [ ] Accesso al repository (`git clone ...`)
- [ ] File `.env` configurato (vedi `docs/deployment/` per le variabili)

---

## Installazione

```bash
# 1. Clona il repository
git clone <repo-url>
cd {{APP_NAME}}

# 2. Crea ambiente virtuale
python -m venv .venv && source .venv/bin/activate

# 3. Installa dipendenze
pip install -e .
# oppure: pip install -r requirements.txt

# 4. Configura ambiente
cp .env.example .env
# Modifica .env con le tue credenziali
```

---

## Primo utilizzo

### 1. [Passo 1 — es. avvia il servizio]

```bash
# Comando per avviare
```

### 2. [Passo 2 — es. verifica che funzioni]

```bash
# Comando per verificare
```

### 3. [Passo 3 — es. prima operazione utile]

<!-- Descrivi la prima azione concreta che l'utente/sviluppatore può fare -->

---

## Struttura del progetto

```
{{APP_NAME}}/
├── app/              ← codice principale
├── tests/            ← test suite
├── docs/             ← documentazione
│   ├── user-guide/   ← guide utente (sei qui)
│   └── ...           ← docs sviluppatore
└── README.md
```

---

## Prossimi passi

- [Feature disponibili](./features.md) — lista completa delle funzionalità
- [Guide pratiche](./guides/) — come fare operazioni specifiche
- [FAQ](./faq.md) — domande frequenti
- [CHANGELOG](../../CHANGELOG.md) — ultime novità

---

## Supporto

Per problemi o domande: [{{SUPPORT_CHANNEL}}]
