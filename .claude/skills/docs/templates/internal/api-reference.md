# API Reference — {{APP_TITLE}}

> Documentazione delle API pubbliche di {{APP_TITLE}}.

## Panoramica

{{APP_TITLE}} espone le seguenti API:

| Endpoint          | Metodo | Descrizione |
| ----------------- | ------ | ----------- |
| {{API_ENDPOINTS}} |

---

## Autenticazione

<!-- Come autenticarsi: JWT, API key, session, etc. -->

```bash
# Esempio di autenticazione
curl -H "Authorization: Bearer <token>" https://...
```

---

## Endpoint

### `GET /api/v1/[risorsa]`

**Descrizione:** [Cosa fa]

**Parametri:**
| Parametro | Tipo | Required | Descrizione |
|---|---|---|---|
| [param] | string | Sì | [Descrizione] |

**Risposta:**

```json
{
  "data": []
}
```

**Esempio:**

```bash
curl https://localhost:8000/api/v1/[risorsa]
```

---

### `POST /api/v1/[risorsa]`

**Descrizione:** [Cosa fa]

**Body:**

```json
{
  "campo": "valore"
}
```

**Risposta:** `201 Created`

---

## Codici di errore

| Codice | Significato           |
| ------ | --------------------- |
| 400    | Richiesta malformata  |
| 401    | Non autenticato       |
| 403    | Non autorizzato       |
| 404    | Risorsa non trovata   |
| 422    | Errore di validazione |
| 500    | Errore interno        |

---

## Rate limiting

<!-- Se applicabile -->

## SDK / Client

<!-- Link a librerie client se esistono -->

---

_Generato da `/docs features` — aggiorna con `/docs update`._
