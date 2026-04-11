---
name: hermes-provider-auth-pool-fix
description: Diagnose und Behebung von Provider-Austausch-Problemen in Hermes, wenn `config.yaml` Änderungen vom internen Credential Pool ignoriert werden.
---

# Hermes Provider Auth Pool Fix & Switching

## Trigger
- User berichtet, dass Agent auf altem Provider (z.B. OpenRouter) festhängt trotz `config.yaml` Wechsels.
- Agent liefert `402/429` Fehler nach Modellwechsel.
- User will Modell wechseln ohne Session-Neustart.

## Root Cause Analysis
Hermes nutzt `auth.json` Credential Pool. Dieser hat Vorrang vor `config.yaml`. 
Fehlt der neue Provider im Pool oder sind alle Einträge auf `exhausted`, wird die Datei ignoriert.

## Diagnostic Steps
1. **Check Config:** `cat ~/.hermes/config.yaml` -> prüfe `provider`, `base_url`, `_config_version`.
2. **Check Auth Pool:** `cat ~/.hermes/auth.json` -> prüfe `credential_pool`.
3. **Verify Pool State:** Prüfe ob neuer Provider im Pool fehlt oder alter Provider `exhausted` sind.

## Repair Workflow

### 1. `auth.json` Credential Pool Patch
Füge den neuen Provider in `credential_pool` von `~/.hermes/auth.json` ein (z.B. via `patch` Tool).
Für Custom-Provider (z.B. Xiaomi) ist der Pool-Key `custom:<name>`:
```json
"custom:xiaomi": [
      {
        "id": "xiaomi-001",
        "label": "XIAOMI_API_KEY",
        "auth_type": "api_key",
        "priority": 0,
        "source": "env:XIAOMI_API_KEY",
        "access_token": "DEIN_KEY_HIER",
        "base_url": "https://api.xiaomimimo.com/v1",
        "last_status": "ok",
        "request_count": 0
      }
    ]
```

### 2. Config Reset Schutz
Stelle sicher, dass `config.yaml` die aktuelle `_config_version` hat (z.B. `12` für v0.7.0). Sonst überschreibt ein Hermes-Update alles.

### 3. Wechsel im laufenden Prozess
Benutze `/model custom:<name>` im Chat, um den internen `model_override` zu setzen. Kein Neustart nötig.